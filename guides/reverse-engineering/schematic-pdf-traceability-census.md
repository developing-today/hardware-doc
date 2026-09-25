# Traceability census — every schematic PDF retained in this repository

> **Provenance.** Authored by the 2026-09-07 schematic net-tracing pass in
> `scratch/schematic-tracing/traceability-census.md`, and promoted into the repository
> **2026-09-20** because it existed nowhere else — the scratch README had claimed the
> directory "can be deleted without losing a finding", which was not true of this file.
> Content is unchanged apart from one relative link repointed at this directory.

**Produced:** 2026-09-07, poppler 26.06.0.
**Method:** [`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](tracing-nets-from-schematic-pdfs.md) §1.

Every `artifacts/**/*.pdf` in the repository (291 files) was run through
`pdftotext -layout`; the raw output is in `text/`. The subset that is a *schematic* is
classified below. **Negative results are stated with the evidence that produced them**, so the
next agent does not repeat the attempt.

The three inputs to each verdict are: `pdfinfo` producer string, `pdfimages -list` row count
(0 = no embedded raster at all), and `pdftotext -layout` word count. Where a verdict is
"not traceable" the additional `pdffonts` result is given, because a schematic with **no
embedded fonts** has had its text converted to vector outlines and no text tool will ever
recover it.

---

## Verdict summary

| Verdict | Count |
|---|---|
| **Traceable** — vector, text layer intact, net names recoverable | 38 |
| **Partly traceable** — text present but sparse; designator/value census only | 5 |
| **Not traceable** — text outlined to vector paths, or raster | 6 |

---

## 1. Traced this session (priority set)

| File | Pages | Words | Rasters | Producer | Result |
|---|---|---|---|---|---|
| `devices/lilygo/t-display-s3-shared/…/T_Display_S3.pdf` | 1 | 1120 | **0** | Altium | **Traceable.** Full designator census + charger, LDO, backlight, header and FPC nets recovered. `PI`/`CO` tokens present; **no `NL` tokens** — binding done against visible label text. |
| `devices/lilygo/…/SCH_T-Display-S3-MIDI_V1.1.pdf` | 1 | 711 | 2 | none | **Traceable.** The 2 rasters are a logo and its soft mask, not schematic content. |
| `devices/lilygo/t-display-s3-amoled/…/T-DISPLAY-S3-AMOLED.pdf` | 2 | 1242 | 1 | Altium | **Traceable.** 52 `NL` tokens. Charger `U5` confirmed 5-pin. |
| `devices/lilygo/…/T-Display-S3-AMOLED-Touch.pdf` | 4 | 1220 | 0 | Altium | **Traceable.** No `NL` tokens; `PI`/`CO` present. `AXPM65611` 12-pin map recovered. |
| `devices/lilygo/…/T-Display-S3-AMOLED-Plus.pdf` | 4 | 1463 | 0 | Altium | **Traceable.** `AXPM65611` map independently confirmed, with rail annotations. |
| `devices/m5stack/cardputer-adv/…/Sch_M5CardputerAdv_v1.0_….pdf` | 4 | 1710 | **0** | Altium | **Traceable.** 66 `NL` tokens. Three open questions closed. |
| `devices/m5stack/cardputer-v1.1/…/Sch_M5Cardputer.pdf` | 2 | 1305 | 0 | Altium | **Traceable.** 44 `NL` tokens. |
| `devices/m5stack/cardputer-v1.1/…/M5Cardputer_Base.pdf` | 1 | 46 | 0 | Altium | **Partly traceable.** Only 46 words on the sheet — it is a near-empty base-board outline, not a dense schematic. Nothing withheld by the tooling. |
| `devices/m5stack/dinmeter/…/K134_DIN_Meter_v1.0-schematic.pdf` | 1 | 873 | **0** | Altium | **Traceable.** 26 `NL` tokens. Encoder, buzzer and Grove rail all resolved. |
| `devices/m5stack/dinmeter-v1.1/…/K134-V11_….pdf` | 1 | 873 | 0 | Altium | **Traceable, and byte-equivalent in content** to the v1.0 sheet — identical word count, identical `NL` set. |
| `devices/m5stack/cap-lora-1262/…/U214-Cap-LoRa1262_SCH_V1.1_….pdf` | 1 | 516 | **0** | Altium | **Traceable.** No `NL` tokens; bound by geometry and confirmed with a 300 dpi crop. |
| `devices/m5stack/cap-cc1101/…/U219-Cap_CC1101_SCH_V0.3_….pdf` | 3 | 974 | **0** | Altium | **Traceable.** No `NL` tokens; same treatment. |
| `components/m5stack/stamp-s3a/artifacts/Sch_StampS3_v0.3.3-StampS3A.pdf` | 1 | 865 | **0** | Altium | **Traceable.** 50 `NL` tokens. `U4` part number recovered. |
| `components/m5stack/stamp-s3/artifacts/Sch_M5StampS3_v0.2.pdf` | 1 | 827 | 0 | Altium | **Traceable.** 50 `NL` tokens. |
| `components/m5stack/stamp-lora-1262/…/Stamp-LoRa-1262-Mini_SCH_A1_….pdf` | 1 | 457 | 0 | Altium | **Traceable.** 17 `NL` tokens. |

## 2. Traceable, read only — **not** this session's records to edit

Findings for these belong to their owners; see `index-fragments.md`.

| File | Pages | Words | Rasters | Producer |
|---|---|---|---|---|
| `devices/m5stack/papermono/…/PaperMono_SCH_V0.6.2_20260522.pdf` | 6 | 3951 | 2 | Altium — **144 `NL` tokens, the richest sheet in the repository** |
| `devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/…` | 2 | 4459 | 0 | Altium |
| `devices/waveshare/esp32-s3-epaper-3.97/…` | 1 | 1173 | 0 | Altium |
| `devices/espressif/esp32-p4-function-ev-board/…-schematics-v1.52.pdf` | 6 | 2986 | 40 | — |
| `devices/espressif/esp32-p4x-c5-function-ev-board/…-2.0-schematics.pdf` | 6 | 3052 | 40 | — |
| `devices/espressif/esp32-p4-eye/…-mb-schematics-v2.3.pdf` | 5 | 1976 | 33 | — |
| `devices/lilygo/t-display-s3-long/…` (both variants) | 1 | 1252 / 1302 | 0 | Altium |
| `devices/lilygo/t-display-s3-pro/…/T-Display-Pro.pdf` | 1 | 1531 | 0 | Altium |
| `devices/lilygo/t-display-amoled-lite/…` | 3 | 1662 | 0 | Altium |
| `devices/lilygo/t4-s3/…/T4-S3-240719.pdf` | 3 | 988 | 0 | — |
| `devices/m5stack/stamp-c6lora/…/S012-Stamp_C6LoRa_SCH_v0.2.3.pdf` | 3 | 1073 | 0 | Altium |
| `devices/soldered-electronics/inkplate-5/…` and `-gen2/…` | 6 / 7 | 1667 / 1900 | 6 / 7 | Eeschema-PDF |
| `devices/zerowriter/…/Zerowriter Inkplate 5 Gen2 Schematics.pdf` | 8 | 1940 | 16 | Eeschema-PDF |
| `devices/seeed-studio/…/xiao-esp32s3-sense-v1.5-sch.pdf` | 4 | 864 | 10 | Eeschema-PDF |
| `devices/seeed-studio/…/xiao-esp32s3-plus-v1.1-sch.pdf` | 4 | 1010 | 8 | Eeschema-PDF |

> KiCad's `Eeschema-PDF` exports carry a normal text layer but **no `PI`/`CO`/`NL` helper
> tokens** — that layer is an Altium-specific artefact. KiCad sheets are traceable, but every
> binding must be geometric, and pin *numbers* are often the only per-pin text.

## 3. Partly traceable — text present, connectivity not

| File | Pages | Words | Why |
|---|---|---|---|
| `devices/lilygo/t-display-s3-pro/…/T-BHI260_V1.1.pdf` | 1 | 190 | daughterboard stub; few nets named |
| `devices/lilygo/t-display-s3-pro/…/T-ICM29048.pdf` | 1 | 131 | as above |
| `devices/lilygo/t-display-s3-amoled/…/Camera-Shield.pdf` | 1 | 396 | as above |
| `devices/lilygo/t-display-s3-pro/…/Camer-Shield.pdf` | 1 | 418 | as above (filename typo is upstream) |
| `devices/seeed-studio/…/wio-sx1262-for-xiao-v1.0-sch.pdf` | 1 | 220 | KiCad, sparse labelling |

## 4. ⚠ NOT traceable — stated with evidence

These four are the negative results. **Do not spend time on them again.**

| File | Evidence | Class |
|---|---|---|
| `devices/nicolai-electronics/tanmatsu/artifacts/schematics/tanmatsu-schematic.pdf` | 10 pages; `pdftotext -layout` yields **0 words**; `pdffonts` lists **no fonts whatsoever**; `pdfimages -list` shows 1 image | **All text converted to vector outlines.** No text tool will recover a net name. Needs the upstream KiCad source, which the Tanmatsu project does publish. |
| `devices/nicolai-electronics/tanmatsu/…/add-on/jtag/schematic.pdf` | 1 page; **0 words**; **0 fonts**; **0 images** | Same — pure vector paths. |
| `devices/zerowriter/…/design/zw_keyboard/schematic.pdf` | 1 page; producer `KiCad`; **0 words**; **0 fonts**; **0 images** | Same. Note the *sibling* Zerowriter sheets exported via `Eeschema-PDF` **do** carry text — so this is an export-setting difference, and the same design is readable from the `OUTPUTS/` copies. **Use those instead.** |
| `devices/seeed-studio/…/xiao-esp32s3-v1.2-sch.pdf`, `…/xiao-esp32s3-v1.1-sch-pcb/XIAO ESP32S3_v1.1_SCH_230327.pdf`, `…/xiao-esp32s3-expansion-board-v1.0-sch.pdf` | 1–2 words each; `pdffonts` lists exactly **one** font, `SimSun-0-50`, embedded solely to draw two full-width colons; **0 images** | **EAGLE 9.6.2 exports with text as outlines.** The one or two extracted "words" are the colons, not net names. The *Eeschema* XIAO sheets in the same directory are fine; prefer them. |

## 5. Not schematics — excluded from this census

Datasheets, manuals, regulatory exhibits, mechanical drawings and PCB-layout plots were
extracted to `text/` but are not assessed here. Two observations worth carrying:

- **Mechanical drawings are near-textless by nature** (9–19 words: a title block and a few
  dimensions). `STAMP-S3A-dimensions.pdf` at 9 words and `K134-din_meter_asm_v1-dimensions.pdf`
  at 14 are *not* broken; the dimensions are drawn, not typed. They are still useful as
  **vector** sources — rasterise and crop rather than reaching for `pdfimages`, which returns
  nothing on all of them.
- `components/joulwatt/jw5712/artifacts/jw5712-jw5712a-datasheet-scanned.pdf` — **0 words,
  4 pages, 4 images, one full-page image per page.** This is a genuine raster scan, exactly the
  case §1 of the guide describes. Its filename already says `-scanned`, which was accurate.
