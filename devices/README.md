# Hardware devices

Each device record links to **every component it contains**; each [component record](../components/README.md) links back to the devices that use it, and to its [vendor sourcing guide](../vendors/README.md).

## Seeed Studio

- [Seeed Studio XIAO ESP32S3 Sense](seeed-studio/xiao-esp32s3-sense/README.md), SKU 113991115, retrieved 2026-08-24 — vendor guide: [Seeed Studio](../vendors/seeed-studio/README.md)

A 17.78 x 21.14 mm ESP32-S3R8 board with a detachable camera / PDM microphone / microSD daughterboard on a 30-pin Hirose board-to-board connector. Notable because Seeed publishes **KiCad sources under CC BY-SA 4.0**, which allowed the otherwise-undocumented [board-to-board connector pinout](seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md#2-the-j3-board-to-board-connector-sense-daughterboard-interface) to be reconstructed from the PCB netlist.

Three findings from that pass are worth knowing before buying one: the **user LED and the microSD chip-select are the same pin**; the **daughterboard consumes all four JTAG pins**, so hardware debugging is impossible with it attached; and the shipped **factory firmware contains hardcoded Wi-Fi credentials** and cannot connect to your network.

## Waveshare

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](waveshare/esp32-s3-knob-touch-lcd-1.8/README.md), product ID 31623, retrieved 2026-08-21 — vendor guide: [Waveshare](../vendors/waveshare/README.md)

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

---

## Related

- [Components](../components/README.md) — the parts these boards are built from
- [Vendor sourcing guides](../vendors/README.md) — [Espressif](../vendors/espressif/README.md) · [Waveshare](../vendors/waveshare/README.md)
- [Espressif ecosystem map](../guides/espressif/ecosystem-and-product-lines.md) · [Marketplace comparison](../guides/markets/vendor-comparison.md) · [Clones and variants](../guides/markets/clones-and-variants.md)
