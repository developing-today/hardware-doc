# How do I play and record audio? — ESP32-P4-WIFI6-Touch-LCD-3.4C

> Evidence status: **vendor documentation + vendor source code. Untested on hardware.**
> Applies equally to the [4C](../../esp32-p4-wifi6-touch-lcd-4c/README.md).

## Capability summary

A full duplex audio subsystem: **ES8311** codec for playback into a speaker amplifier, and an
**ES7210** echo-cancellation ADC for microphone capture. The ES7210's presence is the interesting
part — it signals the board is intended for **voice interaction while audio is playing**
(intercom, voice assistant, hands-free), not just beeps.

## Hardware path

```
ESP32-P4 --I2S--> ES8311 codec --> power amp --> PH2.0 speaker header (8 ohm 2 W)
         --I2S<-- ES7210 AEC ADC <-- on-board MEMS microphone
         --I2C--> both chips (control), GPIO7/8
         --GPIO53--> amplifier enable
```

| Signal | GPIO | Evidence |
|---|---:|---|
| I²S MCLK | **13** | `05_I2SCodec/main/example_config.h`, `CONFIG_IDF_TARGET_ESP32P4` branch |
| I²S BCLK | **12** | same |
| I²S WS / LRCK | **10** | same |
| I²S DOUT (P4 → codec) | **9** | same |
| I²S DIN (codec → P4) | **11** | same |
| Amplifier enable (PA) | **53** | same, `GPIO_OUTPUT_PA` |
| I²C SDA / SCL | **7** / **8** | same |

These come from the **`CONFIG_IDF_TARGET_ESP32P4` branch** of Waveshare's config header. The same
file contains ESP32/S2/S3/H2 branches with entirely different pins — read the right branch. Taking
`GPIO_OUTPUT_PA (GPIO_NUM_46)` from the S3 branch, for example, would be wrong here; the P4 value
is **53**.

## ESP-IDF

```yaml
dependencies:
  idf: "^5.0"
  espressif/es8311: "^1.0.0"
```

Reference project:
`../../esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/demo/ESP-IDF/05_I2SCodec/`

It ships `canon.pcm` as test audio. Broad shape:

1. Bring up I²C (GPIO7/8) and probe the ES8311.
2. Configure I²S with the pins above; the ES8311 needs **MCLK**, so do not omit GPIO13.
3. Configure codec format and volume over I²C.
4. Drive **GPIO53 high to enable the amplifier**.
5. Stream PCM.

> The ES7210 capture path is **not** exercised by `05_I2SCodec`, which is playback-only. No
> Waveshare demo in this archive demonstrates ES7210 capture or echo cancellation. Capture is
> therefore the least-evidenced feature on this board.

## A working capture reference

No *official* example exercises the ES7210, but **XiaoZhi** (`78/xiaozhi-esp32`,
`main/boards/waveshare/esp32-p4-wifi6-touch-lcd/config.h`) configures it for real:

```c
#define AUDIO_INPUT_SAMPLE_RATE  24000
#define AUDIO_OUTPUT_SAMPLE_RATE 24000
#define AUDIO_INPUT_REFERENCE    true      // AEC reference channel
#define AUDIO_CODEC_ES7210_ADDR  ES7210_CODEC_DEFAULT_ADDR
```

24 kHz full duplex with an acoustic-echo-cancellation reference channel — which is the ES7210's
whole purpose. Combined with the BSP's `i2s_rx_chan`, capture is **supported and demonstrated in
community code**, just not by Waveshare.

> That file is one `#elif` chain covering nine Waveshare P4 boards. Read only the
> `CONFIG_BOARD_TYPE_WAVESHARE_ESP32_P4_WIFI6_TOUCH_LCD_3_4C` (or `_4C`) block — other variants use
> different reset/backlight pins.

## Speaker

PH2.0 2-pin header, **8 Ω 2 W recommended** by Waveshare. Two practical points:

- The amplifier is gated by GPIO53. If it is low, everything else can be perfect and you hear
  nothing. Check this before suspecting I²S.
- 2 W into a small enclosure draws real current in bursts. If the board is USB-powered and browns
  out on loud passages, that is a supply problem, not an audio bug.

## Resource conflicts

| Resource | Shared with | Note |
|---|---|---|
| I²C GPIO7/8 | **GT911 touch** | Three devices on one bus — see [touch.md](./touch.md) |
| I²S GPIO9–13 | Nothing else known | Audio-exclusive |
| GPIO53 | Nothing else known | Amplifier enable |
| PSRAM bandwidth | Display, camera | Audio buffers are small by comparison |

The shared I²C bus is the one that matters: a wedged codec stalls **touch** too, and vice versa.
`03_i2c_tools` should confirm all three devices answer before you debug either subsystem.

Audio + display + camera + SD concurrently is **untested**. Audio's bandwidth demand is negligible
against video, but its **latency** demand is not — underruns are audible where a dropped video
frame is not. Treat audio as latency-sensitive when scheduling alongside camera work.

## Limits

| Limit | Value | Kind |
|---|---|---|
| Speaker | 8 Ω 2 W recommended | Board |
| Codec | ES8311 (mono) | Silicon |
| Capture | ES7210 AEC ADC | Silicon |
| Sample rates / bit depths | **Not established** | — |
| Measured latency, SNR, output power | **Unknown — not measured** | — |

## Pitfalls

1. **Reading the wrong `#ifdef` branch.** Use the `CONFIG_IDF_TARGET_ESP32P4` values.
2. **Forgetting GPIO53.** Silence with correct I²S.
3. **Omitting MCLK.** The ES8311 needs GPIO13.
4. **Assuming capture works** because playback does — no demo covers ES7210.
5. **Brownout on loud output** when USB-powered.

## Open questions

- ES7210 capture configuration and I²C address; is echo cancellation on-chip or host-side?
- Supported sample rates and bit depths.
- Whether the MEMS microphone reaches the P4 only via the ES7210 or also directly.
- Amplifier part number — not identified in the schematic text extraction.

## Related

- [Touch](./touch.md) — shares the I²C bus
- [Shared platform record](../../esp32-p4-wifi6-touch-lcd-xc-shared/README.md)
- [Gaps and conflicts](../gaps-and-conflicts.md)
