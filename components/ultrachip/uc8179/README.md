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
