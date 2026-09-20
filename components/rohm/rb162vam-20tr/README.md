# ROHM RB162VAM-20TR

> **Schottky barrier diode**, 20 V / 1 A, **ultra-low V<sub>F</sub> = 0.36 V typ @ 1 A**, in ROHM's TUMD2M (SOD-323HE) package, marking **`N`**.
> Research snapshot **2026-09-01**. Fitted as **`D2` on sheet 2** of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) — the **rectifier of the e-paper frontlight boost converter**.
> ⚠ **ROHM lists this part as *Not Recommended for New Designs*.** **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | ROHM `RB162VAM-20` data sheet, **Rev.001, 2017-05-16**, © 2016 ROHM; local copy `artifacts/rb162vam-20tr-rohm-octopart-mirror.pdf` | `not-tested` |
| **[WEB]** | ROHM product page for `RB162VAM-20TR`, retrieved 2026-09-01 | `not-tested` |
| **[SCH-V]** | Read off sheet 2 rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity and ratings **[DS]**

| Property | Value |
|---|---|
| Part | **`RB162VAM-20`**; ordering code **`RB162VAM-20TR`** (`TR` = taping) |
| Manufacturer | **ROHM Co., Ltd.** |
| Function | Schottky barrier diode, general rectification |
| Structure | Silicon epitaxial planar |
| Package | **TUMD2M**, i.e. **SOD-323HE** **[WEB]** |
| **Marking** | **`N`** |
| **V<sub>R</sub>** | **20 V** |
| V<sub>RM</sub> (repetitive peak, duty ≤ 0.5) | **25 V** |
| **I<sub>O</sub>** | **1 A** (glass-epoxy mounted, 60 Hz half-sine, resistive, T<sub>c</sub> ≤ 85 °C) |
| I<sub>FSM</sub> | 5 A (100 µs, non-repetitive, single cycle, 25 °C) |
| **V<sub>F</sub>** | **0.36 V typ, 0.40 V max @ I<sub>F</sub> = 1 A** |
| **I<sub>R</sub>** | **0.3 mA typ, 1.2 mA max @ V<sub>R</sub> = 20 V** |
| T<sub>j</sub> | 125 °C |
| T<sub>stg</sub> | −40 to +125 °C |
| Packaging | embossed tape, 180 mm reel, 8 mm width, **3000 pcs** |
| Features (vendor) | *"High reliability; small mold type; **super low V<sub>F</sub>**"* |

### 1.1 ⚠ Not Recommended for New Designs

ROHM's product page states: *"**Not Recommended for New Designs.** This product
cannot be used for new designs (Not recommended for design diversion)."*
**[WEB]**

This does not mean the PaperMono is at risk — M5Stack is presumably buying to an
existing agreement, and NRND parts remain available for years. It does mean:

- **Do not copy this circuit into a new design with this part.** Pick a current
  ROHM equivalent (`RB160VAM-30`, `RB168VAM-40` and relatives) or another vendor.
- Long-term repairability of the PaperMono depends on a part ROHM has already
  begun retiring.

### 1.2 ⚠ The reverse leakage is large, and it is a standby-current term

**I<sub>R</sub> = 0.3 mA typical, 1.2 mA maximum at 20 V.** That is enormous for a
signal diode and entirely normal for an ultra-low-V<sub>F</sub> Schottky — the two
trade against each other directly, and ROHM sells this part on the V<sub>F</sub>.

On a battery device the number deserves a second look. **0.3 mA is roughly two
thirds of a milliamp-hour per hour**; on a 1150 mAh cell, a continuously reverse-
biased `D2` alone would be about **160 days** of standby. That is tolerable, but
it is the same order as several other quiescent terms on this board, and it is
strongly temperature-dependent (Schottky leakage roughly doubles every 10 °C).

**It only applies while the frontlight rail is up and the converter is idle.**
When `BL_15V_L3B` is off there is no reverse bias to leak across. **[INF]** —
not measured, and the actual reverse voltage in the idle state was not
established.

---

## 2. Used By

### `devices/m5stack/papermono` — `D2`, sheet 2

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md).
**One instance.**

**On the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md):**
`inferred` **yes** — both SKUs have the same e-paper panel and the same
frontlight; the Lite differs only in dropping NFC and LoRa. Not read from the
Lite's own schematic.

---

## 3. Circuit role — the frontlight boost rectifier **[SCH-V]**

```
EPD_3V3_L3 ──[ L3  10 µH ]──┬────▶|──── D2 ────┬── R27 0 Ω ──┬── BL_15V_L3B
   FTC201610S100MBCA        │   RB162VAM-20TR  │             │
                            │                  │        C26 NC/50V
                     U11 pin 4 SW           C24 33 pF/50 V   (not fitted)
                     AW9967DNR              C25 1 µF/50 V
                     (boost WLED driver)
```

