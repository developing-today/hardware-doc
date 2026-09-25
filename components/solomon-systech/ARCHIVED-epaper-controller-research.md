# ARCHIVED: e-paper controller research, 2026-09-11

> Moved out of `scratch/`, **not deleted**. Archived **2026-09-20**; every operation was `mv`.

Working material from a pass that studied five Solomon Systech controllers together — SSD1677,
SSD1680, SSD1681, SSD1683 and SSD7317 — and whose most valuable finding is about how those five
get **confused with each other**.

## Identity

| Field | Value |
|---|---|
| Archived to | `archive/components/solomon-systech/shared-artifacts/epaper-controller-research-2026-09-11/` |
| Was at | `scratch/_rescued-from-tmp-2026-09-20/nfc-and-epaper-research/` |
| Size | **22 files, 3,123,262 bytes** |
| Tree digest | `ba2d8962991c555858430c37e848e05cd2cb74275e192f983f9b3ed4eaf34e58` |
| Gathered | 2026-09-11 · rescued from `/tmp` and filed 2026-09-20 |

A `pdftotext` of the **SSD1677 Advance Information** document (960 × 680 red/black/white EPD
driver) from the same pass is filed separately under the part it describes, at
[`ssd1677/artifacts/ssd1677-advance-information-pdftotext-2026-09-11.txt`](ssd1677/artifacts/).

Full contents table:
[`archive/components/solomon-systech/shared-artifacts/README.md`](../../archive/components/solomon-systech/shared-artifacts/README.md).

## The finding that matters, restated here so it is not missed

**Crystalfontz serves the wrong datasheet with a 200 and valid `%PDF` magic.** Its controller URLs
have the form `https://www.crystalfontz.com/controllers/<Vendor>/<Part>/<id>/`, and **only the
trailing numeric `<id>` selects a document** — `<Vendor>` and `<Part>` are decorative. A wrong id
returns a *different part's* datasheet, with `Content-Type: application/pdf` and a real PDF body.

Magic-byte validation does not catch it. `pdfinfo Title` does not catch it — one of these files is
a genuine SSD1683 whose `Title` metadata claims `SSD1780`, a part that does not exist. **Only
first-page text catches it.**

Two files in this pass sat under the wrong part number for nine days as a result:

| Was named | Actually is | Filed as |
|---|---|---|
| `ssd1680.pdf` | **SSD7317** Rev 1.3 — an OLED/PLED driver with integrated touch, **not an e-paper part**; and an 87-page bundle, not one document | [`ssd7317/artifacts/`](ssd7317/README.md) |
| `ssd1677.pdf` | **SSD1681** Rev 0.13 | [`ssd1681/artifacts/`](ssd1681/README.md) |
| `ssd1683.pdf` | SSD1683 Rev 1.0 ✅ | [`ssd1683/artifacts/`](ssd1683/README.md) |
| `SSD1680_gh.pdf` | SSD1680 Rev 0.14 ✅ | [`ssd1680/artifacts/`](ssd1680/README.md) |
| `ssd1677_real.pdf` | SSD1677 Rev 1.0 ✅ — a second, byte-different rendering | [`ssd1677/artifacts/`](ssd1677/README.md), kept **alongside** the existing M5Stack mirror |

The `_real` suffix records that the acquiring session **already hit this and refetched** — but it
never renamed the bad file, so an SSD1681 sat there looking authoritative. Written up with a
one-command verification recipe and a live-verified id table in
[`vendors/solomon-systech/README.md` §2–§3](../../vendors/solomon-systech/README.md).

## ⚠ Do not cite the text extractions in the archive

Four `.txt` files remain there under the **old, partly-wrong names**: `ssd1677.txt` is **SSD1681**
text and `ssd1680.txt` is **SSD7317** text. They are kept, not deleted — but regenerate from the
filed PDFs instead of using them.

Five files named `*.bin` in that directory are also **all HTML**, including a 548-byte **404
body**. None is firmware or a waveform LUT.

## ⚠ And a caution about the CSDN articles

Eleven saved CSDN articles on SSD1680/SSD1683 driving, greyscale and voltage tuning are in that
directory and were mined into
[`devices/m5stack/papermono/gaps-and-conflicts.md`](../../devices/m5stack/papermono/gaps-and-conflicts.md).
That record establishes that **three of the SSD1683 voltage articles are AI-generated rewrites of
one free 2024 original**, and that they add claims the original does not make. Cite the original.

## How to get it back

| Route | Reliability |
|---|---|
| Local archive — `mv "archive/components/solomon-systech/shared-artifacts/epaper-controller-research-2026-09-11" .` | exact bytes |
| Regenerate the `.txt` extractions — `pdftotext -layout <filed pdf>` | exact, and **correctly named** |
| The five datasheets themselves | already in the repository or archive under their parts, each hashed |
| The CSDN articles | ⚠ CSDN paywalls and rewrites content; the captures are dated 2026-09-11 and may not be reproducible |
| Good Display `GDEM0097F51_ESP32` sample-code page | <https://www.good-display.com/> — **never examined by any pass** |
