# Hardware components and interfaces

Research retrieved 2026-08-21. Manufacturer-specific parts use `components/<manufacturer>/<part>/`; unresolved or generic interfaces use `components/generic/<category>/`.

Every manufacturer-specific record links back to its **[vendor sourcing guide](../vendors/README.md)** — how to obtain any document from that manufacturer, its part-numbering conventions and its known gotchas. Every record also carries a **Used By** section naming the devices that contain it.

## By manufacturer

| Manufacturer | Sourcing guide | Parts here |
|---|---|---|
| Espressif Systems | [vendors/espressif](../vendors/espressif/README.md) | [ESP32-P4](espressif/esp32-p4/README.md) · [ESP32-S3R8](espressif/esp32-s3r8/README.md) · [ESP32-U4WDH](espressif/esp32-u4wdh/README.md) · [ESP32-WROVER](espressif/esp32-wrover/README.md) · [ESP32-WROOM-32U](espressif/esp32-wroom-32u/README.md) |
| Texas Instruments | [vendors/texas-instruments](../vendors/texas-instruments/README.md) | [DRV2605L](texas-instruments/drv2605l/README.md) · [DRV2605](texas-instruments/drv2605/README.md) · [PCM5100A](texas-instruments/pcm5100a/README.md) · [TLV62569DBVT](texas-instruments/tlv62569dbvt/README.md) · [TPS65186](texas-instruments/tps65186/README.md) · [BQ25306](texas-instruments/bq25306/README.md) |
| NXP Semiconductors | [vendors/nxp](../vendors/nxp/README.md) | [PCAL6416A](nxp/pcal6416a/README.md) · [PCF85063A](nxp/pcf85063a/README.md) |
| E Ink Holdings | [vendors/e-ink](../vendors/e-ink/README.md) | [ED052TC4 / ED052TC2](e-ink/ed052tc4/README.md) — ⚠ no public panel datasheets |
| Winbond | [vendors/winbond](../vendors/winbond/README.md) | [W25Q128JVPIQ](winbond/w25q128jv/README.md) |
| Sitronix | [vendors/sitronix](../vendors/sitronix/README.md) | [ST77916](sitronix/st77916/README.md) · [ST7789VW](sitronix/st7789vw/README.md) · [ST7701S](sitronix/st7701s/README.md) |
| **Jadard Technology** | [vendors/jadard](../vendors/jadard/README.md) | [JD9365](jadard/jd9365/README.md) — ⚠ datasheet omits the paged manufacturer registers |
| **Fitipower Integrated Technology** | [vendors/fitipower](../vendors/fitipower/README.md) | [EK79007AD](fitipower/ek79007ad/README.md) · [EK73217BCGA](fitipower/ek73217bcga/README.md) — a source-driver + gate-driver **pair** |
| **Ilitek (ILI Technology)** | [vendors/ilitek](../vendors/ilitek/README.md) | [ILI9881C](ilitek/ili9881c/README.md) — ⚠ **not** "ILI9981C", which does not exist |
| Hynitron | [vendors/hynitron](../vendors/hynitron/README.md) | [CST816D](hynitron/cst816d/README.md) |
| WCH (Nanjing Qinheng) | [vendors/wch](../vendors/wch/README.md) | [CH445P](wch/ch445p/README.md) · [CH340C](wch/ch340c/README.md) · [CH340X USB-UART bridge](wch/ch340x/README.md) |
| MEMSensing | [vendors/memsensing](../vendors/memsensing/README.md) | [MSM261D4030H1CPM](memsensing/msm261d4030h1cpm/README.md) |
| SGMicro | [vendors/sgmicro](../vendors/sgmicro/README.md) | [SGM2036-3.3](sgmicro/sgm2036-3.3/README.md) · [SGM40567](sgmicro/sgm40567/README.md) · [SGM6029](sgmicro/sgm6029/README.md) |
| Alpha & Omega Semiconductor | [vendors/alpha-and-omega-semiconductor](../vendors/alpha-and-omega-semiconductor/README.md) | [AO3400A](alpha-and-omega-semiconductor/ao3400a/README.md) |
| Alps Alpine | [vendors/alps-alpine](../vendors/alps-alpine/README.md) | [SSCM110100](alps-alpine/sscm110100/README.md) |
| OmniVision Technologies | — | [OV2640](omnivision/ov2640/README.md) · [OV3660](omnivision/ov3660/README.md) · [OV5640](omnivision/ov5640/README.md) |
| GigaDevice | — | [GD25Q64E](gigadevice/gd25q64e/README.md) |
| Hirose Electric | — | [DF40C-30DP-0.4V(51)](hirose/df40c-30dp-0.4v/README.md) |
| *unresolved / generic* | — | everything under `generic/`, below |

## All records

### Inkplate 5 / Inkplate 5 Gen 2 / ZeroWriter Ink

