# 100K-RNTC — charger temperature thermistor (part **unidentified**)

> **100 kΩ NTC thermistor**, fitted as **`R15` on sheet 2** of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153). It is the temperature-qualification sensor for the [IP2315](../../injoinic/ip2315/README.md) battery charger — the part that is supposed to stop charging when it is too hot or too cold.
> Research snapshot **2026-09-01**. **Safety-relevant, and it carries a finding that contradicts other records in this repository:** [§4](#4--conflict-this-does-not-measure-the-cell).
> **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[SCH-V]** | Read off sheet 2 rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[IP]** | Injoinic IP2315 datasheet, held under the [IP2315 record](../../injoinic/ip2315/README.md) | `not-tested` |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Value string on the schematic | **`100K-RNTC`** | **[SCH-V]** |
| Reference designator | **`R15`**, sheet 2 | **[SCH-V]** |
| Function | **Negative-temperature-coefficient thermistor**, nominal **100 kΩ at 25 °C** | **[SCH-V]**, **[IP]** |
| Manufacturer | **unidentified** | — |
| Part number | **unidentified** | — |
| **B constant** | **not stated on the schematic**; the IP2315 datasheet's worked example uses **B = 4100** | **[IP]** |
| Package / case size | **not stated anywhere in the PDF** | — |
| Tolerance | **not stated** — every other resistor on the sheet is printed `/1%`; this one is not | **[SCH-V]** |

### 1.1 ⚠ `100K-RNTC` is a description, not a part number

It says: a **100 k**Ω **R**esistor that is an **NTC**. Nothing more. It names no
manufacturer, no series, no B constant, no tolerance and no package.

**No part number is guessed here.** For a component whose whole job is a safety
interlock, that gap is worth stating loudly rather than papering over.

**What would resolve it:**

1. **M5Stack's manufacturing BOM** — the only source that would give a series and
   a B constant directly.
2. **The B constant is the missing number that actually matters** (§3). If a
   board is available, it can be measured: read the resistance at two known
   temperatures and solve for B.
3. A photograph of the board would give the case size but almost certainly not a
   part number — NTC chips are rarely marked.

---

## 2. Used By

### `devices/m5stack/papermono` — `R15`, sheet 2

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md).
**One instance.**

**On the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md):**
`inferred` **yes**. The Lite drops only NFC and LoRa; the
[compatibility record](../../../devices/m5stack/papermono/compatibility-and-status.md)
states the charging arrangement and the 1150 mAh cell are identical on both SKUs.
Not read from the Lite's own schematic.

### 2.1 The sensing arrangement **[SCH-V]**

Read from a 200 dpi render of sheet 2. Four resistors sit in a row beneath the
IP2315's `LED3`, `ICHGSET` and `NTC` pins:

```
   IP2315 (U1, sheet 2)
   pin 10  LED3 ──────────────────────────┬─────── "NC" net label
   pin 27  ICHGSET ─────────────┬         │
   pin 26  NTC ──┬──────────┐   │         │
                 │          │   │         │
              R15 │       R16 │ R17 │   R18 │
           100K-RNTC     82 kΩ   15 kΩ   NC/1%
              (NTC)       1 %     1 %   not fitted
                 │          │      │       │
                 └──────────┴──────┴───────┴──── GND
```

| Ref | Value | From | To |
|---|---|---|---|
| **`R15`** | **`100K-RNTC`** | **`NTC` (pin 26)** | GND |
| **`R16`** | **82 kΩ / 1 %** | **`NTC` (pin 26)** — the same node | GND |
| `R17` | **15 kΩ / 1 %** | `ICHGSET` (pin 27) | GND |
| `R18` | `NC/1%` | `LED3` (pin 10) | GND — **not fitted** |

So **`R15` and `R16` are in parallel from the `NTC` pin to ground.** The IP2315
biases that pin internally and reads the resulting voltage.

`R16` = 82 kΩ in parallel is a **linearising resistor**: an NTC's resistance is
exponential in temperature, and a fixed parallel resistor flattens the curve over
the band of interest, trading sensitivity at the extremes for a more nearly
linear response across the charge-permitted window. **[INF]**

**This reproduces the IP2315 datasheet's own worked example verbatim** —
*"R<sub>NTC</sub> = 100 kΩ @ 25 °C (B = 4100), R2 = 82 kΩ"* **[IP]** — which is
strong evidence that M5Stack copied the reference design, and therefore that
**B = 4100** is the intended constant. It is `inferred`, not read from the
schematic.

### 2.2 What the charger does with it **[IP]**

The [IP2315 record](../../injoinic/ip2315/README.md) establishes that normal
charging is permitted between roughly **0 °C and 55 °C**, and the charger
suspends or reduces charging outside that window. That is the standard JEITA-style
temperature qualification and it is the whole reason this component exists.

### 2.3 A related resolution, from the same render

