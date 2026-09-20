# Cardputer ADV — audio in and out

> **Question answered:** *"How do I play sound and record audio on a Cardputer ADV?"*
> Applies to **Cardputer ADV only**. The v1.0/v1.1 path (NS4168 + SPM1423 PDM) is different and
> simpler. Last verified **2026-09-04**. **Contains a live driver defect — read §6.**

## 1. The hardware path

```
                        ┌──────────── ES8311 (U6, I²C 0x18) ────────────┐
  MSM381A3729H9BP  ──►  │ MIC1P/MIC1N → PGA → ADC → ASDOUT ──► G46      │
  (U8, analog MEMS)     │                                              │
                        │  G42 ──► DSDIN → DAC → OUTP/OUTN ──┬─► NS4150B (U5) ─► 8 Ω 1 W speaker
  G41 ──► SCLK (BCLK)   │                                    └─► DAC_P ─► PJ-342 3.5 mm jack (J7)
  G43 ──► LRCK          │                                              │
  G8/G9 ──► CDATA/CCLK  └──────────────────────────────────────────────┘
                                        HP_DET ─► Q4 2N7002T ─► AMP_EN ─► NS4150B CTRL
```

| Part | Designator | Role | Record |
|---|---|---|---|
| ES8311 | U6 | codec, I²C `0x18`, I²S slave | [`everest-semiconductor/es8311`](../../../../components/everest-semiconductor/es8311/README.md) |
| NS4150B | U5 | mono class-D, `CTRL` = `AMP_EN` | [`nsiway/ns4150b`](../../../../components/nsiway/ns4150b/README.md) |
| MSM381A3729H9BP | U8 | analog MEMS mic, SNR 65 dB | [`memsensing/msm381a3729h9bp`](../../../../components/memsensing/msm381a3729h9bp/README.md) |
| PJ-342 | J7 | 3.5 mm jack with detect | [`generic/3.5mm-audio-output`](../../../../components/generic/3.5mm-audio-output/README.md) |
| 2N7002T | Q4 | `HP_DET` → `AMP_EN` inversion | — |

Supporting parts read off sheet 3: FB1/FB2/FB3 ferrites on the speaker outputs, R16/R17
100 k 1 % and R23 10 k 1 % around the amplifier inputs, R24 33 R on `AVDD`, R39 10 R, R40 1 k,
R42 1 k and D3 `1N4148WT` in the headphone-detect network, C13–C33 decoupling.

**There is no MCLK line.** G45 is unwired; Meshtastic declares `DAC_I2S_MCLK 45 // dummy`.
The codec must be told to derive its master clock from BCLK.

## 2. Pin table

| Signal | GPIO | ES8311 pin |
|---|---|---|
| I²C `CCLK` (SCL) | G9 | 1 |
| I²C `CDATA` (SDA) | G8 | 19 |
| I²S `BCLK` | G41 | 6 `SCLK/DMIC_SCL` |
| I²S `LRCK` | G43 | 8 |
| I²S `DSDIN` (host → codec) | G42 | 9 |
| I²S `ASDOUT` (codec → host) | G46 | 7 |
| Port | `I2S_NUM_1` | — |

The v1.x used the **same four I²S pins** (G41/G43/G42 for the NS4168, G46/G43 for the PDM mic)
— which is why so much v1.x audio code half-works on an ADV: the pins are right and the codec
is simply never initialised, so nothing comes out.

## 3. Minimal procedure — Arduino / M5Unified

M5Unified does everything, including the codec:

```cpp
#include <M5Cardputer.h>

void setup() {
  auto cfg = M5.config();
  cfg.internal_spk = true;
  cfg.internal_mic = true;
  M5Cardputer.begin(cfg, true);
  M5Cardputer.Speaker.setVolume(128);
}

void loop() {
  M5Cardputer.Speaker.tone(880, 200);   // enabling the speaker runs the ES8311 init
  delay(1000);
}
```

`M5Unified` sets, for `board_M5CardputerADV`:

```cpp
spk_cfg.pin_bck = GPIO_NUM_41; spk_cfg.pin_ws = GPIO_NUM_43;
spk_cfg.pin_data_out = GPIO_NUM_42; spk_cfg.magnification = 16;
spk_cfg.i2s_port = I2S_NUM_1;
spk_enable_cb = _speaker_enabled_cb_cardputer_adv;      // M5Unified.cpp:3018-3031

mic_cfg.pin_data_in = GPIO_NUM_46; mic_cfg.pin_ws = GPIO_NUM_43;
mic_cfg.pin_bck = GPIO_NUM_41;
mic_enable_cb = _microphone_enabled_cb_cardputer_adv;   // M5Unified.cpp:2672-2680
```

