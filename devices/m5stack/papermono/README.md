# M5Stack PaperMono

> **SKU C153** · schematic revision **V0.6.2** (file dated 2026-05-22) ·
> announced and on sale **2026-08-21** · documentation published 2026-08-20 ·
> current at research snapshot **2026-09-01**, at which point the product was
> **out of stock at the official store**.
> Sibling variant: [PaperMono-Lite](../papermono-lite/README.md) (SKU C153-LITE).

An ESP32-S3 development board built around a 3.97-inch touch e-paper panel with
an integrated frontlight, a five-state hardware power manager, NFC and LoRa. It
is best understood as a battery-first low-power platform that happens to have a
display, rather than an e-paper display board that happens to have a battery.

## Contents

| Document | What is in it |
|---|---|
| [**`features/`**](features/README.md) | **Task-oriented guides — one per fitted capability. Start here to build something** |
| [`pinouts-and-buses.md`](pinouts-and-buses.md) | Complete ESP32-S3 pin map, I²C/SPI buses, expander pins, connectors, boot behaviour |
| [`power-architecture.md`](power-architecture.md) | The five power states, every rail and its enable, charging, frontlight, wake sources |
| [`pin-naming-and-the-pyg-ambiguity.md`](pin-naming-and-the-pyg-ambiguity.md) | Why `PYG3` means two different pins, and how to avoid the resulting hazard |
| [`development.md`](development.md) | Frameworks and exact versions, board target, the verbatim PlatformIO block, libraries, build/flash/monitor, port selection, restore offsets — and the **bricking and bootstrapping risks** |
| [`factory-firmware.md`](factory-firmware.md) | Both shipped images parsed: headers, partition maps, build metadata, notable strings, what the device does on power-up, and why the official image is **not reproducible** |
| [`resources-and-conflicts.md`](resources-and-conflicts.md) | Every GPIO, bus, address, SPI host, partition and rail — and what breaks when features run together |
| [`coverage.md`](coverage.md) | Every capability mapped to hardware, docs, examples and test status |
| [`compatibility-and-status.md`](compatibility-and-status.md) | Working / partial / failing / untested, keyed by hardware and library version |
| [`performance.md`](performance.md) | The vendor's four refresh timings, the panel's optical and electrical figures, ESP32-S3 silicon claims — and the **inventory of everything nobody has measured** |
| [`product-history-and-family.md`](product-history-and-family.md) | The dated timeline with its evidence row by row, the M5Paper lineage, and why **PaperMono is not a successor to the PaperS3** |
| [`market-and-pricing.md`](market-and-pricing.md) | Launch and current pricing kept separate, every observation dated with seller, tax, stock and source; the confirmed-not-sold and no-determination lists |
| [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) | Competitors and substitutes by workload and price tier, launch-era vs current fit, use / do-not-use guidance, alternatives by tier |
| [`community.md`](community.md) | Every coverage item by medium and **evidence type**; the claims that failed checking, and the ones that survived |
| [`media.md`](media.md) · [`media/manifest.json`](media/manifest.json) | Visual identification: what was sought, why **no imagery is retained**, and exactly what a future pass should capture |
| [**`examples/`**](examples/best.md) | The 43-project population with **every repository pinned to a commit**, the selected portfolio, and the search log |
| [`projects-and-community.md`](projects-and-community.md) | Third-party firmware and software targeting this board, classified by whether it was actually demonstrated on hardware |
| [`bill-of-materials.md`](bill-of-materials.md) | The full designator census from the schematic — 290 placed components, 230 designators, and what the gaps mean |
| [`gaps-and-conflicts.md`](gaps-and-conflicts.md) | Every recorded contradiction and open question |
| [`sources.md`](sources.md) | Source table with classes, retrieval dates and versions |
| [`research-log.md`](research-log.md) | Every service, query, filter and disposition; retrieval findings; the stopping criterion |
| [`commands.md`](commands.md) | Command ledger — every command with its tool version and execution status |

Vendor documentation-sourcing guides produced by this pass:
[`vendors/m5stack`](../../../vendors/m5stack/README.md) ·
[`vendors/dke`](../../../vendors/dke/README.md).

## Identity and variants

