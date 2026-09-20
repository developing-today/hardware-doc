# Texas Instruments DRV2605L

- **Category:** haptic driver (LRA/ERM, I2C, effect library, smart-loop)
- **Reference designator on this board:** `U13`
- **Marking in the schematic BOM field:** `DRV2605LDGSR` — 10-pin VSSOP (DGS), tape and reel
- **Owning MCU:** **ESP32-S3 only.** The ESP32-U4WDH has no connection to this part
- **Research status:** part identity, board wiring, register interface and calibration procedure established from primary sources; the *actuator* it drives is unidentified
- **Retrieved:** 2026-08-21; schematic re-read pin-by-pin and demo firmware audited 2026-08-23

## Evidence labelling

| Label | Meaning |
|---|---|
| **[SCH]** | Read directly off the five published schematic PNGs |
| **[FW]** | Extracted from a shipped factory binary |
| **[SRC]** | Read from Waveshare's published demo source |
| **[DOC]** | Stated by a manufacturer datasheet or official programming guide |
| **[WEB]** | Vendor web page / wiki |
| **[INF]** | Inference. Reasoning is always given |

---

## 1. Identity, and what the "L" means

The schematic BOM string is `DRV2605LDGSR` **[SCH, sheet 5 `5_DAC.png`]**. Waveshare's product page and wiki shorten this to "DRV2605" **[WEB]**. **Use the DRV2605L datasheet, not the DRV2605 one.** They are different documents:

| | DRV2605 | **DRV2605L** (fitted) |
|---|---|---|
| Document | SLOS825C (EN) / ZHCSCW9E (ZH) | **SLOS854D, May 2014, rev. March 2018** |
| Supply | 2.0–5.2 V | 2.0–5.2 V |
| Packages | WCSP-9 only | **DGS = 10-pin VSSOP** + YZF DSBGA-9 |
| ROM library | Immersion TouchSense 2200 | Immersion TouchSense 2200 (same 123 effects) |
| Register map | Broadly the same | Broadly the same — but **verify bit fields against SLOS854D** |

Decoding the ordering suffix **[DOC]**: `DRV2605L` base part, `DGS` = 10-pin VSSOP, `R` = tape-and-reel.

### ⚠ The vendor ships and links the WRONG PART's datasheet

This is a genuine, verified documentation-sourcing defect on Waveshare's part, and it appears in
**both** of the vendor's distribution channels. Every DRV2605 document Waveshare supplies for this
board is for the **non-L DRV2605**, which is *not* the part fitted:

| Vendor channel | File | Bytes | What it actually is | Correct for fitted part? |
|---|---|---:|---|---|
| Wiki link, `files.waveshare.com/wiki/common/Drv2605.pdf` | `Drv2605.pdf` | 2,478,601 | **`ZHCSCW9E`** — DRV2605 **non-L**, Chinese, rev. April 2018 | ❌ wrong part |
| Demo archive, `…-Demo/ESP-IDF/03_DRV2605_Test/components/SensorLib/datasheet/DRV2605.pdf` | `DRV2605.pdf` | 2,557,610 | **`SLOS825C`** — DRV2605 **non-L**, English, rev. Sept 2014 | ❌ wrong part |
| — | — | — | **`SLOS854D`** — DRV2605**L**, the fitted part | ✅ `artifacts/drv2605l-datasheet.pdf` |

> **Correction to an earlier claim in this file.** It previously stated that the `Drv2605.pdf`
> shipped inside the demo archive "is in fact **the DRV2605L datasheet**", with the filename
> dismissed as the vendor's "L"-dropping shorthand. **That is wrong.** That file is 2,557,610
> bytes and its page 1 reads `SLOS825C – DECEMBER 2012 – REVISED SEPTEMBER 2014` under the title
> **`DRV2605`** — the non-L part. It is byte-identical to
> [`../drv2605/artifacts/drv2605-datasheet-slos825c-2014-09-26.pdf`](../drv2605/artifacts/drv2605-datasheet-slos825c-2014-09-26.pdf).
> The filename is not shorthand; the vendor genuinely ships the wrong document.
>
> Verified 2026-08-24 with `unzip -l`, `sha256sum` and
> `nix-shell -p poppler-utils --run 'pdftotext -f 1 -l 1 <file> -'`.

**Consequence:** anyone who follows Waveshare's documentation — wiki link or bundled demo — will
be reading non-L register and electrical data while programming an L part. The register maps are
broadly similar, which is what makes this dangerous rather than obvious: it fails quietly, not
loudly. Verify every bit field against `SLOS854D` before trusting it. This is the single most
likely source of subtle haptic-driver bugs on this board.

