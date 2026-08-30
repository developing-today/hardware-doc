# Waveshare ESP32-S3-Knob-Touch-LCD-1.8

> Product ID **31623**. Research retrieved **2026-08-21**. Canonical path: `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/`; also visible through ``.

## Identity and variants

Waveshare's round CNC-metal knob/display development device combines two independent wireless MCUs, a 1.8-inch 360 x 360 capacitive-touch LCD, dual directional knob inputs, removable storage, microphone, stereo DAC output and haptics. Product options are black or blue and with or without an optional 3.7 V 102035 LiPo. The wiki's -
  EN suffix describes the referenced product variant/documentation, not a demonstrated PCB hardware revision. No PCB revision, BOM or serial-number scheme is published.

## Key specifications

| Area | Specification | Evidence/caveat |
|---|---|---|
| Main MCU | [ESP32-S3R8](../../../components/espressif/esp32-s3r8/README.md), dual LX7 up to 240 MHz, Wi-Fi, BLE 5, 8 MB PSRAM | Schematic and product page |
| Secondary MCU | [ESP32-U4WDH](../../../components/espressif/esp32-u4wdh/README.md) `U14`, Xtensa LX6, Wi-Fi b/g/n, **Bluetooth Classic BR/EDR** + BLE 4.2, 4 MB embedded flash, no PSRAM | Schematic; **the only source of Classic Bluetooth on the board**. Core count and clock are genuinely uncertain — see the [core-count caveat](../../../components/espressif/esp32-u4wdh/README.md#2--the-core-count-and-clock-speed-caveat-unresolved) |
| Main storage | [W25Q128JVPIQ](../../../components/winbond/w25q128jv/README.md) 128 Mbit / 16 MB external flash | S3 flash; separate from U4WDH's 4 MB |
| Display | [1.8-inch round 360 x 360 panel](../../../components/generic/lcd-panel-module/README.md), marketed [ST77916](../../../components/sitronix/st77916/README.md); code uses [SH8601 compatibility driver](../../../components/generic/sh8601-compatibility-driver/README.md) | Controller naming conflict unresolved |
| Touch | [CST816D/CST816 family](../../../components/hynitron/cst816d/README.md), I2C address 0x15, interrupt/reset | Single-point controller family |
| Audio input | [MSM261D4030H1CPM PDM microphone](../../../components/memsensing/msm261d4030h1cpm/README.md) | S3 PDM input |
| Audio output | [PCM5100A stereo DAC](../../../components/texas-instruments/pcm5100a/README.md) through [CH445P](../../../components/wch/ch445p/README.md) to [3.5 mm line output](../../../components/generic/3.5mm-audio-output/README.md) | No onboard speaker or amplifier. **Shared between both MCUs**: S3 GPIO0 selects the mux, ESP32-U4WDH GPIO32 owns the mute |
| Haptic | [DRV2605L](../../../components/texas-instruments/drv2605l/README.md) at I2C 0x5A and [unknown LRA](../../../components/generic/lra-motor/README.md) | Product shorthand omits L suffix |
| Controls | Two [SSCM110100 directional switches](../../../components/alps-alpine/sscm110100/README.md) used as dual knob inputs — `SW2`/EC1 on the **S3**, `SW1`/EC2 on the **[ESP32-U4WDH](../../../components/espressif/esp32-u4wdh/README.md)**; [power button](../../../components/generic/power-button/README.md) and [ESP32-S3 BOOT button](../../../components/generic/esp32-s3-boot-button/README.md) | Knob parts are not conventional encoders; each knob is readable only by its own MCU; button wiring is not established |
| Storage | [microSD/TF, 4-bit SDMMC](../../../components/generic/micro-sd-sdmmc/README.md) | FAT/FatFs examples |
| Power | 5 V USB input; [TLV62569DBVT](../../../components/texas-instruments/tlv62569dbvt/README.md) main 3.3 V buck; [SGM2036-3.3](../../../components/sgmicro/sgm2036-3.3/README.md) DAC LDO; [charger/power-path unknown](../../../components/generic/charger-power-path/README.md) | Optional [3.7 V 102035 LiPo](../../../components/generic/lipo-102035/README.md) |
| RF | Two [unidentified ceramic antennas](../../../components/generic/ceramic-antenna/README.md) | One per MCU |
| USB | [USB-C orientation-select interface](../../../components/generic/usb-c-interface/README.md) and [unknown USB-UART bridge](../../../components/wch/ch340x/README.md) `U10` | **Plug orientation selects which MCU you talk to**: S3 native USB one way, ESP32-U4WDH via `U10` the other |
| Expansion | Two [PH1.27 10-pin headers](../../../components/generic/ph1.27-expansion-connectors/README.md) | Exact pinout absent |
| Dimensions | 66.00 mm diameter x 22.00 mm height | Official dimension image |
| Enclosure | CNC-machined metal, black or blue | Product page |

Other fitted functional circuitry includes the [AO3400A backlight MOSFET](../../../components/alpha-and-omega-semiconductor/ao3400a/README.md). Passive matching, filtering, pull-up and decoupling parts are intentionally not separate records.

## Dual-MCU architecture

> **📄 Full treatment: [Dual-MCU architecture — how the two MCUs work together](dual-mcu-architecture.md).** The USB-C orientation flip with Waveshare's verbatim instructions, the inter-MCU UART's full-duplex/no-flow-control consequences and bandwidth arithmetic, the reconstructed protocol with its explicit unknowns, which shipped apps actually use the link (the Bluetooth player does; AIDA64, MJPEG and the clock do not), the definitive ownership table, the OTA answer (**S3 yes, U4WDH no**), and what to back up before overwriting anything. **The section below is only the summary.**

**This board has two completely independent wireless MCUs on it.** Not a main chip plus a helper coprocessor — two full ESP32-family SoCs, each with its own crystal, its own antenna, its own flash, its own reset circuit and its own separately-flashed firmware image. Nearly every confusing thing about this product follows from that fact, so it is worth understanding before anything else.

### Why two chips?

**The ESP32-S3 has no Bluetooth Classic (BR/EDR) radio.** It is BLE 5 only, and that is a silicon-level omission — no ESP-IDF version, Arduino core or library can add it. But Bluetooth *audio* in the ordinary sense (A2DP music streaming, AVRCP transport control and track metadata, HFP hands-free, SPP serial, Classic HID media keys) is entirely a BR/EDR profile stack.

So a board that wants to be a Bluetooth media-control knob and a Bluetooth audio receiver simply cannot do it from an ESP32-S3. Waveshare's answer was to solder an original **[ESP32-U4WDH](../../../components/espressif/esp32-u4wdh/README.md)** (reference designator `U14`) next to the S3, give it the Bluetooth Classic and audio job, and connect the two chips with a private two-wire UART.

If you take nothing else from this page: **Classic Bluetooth on this board comes from the secondary MCU, and reaching it means flashing a second, separate firmware image over a differently-oriented USB-C connection.** See the [Classic Bluetooth guide](classic-bluetooth.md).

### Who owns what

| Resource | ESP32-S3R8 (`U2`) | ESP32-U4WDH (`U14`) |
|---|:--:|:--:|
| 1.8" 360x360 QSPI LCD + backlight | yes | — |
| CST816D capacitive touch | yes | — |
| DRV2605L haptics + LRA | yes | — |
| microSD (4-bit SDMMC) | yes | — |
| PDM microphone | yes | — |
| 16 MB external flash (W25Q128) | yes | — |
| 8 MB PSRAM | yes | — |
| **Knob 1** (`SW2`, GPIO8/7) | yes | — |
| **Knob 2** (`SW1`, GPIO19/22) | — | yes |
| Battery ADC divider | yes | — |
| Wi-Fi 802.11 b/g/n | yes (used) | yes (present, unused by factory firmware) |
| Bluetooth LE | yes, BLE 5 | yes, BLE 4.2 |
| **Bluetooth Classic (BR/EDR)** | **no — not possible** | **yes — only source on the board** |
| Native USB device | yes (GPIO19/20) | no — needs bridge `U10` |
| I2S to PCM5100A DAC | yes, via CH445P `S2` bank | yes, via CH445P `S1` bank |
| **CH445P mux select** (`I2S_SWITCH_IN`) | **yes — GPIO0** | — |
| **PCM5100A mute** (`XSMT`) | — | **yes — GPIO32** |
| Own crystal / own antenna | `X1` 40 MHz / `ANT1` | `X2` 40 MHz / `ANT2` |
| Own flash | 16 MB external | 4 MB embedded in package |
| Own firmware image | `WX-ESP32S3-KNOB_V1.2.bin` | `ESP32-KNOB_ESP32_0.bin` |
| Silicon revision | ESP32-S3 (see its own docs) | **v3.1** — see below |

Full pin-by-pin detail for both chips is in [pinouts and buses](pinouts-and-buses.md).

### The secondary MCU is silicon revision v3.1

**This board's ESP32-U4WDH (`U14`) reports chip revision `v3.1` — the current and best-case revision for this part.** ESP32-U4WDH has never been produced below v3.0, and Espressif moved the entire v3.0 range to v3.1 with **PCN20220901**, effective 2022-12-25.

**What v3.1 means practically:**

- **v3.1 is a *minor* revision of v3.0 and is functionally identical to it.** The change was a wafer-level tweak for high-temperature stability, plus a new eFuse minor code and a new marking letter. Espressif's PCN records "Quality & Performance: No impact" and "Customers can still use the current version [of ESP-IDF] for the changed products". Every erratum affecting v3.0 affects v3.1 identically; every v3.0 fix is present. Nothing new is unlocked by v3.1 over v3.0.
- **You get the full v3.x ("ECO3") feature set:** Secure Boot V2 (RSA), fault-injection-hardened flash encryption, the permanent `UART_DOWNLOAD_DIS` eFuse, the PSRAM cache-bug fix (no `SPIRAM_CACHE_WORKAROUND` needed), no spurious power-up watchdog resets, and TWAI down to 12.5 kbit/s.
- **Two things to keep in mind.** `WDT-3.15`, a dual-core cache live-lock, affects **v3.0/v3.1 and no earlier revision**, with no silicon fix — leave `CONFIG_ESP32_ECO3_CACHE_LOCK_FIX` and the interrupt watchdog enabled. And advisory **AR2022-003** documents side-channel extraction of the AES and flash-encryption keys on v3.x with no hardware fix, so use per-device unique keys if you enable secure boot or flash encryption.
- **Nothing in your toolchain needs changing.** ESP-IDF v5.x and Arduino-ESP32 3.x — which both factory images are built with — recognise v3.1 natively. Older tooling boots and runs it correctly but may *print* it as `revision 3`; that is a display limitation, not a fault. There is no "chip revision too new" failure mode for this part.

**How to verify it on your own board** — plug the USB-C in the orientation that selects the ESP32, or you will be talking to the S3 (see [the orientation quirk](#the-usb-c-orientation-quirk)):

```bash
esptool.py --port /dev/ttyACM0 chip_id
# Chip is ESP32-U4WDH (revision v3.1)
#   ^ needs esptool >= 4.3; v4.2.1 and older print "(revision 3)"
```

Or read it from the boot banner with `idf.py -p /dev/ttyACM0 monitor` — look for `I (29) boot: chip revision: v3.1`. From code, `efuse_hal_chip_revision()` returns **`301`** (`major * 100 + minor`). In eFuses, v3.1 is the v3.0 bit pattern plus `EFUSE_BLK0_RDATA5[24] = 1`. On the bare package, the tracking-information line reads `xGxxxxxx`, where v3.0 read `xExxxxxx`.

**Full treatment** — the complete v0.0 → v3.1 matrix, the ECO-versus-`vM.X` naming history, the per-revision errata table, all five identification methods with exact commands, and the tooling-version compatibility table — is in **[§21 of the ESP32-U4WDH component page](../../../components/espressif/esp32-u4wdh/README.md#21-silicon-revisions-the-complete-matrix-and-what-v31-means)**.

### The inter-MCU UART bridge

Two cross-connected wires, 3.3 V CMOS, no flow control, no reset or interrupt line — this is the **only** channel between the two chips:

| Direction | From | To |
|---|---|---|
| S3 → ESP32 | S3 `GPIO38` (`ESP32S3_TX`) | ESP32 `GPIO18` |
| ESP32 → S3 | ESP32 `GPIO23` (`ESP32S3_RX`) | S3 `GPIO48` |

Both sides use **UART1** (UART0 is each chip's own console). The factory firmwares use the link to carry AVRCP **track metadata** and multi-packet **JPEG album cover art** from the ESP32 to the S3 for display, plus status and control frames back the other way (including "clear the A2DP pairing").

**The wire format is undocumented.** Waveshare publishes no protocol description, and **no example in the official demo archive touches this link** — verified by searching the whole tree. What is known about the framing has been reconstructed from log strings compiled into both factory binaries and is set out, with its evidence, in [section 6 of the ESP32-U4WDH component page](../../../components/espressif/esp32-u4wdh/README.md#6-the-inter-mcu-uart-link). Do not build against a guessed frame layout; either sniff the line with a logic analyser or — far easier — reflash both MCUs and define your own protocol.

### The USB-C orientation quirk

There is **one** USB-C receptacle but **two** USB endpoints behind it:

- the **S3's native USB peripheral** (`USB_DP`/`USB_DN` on S3 GPIO20/GPIO19), and
- a **USB-UART bridge `U10`** which serves the ESP32-U4WDH's UART0.

**Which one you get depends on which way round you insert the Type-C plug.** Rotate the plug 180° to reach the other MCU. This is real, documented product behaviour and it is by far the most common cause of "no serial port appeared" and "esptool says the wrong chip".

The bridge gives the ESP32 automatic download mode: `U10` `RTS#` drives `ESP32_EN` and `U10` `TNOW/DTR#` drives `ESP32_IO0`, directly rather than through the usual two-transistor network. A side effect is that terminal programs which assert DTR/RTS on open can reset the ESP32 or drop it into the bootloader unexpectedly.

**Evidence boundary:** the five published schematic sheets contain **no USB Type-C receptacle symbol at all**. Both differential pairs appear only on the 10-pin connector `CN1` (`PM127-2-05-S-4.3`). The actual orientation-selection topology is therefore *not* established — see [gaps and conflicts](gaps-and-conflicts.md) and the [USB-C interface record](../../../components/generic/usb-c-interface/README.md).

### Shared audio output, and why it needs arbitration

Both MCUs want the one [PCM5100A](../../../components/texas-instruments/pcm5100a/README.md) DAC. A [CH445P](../../../components/wch/ch445p/README.md) four-channel 2:1 analog switch (`U18`) selects whose I2S reaches it — but the control is split awkwardly across the two chips:

- **The S3 owns the mux select.** `I2S_SWITCH_IN` (CH445P pin 15) is **S3 GPIO0**. The ESP32 cannot select itself onto the DAC.
- **The ESP32 owns the mute.** The PCM5100A's `XSMT` soft-mute input is driven by **ESP32 GPIO32** and by nothing else — it is not routed through the mux and no S3 pin touches it. The S3 cannot un-mute the DAC.

Neither chip can make a sound without the other's cooperation, so **any source handover has to be negotiated over the inter-MCU UART**. There is also **no MCLK** to the DAC (CH445P channel D is unconnected), so the PCM5100A must run in its BCK-derived clocking mode.

Two live caveats: the CH445P truth table is unverified (no datasheet obtained), so *which* logic level selects *which* bank is unknown; and S3 GPIO0 is also the S3's BOOT strapping pin with an external 10 k pull-up, so the mux sits in an unverified default state from reset. Both are tracked in [gaps and conflicts](gaps-and-conflicts.md), along with the open question of how the S3-only `07_Audio_Test` example manages to get past a mute line it cannot drive.

### Two firmware images, two flashing operations

There is no single "flash the board" step. Each MCU has its own merged image written at offset `0x0` through its own USB path:

| Target | Image | Project | Built | IDF |
|---|---|---|---|---|
| ESP32-S3R8 | `WX-ESP32S3-KNOB_V1.2.bin` (2,138,224 B) | — | 2025-02-28 | v5.1.4-972 + Arduino 3.0.7 |
| ESP32-U4WDH | `ESP32-KNOB_ESP32_0.bin` (1,130,672 B) | `TAIJI_KNOB_32` | 2025-04-18 | v5.4-727-g5cbd2a3877 |

Flashing one does **not** touch the other, and a board with mismatched firmware halves will behave oddly rather than fail cleanly — for instance, audio may go silent because the mute line's owner no longer un-mutes it. Procedures, hashes and safety notes are in [factory firmware and restore](factory-firmware.md); toolchain setup for both targets is in [development](development.md).

### Where to read more

- [Dual-MCU architecture](dual-mcu-architecture.md) — **the full device-level treatment of how the two chips work together**: orientation flip, link bandwidth and protocol, who owns what, OTA, backup and restore guidance
- [ESP32-U4WDH component page](../../../components/espressif/esp32-u4wdh/README.md) — the thorough treatment of the secondary MCU: full 48-pin table, the single-core/dual-core caveat, flashing, Bluetooth APIs, firmware analysis
- [Classic Bluetooth guide](classic-bluetooth.md) — what Classic BT can and cannot do on this board and how to build it
- [Pinouts and buses](pinouts-and-buses.md) — both GPIO maps side by side

## Documentation map

> **New 2026-08-26:** [`esphome-and-clone-confirmation.md`](./esphome-and-clone-confirmation.md) — ESPHome ships a working config for the Guition JC3636K518C, and **all eight of its pin assignments match this board**, evidencing a shared design. Also a third firmware path beyond ESP-IDF and Arduino.

**Hardware and architecture**

- [**Dual-MCU architecture: how the two MCUs work together**](dual-mcu-architecture.md) — USB-C orientation flip, the inter-MCU UART (bandwidth, protocol, unknowns), ownership table, OTA capability, backup/restore guidance
- [Exact pinouts, buses and addressing](pinouts-and-buses.md)
- [Classic Bluetooth: capabilities, limits and how to build it](classic-bluetooth.md) — **requires the secondary MCU; not available from the ESP32-S3**

**Using and developing on the board**

- [**⭐ Getting started: actually developing on this board**](getting-started.md) — **start here if you want to compile and flash your own code.** Which MCU the USB-C flip selects, Arduino and ESP-IDF setup with exact versions and board settings, the eight vendor examples, how to back up the factory firmware before you overwrite it, and the pitfalls that cost people days
- [**The factory "comprehensive example" apps**](factory-demo-apps.md) — the nine preinstalled apps the wiki documents plus **an undocumented tenth (weather)**: what each does, how to drive it with knob and touch, which MCU runs it, TF-card layout, AIDA64 and MJPEG setup
- [Dependency restore script](tools/README.md) — `restore-demo-deps.sh` rebuilds the LVGL 8.4.0 and SensorLib 0.3.1 trees that were removed from the demo archive, verified byte-for-byte
- [Development setup and official examples](development.md) — **now including the vendor-specified toolchain versions, audited and reconciled**
- [**FAQ and troubleshooting**](faq-and-troubleshooting.md) — all eleven vendor FAQ entries with attribution, including Waveshare's own statement of the USB-C orientation behaviour, plus the problems the vendor FAQ omits
- [Factory firmware and restore procedure](factory-firmware.md)

**Sources and third-party work**

- [**Wiki resource links**](wiki-resource-links.md) — complete URL inventory of wiki §8, including 8.6 Software Tools, 8.7 Other Resource Links and 8.8 Project Resources, with retrieval failures and reacquisition commands
- [**Community project catalogue**](examples/catalog.md) — 28 third-party projects assessed with pinned commits and licences ([`catalog.json`](examples/catalog.json); permissively-licensed sources retained in [`examples/selected/`](examples/))
- [Conflicts, limitations and unresolved gaps](gaps-and-conflicts.md)
- [Complete source table](sources.md)
- [Waveshare documentation-sourcing guide](../../../vendors/waveshare/README.md) — reusable URL patterns, API quirks and gotchas for any Waveshare product
- [Artifact manifest](../../../artifact-manifest.md)
- [Community links and snapshot metadata](community.md) — earlier, narrower pass; superseded by the catalogue above
- [All hardware components](../../../components/README.md)

## Artifact layout

- `artifacts/originals/`: the official dimension image, plus the acquisition and archival records for the three vendor ZIPs. **The ZIPs themselves are archived outside the repository** — see [`artifacts/originals/ARCHIVED-ORIGINAL-ZIPS.md`](artifacts/originals/ARCHIVED-ORIGINAL-ZIPS.md) for hashes, verified URLs and exact reacquire commands
- `artifacts/schematic/`: five official schematic PNGs extracted from the ZIP
- `artifacts/demo/`: the complete official Arduino/ESP-IDF **source** archive and both factory firmware images. The two bundled third-party libraries (LVGL 8.4.0, SensorLib 0.3.1) are **not** committed — restore them with [`tools/restore-demo-deps.sh`](tools/README.md)
- `tools/`: developer scripts meant to be run (as opposed to `artifacts/tools/`, which holds vendor utilities kept for the record)
- `artifacts/source-snapshots/`: product/wiki HTML, wiki snapshot pinned at revision **111069** (rendered HTML + raw wikitext), revision history, imageinfo metadata and community repository metadata
- `artifacts/datasheets/`: seven IC datasheets/reference manuals as mirrored by Waveshare on `files.waveshare.com/wiki/common/` (retained to document what Waveshare ships; manufacturer originals live under `components/`)
- `artifacts/tools/`: **five** PC-side tools referenced by the wiki (SSCOM, CH34x macOS driver, AIDA64 remote assets, MJPEG converter, and **Espressif Flash Download Tool 3.9.11** added 2026-08-23)
- `artifacts/images/`: 85 images — board photos, pinout, dimension and block diagrams from the wiki, shared tutorial figures, and storefront gallery photos. Provenance in [`artifacts/images/MANIFEST.md`](artifacts/images/MANIFEST.md). **Rights are Waveshare's; redistribution unclear**
- `examples/selected/`: **five community project tarballs** pinned to specific commits, retained only where licensing permits — see [`examples/catalog.md` §4](examples/catalog.md)

No community source is retained without a permissive licence; two of the five retained projects declare MIT in prose only and are flagged as such.

**On the original ZIPs (updated 2026-08-24).** All three vendor ZIPs have been moved to `../hardware-doc-archive/`, each only after (a) a full member-by-member reconciliation against what remains here, and (b) two independent, hash-verified download URLs. The Demo ZIP was the last and most carefully handled: its extraction is *not* complete here — two library trees were removed — so it was archived only once [`tools/restore-demo-deps.sh`](tools/README.md) was verified to reproduce those trees byte-for-byte from upstream. Full records, including what is and is not still on disk, in [`artifacts/originals/ARCHIVED-ORIGINAL-ZIPS.md`](artifacts/originals/ARCHIVED-ORIGINAL-ZIPS.md). See the root [artifact manifest](../../../artifact-manifest.md) for quantified duplicate storage.
