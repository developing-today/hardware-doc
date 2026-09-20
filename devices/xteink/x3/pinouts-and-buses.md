# Xteink X3 — pinouts and buses

> ESP32-C3. From `BoardConfig::XTEINK_X3` / `XTEINK_X3_UC8279`
> (**[SDK]** `BoardConfig.h:881–947`, commit `24003795381a6c23630a26472ae3b06550333e71`)
> and `XteinkDetect.cpp`. **Independently corroborated by a multimeter.**
> Retrieved **2026-09-04**.

Permalink:
`https://github.com/Free-Ink/freeink-sdk/blob/24003795381a6c23630a26472ae3b06550333e71/libs/hardware/BoardConfig/include/BoardConfig.h#L881-L947`

## The corroboration is unusual and worth stating

The Chinese teardown author writes:

> 主要管脚均使用万用表测量，并于crosspoint项目代码进行交叉验证。
> *"The main pins were all measured with a multimeter and cross-validated against
> the CrossPoint project source code."*
> — [`sunwoods/Xteink-X3`](https://github.com/sunwoods/Xteink-X3) README

That makes the X3 pinout the **only one in this family with independent physical
verification**. He also credits CrossPoint for part numbers he could not read
directly, so the **BOM** is a mix of direct reading and borrowed identification —
treat individual part numbers with more caution than the pins.

## Complete GPIO map

| GPIO | Signal | Dir | Bus / role | Notes |
|---:|---|---|---|---|
| **0** | Battery voltage ADC **and** I²C **SCL** | — | **dual-assigned** | See conflict below |
| **1** | Button ADC ladder group 1 | in | ADC1_CH1 | Back / Confirm / Left / Right |
| **2** | Button ADC ladder group 2 | in | ADC1_CH2 | Up / Down |
| **3** | Power button | in | digital | active-LOW |
| **4** | EPD **DC** | out | display | |
| **5** | EPD **RST** | out | display | |
| **6** | EPD **BUSY** | in | display | |
| **7** | SD **MISO** | in | shared SPI | |
| **8** | **SCLK** | out | shared SPI | display **and** SD |
| **10** | **MOSI / SDA** | out/io | shared SPI | display **and** SD. Released to input for the controller-ID read |
| **12** | SD **CS** | out | shared SPI | |
| **13** | **SD power enable** | out | power | **active-HIGH.** `digitalWrite(13,HIGH)` in setup; **LOW** on every deep sleep |
| **20** | I²C **SDA** — *and* `usbDetect` | io | **dual-assigned** | See conflict below |
| **21** | EPD **CS** | out | display | |

## Two dual-assignment conflicts in the SDK

| GPIO | Assignment A | Assignment B |
|---:|---|---|
| **0** | `batteryAdc = 0` (ADC1_CH0, ÷2 divider) | `X3_I2C_SCL = 0` |
| **20** | `usbDetect = 20` | `X3_I2C_SDA = 20` |

Both pins are given two roles in the **same SDK, same commit**. These cannot both
be live simultaneously.

**Most likely reading:** the `batteryAdc` and `usbDetect` fields were **copied from
the X4 profile** when the X3 profile was created, and are dead on this board —
the X3 has a **BQ27220 fuel gauge** and does not need an ADC for battery voltage
at all. That is a hypothesis with a strong motive, **not a finding.**

**What would settle it:** reading the schematic sketch
(`artifacts/teardown/sunwoods-cn/02.jpg`) for what GPIO0 and GPIO20 connect to, or
a continuity check. **The schematic is held in this repository and has not been
read in detail** — the cheapest open action on this device.

## Display bus

| Signal | GPIO |
|---|---:|
| SCLK | **8** |
| MOSI / SDA | **10** |
| CS | **21** |
| DC | **4** |
| RST | **5** |
| BUSY | **6** |

**Identical to the X4.** Only the controller and the panel geometry differ.

Clock **20 MHz** — UC8253 datasheet maximum (*"Clock rate up to 20 MHz"*, serial
write timing `TSCYCW`; the SDK cites
`https://www.elecrow.com/download/product/DIE01237S/UC8253_Datasheet.pdf`).
UC8279 is rated the same. A prior fork (Witch Reader) ran a conservative
**16 MHz**; 20 MHz is in-spec and ~25 % faster on plane writes.

### Controller fingerprint

`detectX3DisplayController()` bit-bangs a half-duplex 4-wire read on
**SCLK 8 / SDA 10 / CS 21 / DC 4 / RST 5 / BUSY 6** after a reset pulse, and reads
UC8279 **`VER (0x70)`** — reserved `0x00`, `CHIP_VER` (datasheet default `0x03`),
24-bit `LUT_VER` — plus **`FLG (0x71)`**.

Match requires: leading `0x00`, a non-floating `CHIP_VER`, and `FLG` idle with
`BUSY_N = 1` — **in two passes that agree byte-for-byte**. Anything else
conservatively resolves to the shipping **UC8253**.

**Two `Pending` items are recorded honestly by the SDK:** what the UC8253 actually
answers to `0x70`, and whether production MTP programs `CHIP_VER` to something
other than `0x03` (which is why the matcher deliberately does not pin the value).

## SD card — shared SPI, but with a power rail

| Signal | GPIO |
|---|---:|
| SCLK | **8** (shared with display) |
| MOSI | **10** (shared) |
| MISO | **7** |
| CS | **12** |
| **powerEnable** | **13**, **active-HIGH** |

The power enable is the X3's advantage over the X4, and the SDK explains exactly
why it matters:

> "Confirmed by X3 factory-firmware RE: `setup()` does `digitalWrite(13,HIGH)`;
> every deep-sleep does `digitalWrite(13,LOW)`. Without declaring it,
> `powerDownRailsForSleep()` has no X3 SD enable to cut, so **the card stays
> powered through sleep → battery drain**."

**Note the polarity difference from the S3 devices:** GPIO13 here is
**active-HIGH**; the X4 Pro's GPIO5 and the X4 Classic's GPIO6 are **active-LOW**.
And on the **X4**, GPIO13 is the **battery MOSFET latch**, a completely different
function. Three models, same pin number, three meanings — **never port power code
between them.**

## I²C bus — SDA 20 / SCL 0 @ 400 kHz

| Address | Device | Component | Probe used by `XteinkDetect` |
|---|---|---|---|
| **0x55** | **BQ27220** fuel gauge | [`texas-instruments/bq27220`](../../../components/texas-instruments/bq27220/README.md) | SoC reg `0x2C`, voltage reg `0x08` |
| **0x68** | **DS-series RTC** | [`unidentified/…/rtc-ds-series`](../../../components/unidentified/xteink-x3-x4/rtc-ds-series/README.md) | seconds reg `0x00` |
| **0x6B** (alt **0x6A**) | **QMI8658** 6-axis IMU | [`qst/qmi8658a`](../../../components/qst/qmi8658a/README.md) | `WHO_AM_I` reg `0x00` == **`0x05`** |

**This bus is the X3/X4 discriminator.** One C3 binary serves both devices;
`XteinkDetect::detectXteinkVerdict()` scores the presence of these three parts.
Finding them → X3. Finding nothing → X4.

**Safety note:** this probe is compiled **only** for C3 profiles
(`#define FREEINK_XTEINK_C3 (FREEINK_DEVICE_X4 || FREEINK_DEVICE_X3)`). On an
ESP32-S3, GPIO20 is USB D+ and GPIO0 is a boot strap, so running it there would be
actively harmful.

## Input — ADC resistor ladder

**Identical to the X4** — GPIO1 (Back/Confirm/Left/Right) + GPIO2 (Up/Down),
power on GPIO3 active-LOW, `ADC_11db`. Same thresholds, same three-device
calibration data. See [`../x4/features/buttons.md`](../x4/features/buttons.md).

Owner-reported difference: the X3's buttons are *"somewhat mushy and quieter"*
than the X4's — a moulding/switch difference, not an electrical one.

## NFC

An **ISO/IEC 14443A tag** is on the board (**[CN]** BOM) and NFC is an advertised
feature (**[VENDOR]** launch announcement). It is a **passive tag** — it appears on
no host bus, in no board profile, and in no firmware. See
[`features/nfc.md`](features/nfc.md).

## Resource conflicts

| Resource | Contenders |
|---|---|
| SPI 8/10 | EPD **and** microSD — only CS separates them |
| GPIO10 | SPI MOSI **and** the half-duplex controller-ID read (released to input) |
| GPIO0 | `batteryAdc` **and** I²C SCL — **unresolved** |
| GPIO20 | `usbDetect` **and** I²C SDA — **unresolved** |
| GPIO13 | SD rail (X3) vs battery latch (X4) vs unused (S3 models) |
| ADC1 | battery sense + two button ladders |
