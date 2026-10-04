# UltraChip UC8179 — e-paper display controller (800×480 class)

- **Category:** electrophoretic display driver / timing controller.
- **Manufacturer:** UltraChip Inc.
- **Research status:** ⚠ **Identified from firmware source and a live register
  read.** No datasheet retrieved.
- **Retrieved:** 2026-09-04

The controller found in **newer production batches of the Xteink X4, X4 Pro and
X4 Classic**, in place of the Solomon Systech SSD1677 the same boards originally
shipped.

## 1. What is established

| Property | Value | Evidence |
|---|---|---|
| Function | Mono e-paper timing controller, UC81xx KW command family | FreeInk SDK |
| Panel | 800 × 480 on these boards | board profiles |
| Readable ID registers | **`VER (0x70)`** — reserved `0x00`, `CHIP_VER`, 24-bit `LUT_VER`; **`FLG (0x71)`** status, `BUSY_N` = D0 | `XteinkDetect.cpp` |
| Bulk MTP read | **`RMTP (0xA2)`** — 1 dummy byte then MTP[0..n]; `0xA5` at byte 0 indicates a programmed MTP | `XteinkDetect.cpp` |
| `LUT_VER` value | **`0x01`** per the vendor reference | `XteinkDetect.cpp:373-390` |
| **Observed on a shipping X4 Pro** | **`VER = 00 00 01 FF FF`, `FLG = 0x13`** | FreeInk SDK, firsthand |
| Serial write clock used | 20 MHz on Xteink boards | board profiles |
| NVS `screenType` code | **1**, or **0x0B** | `XteinkDetect.cpp` |

## 2. The `CHIP_VER = 0x00` finding — a preserved negative result

An earlier version of the FreeInk matcher required `ver[1] != 0`, on the
reasonable assumption that `CHIP_VER` would carry the datasheet default. A
**shipping X4 Pro carrying a UC8179 returned `CHIP_VER = 0x00`** and was wrongly
rejected, falling back to the SSD1677 driver and producing a blank panel.

The matcher now deliberately **pins no specific `CHIP_VER` value**:

```c
// XteinkDetect.cpp:113-119
bool matchUc81xx(const uint8_t ver[5], uint8_t flg) {
  if (flg == 0x00 || flg == 0xFF) return false;   // floating bus
  if ((flg & 0x01) != 0x01) return false;         // BUSY_N must be idle
  return !verIsFloating(ver);                     // VER must be driven
}
```

**Do not reintroduce a `CHIP_VER` equality check.** This is the most reusable
lesson in the UC81xx records here.

## 3. Datasheet

**Not retrieved.** No UltraChip public portal was located; module-vendor mirrors
(Good Display, Waveshare) are the usual route. Recorded as an open acquisition.

## 4. Caveats

- **`VER`/`FLG` readability is the whole basis of controller auto-detection.** It
  requires a bus where the host can release its data line to input mid-transaction
  — which the **Xteink X4 Classic cannot do** (no MISO, and its bus geometry
  prevents the half-duplex read). On that board, NVS is the only source of truth.
- `LUT_VER` `0x01` distinguishes it from the UC8279's `0x02`/`0x68`/`0x69`.
  **Anything unrecognised falls back to UC8179**, on the empirical grounds that it
  is *"the variant every unit benched so far has carried"*.

---

## Used By

### [Xteink X4 Pro](../../../devices/xteink/x4-pro/README.md) — newer batches

Alternative to the SSD1677 on identical wiring
(SCLK 12 / MOSI 11 / CS 13 / DC 18 / RST 14 / BUSY 6). Selected at boot by the
`VER`/`FLG` probe. **Observed on real hardware returning `VER = 00 00 01 FF FF`.**
→ [`devices/xteink/x4-pro/features/display.md`](../../../devices/xteink/x4-pro/features/display.md)

### [Xteink X4](../../../devices/xteink/x4/README.md) — newer batches

Same role, on the C3 board's pins
(SCLK 8 / MOSI 10 / CS 21 / DC 4 / RST 5 / BUSY 6).
→ [`devices/xteink/x4/features/display.md`](../../../devices/xteink/x4/features/display.md)

### [Xteink X4 Classic](../../../devices/xteink/x4-classic/README.md) — batch-dependent

**Cannot be probed on this board** — the X4C display bus has no MISO, so `VER`
always floats to `0xFF`. Selected instead from NVS `hw_calib/screenType` = **1**
or **0x0B**. This makes cross-unit full-flash restores hazardous on the X4C.
→ [`devices/xteink/x4-classic/README.md`](../../../devices/xteink/x4-classic/README.md)

