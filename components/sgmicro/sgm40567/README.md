# SG Micro SGM40567

- **Part as fitted:** `SGM40567-4.2XG/TR`
- **Category:** single-cell Li-ion **linear battery charger**, fixed 4.2 V float
- **Package:** WLCSP, footprint `WLCSP-0.4-0.92X1.16X0.4MM` (0.92 × 1.16 × 0.4 mm — 6-ball)
- **Retrieved:** 2026-08-24
- **Evidence:** KiCad BOM + PCB netlist of the XIAO ESP32S3 Sense v1.5 design package, plus the designer's own annotation on the schematic sheet. **SG Micro datasheet not obtained in this pass.**

## Part number decode

`SGM40567` family · **`-4.2`** = 4.2 V float voltage (standard single-cell Li-ion) · `XG` package code · `/TR` tape-and-reel.

## Pinout as wired

| Ball | Signal | Connection on the XIAO |
|---|---|---|
| A1 | `BAT` | `VBAT` — battery pads, C26 1 µF |
| A2 | `VIN` | `VBUS` — USB 5 V, C25 1 µF |
| B1 | `IREF` | **R10 = 220 kΩ to GND** — programs charge current |
| B2 | `NCHG` | open-drain status → red charge LED via R11 10 kΩ |
| C1 | (with R10 network) | current-set node |
| C2 | `GND` | ground |

## Charge current is set by R10

The schematic carries the designer's annotation:

> `ICharge = 24000 / 220K = 110mA`

with **R10 = 220 kΩ** confirmed in the BOM. The implied relationship is **I_charge (mA) ≈ 24000 / R10(Ω)**, i.e. a 24,000 A·Ω current-set constant.

**Seeed's wiki instead states 100 mA fast / 0.9 mA trickle.** The two disagree by ~10 %; the schematic's arithmetic is self-consistent, so 110 mA is likely the design value and 100 mA a rounded figure. Unresolved — see [../../devices/seeed-studio/xiao-esp32s3-sense/gaps-and-conflicts.md](../../../devices/seeed-studio/xiao-esp32s3-sense/gaps-and-conflicts.md#3-battery-charge-current-110-ma-schematic-vs-100-ma-wiki).

**Modification.** Charge current is therefore adjustable by changing R10 — e.g. 110 kΩ would imply ~218 mA, useful for larger cells where ~110 mA is slow. Two cautions: it is a **linear** charger, so the extra power becomes heat in a 0.92 × 1.16 mm WLCSP on a 21 mm board; and this is **inference from a schematic annotation, untested**, not a sanctioned procedure.

## Limits and caveats

- Linear topology — dissipation ≈ (V_BUS − V_BAT) × I_charge. At 5 V in, 3.7 V battery, 110 mA that is ~140 mW in a sub-millimetre package.
- **No battery voltage sense is provided to the SoC.** The `VBAT` net has only four members (battery pad, C26, Q1, and this IC) — there is no divider to any ADC. See [../../devices/seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md](../../../devices/seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md#82-there-is-no-battery-voltage-sense--confirmed-by-the-vendor).
- No published thermal-regulation, NTC or safety-timer behaviour established here — obtain the SG Micro datasheet.

## Used by

### Seeed Studio XIAO ESP32S3 Sense

Reference designator **U4**. Charges a single Li-ion cell soldered to the bottom-side `BAT+`/`BAT−` pads from USB `VBUS`.

**Charge LED behaviour** (`CHG0`, red, driven by `NCHG`): on for ~30 s when USB is connected with no battery; **flashing while charging**; off when full. The "flashing = charging" convention is unusual and a common source of confusion.

**Battery polarity is not protected.** Seeed specifies the **negative terminal nearest the USB connector**, positive away from it. There is no reverse-polarity protection on those pads.

Power tree: [../../devices/seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md](../../../devices/seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md#8-power-tree)

## Related
- [SGM6029](../sgm6029/README.md) — the 3V3 buck-boost downstream
- [ESP32-S3R8](../../espressif/esp32-s3r8/README.md)
