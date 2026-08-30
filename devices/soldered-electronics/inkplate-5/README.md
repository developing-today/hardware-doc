# Soldered Electronics — Inkplate 5 and Inkplate 5 Gen 2

> 5.2" Wi-Fi/BLE e-paper development boards with an ESP32-WROVER, from **Soldered Electronics** (Osijek, Croatia — formerly *e-radionica*).
> Research snapshot **2026-08-24**. Design data: **TAPR Open Hardware License** — redistribution permitted.

---

## The two generations differ in exactly one component

This is the headline result of comparing the two official KiCad BOMs, and it is not clearly stated on either product page.

| | **Inkplate 5** | **Inkplate 5 Gen 2** |
|---|---|---|
| Hardware design rev | **V1.2.0** | **V1.1.0** |
| E-paper panel | **`ED052TC2`** *(no component record — see [gaps §6](gaps-and-conflicts.md#6-no-e-ink-panel-datasheet))* | **[`ED052TC4`](../../../components/e-ink/ed052tc4/README.md)** |
| **Resolution** | **960 × 540** | **1280 × 720** |
| Diagonal | 5.2" | 5.2" |
| Processor | [ESP32-WROVER](../../../components/espressif/esp32-wrover/README.md) | [ESP32-WROVER](../../../components/espressif/esp32-wrover/README.md) |
| EPD PMIC | [TPS65186RGZ](../../../components/texas-instruments/tps65186/README.md) | [TPS65186RGZ](../../../components/texas-instruments/tps65186/README.md) |
| I/O expander | [PCAL6416AHF](../../../components/nxp/pcal6416a/README.md) | [PCAL6416AHF](../../../components/nxp/pcal6416a/README.md) |
| RTC | [PCF85063A](../../../components/nxp/pcf85063a/README.md) | [PCF85063A](../../../components/nxp/pcf85063a/README.md) |
| USB-UART | [CH340C](../../../components/wch/ch340c/README.md) | [CH340C](../../../components/wch/ch340c/README.md) |
| Charger | MCP73831T *(no component record)* | MCP73831T *(no component record)* |
| Arduino board define | `ARDUINO_INKPLATE5` | `ARDUINO_INKPLATE5V2` |
| Hardware repo | `Soldered-Inkplate-5-hardware-design` | `Soldered-Inkplate-5-Gen2-hardware-design` |

**Everything else is the same silicon.** Same module, same power architecture, same expander, same RTC, same bridge. Gen 2 is a panel upgrade — a 78 % pixel increase (518,400 → 921,600 px) at the same physical size, so ~1.78× the pixel density.

Resolutions confirmed from the Arduino library's own headers:

```c
// src/boards/Inkplate5/waveforms.h        (ARDUINO_INKPLATE5)
#define E_INK_WIDTH  960
#define E_INK_HEIGHT 540

// src/boards/Inkplate5V2/waveforms.h      (ARDUINO_INKPLATE5V2)
#define E_INK_WIDTH  1280
#define E_INK_HEIGHT 720
```

Note the library calls it **`Inkplate5V2`** while the store and repository call it **"Gen 2"**. Both refer to the same board. When selecting the target in Arduino you want **`Inkplate5V2`**.

> **Which one does ZeroWriter Ink use?** The **Gen 2 / V2** panel (`ED052TC4`, 1280×720) — on a [respun board](../../zerowriter/zerowriter-ink/README.md#the-second-important-fact-this-is-not-a-stock-inkplate-5), not the stock product.

## Complete bill of materials (Inkplate 5, V1.2.0)

Parsed from Soldered's own `OUTPUTS/V1.2.0/Soldered Inkplate 5 BOM.csv`.

| Ref | Part | Function |
|---|---|---|
| **U10** *(U11 on Gen 2)* | **[ESP32-WROVER](../../../components/espressif/esp32-wrover/README.md)** | Dual-core ESP32 module with PSRAM. PSRAM is essential — a 1280×720 framebuffer does not fit in internal RAM |
| **U11** *(U9 on Gen 2)* | **`ED052TC2`** / **[`ED052TC4`](../../../components/e-ink/ed052tc4/README.md)** | E Ink panel. Only the Gen 2's `ED052TC4` has a component record; **no record exists for the `ED052TC2`**, and no manufacturer datasheet exists for either — [gaps §6](gaps-and-conflicts.md#6-no-e-ink-panel-datasheet) |
| **U1** | **[TPS65186RGZ](../../../components/texas-instruments/tps65186/README.md)** (VQFN-49) | E-paper PMIC — generates the ±15 V / ±22 V and VCOM rails |
| **U9** *(U10 on Gen 2)* | **[PCAL6416AHF](../../../components/nxp/pcal6416a/README.md)** | 16-bit I²C GPIO expander @ **0x20** — carries the EPD control lines and SD power |
| **U7** | **[PCF85063A](../../../components/nxp/pcf85063a/README.md)** | RTC (with `X1` = 32.768 kHz ABS07AIG) |
| **U3** | **[CH340C](../../../components/wch/ch340c/README.md)** (SOP-16) | [USB-UART bridge](../../../components/wch/ch340x/README.md) |
| **U4** | **MCP73831T** *(no component record)* | Linear LiPo charger — see [charger and power path](../../../components/generic/charger-power-path/README.md) for the generic interface |
| **U6** | **TPS7A2633DRVR** *(no component record)* | 3.3 V LDO |
| **U2** | **TPS3840PL27DBVR** *(no component record)* | Voltage supervisor |
| **U8** | **SN74LVC1G34DBV** *(no component record)* | Single buffer |
| **U5** | **MC14093BDTR2G** *(no component record)* | Quad Schmitt NAND |
| **R2** | **NCP18XH103F03RB** NTC *(no component record)* | Panel temperature sense — e-paper waveforms are temperature-dependent |
| L1 / L2 | LQH44PN4R7MP0L / NR4012T2R2M | TPS65186 boost inductors |
| F1 | 1206, 500 mA | Fuse |
| **K11** | HYC77-TF09-200 | [microSD socket](../../../components/generic/micro-sd-sdmmc/README.md) |
| **K10** | **CR2032-BS-6-1** | **RTC backup coin-cell holder — footprint present, [ships unpopulated](features/rtc-backup-battery.md)** |
| SW1/SW2/SW3 | — | Reset / wake / user buttons |
| D9, D8 | — | Status LEDs |
| Q1 | **DNP** | Unpopulated |

⚠ **Designators shift between generations:** on the Inkplate 5 `K10` is the coin cell and `K11` the microSD; on the **Gen 2** `K11` is the coin cell. Read the silkscreen, not the other generation's table.

Plus **34 × `HEADER_MALE_1X1_Inkplate`** — the broken-out GPIO/peripheral header pads along the board edge.

Parts marked *(no component record)* are named in the BOM but have no entry under
[`components/`](../../../components/README.md). They are power, supervisory and glue logic that no
claim in this record depends on; creating records for them is an open follow-up.

## How the e-paper interface actually works

This is the interesting engineering in the Inkplate family and it is worth understanding before writing any code.

A parallel ("DES"-style) E Ink panel needs an 8-bit data bus clocked out at high rate, plus several timing signals. The ESP32 has no LCD peripheral. Soldered's solution: **drive the panel with the ESP32's I2S1 peripheral in parallel output mode, fed by DMA.**

From `Inkplate5V2Driver.cpp`:

```c
setI2S1pin(4,  I2S1O_DATA_OUT0_IDX, 0);   // D0
setI2S1pin(5,  I2S1O_DATA_OUT1_IDX, 0);   // D1
setI2S1pin(18, I2S1O_DATA_OUT2_IDX, 0);   // D2
setI2S1pin(19, I2S1O_DATA_OUT3_IDX, 0);   // D3
setI2S1pin(23, I2S1O_DATA_OUT4_IDX, 0);   // D4
setI2S1pin(25, I2S1O_DATA_OUT5_IDX, 0);   // D5
setI2S1pin(26, I2S1O_DATA_OUT6_IDX, 0);   // D6
setI2S1pin(27, I2S1O_DATA_OUT7_IDX, 0);   // D7
```

### Signal map

| Signal | Where it lives | Detail |
|---|---|---|
| `D0`–`D7` | **GPIO 4, 5, 18, 19, 23, 25, 26, 27** | I2S1 parallel data out, DMA-fed |
| `CL` (line clock) | **GPIO 0** | Bit-banged via `GPIO.out_w1ts/w1tc` = `0x01` |
| `LE` (latch enable) | **GPIO 2** | `GPIO.out` bit `0x04` |
| `CKV` | **GPIO 32** | `GPIO.out1` bit `0x01` |
| `SPH` | **GPIO 33** | `GPIO.out1` bit `0x02` |
| `OE` (output enable) | **expander pin 0** | via [PCAL6416A](../../../components/nxp/pcal6416a/README.md) |
| `GMOD` | **expander pin 1** | via [PCAL6416A](../../../components/nxp/pcal6416a/README.md) |
| `SPV` | **expander pin 2** | via [PCAL6416A](../../../components/nxp/pcal6416a/README.md) |
| `WAKEUP` | **expander pin 3** | [TPS65186](../../../components/texas-instruments/tps65186/README.md) wake |
| `PWRUP` | **expander pin 4** | [TPS65186](../../../components/texas-instruments/tps65186/README.md) power-up |
| `VCOM` | **expander pin 5** | [TPS65186](../../../components/texas-instruments/tps65186/README.md) VCOM control |
| [SD card](../../../components/generic/micro-sd-sdmmc/README.md) power MOSFET | **expander pin B2 (10)** | `SD_PMOS_PIN` — SD can be fully depowered for sleep |

Three consequences that matter:

1. **GPIO 0, 2, 4, 5, 18, 19, 23, 25, 26, 27, 32, 33 are all committed to the display.** That is most of the usable ESP32 GPIO. The broken-out header exposes what is left, and you should assume very little is free while the display is in use. GPIO 0 and 2 are also ESP32 **strapping pins** — they are shared with the boot mode selection.
2. **The slow control signals are behind I²C.** Every `OE`/`GMOD`/`SPV` toggle is an I²C transaction on the [PCAL6416A](../../../components/nxp/pcal6416a/README.md) at 0x20. This is why refresh sequencing is structured the way it is, and why you should not expect to bit-bang your own waveforms at speed.
3. **The SD card is switchable.** `SD_PMOS_PIN` on the expander gates [SD](../../../components/generic/micro-sd-sdmmc/README.md) power, which is how the Inkplate reaches low deep-sleep figures. If you drive the SD directly without powering it up first, it simply will not respond.

## Software

| Project | Repo | Licence | Notes |
|---|---|---|---|
| **Inkplate Arduino library** | `SolderedElectronics/Inkplate-Arduino-library` (306★) | **LGPL-3.0** | The main path. Covers Inkplate 2, 5, 5V2, 6, 6PLUS, 6COLOR, 6FLICK, 10, 4TEMPERA, 13SPECTRA |
| MicroPython driver | `SolderedElectronics/Inkplate-micropython` (91★) | MIT | |
| ESP-IDF component | `SolderedElectronics/Inkplate-ESP-IDF-component` | GPL-3.0 | |
| ESPHome component | `SolderedElectronics/Soldered-Inkplate-ESPHome` | GPL-3.0 | External component, SPI Inkplates |
| LVGL library | `SolderedElectronics/Inkplate-LVGL-Library` | GPL-3.0 | |
| Documentation | `SolderedElectronics/Inkplate-documentation` | — | readthedocs source |
| GUI Designer | `SolderedElectronics/Inkplate-GUI-Designer` | — | Web UI designer |
| Image converter | `SolderedElectronics/Inkplate-image-converter` | — | Web tool |

Notable third-party work: **[`turgu1/EPub-InkPlate`](https://github.com/turgu1/EPub-InkPlate)** (307★) — a full EPub reader, the highest-starred Inkplate application and the strongest evidence that the platform is viable for text-heavy devices. Also `turgu1/ESP-IDF-InkPlate` (ESP-IDF port) and `martinberlin/inkplate-platformio`.

## The Inkplate family

| Model | Panel | Notes |
|---|---|---|
| Inkplate 2 | 2.13", colour | SPI panel, small |
| **Inkplate 5** | 5.2" **960×540** | ESP32-WROVER |
| **Inkplate 5 Gen 2 / V2** | 5.2" **1280×720** | ESP32-WROVER; used by ZeroWriter Ink |
| Inkplate 6 | 5.83"/6" | The original, 1,312 % funded on Crowd Supply, 969 backers |
| Inkplate 6PLUS | 6" + touch + frontlight | |
| Inkplate 6COLOR | 6" colour | SPI panel |
| Inkplate 6FLICK | 6" | |
| Inkplate 10 | 9.7" | The large one |
| Inkplate 4 TEMPERA | 4" + glass panel, sensors | |
| Inkplate 13 SPECTRA | 13", Spectra colour | |
| **Inkplate 6 MOTION** | 6" | Separate Arduino library (`Inkplate_Motion_Arduino_Library`) — a different architecture |

Board list taken from `src/boards/` in the Arduino library — the authoritative list of what is actually supported.

## Family comparison

Soldered's own figures for the current (Soldered-era) boards, from `features.rst`:

| | Inkplate 2 | **Inkplate 5** | **Inkplate 5 V2** | Inkplate 6 | 6COLOR | 6PLUS | 6FLICK | Inkplate 10 | 4TEMPERA |
|---|---|---|---|---|---|---|---|---|---|
| Screen | 2.13" | **5.2"** | **5.2"** | 6" | 5.8" | 6" | 6" | 9.7" | 3.8" |
| Resolution | 202×104 | **960×540** | **1280×720** | 800×600 | 600×448 | 1024×758 | 1024×758 | 1200×825 | 600×600 |
| Pixels | 21,008 | **518,400** | **921,600** | 480,000 | 268,800 | 776,192 | 776,192 | 990,000 | 360,000 |
| Greyscale | – | **8** | **8** | 8 | – | 8 | 8 | 8 | 8 |
| Colour | Yes | No | No | No | **Yes** | No | No | No | No |
| Touchscreen | No | **No** | **No** | No | No | Yes | Yes | No | Yes |
| Backlight | No | **No** | **No** | No | No | Yes | Yes | No | Yes |
| microSD | No | **Yes** | **Yes** | Yes | Yes | Yes | Yes | Yes | Yes |
| **Full refresh** | 21 s | **1.02 s** | **1.13 s** | 1.26 s | 12 s | 1.27 s | 1.55 s | 1.61 s | 0.86 s |
| **Fast refresh** | – | **0.12 s** | **0.26 s** | 0.26 s | – | 0.64 s | 0.23 s | 0.62 s | 0.18 s |

Two things stand out. **The Inkplate 5 has the fastest refresh in the family** — 1.02 s full and 0.12 s fast, quicker than the physically smaller Inkplate 6. And the **Gen 2 costs surprisingly little for 78 % more pixels**: full refresh rises only 11 % (1.02 → 1.13 s), because full-refresh time is dominated by the e-paper waveform duration rather than data transfer. Fast refresh roughly doubles (0.12 → 0.26 s), where transfer time is a larger fraction of the total.

For a device like [ZeroWriter Ink](../../zerowriter/zerowriter-ink/README.md) that needs to keep up with typing, the **0.26 s fast refresh** is the number that matters — and it explains the campaign's "variable refresh rate produces almost no perceptible lag" claim being at least architecturally plausible.

Colour boards (Inkplate 2, 6COLOR) pay enormously for colour: 12–21 s full refresh and no fast-refresh mode at all.

## Component records

Every fitted part with a reusable record under [`components/`](../../../components/README.md).
Each links back here from its **Used By** section.

| Part | Role on this board | Record |
|---|---|---|
| ESP32-WROVER | Main processor module (PSRAM essential for the framebuffer) | [`espressif/esp32-wrover`](../../../components/espressif/esp32-wrover/README.md) |
| ED052TC4 | E Ink panel — **Gen 2 only**; the Inkplate 5's `ED052TC2` has no record | [`e-ink/ed052tc4`](../../../components/e-ink/ed052tc4/README.md) |
| TPS65186RGZ | E-paper PMIC, ±15 V / ±22 V and VCOM rails | [`texas-instruments/tps65186`](../../../components/texas-instruments/tps65186/README.md) |
| PCAL6416AHF | I²C GPIO expander @ 0x20 — EPD control lines and SD power gate | [`nxp/pcal6416a`](../../../components/nxp/pcal6416a/README.md) |
| PCF85063A | Real-time clock | [`nxp/pcf85063a`](../../../components/nxp/pcf85063a/README.md) |
| CH340C | USB-UART bridge | [`wch/ch340c`](../../../components/wch/ch340c/README.md) · generic: [`usb-uart-bridge`](../../../components/wch/ch340x/README.md) |
| microSD socket | Power-switchable card slot | [`generic/micro-sd-sdmmc`](../../../components/generic/micro-sd-sdmmc/README.md) |
| — | LiPo charging and power path (this board uses an MCP73831T; **[ZeroWriter's respin](../../zerowriter/zerowriter-ink/README.md) swaps in a [BQ25306](../../../components/texas-instruments/bq25306/README.md)**) | [`generic/charger-power-path`](../../../components/generic/charger-power-path/README.md) |

Seven BOM parts have **no** component record — `MCP73831T`, `TPS7A2633DRVR`, `TPS3840PL27DBVR`,
`SN74LVC1G34DBV`, `MC14093BDTR2G`, `NCP18XH103F03RB` and the `ED052TC2` panel. They are marked
inline in the BOM table above.

## Licensing

**All Soldered open-source hardware is under the TAPR Open Hardware License v1.0.** This is a genuine open-hardware licence permitting manufacture, modification and distribution, with reciprocal documentation obligations. It is why ZeroWriter could legally respin the Inkplate 5 Gen 2 and publish the result.

Software licences vary per repository (LGPL-3.0 for the Arduino library, MIT for MicroPython, GPL-3.0 for the newer components) — check each.

GitHub reports the hardware repos as `NOASSERTION` because it cannot machine-identify TAPR OHL; the `LICENSE.md` in each repo is the actual, unambiguous grant.

## Preserved artifacts

```
inkplate-5/artifacts/
├── hardware/soldered-inkplate-5-hardware-design/   commit 80c0d0fe (2024-10-20), TAPR OHL
│   ├── CAD/V1.2.0/       KiCad: MCU, POWER, E-paper, CTRL & COMS, SD & RTC sheets + PCB + panel
│   └── OUTPUTS/V1.2.0/   BOM.csv, Schematics.pdf, iBOM.html, gerbers, 3D .step, 3D-printable case
│       └── Compliance/   CE, UKCA, safety sheets (EN + DE)
├── source-snapshots/Inkplate-Arduino-library/      commit 1751cbe5 (2026-08-20), LGPL-3.0
├── source-snapshots/Inkplate-micropython/          commit 4a2b2926 (2026-08-10), MIT
└── docs/Inkplate-documentation/                    commit 1b3d3329 (2025-08-25)

inkplate-5-gen2/artifacts/
└── hardware/soldered-inkplate-5-gen2-hardware-design/  commit 7450a321 (2025-03-08), TAPR OHL
    ├── CAD/V1.1.0/  · OUTPUTS/V1.1.0/  · OUTPUTS/Compliance/
```

Soldered ships **CE and UKCA compliance documents and multilingual safety sheets** in the hardware repo. That is unusually thorough for an open-hardware vendor and is worth knowing if you are integrating an Inkplate into a product.

## Related

- [`features/rtc-backup-battery.md`](features/rtc-backup-battery.md) — the CR2032 the board expects but does not ship
- [`features/arduino-api.md`](features/arduino-api.md) — practical Arduino API reference
- [`regulatory-and-skus.md`](regulatory-and-skus.md) — SKUs, EAN barcodes, CE/UKCA declarations, safety constraints

- [Source manifest](sources.md) — every source behind this record, with class, retrieval date and local path
- [Pinouts and buses](pinouts-and-buses.md) · [Peripheral Mode](features/peripheral-mode.md) · [Gaps and conflicts](gaps-and-conflicts.md)
- [Inkplate 5 Gen 2](../inkplate-5-gen2/README.md) — the 1280 × 720 sibling
- [ZeroWriter Ink](../../zerowriter/zerowriter-ink/README.md) — the respun-Gen 2 device
- [Soldered Electronics vendor guide](../../../vendors/soldered-electronics/README.md)
- [Component index](../../../components/README.md) · [Device index](../../README.md)
- Store: <https://soldered.com> · Docs: <https://soldered.com/documentation/inkplate> · Community: <https://community.soldered.com>

> ⚠ Two links carried by earlier versions of this page are no longer sound: `learn.soldered.com`
> **no longer resolves in DNS** (checked 2026-08-28) and `inkplate.readthedocs.io` serves only a
> JavaScript redirect. See [sources.md](sources.md) rows IP5-26 and IP5-27.
