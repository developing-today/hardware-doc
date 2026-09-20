# Cardputer ADV — resources, contention and realistic combinations

> Snapshot **2026-09-04**. The interesting part of this board is not any single peripheral —
> it is that the keyboard, display, SD card, audio and CAP header all want pieces of the same
> small pin budget, and the ADV's whole design is a re-allocation of that budget.

## 1. GPIO budget

The Stamp-S3 footprint exposes **26 usable GPIOs** (G0–G15, G21, G33–G46 minus the ones not
brought out). Here is where they go.

| Consumer | v1.0 / v1.1 | ADV | Δ |
|---|---|---|---|
| Keyboard | **15** (G3,G4,G5,G6,G7,G8,G9,G11,G13,G15 + …) — precisely: 8 drive (`Y0..Y7` via 74HC138 from G8/G9/G11) + 7 sense (G13,G15,G3,G4,G5,G6,G7) = **10 GPIOs** | **3** (G8, G9, G11) | **−7** |
| Display | 6 (G33–G38) | 6 | 0 |
| microSD | 4 (G12,G14,G39,G40) | 4 | 0 |
| Audio | 4 (G41,G42,G43,G46) | 4 | 0 |
| IR | 1 (G44) | 1 | 0 |
| RGB LED | 1 (G21) | 1 | 0 |
| Battery ADC | 1 (G10) | 1 | 0 |
| Grove | 2 (G1,G2) | 2 | 0 |
| Boot | 1 (G0) | 1 | 0 |
| **Free / expansion** | **0** (Grove only) | **7** on the CAP header (G3,G4,G5,G6,G13,G15 + the shared G8/G9) | **+7** |

That single row — *free GPIOs: 0 → 7* — is the ADV.

## 2. Buses

| Bus | Members | Arbitration |
|---|---|---|
| `SPI3_HOST` (display) | ST7789V2 only | none needed |
| **SPI peripheral** G40/G14/G39 | microSD (CS **G12**) · CAP board (CS **G5**) | **yours to write** |
| **I²C internal** G8/G9 | TCA8418 `0x34` · ES8311 `0x18` · BMI270 `0x69` · CAP board's devices | address-based; latency is the real cost |
| I²C external G1/G2 | nothing on board | free |
| `I2S_NUM_1` | ES8311, both directions | one codec, one port |
| `I2S_NUM_0` | **free** | |
| RMT | WS2812 (G21) · IR TX (G44) | one channel each |
| LEDC | channel **7** = backlight | 7 channels free |
| ADC1 | battery (G10) | |
| GPIO ISR | TCA8418 `INT` (G11) · CAP `INT` (G4) · CAP `BUSY` (G6) · G0 | ESP32-S3 has plenty |

## 3. The two contended resources, in detail

### 3.1 SPI peripheral bus — microSD versus CAP

Same `SCK`/`MOSI`/`MISO`, different `CS`. Neither the vendor library nor any third-party
firmware installs a mutex for you.

| Failure mode | Cause | Mitigation |
|---|---|---|
| Radio stops responding after an SD write | both CS asserted, or bus reconfigured mid-transaction | one `SPIClass`, one owner, explicit CS handling |
| Corrupt SD reads once a radio is added | clock raised above the transceiver's tolerance, or vice versa | run at the slower device's limit — 16 MHz for an SX1262 |
| Missed LoRa receive windows | a 512 B block transfer holds the bus while a window opens | short SD transactions; buffer in RAM; do not log inside a receive window |
| Meshtastic + SD logging flakiness | as above | reported pattern; not reproduced by this session |

M5Stack's own factory firmware runs both (`HAL_PIN_SD_CARD_CS 12` and `HAL_PIN_LORA_NSS_GPIO 5`
in the same `hal_config.h`), and Meshtastic's ADV variant does too — so the combination is
**reported-working**, with the timing caveat.

### 3.2 Internal I²C — keyboard versus everything

The keyboard scanner is a *latency-sensitive* device on a bus shared with a codec that gets
long configuration bursts and an IMU that people poll fast.

| Combination | Effect |
|---|---|
| Keyboard + codec enable burst | the codec sequences are 8 register writes; sub-millisecond; TCA8418 has a 10-deep FIFO so events queue, not drop |
| Keyboard + high-rate IMU polling | competes directly; **not characterised**. If keys feel laggy under IMU load, this is why. |
| Keyboard + CAP I²C device | depends entirely on the device; a chatty expander on the CAP header will hurt |
| Bruce's 100 ms polling keyboard | already visibly less responsive than the interrupt path, before any contention |

