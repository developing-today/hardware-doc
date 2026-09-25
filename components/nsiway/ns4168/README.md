# NS4168 — I²S-input class-D audio amplifier

> The speaker amplifier on the **Cardputer v1.0 and v1.1**.
> Record created **2026-09-04**; **datasheet filed and mined 2026-09-20**.
> Sibling already in this repository: [`nsiway/ns4150b`](../ns4150b/README.md), which is the
> **analog**-input part the Cardputer ADV uses instead.
> Document: **《NS4168 用户手册 V0.9》** ("NS4168 User Manual V0.9"), **2015 年 03 月**
> (March 2015), 15 pages, Chinese only. ⚠ **Manufacturer attribution is unresolved — see
> [§6](#6--the-manufacturer-attribution-is-not-supported-by-this-document).**

**Evidence codes.** **[DS §N]** = this user manual, section N · **[SCH-V]** = read from a
400 dpi render of the Cardputer mainboard schematic · **[DOC]** = M5Stack PinMap page ·
**[SRC]** = vendor source code.

## Function

A mono **class-D amplifier with an integrated I²S receiver and DAC**. It takes a digital I²S
stream directly — no separate codec — and drives a speaker. That is what makes it attractive for
a small MCU board: three pins from the host, one part, and you have audio out.

The vendor's own framing **[DS §1]**: in a noisy system the small analog signal sent to a
conventional amplifier gets corrupted, and the MCU's built-in DAC adds its own noise; sending
I²S digitally sidesteps both. It also removes the input coupling capacitors, and *"layout need
not carefully consider amplifier placement and routing"*.

It is **output only**: no ADC, no analog input path, no headphone driver.

## 1. Headline specification

| Property | Value | Evidence |
|---|---|---|
| Input | **I²S** (`BCLK`, `LRCLK`, `SDATA`), 8 kHz – 96 kHz, **automatic sample-rate detection** | **[DS §2]** |
| Output | mono, **bridge-tied load** (`VOP`/`VON`), filterless class-D | **[DS §1, §9.1]** |
| Output power | **2.5 W** at V<sub>DD</sub> = 5 V, R<sub>L</sub> = 4 Ω · **1.2 W** at V<sub>DD</sub> = 3.6 V, 4 Ω | **[DS §6]** |
| Supply range | **3.0 – 5.5 V** (recommended **3 – 5.25 V**) | **[DS §2, §5]** |
| Quiescent current `I`<sub>`DD`</sub> | **13 mA** at 5 V, no load | **[DS §6]** |
| Shutdown leakage `I`<sub>`SD`</sub> | **1 µA** (`V`<sub>`CTRL`</sub> = 0 V) | **[DS §6]** |
| Efficiency | **80 %** at 2.5 W / 4 Ω / 5 V | **[DS §2, §6]** |
| THD+N | **0.2 %** at 1 kHz, 4 Ω, 1.0 W | **[DS §6]** |
| SNR | **85 dB** at 4 Ω, 2.0 W | **[DS §6]** |
| PSRR | **−80 dB** @ 217 Hz · **−72 dB** @ 20 kHz | **[DS §6]** |
| CMRR | **−70 dB** | **[DS §6]** |
| Modulation frequency `f`<sub>`SW`</sub> | **430 kHz** (V<sub>DD</sub> 3 – 5.25 V) — **spread-spectrum PDM** for lower EMI | **[DS §1, §6]** |
| Output offset `V`<sub>`OS`</sub> | 10 mV typ., **40 mV max** | **[DS §6]** |
| Max gain attenuation `A`<sub>`MAX`</sub> | **−10 dB** (the NCN limiter's range) | **[DS §6]** |
| Protection | over-current, over-temperature, under-voltage — **all auto-recovering** | **[DS §2, §9.6]** |
| Package | **eSOP-8**, θ<sub>JC</sub> 20 °C/W, θ<sub>JA</sub> 80 °C/W | **[DS §5, §10]** |
| Operating temperature | **−40 to +85 °C**; junction max **150 °C** | **[DS §5]** |
| ESD | 4000 V | **[DS §5]** |

**Absolute maxima** **[DS §5]**: supply **2.8 – 5.5 V**; `CTRL`, `LRCLK`, `BCLK`, `SDATA` each
**−0.3 V to V<sub>DD</sub>**; soldering **220 °C for ≤ 15 s**.

> ⚠ Note the inputs are clamped to **V<sub>DD</sub>**, not V<sub>DD</sub> + 0.3 V. A host driving
> 3.3 V logic into a part powered from a rail that can sag below 3.3 V is momentarily over the
> absolute maximum. On the Cardputer the host and the amplifier share the same 3.3 V rail
> (§4), so this does not arise — but it would on a 5 V-supplied design driven by 3.3 V logic that
> browns out.

## 2. Pin table

| Pin | Name | Function | **[DS §7.2]** |
|---:|---|---|---|
| 1 | **`CTRL`** | control — channel select, shutdown **and** high-pass-filter programming. See §3 | |
| 2 | `LRCLK` | I²S frame / word-select clock | |
| 3 | `BCLK` | I²S bit clock | |
| 4 | `SDATA` | I²S serial data, two's complement | |
| 5 | `VON` | output, negative | |
| 6 | `VDD` | supply | |
| 7 | `GND` | ground | |
| 8 | `VOP` | output, positive | |

I²S input timing minimums **[DS §9.2.1, table 4]**: `t`<sub>`BIL`</sub> / `t`<sub>`BIH`</sub>
(BCLK low / high width) **40 ns** each; `t`<sub>`LIS`</sub> / `t`<sub>`LIH`</sub> (LRCLK or SDATA
setup / hold to BCLK **rising** edge) **10 ns**; `t`<sub>`SIS`</sub> / `t`<sub>`SIH`</sub> (SDATA
setup / hold to BCLK rising edge) **10 ns**. The part latches on the **rising** BCLK edge, and
`LRCLK` = 1 means **right** channel, `LRCLK` = 0 means **left** **[DS §9.2.1]**.

## 3. ⚠ `CTRL` is a real control interface — this corrects the previous version of this record

**The earlier version of this record said the part had "no control interface: everything is fixed
by hardware". That is wrong.** Pin 1 carries three distinct functions, multiplexed by DC level
and by a one-wire pulse protocol **[DS §9.3]**.

### 3.1 DC level → channel select and shutdown

| `V`<sub>`CTRL`</sub> | Effect | **[DS §6, §9.3.1]** |
|---|---|---|
| **≤ 0.4 V** | **Shutdown**, low-power. Requires `T`<sub>`OFF`</sub> **> 100 µs** held low | |
| **0.9 – 1.15 V** | **Left** channel | |
| 1.15 – 1.5 V | ⚠ **not specified** — a gap in the table | |
| **1.5 V – V<sub>DD</sub>** | **Right** channel | |

The 1.15 – 1.5 V band is genuinely absent from the datasheet's table. A resistor divider landing
in it has undefined behaviour. **Design for the middle of a defined band, not its edge.**

Selecting *left* requires holding `CTRL` at roughly **1 V**, which on a 3.3 V or 5 V board means a
divider — it is not a logic level. This is why boards that only need one channel usually tie
`CTRL` high and take the right channel.

### 3.2 One-wire pulse train → high-pass filter corner

The input high-pass filter has **11 settings**, selected by counting rising edges on `CTRL` after
a **> 100 µs** low preamble **[DS §9.3.2, table 6]**:

| Rising edges | Filter | −3 dB corner (typ.) |
|---:|---|---:|
| **12** | HPF1 | **20 Hz** |
| **1** | HPF2 | 28 Hz |
| 3 | HPF3 | 40 Hz |
| 4 | HPF4 | 65 Hz |
| 5 | HPF5 | 120 Hz |
| 6 | HPF6 | 240 Hz |
| 7 | HPF7 | 458 Hz |
| 8 | HPF8 | 910 Hz |
| 9 | HPF9 | 1.82 kHz |
| 10 | HPF10 | 3.5 kHz |
| 11 | HPF11 | 6.6 kHz |

Pulse widths: **1 µs < T<sub>HI</sub> < 12 µs** and **1 µs < T<sub>LO</sub> < 12 µs**
**[DS §9.3.2]**.

> ⚠ **The mapping is not monotonic and `2` is unassigned.** `12` pulses gives the *lowest*
> corner (HPF1) while `1` pulse gives the next one up (HPF2), and **no row uses 2 pulses**.
> This was verified against a 150 dpi render of page 11 — it is what the table says, not a text
> extraction artifact. It is most likely a defect in the datasheet, but **nothing here can tell
> you which of the two readings the silicon implements**, and the document is a **V0.9** draft
> whose revision-history table is *blank* (§6). Treat the first two rows as unreliable and use
> 3–11 if you need a predictable corner. *(not-tested — no hardware trial was performed.)*

**The default corner at power-up, with no pulse train applied, is not stated anywhere in the
document.** That is an unresolved gap, and it matters for every board that ties `CTRL` to a fixed
level — including the Cardputer.

### 3.3 The NCN anti-distortion limiter

*"防失真 (NCN)"* **[DS §9.4]**: the amplifier detects output clipping and **automatically reduces
its own gain**, up to `A`<sub>`MAX`</sub> = **−10 dB** **[DS §6]**. Purpose: prevent clipping from
input overload or a sagging battery, and protect the speaker at high output.

Attack **t**<sub>`AT`</sub> = **10 ms**, release **t**<sub>`RL`</sub> = **1.1 s**, both at
V<sub>DD</sub> = 3.6 V **[DS §6]**.

> **This is a behaviour, not a feature you can turn off.** A 1.1 s release means that after a
> single loud transient the amplifier stays quieter for over a second. If loudness on this board
> appears to "pump" or to recover slowly after a bang, this is the mechanism — not the driver, not
> the speaker. There is no register and no pin to disable it.

## 4. As fitted on the Cardputer v1.0 / v1.1 — read from the schematic

Designator **`U6`**, value `NS4168`, on `Sch_M5Cardputer.pdf` (SHA-256 `6016c1fe…`) **[SCH-V]**.

| `U6` pin | Net | Note |
|---:|---|---|
| 1 `CTRL` | **tied to pin 6 `VDD`** | ⚠ see below |
| 2 `LRCLK` | `G43` via **`R23` 33 Ω** | |
| 3 `BCLK` | `G41` via **`R24` 33 Ω** | |
| 4 `SDATA` | `G42` via **`R25` 33 Ω** | |
| 5 `VON` | **`FB2` 1000 Ω/MB ferrite bead** → speaker, with `C19` 1 nF to `DGND` | |
| 6 `VDD` | **`+3.3 V` through `FB1` 120 Ω/MB ferrite bead**; `C15` 100 µF ‖ `C16` 100 nF ‖ `C17` 10 µF | |
| 7 `GND` | `DGND`, tied to `GND` through **`R26` 0 Ω** | single-point star tie |
| 8 `VOP` | **`FB3` 1000 Ω/MB ferrite bead** → speaker, with `C20` 1 nF to `DGND` | |

All rows **[SCH-V]**.

### 4.1 ⚠ `CTRL` is strapped to V<sub>DD</sub> — three consequences

**This closes the gap the previous version of this record recorded as "not determined".**
`CTRL` is not floating and it is not on a GPIO: it is wired directly to the part's own `VDD`
node, i.e. **+3.3 V behind `FB1`**.

Against §3.1, V<sub>CTRL</sub> = V<sub>DD</sub> = 3.3 V lands in the **1.5 V – V<sub>DD</sub>**
band. Therefore:

1. **The Cardputer's speaker plays the *right* I²S channel.** Not the left, and not a mono sum.
   Anything written into the left slot is discarded by the amplifier. M5Unified feeds a mono
   stream so this is invisible in normal use, but it matters the moment you hand the I²S port a
   stereo buffer yourself.
2. **Shutdown is physically unreachable.** Reaching it needs V<sub>CTRL</sub> ≤ 0.4 V for
   > 100 µs; the pin is bonded to the rail. **The amplifier is powered whenever the 3.3 V rail
   is up**, and its 13 mA quiescent draw (at 5 V; less at 3.3 V) cannot be removed in firmware.
   For a battery product that is a real, permanent cost. *(inferred from [SCH-V] + [DS §6];
   the current has not been measured on this board.)*
3. **The high-pass filter cannot be programmed**, because programming requires pulsing `CTRL`
   low. The part sits at whatever its power-on default is — and §3.2 notes the datasheet
   **never states what that default is**. So **the corner frequency of the Cardputer's speaker
   path is unknown and undocumented anywhere.** Given an 8 Ω cavity speaker with essentially no
   bass, this is unlikely to be audible, but it is a genuine hole in the record.

### 4.2 The board follows the datasheet's layout advice

**[DS §9.7]** asks for three things, and the schematic does all three **[SCH-V]**:

| Datasheet advice | On the board |
|---|---|
| *"add ferrite beads and capacitors at the output"* to suppress EMI, placed close to the pins | `FB2`/`FB3` 1000 Ω/MB + `C19`/`C20` 1 nF |
| decoupling as close to the supply pin as possible | `C15`/`C16`/`C17` on the `VDD` node |
| *"power and ground preferably star-connected"* | `R26` 0 Ω bridging `DGND` to `GND` |

The supply bypass **deviates slightly**: **[DS §9.5]** specifies *"typically a 100 µF capacitor in
parallel with a 1 µF ceramic"*; the board fits 100 µF + 100 nF + 10 µF. Functionally equivalent or
better, but it is a deviation, and the record should say so rather than imply conformance.

### 4.3 Supply voltage, and what it does to the power claim

The part is fed **3.3 V**. The datasheet's output-power figures are **2.5 W at 5 V / 4 Ω** and
**1.2 W at 3.6 V / 4 Ω** **[DS §6]**; the "Output Power vs Supply Voltage (4 Ω)" curve
**[DS §8]** starts at 3 V and rises to ~2.6 W at 5 V.

**M5Stack's spec table claims "1 W" into the Cardputer's 8 Ω cavity speaker** **[DOC]**.
The datasheet publishes **no 8 Ω figure at all**, and no figure at 3.3 V. Doubling the load
impedance roughly halves the available power at a given rail, and 3.3 V is below the 3.6 V
characterisation point.

> **Conflict, left unresolved per the conflict protocol.** The vendor's 1 W claim is not
> supported by any number in the part's own datasheet, and the two are not directly comparable
> (different load, different rail, unstated THD point). **No arbitration is offered here.** What
> would settle it: a measurement of output voltage across the speaker at the onset of clipping,
> with the rail monitored. That measurement has not been made. *(not-tested.)*

## 5. Pinout as used, and the firmware side

| Signal | Cardputer v1.0 / v1.1 GPIO |
|---|---|
| `BCLK` | **G41** |
| `LRCLK` | **G43** |
| `SDATA` | **G42** |

From the M5Stack PinMap table ("Speaker & IR") **[DOC]** and corroborated by
[`M5Unified`](https://github.com/m5stack/M5Unified/blob/8530f5377d782e4a25a6c482de2e71c3f75ca8eb/src/M5Unified.cpp#L3018-L3031)
**[SRC]**:

```cpp
case board_t::board_M5Cardputer:
case board_t::board_M5CardputerADV:
  if (cfg.internal_spk) {
    spk_cfg.pin_bck = GPIO_NUM_41; spk_cfg.pin_ws = GPIO_NUM_43;
    spk_cfg.pin_data_out = GPIO_NUM_42;
    spk_cfg.magnification = 16; spk_cfg.i2s_port = I2S_NUM_1;
    if (_board == board_t::board_M5CardputerADV) spk_enable_cb = _speaker_enabled_cb_cardputer_adv;
  }
  break;
```

Note the shape of that code: **the same three pins serve both generations**, and the ADV differs
only by installing an enable callback that configures its ES8311. On the v1.x there is no
callback — and now we know why: **there is nothing the firmware *could* configure, because
`CTRL` is strapped to the rail** (§4.1).

`spk_cfg.magnification = 16` is a **software** gain applied by M5Unified before the samples
leave the I²S port. Together with §3.3 this makes the v1.x gain structure worth stating plainly:

```
samples ──► M5Unified ×16 (software) ──► I²S ──► NS4168 fixed gain ──► NCN limiter (0 … −10 dB, auto)
```

There is **no** volume control between the I²S port and the speaker. Raising `magnification`
pushes the amplifier into clipping, at which point the NCN limiter pulls the gain back by up to
10 dB with a **1.1 s release** — so over-driving does not simply get louder, it gets *quieter
for a second afterwards*. *(inferred from [DS §6, §9.4] + [SRC]; not measured.)*

## 6. ⚠ The manufacturer attribution is not supported by this document

This record lives at `components/nsiway/ns4168/` and the component index calls the maker
"NSIWAY". **The filed datasheet does not say that.**

| Where | What it says |
|---|---|
| Cover logo and wordmark **[DS §cover]** | **深圳市永阜康科技有限公司 / SHENZHENSHI YONGFUKANG TECHNOLOGY CO.,LTD** |
| Cover contact block | `TEL:0755-82863877 13242913995` · `E-MAIL:panxia168@126.com` · `http://www.szczkjgs.com` |
| PDF `Title` / `Author` metadata | `DATASHEET SEARCH SITE | WWW.ALLDATASHEET.COM` / `Provided By ALLDATASHEET.COM` |
| Running header on every page | `NS4168` — the part number only |
| Anywhere in the 15 pages | **the string "NSIWAY" / "纳芯威" does not appear** |

Shenzhen Yongfukang is a **component agent/distributor**, and the e-mail and web domain in the
contact block do not match the company name in the logo either. So what is filed here is a
**reseller-branded user manual**, re-wrapped by an aggregator, then mirrored by M5Stack —
**three hops from whoever designed the silicon**.

**Status: unresolved, recorded not repaired.** The directory has **not** been renamed:
several records link to `nsiway/ns4168`, the sibling [`ns4150b`](../ns4150b/README.md) record
rests on the same attribution, and moving a path on the strength of one aggregator copy would
trade a documented uncertainty for an undocumented one. What would settle it: a datasheet served
from the silicon vendor's own domain, or a decapsulation/die photo. Neither was obtained.

This is the same failure mode the component index already flags for
[`chip-wealth-technology/ch13620`](../../chip-wealth-technology/ch13620/README.md) ("manufacturer
recovered from the cover logo; the name appears nowhere in the document text") — except here the
cover logo points at a **distributor**, so it does not resolve the question at all.

### Other metadata worth knowing

- **Version V0.9** — a pre-1.0 document.
- The **修改历史 ("revision history") table on page 2 is completely empty**: headers
  (日期/版本/作者/修改说明) with **no rows**. There is no recorded change history for this part.
- `Creator: Acrobat PDFMaker 9.0 Word 版` — authored in Microsoft Word.
- `CreationDate` 2015-06-28, `ModDate` **2019-05-13** (the ALLDATASHEET re-wrap).

## Artifacts

| File | Bytes | SHA-256 | Notes |
|---|---:|---|---|
| [`artifacts/ns4168-user-manual-v0.9-cn-m5stack-mirror.pdf`](artifacts/ns4168-user-manual-v0.9-cn-m5stack-mirror.pdf) | 829 468 | `479e75a104f48f31584683e5cd3e0d46843884af9da9137680b57700e6a6aab3` | V0.9, March 2015, 15 pages, A4, **Chinese only**. Retrieved **2026-09-04**, filed **2026-09-20** |

Source URL (M5Stack mirror):

```
https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/datasheet/core/NS4168_CN_datasheet.pdf
```

**Renamed on filing** from `NS4168_CN_datasheet.pdf`; bytes unchanged.

**Disposition** `repository` · **Licence** `unknown` — no licence or copyright statement appears
anywhere in the document · **Redistribution status** `unknown`.

**Multi-language policy** (skill step 18.3): **no English version was located**, so this Chinese
document is the **primary source** for this part and belongs in the repository on its own merits.
The same pattern was recorded for the RX8130CE during the PaperMono pass — M5Stack mirrors some
datasheets only in Chinese. Every figure in §1–§3 above was translated here, so a
non-Chinese-reading user does not need to open it.

**Text-layer validation.** The extracted text was checked against three headings that also
render visually (`NS4168 用户手册 V0.9`, `表6 一线脉冲波形与高通滤波器对应关系`, `图13 eSOP-8 封装尺寸图`)
and against the page-11 render used for §3.2. Tables 1–6 all extract as text; figures 1–13 are
vector/raster graphics with no text.

## Substitutes

| Part | Note |
|---|---|
| **NS4150 / NS4150B** | **analog** input — not a drop-in for an I²S source. This is the ADV's part. [`nsiway/ns4150b`](../ns4150b/README.md) |
| MAX98357A | the common Western equivalent: I²S in, class-D out. ⚠ **Its `SD_MODE` pin is a channel-select/shutdown pin with a *different* threshold scheme** from §3.1, and it has no equivalent of the NCN limiter or the one-wire HPF programming. A footprint-level substitution will change the channel and the dynamics |
| Any I²S class-D amp | check: the I²S format (this part expects standard Philips I²S, latching on the **rising** BCLK edge), the channel-select convention, and whether the part has an auto-limiter that will change the perceived loudness |

## Gaps

* **Manufacturer unresolved** — §6. The directory name asserts more than the evidence supports.
* **No English datasheet located.**
* **The power-on default high-pass corner is not stated in the document**, and on the Cardputer it
  cannot be changed (§4.1), so the Cardputer's actual speaker high-pass corner is **unknown**.
* **The 1-pulse / 12-pulse rows of table 6 are internally odd** and `2` is unassigned (§3.2).
  Not testable without hardware.
* **M5Stack's "1 W into 8 Ω" claim is unsupported by the datasheet** and is recorded as a conflict
  (§4.3), not resolved.
* Efficiency, THD and power **at 3.3 V into 8 Ω** — the board's actual operating point — are
  published by nobody. Every number in §1 is at 4 Ω and 3.6 V or 5 V.
* No measurement of any kind has been made on the fitted part.
