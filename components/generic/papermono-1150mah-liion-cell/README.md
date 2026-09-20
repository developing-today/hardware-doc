# PaperMono 1150 mAh Li-ion cell (maker and part **unidentified**)

> The **1150 mAh single-cell lithium-ion battery** shipped in the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) **and** the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md) (C153-Lite). It attaches at **`J2` on sheet 2** through a **2-pin** `CON2_SMD` connector.
> Research snapshot **2026-09-01**. **The cell's maker, model, dimensions and protection arrangement are not published.** What *is* established is the connector, the charge path and — contrary to other wording in this repository — that **the temperature sensor is not in the pack** ([§5](#5--the-thermistor-is-not-in-the-pack)).
> **No hardware was available. Nothing here was measured.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[SCH-V]** | Read off sheet 2 rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[SCH-T]** | Read from the schematic text layer | `executed-success` for the extraction |
| **[DOC]** | `docs.m5stack.com` PaperMono / PaperMono-Lite product pages, retrieved 2026-09-01 | `not-tested` |
| **[IP]** | Injoinic IP2315 datasheet, held under the [IP2315 record](../../injoinic/ip2315/README.md) | `not-tested` |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. What is established

| Property | Value | Evidence |
|---|---|---|
| **Capacity** | **1150 mAh** | **[DOC]** |
| Chemistry | Lithium-ion / lithium-polymer, **1S** | **[INF]** from the charger topology |
| Nominal voltage | **3.7 V** (1S Li-ion convention) | **[INF]** |
| Charge termination | **≈ 4.2 V** — the IP2315 is a 1S charger | **[IP]** |
| Rail name | **`VBAT_L0`** | **[SCH-V]** |
| **Connector** | **`J2`**, footprint **`CON2_SMD`**, **2 pins** | **[SCH-V]** |
| Pin 1 | **GND** (−) | **[SCH-V]** |
| Pin 2 | **`VBAT_L0`** (+) | **[SCH-V]** |
| Local decoupling | **`C13` = 22 µF/10 V** across the connector | **[SCH-V]** |
| Trace requirement | the schematic annotates **`20mil min`** on this net | **[SCH-V]** |
| Charge current | sheet 1 annotates **`充电电流 0.5C`** — "charge current 0.5 C", ≈ **575 mA** | **[SCH-T]** |
| **Same on both SKUs** | **yes — 1150 mAh on C153 and C153-Lite alike** | **[DOC]** |

### 1.1 What is **not** established

| Unknown | Why it matters |
|---|---|
| **Maker and model number** | No repair source; no way to match a replacement exactly |
| **Physical dimensions** | A replacement must fit the enclosure. The dimension code is not published |
| **Protection circuit (PCM/PCB) presence and thresholds** | §4 — this is the important one |
| **Connector polarity as wired to the pack** | §3 — this is the dangerous one |
| **Discharge C-rate and internal resistance** | Governs whether Wi-Fi TX bursts sag the rail |
| **Cycle life, cell vendor grade** | Governs long-term capacity retention |

**No part number is guessed.** M5Stack publishes a capacity and nothing else.

---

## 2. ⚠ Not the same cell as `components/generic/lipo-102035`

This repository already contains a record for an
**[LiPo 102035 battery](../lipo-102035/README.md)**. It is a **different cell for
a different board** and the two must not be conflated:

| | **This record** | [`lipo-102035`](../lipo-102035/README.md) |
|---|---|---|
| Device | **M5Stack PaperMono** (C153) and PaperMono-Lite | **Waveshare ESP32-S3-Knob-Touch-LCD-1.8** |
| Designation | none published | `102035` (a dimension code) |
| Capacity | **1150 mAh, stated by the vendor** | **unknown** — that record works with 500 mAh as an explicitly-labelled placeholder |
| Supplied with the device? | **yes, fitted** | **no** — an optional accessory |
| Connector | **`J2`, `CON2_SMD`, 2-pin, designator known** | designator not legible in the published sheets; **PH1.25 vs PH2.0 unresolved** |
| Charger | **[IP2315](../../injoinic/ip2315/README.md), identified** | **no charger IC identifiable in the published sheets** |

