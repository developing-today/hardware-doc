# Analog Devices (Maxim) MAX98357A — I²S 3.2 W Class-D mono amplifier with integrated DAC

- **Category:** digital audio power amplifier — PCM I²S input, Class-D speaker output, **no I²C control interface**
- **Manufacturer:** Maxim Integrated, now **Analog Devices**
- **Retrieved:** 2026-09-04

## 1. Core facts

| Property | Value |
|---|---|
| Input | **I²S / left-justified / TDM** PCM, 8 – 96 kHz |
| Output | mono Class-D, **3.2 W into 4 Ω** at 5 V, 10 % THD |
| Supply | 2.5 – 5.5 V |
| Control | **none — no I²C, no SPI.** Configuration is by resistor strapping on `SD_MODE` and `GAIN_SLOT` |
| Channel select | `SD_MODE` resistor divider selects Left / Right / (L+R)/2 **and** shutdown |
| Gain | `GAIN_SLOT` resistor selects 3 / 6 / 9 / 12 / 15 dB |
| Datasheet | `https://www.analog.com/media/en/technical-documentation/data-sheets/MAX98357A-MAX98357B.pdf` |

**The thing that bites people:** `SD_MODE` is not a plain enable pin. It is an analogue
threshold input whose *voltage* selects the channel as well as switching the amplifier on. A
firmware author who drives it as a GPIO gets on/off correctly and gets whichever channel the
board's resistor happens to select. On the LilyGO board LilyGO documents it as a plain
"shutdown control … high enables the amplifier, low shuts it down" (S1), which is the correct
*usage* but hides the mechanism.

## 2. Used By

### [LilyGO T-Display K230 / Kit](../../../devices/lilygo/t-display-k230/README.md) — *added 2026-09-04*

Fitted on the **nRF52840 base board** as an **external** I²S amplifier — the K230 already has
an on-die audio codec with two DAC channels, so this is an added speaker path rather than the
only one.

| MAX98357A | K230 |
|---|---|
| `DIN` | **`GPIO35`** / I²S data |
| `BCLK` | **`GPIO32`** / I²S bit clock |
| `LRCK`/`WS` | **`GPIO33`** / I²S word select |
| shutdown | **`GPIO34`** — high = enabled |

Because the on-chip codec and this amplifier are two different sinks, the BSP adds an explicit
route switch: `0059-asoc-canaan-add-external-i2s-output-switch.patch`, plus
`0058-riscv-dts-rm69a10-add-audio-fan-sensor-pins.patch` for the pin muxing. The launcher
exposes it through `ui_i2s_test.c` and the audio settings page.


### [LilyGO T-Display-S3 Pro MVSRBoard](../../../devices/lilygo/t-display-s3-pro-mvsrboard/README.md) — *added 2026-09-07*

The **S** (speaker) in *MVSR* — LilyGO's Microphone/Vibration/Speaker/RTC backplate for the [T-Display-S3 Pro](../../../devices/lilygo/t-display-s3-pro/README.md). Unlike the K230 board above, this is the **only** audio output path on that platform; the ESP32-S3 has no on-die codec.

LilyGO mirrors `MAX98357AETE+T.pdf` in the `T-Display-S3-Pro` repository @ `08b8b2bbcb8b263131af119476403080cd30224f`. It was **not retrieved**, since this record already holds the part; whether LilyGO's mirror is the same revision as the copy held here is **unknown**.

On the same backplate: a [MEMSensing MSM261S4030H0R](../../memsensing/msm261s4030h0r/README.md) microphone and a [PCF85063ATL](../../nxp/pcf85063a/README.md) RTC. **The I²S pin assignment on the backplate was not established** — its schematic (`T-Display-S3-Pro-MVSRBoard_V1.0_20241109.pdf`) was retrieved but not traced, and no MVSRBoard pin header exists in the vendor source. Note also that **two sheets both declare version `V1.0`** with different dates and sizes.
## 3. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | `k230_bsp/docs/HARDWARE_PINMAP.md` | LILYGO | primary | repository doc | `https://github.com/Xinyuan-LilyGO/T-Display-K230/blob/bb831ab358b66f5bd9a87ecd7c580fee4537492e/k230_bsp/docs/HARDWARE_PINMAP.md` | 2026-09-04 | I²S pin mapping, shutdown polarity |
| S2 | `0059-asoc-canaan-add-external-i2s-output-switch.patch` | LILYGO | primary | source | same repo | 2026-09-04 | Route switching between on-chip codec and external amp |
| S3 | MAX98357A/MAX98357B datasheet | Analog Devices | primary | datasheet | `https://www.analog.com/media/en/technical-documentation/data-sheets/MAX98357A-MAX98357B.pdf` | not retrieved | Electrical specification, SD_MODE behaviour |
