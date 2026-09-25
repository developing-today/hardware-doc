# Sitronix ST7567S

- **Category:** monochrome dot-matrix LCD controller + driver, 132 × 65 (132 SEG + 64 COM + 2 icon
  COM pads), COG die
- **Research status:** mined end-to-end from the datasheet now held at `artifacts/`. **No board in
  this repository is known to use it** — see §10. This is a component capability record, not a
  fitment record.
- **Retrieved:** 2026-09-11 (acquired) · **mined and filed:** 2026-09-20
- **Document:** ST7567S Datasheet **Version 1.4, 2016/07/13**, 68 pages
- **Ordering part number on the die:** **`ST7567S-G4`**

The **S** of the ST7567 family: a single-chip STN/FSTN monochrome controller-driver with on-chip
DDRAM, oscillator, charge-pump booster with **on-die flying capacitors**, regulator and follower.
Five host interfaces, no external clock, no external bias resistor network.

> ### ⚠ Read this before using this record or the ST7567A record interchangeably
>
> **ST7567A and ST7567S are different parts with different documents and different capabilities.**
> They share a resolution, a pinout family, an instruction base and a great deal of copied text —
> and they differ in ways that will break a driver. **§2 is the whole point of this record.**
>
> The [ST7567A](../st7567a/README.md) record previously stated that the `S` document existed but was
> **not** filed. That is no longer true; this is it, and §2 supersedes the caveat there.

