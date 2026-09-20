# Silergy SY8089 — 2 A synchronous step-down regulator

> The **3.3 V rail** generator on every Cardputer mainboard (designator **U4**).
> Record created **2026-09-04**. Sibling in this repository: [`silergy/sy7088`](../sy7088/README.md),
> the boost that generates `+5VOUT` on the same boards.

## Function

A small synchronous buck converter in a 5-pin package: `EN`, `IN`, `LX`, `FB`, `GND`. It steps
the board's 5 V rail down to 3.3 V for all the logic. Output voltage is set by an external
feedback divider.

## Key capabilities

| Property | Value | Evidence |
|---|---|---|
| Topology | synchronous buck | schematic |
| Package | 5-pin (SOT-23-5 class) | schematic symbol: `EN`, `IN`, `LX`, `FB`, `GND` |
| Rated current | ~2 A class for this family | **not verified — no datasheet retrieved** |
| Feedback reference | **not established** — see the arithmetic problem below | — |

## Pinout as drawn

| Pin | Name | Cardputer connection |
|---|---|---|
| 1 | `IN` | `+5VOUT` |
| 2 | `EN` | enable network |
| 3 | `LX` | **L2, 4.7 µH** → `+3.3V` |
| 4 | `GND` | GND |
| 5 | `FB` | divider (see below) |

Output capacitors C10/C11 100 nF and C12 22 µF; input C8/C9.

## ⚠ The feedback arithmetic does not resolve

The schematic sheet prints its own formula beside the neighbouring **SY7088**:
`Vout = 1.2 V × (R1/R2 + 1)`. Applying it to the resistors identified near the SY8089
(**R12 68 kΩ**, **R13 15 kΩ**) gives:

`1.2 × (68/15 + 1) = 6.64 V` — **not 3.3 V.**

Two possible explanations, neither resolved in this pass:

1. **The resistor identification is wrong.** Sheet 1 is dense and several `R` values sit close
   together; the text-layer extraction may have associated the wrong pair with this divider.
   R11 (100 kΩ) is also in the vicinity.
2. **The SY8089 has a different feedback reference** than the SY7088. The printed formula is
   annotated next to the boost, not the buck, and the two parts need not share a reference.

**Recorded rather than fudged.** Do not use a computed output voltage for this rail; the rail is
3.3 V because that is what the board runs on, and the divider values above should not be quoted
as evidence for it until either a datasheet or a higher-resolution sheet crop settles which is
true. See [`devices/m5stack/cardputer-adv/gaps-and-conflicts.md`](../../../devices/m5stack/cardputer-adv/gaps-and-conflicts.md) §U4.

This is exactly the failure mode the skill warns about: an inferred value that *looks* like a
finding. It is not one.

## Used By

- **[LilyGO T-Display-S3 family](../../../devices/lilygo/t-display-s3-shared/README.md)** — an `SY8089`-family buck appears as `U4` on the [T-Display-S3 AMOLED](../../../devices/lilygo/t-display-s3-amoled/README.md) V2.0 sheet (`SY8089A1AAC`, replacing the V1.0 board's RT9080 **LDO**), on the [T-Display-S3 Long](../../../devices/lilygo/t-display-s3-long/README.md) (`SY8089AAAC`), on the [T-Display-S3 Pro](../../../devices/lilygo/t-display-s3-pro/README.md) (`SY8089AAAC`) and on the [T4-S3](../../../devices/lilygo/t4-s3/README.md). Read from the schematic designator strings; net connectivity was not traced. The LDO→buck substitution between AMOLED V1.0 and V2.0 is one of the few concrete differences identifiable between those two concurrently sold revisions.

### M5Stack Cardputer ADV (K132-Adv) — [`devices/m5stack/cardputer-adv`](../../../devices/m5stack/cardputer-adv/README.md)

Designator **U4** on schematic sheet 1. Generates `+3.3V` from `+5VOUT` (itself the SY7088's
boost output from the battery), with L2 4.7 µH. Powers the ES8311, TCA8418, BMI270, NS4150B,
the display and the Stamp module's input.

Note the rail topology: **battery → SY7088 boost → 5 V → SY8089 buck → 3.3 V**. Everything the
board does is paid for at the product of two converter efficiencies. That is worth knowing when
reading M5Stack's current figures, and it is why a Grove or CAP peripheral drawing from
`+5VOUT` is comparatively cheap while 3.3 V logic is not.

### M5Stack Cardputer v1.0 (K132) and v1.1 (K132-V11)

[`devices/m5stack/cardputer-v1.0`](../../../devices/m5stack/cardputer-v1.0/README.md) ·
[`devices/m5stack/cardputer-v1.1`](../../../devices/m5stack/cardputer-v1.1/README.md)

**Same part, same designator U4**, on the shared schematic (SHA-256 `6016c1fe…`). The Cardputer
power train — TP4057, SY7088, SY8089, CN809J, three LP3218DT1G FETs — is **identical across all
three generations**; only the battery topology changed (120 + 1400 mAh in a base → a single
1750 mAh cell).

## Substitutes

| Part | Note |
|---|---|
| SY8088, SY8113, SY8009 | Silergy siblings at different current ratings and packages |
| TPS62xxx, MP1584, RT8059 | common alternatives; **check the feedback reference**, which varies (0.6 V, 0.8 V, 1.2 V…) and changes the divider |
| An LDO | far simpler, far worse — the whole point here is efficiency on a battery |

## Gaps

* **No datasheet retrieved.** Rated current, feedback reference, switching frequency, efficiency
  curve, `EN` threshold and thermal limits are all unknown.
* **The feedback divider identification is unresolved** (above). Settling it needs either the
  datasheet's reference voltage or a 1:1 crop of sheet 1 around U4.
* Manufacturer inferred from the `SY` prefix, which is Silergy's convention; not confirmed
  against a package marking.

---

## Update — 2026-09-07: **the feedback arithmetic resolves. The divider is `R11`/`R13`, and the reference is 0.6 V.**

Appended, not substituted. The section above — *"⚠ The feedback arithmetic does not resolve"* —
was working from a misread divider **and** from a formula belonging to a different converter.
Both are corrected here. Method:
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md).

