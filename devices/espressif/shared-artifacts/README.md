# Shared artifacts — Espressif ESP32-P4 development-board family

Documents that Espressif publishes **once** and links from **several** ESP32-P4 board user guides. They are stored here rather than duplicated into each board's `artifacts/` directory.

Without this directory the same 15 files would be stored between two and four times each, adding roughly 30 MB of byte-identical duplication to the repository. Verification tooling that flags duplicate hashes as accidental would also fire on every copy. Each board record links here and lists which of these files apply to it.

Retrieved **2026-08-21**. Every PDF validated by `%PDF` magic; every ZIP validated by `PK\x03\x04` magic and a full `testzip()` integrity pass.

> **Provenance manifest: [`sources.md`](sources.md)** — per-file class, medium, retrieval date,
> version, what each source establishes, its limitations, and the rights position. All URLs
> re-verified **2026-08-28** (every one still resolves).

---

## Contents

### Applies to all five ESP32-P4 boards

| File | Bytes | SHA-256 | Source URL |
|---|---:|---|---|
| ~~`esp-dev-kits-en-master-esp32p4.pdf`~~ **archived 2026-08-24** — [record](ARCHIVED-FRAMEWORK-GUIDES.md) | 30 482 003 | `04d75d2acda82c8f5136bfed4d1732e7e4bd095437e2ecacce271374d8f8538c` | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp-dev-kits-en-master-esp32p4.pdf |

This is the `esp-docs` PDF build of the entire `esp-dev-kits` project rendered for the `esp32p4` target — i.e. **the offline user guide for every P4 board in one file**, current and EOL. It is the single most useful artifact in this directory. Because it is a `master` build it carries no cover version number; it is pinned by SHA-256 and retrieval date instead.

### Applies to the Function-EV family (P4X, P4X-C5, and the EOL P4)

> **Three rows moved on 2026-08-30.** `ek79007ad-datasheet.pdf`, `ek73217bcga-datasheet.pdf` and
> `st7789vw-datasheet.pdf` are **part** datasheets, not board artifacts, and each already had a
> byte-identical twin under `components/`. They now live only in their component records; the
> hashes and byte counts below are unchanged and still correct. See
> [`DRIVER-DATASHEETS-MOVED.md`](DRIVER-DATASHEETS-MOVED.md) for the rationale and the boundary
> this directory now applies.


| File | Bytes | SHA-256 | Source URL |
|---|---:|---|---|
| `1.0K-GT-15PB-fpc-connector-specification.pdf` | 1 257 112 | `9cbe18e256bdab92010f96bf35da06e882e84d5f45e82b4fd8df5121b3298aba` | `https://dl.espressif.com/dl/schematics/1.0K-GT-15PB_specification.pdf` |
| `camera-module-datasheet.pdf` | 2 810 779 | `34c6b337b0b2d555c2c8a412196c0eb93924fa9189f0d9e925fed4644d1922cc` | `https://dl.espressif.com/dl/schematics/camera_datasheet.pdf` |
| `display-datasheet.pdf` | 897 664 | `f426dba146929c85441ac68720126e2c8a29d9bde58a66b72e3b5aa23d20c9de` | `https://dl.espressif.com/dl/schematics/display_datasheet.pdf` |
| `ek73217bcga-datasheet.pdf` **→ [moved to `components/fitipower/ek73217bcga/`](../../../components/fitipower/ek73217bcga/artifacts/ek73217bcga-datasheet.pdf)** | 1 571 109 | `bd4ec28f5b11ab95536da6cf6162af18ff8d1ec34fa19379444eb5c0e8f7763a` | `https://dl.espressif.com/dl/schematics/display_driver_chip_EK73217BCGA_datasheet.pdf` |
| `ek79007ad-datasheet.pdf` **→ [moved to `components/fitipower/ek79007ad/`](../../../components/fitipower/ek79007ad/artifacts/ek79007ad-datasheet.pdf)** | 3 723 767 | `2dbab767e040959f1c7ce1ae3af4e65c888e04d88b066bcb1f3bddee6c8287a4` | `https://dl.espressif.com/dl/schematics/display_driver_chip_EK79007AD_datasheet.pdf` |
| `lcd-subboard-schematics.pdf` | 328 112 | `cbb6a53dc20a68748784b5bf3548801710f925bd69dbdb75510a9a46d6d0007a` | `https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-lcd-subboard-schematics.pdf` |
| `lcd-subboard-pcb-layout.pdf` | 384 111 | `6f1c9a3570205d42bb117a7a3eb930a97646e44d346a244a02eff2c885d69774` | `https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-lcd-subboard-pcb-layout.pdf` |
| `camera-subboard-schematics.pdf` | 332 122 | `dcb30637c379e9fde13dfadefe1b143902fd6ec53383e562ddbab33b271dbe37` | `https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-camera-subboard-schematics.pdf` |
| `camera-subboard-pcb-layout.pdf` | 140 496 | `791c0922cc94891d12a965dcd9c866c3fc663b8d216f6019d9e6ab6873561127` | `https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-camera-subboard-pcb-layout.pdf` |
| `lcd-subboard-assembly-drawing.pdf` | 85 267 | `721e1b04cc39082b95a871fc669b331ed020d67f2e383609ac34f352ec822906` | **No standalone URL** — extracted from `lcd-adapter-board-reference-design.zip` on 2026-08-24 |
| `camera-subboard-assembly-drawing.pdf` | 20 334 | `c527fae12051dadcfa7aefd35bbabd668302e7e262dd30712c389c68d1e46376` | **No standalone URL** — extracted from `camera-adapter-board-reference-design.zip` on 2026-08-24 |
| `lcd-adapter-board-reference-design.zip` | 1 276 237 | `231e1ff2f9373de5b9924eaaab00801ad777fb483945629f160423c3752693ed` | `https://dl.espressif.com/schematics/LCDAdapterBoardReferenceDesign.zip` |
| `camera-adapter-board-reference-design.zip` | 1 349 188 | `2ab4b8ad20b60817ddd1e8d72de0680f841c9bc0d452b82d9d93aa82c9b8e529` | `https://dl.espressif.com/schematics/CameraAdapterBoardReferenceDesign.zip` |