> ⚠ **This document arrived under a URL that named a different part.** Fetched from Crystalfontz as
> `515.pdf` while probing `crystalfontz.com/controllers/UltraChip/UC8179/<id>/`. The
> `<Vendor>/<Part>` path segments on that host are decorative; only the numeric id selects a
> document. §11, and
> [`ai-crawler-site-access-table.md` § crystalfontz.com](../../../ai-crawler-site-access-table.md#crystalfontzcom--serves-controller-datasheets-and-the-url-lies).

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Read out of `artifacts/st7567s-datasheet-v1.4-2016-07-13-crystalfontz-mirror.pdf`, cited by page (the printed footer page equals the PDF page: `Ver 1.4  <n>/68  2016/07/13`) |
| **[DOC-A]** | Read out of the **ST7567A** datasheet held at [`../st7567a/artifacts/`](../st7567a/artifacts/), for comparison only |
| **[DOC-IMG]** | Read off a **rendered page image** rather than the text layer |
| **[INF]** | Inference. Not stated by Sitronix |
| **[NEG]** | Negative result — checked for and **not** found |

### Text-layer validation

**[DOC-IMG]** Page 35 was rendered at 150 dpi and compared character by character against
`pdftotext -layout`. Headings, the `X[7:0]` column-address truth table, the Read-Status flag table
and the footer (`Ver 1.4  35/68  2016/07/13`) match exactly — **including the datasheet's own typo**
(§8.1) and the Read-Status polarity oddity (§8.2). `pdfinfo` reports `Pages: 68` against the printed
`68/68`. The text layer is trustworthy.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Sitronix Technology Corp.** (矽創電子) | **[DOC]** cover, page-header logo |
| Part | `ST7567S`; die ordering number **`ST7567S-G4`** | **[DOC]** p.1, p.6 |
| Document | **Datasheet Version 1.4, 2016/07/13** | **[DOC]** p.1, every footer, p.68 |
| Resolution | **132 × 65** = 132 SEG × (64 COM + 1 icon common) | **[DOC]** p.5, p.12, p.24 |
| DDRAM | **132 × 65 = 8 580 bits** — 8 pages × 8 bits + page 8 × 1 bit | **[DOC]** p.5, p.24 |
| Host interfaces | 8080 parallel · 6800 parallel · 4-line SPI · 3-line SPI · **I²C** | **[DOC]** p.5, p.14, p.17 |
| I²C addresses | **`0x3C`–`0x3F`** (`0111100`…`0111111`), low 2 bits strapped | **[DOC]** p.22 |
| Package | **COG**. Chip **3800 × 640 µm ± 40**, thickness **300 µm**, bump height **12 µm** | **[DOC]** p.6 |
| Operating temperature | **−30 … +85 °C**; storage **−55 … +125 °C** | **[DOC]** p.5, p.49 |
| Duty ratios | **1/65, 1/55, 1/49, 1/33** — **four**, pad-selected | **[DOC]** p.5, p.14 |
| Booster | Built-in charge pump **×4 / ×5**, *capacitors on-die* | **[DOC]** p.5, p.40 |
| PDF metadata | `Title: ST7567S_V1.4`, `Author: devin_chiu`, **PDFCreator 1.2.0 / GPL Ghostscript 9.0**, created 2016-07-14 | **[DOC]** `pdfinfo` |

The `Author` field is `devin_chiu` — **the same author as the ST7567A document** **[DOC-A]**. One
engineer, one house template, two parts; which is exactly why §2 and §8 matter.

---

## 2. ⚠ ST7567S versus ST7567A — the differences that break drivers

Both documents are in this repository; this table is the reason to have both. **Every row is a
measured difference between the two documents**, not a guess.

| | **ST7567S** (V1.4, 2016) | **ST7567A** (V1.3, 2020) | Consequence |
|---|---|---|---|
| **Duty ratios** | **4**: 1/65, 1/55, 1/49, 1/33 **[DOC]** p.5, p.14 | **6**: adds **1/17 and 1/9** **[DOC-A]** p.6, p.48 | The low-duty modes are `A`-only. Code that selects them is not portable |
| **Instruction count** | **23** **[DOC]** p.33 | **23 base + an extension command set** **[DOC-A]** p.37–38 | See the four rows below |
| **Extension command set** (`0xFF`/`0xFE`) | ❌ **absent** **[NEG]** | ✅ present **[DOC-A]** p.38 | `0xFF` on an `S` is **not** a defined instruction. Sitronix: *"Do not use instructions not listed"* |
| **Display Setting Mode** (`0x72`/`0x70`, `DT`/`BA`/`FR`) | ❌ **absent** **[NEG]** | ✅ present **[DOC-A]** p.48 | On `S`, **duty and bias come only from the `SEL[2:1]` and `BS` straps/bit** — no software override |
| **Frame-rate register `FR[2:0]`** | ❌ **absent** **[NEG]** | ✅ 7 steps, **70 – 300 Hz** **[DOC-A]** p.48 | **`S` frame rate is not selectable**: 70 / **75** / 80 Hz min/typ/max at 1/65 duty is a *characteristic*, not a setting **[DOC]** p.50. (Both parts' DC tables quote the same 70/75/80 — on the `A` that is the reset default of a register you can change) |
| **N-line inversion** (`0x85`/`0x84`) | ❌ **absent** **[NEG]** | ✅ N = 1…32 **[DOC-A]** p.46 | `S` does frame inversion only. (You also inherit none of `A`'s DC-bias hazard) |
| **High Power Mode** | ❌ **absent**. **`TSEL` is a *test pin* that "must be connected to L by VSSL"** **[DOC]** p.15 | ✅ `TSEL` pad selects it, and/or `0xFF`→`0x6B`→`0xFE` **[DOC-A]** p.15, p.47 | **The single most dangerous confusion.** Tying `TSEL` high on an `S` is outside spec; on an `A` it selects a mode |
| **`VG` window** | **1.6 V ≤ VG < VDD2 − 0.2 V**, fixed **[DOC]** p.15, p.36 | same, **extended to < 3.8 V in High Power Mode** **[DOC-A]** p.15 | `S` cannot reach the high-`VG` operating points `A` can |
| **`VDD2` / `VDD3` minimum** | **2.4 V** **[DOC]** p.50 | **2.0 V** **[DOC-A]** p.58 | An `A`-based 2.0 V analogue design **does not port to `S`** |
| **`VDD1` minimum** | 1.7 V **[DOC]** p.50 | 1.7 V **[DOC-A]** p.58 | same |
| **Operating temperature** | **−30 … +85 °C** **[DOC]** p.5 | **−30 … +85 °C** **[DOC-A]** p.6 | same |
| **Storage temperature** | **−55 … +125 °C** **[DOC]** p.49 | **−55 … +125 °C** **[DOC-A]** p.57 | same |
| **Display current** | **150 µA** typ / 300 max — pattern **"SNOW"**, `VDD` = **3.0 V** **[DOC]** p.50 | **80 µA** typ / 130 max — pattern **Black**, `VDD` = **3.3 V**, **−20…+70 °C** **[DOC-A]** p.58 | ⚠ **different pattern, supply and temperature window — not comparable.** §3.3 |
| **Power-down current** | — typ / **4.0 µA max** **[DOC]** p.50 | **1.0 µA** typ / **3.0 µA max** **[DOC-A]** p.58 | `S` quotes no typical at all, and a 1 µA higher ceiling. `S` v1.2a *raised* this spec (§8.5) |
| **`VLCD` (`V0−XV0`)** | 4.0 – **13** V **[DOC]** p.50 | 4.0 – **13.65** V **[DOC-A]** p.58 | minor |
| **Application-circuit reference** | ✅ **§15: ITO layout, LCM design, and five application circuits (6800/8080/4-SPI/3-SPI/I²C)**, p.60–67 | ❌ not present | **`S` is the better document if you are designing a module** |
| **Design inequalities for `Vop`** | ❌ **absent** **[NEG]** | ✅ p.59 booster/headroom formulas | **`A` is the better document if you are sizing the power circuit** |
| **Reset/status contradiction** | present (§8.2, §8.3) | present **[DOC-A]** | shared inheritance |
| **Column-address typo "120"** | **present** at p.35 **[DOC-IMG]** | **present** at p.40 **[DOC-A]** | §8.1 — the same defect in both, from the same edit |

### 2.1 What is *identical*

Do not over-rotate: the shared surface is large. Both parts have the same 132 × 65 DDRAM and paging,
the same `SI2`/`PSB`/`C86` interface straps, the same `D[1:3]`-tied-as-SDA serial arrangement, the
same `D[7:4]` 4-bit board ID, the same four I²C addresses `0x3C`–`0x3F` strapped on `ERD`/`RWR`, the
same 23-instruction base set with the same opcodes, the same `V0 = RR × [(99 + EV)/162] × 2.1`
contrast formula, the same booster/regulator/follower staging, the same power-save compound
instruction, the same power-off discharge requirement, and the same reference "refresh" routine.
**[DOC]** p.14–48 vs **[DOC-A]**.

**[INF] Practical rule:** *base-set* code written for one will run on the other. **Anything that
touches `0xFF`, `0x72`, `0x85`, `0x6B`, the `TSEL` pad, 1/17 or 1/9 duty, or a frame-rate setting is
`A`-only and will do something undefined on an `S`.**

---

## 3. Electrical

### 3.1 Supplies

**[DOC]** p.14 (pin roles), p.49 (limiting values), p.50 (DC).

| Rail | Role | Limiting value | Operating | Pads |
|---|---|---|---|---:|
| `VDD1` / `VSS1` | **Digital.** Logic and MPU interface | −0.3 … **4.0 V** | **1.7 – 3.6 V** (feature page says 1.8–3.3 typ) | 3 / 2 |
| `VDD2` / `VSS2` | **Analogue.** Booster input | −0.3 … **4.0 V** | **2.4 – 3.6 V** | 4 / 3 |
| `VDD3` / `VSS3` | **Reference-voltage circuit** | −0.3 … **4.0 V** | **2.4 – 3.6 V** | 2 / 1 |
| `VIN` | any input | −0.3 … `VDD1` + 0.3, and **≤ 3.6 V absolutely** | | |
| `V0 − XV0` | LCD drive | −0.3 … **14 V** | 4.0 – **13 V** | |
| `VG` | segment drive | −0.3 … **3.6 V** | **1.6 V ≤ VG < VDD2 − 0.2 V** | |
| `VM` | common mid-level | — | **0.8 V ≤ VM < VG** | |

`VDD1` may equal `VDD2` (short them externally); `VSS1` and `VSS2` are **always** shorted
externally. **[DOC]** p.14.

> ⚠ **`VDD2`/`VDD3` bottom out at 2.4 V, not 2.0 V.** This is the sharpest electrical difference
> from the `A` (§2) and the one most likely to bite a design migrated between them: a 2.0 V analogue
> rail is legal on an `A` and **out of spec on an `S`.**

Operating invariant, stated as a limiting-value note: **`V0 ≥ VDD2 > VG > VM > VSS ≥ XV0`**
**[DOC]** p.49 note 3, and in the pin table as `V0 ≥ VG > VM > VSS ≥ XV0` **[DOC]** p.14. The p.49
form is stricter — satisfy that one.

**Kelvin pads.** `V0O`/`V0I`, `XV0O`/`XV0I` and `VGO`/`VGI` are separate output and input pads for
one node; the ITO layout must short them. **[DOC]** p.14. Not two rails.

⚠ **`VMO` must be left floating.** The recommended-ITO-resistance table (p.16) lists
`T[11:1], VMO → Floating`, alongside the test pads. `VM` is generated and used internally; the two
`VMO` pads are not a rail you route. **[DOC]** p.16.

### 3.2 The booster's capacitors are on the die

**[DOC]** p.40: *"ST7567S booster is built-in booster capacitors. Booster level can be changed with
instruction only without changing hardware connection."*

So ×4 ↔ ×5 is a **software** change (`0xF8` + `0x00`/`0x01`), and no flying capacitors are needed —
the same headline advantage the `A` has over older ST7565-class parts.

External components remain **optional and conditional** **[DOC]** p.31:

| Part | Value | Required when |
|---|---|---|
| `C1` (V0 reservoir) | 0.1 – 1.0 µF, non-polar, **25 V**, default **N.C.** | panel **> 2″**, heavy load, **or the icon row is used** |
| `C2` (VG reservoir) | 0.1 – 1.0 µF, non-polar, **6 V**, default **N.C.** | same conditions |
| `R1` (bleeder) | 500 kΩ – 1 MΩ, default **N.C.** | insurance against an abnormal power-down path (§7.3) |

Sitronix adds: *"Higher capacitor values are recommended for ripple reduction"* and *"the capacitor
values should be verified according to the display performance on LCD panel."* **[DOC]** p.31.

> ⚠ Note the `A` makes `C2` **mandatory** whenever High Power Mode is on **[DOC-A]** p.35. Since the
> `S` has no High Power Mode (§2), that clause simply does not exist here — the condition list above
> is complete.

### 3.3 DC and current

**[DOC]** p.50. `VSS = 0 V`, −30…+85 °C.

| Item | Symbol | Value |
|---|---|---|
| Input high / low | `VIHC` / `VILC` | 0.7 × `VDD1` … `VDD1` / `VSS1` … 0.3 × `VDD1` |
| Output high / low | `VOHC` / `VOLC` | ≥ 0.8 × `VDD1` / ≤ 0.2 × `VDD1` at **1 mA, `VDD1` = 1.8 V**, on `D[7:0]` |
| Input / output leakage | `ILI` / `ILO` | ±1.0 µA / **±3.0 µA** |
| **COM driver ON resistance** | `RON` | **0.6 kΩ** typ, 0.8 kΩ max (Vop 8.5 V, ΔV 0.85 V) |
| **SEG driver ON resistance** | `RON` | **1.3 kΩ** typ, 1.5 kΩ max (VG 1.9 V, ΔV 0.19 V) |
| **Frame frequency** | `FR` | **70 / 75 / 80 Hz** (min/typ/max) at 1/65 duty, Vop 8.5 V, 25 °C |
| `VLCD` | `V0 − XV0` | **4.0 – 13 V** at 25 °C |

Current consumption, whole bare die, internal power system, `VDD1=VDD2=VDD3=3.0 V`, ×5 booster,
Vop 8.5 V, 1/9 bias, 25 °C:

| Condition | Typ | Max |
|---|---:|---:|
| Display pattern **"SNOW"** (static) | **150 µA** | 300 µA |
| **Display OFF** | 95 µA | 190 µA |
| **Power down** | — | **4.0 µA** |

> ⚠ **"SNOW" is not defined anywhere in the document.** **[NEG]** It is presumably a high-activity
> checkerboard/noise pattern (worst case). The `A` quotes its figure for a **Black** static pattern
> at **3.3 V** over **−20…+70 °C** **[DOC-A]** p.58, while this table uses **3.0 V** and states no
> temperature window. **Three variables differ, so the two parts' current numbers are not
> comparable** and should not be put in one table without this caveat. Recorded so nobody tries.

⚠ The frame-frequency row is the *only* statement of frame rate in the document — **there is no
frame-rate instruction on this part** (§2). 75 Hz typ is what you get.

### 3.4 I²C timing

**[DOC]** p.58. Given twice, once for `VDD1` = 2.8 V and once for 3.3 V, with **identical values in
both tables** — a copy without edit, recorded as a document quirk (§8.4).

| Item | Symbol | Min | Max |
|---|---|---:|---:|
| SCL frequency | `fSCL` | — | **400 kHz** |
| SCL low / high | `tLOW` / `tHIGH` | **160 ns** / **60 ns** | — |
| Data setup / hold | `tSU;Data` / `tHD;Data` | **80 ns** / **40 ns** | — |
| Repeated-START setup | `tSU;STA` | **90 ns** | — |
| START hold | `tHD;STA` | **220 ns** | — |
| STOP setup | `tSU;STO` | **110 ns** | — |
| Bus free | `tBUF` | **150 ns** | — |

Input rise/fall ≤ **15 ns**; thresholds are 20 % / 80 % of `VDD1`. **[DOC]** p.58.

These are far tighter than I²C Fast-mode requires — the part is not the limiting element on a
400 kHz bus. **[INF]**

### 3.5 Hardware reset timing

**[DOC]** p.59. Supply-dependent, and **microseconds**:

| `VDD1` | `tRW` (RSTB low, min) | `tR` (reset time, max) |
|---|---|---|
| 3.3 V | **1.0 µs** | 1.0 µs |
| 2.8 V | **2.0 µs** | 2.0 µs |
| 1.8 V | **3.0 µs** | 3.0 µs |

Identical to the `A`. **[DOC-A]** p.68.

`RSTB` also wants **2–3 kΩ of series ITO resistance** *"to prevent the ESD pulse resetting the
internal register"*, and the required value *"is different from modules"* — a per-module tuning
parameter. **[DOC]** p.16.

---

## 4. Interface selection — strapped on the glass, not configured in software

There is **no runtime interface-selection command.** `SI2`, `PSB` and `C86` are input pads tied to
`VDDH`/`VDD1` or `VSSL`/`VSS1` in the module's ITO layout. **[DOC]** p.14, p.17, p.18.

| `SI2` | `PSB` | `C86` | Interface | Pins used |
|---|---|---|---|---|
| L | L | L | **3-line SPI** (9-bit) | `CSB`, `D0`=SCL, `D[3:1]`=SDA |
| L | L | H | **4-line SPI** | `CSB`, `A0`, `D0`=SCL, `D[3:1]`=SDA |
| L | H | L | **8080 parallel** | `CSB`, `A0`, `ERD`=/RD, `RWR`=/WR, `D[7:0]` |
| L | H | H | **6800 parallel** | `CSB`, `A0`, `ERD`=E, `RWR`=R/W, `D[7:0]` |
| **H** | L | X | **I²C** | `D0`=SCL, `D[3:1]`=SDA, **`ERD`=SA0, `RWR`=SA1** |

Three consequences, all identical to the `A` and all still worth stating:

1. **`D[1]`, `D[2]` and `D[3]` must be tied together externally to form SDA.** `D1` is serial data
   *in*, `D[3:2]` are serial data *out*. *"D[1:3] must be connected together as SDA."* **[DOC]** p.13.
2. **`D[7:4]` become a 4-bit hardware ID** in every serial mode, strapped to `VDDH`/`VSSL`, readable
   as `ID[3:0]` through the SPI status read (`0xFC`). **[DOC]** p.13, p.40. A board identity nibble,
   nothing to do with the controller.
3. **In I²C mode the parallel handshake pins become the address bits**: `ERD` → `SA0`,
   `RWR` → `SA1` **[DOC]** p.13, p.17. The four reserved 7-bit addresses are
   **`0111100`/`0111101`/`0111110`/`0111111` = `0x3C`–`0x3F`** **[DOC]** p.22.

### 4.1 Unused pins are not "don't care"

Every interface table repeats: *"The un-used pins are marked as `---` and should be fixed to `H` by
VDD1 or VDDH."* **[DOC]** p.17, p.18. And p.13, Note 1: **"After VDD1 is turned ON, any MPU interface
pins cannot be left floating."**

For SPI specifically **[DOC]** p.18: *"the SCL signal quality is very important and external noise
maybe causes unexpected data/instruction latch."*

**[INF]** If your MCU tri-states its GPIOs in deep sleep while the panel stays powered, expect
intermittent garbage that looks like a driver bug. Pull the control lines, or drop `VDD1` too.

### 4.2 Recommended ITO resistances

Rarely published and directly useful if you are laying out glass. **[DOC]** p.16.

| Net | Max ITO resistance |
|---|---|
| `VDD1`, `VDD2`, `VDD3` | **< 100 Ω** |
| `VSS1`, `VSS2`, `VSS3` | **< 70 Ω** |
| `V0`, `XV0`, `VG` (both `*O` and `*I`) | < 200 Ω |
| `A0`, `RWR`, `ERD`, `CSB`, `D[7:0]` | < 700 Ω |
| `PSB`, `C86`, `SEL[2:1]`, `SI2`, `TSEL` | **< 5 kΩ** (static straps) |
| `D0`=SCL / `D[3:1]`=SDA in **I²C** | **< 100 Ω** |
| `D0`=SCL / `D[3:1]`=SDA in **SPI** | < 300 Ω |
| `RSTB` | **2 – 3 kΩ** (deliberately high — ESD, §3.5) |
| `T[11:1]`, **`VMO`** | **Floating** |

Note the I²C data/clock budget (**100 Ω**) is three times tighter than SPI's. **[INF]** I²C's
open-drain rise through the ITO is the constraint.

### 4.3 I²C protocol shape

Standard Philips-style display protocol: `START` → slave address → *control byte* {`Co`, `A0`} →
byte → … **[DOC]** p.22.

- `Co = 1` — another control byte follows the data byte (interleaved command stream).
- `Co = 0` — **this is the last control byte**; only data bytes follow until `STOP` or repeated `START`.
- `A0 = 0` — following bytes are **commands**; `A0 = 1` — they are **DDRAM data**.

So the familiar `0x00`-prefixed command burst / `0x40`-prefixed data burst of SSD1306-style drivers
applies: `0x00` = {Co=0, A0=0}, `0x40` = {Co=0, A0=1}. **[INF]** — the datasheet defines the bit
positions; the byte values follow arithmetically.

**I²C is write-only.** §6-4-5 describes *"command/data write to addressed slaves"* and no read
protocol appears anywhere. **[DOC]** p.22. See §8.3.

---

## 5. Memory model and addressing

- DDRAM is **132 columns × 65 rows** — pages 0–7 of 8 bits plus **page 8 of 1 bit** (the icon row,
  `D0` only). `D0` is at the **top** of each page. **[DOC]** p.24, p.34.
- `X = 0…131` (column), `Y = 0…8` (page). **"Addresses outside these ranges are not allowed."**
  **[DOC]** p.25.
- **Column address is a two-command pair:** high nibble `0x10 | X[7:4]`, then `0x00 | X[3:0]`
  **[DOC]** p.33, p.35.
- ⚠ **`X[7:0]` must be ≤ `0x83`.** *"If X[7:0] setting is great than 83h, out of DDRAM range will be
  ignored."* `0x83` = 131 = the last of 132 columns. **[DOC]** p.35.
- **Page address must be set before accessing DDRAM** and is settable *only* by
  `Set Page Address` = `0xB0 | Y[3:0]`. **[DOC]** p.25.
- **The column pointer auto-increments on every access and wraps to the start column** — it does
  **not** advance the page. **[DOC]** p.25, p.35. A full-frame blit is therefore **nine** explicit
  page-set + column-set sequences, not one stream.
- **`Set Start Line` = `0x40 | S[5:0]`, 0–63**, shifts which DDRAM line appears at COM0 — free
  vertical scrolling without touching RAM. **[DOC]** p.34. The icon row is not scrollable. **[INF]**
- ⚠ **`MX` (SEG direction) requires a DDRAM rewrite; `MY` (COM direction) does not.**
  *"It is necessary to rewrite the display data into DDRAM after changing MX setting."* **[DOC]**
  p.25. Set orientation once, at init.
- **After power-on, DDRAM contents are undefined.** *"It's better to initialize whole DDRAM (ex:
  fill all 00h or write the display pattern) before turning the Display ON."* **[DOC]** p.32.

### 5.1 Read-modify-write

`0xE0` enters, `0xEE` (`END`) leaves. **[DOC]** p.37. Inside the mode, **reads do not advance the
column pointer and writes do** — built for cursor blinking and partial redraws. `END` restores the
column address to its value when `0xE0` was issued. Other instructions remain usable inside the mode.

### 5.2 The dummy read, and how wide it is

*"After setting the target address, a dummy read cycle is required before the following
read-operation."* **[DOC]** p.23. The dummy's **width differs by interface** — a detail that is easy
to miss and will desynchronise a driver:

| Interface | Dummy bits |
|---|---:|
| 8080 parallel | **8** |
| 6800 parallel | **8** |
| 3-line SPI | **1** |
| 4-line SPI | **1** |
| **I²C** | 8 — *but see §8.3; I²C has no documented read path at all* |

**[DOC]** p.23.

---

## 6. LCD output stage

**[DOC]** p.12.

| Output | Count | Normal display, data H | Notes |
|---|---:|---|---|
| `SEG0` … `SEG131` | **132** | `VG` on + frame, `VSS` on − frame (inverted for `L`) | `VSS` when display OFF or in power save |
| `COM0` … `COM63` | **64** | scan H → `XV0` (+) / `V0` (−); scan L → `VM` both frames | `VSS` when display OFF or in power save |
| **`COMS`** | **2 pads** | icon common | ⚠ *"The output signals of these two pins are the same. **When icon feature is not used, these pins should be left open.**"* |

Bias taps at 1/65 duty with 1/9 bias **[DOC]** p.36: `V0` = `V0`, **`VG` = 2/9 × V0**,
**`VM` = 1/9 × V0**, `VSS` = `VSS`.

The `SEL[2:1]` pads pick duty, and `BS` picks one of two bias ratios within it **[DOC]** p.14, p.36:

| `SEL2` | `SEL1` | Duty | `BS=0` | `BS=1` |
|---|---|---|---|---|
| L | L | **1/65** | 1/9 | 1/7 |
| L | H | 1/49 | 1/8 | 1/6 |
| H | L | 1/33 | 1/6 | 1/5 |
| H | H | 1/55 | 1/8 | 1/6 |

**That is the whole duty/bias mechanism on this part** — there is no `DT[3:0]`/`BA[2:0]` override
(§2). Choose the straps at module design time and you are committed.

---

## 7. Initialisation, reset and power sequencing

### 7.1 Power-on

**[DOC]** p.42–43.

| Requirement | Value |
|---|---|
| `VDDI` (VDD1) vs `VDDA` (VDD2/VDD3) order | **Any order; applying them in either order will not damage the IC** (`tON-V2 ≥ 0`) |
| Hardware reset after power stable | **Required.** *"If RSTB is Low, High or unstable during power ON, a successful hardware reset by RSTB is required after VDDI is stable"* |
| Recommended reset delay | **1 ms ≤ tON-RST ≤ 30 ms** after power is stable, *"to prevent abnormal display"* |
| "Power stable" definition | the **later** of VDDI/VDDA reaching **90 %** of rated voltage |
| Settling wait in the flow | **5 ms** — and *"depends on the characteristics of LCD panel and the external component of the power circuit. It is recommended to check with the real products"* |

Section 8 adds the blunt version: *"initialization by RSTB pin is **essential** before operating"*,
and *"while RSTB is 'L', no instruction except read status can be accepted."* **[DOC]** p.32.

### 7.2 ⚠ Hardware reset and software reset are not the same

**[DOC]** p.32. This table is the most important page in the document.

| Reset by **hardware only** (`RSTB` low) | Reset by **both** |
|---|---|
| Display OFF (`D=0`, SEG/COM at VSS) · Normal display (`INV=0`, `AP=0`) · `MX=0` · serial counter and shift register cleared · `BS=0` · `BL=0` · exit power save · **`VB=VR=VF=0` (power circuits OFF)** | exit read-modify-write · `S[5:0]=0` · `X[7:0]=0` · `Y[3:0]=0` · `MY=0` · **`RR[2:0]=0b100` (5.0)** · **`EV[5:0]=0b100000` (32)** |

Eight hardware-only items, seven shared — against the `A`'s fifteen and seven, the difference being
exactly the extension registers the `S` does not have (§2). **[DOC]** p.32 vs **[DOC-A]** p.36.

Two consequences:

1. **`0xE2` cannot initialise the analogue power block.** Stated explicitly: the software reset
   *"cannot initialize the built-in power circuit which is initialized by the RSTB pin."* **[DOC]**
   p.37. A design that omits `RSTB` and relies on `0xE2` comes up with `VB`/`VR`/`VF` indeterminate.
2. ⚠ **`0xE2` silently stamps on your contrast.** `RR` and `EV` are in the "both" column. Issue
   `0xE2` as a mid-session "harmless resync" — as Sitronix's own refresh routine does (§7.4) — and
   contrast reverts to `RR=5.0, EV=32`. That is why the vendor routine rewrites `0x24`/`0x81`/`0x20`
   immediately afterwards.

> ⚠ **§9-2-14 understates the software reset.** Its prose says `0xE2` *"resets Start Line (S[5:0]),
> Column Address (X[7:0]), Page Address (Y[3:0]) and COM Direction (MY)"* — **four** items **[DOC]**
> p.37 — while the §8 table lists **seven**, adding read-modify-write exit, `RR[2:0]` and `EV[5:0]`.
> **The table is the complete statement; the prose is an incomplete summary.** The identical
> discrepancy exists in the `A` **[DOC-A]** p.42, so it is inherited, not specific. **Conflict
> recorded; the table is preferred because it is the more specific and more recently revised
> statement, but this is not proven.**

### 7.3 Power-save and power-off

**Power Save is a compound instruction**, not an opcode: `Display OFF (0xAE)` **then**
`All Pixel ON (0xA5)`. Exit is the mirror: `0xA4` then `0xAF`. **[DOC]** p.40.

Entering it (1) stops the oscillator, (2) stops the power circuits, (3) parks COM/SEG at `VSS`.
**Display data and all register settings are preserved** except the `D` and `AP` flags. **[DOC]** p.40.

Exit is slow and staged **[DOC]** p.46 — booster, regulator and follower each take **up to 100 ms**,
and the IC forces outputs to `VSS` for a **typical 200 ms** during the transition. Measured on a
**1.4″ panel with no external capacitors, VDD = 2.7 V, Vop = 9 V**. **Budget ~300 ms before the
image is trustworthy after wake.**

**Power-off has a required sequence and skipping it can damage the panel** **[DOC]** p.47–48:

1. Enter power save (`0xAE`, `0xA5`) **or** pulse `RSTB` low then high.
2. **Wait 250 ms** — `tPOFF`, internal discharge, 250 ms max.
3. Remove `VDD1`–`VDD3`. `tV2OFF` min is 0 ms — they may go together.
4. When dropping `VDDA`, respect **20 ms ≤ tPfall ≤ 0.2 s**.

⚠ *"It is **NOT** recommended to turn VDDI OFF before VDDA. Without VDDI, the internal status cannot
be guaranteed and internal discharge-process maybe stopped. The un-discharged power maybe flows into
COM/SEG output(s) and **the liquid crystal in panel maybe polarized**."* **[DOC]** p.48.

Polarisation is cumulative and permanent. This is the `R1` bleeder's reason to exist (§3.2):
insurance against an abnormal power-down path firmware cannot control.

The IC itself is not at risk — *"IC will NOT be damaged if either VDDI or VDDA is OFF while another
is ON"* **[DOC]** p.48. **The glass is.** Also noted: below **1 V on either rail the internal status
is not guaranteed**, and once the rails are gone the outputs are not guaranteed at all. **[DOC]** p.47.

### 7.4 The vendor's own "refresh" sequence

Sitronix recommends running this **regularly, at a specified interval** — not only at boot.
**[DOC]** p.44.

```c
WriteCommand(0xE2);  // Software Reset   -- or 0xE3 (NOP), if RR/EV must not be disturbed
WriteCommand(0xA2);  // Bias Select: BS=0 -> 1/9 bias at 1/65 duty
WriteCommand(0xA0);  // SEG Direction: MX=0, normal
WriteCommand(0xC0);  // COM Direction: MY=0, normal
WriteCommand(0x24);  // Regulation Ratio = 5.0
WriteCommand(0x81);  // Set EV, byte 1
WriteCommand(0x20);  // Set EV, byte 2 -> EV = 32
WriteCommand(0x2C);  // Power Control: Booster ON  (VB=1, VR=0, VF=0)
WriteCommand(0x2E);  // Power Control: + Regulator (VB=1, VR=1, VF=0)
WriteCommand(0x2F);  // Power Control: + Follower  (VB=1, VR=1, VF=1)
WriteDisplayData();
```

**Byte-for-byte the same routine as the `A`'s** **[DOC-A]** p.52 — which is itself evidence that the
two parts share a base command set. Four things to read out of it:

- **The offer of `0xE3` (NOP) instead of `0xE2` is deliberate.** NOP preserves `RR`/`EV`/start
  line/addresses; `0xE2` resets them, which is why they are rewritten two lines later (§7.2).
- **The power block is staged — `0x2C`, `0x2E`, `0x2F`** — while the instruction description says
  *"typically, these 3 flags are turned ON at the same time"* **[DOC]** p.38. The staged form is the
  *flow's* recommendation and the simultaneous form is the *register's*. Prefer staged; it costs two
  bytes.
- **`DISPON` (`0xAF`) is deliberately absent** — the refresh flow leaves display state alone.
- **Bias comes from `0xA2`/`0xA3` (`BS`)**, which on this part is the only mechanism (§6).

> **Why run a "refresh" at all?** Sitronix does not say. **[NEG]** **[INF]** The plausible reason is
> ESD- or noise-induced register corruption on a COG module with long ITO traces — which is also why
> `RSTB` gets a deliberate 2–3 kΩ series resistance (§3.5). Recorded as speculation.

---

## 8. Errata, document defects and things that will waste your time

### 8.1 ⚠ The "120" typo — present here **and** in the ST7567A

p.35's Set Column Address truth table reads:

```
1 0 0 0 0 0 0 1  ->  129
1 0 0 0 0 0 1 0  ->  120     <- binary 0x82 = 130, not 120
1 0 0 0 0 0 1 1  ->  131
```

**[DOC-IMG]** This is **not** a text-extraction artefact. Page 35 was rendered to PNG and read
visually: the printed table says **120**. The value is **130**, as the surrounding rows and the
binary weight both require.

**The same typo, in the same table, is in the ST7567A at p.40** **[DOC-A]** — already recorded in
[ST7567A §9.3](../st7567a/README.md). And both documents' revision histories attribute their most
recent change to the same edit:

| Document | Version | Date | Change |
|---|---|---|---|
| **ST7567S** | **1.4** | **2016/07/13** | *"Modify Column Address Instructions"* |
| ST7567A | 1.2 | **2016/07/13** | *"Modify Column Address instructions"* |

**[DOC]** p.68, **[DOC-A]** p.77. **[INF]** One edit, applied to both documents on the same day,
introducing or leaving the same error in both. The `A` was revised twice more (to 1.3 in 2020) and
**still carries it**. Treat any "corrected" copy you find elsewhere with suspicion.

### 8.2 ⚠ The Read Status `D` bit is documented with the opposite polarity to the command `D` bit

| Where | Says |
|---|---|
| Instruction table (1), p.33 | *"**D=1, display ON** · D=0, display OFF"* |
| §9-2-1 Display ON/OFF, p.34 | *"**D=1: Normal Display Mode.** D=0: Display OFF"* |
| **§9-2-5 Read Status, p.35** | *"**D=0: Display ON** · D=1: Display OFF"* |
| §9-2-22 SPI Read Status, p.40 | same `D` field |

**[DOC-IMG]** Confirmed on the rendered page — this is printed, not an extraction error. The
identical inversion is in the **ST7567A** **[DOC-A]**, whose v1.3 changelog is literally *"Modify
Read Status register"* — and that change altered the *don't-care* bits `D3:D0`, **not** this
polarity. **[DOC-A]** p.77.

**This is not necessarily a typo.** A status flag that reads `1` for "display is off" is a perfectly
normal design, and both documents agree with each other. But **the same letter `D` means opposite
things in the write path and the read path**, and nothing in either document acknowledges it.

**Conflict recorded, not resolved.** **Practical advice:** do not round-trip. Track display state in
the host and use the status read only for `RST` (reset-in-progress). The evidence that would settle
it is one bus capture on real glass: issue `0xAF`, read status, look at bit 5.

### 8.3 ⚠ "Reads are not available in serial mode" — except for the two instructions that are

p.35 (§9-2-5) says flatly: *"The read function is not available in serial interface mode."*
p.18 (§6-2, 4-line SPI) repeats: *"The read feature is not available in this mode."*

Yet p.40–41 define **`0xFC` = SPI Read Status** and **`0xFD` = SPI Read DDRAM**, both explicitly
*"by 3-Line and 4-Line SPI."* **[DOC]** p.40, p.41.

**Resolution [INF]:** the "not available" sentences describe the *parallel-style* read path
(`R/W`=1 with `A0`), which genuinely does not exist on a serial bus; SPI reads exist but require the
dedicated `0xFC`/`0xFD` opcodes. Corroborated by the `A`'s revision history, whose v1.2b entry is
*"Modify Description about Read Function in SPI Interface"* **[DOC-A]** p.77 — i.e. Sitronix
noticed the problem and patched the *other* document's wording.

**For I²C there is no ambiguity: it is write-only.** §6-4-5 describes only *"command/data write to
addressed slaves"* and no read protocol is given anywhere in 68 pages. **[NEG]**

| Interface | Status read | DDRAM read |
|---|---|---|
| 8080 / 6800 parallel | ✅ direct (`R/W`=1) | ✅ direct |
| 4-line SPI / 3-line SPI | ✅ via `0xFC` | ✅ via `0xFD` |
| **I²C** | ❌ | ❌ |

### 8.4 Smaller defects

- **Figure 6 is captioned "Definition of STRAT and STOP Condition"** — *STRAT* for *START*.
  **[DOC]** p.20. The `A` has the identical typo **[DOC-A]** p.21.
- **The two I²C timing tables (2.8 V and 3.3 V) contain identical numbers.** **[DOC]** p.58. Either
  the timings genuinely do not vary with supply — in which case one table would do — or one was
  copied and not edited. Unresolved.
- **"SNOW" display pattern is never defined.** **[DOC]** p.50 · §3.3.
- **§9-2-14's software-reset list is incomplete** relative to the §8 table. §7.2.
- **`Set Start Line` ranges 0–63** while the panel is 65 rows including the icon common; the icon row
  is not scrollable. **[DOC]** p.34 **[INF]**.
- **No `Vop` design inequalities.** The `A` devotes p.59 to booster-sizing formulas
  (`VDD2 × BL × BE ≥ Vop` and friends); the `S` has **nothing equivalent** **[NEG]**. If you are
  sizing an `S` power circuit, read [ST7567A §4.5](../st7567a/README.md) and treat it as
  **inapplicable-until-confirmed** — the parts' `VDD2` minima already differ (§2).
- **No temperature-compensation command, register or thermistor input.** **[NEG]** — searched all
  68 pages. The regulator's fixed **−0.05 %/°C** thermal gradient **[DOC]** p.5 is all there is;
  compensation is the host's job, exactly as for the `A`.

### 8.5 Revision history

**[DOC]** p.68. Eleven revisions in under three years, then a two-year gap.

| Version | Date | Change |
|---|---|---|
| 1.0 | 2013-10-29 | Formal version |
| 1.0a | 2014-02-18 | Modify the error figure and DC characteristic |
| 1.0b | 2014-06-19 | Modify DC characteristic and limiting value |
| 1.0c | 2014-06-25 | **Modify VLCD formula** |
| 1.1 | 2014-07-08 | **Modify error command** and gold bump size |
| 1.1a | 2014-07-09 | Modify power circuit and typing error |
| 1.1b | 2014-07-24 | Modify description error |
| 1.2 | 2014-10-07 | Modify reference C code of Power ON flow and Refresh |
| 1.2a | 2014-10-17 | **Modify power-down current (up to 4 µA)** |
| 1.3 | 2014-10-29 | Modify part number · **bump height to 12 µm** · coordinate typo · add reset reserve capacitor and V0 reserve resistor · modify reset description in power-on flow |
| **1.4** | **2016-07-13** | **Modify column address instructions** (§8.1) |

Two entries deserve attention:

- **1.2a raised the power-down current specification to 4 µA.** A specification moving *upward* is a
  silicon or characterisation correction, not a documentation tidy. The `A` quotes **1.0 µA typ /
  3.0 µA max** **[DOC-A]** p.58; the `S` quotes **no typical and a 4.0 µA max**. **[INF]** If a
  standby budget was built on the `A`'s figures, re-check it against the `S`'s ceiling.
- **1.1 "Modify error command"** — an instruction was wrong in versions 1.0–1.0c. Which one is not
  said. **[NEG]** Any `S` datasheet copy older than 1.1 found in the wild should be discarded.

---

## 9. Instruction set summary

Complete set — **23 instructions, no extension set.** **[DOC]** p.33. Opcodes assembled from the bit
tables.

| Instruction | Opcode | Notes |
|---|---|---|
| Display ON / OFF | `0xAF` / `0xAE` | ⚠ status-read polarity, §8.2 |
| Set Start Line | `0x40 \| S[5:0]` | 0–63 |
| Set Page Address | `0xB0 \| Y[3:0]` | `Y=8` is the icon page, `D0` only |
| Set Column Address | `0x10 \| X[7:4]`, then `0x00 \| X[3:0]` | **X ≤ `0x83`**; higher is ignored |
| Read Status | `A0=0, R/W=1` → `{0, MX, D, RST, 0,0,0,0}` | **parallel only** |
| Write / Read Data | `A0=1` | dummy read required, §5.2 |
| SEG Direction (`MX`) | `0xA0` / `0xA1` | ⚠ rewrite DDRAM after changing |
| Inverse Display (`INV`) | `0xA6` / `0xA7` | latch only; DDRAM unchanged |
| All Pixel ON (`AP`) | `0xA4` / `0xA5` | latch only |
| Bias Select (`BS`) | `0xA2` / `0xA3` | **the only bias mechanism on this part**, §6 |
| Read-modify-Write / END | `0xE0` / `0xEE` | §5.1 |
| Software RESET | `0xE2` | **partial**, §7.2 |
| COM Direction (`MY`) | `0xC0` / `0xC8` | |
| Power Control | `0x28 \| VB<<2 \| VR<<1 \| VF` | `0x2C`, `0x2E`, `0x2F` staged |
| Regulation Ratio | `0x20 \| RR[2:0]` | 3.0 … 6.5 in 0.5 steps |
| Set EV | `0x81`, then `0x00 \| EV[5:0]` | **double byte — inseparable** |
| Set Booster | `0xF8`, then `0x00` (×4) / `0x01` (×5) | **double byte**; on-die capacitors, §3.2 |
| Power Save | `0xAE` then `0xA5` | compound; §7.3 |
| NOP | `0xE3` | |
| SPI Read Status | `0xFC`, then read `{0,MX,D,RST,ID3..ID0}` | SPI only, §8.3 |
| SPI Read DDRAM | `0xFD`, then read with `A0=1` | SPI only, §8.3 |

> ⚠ **There is no `0xFF`, `0x72`, `0x85`, `0x84`, `0x6B` or `0x64` on this part.** Those are
> ST7567**A** extension opcodes (§2). The `A`'s warning — *"Do not use instructions not listed in
> these tables"* — applies with more force here because the `S`'s table is shorter.

### 9.1 Contrast

**[DOC]** p.38–39:

```
V0 = RR × [ 1 − (63 − EV) / 162 ] × 2.1
   = RR × [ (99 + EV) / 162 ] × 2.1
```

| Register | Command | Range |
|---|---|---|
| `RR[2:0]` — Regulation Ratio | `0x20 \| RR` (`0x20`–`0x27`) | 3.0, 3.5, 4.0, 4.5, **5.0**, 5.5, 6.0, 6.5 |
| `EV[5:0]` — Electronic Volume | **double byte**: `0x81`, then `0x00 \| EV` | 0 – 63 |

Behaviour worth knowing before writing a contrast slider:

- **`0x81` and its value byte are inseparable.** `0x81` puts the part into EV-adjust mode and the
  *next* command byte is consumed as the value **[DOC]** p.39. Anything that can interleave a
  command between them — an I²C `Co=1` stream, an interrupt-driven command queue — corrupts either
  the setting or the following command.
- **Sitronix recommends centring `EV` near `0x1F`** so the end user has range in both directions
  **[DOC]** p.39.
- **The reachable maximum depends on `VDD2` and panel load**, so the computed `V0` is a ceiling, not
  a promise **[DOC]** p.39.
- **Reset defaults `RR=0b100` (5.0), `EV=0b100000` (32)** — and both are reset by the **software**
  reset too (§7.2).
- **The curve is linear in `EV`, and `RR` scales the window.** **[INF]** — arithmetic from the
  formula.

---

## 10. Used By

**None.** No device in this repository is documented as using an ST7567S, and **no fitment is
claimed here.** The datasheet was acquired incidentally while probing the Crystalfontz
controller-document host during Xteink research (§11); it documents the part, not any board.

If you fit one, add a row here and link back from the device record. ⚠ **Check the top marking
carefully** — `ST7567A` and `ST7567S` differ by one character and by everything in §2.

---

## 11. Provenance — the URL that lied

| Field | Value |
|---|---|
| Source host | `www.crystalfontz.com` |
| URL form probed | `https://www.crystalfontz.com/controllers/UltraChip/UC8179/<id>/` |
| Numeric id that returned this file | **515** |
| Part the URL claimed | **UltraChip UC8179** (an e-paper driver — unrelated) |
| Part the file actually is | **Sitronix ST7567S** |
| Retrieved | **2026-09-11** · re-verified and filed **2026-09-20** |
| SHA-256 | `75f3c2aaf8d5353d35c32632d7c56089a108399ec6f30e2c42bb18c237026d9a` |
| Byte size | **918 094** |
| Pages | 68 |
| Local artifact | `artifacts/st7567s-datasheet-v1.4-2016-07-13-crystalfontz-mirror.pdf` |
| Disposition | **repository** (primary, 897 KB; Sitronix publishes nothing equivalent — see the [vendor guide](../../../vendors/sitronix/README.md)) |
| Licence | **unknown.** No notice, no confidentiality marking, no redistribution statement in 68 pages — only the cover's *"Sitronix Technology Corp. reserves the right to change the contents in this document without prior notice."* |
| Redistribution status | **unknown** |

⚠ **This copy carries a Crystalfontz raster stamp on page 1** — a 1700 × 105 RGB image (8 936 B)
plus a 2 601 B soft mask, absent from every other page, and **not present in the text layer**
(`pdftotext` finds zero occurrences of "crystalfontz"). The identical object is on page 1 of every
document recovered from that host. **A Crystalfontz copy will therefore never hash-match the
vendor's original even when the content is identical**; compare text layers before concluding
anything about revisions. Full measurement in [FT5436 §10](../../focaltech/ft5436/README.md).

**The file is genuine; the URL is worthless as identification.** Every numbered document on that
host must be identified by content before filing. The measured id→part map is in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md#appended-2026-09-20--crystalfontz-numeric-id-probe-measured)
and [`archive/devices/xteink/shared-artifacts/research-scratch/datasheets/cfprobe/README.md`](../../../archive/devices/xteink/shared-artifacts/research-scratch/datasheets/cfprobe/README.md).

Filed under `components/sitronix/` rather than under the Xteink device that occasioned the fetch,
per the skill's rule: **a file is filed by what it describes.**

---

## 12. Open questions

| Question | Status |
|---|---|
| Is the Read-Status `D` bit really inverted relative to the command bit? | **Open.** §8.2. One bus capture settles it |
| Can ST7567S be read over I²C at all? | **Open, leaning no.** §8.3. No read protocol in 68 pages |
| Which instruction was wrong before v1.1 ("Modify error command")? | **[NEG]** Not stated. Discard any pre-1.1 copy |
| Why does Sitronix recommend a *periodic* refresh sequence? | **[NEG]** Never explained. ESD/noise register corruption is the **[INF]** guess |
| What is the "SNOW" test pattern? | **[NEG]** Undefined in the document |
| What booster efficiency should be assumed? | **[NEG]** The `S` gives no design inequalities at all; the `A`'s p.59 formulas use an unspecified `BE` |
| Does a revision later than **V1.4 (2016-07-13)** exist? | **Open.** None located. Ten years without an update is plausible for a mature COG part |
| Is there an errata document? | **[NEG]** None found; Sitronix publishes no public errata — see the [vendor guide](../../../vendors/sitronix/README.md) |
| How do `A` and `S` differ **in silicon**, beyond the documented feature delta? | **Open.** §2 is a *document* comparison. No part was measured |
| Any fitment in this repository? | **No** — §10 |

---

## 13. Related records

- **[Sitronix ST7567A](../st7567a/README.md)** — the sibling. **Read §2 before treating them as
  interchangeable.**
- **[Sitronix documentation-sourcing guide](../../../vendors/sitronix/README.md)** — why Sitronix
  publishes nothing, and the ranked list of places that do
- [Sitronix ST77916](../st77916/README.md) — the colour QSPI sibling; same house conventions,
  entirely different register set
- [Sitronix ST7789V2](../st7789v2/README.md) · [ST7789VW](../st7789vw/README.md) ·
  [ST7796S](../st7796s/README.md) · [ST7701S](../st7701s/README.md) — the colour TFT line
- [Display interfaces guide](../../../guides/hardware/display-interfaces.md) — how parallel / SPI /
  I²C command-bus displays compare
- [FocalTech FT5436](../../focaltech/ft5436/README.md) · [FT3267](../../focaltech/ft3267/README.md) ·
  [Chip Wealth Technology CH13620](../../chip-wealth-technology/ch13620/README.md) — the other parts
  recovered from the same Crystalfontz probe

---

## Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| S1 | **ST7567S Datasheet Version 1.4** | Sitronix Technology Corp. | **primary** (via credible mirror) | datasheet | `https://www.crystalfontz.com/controllers/UltraChip/UC8179/515/` — ⚠ **the URL names a different part**; §11 | 2026-09-11 | **2016-07-13** | Everything on this page unless marked otherwise | `artifacts/st7567s-datasheet-v1.4-2016-07-13-crystalfontz-mirror.pdf` |
| S2 | ST7567A Datasheet Version 1.3 | Sitronix Technology Corp. | primary (via credible mirror) | datasheet | `https://www.crystalfontz.com/controllers/UltraChip/UC8179/516/` | 2026-09-11 | 2020-08-04 | **[DOC-A]** rows throughout §2, §7.2, §8 | [`../st7567a/artifacts/st7567a-datasheet-v1.3-2020-08-04-crystalfontz-mirror.pdf`](../st7567a/artifacts/st7567a-datasheet-v1.3-2020-08-04-crystalfontz-mirror.pdf) |
| S3 | Crystalfontz numeric-id probe (`cfprobe`), ids 512–523 | this repository | — | measurement | — | 2026-09-11 / re-verified 2026-09-20 | — | The id→part map, the HTML-under-`.pdf` fall-through, and the page-1 raster stamp | `archive/devices/xteink/shared-artifacts/research-scratch/datasheets/cfprobe/README.md` · [`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md) |

**Local artifacts**

| File | Bytes | SHA-256 | Pages | Licence | Disposition |
|---|---:|---|---:|---|---|
| `artifacts/st7567s-datasheet-v1.4-2016-07-13-crystalfontz-mirror.pdf` | 918 094 | `75f3c2aaf8d5353d35c32632d7c56089a108399ec6f30e2c42bb18c237026d9a` | 68 | **unknown** (no notice anywhere in the document) | repository |

**Reacquire**

```bash
# Primary, verified working 2026-09-20 — note the URL names UC8179, not ST7567S
curl -sSL -o st7567s.pdf "https://www.crystalfontz.com/controllers/UltraChip/UC8179/515/"
head -c 5 st7567s.pdf | grep -q '%PDF' || echo "HTML fall-through — not a PDF"
sha256sum st7567s.pdf   # expect 75f3c2aa...
# Confirm it is the S and not the A:
pdftotext -layout -f 1 -l 1 st7567s.pdf - | head -5    # must read "ST7567S ... Version 1.4 ... 2016/07"
```

> Reacquisition status **`automatic`**. ⚠ The id→document mapping on this host is **not** guaranteed
> stable: it is an internal document id, not a content address, and **id 516 returns the `A`**.
> Re-verify by first-page text, never by URL. Sitronix itself publishes no datasheets — see the
> [vendor guide](../../../vendors/sitronix/README.md).
