# LilyGO T-QT — lineage stub

> **Stub record.** Included because the brief names it as a family relative; it is a
> *cousin*, not a T-Display-S3 variant. Store: **T-QT Pro** handle `t-qt-pro`, published
> 2022-09-21, from **USD 9.05**; **T-QT C6** handle `t-qt-c6`, published 2024-06-13, from
> **USD 13.25**. Both in stock 2026-09-07.
> Repo `Xinyuan-LilyGO/T-QT` @ **`230f0c0ea7677fdde29ca7a49a419dbf597e6b3e`**, MIT, 149★.
> Research retrieved 2026-09-07. No hardware.

## Identity

| | | Source |
|---|---|---|
| Format | a thumbnail-sized board — LilyGO describes T-QT C6 as *"only the size of two thumbnails"* | repo description |
| T-QT Pro | ESP32-S3, 0.85″ **128 × 128** TFT on SPI | store, repo |
| T-QT C6 | **ESP32-C6**, 128 × 128 **touch** TFT, separate charging LED, power-path-management chip with programmable bus limits | repo description @ 2026-09-03 |
| Pins (T-QT S3, ESP-IDF) | `SPI MOSI 2 / SCK 3`, `TFT_CS 5 / RST 1 / DC 6 / BL 10`; `POWERON 10` is present but **commented out** | `LilyGo-Display-IDF/main/product_pins.h`, `#elif CONFIG_LILYGO_T_QT_S3` @ `b1a1cc5` |

## Relationship to the T-Display-S3

Same vendor, same era, same `LilyGo-Display-IDF` support tree, same Arduino-core pinning
culture — and **no shared PCB, panel, bus or pin map**. It is in this repository's LilyGO tree
because a reader enumerating "the T-Display family" will encounter it and should be able to
rule it out quickly.

The one genuinely transferable observation: `product_pins.h` shows a `BOARD_POWERON` define
**commented out** for the T-QT, where the T-Display and T-Display-S3 both have one active. The
power-gate pattern is a LilyGO habit that appears and disappears across the catalogue, which is
why "does this board have a power-enable pin?" must be answered per board rather than assumed.

## Gaps

**Stub.** No schematic retrieved, no artifacts, no component records created, no market
analysis. The T-QT C6's power-path chip is not identified. Documented only to the depth needed
to place it in the family and rule it out.