| `D2` terminal | Net |
|---|---|
| **anode** | the switch node — `L3` and the [AW9967DNR](../../awinic/aw9967/README.md)'s `SW` pin |
| **cathode** | the boost output, through `R27` = 0 Ω to **`BL_15V_L3B`** |

This is a textbook asynchronous boost: `U11` pulls `SW` low, current ramps in
`L3`, `U11` releases, and the inductor's flyback pushes charge through `D2` into
`C25`. The frontlight LED string hangs off `BL_15V_L3B` and its current is set by
`R29` = 18 Ω on the AW9967's `BL_FB` pin.

### 3.1 ⚠ 20 V on a rail named 15 V — the margin is thin, and possibly thinner

The net is called **`BL_15V_L3B`**, and `D2` is a **20 V** part. In a boost, the
diode's reverse voltage while the switch is on is approximately the *output*
voltage, so nominally `D2` sees about **15 V against a 20 V rating — 75 % of
V<sub>R</sub>**, before any switching-node ringing.

That is tight but not wrong. What makes it worth flagging is the surrounding
component choice: **`C24`, `C25` and `C26` are all rated 50 V**, and the AW9967
is a WLED boost whose output rises to whatever the LED string's forward voltage
demands. A 50 V output capacitor is not what a designer fits for a hard 15 V
rail; it is what they fit when the node can go higher. If the string's total
V<sub>F</sub> ever exceeds ~20 V — more LEDs, a colder panel, a different
frontlight supplier — **`D2` is the part that fails first.** **[INF]**

Countervailing evidence: the net *name* says 15 V, the AW9967's own output range
was not checked against this for this record, and the design presumably passed
qualification. **This is a flag, not a defect claim.** It is recorded because a
reader copying this circuit should size the rectifier from the LED string, not
from the net name.

### 3.2 Why an ultra-low-V<sub>F</sub> part here

At a boost output of ~15 V from a 3.3 V input, duty is high and the diode
conducts for the short remainder of each cycle at a comparatively large peak
current. **V<sub>F</sub> × I is the dominant loss in an asynchronous boost's
rectifier**, and 0.36 V versus a typical 0.55 V Schottky is a meaningful
efficiency difference on a battery-powered backlight that may be on for hours.
The design is trading the high reverse leakage of §1.2 for conduction efficiency.
**[INF]**

---

## 4. Substitution

Required: **Schottky**, V<sub>R</sub> ≥ 20 V (**consider 30–40 V** given §3.1),
I<sub>O</sub> ≥ 1 A, SOD-323HE / TUMD2M footprint, low V<sub>F</sub>.

| Alternative | Note |
|---|---|
| ROHM **`RB160VAM-30`**, **`RB168VAM-40`** | Same family, 30 V / 40 V — **the sensible replacement given §1.1 and §3.1** |
| ROHM **`RB162VA-20`** | The non-`M` variant in TUMD2 — **different package** |
| **`1N5819WS`** ([used elsewhere on this board](../../generic/1n5819ws/README.md)) | 40 V / 1 A, SOD-323 — more voltage margin, **higher V<sub>F</sub> (0.6 V @ 1 A)**, hence lower efficiency |
| Generic SOD-323 Schottky | ⚠ Check both V<sub>F</sub> *and* I<sub>R</sub>; the two trade off (§1.2) |

Note that the board already stocks `1N5819WS` for the e-paper bias converter, so
consolidating on it would remove a BOM line at a small efficiency cost. That
M5Stack did **not** do so is itself evidence that the frontlight's efficiency was
considered worth a separate part number. **[INF]**

---

## 5. Integration pitfalls

1. **NRND** (§1.1) — do not design it in fresh.
2. **20 V on a rail whose capacitors are rated 50 V** (§3.1). Size a replacement
   from the LED string's forward voltage.
3. **0.3–1.2 mA reverse leakage** (§1.2), rising fast with temperature.
4. **T<sub>j</sub> is only 125 °C**, low for a rectifier, and the datasheet warns:
   *"To avoid occurrence of thermal runaway, actual board is to be designed to
   fulfil dPd/dTj < 1/Rth(j-a)."* Schottky thermal runaway is a real failure mode
   at high reverse bias and high temperature — the two conditions §1.2 and §3.1
   between them describe.
5. **`R27` = 0 Ω** sits between the rectifier and the rail. It is a link, and a
   convenient place to break the frontlight rail for measurement.
