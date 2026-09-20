# Jiangsu Changjing CJ2310

> **N-channel MOSFET**, 60 V, 3 A, 125 mΩ @ V<sub>GS</sub> = 4.5 V, trench technology, **SOT-23**.
> Research snapshot **2026-09-01**. Fitted as **`Q4` on sheet 4** of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153), where it is the **external switching transistor for the e-paper panel's on-chip DC/DC** — the highest-voltage node on the board runs through it.
> **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Jiangsu Changjing `CJ2310` datasheet, local copy `artifacts/cj2310-changjing-lcsc-mirror.pdf` | `not-tested` |
| **[CAT]** | LCSC / JLCPCB catalogue entry `C75882`, retrieved 2026-09-01 | `not-tested` |
| **[SCH-V]** | Read off sheet 4 rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[MAN]** | DKE **EPD Module User Manual** §7.4, held under the [panel record](../../dke/depg0397bbs770f3/README.md) | `not-tested` |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity and ratings **[DS]**

| Property | Value |
|---|---|
| Part | **`CJ2310`** |
| Manufacturer | **Jiangsu Changjiang Electronics Technology Co., Ltd.** (江苏长电科技) |
| LCSC part | `C75882` **[CAT]** |
| Function | **N-channel** enhancement MOSFET, trench |
| Package | **SOT-23** |
| **V<sub>(BR)DSS</sub>** | **60 V** |
| I<sub>D</sub> continuous | **3 A** |
| R<sub>DS(on)</sub> | **105 mΩ @ 10 V**, **125 mΩ @ 4.5 V** |
| P<sub>D</sub> | 350 mW **[CAT]** |
| C<sub>iss</sub> / C<sub>rss</sub> | 247 pF / 19.5 pF **[CAT]** |
| Q<sub>g</sub> | 6 nC @ 10 V **[CAT]** |
| V<sub>DS(on)</sub> | 500 mV **[CAT]** |
| Operating range | −40 °C to +150 °C **[CAT]** |
| Vendor description | *"uses advanced trench technology to provide excellent R<sub>DS(ON)</sub>, low gate charge and operation with gate voltage as low as **2.5 V**. Suitable for use as a battery protection or in other switching application"* |
| Vendor applications | *"Battery switch; DC/DC converter"* |

### 1.1 Pinout **[DS]**

| Pin | Function |
|---:|---|
| **1** | **GATE** |
| **2** | **SOURCE** |
| **3** | **DRAIN** |

Same order as the board's SOT-523 Shikues parts, which makes the schematic
consistent to read across sheets.

### 1.2 ⚠ 60 V is the property that matters here

Every other MOSFET on this board is a 20 V part. `Q4` is **60 V**, and that is not
incidental — it is switching the node that generates the e-paper panel's
**`PREVGH`** and **`PREVGL`** gate-drive rails (§3). Choosing a 60 V device where
20 V parts serve everywhere else is the designer telling you where the voltage
is.

---

## 2. Used By

### `devices/m5stack/papermono` — `Q4`, sheet 4

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md).
**One instance.**

**On the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md):**
`inferred` **yes**. Both SKUs carry the identical
[DKE DEPG0397BBS770F3](../../dke/depg0397bbs770f3/README.md) panel, which needs
this converter. Not read from the Lite's own schematic, which is published only
as a 4-sheet `PRJ` PDF.

---

## 3. What it actually switches **[SCH-V]**

`Q4` is the switch of a **boost converter plus an inverting charge pump**, both
controlled by the **SSD1677 driver IC inside the e-paper panel** and both built
from discrete parts on the mainboard. The controller is on the far side of a
24-way FPC connector; only the power stage is here.

```
EPD_3V3_L3 ──[ L8  33 µH ]───┬─────▶|─── D4 ────┬──── PREVGH  ──▶ J5.21
  SPH252010H330MT            │    1N5819WS      │      (C72 10 µF/25 V)
                             │                  │
                        Q4 pin 3 DRAIN          │
                        (CJ2310, N-channel)     │
                             │                  │
  J5.2  GDR ──┬── Q4 pin 1 GATE                 │
              │                                 │
         R58 10 kΩ    ┌──┤ C67 10 µF/25 V ├─────┘
              │       │
             GND      ├──── D5 1N5819WS ──▶ (up, to the C67 node)
                      │
                      ├──── PREVGL ──▶ J5.23    (C73 10 µF/25 V)
                      │
                      └──── D6 1N5819WS ──▶ GND

        Q4 pin 2 SOURCE ──┬── R59 1.2 Ω ── GND
                          └── J5.3  RESE   (current sense, back to the panel)
```

| `Q4` terminal | Net | Note |
|---|---|---|
| pin 1 **GATE** | **`GDR`** = `J5`.2 | driven **by the panel**, not by the ESP32 |
| pin 2 **SOURCE** | `RESE` = `J5`.3, and **`R59` = 1.2 Ω** to GND | the current-sense node |
| pin 3 **DRAIN** | the switch node: `L8` and `D4`'s anode | |

