# Cardputer ADV — vendor driver read against the schematic and the register map

**Audited:** 2026-09-07 · workflow step 10 (*audit vendor firmware and driver source against the
primary documents*).

**Sources read side by side**

| Role | Path / identity |
|---|---|
| Schematic | `artifacts/schematic/Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf`, traced in [`schematic-netlist.md`](schematic-netlist.md) |
| Vendor driver | `artifacts/source-snapshots/M5Cardputer-f1392858/` — M5Stack `M5Cardputer`, commit `f1392858` |
| Register map | `…/src/utility/Adafruit_TCA8418/Adafruit_TCA8418_registers.h` (vendored with the driver) |
| Component record | [`components/texas-instruments/tca8418`](../../../components/texas-instruments/tca8418/README.md) |

**Evidence status.** Register *addresses and bit names* below are quoted from the vendored
header, which is primary for what the driver believes. Claims about what the silicon does with
those bits are marked where **no TI datasheet is held in this repository** to check them
against — that is a gap, not an assertion.

Every finding is labelled **active** (misbehaves in normal use) or **inert** (wrong or fragile,
but harmless as the code currently runs). An incorrect write that is later overwritten is a
latent trap, not a live bug.

---

## A. Agreements worth recording — the driver matches the sheet

These were checked because they are the things that usually go wrong, and they are correct here.
Recording a verified agreement is as useful as recording a defect: it stops the next agent
re-deriving it.

| Claim in the driver | Source | Schematic | Verdict |
|---|---|---|---|
| `#define DEFAULT_TCA8418_INT_PIN 11` | `src/utility/Keyboard/KeyboardReader/TCA8418.cpp:13` | `U9` pin 24 `INT` → net `G11` (`NLG11` @ 78.50, 224.66, sheet 2) | ✅ correct |
| `_tca8418->matrix(7, 8)` — 7 rows | `TCA8418.cpp:38` | `U9` pin 1 `ROW7` has **no net label and no aligned peer pin**; only `ROW0`…`ROW6` are netted | ✅ correct; the sheet wires 7 rows |
| 8 columns | `TCA8418.cpp:38` | `U9` pins 9–16 → `Y7`…`Y0` through 22 R/1 % series resistors `R27`…`R34` | ✅ correct |
| I²C address (implicit, fixed part) | `Adafruit_TCA8418` | sheet 2 prints **`7-bit Address 34H`** @ (106–142, 312.5) | ✅ consistent |
| `pinMode(_interrupt_pin, INPUT)` — **no** internal pull-up on an open-drain `INT` | `TCA8418.cpp:44` | `R37` 3.3 kΩ pulls `G11` to `+3.3V` (one of three at x = 48.5 / 59.5 / 70.5, all spanning y 184.57→206.57, pulling `SDA`, `SCL`, `INT`) | ✅ correct **because of `R37`** — see finding 5 |
| BMI270 at `0x69` | M5Unified | `U7` pin 1 `SDO` pulled to `+3.3V` by `R43` 3.3 kΩ; sheet prints `7-bit Address 69H` | ✅ correct |
| BMI270 polled, never interrupt-driven | M5Unified | `U7` `INT1` (pin 4) and `INT2` (pin 9) are **not routed** | ✅ correct, and now known to be *forced* rather than chosen |

## B. Findings

### 1. `Adafruit_TCA8418::begin()` discards every status it collects — **active, low severity**

`src/utility/Adafruit_TCA8418/Adafruit_TCA8418.cpp:60-74`

```cpp
bool Adafruit_TCA8418::begin() {
    bool ret = false;
    ret = writeRegister8(TCA8418_REG_GPIO_DIR_1, 0x00);
    ret = writeRegister8(TCA8418_REG_GPIO_DIR_2, 0x00);
    ret = writeRegister8(TCA8418_REG_GPIO_DIR_3, 0x00);
    ret = writeRegister8(TCA8418_REG_GPI_EM_1, 0xFF);
    ret = writeRegister8(TCA8418_REG_GPI_EM_2, 0xFF);
    ret = writeRegister8(TCA8418_REG_GPI_EM_3, 0xFF);
    ...
```

`ret` is **assigned, never tested**. Only the last assignment survives to the return. A bus
fault on any earlier write is silently discarded.

`TCA8418.cpp:33` branches on that return value and prints an error, so the caller *believes* it
is checking. **Practical consequence:** a partially-failed initialisation — the realistic case
being marginal pull-ups or a contended bus — reports success and yields a keyboard that
enumerates but behaves oddly. A wholly absent device still fails, because the final write also
fails, which is why the severity is low rather than high.

### 2. There is no device probe at all — **inert, but state it**

