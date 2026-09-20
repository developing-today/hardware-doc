# NSIWAY NS4168 — I²S input class-D audio amplifier

> The speaker amplifier on the **Cardputer v1.0 and v1.1**.
> Record created **2026-09-04**. Sibling already in this repository:
> [`nsiway/ns4150b`](../ns4150b/README.md), which is the **analog**-input part the Cardputer ADV
> uses instead.

## Function

A mono **class-D amplifier with an integrated I²S receiver and DAC**. It takes a digital I²S
stream directly — no separate codec — and drives a speaker. That is what makes it attractive for
a small MCU board: three pins from the host, one part, and you have audio out.

The trade-off is that it is **output only**. There is no ADC, no analog input path, no headphone
driver and no I²C control interface: everything is fixed by hardware.

## Key capabilities

| Property | Value | Evidence |
|---|---|---|
| Input | **I²S** (`BCLK`, `LRCLK`, `SDATA`) | M5Stack PinMap |
| Output | mono, bridge-tied load | board: 8 Ω 1 W cavity speaker |
| Rated output | **1 W into 8 Ω** on this board | Cardputer spec table |
| Control | none — **no I²C**, no register interface | board wiring |
| Supply | 3.3 V / 5 V class part | — |
| Enable / shutdown | present on the part; **not routed to a GPIO** on the Cardputer | schematic |

## Pinout as used

| Signal | Cardputer v1.0 / v1.1 GPIO |
|---|---|
| `BCLK` | **G41** |
| `LRCLK` | **G43** |
| `SDATA` | **G42** |

From the M5Stack PinMap table ("Speaker & IR") and corroborated by
[`M5Unified`](https://github.com/m5stack/M5Unified/blob/8530f5377d782e4a25a6c482de2e71c3f75ca8eb/src/M5Unified.cpp#L3018-L3031):

```cpp
case board_t::board_M5Cardputer:
case board_t::board_M5CardputerADV:
  if (cfg.internal_spk) {
    spk_cfg.pin_bck = GPIO_NUM_41; spk_cfg.pin_ws = GPIO_NUM_43;
    spk_cfg.pin_data_out = GPIO_NUM_42;
    spk_cfg.magnification = 16; spk_cfg.i2s_port = I2S_NUM_1;
    if (_board == board_t::board_M5CardputerADV) spk_enable_cb = _speaker_enabled_cb_cardputer_adv;
  }
  break;
```

Note the shape of that code: **the same three pins serve both generations**, and the ADV differs
only by installing an enable callback that configures its ES8311. On the v1.x there is no
callback because there is nothing to configure — the NS4168 has no control interface at all.

`spk_cfg.magnification = 16` is a **software** gain applied by M5Unified before the samples
leave the I²S port. It is the only volume control in the v1.x signal chain that is not the
digital sample values themselves.

## Used By

### M5Stack Cardputer v1.0 (K132) and v1.1 (K132-V11)

[`devices/m5stack/cardputer-v1.0`](../../../devices/m5stack/cardputer-v1.0/README.md) ·
[`devices/m5stack/cardputer-v1.1`](../../../devices/m5stack/cardputer-v1.1/README.md)

Wired as above, driving the internal cavity speaker (8 Ω, 1 W). There is **no headphone jack** on
either board and no way to add one without an external DAC — the NS4168's output is a
bridge-tied class-D switching waveform, not a line-level signal.

**Replaced on the Cardputer ADV** by an [ES8311](../../everest-semiconductor/es8311/README.md)
codec plus an [NS4150B](../ns4150b/README.md) analog-input amplifier. That two-part arrangement
costs an extra IC and two I²C pins, and buys: a real ADC path, a line-level output for the 3.5 mm
jack, an amplifier enable (`AMP_EN`) that the headphone-detect circuit can mute, and
software-controllable codec gain.

## Artifacts

M5Stack mirrors a datasheet — **Chinese only**:

```
https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/datasheet/core/NS4168_CN_datasheet.pdf
```
829 468 B, SHA-256 `479e75a104f48f31584683e5cd3e0d46843884af9da9137680b57700e6a6aab3`,
retrieved 2026-09-04. **Fetched into scratch, not committed here.**

Per the skill's multi-language policy: **no English version was located**, so this Chinese
document is the **primary source** for this part and should be retained on its own merits when a
staging decision is made. The same pattern was recorded for the RX8130CE during the PaperMono
pass — M5Stack mirrors some datasheets only in Chinese.

## Substitutes

| Part | Note |
|---|---|
| **NS4150 / NS4150B** | **analog** input — not a drop-in for an I²S source. This is the ADV's part. |
| MAX98357A | the common Western equivalent: I²S in, class-D out, has a gain/channel-select pin |
| Any I²S class-D amp | check the I²S format (the NS4168 expects standard Philips I²S) and the shutdown-pin polarity |

## Gaps

* Datasheet **retrieved but not mined** — no register map exists to mine (the part has no
  registers), but efficiency, THD+N, supply range, shutdown-pin behaviour and the exact I²S
  format tolerances are not transcribed.
* **No English datasheet located.**
* Whether the part's shutdown pin is tied active or left floating on the Cardputer was **not
  determined** — the v1.x schematic block was not cropped at sufficient resolution in this pass.
