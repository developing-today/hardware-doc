# 1N5819WS — Schottky rectifier (maker **not specified by the schematic**)

> **40 V / 1 A Schottky barrier diode**, V<sub>F</sub> ≈ 0.6 V @ 1 A, 25 A surge, in **SOD-323**.
> Research snapshot **2026-09-01**. Used **three times** on the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) — `D4`, `D5` and `D6` on sheet 4 — all three inside the **e-paper panel's bias generator**, the highest-voltage circuit on the board.
> **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | `1N5817WS – 1N5819WS` datasheet (Guangdong Hottech), local copy `artifacts/1n5819ws-guangdong-hottech-lcsc-mirror.pdf` | `not-tested` |
| **[CAT]** | LCSC / JLCPCB catalogue entries `C191023`, `C369937`, retrieved 2026-09-01 | `not-tested` |
| **[SCH-V]** | Read off sheet 4 rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[MAN]** | DKE **EPD Module User Manual** §7.4, held under the [panel record](../../dke/depg0397bbs770f3/README.md) | `not-tested` |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity and ratings

| Property | Value | Evidence |
|---|---|---|
| Value string on the schematic | **`1N5819WS`** | **[SCH-V]** |
| Manufacturer | **not specified** — §1.1 | — |
| Function | Schottky barrier rectifier | **[DS]** |
| Package | **SOD-323** (Hottech) or **SOD-323F** (KEXIN) — §1.1 | **[CAT]** |
| Case material | moulded plastic, UL94V-0 | **[DS]** |
| Weight | ≈ 0.005 g | **[DS]** |
| **V<sub>RRM</sub>** | **40 V** | **[DS]** |
| I<sub>O</sub> | **1 A** | **[CAT]** |
| I<sub>FSM</sub> | **25 A** | **[CAT]** |
| **V<sub>F</sub>** | **600 mV @ 1 A** | **[CAT]** |
| I<sub>R</sub> | 500 µA @ 40 V (Hottech) / 1 mA @ 40 V (KEXIN) | **[CAT]** |
| Vendor applications | *"low voltage high frequency inverters and polarity protection"* | **[DS]** |

The datasheet is a **family document covering `1N5817WS` (20 V), `1N5818WS`
(30 V) and `1N5819WS` (40 V)** — the same die at three reverse ratings. Reading
the wrong column is the obvious hazard; **40 V is the `1N5819WS` column.**
**[DS]**

### 1.1 `1N5819WS` is a JEDEC type, not a vendor part

Like the [`1N4148WS`](../1n4148ws/README.md) on the same sheet, this is a
second-sourced industry type and the schematic prints only the type number. LCSC
lists at least:

| Maker | LCSC | Package | I<sub>R</sub> @ 40 V |
|---|---|---|---|
| **Guangdong Hottech** | `C191023` | **SOD-323** | 500 µA |
| KEXIN | `C369937` | **SOD-323F** | 1 mA |

**[CAT]**

**Note the package difference.** SOD-323 and SOD-323**F** are *not* the same
footprint — the `F` variant is a flat-lead version with a different land pattern.
That matters for a rework or a respin far more than the leakage spread does. **No
maker is asserted here**; the Hottech document is retained as representative
because its package matches the plain `SOD-323` that the type number implies.
What would resolve it: the top marking on a board, or M5Stack's BOM.

---

## 2. Used By

### `devices/m5stack/papermono` — **3 instances**, all sheet 4

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md).

| Ref | Role in the e-paper bias generator |
|---|---|
| **`D4`** | **boost rectifier** — switch node → `PREVGH` |
| **`D5`** | **charge-pump rectifier** — `PREVGL` → the flying-capacitor node |
| **`D6`** | **charge-pump clamp** — flying-capacitor node → GND |

**On the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md):**
`inferred` **yes, all three**. Both SKUs carry the identical
[DKE DEPG0397BBS770F3](../../dke/depg0397bbs770f3/README.md) panel, which needs
this bias circuit. Not read from the Lite's own schematic.

---

## 3. Circuit role — one boost and one inverting charge pump **[SCH-V]**

The [SSD1677](../../solomon-systech/ssd1677/README.md) inside the panel runs the
control loop; the power stage is on the mainboard and reaches the die through the
[24-way FPC](../fpc0.5-smt-24p-b/README.md) at `J5`.

```
EPD_3V3_L3 ──[ L8  33 µH ]───┬──────▶|─── D4 ───┬──── PREVGH ──▶ J5.21
  SPH252010H330MT            │                  │      C72 10 µF/25 V
                        Q4 drain                │
                        CJ2310 (N-ch)      C67 10 µF/25 V
  J5.2 GDR ──┬── Q4 gate                        │  (flying capacitor)
             │                                  │
        R58 10 kΩ                    ┌──────────┴──────────┐
             │                       │                     │
            GND                   D5 ▲ (anode at PREVGL)  D6 ▼ (cathode at GND)
                                     │                     │
   Q4 source ──┬── R59 1.2 Ω ── GND  └─── PREVGL ──▶ J5.23 └── GND
               └── J5.3 RESE              C73 10 µF/25 V
```

