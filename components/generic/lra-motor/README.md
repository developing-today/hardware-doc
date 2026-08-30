# LRA haptic actuator (unidentified)

- **Category:** linear resonant actuator (LRA), the vibration motor
- **Reference on this board:** no reference designator. It appears in the schematic only as the two nets `LRA_P` / `LRA_N` and the two solder pads `PP2` / `PP1`
- **Owning MCU:** **ESP32-S3**, indirectly — the S3 talks I2C to the DRV2605L, which drives the actuator
- **Research status:** ⚠ **The part is not identified and cannot be identified from published material.** What is established is the interface, the constraints the driver imposes, and how to measure the parameters yourself
- **Retrieved:** 2026-08-21; schematic re-read and driver constraints cross-checked 2026-08-23

## Evidence labelling

**[SCH]** schematic PNG · **[SRC]** vendor demo source · **[DOC]** manufacturer datasheet · **[WEB]** vendor page/wiki · **[INF]** inference, reasoning given

---

## 1. What is actually known

| Fact | Evidence |
|---|---|
| The actuator is a two-terminal device wired to `LRA_P` and `LRA_N` | **[SCH sheet 5 `5_DAC.png`]** |
| Those nets are the `OUT+` (pin 7) and `OUT−` (pin 9) of the DRV2605L `U13` | **[SCH sheet 5]** |
| The connection is via two pads named `PP1` (on `LRA_N`) and `PP2` (on `LRA_P`) — i.e. it is soldered/wired, not a connector with a part number | **[SCH sheet 5]** |
| Waveshare's marketing calls it an "LRA motor" / describes vibration feedback | **[WEB]** |
| The DRV2605L is the driver, meaning the actuator must be one the DRV2605L can drive | **[SCH]** |

That is the complete list. **Everything else is unknown**, including:

- Manufacturer and model number
- **Resonance frequency `f0`** — the single most important parameter
- Rated voltage (RMS)
- Impedance / DC resistance
- Rated acceleration (G), stroke, mass
- Package type (coin/"Z-axis" vs bar/"X-axis")
- Mounting method inside the knob assembly

There is **no BOM, no assembly drawing, no mechanical CAD and no BOM line item** in the published archive **[SCH — the archive is five raster PNGs only]**. No amount of further web research fixes this; it requires either a Waveshare BOM release or physical disassembly.

**Do not guess a part number.** The temptation is to name a common part (Jinlong G0832022, Vybronics VLV101040A, and so on) because they are the usual suspects in this size class. Those are guesses, they would propagate into somebody's calibration constants, and a wrong `RATED_VOLTAGE` can over-drive a real actuator.

## 2. LRA versus ERM — why the distinction matters here

This board fits an **LRA**, and the difference from an ERM changes both the driving strategy and the feel.

| | **LRA** (Linear Resonant Actuator) | **ERM** (Eccentric Rotating Mass) |
|---|---|---|
| Mechanism | A mass on a spring, driven by a voice coil along one axis | A DC motor with an off-centre weight |
| Drive signal | **AC at the resonance frequency `f0`** | DC voltage; amplitude sets speed |
| Frequency | Fixed by mechanics, typically 170–235 Hz. **Cannot be changed** | Varies with amplitude — you cannot set frequency and strength independently |
| Start / stop time | ~5–20 ms with active overdrive/braking | ~50–100 ms; noticeably sluggish |
| Feel | Crisp, "clicky", suited to UI feedback on a knob | Buzzy, muddy, suited to phone ringers |
| Efficiency | Sharply peaked at `f0`; falls off fast either side | Broad |
| Lifetime | No brushes, no rotating contacts — long | Brushes wear |
| Audible noise | Low, if driven at `f0` | Higher |

The consequence of the third row is the crux of this page: **an LRA driven off its resonance produces dramatically less acceleration for the same electrical power, and sounds worse doing it.** A 10 Hz error on a high-Q actuator can cost half the output.

### 2.1 Why calibration matters, concretely

The DRV2605L's "smart loop" does three things that all depend on knowing the actuator:

