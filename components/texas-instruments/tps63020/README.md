# Texas Instruments TPS63020

> Single-inductor buck-boost converter with 4 A internal switches — holds a fixed output as the input crosses it in either direction. On a single Li-ion cell this is what keeps 3.3 V alive as the battery sags from 4.2 V to 3.0 V.
> Research snapshot **2026-08-30**. Fitted as `U17` on the Nicolai Electronics Tanmatsu. **No hardware was available.**

---

## Evidence labelling

| Tag | Meaning |
|---|---|
| **[DOC]** | TI datasheet **SLVS916I**, July 2010, revised **October 2019** — `artifacts/tps63020-datasheet-slvs916i.pdf` |
| **[PCB]** | `tanmatsu.kicad_pcb` pad→net assignments (CERN-OHL-P) |
| **[SCH]** | `power.kicad_sch` symbol pin definitions |
| **[INF]** | Author inference |

---

## 1. Identity, variants and lifecycle

| Property | Value | Source |
|---|---|---|
| Part | **TPS63020DSJR** (tape/reel) | BOM |
| Function | Single-inductor **buck-boost** converter, 4 A switches | [DOC] |
| Package | **VSON-14 (DSJ)**, 4.0 × 3.0 mm, exposed thermal pad connected to PGND | [DOC] |
| Datasheet revision | **SLVS916I** — July 2010, revised October 2019 | [DOC] |
| Lifecycle | Active | [DOC] |
| LCSC | [`C15483`](https://www.lcsc.com/search?q=C15483) | BOM |

### 1.1 TPS63020 vs TPS63021 — the only difference that matters

| | **TPS63020** | TPS63021 |
|---|---|---|
| Output | **Adjustable**, 1.2 – 5.5 V, external divider | **Fixed 3.3 V**, trimmed internal divider |
| `FB` pin | Divider tap | **Must be connected to VOUT** |
| `R1` | 1 MΩ (for 3.3 V) | **0 Ω** |
| `R2` | 180 kΩ | **not used** |

**[DOC] §Pin Functions, Table 3.** Same die, same package, same pinout. If you only need 3.3 V, the '21 removes two resistors and a tolerance stack. The Tanmatsu uses the '20 with an external divider anyway (§4.2).

---

## 2. Key electricals **[DOC §6]**

| Parameter | Min | Typ | Max | Unit |
|---|---:|---:|---:|---|
| **Supply at VIN, VINA** | **1.8** | — | **5.5** | V |
| **Output voltage** | **1.2** | — | **5.5** | V |
| Minimum input for start-up (0–85 °C) | 1.5 | 1.8 | 1.9 | V |
| Minimum input for start-up (full range) | 1.5 | 1.8 | 2.0 | V |
| **Feedback voltage `VFB_PWM`** (PS/SYNC = VIN) | **495** | **500** | **505** | mV |
| `VFB_PS` regulation offset in power-save mode | 0.6 % | — | 5 % | — |
| Max line regulation | — | — | 0.5 | % |
| Max load regulation | — | — | 0.5 | % |
| **Oscillator frequency** | 2200 | **2400** | 2600 | kHz |
| Synchronisation frequency range | 2200 | 2400 | 2600 | kHz |
| **`ISW` average switch current limit** (VIN = VINA = 3.6 V, 25 °C) | **3500** | **4000** | **4500** | mA |
| Duty cycle in step-down conversion | — | 20 % | — | — |
| Operating free-air temperature | −40 | — | **85** | °C |
| Operating junction temperature | −40 | — | 125 | °C |
| **Absolute max** VIN, VINA, VOUT, PS/SYNC, EN, FB, PG | −0.3 | — | **7** | V |
| Absolute max L1, L2 (DC) | −0.3 | — | 7 | V |
| Absolute max L1, L2 (AC, < 10 ns) | −3 | — | 10 | V |
| ESD HBM — VIN, VINA, L1 | — | **±500** | — | V |
| ESD HBM — all other pins | — | ±2000 | — | V |
| ESD CDM — all pins | — | ±1500 | — | V |

> ⚠ **±500 V HBM on VIN, VINA and L1** is unusually low. These pins need real ESD discipline in handling and assembly; TI notes that JEDEC JEP155 considers 500 V HBM safe *with basic ESD control methods applied* — meaning the margin depends on your process, not the part.

### 2.1 The current limit is dynamic, and that surprises people **[DOC §Detailed Description]**

The 4 A figure is not a constant:

- **At start-up** the average current limit begins at **400 mA** and ramps up as the output voltage rises, reaching nominal at roughly **1.2 V** output. **There is no timer** — if the output does not rise, the limit does not rise. A hard short or a very large capacitive load therefore holds the converter in a low-current state indefinitely rather than tripping a fault. This is the intended short-circuit protection, and it is why a stuck rail reads as "converter not starting" rather than "converter faulted".
- **If VIN drops below 2.3 V the limit is reduced**, decreasing further toward the 1.8 V minimum. On a battery input this means available output current falls as the cell empties — exactly when a boost converter is drawing the most input current.
- **If the die exceeds the recommended maximum temperature the limit is also reduced.** Thermal foldback, not shutdown.

For a battery-powered design the practical consequence is that **you cannot budget 4 A across the whole input range**. Size for the current available at your minimum cell voltage, not at 3.6 V.

---

## 3. Pinout **[DOC §Pin Functions]**

| Pin | Name | Dir | Description |
|---:|---|---|---|
| **1** | **`VINA`** | I | **Supply voltage for the control stage** |
| 2 | `GND` | — | Control / logic ground |
| 3 | `FB` | I | Feedback. On fixed versions, tie to VOUT |
| 4, 5 | `VOUT` | O | Buck-boost output |
| 6, 7 | `L2` | I | Inductor connection |
| 8, 9 | `L1` | I | Inductor connection |
| 10, 11 | `VIN` | I | **Supply voltage for the power stage** |
| **12** | **`EN`** | I | Enable (1 = on, 0 = off). ⚠ **"must not be left open"** |
| **13** | **`PS/SYNC`** | I | Power-save mode: **1 = disabled, 0 = enabled**; or a clock for synchronisation. ⚠ **"must not be left open"** |
| 14 | `PG` | O | Power good (open-drain, 1 = good). May be left open |
| — | Exposed pad | — | Connected to **PGND** |

⚠ **Two pins are explicitly documented as "must not be left open": `EN` and `PS/SYNC`.** Both are high-impedance CMOS inputs with no internal pull. This is stated twice in the datasheet's own pin table, and it is directly relevant to §4.4.

### 3.1 Power-save mode is the light-load efficiency knob **[DOC §Detailed Description]**

| `PS/SYNC` | Mode | Behaviour |
|---|---|---|
| **Low (GND)** | **Power save ENABLED** | Below ~**100 mA** average inductor current the converter stops switching and the output is monitored by comp-low/comp-high comparators, bursting only as needed. Output regulates **0.6 % to 5 % above** `VFB_PWM` — deliberate headroom for load transients |
| **High (VIN)** | **Power save DISABLED** — forced PWM | Switches continuously at 2.4 MHz regardless of load. Tighter regulation and fixed-frequency ripple, but the switching losses are paid at every load |
| Clock 2.2–2.6 MHz | Synchronised | Forced PWM locked to an external clock |

**For a battery device this is one of the highest-leverage single-bit decisions on the board.** At a few milliamps of load, forced PWM at 2.4 MHz can cost more in gate-drive and switching loss than the load itself. Power-save mode is the reason this part can sit at high efficiency down into the low-milliamp range.

The trade is real: in power-save mode the output sits **0.6–5 % high** and the ripple is bursty and non-periodic, which matters for noise-sensitive analog and for anything that dislikes non-deterministic EMI.

---

## 4. Exact wiring on the Tanmatsu **[PCB]**

The TPS63020 generates the board's main **3.3 V rail from `VSYS`**, which the [BQ25895](../bq25895/README.md) holds between roughly 3.0 V and 5.0 V. This is the classic buck-boost case: `VSYS` crosses 3.3 V from both sides over a charge/discharge cycle, and a plain buck or boost cannot cover it.

| Pin | Name | Net | Support components |
|---:|---|---|---|
| **1** | **`VINA`** | **`Net-(U17-EN)`** | ⚠ see §4.4 |
| 2 | `GND` | `GND` | |
| **3** | **`FB`** | `Net-(U17-FB)` | **R54 = 1 MΩ** to `+3.3V`; **R55 = 180 kΩ** to `GND` |
| 4, 5 | `VOUT` | **`+3.3V`** | The board's main logic rail |
| 6, 7 | `L2` | `Net-(L4-Pad2)` | **L4 = CMLW6028S1R5MST, 1.5 µH** |
| 8, 9 | `L1` | `Net-(L4-Pad1)` | same inductor |
| 10, 11 | `VIN` | **`VSYS`** | From the BQ25895 system rail |
| **12** | **`EN`** | **`Net-(U17-EN)`** | ⚠ see §4.4 |
| **13** | **`PS/SYNC`** | **`Net-(U17-EN)`** | ⚠ see §4.3, §4.4 |
| 14 | `PG` | `unconnected-(U17-PG-Pad14)` | Power-good unused — permitted |
| 15 | Exposed pad | `GNDPWR` | |

### 4.1 The inductor is the datasheet value

`L4 = CMLW6028S1R5MST` — **1.5 µH**, matching TI's recommended value for this part **[DOC]**. A 6028-size (6.0 × 2.8 mm) shielded power inductor is an appropriate choice for 4 A switches at 2.4 MHz. [INF]

### 4.2 ✅ The feedback divider is exactly TI's recommended value

TI's Table 3, *Resistor Selection For Typical Output Voltages* **[DOC]**:

| VOUT | R1 | R2 |
|---|---|---|
| 2.5 V | 750 kΩ | 180 kΩ |
| **3.3 V** | **1 MΩ** | **180 kΩ** |
| 3.6 V | 1.1 MΩ | 180 kΩ |
| 4.5 V | 1.43 MΩ | 180 kΩ |
| 5 V | 1.6 MΩ | 180 kΩ |

The board fits **R54 = 1 MΩ** (high-side, VOUT→FB) and **R55 = 180 kΩ** (low-side, FB→GND) **[PCB]** — the datasheet's 3.3 V row verbatim. TI additionally specifies that *"the low-side resistor R2 must be kept in the range of 200 kΩ"*; 180 kΩ satisfies that.

Verifying: V<sub>OUT</sub> = V<sub>FB</sub> × (1 + R1/R2) = 0.500 × (1 + 1 000/180) = **3.278 V**, within the ±0.5 % feedback tolerance of the 3.3 V target. Correct by construction.

### 4.3 ⚠ `PS/SYNC` is tied to `EN`, so power-save mode is **disabled** whenever the rail is on

`PS/SYNC` (pin 13) shares a net with `EN` (pin 12) **[PCB]**. Since `EN` must be **high** for the converter to run, `PS/SYNC` is necessarily **high** at the same time — and per §3.1, **`PS/SYNC` high disables power-save mode**.

The Tanmatsu's 3.3 V rail therefore runs in **forced PWM at 2.4 MHz at all loads**, including deep idle.

**This is a real and avoidable battery-life cost.** Power-save mode exists precisely to stop a 2.4 MHz converter burning switching losses when the load is a few milliamps — which is the state a handheld spends most of its life in. Tying `PS/SYNC` to GND instead (or to a GPIO, allowing firmware to force PWM only when the analog sections need clean rails) would recover it.

Against that, forced PWM gives tighter regulation and predictable fixed-frequency ripple, which is defensible for a board with an audio DAC and a radio. Whether it was a considered trade or a convenience of routing is not documented by the vendor. [INF]

### 4.4 ⚠ Unresolved: `VINA`, `EN` and `PS/SYNC` form an isolated net in the published design

Pins **1 (`VINA`)**, **12 (`EN`)** and **13 (`PS/SYNC`)** are all on net `Net-(U17-EN)`. The **only** other component on that net is **C56, a 100 nF capacitor to GND** **[PCB]**. There is no pull-up to `VSYS`, no GPIO, no resistor — nothing that could drive it high.

The KiCad symbol's pin numbering was checked against the datasheet and matches exactly (1 = VINA, 12 = EN, 13 = PS/SYNC) **[SCH]**, so this is not a symbol-mapping artifact.

As drawn this cannot work:

- **`VINA` is the control-stage supply** and requires 1.8–5.5 V **[DOC]**. An unpowered `VINA` means no control circuitry.
- **`EN` "must not be left open"** and must be high to enable the converter.
- The rest of the circuit is correct — `VIN` on `VSYS`, `VOUT` on `+3.3V`, the datasheet-exact divider, the datasheet-value inductor.

**The board demonstrably works and ships**, so one of the following is true, and this record does not have the evidence to choose:

1. The published KiCad snapshot contains an error on this net that does not exist on the manufactured board.
2. The connection exists through something not represented as a pad in the PCB netlist.
3. The snapshot captures an in-progress revision.

Recorded as a conflict rather than resolved by preference, per the research method. **Resolving it would need either the rendered schematic sheet read graphically, or continuity measured on hardware.** Note that if the net *is* connected to `VSYS`, then the 100 nF C56 is a soft-start delay on `EN` — a common idiom — and §4.3's conclusion about power-save mode stands unchanged.

---

## 5. Design and integration pitfalls, in priority order

1. **`EN` and `PS/SYNC` must not float** — the datasheet says so explicitly, twice. §3.
2. **Decide `PS/SYNC` deliberately.** Low = power save (best light-load efficiency, output sits 0.6–5 % high, bursty ripple). High = forced PWM (tight regulation, worse idle efficiency). On battery, low is usually right. §3.1, §4.3.
3. **The 4 A current limit is not constant** — it folds back below 2.3 V input and with temperature, and ramps from 400 mA at start-up. Budget at your minimum cell voltage. §2.1.
4. **Keep `R2` near 200 kΩ.** The feedback divider is not a free choice; too high and FB pin bias current matters, too low and it wastes quiescent current. §4.2.
5. **`VINA` and `VIN` are separate pins** and both need supply. Tying them is normal; leaving `VINA` unconnected is not. §4.4.
6. **Watch the ±500 V HBM rating on VIN/VINA/L1.** §2.
7. **The exposed pad is PGND and is the thermal path.** At multi-amp loads the pad's via array is what keeps the die in spec.
8. **`PG` is open-drain** — it needs a pull-up if you use it. The Tanmatsu leaves it open, which is permitted.
9. **2.4 MHz switching is fast.** Input and output capacitor placement and the inductor loop area matter more than they would at 500 kHz. Follow the datasheet layout.

---

## 6. Alternatives

| Part | vs. TPS63020 | When |
|---|---|---|
| **TPS63021** | Fixed 3.3 V, internal divider | If 3.3 V is all you need — fewer parts, no divider tolerance. §1.1 |
| **TPS63060 / TPS63070** | Higher voltage, USB-PD-friendly buck-boost | Wider input range |
| **TPS61022 / TPS61023** | Boost only | If the input is always below the output |
| **[TLV62569](../tlv62569dbvt/README.md)** | Buck only, documented in this repository | If the input is always above the output — much cheaper and simpler |
| **[SGM2036-3.3](../../sgmicro/sgm2036-3.3/README.md)** | LDO, documented here | Low current, low noise, when the drop is small |
| **MAX77801 / MPQ2013** | Comparable buck-boost second sources | Cost or availability |

**A buck-boost is only justified when the input genuinely crosses the output.** That is exactly the single-Li-ion-cell-to-3.3 V case here: a cell at 4.2 V needs a buck, the same cell at 3.0 V needs a boost. If your rail is 1.8 V or your input never falls below 3.6 V, a plain buck is smaller, cheaper and more efficient.

---

## 7. Open questions

- **§4.4 is unresolved** and is the most important open item: per the published netlist the `VINA`/`EN`/`PS/SYNC` net has no driver.
- Whether tying `PS/SYNC` to `EN` was a deliberate noise-versus-efficiency trade or incidental. The vendor has not commented. §4.3.
- No measured efficiency, idle current or output ripple for this board.
- The actual 3.3 V rail load on the Tanmatsu is not characterised here, so the headroom against the folded-back current limit at low cell voltage is unknown.

---

## Manufacturer

**Texas Instruments** — see [`vendors/texas-instruments/README.md`](../../../vendors/texas-instruments/README.md). The datasheet was obtained from the guessable, session-free URL `https://www.ti.com/lit/ds/symlink/tps63020.pdf` on 2026-08-30, exactly as that guide predicts.

## Used By

| Device | Ref | Role |
|---|---|---|
| [Nicolai Electronics Tanmatsu](../../../devices/nicolai-electronics/tanmatsu/README.md) | `U17` | Generates the main **3.3 V logic rail from `VSYS`**, holding it as the cell sags below 3.3 V. Inductor `L4` = 1.5 µH; feedback `R54` 1 MΩ / `R55` 180 kΩ (TI's exact recommendation). Runs in **forced PWM** because `PS/SYNC` is tied to `EN` (§4.3). See [`bom.md`](../../../devices/nicolai-electronics/tanmatsu/bom.md) |

## Related pages

- [`components/texas-instruments/bq25895/README.md`](../bq25895/README.md) — supplies `VSYS`, the input to this converter
- [`components/texas-instruments/tlv62569dbvt/README.md`](../tlv62569dbvt/README.md) — the buck-only comparison
- [`components/sgmicro/sgm2036-3.3/README.md`](../../sgmicro/sgm2036-3.3/README.md) — the LDO comparison
- [`components/generic/charger-power-path/README.md`](../../generic/charger-power-path/README.md)

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | TPS63020/TPS63021 datasheet | Texas Instruments | primary | datasheet | <https://www.ti.com/lit/ds/symlink/tps63020.pdf> | 2026-08-30 | **SLVS916I**, Jul 2010 rev. Oct 2019, 34 pp, 1 855 244 B | Pinout, electricals, current-limit behaviour, power-save semantics, **Table 3 divider values** | `artifacts/tps63020-datasheet-slvs916i.pdf` |
| S1 | `tanmatsu.kicad_pcb` | Nicolai Electronics | primary | repository | in-tree snapshot | 2026-08-24 | `tanmatsu-hardware` @ `640805dd`, CERN-OHL-P | §4 pin table, R54/R55/C56/L4 values, **the §4.4 anomaly** | `devices/nicolai-electronics/tanmatsu/artifacts/schematics/kicad/tanmatsu.kicad_pcb` |
| S2 | `power.kicad_sch` | Nicolai Electronics | primary | repository | in-tree snapshot | 2026-08-24 | same | Symbol pin numbering, confirming §4.4 is not a mapping artifact | same directory |
| S3 | Tanmatsu production BOM | Nicolai Electronics | primary | repository | in-tree snapshot | 2026-08-24 | CERN-OHL-P | `U17 = TPS63020DSJR`, LCSC C15483 | `devices/nicolai-electronics/tanmatsu/artifacts/production/bom.csv` |

**Method note.** The §4 pin table and every passive value were produced by parsing pad→net assignments out of `tanmatsu.kicad_pcb` programmatically, then cross-checking the pin *names* against the symbol definition in `power.kicad_sch` and against the datasheet's own pin table. All three agree on numbering, which is what makes §4.4 reportable as a genuine anomaly rather than a parsing error.
