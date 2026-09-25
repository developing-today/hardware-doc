# Knowles SPM1423HM4H-B — PDM MEMS microphone

> The microphone on the **Cardputer v1.0 and v1.1** (and on several other M5Stack products).
> Record created **2026-09-04**; **datasheet filed and mined 2026-09-20**.
> Manufacturer confirmed from the document itself: **Knowles Acoustics, a division of Knowles
> Electronics, LLC**, 1151 Maplewood Drive, Itasca, IL 60143 **[DS p.1]**.
> Document: *Digital "Mini" High SNR SiSonic™ Microphone Specification*, **Revision A**,
> release level **Active**, initial release **2012-02-16** (change record `C10113410`) **[DS p.11]**.

**Evidence codes.** **[DS p.N]** = this datasheet, page N of 11 · **[SCH]** = Cardputer mainboard
schematic text layer · **[SCH-V]** = read from a rendered page of that schematic ·
**[DOC]** = M5Stack PinMap page · **[SRC]** = vendor source code.

## Function

A **PDM (pulse-density modulation) digital output** MEMS microphone. It takes a clock in and
returns a 1-bit oversampled bitstream — no codec required, and no analog signal on the board.
The host decimates the bitstream in software or in an I²S/PDM peripheral.

This is the cheap, simple way to put a microphone on a microcontroller, and it is what the first
two Cardputers do.

## 1. The numbers this board actually depends on

Test conditions for the whole table: **23 ±2 °C, 60–70 % R.H., V<sub>DD</sub> = 1.8 V,
f<sub>clock</sub> = 2.4 MHz, no load** **[DS p.3]**. Note that the *characterisation* supply is
1.8 V, not the 3.3 V the Cardputer uses — see §3.

| Parameter | Min | Nom | Max | Unit | Why it matters here |
|---|---:|---:|---:|---|---|
| Supply `V`<sub>`DD`</sub> | **1.6** | — | **3.6** | V | The Cardputer runs it at **3.3 V** — inside the range, but only 0.3 V of headroom |
| Current `I`<sub>`DD`</sub> | — | — | **600** | µA | measured at V<sub>DD</sub> = 3.6 V **[DS p.3 note 6]** |
| Sleep current `I`<sub>`SLEEP`</sub> | — | 25 | 45 | µA | **only when f<sub>clock</sub> < 1 kHz** |
| Sensitivity | −25 | **−22** | −19 | dBFS | at 94 dB SPL, 1 kHz |
| SNR | — | **61.5** | — | dB(A) | 94 dB SPL, 1 kHz, A-weighted |
| THD | — | — | **1** | % | at 100 dB SPL |
| THD | — | — | **10** | % | at 110 dB SPL — the practical ceiling |
| **Clock frequency** | **1.0** | — | **3.25** | MHz | ⚠ see §2 |
| Clock duty cycle | 40 | — | 60 | % | |
| Clock rise / fall | — | — | 10 | ns | |
| Output load `C`<sub>`LOAD`</sub> | — | — | **100** | pF | |
| `V`<sub>`IL`</sub> | −0.3 | — | **0.35 × V<sub>DD</sub>** | V | at I<sub>out</sub> = 1 mA |
| `V`<sub>`IH`</sub> | **0.65 × V<sub>DD</sub>** | — | V<sub>DD</sub>+0.3 | V | |
| `t`<sub>`dv`</sub> — clock edge to valid data | 18 | — | **60** | ns | |
| `t`<sub>`dz`</sub> — clock edge to High-Z | 0 | — | 16 | ns | |
| Fall-asleep time | — | — | 10 | ms | |
| Wake-up time | — | — | 10 | ms | |
| Directivity | — | omni-directional | — | — | |
| Data format | — | **½-cycle PDM** | — | — | |

All of the above is **[DS p.3]**. The table is a **raster image** in the PDF — it has no text
layer, so every value here was read from a 170 dpi render of page 3, cross-checked against the
page heading *"6. ACOUSTIC & ELECTRICAL SPECIFICATIONS"* which *does* appear in the text layer.

**Absolute maximum ratings** **[DS p.3]**: `CLOCK` to ground −0.3 … **+5.0 V**;
`SELECT`, `V`<sub>`DD`</sub>, `DATA` to ground −0.3 … **+5.0 V**; input current **±5 mA**;
`DATA` output short circuit **indefinite** to ground or V<sub>DD</sub>.
Operating and storage temperature **−40 °C to +100 °C** **[DS p.2]**.

