# Pinouts and buses — Waveshare ESP32-S3-ePaper-3.97

> Research snapshot **2026-09-01**. **No hardware in hand.** Every mapping below is
> read from the published schematic or from the vendor's own driver source. The
> *extraction* is `executed-success` (the commands are in [`commands.md`](commands.md)
> and reproducible); the *electrical claims* are `not-tested`.

## Where this comes from

Two independent sources, which agree:

| Source | What it gives | Evidence label |
|---|---|---|
| **[SCH]** `artifacts/schematic/ESP32-S3_e-Paper-3.97-schematic.pdf` — Altium PDF, 1 sheet, 257 550 B, SHA-256 `b1203145…` | An **allocation table drawn on the sheet itself**, mapping every `GPxx` net to its subsystem | `executed-success` for the text extraction |
| **[SRC]** `waveshareteam/ESP32-S3-ePaper-3.97` @ `9b12d40`, `Arduino/examples/02_E-Paper_Example/DEV_Config.h` lines 49–54 | The six e-paper pins as `#define`s the vendor actually compiles | `executed-success` for the read |

**They agree on all six e-paper pins.** That cross-check is the reason the e-paper
rows below are the most trustworthy in this document — two sources produced by
different Waveshare teams, from different toolchains, matching exactly.

### How the schematic text was recovered

Waveshare's schematic is an Altium PDF publisher export. Per this repository's
[Waveshare vendor guide §8.7](../../../vendors/waveshare/README.md), these normally
resist `grep` because each glyph is emitted as its own text object with its own
transform. There is no `pdftotext` on this host either.

The route that worked — scripts are in [`tools/`](tools/) and the exact invocations
in [`commands.md`](commands.md):

1. `tools/pdftext.py` — inflate every `FlateDecode` stream, including **Form XObjects**
   (the entire sheet lives in one XObject here, *not* in `/Contents`; a page-only
   walker returns zero text and looks like "no text layer"), then interpret the
   `BT`/`Tm`/`Td`/`Tj`/`TJ` operators to get `(x, y, glyph)`.
2. `tools/reflow.py` — group glyphs by baseline, sort by x, join runs whose gap is
   under threshold. 4 318 glyphs → 1 150 tokens.

Result: `artifacts/schematic/schematic-text-reflowed.tsv`, retained so no one has to
re-derive it.

> **This is a reading aid, not a netlist.** It recovers *text adjacency*, not
> electrical connectivity. Unlabelled wire-only connections are invisible to it.
> Every row below is text that appears in the sheet's own allocation table; none of
> it is traced connectivity. Where it matters, the vendor source corroborates.

## The GPIO allocation table

This is the table Waveshare draws beside the module symbol `U7`
(`ESP32-S3-WROOM-1-N16R8`), transcribed. Its column headings are the vendor's own:
`ePaper`, `Audio`, `SD Card`, `RTC`, `KEY & LED`, `QMI8658A`, `Power`, `OTS`.