**Design guidance:** put anything slow, chatty or non-critical on the **Grove** port. The
internal bus should carry things that *must* be there.

## 4. Memory — the real ceiling

512 KB SRAM, **no PSRAM**, 8 MB flash. This is not a contention problem, it is a hard wall, and
it shapes what the community builds.

| Consumer | Typical cost |
|---|---|
| 240 × 135 × 16 bpp framebuffer | 64 800 B (12.7 % of SRAM) |
| Double buffering | 129 600 B (25 %) |
| Wi-Fi + LWIP | ~50–80 KB |
| TLS session | tens of KB |
| Audio decode buffers | tens to hundreds of KB |
| BLE (NimBLE) | smaller than Bluedroid, which is why the factory firmware uses it |

Observed community workarounds:

* **Memory-mapped flash partitions instead of RAM.** The Plai/Meshtastic-client author put a
  2.16 MB GNU Unifont table in its own partition with fixed-size records so lookup is
  arithmetic, and mapped it — *"rendering Cyrillic, CJK or Greek costs no heap at all"*
  (r/CardPuter, 2026-08-01).
* Meshtastic's ADV variant compiles with **`-DOLEDDISPLAY_REDUCE_MEMORY`**.
* Bruce ships an `[env_light]` profile and a `-DLITE_VERSION=1` flag "to save space for
  M5Launcher Compatibility".
* `engneer-hamachan/area512` is literally named for the constraint: *"A self-contained Ruby &
  Python development environment for the 512 KB M5Stack Cardputer"*.

## 5. Flash partitioning

| Firmware | Layout |
|---|---|
| **M5Stack factory (`CardputerADV` branch)** | `nvs 0x9000/0x4000`, `otadata 0xd000/0x2000`, `phy_init 0xf000/0x1000`, **`factory app 0x10000 / 4 MB`** — single app, **no OTA slots**, ~3.9 MB unallocated |
| Bruce | `board_build.partitions = custom_8Mb.csv` |
| Meshtastic ADV | `board_build.partitions = default_8MB.csv` |
| `CCP101/cardputer-recoverable-multiboot` | a community scheme putting M5Launcher in `factory` and applications in OTA slots — the practical answer to "how do I keep a recovery path" |

The factory layout leaving half the flash unallocated is worth noting: there is room for a
large data partition (which is exactly what the Unicode-font trick uses).

## 6. Realistic combinations, assessed

| Combination | Status | Evidence |
|---|---|---|
| Display + keyboard + SD | **works** | every firmware |
| Display + keyboard + audio out | **works** | WebRadio, MP3 players, DAW projects |
| Audio in **then** audio out without re-enable | **fails** | driver defect, [`features/audio.md`](features/audio.md) §6.2 |
| Display + keyboard + Wi-Fi + audio streaming | **works, RAM-tight** | WebRadio ports |
| Display + keyboard + CAP LoRa + GNSS | **works** | factory firmware, Meshtastic, Plai |
| CAP LoRa + SD logging | **works with timing caveats** | §3.1 |
| Backlight PWM + RGB LED | **fails** | shared `BL_3V3` rail; vendor documents it for v1.1 |
| IMU motion-wake from deep sleep | **not possible** | no IMU interrupt line traced |
| Wall-clock time across power cycle | **not possible** | no RTC |
| Wi-Fi + BLE simultaneously | **works** (time-shared) | ESP32-S3 standard; RAM is the limit |
| Second display on CAP + built-in display | **works** | `Prokuon/CardputerADV_Cap_TFT-2.8`, `guicmg/cardputer_adv_external_screen` |

## 7. Ownership and arbitration summary

There is **one CPU and no coprocessor**. Nothing on this board arbitrates anything for you:
no bus mux, no I/O expander on the mainboard, no PMIC with a state machine. Every conflict in
this document is resolved in your firmware or not at all.

The only piece of hardware that makes a decision on its own is the **headphone-detect network**
(`HP_DET` → Q4 → `AMP_EN`), which mutes the speaker amplifier when a plug is inserted — and
software cannot see or override it.