Note `mic_cfg.pin_bck` is set on the ADV and **not** on the v1.x — the PDM mic needed only a
clock and a data line; the codec needs a full I²S frame.

## 4. Working examples

* `M5Cardputer/examples/Basic/buzzer` and `Basic/mic`, `Basic/mic_wav_record` — vendored at
  [`../artifacts/source-snapshots/M5Cardputer-f1392858/examples/`](../artifacts/source-snapshots/M5Cardputer-f1392858/examples/).
  Written for the v1.x; they exercise the same M5Unified API and therefore work on the ADV
  through the callbacks.
* `AndyAiCardputer/mp3-player-winamp-cardputer-adv` — explicitly "with ES8311 audio codec support".
* `halbeshuhn/Cardputer-WebRadio`, `wusiu/WebRadio_WuSiU_Cardputer_Adv` — streaming decode.
* `urtubia/miniacid`, `CHARL3X/GLIDE-Synth-Cardputer-ADV` — synthesis, i.e. sustained
  low-latency output.
* Meshtastic pulls `pschatzmann/arduino-audio-driver@v0.3.0` for the ADV variant, which is a
  third independent ES8311 implementation if you want to compare.

## 5. Alternatives

| Approach | When | Notes |
|---|---|---|
| `M5Unified` `Speaker_Class`/`Mic_Class` | default | handles codec enable/disable, mixing, WAV |
| `pschatzmann/arduino-audio-driver` | you want a maintained standalone ES8311 driver | what Meshtastic uses |
| Raw `driver/i2s_std.h` + your own I²C writes | full control over sample format and codec registers | you must implement the enable sequence yourself; see §6 for what *not* to copy |
| ESP-ADF | full audio pipeline | heavy for 512 KB with no PSRAM |

## 6. ⚠ Vendor driver audit — ES8311 enable callbacks

Read side by side with the ES8311 register map. Two findings; the second is a live bug.

### 6.1 The two callbacks disagree about register `0x01`