| Record | Category | Fitted on |
|---|---|---|
| [E Ink ED052TC4 / ED052TC2](e-ink/ed052tc4/README.md) | 5.2" parallel-interface e-paper panel, 1280×720 (TC4) or 960×540 (TC2) | Inkplate 5 (`U11`) · Gen 2 (`U9`) · ZeroWriter Ink (`U9`) |
| [Espressif ESP32-WROVER](espressif/esp32-wrover/README.md) | ESP32 module **with PSRAM** — mandatory for the e-paper framebuffers | Inkplate 5 (`U10`) · Gen 2 (`U11`) · ZeroWriter Ink (`U11`) |
| [Espressif ESP32-WROOM-32U-N4](espressif/esp32-wroom-32u/README.md) | ESP32 module, external-antenna variant, 4 MB flash | ZeroWriter Ink **keyboard PCB** (`U1`) |
| [Texas Instruments TPS65186](texas-instruments/tps65186/README.md) | e-paper display PMIC (bias rails + VCOM), I²C `0x48` | Inkplate 5 · Gen 2 · ZeroWriter Ink (`U1`) |
| [NXP PCAL6416A](nxp/pcal6416a/README.md) | 16-bit I²C GPIO expander, `0x20` — carries EPD control and SD power | Inkplate 5 (`U9`) · Gen 2 (`U10`) · ZeroWriter Ink (`U10`) |
| [NXP PCF85063A](nxp/pcf85063a/README.md) | real-time clock/calendar with alarm and timer, I²C `0x51`, 220 nA | Inkplate 5 · Gen 2 · ZeroWriter Ink (`U7`) |
| [Texas Instruments BQ25306](texas-instruments/bq25306/README.md) | switch-mode 1S/2S Li-ion charger, 2.0 A @ 4.18 V as configured | **ZeroWriter Ink only** (`U12`) |
| [WCH CH340C](wch/ch340c/README.md) | USB-to-UART bridge with integrated crystal | Inkplate 5 · Gen 2 · ZeroWriter Ink (`U3`) |

### Display controllers

All five records below were created on **2026-08-30** for controllers that were fitted on documented boards but had no component record. See the [display interfaces guide](../guides/hardware/display-interfaces.md) for how these interfaces compare.

| Record | Interface | Resolution | GRAM? | Fitted on |
|---|---|---|---|---|
| [Jadard JD9365](jadard/jd9365/README.md) · [programming ref](jadard/jd9365/jd9365-programming-reference.md) | MIPI-DSI, 2 lane @ 1500 Mbps | 800×800 / 720×720 (800×1280 max) | ❌ no | Waveshare [P4 3.4C](../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) and [4C](../devices/waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md) |
| [Sitronix ST7789VW](sitronix/st7789vw/README.md) | SPI | 240×240 (240×320 max) | ✅ yes | Espressif [P4X-EYE](../devices/espressif/esp32-p4x-eye/README.md) / [P4-EYE](../devices/espressif/esp32-p4-eye/README.md) |
| [Fitipower EK79007AD](fitipower/ek79007ad/README.md) | MIPI-DSI | 1024×600 | ❌ no | Espressif 7″ optional panel — **source driver + TCON** |
| [Fitipower EK73217BCGA](fitipower/ek73217bcga/README.md) | none (timing signals only) | up to 1200 gate outputs | — | Same panel — **gate driver**, the EK79007AD's companion |
| [Ilitek ILI9881C](ilitek/ili9881c/README.md) | MIPI-DSI | 800×1280 | ❌ no | Espressif P4 devkit panel, **chip rev v0.0** |

Three things in that table are easy to get wrong and are documented in the records:

