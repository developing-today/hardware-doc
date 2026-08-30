# SGMicro SGM2036-3.3 — the low-noise audio rail

- **Category:** 300 mA low-noise, low-dropout linear regulator (RF LDO)
- **Reference designator on this board:** `U20`
- **Marking in the schematic BOM field:** `SGM2036-3.3YN5G/TR` — **SOT-23-5**, fixed 3.3 V, tape-and-reel
- **Owning MCU:** **none.** Unconditionally enabled in hardware
- **Research status:** fully established. The manufacturer datasheet was successfully retrieved on 2026-08-23 after previously failing — see §8
- **Retrieved:** 2026-08-21; datasheet obtained and schematic re-read pin-by-pin 2026-08-23

## Evidence labelling

**[SCH]** schematic PNG · **[SRC]** vendor demo source · **[DOC]** manufacturer datasheet · **[WEB]** vendor page/wiki · **[INF]** inference, reasoning given

---

## 1. Identity — the ordering string decodes exactly

The schematic BOM field reads `SGM2036-3.3YN5G/TR` **[SCH sheet 5 `5_DAC.png`]**. That string appears verbatim in SGMicro's ordering table **[DOC, rev. B.2, November 2021]**:

| Model | Package | Temperature range | **Ordering number** | Package marking | Packing |
|---|---|---|---|---|---|
| SGM2036-3.3 | **SOT-23-5** | −40 °C to +85 °C | **`SGM2036-3.3YN5G/TR`** | `SPHXX` (see note) | Tape and reel, 3000 |

So every element is confirmed:

| Fragment | Meaning |
|---|---|
| `SGM2036` | The part family |
| `-3.3` | **Fixed 3.3 V output** — not the ADJ version |
| `Y` | SGMicro's green/RoHS designator |
| `N5` | **SOT-23-5** package |
| `G` | Green |
| `/TR` | Tape and reel, 3000 pieces |

This matters for one specific reason: **the SOT-23-5 package's pin 4 is `BP` on the fixed-voltage version and `FB` on the adjustable version.** Since this is the fixed `-3.3` part, **pin 4 is `BP`, a reference-noise bypass pin, and the capacitor on it is a noise-reduction capacitor, not part of a feedback divider.** Reading it as feedback would be a substantive error. §2 confirms the board wires it as `BP`.

Note also the datasheet is titled *"300 mA, Low Power and Low Dropout **RF** Linear Regulator"* — this part is marketed for noise-sensitive RF and analogue rails, which is exactly the job it is doing here.

## 2. Exact wiring **[SCH sheet 5]**

| Pin | Name | Connected to | Detail |
|---:|---|---|---|
| 1 | `IN` | **5 V**, via `L8` `BLM18AG102SN1D` ferrite bead | `C62` **1 µF** input capacitor after the bead |
| 2 | `GND` | GND | |
| 3 | `EN` | **tied to `IN`** | **Always on.** No processor can disable it |
| 4 | **`BP`** | `C101` **10 nF** to GND | Reference-noise bypass. **This is what makes it low-noise** |
| 5 | `OUT` | **`3V3_DAC`** | `C66` **1 µF** output capacitor |

Two things to notice immediately:

**It runs from 5 V, not from the 3.3 V buck rail.** This is a separate branch off the 5 V input, not a post-regulator cascaded behind the [TLV62569DBVT](../../texas-instruments/tlv62569dbvt/README.md). That is deliberate: cascading would have imported the buck's switching ripple and load-transient response into the audio rail, which is the exact thing this LDO exists to avoid. The cost is efficiency — see §4.

**There is a ferrite bead on the input.** `L8` is a `BLM18AG102SN1D` (Murata BLM18A series, 0603, 1000 Ω at 100 MHz) **[SCH]**. Combined with `C62` it forms an LC filter against high-frequency conducted noise arriving on the 5 V rail — most obviously the buck's own 1.5 MHz switching and the USB port's noise. **[INF]** This is a considered design; a plain LDO with no input bead would have been the lazy choice.

### 2.1 What is on the `3V3_DAC` rail

Only two devices **[SCH sheet 5]**:

| Device | Designator | Pin |
|---|---|---|
| **PCM5100A** audio DAC | `U12` | `DVDD` (pin 20) and `A3V3` → `CPVDD` (pin 1) / `AVDD` (pin 8) |
| **CH445P** audio mux | `U18` | `VCC` (pin 14), with `C100` 100 nF |

Nothing else. In particular the microphone, the display and the radios are **not** on this rail — they are on the buck's `3V3`. See [tlv62569dbvt §1.1](../../texas-instruments/tlv62569dbvt/README.md#11-what-is-on-this-rail-sch-all-five-sheets).

### 2.2 `EN` tied to `IN` — and why the datasheet demands it