The two **assembly drawings** are the only files here that Espressif does not publish as
standalone downloads. They were promoted out of the adapter-board ZIPs so they are discoverable;
see [`EXTRACTED-ADAPTER-BOARDS.md`](./EXTRACTED-ADAPTER-BOARDS.md) §3.

Note the URL inconsistency: sub-board **PDFs** live under `/dl/schematics/` while the adapter-board **ZIPs** live under `/schematics/`. Both are real; neither path is a redirect of the other. This trap is recorded in the [vendor guide](../../../vendors/espressif/README.md).

Note also that the sub-board PDFs are still named `esp32-p4-function-ev-board-…` after the **EOL** board, even though the current P4X and P4X-C5 user guides link to them. Espressif has not re-issued them under new names.

#### What is inside the two adapter-board ZIPs

> **Both ZIPs were extracted and fully inventoried on 2026-08-24.** They are now also present as
> the directories `camera-adapter-board-reference-design/` and
> `lcd-adapter-board-reference-design/`. The complete inventory, hashes, per-file disposition, BOM
> findings and version-skew analysis are in
> **[`EXTRACTED-ADAPTER-BOARDS.md`](./EXTRACTED-ADAPTER-BOARDS.md)** — read that rather than the
> summary below if you need detail.

These are the **most complete design packages Espressif publishes anywhere in the P4 family** — considerably more complete than anything published for the main boards. Each contains 74 members (plus macOS `__MACOSX` resource-fork noise):

```
LCD Adapter Board/
├── 01_Schematic/   SCH_ESP32-P4_HMI_SubBoard_V1.3_20240709.{DSN,pdf}   (OrCAD source + PDF)
├── 02_PCB/         PCB_ESP32-P4_HMI_SubBoard_V1.2_20240527.{brd,pdf}   (Allegro source + PDF)
├── 03_Gerber/      Gerber_…_V1.2_20240527/  TOP/BOTTOM/SILK/SOLDER/PASTE .art, .drl, .rou
├── 04_PCB 加工说明/  PCB 加工说明_…_V1.2_20240524.xls                     (fabrication notes, Chinese)
├── 05_BOM/         BOM(V0.4)_ESP32-P4-HMI-SubBOARD_XX_TTNNVV.xlsx
└── 06_Placement/   Assemble_…_V1.2_20240527.pdf, place_txt.txt
```

The camera adapter ZIP has the identical structure. Both ship **editable EDA source** (OrCAD `.DSN`, Allegro `.brd`), full Gerbers and a BOM — so these sub-boards are genuinely reproducible, unlike the main boards.

