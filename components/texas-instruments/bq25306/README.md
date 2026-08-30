# Texas Instruments BQ25306 (BQ25306RTER)

- **Category:** **standalone switch-mode (synchronous buck) 1-cell / 2-cell Li-ion, Li-polymer and LiFePO4 battery charger**, 17 V input, 3 A
- **Reference designator:** `U12` on the **ZeroWriter Ink main board** ("Zerowriter Inkplate 5 Gen2", KiCad v1.2.0)
- **Marking in the BOM `Value` field:** `BQ25306RTER` — WQFN-16 (`RTE`), 3.0 × 3.0 mm, tape-and-reel
- **Owning MCU:** **none.** This part has no digital control interface at all. It is configured entirely by resistors and cannot be read, written or commanded by the ESP32-WROVER
- **Not fitted** on Soldered's stock [Inkplate 5](../../../devices/soldered-electronics/inkplate-5/README.md) or [Inkplate 5 Gen 2](../../../devices/soldered-electronics/inkplate-5-gen2/README.md) — those use an `MCP73831T` **linear** charger at `U4`
- **Research status:** part identity, package, every pin's net, both programming resistors and the resulting charge parameters established from the published KiCad design and the TI datasheet. Battery capacity and cell chemistry remain unknown
- **Retrieved:** 2026-08-24. Datasheet downloaded, schematic read pin-by-pin and programming resistors solved 2026-08-26

## Evidence labelling

| Label | Meaning |
|---|---|
| **[DOC]** | Manufacturer datasheet — TI `SLUSDC7A`, March 2020, revised November 2020 |
| **[SCH]** | Read directly from ZeroWriter's published KiCad schematic (`CTRL & COMS.kicad_sch`, v1.2.0, sheet 3/8, dated 2025-06-30) and from the plotted `…Schematics.pdf` page 3 |
| **[BOM]** | ZeroWriter / Soldered KiCad BOM CSV exports |
| **[SRC]** | Published source code |
| **[FW]** | String scan of a shipped firmware binary |
| **[WEB]** | Vendor web page |
| **[INF]** | Inference. Reasoning and arithmetic are always shown |

---

## 1. Identity, package, family and lifecycle

Decoding the ordering suffix **[DOC, mechanical-data package drawing `RTE0016C` / `4219117/B`, April 2022]**: `BQ25306` base part, `RTE` = 16-pin WQFN 3.0 × 3.0 mm with a **thermal pad (pin 17)**, 0.8 mm max height, `R` = large tape-and-reel.

| | Value | Source |
|---|---|---|
| Document | **`SLUSDC7A`** — "BQ25306 Standalone 17-V, 3.0-A 1-2 Cell Buck Battery Charger", March 2020, rev. November 2020 | [DOC] |
| Package | WQFN-16 (`RTE0016C`), 3.00 × 3.00 mm body, 0.5 mm pitch, exposed thermal pad | [DOC] |
| Cells supported | 1S **or** 2S — the cell count is implied purely by the `FB` divider ratio; there is no cell-count strap | [DOC §10.2.1.2.1] |
| Chemistries | Li-Ion, Li-polymer, LiFePO4 | [DOC §1] |
| Lifecycle | **ACTIVE** as of 2026-08-26 (TI product folder returns `ACTIVE`, no NRND/LIFEBUY/obsolete marker) | [WEB] |

There is only one orderable part number in this datasheet. TI's own comparison table **[DOC §6]** places it against its nearest sibling:

| | `BQ25302` | **`BQ25306`** (fitted) |
|---|---|---|
| Cells in series | 1 cell | **1–2 cell** |
| Input voltage | 4.1 – 6.2 V | **4.1 – 17 V** |
| Charge voltage | fixed 4.1 / 4.2 / 4.35 / 4.4 V | **programmable 3.4 – 9.0 V** |
| Max fast-charge current | 2.0 A | **3.0 A** |
| Battery temperature protection | cold/hot | cold/hot |

The thermal table is headed `BQ2530x`, indicating a wider family sharing the RTE package and much of the architecture; **those are different datasheets and different default parameters — do not substitute one for another on the strength of the shared package.** Note in particular that on this board the extra capability the BQ25306 buys over the cheaper BQ25302 is **not used**: the input is 5 V only (§3), the pack is 1S, and the programmed current is 2.0 A — exactly the BQ25302's ceiling. The programmable charge voltage (4.18 V rather than a fixed 4.2 V) is the one differentiator actually exercised. **[INF]**

### 1.1 Why ZeroWriter changed the charger

This part is the clearest single signal of ZeroWriter's design intent. Soldered's stock Inkplate 5 Gen 2 charges with an `MCP73831T` **linear** charger at `U4` **[BOM]**. ZeroWriter deleted it, moved a `USBLC6-2SC6` USB ESD protector into the `U4` position, and added `U12` = BQ25306 plus `L3` = `SRP3212A-1R0M` (1 µH) and the support capacitors `C58` 4u7, `C59` 2u2, `C60`/`C61` 10u, `C62` 470p **[BOM, SCH]**.

A linear charger dissipates `(Vin − Vbat) × Icharge`. At the 2 A this board is programmed for and a 5 V input into a 3.7 V cell, that would be **2.6 W** burned in one SOT-23-5 — thermally impossible. A synchronous buck at ~92.5 % **[DOC §1]** dissipates roughly 0.65 W instead. Switching to a buck topology is exactly what you do when you fit a much larger cell and want it charged in reasonable time, which is consistent with the campaign's "up to weeks of daily use" / ~100 h battery claim.

## 2. Absolute maximum and recommended operating conditions **[DOC §8.1–8.3]**

