# NXP PCF85063A (PCF85063ATL)

- **Category:** **tiny CMOS real-time clock / calendar**, I²C, with alarm, countdown timer, programmable clock output and offset (aging) trim
- **Reference designator:** `U7` on **all three** boards — [Inkplate 5](../../../devices/soldered-electronics/inkplate-5/README.md), [Inkplate 5 Gen 2](../../../devices/soldered-electronics/inkplate-5-gen2/README.md), [ZeroWriter Ink](../../../devices/zerowriter/zerowriter-ink/README.md)
- **Package fitted: `DFN2626-10` (SOT1197-1) → the `PCF85063ATL` variant.** Established from the PCB footprint (10 signal pads + an exposed die paddle) and the 10-pin schematic symbol with `CLKOE` on pin 3 — the SO8 and TSSOP8 variants have no `CLKOE` pin
- **Companion part:** `X1`, a 32.768 kHz tuning-fork crystal whose identity is **ambiguous in the BOM** — see §4.2
- **I²C address:** **`0x51`** (7-bit) / `A2h` write, `A3h` read. **Fixed, not strappable.** Direct on the ESP32's `Wire` bus — **not** behind the [PCAL6416A](../pcal6416a/README.md) expander
- **Owning MCU:** ESP32-WROVER, `IO21` = SDA / `IO22` = SCL. Interrupt lands on **`IO39`**
- **Research status:** register map, oscillator behaviour, board wiring on all three variants, backup path and the Inkplate driver's behaviour established from primary sources. The crystal's actual load capacitance is **unresolved and matters** (§4)
- **Retrieved:** 2026-08-24. Datasheet re-read, all three schematics parsed pin-by-pin and the Inkplate Arduino RTC driver audited line-by-line 2026-08-26

## Evidence labelling

| Label | Meaning |
|---|---|
| **[DOC]** | NXP datasheet — `PCF85063A`, **Rev. 7, 30 March 2018**, Product data sheet |
| **[SCH]** | Read from the published KiCad schematics (Soldered Inkplate 5 V1.2.0, Inkplate 5 Gen 2 V1.1.0, ZeroWriter Inkplate 5 Gen2 v1.2.0) and the plotted schematic PDFs |
| **[PCB]** | Read from the published `.kicad_pcb` layout |
| **[BOM]** | KiCad BOM CSV exports |
| **[SRC]** | Inkplate Arduino library source, **v11.1.4** |
| **[FW]** | String scan of a shipped firmware binary |
| **[INF]** | Inference. Reasoning and arithmetic are always shown |

---

## 1. Identity, variants and lifecycle

The whole family shares one datasheet **[DOC §4]**:

