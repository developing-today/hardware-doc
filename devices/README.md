# Hardware devices

Each device record links to **every component it contains**; each [component record](../components/README.md) links back to the devices that use it, and to its [vendor sourcing guide](../vendors/README.md).

## Seeed Studio

- [Seeed Studio XIAO ESP32S3 Sense](seeed-studio/xiao-esp32s3-sense/README.md), SKU 113991115, retrieved 2026-08-24 — vendor guide: [Seeed Studio](../vendors/seeed-studio/README.md)

A 17.78 x 21.14 mm ESP32-S3R8 board with a detachable camera / PDM microphone / microSD daughterboard on a 30-pin Hirose board-to-board connector. Notable because Seeed publishes **KiCad sources under CC BY-SA 4.0**, which allowed the otherwise-undocumented [board-to-board connector pinout](seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md#2-the-j3-board-to-board-connector-sense-daughterboard-interface) to be reconstructed from the PCB netlist.

Three findings from that pass are worth knowing before buying one: the **user LED and the microSD chip-select are the same pin**; the **daughterboard consumes all four JTAG pins**, so hardware debugging is impossible with it attached; and the shipped **factory firmware contains hardcoded Wi-Fi credentials** and cannot connect to your network.

## Waveshare

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](waveshare/esp32-s3-knob-touch-lcd-1.8/README.md), product ID 31623, retrieved 2026-08-21 — vendor guide: [Waveshare](../vendors/waveshare/README.md)
- [Waveshare ESP32-S3-ePaper-3.97](waveshare/esp32-s3-epaper-3.97/README.md), SKUs **33552 / 33810 / 33811**, **USD 34.99–47.99**, retrieved 2026-09-01 — the knowledge base's first Waveshare **e-paper** board (all others are LCD). Same SoC, memory, 3.97" 4-grey panel **and SSD1677 controller** as the [M5Stack PaperMono](m5stack/papermono/README.md); active area matches to 0.01 mm and DPI exactly. **It has no expansion header** — which refutes the "prefer a Waveshare board *with expansion*" advice it was written to support. Schematic, panel manual and vendor source retained; [pinouts](waveshare/esp32-s3-epaper-3.97/pinouts-and-buses.md) · [conflicts](waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md)

**Waveshare's other ESP32 e-paper boards** — surveyed 2026-09-01, stub records, not researched in depth. Recorded so the population is known:

| Board | Price, 2026-09-01 | Why it is here |
|---|---|---|
| [e-Paper ESP32 Driver Board](waveshare/e-paper-esp32-driver-board/README.md) | USD 14.99 | Original ESP32; drives **23 documented raw panels** over a 24-pin FPC. The oldest and most widely deployed of the family |
| [ESP32-S3-ePaper-1.54](waveshare/esp32-s3-epaper-1.54/README.md) | USD 15.99–22.99 | 1.54" 200 × 200. **Has the 2 × 6 2.54 mm expansion header the 3.97" lacks** — 40 000 pixels instead of 384 000 |
| [ESP32-C6-ePaper-1.54](waveshare/esp32-c6-epaper-1.54/README.md) | USD 16.99–17.99 | Same, on **ESP32-C6 — Wi-Fi 6, Zigbee/Thread**, plus a TCA9554 I/O expander |
| [ESP32-S3-PhotoPainter](waveshare/esp32-s3-photopainter/README.md) | USD 82.99–83.99 | 7.3" Spectra 6 in a wood frame. **An appliance, not a development board** — and the `PhotoPainter` name covers four products, only one of which is ESP32 |

