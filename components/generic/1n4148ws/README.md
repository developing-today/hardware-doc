# 1N4148WS — small-signal switching diode (maker **not specified by the schematic**)

> **The industry-standard 100 V / 150 mA fast switching diode**, 4 ns reverse recovery, in **SOD-323**.
> Research snapshot **2026-09-01**. Fitted as **`D3` on sheet 4** of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) — the **flyback clamp across the buzzer**. One instance.
> **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Jiangsu Changjing `1N4148WS` datasheet, local copy `artifacts/1n4148ws-changjing-lcsc-mirror.pdf` | `not-tested` |
| **[CAT]** | LCSC / JLCPCB catalogue entries `C2128`, `C57759`, retrieved 2026-09-01 | `not-tested` |
| **[SCH-V]** | Read off sheet 4 rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Value string on the schematic | **`1N4148WS`** | **[SCH-V]** |
| Manufacturer | **not specified** — §1.1 | — |
| Function | Fast small-signal switching diode | **[DS]** |
| Package | **SOD-323** | **[DS]** |
| V<sub>R</sub> | **100 V** (Changjing) / **75 V** (ST) — §1.1 | **[CAT]** |
| I<sub>F</sub> continuous | **150 mA** | **[CAT]** |
| I<sub>FSM</sub> | **2 A** (Changjing) / 350 mA (ST) | **[CAT]** |
| V<sub>F</sub> | 1.25 V @ 150 mA | **[CAT]** |
| I<sub>R</sub> | 1 µA @ 75 V | **[CAT]** |
| P<sub>D</sub> | 200 mW | **[CAT]** |
| **t<sub>rr</sub>** | **4 ns** | **[CAT]** |

### 1.1 `1N4148WS` is a JEDEC type, not a vendor part

`1N4148` is one of the oldest and most widely second-sourced part numbers in
electronics; `WS` denotes the SOD-323 package. **Dozens of makers produce it**,
and the schematic prints only the type number. LCSC alone lists at least two:

| Maker | LCSC | V<sub>R</sub> | I<sub>FSM</sub> |
|---|---|---|---|
| **Jiangsu Changjing** | `C2128` | **100 V** | **2 A** |
| ST (Semtech) | `C57759` | 75 V | 350 mA |

**[CAT]**

The Changjing part is held here as the representative datasheet, on the reasoning
that **M5Stack demonstrably buys Changjing discretes for this board** — the same
sheet carries [`CJ2310`](../../changjing/cj2310/README.md) and sheet 2 carries
[`CJ3439KDW`](../../changjing/cj3439kdw/README.md). **That is a plausibility
argument, not an identification, and no maker is asserted.** What would resolve
it: the top marking on an assembled board, or M5Stack's BOM.

The spread matters a little: **75 V vs 100 V** of reverse rating and **350 mA vs
2 A** of surge. Both are far beyond what this circuit needs (§2.1), so the
ambiguity has no practical consequence *here* — but it would if the part were
reused somewhere more demanding.

---

## 2. Used By

### `devices/m5stack/papermono` — `D3`, sheet 4

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md).
**One instance**, and it is the board's only `1N4148`-type part; the three
Schottkys in the e-paper bias converter are
[`1N5819WS`](../1n5819ws/README.md) and the frontlight rectifier is a
[ROHM part](../../rohm/rb162vam-20tr/README.md).

**On the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md):**
`inferred` **yes** — the Lite retains the buzzer, and differs only in dropping
NFC and LoRa. Not read from the Lite's own schematic.

### 2.1 Circuit role — the buzzer flyback clamp **[SCH-V]**

```
              3V3_L1
                 │
          ┌──────┴──────┐
          │   BUZZER1   │   "ER103", magnetic buzzer
          │   +      −  │
          └───┬──────┬──┘
              │      │
       cathode│      │
             D3      │       1N4148WS, across the buzzer
        anode │      │
              └──────┤
                     │
                Q3 drain (SK2302AAT, N-channel)
                Q3 gate ── G42_BB_PWM   (R50 10 kΩ pulldown)
                Q3 source ── GND
```

| `D3` terminal | Net |
|---|---|
| **anode** | `Q3`'s **drain** — the buzzer's `−` terminal |
| **cathode** | the buzzer's `+` terminal, i.e. **`3V3_L1`** |

A magnetic buzzer is an inductive load. When
[`Q3`](../sk2302aat/README.md) turns off, the coil's current must keep flowing;
without a path it develops whatever voltage is needed to find one, which on a
20 V MOSFET is an avalanche event on every cycle. `D3` gives that current a path
back into the supply, clamping the drain to about **`3V3_L1` + 0.8 V ≈ 4.1 V**.

**This is why the part is a `1N4148` and not a Schottky.** The recovery speed
(4 ns) matters more than the forward drop, because the diode conducts once per
PWM edge; and the drop itself is *desirable* here — a higher clamp voltage
collapses the coil current faster, which makes the buzzer louder for a given
drive. A Schottky would clamp lower and damp the tone. **[INF]**

### 2.2 Operating conditions — de-rated to the point of irrelevance

