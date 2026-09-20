# Jiangsu Changjing CJ3439KDW

> **Complementary MOSFET pair — one N-channel and one P-channel in a single SOT-363**, ±20 V, 0.75 A / −0.66 A, 380 mΩ @ 4.5 V.
> Research snapshot **2026-09-01**. Fitted as **`Q1` on sheet 2** of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153), where the two halves together form the **gated battery-voltage sense divider** — the circuit that lets the board measure the cell without leaking current the rest of the time.
> **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Jiangsu Changjing `CJ3439KDW` datasheet, **D, Mar 2016**; local copy `artifacts/cj3439kdw-changjing-lcsc-mirror.pdf` | `not-tested` |
| **[CAT]** | LCSC / JLCPCB catalogue entry `C99824`, retrieved 2026-09-01 | `not-tested` |
| **[SCH-V]** | Read off sheet 2 rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity and ratings **[DS]**

| Property | Value |
|---|---|
| Part | **`CJ3439KDW`** |
| Manufacturer | **Jiangsu Changjiang Electronics Technology Co., Ltd.** (江苏长电科技) |
| LCSC part | `C99824` **[CAT]** |
| Function | **N-channel + P-channel complementary pair**, two independent dice in one package |
| Package | **SOT-363** (SC-88, 6-lead) |
| Datasheet date | **D, Mar 2016** |
| Vendor applications | *"Load/power switching; interfacing switching; battery management for ultra small portable electronics; logic level shift"* |
| Vendor note | *"Including a N-ch **CJ3134K** and a P-ch **CJ3139K** (independently) in a package"* |

| | **N-MOSFET** | **P-MOSFET** |
|---|---|---|
| V<sub>DS</sub> | **20 V** | **−20 V** |
| **V<sub>GS</sub>** | **±12 V** | **±12 V** |
| I<sub>D</sub> continuous | **0.75 A** | **−0.66 A** |
| I<sub>DM</sub> pulsed (10 µs) | 1.8 A | −1.2 A |
| R<sub>DS(on)</sub> @ 4.5 V | **380 mΩ** | 520 mΩ |
| R<sub>DS(on)</sub> @ 2.5 V | 450 mΩ | 700 mΩ |
| R<sub>DS(on)</sub> @ 1.8 V | 800 mΩ | 950 mΩ (typ) |

Thermal: R<sub>θJA</sub> **833 °C/W**, T<sub>J</sub> 150 °C, T<sub>stg</sub>
−55…+150 °C, lead temperature 260 °C. Features listed: low R<sub>DS(on)</sub>,
operation at low logic-level gate drive, **ESD-protected gates**.

> **V<sub>GS</sub> = ±12 V**, noticeably more headroom than the ±8 V of the
> board's [SK2301AAT](../../generic/sk2301aat/README.md) and
> [SK2302AAT](../../generic/sk2302aat/README.md).

### 1.1 Pinout **[DS]** — this is what makes §3 assertable

```
   D1    G2    S2
    6     5     4
    ┌───────────┐
    │           │
    └───────────┘
    1     2     3
   S1    G1    D2
```

| Pin | Function | Die |
|---:|---|---|
| 1 | `S1` — source | **N-channel** |
| 2 | `G1` — gate | **N-channel** |
| 6 | `D1` — drain | **N-channel** |
| 3 | `D2` — drain | **P-channel** |
| 4 | `S2` — source | **P-channel** |
| 5 | `G2` — gate | **P-channel** |

Note the **diagonal layout**: the N-channel occupies pins 1, 2, 6 and the
P-channel pins 3, 4, 5. Reading it as "left half / right half" is wrong and is an
easy mistake at a rework bench.

---

## 2. Used By

### `devices/m5stack/papermono` — `Q1`, sheet 2

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md).
**One instance.** The schematic draws it as two symbols, **`Q1A`** (the
N-channel) and **`Q1B`** (the P-channel), which is why the census records `Q1`
twice — one `CO` marker per drawn part, one physical package.

**On the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md):**
`inferred` **yes**. The Lite drops only NFC and LoRa and carries the same 1150 mAh
cell and the same charging arrangement, so it needs the same battery
measurement. Not read from the Lite's own schematic.

---

## 3. What it actually switches **[SCH-V]**

`Q1` is the switch in a **gated battery-voltage divider**. This is the circuit the
firmware uses to read the cell, and both dice are needed for it.

