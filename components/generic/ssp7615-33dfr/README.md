# SSP7615-33DFR — 3.3 V / 400 mA CMOS LDO

> High-accuracy, low-noise, low-dropout CMOS linear regulator: **1.5–8 V in, 400 mA at 3.3 V out, 200 mV dropout at 100 mA, 0.5 µA quiescent current**, with an active-high enable and built-in fold-back short-circuit protection, in a DFN 1 × 1 mm four-pad package.
> Research snapshot **2026-09-01**. Fitted **four times** on the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) — it produces `3V3_L0`, `3V3_L1`, `3V3_L2_LoRa` and `EPD_3V3_L3B`, i.e. four of the board's five 3.3 V-class rails. **No hardware was available.**

> **Filing note.** This record lives under `components/generic/` as the tree was laid out, but the part is **not** generic: a datasheet was obtained and the manufacturer is **Shanghai Siproin Microelectronics Co., Ltd.** (上海矽普微电子). A future reorganisation should move it to `components/siproin/ssp7615-33dfr/`; it is left here so that existing links keep working. The manufacturer identification is a finding of this pass, not an assumption.

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Siproin `SSP7615` datasheet **V1.3 (English)** — local copy `artifacts/ssp7615-datasheet-v1.3-en.pdf` | `not-tested` |
| **[SCH]** | `PaperMono_SCH_V0.6.2_20260522.pdf`, sheet + designator + pin | `executed-success` for the extraction; `not-tested` electrically |
| **[SRC]** | M5Stack source at a cited `file:line` | `executed-success` for the read |
| **[DOC]** | `docs.m5stack.com`, retrieved 2026-09-01 | `not-tested` |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity and part numbering

| Property | Value | Evidence |
|---|---|---|
| Base part | **`SSP7615`** | **[DS]** cover |
| Ordering part as fitted | **`SSP7615-33DFR`** | **[SCH]** sheet 2 |
| Manufacturer | **Shanghai Siproin Microelectronics Co., Ltd.** | **[DS]** footer, every page |
| Function | High-accuracy, low-noise, high-speed CMOS linear voltage regulator | **[DS]** |
| Datasheet | **V1.3**, English, 13 pp | **[DS]** footer |

### 1.1 Decoding the suffix **[DS Ordering Information]**

```
SSP7615 - 33 DF R [G]
          │   │  │  └── Halogen free
          │   │  └───── RoHS / Pb free
          │   └──────── Package:  M = SOT23-3
          │                       M5 = SOT23-5
          │                       DF = DFN 1 × 1 - 4
          └──────────── Output voltage, integer form (1.2 – 5.0 V)
```

So **`SSP7615-33DFR`** = **3.3 V output, DFN 1 × 1-4 package, RoHS/Pb-free**. The output voltage is fixed at manufacture; there is no adjust pin and no divider.

> ⚠ **Only the SOT23-5 and DFN packages have an enable pin.** The SOT23-3 variant is `GND` / `VOUT` / `VIN` only. A footprint change between package options is therefore also a *functional* change — this board depends on `EN` on three of its four instances.

---

## 2. Key limits **[DS Features, Absolute Maximum Ratings]**

| Parameter | Value |
|---|---|
| Input voltage | **1.5 V – 8 V** |
| Output voltage options | 1.2 V – 5.0 V (fixed per ordering code) |
| **Maximum output current** | **400 mA @ V<sub>OUT</sub> = 3.3 V** |
| **Dropout voltage** | **200 mV @ I<sub>OUT</sub> = 100 mA** |
| Quiescent current | **0.5 µA typical** |
| Shutdown current | **< 1 µA** |
| PSRR | 60 dB @ 1 kHz |
| Recommended output capacitor | **1 µF** |
| Protection | Built-in short-circuit protection and **fold-back** output current limiter |
| Enable | **Active high, must not float** |
| Vendor-named applications | radio control, cellphones/radiophones/digital cameras, Bluetooth and wireless handsets, portable consumer equipment |

---

## 3. Pinout — DFN 1 × 1-4 **[DS Table 3]**

| Pin | Name | Function |
|---:|---|---|
| **1** | `VOUT` | Output |
| **2** | `GND` | Ground |
| **3** | `EN` | **Enable — active high, "not floating"** |
| **4** | `VIN` | Input |

For reference, the other packages **[DS Tables 1–2]**:

