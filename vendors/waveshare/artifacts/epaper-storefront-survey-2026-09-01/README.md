# Waveshare e-paper / ESP32 storefront survey — 2026-09-01

Dated `waveshare.com` storefront captures for the **ten products** that the 2026-09-01
e-paper survey enumerated as the candidate population. They are the primary evidence behind
that enumeration, and they are the only dated market record held for most of these SKUs.

Retrieved **2026-09-01** by the pass working in `archive/devices/waveshare/shared-artifacts/epaper-esp32/research-scratch/`. Filed into
the repository **2026-09-20**; until then all ten existed only in scratch, including the four
that four stub device records had been written from.

## Why the set is split across three places

A storefront page describes **a product**, so it belongs to that product's record wherever one
exists. Only the products with no record of their own are held here, under the vendor.

| Product | Capture | Filed to |
|---|---|---|
| ESP32-S3 3.97inch e-Paper | `storefront-esp32-s3-epaper-3.97-2026-09-01.html` | [`devices/waveshare/esp32-s3-epaper-3.97/artifacts/source-snapshots/`](../../../../devices/waveshare/esp32-s3-epaper-3.97/artifacts/source-snapshots/) — filed 2026-09-01 |
| e-Paper ESP32 Driver Board | `storefront-e-paper-esp32-driver-board-2026-09-01.html` | [`devices/waveshare/e-paper-esp32-driver-board/artifacts/source-snapshots/`](../../../../devices/waveshare/e-paper-esp32-driver-board/artifacts/source-snapshots/) |
| ESP32-S3 1.54inch e-Paper | `storefront-esp32-s3-epaper-1.54-2026-09-01.html` | [`devices/waveshare/esp32-s3-epaper-1.54/artifacts/source-snapshots/`](../../../../devices/waveshare/esp32-s3-epaper-1.54/artifacts/source-snapshots/) |
| ESP32-C6 1.54inch e-Paper | `storefront-esp32-c6-epaper-1.54-2026-09-01.html` | [`devices/waveshare/esp32-c6-epaper-1.54/artifacts/source-snapshots/`](../../../../devices/waveshare/esp32-c6-epaper-1.54/artifacts/source-snapshots/) |
| ESP32-S3-PhotoPainter 7.3inch E6 | `storefront-esp32-s3-photopainter-2026-09-01.html` | [`devices/waveshare/esp32-s3-photopainter/artifacts/source-snapshots/`](../../../../devices/waveshare/esp32-s3-photopainter/artifacts/source-snapshots/) |

The five below have **no device record**, so they are held here rather than left stranded.

| File | Bytes | SHA-256 (short) | Product, per its own `<title>` |
|---|---:|---|---|
| `storefront-e-paper-esp8266-driver-board-2026-09-01.html` | 211,012 | `b8ea240a…` | Universal e-Paper Driver Board, **ESP8266** onboard — the non-ESP32 sibling of the driver board |
| `storefront-esp32-s3-epaper-13.3e6-2026-09-01.html` | 203,603 | `5711e225…` | 13.3inch Full Colour E-Paper (**E6**) with ESP32-S3 e-Paper driver board |
| `storefront-esp32-s3-epaper-1.54g-2026-09-01.html` | 196,678 | `ea6228d5…` | ESP32-S3 1.54inch e-Paper **(G)**, 200 × 200, four-colour — the colour variant of the 1.54 above |
| `storefront-photopainter-b-2026-09-01.html` | 193,366 | `f11b1ad2…` | 7.3inch **E6** full-colour e-paper in a solid-wood frame (no ESP32-S3 in the name) |
| `storefront-photopainter-2026-09-01.html` | 190,369 | `a457cba4…` | 7.3inch **ACeP 7-colour** e-paper in a solid-wood frame — the older panel generation |

Exact sizes and SHA-256 values are in `manifest.tsv` beside this file.

## What these establish, and what they do not

**Establish:** that each product existed and was listed on `waveshare.com` on 2026-09-01, with
the marketed name, resolution, colour capability and headline feature claims in its `<title>`
and page body. They are the basis for the survey's claim to have enumerated the population.

**Do not establish:** anything about the hardware inside. A storefront listing is vendor
marketing prose — the weakest class in the source hierarchy. No schematic, no part number and
no pin assignment should be taken from these files. The three PhotoPainter/ACeP entries in
particular are *not* ESP32 boards and were captured only to bound the search.

**Pricing was not extracted.** These captures were taken for enumeration, not price sampling,
and no dated price observation has been read out of them.

## Retrieval note

The population was enumerated through `catalogsearch`, **not** through
`waveshare.com/product/displays/e-paper.htm`, which returns HTTP 200 and ~244 KB containing
**zero product links** because the listing is JS-rendered. That trap and the rest of the
Waveshare host map are in [`vendors/waveshare/README.md`](../../README.md).
