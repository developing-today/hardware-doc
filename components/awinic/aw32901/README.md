# Awinic AW32901FCR

> Over-voltage-protection **load switch with surge protection** — an integrated low-R<sub>DS(on)</sub> nFET in series with the USB input, which opens in ~50 ns when the input exceeds a fixed 5.95 V threshold, and survives 120 V surges and 29 V DC.
> Research snapshot **2026-09-01**. Fitted as **`U2`** on sheet 2 of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153), in the sheet block labelled `PROTECTION`. **No hardware was available.**

> ⚠ **This is not a battery-protection IC.** It is an *input* over-voltage protection switch, sitting between the USB-C connector and the charger. The distinction matters: it protects the board from the adapter, not the cell from the board. Cell protection on this design is whatever is inside the pack, plus the charger's own limits.

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Awinic `AW329XX` datasheet **V1.3**, December 2021 — local copy `artifacts/aw329xx-datasheet-en-v1.3.pdf` | `not-tested` |
| **[VP]** | Awinic product page for `AW32901FCR`, retrieved 2026-09-01 | `not-tested` |
| **[SCH]** | `PaperMono_SCH_V0.6.2_20260522.pdf`, sheet + designator + pin | `executed-success` for the extraction; `not-tested` electrically |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Ordering part | **`AW32901FCR`** | **[SCH]** sheet 2, `U2`; **[VP]** |
| Manufacturer | **Shanghai Awinic Technology Co., Ltd.** (上海艾为电子) | **[DS]** |
| Product-page category | *"OVP with surge protection"* → *"Over-Voltage Protection Load Switch with Surge Protection"* | **[VP]** |
| Package | **FCQFN-12, 1.3 mm × 1.8 mm** (12 balls, A1–A4 / B1–B4 / C1–C4) | **[VP]**, **[DS]** |
| Datasheet | **`DS_AW329XX_EN_V1.3`**, December 2021, 19 pp — covers the whole AW329xx family | **[DS]** cover |
| Lifecycle | Active | **[VP]** |

### 1.1 Family — the suffix *is* the OVP threshold **[DS Device Comparison Table]**

The parts are identical apart from the default over-voltage trip point, so a substitution changes the protection level and nothing else:

| Part | V<sub>IN_OVLO</sub> min | **typ** | max | Hysteresis |
|---|---:|---:|---:|---:|
| **AW32901** | 5.83 V | **5.95 V** | 6.07 V | 130 mV |
| AW32902 | 6.08 V | 6.20 V | 6.32 V | 130 mV |
| AW32905 | 6.66 V | 6.80 V | 6.94 V | 140 mV |
| AW32909 | 9.78 V | 9.98 V | 10.18 V | 210 mV |
| AW32910 | 10.29 V | 10.50 V | 10.71 V | 210 mV |
| AW32912 | 13.7 V | 14.0 V | 14.3 V | 280 mV |

The threshold is additionally **adjustable from 4 V to 24 V** through the `OVLO` pin. **[DS]**

---

## 2. Key limits **[DS Absolute Maximum Ratings, VP Parameters]**

| Parameter | Value |
|---|---|
| `IN` absolute maximum | **29 V** DC |
| `OUT`, `OVLO`, `ACOK`, `EN` absolute maximum | 6 V |
| Surge withstand (internal clamp) | **> 120 V**, IEC 61000-4-5 |
| Continuous switch current `IN`→`OUT` | **5 A** |
| Peak current (10 ms) | 8 A |
| Body-diode continuous forward current | 1.5 A |
| R<sub>DS(on)</sub> typical | **27 mΩ** |
| OVP response time | **≈50 ns** typical |
| System ESD | ±8 kV contact, ±15 kV air (IEC 61000-4-2) |
| Ambient / junction temperature | −40 to +85 °C / −40 to +150 °C |
| Other protections | Over-temperature (OTP), under-voltage lockout (UVLO) |

---

## 3. Pinout **[DS Pin Configuration, FCQFN-12]**

|  | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **A** | `EN` | `OUT` | `OUT` | `GND` |
| **B** | `ACOK` | `OUT` | `IN` | `GND` |
| **C** | `OVLO` | `IN` | `IN` | `GND` |

