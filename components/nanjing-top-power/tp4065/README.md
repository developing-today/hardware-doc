# TP4065 — linear Li-ion charger (as documented; **not** as fitted)

- **Category:** single-cell Li-ion constant-current / constant-voltage linear charger with a
  resistor-programmed charge current.
- **Manufacturer:** **unresolved.** TP40xx parts are widely attributed to Nanjing Top Power ASIC
  Corp; **no primary document was obtained** during this pass and the filing directory reflects
  the common attribution, not established evidence. Compare the sibling
  [`generic/tp4057`](../../generic/tp4057/README.md) record, which reached the same wall and
  filed under `generic/` instead.
- **Retrieved:** 2026-09-07

## ⚠ Read this first: the part in the schematic is not the part on the board

`U6` on the **LilyGO T-Display-S3** schematic (`T_Display_S3.pdf`, title block 2024-04-29) is
labelled **`TP4065`**. An owner who traced a physical board reported something else entirely:

> "when I try to find the TP4056 on the PCB it cannot be found? The datasheet shows that the IC
> should be an 8 pin SOP-8 package which cannot be located. Tracing out the PCB I find that the
> charging IC appears to be a device that is a **5-Lead TSOT-23 package with the marking of
> `65b311`** printed on top. This does not agree with the posted schematic."
> — [LilyGO issue #230](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/230), 2024-03-02.
> Evidence class: **firsthand physical inspection.** (Note the reporter writes "TP4056" in
> prose while the schematic reads TP4065 — two different parts with similar programming
> equations.)

LilyGO never published a corrected sheet. **This record therefore documents a designator, not a
confirmed fitted part.** The unidentified `65b311`/`AXPM65611` string has its own record:
[`components/unidentified/lilygo-t-display-s3-family/axpm65611/`](../../unidentified/lilygo-t-display-s3-family/axpm65611/README.md).

## 1. What the schematic says

| Property | Value | Evidence |
|---|---|---|
| Designator | `U6` | `T_Display_S3.pdf` designator census |
| Pins shown | `CHRG 1`, `GND 2`, `BAT 3`, `VCC 4`, `PROG 5` | same |
| Programming resistor | `R9 = 2K` | same |
| Sheet note | **`R13  IBAT (mA) = 580`** | same |
| Vendor README | *"The default charging current is **500mA**"* | `README.md` @ `ec889e7` |

**500 mA and 580 mA are both stated by LilyGO, in two documents, for the same board.** A 2 kΩ
`PROG` resistor gives ≈580 mA under the TP4056/TP4065 equation *I = 1200 V / R<sub>PROG</sub>*,
which matches the schematic note and not the README.

## 2. Where it also appears

The same `TP4065` designator string appears on **three** LilyGO schematics:

| Board | Designator |
|---|---|
| T-Display-S3 | `U6` |
| T-Display-S3 AMOLED (V1.0 sheet) | `U5` |
| T-Display-S3 AMOLED Touch (V2.0 sheet) | `U6` |

So whatever it is, it is LilyGO's standard cheap charger for the non-PMIC boards. The boards
that moved upmarket use a real I²C PMIC instead — [SY6970](../../silergy/sy6970/README.md)
on Long/Pro/T4-S3/1.64/1.43-1.75, [BQ25896](../../texas-instruments/bq25896/README.md) on
AMOLED Plus, [AXP2101](../../x-powers/axp2101/README.md) on AMOLED Lite.

## 3. Safety consequences on these boards

- **No battery protection is fitted anywhere on the T-Display-S3.** LilyGO's maintainer,
  2025-02-06: *"No built-in battery protection, needs to be used with a lithium-ion battery
  with battery protection."* Use a protected cell.
- **500–580 mA is above 1 C for a 350–400 mAh cell**, which is the size that fits third-party
  shells. That is what prompted issue #230.
- **Do not swap the programming resistor on the strength of the schematic.** The equation you
  would use comes from a datasheet for a part that a careful owner has already shown may not be
  fitted.

## 4. Gaps

- **No datasheet obtained**, for TP4065 or for the `65b311` part.
- Manufacturer unconfirmed.
- The actual charge current has never been measured by anyone in the searched set. A series
  ammeter into a discharged cell would settle the 500-vs-580 question **and** narrow the part
  identity by behaviour.

## 5. Used by

### LilyGO T-Display-S3 / Touch — designator `U6`
→ [`devices/lilygo/t-display-s3`](../../../devices/lilygo/t-display-s3/README.md).
Charges the JST 1.25 mm cell from USB-C 5 V only (`VBUS` is not brought out to the header).
Charge status drives the red LED. **Identity disputed — see the warning above.**

### LilyGO T-Display-S3 AMOLED — designator `U5` (V1.0 sheet) / `U6` (Touch sheet)
→ [`devices/lilygo/t-display-s3-amoled`](../../../devices/lilygo/t-display-s3-amoled/README.md).
Same role. Not independently verified against hardware.
