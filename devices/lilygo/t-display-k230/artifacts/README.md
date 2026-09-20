# T-Display K230 — artifact layout

## What is here

| Directory | Contents |
|---|---|
| `source-snapshots/` | Facts extracted from LilyGO's BSP at a pinned commit, so no future work depends on re-cloning ~192 MB of unlicensed repositories |
| `datasheets/` | **Deliberately empty.** Chip documents describe a *component*, not this board, and are filed at [`components/canaan/k230/artifacts/`](../../../../components/canaan/k230/artifacts/) |
| `schematic/` | **Empty, and this is a finding.** LilyGO publishes no schematic for this board — the wiki's `#schematic` heading has no content beneath it. Tracked as [`GC-5`](../gaps-and-conflicts.md) |
| `firmware/` | **Empty.** LilyGO ships **no** factory system image; the only prebuilt binaries are the nRF52840 UF2 and bootloader, which live in a companion repository and are recorded in [`acquisition/manifest.json`](../acquisition/manifest.json) |
| `originals/` | Empty |

## Why so little is vendored

Three independent reasons, all recorded rather than assumed:

1. **Licence.** Not one of the four LilyGO repositories for this product carries a `LICENSE`
   file. Redistribution status is `unknown` for their source *and* for the prebuilt firmware.
2. **Size.** The BSP is ~110 MB before its ~100 MB SDK submodule; `T-Display-K230_canmv_rt` is
   745 MB.
3. **Reproducibility.** Everything is available at a pinned commit and reacquisition is
   `automatic` for every item that exists at all.

The three items whose reacquisition is **`lost`** — the schematic, `K230_PINOUT_V1.0_20230524`,
and a factory image — are lost because **they were never published**, not because they were
missed.

## Where the chip documents actually are

[`components/canaan/k230/artifacts/`](../../../../components/canaan/k230/artifacts/) — seven
Markdown documents with a `SHA256SUMS` file, plus
[`CANAAN-EDA-SET.md`](../../../../components/canaan/k230/artifacts/CANAAN-EDA-SET.md), which
enumerates 22 Canaan reference-board EDA files with exact byte sizes and two reacquisition URLs
each.
