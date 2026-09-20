# LilyGO / TTGO T-Display (ESP32) — lineage stub

> **Stub record**, written to anchor the T-Display-S3's ancestry. Not researched to device
> depth. Store handle `t-display`, published **2023-08-04** (the *store page*; the product is
> older — the repo predates it). SKUs `Q224` 4 MB **USD 8.04**, `Q125` 16 MB **USD 8.94**,
> `K163`/`K164`/`K198` with shell **USD 11.99–12.99**. In stock 2026-09-07.
> Repo `Xinyuan-LilyGO/TTGO-T-Display` @ **`6f89cddcde7152b84f7afc1831b6a1dee1fc3206`**,
> licence MIT, **1 192★** — the most-starred repository in the whole organisation.

## Identity

| | | Source |
|---|---|---|
| SoC | **ESP32** (not S3), dual LX6 | store, repo |
| Display | **1.14″, 135 × 240**, ST7789 on **4-wire SPI** | ESPHome model `T-DISPLAY` |
| Pins (ESPHome model) | `cs_pin=5, dc_pin=16`, `offset_width=52, offset_height=40`, `invert_colors=True` | `esphome/components/mipi_spi/models/lilygo.py`, `dev` @ 2026-09-07 |
| Pins (ESP-IDF) | `POWERON 14`, `SPI MISO 21 / MOSI 19 / SCK 18`, `TFT_CS 5 / RST 23 / DC 16 / BL 4` | `LilyGo-Display-IDF/main/product_pins.h`, `#elif CONFIG_LILYGO_T_DISPLAY` @ `b1a1cc5` |
| Flash | 4 MB or 16 MB **as a purchase option** | store SKUs `Q224` / `Q125` |

## Why it matters to the T-Display-S3

- **It defined the format** — a cheap ESP32 with a bonded colour strip, two buttons and a
  battery connector — and the S3 board is a straight re-do of it with a faster SoC, a bigger
  panel and a parallel bus.
- **It carries a power-enable pin too** (`BOARD_POWERON 14`), which is the direct ancestor of
  the T-Display-S3's GPIO15 gate. The trap is inherited, not new.
- **It has software support the S3 board does not**: `wled/WLED` ships
  `usermods/TTGO-T-Display/`, and there is no WLED equivalent for any S3 board in the family.
- Its 1 192★ against the S3's 1 169★ is the clearest single measure of how much community mass
  the line carries.

## Differences that matter if you are choosing between them

| | T-Display (ESP32) | T-Display-S3 |
|---|---|---|
| Price 2026-09-07 | **USD 8.04** | USD 9.04 |
| SoC | ESP32 (LX6, BLE **and Classic Bluetooth**) | ESP32-S3 (LX7, **BLE only**) |
| Display | 1.14″ 135×240 SPI | 1.9″ 170×320 **8-bit parallel** |
| PSRAM | none | 8 MB OPI |
| Flash | 4 or 16 MB | 16 MB |
| USB | CH340-class bridge | **native USB**, no bridge |
| WLED | **supported** | not supported |

**The ESP32 board is the one to pick if you need Classic Bluetooth or WLED.** For everything
else the S3 board is better for a dollar more.

## Gaps

This is a **stub**. No pinout table beyond the two vendor sources quoted, no schematic
retrieved, no artifacts held, no market analysis beyond the store snapshot. Documented to the
depth needed to establish lineage and nothing further.
