# Diodes Incorporated PI4IOE5V6408

- **Category:** 8-bit **I²C GPIO expander**, 5 V-tolerant, with per-pin high-impedance
  control and an interrupt output
- **Package as fitted:** 16-pin (`INT`, `VDD`, `P7…P0`, `ADDR`, `RESET`, `SCL`, `SDA`,
  `VDD_Bus`, `GND`)
- **Research status:** **no datasheet retrieved.** Everything below is established from
  M5Stack schematics, M5Stack's own driver class, and Meshtastic's raw register writes —
  three independent sources that agree.
- **Retrieved:** 2026-09-04

> **Why this part has a record:** it appears in **three** M5Stack LoRa products as the thing
> that switches an SX1262's antenna path. If an M5Stack LoRa radio initialises but does not
> reach the air, this chip is the first place to look.

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Diodes Incorporated** (formerly Pericom — the `PI` prefix) | part-number convention, `inferred` |
| Function | 8-bit I²C I/O expander | vendor docs |
| I²C address as fitted | **0x43** (7-bit) | M5Stack `PI4IOE5V6408_Class ioe(0x43, …)`; Meshtastic `#define PI4IO_ADDR 0x43` |
| Address selection | `ADDR` pin (9) strap | schematic |
| Bus speed used | **400 kHz** in M5Stack's example | vendor code |
| Supply | `VDD` (2), plus a separate `VDD_Bus` (15) reference | schematic |
| Interrupt | `INT` (1) — **not routed** on the Cap LoRa-1262 | schematic |
| Reset | `RESET` (10) — tied off on the Cap LoRa-1262 | schematic |

Pin order as drawn on the M5Stack symbol: 1 `INT`, 2 `VDD`, 3 `P7`, 4 `P6`, 5 `P5`, 6 `P4`,
7 `P3`, 8 `P2`, 9 `ADDR`, 10 `RESET`, 11 `P1`, 12 `P0`, 13 `SCL`, 14 `SDA`, 15 `VDD_Bus`,
16 `GND`.

## 2. Registers, as used in the field

Meshtastic writes raw registers; this is the primary evidence for the map. **[SRC]**
`meshtastic/firmware` `src/platform/extra_variants/m5stack_cardputer_adv/variant.cpp`

| Register | Name used upstream | Purpose |
|---|---|---|
| **`0x03`** | `PI4IO_REG_IO_DIR` | per-pin direction; **1 = output** |
| **`0x05`** | `PI4IO_REG_OUT_SET` | per-pin output level |
| **`0x07`** | `PI4IO_REG_OUT_H_IM` | per-pin **high-impedance**; **0 = drive** |

⚠ **The high-impedance register is the trap.** A pin configured as an output on this part is
*still* not driving until `0x07` clears its bit. M5Stack's own source comments the line
*"Disable high-impedance so pin can actually drive"*. Any port that sets direction and level
but skips `0x07` produces a pin that measures floating and a radio that appears dead.

Correct order (both vendor and upstream do it this way):

```text
0x03 |= (1 << n)      # output
0x07 &= ~(1 << n)     # not high-Z
0x05 |= (1 << n)      # high
```

M5Unified wraps the same three writes:

```cpp
m5::PI4IOE5V6408_Class ioe(0x43, 400000, &m5::In_I2C);
if (ioe.begin()) {                    // presence == identity, see §4
    ioe.setDirection(0, true);
    ioe.setHighImpedance(0, false);
    ioe.digitalWrite(0, true);
}
```

## 3. ⚠ Registers **not** established

`0x00`–`0x02`, `0x04`, `0x06`, `0x08`+ — including the device-ID register, input register,
pull-up/pull-down configuration, interrupt mask and interrupt status — were **not**
established by this pass, because no datasheet was retrieved and neither code path touches
them. Do not guess them.

## 4. Presence at 0x43 is used as a *product* identity, and that is fragile

Both M5Stack's example and Meshtastic decide **which expansion board is fitted** by probing
address `0x43`:

| Probe | Conclusion drawn |
|---|---|
| ACK | Cap LoRa-1262 (U214) — drive P0 high before RF |
| NAK | Cap LoRa868 (U201) — no antenna switch to set |

Meshtastic probes **`Wire1` first, then `Wire`**, logs `"Cap LoRa-1262 not found"` on
failure, and continues regardless.

**This is a heuristic, not an identity read.** Anything else answering at 0x43 — including a
Grove sensor plugged into the Cap's own pass-through I²C port — is mistaken for the antenna
switch, and the real switch never gets set. Neither code path reads a device-ID register to
confirm.

## 5. Used By

### [M5Stack Cap LoRa-1262 (U214)](../../../devices/m5stack/cap-lora-1262/README.md) — designator `U2`

