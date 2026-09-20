# DKE DEPG0397BBS770F3

- **Category:** 3.97-inch active-matrix electrophoretic (e-paper) display module — 480 × 800, bi-stable, pure-reflective, SPI, with an [SSD1677](../../solomon-systech/ssd1677/README.md) driver bonded on
- **Manufacturer:** **DKE Holding Company Limited** (东方科脉 / Dongfang Kemai)
- **Research status:** the **full 30-page module user manual is retained** in `artifacts/`. **The PDF has no text layer** — every glyph is a vector outline — so every value below was transcribed by rendering pages to PNG at 140 dpi and reading the images. Pages 1, 4, 5, 6, 7, 8, 9, 10, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25 were read this way.
- **Retrieved:** 2026-09-01

The display of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) and its Lite sibling. The panel is bonded to a 24-pin FPC carrying a 4-wire SPI interface and the discrete boost network the on-chip DC/DC needs.

---

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[MAN]** | Read off a **rendered page image** of `artifacts/depg0397bbs770f3-epd-module-user-manual.pdf`, cited by manual page number | `executed-success` for the transcription; `not-tested` — the vendor's values themselves are unmeasured |
| **[SCH]** | Read out of `PaperMono_SCH_V0.6.2_20260522.pdf`, cited as sheet + designator + pin | `executed-success` for the extraction; `not-tested` electrically |
| **[SRC]** | Read out of M5Stack source at a cited `file:line` | `executed-success` for the read; `not-tested` on hardware |
| **[CTL]** | Solomon Systech SSD1677 datasheet, Rev 1.0, Nov 2018 — held at [`../../solomon-systech/ssd1677/artifacts/`](../../solomon-systech/ssd1677/README.md) | `not-tested` |
| **[DOC]** | `docs.m5stack.com` / `shop.m5stack.com`, retrieved 2026-09-01 | `not-tested` |
| **[INF]** | Inference | `inferred` |

> **Why the transcription method matters.** `pdftotext` returns **nothing** for this document — not garbage, nothing. Had it returned plausible-looking text, that text would have had to be validated against a rendered page before use. It does not, so page rasterisation was the only route. Every figure below can be re-checked by rendering the cited page:
>
> ```bash
> nix-shell -p poppler-utils --run \
>   'pdftoppm -r 140 -png -f 7 -l 7 artifacts/depg0397bbs770f3-epd-module-user-manual.pdf pg'
> ```

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **DKE Holding Company Limited** — the footer of every page; the mechanical drawing carries the Chinese mark **东方科脉** | **[MAN]** pp. 1–30 |
| Model on the manual cover | **`DEPG0397BBS770F3`** | **[MAN]** p. 1: "Specification for 3.97 inch EPD — Model NO. : DEPG0397BBS770F3" |
| Model per M5Stack's OTP demo | **`DEPG0397BBS770F3HP-XM`** | **[SRC]** `M5PaperMono-OTP-Demo/README.md`. ⚠ **Conflict — see §8-C1** |
| Document | **EPD Module User Manual**, 30 pp. The embedded mechanical drawing is `REV. A0`, `FIRST ISSUE`, dated **2024-09-29** | **[MAN]** pp. 1, 6 |
| Driver IC | **Solomon Systech `SSD1677`**, named on the mechanical drawing | **[MAN]** p. 6, drawing note 2 |
| Interface | **4-wire SPI** (`BS` pin tied low). 3-wire 9-bit SPI is selectable but not used here | **[MAN]** p. 7 pin 8, p. 8 note 5-5; **[SCH]** |
| Resolution | **480 (H) × 800 (V)**, DPI **235** | **[MAN]** p. 5 |
| Reference designator on PaperMono | FPC connector **`J5`**, sheet 4 | **[SCH]** |
| ⚠ Marking verified? | **No.** No photograph of the fitted panel's model/batch label was inspected. The mechanical drawing shows dedicated `MODEL NO.` and `BATCH NO.` fields on the back of the module, so the fitted part's exact suffix is physically checkable but was not checked here | **[INF]** |

---

## 2. Overview and features

**[MAN]** p. 4, verbatim in substance:

> DEPG0397BBS770F3 is an Active Matrix Electrophoretic Display (AM EPD), with interface and a reference system design. The display is capable to display image at **1-bit white and black** full display capabilities. The 3.97 inch active area contains 480 × 800 pixels. The module is a TFT-array driving electrophoresis display, with integrated circuits including gate driver, source driver, MCU interface, timing controller, oscillator, DC-DC, SRAM, LUT, VCOM. Module can be used in portable electronic devices, such as Electronic Shelf Label (ESL) System.

Feature list **[MAN]** p. 4:

- 480 × 800 pixels display
- High contrast, high reflectance
- Ultra-wide viewing angle, ultra-low power consumption
- **Pure reflective mode** — no backlight of its own (PaperMono adds a separate frontlight, §7)
- **Bi-stable display** — the image persists with power removed
- Commercial temperature range
- Landscape / portrait modes
- Hard-coat antiglare display surface
- **Ultra-low-current deep sleep mode**
- **On-chip display RAM**
- **Waveform can be stored in on-chip OTP or written by MCU**
- Serial peripheral interface available
- On-chip oscillator
- On-chip booster and regulator for generating VCOM, gate and source driving voltage
- **I²C signal master interface to read an external temperature sensor**
- **Built-in temperature sensor**

Note the manual describes the panel as **1-bit black and white** and, in the optical table, as `2Grey Level`. M5Stack markets it as 4-level greyscale and ships a working 4-grey demo. **Conflict — §8-C2.**

---

## 3. Mechanical and optical specification

### 3.1 Mechanical

**[MAN]** p. 5.

| Parameter | Specification | Unit | Remark |
|---|---|---|---|
| Screen size | **3.97** | inch | |
| Display resolution | **480 (H) × 800 (V)** | pixel | **DPI 235** |
| Active area | **51.84 × 86.40** | mm | |
| Pixel pitch | **0.108 × 0.108** | mm | |
| Pixel configuration | **Rectangle** | | |
| Outline dimension | **56.24 (H) × 96.62 (V) × 0.92** | mm | |
| Weight | **10.44 ± 0.5** | g | |

Additional dimensions from the mechanical drawing **[MAN]** p. 6: module thickness **0.92 ± 0.10 mm** without protect film; protect film (TPT) **0.50 mm**; FPC thickness **0.10 ± 0.03 mm**; stiffener on the connector side **0.30 ± 0.05 mm**; FPC tail overall **43.83 ± 0.30 mm**. Drawing tolerances: unmarked angles ± 5°, `.X = ±0.4 mm`, `.XX = ±0.20 mm`, `.XXX = ±0.20 mm`. Drawn by `HH HUANG`, checked `H GONG`, approved `LY YU`. RoHS mark present.

