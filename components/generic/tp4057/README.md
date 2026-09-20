# TP4057 — 500 mA linear Li-ion battery charger

- **Category:** single-cell Li-ion constant-current / constant-voltage linear charger, SOT23-6.
- **Manufacturer:** **unresolved from the mirrored datasheet.** The document M5Stack serves has
  no vendor name or logo on page 1. TP4057 is a widely second-sourced Chinese part; filed under
  `generic/` rather than asserting a maker.
- **Retrieved:** 2026-09-04

The battery charger of the M5Stack DinMeter (`U2`), and of many M5Stack products.

---

## 1. Identity and headline specification

| Property | Value | Evidence |
|---|---|---|
| Part | **TP4057** | datasheet cover; DinMeter schematic `U2` value text |
| Package | **SOT23-6** | datasheet |
| Function | complete linear Li-ion charger, **no external MOSFET, sense resistor or blocking diode** | datasheet |
| Max programmable charge current | **500 mA** | datasheet |
| **Float voltage** | **4.24 V ±1 %** | datasheet — **note: 4.24 V, not the usual 4.2 V** |
| Charge current | set by an external resistor on `PROG` | datasheet |
| Termination | when current falls to 1/10 of the programmed value | datasheet |
| Sleep current (input removed) | battery drain **< 1 µA** | datasheet |
| Shutdown quiescent | 25 µA | datasheet |
| Other features | thermal regulation (folds back current when hot), battery-temperature monitoring, UVLO, auto-recharge, **two status pins** (`CHRG`, `STDBY`) | datasheet |
| Pins | `VCC`, `BAT`, `CHRG`, `STDBY`, `PROG`, `GND` | datasheet; DinMeter schematic `U2` |

**Language.** The mirrored datasheet is **Chinese only**; no English version was located. It is
therefore the primary source and is retained in the repository.

The **4.24 V** float is worth flagging: it is above the 4.20 V nominal many cells specify. It is
the part's documented behaviour, not a board choice.

## 2. Artifacts

| File | Size | SHA-256 | Language | Licence | Redistribution | Disposition |
|---|---:|---|---|---|---|---|
| [`artifacts/tp4057-datasheet-cn-m5stack-mirror.pdf`](artifacts/tp4057-datasheet-cn-m5stack-mirror.pdf) | 628 588 | `c949a7c3ef589ca575b2eaecd454f901e81f6b0896e6a706fa8cb4157aa0377b` | zh-CN | unknown | `unknown` | `repository` |

Retrieved 2026-09-04 from
`https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/core/M5DinMeter/tp4057.pdf`
(HTTP 200, `%PDF` validated). Renamed from upstream `tp4057.pdf` to record that it is an
M5Stack mirror rather than a vendor-hosted copy — no vendor host was located. Linked from **both**
DinMeter documentation pages. Note the URL path is under `products/core/M5DinMeter/`: M5Stack
files this chip datasheet under the *board*, which is exactly the filing error this repository's
convention avoids — it lives here, under the component.

---

## Used By

### M5Stack DinMeter (K134) and DinMeter v1.1 (K134-V11)

Fitted as **`U2`**. Input from `+5VIN` (the [ME3116AM6G](../../microne/me3116am6g/README.md)
buck output or USB), output to `VBAT_IN` on the 1.25 mm 2-pin battery connector `J2`. Programme
resistor `R13` = **3.3 kΩ**; M5Stack specifies the resulting charge current as **100 mA**
(charging a 250 mA·h bundled cell at ~0.4 C). Status pins drive indicator LEDs
`D1`/`D2`/`D3` through `R17`/`R19` (10 kΩ / 100 kΩ). Decoupling `C15` 10 µF, `C21` 10 µF.

The charger sits *upstream* of the battery power path (`Q3`/`Q6` AP40P05 P-FETs) and the boost
converter, so charging and running are independent.

→ [`devices/m5stack/dinmeter/features/power-and-battery.md`](../../../devices/m5stack/dinmeter/features/power-and-battery.md)
→ [`devices/m5stack/dinmeter/pinouts-and-buses.md` §4](../../../devices/m5stack/dinmeter/pinouts-and-buses.md#4-power-tree-and-the-latch)

### M5Stack Cardputer v1.0, v1.1 and ADV

Designator **U1** on all three (the v1.0/v1.1 share one published schematic file, SHA-256
`6016c1fe…`). `+5VIN` → R1 **0.8 Ω** → `VCC`; `BAT` → `VBAT_IN`; `PROG` → **R5 3.3 kΩ**;
`CHRG` and `STDBY` status outputs; C6 10 µF on `BAT`.

Charge current **inferred** at roughly **300 mA** from `R_PROG = 3.3 kΩ` and the family's usual
`I = 1000 × V_PROG / R_PROG` relation. **Not measured, and no datasheet was consulted for this
board** — treat as an order-of-magnitude figure.

⚠ **R3 (1 kΩ) and D3 (an LED) beside the charger are drawn greyed out — depopulated.** A charge
indicator the production board does not fit. That is a positive DNP marking, not an omission.

⚠ M5Stack states on **all three** product pages that **the side power switch must be ON to
charge**. This is the most repeated warning in the family's documentation and the most likely
cause of a "my Cardputer won't charge" report.

Records: [v1.0](../../../devices/m5stack/cardputer-v1.0/README.md) ·
[v1.1](../../../devices/m5stack/cardputer-v1.1/README.md) ·
[ADV](../../../devices/m5stack/cardputer-adv/README.md)

⚠ **Note the disagreement with the DinMeter entry above**, which cites the same part with
`R_PROG = 3.3 kΩ` and a vendor-stated **100 mA**. Both figures are recorded as their sources
give them; they are not reconciled here. Logged in
[`scratch/index-merge/corrections-requiring-review.md`](../../../scratch/index-merge/corrections-requiring-review.md).

*Added 2026-09-07 from `scratch/m5stack-cardputer/index-fragments.md` §3.7.*
