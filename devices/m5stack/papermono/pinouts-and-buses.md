# PaperMono — pinouts, buses and architecture

> Board: M5Stack PaperMono, SKU C153. Hardware revision as documented:
> schematic **V0.6.2**, file dated 2026-05-22, PDF exported 2026-06-08 and last
> modified 2026-07-28.
> Research snapshot 2026-09-01.

Primary source for everything on this page is the official schematic,
[`artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf`](artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf),
read with [`tools/altium_pdf_pin_table.py`](../../../tools/altium_pdf_pin_table.py).
Where the vendor product page or the vendor firmware says something different,
both are given and the disagreement is recorded rather than settled by
preference.

**Read [`pin-naming-and-the-pyg-ambiguity.md`](pin-naming-and-the-pyg-ambiguity.md) before
using any `PYG*` name from vendor documentation.** The same token denotes
different pins on the two custom chips.

## Contents

- [Board set — this is not one PCB](#board-set--this-is-not-one-pcb)
- [ESP32-S3 complete pin map](#esp32-s3-complete-pin-map)
- [Pins that are not available](#pins-that-are-not-available)
- [I²C bus](#i²c-bus--the-one-shared-bus)
- [SPI buses](#spi-buses)
- [M5IOE1 expander pins](#m5ioe1-expander-pins)
- [M5PM1 power-manager pins](#m5pm1-power-manager-pins)
- [Connectors](#connectors)
- [Boot, reset and download mode](#boot-reset-and-download-mode)

## Board set — this is not one PCB

The schematic PDF concatenates **three separate Altium documents**, which is
directly visible in the title blocks and in the fact that reference designators
restart per document (there are three different `U1`s, two `X1`s, two `ANT1`s).
Treat a designator as meaningful only together with its sheet number.

| Sheets | Document | Title block | What it is |
|---|---|---|---|
| 1–4 | main project (title block left blank) | — | Main board: block diagram, power, MCU, peripherals |
| 5 | `PaperMono KEY RGB.SchDoc` | dated 2026-04-14 | Sub-board: 2 user keys, power button, RGB LED, PDM microphone |
| 6 | `02 Paper Mono NFC.SchDoc` | rev **V0.2**, dated 2026-07-28, marked **sheet 2/2** | Sub-board: ST25R3916 NFC reader, its crystal and antenna |

**Sheet 1 of 2 of the NFC document is not present in the published PDF.** The
included sheet is explicitly numbered `2/2`. This is an omission in the vendor's
export, not an absence of circuitry — treat NFC front-end details not visible on
sheet 6 as undocumented rather than as not-fitted. Recorded as an open gap in
[`gaps-and-conflicts.md`](gaps-and-conflicts.md).

Off-board assemblies reach the main board through connectors rather than being
drawn: the e-paper panel, the touch panel, the frontlight, and the LoRa module.

## ESP32-S3 complete pin map

The MCU is a bare **ESP32-S3R8** die in a 56-pin QFN (designator `U12`, sheet 3),
not a module — 8 MB in-package octal PSRAM, no in-package flash. Component
record: [`components/espressif/esp32-s3r8`](../../../components/espressif/esp32-s3r8/README.md).

Every row below was read from the schematic symbol. `—` means the pin carries no
net label on the sheet.

| GPIO | Pin | Net | Function | Notes |
|---|---|---|---|---|
| GPIO0 | 5 | `G0_BOOT_OUT` | Boot strap, driven by M5PM1 `BOOT_OUT_OD` | strapping pin |
| GPIO1 | 6 | `G1_PY_IRQ` | M5PM1 interrupt to host | |
| GPIO2 | 7 | `G2_KEY1` | User button A | also an M5PM1 wake source |
| GPIO3 | 8 | `G3_KEY2` | User button B | strapping pin; also an M5PM1 wake source |
| GPIO4 | 9 | `G4_TP_INT` | Touch controller interrupt | |
| GPIO5 | 10 | `G5_LoRa_INT` | LoRa `DIO1` / IRQ | |
| GPIO6 | 11 | `G6_RFID_INT` | ST25R3916 IRQ | |
| GPIO7 | 12 | `G7_PYB_IRQ` | M5IOE1 `OD_INTOUT` interrupt | |
| GPIO8 | 13 | `G8_TF_DATA3` | microSD DAT3 | |
| GPIO9 | 14 | `G9_TF_DATA2` | microSD DAT2 | |
| GPIO10 | 15 | `G10_TF_DATA1` | microSD DAT1 | |
| GPIO11 | 16 | `G11_TF_DATA0` | microSD DAT0 | |
| GPIO12 | 17 | `G12_TF_CMD` | microSD CMD | |
| GPIO13 | 18 | `G13_TF_CLK` | microSD CLK | 22 Ω series (`R35`) |
| GPIO14 | 19 | `G14_SPI2_MOSI` | E-paper SDA (SPI data) | |
| GPIO15 | 21 | `G15_SPI2_CLK` | E-paper SCL (SPI clock) | 22 Ω series (`R38`) |
| GPIO16 | 22 | `G16_EINK_CS` | E-paper CSB | |
| GPIO17 | 23 | `G17_EINK_DC` | E-paper D/C | |
| GPIO18 | 24 | `G18_EINK_BUSY` | E-paper BUSY_N | input |
| GPIO19 | 25 | `G19_USB_N` | USB D− | via `FT1` common-mode filter |
| GPIO20 | 26 | `G20_USB_P` | USB D+ | via `FT1` common-mode filter |
| GPIO21 | 27 | `G21_LoRa_BUSY` | LoRa `BUSY` | |
| GPIO26 | 28 | — | not connected | in-package flash CS, unused |
| GPIO33 | 38 | — | **reserved** | octal PSRAM |
| GPIO34 | 39 | — | **reserved** | octal PSRAM |
| GPIO35 | 40 | — | **reserved** | octal PSRAM |
| GPIO36 | 41 | — | **reserved** | octal PSRAM |
| GPIO37 | 42 | — | **reserved** | octal PSRAM |
| GPIO38 | 43 | `G38_SPI1_MOSI` | LoRa SPI MOSI | |
| GPIO39 | 44 | `G39_SPI1_CLK` | LoRa SPI CLK | 22 Ω series (`R34`) |
| GPIO40 | 45 | `G40_SPI1_MISO` | LoRa SPI MISO | |
| GPIO41 | 47 | `G41_LoRa_NSS` | LoRa chip select | |
| GPIO42 | 48 | `G42_BB_PWM` | Buzzer drive | |
| GPIO43 | 49 | `G43_U0_TX` | UART0 TX | 499 Ω series (`R30`) |
| GPIO44 | 50 | `G44_U0_RX` | UART0 RX | |
| GPIO45 | 51 | `G45_PDM_CLK` | PDM microphone clock | strapping pin |
| GPIO46 | 52 | `G46_PDM_DAT` | PDM microphone data | strapping pin |
| GPIO47 | 37 | `G47_SYS_SDA` | **System I²C SDA** | 2.2 kΩ pull-up (`R36`) |
| GPIO48 | 36 | `G48_SYS_SCL` | **System I²C SCL** | 2.2 kΩ pull-up (`R37`) |

Flash interface (dedicated pins, sheet 3): `SPICLK` p33 → `NOR_SCK`,
`SPICS0` p32 → `NOR_CS`, `SPID` p35 → `NOR_DI`, `SPIQ` p34 → `NOR_DO`,
`SPIWP` p31 → `NOR_WP`, `SPIHD` p30 → `NOR_HOLD`. Supply `VDD_SPI` p29.
`CHIP_PU` p4 carries `SOC_RESET`. Crystal `XTAL_P`/`XTAL_N` p54/p53 to a 40 MHz
`CN4040M000157A530001` with 24 pF loading caps.

This matches the vendor product page's pin tables everywhere the two overlap.
The schematic additionally establishes **USB (GPIO19/20)** and **UART0
(GPIO43/44)**, which the product page does not list at all.

### Prose: what this map means in practice

Nearly every GPIO is committed. Of the 45 pins the ESP32-S3 brings out on this
package, five are consumed by in-package octal PSRAM, six by the microSD slot in
4-bit mode, five by the e-paper, six by LoRa, two by USB, two by UART0, two by
I²C, two by the microphone, one by the buzzer, and the remainder by buttons and
the six interrupt lines from the expander, power manager, touch, IMU, RTC and
NFC. **There is no free GPIO on a header, and there is no expansion header at
all** — unlike most M5Stack cores, the PaperMono exposes no Grove or M-Bus
connector. Any additional peripheral has to go on the shared I²C bus or take
over one of the M5IOE1's expander pins.

The consequence for firmware authors is that the M5IOE1 is not an optional
convenience. Panel power, panel reset, touch power, touch reset, microSD power,
card detect, microphone power, NFC enable, LoRa reset, LoRa antenna switch, two
of the three LED colours and the charger's bus gate are *all* behind it. Losing
I²C means losing the ability to power-cycle the display.

## Pins that are not available

| Pins | Why |
|---|---|
| GPIO33–GPIO37 | Octal PSRAM. The ESP32-S3**R8** carries 8 MB OPI PSRAM in package and these five pins are consumed by it. |
| GPIO26 | In-package flash chip select on other ESP32-S3 variants; unconnected here. |
| GPIO22–GPIO25, GPIO27–GPIO32 | Do not exist on the ESP32-S3. |

**Octal PSRAM is a hard build requirement, not a preference.** M5GFX aborts
display initialisation with `"M5PaperMono need OPI-PSRAM enabled"` if the build
does not select it. The failure presents as a blank screen on an otherwise
working board with a single log line — a build misconfiguration that looks like
dead hardware. Set `board_build.arduino.memory_type = qio_opi`.

## I²C bus — the one shared bus

A single I²C bus on **GPIO47 (SDA) / GPIO48 (SCL)**, pulled up by 2.2 kΩ to
`3V3_L2`, carries seven devices.

| Address | Device | Component record | Notes |
|---|---|---|---|
| `0x32` | RX8130CE RTC | [record](../../../components/seiko-epson/rx8130ce/README.md) | `nIRQ` → M5PM1 G0 |
| `0x38` | FT6336G touch | [record](../../../components/focaltech/ft6336g/README.md) | on the touch FPC |
| `0x4F` | M5IOE1 I/O expander | [record](../../../components/m5stack/m5ioe1/README.md) | address is **undocumented** — see below |
| `0x50` | ST25R3916 NFC | [record](../../../components/stmicroelectronics/st25r3916/README.md) | on the NFC sub-board |
| `0x68` | BMI270 IMU | [record](../../../components/bosch-sensortec/bmi270/README.md) | alternate `0x69`; bus clocked at **100 kHz** for this device |
| `0x6E` | M5PM1 power manager | [record](../../../components/m5stack/m5pm1/README.md) | |
| `0x75` | IP2315 charger | [record](../../../components/injoinic/ip2315/README.md) | **normally gated off the bus** — see below |

All seven addresses were confirmed both in the vendor firmware source and on the
vendor product page; none conflict.

**Two traps on this bus.**

*The charger is not always present.* The IP2315's I²C mode depends on its bus
pins being pulled to `VBAT`, and the vendor documents that a low battery can
leave it failing to enter I²C mode and disturbing everyone else on the bus. The
M5IOE1's `IO11` (`PYB_CHG_IIC`) gates the charger onto the bus, and the vendor's
guidance is to attach it only for the duration of a transaction. A scan that does
not first assert that gate will simply not find `0x75`, and that is correct
behaviour, not a fault. The IP2315 datasheet additionally documents a bus-lockup
mechanism involving a missing NACK on the final read byte, which is presumably
why the gate exists at all.

*The expander's address is not in its own manual.* Everything — firmware,
product page, this board — uses `0x4F`, but the M5IOE1 V1.4 manual states the
address range `0x6F`–`0x76` in three separate places, and the chip's `IO7` is
genuinely wired to an `ADD_SET` divider. The vendor library constant is even
named `..._ADDR_2` and its autodetect sweeps both ranges. Unresolved; see
[`gaps-and-conflicts.md`](gaps-and-conflicts.md).

## SPI buses

Two SPI peripherals plus the dedicated flash interface.

| Bus | Signals | Device | Clock |
|---|---|---|---|
| SPI2 | GPIO14 MOSI, GPIO15 CLK, GPIO16 CS, GPIO17 DC, GPIO18 BUSY | E-paper (SSD1677) | M5GFX drives **40 MHz**; vendor OTP demo uses 20 MHz |
| SPI1 | GPIO38 MOSI, GPIO39 CLK, GPIO40 MISO, GPIO41 NSS | Stamp LoRa-1262 | RadioLib default |
| SPI0 | dedicated `SPICLK/CS0/D/Q/WP/HD` | XM25UH128DHIQT 16 MB NOR flash | quad-capable |

The e-paper link is **write-only** — there is no MISO, and status is read
through the `BUSY` line alone.

**A clock conflict worth knowing about.** M5GFX runs the panel at 40 MHz, while
the SSD1677 datasheet (§12.1) and the DKE panel manual (p. 16) *both* state a
20 MHz maximum write clock, and the vendor's own OTP demo uses 20 MHz. This may
be a factor in the refresh instability M5Stack itself warns about. Recorded as a
conflict; not tested on hardware.

Flash is wired for quad operation — all four data lines are routed — and the
`Q` in `XM25UH128DHIQT` denotes a factory-set QE bit. The vendor PlatformIO
snippet accordingly specifies `qio_opi`. The shipped factory image nevertheless
reports **DIO** in its header; since `sdkconfig.defaults` pins no flash mode,
that is an ESP-IDF default rather than a hardware limit. The hardware supports
QIO.

## M5IOE1 expander pins

I²C `0x4F`, interrupt on `OD_INTOUT` → ESP32-S3 GPIO7. Vendor firmware polls it
(`M5IOE1_INT_MODE_DISABLED`) rather than using the interrupt.

| Pin (symbol) | Net | Function |
|---|---|---|
| `PYG1` | `PYB_TF_DET` | microSD card detect (pulled up by the card's own power domain; low = inserted) |
| `PYG2_ADC1` | `PYB_LoRa_ANT_SW` | LoRa antenna switch |
| `PYG3` | `PYB_EPD_EN` | **E-paper 3.3 V rail enable** |
| `PYG4_ADC2` | `PYB_NFC_EN` | NFC enable |
| `PYG5_ADC3` | `PYB_EINK_RST` | E-paper reset |
| `PYG6` | `PYB_TP_RST` | Touch reset |
| `PYG7_ADC4` | `ADD_SET` | Own I²C address select |
| `PYG8_PWM2` | `PYB_LED_G` | RGB green |
| `PYG9_PWM1` | `PYB_LED_B` | RGB blue |
| `PYG10_PWM4` | `PYB_LoRa_RST` | LoRa reset |
| `PYG11_PWM3` | `PYB_CHG_IIC` | IP2315 I²C bus gate |
| `PYG12` | `PYB_PDM_EN` | Microphone power enable |
| `PYG13` | `PYB_TP_EN` | Touch power enable |
| `PYG14` | `PYB_TF_EN` | microSD power enable |

Two of these are **absent from the vendor product page's pin tables**: `PYG4`
(NFC enable, used by the firmware) and `PYG7` (`ADD_SET`). The product page is
otherwise complete and accurate.

> **Off-by-one.** In the vendor Arduino library `M5IOE1_PIN_3 = 2` — the label is
> 1-based, the enum value 0-based. `M5PM1_GPIO_NUM_3 = 3` does not do this.
> Passing a documentation `PYG<n>` straight into the M5IOE1 API silently reaches
> pin *n+1*.

## M5PM1 power-manager pins

I²C `0x6E`, interrupt on `G1_PY_IRQ` → ESP32-S3 GPIO1. Five GPIOs; see the
[component record](../../../components/m5stack/m5pm1/README.md) for the full
21-pad table and register map.

| Pin | Symbol name | Net | Function |
|---|---|---|---|
| 3 | `G0_WAKEin(INT0/2)_IRQout_NEOPIXEL` | `PYG0_RTC_INT` | RTC alarm — wake source |
| 17 | `G1_IRQout_ADC` | `G1_PY_IRQ` | Interrupt out to host |
| 20 | `G2_WAKEin(INT0/2)_IRQout_ADC` | `PYG2_LoRa_EN` | LoRa rail enable |
| 13 | `G3_WAKEin(INT3/4)_IRQout_PWM` | `PYG3_BL_PWM` | **Frontlight brightness PWM** |
| 12 | `G4_WAKEin(INT3/4)_IRQout_PWM` | `PYG4_IMU_INT` | IMU interrupt — wake source |

Rail enables and analogue inputs are separate pins: `LDO3V3_EN_PP`,
`DCDC3V3_EN_PP`, `BOOST5V_EN_PP`, `CHG_EN_PP`, `BAT_ADC_EN_OD`, `BAT_ADC_IN`,
`5VIN_ADC_IN`, `5VOUT_ADC_IN`, `LED_EN_PP`, `BTN_PU`, `BOOT_OUT_OD`. See
[`power-architecture.md`](power-architecture.md).

The IMU and RTC interrupts land on the **power manager**, not on the ESP32-S3.
That is what allows the board to be woken from its deepest states by a motion
event or an alarm while the application processor is unpowered.

## Connectors

| Ref | Sheet | Part | Pins | Carries |
|---|---|---|---|---|
| `J5` | 4 | `FPC0.5-SMT-24P-B` | 24 | E-paper panel — SPI, BUSY, RST, DC, CS, and the panel's own boost rails (`GDR`, `RESE`, `VDHR`, `VSH`, `VGH`, `VSL`, `VGL`, `VCOM`) |
| `J4` | 4 | — | 8 | Touch panel FPC — `TP_SYS_SDA`, `TP_SYS_SCL`, `G4_TP_INT`, `PYB_TP_RST`, `TP_VDD` |
| `J1` | 2 | — | 6 | Frontlight — `PYG3_BL_PWM`, `BL_FB`, `BL_15V_L3B` |
| `J6` | 4 | `AXE512127D` | 12 + 4 tabs | Board-to-board to the KEY/RGB/PDM sub-board — keys, `PWR_BTN`, `PY_LED_R`, `PYB_LED_G/B`, PDM clock and data |
| `J3` | 4 | `BTB0.408-10PLBDR-G41` | 10 | Board-to-board to the NFC sub-board — I²C, `G6_RFID_INT`, `PYB_NFC_EN`, `3V3_L2` |
| `U14` | 4 | `Stamp-LoRa-1262-mini` | 13 | LoRa module — SPI, `SX_BUSY`, `LORA_IRQ`, `SX_NRST`, `SX_ANT_SW`, `VIN_3V3` |
| `J2` | 2 | `CON2_SMD` | 2 | Battery **only** — pin 2 `VBAT_L0`, pin 1 GND. **No thermistor pin**; see note below |
| `USB` | 2 | `TYPEC-302-BRP16SC08` | 16 | USB-C receptacle. **Its designator is the bare string `USB`, not `U1`** |

> **The battery connector has no NTC pin.** `J2` is a 2-contact part carrying
> only `VBAT_L0` and ground. The `100K-RNTC` thermistor is **`R15`, a mainboard
> component on the IP2315's `NTC` pin (26)** — so pack temperature is inferred
> from a thermistor near the charger, not sensed inside the cell. Whether `R15`
> is thermally coupled to the cell by layout is not established from the
> schematic. Earlier revisions of this record said "NTC-sensed at `J2`"; that was
> wrong. Source: [`bill-of-materials.md`](bill-of-materials.md).

The e-paper FPC pinout matches the DKE panel manual's Input/Output Pin
Assignment table (p. 7) position for position — an independent cross-check that
the schematic extraction is being read correctly.

**USB-C is power and data only.** The CC resistors are marked `NC` on the
schematic, so there is no USB-PD negotiation; combined with an upstream ~5.95 V
OVP this is a plain 5 V input.

## Boot, reset and download mode

- `CHIP_PU` is driven by `SOC_RESET`; the M5PM1 owns the reset.
- GPIO0 is driven by the M5PM1's open-drain `BOOT_OUT_OD`, so **the power
  manager, not a physical button, puts the ESP32-S3 into download mode.**
- Documented user procedure: hold the power button about 2 s until the red LED
  blinks, then release.
- Power on / reset: one short press. Power off: two presses in succession.
- GPIO3, GPIO45 and GPIO46 are strapping pins that also carry user button B and
  the PDM microphone. Driving the microphone or holding button B during reset
  perturbs straps; the vendor firmware does not appear to guard against this.
  `inferred` from the pin map, `not-tested`.

The product page and the Arduino tutorial page disagree about which control
enters download mode — the former says the power button, the latter refers to a
"reset button on the side". The schematic shows three switches on the KEY/RGB
sub-board (`S1` `PWR_BTN`, `S2` `G2_KEY1`, `S3` `G3_KEY2`) and no separate reset
button, which supports the power-button reading. Recorded in
[`gaps-and-conflicts.md`](gaps-and-conflicts.md).
