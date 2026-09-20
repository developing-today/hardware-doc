# M5Stack DinMeter v1.1 (SKU K134-V11)

> **Product ID** `K134-V11` · **Announced** 2026-01-30 · **Status** current, in stock at
> USD 24.50 (2026-09-04) · **Research retrieval date** 2026-09-04

**This is a scoped revision record, not a duplicate.** The DinMeter v1.1 is the original
[DinMeter (K134)](../dinmeter/README.md) carrier board with a different core module soldered on
it. Everything the two share — pinouts, buses, power tree, feature guides, development
workflow, factory firmware, mechanical envelope — lives in the K134 record and is **not
repeated here**. This document covers only what is actually different, and the evidence for why
the list is that short.

---

## Why not a second full record

M5Stack publishes the following under v1.1 names:

| Asset | v1.1 URL / path | SHA-256 | Same as v1.0? |
|---|---|---|---|
| Schematic PDF | `m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1211/K134-V11_DIN_Meter_v1.0_2025_11_25_17_15_58.pdf` | `03ec335396e4f527119f89f697fca9887505dc1b28077871b2fb361ba6e4c070` | **byte-identical** |
| Structure model | `m5stack/M5_Hardware` → `Products/K134-V11_DinMeter_v1.1/Structures/DinMeter_v1.1.stl` | `90f04d6a0ae2cbb6f888065382da46ab1d699188ccebf1510963cc4aef00fbf7` | **byte-identical** |
| Dimension drawing | `.../1211/K134-din_meter_asm_v1.pdf` | `db42c8a995b6d0bf…` | **same file, same URL** as v1.0 |
| GPIO PinMap | v1.1 doc page | — | **identical assignments** |

Note the v1.1 schematic's own filename: `K134-V11_DIN_Meter_**v1.0**_2025_11_25…`. Even the
name says v1.0.

So the carrier PCB documentation **has not been revised**. Writing a second full record would
require asserting board-level differences that no published document supports. See
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) for what that does and does not license us to
conclude.

---

## The change

| | DinMeter (K134) | DinMeter v1.1 (K134-V11) |
|---|---|---|
| Core module | [**Stamp-S3**](../../../components/m5stack/stamp-s3/README.md) (`S007`) | [**Stamp-S3A**](../../../components/m5stack/stamp-s3a/README.md) (`S007-V033`) |
| Display controller (per docs) | **ST7789V2** | **ST7789P3** |
| Package size | 136.0 × 93.0 × 23.0 mm | 136.0 × 95.0 × 24.0 mm |
| Gross weight | 47.0 g | 44.9 g |
| Bundle | adhesive tape, 250 mAh cell, sticker, DC-JACK terminal, back bracket | 250 mAh cell, **2.54-2P terminal**, **plastic back clip**, adhesive tape, **pin sticker** |
| Everything electrical | — | **unchanged** |

The vendor's own "Product Comparison" table on the v1.1 page has exactly **one** row:
*Main Controller — Stamp-S3A vs Stamp-S3*. It does not mention the display controller.

### 1. Stamp-S3 → Stamp-S3A

Fully documented, from both schematics, at
[`components/m5stack/stamp-s3a/README.md`](../../../components/m5stack/stamp-s3a/README.md).
Summary of what a DinMeter owner actually experiences:

| Aspect | Effect on DinMeter v1.1 |
|---|---|
| **Sleep current** | `VIN_5V` sleep drops 310.89 µA → **6.84 µA** (vendor figures, method unstated). The most useful change for a battery-backed panel meter |
| **Standby current** | 33.5 mA → **25.5 mA** |
| **RGB LED** | ⚠ **Requires `GPIO38 = HIGH` before it will light.** See below |
| **Antenna** | Rebuilt matching network; vendor claims better reception, publishes no figure |
| **Regulator** | µPOL module → discrete buck + external 2.2 µH inductor |
| **GPIO map** | **Unchanged** |
| **PSRAM / flash** | **Unchanged** — ESP32-S3FN8, 8 MB flash, no PSRAM, on both |
| **Firmware source compatibility** | **Compatible**, except RGB LED |

