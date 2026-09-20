# Xteink X4 Pro — pinouts and buses

> Reconstructed from the FreeInk SDK board profile and its bring-up document,
> both of which are explicit about which lines were **probed on hardware** and
> which remain inferred from a firmware dump. Retrieved **2026-09-04**.

## Primary evidence

| Tag | Source | Pin |
|---|---|---|
| **[SDK]** | `Free-Ink/freeink-sdk` @ `24003795381a6c23630a26472ae3b06550333e71`, `libs/hardware/BoardConfig/include/BoardConfig.h`, `constexpr BoardProfile XTEINK_X4_PRO` at **lines 1495–1613** | commit-pinned |
| **[DOC]** | same commit, `docs/xteink-x4pro-support.md` | commit-pinned |
| **[HW]** | Marked *"Confirmed on hardware"* in **[DOC]** — bit-banged pin sweep, pull-up edge test, live I²C scan | — |
| **[RE]** | Ghidra analysis of the OEM flash dump, IROM offsets quoted in **[DOC]** | — |

Permalink to the profile:
`https://github.com/Free-Ink/freeink-sdk/blob/24003795381a6c23630a26472ae3b06550333e71/libs/hardware/BoardConfig/include/BoardConfig.h#L1495-L1613`

## Complete GPIO map

| GPIO | Signal | Dir | Bus / role | Notes | Evidence |
|---:|---|---|---|---|---|
| 0 | Button **Left** → Up / prev page | in | digital, active-LOW | **Boot strap** — fine as a button if not held at reset | **[HW]** `:1528` |
| 1 | **Master peripheral rail enable** | out | power | Driven HIGH **first** in board-init; panel + SD depend on it | **[RE]** `board_begin` IROM `0x420a23dc`; `:1606` |
| 2 | **Touch power enable** | out | power | **ACTIVE-LOW.** GT911 is unpowered and silent until this is LOW | **[HW]** `:1562, 1567` |
| 3 | Button **Power** | in | digital, active-LOW | `powerActiveHigh = false` | **[HW]** `:1528` |
| 4 | GT911 **RST** | out | touch | Earlier RE had 4/10 reversed; **corrected** | **[HW]** `:1552` |
| 5 | **SD power enable** | out | power | **ACTIVE-LOW.** Pulse HIGH 80 ms → LOW 120 ms, then hold LOW | **[HW]** `:1521` |
| 6 | EPD **BUSY** | in | display | Busy = **HIGH** | **[HW]** `:1509` |
| 7 | Button **Right** → Down / next page | in | digital, active-LOW | Reads `INPUT_PULLUP` — **not** a display enable | **[HW]** `:1528` |
| 8 | Frontlight **cool/white** | out | LEDC ch4 | active-HIGH | **[HW]** `:1577` |
| 9 | Frontlight **warm** | out | LEDC ch5 | active-HIGH | **[HW]** `:1577` |
| 10 | GT911 **INT** / address select | i/o | touch | Driven at reset to select address, then floated to input | **[HW]** `:1551` |
| 11 | EPD **MOSI** | out | display SPI | write-only, no MISO | **[HW]** `:1509` |
| 12 | EPD **SCLK** | out | display SPI | | **[HW]** `:1509` |
| 13 | EPD **CS** | out | display SPI | | **[HW]** `:1509` |
| 14 | EPD **RST** | out | display | | **[HW]** `:1509` |
| 18 | EPD **DC** | out | display | driven only for commands | **[HW]** `:1509` |
| 19 | USB **D−** | i/o | native USB-OTG | do not repurpose | **[DOC]** §RTC/USB/battery |
| 20 | USB **D+** | i/o | native USB-OTG | do not repurpose | **[DOC]** §RTC/USB/battery |
| 21 | Charger **STAT** | in | battery | **active-HIGH** = charging; input, no pull | **[RE]** `Cw2017PowerHal` vtable slot 3 → IROM `0x4214f67c`; `:1535, 1613` |
| 38 | I²C **SCL** | out | shared bus | 400 kHz | **[HW]** `:1550` |
| 39 | I²C **SDA** | i/o | shared bus | 400 kHz | **[HW]** `:1549` |
| 40 | SDMMC **DAT0** | i/o | storage | | **[HW]** `:1586` |
| 41 | SDMMC **CLK** | out | storage | | **[HW]** `:1586` |
| 42 | SDMMC **CMD** | i/o | storage | | **[HW]** `:1586` |
| 45 | (SD SPI CS, vestigial) | — | — | Retained in the SPI view only; unused once `busWidth != 0` | **[SDK]** `:1521` |

**Unassigned / unknown:** `batteryAdc` and `usbDetect` are both
`PIN_UNASSIGNED`. Battery monitoring exists in stock firmware but no ADC pin was
isolated, and no VBUS-presence signal was conclusively identified — stock derives
its battery icon from the GPIO21 charge state instead **[SDK]** `:1529, 1537`.

## Display bus

| Signal | GPIO | Notes |
|---|---:|---|
| SCLK | 12 | |
| MOSI | 11 | **write-only — there is no MISO** |
| CS | 13 | driven every byte in `writeCommand`/`writeData` |
| DC | 18 | LOW = command, HIGH = data |
| RST | 14 | |
| BUSY | 6 | input, busy = HIGH |

Clock: OEM uses **5 MHz**; FreeInk uses **20 MHz** (SSD1677 datasheet write max).
Native scan is 800×480 landscape, `NO_FLIP`.