| Parameter | Min | Max | Unit | Note for this board |
|---|---:|---:|---|---|
| `VBUS` (abs max, converter not switching) | −2 | **28** | V | Only 5 V is ever applied here |
| `PMID` (abs max) | −0.3 | 28 | V | |
| `SW` (abs max) | −2 | 20 | V | −3 V for 10 ns transient |
| `BTST` (abs max) | −0.3 | 25.5 | V | |
| `BTST` to `SW` | −0.3 | 5.5 | V | |
| `BAT`, `FB`, `FB_GND` (abs max) | −0.3 | 11 | V | |
| **`STAT`, `ICHG`, `REGN`, `POL`, `/EN`, `TS` (abs max)** | −0.3 | **5.5** | V | **See §3.2 — `POL` is tied to `VBUS` on this board** |
| `STAT` sink current | — | 6 | mA | |
| `REGN` sink current | — | 20 | mA | |
| Junction temperature | −40 | 150 | °C | |
| **Recommended `VVBUS`** | **4.1** | **17.0** | V | Board only ever sees ~5 V |
| Recommended `VBAT` | 3.4 | 9 | V | 1S here |
| Recommended `IVBUS` / `ISW` | — | 3 | A | |
| Ambient `TA` | −40 | 85 | °C | |
| ESD HBM / CDM | ±2000 / ±250 | | V | |

### 2.1 Key electrical parameters **[DOC §8.5]**

| Parameter | Symbol | Min | Typ | Max | Unit |
|---|---|---:|---:|---:|---|
| Switching frequency | `FSW` | 1.02 | **1.20** | 1.38 | MHz |
| Max duty cycle | `DMAX` | — | 97.0 | — | % |
| Battery feedback regulation voltage | `VFB_REF_VBATREG` | 1094 | **1100** | 1104.5 | mV |
| Charge-voltage programming range | `VBATREG_RANGE` | 3.400 | — | 9.000 | V |
| Charge-current ratio | `KICHG` | 36000 | **40000** | 44000 | A·Ω |
| `ICHG` pin regulated voltage | `VICHG` | 993 | 998 | 1003 | mV |
| Min / max `RICHG` | — | 11.70 | — | 250 | kΩ |
| `RICHG` threshold that clamps `IPRE`/`ITERM` to 63 mA | `RICHG_HIGH` | 60 | 65 | 70 | kΩ |
| `VBUS` power-on reset | `VVBUS_UVLOZ` | 3.0 | — | 3.80 | V |
| `VBUS` threshold to turn `REGN` on | `VVBUS_LOWV` | 3.8 | 3.90 | 4.00 | V |
| `VBUS` over-voltage, rising | `VVBUS_OVP_RISE` | 17.00 | **17.40** | 17.80 | V |
| `VBUS` OVP hysteresis | `VVBUS_OVP_HYS` | — | 750 | — | mV |
| Sleep entry / exit (`VBUS − VBAT`) | `VSLEEP` / `VSLEEPZ` | 30 / 110 | 60 / 157 | 100 / 295 | mV |
| Minimum input-voltage regulation | `VINDPM_MIN` | 4.0 | 4.07 | 4.2 | V |
| Input current regulation | `IINDPM_3A` | 3.00 | **3.35** | 3.70 | A |
| HSFET cycle-by-cycle current limit | `IHSFET_OCP` | 5.2 | 6.2 | 6.7 | A |
| Junction temperature regulation | `TREG` | 111 | **120** | 133 | °C |
| Thermal shutdown rise / fall | `TSHUT` | — | 150 / 125 | — | °C |
| `REGN` LDO output (VBUS = 5 V, 0–16 mA) | `VREGN` | 4.2 | — | 5.0 | V |
| RBFET / HSFET / LSFET `RDS(on)` | `Q1`/`Q2`/`Q3` | — | 40 / 50 / 45 | 65 / 82 / 72 | mΩ |
| `STAT` blink rate / duty | `FBLINK` | — | 1 / 50 | — | Hz / % |
| Fast-charge safety timer | `tSAFETY_FAST` | 15.0 | **20.0** | 24.0 | hr |
| Precharge safety timer | `tSAFETY_PRE` | 1.5 | **2.0** | 2.5 | hr |
| Delay, VBUS applied → charge start | `tCHG_ON_VBUS` | — | 275 | — | ms |
| Delay, `/EN` rising → charger on | `tCHG_ON_EN` | — | 245 | — | ms |
| Thermal resistance, JEDEC | `RθJA` | — | **45.8** | — | °C/W |

### 2.2 Quiescent and leakage currents **[DOC §8.5]**

This is where the part earns its place in a battery device.

| Condition | Symbol | Typ | Max | Unit |
|---|---|---:|---:|---|
| **BAT/SW leakage, HiZ mode (VBUS floating), `VBAT` = 4.5 V** | `IQ_BAT_HIZ` | **0.17** | 1.0 | µA |
| BAT/SW leakage, disable mode, `VBAT` = 9 V | `IQ_BAT_DIS_9V` | 0.50 | 2 | µA |
| VBUS leakage when disabled, `VBUS` = 5 V | `IQ_VBUS_DIS` | 3.5 | 4.25 | µA |
| VBUS reverse current from BAT/SW (VBUS shorted to GND), `VBAT` = 4.5 V | `IVBUS_REVS` | 0.07 | 3 | µA |

TI's headline "200 nA low battery leakage" is the `IQ_BAT_HIZ` figure. **On this board that number is what matters**: with the USB cable unplugged the charger sits in HiZ and draws ~0.17 µA typ from the pack. Against a device that claims ~100 h of use, the charger's own shelf drain is irrelevant — good. Note the *maximum* is 1.0 µA, ~6× the typical; budget against the max, not the typ.

## 3. Exact wiring on the ZeroWriter Ink main board **[SCH, sheet 3/8 "BATTERY CHARGER"]**

Every pin of `U12` is accounted for. Verified twice: by parsing the KiCad netlist geometrically, and by reading the plotted schematic PDF page 3 as an image.

