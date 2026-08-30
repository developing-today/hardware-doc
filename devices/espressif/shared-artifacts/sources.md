# Shared artifacts (ESP32-P4 board family) — source manifest

> Provenance for every file Espressif publishes **once** and links from **several** ESP32-P4 board
> user guides, stored here rather than duplicated into four board directories.
> Originally retrieved **2026-08-21**; adapter-board ZIPs extracted **2026-08-24**;
> all URLs re-verified **2026-08-28**.
>
> Local paths are relative to this directory. This manifest is the provenance record;
> [`README.md`](README.md) is the contents guide and
> [`EXTRACTED-ADAPTER-BOARDS.md`](EXTRACTED-ADAPTER-BOARDS.md) is the extraction analysis.

`Class` is one of **primary** / **authorized mirror** / **credible mirror** / **standard** / **community**.

Without this directory the same files would be stored two to four times each, adding roughly 30 MB
of byte-identical duplication. Each board record links here and lists which files apply to it —
see [the applicability matrix in `README.md`](README.md#which-board-uses-what).

---

## 1. Function-EV family — FPC connector, panel, camera and display-driver documentation

Linked from the [P4X](../esp32-p4x-function-ev-board/README.md),
[P4X-C5](../esp32-p4x-c5-function-ev-board/README.md) and
[EOL P4](../esp32-p4-function-ev-board/README.md) Function-EV board guides.
All served from `dl.espressif.com/dl/schematics/`. All re-probed **2026-08-28**: HTTP 206,
`application/pdf`.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| SA-1 | `1.0K-GT-15PB` FPC connector specification | 华德共创 (connector vendor), via Espressif | authorized mirror | datasheet | <https://dl.espressif.com/dl/schematics/1.0K-GT-15PB_specification.pdf> | 2026-08-21; HTTP 206 2026-08-28 | undated | The **15-pin, 1.0 mm pitch FPC connector** used for both the MIPI-DSI and MIPI-CSI links on every Function-EV board | ⚠ Third-party copyright, mirrored with **no stated licence** — redistribution `unknown`. 1,257,112 B, SHA-256 `9cbe18e256bdab92010f96bf35da06e882e84d5f45e82b4fd8df5121b3298aba`. Confirmed as `J3` on the LCD adapter BOM | [`1.0K-GT-15PB-fpc-connector-specification.pdf`](1.0K-GT-15PB-fpc-connector-specification.pdf) |
| SA-2 | Camera module datasheet | camera vendor, via Espressif | authorized mirror | datasheet | <https://dl.espressif.com/dl/schematics/camera_datasheet.pdf> | 2026-08-21; HTTP 206 2026-08-28 | undated | The optional 2 MP MIPI-CSI camera accessory | ⚠ Third-party copyright, `unknown` redistribution. ⚠ **Generic upstream filename** (`camera_datasheet.pdf`) — the URL identifies nothing; renamed locally for descriptiveness. 2,810,779 B, SHA-256 `34c6b337b0b2d555c2c8a412196c0eb93924fa9189f0d9e925fed4644d1922cc` | [`camera-module-datasheet.pdf`](camera-module-datasheet.pdf) |
| SA-3 | Display module datasheet | panel vendor, via Espressif | authorized mirror | datasheet | <https://dl.espressif.com/dl/schematics/display_datasheet.pdf> | 2026-08-21; HTTP 206 2026-08-28 | undated | The optional **7-inch 1024 × 600 capacitive-touch MIPI-DSI panel** accessory | ⚠ Third-party copyright, `unknown` redistribution. ⚠ Generic upstream filename; renamed locally. 897,664 B, SHA-256 `f426dba146929c85441ac68720126e2c8a29d9bde58a66b72e3b5aa23d20c9de` | [`display-datasheet.pdf`](display-datasheet.pdf) |
| SA-4 | EK73217BCGA display-driver datasheet | Fitipower/EK, via Espressif | authorized mirror | datasheet | <https://dl.espressif.com/dl/schematics/display_driver_chip_EK73217BCGA_datasheet.pdf> | 2026-08-21; HTTP 206 2026-08-28 | undated | One of the two driver ICs on the 7-inch panel/adapter | ⚠ Third-party copyright, `unknown` redistribution. 1,571,109 B, SHA-256 `bd4ec28f5b11ab95536da6cf6162af18ff8d1ec34fa19379444eb5c0e8f7763a`. Component record: [`components/fitipower/ek73217bcga`](../../../components/fitipower/ek73217bcga/README.md) (created 2026-08-30) | [`ek73217bcga-datasheet.pdf`](../../../components/fitipower/ek73217bcga/artifacts/ek73217bcga-datasheet.pdf) |
| SA-5 | EK79007AD display-driver datasheet | Fitipower/EK, via Espressif | authorized mirror | datasheet | <https://dl.espressif.com/dl/schematics/display_driver_chip_EK79007AD_datasheet.pdf> | 2026-08-21; HTTP 206 2026-08-28 | undated | The other driver IC on the 7-inch panel/adapter | ⚠ Third-party copyright, `unknown` redistribution. 3,723,767 B, SHA-256 `2dbab767e040959f1c7ce1ae3af4e65c888e04d88b066bcb1f3bddee6c8287a4`. Component record: [`components/fitipower/ek73217bcga`](../../../components/fitipower/ek73217bcga/README.md) (created 2026-08-30) | [`ek79007ad-datasheet.pdf`](../../../components/fitipower/ek79007ad/artifacts/ek79007ad-datasheet.pdf) |

## 2. Function-EV family — LCD and camera sub-board design files

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| SA-6 | LCD sub-board schematics | Espressif Systems | primary | schematic | <https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-lcd-subboard-schematics.pdf> | 2026-08-21; HTTP 206 2026-08-28 | **V1.3**, 2024-07-09 (from embedded metadata) | The LCD adapter board's circuitry | ⚠ **Byte-identical** to the copy inside SA-12 (SHA-256 `cbb6a53d…`) — the only one of the four sub-board PDFs that is. ⚠ Filename still says `esp32-p4-function-ev-board-…` after the **EOL** board although the current guides link it. 328,112 B | [`lcd-subboard-schematics.pdf`](lcd-subboard-schematics.pdf) |
| SA-7 | LCD sub-board PCB layout | Espressif Systems | primary | schematic | <https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-lcd-subboard-pcb-layout.pdf> | 2026-08-21; HTTP 206 2026-08-28 | **V1.2**, re-exported 2024-07-02 | The LCD adapter board's layout | ⚠ Hash differs from SA-12's copy (`6f1c9a35…` vs `f07ef2f2…`) but this is a **re-print, not a different revision** — `Allegro Design Publisher`, `CreationDate D:20240702171437+08'00'`, embedded text says **V1.2**, and the standalone print includes a `Composite` sheet the ZIP copy does not. See [`EXTRACTED-ADAPTER-BOARDS.md` §4](EXTRACTED-ADAPTER-BOARDS.md). 384,111 B | [`lcd-subboard-pcb-layout.pdf`](lcd-subboard-pcb-layout.pdf) |
| SA-8 | Camera sub-board schematics | Espressif Systems | primary | schematic | <https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-camera-subboard-schematics.pdf> | 2026-08-21; HTTP 206 2026-08-28 | **V1.1**, 2024-05-29 design; re-exported 2024-07-02 | The camera adapter board's circuitry | ⚠ Hash differs from SA-11's copy (`dcb30637…` vs `b26da766…`) — again a **re-print**, `Microsoft: Print To PDF`, `CreationDate D:20240702164928+08'00'`. The `Print To PDF` producer also makes byte differences partly non-deterministic. 332,122 B | [`camera-subboard-schematics.pdf`](camera-subboard-schematics.pdf) |
| SA-9 | Camera sub-board PCB layout | Espressif Systems | primary | schematic | <https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-camera-subboard-pcb-layout.pdf> | 2026-08-21; HTTP 206 2026-08-28 | **V1.1**, 2024-05-29 | The camera adapter board's layout | ⚠ Re-print of SA-11's copy (`791c0922…` vs `a8b9443e…`). 140,496 B | [`camera-subboard-pcb-layout.pdf`](camera-subboard-pcb-layout.pdf) |
| SA-10 | LCD sub-board **assembly drawing** | Espressif Systems | primary | schematic | **no standalone URL** — extracted from SA-12 on 2026-08-24 | 2026-08-24 (extraction) | **V1.2**, 2024-05-27 | Component placement for assembling the LCD adapter | ⚠ **Espressif publishes no standalone download for this file.** Promoted out of the ZIP so it is discoverable; a `PROMOTED-assembly-drawing.md` placeholder was left at the original path. Provenance inherits from SA-12. 85,267 B, SHA-256 `721e1b04cc39082b95a871fc669b331ed020d67f2e383609ac34f352ec822906` | [`lcd-subboard-assembly-drawing.pdf`](lcd-subboard-assembly-drawing.pdf) |
| SA-10b | Camera sub-board **assembly drawing** | Espressif Systems | primary | schematic | **no standalone URL** — extracted from SA-11 on 2026-08-24 | 2026-08-24 (extraction) | **V1**, 2024-05-29 | Component placement for assembling the camera adapter | Same promotion and placeholder arrangement as SA-10. 20,334 B, SHA-256 `c527fae12051dadcfa7aefd35bbabd668302e7e262dd30712c389c68d1e46376` | [`camera-subboard-assembly-drawing.pdf`](camera-subboard-assembly-drawing.pdf) |

## 3. Function-EV family — adapter-board reference designs

**The most complete design packages Espressif publishes anywhere in the P4 family.** Each ships
editable OrCAD `.DSN` schematic source, editable Allegro `.brd` board source, full Gerbers, drill
files, a BOM and Chinese-language fabrication notes — so these sub-boards are genuinely
reproducible, unlike any main board in the family.

**Note the path is `/schematics/`, not `/dl/schematics/`.** Both exist on this host and neither
redirects to the other.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| SA-11 | Camera Adapter Board reference design | Espressif Systems | primary | repository (archive) | <https://dl.espressif.com/schematics/CameraAdapterBoardReferenceDesign.zip> | 2026-08-21; extracted 2026-08-24; HTTP 206 `binary/octet-stream` 2026-08-28 | Schematic **V1.1** / PCB **V1.1**, both **2024-05-29**; fab notes 2024-06-05; `BOM(V0.3)` | Complete reproducible design: 74 ZIP members, **25 real files** after excluding macOS noise. BOM `docProps` name `lizijin` (created 2024-05-30) and `Wang Dong` (modified 2026-05-26) | ✅ **No version skew** — everything is V1.1 / 2024-05-29. ⚠ **No licence stated**; redistribution `unknown`. ⚠ **Single-source risk: no Internet Archive capture exists** (checked 2026-08-24). ⚠ Contains a directory whose name is **unflagged UTF-8** Chinese (`04_PCB 加工说明`) — stock `unzip` mangles it and the usual CP437→GBK repair produces mojibake; decode raw bytes as UTF-8. ⚠ Contains the Gerbers **twice** (an inner ZIP plus an identical extracted directory, verified by `diff -rq`). 1,349,188 B, SHA-256 `2ab4b8ad20b60817ddd1e8d72de0680f841c9bc0d452b82d9d93aa82c9b8e529` | [`camera-adapter-board-reference-design.zip`](camera-adapter-board-reference-design.zip) + [extracted tree](camera-adapter-board-reference-design/) |
| SA-12 | LCD Adapter Board reference design | Espressif Systems | primary | repository (archive) | <https://dl.espressif.com/schematics/LCDAdapterBoardReferenceDesign.zip> | 2026-08-21; extracted 2026-08-24; HTTP 206 `binary/octet-stream` 2026-08-28 | Schematic **V1.3** (2024-07-09) / PCB, Gerbers, placement, assembly, fab notes all **V1.2** (2024-05-24/27); `BOM(V0.4)` | Complete reproducible design: 74 ZIP members, **26 real files** after excluding macOS noise | ⚠ **Real version skew, confirmed by extraction.** *Every* manufacturing output is **V1.2**; only the schematic is **V1.3**. Anyone fabricating from these Gerbers builds V1.2 hardware while reading a V1.3 schematic — and SA-6, Espressif's *only* published LCD sub-board schematic, is the V1.3 one. ⚠ No licence stated; `unknown`. ⚠ **No Internet Archive capture exists.** ⚠ Same unflagged-UTF-8 filename trap. 1,276,237 B, SHA-256 `231e1ff2f9373de5b9924eaaab00801ad777fb483945629f160423c3752693ed` | [`lcd-adapter-board-reference-design.zip`](lcd-adapter-board-reference-design.zip) + [extracted tree](lcd-adapter-board-reference-design/) |

## 4. EYE family — camera and display component documentation

Linked from the [P4X-EYE](../esp32-p4x-eye/README.md) and [EOL P4-EYE](../esp32-p4-eye/README.md)
guides. Served from a **third distinct path prefix** on the same host: `/AE/esp-dev-kits/`.
All re-probed **2026-08-28**: HTTP 206, `application/pdf`.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| SA-13 | OV2710 camera-sensor overview | OmniVision, via Espressif | authorized mirror | datasheet | <https://dl.espressif.com/AE/esp-dev-kits/ov2710pbv1.1web.pdf> | 2026-08-21; HTTP 206 2026-08-28 | v1.1 per filename | The camera sensor in the EYE boards' 2 MP module | ⚠ Third-party copyright, `unknown` redistribution. A product **brief**, not a full datasheet. 159,720 B, SHA-256 `d34890622db7f06324242329e6b5193597c0088ffe9a2765194166ae3b201912`. Component record now exists | [`ov2710-camera-module-datasheet.pdf`](ov2710-camera-module-datasheet.pdf) |
| SA-14 | HDF2710-47-MIPI camera-module specification | module vendor, via Espressif | authorized mirror | datasheet | <https://dl.espressif.com/AE/esp-dev-kits/HDF2710-47-MIPI-V2.0.pdf> | 2026-08-21; HTTP 206 2026-08-28 | **V2.0** per filename | The camera module **as fitted** on the EYE boards | ⚠ Third-party copyright, `unknown` redistribution. 246,656 B, SHA-256 `050c43a50e45e77436dc99486098614f4ee04511c3586d702cab28b506868ecc`. Component record now exists | [`hdf2710-47-mipi-camera-module-spec.pdf`](hdf2710-47-mipi-camera-module-spec.pdf) |
| SA-15 | ST7789VW LCD-controller datasheet | Sitronix, via Espressif | authorized mirror | datasheet | `https://dl.espressif.com/AE/esp-dev-kits/ST7789VW芯片手册.pdf` — request as `ST7789VW%E8%8A%AF%E7%89%87%E6%89%8B%E5%86%8C.pdf` | 2026-08-21; HTTP 206 2026-08-28 | as served | The controller driving the EYE boards' 1.54-inch 240 × 240 SPI panel | ⚠ **Upstream filename is Chinese and must be percent-encoded**; renamed to portable ASCII on retrieval (`芯片手册` = "chip manual"). Third-party copyright, `unknown` redistribution. 3,135,599 B, SHA-256 `1f9e956057e3909c0714bdab9e682205e03cf52adefd5b4a01093fa3167d398b`. Component record now exists, although Sitronix parts `st7701s` and `st77916` do | [`st7789vw-datasheet.pdf`](../../../components/sitronix/st7789vw/artifacts/st7789vw-datasheet.pdf) |
| SA-16 | ZJY154KC-IF17 1.54-inch LCD module specification | module vendor, via Espressif | authorized mirror | datasheet | `https://dl.espressif.com/AE/esp-dev-kits/胶铁一体ZJY154KC-IF17.pdf` — request as `%E8%83%B6%E9%93%81%E4%B8%80%E4%BD%93ZJY154KC-IF17.pdf` | 2026-08-21; HTTP 206 2026-08-28 | as served | The display module **as fitted**, around the ST7789VW | ⚠ Chinese upstream filename, percent-encoding required, renamed on retrieval (`胶铁一体` = "adhesive-and-metal integrated", describing the bonding construction). Third-party copyright, `unknown` redistribution. 1,290,995 B, SHA-256 `c323a0f082bea4a99431be5d54f2f3305d7489432e18c97d25aa23627bf3bfc5`. Component record now exists | [`zjy154kc-if17-lcd-module-spec.pdf`](zjy154kc-if17-lcd-module-spec.pdf) |

## 5. Archived — offline documentation build

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| SA-17 | esp-dev-kits Documentation, ESP32-P4 target, PDF build | Espressif Systems | primary | manual | <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp-dev-kits-en-master-esp32p4.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | release **`master`**; title page **Aug 23, 2026**; PDF `CreationDate` 2026-08-23 12:25:45; **80 pages** | The offline user guide for **every** P4 board, current and EOL — which now makes it the most robust surviving copy of the two EOL guides whose HTML URLs have since **moved and 404'd** | ⚠ **Archived out of the repository 2026-08-24** to `archive/…` at the same relative path; **nothing was deleted**. Removal was safe because its content was already mined into the five board records on 2026-08-21. ⚠ **`master` build — a moving target**; the URL will serve newer documents over time, so the hash pins only what was fetched. Mitigations: a Wayback capture from 2026-03-31, a fresh Wayback save accepted 2026-08-24, and the docs source in Git. ⚠ The **un-scoped** URL form (without `esp32p4/`) returns HTTP 404. 30,482,003 B, SHA-256 `04d75d2acda82c8f5136bfed4d1732e7e4bd095437e2ecacce271374d8f8538c`. Full record: [`ARCHIVED-FRAMEWORK-GUIDES.md`](ARCHIVED-FRAMEWORK-GUIDES.md) | archived → `archive/devices/espressif/shared-artifacts/` |

## 6. Verification and reacquisition sources

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Establishes | Scope/limitations |
|---|---|---|---|---|---|---|---|---|
| SA-18 | Espressif China mirror host | Espressif Systems | authorized mirror | archive | `https://dl.espressif.cn/schematics/{Camera,LCD}AdapterBoardReferenceDesign.zip` | 2026-08-24 | A same-operator fallback path for SA-11 and SA-12 using the identical path scheme | ⚠ **Same operator**, so this is a mirror, not an independent source. It does not reduce the single-source risk noted on SA-11/SA-12 |
| SA-19 | `espressif/esp-dev-kits` repository | Espressif Systems | primary | repository | <https://github.com/espressif/esp-dev-kits> | 2026-08-24; HTTP 200 2026-08-28 | The documentation source behind SA-17 and the board example code | Not cloned. Commit `f6f80ab` at the 2026-08-21 pass; **`df877cb` on 2026-08-28** |
| SA-20 | Wayback capture of SA-17 | Internet Archive | credible mirror | archive | `http://web.archive.org/web/20260331013312/https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp-dev-kits-en-master-esp32p4.pdf` | 2026-08-24 (HTTP 200) | An older capture of the moving-target PDF | ⚠ Captures a **different build** than the archived local copy. Useful as a fallback, not as a hash match |

---

## 7. Rights and disposition

| Group | Copyright | Redistribution status | Disposition |
|---|---|---|---|
| SA-6 – SA-12, SA-17 (Espressif-authored: sub-board schematics/layouts/assembly, adapter reference designs, docs build) | Espressif Systems | **unknown** — freely published, no explicit licence | `repository` (SA-17 archived out) |
| SA-1 – SA-5, SA-13 – SA-16 (third-party datasheets mirrored by Espressif) | **Third-party** manufacturers — OmniVision, Fitipower/EK, Sitronix, and the panel, camera-module and connector vendors | **unknown** | `repository` |

**No file in this directory carries an explicit grant of redistribution rights.** They are retained
for internal engineering reference and **should not be republished**. This matches the position
already recorded for Waveshare-mirrored third-party datasheets in
[`component-download-failures.txt`](../../../component-download-failures.txt).

---

## 8. Retrieval findings

**Everything in this directory still resolves.** All sixteen live URLs (SA-1 – SA-16) plus SA-17 and
SA-19 returned HTTP 206 or 200 with the expected content type on **2026-08-28**, including both
percent-encoded Chinese filenames and both adapter-board ZIPs.

**Three unrelated URL schemes on one host.** `dl.espressif.com` serves this directory's files from
**three** prefixes that are not redirects of one another:

| Prefix | Serves |
|---|---|
| `/dl/schematics/` | SA-1 – SA-9 (connector, panel, camera, driver ICs, sub-board PDFs) and the EOL Function-EV board's main-board files |
| `/schematics/` | SA-11, SA-12 (adapter-board ZIPs) and the P4X-C5 board's main-board files |
| `/AE/esp-dev-kits/` | SA-13 – SA-16 (EYE-family component docs) and the EOL P4-EYE's schematic and layout |

Guessing the wrong prefix returns a 404, not a redirect.

**Two ZIPs have no Internet Archive capture at all** (SA-11, SA-12, checked 2026-08-24). They are
the most complete design data Espressif publishes for this family and have exactly one origin
operator. Submitting both to `https://web.archive.org/save/` remains the highest-value outstanding
follow-up — it is [recommended but not done](EXTRACTED-ADAPTER-BOARDS.md#10-recommended-not-done).

**`Last-Modified` moves without the content changing.** Both ZIPs reported `Last-Modified` of
2026-08-21 on the 2026-08-24 probe while their SHA-256 still matched the 2026-08-21 download — they
were re-uploaded, not changed. **Do not treat `Last-Modified` as a change signal on this host.**

**The documentation host is the unstable one.** Every migration and failure recorded across this
board family is on `docs.espressif.com` — most recently the EOL board guides moving out of the
`eol/` path segment, documented in
[the EOL board's manifest §4](../esp32-p4-function-ev-board/sources.md#4-retrieval-findings).
`dl.espressif.com` has served every artifact here reliably across all three passes.

---

## 9. Known duplication and gaps

**Intentional duplication, recorded so verification tooling can expect it.** Roughly **6.1 MiB** of
this directory is the same content stored twice — the two adapter-board ZIPs alongside their
extracted trees. The rationale is in
[`EXTRACTED-ADAPTER-BOARDS.md` §6](EXTRACTED-ADAPTER-BOARDS.md#6-why-both-the-zip-and-the-extraction-are-kept):
the ZIP is the only form whose hash can be checked against the vendor, the extraction is the only
form that can be grepped, diffed or browsed. One exact SHA-256 duplicate pair is detectable within
this directory — SA-6 (`lcd-subboard-schematics.pdf`) and the V1.3 schematic inside SA-12's
extracted tree, both `cbb6a53d…`, 328,112 B.

**Three sub-board PDFs differ in hash from their in-ZIP counterparts but are re-prints, not
revisions** (SA-7, SA-8, SA-9). Do not read the differing hashes as evidence of a design change —
the analysis is in [`EXTRACTED-ADAPTER-BOARDS.md` §4](EXTRACTED-ADAPTER-BOARDS.md#4-finding-the-standalone-sub-board-pdfs-are-re-prints-not-different-revisions).

**Ten manufacturer parts named in the adapter BOMs have no `components/` record** — `DMN63D8LDW-7`,
`LBSS138DW1T1G`, `ME6211C18M5G-N` / `ME6211C28M5G-N`, three Jushuo FFC/FPC connectors,
`FPC-05F-24PH20`, `ETA1611S2G`, `AP3012KTR-G1`, `TYPE-C-31-M-12`, `SWPA3012S100MT` and an MDH 24 MHz
oscillator. **No datasheets were present in either archive**, so nothing was auto-created. Leads and
LCSC/JLCPCB cross-references are in
[`EXTRACTED-ADAPTER-BOARDS.md` §5](EXTRACTED-ADAPTER-BOARDS.md#5-findings-from-the-boms--components-not-yet-recorded).
Neither do the five component parts documented by SA-4, SA-5 and SA-13 – SA-16 have records.

**Two Chinese-language fabrication-notes spreadsheets are unread.** `04_PCB 加工说明_….xls` in each
package carries stackup, impedance-control and surface-finish requirements and is currently
inaccessible to most of this repository's audience.

**Two source URLs are generic to the point of uselessness.** SA-2 (`camera_datasheet.pdf`) and SA-3
(`display_datasheet.pdf`) identify neither vendor nor part in the URL. Both were renamed locally for
descriptiveness, but the **part identities behind them are not independently established** — unlike
the EYE family's, which SA-13/SA-14 and SA-15/SA-16 name explicitly.

**Retrieval-date convention.** `2026-08-21` rows were mined then; `2026-08-24` marks the extraction
and archiving pass; `2026-08-28` marks **status re-verification only** — HTTP code and content type.
No file was re-downloaded, re-hashed or re-compared on 2026-08-28.

---

## 10. Related records

- [`README.md`](README.md) — contents guide and the [per-board applicability matrix](README.md#which-board-uses-what)
- [`EXTRACTED-ADAPTER-BOARDS.md`](EXTRACTED-ADAPTER-BOARDS.md) — extraction inventory, version-skew analysis, BOM findings, reacquisition and verification commands
- [`ARCHIVED-FRAMEWORK-GUIDES.md`](ARCHIVED-FRAMEWORK-GUIDES.md) — provenance for SA-17 after archiving
- Board records: [P4X-Function-EV](../esp32-p4x-function-ev-board/sources.md) · [P4X-C5-Function-EV](../esp32-p4x-c5-function-ev-board/sources.md) · [P4X-EYE](../esp32-p4x-eye/sources.md) · [P4-Function-EV (EOL)](../esp32-p4-function-ev-board/sources.md) · [P4-EYE (EOL)](../esp32-p4-eye/sources.md)
- [ESP32-P4 component record](../../../components/espressif/esp32-p4/README.md) · [Espressif vendor sourcing guide](../../../vendors/espressif/README.md)
