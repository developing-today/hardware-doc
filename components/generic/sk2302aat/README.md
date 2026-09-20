# Shikues SK2302AAT

> **N-channel MOSFET**, 20 V, 2.1 A, 70 mΩ @ V<sub>GS</sub> = 2.5 V, TrenchFET, **SOT-523**, marking **`A2S`**.
> Research snapshot **2026-09-01**. Used **twice** on the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153): **`Q2` sheet 2** (the USB-presence half of the battery-detect switch) and **`Q3` sheet 4** (the **buzzer driver**).
> **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Shikues `SK2302AAT` datasheet **REV.08**, local copy `artifacts/sk2302aat-shikues-lcsc-mirror.pdf` | `not-tested` |
| **[CAT]** | LCSC / JLCPCB catalogue entry `C475757`, retrieved 2026-09-01 | `not-tested` |
| **[SCH-V]** | Read off the schematic rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity and ratings

| Property | Value | Evidence |
|---|---|---|
| Part | **`SK2302AAT`** | **[SCH-V]**, **[DS]** |
| Manufacturer | **Shikues** | **[CAT]** |
| LCSC part | `C475757` | **[CAT]** |
| Function | **N-channel** enhancement MOSFET, TrenchFET | **[DS]** |
| Package | **SOT-523** | **[DS]** |
| **Top marking** | **`A2S`** | **[DS]** |
| V<sub>DS</sub> | **20 V** | **[DS]** |
| **V<sub>GS</sub>** | **±8 V** | **[DS]** |
| I<sub>D</sub> continuous | **2.1 A** | **[DS]** |
| I<sub>S</sub> (body diode) | 0.6 A | **[DS]** |
| R<sub>DS(on)</sub> | **70 mΩ @ 2.5 V** | **[CAT]** |
| V<sub>GS(th)</sub> | 650 mV | **[CAT]** |
| P<sub>D</sub> | **0.35 W** | **[DS]** — LCSC also says 350 mW; the two agree, unlike the [SK2301AAT](../sk2301aat/README.md#12--a-power-dissipation-discrepancy-between-the-datasheet-and-the-distributor) |
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

Same pin order as its P-channel sibling
[`SK2301AAT`](../sk2301aat/README.md) — which is convenient for the two-transistor
switch of §3.1 and dangerous at a rework bench, since **the two parts differ by
one digit and by channel type**.

---

## 2. Used By

### `devices/m5stack/papermono` — **2 instances**

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md).

| Ref | Sheet | Role | §|
|---|---:|---|---|
| **`Q2`** | 2 | USB-presence inverter driving the `Q5` high-side switch | §3.1 |
| **`Q3`** | 4 | **buzzer low-side driver** | §3.2 |

**On the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md):**
`inferred` **yes, both**. The Lite drops only NFC and LoRa; both the battery
detect path and the buzzer are retained. Not read from the Lite's own schematic.

---

## 3. What each one switches **[SCH-V]**

### 3.1 `Q2`, sheet 2 — USB-presence detection

`Q2` is the low-side half of a two-transistor high-side switch whose pass element
is **`Q5`** ([SK2301AAT](../sk2301aat/README.md), P-channel).

| `Q2` terminal | Net |
|---|---|
| pin 1 **GATE** | **`VUSB_IN`**, with **`R9` = 100 kΩ** to GND |
| pin 2 **SOURCE** | **GND** |
| pin 3 **DRAIN** | **`Q5`'s gate**, pulled up to `VBAT_L0` by `R45` = 100 kΩ |

