# UltraChip UC8253 — e-paper display controller

- **Category:** electrophoretic (e-paper) display driver / timing controller.
- **Manufacturer:** UltraChip Inc.
- **Research status:** ⚠ **Identified from firmware and driver source only.** No
  datasheet was retrieved in this session; the specification below is what the
  FreeInk SDK cites and implements.
- **Retrieved:** 2026-09-04

The panel controller of the **original-production Xteink X3**.

## 1. What is established

| Property | Value | Evidence |
|---|---|---|
| Function | Mono e-paper timing controller, KW (black/white) mode | driver source |
| Interface | 4-wire SPI, write-oriented | driver source |
| **Max serial write clock** | **20 MHz** — *"Clock rate up to 20 MHz"*, serial write timing `TSCYCW` | UC8253 datasheet, cited by FreeInk SDK |
| Mode used | `PSR KW/R = 1`: 1 bpp, `DTM1` = OLD plane, `DTM2` = NEW plane, **differential refresh** | `Uc8253Driver` |
| Command set | `PSR`, `PON`, `POF`, `DTM1 0x10`, `DSP 0x11`, `DRF 0x12`, `DTM2 0x13`, `CDI 0x50`, `TRES 0x61`, `DSLP 0x07`+`0xA5` | driver source |
| Waveforms | The X3 driver carries **six tuned custom banks**, in the UC8253's **43-byte LUT format** | `docs/xteink-x3-uc8279-support.md` |
| Grayscale | **Supported** on this part — the X3 reader's **4-level anti-aliasing** path uses it | same |
| **`VER (0x70)` behaviour** | **UNKNOWN.** See §3 | same, marked `Pending` |

## 2. Datasheet

**Not retrieved.** The FreeInk SDK cites:

`https://www.elecrow.com/download/product/DIE01237S/UC8253_Datasheet.pdf`

— an **Elecrow mirror**, not an UltraChip-hosted document. No UltraChip public
portal was located. Retrieval status: `not-attempted` this session; recorded so a
future pass can fetch and hash it. Expect the usual mirror caveat: the revision a
module vendor serves may lag the chip maker's.

## 3. The open question about `0x70`

The Xteink X3 boot probe distinguishes UC8253 from UC8279d by issuing `VER (0x70)`
and checking for a structured, non-floating reply. It works — but the FreeInk
maintainers flag an assumption they have not tested:

> "**Pending:** what the UC8253 actually answers to `0x70` (UC815x-family REV
> places the revision in the first byte, which the matcher relies on)…"

So the detection is **empirically reliable and theoretically unverified**. If a
UC8253 ever answers `0x70` with a driven, structured byte pattern, the matcher
would misidentify it as an UltraChip sibling. Recorded as a live risk, not a
defect.

## 4. Caveats and unsafe assumptions

- **Its LUT format is incompatible with the UC8279's.** UC8253 uses 43-byte LUTs;
  the UC8279 uses **group-based** 7-byte groups, 7 groups per LUT in KW mode.
  Tuned waveform banks **cannot be copied between them**, despite a nearly
  identical command set. This is the single most expensive trap in porting between
  the two.
- Do not assume grayscale carries over to the UC8279 — it does not, yet.

---

## Used By

### [Xteink X3](../../../devices/xteink/x3/README.md) — original production run

Chip-on-glass inside the 3.7″ 792×528 module; **no board reference designator**.
Driven by the ESP32-C3 over the SPI bus it **shares with the microSD card**:

| Controller signal | X3 GPIO |
|---|---:|
| SCLK | 8 |
| SDA (MOSI) | 10 |
| CS | 21 |
| DC | 4 |
| RST | 5 |
| BUSY | 6 |

`displaySpiHz` = **20 MHz** (datasheet maximum). A prior fork ran 16 MHz;
20 MHz is in-spec and ~25 % faster on plane writes.

Selected at boot: if the display-bus probe does **not** find an UltraChip
`VER`/`FLG` signature, the SDK conservatively resolves to this part.

→ [`devices/xteink/x3/features/display.md`](../../../devices/xteink/x3/features/display.md)
→ [`devices/xteink/x3/pinouts-and-buses.md`](../../../devices/xteink/x3/pinouts-and-buses.md)

## See also

[`../uc8279/README.md`](../uc8279/README.md) — the part that replaced it in
~July 2026 production · [`../README.md`](../README.md)

---

## Datasheet — retrieved 2026-09-11

The record above listed `https://www.elecrow.com/download/product/DIE01237S/UC8253_Datasheet.pdf`
with retrieval status `not-attempted`. **It has now been fetched, validated and
retained.**

| Field | Value |
|---|---|
| Local path | [`artifacts/uc8253c-a-datasheet-rev0.6-2020-10-13-elecrow-mirror.pdf`](artifacts/uc8253c-a-datasheet-rev0.6-2020-10-13-elecrow-mirror.pdf) |
| **SHA-256** | `bee25538177b8cc6f67c1ffe696d8fd09bda7842b42e021fb9bd41a3da91c125` |
| **Bytes** | **1,294,916** |
| Pages | **75**, A4 (595 × 842 pt) |
| Source URL | <https://www.elecrow.com/download/product/DIE01237S/UC8253_Datasheet.pdf> |
| Source class | **credible mirror** — Elecrow is a module vendor, not UltraChip |
| Retrieved | **2026-09-11**, HTTP 200, magic bytes `%PDF` |
| **Document title (PDF metadata)** | `03-DTS-1891 UC8253c_A0.6 for TFT module use only` |
| **IC version** | **`c_A`** |
| **Datasheet revision** | **0.6**, dated **October 13, 2020** |
| PDF `CreationDate` | 2020-10-20 21:43:51 |
| PDF author / producer | `matthew.lin` / PDFCreator Free 3.5.1 |
| Cover text | *"HIGH-VOLTAGE MIXED-SIGNAL IC — All-in-one driver IC w/ Timing Controller for White/Black/Red Dot-Matrix Micro-Cup ESL"* |
| Redistribution status | **`conditional` / `unknown`** — the cover is marked ***"for TFT module use only"***, which is a use restriction of unclear scope, not a licence |
| Disposition | `repository`, **unstaged** |

**Text-layer validation performed.** `pdftotext -layout` on page 1 returns the
same heading visible in the rendered page (*"HIGH-VOLTAGE MIXED-SIGNAL IC"*,
*"IC Version: c_A"*, *"Datasheet Revision: 0.6 … Oct 13, 2020"*). No value has
been transcribed from an unvalidated text layer.

### Two things the metadata tells you that the content does not

1. **This is the `c_A` silicon**, not an unqualified "UC8253". UltraChip's
   internal document number is `03-DTS-1891`. If the X3's fitted part is a
   different sub-revision, register defaults may differ.
2. **It was exported by a named UltraChip employee with a consumer PDF tool in
   October 2020** and has circulated through module vendors ever since. **There is
   no UltraChip customer portal**; this is the distribution channel.

### Relationship to the UC8179 datasheet now held

[`../uc8179/`](../uc8179/README.md) holds `03-DTS-1664 UC8179c_C0.6`, from a
different mirror. The two share a document template, a revision number (0.6), a
cover, and the *"for TFT module use only"* marking — they are siblings from one
document family. **They are different parts and different documents**; the shared
`0.6` is a coincidence of UltraChip's numbering, not a common revision.

**Used by:** [Xteink X3](../../../devices/xteink/x3/README.md).