| SOT23-3 | | SOT23-5 | |
|---:|---|---:|---|
| 1 | `GND` | 1 | `VIN` |
| 2 | `VOUT` | 2 | `GND` |
| 3 | `VIN` | 3 | `EN` |
| | | 4 | `NC` |
| | | 5 | `VOUT` |

The PaperMono's schematic symbol shows five markers — pins 1–4 plus a `GND_EP` exposed pad — matching the DFN package. **[SCH]**

---

## 4. Used By

### `devices/m5stack/papermono`

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md). **Four instances, all on schematic sheet 2, all taking `VBUS_L0` as input.**

Sheet 1's power architecture is explicit that this is a **parallel**, not cascaded, structure. M5Stack's own words: *"The PaperMono multi-level power switching design is **not a series structure**. The power inputs for the L1 ~ L3B switches all originate from the L0 (SYS_VBUS) source rather than from the preceding power level, allowing each level to be controlled independently."* **[DOC]** These four LDOs are the mechanism.

#### 4.1 Every instance

| # | Ref | Block | Input | **Output rail** | **Enable net** | Enable source | EN pull-down | Caps |
|---|---|---|---|---|---|---|---|---|
| 1 | **`U4`** | `L0_SW` | `VBUS_L0` | **`3V3_L0`** — always-on: M5PM1 `VCC`, RX8130CE RTC `VIO`, power-button pull-up (`R1`, 10 kΩ, sheet 5), debug test points | *not resolved* — see §4.2 | — | — | `C14`, `C15` = 10 µF/10 V |
| 2 | **`U6`** | `L1_SW` | `VBUS_L0` | **`3V3_L1`** — the BMI270 IMU (`U15`, sheet 4) | **`3V3_L1_EN`** | [M5PM1](../../m5stack/m5pm1/README.md) `U7` pin 18, `LDO3V3_EN_PP` → `pm1.setLdoEnable(bool)` | `R24` = 1 MΩ/1 % | `C18`, `C19` = 10 µF/10 V |
| 3 | **`U5`** | `L3_SW` | `VBUS_L0` | **`EPD_3V3_L3B`** — the e-paper panel's logic rail (FPC `J5`) | **`PYB_EPD_EN`** | [M5IOE1](../../m5stack/m5ioe1/README.md) **`PYG3`** = `M5IOE1_PIN_3`, enum value **2** | `R23` = 1 MΩ/1 % | `C16`, `C17`, `C20` = 10 µF/10 V |
| 4 | **`U9`** | — | `VBUS_L0` | **`3V3_L2_LoRa`** — the Stamp LoRa-1262 module (`U14`, sheet 4) | **`PYG2_LoRa_EN`** | ⚠ **M5PM1 `U7` pin 20**, `G2_WAKEin(INT0/2)_IRQout_ADC` — *not* the M5IOE1, despite the `PYG` prefix | `R26` = 1 MΩ/1 % | `C22`, `C23` = 10 µF/10 V |

All three switched instances use an identical **1 MΩ enable pull-down**, so an undriven or high-Z enable leaves the rail off — the safe default, and consistent across the design. **[SCH]**

> ⚠ **Instance 4's net name is misleading, and this is a systematic problem on this board.** `PYG2_LoRa_EN` uses the `PYG` prefix that M5Stack's documentation otherwise reserves for M5IOE1 pins, but the schematic wires it to the **M5PM1**. The firmware agrees with the schematic, not the prefix: `LORA_EN_PM1_PIN = M5PM1_GPIO_NUM_2` (`hal_lora.cpp:29`). **[SRC]** M5IOE1 `PYG2` is a *different* pin — the LoRa **antenna switch** (`hal_lora.cpp:31`). Two different chips, two different pins, one prefix.

#### 4.2 `3V3_L0`'s enable was not resolved

`U4`'s `EN` net did not come out of the PDF text layer. Sheet 1 lists `3V3_L0` under the **L0 Shipping** column, i.e. it is the rail that exists whenever the battery does — which implies `EN` is tied to `VIN` or to a permanently-asserted node rather than driven. That is consistent, but it is an inference from the power-state table, not a read of the net. **[INF]** Read it off the rendered sheet before relying on it.

This matters because `3V3_L0` powers the M5PM1 itself. If it were switchable, the thing that switches it would have to be the M5PM1, which cannot switch off its own supply.

#### 4.3 ⚠ Near end of discharge these are not 3.3 V rails

