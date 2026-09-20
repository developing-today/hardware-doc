# Knowles SPM1423HM4H-B — PDM MEMS microphone

> The microphone on the **Cardputer v1.0 and v1.1** (and on several other M5Stack products).
> Record created **2026-09-04**. Manufacturer: **Knowles Electronics** (the SPM/SPH prefix is
> Knowles' MEMS microphone family). M5Stack mirrors an English datasheet — see *Artifacts*.

## Function

A **PDM (pulse-density modulation) digital output** MEMS microphone. It takes a clock in and
returns a 1-bit oversampled bitstream — no codec required, and no analog signal on the board.
The host decimates the bitstream in software or in an I²S/PDM peripheral.

This is the cheap, simple way to put a microphone on a microcontroller, and it is what the first
two Cardputers do.

## Key capabilities

| Property | Value | Evidence |
|---|---|---|
| Output | **PDM**, 1-bit | part family; board wiring |
| Interface | `CLK` in, `DAT` out, plus `VCC`/`GND` — **four pins** | M5Stack PinMap |
| Supply | **3.3 V** on the Cardputer | PinMap: `VCC` = 3.3 V |
| Channel select | typically an `L/R` pin or strap; **not brought out on the Cardputer** | schematic |
| Sensitivity, SNR, AOP | in the datasheet; **not transcribed** in this pass | — |

## Pinout as used

| Signal | Cardputer v1.0 / v1.1 |
|---|---|
| `DAT` | **G46** |
| `CLK` | **G43** |
| `VCC` | 3.3 V |
| `GND` | GND |

Straight from the M5Stack PinMap table ("SPM1423 MIC"), and corroborated by
[`M5Unified`](https://github.com/m5stack/M5Unified/blob/8530f5377d782e4a25a6c482de2e71c3f75ca8eb/src/M5Unified.cpp#L2664-L2670):

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

## Used By

### M5Stack Cardputer v1.0 (K132) and v1.1 (K132-V11)

[`devices/m5stack/cardputer-v1.0`](../../../devices/m5stack/cardputer-v1.0/README.md) ·
[`devices/m5stack/cardputer-v1.1`](../../../devices/m5stack/cardputer-v1.1/README.md)

Designator **M1** on the shared mainboard schematic (SHA-256 `6016c1fe…`), value string
`SPM1423HM4H-B`. Wired as above.

`CLK` on **G43** is shared with the speaker path's `LRCLK` (the NS4168's `LRCLK` is also G43),
so the microphone clock and the speaker word-select are the same net. That is workable because
M5Unified drives one I²S port and only one direction is active at a time, but it means
**simultaneous full-duplex audio is not available on the v1.x** — a limitation the ADV's codec
removes.

**Replaced on the Cardputer ADV** by an analog MEMS microphone
([`memsensing/msm381a3729h9bp`](../../memsensing/msm381a3729h9bp/README.md)) feeding the
[ES8311](../../everest-semiconductor/es8311/README.md) codec's ADC. That change is what makes the
ADV's 3.5 mm jack and its recording path possible.

## Artifacts

M5Stack mirrors an English datasheet:

```
https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/datasheet/core/SPM1423HM4H-B_datasheet_en.pdf
```
1 272 831 B, SHA-256 `85ecd7d7a42c7853a77a4dbc903606f7da82cf03abd496b75eb526147e1acbb0`,
retrieved 2026-09-04. **Fetched into scratch, not committed here** — pending a decision, and
because [`vendors/m5stack`](../../../vendors/m5stack/README.md) §5.5 warns that M5Stack's
mirrors of third-party datasheets are not necessarily current. Prefer Knowles' own copy and hash
both; keep the M5Stack mirror labelled as a mirror if it turns out to be the only accessible one.

## Substitutes

| Part | Note |
|---|---|
| Any PDM MEMS mic with `CLK`/`DAT`/`VCC`/`GND` | check the channel-select convention and the clock frequency range |
| **MSM261D3526H1CPM / MSM261D4030H1CPM** | the PDM parts already documented in this repository |
| **Analog MEMS mic** | **not a drop-in** — needs a codec with an analog input, which is exactly what the ADV added |

## Gaps

* Datasheet **retrieved but not committed and not mined** — sensitivity, SNR, AOP, clock range
  and channel-select behaviour are not transcribed here.
* Knowles' own current copy was not located; only M5Stack's mirror.
* Package marking not verified against a board photograph.
