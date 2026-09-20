# Xteink X4 — resources and conflicts

ESP32-C3, 16 MB flash, **no PSRAM**. Snapshot **2026-09-04**.

## GPIO allocation — every pin accounted for

| GPIO | Owner | Exclusive? | Notes |
|---:|---|---|---|
| 0 | Battery voltage ADC (ADC1_CH0) | shared with ADC1 timing | ÷2 divider |
| 1 | Button ladder group 1 (ADC1_CH1) | shared with ADC1 timing | Back/Confirm/Left/Right |
| 2 | Button ladder group 2 (ADC1_CH2) | shared with ADC1 timing | Up/Down |
| 3 | Power button | ✅ | active-LOW |
| 4 | EPD DC | ✅ | |
| 5 | EPD RST | ✅ | |
| 6 | EPD BUSY | ✅ | |
| 7 | SD MISO | ✅ | the only SD-exclusive data line |
| **8** | **SPI SCLK** | ❌ **display + SD** | |
| **10** | **SPI MOSI** | ❌ **display + SD** | also released to input for the controller-ID probe |
| 12 | SD CS | ✅ | |
| 13 | Battery MOSFET latch | ✅ | **LOW = power off** |
| 20 | `usbDetect` | ⚠ **contested** — see below | |
| 21 | EPD CS | ✅ | |

**No free GPIOs are identified.** Anyone wanting to add hardware to an X4 is
taking a pin away from something.

## The one real bus conflict

**The e-paper controller and the microSD card share SCLK 8 and MOSI 10**, separated
only by chip select (`sd.separateSpi = false`).

| Consequence | Detail |
|---|---|
| **Serialisation** | A large card read stalls display refresh and vice versa. There is no arbitration beyond CS |
| **Clock renegotiation** | The panel wants ≤20 MHz (or 40 MHz overclocked); the SD manager defaults to 40 MHz. The bus is reconfigured per transaction |
| **Probe timing** | The controller-ID probe releases MOSI to **input** mid-transaction for a half-duplex read. It must run **before** `EpdBus::begin()` and must first `gpio_hold_dis()` the RST pin, or a retained sleep-path latch makes every `digitalWrite` silently bounce and the probe selects the wrong driver |

The [X3](../x3/pinouts-and-buses.md) shares this design. The S3 devices moved the
card to **native SDMMC on dedicated pins**, which is the single biggest
architectural improvement between generations.

## ADC1 contention

Three functions on one ADC: battery sense (GPIO0) and both button ladder groups
(GPIO1, GPIO2). Reads are sequential. `analogSetAttenuation(ADC_11db)` is set
globally, so **the battery divider and the button ladder share an attenuation
setting** — you cannot tune one without the other.

**Only one button per ladder group is detectable at a time.** A resistor ladder
produces one voltage; two simultaneous presses in the same group yield a third,
wrong reading. Cross-group chords (e.g. Left + Up) work.

## Memory

| Resource | Value |
|---|---|
| SRAM | ~400 KB (ESP32-C3) |
| **PSRAM** | **None** |
| Flash | 16 MB |
| App partitions | 2 × 6400 KiB (dual-OTA) |
| SPIFFS | 3456 KiB |

**The absence of PSRAM is the binding constraint.** It is the documented cause of
OTA out-of-memory failures on this SoC class, and it is why the S3 devices can do
multi-buffer rendering and damage-window partial refresh and this one cannot.

## Flash partition map

`nvs` `0x009000` (20 KiB) · `otadata` `0x00E000` (8 KiB) ·
`app0` `0x010000` (6400 KiB) · `app1` `0x650000` (6400 KiB) ·
`spiffs` `0xC90000` (3456 KiB) · `coredump` `0xFF0000` (64 KiB).

Parsed directly from the factory dump. **Different from the X4 Pro's**
(`0x7E0000` app slots, 80 KiB SPIFFS) — the X4 devotes ~40× more space to SPIFFS,
consistent with serving a web file-manager UI from flash.

## Power domains

| Domain | Control | Note |
|---|---|---|
| Battery → system | **GPIO13 MOSFET latch** | **Two board revisions behave differently** — see below |
| SD card | **none** | **The card cannot be powered down.** Structural sleep drain |
| Display | none — controller's internal booster (`0x0C` soft-start) | No external PMIC, no charge pump |

## Unresolved conflicts

### GPIO20 — `usbDetect` or I²C SDA?

`XTEINK_X4` sets `usbDetect = 20`. The X3 profile — same board family — sets
**both** `usbDetect = 20` **and** `X3_I2C_SDA = 20`. The X4 has no I²C
peripherals so the pin is free here, but **neither assignment is marked
hardware-confirmed**, and the X4's may simply be inherited from a template.

**Resolution:** scope GPIO20 during USB plug/unplug, or continuity-check it to the
USB-C connector.

### GPIO13 means three different things across the family

| Device | GPIO13 |
|---|---|
| **X4** | **Battery MOSFET latch.** Drive LOW to power off |
| [X3](../x3/pinouts-and-buses.md) | **SD power enable, active-HIGH** |
| X4 Pro / X4 Classic | unused (their SD enables are GPIO5 / GPIO6, **active-LOW**) |

**Never port power or sleep code between these devices without re-checking.**

### Two X4 board revisions, indistinguishable

Most units **self-latch** through a pull once the power button bridges the rail,
so firmware never needed to assert GPIO13. **At least one field revision does not
self-latch and stays powered only while the button is held.** Asserting the latch
is a no-op on self-latching units — **always assert it**.

**There is no known revision marking.** This is the most operationally important
unknown about the device.

## Realistic concurrent-use scenarios

| Scenario | Assessment | Status |
|---|---|---|
| Page turn while streaming from SD | **Serialised** — one SPI bus | Not benchmarked |
| Wi-Fi download + display refresh | Memory pressure likely (no PSRAM) | Not benchmarked |
| OTA while low on heap | **Known to fail** on this SoC class | Reported |
| Battery read during button poll | Sequential ADC1 reads; shared attenuation | Not benchmarked |
| Deep sleep with an SD card inserted | **Card stays powered — no enable pin** | Never measured |
