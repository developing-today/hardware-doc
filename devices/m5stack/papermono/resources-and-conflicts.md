# Resources and conflicts — M5Stack PaperMono

> Who owns which GPIO, bus, address, SPI host, partition and rail — and what happens when
> features run together.
> Hardware revision **V0.6.2** · snapshot **2026-09-01**.
> Limits are labelled **silicon** / **board** / **framework** / **observed**.
> **Nothing here was measured on hardware.**

## 1. The headline: there is no free GPIO and no expansion connector

**Every usable ESP32-S3 pin on this board is committed, and there is no header of any
kind — no Grove port, no M-Bus, no expansion connector.** That is unusual for an M5Stack
core and it is the constraint that shapes every design decision on this product.

| Disposition | Count | Pins |
|---|---:|---|
| E-paper (SPI2 + DC/CS/BUSY) | 5 | 14, 15, 16, 17, 18 |
| microSD (4-bit SDMMC) | 6 | 8, 9, 10, 11, 12, 13 |
| LoRa (SPI + BUSY + IRQ) | 6 | 5, 21, 38, 39, 40, 41 |
| **Reserved — in-package octal PSRAM** | 5 | **33, 34, 35, 36, 37** |
| Interrupts in (PM1, touch, NFC, IOE1) | 4 | 1, 4, 6, 7 |
| USB (native) | 2 | 19, 20 |
| UART0 | 2 | 43, 44 |
| System I²C | 2 | 47, 48 |
| PDM microphone | 2 | 45, 46 |
| User buttons | 2 | 2, 3 |
| Buzzer | 1 | 42 |
| Boot strap from the M5PM1 | 1 | 0 |
| Unconnected | 1 | 26 |
| Do not exist on the ESP32-S3 | — | 22–25, 27–32 |
| **Free** | **0** | **—** |

