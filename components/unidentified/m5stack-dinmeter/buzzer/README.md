# Unidentified — M5Stack DinMeter buzzer (`LS1`)

- **Category:** electro-magnetic (passive) buzzer / sounder.
- **Manufacturer / part number:** ⚠ **NOT ESTABLISHED.** `LS1` carries a `CO` marker and the
  label `Buzzer` on the schematic, but **no part number and no value**.
- **Retrieved:** 2026-09-04

## 1. What is established

| Property | Value | Evidence |
|---|---|---|
| Designator | `LS1`, 2 pads (`PILS101`, `PILS102`) | DinMeter schematic |
| Label on sheet | `Buzzer` | schematic, (158, 464.1) |
| Drive | **`Q5` SS8050 NPN** low-side, base resistor **`R25` 470 Ω** from net `beep` | schematic |
| Flyback | **`D6` 1N4148WT** across the coil | schematic — *a flyback diode implies an inductive (magnetic) buzzer, not a piezo* |
| Supply | `+5VIN` | schematic |
| Local bulk | `C27` 10 µF | schematic |
| Control GPIO | `beep` → Stamp pad 3 → **ESP32-S3 GPIO3** | schematic; M5Unified |
| Passive, not self-driving | ESP-IDF board support models it as a **LEDC PWM tone source**, not an on/off element | `esp-board-manager` `ledc_buzzer` |
| Default tone config | LEDC channel 1, timer 1, **4 kHz**, 10-bit resolution, low-speed mode | `esp-board-manager` |
| M5Unified config | `spk_cfg.pin_data_out = GPIO_NUM_3`, `spk_cfg.buzzer = true`, `magnification = 48` | `M5Unified/src/M5Unified.cpp:2921-2928` |
| Frequencies used in vendor examples | 4 000 Hz, 8 000 Hz, 10 000 Hz | `M5DinMeter/examples/Basic/{buzzer,button,encoder}.ino` |

The `SS8050` transistor is annotated on the sheet with `Y1` immediately to its right — that is
the SOT-23 **marking code** for an SS8050, not a separate designator. See
[`devices/m5stack/dinmeter/pinouts-and-buses.md` §6](../../../../devices/m5stack/dinmeter/pinouts-and-buses.md#6-reference-designator-census-and-three-that-do-not-resolve).

## 2. What is not established

Resonant frequency, sound-pressure level, rated voltage, coil resistance, current draw, and
package/footprint dimensions. Nothing about the acoustic behaviour is published.

**What would resolve it:** a teardown photograph of `LS1`'s top marking, or an M5Stack BOM.

## 3. Practical notes

- It is **passive**: you must supply a square wave. Writing a DC level makes it click once.
- Being magnetic with a flyback diode, it will have a pronounced resonance — the vendor's use
  of 4 kHz and 8–10 kHz in different examples suggests a broad usable range, but the loudest
  frequency is unknown without measurement.
- It is driven from **`+5VIN`**, so it is louder on USB/DC than on battery-only operation where
  the rail comes from the boost.
- GPIO3 is an ESP32-S3 **strapping-adjacent** pin (JTAG source select on some parts); it is
  driven as a plain LEDC output here with no reported issue.

## 4. Artifacts

**None.** Establishing evidence: the device schematic and
[`devices/m5stack/dinmeter/artifacts/source-snapshots/dinmeter-board_peripherals.yaml`](../../../../devices/m5stack/dinmeter/artifacts/source-snapshots/dinmeter-board_peripherals.yaml).

---

## Used By

### M5Stack DinMeter (K134) and DinMeter v1.1 (K134-V11)

`LS1`. Identical on both revisions.
→ [`devices/m5stack/dinmeter/features/buzzer.md`](../../../../devices/m5stack/dinmeter/features/buzzer.md)

---

## Update — 2026-09-07: drive circuit re-traced. **`C27` is in series with the base, not a bulk capacitor.**

Appended, not substituted. The table above records *"Local bulk | `C27` 10 µF"*. Net tracing
shows `C27` is **in the base-drive path**, between `R25` and the transistor — an AC coupling
capacitor, not decoupling. Method:
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md).

### The evidence

All five drive-path pin tokens share **y = 491.37** and run strictly left-to-right in x:

```
PIR2501 @  45.00, 491.37   R25 pin 1   <- net `beep`
PIR2502 @  67.00, 491.37   R25 pin 2
PIC2701 @  74.00, 491.37   C27 pin 1
PIC2702 @  89.00, 491.37   C27 pin 2
PIQ501  @ 121.00, 491.37   Q5 base
```

A series chain on one horizontal wire. A decoupling capacitor would have one pin on the rail and
one on ground; both of `C27`'s pins are on the signal path. Confirmed by a 300 dpi render, which
shows the capacitor symbol drawn *in* the wire between `R25` and the base node.

`D7` `1N4148WT` hangs off the base node at x = 99.50 — cathode `PID702` @ y 502.57 (up, to the
base), anode `PID701` @ y 523.57 (down, to `GND` @ y 553.60): a **negative-excursion clamp**,
which is exactly what an AC-coupled base needs.

```
beep ── R25 470Ω ── C27 10µF ──┬── Q5 base (SS8050 NPN)
                               └── D7 (cathode up) ── GND
```

### What this changes

- **The row "Local bulk | `C27` 10 µF" is superseded.** `C27` is a coupling capacitor. There is
  no local bulk capacitor identified on the `+5VIN` node in this branch.
- **The transducer cannot be driven with a DC level.** A steady GPIO high produces one brief
  pulse and then nothing. It *must* be driven with a waveform. The record's existing statement
  that the part is passive and modelled as a PWM tone source is therefore **confirmed by the
  hardware**, not merely by how the library treats it.
- **High-pass corner ≈ 34 Hz** (1 / 2π · 470 Ω · 10 µF), so the whole audio band passes and the
  coupling imposes no practical restriction on tone selection.

### Re-confirmed unchanged

| Property | Value | Token |
|---|---|---|
| `LS1`, 2 pads | value field `Buzzer` | `PILS101` @ 142.50, 448.37 · `PILS102` @ 142.50, 455.37 |
| `D6` `1N4148WT` anti-parallel across `LS1` | flyback | `PID602` @ 99.50, 426.57 · `PID601` @ 99.50, 448.57 |
| `Q5` `SS8050` low-side NPN | collector/emitter | `PIQ503` @ 135.50, 476.77 · `PIQ502` @ 135.50, 505.77 → `GND` |
| `R25` 470 Ω | base resistor | above |
| Supply | `+5VIN` | — |
| Control GPIO | `beep` → module pad 3 → `G3` | `NLbeep` @ 29.50, 488.20 |

**The flyback diode remains the strongest evidence for the category.** `D6` is drawn
anti-parallel across `LS1`; a catch diode is only needed for an inductive load. This supports the
"electro-magnetic (passive) buzzer" categorisation at the head of this record — a piezo element
would not need one.

### Still not established

Resonant frequency, sound-pressure level, rated voltage, coil resistance, current draw,
manufacturer and part number — **all unchanged.** The schematic gives topology, not identity.
This record stays open.
