# LilyGO T-Display-S3 AMOLED (1.91″)

> **Product:** T-Display S3 AMOLED · store handle `t-display-s3-amoled` · published **2023-04-14** ·
> **16 SKUs** including **V1.0 and V2.0 sold concurrently**, touch and non-touch, three regional
> warehouses · from **USD 26.44** (2026-09-07).
>
> **Two repositories cover this board.** The original
> [`T-Display-S3-AMOLED`](https://github.com/Xinyuan-LilyGO/T-Display-S3-AMOLED) @ `edd1333`
> **stopped receiving pushes on 2024-08-09**; the live one is
> [`LilyGo-AMOLED-Series`](https://github.com/Xinyuan-LilyGO/LilyGo-AMOLED-Series) @ `6d1dc00`,
> a single Arduino/PlatformIO library covering four AMOLED boards. **Use the latter.**
>
> Research retrieved **2026-09-07**. No hardware. Part of the
> [T-Display-S3 family](../t-display-s3-shared/README.md).

## Identity

| | |
|---|---|
| Panel | 1.91″ AMOLED, **240 × 536**, **350 nits** (vendor figure) |
| Controller | **Raydium RM67162**, **QSPI** — not parallel, not plain SPI |
| Touch | optional; **Hynitron CST816** family, I²C. LilyGO's library supports "both touch and non-touch versions" from one build |
| SoC | ESP32-S3R8, 16 MB flash, 8 MB OPI PSRAM |
| Sold as | V1.0 / V2.0 × soldered / non-soldered × touch / non-touch × 3 warehouses |
| Component records | [`raydium/rm67162`](../../../components/raydium/rm67162/README.md) · [`hynitron/cst816d`](../../../components/hynitron/cst816d/README.md) · [`espressif/esp32-s3r8`](../../../components/espressif/esp32-s3r8/README.md) · [`winbond/w25q128jv`](../../../components/winbond/w25q128jv/README.md) |

## The V1.0 / V2.0 problem — read before buying

LilyGO sells **both revisions at once** (`H619`/`H634` = V1.0, `H713`/`H712` = V2.0, all in
stock 2026-09-07) and publishes **no statement of what differs**. Comparing the two schematics
it ships:

| | `T-DISPLAY-S3-AMOLED.pdf` (older repo) | `T-Display-S3-AMOLED-Touch.pdf` (`LilyGo-AMOLED-Series`) |
|---|---|---|
| Flash `U3` | **`W25Q32`** — 4 MB | **`W25Q128JV`** — 16 MB |
| 3.3 V regulator | `U4 = IC_RT9080` (LDO) | `U4 = SY8089A1AAC` (**buck**) |
| Display supply | `U6 = IC_BV6802` | `U5 = AXPM65611` |
| Charger | `U5 = TP4065` | `U6 = TP4065` |
| Transistors | — | `Q1 NCE3401AY`, `Q2 KIA3400` |
| ESD | `D1/D2 ESD5451N-2` | `D5 SMF5.0A`, `D4 B5819W` |

The `W25Q32` is the alarming one: **4 MB where every README and store listing says 16 MB.**
Most likely a stale early sheet, but it is the vendor's own document and it is still published.
**Run `esptool.py flash_id` before you rely on 16 MB.** Recorded as family conflict
[F3](../t-display-s3-shared/README.md#4-family-level-conflicts) and revision
[R2](../t-display-s3-shared/board-revision-drift.md#r2--t-display-s3-amoled-191-v10-and-v20-sold-concurrently).

## Pinout

From `examples/factory/pins_config.h` @ **`edd133335c9f7c38d1e9be2d0eb67371f1f6428e`**,
cross-checked against `LilyGo-Display-IDF/main/product_pins.h`
(`#elif CONFIG_LILYGO_T_DISPLAY_S3_AMOLED`) @ `b1a1cc5`. **The two agree exactly.**

| Signal | GPIO | Note |
|---|---|---|
| `TFT_QSPI_CS` | 6 | |
| `TFT_QSPI_SCK` | 47 | |
| `TFT_QSPI_D0` | 18 | also `TFT_MOSI` |
| `TFT_QSPI_D1` | 7 | also `TFT_DC` |
| `TFT_QSPI_D2` | 48 | |
| `TFT_QSPI_D3` | 5 | |
| `TFT_QSPI_RST` | 17 | |
| `TFT_TE` | 9 | tearing-effect input |
| `TFT_SDO` | 8 | |
| `PIN_LED` | 38 | **not a backlight** — AMOLED is self-emissive. This is an indicator |
| `PIN_BAT_VOLT` | 4 | same divider arrangement as the base board |
| `PIN_BUTTON_1` | 0 | BOOT |
| `PIN_BUTTON_2` | **21** | **not GPIO14** — code from the base board will read a floating pin |
| I²C `SDA` / `SCL` | **3 / 2** | per `product_pins.h`; **touch IRQ is GPIO21 on the Touch variant, which collides with `BUTTON_2`** |

SPI clock in LilyGO's own example: **75 MHz** (`#define SPI_FREQUENCY 75000000`), mode 0,
`SPI2_HOST`. That is far faster than the base board's 16 MHz parallel bus — QSPI at 75 MHz
moves 4 bits per clock.

**There is no GPIO15 power gate on this board.** The single most important base-board
workaround does not apply, and looking for it wastes time.

## Display and software

`TFT_eSPI` **cannot drive this panel** — it has no QSPI transport. LilyGO's "TFT_eSPI examples"
in `LilyGo-AMOLED-Series` are `TFT_eSPI` **Sprites** rendered off-screen and pushed by the
library's own QSPI routine. Use:

| Route | How |
|---|---|
| **`LilyGo-AMOLED-Series`** (recommended) | Arduino Library Manager → "LilyGO AMOLED Series" → Install All. Auto-detects which of the four AMOLED boards it is on |
| `Arduino_GFX` | `Arduino_ESP32QSPI` + an RM67162 init |
| **ESPHome** | `mipi_spi` model **`T-DISPLAY-S3-AMOLED`**: `cs_pin=6, reset_pin=17, enable_pin=38, bus_mode=QUAD, brightness=0xD0, no_slpout=True`. Confirmed in `esphome/components/mipi_spi/models/amoled.py`, `dev` @ 2026-09-07 |
| LVGL | 8.x by default; the library ships an `lv_conf.h.v9` you rename to move to 9.x |

Dependencies the library declares: `XPowersLib v0.2.7`, `SensorLib v0.2.4`, `lvgl 8.x/9.x`,
`AceButton v1.10.1`, `Adafruit_NeoPixel v1.11.0`, `TinyGPSPlus v1.0.3`.
Arduino core: **V2.0.16 or later** — note this is *different from and newer than* the 2.0.14
the base board pins.

## Power

| | |
|---|---|
| Charger | **TP4065** on both schematics |
| Regulator | RT9080 LDO (V1.0) → SY8089A1AAC buck (V2.0) |
| Battery sense | GPIO4 |
| Vendor current figures | **90–230+ mA** active at 240 MHz with Wi-Fi; **≈230 µA** deep sleep, external GPIO0 wake |

Those sleep figures are LilyGO's own, from the `LilyGo-AMOLED-Series` README table @ `6d1dc00`
— and unlike the base board, they exist. They are **not** transferable to the base board.

## Add-ons

A **Camera Shield** exists (`H679`, USD 6.33) with its own schematic and example; it is the
only 1.91″-specific accessory.

## Documentation map

- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — the V1.0/V2.0 problem, the flash-size
  conflict, the GPIO21 collision, two unidentified parts
- Pinout, development and software: **in this file** (§ *Pinout*, § *Display and software*)
- Family-level material: [`../t-display-s3-shared/README.md`](../t-display-s3-shared/README.md),
  [`board-revision-drift.md`](../t-display-s3-shared/board-revision-drift.md),
  [`sources.md`](../t-display-s3-shared/sources.md)
- Pricing for every board in the family, dated 2026-09-07:
  [`../t-display-s3/market-and-pricing.md`](../t-display-s3/market-and-pricing.md)
- The `USB CDC On Boot` trap and the Arduino-core version pin apply here too:
  [`../t-display-s3/features/usb.md`](../t-display-s3/features/usb.md),
  [`../t-display-s3/development.md`](../t-display-s3/development.md)

**Not written for this board:** a standalone `pinouts-and-buses.md`, `features/`,
`examples/catalog.json` or `acquisition/manifest.json`. This is a **full-ish**, not a full,
record — see [`../t-display-s3-shared/research-log.md`](../t-display-s3-shared/research-log.md)
for the depth table.

## Artifacts

`artifacts/schematic/T-DISPLAY-S3-AMOLED.pdf` (507 994 B, SHA-256 `e44158506e7ca189…`) —
the V1.0-era sheet.
`artifacts/schematic/T-Display-S3-AMOLED-Touch.pdf` (361 409 B, SHA-256 `da46e0f36732b99c…`) —
the current sheet, and the one LilyGO's resource table points at for **both** touch and
non-touch.
`artifacts/schematic/Camera-Shield.pdf` (157 812 B, SHA-256 `362bdcfb504a57c8…`).
Both retrieved 2026-09-07 at the commits above. RM67162 and CST816 datasheets are filed under
their components.