## See also

[`../uc8279/README.md`](../uc8279/README.md) ·
[`../../solomon-systech/ssd1677/README.md`](../../solomon-systech/ssd1677/README.md) —
the part it substitutes for · [`../README.md`](../README.md)

---

## Datasheet — obtained 2026-09-11

The record above stated *"No datasheet retrieved."* **One has now been obtained,
validated and retained.**

| Field | Value |
|---|---|
| Local path | [`artifacts/uc8179c-c-datasheet-rev0.6-2019-11-26-crystalfontz-mirror.pdf`](artifacts/uc8179c-c-datasheet-rev0.6-2019-11-26-crystalfontz-mirror.pdf) |
| **SHA-256** | `bf1dcef76e0d02a5683814e5f2b525bb7079e57509bf9a0754235b24fa587f50` |
| **Bytes** | **1,202,516** |
| Pages | **81**, A4 |
| Source URL | <https://www.crystalfontz.com/controllers/UltraChip/UC8179/517/> |
| Source class | **credible mirror** — Crystalfontz is a display distributor, not UltraChip |
| Retrieved | **2026-09-11**, HTTP 200, magic bytes `%PDF` |
| **Document title (PDF metadata)** | `03-DTS-1664  UC8179c_Ｃ0.6 for__TFT_Module_Use_only` (note the full-width `Ｃ`) |
| **IC version** | **`c_C`** |
| **Datasheet revision** | **0.6**, dated **November 26, 2019** |
| PDF `CreationDate` | 2019-12-05 00:13:59 |
| PDF author / producer | `cindy.lu` / PDFCreator 2.5.3.6324 |
| Redistribution status | **`conditional` / `unknown`** — cover marked ***"for TFT Module Use Only"*** |
| Disposition | `repository`, **unstaged** |

**Text-layer validated** against the rendered page-1 heading
(*"HIGH-VOLTAGE MIXED-SIGNAL IC"*, *"IC Version: c_C"*,
*"Datasheet Revision: 0.6 (for_TFT_Module_Use_Only) November 26, 2019"*).

### This is the `c_C` silicon — and that matters for the Xteink boards

The FreeInk driver's notes refer to *"the UC8179c table"* when interpreting the
PLL (`0x30`) register. **This document is that part.** The X4 Pro, X4 Classic and
X4 all ship UC8179 in some production batches; whether they ship `c_C`
specifically is **not established** — no top marking has been read off any
Xteink board, because the only public board photographs are the FCC internal
photos of the X3 and X4, which have not been read at that level of detail.

### How it was found — a trap worth recording

`https://www.crystalfontz.com/controllers/UltraChip/UC8179/478/` returns a
**valid 477 KB PDF**, and it is **the GOODiX GT911 Programming Guide**. The
`UC8179` path segment is decorative; only the trailing number selects a document.
The correct id is `517`, read from the page's own
`datasheet-viewer.php?id=517` link. `datasheet-viewer.php?id=517` itself returns
HTML, not the PDF — the working form is the trailing-number path.

**Validating by magic bytes alone would have filed a touch-controller manual as a
display-controller datasheet.** Always check the PDF's own title.

Crystalfontz carries only **UC8151** (id 511) and **UC8179** (id 517) from
UltraChip. It does **not** carry UC8253 or UC8279.

**Used by:** [Xteink X4](../../../devices/xteink/x4/README.md) ·
[X4 Pro](../../../devices/xteink/x4-pro/README.md) ·
[X4 Classic](../../../devices/xteink/x4-classic/README.md) — all three as one of
three batch-dependent controller options.

---

## Archive copy, and the "UC8179C" naming trap — audited 2026-09-20

### The archived copy is a byte-identical duplicate of the retained artifact

The Xteink research scratch batch holds a second copy of this document under a
different filename. It had never been cited by any record. It is **not** a second
revision and **not** a second source — it is the same bytes.

| | Retained artifact | Archived copy |
|---|---|---|
| Path | `artifacts/uc8179c-c-datasheet-rev0.6-2019-11-26-crystalfontz-mirror.pdf` | `archive/devices/xteink/shared-artifacts/research-scratch/datasheets/uc8179c-datasheet-v0.6-crystalfontz.pdf` |
| **SHA-256** | `bf1dcef76e0d02a5683814e5f2b525bb7079e57509bf9a0754235b24fa587f50` | **identical** |
| **Bytes** | 1,202,516 | **identical** |
| Pages | 81 | 81 |