> #### ⚠ The RGB LED will not light with stock M5Unified
>
> On Stamp-S3A the WS2812B-2020's supply comes from `BL_3V3`, gated by an AW35122FDR load switch
> whose enable is ESP32-S3 **GPIO38**. On Stamp-S3 the LED was on the always-on `VDD_3V3`.
>
> M5Unified (master `8530f5377d782e4a25a6c482de2e71c3f75ca8eb`, 2026-09-04) maps
> `board_M5DinMeter → GPIO_NUM_21` for the RGB LED (`src/M5Unified.cpp:246`) and contains **no
> GPIO38 enable step for any board**. There is no `board_M5DinMeter_v11` and no
> `board_M5StampS3A` enum. A v1.1 unit therefore identifies as `board_M5DinMeter` and the LED
> path is missing its power-enable.
>
> **Status: `inferred` — predicted from vendor documentation + schematic + source read. Not
> reproduced on hardware.** Workaround (`not-tested`):
> ```cpp
> pinMode(38, OUTPUT); digitalWrite(38, HIGH); delay(1);   // then drive GPIO21 as usual
> ```

### 2. ST7789V2 → ST7789P3

| Source | v1.0 | v1.1 |
|---|---|---|
| Features list | "ST7789v2 screen" | "**ST7789P3** display" |
| Specification row *Display Driver* | `ST7789V2` | `ST7789P3` |
| PinMap section heading | `ST7789V2` | `ST7789P3` |
| *Datasheets* section | links `ST7789V2_SPEC_V1.0.pdf` | **no display datasheet at all** |
| Product Comparison table | — | **does not mention the display** |

The change is real in the documentation and consistent across three places on the page. But
M5Stack **withdrew the datasheet link** rather than replacing it, publishes no ST7789P3
document, and did not list the display in its own comparison table. The pin assignments
(CS G7, SCK G6, RS G4, MOSI G5, RESET G8, BL G9) and the resolution (135 × 240) are identical.

Practically: both are Sitronix ST7789-family SPI TFT controllers with the same command set for
everything an application does. M5GFX/LovyanGFX drives both through its ST7789 panel class;
M5Unified's `board_M5DinMeter` display path is unchanged. **No API difference is expected**, and
none was found. → [`components/sitronix/st7789p3/README.md`](../../../components/sitronix/st7789p3/README.md)

### 3. Packaging and bundle

The v1.1 box is 2 mm wider and 1 mm taller but 2.1 g lighter, and the accessory list changed:
the "DC-JACK terminal input (6-36V)" became a "2.54-2P Terminal", the "back bracket" became a
"plastic back clip", and a "pin sticker" replaced the "silk-screened sticker". Cosmetic/logistics
changes with no electrical meaning. **[DOC]**

---

## Identity and variants

| Property | Value | Evidence |
|---|---|---|
| Marketed name | **DinMeter v1.1** | docs page title, 2026-09-04 |
| SKU | **`K134-V11`** | docs page header; shop variant `sku: "K134-V11"` |
| Documentation | <https://docs.m5stack.com/en/core/DinMeter_v1.1> (HTTP 200) | verified 2026-09-04 |
| Shop listing | <https://shop.m5stack.com/products/m5stack-din-meter-v1-1-with-m5stamps3a> | HTTP 200 |
| Shop product id / variant id | `9014041182465` / `47570426593537` | `…/…​.js` JSON |
| Created / published | `2026-01-30T10:02:16+08:00` / `2026-01-30T12:30:47+08:00` | shop JSON |
| Tags | `ESP32-S3`, `STAMP` | shop JSON |
| Shipping weight | 70 g | shop JSON |
| Price | **USD 24.50**, in stock | shop JSON, 2026-09-04 |
| Regional variants | none found | — |

---

## Key specifications (v1.1 page, where they differ from v1.0)

Identical to v1.0 except as noted:

| Specification | v1.1 value | Same as v1.0? |
|---|---|---|
| SoC | ESP32-S3FN8 @ 240 MHz | ✔ |
| Flash | 8 MB | ✔ |
| PSRAM | none | ✔ |
| Display driver | **ST7789P3** | ✘ (was ST7789V2) |
| Resolution | 135 × 240 | ✔ |
| DC input | 6 – 36 V | ✔ |
| Charging current | 100 mA | ✔ |
| Grove load | PORT.A 5 V @ 220 mA, PORT.B 5 V @ 220 mA | ✔ |
| Standby current (battery) | DC 4.2 V @ 38.4 µA | ✔ — **note:** unchanged despite the module's much lower sleep current, because the board latches the battery *off* rather than sleeping |
| Battery socket | 1.25 mm-2P | ✔ |
| Operating temp | 0 – 40 °C | ✔ |
| Product size / weight | 53.0 × 30.0 × 32.0 mm / 17.8 g | ✔ |
| Package size / gross | 136.0 × 95.0 × 24.0 mm / 44.9 g | ✘ |

