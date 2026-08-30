# Power button

- **Category:** device power / reset control
- **Reference designator on this board:** **none.** ⚠ **No button symbol appears in the five published schematic sheets.** What *is* in the schematic is the reset net it most plausibly acts on, and that net's support components
- **Owning MCU:** **probably the ESP32-S3** — via `CHIP_PU`, which is a reset input, not a GPIO
- **Research status:** the control's existence and name come from Waveshare. Its net is **inferred** (§2), not established. Its part, topology, latching behaviour and whether it gates power at all are **unknown**
- **Retrieved:** 2026-08-21; the `CHIP_PU` net and the pull-up bank re-examined, and the inference boundary tightened, 2026-08-23

## Evidence labelling

**[SCH]** schematic PNG · **[DOC]** manufacturer design guideline · **[WEB]** vendor page/wiki · **[INF]** inference, reasoning given

---

## 1. What Waveshare says

The product material identifies a control as the **power button** **[WEB]**.

That is the whole of the vendor's statement. There is no description of press-and-hold behaviour, no indication of whether it is momentary or latching, and no statement of what it actually switches.

## 2. What the schematic offers, and the limits of the inference

### 2.1 The candidate net

Schematic sheet 1 contains a bank of 10 kΩ pull-ups to 3V3 **[SCH]**:

| Resistor | Net | Also has |
|---|---|---|
| **`R57`** | **`CHIP_PU`** | `C8` **1 µF** to ground, on sheet 2 |
| `R58` | `GPIO0` | — (this is the [BOOT button](../esp32-s3-boot-button/README.md) net) |
| `R59`, `R60` | `EC1_B`, `EC1_A` | knob 1 |
| `R55`, `R56` | `EC2_A`, `EC2_B` | knob 2 |

`CHIP_PU` is the ESP32-S3's active-high chip-enable / reset input. A 10 kΩ pull-up plus a 1 µF capacitor is **exactly** Espressif's recommended reset network **[DOC, ESP32-S3 hardware design guidelines]**, giving a `10 kΩ × 1 µF = 10 ms` RC delay on release.

**[INF]** A momentary switch from `CHIP_PU` to ground is the standard way to implement a reset or "power" button in this arrangement, and the pull-up plus capacitor is precisely the other half of that circuit. **This is the most plausible reading, and `CHIP_PU` is the only net in the published schematic that fits the description at all.**

### 2.2 Why this is inference and not evidence

The switch itself is not drawn. And there is a real alternative.

**[INF]** On a battery-powered device a "power button" often does something quite different from resetting the MCU — it gates power at the source: a latching load switch, a soft-latch around the charger, or a `KEY`/`ONOFF` pin on an integrated power-management IC. **This board has exactly such an unidentified block**: the charger and power-path function is entirely absent from the published sheets ([generic/charger-power-path](../charger-power-path/README.md)), and several very common integrated charger-plus-boost parts — the IP5306 family, for instance — include a button input that switches the output rail on and off.

So there are two credible readings, and the published material does not distinguish them:

| Reading | What the button does | Fits the evidence? |
|---|---|---|
| **A: reset button** — momentary to `CHIP_PU` | Resets the ESP32-S3. **Powers nothing down**; the ESP32-U4WDH, the display and every rail stay live | The `R57`/`C8` network fits perfectly. But "power button" is a strange name for a reset |
| **B: true power control** — into the missing power-management block | Latches the 5 V rail on and off | Explains the *name*. Nothing in the published sheets contradicts it, because that block is not published |

**[INF]** The name argues for B; the only visible circuitry argues for A. **We do not resolve this.** It is entirely possible that both exist as separate controls, or that one button does A on a short press and B on a long press via a power-management IC.

**Do not document either reading as established.** §4 says how to find out.

### 2.3 What reading A would mean, if it is right

If the button is a momentary `CHIP_PU`-to-ground switch:

- It **resets the ESP32-S3 only.** The ESP32-U4WDH's `EN` is a separate net — `ESP32_EN`, with `R54` 10 kΩ and `C22` 1 µF, driven by the USB-UART bridge's `RTS#` **[SCH sheet 3]** — and is **not** connected to `CHIP_PU`.
- **It would save no power.** The U4WDH would keep drawing its ~50 mA, the backlight would keep drawing whatever it draws, and both regulators' `EN` pins are hard-tied ([tlv62569dbvt §2.1](../../texas-instruments/tlv62569dbvt/README.md#21-en-tied-high--consequences), [sgm2036-3.3 §2.2](../../sgmicro/sgm2036-3.3/README.md#22-en-tied-to-in--and-why-the-datasheet-demands-it)).
- Combined with the [BOOT button](../esp32-s3-boot-button/README.md), it would give the standard EN+BOOT manual download-mode sequence — a real practical benefit regardless of what the button is called.

