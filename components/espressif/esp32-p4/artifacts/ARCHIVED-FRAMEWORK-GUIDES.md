# Archived framework/SDK guide — ESP32-P4

One large Espressif **framework documentation** PDF that used to live in this directory has been moved out of the repository. It was **regenerable from a stable, verified Espressif URL** and is not scarce, unlike the datasheet, technical reference manual, errata and hardware-design guidelines in this directory, **all of which are retained**.

- **Archived:** 2026-08-24
- **Moved to:** `archive/components/espressif/esp32-p4/artifacts/` (same relative path)
- **Total reclaimed here:** 13 656 675 bytes (~13.0 MiB)

Nothing was deleted. The knowledge worth keeping was extracted into committed Markdown **before** the file was moved — see [What was extracted](#what-was-extracted-and-where-it-now-lives).

---

## 1. `esp-idf-programming-guide-v5.3.2-esp32p4.pdf`

| Field | Value |
|---|---|
| **Original path** | `components/espressif/esp32-p4/artifacts/esp-idf-programming-guide-v5.3.2-esp32p4.pdf` |
| **What it is** | ESP-IDF Programming Guide — complete API reference and API guides, rendered for the **`esp32p4` target** |
| **Version** | **v5.3.2** (versioned release, immutable URL) |
| **Byte size** | **13 656 675** |
| **SHA-256** | `adf06f5531a5c84505dcb069e28a864a653b39e0d299701c0fb905e02f2e6f65` |
| **Page count** | **2 262** |
| **Build date** | PDF `CreationDate` **2024-12-05 19:17:58** (LaTeX/hyperref → xdvipdfmx) |
| **Why removal was OK** | Versioned release documentation on an immutable per-release URL, which returned **exactly 13 656 675 bytes** — byte-identical in size to the local copy. Three independent recovery paths verified. |

**Verified download URLs** (checked 2026-08-24):

| # | URL | Result |
|---|---|---|
| 1 | `https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32p4/esp-idf-en-v5.3.2-esp32p4.pdf` | **HTTP 206** (range GET), `Content-Type: application/pdf`, **`Content-Range: bytes 0-0/13656675`** ✅ size matches exactly |
| 2 | `https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32p4/index.html` | **HTTP 200**, `Content-Length: 9753` — HTML docs root for the same build |
| 3 | `http://web.archive.org/web/20250210105200/https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32p4/esp-idf-en-v5.3.2-esp32p4.pdf` | **HTTP 200** — Wayback capture, 2025-02-10 |
| 4 | `https://github.com/espressif/esp-idf/releases/tag/v5.3.2` | **HTTP 200** — source tag; docs buildable from `docs/` |

> v5.3.x is the relevant series for ESP32-P4: it is the first ESP-IDF line with production P4 support. See [ESP32-P4 § 9 Software support and minimum ESP-IDF version](../README.md#9-software-support-and-minimum-esp-idf-version).

---

## What was extracted, and where it now lives

Knowledge mining was done with `pdftotext -layout` before archiving. Every extracted fact carries a page citation back to the specific build recorded above.

| New document | Captures |
|---|---|
| [`guides/espressif/esp-idf-peripheral-capabilities.md`](../../../../guides/espressif/esp-idf-peripheral-capabilities.md) | The ESP32-vs-S3-vs-P4 comparison. P4-specific material extracted from this build includes: **5 regular UARTs + 1 LP UART**, **3 TWAI controllers**, **two USB-OTG peripherals (one High-Speed, one Full-Speed)**, **only one I2S peripheral**, **2 analog-comparator units**; the **SDMMC** situation where slot 0 is "dedicated to UHS-I mode, which is **not yet supported in the driver**" and the host "requires an **external power supply for the IO voltage**"; the absence of hardware cache-coherent interconnect; **`esp_wifi_remote`** as the documented route to Wi-Fi on a radioless part; and the distinctive **PSRAM configuration** — 16-line **HEX** mode only, 20/200 MHz clock options, powered from **internal LDO channel 2** at 1.9 V (fixed; `CONFIG_ESP_LDO_CHAN_PSRAM_DOMAIN` has range "from 2 to 2") with flash on a separate 3.3 V LDO domain, plus `CONFIG_SPIRAM_XIP_FROM_PSRAM`. |

Cross-linked from the [ESP32-P4 component record](../README.md).

## What was deliberately **not** archived from this directory

Retained because they are the scarce, high-value primary sources: `esp32-p4-datasheet.pdf`, `esp32-p4-technical-reference-manual.pdf`, `esp32-p4-errata.pdf`, `esp32-p4-hardware-design-guidelines.pdf`.
