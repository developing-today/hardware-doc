# M5Stack PaperMono — bill of materials

> A **290-component, 230-designator census** recovered from
> [`PaperMono_SCH_V0.6.2_20260522.pdf`](artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf),
> the only schematic M5Stack publishes for the [PaperMono](README.md) (SKU C153).
> Research snapshot **2026-09-01**. **No hardware was in the loop** and this is
> **not a vendor BOM** — see [§2, Method and its limits](#2-method-and-its-limits)
> before using any quantity or value here for procurement.

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[SCH-M]** | Recovered from the Altium PDF's invisible `CO`/`PI` marker layer, then **checked against a rendered page image** | `executed-success` for the extraction |
| **[SCH-T]** | Read from the PDF text layer *only* (adjacency to a symbol), **not** confirmed against a rendered image | `executed-success` for the extraction; the *attribution to a designator* is `inferred` |
| **[SCH-V]** | Read directly off a page rendered to PNG at 200 dpi and inspected as an image | `executed-success` |
| **[DS]** | A component datasheet held under that component's `artifacts/` | `not-tested` |
| **[INF]** | Inference, flagged as such | `inferred` |

Nothing here is `reported-working`: no PaperMono was measured, probed or powered.

---

## 1. Headline counts

| Quantity | Value |
|---|---:|
| **Placed components** (sheet-scoped instances) | **290** |
| **Distinct reference-designator strings** | **230** |
| Sheets carrying components | 5 of 6 (sheet 1 is a block diagram and carries none) |
| Separate Altium documents concatenated into the PDF | **3** |
| Components with a component record in this repository | **56** |
| Components deliberately left without a record (ordinary passives) | **221** |
| Components **unidentified** after searching | **13** |

Per sheet:

| Sheet | Document | Placed components |
|---:|---|---:|
| 1 | main project — architecture/block diagram, power-state table | **0** |
| 2 | main project — USB-C, protection, charger, rails, frontlight boost | **93** |
| 3 | main project — ESP32-S3, flash, RF front end, test points | **52** |
| 4 | main project — RTC, IMU, buzzer, NFC/LoRa interfaces, TP, EPD, microSD | **79** |
| 5 | `PaperMono KEY RGB.SchDoc` — keys, RGB LED, PDM microphone | **23** |
| 6 | `02 Paper Mono NFC.SchDoc` — ST25R3916 NFC front end | **43** |

---

## 2. Method and its limits

**Read this before quoting a number from this page.**

The census comes from the **Altium `CO` (component-outline) marker layer** that
Altium Designer's PDF publisher embeds as invisible text at every placed symbol.
That has three consequences that a reader must hold onto:

1. **It captures placed symbols, not a purchased BOM.** A `CO` marker says "a
   symbol with this designator sits here". It says nothing about whether the pad
   is populated at assembly. Parts whose value string reads `NC` are *drawn* and
   *counted* here but are **not fitted** — there are **11** of them (§8).
   Conversely, anything M5Stack fits that has no schematic symbol (test coupons,
   shield cans, the LoRa module's own internals) is invisible to this method.

2. **Values come from text adjacency, not from a parsed netlist.** Altium writes
   the designator and the value as two ordinary text objects near the symbol.
   Pairing them is a nearest-neighbour guess. It is right the overwhelming
   majority of the time and it is *wrong* where symbols are packed tightly —
   which on this schematic means the charger block on sheet 2 and the microSD
   block on sheet 4. Every value in this document that is load-bearing for a
   component record was re-read from a **rendered page image** and is marked
   **[SCH-V]**; the rest are **[SCH-T]** and should be treated as good but
   unconfirmed.

3. **Tolerances and dielectrics are only as good as the string.** `100nF/25V`
   tells you capacitance and voltage. It does not tell you X5R vs X7R, case size,
   or the DC-bias derating that actually determines whether a 22 µF/10 V 0603 is
   4 µF at 4.2 V. **No case sizes appear anywhere in this PDF.** Resistor
   tolerance is uniformly printed `/1%`; capacitor tolerance is never printed.

### 2.1 ⚠ Two parser artefacts had to be repaired — and one of them refutes a claim

`tools/altium_pdf_netlist.py` matches a marker prefix (`CO`, `PI`, `NL`) anywhere
in a word not preceded by a letter. Its docstring already warns that `GPIO0`
parses as `G` + `PI`-marker `O0`, and guards that with a negative lookbehind. The
guard does **not** cover ordinary schematic text that *begins* with those letters,
and this schematic contains two such strings:

| Raw word in the PDF | Where | Mis-read as | Reality |
|---|---|---|---|
| `CON2_SMD` | sheet 2, at `J2` | a component **`N2`** | the battery connector's **footprint label** **[SCH-V]** |
| `PIN1` … `PIN24` (24 words) | sheet 4, at `J5` | pin markers **`N1` … `N24`** | the FPC symbol's **pin-name labels** **[SCH-V]** |

> ⚠ **There is no `N`-series on this board, so "`N1` is missing" is not a finding.**
> An earlier reading of this census recorded `N1` as a gap alongside the five
> missing resistors. It is not a gap: **`N1` never existed, and neither did `N2`.**
> The battery connector is `J2` and nothing else. Confirmed by rendering sheet 2
> at 200 dpi and reading the symbol, which shows a 2-pin connector labelled `J2`
> with `CON2_SMD` printed beneath it as the footprint name. Date 2026-09-01.

### The second defect: a designator with no digits disappears

`designators()` keeps only marker bodies matching `[A-Z]+[0-9]+`. **A designator
with no number is silently dropped.** This board has one:

| Marker | Where | Pin markers | Reality |
|---|---|---|---|
| **`COUSB`** | sheet 2 | **16 × `PIUSB01`…`PIUSB016`** | the **USB-C receptacle**, designated **`USB`** |
| `CORE` | sheet 1 | **none** | the block-diagram word **"CORE"** — a phantom, like `CON2_SMD` |

The pin markers are what separate the two: a real component's outline marker is
accompanied by pin markers, and 16 of them is exactly a 16-contact USB-C
receptacle. `CORE` has none, and sheet 1 genuinely carries no components.

> ⚠ **The USB-C receptacle's reference designator is `USB`, not `U1`.** An
> earlier reading of this census recorded it as a second `U1` on sheet 2 —
> because `TYPEC-302-BRP16SC08` sits above the symbol and `USB` below it, and the
> IP2315's `U1` is the nearest designator-shaped string. **Refuted** by the
> marker layer: sheet 2 contains exactly one `CO` marker with body `U1` (the
> IP2315, whose adjacent text is `CC1 / NC/1% / CC2 / DM`) and one with body
> `USB`. **Sheet 2 has one `U1`, not two.** Date 2026-09-01.

### The third defect: eight clipped markers on sheet 6

**On sheet 6 only**, `pdftotext` drops the leading glyph of eight `CO` markers:

```
x=506.50 'PIC1802'   x=511.00 'COC18'   x=512.30 'C18'    <- intact
x=463.50 'PIC1602'   x=467.64  'OC16'   x=469.14 'C16'    <- leading C dropped
```

Eight capacitors — `C1`, `C16`, `C17`, `C19`, `C21`, `C24`, `C25`, `C27` — were
therefore missing from the raw census. **They are placed parts, not gaps.** With
them restored, sheet 6 holds 43 components and its `C` series runs `C1`–`C31`
unbroken.

This is the [method's own warning](../../../.agents/skills/hardware-device-research/SKILL.md)
about trusting a text layer, landing **three times** on one document. The corrected census
is produced by [`scratch/m5stack-papermono/tools/census.py`](../../../scratch/m5stack-papermono/tools/census.py),
which repairs both defects and prints the gap analysis below. **[SCH-M]**

---

## 3. ⚠ Designators repeat across sheets — a designator alone is meaningless

The published PDF is **three separate Altium documents printed back to back**,
not one six-sheet project. Each document numbers its designators from 1.

| Sheets | Document | Evidence |
|---|---|---|
| 1–4 | the main project | continuous numbering `C1`–`C85`, `U1`–`U21`, `R1`–`R68` across the four sheets |
| 5 | `PaperMono KEY RGB.SchDoc` | title block, sheet 5: `File: Y:\AD.Prj\..\PaperMono KEY RGB.SchDoc`, dated **2026-04-14** **[SCH-T]** |
| 6 | `02 Paper Mono NFC.SchDoc` | title block, sheet 6: `File: Y:\AD.Prj\..\02 Paper Mono NFC.SchDoc`, `Paper Mono NFC`, `2/2`, `V0.2`, dated **2026-07-28** **[SCH-T]** |

So the same string names different parts:

| Designator | Sheet 2 (main) | Sheet 5 (KEY/RGB) | Sheet 6 (NFC) |
|---|---|---|---|
| **`U1`** | [Injoinic IP2315](../../../components/injoinic/ip2315/README.md) charger — **and nothing else; the receptacle is `USB`** | [LMD4737T261-AC02](../../../components/generic/lmd4737t261-ac02-pdm-microphone/README.md) PDM microphone | [AW35122FDR](../../../components/awinic/aw35122/README.md) load switch |
| **`J1`** | frontlight connector, 6-pin | [`AXE612124D`](../../../components/panasonic/axe612124d/README.md) board-to-board | [`BTB0.408-10PLBDR-G41`](../../../components/generic/btb0.408-10plbdr-g41/README.md) board-to-board |
| **`LED1`** | charger status LED net | [RS-C1415MBAR](../../../components/generic/rs-c1415mbar-rgb-led/README.md) RGB LED | — |
| **`C1`** | 100 nF/25 V | 100 nF/10 V | 10 nF |
| **`R1`** | `NC/1%` (IP2315 `CC1`) | 10 kΩ (power-button pull-up) | 0 Ω (NFC 3V3 link) |
| **`L1`** | `FTC252012S2R2MBCA` 2.2 µH | 2 nH | 270 nH ±5% |

and there are three different `U1`s, two `X1`s, two `ANT1`s and two `LED1`s.

> **Cite every part as `<designator> sheet <n>`.** "`U1`" is ambiguous;
> "`U1` sheet 2" is not. Every row in this document does so, and so should any
> record, issue report or firmware comment that refers to this board.

---

## 4. ⚠ Gaps in the designator sequence — what is and is not evidence

Enumerating the *complete* set per document, rather than searching for the parts
one expects, is what makes a gap meaningful. The corrected census finds gaps in
**exactly one** prefix, in **exactly one** document:

| Document | Prefix | Present | Highest | **Gaps** |
|---|---|---:|---|---|
| main (2–4) | `R` | 63 | `R68` | **`R46`, `R48`, `R55`, `R56`, `R57`** |
| main (2–4) | `C` `U` `D` `L` `Q` `J` `TP` `TVS` `ANT` `BUZZER` `FT` `LED` `X` | — | — | none |
| KEY RGB (5) | all | — | — | none |
| NFC (6) | all | — | — | none |

**Verification of the five.** `R46`, `R48`, `R55`, `R56` and `R57` appear
**nowhere in the PDF** — not as a `CO` marker, not as a `PI` marker, not as
visible text, on any of the six sheets. This was tested by scanning every
extracted word on every page for those literals, not by looking where they were
expected. **[SCH-M]**

**What the gaps most likely mean.** Honestly: the most probable explanation is
the dullest one.

- **Most likely — parts deleted during design.** All five sit inside `R42`–`R68`,
  which is the *sheet 4* resistor block. Sheet 4 is present and complete; its
  other 22 resistors are all there. A gap inside a range whose sheet is published
  means the symbol was placed and later removed, and Altium does not renumber on
  delete. `R55`–`R57` being three *consecutive* numbers is the signature of one
  small sub-circuit being taken out in a single edit. **[INF]**
- **Possible — annotation churn.** A re-annotation pass that renumbered some
  parts can leave holes without anything having been deleted. Indistinguishable
  from the above without the source project. **[INF]**
- **Unlikely here — an unpublished sheet.** This is the explanation the method
  warns to look for, and it is the right one elsewhere in this device's record:
  the NFC document announces itself as sheet **`2/2`**, so **NFC sheet 1 of 2 is
  genuinely unpublished** (see [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
  R8). But a missing sheet would take a *contiguous block* of designators with
  it, across several prefixes at once. Five scattered resistors and no missing
  `C`, `U`, `D` or `Q` is not that pattern. **[INF]**

**What cannot be concluded.** Nothing here establishes what the deleted parts
*were*. Do not infer a depopulated feature from them. Resolving this needs the
Altium source project or a photographed bare PCB showing unpopulated pads — the
schematic alone cannot answer it.

---

## 5. Sheet 2 — USB-C input, protection, charging, rails, frontlight boost (92)

### 5.1 Integrated circuits and actives

| Ref | Part | Function | Record |
|---|---|---|---|
| `U1` | `IP2315` | 1S Li-ion synchronous buck charger, I²C `0x75`, **gated off the bus** | [injoinic/ip2315](../../../components/injoinic/ip2315/README.md) |
| `U2` | `AW32901FCR` | USB-input OVP load switch, 5.95 V threshold | [awinic/aw32901](../../../components/awinic/aw32901/README.md) |
| `U3` | `AW39112DNR` | 2-bit level translator — the charger's I²C gate | [awinic/aw39112](../../../components/awinic/aw39112/README.md) |
| `U4` | `SSP7615-33DFR` | 3.3 V/400 mA LDO → `3V3_L0` (always-on rail) | [generic/ssp7615-33dfr](../../../components/generic/ssp7615-33dfr/README.md) |
| `U5` | `SSP7615-33DFR` | 3.3 V LDO → `EPD_3V3_L3` | idem |
| `U6` | `SSP7615-33DFR` | 3.3 V LDO → `3V3_L1` | idem |
| `U7` | `M5PM1` | power-management coprocessor, I²C `0x6E` (Puya PY32L020F15U6 inside) | [m5stack/m5pm1](../../../components/m5stack/m5pm1/README.md) |
| `U8` | `AW35122FDR` | 1.5 A load switch → `TF_3V3_L3` (microSD) | [awinic/aw35122](../../../components/awinic/aw35122/README.md) |
| `U9` | `SSP7615-33DFR` | 3.3 V LDO → `3V3_L2_LoRa` | [generic/ssp7615-33dfr](../../../components/generic/ssp7615-33dfr/README.md) |
| `U10` | `JW5712` | 600 mA buck → `3V3_L2`, the main system rail | [joulwatt/jw5712](../../../components/joulwatt/jw5712/README.md) |
| `U11` | `AW9967DNR` | boost WLED driver — the e-paper frontlight, `BL_15V_L3B` | [awinic/aw9967](../../../components/awinic/aw9967/README.md) |

### 5.2 Discrete semiconductors

| Ref | Part | Circuit role | Record |
|---|---|---|---|
| `D1` | `DSK34` | Schottky at the IP2315 `LX`/`DM` node **[SCH-T]** — role not confirmed visually | **unidentified**, §9 |
| `D2` | `RB162VAM-20TR` | **frontlight boost rectifier**: `L3` → `D2` → `R27` → `BL_15V_L3B` **[SCH-V]** | [rohm/rb162vam-20tr](../../../components/rohm/rb162vam-20tr/README.md) |
| `Q1` | `CJ3439KDW` | **complementary N+P pair — the gated battery-sense divider.** `Q1A` (N) gate = `BAT_ADC_EN`; its drain pulls `Q1B` (P) gate low through `R3` = 1 MΩ; `Q1B` connects `VBAT_L0` to the `R5`/`R12` 1 kΩ + 1 kΩ divider feeding `BAT_ADC` **[SCH-V]** | [changjing/cj3439kdw](../../../components/changjing/cj3439kdw/README.md) |
| `Q2` | `SK2302AAT` | N-channel; gate = `VUSB_IN`, source = GND, drain = `Q5` gate. **USB-presence detector** **[SCH-V]** | [generic/sk2302aat](../../../components/generic/sk2302aat/README.md) |
| `Q5` | `SK2301AAT` | P-channel high side; source = `VBAT_L0`, drain = `VBAT_DET`, gate held up by `R45` = 100 kΩ. **Connects the battery to `VBAT_DET` only while USB is present** **[SCH-V]** | [generic/sk2301aat](../../../components/generic/sk2301aat/README.md) |
| `TVS1` | `ESD5311` | ESD clamp on **`USB_N`** **[SCH-V]** | [generic/esd5311](../../../components/generic/esd5311/README.md) |
| `TVS2` | `ESD5311` | ESD clamp on **`USB_P`** **[SCH-V]** | idem |
| `LED1` | — | charger status LED on the IP2315 `LED1/SCL` net **[SCH-T]** | **unidentified**, §9 |

### 5.3 Connectors

| Ref | Part | Pins | Carries | Record |
|---|---|---:|---|---|
| **`USB`** | `TYPEC-302-BRP16SC08` | 16 | USB-C receptacle: `VBUS`, `GND`, `CC1`, `CC2`, `DP1/DP2`, `DN1/DN2`, `SBU1/SBU2`, 4× shell | [generic/typec-302-brp16sc08](../../../components/generic/typec-302-brp16sc08/README.md) |
| `J1` | — | 6 | frontlight: `BL_15V_L3B`, `BL_FB`, `PYG3_BL_PWM` | **unidentified**, §9 |
| `J2` | `CON2_SMD` | 2 | **battery only** — pin 2 `VBAT_L0`, pin 1 GND, `C13` = 22 µF/10 V across **[SCH-V]** | [generic/papermono-1150mah-liion-cell](../../../components/generic/papermono-1150mah-liion-cell/README.md) |

> **The USB-C receptacle's designator is the bare string `USB`** — no number.
> That is legal in Altium and unusual in practice, and it is why a naive census
> misses the part entirely (§2.1). Its symbol carries `TYPEC-302-BRP16SC08` above
> and `USB` below; the IP2315's carries `IP2315（无后缀）`. **[SCH-V]**
>
> ⚠ [`pinouts-and-buses.md`](pinouts-and-buses.md) lists this connector as
> "`U1` (sheet 2)". That is the mis-attribution described in §2.1; the designator
> is `USB`. Not corrected there by this pass — recorded here. Date 2026-09-01.

### 5.4 Inductors — no records, and why

Per the method, ordinary passives get a record only where they affect firmware,
signal integrity, calibration, safety or a published interface. These are
switching-converter magnetics: the converter's record already documents the
topology, and the inductor value is a design parameter of that converter rather
than an independent interface. **No records were created.**

| Ref | Part | Value | Circuit role |
|---|---|---|---|
| `L1` | `FTC252012S2R2MBCA` | 2.2 µH | **IP2315 buck output inductor** — `LX` (pins 11–14) → `VBAT_L0` **[SCH-T]** |
| `L2` | `FTC201610S2R2MBCA` | 2.2 µH | **JW5712 buck output inductor** — `SW` → `3V3_L2` **[SCH-V]** |
| `L3` | `FTC201610S100MBCA` | 10 µH | **AW9967 boost inductor** — `EPD_3V3_L3` → `SW`, then `D2` → `BL_15V_L3B` **[SCH-V]** |

`FTC` and `SPH` are shielded-power-inductor series codes; the numeric field
encodes case size and inductance (`201610` = 2.0 × 1.6 × 1.0 mm, `S100` = 10 µH,
`S2R2` = 2.2 µH). No manufacturer is printed on the schematic and none was
established. **[INF]**

### 5.5 Passives — no records

**38 capacitors** `C1`–`C38` and **31 resistors** (`R1`–`R29`, `R45`). Values
**[SCH-T]** unless marked.

| Ref | Value | Where it sits |
|---|---|---|
| `C1` | 100 nF/25 V | `VUSB_IN` local decoupling |
| `C2`, `C3` | 22 µF/10 V ×2 | `VBAT_L0` bulk at the charger output |
| `C4` | 100 nF/25 V | `VBAT_DET` |
| `C5` | 1 µF/25 V | IP2315 `nACOK` area |
| `C6` | 1 µF/25 V | IP2315 `OVLO` area |
| `C7` | 100 nF/25 V | **`BAT_ADC` filter**, with `R5`/`R12` **[SCH-V]** |
| `C8`–`C11` | 22 µF/10 V ×4 | `VSYS` bulk |
| `C12` | 100 nF/25 V | `5VIN_ADC` filter |
| `C13` | 22 µF/10 V | **across the battery connector `J2`** **[SCH-V]** |
| `C14`, `C15` | 10 µF/10 V ×2 | `U4` LDO in/out (`3V3_L0`) |
| `C16`, `C17` | 10 µF/10 V ×2 | `U5` LDO in/out (`EPD_3V3_L3`) |
| `C18`, `C19` | 10 µF/10 V ×2 | `U6` LDO in/out (`3V3_L1`) |
| `C20`, `C21` | 10 µF/10 V ×2 | `U8` load-switch in/out (`TF_3V3_L3`) |
| `C22`, `C23` | 10 µF/10 V ×2 | `U9` LDO in/out (`3V3_L2_LoRa`) |
| `C24` | **33 pF/50 V** | AW9967 boost output snubber/feedforward **[SCH-V]** |
| `C25` | **1 µF/50 V** | **the frontlight rail's only real output capacitor** **[SCH-V]** |
| `C26` | **`NC/50V`** | frontlight output — **not fitted** **[SCH-V]** |
| `C27`–`C29` | 10 µF/10 V ×3 | `3V3_L2` bulk |
| `C30`–`C32` | 22 µF/10 V ×3 | `VBUS_L0` bulk |
| `C33` | 1 nF/50 V | `VBUS_L0` HF bypass |
| `C34`–`C36` | 22 µF/10 V ×3 | JW5712 input bulk |
| `C37` | 100 nF/25 V | M5PM1 `VCC` decoupling |
| `C38` | 10 µF/10 V | M5PM1 `VCC` bulk |
| `R1`, `R2` | **`NC/1%`** | **IP2315 `CC1`/`CC2` series — not fitted; this is why there is no USB-PD** **[SCH-V]** |
| `R3` | 1 MΩ | `Q1B` gate pull-up to `VBAT_L0` **[SCH-V]** |
| **`R4`** | **5.1 kΩ** | **USB-C `CC1` pulldown (Rd)** **[SCH-V]** |
| `R5`, `R12` | 1 kΩ, 1 kΩ | **`BAT_ADC` divider — 2:1** **[SCH-V]** |
| `R6` | `NC/1%` | IP2315 `nACOK` — not fitted |
| `R7` | 10 kΩ | IP2315 `VSYS`/`OVLO` area |
| `R8`, `R13` | `NC` | charger I²C `CHG_SYS_SCL`/`SDA` series — **not fitted** |
| `R9` | 100 kΩ | `Q2` gate pulldown **[SCH-V]** |
| `R10` | `0R/1%` | IP2315 `OVLO` link |
| `R11` | 100 kΩ | `Q1A` gate pulldown on `BAT_ADC_EN` **[SCH-V]** |
| **`R14`** | **5.1 kΩ** | **USB-C `CC2` pulldown (Rd)** **[SCH-V]** |
| `R15` | **`100K-RNTC`** | **NTC thermistor on IP2315 `NTC` (pin 26) → GND** **[SCH-V]** |
| `R16` | 82 kΩ | **parallel/linearising resistor on the same `NTC` node** **[SCH-V]** |
| `R17` | **15 kΩ** | **IP2315 `ICHGSET` (pin 27) → GND — the charge-current programming resistor** **[SCH-V]** |
| `R18` | `NC/1%` | IP2315 `LED3` (pin 10) → GND — **not fitted** **[SCH-V]** |
| `R19`, `R21` | 10 kΩ, 10 kΩ | `5VIN_ADC` divider |
| `R20` | `0R/1%` | `VBUS_L0`/`VBAT_L0` link |
| `R22` | 100 kΩ | `PYB_CHG_IIC` / `U3` `OE` |
| `R23`, `R24`, `R26`, `R28` | 1 MΩ ×4 | LDO / load-switch `EN` pulldowns (`U5`, `U6`, `U9`, `U10`) |
| `R25` | `NC/1%` | `U8` `EN` — not fitted |
| `R27` | `0R/1%` | link between the boost output and `BL_15V_L3B` **[SCH-V]** |
| `R29` | 18 Ω | **AW9967 `BL_FB` current-set resistor** |
| `R45` | 100 kΩ | `Q5` gate pull-up to `VBAT_L0` **[SCH-V]** |

> ⚠ **`R17` = 15 kΩ resolves an open question in the
> [IP2315 record](../../../components/injoinic/ip2315/README.md#4-2--the-ntc-and-ichgset-network).**
> That record could not tell from the text layer which of `R17`/`R18` reached
> `ICHGSET`. Rendering the block at 200 dpi settles it: **`R17` is on `ICHGSET`,
> `R18` is on `LED3` and is not fitted.** The conflict the record raises stands
> and is now sharper — **15 kΩ is not one of the four values the IP2315 datasheet
> tabulates for `ICHGSET`** (51 k / 130 k / 180 k / NC), so the programmed charge
> current cannot be read off the datasheet table at all. Sheet 1 annotates
> `充电电流 0.5C` ("charge current 0.5 C"), ≈ 575 mA for the 1150 mAh cell.
> **[SCH-V]** + **[INF]**

---

## 6. Sheet 3 — application processor, flash, RF front end, test points (52)

### 6.1 Integrated circuits

| Ref | Part | Function | Record |
|---|---|---|---|
| `U12` | `ESP32-S3R8` | application SoC, 8 MB in-package octal PSRAM | [espressif/esp32-s3r8](../../../components/espressif/esp32-s3r8/README.md) |
| `U13` | `XM25UH128DHIQT` | 128 Mbit (16 MB) SPI NOR flash | [xmc/xm25uh128dhiqt](../../../components/xmc/xm25uh128dhiqt/README.md) |
| `X1` | `CN4040M000157A530001` | 40 MHz crystal, ESP32-S3 main oscillator | [generic/cn4040m000157a530001-40mhz-crystal](../../../components/generic/cn4040m000157a530001-40mhz-crystal/README.md) |
| `FT1` | `ICMF062P900MFR` | **USB common-mode choke** on `USB_N`/`USB_P` before the S3 | **unidentified**, §9 |
| `ANT1` | — | 2.4 GHz antenna, fed through `L5` (0 Ω) and the `L4`/`C41`/`C42` match | **unidentified**, §9 |

### 6.2 RF match and crystal load — no records

| Ref | Part / value | Circuit role |
|---|---|---|
| `L4` | `LQP03TN2N6B02D` | **RF matching series inductor** (Murata LQP03TN 0201 thin-film, `2N6` = 2.6 nH). The schematic *also* prints `2nH` beside this group; the two strings disagree and the discrepancy is not resolved **[SCH-T]** |
| `L5` | `0R/1%` | link between `ANT1` and the match — a 50 Ω pass-through / measurement break |
| `L6` | `2nH` | RF match shunt, marked `50Ω` |
| `L7` | `24nH` | crystal-network inductor at `XTAL_P`/`XTAL_N` |
| `C39`, `C40` | `GRM0335C1H2R0BA01D` (2.0 pF), `GRM0335C1H1R8BA01D` (1.8 pF) | **Murata GRM0335 0201 C0G RF capacitors** in the antenna match |
| `C41`, `C42` | **`NC(TBD)`** | **match tuning positions, deliberately left open and marked "to be determined"** — the clearest statement in the document that the antenna match was still being characterised at V0.6.2 **[SCH-T]** |
| `C45`, `C50` | 24 pF ×2 | 40 MHz crystal load capacitors |

No records: these are the RF matching network and the crystal load. The match is
a board-level property documented in the device's RF section, not a component
interface; the caps are commodity C0G parts whose only relevant property (value)
is already stated. The **`NC(TBD)`** positions are the interesting part and they
belong to the board, not to a component.

### 6.3 Passives and test points — no records

**19 capacitors** `C43`–`C57` (plus `C39`–`C42` above), **12 resistors**
`R30`–`R41`, **15 test points** `TP1`–`TP12` on this sheet (`TP13`–`TP15` on
sheet 4).

| Ref | Value | Role |
|---|---|---|
| `C43`, `C44` | 100 nF/25 V, 10 µF/10 V | `VDD3P3` decoupling |
| `C46`–`C49` | 10 µF/10 V, 1 µF/25 V, 100 nF/25 V ×2 | S3 supply decoupling |
| `C51`, `C52` | 100 nF/25 V, 10 µF/10 V | `VDD3P3_CPU` |
| `C53` | 1 µF/25 V | `CHIP_PU` / `SOC_RESET` RC |
| `C54`, `C55` | 100 nF/25 V, 10 µF/10 V | `VDD3P3_RTC` |
| `C56`, `C57` | 1 µF/25 V, 100 nF/25 V | NOR flash `VDD_NOR` decoupling |
| `R30` | 499 Ω | `G44_U0_RX` series |
| `R31`, `R32`, `R33` | 10 kΩ, 10 kΩ, 10 kΩ | `SOC_RESET`, `G0_BOOT_OUT` pull-ups |
| **`R34`, `R35`, `R38`, `R39`, `R40`, `R41`, `R47`** | **22 Ω ×7** | **series damping** on SPI, e-paper SPI, USB `D+`/`D−` and the RTC I²C — the board's standard signal-integrity value |
| `R36`, `R37` | **2.2 kΩ ×2** | **system I²C bus pull-ups** to `3V3_L2` (`G47_SYS_SDA` / `G48_SYS_SCL`) |
| `TP1`–`TP12` | — | rails and debug: `VBUS_L0`, `3V3_L0`, `3V3_L1`, `3V3_L2`, `3V3_L2_LoRa`, `GND`, `G43_U0_TX`, `G44_U0_RX`, `SOC_RESET`, `G0_BOOT_OUT`, `BAT_ADC_EN`, `PY_LED_R` **[SCH-T]** |

---

## 7. Sheet 4 — RTC, IMU, buzzer, radios, touch, e-paper, microSD (79)

### 7.1 Integrated circuits and modules

| Ref | Part | Function | Record |
|---|---|---|---|
| `U14` | `Stamp-LoRa-1262-mini` | LoRa module (Semtech SX1262 inside) — **not fitted on the Lite** | [m5stack/stamp-lora-1262](../../../components/m5stack/stamp-lora-1262/README.md) |
| `U15` | `BMI270` | 6-axis IMU, I²C `0x68` | [bosch-sensortec/bmi270](../../../components/bosch-sensortec/bmi270/README.md) |
| `U16` | `RX8130CE` | RTC, I²C `0x32` | [seiko-epson/rx8130ce](../../../components/seiko-epson/rx8130ce/README.md) |
| `U17` | `M5IOE1` | I/O expander coprocessor, I²C `0x4F` | [m5stack/m5ioe1](../../../components/m5stack/m5ioe1/README.md) |
| `U18` | `AW35122FDR` | load switch → `TP_VDD` (touch) | [awinic/aw35122](../../../components/awinic/aw35122/README.md) |
| `U19` | `AW39112DNR` | 2-bit translator — the self-isolating touch I²C branch | [awinic/aw39112](../../../components/awinic/aw39112/README.md) |
| `U20` | — | **microSD socket**, 9 contacts + shell. **No part number on the schematic** | [generic/micro-sd-sdmmc](../../../components/generic/micro-sd-sdmmc/README.md) (interface); part **unidentified**, §9 |
| `U21` | `AW35122FDR` | load switch → `PDM_VDD` (microphone) | [awinic/aw35122](../../../components/awinic/aw35122/README.md) |

### 7.2 Connectors

| Ref | Part | Pins | Carries | Record |
|---|---|---:|---|---|
| `J3` | `BTB0.408-10PLBDR-G41` | 10 + 4 tabs | to the **NFC sub-board**: 3V3, GND, I²C, `G6_RFID_INT`, `PYB_NFC_EN` | [generic/btb0.408-10plbdr-g41](../../../components/generic/btb0.408-10plbdr-g41/README.md) |
| `J4` | — | 8 | **touch panel FPC** — `TP_VDD`, `TP_SYS_SDA/SCL`, `G4_TP_INT`, `PYB_TP_RST` | **unidentified**, §9; controller: [focaltech/ft6336g](../../../components/focaltech/ft6336g/README.md) |
| `J5` | `FPC0.5-SMT-24P-B` | 24 | **e-paper panel FPC** — 4-wire SPI, `BUSY`, `RST`, and the panel's own boost network | [generic/fpc0.5-smt-24p-b](../../../components/generic/fpc0.5-smt-24p-b/README.md) · panel: [dke/depg0397bbs770f3](../../../components/dke/depg0397bbs770f3/README.md) |
| `J6` | `AXE512127D` | 12 + 4 tabs | to the **KEY/RGB/PDM sub-board** | [panasonic/axe512127d](../../../components/panasonic/axe512127d/README.md) |
| `BUZZER1` | `ER103` | 2 | **magnetic buzzer**, `+` on `3V3_L1` | **unidentified**, §9 |

### 7.3 Discrete semiconductors

| Ref | Part | Circuit role | Record |
|---|---|---|---|
| `Q3` | `SK2302AAT` | N-channel **buzzer low-side driver**: gate = `G42_BB_PWM` with `R50` = 10 kΩ pulldown, source = GND, drain = `BUZZER1` `−` **[SCH-V]** | [generic/sk2302aat](../../../components/generic/sk2302aat/README.md) |
| `Q4` | `CJ2310` | N-channel **e-paper bias switch** — the external NMOS for the SSD1677's on-chip DC/DC. Gate = `J5`.2 `GDR`, drain = `L8`/`D4`, source = `RESE` sense node through `R59` = 1.2 Ω **[SCH-V]** | [changjing/cj2310](../../../components/changjing/cj2310/README.md) |
| `D3` | `1N4148WS` | **flyback clamp across the buzzer** — anode on `Q3`'s drain, cathode on the `3V3_L1` side **[SCH-V]** | [generic/1n4148ws](../../../components/generic/1n4148ws/README.md) |
| `D4` | `1N5819WS` | **e-paper boost rectifier** → `PREVGH` **[SCH-V]** | [generic/1n5819ws](../../../components/generic/1n5819ws/README.md) |
| `D5` | `1N5819WS` | **inverting charge-pump diode** — `PREVGL` → flying node **[SCH-V]** | idem |
| `D6` | `1N5819WS` | **inverting charge-pump diode** — flying node → GND **[SCH-V]** | idem |
| `TVS3`–`TVS9` | `ESD5311` ×7 | **ESD clamps on the microSD interface**, one per line — see §7.5 | [generic/esd5311](../../../components/generic/esd5311/README.md) |

### 7.4 The e-paper bias generator, as drawn **[SCH-V]**

Worth stating as a circuit because three of the six diodes and one of the five
MOSFETs on this board exist only to serve it, and because it matches the DKE
panel manual's own typical application circuit:

```
EPD_3V3_L3 ──[ L8  33 µH ]──┬──▶|── D4 ──┬── PREVGH   (C72 10 µF/25 V)
   SPH252010H330MT          │            │
                            │            └──┤ C67 10 µF/25 V ├──┬── D5 ──┘
                       Q4 drain                                 │
   J5.2 GDR ──┬── Q4 gate                                       └── D6 ── GND
              │   CJ2310                                        │
          R58 10 kΩ                                           PREVGL (C73 10 µF/25 V)
              │
             GND       Q4 source ── R59 1.2 Ω ── GND
                                 └── J5.3 RESE  (peak-current sense back to the panel)
```

`L8` = `SPH252010H330MT`, 33 µH. **No inductor record**: like `L1`–`L3` it is a
converter design parameter, and the converter is inside the panel's SSD1677.

### 7.5 microSD ESD and pull-ups **[SCH-T]**, clamps **[SCH-V]**

| Line | ESD clamp | Pull-up | Value |
|---|---|---|---|
| `G9_TF_DATA2` | `TVS3` | `R62` | 4.7 kΩ |
| `G8_TF_DATA3` | `TVS4` | `R63` | 4.7 kΩ |
| `G12_TF_CMD` | `TVS5` | `R64` | 4.7 kΩ |
| `G13_TF_CLK` | `TVS6` | `R65` | 4.7 kΩ |
| `G11_TF_DATA0` | `TVS7` | `R66` | 4.7 kΩ |
| `G10_TF_DATA1` | `TVS8` | `R67` | 4.7 kΩ |
| `PYB_TF_DET` | `TVS9` | `R68` | **1 MΩ** — card-detect, not a bus line |

The sheet's own note: *"The `PYB_TF_DET` pin uses an internal pull-up to detect a
ground connection. It identifies card insertion and wakes up the ESP32."*
**[SCH-T]**

### 7.6 Passives — no records

**28 capacitors** `C58`–`C85`, **25 resistors** (`R42`–`R44`, `R47`, `R49`–`R54`,
`R58`–`R68`), **3 test points** `TP13`–`TP15` (`PYB_PDM_EN`, `PYB_TP_EN`, `RST`).

| Ref | Value | Role |
|---|---|---|
| `C58`, `C59` | 10 µF/10 V ×2 | IMU / NFC-connector rail decoupling |
| `C60`–`C62` | 1 µF/25 V ×3 | RTC decoupling |
| `C63`, `C64` | 100 nF/25 V ×2 | IMU decoupling |
| `C65` | 10 µF/10 V | LoRa module `VIN_3V3` |
| `C66`, `C68` | 10 µF/10 V ×2 | `TP_VDD` in/out |
| **`C67`** | **10 µF/25 V** | **e-paper charge-pump flying capacitor** **[SCH-V]** |
| `C69`, `C70` | 10 µF/10 V, 100 nF/25 V | M5IOE1 decoupling |
| `C71`, `C72`, `C73` | 10 µF/25 V ×3 | `EPD_3V3_L3`, `PREVGH`, `PREVGL` **[SCH-V]** |
| `C74`, `C75` | 4.7 µF/25 V ×2 | at `J5`.4/.5 — panel `VDHR` |
| `C76` | 10 µF/10 V | `3V3_L2` at the `J6` sub-board connector |
| `C77`–`C84` | 10 µF/25 V, 1 µF/25 V, 4.7 µF/25 V (mixed) | **`J5`.17–.24 panel rail decoupling** — `VDDD`, `VSH`, `VGH`, `VSL`, `VGL`, `VCOM`; values as the DKE manual specifies |
| `C85` | 10 µF/10 V | `PDM_VDD` |
| `R42`, `R43`, `R44` | 10 Ω, 100 kΩ, 22 Ω | IMU/`J3` area **[SCH-T]** — see §9 caveat |
| `R47` | 22 Ω | RTC `PYG0_RTC_INT` series |
| `R49` | 100 kΩ | RTC interrupt pull-up to `3V3_L0` |
| `R50` | 10 kΩ | `Q3` buzzer gate pulldown **[SCH-V]** |
| `R51`, `R53` | 10 kΩ ×2 | M5IOE1 `NRST` / `G7_PYB_IRQ` |
| `R52`, `R54` | `NC/1%`, 100 kΩ | M5IOE1 `ADD_SET` — **`R52` not fitted**, `R54` fitted: this pair sets the expander's I²C address |
| `R58` | 10 kΩ | `Q4` gate pulldown **[SCH-V]** |
| **`R59`** | **1.2 Ω** | **e-paper DC/DC current-sense resistor (`RESE`)** **[SCH-V]** |
| `R60`, `R61` | `0R/1%` ×2 | links on `G18_EINK_BUSY` and `PYB_EINK_RST` |
| `R62`–`R68` | see §7.5 | microSD |

---

## 8. Sheets 5 and 6 — the two sub-boards

### 8.1 Sheet 5 — `PaperMono KEY RGB.SchDoc` (23)

| Ref | Part / value | Function | Record |
|---|---|---|---|
| `U1` | `LMD4737T261-AC02` | PDM MEMS microphone | [generic/lmd4737t261-ac02-pdm-microphone](../../../components/generic/lmd4737t261-ac02-pdm-microphone/README.md) |
| `LED1` | `RS-C1415MBAR` | side RGB indicator | [generic/rs-c1415mbar-rgb-led](../../../components/generic/rs-c1415mbar-rgb-led/README.md) |
| `J1` | `AXE612124D` | board-to-board header, mates `J6` sheet 4 | [panasonic/axe612124d](../../../components/panasonic/axe612124d/README.md) |
| `S1`, `S2`, `S3` | `SW` | tactile switches: power button, `G2_KEY1`, `G3_KEY2` | **unidentified**, §9 |
| `DR1` | `ESD5311` | ESD clamp on **`PWR_BTN`** | [generic/esd5311](../../../components/generic/esd5311/README.md) |
| `DR2` | `ESD5311` | ESD clamp on **`G2_KEY1`** | idem |
| `DR3` | `ESD5311` | ESD clamp on **`G3_KEY2`** | idem |
| `R1` | 10 kΩ | **`PWR_BTN` pull-up to `3V3_L0`** — the always-on rail |
| `R2`, `R5` | 10 kΩ ×2 | `G2_KEY1`, `G3_KEY2` pull-ups **to `3V3_L2`** |
| `R3`, `R4` | 22 Ω ×2 | series damping on `G46_PDM_DAT`, `G45_PDM_CLK` |
| `R6`, `R7`, `R8` | 560 Ω, 820 Ω, 1 kΩ | RGB LED ballast — blue, green, red |
| `C1`, `C3`, `C4` | 100 nF/10 V ×3 | switch debounce at `S1`, `S2`, `S3` |
| `C2` | 100 nF/10 V | `PDM_VDD` decoupling |
| `C5` | 10 µF/10 V | `3V3_L2` bulk |
| `L1` | 2 nH | `PDM_VDD` feed — no record (supply bead) |

> **The power button pulls up to `3V3_L0` while the two user keys pull up to
> `3V3_L2`.** `3V3_L0` is the always-on rail and `3V3_L2` is switched off in the
> deep states, so **only the power button can be sensed when the system is at its
> lowest power level.** That is consistent with sheet 1's power-state table,
> which lists the power button as the `L0`/`L1` wake path and the keys only from
> `L2`. **[SCH-T]** + **[INF]**

### 8.2 Sheet 6 — `02 Paper Mono NFC.SchDoc` (43)

| Ref | Part / value | Function | Record |
|---|---|---|---|
| `U2` | `ST25R3916-AQWT` | NFC reader/writer + card emulation, I²C `0x50` | [stmicroelectronics/st25r3916](../../../components/stmicroelectronics/st25r3916/README.md) |
| `U1` | `AW35122FDR` | load switch gating `VCC_3V3` for the whole sub-board | [awinic/aw35122](../../../components/awinic/aw35122/README.md) |
| `X1` | **`27.12MHZ(XL7EL89CMI-111YLC)`** | **27.12 MHz crystal — the NFC carrier reference** | [generic/xl7el89cmi-111ylc-27.12mhz-crystal](../../../components/generic/xl7el89cmi-111ylc-27.12mhz-crystal/README.md) |
| `J1` | `BTB0.408-10PLBDR-G41` | board-to-board, mates `J3` sheet 4 | [generic/btb0.408-10plbdr-g41](../../../components/generic/btb0.408-10plbdr-g41/README.md) |
| `ANT1` | — | **PCB loop antenna**: 4 turns, 25 × 25 mm, 0.25 mm trace, 0.3 mm gap, 17 µm (0.5 oz) copper — stated as a layout note on the sheet | **unidentified** (it is copper, not a part), §9 |
| `L1`, `L2` | 270 nH ±5% ×2 | **EMC filter inductors** on `RFO1`/`RFO2` |
| `C14`, `C15` | 10 pF ×2 | **27.12 MHz crystal load capacitors** on `XTO`/`XTI` |
| `C2`–`C13` | 220 pF, 10 pF, 150 pF, 680 pF, 160 pF (mixed) | **the antenna matching and EMC filter bank** — `RFI_P`/`RFI_N`, `ANT1_P`/`ANT1_N` |
| `C16`–`C31` | 10 nF / 10 µF alternating ×16 | ST25R3916 supply decoupling (`VDD_AM`, `VDD_TX`, `VDD_RF`, `VDD_A`, `VDD_D`, `VDD_IO`, `VDD_DR`) |
| `C1` | 10 µF | `VCC_3V3` bulk at the load switch |
| `R1` | 0 Ω | `3V3_L2` → `U1` input link |
| `R2` | `NC` | `PYB_RFID_RST` → `U1` `EN` — **not fitted** |
| `R3`, `R5` | 2 Ω ×2 | **antenna series damping** on `ANT1_P` / `ANT1_N` |
| `R4` | 0 Ω | `I2C_EN` tied to `VCC_3V3` — **selects I²C, not SPI** |

> `R4` = 0 Ω to `VCC_3V3` on `I2C_EN` is the interface selection. The sheet spells
> it out: *"`I2C_EN`=VDD; I2C mode / `I2C_EN`=GND; SPI mode"*. **[SCH-T]**

### 8.3 The 11 `NC` positions — drawn but not fitted

Counted in the 289 because they are placed symbols; **not on the board**.

| Ref | Sheet | Value | What not fitting it means |
|---|---:|---|---|
| `R1`, `R2` | 2 | `NC/1%` | **No USB-PD.** The IP2315's `CC1`/`CC2` never reach the connector |
| `R6` | 2 | `NC/1%` | IP2315 `nACOK` unused |
| `R8`, `R13` | 2 | `NC` | charger I²C series links open — part of why `0x75` is off the bus |
| `R18` | 2 | `NC/1%` | IP2315 `LED3` unused |
| `R25` | 2 | `NC/1%` | `U8` `EN` pulldown omitted |
| `C26` | 2 | `NC/50V` | frontlight output capacitance reduced to `C25` alone |
| `C41`, `C42` | 3 | `NC(TBD)` | **antenna match positions left open and explicitly "TBD"** |
| `R52` | 4 | `NC/1%` | M5IOE1 address strap left at its default |
| `R2` | 6 | `NC` | `PYB_RFID_RST` does **not** drive the NFC load switch through this resistor |

> ⚠ **`R2` sheet 6 = `NC` deserves attention.** The device record establishes
> ([`gaps-and-conflicts.md`](gaps-and-conflicts.md) R9) that `PYB_NFC_EN` and
> `PYB_RFID_RST` are the same wire across the board-to-board pair, and that it
> drives a load-switch enable rather than a reset. The resistor drawn in that
> path is **not fitted**, and `R2`'s other end is marked `NC` too. What actually
> enables `U1` sheet 6 was **not resolved** from this PDF and is listed in §9.

---

## 9. Unidentified — 12 positions, and what would resolve each

Per the method, **no part number is guessed**. Each of these is a real placed
component whose part could not be established from the published evidence.

| Ref | Sheet | What the schematic says | What would resolve it |
|---|---:|---|---|
| `D1` | 2 | `DSK34` | A `DSK34` marking search returned nothing conclusive. A photograph of the top marking, or M5Stack's BOM |
| `LED1` | 2 | no part string | Board photo; it is the charger's status LED |
| `J1` | 2 | no part string, 6-pin | Board photo of the frontlight connector, or a replacement-part listing |
| `FT1` | 3 | `ICMF062P900MFR` | A common-mode choke; the code resembles a `0603`/`90 Ω` USB CMC but **no manufacturer was established**. Vendor cross-reference needed |
| `ANT1` | 3 | no part string | Whether it is a chip antenna or PCB trace is not shown. A board photo settles it |
| `J4` | 4 | no part string, 8-pin FPC | Board photo; the mating flex is part of the touch panel assembly |
| `U20` | 4 | `MicroSD` only | Board photo of the socket; the *interface* is fully documented |
| `BUZZER1` | 4 | `ER103` | `ER103` looks like a series code for a 10 mm magnetic buzzer but no vendor was confirmed |
| `S1`, `S2`, `S3` | 5 | `SW` only | Board photo, or the mechanical drawing |
| `ANT1` | 6 | layout note only | It is a **PCB trace loop**, not a purchased part; "unidentified" is the wrong frame — there is nothing to buy |
| `L1`–`L3`, `L8` | 2, 4 | `FTC…`, `SPH…` series codes | Series codes without a manufacturer prefix. An LCSC/Digi-Key cross-reference on the full code |
| `U1` sheet 6 enable | 6 | `R2` = `NC` | What drives `U1`'s `EN` when `R2` is unfitted. Needs NFC sheet **1 of 2**, which is unpublished |

Three further caveats that are **not** identity questions but are unresolved:

- **`R42`, `R43`, `R44` values** (sheet 4). The text layer renders these as
  fragmented single characters (`1 0 R / 1 %`, `2 2 R / 1 %`) because they sit in
  a dense area. 10 Ω / 100 kΩ / 22 Ω is the reading, **[SCH-T]** only, and it was
  not confirmed against a rendered image.
- **`J4`'s pin numbering** (sheet 4). The signal set is solid; the 1-to-8 order is
  not, and is [deliberately not asserted](../../../components/focaltech/ft6336g/README.md#41-signals-at-j4-sch-sheet-4).
- **Capacitor dielectrics and case sizes.** Absent from the document entirely.

---

## 10. What has a component record

**56 of the 290** placed components resolve to a record; **13** are unidentified
(§9); the remaining **221** are ordinary passives left without one. The
[component index](../../../components/README.md) is the entry point; these are
the ones this board contributes.

**Created before this pass:** IP2315 · AW32901FCR · AW39112DNR ×2 · AW35122FDR ×4
· AW9967DNR · SSP7615-33DFR ×4 · JW5712 · M5PM1 · M5IOE1 · PY32L020F15U6 ·
ESP32-S3R8 · XM25UH128DHIQT · 40 MHz crystal · BMI270 · RX8130CE · FT6336G ·
DEPG0397BBS770F3 · SSD1677 · Stamp-LoRa-1262 · SX1262 · ST25R3916 ·
LMD4737T261-AC02 · RS-C1415MBAR.

**Created by this pass (2026-09-01):**

| Record | Instances | Designators |
|---|---:|---|
| [`TYPEC-302-BRP16SC08`](../../../components/generic/typec-302-brp16sc08/README.md) | 1 | **`USB`** sheet 2 |
| [`FPC0.5-SMT-24P-B`](../../../components/generic/fpc0.5-smt-24p-b/README.md) | 1 | `J5` sheet 4 |
| [`AXE512127D`](../../../components/panasonic/axe512127d/README.md) | 1 | `J6` sheet 4 |
| [`AXE612124D`](../../../components/panasonic/axe612124d/README.md) | 1 | `J1` sheet 5 |
| [`BTB0.408-10PLBDR-G41`](../../../components/generic/btb0.408-10plbdr-g41/README.md) | 2 | `J3` sheet 4 · `J1` sheet 6 |
| [`ESD5311`](../../../components/generic/esd5311/README.md) | **12** | `TVS1`, `TVS2` sheet 2 · `TVS3`–`TVS9` sheet 4 · `DR1`–`DR3` sheet 5 |
| [`SK2301AAT`](../../../components/generic/sk2301aat/README.md) | 1 | `Q5` sheet 2 |
| [`SK2302AAT`](../../../components/generic/sk2302aat/README.md) | 2 | `Q2` sheet 2 · `Q3` sheet 4 |
| [`CJ2310`](../../../components/changjing/cj2310/README.md) | 1 | `Q4` sheet 4 |
| [`CJ3439KDW`](../../../components/changjing/cj3439kdw/README.md) | 1 | `Q1` sheet 2 |
| [`RB162VAM-20TR`](../../../components/rohm/rb162vam-20tr/README.md) | 1 | `D2` sheet 2 |
| [`1N4148WS`](../../../components/generic/1n4148ws/README.md) | 1 | `D3` sheet 4 |
| [`1N5819WS`](../../../components/generic/1n5819ws/README.md) | 3 | `D4`, `D5`, `D6` sheet 4 |
| [`XL7EL89CMI-111YLC` 27.12 MHz](../../../components/generic/xl7el89cmi-111ylc-27.12mhz-crystal/README.md) | 1 | `X1` sheet 6 |
| [`100K-RNTC` thermistor](../../../components/generic/100k-rntc-thermistor/README.md) | 1 | `R15` sheet 2 |
| [1150 mAh Li-ion cell](../../../components/generic/papermono-1150mah-liion-cell/README.md) | 1 | at `J2` sheet 2 |

---

## 11. ⚠ Conflict raised by this pass — the NTC does not measure the cell

Several places in this device's record describe the battery as **"NTC-sensed"**
and put the thermistor **at `J2`**, for example
[`README.md`](README.md) ("1150 mAh Li-ion, NTC-sensed"),
[`features/battery-and-charging.md`](features/battery-and-charging.md)
("battery (J2, 1150 mAh + 100K NTC)") and
[`pinouts-and-buses.md`](pinouts-and-buses.md) ("`J2` … Battery, with a
`100K-RNTC` thermistor").

**The schematic does not support the thermistor being in the battery pack.**
**[SCH-V]**

| Claim | Evidence |
|---|---|
| `J2` has **two pins only** | Rendered at 200 dpi: a 2-contact symbol, pin 2 → `VBAT_L0`, pin 1 → GND, `CON2_SMD` printed beneath, `C13` = 22 µF/10 V across. There is no third contact and no thermistor pin |
| `R15` (`100K-RNTC`) is a **board part** | It carries a reference designator in the `R` series, is placed on sheet 2 beside the IP2315, and connects `NTC` (pin 26) to GND in parallel with `R16` = 82 kΩ |

So the arrangement is: **a 100 kΩ NTC soldered to the mainboard on the charger's
`NTC` pin**, not a thermistor inside the cell reaching the board through the
connector. Two consequences, both safety-relevant, both `inferred`:

1. **What is being measured is board temperature near the charger, not cell
   temperature.** Those track each other loosely at best, and diverge exactly when
   it matters — a cell going into thermal runaway heats faster than the PCB
   beneath it.
2. **A replacement cell needs no thermistor**, and fitting a 3-wire pack would not
   improve the protection, because there is nowhere for the third wire to go.

**This conflict is recorded, not resolved.** It is possible M5Stack places `R15`
physically under the cell so that it is thermally coupled to it; nothing in a
schematic can show that, and a board photograph or a thermal measurement would
settle it. The wording in the records above should be read as "the charger has
NTC-based temperature qualification", which is true, rather than "the battery
pack contains a thermistor", which this evidence does not support. Date
2026-09-01. See also the
[battery record](../../../components/generic/papermono-1150mah-liion-cell/README.md)
and the [thermistor record](../../../components/generic/100k-rntc-thermistor/README.md).

---

## 12. Reproducing this census

```bash
cd scratch/m5stack-papermono
nix-shell -p poppler-utils --run '
  for n in 1 2 3 4 5 6; do
    pdftotext -bbox -f $n -l $n \
      pdf/PaperMono_SCH_V0.6.2_20260522.pdf pdf/bbox-p$n.xml
  done'
python3 tools/census.py          # corrected counts + gap analysis
python3 tools/co_values.py       # designator -> adjacent-text dump
python3 ../../tools/altium_pdf_render_sheet.py 4      # a sheet as ordered text
python3 ../../tools/altium_pdf_pin_table.py 4 J5      # one component's pins
```

To re-read a block as an image, which is what **[SCH-V]** means:

```bash
nix-shell -p poppler-utils -p imagemagick --run '
  pdftoppm -r 200 -png -f 2 -l 2 pdf/PaperMono_SCH_V0.6.2_20260522.pdf out
  magick out-2.png -crop 400x260+1850+230 +repage -resize 250% crop.png'
```

`executed-success` for all of the above on 2026-09-01.

---

## 13. Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | **V0.6.2**, 6 sheets, A4 landscape, Altium | the entire census, every value and every net cited here. Local: [`artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf`](artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf) |
| S2 | PaperMono product page | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | — | 1150 mAh cell capacity; SKU C153 |

Component datasheets acquired for the records created by this pass are hashed in
each component's own **Local artifacts** table, and indexed from
[`sources.md`](sources.md).

## Related pages

- [PaperMono device record](README.md) — start here
- [`pinouts-and-buses.md`](pinouts-and-buses.md) — the wiring tables this BOM supports
- [`power-architecture.md`](power-architecture.md) — what the rails on sheet 2 do
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — board-wide unresolved items
- [Component index](../../../components/README.md)