The non-L documents are preserved in [`../drv2605/`](../drv2605/) as evidence of the sourcing
error, not as a reference for this part.

**Fitted date code / silicon revision: unknown.** No retained board photograph resolves the top marking on `U13`.

## 2. Absolute and recommended limits **[DOC, SLOS854D §6]**

| Parameter | Min | Typ | Max | Unit |
|---|---:|---:|---:|---|
| `VDD` supply (recommended) | 2.0 | — | 5.2 | V |
| `VDD` (absolute max) | −0.3 | — | 5.5 | V |
| Load impedance `ZL` at `VDD` = 5.2 V | 8 | — | — | Ω |
| LRA resonance frequency range `f(LRA)` | 125 | — | 300 | Hz |
| PWM input frequency at `IN/TRIG` | 10 | — | 250 | kHz |
| Analog input voltage at `IN/TRIG` | 0 | — | 1.8 | V |
| Digital `VIL` / `VIH` | — | — | 0.5 / 1.3 | V |
| `REG` pin regulator output | — | 1.83 | — | V |
| Shutdown current (`EN` = 0) | — | 4 | 7 | µA |
| Standby current (`EN` high, `STANDBY` = 1) | — | 4.1 | 7 | µA |
| Quiescent current (enabled, no signal) | — | 0.5 | 0.65 | mA |
| `EN` internal pull-**down** | — | 2 | — | MΩ |
| Operating free-air temperature | −40 | — | 85 | °C |
| ESD HBM, `OUT+`/`OUT−` (VSSOP) | — | ±500 | — | V |
| ESD HBM, other pins | — | ±1000 | — | V |

Two of these matter especially on this board:

- **8 Ω minimum load.** If you replace the actuator, do not fit anything below 8 Ω.
- **125–300 Hz LRA range.** The auto-resonance engine will not track an actuator outside this band. Most coin and bar LRAs sit at 170–235 Hz, so this is rarely a problem — but a "haptic" part that is really a buzzer or a kilohertz piezo cannot be driven closed-loop here.

## 3. Exact wiring on this board **[SCH, sheet 5 `5_DAC.png`]**

`U13` is drawn as the 10-pin DGS symbol. Every pin is accounted for:

| Pin | Name | Net on this board | Detail |
|---:|---|---|---|
| 1 | `REG` | — | `C44` 1 µF to GND. Internal 1.83 V regulator output; **not a rail you may load** |
| 2 | `SCL` | `HAPTIC_SCL` | Aliased to `TP_SCL` on sheet 2 → **ESP32-S3 GPIO12** |
| 3 | `SDA` | `HAPTIC_SDA` | Aliased to `TP_SDA` on sheet 2 → **ESP32-S3 GPIO11** |
| 4 | `IN/TRIG` | `HAPTIC_TRIG` | **Tied to GND** in sheet 2's alias block |
| 5 | `EN` | `HAPTIC_EN` | **Tied to 3V3** in sheet 2's alias block |
| 6 | `VDD/NC` | *unconnected* | Marked with an explicit no-connect cross. Datasheet permits tie-to-VDD or float |
| 7 | `OUT+` | `LRA_P` → pad `PP2` | Positive differential output |
| 8 | `GND` | GND | |
| 9 | `OUT−` | `LRA_N` → pad `PP1` | Negative differential output |
| 10 | `VDD` | `3V3` | `C43` 1 µF decoupling |

**Where the tie-offs actually are.** An earlier revision of this page said "EN is tied 3.3 V and IN/TRIG is tied ground in schematic" without saying where — and they are *not* drawn at the `U13` symbol. Sheet 5 shows only the net labels leaving the symbol. The tie-offs appear in the net-alias block in the **top-right corner of sheet 2 `2_ESP32S3-R8.png`**, where `HAPTIC_TRIG` terminates on a ground symbol and `HAPTIC_EN` terminates on `3V3`. That is where to look if you are verifying this yourself.

### 3.1 Consequences of the hardwired `EN` and `IN/TRIG`

This is the single most important practical section on this page.

| | Consequence |
|---|---|
| `EN` hard-tied to 3V3 | **You cannot hardware-shutdown the DRV2605L.** The 4 µA shutdown state is unreachable. Your only low-power option is the software `STANDBY` bit (register `0x01` bit 6), worth ~4.1 µA typ. Set it |
| `EN` hard-tied to 3V3 | The chip is powered and out of hardware reset the moment 3V3 rises, **before your firmware runs**. It sits in POR defaults: `MODE` = 0 (internal trigger), `STANDBY` = 1, `LIBRARY_SEL` = 1, `N_ERM_LRA` = 0 (**ERM**) |
| `IN/TRIG` hard-tied to GND | **External trigger, PWM and analog input modes are all unusable.** `MODE[2:0]` values 1, 2, 3 have no path to a host pin |
| `IN/TRIG` hard-tied to GND | The Immersion **Audio-to-Vibe** feature needs an analog audio signal on `IN/TRIG` and is therefore **unusable on this board**, despite the board having an audio path. Do not promise it |
| Both | The only usable modes are **0** (internal trigger), **5** (RTP), **6** (diagnostics) and **7** (auto-calibration) |

