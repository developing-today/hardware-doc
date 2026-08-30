# Sitronix ST7701S

> TFT LCD controller, up to 480×864, MIPI DSI / RGB
> Research snapshot **2026-08-24**. Documented as fitted to the Nicolai Electronics Tanmatsu; no hardware was available.

## Key specifications

| Property | Value |
|---|---|
| Max resolution | 480 × 864 |
| Colour | up to 16.7 M (24-bit RGB888) |
| Interfaces | **MIPI DSI**, RGB parallel, SPI |
| Typical use | Small high-density portrait panels |

No manufacturer datasheet located in this research pass.

## Notes

A widely used controller for small portrait TFT panels. Espressif provide an
`esp_lcd_st7701` driver, but **the initialisation command sequence is panel-specific** — the
controller alone is not enough, you need the sequence for the exact glass it is bonded to.

⚠ Colour depth is disputed between vendor sources — see [`display.md`](../../../devices/nicolai-electronics/tanmatsu/display.md).

## Used by

### Nicolai Electronics Tanmatsu

| | |
|---|---|
| Panel | **SWI `LH397K-IC01`** — 3.97", 480×800, 330 cd/m², 51.84 × 86.40 mm |
| Interface | **MIPI DSI, 2 data lanes** + clock, via `CN1` (Hirose DF37NB-24DS-0.4V) |
| Reset | ESP32-P4 GPIO **14** |
| Tearing effect | ESP32-P4 GPIO **11** |
| PHY supply | ESP32-P4 internal **LDO channel 3 at 2.5 V** (`VMIPI`) |
| Backlight | ≈24 V @ 20 mA from an AP3032, PWM'd by the **coprocessor** (`PB4`), set via coprocessor I2C register `0x0B` |
| Driver | [`nicolaielectronics/mipi_dsi_abstraction`](https://components.espressif.com/components/nicolaielectronics/mipi_dsi_abstraction) — carries the Tanmatsu init sequence |

Device record: [Nicolai Electronics Tanmatsu](../../../devices/nicolai-electronics/tanmatsu/README.md) · BOM: [`bom.md`](../../../devices/nicolai-electronics/tanmatsu/bom.md) · pinouts: [`pinouts-and-buses.md`](../../../devices/nicolai-electronics/tanmatsu/pinouts-and-buses.md)

## Caveats

- Nothing in this record was verified on hardware.
- Board-level integration details come from the Tanmatsu production BOM (CERN-OHL-P), the Badge.Team BSP (MIT) and badge.team documentation, all retrieved 2026-08-24.
- Part-level specifications are from manufacturer product pages; **no local datasheet copies were retained**.
