# 1.25WT-2P — 1.25 mm horizontal SMT wire-to-board header (unattributed)

> The **battery socket** on the M5Stack DinMeter (K134 / K134-V11), designator `J2`.
> Record created **2026-09-20**, when the drawing was filed out of scratch.
> Filed under `components/generic/` because **the drawing names no manufacturer** — see §4.
> Document: 产品名称 **"(1.25) 卧式连接器"** ("(1.25) horizontal connector"), 间距 **1.25 mm**,
> scale 1:1, sheet 1 of 1, 初始日期 (initial date) **2011-06-16**, revision block **blank**
> **[DWG]**.

**Evidence codes.** **[DWG]** = this drawing · **[SCH]** = DinMeter schematic ·
**[DOC]** = M5Stack DinMeter product/doc page.

## 1. What it is

A **1.25 mm pitch, horizontal (卧式 — right-angle / side-entry), surface-mount wire-to-board
header** with two through-body solder tabs for mechanical retention. It is the connector
commonly sold as "MX1.25" and dimensionally in the same family as the JST **GH** series; M5Stack
uses it as the standard LiPo socket across many of its products.

The drawing is **generic across the series**, covering **2P through 20P**. Only the `A`/`B`/`C`
dimensions change with pole count.

## 2. Dimensions

Series table **[DWG]** — the first row is the fitted part:

| Variant | `A` (pin span) | `B` (body) | `C` (overall, incl. tabs) |
|---|---:|---:|---:|
| **1.25WT-2P** | **1.25 mm** | **4.42 mm** | **7.55 mm** |
| 1.25WT-3P | 2.50 | 5.67 | 8.80 |
| 1.25WT-4P | 3.75 | 6.92 | 10.05 |
| 1.25WT-5P | 5.00 | 8.17 | 11.30 |
| 1.25WT-6P | 6.25 | 9.42 | 12.55 |
| 1.25WT-8P | 8.75 | 11.92 | 15.05 |
| 1.25WT-10P | 11.25 | 14.42 | 17.55 |
| 1.25WT-20P | 23.75 | 26.92 | 30.05 |

(The sheet lists every pole count from 2 to 20; the rows above are a representative subset. Note
the arithmetic: `A = (N−1) × 1.25`, `B = A + 3.17`, `C = A + 6.30`.)

Common dimensions **[DWG]**: pitch **1.250 ±0.1 mm** · body height **3.500 ±0.1 mm** ·
depth **3.500 ±0.1 mm** with a **2.450 mm** internal step · contact tail **0.300 mm** ·
tolerances **`A` ±0.1, `B` ±0.2, `C` ±0.2**.

Recommended footprint **[DWG]**: signal pads on the **1.25 mm** pitch, **0.80 mm** pad width,
**3.00 mm** pad-row spacing, retention-tab pads offset **2.10 mm**, tab pad pitch **3.00 mm**.

General tolerance table **[DWG]**: ≤3 mm → ±0.10 · >3–10 → ±0.15 · >10–20 → ±0.2 ·
>20 → ±0.25 (未注公差 — "unspecified tolerances").

Material **[DWG]**: `Nylon 9tul 94v-0 or ul` — i.e. a nylon housing with a **UL94 V-0**
flammability rating. The sheet carries a **RoHS** mark.

## 3. ⚠ What the drawing does *not* tell you

This is a **mechanical drawing only**. It is complete for layout and **useless for electrical
design**. Absent from the sheet:

| Not specified | Why it matters |
|---|---|
| **Current rating** | The DinMeter charges and discharges a 250 mAh cell through it. Nothing here bounds that |
| **Voltage rating** | — |
| **Contact resistance** | — |
| **Contact material and plating** | Determines corrosion behaviour and mating cycles |
| **Mating cycles** | These are small, springy contacts; the number is usually 30 or fewer in this family |
| **Insertion / withdrawal force** | — |
| **Operating temperature** | Only the housing material is given |
| **Mating housing / crimp terminal part numbers** | You cannot order the cable half from this sheet |