| Pin | Name | Net on this board | Detail |
|---:|---|---|---|
| 1 | `VBUS` | `VUSB` | `C58` **4u7** + `C38` **2u2** + `C39` **100n** to GND. TI asks for 2.2 µF minimum — comfortably met |
| 2 | `REGN` | `REGN` | `C59` **2u2** to GND. TI specifies exactly 2.2 µF |
| 3 | `STAT` | `CHRG-ST` | Leaves the board on `K1` pin 1 (`HC-1.25-16PWT`) and appears on test point `TP50`. **§7** |
| 4 | `ICHG` | `ICHG` | **`R25` = 20 kΩ to GND.** The charge-current programming resistor — **§3.1** |
| 5 | `POL` | **`VUSB`** | **Tied to `VBUS`. TI says "keep this pin floating for standalone charger" — §3.2** |
| 6 | `/EN` | **GND** | Hard-tied to ground → **the charger is permanently enabled** whenever `VBUS` is valid |
| 7 | `TS` | *(local node)* | **`R17` 10 kΩ to `REGN`, `R18` 10 kΩ to GND.** This is TI's documented "TS not used" network — **there is no battery thermistor. §6** |
| 8 | `FB_GND` | `FB-GND` | Kelvin return for the feedback divider; goes to `R28` **100 kΩ** |
| 9 | `FB` | `CHRG-FB` | Divider midpoint. `R29` **280 kΩ** to `VBAT`, `C62` **470 pF** feed-forward across `R29` — **§3.1** |
| 10 | `BAT` | `VBAT` | Battery sense and converter output. `C61` **10 µF**. TI recommends 10 µF |
| 11, 12 | `GND` | GND | |
| 13, 14 | `SW` | `CHRG-SW` | → `L3` `SRP3212A-1R0M` **1.0 µH** → `VBAT` |
| 15 | `BTST` | `BTST` | `C37` **47 nF** from `BTST` to `SW`. TI specifies 0.047 µF |
| 16 | `PMID` | *(local node)* | `C60` **10 µF** to GND. TI recommends 10 µF |
| 17 | Thermal pad | GND | Tied to the `GND` net with pins 11/12 |

The passive set is a **textbook copy of TI's Figure 10-1 typical application**: 2.2 µF `VBUS`, 10 µF `PMID`, 2.2 µF `REGN`, 47 nF bootstrap, 10 µF `BAT`, 470 pF feed-forward. The inductor choice is also correct and diagnostic:

> **`L3` = 1.0 µH is TI's recommendation for `VVBUS_MAX` < 6.2 V; 2.2 µH is required above that** **[DOC §10.2.1.2.3]**.

So although the silicon accepts 17 V, **this board is a 5 V-input design and must not be fed a high-voltage adapter.** With a 1 µH inductor at 9 V or 12 V input the ripple current would be roughly double what the design intends. The USB-C receptacle on the breakout board has plain 5.1 kΩ CC pull-downs (`R1`, `R2`) and no PD negotiation **[SCH breakout]**, so in normal use only 5 V is ever presented — the risk is confined to somebody wiring a barrel jack to `VUSB`.

### 3.1 Solving the two programming resistors

**Charge current** **[DOC §7-1, §10.2.1.2.2]**:

```
ICHG = KICHG / RICHG          KICHG = 40 000 A·Ω typ

ICHG = 40 000 / 20 000  =  2.00 A
```

With the `KICHG` min/max of 36 000 / 44 000 the guaranteed window is **1.80 A – 2.20 A**. `RICHG` = 20 kΩ sits above `RICHG_MIN_SLE1` (11.70 kΩ) and far below `RICHG_HIGH` (60–70 kΩ), so **precharge and termination are *not* clamped to 63 mA** and both land at 10 % of `ICHG`:

- `IPRECHG` = **200 mA** typ
- `ITERM` = **200 mA** typ

**Charge voltage** **[DOC §7-1, §10.2.1.2.1]**:

```
VBATREG = 1.1 × (1 + R1/R2)          R1 = R29 = 280 kΩ,  R2 = R28 = 100 kΩ

VBATREG = 1.1 × (1 + 280/100) = 1.1 × 3.8 = 4.18 V
```

Applying the `VFB_REF_VBATREG` tolerance (1094 – 1104.5 mV) and ignoring resistor tolerance, the regulation point is **4.157 V – 4.197 V**. That is a deliberate, slightly conservative choice: a standard 4.20 V cell is never overcharged even at the top of the IC's tolerance band. Charging a Li-ion cell ~20 mV below 4.20 V costs perhaps 1–2 % of capacity and buys a measurable improvement in cycle life. **[INF]**

Two checks against TI's guidance:

- TI recommends `R2` ≤ 200 kΩ **[DOC §7-1]**. `R28` = 100 kΩ ✅
- TI's own 1-cell example is `R1` = 562 kΩ / `R2` = 200 kΩ (ratio 2.81 → 4.191 V). ZeroWriter uses 280 k/100 k (ratio 2.80 → 4.18 V) — the same design, halved, so twice the divider current (~11 µA vs ~5.5 µA off the pack). Still negligible. ✅
- ⚠ TI requires **1 % or better** resistors for `R1`/`R2` **[DOC §10.2.1.2.1]**. The BOM records only `280k` and `100k` with a generic `0603R` footprint and **no tolerance** **[BOM]**. If these were fitted as 5 % parts the worst-case regulation point moves to roughly 4.18 × (1 ± 0.037) ≈ **4.03 V – 4.33 V** — the upper end of which overcharges the cell. **This is the single most important unverified parameter on the page.** **[INF]**

### 3.2 Two annotations on the vendor's own schematic disagree

The schematic sheet carries two free-text notes in the charger block **[SCH]**:

| Text | Position | Verdict |
|---|---|---|
| `ICHG:3A` | printed immediately under `R25` | **Wrong.** `R25` = 20 kΩ gives 2.0 A. 3 A would need `RICHG` ≈ 13.3 kΩ |
| `ICHG:2A` / `VIN:5V` / `VREG:4.18V` | printed beside the `U12` symbol | **Correct.** All three match the fitted resistors exactly |

Both are drawn on the same sheet, 47 mm apart. The `ICHG:3A` note is almost certainly a leftover from an earlier iteration that was superseded when the resistor was chosen. **Trust `R25` and the arithmetic, not the silkscreen-style annotation.** If you are reverse-engineering charge current from the published design, read the resistor.

