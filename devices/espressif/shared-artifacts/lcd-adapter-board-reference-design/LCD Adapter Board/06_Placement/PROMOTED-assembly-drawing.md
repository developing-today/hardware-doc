# `Assemble_ESP32-P4_HMI_SubBoard_V1.2_20240527.pdf` — PROMOTED, not deleted

This file was **moved up** within this repository on **2026-08-24**. It was not archived and not
deleted; it is still here, one directory tree higher and under a discoverable name.

| Field | Value |
|---|---|
| Original relative path | `devices/espressif/shared-artifacts/lcd-adapter-board-reference-design/LCD Adapter Board/06_Placement/Assemble_ESP32-P4_HMI_SubBoard_V1.2_20240527.pdf` |
| Moved to | `devices/espressif/shared-artifacts/lcd-subboard-assembly-drawing.pdf` |
| Relative link | [`../../../lcd-subboard-assembly-drawing.pdf`](../../../lcd-subboard-assembly-drawing.pdf) |
| What it is | The **assembly drawing** for the ESP32-P4 **HMI (LCD) adapter sub-board** — component outlines, reference designators and orientation marks for top and bottom, as used by the assembly house |
| SHA-256 | `721e1b04cc39082b95a871fc669b331ed020d67f2e383609ac34f352ec822906` |
| Size | **85,267 bytes** |
| Version | Board revision **V1.2** |
| Release / build date | **2024-05-27** (filename); ZIP member mtime `2024-05-28 01:30` |
| Author / vendor | Espressif Systems |
| License | **None stated.** Redistribution status `unknown` |
| Upstream repo / commit | Not applicable — published only inside a ZIP on `dl.espressif.com` |

## Why it was promoted

**Espressif does not publish this file standalone.** The HMI sub-board schematic and PCB-layout
PDFs have their own `dl.espressif.com/dl/schematics/…` URLs and are already mirrored at the top
of `shared-artifacts/` as `lcd-subboard-schematics.pdf` and `lcd-subboard-pcb-layout.pdf`. The
assembly drawing has no such URL — it exists *only* inside
`lcd-adapter-board-reference-design.zip`. Left here it was effectively invisible: five directory
levels deep, inside a tree that had never been extracted until 2026-08-24.

## ⚠️ Version caveat — read before using this drawing

This drawing is **V1.2**, and so are the PCB, the Gerbers, the drill files, the placement file
and the fabrication notes in this package. **The schematic in the same package is V1.3**
(`SCH_ESP32-P4_HMI_SubBoard_V1.3_20240709`), and so is the schematic Espressif publishes
standalone as `lcd-subboard-schematics.pdf` — the two are byte-identical.

So: **every manufacturing output Espressif ships for this sub-board describes V1.2 hardware,
while the only schematic it publishes describes V1.3.** If you build from these outputs, this
assembly drawing is authoritative for what is actually on the board; the schematic may not be.
Reconcile before committing to a build. Full detail in
[`../../../EXTRACTED-ADAPTER-BOARDS.md`](../../../EXTRACTED-ADAPTER-BOARDS.md) §4.

The camera adapter board has no such skew — it is V1.1 throughout.

## The original is still recoverable, three ways

```bash
# 1. From the retained ZIP in this repository (no network, byte-exact)
cd ../../..
unzip -j lcd-adapter-board-reference-design.zip \
  'LCD Adapter Board/06_Placement/Assemble_ESP32-P4_HMI_SubBoard_V1.2_20240527.pdf' -d /tmp

# 2. From the promoted copy in this repository (byte-identical, just renamed)
cp ../../../lcd-subboard-assembly-drawing.pdf \
   ./Assemble_ESP32-P4_HMI_SubBoard_V1.2_20240527.pdf

# 3. From Espressif (see EXTRACTED-ADAPTER-BOARDS.md for probe results)
curl -L -O https://dl.espressif.com/schematics/LCDAdapterBoardReferenceDesign.zip
```

Verify either way:

```bash
sha256sum Assemble_ESP32-P4_HMI_SubBoard_V1.2_20240527.pdf
# expect 721e1b04cc39082b95a871fc669b331ed020d67f2e383609ac34f352ec822906
```

## Also in this directory

`place_txt.txt` (7,953 bytes) was **not** moved. It is the machine-readable companion to this
drawing — reference designator, X/Y coordinates, rotation and board side for each part — and it
is only meaningful alongside the Gerbers in `../03_Gerber/`, so it stays with them.

## See also

- [`../../../EXTRACTED-ADAPTER-BOARDS.md`](../../../EXTRACTED-ADAPTER-BOARDS.md) — full inventory
  of both adapter-board archives, the promotion table, and the ZIP-vs-extraction rationale
- [`../../../README.md`](../../../README.md) — the shared-artifacts index
