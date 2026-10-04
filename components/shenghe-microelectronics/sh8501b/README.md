# Shenghe Microelectronics SH8501B

> Also seen as **`SH8501B0`** — that is LilyGO's filename, **not** a part number,
> revision or variant. The manufacturer's own ordering section says
> *"Product Code: SH8501B"*. See [§5](#5-the-b0-question-and-the-archive-duplicate--audited-2026-09-20).

- **Category:** AMOLED display driver IC — **max 240 RGB (H) × 240+ (V)**, 16.7 M colours.
- **Manufacturer:** **SHENGHE MICRO ELECTRONICS**, established from the datasheet cover.
- **Retrieved:** 2026-09-07
- **Sibling:** [`sh8601z`](../sh8601z/README.md)

The display driver of the **LilyGO T-Display AMOLED Lite (1.47″)**, 194 × 368 — and the reason
that board needs a level shifter.

## 1. Identity and artifact

| Property | Value |
|---|---|
| Part | **SH8501B.** The document's own *Ordering information* gives **"Product Code: SH8501B"** (p. 8). LilyGO's filename says `SH8501B0`; **the string `SH8501B0` does not occur once in the 168 pages** — see §5 |
| Cover page text | "CONFIDENTIAL · SHENGHE MICRO ELECTRONICS · **SH8501B** · **240RGBx240 / 16.7M color** · AMOLED Display Driver IC · Datasheet · **Preliminary Version 0.0** · User Command Set · September, 2020 · © 2020 SHENGHEMICRO" (p. 1) |
| Local artifact | [`artifacts/sh8501b0-datasheet-lilygo-mirror.pdf`](artifacts/sh8501b0-datasheet-lilygo-mirror.pdf) — 4 412 013 B, SHA-256 `663d767850d7db71252c62f9de709cbaf278a88d25048aa168f6cb5586425b41` |
| Mirror source | `Xinyuan-LilyGO/LilyGo-AMOLED-Series` → `datasheet/SH8501B0 DataSheet.pdf` @ `6d1dc008b94578cc34ba4a0f3b223dd808ca963f` |
| Marked | **CONFIDENTIAL** |
| Licence | Shenghe copyright, marked confidential; repository MIT does not cover it. **Redistribution status: `prohibited` on the face of the document** — should remain **unstaged** |

## 2. The 1.8 V problem

On the T-Display AMOLED Lite, every signal between the ESP32-S3 and this controller crosses an
**RS0108YTQC20 8-bit level translator** (`U2`). The schematic's net names make it explicit:
`AM_SPI_CSX`/`AM_SPI_CSX-1V8`, `AM_SPI_SCL`/`AM_SPI_SCL_1V8`, `AM_SPI_SD0..3`/`…_1V8`,
`TE`/`TE_1V8`, `TP_INT`/`TP_INT_1V8`.

**The panel side runs at 1.8 V.** That is not true of any other display in the family, and it
has consequences:

- Extra propagation delay and reduced maximum QSPI clock versus a direct 3.3 V link.
- The board needs an **AXP2101 PMU** partly to generate the 1.8 V rail — which is why the Lite
  is the only board in the family with a full PMU.
- Panel power sequencing is more involved, and is plausibly why LilyGO's own figures give the
  Lite a **1.1 mA** deep-sleep current against 230 µA for the 1.91″/2.41″ boards, and
  **timer-only** wake instead of external GPIO wake.

## 3. What was not verified

As of the 2026-09-07 pass: cover and table of contents only. The **2026-09-20**
audit added identity, resolution, interface and OTP facts with page citations —
see [§5](#5-the-b0-question-and-the-archive-duplicate--audited-2026-09-20).
**Still no register, timing or electrical value is transcribed**; the command set
(pp. 134–162) is unmined.
Extraction method and its pitfalls: [`vendors/lilygo/README.md`](../../../vendors/lilygo/README.md).

## 4. Used by

### LilyGO T-Display AMOLED Lite (1.47″)
→ [`devices/lilygo/t-display-amoled-lite`](../../../devices/lilygo/t-display-amoled-lite/README.md)

194 × 368, 450 nits. QSPI via the level shifter: `DISP_CS` GPIO4, `SCK` GPIO5,
`DATA0..3` GPIO 7/10/11/12, `RESET` GPIO40, `TE` GPIO6. Touch is a separate
[Chipsemi CHSC5816](../../chipsemi/chsc5816/README.md); PMU is an
[X-Powers AXP2101](../../x-powers/axp2101/README.md).
**Vendor states this board does not support hardware screen rotation.**

---

## 5. The `B0` question, and the archive duplicate — audited 2026-09-20

### ⚠ `B0` is not a revision, not a variant, and not part of the part number

The directory here is `sh8501b` while LilyGO's file is named `SH8501B0 DataSheet.pdf`.
The record above hedged this. It is now settled **against** `B0` being a suffix:

| Evidence | Page | Reading |
|---|---|---|
| **`grep -c "SH8501B0"` over the full validated text layer** | all 168 | **0 occurrences.** The string does not appear anywhere in the document |
| **Ordering information** | **p. 8** (PDF p. 9) | *"• **Product Code: SH8501B**"* · *"• Package: COF/COG"*. This is the document's only product-code statement, and it carries no `0` |
| Cover | **p. 1** | Title block reads **`SH8501B`** |
| Running header, every page | p. 1–168 | `SH8501B — 240x240 AMOLED Display Driver IC` |
| **Version History — the whole table** | **p. 7** (PDF p. 8) | A single row: **`Ver0.0` · September. 2020 · "Initial Draft"**. Footer on every page: *"Preliminary **Version 0.0**"* |

**Conclusion:** the part is **SH8501B**; the record directory `sh8501b` is correct
and needs no rename. The most economical reading of LilyGO's filename is
`SH8501B` + the document's version digit `0` (from *Preliminary Version 0.0*),
i.e. "SH8501B, v0" — but **that is `inferred`**, from the coincidence of the only
`0` in the document being its version number. What is **established** is the
negative: `B0` is **not** a documented silicon revision, package code or variant,
because the manufacturer's own ordering section names the part without it.

Note what this also means: **only one revision of this document has ever existed**
(Ver0.0, "Initial Draft", September 2020), so there is no later revision to hunt
for, and no earlier one that LilyGO might have mirrored.

### Two precisions on the specifications above

1. **Resolution.** The cover and running header say `240RGBx240`, which *appears*
   to conflict with the Lite's 194 × 368 panel. It does not. The features table
   (**p. 9**, PDF p. 10) states **"Max. 240 RGB (H) x 240+ (V)"** — the horizontal
   limit is hard at 240 RGB, the vertical is open-ended. 194 (H) × 368 (V) fits:
   194 ≤ 240, and 368 falls under "240+". Same table: **1:6 MUX operation**,
   **120 source channels with MUX**, GOA gate drive `GOAR[16:1]`/`GOAL[16:1]`,
   LTPS AMOLED rigid & flexible, Real RGB and Delta RGB pixel arrangements,
   P-MOS type panel support, 16 M colours.
2. **The QSPI path is a first-class documented interface, not an improvisation.**
   §1.1 (p. 8) presents **MIPI DSI, 2 data lanes + 1 clock lane** as the
   high-speed interface (D-PHY v1.0, DSI v1.02, max 250 Mbps @ 1 lane /
   125 Mbps @ 2 lane), but the features table (p. 9) also lists
   **"MIPI DBI Type-B (MPU 8-bit) and Type-C (3/4-wire mode), **Quad-SPI**"**, and
   the document devotes **§4.7 Dual SPI Interface (p. 55)**, **§4.8 Quad SPI
   Interface (p. 59)** and **§4.9 Pixel Format for SPI/MPU Interface (p. 60)** to
   it, with AC characteristics in **Table 15 (p. 27)** and pad assignments in
   **Tables 28–29 (pp. 50–51)**. That is why LilyGO can drive it over QSPI.
   Also documented: **OTP 8K × 8 bit, 3× re-writable, external programming
   voltage only** (p. 9) — relevant because initialisation settings may be
   partly or wholly preloaded from OTP (§1.1, p. 8).

> **Still not verified.** No register value, timing number or electrical limit has
> been transcribed beyond the identity, resolution, interface and OTP facts cited
> above. The command set (§5 of the datasheet, pp. 134–162) remains unmined.

### The archived copy is a byte-identical duplicate

| | Retained artifact | Archived copy |
|---|---|---|
| Path | `artifacts/sh8501b0-datasheet-lilygo-mirror.pdf` | `archive/devices/lilygo/t-display-s3-shared/artifacts/research-scratch/dl/SH8501B0_DataSheet.pdf` |
| **SHA-256** | `663d767850d7db71252c62f9de709cbaf278a88d25048aa168f6cb5586425b41` | **identical** |
| **Bytes** | 4,412,013 | **identical** |
| Pages | 168 | 168 |

Verified 2026-09-20 by `sha256sum` and a full-file `cmp` — `executed-success`.
PDF 1.5, A4 (595.32 × 841.92 pt), Creator and Producer **Microsoft® Word 2016**,
`CreationDate` 2020-08-28 03:30:39, `ModDate` 2020-08-28 03:49:22 — note both
predate the document's own stated **September 2020** cover date by a few days.
No `Title`/`Author` metadata is set.

The archived file is the acquiring pass's raw download; the retained file is the
copy it promoted and renamed. **Left in place** — the canonical copy already sits
at this component path, and removing a file from that scratch tree would
invalidate the locale-pinned tree digest (`f78adc6b7c0b…`, 118 files) that
certifies its relocation. See
[`README.ARCHIVE.md`](../../../archive/devices/lilygo/t-display-s3-shared/artifacts/research-scratch/README.ARCHIVE.md).

**Licence unchanged:** the cover carries a diagonal **CONFIDENTIAL / ALL RIGHTS
RESERVED / EDO ONLY** watermark and a per-page *"Confidential"* footer.
Redistribution status **`prohibited` on the face of the document**; disposition
`repository`, **unstaged**.

---

## 6. Sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | SH8501B — 240RGBx240 / 16.7M color AMOLED Display Driver IC, Datasheet, User Command Set | **SHENGHE MICRO ELECTRONICS** | primary (via vendor mirror) | datasheet | [`artifacts/sh8501b0-datasheet-lilygo-mirror.pdf`](artifacts/sh8501b0-datasheet-lilygo-mirror.pdf) | 2026-09-07 (acquired), **2026-09-20** (identity audited) | **Preliminary Version 0.0, September 2020** | §1, §5 |
| S-2 | Same bytes, LilyGO repository mirror | Shenghe, mirrored by **LilyGO** | credible mirror | repository file | `Xinyuan-LilyGO/LilyGo-AMOLED-Series` → `datasheet/SH8501B0 DataSheet.pdf` @ `6d1dc008b94578cc34ba4a0f3b223dd808ca963f` | 2026-09-07 | same | §1 — the sole located reacquisition path |
| S-3 | Archived working copy of S-1 | this repository's archive tier | — | artifact | `archive/devices/lilygo/t-display-s3-shared/artifacts/research-scratch/dl/SH8501B0_DataSheet.pdf` | **2026-09-20** | same | §5 — duplicate proven by hash and `cmp` |