**How it works.** The SSD1677 asserts `GDR`, `Q4` turns on, current ramps in
`L8` and develops a voltage across `R59`; the panel watches that voltage on
`RESE` and releases `GDR` at its peak-current threshold. The inductor's flyback
then forward-biases `D4` and charges `C72` to **`PREVGH`**, the positive
gate-drive rail. The same switching node drives `C67` as a flying capacitor, and
`D5`/`D6` rectify it the other way into **`PREVGL`**, the negative rail.

This matches DKE's own typical application circuit **[MAN]** §7.4 — which is the
independent confirmation that this reading of the topology is right.

### 3.1 Three consequences worth knowing

1. **Firmware does not control this converter.** `GDR` comes from inside the
   panel. There is no GPIO, no register on the ESP32-S3 side, and no way to
   observe it except with a probe. A display that will not refresh because
   `PREVGH` is not coming up looks, from software, exactly like a panel that is
   busy.
2. **`R59` = 1.2 Ω sets the peak current, and it sits in series with a
   connector.** The sense loop runs mainboard → `J5`.3 → panel and back. Contact
   resistance in the FPC joint adds to `R59`, *lowering* the peak current the
   panel thinks it has reached. A partially seated flex therefore produces weak
   bias rails and **display artefacts**, not a clean failure. **[INF]** This is
   worth trying before debugging waveform LUTs.
3. **`R58` = 10 kΩ is a gate pulldown.** With the panel unpowered or the flex
   unplugged, `GDR` floats; `R58` holds `Q4` off so the converter cannot
   self-start into an undefined state.

### 3.2 Operating conditions

| Parameter | Rating | On this board | Margin |
|---|---|---|---|
| V<sub>DS</sub> | **60 V** | switch node swings to `PREVGH` + V<sub>F</sub> | see below |
| V<sub>GS</sub> | ±20 V (typical for the class; **not transcribed from [DS]**) | `GDR` from a 3.3 V-class panel driver | comfortable |
| I<sub>D</sub> | 3 A | inductor peak set by `R59` | comfortable |
| R<sub>DS(on)</sub> | 125 mΩ @ 4.5 V | in series with `R59` = 1.2 Ω in the sense path | **~10 % of the sense resistance** |

**On V<sub>DS</sub>:** the SSD1677's `VGH` is typically around **+22 V** and
`VGL` around **−20 V** for this panel class. The drain therefore swings to
roughly `PREVGH` + 0.5 V ≈ 22.5 V, well inside 60 V. The 60 V part gives ~2.7×
margin, which is appropriate for a hard-switched node with inductor ringing.
**[INF]** — the exact `VGH`/`VGL` values were **not** read from the SSD1677
datasheet for this record.

**On R<sub>DS(on)</sub>:** 125 mΩ against `R59` = 1.2 Ω means `Q4`'s channel
contributes about **10 %** of the total sense resistance. That is not negligible,
and it is temperature-dependent — R<sub>DS(on)</sub> rises with junction
temperature, which lowers the peak current slightly as the panel warms. Whether
the SSD1677's design accounts for this is unknown; a 10 % term suggests the
resistor value was chosen with the FET's contribution in mind. **[INF]**

---

## 4. Substitution

Required: **N-channel**, V<sub>DS</sub> ≥ 60 V (do **not** substitute a 20 V or
30 V part — §1.2), logic-level threshold (must be fully on from the panel's gate
drive, which the vendor states works down to **2.5 V**), R<sub>DS(on)</sub>
≲ 150 mΩ so the sense-path contribution does not shift, SOT-23, **pin 1 = G,
2 = S, 3 = D**.

| Alternative | Note |
|---|---|
| Diodes **DMN6075S**, Vishay **Si2306BDS**, AOS **AO3402** | 60 V-class SOT-23 N-channel |
| **`2N7002`** | ⚠ **60 V but only ~115 mA** — nowhere near enough, and a classic substitution error |
| [AOS **AO3400A**](../../alpha-and-omega-semiconductor/ao3400a/README.md) | ⚠ **30 V only.** Documented in this repo, and **not** a substitute here |

**Match R<sub>DS(on)</sub> as well as voltage**, because it is 10 % of the
current-sense resistance (§3.2) — a much lower-R<sub>DS(on)</sub> part shifts the
converter's peak current up.

---

## 5. Integration pitfalls

1. **60 V for a reason** (§1.2, §3.2). The single most important substitution
   constraint.
2. **The gate is driven by the display, not the host** (§3.1). No software
   control, no software visibility.
3. **`R59` = 1.2 Ω and `Q4`'s R<sub>DS(on)</sub> are in the same sense path**
   (§3.2) — changing either changes the panel's bias rails.
4. **The sense loop crosses an FPC connector** (§3.1) — a mechanical fault
   presents as a display-quality bug.
