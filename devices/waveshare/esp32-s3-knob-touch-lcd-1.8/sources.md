# Source manifest

Every source was retrieved or checked on **2026-08-21**. Local paths are relative to this device folder unless noted. A dash means link-only.

| Title | URL | Publisher | Retrieved | Version/date | Local artifact | Notes |
|---|---|---|---:|---|---|---|
| ESP32-S3 1.8inch Knob Display product page, ID 31623 | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | Waveshare | 2026-08-21 | live page | `artifacts/source-snapshots/waveshare-product-31623.html` | Identity, options, specs, dimensions |
| ESP32-S3-Knob-Touch-LCD-1.8 Wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | Waveshare | 2026-08-21 | live page | `artifacts/source-snapshots/waveshare-wiki-current.html` | Setup, examples, FAQ, resources |
| Immutable wiki revision 111069 | https://www.waveshare.com/w/api.php?action=parse&oldid=111069&prop=text\|wikitext\|revid | Waveshare | 2026-08-21 | revid 111069, 2026-08-07T13:19:04Z | `artifacts/source-snapshots/waveshare-wiki-oldid-111069.html`, `...-parse.json`, `waveshare-wiki-wikitext-oldid-111069.txt` | `index.php?oldid=` returns HTTP 404 (WAF); the API path works. See [vendor guide §1](../../../vendors/waveshare/README.md) |
| Official schematic ZIP | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip | Waveshare | 2026-08-21 | undated | `artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` | SHA-256 baa5ac...; five extracted PNGs |
| Official demo ZIP | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip | Waveshare | 2026-08-21 | LVGL 8.4.0; SensorLib 0.3.1 | `artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` | Complete Arduino + ESP-IDF source, licenses retained. **Also contains both factory firmware images** under `Firmware/` — a second source for them; see [factory firmware](factory-firmware.md#provenance-where-each-binary-comes-from-and-its-fallback) |
| Official factory BIN ZIP | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip | Waveshare | 2026-08-21 | S3 V1.2 / builds 2025-02-28 and 2025-04-18 | `artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip` | Two merged images; byte-identical to the copies in the Demo ZIP. Preferred download (2 MB vs 69 MB) |
| Official dimension image | https://www.waveshare.com/w/upload/9/9d/ESP32-S3-Knob-Touch-LCD-1.8-14.jpg | Waveshare | 2026-08-21 | undated | `artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-14.jpg` | 66 x 22 mm |
| ESP32-S3 datasheet | https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf | Espressif | 2026-08-21 | live manufacturer document | `../../../components/espressif/esp32-s3r8/artifacts/esp32-s3-datasheet.pdf` | Manufacturer original redirects to documentation host |
| ESP32-S3 TRM | https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf | Espressif | 2026-08-21 | live manufacturer document | `../../../components/espressif/esp32-s3r8/artifacts/esp32-s3-technical-reference-manual.pdf` | Manufacturer original |
| ESP32 datasheet | https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf | Espressif | 2026-08-21 | live manufacturer document | `../../../components/espressif/esp32-u4wdh/artifacts/esp32-datasheet.pdf` | Manufacturer original |
| ESP32 TRM | https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf | Espressif | 2026-08-21 | live manufacturer document | `../../../components/espressif/esp32-u4wdh/artifacts/esp32-technical-reference-manual.pdf` | Manufacturer original |
| ST77916 Specification | https://dl.espressif.com/AE/esp-iot-solution/ST77916_SPEC_V1.0.pdf | Sitronix via Espressif | 2026-08-21 | V1.0 | `../../../components/sitronix/st77916/artifacts/st77916-spec-v1.0.pdf` | Controller conflict noted |
| CST816D Datasheet | https://files.waveshare.com/wiki/common/CST816D_datasheet_En_V1.3.pdf | Hynitron via Waveshare | 2026-08-21 | English V1.3 | `../../../components/hynitron/cst816d/artifacts/cst816d-datasheet-v1.3.pdf` | Official board resource mirror |
| PCM5100A Datasheet | https://www.ti.com/lit/gpn/PCM5100A | Texas Instruments | 2026-08-21 | live datasheet | `../../../components/texas-instruments/pcm5100a/artifacts/pcm5100a-datasheet.pdf` | Manufacturer original |
| DRV2605L Datasheet | https://www.ti.com/lit/gpn/DRV2605L | Texas Instruments | 2026-08-21 | live datasheet | `../../../components/texas-instruments/drv2605l/artifacts/drv2605l-datasheet.pdf` | Manufacturer original |
| TLV62569 Datasheet | https://www.ti.com/lit/gpn/TLV62569 | Texas Instruments | 2026-08-21 | live datasheet | `../../../components/texas-instruments/tlv62569dbvt/artifacts/tlv62569-datasheet.pdf` | Manufacturer original |
| W25Q128JV Datasheet | https://www.winbond.com/resource-files/w25q128jv%20revf%2003272018%20plus.pdf | Winbond | 2026-08-21 | Rev F, file dated 2018-03-27 | `../../../components/winbond/w25q128jvpiq/artifacts/w25q128jv-datasheet-rev-f.pdf` | Manufacturer original |
| AO3400A Datasheet | https://www.aosmd.com/sites/default/files/res/datasheets/AO3400A.pdf | Alpha and Omega Semiconductor | 2026-08-21 | live datasheet | `../../../components/alpha-and-omega-semiconductor/ao3400a/artifacts/ao3400a-datasheet.pdf` | Manufacturer original |
| SSCM series PDF catalog | https://tech.alpsalpine.com/cms.media/product_catalog_sw_01_sscm_en_90b44d6d7f.pdf | Alps Alpine | 2026-08-21 | manufacturer catalog | `../../../components/alps-alpine/sscm110100/artifacts/sscm-series-catalog.pdf` | Validated PDF; includes SSCM110100 |
| CH445P manufacturer download attempt | https://www.wch.cn/downloads/file/337.html | WCH | 2026-08-21 | - | - | Returned JavaScript, rejected |
| SGM2036 product page | https://www.sg-micro.com/product/SGM2036 | SGMicro | 2026-08-21 | live page | - | Direct PDF URL returned HTTP 404 |
| SGM2036 direct PDF attempt | https://www.sg-micro.com/uploads/soft/20240814/1723624970.pdf | SGMicro | 2026-08-21 | URL path dated 2024-08-14 | - | Failed HTTP 404 |
| MSM261D4030H1CPM distributor PDF attempt | https://datasheet.lcsc.com/lcsc/1811081617_MEMSensing-MSM261D4030H1CPM_C74250.pdf | LCSC / MEMSensing | 2026-08-21 | URL path dated 2018-11-08 | - | Returned HTML, not retained as PDF |
| Arduino-ESP32 installation/API docs | https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html | Espressif | 2026-08-21 | required >=3.2.0 by Waveshare | - | Environment reference |
| ESP-IDF ESP32-S3 setup | https://docs.espressif.com/projects/esp-idf/en/v5.1.4/esp32s3/get-started/ | Espressif | 2026-08-21 | 5.1.4 | - | Official setup reference |
| LVGL documentation | https://docs.lvgl.io/8.4/ | LVGL project | 2026-08-21 | 8.4 | bundled source in demo | GUI API |
| SensorLib repository | https://github.com/lewisxhe/SensorLib | Lewis He | 2026-08-21 | bundled 0.3.1 | bundled in demo archive | License retained in archive |

Community repositories are link-only and recorded with branch, last push/update and license API fields in [community.md](community.md) and its local JSON metadata.

## Newly acquired 2026-08-21 (exhaustive Waveshare pass)

Enumerated from the pinned wiki **wikitext** (revid 111069) plus the storefront page and the
MediaWiki `imageinfo` API, per [`vendors/waveshare/README.md`](../../../vendors/waveshare/README.md).
All files validated by magic bytes.

### Waveshare-mirrored IC datasheets and reference manuals

| Title | URL | Publisher | Retrieved | Version | Local artifact | Notes |
|---|---|---|---:|---|---|---|
| CST816D touch controller datasheet (Waveshare mirror) | https://files.waveshare.com/wiki/common/CST816D_datasheet_En_V1.3.pdf | Hynitron via Waveshare | 2026-08-21 | English V1.3 | [`components/hynitron/cst816d/artifacts/cst816d-datasheet-v1.3.pdf`](../../../components/hynitron/cst816d/artifacts/cst816d-datasheet-v1.3.pdf) | **Relocated 2026-08-24.** Byte-identical duplicate of the components/ copy; device-side copy archived to `../hardware-doc-archive/`. 1098205 B, sha256 `a0b14a06ef5d8205` |
| DRV2605 haptic driver datasheet (Waveshare mirror) | https://files.waveshare.com/wiki/common/Drv2605.pdf | TI via Waveshare | 2026-08-21 | undated mirror | [`components/texas-instruments/drv2605/artifacts/drv2605-datasheet-slos825-2025-06-02.pdf`](../../../components/texas-instruments/drv2605/artifacts/drv2605-datasheet-slos825-2025-06-02.pdf) | **Relocated 2026-08-24.** Verified `ZHCSCW9E` (Chinese, rev. Apr 2018) — **DRV2605 non-L, wrong part**; board fits DRV2605L. Byte-identical duplicate; device-side copy archived. 2478601 B, sha256 `bd7549137c51d8b6` |
| ESP32-S3 datasheet (Waveshare mirror) | https://files.waveshare.com/wiki/common/Esp32-s3_datasheet_en.pdf | Espressif via Waveshare | 2026-08-21 | undated mirror | [`components/espressif/esp32-s3r8/artifacts/esp32-s3-datasheet-v1.6-waveshare-mirror.pdf`](../../../components/espressif/esp32-s3r8/artifacts/esp32-s3-datasheet-v1.6-waveshare-mirror.pdf) | **Relocated 2026-08-24.** Verified **v1.6**; components/ holds current v2.2. 1186331 B, sha256 `b79310e52e905999` |
| ESP32-S3 TRM (Waveshare mirror) | https://files.waveshare.com/wiki/common/Esp32-s3_technical_reference_manual_en.pdf | Espressif via Waveshare | 2026-08-21 | undated mirror | [`components/espressif/esp32-s3r8/artifacts/esp32-s3-technical-reference-manual-v1.2-waveshare-mirror.pdf`](../../../components/espressif/esp32-s3r8/artifacts/esp32-s3-technical-reference-manual-v1.2-waveshare-mirror.pdf) | **Relocated 2026-08-24.** Verified **v1.2**; components/ holds current v1.8. 14540185 B, sha256 `47bb075de167d816` |
| ESP32 datasheet (Waveshare mirror) | https://files.waveshare.com/wiki/common/Esp32_datasheet_en.pdf | Espressif via Waveshare | 2026-08-21 | undated mirror | [`components/espressif/esp32-u4wdh/artifacts/esp32-datasheet-v4.9-waveshare-mirror.pdf`](../../../components/espressif/esp32-u4wdh/artifacts/esp32-datasheet-v4.9-waveshare-mirror.pdf) | **Relocated 2026-08-24.** Verified **v4.9**; components/ holds current v5.3. ⚠ v4.9 predates the U4WDH dual-core correction. 991747 B, sha256 `608f5d36daa88db4` |
| ESP32 TRM (Waveshare mirror) | https://files.waveshare.com/wiki/common/Esp32_technical_reference_manual_en.pdf | Espressif via Waveshare | 2026-08-21 | undated mirror | [`components/espressif/esp32-u4wdh/artifacts/esp32-technical-reference-manual-v5.4-waveshare-mirror.pdf`](../../../components/espressif/esp32-u4wdh/artifacts/esp32-technical-reference-manual-v5.4-waveshare-mirror.pdf) | **Relocated 2026-08-24.** Verified **v5.4**; components/ holds current v5.8. 10220576 B, sha256 `e897ef6a5b1aaecd` |
| PCM5100A audio DAC datasheet (Waveshare mirror) | https://files.waveshare.com/wiki/common/Pcm5100a.pdf | TI via Waveshare | 2026-08-21 | undated mirror | [`components/texas-instruments/pcm5100a/artifacts/pcm5100a-datasheet-zhcsa60c-zh-waveshare-mirror.pdf`](../../../components/texas-instruments/pcm5100a/artifacts/pcm5100a-datasheet-zhcsa60c-zh-waveshare-mirror.pdf) | **Relocated 2026-08-24.** Verified `ZHCSA60C` — **Chinese translation**, same revision level as English SLAS859C (not an older revision). 1453455 B, sha256 `9822f33dad999bca` |

### PC tools referenced by the wiki

| Title | URL | Publisher | Retrieved | Version | Local artifact | Notes |
|---|---|---|---:|---|---|---|
| SSCOM serial terminal | https://files.waveshare.com/wiki/common/Sscom5.13.1.zip | Waveshare (mirror) | 2026-08-21 | 5.13.1 | `artifacts/tools/Sscom5.13.1.zip` | **Found only in wikitext**, absent from rendered HTML; 420199 B, sha256 `d85cce9c2494ec7d` |
| CH34x USB-serial driver (macOS) | https://files.waveshare.com/wiki/common/CH34XSER_MAC.7z | Waveshare (mirror) | 2026-08-21 | undated | `artifacts/tools/CH34XSER_MAC.7z` | WCH driver mirrored by Waveshare; 4123873 B, sha256 `c041275b27906b6b` |
| AIDA64 remote-panel assets | https://files.waveshare.com/wiki/common/Aida_remote_1.85.zip | Waveshare (mirror) | 2026-08-21 | 1.85 | `artifacts/tools/Aida_remote_1.85.zip` | For the PC-monitor demo; 475 B, sha256 `81f6d7c78f89fb48` |
| MJPEG conversion tool | https://files.waveshare.com/wiki/common/mjpeg%20Conversion%20tool%20V2.1.zip | Waveshare (mirror) | 2026-08-21 | V2.1 | `artifacts/tools/mjpeg_Conversion_tool_V2.1.zip` | URL contains literal spaces (%20); 81719210 B, sha256 `8db4252b99ed2766` |
| **Espressif Flash Download Tool** | https://dl.espressif.com/public/flash_download_tool.zip | Espressif | **2026-08-23** | archive contains `flash_download_tool_3.9.11.exe` | `artifacts/tools/flash_download_tool.zip` | Wiki §8.6.3. **URL is unversioned and mutable** — always serves current, so the hash pins only what we fetched. 25943693 B, sha256 `c1fbf280aa04cd8fbe725bff74360fb0a7c83fbd49afcaf37f6c14a6575ea9bc`. Windows-only GUI; the wiki's own §7 procedure uses `esptool` instead |

### Images

Per-file provenance (source page, direct URL, subject/view, bytes, sha256) is in
[`artifacts/images/MANIFEST.md`](artifacts/images/MANIFEST.md).

| Set | URL pattern | Retrieved | Files | Bytes | Local path |
|---|---|---:|---:|---:|---|
| Board-specific wiki images (photos, pinout, dimension & block diagrams) | `https://www.waveshare.com/w/upload/<a>/<ab>/ESP32-S3-Knob-Touch-LCD-1.8-*` | 2026-08-21 | 38 | 10825731 | `artifacts/images/wiki/` |
| Shared Waveshare tutorial figures embedded on this wiki page | `https://www.waveshare.com/w/upload/...` | 2026-08-21 | 39 | 2557172 | `artifacts/images/wiki-shared/` |
| Storefront gallery photos (800x800) | `https://www.waveshare.com/media/catalog/product/cache/1/image/800x800/.../esp32-s3-knob-touch-lcd-1.8-N.jpg` | 2026-08-21 | 5 | 231568 | `artifacts/images/product-page/` |

**Rights:** all Waveshare images are Waveshare's property, published without an explicit license.
Redistribution rights are **unclear**; retained for internal engineering reference only.

### Additional page snapshots

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Wiki page at pinned revision 111069 (rendered) | `api.php?action=parse&oldid=111069` | 2026-08-21 | `artifacts/source-snapshots/waveshare-wiki-oldid-111069.html` |
| Wiki raw wikitext at revision 111069 | `api.php?action=parse&oldid=111069&prop=wikitext` | 2026-08-21 | `artifacts/source-snapshots/waveshare-wiki-wikitext-oldid-111069.txt` |
| Wiki revision history (100 revisions) | `api.php?action=query&prop=revisions&rvlimit=100` | 2026-08-21 | `artifacts/source-snapshots/waveshare-wiki-history-2026-08-21.json` |
| Wiki page re-fetch (live) | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `artifacts/source-snapshots/waveshare-wiki-current-2026-08-21.html` |
| Storefront product page re-fetch (live) | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | 2026-08-21 | `artifacts/source-snapshots/waveshare-product-31623-2026-08-21.html` |
| MediaWiki imageinfo for all 77 page images | `api.php?action=query&prop=imageinfo` | 2026-08-21 | `artifacts/source-snapshots/wiki-imageinfo-2026-08-21.json` |

See [`vendors/waveshare/README.md`](../../../vendors/waveshare/README.md) for the reusable
sourcing procedure, URL patterns and gotchas that produced this manifest.

## Factory firmware source coverage (verified 2026-08-22)

The two factory firmware binaries are the most restore-critical artifacts here, so their sourcing is
tracked explicitly rather than implicitly through the archives that carry them.

| Binary | Target MCU | Bytes | SHA-256 | Archive 1 | Archive 2 |
|---|---|---:|---|---|---|
| `ESP32-KNOB_ESP32_0.bin` | ESP32-U4WDH | 1130672 | `0c1c21b9822d4c2d80d58534b33eb0083880de4ed7354a38b4c78ba51757349d` | `-BIN.zip` | `-Demo.zip` (`Firmware/`) |
| `WX-ESP32S3-KNOB_V1.2.bin` | ESP32-S3R8 | 2138224 | `f7c1cc18b687559f3bd69e5c9ab526bc61c2b2d9c502f38367f7f2bfe4ff8e87` | `-BIN.zip` | `-Demo.zip` (`Firmware/`) |

Both archive URLs were re-checked live on 2026-08-22 (HTTP 200, `application/zip`), and both archives were
re-extracted and re-hashed locally to confirm the members are byte-identical across them.

Publishing pages recorded as sources for the firmware: the [wiki page](https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8),
the pinned-revision `api.php?action=parse&oldid=111069` URL, and the
[product page](https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm) — rows 7-9 of the table above.

**No mirrors exist.** Wayback has no snapshot of either ZIP, and the alternative Waveshare path forms
(`files.waveshare.com/upload/`, `www.waveshare.com/w/upload/`, `wiki/File:`) all return HTTP 404.
The local copies in `artifacts/originals/` are the only offline guarantee.
Full detail, including build metadata, IDF versions and per-archive member paths, is in
[factory-firmware.md](factory-firmware.md#provenance-where-each-binary-comes-from-and-its-fallback).

## ESP32-U4WDH silicon revision (added 2026-08-21)

Sources backing the claim that this board's secondary MCU is chip revision **v3.1**, and the summary
subsection in [`README.md`](README.md#the-secondary-mcu-is-silicon-revision-v31). The full matrix,
the per-revision errata table and the retrieval notes live in
[§21 of the component page](../../../components/espressif/esp32-u4wdh/README.md#21-silicon-revisions-the-complete-matrix-and-what-v31-means);
this table records only what a device-level reader needs to re-verify the claim.

| Source | URL | Publisher | Retrieved | Version | Local artifact |
|---|---|---|---:|---|---|
| **PCN20220901 — Upgrade Chip Revision of ESP32 Series Products** (announces v3.0 → v3.1; names ESP32-U4WDH in Category 2) | https://www.espressif.com/sites/default/files/pcn_downloads/PCN20220901%20Upgrade%20Chip%20Revision%20of%20ESP32%20Series%20Products.pdf | Espressif | 2026-08-21 | ESP-07-2-007-03 v1.4, issued 2022-10-25 | `../../../components/espressif/esp32-u4wdh/artifacts/pcn20220901-esp32-chip-revision-upgrade.pdf` |
| **AR2022-005 — Compatibility Advisory for Chip Revision Numbering Scheme** (ECO → `vM.X`) | https://www.espressif.com/sites/default/files/advisory_downloads/AR2022-005%20Compatibility%20Advisory%20for%20Chip%20Revision%20Numbering%20%20Scheme.pdf | Espressif | 2026-08-21 | v1.0, 2022-09-29 | `../../../components/espressif/esp32-u4wdh/artifacts/ar2022-005-chip-revision-numbering-scheme.pdf` |
| **AR2022-003 — Security Advisory: Breaking the Hardware AES Core and Firmware Encryption of ESP32 Chip Revision v3.0** | https://www.espressif.com/sites/default/files/advisory_downloads/AR2022-003%20Security%20Advisory%20Concerning%20Breaking%20the%20Hardware%20AES%20Core%20and%20Firmware%20Encryption%20of%20ESP32%20Chip%20Revision%20v3.0%20-%20V2.0%20EN.pdf | Espressif | 2026-08-21 | V2.0, 2022-11-18 | `../../../components/espressif/esp32-u4wdh/artifacts/ar2022-003-esp32-v3-aes-fault-injection-advisory.pdf` |
| **ESP32 Series SoC Errata — HTML build** (per-revision errata matrix, eFuse and marking identification tables) | https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/ | Espressif | 2026-08-21 | doc v3.0, 2025-10-11 | PDF form: `../../../components/espressif/esp32-u4wdh/artifacts/esp32-errata.pdf` |
| **ESP32 Chip Revision v3.0 User Guide** (the seven ECO3 design changes) | https://documentation.espressif.com/esp32_chip_revision_v3_0_user_guide_en.pdf | Espressif | 2026-08-21 | v1.3, 2022.11 | `../../../components/espressif/esp32-u4wdh/artifacts/esp32-chip-revision-v3-0-user-guide.pdf` |
| ESP32 Series Datasheet — HTML build (Table 1-1: `ESP32-U4WDH … v3.0/v3.1`, footnote 4 → PCN20220901) | https://documentation.espressif.com/esp32_datasheet_en.html | Espressif | 2026-08-21 | v5.3 | `../../../components/espressif/esp32-u4wdh/artifacts/esp32-series-datasheet-v5.3.html` |
| ESP-IDF Programming Guide — Chip Revision (versioning scheme, compatibility checks, `efuse_hal_*`) | https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/chip_revision.html | Espressif | 2026-08-21 | `latest` | - |
| ESP-IDF `esp_hw_support/port/esp32/Kconfig.hw_support` (the only public source mapping **ECO4 ≡ v3.1**) | https://github.com/espressif/esp-idf/blob/master/components/esp_hw_support/port/esp32/Kconfig.hw_support | Espressif | 2026-08-21 | `master` | - |
| esptool `esptool/targets/esp32.py` (revision decode and the `(revision v3.1)` output format) | https://github.com/espressif/esptool/blob/master/esptool/targets/esp32.py | Espressif | 2026-08-21 | `master` | - |

All three new PDFs were validated on `%PDF` magic bytes at download. PCN20220901 and AR2022-005 were
additionally submitted to `web.archive.org/save/` on 2026-08-21 (both accepted): they are single-copy
Espressif-hosted documents with no mirrors found, and PCN20220901's filename cannot be guessed — it has
to be enumerated from https://www.espressif.com/en/support/documents/pcns.

## Section 4/8/9 mining pass (2026-08-23)

The 2026-08-21 pass captured the wiki's hardware and example content. This pass mined the sections it had
not used: **§3 Development Tools**, **§4 Comprehensive Example Usage Instructions**, **§8.6 Software Tools**,
**§8.7 Other Resource Links**, **§8.8 Project Resources** and **§9 FAQ**. Outputs are
[factory-demo-apps.md](factory-demo-apps.md), [faq-and-troubleshooting.md](faq-and-troubleshooting.md),
[wiki-resource-links.md](wiki-resource-links.md) and [examples/catalog.md](examples/catalog.md).

### Live re-fetch result

| Check | Result |
|---|---|
| `https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8` re-fetched **2026-08-23** | HTTP 200, 134,571 B |
| Revision | **still 111069** (`wgCurRevisionId` / `wgRevisionId`) |
| Content diff vs `waveshare-wiki-current-2026-08-21.html` | **No content differences.** Only the MediaWiki parser-cache timestamp, `wgRequestId`, Cloudflare challenge nonce and template CPU timings differ |

**The 2026-08-21 snapshot is current.** Nothing on the live page was missed by the snapshot, and the
retained wikitext (`artifacts/source-snapshots/waveshare-wiki-wikitext-oldid-111069.txt`, 999 lines)
remains the authoritative local copy — which matters, because both API retrieval routes have since broken:

> ⚠️ **`api.php` is broken server-side as of 2026-08-23.** Every query returns a PHP fatal:
> `Parse error: syntax error, unexpected '?' in /yundisk/web/waveshare/dotcom/w/includes/Setup.php on line 472`.
> `action=raw` returns the same error in 99 bytes. Rendered page views still work.
> On 2026-08-21 the API path was the documented **workaround** for the WAF block on `index.php?oldid=`;
> **both routes to a pinned revision are now unavailable.** See [`vendors/waveshare/README.md`](../../../vendors/waveshare/README.md).

### Newly acquired

| Title | URL | Publisher | Retrieved | Local artifact | Validated |
|---|---|---|---:|---|---|
| Espressif Flash Download Tool (wiki §8.6.3) | https://dl.espressif.com/public/flash_download_tool.zip | Espressif | 2026-08-23 | `artifacts/tools/flash_download_tool.zip` | ZIP magic; contains `flash_download_tool_3.9.11.exe` |
| `joshuacant/BlueKnob` @ `c71c98ff5b` | https://codeload.github.com/joshuacant/BlueKnob/tar.gz/c71c98ff5b | joshuacant | 2026-08-23 | `examples/selected/BlueKnob.tar.gz` | gzip; Apache-2.0 `LICENSE` present |
| `IngoDuesentrieb/esp32-s3-knob-hardware-explorer` @ `87602cacde` | https://codeload.github.com/IngoDuesentrieb/esp32-s3-knob-hardware-explorer/tar.gz/87602cacde | IngoDuesentrieb | 2026-08-23 | `examples/selected/esp32-s3-knob-hardware-explorer.tar.gz` | gzip; MIT `LICENSE` present |
| `0015/lvgl_kawaii_face` @ `d58e1c8f8e` | https://codeload.github.com/0015/lvgl_kawaii_face/tar.gz/d58e1c8f8e | Eric N. | 2026-08-23 | `examples/selected/lvgl_kawaii_face.tar.gz` | gzip; MIT `LICENSE` present |
| `svwhisper/lyngdorf-secondary-sleep` @ `dfc372fb07` | https://codeload.github.com/svwhisper/lyngdorf-secondary-sleep/tar.gz/dfc372fb07 | svwhisper | 2026-08-23 | `examples/selected/lyngdorf-secondary-sleep.tar.gz` | gzip; ⚠️ MIT **in README only**, no `LICENSE` file |
| `UnkMihai/…-first-successful-screen-test` @ `3cd890b473` | https://codeload.github.com/UnkMihai/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-first-successful-screen-test/tar.gz/3cd890b473 | UnkMihai | 2026-08-23 | `examples/selected/Waveshare-…-first-successful-screen-test.tar.gz` | gzip; ⚠️ MIT **in README only**, no `LICENSE` file |

Repository metadata for all 28 catalogued projects — pinned commit, licence, dates, size, language,
framework, retention flag — is at [`examples/catalog.json`](examples/catalog.json), retrieved 2026-08-23
via the GitHub REST API.

### Content verified rather than downloaded

| Item | Finding |
|---|---|
| `artifacts/tools/Aida_remote_1.85.zip` | **Not truncated.** 475 B is correct: a valid ZIP holding one CRLF text file, `aida_remote_1.85/aida_remote_1.85.rslcd`, declaring `<LCDVER>200</LCDVER><SWVER>6.33.5741 Beta</SWVER>` and eight sensor IDs (`SCPUUTI`, `SCPUCLK`, `TCPUPKG`, `FCPU`, `SGPU1UTI`, `SGPU1CLK`, `TGPU1DIO`, `FGPU1`). Broken out in [factory-demo-apps.md §3.1](factory-demo-apps.md) |
| `artifacts/tools/mjpeg_Conversion_tool_V2.1.zip` | 7 entries: `ffmpeg.exe` (60,993,536 B), `ffprobe.exe` (45,051,904 B), and a .NET wrapper (`.exe`/`.dll`/`.pdb`/`.deps.json`/`.runtimeconfig.json`) whose filenames are GB2312-encoded. **Not upstream FFmpeg** |
| As-shipped SD card layout | Enumerated via GitHub tree API from `nkinnan/manufacturer-firmware-and-sd-card-contents_Guition-K5-Knob-Series-JC3636K518` @ `cee5b94c63`. **Nine directories, five of them undocumented by the wiki.** Not mirrored — no licence and third-party copyrighted media. See [examples/catalog.md §2](examples/catalog.md) |

### Retrieval failures

| Item | URL | Status |
|---|---|---|
| Waveshare wiki MediaWiki API | `https://www.waveshare.com/wiki/api.php?…` and `…/w/api.php?…` | **Broken server-side** — PHP parse error in `Setup.php`. Vendor regression since 2026-08-21 |
| Wiki raw wikitext | `…/index.php?title=…&action=raw` | **Blocked** — returns the same PHP error, 99 B |
| Guition clone vendor source `JC3636K518CN_knob_EN.zip` | `https://pan.jczn1688.com/directlink/1/HMI%20display/JC3636K518CN_knob_EN.zip` · share `https://pan.jczn1688.com/s/54f682` | **Failed.** JS file-manager returns 11,275 B of HTML with a browser UA; Cloudreve API paths `/api/v3/share/{download,info}/54f682` return `{"detail":"Not Found"}`. Needs a real browser session. **High value** — reportedly the same application as the Waveshare comprehensive example, for which no source is published |
| `nkinnan/manufacturer-firmware-and-sd-card-contents_Waveshare-ESP32-S3-Knob-Touch-LCD-1.8` | GitHub | **Empty repository** — API reports `size: 0` and zero branches. The Waveshare-specific firmware/SD dump was never pushed; only the Guition sibling has content |
| Arduino-ESP32 offline component package (wiki §8.6.1) | `https://drive.google.com/drive/folders/1Pcs_A4FKWvdSHnz9lEBYqOpr-noTMbIv` | **Not retained — deliberate.** Google Drive *folder*: no stable direct-download URL, no version, no checksum, third-party-controlled. Prefer Espressif's board manager |

Broader searches for community projects (Reddit, Hackaday, Hackster, general web) surfaced nothing
board-specific beyond what GitHub search and the wiki's §8.8 already yielded. Recorded as a negative
result so the search is not repeated.