### 3.3 `POL` tied to `VBUS` — undocumented, but benign here

`POL` selects the polarity of `/EN` **[DOC Table 7-1]**:

| `POL` | `/EN` behaviour |
|---|---|
| **floating** | Enabled with `/EN` **low or floating**; disabled with `/EN` **high**. *"Keep this pin floating for standalone charger."* |
| **grounded** | Enabled with `/EN` **high**; disabled with `/EN` **low or floating** |
| **tied high** | **Not documented anywhere in SLUSDC7A** |

ZeroWriter ties `POL` to `VUSB` and `/EN` to GND **[SCH]**. Reading the input thresholds (`VILO` ≤ 0.40 V, `VIH` ≥ 1.3 V) the part evidently distinguishes only three states — low, high, floating — and `POL` high is simply not in the table. **[INF]** The most likely reading is that the designer treated `POL` as a two-state input, saw "floating or grounded", and chose to terminate it rather than leave a pin floating; with `/EN` at GND the charger is enabled under the *floating* interpretation, which is what the observed behaviour of the product (it charges) implies. **[INF, marked uncertain]**

Two consequences worth writing down:

1. **`POL` abs max is 5.5 V** while `VBUS` abs max is 28 V **[DOC §8.1]**. On this board `POL` sits at whatever `VBUS` sits at. USB-C 5 V nominal can legitimately reach 5.5 V at the top of the tolerance band, and inrush/hot-plug ringing on an unprotected 5 V rail routinely overshoots further. **This pin has essentially zero design margin**, and it is the pin that would fail first if anyone applied a 9 V or 12 V supply. **[INF]**
2. **There is no software or hardware charge-inhibit.** `/EN` is hard-tied, so charging cannot be suspended by the ESP32, by the power switch, or by anything else. The charger runs whenever a 5 V source is present, including with the device's slide switch off.

## 4. The charge profile as configured on this board

TI's four-phase profile **[DOC §9.3.2.1, Table 9-1]**, with the thresholds resolved for `VBATREG` = 4.18 V and `ICHG` = 2.0 A. All percentages are of `VFB_REF_VBATREG`, so they scale directly with `VBATREG`.

| Phase | Entry condition | Current | Value here |
|---|---|---|---|
| **Battery short (trickle)** | `VBAT` < `VBAT_SHORT` | `IBAT_SHORT` | **35 mA** typ (25–46 mA) |
| **Precharge** | `VBAT_SHORT` < `VBAT` < `VBAT_LOWV` | `IPRECHG` = 10 % `ICHG` | **200 mA** typ |
| **Fast charge (CC)** | `VBAT` > `VBAT_LOWV` | `ICHG` | **2.00 A** typ (1.80–2.20 A) |
| **Voltage regulation (CV)** | `VBAT` at `VBATREG` | tapering | to `ITERM` |
| **Terminated** | `I` < `ITERM` **and** `VBAT` > recharge threshold | 0 | **200 mA** typ |

Derived voltage thresholds, all typ **[DOC §8.5]** **[INF for the arithmetic]**:

| Threshold | Datasheet | Value at `VBATREG` = 4.18 V |
|---|---|---:|
| `VBAT_SHORT` rising / falling | 2.20 / 2.00 V (absolute, not a percentage) | **2.20 V / 2.00 V** |
| `VBAT_LOWV` rising (pre → fast) | 70 % | **2.93 V** |
| `VBAT_LOWV` falling (fast → pre) | 68 % | **2.84 V** |
| Recharge threshold | 96.4 % | **4.03 V** |
| Battery OVP rising | 104 % | **4.35 V** |
| Battery OVP falling | 102 % | **4.26 V** |

On battery OVP the converter stops switching **and a 7 mA pull-down is applied to the `BAT` pin** until the voltage falls back below 4.26 V **[DOC §9.3.4.3.1]**.

### 4.1 Termination and recharge

Charging terminates when the current falls below `ITERM` **and** `VBAT` is above the recharge threshold **[DOC §9.3.2.3]**. After termination the converter stops switching entirely and the safety timer is disabled. A new cycle starts automatically when `VFB` falls below 96.4 % (`VBAT` ≈ 4.03 V), with the safety timer reset **[DOC §9.3.2.4]**.

**Termination is temporarily disabled while the device is in input-current regulation or thermal regulation**, and in those states the safety timer counts at half rate (so the effective fast-charge timer becomes 40 h) **[DOC §9.3.2.3, §9.3.4.2]**. That matters here: see §9.2.

## 5. Input handling — DPM, current limit, OVP, sleep

| Mechanism | Behaviour | Value here |
|---|---|---|
| **VINDPM** (input *voltage* DPM) | Regulates `PMID` by reducing charge current so a weak supply is not crashed. Threshold **dynamically tracks the battery**: the higher of `VINDPM_MIN` and `1.044 × VBAT + 125 mV` **[DOC §9.3.4.1.2]** | `VINDPM_MIN` = **4.07 V** typ. At `VBAT` = 3.7 V → 4.99 V; at `VBAT` = 4.18 V → **4.49 V** |
| **IINDPM** (input *current* limit) | Fixed, built-in. Duty cycle is reduced when input current exceeds the threshold **[DOC §9.3.4.1.3]** | **3.35 A** typ (3.00–3.70 A). **Not programmable — there is no ILIM pin and no I²C** |
| **Input OVP** | Converter stops switching, safety timer stops, `REGN` stays on, `STAT` blinks **[DOC §9.3.4.1.1]** | **17.4 V** typ rising, 750 mV hysteresis |
| **Sleep** | Enters when `VBUS − VBAT` falls below `VSLEEP`; exits above `VSLEEPZ` | 60 mV / 157 mV typ |
| **HiZ** | `VBUS` below `VVBUS_UVLOZ` (3.0–3.8 V). `REGN` off, `STAT` open, ~0.17 µA from the pack | |
| **Cycle-by-cycle HSFET limit** | Peak inductor current limit, per switching cycle | `IHSFET_OCP` **6.2 A** typ |

