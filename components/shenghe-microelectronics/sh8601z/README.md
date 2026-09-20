# Shenghe Microelectronics SH8601Z

- **Category:** AMOLED display driver IC — **480 RGB × 480**, 16.7 M colours.
- **Manufacturer:** **SHENGHE MICRO ELECTRONICS** — established from the datasheet's own cover
  page and running headers.
- **Retrieved:** 2026-09-07
- **Sibling:** [`sh8501b`](../sh8501b/README.md), the 1.47″ part from the same maker.

The display driver of the **LilyGO T-Display-S3 AMOLED 1.43″** in its `DO0143FAT01` /
`DO0143FMST02` build variant.

## 1. Why this record matters beyond one board

**It settles who makes the SH86xx parts.** This repository already contains
[`components/generic/sh8601-compatibility-driver`](../../generic/sh8601-compatibility-driver/README.md),
written for a Waveshare board whose vendor code calls a driver `esp_lcd_sh8601` while the fitted
controller is almost certainly a Sitronix ST77916. That record correctly concludes the *driver
name* is not evidence of an SH8601 controller — and it could not say who would make one if it
existed.

**Now we know: SH8601Z is a real part, and it is Shenghe Microelectronics, not Sitronix.**
The two records are complementary, not contradictory:

| | This record | `generic/sh8601-compatibility-driver` |
|---|---|---|
| Subject | the **silicon** | the **software naming conflict** |
| Claim | SH8601Z exists, is Shenghe's, and is fitted to a LilyGO board | `esp_lcd_sh8601` is a generic QSPI shim and its presence proves nothing about a Waveshare panel |
| Together | a driver *named* `sh8601` may drive a real SH8601 (LilyGO 1.43″) **or** anything else with a QSPI DCS front end (Waveshare) | |

## 2. Identity and artifact

| Property | Value |
|---|---|
| Part | **SH8601Z** |
| Cover page text | "SHENGHE MICRO ELECTRONICS · 480 RGB × 480 / 16.7M color · AMOLED Display Driver IC · Datasheet · SH8601Z" |
| Local artifact | [`artifacts/sh8601z-datasheet-lilygo-mirror.pdf`](artifacts/sh8601z-datasheet-lilygo-mirror.pdf) — 4 505 031 B, SHA-256 `2831dc9730e8daeabd6eac0871080afc988ffd5725962421b7c21cf6972d7628` |
| Mirror source | `Xinyuan-LilyGO/T-Display-S3-AMOLED-1.43-1.75` → `information/SH8601Z.pdf` @ `87aabe888eea6a7c0f95ce1991ca75fa98c2a172` |
| Marked | **CONFIDENTIAL** on the first page |
| Licence | Shenghe copyright, marked confidential. Repository is MIT, which does not cover it. **Redistribution status: `prohibited` on the face of the document** — should remain **unstaged** pending a decision |

## 3. How the cover was read

The PDF's plain text layer is offset like the family's other Chinese-vendor datasheets, but the
`/ToUnicode` CMap route produced clean English (`SHENGHE MICRO ELECTRONICS`, `480 RGB x 480`,
`16.7M color`, `AMOLED Display Driver IC`, `SH8601Z`) and the two routes agree. Method:
[`vendors/lilygo/README.md`](../../../vendors/lilygo/README.md).

**Only the cover and table of contents were read.** No register, timing or electrical value is
transcribed here.

## 4. Board usage

Selected at build time by `CONFIG_SCREEN_TYPE_DO0143FAT01` in
`components/private_library/pin_config.h` @ `87aabe8`, whose comment reads:
`DO0143FAT01 // DO0143FMST02 // 1.43 inches (SH8601 FT3168)`.

The **other** 1.43″ build option (`DO0143FMST10`) uses a
[Chipone CO5300](../../chipone/co5300/README.md) instead. One product page, two display
controllers.

Pins: QSPI `LCD_SDIO0..3` GPIO 11/13/14/15, `LCD_SCLK` 12, `LCD_CS` 10, `LCD_RST` 17,
`LCD_EN` 16. Touch is a separate [FocalTech FT3168](../../focaltech/ft3168/README.md) on
I²C (SDA GPIO7 / SCL GPIO6, INT GPIO9).

Note the datasheet's **480 × 480** against the panel's **466 × 466** visible / **473 × 467**
in LilyGO's header — three numbers, consistent with a 480-wide controller driving a smaller
round panel through a window. Not confirmed.

## 5. Used by

### LilyGO T-Display-S3 AMOLED 1.43″ (`DO0143FAT01` variant)
→ [`devices/lilygo/t-display-s3-amoled-1-43-1-75`](../../../devices/lilygo/t-display-s3-amoled-1-43-1-75/README.md)
