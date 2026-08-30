# Archived 3D model ZIPs — reacquisition record

> Moved out of the repository **2026-08-28**, not deleted. **Mined first** — the useful
> images are now in [`../../media/`](../../media/); only the bulky STEP/PNG payloads left.

## What was archived

| File | Bytes (ZIP) | Bytes (uncompressed) | SHA-256 (of the ZIP) | Contains |
|---|---:|---:|---|---|
| `xiao-esp32s3-sense-3d-model.zip` | 8 832 441 | 8 830 621 | `773c16cb7518a3a18df926979f24c7e224f19309aad69962ec8a54454e288c59` | `Seeed Studio XIAO-ESP32-S3-Sense.step` (5.7 MB), `.png` render (3.0 MB), `S3 Sense.jpg` |
| `xiao-esp32s3-3d-model.zip` | 4 382 912 | 4 381 720 | `0d552ed2cc7359ea132601f4f7fe2c9d816e2dfe4f58f6463e83f84a901d3650` | `XIAO-ESP32S3 v2.step` (1.3 MB), `XIAO-ESP32S3.png` (2.8 MB), `Top view.jpg`, `Bottom View.jpg` |

> **Verify against the ZIP column.** These files are barely compressible (STEP and PNG payloads),
> so the two byte counts differ by only ~1.8 KB — close enough to mistake one for the other.
> An earlier revision of this record listed the *uncompressed* totals under a plain "Bytes"
> heading, which would have failed a `sha256sum`/size check on a re-fetched ZIP.

Archive path: `../hardware-doc-archive/doc/hardware/devices/seeed-studio/xiao-esp32s3-sense/artifacts/cad/`

## Reacquisition

```bash
B=https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res
curl -fsSL "$B/seeed-studio-xiao-esp32s3-sense-3d_model.zip" -o xiao-esp32s3-sense-3d-model.zip
curl -fsSL "$B/seeed-studio-xiao-esp32s3-3d_model.zip"       -o xiao-esp32s3-3d-model.zip
```

Retrieved 2026-08-24, from the wiki's *Resources → Mechanical Design* section.

## What was extracted before archiving

These ZIPs were **initially archived unmined** — checking them first turned up a genuinely
useful finding, which is why the mine-before-archive step exists.

| Extracted to | What |
|---|---|
| [`media/board-bottom-view.jpg`](../../media/board-bottom-view.jpg) | **The most legible view of the bottom-side pads that exists.** Clean vendor render showing `MTDO`, `MTDI`, `GND`, `EN`, `MTCK`, `MTMS`, `D+`, `D−` and `BAT +/−` silkscreen |
| [`media/board-top-view.jpg`](../../media/board-top-view.jpg) | Top face — shield can with `Model:XIAO-ESP32-S3` / `FCC ID:Z4T-XIAOESP32S3`, `R`/`B` button markings, U.FL connector, B2B footprint |
| [`media/sense-assembled-render.jpg`](../../media/sense-assembled-render.jpg) | Sense stack assembled, camera fitted |

**The finding:** the bottom-view render confirms **all four JTAG signals are broken out as
labelled user pads** on the mainboard. That materially qualifies the "no JTAG on the Sense"
limitation — the debug port is deliberately exposed, and is only consumed when the daughterboard
is attached. Documented at
[`pinouts-and-buses.md` § The bottom side carries labelled JTAG pads](../../pinouts-and-buses.md#the-bottom-side-carries-labelled-jtag-pads).

The same pads appear in the [FCC internal photos](../../regulatory-and-certification.md), but at
709 × 531 px the labels are barely readable; this render is the better reference.

## What remains only in the archive

The **STEP files** (5.7 MB + 1.3 MB) — full mechanical solids for enclosure design, fit checks
and CAD assembly. Not needed for firmware or electrical work, and not mineable into Markdown.
Refetch them if you are designing an enclosure.

Board outline is already documented without them: **17.78 × 21.14 mm**, derived from the KiCad
`Edge.Cuts` layer — see [`bom-and-board-construction.md`](../../bom-and-board-construction.md).
The high-resolution PNG renders (2.8 / 3.0 MB) are decorative duplicates of the JPGs kept in `media/`.