`VBUS_L0` is tied to `VBAT_L0` through a 0 Ω link (`R20`) **[SCH]**, so all four LDOs run **directly off the cell**. A single Li-ion cell spends the last part of its discharge between 3.0 V and 3.5 V, and the dropout spec is 200 mV at 100 mA (§2).

**Consequence:** below roughly **3.5 V pack voltage the four rails leave regulation and follow the battery down.** They do not fail — an LDO in dropout is a resistor — but they are no longer 3.3 V, and the margin shrinks continuously as the pack empties. **[INF]**, arithmetic from two `executed-success` reads; not measured.

The same effect applies to the [JW5712](../../joulwatt/jw5712/README.md) buck producing `3V3_L2`, which enters 100 % duty-cycle mode for the same reason. So **every 3.3 V rail on this board becomes a battery-follower near end of charge**, which is a coherent architectural choice rather than an oversight — but it is worth knowing before trusting an ADC reference or a display bias at 15 % battery.

#### 4.4 The output capacitors are 10× the datasheet's recommendation

Every instance uses **10 µF/10 V** where the datasheet recommends **1 µF** (§2). For a CMOS LDO this is normally harmless-to-beneficial for transient response, but stability of a low-I<sub>Q</sub> CMOS regulator does depend on output-capacitor ESR and value, and the datasheet gives a recommendation rather than a range. Recorded as an observation, not a defect: it is a consistent, deliberate choice across four instances, and M5Stack presumably validated it. **[INF]**

---

## 5. Drivers and libraries

**Not applicable** — no bus interface. On the PaperMono:

```cpp
pm1.setLdoEnable(true);                    // 3V3_L1  -> U6  (IMU)
pm1.gpioSetOutput(M5PM1_GPIO_NUM_2, true); // 3V3_L2_LoRa -> U9
ioe1.digitalWrite(M5IOE1_PIN_3, HIGH);     // EPD_3V3_L3B -> U5
// 3V3_L0 (U4) is not software-controllable
```

`pm1.ldoSetPowerHold(true)` retains `3V3_L1` across an M5PM1 shutdown — that is how the board keeps the BMI270 alive as a wake source while everything else is off. **[DOC]**

---

## 6. Integration pitfalls

1. **`EN` must not float** (§2, §3). Every switched instance here fits a 1 MΩ pull-down; copy that.
2. **The output voltage is in the part number** (§1.1). `SSP7615-33DFR` and `SSP7615-30DFR` share a footprint and differ by 300 mV — a silent substitution.
3. **SOT23-3 has no `EN`** (§1.1). Package and function are coupled.
4. **400 mA is at 3.3 V out**; the current capability is not constant across the output-voltage options.
5. **Dropout plus a Li-ion input equals an unregulated rail at low state of charge** (§4.3).
6. **Fold-back current limiting**, not constant-current limiting: under a hard short the LDO reduces current as the output collapses. Good for safety, but it means a heavily capacitive load can prevent start-up ("start-up into a short" behaviour). **[INF]**

---

## 7. Alternatives

| Part | vs. SSP7615-33DFR | When |
|---|---|---|
| **[SGMicro SGM2036-3.3](../../sgmicro/sgm2036-3.3/README.md)** | Low-noise 3.3 V LDO, documented in this repository | Direct substitute class |
| TI **TLV757P** / **TPS7A02** | 300 mA / 200 mA, **25 nA** I<sub>Q</sub> on the TPS7A02, excellent documentation | When quiescent current dominates and the vendor's documentation quality matters |
| **[Joulwatt JW5712](../../joulwatt/jw5712/README.md)** buck | 600 mA switching, 360 nA I<sub>Q</sub>, needs an inductor | Higher current, where the LDO's dropout loss would be significant |
| **[AW35122](../../awinic/aw35122/README.md)** load switch | Switches without regulating | When the downstream rail does not need its own regulation |

The PaperMono uses all three of those categories, and the split is instructive: **buck for the big load, LDOs for the quiet rails, load switches where the rail is just `3V3_L2` gated.** **[INF]**

---

## 8. Open questions

- `U4`'s enable net (§4.2).
- Whether the 10 µF output capacitors are within the part's stable range (§4.4) — the datasheet gives a recommendation, not a range.
- Whether a Chinese-language SSP7615 datasheet exists with more detail; only the English V1.3 was retrieved.
- The LCSC part numbers found during the search (`C3011520`, `C3011522`, `C3011523`) correspond to other output-voltage options in the family; the specific code for the `-33DFR` variant was **not** confirmed.
- No hardware measurement of dropout, load regulation or rail behaviour at low battery.