| Field | Value | Evidence |
|---|---|---|
| Marketed name | PaperMono | vendor product page |
| SKU | C153 | vendor product page, store listing |
| Manufacturer | M5Stack Technology Co., Ltd (Shenzhen) | vendor site |
| Schematic revision | V0.6.2, dated 2026-05-22 | schematic filename and title blocks |
| Sub-board revisions | KEY/RGB sheet dated 2026-04-14; NFC sheet rev V0.2 dated 2026-07-28 | schematic title blocks |
| Case colour | Grey | vendor comparison table |
| Variant | PaperMono-Lite, SKU C153-LITE, white case, no NFC, no LoRa | vendor comparison table |

There is exactly one hardware revision in evidence. No regional variants were
found, and no FCC/CE/TELEC identifier appears anywhere on M5Stack's site —
`/en/certification` returns zero matches for both `PaperMono` and `C153`. That
is a verified negative, not a failed search.

**Do not read PaperMono as a successor to the M5PaperS3.** See
[product history](#product-history-family-and-culture).

## What it is and visual identification

A closed handheld slab, 62.0 × 101.0 × 8.0 mm, 74.7 g, with the e-paper panel
occupying most of the front face, a USB-C port, two user buttons plus a power
button, and a side RGB indicator. There is **no expansion connector** — no
Grove port, no M-Bus — which is unusual for an M5Stack core and materially
limits what can be added to it.

Internally it is **three PCBs plus three flexible assemblies**: a main board, a
KEY/RGB/microphone sub-board, an NFC sub-board, and FPC connections to the
e-paper panel, the touch layer and the frontlight, with the LoRa radio on a
plug-in `Stamp-LoRa-1262-mini` module. See
[`pinouts-and-buses.md`](pinouts-and-buses.md#board-set--this-is-not-one-pcb).

> **Images: an explicit gap.** No product, teardown or PCB photograph has been
> retained in this record. The vendor's product imagery is not licensed for
> redistribution and no independent teardown existed at the snapshot date. The
> only visual hardware evidence held here is the vendor schematic and the
> mechanical drawing. Recorded rather than filled with unattributed images.

## Product history, family and culture

| Date | Event | Evidence |
|---|---|---|
| 2026-04-14 | KEY/RGB sub-board schematic dated | schematic title block |
| 2026-05-22 | Main schematic V0.6.2 dated | schematic filename |
| 2026-06-08 | Schematic PDF created | PDF metadata |
| 2026-07-28 | NFC sub-board schematic V0.2 dated; schematic PDF last modified | title block, PDF metadata |
| 2026-08-06 | Factory firmware image built | `esp_app_desc_t` in the shipped binary |
| 2026-08-10 | UserDemo repository HEAD commit | `c1099107…` |
| 2026-08-18 | Store record created | Shopify metadata |
| 2026-08-20 | Documentation published under "Controllers" | vendor release history |
| 2026-08-21 | Store published; vendor blog announcement; first independent sell-out report nine minutes later | store metadata, community |
| 2026-08-29 | First hands-on video published | community |

The M5Paper line: **M5Paper** (ESP32, 4.7" IT8951), **M5PaperS3** (ESP32-S3,
4.7", 16 grey levels, 1800 mAh, expansion port — now end-of-life), then
**PaperMono** and **PaperMono-Lite**. Relative to the PaperS3 the PaperMono has
**about 35 % fewer pixels, 4 grey levels instead of 16, a smaller battery and no
expansion port**, while adding a frontlight, NFC, LoRa and the M5PM1 power
system. It is a repositioning, not an upgrade, and describing it as a successor —
as several launch articles did — is not supported by the vendor's own
specifications.

## Key specifications

| Specification | Value | Component record |
|---|---|---|
| SoC | ESP32-S3R8, Xtensa LX7 dual-core @ 240 MHz, bare die in 56-pin QFN | [esp32-s3r8](../../../components/espressif/esp32-s3r8/README.md) |
| Flash | 16 MB external SPI NOR (`XM25UH128DHIQT`), quad-capable | [xm25uh128dhiqt](../../../components/xmc/xm25uh128dhiqt/README.md) |
| PSRAM | 8 MB octal, in package — **mandatory in the build config** | [esp32-s3r8](../../../components/espressif/esp32-s3r8/README.md) |
| Wireless | 2.4 GHz Wi-Fi + Bluetooth LE (ESP32-S3 radio) | — |
| Display | 3.97" e-paper, 480 × 800, 235 DPI, 4-level greyscale, DKE `DEPG0397BBS770F3` | [depg0397bbs770f3](../../../components/dke/depg0397bbs770f3/README.md) |
| Display controller | Solomon Systech SSD1677, 4-wire SPI | [ssd1677](../../../components/solomon-systech/ssd1677/README.md) |
| Frontlight | AW9967 boost, 15 V rail, PWM dimmed from the M5PM1 | [aw9967](../../../components/awinic/aw9967/README.md) |
| Touch | FocalTech FT6336G, I²C `0x38` | [ft6336g](../../../components/focaltech/ft6336g/README.md) |
| Power management | M5PM1, I²C `0x6E` — a `PY32L020F15U6` running M5Stack firmware | [m5pm1](../../../components/m5stack/m5pm1/README.md) |
| I/O expander | M5IOE1, I²C `0x4F` — same silicon | [m5ioe1](../../../components/m5stack/m5ioe1/README.md) |
| IMU | Bosch BMI270, I²C `0x68` | [bmi270](../../../components/bosch-sensortec/bmi270/README.md) |
| RTC | Seiko Epson RX8130CE, I²C `0x32` | [rx8130ce](../../../components/seiko-epson/rx8130ce/README.md) |
| NFC | ST ST25R3916, I²C `0x50` — ISO14443A/B, FeliCa, ISO15693 | [st25r3916](../../../components/stmicroelectronics/st25r3916/README.md) |
| LoRa | `Stamp LoRa-1262` module (Semtech SX1262), 868–923 MHz, FPC antenna | [stamp-lora-1262](../../../components/m5stack/stamp-lora-1262/README.md) |
| Charger | Injoinic IP2315, I²C `0x75` — **gated off the bus by default** | [ip2315](../../../components/injoinic/ip2315/README.md) |
| Storage | microSD, 4-bit SDMMC on GPIO8–13 | — |
| Audio | PDM microphone `LMD4737T261-AC02`; buzzer on GPIO42 | [mic](../../../components/generic/lmd4737t261-ac02-pdm-microphone/README.md) |
| Battery | 1150 mAh Li-ion; 2-wire connector. Thermistor `R15` is on the **mainboard**, not in the pack | [cell](../../../components/generic/papermono-1150mah-liion-cell/README.md) |
| Buttons | 2 user + 1 power (on / off / reset / boot) | — |
| Size / weight | 62.0 × 101.0 × 8.0 mm, 74.7 g | vendor |

Two specifications are worth qualifying rather than repeating. **"4-level
greyscale"** is M5Stack's claim and the vendor OTP demo does implement a working
four-grey mode, but the DKE panel manual's own optical table reads
`GN — 2Grey Level`; the contradiction is unresolved and recorded. **Bluetooth**
is a capability of the ESP32-S3 silicon, not something M5Stack lists in the
PaperMono specification table — one launch article's "Bluetooth 5.0 LE + Mesh"
line is that publication's inference, not a vendor spec.

## Architecture and components

```
                 ┌──────────────┐
   USB-C ──▶ OVP │  IP2315      │──▶ battery 1150 mAh
   5.95 V        │  charger     │      │
                 └──────┬───────┘      │
                    I²C │ (gated)      ▼
                        │         VBUS_L0 / VBAT_L0
                        │              │
   ┌────────────────────┴──────────────┴────────────────────┐
   │  M5PM1  (PY32L020F15U6)   I²C 0x6E   ── owns L0..L2     │
   │  reset + boot straps + rail enables + wake logic        │
   └───┬────────────────────────────────────────────────────┘
       │ SOC_RESET, BOOT_OUT
       ▼
   ┌───────────────┐   SPI2   ┌──────────┐   FPC   ┌──────────────┐
   │  ESP32-S3R8   │─────────▶│ SSD1677  │────────▶│ DKE 3.97" EPD│
   │  16 MB flash  │          └──────────┘         └──────────────┘
   │  8 MB OPI RAM │   SPI1   ┌──────────────────┐
   │               │─────────▶│ Stamp LoRa-1262  │
   │               │  SDMMC   ┌──────────┐
   │               │─────────▶│ microSD  │
   └───┬───────────┘          └──────────┘
       │ I²C  GPIO47/48  (one bus, seven devices)
       ├── 0x32 RX8130CE RTC ──── nIRQ ──▶ M5PM1 G0
       ├── 0x38 FT6336G touch
       ├── 0x4F M5IOE1 expander ─── 14 pins: panel/touch/SD/mic power,
       │                             resets, LED, LoRa reset + ant switch
       ├── 0x50 ST25R3916 NFC
       ├── 0x68 BMI270 IMU ──────── INT1 ──▶ M5PM1 G4
       ├── 0x6E M5PM1
       └── 0x75 IP2315   (behind a level translator, normally disconnected)
```

The defining structural fact is that **two auxiliary microcontrollers sit
between the application processor and most of the board.** Panel power, panel
reset, touch power and reset, microSD power and detect, microphone power, NFC
enable, LoRa reset and antenna switch, two of three LED colours, and the
charger's bus access are all behind the M5IOE1. Reset, boot mode, rail enables
and every deep wake source are behind the M5PM1. Neither is optional.

## Common tasks / How do I…?

Every fitted capability has a task-oriented guide under
[**`features/`**](features/README.md). **Nothing in them was tested on hardware** — see
[Known gaps](#known-gaps).

| Task | Guide |
|---|---|
| Drive the e-paper reliably (and not damage it) | [`features/epaper-display.md`](features/epaper-display.md) |
| Set frontlight brightness | [`features/frontlight.md`](features/frontlight.md) |
| Read touch input | [`features/touch.md`](features/touch.md) |
| Read the buttons, drive the RGB indicator | [`features/buttons-and-rgb-led.md`](features/buttons-and-rgb-led.md) |
| Put the device to sleep and wake it | [`features/power-and-sleep.md`](features/power-and-sleep.md) |
| Read the battery, control charging | [`features/battery-and-charging.md`](features/battery-and-charging.md) |
| Get on Wi-Fi, use BLE | [`features/wifi-and-bluetooth.md`](features/wifi-and-bluetooth.md) |
| Send and receive LoRa | [`features/lora.md`](features/lora.md) |
| Set up NFC | [`features/nfc.md`](features/nfc.md) |
| Read motion, wake on it | [`features/imu.md`](features/imu.md) |
| Keep time, schedule a wake-up | [`features/rtc.md`](features/rtc.md) |
| Mount a microSD card | [`features/microsd.md`](features/microsd.md) |
| Record audio | [`features/microphone.md`](features/microphone.md) |
| Make a noise | [`features/buzzer.md`](features/buzzer.md) |
| Flash it, get a serial console | [`features/usb-and-serial.md`](features/usb-and-serial.md) |
| Use the I/O expander safely | [`features/io-expander.md`](features/io-expander.md) |
| Understand which GPIO does what | [`pinouts-and-buses.md`](pinouts-and-buses.md) |
| Avoid the `PYG3` pin-naming hazard | [`pin-naming-and-the-pyg-ambiguity.md`](pin-naming-and-the-pyg-ambiguity.md) |
| Work out what conflicts with what | [`resources-and-conflicts.md`](resources-and-conflicts.md) |
| Check whether something is known to work | [`compatibility-and-status.md`](compatibility-and-status.md) |
| Find M5Stack's documentation for another product | [`vendors/m5stack`](../../../vendors/m5stack/README.md) |

## Development

- **Frameworks**: Arduino (arduino-esp32 3.3.10) and ESP-IDF **5.5.1**. UiFlow2
  is advertised, but the UiFlow2 page states no required firmware version, no
  block list and no limitations — a genuine documentation gap, confirmed by
  full-text search rather than assumed.
- **Libraries**: `M5Unified`, `M5GFX`, `M5PM1`, `M5IOE1`, `M5Unit-NFC`,
  `RadioLib` 7.2.1.
- **The vendor's `M5Unified#develop` requirement is stale.** `board_M5PaperMono`
  is byte-identical on `master` and `develop` and ships in released tags
  M5Unified 0.2.21 and M5GFX 0.2.28.
- **Octal PSRAM is mandatory** (`board_build.arduino.memory_type = qio_opi`).
  Without it M5GFX aborts display init with `"M5PaperMono need OPI-PSRAM
  enabled"` and you get a blank screen on working hardware.
- **Partitions**: single `factory` app at offset `0xF00000`, ~15 MB, **no OTA
  slot** in either vendor project.
- **Download mode**: hold the power button ~2 s until the red LED blinks.
- **E-paper waveforms**: M5Stack's own note says the M5GFX waveforms "are
  currently unstable" and recommends the panel maker's OTP waveform example
  instead. This is corroborated in-tree — M5GFX `develop` has replaced the LUTs,
  leaving the previous `lut_quality` commented out. Do roughly one full refresh
  per ten partial refreshes, and never run continuous partial refreshes: the
  vendor warns of irreversible DC-imbalance damage.

## Factory firmware

Two images were retrieved from the M5Burner API and validated by content
(ESP32 image magic `0xE9`), held in [`artifacts/firmware/`](artifacts/firmware/):

| Image | Bytes | SHA-256 | Build identity |
|---|---|---|---|
| `C153-PaperMono-UserDemo-v1.2.bin` | 2,868,208 | `72c290bc2ffa216041b276660277369bd17ecef92315e367d98bb2c96c8428fa` | `PaperMono-UserDemo`, version **`c78f6c5-dirty`**, IDF v5.5.1, 2026-08-06 |
| `crosspoint-paper-mono-cjk-1.5.0-RC.bin` | 10,319,500 | `e2dee32b468da1d743b9fe8889eca959f5c0acdbe09c8f4cc3e69c69f8ebe935` | `crosspoint-reader-mono`, `paper-mono-v2-15-g87a191f`, IDF 5.5.2 — third-party e-reader |

The official image reports **`-dirty`**: it was built from an uncommitted tree
and is therefore **not reproducible from any published commit**. That is why the
binaries are retained here rather than referenced. Source for the demo is at
`m5stack/M5PaperMono-UserDemo` (HEAD `c1099107271d31a0678d661a896e2b04dbb331ea`,
2026-08-10), but it will not reproduce these bytes.

The vendor link labelled "PaperMono Factory Reset Firmware" resolves to a
firmware record named "PaperMono UserDemo" — the same image, differently
labelled.

## Pricing and availability

All observations dated **2026-09-01**. Not currency-converted: three VAT regimes,
not comparable.

| Seller | SKU | Price | Stock |
|---|---|---|---|
| shop.m5stack.com | C153 | **USD 65.00** | out of stock |
| shop.m5stack.com | C153-LITE | **USD 55.00** | out of stock |
| thepihut.com | C153 | GBP 62.40 incl. VAT | out of stock |
| openelab.io / .de | M5-C153 | EUR 79.95 | listed available, title says "Pre-sale" |

The NFC + LoRa hardware is the entire USD 10 difference between the two SKUs.
Confirmed **not** sold by Amazon, AliExpress, Switch Science, Adafruit,
Reichelt, Botland or Core Electronics. Mouser, DigiKey and TinyTronics were
bot-walled and returned no determination — an explicit gap, not a negative.

It sold out within minutes of the store opening and had not restocked eleven
days later. The vendor said "two or three months" on 2026-08-22; one publication
reported "next year". Both are recorded; they conflict. A widely repeated claim
that the delay is due to an e-ink driver IC shortage was **checked against the
cited post and its full reply chain and does not appear there** — it is hearsay.

## Community, editorial and project coverage

Eleven days after launch: **zero written reviews, one hands-on video** (Volos
Projects, 2026-08-29, carrying a vendor affiliate link and self-described as a
first look). Everything written — LinuxGizmos, CNX-Software, Liliputing,
MuyLinux, Tux Machines — traces back to a single vendor blog post and is
reproduced marketing copy. Hackaday published nothing. Two independent broad
search passes reached the same conclusion.

The real early signal is code rather than articles: four third-party GitHub
projects appeared within eleven days, two with credible hardware validation
(`MagicCube/free-ink-on-paper-mono` and `Free-Ink/freeink-sdk`), independently
corroborating an M5PM1 single-click-reset behaviour.

One widely repeated factual error worth flagging: a launch article stated the
USD 55 model has NFC and LoRa. It does not — that is the Lite.

## Distinctive strengths

- A genuine hardware low-power architecture, not a sleep mode: five states, wake
  on RTC/motion/touch/keys with the application processor unpowered.
- Frontlit e-paper with touch at this size and price is uncommon.
- NFC and LoRa on the same board as an e-paper reader is, as far as this survey
  found, unique in the class.
- Complete published schematic, and vendor datasheets for both custom chips —
  better hardware disclosure than most comparable products.

## Shortcomings and constraints

- **No expansion connector at all.** Every GPIO is committed; anything added has
  to share the I²C bus.
- Vendor acknowledges its own display waveforms are unstable and recommends
  bypassing its graphics library for refresh configuration.
- Two auxiliary MCUs mean two more firmware surfaces, two more documentation
  sets, and a naming ambiguity that can silently cut panel power.
- 4 grey levels and 480 × 800 are a step down from the PaperS3 it sits beside.
- No OTA partition in either vendor project.
- No certification identifiers published.
- Out of stock since launch day with conflicting restock guidance.
- Official firmware not reproducible from published source.

## When to use / when not to use

**Use it** for battery-powered, long-idle, event-driven applications — access
control and identity terminals, e-paper signage with LoRa telemetry, sensor
displays that wake on motion or schedule — where the power architecture is the
point and the display is a low-duty output.

**Do not use it** where you need a fast or high-fidelity e-paper display
(4 grey levels, and the vendor's own refresh guidance is conservative), where
you need to attach external hardware (no expansion port), where you need field
updates (no OTA partition as shipped), or where you need regulatory paperwork
(none published). For a general e-paper development board with expansion, prefer
Inkplate or the [Waveshare ESP32-S3-ePaper-3.97](../../waveshare/esp32-s3-epaper-3.97/README.md)
(same SoC, memory and panel size, with headers and an audio path instead of
radios); for a reading device, this is a
development board, not a reader.

## Known gaps

This is a **broad-coverage snapshot dated 2026-09-01**, not a claim of
completeness. Not done in this pass, and honestly outstanding:

- [`performance.md`](performance.md) — **now written, and its content is mostly absence**:
  no current in any power state, no battery runtime, no Wi-Fi/SD/LoRa throughput, and the
  vendor's four refresh timings are lab figures for a LUT set that may no longer be the
  shipped one. The page inventories every missing measurement rather than inventing any
- `examples/` catalogue — the vendor and third-party examples are referenced by upstream
  URL and commit in [`coverage.md`](coverage.md), but none is vendored here
- Acquisition manifest and downloader — **present** at
  [`acquisition/`](acquisition/README.md); note its artifact IDs (`S10`, `S11`, `S30`, `S31`, …)
  predate the renumbering in [`sources.md`](sources.md) (`S14`, `S15`, `S38`, `S39`, …) and
  have not been reconciled. Hashes, sizes and URLs agree in both
- **No product or teardown imagery retained** — recorded, with the reasons and a work list,
  in [`media.md`](media.md) and [`media/manifest.json`](media/manifest.json)
- Component records for `stmicroelectronics/st25r3916` and `seiko-epson/rx8130ce` are
  **stubs** — the datasheet artifacts are held, the write-ups are not done
- Nothing verified on physical hardware: **every behavioural claim in this
  record — including in every `features/` guide — is `inferred`, `reported-working` or
  read from source, never `executed-success` against a device**

Written in this pass: [`features/`](features/README.md) (16 guides),
[`coverage.md`](coverage.md), [`resources-and-conflicts.md`](resources-and-conflicts.md),
[`compatibility-and-status.md`](compatibility-and-status.md), and the vendor guides
[`vendors/m5stack`](../../../vendors/m5stack/README.md) and
[`vendors/dke`](../../../vendors/dke/README.md).

Added subsequently, on the same 2026-09-01 evidence base and with nothing new retrieved:
[`development.md`](development.md), [`factory-firmware.md`](factory-firmware.md),
[`product-history-and-family.md`](product-history-and-family.md),
[`market-and-pricing.md`](market-and-pricing.md),
[`comparisons-and-recommendations.md`](comparisons-and-recommendations.md),
[`community.md`](community.md), [`performance.md`](performance.md),
[`media.md`](media.md) and [`media/manifest.json`](media/manifest.json).

See [`gaps-and-conflicts.md`](gaps-and-conflicts.md) for the full conflict list.

## Artifact layout

```
artifacts/
├── schematic/PaperMono_SCH_V0.6.2_20260522.pdf      1,462,039 B  6 sheets, Altium
├── mechanical/C153_PaperMono_model_size.pdf            21,346 B
└── firmware/
    ├── C153-PaperMono-UserDemo-v1.2.bin            2,868,208 B
    ├── crosspoint-paper-mono-cjk-1.5.0-RC.bin     10,319,500 B
    └── esp-image-analysis.txt
```

Component-owned documents are filed under the component they describe, not here:
the DKE panel manual, the SSD1677, M5PM1, M5IOE1, ST25R3916, SX1262, RX8130CE,
BMI270 and ESP32-S3 datasheets each live in their own component record's
`artifacts/`. Several are M5Stack mirrors of other vendors' documents and are
named and labelled as such, because the revision M5Stack serves is not always
the current one — the BMI270 mirror is five years behind Bosch's.