```
                    VBAT_L0
                       │
              ┌────────┴────────┐
              │                 │
         R3 1 MΩ           Q1B pin 4  SOURCE
              │            (P-channel, CJ3439KDW)
              ├──────────  Q1B pin 5  GATE
              │            Q1B pin 3  DRAIN
     Q1A pin 6 DRAIN            │
     (N-channel)           R5 1 kΩ
     Q1A pin 1 SOURCE ─ GND     │
     Q1A pin 2 GATE             ├──── BAT_ADC ──┬── C7 100 nF/25 V ── GND
              │                 │               │
   BAT_ADC_EN ┤            R12 1 kΩ             │
              │                 │               │
        R11 100 kΩ             GND              │
              │                                 │
             GND                                └── to the M5PM1 BAT_ADC_IN
```

| Node | Net | Evidence |
|---|---|---|
| `Q1A` gate (pin 2) | **`BAT_ADC_EN`**, pulled down by **`R11` = 100 kΩ** | **[SCH-V]** |
| `Q1A` source (pin 1) | **GND** | **[SCH-V]** |
| `Q1A` drain (pin 6) | `Q1B`'s gate node, pulled up by **`R3` = 1 MΩ** | **[SCH-V]** |
| `Q1B` source (pin 4) | **`VBAT_L0`** | **[SCH-V]** |
| `Q1B` gate (pin 5) | the same node as `Q1A`'s drain | **[SCH-V]** |
| `Q1B` drain (pin 3) | **`R5` = 1 kΩ** → `BAT_ADC` → **`R12` = 1 kΩ** → GND | **[SCH-V]** |
| `BAT_ADC` | filtered by **`C7` = 100 nF/25 V** | **[SCH-V]** |

**Operation:**

| `BAT_ADC_EN` | `Q1A` | `Q1B` gate | `Q1B` | `BAT_ADC` | Divider current |
|---|---|---|---|---|---|
| **low** (or floating — `R11` holds it) | off | pulled to `VBAT_L0` by `R3` ⇒ V<sub>GS</sub> = 0 | **off** | ~0 V | **only `V`<sub>BAT</sub>`/1 MΩ` ≈ 4 µA through `R3`** |
| **high** | on | pulled to GND ⇒ V<sub>GS</sub> ≈ −V<sub>BAT</sub> | **on** | **≈ V<sub>BAT</sub> / 2** | ≈ 2 mA through `R5`+`R12` |

`R5` = `R12` = 1 kΩ, so **`BAT_ADC` = V<sub>BAT</sub> × 0.5** — a 4.2 V cell
presents 2.1 V, comfortably inside a 3.3 V ADC range.

### 3.1 Why the gate exists, and why it is worth 1 kΩ + 1 kΩ

A permanently connected 1 kΩ/1 kΩ divider across a 3.7 V cell burns
**≈ 1.85 mA continuously**. On a 1150 mAh cell that alone is a **~26-day** flat
battery with the rest of the board switched off. Unacceptable for a device whose
selling point is e-paper standby.

Gating it costs one dual MOSFET and two resistors and reduces the standing drain
to the ~4 µA through `R3` — a **~450× improvement** — while keeping the divider
low-impedance (1 kΩ) *during* a measurement, which is what an SAR ADC wants for a
fast, accurate settle. A high-value always-on divider (say 1 MΩ/1 MΩ) would have
avoided the drain but would need a long settling time and would be noise-prone.

**This is a deliberate and rather good piece of design**, and it is the reason the
part is a *complementary pair* rather than a single FET: the P-channel does the
high-side switching and the N-channel provides the level shift that lets a 3.3 V
logic signal control it against a variable battery rail. **[INF]**

### 3.2 The `_EN` polarity is the right way round, and that is evidence

Note the logic: **`BAT_ADC_EN` high enables the divider.** Had `Q1B` been an
N-channel with its source at the bottom, `R3` would hold it *on* by default and
the signal would have to be named `_DIS`. The naming and the topology agree,
which is a useful independent check that the P-channel identification is right —
and the datasheet's pinout (§1.1) confirms it directly.

### 3.3 Who owns `BAT_ADC_EN` and `BAT_ADC`

Both belong to the [M5PM1](../../m5stack/m5pm1/README.md) power-management
coprocessor, not to the ESP32-S3: sheet 2 shows `BAT_ADC_EN_OD` on M5PM1 pin 1
and `BAT_ADC_IN` on pin 11. **[SCH-V]** So **battery measurement is a
power-manager function**, and an application reads the cell by asking the M5PM1
over I²C at `0x6E` rather than by sampling an ADC itself. See
[`power-architecture.md`](../../../devices/m5stack/papermono/power-architecture.md).