| GPIO | Net | Subsystem | Direction | Notes |
|---|---|---|---|---|
| GPIO0 | `ESP_BOOT` | OTS | in | Strapping pin — BOOT button |
| GPIO1 | `PWR_OUT` | Power | — | [AXP2101](../../../components/x-powers/axp2101/README.md) domain |
| GPIO2 | `ESP_CHG` | Power | — | Charge status from AXP2101 |
| **GPIO3** | **`EPD_BUSY`** | **ePaper** | **in** | **Confirmed by [SRC] `EPD_BUSY_PIN 3`** |
| GPIO4 | `Button_Up` | KEY & LED | in | Rotary switch, up |
| GPIO5 | `Button_Function` | KEY & LED | in | Rotary switch, centre/press |
| GPIO6 | `Button_Down` | KEY & LED | in | Rotary switch, down |
| GPIO7 | — | — | — | **No assignment in the table.** See [free pins](#is-anything-free) |
| GPIO8 | `SD_D2` | SD Card | i/o | |
| **GPIO9** | **`EPD_DC`** | **ePaper** | **out** | **Confirmed by [SRC] `EPD_DC_PIN 9`** |
| **GPIO10** | **`EPD_CS`** | **ePaper** | **out** | **Confirmed by [SRC] `EPD_CS_PIN 10`** |
| **GPIO11** | **`EPD_SCK`** | **ePaper** | **out** | **Confirmed by [SRC] `EPD_SCK_PIN 11`** |
| **GPIO12** | **`EPD_DIN`** | **ePaper** | **out** | SPI MOSI. **Confirmed by [SRC] `EPD_MOSI_PIN 12`** |
| GPIO13 | `I2S_MCLK` | Audio | out | To [ES8311](../../../components/everest-semiconductor/es8311/README.md) |
| GPIO14 | `I2S_SCLK` | Audio | out | |
| GPIO15 | `SD_MISO` | SD Card | in | |
| GPIO16 | `SD_CLK` | SD Card | out | |
| GPIO17 | `SD_MOSI` | SD Card | out | |
| GPIO18 | `SD_CS` | SD Card | out | |
| GPIO19 | `ESP_USB_N` | OTS | i/o | Native USB D− |
| GPIO20 | `ESP_USB_P` | OTS | i/o | Native USB D+ |
| GPIO21 | `I2S_DSOUT` | Audio | out | |
| GPIO35 | *NC* | OTS | — | Marked **NC** — consumed by the module's octal PSRAM, see [Is anything free?](#is-anything-free) |
| GPIO36 | *NC* | OTS | — | Marked **NC** |
| GPIO37 | *NC* | OTS | — | Marked **NC** |
| GPIO38 | `PWR_IRQ` | Power | in | AXP2101 interrupt |
| GPIO39 | `AudioCTR_PIN`, `AXIS_INT1` | Audio, QMI8658A | — | **Two functions on one pin** — see [conflicts](#pin-conflicts-and-shared-nets) |
| GPIO40 | `AXIS_INT2` | QMI8658A | in | IMU interrupt 2 |
| GPIO41 | `ESP_I2C_SDA` | *(shared bus)* | i/o | `Audio_SDA` + `RTC_SDA` + `AXIS_SDA` + `AXP_SDA` |
| GPIO42 | `ESP_I2C_SCL` | *(shared bus)* | out | `Audio_SCL` + `RTC_SCL` + `AXSI_SCL` + `AXP_SCL` |
| GPIO43 | `ESP_LED1`, `ESP_UART_RX` | KEY & LED, OTS | — | UART0 RXD0 also lands here |
| GPIO44 | `ESP_LED2`, `ESP_UART_TX` | KEY & LED, OTS | — | UART0 TXD0 also lands here |
| GPIO45 | `RTC_INT_ESP` | RTC | in | [PCF85063A](../../../components/nxp/pcf85063a/README.md) alarm/interrupt |
| **GPIO46** | **`EPD_RST`** | **ePaper** | **out** | **Confirmed by [SRC] `EPD_RST_PIN 46`** |
| GPIO47 | `I2S_LRCK` | Audio | out | |
| GPIO48 | `I2S_DSDIN` | Audio | in | Microphone path |

Source: **[SCH]**, allocation table at sheet coordinates y≈39–162, x≈159–370.
Bold rows additionally **[SRC]**.

### The one column heading that does not make sense

The `GPxx` column carries the heading **"IO Expander"**. **No I/O expander part
appears anywhere in the schematic's text layer** — no TCA9554, no PCA95xx, no
PCAL6416. Its sibling the
[ESP32-C6-ePaper-1.54](../esp32-c6-epaper-1.54/README.md) *does* fit a TCA9554 and
Waveshare documents it explicitly, so the most likely reading is that this heading
is **copied from a sibling board's schematic template**.

Treated as an **unexplained label, not a part**. Per the method's rule against
promoting a candidate to a finding, no `tca9554` component record was created.
Tracked as [C-WS4](gaps-and-conflicts.md#c-ws4--io-expander-column-heading-with-no-io-expander-part).

## Buses

### E-paper — 4-wire SPI

| Signal | GPIO | Panel pin role |
|---|---|---|
| `EPD_SCK` | 11 | SCL |
| `EPD_DIN` | 12 | SDA (MOSI; write-only) |
| `EPD_CS` | 10 | CS# |
| `EPD_DC` | 9 | D/C# |
| `EPD_RST` | 46 | RES# |
| `EPD_BUSY` | 3 | BUSY |

The panel is a **3.97" 800 × 480 module with an [SSD1677](../../../components/solomon-systech/ssd1677/README.md)
bonded on** — see the [panel component record](../../../components/waveshare/3.97inch-e-paper/README.md).
The SSD1677 supports 3-wire (9-bit) and 4-wire (8-bit) SPI selected by the `BS1`
pin; the schematic carries a `BS`/`3-line SPI` / `4-line SPI` annotation and the
vendor driver defines `D_9PIN 1`, so **4-wire is what the board uses**.

There is **no software-controlled panel power rail**: `DEV_Config.h` sets
`EPD_PWR_PIN -1`. Panel supply `EPD_VCC` comes from the AXP2101 rail labelled
`EPD_VCC_AXP` on the sheet, so power gating is a PMIC operation, not a GPIO one.
`not-tested`.

The panel's high-voltage rails (`VGH`, `VGL`, `VSH1`, `VSH2`, `VSL`, `VCOM`, `VPP`)
and the boost control pins `GDR` / `RESE` appear on the panel FPC connector `J2`,
which is the SSD1677's **integrated DC-DC** doing the work — the board supplies no
separate EPD boost converter. This matches the topology already documented for the
[PaperMono's panel](../../../components/dke/depg0397bbs770f3/README.md).

### I²C — one bus, four devices

`ESP_I2C_SDA` = **GPIO41**, `ESP_I2C_SCL` = **GPIO42**. Everything shares it:

| Device | Net alias on sheet | Address | Record |
|---|---|---|---|
| [AXP2101](../../../components/x-powers/axp2101/README.md) PMIC | `AXP_SDA` / `AXP_SCL` | `0x34` **[SRC]** | via `AXP2101_SLAVE_ADDRESS` |
| [ES8311](../../../components/everest-semiconductor/es8311/README.md) codec | `Audio_SDA` / `Audio_SCL` | `0x18` (7-bit, `CE`=0) — **`inferred` from the datasheet, not read from board source** | |
| [PCF85063A](../../../components/nxp/pcf85063a/README.md) RTC | `RTC_SDA` / `RTC_SCL` | `0x51` — **`inferred`** | |
| [QMI8658A](../../../components/qst/qmi8658a/README.md) IMU | `AXIS_SDA` / `AXSI_SCL` *(vendor's typo)* | `0x6A`/`0x6B` — **`inferred`** | |

Only the AXP2101 address is evidenced from this board's own source. The other three
are the parts' usual addresses and are **not** confirmed against this board — a
future pass should read them out of the ESP-IDF examples
`06_I2C_PCF85063`, `07_I2C_SHTC3`, `05_QMI8658A`.

The [SHTC3](../../../components/sensirion/shtc3/README.md) is also on this bus
(fixed address `0x70`), though the sheet's allocation table gives it no column.

### I²S — audio

`I2S_MCLK` 13, `I2S_SCLK` 14, `I2S_LRCK` 47, `I2S_DSOUT` 21, `I2S_DSDIN` 48 — a
standard 5-wire I²S to the ES8311, with `AudioCTR_PIN` on GPIO39 gating the
[NS4150B](../../../components/nsiway/ns4150b/README.md) amplifier.

### SD card — 1-bit SPI mode, not SDMMC

`SD_CLK` 16, `SD_MOSI` 17, `SD_MISO` 15, `SD_CS` 18, plus `SD_D1` (GPIO7 region)
and `SD_D2` (GPIO8). **The net names are SPI names** (`MOSI`/`MISO`/`CS`), which is
a different choice from the 4-bit SDMMC used on Waveshare's
[Knob-Touch-LCD board](../esp32-s3-knob-touch-lcd-1.8/README.md). `D1`/`D2` being
present suggests 4-bit wiring exists even if the vendor example drives it as SPI —
**unresolved**, tracked as [C-WS5](gaps-and-conflicts.md#c-ws5--sd-card-spi-names-but-4-bit-nets).

## Pin conflicts and shared nets

1. **GPIO39 carries two functions** — `AudioCTR_PIN` *and* `AXIS_INT1`. If both the
   amplifier gate and the IMU interrupt genuinely land on GPIO39, they cannot both
   be used as intended. Most likely the allocation table lists a *candidate*
   assignment for one of them. **Unresolved** — needs the rendered sheet or a
   continuity check. `inferred`.
2. **GPIO43/44 are UART0 and the LEDs.** `ESP_UART_TX`/`RX` are the console. Driving
   `ESP_LED1`/`ESP_LED2` on the same pins means **using the LEDs costs you the boot
   log**, or vice versa.
3. **One I²C bus for PMIC, codec, RTC and IMU.** A hung transaction takes out power
   management with it. There is no second bus to fall back on.
4. **GPIO0 is the BOOT strap** — normal ESP32-S3 caveat.

## Is anything free?

Practically, **no**. This is the single most important fact about the board for
anyone arriving from the PaperMono comparison.

- **GPIO7** is the only pin with no entry in the allocation table, and even that is
  ambiguous: `SD_D1` sits at the same table row, so GPIO7 is most likely the SD
  card's DAT1. **Do not assume GPIO7 is free.** `inferred`.
- **GPIO35–37 are marked NC**, and that is not spare capacity — the fitted module is
  an **`ESP32-S3-WROOM-1-N16R8`**, whose 8 MB PSRAM is **octal**, consuming
  GPIO35/36/37 internally. Waveshare marking them NC is correct and they are not
  usable. See [ESP32-S3R8](../../../components/espressif/esp32-s3r8/README.md).

### There is no expansion header

The board's only connectors are:

| Designator | Type | Purpose |
|---|---|---|
| `H1` | USB Type-C receptacle | Power, native USB, flashing, console |
| `H2` | **PH1.25-2P** | Speaker output (from NS4150B) |
| `H3` | **PH1.25-2P** | 3.7 V Li-ion battery |
| `H4` | **PH1.25-2P** | RTC backup battery (via `R61`, 0 Ω) |
| `J2` | FPC | The e-paper panel itself |
| — | microSD socket (`TF-07F`) | Storage |

**No 2.54 mm header, no Qwiic/STEMMA/easyC connector, no broken-out GPIO of any
kind.** `LSK1`–`LSK4` are solder links and `TP1`–`TP9` are test points, neither of
which is a user expansion interface.

This directly contradicts the framing that sent this research here — see
[C-WS1](gaps-and-conflicts.md#c-ws1--the-expansion-claim-is-backwards) and the
[PaperMono comparison](../../m5stack/papermono/comparisons-and-recommendations.md).
Waveshare's **1.54-inch** e-paper boards *do* carry a 2×6 2.54 mm header; this one
does not.

## Power domains

From the AXP2101 rails named on the sheet, cross-read against the vendor's
`axp_prot.cpp`:

| Rail | Set to | Evidence | Feeds |
|---|---|---|---|
| `DC1` | **3300 mV** | **[SRC]** `axp_prot.cpp:53` | `VCC3V3` main logic |
| `ALDO1` | **3300 mV** | **[SRC]** `:55` | |
| `ALDO2` | **3300 mV** | **[SRC]** `:56` | |
| `ALDO3` | **3300 mV** | **[SRC]** `:57` | |
| `ALDO4` | present on sheet | **[SCH]** | not configured in the sampled source |
| `BLDO1`, `BLDO2` | present on sheet | **[SCH]** | `EPD_VCC_AXP` is a candidate consumer — **not established** |
| `VBACKUP` | RTC coin cell, charge target **3000 mV** | **[SRC]** `:116` | `H4` |

Which rail feeds the panel is **not established** from text extraction alone; it
needs the rendered sheet. Tracked in [gaps-and-conflicts.md](gaps-and-conflicts.md).

Charging, as configured by the vendor firmware **[SRC]** `axp_prot.cpp`:

| Parameter | Value | Line |
|---|---|---|
| Precharge current | 50 mA | `:101` |
| Constant current | **200 mA** | `:102` |
| Termination current | 25 mA | `:103` |
| Charge target voltage | **4.2 V** | `:106` |
| System power-down voltage | 2600 mV | `:50` |
| VBUS input limit | 4.36 V / **1500 mA** | `:46`–`:47` |
| Low-battery warning | 10 % | `:119` |
| PMIC watchdog | 4 s, IRQ to pin | `:110`–`:112` |
| Power key off / on hold | 4 s / 1 s | `:61`, `:76` |

These are **firmware defaults, not hardware limits** — a user program may change any
of them. `reported-working` (they are what the shipped code sets; not measured).

## See also

- [Device record](README.md)
- [Development, examples and firmware](development.md)
- [Conflicts and unresolved identities](gaps-and-conflicts.md)
- [Source table](sources.md)
- [Command ledger](commands.md)
- [Waveshare documentation-sourcing guide](../../../vendors/waveshare/README.md)