A sibling of this board, the **Guition JC3636K518**, is documented — as far as the evidence allows — in [clones-and-variants.md §5](../guides/markets/clones-and-variants.md#5-worked-example--waveshare-knob-board-and-guition-jc3636k518). It is not a separate device record here because we have not handled one.

### ESP32-P4 round-display boards

Retrieved 2026-08-24. Two variants of **one PCB**, differing only in the fitted round MIPI-DSI panel. Both use the [ESP32-P4](../components/espressif/esp32-p4/README.md) with an ESP32-C6-MINI-1 companion radio over SDIO — the same no-radio-on-the-P4 pattern as Espressif's own boards below.

| Board | Panel | Status | Notes |
|---|---|---|---|
| [ESP32-P4-WIFI6-Touch-LCD-3.4C](waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) | 3.4″ **800 × 800** | on sale, SKU **31523** | Crisper (~333 ppi) |
| [ESP32-P4-WIFI6-Touch-LCD-4C](waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md) | 4″ **720 × 720** | on sale, SKU **31522** | Larger but coarser (~255 ppi) |
| [Shared XC platform record](waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md) | — | — | Schematic, demo archive, pin map, architecture |

`XC` is Waveshare's own family wildcard: both wikis link the **same** schematic and demo archive under an `ESP32-P4-WIFI6-Touch-LCD-XC` path, so those artifacts are stored once. The variants differ in exactly three things — resolution constants, the physical panel, and a single byte in the JD9365 init sequence.

Both are sold under **one listing** at $64.99–$74.99 via a *Version Options* selector — the URL says `3.4c` but serves both. Waveshare maintain an official Apache-2.0 repository, a published BSP component (`waveshare/esp32_p4_wifi6_touch_lcd_xc` 3.0.1) and factory firmware for both: see [official repo and community](waveshare/esp32-p4-wifi6-touch-lcd-3.4c/official-repo-and-community.md).

## Espressif — official ESP32-P4 development boards

Retrieved 2026-08-21. All five are built on the [ESP32-P4](../components/espressif/esp32-p4/README.md), which has **no radio**; each carries a companion Wi-Fi/Bluetooth module. The `P4X` prefix denotes a board fitted with ESP32-P4 chip revision **v3.1 or later** — it is **not** a different chip.

| Board | Status | Companion radio | Distinguishing feature | Sources |
|---|---|---|---|---|
| [ESP32-P4X-Function-EV-Board](espressif/esp32-p4x-function-ev-board/README.md) | current | ESP32-C6-MINI-1 (2.4 GHz Wi-Fi 6) | Flagship multimedia board: 7″ 1024×600 MIPI-DSI touch panel, MIPI-CSI camera, Ethernet, audio, USB HS host + device | [manifest](espressif/esp32-p4x-function-ev-board/sources.md) |
| [ESP32-P4X-C5-Function-EV-Board](espressif/esp32-p4x-c5-function-ev-board/README.md) | current | **ESP32-C5-MINI-1 (2.4 + 5 GHz Wi-Fi 6)** | Same design with **dual-band** Wi-Fi; **the only P4 board whose main-board schematic, PCB layout and dimensions Espressif publishes** | [manifest](espressif/esp32-p4x-c5-function-ev-board/sources.md) |
| [ESP32-P4X-EYE](espressif/esp32-p4x-eye/README.md) | current | ESP32-C6-MINI-1U (external antenna) | Enclosed hand-held **camera**: 2 MP MIPI-CSI, 1.54″ SPI LCD, rotary encoder, battery, on-device YOLOv11-nano demo | [manifest](espressif/esp32-p4x-eye/sources.md) |
| [ESP32-P4-Function-EV-Board](espressif/esp32-p4-function-ev-board/README.md) | **EOL** | ESP32-C6-MINI-1 | Predecessor of the P4X board; **retains the published schematic / PCB / dimensions / assembly set** | [manifest](espressif/esp32-p4-function-ev-board/sources.md) |
| [ESP32-P4-EYE](espressif/esp32-p4-eye/README.md) | **EOL** | ESP32-C6-MINI-1U | Predecessor of the P4X-EYE; **retains the published schematic and PCB layout** | [manifest](espressif/esp32-p4-eye/sources.md) |

⚠ **Both EOL user guides moved between 2026-08-21 and 2026-08-28** — Espressif dropped the `eol/`
path segment, the originally-cited URLs now return HTTP 404, and neither has an Internet Archive
capture. Current URLs and the full finding are in
[the EOL board's manifest §4](espressif/esp32-p4-function-ev-board/sources.md#4-retrieval-findings).

There is **no ESP32-P4 Korvo board.** The Korvo line is an audio/HMI family built on the ESP32-S3 (`ESP32-S3-Korvo-2`, `ESP32-S3-Korvo-2-LCD`) and the newer S3.1 (`ESP32-S31-Korvo-1`). See [ESP32-P4 §1](../components/espressif/esp32-p4/README.md#1-identity-and-variants) and the board records above.

Documents Espressif publishes once and links from several of these boards are stored in [`espressif/shared-artifacts/`](espressif/shared-artifacts/README.md) rather than duplicated into each board.

The companion-radio arrangement these five boards share — and how it contrasts with the ESP32-S3 + ESP32-U4WDH retrofit on the Waveshare knob board — is mapped in [ecosystem-and-product-lines.md §6](../guides/espressif/ecosystem-and-product-lines.md#6-the-companion-radio-pattern-p4--c6c5).

## Soldered Electronics

Retrieved 2026-08-24. Osijek, Croatia — makers of the **Inkplate** e-paper series. Vendor guide: [Soldered Electronics](../vendors/soldered-electronics/README.md).

| Board | Panel | Hardware rev | Arduino target | Sources |
|---|---|---|---|---|
| [Inkplate 5](soldered-electronics/inkplate-5/README.md) | 5.2″ **960 × 540** | V1.2.0 | `Inkplate5` | [manifest](soldered-electronics/inkplate-5/sources.md) |
| [Inkplate 5 Gen 2](soldered-electronics/inkplate-5-gen2/README.md) | 5.2″ **1280 × 720** | V1.1.0 | `Inkplate5V2` | [manifest](soldered-electronics/inkplate-5-gen2/sources.md) |

Both generations share **one full technical record** — [`inkplate-5/README.md`](soldered-electronics/inkplate-5/README.md) — because they differ in **exactly one component**, the panel. Everything else (ESP32-WROVER, TPS65186 PMIC, PCAL6416A expander, PCF85063A RTC) is common. The Gen 2 keeps its own page because Soldered publish its hardware design in a **separate upstream repository**.

Worth knowing before integrating one: Soldered ship **CE and UKCA compliance documents and multilingual safety sheets inside the public hardware repository**, which is unusually thorough for an open-hardware vendor. Hardware is **TAPR OHL**; the Arduino library is **LGPL-3.0**.

## ZeroWriter

Open-source e-paper typewriters by Adam Wilk. Vendor guide: [Zerowriter](../vendors/zerowriter/README.md).

| Device | Status | Platform | Retrieved |
|---|---|---|---|
| [ZeroWriter Ink](zerowriter/zerowriter-ink/README.md) | shipping since Jan 2026; Crowd Supply, funded 2024-10-17, $285 | Respun [Inkplate 5 Gen 2](soldered-electronics/inkplate-5-gen2/README.md) + a second ESP32 for the keyboard | 2026-08-24 |
| [Zerowriter Fold](zerowriter/zerowriter-fold/README.md) | **unshipped** — Kickstarter live at snapshot, ~$239 First Wave / ~$329 retail, ships late 2026 | Claimed **in-house** hardware; 6″ **frontlit** e-ink, folding laptop-style case, hot-swap Choc keyboard | 2026-08-24 |

**ZeroWriter Ink** was built **in collaboration with Soldered Electronics**. The headline finding is that the device contains **two ESP32s** — an ESP32-WROVER on the display board and an ESP32-WROOM-32U-N4 on the keyboard PCB — which is stated nowhere in the campaign material and was recovered only from the project's own KiCad BOMs.

Its main board is a **respin of the [Inkplate 5 Gen 2](soldered-electronics/inkplate-5-gen2/README.md)**, not the stock product: 8 parts added, 14 removed, 20 values changed, including a swap from a linear to a switch-mode charger. Firmware written against the Inkplate Arduino library should run, but **power, charging, USB and SD paths differ** — see [the BOM comparison](zerowriter/zerowriter-ink/README.md).

Its Raspberry-Pi predecessor, **ZeroWriter 1**, silently patched two files in Waveshare's vendored e-paper driver library; both changes are analysed in [zerowriter1-epaper-driver-notes.md](zerowriter/zerowriter-ink/zerowriter1-epaper-driver-notes.md).

**Zerowriter Fold** is documented **from vendor marketing material only** — the Kickstarter campaign page bot-blocks every user agent tried and was never read. No design files, teardown, review or unit exists. Treat every figure as a vendor claim about an unshipped product; the record's [source manifest](zerowriter/zerowriter-fold/sources.md) states exactly what that evidence can and cannot support. The consequential claim is that the Fold uses **in-house hardware** rather than an Inkplate — if accurate, none of the Inkplate research transfers to it.

## M5Stack

Retrieved **2026-09-01**. Two SKUs of **one board**, launched together on 2026-08-21 and both out of stock nine minutes later.

| Board | SKU | Price | Distinguishing feature | Sources |
|---|---|---|---|---|
| [PaperMono](m5stack/papermono/README.md) | **C153** | USD 65.00 | Grey case, **NFC (ST25R3916) + LoRa (Stamp LoRa-1262)** | [sources](m5stack/papermono/sources.md) · [research log](m5stack/papermono/research-log.md) · [commands](m5stack/papermono/commands.md) |
| [PaperMono-Lite](m5stack/papermono-lite/README.md) | **C153-Lite** / `C153-LITE` | USD 55.00 | White case, **no NFC, no LoRa**; 72.4 g vs 74.7 g. Everything else identical, battery included | shares the PaperMono's manifests |

A 3.97″ 480 × 800 frontlit touch e-paper handheld on an ESP32-S3R8. Best understood as **a battery-first low-power platform that happens to have a display**, not an e-paper board that happens to have a battery: it has five hardware power states and can wake on RTC alarm, motion, touch or keys **with the application processor unpowered**. The full record: [`papermono/`](m5stack/papermono/README.md), with [pinouts and buses](m5stack/papermono/pinouts-and-buses.md), [power architecture](m5stack/papermono/power-architecture.md) and [gaps and conflicts](m5stack/papermono/gaps-and-conflicts.md).

Four things to know before buying or building for one:

- **There is no expansion connector at all** — no Grove, no M-Bus. Every GPIO is committed; the only way in is the shared I²C bus. This is unusual for an M5Stack core and is the single biggest constraint.
- **Two auxiliary microcontrollers sit between the application processor and most of the board.** Panel power and reset, touch power and reset, microSD power and detect, microphone power, NFC enable, LoRa reset, two of three LED colours and the charger's bus gate are all behind the **M5IOE1** expander; reset, boot mode, rail enables and every wake source are behind the **M5PM1** power manager. Neither is optional, and both are the *same* Puya PY32L020F15U6 die running different M5Stack firmware.
- **`PYG3` denotes two different pins**, one on each of those chips — the frontlight PWM and the e-paper rail enable. Getting it wrong silently kills the display. [The whole hazard, and how it was resolved from the schematic](m5stack/papermono/pin-naming-and-the-pyg-ambiguity.md).
- **Do not read PaperMono as a successor to the M5PaperS3.** Against the PaperS3 it has ~35 % fewer pixels, 4 grey levels instead of 16, a smaller battery and no expansion port, while adding a frontlight, NFC, LoRa and the power architecture. A repositioning, not an upgrade.

⚠ **Nothing in either record was verified on physical hardware.** Every behavioural claim is `inferred`, `reported-working` or read from vendor source. The board sold out within minutes of launch and had not restocked eleven days later, so no unit could be obtained — and for the same reason there were, at the snapshot date, **zero written reviews and one hands-on video** anywhere. The real independent evidence is four third-party GitHub projects, two with credible hardware validation.

M5Stack publishes a complete schematic and datasheets for both of its custom chips, which is better hardware disclosure than most comparable vendors — but **no C153 directory exists in `m5stack/M5_Hardware`**, so there is no machine-readable netlist and the pin map was recovered by parsing invisible Altium marker text out of the published PDF. Method and limitations: [`commands.md`](m5stack/papermono/commands.md#altium-pdf-tooling).

### DinMeter — *added 2026-09-04*

A 1/32-DIN panel instrument built on a Stamp module: orange rotary encoder, 1.14" display, buzzer and a **6–36 V DC input**, in a DIN 43700 cutout. M5Stack publishes a **byte-identical** schematic and STL for both revisions, so the v1.1 record is scoped to the module substitution that is the entire content of the revision.

| Device | SKU | Record | Notes |
|---|---|---|---|
| **DinMeter** | `K134` | [`m5stack/dinmeter`](m5stack/dinmeter/README.md) | 1/32-DIN panel instrument: orange rotary encoder, 1.14" ST7789V2 135×240, BM8563 RTC, buzzer, **6–36 V DC input**, Li-ion charger + latch, PORT.A/B. Stamp-S3 core module. **`[EOL]` at the vendor, 2026-09-04** |
| **DinMeter v1.1** | `K134-V11` | [`m5stack/dinmeter-v1.1`](m5stack/dinmeter-v1.1/README.md) | Same carrier with a **Stamp-S3A** module and an ST7789P3 display. Scoped revision record — M5Stack publishes a **byte-identical** schematic and STL for both. Includes [`stamp-s3-to-s3a-delta.md`](m5stack/dinmeter-v1.1/stamp-s3-to-s3a-delta.md), the full schematic-derived module delta |

### Cardputer family — *added 2026-09-04*

Card-sized computers with a 56-key QWERTY keyboard over a 1.14″ 240×135 display. Five records; the ADV is the full-depth one. Note that **the v1.0 and v1.1 share one published schematic file byte-for-byte** (SHA-256 `6016c1fe…`), so the revision is a module substitution — Stamp-S3 → Stamp-S3A — with an undocumented or unchanged mainboard, and the document alone cannot say which.

| Device | Manufacturer | SKU | SoC | Notes |
|---|---|---|---|---|
| [Cardputer ADV](m5stack/cardputer-adv/README.md) | M5Stack | `K132-Adv` | ESP32-S3FN8 | Card-sized computer, 56-key TCA8418 keyboard, ES8311 audio, BMI270, 14-pin CAP expansion header. **Full-depth record.** |
| [Cardputer v1.1](m5stack/cardputer-v1.1/README.md) | M5Stack | `K132-V11` | ESP32-S3FN8 | Stamp-S3A refresh of the original; 74HC138 keyboard. **`[EOL]` at 2026-09-04.** |
| [Cardputer v1.0](m5stack/cardputer-v1.0/README.md) | M5Stack | `K132` | ESP32-S3FN8 | The original; StampS3 module. Shares a published schematic file with v1.1. |
| [Cardputer Mesh Kit](m5stack/cardputer-mesh-kit/README.md) | M5Stack | `K152` | ESP32-S3FN8 | Cardputer ADV + Cap LoRa-1262 bundle; officially licensed Meshtastic device. |
| [CardputerZero](m5stack/cardputer-zero/README.md) | M5Stack | `C154` / `C155` | **Raspberry Pi CM0** | Linux handheld in the Cardputer form factor. Vendor marks it *work in progress*. |

⚠ **The Cardputer ADV and the CardputerZero are not comparable devices** despite sharing a name, a form factor, a keypad scanner and an expansion connector: one is a microcontroller, the other a Linux computer, and their EXT headers are **not pin-compatible** — the Zero's left column is USB/GPIO/SPI0 and its UART pair is reversed relative to the ADV's.

### Cardputer expansions — LoRa, sub-GHz and NFC — *added 2026-09-04*

Nine records covering M5Stack's radio expansions for the Cardputer line, from the Grove-attached E220 units of 2023 to the **Cap CC1101 & NFC** released 2026-08-28. Entry point: [`m5stack/cap-lora-1262/`](m5stack/cap-lora-1262/README.md); the two portability-focused guides are [`features/lora.md`](m5stack/cap-lora-1262/features/lora.md) and [`features/nfc.md`](m5stack/cap-cc1101/features/nfc.md), both written for someone adding these capabilities to *other* firmware.

| Device | Notes | Depth |
|---|---|---|
| [M5Stack Cap LoRa-1262 (U214)](m5stack/cap-lora-1262/README.md) | Cardputer-Adv expansion — SX1262 LoRa + ATGM336H-6N GNSS, 868–923 MHz, Meshtastic-supported upstream | full |
| [M5Stack Cap CC1101 & NFC (U219)](m5stack/cap-cc1101/README.md) | Cardputer-Adv expansion — CC1101 sub-GHz (315/433/868/915 MHz, dual SP3T switched) + ST25R3916 NFC over SPI | full |
| [M5Stack Cap LoRa868 (U201)](m5stack/cap-lora868/README.md) | The **first** Cardputer-Adv LoRa expansion, 2025-09-05, now EOL — predecessor of the Cap LoRa-1262 | medium |
| [M5Stack Cardputer Mesh Kit (K152)](m5stack/cardputer-mesh-kit/README.md) | Bundle: Cardputer-Adv + Cap LoRa-1262, pre-flashed Meshtastic, the only Meshtastic-registration-eligible configuration | medium |
| [M5Stack LoRa Unit (E220)](m5stack/unit-lora-e220/README.md) | Grove/UART LLCC68 modem — attaches to *any* Cardputer, but **not** a Meshtastic path | light |
| [M5Stack LoRaWAN Unit (STM32WLE5)](m5stack/unit-lorawan-stm32wle5/README.md) | Grove/UART LoRaWAN modem, **region per SKU**, RAK3172 module | light |
| [M5Stack Unit C6L (U202)](m5stack/unit-c6l/README.md) | Self-contained ESP32-C6 + SX1262 Meshtastic node on a Grove cable — the route for an **original** Cardputer | light |
| [M5Stack Stamp C6LoRa (S012)](m5stack/stamp-c6lora/README.md) | Solder-down ESP32-C6 + SX1262 SMD module — **not** a Cardputer expansion | light |

⚠ **Initialising the Cap LoRa-1262 requires one non-obvious step**: M5Stack states that the RF antenna switch must be enabled by setting **`P0` of the Cap's PI4IOE I/O expander HIGH**, over the host's *internal* I²C bus. Omit it and the radio transmits into a disconnected antenna.

## Xteink (阅星瞳 / 星瞳 "Star Pupil")

Shenzhen maker of low-cost pocket e-ink readers, and the hardware target of the
CrossPoint Reader / FreeInk firmware ecosystem. **Six products**, four of them
ESP32-based. See the [family index](xteink/README.md).

| Device | SoC | Panel | Price (2026-09-04) | Record |
|---|---|---|---|---|
| [X4 Pro](xteink/x4-pro/README.md) | ESP32-S3, 8 MB PSRAM | 4.26″ 800×480, GT911 touch, warm/cool frontlight | **$99** | deep |
| [X4](xteink/x4/README.md) | ESP32-C3 | 4.26″ 800×480 | **delisted** | deep |
| [X3](xteink/x3/README.md) | ESP32-C3 | 3.7″ 792×528, ~257 PPI, IMU + NFC | **$69** | deep |
| [X4 Classic](xteink/x4-classic/README.md) | ESP32-S3, 8 MB PSRAM | 4.26″ 800×480, 7 buttons, IMU | not listed | medium |
| [S4](xteink/s4/README.md) | **Android 11** | not established | ¥339 (China) | stub |
| [Nano / Tong Card 瞳卡](xteink/nano/README.md) | **none — passive NFC-powered** | four-colour e-paper card | not captured | stub |

**Note the naming trap:** the X4 Pro is *not* an enhanced X4. They share a screen
size and a brand; different SoC architecture, flash layout, input hardware and
charging connector. Firmware for one will not run on the other.

Three axes of variation are **invisible from outside** and none is externally marked: the **panel controller** (the X3 ships a UC8253 *or* a UC8279d; the X4 family an SSD1677 *or* UC8179 *or* UC8279 — firmware probes the display bus at boot, **except on the X4 Classic, which has no MISO and must trust an NVS byte the factory wrote once**); the **power latch** (at least one X4 revision does not self-latch); and the **USB-lock state**, which owners find **does not correlate with sales channel**.

### Round-two corrections — *2026-09-11*

⚠ **Two rows in the table above are now wrong, and one device is missing from it.** Per this
repository's append-only rule the stale rows are **left exactly as written**; the corrections are
here. The family index [`xteink/README.md`](xteink/README.md) carries the full corrected table.

**1. The X4 Classic launched on 2026-09-06, and it replaced the X4.**
The row above says *"not listed"*. It is listed, and the X4 row's price is the one that is now
historical:

| Device | Marketed as | Listed | Price | Status 2026-09-11 |
|---|---|---|---|---|
| [X4 Classic](xteink/x4-classic/README.md) | **"XTEINK X4 Classic (X4 V2)"** | **2026-09-06** | **USD 79** bare / 95 with base | on sale, in stock |
| [X4](xteink/x4/README.md) | — | — | last observed ~USD 69 | **withdrawn — the product record *and all four of its dedicated accessories* are gone from the catalogue** |

**The vendor's own store title asserts the succession**: the Classic *is* the second version of
the X4. The FCC record agrees — `2BTR9-XTEINKX4` granted 2026-01-05, then `2BTR9-X4C` granted
2026-07-20. On 2026-09-04 the X4's four accessories were still listed but sold out; a week later
the product records themselves had been removed. **That is a completed withdrawal, not a
stockout.**

**2. There is a sixth device, and the vendor has never mentioned it.**

| Device | SoC | Panel | Price | Record |
|---|---|---|---|---|
| [X4 Light](xteink/x4-light/README.md) | **unknown** | **unknown** | **never listed** | certification-only |

**FCC `2BTR9-X4L`, granted 2026-08-13.** No announcement, no store listing, no price, no review,
no community mention. It was found by **enumerating Xteink's FCC grantee code `2BTR9`**, not by
searching for a product name — a vendor's grantee index lists every device it has certified for
the US, including ones it has never announced. Its internal photographs unlock **2027-02-09**;
its external photographs are already public and held in the record. ⚠ **"Light" is a marketing
word and the filing does not define it** — do not infer a specification or a price slot from the
name.

That makes the table above **seven entries**, not six. Four are confirmed ESP32-based; the X4
Light's SoC is **unknown**, and the Nano is a passive NFC card rather than a reader.

**3. ⚠ The certification finding for this family is reversed.** Records in this tree stated that
no FCC or CE filing existed for any Xteink device. **Refuted.** Xteink holds **five granted
Original Equipment authorisations** under grantee code `2BTR9` — X3, X4, X4 Pro, X4 Classic and
X4 Light. The original finding confused *"no mark visible in a product photo"* with *"no grant"*.
Per-device detail and the positive/negative controls that make it evidence:
`xteink/<record>/certification-and-compliance.md`. Corrections are appended beneath every stale
claim and listed in
[`scratch/index-merge/corrections-requiring-review.md`](../scratch/index-merge/corrections-requiring-review.md).

One consequence worth surfacing at index level: the `2BTR9-XTEINKX4` filing's **Internal Photos
were never withheld**, which makes them the **first public teardown of the Xteink X4** —
[`xteink/x4/artifacts/certification/`](xteink/x4/artifacts/certification/README.md). The X3's are
public too; the X4 Pro's unlock **2026-12-12**. Schematics are withheld **permanently** on all
five filings, so the FCC is not a route to an Xteink schematic.

## LilyGO (Shenzhen Xin Yuan Electronic Technology; also trades as TTGO)

Vendor guide: [LilyGO / TTGO](../vendors/lilygo/README.md). The **T-Display-S3 family** is a *name*, not a platform: eleven boards, eight display
controllers and four different chargers ship under it. Start at the shared platform record.

| Device | Identity | Depth |
|---|---|---|
| [T-Display-S3 family — shared platform](lilygo/t-display-s3-shared/README.md) | family hub: enumeration evidence, shared artifacts, family-wide traps, [board-revision drift](lilygo/t-display-s3-shared/board-revision-drift.md) | — |
| [T-Display-S3](lilygo/t-display-s3/README.md) | ESP32-S3R8 + 1.9″ 170×320 ST7789V on an **8-bit Intel-8080 parallel** bus. USD 9.04 | **full** |
| [T-Display-S3 Touch](lilygo/t-display-s3-touch/README.md) | same PCB; panel swapped for one with a bonded CST816S → later CST328 | medium |
| [T-Display-S3 AMOLED](lilygo/t-display-s3-amoled/README.md) | 1.91″ 240×536 RM67162 on QSPI; **V1.0 and V2.0 sold concurrently** | full-ish |
| [T-Display-S3 AMOLED Plus](lilygo/t-display-s3-amoled-plus/README.md) | same panel, BQ25896 PMIC + PCF85063ATL RTC + microSD | medium |
| [T-Display-S3 AMOLED 1.64″](lilygo/t-display-s3-amoled-1-64/README.md) | 280×456 CO5300/ICNA3311 + FT3168 + SY6970 | medium |
| [T-Display-S3 AMOLED 1.43″/1.75″](lilygo/t-display-s3-amoled-1-43-1-75/README.md) | round 466×466; **two display and two touch controllers behind one product page** | medium |
| [T4-S3](lilygo/t4-s3/README.md) | the "2.41″ AMOLED": 450×600 RM690B0 + CST226SE. Sold as *T4-S3*, not T-Display-S3 | medium |
| [T-Display AMOLED Lite](lilygo/t-display-amoled-lite/README.md) | 1.47″ 194×368 SH8501B behind a **1.8 V level shifter**; AXP2101 PMU | medium |
| [T-Display-S3 Long](lilygo/t-display-s3-long/README.md) | 3.4″ 180×640 bar; **AXS15231B drives display *and* touch from one die** | full-ish |
| [T-Display-S3 Pro](lilygo/t-display-s3-pro/README.md) | 2.33″ 222×480 ST7796 on plain SPI, camera, microSD, 3 buttons, SY6970 | full-ish |
| [T-Display-S3 Pro MVSRBoard](lilygo/t-display-s3-pro-mvsrboard/README.md) | audio/RTC/haptic backplate for the Pro | stub |
| [T-Display (TTGO, ESP32)](lilygo/t-display-ttgo/README.md) | the ancestor. 1.14″ 135×240 SPI. **The only one WLED supports** | lineage stub |
| [T-QT](lilygo/t-qt/README.md) | thumbnail-sized 128×128 cousin | lineage stub |
| [T-Dongle-S3](lilygo/t-dongle-s3/README.md) | USB-A dongle, 0.96″ ST7735, on-board microSD | lineage stub |
| [T-Display K230 / Kit](lilygo/t-display-k230/README.md) | **the repository's first RISC-V device** — see below | full |

### T-Display K230 — *added 2026-09-04*

- [`lilygo/t-display-k230`](lilygo/t-display-k230/README.md) — **T-Display K230** (SKU `K256`/`-A`/`-B`/`-C`) and **T-Display K230 Kit** (`K256-03`, `K277`, `K256-04`, `K256-04-A`). A 4.1″ AMOLED handheld running **Linux on a 64-bit RISC-V** Kendryte K230, with LoRa, a 2 MP MIPI camera, USB Ethernet, a 40-pin header, and an optional QWERTY keyboard base carrying an nRF9151 LTE-M/GNSS modem. **The repository's first RISC-V device.**

⚠ **LilyGO stock codes collide with chip names.** `K230` is a LilyGO SKU for the transparent-case variant of the **T-Embed CC1101**, an ESP32-S3 board with no Kendryte silicon in it. The Kendryte K230 board's SKUs are `K256*` and `K277`. **Never infer silicon from a LilyGO SKU** — and see the [vendor guide](../vendors/lilygo/README.md) for why the wiki must be verified against the board's GitHub repository.

---

## Nicolai Electronics

- [Nicolai Electronics Tanmatsu](nicolai-electronics/tanmatsu/README.md), retrieved 2026-08-24, hardware repo commit `640805dd` — "the terminal for hackers": an **ESP32-P4** handheld with a QWERTY keyboard, LoRa, a MIPI-DSI display and a 36-pin expansion port, derived from the Dutch hacker-camp badge lineage ([Badge.team](https://badge.team), MCH2022 / WHY2025) but sold as a product.

Notable for **openness rather than volume**: the full KiCad design is published under **CERN-OHL-P** and the firmware under **MIT**, with a git-maintained Sphinx documentation site. The limiting factor on information is that the device is new and low-volume, and the detail is spread across ~10 repositories.

> *Indexed 2026-09-07.* This record was written in the 2026-08-24 pass but was never linked from this index — an orphan found by the cross-link audit at the end of the 2026-09-04/07 sweep. The entry above is a discoverability fix written from the record's own opening section; **the record itself was not reviewed or modified**, and it remains the authority on its own contents.

---

## Two new per-record file types — *added 2026-09-11*

Round two of the 2026-09-04 sweep added two kinds of page to device records across the tree.
Neither is listed per-device above; both are worth knowing exist.

| File | What it is | Where |
|---|---|---|
| `certification-and-compliance.md` | Regulatory grants by jurisdiction — FCC ID, grant date, frequencies, test firm, withheld exhibits and embargo dates — **each carrying the positive and negative controls that make an absence finding mean anything**. Method: [`guides/research/finding-certification-records.md`](../guides/research/finding-certification-records.md) | **32 records**: M5Stack, LilyGO and all five Xteink |
| `schematic-netlist.md` | A net list **recovered from the vendor's schematic PDF**, not from EDA sources — connector pinouts, per-net membership and the unrouted or mislabelled nets the trace exposed. Method: [`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md) | [`lilygo/t-display-s3-shared`](lilygo/t-display-s3-shared/schematic-netlist.md) · [`m5stack/cardputer-adv`](m5stack/cardputer-adv/schematic-netlist.md) · [`m5stack/dinmeter`](m5stack/dinmeter/schematic-netlist.md) · [`m5stack/cap-lora-1262`](m5stack/cap-lora-1262/schematic-netlist.md) · [`m5stack/cap-cc1101`](m5stack/cap-cc1101/schematic-netlist.md) |

Two of those boards also gained a `driver-vs-document-audit.md` — the vendor driver read
side-by-side against the schematic and the datasheet:
[`cardputer-adv`](m5stack/cardputer-adv/driver-vs-document-audit.md) (`M5Cardputer` @ `f1392858`)
and [`dinmeter`](m5stack/dinmeter/driver-vs-document-audit.md) (`M5DinMeter` @ `8ccbad7`).

**Why the tracing worked, and when it will not.** Altium exports embed invisible `CO` / `PI` /
`NL` marker tokens at item coordinates — component outlines, pins and net labels — so a net can
be reconstructed by geometry from the PDF text layer alone. **291 schematic PDFs in this
repository were assessed**; the per-file verdict is in
[`scratch/schematic-tracing/traceability-census.md`](../scratch/schematic-tracing/traceability-census.md).
Two traps that census found, both worth checking before concluding a design is undocumented:

- ⚠ **KiCad and EAGLE exports frequently outline their text to vector paths.** `pdftotext` then
  yields **zero words** and the file is permanently untraceable. For
  [`zerowriter/zerowriter-ink`](zerowriter/zerowriter-ink/README.md) and
  [`seeed-studio/xiao-esp32s3-sense`](seeed-studio/xiao-esp32s3-sense/README.md) **a second,
  usable export of the same design sits in the same directory** — prefer the `Eeschema` copies.
- ⚠ **Non-Altium exports carry no `CO`/`PI`/`NL` tokens**, so every binding must be geometric.
  That applies to the Espressif ESP32-P4 board schematics, which are otherwise traceable.

The richest untraced sheet in the repository is the **M5Stack PaperMono**'s
`PaperMono_SCH_V0.6.2` — 6 pages, 144 net-label tokens, fully traceable, and **not traced**,
because that record was owned by another session throughout both rounds.

---

## Related

- [Components](../components/README.md) — the parts these boards are built from
- [Vendor sourcing guides](../vendors/README.md) — [Espressif](../vendors/espressif/README.md) · [Waveshare](../vendors/waveshare/README.md)
- [Espressif ecosystem map](../guides/espressif/ecosystem-and-product-lines.md) · [Marketplace comparison](../guides/markets/vendor-comparison.md) · [Clones and variants](../guides/markets/clones-and-variants.md)
