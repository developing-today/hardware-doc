# Unidentified — Stamp-S3A step-down converter (`U4`)

- **Category:** synchronous step-down (buck) converter IC, wafer-level/CSP ball grid, with
  pin-strapped output selection.
- **Manufacturer / part number:** ⚠ **NOT ESTABLISHED.** The `Sch_StampS3_v0.3.3.pdf` symbol
  carries **no part-number text**.
- **Retrieved:** 2026-09-04

The 5 V → 3.3 V converter on the **M5Stack Stamp-S3A** (board rev v0.3.3), replacing the
[MUN3CAD01-SC](../../../murata/mun3cad01-sc/README.md) µPOL module used on the Stamp-S3 v0.2.

---

## 1. What is established

From `Sch_StampS3_v0.3.3.pdf`, marker layer parsed:

| Property | Value |
|---|---|
| Designator | `U4` |
| Ball/pin names, 8 total | `A1 SW`, `A2 VIN`, `B1 EN`, `B2 GND`, `C1 VSEL1`, `C2 VOS`, `D1 VSEL2`, `D2 VSEL3` |
| Vendor annotation on the sheet | **`IOUT: 0~0.6A`** |
| Input | `VIN_5V` |
| Output sense | `VOS` → `VDD_3V3` (a *sense* pin, so the output node is measured remotely rather than through a resistive divider) |
| External inductor | **`L4` = `MWTC201608S2R2`** — 2.2 µH in a 2016-metric (0806-imperial) package, on the `SW` node |
| Support passives | `C15` 1 nF, `C16` 10 µF/10 V, `C18` 100 nF/25 V, `C21` 10 µF, `C22` 10 µF, `C25` 10 µF |
| Enable | `B1 EN` ← `R16` 100 kΩ network |
| Output-voltage setting | **pin-strapped** via `VSEL1` / `VSEL2` / `VSEL3` — there is **no feedback divider**; `R6` and `R17` from the v0.2 design are deleted |

## 2. Why this is recorded as unidentified rather than guessed

The topology is distinctive — three `VSEL` strap balls, a `VOS` sense pin, `SW` with an
external inductor, 0.6 A, 2 × 4 ball grid — and it would be easy to name a plausible family.
**No candidate part number is asserted anywhere in this repository**, because a comparison
shortlist is not a reading, and a near-miss part number on a power rail is exactly the kind of
error that propagates.

M5Stack's own Stamp-S3A specification page lists `DC-DC: MUN3CAD01-SC` and links that
datasheet. **That is demonstrably not this part**: the µPOL module has an integrated inductor
and an `FB` pin, no `SW`, no `VSEL` straps, and is rated 1 A rather than 0.6 A. The
specification row was evidently carried over from the Stamp-S3 page. See
[`components/m5stack/stamp-s3a/README.md` §5](../../../m5stack/stamp-s3a/README.md#5-change-3--the-dc-dc-was-replaced-and-the-datasheet-page-is-stale).

## 3. What would resolve it

1. A photograph of `U4`'s top marking on a Stamp-S3A (CSP parts often carry a 3–4 character
   code, which usually needs a vendor decode table).
2. The `MWTC201608S2R2` inductor's maker — a 2.2 µH/0806 power inductor is often specified in
   the converter vendor's own reference design, so identifying it may point at the IC family.
3. An M5Stack BOM, or a reply from `support@m5stack.com`.
4. An updated Stamp-S3A specification page. Worth re-checking periodically: the current page's
   DC-DC row is stale, so M5Stack may correct it.

## 4. Consequences while it stays unidentified

- **The 0.6 A output limit is a real design constraint** and it is *lower* than the Stamp-S3's
  1 A. Anything drawing 3.3 V through the module — an application that loads `VDD_3V3` heavily
  via the module's `3V3` pin — has less headroom on an S3A than on an S3. The vendor does not
  mention this anywhere. **`inferred` from the schematic annotation.**
- Efficiency curve, light-load mode behaviour, switching frequency, soft-start and protection
  behaviour are unknown, so the module's much-improved sleep figures cannot be attributed with
  confidence.
- Nothing here is firmware-visible: there is no register interface.

## 5. Artifacts

**None.** Establishing evidence:
[`components/m5stack/stamp-s3a/artifacts/Sch_StampS3_v0.3.3-StampS3A.pdf`](../../../m5stack/stamp-s3a/artifacts/Sch_StampS3_v0.3.3-StampS3A.pdf)
and the parsed layout beside it.

---

## Used By

### M5Stack Stamp-S3A (SKU S007-V033), board rev v0.3.3

`U4` — the module's only 5 V → 3.3 V converter.
→ [`components/m5stack/stamp-s3a/README.md`](../../../m5stack/stamp-s3a/README.md)

### Reached from this device

