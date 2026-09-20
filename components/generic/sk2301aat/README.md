# Shikues SK2301AAT

> **P-channel MOSFET**, −20 V, −2.1 A, 130 mΩ @ V<sub>GS</sub> = −4.5 V, TrenchFET, **SOT-523**, marking **`A1S`**.
> Research snapshot **2026-09-01**. Fitted as **`Q5` on sheet 2** of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153), where it is the **high-side switch that connects the battery to the `VBAT_DET` net — and only while USB is plugged in**.
> **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Shikues `SK2301AAT` datasheet **REV.08**, local copy `artifacts/sk2301aat-shikues-lcsc-mirror.pdf` | `not-tested` |
| **[CAT]** | LCSC / JLCPCB catalogue entry `C5334586`, retrieved 2026-09-01 | `not-tested` |
| **[SCH-V]** | Read off sheet 2 rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity and ratings

| Property | Value | Evidence |
|---|---|---|
| Part | **`SK2301AAT`** | **[SCH-V]**, **[DS]** |
| Manufacturer | **Shikues** | **[CAT]** |
| LCSC part | `C5334586` | **[CAT]** |
| Function | **P-channel** enhancement MOSFET, TrenchFET | **[DS]** |
| Package | **SOT-523** | **[DS]** |
| **Top marking** | **`A1S`** | **[DS]** |
| V<sub>DS</sub> | **−20 V** | **[DS]** |
| **V<sub>GS</sub>** | **±8 V** | **[DS]** |
| I<sub>D</sub> continuous | **−2.1 A** | **[DS]** |
| I<sub>DM</sub> pulsed | −4.8 A | **[DS]** |
| I<sub>S</sub> (body diode) | −0.72 A | **[DS]** |
| R<sub>DS(on)</sub> | **130 mΩ @ −4.5 V** | **[CAT]** |
| P<sub>D</sub> | **0.35 W** | **[DS]** — LCSC lists 700 mW; §1.2 |
| R<sub>θJA</sub> | 357 °C/W (t ≤ 5 s) | **[DS]** |
| T<sub>J</sub> | 150 °C | **[DS]** |
| T<sub>stg</sub> | −55 to +150 °C | **[DS]** |
| Applications (vendor) | *"Load switch for portable devices; DC/DC converter"* | **[DS]** |

### 1.1 Pinout **[DS]**

| Pin | Function |
|---:|---|
| **1** | **GATE** |
| **2** | **SOURCE** |
| **3** | **DRAIN** |

This ordering is what makes the §3 circuit reading unambiguous, and it was
checked against the schematic symbol's own `S`/`G`/`D` labels, which agree.

### 1.2 ⚠ A power-dissipation discrepancy between the datasheet and the distributor

The datasheet's absolute-maximum table says **P<sub>D</sub> = 0.35 W**. LCSC's
parametric field says **700 mW**. **[DS]** vs **[CAT]**

Both numbers are plausible for SOT-523 depending on the pad area and pulse
duration assumed — 0.35 W is a steady-state figure and 0.7 W typically a t ≤ 5 s
or 1-inch-square-copper figure. **The discrepancy is recorded, not resolved.**
Use **0.35 W** as the design figure: it is the manufacturer's, and it is the
conservative one. On this board the dissipation is negligible either way (§3.2).

---

## 2. Used By

### `devices/m5stack/papermono` — `Q5`, sheet 2

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md).
**One instance**, and it is the only P-channel device on the board outside the
complementary pair inside
[`Q1` CJ3439KDW](../../changjing/cj3439kdw/README.md).

**On the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md):**
`inferred` **yes**. The Lite drops only NFC and LoRa; the charging and battery
sensing path is stated to be identical, including the same 1150 mAh cell. Not
read from the Lite's own schematic.

---

## 3. What it actually switches **[SCH-V]**

Read from sheet 2 rendered at 200 dpi. `Q5` works with
**`Q2`** ([SK2302AAT](../sk2302aat/README.md), N-channel) as a two-transistor
level-shifting high-side switch:

```
                         VBAT_L0
                            │
                   R45 100 kΩ   ┌── Q5 pin 2  SOURCE
                            ├───┤   SK2301AAT  (P-channel)
                            │   └── Q5 pin 3  DRAIN ──── VBAT_DET
                            │
    VUSB_IN ── Q2 pin 1 ── Q5 pin 1 GATE
      │        (GATE)
   R9 100 kΩ   Q2 pin 3 DRAIN
      │        Q2 pin 2 SOURCE ── GND
     GND        SK2302AAT (N-channel)
```