> For a battery connector, the missing **current rating** is the one that matters. If you need a
> number, take it from a branded equivalent whose datasheet you actually hold (JST GH is rated
> **1 A** per contact with AWG 28–32) — and **record that you substituted the rating**, because
> this drawing does not support it. *(inferred; the fitted part's rating is unknown.)*

## 4. ⚠ Unattributed — and deliberately filed as generic

The sheet carries **no company name, no logo, no part-number prefix and no contact details**.
The title block's 设计/审核/批准 (design / check / approve) signature boxes are **empty**, the
版次 (revision) box is **empty**, and the change table at top-right has **no rows**. The only date
is 初始日期 **2011-06-16**.

`1.25WT` is a **descriptive designation**, not a manufacturer's series: `1.25` = pitch,
`WT` = 卧贴 / 卧式贴片 ("horizontal SMT"). Many Chinese connector houses publish near-identical
sheets under the same string.

**So this record is filed at `components/generic/` and makes no manufacturer claim.** If a
branded equivalent is later confirmed for the fitted part, this record should link to it rather
than be replaced — other records cite this path.

> ⚠ **Correction to [`devices/m5stack/dinmeter/sources.md`](../../../devices/m5stack/dinmeter/sources.md)
> row S-27**, which describes this file as *"No text layer — image-only scan"*.
> **It is not a scan.** It is a **vector CAD export** (`Producer: ODA PDF Export v4.2.1.0`,
> page size 7086 × 5011 pt), and it renders crisply at any resolution. It has no text layer
> because the annotations are stroked geometry, not glyphs — which is why `pdftotext` returns
> **zero** lines rather than garbage. Everything in §2 was read from a **60 dpi** render; the
> drawing needs no more than that. The practical difference: a "scan" implies the content is
> degraded and hard to recover, and **it is not**.

## Used By

### M5Stack DinMeter (K134) and DinMeter v1.1 (K134-V11)

[`devices/m5stack/dinmeter`](../../../devices/m5stack/dinmeter/README.md) ·
[`devices/m5stack/dinmeter-v1.1`](../../../devices/m5stack/dinmeter-v1.1/README.md)

Designator **`J2`**, the **Li-ion battery** socket **[SCH]** **[DOC]**. Both SKUs ship with a
**250 mAh** cell. Charging is by `U2` [TP4057](../tp4057/README.md) **[SCH]** — a 500 mA linear charger
with a **4.24 V float** — so peak current through the connector is bounded well below any
plausible rating for the family.

> **Two contacts only — no NTC.** The 2-pole variant carries `BAT+` and `BAT−` and nothing else.
> Any charge-temperature protection on this board must therefore come from somewhere other than
> the cell. The same structural point is recorded for the PaperMono's `J2`
> ([`devices/m5stack/papermono/pinouts-and-buses.md`](../../../devices/m5stack/papermono/pinouts-and-buses.md)).

> ⚠ **Polarity is not defined by this drawing.** A 2-pin connector will mate happily either way
> round if the cable is crimped mirrored, and **nothing on this sheet marks pin 1**. Which
> contact is `BAT+` is a property of the **schematic and the cell's own cable**, not of the
> connector. Verify before connecting a cell that did not ship with the board — M5Stack, Adafruit
> and generic AliExpress LiPo cells do **not** all use the same polarity on a 1.25 mm 2-pin
> housing, and reversing it is a destructive error.

## Artifacts

| File | Bytes | SHA-256 | Notes |
|---|---:|---|---|
| [`artifacts/1.25wt-2p-drawing-m5stack-mirror.pdf`](artifacts/1.25wt-2p-drawing-m5stack-mirror.pdf) | 1 110 811 | `743d2118e45770340869efb7de84fe5dfa2625de9f36bb6524d95d24c9d5ea31` | 1 page, 7086 × 5011 pt. Vector, **no text layer**. Retrieved **2026-09-04**, filed **2026-09-20** |

Source URL (M5Stack mirror — filed under **M5Dial's** path, not DinMeter's):

```
https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/core/M5Dial/1.25WT-2P.pdf
```

**Renamed on filing** from `1.25WT-2P.pdf`; bytes unchanged. Filename lower-cased for
portability; the dot in `1.25wt` is retained because it is part of the designation.

**Disposition** `repository` · **Licence** `unknown` — no notice of any kind on the sheet ·
**Redistribution status** `unknown`.

PDF metadata: `Producer: ODA PDF Export v4.2.1.0`, `CreationDate` **2018-04-17**,
`ModDate` **2024-02-18**. Note the **creation date (2018) is seven years after the drawing's own
初始日期 (2011)** — the PDF is a later re-export of an older DWG, so the 2018/2024 timestamps date
the *file*, not the *drawing*.

## Substitutes

| Family | Note |
|---|---|
| **JST GH** (`SM02B-GHS-TB` and relatives) | Same 1.25 mm pitch and closely similar geometry; a branded part with a real datasheet, including a current rating. ⚠ **Not guaranteed to intermate** — verify the housing latch and polarisation against the fitted part before assuming a cable will fit |
| "MX1.25" / `A1251` generics | What is usually actually sold. Same caveat, and no datasheet at all |
| **JST PH 2.0 mm** | **Not a substitute** — different pitch. Worth naming because it is the *other* common LiPo connector (the Tanmatsu uses PH-2.0), and the two are easy to confuse in photographs |

## Gaps

* **No manufacturer** (§4) and therefore **no vendor sourcing guide**.
* **No electrical ratings at all** (§3) — current, voltage, contact resistance, mating cycles and
  temperature range are all unknown for the fitted part.
* **The mating cable housing and crimp terminal are not identified.**
* **Pin-1 polarity is not marked on the drawing** and must be taken from the schematic.
* Whether M5Stack's DinMeter actually fits a part built to *this* drawing, as opposed to a
  look-alike, is **unverified** — the link is that M5Stack published this sheet for this
  connector.