### 3.2 Optical

**[MAN]** p. 5. Measured with an Eye-One Pro spectrophotometer (note 3-1).

| Symbol | Parameter | Conditions | Min | Typ | Max | Unit |
|---|---|---|---:|---:|---:|---|
| `KS` | Black state L* value | | – | **24** | 30 | |
| `WS` | White state L* value | | **58** | **62** | – | |
| `WS` | **White ghosting ΔL** | Full display mode | – | **1** | – | |
| `WS` | White ghosting ΔL | Partial display mode | – | **1** | – | |
| `WS` | White ghosting ΔL | Full-partial display mode | – | **1** | – | |
| `R` | **White reflectivity** | White | **26** | **30** | – | **%** |
| `CR` | **Contrast ratio** | **Indoor** | **5** | **7** | – | |
| `GN` | **`2Grey Level`** | – | – | – | – | |
| `Life` | | **23 ± 3 °C, 55 ± 10 %RH** | | **5 years** | | |

Notes **[MAN]** p. 5: *3-2.* `CR = surface reflectance with all white pixels / surface reflectance with all black pixels`. *3-3.* "When the product is stored, the display screen should be kept **white and face up**."

Two things worth reading carefully rather than skimming:

- **Contrast ratio 5–7 is an e-paper figure, not an LCD figure.** A typical 7:1 with 30 % white reflectance is roughly newsprint. It is specified *indoor*; outdoors in daylight a reflective display gets better, not worse, but that is not what this row states.
- **The 5-year life figure is a storage/ambient-condition statement**, not a refresh-count endurance rating. The manual gives **no** maximum refresh count anywhere, which is exactly the number you would want when choosing between refresh modes.

---

## 4. FPC pin assignment

**24-pin FPC.** Transcribed in full from **[MAN]** p. 7, §5 *Input/output Pin Assignment*. `I` = input, `O` = output, `I/O` = bidirectional, `P` = power, `C` = capacitor pin.

| No. | Name | I/O | Description | Remark |
|---:|---|---|---|---|
| 1 | `NC` | | Do not connect with other NC pins | Keep Open |
| 2 | `GDR` | O | N-Channel MOSFET Gate Drive Control | |
| 3 | `RESE` | I | Current Sense Input for the Control Loop | |
| 4 | `NC` | | Do not connect with other NC pins | Keep Open |
| 5 | `VDHR` | C | Positive Source driving voltage | |
| 6 | `NC` | O | I2C Interface to digital temperature sensor Clock pin | Note 5-6 |
| 7 | `NC` | I/O | I2C Interface to digital temperature sensor Data pin | Note 5-6 |
| 8 | `BS` | I | Bus Interface selection pin | Note 5-5 |
| 9 | `BUSY_N` | O | Busy state output pin | Note 5-4 |
| 10 | `RST_N` | I | Reset signal input. Active Low. | Note 5-3 |
| 11 | `DC` | I | Data /Command control pin | Note 5-2 |
| 12 | `CSB` | I | Chip select input pin | Note 5-1 |
| 13 | `SCL` | I | Serial Clock pin (SPI) | |
| 14 | `SDA` | I/O | Serial Data pin (SPI) | |
| 15 | `VDDIO` | P | Power Supply for interface logic pins. It should be connected with VCI | |
| 16 | `VDD` | P | Power Supply for the chip | |
| 17 | `GND` | P | Ground | |
| 18 | `VDDD` | C | Core logic power pin. VDD can be regulated internally from VCI. A capacitor should be connected between VDD and VSS | |
| 19 | `VPP` | P | FOR TEST | Keep Open |
| 20 | `VSH` | C | Positive Source driving voltage | |
| 21 | `VGH` | C | Power Supply pin for Positive Gate driving voltage and VSH1 | |
| 22 | `VSL` | C | Negative Source driving voltage | |
| 23 | `VGL` | C | Power Supply pin for Negative Gate driving voltage, VCOM and VSL | |
| 24 | `VCOM` | C | VCOM driving voltage | |

Notes **[MAN]** p. 8:

- **5-1** `CSB` (CS#): the chip is enabled for MCU communication **only when CS# is pulled LOW**.
- **5-2** `DC` (D/C#): **HIGH ⇒ data, LOW ⇒ command**, in 4-wire SPI mode.
- **5-3** `RST_N` (RES#): reset is **active low**.
- **5-4** `BUSY_N`: "When Busy is **High**, the operation of chip should not be interrupted, **command should not be sent**." The chip raises Busy when outputting a display waveform and when communicating with a digital temperature sensor.
- **5-5** Bus interface selection:

  | `BS1` state | MCU interface |
  |---|---|
  | **L** | **4-line serial peripheral interface (SPI) — 8-bit SPI** |
  | H | 3-line serial peripheral interface (SPI) — 9-bit SPI |

- **5-6** Pins 6/7 "connect to the VSS if there is no external temperature sensor. External pull-up resistor is required when connecting to an I2C slave."

> ⚠ **`BUSY_N` is named as if active-low but documented as active-high.** Note 5-4 and the SSD1677 datasheet both say the pad outputs **high** while busy **[MAN]** p. 8, **[CTL]** §7 (`0x12`, `0x20`, `0x10`). The `_N` suffix is misleading. M5Stack's driver treats high as busy **[SRC]**.

### 4.1 Pin names differ between the module manual and the controller datasheet

The FPC labels are DKE's; the die pads are Solomon Systech's. They are not the same strings:

| FPC (DKE) | SSD1677 (Solomon Systech) |
|---|---|
| `BS` | `BS1` |
| `BUSY_N` | `BUSY` |
| `RST_N` | `RES#` |
| `DC` | `D/C#` |
| `CSB` | `CS#` |
| `SDA` | `SDI` / `SDO` (bidirectional on one pad) |
| `VDHR` | `VSH1R` / `VSH2R` family |
| `VDDD` | `VDD` |

**[MAN]** p. 7 vs **[CTL]** §5.

---

## 5. Electrical characteristics

### 5.1 Absolute maximum ratings

**[MAN]** p. 9, §6.1.

| Parameter | Symbol | Rating | Unit |
|---|---|---|---|
| Logic supply voltage | `VCI`, `VDDIO` | **−0.5 to +4.0** | V |
| Logic input voltage | `VIN` | −0.5 to V<sub>DDIO</sub> + 0.5 | V |
| Logic output voltage | `VOUT` | −0.5 to V<sub>DDIO</sub> + 0.5 | V |
| **Operating temperature** | `TOPR` | **0 to +50** | °C |
| **Storage temperature** | `TSTG` | **−25 to +70** | °C |
| Optimal storage temperature | `TSTGo` | **23 ± 3** | °C |
| Optimal storage humidity | `HSTGo` | **55 ± 10** | %RH |

> ⚠ **The panel's operating range is 0 to +50 °C — far narrower than the controller's.** The SSD1677 die is rated `TOPR` **−25 to +85 °C** **[CTL]** §10. The *module* is the binding constraint: below 0 °C the electrophoretic ink itself is out of specification, and the OTP waveform bank does not extend there. Anyone reasoning from the controller datasheet alone will over-estimate the environmental envelope by 25 °C at one end and 35 °C at the other. **[INF]** from two `not-tested` primary sources.
>
> Storage note **[MAN]** p. 9 note 2 and p. 5 note 3-3: **the screen should be left white and face up** during storage. This is a real requirement for e-paper, not boilerplate — a panel stored dark for long periods can retain the pattern.

### 5.2 Panel DC characteristics

**[MAN]** p. 10, §6.2. Conditions: `VSS = 0 V`, `VCI = 3.0 V`, `TOPR = 23 °C`.

| Parameter | Symbol | Condition | Pin | Min | Typ | Max | Unit |
|---|---|---|---|---:|---:|---:|---|
| Single ground | `VSS` | – | | – | 0 | – | V |
| **Logic supply voltage** | `VCI` | – | `VCI` | **2.2** | **3.0** | **3.3** | V |
| Power for interface logic pins | `VDDIO` | | `VDDIO` | 2.2 | – | 3.3 | V |
| Core logic voltage | `VDD` | | `VDD` | 1.7 | 1.8 | 1.9 | V |
| VCOM_DC output voltage | `Vcom` | – | `VCOM` | −4.0 | – | −0.1 | V |
| High level input voltage | `VIH` | – | – | 0.8 V<sub>DDIO</sub> | – | – | V |
| Low level input voltage | `VIL` | – | – | – | – | 0.2 V<sub>DDIO</sub> | V |
| High level output voltage | `VOH` | I<sub>OH</sub> = −100 µA | – | – | 0.9 V<sub>DDIO</sub> | – | V |
| Low level output voltage | `VOL` | I<sub>OL</sub> = 100 µA | – | – | – | 0.1 V<sub>DDIO</sub> | V |
| **Typical power** | `PTYP` | VCI = 3.0 V | | – | – | **36** | mW |
| **Deep sleep mode power** | `PSTPY` | VCI = 3.0 V | | – | – | **0.003** | mW |
| **Typical operating current** | `Iopr_VCI` | VCI = 3.0 V | | – | – | **12** | mA |
| **Image update time** | – | 23 °C | | – | – | **4** | **sec** |
| **Typical peak current** | `Iopr_VCI` | 2.3 – 3.6 V | | | **120** | – | mA |
| **Deep sleep mode current** | `Idslp_VCI` | DC/DC off, no clock, no input load, RAM data not retained | | – | – | **1** … **5** | µA |

Notes **[MAN]** p. 10: typical power is measured for a transition from a horizontal 2-scale pattern to a vertical 2-scale pattern; **"the listed electrical characteristics are only guaranteed under the controller & waveform provided by DKE"** (note 3); measured with a Tektronix MDO3014 oscilloscope and TCP0030A current probe (note 4).

> ⚠ **Note 3 is the most consequential sentence in the electrical section.** DKE guarantees these numbers **only for the waveform it programmed into the SSD1677's OTP**. M5GFX does *not* use that waveform — it uploads its own LUTs from flash (§7). Every figure in this table, including the 4-second image update time and the 120 mA peak, is therefore untested for the M5GFX path, and the vendor's own recommendation to prefer the OTP demo follows directly from it.
>
> **120 mA peak at 3 V is not negligible** for a battery device that also runs Wi-Fi. It is a short burst during the update, but a supply designed to the 12 mA typical figure will sag.

### 5.3 Serial interface timing

**[MAN]** p. 16. Conditions: `VDDIO − VSS = 2.2 V to 3.7 V`, `TOPR = 23 °C`, `CL = 30 pF`.

**Write mode**

| Symbol | Parameter | Min | Typ | Max | Unit |
|---|---|---:|---:|---:|---|
| `fSCL` | **SCL frequency (write mode)** | | | **20** | **MHz** |
| `tCSSU` | CS# low before the first rising edge of SCLK | 20 | | | ns |
| `tCSHLD` | CS# remains low after the last falling edge of SCLK | 20 | | | ns |
| `tCSHIGH` | CS# remains high between two transfers | 100 | | | ns |
| `tSCLCYC` | SCL cycle time | 50 | | | ns |
| `tSCLHIGH` | SCL high time | 25 | | | ns |
| `tSCLLOW` | SCL low time | 25 | | | ns |
| `tSISU` | SDA setup before the next SCL rising edge | 10 | | | ns |
| `tSIHLD` | SDA hold after the SCL rising edge | 40 | | | ns |

**Read mode**

| Symbol | Parameter | Min | Typ | Max | Unit |
|---|---|---:|---:|---:|---|
| `fSCL` | **SCL frequency (read mode)** | | | **2.5** | **MHz** |
| `tCSSU` | | 100 | | | ns |
| `tCSHLD` | | 50 | | | ns |
| `tCSHIGH` | | 250 | | | ns |
| `tSCLHIGH` / `tSCLLOW` | | 180 | | | ns |
| `tSOSU` | SDA (read) stable before the next SCL rising edge | | 50 | | ns |
| `tSOHLD` | SDA (read) stable after the SCL falling edge | | 0 | | ns |

> ⚠ **Write is 20 MHz max; read is 2.5 MHz max — an 8× asymmetry.** Any code that reads back the OTP registers or the status byte at the write clock is out of specification. This figure is identical in the SSD1677 datasheet **[CTL]** §12.1, so the two documents agree.
>
> ⚠ **M5GFX drives this panel at 40 MHz** — `freq_write = 40000000` **[SRC]** `M5GFX/src/M5GFX.cpp:2114` — which is **twice the documented maximum**. The vendor's own recommended OTP demo uses **20 MHz**, exactly at spec **[SRC]** `EDP_SPI.cpp:33`. See §8-C4.

---

## 6. Command set as this module documents it

The command table is the SSD1677's, reproduced by DKE in abbreviated form on **[MAN]** pp. 17–20. The [SSD1677 record](../../solomon-systech/ssd1677/README.md) carries the controller-level detail; what follows is what *DKE* chose to document for *this* module, which is a strict subset and is the better guide to what the fitted OTP actually supports.

| Hex | Command | Parameters DKE documents |
|---|---|---|
| `0x01` | Driver Output control | `A[9:0] = 2A7h [POR], 680 MUX`; `B[2:0] = 000 [POR]` |
| `0x03` | Gate Driving voltage control | `A[4:0] = 17h [POR]`, VGH at 20 V; range 12–20 V |
| `0x04` | Source Driving voltage control | `A = 41h` (VSH1 15 V), `B = A8h` (VSH2 5.0 V), `C = 32h` (VSL −15 V) |
| `0x10` | **Deep Sleep mode** | `A[1:0]`: `00` normal [POR], **`11` enter deep sleep**. "BUSY pad will keep output high" |
| `0x11` | Data Entry mode setting | `A[1:0]` = ID[1:0] increment/decrement; `A[2]` = AM (X- or Y-direction address advance) |
| `0x12` | SWRESET | Resets commands/parameters to S/W-reset defaults **except `R10h` Deep Sleep**. **RAM is unaffected** |
| `0x18` | Temperature Sensor Control | **`A = 48h` [POR] external sensor; `A = 80h` internal sensor** |
| `0x1A` | Temperature Sensor Control (write) | `A[11:0] = 7FFh [POR]` |
| `0x20` | **Master Activation** | Activates the display-update sequence selected by `R22h`. "User should not interrupt this operation to avoid corruption of panel images" |
| `0x21` | Display Update Control 1 | `A[7:4]` Red RAM option, `A[3:0]` BW RAM option: `0000` normal, `0100` bypass as 0, `1000` inverse |
| `0x22` | **Display Update Control 2** | See below — **DKE documents only three values** |
| `0x24` | Write RAM (BW) | **White pixel = 1, black pixel = 0** |
| `0x26` | Write RAM (RED) | RED = 1; white/black = 0 |
| `0x2C` | Write VCOM register | `A[7:0] = 50h` |
| `0x2D` | OTP Register Read | 11 bytes: `A`–`B` VCOM information, `C`–`G` display mode, `H`–`K` waveform version |
| `0x2F` | Status Bit Read | `[5]` HV-ready flag (0 = ready), `[4]` VCI-detection flag, `[2]` busy flag, `[1:0]` chip ID [POR `01`]. **`[5]`/`[4]` are invalid after reset until commands `0x14`/`0x15` are issued** |
| `0x32` | Write LUT | LUT register from the MCU interface |

`0x22` values, as DKE documents them **[MAN]** p. 18:

| Setting | Sequence | Value |
|---|---|---|
| **LUT from MCU** | Enable clock → enable analog → **pattern display** → disable analog → disable OSC | **`C7`** |
| **LUT from OTP** (external temperature sensor operation) | Enable analog → **load LUT** | **`90`** |
| | Enable analog → **pattern display** → disable analog → disable OSC | **`47`** |

> ⚠ **The values M5Stack actually uses are in neither table.** The OTP demo writes `0x22` = **`0xF8`** (partial refresh), **`0x14`** (partial follow-up), **`0xFF`** (mono full refresh) and **`0xD7`** (four-grey full refresh) **[SRC]** `EDP_OTP_LUT_demo.cpp:264-266, 276-279, 319-321, 370-375`. DKE's reference program at **[MAN]** p. 24 uses **`0xF7`**. The SSD1677 datasheet enumerates twelve values (`80 01 C0 03 91 99 B1 B9 C7 CF F7 FF`) **[CTL]** §7, of which only `FF` matches M5Stack's set. §8-C5.

---

## 7. Operation

### 7.1 LUT-from-OTP operation flow

**[MAN]** p. 23, §10.1, transcribed from the flowchart:

```
Power On (Apply VCI)
        ↓
Reset the EPD driver IC
        ↓
Turn on the oscillator clock and DC/DC regulator to generate the drive voltage
        ↓
Define the display size, RAM address, border
        ↓
Load LUT from OTP
        ↓
Load image data and update
        ↓
   ┌────┴────┐
Power Off   Enter into deep sleep
   │             │
   └→ Power On   └→ Reset the EPD driver IC
```

Two exits are drawn, and they re-enter at different points: **power-off returns to "Power On"**, **deep sleep returns to "Reset the EPD driver IC"**. That matches the controller's rule that leaving deep sleep requires a hardware reset **[CTL]** §7 (`0x10` remark).

### 7.2 OTP operation reference program code

**[MAN]** p. 24, §10.2, transcribed in full. This is DKE's own known-good sequence and is the reference against which M5Stack's driver should be judged.

| Action | Value / data | Comment |
|---|---|---|
| **POWER ON** | 3 V | |
| delay | 10 ms | |
| **PIN CONFIG** | | |
| `RES#` | low | Hardware reset |
| delay | **200 µs** | |
| `RES#` | high | |
| delay | **200 µs** | |
| Read busy pin | | Wait for busy low |
| Command `0x12` | | Software reset |
| Read busy pin | | Wait for busy low |
| Command `0x0C` | `AE C7 C3 C0 80` | Booster Soft-start Control |
| Command `0x01` | `DF 01 02` | Set display size and driver output control |
| Command `0x11` | **`01`** | RAM data entry mode |
| Command `0x44` | `00 00 1F 03` | Set RAM X address |
| Command `0x45` | `DF 01 00 00` | Set RAM Y address |
| Command `0x3C` | `01` | Set border |
| Command `0x18` | `80` | *(internal temperature sensor)* |
| **LOAD IMAGE AND UPDATE** | | |
| Command `0x4E` | `00 00` | Set RAM X address counter |
| Command `0x4F` | `DF 01` | Set RAM Y address counter |
| Command `0x24` | **48000 bytes** | Load BW image (800/8 × 480) |
| Command `0x22` | **`F7`** | Image update |
| Command `0x20` | | |
| Read busy pin | | Wait for busy low |
| Command `0x10` | **`01`** | Enter deep sleep mode |
| **POWER OFF** | | |

Decoding the geometry parameters against the controller **[CTL]** §7, §8.1, §8.3–8.5 — `inferred`, arithmetic shown so it can be checked:

- `0x01` `{DF, 01, 02}` ⇒ `A[9:0] = 0x1DF = 479`; MUX gate lines = `A + 1` = **480 gate lines**. `B[2:0] = 010` ⇒ `SM = 1`, i.e. the interlaced scan order `G0, G2, G4 … G678, G1, G3 …`.
- `0x44` `{00, 00, 1F, 03}` ⇒ `XSA = 0x000`, `XEA = 0x31F = 799` ⇒ **800 source columns**.
- `0x45` `{DF, 01, 00, 00}` ⇒ `YSA = 0x1DF = 479`, `YEA = 0x000` ⇒ **480 rows, counted downward**.
- `0x11 = 0x01` ⇒ Y decrement, X increment; `AM = 0` ⇒ counter advances in X.
- 48 000 bytes = 800 × 480 / 8. ✅ consistent.

So **the panel is 800 source × 480 gate.** That contradicts the mechanical drawing on the same document's page 6 — §8-C3.

### 7.3 What M5Stack's OTP demo does differently

`M5PaperMono-OTP-Demo` follows DKE's sequence closely, which is itself evidence the demo was derived from this manual **[SRC]** `components/EDP_OTP_LUT_demo/src/EDP_OTP_LUT_demo.cpp:206-224`:

| Step | DKE reference **[MAN]** p. 24 | M5Stack OTP demo **[SRC]** | Same? |
|---|---|---|---|
| `0x12` software reset | ✅ | `EDP_OTP_LUT_demo.cpp:206` | ✅ |
| `0x0C` booster soft-start | `AE C7 C3 C0 80` | `{0xAE,0xC7,0xC3,0xC0,0x80}` at `:221`, `:336` | ✅ **byte-identical** |
| `0x01` driver output | `DF 01 02` | `{0xDF,0x01,0x02}` at `:222`, `:337` | ✅ **byte-identical** |
| `0x18` temperature sensor | `80` (internal) | `{0x80}` at `:220`, `:356` | ✅ |
| `0x3C` border | `01` | `{0x01}` at `:223`, `:355`; **`0x80` (float) for partial refresh** at `:251` | ✅ + extension |
| `0x11` data entry | `01` | **`0x03`** for mono at `:162`; **`0x02`** for four-grey at `:340` | ❌ **differs** |
| `0x21` RAM display mode | *(absent)* | `{0x00}` at `:224`, and again before mono refresh at `:319` | ➕ M5Stack adds |
| `0x1A` temperature override | *(absent)* | **`{0x5A}` = 90** in four-grey mode at `:357` | ➕ M5Stack adds |
| `0x22` update value | **`F7`** | `0xFF` mono / `0xD7` four-grey / `0xF8`, `0x14` partial | ❌ **differs** |
| `0x10` deep sleep | `01` | `{0x01}` at `:236` — **after every refresh** | ✅ |
| RAM pre-clear `0x46`/`0x47` | *(absent)* | *(absent)* | both omit what **[CTL]** §9.1 prescribes |

Register `0x1A = 0x5A` (decimal 90) in the four-grey path is the interesting addition: the demo's own comment calls it "Gray-mode temperature value", i.e. it **forces a temperature reading** so that the controller's OTP LUT search selects the greyscale waveform bank rather than whichever bank the real die temperature would pick **[SRC]** `EDP_OTP_LUT_demo.cpp:357`. `inferred` — the mechanism follows from the controller's documented LUT-search rule ("last match wins" over 34 temperature ranges, **[CTL]** §6.9) but was not verified against DKE's OTP contents, which are not published.

Other demo details **[SRC]**: SPI2, mode 0, half-duplex, 4092-byte chunks, 20 MHz; packing MSB-first, 100 bytes per row × 480 rows; in mono RAM **1 = white, 0 = black** (matching `0x24`'s definition); four-grey encoding `white = 00, light = 10, dark = 01, black = 11` across the (`0x24`, `0x26`) plane pair; three frame buffers of 48 000 bytes allocated in PSRAM.

### 7.4 Typical application circuit

**[MAN]** p. 22, §9. The module needs an external boost network — the SSD1677's on-chip regulator drives an external FET:

| Part | Value | Reference part / requirement |
|---|---|---|
| `C4`, `C6` | 1 µF | 0603, X5R/X7R, 6 V |
| `C1 C2 C3 C5 C7 C8` | 4.7 µF | 0805, X5R/X7R, **25 V** |
| `C9` | 1 µF | 0805, X7R, 25 V |
| `R1` | **2.2 Ω** | 0805, 1 % — the `RESE` current-sense resistor |
| `D1 D2 D3` | Schottky | **MBR0530**: V<sub>R</sub> ≥ 30 V, I<sub>O</sub> ≥ 500 mA, V<sub>F</sub> ≤ 430 mV |
| `Q1` | NMOS | **Si1304BDL / NX3008NBK**: BV<sub>DSS</sub> ≥ 30 V, V<sub>GS(th)</sub> 0.9 V typ / 1.3 V max, R<sub>DS(on)</sub> ≤ 2.1 Ω @ V<sub>GS</sub> = 2.5 V |
| `L1` | **47 µH** | CDRH2D18 / LDNP-470NC |

`GDR` drives `Q1`'s gate, `RESE` senses the current through `R1`, and `D1`–`D3` with `C1`–`C3` form the charge pump that produces `VGH`/`VGL`. **The 25 V capacitor rating is not optional** — `VGH` reaches 20 V.

### 7.5 Reliability test conditions

**[MAN]** p. 25, §11. Useful as an environmental envelope even though these are DKE's qualification tests, not user ratings.

| # | Test | Condition |
|---|---|---|
| 1 | Low-temperature operation | **0 °C for 240 h** |
| 2 | High-temperature high-humidity storage | 60 °C / 80 %RH for 240 h |
| 3 | Thermal shock | 1 cycle: −25 °C / 30 min ↔ 60 °C / 30 min, **100 cycles** |
| 4 | Low-humidity storage | 60 °C / 35 %RH for 240 h |
| 5 | High-temperature high-humidity operation | 40 °C / 80 %RH for 240 h |
| 6 | ESD gun | Air ±4 kV; contact ±2 kV (HBM 100 pF / 1.5 kΩ); contact ±200 V (MM 200 pF / 0 Ω) — **naked EPD display, including IC and FPC area** |
| 7 | Vibration | 10–500 Hz, X/Y/Z, 1 h per direction |
| 8 | Drop | Height by object weight: ≤ 20 kg → 1000 mm; ≤ 50 kg → 500 mm; ≤ 100 kg → 250 mm |

Notes: "Stay white pattern for storage and non-operation test"; "Operation is black → white pattern, the interval is **150 s**."

That 150-second interval is worth noting — DKE's own endurance testing refreshes **once every 2.5 minutes**, which says something about the duty cycle the panel is designed for.

---

## 8. Conflicts and caveats

These are recorded, not resolved. Where a least-risky implementation path exists it is stated.

### C1 — Model number: `DEPG0397BBS770F3` vs `DEPG0397BBS770F3HP-XM`

| Source | String |
|---|---|
| Manual cover **[MAN]** p. 1 | "Model NO. : **`DEPG0397BBS770F3`**" |
| Mechanical drawing title block **[MAN]** p. 6 | `PROJECT: DEPG0397BBS770F3` |
| `M5PaperMono-OTP-Demo/README.md` **[SRC]** | "**`DEPG0397BBS770F3HP-XM`**" |
| `docs.m5stack.com` product pages **[DOC]** | *no panel part number at all* — only "3.97-inch Touchscreen" in the datasheet list |

**Unresolved.** The M5Stack string is a strict superset of the DKE string, so the likeliest reading is that `HP-XM` is a variant/customisation suffix — `HP` possibly a waveform or OTP option, `XM` a customer code — and that DKE supplied a customer-specific OTP under a base-model manual. That is a hypothesis, **not a finding**: no DKE document in hand mentions any suffix, and no part-number decoder for the `DEPGxxxx` family was located.

**Practical consequence.** The retained manual may describe a *base* model whose OTP contents differ from the fitted part's. §8-C2 is exactly the kind of divergence that would produce. **Least-risky path:** treat the manual's optical and electrical tables as indicative, read the fitted panel's actual OTP with command `0x2D` (returns VCOM information, display mode and a 4-byte **waveform version**) before relying on any waveform behaviour, and check the `MODEL NO.`/`BATCH NO.` fields silkscreened on the module's back **[MAN]** p. 6.

### C2 — Greyscale: `2Grey Level` vs 4-level greyscale

| Source | Claim |
|---|---|
| Manual optical table **[MAN]** p. 5 | Row `GN` — **`2Grey Level`** (all min/typ/max cells empty) |
| Manual overview **[MAN]** p. 4 | "capable to display image at **1-bit white and black** full display capabilities" |
| M5Stack product pages **[DOC]** | "3.97" **4-level grayscale** monochrome e-paper, 480×800" — on both the PaperMono and PaperMono-Lite spec tables |
| M5Stack OTP demo **[SRC]** | Implements a **four-grey mode** using the OTP waveform: two RAM planes, `white = 00, light = 10, dark = 01, black = 11`, `0x22 = 0xD7`, `0x1A = 0x5A` (`EDP_OTP_LUT_demo.cpp:139-140, 336-375`) |
| M5GFX **[SRC]** | Ships a `Panel_SSD1677_4Gray` class with four-grey LUTs |

**Unresolved.** Three readings are each plausible and the evidence does not choose between them:

1. **The manual is stale or describes a different OTP.** The `HP-XM` suffix (C1) would be the mechanism.
2. **`GN` documents the *guaranteed optically characterised* levels**, not the achievable ones. The row has no min/typ/max values, only a label — consistent with "we characterise black and white, we do not characterise intermediate levels". Under this reading four-grey works but its L* values, ghosting and life are unspecified.
3. **Four-grey is a controller capability being used beyond the module's specification.** The SSD1677 has two RAM planes and a `DISPLAY Mode 2` **[CTL]** §7 (`0x22`); driving them does not require the module vendor's blessing.

**Least-risky path.** Reading 2 is the one that costs nothing to assume: use four-grey, but **do not expect the p. 5 optical figures to hold for the intermediate levels**, and treat DKE's electrical note 3 (§5.2 — figures guaranteed only under DKE's waveform) as applying with extra force. Note also that the vendor's four-grey path *is* the OTP path, so it is at least using DKE's own waveform data rather than a third-party LUT.

### C3 — The mechanical drawing has gate and source swapped

| Source | Claim |
|---|---|
| Mechanical drawing note 3 **[MAN]** p. 6 | `RESOLUTION: 800gate X 480source` |
| Controller configuration, DKE's own reference code **[MAN]** p. 24 | `0x01` `{DF,01,02}` ⇒ **480 gate lines**; `0x44` ⇒ `XEA = 799` ⇒ **800 source columns** |
| SSD1677 hardware maximum **[CTL]** §1, §5 | **960 source outputs, 680 gate outputs** |
| M5Stack drivers **[SRC]** | `M5GFX.cpp:2126-2130` sets `panel_width = 800, panel_height = 480, offset_rotation = 3`; the OTP demo works natively in 800 × 480 |

**The drawing is wrong, and provably so:** 800 gate lines exceed the SSD1677's 680 gate outputs. The panel is **800 source × 480 gate**, and DKE's own reference program on p. 24 configures it that way. Recorded because the erroneous string is on a page a hardware engineer is likely to read in isolation.

### C4 — M5GFX exceeds the documented SPI write clock by 2×

| Source | Clock |
|---|---|
| Module manual **[MAN]** p. 16 | `fSCL` write mode **max 20 MHz** |
| SSD1677 datasheet **[CTL]** §12.1 | `fSCL` write mode **max 20 MHz** — same figure, independently stated |
| M5Stack OTP demo **[SRC]** `EDP_SPI.cpp:33` | **20 MHz** — at spec |
| M5GFX **[SRC]** `M5GFX.cpp:2114` | **40 MHz** — `freq_write = 40000000` |

Both primary documents agree on 20 MHz; M5GFX runs at double it. M5Stack's docs specify neither. This is **not** an interpretation conflict — it is a driver operating outside a specification that two independent vendor documents state identically.

Whether it misbehaves in practice is `not-tested` here; SPI over a short FPC often tolerates overclocking. But it is a concrete, checkable mechanism behind M5Stack's own warning that "the e-paper driver waveforms for PaperMono in the M5GFX library are currently unstable" **[DOC]**, and it is the first thing to change when debugging refresh artefacts.

### C5 — Nobody's `0x22` values match anybody's table

| Source | `0x22` values documented or used |
|---|---|
| SSD1677 datasheet **[CTL]** §7 | `80 01 C0 03 91 99 B1 B9 C7 CF F7 FF` |
| DKE manual **[MAN]** p. 18 | `C7` (LUT from MCU), `90` (load LUT from OTP), `47` (pattern display) |
| DKE reference program **[MAN]** p. 24 | `F7` |
| M5Stack OTP demo **[SRC]** | `FF` (mono full), `D7` (four-grey full), `F8` (partial), `14` (partial follow-up) |

Only `C7`, `F7` and `FF` are common to any two lists. `90`, `47`, `D7`, `F8` and `14` appear in exactly one source each.

**The values are evidently a bit-field, not an enumeration** — `C7` = `1100 0111`, `CF` = `C7 | 0x08` (mode 2), `F7` = `C7 | 0x30` (load temperature twice) — and M5GFX carries a comment confirming the field is decomposable: "0x07 becomes 0xC7 when the analog section is off: Mode 1 refresh, followed by analog and oscillator power-down" **[SRC]** `M5GFX develop:src/lgfx/v1/panel/Panel_SSD1677.cpp` in `_refresh_mode1_text`. But **no source in hand publishes the bit definitions**, so `0xD7`, `0xF8` and `0x14` cannot be decoded with confidence. `inferred`, and deliberately left there.

**Least-risky path:** copy the values from the vendor path you have chosen (DKE's `F7`, or M5Stack's OTP demo) rather than composing your own.

### C6 — Deep-sleep parameter `0x01` is not a documented value

Both DKE's reference program **[MAN]** p. 24 and M5Stack's demo **[SRC]** `EDP_OTP_LUT_demo.cpp:236` write `0x10` with data **`0x01`**. Both the module manual **[MAN]** p. 17 and the controller datasheet **[CTL]** §7 define only `A[1:0] = 00` (normal) and **`11`** (enter deep sleep) — i.e. `0x03`.

Two independent vendors using `0x01` against their own documentation is more likely to mean the parameter is decoded loosely (any non-zero, or bit 0 alone) than that both made the same typo, but that is **`inferred`**. Recorded because a reader who "corrects" `0x01` to `0x03` is departing from the only two known-working sequences.

### C7 — Resolution is quoted both ways round

Every `docs.m5stack.com` page and the SSD1677 configuration say **480 × 800**; both store product titles *and* both URL handles say **800 × 480** **[DOC]**. The manual says `480(H) × 800(V)` **[MAN]** p. 5 while its own reference code drives 800 columns × 480 rows **[MAN]** p. 24.

Not a contradiction — portrait-native panel, landscape-native RAM, marketing picks whichever reads better — but anyone writing a raw driver from the "480 × 800" figure **will get the axes transposed**. M5GFX resolves it with `offset_rotation = 3` **[SRC]**.

### C8 — Other gaps

- **No maximum refresh count / endurance rating** anywhere in the manual. The "5 years" life row is a storage-condition statement (§3.2).
- **No viewing-angle number** despite "ultra wide viewing angle" in the feature list.
- **OTP contents are not published.** How many of the 34 waveform sets and temperature ranges DKE programmed, and over what temperature span, is unknown — and per **[CTL]** §6.9, "display will not be updated if no suitable temperature range matches the sensed temperature." Given the module's 0–50 °C operating rating (§5.1), behaviour below 0 °C is undefined in a specific and unpleasant way.
- **DC balance.** M5Stack warns that when supplying custom waveforms you must "pay attention to DC balance; otherwise, **irreversible damage may be caused to the panel**" **[DOC]**. DKE's manual does not restate this, because its recommended path is the factory OTP waveform where the question does not arise. It is the strongest argument for the OTP path over M5GFX's uploaded LUTs.

---

## 9. Used By

### [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) — FPC connector `J5`, sheet 4

The panel connects through a **24-pin FPC** to `J5`. The board provides the boost network of §7.4 as discrete parts around the connector, and routes the four SPI signals plus BUSY straight to the ESP32-S3 — but **not** reset or power, which come from the [M5IOE1](../../m5stack/m5ioe1/README.md) expander instead.

| `J5` pin | Panel signal | PaperMono net | Goes to | Evidence |
|---:|---|---|---|---|
| 2 | `GDR` | — | Gate of the boost NMOS | **[SCH]** `J5`.2 |
| 3 | `RESE` | — | Current-sense node | **[SCH]** `J5`.3 |
| 9 | `BUSY_N` | `G18_EINK_BUSY` | **ESP32-S3 GPIO18** | **[SCH]** `J5`.9; **[SRC]** `EDP_SPI.cpp:30`, `M5GFX.cpp:2125` |
| 10 | `RST_N` | `PYB_EINK_RST` | **M5IOE1 `IO5`** — *not* an ESP32 pin | **[SCH]** `J5`.10; **[SRC]** `EDP_SPI.cpp:38`, and `M5GFX.cpp:2124` sets `cfg.pin_rst = GPIO_NUM_NC` |
| 11 | `DC` | `G17_EINK_DC` | **ESP32-S3 GPIO17** | **[SCH]** `J5`.11; **[SRC]** `EDP_SPI.cpp:29`, `M5GFX.cpp:2109` |
| 12 | `CSB` | `G16_EINK_CS` | **ESP32-S3 GPIO16** | **[SCH]** `J5`.12; **[SRC]** `EDP_SPI.cpp:28`, `M5GFX.cpp:2085, 2123` |
| 13 | `SCL` | `G15_SPI2_CLK` | **ESP32-S3 GPIO15** | **[SCH]** `J5`.13; **[SRC]** `EDP_SPI.cpp:27`, `M5GFX.cpp:2108` |
| 14 | `SDA` | `G14_SPI2_MOSI` | **ESP32-S3 GPIO14** | **[SCH]** `J5`.14; **[SRC]** `EDP_SPI.cpp:26`, `M5GFX.cpp:2106` |
| 15 | `VDDIO` | `EPD_3V3_L3B` | Rail gated by **M5IOE1 `IO3`** | **[SCH]** `J5`.15; **[SRC]** `EDP_SPI.cpp:37` |
| 17–24 | `GND`, `VDDD`, `VSH`, `VGH`, `VSL`, `VGL`, `VCOM` | — | Local decoupling: `C77`–`C84`, values **1 µF/25 V** and **4.7 µF/25 V** as the manual specifies | **[SCH]** `J5`.17–.24 |

Sheet 4 also shows the nets `PREVGH` and `PREVGL` near `J5`.21–.23 **[SCH]**, matching DKE's own block diagram where the driver PCBA's DC/DC circuit feeds `PREVGH & PREVGL` to the panel **[MAN]** p. 21.

Board-level consequences worth stating in this record because they are properties of *the panel's integration*, not of the panel:

- **Reset and power both live behind the I²C expander.** You cannot reset or power-cycle the display without a working I²C bus and a working M5IOE1. `EDP_SPI.cpp`'s `hardware_reset()` does exactly this: enable `IOE_EPD_ENABLE` (raw pin `2` = `IO3`), then pulse `IOE_EPD_RESET` (raw `4` = `IO5`) low for 10 ms and high for 10 ms **[SRC]** `EDP_SPI.cpp:36-38` and the surrounding function. Note the **10 ms** pulses versus DKE's **200 µs** (§7.2) — M5Stack is generous, which is the safe direction.
- **The panel is driven landscape and rotated in software** — `offset_rotation = 3` **[SRC]** `M5GFX.cpp:2126-2130`. See §8-C7.
- **PSRAM is a hard requirement.** M5GFX aborts display init with `"M5PaperMono need OPI-PSRAM enabled"` if `CONFIG_SPIRAM_MODE_OCT` is absent **[SRC]** `M5GFX.cpp:2072-2081`; the board still enumerates but the screen stays dark. The OTP demo allocates 3 × 48 000 bytes in PSRAM **[SRC]** `EDP_OTP_LUT_demo.cpp:96`.
- **A frontlight is added by the board, not the module.** The panel is pure-reflective (§2); PaperMono's frontlight is a separate 15 V LED string (`BL_15V_L3B`, `EINK_BL`) driven by PWM from the [M5PM1](../../m5stack/m5pm1/README.md) `IO3` **[SCH]** sheet 1, `U7`.13.
- **M5Stack's own refresh timings should not be treated as characteristic of this panel.** The published figures (`epd_quality` 4.71 s, `epd_text` 0.45 s, `epd_fast` 0.34 s, `epd_fastest` 0.07 s **[DOC]**) are M5GFX LUT timings from an unnamed build; both `lut_quality` and `lut_text` were replaced on M5GFX `develop`, and the factory firmware pins an older commit than either branch head **[SRC]**. DKE's own figure for a full update is **4 s** at 23 °C (§5.2).

### [M5Stack PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md)

**Same panel, same connector, same wiring.** The Lite differs from the PaperMono only in dropping NFC and LoRa; both product pages carry an identical display specification row and both link the same "3.97-inch Touchscreen" datasheet **[DOC]**. The Lite's schematic is published as a 4-sheet `PRJ` PDF rather than a 6-sheet `SCH`, so its `J5` wiring is **not** independently confirmed here.

---

## 10. Related components

- [**Solomon Systech SSD1677**](../../solomon-systech/ssd1677/README.md) — the driver IC bonded to this panel. Command-level detail, OTP mechanism, LUT search and the DC-balance hazard live there
- [**M5Stack M5IOE1**](../../m5stack/m5ioe1/README.md) — supplies this panel's **reset** (`IO5`) and **3V3 rail** (`IO3`)
- [**M5Stack M5PM1**](../../m5stack/m5pm1/README.md) — drives the board's frontlight, which the panel itself does not have
- [Vendor sourcing guides index](../../../vendors/README.md) — `vendors/dke/` exists but carries no sourcing guide yet. This manual was obtained only as an M5Stack product-page attachment, not from DKE

---

## 11. Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/depg0397bbs770f3-epd-module-user-manual.pdf` | 8 666 208 | `6b65f56d5d549a132e5c807eef329fb3e997feab04ac06e8a107f01591618130` | **DKE EPD Module User Manual**, "Specification for 3.97 inch EPD", model `DEPG0397BBS770F3`, **30 pp.** PDF 1.4, A4. Producer **`iLovePDF`**, ModDate **2026-08-21** |

**⚠ No text layer.** All glyphs are vector outlines; `pdftotext` returns empty output for every page. Transcription was done from 140 dpi PNG renders (§Evidence labelling). The `iLovePDF` producer string and the 2026-08-21 modification date — the same day the PaperMono store listing went live — indicate the file was **re-processed before publication**, which is the most likely explanation for the lost text layer. There is no `Author`, `Title` or `Creator` metadata at all; the original authoring tool is unrecoverable from the file.

The manual is **undated on its cover** and carries **no revision table**. The only internal date is on the embedded mechanical drawing: `REV. A0`, `FIRST ISSUE`, **2024-09-29**.

**Licence.** DKE Holding Company Limited copyright, no licence statement, no confidentiality footer. Mirrored by M5Stack with no stated terms. Redistribution status **`unknown`**; disposition `repository`.

**Only one acquisition URL is known.** The document was located solely as an attachment on M5Stack's PaperMono product page, under the generic label "3.97-inch Touchscreen". No DKE-hosted copy was found. That single-source status is recorded here deliberately rather than left as a silent gap.

---

## 12. Authoritative sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | EPD Module User Manual — `DEPG0397BBS770F3` | **DKE Holding Company Limited**, mirrored by M5Stack | primary (via authorized mirror) | module specification | `artifacts/depg0397bbs770f3-epd-module-user-manual.pdf`; upstream `static-cdn.m5stack.com/resource/docs/products/core/PaperMono/…` (linked as "3.97-inch Touchscreen") | 2026-09-01 | undated cover; drawing **REV A0, 2024-09-29**; file ModDate 2026-08-21 | §1–§8 |
| S-2 | SSD1677 datasheet | Solomon Systech, mirrored by M5Stack | authorized mirror | controller datasheet | [`../../solomon-systech/ssd1677/artifacts/ssd1677-rev1.0-nov2018-m5stack-mirror.pdf`](../../solomon-systech/ssd1677/README.md) | 2026-09-01 | **Rev 1.0, Nov 2018**, "Advance Information" | §4.1, §5.1, §6, §7.2, §8-C3/C4/C5/C6 |
| S-3 | PaperMono schematic | M5Stack | primary | schematic PDF | `PaperMono_SCH_V0.6.2_20260522.pdf` (held in the device tree) | 2026-09-01 | **V0.6.2, 2026-05-22**, 6 sheets | §9 wiring (sheet 4, `J5`) |
| S-4 | `M5PaperMono-OTP-Demo` | M5Stack | primary | source | `github.com/m5stack/M5PaperMono-OTP-Demo` @ `c7c02554f89fd06f80d988b805b2a59050c78a46` | 2026-09-01 | 2026-08-20, MIT | §1 model string, §7.3, §8-C1/C5/C6 |
| S-5 | `M5GFX` | M5Stack | primary | source | `github.com/m5stack/M5GFX`, `master` @ `d91077b9a607b59404e4e4a49f775c792bfae382`; `develop` @ `8d6e8b3e0e9629e0bf0702d263e9263b588b6075` | 2026-09-01 | release 0.2.28 | §8-C4/C5/C7, §9 |
| S-6 | PaperMono / PaperMono-Lite product pages | M5Stack | primary | vendor docs | `docs.m5stack.com/en/core/PaperMono`, `.../PaperMono-Lite` | 2026-09-01 | undated | §8-C2/C7/C8, §9 |
| S-7 | PaperMono store listing | M5Stack | primary | retail listing | `shop.m5stack.com/products/m5papermono-with-lora-nfc-800x480-3-97-eink-display` | 2026-09-01 | SKU `C153`, published 2026-08-21 | §8-C7 (the `800x480` handle) |
