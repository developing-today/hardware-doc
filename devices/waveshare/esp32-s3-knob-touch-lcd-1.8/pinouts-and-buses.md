# Pinouts, buses and addressing

Retrieved: 2026-08-21; ESP32-U4WDH map re-derived pin-by-pin from the schematic and corrected 2026-08-22. Pin mappings below are cross-checked between the five schematic PNGs and official examples. "NC/unresolved" is intentional where evidence is incomplete.

**Verification pass 2026-08-24.** All five sheets were re-read as tiled, 6–14× upscaled crops. **Both GPIO maps below were checked entry-by-entry against the on-sheet alias tables and came back clean — not one pin assignment changed.** The pass additionally resolved `CN1` (§ "Connector records"), hardened the `LCD_TE` finding from "not established" to *explicitly marked no-connect*, and added several hardwired straps that were previously undocumented (§ "Hardwired straps"). It also **re-confirmed that the `BATT_ADC` divider taps the `5V` net and not a battery terminal** — see [gaps-and-conflicts](gaps-and-conflicts.md).

**This board has two MCUs and therefore two GPIO maps.** They share nothing except two UART wires and one analog audio mux. Read [Dual-MCU architecture](dual-mcu-architecture.md) first if you have not — in particular [§4, the definitive ownership table](dual-mcu-architecture.md#4-who-owns-what--the-definitive-table) — and see the [ESP32-U4WDH component page](../../../components/espressif/esp32-u4wdh/README.md) for the secondary chip in full.

## ESP32-S3 GPIO map

Reference designator `U2`. Schematic sheet `2_ESP32S3-R8.png`.

| GPIO | Net/function | Bus/notes |
|---:|---|---|
| 0 | **`I2S_SWITCH_IN`** — CH445P (`U18`) mux select | **Also the S3 BOOT strapping pin**, with 10 k pull-up `R58` to 3V3, and also brought out to connector `CN1` **pin 8**. Chooses whether the S3 or the ESP32-U4WDH drives the PCM5100A. See "Audio arbitration" below |
| 1 | BATT_ADC | ADC1 channel 0; 10 k/10 k divider (`R62`/`R63`) **from the 5 V rail** — re-verified 2026-08-24, the divider's top net label reads `5V`. It is **not** a battery-terminal sense. See [lipo-102035 §4](../../../components/generic/lipo-102035/README.md#4--batt_adc-does-not-measure-the-battery) |
| 2 | SDMMC D3 | 4-bit SD; 10 k pull-up `R49` |
| 3 | SDMMC CMD | 10 k pull-up `R48` |
| 4 | SDMMC CLK | net `SDMMC_SCK`; **no pull-up fitted** |
| 5 | SDMMC D0 | 10 k pull-up `R47` |
| 6 | SDMMC D1 | 10 k pull-up `R46` |
| 7 | EC1_B | primary knob (`SW2`) input, 10 k pull-up `R59` |
| 8 | EC1_A | primary knob (`SW2`) input, 10 k pull-up `R60` |
| 9 | TP_INT | CST816 touch interrupt |
| 10 | TP_RST | CST816 touch reset |
| 11 | TP_SDA / HAPTIC_SDA | shared I2C SDA — `HAPTIC_SDA` and `TP_SDA` are aliased to **one net** on sheet 2 |
| 12 | TP_SCL / HAPTIC_SCL | shared I2C SCL — likewise one net |
| 13 | LCD_QSPI_SCL | SPI2/QSPI clock |
| 14 | LCD_QSPI_CS | display chip select |
| 15 | LCD_QSPI_D0 | display data 0 |
| 16 | LCD_QSPI_D1 | display data 1 |
| 17 | LCD_QSPI_D2 | display data 2 |
| 18 | LCD_QSPI_D3 | display data 3 |
| 19 | USB_DN | native USB D- (one of the two USB-C orientations) |
| 20 | USB_DP | native USB D+ |
| 21 | LCD_RST | display reset |
| 38 | `ESP32S3_TX` | **inter-MCU UART1 TX** → ESP32-U4WDH GPIO18 |
| 39 | `S3_I2S_DAC_BCK` | to CH445P `S2A` |
| 40 | `S3_I2S_DAC_LRCK/WS` | to CH445P `S2C` |
| 41 | `S3_I2S_DAC_DIN` | to CH445P `S2B` |
| 42 | SDMMC D2 | 10 k pull-up `R10` |
| 45 | PDM_MIC_SCK | microphone clock |
| 46 | PDM_MIC_DATA | microphone data |
| 47 | LCD_BLK | AO3400A gate; PWM backlight |
| 48 | `ESP32S3_RX` | **inter-MCU UART1 RX** ← ESP32-U4WDH GPIO23 |

`CHIP_PU` is a separate reset net with `C8` 1 µF, not a GPIO. Unlisted S3 pins are not claimed as available. The S3 does **not** connect to `XSMT`, `EC2_A`, `EC2_B` or the ESP32's UART0.

**`LCD_TE` is not connected to the MCU — confirmed 2026-08-24 [SCH `2_ESP32S3-R8.png`].** The net originates at the panel connector `U5` pin 23 on sheet 1. In the GPIO alias table on sheet 2 its row has an **empty GPIO cell *and* an explicit `X` no-connect marker drawn on the `LCD_TE` stub** (read at 700×). That marker is a positive assertion by the designer, not merely an omission — an earlier revision of this page said only that the connection was "not established", which understated the evidence. **Practical consequence: tearing-effect / vsync-locked drawing is unavailable on this board.** You cannot synchronise flushes to the panel's scanout; expect to manage tearing with double-buffering and flush timing instead.

**Correction note (2026-08-22):** an earlier revision of this page described GPIO0 as a "CHIP_PU/USB selection-related net in connector block". That was wrong. Sheet `2_ESP32S3-R8.png` aliases `GPIO0` to `I2S_SWITCH_IN`, and sheet `5_DAC.png` shows `I2S_SWITCH_IN` arriving at CH445P pin 15. GPIO0 is the audio mux select.

## Hardwired straps — signals that exist but no MCU controls

New in the 2026-08-24 pass at *this* page's level — some were already recorded on the relevant component pages, and that is noted per row. Each is a peripheral pin you might reasonably expect to be firmware-controlled, and is not. All are **[SCH]** with the sheet and marker cited.

| Net / pin | Strapped to | Sheet | Consequence |
|---|---|---|---|
| `HAPTIC_EN` — DRV2605L (`U13`) pin 5 `EN` | **3V3** | `2_ESP32S3-R8.png` net-tie block | The haptic driver is **permanently enabled**; hardware shutdown is unreachable. Use the DRV2605L's `STANDBY` bit instead. Full consequences in [drv2605l §3.1](../../../components/texas-instruments/drv2605l/README.md) |
| `HAPTIC_TRIG` — DRV2605L (`U13`) pin 4 `IN/TRIG` | **GND** | same block | **No external-trigger, PWM or analog input mode**, and Audio-to-Vibe is unusable. The DRV2605L is controllable *only* over I2C (0x5A). Corroborated: no such GPIO appears anywhere in Waveshare's demo sources |
| `MIC1` pin 2 `L/R` | **GND** | `4_OTHER.png` | Fixes which PDM half-slot the microphone drives. Matters when configuring ESP-IDF PDM RX — the mic occupies one channel only, and which clock edge its data is valid on follows from this strap |
| `CARD1` pin 9 `SWITCH` (card detect) | **explicit `X` no-connect** | `4_OTHER.png` | **The microSD card-detect switch is not wired to either MCU.** Card presence can only be discovered by attempting a mount |
| `U18` CH445P pin 13 `EN#` | **GND** | `5_DAC.png` | Mux permanently enabled (traced at 800×: down, left, into the same node as `C100`'s low side) |
| `U18` CH445P pins 10/11/12 (`DD`, `S2D`, `S1D`) | **explicit `X` no-connect** ×3 | `5_DAC.png` | The mux's D channel — labelled `MCK` in the sheet's own legend table — is unpopulated at both inputs *and* the output. Three independent marks confirming **no MCLK reaches the PCM5100A**. `U12` pin 12 `SCK` likewise carries no net |
| `U13` DRV2605L pin 6 `VDD/NC` | **explicit `X` no-connect** | `5_DAC.png` | — |


## ESP32-U4WDH GPIO map

Reference designator `U14`. Schematic sheet `3_ESP32-CHIP.png`. This is a bare 48-pin QFN, not a module. Full treatment, including the package-pin table and the single-core/dual-core caveat, on the [ESP32-U4WDH component page](../../../components/espressif/esp32-u4wdh/README.md).

### Pins that carry a signal

| GPIO | Package pin | Net/function | Notes |
|---:|---:|---|---|
| 0 | 23 | `ESP32_IO0` — boot strap / auto-download | 10 k pull-up `R50`, `C24` 100 nF. Driven by bridge `U10` `TNOW/DTR#` through `R14` 5.1 k. Also appears on connector `CN1` |
| 1 | 41 | `ESP32_UART0_TX` | console/download TX → bridge `U10` RXD |
| 3 | 40 | `ESP32_UART0_RX` | console/download RX ← bridge `U10` TXD, via `R65` 470 R |
| 18 | 35 | `ESP32S3_TX` — **inter-MCU UART1 RX** | receives from S3 GPIO38 |
| 19 | 38 | `EC2_A` — second knob (`SW1`) channel A | 10 k pull-up `R55`, active low |
| 22 | 39 | `EC2_B` — second knob (`SW1`) channel B | 10 k pull-up `R56`, active low |
| 23 | 36 | `ESP32S3_RX` — **inter-MCU UART1 TX** | drives S3 GPIO48 |
| 25 | 14 | `ESP32_I2S_DAC_BCK` | I2S0 BCLK → CH445P `S1A` |
| 26 | 15 | `ESP32_I2S_DAC_DIN` | I2S0 SDOUT → CH445P `S1B` |
| 27 | 16 | `ESP32_I2S_DAC_LRCK/WS` | I2S0 WS → CH445P `S1C` |
| 32 | 12 | **`XSMT`** — PCM5100A soft mute | **Direct to the DAC, not through the mux. No S3 pin touches this net and no pull resistor is fitted.** The U4WDH alone can un-mute the DAC |

`EN`/`CHIP_PU` is package pin 9, net `ESP32_EN`, with `R54` 10 k pull-up and `C22` 1 µF, driven by bridge `U10` `RTS#`. It is a reset input, not a GPIO.

Note that GPIO32 is the `32K_XP` pad and GPIO33 is `32K_XN`: **no 32.768 kHz crystal is fitted**, so those RTC pins are repurposed. GPIO32 became the DAC mute line.

### Pins with a net label but no second endpoint

These four have net names on sheet 3 but do not terminate anywhere else in the five published sheets. They may be test points or unrouted stubs. **Do not assume they are usable.**

| GPIO | Package pin | Net |
|---:|---:|---|
| 2 | 22 | `ESP32_IO2` (also a boot strapping pin) |
| 4 | 24 | `ESP32_IO4` |
| 21 | 42 | `ESP32_IO21` |
| 33 | 13 | `ESP32_IO33` |

### Pins that are unavailable

| GPIO | Package pins | Why |
|---|---|---|
| 6, 7, 8, 9, 10, 11 | 28–33 (`SD_CLK`, `SD_DATA_0..3`, `SD_CMD`) | **Bonded to the in-package 4 MB flash die.** The schematic shows no net on any of them — the board confirms what the datasheet says |
| 5, 12, 13, 14, 15, 16, 17 | 34, 18, 20, 17, 21, 25, 27 | Present on the package but **not connected to anything** on this board |
| 34, 35, 36, 39 | 10, 11, 5, 8 (`VDET_1/2`, `SENSOR_VP/VN`) | Input-only pins, **not connected** |

**There are no spare, board-accessible GPIOs on the ESP32-U4WDH.** Everything it can do, it does with the eleven signals listed above.

### Support circuitry (not GPIO)

| Item | Detail |
|---|---|
| Crystal | `X2` 40 MHz on pins 44/45, load caps `C55`/`C56` 10 pF, series `R51` 0 R on XTAL_P |
| Antenna | `ANT2` (`CA-C03` symbol) fed from `LNA_IN` (pin 2) via π network `C46` 2.2 pF / `L5` 2 nH / `C45` 2.2 pF |
| Supplies | VDDA pins 1/43/46, VDD3P3 pins 3/4 via `L6` 2 nH, VDD3P3_RTC pin 19, VDD3P3_CPU pin 37, VDD_SDIO pin 26 (`C57` 1 µF — internal flash rail, do not load) |
| Regulator RC | `CAP1` pin 48 → `C59` 10 nF; `CAP2` pin 47 → `R52` 20 k + `C58` 3.3 nF |
| Ground | Exposed centre pad, pin 49 |

## USB-UART bridge U10 (serves the ESP32-U4WDH only)

Drawn as a 10-pin functional symbol on sheet `3_ESP32-CHIP.png` with **no part number**. **Identified 2026-08-21 as a WCH CH340X (MSOP-10), VID:PID `1A86:7523`** — see the [USB-UART bridge component record](../../../components/wch/ch340x/README.md) for the full evidence chain and the confirmation procedure.

| `U10` pin | Signal | Connects to |
|---:|---|---|
| 1 | UD+ | `USB_ESP32_DP` |
| 2 | UD- | `USB_ESP32_DN` |
| 3 | GND | GND |
| 4 | RTS# | `ESP32_EN` (U14 pin 9) |
| 5 | CTS# | **`R14` 5.1 kΩ to pin 6** — a mode-select strap, not flow control |
| 6 | TNOW/DTR# | `ESP32_IO0` (U14 pin 23) **directly**; `R14` 5.1 kΩ from this node to pin 5 |
| 7 | VCC | 3V3 |
| 8 | TXD | `ESP32_UART0_RX` (U14 pin 40, via `R65` 470 R) |
| 9 | RXD | `ESP32_UART0_TX` (U14 pin 41) |
| 10 | V3 | 3V3 |

**Correction (2026-08-21):** an earlier revision described `R14` as sitting in series between pin 6 and `ESP32_IO0`. It does not — it connects **pin 6 to pin 5**. That is verbatim WCH CH340 datasheet §5.3 option ②, "a 4.7 kΩ resistor connected between the 6# pin and the 5# pin … push-pull DTR enhancement mode", with a value inside WCH's stated 3–5.6 kΩ range. This is the load-bearing evidence for identifying `U10` as a **CH340X**, and it means **`CTS#` is not available as flow control**.

`RTS#` drives `EN` and `DTR#` drives `IO0` **directly**, without the two-transistor cross-coupled network used on most ESP32 dev boards — because CH340X's push-pull DTR mode is designed to make that network unnecessary. Practical consequence is unchanged: a serial terminal that asserts DTR or RTS on port open can reset the ESP32 or drop it into the bootloader. Disable DTR/RTS assertion if your monitor session dies on connect.

## Audio arbitration: CH445P (`U18`)

Schematic sheet `5_DAC.png`. Four-channel 2:1 analog switch selecting whose I2S reaches the PCM5100A.

| Channel | `S1` input (ESP32-U4WDH) | `S2` input (ESP32-S3) | `D` common → PCM5100A |
|---|---|---|---|
| A | GPIO25 `ESP32_I2S_DAC_BCK` | GPIO39 `S3_I2S_DAC_BCK` | `I2S_DAC_BCK` → `U12` pin 13 |
| B | GPIO26 `ESP32_I2S_DAC_DIN` | GPIO41 `S3_I2S_DAC_DIN` | `I2S_DAC_DIN` → `U12` pin 14 |
| C | GPIO27 `ESP32_I2S_DAC_LRCK/WS` | GPIO40 `S3_I2S_DAC_LRCK/WS` | `I2S_DAC_LRCK/WS` → `U12` pin 15 |
| D | *unconnected* | *unconnected* | *unconnected* — **no MCLK reaches the DAC from either MCU** |

- Select `IN` (pin 15) = net `I2S_SWITCH_IN` = **ESP32-S3 GPIO0**
- `EN#` (pin 13) tied to GND — permanently enabled
- `VCC` (pin 14) = `3V3_DAC` from the SGM2036-3.3 LDO (`U20`)

**Split ownership:** the S3 selects the source; the ESP32-U4WDH owns `XSMT` (mute). Neither can produce audio alone, so a source handover has to be coordinated over the inter-MCU UART. **Select polarity, resolved 2026-08-21: `IN` = 0 selects the `S1` bank (ESP32-U4WDH); `IN` = 1 selects the `S2` bank (ESP32-S3).** Established two ways — the CH440/CH445 datasheet truth table (§5.1), now retrieved, and Waveshare's own `07_Audio_Test/audio_bsp.c`, which sets GPIO0 **high** under the comment *"give control of the PCM5100A to the ESP32-S3"*. See [WCH CH445P §3–§4](../../../components/wch/ch445p/README.md). Because the PCM5100A gets no MCLK, it must run in BCK-derived PLL clocking mode, which also constrains the usable sample rates — see [PCM5100A §5](../../../components/texas-instruments/pcm5100a/README.md).

## Bus inventory

| Bus | Controller | Signals | Devices/address |
|---|---|---|---|
| I2C0 | ESP32-S3 | GPIO11 SDA, GPIO12 SCL, 5.1 k pull-ups (`R5`/`R6`) to 3V3 | CST816D 0x15; DRV2605L 0x5A |
| Display QSPI/SPI2 | ESP32-S3 | GPIO13-18 + reset 21 | marketed ST77916; software called SH8601 |
| SDMMC 4-bit | ESP32-S3 | GPIO2-6, 42 | microSD socket; no address |
| PDM RX | ESP32-S3 | GPIO45/46 | MSM261D4030H1CPM; no address |
| SPI flash | ESP32-S3 dedicated | SPICS0/CLK/IO0-3 | W25Q128JVPIQ |
| SPI flash | ESP32-U4WDH internal | package-internal, GPIO6-11 | 4 MB embedded die; not board-accessible |
| I2S TX | **either MCU**, through CH445P | S3 39/40/41 (`S2` bank) or U4WDH 25/27/26 (`S1` bank) | PCM5100A; no address, no MCLK |
| DAC mute | **ESP32-U4WDH only** | U4WDH GPIO32 → `XSMT` | PCM5100A pin 17 |
| Audio mux select | **ESP32-S3 only** | S3 GPIO0 → `I2S_SWITCH_IN` | CH445P pin 15 |
| **Inter-MCU UART1** | both | S3 TX38 → U4WDH RX18; U4WDH TX23 → S3 RX48 | board-internal, **full duplex, no RTS/CTS**, undocumented protocol, **baud unknown** — see [Dual-MCU architecture §2](dual-mcu-architecture.md#2-the-inter-mcu-link-a-two-wire-uart) |
| UART0 console (S3) | ESP32-S3 | `U0TX`/`U0RX` | not routed to the USB bridge |
| UART0 console (U4WDH) | ESP32-U4WDH | GPIO1/GPIO3 | to bridge `U10` |
| USB | orientation selected | S3 GPIO19/20 native, **or** `U10` bridge to U4WDH UART0 | plug orientation matters |

## Power rails as drawn

Confirmed 2026-08-24 **[SCH]**. Included here because the rail a peripheral sits on determines what happens to it in low-power states.

| Rail | Source | Reference designators |
|---|---|---|
| `5V` | **no source anywhere in the five sheets** — it is only ever consumed | — |
| `3V3` | buck from `5V` | `U19` `TLV62569DBVT`; `L4` 2.2 µH; feedback `R7` 100 k (high) / `R8` 22.1 k (low), giving 0.6 × (1 + 100/22.1) ≈ 3.32 V, and the sheet carries that formula as an annotation. `EN` tied to `VIN` |
| `3V3_DAC` | LDO from `5V`, behind a ferrite | `U20` `SGM2036-3.3YN5G/TR`; `L8` ferrite bead `BLM18AG102SN1D`; `EN` tied to `IN` |
| `A3V3` | **net-tied to `3V3_DAC`** on sheet 5 | — |
| `AGND` | **net-tied to `GND`** on sheet 5 | — |

So the analog audio section has its own LDO fed through a ferrite off `5V`, deliberately *not* off the digital `3V3` buck — the usual arrangement for keeping switching noise out of a DAC.

**The `5V` net having no drawn source is the single largest hole in the published schematic.** It is consumed by `U19` (sheet 1), by `L8`/`U20` (sheet 5), by the `R62`/`R63` `BATT_ADC` divider (sheet 4) and by `CN1` pin 1 (sheet 1), and produced by nothing. See [generic/charger-power-path](../../../components/generic/charger-power-path/README.md).

## Connector records

The 3.5 mm output, battery socket, USB-C and PH1.27 headers are documented in their linked component/interface records.

Connector **`CN1`** (`PM127-2-05-S-4.3`, sheet `1_LCD&POWER.png`) is the only 10-pin header drawn in the five sheets. **Its pinout is now resolved [SCH, 2026-08-24]:**

| Pin | Net | Belongs to |
|---:|---|---|
| 1 | `5V` | board input rail |
| 2 | `GND` | — |
| 3 | `USB_DN` | ESP32-S3 native USB D− (GPIO19) |
| 4 | `USB_DP` | ESP32-S3 native USB D+ (GPIO20) |
| 5 | `USB_ESP32_DP` | USB-UART bridge `U10` D+ → ESP32-U4WDH |
| 6 | `USB_ESP32_DN` | USB-UART bridge `U10` D− → ESP32-U4WDH |
| 7 | `GND` | — |
| 8 | `GPIO0` | ESP32-S3 — **BOOT strap *and* CH445P mux select** |
| 9 | `OUTR` | PCM5100A `U12` pin 7 |
| 10 | `OUTL` | PCM5100A `U12` pin 6 |

Odd pins on the top row, even on the bottom, pin 1 marked by the usual dot; each differential pair lands on one column pair. Read independently twice, at 500× and 1000× magnification, by locating each pin-number annotation relative to its own wire stub. This **supersedes the earlier decision not to transcribe the numbering** — the raster is not ambiguous at sufficient magnification, though the earlier caution was reasonable. Full treatment, including why this is probably an internal board-to-board connector rather than a user expansion header, in [generic/ph1.27-expansion-connectors](../../../components/generic/ph1.27-expansion-connectors/README.md).

⚠ A schematic symbol establishes *net-to-pin-number*. It does **not** establish which physical pin on the fitted header is pin 1, nor the row orientation seen from above the assembled board. This header carries two USB pairs and the mux-select/BOOT line: **verify by continuity before connecting anything.**

Notably, **no USB Type-C receptacle appears anywhere in the five sheets.** The orientation-selection behaviour is documented only by Waveshare's FAQ; its topology is unresolved.

Battery connector descriptions conflict: product imagery/wiki uses MX1.25 while other product wording uses PH1.25; inspect pitch, keying and polarity before use.