Grounding an unused `IN/TRIG` is exactly what TI recommends ("If not used, this pin should be connected to GND" **[DOC §5]**), so this is a deliberate and correct design decision — it just closes off three of the seven modes.

### 3.2 The I2C bus it shares

| Item | Value | Evidence |
|---|---|---|
| Bus | ESP32-S3 I2C0, `SDA` = GPIO11, `SCL` = GPIO12 | [SCH sheet 2] |
| Pull-ups | `R5` and `R6`, **5.1 kΩ to 3V3** | [SCH sheet 2] |
| DRV2605L address | **0x5A** (7-bit), fixed, not strappable | [DOC] |
| Other device on the bus | **CST816D touch controller at 0x15** | [SCH sheet 1, SRC] |
| Bus speed used by the vendor demo | **300 kHz** | [SRC `i2c_bsp.c`] |

Two gotchas:

1. **The address is not configurable.** There is exactly one DRV2605L address. A second haptic driver needs a different part or an I2C mux.
2. **The vendor demo enables the S3's *internal* pull-ups on top of the 5.1 kΩ externals** — `.flags = { .enable_internal_pullup = true }` in `i2c_bsp.c` **[SRC]**. The S3's internal pull-ups are roughly 45 kΩ, so the parallel result is ~4.6 kΩ and the effect is small. But it is redundant, and it will mask a missing-external-pull-up fault if you port this code to a board without `R5`/`R6`. Set it `false`; the externals are correct on their own.

### 3.3 The actuator

`OUT+`/`OUT−` go to `LRA_P`/`LRA_N` and terminate on two pads, `PP1` and `PP2` **[SCH]**. The fitted actuator is an LRA of **unknown manufacturer, model, resonance frequency, rated voltage and impedance**, documented on its own page: **[generic/lra-motor](../../generic/lra-motor/README.md)**. Everything in §5 below exists because those parameters are unknown and must be measured.

## 4. The register interface

Full map is SLOS854D §8.6. Working subset with POR defaults **[DOC]**:

| Reg | Default | Name | What you use it for |
|---:|---:|---|---|
| `0x00` | `0xE0` | `STATUS` | `DEVICE_ID[7:5]`, `DIAG_RESULT[3]`, `OVER_TEMP[1]`, `OC_DETECT[0]`. **Read after every calibration and diagnostic** |
| `0x01` | `0x40` | `MODE` | `DEV_RESET[7]`, `STANDBY[6]`, `MODE[2:0]`. Default `0x40` = standby + internal trigger |
| `0x02` | `0x00` | `RTP_INPUT` | Real-time playback amplitude byte |
| `0x03` | `0x01` | `LIBRARY_SEL` | `HI_Z[4]`, `LIBRARY_SEL[2:0]` |
| `0x04`–`0x0B` | `0x01`,`0x00`… | `WAV_FRM_SEQ1..8` | Eight sequence slots. Bit 7 = `WAIT` (low 7 bits become a delay of *n* × 10 ms instead of an effect). `0x00` terminates the sequence |
| `0x0C` | `0x00` | `GO` | Write `0x01` to fire. Self-clears |
| `0x0D`–`0x0F` | `0x00` | `ODT`, `SPT`, `SNT` | Overdrive / positive / negative sustain time offsets |
| `0x10` | `0x00` | `BRT` | Brake time offset |
| `0x16` | `0x3E` | `RATED_VOLTAGE` | **Calibration input** — steady-state drive level |
| `0x17` | `0x8C` | `OD_CLAMP` | **Calibration input** — peak overdrive clamp |
| `0x18` | `0x0C` | `A_CAL_COMP` | **Calibration output** — resistive-loss compensation |
| `0x19` | `0x6C` | `A_CAL_BEMF` | **Calibration output** — back-EMF normalisation |
| `0x1A` | `0x36` | `FEEDBACK_CTRL` | **`N_ERM_LRA[7]`**, `FB_BRAKE_FACTOR[6:4]`, `LOOP_GAIN[3:2]`, `BEMF_GAIN[1:0]`. Calibration writes `BEMF_GAIN` |
| `0x1B` | `0x93` | `CONTROL1` | `STARTUP_BOOST[7]`, `AC_COUPLE[5]`, `DRIVE_TIME[4:0]` |
| `0x1C` | `0xF5` | `CONTROL2` | `BIDIR_INPUT[7]`, `BRAKE_STABILIZER[6]`, `SAMPLE_TIME`, `BLANKING_TIME`, `IDISS_TIME` |
| `0x1D` | `0xA0` | `CONTROL3` | `NG_THRESH[7:6]`, `ERM_OPEN_LOOP[5]`, `SUPPLY_COMP_DIS[4]`, `DATA_FORMAT_RTP[3]`, `LRA_DRIVE_MODE[2]`, `N_PWM_ANALOG[1]`, **`LRA_OPEN_LOOP[0]`** |
| `0x1E` | `0x20` | `CONTROL4` | `ZC_DET_TIME[7:6]`, **`AUTO_CAL_TIME[5:4]`**, `OTP_STATUS[2]`, `OTP_PROGRAM[0]` |
| `0x20` | — | `OL_LRA_PERIOD` | Open-loop LRA drive period |
| `0x21` | — | `VBAT` | Supply voltage monitor |
| `0x22` | — | `LRA_RESONANCE_PERIOD` | **Measured resonance period — read this to discover your actuator's `f0`** |