**`D4` — the boost rectifier.** Anode on the switch node, cathode on `PREVGH`.
When `Q4` ([CJ2310](../../changjing/cj2310/README.md)) releases, `L8`'s flyback
forward-biases `D4` and charges `C72`. Standard asynchronous boost.

**`D5` and `D6` — the inverting charge pump.** `C67` is a flying capacitor tied
to the same switch node. While the node is high, `D6` conducts and pins `C67`'s
far plate near ground, charging it. When the node falls to ~0 V, that plate is
driven **negative**, and `D5` conducts to pull `PREVGL` down with it. `C73`
holds the result.

So **one switching node, driven by one transistor, generates both a positive and
a negative rail.** This matches DKE's own typical application circuit **[MAN]**
§7.4 — the independent confirmation that this reading is right.

### 3.1 Why 40 V, and why the same part three times

`PREVGH` and `PREVGL` are the panel's gate-drive supplies, typically around
**+22 V** and **−20 V** for this class of e-paper driver. **[INF]** — not read
from the SSD1677 datasheet for this record.

- **`D4`** sees roughly `PREVGH` in reverse while `Q4` is on: **~22 V against
  40 V**, about 55 % of rating.
- **`D5`** sees roughly `PREVGH` − `PREVGL` at the worst moment, which is a
  larger swing, and **`D6`** sees roughly |`PREVGL`| plus the switch-node
  amplitude.

Using one 40 V part for all three is the sensible choice: it covers the worst
case, removes two BOM lines, and gives a consistent V<sub>F</sub> across the two
rails so they track. The **surrounding decoupling is 25 V-rated**
(`C67`, `C71`, `C72`, `C73` all 10 µF/25 V), which independently corroborates
that the rails sit in the low twenties. **[SCH-V]** + **[INF]**

Contrast with `D2` on sheet 2, the frontlight rectifier, which is a
**[20 V ROHM part](../../rohm/rb162vam-20tr/README.md)** chosen for
ultra-low V<sub>F</sub> — the designer took efficiency there and voltage margin
here. Two rectifiers, two different trade-offs, both defensible.

### 3.2 Consequences worth knowing

1. **The V<sub>F</sub> of `D5`/`D6` directly sets how negative `PREVGL` gets.**
   An inverting charge pump loses **two** diode drops, so `PREVGL` ≈
   −(switch-node amplitude − 2 × V<sub>F</sub>) ≈ 1.2 V short of ideal at 0.6 V
   each. Substituting a higher-V<sub>F</sub> part makes `PREVGL` less negative,
   which degrades the panel's gate drive and shows up as **poor contrast or
   ghosting**, not as a failure. **[INF]**
2. **Nothing in software controls or observes this.** `GDR` comes from inside the
   panel. A bias-rail problem is invisible from firmware and looks like a slow or
   dirty refresh.
3. **These are the only 40 V-class parts in the signal area of sheet 4.** When
   probing, `J5` pins 20–24 and the `D4`/`D5`/`D6` nodes are the high-voltage
   ones.

---

## 4. Substitution

Required: **Schottky**, V<sub>RRM</sub> ≥ 40 V, I<sub>O</sub> ≥ 1 A, low
V<sub>F</sub> (§3.2), **SOD-323 — check `F` vs plain** (§1.1).

| Alternative | Note |
|---|---|
| **`1N5819HW`**, `SS14`, `B5819W` | Same class, common second sources |
| **`1N5818WS`** (30 V) | ⚠ Same family, **less margin**; the datasheet's middle column |
| **`1N5817WS`** (20 V) | ⚠ **Do not** — 20 V is inadequate here (§3.1) |
| **`BAT54`** family | ⚠ 30 V and **200 mA** — far too little current |
| [`RB162VAM-20TR`](../../rohm/rb162vam-20tr/README.md) | ⚠ The board's other Schottky, but **20 V** — not a substitute in this circuit |

**Do not substitute a standard silicon rectifier** (`1N4148WS`, `1N4007`): the
0.7–1.0 V drop costs `PREVGL` another volt (§3.2), and the recovery time is far
too slow for a switching node.

---

## 5. Integration pitfalls

1. **SOD-323 vs SOD-323F** (§1.1) — different land patterns under the same type
   number.
2. **The datasheet is a three-part family document** (§1) — read the `1N5819WS`
   column, not the header.
3. **V<sub>F</sub> is a functional parameter here, not just a loss term** (§3.2).
4. **Reverse leakage 0.5–1 mA at 40 V**, and the panel's bias rails are held by
   10 µF capacitors that must survive the panel's deep-sleep periods. Leakage
   discharges them; how fast was not calculated. **[INF]**
