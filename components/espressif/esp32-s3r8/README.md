# Espressif ESP32-S3R8

- **Category:** dual-core wireless MCU/SoC with in-package PSRAM
- **Research status:** verified against available board schematic/code and linked primary material
- **Retrieved:** 2026-08-21

## Capabilities

Two Xtensa LX7 cores up to 240 MHz, 2.4 GHz 802.11 b/g/n Wi-Fi (Wi-Fi 4), Bluetooth 5 LE with Bluetooth Mesh, USB 2.0 OTG and USB Serial/JTAG, vector instructions, 512 KB SRAM and 8 MB octal PSRAM in the R8 variant. The radio is **Wi-Fi + Bluetooth LE only** — there is no Classic Bluetooth; see [Radio capabilities and the Classic Bluetooth limitation](#radio-capabilities-and-the-classic-bluetooth-limitation).

## Limits

No Classic Bluetooth — see [Radio capabilities and the Classic Bluetooth limitation](#radio-capabilities-and-the-classic-bluetooth-limitation) below, which treats this at length because it is the single most consequential architectural constraint of the part. The R8 suffix identifies 8 MB in-package PSRAM, not flash; this board supplies 16 MB external flash. GPIO electrical, strapping, ADC and radio limits remain those in the datasheet.

## Radio capabilities and the Classic Bluetooth limitation

This section exists because "no Classic Bluetooth" is not a footnote. It is a chip-level capability boundary that forces board-level design decisions, and it has already forced one on a device documented here: the Waveshare ESP32-S3-Knob-Touch-LCD-1.8 fits an **entire second MCU** solely to supply the profiles the ESP32-S3 cannot.

### What the radio actually is

| Radio | ESP32-S3 support | Notes |
|---|---|---|
| Wi-Fi | **Yes** — IEEE 802.11 b/g/n, 2.4 GHz only | "Wi-Fi 4" generation. 20/40 MHz channels; STA, SoftAP and combined modes |
| Wi-Fi 5/6 (802.11ac/ax), 5 GHz | **No** | Not present in silicon on any current ESP32-S3 |
| Bluetooth Low Energy | **Yes** — Bluetooth 5 (LE) | Includes the Bluetooth 5 LE PHY features: 2 M PHY, Coded PHY (long range), extended advertising |
| Bluetooth Mesh | **Yes** — via ESP-BLE-MESH | An LE-based mesh networking profile; unrelated to BR/EDR |
| Bluetooth Classic / BR/EDR | **No** | There is no BR/EDR baseband or link controller in the die |

The primary evidence is the datasheet itself. Espressif titles the document **"ESP32-S3 Wi-Fi + Bluetooth *Low Energy* SoC"**, and the SoC block diagram's wireless section contains exactly two Bluetooth blocks — **"Bluetooth LE Link Controller"** and **"Bluetooth LE Baseband"**. There is no BR/EDR link controller or BR/EDR baseband block, and no BR/EDR entry anywhere in the RF specification tables. See the local copy at [artifacts/esp32-s3-datasheet.pdf](artifacts/esp32-s3-datasheet.pdf). Corroborating this from the software side, the ESP-IDF Programming Guide's Bluetooth API section, when rendered for the `esp32s3` target, offers only *Controller & HCI*, *Bluetooth Common*, *Bluetooth LE* (Bluedroid), *NimBLE-based Host APIs* and *ESP-BLE-MESH* — the Classic Bluetooth API pages that appear for the `esp32` target are absent (checked 2026-08-22 against the v6.0.2 build).

This is a **hardware** absence, not a software, licensing or fuse-configuration one. No ESP-IDF version, no Arduino-ESP32 core version, and no third-party library can add BR/EDR to an ESP32-S3. The usual way developers discover this is a build failure from `BluetoothSerial.h` under Arduino-ESP32 reporting that Bluetooth Classic is unavailable for this target; that message is accurate and final.

### What you therefore cannot do with an ESP32-S3 alone

Every profile in the following table is defined over BR/EDR and is consequently unavailable:

| Profile | Typical use | Available on ESP32-S3? |
|---|---|---|
| A2DP sink | Being a Bluetooth speaker — a phone streams stereo music to your device | **No** |
| A2DP source | Being a Bluetooth transmitter — streaming stereo music to headphones or a speaker | **No** |
| AVRCP (CT/TG) | Play/pause/next/previous, absolute volume, track metadata, album art over OBEX/BIP | **No** |
| HFP / HSP | Hands-free calling, microphone audio to a phone, call control | **No** |
| SPP | The classic "Bluetooth serial port" — RFCOMM streams, the usual Android-terminal pairing route | **No** |
| Classic BT HID (host or device) | Many commodity keyboards, mice and media remotes, which are BR/EDR-only | **No** |
| Legacy pairing with BR/EDR-only peers | Older car head units, older audio gear | **No** |

The practical headline is: **most things people mean by "Bluetooth audio" are Classic Bluetooth.** If your product description contains the phrase "Bluetooth speaker", "Bluetooth headphones", "Bluetooth receiver", or "control music playback from the device", you are describing A2DP and AVRCP, and the ESP32-S3 cannot provide them. The same trap catches "just talk to it over Bluetooth serial from my phone" (SPP) and "pair my Bluetooth keyboard to it" (Classic HID) — both are extremely common expectations and both fail on this part.

A second, subtler consequence: interoperability with *existing* peers. Even where an LE equivalent of a profile exists, the peer device has to speak it. A ten-year-old car stereo will not.

### What LE alternatives exist, and where they stop

| Alternative | What it replaces | Status on ESP32-S3 | Practical limits |
|---|---|---|---|
| BLE GATT, custom service | SPP | **Fully supported**, Bluedroid or NimBLE | Works well, but only with a peer you also write. Throughput is far below RFCOMM. There is no standard "BLE serial port" — Nordic UART Service (NUS) is a de-facto convention, not a SIG profile, so generic terminal apps may or may not speak it |
| BLE HID over GATT (HOGP) | Classic BT HID | **Fully supported** as a HID *device* | Modern hosts (current Windows/macOS/iOS/Android/Linux) accept BLE HID devices. Acting as a HID *host* for arbitrary commodity peripherals is much weaker, and BR/EDR-only peripherals remain unreachable regardless |
| ESP-BLE-MESH | — | **Fully supported** | Mesh control networking, not a Classic replacement; no audio |
| ESP-NOW | Ad-hoc device-to-device links | **Fully supported** (Wi-Fi-layer, Espressif-proprietary) | Espressif-to-Espressif only. Phones and PCs cannot participate. Good for a companion remote or sensor link, useless for consumer interoperability |
| Wi-Fi audio streaming (HTTP/RTSP/AirPlay-like, or ESP-ADF pipelines) | A2DP | Supported at the transport level | Requires network provisioning and a cooperating source application; not a drop-in for "pair and play" |
| **LE Audio (BAP/ASHA-class profiles) with the LC3 codec** | A2DP, HFP | **Not available in practice — see caveat** | Discussed below |

**LE Audio caveat — read this carefully.** LE Audio is the Bluetooth SIG's LE-based replacement for A2DP/HFP, built on Isochronous Channels (CIS/BIS) introduced in Bluetooth 5.2, with LC3 as its mandatory codec. The ESP32-S3 is a **Bluetooth 5 (LE)** part; Isochronous Channel support is a Bluetooth 5.2 controller feature, and **we have found no Espressif documentation stating that the ESP32-S3 controller implements Isochronous Channels**, nor any LE Audio / BAP / LC3 API in the ESP-IDF Bluetooth API reference rendered for the `esp32s3` target. On that evidence, LE Audio should be treated as **unavailable on the ESP32-S3**.

Two honest qualifications: (1) this is an argument from the *absence* of a documented feature rather than from an explicit Espressif statement of non-support, so it is marked **uncertain** rather than asserted as a silicon fact; (2) even if a controller-level path existed, LE Audio would still not solve the compatibility problem, because the *peer* must also support LE Audio, and the overwhelming majority of phones, cars and headphones in service today do not. **Do not plan a product around LE Audio on this chip.** If you need to settle the question definitively for a specific silicon revision and IDF version, check the ESP-IDF release notes and the controller's supported-features list for your exact target rather than relying on this page.

### Which Espressif parts have Classic Bluetooth

Only the **original ESP32 series** does. Every later Espressif SoC is Bluetooth LE only (or has no Bluetooth at all).

| SoC | Wi-Fi | Bluetooth Classic (BR/EDR) | Bluetooth LE | Notes |
|---|---|---|---|---|
| **ESP32** (incl. ESP32-U4WDH, -D0WD, -WROOM-32, -WROVER) | 802.11 b/g/n | **Yes** | Yes, BLE 4.2 | The only Espressif family with BR/EDR. A2DP/AVRCP/SPP/HFP/Classic-HID all available |
| ESP32-S2 | 802.11 b/g/n | No | **No Bluetooth at all** | Wi-Fi-only part; frequently mistaken for having BLE |
| **ESP32-S3** | 802.11 b/g/n | **No** | Yes, Bluetooth 5 LE + Mesh | This part |
| ESP32-C3 | 802.11 b/g/n | No | Yes, Bluetooth 5 LE + Mesh | RISC-V |
| ESP32-C6 | 802.11 b/g/n **+ ax (Wi-Fi 6)** | No | Yes, Bluetooth 5 LE | Also 802.15.4 (Thread/Zigbee) |
| ESP32-H2 | **No Wi-Fi** | No | Yes, Bluetooth 5 LE | 802.15.4-centric part |
| ESP32-C2 / ESP8684 | 802.11 b/g/n | No | Yes, Bluetooth 5 LE | Cost-reduced |
| ESP32-P4 | **No radio** | No | No | Application processor; needs a companion radio SoC |

The one-line rule worth memorising: **if the part number has a letter suffix after "ESP32", it does not have Classic Bluetooth.** Verify against the specific part's datasheet before committing; this table is a navigation aid, and Espressif's line-up changes.

### Design workarounds when Classic Bluetooth is genuinely required

In rough order of decreasing integration:

1. **Use an original ESP32 instead of an S3.** Simplest and cheapest if you do not need what the S3 adds. You give up the S3's extra performance, PIE/SIMD vector instructions, native USB OTG, larger PSRAM options and Bluetooth 5 LE PHY features, and you inherit the older part's BLE 4.2 stack. For a device whose headline feature is Classic Bluetooth audio, this is usually the right answer.
2. **Keep the S3 and add an external Classic Bluetooth module.** A self-contained BT audio module (typically speaking I2S plus a UART or GPIO control interface) offloads the whole stack. You gain a known-good audio path; you lose control over the profile behaviour, and you are dependent on a module vendor's firmware, which is often undocumented and unmodifiable.
3. **Fit a companion MCU that has BR/EDR — most naturally an original ESP32 — and bridge the two chips.** You keep the S3 for display, USB, storage and DSP, and hand Bluetooth Classic to the second chip. This costs a second crystal, a second antenna, a second flash, board area, power, an inter-MCU transport (usually UART) and a protocol you must design, plus a second firmware image to build, flash and version. It is not cheap, and it is chosen when *both* halves of the capability set are mandatory.

**Worked example of approach 3.** The [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) is a shipping product built exactly this way. It pairs this ESP32-S3R8 with an [ESP32-U4WDH](../../espressif/esp32-u4wdh/README.md) — an original-series ESP32 in a compact package with 4 MB in-package flash — whose *only* job is Bluetooth Classic. The factory firmware on that second MCU implements A2DP sink and source, AVRCP controller and target, AVRCP Cover Art over OBEX/BIP, SPP, Classic BT HID and BLE HID. The board carries a second 40 MHz crystal and a second antenna for it, routes an inter-MCU UART between the two chips, and splits the audio hardware across them (the S3 owns the analogue mux select; the U4WDH owns the DAC mute line), so neither MCU can produce sound alone. The device-level write-up is [Classic Bluetooth on this board](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/classic-bluetooth.md), and the two-image flashing consequences are in [factory firmware and restore](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/factory-firmware.md).

That example is the concrete illustration of the cost: a Classic-Bluetooth requirement discovered late turns into a second processor, a second RF chain, an undocumented private protocol, a doubled flashing procedure and a permanent cross-chip coupling in the audio path. It is far cheaper to check this constraint at part-selection time.

### Rules of thumb

- Audit your requirements for A2DP, AVRCP, SPP, HFP and Classic HID **before** selecting an S3.
- "Bluetooth" in a marketing requirement almost never means "Bluetooth LE". Ask which profiles.
- If the peer device already exists and you cannot change its firmware, its Bluetooth generation, not yours, decides the answer.
- Both radios on a two-chip design are independent and can run simultaneously; that is a genuine benefit of the companion-MCU approach, not merely a workaround.

## Board wiring

Primary application/display MCU. QSPI LCD: GPIO13 clock, 14 CS, 15-18 D0-D3, 21 reset, 47 backlight. Touch/haptic I2C: GPIO11 SDA, 12 SCL; touch INT 9 and reset 10. SDMMC: GPIO2 D3, 3 CMD, 4 CLK, 5 D0, 6 D1, 42 D2. Encoder: GPIO8/A and GPIO7/B. PDM MIC: GPIO45 clock and 46 data. I2S DAC: GPIO39 BCK, 40 LRCK/WS, 41 data. USB D-/D+ are GPIO19/20; inter-MCU UART is GPIO48 RX and GPIO38 TX; battery ADC is GPIO1.

## Firmware and APIs

Supported by ESP-IDF and Arduino-ESP32. Use target `esp32s3`; official examples use ESP-IDF 5.1.4 and require Arduino-ESP32 >=3.2.0 for Arduino builds.

## Processor Instruction Extensions (PIE)

PIE is Espressif's name for the ESP32-S3's 128-bit SIMD/vector instruction set extension to the Xtensa LX7 cores (informally called the "pixel engine"). It adds wide vector registers and instructions for parallel integer and fixed-point arithmetic, aligned/unaligned vector load-store, and multiply-accumulate.

This matters for this board because the ESP32-S3 drives the QSPI LCD as well as the PDM microphone and I2S audio path. PIE is the hardware basis for accelerating exactly those workloads: pixel format conversion and blitting for the display, and FIR/FFT/matrix kernels for audio DSP. Espressif's `esp-dsp` library and LVGL's ESP32-S3 assembly paths use these instructions, so using them is normally a matter of enabling the accelerated library builds rather than hand-writing intrinsics.

There is **no separate "PIE guide" PDF**. Espressif publishes the PIE specification as **Chapter 1, "Processor Instruction Extensions (PIE)"**, of the ESP32-S3 Technical Reference Manual, covering instruction encoding fields, pipeline hazard rules, and the extended-instruction functional description. See the local copy at [artifacts/esp32-s3-technical-reference-manual.pdf](artifacts/esp32-s3-technical-reference-manual.pdf) (TRM v1.8). This was confirmed on 2026-08-21 against Espressif's own documentation-platform full-text index; the historically cited standalone URL `esp32-s3_processor_instruction_extensions_pie_guide_en.pdf` does not resolve and has no Wayback snapshot.

## Versions and revisions

ESP32-S3 family datasheet and TRM snapshots retrieved on the date below; package marking/silicon revision is not stated in the board documents. The local TRM is version 1.8 (revised 2026-03-04) and matches the byte size of the copy currently served by Espressif's documentation platform. The errata and hardware design guidelines are continuously-updated `latest`/`master` esp-docs builds rather than statically numbered revisions, so they carry no cover version number; they are pinned here by SHA-256 and retrieval date.

## Caveats

Do not describe the board's 16 MB W25Q128 flash as part of ESP32-S3R8. GPIO0 is also brought into the board's unusual USB/target selection circuitry.

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md)
- [Seeed Studio XIAO ESP32S3 Sense](../../../devices/seeed-studio/xiao-esp32s3-sense/README.md)

### Seeed Studio XIAO ESP32S3 Sense

Fitted as **U1**, bare QFN56 (footprint `QFN56G-0.4-7X7MM`), on a 17.78 × 21.14 mm 4-layer board — one of the smallest ESP32-S3 designs in production. Paired with an external 8 MB `GD25Q64ENIGR` flash on the dedicated SPI pins and a 40 MHz crystal (X1, reached through `L5` 24 nH since board revision v1.2).

Three integration details from this board are worth carrying to any ESP32-S3R8 design, because they are properties of the **package**, not of Seeed's layout:

- **GPIO33–GPIO37 and `SPICS1` are no-connects at board level.** The PCB netlist shows U1 pins 28 and 38–42 terminating in single-pad nets. They are consumed *inside the package* by the octal PSRAM die. Driving them raises no error — it corrupts PSRAM access, typically surfacing as a cache-access panic far from the offending code. This is the most important practical consequence of choosing the R8 variant.
- **The R8 suffix means 8 MB of in-package PSRAM, not flash.** Flash is a separate external device. This is a persistent source of confusion in marketplace listings and community posts.
- **The JTAG pins are ordinary GPIO and boards do reuse them.** Here `MTCK`/`MTDO`/`MTDI`/`MTMS` (GPIO39/40/41/42) carry the camera SCCB bus and the PDM microphone, so hardware debugging is impossible with the sensor board attached.

Seeed left the `GPIO45` and `GPIO46` strapping pins unconnected, which removes two classic ESP32-S3 footguns; only `GPIO3` (JTAG source select) is exposed on the user header.

Also relevant to this board: the [Classic Bluetooth limitation](#radio-capabilities-and-the-classic-bluetooth-limitation) below. The XIAO ESP32S3 Sense is frequently proposed for "Bluetooth audio" wearables, and **A2DP, AVRCP, HFP, SPP and Classic HID are all unavailable** on this silicon.

Full pin map: [pinouts-and-buses.md](../../../devices/seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md#11-full-esp32-s3r8-pin-usage-map)

## Related components

- [ESP32-U4WDH](../../espressif/esp32-u4wdh/README.md) — original-series ESP32 with BR/EDR, used as the Classic Bluetooth companion MCU on the Waveshare knob board
- [Espressif vendor sourcing guide](../../../vendors/espressif/README.md) — hosts, URL templates and validation procedure for all Espressif documents cited here

## Framework guides

Distilled from the ESP-IDF and ESP-IoT-Solution PDFs formerly held in `artifacts/` (see [ARCHIVED-FRAMEWORK-GUIDES.md](artifacts/ARCHIVED-FRAMEWORK-GUIDES.md)):

- [ESP-IDF peripheral capabilities](../../../guides/espressif/esp-idf-peripheral-capabilities.md) — ESP32 vs **ESP32-S3** vs ESP32-P4. Note in particular that the S3 is **`LEDC_LOW_SPEED_MODE` only**, and the [octal-PSRAM 120 MHz temperature warning](../../../guides/espressif/esp-idf-peripheral-capabilities.md#43-esp32-s3--120-mhz-octal-psram-is-temperature-fragile) that applies directly to this part's in-package octal PSRAM.
- [ESP-IoT-Solution components](../../../guides/espressif/esp-iot-solution-components.md) — the LCD interface-selection table, touch-controller support and the Knob component used by the knob board.

## Authoritative sources

| Title | URL | Retrieved | Version | Local artifact |
|---|---|---:|---|---|
| ESP32-S3 Series Datasheet | https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf | 2026-08-21 | - | artifacts/esp32-s3-datasheet.pdf |
| ESP32-S3 Technical Reference Manual (includes Ch. 1 Processor Instruction Extensions / PIE) | https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf | 2026-08-21 | v1.8, revised 2026-03-04 | artifacts/esp32-s3-technical-reference-manual.pdf |
| ESP32-S3 Series SoC Errata | https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32s3/esp-chip-errata-en-master-esp32s3.pdf | 2026-08-21 | esp-docs `master` build | artifacts/esp32-s3-errata.pdf |
| ESP Hardware Design Guidelines (ESP32-S3) | https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/esp-hardware-design-guidelines-en-master-esp32s3.pdf | 2026-08-21 | esp-docs `master` build | artifacts/esp32-s3-hardware-design-guidelines.pdf |
| ESP-IDF Programming Guide v5.1.4 (esp32s3 target) | https://docs.espressif.com/projects/esp-idf/en/v5.1.4/esp32s3/esp-idf-en-v5.1.4-esp32s3.pdf | 2026-08-21 | v5.1.4 | **archived 2026-08-24** — see [ARCHIVED-FRAMEWORK-GUIDES.md](artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) |
| ESP-IDF Programming Guide v5.2.5 (esp32s3 target) | https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32s3/esp-idf-en-v5.2.5-esp32s3.pdf | 2026-08-21 | v5.2.5 | **archived 2026-08-24** — see [ARCHIVED-FRAMEWORK-GUIDES.md](artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) |
| ESP-IoT-Solution Programming Guide | https://docs.espressif.com/projects/esp-iot-solution/en/latest/esp-iot-solution-en-master.pdf | 2026-08-21 | esp-docs `master` build | **archived 2026-08-24** — see [ARCHIVED-FRAMEWORK-GUIDES.md](artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) |
| ESP-IDF Bluetooth API reference, rendered for target `esp32s3` (evidence that no Classic Bluetooth or LE Audio API is offered for this target) | https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/bluetooth/index.html | 2026-08-22 | v6.0.2 as served | - (HTML, link-only) |

## Local artifacts

| File | Bytes | SHA-256 |
|---|---:|---|
| artifacts/esp32-s3-datasheet.pdf | 1098115 | `2d5a7cb7fd559d8d972bd88db32669c0196d23f22d7afaafb0f63d099b589a3f` |
| artifacts/esp32-s3-technical-reference-manual.pdf | 15215232 | `4484bf8a69035ec42a731c58c64ada6fbd1f1618c5559409f134d9ea083f444f` |
| artifacts/esp32-s3-errata.pdf | 628995 | `61c5b04ee6460fad9cb912404c8e80a8d4f82433cac28f4b9035aba44c92a826` |
| artifacts/esp32-s3-hardware-design-guidelines.pdf | 4193030 | `04aa9e57515f591477a2b84f8c99c6c13946e5a378980d07ce33d33787dd4f2b` |
| ~~artifacts/esp-idf-programming-guide-v5.1.4-esp32s3.pdf~~ **archived 2026-08-24** | 25626642 | `d1efc23ceef7859fd31e089f76dffa4ae9b1b56b0cce17a236b88795a10acfde` |
| ~~artifacts/esp-idf-programming-guide-v5.2.5-esp32s3.pdf~~ **archived 2026-08-24** | 29188396 | `e29de49974c7e9714f2ff6d98507cd7f0240ee538acb2120ce58ba44dc9be4ea` |
| ~~artifacts/esp-iot-solution-programming-guide.pdf~~ **archived 2026-08-24** | 26148298 | `8bf04c5a5a700337815c9df0e5b5f92275b4c1a900584bcb5034e8dc4802ab93` |
| **added 2026-08-24 (Waveshare mirror, older revisions)** | | |
| artifacts/esp32-s3-datasheet-v1.6-waveshare-mirror.pdf | 1186331 | `b79310e52e90599920fb067c9365263a18943c2efc4b9788edffc2b2d6cdefa1` |
| artifacts/esp32-s3-technical-reference-manual-v1.2-waveshare-mirror.pdf | 14540185 | `47bb075de167d8165fc845f4729396080cf0fc92a9f0b793a2527dddae8a2ed9` |

All artifacts were validated as genuine PDFs (`%PDF` header and `%%EOF` trailer present) on retrieval.

### Multiple document revisions held

This record deliberately holds **two revisions each** of the datasheet and the TRM. The older
revisions arrived 2026-08-24 from the Waveshare wiki mirror, relocated out of
`devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/datasheets/` so that component
documentation lives in the component record. Revision strings were read from pages 1–2 with
`pdftotext`; sizes and hashes were re-verified after the move.

| Document | Revision | Standing | Source | Local path |
|---|---|---|---|---|
| ESP32-S3 Series Datasheet | **v2.2** | current | Espressif direct | `artifacts/esp32-s3-datasheet.pdf` |
| ESP32-S3 Series Datasheet | v1.6 | older | Waveshare mirror, `files.waveshare.com/wiki/common/Esp32-s3_datasheet_en.pdf` | `artifacts/esp32-s3-datasheet-v1.6-waveshare-mirror.pdf` |
| ESP32-S3 Technical Reference Manual | **v1.8** | current | Espressif direct | `artifacts/esp32-s3-technical-reference-manual.pdf` |
| ESP32-S3 Technical Reference Manual | v1.2 | older | Waveshare mirror, `files.waveshare.com/wiki/common/Esp32-s3_technical_reference_manual_en.pdf` | `artifacts/esp32-s3-technical-reference-manual-v1.2-waveshare-mirror.pdf` |

**Which revision applies to the fitted part?** The knob board fits a bare **ESP32-S3R8**. The
silicon is described correctly by the **current** revisions (v2.2 / v1.8) — those are
authoritative for what the chip does, and are the default reference.

The v1.6 / v1.2 copies serve a narrower purpose: **they are what Waveshare designed and wrote
firmware against.** Register descriptions, reset defaults and errata wording do change between
Espressif revisions. When the board's observed behaviour or the vendor demo code disagrees with
the current TRM, check the older revision before assuming a bug — the older text often explains
the vendor's choice.

> ⚠ **The vendor links older documents.** Waveshare's wiki for this board serves ESP32-S3
> datasheet **v1.6** and TRM **v1.2** from its shared `/wiki/common/` pool. Anyone following the
> vendor's own documentation links lands on revisions several years behind Espressif's current
> publications. Prefer the Espressif copies above.
>
> Waveshare also updates that pool **in place**, so those URLs may silently begin returning a
> different revision under the same filename. The mirrored copies here are revision-pinned by
> filename and hash precisely because the upstream URL is not.

`esp-iot-solution` is included because it is the official home of the ESP-IDF component drivers this board depends on — QSPI LCD panel drivers, touch controllers, knob/encoder input and LVGL porting — none of which are documented in the core ESP-IDF programming guide. The v5.2.5 programming guide is retained alongside v5.1.4 because it is the newest ESP-IDF release for which Espressif publishes a PDF build at all; see the vendor guide for the details of that cutoff.

## Documentation sourcing

Espressif's documentation hosts, URL templates, migrated document classes and validation procedure are documented once, reusably, in the [Espressif vendor guide](../../../vendors/espressif/README.md). Read it before attempting to acquire further Espressif documents.

Note on source URLs: the `www.espressif.com/sites/default/files/documentation/*.pdf` paths now HTTP-redirect to Espressif's new documentation platform. The datasheet and TRM still resolve to real PDFs through that redirect; the errata and hardware design guidelines have been migrated into the versioned `esp-docs` projects, whose PDF build URLs are given above. `esp-dsp`, which would otherwise be the natural reference for the S3's PIE/SIMD kernels, publishes **no PDF build** — only an HTML site and its GitHub repository. Module datasheets (ESP32-S3-WROOM-1/-2, ESP32-S3-MINI-1) are deliberately **not** stored here: this board mounts a bare ESP32-S3R8, not a module, so module documentation would not describe the part fitted.