The `_OD` suffix on the M5PM1 pin name indicates an **open-drain** output, which
`R11` = 100 kΩ complements as the pulldown — meaning the M5PM1 can only pull the
node *low*, and the enable is… **[INF]** ⚠ this reading and the §3 operating
table disagree about which way an open-drain output would drive the gate. With an
open-drain output and a pulldown, the pin cannot drive the gate high at all.
**Either the `_OD` naming is inherited rather than literal, or there is a pull-up
not visible in this reading.** Recorded as an open question (§7) rather than
resolved; the divider topology itself is not in doubt.

### 3.4 Operating conditions — heavily de-rated

| Parameter | Rating | On this board |
|---|---|---|
| V<sub>DS</sub> (both) | ±20 V | ≤ 4.35 V |
| **V<sub>GS</sub>** | **±12 V** | ≤ 4.35 V — **~2.8× margin** |
| I<sub>D</sub> | 0.75 A / −0.66 A | ~2 mA |
| R<sub>DS(on)</sub> | 520 mΩ @ −4.5 V (P) | in series with `R5` = 1 kΩ ⇒ **~0.05 % divider error** |

That last row is worth stating: the P-channel's on-resistance sits in series with
the top leg of the divider, so it perturbs the ratio. At ~520 mΩ against 1 kΩ it
is **0.05 %** — negligible. But R<sub>DS(on)</sub> rises to 700 mΩ at 2.5 V of
drive and ~950 mΩ at 1.8 V, so at a **deeply discharged cell** the error grows to
about 0.1 %, still negligible, and the *real* risk is not accuracy but the FET
failing to enhance at all. **[INF]**

---

## 4. Substitution

| Alternative | Note |
|---|---|
| Changjing **`CJ3134K`** + **`CJ3139K`** | The two dice, sold separately — the datasheet says so explicitly **[DS]** |
| Diodes **DMC2400UV**, AOS **AO6604**, Vishay **Si1029X** | Complementary pairs in SOT-363 / SC-70-6 |
| Two discrete SOT-523 FETs | ⚠ Doubles the footprint and loses the matched pair; the board already carries [SK2301AAT](../../generic/sk2301aat/README.md) + [SK2302AAT](../../generic/sk2302aat/README.md) doing exactly this on the `VBAT_DET` path |

Required: **one N-channel and one P-channel**, ≥ 20 V, **V<sub>GS</sub> ≥ ±8 V**,
logic-level thresholds, **and the same SOT-363 pin assignment** — complementary
pairs in this package do **not** share a universal pinout, and swapping the dice
turns the circuit into a permanent short from `VBAT_L0` to the divider.

---

## 5. Integration pitfalls

1. **The pinout is diagonal** (§1.1): N-channel on 1/2/6, P-channel on 3/4/5.
   Verify against the replacement's own datasheet, never by assumption.
2. **`R3` = 1 MΩ is the standing drain**, ~4 µA. If the board's sleep current is
   being budgeted, this is one of the terms.
3. **`R11` = 100 kΩ is a safety pulldown.** Without it the divider's state during
   reset is undefined and the board would leak ~1.85 mA whenever the M5PM1 is not
   driving the pin.
4. **`R5` and `R12` must be matched to keep the ratio.** Both are 1 %; the ratio
   error is therefore up to ~1 %, which is **larger than every other error term
   in §3.4 combined** and is the dominant uncertainty in the reported battery
   voltage. **[INF]**
5. **`BAT_ADC` is an M5PM1 pin, not an ESP32-S3 pin** (§3.3). Firmware reads it
   over I²C.
6. **Two `CO` markers, one package** (§2) — a census counts `Q1` twice.

---

## 6. A note on the board's two gated-sense circuits

The PaperMono has **two** transistor-gated battery-related nets, and they are
easily confused:

| | `BAT_ADC` (this record) | `VBAT_DET` ([SK2301AAT](../../generic/sk2301aat/README.md)) |
|---|---|---|
| Switch | `Q1` CJ3439KDW, N+P in one package | `Q2` + `Q5`, two discrete SOT-523 FETs |
| Controlled by | **`BAT_ADC_EN`** — a logic signal from the M5PM1 | **`VUSB_IN`** — a power rail; automatic, no firmware |
| Output | V<sub>BAT</sub> **÷ 2**, filtered | V<sub>BAT</sub> **unattenuated** |
| Consumer | M5PM1 ADC | not established |
| Purpose | measure the cell | detect the cell, probably for the charger |

