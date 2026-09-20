# Sitronix ST7796S

- **Category:** single-chip TFT-LCD controller/driver with on-chip GRAM — **320 RGB × 480 dot**,
  262 k colours; MCU parallel (8/9/16/18-bit), 3/4-wire SPI and RGB interfaces.
- **Manufacturer:** Sitronix Technology Corporation (Taiwan).
- **Retrieved:** 2026-09-07
- **Siblings here:** [`st7789v`](../st7789v/README.md) · [`st7789v2`](../st7789v2/README.md) ·
  [`st7789vw`](../st7789vw/README.md) · [`st7789p3`](../st7789p3/README.md) ·
  [`st77916`](../st77916/README.md) · [`st7701s`](../st7701s/README.md)

The display controller of the **LilyGO T-Display-S3 Pro** — 2.33″, 222 × 480, on plain **4-wire
SPI**. It is the only board in the T-Display-S3 family that uses ordinary SPI for its display.

## ⚠ S or U? An unresolved naming conflict

Three sources, three strings:

| Source | Says |
|---|---|
| LilyGO's `T-Display-S3-Pro` README specification table | **`ST7796U (SPI)`** |
| The datasheet LilyGO ships in that same repository | **`ST7796S-Sitronix.pdf`** |
| ESPHome's `mipi_spi` model | `ST7796` (unsuffixed), extended as `T-DISPLAY-S3-PRO` |

**ST7796S and ST7796U are different Sitronix parts.** They share the 320 × 480 GRAM and much of
the command set but are not documented as interchangeable. This record is filed under **`S`**
because that is what the *primary document in the vendor's own repository* says, and a datasheet
outranks a specification table — but the conflict is real and is **not resolved**. Anyone
writing an init sequence from scratch should verify against the physical marking.

## 1. Identity and artifact

| Property | Value |
|---|---|
| Part | **ST7796S** (per the shipped datasheet) |
| Local artifact | [`artifacts/st7796s-datasheet-lilygo-mirror.pdf`](artifacts/st7796s-datasheet-lilygo-mirror.pdf) — 3 557 406 B, SHA-256 `da0d7eb40cc1f3b59df0e70a602cbd729822eadad56f2e45d23460fe1ff70d47` |
| Mirror source | `Xinyuan-LilyGO/T-Display-S3-Pro` → `datasheet/ST7796S-Sitronix.pdf` @ `08b8b2bbcb8b263131af119476403080cd30224f` |
| Licence | Sitronix copyright. **The `T-Display-S3-Pro` repository declares no licence at all**, so redistribution status is doubly unknown |

Sitronix does not publish ST77xx datasheets openly; board-vendor mirrors are the acquisition
route, as recorded for [ST77916](../st77916/README.md) and [ST7789V2](../st7789v2/README.md).

## 2. Interface on the T-Display-S3 Pro

| Property | Value | Source |
|---|---|---|
| Bus | **4-wire SPI**, shared with the microSD card | `examples/factory/utilities.h` @ `08b8b2b` — the file's own comment reads `// SD , TFT share SPI Bus` |
| Pins | `MISO` 8 · `MOSI` 17 · `SCK` 18 · `CS` 39 · `RST` 47 · `DC` 9 · `BL` 48 | same |
| Panel | 222 × 480 (LilyGO also writes 480 × 222) | vendor README |
| **GRAM offset** | **`offset_width = 49`** — a 222-px panel in a 320-wide controller | ESPHome `T-DISPLAY-S3-PRO` model |
| Inversion | on | ESPHome `invert_colors=True` |

The 49-column offset is the ST7796's analogue of the T-Display-S3's 35-column ST7789 offset, and
it fails the same way if omitted: a shifted image with a garbage band.

**Bus sharing matters.** The display and the microSD card are on one SPI bus with separate chip
selects (`TFT_CS` 39, `SD_CS` 14). Concurrent access must be serialised, and a long SD write
will stall display updates — a design constraint worth knowing before building a
video-playback or logging application on this board.

## 3. Backlight — and the V1.0/V1.1 trap

`BOARD_TFT_BL` is GPIO48, but **the brightness scale changed between board revisions**:

```c
#ifdef USING_DISPLAY_PRO_V1
#define BRIGHTNESS_MAX_LEVEL        255      // V1.0
#else
#define BRIGHTNESS_MAX_LEVEL        16       // V1.1
#endif
```
— `examples/factory/utilities.h` @ `08b8b2b`, whose comment states *"The difference between
V1.0 and V1.1 is the backlight driver."* Build for the wrong one and brightness is 16× off.
Full detail: [board-revision-drift R6](../../../devices/lilygo/t-display-s3-shared/board-revision-drift.md#r6--t-display-s3-pro-v10-vs-v11-backlight-driver).

## 4. Software

`Arduino_GFX` (LilyGO's choice; the repo vendors `GFX Library for Arduino`) ·
`TFT_eSPI` (plain SPI, so it can work, but **no vendor setup file ships**) ·
`LovyanGFX` (`Panel_ST7796`) · ESP-IDF `esp_lcd_new_panel_st7796()` ·
**ESPHome** `mipi_spi` model `T-DISPLAY-S3-PRO`.

## 5. What was not verified

Datasheet cover, register map and timing were **not read**; nothing is transcribed from it.
The S-vs-U question is open.

## 6. Used by

### LilyGO T-Display-S3 Pro
→ [`devices/lilygo/t-display-s3-pro`](../../../devices/lilygo/t-display-s3-pro/README.md)

Sole display controller, 4-wire SPI shared with the microSD. Touch is a separate
[Hynitron CST226SE](../../hynitron/cst226se/README.md) at I²C `0x5A`.