Supply-current model, for budgeting: **ΔI<sub>DD</sub> = 0.5 × V<sub>DD</sub> × C<sub>LOAD</sub> ×
f<sub>CLOCK</sub>** **[DS p.3 note 5]**. At 3.3 V, 100 pF and 2.4 MHz that is ≈ 400 µA of the
600 µA budget spent purely driving the data line — so keep the trace short and the load light.

## 2. ⚠ Four traps

**2.1 — Polarity is inverted.** *"Increasing sound pressure → **decreasing** density of 1's"*
**[DS p.3]**. Most PDM decimators assume the opposite. If your captured audio is phase-inverted
relative to a second microphone, this is why.

**2.2 — The clock window is 1.0 – 3.25 MHz, and both ends bite.**
Below **1 MHz** the part is not merely out of spec, it *changes state*: the state diagram
**[DS p.4]** has exactly three states — `Powered Down` (V<sub>DD</sub> off), `Sleep`
(V<sub>DD</sub> on, f<sub>clock</sub> < 1 kHz) and `Active` (V<sub>DD</sub> on,
f<sub>clock</sub> > 1 MHz). The band **1 kHz … 1 MHz is undefined by the datasheet** — neither
transition condition is satisfied. Do not park the clock there; either run ≥ 1 MHz or stop it
below 1 kHz.
Above **3.25 MHz** you are past the specified maximum. An ESP32-S3 PDM RX at 16 kHz with the
default 64× oversampling lands near 1.0 MHz — i.e. at the **bottom** edge. Prefer a configuration
that puts f<sub>clock</sub> comfortably inside the band; the datasheet's own characterisation
point is 2.4 MHz.

**2.3 — Sleep is entered by stopping the clock, not by a pin.** There is no enable, shutdown or
reset input. `Fall-asleep` and `Wake-up` are both **≤ 10 ms** **[DS p.3]**, so gating the clock
is a real power lever (600 µA → 25 µA typ.) but it is *not* instantaneous. Budget 10 ms before
the first sample after restarting the clock is trustworthy.

**2.4 — `SELECT` chooses the clock edge, and the default is the falling edge.** **[DS p.7]**

| `SELECT` | Label | Drives data after | High-Z after |
|---|---|---|---|
| High | `Data_H` | **rising** clock edge | falling clock edge |
| **Low (default)** | `Data_L` | **falling** clock edge | rising clock edge |

Two microphones share one data line by taking opposite `SELECT` levels; each tri-states while the
other drives. A single microphone still obeys the rule — **the host must sample on the correct
edge or it reads the High-Z half of the cycle.**

## 3. As fitted on the Cardputer v1.0 / v1.1 — read from the schematic

⚠ **Correction to the previous version of this record: the designator is `U5`, not `M1`.**
On `Sch_M5Cardputer.pdf` (SHA-256 `6016c1fe…`), **`M1` is the `STAMP-S3-DIP-1.27` module
footprint**. The microphone is **`U5`**, value `SPM1423HM4H-B` **[SCH-V]**.

| `U5` pin | Name | Net | Note |
|---:|---|---|---|
| 1 | `GND` | `GND` | |
| 2 | **`SELECT`** | **`GND`** | ⚠ **tied hard to ground** — see below |
| 3 | `GND` | `GND` | |
| 4 | `CLK` | `G43` **via `R17` 33 Ω** | shared with the speaker `LRCLK` |
| 5 | `DAT` | `G46` **via `R16` 33 Ω** | |
| 6 | `3V3` | `+3.3 V` | |

All six rows **[SCH-V]**, read from a 400 dpi render of sheet 1 of the mainboard schematic.

**What `SELECT = GND` means in practice.** The part is in its **default `Data_L`** configuration,
so it **drives `DAT` after the falling `CLK` edge and tri-states after the rising edge**
**[DS p.7]**. Configure the host's PDM receiver for the falling-edge / "left" slot accordingly.
It also means **the channel cannot be changed in firmware** — there is no GPIO on `SELECT`.

**The 33 Ω series resistors (`R16`, `R17`) were not previously recorded here.** They are
edge-rate damping on a clock running at ≥ 1 MHz across a small board. They also sit between the
pin and the 100 pF C<sub>LOAD</sub> limit, so the *pin* sees less than the net capacitance.

**Supply headroom.** `+3.3 V` against a **3.6 V absolute recommended maximum** is 0.3 V of
margin, and the datasheet's own characterisation is at 1.8 V. All the sensitivity, SNR and THD
figures in §1 are therefore **not** measured at this board's operating point. Treat them as
indicative, not as predictions for this product. *(inferred — no measurement of the fitted part
exists in this repository.)*

## 4. Pinout as used, and the firmware side