**Because there is no MISO on the write path, the controller-ID probe releases
MOSI to input mid-transaction** and clocks the reply back on the same wire — a
half-duplex read. That is why the probe can work at all on a "write-only" bus
**[SDK]** `XteinkDetect.cpp:79–91`.

### The pin-map trap

Every early reverse-engineering pass read **app0**, which is a *different device
variant* (`ESP32S3_X4_TL`, Arduino-era, hardcoded pins). App0 gives **CS and DC
swapped, and SCLK/MOSI in the wrong order**. The device actually boots **app1**.
With the app0 map, the controller resets and runs full-length waveforms but never
develops an image — a failure mode that looks like a dead panel or a missing
power rail, and generated a long false "EPD PMIC / dead rails" investigation
before the pins were swept on hardware **[DOC]** §Root cause.

## I²C bus — SDA 39 / SCL 38 @ 400 kHz

| Address | Device | Component | Notes |
|---|---|---|---|
| **0x51** | BM8563 RTC (PCF8563-compatible) | [`generic/bm8563`](../../../components/generic/bm8563/README.md) | Class `XTEink::BM8563Driver` in the dump; init at IROM `0x420a2834` |
| **0x5D** (alt 0x14) | GT911 touch | [`goodix/gt911`](../../../components/goodix/gt911/README.md) | Only ACKs once GPIO2 is LOW **and** GPIO1 is HIGH |
| **0x63** | CW2017 fuel gauge | [`cellwise/cw2017`](../../../components/cellwise/cw2017/README.md) | **Not** a display PMIC — an early hypothesis said it was |

An idle scan of this bus with GPIO2 high shows **only 0x51 and 0x63**. The missing
GT911 is the diagnostic signature of an unpowered touch rail.

## Touch — GT911 details

| Property | Value |
|---|---|
| Reset dance | RST LOW + INT at select level, 2 ms → RST HIGH, 8 ms → INT to INPUT+pull, 60 ms, probe |
| Address select | INT level as RST rises: LOW → 0x5D |
| Config upload | **None.** The GT911 self-loads its internal config |
| Status register | `0x814E` — bit7 ready, low nibble = point count |
| Point data | from `0x8150`, 8 bytes each, **X-lo at byte 0** (`gt911CoordsAtByte0 = true`) |
| Mounting | **Portrait sensor on a landscape panel** — reports X:0–480, Y:0–800 → `swapXY = true` |
| Home key | GT911 capacitive key bit, status `0x814E & 0x10` — **not a GPIO** |

An earlier failure had the config registers reading back all-zero: the cause was a
**too-short reset** that never triggered the internal config load, not a missing
config table. The SDK's 10/10/50/50 ms sequence fixes it **[DOC]** §Touch.

## Storage — native SDMMC

| Signal | GPIO |
|---|---:|
| CLK | 41 |
| CMD | 42 |
| DAT0 | 40 |
| power enable | 5 (**active-LOW**) |

1-bit, slot 1, internal pull-ups, 40 MHz. DAT1/2/3 unused.
**SPI-mode CMD0 is silent on this slot** — an SPI card path can never work.

Mount sequence, both steps required:
1. Pulse GPIO5 HIGH (80 ms) → LOW (120 ms), then run `sdmmc_card_init`
   **and a real sector-0 read**, retrying the *whole* thing. Retrying only
   `card_init` leaves the first un-retried block read to fail with
   `sdmmc_read_sectors_dma … 0x107`.
2. **Leave GPIO5 LOW.** Driving it HIGH after init breaks every subsequent read.

Transfers bounce through a `MALLOC_CAP_DMA` buffer because SdFat caches may live
in PSRAM or be unaligned.

## Power rails and boot order

1. **GPIO1 HIGH** — master peripheral rail. First action in board-init.
2. **GPIO2 LOW** — touch rail on (active-low).
3. **GPIO5** pulsed HIGH→LOW — SD rail, held LOW.
4. Display reset and controller probe.

The sleep path drives each enable to its *off* level **by polarity**, so on this
board that means driving GPIO2 and GPIO5 **HIGH**.

## Resource conflicts and shared buses

| Resource | Shared by | Arbitration |
|---|---|---|
| I²C 39/38 | GT911, BM8563, CW2017 | One Arduino `Wire` controller (`i2cBus = 0`) for all three. No conflict, but all three stall if the bus is held |
| LEDC ch4/ch5 | frontlight only | Reserved; do not reuse for PWM elsewhere |
| GPIO0 | Button Left **and** the ESP32-S3 boot strap | Holding Left at reset enters download mode |
| GPIO19/20 | native USB only | **Never probe these.** The C3 X3/X4 detect fingerprint pokes SDA20/SCL0, which on this S3 lands on D+ and a boot strap — which is why `XteinkDetect` compiles the C3 fingerprint to a no-op unless a C3 profile is in the build **[SDK]** `XteinkDetect.cpp:13–19` |

## Bezel / viewable insets

`viewableInsets = {9, 7, 3, 7}` (top, right, bottom, left) **[SDK]** `:1612`.
7 px side inset is empirically tuned so an edge-hugging scrollbar stays visible;
top/bottom are **carried over from the X4 and are not measured**. Without these,
upstream firmware draws under the glass on this device.

## What is still unconfirmed

- **Panel mount orientation** — ships `NO_FLIP`, pending hardware.
- **`usbDetect`** — GPIO10 floated as a candidate, unconfirmed (and GPIO10 is
  already the GT911 INT, so this is unlikely and should be treated sceptically).
- **`batteryAdc`** — not isolated.
- **Touch `flipX`/`flipY`** — see [`gaps-and-conflicts.md`](gaps-and-conflicts.md);
  the SDK contradicts itself.
