# Everest Semiconductor ES8311

- **Category:** low-power mono **audio codec** — ADC + DAC, I²S/PCM serial audio, I²C control, integrated microphone bias and PGA
- **Manufacturer:** Everest Semiconductor (深圳市中科蓝讯 / Everest-semi)
- **Control interface:** I²C. 7-bit address **`0x18`** with `CE` low, `0x19` with `CE` high — **`inferred` from the datasheet, not read from any board's source in this pass**
- **Document status:** datasheet retained; **version `unknown`** — the mirrored copy carries no revision marking that this pass identified
- **Research status:** **stub.** The datasheet is held and validated; the register map has **not** been mined. Board-level integration is documented under [Used by](#used-by)
- **Retrieved:** 2026-09-01. **Nothing verified on hardware.**

## What it is

A single-channel codec aimed at voice: one ADC path for a microphone, one DAC path
for a speaker or line output, with the analogue front end (bias, PGA) integrated so a
host needs only an amplifier for loudspeaker drive. It is the codec Espressif's own
reference designs use most often for voice-assistant work, which is why it appears on
so many ESP32-S3 boards.

Audio data moves over **I²S**; configuration goes over **I²C**. Both are needed —
a board that wires I²S but not I²C cannot bring the part out of reset into a useful
state.

## What has not been done

- **Register map not transcribed.** No initialisation sequence, no clock-tree
  analysis, no PGA or ALC settings.
- **No audit of any driver against the datasheet** — the method's
  [step 10](../../../.agents/skills/hardware-device-research/SKILL.md#10-audit-vendor-firmware-and-driver-source-against-the-primary-documents).
  Waveshare ships a hand-rolled `es8311.cpp`/`es8311_reg.h` rather than using a
  library, which makes it a good audit target.
- **No I²C address confirmed on hardware or in board source.** The `0x18`/`0x19`
  values above are the part's documented defaults, labelled `inferred`.
- **No comparison** against the sibling [ES8156](../es8156/README.md) already in this
  knowledge base — the ES8156 is DAC-only, so the two are not interchangeable where
  capture is needed, but that has not been written up properly.

## Artifacts

| File | Bytes | SHA-256 | Source | Retrieved | Version |
|---|---|---|---|---|---|
| [`artifacts/es8311-datasheet-waveshare-mirror.pdf`](artifacts/es8311-datasheet-waveshare-mirror.pdf) | 729 315 | `be42a2cb09093378feaccf55c227be579edc5a17786a11cc34254ea91264538a` | `https://files.waveshare.com/wiki/common/ES8311.DS.pdf` | 2026-09-01 | `unknown` |

**This is Waveshare's mirror, not Everest's own copy.** Named accordingly, per the
repository's rule that a vendor mirror is retained only when labelled as one. The
manufacturer's original was **not obtained** in this pass — worth doing, because
[Waveshare's mirrors have already been shown to run stale on this very board](../../nxp/pcf85063a/README.md):
its PCF85063A copy is three years and one revision behind NXP's.

Validated by magic bytes (`%PDF-`), not by HTTP status. **Licence `unknown`** — no
stated terms. Disposition: `repository`.

## Used by

### [Waveshare ESP32-S3-ePaper-3.97](../../../devices/waveshare/esp32-s3-epaper-3.97/README.md)

Designator `U8`. The board's only audio codec, providing both the microphone capture
path and the playback path that feeds the
[NS4150B](../../nsiway/ns4150b/README.md) amplifier and the MX1.25 speaker header.

| Connection | Pin | Note |
|---|---|---|
| I²S `MCLK` | GPIO13 | |
| I²S `SCLK` | GPIO14 | |
| I²S `LRCK` | GPIO47 | |
| I²S `DSOUT` | GPIO21 | codec → host (capture) |
| I²S `DSDIN` | GPIO48 | host → codec (playback) |
| I²C `SDA` / `SCL` | GPIO41 / GPIO42 | **shared** with the PMIC, RTC and IMU |
| Amplifier gate | GPIO39 (`AudioCTR_PIN`) | **also carries `AXIS_INT1` in the schematic table — [unresolved](../../../devices/waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws9--gpio39-carries-two-functions)** |

Microphone nets `MIC_P` / `MIC_N` reach the codec differentially. This is the
hardware behind the board's marketed "AI voice interaction" — the cloud side of which
is the third-party [xiaozhi](https://github.com/78/xiaozhi-esp32) firmware, not a
Waveshare service. See
[development.md](../../../devices/waveshare/esp32-s3-epaper-3.97/development.md).

Vendor example: `Arduino/examples/01_Audio_Test`, plus ESP-IDF `02_Mic_test` and
`03_Music`.

### M5Stack Cardputer ADV (K132-Adv) — [`devices/m5stack/cardputer-adv`](../../../devices/m5stack/cardputer-adv/README.md)

Designator **U6**, I²C **`0x18`** on the internal bus (SDA G8 / SCL G9), I²S slave on
`I2S_NUM_1`: `SCLK` G41, `LRCK` G43, `DSDIN` G42, `ASDOUT` G46. **No MCLK is wired**, so the
codec is configured MCLK-from-BCLK (`0x01 = 0xB5` or `0xBA`, `0x02 = 0x18` → `MULT_PRE=3`).

It is the **only** audio path on the board: the analog MEMS microphone
([MSM381A3729H9BP](../../memsensing/msm381a3729h9bp/README.md)) feeds `MIC1P`/`MIC1N`, and the
DAC drives both the [NS4150B](../../nsiway/ns4150b/README.md) speaker amplifier and the 3.5 mm
jack. Nothing on this board makes a sound without it.

⚠ **Two defects in M5Unified's ADV callbacks** (`8530f537`), both inherited verbatim by Bruce:

1. `_speaker_enabled_cb_cardputer_adv` writes `0x01 = 0xB5` while
   `_microphone_enabled_cb_cardputer_adv` writes `0x01 = 0xBA` — **the same clock-manager
   register on the same shared codec**. Last writer wins; speaker-then-mic and mic-then-speaker
   are not equivalent.
2. The **microphone's** disable list ends `0x00 = 0x00` (**CSM power down**), while the
   **speaker's** disable list is **empty**. So disabling the mic silences the speaker, and
   disabling the speaker leaves the codec fully powered.

Analysis: [`devices/m5stack/cardputer-adv/features/audio.md` §6](../../../devices/m5stack/cardputer-adv/features/audio.md).

*Added 2026-09-07 from `archive/devices/m5stack/shared-artifacts/cardputer/research-scratch/index-fragments.md` §3.1.*

## See also

- [ES8156](../es8156/README.md) — DAC-only sibling, already recorded here
- [NS4150B](../../nsiway/ns4150b/README.md) — the amplifier it drives on this board
- [All components](../../README.md)
