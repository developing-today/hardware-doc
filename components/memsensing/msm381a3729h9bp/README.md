# MEMSensing MSM381A3729H9BP — analog MEMS microphone

> Marking read from the M5Stack Cardputer ADV schematic (sheet 3, designator **U8**):
> `MSM381A3729H9BPC` in the value field. Recorded here as **`MSM381A3729H9BP`**, the part
> family, with the trailing character treated as a packaging/grade suffix — see *Gaps*.
> Record created **2026-09-04**. Sibling records already in this repository:
> [`msm261d3526h1cpm`](../msm261d3526h1cpm/README.md), [`msm261d4030h1cpm`](../msm261d4030h1cpm/README.md).

## Function

A bottom- or top-port **analog output** MEMS microphone: a differential (or single-ended) analog
audio signal, to be amplified and digitised by an external codec ADC. Unlike the MSM261 series
already documented here, and unlike the **SPM1423** used on the earlier Cardputers, this part is
**not PDM** — it produces analog audio and therefore requires a codec with an analog microphone
input.

That distinction is the whole reason the Cardputer ADV changed both the microphone *and* the
audio chain at the same time.

## Key capabilities

| Property | Value | Evidence |
|---|---|---|
| Output | **analog** | schematic: `OUT` (pin 4) → `MIC_P` / `MIC_N` into the ES8311's `MIC1P`/`MIC1N` |
| SNR | **65 dB** | M5Stack Cardputer ADV specification table |
| Supply | analog `AVDD` domain, decoupled by C32 1 µF and C33 10 µF | schematic |
| Package | 4-pad MEMS package | schematic symbol: `VDD` (1), `GND` (2), `GND` (3), `OUT` (4) |
| Sensitivity, frequency response, AOP | **not established** | no datasheet retrieved |

## Pinout as drawn

| Pin | Name | Net on the Cardputer ADV |
|---|---|---|
| 1 | `VDD` | `AVDD` (analog 3.3 V, via R24 33 Ω 1 %) |
| 2 | `GND` | `AGND` |
| 3 | `GND` | `AGND` |
| 4 | `OUT` | `MIC_P` → ES8311 pin 18 `MIC1P/DMIC_SDA` |

`MIC_N` returns to the ES8311's pin 17 `MIC1N`, with R41 100 Ω 1 % and C31 1 µF in the network —
so the codec sees a pseudo-differential input.

## Used By

### M5Stack Cardputer ADV (K132-Adv) — [`devices/m5stack/cardputer-adv`](../../../devices/m5stack/cardputer-adv/README.md)

Designator **U8**, on schematic sheet 3, in the analog audio block beside the ES8311.

The microphone has **no direct connection to the SoC**. Its output goes into the
[ES8311](../../everest-semiconductor/es8311/README.md) codec's `MIC1P`/`MIC1N` inputs; the codec
digitises it and returns I²S on `ASDOUT` → **G46**. So from firmware's point of view there is no
"microphone" — there is a codec ADC, configured by
[`M5Unified`'s `_microphone_enabled_cb_cardputer_adv`](../../../devices/m5stack/cardputer-adv/features/audio.md):

```c
2, 0x0E, 0x02,  // SYSTEM: enable analog PGA, enable ADC modulator
2, 0x14, 0x10,  // ADC_REG14: select Mic1p-Mic1n, PGA gain MINIMUM
2, 0x17, 0xBF,  // ADC_REG17: ADC volume 0 dB
2, 0x1C, 0x6A,  // ADC_REG1C: EQ bypass, DC-offset cancellation
```

Note `0x14 = 0x10` selects the **differential Mic1p–Mic1n** path at **minimum PGA gain**. If the
recorded level is too low on this board, that constant is where to look first — and the vendor
never exposes it.

⚠ **Cross-subsystem hazard.** The microphone's *disable* sequence in M5Unified writes
`0x00 = 0x00` (**CSM power down**) to the shared codec, which also silences the speaker. Full
analysis: [`cardputer-adv/features/audio.md` §6.2](../../../devices/m5stack/cardputer-adv/features/audio.md).

**Predecessor on the same product line:** Cardputer v1.0 and v1.1 use a **Knowles SPM1423**
PDM microphone wired straight to the SoC (`DAT` → G46, `CLK` → G43) with no codec.
See [`knowles/spm1423hm4h-b`](../../knowles/spm1423hm4h-b/README.md).

## Substitutes

| Part | Note |
|---|---|
| Any analog MEMS mic with the same 4-pad footprint | the surrounding network (R39, R41, C31, C32) sets the bias and filtering; check sensitivity before swapping |
| **PDM** MEMS mic (SPM1423, MSM261D…) | **not a drop-in** — a PDM part needs a clock and a digital receiver, not an analog codec input |
| MSM261D3526H1CPM / MSM261D4030H1CPM | the PDM siblings already documented in this repository; different interface entirely |

## Gaps

* **No datasheet.** MEMSensing (深圳市敏芯微电子 / MEMSensing Microsystems, Suzhou) does not
  publish this part number through a search-indexable route that this pass located, and M5Stack
  does **not** link a datasheet for it on the Cardputer ADV page — the page links ES8311,
  NS4150B, BMI270, ST7789V2 and ESP32-S3, but not the microphone.
* Sensitivity (dBV/Pa), frequency response, acoustic overload point, directionality and port
  orientation are all **unknown**.
* The trailing `C` in the schematic string `MSM381A3729H9BPC` is **unexplained**. It could be a
  package/grade suffix or an artefact of the schematic's value field. Recorded as read; the
  directory is named for the unambiguous part of the string.
* No board photograph was obtained, so the **top marking has not been checked** against the
  schematic value.