Evidence: `devices/m5stack/cardputer-adv/artifacts/schematic/Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf`,
sheet 1, `Creator: Altium Designer`, traced with `pdftotext -bbox-layout`.

### Error 1 — the upper resistor is `R11` (68 kΩ), not `R12`

`R12` is **100 kΩ**, at `COR12` (236.50, 221.20) — roughly 460 pt away on the opposite side of
the sheet, in an unrelated network. It is not part of this feedback divider.

The `U4` feedback column is unambiguous once coordinates are read:

```
PIR1102 @ 690, 206.9   -> the +3.3V output rail (row y 203.8)
PIR1101 @ 690, 228.9 --+
                       |--- FB node; U4 pin 5 (FB) @ 640, 232.37
PIR1302 @ 691, 235.6 --+
PIR1301 @ 691, 258.2   -> GND (y 280.1)

COR11 @ 697.50, 214.20   value "68KΩ"  @ 702, 222.4
COR13 @ 698.00, 243.93   value "15KΩ"  @ 702, 251.4
```

### Error 2 — the printed formula belongs to the SY7088, not the SY8089

`Vout=1.2V*(R1/R2+1)` sits at **(612.67, 157.65)**, directly beneath the **SY7088 boost `U2`**
(symbol spans y 63–135). The SY8089 `U4` symbol is at y 192–244, about 86 pt lower. The formula
was never annotating this part.

Applied to `U2`'s own divider — `R4` 75 kΩ (@ 673, 99.2) / `R6` 22 kΩ (@ 673, 128.9) — it gives
1.2 × (75/22 + 1) = **5.29 V**, self-consistent for the `+5VOUT` rail it feeds. That is the
formula doing its job on the part it belongs to.

### Result

```
Vout = Vfb x (R11/R13 + 1) = Vfb x (68/15 + 1) = Vfb x 5.5333
3.3 V  =>  Vfb = 3.3 / 5.5333 = 0.596 V
```

A **0.6 V** feedback reference makes the design exact to 0.7 %. Of the two possibilities the
section above offered, the second — *"the SY8089 has a different feedback reference than the
SY7088"* — is correct, and the value it requires is 0.6 V.

⚠ **Evidence status: `inferred`, not `primary`.** This 0.596 V is *derived from the board's own
divider and its intended output*, not read from a datasheet. **No SY8089 datasheet is retained in
this repository** — the "No datasheet retrieved" gap noted above is unchanged, and acquiring one
remains the way to promote this from inferred to established. What has changed is that the
arithmetic is no longer impossible, and the row above reading *"Feedback reference | **not
established** — see the arithmetic problem below"* can now be read as "not established from a
primary source; requires 0.6 V for this board to work as designed".

### Practical note for anyone re-deriving an output voltage

The divider is `R11` over `R13` on this board. If you change the output voltage, the relation is
`Vout = 0.6 V × (R_upper/R_lower + 1)`. Do **not** use the 1.2 V constant printed on the same
sheet — it is the boost converter's.

Traced in full: [`devices/m5stack/cardputer-adv/schematic-netlist.md`](../../../devices/m5stack/cardputer-adv/schematic-netlist.md) §3.
