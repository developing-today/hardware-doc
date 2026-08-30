# Espressif ESP32-P4X-Function-EV-Board

> Espressif's flagship ESP32-P4 multimedia evaluation board. Current production board; supersedes the end-of-life [ESP32-P4-Function-EV-Board](../esp32-p4-function-ev-board/README.md). Research retrieved **2026-08-21**.

- **Manufacturer:** Espressif Systems
- **Chip:** [ESP32-P4](../../../components/espressif/esp32-p4/README.md), silicon revision **v3.1 or later**
- **Companion radio:** ESP32-C6-MINI-1 module (2.4 GHz Wi-Fi 6 + Bluetooth 5 LE + 802.15.4)
- **Documentation project:** `esp-dev-kits`, target `esp32p4`, slug `esp32-p4x-function-ev-board`
- **Status:** current

---

## 1. Identity and variants

| Field | Value |
|---|---|
| Marketed name | ESP32-P4X-Function-EV-Board |
| Also listed as | `ESP32-P4X-Function-EV-Board-L2` on Espressif's DevKits store listing — an ordering SKU, not a separate design (see caveat below) |
| Predecessor | ESP32-P4-Function-EV-Board (**EOL**), board versions v1.4 and v1.52 |
| Difference from predecessor | **Only the silicon revision.** Espressif: *"The difference between the ESP32-P4X-Function-EV-Board and the ESP32-P4-Function-EV-Board is that the main chip on the former has been upgraded to the ESP32-P4 chip revision v3.1 or later version."* (S1) |
| Sibling | [ESP32-P4X-C5-Function-EV-Board](../esp32-p4x-c5-function-ev-board/README.md) — same concept, ESP32-C5 radio instead of C6 |

> **Caveat — SKU vs. design.** The string `ESP32-P4X-Function-EV-Board-L2` appears in Espressif's DevKits catalogue (S3). No user guide, schematic or revision note anywhere in `esp-dev-kits` uses that suffix, and Espressif's own DevKits blurb says the board has "Same functionality as ESP32-P4-Function-EV-Board" (S3). The most likely reading is an accessory-bundle SKU (the LCD and camera are optional extras). **Unresolved** — do not assume it is a distinct PCB.