The same image settles a question the
[IP2315 record left open](../../injoinic/ip2315/README.md#4-2--the-ntc-and-ichgset-network):
it could not tell from the PDF text layer **which of `R17`/`R18` reaches
`ICHGSET`**.

**Answer: `R17` = 15 kΩ is on `ICHGSET`; `R18` = `NC` is on `LED3` and is not
fitted.** **[SCH-V]**

The conflict that record raises therefore stands and is now sharper: **15 kΩ is
not one of the four values the IP2315 datasheet tabulates for `ICHGSET`**
(51 k / 130 k / 180 k / NC), so the programmed charge current cannot be read off
the datasheet table at all. Sheet 1 annotates the charge current as
**`充电电流 0.5C`** ("charge current 0.5 C") — ≈ 575 mA for the 1150 mAh cell.
**[SCH-V]**

---

## 3. ⚠ The B constant is unknown, and that is the safety-relevant gap

An NTC is characterised by **two** numbers: its resistance at 25 °C, and its
**B constant** (the exponent governing how fast resistance falls with
temperature). The schematic gives the first and not the second.

**Fitting a 100 kΩ NTC with the wrong B constant produces a thermistor that reads
the right value at 25 °C and the wrong value everywhere else** — and "everywhere
else" is precisely the region the interlock exists to detect.

Worked illustration, at the trip points that matter:

| B | R at 0 °C | R at 55 °C | R at 60 °C |
|---:|---:|---:|---:|
| **3435** | ~330 kΩ | ~23 kΩ | ~20 kΩ |
| **4100** *(the reference-design value)* | ~380 kΩ | ~20 kΩ | ~17 kΩ |
| **4250** | ~395 kΩ | ~19 kΩ | ~16 kΩ |

**[INF]** — computed from the standard Beta relation
`R(T) = R25 · exp(B · (1/T − 1/298.15))`, not read from any datasheet.

A B = 3435 part substituted for a B = 4100 one reads about **20 kΩ at 55 °C where
the charger expects 20 kΩ at 60 °C** — i.e. it would **let charging continue
several degrees hotter than intended**. That is the wrong direction for a safety
device.

**Practical rules:**

- **Never substitute an NTC by its 25 °C value alone.** Match B as well.
- If this board is ever repaired, **use a 100 kΩ NTC with B = 4100** unless the
  real value is established, because that is what the charger's reference design
  assumes.
- Because both trip points are determined by the *combination* of `R15`, `R16`
  and the IP2315's internal thresholds, changing any one of them moves both
  limits.

---

## 4. ⚠ Conflict: this does **not** measure the cell

**This is the most consequential finding in this record, and it contradicts
wording elsewhere in this repository.**

Several places in the PaperMono record describe the battery as **"NTC-sensed"**
and place the thermistor **at the battery connector `J2`**:

| Where | Wording |
|---|---|
| [`README.md`](../../../devices/m5stack/papermono/README.md) | "Battery \| 1150 mAh Li-ion, **NTC-sensed**" |
| [`features/battery-and-charging.md`](../../../devices/m5stack/papermono/features/battery-and-charging.md) | "battery (**J2**, 1150 mAh **+ 100K NTC**)"; "Cell \| 1150 mAh Li-ion **at `J2`**, `100K-RNTC` thermistor" |
| [`pinouts-and-buses.md`](../../../devices/m5stack/papermono/pinouts-and-buses.md) | "`J2` … Battery, **with a `100K-RNTC` thermistor**" |

**The schematic does not support the thermistor being in the battery pack.**

| Claim | Evidence **[SCH-V]** |
|---|---|
| **`J2` has two pins only** | Rendered at 200 dpi, `J2` is a 2-contact symbol: pin 2 → `VBAT_L0`, pin 1 → GND, with `CON2_SMD` printed beneath as the footprint name and `C13` = 22 µF/10 V across it. **There is no third contact and no thermistor pin** |
| **`R15` is a mainboard part** | It carries a designator in sheet 2's `R` series, is placed beside the IP2315, and connects `NTC` (pin 26) to GND in parallel with `R16` (§2.1) |

So the arrangement is **a 100 kΩ NTC soldered to the mainboard on the charger's
`NTC` pin** — not a thermistor inside the cell reaching the board through the
connector.

**Two consequences, both `inferred`, both safety-relevant:**

1. **What is measured is board temperature near the charger, not cell
   temperature.** The two track loosely, and they diverge exactly when it
   matters — a cell entering thermal runaway heats far faster than the PCB
   beneath it, and the interlock would respond late or not at all. Conversely a
   warm charger IC could inhibit charging while the cell is fine.
2. **A replacement cell needs no thermistor.** Fitting a 3-wire pack would not
   improve the protection, because there is nowhere for the third wire to go.

**This conflict is recorded, not resolved.** It is entirely possible that M5Stack
places `R15` physically beneath or beside the cell so that it is thermally
coupled to it — that is a common and legitimate design when a pack has no NTC,
and nothing in a schematic can show it. **A board photograph or a thermal
measurement would settle it, and neither was available.**

**Suggested reading of the existing wording**, pending that: *"the charger has
NTC-based temperature qualification"* — which is true — rather than *"the battery
pack contains a thermistor"* — which this evidence does not support. Date
2026-09-01. Per the
[conflict protocol](../../../.agents/skills/hardware-device-research/SKILL.md),
the other records are **not** edited by this pass; they are linked and the
disagreement is stated.

See also the [battery record](../papermono-1150mah-liion-cell/README.md#5--the-thermistor-is-not-in-the-pack)
and the
[BOM §11](../../../devices/m5stack/papermono/bill-of-materials.md#11--conflict-raised-by-this-pass--the-ntc-does-not-measure-the-cell).

---

## 5. Substitution

| Requirement | Value |
|---|---|
| R at 25 °C | **100 kΩ** |
| **B constant** | **4100** (the IP2315 reference-design value) — §3 |
| Tolerance | unstated on the schematic; ±1 % B-tolerance parts are standard for charger sensing |
| Package | unstated; 0402 or 0603 chip NTC is the norm |

Widely available equivalents: Murata `NCP15XH103F03RC` (B = 3380 — **wrong B**),
`NCP15WB473` (47 kΩ), Vishay `NTCS0402E3104FXT` (100 kΩ, B = 4100 — **matches**),
Murata `NCU15XH103F6SRC`, TDK `NTCG103` series. **Check B, not just 100 kΩ.**

---

## 6. Integration pitfalls

1. **It is not a resistor.** A rework that fits an ordinary 100 kΩ chip resistor
   in `R15` produces a charger that believes the temperature is permanently 25 °C
   — i.e. **a silently disabled safety interlock**. Nothing in firmware would
   report it.
2. **B is unknown** (§3) and matters more than the nominal value.
3. **It probably does not measure the cell** (§4).
4. **`R15` and `R16` set the trip points jointly** (§2.1) — do not change one.
5. **The tolerance is not printed** while every neighbouring resistor's is
   (§1) — so the fitted grade is unknown.
6. **`R17` = 15 kΩ on `ICHGSET` is not a tabulated value** (§2.3), so the actual
   charge current cannot be derived from the datasheet either. Two of the
   charger's three programming resistors are therefore not fully understood.

---

## 7. Open questions

- **Manufacturer, part number, B constant, tolerance, package** (§1.1, §3).
- **Whether `R15` is thermally coupled to the cell** (§4) — the blocking question,
  answerable only with a board.
- What charge current 15 kΩ on `ICHGSET` actually programs (§2.3).
- The IP2315's internal `NTC` bias arrangement (current source? divider from an
  internal reference?), which determines how `R15`∥`R16` maps to a voltage. Not
  read from **[IP]** for this record.
- No measurement of anything.

---

## Manufacturer

**Unidentified** (§1.1). No vendor sourcing guide applies. **No search was made
for a part number**, because the schematic string carries no vendor-specific token
to search on — `100K-RNTC` would match every 100 kΩ NTC ever made. This is a
deliberate non-attempt rather than a failed one: the resolution path is a BOM or a
measurement (§1.1), not a catalogue query.

## Related pages

- [Injoinic IP2315](../../injoinic/ip2315/README.md) — **the charger that reads this thermistor**, and whose `R17`/`R18` question §2.3 answers
- [1150 mAh Li-ion cell](../papermono-1150mah-liion-cell/README.md) — what is *not* being measured (§4)
- [PaperMono battery and charging feature guide](../../../devices/m5stack/papermono/features/battery-and-charging.md)
- [PaperMono bill of materials §11](../../../devices/m5stack/papermono/bill-of-materials.md#11--conflict-raised-by-this-pass--the-ntc-does-not-measure-the-cell)
- [PaperMono power architecture](../../../devices/m5stack/papermono/power-architecture.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | `R15` = `100K-RNTC` on IP2315 pin 26; `R16` = 82 kΩ in parallel; **`R17` = 15 kΩ on `ICHGSET`, `R18` = `NC` on `LED3`**; **`J2` is 2-pin**; the `充电电流 0.5C` annotation | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| D1 | IP2315 datasheet | Injoinic | primary | see the [IP2315 record](../../injoinic/ip2315/README.md#manufacturer) | 2026-09-01 | V1.0 (cn), 16 pp | the `R_NTC = 100 kΩ @ 25 °C (B = 4100), R2 = 82 kΩ` worked example; the ~0–55 °C charge window; the `ICHGSET` value table | `../../injoinic/ip2315/artifacts/` |

**Local artifacts** — **none.** The part is unidentified (§1.1); there is no
document to hold. The circuit evidence lives in the schematic, which is held under
the device record.

**Method note.** Everything in §2.1 and §4 was read from a **200 dpi PNG render**
of schematic sheet 2, cropped to the `R15`–`R18` block and to `J2` respectively.
The text layer in the `R15`–`R18` region places all four values and all three pin
names in one horizontal band and cannot attribute them; an earlier text-only pass
left the `R17`/`R18` question open for exactly that reason.