**The VINDPM tracking behaviour is the practical one.** At `VBAT` = 3.7 V the VINDPM target is 4.99 V, essentially at the USB rail voltage. With a cable and connector drop of a couple of hundred millivolts on a 2 A charge current, the input will sit at or below the VINDPM threshold and the charger will **fold back charge current to hold `PMID` at ~5.0 V**. This is not a fault — it is the loop doing its job — but it means:

> **Observed charge current will very often be well below the programmed 2 A, and will vary with the cable.** A thin or long USB-C cable is the most common cause of "it charges slowly", and neither the LED nor the firmware can tell you it is happening. **[INF]**

There is **no input-current-limit programming**, so the charger will happily try to pull ~1.7 A from a 5 V/500 mA USB 2.0 port. What actually happens is that the port's voltage sags, VINDPM engages, and the charger backs off — which is the correct behaviour and the entire reason VINDPM exists. **[INF]**

## 6. TS pin: there is no battery temperature sensing on this board

The `TS` pin is the charger's battery-thermistor input. TI's intended network is a divider from `REGN` to `TS` to GND with a 103AT-2 NTC in the pack; charging is suspended outside the programmed window **[DOC §9.3.2.6]**.

**ZeroWriter fits `R17` = 10 kΩ (`REGN` → `TS`) and `R18` = 10 kΩ (`TS` → GND) and no thermistor** **[SCH]**. That is verbatim TI's documented instruction for the unused case:

> *"When TS pin is not used, connect a 10-kΩ resistor from REGN to TS and a 10-kΩ resistor from TS to GND."* **[DOC Table 7-1]**

So this is a correct, sanctioned configuration — but its consequence should be stated plainly:

> **⚠ The battery pack's temperature is not monitored by the charger.** The only battery-temperature protection in the product is whatever protection circuit is inside the pack itself, which is not documented in any published ZeroWriter material. Charging a lithium cell below 0 °C causes lithium plating and permanent capacity loss; charging a hot cell is a safety issue. Neither is detected here.

### 6.1 A margin note on the divider

`R17`/`R18` at 10 k/10 k put `VTS` at exactly **50.0 % of `REGN`**. The comparator thresholds are percentages of `REGN` **[DOC §8.5]**:

| Threshold | Min | Typ | Max |
|---|---:|---:|---:|
| `VT1%` cold (`VTS` rising, charge suspends **above** this) | 72.68 | 73.5 | 74.35 % |
| `VT3%` hot (`VTS` falling, charge suspends **below** this) | 46.35 | 47.25 | **48.15 %** |

The cold side has 22 percentage points of margin. **The hot side has only 1.85 pp** against the worst-case threshold. With ideal 1 % resistors the divider ratio can reach 49.5 %, still clear. With 5 % resistors it can reach **47.5 %, which is inside the hot-trip band** — the charger would then refuse to charge and blink the LED, for no reason at all. The BOM does not record the tolerance of `R17`/`R18` **[BOM]**. If you are debugging a ZeroWriter that will not charge and blinks its LED, **measure `TS` against `REGN` before anything else**: it should be 50 % ± 1 %. **[INF]**

## 7. What firmware can see: nothing

This is the most important integration fact on the page.

`STAT` is an open-drain output with three states **[DOC §9.3.3, Table 9-2]**:

| Charging state | `STAT` |
|---|---|
| Charging in progress (including recharge) | **LOW** |
| Charging complete | **HIGH** (open) |
| HiZ, sleep, or charge disabled | **HIGH** (open) |
| Safety timer expired **with** `VBAT` above recharge threshold | **HIGH** (open) |
| Any fault — input OVP, TS cold/hot, battery OVP, thermal shutdown, safety timer expired with `VBAT` below recharge threshold, `ICHG` pin open/short, `FB` pin open/short | **BLINKING at 1 Hz, 50 % duty** |

On this board the `CHRG-ST` net goes to test point `TP50` and out of the board on `K1` pin 1 of the 16-pin inter-board connector **[SCH]**. Following it onto the breakout board **[SCH `Zerowriter breakout board.kicad_sch`]**:

```
REGN  ──(not used)
VUSB ──[ R3 2k2 ]── D1 anode ── D1 (LTST-S270EKT) ── D1 cathode ── CHRG-ST ── K3.1 ─┄┄ K1.1 ─┄┄ U12 pin 3 STAT
```

That is the whole story. **`STAT` drives one LED on the breakout board and goes nowhere else.** It is not connected to any ESP32 GPIO, not to the PCAL6416A expander, and not to the keyboard processor.

| Consequence | |
|---|---|
| **Firmware cannot read charge state** | Not "charging", not "complete", not "fault". There is no path |
| **Firmware cannot detect a charging fault** | A blinking LED is the *only* indication of TS fault, battery OVP, input OVP, thermal shutdown or safety-timer expiry |
| **The only battery telemetry that exists** is the analogue battery-voltage divider on `V_BAT` → **ESP32-WROVER `IO35`** (ADC1_CH7), gated by a MOSFET the firmware enables via `V_BAT_MOS` **[SCH `MCU.kicad_sch`]** | So "is it charging?" has to be *inferred* from the battery voltage trend, or from USB presence |
| A string scan of the shipped SD-1.3 main-board firmware found no charger-related strings **[FW]** | Weak evidence — register-free hardware needs no strings — but consistent with there being nothing to read |
| ZeroWriter publishes **no main-board firmware source** (only the keyboard sketch `src/keyboard/zwi_kb_feb2026/`) **[SRC]** | So how the shipped firmware presents battery state cannot be established from source |

Two deviations from TI's guidance in the LED circuit, neither harmful:

- TI says *"Connect this pin to REGN via a current limiting resistor and LED"* **[DOC Table 7-1]**. ZeroWriter pulls up to **`VUSB` (5 V)** instead. `STAT`'s abs max is 5.5 V, so this is legal but has no headroom, and it means the LED is dark whenever USB is absent — which is arguably the desired behaviour anyway. **[INF]**
- LED current ≈ (5 V − ~2 V) / 2.2 kΩ ≈ **1.4 mA**, well inside the 6 mA `ISTAT_SINK` limit. ✅ **[INF]**

