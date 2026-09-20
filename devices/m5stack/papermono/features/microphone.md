# Microphone — M5Stack PaperMono

> **How do I record audio, and why do the pins matter more than usual?**
> Hardware revision **V0.6.2** · snapshot **2026-09-01** · nothing tested on hardware.

## 1. Capability summary and the hardware path

A single PDM microphone on the KEY/RGB sub-board, read by the ESP32-S3's I²S peripheral
in PDM RX mode, with its supply switched by the [I/O expander](io-expander.md).

```
LMD4737T261-AC02 (PDM mic)  ──DAT──▶ ESP32-S3 GPIO46
                            ◀─CLK─── ESP32-S3 GPIO45
                            ◀─VDD─── PDM_VDD, AW35122 load switch (U21), M5IOE1 IO12
```

| Element | Part | Record |
|---|---|---|
| Microphone | `LMD4737T261-AC02` | [`components/generic/lmd4737t261-ac02-pdm-microphone`](../../../../components/generic/lmd4737t261-ac02-pdm-microphone/README.md) |
| Power switch | Awinic `AW35122` (`U21`) | [`components/awinic/aw35122`](../../../../components/awinic/aw35122/README.md) |
| Power enable | M5IOE1 `IO12` | [`io-expander.md`](io-expander.md) |
| Connector | `J6` (16-pin B2B to the sub-board) | [`../pinouts-and-buses.md`](../pinouts-and-buses.md#connectors) |

> **No datasheet for `LMD4737T261-AC02` exists.** The only web occurrences anywhere are
> M5Stack's own pages. Sensitivity, SNR, AOP, frequency response, supply current and
> supported clock range are all **unknown**. Nothing about audio quality can be stated
> here.

## 2. ⚠ Both microphone pins are ESP32-S3 strapping pins

**GPIO45 and GPIO46 are strapping pins.** They are sampled at reset to select boot
behaviour (`VDD_SPI` voltage and boot-message routing on the ESP32-S3), and here they
carry the PDM clock and data.

Consequences:

- **Anything driving GPIO45 or GPIO46 across a reset perturbs the straps.** The vendor
  firmware does not appear to guard against this. `inferred` from the pin map;
  `not-tested`.
- The microphone is a *data source* on GPIO46 and the ESP32-S3 drives the clock on
  GPIO45, so in normal operation neither is driven by an external part during boot — but
  the mic's own output stage is on GPIO46, and its state at reset depends on whether
  `PDM_VDD` is up.
- The factory firmware **explicitly releases both pins** before reconfiguring
  (`hal_mic.cpp:56–62`):

```c
static void releaseMicPins() {
    gpio_reset_pin(GPIO_NUM_46);
    gpio_set_direction(GPIO_NUM_46, GPIO_MODE_INPUT);
    gpio_set_pull_mode(GPIO_NUM_46, GPIO_FLOATING);
    gpio_reset_pin(GPIO_NUM_45);
}
```

That routine exists for a reason. Copy it.

Note that GPIO3 (Button B) is a **third** strapping pin on this board — see
[`usb-and-serial.md`](usb-and-serial.md) and
[`buttons-and-rgb-led.md`](buttons-and-rgb-led.md).

## 3. Prerequisites

| Item | Value |
|---|---|
| M5Unified | 0.2.21 — `M5.Mic` |
| M5IOE1 | 1.0.9, for `PDM_VDD` |
| ESP-IDF | 5.5.1 |
| Power state | **L3B** |

## 4. Resources consumed

| Resource | Value |
|---|---|
| ESP32-S3 GPIO | **GPIO45** (`PDM_CLK`), **GPIO46** (`PDM_DAT`) — both strapping pins |
| I²S peripheral | **`I2S_NUM_0`** in the factory firmware |
| Expander pin | `IO12` (`PDM_VDD_EN`) |
| Rail | `PDM_VDD` (state L3B) |
| DMA | `dma_buf_len = 128`, `dma_buf_count = 8` |

## 5. The vendor's exact configuration

Transcribed from `M5PaperMono-UserDemo/main/hal/hal_mic.cpp:12–96`. `executed-success`
on the read; `not-tested` on hardware.

| Setting | Value |
|---|---|
| Sample rate | **16 000 Hz** |
| I²S port | `I2S_NUM_0` |
| `pin_ws` | GPIO45 (the PDM clock lands on `WS`) |
| `pin_data_in` | GPIO46 |
| `pin_mck` / `pin_bck` | `I2S_PIN_NO_CHANGE` |
| `input_channel` | `m5::input_channel_t::input_only_right` |
| `over_sampling` | 1 |
| `magnification` | 2 |
| `dma_buf_len` / `dma_buf_count` | 128 / 8 |

`input_only_right` is worth noting: the microphone appears on the **right** PDM channel.
Configuring a stereo or left-channel capture gets you silence.

## 6. Minimal procedure (`inferred`)

```cpp
#include <M5Unified.h>
#include <M5IOE1.h>

static int16_t buf[512];

bool initMic() {
  M5.Mic.end();
  ioe1.digitalWrite(M5IOE1_PIN_12, LOW);   delay(20);   // power-cycle the mic
  ioe1.digitalWrite(M5IOE1_PIN_12, HIGH);  delay(20);
  releaseMicPins();                                     // see section 2

  auto c = M5.Mic.config();
  c.pin_mck = I2S_PIN_NO_CHANGE;  c.pin_bck = I2S_PIN_NO_CHANGE;
  c.pin_ws  = GPIO_NUM_45;        c.pin_data_in = GPIO_NUM_46;
  c.i2s_port      = I2S_NUM_0;
  c.input_channel = m5::input_channel_t::input_only_right;
  c.sample_rate   = 16000;
  c.over_sampling = 1;
  c.magnification = 2;
  c.dma_buf_len   = 128;  c.dma_buf_count = 8;
  M5.Mic.config(c);
  return M5.Mic.begin();
}

void record() {
  M5.Mic.record(buf, 512, 16000, false);
  while (M5.Mic.isRecording()) { delay(1); }    // vendor waits with a 160 ms timeout
}
```

The **power-cycle before `begin()`** is not decoration — the vendor's `initMic()` does
exactly that, with 20 ms settling on each side.

## 7. Silicon / board / framework / observed limits

| Class | Limit |
|---|---|
| **Silicon (ESP32-S3)** | PDM RX is available on `I2S_NUM_0`. `I2S_NUM_1` exists but does not do PDM RX — so **the microphone and an I²S playback path cannot both use instance 0** |
| **Board** | Both pins are strapping pins (§2) |
| **Board** | **Mono, one microphone.** No stereo, no beamforming |
| **Board** | Supply switchable, so the mic can be fully powered down |
| **Framework** | Vendor configures 16 kHz / right channel only; other rates were not exercised by any vendor code |
| **Unknown** | Every acoustic parameter — no datasheet exists |

## 8. There is no audio output path for this

The PaperMono has a **[buzzer](buzzer.md), not a speaker**. There is no codec, no
amplifier and no DAC output on the board.

Curiously, **both** custom chips' register maps expose an `AW8737A_PULSE` register
(M5PM1 `0x53`, M5IOE1 `0x90`) — an audio-amplifier control — with no corresponding
amplifier anywhere in the PaperMono BOM. These are almost certainly generic features of
the shared `PY32L020F15U6` firmware rather than anything populated on C153. `inferred`.

There is also a version delta worth knowing: M5Unified `develop` contains a change
described in its own diff as *"Keep Audio Power (M5IOE1_G3) on: cutting it forces another
codec…"*. **That comment is about a different board** — on the PaperMono, M5IOE1 `IO3` is
the e-paper rail. Do not read it as PaperMono audio guidance.

## 9. Conflicts and simultaneous use

| Combination | Verdict | Mechanism |
|---|---|---|
| Mic + [buzzer](buzzer.md) | ✅ | Different peripherals — I²S vs LEDC — and the buzzer will be audible in the recording |
| Mic + I²S playback | ❌ **not on the same instance** | PDM RX occupies `I2S_NUM_0`. There is nothing to play to anyway |
| Mic + [display](epaper-display.md) refresh | ⚠ untested | No pin conflict; both are DMA clients |
| Mic + [sleep](power-and-sleep.md) below L3B | ❌ | `PDM_VDD` is an L3B rail |
| Mic pins + reset/boot | ⚠ | Strapping pins (§2) |
| Mic + [Wi-Fi](wifi-and-bluetooth.md) | ⚠ untested | The usual DMA/CPU contention; no measurement exists |

## 10. Debugging

| Symptom | Cause |
|---|---|
| `M5.Mic.begin()` fails | `PDM_VDD` off (`IO12`); or the pins were left claimed — call `releaseMicPins()` |
| Silence, no error | Wrong channel — the mic is on `input_only_right` |
| Board boots into an odd mode after a recording session | GPIO45/46 strap perturbation (§2) |
| Level too low / too high | `magnification = 2` in the vendor config; there is no hardware gain control |
| Distortion | Unknown — no AOP figure exists for this microphone |

## 11. Unresolved questions

- **No acoustic specification exists at all** for `LMD4737T261-AC02`.
- Whether sample rates other than 16 kHz work — nothing exercises them.
- Whether the strapping-pin exposure causes real boot failures in practice.

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**; the microphone is fitted on both C153 and C153-LITE |
| Framework range | M5Unified 0.2.21 · ESP-IDF 5.5.1 · M5IOE1 1.0.9 |
| Evidence | Pin map and I²S configuration: **read from vendor source** at cited `file:line`. Strapping-pin hazard: **`inferred`** from the pin map. Sketch: **`inferred`** |
| Confidence | High on wiring and the exact vendor config; **zero on audio quality** |
| Last verified | **2026-09-01** |

## Related

- [`../pinouts-and-buses.md`](../pinouts-and-buses.md) · [`../resources-and-conflicts.md`](../resources-and-conflicts.md)
- [`buzzer.md`](buzzer.md) · [`io-expander.md`](io-expander.md) · [`usb-and-serial.md`](usb-and-serial.md) · [`power-and-sleep.md`](power-and-sleep.md)
- [`components/generic/lmd4737t261-ac02-pdm-microphone`](../../../../components/generic/lmd4737t261-ac02-pdm-microphone/README.md) · [`components/awinic/aw35122`](../../../../components/awinic/aw35122/README.md)