5. **`R58` = 10 kΩ is not optional** (§3.1).
6. **This node reaches ~±20 V.** The decoupling around `J5` pins 17–24 is
   **25 V**-rated for that reason. Probe accordingly, and do not hot-plug the
   panel flex.
7. **Same maker, adjacent part numbers.** The board also carries
   [`CJ3439KDW`](../cj3439kdw/README.md); `CJ2310` and `CJ3439KDW` are both
   Changjing N-channel-bearing parts in different packages with different
   functions.

---

## 6. Open questions

- The SSD1677's actual `VGH`/`VGL` targets on this panel, which set `Q4`'s real
  V<sub>DS</sub> stress (§3.2) — obtainable from the
  [SSD1677 record](../../solomon-systech/ssd1677/README.md) and the
  [panel manual](../../dke/depg0397bbs770f3/README.md), not read for this record.
- The datasheet's V<sub>GS</sub> maximum and V<sub>GS(th)</sub> — present in the
  file, not transcribed.
- The switching frequency of the panel's DC/DC, hence `L8`'s ripple and `Q4`'s
  switching loss. Not published by DKE or Solomon Systech in the documents held.
- No measurement of anything.

---

## Manufacturer

**Jiangsu Changjiang Electronics Technology Co., Ltd.** (江苏长电科技, "CJ"),
`www.cj-elec.com`. No vendor sourcing guide exists in this repository yet.

**⚠ Retrieval finding — the LCSC PDF host trap.** LCSC's catalogue gave
`https://www.lcsc.com/datasheet/lcsc_datasheet_1810010214_…CJ2310_C75882.pdf`,
which returned **HTTP 200 and 47 960 bytes of HTML** to all five user-agents
tried. The CDN rewrite worked first try:

```
wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/1810010214_Jiangsu-Changjing-Electronics-Technology-Co---Ltd--CJ2310_C75882.pdf
```

**Check the `%PDF` magic bytes; the status code and the extension both lie.**
`executed-success`, 2026-09-01. Note also that LCSC spells the maker
**"Changjing"** in filenames while the datasheet header says **"CHANGJIANG"** —
search both spellings. This belongs in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

## Related pages

- [DKE DEPG0397BBS770F3](../../dke/depg0397bbs770f3/README.md) — the panel whose DC/DC this serves; §7.4 of its manual is the reference circuit
- [Solomon Systech SSD1677](../../solomon-systech/ssd1677/README.md) — the controller that drives `GDR`
- [FPC0.5-SMT-24P-B](../../generic/fpc0.5-smt-24p-b/README.md) — `J5`, the connector this converter's sense loop crosses
- [1N5819WS](../../generic/1n5819ws/README.md) — `D4`/`D5`/`D6` in the same converter
- [Changjing CJ3439KDW](../cj3439kdw/README.md) — same maker, `Q1`, the battery-sense gate
- [PaperMono bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| D1 | `CJ2310` SOT-23 Plastic-Encapsulate MOSFETs | Jiangsu Changjiang Electronics (via LCSC CDN) | primary, via distributor mirror | <https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/1810010214_Jiangsu-Changjing-Electronics-Technology-Co---Ltd--CJ2310_C75882.pdf> | 2026-09-01 | undated, 5 pp | **60 V**, 3 A, 105/125 mΩ, **pin 1 = G / 2 = S / 3 = D**, the 2.5 V gate-drive claim | `artifacts/cj2310-changjing-lcsc-mirror.pdf` |
| C1 | LCSC entry `C75882` | LCSC / JLCPCB | distributor | JLCPCB SMT parts API, keyword `CJ2310` | 2026-09-01 | — | manufacturer; 350 mW; 247 pF/19.5 pF; 6 nC; −40…+150 °C; the (broken) `www.lcsc.com` URL | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | `Q4` = `CJ2310`; the whole §3 topology; `L8`, `R58`, `R59`, `C67`, `C72`, `C73`, `D4`–`D6`; the `J5`.2/.3 connections | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| M1 | EPD Module User Manual §7.4 *Typical application circuit* | DKE | primary | see the [panel record](../../dke/depg0397bbs770f3/README.md#12-authoritative-sources) | 2026-09-01 | 30 pp | independent confirmation of the §3 topology | `../../dke/depg0397bbs770f3/artifacts/depg0397bbs770f3-epd-module-user-manual.pdf` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/cj2310-changjing-lcsc-mirror.pdf` | 1 218 917 | `8095c146e18963bbe745b141c23716030c3caf7ab08f149070b07c666130deb8` | 5 |

**Method note.** D1 validated as `%PDF` (`executed-success`) with an intact text
layer. §3 was read from a 200 dpi render of sheet 4; the text layer in that region
interleaves the labels of `Q4`, `D4`, `D5`, `D6`, `C67`, `C71`–`C73` and the
neighbouring translator, and cannot be untangled reliably. The topology was then
cross-checked against DKE's own reference circuit, which agrees.
