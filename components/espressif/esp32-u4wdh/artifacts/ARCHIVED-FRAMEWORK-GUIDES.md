# Archived framework/SDK guides — ESP32-U4WDH

Three large Espressif **framework documentation** PDFs that used to live in this directory have been moved out of the repository. They were **regenerable from stable, verified Espressif URLs** and are not scarce, unlike the chip datasheet, TRM, errata, hardware-design guidelines and PCNs in this directory, **all of which are retained**.

- **Archived:** 2026-08-24
- **Moved to:** `archive/hardware-doc/components/espressif/esp32-u4wdh/artifacts/` (same relative path)
- **Total reclaimed here:** 94 374 621 bytes (~90.0 MiB)

Nothing was deleted. The knowledge worth keeping was extracted into committed Markdown **before** the files were moved — see [What was extracted](#what-was-extracted-and-where-it-now-lives).

---

## 1. `esp-idf-programming-guide-v5.1.4-esp32.pdf`

| Field | Value |
|---|---|
| **Original path** | `components/espressif/esp32-u4wdh/artifacts/esp-idf-programming-guide-v5.1.4-esp32.pdf` |
| **What it is** | ESP-IDF Programming Guide — the complete API reference and API guides for ESP-IDF, rendered for the **`esp32` target** |
| **Version** | **v5.1.4** (versioned release, immutable URL) |
| **Byte size** | **37 852 819** |
| **SHA-256** | `05dbacd27a36cd1189f036cfd93d5e711fa3b9a0933dfda63f6ba326b44a384e` |
| **Page count** | **3 006** |
| **Build date** | PDF `CreationDate` **2024-05-09 12:30:13** (LaTeX/hyperref → xdvipdfmx) |
| **Why removal was OK** | Versioned release documentation. The URL below is immutable per-release and returned a file of **exactly 37 852 819 bytes** — byte-identical in size to the local copy. Three independent recovery paths verified. |

**Verified download URLs** (checked 2026-08-24):

| # | URL | Result |
|---|---|---|
| 1 | `https://docs.espressif.com/projects/esp-idf/en/v5.1.4/esp32/esp-idf-en-v5.1.4-esp32.pdf` | **HTTP 206** (range GET), `Content-Type: application/pdf`, **`Content-Range: bytes 0-0/37852819`** ✅ size matches exactly |
| 2 | `https://docs.espressif.com/projects/esp-idf/en/v5.1.4/esp32/index.html` | **HTTP 200**, `Content-Length: 9605` — HTML docs root for the same build |
| 3 | `http://web.archive.org/web/20251206114556/https://docs.espressif.com/projects/esp-idf/en/v5.1.4/esp32/esp-idf-en-v5.1.4-esp32.pdf` | **HTTP 200** — Wayback capture, 2025-12-06 |
| 4 | `https://github.com/espressif/esp-idf/releases/tag/v5.1.4` | **HTTP 200** — source tag; docs are buildable from `docs/` |

---

## 2. `esp-idf-programming-guide-v5.2.5-esp32.pdf`

| Field | Value |
|---|---|
| **Original path** | `components/espressif/esp32-u4wdh/artifacts/esp-idf-programming-guide-v5.2.5-esp32.pdf` |
| **What it is** | ESP-IDF Programming Guide, **`esp32` target** |
| **Version** | **v5.2.5** |
| **Byte size** | **30 789 611** |
| **SHA-256** | `02b301cff2b2816ea36bd2cc45003a327097c1005a88274c8f560d73ead6098b` |
| **Page count** | **3 292** |
| **Build date** | PDF `CreationDate` **2025-02-26 05:56:47** |
| **Why removal was OK** | Versioned release; immutable URL returned **`Content-Range: bytes 0-0/30789611`**, matching the local size exactly. |

**Verified download URLs** (checked 2026-08-24):

| # | URL | Result |
|---|---|---|
| 1 | `https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32/esp-idf-en-v5.2.5-esp32.pdf` | **HTTP 206**, `application/pdf`, **`Content-Range: bytes 0-0/30789611`** ✅ |
| 2 | `https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32/index.html` | **HTTP 200**, `Content-Length: 9726` |
| 3 | `http://web.archive.org/web/20251219215035/https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32/esp-idf-en-v5.2.5-esp32.pdf` | **HTTP 200** — Wayback capture, 2025-12-19 |
| 4 | `https://github.com/espressif/esp-idf/releases/tag/v5.2.5` | **HTTP 200** |

> v5.2.5 is retained in the record as *the newest ESP-IDF release for which Espressif publishes a PDF build at all* — see the [Espressif vendor guide](../../../../vendors/espressif/README.md).

---

## 3. `esp-adf-programming-guide.pdf`

| Field | Value |
|---|---|
| **Original path** | `components/espressif/esp32-u4wdh/artifacts/esp-adf-programming-guide.pdf` |
| **What it is** | **Espressif Audio Development Framework (ESP-ADF) Guide** — audio element/pipeline framework, streams, codecs, Bluetooth audio services, audio board references |
| **Title (PDF metadata)** | "Espressif Audio Development Framework Guide"; Author "Espressif Systems" |
| **Version** | Release **`latest`** (i.e. the **`master`** branch build) — ⚠ **not a versioned release** |
| **Byte size** | **25 732 191** |
| **SHA-256** | `ed250ded5ae0174ec9b5ba8e4944641f057dd24e1441b5dee37b1a76fe242e61` |
| **Page count** | **495** |
| **Publication date** | Title page states **Jul 31, 2026**; PDF `CreationDate` 2026-07-30 20:56:21; server `Last-Modified: Fri, 31 Jul 2026 01:56:22 GMT` |
| **Why removal was OK** | The canonical URL currently serves a file of **exactly 25 732 191 bytes**, byte-identical in size to the local copy, plus a Wayback capture and the full documentation source in Git. |

> ⚠ **Moving-target caveat.** Because this is a `master` build, URL 1 will serve a *newer* document as ESP-ADF develops. It will not reproduce this exact 2026-07-31 build indefinitely. Mitigations: (a) the Wayback capture below, (b) a **fresh Wayback save was submitted 2026-08-24 (HTTP 200)** capturing this build, (c) the documentation source is in Git and this build is reproducible from it.

**Verified download URLs** (checked 2026-08-24):

| # | URL | Result |
|---|---|---|
| 1 | `https://docs.espressif.com/projects/esp-adf/en/latest/esp-adf-en-master.pdf` | **HTTP 206**, `application/pdf`, **`Content-Range: bytes 0-0/25732191`** ✅ size matches exactly; `Last-Modified: Fri, 31 Jul 2026 01:56:22 GMT` |
| 2 | `https://docs.espressif.com/projects/esp-adf/en/latest/index.html` | **HTTP 200**, `Content-Length: 8460` — HTML docs root (this is where URL 1 was discovered; the guide links it as `./esp-adf-en-master.pdf`) |
| 3 | `http://web.archive.org/web/20251117093334/https://docs.espressif.com/projects/esp-adf/en/latest/esp-adf-en-master.pdf` | **HTTP 200** — Wayback capture, 2025-11-17 (an **earlier** master build) |
| 4 | `https://github.com/espressif/esp-adf` | **HTTP 200** — documentation source under `docs/` |

> **Note on the URL:** the ADF PDF is **target-agnostic** — `esp-adf-en-master.pdf`, with no `-esp32` suffix. Guessing `.../esp-adf-en-master-esp32.pdf` or `.../esp32/esp-adf-en-master-esp32.pdf` returns **HTTP 404**. Both wrong forms were probed on 2026-08-24.

---

## What was extracted, and where it now lives

Knowledge mining was done with `pdftotext -layout` before archiving. Every extracted fact carries a page citation back to the specific build recorded above.

| New document | Captures |
|---|---|
| [`guides/espressif/esp-adf-audio-pipelines.md`](../../../../guides/espressif/esp-adf-audio-pipelines.md) | The full ESP-ADF extraction: the Element→Pipeline→ringbuffer architecture and its seven element callbacks; the Bluetooth service's HFP/A2DP/AVRCP profile set and its complete API surface (`bluetooth_service_start`, `bluetooth_service_create_stream`, the `periph_bluetooth_*` AVRCP passthrough commands); the `audio_hal` codec abstraction and the list of codec chips with in-tree drivers; **the audio memory-budget table** (Bluetooth = 140 kB internal RAM without PSRAM vs 95 kB with, against a 290 kB baseline) and the internal-RAM optimisation rules; recommended system settings; the full stream/codec element inventory. Also records that **ESP-ADF has no ESP32-P4 support**. |
| [`guides/espressif/esp-idf-peripheral-capabilities.md`](../../../../guides/espressif/esp-idf-peripheral-capabilities.md) | The ESP32-vs-S3-vs-P4 extraction from the two ESP-IDF guides above (plus the S3 and P4 builds): peripheral instance counts stated numerically, the LEDC high-speed-mode divergence, SDMMC slot differences and the ESP32 `HS1_*`/SPI-flash pin conflict, PDM-TX restrictions, and the **ESP32 PSRAM constraints** — the 1.8 V/3.3 V MTDI hazard that "can damage the PSRAM and/or flash chip", and the 64 Mbit `CONFIG_SPIRAM_2T_MODE` silicon-bug workaround that halves usable PSRAM. It also records the important negative finding that **the IDF guide renders `SOC_*` peripheral counts symbolically**, so the retained TRMs remain authoritative for RMT/PCNT/MCPWM/timer counts. |

Cross-linked from the [ESP32-U4WDH component record](../README.md).

## What was deliberately **not** archived from this directory

Retained because they are the scarce, high-value primary sources: `esp32-datasheet.pdf`, `esp32-technical-reference-manual.pdf` (+ Waveshare mirrors), `esp32-errata.pdf`, `esp32-hardware-design-guidelines.pdf`, `esp32-mini-1-mini-1u-datasheet.pdf`, `esp32-chip-revision-v3-0-user-guide.pdf`, `pcn-2021-021-esp32-u4wdh-dual-core.pdf`, `pcn20220901-esp32-chip-revision-upgrade.pdf`, `ar2022-003-esp32-v3-aes-fault-injection-advisory.pdf`, `ar2022-005-chip-revision-numbering-scheme.pdf`.
