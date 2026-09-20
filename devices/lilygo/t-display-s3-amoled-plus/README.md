# LilyGO T-Display-S3 AMOLED Plus

> **Product:** T-Display S3 AMOLED Plus · handle `t-display-s3-amoled-plus` · published
> **2024-10-31** · SKU `H754` "1.9inch" · **USD 32.68**, in stock 2026-09-07.
> Covered by `LilyGo-AMOLED-Series` @ **`6d1dc008b94578cc34ba4a0f3b223dd808ca963f`**.
> Research retrieved 2026-09-07. **Depth: medium.** No hardware.

## Identity — the same panel, a completely different board

The panel is the **same 1.91″ 240 × 536 RM67162 AMOLED** as the
[T-Display-S3 AMOLED](../t-display-s3-amoled/README.md). Everything behind it is different, and
the differences are the reason to buy it.

| Function | Part | Interface | Component record |
|---|---|---|---|
| SoC | ESP32-S3 | — | [`espressif/esp32-s3r8`](../../../components/espressif/esp32-s3r8/README.md) |
| Flash `U3` | **W25Q128JV**, 16 MB | QSPI | [`winbond/w25q128jv`](../../../components/winbond/w25q128jv/README.md) |
| Display | RM67162, 240×536 | QSPI | [`raydium/rm67162`](../../../components/raydium/rm67162/README.md) |
| **Charger / PMIC `U6`** | **TI BQ25896** — I²C, buck charger with OTG boost, ADC, path management | I²C | [`texas-instruments/bq25896`](../../../components/texas-instruments/bq25896/README.md) |
| **RTC `U7`** | **NXP PCF85063ATL** | I²C | [`nxp/pcf85063a`](../../../components/nxp/pcf85063a/README.md) |
| **RTC backup cell `U8`** | **Seiko MS412FE-FL26E** rechargeable lithium coin | — | *(record pending)* |
| Regulator `U5` | RT9080-33GJ5 LDO | — | *(record pending)* |
| Display supply `U4` | `AXPM65611` — **unidentified** | — | [unidentified](../../../components/unidentified/lilygo-t-display-s3-family/axpm65611/README.md) |
| **microSD `J1`** | `MISROSD/TF_SLOT` | SPI/SDMMC | [`generic/micro-sd-sdmmc`](../../../components/generic/micro-sd-sdmmc/README.md) |
| Battery connectors | **two** — `CN4`, `CN5`, both 2P 2.5 mm | — | — |
| Antenna | `P1` IPEX-1 | — | — |
| Headers | `P4`, `P5` — 14-pin 2.54 mm | — | — |

Derived from `schematic/T-Display-S3-AMOLED-Plus.pdf` @ `6d1dc00`
(468 313 B, SHA-256 `ec4a97b697dd14413c88ea98d9bedaf601fa98ef24d88c9b0d7bf3fd0c2d046f`,
retained under `artifacts/schematic/`). Part identities are read from the sheet's designator
strings; **net connectivity was not traced.**

## Why it matters

Three things the plain AMOLED board does not have:

1. **A real PMIC.** The BQ25896 is I²C-controlled: programmable charge current, input-current
   limit, OTG 5 V boost, and on-chip ADC for battery/system/input voltage and charge current.
   Compare the plain AMOLED's dumb linear **TP4065**, where charge current is a soldered
   resistor. LilyGO ships `examples/PPM_Example_for_191Plus` for it.
2. **A battery-backed RTC.** PCF85063ATL plus a Seiko MS412FE rechargeable coin cell means the
   clock survives a main-battery swap. Nothing else in the AMOLED line has this.
3. **A microSD slot on the board**, not on a shield.

LilyGO's own sleep figure reflects the added complexity: **≈230–700 µA "dynamic"** deep sleep
against a flat ≈230 µA for the plain AMOLED — the range is the RTC and PMIC doing work.
Active current is the same 90–230+ mA class.

## Software

`LilyGo-AMOLED-Series` auto-detects the board. Pin map is in `product_pins.h` @ `b1a1cc5` and
in the library's board table.

**ESPHome supports it as a named model** — `T-DISPLAY-S3-AMOLED-PLUS` in
`esphome/components/mipi_spi/models/amoled.py` (`dev`, 2026-09-07):
`cs_pin=6, reset_pin=17, dc_pin=7, enable_pin=38, data_rate=40MHz, brightness=0xD0`, with a
**16-command init sequence** (`PAGESEL 4 / 0x6A 0x00 / PAGESEL 5 / PAGESEL 7 / 0x07 0x4F / …`).
That sequence differs from the plain AMOLED's, which is `(SLPOUT,)` only — so **the two boards
need different panel initialisation despite the same controller.** That is a concrete, useful
finding: do not assume RM67162 code ports between them.

## Sources

| ID | Source | Class | Retrieved |
|---|---|---|---|
| PL1 | `LilyGo-AMOLED-Series` README.MD § *Support Product* @ `6d1dc00` | primary | 2026-09-07 |
| PL2 | `schematic/T-Display-S3-AMOLED-Plus.pdf` @ `6d1dc00` | primary | 2026-09-07 |
| PL3 | `esphome/components/mipi_spi/models/amoled.py`, `dev` | primary (third-party) | 2026-09-07 |
| PL4 | LilyGO store feed | primary | 2026-09-07 |

## Gaps

- **This is a medium-depth record.** No `pinouts-and-buses.md`, `features/` or `examples/`
  directory was written. What is missing: a full GPIO table, per-feature guides, an example
  catalogue and an acquisition manifest.
- Net connectivity not traced.
- `AXPM65611` (`U4`) unidentified.
- **Two battery connectors** (`CN4`, `CN5`) — whether they are parallel, alternates, or one is
  for the RTC cell is **not established**.
- No hardware; no measurements.