## 8. Power path: yes, it runs without a battery

The brief question "can the system run with a dead or absent battery?" has a clear answer here, and it is **not** provided by the BQ25306.

The BQ25306 is a **standalone charger without power path** — TI's own Figure 10-1 topology **[DOC §10.2.1]**. There is no `SYS` pin. The buck output is the `BAT` node and nothing else.

ZeroWriter provides the power path with discrete parts, in a block the schematic labels **"AUTO SOURCE SELECTION"** **[SCH]**:

```
VUSB ──┬──────────────── D10 (BAT20J Schottky) ──┬── SW_IN ──[Q4 SSM3J358R]── VIN ──[U6 TPS7A2633]── 3V3
       │                                          │              ▲
       │                                          │              └─ gated by PWR_SW (slide switch S1 on the breakout)
       ├──[R36 100k]── GND                        │
       └────── Q7 gate                            │
                                                  │
VBAT ──────────[Q7 SSM3J358R P-MOSFET]────────────┘
```

- **USB present:** `VUSB` holds `Q7`'s gate high → `Q7` off. `D10` conducts, so `SW_IN` ≈ `VUSB` − ~0.4 V ≈ **4.6 V**.
- **USB absent:** `R36` pulls `Q7`'s gate to GND → `Q7` on → `SW_IN` ≈ `VBAT`.
- `VBAT` (max 4.18 V) never exceeds `SW_IN` while on USB, so `Q7`'s body diode does not conduct backwards. **[INF]**

| Question | Answer |
|---|---|
| **Does the device run from USB with no battery fitted?** | **Yes.** `D10` feeds the system from `VUSB` directly. The charger is not in the system's supply path at all |
| Does the system load steal charge current? | **No.** While on USB the system is fed through `D10`; the charger's 2 A goes to the pack. Input current is charge current *plus* system current, both drawn from `VUSB` |
| Does the device run from USB with a **deeply discharged** pack? | **Yes** — same reason. But see below for what happens to the pack |
| Can the charger recover a deeply discharged pack? | **Slowly.** Below 2.00 V the charger delivers only **35 mA**; between 2.00 V and 2.93 V it delivers 200 mA. A pack sitting at 1.5 V takes hours to climb through trickle before precharge even starts |
| What about pack-side protection? | If the pack's protection FET has latched off on undervoltage, the BQ25306 sees an open circuit. Whether ZeroWriter's pack has a protection board, and whether it recovers on applied charge voltage, is **not established** |

## 9. Practical guidance

### 9.1 Estimating charge time

There is no gas gauge and no charge-state telemetry, so charge time has to be estimated. With `ICHG` = 2.0 A and `ITERM` = 200 mA (a 10:1 ratio, so a long CV tail):

```
t_CC  ≈  (0.75 × C_Ah) / I_CC              CC phase, roughly to 4.18 V
t_CV  ≈  0.5 h to 1.0 h                    taper from ICHG down to ITERM
t_tot ≈  t_CC + t_CV
```

Worked example for a hypothetical 5 Ah pack, starting near empty, with the full 2 A available:

```
t_CC  ≈ (0.75 × 5.0) / 2.0        = 1.9 h
t_CV  ≈                             ~0.8 h
t_tot ≈                             ~2.7 h
```

Three things will make the real number larger, and all three are invisible to the user:

1. **VINDPM foldback** on a lossy cable (§5). This is the big one.
2. **Thermal regulation** at `TREG` = 120 °C junction, which also *disables termination* and halves the timer rate (§9.2).
3. Charging from a 500 mA or 900 mA USB port.

**ZeroWriter's pack capacity is not published and is not in the BOM** — `K4` is only a `JST-2pin-SMD` **[BOM]**. Substitute your own measured capacity.

### 9.2 The safety timers, and the batteryless corner case

`tSAFETY_FAST` = 20 h (15–24 h), `tSAFETY_PRE` = 2 h (1.5–2.5 h) **[DOC §8.6]**. The timer resets on **[DOC §9.3.2.5]**: battery falling below the recharge threshold, `VBUS` recycled, `/EN` toggled (impossible here — `/EN` is hard-tied), or the battery crossing `VBAT_SHORT` or `VBAT_LOWV`.

- During **input-current or thermal regulation** the timer counts at **half rate** — the fast-charge timer effectively becomes 40 h.
- During **TS fault, VBUS OVP, VBAT OVP, ICHG open/short, FB fault or thermal shutdown** the timer is **suspended** entirely and resumes when the fault clears.
- Expiry with `VBAT` **above** recharge threshold → charge suspended, `STAT` **open** (LED off, looks like "done").
- Expiry with `VBAT` **below** recharge threshold → charge suspended, `STAT` **blinking** (fault).

**With no battery fitted:** the converter regulates the open `BAT` node to 4.18 V with whatever small leakage load exists. Current never falls below `ITERM` if anything is loading it, so it never terminates, and after 20 h the safety timer expires. The node then decays below the 4.03 V recharge threshold, which resets the timer and restarts charging. **Expect a slow ~20-hour cycling behaviour, not a hard failure.** The system itself keeps running from `D10` throughout, so this is invisible. **[INF — reasoned from §9.3.2.4/§9.3.2.5, not observed]**

### 9.3 Thermal sanity check

At 5 V in, 4.0 V battery, 2 A charge current and TI's stated 92.5 % efficiency **[DOC §1]**:

```
P_out  = 4.0 V × 2.0 A            = 8.0 W
P_in   = 8.0 / 0.925              = 8.65 W
P_loss = 8.65 − 8.0               = 0.65 W
ΔT_J   = 0.65 W × 45.8 °C/W       = 30 °C
```

So `TJ` ≈ 55 °C at 25 °C ambient — comfortably under `TREG` = 120 °C. **[INF]**

