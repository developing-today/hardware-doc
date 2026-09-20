# Xteink X4 — pinouts and buses

> ESP32-C3. Reconstructed from `BoardConfig::XTEINK_X4`
> (**[SDK]** `BoardConfig.h:844–874`, commit `24003795381a6c23630a26472ae3b06550333e71`)
> and `InputManager` for the ADC ladder. Retrieved **2026-09-04**.

Permalink:
`https://github.com/Free-Ink/freeink-sdk/blob/24003795381a6c23630a26472ae3b06550333e71/libs/hardware/BoardConfig/include/BoardConfig.h#L844-L874`

Corroboration: the [X3 teardowns](../x3/media.md) are of the **same board family**
and their author states the main pins were *"measured with a multimeter and
cross-checked against the CrossPoint project source"*.

## Complete GPIO map

| GPIO | Signal | Dir | Bus / role | Notes |
|---:|---|---|---|---|
| **0** | **Battery voltage ADC** | in | ADC1_CH0 | `batteryDividerMultiplier = 2.0` |
| **1** | **Button ADC ladder group 1** | in | ADC1_CH1 | Back / Confirm / Left / Right |
| **2** | **Button ADC ladder group 2** | in | ADC1_CH2 | Up / Down |
| **3** | **Power button** | in | digital | active-LOW (`INPUT_PULLUP`) |
| **4** | EPD **DC** | out | display | |
| **5** | EPD **RST** | out | display | |
| **6** | EPD **BUSY** | in | display | |
| **7** | SD **MISO** | in | shared SPI | the only SD-specific data line |
| **8** | **SCLK** | out | **shared SPI** | display **and** SD |
| **10** | **MOSI** | out | **shared SPI** | display **and** SD |
| **12** | SD **CS** | out | shared SPI | |
| **13** | **Battery MOSFET latch** | out | power | HIGH = hold; **LOW = power off** |
| **20** | `usbDetect` | in | USB | **see the conflict note below** |
| **21** | EPD **CS** | out | display | |

`batteryChargeStatus`, `sd.powerEnable`, `display.powerEnable`: **unassigned**.

### GPIO20 — an unresolved conflict

The X4 profile sets `usbDetect = 20`. On the **X3**, which shares this board
layout, **GPIO20 is the I²C SDA line** (`X3_I2C_SDA = 20`,
**[SDK]** `XteinkDetect.cpp`). The X4 has no I²C peripherals, so the pin is free
here — but the two profiles assign the same physical pin two different roles, and
**neither assignment is marked hardware-confirmed**.

Most likely reading: the X4 genuinely uses GPIO20 for USB presence and the X3
repurposed it for I²C when the RTC/gauge/IMU were added. **Not verified.** See
[`gaps-and-conflicts.md`](gaps-and-conflicts.md).

## Display bus

| Signal | GPIO |
|---|---:|
| SCLK | **8** |
| MOSI | **10** |
| CS | **21** |
| DC | **4** |
| RST | **5** |
| BUSY | **6** |
| powerEnable | — |

**Clock policy, quoted from the source:**

```c
// BoardConfig.h:830-843
// Default 20 MHz = SSD1677 datasheet max for write mode … The plane writes are
// ~38 ms/refresh at 20 MHz. Define -DFREEINK_X4_OVERCLOCK_SPI to run 40 MHz — the
// (out-of-spec, 2x datasheet) clock the CrossPoint / Witch Reader fork used, which
// halves that to ~19 ms … but can glitch plane writes on marginal wiring.
```

The SDK cites the SSD1677 datasheet directly:
`https://files.waveshare.com/upload/2/2a/SSD1677_1.0.pdf` — *"MCU interface: SPI
serial peripheral, Maximum 20 MHz for write"*.

**Note a trap:** `Ssd1677Driver`'s own 0-default is **40 MHz**, so any board that
leaves `displaySpiHz = 0` silently runs out of spec.

## SD card — shares the display SPI bus