Same idea, different mechanism, different purpose. **They are not redundant.**

---

## 7. Open questions

- **The `_OD` / pulldown contradiction in §3.3.** The M5PM1 pin is named
  `BAT_ADC_EN_OD` (open-drain) but the gate has only a 100 kΩ pulldown, and an
  open-drain output cannot then drive it high. Resolving this needs a re-render of
  the M5PM1 pin region, or the M5PM1 datasheet's pin-type table.
- Whether firmware calibrates out the `R5`/`R12` tolerance (§5.4).
- The datasheet's V<sub>GS(th)</sub> and full electrical tables — present in the
  file, not transcribed here.
- No measurement of anything: no ADC reading, no leakage, no divider accuracy.

---

## Manufacturer

**Jiangsu Changjiang Electronics Technology Co., Ltd.** (江苏长电科技, "CJ"),
`www.cj-elec.com`. A large Chinese discrete-semiconductor maker, distributed
mainly through LCSC. No vendor sourcing guide exists in this repository yet.
The board also carries their [CJ2310](../cj2310/README.md) and, probably, their
[1N4148WS](../../generic/1n4148ws/README.md).

**⚠ Retrieval finding — the LCSC PDF host trap.** LCSC's catalogue gives the
datasheet URL as
`https://www.lcsc.com/datasheet/lcsc_datasheet_1810010613_…CJ3439KDW_C99824.pdf`,
which returned **HTTP 200 and 47 908 bytes of HTML** to all five user-agents
tried. Rewriting the host and path to the CDN worked first try:

```
wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/1810010613_Jiangsu-Changjing-Electronics-Technology-Co---Ltd--CJ3439KDW_C99824.pdf
```

**Check the `%PDF` magic bytes; the status code and the `.pdf` extension both
lie.** `executed-success`, 2026-09-01. This belongs in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

Note that LCSC's stored filename spells the company **"Changjing"** while the
datasheet's own header spells it **"CHANGJIANG"**. Search both.

## Related pages

- [Changjing CJ2310](../cj2310/README.md) — same maker, `Q4`, the e-paper bias switch
- [Shikues SK2301AAT](../../generic/sk2301aat/README.md) · [SK2302AAT](../../generic/sk2302aat/README.md) — the board's other gated battery circuit (§6)
- [M5Stack M5PM1](../../m5stack/m5pm1/README.md) — owns `BAT_ADC_EN` and `BAT_ADC`
- [1150 mAh Li-ion cell](../../generic/papermono-1150mah-liion-cell/README.md) — what is being measured
- [PaperMono power architecture](../../../devices/m5stack/papermono/power-architecture.md) · [bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| D1 | `CJ3439KDW` SOT-363 Plastic-Encapsulate MOSFETs | Jiangsu Changjiang Electronics (via LCSC CDN) | primary, via distributor mirror | <https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/1810010613_Jiangsu-Changjing-Electronics-Technology-Co---Ltd--CJ3439KDW_C99824.pdf> | 2026-09-01 | **D, Mar 2016**, 6 pp | complementary N+P construction, **the §1.1 equivalent-circuit pinout**, all §1 maxima, the `CJ3134K`/`CJ3139K` die identification | `artifacts/cj3439kdw-changjing-lcsc-mirror.pdf` |
| C1 | LCSC entry `C99824` | LCSC / JLCPCB | distributor | JLCPCB SMT parts API, keyword `CJ3439KDW` | 2026-09-01 | — | manufacturer; 120 pF / 13 pF / 15 pF; 660 mA / 750 mA; the (broken) `www.lcsc.com` URL | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | `Q1` = `CJ3439KDW`; the whole §3 topology; `R3`, `R5`, `R11`, `R12`, `C7` values; `BAT_ADC_EN` and `BAT_ADC` nets | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/cj3439kdw-changjing-lcsc-mirror.pdf` | 1 042 949 | `41cb3b3374616678b096dfab449a544e165c1878e2b6d7b2f0fbf1c70effcb66` | 6 |

**Method note.** D1 validated as `%PDF` (`executed-success`) with an intact text
layer. §3 was read from a 200 dpi render of sheet 2 **before** the datasheet was
retrieved; the datasheet's equivalent-circuit pinout then confirmed the channel
assignment independently — the image showed a complementary pair with the
P-channel high-side, and `CJ3439KDW` turned out to be exactly that. Two
independent sources agreeing is why §3 is asserted rather than inferred.