Two caveats. The schematic (V1.3, 2024-07-09) is a later revision than the PCB (V1.2, 2024-05-27), the same mismatch pattern seen on the [ESP32-P4-EYE](../esp32-p4-eye/README.md#2-a-versioning-wrinkle-worth-noticing). And several member paths contain non-ASCII (Chinese) directory names; they are preserved as supplied rather than renamed, since renaming inside an archive would break its integrity hash.

> **Both caveats were confirmed and sharpened by the 2026-08-24 extraction.** The version skew is
> worse than "schematic vs PCB": *every* manufacturing output — Gerbers, drill, placement,
> assembly drawing and fabrication notes — is V1.2, and only the schematic is V1.3. Separately,
> the Chinese directory name `04_PCB 加工说明` is stored as **unflagged UTF-8**, so the usual
> CP437→GBK repair produces mojibake; decode the raw bytes as UTF-8 instead. Both are documented
> in [`EXTRACTED-ADAPTER-BOARDS.md`](./EXTRACTED-ADAPTER-BOARDS.md) §2 and §4.

### Applies to the EYE family (P4X-EYE and the EOL P4-EYE)

| File | Bytes | SHA-256 | Source URL |
|---|---:|---|---|
| `ov2710-camera-module-datasheet.pdf` | 159 720 | `d34890622db7f06324242329e6b5193597c0088ffe9a2765194166ae3b201912` | `https://dl.espressif.com/AE/esp-dev-kits/ov2710pbv1.1web.pdf` |
| `hdf2710-47-mipi-camera-module-spec.pdf` | 246 656 | `050c43a50e45e77436dc99486098614f4ee04511c3586d702cab28b506868ecc` | `https://dl.espressif.com/AE/esp-dev-kits/HDF2710-47-MIPI-V2.0.pdf` |
| `st7789vw-datasheet.pdf` **→ [moved to `components/sitronix/st7789vw/`](../../../components/sitronix/st7789vw/artifacts/st7789vw-datasheet.pdf)** | 3 135 599 | `1f9e956057e3909c0714bdab9e682205e03cf52adefd5b4a01093fa3167d398b` | `https://dl.espressif.com/AE/esp-dev-kits/ST7789VW芯片手册.pdf` |
| `zjy154kc-if17-lcd-module-spec.pdf` | 1 290 995 | `c323a0f082bea4a99431be5d54f2f3305d7489432e18c97d25aa23627bf3bfc5` | `https://dl.espressif.com/AE/esp-dev-kits/胶铁一体ZJY154KC-IF17.pdf` |

**Renames recorded.** The last two upstream filenames are Chinese and must be percent-encoded in the request (`ST7789VW%E8%8A%AF%E7%89%87%E6%89%8B%E5%86%8C.pdf`, `%E8%83%B6%E9%93%81%E4%B8%80%E4%BD%93ZJY154KC-IF17.pdf`). They were renamed to portable ASCII on retrieval per the repository's filename policy. The first two were renamed only for descriptiveness. `ST7789VW芯片手册` means "ST7789VW chip manual"; `胶铁一体` means "adhesive-and-metal integrated", describing the display module's bonding construction.

Note the **third `dl.espressif.com` path prefix**: `/AE/esp-dev-kits/`, distinct from both `/dl/schematics/` and `/schematics/`. Espressif uses at least three unrelated schemes on this one host.

---

## Rights and disposition

| Group | Copyright | Redistribution status | Disposition |
|---|---|---|---|
| `esp-dev-kits` PDF, sub-board schematics/layouts, adapter reference designs | Espressif Systems | **unknown** — freely published, no explicit licence | `repository` |
| Camera, display, display-driver and FPC-connector datasheets | **Third-party** manufacturers (OmniVision, EK/Fitipower, panel and connector vendors); mirrored by Espressif with no stated licence | **unknown** | `repository` |

None of these files carries an explicit grant of redistribution rights. They are retained for internal engineering reference and should not be republished. This mirrors the position already recorded for Waveshare-mirrored third-party datasheets in [`component-download-failures.txt`](../../../component-download-failures.txt).

---

## Which board uses what

| File group | [P4X-Function-EV](../esp32-p4x-function-ev-board/README.md) | [P4X-C5-Function-EV](../esp32-p4x-c5-function-ev-board/README.md) | [P4X-EYE](../esp32-p4x-eye/README.md) | [P4-Function-EV (EOL)](../esp32-p4-function-ev-board/README.md) | [P4-EYE (EOL)](../esp32-p4-eye/README.md) |
|---|:-:|:-:|:-:|:-:|:-:|
| `esp-dev-kits` PDF | ✓ | ✓ | ✓ | ✓ | ✓ |
| FPC / panel / camera / driver datasheets | ✓ | ✓ | — | ✓ | — |
| LCD & camera sub-board PDFs | ✓ | ✓ | — | ✓ | — |
| Adapter-board reference-design ZIPs | ✓ | ✓ | — | ✓ | — |
| OV2710 / HDF2710 / ST7789VW / ZJY154KC | — | — | ✓ | — | ✓ |

---

See also the [source manifest](sources.md), the [ESP32-P4 component record](../../../components/espressif/esp32-p4/README.md) and the [Espressif vendor sourcing guide](../../../vendors/espressif/README.md).
