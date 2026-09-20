# Raydium RM67162

- **Category:** AMOLED display driver IC with on-chip GRAM; **QSPI / SPI / MIPI-DSI** host
  interfaces; on-chip brightness (DBV) control.
- **Manufacturer:** Raydium Semiconductor Corporation (Taiwan).
- **Retrieved:** 2026-09-07

The display driver of the **LilyGO T-Display-S3 AMOLED (1.91″)** and the
**T-Display-S3 AMOLED Plus** — 240 × 536 panels driven over **QSPI**.

## 1. Identity and artifact

| Property | Value |
|---|---|
| Part | **RM67162** |
| Datasheet version | **V0.0** per the filename LilyGO ships (`RM67162 DataSheet_V0.0.pdf` in one repo, `RM67162 DataSheet.pdf` in the other) |
| Local artifact | [`artifacts/rm67162-datasheet-v0.0-lilygo-mirror.pdf`](artifacts/rm67162-datasheet-v0.0-lilygo-mirror.pdf) — 3 729 479 B, SHA-256 `1717405949518703a8fe40e1dcbbb1d1abf7fa765b2bb7c2d101f430398a5b51` |
| Mirror source | `Xinyuan-LilyGO/LilyGo-AMOLED-Series` → `datasheet/RM67162 DataSheet.pdf` @ `6d1dc008b94578cc34ba4a0f3b223dd808ca963f` |
| Second mirror, same bytes | `Xinyuan-LilyGO/T-Display-S3-AMOLED` → `datasheet/RM67162 DataSheet_V0.0.pdf` @ `edd133335c9f7c38d1e9be2d0eb67371f1f6428e`, **3 729 479 B — identical size**, so almost certainly the same file under two names. Only one copy is retained; the second URL is recorded here rather than stored twice |
| Licence | Raydium copyright. Repository is MIT, which does not cover the PDF. **Redistribution status: unknown** |

Raydium does not publish RM67162 on an open portal; board-vendor mirrors are the acquisition
route.

## 2. Interface as used by LilyGO

| Property | Value | Source |
|---|---|---|
| Host bus | **QSPI** — `CS`, `SCK`, `D0..D3`, plus `RST` and a `TE` input | `pins_config.h` @ `edd1333` |
| Clock | **75 MHz**, mode 0, `SPI2_HOST` | `#define SPI_FREQUENCY 75000000` |
| Resolution | 240 × 536 | vendor README |
| Brightness | on-chip; ESPHome writes **`0xD0`** | `esphome/.../amoled.py` |
| Sleep-out | ESPHome sets `no_slpout=True` and puts `SLPOUT` **early in the init sequence** for the plain AMOLED board | same |

**Two boards, same controller, different initialisation.** ESPHome's `T-DISPLAY-S3-AMOLED`
model uses `initsequence=(SLPOUT,)` — essentially nothing. Its `T-DISPLAY-S3-AMOLED-PLUS` model
uses a **16-command sequence** (`PAGESEL 4`, `0x6A 0x00`, `PAGESEL 5`, `PAGESEL 7`, `0x07 0x4F`,
`PAGESEL 1`, `0x2A 0x02`, `0x2B 0x73`, `PAGESEL 0x0A`, `0x29 0x10`, `PAGESEL 0`, `0x53 0x20`,
`TEON 0x00`, `PIXFMT 0x75`, `0xC4 0x80`) and a **40 MHz** data rate against the plain board's
75 MHz. Panel-module differences, not controller differences — but **RM67162 code does not
port between the two LilyGO boards unchanged**, which is worth knowing before assuming it does.

## 3. Software

| Route | Note |
|---|---|
| **`LilyGo-AMOLED-Series`** | LilyGO's own library; carries the init tables. The path of least resistance |
| `Arduino_GFX` | `Arduino_ESP32QSPI` + an RM67162 driver |
| ESPHome | `mipi_spi`, models `T-DISPLAY-S3-AMOLED` / `T-DISPLAY-S3-AMOLED-PLUS` |
| **`TFT_eSPI`** | **cannot drive it.** No QSPI transport. LilyGO's "TFT_eSPI examples" are Sprites pushed by the library's own QSPI routine |

## 4. What was not verified

The datasheet's cover and register map were **not read**; no value in this record is
transcribed from it. Everything above is from board-level sources and from independent
third-party (ESPHome) configuration. The `V0.0` version string is LilyGO's filename.

## 5. Used by

### LilyGO T-Display-S3 AMOLED (1.91″)
→ [`devices/lilygo/t-display-s3-amoled`](../../../devices/lilygo/t-display-s3-amoled/README.md).
QSPI on GPIO 6 (CS), 47 (SCK), 18/7/48/5 (D0–D3), 17 (RST), 9 (TE), 8 (SDO). 75 MHz. Touch,
where fitted, is a separate Hynitron CST816 part on I²C.

### LilyGO T-Display-S3 AMOLED Plus
→ [`devices/lilygo/t-display-s3-amoled-plus`](../../../devices/lilygo/t-display-s3-amoled-plus/README.md).
Same panel and controller, different board: BQ25896 PMIC, PCF85063ATL RTC, microSD, and a
**different init sequence and clock** (see §2).