The TCA8418 has no identification register, so `begin()` returning `true` means only "the last
write was ACKed". The driver never reads back a register it has just written, which would be the
cheap substitute. Not a defect; a limit on what "keyboard initialised OK" means.

### 3. Two different values are written to `INT_STAT` — **inert**

| Site | Write |
|---|---|
| `Adafruit_TCA8418.cpp:184` (`flush()`) | `writeRegister8(TCA8418_REG_INT_STAT, 3)` |
| `TCA8418.cpp:61` (`update()`) | `writeRegister8(TCA8418_REG_INT_STAT, 1)` |

`INT_STAT` is write-1-to-clear. `flush()` clears bits 0 and 1 (`K_INT`, `GPI_INT`); the steady-state
`update()` path clears only bit 0. Per the vendored header, bit 3 is
`TCA8418_REG_STAT_OVR_FLOW_INT (0x08)` and is **never cleared anywhere in the driver.**

This is **inert as configured**: `enableInterrupts()` (`Adafruit_TCA8418.cpp:313-318`) sets only
`GPI_IEN | KE_IEN` and leaves `OVR_FLOW_IEN (0x08)` alone, so an overflow can set the status bit
but will not assert `INT`. The `_isr_flag` clear test at `TCA8418.cpp:63` reads
`(intstat & 0x01) == 0`, which is consistent with clearing only bit 0. Nothing hangs.

It becomes **active** the moment anyone enables the overflow interrupt: `OVR_FLOW_INT` would
latch, `INT` would stay asserted, and `_isr_flag` would never clear — a hung keyboard. Flagged
as a latent trap rather than a live bug.

### 4. FIFO overflow is unobservable — **active, benign under normal typing**

`update()` reads exactly **one** event per call (`_tca8418->getEvent()`,
`Adafruit_TCA8418.cpp:162-166` → a single read of `KEY_EVENT_A`), then re-reads `INT_STAT` and
leaves `_isr_flag` set if more events are pending. Draining therefore proceeds one event per
`M5Cardputer.update()` iteration.

The driver never reads `TCA8418_REG_KEY_LCK_EC (0x03)`, the event counter, and never sets
`TCA8418_REG_CFG_OVR_FLOW_M (0x20)`, which selects the overflow policy. **Consequence:** on a
burst longer than the controller's event FIFO, keystrokes are discarded and *nothing in the stack
can tell that it happened.* For a 56-key device driven by human fingers this will essentially
never fire; for macro playback, a key-rollover test, or a slow main loop, it is a real and
silent loss path.

### 5. `GPI_EM_1..3 = 0xFF` enables key events on pins that are not in the matrix — **inert, fragile**

`begin()` marks **all** GPI pins as key-event sources before `matrix(7, 8)` narrows the keypad
selection via `KP_GPIO_1..3`. `ROW7` (`U9` pin 1) is left as a GPIO with event reporting enabled
and, per the schematic, **nothing connected to it**.

It is inert because the part's unused row/column inputs sit at a defined level on their own.
**This could not be verified against a datasheet — none is held here** — so the statement is
that the board has shipped in this configuration without reports of phantom keys, which is
evidence but not proof. The fragility is real: the configuration depends on silicon default
behaviour rather than on anything the driver states.

### 6. `attachInterruptArg(..., CHANGE)` on a level-latched, active-low output — **inert**

`TCA8418.cpp:45`. `INT` is open-drain and asserted low until `INT_STAT` is cleared, so the
meaningful edge is the falling one. `CHANGE` also fires on the release, setting `_isr_flag` a
second time; `update()` then finds `INT_STAT` bit 0 already clear and simply drops the flag.
Harmless, slightly wasteful, and worth knowing if you ever count interrupts.

---

## C. Not a defect: three things that look wrong and are not

- **`M5Unified` polls the BMI270 rather than using an interrupt.** Established above: the
  interrupt lines do not exist on this board. The library is correct.
- **`pinMode(INT, INPUT)` with no pull on an open-drain output.** Correct here, because `R37`
  3.3 kΩ is fitted. On a board without it this exact line would be a live bug — so do **not**
  copy this driver to another TCA8418 design without checking for the resistor.
- **`matrix(7, 8)` when the symbol shows eight `ROW` pins.** The symbol has eight pin *names*;
  only seven are netted. The driver matches the wiring, not the symbol.

## D. Gap this audit exposes

**No TCA8418 datasheet is retained in this repository.** Every register-semantics claim above
rests on the vendored `Adafruit_TCA8418_registers.h` comments, which are secondary. Findings 3,
4 and 5 would move from "argued" to "established" with TI `SCPS215` in
`components/texas-instruments/tca8418/artifacts/`. Recorded as an acquisition target, not
silently worked around.