**Anything you add must go on the shared I²C bus, or take over one of the M5IOE1's
fourteen expander pins — all of which are also assigned.** There is no spare expander pin
either. See [`features/io-expander.md` §8](features/io-expander.md#8--m5unified-already-owns-most-of-these-pins).

## 2. The single I²C bus and its seven addresses

**GPIO47 SDA / GPIO48 SCL, pulled up by 2.2 kΩ (`R36`, `R37`) to `3V3_L2`.** One bus,
seven devices, no second bus anywhere on the board.

| Address | Device | Speed used | Owner | Notes |
|---|---|---|---|---|
| `0x32` | RX8130CE RTC | 400 kHz | `M5.Rtc` | `nIRQ` → **M5PM1 `G0`** |
| `0x38` | FT6336G touch | 400 kHz | M5GFX `Touch_FT5x06` on `I2C_NUM_1` | `INT` → GPIO4 |
| `0x4F` | M5IOE1 expander | **100 kHz** | M5Unified + your code | Address **contradicted by its own manual** (`0x6F`–`0x76`) |
| `0x50` | ST25R3916 NFC | 400 kHz | `M5Unit-NFC` | C153 only. Identity: reg `0x7F` == `0x05` |
| `0x68` | BMI270 IMU | **100 kHz** | `M5.Imu` | alt `0x69`, probed. `INT1` → **M5PM1 `G4`** |
| `0x6E` | M5PM1 power manager | **100 kHz** | `M5.Power` + your code | IRQ → GPIO1 |
| `0x75` | IP2315 charger | 100 kHz | `M5.Power`, **gated** | **Absent from a scan unless M5IOE1 `IO11` is asserted** |

All seven addresses were confirmed in **both** the vendor firmware source and the vendor
product page; none conflict.

### Bus arbitration rules that matter

1. **Speed is per-transaction.** The IMU, M5PM1 and M5IOE1 are driven at 100 kHz while the
   RTC, NFC and touch run at 400 kHz. Any master transaction sets the rate for that
   transaction only. The FT6336G tolerates 10 kHz–400 kHz, so it is safe throughout.
2. **The charger must be gated on, transacted with, and gated off.** Leaving it attached
   degrades bus stability — M5Stack's words — and a low battery can leave the IP2315
   failing to enter I²C mode and **disturbing the other six devices**. The IP2315
   datasheet documents a bus-lockup mechanism involving a missing NACK on the final read
   byte. M5Unified brackets every access with a 64-attempt readiness scan.
3. **Recovery from a wedged bus is a short press of the power button** (vendor-documented),
   which resets the device through the M5PM1.
4. **The M5PM1's first transaction after I²C idle-sleep fails by design.** Its own
   firmware uses that transaction to wake up. M5Stack's code calls
   `setI2cSleepTime(0)` twice for this reason.
5. **Losing this bus loses the display, touch, microSD, microphone, NFC, LoRa reset,
   battery telemetry and the ability to sleep.** It is a single point of failure with no
   redundancy.

## 3. SPI — two hosts, and a naming mismatch

| ESP-IDF host | Schematic net names | Device | Clock | Notes |
|---|---|---|---|---|
| **`SPI2_HOST`** | `G14_SPI2_MOSI`, `G15_SPI2_CLK` | E-paper SSD1677 | **40 MHz** in M5GFX, **20 MHz** in the OTP demo | 3-wire, **write-only** — no MISO. 22 Ω on SCLK (`R38`) |
| **`SPI3_HOST`** | `G38_SPI1_MOSI`, `G39_SPI1_CLK` | Stamp LoRa-1262 | **8 MHz** | ⚠ **schematic says "SPI1", firmware opens `SPI3_HOST`** |
| SPI0 (dedicated) | `NOR_*` | XM25UH128DHIQT flash | 80 MHz per the image header | Quad-capable; ships configured DIO |

**The two hosts are genuinely independent**, so e-paper refresh and LoRa traffic do not
contend for a bus. The `SPI1`/`SPI3_HOST` mismatch is a naming collision between M5Stack's
schematic labels and ESP-IDF's host numbering — made confusing by the fact that the
e-paper's `SPI2` label *does* coincide with `SPI2_HOST`.

**microSD is not on SPI at all** — it is the SDMMC peripheral in 4-bit mode.

> ⚠ **M5GFX drives the panel at 40 MHz.** The SSD1677 datasheet §12.1 **and** the DKE panel
> manual p. 16 independently state a **20 MHz** maximum write clock, and the vendor's own
> OTP demo uses 20 MHz. A 2× overclock of a rated bus limit, in the same library the
> vendor says has refresh problems. **Unresolved, untested, and the most likely single
> cause worth investigating first.**

## 4. SDMMC

| Item | Value |
|---|---|
| Peripheral | SDMMC host, `slot_config.width = 4` |
| Pins | CLK 13, CMD 12, D0 11, D1 10, D2 9, D3 8 |
| Frequency | **`SDMMC_HOST_DEFAULT()`** — the vendor does **not** override `max_freq_khz` |
| Mount | `/sdcard`, `max_files = 8`, `allocation_unit_size = 16 KiB`, `format_if_mount_failed = false` |
| Power | M5IOE1 `IO14` (`TF_EN`) — **left LOW by the factory HAL, driven HIGH by M5GFX** |
| Detect | M5IOE1 `IO1` (`TF_DET`), **low = inserted**, pulled up by the card's own power domain |

## 5. Memory, flash and partitions

| Resource | Size | Notes |
|---|---|---|
| Internal SRAM | 512 KB | Shared with the Wi-Fi/BLE stacks and the display driver |
| **PSRAM** | **8 MB octal, in package** | **Mandatory.** Consumes GPIO33–37. Without `CONFIG_SPIRAM_MODE_OCT`, M5GFX aborts display init |
| Flash | 16 MB external NOR | Quad-capable; **ships configured DIO** |

Partition table — **identical in both vendor projects**:

```
# Name,   Type, SubType, Offset,  Size,     Flags
nvs,      data, nvs,     0x9000,  0x6000,     (24 KiB)
phy_init, data, phy,     0xf000,  0x1000,     ( 4 KiB)
factory,  app,  factory, 0x10000, 0xF00000,   (15 MiB)
```

- **One `factory` app at `0xF00000`. No OTA slot. No SPIFFS, no FATFS-in-flash, no
  coredump partition.** The shipped firmware is **not field-updatable over the air**.
- ~960 KB of flash above the app is unallocated and unused.
- The third-party CrossPoint image repartitions entirely (6400 KB app, 4096 KB `cjkfont`,
  SPIFFS, coredump) — proof this is a firmware choice, not a hardware constraint.

## 6. Timers, PWM and DMA

| Resource | Total | Used by the board | Left |
|---|---:|---|---|
| **LEDC timers** | 4 | **`LEDC_TIMER_3`** — buzzer | 3 |
| **LEDC channels** | 8 low-speed | **`LEDC_CHANNEL_7`** — buzzer | 7 |
| I²S | 2 | **`I2S_NUM_0`** — PDM microphone RX | `I2S_NUM_1`, which **cannot do PDM RX** (silicon) |
| GDMA | 5 in / 5 out | E-paper SPI, SDMMC, I²S, Wi-Fi | Tight under a display + SD + Wi-Fi load. **Unmeasured** |
| **M5PM1 PWM** | 2 channels, **one shared frequency register** | PWM0 → frontlight, 5 kHz | PWM1 free, but forced to the same frequency |
| **M5IOE1 PWM** | 4 channels, **one shared frequency register** | PWM2 → LED green, PWM1 → LED blue, 5 kHz | PWM3 (`IO11`) and PWM4 (`IO10`) are used as digital lines |
| M5IOE1 ADC | 4 channels | none — `IO2`/`IO4`/`IO5`/`IO7` are all digital or `ADD_SET` | all four, if you repurpose a pin you cannot spare |
| RMT / PCNT / MCPWM / TWAI | full | 0 | Available in silicon, **pin-starved to the point of uselessness** |

**The buzzer's timer 3 / channel 7 allocation is deliberate** — top of the range, so
user code allocating from 0 upward does not collide. Keep the convention.

## 7. Interrupts

| Line | To | Used? |
|---|---|---|
| M5PM1 IRQ (`G1`) | ESP32-S3 **GPIO1** | ✅ M5Unified configures it; the wake path uses it |
| Touch `INT` | ESP32-S3 **GPIO4** | ✅ M5GFX; also the touch-wake EXT0 pin |
| NFC `IRQ` | ESP32-S3 **GPIO6** | ❌ **unused** — the vendor scan app sets `using_irq = false` |
| M5IOE1 `OD_INTOUT` | ESP32-S3 **GPIO7** | ❌ **unused** — the firmware polls (`M5IOE1_INT_MODE_DISABLED`) |
| LoRa `DIO1` | ESP32-S3 **GPIO5** | ✅ RadioLib, `GPIO_INTR_POSEDGE` |
| RTC `nIRQ` | **M5PM1 `G0`** | ✅ as a wake source |
| IMU `INT1` | **M5PM1 `G4`** | ✅ as a wake source, **falling edge / active-low** |

**Two of seven interrupt lines are wired and never used by any vendor code.** The GPIO7
expander interrupt in particular is unproven on this board, and `INT_OUT` is open-drain
and needs a pull-up.

**M5IOE1 interrupt exclusion pairs** — interrupts cannot be enabled simultaneously
within a pair: `IO1&IO6` · `IO2&IO3` · `IO7&IO12` · `IO8&IO9` · `IO10&IO14` ·
`IO11&IO13`. **Four of those six pairs straddle live PaperMono signals**: SD detect vs
touch reset, LoRa antenna switch vs e-paper rail, LoRa reset vs SD power, charger gate vs
touch power.

## 8. Power rails and their owners

| Rail | Source | Enable owner | Feeds | State |
|---|---|---|---|---|
| `VUSB_IN` | USB-C | — | input only | — |
| `VBUS_L0` | battery bus after protection | — | everything downstream | L0 |
| `3V3_L0` | `U4` SSP7615-33DFR, 400 mA | always on (`inferred`) | M5PM1, always-on logic | L0 |
| `3V3_L1` | `U6` SSP7615-33DFR, 400 mA | **M5PM1 `LDO3V3_EN_PP`** | **RTC, IMU** | L1 |
| `3V3_L2` | `U10` JW5712 DC-DC, 600 mA | **M5PM1 `DCDC3V3_EN_PP`** | ESP32-S3, I²C pull-ups, keys, NFC sub-board | L2 |
| `3V3_L2_LoRa` | `U9` SSP7615-33DFR, 400 mA | **M5PM1 `G2`** | Stamp LoRa-1262 | L2 |
| `EPD_3V3_L3B` | `U5` SSP7615-33DFR, 400 mA | **M5IOE1 `IO3`** | e-paper panel | L3 |
| `BL_15V_L3B` | `U11` AW9967 boost | **M5PM1 `G3`** (PWM) | frontlight | L3B |
| `TF_3V3_L3B` | `U8` AW35122 switch | **M5IOE1 `IO14`** | microSD | L3B |
| `TP_VDD` | `U18` AW35122 switch | **M5IOE1 `IO13`** | touch controller | L3B |
| `PDM_VDD` | `U21` AW35122 switch | **M5IOE1 `IO12`** | microphone | L3B |
| `VDD_NOR` | from `3V3_L2` | — | SPI NOR flash | L2 |

**Every switched LDO carries a 1 MΩ pulldown on its enable** (`R24`, `R26`, `R23`), so
every optional rail defaults **off** on cold power-up. A blank screen is the expected
result of forgetting to bring up `EPD_3V3_L3B`.

**Ownership summary:** the M5PM1 owns L0/L1/L2 and the frontlight; the M5IOE1 owns every
L3B switch except the frontlight. **The ESP32-S3 owns none of its own power.**

Current budget: the largest regulator is the 600 mA `3V3_L2` DC-DC feeding the SoC.
**No current figure exists for any consumer**, so no meaningful budget can be drawn up.
That is a gap, not an omission.

## 9. Boot straps

| GPIO | Strap function | Also carries | Risk |
|---|---|---|---|
| **GPIO0** | boot mode | **M5PM1 `BOOT_OUT_OD`** | By design — the power manager, not a button, selects download mode |
| **GPIO3** | strapping | **User button B** | Holding B across reset perturbs the strap |
| **GPIO45** | `VDD_SPI` select | **PDM mic clock** | Driven by the ESP32-S3 itself |
| **GPIO46** | boot-message routing | **PDM mic data** | Driven by the microphone; state depends on whether `PDM_VDD` is up |

`CHIP_PU` carries `SOC_RESET` from the M5PM1. **The application processor cannot reset
itself independently of the power manager.** No vendor firmware guards the GPIO3/45/46
strap exposure; `inferred`, `not-tested`.

## 10. Realistic simultaneous-use scenarios

Features are evaluated in combination, not in isolation. **None of these has been run.**

| Combination | Verdict | Mechanism and what would actually bite |
|---|---|---|
| **E-paper refresh + microSD + Wi-Fi, concurrently** | ⚠ **untested, and the case most worth testing** | **No pin conflict at all** — GPIO14–18, GPIO8–13 and an internal radio. The pressure is elsewhere: (a) **GDMA** — a full refresh is up to ~4.7 s of SPI DMA, SDMMC is a second client, Wi-Fi a third; (b) **PSRAM bandwidth** — the display framebuffers live in octal PSRAM and Wi-Fi buffers compete for internal SRAM; (c) **the `3V3_L2` 600 mA rail and the battery** carry a Wi-Fi TX burst on top of an SD write burst with no published figure for either. Also note the whole L3B group comes up together, so you cannot power-manage the card independently of the panel without expander writes. **Nobody has demonstrated this.** |
| **LoRa + Wi-Fi** | ✅ **they do not share a radio — say it plainly** | LoRa is **sub-GHz, 868–923 MHz**, on a physically separate SX1262 module with its own FPC antenna, reached over `SPI3_HOST`. Wi-Fi and BLE are **2.4 GHz** inside the ESP32-S3 die. Different bands, different antennas, different peripherals, **no coexistence scheduling required**. What they share is CPU time and the battery. (Wi-Fi and **BLE** *do* share one 2.4 GHz radio and are time-sliced — that is the pair that needs coexistence care, not LoRa.) |
| **NFC + charger, both on the shared I²C bus** | ⚠ **the genuinely risky pair** | Both are on the **one** bus. NFC polling is sustained and chatty — the vendor app runs 180 ms detect calls with 60 ms gaps across 3500 ms windows for type A — and gating the IP2315 onto the bus is **the one documented bus-stability hazard on this board**, worse still at low battery. **Do not open the charger gate inside an NFC scan window.** Batch charger reads between scans and close the gate immediately. If the bus wedges, the documented recovery is a short press of the power button, i.e. a reset |
| **Microphone on GPIO45/46, which are strapping pins** | ⚠ **board-level hazard, unguarded** | GPIO45 selects `VDD_SPI` voltage and GPIO46 routes boot messages. The mic's output stage sits on GPIO46 and its state at reset depends on whether `PDM_VDD` is up — which is an expander-controlled rail that firmware may or may not have left asserted. The factory firmware calls `gpio_reset_pin()` on both and floats GPIO46 before reconfiguring, which is the right defensive move, but **nothing guards the reset path itself**. `inferred`, `not-tested` |
| Display + touch | ✅ intended | M5GFX resets both together on `IO5`/`IO6` |
| Display + LoRa | ✅ | Separate SPI hosts |
| Display + frontlight | ✅ | Different chips — and the `PYG3` ambiguity is the only real hazard |
| Sleep + microSD mounted | ⚠ **unmount first** | The card rail is L3B; dropping it under an open file is a corruption path |
| Sleep + RTC or IMU wake | ✅ down to **L1** | The intended low-power pattern; requires `ldoSetPowerHold(true)` |
| Sleep + touch wake | ✅ only in **L2** | Touch does not reach the M5PM1 |
| Touch wake + M5PM1 IRQ wake, one call | ❌ | `M5.Power.deepSleep(us, touch_wakeup=true)` **substitutes** GPIO4 for GPIO1 |
| Any two M5IOE1 interrupts from one exclusion pair | ❌ | §7 |
| Two PWM consumers wanting different frequencies on one expander | ❌ | One shared `PWM_FREQ` register per chip |
| Buzzer + user LEDC allocation from channel 0 | ✅ | Buzzer sits at timer 3 / channel 7 |
| Microphone + I²S playback | ❌ (moot) | PDM RX is `I2S_NUM_0`-only — **silicon**. There is no audio output on this board anyway |

## 11. The three constraints that actually bite

**1. There is no free GPIO and no expansion connector.** Not "few" — none, and no header
to expose one on. Every extension has to be I²C, and the I²C bus already has seven devices
and one documented stability hazard on it.

**2. Two auxiliary microcontrollers own the board, and one naming collision can kill the
display.** `PYG3` denotes the M5PM1's frontlight PWM *net* and the M5IOE1's e-paper-rail
*pin*. Both are live. Writing the wrong one cuts panel power and reports nothing. Compounded
by `M5IOE1_PIN_3 = 2`. See
[`pin-naming-and-the-pyg-ambiguity.md`](pin-naming-and-the-pyg-ambiguity.md).

**3. Octal PSRAM is mandatory and its absence looks like dead hardware.** M5GFX identifies
the board, then silently declines to bring up the panel, logging one line that the
vendor's own `CORE_DEBUG_LEVEL=0` compiles out.

## Related

- [`pinouts-and-buses.md`](pinouts-and-buses.md) — the underlying pin map and connector table
- [`power-architecture.md`](power-architecture.md) — rails, states and wake sources in full
- [`coverage.md`](coverage.md) · [`compatibility-and-status.md`](compatibility-and-status.md) · [`features/README.md`](features/README.md) · [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
