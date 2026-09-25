# ARCHIVED: `research-scratch/` — the research working store for this board family

> Moved out of `scratch/`, **not deleted**. Archived **2026-09-20**; every operation was `mv`.

## Identity

| Field | Value |
|---|---|
| Original path | `scratch/esp32-p4-wifi6-touch-lcd-xc/` |
| Archived to | `archive/devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/research-scratch/` |
| Type | directory |
| Size | **3,065,531 bytes** (2.92 MiB) |
| File count | **23** |
| Tree digest | `ed847572df6c0a232f90f1f20382be97ab9649878e53b252718746793eb611ad` — verified identical before and after the move |
| Gathered | 2026-08-26 (17 files), 2026-08-28 (2), 2026-08-30 (7) |

`research-scratch/` is the convention the parallel relocations used for every device subject, so
the substitution is uniform:

```
scratch/esp32-p4-wifi6-touch-lcd-xc/<anything>
  →  archive/devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/research-scratch/<anything>
```

Three records in this repository cite the old path. They were **not** edited; the map for every
relocated subject is in [`SCRATCH-RELOCATION-2026-09-20.md`](../../../../SCRATCH-RELOCATION-2026-09-20.md).

## It was 212 MB and is now 2.9 MB

Two consolidation passes removed what was reproducible, each proving the recipe first:

| Removed | Bytes | Why it was safe |
|---|---:|---|
| `downloads/ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip` | 117,768,225 | Byte-identical copy survives in [`artifacts/originals/`](ARCHIVED-originals.md) |
| `downloads/lvgl-9.3.0.zip` | 90,040,639 | Published upstream release, `lvgl/lvgl` v9.3.0 @ `c033a98afddd65aaafeebea625382a94020fe4a7` |
| `downloads/Arduino_GFX-1.6.0.zip` | 10,824,248 | Published upstream release |
| `downloads/esp_lcd_jd9365-2.0.2.zip` | 16,200 | Published component release |

All four are documented with hashes and reacquisition URLs in
[`ARCHIVED-originals.md`](ARCHIVED-originals.md). The `downloads/` directory remains as an empty
marker.

## What is in the 23 files

| Path | What | Mined? |
|---|---|---|
| `bsp-source/` (6) | Espressif BSP component `esp32_p4_wifi6_touch_lcd_xc` — `bsp_header.h`, the 36 KB `.c`, `Kconfig`, `idf_component.yml` | ✅ fully — `devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/bsp-source-findings.md` |
| `pages/` (5) | Waveshare product listing, CN shop page, docs-platform page, and two **netseye** documents on running **Linux** on this board | ✅ cited from four records |
| `failed-downloads/` (4) | **Negative evidence, correctly named** — two LCSC pages and a DuckDuckGo bot challenge saved with `.pdf` extensions, with their own README | n/a |
| `renders/` (3) | Schematic page 1 at 200 dpi, plus `J8` and RTC crops | facts promoted; images regenerable |
| `bbox.xml` (1) | `pdftotext -bbox-layout` word coordinates for the schematic | regenerable |
| `community-probe/xiaozhi-config.h` (1) | A community board config: I²S MCLK/WS/BCLK/DIN on GPIO 13/10/12/11, **24 kHz** audio rate | ✅ the pin set agrees with the BSP; the sample rate is its own contribution |
| `README.md`, `README.workspace-prior.md` (2) | The 2026-08-26 working notes and the 2026-09-20 signpost | — |

## Two claims in the old notes that are no longer true

1. `README.workspace-prior.md` describes a mirror at `~/hardware-doc-archive/workspace/`. **That
   path is gone.**
2. It says the schematic *"has no usable text layer for net tracing"*. That remains true for **net
   tracing** — GPIO-to-net mapping runs through 0 Ω resistors drawn as three separate text runs —
   but `pdftotext`, `pdfinfo` and `pdftoppm` **are** available on this host, so the text layer is
   readable for other purposes.

One thing was **not** re-verified by any pass: the claim that `renders/` regenerates via
`pdftoppm`. Unlike the `text/`, `bbox/` and FCC-photograph recipes elsewhere, it was never tested.
The renders are small and were kept, so nothing turns on it.

## How to get it back

```bash
mv "archive/devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/research-scratch" \
   "scratch/esp32-p4-wifi6-touch-lcd-xc"
```

Without the archive, the individual pieces are reacquirable:

| Piece | Source |
|---|---|
| BSP component | <https://components.espressif.com/components/espressif/esp32_p4_wifi6_touch_lcd_xc> |
| Vendor pages | <https://www.waveshare.com/esp32-p4-wifi6-touch-lcd-xc.htm> · <https://www.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-XC> |
| netseye Linux docs | the `WAVESHARE_XC.md` and `README.md` of the netseye Linux port repository |
| `renders/`, `bbox.xml` | `pdftoppm -r 200 -png` / `pdftotext -bbox-layout` on the schematic PDF, which is **in the repository** under `artifacts/schematic/` |
| `failed-downloads/` | ⚠ **not reacquirable, and that is the point** — they are captures of two LCSC bot walls and a DuckDuckGo challenge as they were on 2026-08-26 |