| Pin | Net | Goes to |
|---:|---|---|
| **12 (`P0`)** | **`SX_ANT_SW`** | `Stamp LoRa-1262 Mini` **pin 10 `SW`** — the LoRa antenna/RF switch |
| 13 (`SCL`) | `SCL` | host **G9** |
| 14 (`SDA`) | `SDA` | host **G8** |
| 2 (`VDD`) | `VDD_3V3` | on-board buck |
| 9 (`ADDR`) | strapped | → 0x43 |
| 1 (`INT`), 10 (`RESET`), 3–8 (`P7…P2`), 11 (`P1`) | **unused** | — |

**Seven of eight outputs are unused** and already on the host's I²C bus — free expansion for
a derivative design. Depopulated around it: `R5/NC`, `R6/NC`, `R7/NC` (10 kΩ), `C13/NC`,
`C14/NC` (100 nF).

Bring-up consequence: **the radio cannot reach the antenna without a working I²C bus**, even
though SPI, reset and BUSY are all direct host GPIO. Full detail:
[`devices/m5stack/cap-lora-1262/features/io-expander-and-rf-switch.md`](../../../devices/m5stack/cap-lora-1262/features/io-expander-and-rf-switch.md).

### [M5Stack Stamp C6LoRa (S012)](../../../devices/m5stack/stamp-c6lora/README.md) — inside the module

The vendor description: *"A PI4IOE5V6408 IO expansion chip is integrated internally to
control the LoRa module's transceiver circuit and **signal amplifier enable** function,
achieving superior power consumption control while providing additional available IO
resources."* Five expander pins are brought out of the module as **`EXT_P0 … EXT_P4`**.

Note the extra job here: as well as the RF switch it gates the **SGM13005L4 LNA**, which is
a real power win compared with an always-on LNA. Address and register usage inside the
module: **not established**.

### [M5Stack Unit C6L (U202)](../../../devices/m5stack/unit-c6l/README.md) — inside the Stamp C6LoRa

Inherited from the module above.

### ❌ Not the same as the PaperMono's expander

The [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) uses **`M5IOE1`**, a
different part with its own quirks (including a documented `M5IOE1_PIN_n` = `n − 1`
off-by-one). Do not carry assumptions across —
[`components/m5stack/m5ioe1`](../../m5stack/m5ioe1/README.md).

## 6. Caveats

| # | Issue |
|---|---|
| 1 | **No datasheet in this repository.** Register map is known only where two code bases exercise it |
| 2 | **The high-impedance register (`0x07`) is mandatory** and easy to miss — §2 |
| 3 | **Presence-probing as product identification is fragile** — §4 |
| 4 | Upstream Meshtastic shipped this init **wrong twice** before it worked (fixes `3261c04a`, 2026-05-18 and `98e0604e`, 2026-05-19; first good release **v2.7.24**). If you are debugging an older build, suspect it |
| 5 | Whether `INT` is usable, and what the interrupt semantics are, is **unknown** here |

## 7. Local artifacts

**None.** No PI4IOE5V6408 datasheet was retrieved. If one is obtained it belongs in
`artifacts/` here, and §3 should shrink accordingly.

## 8. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| P-1 | Cap LoRa-1262 schematic V1.1 | M5Stack | primary | schematic | [`devices/m5stack/cap-lora-1262/artifacts/schematic/`](../../../devices/m5stack/cap-lora-1262/artifacts/schematic/) | 2026-09-04 | 16-pin symbol, `P0` → `SX_ANT_SW`, unused pins |
| P-2 | Cap LoRa-1262 documentation (pin map) | M5Stack | primary | official page | `https://docs.m5stack.com/en/cap/Cap_LoRa-1262` | 2026-09-04 | *"Enable the RF antenna switch: Set P0 of the PI4IOE IO expansion chip to high level."* |
| P-3 | M5Stack Arduino guide | M5Stack | primary | tutorial | `https://docs.m5stack.com/en/arduino/projects/cap/cap_lora868` | 2026-09-04 | `PI4IOE5V6408_Class(0x43, 400000, &m5::In_I2C)` and the three-call sequence |
| P-4 | Meshtastic `variant.cpp` | Meshtastic | primary | repository | `https://github.com/meshtastic/firmware/blob/master/src/platform/extra_variants/m5stack_cardputer_adv/variant.cpp` | 2026-09-04 | **Register numbers 0x03 / 0x05 / 0x07 and their values** |
| P-5 | Stamp C6LoRa store listing | M5Stack | primary | store listing | `https://shop.m5stack.com/products/m5stamp-c6lora-module-esp32-c6-sx1262.json` | 2026-09-04 | Second and third **Used By** entries; LNA-enable role |
