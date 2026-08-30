# Archived framework/SDK guide — ESP32-P4 development boards

One large Espressif **development-board documentation** PDF that used to live in this directory has been moved out of the repository. It was **regenerable from a stable, verified Espressif URL** and is not scarce, unlike the board schematics, PCB layouts, dimension drawings and component datasheets in this directory, **all of which are retained**.

- **Archived:** 2026-08-24
- **Moved to:** `archive/hardware-doc/devices/espressif/shared-artifacts/` (same relative path)
- **Total reclaimed here:** 30 482 003 bytes (~29.1 MiB)

Nothing was deleted.

---

## 1. `esp-dev-kits-en-master-esp32p4.pdf`

| Field | Value |
|---|---|
| **Original path** | `devices/espressif/shared-artifacts/esp-dev-kits-en-master-esp32p4.pdf` |
| **What it is** | **esp-dev-kits Documentation**, ESP32-P4 target — the offline build of the user guides for every ESP32-P4 development board: ESP32-P4X-Function-EV-Board, ESP32-P4X-C5-Function-EV-Board, ESP32-P4X-EYE, and the EOL ESP32-P4-Function-EV-Board and ESP32-P4-EYE |
| **Version** | Release **`master`** — ⚠ **not a versioned release** |
| **Byte size** | **30 482 003** |
| **SHA-256** | `04d75d2acda82c8f5136bfed4d1732e7e4bd095437e2ecacce271374d8f8538c` |
| **Page count** | **80** |
| **Publication date** | Title page states **Aug 23, 2026**; PDF `CreationDate` **2026-08-23 12:25:45** |
| **Why removal was OK** | The canonical URL currently serves a file of **exactly 30 482 003 bytes**, byte-identical in size to the local copy. More importantly, **its content was already fully mined into the five board records** in this tree during the 2026-08-21 research pass — the HTML equivalents of every page in it are cited there as primary sources S1–S5. Its role here was as an offline convenience copy, not as unique evidence. |

> ⚠ **Moving-target caveat.** This is a `master` build; URL 1 will serve a newer document over time. Mitigations: (a) the Wayback capture below, (b) a **fresh Wayback save was submitted 2026-08-24 (HTTP 200)** capturing this build, (c) the documentation source is in Git, (d) the per-board HTML pages are separately cited in each board record.

**Verified download URLs** (checked 2026-08-24):

| # | URL | Result |
|---|---|---|
| 1 | `https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp-dev-kits-en-master-esp32p4.pdf` | **HTTP 206** (range GET), `Content-Type: application/pdf`, **`Content-Range: bytes 0-0/30482003`** ✅ size matches exactly |
| 2 | `https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/index.html` | **HTTP 200**, `Content-Length: 15826` — HTML docs root for the ESP32-P4 board family |
| 3 | `http://web.archive.org/web/20260331013312/https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp-dev-kits-en-master-esp32p4.pdf` | **HTTP 200** — Wayback capture, 2026-03-31 |
| 4 | `https://github.com/espressif/esp-dev-kits` | **HTTP 200** — documentation source and board example code |

> **Note on the URL:** unlike the ESP-ADF and ESP-IoT-Solution PDFs, this one **is** target-scoped and lives under the `esp32p4/` path segment. The un-scoped form `https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp-dev-kits-en-master-esp32p4.pdf` returns **HTTP 404**; it was probed on 2026-08-24.

---

## What this document contained, and where that knowledge lives

This PDF's content was **already extracted** into the board records during the 2026-08-21 research pass, before this archiving exercise. The mapping:

| Content | Where it lives |
|---|---|
| ESP32-P4X-Function-EV-Board — overview, feature list, power supply options, J1 header pin table (40 pins, with the `R61`/`R59`→`R199`/`R197` XTAL_32K and `R231`→`R100` SD_PWRn strap-swap footnotes), block diagram, related documents | [ESP32-P4X-Function-EV-Board record](../esp32-p4x-function-ev-board/README.md) |
| ESP32-P4X-C5-Function-EV-Board — feature list (ESP32-C5-MINI-1, 2.4/5 GHz Wi-Fi 6 + BLE 5 + 802.15.4; 16 MB flash + 32 MB PSRAM; 7-inch 1024×600 MIPI-DSI touch screen; 2 MP MIPI-CSI camera; ES8311 codec + NS4150B amplifier; MicroSD 4-bit; RJ45 10/100; USB 2.0 OTG Type-C, Type-A, Full-Speed and Serial/JTAG ports), "No previous revisions", the `R30`→`R29` P4_WAKEUP_C5 footnote | [ESP32-P4X-C5-Function-EV-Board record](../esp32-p4x-c5-function-ev-board/README.md) |
| ESP32-P4X-EYE — component tables (ESP32-C6-MINI-1U test points, USB 2.0 HS device port, USB debug port, power switch, 1.54-inch 240×240 SPI LCD, MicroSD via 4-line SDIO or SPI, charging indicator), revision statement, related documents | [ESP32-P4X-EYE record](../esp32-p4x-eye/README.md) |
| **The "P4X" naming rule** — *"The difference between the ESP32-P4X-Function-EV-Board and the ESP32-P4-Function-EV-Board is that the main chip on the former has been upgraded to the ESP32-P4 chip revision v3.1 or later version"* (repeated verbatim for the EYE pair) | [ESP32-P4 component record § 1, "The P4X naming trap"](../../../components/espressif/esp32-p4/README.md#1-identity-and-variants) |
| **EOL status** of ESP32-P4-Function-EV-Board and ESP32-P4-EYE, and their v1.4/v1.52 design-file lists | [ESP32-P4-Function-EV-Board record](../esp32-p4-function-ev-board/README.md), [ESP32-P4-EYE record](../esp32-p4-eye/README.md) |

Framework-level material extracted in this pass is in [`guides/espressif/`](../../../guides/espressif/README.md).

## What was deliberately **not** archived from this directory

Retained because they are board- and component-level primary sources that are far harder to re-obtain: `ek79007ad-datasheet.pdf`, `ek73217bcga-datasheet.pdf`, `st7789vw-datasheet.pdf`, `camera-module-datasheet.pdf`, `display-datasheet.pdf`, `ov2710-camera-module-datasheet.pdf`, `hdf2710-47-mipi-camera-module-spec.pdf`, `zjy154kc-if17-lcd-module-spec.pdf`, `1.0K-GT-15PB-fpc-connector-specification.pdf`, the LCD and camera sub-board schematics/PCB/assembly drawings, and both adapter-board reference-design bundles.