| Pin | Function **[DS Pin Definition]** |
|---|---|
| `EN` (A1) | Enable, **active low** |
| `ACOK` (B1) | Open-drain status: pulled **low** while V<sub>IN_UVLO</sub> < V<sub>IN</sub> < V<sub>IN_OVLO</sub>; otherwise Hi-Z |
| `OVLO` (C1) | OVP threshold adjustment |
| `IN` / `OUT` / `GND` | Power path |

> ⚠ **`OVLO` must not float.** To use the default threshold the datasheet requires **`R2 = 0 Ω`, `R1 = NC`, `OVLO` connected directly to GND**, and states explicitly *"OVLO pin cannot be left floating."* **[DS]** The two-resistor divider is only for a custom threshold.

The datasheet also notes that if an external TVS is fitted, its **clamping voltage must be below 34 V**, and that a design relying on the AW329xx alone must account for the 29 V `IN` rating. **[DS]**

---

## 4. Used By

### `devices/m5stack/papermono`

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md), designator **`U2`**, schematic sheet 2, in the block silkscreened `PROTECTION`. The sheet carries the annotation **`OVP = 5.95V`** next to it, confirming the default threshold is in use. **[SCH]**

**Position in the power chain:**

```
USB-C  ──►  VUSB_IN  ──►  [ AW32901FCR  U2 ]  ──►  5V_IN  ──►  [ IP2315  U1 ]  ──►  VBAT_L0
                              OVP 5.95 V                          charger
                                                     VBAT_L0 ──(R20 = 0 Ω)──► VBUS_L0  ──► all downstream rails
```

**Net-by-net [SCH]:**

| Ball | Name | Net |
|---|---|---|
| B3, C2, C3 | `IN` | `VUSB_IN` (from the USB-C connector, behind `TVS1` = `ESD5311`) |
| A2, A3, B2 | `OUT` | **`5V_IN`** → [IP2315](../../injoinic/ip2315/README.md) `VIN` (pins 20/21) |
| A1 | `EN` (active low) | local network with `R10` = `0 Ω/1%` |
| B1 | `ACOK` | local network with `R6` = `NC/1%` — status **not routed to any processor** |
| C1 | `OVLO` | network with `R10`/`R11`/`R12`; default threshold in use per the sheet annotation |
| A4, B4, C4 | `GND` | `GND` |
| — | decoupling | `C5` = `1 µF/25 V` input, `C6` = `1 µF/25 V` output |

**Consequences for this board — both worth knowing before debugging a charge fault:**