| Signal | GPIO |
|---|---:|
| SCLK | **8** (shared) |
| MOSI | **10** (shared) |
| MISO | **7** |
| CS | **12** |
| powerEnable | **none** |

`separateSpi = false`, `spiHz = 0` (SD manager default, 40 MHz).

**Consequence:** the panel and the card contend for one bus. There is no
arbitration beyond chip select, so a large card read stalls display updates.
Unlike the [X3](../x3/pinouts-and-buses.md), the X4 has **no SD power enable**, so
the card cannot be powered down for sleep.

## Input — the ADC resistor ladder

`InputStyle::XteinkAdcLadder`. Six buttons on **two** ADC pins.

**[SDK]** `InputManager.h:73–74, 411–414` and `InputManager.cpp:29–45`.

### Group 1 — GPIO1, four buttons

Recorded raw 12-bit values from three real devices:

| | BACK | CONFIRM | LEFT | RIGHT |
|---|---:|---:|---:|---:|
| unit 1 | 3597 | 2760 | 1530 | 6 |
| unit 2 | 3470 | 2666 | 1480 | 6 |
| unit 3 | 3470 | 2655 | 1470 | 3 |
| **average** | **3512** | **2694** | **1493** | **5** |

Decision thresholds are the midpoints of adjacent averages:

```c
const int InputManager::ADC_RANGES_1[] = {ADC_NO_BUTTON, 3100, 2090, 750, INT32_MIN};
```
Button `i` is pressed when `ranges[i+1] < adc <= ranges[i]`.

### Group 2 — GPIO2, two buttons

```c
const int InputManager::ADC_RANGES_2[] = {ADC_NO_BUTTON, 1120, INT32_MIN};
// local index 0/1 is remapped to BTN_UP / BTN_DOWN by adding 4
```

### Setup

```c
pinMode(1, INPUT); pinMode(2, INPUT);
pinMode(3, INPUT_PULLUP);          // power, active-LOW
analogSetAttenuation(ADC_11db);
```

**Only one button per group is detectable at a time** — a resistor ladder produces
one voltage. Chords across the two groups work; chords within a group do not.

The `InputPins` struct values `{0,1,2,3,4,5,3,false}` are **logical button indices,
not GPIOs**, for every field except `power` (GPIO3). Reading them as pin numbers is
an easy and serious mistake.

## Power

| Rail | GPIO | Note |
|---|---:|---|
| Battery MOSFET latch | **13** | Assert HIGH to hold power. **Drive LOW to power off** |
| Battery sense | 0 | ADC, ÷2 divider |

**Two board revisions exist.** Most units self-latch through a pull once the power
button bridges the rail, so firmware never needed to assert GPIO13. **At least one
field revision does not self-latch and stays powered only while the button is
held.** Asserting the latch is harmless on self-latching units — always do it.

Note the same GPIO13 is the **SD power enable on the X3**. The X4 keeps it as
`power.latch0`, driven by the consumer's sleep path, and it is *"left unchanged"*
by the SD code.

## Resource conflicts

| Resource | Contenders | Note |
|---|---|---|
| SPI bus (8/10) | EPD **and** microSD | Only CS separates them |
| GPIO13 | Power latch (X4) vs SD rail (X3) | **Same pin, different meaning per model** — do not port blindly |
| GPIO20 | `usbDetect` (X4) vs I²C SDA (X3) | Unresolved |
| ADC1 | GPIO0 battery + GPIO1/2 buttons | Three channels of one ADC; sequential reads |

## Absent

No I²C bus, no RTC, no fuel gauge, no IMU, no touch, no frontlight, no SDMMC, no
audio, no LEDs, no NFC. `NO_SENSORS`, `NO_GAUGE`, `NO_TOUCH`, `NO_FRONTLIGHT`,
`NO_AUDIO`, `NO_LEDS`, `NO_SDMMC`, `NO_MIC`.

**This absence is itself the X3/X4 runtime discriminator**: `XteinkDetect` probes
SDA20/SCL0 for a BQ27220 (0x55), DS3231 (0x68) and QMI8658 (0x6B). Finding them
means X3; finding nothing means X4.
