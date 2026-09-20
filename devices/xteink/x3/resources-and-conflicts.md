# Xteink X3 — resources and conflicts

ESP32-C3, 16 MB flash, **no PSRAM**. Snapshot **2026-09-04**.

## GPIO allocation

| GPIO | Owner | Exclusive? |
|---:|---|---|
| **0** | **I²C SCL** — *and* `batteryAdc` in the profile | ❌ **contested** |
| 1 | Button ladder group 1 (ADC1_CH1) | shared ADC1 timing |
| 2 | Button ladder group 2 (ADC1_CH2) | shared ADC1 timing |
| 3 | Power button | ✅ |
| 4 | EPD DC | ✅ |
| 5 | EPD RST | ✅ |
| 6 | EPD BUSY | ✅ |
| 7 | SD MISO | ✅ |
| **8** | **SPI SCLK** | ❌ display + SD |
| **10** | **SPI MOSI / SDA** | ❌ display + SD; also released to input for the controller-ID read |
| 12 | SD CS | ✅ |
| **13** | **SD power enable, active-HIGH** | ✅ |
| **20** | **I²C SDA** — *and* `usbDetect` in the profile | ❌ **contested** |
| 21 | EPD CS | ✅ |

**No free GPIOs identified.**

## Two dual-assignments the SDK does not resolve

| Pin | Assignment A | Assignment B |
|---:|---|---|
| **0** | `batteryAdc = 0` (ADC1_CH0, ÷2 divider) | `X3_I2C_SCL = 0` |
| **20** | `usbDetect = 20` | `X3_I2C_SDA = 20` |

Same SDK, same commit `2400379`. **Both pairs cannot be live.**

**Hypothesis, not a finding:** `batteryAdc` and `usbDetect` were copied from the
[X4 profile](../x4/pinouts-and-buses.md) and are dead here — the X3 has a
**BQ27220 fuel gauge** and does not need an ADC battery sense at all.

**What would settle it:** the schematic sketch at
`artifacts/teardown/sunwoods-cn/02.jpg` — **held in this repository and not yet
read**. The cheapest unresolved question in the whole Xteink subject.

## Bus contention

**EPD and microSD share SCLK 8 / MOSI 10**, separated only by chip select
(`separateSpi = false`). Consequences are identical to the
[X4's](../x4/resources-and-conflicts.md): serialisation, per-transaction clock
renegotiation, and a controller-ID probe that must run before `EpdBus::begin()`
and release any retained GPIO hold on RST first.

**Unlike the X4, the X3 can power its card down** — see below.

## I²C bus — SDA 20 / SCL 0 @ 400 kHz

Three devices, one Arduino `Wire` controller (single-bus SoC, so `i2cBus` is
ignored):

| Address | Device | Consequence of a stalled bus |
|---|---|---|
| 0x55 | [BQ27220](../../../components/texas-instruments/bq27220/README.md) gauge | battery reading lost |
| 0x68 | [DS-series RTC](../../../components/unidentified/xteink-x3-x4/rtc-ds-series/README.md) | clock lost |
| 0x6B | [QMI8658](../../../components/qst/qmi8658a/README.md) IMU | motion page-turn lost |

**And board identification lost** — `XteinkDetect` uses exactly these three to
decide X3-vs-X4 at boot. A wedged I²C bus does not merely disable three sensors;
it can select the wrong board profile.

## ADC1 contention

Button ladder groups on GPIO1 and GPIO2, sequential reads, one global
`ADC_11db` attenuation. **Only one button per group is detectable at a time**;
cross-group chords work.

## Power domains

| Domain | Control | Note |
|---|---|---|
| **SD card** | **GPIO13, active-HIGH** | `setup()`: HIGH. Every deep sleep: LOW. **Omit the LOW and the card drains the battery through sleep** |
| Display | controller internal booster | No external PMIC |
| Battery charge | TP4056-class IC, **no host status GPIO declared** | Drives a red charge LED directly |

### GPIO13 means three different things across the family

| Device | GPIO13 |
|---|---|
| **X3** | **SD power enable, active-HIGH** |
| [X4](../x4/resources-and-conflicts.md) | **Battery MOSFET latch — LOW powers the device off** |
| X4 Pro / X4 Classic | unused (SD enables are GPIO5 / GPIO6, **active-LOW**) |

**Porting sleep code from an X4 to an X3 would drive GPIO13 LOW to "power off" and
instead merely cut the SD card. Porting the other way would cut power mid-write.**

## Memory and flash

SRAM ~400 KB · **PSRAM none** · flash 16 MB. Partition layout **not established
for the X3** — the X4's (`app0` 6400 KiB @ `0x10000`, `spiffs` 3456 KiB @
`0xC90000`) is a reasonable assumption and **has not been verified**.

**No PSRAM** is the binding constraint, and it is on this device that
**OTA out-of-memory was actually observed**.

## Panel-controller resource note

Units from ~July 2026 carry a **UC8279d** whose **LUT format is incompatible**
with the UC8253's: group-based 7-byte groups × 7 groups vs 43-byte LUTs. The X3's
six tuned waveform banks **cannot be copied over**, and grayscale is unavailable
until new banks are tuned. See [`features/display.md`](features/display.md).

## Realistic concurrent-use scenarios

| Scenario | Assessment | Status |
|---|---|---|
| Page turn while streaming from SD | **Serialised** — one SPI bus | Not benchmarked |
| Motion page-turn (IMU polling) + display refresh | IMU has **no interrupt**, so it must be polled during refresh | Not benchmarked |
| Wi-Fi + display refresh | Memory pressure likely; no PSRAM | **OTA is known to fail** |
| Deep sleep with card inserted | **Works — if firmware declares GPIO13** | Never measured |
| I²C poll + SPI transfer | Independent buses; no conflict expected | Untested |