> **Silicon warning carried by Espressif at the top of the user guide (S1):** *"The ESP32-P4X-Function-EV-Board with the ESP32-P4 chip revision v3.1 does not support Secure Download. Please do not enable Secure Download Mode."* This is errata **ROM-770**. See the [chip errata table](../../../components/espressif/esp32-p4/README.md#10-errata-summary).

---

## 2. What it is and what it is for

A large, fully populated evaluation platform for the ESP32-P4's multimedia path. Espressif positions it for "visual doorbells, network cameras, smart home central control screens, LCD electronic price tags, two-wheel vehicle dashboards" (S1). Practically, it is the board you use to answer *"can the P4 actually drive my panel and camera at the frame rate I need"* before committing to a custom design.

It is not a compact or low-power board. It has three USB-C ports plus a USB-A host port, RJ45 Ethernet, a speaker header, and a 40-pin GPIO header, and its power tree is explicitly not optimised for sleep (§7).

---

## 3. Key specifications

| Function | Part / interface | Component record |
|---|---|---|
| Main SoC | ESP32-P4 (QFN104), rev v3.1+ | [ESP32-P4](../../../components/espressif/esp32-p4/README.md) |
| Wireless | **ESP32-C6-MINI-1** module — 2.4 GHz Wi-Fi 6, Bluetooth 5 (LE), 802.15.4 | **no record** — ⚠ *not* the [ESP32-C6-WROOM-1](../../../components/espressif/esp32-c6-wroom-1/README.md), which is a different module (PCB-trace WROOM package, 8 MB flash). See §5 |
| Flash | 16 MB SPI NOR, **80 MHz max, no auto-suspend** by default | no record |
| PSRAM | In-package on the P4 (16 or 32 MB per part number) | [ESP32-P4 §3](../../../components/espressif/esp32-p4/README.md#3-memory-subsystem) |
| Display | MIPI-DSI via 15-pin 1.0 mm FPC (`1.0K-GT-15PB`) → LCD adapter board → **7-inch capacitive touch, 1024 × 600** (optional accessory) | no record — [connector and panel datasheets](../shared-artifacts/sources.md#1-function-ev-family--fpc-connector-panel-camera-and-display-driver-documentation) |
| Display driver ICs | EK79007AD and EK73217BCGA — a **pair** on the same panel/adapter, not alternatives | [ek79007ad](../../../components/fitipower/ek79007ad/README.md) · [ek73217bcga](../../../components/fitipower/ek73217bcga/README.md) |
| Camera | MIPI-CSI via 15-pin 1.0 mm FPC → camera adapter board → **2 MP** module (optional accessory) | no record — [datasheet retained](../shared-artifacts/sources.md#1-function-ev-family--fpc-connector-panel-camera-and-display-driver-documentation) |
| Audio codec | **ES8311** mono codec, I2S + I2C to the P4 | no record |
| Audio amplifier | **NS4150B** 3 W mono Class-D; speaker header drives 4 Ω / 3 W, 2.00 mm pitch | no record |
| Microphone | Onboard, into the ES8311 | no record |
| Ethernet | **IP101GR** PHY on the P4's EMAC RMII interface → RJ45, 10/100 Mbps | no record |
| Storage | MicroSD slot, 4-bit mode | [generic microSD / SDMMC](../../../components/generic/micro-sd-sdmmc/README.md) |
| USB | USB 2.0 Type-C (HS device) · USB 2.0 Type-A (HS host, 500 mA) · USB Full-speed Type-C · USB Serial/JTAG Type-C | [generic USB-C interface](../../../components/generic/usb-c-interface/README.md) |
| USB host power switch | **TPS2051C**, 500 mA limit with short-circuit/overload protection | no record |
| Clocks | 40 MHz XTAL, 32.768 kHz XTAL | no record |
| Power | Buck for 3.3 V, buck for P4 `VDD_HP`, 5 V→3.3 V LDO, power switch, 5 V power-on LED | no record |
| Expansion | J1 40-pin header | §6 |
| Buttons | BOOT, Reset | no record |

All rows above from S1 unless noted. **Manufacturer:** [Espressif Systems — vendor sourcing guide](../../../vendors/espressif/README.md).

Rows marked **no record** name a real fitted part that has no entry under
[`components/`](../../../components/README.md). Where a datasheet was retained it is in
[`../shared-artifacts/`](../shared-artifacts/) with provenance in
[its manifest](../shared-artifacts/sources.md).

**Reading the table practically:** the two ports that trip people up are the USB pair. *The USB 2.0 Type-C and USB 2.0 Type-A ports cannot be used simultaneously* (S1) — they are two physical connectors on the **one** USB 2.0 High-Speed OTG controller, wired for the two roles. Separately, the USB Serial/JTAG Type-C is the port you flash and debug through, and on this board it is a native P4 peripheral rather than a USB-UART bridge chip; that change was made in board version v1.52 of the predecessor (§9).

---

## 4. Board layout, clockwise from J1

Espressif's own numbering (S1), condensed:

1. **J1** GPIO header · 2. ESP32-C6 module programming connector · 3. **ESP32-C6-MINI-1** · 4. Microphone · 5. Reset button · 6. **ES8311** codec · 7. Speaker output port · 8. **NS4150B** PA · 9. 5 V→3.3 V LDO · 10. **BOOT** button · 11. **IP101GR** Ethernet PHY · 12. 3.3 V buck · 13. 5 V power-on LED · 14. RJ45 · 15. USB Full-speed port · 16. **USB Serial/JTAG port** · 17. USB 2.0 Type-C · 18. USB 2.0 Type-A · 19. Power switch · 20. **TPS2051C** USB power switch · 21. **MIPI CSI connector** · 22. `VDD_HP` buck · 23. **ESP32-P4** · 24. 40 MHz XTAL · 25. 32.768 kHz XTAL · 26. **MIPI DSI connector** · 27. 16 MB SPI flash · 28. MicroSD slot

---

## 5. The companion radio, and why it is there

The ESP32-P4 has **no radio at all**. This board therefore carries an **ESP32-C6-MINI-1** module whose only job is Wi-Fi and Bluetooth, driven from the P4 over ESP-Hosted. The full argument, including how this compares with the ESP32-S3's Bluetooth-Classic workaround on the Waveshare knob board, is in [ESP32-P4 §5](../../../components/espressif/esp32-p4/README.md#5-no-wireless--the-defining-constraint).

Three board-level consequences you will meet immediately:

1. **There are two firmware images on this board.** The P4's application, and ESP-Hosted slave firmware on the C6. They must be version-matched.
2. **There are two programming paths.** The P4 flashes over its own USB Serial/JTAG port; the C6 flashes over a dedicated *ESP32-C6 Module Programming Connector* (item 2), which needs an ESP-Prog or another UART tool — it is **not** wired to any USB port on the board.
3. **Choosing C6 fixes your radio at 2.4 GHz.** If you need 5 GHz, that is not a firmware change; it is a different board — the [C5 variant](../esp32-p4x-c5-function-ev-board/README.md).

---

## 6. J1 header block

40-pin header. Numbering matches the schematic (S1). `P` = power, `I/O/T` = input/output/high-impedance.

| No. | Name | Type | Function | | No. | Name | Type | Function |
|---:|---|---|---|---|---:|---|---|---|
| 1 | 3V3 | P | 3.3 V | | 21 | 2 | I/O/T | GPIO2 |
| 2 | 5V | P | 5 V | | 22 | NC(1) | I/O/T | GPIO1 [a] |
| 3 | 7 | I/O/T | GPIO7 | | 23 | NC(0) | I/O/T | GPIO0 [a] |
| 4 | 5V | P | 5 V | | 24 | 36 | I/O/T | GPIO36 |
| 5 | 8 | I/O/T | GPIO8 | | 25 | GND | GND | Ground |
| 6 | GND | GND | Ground | | 26 | 32 | I/O/T | GPIO32 |
| 7 | 23 | I/O/T | GPIO23 | | 27 | NC | – | No connection |
| 8 | 37 | I/O/T | **U0TXD**, GPIO37 | | 28 | NC | – | No connection |
| 9 | GND | GND | Ground | | 29 | 33 | I/O/T | GPIO33 |
| 10 | 38 | I/O/T | **U0RXD**, GPIO38 | | 30 | GND | GND | Ground |
| 11 | 21 | I/O/T | GPIO21 | | 31 | 26 | I/O/T | GPIO26 |
| 12 | 22 | I/O/T | GPIO22 | | 32 | 54 | I/O/T | GPIO54 |
| 13 | 20 | I/O/T | GPIO20 | | 33 | 48 | I/O/T | GPIO48 |
| 14 | GND | GND | Ground | | 34 | GND | GND | Ground |
| 15 | 6 | I/O/T | GPIO6 | | 35 | 53 | I/O/T | GPIO53 |
| 16 | 5 | I/O/T | GPIO5 | | 36 | 46 | I/O/T | GPIO46 |
| 17 | 3V3 | P | 3.3 V | | 37 | 47 | I/O/T | GPIO47 |
| 18 | 4 | I/O/T | GPIO4 | | 38 | 27 | I/O/T | GPIO27 |
| 19 | 3 | I/O/T | GPIO3 | | 39 | GND | GND | Ground |
| 20 | GND | GND | Ground | | 40 | NC(45) | I/O/T | GPIO45 [b] |

[a] **GPIO0 and GPIO1 are not connected by default.** They are consumed by the 32.768 kHz crystal. To free them, disable XTAL_32K by moving `R61`→`R199` and `R59`→`R197` (S1). You lose the low-power clock.
[b] **GPIO45 is not connected by default**; it is consumed by `SD_PWRn`. Free it by moving `R231`→`R100` (S1). You lose software control of MicroSD power.

Note what is *absent*: the MIPI-DSI and MIPI-CSI lanes are not on this header and cannot be — they are dedicated high-speed differential pins on the FPC connectors. J1 is for slow expansion, not for tapping the multimedia buses.

### LCD adapter board wiring

Two of the LCD adapter's signals are **not** carried on the FPC and must be jumpered by hand (S1):

| ESP32-P4X-Function-EV-Board | LCD adapter board | Note |
|---|---|---|
| MIPI DSI connector | J3 header | via the **reverse-direction** ribbon cable |
| GPIO27 (J1 pin 38) | RST_LCD (J6) | DuPont wire; GPIO is software-configurable, 27 is the default |
| GPIO26 (J1 pin 31) | PWM (J6) | DuPont wire; backlight PWM, 26 is the default |
| 5V (J1) | 5V (J6) | Only if not powering the adapter from its own J1 USB |
| GND (J1) | GND (J6) | |

**Ribbon-cable direction is not interchangeable.** The **forward-direction** cable (contacts on the same side at both ends) is for the **camera**; the **reverse-direction** cable (contacts on opposite sides) is for the **LCD** (S1). Getting this wrong mirrors the pinout.

---

## 7. Known limitations

- **Flash is capped at 80 MHz with no auto-suspend.** 120 MHz and auto-suspend require contacting Espressif (S1). If your benchmark assumes 120 MHz flash, it does not apply here.
- **This board cannot demonstrate the P4's sleep-current figures.** Espressif's own note: LDO_VO3/LDO_VO4 power on-board VDD domains and must be configured in software; leaving them on in Light/Deep-sleep gives "relatively high" consumption, and *"even when turned off, the total power consumption may still exceed the typical low-power specifications listed in the chip datasheet due to the board-level power architecture"* (S1). Espressif recommends optimising the power architecture in your own hardware. Do not benchmark P4 sleep power here.
- **USB Type-C (HS) and USB Type-A (HS host) are mutually exclusive.**
- **The C6 module has no USB path**; it needs an ESP-Prog on the module programming connector.
- **The LCD and camera are optional accessories.** A bare board has no display and no camera.
- **No published BOM for the main board.** Espressif publishes the schematic, PCB layout, dimensions and assembly drawing for the (EOL) predecessor, and full reference designs including BOM and Gerbers only for the LCD and camera *adapter* boards. For the main board, Espressif directs you to `sales@espressif.com`.

---

## 8. Design files: what exists, and an important substitution

**Espressif publishes no direct schematic or PCB PDF for the ESP32-P4X-Function-EV-Board.** The user guide's Related Documents section offers a single *"ESP32-P4X-Function-EV-Board Reference Design (ZIP)"* link, and **that link does not resolve** — it returns the documentation platform's 13 745-byte soft-404 shell for every filename variant tried. Every probe is recorded in [component-download-failures.txt](../../../component-download-failures.txt).

What is retained instead, and why it is defensible:

Because the P4X board differs from the EOL ESP32-P4-Function-EV-Board **only in the silicon revision fitted** (Espressif's own words, S1), the predecessor's complete, published design-file set is the closest available primary evidence for this board's circuitry. Those files are retained under the [EOL board's record](../esp32-p4-function-ev-board/README.md) — schematic v1.52, PCB layout, dimensions (PDF + DXF), assembly drawing.

**Label that substitution honestly in any downstream work.** The claim "the P4X schematic is identical to the v1.52 schematic" is *not* established; what is established is that Espressif describes the difference as a chip-revision change. Board-revision silkscreen, component substitutions and errata-driven passive changes are all possible and unverified.

The FPC connector spec, panel, camera and display-driver datasheets, and the LCD/camera adapter reference designs (which *do* include Gerbers, BOM and assembly drawings) are shared across the P4 board family and are retained once under [`devices/espressif/shared-artifacts/`](../shared-artifacts/) to avoid storing four identical copies.

---

## 9. Product history

| Date/version | Event | Source |
|---|---|---|
| ESP32-P4-Function-EV-Board **v1.4** | Original release. USB-to-UART Type-C port for debug; IO24 and IO25 present on the pin headers | S2 |
| ESP32-P4-Function-EV-Board **v1.52** | Debug port switched to the **P4's native USB Serial/JTAG**; a Full-speed USB OTG breakout added on a Type-C port; **IO24 and IO25 removed** from the pin headers | S2 |
| ESP32-P4-Function-EV-Board | Moved to **EOL**; documentation retained "for reference only… no longer receive updates, bug fixes, or official support" | S4 |
| **ESP32-P4X-Function-EV-Board** | Current board. Chip upgraded to ESP32-P4 revision **v3.1 or later** | S1 |

If you are porting code or a pin map from an older P4 board or an old blog post, **check for IO24/IO25**; their removal in v1.52 is the most likely silent breakage.

---

## 10. Getting started, examples and firmware

Standard ESP-IDF flow; target `esp32p4`; **minimum ESP-IDF v5.3**, newer strongly preferred — see [ESP32-P4 §9](../../../components/espressif/esp32-p4/README.md#9-software-support-and-minimum-esp-idf-version).

Flash and monitor over the **USB Serial/JTAG** Type-C port. To force download mode: hold **BOOT**, press and release **Reset**, release BOOT.

Official examples (S1), in `espressif/esp-dev-kits` at `examples/esp32-p4-function-ev-board/` (commit `f6f80ab` at retrieval):

| Example | What it demonstrates |
|---|---|
| `esp_brookesia_phone` | Android-like multi-app UI over ESP_Brookesia, exercising MIPI-DSI, MIPI-CSI, the ESP32-C6, SD card and audio together — the best single integration example |
| `lvgl_demo_v8` | LVGL v8 port + built-in performance benchmarks on the 7-inch panel |
| `lvgl_demo_v9` | LVGL v9 port + performance benchmarks |

Prebuilt images can also be flashed from a browser via **ESP Launchpad** without installing ESP-IDF: `https://espressif.github.io/esp-launchpad/?flashConfigURL=https://espressif2022.github.io/ESP32-P4-Function-EV-Board/launchpad.toml` (S1). Note the Launchpad config is still published under the *pre-P4X* board name.

---

## 11. Sources

**Full manifest — class, medium, retrieval dates, what each source establishes and its limitations:
[`sources.md`](sources.md).** The summary below is retained for quick reference; `S1`–`S5` map onto
`P4X-1`–`P4X-5` there.

> ⚠ **S2's URL is now dead.** The EOL user guides moved out of the `eol/` path segment between
> 2026-08-21 and 2026-08-28; the cited path returns HTTP 404 with no Wayback capture. Current URL
> and full finding: [`sources.md` §5](sources.md#5-retrieval-findings).

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes |
|---|---|---|---|---|---|---|---|---|
| S1 | ESP32-P4X-Function-EV-Board User Guide | Espressif Systems | primary | manual | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4x-function-ev-board/user_guide.html | 2026-08-21 | esp-dev-kits `latest`, source commit `f6f80ab` | Everything in §1–§8, §10 |
| S2 | ESP32-P4-Function-EV-Board User Guide (EOL section) | Espressif Systems | primary | manual | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/eol/esp32-p4-function-ev-board/user_guide.html | 2026-08-21 | esp-dev-kits `latest` | v1.4 → v1.52 revision history; design-file URLs |
| S3 | Espressif DevKits product catalogue | Espressif Systems | primary | store listing | https://www.espressif.com/en/products/devkits | 2026-08-21 | as served | Board lineup; `-L2` SKU string; "Same functionality as ESP32-P4-Function-EV-Board" |
| S4 | esp-dev-kits — EOL (End of Life) Boards, ESP32-P4 | Espressif Systems | primary | official page | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/eol/eol-boards.html | 2026-08-21 | `latest` | EOL status of the predecessor boards |
| S5 | esp-dev-kits documentation, ESP32-P4 target, PDF build | Espressif Systems | primary | manual | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp-dev-kits-en-master-esp32p4.pdf | 2026-08-21 | esp-docs `master` build | Offline copy of every P4 board user guide — **archived 2026-08-24**, [record](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) |

---

## 12. Local artifacts

Board-specific: **none** — see §8 for why, and [component-download-failures.txt](../../../component-download-failures.txt) for the failed probes.

Shared with the rest of the ESP32-P4 board family, in [`../shared-artifacts/`](../shared-artifacts/):

| File | Bytes | SHA-256 |
|---|---:|---|
| ~~esp-dev-kits-en-master-esp32p4.pdf~~ **archived 2026-08-24** — [record](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) | 30 482 003 | `04d75d2acda82c8f5136bfed4d1732e7e4bd095437e2ecacce271374d8f8538c` |
| 1.0K-GT-15PB-fpc-connector-specification.pdf | 1 257 112 | `9cbe18e256bdab92010f96bf35da06e882e84d5f45e82b4fd8df5121b3298aba` |
| camera-module-datasheet.pdf | 2 810 779 | `34c6b337b0b2d555c2c8a412196c0eb93924fa9189f0d9e925fed4644d1922cc` |
| display-datasheet.pdf | 897 664 | `f426dba146929c85441ac68720126e2c8a29d9bde58a66b72e3b5aa23d20c9de` |
| ek73217bcga-datasheet.pdf | 1 571 109 | `bd4ec28f5b11ab95536da6cf6162af18ff8d1ec34fa19379444eb5c0e8f7763a` |
| ek79007ad-datasheet.pdf | 3 723 767 | `2dbab767e040959f1c7ce1ae3af4e65c888e04d88b066bcb1f3bddee6c8287a4` |
| lcd-subboard-schematics.pdf | 328 112 | `cbb6a53dc20a68748784b5bf3548801710f925bd69dbdb75510a9a46d6d0007a` |
| lcd-subboard-pcb-layout.pdf | 384 111 | `6f1c9a3570205d42bb117a7a3eb930a97646e44d346a244a02eff2c885d69774` |
| camera-subboard-schematics.pdf | 332 122 | `dcb30637c379e9fde13dfadefe1b143902fd6ec53383e562ddbab33b271dbe37` |
| camera-subboard-pcb-layout.pdf | 140 496 | `791c0922cc94891d12a965dcd9c866c3fc663b8d216f6019d9e6ab6873561127` |
| lcd-adapter-board-reference-design.zip | 1 276 237 | `231e1ff2f9373de5b9924eaaab00801ad777fb483945629f160423c3752693ed` |
| camera-adapter-board-reference-design.zip | 1 349 188 | `2ab4b8ad20b60817ddd1e8d72de0680f841c9bc0d452b82d9d93aa82c9b8e529` |

Closest available main-board design files: [EOL board artifacts](../esp32-p4-function-ev-board/README.md#5-local-artifacts) — read §8 first.

---

## 13. Related records

- [Source manifest](sources.md) — every source behind this record
- [ESP32-P4 component record](../../../components/espressif/esp32-p4/README.md)
- [ESP32-P4X-C5-Function-EV-Board](../esp32-p4x-c5-function-ev-board/README.md) — the 5 GHz sibling
- [ESP32-P4X-EYE](../esp32-p4x-eye/README.md) — the camera-focused P4 board
- [ESP32-P4-Function-EV-Board (EOL)](../esp32-p4-function-ev-board/README.md) — predecessor, and the source of the retained design files
- [Shared artifacts](../shared-artifacts/README.md) · [their sources](../shared-artifacts/sources.md)
- [Espressif vendor sourcing guide](../../../vendors/espressif/README.md)
- [Component index](../../../components/README.md) · [Device index](../../README.md)


> **Shared artifact note.** The offline esp-dev-kits PDF for the ESP32-P4 boards (`esp-dev-kits-en-master-esp32p4.pdf`) was **archived 2026-08-24** — its content was already mined into this and the sibling board records. Provenance, SHA-256 and verified download URLs: [`shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md`](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md).