## 3. What is unknown

| Unknown | Note |
|---|---|
| **Which net it acts on** | §2.2. The central question |
| **Momentary or latching** | Unknown |
| **Whether long-press behaviour exists** | Unknown. A power-management IC would typically implement one |
| **Whether it can actually power the board down** | Unknown, and doubtful under reading A |
| Button part number, type, contact rating, cycle life | **Unknown** — no symbol, no BOM string |
| Debounce components | **None drawn** beyond `C8`, which is a reset-timing capacitor — though it would incidentally debounce a reset button very well |
| Physical placement and accessibility | **Unknown.** On a sealed metal knob body this matters |
| **Whether firmware can read it** | **No.** No signal from any button reaches a GPIO on either MCU **[SCH]** |

That last row deserves emphasis: **you cannot implement "long-press to enter settings", or any other software behaviour, on this button.** It is not wired to a readable pin under either reading. If you need a software-readable button, use the touchscreen or a knob.

## 4. How to find out

In increasing order of effort. Any one of these settles §2.2.

1. **Press it and watch the serial console.** If the ESP32-S3 reboots and prints its boot banner, it is reading A (or at least includes a reset). If the device goes dark and the ESP32-U4WDH also stops responding, it is reading B.
2. **Press it and check whether the other MCU survives.** Connect in the U4WDH's USB orientation and watch whether *its* port drops. Under reading A it should not.
3. **Continuity-check the button** to `CHIP_PU`, to ground, and to the battery/charger area.
4. **Measure current draw** immediately before and after a press. Under reading A it is essentially unchanged; under reading B it collapses.
5. **Photograph the board** and trace what the button connects to.

**Experiment 1 takes ten seconds and resolves most of the ambiguity.** It has not been performed here because no physical board was available for this research.

## 5. Pitfalls

1. **Do not assume it powers the board off.** §2.2, §2.3. Under the reading best supported by the visible schematic it is a reset and saves nothing.
2. **Firmware cannot read it.** §3. Do not design a UI around it.
3. **It resets the S3 only, if reading A is right.** The secondary MCU is on a separate reset net **[SCH]**.
4. **Do not confuse it with the BOOT button.** Different net, different purpose. See [generic/esp32-s3-boot-button](../esp32-s3-boot-button/README.md).
5. **If you want to reduce power draw, the levers are firmware, not this button** — sleep the ESP32-U4WDH and blank the backlight. See [generic/lipo-102035 §5](../lipo-102035/README.md#5-battery-life-estimation-for-this-board).
6. **A press during flashing will interrupt it** under reading A.

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md)

## Related pages

- [generic/esp32-s3-boot-button](../esp32-s3-boot-button/README.md) — the other button, acting on GPIO0
- [generic/charger-power-path](../charger-power-path/README.md) — the missing block that reading B would live in
- [texas-instruments/tlv62569dbvt](../../texas-instruments/tlv62569dbvt/README.md) — why no rail can be switched off in software
- [generic/lipo-102035](../lipo-102035/README.md) — what actually reduces power draw
- [Pinouts and buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md)
- [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md)

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Waveshare product page — the "power button" identification | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/source-snapshots/waveshare-product-31623.html` |
| Waveshare wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-wiki-current.html` |
| Board schematic sheet 1 — the pull-up bank, `R57` on `CHIP_PU` | — | 2026-08-21 | `.../artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/1_LCD&POWER.png` |
| Board schematic sheet 2 — `CHIP_PU` with `C8` 1 µF | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/2_ESP32S3-R8.png` |
| Board schematic sheet 3 — `ESP32_EN` (`R54`/`C22`), the *separate* reset net for the secondary MCU | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/3_ESP32-CHIP.png` |
| ESP32-S3 Hardware Design Guidelines — the recommended `CHIP_PU` 10 kΩ + 1 µF reset network | https://www.espressif.com/sites/default/files/documentation/esp32-s3_hardware_design_guidelines_en.pdf | 2026-08-21 | `../../espressif/esp32-s3r8/artifacts/esp32-s3-hardware-design-guidelines.pdf` |
