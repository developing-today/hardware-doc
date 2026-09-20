# Sitronix ST7789V

- **Category:** single-chip TFT-LCD controller/driver with on-chip GRAM — **240 RGB × 320 dot**,
  262 k colours; 8/9/16/18-bit MCU parallel (Intel 8080 type I/II), 3/4-wire SPI, and RGB
  interfaces.
- **Manufacturer:** Sitronix Technology Corporation (Taiwan).
- **Retrieved:** 2026-09-07
- **Sibling records already in this repository:** [`st7789v2`](../st7789v2/README.md) ·
  [`st7789vw`](../st7789vw/README.md) · [`st7789p3`](../st7789p3/README.md) ·
  [`st7701s`](../st7701s/README.md) · [`st77916`](../st77916/README.md) ·
  [`st7796s`](../st7796s/README.md)

The display controller of the **LilyGO T-Display-S3** and **T-Display-S3 Touch**, driven over
an **8-bit Intel-8080 parallel** bus — an unusual choice that is the main reason those boards
redraw as fast as they do.

> **Which ST7789 is this?** Sitronix ships ST7789V, V2, VW and P3 as distinct documents with
> distinct part numbers. This record is for the **plain `V`**, because that is the exact string
> on the datasheet LilyGO ships (`ST7789V_SPEC_V1.4.pdf`) inside the T-Display-S3 board
> repository. Do **not** assume the V2 or VW register set applies unchanged; see
> [§4](#4-do-not-substitute-the-family-members-blindly).

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **ST7789V** | filename and content of the vendor-mirrored datasheet |
| Datasheet version | **V1.4** | filename `ST7789V_SPEC_V1.4.pdf`; **the cover page was not independently verified** — see [§5](#5-what-was-not-verified) |
| Resolution | 240 RGB × 320 | family specification |
| Local artifact | [`artifacts/st7789v-spec-v1.4-lilygo-mirror.pdf`](artifacts/st7789v-spec-v1.4-lilygo-mirror.pdf) — 3 198 803 B, SHA-256 `94c959b15fea4a8dc9381e4c4fa94e51037a39d990f16803a03c7c2294a9cdde` | fetched 2026-09-07 |
| Mirror source | `Xinyuan-LilyGO/T-Display-S3` → `datasheet/ST7789V_SPEC_V1.4.pdf` @ commit `ec889e789b3cf093412689a143f7f37b42b56af7` | GitHub raw |
| Licence | Sitronix copyright; the surrounding repository is MIT, which does not cover the PDF. **Redistribution status: unknown** | — |

This is a **vendor mirror**, not Sitronix's own copy. Sitronix does not publish ST77xx
datasheets on an open portal, so board-vendor mirrors are the normal acquisition route for the
whole family — a pattern already recorded for the [ST77916](../st77916/README.md) and
[ST7789V2](../st7789v2/README.md).

## 2. Interface as used on the T-Display-S3

| Property | Value |
|---|---|
| Bus | **8-bit Intel-8080** (`TFT_PARALLEL_8_BIT`) |
| Signals | `D0..D7`, `WR`, `RD`, `DC`, `CS`, `RST` |
| Pixel clock, vendor | **16 MHz** |
| Pixel clock, ESPHome | 10 MHz |
| Colour depth | RGB565 (16-bit), 2 bus cycles per pixel |
| Inversion | **on** |
| Colour order | vendor `TFT_eSPI` setup says **RGB**; ESPHome says **BGR** — an unresolved conflict, see the [device record](../../../devices/lilygo/t-display-s3/gaps-and-conflicts.md#g3--colour-order-rgb-or-bgr) |
| GRAM offset | **35 columns** — the board's panel is 170 px wide in a 240-wide controller |

**The 35-column offset is the single most consequential integration fact.** It appears as
`CGRAM_OFFSET` in TFT_eSPI, `offset_width: 35` in ESPHome, and two literal `35`s in the
`Arduino_GFX` constructor. Get it wrong and you see a shifted image with a garbage band —
the symptom in [LilyGO issue #128](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/128).

## 3. Software

| Library | Support | Note |
|---|---|---|
| `TFT_eSPI` | `ST7789_DRIVER` + `TFT_PARALLEL_8_BIT` | needs `CGRAM_OFFSET`; configuration lives inside the library |
| `Arduino_GFX` | `Arduino_ST7789` + `Arduino_ESP32LCD8` | offsets are constructor arguments |
| `LovyanGFX` | `lgfx::Panel_ST7789` + `Bus_Parallel8` | |
| ESP-IDF | `esp_lcd_new_panel_st7789()` + `esp_lcd_new_panel_io_i80()` | first-party |
| ESPHome | `mipi_spi` model `T-DISPLAY-S3` | pins and offset built in |

Guide: [`guides/hardware/parallel-8080-lcd-buses.md`](../../../guides/hardware/parallel-8080-lcd-buses.md).

## 4. Do not substitute the family members blindly

ST7789**V**, **V2**, **VW** and **P3** are separate Sitronix documents. The
[`st7789v2` record](../st7789v2/README.md) in this repository documents a 2016 datasheet for a
part M5Stack later replaced with a P3 in a mid-life revision — i.e. these parts are **not**
drop-in equivalent in practice even for the same vendor. Treat a driver written against one as
a starting point for another, not as a port.

## 5. What was not verified

- **The datasheet's cover page was not read.** The version "V1.4" is taken from LilyGO's
  filename. The PDF's magic bytes and size were validated; its text layer was not checked
  against a rendered heading, which the research method requires before transcribing values.
  **No numeric value has been transcribed from it into this record** — everything above comes
  from board-level sources — so the risk is contained, but the verification is owed.
- Whether Sitronix's current ST7789V revision differs from V1.4.
- The colour-order conflict.

## 6. Used by

### LilyGO T-Display-S3 and T-Display-S3 Touch

→ [`devices/lilygo/t-display-s3`](../../../devices/lilygo/t-display-s3/README.md) ·
[`devices/lilygo/t-display-s3-touch`](../../../devices/lilygo/t-display-s3-touch/README.md)

Role: the sole display controller, bonded to a 1.9″ 170 × 320 IPS panel and driven over an
8-bit Intel-8080 bus at 16 MHz. Backlight is separate, via an
[AW9364DNR](../../awinic/aw9364/README.md) boost driver on GPIO38. The panel is powered from a
rail gated by GPIO15, so **the controller is unreachable until that pin is driven high** —
which is the board's most-reported failure mode. Pin map:
[`pinouts-and-buses.md`](../../../devices/lilygo/t-display-s3/pinouts-and-buses.md).