Verified 2026-09-20 by `sha256sum` **and** by `cmp` over the full files —
`executed-success`. Both are the same Crystalfontz fetch (id `517`); the archived
one is the working copy the acquiring pass downloaded, the retained one is the
copy it promoted. **Disposition: left in place.** Moving it would strip a file out
of a scratch tree whose relocation is certified by a recorded, locale-pinned tree
digest (`43841e95f52e…`, 505 files), and would create no copy that does not
already exist at the canonical component path. See
[`README.ARCHIVE.md`](../../../archive/devices/xteink/shared-artifacts/research-scratch/README.ARCHIVE.md),
which already flagged this file as a chip document whose home is
`components/ultrachip/uc8179/artifacts/` — it is now there, so that task is closed.

> ⚠ **The "Crystalfontz raster banner" caveat does not apply to this file.**
> Crystalfontz is known to stamp a raster banner onto page 1 of some mirrored
> datasheets, which defeats text-based comparison and prevents a hash match.
> **This document has no image on page 1 at all**: `pdfimages -list -f 1 -l 1`
> returns zero rows, and the first raster object in the file is the block diagram
> on **p. 4**. 1,118 image objects exist across 81 pages, none on the cover.
> `executed-success`, 2026-09-20.

### ⚠ There is no part called "UC8179C". The part is UC8179

Both filenames above, and this record's own artifact name, contain a `c` that
looks like a part-number suffix. It is not one. Checked against the document
itself before any merge or variant record was considered:

| Evidence | Page | Reading |
|---|---|---|
| **Ordering information — the only part numbers in the document** | **p. 5** | `UC8179cGAC-U0X3-3` and `UC8179cGAC-U0X3-4`, differing only by 3″ vs 4″ waffle tray. **No `UC8179C` orderable exists** |
| Product heading and introduction | **p. 3** | *"**UC8179** — All-in-one driver IC with Timing Controller…"*, *"The **UC8179** is an all-in-one driver…"* — unsuffixed throughout |
| Cover block | **p. 1** | *"**IC Version: c_C**"* on its own line, separate from the title. `c_C` is a **field**, not part of the name |
| Running footer, all 81 pages | p. 1–81 | `UC8179c_C0.6 (for_TFT_Module_Use_Only)` — i.e. part `UC8179`, IC version `c_C`, datasheet revision `0.6` |
| PDF metadata `Title` | — | `03-DTS-1664  UC8179c_Ｃ0.6 for__TFT_Module_Use_only` (full-width `Ｃ`) — **this string is where the filename "uc8179c" came from** |

**Corroborated by the sibling part.** [UC8253](../uc8253/README.md) uses the
identical convention: cover *"IC Version: **c_A**"*, orderables
`UC8253cGAA-L0P3-3` / `-L0X3-3` / `-L0P3-4` / `-L0X3-4` (p. 5). `c_<letter>` is
UltraChip's house IC-version field across the family, and the `c` in `cGAC` /
`cGAA` is part of the orderable suffix, not of the product name.

**Conclusion:** UC8179C is **not** a distinct part from UC8179. No separate record
and no variant section is warranted; this record already covers it, and
`components/ultrachip/uc8179/` is the correct home. What *is* real is the **IC
version `c_C`**, which this record already states.

This is the second UltraChip mis-identification trap caught in this directory —
the first was `datasheet-viewer.php?id=478` serving the **GOODiX GT911 programming
guide** under a `UC8179` path (see *"How it was found"* above). Both have the same
root cause: **an UltraChip document's filename or URL is not evidence of its
part.** Read the ordering table.

### Three corrections to this record, from the same reading

1. **This is an engineering-sample document.** The cover (p. 1) reads
   ***"ES Specifications"*** — Engineering Sample — immediately left of
   *"IC Version: c_C"*. The record above did not say so. Treat the register
   defaults accordingly; this is provisional silicon documentation, in the same
   class as the SSD1680's *"Product Preview"*.
2. **The document contradicts itself on its own date by one day.** Cover:
   *"Datasheet Revision: 0.6 … **November 26, 2019**"*. Revision history (p. 81):
   *"0.6 — First release — **Nov. 25, 2019**"*. Immaterial, but it is the only
   revision-history entry in the file: **0.6 is the first and only release**, so
   there is no earlier revision to look for.
3. **Maximum geometry is 800 × 600, not "800 × 480".** Feature highlights (p. 3):
   *"Up to **800 source x 600 gate** resolution + 1 border + 1 VCOM"*, 1 bit
   white/black + 1 bit red per pixel. The `800×480` in this record's title is the
   **Xteink panel's** resolution, not the controller's limit. Supply `2.3–3.6 V`;
   OTP **6 KB** for LUTs and settings; package **COG**; bump pitch 13 µm (p. 3).