| Parameter | Rating | On this board | Margin |
|---|---|---|---|
| V<sub>R</sub> | 75–100 V | ≤ 3.3 V | **≥ 22×** |
| I<sub>F</sub> | 150 mA | a small magnetic buzzer's coil current, tens of mA | comfortable |
| I<sub>FSM</sub> | 0.35–2 A | the flyback pulse, ≈ the coil's peak current | comfortable |
| P<sub>D</sub> | 200 mW | ≈ V<sub>F</sub> × I × duty, a few mW | ≫ |

The part is chosen for ubiquity and cost, not for its ratings. That is the
correct engineering call.

---

## 3. Notes for firmware

- **The buzzer runs from `3V3_L1`**, not from the main `3V3_L2` system rail. Its
  availability is tied to the `L1` domain being enabled — see
  [`power-architecture.md`](../../../devices/m5stack/papermono/power-architecture.md).
- **`G42_BB_PWM` is ESP32-S3 GPIO42**, with `R50` = 10 kΩ holding `Q3` off during
  reset. The buzzer should be silent until firmware drives it.
- **The buzzer symbol carries an explicit red ✗ no-connect** on one terminal —
  a positive assertion by the designer, not an omission. **[SCH-V]**
- The buzzer's own part, **`ER103`, is unidentified**, so its resonant frequency
  is unknown. Driving a magnetic buzzer off resonance is dramatically quieter;
  finding the right frequency will be empirical.

---

## 4. Substitution

Any `1N4148W`-family part in SOD-323 works. `1N4148WS`, `1N4148W` (SOD-123),
`LL4148` (MiniMELF), `BAV70`/`BAV99` (dual, SOT-23) are all the same junction in
different bodies.

**Do not substitute a Schottky** (`BAT54`, `1N5819`) without thinking: it will
work as a clamp, but it lowers the clamp voltage and changes the buzzer's
acoustic output (§2.1).

---

## 5. Open questions

- **The maker actually fitted** (§1.1).
- The buzzer `ER103`'s identity, coil inductance and resonant frequency — the
  determinant of both the flyback energy and the drive strategy.
- Whether firmware drives GPIO42 as a fixed square wave or a variable-duty PWM.
- No measurement of anything.

---

## Manufacturer

**Not specified by the schematic** (§1.1). The retained datasheet is Jiangsu
Changjing's; see the [CJ2310](../../changjing/cj2310/README.md#manufacturer) and
[CJ3439KDW](../../changjing/cj3439kdw/README.md#manufacturer) records for that
vendor's document-sourcing notes.

**⚠ Retrieval finding — the LCSC PDF host trap.** LCSC's catalogue gave
`https://www.lcsc.com/datasheet/lcsc_datasheet_1810101110_…1N4148WS_C2128.pdf`,
which returned **HTTP 200 and 67 606 bytes of HTML** to all five user-agents
tried. The CDN rewrite worked first try:

```
wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/1810101110_Jiangsu-Changjing-Electronics-Technology-Co---Ltd--1N4148WS_C2128.pdf
```

**Check the `%PDF` magic bytes; the status code and the `.pdf` extension both
lie.** `executed-success`, 2026-09-01, reproduced across five parts from this
board. This belongs in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

## Related pages

- [Shikues SK2302AAT](../sk2302aat/README.md) — **`Q3`, the buzzer driver `D3` protects**
- [1N5819WS](../1n5819ws/README.md) — the board's Schottky, three instances, e-paper bias
- [ROHM RB162VAM-20TR](../../rohm/rb162vam-20tr/README.md) — the board's other rectifier
- [PaperMono bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md) · [power architecture](../../../devices/m5stack/papermono/power-architecture.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| D1 | `1N4148WS` switching diode datasheet | Jiangsu Changjing (via LCSC CDN) | representative primary, via distributor mirror | <https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/1810101110_Jiangsu-Changjing-Electronics-Technology-Co---Ltd--1N4148WS_C2128.pdf> | 2026-09-01 | undated, 2 pp | SOD-323, 100 V, 150 mA, 4 ns — **for the Changjing part, which is not confirmed to be the fitted one** (§1.1) | `artifacts/1n4148ws-changjing-lcsc-mirror.pdf` |
| C1 | LCSC entries `C2128`, `C57759` | LCSC / JLCPCB | distributor | JLCPCB SMT parts API, keyword `1N4148WS` | 2026-09-01 | — | the §1.1 multi-vendor spread; V<sub>F</sub>, I<sub>R</sub>, P<sub>D</sub>, t<sub>rr</sub> | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | `D3` = `1N4148WS`; the §2.1 orientation and topology; `3V3_L1` supply; `R50` = 10 kΩ; the no-connect marker | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/1n4148ws-changjing-lcsc-mirror.pdf` | 774 532 | `59e951bd3155eb4a94e958d10edc3b7d17325f38cf06784cac07fbcc9fcabf2e` | 2 |

**Method note.** D1 validated as `%PDF` (`executed-success`). The **diode's
orientation** in §2.1 — which is the entire content of this record, since the part
itself is a commodity — is legible only from a rendered page image; the text layer
places `D3`, `Q3`, `BUZZER1` and `C58` labels in one cluster and cannot resolve
which terminal is which.