1. **`ACOK` goes nowhere.** No MCU can read "input present and in range". Firmware infers input state from the [M5PM1](../../m5stack/m5pm1/README.md)'s `5VIN_ADC` / `BAT_ADC` measurements instead. If the AW32901 has tripped, the symptom is simply "no charging" with no dedicated flag. **[INF]**
2. **The 5.95 V threshold makes the IP2315's fast-charge feature unreachable.** The charger downstream advertises 9 V and 12 V PD/FCP/AFC/PE+ negotiation, but this switch opens above ~5.95 V, so those voltages could never reach it. The PaperMono also leaves the IP2315's CC series resistors (`R1`, `R2`) unpopulated, so negotiation is disabled at both ends. See [IP2315 §4.1](../../injoinic/ip2315/README.md#41--pd-is-depopulated--this-is-a-5-v-charger-in-practice). **[INF]**
3. **A 5 A-rated switch on a ~1 A path** — the part is heavily over-specified for a 1150 mAh device, and is presumably chosen for the surge/ESD spec and the small FCQFN footprint rather than the current rating. **[INF]**

---

## 5. Drivers and libraries

**Not applicable — this is a passive-control analogue part.** It has no bus interface and no registers. Its only host-visible signal, `ACOK`, is unconnected on the PaperMono (§4).

---

## 6. Integration pitfalls

1. **`OVLO` must be tied — never floated** (§3). With the default threshold, tie it to GND directly or through 0 Ω.
2. **`EN` is active low.** An accidentally floating or pulled-high `EN` leaves the switch off, presenting as "the board will not charge and draws nothing from USB."
3. **The part number encodes the threshold** (§1.1). Substituting an AW32905 for an AW32901 raises the trip point from 5.95 V to 6.8 V — a silent, board-level safety change.
4. **A downstream TVS must clamp below 34 V** to stay inside the `IN` rating (§3).
5. **The body diode conducts backwards at up to 1.5 A** even when the switch is off; this is not a reverse-current blocker.

---

## 7. Alternatives

| Part | vs. AW32901FCR | When |
|---|---|---|
| AW32902 / AW32905 / AW32909 / AW32910 / AW32912 | Same silicon, higher OVP threshold | When the design *does* want 9 V or 12 V fast charge |
| TI **TPD4S014** / **TPS2596** | Comparable OVP/eFuse class, US-vendor documentation | Where Awinic sourcing or documentation is a problem |
| Discrete PMOS + comparator | Cheaper in BOM cost only | Loses the 120 V surge clamp and the 50 ns response |

---

## 8. Open questions

- Exactly which of `R10`/`R11`/`R12` sits on `OVLO` versus `EN` on the PaperMono was not resolved from the PDF text layer; the sheet's `OVP = 5.95V` annotation establishes that the **default** (grounded `OVLO`) configuration is in use, which is the fact that matters.
- Whether `ACOK` is intentionally unused or a lost opportunity; the vendor has not commented.
- No hardware measurement of the trip point or of R<sub>DS(on)</sub>.

---

## Manufacturer

**Shanghai Awinic Technology Co., Ltd.** No vendor sourcing guide exists in this repository yet. The retrieval recipe that worked on 2026-09-01, recorded because Awinic's site gives no obvious download link:

1. `https://www.awinic.com/{cn|en}/productDetail/<FULL-ORDERING-PART>` — the **full** ordering part number (`AW32901FCR`), not the base part (`AW32901`), which silently returns the home page.
2. The page contains `data-file-url="doc/<YYYYMM>/<uuid>.pdf"` and `data-doc-title="DS_..."`.
3. Download via `https://www.awinic.com/en/download?file=<urlencoded file>&fileName=<urlencoded title>`.

Plain `curl` with a Chrome 131 User-Agent was sufficient; no fallback User-Agent was needed, and no login is required.

## Related pages

- [Injoinic IP2315](../../injoinic/ip2315/README.md) — the charger immediately downstream
- [Awinic AW35122](../aw35122/README.md) · [AW39112](../aw39112/README.md) · [AW9967](../aw9967/README.md) — the other Awinic parts on this board
- [Generic charger / power-path record](../../generic/charger-power-path/README.md)
- [Generic USB-C interface record](../../generic/usb-c-interface/README.md)

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | AW329XX datasheet | Awinic | primary | datasheet | `https://www.awinic.com/en/download?file=doc/20230609wm/6a5a084d-01eb-4146-9a40-a6e6608f0e79.pdf&fileName=DS_AW329XX_EN_V1.3` | 2026-09-01 | **V1.3**, Dec 2021, 19 pp, 575 578 B | Threshold table, absolute maxima, pin map, `OVLO` grounding requirement, TVS clamp limit | `artifacts/aw329xx-datasheet-en-v1.3.pdf` |
| D2 | AW32901FCR product page | Awinic | primary | official page | <https://www.awinic.com/en/productDetail/AW32901FCR> | 2026-09-01 | — | Category, package `FCQFN 1.3X1.8-12L`, 27 mΩ R<sub>DS(on)</sub>, 5 A, 120 V surge, 50 ns, 29 V DC | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | schematic | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | `U2` net assignments, `OVP = 5.95V` annotation, `R6`/`R10` values | `devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/aw329xx-datasheet-en-v1.3.pdf` | 575 578 | `2dfda61d8aadf8ef8655ede785eb92f38979e1260e68d295ed9756645208b2d1` | 19 |

**Method note.** D1 validated as `%PDF`, 19 pages, text layer intact. The document is watermarked *"Awinic Confidential"* in the page background but is served publicly from the vendor's own site without login.
