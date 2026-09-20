# DinMeter — vendor driver read against the schematic

**Audited:** 2026-09-07 · workflow step 10.

**Sources read side by side**

| Role | Path / identity |
|---|---|
| Schematic | `artifacts/schematic/K134_DIN_Meter_v1.0-schematic.pdf`, traced in [`schematic-netlist.md`](schematic-netlist.md) |
| Vendor driver | `artifacts/source-snapshots/M5DinMeter-8ccbad7297beb82a140f812e5606e060d8a5e0dc.tar.gz` → `m5stack-M5DinMeter-8ccbad7/` |

---

## A. Agreements — the driver matches the sheet

| Claim | Source | Schematic | Verdict |
|---|---|---|---|
| `#define DIAL_ENCODER_PIN_A 41` | `src/M5DinMeter.h:8` | `J5.3` (`A`) → net `IN_A` → module pad 23, pin name **`G41/MTDI`** | ✅ |
| `#define DIAL_ENCODER_PIN_B 40` | `src/M5DinMeter.h:9` | `J5.5` (`B`) → net `IN_B` → module pad 21, pin name **`G40/MTDO`** | ✅ |
| Buzzer on GPIO3 (`spk_cfg.pin_data_out = GPIO_NUM_3`, M5Unified) | — | net `beep` → module pad 3, pin name `G3` | ✅ |
| Buzzer modelled as a driven tone source, not on/off | M5Unified / ESP-IDF board support | base drive is **AC-coupled through `C27` 10 µF**; a DC level cannot reach the transistor | ✅ and now *explained* by the hardware |

## B. Findings

### 1. `pinMode(INPUT_PULLUP)` on lines that already carry 10 kΩ pull-ups — **inert**

`src/utility/Encoder.h`, `ENCODER::begin()`:

```cpp
pinMode(_pin1, INPUT_PULLUP);
pinMode(_pin2, INPUT_PULLUP);
```

The schematic fits `R2` and `R3`, both 10 kΩ, from `IN_A`/`IN_B` to `+3.3V`. The ESP32-S3's
internal pull-up (nominally ~45 kΩ) lands in parallel, giving ≈ 8.2 kΩ. That is a stiffer
pull-up than designed, not a fault, and it slightly *helps* the RC settling discussed next.
Harmless; recorded because it changes the filter time constant and someone measuring edge shapes
will otherwise be puzzled.

### 2. The 2 ms settling delay is about 2.4 time constants, not 5 — **inert, borderline**

Same function:

```cpp
// allow time for a passive R-C filter to charge
// through the pullup resistors, before reading
// the initial state
delayMicroseconds(2000);
```

The comment shows the author knew an RC filter might be present. On this board it is: `C2` and
`C3`, 100 nF, from `IN_A`/`IN_B` to `GND`.

With the parallel pull-up of ≈ 8.2 kΩ, τ ≈ 8.2 kΩ × 100 nF ≈ **0.82 ms**. A 2 000 µs delay is
≈ 2.4 τ, i.e. the node reaches ≈ **91 %** of the rail before the initial quadrature state is
latched. It will read high — 91 % of 3.3 V is 3.0 V, far above V_IH — so the code is correct in
practice. But the margin is 2.4 τ where the conventional figure is 5 τ, and the value is
hard-coded in a library shared across boards with different filter components. **Inert here;
a trap if this Encoder copy is reused with a larger capacitor.**

This is also the first *quantitative* statement about the encoder input filter available
anywhere in this record, and it has a second consequence: the RC corner is
1/(2π · 8.2 kΩ · 100 nF) ≈ **194 Hz**, which is the hardware ceiling on edge rate regardless of
how fast the ISR is.

### 3. The encoder consumes two of the four JTAG pins — **active, by design, undocumented**

`GPIO41` = `MTDI`, `GPIO40` = `MTDO`, as printed on the module footprint's own pin names. Calling
`DinMeter.begin(true)` attaches `CHANGE` interrupts to both. **An external JTAG probe and the
rotary encoder cannot be used at the same time.** Neither the header, the driver, nor the product
documentation says so.

Note also that `GPIO41`/`MTDI` is sampled at reset on ESP32 parts for eFuse-configurable boot
behaviour; on the ESP32-S3 the strapping pins are 0, 3, 45 and 46, so `MTDI` is **not** a strap
here and the 10 kΩ pull-up is safe. Checked rather than assumed.

### 4. `M5DinMeter::begin()` does nothing but forward — **not a defect**

`src/M5DinMeter.cpp:7-19` calls `M5.begin()` then optionally `Encoder.begin()`. There is no
board-specific power-up ordering in this library at all; everything is in M5Unified. So there is
no ordering here to compare against a datasheet — stated explicitly, because "no finding" and
"not checked" are different and only one of them is useful.

### 5. The encoder is polled through an ISR that never reports loss — **inert**

`Encoder::update()` is a 16-state quadrature decoder with `+2`/`-2` cases for "assume pin1 edges
only" — i.e. it *detects* that it missed an intermediate state and guesses a direction rather
than flagging it. On a hand-turned knob behind a 194 Hz RC filter this will not fire. There is no
error counter, so a fast spin degrades silently. Worth knowing; not worth fixing.

## C. Not checked

- **`M5DinMeter-UserDemo`** (also snapshotted) was not audited.
- **`U5` `RTC8563` initialisation against the RTC's register map** was not audited. The RTC is on
  the internal bus (`IN_SDA`/`IN_SCL` → `G11`/`G12`) with `Y2` 32.768 kHz ±20 ppm 12.5 pF and
  `C28`/`C29` 6.0 pF loading capacitors. The 12.5 pF crystal against 6.0 pF fitted loading is the
  obvious thing to examine next — nominal C_L for a 12.5 pF crystal needs roughly 2 × (12.5 − C_stray)
  per leg, which 6.0 pF is in the right region for, but this was **not** worked through and is
  recorded as an open item rather than a result.
