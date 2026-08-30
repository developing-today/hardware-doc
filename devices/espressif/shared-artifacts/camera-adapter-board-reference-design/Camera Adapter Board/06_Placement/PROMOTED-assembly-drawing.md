# `Assemble_ESP32-P4_FUNCTION_EV_BOARD_MIPI_Sub_V1_20240529.pdf` — PROMOTED, not deleted

This file was **moved up** within this repository on **2026-08-24**. It was not archived and not
deleted; it is still here, one directory tree higher and under a discoverable name.

| Field | Value |
|---|---|
| Original relative path | `devices/espressif/shared-artifacts/camera-adapter-board-reference-design/Camera Adapter Board/06_Placement/Assemble_ESP32-P4_FUNCTION_EV_BOARD_MIPI_Sub_V1_20240529.pdf` |
| Moved to | `devices/espressif/shared-artifacts/camera-subboard-assembly-drawing.pdf` |
| Relative link | [`../../../camera-subboard-assembly-drawing.pdf`](../../../camera-subboard-assembly-drawing.pdf) |
| What it is | The **assembly drawing** for the ESP32-P4 Function EV Board **MIPI camera adapter sub-board** — component outlines, reference designators and orientation marks for top and bottom, as used by the assembly house |
| SHA-256 | `c527fae12051dadcfa7aefd35bbabd668302e7e262dd30712c389c68d1e46376` |
| Size | **20,334 bytes** |
| Version | **V1** of the assembly drawing, for board revision **V1.1** |
| Release / build date | **2024-05-29** (filename); ZIP member mtime `2024-06-04 23:05` |
| Author / vendor | Espressif Systems |
| License | **None stated.** Redistribution status `unknown` |
| Upstream repo / commit | Not applicable — published only inside a ZIP on `dl.espressif.com` |

## Why it was promoted

**Espressif does not publish this file standalone.** The sub-board schematic and PCB-layout PDFs
have their own `dl.espressif.com/dl/schematics/…` URLs and are already mirrored at the top of
`shared-artifacts/`. The assembly drawing has no such URL — it exists *only* inside
`camera-adapter-board-reference-design.zip`. Left here it was effectively invisible: five
directory levels deep, inside a tree that had never been extracted until 2026-08-24.

It is also the smallest and most immediately useful document in the whole package: 20 KB that
tells you where every part sits on the board.

## The original is still recoverable, three ways

```bash
# 1. From the retained ZIP in this repository (no network, byte-exact)
cd ../../..
unzip -j camera-adapter-board-reference-design.zip \
  'Camera Adapter Board/06_Placement/Assemble_ESP32-P4_FUNCTION_EV_BOARD_MIPI_Sub_V1_20240529.pdf' -d /tmp

# 2. From the promoted copy in this repository (byte-identical, just renamed)
cp ../../../camera-subboard-assembly-drawing.pdf \
   ./Assemble_ESP32-P4_FUNCTION_EV_BOARD_MIPI_Sub_V1_20240529.pdf

# 3. From Espressif (see EXTRACTED-ADAPTER-BOARDS.md for probe results)
curl -L -O https://dl.espressif.com/schematics/CameraAdapterBoardReferenceDesign.zip
```

Verify either way:

```bash
sha256sum Assemble_ESP32-P4_FUNCTION_EV_BOARD_MIPI_Sub_V1_20240529.pdf
# expect c527fae12051dadcfa7aefd35bbabd668302e7e262dd30712c389c68d1e46376
```

## Also in this directory

`place_txt.txt` (2,332 bytes) was **not** moved. It is the machine-readable companion to this
drawing — reference designator, X/Y coordinates, rotation and board side for each part — and it
is only meaningful alongside the Gerbers in `../03_Gerber/`, so it stays with them.

## See also

- [`../../../EXTRACTED-ADAPTER-BOARDS.md`](../../../EXTRACTED-ADAPTER-BOARDS.md) — full inventory
  of both adapter-board archives, the promotion table, and the ZIP-vs-extraction rationale
- [`../../../README.md`](../../../README.md) — the shared-artifacts index