**They are cross-linked rather than merged**, because almost everything specific
differs. What the two records genuinely share is the *class* of problem — an
unidentified single-cell Li-ion behind an under-documented connector — and the
`lipo-102035` record's
[safety section](../lipo-102035/README.md#7-safety) and
[connector-polarity warning](../lipo-102035/README.md#3-connector--also-unresolved-and-this-one-is-dangerous)
apply here in full.

---

## 3. ⚠ Connector polarity — verify before connecting anything

The schematic establishes the **board side** unambiguously **[SCH-V]**:

```
        J2  "CON2_SMD"          20mil min
   ┌──────────┐
   │    2  ●──┼───────────────┬────── VBAT_L0   (+)
   │          │               │
   │    1  ●──┼───────────────┼─┬──── GND       (−)
   └──────────┘               │ │
      "Battery"           C13 22 µF/10 V
```

**Pin 2 is positive, pin 1 is negative.**

**It does not establish the pack side.** There is **no industry-wide polarity
convention for two-pin lithium-cell connectors** — some vendors wire red to pin 1
and some to pin 2, and the housings are mechanically identical either way.

> **Before connecting any replacement cell, check polarity with a meter against
> the board's own pin 1 / pin 2.** Reversed connection of a lithium cell into a
> charger input is a fire risk, not a "it does not work" outcome. This is the
> single highest-risk item on this page.

The connector's own part is also unidentified — `CON2_SMD` is a footprint name,
not an orderable part — so **the housing family (PH1.25, PH2.0, ZH1.5 or other)
is unknown**, and a replacement lead cannot be specified from this record.

---

## 4. ⚠ Protection: what the board does, and what it does not

**The board provides charge control. It does not provide cell protection.**

| Function | Provided by | Where |
|---|---|---|
| CC/CV charging to ~4.2 V | **[IP2315](../../injoinic/ip2315/README.md)** synchronous buck charger | `U1`, sheet 2 |
| Charge current programming | `R17` = 15 kΩ on `ICHGSET` | sheet 2 — ⚠ **not a datasheet-tabulated value**, see the [thermistor record §2.3](../100k-rntc-thermistor/README.md#23-a-related-resolution-from-the-same-render) |
| Temperature qualification | **[`100K-RNTC`](../100k-rntc-thermistor/README.md)** `R15` ∥ `R16` = 82 kΩ on the charger's `NTC` pin | sheet 2 — ⚠ **§5** |
| Input over-voltage | [AW32901FCR](../../awinic/aw32901/README.md), 5.95 V threshold | `U2`, sheet 2 |
| Battery voltage measurement | the [`Q1` CJ3439KDW gated divider](../../changjing/cj3439kdw/README.md#3-what-it-actually-switches-sch-v) → M5PM1 `BAT_ADC` | sheet 2 |
| **Over-discharge cut-off** | **not on the schematic** | — |
| **Over-current / short-circuit cut-off** | **not on the schematic** | — |
| **Cell over-voltage backstop** | **not on the schematic** | — |

The last three are the functions of a **pack-mounted protection circuit (PCM)**,
which single-cell pouch cells normally ship with, bonded to the tab and hidden
under the yellow tape. **Its presence here is `inferred`, not established** — a
2-pin connector is exactly what a PCM-protected pouch cell presents, and shipping
an unprotected cell in a consumer product would be unusual. But nothing in the
published evidence confirms it.

**Practical consequence:** if a replacement cell is fitted **without** a PCM, the
board will happily charge it and the ESP32-S3 will happily discharge it, with no
hardware backstop at either end. The M5PM1's low-voltage handling is a firmware
behaviour, not a protection circuit.

> **Only fit protected cells.** `inferred` reasoning, stated as a safety
> recommendation rather than a finding.

---

## 5. ⚠ The thermistor is **not** in the pack

**This contradicts wording in several other records in this repository, and it is
recorded as a conflict rather than silently corrected.**

The following places describe the battery as NTC-sensed and place the thermistor
at `J2`:

| Where | Wording |
|---|---|
| [`README.md`](../../../devices/m5stack/papermono/README.md) | "Battery \| 1150 mAh Li-ion, **NTC-sensed**" |
| [`features/battery-and-charging.md`](../../../devices/m5stack/papermono/features/battery-and-charging.md) | "battery (**J2**, 1150 mAh **+ 100K NTC**)"; "Cell \| 1150 mAh Li-ion **at `J2`**, `100K-RNTC` thermistor" |
| [`pinouts-and-buses.md`](../../../devices/m5stack/papermono/pinouts-and-buses.md) | "`J2` … Battery, **with a `100K-RNTC` thermistor**" |

**The schematic does not support that.** **[SCH-V]**

| Claim | Evidence |
|---|---|
| **`J2` has exactly two contacts** | Rendered at 200 dpi: a 2-pin symbol, pin 2 → `VBAT_L0`, pin 1 → GND, `CON2_SMD` beneath, `C13` across. **No third contact exists**, so no thermistor wire can reach the board |
| **`R15` is a mainboard component** | It carries a sheet-2 `R`-series designator, sits beside the IP2315, and connects the charger's `NTC` pin (26) to ground in parallel with `R16` |

So the temperature qualification measures **board temperature near the charger**,
not cell temperature. Two consequences, both `inferred`, both safety-relevant:

1. **A cell entering thermal runaway heats much faster than the PCB beneath it.**
   A board-mounted sensor responds late, or not at all, to the failure it exists
   to catch. Conversely, a warm charger could inhibit charging while the cell is
   perfectly cool.
2. **A replacement cell does not need a thermistor**, and a 3-wire pack would gain
   nothing — there is nowhere for the third wire to go.

**Unresolved, deliberately.** M5Stack may place `R15` physically under or beside
the cell so that it is thermally coupled — a legitimate design when the pack has
no NTC, and one that no schematic can show. **A board photograph or a thermal
measurement settles it; neither was available.**

Pending that, the accurate phrasing is *"the charger performs NTC-based
temperature qualification"* rather than *"the pack contains a thermistor"*.
Date 2026-09-01. Full detail in the
[thermistor record §4](../100k-rntc-thermistor/README.md#4--conflict-this-does-not-measure-the-cell)
and
[BOM §11](../../../devices/m5stack/papermono/bill-of-materials.md#11--conflict-raised-by-this-pass--the-ntc-does-not-measure-the-cell).

---

## 6. Charge current — 0.5 C, and one loose end

Sheet 1's block diagram annotates the charging block **`充电电流 0.5C`**
("charge current 0.5 C"). **[SCH-T]** At 1150 mAh that is **≈ 575 mA**, a
conservative and cell-friendly rate: a full charge from empty takes roughly
**2–2.5 hours** including the CV tail. **[INF]**

**But the programming resistor does not corroborate it.** `R17` = **15 kΩ** sits
on the IP2315's `ICHGSET` pin **[SCH-V]**, and **15 kΩ is not one of the four
values the IP2315 datasheet tabulates** (51 k / 130 k / 180 k / NC) **[IP]**. Of
those, 51 kΩ / 500 mA is the closest to 0.5 C.

**The conflict is unresolved.** Either the datasheet's table is not exhaustive,
or the resistor selects something the held datasheet version does not describe.
It is tracked in the
[IP2315 record](../../injoinic/ip2315/README.md#4-2--the-ntc-and-ichgset-network)
and this record does not resolve it. **Do not quote a charge current in
milliamps as established.**

Note also that the charger is **fed from 5 V only** — the
[USB-C CC resistors are plain 5.1 kΩ pulldowns and the IP2315's own CC pins are
depopulated](../typec-302-brp16sc08/README.md#32--the-cc-arrangement-a-plain-sink-and-no-usb-pd--twice-over) —
so no adapter can shorten the charge time.

---

## 7. Runtime — what can and cannot be said

**Nothing here is measured**, and no current figure for this board exists in any
source held. What *can* be said:

- **1150 mAh at 3.7 V ≈ 4.26 Wh.**
- Conversion losses are real: `VBAT_L0` feeds the
  [JW5712 buck](../../joulwatt/jw5712/README.md) to make `3V3_L2`, and several
  [SSP7615 LDOs](../ssp7615-33dfr/README.md) elsewhere. An 85–90 % end-to-end
  figure is the usual working assumption.
- The board's deep-sleep architecture is unusually thorough — five power levels,
  the [M5PM1](../../m5stack/m5pm1/README.md) able to unpower the ESP32-S3
  entirely, and a **[gated battery-sense divider](../../changjing/cj3439kdw/README.md#31-why-the-gate-exists-and-why-it-is-worth-1-kω--1-kω)**
  that exists purely to avoid ~1.85 mA of standing drain. That last detail is
  itself evidence that standby current was taken seriously.
- **Known standing drains identified by this pass:** ~4 µA through `R3` = 1 MΩ in
  the sense-divider gate, and up to 0.3–1.2 mA of reverse leakage through
  [`D2`](../../rohm/rb162vam-20tr/README.md#12--the-reverse-leakage-is-large-and-it-is-a-standby-current-term)
  *if* the frontlight rail is biased. Neither dominates on its own.

**Refusing a runtime estimate is the honest position.** See
[`features/battery-and-charging.md`](../../../devices/m5stack/papermono/features/battery-and-charging.md)
for what the device record says.

---

## 8. Used By

### `devices/m5stack/papermono` — at `J2`, sheet 2

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md).
Fitted as shipped.

### `devices/m5stack/papermono-lite`

→ [M5Stack PaperMono-Lite (C153-Lite)](../../../devices/m5stack/papermono-lite/README.md).
**The same 1150 mAh cell** — explicitly, on both product pages, and noted in the
[compatibility record](../../../devices/m5stack/papermono/compatibility-and-status.md):
*"including the 1150 mAh battery — the Lite does not get a smaller cell."*
**[DOC]** The Lite's schematic is published only as a 4-sheet `PRJ` PDF, so its
`J2` wiring was **not** read directly; the connector is `inferred` to be the same.

---

## 9. Safety

In priority order. Most of this applies to any single-cell lithium device; the
first two are specific to what this record establishes.

1. **Verify connector polarity with a meter before first connection** (§3). Pin 2
   is positive on the board side; the pack side is unknown.
2. **Fit only protected cells** (§4). The board provides no over-discharge,
   over-current or backstop over-voltage protection.
3. **Do not assume the temperature interlock is watching the cell** (§5).
4. **Match capacity and physical size conservatively.** A larger cell in the same
   space is a mechanical hazard; a swollen or compressed pouch cell is a fire
   risk. The enclosure's internal dimensions are not published.
5. **Never charge a visibly swollen, punctured or previously over-discharged
   cell.**
6. **Charge at 0.5 C or less** if the cell's own rating is unknown (§6).

---

## 10. Open questions

- **Maker, model, dimensions** (§1.1).
- **Whether the pack contains a PCM, and its thresholds** (§4).
- **The pack-side connector polarity and housing family** (§3).
- **Whether `R15` is thermally coupled to the cell** (§5) — the blocking question
  for the safety argument.
- **What charge current `R17` = 15 kΩ actually programs** (§6).
- Internal resistance and discharge C-rate — determines rail sag during Wi-Fi TX.
- No measurement of anything: no capacity test, no current draw, no runtime.

---

## Manufacturer

**Unidentified.** M5Stack publishes the capacity and nothing further; no cell
vendor, model or dimension code appears on any product page, in the schematic, or
in the module-size drawing held at
`scratch/m5stack-papermono/pdf/C153_PaperMono_model_size.pdf`. **No search for a
part number was attempted**, because there is no vendor-specific token to search
on — the resolution path is a photograph of the cell's own label, or M5Stack's
BOM, not a catalogue query.

## Related pages

- [`100K-RNTC` thermistor](../100k-rntc-thermistor/README.md) — the temperature sensor, and the §5 conflict in full
- [Injoinic IP2315](../../injoinic/ip2315/README.md) — the charger
- [Awinic AW32901FCR](../../awinic/aw32901/README.md) — input OVP ahead of the charger
- [Changjing CJ3439KDW](../../changjing/cj3439kdw/README.md) — the gated divider that measures this cell
- [Shikues SK2301AAT](../sk2301aat/README.md) — the USB-gated `VBAT_DET` tap
- [XUNPU TYPEC-302-BRP16SC08](../typec-302-brp16sc08/README.md) — why charging is 5 V-only
- [LiPo 102035](../lipo-102035/README.md) — a **different** cell on a **different** board (§2)
- [M5Stack M5PM1](../../m5stack/m5pm1/README.md) — the power manager that owns battery measurement
- [PaperMono battery and charging feature guide](../../../devices/m5stack/papermono/features/battery-and-charging.md) · [power architecture](../../../devices/m5stack/papermono/power-architecture.md) · [bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | **`J2` is 2-pin**, `CON2_SMD`, pin 2 = `VBAT_L0`, pin 1 = GND, `C13` = 22 µF/10 V, `20mil min`; `R15`/`R16`/`R17` placement; the `充电电流 0.5C` annotation | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| W1 | PaperMono product page | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | — | **1150 mAh** | `../../../scratch/m5stack-papermono/docs/pages/` |
| W2 | PaperMono-Lite product page | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono%20Lite> | 2026-09-01 | — | **1150 mAh on the Lite too** | `../../../scratch/m5stack-papermono/docs/pages/` |
| D1 | IP2315 datasheet | Injoinic | primary | see the [IP2315 record](../../injoinic/ip2315/README.md#manufacturer) | 2026-09-01 | V1.0 (cn), 16 pp | 1S CC/CV charging; the `ICHGSET` value table that 15 kΩ is absent from; the NTC worked example | `../../injoinic/ip2315/artifacts/` |

**Local artifacts** — **none.** The cell is unidentified; there is no datasheet to
hold, and this is a recorded negative result rather than an unattempted one.

**Method note.** The `J2` pin count in §3 and §5 — the load-bearing observation in
this record — was read from a **200 dpi PNG render** of schematic sheet 2 cropped
to the connector. The text layer around `J2` mixes the connector's labels with
`U4`, `C14`, `C15`, `Q2`, `Q5` and `R9`, and an earlier text-only pass could not
have established the pin count from it.
