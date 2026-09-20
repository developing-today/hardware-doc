# Xteink X4 Classic — pinouts and buses

> ESP32-S3. Reconstructed **entirely from a stock flash dump** (`flashx4c.bin`,
> app0 = `xteink_app` v7.0.11) by the FreeInk maintainers. **No schematic, no
> teardown, no photograph of this board exists.** Retrieved **2026-09-04**.

## Evidence and how it was decoded

| Tag | Source |
|---|---|
| **[SDK]** | `Free-Ink/freeink-sdk` @ `24003795381a6c23630a26472ae3b06550333e71`, `BoardConfig.h` **L1615–1706** |
| **[DOC]** | same commit, `docs/xteink-x4c-support.md` |
| **[RE]** | Ghidra analysis of `flashx4c.bin`; IROM offsets quoted below |

Permalink:
`https://github.com/Free-Ink/freeink-sdk/blob/24003795381a6c23630a26472ae3b06550333e71/libs/hardware/BoardConfig/include/BoardConfig.h#L1615-L1706`

**The decoding method is worth recording**, because it is reusable on any
ESP-IDF/Arduino firmware dump. A single board-init function `FUN_4214c798`
registers every GPIO through one config call whose **mode argument is an opaque
integer**. The maintainers recovered its meaning by **cross-referencing pins whose
role was already unambiguous**:

| Mode value | Meaning | Deduced from |
|---:|---|---|
| **0** | plain `INPUT` | the charge-STAT line, which cannot be an output |
| **1** | `OUTPUT` | the SPI drive lines and the GPIO1 rail, which must be outputs |
| **2** | input + ISR | the buttons, which are interrupt-attached |

That is a clean example of proving an encoding from the constrained cases rather
than assuming it.

## Complete GPIO map

| GPIO | Signal | Dir | Role | Confidence |
|---:|---|---|---|---|
| **0** | Button **Left** (side) → up / previous page | in | digital, active-LOW, ISR | HIGH |
| **1** | **Master peripheral / panel rail** | out | driven HIGH at boot | HIGH |
| **2** | Button **Right** (bottom key 2) | in | active-LOW, ISR | HIGH |
| **3** | Button **Power** | in | active-LOW, ISR | HIGH |
| **4** | **plain input, NOT interrupt-attached** | in | **role PENDING — not a button, not used by the SDK** | — |
| **5** | Button **Left** (bottom key 1) | in | active-LOW, ISR | HIGH |
| **6** | **SD power enable** | out | **ACTIVE-LOW**; pulse HIGH 80 ms → LOW 120 ms, hold LOW | HIGH |
| **7** | Button **Right** (side) → down / next page | in | active-LOW, ISR | HIGH |
| **8** | Button **Confirm** (bottom key 3) | in | active-LOW, ISR | HIGH |
| **9** | Button **Back** (bottom key 4) | in | active-LOW, ISR | HIGH |
| **10** | EPD **RST** | out | active-low reset pulse | HIGH |
| **11** | EPD **MOSI** | out | write-only, **no MISO** | HIGH |
| **12** | EPD **SCLK** | out | | HIGH |
| **13** | EPD **CS** | out | | HIGH |
| **14** | EPD **DC** | out | command = LOW, data = HIGH | HIGH |
| **18** | EPD **BUSY** | in | active-high | HIGH |
| **19 / 20** | USB **D− / D+** | i/o | native S3 USB-OTG, USB-MSC capable | HIGH |
| **21** | Charge **STAT** | in | active-HIGH — **polarity PENDING** | med |
| **38 / 39** | I²C **SCL / SDA** | — | 400 kHz | HIGH |
| **40 / 41 / 42** | SDMMC **DAT0 / CLK / CMD** | i/o | slot 1, 1-bit | HIGH |

`batteryAdc`, `usbDetect`, `display.powerEnable`: unassigned.

### The RE trail, pin by pin

- `FUN_4214d260(bus, 11, 12, 13, 14)` constructs the SPI display bus → **MOSI 11 /
  SCLK 12 / CS 13 / DC 14**, and stores GPIO14 as the derived bus's D/C pin.
- The boot path binds the remaining display tuple as `bus / GPIO10 / GPIO18`;
  `FUN_42148418` pulses `tuple[1]` **HIGH→LOW→HIGH as RESET** → **RST = 10**,
  leaving `tuple[2]` = **BUSY = 18**.
- `FUN_4214d4a8` pulses **GPIO6** HIGH for 80 ms, LOW for 120 ms, then runs SDMMC
  with the active-low gate held LOW → **SD power enable = 6**.
- The board init constructs the BM8563 RTC and CW2017 gauge on **I²C SDA 39 /
  SCL 38 @ 400 kHz**.

## Display bus — and the trap versus the X4 Pro

| Signal | **X4 Classic** | X4 Pro | Same? |
|---|---:|---:|---|
| SCLK | 12 | 12 | ✅ |
| MOSI | 11 | 11 | ✅ |
| CS | 13 | 13 | ✅ |
| **DC** | **14** | **18** | ❌ |
| **RST** | **10** | **14** | ❌ |
| **BUSY** | **18** | **6** | ❌ |

