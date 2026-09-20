# Device comparison matrix

> Every device documented under [`devices/`](../../devices/README.md), side by side.
> Compiled **2026-08-30** from the device records as they stood on that date. **Nothing here is a
> new measurement or a new retrieval** — every cell is either read out of a linked record or marked
> unknown.

## How to read this page

This is an **aggregation**, not a source. Where a cell disagrees with the device record it links
to, **the device record wins** — that is the standing rule in [the guides index](../README.md#conventions).
Where two device records disagree with *each other*, that is recorded in
[§10 Conflicts between records](#10-conflicts-between-records) rather than silently resolved.

Evidence labels are the repository's: **[DOC]** vendor document · **[SCH]** schematic ·
**[SRC]** source code · **[WEB]** vendor web page · **[COM]** community report · **[INF]** inference.
Because this page synthesises, most cells inherit the label of the record they came from; labels
are given inline only where the provenance is unusual or weak.

**"—" means the device does not have the thing. "unknown" means the record does not establish it.**
Those are different, and the distinction is load-bearing: an unknown price is a research gap, an
absent display is a design decision.

### The fourteen devices

| # | Device | Vendor | Record | Retrieved |
|---:|---|---|---|---|
| 1 | ESP32-S3-Knob-Touch-LCD-1.8 | Waveshare | [record](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) | 2026-08-21 |
| 2 | ESP32-P4-WIFI6-Touch-LCD-3.4C | Waveshare | [record](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) | 2026-08-24 |
| 3 | ESP32-P4-WIFI6-Touch-LCD-4C | Waveshare | [record](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md) | 2026-08-24 |
| 4 | ESP32-P4X-Function-EV-Board | Espressif | [record](../../devices/espressif/esp32-p4x-function-ev-board/README.md) | 2026-08-21 |
| 5 | ESP32-P4X-C5-Function-EV-Board | Espressif | [record](../../devices/espressif/esp32-p4x-c5-function-ev-board/README.md) | 2026-08-21 |
| 6 | ESP32-P4X-EYE | Espressif | [record](../../devices/espressif/esp32-p4x-eye/README.md) | 2026-08-21 |
| 7 | ESP32-P4-Function-EV-Board **(EOL)** | Espressif | [record](../../devices/espressif/esp32-p4-function-ev-board/README.md) | 2026-08-21 |
| 8 | ESP32-P4-EYE **(EOL)** | Espressif | [record](../../devices/espressif/esp32-p4-eye/README.md) | 2026-08-21 |
| 9 | XIAO ESP32S3 Sense | Seeed Studio | [record](../../devices/seeed-studio/xiao-esp32s3-sense/README.md) | 2026-08-24 |
| 10 | Inkplate 5 | Soldered Electronics | [record](../../devices/soldered-electronics/inkplate-5/README.md) | 2026-08-24 |
| 11 | Inkplate 5 Gen 2 | Soldered Electronics | [record](../../devices/soldered-electronics/inkplate-5-gen2/README.md) | 2026-08-24 |
| 12 | ZeroWriter Ink | ZeroWriter | [record](../../devices/zerowriter/zerowriter-ink/README.md) | 2026-08-24 |
| 13 | Zerowriter Fold | ZeroWriter | [record](../../devices/zerowriter/zerowriter-fold/README.md) | 2026-08-24 |
| 14 | Tanmatsu | Nicolai Electronics | [record](../../devices/nicolai-electronics/tanmatsu/README.md) | 2026-08-24 |

Two further directories under `devices/` are **platform records, not devices**, and are excluded
from the counts: [`waveshare/esp32-p4-wifi6-touch-lcd-xc-shared`](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md)
(the schematic and demo archive shared by #2 and #3) and
[`espressif/shared-artifacts`](../../devices/espressif/shared-artifacts/README.md) (the datasheets
and adapter-board designs shared by #4–#8).

---

## 1. Processors

| Device | Main SoC | ISA / cores / clock | Companion processors |
|---|---|---|---|
| [Knob 1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) | [ESP32-S3R8](../../components/espressif/esp32-s3r8/README.md) | Xtensa LX7 ×2, ≤240 MHz | **[ESP32-U4WDH](../../components/espressif/esp32-u4wdh/README.md)** (`U14`), Xtensa LX6, silicon rev **v3.1** — a second *full* SoC, not a helper |
| [P4 3.4C](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) | [ESP32-P4NRW32](../../components/espressif/esp32-p4/README.md) | RISC-V HP ×2 @ **360 MHz** + LP ×1 @ 40 MHz | ESP32-C6-MINI-1-N4 over SDIO (radio only) |
| [P4 4C](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md) | ESP32-P4NRW32 | as 3.4C | as 3.4C |
| [P4X-Function-EV](../../devices/espressif/esp32-p4x-function-ev-board/README.md) | ESP32-P4, rev **v3.1+** | RISC-V HP ×2 + LP ×1 | ESP32-C6-MINI-1 (radio only) |
| [P4X-C5-Function-EV](../../devices/espressif/esp32-p4x-c5-function-ev-board/README.md) | ESP32-P4 | RISC-V HP ×2 + LP ×1 | **ESP32-C5-MINI-1** (radio only) |
| [P4X-EYE](../../devices/espressif/esp32-p4x-eye/README.md) | ESP32-P4, rev **v3.1+** | RISC-V HP ×2 + LP ×1 | ESP32-C6-MINI-1**U** (external antenna) |
| [P4-Function-EV (EOL)](../../devices/espressif/esp32-p4-function-ev-board/README.md) | ESP32-P4, rev **before v3.1** | RISC-V HP ×2 + LP ×1 | ESP32-C6-MINI-1 |
| [P4-EYE (EOL)](../../devices/espressif/esp32-p4-eye/README.md) | ESP32-P4, rev **before v3.1** | RISC-V HP ×2 + LP ×1 | ESP32-C6-MINI-1U |
| [XIAO S3 Sense](../../devices/seeed-studio/xiao-esp32s3-sense/README.md) | [ESP32-S3R8](../../components/espressif/esp32-s3r8/README.md) | Xtensa LX7 ×2 @ 240 MHz | — |
| [Inkplate 5](../../devices/soldered-electronics/inkplate-5/README.md) | [ESP32-WROVER](../../components/espressif/esp32-wrover/README.md) (`U10`) | Xtensa LX6 ×2, 80–240 MHz | — |
| [Inkplate 5 Gen 2](../../devices/soldered-electronics/inkplate-5-gen2/README.md) | ESP32-WROVER (`U11`) | as Inkplate 5 | — |
| [ZeroWriter Ink](../../devices/zerowriter/zerowriter-ink/README.md) | ESP32-WROVER (`U11`) | as Inkplate 5 | **[ESP32-WROOM-32U-N4](../../components/espressif/esp32-wroom-32u/README.md)** on the keyboard PCB |
| [Zerowriter Fold](../../devices/zerowriter/zerowriter-fold/README.md) | **unknown** | unknown | unknown |
| [Tanmatsu](../../devices/nicolai-electronics/tanmatsu/README.md) | ESP32-P4NRW32 (`U7`) | RISC-V HP ×2, **360 or 400 MHz — vendor docs disagree** | ESP32-C6-WROOM-1-N8 (`U20`, radio) **and** [CH32V203C8T6](../../components/wch/ch32v203c8t6/README.md) (`U12`, always-on coprocessor) |

**Six of fourteen devices carry more than one processor**, and in five of those six the multi-chip
arrangement is the single most important thing to understand before writing firmware. The
[companion-radio pattern](../espressif/ecosystem-and-product-lines.md#6-the-companion-radio-pattern-p4--c6c5)
accounts for seven boards (all six P4 boards plus the Tanmatsu) and is forced: the ESP32-P4 has
[no radio of any kind](../../components/espressif/esp32-p4/README.md#5-no-wireless--the-defining-constraint).
The Knob 1.8 and ZeroWriter Ink reach two-chip designs by entirely different routes — see
[§8](#8-what-each-device-is-uniquely-good-at).

### The P4 clock figure is not consistent across the library

Three records give three framings for the same core: the [chip record](../../components/espressif/esp32-p4/README.md)
says **up to 400 MHz**, Waveshare's board records say **360 MHz**, and the Tanmatsu record records
that its own vendor's documents say **360 in one place and 400 in another**. These are probably not
in genuine conflict — 360 MHz is a plausible board-level operating point below a 400 MHz silicon
ceiling — but no record states that reconciliation, so **do not treat "the P4 runs at X MHz" as
established.** Logged in [§10](#10-conflicts-between-records).

---

## 2. Memory and storage

| Device | SRAM | PSRAM | Flash | Removable storage |
|---|---|---|---|---|
| Knob 1.8 | 512 KB (S3) | **8 MB** in-package (S3R8) | **16 MB** external [W25Q128JVPIQ](../../components/winbond/w25q128jv/README.md); separate **4 MB** in-package on the U4WDH | microSD, **4-bit SDMMC** |
| P4 3.4C / 4C | 768 KB L2MEM + 32 KB LP + 8 KB TCM | **32 MB** in-package | **32 MB** NOR QSPI (GD25Q256) | microSD, SDIO 3.0 — **pin map unresolved**, see [the shared record](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md#known-conflict--do-not-trust-the-sd-card-pins-in-03_sdmmc) |
| P4X-Function-EV | 768 KB L2MEM + 32 KB LP | in-package, **16 or 32 MB — not stated for this board** | 16 MB SPI NOR, **80 MHz cap, no auto-suspend** | microSD, 4-bit |
| P4X-C5-Function-EV | 768 KB L2MEM + 32 KB LP | **32 MB — stated** | 16 MB SPI NOR, same 80 MHz cap | microSD, 4-bit |
| P4X-EYE / P4-EYE | 768 KB L2MEM + 32 KB LP | in-package, size not stated | **16 MB** SPI | microSD, **4-line SDIO *or* SPI** |
| P4-Function-EV (EOL) | as P4X-Function-EV | as P4X-Function-EV | 16 MB, 80 MHz | microSD, 4-bit |
| XIAO S3 Sense | 512 KB | **8 MB** octal in-package | **8 MB** [GD25Q64E](../../components/gigadevice/gd25q64e/README.md) | microSD, **SPI 1-bit**, `CS` = GPIO21 |
| Inkplate 5 / Gen 2 | 520 KB (ESP32) | **8 MB** inside the WROVER can | 4 MB inside the can | microSD, **power-switchable** via the [PCAL6416A](../../components/nxp/pcal6416a/README.md) |
| ZeroWriter Ink | 520 KB | 8 MB (WROVER) | 4 MB (WROVER) | microSD, **relocated to a breakout PCB** |
| Zerowriter Fold | unknown | unknown | unknown | microSD (claimed) |
| Tanmatsu | 768 KB L2MEM + 32 KB LP | **32 MB** in-package | **16 MB** [W25Q128JVS](../../components/winbond/w25q128jv/README.md) | microSD, SDIO 2.0/3.0, **3.3 V and 1.8 V signalling** |

**PSRAM is the axis that actually separates these devices.** Every device in the library that drives
a display of any consequence has PSRAM, and in three cases the record states plainly that the
framebuffer would not otherwise fit: the [Inkplate 5 Gen 2's](../../devices/soldered-electronics/inkplate-5-gen2/README.md#why-the-higher-resolution-costs-you-something)
900 KiB of e-paper buffers, the [Tanmatsu's](../../devices/nicolai-electronics/tanmatsu/display.md)
768 KB single / 1.5 MB double 800×480 RGB565 buffer, and the P4 boards' 1.92 MB single 800×800
RGB888 frame. The arithmetic is worked through in
[display-interfaces.md § framebuffer budget](../hardware/display-interfaces.md#5-framebuffers-psram-and-the-arithmetic-that-decides-the-board).

Three smaller observations that only appear when the boards are lined up:

- **microSD is present on 13 of 14** and is wired five different ways — 4-bit SDMMC, SDIO 3.0,
  4-line-or-SPI, 1-bit SPI, and power-gated-through-an-I²C-expander. The bus width is a better
  predictor of whether video capture is viable than the SoC is.
- **Two boards can cut power to the card.** The Inkplate does it through expander pin `B2`
  (`SD_PMOS_PIN`) and the Waveshare P4 boards through GPIO45 driving an AO3401 P-MOSFET — and in
  the Waveshare case **no shipped demo touches GPIO45**, so a from-scratch project can get a dead
  card slot with no visible cause.
- **The 80 MHz flash cap on the Espressif P4 boards is a board restriction, not a silicon one**, and
  it is gated behind contacting Espressif. Any P4 benchmark that assumes 120 MHz flash does not
  apply to boards #4–#8.

---

## 3. Display

| Device | Type | Size | Resolution | Controller | Interface |
|---|---|---|---|---|---|
| Knob 1.8 | round IPS-claimed TFT | 1.8″ | 360 × 360 | **[ST77916](../../components/sitronix/st77916/README.md)** marketed; driver named [`sh8601`](../../components/generic/sh8601-compatibility-driver/README.md) | **QSPI** @ 40 MHz, 16 bpp |
| P4 3.4C | round IPS, optically bonded | 3.4″ | **800 × 800** (~333 ppi) | JD9365 *(no component record)* | **MIPI-DSI**, 2 lane @ 1500 Mbps, 24 bpp |
| P4 4C | round IPS | 4.0″ | **720 × 720** (~255 ppi) | JD9365 | MIPI-DSI, 2 lane @ 1500 Mbps |
| P4X-Function-EV | IPS cap-touch, **optional accessory** | 7″ | 1024 × 600 | EK79007AD + EK73217BCGA *(no records)* | MIPI-DSI via 15-pin FPC + adapter board |
| P4X-C5-Function-EV | as above, **optional accessory** | 7″ | 1024 × 600 | EK79007AD + EK73217BCGA | MIPI-DSI |
| P4X-EYE / P4-EYE | TFT, fitted | 1.54″ | 240 × 240 | **ST7789VW** *(no record)*, module `ZJY154KC-IF17` | **SPI** |
| P4-Function-EV (EOL) | as P4X-Function-EV | 7″ | 1024 × 600 | EK79007AD + EK73217BCGA | MIPI-DSI |
| XIAO S3 Sense | **— none** | — | — | — | — |
| Inkplate 5 | **e-paper**, 8 grey | 5.2″ | 960 × 540 | **none — bare row/column drivers** | **parallel DES**, 8-bit, driven from ESP32 **I2S1 in LCD mode** |
| Inkplate 5 Gen 2 | e-paper, 8 grey | 5.2″ | **1280 × 720** | none | as Inkplate 5 |
| ZeroWriter Ink | e-paper, 8 grey | 5.2″ | 1280 × 720 | none | as Inkplate 5 |
| Zerowriter Fold | e-paper, **frontlit, 10 levels** (claimed) | 6″ | **unknown** | **unknown** | **unknown** |
| Tanmatsu | TFT, `SWI LH397K-IC01`, 330 cd/m², 60 Hz nominal | 3.97″ | 480 × 800 native, used 800 × 480 | **[ST7701S](../../components/sitronix/st7701s/README.md)** | **MIPI-DSI**, 2 lane |

Panels: [ED052TC2 / ED052TC4](../../components/e-ink/ed052tc4/README.md) for the three e-paper
devices. The full treatment of the technologies in this table is in
[display-interfaces.md](../hardware/display-interfaces.md) and, for the e-paper column,
[e-paper-displays.md](../hardware/e-paper-displays.md).

**Five distinct display transports appear in fourteen devices** — QSPI, MIPI-DSI, SPI, e-paper
parallel-DES-over-I2S, and nothing at all. Notably **absent** from the whole library: any device
using the classic Intel-8080 (i80) parallel LCD bus or the ESP32-S3/P4 RGB parallel interface,
despite both being prominent in Espressif's `LCD_CAM` peripheral. That gap is discussed in
[§11](#11-gaps-the-comparison-exposes).

---

## 4. Input

| Device | Touch | Physical controls | Other |
|---|---|---|---|
| Knob 1.8 | [CST816D](../../components/hynitron/cst816d/README.md), **single-point**, I²C `0x15` | **Two independent knobs** ([SSCM110100](../../components/alps-alpine/sscm110100/README.md)) — one on each MCU; power button; BOOT | — |
| P4 3.4C / 4C | **GT9271** multipoint, I²C — ⚠ [see conflict C-1](#10-conflicts-between-records); **INT not wired, must poll** | BOOT/Reset | — |
| P4X-Function-EV / C5 | on the optional 7″ panel | BOOT, Reset | — |
| P4X-EYE / P4-EYE | — | **Rotary encoder**, user buttons, Boot (`⚙`), Reset (`↻`) | fill light |
| XIAO S3 Sense | — | BOOT, Reset | — |
| Inkplate 5 / Gen 2 | **— none** | Reset / wake / user buttons (`SW1`–`SW3`) | — |
| ZeroWriter Ink | — | **60 % hot-swap mechanical keyboard**, Kailh Choc Pro Red, on its own ESP32 | — |
| Zerowriter Fold | — | 60 % hot-swap Choc v1 (claimed) | — |
| Tanmatsu | **— none; explicitly not a touchscreen** | **69-key QWERTY + 6 function keys**, metal-dome, white LED backlight | [BMI270](../../components/bosch-sensortec/bmi270/README.md) IMU |

Two things worth pulling out. First, **the two keyboard devices and the Tanmatsu all put the
keyboard behind a second processor** — ZeroWriter on a whole ESP32-WROOM-32U, Tanmatsu on a
CH32V203 that also owns the RTC, the PMIC and both backlights. A keyboard is apparently never just
a matrix. Second, **touch and keyboard are mutually exclusive across the entire library**: no
documented device has both, and the two devices with the largest displays (Inkplate 5 Gen 2 at 5.2″,
Fold at 6″) have neither touch nor, in the Inkplate's case, any keyboard at all.

---

## 5. Connectivity

| Device | Wi-Fi | Bluetooth | Other radio | Wired |
|---|---|---|---|---|
| Knob 1.8 | b/g/n (S3, used); b/g/n on the U4WDH (present, unused by factory firmware) | **BLE 5 (S3)** *and* **Classic BR/EDR + BLE 4.2 (U4WDH only)** | — | USB-C — **orientation selects which MCU** |
| P4 3.4C / 4C | **Wi-Fi 6, 2.4 GHz** via C6 over SDIO | BT 5 LE via C6 | 802.15.4 via C6 | USB 2.0 HS Type-A, USB FS Type-C, CH343P UART |
| P4X-Function-EV | Wi-Fi 6, 2.4 GHz via C6 | BT 5 LE | 802.15.4 | **Ethernet 10/100** (IP101GR + RJ45); 4 USB ports |
| P4X-C5-Function-EV | **Wi-Fi 6, 2.4 *and* 5 GHz** via C5 | BT 5 LE | 802.15.4 | Ethernet 10/100; 4 USB ports |
| P4X-EYE / P4-EYE | Wi-Fi 6 via C6-MINI-1**U**, external antenna | BT 5 LE | 802.15.4 | USB 2.0 HS **device-only** + USB Debug |
| P4-Function-EV (EOL) | as P4X-Function-EV | as P4X-Function-EV | 802.15.4 | Ethernet; on **v1.4** a USB-UART bridge, on **v1.52** native USB Serial/JTAG |
| XIAO S3 Sense | b/g/n, **U.FL only, no PCB antenna** | **BLE 5 only — no Classic, no A2DP** | — | **native USB**, no bridge IC |
| Inkplate 5 / Gen 2 | b/g/n (WROVER) | BT 4.2 BR/EDR + BLE (WROVER) | — | [CH340C](../../components/wch/ch340c/README.md) USB-UART; easyC/Qwiic I²C |
| ZeroWriter Ink | present in silicon, **not enabled in shipped firmware** | present, not enabled | — | USB-C (charging + UART file transfer) on a breakout PCB; **QR-code transfer to phone** |
| Zerowriter Fold | "no Wi-Fi required"; **Cloud Push in development** | unknown | unknown | USB-C |
| Tanmatsu | **Wi-Fi 6, 2.4 GHz** via C6-WROOM-1-N8 | **BLE 5.3** | **802.15.4 (Thread 1.3 / Zigbee 3.0)** *and* **LoRa 868/915 MHz, 22 dBm** ([E22-900M22S](../../components/ebyte/e22-900m22s/README.md)) | [CH334R](../../components/wch/ch334r/README.md) 4-port USB hub; USB-C device + USB-A host (1 A) |

**Bluetooth Classic exists on exactly two devices in this library, and never on the main SoC.**
The Knob 1.8 gets it from a bolted-on ESP32-U4WDH whose only reason for existing is that
[the ESP32-S3 has no BR/EDR radio](../../components/espressif/esp32-s3r8/README.md#radio-capabilities-and-the-classic-bluetooth-limitation);
the Inkplates get it incidentally because a WROVER contains an original ESP32 die. Everything
newer — S3, C6, C5, P4-plus-companion — is BLE-only. If your product needs A2DP, SPP or Classic HID,
**that constraint eliminates most of this lineup at the silicon level** and no firmware change
recovers it.

**Only one device in the library does 5 GHz Wi-Fi** (the P4X-C5 board) and **only one does LoRa**
(the Tanmatsu). Both are single points of coverage, so neither claim has a second source inside
this library.

---

## 6. Power, battery, audio, camera

| Device | Input / regulation | Battery | Audio in | Audio out | Camera |
|---|---|---|---|---|---|
| Knob 1.8 | 5 V USB; [TLV62569](../../components/texas-instruments/tlv62569dbvt/README.md) 3V3 buck; [SGM2036-3.3](../../components/sgmicro/sgm2036-3.3/README.md) DAC LDO | **optional** 3.7 V [102035 LiPo](../../components/generic/lipo-102035/README.md); [charger/power-path unidentified](../../components/generic/charger-power-path/README.md) | PDM MEMS [MSM261D4030](../../components/memsensing/msm261d4030h1cpm/README.md) | [PCM5100A](../../components/texas-instruments/pcm5100a/README.md) DAC → [CH445P](../../components/wch/ch445p/README.md) mux → 3.5 mm. **No speaker, no amp** | — |
| P4 3.4C / 4C | MP1658, MP1605 *(no records)*; RTC backup cell **rechargeable only** | — | **dual** MEMS mics + ES7210 AEC ADC | ES8311 codec + PA, PH2.0 header, 8 Ω 2 W | **MIPI-CSI 2-lane**, 1080p30 H.264/JPEG encode |
| P4X-Function-EV / C5 | USB; 3V3 buck, `VDD_HP` buck, 5 V→3V3 LDO. **Not sleep-optimised** | — | onboard mic → ES8311 | ES8311 + NS4150B 3 W class-D, 4 Ω speaker header | MIPI-CSI 2 MP, **optional accessory** |
| P4X-EYE / P4-EYE | USB; power switch (`I`/`O`) | **Li connector + charger, red/green indicator** — the only portable P4 board. **No runtime figure published** | digital microphone | **— no codec, no amp, no speaker** | **2 MP fitted**, OV2710 / `HDF2710-47-MIPI`, **manual focus**, MIPI-CSI |
| P4-Function-EV (EOL) | as P4X-Function-EV | — | ES8311 | ES8311 + NS4150B | MIPI-CSI, optional |
| XIAO S3 Sense | [SGM40567](../../components/sgmicro/sgm40567/README.md) charger (~100–110 mA, `R10`-set); [SGM6029](../../components/sgmicro/sgm6029/README.md) buck-boost 600 mA | BAT± pads; **no battery-voltage sense at all** (vendor-confirmed) | PDM MEMS [MSM261D3526](../../components/memsensing/msm261d3526h1cpm/README.md), mono, `I2S_NUM_0` only | — | **[OV2640](../../components/omnivision/ov2640/README.md) / [OV3660](../../components/omnivision/ov3660/README.md) / [OV5640](../../components/omnivision/ov5640/README.md)**, 8-bit DVP, **no PWDN, no RESET** |
| Inkplate 5 / Gen 2 | `MCP73831T` **linear** charger; `TPS7A2633` LDO; `TPS3840` supervisor; **[TPS65186](../../components/texas-instruments/tps65186/README.md) EPD PMIC** | LiPo (connector) | — | — | — |
| ZeroWriter Ink | **[BQ25306](../../components/texas-instruments/bq25306/README.md) switch-mode** charger replacing the linear part; TPS65186 block unchanged | built-in, **user-replaceable**; **~100 h claimed** | — | — | — |
| Zerowriter Fold | unknown | **50–100 h claimed**, capacity not given | unknown | unknown | unknown |
| Tanmatsu | **[BQ25895](../../components/texas-instruments/bq25895/README.md)** PMIC (charge + monitor + 5 V boost); **[TPS63020](../../components/texas-instruments/tps63020/README.md)** 3V3 buck-boost; `LR8341A-M25` 2.5 V always-on rail for the coprocessor | **2500 mAh** LiPo, 104050, JST PH-2.0 | — | [ES8156](../../components/everest-semiconductor/es8156/README.md) DAC + FM8002A amp → 8 Ω speaker + 3.5 mm | **22-pin MIPI-CSI**, RPi Zero/5 pinout; **software support narrow** (OV5647-class only) |

The **only measured-ish power figures anywhere in the library** are Seeed's for the XIAO
(31.6 mA modem-sleep, 2.45 mA light-sleep, 33.51 µA deep-sleep, ~155 mA webcam average, ~366 mA peak)
— and Seeed's own table contradicts itself with a 3 mA deep-sleep row, while owners report **~90 mA**
once the camera has been used, because the camera has no power-down line. Everything else is a
vendor claim, an absence, or an explicit refusal: Espressif states outright that **P4 sleep current
cannot be benchmarked on the Function-EV boards** because `LDO_VO3`/`LDO_VO4` power board domains,
and the P4X-EYE record deliberately makes **no runtime claim** because no source supports one.

---

## 7. Expansion, enclosure, price, licence, lifecycle

| Device | Expansion | Enclosure / size | Price (dated) | Design-data licence | Status |
|---|---|---|---|---|---|
| Knob 1.8 | 2 × [PH1.27 10-pin](../../components/generic/ph1.27-expansion-connectors/README.md), **pinout absent** | **CNC metal**, black/blue, 66 mm ⌀ × 22 mm | **unknown** — no price captured | Schematic PNGs published, **no stated licence**; demo archive has **no LICENSE file** | current |
| P4 3.4C | 40-pin header, **28 GPIO**, **not Pi-compatible** (pin 4 is a GPIO where a Pi has 5 V); SH1.0 headers | bare board, PCB **rev1.1** | **$64.99 – $74.99** across both variants, waveshare.com **2026-08-24**; which price maps to which SKU **unresolved** | Code **Apache-2.0** + published BSP `3.0.1`; **schematic and wiki carry no licence** | current, **SKU 31523** |
| P4 4C | as 3.4C | bare board | same listing, same range | as 3.4C | current, **SKU 31522** — ⚠ [see conflict C-2](#10-conflicts-between-records) |
| P4X-Function-EV | J1 40-pin (GPIO0/1 and 45 not connected by default) | bare board, large | **unknown** | **No main-board design files** — the reference-design ZIP link is dead. Adapter boards **do** have full designs incl. Gerbers + BOM | current |
| P4X-C5-Function-EV | J1 40-pin | bare board, **v2.0** | **unknown** | **Schematic + PCB layout + dimensions PDF + DXF published** — the only board in the family. No BOM, no Gerbers | current |
| P4X-EYE | 2 × 10P female header | **enclosed hand-held**, port markings silkscreened on the case | **unknown** | **None** — reference-design ZIP dead; use the EOL predecessor's | current |
| P4-Function-EV (EOL) | J1 40-pin; **IO24/IO25 present on v1.4, removed on v1.52** | bare board | **unknown** | **Schematic v1.52 + PCB + dimensions + DXF + assembly drawing** | **EOL** |
| P4-EYE (EOL) | 2 × 10P | enclosed | **unknown** | **Schematic V2.3 + PCB V2.2** — *different board versions* | **EOL** |
| XIAO S3 Sense | 11 castellated GPIO + `J3` 30-pin [Hirose DF40C-30DP-0.4V](../../components/hirose/df40c-30dp-0.4v/README.md) B2B | bare, **17.78 × 21.14 mm**, 4-layer, **no mounting holes** | **$13.99**, Seeed store **2026-08-24** (bare S3 $7.49 ⇒ daughterboard = **$6.50**) | **KiCad sources under CC BY-SA 4.0** | in production |
| Inkplate 5 | 34 header pads; easyC/Qwiic | bare board; **3D-printable case in the repo** | **unknown** | **TAPR OHL v1.0** hardware; LGPL-3.0 Arduino lib, MIT MicroPython, GPL-3.0 IDF/ESPHome/LVGL | current, **V1.2.0** |
| Inkplate 5 Gen 2 | as Inkplate 5 | as Inkplate 5 | **unknown** | **TAPR OHL v1.0** | current, **V1.1.0** |
| ZeroWriter Ink | qwiic; 16-pin `HC-1.25-16PWT` inter-board | custom, **300 × 195 × 15 mm**; STLs in repo | **$285**, Crowd Supply, funded **2024-10-17**, 585 backers | Design files **GPL-3.0**; **main application firmware is binaries only** | shipping since **Jan 2026** |
| Zerowriter Fold | unknown | folding laptop-style, **12″ × 5″ × 1.25″** closed, **900 g** | **~$239 First Wave / ~$329 retail**, Kickstarter **2026-08-24** — plus $20–35 shipping, VAT, ~10 % US tariff | **Nothing published.** "Zerowriter Core" open source promised in **future tense** | **unshipped**, claimed late 2026 |
| Tanmatsu | **36-pin rear port** (14 GPIO, all 4 rails, USB, I²C, I3C, I²S) + **side "CATT" port: PMOD + SAO + JTAG simultaneously** | 3D printed, **120 × 135 × 18 mm**, **215 g** with battery | **€99.17 ex VAT / €119.99 inc 21 % NL VAT**, vendor shop **2026-08-24** | **CERN-OHL-P** hardware *and* mechanical; MIT firmware; Apache-2.0 C6 firmware; **branding all rights reserved** | sold; pre-order for much of its life; **only 868/915 MHz external-antenna variant offered** |

### Reading the licence column

There is a clean four-way split, and it maps almost exactly onto how useful each record was to build:

| Posture | Devices | Consequence |
|---|---|---|
| **Full open hardware with EDA sources** | Tanmatsu (CERN-OHL-P), Inkplate 5 / Gen 2 (TAPR OHL), XIAO (CC BY-SA 4.0), ZeroWriter Ink (GPL-3.0) | Netlists are recoverable. This is where [the pinout reconstructions](../reverse-engineering/netlists-from-vendor-eda-files.md) came from — the XIAO B2B connector, the [ED052TC4 panel pinout](../../components/e-ink/ed052tc4/README.md), the Inkplate-vs-ZeroWriter BOM diff |
| **PDF schematic, no licence** | Waveshare Knob 1.8, Waveshare P4 3.4C/4C | You can read it; redistribution status unknown, held unstaged |
| **Partial vendor PDFs, inconsistent** | Espressif P4 family — the **EOL** boards publish more than their current successors | Documented substitutions required; see [P4X-Function-EV §8](../../devices/espressif/esp32-p4x-function-ev-board/README.md#8-design-files-what-exists-and-an-important-substitution) |
| **Nothing at all** | Zerowriter Fold | No component records exist for it, correctly |

**The most striking single fact in this column is that Soldered ship CE and UKCA compliance
documents and multilingual safety sheets inside the public hardware repository.** No other vendor
in this library does that, and it is the reason ZeroWriter could legally respin the Gen 2 and
publish the result.

**The second most striking is a regression:** for both Espressif EYE and Function-EV lines, the
*current* board publishes **less** than the *end-of-life* board it replaced. The reference-design
ZIP links on the P4X pages return a 13,745-byte soft-404 for every filename variant tried, while
the EOL predecessors' real PDFs still resolve. Every record that relies on this substitution
labels it, and so should any downstream work.

---

## 8. What each device is uniquely good at

Ordered by how distinctive the answer is.

**[Tanmatsu](../../devices/nicolai-electronics/tanmatsu/README.md) — the only device that is simultaneously radio-rich, open, and a finished handheld.**
Wi-Fi 6, BLE 5.3, Thread/Zigbee *and* LoRa in one 215 g case, with CERN-OHL-P KiCad sources and an
LCSC-numbered BOM, at €99 ex VAT. Its genuinely unusual engineering decision is the always-on
CH32V203 coprocessor: it owns the keyboard, the RTC, both backlights and PMIC control, runs from a
2.5 V rail that persists when the device is "off", **and can be reflashed by the ESP32-P4 over
RVSWD** — the main SoC can reprogram its own power controller. If you want to build a hackable
pocket terminal, nothing else here is close.

**[XIAO ESP32S3 Sense](../../devices/seeed-studio/xiao-esp32s3-sense/README.md) — unbeatable capability per cubic millimetre.**
Camera, microphone, SD, Wi-Fi, BLE and 8 MB PSRAM in **17.78 × 21.14 mm** for **$13.99**. The record
states the economics precisely: the daughterboard costs **$6.50** over the bare board. If your
constraint is "must fit inside X", this wins by default. The costs are equally precise — the
daughterboard consumes **all four JTAG pins**, the user LED and SD chip-select are **the same pin**,
and there is **no battery-voltage sense**.

**[ESP32-P4X-C5-Function-EV-Board](../../devices/espressif/esp32-p4x-c5-function-ev-board/README.md) — the only readable P4 reference design, and the only 5 GHz device.**
Two independent reasons to pick it: it is the sole P4 board whose main-board schematic, PCB layout
and dimensions Espressif actually publishes, and it is the sole device in the library with 5 GHz
Wi-Fi. For a product that streams 1080p video off a congested 2.4 GHz band, that second point is
the whole argument.

**[ESP32-P4X-EYE](../../devices/espressif/esp32-p4x-eye/README.md) — the only P4 board that is meaningfully portable, and the clearest demonstration of what a P4 is for.**
Enclosed, battery-capable, rotary encoder, fitted manual-focus 2 MP MIPI-CSI camera, and a factory
demo that runs **YOLOv11-nano on-device** — a workload no ESP32-S3 can approach. No performance
figures are published and none are invented here.

**[Waveshare ESP32-P4-WIFI6-Touch-LCD-3.4C](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) — the highest pixel density in the library, on the most complete HMI board.**
800 × 800 at ~333 ppi on an optically bonded round panel, plus MIPI-CSI in, ES8311 out, dual mics
with AEC, and a 40-pin header, at $64.99–74.99. It is also the best-supported board here in
software terms: an **Apache-2.0 CI-tested vendor repository**, a **published BSP component**
(`waveshare/esp32_p4_wifi6_touch_lcd_xc` 3.0.1) and factory firmware for both variants.

**[Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — the only device with Bluetooth Classic audio, and the only CNC-metal enclosure.**
It is also the only device with **two independent knobs on two different processors**, and the only
one where **which way round you insert the USB-C plug decides which MCU you are talking to**. Choose
it if you want a physical media-control knob with A2DP; do not choose it if you want a simple
single-target development board.

**[Inkplate 5 / Gen 2](../../devices/soldered-electronics/inkplate-5/README.md) — the fastest-refreshing e-paper in the Inkplate family, on genuinely open hardware.**
Soldered's own figures put the Inkplate 5 at **1.02 s full / 0.12 s fast refresh**, quicker than the
physically smaller Inkplate 6, and the Gen 2 pays only **11 %** more on full refresh for **78 %** more
pixels. TAPR OHL sources plus CE/UKCA documents in the repo make it the reference platform for
anyone building an e-paper product rather than a toy.

**[ZeroWriter Ink](../../devices/zerowriter/zerowriter-ink/README.md) — the only finished consumer product in the library, and a worked example of respinning open hardware.**
Its value here is less the device than the diff: **8 parts added, 14 removed, 20 values changed**
against the stock Gen 2, including a linear→switch-mode charger swap, and an ESP32 pin map verified
**byte-identical**. That is the clearest documented answer to "what does it actually take to turn an
open dev board into a product".

**[ESP32-P4X-Function-EV-Board](../../devices/espressif/esp32-p4x-function-ev-board/README.md) — the bench platform.**
Ethernet, four USB paths, 7″ 1024×600 DSI, MIPI-CSI, audio in and out, 40-pin header. It exists to
answer "can the P4 drive my panel and camera at the frame rate I need" before you commit to a custom
design. It is explicitly **not** the board to benchmark sleep current on.

**[Zerowriter Fold](../../devices/zerowriter/zerowriter-fold/README.md) — nothing yet.**
It is in this matrix for completeness and as a warning. Every cell is a vendor claim about an
unshipped product, the Kickstarter page was never retrieved, and the one consequential claim — that
it uses **in-house** hardware rather than an Inkplate — would, if true, mean **none of the Inkplate
research transfers to it.**

---

## 9. Which device for which job

| If you need… | Pick | Why, and what it costs you |
|---|---|---|
| A camera in the smallest possible space | **XIAO ESP32S3 Sense** | $13.99, 17.8 × 21.1 mm. Costs: no JTAG with the daughterboard fitted, no battery sense, ~90 mA idle once the camera has run |
| Serious on-device vision (detection, YOLO-class) | **ESP32-P4X-EYE**, or **P4X-Function-EV** to prototype | P4 + 32 MB PSRAM + ISP + H.264. Costs: two firmwares, awkward C6 flashing over test points |
| 5 GHz Wi-Fi | **ESP32-P4X-C5-Function-EV-Board** | The only option in the library. Not a firmware change — a different board |
| Bluetooth Classic / A2DP audio | **Knob 1.8** (its ESP32-U4WDH) | The only source in the library. Costs: a second firmware image, a second flashing path, and a documented [USB-C orientation quirk](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md#the-usb-c-orientation-quirk) |
| A high-density round touch UI | **P4 3.4C** (800 × 800) | ~333 ppi, MIPI-DSI, PPA + 2D-DMA behind it. Costs: LVGL's rectangular layouts waste the corners |
| A larger round panel, density secondary | **P4 4C** (720 × 720, ~255 ppi) | Same PCB. Costs: the vendor Arduino library **defaults to the 3.4C** — an unmodified build silently targets 800 × 800 on a 720 × 720 panel |
| Ethernet on a P4 | **P4X-Function-EV** or **P4X-C5** | IP101GR + RJ45. The EYE boards have none |
| Always-on text display, weeks of battery | **Inkplate 5 Gen 2** | 1280 × 720 e-paper, power-gated SD, TAPR OHL. Costs: [most usable ESP32 GPIO is committed to the display bus](../../devices/soldered-electronics/inkplate-5/README.md#how-the-e-paper-interface-actually-works) |
| The same, but you want to *type* | **ZeroWriter Ink**, or the Inkplate + your own keyboard | 0.26 s fast refresh keeps up with typing. Costs: main firmware is binary-only; two processors |
| A hackable pocket terminal with LoRa | **Tanmatsu** | Only device with LoRa; CERN-OHL-P sources. Costs: no touch, ≤1 A from all 3.3 V outputs, camera software support narrow |
| To read a real P4 schematic before designing your own | **P4X-C5** (published) or **P4-Function-EV EOL** (published, v1.52) | Label the EOL substitution honestly — "chip-revision change" is not "identical schematic" |
| To buy something today, cheaply, with real documentation | **XIAO Sense $13.99** or **Tanmatsu €99** | The two devices with both a dated price *and* published EDA sources |

### What to avoid, and why

- **Do not benchmark ESP32-P4 sleep current on any Espressif Function-EV board.** Espressif says
  so explicitly; the board power architecture dominates.
- **Do not port a P4 pin map from a pre-2024 blog post.** If it mentions IO24 or IO25 on a header,
  it predates board v1.52 and will not work.
- **Do not trust `03_sdmmc` in the Waveshare P4 demo archive.** It is the stock Espressif example
  with *Espressif Function-EV-Board* pin defaults, unmodified. The microSD pin assignment for the
  Waveshare boards is **unresolved**.
- **Do not assume a bare XIAO ESP32S3 can take the Sense daughterboard.** The B2B connector is not
  fitted; established from the FCC model-differences exhibit.
- **Do not treat the Zerowriter Fold's specification as evidence of anything.**

---

## 10. Conflicts between records

Genuine disagreements found while compiling this page. None are resolved here; each is stated so a
future pass can close it.

### C-1. Touch controller on the Waveshare P4 boards: GT9271 vs GT911

| Record | Says |
|---|---|
| [P4 3.4C README, key specifications](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) | **GT9271** capacitive, "GT911-compatible driver" |
| [GT9271 component record](../../components/goodix/gt9271/README.md) | **GT9271**, quoting Waveshare's `docs/HARDWARE.md` verbatim |
| [Shared XC platform record, board architecture](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md#board-architecture) | **GT911**, linking the [GT911 record](../../components/goodix/gt911/README.md) |

Same PCB, two different part numbers in this repository. The GT9271 rows carry a direct vendor
quotation and the shared record's row does not, so the shared record's `GT911` is most likely a
simplification that predates the GT9271 finding — **but that is an inference, not a resolution.**
Functionally it does not matter (both are driven by `esp_lcd_touch_gt911`); for a BOM or a repair it
does. **Unresolved.**

### C-2. Is the ESP32-P4-WIFI6-Touch-LCD-4C purchasable?

The [4C record](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md) contradicts itself.
Its header and its "Availability — it is on sale" section state the board is **on sale as SKU 31522**
under the shared listing, with SKU data cited. Two later sections still carry the earlier,
superseded conclusion: *"even though the board is not in the store"* and, in Shortcomings,
*"**Not purchasable** through Waveshare's store as of 2026-08-24."* The record's own
[C2 conflict entry](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md) marks
availability **resolved** in favour of "on sale". **This is stale text inside a corrected record**,
not a source conflict — but it is exactly the kind of residue that gets quoted later.

### C-3. ESP32-P4 core clock: 360 vs 400 MHz

[Chip record](../../components/espressif/esp32-p4/README.md): "up to 400 MHz".
[Waveshare P4 records](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md): "360 MHz".
[Tanmatsu record](../../devices/nicolai-electronics/tanmatsu/README.md): "**360 MHz or 400 MHz — the
vendor's own docs disagree**". Probably board operating point vs silicon ceiling, but **no record
says so**, and the Tanmatsu's is a genuine intra-vendor contradiction. **Unresolved.**

### C-4. PSRAM size on the ESP32-P4X-Function-EV-Board

The [C5 board record](../../devices/espressif/esp32-p4x-c5-function-ev-board/README.md) notes that
its user guide commits to **32 MB PSRAM** while the C6 board's guide only says "supports up to
32 MB", and instructs treating the C6 board's figure as **unconfirmed**. Both boards are otherwise
described as the same design. **Unresolved by Espressif, correctly flagged in the record.**

### C-5. Inkplate refresh times: vendor table vs calculated estimate

| Source | ED052TC4 (Gen 2) full refresh | Partial |
|---|---|---|
| Soldered `features.rst`, via [Inkplate 5 record](../../devices/soldered-electronics/inkplate-5/README.md#family-comparison) | **1.13 s** (and 0.26 s "fast") | — |
| [ED052TC4 component record §6.4](../../components/e-ink/ed052tc4/README.md) — **calculated, not measured** | **≈0.8 s** 1-bit / **≈0.9 s** 3-bit, ±2× | **≈92 ms** |

Same order of magnitude, different methods, and the component record explicitly warns its figures
carry a **2× uncertainty** because `lcd_tx_wrx2_en = 1` may halve the effective byte rate. Neither
is a measurement on hardware. Notably, the component record lists "measured refresh times" as its
**single most useful open question** while the device record already carries the vendor's published
table — the two records are not aware of each other on this point. See
[e-paper-displays.md §6](../hardware/e-paper-displays.md#6-update-modes-and-real-timings).

### C-6. Tanmatsu display colour depth: RGB565 or RGB888?

Specifications page: the panel does RGB888 but *"current software can not make use of this mode"*.
BSP documentation: for Tanmatsu *"888RGB and 565RGB are both valid options which will be honoured"*.
Recorded in [`display.md` §7](../../devices/nicolai-electronics/tanmatsu/display.md) and the device's
own gaps file. **Unresolved.** The safe assumption is RGB565, and the safe *practice* is to read
back the format the BSP gives you rather than assuming your request was honoured.

### C-7. Display controller identity on the Knob 1.8 — ST77916 vs SH8601

**Analysed and resolved** in [ST77916 §2](../../components/sitronix/st77916/README.md): the panel
has a backlight, so it cannot be an AMOLED, so it cannot be an SH8601; the driver file name is
copy-paste residue from Espressif's generic QSPI shim. Listed here because it is the archetype of a
class of conflict — *the driver filename is not evidence of the silicon* — and because the same
pattern will recur on any QSPI panel. Residual uncertainty in the record is ~10 %, on the grounds
that a different Sitronix-alike would also fit the evidence.

### C-8. Two intra-record contradictions worth knowing

Not cross-record conflicts, but they will bite anyone quoting these devices:

- **XIAO deep-sleep current.** Seeed's own spec table gives both **33.51 µA** and **3 mA**
  ([conflict #4](../../devices/seeed-studio/xiao-esp32s3-sense/gaps-and-conflicts.md#4-seeeds-own-spec-table-gives-two-different-deep-sleep-figures-for-the-sense)),
  and owners measure **~90 mA** once the camera has been used. Three numbers spanning three orders
  of magnitude for the same board state.
- **Knob 1.8 USB-C.** Waveshare document the orientation-selects-your-MCU behaviour on the wiki, but
  **the five published schematic sheets contain no USB Type-C receptacle symbol at all**. The
  behaviour is real and vendor-stated; the topology that implements it is **not established**.

---

## 11. Gaps the comparison exposes

Compiling the matrix made the shape of the library's coverage visible. These are collection gaps,
not errors.

**Prices are missing for 8 of 14 devices.** Dated prices exist only for the XIAO ($13.99), the
Waveshare P4 pair ($64.99–74.99, unallocated between SKUs), ZeroWriter Ink ($285), the Fold
(~$239/~$329, unshipped) and the Tanmatsu (€99.17/€119.99). **No price was ever captured for the
Waveshare Knob 1.8, either Inkplate, or any of the five Espressif boards** — and the markets index
states plainly that no prices were verified in the 2026-08-24 pass. Two of those (Inkplate 5 and
Gen 2) are commercially available products where a price is one page load away.

**Nothing in this library has been tested on hardware.** Every device record says so. There is not
one measured current, frame rate, refresh time, temperature or throughput figure anywhere. Several
records name the specific measurement that would be most valuable — the ED052TC4's `micros()`
around `display()`, the Tanmatsu's achievable frame rate, the Knob's CH445P truth table.

**No device uses a parallel RGB or i80 LCD.** Five display transports are documented and both of the
`LCD_CAM`-based parallel interfaces are absent, so the library's advice on them is necessarily
theoretical. See [display-interfaces.md §3](../hardware/display-interfaces.md#3-the-interfaces-in-detail).

**No colour e-paper, and no frontlit e-paper that has shipped.** Soldered's 6COLOR and 13 SPECTRA
are *named* in the family table with refresh figures (12–21 s full, no fast mode) but have no
records; the only frontlit device is the unshipped, unverified Fold.

**Roughly two dozen fitted parts have no component record.** Concentrated in three areas: display
controllers (**JD9365, ST7789VW, EK79007AD, EK73217BCGA, ILI9881C** — see
[display-interfaces.md §11](../hardware/display-interfaces.md#11-every-display-controller-in-the-library)),
audio and Ethernet on the Espressif boards (ES8311, ES7210, NS4150B, IP101GR, TPS2051C), and the
companion radio modules themselves (**ESP32-C6-MINI-1, C6-MINI-1U, C5-MINI-1**) — which is
conspicuous, since those modules are the reason seven of these boards have any networking at all.
The `ED052TC2` panel of the Inkplate 5 also has no record while its Gen 2 sibling has a 700-line one.

**Single-source capabilities.** 5 GHz Wi-Fi, LoRa, Ethernet, Bluetooth Classic, hardware H.264,
rotary encoders and mechanical keyboards each appear on one or two devices only. Any general claim
this library makes about those features rests on a single record.

**Two lifecycle hazards are already live.** Both Espressif EOL user guides **moved between
2026-08-21 and 2026-08-28**; the originally-cited URLs now return HTTP 404 and **neither has an
Internet Archive capture**. The Waveshare XC schematic and 112 MiB demo ZIP live under a
product-specific path with **no third-party mirror located**. Two Soldered links have also gone —
`learn.soldered.com` no longer resolves in DNS.

---

## Related

- [Vendor and marketplace comparison](vendor-comparison.md) — where to buy, and whether the documentation will still be there later
- [Clones, siblings and variants](clones-and-variants.md) — including the Guition JC3636K518 as a sibling of the Knob 1.8
- [E-paper displays](../hardware/e-paper-displays.md) · [Display interfaces](../hardware/display-interfaces.md)
- [Espressif ecosystem and product lines](../espressif/ecosystem-and-product-lines.md) · [SoC peripheral reference](../espressif/soc-peripheral-reference.md)
- [Device index](../../devices/README.md) · [Component index](../../components/README.md) · [Guides index](../README.md)

---

## Evidence boundary

**This page contains no new research.** Every specification, price and status was read out of the
device and component records linked from its own cells, as those records stood on **2026-08-30**.
No vendor page was re-probed, no product was re-priced, and **no hardware was tested** — consistent
with every record it draws on.

What is genuinely new here, and therefore carries this page's own (weaker) authority:

- The **cross-record conflicts** in §10. C-1, C-2 and C-3 were found by comparing records, not by
  consulting sources; C-2's diagnosis as "stale text" is **[INF]**.
- The **groupings and counts** in §§1–7 (five display transports, Bluetooth Classic on two devices,
  microSD on 13 of 14, licence four-way split). These are arithmetic over the records and are only
  as complete as the records are.
- The **recommendations** in §§8–9. These are judgements from documented properties, not from use.
  No device in this library has been operated by anyone who wrote about it here.
- The **gap analysis** in §11 is a statement about *this collection*, not about the world.

Where this page and a device record differ, **the device record is correct.**
