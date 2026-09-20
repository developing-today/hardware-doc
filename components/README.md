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
| **Shanghai Awinic Technology** | — | [AW32901FCR](awinic/aw32901/README.md) · [AW35122FDR](awinic/aw35122/README.md) · [AW39112DNR](awinic/aw39112/README.md) · [AW9967DNR](awinic/aw9967/README.md) — *added 2026-09-01* |
| **Injoinic Technology** | — | [IP2315](injoinic/ip2315/README.md) — ⚠ I²C pins shared with the LED driver; see the record |
| **Joulwatt Technology** | — | [JW5712](joulwatt/jw5712/README.md) — ⚠ the public datasheet is a 4-page image-only scan |
| **Puya Semiconductor** | — | [PY32L020F15U6](puya/py32l020f15u6/README.md) — the silicon behind M5Stack's M5PM1 and M5IOE1 |
| **XMC (Wuhan Xinxin)** | — | [XM25UH128DHIQT](xmc/xm25uh128dhiqt/README.md) |
| **FocalTech Systems** | — | [FT6336G](focaltech/ft6336g/README.md) — ⚠ datasheet omits the I²C address and the register map |
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
| [Ebyte E22-900M22S](ebyte/e22-900m22s/README.md) | LoRa transceiver module — Semtech SX1262 plus PA, LNA, RF switch and matching, stamp-hole SMD. Tanmatsu `U23` |
| [Espressif ESP32-C6-WROOM-1-N8](espressif/esp32-c6-wroom-1/README.md) | Wi-Fi 6 / BLE 5.3 / IEEE 802.15.4 module |
| [Goodix GT9271](goodix/gt9271/README.md) | multi-point projected-capacitive touch controller, I²C — driven through the **GT911-compatible** driver API |
| [OPSCO SK6805-EC20](normand/sk6805-ec20/README.md) | 2020-package addressable RGB LED, NeoPixel-class single-wire, 2.0 × 2.0 mm. Filed under "Normand". Tanmatsu `U27`–`U32` |
| [Texas Instruments BQ25895](texas-instruments/bq25895/README.md) | single-cell Li-ion switch-mode charger — NVDC power path, ADC telemetry, 3.1 A boost (OTG). Tanmatsu `U15` |
| [Texas Instruments TPS63020](texas-instruments/tps63020/README.md) | single-inductor buck-boost, 4 A switches — holds output as input crosses it. Tanmatsu `U17` |
| [WCH CH32V203C8T6](wch/ch32v203c8t6/README.md) | 32-bit RISC-V microcontroller, LQFP-48 — always-on management coprocessor |
| [WCH CH334R](wch/ch334r/README.md) | 4-port USB 2.0 high-speed hub controller, QSOP-16. Tanmatsu `U5` |

---

## M5Stack PaperMono (SKU C153) and PaperMono-Lite

Records created **2026-09-01** from the published schematic PDF (`PaperMono_SCH_V0.6.2_20260522.pdf`), M5Stack's source repositories and the shipped factory firmware. No hardware was in the loop for any of them.

### Power chain

| Record | Category | Fitted as |
|---|---|---|
| [Awinic AW32901FCR](awinic/aw32901/README.md) | USB-input **OVP load switch with surge protection**, 5.95 V threshold, 120 V surge clamp | `U2`, sheet 2 |
| [Injoinic IP2315](injoinic/ip2315/README.md) | 1S Li-ion **synchronous buck charger** with input fast-charge protocols, I²C `0x75` | `U1`, sheet 2 |
| [Joulwatt JW5712](joulwatt/jw5712/README.md) | 600 mA **buck**, 360 nA I<sub>Q</sub> — produces `3V3_L2`, the main system rail | `U10`, sheet 2 |
| [SSP7615-33DFR](generic/ssp7615-33dfr/README.md) | 400 mA 3.3 V **LDO** (Shanghai Siproin) — **4 instances**: `3V3_L0`, `3V3_L1`, `3V3_L2_LoRa`, `EPD_3V3_L3B` | `U4`, `U6`, `U5`, `U9`, sheet 2 |
| [Awinic AW35122FDR](awinic/aw35122/README.md) | 1.5 A **load switch** — **4 instances**, the `L3B` domain: microSD, touch, microphone, NFC rails | `U8` · `U18` · `U21` · sheet-6 `U1` |
| [Awinic AW39112DNR](awinic/aw39112/README.md) | 2-bit **level translator / bus gate** — **2 instances**: the charger's I²C gate and the touch bus isolator | `U3`, sheet 2 · `U19`, sheet 4 |
| [Awinic AW9967DNR](awinic/aw9967/README.md) | Boost **WLED driver** — the e-paper frontlight, `BL_15V_L3B` | `U11`, sheet 2 |

### Compute, storage and clock

| Record | Category | Fitted as |
|---|---|---|
| [Espressif ESP32-S3R8](espressif/esp32-s3r8/README.md) | application SoC, 8 MB in-package octal PSRAM | `U12`, sheet 3 |
| [XMC XM25UH128DHIQT](xmc/xm25uh128dhiqt/README.md) | 128 Mbit (16 MB) SPI NOR flash — **resolves the board's QIO-vs-DIO documentation conflict** | `U13`, sheet 3 |
| [40 MHz crystal `CN4040M000157A530001`](generic/cn4040m000157a530001-40mhz-crystal/README.md) | ESP32-S3 main oscillator — ⚠ **no datasheet found** | `X1`, sheet 3 |
| [Puya PY32L020F15U6](puya/py32l020f15u6/README.md) | Cortex-M0+ MCU, 24 KB flash / 3 KB SRAM — **the silicon behind both M5Stack custom chips** | `U7` and `U17` |
| [M5Stack M5PM1](m5stack/m5pm1/README.md) | power-management coprocessor, I²C `0x6E` | `U7`, sheet 2 |
| [M5Stack M5IOE1](m5stack/m5ioe1/README.md) | I/O expander coprocessor, I²C `0x4F` | `U17`, sheet 4 |

### Human interface and sensing

| Record | Category | Fitted as |
|---|---|---|
| [FocalTech FT6336G](focaltech/ft6336g/README.md) | capacitive touch controller, I²C `0x38` — ⚠ effective area inset 5 px on every edge | on the touch FPC at `J4`, sheet 4 |
| [Bosch Sensortec BMI270](bosch-sensortec/bmi270/README.md) | 6-axis IMU, I²C `0x68`/`0x69` at 100 kHz — **`INT1` wakes the M5PM1 from full power-down** | `U15`, sheet 4 |
| [LMD4737T261-AC02](generic/lmd4737t261-ac02-pdm-microphone/README.md) | PDM MEMS microphone — ⚠ **no datasheet found**; ⚠ both signals on ESP32-S3 strapping pins | `U1`, sheet 5 |
| [RS-C1415MBAR](generic/rs-c1415mbar-rgb-led/README.md) | side RGB indicator — ⚠ **no datasheet found**; ⚠ **red is on/off only**, no PWM | `LED1`, sheet 5 |
| [DKE DEPG0397BBS770F3](dke/depg0397bbs770f3/README.md) | 3.97" 4-level-greyscale e-paper panel | FPC `J5`, sheet 4 |

### Display controller, radios and clock — *added 2026-09-01*

