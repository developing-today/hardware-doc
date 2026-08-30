# Wiki resource links — complete URL inventory

Retrieved **2026-08-21**; re-verified against the live page **2026-08-23** (still revision 111069; link set unchanged).

Source: Waveshare wiki [ESP32-S3-Knob-Touch-LCD-1.8](https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8), **section 8 "Resources"** in full — including **8.6 Software Tools**, **8.7 Other Resource Links** and **8.8 Project Resources** — plus every outbound URL appearing anywhere else in the page body.

This page is an **inventory**, not an endorsement. Every URL the vendor publishes is listed with what it is, whether we hold a local copy, and how to reacquire it. Community projects get technical assessment in **[examples/catalog.md](examples/catalog.md)**; this page records only what Waveshare itself links.

Retrieval date for every row below: **2026-08-21** unless stated otherwise.

---

## 8.1–8.5 Vendor downloadables

| # | Title | URL | Local artifact | Validated |
|---|---|---|---|---|
| 8.1 | Schematic diagram (ZIP) | `https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` | `artifacts/originals/…-schematic.zip` | yes — ZIP, 5 PNGs extracted |
| 8.2 | Demo archive (ZIP) | `https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` | `artifacts/originals/…-Demo.zip` | yes — Arduino + ESP-IDF trees, ~69 MB |
| 8.3 | Factory BIN files (ZIP) | `https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip` | `artifacts/originals/…-BIN.zip` | yes — 2 merged images, ~2 MB |
| 8.4 | **AIDA64 configuration file** | `https://files.waveshare.com/wiki/common/Aida_remote_1.85.zip` | `artifacts/tools/Aida_remote_1.85.zip` | yes — 475 B ZIP; contents analysed below |
| 8.5 | Seven IC datasheets (see below) | `files.waveshare.com/wiki/common/…` | `artifacts/datasheets/` | yes — all seven PDFs |

### 8.4 note — the AIDA64 file is legitimately tiny

At **475 bytes** this looks like a truncated download, so we verified it: it is a valid ZIP containing a single CRLF text file `aida_remote_1.85/aida_remote_1.85.rslcd`, an AIDA64 RemoteSensor layout declaring `<LCDVER>200</LCDVER><SWVER>6.33.5741 Beta</SWVER>` and eight sensor slots. Its contents are broken out in [factory-demo-apps.md §3.1](factory-demo-apps.md). **Not a failed retrieval.**

Note the filename says `1.85` — that is the **AIDA64 config revision**, not the 1.85-inch sibling board. The file is shared across Waveshare products (it lives under `wiki/common/`).

### 8.5 Datasheets

| Title | URL | Local |
|---|---|---|
| ESP32-S3 Series Datasheet | `https://files.waveshare.com/wiki/common/Esp32-s3_datasheet_en.pdf` | `components/espressif/esp32-s3r8/artifacts/esp32-s3-datasheet-v1.6-waveshare-mirror.pdf` (v1.6) |
| ESP32-S3 Technical Reference Manual | `https://files.waveshare.com/wiki/common/Esp32-s3_technical_reference_manual_en.pdf` | `components/espressif/esp32-s3r8/artifacts/esp32-s3-technical-reference-manual-v1.2-waveshare-mirror.pdf` (v1.2) |
| ESP32 Datasheet | `https://files.waveshare.com/wiki/common/Esp32_datasheet_en.pdf` | `components/espressif/esp32-u4wdh/artifacts/esp32-datasheet-v4.9-waveshare-mirror.pdf` (v4.9) |
| ESP32 Technical Reference Manual | `https://files.waveshare.com/wiki/common/Esp32_technical_reference_manual_en.pdf` | `components/espressif/esp32-u4wdh/artifacts/esp32-technical-reference-manual-v5.4-waveshare-mirror.pdf` (v5.4) |
| PCM5100A datasheet | `https://files.waveshare.com/wiki/common/Pcm5100a.pdf` | `components/texas-instruments/pcm5100a/artifacts/pcm5100a-datasheet-zhcsa60c-zh-waveshare-mirror.pdf` (`ZHCSA60C`, Chinese) |
| DRV2605 datasheet | `https://files.waveshare.com/wiki/common/Drv2605.pdf` | `components/texas-instruments/drv2605/artifacts/drv2605-datasheet-slos825-2025-06-02.pdf` (`ZHCSCW9E`, Chinese, **non-L part**) |
| CST816 Datasheet | `https://files.waveshare.com/wiki/common/CST816D_datasheet_En_V1.3.pdf` | `components/hynitron/cst816d/artifacts/cst816d-datasheet-v1.3.pdf` (deduplicated) |

These are Waveshare's **mirrors**. Manufacturer originals are held under `components/` and are preferred for citation; the mirrors are retained to document what the vendor actually ships. Two naming imprecisions worth noting: the board carries a **DRV2605L** (Waveshare links the non-L datasheet) and a **CST816D** (linked as "CST816").

