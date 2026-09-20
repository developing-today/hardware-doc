# Audio — playback, capture and the two output paths

**Question:** *How do I play sound and record from the microphone — and why is there no sound?*

| | |
|---|---|
| On-chip | [K230](../../../../components/canaan/k230/README.md) audio codec: **2 DAC + 2 ADC channels, 8–192 kHz**, ALC, up to **8 PDM DMICs**, I²S with 2×2 expansion |
| External amp | [MAX98357A](../../../../components/analog-devices/max98357a/README.md) on the **nRF52840 base board** |
| I²S pins | data `GPIO35`, BCLK `GPIO32`, LRCK `GPIO33`, shutdown `GPIO34` (**high = on**) |
| Analogue out | 3.5 mm jack (Cased Version) |
| Speaker / microphone parts | **unidentified** — [`unidentified/t-display-k230`](../../../../components/unidentified/t-display-k230/README.md) U2, U3 |
| Userspace | **ALSA** (`amixer`, `aplay`) |
| Evidence | `reported-working` |

## Two output paths, and this is the usual cause of silence

The K230 has an **on-die codec** that can drive the headphone jack directly, *and* an I²S output
that feeds the MAX98357A on the expansion base. They are different sinks and the BSP adds an
explicit route switch to choose between them:

- `0059-asoc-canaan-add-external-i2s-output-switch.patch`
- `0058-riscv-dts-rm69a10-add-audio-fan-sensor-pins.patch` (pin muxing)

**If there is no sound, check the route before anything else.** Then check `GPIO34` — the
MAX98357A is in shutdown when that line is low.

## Playing and recording

```sh
aplay -l                     # list playback devices
aplay -D <dev> file.wav
amixer                       # the route switch and volumes live here
arecord -D <dev> -f S16_LE -r 16000 out.wav
```

Buildroot builds `alsa-utils` with `amixer` and `aplay`
(`BR2_PACKAGE_ALSA_UTILS_AMIXER`, `_APLAY`), plus Canaan's `audio_demo`
(`BR2_PACKAGE_AUDIO_DEMO`) and `audio_rec_play` (`BR2_PACKAGE_AUDIO_REC_PLAY`).

Launcher apps: music player, network radio, recorder, video player,
`ui_audio.c`, `ui_i2s_test.c`, `ui_mic_spectrum.c`, `pcm_volume.c`.

## Microphone

A microphone exists (wiki, and the launcher's mic spectrum and Xiaozhi wake-word features).
**Whether it is PDM or analogue is unknown** — the K230 supports both, up to 8 PDM DMICs or 2 ADC
channels. See U3 in the unidentified-parts record.

**Ownership matters:** *"Wake-word listening is active only while the Xiaozhi app is open and
owns the microphone."* One consumer at a time, arbitrated in the launcher only.

## Alternatives

| Route | When |
|---|---|
| On-chip codec → 3.5 mm | Headphones, line out. No extra hardware. |
| On-chip I²S → MAX98357A | Speaker on the nRF52840 base. Louder, mono, needs the base board. |
| PDM DMIC | Up to 8, board fits fewer. |
| USB audio | Possible via the USB host port; untested. |

## Limits

| Limit | Value | Class |
|---|---|---|
| Sample rates | 8–192 kHz | silicon |
| DAC / ADC | 2 / 2 | silicon |
| PDM DMICs | 8 max | silicon |
| MAX98357A | mono, 3.2 W into 4 Ω @ 5 V | component |
| Simultaneous I²S-out + PDM-in | supported by the SoC; **untested on this board** | silicon / unmeasured |
| Measured SNR, output power, latency | **none published** | unmeasured |

## Pitfalls

1. Wrong route → silence with no error.
2. `GPIO34` low → amplifier in shutdown.
3. The MAX98357A is on the **nRF52840 base**, not the bare board or the keyboard base.
4. `0058` mentions "fan" pins alongside audio — a fan header may exist on some variant. The
   launcher has `K230_FAN_ENABLED 0`. Unverified.