| Terminal | Net |
|---|---|
| `Q5` pin 2 — **SOURCE** | **`VBAT_L0`** (the battery rail) |
| `Q5` pin 3 — **DRAIN** | **`VBAT_DET`** |
| `Q5` pin 1 — **GATE** | `Q2`'s drain, held at `VBAT_L0` by **`R45` = 100 kΩ** |
| `Q2` pin 1 — **GATE** | **`VUSB_IN`**, held down by **`R9` = 100 kΩ** |

**Operation:**

| USB state | `Q2` | `Q5` gate | `Q5` | `VBAT_DET` |
|---|---|---|---|---|
| **Unplugged** — `VUSB_IN` ≈ 0 V | off (`R9` holds the gate at GND) | pulled to `VBAT_L0` by `R45` ⇒ V<sub>GS</sub> = 0 | **off** | **disconnected** |
| **Plugged** — `VUSB_IN` ≈ 5 V | on | pulled to GND ⇒ V<sub>GS</sub> ≈ −V<sub>BAT</sub> | **on** | **= `VBAT_L0`** |

So: **`VBAT_DET` carries the battery voltage only while USB power is present.**
`Q2` is doing nothing but detecting USB presence and inverting it; `Q5` is the
actual switch.

### 3.1 Why build it this way

A P-channel high-side switch cannot be driven directly from a logic level
referenced to ground when its source sits at V<sub>BAT</sub> — pulling the gate
to 3.3 V would leave V<sub>GS</sub> ≈ −0.9 V at a 4.2 V cell, not enough to
enhance it, and would leave it partly on at low cell voltage. The N-channel
pull-down is the standard fix: it swings the gate the full V<sub>BAT</sub> and
costs one transistor and two resistors. **[INF]**

Using **`VUSB_IN` itself as the control signal** rather than a GPIO is the neat
part. It makes the function **automatic and unpowered** — the detection works
before any firmware runs, and it consumes nothing when USB is absent. **[INF]**

### 3.2 Operating conditions on this board — the part is enormously de-rated

| Parameter | Rating **[DS]** | On this board | Margin |
|---|---|---|---|
| V<sub>DS</sub> | −20 V | ≤ 4.35 V (a full 1S Li-ion) | **~4.6×** |
| **V<sub>GS</sub>** | **±8 V** | ≤ 4.35 V | **~1.8×** |
| I<sub>D</sub> | −2.1 A | a sense/detect current through a high-impedance node | ≫ |
| P<sub>D</sub> | 0.35 W | negligible | ≫ |

**V<sub>GS</sub> = ±8 V is the only rating worth watching**, and it is fine here
because a 1S Li-ion cannot exceed ~4.35 V. It would **not** be fine in a 2S
design, which is the first thing to check if this sub-circuit is copied.

---

## 4. Where `VBAT_DET` goes — not established

`VBAT_DET` also appears near the [IP2315 charger](../../injoinic/ip2315/README.md)
block on sheet 2. **What consumes it was not resolved**: the text layer in that
region interleaves the charger's, the OVP switch's and this circuit's labels, and
the region was not re-rendered to settle it.

Two readings, neither adopted:

- a **battery-presence input** to the charger, which would let the charger
  distinguish "no cell fitted" from "deeply discharged cell" — but only while USB
  is present, which is exactly when the charger needs to know;