5. **All three are in a converter whose controller is on the far side of a
   connector** — see the
   [CJ2310 record §3.1](../../changjing/cj2310/README.md#31-three-consequences-worth-knowing)
   for why a marginal FPC contact presents as a display-quality bug.

---

## 6. Open questions

- **The maker actually fitted, and therefore the exact package** (§1.1).
- The SSD1677's real `VGH`/`VGL` targets, which set the true reverse stress
  (§3.1) — obtainable from the
  [SSD1677](../../solomon-systech/ssd1677/README.md) and
  [panel](../../dke/depg0397bbs770f3/README.md) records, not read here.
- The converter's switching frequency, hence switching losses and ripple.
- Whether reverse leakage meaningfully discharges the bias rails in deep sleep
  (§5.4).
- No measurement of anything.

---

## Manufacturer

**Not specified by the schematic** (§1.1). The retained document is Guangdong
Hottech's. No vendor sourcing guide exists in this repository for that maker.

**⚠ Retrieval finding — the LCSC PDF host trap.** LCSC's catalogue gave
`https://www.lcsc.com/datasheet/lcsc_datasheet_2409300937_Guangdong-Hottech-1N5819WS_C191023.pdf`,
which returned **HTTP 200 and 48 710 bytes of HTML** to all five user-agents
tried (Chrome 131, ClaudeBot, WhatsApp, ChatGPT-User, plain `curl`). Rewriting to
the CDN worked first try:

```
wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2409300937_Guangdong-Hottech-1N5819WS_C191023.pdf
```

**No user-agent rotation helps, because this is not bot-blocking — it is the
wrong host.** **Check the `%PDF` magic bytes; both the status code and the `.pdf`
extension lie.** `executed-success`, 2026-09-01, reproduced across five parts from
this board. This belongs in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

## Related pages

- [Changjing CJ2310](../../changjing/cj2310/README.md) — **`Q4`, the switch these three rectify for**
- [DKE DEPG0397BBS770F3](../../dke/depg0397bbs770f3/README.md) — the panel; §7.4 of its manual is the reference circuit
- [Solomon Systech SSD1677](../../solomon-systech/ssd1677/README.md) — the controller driving `GDR`
- [FPC0.5-SMT-24P-B](../fpc0.5-smt-24p-b/README.md) — `J5`, where `PREVGH`/`PREVGL` cross to the panel
- [ROHM RB162VAM-20TR](../../rohm/rb162vam-20tr/README.md) — the board's other Schottky, a different trade-off
- [PaperMono bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| D1 | `1N5817WS – 1N5819WS` Schottky Barrier Diode | Guangdong Hottech (via LCSC CDN) | representative primary, via distributor mirror | <https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2409300937_Guangdong-Hottech-1N5819WS_C191023.pdf> | 2026-09-01 | undated, 4 pp | **40 V** V<sub>RRM</sub> for the `WS` suffix, SOD-323, UL94V-0, 0.005 g, the family's three-part structure — **for the Hottech part, not confirmed as the fitted one** (§1.1) | `artifacts/1n5819ws-guangdong-hottech-lcsc-mirror.pdf` |
| C1 | LCSC entries `C191023`, `C369937` | LCSC / JLCPCB | distributor | JLCPCB SMT parts API, keyword `1N5819WS` | 2026-09-01 | — | the §1.1 multi-vendor spread including the **SOD-323 vs SOD-323F** package difference; 1 A, 25 A, 600 mV, leakage | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | all three instances; the §3 topology and every diode orientation; `L8`, `R58`, `R59`, `C67`, `C72`, `C73`; the `J5`.2/.3/.21/.23 connections | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| M1 | EPD Module User Manual §7.4 | DKE | primary | see the [panel record](../../dke/depg0397bbs770f3/README.md#12-authoritative-sources) | 2026-09-01 | 30 pp | independent confirmation of the §3 topology | `../../dke/depg0397bbs770f3/artifacts/depg0397bbs770f3-epd-module-user-manual.pdf` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/1n5819ws-guangdong-hottech-lcsc-mirror.pdf` | 1 157 833 | `609a5bc2fcd5bbb36f47f802b11102f1e140eae519c74b067cb615b4d52d0a4f` | 4 |

**Method note.** D1 validated as `%PDF` (`executed-success`) with an intact text
layer. The **orientation of all three diodes** — which is what distinguishes a
boost rectifier from a charge-pump clamp, and therefore the whole of §3 — was read
from a 200 dpi render of sheet 4. The text layer in that region places `D4`, `D5`,
`D6`, `Q4`, `C67`, `C71`–`C73`, `R58`, `R59` and `L8` in one cluster and cannot
resolve anode from cathode.