- [M5Stack DinMeter v1.1 (K134-V11)](../../../../devices/m5stack/dinmeter-v1.1/README.md) — the
  Stamp-S3A it fits contains this part.

---

## Update — 2026-09-07: **RESOLVED. The schematic prints `JW5712`.**

Appended, not substituted. The statement above — *"The `Sch_StampS3_v0.3.3.pdf` symbol carries
**no part-number text**"* — is **incorrect for the copy retained in this repository**, and the
sibling session's `JW5712` argument is confirmed *directly*, not inferentially.

### The evidence

File: `components/m5stack/stamp-s3a/artifacts/Sch_StampS3_v0.3.3-StampS3A.pdf`, page 1,
`Creator: Altium Designer`, 0 embedded rasters, 865 words, 50 `NL` tokens.

```
python3 trace.py grep bbox/<file>.xhtml 'JW5712'
  p1 x=193.49 y=546.41  JW5712
```

That coordinate is directly **below** the `U4` symbol body (pin tokens span x 171.5–243.5,
y 477.37–534.91), which is Altium's Comment/Value position; the designator `U4` sits
correspondingly **above** it at (186.67, 467.31). A 300 dpi render of the region shows
`U4` above the symbol and `JW5712` below it, in the vendor's ordinary designator/value styling.

So this is not an inference from pin function, package or current rating. **The sheet names the
part.**

### Why the earlier pass missed it

The earlier pass parsed the *marker* layer (`CO`/`PI` tokens) and correctly recovered all eight
ball names. The value string is ordinary visible text in the page's text layer, ~12 pt below the
symbol, and it was not in the coordinate window that was read. This is a good argument for
always running `netlist.py --components`, which reports each `CO<designator>` together with the
plain-text tokens nearest it, rather than only harvesting the marker layer.

### Ball map re-confirmed, with coordinates

Unchanged from the table above; restated with tokens so it can be re-checked.

| Ball | Name | Token | Net |
|---|---|---|---|
| `A1` | `SW` | `PIU40A1` @ 243.50, 477.37 | `L4` `MWTC201608S2R2` 2.2 µH → output node |
| `A2` | `VIN` | `PIU40A2` @ 171.50, 506.37 | `VIN_5V` |
| `B1` | `EN` | `PIU40B1` @ 171.50, 477.37 | `R16` 100 kΩ/1 % up to the `VIN` line |
| `B2` | `GND` | `PIU40B2` @ 171.50, 534.91 | `GND` |
| `C1` | `VSEL1` | `PIU40C1` @ 243.50, 520.37 | strap |
| `C2` | `VOS` | `PIU40C2` @ 243.50, 491.37 | `VDD_3V3` — remote sense |
| `D1` | `VSEL2` | `PIU40D1` @ 243.50, 527.37 | strap |
| `D2` | `VSEL3` | `PIU40D2` @ 243.50, 534.91 | strap |

Annotations on the sheet: **`IOUT: 0~0.6A`** @ (209.45–229.20, 452.93), and the section headings
`ESP32` @ (44, 403.8) / `DCDC` @ (44, 428.9) / `VDD_3V3` @ (42, 438.6).

**New observation from the render:** `VSEL1`, `VSEL2` and `VSEL3` are **all three tied together
to a single vertical net labelled `VIN_5V`**, with junction dots on `C1` and `D1`. The output
voltage is therefore selected by the strap combination "all high", not by any resistor network —
which is consistent with the existing observation that `R6` and `R17` from the v0.2 design are
deleted.

### Corroboration already in the repository

`devices/m5stack/cap-lora-1262/artifacts/schematic/U214-Cap-LoRa1262_SCH_V1.1_20251029.pdf`
carries the **same part** as `U3`, with the value string `JW5712` at (140, 186.3), the same
`IOUT: 0~0.6A` annotation and the same eight ball names — a second, independent M5Stack sheet
naming it. `devices/m5stack/cap-cc1101/…/U219-Cap_CC1101_SCH_V0.3_20260528.pdf` fits it a third
time as `U1`.

### Disposition

**This unidentified record is retained and must not be deleted** — other records link to it.
The real component record already exists:
[`components/joulwatt/jw5712`](../../../joulwatt/jw5712/README.md), with a scanned datasheet at
`components/joulwatt/jw5712/artifacts/jw5712-jw5712a-datasheet-scanned.pdf`.

> ⚠ Note for whoever works that datasheet: it is a **raster scan** — 4 pages, 4 full-page
> images, `pdftotext` yields **0 words**. It cannot be text-searched. See
> [`guides/reverse-engineering/schematic-pdf-traceability-census.md`](../../../../guides/reverse-engineering/schematic-pdf-traceability-census.md) §5.

Proposed index change (not applied):
[`archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/index-fragments.md`](../../../../archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/index-fragments.md).