Caveat: 45.8 °C/W is the **JEDEC high-K four-layer** figure **[DOC §8.4]**. A small, densely packed board inside a sealed 15 mm-thick plastic enclosure with a 5.2 " e-paper panel over it is not a JEDEC board. TI's own note is explicit that the thermal pad must be tied to a ground plane with vias **[DOC Table 7-1]**. Treat 30 °C rise as an optimistic floor, and note that the *enclosure* temperature — not the die — is what the thermal-regulation loop is implicitly protecting.

Input current at that operating point is 8.65 W / 5 V ≈ **1.73 A**, *plus* the system load (ESP32-WROVER, e-paper PMIC, keyboard processor) which flows through the same `VUSB` net. A ~2 A total draw from a USB-C port is fine for a 3 A source and marginal for anything less.

### 9.4 Bring-up and debug checklist

Everything is configured by resistors, so debugging is a voltmeter exercise:

| Measure | Expect | If wrong |
|---|---|---|
| `REGN` (`C59`) | 4.2 – 5.0 V with USB in | No `REGN` → `VBUS` below `VVBUS_LOWV` (3.9 V), or the part is disabled |
| `TS` ÷ `REGN` | **50 % ± 1 %** | Outside 48.2–72.7 % → charger latched in TS fault, LED blinking |
| `ICHG` pin | ~**0.998 V** (`VICHG`) | 0 V or open → `STAT` blinks and the converter never starts **[DOC §9.3.4.4]** |
| `R25` | 20 kΩ | Determines charge current, `ICHG = 40000/R` |
| `FB` pin | ~**1.10 V** when in CV | `FB` shorted or open → converter stops, `STAT` blinks |
| `R29`/`R28` | 280 kΩ / 100 kΩ | Determines `VBATREG = 1.1 × (1 + R29/R28)` |
| `/EN` pin | **0 V** | Should be hard-tied |
| `POL` pin | = `VBUS` | See §3.2 |
| `SW` node | 1.2 MHz switching while charging | Not switching → in termination, sleep, HiZ or fault |
| LED `D1` on the breakout | solid = charging, off = done/idle, **1 Hz blink = fault** | Blink is the only fault indication that exists |

### 9.5 Safety considerations

1. **No battery temperature sensing.** §6. If you repack the device with a different cell, understand that nothing on the board will stop it charging at −10 °C or at 60 °C.
2. **Charging cannot be disabled.** `/EN` is hard-tied. There is no firmware kill switch, and the slide switch does not stop charging.
3. **The regulation voltage is set by two undocumented-tolerance resistors.** §3.1. If you respin, specify 1 % or better explicitly.
4. **Do not feed anything but 5 V into `VUSB`.** The 1 µH inductor is sized for < 6.2 V (§3), and `POL` is rated 5.5 V (§3.2). The IC's 17 V capability is not available on this board.
5. **If you increase `ICHG`**, check the pack's C-rate first (2 A into a 2 Ah cell is 1 C — acceptable for many but not all cells), then re-run §9.3, then confirm the inductor's saturation rating: TI requires `ISAT ≥ ICHG + ½ × IRIPPLE` **[DOC eq. 3]**, and `SRP3212A-1R0M`'s rating is not recorded in the BOM.
6. **Never fit a resistor to the `ICHG` pin's node other than `RICHG`.** *"No capacitor is allowed to connect at this pin"* **[DOC Table 7-1]** — the pin is a current-mirror reference, and a capacitor there is a fault condition, not a filter.

## 10. Alternatives

| Part | Trade-off vs BQ25306 |
|---|---|
| **BQ25306** (fitted) | Standalone, resistor-programmed, 17 V tolerant, 3 A, 200 nA battery leakage, WQFN-16. **No I²C, no power path, no gas gauge** |
| `MCP73831T` | What Soldered fits on the stock Inkplate 5 / Gen 2. Linear, SOT-23-5, one resistor. Simple and cheap, but caps out around 500 mA before thermal limits bite |
| [**BQ25895**](../bq25895/README.md) | **I²C**, integrated power path with a `SYS` output, ADC for VBUS/VBAT/ICHG/TS, OTG boost, D+/D− USB adapter detection. **This is what you fit if you want firmware to know anything.** More pins, more BOM, more code |
| BQ24074 / BQ24075 | True power path (`SYS` rail independent of the battery) but **linear**, so back to the thermal ceiling |
| BQ25302 / BQ25305 | Same `RTE` package family (`BQ2530x` in the thermal table). The BQ25302 is 1-cell only, 4.1–6.2 V in, fixed charge voltages, 2.0 A max **[DOC §6]** — which on paper covers everything this board actually does except the 4.18 V setpoint. **Read their own datasheets; do not assume pin compatibility** |
| Any part + a fuel gauge (BQ27441, MAX17048) | The orthogonal fix: keep the dumb charger, add I²C state-of-charge sensing on the pack |

**On this board none are drop-in**: the footprint is WQFN-16 RTE with a thermal pad, and there is no I²C stub or spare GPIO routed to the charger block. Adding charge-state visibility to an existing ZeroWriter without a respin means tapping `CHRG-ST` at `TP50` and wiring it to a spare input — which is entirely feasible, since `STAT` is already a clean open-drain signal brought out to a test point.

## 11. Open questions