[`M5Unified.cpp:1000-1023`](https://github.com/m5stack/M5Unified/blob/8530f5377d782e4a25a6c482de2e71c3f75ca8eb/src/M5Unified.cpp#L1000-L1023) — speaker enable:

```c
2, 0x00, 0x80,  // RESET / CSM POWER ON
2, 0x01, 0xB5,  // CLOCK_MANAGER / MCLK=BCLK
2, 0x02, 0x18,  // CLOCK_MANAGER / MULT_PRE=3
2, 0x0D, 0x01,  // SYSTEM / power up analog
2, 0x12, 0x00,  // SYSTEM / power-up DAC      - NOT default
2, 0x13, 0x10,  // SYSTEM / enable HP drive   - NOT default
2, 0x32, 0xBF,  // DAC volume (0 dB)
2, 0x37, 0x08,  // bypass DAC equaliser       - NOT default
```

[`M5Unified.cpp:1481-1507`](https://github.com/m5stack/M5Unified/blob/8530f5377d782e4a25a6c482de2e71c3f75ca8eb/src/M5Unified.cpp#L1481-L1507) — microphone enable:

```c
2, 0x00, 0x80,
2, 0x01, 0xBA,  // CLOCK_MANAGER / MCLK=BCLK     ← 0xBA, not 0xB5
2, 0x02, 0x18,
2, 0x0D, 0x01,
2, 0x0E, 0x02,  // enable analog PGA + ADC modulator
2, 0x14, 0x10,  // Mic1p-Mic1n, PGA gain minimum
2, 0x17, 0xBF,  // ADC volume 0 dB
2, 0x1C, 0x6A,  // ADC EQ bypass, DC-offset cancel
```

`0x01` is one clock-manager register on one shared codec. `0xB5` and `0xBA` differ in the low
nibble — the ADC/DAC clock-divider select field. **Whichever subsystem is enabled last wins**,
and the other runs on a divider it did not ask for. Severity: *latent*, because both values
enable both clock trees and the audible effect at 16 kHz mono is small — but it means
speaker-then-mic and mic-then-speaker are not equivalent, which is exactly the kind of thing
that produces "it only works if I start the mic first" bug reports.

### 6.2 ⚠ Disabling the microphone powers down the codec, silencing the speaker

The microphone's `disabled_bulk_data`:

```c
2, 0x0D, 0xFC,  // SYSTEM / power down analog circuitry
2, 0x0E, 0x6A,
2, 0x00, 0x00,  // RESET / CSM POWER DOWN        ← powers down the whole chip
```

The speaker's `disabled_bulk_data` is **empty** (`{ 0 }` — a zero-length command list).

So:

* `Mic.end()` (or any M5Unified path that disables the mic) executes **`0x00 = 0x00`, CSM power
  down**, on the codec that is also driving the speaker. Any speaker output in flight stops and
  will not resume until something re-runs the speaker enable sequence.
* Conversely `Speaker.end()` does nothing at all — the codec stays fully powered, analog
  circuitry live. That is a **standby-current cost that the vendor's own 0.23 µA figure does
  not include**, because that figure is measured with the power switch OFF.

**Status: active defect**, present at `M5Unified` `8530f537` (2026-08-27). It is a genuine
cross-subsystem interaction, not a theoretical one: M5Unified auto-toggles enable state when
you alternate `Speaker` and `Mic` use, which is exactly what a voice-recorder or a
push-to-talk app does.

**Workaround:** after any microphone teardown, force a speaker re-enable
(`M5.Speaker.end(); M5.Speaker.begin();`) before playing again, or drive the codec yourself and
never call the vendor disable path.

**Not filed upstream by this session.**

### 6.3 What the driver never touches

Neither callback reads any ES8311 status or fault register, and neither reads the chip ID
(`0xFD`/`0xFE`) to confirm a codec is actually present. On a board where the codec is the only
audio path, a silent I²C failure produces silence with no diagnostic. Bruce's port
(`boards/m5stack-cardputer/interface.cpp:491-527`) copies the same sequences verbatim,
including the register-`0x01` divergence — so the defect has already propagated to the largest
third-party firmware.

## 7. The headphone jack and the speaker mute

M5Stack states: *"When a 3.5 mm headphone jack is inserted, the speaker amplifier will be
disabled."* The mechanism on sheet 3 is `HP_DET` from the PJ-342's switch contact, through
D3 (`1N4148WT`) and Q4 (`2N7002T`) with R40/R42 1 k, producing `AMP_EN` into the NS4150B's
`CTRL` pin. It is **hardware, not firmware** — no GPIO participates, and there is no way for
software to read jack-insertion state or to override the mute.

Contrast the CardputerZero, which routes `HP_DET` to a CPU GPIO (`G17`) and enables its
amplifier from `G24`. The ADV gives up that flexibility for pin count.

## 8. Resources and conflicts

| Resource | Used | Conflicts |
|---|---|---|
| `I2S_NUM_1` | speaker **and** mic | `I2S_NUM_0` is free; you cannot easily run them as two independent ports because there is one codec |
| G41, G42, G43, G46 | dedicated | none |
| I²C `0x18` | ES8311 | shares the bus with TCA8418 `0x34` and BMI270 `0x69` |
| CPU | software mixing in `Speaker_Class` | at 240 MHz with no PSRAM, sustained decode + display + Wi-Fi is the realistic ceiling; see [`../performance.md`](../performance.md) |

Simultaneous-use notes:

* **Audio + keyboard**: both on the internal I²C bus. Codec register writes are short; key
  events are FIFO-buffered. No failures reported.
* **Audio + microSD**: independent buses, but both want CPU. WAV playback from SD is
  demonstrated by several projects.
* **Audio + Wi-Fi streaming**: demonstrated (`Cardputer-WebRadio`), and the community reports it
  as the memory ceiling on a no-PSRAM part.

## 9. Limits

| Limit | Value | Class |
|---|---|---|
| Speaker | 8 Ω, 1 W | board |
| Mic SNR | 65 dB | vendor spec |
| No MCLK | must use BCLK-derived clocking | board |
| No PSRAM | decode buffers live in 512 KB SRAM | **silicon** |
| Jack detect | hardware-only, not readable | board |
| Sample rates | not characterised by this session | not tested |

## 10. Evidence status

| Claim | Status |
|---|---|
| Part identities, designators, pin-to-pin wiring | **official** — schematic sheet 3 text layer, validated against the product page's PinMap |
| I²S/I²C pin assignment | **official** — M5Unified source, three independent implementations agree |
| Register sequences quoted | **official** — verbatim from M5Unified at a pinned commit |
| §6.1 divergence, §6.2 power-down interaction | **derived by reading the source**; consequences reasoned, **not hardware-tested** |
| Hardware jack mute | **official** — vendor prose + schematic network |
| Any audio quality, latency or level measurement | **not tested** |