SGMicro's pin description is explicit: *"This pin must be pulled high by an external resistor connected to IN pin if EN pin is not used."* **[DOC]** The board ties `EN` directly to `IN` **[SCH]**, which satisfies that requirement (a direct tie is the degenerate case of the pull-up).

Consequences:

- **No software control of the audio rail.** The DAC and mux are powered whenever 5 V is present.
- **The 0.01 µA shutdown current is unreachable.** You always pay the 20 µA quiescent current.
- **The automatic discharge function never fires.** The SGM2036 discharges `VOUT` quickly when disabled **[DOC]** — a nice feature for pop suppression that this board cannot use.
- **Sequencing is fixed.** `3V3_DAC` and `3V3` both come up together, following 5 V. There is no way to bring the DAC up after the mux, or vice versa.

The last point is worth remembering when reasoning about audio pops. Pop/click suppression on this board is entirely the PCM5100A's `XSMT` soft-mute pin's job — and **that pin is owned by the ESP32-U4WDH alone**, which is a documented board-wide problem. See [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md).

## 3. Key specifications **[DOC, rev. B.2, November 2021]**

| Parameter | Min | Typ | Max | Unit |
|---|---:|---:|---:|---|
| Input voltage range `VIN` | 1.6 | — | 5.5 | V |
| Output voltage accuracy at `IOUT` = 0.1 mA, +25 °C | −2.5 | — | +2.5 | % |
| **Maximum output current** | **300** | — | — | mA |
| Output current limit `ILIMIT` | 360 | 560 | — | mA |
| Supply pin current `IQ`, no load | — | **20** | 26 | µA |
| Shutdown supply current | — | 0.01 | — | µA |
| **Dropout voltage at 300 mA, 3.0 V ≤ VOUT < 3.6 V** | — | **190** | **250** | mV |
| Thermal shutdown `TSHDN` | — | 140 | — | °C |
| Thermal shutdown hysteresis | — | 15 | — | °C |
| Operating temperature | −40 | — | +85 | °C |
| Junction temperature (abs max) | — | — | +150 | °C |
| **Power dissipation `PD` at TA = +25 °C, SOT-23-5** | — | **390** | — | mW |
| **Package thermal resistance `θJA`, SOT-23-5** | — | **285** | — | °C/W |
| `IN` to GND (abs max) | −0.3 | — | 6 | V |
| `EN` to GND (abs max) | −0.3 | — | 6 | V |
| Output short-circuit duration | — | **Infinite** | — | — |
| ESD HBM / MM | — | 4000 / 400 | — | V |

Recommended operating conditions **[DOC]**:

| | Value | Board fits? |
|---|---|---|
| Input effective capacitance `CIN` | **0.1 µF minimum** | ✅ `C62` = 1 µF |
| Output effective capacitance `COUT` | **0.5 µF to 10 µF** | ✅ `C66` = 1 µF |
| Enable input voltage range | 0 V to 5.5 V | ✅ tied to 5 V |

Note the output capacitor has a specified **upper** bound of 10 µF, not just a lower one. Adding a large bulk capacitor to `3V3_DAC` "for stability" would take it outside the recommended range. Do not.

### 3.1 Output-voltage accuracy in practice

±2.5% on 3.3 V is **3.218 V to 3.383 V**. The PCM5100A's recommended supply is 3.3 V ±10% **[DOC PCM5100A]**, so this is comfortably inside. The tolerance is not a concern; the noise performance is the point of the part.

### 3.2 The dropout number is the one that constrains the input rail

At 300 mA and a 3.3 V output, dropout is **190 mV typ, 250 mV max** **[DOC]**. So the minimum input for regulation is about **3.55 V** at full load. The board feeds it from 5 V, so there is ~1.45 V of margin — the LDO will hold regulation through a substantial 5 V sag, which is a real robustness benefit given the unresolved power-path situation ([generic/charger-power-path](../../generic/charger-power-path/README.md)).

At the *actual* load (§4, ~15 mA) dropout is a small fraction of the 300 mA figure, so the margin is even larger.

## 4. Efficiency and thermal — the price of a clean rail

An LDO's efficiency is, to first order, `VOUT / VIN`. Here:

```
η ≈ 3.3 / 5.0 = 66%
```

The other 34% is heat. Dissipation is `(VIN − VOUT) × IOUT = 1.7 V × IOUT`:

| Load | `PD` | Junction rise at `θJA` = 285 °C/W | Comment |
|---:|---:|---:|---|
| 15 mA **(realistic — see below)** | 25.5 mW | **7 °C** | Uneventful |
| 50 mA | 85 mW | 24 °C | Fine |
| 100 mA | 170 mW | 48 °C | Warm |
| 200 mA | 340 mW | 97 °C | **Near the 390 mW package limit** |
| **300 mA (rated max)** | **510 mW** | **145 °C** | **Exceeds `PD` = 390 mW and pushes `TJ` past the 140 °C thermal shutdown** |