- **JD9365 is Jadard, not Fitipower**, and a public datasheet **does** exist — though it omits the paged manufacturer registers where the init table lives. Register `0x40` is the horizontal-resolution selector; that is why it is the only byte differing between the 3.4C and 4C. [Details](jadard/jd9365/README.md#5--register-0x40--what-it-actually-is)
- **EK79007AD and EK73217BCGA are a pair**, not alternatives — a source driver and a gate driver for one panel. Neither works alone.
- **"ILI9981C" does not exist.** It is a transcription error for ILI9881C, still present in one device record and two guides. [Disproof](ilitek/ili9881c/README.md#-this-part-is-ili9881c-the-repository-called-it-ili9981c-that-part-does-not-exist)

Also display-related: [Sitronix ST77916](sitronix/st77916/README.md) (QSPI, 360×360 round) · [Sitronix ST7701S](sitronix/st7701s/README.md) · [SH8601 compatibility driver record](generic/sh8601-compatibility-driver/README.md) (a *software* artefact, not silicon) · [E Ink ED052TC4](e-ink/ed052tc4/README.md).

### All other records

| Record | Category |
|---|---|
| [OmniVision OV3660](omnivision/ov3660/README.md) | 3 MP (2048x1536) BSI CMOS image sensor, DVP — **current** sensor on the XIAO ESP32S3 Sense |
| [OmniVision OV2640](omnivision/ov2640/README.md) | 2 MP (1600x1200) CMOS image sensor, DVP — **discontinued**, early XIAO ESP32S3 Sense units |
| [OmniVision OV5640](omnivision/ov5640/README.md) | 5 MP (2592x1944) BSI CMOS image sensor with **autofocus**, DVP + MIPI |
| [GigaDevice GD25Q64E](gigadevice/gd25q64e/README.md) | 64 Mbit (8 MB) serial NOR flash — the XIAO ESP32S3 Sense application flash |
| [Hirose DF40C-30DP-0.4V(51)](hirose/df40c-30dp-0.4v/README.md) | 0.4 mm-pitch 30-contact board-to-board connector — the XIAO Sense daughterboard interface |
| [SG Micro SGM40567](sgmicro/sgm40567/README.md) | single-cell Li-ion linear charger, 4.2 V, resistor-programmed charge current |
| [SG Micro SGM6029](sgmicro/sgm6029/README.md) | buck-boost DC-DC, 3.3 V / 600 mA |
| [MEMSensing MSM261D3526H1CPM](memsensing/msm261d3526h1cpm/README.md) | mono PDM MEMS microphone — the XIAO ESP32S3 Sense mic, identified from the daughterboard BOM |
| [Espressif ESP32-P4](espressif/esp32-p4/README.md) | dual-core RISC-V high-performance application SoC with in-package PSRAM, MIPI-DSI/CSI, H.264 — **no radio** (retrieved 2026-08-21) |
| [Espressif ESP32-S3R8](espressif/esp32-s3r8/README.md) | dual-core wireless MCU/SoC with in-package PSRAM |
| [Espressif ESP32-U4WDH](espressif/esp32-u4wdh/README.md) | Wi-Fi + **Bluetooth Classic**/BLE MCU with embedded 4 MB flash (secondary MCU; core count unresolved) |
| [Winbond W25Q128JVPIQ](winbond/w25q128jv/README.md) | 128 Mbit (16 MB) serial NOR flash — the S3's application flash |
| [Sitronix ST77916](sitronix/st77916/README.md) | LCD display controller (**primary display record**; resolves the ST77916/SH8601 conflict) |
| [SH8601 compatibility driver record](generic/sh8601-compatibility-driver/README.md) | display-driver compatibility/conflict record |
| [Hynitron CST816D / CST816 family](hynitron/cst816d/README.md) | capacitive touch controller |
| [Texas Instruments PCM5100A](texas-instruments/pcm5100a/README.md) | stereo audio DAC, line level, no control bus |
| [Texas Instruments DRV2605L](texas-instruments/drv2605l/README.md) | haptic driver |
| [WCH CH445P](wch/ch445p/README.md) | quad 2:1 analog switch, audio-source mux (**datasheet and truth table now resolved**) |
| [MEMSensing MSM261D4030H1CPM](memsensing/msm261d4030h1cpm/README.md) | digital PDM MEMS microphone |
| [Texas Instruments TLV62569DBVT](texas-instruments/tlv62569dbvt/README.md) | 3.3 V step-down converter |
| [SGMicro SGM2036-3.3](sgmicro/sgm2036-3.3/README.md) | low-noise 3.3 V LDO |
| [AOS AO3400A](alpha-and-omega-semiconductor/ao3400a/README.md) | N-channel MOSFET |
| [Alps Alpine SSCM110100](alps-alpine/sscm110100/README.md) | directional/slide switch |
| [microSD / SDMMC interface](generic/micro-sd-sdmmc/README.md) | removable storage interface |
| [LRA vibration motor (unidentified)](generic/lra-motor/README.md) | linear resonant actuator |
| [LiPo 102035 battery (optional, maker unknown)](generic/lipo-102035/README.md) | 3.7 V lithium-polymer battery |
| [USB-UART bridge `U10` — **WCH CH340X**](wch/ch340x/README.md) | USB-to-UART converter (**identity resolved 2026-08-21**) |
| [Battery charger / power-path (unidentified)](generic/charger-power-path/README.md) | battery charging and power management function |
| [1.8-inch 360 x 360 LCD panel module (unidentified)](generic/lcd-panel-module/README.md) | round capacitive-touch TFT module |
| [2.4 GHz ceramic antennas (unidentified)](generic/ceramic-antenna/README.md) | onboard RF antennas |
| [USB-C target-selection interface](generic/usb-c-interface/README.md) | USB-C power/data interface |
| [3.5 mm stereo line output](generic/3.5mm-audio-output/README.md) | analog audio interface |
| [PH1.27 10-pin expansion connectors](generic/ph1.27-expansion-connectors/README.md) | board expansion interfaces |
| [Power button](generic/power-button/README.md) | device power control interface |
| [ESP32-S3 BOOT button](generic/esp32-s3-boot-button/README.md) | ESP32-S3 download-mode control interface |

---

## Related

- [Devices](../devices/README.md) — the boards these parts are fitted to
- [Vendor sourcing guides](../vendors/README.md) — per-manufacturer document retrieval
- [Espressif ecosystem map](../guides/espressif/ecosystem-and-product-lines.md) — choosing between ESP32 family parts
- [Clones and variants](../guides/markets/clones-and-variants.md) — when the fitted part is not the documented one
