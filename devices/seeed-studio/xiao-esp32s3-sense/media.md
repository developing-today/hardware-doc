# Media — XIAO ESP32S3 Sense

> Visual identification and reference imagery. Snapshot **2026-08-24**.
> Machine-readable index with hashes and source URLs: [`media/manifest.json`](media/manifest.json). **14 images, ~19 MB.**

## Rights

| Group | Source | Licence | Redistribution |
|---|---|---|---|
| Block diagram | Extracted from the CC BY-SA 4.0 schematic package | **CC BY-SA 4.0** | `allowed` (attribution: Seeed Studio) |
| Official pinout diagrams | `files.seeedstudio.com/wiki/...` | none stated | **`unknown`** |
| Product / assembly photography | `files.seeedstudio.com/wiki/...` | none stated | **`unknown`** |

No watermarks were removed and no image was altered other than renaming. Original filenames are recorded in the manifest.

## Block diagram — the one worth knowing about

![Block diagram of the XIAO ESP32S3 Sense v1.5 showing the ESP32-S3R8 SoC, GD25Q64 flash, USB-C, charger and buck-boost on the mainboard, connected via the 30-pin board-to-board connector to the camera, PDM microphone and microSD slot on the Sense daughterboard](media/block-diagram-v1.5.png)

**`media/block-diagram-v1.5.png`** — Seeed's own architecture diagram for board revision v1.5.

This is **not published anywhere on the wiki or the product page**. It ships inside the `SCH&PCB` KiCad package as a `.drawio` file plus a rendered PNG, where nobody looks. It is the clearest single overview of the board's architecture that exists.

The editable source is also retained as [`media/block-diagram-v1.5.drawio`](media/block-diagram-v1.5.drawio) — open it at <https://app.diagrams.net> to modify. Because it comes from the CC BY-SA 4.0 schematic package, it is the one image here you can confidently reuse with attribution.

## Official pinout diagrams

High-resolution, and the most practically useful images Seeed publishes.

| File | Shows |
|---|---|
| `XIAO_ESP32-S3_Sense_front_pinout.png` (5.1 MB) | **Sense**, front — pin labels and functions |
| `XIAO_ESP32-S3_Sense_back_pinout.png` (2.1 MB) | **Sense**, back — including the `BAT+`/`BAT−` pads |
| `XIAO_ESP32-S3_front_pinout.png` (2.7 MB) | Plain XIAO ESP32S3, front |
| `XIAO_ESP32-S3_back_pinout.png` (2.1 MB) | Plain XIAO ESP32S3, back |
| `XIAO_ESP32-S3_Plus_front_pinout.png` (2.5 MB) | **Plus** variant, front — 18 GPIO |
| `XIAO_ESP32-S3_Plus_back_pinout.png` (2.6 MB) | Plus variant, back |
| `xiao-esp32s3-sense-pinout.jpg` (118 KB) | Compact combined pinout |

The Plus diagrams are included deliberately: the Plus is the most likely alternative purchase, and its **B2B connector is not compatible with the Sense camera board** — comparing the two back views makes the difference visible. See [`comparisons-and-recommendations.md` §6](comparisons-and-recommendations.md#6-versus-the-xiao-esp32s3-plus--examined-from-the-schematics).

> ⚠ **These diagrams are vendor-maintained artwork, not generated from the netlist.** Where they disagree with [`pinouts-and-buses.md`](pinouts-and-buses.md), prefer the netlist-derived tables — the wiki has [demonstrable pin errors](gaps-and-conflicts.md), such as listing the microSD `CS` as GPIO3 in one section and GPIO21 in another.

## Product and assembly

| File | Shows |
|---|---|
| `xiaoesp32s3sense.jpg` | Product shot — the board as sold |
| `xiao-esp32-s3-sense-overview.png` | Annotated feature overview |
| `sense-daughterboard-detached.jpg` | **Mainboard and daughterboard separated** — the clearest view of the two-board sandwich |
| `b2b-connector-detail.png` | Close-up of the board-to-board connector region |
| `sense-assembly.png` | Assembly / mating |

`sense-daughterboard-detached.jpg` is the most useful for identification: it shows that the camera, microphone and microSD are all on the removable board, and that the mainboard alone is a plain XIAO ESP32S3.

## Board renders (from the archived 3D models)

| File | Shows |
|---|---|
| [`board-bottom-view.jpg`](media/board-bottom-view.jpg) | **Bottom face — the most legible view of the labelled pads anywhere.** `MTDO` `MTDI` `GND` `EN` `MTCK` `MTMS` `D+` `D−` and `BAT +/−` |
| [`board-top-view.jpg`](media/board-top-view.jpg) | Top face — shield can with `FCC ID:Z4T-XIAOESP32S3`, `R`/`B` button silkscreen, U.FL connector, B2B footprint |
| [`sense-assembled-render.jpg`](media/sense-assembled-render.jpg) | Sense stack assembled, camera fitted |

These were mined out of Seeed's 3D-model ZIPs before those were archived — see
[`artifacts/cad/ARCHIVED-3D-MODELS.md`](artifacts/cad/ARCHIVED-3D-MODELS.md). The bottom view
is what confirmed that **all four JTAG signals are broken out as user pads**, qualifying the
"no JTAG on the Sense" limitation. The STEP solids remain archive-only.

## What is missing

Stated plainly:

- ~~No PCB photography~~ — **partly resolved**: the vendor 3D renders above show both faces clearly. Still no *teardown* or daughterboard component close-ups, no daughterboard component close-ups. This is why the [microphone part number](gaps-and-conflicts.md#7-microphone-part-number-not-established--resolved-2026-08-24) remains unidentified: a single sharp photo of the daughterboard silkscreen would likely settle it.
- **No revision-marking photographs** — nothing showing how to tell a v1.1 board from a v1.3 in hand.
- **No thermal imagery**, despite thermals being a [recurring community complaint](community.md#42-a-hard-thermal-datum).
- **No independent photography.** Everything here is vendor-produced, so it shows the product as marketed. Note the product photos show the **OV2640-era** camera; current units ship an OV3660.

Regulatory filings (FCC internal photos) would supply several of these and were not mined.

## Related
- [`media/manifest.json`](media/manifest.json) — hashes, source URLs, original filenames
- [`pinouts-and-buses.md`](pinouts-and-buses.md) — authoritative netlist-derived pin data
- [`README.md`](README.md) — device overview