1. **Auto-resonance tracking.** It senses back-EMF between drive pulses to find `f0` and locks the drive to it — including as `f0` drifts with temperature and mounting. This only runs if `N_ERM_LRA` (register `0x1A` bit 7) is set to LRA **and** `LRA_OPEN_LOOP` (`0x1D` bit 0) is clear.
2. **Automatic overdrive.** It briefly exceeds the rated voltage on attack to get the mass moving in a few milliseconds rather than tens. Bounded by `OD_CLAMP`.
3. **Automatic braking.** It drives the actuator *anti-phase* at the end of an effect to stop the mass dead. Without this an LRA rings on for 50–100 ms and every "click" smears into the next.

All three need `A_CAL_COMP` and `A_CAL_BEMF`, which are produced by the auto-calibration routine against the *specific fitted actuator*. Running with the ROM defaults means running with constants characterised for some other actuator entirely.

**⚠ Neither of Waveshare's two published haptic demos calibrates, and both select an ERM waveform library** — see [DRV2605L §4.3](../../texas-instruments/drv2605l/README.md#43--both-vendor-demos-select-an-erm-library-for-an-lra-actuator) for the evidence and [§5](../../texas-instruments/drv2605l/README.md#5-the-calibration-workflow-for-the-fitted-lra) for the corrected procedure. If your haptics feel weak or mushy on this board, that is almost certainly why, and it is a firmware problem rather than a hardware limitation.

## 3. Constraints the DRV2605L imposes on the fitted (and any replacement) actuator

These are hard bounds from the driver's datasheet **[DOC SLOS854D §6.3]**, so whatever is fitted must satisfy them, and any replacement must too:

| Constraint | Value | Why it binds |
|---|---|---|
| Load impedance | **≥ 8 Ω** at `VDD` = 5.2 V | Below this the output stage over-currents; `OC_DETECT` in register `0x00` will assert |
| LRA frequency range | **125–300 Hz** | The auto-resonance engine's tracking range. Outside it, closed loop will not lock |
| Drive rail | **3.3 V** on this board **[SCH]** | Peak output cannot exceed the supply, so `OD_CLAMP` above ~3.3 V is meaningless. An actuator rated for 2.5–3.0 V RMS will be under-driven here |
| Output type | Differential, `OUT+`/`OUT−` | A single-ended actuator with one side grounded will not work |

The 3.3 V rail is worth dwelling on. Many LRAs are specified at 2.0 V RMS or 1.8 V RMS, which is comfortable here. Some larger ones are rated 3.0 V RMS, which on a 3.3 V rail leaves almost no headroom for the overdrive that makes an LRA feel crisp. **[INF]** Given the board runs everything from 3.3 V, the fitted actuator is most likely a 1.8–2.0 V RMS class part — but this is reasoning about design practice, not evidence, and it must not be used as a calibration input.

## 4. How to identify the parameters you need

Ordered cheapest-first. §1 of the driver page gives the register mechanics; this is the measurement strategy.

### 4.1 Ask the chip for `f0` — no disassembly

The DRV2605L reports the resonance period it locked to, in register `0x22` (`LRA_RESONANCE_PERIOD`), in units of **98.46 µs**:

```
f0 ≈ 1 / (LRA_RESONANCE_PERIOD × 98.46e-6)
```

Procedure: set `N_ERM_LRA` = 1, leave `LRA_OPEN_LOOP` = 0, set `DRIVE_TIME` to a mid-range guess (say `0x13`, i.e. ~2.4 ms half-period ≈ 205 Hz), select library 6, play effect **118** (long buzz), wait ~200 ms for the loop to settle, then read `0x22`. Repeat with the measured value fed back into `DRIVE_TIME` and confirm it is stable.

This is by far the best-value measurement: one register read tells you the parameter that dominates everything else.

### 4.2 Scope the drive

Probe `LRA_P`/`LRA_N` at pads `PP2`/`PP1` **[SCH]** while an effect plays. You get `f0` directly from the commutation rate, and you can see whether the braking pulse at the end of the effect is present (it is a visible anti-phase burst). Absence of a braking pulse is a strong sign the part is running in ERM mode.

### 4.3 Impedance sweep — the definitive route

Lift one actuator terminal from its pad and measure with an LCR meter or a small network analyser:

- **DC resistance** → your check against the 8 Ω floor, and a rough size class indicator
- **Impedance minimum vs frequency** → mechanical `f0`
- **Sharpness of the minimum** → Q, which tells you how badly off-resonance driving will hurt

### 4.4 Rated voltage — the one you cannot measure safely