6. **`C26` is `NC`** — the output capacitance is `C25` = 1 µF/50 V alone, plus a
   33 pF snubber. That is little bulk for a boost; a replacement diode with more
   junction capacitance will change the ringing behaviour noticeably. **[INF]**

---

## 6. Open questions

- The frontlight LED string's forward voltage, which determines the actual
  reverse stress on `D2` (§3.1). Not published; the frontlight is part of the
  panel assembly.
- The AW9967's switching frequency and output-voltage limit as configured —
  partly covered in the [AW9967 record](../../awinic/aw9967/README.md), not
  cross-checked against `D2` here.
- Whether `D2` is reverse-biased when the frontlight is off (§1.2).
- No measurement of anything.

---

## Manufacturer

**ROHM Co., Ltd.** No vendor sourcing guide exists in this repository yet.

**⚠ Retrieval finding — ROHM's own CDN would not serve this document.** Every
`fscdn.rohm.com` path tried returned a **404 with a 321-byte HTML body**,
including the two forms ROHM uses for current and NRND parts:

| URL | Result |
|---|---|
| `fscdn.rohm.com/en/products/databook/datasheet/discrete/diode/schottky_barrier/rb162vam-20-e.pdf` | **404** |
| `fscdn.rohm.com/en/products/databook/datasheet-nrnd/…/rb162vam-20-e.pdf` | **404** |
| `fscdn.rohm.com/…/rb162vam-20.pdf` (no `-e`) | **404** |
| `www.rohm.com/datasheet/RB162VAM-20/rb162vam-20-e` | **403** |
| `datasheets.ibselectronics.com/RB162VAM-20TR-Rohm-datasheet-142143350.pdf` | **403** to all five user-agents |
| **`datasheet.octopart.com/RB162VAM-20TR-Rohm-datasheet-142143350.pdf`** | **200, `%PDF` ✓**, 2 202 076 B |

**The document is on Octopart's mirror under the same numeric ID as the IBS
Electronics copy that 403s** — `142143350`. That ID appears to be a shared
distributor-datasheet identifier, so **when `datasheets.ibselectronics.com/<name>-<id>.pdf`
is blocked, try `datasheet.octopart.com/<name>-<id>.pdf`**. That is the reusable
finding here and it belongs in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

Plausible reason for the ROHM 404s: NRND parts are removed from the public
datasheet CDN while the product page survives. If so, **ROHM's own site is not a
reliable source for any NRND part**, and a mirror is mandatory.

## Related pages

- [Awinic AW9967DNR](../../awinic/aw9967/README.md) — `U11`, the boost controller `D2` rectifies for
- [1N5819WS](../../generic/1n5819ws/README.md) — the board's other Schottky, 40 V, in the e-paper bias converter
- [PaperMono frontlight feature guide](../../../devices/m5stack/papermono/features/frontlight.md)
- [PaperMono power architecture](../../../devices/m5stack/papermono/power-architecture.md) · [bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| D1 | `RB162VAM-20` Schottky Barrier Diode data sheet | ROHM (via Octopart mirror) | primary, via mirror | <https://datasheet.octopart.com/RB162VAM-20TR-Rohm-datasheet-142143350.pdf> | 2026-09-01 | **Rev.001, 2017-05-16**, © 2016 ROHM, 8 pp | all of §1: V<sub>R</sub>, V<sub>RM</sub>, I<sub>O</sub>, I<sub>FSM</sub>, V<sub>F</sub>, **I<sub>R</sub>**, T<sub>j</sub>, marking `N`, taping, the thermal-runaway warning | `artifacts/rb162vam-20tr-rohm-octopart-mirror.pdf` |
| W1 | `RB162VAM-20TR` product page | ROHM | primary | <https://www.rohm.com/products/diodes/schottky-barrier-diodes/ultra-low-vf/rb162vam-20-product> | 2026-09-01 | — | **"Not Recommended for New Designs"**; package **SOD-323HE**; the *ultra-low V<sub>F</sub>* category placement | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | `D2` = `RB162VAM-20TR`; the §3 topology; `L3` = 10 µH, `R27` = 0 Ω, `C24`/`C25`/`C26` values and the `NC` | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/rb162vam-20tr-rohm-octopart-mirror.pdf` | 2 202 076 | `e769d2b55951abd54ba6fc9832086c73860cde41fa7b09408daa50ea40a4b33d` | 8 |

**Method note.** D1 validated as `%PDF` (`executed-success`) with an intact text
layer; its first page was read directly and is the source of every number in §1.
Six URLs across four hosts were tried before one served the document — see
[Manufacturer](#manufacturer). §3 was read from a 200 dpi render of sheet 2.