- an **ADC sense point**, though the board already has a dedicated and better one
  in the [`Q1`/`R5`/`R12` gated divider](../../changjing/cj3439kdw/README.md#3-what-it-actually-switches-sch-v)
  feeding `BAT_ADC`.

The **first is more plausible** — gating it on USB presence makes sense for a
charger-side detect and makes little sense for a general voltage measurement.
`inferred`, and listed as an open question.

---

## 5. Substitution

`2301` is a de-facto industry number for a small P-channel MOSFET, so drop-in
equivalents are abundant — **but the package is not.**

| Alternative | Package | Note |
|---|---|---|
| Vishay **Si2301CDS**, AOS **AO3401A**, Diodes **DMP2160U** | **SOT-23** | Electrically comparable or better; **larger footprint** |
| UMW / Slkor / CJ `2301` parts | SOT-23 or SOT-523 | Chinese second sources; check the package suffix |
| **Any SOT-523 P-channel ≥ 20 V, ≥ 0.5 A** | SOT-523 | What actually matters here |

Required for this position: **P-channel**, |V<sub>DS</sub>| ≥ 20 V,
**V<sub>GS</sub> ≥ ±8 V**, low-threshold (must enhance at 3.0 V of gate drive at
a depleted cell), and **pin 1 = G, 2 = S, 3 = D** — SOT-523 pinouts are not
universal across vendors and a mismatched one silently connects the body diode
the wrong way round.

---

## 6. Integration pitfalls

1. **V<sub>GS</sub> = ±8 V only.** Fine at 1S; **not** at 2S (§3.2).
2. **The body diode conducts even when the FET is off.** Source is `VBAT_L0`,
   drain is `VBAT_DET`; the intrinsic diode points source→drain in a P-channel,
   so `VBAT_DET` is never fully isolated from the cell — it sits about a diode
   drop below it if something pulls it up. Not a problem for a sense node, but it
   means "off" does not mean "open". **[INF]**
3. **P<sub>D</sub>: 0.35 W or 0.7 W depending on the source** (§1.2).
4. **`Q5` and `Q2` are a pair.** Replacing one without the other breaks the
   polarity logic — `Q2` is N-channel, `Q5` is P-channel, and `SK2301AAT` and
   [`SK2302AAT`](../sk2302aat/README.md) differ by **one digit** in the part
   number while differing in channel type. That is an easy and destructive
   confusion at a rework bench.
5. **The control signal is a power rail, not a GPIO.** Firmware cannot disable
   this path; there is no register for it.

---

## 7. Open questions

- **What consumes `VBAT_DET`** (§4) — the main gap in understanding this circuit.
- The P<sub>D</sub> discrepancy (§1.2).
- V<sub>GS(th)</sub> and R<sub>DS(on)</sub> at low gate drive, which govern
  behaviour at a depleted cell — in the datasheet's electrical table, not
  transcribed here.
- No measurement of anything; the whole circuit is `inferred` from the drawing.

---

## Manufacturer

**Shikues.** No vendor sourcing guide exists in this repository yet.

**⚠ Retrieval finding.** The datasheet is on **`wmsc.lcsc.com`** and **not** on
`www.lcsc.com/datasheet/…`, which returns **HTTP 200 with `text/html`** under a
`.pdf` URL. **Check the `%PDF` magic bytes, never the status code.** For this part
the direct `wmsc` URL worked first try with a Chrome 131 UA; for its sibling
[`SK2302AAT`](../sk2302aat/README.md) the `www.lcsc.com` form had to be rewritten
to the `wmsc` form by hand. The rewrite is mechanical:

```
www.lcsc.com/datasheet/lcsc_datasheet_<stamp>_<name>_<code>.pdf
  ->  wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/<stamp>_<name>_<code>.pdf
```

`executed-success`, 2026-09-01, on five parts. This belongs in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

## Related pages

- [Shikues SK2302AAT](../sk2302aat/README.md) — **`Q2`, the N-channel half of this switch**, and `Q3` the buzzer driver
- [Changjing CJ3439KDW](../../changjing/cj3439kdw/README.md) — `Q1`, the board's other two-transistor gated sense circuit
- [Injoinic IP2315](../../injoinic/ip2315/README.md) — the charger `VBAT_DET` probably serves
- [Awinic AW32901FCR](../../awinic/aw32901/README.md) — what produces `VUSB_IN`'s downstream rail
- [PaperMono power architecture](../../../devices/m5stack/papermono/power-architecture.md) · [bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| D1 | `SK2301AAT` P-Channel 20-V (D-S) MOSFET | Shikues (via LCSC CDN) | primary, via distributor mirror | <https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2311241453_Shikues-SK2301AAT_C5334586.pdf> | 2026-09-01 | **REV.08**, 4 pp | channel type, SOT-523, marking `A1S`, **pin 1 = G / 2 = S / 3 = D**, all §1 maxima | `artifacts/sk2301aat-shikues-lcsc-mirror.pdf` |
| C1 | LCSC entry `C5334586` | LCSC / JLCPCB | distributor | JLCPCB SMT parts API, keyword `SK2301AAT` | 2026-09-01 | — | manufacturer; R<sub>DS(on)</sub> 130 mΩ @ 4.5 V; 290 pF / 29 pF; 3.9 nC; the 700 mW figure of §1.2 | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | `Q5` = `SK2301AAT`; the §3 topology, `R45` = 100 kΩ, `R9` = 100 kΩ, `Q2` = SK2302AAT | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/sk2301aat-shikues-lcsc-mirror.pdf` | 580 924 | `427b287b6b7a9a50633b3e4e1963082f34c53a0e30484180c19a032c2662fe7a` | 4 |

**Method note.** D1 validated as `%PDF` (`executed-success`) with an intact text
layer, and its pinout table is what makes §3 assertable rather than guessed. The
circuit itself was read from a 200 dpi render of sheet 2 — the text layer in that
region attributes labels to the wrong designators, and an earlier text-only pass
produced a reading that the image refuted.
