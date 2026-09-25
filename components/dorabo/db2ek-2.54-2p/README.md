# Dorabo DB2EK-2.54-2P-GN-S — 2.54 mm pluggable screw-terminal plug

> The **DC input terminal** on the M5Stack DinMeter (K134 / K134-V11), designator `J1`.
> Record created **2026-09-20**, when the drawing was filed out of scratch.
> Manufacturer, read from the drawing's own title block: **宁波地博电气有限公司 /
> Ningbo Dorabo Electric CO., Ltd**, brand **DORABO** **[DWG]**.
> Document: `DB2EK-2.54-XXP-C-S` **customer drawing**, rev **T0-1**, sheet 1/1, A4, scale 1:1,
> drawn *Steven Lu* / checked *Duck Mao* / approved *JTing Chen*, all dated **2022-04-23**
> **[DWG]**.

**Evidence codes.** **[DWG]** = this drawing · **[SCH]** = DinMeter schematic ·
**[DOC]** = M5Stack DinMeter product/doc page.

> ⚠ **Naming correction.** Existing DinMeter records romanise the manufacturer as
> *"Ningbo Dibo Electric"*. The company's **own English name on its own drawing** is
> **Ningbo Dorabo Electric CO., Ltd**, with the brand rendered `DORABO`. *Dibo* is a plausible
> pinyin transliteration of 地博 but it is not what the vendor calls itself. Use **Dorabo** —
> it is also the only spelling that will find the company in a search.

## 1. What the part number means

The drawing's own decode block **[DWG]**:

```
DB2EK — 2.54 — XXP — C — S/P
  │       │      │     │    └── screw head: S = Slotted, P = Phillips
  │       │      │     └─────── colour code
  │       │      └───────────── poles
  │       └──────────────────── pitch, mm
  └──────────────────────────── series
```

Colour codes: `1` Green · `2` Black · `3` Blue · `4` Clear · `5` Gray · `6` Orange · `7` Red ·
`8` White · `9` Yellow.

> ⚠ **The M5Stack filename does not follow the vendor's own scheme.** M5Stack serves the drawing
> as `DB2EK-2.54-2P-GN-S.pdf` — `GN` where the vendor's decode expects the numeral `1` for green.
> The correct vendor ordering code for the fitted part is therefore **`DB2EK-2.54-02P-1-S`**, and
> `DB2EK-2.54-2P-GN-S` is M5Stack's own descriptive shorthand, not an orderable part number.
> *(inferred from the decode block; no vendor price list was consulted.)*

**The drawing is generic across the series.** It covers **02–24 poles**; nothing on the sheet is
specific to the 2-pole variant. Every dimension below is either a constant or a formula in `N`.

## 2. Electrical ratings — and why there are two sets

The drawing carries **two independent rating blocks**, and they do not agree. This is normal and
it is not a defect: they are different standards with different derating philosophies.

**UL/CUL** (`UL` mark on the sheet) **[DWG]**:

| Use group | B | C | D |
|---|---:|---:|---:|
| Rated voltage | **150 V** | — | — |
| Rated current | **5 A** | — | — |

**IEC** (`VDE` mark on the sheet) **[DWG]**:

| | III | III | II |
|---|---:|---:|---:|
| Overvoltage category | III | III | II |
| Pollution degree | 3 | 2 | 2 |
| Rated voltage | **100 V** | **130 V** | **320 V** |
| Rated current | **5 A** | **5 A** | **5 A** |
| Rated impulse withstand | 1.5 kV | 1.5 kV | 1.5 kV |

Withstanding voltage **1300 V for 1 minute** **[DWG]**.

> **Read the voltage ratings as a set, not as a maximum.** 320 V is available *only* at
> overvoltage category II and pollution degree 2 — i.e. a clean, mains-isolated enclosure. In a
> dirtier environment (pollution degree 3) the same part is a **100 V** connector. The current
> rating is **5 A in every case**.

## 3. Wire, mechanical and material

| Property | Value | **[DWG]** |
|---|---|---|
| Wire range | **26–20 AWG**, solid or stranded | |
| Conductor cross-section | **0.5 mm²** | |
| **Stripping length** | **5–6 mm** | |
| **Screw torque (max)** | **M1.6 / 0.1 N·m** | |
| Pitch | **2.54 mm** | |
| Poles available | **02–24** | |
| Insulation material | **PA66** | |
| Flammability | **UL94V-0** | |
| Contact material | **copper alloy**, **nickel plated** | |
| Operating temperature | **−40 to +105 °C** | |
| Pin dimensions / PCB hole diameter | **listed as "–"** — not specified on this sheet | |

Body dimensions **[DWG]**: width **N × 2.54 + 0.60 mm** (so **5.68 mm** for 2 poles), height
**13.15 mm**, depth **10.50 mm**, with a **5.85 mm** dimension to the wire-entry face.
Linear tolerances follow **GB/T 14486-2008** per the table at top-left (±0.20 mm up to 6 mm,
±0.30 to 10 mm, ±0.50 to 30 mm, …).

> ⚠ **0.1 N·m is a very small torque** — about what you get from a jeweller's screwdriver at
> gentle finger pressure. These are M1.6 screws in a plastic body. Over-tightening strips them,
> and there is no torque feedback. This is the single most common way to kill one of these
> connectors.

## 4. ⚠ This drawing shows the **plug**, not the board header

