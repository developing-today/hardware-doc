# Texas Instruments BQ25895

> Single-cell Li-ion switch-mode charger, NVDC power path, integrated ADC telemetry and a 3.1 A boost (OTG) converter, all under I²C control.
> Research snapshot **2026-08-30**. Fitted as `U15` on the Nicolai Electronics Tanmatsu. **No hardware was available** — every claim below is traced to the datasheet, the published KiCad design, or the coprocessor firmware source.

---

## Evidence labelling

| Tag | Meaning |
|---|---|
| **[DOC]** | TI datasheet **SLUSC88C**, March 2015, revised **October 2022** — local copy `artifacts/bq25895-datasheet-slusc88c.pdf` |
| **[PCB]** | `tanmatsu.kicad_pcb` net/pad assignments, from the published `tanmatsu-hardware` KiCad design (CERN-OHL-P) |
| **[SRC]** | Tanmatsu coprocessor firmware, `pmic.c` / `pmic_regs.h` (MIT), snapshot in the device tree |
| **[INF]** | Inference by the author, flagged as such |

Nothing here is `executed-success` or hardware-tested. Everything is `reported-working` (vendor firmware ships and the product functions) or `inferred`.

---

## 1. Identity, variants and lifecycle

| Property | Value | Source |
|---|---|---|
| Full part | **BQ25895RTWR** (tape/reel) — the Tanmatsu BOM says `BQ25895RTW` | BOM, [DOC] |
| Marketing name | "I²C Controlled Single Cell 5-A Fast Charger with MaxCharge™ for High Input Voltage and Adjustable Voltage 3.1-A Boost Operation" | [DOC] p.1 |
| Package | **WQFN-24 (RTW)**, 4.00 × 4.00 mm, exposed thermal pad | [DOC] §Device Information |
| Datasheet revision | **SLUSC88C** — original March 2015, latest revision October 2022 | [DOC] |
| Lifecycle | Active. Long-lived part; the 2015→2022 revision span is documentation maintenance, not silicon churn | [DOC] |
| LCSC | [`C80200`](https://www.lcsc.com/search?q=C80200) | BOM |
| I²C address | **0x6A** (7-bit), fixed — not strappable | [DOC], [SRC] `pmic.c:13` |
| Device ID | REG14 `PN[2:0] = 111`, `DEV_REV = 01` | [DOC] Table 8-26 |

### 1.1 Family members and what actually differs

The BQ2589x family shares one register map and one driver, and differs in the analog corners. Confusing them is the usual mistake:

| Part | Charge current | Boost | Notable difference |
|---|---|---|---|
| **BQ25895** | 5 A | 3.1 A, 4.55–5.51 V | The part documented here. `PN = 111` |
| BQ25896 | 3 A | 2.15 A | Lower current, otherwise near-identical register map. `PN = 000` |
| BQ25890 | 5 A | 1.2 A | No MaxCharge / HVDCP handshake |
| BQ25895M | 5 A | 3.1 A | Factory-set defaults differ (aimed at 9 V adapters); **same silicon, different EEPROM defaults** |

> ⚠ **`PN[2:0]` is the only reliable runtime discriminator.** Read REG14 and check for `111`. A driver written for the BQ25896 will happily enumerate a BQ25895 and then set charge currents that read back wrong, because the current step sizes differ.

---

## 2. Absolute maximum and recommended limits **[DOC §7.1, §7.3, §7.5]**

| Parameter | Min | Max | Unit | Note |
|---|---:|---:|---|---|
| VBUS (converter not switching) | −2 | **22** | V | Survives 22 V; regulates only to 14 V |
| PMID | −0.3 | 22 | V | |
| STAT, DSEL, BTST | −0.3 | 20 | V | |
| SW | −2 | 16 | V | −3 V for ≤10 ns transients |
| BAT, SYS | −0.3 | **6** | V | Note the much lower rating than VBUS |
| SDA, SCL, INT, OTG, REGN, TS, CE, QON | −0.3 | **7** | V | |
| ILIM | −0.3 | 5 | V | |
| Junction temperature | −40 | 150 | °C | |
| **VBUS operating range** | **3.9** | **14** | V | Outside this it will not charge |
| VBUS OVP (`VACOV`) rising | 14 | 14.6 | V | Falling 13.5–14 V |
| VBUS for active I²C, no battery | **3.6** | — | V | Below this the chip will not answer |
| VBAT for active I²C, no VBUS | **2.3** | — | V | |

**Quiescent current** — this is what makes ship mode worth using **[DOC §7.5]**:

| Condition | Typ | Max |
|---|---:|---:|
| High-Z, no VBUS, **BATFET disabled** (`REG09[5]=1`), battery monitor off | **12 µA** | 23 µA |
| High-Z, no VBUS, BATFET enabled, battery monitor off | 32 µA | 60 µA |
| Leakage between BAT and VBUS, VBUS < UVLO | 5 µA | — |
| VBUS present, converter not switching | 1.5 mA | 3 mA |
| Boost mode, no load, switching | 5 mA | — |

The ~20 µA difference between BATFET-off and BATFET-on is the entire argument for ship mode: on a 1500 mAh cell it is roughly 8 years versus 5 years of shelf life, and it is why the Tanmatsu's power-off path sets `BATFET_DIS`.

**Thermal** **[DOC §7.4]**: R<sub>θJA</sub> = 31.8 °C/W, R<sub>θJC(bot)</sub> = 2.0 °C/W. The exposed pad is the only meaningful heat path — R<sub>θJC(top)</sub> is 27.9 °C/W, so airflow over the package body does very little. At 3 A charge and ~91 % efficiency you are dissipating on the order of 1 W, which is ≈32 °C rise on a board with a poor pad. This is why the internal thermal regulation loop (`TREG`) matters in practice rather than being a formality.

**Accuracy** **[DOC §1]**: charge voltage ±0.5 %, charge current ±5 %, input current ±7.5 %. The charge-voltage figure is the one that matters for cell life; ±0.5 % of 4.2 V is ±21 mV.

---

## 3. Register map **[DOC §8.4, Tables 8-8 … 8-26]**

21 registers, `00h`–`14h`, all 8-bit. Auto-increment on sequential read **is** supported.

| Addr | Name | Contents | Reset by |
|---|---|---|---|
| `00h` | Input source | `EN_HIZ`, `EN_ILIM`, `IINLIM[5:0]` | REG_RST only |
| `01h` | Boost temp / VINDPM offset | `BHOT[1:0]`, `BCOLD`, `VINDPM_OS[4:0]` | REG_RST; BHOT/BCOLD also by watchdog |
| `02h` | ADC & detection | `CONV_START`, `CONV_RATE`, `BOOST_FREQ`, `ICO_EN`, `HVDCP_EN`, `MAXC_EN`, `FORCE_DPDM`, `AUTO_DPDM_EN` | mixed — see below |
| `03h` | Charger control | `BAT_LOADEN`, `WD_RST`, `OTG_CONFIG`, `CHG_CONFIG`, `SYS_MIN[2:0]`, *reserved* | **REG_RST + watchdog** |
| `04h` | Fast charge current | `EN_PUMPX`, `ICHG[6:0]` | **REG_RST + watchdog** |
| `05h` | Pre-charge / termination | `IPRECHG[3:0]`, `ITERM[3:0]` | **REG_RST + watchdog** |
| `06h` | Charge voltage | `VREG[5:0]`, `BATLOWV`, `VRECHG` | **REG_RST + watchdog** |
| `07h` | Timers | `EN_TERM`, `STAT_DIS`, `WATCHDOG[1:0]`, `EN_TIMER`, `CHG_TIMER[1:0]`, *reserved* | **REG_RST + watchdog** |
| `08h` | IR comp / thermal | `BAT_COMP[2:0]`, `VCLAMP[2:0]`, `TREG[1:0]` | **REG_RST + watchdog** |
| `09h` | Misc control | `FORCE_ICO`, `TMR2X_EN`, `BATFET_DIS`, *rsvd*, `BATFET_DLY`, `BATFET_RST_EN`, `PUMPX_UP`, `PUMPX_DN` | mixed — **BATFET bits are software-only** |
| `0Ah` | Boost voltage | `BOOSTV[3:0]`, 4 reserved | REG_RST + watchdog |
| `0Bh` | **Status (RO)** | `VBUS_STAT[2:0]`, `CHRG_STAT[1:0]`, `PG_STAT`, `SDP_STAT`, `VSYS_STAT` | — |
| `0Ch` | **Fault (RO)** | `WATCHDOG_FAULT`, `BOOST_FAULT`, `CHRG_FAULT[1:0]`, `BAT_FAULT`, `NTC_FAULT[2:0]` | latched, see §3.3 |
| `0Dh` | VINDPM | `FORCE_VINDPM`, `VINDPM[6:0]` | REG_RST |
| `0Eh` | **ADC: VBAT (RO)** | `THERM_STAT`, `BATV[6:0]` | — |
| `0Fh` | **ADC: VSYS (RO)** | `SYSV[6:0]` | — |
| `10h` | **ADC: TS (RO)** | `TSPCT[6:0]` | — |
| `11h` | **ADC: VBUS (RO)** | `VBUS_GD`, `VBUSV[6:0]` | — |
| `12h` | **ADC: ICHG (RO)** | `ICHGR[6:0]` | — |
| `13h` | **ADC: IDPM (RO)** | `VDPM_STAT`, `IDPM_STAT`, `IDPM_LIM[5:0]` | — |
| `14h` | ID / reset | `REG_RST`, `ICO_OPTIMIZED`, `PN[2:0]`, `TS_PROFILE`, `DEV_REV[1:0]` | — |

### 3.1 Scaling constants — the numbers you actually need **[DOC Tables 8-8 … 8-24]**

Every multi-bit field is a plain weighted binary sum on top of an offset. Real values, not approximations:

| Field | Offset | Bit weights (MSB→LSB) | Range | Reset default |
|---|---:|---|---|---|
| `IINLIM[5:0]` | 100 mA | 1600 / 800 / 400 / 200 / 100 / 50 mA | 100 mA – 3250 mA | — |
| `VINDPM_OS[4:0]` | 0 mV | 1600 / 800 / 400 / 200 / 100 mV | 0 – 3100 mV | **500 mV (00101)** |
| `SYS_MIN[2:0]` | **3.0 V** | 0.4 / 0.2 / 0.1 V | 3.0 – 3.7 V | **3.5 V (101)** |
| `ICHG[6:0]` | 0 mA | 4096 / 2048 / 1024 / 512 / 256 / 128 / 64 mA | 0 – **5056 mA** | **2048 mA (0100000)** |
| `IPRECHG[3:0]` | **64 mA** | 512 / 256 / 128 / 64 mA | 64 – 1024 mA | **128 mA (0001)** |
| `ITERM[3:0]` | **64 mA** | 512 / 256 / 128 / 64 mA | 64 – 1024 mA | **256 mA (0011)** |
| `VREG[5:0]` | **3.840 V** | 512 / 256 / 128 / 64 / 32 / **16 mV** | 3.840 – **4.608 V** | **4.208 V (010111)** |
| `BOOSTV[3:0]` | **4.55 V** | 512 / 256 / 128 / 64 mV | 4.55 – 5.51 V | **5.126 V (1001)** |
| `VCLAMP[2:0]` | 0 mV | 128 / 64 / 32 mV | 0 – 224 mV | 0 mV |
| `BAT_COMP[2:0]` | 0 mΩ | 80 / 40 / 20 mΩ | 0 – 140 mΩ | 0 mΩ |
| `VINDPM[6:0]` | **2.6 V** | 6400 / 3200 / 1600 / 800 / 400 / 200 / 100 mV | 2.6 – 15.3 V | — |
| **ADC** `BATV[6:0]` | **2.304 V** | 1280 / 640 / 320 / 160 / 80 / 40 / **20 mV** | 2.304 – 4.848 V | — |
| **ADC** `SYSV[6:0]` | **2.304 V** | same as BATV | 2.304 – 4.848 V | — |
| **ADC** `VBUSV[6:0]` | **2.6 V** | 6400 / 3200 / 1600 / 800 / 400 / 200 / **100 mV** | 2.6 – 15.3 V | — |
| **ADC** `ICHGR[6:0]` | **0 mA** | 3200 / 1600 / 800 / 400 / 200 / 100 / **50 mA** | 0 – 6350 mA | — |
| **ADC** `TSPCT[6:0]` | **21 %** | 29.76 / 14.88 / 7.44 / 3.72 / 1.86 / 0.93 / **0.465 %** | 21 – 80 % of REGN | — |
| `IDPM_LIM[5:0]` | 100 mA | same weights as `IINLIM` | 100 – 3250 mA | — |

Two hardware clamps worth knowing, because they make readback disagree with what you wrote: `ICHG > 1001111` is clamped to 5056 mA, and `VREG > 110000` is clamped to 4.608 V **[DOC Tables 8-12, 8-14]**.

### 3.2 Enumerated fields, verbatim **[DOC Tables 8-9, 8-15, 8-16, 8-19, 8-20]**

```
REG0B  VBUS_STAT[2:0]   000 No input          001 USB Host SDP
                        010 USB CDP (1.5 A)   011 USB DCP (3.25 A)
                        100 Adjustable HV DCP (MaxCharge) (1.5 A)
                        101 Unknown adapter (500 mA)
                        110 Non-standard adapter (1 A / 2 A / 2.1 A / 2.4 A)
                        111 OTG
REG0B  CHRG_STAT[1:0]   00 Not charging   01 Pre-charge (<VBATLOWV)
                        10 Fast charging  11 Charge termination done
REG0C  CHRG_FAULT[1:0]  00 Normal
                        01 Input fault (VBUS>VACOV, or VBAT<VBUS<3.8 V)
                        10 Thermal shutdown
                        11 Charge safety-timer expiration
REG0C  NTC_FAULT[2:0]   Buck mode:  000 Normal  001 TS Cold  010 TS Hot
                        Boost mode: 000 Normal  101 TS Cold  110 TS Hot
REG07  WATCHDOG[1:0]    00 Disable   01 40 s (default)   10 80 s   11 160 s
REG07  CHG_TIMER[1:0]   00 5 h   01 8 h   10 12 h (default)   11 20 h
REG08  TREG[1:0]        00 60 °C   01 80 °C   10 100 °C   11 120 °C (default)
REG01  BHOT[1:0]        00 34.75 % (default)  01 37.75 %  10 31.25 %  11 disable boost thermal protection
```

### 3.3 Reset defaults you will trip over

Three reset defaults surprise people, and all three are *enabled*:

- **`OTG_CONFIG` defaults to 1 — OTG boost ENABLED.** A freshly reset BQ25895 with no VBUS will attempt to boost the battery onto VBUS. If your board's OTG pin is not also asserted this is inert (both the `OTG` pin and `OTG_CONFIG` must agree), but on a board that ties `OTG` high it is not.
- **`CHG_CONFIG` defaults to 1 — charging ENABLED.**
- **`WATCHDOG` defaults to 01 — 40 s.** See §6.

---

## 4. The TS pin, and why it is usually the first thing a board gets wrong **[DOC §7.5, §9]**

TS is a ratiometric input: the chip compares V(TS) against percentages of the **REGN LDO**, which is 5.6 / **6.0** / 6.4 V when VBUS is present **[DOC §7.5]**. TI's recommended network is a 103AT-2 (10 kΩ @ 25 °C) NTC in a divider from REGN to TS to GND **[DOC §9]**.

Thresholds, as percentage of REGN **[DOC §7.5]**:

| Threshold | Meaning | Min | Typ | Max |
|---|---|---:|---:|---:|
| `V(LTF)` | **Cold**, TS rising | 72.75 % | **73.25 %** | 73.75 % |
| `V(LTF_HYS)` | Cold hysteresis, falling | — | 0.4 % | — |
| `V(HTF)` | **Hot**, TS rising | 47.75 % | **48.25 %** | 48.75 % |
| `V(TCO)` | Cut-off, TS falling | 44.25 % | **44.75 %** | 45.25 % |

The permitted window is therefore roughly **48.25 % < V(TS)/V(REGN) < 73.25 %**. Charging suspends when TS leaves it — silently, from firmware's point of view, unless you read `NTC_FAULT`.

---

## 5. Exact wiring on the Tanmatsu **[PCB]**

Pad-by-pad, straight from the published PCB netlist:

| Pin | Name | Net | Notes |
|---:|---|---|---|
| 1 | VBUS | `VBUS` | From the USB-C connector |
| **2** | **D+** | **unconnected** | ⚠ see §5.1 |
| **3** | **D−** | **unconnected** | ⚠ see §5.1 |
| 4 | STAT | `Net-(U15-STAT)` → **R45 1 kΩ** | Open-drain charge-status indicator |
| 5 | SCL | `/Coprocessor/PM_SCL` | Private bus to the CH32V203 |
| 6 | SDA | `/Coprocessor/PM_SDA` | |
| 7 | INT | `/Coprocessor/PM_INT` | Wired, but see §5.4 |
| 8 | SYS | `VSYS` | System rail |
| 9, 17, 18, 25 | GND / pad | `GND` | Pin 25 is the exposed thermal pad |
| **10** | **ILIM** | `Net-(U15-ILIM)` → **R48 261 Ω** to GND | see §5.2 |
| **11** | **TS** | `Net-(U15-TS)` → **R51 10 kΩ** to REGN, **R50 10 kΩ** to GND | ⚠ see §5.3 |
| **12** | **QON** | `/Coprocessor/POWER_BTN` | see §5.5 |
| 13, 14 | BAT | `VBATT` | |
| 15, 16 | SYS | `VSYS` | |
| 19, 20 | SW | `/Power/b2l` | → **L**, and **D85** (SMD24PL-TP Schottky) to `VOTG` |
| 21 | BTST | `Net-(U15-BTST)` → **C44 47 nF** to SW | Bootstrap cap; datasheet value |
| 22 | REGN | `Net-(U15-REGN)` → **C47 4.7 µF** to GND | Datasheet minimum |
| 23 | PMID | `VOTG` | The 5 V OTG rail — see §5.6 |
| **24** | **DSEL** | **unconnected** | |

### 5.1 ⚠ D+/D− are not connected, so USB source detection cannot work

`D+` and `D−` are left floating **[PCB]**. Every input-type detection feature therefore has nothing to work with:

- `AUTO_DPDM_EN` (REG02[0], default **enabled**) — the automatic BC1.2 / PSEL detection that runs on VBUS insertion.
- `FORCE_DPDM` (REG02[1]) — manual re-trigger of the same.
- `HVDCP_EN` (REG02[3], default enabled) and `MAXC_EN` (REG02[2], default enabled) — the high-voltage adapter handshakes, which work by pulsing D+/D−.
- `VBUS_STAT[2:0]` in REG0B — will not report SDP/CDP/DCP meaningfully.

**Consequence:** the board can never negotiate more than the default input current, and `VBUS_STAT` should be treated as uninformative. The input current limit must be set explicitly by firmware (which is what `pmic_set_input_current_limit()` is for), and the ILIM resistor is the real backstop. The coprocessor firmware **does** expose setters for `hvdcp_en`, `maxc_en`, `auto_dpdm_en` and `force_dpdm` **[SRC]** `pmic.c:127–220` — they will all write successfully and do nothing observable on this board.

### 5.2 ILIM: 261 Ω, and the limit is *not* 1.5 A

`IINMAX = K_ILIM / R_ILIM`, and `K_ILIM` is specified as **320 / 355 / 390 A·Ω** (min/typ/max) **[DOC §7.5]**.

With R48 = 261 Ω:

| K_ILIM | IINMAX |
|---|---:|
| min 320 | **1.226 A** |
| **typ 355** | **1.360 A** |
| max 390 | 1.494 A |

The comment in the vendor header — `// Enable input current limit (ILIM) of 1.5A (260Ω)` **[SRC]** `pmic_regs.h:14` — is computed from the **maximum** K_ILIM and is therefore optimistic. The typical hardware ceiling is about **1.36 A**, and a worst-case part limits at **1.23 A**. If you are budgeting simultaneous charging and 5 V OTG load, use 1.2 A, not 1.5 A.

Note also that ILIM only clamps; the *effective* limit is the lower of ILIM and `IINLIM[5:0]`, and only when `EN_ILIM = 1` **[DOC §8.3.3]**.

### 5.3 ⚠ There is no thermistor — TS is tied to a fixed 50 % divider

R51 = 10 kΩ (REGN→TS) and R50 = 10 kΩ (TS→GND) **[PCB]**. Both are fixed resistors; **no NTC is fitted**. V(TS) is therefore pinned at **50.0 % of REGN** regardless of battery temperature.

Two consequences, one benign and one not:

1. **Battery temperature protection is defeated by design.** The pack's thermal safety rests entirely on whatever protection circuit is inside the cell assembly, plus the BQ25895's own *die* thermal regulation (`TREG`, a completely different mechanism that measures the chip, not the cell). Any firmware presenting "battery temperature" to a user from this board would be fabricating it.

2. ⚠ **50 % is uncomfortably close to the hot threshold.** `V(HTF)` is 47.75–48.75 % of REGN. The design margin is therefore only **1.25 to 2.25 percentage points**. With 1 % resistors the divider itself is 50 % ± 0.5 pp, leaving as little as **0.75 pp** of margin on a worst-case part. A resistor drifting high on R50, or a REGN measurement offset, lands on a spurious **`NTC_FAULT = TS Hot`** and charging stops with no obvious cause. [INF] — I have not measured a board; this is a tolerance-stack reading of the datasheet against the BOM values.

   If you are debugging a Tanmatsu that will not charge, read REG0C first. The coprocessor does surface this: `out_faults->ntc_hot` **[SRC]** `pmic.c:1146`.

### 5.4 INT is wired but the firmware polls

Pin 7 goes to `/Coprocessor/PM_INT` **[PCB]**, and badge.team's pinout documents it as coprocessor `PB9`. However the shipped coprocessor firmware contains **no interrupt handler for it** and no reference to `PM_INT` in `hardware.h` **[SRC]**; `main.c` polls the PMIC on a timer instead. The signal is available if you rewrite the coprocessor firmware; it is not used today.

### 5.5 QON is the power button — this is the whole soft-power design

The net `/Coprocessor/POWER_BTN` connects **four** things **[PCB]**:

| Ref | Pin | Role |
|---|---|---|
| `U15` | 12 (**QON**) | BQ25895 BATFET wake / full-system-reset input |
| `U12` | 33 | CH32V203 coprocessor GPIO |
| `SW3` | 1 | The physical **power button** |
| `Q4` | 3 | AP2302B N-channel MOSFET, drain — lets the coprocessor pull the net down |
| `TP6` | 1 | Test point, silkscreened **`~{QON}`** — confirming the identification |

So: pressing the power button pulls QON low, which is exactly the BQ25895's documented exit-from-ship-mode mechanism **[DOC §8.3.6]**, *and* is simultaneously readable by the coprocessor as a button press. `Q4` lets firmware assert the same line. `BATFET_RST_EN` (REG09[2], default **enabled**) means a long QON press performs a full system reset — a hardware-level recovery path that works even if both processors are wedged.

### 5.6 PMID/`VOTG` powers more than the USB-A port

`VOTG` (pin 23, PMID) feeds **[PCB]**:

| Ref | Part | Role |
|---|---|---|
| `U27`–`U32` | **6 × SK6805** | The addressable RGB LEDs — all six run from 5 V |
| `U26` | 74LVC1G17GW | Schmitt buffer level-shifting LED data from 3.3 V to 5 V |
| `U14` | SY6280AAC | The USB-A host port power switch |
| `J7` pin 1 | Internal add-on port | 5 V out to expansion boards |
| `C49`, `C51`, `C53`, `C54`, `C55` | 5 × 10 µF | Bulk decoupling |
| `D85` | SMD24PL-TP Schottky | From SW to VOTG |

> ⚠ **The RGB LEDs cannot light unless the boost converter is running.** `OTG_CONFIG` (REG03[5]) must be set — and, on the Tanmatsu, that means asking the coprocessor, since the ESP32-P4 has no path to the PMIC. This is a non-obvious coupling: "turn on an LED" is transitively "enable a 5 V boost converter", with its ~5 mA quiescent cost **[DOC §7.5]** on top of the LED current itself.

---

## 6. The watchdog — the classic trap, and how this board sidesteps it

This is the single most common way to lose a day with a BQ25895.

**The mechanism [DOC Tables 8-11 … 8-17]:** REG07 `WATCHDOG[1:0]` defaults to `01` = **40 s**. If no I²C transaction resets it within that window, the chip sets `WATCHDOG_FAULT` in REG0C and **resets REG03 through REG09 to their power-on defaults**. Every register in that range is marked `Reset by Watchdog` in the datasheet's Type column.

**What that costs you concretely:**

| Register | Reverts to | Practical effect |
|---|---|---|
| `REG04 ICHG` | 2048 mA | Your carefully chosen charge current is gone |
| `REG06 VREG` | **4.208 V** | Float voltage jumps to 4.208 V — above a conservative 4.10 V or 4.15 V setting |
| `REG06 BATLOWV` | 3.0 V | |
| `REG05 ITERM` | 256 mA | |
| `REG03 SYS_MIN` | 3.5 V | |
| `REG03 CHG_CONFIG` | **Charge enabled** | Charging you deliberately stopped restarts |
| `REG03 OTG_CONFIG` | **OTG enabled** | The boost converter turns itself back on |
| `REG07 CHG_TIMER` | 12 h | |
| `REG08 TREG` | 120 °C | Thermal regulation loosens |

Note the asymmetry that trips people the other way: **the naive expectation is "charging stops if firmware stops petting it", but the actual behaviour is the opposite** — a watchdog expiry re-enables charging and OTG at default settings. `EN_HIZ` (REG00) is *not* watchdog-reset **[DOC Table 8-8: `R/W by REG_RST` only]**, so a HIZ'd input stays HIZ'd; but the BATFET bits in REG09 are likewise software-only, so ship mode also survives.

**Petting it:** write `WD_RST` (REG03[6]) = 1. It self-clears. `pmic_reset_watchdog()` **[SRC]** `pmic.c:337` does a read-modify-write of REG03 and sets the bit, which is correct.

**What the Tanmatsu does:** `main.c:816` calls `pmic_set_watchdog_timer_limit(0)` during initialisation, with the comment `// Disable PMIC I2C watchdog` **[SRC]**. The watchdog is therefore **off for the life of the session**, and none of the above applies on this board.

That is a legitimate design choice — the coprocessor is the only I²C master and has nothing else to do — but it is a *trade*: there is now **no failsafe if the coprocessor firmware hangs**. A wedged CH32V203 leaves the charger in whatever state it was last commanded into, indefinitely. With the watchdog enabled the chip would at least fall back to safe defaults.

---

## 7. Driver audit — Tanmatsu coprocessor firmware vs. SLUSC88C

Method per [`hardware-device-research` §10](../../../.agents/skills/hardware-device-research/SKILL.md): every constant, field offset and sequence in `pmic.c` / `pmic_regs.h` was decoded against the datasheet register tables.

**Overall:** `pmic_regs.h` is an accurate, complete transcription of the register map — all 21 registers, correct bit positions and widths, including the reserved bits. It is better than most vendor headers. The defects are all in `pmic.c`.

### 7.1 🔴 `pmic_get_charge_voltage_limit()` never returns a value — `pmic.c:637`

```c
pmic_result_t pmic_get_charge_voltage_limit(uint16_t* out_voltage) {
    ...
    if (out_voltage) {
        uint16_t voltage = 3840;
        if (value.vreg & (1 << 5)) { voltage += 512; }
        ...
        if (value.vreg & (1 << 0)) { voltage += 16; }
    }                       // <-- `voltage` goes out of scope here
    return PMIC_OK;         // <-- *out_voltage was never assigned
}
```

The local `voltage` is computed correctly and then discarded. **`*out_voltage` is left holding whatever the caller's uninitialised stack contained**, and the function reports `PMIC_OK`. Contrast the sibling `pmic_get_boost_mode_voltage()` at `pmic.c:1055`, which writes through the pointer directly and is correct.

- **Status:** live defect, though currently unexercised — no caller in the shipped `main.c` reads back the charge voltage limit.
- **Consequence if used:** any host querying the float voltage through the coprocessor's register file gets garbage. Anyone adding a battery-settings UI hits this immediately.
- **Fix:** add `*out_voltage = voltage;` before the closing brace.

### 7.2 🟠 Five value encoders use `>` where they must use `>=` — off-by-one-LSB on every exact multiple

The file uses a greedy binary decomposition to convert engineering units into register bit weights. Five functions compare with `>` instead of `>=`, so whenever the running remainder lands **exactly** on a bit weight, that bit is skipped and the error cascades:

| Function | Lines | Field | [DOC] |
|---|---|---|---|
| `pmic_set_minimum_system_voltage_limit` | `pmic.c:257, 262, 267` | `SYS_MIN` | Table 8-11 |
| `pmic_set_termination_current` | `pmic.c:463, 467, 471, 475` | `ITERM` | Table 8-13 |
| `pmic_set_precharge_current` | `pmic.c:513, 517, 521, 525` | `IPRECHG` | Table 8-13 |
| `pmic_set_charge_voltage_limit` | `pmic.c:610–632` | `VREG` | Table 8-14 |

The correct form is used elsewhere in the same file — `pmic_set_input_current_limit` (`:35–58`), `pmic_set_charge_current_fast` (`:372–399`), `pmic_set_boost_mode_voltage` (`:1036–1051`), `pmic_set_vindpm` (`:1163–1190`) and the REG08 helpers all use `>=`. So this is a transcription slip in five places, not a deliberate convention.

**Worked consequences, all reachable from shipped code:**

| Call site | Requested | Actually programmed | Error |
|---|---|---|---|
| `pmic_configure_battery_charger()` `pmic.c:1459` | `VREG` **4200 mV** | `010110` = 3840+256+64+32 = **4192 mV** | −8 mV |
| `pmic_battery_attached()` `pmic.c:1420` | `SYS_MIN` **3700 mV** | `110` = **3600 mV** | −100 mV |
| `pmic_battery_attached()` `pmic.c:1436` | `SYS_MIN` **3500 mV** ("back to the default") | `100` = **3400 mV** | −100 mV |
| (any caller) | `ITERM` 256 mA | `0010` = **192 mA** | −64 mA |

The `SYS_MIN` errors are the most consequential: the comment at `pmic.c:1436` says "Set minimum system voltage back to the default 3.5 v" and it does not — the board is left at 3.4 V after every empty-battery detection attempt. One full LSB below intent. The `VREG` error is −8 mV on a ±0.5 % (±21 mV) specification, so it is inside the part's own tolerance and harmless in practice; the `SYS_MIN` error is a whole step and is not.

- **Status:** live, exercised on every boot that runs battery detection.
- **Fix:** change `>` to `>=` in the four functions listed. A regression test that round-trips every representable value through set/get would have caught all of them.

### 7.3 🟠 `pmic_power_off()` calls the *getter* where it means the setter — `pmic.c:1381`

```c
pmic_result_t pmic_power_off() {
    pmic_result_t res;
    res = pmic_get_watchdog_timer_limit(0);  // Disable watchdog timer
```

`pmic_get_watchdog_timer_limit(uint8_t* out_seconds)` with `out_seconds = NULL` performs one I²C read of REG07, writes nothing, and returns `PMIC_OK`. The intended call is `pmic_set_watchdog_timer_limit(0)`. The comment states the intent unambiguously; the code does not implement it.

- **Status:** **latent, not live.** `main.c:816` already disables the watchdog at start-up, so by the time `pmic_power_off()` runs there is nothing left to disable. This is a trap, not a current bug — exactly the distinction worth preserving.
- **When it would bite:** if initialisation order changed, if `REG_RST` (REG14[7]) were ever asserted (which restores `WATCHDOG` to 40 s), or if this function were reused on a board that keeps the watchdog enabled. Then the device would enter ship mode with a live 40 s watchdog, and REG03–REG09 would revert to defaults 40 s later — including `OTG_CONFIG = enabled`. `BATFET_DIS` is software-only and would survive **[DOC Table 8-17]**, so the unit would stay off; but the boost converter's control bit would be re-armed.
- **Fix:** one character class — `pmic_set_watchdog_timer_limit(0)`.

### 7.4 🟡 `pmic_set_input_voltage_limit_offset()` takes a raw register code, not millivolts — `pmic.c:86`

```c
pmic_result_t pmic_set_input_voltage_limit_offset(uint8_t offset) {
    ...
    value.vindpm_os = offset;   // written straight through
```

Every other setter in the file takes engineering units (`uint16_t` millivolts or milliamps) and encodes them. This one takes the raw 5-bit `VINDPM_OS` code in an oddly-typed `uint8_t`, with a name that reads exactly like the millivolt setters. A caller passing `500` — the datasheet default of 500 mV, and the obvious thing to pass — gets `500 & 0x1F = 20`, i.e. **2000 mV**, four times the intended offset **[DOC Table 8-9]**.

- **Status:** latent; no caller in the shipped firmware.
- **Fix:** either rename to `..._offset_raw()` or convert millivolts using the 1600/800/400/200/100 mV weights, matching the rest of the file.

### 7.5 🟡 `BOOST_FREQ` writes are silently dropped while OTG is enabled — `pmic.c:149`

`pmic_set_otg_boost_frequency()` does a read-modify-write of REG02[5]. The datasheet states plainly: *"Write to this bit is ignored when OTG_CONFIG is enabled"* **[DOC Table 8-10]**. Since `OTG_CONFIG` **defaults to enabled**, a driver that sets the boost frequency before explicitly disabling OTG will have the write discarded with no error, and no readback check exists to notice.

- **Status:** latent trap in the API contract.
- **Fix:** document the ordering requirement, or have the function disable OTG, write, and restore.

### 7.6 🟡 ADC stop ordering is ambiguous — `pmic.c:222`, called from `pmic.c:1383`

`pmic_set_adc_configuration(bool start, bool continuous)` writes `CONV_START` and `CONV_RATE` in a single byte. The datasheet says `CONV_START` *"is read-only when CONV_RATE = 1"* **[DOC Table 8-10]**. `pmic_power_off()` calls `pmic_set_adc_configuration(false, false)`, attempting to clear both at once. Whether the part evaluates the read-only condition against the pre-write or post-write state of `CONV_RATE` is not specified.

- **Status:** unresolved ambiguity, not a confirmed defect. [INF]
- **Safe pattern:** clear `CONV_RATE` in one write, then clear `CONV_START` in a second.

### 7.7 ✅ Things the driver gets right, so nobody "fixes" them

- **`NTC_FAULT` decoding — `pmic.c:1145–1147`.** The expressions `(ntc_fault & 3) == 1` for cold, `== 2` for hot, and `(ntc_fault >> 2) & 1` for boost-mode look like a hack but are exactly correct: buck codes are `001`/`010` and boost codes are `101`/`110`, so the low two bits carry the cold/hot sense in both modes and bit 2 carries the mode **[DOC Table 8-20]**. This is a genuinely elegant reading of an awkward encoding.
- **All bitfield offsets and widths in `pmic_regs.h`** match the datasheet, including reserved bits at REG03[0], REG07[0], REG09[4] and REG0A[3:0], and the read-modify-write discipline preserves them.
- **`ICHG` and `IINLIM` encoders** saturate correctly at the register maxima (5056 mA and 3250 mA) rather than wrapping.
- **`CHG_TIMER`, `WATCHDOG` and `TREG` enum mappings** are all correct against Tables 8-15 and 8-16, including the non-obvious `CHG_TIMER = 00 → 5 h`.

### 7.8 Summary

| # | Severity | Location | Defect | Live? |
|---|---|---|---|---|
| 7.1 | 🔴 High | `pmic.c:637` | `pmic_get_charge_voltage_limit` never assigns `*out_voltage` | Yes (unexercised) |
| 7.2 | 🟠 Medium | `pmic.c:257,262,267,463…,513…,610…` | `>` instead of `>=` in 5 encoders; SYS_MIN off by a full 100 mV step | **Yes, exercised** |
| 7.3 | 🟠 Medium | `pmic.c:1381` | Getter called instead of setter; watchdog not disabled at power-off | Latent |
| 7.4 | 🟡 Low | `pmic.c:86` | Raw register code behind a millivolt-shaped name | Latent |
| 7.5 | 🟡 Low | `pmic.c:149` | `BOOST_FREQ` write ignored while OTG enabled | Latent |
| 7.6 | 🟡 Low | `pmic.c:222` | ADC stop ordering vs. `CONV_RATE` read-only rule | Ambiguous |

None of these has been reported upstream by this record's author. `pmic.c` is MIT-licensed; the fixes for 7.1, 7.2 and 7.3 are each one line.

---

## 8. Drivers and libraries

### 8.1 What ships on the Tanmatsu

| Layer | Where | Notes |
|---|---|---|
| Register access | `coprocessor-firmware/pmic.c`, `pmic_regs.h` (MIT) | ~1470 lines, full register coverage; audited above |
| Host-facing API | `i2c_registers.h` — `I2C_REG_PMIC_*` | The ESP32-P4 sees **engineering units**, not raw registers |
| ESP-IDF component | `tanmatsu_coprocessor.c` / `.h` | Talks to the coprocessor at 0x5F |

The coprocessor republishes telemetry as 16-bit little-endian values **[SRC]** `i2c_registers.h:110–130`:

```
I2C_REG_PMIC_ADC_VBAT_0/_1    battery voltage, mV
I2C_REG_PMIC_ADC_VSYS_0/_1    system voltage, mV
I2C_REG_PMIC_ADC_VBUS_0/_1    input voltage, mV
I2C_REG_PMIC_ADC_ICHGR_0/_1   charge current, mA
I2C_REG_PMIC_ADC_TS_0/_1      TS as % of REGN ×100
I2C_REG_PMIC_FAULT            REG0C, passed through
I2C_REG_PMIC_COMM_FAULT       set when the coprocessor's own I²C to the PMIC fails
I2C_REG_PMIC_CHARGING_CONTROL / _STATUS
I2C_REG_PMIC_OTG_CONTROL
I2C_REG_PMIC_POWER_CONTROL
```

> ⚠ **`I2C_REG_PMIC_ADC_TS_*` is meaningless on this board** — it will always read ≈5000 (50.00 %) because of the fixed divider in §5.3. Do not present it as a temperature.

### 8.2 Other options if you are using this part elsewhere

| Driver | Language / framework | Notes |
|---|---|---|
| **Linux** `drivers/power/supply/bq25890_charger.c` | Kernel, mainline | Covers BQ25890/2/5/6/7 via `compatible = "ti,bq25895"`. Mature, uses the `power_supply` class and devicetree properties like `ti,charge-current`. The best reference implementation. |
| **Zephyr** `drivers/charger/charger_bq25180.c` | — | Different part; **not** compatible. No mainline Zephyr BQ25895 driver as of this snapshot. |
| **`sqfmi/bq25895` / various Arduino ports** | Arduino | Community quality varies widely; several transcribe the BQ25896 current steps. Check `ICHG` weights against Table 8-12 before trusting one. |
| Roll your own | any | The register map is small and fully public; ~300 lines gets you everything. Given the state of the community drivers this is often the right call. |

TI publishes no reference C driver for this part, only the datasheet and EVM documentation.

---

## 9. Initialisation and integration pitfalls, in priority order

1. **Decide the watchdog policy before anything else.** Either pet it on a timer comfortably inside 40 s, or disable it (`WATCHDOG = 00`) and accept that you have no failsafe. Doing neither means your settings evaporate 40 s after boot. §6.
2. **Read `PN[2:0]` from REG14 and confirm `111`.** The family shares an address and a register map but not the current scaling. §1.1.
3. **`OTG_CONFIG` and `CHG_CONFIG` default to enabled.** If your board must not boost, clear REG03[5] explicitly during init rather than assuming.
4. **Check REG0C before believing anything else.** A `TS Hot` or `Input fault` explains most "it won't charge" reports, and none of it is visible from the charge-status bits alone.
5. **`VREG` resolution is 16 mV.** 4.20 V is not representable; the nearest values are 4.192 V and 4.208 V. Decide which side of 4.2 V you want and set it deliberately.
6. **The ADC is one-shot by default.** `CONV_RATE = 0` means you get a single conversion per `CONV_START`. Continuous mode (`CONV_RATE = 1`) runs at 1 Hz and costs quiescent current. Reading the ADC registers without triggering a conversion returns stale data.
7. **Sequential reads auto-increment**, so REG0B–REG13 can be slurped in one transaction — worth doing, since the status and ADC values are then coherent with each other.
8. **`FORCE_ICO` and `PUMPX_UP`/`PUMPX_DN` self-clear.** Do not poll them expecting them to stay set; poll `ICO_OPTIMIZED` (REG14[6]) instead.
9. **ILIM and `IINLIM` are ANDed, not ORed.** The effective limit is the lower of the two, and ILIM only participates when `EN_ILIM = 1`. If your measured input current is lower than you programmed, check the resistor. §5.2.

---

## 10. Alternatives

| Part | vs. BQ25895 | When to prefer it |
|---|---|---|
| **BQ25896** | 3 A charge, 2.15 A boost, same registers | Smaller batteries; cheaper; identical firmware effort |
| **BQ25792** | 1–4 cell, USB-PD-friendly, dual-input | Multi-cell, or if you need PD negotiation |
| **[BQ25306](../bq25306/README.md)** | Much simpler, no boost, no ADC | Documented in this repository. When you want charging and nothing else |
| **MP2762A** | Similar class, narrower supply | Cost-driven second source |
| **BQ25798** | Adds MPPT for solar | Energy-harvesting inputs |

The BQ25895's distinguishing features are the **integrated ADC** (removes a separate fuel gauge for coarse work) and the **boost converter** (removes a separate 5 V supply for a USB host port). If you need neither, this part is over-specified and BQ25306-class silicon is cheaper and easier.

⚠ It is *not* a fuel gauge. It measures VBAT, VSYS, VBUS and charge current; it does **not** do coulomb counting, and state-of-charge estimated from open-circuit voltage alone is worth roughly ±15 % under load. If you need real SoC, add a BQ27xxx or MAX17xxx.

---

## 11. Open questions

- The `D85` Schottky (SMD24PL-TP) from `SW` to `VOTG` **[PCB]** is not part of TI's reference application. Its purpose — most plausibly a clamp or a bootstrap aid — is not documented by the vendor. Reading the schematic sheet graphically rather than via the netlist would settle it.
- Whether the shipped Tanmatsu units have the same 261 Ω ILIM resistor as the published BOM has not been verified against hardware.
- The tolerance-margin concern in §5.3 is analytic. Measuring V(TS)/V(REGN) on a real board and comparing against the 48.25 % threshold would confirm or dismiss it.
- No upstream issue has been filed for the §7 defects.

---

## Manufacturer

**Texas Instruments** — see [`vendors/texas-instruments/README.md`](../../../vendors/texas-instruments/README.md) for documentation-sourcing patterns. Relevant here: the datasheet is at the guessable, session-free URL `https://www.ti.com/lit/ds/symlink/bq25895.pdf`, which is how the local copy was obtained on 2026-08-30.

## Used By

| Device | Ref | Role |
|---|---|---|
| [Nicolai Electronics Tanmatsu](../../../devices/nicolai-electronics/tanmatsu/README.md) | `U15` | Battery charging, power path, ADC telemetry, soft power-on via QON, and the 5 V OTG rail that feeds the USB-A port, the RGB LEDs and the add-on connector. Reachable **only** through the CH32V203 coprocessor at I²C 0x5F. See [`bom.md`](../../../devices/nicolai-electronics/tanmatsu/bom.md), [`pinouts-and-buses.md`](../../../devices/nicolai-electronics/tanmatsu/pinouts-and-buses.md) §1.2, [`keyboard.md`](../../../devices/nicolai-electronics/tanmatsu/keyboard.md) §1.10 |

## Related pages

- [`components/wch/ch32v203c8t6/README.md`](../../wch/ch32v203c8t6/README.md) — the coprocessor that owns this chip
- [`components/normand/sk6805-ec20/README.md`](../../normand/sk6805-ec20/README.md) — powered from this chip's PMID rail
- [`components/texas-instruments/tps63020/README.md`](../tps63020/README.md) — the buck-boost downstream on VSYS
- [`components/texas-instruments/bq25306/README.md`](../bq25306/README.md) — the simpler charger, for comparison
- [`components/generic/charger-power-path/README.md`](../../generic/charger-power-path/README.md)

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | BQ25895 datasheet | Texas Instruments | primary | datasheet | <https://www.ti.com/lit/ds/symlink/bq25895.pdf> | 2026-08-30 | **SLUSC88C**, Mar 2015 rev. Oct 2022, 65 pp, 2 681 280 B | Complete register map, all scaling constants, electricals, TS thresholds, K_ILIM, watchdog semantics | `artifacts/bq25895-datasheet-slusc88c.pdf` |
| D2 | BQ25895 product folder | Texas Instruments | primary | official page | <https://www.ti.com/product/BQ25895> | 2026-08-30 | — | Lifecycle status, package options | — |
| S1 | Tanmatsu coprocessor firmware — `pmic.c` (1468 lines), `pmic_regs.h` (252 lines), `main.c`, `i2c_registers.h` | Nicolai Electronics | primary | repository | in-tree snapshot | 2026-08-26 | MIT, SPDX-FileCopyrightText 2024-2025 | Vendor register interpretation; all §7 defects; watchdog policy | `devices/nicolai-electronics/tanmatsu/artifacts/source-snapshots/coprocessor-firmware/` |
| S2 | Tanmatsu KiCad design — `tanmatsu.kicad_pcb`, `power.kicad_sch` | Nicolai Electronics | primary | repository | in-tree snapshot | 2026-08-24 | `tanmatsu-hardware` @ `640805dd`, CERN-OHL-P | Every net and pad in §5; R48/R50/R51/C44/C47/D85 values | `devices/nicolai-electronics/tanmatsu/artifacts/schematics/kicad/` |
| S3 | Tanmatsu production BOM | Nicolai Electronics | primary | repository | in-tree snapshot | 2026-08-24 | CERN-OHL-P | `U15 = BQ25895RTW`, LCSC C80200 | `devices/nicolai-electronics/tanmatsu/artifacts/production/bom.csv` |

**Method note.** D1 was fetched with `curl` and a Chrome 131 User-Agent, validated as `%PDF`, 65 pages. TI serves datasheets to bare `curl` without difficulty; no fallback was needed. Register values in §3 were extracted from the PDF text layer and cross-checked against the bit positions in `pmic_regs.h`; the two agree throughout.