**[INF]** — arithmetic ours; `θJA` and `PD` from **[DOC]**.

**Conclusion: at 5 V input and 3.3 V output, this part cannot deliver its rated 300 mA continuously in SOT-23-5.** The thermal ceiling is roughly `390 mW / 1.7 V ≈ 230 mA` at 25 °C ambient, and less inside a sealed enclosure. The datasheet's 300 mA rating assumes a smaller input-to-output differential.

**This is not a problem on this board**, because the actual load is tiny:

| Consumer | Estimated current | Basis |
|---|---:|---|
| PCM5100A, playing | ~10–15 mA | [DOC PCM5100A] |
| PCM5100A, muted | ~5 mA | [DOC] |
| CH445P analog mux | < 1 mA | **[INF]** — no datasheet obtainable, see [wch/ch445p](../../wch/ch445p/README.md). Analogue switches are microamps |
| **Total** | **~15 mA** | |

15 mA out of a thermally-limited ~230 mA is **a 15× margin**. The part is heavily over-specified for the job, which is exactly what you want in a noise-critical rail — it will never be operating anywhere near its limits, and its noise and PSRR figures are best at light load.

Total waste heat on this rail: `1.7 V × 15 mA = 25 mW`. Negligible against the board's total.

## 5. Why an LDO here at all

The board deliberately runs two separate 3.3 V rails **[SCH]**:

| | `3V3` | `3V3_DAC` |
|---|---|---|
| Source | TLV62569DBVT **buck**, 5 V → 3.315 V | **SGM2036-3.3 LDO**, 5 V → 3.3 V |
| Efficiency | ~90–95% | ~66% |
| Capacity | 2 A silicon (thermally ~1.2 A sustained) | 300 mA silicon (thermally ~230 mA) |
| Noise | Switching ripple at 1.5 MHz, variable in Power Save Mode, plus load-transient response | Low, and further reduced by the `BP` capacitor |
| Loads | MCUs, radios, display, backlight, SD, flash, haptics, **microphone** | **PCM5100A and CH445P only** |
| Input filtering | none extra | **ferrite bead `L8` + `C62`** |

The rationale **[INF]**:

1. **A buck's noise is worst exactly where audio cares.** Its 1.5 MHz fundamental is easy to reject, but its response to load steps — a Wi-Fi TX burst, an SD write, a haptic pulse — is a broadband transient with energy reaching down into the audio band, and a DAC's PSRR is not good enough there to hide it.
2. **Power Save Mode makes the switching frequency drop and vary at light load** ([tlv62569dbvt §3.1](../../texas-instruments/tlv62569dbvt/README.md#31-two-behaviours-worth-knowing-about)). Idle is precisely when a listener would notice.
3. **The load is small enough that the efficiency penalty does not matter.** 25 mW of waste heat buys a demonstrably quieter rail.

**The one criticism:** the **microphone is on the buck rail, not this one** **[SCH sheet 4]**. There is spare capacity here — 15 mA used out of ~230 mA available — and moving a ~1 mA PDM microphone onto the clean rail would have cost essentially nothing. See [memsensing/msm261d4030h1cpm §6](../../memsensing/msm261d4030h1cpm/README.md#6-power-and-noise).

## 6. Pitfalls

1. **Pin 4 is `BP`, not `FB`.** §1. Treating `C101` as part of a feedback divider is wrong; it is a reference-noise bypass, and removing it degrades noise and PSRR without changing the output voltage.
2. **`COUT` has an upper limit of 10 µF.** §3. Do not add bulk capacitance.
3. **Do not load this rail.** It exists for audio. §4 and §5. Anything you add here is both a thermal load and a noise source on the one rail that was kept clean.
4. **You cannot power-cycle the DAC.** `EN` is tied high (§2.2). Any pop suppression has to come from `XSMT`, which the S3 does not control.
5. **Do not assume "300 mA" is available.** §4 — the thermal ceiling at 5 V→3.3 V is roughly 230 mA at room temperature, less in an enclosure.
6. **The `BLM18AG102SN1D` bead is part of the design, not decoration.** If you rework this area, put it back. A ferrite bead plus `C62` is what stops the buck's conducted noise reaching the LDO input in the first place; the LDO's own PSRR is finite.
7. **The datasheet URL is not stable.** §8. If you need the PDF again, re-derive the link from SGMicro's product page rather than reusing the archived one.

## 7. Alternatives

| Part | Why you might |
|---|---|
| **SGM2036-3.3** (this) | 300 mA, 20 µA `IQ`, `BP` pin, SOT-23-5, 165–190 mV dropout. Well chosen for the job |
| TI TPS7A20 / TPS7A02 | Comparable ultra-low-noise LDOs with published noise-spectral-density curves — easier to design against if you care about numbers |
| ADI/LT LT3042 | Reference-grade ultra-low-noise. Overkill and expensive for a 15 mA load |
| A larger `COUT` + plain LDO | Cheaper, worse. The `BP` pin is doing the real work |
| No LDO at all, DAC on the buck rail | Saves 25 mW and a part. **Measurably worse audio.** Do not |

The SGM2036 is a sensible, unglamorous choice. There is no obvious improvement to make here.

## 8. Sourcing note — the datasheet URL is unstable

The manufacturer PDF **was retrieved and validated on 2026-08-23**, after failing on 2026-08-21. The method matters, because the stable-looking path does not work:

1. `https://www.sg-micro.com/uploads/soft/20240814/1723624970.pdf` → **HTTP 404** (this is the URL that failed in the earlier sweep)
2. `https://www.sg-micro.com/uploads/soft/SGM2036.pdf` → **HTTP 404**
3. `https://www.sg-micro.com/showproduct/97.html` → **HTTP 404** (the old CMS path)
4. `https://www.sg-micro.com/search?keyword=SGM2036` → **HTTP 404**
5. ✅ `https://www.sg-micro.com/product/SGM2036` → HTTP 200, ~590 KB of Next.js HTML. **Grep the embedded payload** for a URL of the form `https://www.sg-micro.com/rect/assets/<uuid>/SGM2036.pdf?access_token=<token>`
6. ✅ Fetch that URL → HTTP 200, `application/pdf`, 942 554 bytes, `%PDF-1.6`, 21 pages

**The `access_token` is very likely rotated per page render**, so the captured URL may not be re-fetchable. If you need the PDF again, redo steps 5–6. The validated copy is retained locally regardless. Full log in [component-download-failures.txt](../../../component-download-failures.txt).

## 9. Open questions

| Question | Status |
|---|---|
| Measured noise on `3V3_DAC` | **Unknown.** No measurements published, and none taken here |
| Actual PCM5100A + CH445P current draw | **Estimated** (§4), not measured. The CH445P has no obtainable datasheet at all |
| `L8` ferrite bead's exact impedance curve | Part number is known (`BLM18AG102SN1D`); the curve was not retrieved. Murata's BLM18A series is 0603, nominally 1000 Ω at 100 MHz |
| `U20` date code | **Unknown** |

## Manufacturer

**SGMicro** — see the [SGMicro documentation-sourcing guide](../../../vendors/sgmicro/README.md) for this vendor's document portals, URL patterns, part-numbering conventions, distribution channels and known gotchas.

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — `U20`, 5 V → 3.3 V, the `3V3_DAC` audio rail

## Related pages

- [texas-instruments/tlv62569dbvt](../../texas-instruments/tlv62569dbvt/README.md) — the main `3V3` buck rail, and the rail-split rationale
- [texas-instruments/pcm5100a](../../texas-instruments/pcm5100a/README.md) — the principal consumer of this rail
- [wch/ch445p](../../wch/ch445p/README.md) — the other consumer
- [memsensing/msm261d4030h1cpm](../../memsensing/msm261d4030h1cpm/README.md) — the microphone that is *not* on this rail
- [Pinouts and buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md)

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| SGM2036 datasheet, rev. B.2, November 2021 — source of every figure in §1 and §3 | https://www.sg-micro.com/product/SGM2036 (see §8 for the asset URL) | 2026-08-23 | [artifacts/sgm2036-datasheet.pdf](artifacts/sgm2036-datasheet.pdf) |
| SGMicro SGM2036 product page | https://www.sg-micro.com/product/SGM2036 | 2026-08-23 | — |
| Board schematic sheet 5 — the `U20` LDO block, `L8`/`C62`/`C66`/`C101`, and the `3V3_DAC` net | — | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/5_DAC.png` |
| Board schematic sheet 1 — the 5 V rail this LDO taps | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/1_LCD&POWER.png` |
| PCM5100A datasheet (supply requirements and current used in §4) | https://www.ti.com/lit/gpn/PCM5100A | 2026-08-21 | `../../texas-instruments/pcm5100a/artifacts/pcm5100a-datasheet.pdf` |
| TLV62569 datasheet (the buck this rail deliberately avoids) | https://www.ti.com/lit/gpn/TLV62569 | 2026-08-21 | `../../texas-instruments/tlv62569dbvt/artifacts/tlv62569-datasheet.pdf` |
| Retrieval log, including the four dead URLs | — | 2026-08-23 | [component-download-failures.txt](../../../component-download-failures.txt) |
| Waveshare wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-wiki-current.html` |
