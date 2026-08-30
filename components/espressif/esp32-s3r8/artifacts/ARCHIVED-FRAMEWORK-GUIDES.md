# Archived framework/SDK guides — ESP32-S3R8

Three large Espressif **framework documentation** PDFs that used to live in this directory have been moved out of the repository. They were **regenerable from stable, verified Espressif URLs** and are not scarce, unlike the chip datasheet, TRM, errata and hardware-design guidelines in this directory, **all of which are retained**.

- **Archived:** 2026-08-24
- **Moved to:** `archive/components/espressif/esp32-s3r8/artifacts/` (same relative path)
- **Total reclaimed here:** 80 963 336 bytes (~77.2 MiB)

Nothing was deleted. The knowledge worth keeping was extracted into committed Markdown **before** the files were moved — see [What was extracted](#what-was-extracted-and-where-it-now-lives).

---

## 1. `esp-idf-programming-guide-v5.2.5-esp32s3.pdf`

| Field | Value |
|---|---|
| **Original path** | `components/espressif/esp32-s3r8/artifacts/esp-idf-programming-guide-v5.2.5-esp32s3.pdf` |
| **What it is** | ESP-IDF Programming Guide — complete API reference and API guides, rendered for the **`esp32s3` target** |
| **Version** | **v5.2.5** (versioned release, immutable URL) |
| **Byte size** | **29 188 396** |
| **SHA-256** | `e29de49974c7e9714f2ff6d98507cd7f0240ee538acb2120ce58ba44dc9be4ea` |
| **Page count** | **3 244** |
| **Build date** | PDF `CreationDate` **2025-02-26 05:55:54** (LaTeX/hyperref → xdvipdfmx) |
| **Why removal was OK** | Versioned release documentation on an immutable per-release URL, which returned **exactly 29 188 396 bytes** — byte-identical in size to the local copy. Three independent recovery paths verified. |

**Verified download URLs** (checked 2026-08-24):

| # | URL | Result |
|---|---|---|
| 1 | `https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32s3/esp-idf-en-v5.2.5-esp32s3.pdf` | **HTTP 206** (range GET), `application/pdf`, **`Content-Range: bytes 0-0/29188396`** ✅ size matches exactly |
| 2 | `https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32s3/index.html` | **HTTP 200**, `Content-Length: 9742` |
| 3 | `http://web.archive.org/web/20251108075140/https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32s3/esp-idf-en-v5.2.5-esp32s3.pdf` | **HTTP 200** — Wayback capture, 2025-11-08 |
| 4 | `https://github.com/espressif/esp-idf/releases/tag/v5.2.5` | **HTTP 200** |

> v5.2.5 is *the newest ESP-IDF release for which Espressif publishes a PDF build at all* — see the [Espressif vendor guide](../../../../vendors/espressif/README.md).

---

## 2. `esp-idf-programming-guide-v5.1.4-esp32s3.pdf`

| Field | Value |
|---|---|
| **Original path** | `components/espressif/esp32-s3r8/artifacts/esp-idf-programming-guide-v5.1.4-esp32s3.pdf` |
| **What it is** | ESP-IDF Programming Guide, **`esp32s3` target** |
| **Version** | **v5.1.4** |
| **Byte size** | **25 626 642** |
| **SHA-256** | `d1efc23ceef7859fd31e089f76dffa4ae9b1b56b0cce17a236b88795a10acfde` |
| **Page count** | **2 870** |
| **Build date** | PDF `CreationDate` **2024-05-09 12:28:47** |
| **Why removal was OK** | Versioned release; immutable URL returned **`Content-Range: bytes 0-0/25626642`**, matching the local size exactly. |

**Verified download URLs** (checked 2026-08-24):

| # | URL | Result |
|---|---|---|
| 1 | `https://docs.espressif.com/projects/esp-idf/en/v5.1.4/esp32s3/esp-idf-en-v5.1.4-esp32s3.pdf` | **HTTP 206**, `application/pdf`, **`Content-Range: bytes 0-0/25626642`** ✅ |
| 2 | `https://docs.espressif.com/projects/esp-idf/en/v5.1.4/esp32s3/index.html` | **HTTP 200**, `Content-Length: 9621` |
| 3 | `http://web.archive.org/web/20250904075935/https://docs.espressif.com/projects/esp-idf/en/v5.1.4/esp32s3/esp-idf-en-v5.1.4-esp32s3.pdf` | **HTTP 200** — Wayback capture, 2025-09-04 |
| 4 | `https://github.com/espressif/esp-idf/releases/tag/v5.1.4` | **HTTP 200** |

---

## 3. `esp-iot-solution-programming-guide.pdf`

| Field | Value |
|---|---|
| **Original path** | `components/espressif/esp32-s3r8/artifacts/esp-iot-solution-programming-guide.pdf` |
| **What it is** | **ESP-IoT-Solution User Guide** — the official home of the ESP-IDF *component* drivers: LCD panel drivers (SPI/QSPI/I80/RGB/MIPI-DSI), touch controllers, knob/encoder input, LVGL adapters, USB host/device stacks, sensor hub |
| **Version** | Release **`master`** — ⚠ **not a versioned release** |
| **Byte size** | **26 148 298** |
| **SHA-256** | `8bf04c5a5a700337815c9df0e5b5f92275b4c1a900584bcb5034e8dc4802ab93` |
| **Page count** | **747** |
| **Publication date** | Title page states **Jul 29, 2026**; PDF `CreationDate` 2026-07-29 02:10:23; server `Last-Modified: Wed, 29 Jul 2026 07:10:23 GMT` |
| **Why removal was OK** | The canonical URL currently serves a file of **exactly 26 148 298 bytes**, byte-identical in size to the local copy, plus a Wayback capture and the full documentation source in Git. |

> ⚠ **Moving-target caveat.** This is a `master` build; URL 1 will serve a *newer* document over time and will not reproduce this exact 2026-07-29 build indefinitely. Mitigations: (a) the Wayback capture below, (b) a **fresh Wayback save was submitted 2026-08-24 (HTTP 200)** capturing this build, (c) the documentation source is in Git.

**Verified download URLs** (checked 2026-08-24):

| # | URL | Result |
|---|---|---|
| 1 | `https://docs.espressif.com/projects/esp-iot-solution/en/latest/esp-iot-solution-en-master.pdf` | **HTTP 206**, `application/pdf`, **`Content-Range: bytes 0-0/26148298`** ✅ size matches exactly; `Last-Modified: Wed, 29 Jul 2026 07:10:23 GMT` |
| 2 | `https://docs.espressif.com/projects/esp-iot-solution/en/latest/index.html` | **HTTP 200**, `Content-Length: 11224` — HTML docs root (where URL 1 was discovered; linked as `./esp-iot-solution-en-master.pdf`) |
| 3 | `http://web.archive.org/web/20260707003349/https://docs.espressif.com/projects/esp-iot-solution/en/latest/esp-iot-solution-en-master.pdf` | **HTTP 200** — Wayback capture, 2026-07-07 |
| 4 | `https://github.com/espressif/esp-iot-solution` | **HTTP 200** — documentation source under `docs/` |

> **Note on the URL:** like ESP-ADF, this PDF is **target-agnostic** — `esp-iot-solution-en-master.pdf`, with no chip suffix. The plausible-looking `.../esp-iot-solution-en-master-esp32s3.pdf` and `.../esp32s3/esp-iot-solution-en-master-esp32s3.pdf` both return **HTTP 404**; both were probed on 2026-08-24.

---

## What was extracted, and where it now lives

Knowledge mining was done with `pdftotext -layout` before archiving. Every extracted fact carries a page citation back to the specific build recorded above.

| New document | Captures |
|---|---|
| [`guides/espressif/esp-iot-solution-components.md`](../../../../guides/espressif/esp-iot-solution-components.md) | The full ESP-IoT-Solution extraction: the **LCD driver-interface comparison table** (SPI/QSPI/I80/RGB/MIPI-DSI — IO count, data width, bandwidth, GRAM location) with the QSPI GRAM caveat that splits SPD2010-style from ST77903-style driving, and the warning that the driver-IC model alone does not determine interface type (`IM[3:0]` pins); the **supported touch-controller list** and the `esp_lcd_touch` abstraction; the **Knob component** — its ~30 pulses/second ceiling, its explicit "not 100 % accurate" caveat, the five knob events, the configuration items and the `enable_power_save` light-sleep gotcha; the USB controller taxonomy including the ESP-IDF 5.5 P4 USB-PHY merge. |
| [`guides/espressif/esp-idf-peripheral-capabilities.md`](../../../../guides/espressif/esp-idf-peripheral-capabilities.md) | The ESP32-vs-S3-vs-P4 extraction from the two ESP-IDF guides above (plus the ESP32 and P4 builds): peripheral instance counts stated numerically; the fact that **ESP32-S3 is `LEDC_LOW_SPEED_MODE` only** while the ESP32 has a high-speed group; SDMMC slot capabilities; cache-coherency absence; and the **ESP32-S3 octal-PSRAM 120 MHz warning** — "an experimental feature… after the temperature increases or decreases by approximately 20 Celsius degrees… accesses to / from PSRAM will crash randomly" — which bears directly on the R8's in-package octal PSRAM. |

Cross-linked from the [ESP32-S3R8 component record](../README.md).

## What was deliberately **not** archived from this directory

Retained because they are the scarce, high-value primary sources: `esp32-s3-datasheet.pdf` (+ Waveshare mirror), `esp32-s3-technical-reference-manual.pdf` (+ Waveshare mirror), `esp32-s3-errata.pdf`, `esp32-s3-hardware-design-guidelines.pdf`.