The rendered sheet shows a **pluggable (plug/female) half** with screw clamps and a wire-entry
face — the part the user's wires land in. It **mates with a separate PCB-mounted header** that is
**not on this drawing and not otherwise documented here**.

Consequences:

- **`Pin Dimensions` and `PCB Hole Diameter` are both "–" on the sheet** because the plug has no
  PCB pins. Anyone laying out a board to accept this connector needs the **header** drawing, which
  this repository does **not** hold.
- Mating retention, insertion force and mating cycles are **not specified** on this sheet.
- The 5 A rating belongs to the plug. The header's rating is unverified here.

**Not resolved:** which header part M5Stack fits on the DinMeter PCB. The schematic labels `J1`
with the plug's part number **[SCH]**, which is the vendor's habit of naming the connector by its
user-facing half.

## Used By

### M5Stack DinMeter (K134) and DinMeter v1.1 (K134-V11)

[`devices/m5stack/dinmeter`](../../../devices/m5stack/dinmeter/README.md) ·
[`devices/m5stack/dinmeter-v1.1`](../../../devices/m5stack/dinmeter-v1.1/README.md)

Designator **`J1`**, the **6–36 V DC input**, feeding `D13`/`D12` → `U1`
[ME3116AM6G](../../microne/me3116am6g/README.md) buck → `+5VIN` **[SCH]** **[DOC]**.
Green body, slotted screws — i.e. the `-1-S` variant.

**The DinMeter v1.1 ships the plug in the box** ("2.54-2P terminal" in the v1.1 bundle list);
the v1.0 bundle lists a "DC-JACK terminal" **[DOC]**. Same part, different bundle wording.

> **Headroom on this board.** The DinMeter's input range is **6–36 V** **[DOC]**. Against §2,
> 36 V is comfortably inside every rating in the table. **Current is the binding constraint, not
> voltage**: 5 A, with 26–20 AWG wire. A DIN-rail meter drawing a watt or two is nowhere near
> either limit, so the connector is not a design risk here — but it is also **not a power
> terminal**, and it should not be repurposed as one.

> ⚠ **Strain relief.** The DinMeter's own feature guide already warns that this is *"a screw
> terminal on a small body"*
> ([`features/din-mounting-and-mechanical.md`](../../../devices/m5stack/dinmeter/features/din-mounting-and-mechanical.md)).
> §3 gives the number behind that warning: **M1.6 screws at 0.1 N·m**.

## Artifacts

| File | Bytes | SHA-256 | Notes |
|---|---:|---|---|
| [`artifacts/db2ek-2.54-xxp-c-s-customer-drawing-rev-t0-1-m5stack-mirror.pdf`](artifacts/db2ek-2.54-xxp-c-s-customer-drawing-rev-t0-1-m5stack-mirror.pdf) | 383 085 | `ed6e82d9ca0d69f082dd0313a0d5d57220c072061d6a4bffaf8a18cd7977779d` | 1 page, A4, **page rotation 270°**. Retrieved **2026-09-04**, filed **2026-09-20** |

Source URL (M5Stack mirror — note it is filed under **M5Dial's** path, not DinMeter's):

```
https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/core/M5Dial/DB2EK-2.54-2P-GN-S%202.54mm%202Pin%20Green.pdf
```

**Renamed on filing** from `DB2EK-2.54-2P-GN-S.pdf` (itself already shortened from the
space-containing URL filename); bytes unchanged.

**Disposition** `repository` · **Licence** `unknown` — the sheet is marked
`TYPE: CUSTOMER_DRAWING` with no licence or confidentiality notice · **Redistribution status**
`unknown`.

**Text-layer note.** The PDF was produced by *"Microsoft: Print To PDF"* from an AutoCAD model
(`Title: F:\0Z5P\DB2EK-2.54\DB2EK-2.54-XXP-C-S Model (1)`, `Author: 86134`, created
2022-04-24). Its text layer yields only **ten lines** — the part-number decode block. **Every
number in §2 and §3 was read from a 150 dpi render**, not from extracted text. The render was
validated against the decode block, which appears in both the text layer and the image.

## Substitutes

The `xxEK`/`2EDG`-style 2.54 mm pluggable terminal is a commodity form factor with many makers
(Degson, Ningbo Kangnex/WJ, Dinkle and others). **Mating is by mechanical compatibility with the
board header, not by part number**, and the header is undocumented here (§4). Before substituting:

- confirm **pitch 2.54 mm** and pole count;
- confirm the **plug keying/polarisation** matches the fitted header — series differ here and a
  wrong-series plug can be forced in;
- check the substitute's **own** UL/IEC ratings rather than assuming §2 transfers.

## Gaps

* **The mating PCB header is not identified and not documented** (§4). That is the piece a board
  designer actually needs.
* **No vendor sourcing guide** exists for Dorabo — no `vendors/dorabo/` record. The only copy of
  this drawing held here came from M5Stack's bucket; Dorabo's own site was not reached in this
  pass, and no attempt is recorded.
* **Mating cycles, insertion/withdrawal force and contact resistance are not on the sheet** and
  were not found elsewhere.
* Whether the fitted part is genuinely a Dorabo part or a look-alike from another maker is
  **unverified** — the identification rests on M5Stack having published *this* drawing for *this*
  connector, not on a marking on the physical part.
* Rev **T0-1** (2022-04-23) may not be current; no newer revision was sought.