**Three of six display pins are permuted between two boards that share a chassis,
a panel and an SoC.** Porting display code across without changing them produces
a controller that resets and runs full-length waveforms but never develops an
image — the exact symptom that cost the X4 Pro bring-up months. Treat this table
as the single most important thing on this page.

`displaySpiHz` = **20 MHz** — chosen as the UC8279 serial-write maximum, to avoid
throttling full-plane anti-aliasing uploads. `GPIO1` supplies the panel rail.
No custom LUT, no drive voltages, no external PMIC.

**One command-stream difference from the X4 Pro:** the X4C **omits the UC8279 PLL
(`0x30`) command** that the X4 Pro programs.

## Panel-controller selection — NVS only

The X4C bus has **no MISO**, so the UC81xx `VER (0x70)` / `FLG (0x71)` probe used
on every other device in the family **cannot work** — the released line always
floats to `0xFF`. `applyXteinkDisplayController()` special-cases it:

```
NVS namespace hw_calib, key screenType (u8):
   1 or 0x0B → UC8179
   2 or 0x0C → UC8279
   3 / default / unset → SSD1677
```

> "X4 Classic has NO MISO line, so the display-bus probe can never read the
> controller ID (VER always floats to 0xFF). **NVS `hw_calib/screenType` is the
> ONLY source of truth here — the factory writes it once.**"
> — **[SDK]** `XteinkDetect.cpp`

**This is a live hazard.** The same SDK warns that `screenType` is unreliable in
the field *"a full-flash from another unit overwrites it, so it can name the wrong
panel"* — and on every other board a live bus probe overrides it. **On the X4C
there is no override.** Restoring an X4C from another unit's full-flash image can
silently leave it driving the wrong controller.

## Input — seven discrete interrupt-driven buttons

Physical layout = the X4 Pro's **two side keys** + the C3 X4's **four bottom keys**.

| Action | GPIO | Physical position |
|---|---:|---|
| Up / previous page | **0** | side, Left |
| Down / next page | **7** | side, Right |
| Left | **5** | bottom key 1 |
| Right | **2** | bottom key 2 |
| Confirm | **8** | bottom key 3 |
| Back | **9** | bottom key 4 |
| Power | **3** | — |

Stock array order is **2, 5, 8, 9** ("Bottom Key 1–4"). The SDK records that the
mapping was **corrected by hardware testing**: *"the old GPIO8/9 left/right
assignment made the physical Confirm/Back keys act as Up/Down."*

**Not an ADC ladder.** Every key is its own GPIO with its own interrupt — strictly
better than the C3 devices' two-pin resistor ladder: chords work, no polling, no
per-unit calibration. With all six navigation actions mapped, the UI renders
side-bezel button hints.

**Note the pin reuse:** GPIO2, 5, 8 and 9 are, on the X4 Pro, **touch power, SD
power, frontlight cool and frontlight warm** respectively. Firmware that
unconditionally configures those as outputs will fight four buttons here. Always
gate on `FREEINK_CAP_TOUCH` / `FREEINK_CAP_FRONTLIGHT`.

## I²C bus — SDA 39 / SCL 38 @ 400 kHz

| Address | Device | Component |
|---|---|---|
| **0x51** | BM8563 RTC (PCF8563-register-compatible) | [`generic/bm8563`](../../../components/generic/bm8563/README.md) |
| **0x63** | CW2017 fuel gauge — **needs an 80-byte BATINFO profile** | [`cellwise/cw2017`](../../../components/cellwise/cw2017/README.md) |
| **0x6B** | QMI8658 6-axis IMU, `WHO_AM_I` = `0x05`, **no interrupt line** | [`qst/qmi8658a`](../../../components/qst/qmi8658a/README.md) |

The IMU init (`CTRL1/2/3/7` at 0x6B) was RE-confirmed from the dump.

## Storage — native SDMMC

CLK **41**, CMD **42**, DAT0 **40**, slot 1, 1-bit. D1/D2/D3 unused.
Power enable **GPIO6, active-LOW**: driven HIGH 80 ms, then LOW, held LOW while
mounted. The block device performs that power cycle and **retries it on mount
failure** — same pattern as the X4 Pro, different pin.

## Resource conflicts

| Resource | Contenders | Note |
|---|---|---|
| I²C 39/38 | BM8563, CW2017, QMI8658 | One `Wire` controller; a stalled bus blocks all three |
| GPIO0 | Side-Left button **and** the S3 boot strap | Holding it at reset enters download mode |
| GPIO19/20 | native USB only | **Never probe.** The C3 fingerprint pokes SDA20/SCL0 — D+ and a strap here |
| GPIO2/5/8/9 | Buttons here; **rails and PWM on the X4 Pro** | The most likely cross-model porting bug |
| GPIO4 | **unknown** | Configured as an input, never read. Do not repurpose until its role is known |

## Bezel insets

`viewableInsets = {9, 7, 3, 7}` — **carried over from the X4 Pro on the grounds of
identical glass, and explicitly "pending measurement"**. Not independently
established for this device.

## What is still PENDING

- **The role of GPIO4** — an input, configured but not interrupt-attached and never
  read by the SDK.
- **Charge-STAT polarity** on GPIO21.
- **Panel mount orientation** (ships `NO_FLIP`).
- Whether the `R2` in the board revision string `ESP32S3_X4R2_CLA` implies an
  **R1 that shipped**.