| Signal | Cardputer v1.0 / v1.1 |
|---|---|
| `DAT` | **G46** |
| `CLK` | **G43** |
| `VCC` | 3.3 V |
| `GND` | GND |

Straight from the M5Stack PinMap table ("SPM1423 MIC") **[DOC]**, and corroborated by
[`M5Unified`](https://github.com/m5stack/M5Unified/blob/8530f5377d782e4a25a6c482de2e71c3f75ca8eb/src/M5Unified.cpp#L2664-L2670)
**[SRC]**:

```cpp
case board_t::board_M5Cardputer:
  if (cfg.internal_mic) { mic_cfg.pin_data_in = GPIO_NUM_46;
                          mic_cfg.pin_ws      = GPIO_NUM_43; }
  break;
```

⚠ **Note what is absent: `pin_bck` is not set.** A PDM microphone needs a clock and a data line,
not a full I²S frame. The ADV's row in the same table *does* set `pin_bck = GPIO_NUM_41`, because
the ADV's microphone path goes through an I²S codec instead. That one missing line is a compact
way to see the generational difference.

**Driver-versus-document note.** M5Unified sets no explicit PDM clock frequency for this board in
the lines above; the rate follows from the sample rate the application requests. Nothing in the
driver clamps f<sub>clock</sub> to the **1.0 – 3.25 MHz** window of §2.2, so **an application that
selects a low sample rate can drive this part out of specification without any warning**. This is
a *latent* trap rather than an observed defect — no failure has been reported and none was
reproduced here. *(not-tested.)*

## Used By

### M5Stack Cardputer v1.0 (K132) and v1.1 (K132-V11)

[`devices/m5stack/cardputer-v1.0`](../../../devices/m5stack/cardputer-v1.0/README.md) ·
[`devices/m5stack/cardputer-v1.1`](../../../devices/m5stack/cardputer-v1.1/README.md)

Designator **`U5`** on the shared mainboard schematic (SHA-256 `6016c1fe…`), wired as §3.

`CLK` on **G43** is shared with the speaker path's `LRCLK` (the NS4168's `LRCLK` is also G43),
so the microphone clock and the speaker word-select are the same net. That is workable because
M5Unified drives one I²S port and only one direction is active at a time, but it means
**simultaneous full-duplex audio is not available on the v1.x** — a limitation the ADV's codec
removes.

> **Consequence of §2.2 for this shared net.** Because `CLK` *is* the speaker `LRCLK`, the
> microphone sees whatever the speaker path leaves on G43. When the speaker is active,
> `LRCLK` runs at the **sample rate** — tens of kilohertz, i.e. **inside the 1 kHz … 1 MHz band
> the datasheet does not define**. This is the mechanism behind "only one direction at a time"
> and it is a property of the *part*, not merely of the driver. *(inferred from [DS p.3–4] plus
> the shared net; not measured.)*

**Replaced on the Cardputer ADV** by an analog MEMS microphone
([`memsensing/msm381a3729h9bp`](../../memsensing/msm381a3729h9bp/README.md)) feeding the
[ES8311](../../everest-semiconductor/es8311/README.md) codec's ADC. That change is what makes the
ADV's 3.5 mm jack and its recording path possible.

## Mechanical and assembly

Bottom-port package, **4.284 × 3.324 mm body**, 6 pads on a 1.651 / 3.302 mm grid, 0.914 mm pad
pitch (×5), 2.337 mm pad span **[DS p.5]**; recommended land pattern **[DS p.6]**; tape-and-reel
12.0 ±0.3 mm tape, 8.00 mm pitch, laser-marked with `SPM1423HM4H-B` **[DS p.8]**.

**Handling constraints that will destroy the part** **[DS p.9]** — these are the reason a
rework attempt on a Cardputer usually ends with a dead microphone:

- **Do not board-wash after reflow.** No cleaning agents, no ultrasonic processing.
- **Do not brush the board** after reflow, with or without solvent.
- **Do not pull a vacuum over the port hole**, and do not apply air pressure into it.
- **Do not insert anything into the port hole**, ever.
- **MSL class 2a**; 12-month shelf life in the unopened factory bag at ≤ 30 °C / 70 % R.H.
- **No more than 3 reflow cycles.**

Reliability spec caveat **[DS p.10]**: after the listed environmental tests, sensitivity *"shall
not deviate more than 3 dB from its initial value"* — i.e. ±3 dB of drift is a **pass**, not a
fault.

**Part marking** **[DS p.2]**: eight characters, `S` + 7 job-identification digits.
`S` = Knowles SiSonic production, `E` = Knowles engineering sample. **There is no part number on
the package**, so a board photograph can confirm the *family* and the *production status* but
**cannot confirm `SPM1423HM4H-B` specifically**. That gap is therefore not closeable by
photography.