| Type number | Package | Pins | Has `CLKOE`? | Marking | Orderable |
|---|---|---:|---|---|---|
| `PCF85063AT` | SO8 (SOT96-1) | 8 | no | `85063A` | `PCF85063AT/AY` (13") · `PCF85063AT/AAZ` (7") |
| **`PCF85063ATL`** | **DFN2626-10 (SOT1197-1)**, 2.6 × 2.6 × 0.5 mm | **10** | **yes** | `063A` | **`PCF85063ATL/1,118`** · 12NC `935299022118` · 7" tape and reel |
| `PCF85063ATT` | TSSOP8 (SOT505-1) | 8 | no | `063A` | `PCF85063ATT/AJ` (13") |

**Only the `ATL` has the `CLKOE` pin.** The Inkplate schematic symbol has ten pins with `CLKOE` on pin 3 and `n.c.` on pin 8 — exactly the `ATL` pinout **[SCH]** — and the PCB footprint `Soldered footprints:PCF85063A` has **ten 0.7 × 0.25 mm signal pads plus one unnumbered 1.1 × 2.3 mm pad with no net** **[PCB]**. That unnumbered pad is the DFN's exposed die paddle. **The fitted part is `PCF85063ATL`, IC revision 1.**

NXP's guidance on that paddle is worth repeating because the board follows it: *"The die paddle (exposed pad) is connected to VSS through high ohmic (non-conductive) silicon attach and should be electrically isolated… In no case should traces be run under the package exposed pad."* **[DOC Table 4 note 1]** Soldered leaves the pad netless. ✅

**Lifecycle:** NXP's product page returns an **Active** status as of 2026-08-26 and the part is listed under NXP's product-longevity programme **[WEB]**.

### 1.1 Do not confuse it with the PCF85063B or the PCF8563

Three near-neighbours cause real bugs:

| Part | Interface | Relationship |
|---|---|---|
| `PCF85063A` | **I²C** | This part |
| `PCF85063B` | **SPI** | Same feature set, different bus, DFN2626-10 only. Same-looking part number |
| `PCF85063TP` | I²C | **No alarm at all.** "Basic functions only" **[DOC Table 45]** |
| [`PCF8563`](#12-alternatives-and-how-they-differ) | I²C | **Same 7-bit address `0x51`.** Completely different register offsets. See §12 |

## 2. Electrical characteristics and limits **[DOC §12, §13]**

### 2.1 Limiting values **[DOC §12, Table 40]**

| Parameter | Min | Max | Unit |
|---|---:|---:|---|
| `VDD` supply voltage | −0.5 | **+6.5** | V |
| `VI` input voltage (SCL, SDA, OSCI, CLKOE) | −0.5 | +6.5 | V |
| `II` / `IO` input / output current | −10 | +10 | mA |
| `Ptot` total power dissipation | — | 300 | mW |
| ESD HBM | — | **5000** | V |
| ESD CDM (`ATL`) | — | 1750 | V |
| `Tamb` operating | −40 | +85 | °C |

> **⚠ NXP's reflow warning, and it applies directly to this board.** *"NXP recommends not to bias the PCF85063A device during reflow (e.g. if utilizing a 'coin' type battery in the assembly). If customer so chooses to continue to use this assembly method, there must be the allowance for a full '0 V' level Power supply 'reset' to re-enable the device. Without a proper POR, the device may remain in an indeterminate state."* **[DOC Table 40 note 1]** All three boards have a CR2032 holder wired straight through a diode to `VDD` (§5.3). See §6.2 for why this makes the software reset non-optional.

### 2.2 Static characteristics **[DOC §13, Table 41]**

Conditions: `VDD` 0.9–5.5 V, `Tamb` −40 to +85 °C, `fosc` = 32.768 kHz, quartz `Rs` = 60 kΩ, `CL` = 7 pF.

| Symbol | Parameter | Min | Typ | Max | Unit |
|---|---|---:|---:|---:|---|
| `VDD` | supply, interface inactive (`fSCL` = 0) | **0.9** | — | 5.5 | V |
| `VDD` | supply, interface active at 400 kHz | **1.8** | — | 5.5 | V |
| `IDD` | CLKOUT disabled, `VDD` = 3.3 V, interface inactive, 25 °C | — | **220** | 450 | nA |
| `IDD` | same at 50 °C | — | 250 | 500 | nA |
| `IDD` | same at 85 °C | — | 470 | 600 | nA |
| `IDD` | interface active, `fSCL` = 400 kHz | — | **18** | 50 | µA |
| `VIL` / `VIH` | input thresholds | −0.5 / 0.7·`VDD` | — | 0.3·`VDD` / 5.5 | V |
| `VOL` | on SDA, INT, CLKOUT | `VSS` | — | 0.2·`VDD` | V |
| `VOH` | on CLKOUT (push-pull) | 0.8·`VDD` | — | `VDD` | V |
| `IOL` | sink at `VOL` = 0.4 V, `VDD` = 3.3 V — **SDA** | 3 | 8.5 | — | mA |
| `IOL` | same — **INT** | **2** | 6 | — | mA |
| `IOL` | same — CLKOUT | 1 | 3 | — | mA |
| `Ci` | input capacitance | — | — | 7 | pF |
| `Δfosc/fosc` | relative oscillator frequency variation for a 200 mV `VDD` change, 25 °C | — | **0.075** | — | ppm |
| **`CL(itg)`** | **integrated load capacitance, `CAP_SEL` = 0** | 4.2 | **7** | 9.8 | pF |
| **`CL(itg)`** | **integrated load capacitance, `CAP_SEL` = 1** | 7.5 | **12.5** | 17.5 | pF |
| `Rs` | crystal series resistance | — | — | **100** | kΩ |

Three of these deserve emphasis:

- **220 nA typical.** At `VDD` = 3.3 V, 25 °C, CLKOUT off. This is what lets a battery e-paper device keep time for years off a CR2032. But note the **max is 450 nA — twice the typical** — and the typical **doubles again by 85 °C**. Budget against 600 nA if the device lives in a car.
- **The I²C interface is 5 V tolerant** **[DOC Table 41 note 5]**. That matters on this board, where the bus pull-ups are on a *higher* rail than the RTC's own `VDD` (§5.4).
- **`CL(itg)` is the *series* combination of the two internal pin capacitors**: `CL(itg) = (COSCI × COSCO) / (COSCI + COSCO)` **[DOC Table 41 note 7]**. This is the key to §4, and it is easy to get wrong.

### 2.3 I²C **[DOC §9.5]**

| Item | Value |
|---|---|
| Max data rate | **400 kbit/s** (Fast-mode) |
| 7-bit slave address | **`1010001` = `0x51`** — fixed, one address per bus |
| Address byte | `A2h` write, `A3h` read |
| Register address field | **5 bits**; the upper 3 bits of the register-address byte are ignored |
| Auto-increment | after every read or write byte, **wrapping from `11h` back to `00h`** |
| Registers | 18 |

## 3. Register map **[DOC Table 5, Table 8]**

Every value below is transcribed from the datasheet. POR/software-reset defaults in the right-hand column.

| Addr | Register | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 | Reset |
|---:|---|---|---|---|---|---|---|---|---|---:|
| `00h` | **`Control_1`** | `EXT_TEST` | – | `STOP` | `SR` | – | `CIE` | `12_24` | **`CAP_SEL`** | `0x00` |
| `01h` | **`Control_2`** | `AIE` | `AF` | `MI` | `HMI` | `TF` | `COF[2]` | `COF[1]` | `COF[0]` | `0x00` |
| `02h` | **`Offset`** | `MODE` | `OFFSET[6:0]` | | | | | | | `0x00` |
| `03h` | `RAM_byte` | `B[7:0]` — free byte, no hardware function | | | | | | | | `0x00` |
| `04h` | **`Seconds`** | **`OS`** | `SECONDS` BCD 0–59 | | | | | | | **`0x80`** |
| `05h` | `Minutes` | – | `MINUTES` BCD 0–59 | | | | | | | `0x00` |
| `06h` | `Hours` | – | – | `AMPM`¹ | `HOURS` BCD | | | | | `0x00` |
| `07h` | `Days` | – | – | `DAYS` BCD 1–31 | | | | | | `0x01` |
| `08h` | `Weekdays` | – | – | – | – | – | `WEEKDAYS` 0–6 | | | `0x06` |
| `09h` | `Months` | – | – | – | `MONTHS` BCD 1–12 | | | | | `0x01` |
| `0Ah` | `Years` | `YEARS` BCD 0–99 | | | | | | | | `0x00` |
| `0Bh` | `Second_alarm` | `AEN_S` | `SECOND_ALARM` BCD | | | | | | | **`0x80`** |
| `0Ch` | `Minute_alarm` | `AEN_M` | `MINUTE_ALARM` BCD | | | | | | | **`0x80`** |
| `0Dh` | `Hour_alarm` | `AEN_H` | – | `AMPM`¹ | `HOUR_ALARM` BCD | | | | | **`0x80`** |
| `0Eh` | `Day_alarm` | `AEN_D` | – | `DAY_ALARM` BCD | | | | | | **`0x80`** |
| `0Fh` | `Weekday_alarm` | `AEN_W` | – | – | – | – | `WEEKDAY_ALARM` | | | **`0x80`** |
| `10h` | `Timer_value` | `T[7:0]` | | | | | | | | `0x00` |
| `11h` | **`Timer_mode`** | – | – | – | `TCF[1]` | `TCF[0]` | `TE` | `TIE` | `TI_TP` | **`0x18`** |

¹ `AMPM` exists only in 12-hour mode (`12_24` = 1).

Reset state of the clock: **00:00:00, 2000-01-01, Saturday** **[DOC §8.2.1.3]**.

### 3.1 `Control_1` (`00h`) bit meanings **[DOC Table 6]**

| Bit | Name | 0 | 1 |
|---:|---|---|---|
| 7 | `EXT_TEST` | normal | external clock test mode — `CLKOUT` becomes an **input** |
| 6 | – | unused (but see the reset command) | |
| 5 | `STOP` | RTC clock runs | RTC stopped; divider chain F2–F14 asynchronously reset |
| 4 | `SR` | no reset | initiate **software reset**; always reads back 0 |
| 3 | – | unused (but see the reset command) | |
| 2 | `CIE` | no correction interrupt | pulse on `INT` at every offset-correction cycle |
| 1 | `12_24` | **24-hour mode** | 12-hour mode |
| 0 | **`CAP_SEL`** | **7 pF** internal load | **12.5 pF** internal load |

**Software reset = write `01011000` = `0x58` to `Control_1`** — bits 6, 4 and 3 set, everything else clear **[DOC §8.2.1.3]**. NXP recommends re-initialising the interface with a STOP and START immediately afterwards.

> ⚠ `CAP_SEL` lives in the same register as `SR`, so **a software reset silently reverts the crystal load-capacitance selection to 7 pF.** If your board needs 12.5 pF, re-write `CAP_SEL` after every reset. §4 and §11.

### 3.2 `Control_2` (`01h`) bit meanings **[DOC Table 9, Table 11]**

| Bit | Name | Meaning |
|---:|---|---|
| 7 | `AIE` | alarm interrupt enable |
| 6 | `AF` | alarm flag. **Read** 1 = alarm fired. **Write 0 clears it; writing 1 leaves it unchanged** — a logical AND is performed on write so that clearing one flag cannot clobber another |
| 5 | `MI` | minute interrupt enable |
| 4 | `HMI` | half-minute interrupt enable |
| 3 | `TF` | timer flag — same write-to-clear semantics |
| 2:0 | `COF[2:0]` | CLKOUT frequency |

`COF[2:0]` **[DOC Table 11]**:

| `COF` | CLKOUT | Duty | Affected by `STOP`? |
|---:|---:|---|---|
| **`000`** (default) | **32768 Hz** | 60:40 – 40:60, uncontrolled | no |
| `001` | 16384 Hz | 50:50 | no |
| `010` | 8192 Hz | 50:50 | no |
| `011` | 4096 Hz | 50:50 | **yes → LOW** |
| `100` | 2048 Hz | 50:50 | **yes → LOW** |
| `101` | 1024 Hz | 50:50 | **yes → LOW** |
| `110` | **1 Hz** | 50:50 | **yes → LOW**. Affected by offset-correction pulses |
| `111` | LOW (disabled) | — | — |

**`CLKOUT` is push-pull and enabled at power-on, at 32.768 kHz** — the POR default `Control_2` = `0x00` means `COF` = `000`. On these boards `CLKOE` is hard-tied high, so the 32.768 kHz square wave is running the moment the RTC has power, before any firmware executes. §5.2.

### 3.3 `Offset` (`02h`) **[DOC Table 12, Table 13]**

| Bit | Name | Meaning |
|---:|---|---|
| 7 | `MODE` | **0** = normal, correction applied once every **two hours**, **4.34 ppm per LSB**. **1** = "course"/fast, correction every **4 minutes**, **4.069 ppm per LSB** |
| 6:0 | `OFFSET[6:0]` | two's complement, **+63 to −64** |

Full-scale range: `MODE` = 0 → **+273.420 to −277.760 ppm**; `MODE` = 1 → **+256.347 to −260.416 ppm**. Attainable accuracy after trimming is **±2 ppm** **[DOC Fig. 12]**, and **1 ppm = 0.0864 s/day**.

### 3.4 `Timer_mode` (`11h`) **[DOC Table 35]**

| Bit | Name | Values |
|---:|---|---|
| 4:3 | `TCF[1:0]` | `00` = 4.096 kHz · `01` = 64 Hz · `10` = 1 Hz · **`11` = 1/60 Hz (default)** |
| 2 | `TE` | timer enable |
| 1 | `TIE` | timer interrupt enable |
| 0 | `TI_TP` | **0** = INT follows `TF` · **1** = INT generates a pulse |

Countdown period = `T[7:0] / SourceClockFrequency`. With `TCF` = `11` (1/60 Hz) and `T` = 255 the maximum period is **255 minutes ≈ 4 h 15 min**.

`TI_TP` changes the timer's whole character **[DOC §8.2.2.3]**:

- **`TI_TP` = 1** — a pulse is generated regardless of `TF`; `TF` stays set until cleared but does not gate `INT`; **the countdown runs in a repetitive loop**.
- **`TI_TP` = 0** — `INT` follows `TF`; if `TF` is not cleared before the next expiry no `INT` is generated; **the timer stops after the first countdown**.

## 4. The oscillator, the load capacitance, and the thing most likely to be wrong

This is the section that matters most in practice. RTC drift bugs are almost always load-capacitance bugs.

### 4.1 How `CAP_SEL` interacts with external capacitors

`CL(itg)` is the **series** combination of the internal `COSCI` and `COSCO` **[DOC Table 41 note 7]**. So:

| `CAP_SEL` | `CL(itg)` (series) | Implied per-pin capacitance |
|---:|---:|---:|
| 0 | 7 pF | ≈ 14 pF on each of OSCI and OSCO |
| 1 | 12.5 pF | ≈ 25 pF on each |

Adding an external capacitor `Cext` from **each** pin to ground adds `Cext` in parallel at each pin, so the resulting series load becomes `(C_int + Cext) / 2`.

Now apply that to the two board variants **[SCH, BOM]** **[INF for the arithmetic]**:

| Board | `C34` / `C35` external | `CAP_SEL` = 0 (7 pF) gives | `CAP_SEL` = 1 (12.5 pF) gives |
|---|---|---:|---:|
| **Inkplate 5** (V1.2.0) | **DNP — not fitted** | **7 pF** | **12.5 pF** |
| **Inkplate 5 Gen 2** (V1.1.0) | **12 pF each** | (14+12)/2 = **13 pF** | (25+12)/2 = **18.5 pF** |
| **ZeroWriter Ink** (v1.2.0) | **12 pF each** — identical to Gen 2 | **13 pF** | **18.5 pF** |

> **The correct `CAP_SEL` is therefore different between Inkplate 5 and Inkplate 5 Gen 2 / ZeroWriter, for the same nominal crystal.** On the Gen 2 / ZeroWriter boards, `CAP_SEL` = **0** produces ≈ 13 pF; `CAP_SEL` = **1** produces ≈ 18.5 pF, which is far above any plausible crystal specification and will make the clock run **slow**.

Soldered's own comment in the calibration example says exactly this, in the opposite direction: *"If you use an internal capacitor, you have to remove the external ones. If you use an external one, you don't have the next line of code."* **[SRC]** — and then the example nonetheless calls `setInternalCapacitor(RTC_12_5PF)` on a board that has the external 12 pF parts fitted. §9.3.

### 4.2 ⚠ The crystal's identity is ambiguous in every BOM

All three BOMs record `X1` with the **value** and the **footprint** disagreeing about load capacitance **[BOM]**:

| Board | BOM `Package`/`Footprint` field | BOM `Value`/`Designation` field |
|---|---|---|
| Inkplate 5 V1.2.0 | `ABS07AIG-32.768KHZ-7-D-T` | `7LC32768F12UC` |
| Inkplate 5 Gen 2 V1.1.0 | `ABS07AIG-32.768KHZ-7-D-T` | `7LC32768F12UC` |
| ZeroWriter v1.2.0 | `Soldered footprints:ABS07AIG-32.768KHZ-7-D-T` | `7LC32768F12UC` |

- `ABS07AIG-32.768KHZ-**7**-D-T` is an Abracon ordering code in which the field after the frequency is the **load capacitance in pF → 7 pF**.
- `7LC32768F**12**UC` reads as a **12 (12.5) pF** part under the common convention for this style of code.

These cannot both be right. The KiCad "footprint" field is a *library* name, so it is entirely possible Soldered named the footprint after the first crystal they used and later changed the fitted part without renaming the library — but the reverse is equally possible. **Nothing in the published design settles it, and the answer changes which `CAP_SEL` value is correct.** Treat this as unresolved.

**Empirical resolution — do this rather than guessing:**

1. Move solder jumper `JP2` to connect pads **2–3** so `CLKOUT` reaches `IO39` / test point `TP74` (§5.2), or probe `TP74` directly.
2. Leave `COF` at its default `000` (32.768 kHz).
3. Measure `CLKOUT` with a counter good to ~0.01 Hz, first with `CAP_SEL` = 0, then with `CAP_SEL` = 1.
4. Whichever is closer to 32768.000 Hz is the correct setting for **your** board; then trim the residue with the `Offset` register (§8).

Rough expectation for a typical 32.768 kHz tuning fork (motional `C1` ≈ 3 fF, shunt `C0` ≈ 1.3 pF): moving the load from 12.5 pF to 18.5 pF pulls the frequency down by roughly **−33 ppm ≈ −2.8 s/day**; from 7 pF to 18.5 pF, roughly **−105 ppm ≈ −9 s/day**. **[INF — generic crystal parameters, not this crystal's; treat as an order of magnitude only]**

### 4.3 Other oscillator facts worth knowing

- **`Rs` max 100 kΩ** **[DOC Table 41]**. Cheap 32.768 kHz tuning forks in 3.2 × 1.5 mm packages routinely specify 50–70 kΩ typical; check before substituting a smaller can.
- **Start-up takes 200 ms to 2 s** depending on crystal, temperature and supply **[DOC §8.3.1.1]**. The `OS` flag is set for the whole of that window. Firmware that reads `OS` 5 ms after power-up will see it set and wrongly conclude the clock is broken. §6.
- **`VDD` ≥ 1.2 V is needed for reliable, prompt start-up**, even though the part *runs* down to 0.9 V **[DOC Table 41 note 1]**. A dying CR2032 will keep an already-running oscillator alive far below the voltage at which it would restart one.
- Supply-voltage sensitivity is tiny: **0.075 ppm per 200 mV** **[DOC Table 41]**. Do not chase `VDD` ripple as a source of drift; chase load capacitance and temperature. A tuning-fork crystal's parabolic temperature curve (typically −0.034 ppm/°C² about a +25 °C turnover) dominates everything else, and the PCF85063A has **no temperature compensation** — that is what the PCF2127/PCF2129 are for (§12).

## 5. Exact wiring — identical on all three boards

`U7` is drawn the same way on Inkplate 5, Inkplate 5 Gen 2 and ZeroWriter Ink. The only difference between them is `C34`/`C35` (§4.1) and the coin-cell holder's designator.

| Pin | Name | Net | Detail |
|---:|---|---|---|
| 1 | `OSCI` | `X1` | → crystal `X1` pin 1, and `C34` if fitted |
| 2 | `OSCO` | `X2` | → crystal `X1` pin 2, and `C35` if fitted |
| 3 | **`CLKOE`** | **`3V3_RTC`** | **Hard-tied high — the clock output is permanently enabled in hardware** |
| 4 | `INT` | *(local)* | `R42` **10 kΩ pull-up to `3V3`**, then to solder jumper `JP2` pad **1** |
| 5 | `VSS` | GND | |
| 6 | `SDA` | `I2C_SDA` | → ESP32-WROVER **`IO21`** |
| 7 | `SCL` | `I2C_SCL` | → ESP32-WROVER **`IO22`** |
| 8 | `n.c.` | — | Explicit no-connect cross in the schematic ✅ |
| 9 | `CLKOUT` | `CLKOUT_RTC` | → `JP2` pad **3**, and test point `TP74` on ZeroWriter |
| 10 | `VDD` | `3V3_RTC` | `C36` **100 nF**. Fed by the diode-OR of §5.3 |
| — | exposed pad | *(no net)* | Electrically isolated, per NXP **[PCB]** |

> Naming trap: the **net labels** on `OSCI`/`OSCO` are `X1` and `X2`, while the **crystal's reference designator** is also `X1`. When reading these schematics, "X1" means two different things depending on context.

### 5.1 The I²C bus, and what else is on it

| Item | Value | Evidence |
|---|---|---|
| Bus | ESP32-WROVER I²C0 via Arduino `Wire` — `SDA` = `IO21`, `SCL` = `IO22` | [SCH `MCU.kicad_sch`] |
| Pull-ups | **`R1` and `R4`, 10 kΩ to `3V3`** (on the POWER sheet) | [SCH] |
| Bus speed | `Wire.begin()` with no arguments → Arduino-ESP32 default **100 kHz**. Nothing on the RTC/expander/PMIC path calls `Wire.setClock()`. The only `setClock()` in the tree is inside the vendored Zanshin BME680 driver (`I2C_STANDARD_MODE` = 100000), which would only run if a sketch uses the BME680 feature | [SRC] |
| **PCF85063A** | **`0x51`** | [DOC] |
| PCAL6416A I/O expander | `0x20` (`IO_INT_ADDR`) | [SRC `boards/Inkplate5V2/pins.h`] |
| TPS65186 e-paper PMIC | `0x48` (`TPS65186_I2C_ADDR`) | [SRC `features/TPS65186/TPS65186.h`] |
| User expansion | `K3` — **`easyC-SMD`** on Inkplate 5 / Gen 2, renamed **`qwiic-SMD`** on ZeroWriter (same connector) | [SCH] |
| Broken out to headers | `K5` (SCL) and `K8` (SDA) on the Inkplate breakout header row | [SCH] |

> **The RTC is *not* behind the PCAL6416A expander.** It is a peer of the expander on the same physical bus. This is worth stating explicitly because the e-paper control signals *are* behind the expander, which leads people to assume everything is. Talking to the RTC requires no expander transaction.

**Address-collision hazard on the easyC/Qwiic connector:** `0x51` is a popular address. Soldered's own easyC EEPROM breakouts and many 24Cxx-style parts land on `0x50`–`0x57`. Plugging one in can shadow the on-board RTC with no error other than nonsense time values.

The Inkplate library serialises all bus access behind a **FreeRTOS recursive mutex** (`mutexI2C`, taken by `i2cStart()` and released by `i2cEnd()`) **[SRC `system/inkplateSemaphore.cpp`]**. If you talk to the RTC directly with `Wire` from another task, take that mutex too, or you will corrupt e-paper power sequencing.

### 5.2 `INT`, `CLKOUT` and solder jumper `JP2`

`JP2` is a three-pad SMD jumper, library symbol `SMD_JUMPER_3_PAD_CONNECTED_LEFT_TRACE` **[SCH]**:

```
         pad 1 ── RTC INT  (open drain, 10k pull-up to 3V3 via R42)
                    │
                 [default trace connects 1–2]
                    │
         pad 2 ── GPIO_39  ──> ESP32-WROVER pin 5 (SENSOR_VN / GPIO39)
                              also to breakout header K35 (IP5) / K40 (Gen2, ZW), and TP73 (ZW)

         pad 3 ── RTC CLKOUT  (push-pull, also TP74 on ZeroWriter)
```

So **by default `IO39` sees the RTC's alarm/timer interrupt**, and `CLKOUT` goes nowhere except a test point. Cutting the 1–2 trace and bridging 2–3 swaps `IO39` over to the 32.768 kHz clock output — which is how you would calibrate (§4.2), at the cost of the interrupt.

`IO39` is a good choice for this: on the ESP32 it is `SENSOR_VN`, an **input-only** pin that is also `RTC_GPIO3` and `ADC1_CH3`, so it is a valid `esp_sleep_enable_ext0_wakeup()` source. The vendor's own example does exactly that **[SRC]**:

```c
display.rtc.setAlarmEpoch(display.rtc.getEpoch() + 10, RTC_ALARM_MATCH_DHHMMSS);
esp_sleep_enable_ext0_wakeup(GPIO_NUM_39, 0);   // wake on INT going LOW
esp_deep_sleep_start();
```

Two things about that example are worth flagging:

1. It carries an in-tree comment reading *"NOTE: GPIO39 is NOT guaranteed for Inkplate 5v2"* **[SRC]** — which the schematic contradicts: `JP2` pad 2 is `GPIO_39` on the Inkplate 5, Inkplate 5 Gen 2 and ZeroWriter schematics alike **[SCH ×3]**. Trust the schematic.
2. `R42` pulls `INT` up to **`3V3`**, not to `3V3_RTC`. NXP's guidance is *"tying VDD of the device and VDD of all the external pull-up resistors to the same Power Supply"* **[DOC Table 4 note 2]**. When the main 3V3 rail is off and the RTC is running from the coin cell, `INT` has **no pull-up at all** and floats — harmless, because the ESP32 is unpowered too, but it means you cannot use `INT` to wake anything that outlives the 3V3 rail.

### 5.3 Battery backup: a passive diode-OR, and it never charges the cell

```
3V3      ──▶|── D11 (M4_DIODA) ──┬── 3V3_RTC ── U7 pin 10 VDD
                                  │              └── C36 100n
CR2032 + ──▶|── D12 (M4_DIODA) ──┘
  (K10 on Inkplate 5 · K11 on Gen 2 and ZeroWriter, net RTC-BATT)
```

**[SCH ×3, verified against the plotted PDF as an image]**

| Property | Consequence |
|---|---|
| Two diodes, cathodes commoned | `3V3_RTC` follows **whichever source is higher**, minus one forward drop |
| The coin cell is **only ever a source** | **A CR2032 is not rechargeable and is never charged here.** This is the correct topology; getting it wrong is a fire risk |
| Holder fitted on all three boards | `CR2032-BS-6-1`, present and not marked DNP in all three BOMs **[BOM]** |
| The RTC is the **only** load on `3V3_RTC` | So the backup drain is the datasheet 220 nA typ (plus diode leakage), not a shared rail |
| `D11`/`D12` are identified only as `M4_DIODA` | BOM value *and* footprint both read `M4_DIODA` (Croatian *dioda* = diode). "M4" is the standard SMA marking for a 1 A / 400 V general-purpose rectifier. **The actual device is not specified** **[BOM]** |

**Backup lifetime, roughly:** a CR2032 holds ~220 mAh. At 220 nA that is nominally ~114 years, i.e. the cell's own ~10-year shelf life is the limit, not the load. Even at the 600 nA worst case over temperature it is ~42 years. **[INF]** In practice the diode reverse leakage — unknown, because the diode is unspecified — is likely to dominate.

**Forward-drop caveat.** At sub-microamp currents a silicon rectifier's forward drop is a few hundred millivolts, not the 0.7 V rule of thumb, so `3V3_RTC` sits somewhere around **2.9–3.1 V** when the main rail is up. That is comfortably inside the 0.9–5.5 V operating window and above the 1.8 V needed for 400 kHz I²C, so it does not matter functionally — but it does mean **`VDD_RTC` is not 3.3 V**, which matters for §5.4 and for any `0.7 × VDD` threshold calculation. **[INF — the diode is unspecified, so this is an estimate]**

### 5.4 Bus pull-ups sit on a higher rail than the device `VDD`

`R1`/`R4` pull `SDA`/`SCL` to **`3V3`**, while `U7`'s `VDD` is **`3V3_RTC`** ≈ 3.0 V. NXP explicitly recommends against this **[DOC Table 4 note 2]** — but also explicitly states the interface is **5 V tolerant** **[DOC Table 41 note 5]**, so the arrangement is safe and the RTC will not sink current from the bus when the main rail is up and its own rail is a diode drop lower. `VIH` is `0.7 × VDD_RTC` ≈ 2.1 V, so a 3.3 V bus high is comfortably recognised. **No action needed; just do not be surprised by it when scoping.** **[INF]**

## 6. The `OS` flag — how firmware knows timekeeping was lost

**This is the single most important firmware-facing behaviour of this part.**

### 6.1 What `OS` actually means **[DOC §8.3.1.1]**

`OS` is **bit 7 of the `Seconds` register (`04h`)**. Its POR value is **1**.

| `OS` | Meaning |
|---:|---|
| 0 | *"clock integrity is guaranteed"* |
| 1 | *"clock integrity is **not** guaranteed; oscillator has stopped or has been interrupted"* |

Semantics that firmware must respect:

- `OS` is set whenever the oscillator stops — including the **200 ms to 2 s** normal start-up window after power is applied, and including a brown-out too shallow to reset the registers.
- **`OS` is only ever cleared by command.** It never self-clears.
- **If you write 0 to `OS` and it reads back 1, the oscillator is not running.** NXP presents this as the supported way to test the oscillator and to detect a supply that has sagged to the point where oscillation fails.
- Because it lives in the same byte as the seconds count, **any full-byte write to `04h` also writes `OS`.** Writing a BCD seconds value ≤ `0x59` therefore clears `OS` as a side effect.

### 6.2 Why the software reset is not optional on these boards

NXP: *"To ensure that all control registers will be set to their default values, the VDD level must be at zero volts at initial power-up. If this is not possible, a reset must be initiated with the software reset command when power is stable."* **[DOC §8.2]** And: *"There is a low probability that some devices will have corruption of the registers after the automatic power-on reset if the device is powered up with a residual VDD level."* **[DOC §8.2.1.3]**

**On these boards `VDD_RTC` never goes to 0 V while a coin cell is fitted** — that is the entire point of the diode-OR. So the condition NXP warns about is the *normal* condition here, on every single power-up. **Issue the `0x58` software reset once at first provisioning, and after any suspected corruption.** **[INF, but directly implied by the datasheet]**

### 6.3 ⚠ The Inkplate Arduino library does not expose `OS` at all

Audited against v11.1.4 **[SRC `src/features/rtc/rtc.cpp`]**:

```c
void RTC::updateTime()
{
    ...
    Wire.requestFrom(I2C_ADDR, 7);
    Second = bcdToDec(Wire.read() & 0x7F);   // <-- OS flag masked off and discarded
    ...
}
```

`0x7F` strips bit 7. **No method in the `RTC` class reads, returns or checks `OS`.** Instead, the library substitutes its own convention:

```c
#define RTC_RAM_by 0x03
#define RTC_SET    0xAA

bool RTC::isSet() { /* read 03h */ return _ramByte == 170; }   // 170 == 0xAA
```

`setTime()`, `setDate()` and `setEpoch()` all write `0xAA` into the free `RAM_byte` at `03h`; `isSet()` reports whether it is still there **[SRC]**.

| | `isSet()` (`RAM_byte` == `0xAA`) | `OS` flag (`04h` bit 7) |
|---|---|---|
| Full POR from 0 V | `RAM_byte` resets to `0x00` → **correctly false** | set → correctly flags loss |
| Software reset | `RAM_byte` resets to `0x00` → correctly false | set → correct |
| **Oscillator stopped or interrupted while `VDD` stayed up** (brown-out, crystal fault, condensation, a probe on `OSCI`) | **`RAM_byte` still holds `0xAA` → reports "time is valid"** | **set → correctly flags loss** |
| Register corruption from a residual-`VDD` power-up (§6.2) | may or may not survive | oscillator behaviour independent |

> **Conclusion: `isSet()` is a *provisioning* flag, not an integrity flag.** It answers "has anyone ever set this clock?" It does **not** answer "is the time I am about to read trustworthy?" — and those diverge in exactly the failure mode a battery-backed RTC exists to survive. **Any firmware that cares should read `04h` bit 7 directly**, in addition to calling `isSet()`.

Reading it takes four lines and does not need the library:

```c
static bool rtcOscillatorStopped()
{
    Wire.beginTransmission(0x51);
    Wire.write(0x04);                 // Seconds
    Wire.endTransmission();
    Wire.requestFrom(0x51, 1);
    return (Wire.read() & 0x80) != 0; // OS
}

static void rtcClearOscillatorStopFlag(uint8_t currentSecondsBcd)
{
    Wire.beginTransmission(0x51);
    Wire.write(0x04);
    Wire.write(currentSecondsBcd & 0x7F);  // writing bit 7 = 0 clears OS
    Wire.endTransmission();
}
```

Remember to allow for start-up: **do not treat `OS` = 1 as fatal within ~2 s of the RTC's supply appearing.** Poll for up to 2 s, clearing and re-reading, before declaring the oscillator dead **[DOC §8.3.1.1]**.

## 7. Alarm, timer and the minute/half-minute interrupts

### 7.1 Alarm **[DOC §8.5.6]**

- Five alarm registers, `0Bh`–`0Fh`: second, minute, hour, day, weekday.
- Each has an `AEN_x` bit 7. **`AEN_x` = 0 *enables* that field's comparison; `AEN_x` = 1 ignores it.** The reset value is `0x80` — all comparisons disabled. **The polarity is inverted relative to intuition and is a classic source of "my alarm fires every second".**
- `AF` is set when **all enabled** comparisons match simultaneously, **and only on the increment into the matching state**.
- `AIE` = 1 makes `INT` follow `AF`.
- `AF` remains set until cleared by command. Once cleared it will not set again until the time next increments into a match.

Match granularity is chosen by which `AEN_x` bits you clear. The Inkplate library exposes exactly this as bit masks **[SRC `rtc.h`]**:

| Constant | Value | Matches |
|---|---:|---|
| `RTC_ALARM_MATCH_SS` | `0b00000001` | every minute, at a given second |
| `RTC_ALARM_MATCH_MMSS` | `0b00000011` | every hour |
| `RTC_ALARM_MATCH_HHMMSS` | `0b00000111` | every day |
| `RTC_ALARM_MATCH_DHHMMSS` | `0b00001111` | every month, on a day-of-month |
| `RTC_ALARM_MATCH_WHHMMSS` | `0b00010111` | every week, on a weekday |

### 7.2 Countdown timer **[DOC §8.6]**

`Timer_value` (`10h`) counts down at the rate chosen by `TCF`. Maximum period is 255 × 60 s = **4 h 15 min**. `TF` (`Control_2` bit 3) is the flag; `TIE` gates the interrupt; `TI_TP` chooses level-follows-flag versus pulse-and-repeat (§3.4).

### 7.3 Minute / half-minute interrupts **[DOC §8.2.2.2]**

`MI` and `HMI` in `Control_2` are pre-defined timers synchronised to the seconds counter:

| `MI` | `HMI` | Result |
|---:|---:|---|
| 0 | 0 | none |
| 1 | 0 | interrupt every minute |
| 0 | 1 | interrupt every 30 s |
| 1 | 1 | interrupt every 30 s (indistinguishable from `HMI` alone) |

Pulses on `INT` are **1/64 s** wide in normal offset mode. The **first** interrupt after enabling `MI` arrives after 1–59 s, and after enabling `HMI` after 1–29 s; subsequent ones are regular. Note the constraint: **`MI`/`HMI` must only be used with `Offset` `MODE` = 0, and the periods are only consistent when `OFFSET[6:0]` = 0** **[DOC §8.2.2.2]**.

### 7.4 `TF` is shared

`TF` is set by the first trigger of `MI`, `HMI`, **or** the countdown timer **[DOC §8.2.2.3]**. Its purpose is to let the host distinguish *timer* from *alarm* when `INT` fires. If you use two of the three timer sources at once you cannot tell them apart from `TF`.

## 8. Offset (aging / accuracy) calibration

NXP's procedure **[DOC §8.2.3.3, Fig. 11]**, with the datasheet's own worked example:

```
1. Measure CLKOUT:                f_meas   = 32768.48 Hz
2. Convert to period:             t_meas   = 1 / f_meas       = 30.517131 µs
3. Difference from ideal:         D_meas   = 1/32768 − t_meas = 0.000447 µs
4. ppm deviation:                 E_ppm    = 1e6 × D_meas / t_meas = +14.648 ppm
5. Offset register value:
       MODE = 0:  Offset = E_ppm / 4.34   =  3.375  ->  write +3
       MODE = 1:  Offset = E_ppm / 4.069  =  3.6    ->  write +4
```

**Sign convention, stated plainly because it is easy to invert:** in the datasheet's own example the crystal is running **fast** (32768.48 Hz) and the resulting offset value is **positive**. So *positive offset corrects a fast clock; negative offset corrects a slow clock.*

Practical notes:

- **`MODE` = 0 (correction every 2 hours, 4.34 ppm/LSB) is the right default.** `MODE` = 1 corrects every 4 minutes and NXP notes it *"can result in higher power consumption."*
- The correction works by **adding or removing clock pulses, not by pulling the oscillator**. Consequently a 1 Hz `CLKOUT` and the 1 Hz / 1/60 Hz timer sources are perturbed by correction pulses, while 1024 Hz and above are not **[DOC Table 15, Table 17]**.
- Setting `CIE` (`Control_1` bit 2) emits a pulse on `INT` for every correction pulse applied — useful for verifying that the trim is actually happening, useless in production because it shares the pin with the alarm.
- Achievable accuracy after trimming: **±2 ppm ≈ ±0.17 s/day** **[DOC Fig. 12]**.
- **The offset register does not survive a software reset** (`02h` resets to `0x00`). Re-apply it, along with `CAP_SEL`, after any reset.
- **It cannot compensate temperature.** A tuning-fork crystal trimmed at 25 °C will drift by tens of ppm at 0 °C or 45 °C. If you need better, you need a TCXO-based RTC (§12).

### 8.1 Calibrating without an oscilloscope

Soldered's example documents the long-baseline method, which is the right one for a sealed product **[SRC]**: run the clock for 2–3 days against a trusted reference, photograph both together at start and end, and compute

```
E_ppm = 1e6 × (t_rtc − t_ref) / t_ref
```

then divide by 4.34 (`MODE` = 0) and round. Two or three days gives roughly 1 ppm resolution if you can read the seconds to ±0.5 s at both ends. **[INF]**

## 9. Drivers, libraries and versions

### 9.1 What Soldered ships

| Item | Version | Notes |
|---|---|---|
| **Inkplate Arduino library** | **11.1.4** (`library.properties`) | https://github.com/SolderedElectronics/Inkplate-Arduino-library — LGPL-3.0. The RTC driver is `src/features/rtc/rtc.{h,cpp}`, ~870 lines, exposed as `display.rtc.*` |
| Board target | `ARDUINO_INKPLATE5V2` / `ARDUINO_INKPLATE5` | Selected from "Inkplate Boards" in Boards Manager |
| Examples | `examples/Inkplate5V2/Advanced/RTC/{Inkplate5V2_RTC_Simple, _RTC_Alarm, _RTC_Interrupt_Alarm, _RTC_Timer}` · `Advanced/DeepSleep/Inkplate5V2_RTC_Alarm_With_Deep_Sleep` · **`Diagnostics/Inkplate5V2_RTC_Calibration`** | |

Public API **[SRC `rtc.h`]**:

```
setTime(h,m,s,isPM)  setDate(wd,d,m,yr)  setEpoch(u32)  getEpoch()
getRtcData()  getSecond/Minute/Hour/Day/Weekday/Month/Year()  isPM()
setAlarm(s,m,h,d,wd)  setAlarmEpoch(u32,match)  enableAlarm()  readAlarm()
getAlarmSecond/Minute/Hour/Day/Weekday()
checkAlarmFlag()  clearAlarmFlag()
timerSet(srcClock,value,intEnable,intPulse)  checkTimerFlag()  clearTimerFlag()  disableTimer()
changeTimeFormat()  isSet()  reset()
setInternalCapacitor(bool)  setClockOffset(bool mode, int value)
```

### 9.2 Peripheral Mode — the RTC over UART

Soldered exposes the whole RTC through [Peripheral Mode](../../../devices/soldered-electronics/inkplate-5/features/peripheral-mode.md) at 115200 baud over the [CH340C](../../wch/ch340c/README.md): `rtcSetTime`, `rtcSetDate`, `rtcSetEpoch`, `rtcGetEpoch`, `rtcSetAlarm`, `rtcSetAlarmEpoch`, `rtcCheckAlarmFlag`, `rtcClearAlarmFlag`, `rtcDisableAlarm`. So a **host system** — Raspberry Pi, STM32, a PC — can use the Inkplate's RTC as its own scheduled wake source without writing any ESP32 code. Note that Peripheral Mode inherits every one of the library gotchas in §9.3.

### 9.3 ⚠ Six real defects and traps in the vendor driver

All read from v11.1.4 source **[SRC]**, all verified against **[DOC]**.

**1. `OS` is masked and discarded; `isSet()` is not an integrity check.** §6.3. The most consequential of the six.

**2. `setTime()` + `setDate()` is the exact anti-pattern the datasheet warns against.** NXP: *"it is very important to make a read or write access in one go… As an example, if the time (seconds through to hours) is set in one access and then in a second access the date is set, it is possible that the time will increment between the two accesses."* **[DOC §8.4]** The library's `setTime()` writes `03h`–`06h`; `setDate()` then performs a *separate* transaction writing `07h`–`0Ah` **[SRC]**. A second rollover between the two calls corrupts the date. **Use `setEpoch()` instead** — it writes `03h` through `0Ah` in one transaction and is correct.

**3. `enableAlarm()` clobbers `Control_2` wholesale.**

```c
Control2 = RTC_CTRL_2_DEFAULT | RTC_ALARM_AIE;   // 0x00 | 0x80  ==  0x80
Wire.write(RTC_CTRL_2); Wire.write(Control2);
```

That write sets `COF[2:0]` = `000` (**CLKOUT back to 32.768 kHz**) and clears `MI`, `HMI` and `TF`. If you had configured a different `CLKOUT` frequency, calling `setAlarm()` silently undoes it.

**4. `timerSet()` disables the alarm interrupt.** It writes `Control_2` = `0x00` before reconfiguring `Timer_mode` **[SRC]**, clearing `AIE`. **You cannot have a library-configured alarm and a library-configured timer at the same time**; whichever you configure second wins.

**5. `reset()` is correct but misleadingly named, and loses your calibration.**

```c
#define RTC_CTRL_1_DEFAULT 0x58     // this is NOT the default; the default is 0x00
void RTC::reset() { write(RTC_CTRL_1, RTC_CTRL_1_DEFAULT); }
```

`0x58` is the **software reset command** **[DOC §8.2.1.3]** and the function does the right thing. But the constant's name says otherwise, and the consequence is easy to miss: **a reset returns `CAP_SEL` to 7 pF and `Offset` to 0.** Re-apply both afterwards.

**6. `setEpoch()`/`getEpoch()` are timezone-dependent.** `setEpoch()` calls `localtime()` and `getEpoch()` calls `mktime()` **[SRC]**, so what is actually stored in the RTC is **local** time, and the round trip is only consistent if `TZ` is configured identically at both ends. Pick one convention — storing UTC and doing your own conversion is usually less surprising — and be aware that `rtcSetEpoch` in Peripheral Mode inherits this.

Also worth knowing, though not a defect: `setTime()` does **not** use the `STOP` bit, so the seconds boundary lands with up to ~0.5 s of uncertainty. NXP's precise-start procedure is `STOP` = 1 → write registers → `STOP` = 0, after which the first increment occurs **0.507813 s to 0.507935 s** later **[DOC §8.2.1.2, Table 7]**. For NTP-synchronised timekeeping this is the difference between ±0.5 s and ±1 ms.

And in the calibration example: `setInternalCapacitor(RTC_12_5PF)` is called on a board whose external 12 pF capacitors are fitted, alongside `setClockOffset(1, -63)` — the **maximum negative correction, −256.347 ppm ≈ −22.1 s/day**. A trim that large indicates a badly mismatched load, which is exactly what 12.5 pF internal + 12 pF external would produce (§4.1). **Treat both of those numbers as placeholders to be replaced by your own measurement, not as the correct settings for a stock board.** **[INF]**

### 9.4 Alternatives to the vendor driver

| Library | Where | Notes |
|---|---|---|
| **Inkplate Arduino library 11.1.4** | https://github.com/SolderedElectronics/Inkplate-Arduino-library | What ships. Convenient, integrated with the mutex and Peripheral Mode. Caveats in §9.3 |
| **Raw `Wire`** | Arduino-ESP32 core | **Recommended for anything that must be correct.** The part is 18 registers; §10 is the whole driver |
| ESP-IDF `driver/i2c_master.h` | ESP-IDF ≥ 5.2 (`i2c_master` API; the legacy `driver/i2c.h` is deprecated in 5.x) | If you are not using Arduino. No official Espressif PCF85063A driver exists |
| `Rtc_Pcf8563` / generic PCF8563 libraries | various | **Will appear to work and will not.** Same address `0x51`, different register offsets — see §12 |
| Soldered `PCF85063A-SOLDERED` breakout library | https://github.com/SolderedElectronics/PCF85063A-SOLDERED | Standalone driver for their easyC RTC breakout; same silicon |

Because there is no ESP-IDF driver and the register map is trivial, most non-Arduino projects write their own. Do.

## 10. Correct initialisation, and reading the time atomically

### 10.1 Reading the time

NXP's required sequence **[DOC §8.4]**:

1. START, slave address for **write** (`A2h`)
2. Set the address pointer to **`04h`** (Seconds)
3. RESTART (or STOP then START)
4. Slave address for **read** (`A3h`)
5. Read Seconds, Minutes, Hours, Days, Weekdays, Months, Years — **seven bytes, one transaction**
6. STOP

During the access the time counters are frozen, which prevents a carry from tearing the read. **A maximum of one pending increment is buffered, so the whole access must complete within one second** **[DOC §8.4]**. At 100 kHz a 7-byte read takes well under 1 ms, so this is only a hazard if a debugger halts mid-transaction or another task starves the bus while holding it.

The Inkplate library's `updateTime()` does this correctly **[SRC]** — a single `requestFrom(0x51, 7)` after pointing at `04h`. That part is right; it just throws `OS` away (§6.3).

Field masks when decoding **[DOC §8.3]**:

```c
sec  = bcd2dec(b[0] & 0x7F);   // bit 7 = OS  -- capture it before masking!
min  = bcd2dec(b[1] & 0x7F);
hour = bcd2dec(b[2] & 0x3F);   // 24h mode; in 12h mode use & 0x1F and read bit 5 as PM
day  = bcd2dec(b[3] & 0x3F);
wday =         b[4] & 0x07;    // 0 = Sunday ... 6 = Saturday, NOT BCD
mon  = bcd2dec(b[5] & 0x1F);
year = bcd2dec(b[6]) + 2000;
```

Leap years: *"If the year counter contains a value which is exactly divisible by 4 (including the year 00), the PCF85063A compensates for leap years by adding a 29th day to February."* **[DOC Table 23 note 1]** — i.e. a naive divisible-by-4 rule over a 2000–2099 window, which happens to be correct for the whole of that century because 2000 is a leap year. **It will be wrong in 2100.**

### 10.2 A recommended init sequence

```c
#define RTC_ADDR 0x51

void rtc_init(bool boardHasExternalLoadCaps)
{
    // 1. Read OS BEFORE touching anything. Allow for oscillator start-up:
    //    the datasheet permits 200 ms .. 2 s from power-on. [DOC 8.3.1.1]
    bool lost = false;
    for (int i = 0; i < 40; i++) {                 // up to ~2 s
        if (!rtcOscillatorStopped()) break;
        lost = true;
        delay(50);
    }

    // 2. If this is first provisioning, or registers may be corrupt after a
    //    residual-VDD power-up (always possible here -- the coin cell means VDD
    //    never reaches 0 V), issue the software reset. [DOC 8.2, 8.2.1.3]
    if (lost || !rtcProvisioned()) {
        i2c_write(RTC_ADDR, 0x00, 0x58);           // software reset
        delay(2);
        // NXP: re-initialise the interface with a STOP and START after this.
    }

    // 3. Re-apply everything the reset cleared.
    uint8_t ctrl1 = 0x00;                          // EXT_TEST=0, STOP=0, CIE=0, 24h
    if (!boardHasExternalLoadCaps) ctrl1 |= 0x01;  // CAP_SEL = 1 -> 12.5 pF
    i2c_write(RTC_ADDR, 0x00, ctrl1);
    i2c_write(RTC_ADDR, 0x02, myMeasuredOffset);   // Offset, MODE=0 -- see section 8

    // 4. Control_2: silence CLKOUT unless you need it. COF=111 -> CLKOUT LOW.
    //    Do this before enabling any interrupt, because enableAlarm()-style
    //    whole-register writes will undo it. [SRC gotcha 3]
    i2c_write(RTC_ADDR, 0x01, 0x07);

    // 5. Set the time in ONE transaction, 03h..0Ah, with STOP asserted for a
    //    clean seconds boundary. Writing 04h with bit 7 clear also clears OS.
    // 6. Only now report "time valid" to the rest of the system.
}
```

Note step 3's condition. On an **Inkplate 5** (`C34`/`C35` DNP) the internal capacitors are the whole load, so `CAP_SEL` = 1 (12.5 pF) is likely correct. On **Inkplate 5 Gen 2 / ZeroWriter Ink** (12 pF fitted) `CAP_SEL` = **0** is likely correct. **Likely**, because the crystal's specified `CL` is ambiguous — §4.2. Measure.

### 10.3 A note on `CLKOUT` and power

`CLKOUT` is **push-pull, enabled at power-on, at 32.768 kHz**, and `CLKOE` is hard-tied high on these boards, so it toggles from the instant the RTC has power. Every datasheet `IDD` figure in §2.2 is specified with *CLKOUT disabled*. Driving even a short trace and a test pad at 32.768 kHz costs `f × C × V²` — with, say, 10 pF of trace and pad at 3 V that is ~3 nW, negligible against 220 nA × 3 V ≈ 660 nW, but it is not zero and it rises fast if anything is actually loading the pin. **[INF]**

Since `CLKOUT` goes nowhere useful in the default `JP2` position, **set `COF` = `111` in your init to park it LOW**, and only enable it when you are calibrating.

## 11. Pitfalls, in priority order

1. **`isSet()` is not `OS`.** §6.3. Read `04h` bit 7 yourself.
2. **`OS` = 1 for up to 2 s after power-up is normal**, not a fault. §6.1.
3. **`CAP_SEL` differs between Inkplate 5 and Gen 2/ZeroWriter**, and the crystal spec is ambiguous. §4. This is the drift bug you will actually hit.
4. **A software reset clears `CAP_SEL` and `Offset`.** §3.1, §9.3.
5. **`AEN_x` = 0 *enables* the comparison.** Inverted from intuition, and the reset value is "all disabled". §7.1.
6. **Never set time and date in two transactions.** Use `setEpoch()` or a single `03h`–`0Ah` write. §9.3, §10.1.
7. **`setAlarm()` resets `CLKOUT` to 32.768 kHz; `timerSet()` disables the alarm interrupt.** §9.3.
8. **`0x51` collides with common EEPROM breakouts** on the easyC/Qwiic connector. §5.1.
9. **The PCF8563 has the same address and a different map.** §12. A generic "PCF8563 RTC library" will half-work.
10. **`INT` is open-drain** with only 2 mA guaranteed sink, pulled up by `R42` to `3V3` — **not** to the RTC's own rail. It floats when the main rail is down. §5.2.
11. **`CLKOUT` runs at power-on** whether you want it or not. §10.3.
12. **The Inkplate library talks I²C behind a recursive mutex.** Take `mutexI2C` if you go around it. §5.1.
13. **Weekday is not BCD** — it is a plain 0–6 value in `08h` bits 2:0, with 0 = Sunday. `bcdToDec()` on it happens to be harmless for 0–6, but do not rely on that.
14. **`MI`/`HMI` require `Offset` `MODE` = 0** and are only regular when `OFFSET` = 0. §7.3.

## 12. Alternatives, and how they differ

| Part | Interface | `IDD` typ | Backup pin | Notable | Verdict |
|---|---|---:|---|---|---|
| **PCF85063A** (fitted) | I²C | **220 nA** | no | Alarm, timer, integrated selectable load caps, offset trim, tiny DFN | Correct choice for this class of device |
| `PCF85063B` | **SPI** | 220 nA | no | Otherwise identical | Only if you need SPI |
| `PCF85063TP` | I²C | 220 nA | no | **No alarm** | Never, for a wake-on-schedule design |
| **[`PCF8563`](../pcf8563/artifacts/pcf8563-datasheet-rev-11.pdf)** | I²C | 250 nA | no | **Same address `0x51`.** Uses a `VL` (voltage-low) flag instead of `OS`. Registers shifted: `Control_status_1` at `00h`, `Control_status_2` at `01h`, **`VL_seconds` at `02h`** (vs `04h` here) | The classic. See below |
| `PCF8523` | I²C | **150 nA** | **yes** | Lowest power, Fast-mode+ 1 MHz, proper battery-switchover pin | Would remove the need for `D11`/`D12` |
| `PCF85263A` / `PCF85363A` | I²C | 230 nA | **yes** | Timestamp/tamper input, stopwatch to 1/100 s, 64 B RAM (`85363A`) | If you need event timestamping |
| `PCF2127` / `PCF2129` | I²C **and** SPI | 500 nA | yes | **Temperature compensated, quartz built in, factory calibrated**, 512 B RAM (`2127`) | The answer if ±2 ppm at one temperature is not good enough |
| `DS3231` | I²C | ~840 nA (timekeeping) at addr `0x68` | yes | TCXO, ±2 ppm **over −40…+85 °C**, integrated crystal, two alarms | The industry default when accuracy matters more than power or cost. Much larger and ~10× the price |
| `PCA8565` | I²C | 600 nA | no | **AEC-Q100 grade 1**, −40…+125 °C | Automotive |

### 12.1 Cross-reference: the PCF8563 in this repository

This repository already holds NXP's PCF8563 datasheet at [`../pcf8563/artifacts/pcf8563-datasheet-rev-11.pdf`](../pcf8563/artifacts/pcf8563-datasheet-rev-11.pdf) (**Rev. 11, 26 October 2015**, `sha256:871273b1…d1b8da2e05f`). There is **no `README.md` in that directory yet** — it is an artifacts-only stub.

The two parts are close enough to be dangerous:

| | **PCF85063A** | **PCF8563** |
|---|---|---|
| 7-bit I²C address | **`0x51`** | **`0x51`** — *identical* |
| Address byte | `A2h` / `A3h` | `A2h` / `A3h` — *identical* |
| Register count | 18 (`00h`–`11h`) | 16 (`00h`–`0Fh`) |
| Control registers | `Control_1` `00h`, `Control_2` `01h` | `Control_status_1` `00h`, `Control_status_2` `01h` |
| Offset / trim register | **`Offset` at `02h`** | **none** — no aging trim at all |
| Free RAM byte | **`RAM_byte` at `03h`** | none |
| **Seconds register** | **`04h`**, integrity flag = **`OS`** (bit 7) | **`02h`**, integrity flag = **`VL`** (bit 7) |
| Integrity-flag meaning | oscillator has stopped | supply dropped below the low-voltage threshold |
| Internal load capacitors | **yes, selectable 7 / 12.5 pF** | **no** — external caps mandatory |
| `IDD` typ | 220 nA | 250 nA |
| Alarm / timer / CLKOUT | yes / yes / yes | yes / yes / yes |

> **A bus scan cannot tell them apart.** Both ACK at `0x51`. A PCF8563 driver pointed at a PCF85063A will read the `Offset` register as seconds and the `RAM_byte` as minutes — producing plausible-looking garbage rather than an obvious failure. If you are porting code between Soldered's easyC RTC breakouts, check which silicon you have.

## 13. Open questions

| Question | Status |
|---|---|
| **`X1`'s actual load capacitance — 7 pF or 12.5 pF** | **Unresolved and consequential.** BOM footprint field says `ABS07AIG-…-7-…`, value field says `7LC32768F12UC`. §4.2. Resolvable only by reading the can, or empirically by the `CLKOUT` measurement in §4.2 |
| Which `CAP_SEL` setting Soldered's shipped firmware uses on each board | **Not established.** The library defaults to whatever the POR leaves (`CAP_SEL` = 0), and nothing in `Inkplate::begin()` touches the RTC **[SRC]** |
| `D11`/`D12` actual part | **Unspecified.** BOM records `M4_DIODA` for both value and footprint. Reverse leakage — which dominates coin-cell life — is therefore unknown. §5.3 |
| Whether a CR2032 is shipped fitted in any of the three products | **Not established.** The holder is populated in all three BOMs; whether a cell is in the box is a packaging question no design file answers |
| Whether ZeroWriter's shipped firmware uses the RTC at all | **Not establishable.** Only the keyboard sketch is published; the main-board firmware is binary-only, and a string scan of SD-1.3 found only ESP-IDF-internal `rtc_*` symbols (the ESP32's *own* RTC domain), nothing PCF85063A-specific **[FW]** |
| Why the vendor example carries *"GPIO39 is NOT guaranteed for Inkplate 5v2"* | **Unexplained**, and contradicted by all three schematics. §5.2 |
| Whether `setClockOffset(1, -63)` in the calibration example reflects a measured board or is a placeholder | **Unknown.** It is the register's maximum negative value, which is suspicious either way. §9.3 |
| Silicon revision on physical units | Datasheet lists IC revision 1 for all orderable `85063A` parts **[DOC Table 2]**; not verified against a board photograph |

## Manufacturer

**NXP Semiconductors** — see the [NXP documentation-sourcing guide](../../../vendors/nxp/README.md) for this vendor's document portals, URL patterns, part-numbering conventions and known gotchas. **Note in particular NXP's inverted user-agent behaviour**: `nxp.com` returns 404 to browser user-agent strings and 200 to a bare `curl`, recorded in [`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

## Used By

- [Soldered Inkplate 5](../../../devices/soldered-electronics/inkplate-5/README.md) — reference designator `U7`, I²C `0x51` on ESP32-WROVER `IO21`/`IO22`, `INT` → `IO39` via `JP2`, coin cell `K10`. **`C34`/`C35` are DNP**, so the internal load capacitors are the entire crystal load
- [Soldered Inkplate 5 Gen 2](../../../devices/soldered-electronics/inkplate-5-gen2/README.md) — reference designator `U7`, same wiring, coin cell `K11`. **`C34`/`C35` = 12 pF fitted** — see §4.1, the correct `CAP_SEL` differs from the Inkplate 5
- [ZeroWriter Ink](../../../devices/zerowriter/zerowriter-ink/README.md) — reference designator `U7` on the respun "Zerowriter Inkplate 5 Gen2" main board. **Unchanged from the Gen 2 design**, including the 12 pF load capacitors, plus test points `TP73` (`GPIO_39`) and `TP74` (`CLKOUT_RTC`)

## Related pages

- [nxp/pcf8563](../pcf8563/artifacts/pcf8563-datasheet-rev-11.pdf) — same I²C address, different register map. §12.1. Artifacts-only directory; no record page yet
- [nxp/pcal6416a](../pcal6416a/README.md) — the other NXP part on the same I²C bus, at `0x20`. **The RTC is not behind it**
- [texas-instruments/tps65186](../../texas-instruments/tps65186/README.md) — third device on the bus, at `0x48`
- [texas-instruments/bq25306](../../texas-instruments/bq25306/README.md) — the ZeroWriter charger; together with this RTC it sets the device's standby drain
- [espressif/esp32-wrover](../../espressif/esp32-wrover/README.md) — the host, and the owner of `IO39`
- [wch/ch340c](../../wch/ch340c/README.md) — transport for Peripheral Mode's `rtc*` commands
- [Inkplate 5 Peripheral Mode](../../../devices/soldered-electronics/inkplate-5/features/peripheral-mode.md)

## Authoritative sources

| Title | URL | Retrieved | Version | Local artifact |
|---|---|---:|---|---|
| PCF85063A datasheet | https://www.nxp.com/docs/en/data-sheet/PCF85063A.pdf | 2026-08-23 (re-read 2026-08-26) | **Rev. 7, 30 March 2018** · 726,288 B · `sha256:a09223db…f430f6000b` | [artifacts/pcf85063a-datasheet.pdf](artifacts/pcf85063a-datasheet.pdf) |
| PCF85063A product folder (status Active) | https://www.nxp.com/products/PCF85063A | 2026-08-26 | — | — |
| PCF8563 datasheet — for the §12.1 comparison | https://www.nxp.com/docs/en/data-sheet/PCF8563.pdf | 2026-08-23 | **Rev. 11, 26 October 2015** · `sha256:871273b1…d1b8da2e05f` | [`../pcf8563/artifacts/pcf8563-datasheet-rev-11.pdf`](../pcf8563/artifacts/pcf8563-datasheet-rev-11.pdf) |
| Soldered Inkplate 5 schematic, `SD & RTC` sheet (`U7`, `X1`, `C34`/`C35` **DNP**, `D11`/`D12`, `K10`, `JP2`, `R42`) | https://github.com/SolderedElectronics/Soldered-Inkplate-5-hardware-design | 2026-08-24 | KiCad V1.2.0 | `../../../devices/soldered-electronics/inkplate-5/artifacts/hardware/soldered-inkplate-5-hardware-design/CAD/V1.2.0/SD & RTC.kicad_sch` |
| Soldered Inkplate 5 Gen 2 schematic, `SD & RTC` sheet (`C34`/`C35` = **12 pF**, `K11`) | https://github.com/SolderedElectronics/Soldered-Inkplate-5-gen2-hardware-design | 2026-08-24 | KiCad V1.1.0 | `../../../devices/soldered-electronics/inkplate-5-gen2/artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/CAD/V1.1.0/SD & RTC.kicad_sch` |
| ZeroWriter Ink schematic, `SD & RTC` sheet | https://github.com/zerowriter/zerowriter_ink | 2026-08-24 | KiCad v1.2.0 | `../../../devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter_ink/design/src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/SD & RTC.kicad_sch` |
| Same, plotted (visual confirmation of the diode-OR and `JP2`) | — | 2026-08-26 | page 4 of 8 | `.../Zerowriter Inkplate 5 Gen2/v1.2.0/OUTPUTS/Zerowriter Inkplate 5 Gen2 Schematics.pdf` |
| ZeroWriter PCB layout — `U7` footprint, **10 pads + isolated exposed pad → DFN2626-10** | — | 2026-08-26 | v1.2.0 | `.../Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/Zerowriter Inkplate 5 Gen2.kicad_pcb` |
| BOMs recording the `X1` value/footprint conflict (all three boards) | — | 2026-08-26 | — | `.../Soldered Inkplate 5 BOM.csv` · `.../Soldered Inkplate 5 Gen2 BOM.csv` · `.../Zerowriter Inkplate 5 Gen2.csv` |
| Inkplate Arduino library — RTC driver | https://github.com/SolderedElectronics/Inkplate-Arduino-library | 2026-08-26 | **v11.1.4**, LGPL-3.0 | `../../../devices/soldered-electronics/inkplate-5/artifacts/source-snapshots/Inkplate-Arduino-library/src/features/rtc/rtc.cpp` and `rtc.h` |
| Inkplate Arduino library — I²C mutex, `begin()`, peripheral addresses | — | 2026-08-26 | v11.1.4 | `.../src/system/inkplateSemaphore.cpp` · `.../src/Inkplate.cpp` · `.../src/features/TPS65186/TPS65186.h` · `.../src/boards/Inkplate5V2/pins.h` |
| Vendor RTC calibration example (`setInternalCapacitor`, `setClockOffset`, the drift procedure) | — | 2026-08-26 | v11.1.4 | `.../examples/Inkplate5V2/Diagnostics/Inkplate5V2_RTC_Calibration/Inkplate5V2_RTC_Calibration.ino` |
| Vendor deep-sleep + RTC alarm example (`esp_sleep_enable_ext0_wakeup(GPIO_NUM_39, 0)`) | — | 2026-08-26 | v11.1.4 | `.../examples/Inkplate5V2/Advanced/DeepSleep/Inkplate5V2_RTC_Alarm_With_Deep_Sleep/…ino` |
| Soldered PCF85063A breakout library | https://github.com/SolderedElectronics/PCF85063A-SOLDERED | 2026-08-26 | — | — |
| ZeroWriter shipped main-board firmware (string scan) | — | 2026-08-26 | SD-1.3 | `.../zerowriter_ink/firmware_releases/SD-1.3/firmware.bin` |
