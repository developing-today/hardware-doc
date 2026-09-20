# DinMeter v1.1 — pinouts and buses

**The GPIO map is identical to the DinMeter v1.0's, in every respect.**
→ **[`../dinmeter/pinouts-and-buses.md`](../dinmeter/pinouts-and-buses.md)** is the full,
schematic-derived reference: all 31 Stamp pads, every bus, the complete power tree, the
designator census and the Grove wire-colour conflict. This page records only what is
v1.1-specific, and the evidence that the rest genuinely is unchanged.

---

## 1. Why one pinout document serves both

| Evidence | Finding |
|---|---|
| Published schematic | The file linked from the v1.1 page (`.../1211/K134-V11_DIN_Meter_v1.0_2025_11_25_17_15_58.pdf`) is **byte-identical** to the v1.0 file (`.../500/DIN_Meter_v1.0.pdf`), SHA-256 `03ec3353…6e4c070`. Its own filename contains `_v1.0_` |
| Published STL | `DinMeter_v1.1.stl` is **byte-identical** to `DinMeter.stl`, SHA-256 `90f04d6a…` |
| Dimension drawing | **The same URL** is linked from both pages |
| Vendor PinMap | Identical assignments, signal for signal (compared below) |
| M5Unified | **One** board enum, `board_M5DinMeter`, serves both. There is no v1.1 variant at master `8530f5377d782e4a25a6c482de2e71c3f75ca8eb` (2026-09-04) |

So the carrier's documentation has not been revised. That does **not** prove the PCB is
unchanged — it proves the documentation is. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

## 2. The v1.1 PinMap, compared line by line

Both product pages' PinMap tables, side by side. **Every assignment matches.**

| Block | v1.0 page | v1.1 page | Same? |
|---|---|---|---|
| RTC SCL | G12 | G12 | ✔ |
| RTC SDA | G11 | G11 | ✔ |
| ENCODER B | G40 | G40 | ✔ |
| ENCODER A | G41 | G41 | ✔ |
| BEEP | G3 | G3 | ✔ |
| BTN (WAKE) | G42 | G42 | ✔ |
| Display CS | G7 | G7 | ✔ |
| Display SCK | G6 | G6 | ✔ |
| Display RS (D/C) | G4 | G4 | ✔ |
| Display MOSI | G5 | G5 | ✔ |
| Display RESET | G8 | G8 | ✔ |
| Display BL | G9 | G9 | ✔ |
| PORT.A | G13 / G15 | G13 / G15 | ✔ |
| PORT.B | G2 / G1 | G2 / G1 | ✔ |
| HOLD | GPIO46 | GPIO46 | ✔ |
| **Section heading** | `ST7789V2` | **`ST7789P3`** | ✘ — the *only* difference in the whole table |

## 3. What is v1.1-specific

### 3.1 GPIO38 — new, internal to the module, and required for the RGB LED

| Pin | v1.0 (Stamp-S3) | v1.1 (Stamp-S3A) |
|---|---|---|
| **GPIO38** (`DISP_BL`, inside the module) | Gates the Stamp's rear LCD-FPC backlight rail **only**. Unused on the DinMeter carrier | Gates `BL_3V3`, which now also supplies the **WS2812B-2020 RGB LED**. **Must be driven high** before the LED will light |

GPIO38 is **not** one of the Stamp's 23 broken-out IOs and appears nowhere on the DinMeter
carrier schematic. It is entirely internal, so there is no conflict — on this board it has
exactly one job.

Evidence and code: [`stamp-s3-to-s3a-delta.md` §3](stamp-s3-to-s3a-delta.md#3-change-1--the-rgb-led-is-no-longer-always-powered-the-only-source-compatibility-break)
and [`../dinmeter/features/rgb-led.md`](../dinmeter/features/rgb-led.md).

### 3.2 The display controller name

`ST7789V2` → `ST7789P3`. Same six pins, same 135 × 240, same driver path, same GRAM gap
(+52, +40) and same `INVON` requirement. **No datasheet exists for the ST7789P3** — see
[`components/sitronix/st7789p3`](../../../components/sitronix/st7789p3/README.md).

### 3.3 Everything internal to the module that changed

Not visible from the carrier, but it is what you are actually buying:

| Item | v1.0 | v1.1 |
|---|---|---|
| Module DC-DC | `M2` MUN3CAD01-SC, **1 A**, integrated inductor | `U4` unidentified 8-ball buck, **0.6 A**, external `L4` 2.2 µH |
| Module load switch `U2` | SGM2578 (alt `WS4622C-4/TR`) | **AW35122FDR** |
| Antenna match | 3 elements, `ANT1` = `PROANT440` | 6 positions + an `ESP_EN` filter, `ANT1` **unlabelled** |
| Rear FPC pin numbering | `J1` pin 1 = `VIN_5V` | `J1` pin **12** = `VIN_5V` (**unresolved** whether physical) |

Full treatment: [`stamp-s3-to-s3a-delta.md`](stamp-s3-to-s3a-delta.md).

## 4. Quick reference — the pins you actually use

Reproduced here so you do not have to open two documents for the common case. **Authoritative
version, with per-pin evidence, is in
[`../dinmeter/pinouts-and-buses.md`](../dinmeter/pinouts-and-buses.md) §2.**

| Function | GPIO |
|---|---|
| Display: MOSI / SCLK / CS / D-C / RESET / backlight | 5 / 6 / 7 / 4 / 8 / 9 |
| Encoder A / B | 41 / 40 |
| Encoder push-button (also WAKE) | 42 |
| Buzzer | 3 |
| RTC I²C SDA / SCL (**internal bus**) | 11 / 12 |
| PORT.A I²C SDA / SCL (**external bus**) | 13 / 15 |
| PORT.B signals | 1 / 2 |
| Battery ADC (divider ÷2) | 10 |
| **Power hold — raise this in `setup()`** | **46** |
| Stamp `G0` button / boot strap | 0 |
| **RGB LED data** (internal) | 21 |
| **RGB LED power enable (internal) — v1.1 only** | **38** |
| Free, unlabelled on the schematic | 43, 44 (UART0) |
| ⚠ Advertised free but **not** free — latch network fitted | 14, 39 |

## Related

[`../dinmeter/pinouts-and-buses.md`](../dinmeter/pinouts-and-buses.md) ·
[`../dinmeter/resources-and-conflicts.md`](../dinmeter/resources-and-conflicts.md) ·
[`stamp-s3-to-s3a-delta.md`](stamp-s3-to-s3a-delta.md) ·
[`components/m5stack/stamp-s3a`](../../../components/m5stack/stamp-s3a/README.md)