The unchanged 38.4 µA standby figure is worth pausing on: it is quoted identically on both
pages, which is consistent with it being a *board* measurement dominated by the latch circuit
rather than by the module. **[INF]**

---

## New in the v1.1 documentation

The v1.1 page carries three "Learn" sections the v1.0 page does not, all of which are useful
and all of which apply to v1.0 too except the last:

- **Power On/Off** — reworded but equivalent: wake by WAKE button or RTC IRQ; firmware must set
  HOLD (GPIO46) high during init; power off with RST or `GPIO46 = 0`.
- **Download Mode** — hold `G0` on the Stamp-S3A before power-up.
- **RGB LED Power Supply** — **new and v1.1-specific.** The GPIO38 requirement, quoted in full
  in [`components/m5stack/stamp-s3a/README.md` §3](../../../components/m5stack/stamp-s3a/README.md#3-change-1--the-rgb-led-is-no-longer-always-powered-firmware-visible).

---

## Everything else

| Topic | Where |
|---|---|
| Full GPIO map, buses, power tree, designator census | [`../dinmeter/pinouts-and-buses.md`](../dinmeter/pinouts-and-buses.md) |
| Arduino / ESP-IDF / UiFlow2 / MicroPython | [`../dinmeter/development.md`](../dinmeter/development.md) |
| Feature guides (encoder, display, RTC, buzzer, power, Grove, Wi-Fi/BLE, mounting, RGB) | [`../dinmeter/features/`](../dinmeter/features/README.md) |
| Factory firmware and restore | [`../dinmeter/factory-firmware.md`](../dinmeter/factory-firmware.md) |
| Projects and community | [`../dinmeter/projects-and-community.md`](../dinmeter/projects-and-community.md) |
| Comparisons (Waveshare knob, M5Dial, DIY) | [`../dinmeter/comparisons-and-recommendations.md`](../dinmeter/comparisons-and-recommendations.md) |
| Coverage, resources/conflicts, compatibility | [`../dinmeter/coverage.md`](../dinmeter/coverage.md), [`../dinmeter/resources-and-conflicts.md`](../dinmeter/resources-and-conflicts.md), [`../dinmeter/compatibility-and-status.md`](../dinmeter/compatibility-and-status.md) |
| Research log, commands, sources | [`../dinmeter/research-log.md`](../dinmeter/research-log.md), [`../dinmeter/commands.md`](../dinmeter/commands.md), [`../dinmeter/sources.md`](../dinmeter/sources.md) |
| Media provenance | [`../dinmeter/media.md`](../dinmeter/media.md) |
| **v1.1-specific conflicts** | [`gaps-and-conflicts.md`](gaps-and-conflicts.md) |
| **v1.1-specific pricing** | [`market-and-pricing.md`](market-and-pricing.md) |
| **v1.1-specific sources** | [`sources.md`](sources.md) |

---

## Artifact layout

```
devices/m5stack/dinmeter-v1.1/artifacts/
├── schematic/
│   └── K134-V11_DIN_Meter_v1.0_2025_11_25_17_15_58-schematic.pdf   433 658 B  03ec3353…
│       ^ deliberately retained despite being byte-identical to the v1.0 file:
│         the duplication under two URLs and two filenames IS the finding
├── mechanical/
│   └── DinMeter_v1.1.stl                                           573 284 B  90f04d6a…
│       ^ likewise byte-identical to DinMeter.stl
└── docs/
    ├── docs-en-core-DinMeter_v1.1.pdf → archive/…               11 261 000 B  617a9ea8…
    ├── docs-en-core-DinMeter_v1.1.pdf.ARCHIVED.md                 placeholder
    └── docs-en-core-DinMeter_v1.1.txt                               6 438 B   page text
```

**Intentional duplication, recorded:** ~1.0 MB is byte-identical to files under
`devices/m5stack/dinmeter/artifacts/`. Deduplicating would destroy the evidence that M5Stack
published the same bytes twice. The documentation PDF, by contrast, is genuinely different
content.

## Components fitted (deltas only)

| Function | v1.1 part | Record |
|---|---|---|
| Core module | **Stamp-S3A** `S007-V033` | [`components/m5stack/stamp-s3a`](../../../components/m5stack/stamp-s3a/README.md) |
| Display controller | **ST7789P3** | [`components/sitronix/st7789p3`](../../../components/sitronix/st7789p3/README.md) |

All other fitted parts are as listed in the
[K134 key-specification table](../dinmeter/README.md#key-specifications) — same schematic, same
BOM as far as anything published shows.