## Artifacts

| File | Bytes | SHA-256 | Notes |
|---|---:|---|---|
| [`artifacts/spm1423hm4h-b-datasheet-rev-a-m5stack-mirror.pdf`](artifacts/spm1423hm4h-b-datasheet-rev-a-m5stack-mirror.pdf) | 1 272 831 | `85ecd7d7a42c7853a77a4dbc903606f7da82cf03abd496b75eb526147e1acbb0` | Rev A, 11 pages, letter. Retrieved **2026-09-04**, filed **2026-09-20** |

Source URL (M5Stack mirror):

```
https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/datasheet/core/SPM1423HM4H-B_datasheet_en.pdf
```

**Renamed on filing** from `SPM1423HM4H-B_datasheet_en.pdf` to the name above, per the repository's
`<part>-<doc>-<rev>-<source>-mirror.pdf` convention. Bytes unchanged — the hash above is the
hash of the original download.

**Disposition** `repository` · **Licence** `unknown` — no licence statement appears in the
document. The final page carries a **liability disclaimer, not a redistribution restriction**:
*"The information contained in this literature is based on our experience to date … It is intended
as a guide for use by persons having technical skill at their own discretion and risk"*
**[DS p.11]**. **Redistribution status** `unknown`.

### ⚠ Provenance: this is an aggregator copy, not a Knowles original

The PDF's own metadata says so:

| Field | Value |
|---|---|
| `Title` | `DATASHEET SEARCH SITE | WWW.ALLDATASHEET.COM` |
| `Author` | `Provided By ALLDATASHEET.COM(FREE DATASHEET DOWNLOAD SITE)` |
| `Creator` | `SolidWorks 2010 SP4.0 (2010164)` |
| `Producer` | `SolidWorks PDF Publisher` |
| `CreationDate` | 2012-02-16 — matches the Rev A release date on p.11 |
| `ModDate` | **2013-11-26** |

So the chain is **Knowles (SolidWorks export, 2012) → ALLDATASHEET (re-wrapped, 2013) → M5Stack's
OSS bucket → here**. The *content* pages are Knowles' own and internally consistent (every page
footer reads "Knowles Acoustics, a division of Knowles Electronics, LLC · Revision: A ·
Release Level: Active · Sheet N of 11"), and the page count matches the stated 11. But **M5Stack
did not mirror this from Knowles**, and neither did we. This matters for
[`vendors/m5stack`](../../../vendors/m5stack/README.md) §5.5's warning about M5Stack's third-party
datasheet mirrors: in this instance the mirror is two hops from the manufacturer.

**Not resolved:** Knowles' own current copy was not located in this pass, so it is unknown whether
Revision A is still current or whether a later revision exists. Rev A is dated **2012** and
marked *Active*; the part is a 2010s-era design and may well be obsolete by now. No Knowles
lifecycle statement was found.

## Substitutes

| Part | Note |
|---|---|
| Any PDM MEMS mic with `CLK`/`DAT`/`VCC`/`GND` | check the **channel-select convention** (§2.4 — which edge is the default?), the **clock band** (§2.2), and the **polarity** (§2.1). These three differ between vendors and all three break audio silently |
| **MSM261D3526H1CPM / MSM261D4030H1CPM** | the PDM parts already documented in this repository — [`memsensing/msm261d3526h1cpm`](../../memsensing/msm261d3526h1cpm/README.md) · [`memsensing/msm261d4030h1cpm`](../../memsensing/msm261d4030h1cpm/README.md) |
| **Analog MEMS mic** | **not a drop-in** — needs a codec with an analog input, which is exactly what the ADV added |

## Gaps

* **Knowles' own copy of the datasheet was not located**; what is held is an ALLDATASHEET
  re-wrap mirrored by M5Stack. Lifecycle status (active / NRND / obsolete) is **unknown**.
* Whether a revision later than **Rev A (2012-02-16)** exists is **unknown**.
* The tables and figures on pages 3, 4, 6, 7 and 10 are **raster images with no text layer**.
  §1, §2.2 and §2.4 were transcribed from renders. They were cross-checked against text-layer
  headings, but a second reader is worth having before anything here is treated as gospel.
* The **reliability table on p.10** (test conditions and durations) was not transcribed — only its
  ±3 dB acceptance criterion.
* **No measurement of the fitted part exists.** Every acoustic figure is the datasheet's, at
  1.8 V, not at the Cardputer's 3.3 V.
* Package marking still not verified against a board photograph — and per §"Mechanical", the
  marking is a job number, so **photography cannot close this gap anyway**.
