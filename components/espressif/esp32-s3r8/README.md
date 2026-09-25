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

- **The entire [LilyGO T-Display-S3 family](../../../devices/lilygo/t-display-s3-shared/README.md)** — eleven boards, every one of which uses the ESP32-S3R8, as a **bare die** rather than a module: [T-Display-S3](../../../devices/lilygo/t-display-s3/README.md) and [Touch](../../../devices/lilygo/t-display-s3-touch/README.md), [AMOLED](../../../devices/lilygo/t-display-s3-amoled/README.md), [AMOLED Plus](../../../devices/lilygo/t-display-s3-amoled-plus/README.md), [AMOLED 1.64″](../../../devices/lilygo/t-display-s3-amoled-1-64/README.md), [AMOLED 1.43/1.75″](../../../devices/lilygo/t-display-s3-amoled-1-43-1-75/README.md), [T4-S3](../../../devices/lilygo/t4-s3/README.md), [AMOLED Lite](../../../devices/lilygo/t-display-amoled-lite/README.md), [Long](../../../devices/lilygo/t-display-s3-long/README.md), [Pro](../../../devices/lilygo/t-display-s3-pro/README.md). All pair it with a 16 MB [W25Q128JV](../../winbond/w25q128jv/README.md) over QIO and use the in-package 8 MB **OPI** PSRAM — which consumes **GPIO26–37** and is the reason these boards have so few free pins. Two integration facts recur family-wide and are documented at the family hub: the **native-USB `USB CDC On Boot` boot-blocking trap** ([`features/usb.md`](../../../devices/lilygo/t-display-s3/features/usb.md)) and the requirement to set Arduino `PSRAM = OPI PSRAM`, without which `ps_malloc()` silently fails.

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md)
- [Seeed Studio XIAO ESP32S3 Sense](../../../devices/seeed-studio/xiao-esp32s3-sense/README.md)
- [M5Stack PaperMono (SKU C153)](../../../devices/m5stack/papermono/README.md) — *added 2026-09-01*
- [Waveshare ESP32-S3-ePaper-3.97 (SKUs 33552 / 33810 / 33811)](../../../devices/waveshare/esp32-s3-epaper-3.97/README.md) — *added 2026-09-01*. Fitted as an **`ESP32-S3-WROOM-1-N16R8` module** rather than a bare die, so 16 MB flash + 8 MB **octal** PSRAM. The octal PSRAM consumes GPIO35–37, which the board's own schematic marks `NC` — see that record's [pinouts](../../../devices/waveshare/esp32-s3-epaper-3.97/pinouts-and-buses.md#is-anything-free). Native USB on GPIO19/20 with **no USB-UART bridge fitted**. Note the vendor storefront contradicts itself on the flash/PSRAM split; the module part number settles it ([C-WS3](../../../devices/waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws3--the-storefront-swaps-flash-and-psram))

### Seeed Studio XIAO ESP32S3 Sense

Fitted as **U1**, bare QFN56 (footprint `QFN56G-0.4-7X7MM`), on a 17.78 × 21.14 mm 4-layer board — one of the smallest ESP32-S3 designs in production. Paired with an external 8 MB `GD25Q64ENIGR` flash on the dedicated SPI pins and a 40 MHz crystal (X1, reached through `L5` 24 nH since board revision v1.2).

Three integration details from this board are worth carrying to any ESP32-S3R8 design, because they are properties of the **package**, not of Seeed's layout:

- **GPIO33–GPIO37 and `SPICS1` are no-connects at board level.** The PCB netlist shows U1 pins 28 and 38–42 terminating in single-pad nets. They are consumed *inside the package* by the octal PSRAM die. Driving them raises no error — it corrupts PSRAM access, typically surfacing as a cache-access panic far from the offending code. This is the most important practical consequence of choosing the R8 variant.
- **The R8 suffix means 8 MB of in-package PSRAM, not flash.** Flash is a separate external device. This is a persistent source of confusion in marketplace listings and community posts.
- **The JTAG pins are ordinary GPIO and boards do reuse them.** Here `MTCK`/`MTDO`/`MTDI`/`MTMS` (GPIO39/40/41/42) carry the camera SCCB bus and the PDM microphone, so hardware debugging is impossible with the sensor board attached.

Seeed left the `GPIO45` and `GPIO46` strapping pins unconnected, which removes two classic ESP32-S3 footguns; only `GPIO3` (JTAG source select) is exposed on the user header.

Also relevant to this board: the [Classic Bluetooth limitation](#radio-capabilities-and-the-classic-bluetooth-limitation) below. The XIAO ESP32S3 Sense is frequently proposed for "Bluetooth audio" wearables, and **A2DP, AVRCP, HFP, SPP and Classic HID are all unavailable** on this silicon.

Full pin map: [pinouts-and-buses.md](../../../devices/seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md#11-full-esp32-s3r8-pin-usage-map)

### M5Stack PaperMono (SKU C153)

> **FCC internal photographs — 2026-09-20.** The PaperMono's FCC filing
> (`2AN3WM5PAPERMONO`) includes an internal-photograph exhibit, now retained at
> [`devices/m5stack/papermono/artifacts/certification/`](../../../devices/m5stack/papermono/artifacts/certification/README.md).
> It is the first physical-hardware evidence for this part on this board.
>
> **Confirmed.** The die is legible in the exhibit (p. 3), marked
> `ESP32-S3` / `392025` / `R8MRK714000` / `FC00MCJ114` beneath the Espressif
> logo, in a **56-pin QFN** — corroborating "bare package, not a module" from a
> source other than the schematic. `R8` appears in the lot string, consistent
> with the R8 variant, though the marking format does not spell out `ESP32-S3R8`.
> A 4-pad crystal and the SOP-8 XMC flash sit immediately beside it, as the
> schematic predicts.
>
> Extraction: [`certification.md` §6](../../../devices/m5stack/papermono/certification.md#6--what-the-internal-photographs-show).

*Added 2026-09-01.* Fitted as **`U12`**, bare package, on schematic sheet 3 (`MCU_Core`) of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) and its Lite sibling. Paired with an external **16 MB [XMC XM25UH128DHIQT](../../xmc/xm25uh128dhiqt/README.md)** NOR flash and a **[40 MHz crystal](../../generic/cn4040m000157a530001-40mhz-crystal/README.md)** (`X1`, reached through `L7` = 24 nH). Evidence is the published schematic PDF and M5Stack's own source; no hardware was available.

**On this board the ESP32-S3 does not control its own power.** Two [Puya PY32L020F15U6](../../puya/py32l020f15u6/README.md) coprocessors running M5Stack firmware — the [M5PM1](../../m5stack/m5pm1/README.md) (I²C `0x6E`) and the [M5IOE1](../../m5stack/m5ioe1/README.md) (I²C `0x4F`) — own the rails, the power button, the `BOOT` strap, the display frontlight and every `L3B` peripheral rail. The S3 is a peripheral of its own power system.

Four integration details from this board are worth carrying to any ESP32-S3R8 design:

- **⚠ `GPIO45` and `GPIO46` are used as the PDM microphone clock and data.** Both are strapping pins: `GPIO45` selects the **`VDD_SPI` voltage** (default weak pull-down = 3.3 V; sampled high ⇒ **1.8 V**, which under-volts the 2.3–3.6 V flash), and `GPIO46` controls **ROM message printing**. The board is safe only because the microphone's rail (`PDM_VDD`) is behind a load switch that is **off at reset** — the protection is the load switch, not the wiring. Firmware that leaves that rail enabled across a soft reset re-exposes the `GPIO46` strap. See [LMD4737T261-AC02 §3.3](../../generic/lmd4737t261-ac02-pdm-microphone/README.md#33--both-pdm-signals-land-on-esp32-s3-strapping-pins).
- **`GPIO15`/`GPIO16` — the `XTAL_32K` pins — carry the e-paper SPI** (`G15_SPI2_CLK`, `G16_EINK_CS`), so there is **no 32.768 kHz crystal**. Timekeeping across sleep is the RX8130CE's job, not the S3's internal RTC.
- **`VDD_SPI` (pin 29) supplies the external flash directly** as `VDD_NOR`, with a 22 Ω series resistor on `SPICLK`. All four SPI data lines (`SPID`/`SPIQ`/`SPIWP`/`SPIHD`) are routed, and the fitted flash ships with its Quad Enable bit set at the factory — so **the hardware supports QIO**, even though the shipped factory image's header reports DIO. That conflict is resolved in [XM25UH128DHIQT §5](../../xmc/xm25uh128dhiqt/README.md#5--resolving-the-qiodio-conflict).
- **Octal PSRAM is enforced in software.** `M5GFX.cpp:2072–2081` aborts display initialisation and logs `"M5PaperMono need OPI-PSRAM enabled"` if `CONFIG_SPIRAM_MODE_OCT` is missing. The board still enumerates and runs — with a blank screen and one easily-missed log line. This is a direct consequence of choosing the **R8** variant, whose 8 MB in-package PSRAM is octal.

Also relevant: the [Classic Bluetooth limitation](#radio-capabilities-and-the-classic-bluetooth-limitation). The PaperMono has a buzzer and a PDM microphone but no Classic Bluetooth audio path, and none can be added.

Toolchain as shipped: **ESP-IDF 5.5.1**, `arduino-esp32` 3.3.10 as a managed component, 16 MB flash, single 15 MiB `factory` partition with **no OTA slots**.

### Xteink X4 Pro and X4 Classic — *added 2026-09-04*

Two sealed consumer e-readers built on the same ESP32-S3 board with **16 MB flash
and 8 MB PSRAM**, targeted in PlatformIO as `esp32-s3-devkitc1-n16r8`
(*"matches the X4 Pro dump"*). Identified from a factory flash dump and
on-hardware probing, not from a schematic — **no schematic or teardown exists for
either device**.

| | [X4 Pro](../../../devices/xteink/x4-pro/README.md) | [X4 Classic](../../../devices/xteink/x4-classic/README.md) |
|---|---|---|
| Board tag in stock firmware | `ESP32S3_X4_TL_SSD1677` | `ESP32S3_X4_CLA` (rev `ESP32S3_X4R2_CLA`) |
| Touch | [GT911](../../goodix/gt911/README.md) @0x5D | **none** |
| Frontlight | dual warm/cool, LEDC ch4/ch5 on GPIO8/9 | **none** — those pins become buttons |
| IMU | **none** | [QMI8658](../../qst/qmi8658a/README.md) @0x6B |
| Buttons | 2 side + power | **7 discrete, interrupt-driven** |
| Display DC / RST / BUSY | 18 / 14 / 6 | **14 / 10 / 18** |
| SD power enable | GPIO5, active-LOW | GPIO6, active-LOW |

Shared: display SPI SCLK 12 / MOSI 11 / CS 13 at 20 MHz; **native SDMMC 1-bit**
on CLK 41 / CMD 42 / DAT0 40; I²C SDA 39 / SCL 38 @ 400 kHz; native USB
D− 19 / D+ 20; charge STAT GPIO21 active-HIGH; **GPIO1 as a master peripheral
rail driven HIGH first at boot** — without it *"EPD BUSY never asserts, SD
returns 0xFF"*.

**Two S3-specific traps worth carrying forward:**

1. **GPIO19/20 are native USB D−/D+ and must never be probed at boot.** The
   sibling ESP32-C3 Xteink devices run an I²C device-fingerprint on SDA 20 /
   SCL 0; on an S3 those land on **D+ and a boot strap**. The SDK compiles that
   path out unless a C3 profile is in the build — a hand-rolled build combining
   both profiles would be actively dangerous.
2. **GPIO0 is the Left navigation button *and* the boot strap** on the X4 Pro.
   Fine as a button, but powering on with it held enters download mode.

**Why the R8 variant matters here.** The 8 MB in-package PSRAM is what separates
these from the C3-based [X4](../../../devices/xteink/x4/README.md) and
[X3](../../../devices/xteink/x3/README.md), where CrossPoint had to abandon
GitHub-release OTA because *"it causes out of memory issues on the x3"*. The
[InkBack SDK fork](https://github.com/goodyttoor/inkback-freeink-sdk) uses it for
*"PSRAM multi-buffer, damage windows, ghost budget"* — none of which is possible
on the C3 devices.

Stock toolchain differs by generation: the X4 Pro's 7.4.4 firmware is a **native
ESP-IDF 6.0.1** build (app descriptor `xteink_app 7.4.4`, built 2026-08-27), while
the C3 devices ship **Arduino-framework** builds on ESP-IDF 4.4.7.

→ [`devices/xteink/x4-pro/pinouts-and-buses.md`](../../../devices/xteink/x4-pro/pinouts-and-buses.md)
→ [`devices/xteink/x4-classic/README.md`](../../../devices/xteink/x4-classic/README.md)

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
| ESP32-S3 Series Datasheet — **M5Stack mirror** (linked from the PaperMono product page) | https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/472/esp32-s3_datasheet_en.pdf | 2026-09-01 | **v2.0**, 84 pp, 1 083 807 B | The revision M5Stack ships to PaperMono users; see [Four ESP32-S3 datasheet files](#four-esp32-s3-datasheet-files-four-different-sha-256-values--added-2026-09-01) | artifacts/esp32-s3-datasheet-v2.0-m5stack-mirror.pdf |
| M5Stack PaperMono schematic — `PaperMono_SCH_V0.6.2_20260522.pdf` | https://docs.m5stack.com/en/core/PaperMono | 2026-09-01 | V0.6.2, 2026-05-22, 6 sheets | The `U12` wiring in the PaperMono **Used By** section: strapping-pin usage, `VDD_SPI`→flash, `XTAL_32K` reuse | devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf |

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
| **added 2026-09-01 (M5Stack mirror, older revision)** | | |
| artifacts/esp32-s3-datasheet-v2.0-m5stack-mirror.pdf | 1083807 | `b6db403d6d5db8d1b4db0c8390ff7e0a7db714b8388e986e1c64bff563f76b61` |

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

### Four ESP32-S3 datasheet files, four different SHA-256 values — *added 2026-09-01*

The M5Stack PaperMono research pass added a fourth copy, and the resulting picture is worth
stating explicitly because it is the concrete case the research method's filing rules were
written around. **The tree now holds four ESP32-S3 datasheet files. No two are byte-identical.**

| Local file | Revision | Pages | Bytes | SHA-256 | Source |
|---|---|---:|---:|---|---|
| `artifacts/esp32-s3-datasheet.pdf` | **v2.2** — current | **87** | 1 098 115 | `2d5a7cb7fd559d8d972bd88db32669c0196d23f22d7afaafb0f63d099b589a3f` | **Espressif direct** |
| `artifacts/esp32-s3-datasheet-v2.0-m5stack-mirror.pdf` | **v2.0** | **84** | 1 083 807 | `b6db403d6d5db8d1b4db0c8390ff7e0a7db714b8388e986e1c64bff563f76b61` | **M5Stack mirror**, `m5stack-doc.oss-cn-shenzhen.aliyuncs.com/472/esp32-s3_datasheet_en.pdf` |
| `artifacts/esp32-s3-datasheet-v1.6-waveshare-mirror.pdf` | **v1.6** | **75** | 1 186 331 | `b79310e52e90599920fb067c9365263a18943c2efc4b9788edffc2b2d6cdefa1` | **Waveshare mirror**, `files.waveshare.com/wiki/common/Esp32-s3_datasheet_en.pdf` |
| `devices/seeed-studio/xiao-esp32s3-sense/artifacts/datasheets/esp32-s3-datasheet-seeed-copy.pdf` | **v1.6** | **75** | 1 186 462 | `8f3a10205e31799d11ae6629c7383cce896d59f3a009048b53fcfa1ca90708b9` | **Seeed copy** |

**Which revision each board vendor ships:**

| Board vendor | Revision served | Behind current (v2.2) by |
|---|---|---|
| **Espressif** | **v2.2**, 87 pp | — (this is current) |
| **M5Stack** ([PaperMono](../../../devices/m5stack/papermono/README.md)) | **v2.0**, 84 pp | one minor revision |
| **Waveshare** ([Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md)) | **v1.6**, 75 pp | six revisions, twelve pages |
| **Seeed Studio** ([XIAO ESP32S3 Sense](../../../devices/seeed-studio/xiao-esp32s3-sense/README.md)) | **v1.6**, 75 pp | six revisions, twelve pages |

Two observations that only become visible once all four are held together:

1. **Waveshare and Seeed both serve revision 1.6 — and their files are not the same bytes.**
   1 186 331 vs 1 186 462 bytes, 131 bytes apart, different hashes, same 75 pages and the same
   cover version string. These are **two separate exports of the same revision**, not two
   different revisions and not one file mirrored twice. Deduplicating them by "they're both
   v1.6" would have destroyed the evidence that two vendors independently re-exported the
   document. Deduplicating them by hash would keep both, correctly.
2. **M5Stack is the closest to current of the three board vendors**, at one minor revision
   behind rather than six. The 84→87 page growth between v2.0 and v2.2 is not cosmetic.

**The operational rule this supports:** *hash mirrors, do not assume them.* A file's revision
string, its page count and its byte size are three independent facts and all three can agree
while the bytes differ. Nobody could have told these four apart without hashing them, and the
first three were collected by three different agents on three different device tasks, each of
whom believed they were fetching "the ESP32-S3 datasheet".

**Which one to read.** For what the silicon does, use **v2.2** — it is current and
authoritative. Use a vendor's mirrored revision when you are trying to understand *that
vendor's* design or firmware, because it is what they had in front of them.

`esp-iot-solution` is included because it is the official home of the ESP-IDF component drivers this board depends on — QSPI LCD panel drivers, touch controllers, knob/encoder input and LVGL porting — none of which are documented in the core ESP-IDF programming guide. The v5.2.5 programming guide is retained alongside v5.1.4 because it is the newest ESP-IDF release for which Espressif publishes a PDF build at all; see the vendor guide for the details of that cutoff.

## Documentation sourcing

Espressif's documentation hosts, URL templates, migrated document classes and validation procedure are documented once, reusably, in the [Espressif vendor guide](../../../vendors/espressif/README.md). Read it before attempting to acquire further Espressif documents.

Note on source URLs: the `www.espressif.com/sites/default/files/documentation/*.pdf` paths now HTTP-redirect to Espressif's new documentation platform. The datasheet and TRM still resolve to real PDFs through that redirect; the errata and hardware design guidelines have been migrated into the versioned `esp-docs` projects, whose PDF build URLs are given above. `esp-dsp`, which would otherwise be the natural reference for the S3's PIE/SIMD kernels, publishes **no PDF build** — only an HTML site and its GitHub repository. Module datasheets (ESP32-S3-WROOM-1/-2, ESP32-S3-MINI-1) are deliberately **not** stored here: this board mounts a bare ESP32-S3R8, not a module, so module documentation would not describe the part fitted.
