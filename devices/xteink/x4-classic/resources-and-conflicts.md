# Resources and conflicts — Xteink X4 Classic

Snapshot **2026-09-11**. Pin data from the FreeInk profile
`BoardConfig::XTEINK_X4_CLASSIC` at commit
[`9f4d3f9`](https://github.com/Free-Ink/freeink-sdk/blob/9f4d3f9ca675e64cc9d616081f39a33cdefce57e/libs/hardware/BoardConfig/include/BoardConfig.h)
and `docs/xteink-x4c-support.md`, **corroborated independently** by
[`clackups/draftling`'s `xteink_x4_classic.h`](https://github.com/clackups/draftling/blob/92ba7e514f66bbe42a7fea6d38eff45eed82617b/firmware/main/boards/xteink_x4_classic.h),
a hand-written board header for a different firmware project.

**Both sources derive from the same OEM reverse engineering**, so they are not
fully independent — Draftling's header names FreeInk as its origin and states
plainly *"This board has NOT been tested on physical hardware."* They are counted
here as **one custodian with a second reading**, not two custodians. The full
tables live in [`pinouts-and-buses.md`](pinouts-and-buses.md); this file is about
ownership, arbitration and what cannot run at the same time.

## 1. GPIO ownership

| GPIO | Owner | Direction | Contention |
|---|---|---|---|
| 0 | **Left / page-up key** | in, pull-up, ISR | **Also the ESP32-S3 boot strap.** Held at reset → download mode. A user pressing Left during a power-on reset will not boot the app |
| 1 | **Master peripheral rail latch** | out, driven HIGH at boot | **Everything** — panel, SD and the I²C devices are unpowered until this is high. Nothing else may touch it |
| 2 | **Bottom-right key** | in, pull-up, ISR | On the X4 Pro this pin is the **GT911 touch power enable**. Porting Pro code here drives a button pin as an output |
| 3 | **Power key** | in, pull-up, ISR | **The only EXT1 deep-sleep wake source.** Also the pin a wake handler must re-sample |
| 4 | **unassigned discrete input** | in | Role unknown. Neither FreeInk nor Draftling uses it. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md) |
| 5 | **Bottom-left key** | in, pull-up, ISR | On the X4 Pro this is the **SD power gate**. Same porting hazard as GPIO2, in the opposite direction |
| 6 | **SD power enable**, active-LOW | out | On the X4 Pro this is the panel **BUSY** input. **Three different meanings for GPIO6 across the family** |
| 7 | **Right / page-down key** | in, pull-up, ISR | — |
| 8 | **Confirm key** | in, pull-up, ISR | On the X4 Pro this is the **cool frontlight LEDC channel** |
| 9 | **Back key** | in, pull-up, ISR | On the X4 Pro this is the **warm frontlight LEDC channel** |
| 10 | **Panel RST** | out | On the X4 Pro GPIO10 is the **GT911 INT / address-select** pin |
| 11 | Panel MOSI (SPI2) | out | Write-only; **no MISO on this board** |
| 12 | Panel SCLK (SPI2) | out | — |
| 13 | Panel CS | out | — |
| 14 | Panel DC | out | On the X4 Pro GPIO14 is **RST** |
| 18 | Panel BUSY | in | On the X4 Pro GPIO18 is **DC** |
| 19 / 20 | Native USB D− / D+ | — | USB-OTG / USB-MSC capable. **There is no USB socket on the enclosure** — the port is pads, not a connector |
| 21 | Charger `STAT` | in, active-HIGH | Polarity is `inferred` from the profile field, not observed |
| 38 / 39 | I²C SCL / SDA @ 400 kHz | — | Shared by three devices, see §2 |
| 40 / 41 / 42 | SDMMC DAT0 / CLK / CMD, slot 1, 1-bit | — | Native peripheral, not bit-banged |

### The three-way GPIO trap, stated once

**GPIO2, GPIO5, GPIO6, GPIO8, GPIO9, GPIO10, GPIO14 and GPIO18 all mean
something different on the X4 Classic than on the X4 Pro**, even though the two
boards share a SoC, a panel, a flash size and most of a firmware. Five of them
change from *output* to *input* or the reverse.

Porting an X4 Pro driver to the X4 Classic without re-reading the profile will
drive four button pins as outputs (2, 5, 8, 9) and read two output pins as
inputs. **Never port power or display code between these two boards by pin
number.** This is the X4 Classic's version of the family-wide GPIO13 hazard
already recorded in the [family index](../README.md).

## 2. I²C bus — SDA 39 / SCL 38 @ 400 kHz

| Address | Device | Owner | Notes |
|---|---|---|---|
| `0x51` | **BM8563 RTC** | timekeeping | PCF8563-register-compatible → [`generic/bm8563`](../../../components/generic/bm8563/README.md) |
| `0x63` | **CW2017 fuel gauge** | battery | Reports 0 % until an 80-byte BATINFO profile is written to `0x10..0x5F` → [`cellwise/cw2017`](../../../components/cellwise/cw2017/README.md) |
| `0x6B` | **QMI8658 IMU** | Shake-to-Flip | `WHO_AM_I = 0x05`, **no interrupt line** → [`qst/qmi8658a`](../../../components/qst/qmi8658a/README.md) |

**No address collisions.** All three are on one master; there is no second bus
and no mux. The IMU has no INT pin, so **Shake-to-Flip must be polled**, which is
a real power cost on a device that otherwise spends its life in deep sleep. No
measurement of that cost exists.

The X4 Pro carries the same RTC and gauge at the same addresses **plus** a GT911
at `0x5D`; the X4 Classic's `0x5D` is empty because the touch controller is not
fitted and GPIO2 — its power enable on the Pro — is a button here.

## 3. SPI2 (FSPI)

Single master, single slave: the panel. **No MISO.** Consequences:

- The boot-time bus probe used on every other Xteink board (write `0x70`/`0x71`,
  read the reply on a re-purposed MOSI) **cannot run**. The SDK instead reads NVS
  `hw_calib/screenType` — `1` = UC8179, `2` = UC8279, `3`/absent = SSD1677.
- **A wiped or re-initialised NVS silently selects the wrong panel driver** and
  there is no way for firmware to detect the mistake. This is the single most
  consequential difference between the X4 Classic and every sibling, and it is
  why `nvs` must be preserved across a reflash. See
  [`development.md`](development.md) and
  [`../firmware-ecosystem.md`](../firmware-ecosystem.md).

## 4. Flash and partitions (16 MB, dual-OTA)

| Partition | Offset | Size |
|---|---|---|
| `nvs` | `0x009000` | 20 KB |
| `otadata` | `0x00E000` | 8 KB |
| `app0` | `0x010000` | 8,060 KB |
| `app1` | `0x7F0000` | 8,060 KB |
| `spiffs` | `0xFD0000` | 80 KB |
| `coredump` | `0xFE4000` | 112 KB |

The layout is identical to the X4 Pro's, as read from a **physical X4 Pro** by
[`kycube/x4pro-emu`](https://github.com/kycube/x4pro-emu/blob/bf4b86ae0471012d4d07c0bb3042f3f561c9c302/docs/device/partitions.md)
on 2026-09-06 — the first time this table has had a non-SDK witness anywhere in
this family. **It has not been read off an X4 Classic.**

**`nvs` at `0x009000` holds the panel identity.** Any flashing procedure that
erases the whole chip destroys it. Draftling's X4C partition table keeps an
`otadata` partition specifically so the stock and CrossPoint OTA updaters can
reinstall themselves afterwards.

## 5. Realistic concurrent-use scenarios

| Scenario | Verdict | Why |
|---|---|---|
| Panel refresh **+** SD read | **OK** | Different peripherals: SPI2 vs the SDMMC block. The X4's shared-SPI hazard does **not** apply here |
| Panel refresh **+** I²C poll | **OK** | Independent buses |
| SD mounted **+** deep sleep | **needs care** | GPIO6 is held LOW while mounted; the sleep path must release or hold it deliberately |
| Wi-Fi **+** panel refresh | **untested** | Both are current spikes on one cell with no PMIC. Nobody has measured the brown-out margin |
| USB-MSC **+** anything | **untested, and physically awkward** | The SDK enables MSC, but the enclosure has no USB socket |
| Shake-to-Flip **+** deep sleep | **contradictory by construction** | The QMI8658 has no interrupt line wired, so motion cannot wake the device. Shake-to-Flip can only work while awake |
| Button ISR **+** boot | **hazard** | GPIO0 is both the Left key and the boot strap |

## 6. Power rails

There is **no PMIC and no software power-off latch**. GPIO1 gates the peripheral
rail; the SoC itself cannot be cut from software. "Off" is `esp_deep_sleep_start()`
with `EXT1` armed on GPIO3, and the pin states of GPIO1/GPIO6/GPIO10 held through
sleep with `gpio_hold_en`. Draftling's header says this explicitly:
*"there is no hardware latch that can fully power this board off from software."*

Charging is **pogo-pin only**, four contacts, magnetic. `STAT` on GPIO21. No
charger IC is on the I²C bus, so **charge state is only ever a single GPIO
level** — there is no current, voltage or fault reporting from the charger.