There is no non-destructive measurement for "rated voltage"; it is a manufacturer's thermal/lifetime specification. **Start conservative at 1.8 V RMS**, verify the actuator does not get warm during a sustained buzz, and only then consider raising it. See the worked `RATED_VOLTAGE` computation in [DRV2605L §5.1](../../texas-instruments/drv2605l/README.md#51-compute-the-register-values-doc-852).

### 4.5 Physical identification

If you open the unit: LRAs in this size class carry either a laser-etched part number on the can or a label on the flying leads. Photograph it, and if you identify it, please record the finding here and in [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md). Note that many Chinese-market LRAs carry only a house code and are only identifiable via the assembler.

## 5. Pitfalls

1. **Assuming the demos are correct.** They are not, for this actuator type. See §2.1.
2. **Using a fixed-frequency PWM.** `IN/TRIG` is grounded on this board **[SCH]**, so the PWM path is unavailable anyway — but even if it were available, driving an LRA at a fixed guessed frequency is the worst of both worlds.
3. **Open-loop LRA mode.** `LRA_OPEN_LOOP` (`0x1D` bit 0) with `OL_LRA_PERIOD` (`0x20`) will make noise without needing calibration, and it is a legitimate fallback if auto-calibration keeps failing. But it gives up resonance tracking, overdrive and braking — i.e. everything that makes an LRA better than an ERM. Treat it as a diagnostic, not a shipping configuration.
4. **Calibrating on the bench, before final assembly.** TI is explicit **[DOC §8.5.6 step 6]** that evaluation "should occur during the final assembly of the device because the auto-calibration process can affect actuator performance and behavior". An LRA's effective `f0` and damping depend on the mass it is bolted to. Calibrate the assembled knob, not a loose actuator.
5. **Burning `OTP_PROGRAM`.** One-time, irreversible, and on a board whose actuator has no datasheet. Cache in NVS instead.
6. **Firing haptics from a UI callback and blocking.** Effects run for tens of milliseconds. See [DRV2605L §7](../../texas-instruments/drv2605l/README.md#7-initialisation-and-integration-gotchas).
7. **Confusing the knob's tactile detents with haptics.** The rotary encoders on this board are mechanical parts with their own physical detents — see [alps-alpine/sscm110100](../../alps-alpine/sscm110100/README.md). The LRA adds *electronic* feedback on top of, not instead of, that mechanical feel. Getting them out of phase (haptic click arriving 40 ms after the mechanical detent) feels worse than no haptics at all, which is another reason braking and short attack times matter.

## 6. Replacement

**Replacement compatibility cannot be established** without identifying the original, because you would be matching an unknown. What you *can* say is what a replacement must satisfy:

| Requirement | Value | Source |
|---|---|---|
| Type | LRA (or an ERM if you accept the change in feel and reconfigure `N_ERM_LRA`) | — |
| Impedance | ≥ 8 Ω | [DOC] |
| `f0` | 125–300 Hz | [DOC] |
| Rated voltage | ≤ ~3.0 V RMS, given the 3.3 V rail | [SCH] + [DOC] |
| Terminals | Two, differential, floating | [SCH] |
| Mechanical | **Unknown** — the existing cavity, orientation and mounting are not documented | — |

And you must re-run auto-calibration after any swap. The mechanical fit is the part that will actually stop you; the electrical envelope is generous.

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — nets `LRA_P`/`LRA_N`, pads `PP2`/`PP1`

## Related pages

- [texas-instruments/drv2605l](../../texas-instruments/drv2605l/README.md) — the driver, the register interface and the full calibration procedure
- [alps-alpine/sscm110100](../../alps-alpine/sscm110100/README.md) — the mechanical detents this actuator is felt alongside
- [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md) — where this unknown is tracked board-wide

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Board schematic archive (five PNGs; sheet 5 carries `LRA_P`/`LRA_N`/`PP1`/`PP2`) | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` |
| Schematic sheet 5, the only sheet showing the actuator nets | — | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/5_DAC.png` |
| DRV2605L datasheet SLOS854D — source of every numeric constraint in §3 | https://www.ti.com/lit/gpn/DRV2605L | 2026-08-21 | `../../texas-instruments/drv2605l/artifacts/drv2605l-datasheet.pdf` |
| Waveshare product page (describes vibration feedback) | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/source-snapshots/waveshare-product-31623.html` |
| Waveshare wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/source-snapshots/waveshare-wiki-current.html` |
