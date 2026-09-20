# Unidentified — M5Stack DinMeter rotary encoder ("the orange knob")

- **Category:** incremental quadrature rotary encoder with integrated push switch.
- **Manufacturer / part number:** ⚠ **NOT ESTABLISHED.** No part number, manufacturer or series
  is printed on the schematic, stated in the documentation, or listed in the datasheets section
  of either DinMeter product page.
- **Scope:** device-scoped, per the convention for unidentified parts, so it cannot collide
  with other unknown encoders.
- **Retrieved:** 2026-09-04

This is the component that defines the product's identity — the bright orange knurled knob —
and it is the one M5Stack documents least.

---

## 1. What *is* established

All from the DinMeter schematic (`K134_DIN_Meter_v1.0-schematic.pdf`, parsed marker layer),
which is shared byte-for-byte by v1.0 and v1.1.

| Property | Value |
|---|---|
| Not soldered to the main board | It attaches through a **7-pad connector `J5`** (`PIJ501`…`PIJ505` recovered, pads 6–7 present on the symbol), labelled **`Rotary encode`** on the sheet |
| Channel A | `IN_A` → Stamp pad 23 → **ESP32-S3 GPIO41**, pulled up by `R2` 10 kΩ to `+3.3V` |
| Channel B | `IN_B` → Stamp pad 21 → **ESP32-S3 GPIO40**, pulled up by `R3` 10 kΩ to `+3.3V` |
| Common | `GND` |
| Push switch | separate contacts labelled `b1`/`b2` on the same connector block, net `BTN` → `WAKE` → Stamp pad 25 → **GPIO42**, pulled up by `R1` 10 kΩ, debounced by `C1` 100 nF |
| Switch also wakes the board | `BTN` feeds the power-latch wake path through `D4` (B5819WT) |
| Detent behaviour | **not stated anywhere.** Counts-per-revolution, detents-per-revolution and whether detents align to full quadrature cycles are all unknown |
| Shaft, knob, torque, life | **not stated** |
| Colour | orange knob cap (product photography) — whether the cap is part of the encoder or a separate moulding is **not established** |

## 2. What the software assumes

Two independent implementations agree that it is a **standard 2-channel quadrature encoder with
4 counts per detent**:

| Source | Treatment |
|---|---|
| `m5stack/M5DinMeter` | A vendored copy of **PJRC's `Encoder` library** (Paul Stoffregen, MIT, v1.2), constructed as `ENCODER(41, 40)` — `src/M5DinMeter.h:8-9,33`. Full x4 decoding, interrupt-driven |
| `espressif/esp-board-manager` | **PCNT** unit, two channels, each pin edge on one channel and level on the other, `max_glitch_ns: 1000`, limits ±1000, `accum_count: true`. Its comment: *"Both channels are counted so one detent is four counts and the direction is unambiguous."* |

So: x4 decoding, 1 kHz-ish glitch filtering is adequate, and no external debounce hardware
beyond the 10 kΩ pull-ups is fitted.

## 3. Why identification matters, and what would resolve it

It matters for: sourcing a replacement after mechanical wear (this is the part that will fail
first in a panel instrument), knowing the rated rotational life, knowing the switch's rated
operations, and knowing whether the detent count matches the electrical cycle count.

**Candidate families were deliberately NOT recorded here.** This repository holds an
[Alps Alpine `SSCM110100`](../../../alps-alpine/sscm110100/README.md) encoder record from
another device; the DinMeter's encoder is **not** asserted to be that part or any relative of
it. Nothing in the DinMeter's evidence names Alps.

**What would settle it:**
1. A teardown photograph showing the encoder body's manufacturer marking.
2. An M5Stack BOM or a reply from `support@m5stack.com`.
3. The `J5` mating connector part, which would at least narrow the encoder module family.

Until then this record stays `unidentified`.

## 4. Artifacts