When USB is plugged in, `VUSB_IN` rises, `Q2` turns on, `Q5`'s gate is pulled to
ground, and `Q5` connects `VBAT_L0` to `VBAT_DET`. Unplugged, `R9` holds `Q2`
off and `R45` holds `Q5` off. The full analysis, including why the circuit is
built this way and where `VBAT_DET` goes, is in the
[SK2301AAT record §3](../sk2301aat/README.md#3-what-it-actually-switches-sch-v).

The gate is driven by **a power rail, not a GPIO** — the detection is automatic
and works before firmware runs.

### 3.2 `Q3`, sheet 4 — the buzzer driver

This is a textbook low-side inductive-load driver, and reading it settles what
three other parts on sheet 4 are for.

```
                       3V3_L1
                          │
                    ┌─────┴─────┐
                    │  BUZZER1  │  "ER103", magnetic
                    │  + ─── −  │
                    └──┬─────┬──┘
                       │     │
                D3 ────┘     │      1N4148WS, cathode to +, anode to −
             (flyback)       │
                             │
  G42_BB_PWM ──┬── Q3 pin 1 GATE
               │   Q3 pin 3 DRAIN ──┘
          R50 10 kΩ
               │   Q3 pin 2 SOURCE ── GND
              GND
```

| `Q3` terminal | Net |
|---|---|
| pin 1 **GATE** | **`G42_BB_PWM`** — ESP32-S3 **GPIO42**, with **`R50` = 10 kΩ** pulldown |
| pin 2 **SOURCE** | **GND** |
| pin 3 **DRAIN** | the buzzer's **`−`** terminal |

The buzzer's `+` terminal sits on **`3V3_L1`**, and **`D3`**
([1N4148WS](../1n4148ws/README.md)) is connected across the buzzer with its
**anode on `Q3`'s drain and its cathode on the `3V3_L1` side** — the classic
**flyback/freewheel diode** for an inductive load. **[SCH-V]**

Three things follow that are useful when writing firmware or debugging:

1. **`R50` = 10 kΩ is a gate pulldown, and it matters.** GPIO42 is high-Z during
   reset and while the ESP32-S3 is held in reset by the
   [M5PM1](../../m5stack/m5pm1/README.md). Without the pulldown the buzzer could
   chirp on every boot. With it, the buzzer is silent unless firmware drives the
   pin. **[INF]**
2. **The buzzer runs from `3V3_L1`, not `3V3_L2`.** `3V3_L1` is a different power
   domain from the main system rail, so **the buzzer's availability is tied to
   `L1` being enabled**, independent of whether the application rail is up. Check
   [`power-architecture.md`](../../../devices/m5stack/papermono/power-architecture.md)
   before assuming a beep will sound in a given power state.
3. **The buzzer symbol carries an explicit no-connect marker** (a red ✗) on one
   of its terminals. That is a *positive assertion by the designer*, not an
   omission — unlike the USB-C `SBU` stubs, which are simply left open. **[SCH-V]**

### 3.3 Operating conditions — both instances are heavily de-rated

| Parameter | Rating | `Q2` (sheet 2) | `Q3` (sheet 4) |
|---|---|---|---|
| V<sub>DS</sub> | 20 V | ≤ 4.35 V | ≤ 3.3 V + flyback (clamped by `D3`) |
| **V<sub>GS</sub>** | **±8 V** | ≤ 5.5 V (`VUSB_IN`) | ≤ 3.3 V |
| I<sub>D</sub> | 2.1 A | ~µA | a magnetic buzzer, tens of mA |
| P<sub>D</sub> | 0.35 W | ~0 | ≪ |

`Q2`'s gate sees `VUSB_IN`, which is USB V<sub>BUS</sub> **before** the
[AW32901FCR](../../awinic/aw32901/README.md) OVP switch. That switch trips at
**5.95 V**, so a fault could present up to that before it acts — still inside the
±8 V V<sub>GS</sub> rating, but the margin is **1.3×**, not the comfortable 2.4×
it looks like at nominal 5 V. It is the tightest rating on either instance.
**[INF]**

---

## 4. Substitution

`2302` is a de-facto industry number for a small N-channel MOSFET.

| Alternative | Package | Note |
|---|---|---|
| Vishay **Si2302CDS**, AOS **AO3400A** ([documented here](../../alpha-and-omega-semiconductor/ao3400a/README.md)), Diodes **DMN2075U** | **SOT-23** | Electrically equal or better; **larger footprint** |
| UMW / Slkor / CJ `2302` parts | SOT-23 or SOT-523 | Chinese second sources; check the package suffix |
| **Any SOT-523 N-channel ≥ 20 V, low-V<sub>GS(th)</sub>** | SOT-523 | What matters here |

Required: **N-channel**, V<sub>DS</sub> ≥ 20 V, **V<sub>GS</sub> ≥ ±8 V**,
logic-level threshold (must be fully on at 3.3 V of drive), pin order
**1 = G, 2 = S, 3 = D**.

---

## 5. Integration pitfalls

1. **`SK2301AAT` and `SK2302AAT` differ by one digit and by channel type**, share
   a package and share a pinout. Both are on this board, on adjacent sheets. This
   is the most likely rework error involving either part.
2. **V<sub>GS</sub> = ±8 V** and `Q2`'s gate is on raw USB V<sub>BUS</sub>
   (§3.3) — the tightest margin on the part.
3. **`R50` is not optional** (§3.2). Removing it makes the buzzer sensitive to
   the GPIO's reset state.
4. **`D3` is not optional either.** A magnetic buzzer is inductive; without the
   flyback diode the drain sees a spike well beyond 20 V at turn-off.
5. **The buzzer sits on `3V3_L1`**, a different domain from the system rail
   (§3.2).
6. **The body diode conducts when off.** `Q3`'s drain cannot be pulled below
   about −0.7 V without conducting into ground.

---

## 6. Open questions

- **What consumes `VBAT_DET`** — see the
  [SK2301AAT record §4](../sk2301aat/README.md#4-where-vbat_det-goes--not-established).
- The buzzer's own part (`ER103`) is **unidentified**, so its inductance,
  resonant frequency and current draw are unknown, and with them the actual
  switching stress on `Q3`.
- Whether M5Stack's firmware drives GPIO42 as a square wave or with a PWM duty —
  the net is named `G42_BB_PWM`, implying PWM, but this was not read from source.
- No measurement of anything.

---

## Manufacturer

**Shikues.** No vendor sourcing guide exists in this repository yet.

**⚠ Retrieval finding — this part is the clean demonstration of the LCSC trap.**
LCSC's own catalogue gave the datasheet URL as
`https://www.lcsc.com/datasheet/lcsc_datasheet_2003311817_Shikues-SK2302AAT_C475757.pdf`.
That URL returned **HTTP 200** and **47 038 bytes beginning `<!doc`** — an HTML
page under a `.pdf` name. Five different user-agents (Chrome 131, ClaudeBot,
WhatsApp, ChatGPT-User, plain `curl`) all got the same HTML. **No user-agent
rotation helps, because it is not bot-blocking — it is the wrong host.**

Rewriting to the CDN worked first try:

```
https://www.lcsc.com/datasheet/lcsc_datasheet_2003311817_Shikues-SK2302AAT_C475757.pdf   -> HTML
https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2003311817_Shikues-SK2302AAT_C475757.pdf  -> %PDF ✓
```

**Check the `%PDF` magic bytes; the status code and the file extension both lie.**
`executed-success`, 2026-09-01, reproduced on five parts from this board. This
belongs in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md) and
confirms the finding first recorded in the
[IP2315 record](../../injoinic/ip2315/README.md#manufacturer).

## Related pages

- [Shikues SK2301AAT](../sk2301aat/README.md) — **`Q5`, the P-channel half of the `Q2` switch**
- [1N4148WS](../1n4148ws/README.md) — **`D3`, the buzzer flyback diode**
- [AOS AO3400A](../../alpha-and-omega-semiconductor/ao3400a/README.md) — comparable N-channel documented here
- [Changjing CJ2310](../../changjing/cj2310/README.md) — the board's other N-channel, in the e-paper bias converter
- [PaperMono power architecture](../../../devices/m5stack/papermono/power-architecture.md) · [bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| D1 | `SK2302AAT` SOT-523 Plastic-Encapsulate MOSFET | Shikues (via LCSC CDN) | primary, via distributor mirror | <https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2003311817_Shikues-SK2302AAT_C475757.pdf> | 2026-09-01 | **REV.08**, 4 pp | channel type, SOT-523, marking `A2S`, **pin 1 = G / 2 = S / 3 = D**, all §1 maxima | `artifacts/sk2302aat-shikues-lcsc-mirror.pdf` |
| C1 | LCSC entry `C475757` | LCSC / JLCPCB | distributor | JLCPCB SMT parts API, keyword `SK2302AAT` | 2026-09-01 | — | manufacturer; 70 mΩ @ 2.5 V; V<sub>GS(th)</sub> 650 mV; the (broken) `www.lcsc.com` datasheet URL of the Manufacturer note | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | both instances; §3.1 and §3.2 topologies; `R9`, `R45`, `R50` values; `D3` orientation; the buzzer's no-connect marker | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/sk2302aat-shikues-lcsc-mirror.pdf` | 499 935 | `88f31ab70e4f6630b1d15e5a6f9a5f1e6ae713b40b503a4fa389a91fffed69aa` | 4 |

**Method note.** D1 validated as `%PDF` (`executed-success`) with an intact text
layer. Both circuits in §3 were read from 200 dpi renders rather than from the
text layer, which in both regions attaches labels to neighbouring designators; the
`D3` orientation in particular is only legible from the image.