---

## 8.6 Software Tools

Four subsections. **All now held locally.**

### 8.6.1 Arduino

| Title | URL | Local | Notes |
|---|---|---|---|
| Arduino IDE official download | `https://www.arduino.cc/en/software/` | link only | Version-mutable; no pinned version given |
| ESP32-Arduino official documentation | `https://docs.espressif.com/projects/arduino-esp32/en/latest/index.html` | link only | `latest`, not pinned — while the wiki requires core **≥ 3.2.0** |
| **Arduino-ESP32 offline component package** | `https://drive.google.com/drive/folders/1Pcs_A4FKWvdSHnz9lEBYqOpr-noTMbIv?usp=sharing` | **not retained** | **Google Drive folder.** See warning below |

> ⚠️ **The offline board package is hosted on a personal Google Drive folder.** It is not a Waveshare-controlled URL, has no version pinning, no checksum, and no guarantee of continued existence. It is the vendor's recommended fallback for users who cannot reach Espressif's servers.
>
> **We did not retain it.** A Drive *folder* has no stable direct-download URL, its contents change without notice, and mirroring an unversioned toolchain of unknown provenance is not a defensible artifact. **Prefer online installation from Espressif's own board-manager URL.** If you must use this, verify what you download against Espressif's published releases before running it.

### 8.6.2 VScode

| Title | URL | Local |
|---|---|---|
| VScode official website | `https://code.visualstudio.com/download` | link only — version-mutable installer |

### 8.6.3 Firmware Flashing Tool

| Title | URL | Local | Validated |
|---|---|---|---|
| Flash_download_tool | `https://dl.espressif.com/public/flash_download_tool.zip` | `artifacts/tools/flash_download_tool.zip` | **yes — acquired 2026-08-23** |

**Acquired this pass** (25,943,693 bytes; SHA-256 `c1fbf280aa04cd8fbe725bff74360fb0a7c83fbd49afcaf37f6c14a6575ea9bc`). Contains `flash_download_tool_3.9.11.exe` (26,519,970 bytes, dated 2026-06-03) plus `bin/`, `combine/`, `configure/`, `efuse_dump/`, `flash_dump/`, `secure/` directories.

Espressif's official **Windows-only GUI** flasher. The URL is **unversioned and mutable** — it always serves current, so the hash above pins *what we retrieved*, not a stable release. The version is discoverable only from the inner `.exe` filename.

Note the wiki links this tool but its own §7 "BIN File Flashing" walkthrough uses **command-line `esptool`** instead. `esptool` is cross-platform, scriptable, and what every community project uses; prefer it. See [factory-firmware.md](factory-firmware.md).

### 8.6.4 FFmpeg

| Title | URL | Local | Validated |
|---|---|---|---|
| FFmpeg tool v2.1 | `https://files.waveshare.com/wiki/common/mjpeg%20Conversion%20tool%20V2.1.zip` | `artifacts/tools/mjpeg_Conversion_tool_V2.1.zip` | yes — 81,719,210 B ZIP |

Despite the section title this is **not** upstream FFmpeg — it is Waveshare's **.NET GUI wrapper bundling** `ffmpeg.exe` and `ffprobe.exe`. Windows-only; internal filenames are GB2312-encoded Chinese. Contents and a plain-FFmpeg replacement command are in [factory-demo-apps.md §4](factory-demo-apps.md).

### 8.6.5 Debugging Tool — *commented out in the source*

The wikitext contains a **commented-out** subsection:

~~~
<!--===Debugging Tool===
*[https://files.waveshare.com/wiki/common/Sscom5.13.1.zip SSCOM debugging assistant]-->
~~~

Not rendered on the live page, so a reader would never see it. The URL still resolves and we hold it at `artifacts/tools/Sscom5.13.1.zip` (420,199 bytes). SSCOM is a Chinese-language Windows serial terminal. Recorded for completeness; there is no reason to prefer it over `idf.py monitor`, `screen` or `minicom`.

*(A second commented-out block elsewhere in the wikitext hides an entire **MicroPython** development-tools entry — see [development.md](development.md). MicroPython is **not** offered for this board.)*

---

## 8.7 Other Resource Links

The vendor's entire section 8.7 is **one link**:

| Title | URL | What it is | Local |
|---|---|---|---|
| LVGL official documentation | `https://docs.lvgl.io/master/intro/introduction/index.html` | LVGL embedded GUI library docs | link only |

> ⚠️ **Version mismatch.** This points at **`master`** (currently LVGL 9.x). The board's demo archive bundles and requires **LVGL 8.4.0**, which the wiki's own library table states. LVGL 9 changed a great deal of the widget and display-driver API. **Use <https://docs.lvgl.io/8.4/> instead** when working with the official examples. The same `master` link is repeated in two `{{Note}}` boxes attached to the `08_LVGL_Test` demos.

---

## 8.8 Project Resources — third-party projects

The vendor's own disclaimer, quoted verbatim:

> "This section features third-party project resources. We merely provide links and bear no responsibility for content updates or maintenance. Thank you for your understanding."

**Nine entries.** Presented here as the vendor presents them; technical assessment, licences, pinned commits and build notes are in **[examples/catalog.md](examples/catalog.md)**.

| # | Attribution as given by Waveshare | Type | URL |
|---|---|---|---|
| 1 | **Volos Projects** — "Why This 1.8" Knob Board Is Perfect for Remote Projects" | YouTube | `https://www.youtube.com/watch?v=8pHF0OAG2TI` |
| | | GitHub | `https://github.com/VolosR/Knob18Meters` |
| 2 | **iHayri1** — "ESP32-S3 1.8" Knob Display, unboxing, review and Combination Lock example" | YouTube | `https://www.youtube.com/watch?v=d2aSVfH3RDM` |
| | | GitHub | `https://github.com/ihayri/ESP32-S3-1.8inch-Knob-Display-Development-Board` |
| 3 | **Muness** — "ESP32-S3 Knob Hifi Controller" | Forum ① | `https://community.roonlabs.com/t/50-esp32-s3-knob-hifi-controller/311363` |
| | | Forum ② | `https://forums.lyrion.org/forum/user-forums/3rd-party-hardware/1804977-roon-knob-includes-lms-support` |
| | | GitHub | `https://github.com/muness/roon-knob` |
| 4 | **That Project** — "The Ultimate Animated Face for ESP32 \| 17+ Expressions" | YouTube | `https://www.youtube.com/watch?v=iCm50dTcAtc` |
| | | GitHub | `https://github.com/0015/lvgl_kawaii_face` |
| 5 | **Mat** — "a hobby project for a round ESP32 to create a life counter for trading card games like MTG" | GitHub | `https://github.com/knobby-mtg/knobby-mtg-life-counter` |
| 6 | **Anton Belo** — "Magic: The Gathering life & counter tracker for the Waveshare ESP32-S3-Knob-Touch-LCD-1.8 round knob display" | GitHub | `https://github.com/juggernautwins608/Waveshare-1.8-Magic-the-Gathering-Life-Counter` |
| 7 | **Embedded Wizard** — "GUI Demo on Espressif ESP32-S3" | YouTube | `https://www.youtube.com/watch?v=hxJjh68Yqro` |
| | | GitHub | `https://github.com/EmbeddedWizardGUI/ESP32-S3-Knob-Touch-LCD-1.8-EN` |
| 8 | **Eric Haight** — "Planes above you, on your desk, all day" | YouTube (Short) | `https://www.youtube.com/shorts/44ysoSGY22M` |
| | | Guide | `https://deskrad.com/` |
| 9 | **Chris Meyer** — "Standalone bedside dial for Orion Sleep toppers" | GitHub | `https://github.com/chris023/orion-waveshare-rotary-dial` |

Observations on the list as a set:

- **Eight GitHub repos, five YouTube videos, two forum threads, one standalone site.** Entries 5, 6 and 9 are repo-only; entry 8 is the only one with no repository at all.
- **Two independent MTG life counters** (5 and 6) — the round form factor is evidently compelling for tabletop gaming counters, and a third, `jeager/arcmind-life-counter`, exists but is not listed by Waveshare.
- **`deskrad.com` (entry 8) is a commercial product site**, not a project write-up, and the name collides with several unrelated GitHub repos. Treat with care.
- **The list is substantially incomplete.** A GitHub search on 2026-08-23 found **28** board-specific repositories against Waveshare's eight — including the highest-value ones for anybody doing serious work here (ESPHome support, secondary-MCU firmware, display-driver resolution). See [examples/catalog.md](examples/catalog.md).

---

## Outbound links elsewhere in the page body

Not in section 8, but referenced in the walkthroughs. All link-only.

| Context | Title | URL |
|---|---|---|
| §2 Lithium Battery Installation | Embedded YouTube video (the **entire** section content) | `https://www.youtube.com/watch?v=RUIXx_-BYDg` |
| §4 intro + §9 FAQ 2 | **Volos usage demonstration** — *different video from 8.8 entry 1* | `https://www.youtube.com/watch?v=5G4W3irHkks` |
| §4.2.1 AIDA64 | AIDA64 official website | `https://www.aida64.com/` |
| §5.1.1 | Arduino official website (software) | `https://www.arduino.cc/en/software` |
| §5.1.1 note | Arduino-esp32 environment setup | `https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html` |
| §5.1.2 | Waveshare **Arduino Board Managers Tutorial** | `https://www.waveshare.com/wiki/Arduino_Board_Managers_Tutorial` |
| §5.1.3 | Waveshare **Arduino Library Manager Tutorial** | `https://www.waveshare.com/wiki/Arduino_Library_Manager_Tutorial` |
| §5.2 / §6.2 notes | Arduino-ESP32 SD library | `https://github.com/espressif/arduino-esp32/tree/master/libraries/SD` |
| §6.1.1 | VScode download | `https://code.visualstudio.com/download` |
| §6.1.1 note | **ESP-IDF v5.1.4** Windows setup — *the only pinned IDF version on the page* | `https://docs.espressif.com/projects/esp-idf/en/v5.1.4/esp32s3/get-started/windows-setup.html` |
| §6.1.2 | Waveshare **Install Espressif IDF Plugin Tutorial** | `https://www.waveshare.com/wiki/Install_Espressif_IDF_Plugin_Tutorial` |
| §7 BIN flashing | pip bootstrap | `https://bootstrap.pypa.io/get-pip.py` |
| §9 FAQ 9 | **CH34x macOS driver** | `https://files.waveshare.com/wiki/common/CH34XSER_MAC.7z` — held at `artifacts/tools/CH34XSER_MAC.7z` |
| §9 FAQ 11 | Waveshare **SquareLine Studio tutorial** | `https://www.waveshare.com/wiki/Waveshare_SquareLine_Studio` |
| Infobox | Product storefront page | `https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm` |

The five Waveshare `wiki/*_Tutorial` pages are **generic, shared across products, and separately mutable**. They are not snapshotted here; nothing board-specific depends on them.

---

## Retrieval failures and things deliberately not retained

Recorded so a future pass does not repeat the work.

| Item | Status | Detail |
|---|---|---|
| **Arduino-ESP32 offline component package** | **not retained — deliberate** | Google Drive *folder* (`1Pcs_A4FKWvdSHnz9lEBYqOpr-noTMbIv`). No stable direct-download URL, no version, no checksum, third-party-controlled. Use Espressif's board manager instead. |
| **Waveshare wiki `api.php`** | **broken server-side, 2026-08-23** | Every `api.php` query now returns a PHP fatal: `Parse error: syntax error, unexpected '?' in /yundisk/web/waveshare/dotcom/w/includes/Setup.php on line 472`. The **rendered page still works** (HTTP 200). This is a vendor-side regression since the 2026-08-21 pass, when the API path was the *recommended* workaround for the `oldid` WAF block. **Both documented retrieval routes for pinned revisions are now unavailable.** Our existing wikitext snapshot is therefore the authoritative local copy. Update [`vendors/waveshare/README.md`](../../../vendors/waveshare/README.md) accordingly. |
| `index.php?title=…&action=raw` | **blocked** | Returns 99 bytes of the same PHP parse error. |
| Guition **JC3636K518CN_knob_EN.zip** (clone-board vendor source) | **failed** | `pan.jczn1688.com` is a JavaScript file-manager; direct link returns 11,275 B of HTML, and Cloudreve API paths return `{"detail":"Not Found"}`. Would need a real browser session. See [examples/catalog.md](examples/catalog.md) for why this matters and the reacquisition command. |
| `nkinnan/manufacturer-firmware-and-sd-card-contents_Waveshare-…` | **empty repository** | API reports `size: 0` and **no branches**. The promised as-shipped SD-card contents were never pushed. The **Guition** sibling repo *does* have content (327 MB). |

### Reacquisition commands

~~~sh
# Vendor downloadables (stable URLs)
curl -L -O https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip
curl -L -O https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip
curl -L -O https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip
curl -L -O https://files.waveshare.com/wiki/common/Aida_remote_1.85.zip
curl -L -O "https://files.waveshare.com/wiki/common/mjpeg%20Conversion%20tool%20V2.1.zip"
curl -L -O https://files.waveshare.com/wiki/common/CH34XSER_MAC.7z
curl -L -O https://dl.espressif.com/public/flash_download_tool.zip   # mutable: always current

# Wiki page. api.php is broken as of 2026-08-23; rendered HTML is the only route.
curl -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36" \
     -o waveshare-wiki-current.html https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8

# Clone-board vendor source — needs a browser session, not curl
#   https://pan.jczn1688.com/s/54f682   (file: JC3636K518CN_knob_EN.zip)
~~~

---

## Cross-references

- [sources.md](sources.md) — the full source manifest with hashes
- [examples/catalog.md](examples/catalog.md) — third-party projects, assessed
- [factory-demo-apps.md](factory-demo-apps.md) — what the AIDA64 and MJPEG tools are for
- [faq-and-troubleshooting.md](faq-and-troubleshooting.md) — vendor FAQ
- [development.md](development.md) — toolchain versions
- [Waveshare documentation-sourcing guide](../../../vendors/waveshare/README.md) — URL patterns and API quirks