| Record | Category | Fitted as | On the Lite? |
|---|---|---|---|
| [Solomon Systech SSD1677](solomon-systech/ssd1677/README.md) | e-paper display driver + controller, 4-wire SPI — ⚠ the only mirror is **Rev 1.0, Nov 2018, "Advance Information"**, re-processed through `PDFill` | on the panel FPC at `J5`, sheet 4 | ✅ yes |
| [M5Stack Stamp LoRa-1262](m5stack/stamp-lora-1262/README.md) | plug-in LoRa module (Semtech SX1262), 868–923 MHz, FPC antenna — ⚠ **no module datasheet exists anywhere** | `U14`, sheet 4 | ❌ **no** |
| [Semtech SX1262](semtech/sx1262/README.md) | the transceiver inside that module; datasheet **Rev 2.2, Dec 2024** held at `semtech/sx1262/artifacts/` | inside `U14` | ❌ **no** |
| [STMicroelectronics ST25R3916](stmicroelectronics/st25r3916/README.md) | NFC reader/writer + card emulation, I²C `0x50`; datasheet **DS12484 Rev 8** held at `stmicroelectronics/st25r3916/artifacts/` | NFC sub-board, sheet 6 | ❌ **no** |
| [Seiko Epson RX8130CE](seiko-epson/rx8130ce/README.md) | RTC with alarm and timer, I²C `0x32` — **its interrupt wakes the M5PM1, not the ESP32-S3**; manual **ETM50E-09** held at `seiko-epson/rx8130ce/artifacts/` | `U16`, sheet 4 | ✅ yes |

> Records for all three were written on 2026-09-01 and the rows above link them.
> Their datasheets are hashed in
> [`devices/m5stack/papermono/sources.md`](../devices/m5stack/papermono/sources.md)
> (S22, S23, S24). Note the RX8130CE manual M5Stack mirrors is **Epson's English
> `ETM50E-09` served under a `_cn` filename** — `_cn` denotes Epson's China
> site, not a Chinese-language edition; no Chinese edition exists.

The **On the Lite?** column is the whole difference between the two SKUs: the
[PaperMono-Lite](../devices/m5stack/papermono-lite/README.md) drops NFC and LoRa
and nothing else. See that record for what does and does not carry over.

Three findings from this set are worth surfacing at index level because they are easy to hit and hard to diagnose:

- **The IP2315 charger is deliberately kept *off* the shared I²C bus** and connected only for the duration of a transaction. A bus scan will not find `0x75`. The reason is in the [IP2315 record](injoinic/ip2315/README.md#3--the-ic-pins-are-the-led-driver-pins--this-is-the-whole-hazard): its I²C pins are the battery-level LED driver pins, its mode selection depends on them being pulled to V<sub>BAT</sub>, and a read that fails to NACK its last byte can hold the bus.
- **M5GFX drives the frontlight dimming input at 5 kHz, below the AW9967's specified 10 kHz minimum.** [Details](awinic/aw9967/README.md#62--m5gfx-drives-the-dimming-input-at-half-the-datasheets-minimum-frequency). Both numbers are direct reads; the consequence is unmeasured.
- **The board is wired for QIO flash even though the shipped image says DIO.** All four data lines are routed and the flash ships with `QE = 1` set at the factory. [Resolution](xmc/xm25uh128dhiqt/README.md#5--resolving-the-qiodio-conflict).

Four parts on this board could not be attributed to a manufacturer despite systematic searching. Their records carry full search ledgers so the work is not repeated: the [crystal](generic/cn4040m000157a530001-40mhz-crystal/README.md#6-datasheet-search--negative-result), the [PDM microphone](generic/lmd4737t261-ac02-pdm-microphone/README.md#5-datasheet-search--negative-result) and the [RGB LED](generic/rs-c1415mbar-rgb-led/README.md#6-datasheet-search--negative-result); the [JW5712](joulwatt/jw5712/README.md#8-datasheet-status--read-this-before-relying-on-a-number-here) has a datasheet that is an image-only scan.

---

## Related

- [Devices](../devices/README.md) — the boards these parts are fitted to
- [Vendor sourcing guides](../vendors/README.md) — per-manufacturer document retrieval
- [Espressif ecosystem map](../guides/espressif/ecosystem-and-product-lines.md) — choosing between ESP32 family parts
- [Clones and variants](../guides/markets/clones-and-variants.md) — when the fitted part is not the documented one

---

## M5Stack PaperMono — component coverage completed *(added 2026-09-01)*

A **290-component, 230-designator census** of `PaperMono_SCH_V0.6.2_20260522.pdf`
is published as
[`devices/m5stack/papermono/bill-of-materials.md`](../devices/m5stack/papermono/bill-of-materials.md).
The sixteen records below close the gap between that census and this index. Every
one is schematic-derived; **no hardware was in the loop for any of them.**

### New manufacturers

| Manufacturer | Sourcing guide | Parts here |
|---|---|---|
| **Panasonic Industry** | — | [AXE512127D](panasonic/axe512127d/README.md) · [AXE612124D](panasonic/axe612124d/README.md) — an A4S 0.4 mm socket/header **pair** |
| **ROHM** | — | [RB162VAM-20TR](rohm/rb162vam-20tr/README.md) — ⚠ **Not Recommended for New Designs** |
| **Jiangsu Changjing (CJ)** | — | [CJ2310](changjing/cj2310/README.md) · [CJ3439KDW](changjing/cj3439kdw/README.md) |
| **XUNPU** | — | [TYPEC-302-BRP16SC08](generic/typec-302-brp16sc08/README.md) · [BTB0.408-10PLBDR-G41](generic/btb0.408-10plbdr-g41/README.md) — ⚠ the latter has **no datasheet at all** |
| **Shikues** | — | [SK2301AAT](generic/sk2301aat/README.md) · [SK2302AAT](generic/sk2302aat/README.md) |
| **TECH PUBLIC** | — | [ESD5311](generic/esd5311/README.md) |
| **YXC Crystal Oscillators** | — | [XL7EL89CMI-111YLC 27.12 MHz](generic/xl7el89cmi-111ylc-27.12mhz-crystal/README.md) |

### Connectors — published interfaces, so the pinouts are the point

| Record | Category | Fitted as | On the Lite? |
|---|---|---|---|
| [XUNPU TYPEC-302-BRP16SC08](generic/typec-302-brp16sc08/README.md) | USB-C 3.1 receptacle, 16 contacts, 5 A / **5 V** | **`USB`**, sheet 2 | ✅ yes |
| [FPC0.5-SMT-24P-B](generic/fpc0.5-smt-24p-b/README.md) | 24-way 0.5 mm FPC — the e-paper panel connector; **manufacturer unidentified** | `J5`, sheet 4 | ✅ yes |
| [Panasonic AXE512127D](panasonic/axe512127d/README.md) | A4S **socket**, 0.4 mm pitch, 12 contacts, 0.8 mm mated height | `J6`, sheet 4 | ✅ yes |
| [Panasonic AXE612124D](panasonic/axe612124d/README.md) | A4S **header** — the mating half | `J1`, sheet 5 | ✅ yes |
| [BTB0.408-10PLBDR-G41](generic/btb0.408-10plbdr-g41/README.md) | 0.4 mm board-to-board to the NFC sub-board, **both halves** | `J3` sheet 4 · `J1` sheet 6 | ❌ **no** |

### Protection and discretes

| Record | Category | Instances | On the Lite? |
|---|---|---|---|
| [ESD5311](generic/esd5311/README.md) | bidirectional ESD suppressor, 0.3 pF, DFN1006-2 | **12** — `TVS1`/`TVS2` (USB), `TVS3`–`TVS9` (microSD, **every line**), `DR1`–`DR3` (buttons) | ✅ yes |
| [Shikues SK2301AAT](generic/sk2301aat/README.md) | **P-channel** MOSFET, −20 V, SOT-523 | `Q5` sheet 2 — the USB-gated `VBAT_DET` high-side switch | ✅ yes |
| [Shikues SK2302AAT](generic/sk2302aat/README.md) | **N-channel** MOSFET, 20 V, SOT-523 | `Q2` sheet 2 (USB-presence inverter) · `Q3` sheet 4 (**buzzer driver**) | ✅ yes |
| [Changjing CJ2310](changjing/cj2310/README.md) | N-channel MOSFET, **60 V**, SOT-23 | `Q4` sheet 4 — the **e-paper bias-converter switch** | ✅ yes |
| [Changjing CJ3439KDW](changjing/cj3439kdw/README.md) | **complementary N+P pair**, SOT-363 | `Q1` sheet 2 — the **gated battery-sense divider** | ✅ yes |
| [ROHM RB162VAM-20TR](rohm/rb162vam-20tr/README.md) | Schottky, 20 V / 1 A, **ultra-low V<sub>F</sub> 0.36 V** | `D2` sheet 2 — frontlight boost rectifier | ✅ yes |
| [1N4148WS](generic/1n4148ws/README.md) | switching diode, SOD-323 | `D3` sheet 4 — buzzer flyback clamp | ✅ yes |
| [1N5819WS](generic/1n5819ws/README.md) | Schottky, 40 V / 1 A, SOD-323 | `D4`, `D5`, `D6` sheet 4 — e-paper boost + inverting charge pump | ✅ yes |

### Crystal, sensor and cell

| Record | Category | Fitted as | On the Lite? |
|---|---|---|---|
| [XL7EL89CMI-111YLC 27.12 MHz](generic/xl7el89cmi-111ylc-27.12mhz-crystal/README.md) | NFC carrier reference — **27.12 MHz = 2 × 13.56 MHz, fixed by ISO 14443** | `X1`, sheet 6 | ❌ **no** |
| [`100K-RNTC` thermistor](generic/100k-rntc-thermistor/README.md) | charger temperature qualification; **part unidentified, B constant unknown** | `R15`, sheet 2 | ✅ yes |
| [PaperMono 1150 mAh Li-ion cell](generic/papermono-1150mah-liion-cell/README.md) | the shipped battery; maker unidentified | at `J2`, sheet 2 | ✅ yes — **same capacity on both SKUs** |

### Five findings worth surfacing at index level

- **⚠ The NTC does not measure the cell.** `J2` is a **2-pin** connector carrying
  only + and −, and `100K-RNTC` is `R15`, a **mainboard** part on the charger's
  `NTC` pin. Several places in the device record say the battery is "NTC-sensed
  at `J2`"; the schematic does not support a thermistor in the pack. Recorded as
  a conflict, **not resolved** — `R15` may be thermally coupled to the cell by
  layout, which no schematic can show.
  [Detail](generic/100k-rntc-thermistor/README.md#4--conflict-this-does-not-measure-the-cell) ·
  [BOM §11](../devices/m5stack/papermono/bill-of-materials.md#11--conflict-raised-by-this-pass--the-ntc-does-not-measure-the-cell)
- **`R17` = 15 kΩ is on `ICHGSET`, `R18` = `NC` is on `LED3`** — resolving an
  open question in the [IP2315 record](injoinic/ip2315/README.md). The conflict it
  raises gets sharper, not softer: **15 kΩ is not a tabulated `ICHGSET` value.**
- **There is no `N1` gap, because there is no `N` series.** `CON2_SMD` (`J2`'s
  footprint label) and `PIN1`…`PIN24` (`J5`'s pin-name labels) are mis-read as
  markers by the Altium PDF parser. Separately, `pdftotext` **drops a glyph from
  eight `CO` markers on sheet 6**, hiding eight capacitors that are really there.
  Third, a designator with **no digits** — the USB-C receptacle is **`USB`**, not
  a second `U1` — is dropped by a `[A-Z]+[0-9]+` filter. The only genuine gaps on
  the whole board are **`R46`, `R48`, `R55`, `R56`, `R57`**.
  [Detail](../devices/m5stack/papermono/bill-of-materials.md#21--two-parser-artefacts-had-to-be-repaired--and-one-of-them-refutes-a-claim)
- **⚠ The two halves of the NFC board-to-board connector disagree about pin
  numbering** — `J3` puts every signal on an even pin, `J1` on an odd pin, and
  both carry the *same* part string. Taken literally, pin-for-pin mating would
  short 3V3 to ground. Unresolved; **do not assume `J3` pin *N* = `J1` pin *N***.
  [Detail](generic/btb0.408-10plbdr-g41/README.md#33--unresolved-conflict--the-two-halves-do-not-agree-on-pin-numbering)
- **USB-C has 5.1 kΩ R<sub>d</sub> on *both* CC lines** (`R4` on `CC1`, `R14` on
  `CC2`) while the IP2315's own CC pins are depopulated. Two independent reasons
  there is no USB-PD, plus a third: the AW32901 OVP trips at 5.95 V.
  [Detail](generic/typec-302-brp16sc08/README.md#32--the-cc-arrangement-a-plain-sink-and-no-usb-pd--twice-over)

### Retrieval note that will recur

**`www.lcsc.com/datasheet/*.pdf` returns HTTP 200 with `text/html`.** Five of the
nine datasheets acquired for this pass failed there and succeeded after a
mechanical host rewrite:

```
www.lcsc.com/datasheet/lcsc_datasheet_<stamp>_<name>_<code>.pdf
  ->  wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/<stamp>_<name>_<code>.pdf
```

**Check the `%PDF` magic bytes; neither the status code nor the `.pdf` extension
proves anything.** No user-agent rotation helps — it is the wrong host, not
bot-blocking. Also: **DuckDuckGo-lite, Mojeek and searx.be all blocked or
captcha'd `curl` on 2026-09-01**, and the only search channel that worked for
these Chinese-market discretes was **JLCPCB's SMT parts API**. ROHM's own CDN
404s for its NRND parts; **Octopart's mirror served the document under the same
numeric ID that IBS Electronics 403s on**. All of this belongs in
[`ai-crawler-site-access-table.md`](../ai-crawler-site-access-table.md).

**Three parts have no datasheet and no maker, and the search ledgers are
recorded so the work is not repeated:**
[`FPC0.5-SMT-24P-B`](generic/fpc0.5-smt-24p-b/README.md#5-datasheet-search--negative-result) (a library designation, not an orderable part),
[`BTB0.408-10PLBDR-G41`](generic/btb0.408-10plbdr-g41/README.md#5-datasheet-search--negative-result) (XUNPU identified, `dataManualUrl` is `None`),
and the [`100K-RNTC`](generic/100k-rntc-thermistor/README.md#11--100k-rntc-is-a-description-not-a-part-number) and
[1150 mAh cell](generic/papermono-1150mah-liion-cell/README.md#11-what-is-not-established), whose schematic strings carry no vendor token to search on.

---

## Waveshare ESP32-S3-ePaper-3.97 — component coverage *(added 2026-09-01)*

Six records reached from the
[ESP32-S3-ePaper-3.97](../devices/waveshare/esp32-s3-epaper-3.97/README.md) pass —
the knowledge base's first Waveshare **e-paper** board. Four are new, one is a stub
written over an artifact that had been sitting here unattached since 2026-08-23, and
one is an identity-only record with no datasheet yet.

### New manufacturers

| Manufacturer | Part | Datasheet held | Note |
|---|---|---|---|
| **X-Powers** | [AXP2101](x-powers/axp2101/README.md) | **V1.4 EN**, 1 554 740 B | Single-cell PMIC — charger, multi-rail regulator, power-key controller, backup-cell charger |
| **Sensirion** | [SHTC3](sensirion/shtc3/README.md) | yes, revision `unknown` | Humidity/temperature. **Fixed I²C address `0x70`** — two cannot share a bus |
| **Nsiway** | [NS4150B](nsiway/ns4150b/README.md) | **none — `reference-only`** | Class-D amplifier. Part number read from the schematic; *everything else about it is unestablished* |
| **Waveshare** *(as a part maker, not a board vendor)* | [3.97inch e-Paper panel](waveshare/3.97inch-e-paper/README.md) | **manual Rev 1.0, 2025-04-24** | The panel itself, filed as a component because it is sold standalone too |

### Extended or newly written

| Part | What changed |
|---|---|
| [ES8311](everest-semiconductor/es8311/README.md) | **New record.** Mono voice codec, joins the existing [ES8156](everest-semiconductor/es8156/README.md) |
| [QMI8658A](qst/qmi8658a/README.md) | **New stub over a pre-existing artifact.** The Rev A datasheet had been held since 2026-08-23 with no record page beside it |
| [SSD1677](solomon-systech/ssd1677/README.md) | Second **Used By** entry — a board from a *different vendor* with a *different panel supplier* at the same 3.97" size |
| [PCF85063A](nxp/pcf85063a/README.md) | Second **Used By** entry, plus a **second copy of the datasheet** |
| [ESP32-S3R8](espressif/esp32-s3r8/README.md) | Third **Used By** entry — fitted here as an `ESP32-S3-WROOM-1-N16R8` module |

### Four findings worth surfacing at index level

**1 — The vendor names a chip that does not appear to exist.** Waveshare's storefront
*and* its official documentation call the board's PMIC a **"TG28"**. The schematic
labels it **`AXP2101`** with X-Powers pin names throughout, and Waveshare's own
firmware drives it through XPowersLib's AXP2101 path. No datasheet or product page for
a "TG28" was found. **No `tg28` record was created** — that would be a part number
promoted from marketing copy.

**2 — Two 3.97-inch e-paper panels from different vendors match to 0.01 mm.**
[Waveshare's](waveshare/3.97inch-e-paper/README.md) and
[DKE's DEPG0397BBS770F3](dke/depg0397bbs770f3/README.md) share active area, DPI (235),
resolution and **the same SSD1677 controller**. Whether they are the same panel is
[unresolved](../devices/waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws8--is-this-the-same-panel-as-the-papermonos)
— Waveshare publishes no panel part number. The two manuals also state the
gate/source orientation **opposite ways round**.

**3 — A third confirmation that Waveshare's `common/` mirrors run stale.** Its
PCF85063A copy is **Rev. 6 (2015)** against NXP's **Rev. 7 (2018)** — different size,
different hash. Both kept. Always hash a `files.waveshare.com/wiki/common/` PDF
against the manufacturer's copy.

**4 — A panel datasheet with a text layer that lies.** The 3.97-inch manual embeds two
subset fonts at uniform code-point offsets (+29 and +26), so naive extraction produces
text that is *human-legible but wrong* — the most dangerous PDF failure mode. Decoded
and validated against a known cover heading before any value was transcribed; that is
what recovered `Driver IC: SSD1677`. Method and tooling in
[the device's `commands.md`](../devices/waveshare/esp32-s3-epaper-3.97/commands.md)
and [`vendors/waveshare` §9.3](../vendors/waveshare/README.md).

---

## Seven-pass component sweep *(added 2026-09-04 — 2026-09-07)*

Records added by the Xteink, M5Stack DinMeter, M5Stack Cardputer, M5Stack LoRa-expansion,
LilyGO T-Display K230, LilyGO T-Display-S3 and LoRa-generation-lineage passes. **No hardware
was in the loop for any of them**; every claim is schematic-, datasheet- or source-derived.
Where two passes reached the same manufacturer the entry below is merged.

### New manufacturers

| Manufacturer | Sourcing guide | Parts here |
|---|---|---|
| **UltraChip** | — | [UC8253](ultrachip/uc8253/README.md) · [UC8179](ultrachip/uc8179/README.md) · [UC8279](ultrachip/uc8279/README.md) — e-paper display controllers |
| **CellWise** | — | [CW2017](cellwise/cw2017/README.md) — battery fuel gauge |
| **Canaan Creative (Kendryte)** | [vendors/canaan](../vendors/canaan/README.md) | [K230](canaan/k230/README.md) — RISC-V AIoT SoC. **This repository's first RISC-V part** |
| **Raydium Semiconductor** | — | [RM69A10](raydium/rm69a10/README.md) · [RM67162](raydium/rm67162/README.md) · [RM690B0](raydium/rm690b0/README.md) — AMOLED display drivers |
| **GalaxyCore** | — | [GC2093](galaxycore/gc2093/README.md) — CMOS image sensor |
| **Realtek Semiconductor** | — | [RTL8189FS](realtek/rtl8189fs/README.md) · [RTL8152B](realtek/rtl8152b/README.md) — Wi-Fi and USB Ethernet |
| **Nordic Semiconductor** | — | [nRF52840](nordic-semiconductor/nrf52840/README.md) · [nRF9151](nordic-semiconductor/nrf9151/README.md) — BLE and cellular IoT |
| **ASAIR / Guangzhou Aosong** | — | [AHT20](asair/aht20/README.md) — environmental sensor |
| **Lontium Semiconductor** | — | [LT9611](lontium/lt9611/README.md) — display bridge |
| **AXS Technology** | — | [AXS15231B](axs-technology/axs15231b/README.md) — display driver **and** touch controller in one die |
| **Chipone** | — | [CO5300](chipone/co5300/README.md) — AMOLED driver, also referenced as ICNA3311 |
| **Shenghe Microelectronics** | — | [SH8601Z](shenghe-microelectronics/sh8601z/README.md) · [SH8501B](shenghe-microelectronics/sh8501b/README.md) — **settles who makes the SH86xx parts** |
| **Nanjing Top Power** | — | [TP4065](nanjing-top-power/tp4065/README.md) — linear Li-ion charger |
| **Semtech** | [vendors/semtech](../vendors/semtech/README.md) | six new transceiver records — see *LoRa silicon generations* below |
| **M5Stack** *(as a module maker)* | [vendors/m5stack](../vendors/m5stack/README.md) | [Stamp-S3](m5stack/stamp-s3/README.md) · [Stamp-S3A](m5stack/stamp-s3a/README.md) |
| **Microne** | — | [ME3116AM6G](microne/me3116am6g/README.md) — 6–36 V → 5 V buck. ⚠ schematic-only, **no datasheet located** |
| **Belling** | — | [BL8075CB5TR33](belling/bl8075/README.md) — 3.3 V LDO. ⚠ schematic-only |
| **Murata** | — | [MUN3CAD01-SC](murata/mun3cad01-sc/README.md) — 1 A µPOL module, the Stamp-S3's regulator |
| **Knowles** | — | [SPM1423HM4H-B](knowles/spm1423hm4h-b/README.md) — PDM MEMS microphone |
| **Worldsemi** | — | [WS2812](worldsemi/ws2812/README.md) — addressable RGB LED |
| **Consonance** *(inferred)* | — | [CN809](consonance/cn809/README.md) — voltage supervisor / reset generator |
| **NSIWAY** | — | [NS4168](nsiway/ns4168/README.md) — I²S-input class-D amplifier |
| **ZhongKeWei** | — | [ATGM336H-6N](zhongkewei/atgm336h-6n/README.md) · [AT6668](zhongkewei/at6668/README.md) — GNSS module and the chipset inside it |
| **Infineon** | — | [BGS13SN8](infineon/bgs13sn8/README.md) — SP3T RF switch |
| **Ebyte** | — | [E220 series](ebyte/e220-400t22s/README.md) — LLCC68 **UART modem** modules |

### Xteink pocket e-readers — *added 2026-09-04*

| Part | Where |
|---|---|
| [`ultrachip/uc8253`](ultrachip/uc8253/README.md) | Xteink X3, original production |
| [`ultrachip/uc8179`](ultrachip/uc8179/README.md) | Xteink X4 / X4 Pro / X4 Classic, newer batches |
| [`ultrachip/uc8279`](ultrachip/uc8279/README.md) | Xteink X3 (as UC8279d) and the X4 family; EEGO A4 as UC8279C |
| [`cellwise/cw2017`](cellwise/cw2017/README.md) | Xteink X4 Pro, X4 Classic |
| [`espressif/esp32-c3`](espressif/esp32-c3/README.md) | Xteink X3, X4. **Family-level identification only** — the exact package variant has never been read |
| [`texas-instruments/bq27220`](texas-instruments/bq27220/README.md) | Xteink X3. The family's best battery instrumentation — no profile upload needed |
| [`unidentified/xteink-x3-x4/`](unidentified/xteink-x3-x4/README.md) | Four evidenced-but-unidentified parts on the ESP32-C3 Xteink boards: a Puya 128 Mbit flash, a DS-series RTC (**three sources disagree**), an ISO 14443A NFC tag (**purpose established, part not**), and a TP4056-class charger |

Family trait worth knowing: **UC81xx parts answer `VER (0x70)` and `FLG (0x71)` register reads;
the Solomon Systech SSD16xx family does not.** That asymmetry is what makes runtime
panel-controller detection possible on boards shipping more than one variant. And the CW2017
**reports 0 % until the host uploads an 80-byte BATINFO profile**, and has **no current
register**, so charge state must come from a separate GPIO.

### M5Stack DinMeter (K134 / K134-V11) — *added 2026-09-04*

| Part | Record | Function |
|---|---|---|
| **Stamp-S3** | [`m5stack/stamp-s3`](m5stack/stamp-s3/README.md) | ESP32-S3FN8 core module, SKU `S007`, board rev v0.2. 8 MB flash, **no PSRAM**, 23 GPIOs, USB-C, WS2812B-2020 on GPIO21, rear 8/12-pin LCD FPC. **`[EOL]`** |
| **Stamp-S3A** | [`m5stack/stamp-s3a`](m5stack/stamp-s3a/README.md) | The successor, SKU `S007-V033`, board rev **v0.3.3**. Same SoC/flash/PSRAM/pinout; new regulator, rebuilt antenna match, and the **RGB LED moved to a switched rail needing GPIO38** |
| **ST7789V2** | [`sitronix/st7789v2`](sitronix/st7789v2/README.md) | 240×320 TFT controller; the DinMeter's 1.14" 135×240 panel. Datasheet v1.0 (2016/11) retained. GRAM gap +52/+40, `INVON` required |
| **ST7789P3** | [`sitronix/st7789p3`](sitronix/st7789p3/README.md) | DinMeter v1.1's controller. ⚠ **No datasheet exists anywhere**; command-compatibility with ST7789V2 is inferred, not verified |
| **BM8563** | [`generic/bm8563`](generic/bm8563/README.md) | I²C RTC, 0x51, PCF8563-equivalent. CN-only datasheet — and it carries a stray `MAX1937` string, i.e. a derived document |
| **TP4057** | [`generic/tp4057`](generic/tp4057/README.md) | 500 mA linear Li-ion charger, SOT23-6, **4.24 V float** |
| **ME3116AM6G** | [`microne/me3116am6g`](microne/me3116am6g/README.md) | 6–36 V → 5 V buck. ⚠ Schematic-only; **no datasheet located** |
| **SY7088** | [`silergy/sy7088`](silergy/sy7088/README.md) | Battery → 5 V boost. ⚠ Schematic-only. Its own divider computes to **≈5.38 V** against a "5 V" spec |
| **BL8075CB5TR33** | [`belling/bl8075`](belling/bl8075/README.md) | 3.3 V LDO. ⚠ Schematic-only |
| **MUN3CAD01-SC** | [`murata/mun3cad01-sc`](murata/mun3cad01-sc/README.md) | 1 A µPOL module — the **Stamp-S3's** regulator. ⚠ Still listed on the Stamp-S3**A** page, where it is not fitted |
| **SGM2578** | [`sgmicro/sgm2578`](sgmicro/sgm2578/README.md) | Load switch, Stamp-S3 backlight rail. ⚠ Schematic-only |
| [`unidentified/m5stack-dinmeter/rotary-encoder`](unidentified/m5stack-dinmeter/rotary-encoder/README.md) | — | **The orange knob.** No part number in the schematic or on either product page. Quadrature GPIO41/40 + switch GPIO42 on a 7-pad connector `J5` |
| [`unidentified/m5stack-dinmeter/buzzer`](unidentified/m5stack-dinmeter/buzzer/README.md) | — | `LS1` carries no part number or value. Magnetic (flyback diode fitted), passive, GPIO3 via an SS8050 |
| [`unidentified/m5stack-stamp-s3a/dcdc-u4`](unidentified/m5stack-stamp-s3a/dcdc-u4/README.md) | — | The Stamp-S3A's regulator. 8 balls, `IOUT: 0~0.6A`, external 2.2 µH inductor. ⚠ **A later pass identifies this as a [JoulWatt JW5712](joulwatt/jw5712/README.md)** — see [`scratch/index-merge/corrections-requiring-review.md`](../scratch/index-merge/corrections-requiring-review.md) |

### M5Stack Cardputer family — *added 2026-09-04*

| Part | Manufacturer | Function | Used by |
|---|---|---|---|
| [TCA8418](texas-instruments/tca8418/README.md) | Texas Instruments | I²C keypad scanner, 8×10 matrix, event FIFO | Cardputer ADV (`0x34`, 7×8), CardputerZero (`0x34`, 46 keys) |
| [74HC138](generic/74hc138/README.md) | generic logic | 3-to-8 decoder used as a keyboard column driver | Cardputer v1.0, v1.1 |
| [ESP32-S3FN8](espressif/esp32-s3fn8/README.md) | Espressif | ESP32-S3 with 8 MB in-package flash and **no PSRAM** | Stamp-S3 / Stamp-S3A, all ESP32 Cardputers |
| [MSM381A3729H9BP](memsensing/msm381a3729h9bp/README.md) | MEMSensing | analog MEMS microphone | Cardputer ADV |
| [SPM1423HM4H-B](knowles/spm1423hm4h-b/README.md) | Knowles | PDM MEMS microphone | Cardputer v1.0, v1.1 |
| [NS4168](nsiway/ns4168/README.md) | NSIWAY | I²S-input class-D amplifier | Cardputer v1.0, v1.1 |
| [WS2812](worldsemi/ws2812/README.md) | Worldsemi | addressable RGB LED | Stamp-S3, Stamp-S3A |
| [CN809](consonance/cn809/README.md) | Consonance (*inferred*) | voltage supervisor / reset generator | all Cardputer mainboards |
| [SY8089](silergy/sy8089/README.md) | Silergy | 2 A synchronous buck, the 3.3 V rail | all Cardputer mainboards |
| [LP3218DT1G](unidentified/cardputer/lp3218dt1g/README.md) | **unidentified** | power-path MOSFET ×3 | all Cardputer mainboards |

### M5Stack LoRa, sub-GHz and NFC expansions — *added 2026-09-04*

| Record | Category |
|---|---|
| [Texas Instruments CC1101](texas-instruments/cc1101/README.md) | Sub-1 GHz FSK/OOK transceiver, QFN-20. Datasheet held (M5Stack mirror) |
| [ST STM32WLE5](stmicroelectronics/stm32wle5/README.md) | Cortex-M4 + Semtech sub-GHz radio on one die; used as an AT-command LoRaWAN modem |
| [ZhongKeWei ATGM336H-6N](zhongkewei/atgm336h-6n/README.md) | 18-pad multi-constellation GNSS module. Datasheet held (M5Stack mirror) |
| [ZhongKeWei AT6668](zhongkewei/at6668/README.md) | The chipset inside the ATGM336H; CASIC binary protocol (spec archived) |
| [Diodes PI4IOE5V6408](diodes-incorporated/pi4ioe5v6408/README.md) | I²C GPIO expander @ 0x43 — controls the RF switch on three M5Stack LoRa products |
| [Analog Devices MAX2659](analog-devices/max2659/README.md) | GNSS low-noise amplifier |
| [Infineon BGS13SN8](infineon/bgs13sn8/README.md) | SP3T RF switch — two of them do the Cap CC1101's band selection |
| [Ebyte E220 series](ebyte/e220-400t22s/README.md) | LLCC68 **UART modem** modules — explicitly *not* SPI-attached, therefore not Meshtastic-capable |
| [RF balun B0310J50100AHF](generic/rf-balun-b0310j50100ahf/README.md) | Wideband balun on the CC1101's differential port — manufacturer unidentified |
| [GNSS ceramic patch antenna (ANT1818-04)](generic/gnss-ceramic-patch-antenna/README.md) | 18×18×4 mm L1 patch — distinct from the 2.4 GHz `generic/ceramic-antenna` record |
| [RP-SMA vs SMA antenna connectors](generic/rp-sma-and-sma-antenna-connectors/README.md) | The `SMA-KE` designation, and M5Stack's unresolved self-contradiction about Cap connectors |

Five **existing** records were extended rather than added by that pass: `semtech/sx1262` (four
new Used By entries and the **1.8 V vs 3.0 V TCXO conflict**), `m5stack/stamp-lora-1262` (§6A
names module pins 11–13 `GND`/`ANT`/`GND`, and a module schematic is now held),
`stmicroelectronics/st25r3916` (the same chip strapped to **SPI** rather than I²C),
`joulwatt/jw5712` (the **same regulator, host-enabled on one Cap and always-on on the other**)
and `generic/xl7el89cmi-111ylc-27.12mhz-crystal`.

### LoRa silicon generations — Semtech — *added 2026-09-04*

Six new records under `components/semtech/`, supporting
[`guides/hardware/lora-radio-generations.md`](../guides/hardware/lora-radio-generations.md).

| Record | Category |
|---|---|
| [`semtech/lr2021`](semtech/lr2021/README.md) | **LoRa Plus™ LR2021 — the fourth-generation LoRa transceiver.** Dual-band (150–960 MHz + 1.5–2.5 GHz), FLRC to 2.6 Mbps, multi-SF receive, BLE/802.15.4/Z-Wave/Sigfox PHYs, SATCOM. ⚠ Not a drop-in for anything: 16-bit opcodes, 24-bit registers, two FIFOs, mandatory boot-time PRAM upload |
| [`semtech/lr1121`](semtech/lr1121/README.md) | Gen 3, LoRa Connect. Multi-band + **AES-128 crypto engine and secure key store**. ⚠ **No GNSS or Wi-Fi scanner** despite the LoRa Edge part number — light record, datasheet gated |
| [`semtech/lr11x0`](semtech/lr11x0/README.md) | Gen 3, LoRa Edge — **LR1110 and LR1120**. GNSS + passive Wi-Fi scanning, resolved by a **cloud solver**, plus the crypto engine. Light record, datasheet gated |
| [`semtech/sx1276`](semtech/sx1276/README.md) | **Gen 1 (2013).** Register-mapped SPI, no `BUSY`, two overlapping register maps. The *before* picture for the SX127x → SX126x break. Rev 5 datasheet + both errata notes retained |
| [`semtech/llcc68`](semtech/llcc68/README.md) | Gen 2, **pin-to-pin compatible with the SX1262** — ⚠ and 19 dB worse link budget. **Cannot do SF12 at all**; no bandwidth below 100 kHz. The real substitution trap |
| [`semtech/sx1268`](semtech/sx1268/README.md) | Gen 2, pin-compatible with the SX1262, ⚠ **410–810 MHz only** — 868 and 915 MHz are out of range |

⚠ **The LR2021's interrupt DIO is `DIO11`, not `DIO1`.** Firmware that hard-codes `DIO1`
silently sees no interrupts on an LR2021 board — which matters because at least one board
([LilyGO T-Display K230](../devices/lilygo/t-display-k230/README.md)) ships either radio on the
same host GPIO. **No board documented here uses the LR2021 as its default radio yet.**

### LilyGO T-Display K230 — *added 2026-09-04*

| Record | Note |
|---|---|
| [`canaan/k230`](canaan/k230/README.md) | Kendryte K230 RISC-V AIoT SoC — **this repository's first RISC-V part** |
| [`raydium/rm69a10`](raydium/rm69a10/README.md) | 4.1″ AMOLED display driver |
| [`galaxycore/gc2093`](galaxycore/gc2093/README.md) | 2 MP MIPI CMOS image sensor |
| [`realtek/rtl8189fs`](realtek/rtl8189fs/README.md) · [`realtek/rtl8152b`](realtek/rtl8152b/README.md) | SDIO Wi-Fi and USB Ethernet |
| [`nordic-semiconductor/nrf52840`](nordic-semiconductor/nrf52840/README.md) · [`nordic-semiconductor/nrf9151`](nordic-semiconductor/nrf9151/README.md) | BLE companion, and the LTE-M/GNSS modem on the keyboard base |
| [`asair/aht20`](asair/aht20/README.md) | Temperature/humidity sensor at `0x38` on the base board's I²C4 |
| [`lontium/lt9611`](lontium/lt9611/README.md) | MIPI-DSI → HDMI bridge |
| [`goodix/gt9895`](goodix/gt9895/README.md) | Goodix "Berlin" touch controller. **Not** compatible with the GT911/GT9271 driver |
| [`texas-instruments/bq25896`](texas-instruments/bq25896/README.md) | I²C charger; **sibling of the existing BQ25895, not the same part** |
| [`analog-devices/max98357a`](analog-devices/max98357a/README.md) | I²S Class-D amplifier |
| [`xlsemi/xl9555`](xlsemi/xl9555/README.md) | 16-bit I²C GPIO expander. **README added 2026-09-04** over an `artifacts/` directory that predates the pass |
| [`unidentified/t-display-k230`](unidentified/t-display-k230/README.md) | Six unresolved parts on that board |

⚠ **`espressif/esp32-s3r8` was deliberately *not* given a Used-By row for this board**, even
though LilyGO's wiki claims an ESP32-S3-R8 co-processor. The claim is unverified and
contradicted by the board's own BSP; see that device record's `GC-2`.

### LilyGO T-Display-S3 family — *added 2026-09-07*

| Record | Category | Used by | Note |
|---|---|---|---|
| [AXS Technology AXS15231B](axs-technology/axs15231b/README.md) | combined AMOLED/LCD driver **and** capacitive touch controller in one die; QSPI + I²C `0x3B` | LilyGO T-Display-S3 Long | ⚠ datasheet carries an explicit no-redistribution notice — keep unstaged |
| [Chipone CO5300](chipone/co5300/README.md) | AMOLED driver, QSPI; also referenced as ICNA3311 | LilyGO 1.64″ / 1.43″ / 1.75″ AMOLED | datasheet **archived** (12.6 MiB) with placeholder |
| [Raydium RM67162](raydium/rm67162/README.md) | 240×536 AMOLED driver, QSPI | LilyGO T-Display-S3 AMOLED, AMOLED Plus | |
| [Raydium RM690B0](raydium/rm690b0/README.md) | 480×600 AMOLED driver, QSPI | LilyGO T4-S3 | |
| [Shenghe SH8601Z](shenghe-microelectronics/sh8601z/README.md) | 480×480 AMOLED driver | LilyGO 1.43″ AMOLED (`DO0143FAT01`) | ⚠ marked CONFIDENTIAL — keep unstaged. **Settles who makes the SH86xx parts** |
| [Shenghe SH8501B](shenghe-microelectronics/sh8501b/README.md) | 240-column AMOLED driver, 1.8 V | LilyGO T-Display AMOLED Lite | ⚠ marked CONFIDENTIAL — keep unstaged |
| [Sitronix ST7789V](sitronix/st7789v/README.md) | 240×320 TFT controller; 8-bit Intel-8080 here | LilyGO T-Display-S3 / Touch | |
| [Sitronix ST7796S](sitronix/st7796s/README.md) | 320×480 TFT controller, 4-wire SPI | LilyGO T-Display-S3 Pro | ⚠ vendor README says ST7796**U** — unresolved |
| [Hynitron CST328](hynitron/cst328/README.md) | mutual-capacitance touch, I²C `0x1A` | LilyGO T-Display-S3 Touch (later) | Chinese-only datasheet ⇒ **primary source** |
| [Hynitron CST3530](hynitron/cst3530/README.md) | capacitive touch, I²C | LilyGO T-Display-S3 Long (later) | address unknown |
| [Hynitron CST226SE](hynitron/cst226se/README.md) | multi-point touch, I²C `0x5A` | LilyGO T-Display-S3 Pro, T4-S3 | no datasheet obtained |
| [FocalTech FT3168](focaltech/ft3168/README.md) | capacitive touch for small AMOLED, I²C | LilyGO 1.64″ / 1.43″ AMOLED | address not verified |
| [Silergy SY6970](silergy/sy6970/README.md) | I²C switch-mode Li-ion charger/PMIC with OTG + ADC, `0x6A` | LilyGO Long, Pro, T4-S3, 1.64″, 1.43/1.75″ | |
| [Awinic AW9364](awinic/aw9364/README.md) | 4-channel LED backlight boost, one-wire brightness | LilyGO T-Display-S3 | **no datasheet located** |
| [TP4065 (charger, as documented)](nanjing-top-power/tp4065/README.md) | linear Li-ion charger | LilyGO T-Display-S3, 1.91″ AMOLED | ⚠ **schematic disagrees with a shipping board** |
| [Diodes AP2112K-3.3](diodes-incorporated/ap2112k/README.md) | 600 mA 3.3 V LDO; RT9013 named as a second source | LilyGO T-Display-S3 | |
| [Bosch BHI260AP](bosch-sensortec/bhi260ap/README.md) | 6-axis IMU + Fuser2 sensor-hub core | LilyGO T-Display-S3 Pro (**some units**) | |
| [MEMSensing MSM261S4030H0R](memsensing/msm261s4030h0r/README.md) | MEMS microphone | LilyGO T-Display-S3 Pro MVSRBoard | datasheet retained, not read |
| [NXP PCF8563](nxp/pcf8563/README.md) | I²C RTC | LilyGO 1.43″/1.75″ AMOLED | **record created to fill a gap** — the artifact existed with no README |
| [Unidentified `AXPM65611` / `65b311`](unidentified/lilygo-t-display-s3-family/axpm65611/README.md) | unknown; probably an AMOLED bipolar supply and/or the real charger | LilyGO AMOLED, AMOLED Plus, T-Display-S3 | records what would resolve it |

Ten existing records gained a **Used By** row from the same pass, each preceded by an `mmin -30`
check: `espressif/esp32-s3r8` · `winbond/w25q128jv` · `hynitron/cst816d` · `silergy/sy8089` ·
`texas-instruments/bq25896` · `nxp/pcf85063a` · `x-powers/axp2101` · `chipsemi/chsc5816` ·
`lite-on/ltr-553als-01` · `analog-devices/max98357a`.

> **Merge note, 2026-09-07.** The LilyGO T-Display-S3 fragment
> (`scratch/lilygo-t-display-s3/index-fragments.md`, SHA-256 `2f3acf08…`) was still being
> written when this index was updated. The rows above are as that fragment stood at 06:23;
> re-diff it before treating this section as final. See
> [`scratch/index-merge/README.md`](../scratch/index-merge/README.md).

### One pre-existing defect, reported not repaired

`components/generic/bm8563/README.md` contains **two links to `../../nxp/pcf8563/README.md`**.
That record **now exists** (created by the T-Display-S3 pass on 2026-09-07), so the links
resolve — but they were broken when the Xteink pass reported them on 2026-09-04, and
[`nxp/pcf85063a/README.md`](nxp/pcf85063a/README.md) still flags the directory as
*"Artifacts-only directory; no record page yet"*. Both are logged in
[`scratch/index-merge/corrections-requiring-review.md`](../scratch/index-merge/corrections-requiring-review.md).

## Round-two component work *(added 2026-09-11)*

Three sessions ran on 2026-09-11 — Xteink round two, schematic net-tracing, and certification /
market. This section indexes what they produced. It is **additive to** the seven-pass sweep
section above; no row there was changed.

### One new record

| Record | Category | Used by | Note |
|---|---|---|---|
| [Shenzhen Jinhangbiao KH3216-A35](generic/kh3216-a35-chip-antenna/README.md) | 2.4 GHz SMD chip antenna — **2.30 dBi peak, VSWR ≤ 2.0, 50 Ω** | [Xteink X4 Classic](../devices/xteink/x4-classic/README.md) | ⚠ **Identified from an FCC exhibit, not a vendor datasheet.** The source document is the `2BTR9-X4C` antenna report, so the part's identity, integrity and parameters rest on a test-lab filing — see the record's own caveat. It is the **first antenna part in this library identified from a regulatory record** |

### Datasheets acquired for existing records

Five records that previously had no primary document now have one. Each was magic-byte
validated; the record carries the hash.

| Record | Acquired |
|---|---|
| [`ultrachip/uc8253`](ultrachip/uc8253/README.md) | datasheet `UC8253c_A` rev 0.6 (2020-10-13), 1,294,916 B, `bee25538…` — ⚠ cover marked *"for TFT module use only"*, a **use restriction of unclear scope**, not a licence. Kept **unstaged** |
| [`ultrachip/uc8179`](ultrachip/uc8179/README.md) | datasheet `UC8179c_C` rev 0.6 (2019-11-26), 1,202,516 B, `bf1dcef7…` — same marking, same treatment |
| [`espressif/esp32-c3`](espressif/esp32-c3/README.md) | datasheet **v2.4**, 900,158 B, `833fc000…` |
| [`texas-instruments/bq27220`](texas-instruments/bq27220/README.md) | datasheet `SLUSCB7A` Rev A **and** technical reference manual `SLUUBD4` Rev A — this closes the acquisition gap the schematic-tracing pass flagged for the sibling TCA8418 |
| [`goodix/gt911`](goodix/gt911/README.md) | **Programming Guide Rev.00**, 477,454 B, `60c6c228…` — ⚠⚠ **page 1 reads *"GOODIX CONFIDENTIAL … Reproduction and/or distribution … is strictly prohibited without written consent of GOODIX."*** Redistribution status **`prohibited` as written**. Held **unstaged pending a user decision** |

Two records still have **no datasheet**, and both absences were re-tested rather than assumed:

- [`ultrachip/uc8279`](ultrachip/uc8279/README.md) — **12 sources tried, all failed.** The record lists them.
- [`cellwise/cw2017`](cellwise/cw2017/README.md) — no datasheet, **and the part is not in CellWise's public catalogue at all.** That is a stronger negative than a failed download.

### `unidentified/*` — three resolved or advanced, none deleted

**No `components/unidentified/*` record was deleted, and none should be.** Other records link to
them, and they are the stable landing place for a search on the unknown string.

| Record | Status after round two | Points at |
|---|---|---|
| [`unidentified/m5stack-stamp-s3a/dcdc-u4`](unidentified/m5stack-stamp-s3a/dcdc-u4/README.md) | ✅ **Resolved — the sheet prints `JW5712`.** Retained for linkage | [`joulwatt/jw5712`](joulwatt/jw5712/README.md), which already existed with a datasheet |
| [`unidentified/lilygo-t-display-s3-family/axpm65611`](unidentified/lilygo-t-display-s3-family/axpm65611/README.md) | ⚠ **Function established, identity still unknown.** Better described as *"AMOLED bipolar display-bias supply, 12-pin, manufacturer unknown"* than as *"unidentified"* | no real record possible — `components/<manufacturer>/<part>/` cannot be created without a manufacturer |
| [`unidentified/m5stack-dinmeter/rotary-encoder`](unidentified/m5stack-dinmeter/rotary-encoder/README.md) | topology established — 5-terminal, A/COM/B plus switch; identity unknown | — |
| [`unidentified/m5stack-dinmeter/buzzer`](unidentified/m5stack-dinmeter/buzzer/README.md) | topology established — magnetic, AC-coupled drive; identity unknown | — |
| [`unidentified/xteink-x3-x4`](unidentified/xteink-x3-x4/README.md) | extended by the Xteink round-two pass | — |

⚠ **The `dcdc-u4` row in the seven-pass section above carries a `⚠` pointing at
[`corrections-requiring-review.md`](../scratch/index-merge/corrections-requiring-review.md).**
It is now **adjudicated**: the part is `JW5712`, the schematic PNG was re-fetched and
hash-matched, and two sessions agree independently — the certification/market pass in
[`corrections-adjudicated.md` §1](../scratch/index-merge/corrections-adjudicated.md) and the
schematic-tracing pass from the sheet text. The original row is unchanged.

[`joulwatt/jw5712`](joulwatt/jw5712/README.md) accordingly deserves **three** *Used by* rows —
`components/m5stack/stamp-s3a` (`U4`), [`devices/m5stack/cap-lora-1262`](../devices/m5stack/cap-lora-1262/README.md) (`U3`)
and [`devices/m5stack/cap-cc1101`](../devices/m5stack/cap-cc1101/README.md) (`U1`). Three M5Stack
boards fit the same part. ⚠ That record's datasheet is a **raster scan** — 4 pages, one full-page
image each, `pdftotext` yields 0 words — so it cannot be text-searched and OCR would be needed
for any register or parametric work. The `-scanned` filename suffix is accurate.

### Named on a schematic, no record yet

The net-tracing pass read these part numbers directly off vendor sheets but did not create
records, because none of the boards fitting them was in its scope. Listed so the next reader does
not re-derive them. **Create one only when working the relevant board.**

| Part | Fitted as | Source sheet |
|---|---|---|
| `PI4IOE5V6408ZTAEX` I²C GPIO expander · `MAX2659` GNSS LNA · `GP-02` GNSS module | `U2` · `U1` · `M2` | Cap LoRa-1262 `U214_SCH_V1.1_20251029` |
| `BL8075CB5TR33` 3.3 V regulator · `ME3116AM6G` wide-input buck · `CN809J` reset supervisor · `AP40P05` P-FET · `LN2324DT2AG` | `U4` · `U1` · `U7` · `Q3`/`Q6` · `Q4` | DinMeter `K134_DIN_Meter_v1.0` |
| `AW9364DNR` backlight boost · `AP2112K-3.3V` / `RT9013` LDO | `U4` · `U7` | `T_Display_S3.pdf` |
| `MSM381A3729H9BPC` PDM microphone · `PESDNC2FD3V3B` / `PESDNC2FD5VB` ESD arrays | `U8` · `D6`–`D8` | Cardputer ADV sheets 3 and 1 |
| `DFP252012TF-100M` 10 µH inductor | `L6`/`L7`, `L3`/`L4` | the AMOLED sheets |

A [`belling/bl8075`](belling/bl8075/README.md) record **does** now exist, written by the Xteink
round-two pass for a different board.

### Two findings for records this pass did not own

- ⚠ [`nanjing-top-power/tp4065`](nanjing-top-power/tp4065/README.md) — **the schematic symbol is
  5-pin, not SOP-8.** If that record states or implies SOP-8 it needs a dated correction. **Not
  applied** — outside every round-two session's scope. Flagged in
  [`corrections-requiring-review.md`](../scratch/index-merge/corrections-requiring-review.md).
- [`silergy/sy8089`](silergy/sy8089/README.md) — no datasheet retained. Its feedback reference is
  now **derived** as 0.6 V from the Cardputer ADV divider. **That is inference, not primary
  evidence**, and the record says so.