> **Transcription warning.** SLOS854D's register-map *overview* table prints `BLANKING_TIME[1:0]` and `IDISS_TIME[1:0]` in `0x1C`, while the auto-calibration *procedure* text refers to `BLANKING_TIME[3:0]` and `IDISS_TIME[3:0]`. The per-register bit-field pages are authoritative. **Read SLOS854D §8.6 directly, rather than trusting any transcription including this one, when writing those two fields.**

### 4.1 Modes (`MODE[2:0]` in `0x01`) **[DOC]**

| Value | Mode | Usable on this board? |
|---:|---|---|
| 0 | Internal trigger — write `GO` | **Yes.** The normal mode |
| 1 | External trigger, edge | No — `IN/TRIG` grounded |
| 2 | External trigger, level | No — `IN/TRIG` grounded |
| 3 | PWM / analog input | No — `IN/TRIG` grounded |
| 4 | Audio-to-vibe | No — `IN/TRIG` grounded |
| 5 | Real-time playback (RTP) | **Yes.** Amplitude byte over I2C |
| 6 | Diagnostics | **Yes.** Fires a test pulse, reports in `DIAG_RESULT` |
| 7 | Auto calibration | **Yes.** See §5 |

### 4.2 Library selection (`LIBRARY_SEL[2:0]` in `0x03`) **[DOC §8.6, Table 7]**

| Value | Library |
|---:|---|
| 0 | Empty |
| 1 | TS2200 Library A (**ERM**) |
| 2 | TS2200 Library B (ERM) |
| 3 | TS2200 Library C (ERM) |
| 4 | TS2200 Library D (ERM) |
| 5 | TS2200 Library E (ERM) |
| **6** | **LRA Library** |
| 7 | TS2200 Library F (ERM) |

All libraries expose the same 123 numbered effects (`1` = Strong Click 100%, `47` = Buzz 1 100%, `118` = long buzz intended for programmatic stopping, …); they differ in the tuning applied.

### 4.3 ⚠ Both vendor demos select an ERM library for an LRA actuator

This is a real defect in the published examples, not a documentation nuance.

| Demo | Line | Library selected | Correct for an LRA? |
|---|---|---:|---|
| `Arduino/examples/03_DRV2605_Test/03_DRV2605_Test.ino` | `drv.selectLibrary(1);` | 1 = **ERM** Library A | **No** |
| `ESP-IDF/03_DRV2605_Test/components/i2c_equipment/i2c_equipment.cpp` | `drv.selectLibrary(5);` | 5 = **ERM** Library E | **No** |

**[SRC]**, cross-referenced against **[DOC Table 7]**.

Furthermore, **neither demo writes `N_ERM_LRA` (register `0x1A` bit 7), and neither demo runs auto-calibration** **[SRC]**. The POR default of `0x1A` is `0x36` — bit 7 clear — so in both official examples the DRV2605L is **running in ERM mode, with ERM library tuning, driving an LRA**.

It still buzzes, which is why the examples appear to work. What is actually lost:

- No auto-resonance tracking, so the LRA is driven off its `f0` and produces a fraction of the acceleration it could
- No automatic overdrive or braking, so clicks are mushy and long instead of crisp
- The `A_CAL_COMP`/`A_CAL_BEMF` values in use are ROM defaults (`0x0C`, `0x6C`) characterised against some entirely different actuator

