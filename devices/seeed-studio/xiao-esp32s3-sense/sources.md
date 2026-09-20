# Sources — XIAO ESP32S3 Sense

All retrieved **2026-08-24**. `Class`: `primary` · `authorized mirror` · `credible mirror` · `standard` · `community`.

## Primary — Seeed Studio

| ID | Title | Publisher | Class | Medium | URL | Published/updated | Establishes | Limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|
| S1 | XIAO ESP32S3 Sense product page | Seeed | primary | store listing | [p-5639](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html) | unknown | SKU 113991115, marketed identity | **Stale** — still advertises OV2640 | — |
| S2 | Sense v1.5 schematic (KiCad PDF) | Seeed | primary | schematic | [`202003753_…Sense_v1.5_SCH_260226.pdf.pdf`](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/new-res/202003753_XIAO%20ESP32S3%20Sense_v1.5_SCH_260226.pdf.pdf) | sheet 2026-02-10, PDF 2026-02-26 | **BOM, net names, charge-current annotation, revision history** | Title block says **v1.3** | [`artifacts/schematics/xiao-esp32s3-sense-v1.5-sch.pdf`](artifacts/schematics/xiao-esp32s3-sense-v1.5-sch.pdf) |
| S3 | Sense v1.5 SCH&PCB package (KiCad 9 source) | Seeed | primary | EDA source | [zip](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/new-res/202003753_XIAO%20ESP32S3%20Sense_v1.5_SCH&PCB_260226.zip) | 2026-02-25 | **Authoritative netlist → the J3 pinout**, 4-layer stackup, 17.78 × 21.14 mm outline | — | [`artifacts/extracted/xiao-esp32s3-sense-v1.5-sch-pcb/`](artifacts/extracted/) |
| S4 | "XIAO ESP32S3 v1.4" schematic | Seeed | primary | schematic | [`202003751_…v1.4_SCH_260226.pdf.pdf`](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/new-res/202003751_XIAO%20ESP32S3_v1.4_SCH_260226.pdf.pdf) | — | **Nothing — serves the Sense file** | **Byte-identical to S2.** [Conflict #1](gaps-and-conflicts.md#1-seeed-serves-the-wrong-file-under-the-xiao-esp32s3-v14-schematic-url) | [pointer](artifacts/schematics/xiao-esp32s3-v1.4-sch.pdf.DUPLICATE.md) |
| S5 | XIAO ESP32S3 v1.2 schematic (EAGLE) | Seeed | primary | schematic | [pdf](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_SCH_v1.2.pdf) | 2024-08-02 | Closest available non-Sense schematic | **No text layer** (EAGLE vector export) | [`…v1.2-sch.pdf`](artifacts/schematics/xiao-esp32s3-v1.2-sch.pdf) |
| S6 | XIAO ESP32S3 v1.1 SCH&PCB (EAGLE XML) | Seeed | primary | EDA source | [zip](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_v1.1_SCH&PCB_230327.zip) | 2023-03-28 | Parseable XML for the EAGLE era | Not fully mined | [`artifacts/extracted/xiao-esp32s3-v1.1-sch-pcb/`](artifacts/extracted/) |
| S7 | Wiki: Getting Started (Markdown source) | Seeed | primary | manual | [raw](https://raw.githubusercontent.com/Seeed-Studio/wiki-documents/docusaurus-version/sites/en/docs/Sensor/SeeedStudio_XIAO/SeeedStudio_XIAO_ESP32S3/XIAO_ESP32S3_Getting_Started.md) | — | Power figures, battery notes, bootloader entry, OV2640→OV3660 change, FAQ | **Contains self-contradictions** ([#4](gaps-and-conflicts.md#4-seeeds-own-spec-table-gives-two-different-deep-sleep-figures-for-the-sense)) | [`artifacts/wiki-snapshot/…`](artifacts/wiki-snapshot/) |
| S8 | Wiki corpus — 230 Markdown files | Seeed | primary | manual | repo `Seeed-Studio/wiki-documents`, branch `docusaurus-version` | — | Camera/mic/SD guides, 68 artifact URLs, 75 project links | Branch trap: `main` 404s | [`artifacts/wiki-snapshot/`](artifacts/wiki-snapshot/) |
| S9 | Factory firmware bundle (2024-08-14) | Seeed | primary | firmware | [zip](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO-ESP32S3-Sense-firmware-20240814.zip) | filename 2024-08-14; **binaries 2023-02-08** | Flash offsets, partition map, hardcoded credentials | Date is a repackaging date | [`artifacts/firmware/`](artifacts/firmware/) |
| S10 | XIAO Reference Design catalogue | Seeed | primary | catalogue | [pdf](https://files.seeedstudio.com/wiki/XIAO/XIAO-Reference-Design.pdf) | 2025-11-15 | Cross-XIAO comparison tables; **117 community projects with URLs** | Contains a duplicated description; a **third** contradictory low-power figure | [`xiao-reference-design.pdf`](artifacts/datasheets/xiao-reference-design.pdf.ARCHIVED.md) *(archived — placeholder)* |
| S11 | Sense pinout spreadsheet | Seeed | primary | pinout | [xlsx](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_Sense_Pinout.xlsx) | — | Vendor pin table | Hand-maintained | [`artifacts/pinouts/`](artifacts/pinouts/) |

## Primary — component manufacturers

| ID | Title | Publisher | Class | Medium | Version | Establishes | Limitations | Local path |
|---|---|---|---|---|---|---|---|---|
| C1 | OV2640 datasheet | OmniVision | primary | datasheet | **v1.6, 2006-02-28** | 1600×1200, 2.2 µm, 40 dB S/N, 600 µA standby | "Advanced Information / Preliminary". Redistribution `unknown` | [pdf](../../../components/omnivision/ov2640/artifacts/ov2640-datasheet-v2.2.pdf) |
| C2 | OV3660 datasheet | OmniVision | primary | datasheet | **v1.3, 2011-05** | 2048×1536, 1/5", 98 mA, 70 dB DR | **PRELIMINARY**, some values TBD. **Redistribution restricted** | [pdf](../../../components/omnivision/ov3660/artifacts/ov3660-datasheet.pdf) — relocated 2026-08-30 to the [component record](../../../components/omnivision/ov3660/README.md) |
| C3 | OV5640 datasheet | OmniVision | primary | datasheet | **v2.03, 2011-05** | 2592×1944, autofocus, 140 mA | **Redistribution restricted** | [pdf](../../../components/omnivision/ov5640/artifacts/ov5640-datasheet-v2.03.pdf) |
| C4 | ESP32-S3 datasheet (Seeed-hosted copy) | Espressif via Seeed | authorized mirror | datasheet | unknown | Strapping pins, ADC units, GPIO limits | **Vendor mirror.** Byte-differs from Espressif's original *and* from Waveshare's mirror — three portals, three revisions. Prefer the [Espressif copy in the component record](../../../components/espressif/esp32-s3r8/README.md) | [pdf](artifacts/datasheets/esp32-s3-datasheet-seeed-copy.pdf) |
| C5 | ESP-IDF / ESP-IoT-Solution programming guides | Espressif | primary | framework docs | v5.1.4, v5.2.5 | API reference behind the camera, I²S and LEDC guidance used throughout | **Archived, not in the repo** — held under the [ESP32-S3R8 component](../../../components/espressif/esp32-s3r8/README.md), ~77 MiB. Hashes, sizes and download URLs: [`ARCHIVED-FRAMEWORK-GUIDES.md`](../../../components/espressif/esp32-s3r8/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) | archive |

## Primary — Espressif software

| ID | Title | Class | Medium | URL | Establishes | Local path |
|---|---|---|---|---|---|---|
| E1 | `arduino-esp32` `variants/XIAO_ESP32S3/pins_arduino.h` | primary | repository | [raw @ master](https://raw.githubusercontent.com/espressif/arduino-esp32/master/variants/XIAO_ESP32S3/pins_arduino.h) | **D0–D10 map, `LED_BUILTIN 21`, USB VID/PID `2886:0056`, `SS = 44`** | [local](artifacts/source-snapshots/pins_arduino.h) |
| E2 | `camera_pins.h`, `CAMERA_MODEL_XIAO_ESP32S3` block | primary | repository | [raw @ master](https://raw.githubusercontent.com/espressif/arduino-esp32/master/libraries/ESP32/examples/Camera/CameraWebServer/camera_pins.h) | **Full DVP pin map; `PWDN` and `RESET` = −1** | [local](artifacts/source-snapshots/camera_pins.h) |

E1 and E2 independently corroborate the netlist derived from S3. Retrieved from `master`, so **not revision-pinned** — a known weakness of these two rows.

## Community

| ID | Source | Class | Medium | Establishes | Evidence type |
|---|---|---|---|---|---|
| M1 | [limengdu/SeeedStudio-XIAO-ESP32S3-Sense-camera](https://github.com/limengdu/SeeedStudio-XIAO-ESP32S3-Sense-camera) @ `bb67cd0a` | community (Seeed engineer) | repository | Arduino 2.x vs 3.x camera API split | demonstrable project |
| M2 | [Sukecz/esp32-birdnet-mic](https://github.com/Sukecz/esp32-birdnet-mic) @ `8552b12a` | community | repository | Continuous PDM capture + Wi-Fi is achievable | demonstrable project, actively maintained |
| M3 | [KamranAghlami/XIAO_Webcam](https://github.com/KamranAghlami/XIAO_Webcam) @ `aed81505` | community | repository | USB UVC device class works | demonstrable project |
| M4 | [fabio-garavini/Xiao_Sense_CameraWebServer_Audio](https://github.com/fabio-garavini/Xiao_Sense_CameraWebServer_Audio) @ `47bb9edc` | community | repository | Camera + microphone concurrency | demonstrable project; **unlicensed**, stale (2024-03) |
| M5 | 28 showcase projects (Hackster/Hackaday/YouTube/Instructables) | community | project logs, videos | What the board is used for | **reproduced documentation** — vendor-curated, unverified |
| M6 | Full catalogue of 18 GitHub repos | community | repositories | Ecosystem breadth | see [`examples/catalog.json`](examples/catalog.json) |

## Evidence hierarchy used in this tree

1. **`.kicad_pcb` resolved nets** — actual copper. Overrides everything.
2. **`.kicad_sch`** — component-level detail the PCB flattens (series resistors, DNP parts).
3. **Espressif board-support headers** — independent confirmation of 1–2.
4. **Component datasheets** — capability of parts, not board wiring.
5. **Seeed wiki prose** — intent and vendor claims; demonstrably contains errors.
6. **Product page / catalogue** — marketing; stalest tier.
7. **Community projects** — existence proofs, not measurements.

Where tiers conflict, the conflict is recorded in [`gaps-and-conflicts.md`](gaps-and-conflicts.md) rather than resolved by preference.

## Coverage boundary

**No hardware.** No electrical, thermal, timing or power figure here was measured. No example was compiled or flashed. The Sense daughterboard was not torn down, which is why the [microphone part number](gaps-and-conflicts.md#7-microphone-part-number-not-established--resolved-2026-08-24) and the daughterboard-side wiring remain open. Regulatory filings were not mined. See [`examples/search-log.md`](examples/search-log.md) for search depth and exclusions.