| Question | Status |
|---|---|
| Battery pack capacity, chemistry, cell count and protection circuit | **Unknown.** `K4` is a bare `JST-2pin-SMD` in the BOM; no pack part number is published anywhere. This blocks any real charge-time or C-rate statement |
| Tolerance of `R25`, `R28`, `R29`, `R17`, `R18` | **Not recorded.** BOM lists values and a generic `0603R` footprint only. TI requires ≥ 1 % for the FB divider and the `ICHG` resistor **[DOC]** |
| `SRP3212A-1R0M` saturation current | **Not recorded.** Needed to verify TI's `ISAT ≥ ICHG + ½ IRIPPLE` |
| Behaviour with `POL` tied high | **Undocumented by TI.** §3.2. The product charges, so the *floating* interpretation appears to hold, but this is inference |
| `F1` on the breakout board, `SMD1206-350-6V` | **Ambiguous.** Under the common `SMD<size>-<Ihold×10 mA>-<V>` convention this reads **3.5 A hold / 6 V**; a "350 mA" reading would be flatly inconsistent with a 2 A charge current plus system load. Soldered's own Gen 2 fuse is spelled out as `1206FUSE-500mA` **[BOM]**, so the naming convention differs between the two designs. **Not resolved; 3.5 A is the plausible reading** **[INF]** |
| Why the sheet says `ICHG:3A` next to a 20 kΩ resistor | **Unexplained.** Most likely a stale annotation from a 3 A iteration. §3.2 |
| How the shipped firmware presents battery state | **Not establishable.** No main-board source is published; only binaries **[SRC]** |
| Silicon date code / lot on a physical unit | **Unknown.** No board photograph at sufficient resolution is retained here |

## Manufacturer

**Texas Instruments** — see the [Texas Instruments documentation-sourcing guide](../../../vendors/texas-instruments/README.md) for this vendor's document portals, URL patterns, part-numbering conventions, distribution channels and known gotchas.

## Used By

- [ZeroWriter Ink](../../../devices/zerowriter/zerowriter-ink/README.md) — reference designator `U12` on the respun "Zerowriter Inkplate 5 Gen2" main board. **ZeroWriter-specific addition**; replaces the `MCP73831T` linear charger of the stock design. Programmed for **2.0 A** fast charge at **4.18 V**, `/EN` hard-tied enabled, no thermistor, `STAT` to an LED on the breakout board only
- **Not** fitted on [Soldered Inkplate 5](../../../devices/soldered-electronics/inkplate-5/README.md) or [Soldered Inkplate 5 Gen 2](../../../devices/soldered-electronics/inkplate-5-gen2/README.md) — both use `MCP73831T` at `U4` **[BOM]**

## Related pages

- [texas-instruments/bq25895](../bq25895/README.md) — the I²C-controlled alternative, for comparison
- [texas-instruments/tps65186](../tps65186/README.md) — the e-paper PMIC sharing the same board and battery
- [nxp/pcal6416a](../../nxp/pcal6416a/README.md) — the I²C expander; note the charger is **not** behind it, because it has no digital interface at all
- [nxp/pcf85063a](../../nxp/pcf85063a/README.md) — the RTC, the other part that determines this device's standby drain
- [espressif/esp32-wrover](../../espressif/esp32-wrover/README.md) — reads battery voltage on `IO35`, the only battery telemetry that exists
- [wch/ch340c](../../wch/ch340c/README.md) — shares the `VUSB` rail

## Authoritative sources

| Title | URL | Retrieved | Version | Local artifact |
|---|---|---:|---|---|
| BQ25306 datasheet | https://www.ti.com/lit/gpn/BQ25306 | 2026-08-26 | **`SLUSDC7A`**, March 2020, rev. November 2020 · 2,781,845 B · `sha256:8a70d122…7ac2a5` | [artifacts/bq25306-datasheet.pdf](artifacts/bq25306-datasheet.pdf) |
| BQ25306 product folder (lifecycle = ACTIVE) | https://www.ti.com/product/BQ25306 | 2026-08-26 | — | — |
| ZeroWriter Ink main-board schematic, sheet 3/8 "BATTERY CHARGER" (`U12`, `R17`, `R18`, `R25`, `R28`, `R29`, `L3`, `C37`–`C39`, `C58`–`C62`) | https://github.com/zerowriter/zerowriter_ink | 2026-08-24 | KiCad v1.2.0, sheet dated 2025-06-30 | `../../../devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter_ink/design/src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/CTRL & COMS.kicad_sch` |
| Same, plotted | — | 2026-08-26 | page 3 of 8 | `.../Zerowriter Inkplate 5 Gen2/v1.2.0/OUTPUTS/Zerowriter Inkplate 5 Gen2 Schematics.pdf` |
| ZeroWriter Ink main-board BOM (`U12 BQ25306RTER`, `L3 SRP3212A-1R0M`, `U4 USBLC6-2SC6`) | — | 2026-08-24 | v1.2.0 | `.../Zerowriter Inkplate 5 Gen2/v1.2.0/OUTPUTS/Zerowriter Inkplate 5 Gen2.csv` |
| ZeroWriter breakout-board schematic (`D1` charge LED, `R3` 2k2 to `VUSB`, `F1`, USB-C `K1`) | — | 2026-08-26 | v1.2.0 | `.../Zerowriter breakout board/v1.2.0/CAD/Zerowriter breakout board.kicad_sch` |
| ZeroWriter breakout-board BOM | — | 2026-08-26 | v1.2.0 | `.../Zerowriter breakout board/v1.2.0/OUTPUTS/Zerowriter breakout board.csv` |
| Soldered Inkplate 5 Gen 2 BOM (`U4 MCP73831T`, `F1 1206FUSE-500mA`) — evidence the BQ25306 is **not** in the stock design | — | 2026-08-24 | V1.1.0 | `../../../devices/soldered-electronics/inkplate-5-gen2/artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/OUTPUTS/V1.1.0/Soldered Inkplate 5 Gen2 BOM.csv` |
| Soldered Inkplate 5 BOM (`U4 MCP73831T`) | — | 2026-08-24 | V1.2.0 | `../../../devices/soldered-electronics/inkplate-5/artifacts/hardware/soldered-inkplate-5-hardware-design/OUTPUTS/V1.2.0/Soldered Inkplate 5 BOM.csv` |
| ZeroWriter shipped main-board firmware (string scan; no charger strings found) | — | 2026-08-26 | SD-1.3 | `.../zerowriter_ink/firmware_releases/SD-1.3/firmware.bin` |
| Crowd Supply campaign (battery-life claim) | https://www.crowdsupply.com/zerowriter/zerowriter-ink | 2026-08-24 | — | — |