**None.** Establishing evidence is the device schematic and the extracted layout:
- [`devices/m5stack/dinmeter/artifacts/schematic/K134_DIN_Meter_v1.0-schematic.pdf`](../../../../devices/m5stack/dinmeter/artifacts/schematic/K134_DIN_Meter_v1.0-schematic.pdf)
- [`devices/m5stack/dinmeter/artifacts/source-snapshots/dinmeter-board_peripherals.yaml`](../../../../devices/m5stack/dinmeter/artifacts/source-snapshots/dinmeter-board_peripherals.yaml)

---

## Used By

### M5Stack DinMeter (K134) and DinMeter v1.1 (K134-V11)

The primary input device. Quadrature on GPIO41 (A) / GPIO40 (B); push switch on GPIO42, which
doubles as the board's wake key. Identical on both revisions.

→ [`devices/m5stack/dinmeter/features/rotary-encoder-and-buttons.md`](../../../../devices/m5stack/dinmeter/features/rotary-encoder-and-buttons.md)

---

## Update — 2026-09-07: `J5` has **five** pins, not seven; topology now established

Appended, not substituted. The table above states *"a **7-pad connector `J5`**
(`PIJ501`…`PIJ505` recovered, pads 6–7 present on the symbol)"*. **The symbol has five pins.**
Method: [`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md).

```
python3 trace.py grep bbox/<dinmeter>.xhtml '^PIJ5'
  p1 x=445.50 y=361.91  PIJ501      p1 x=503.00 y=361.91  PIJ502
  p1 x=459.50 y=389.77  PIJ503      p1 x=474.50 y=389.77  PIJ504
  p1 x=488.50 y=389.77  PIJ505
```

There is no `PIJ506` or `PIJ507` anywhere in the document. A 300 dpi render of the symbol shows
five pins and no more. The earlier "pads 6–7 present" reading is withdrawn.

### What the render adds that the marker layer alone could not

The five pins are **named on the symbol**, and the names settle the topology:

| Pin | Symbol name | Net | Termination |
|---|---|---|---|
| 1 | `b1` | `BTN` @ 430, 359.2 | push switch, one side |
| 2 | `b2` | `GND` @ 533, 362.5 | push switch, other side |
| 3 | **`A`** | `IN_A` @ 457, 419.9 | `R2` 10 kΩ to `+3.3V`, `C2` 100 nF to `GND` |
| 4 | **`COM`** | `GND` @ 475, 416.7 | — |
| 5 | **`B`** | `IN_B` @ 486, 419.9 | `R3` 10 kΩ to `+3.3V`, `C3` 100 nF to `GND` |

So it is a **standard 3-terminal incremental quadrature encoder (A / COM / B) with COM
grounded**, plus an integrated 2-terminal momentary push switch — a single 5-terminal part, not a
7-pad connector carrying two separate devices. The switch contacts are drawn *inside the same
symbol*, above the A/COM/B group.

Everything the existing table says about the GPIO mapping, the pull-ups and the wake path is
**confirmed unchanged**: `IN_A` → pad 23 → GPIO41, `IN_B` → pad 21 → GPIO40, `BTN` → `WAKE` →
pad 25 → GPIO42.

### Two things this makes newly sayable

1. **The encoder sits on the JTAG data pins.** The module footprint prints the pad names itself:
   pad 23 is `G41/MTDI` and pad 21 is `G40/MTDO`. An external JTAG probe and the encoder cannot
   be used simultaneously. Not stated in the header, the driver, or M5Stack's documentation.
2. **The input filter has a measurable ceiling.** With the 10 kΩ external pull-up in parallel
   with the ESP32-S3 internal one that `Encoder::begin()` also enables (≈ 8.2 kΩ) and `C2`/`C3`
   at 100 nF, τ ≈ 0.82 ms and the corner is ≈ **194 Hz**. That is the hardware limit on edge
   rate, independent of firmware. See
   [`devices/m5stack/dinmeter/driver-vs-document-audit.md`](../../../../devices/m5stack/dinmeter/driver-vs-document-audit.md).

### Still not established

Manufacturer, part number, series, counts-per-revolution, detents-per-revolution, detent
alignment, shaft type, torque and rated life — **all unchanged from the list above.** The
schematic names none of them, and pin-count alone does not identify a part. This record stays
open.