**Do not copy `selectLibrary(1)` or `selectLibrary(5)` from the demos.** Use `6`, and calibrate. §5 is the procedure.

## 5. The calibration workflow for the fitted LRA

TI's procedure is SLOS854D §8.5.6 **[DOC]**. Below it is specialised to this board and to the fact that the actuator's parameters are unknown.

### 5.0 Prerequisite: find out what the actuator actually is

You cannot fill in `RATED_VOLTAGE` or `OD_CLAMP` without the actuator's rated RMS voltage, and you cannot choose a sensible `DRIVE_TIME` without its resonance frequency. Neither is published. Three routes, in increasing order of confidence:

1. **Ask the chip.** Put the device in LRA closed loop with a conservative guess, play effect 118 (long buzz), then read `LRA_RESONANCE_PERIOD` (`0x22`). The period is in units of 98.46 µs, so `f0 ≈ 1 / (value × 98.46 µs)`. Cheapest route; usually lands within a few Hz.
2. **Measure it.** Scope `LRA_P`/`LRA_N` at pads `PP1`/`PP2` while the auto-resonance engine runs, and read the commutation frequency.
3. **Impedance sweep.** Lift one actuator terminal and sweep with an LCR meter or network analyser. The impedance minimum is `f0`; the DC resistance is your sanity check against the 8 Ω floor.

For rated voltage, absent any datasheet, **start low**: 1.8 V RMS is a common rating for small LRAs and will not damage anything on a 3.3 V rail. Increase only after `f0` is confirmed and current draw observed.

### 5.1 Compute the register values **[DOC §8.5.2]**

For an **LRA in closed loop**:

```
V(LRA-CL_RMS) = 20.58e-3 × RATED_VOLTAGE[7:0]
                / sqrt( 1 - (4 × t(SAMPLE_TIME) + 300e-6) × f(LRA) )
```