---

## Manufacturer

**Shanghai Siproin Microelectronics Co., Ltd.** (上海矽普微电子). No vendor sourcing guide exists in this repository yet.

Sourcing notes from this session:

- The datasheet is served **directly and without a session** from the vendor's own site: `https://www.siproin.com/uploads/Datasheets/Pow_driver/LDO/SSP7615_DATASHEET_V1.3_E.pdf`. A mirror of the same document exists at `https://www.siproin-ic.com/wp-content/uploads/2024/07/SSP7615_DATASHEET_V1.3_E.pdf` — two independent hosts for the same file, which is worth recording because it means this artifact is unusually well-preserved for a small Chinese vendor.
- Plain `curl` with a Chrome 131 User-Agent; no fallback needed.
- LCSC hosts copies under `https://www.lcsc.com/datasheet/lcsc_datasheet_<date>_Shanghai-Siproin-Microelectronics-SSP7615-30DFR_C3011522.pdf` — **note that is the `-30` variant**, and LCSC's PDF URLs return HTML to automated clients regardless. Prefer the vendor.

## Related pages

- [Joulwatt JW5712](../../joulwatt/jw5712/README.md) — the buck producing the fifth 3.3 V-class rail
- [M5Stack M5PM1](../../m5stack/m5pm1/README.md) — owns `3V3_L1_EN` and `PYG2_LoRa_EN`
- [M5Stack M5IOE1](../../m5stack/m5ioe1/README.md) — owns `PYB_EPD_EN`
- [Awinic AW35122](../../awinic/aw35122/README.md) — the load switches used where regulation is not needed
- [Bosch Sensortec BMI270](../../bosch-sensortec/bmi270/README.md) — the sole load on `3V3_L1`
- [SGMicro SGM2036-3.3](../../sgmicro/sgm2036-3.3/README.md) — comparable LDO documented in this repository

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | SSP7615 datasheet | Shanghai Siproin Microelectronics | primary | datasheet | <https://www.siproin.com/uploads/Datasheets/Pow_driver/LDO/SSP7615_DATASHEET_V1.3_E.pdf> | 2026-09-01 | **V1.3**, English, 13 pp, 1 064 586 B | Manufacturer identity, ordering-code decode, all electrical limits in §2, all three package pinouts in §3 | `artifacts/ssp7615-datasheet-v1.3-en.pdf` |
| D2 | SSP7615 datasheet (second host, same document) | Siproin | authorized mirror | datasheet | <https://www.siproin-ic.com/wp-content/uploads/2024/07/SSP7615_DATASHEET_V1.3_E.pdf> | 2026-09-01 | V1.3 | Redundant recovery URL | not stored twice |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | schematic | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | All four instances, rails, enable nets and passive values in §4 | `devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| S2 | PaperMono M5PM1/M5IOE1 power-management page | M5Stack | primary | official page | <https://docs.m5stack.com/en/arduino/papermono/m5pm1_m5ioe1> | 2026-09-01 | — | The "not a series structure" architecture statement; `setLdoEnable` / `ldoSetPowerHold` | `scratch/m5stack-papermono/docs/pages/en-arduino-papermono-m5pm1_m5ioe1.html` |
| S3 | `M5PaperMono-UserDemo/main/hal/hal_lora.cpp` | M5Stack | primary | repository | <https://github.com/m5stack/M5PaperMono-UserDemo> | 2026-09-01 | `main` @ `c1099107271d31a0678d661a896e2b04dbb331ea`, MIT | `LORA_EN_PM1_PIN = M5PM1_GPIO_NUM_2`, resolving the `PYG2` prefix conflict in §4.1 | `scratch/m5stack-papermono/repos/M5PaperMono-UserDemo/` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/ssp7615-datasheet-v1.3-en.pdf` | 1 064 586 | `5ca4f994acdfaaba7532d3fdd656ffe3d040272148006a63340c5eb4e0d79830` | 13 |

**Method note.** D1 validated as `%PDF`, 13 pages, text layer intact. LCSC was tried first and rejected: `datasheet.lcsc.com` / `www.lcsc.com/datasheet/...` return **HTTP 200 with `text/html`** for `.pdf` URLs. **Check the `%PDF` magic bytes, never the status code.**
