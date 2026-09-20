# Xteink X4 Pro — resources and conflicts

ESP32-S3, 16 MB flash, **8 MB PSRAM**. Snapshot **2026-09-04**.

## GPIO allocation

| GPIO | Owner | Exclusive? | Note |
|---:|---|---|---|
| 0 | Button Left → up/prev | ⚠ | **also the S3 boot strap** |
| 1 | **Master peripheral rail**, HIGH | ✅ | asserted **first** at boot |
| 2 | **Touch power enable, ACTIVE-LOW** | ✅ | buttons on the X4 Classic |
| 3 | Button Power | ✅ | active-LOW |
| 4 | GT911 RST | ✅ | |
| 5 | **SD power enable, ACTIVE-LOW** | ✅ | buttons on the X4 Classic |
| 6 | EPD BUSY | ✅ | busy = HIGH |
| 7 | Button Right → down/next | ✅ | *not* a display enable — an earlier hypothesis, refuted |
| 8 | Frontlight **cool**, LEDC ch4 | ✅ | buttons on the X4 Classic |
| 9 | Frontlight **warm**, LEDC ch5 | ✅ | buttons on the X4 Classic |
| 10 | GT911 INT / address select | ⚠ | **also floated as a `usbDetect` candidate — almost certainly wrong** |
| 11 / 12 / 13 | EPD MOSI / SCLK / CS | ✅ | |
| 14 | EPD RST | ✅ | |
| 18 | EPD DC | ✅ | |
| 19 / 20 | USB D− / D+ | ✅ | **never probe** |
| 21 | Charger STAT, active-HIGH | ✅ | |
| 38 / 39 | I²C SCL / SDA @400 kHz | ❌ **three devices** | |
| 40 / 41 / 42 | SDMMC DAT0 / CLK / CMD | ✅ | |
| 45 | (SD SPI CS, vestigial) | — | unused once `busWidth != 0` |

**Unassigned:** `batteryAdc`, `usbDetect`, `display.powerEnable`.

## Boot ordering — this is load-bearing

1. **GPIO1 HIGH** — master peripheral rail. First action in board-init.
2. **GPIO2 LOW** — touch rail on (active-low).
3. **GPIO5** pulsed HIGH 80 ms → LOW 120 ms — SD rail, then **held LOW**.
4. Display reset, then the controller-ID probe, then `EpdBus::begin()`.

**Omitting step 1:** *"EPD BUSY never asserts, SD returns 0xFF."*
**Getting step 2's polarity wrong:** the GT911 never ACKs; an I²C scan shows only
0x51 and 0x63.
**Getting step 3 wrong:** every SD block read fails with `0x107`.

**Two active-LOW enables on one board is the opposite of the usual convention**
and is the single most common source of bring-up failure here.

## Shared buses

| Bus | Devices | Arbitration |
|---|---|---|
| **I²C 39/38 @400 kHz** | [GT911](../../../components/goodix/gt911/README.md) 0x5D · [BM8563](../../../components/generic/bm8563/README.md) 0x51 · [CW2017](../../../components/cellwise/cw2017/README.md) 0x63 | **One Arduino `Wire` controller** (`i2cBus = 0`). A stalled bus blocks touch, clock **and** battery |
| Display SPI 12/11/13 | EPD only | Dedicated. **Unlike the C3 models, the SD card does not share it** |
| SDMMC 41/42/40 | microSD only | Dedicated, 1-bit |

**The display and storage buses being independent is the X4 Pro's main structural
advantage over the [X4](../x4/resources-and-conflicts.md) and
[X3](../x3/resources-and-conflicts.md)**, where a card read stalls the panel.

## Peripheral resources reserved

| Resource | Owner |
|---|---|
| **LEDC channels 4 and 5** | Frontlight cool/warm. Do not reuse for other PWM |
| **SDMMC slot 1** | microSD |
| Native USB peripheral | CDC (and MSC in stock, unported) |
| DMA | **Both** the display path and SDMMC. Reads/writes bounce through a `MALLOC_CAP_DMA` buffer because SdFat's caches may sit in **PSRAM** or be unaligned |

## Memory

| Resource | Value |
|---|---|
| SRAM | 512 KB (ESP32-S3) |
| **PSRAM** | **8 MB, octal** |
| Flash | 16 MB |
| App partitions | 2 × 8064 KiB (dual-OTA) |
| SPIFFS | **80 KiB** — 40× smaller than the X4's |

PSRAM is why multi-buffer rendering and damage-window partial refresh are viable
here and not on the C3 models. It is also why the **DMA bounce buffer is
mandatory**: an SdFat cache allocated in PSRAM is not DMA-capable.

## Strap and USB hazards

| Pin | Hazard |
|---|---|
| **GPIO0** | Boot strap **and** the Left button. Powering on with Left held enters download mode |
| **GPIO19/20** | Native USB D−/D+. The **C3 Xteink device fingerprint pokes SDA 20 / SCL 0**, which on this S3 lands on **D+ and a boot strap**. `XteinkDetect` compiles that path out unless a C3 profile is in the build — **a build defining both a C3 and this profile would be dangerous** |

## Cross-model porting hazards

| Pin | X4 Pro | X4 Classic | Consequence of porting blindly |
|---:|---|---|---|
| 2 | Touch power (out, active-LOW) | **Button** (in) | Driving a button pin as an output |
| 5 | SD power (out, active-LOW) | **Button** (in) | Same |
| 8 / 9 | **Frontlight PWM** (out) | **Buttons** (in) | LEDC configured on button inputs |
| 6 | **EPD BUSY** (in) | **SD power** (out) | Panel never appears ready |
| 14 | **EPD RST** | **EPD DC** | Panel resets and never develops an image |
| 18 | **EPD DC** | **EPD BUSY** | Same |
| 10 | **GT911 INT** | **EPD RST** | Same |

**Seven pins change meaning between two boards that share a chassis, a panel and
an SoC.** Always gate on `FREEINK_CAP_TOUCH` / `FREEINK_CAP_FRONTLIGHT` and take
pins from the active `BoardProfile`, never from a constant.

## Realistic concurrent-use scenarios

| Scenario | Assessment | Status |
|---|---|---|
| Display refresh **+** SD read | Independent buses, but **both DMA-heavy**; SD adds a bounce copy | **Not benchmarked** |
| Touch poll **+** RTC read **+** gauge read | One `Wire` controller, sequential | **Not benchmarked** |
| Frontlight PWM **+** Wi-Fi | LEDC + radio on one battery of **unknown capacity** | **Not benchmarked** |
| BLE **+** Wi-Fi | One 2.4 GHz radio, shared | **Not benchmarked** |
| Deep sleep | Enables driven to off level **by polarity** (GPIO2/5 → HIGH) | Implemented; **power draw never checked** |

## Unresolved

- **`usbDetect`** — unassigned; GPIO10 floated as a candidate but it is already
  the GT911 INT. Treat that candidacy as wrong.
- **`batteryAdc`** — not isolated. Battery percentage comes from the CW2017.
- **Touch `flipX`/`flipY`** — the SDK's header and its own device document
  disagree. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md).