Rearranged, with `SAMPLE_TIME` = 3 (300 µs, TI's recommended default) and a measured `f0`:

```
RATED_VOLTAGE = V_rms × sqrt( 1 - 1.5e-3 × f0 ) / 20.58e-3
```

Worked example, `V_rms` = 1.8 V and `f0` = 205 Hz:

```
sqrt(1 - 1.5e-3 × 205) = sqrt(0.6925) = 0.8322
RATED_VOLTAGE = 1.8 × 0.8322 / 20.58e-3 = 72.8   ->  write 0x49
```

The overdrive clamp in LRA mode uses the **peak** form:

```
V(LRA_clamp_peak) = 21.22e-3 × OD_CLAMP[7:0]
```

Pick a clamp comfortably above rated but at or below the supply. The rail is 3.3 V **[SCH]**, so ~3.0 V peak is the sensible ceiling:

```
OD_CLAMP = 3.0 / 21.22e-3 = 141   ->  write 0x8D
```

The datasheet is explicit **[DOC §8.5.2.2]**: *"If the supply voltage (VDD) is less than the overdrive clamp voltage, the output driver is unable to reach the clamp voltage value"*, and *"If the rated voltage exceeds the overdrive clamp voltage, the overdrive clamp voltage has priority"*. Setting `OD_CLAMP` above 3.3 V here achieves nothing — the rail is a hard ceiling.

`DRIVE_TIME[4:0]` is the **initial guess at the LRA half-period** **[DOC §8.5.1.1]**; TI's own example is 200 Hz → 2.5 ms. The field steps in 0.1 ms increments from a 0.5 ms base:

```
DRIVE_TIME = round( (1 / (2 × f0) - 0.5e-3) / 0.1e-3 )
```

For `f0` = 205 Hz: half-period 2.439 ms → `DRIVE_TIME` = round((2.439 − 0.5)/0.1) = 19 = `0x13`.

### 5.2 The sequence **[DOC §8.5.6]**

```c
// Preconditions on this board: EN is hard-tied high, so the part is already
// powered. IN/TRIG is hard-tied low, so no mode that uses it is available.

w(0x01, 0x07);              // 1. leave STANDBY, MODE = 7 (auto calibration)

w(0x1A, 0x80 | (2 << 4)     // 2a. N_ERM_LRA = 1  <-- THE STEP BOTH DEMOS SKIP
             | (2 << 2));   //     FB_BRAKE_FACTOR = 2, LOOP_GAIN = 2
                            //     (BEMF_GAIN is an OUTPUT; leave it)
w(0x16, 0x49);              // 2b. RATED_VOLTAGE, from §5.1
w(0x17, 0x8D);              // 2c. OD_CLAMP, from §5.1
w(0x1E, (0 << 6)            // 2d. ZC_DET_TIME = 0
             | (3 << 4));   //     AUTO_CAL_TIME = 3
w(0x1B, 0x13);              // 2e. DRIVE_TIME from §5.1. NB this clears
                            //     STARTUP_BOOST; OR in 0x80 to keep it
w(0x1C, (3 << 4)            // 2f. SAMPLE_TIME  = 3
             | (1 << 2)     //     BLANKING_TIME = 1
             | (1));        //     IDISS_TIME    = 1

w(0x0C, 0x01);              // 3. GO. Self-clears when calibration finishes.
while (r(0x0C) & 0x01) { delay_ms(5); }

if (r(0x00) & 0x08) {       // 4. DIAG_RESULT set = FAILED
    // Most common causes, in order:
    //   - actuator open circuit (check PP1/PP2)
    //   - RATED_VOLTAGE far too low to get the actuator moving
    //   - DRIVE_TIME nowhere near the real half-period
    //   - N_ERM_LRA left at 0 while an LRA is fitted
}

// 5. Harvest the results and cache them.
uint8_t comp = r(0x18);     // A_CAL_COMP
uint8_t bemf = r(0x19);     // A_CAL_BEMF
uint8_t fbck = r(0x1A);     // FEEDBACK_CTRL, now with BEMF_GAIN filled in

// 6. Switch to normal operation.
w(0x03, 0x06);              // LIBRARY_SEL = 6 = LRA library
w(0x01, 0x00);              // MODE = 0, internal trigger, out of standby
```

### 5.3 Persist the results — three options, two of them good

TI offers **[DOC §8.5.6 step 6]**: recalibrate on every power-up; store the results in host memory and rewrite them; or burn them into the DRV2605L's one-time-programmable memory via `OTP_PROGRAM` (`0x1E` bit 0).

| Option | Verdict on this board |
|---|---|
| Recalibrate every boot | **Fine, and the recommended default.** Costs a few hundred milliseconds and one perceptible buzz at startup, and self-corrects for temperature and ageing |
| Cache `A_CAL_COMP`, `A_CAL_BEMF`, `FEEDBACK_CTRL`, `RATED_VOLTAGE`, `OD_CLAMP`, `CONTROL1`, `CONTROL2`, `CONTROL4` in **NVS** and rewrite at boot | **Best user experience.** The S3 has an `nvs` partition **[FW]**. Rewrite all eight bytes, not just the two "output" ones |
| **`OTP_PROGRAM`** | **Do not.** One-time and irreversible. One attempt, on a board whose actuator has no datasheet — a wrong `RATED_VOLTAGE` permanently degrades the hardware. There is no upside; the S3 already has non-volatile storage |

### 5.4 Real-time playback (RTP) mode

RTP bypasses the ROM library and streams an amplitude envelope over I2C. The closed-loop machinery — resonance tracking, overdrive, braking — still applies, so RTP on a calibrated LRA is genuinely good.

```c
w(0x01, 0x05);              // MODE = 5, RTP
w(0x02, amplitude);         // write repeatedly to shape the envelope
// ...
w(0x02, 0x00);              // silence
w(0x01, 0x40);              // back to STANDBY when done
```

`DATA_FORMAT_RTP` (`0x1D` bit 3) picks the interpretation of `RTP_INPUT`: **0 = signed** (default, so `0x00` is mid-scale and the POR default is *silence*), **1 = unsigned** (`0x00` is minimum). Get this wrong and your envelope is inverted or clipped.

Practical rate limit: at the demo's 300 kHz bus speed a register write is roughly 100 µs, so a few kHz of envelope updates is achievable. Do not try to synthesise a waveform sample-by-sample — RTP sets the *amplitude*; the chip generates the carrier at `f0`.

## 6. Libraries, drivers and versions

### 6.1 What Waveshare ships **[SRC]**

Both official DRV2605 examples use **SensorLib 0.3.1** by Lewis He, vendored into the demo archive:

- Arduino: `Arduino/examples/03_DRV2605_Test/` uses `SensorDRV2605.hpp`, `drv.begin(Wire, DRV2605_SLAVE_ADDRESS, 11, 12)`
- ESP-IDF: `ESP-IDF/03_DRV2605_Test/components/SensorLib/` (`library.properties` → `version=0.3.1`), driven through a callback shim `i2c_dev_Callback()` in `components/i2c_equipment/i2c_equipment.cpp` so SensorLib's transport becomes the ESP-IDF 5.x `i2c_master` driver

The ESP-IDF project is built against **ESP-IDF 5.3.2** (`sdkconfig` header line) **[SRC]**.

SensorLib's DRV2605 class covers `begin`, `selectLibrary`, `setMode`, `setWaveform`, `run`, `stop`, `setRealtimeValue`, `useERM`, `useLRA`. **It exposes no auto-calibration routine.** For §5 you will be writing registers directly whichever wrapper you pick — SensorLib does not get in the way, but it does not help either.

| Library | Version | Where | Notes |
|---|---|---|---|
| SensorLib | **0.3.1** | https://github.com/lewisxhe/SensorsLib | What the vendor ships. Header-only C++, Arduino + ESP-IDF. Also covers the CST816 on this board |
| Adafruit DRV2605 Library | 1.2.x | https://github.com/adafruit/Adafruit_DRV2605_Library | The most widely used Arduino driver. Same API shape. Also no auto-cal helper |
| ESP-IDF `i2c_master` | ESP-IDF **5.3.2** as shipped; API stable since 5.2 | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32s3/api-reference/peripherals/i2c.html | Direct register access. **Recommended** — the part is 30 registers and calibration needs raw access anyway |
| Legacy `driver/i2c.h` | deprecated in ESP-IDF 5.x | — | Do not start new work on it |

### 6.2 Minimal ESP-IDF transport

```c
#include "driver/i2c_master.h"

#define DRV2605L_ADDR 0x5A

static i2c_master_dev_handle_t drv;

static esp_err_t w(uint8_t reg, uint8_t val) {
    uint8_t b[2] = { reg, val };
    return i2c_master_transmit(drv, b, 2, pdMS_TO_TICKS(100));
}
static uint8_t r(uint8_t reg) {
    uint8_t v = 0;
    i2c_master_transmit_receive(drv, &reg, 1, &v, 1, pdMS_TO_TICKS(100));
    return v;
}

void drv2605l_attach(i2c_master_bus_handle_t bus) {
    i2c_device_config_t cfg = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address  = DRV2605L_ADDR,
        .scl_speed_hz    = 300000,          // matches the vendor demo
    };
    ESP_ERROR_CHECK(i2c_master_bus_add_device(bus, &cfg, &drv));
    // sanity check: DEVICE_ID in 0x00 bits 7:5 reads 7 for DRV2605L
    assert(((r(0x00) >> 5) & 0x07) == 7);
}
```

Keep the `DEVICE_ID` check. `0x00` defaults to `0xE0`, so bits 7:5 = 7 identifies DRV2605L silicon; a `0` means you are talking to something else, and a bus NAK usually means the shared touch controller is holding the bus.

## 7. Initialisation and integration gotchas

1. **The chip is awake before your code is.** `EN` is tied high. Assume nothing beyond the POR defaults, and explicitly write every field you care about.
2. **`STANDBY` defaults to 1.** `0x01` POR value is `0x40`. Write only `MODE` and forget bit 6, and nothing plays — with no error.
3. **It shares a bus with the touch controller.** The CST816D at 0x15 is interrupt-driven on GPIO9 and will be transacted from an LVGL input-device callback. **Serialise both onto one bus handle or one mutex.** ESP-IDF 5.x's `i2c_master` bus object serialises internally; two independent drivers on the same pins would not.
4. **Haptic playback is slow relative to a UI frame.** A strong click is tens of milliseconds. Fire and return; never block an LVGL or display task on `while (r(0x0C) & 1)`.
5. **The 3.3 V rail is shared with the display and radios.** It comes from a `TLV62569DBVT` buck **[SCH]** — see [tlv62569dbvt](../tlv62569dbvt/README.md). A haptic pulse into a small LRA is modest next to the backlight, but firing haptics at the same instant as a Wi-Fi TX burst and a full-screen redraw stacks three transients on one rail. If you see brownouts, stagger them.
6. **`OVER_TEMP` and `OC_DETECT` in `0x00` are free diagnostics.** Poll them after playback during bring-up; an over-current flag usually means a shorted actuator or one below 8 Ω.
7. **Effect 118 is the one designed to be stopped programmatically.** Everything else runs to completion. To abort early, go to standby, or assert `HI_Z` (`0x03` bit 4) which takes effect immediately even mid-transaction **[DOC]**.
8. **`f0` drifts** with temperature and with how the actuator is mounted. Closed loop tracks it; open loop does not. That is the whole reason to use library 6 and closed loop rather than a fixed-frequency PWM.

## 8. Alternatives, if you are respinning rather than programming

| Part | Why you might |
|---|---|
| **DRV2605L** (this) | I2C, ROM library, closed loop, 2–5.2 V. Still the default choice |
| DRV2604L | Same family, **RAM** waveform storage instead of the licensed Immersion ROM library. Choose for fully custom effects |
| DRV2625 | Adds a proper `TRIG` and better LRA braking; different register map |
| DRV2603 | PWM-in only, no I2C, no library. Cheaper; you give up closed loop entirely |
| DRV8601 / plain H-bridge | Only for an ERM where feel does not matter |

On **this** board none are drop-in: the footprint is DGS/VSSOP-10 and `IN/TRIG` is grounded, so anything needing a PWM input is a non-starter without cutting a trace.

## 9. Open questions

| Question | Status |
|---|---|
| Actuator manufacturer, model, `f0`, rated voltage, impedance | **Unknown.** Not in any published Waveshare material. See [generic/lra-motor](../../generic/lra-motor/README.md). Recoverable only by measurement — §5.0 |
| `U13` date code / silicon revision | **Unknown.** Needs a board photograph at sufficient resolution |
| Whether the factory S3 firmware calibrates | **Not established.** No calibration-specific string in `WX-ESP32S3-KNOB_V1.2.bin` settles it. The published *demo* source definitively does not calibrate **[SRC]** |
| Why both demos pick an ERM library | **Unexplained.** Most plausibly copy-paste from Adafruit/SensorLib example sketches, which default to `selectLibrary(1)` for a generic ERM **[INF]** |

## Manufacturer

**Texas Instruments** — see the [Texas Instruments documentation-sourcing guide](../../../vendors/texas-instruments/README.md) for this vendor's document portals, URL patterns, part-numbering conventions, distribution channels and known gotchas.

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — reference designator `U13`, ESP32-S3 I2C0 @ 0x5A

## Related pages

- [generic/lra-motor](../../generic/lra-motor/README.md) — the actuator this part drives
- [hynitron/cst816d](../../hynitron/cst816d/README.md) — the other device on the same I2C bus
- [texas-instruments/tlv62569dbvt](../tlv62569dbvt/README.md) — the buck that supplies its 3V3
- [Pinouts and buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md)

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| DRV2605L datasheet, SLOS854D (May 2014, rev. March 2018) | https://www.ti.com/lit/gpn/DRV2605L | 2026-08-21 | [artifacts/drv2605l-datasheet.pdf](artifacts/drv2605l-datasheet.pdf) |
| DRV2605L product folder | https://www.ti.com/product/DRV2605L | 2026-08-21 | — |
| ⚠ Vendor's copy shipped in the demo archive — **is the non-L `SLOS825C`, NOT this part** | — | 2026-08-21 (re-identified 2026-08-24) | [`../drv2605/artifacts/drv2605-datasheet-slos825c-2014-09-26.pdf`](../drv2605/artifacts/drv2605-datasheet-slos825c-2014-09-26.pdf) |
| ⚠ Vendor's wiki link `files.waveshare.com/wiki/common/Drv2605.pdf` — **is the non-L `ZHCSCW9E` (Chinese), NOT this part** | https://files.waveshare.com/wiki/common/Drv2605.pdf | 2026-08-24 | [`../drv2605/artifacts/drv2605-datasheet-slos825-2025-06-02.pdf`](../drv2605/artifacts/drv2605-datasheet-slos825-2025-06-02.pdf) |
| Board schematic sheet 5 (DRV2605L symbol, `LRA_P`/`LRA_N`, `PP1`/`PP2`) | — | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/5_DAC.png` |
| Board schematic sheet 2 (`HAPTIC_*` alias block, I2C pull-ups `R5`/`R6`) | — | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/2_ESP32S3-R8.png` |
| Waveshare Arduino demo `03_DRV2605_Test` | — | 2026-08-21 | `.../artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Arduino/examples/03_DRV2605_Test/` |
| Waveshare ESP-IDF demo `03_DRV2605_Test` (SensorLib 0.3.1, IDF 5.3.2) | — | 2026-08-21 | `.../artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/ESP-IDF/03_DRV2605_Test/` |
| SensorLib | https://github.com/lewisxhe/SensorsLib | 2026-08-21 | vendored at `.../ESP-IDF/03_DRV2605_Test/components/SensorLib/` (v0.3.1) |
| Adafruit DRV2605 Library | https://github.com/adafruit/Adafruit_DRV2605_Library | 2026-08-23 | — |
| ESP-IDF v5.3.2 I2C master driver | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32s3/api-reference/peripherals/i2c.html | 2026-08-23 | closest archived PDF: `../../espressif/esp32-s3r8/artifacts/esp-idf-programming-guide-v5.2.5-esp32s3.pdf` |
| Waveshare product page | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-product-31623.html` |
| Waveshare wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-wiki-current.html` |
