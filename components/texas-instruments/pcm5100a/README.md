# Texas Instruments PCM5100A

- **Category:** 2-channel 32-bit / 384 kHz audio DAC with integrated BCK-referenced PLL and 2.1 V\_RMS ground-centred line outputs
- **Research status:** verified against the board schematic (pin by pin), both vendor example trees, and the TI datasheet retrieved into `artifacts/`
- **Retrieved:** 2026-08-21

`U12` on the [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md), marked **`PCM5100APWR`** on the schematic. It is the board's only audio output device, and it is a **line-level** DAC, not an amplifier.

The single most consequential fact about it on this board: **it has no control bus.** Every configuration decision — audio format, filter, de-emphasis, clock mode — is a hardwired pin strap you cannot change in firmware. The only runtime control is a single mute line, `XSMT`, and that line is owned by the *other* MCU. See §4.2 and §7.1.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[SCH]** | Read directly off the board schematic PNGs in `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/` |
| **[DOC]** | Stated by TI in `artifacts/pcm5100a-datasheet.pdf` (SLAS859C, May 2015) |
| **[SRC]** | Read out of Waveshare's own example source in the device's `artifacts/demo/` tree |
| **[INF]** | Inference. Not established by the above |
| **[WEB]** | Non-TI web source, dated at retrieval |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Marked part | **`PCM5100APWR`** | **[SCH]** sheet `5_DAC.png`, symbol name on `U12` |
| Reference designator | **U12** | **[SCH]** |
| Package | **TSSOP-20** (`PW`), 5.50 × 4.40 mm body, 0.65 mm pitch | **[DOC]** device-comparison table; `PW` is TI's TSSOP code |
| Suffix `R` | **Tape-and-reel** packing (2000 pcs); `PWT` would be the 250-pc reel | **[DOC]** TI packaging convention |
| Datasheet | **SLAS859C**, "PCM510xA 2.1 V\_RMS, 112/106/100 dB Audio Stereo DAC with PLL and 32-bit, 384 kHz PCM Interface", May 2012, revised **May 2015** | **[DOC]** |
| Lifecycle | Active. Long-standing TI production part | **[WEB]** ti.com product page, 2026-08-21 |
| Control interface | **None.** Hardware-pin control only — §1.2 | **[DOC]** |

### 1.1 ⚠ The `A` matters, and so does the last digit

Three orthogonal naming traps.

**Trap 1 — `PCM5100` vs `PCM5100A`.** The `A` is not cosmetic. The whole datasheet is titled `PCM510xA`, and TI's own revision history records the device number being changed *from* `PCM510x` *to* `PCM510xA` **[DOC]**. Treat non-`A` documentation as stale.

**Trap 2 — the family's three grades.** `PCM5100A`, `PCM5101A` and `PCM5102A` share the **same TSSOP-20 pinout and the same pin straps**, differing only in tested audio performance **[DOC]**:

| Part | Dynamic range | SNR | THD+N at −1 dBFS |
|---|---:|---:|---:|
| PCM5102A | 112 dB | 112 dB | −93 dB |
| PCM5101A | 106 dB | 106 dB | −92 dB |
| **PCM5100A** | **100 dB** | **100 dB** | **−90 dB** |

**This board has the lowest grade of the three.** A defensible choice for a line-out on a battery-powered knob, but it means anyone comparing this board to the ubiquitous "PCM5102A I2S DAC" breakout modules is comparing against a 12 dB better part. `-Q1` automotive variants of all three also exist; not relevant here.

**Trap 3 — PCM5100A is not PCM5122 / PCM5142 / PCM5242.** Those *do* have I²C or SPI control ports, on-chip miniDSP, digital volume and configurable clocking. The `510xA` line deliberately has none of it. If you find a "PCM51xx register map", it is for a different part and does not apply here.

### 1.2 What "no control bus" costs you

**[DOC]** There is no I²C address, no SPI port, no register map, and no software volume control. Consequences:

- **Volume must be done in the digital samples.** Waveshare's example does exactly that — it scales `int16_t` samples by a float factor before writing to I²S **[SRC]** (`audio_bsp.c`, `bsp_i2s_write()`). At low volumes this throws away bits: at a factor of 0.1 you have lost ~3.3 bits of the 16 you had. Prefer to keep the DAC near full scale and attenuate downstream, or use a wider sample width.
- **No de-emphasis control, no filter switching, no soft-ramp configuration at runtime.** All strapped — §4.2.
- **No way to read status.** There is no "PLL locked" or "clock error" flag to poll. Failures are silent.

---

## 2. Key electrical and audio specifications

**[DOC]** from `artifacts/pcm5100a-datasheet.pdf`.

| Parameter | Value | Note for this board |
|---|---|---|
| Full-scale output | **2.1 V\_RMS single-ended, ground-centred** | ≈ 5.9 V peak-to-peak. Hot for a line output; will clip inputs that expect 1 V\_RMS **[INF]** |
| Output topology | **Ground-centred** — no DC blocking capacitors and no external muting circuit required | The `510xA` line's headline feature **[DOC]**. The board correspondingly fits **no** series output capacitors on `OUTL`/`OUTR` **[SCH]** |
| Dynamic range / SNR | 100 dB (this grade) | §1.1 |
| THD+N at −1 dBFS | −90 dB typ, −80 dB max at fS = 48 kHz | |
| PCM word length | up to 32-bit | Board firmware uses 16-bit **[SRC]** |
| Sample rate | up to 384 kHz | Board firmware uses 44.1 kHz **[SRC]** |
| `fSCK` (system clock) | 512, 768, 1024, 1152, 1536, 2048 × fS, up to **50 MHz** | **Not supplied on this board** — §5 |
| Supply | `AVDD`/`CPVDD` 3.3 V analog, `DVDD` 1.8 V or 3.3 V digital | Board runs **both at 3.3 V** from `3V3_DAC` **[SCH]** |
| Charge pump | Internal, generating the negative rail for ground-centred output | Needs `CAPP`/`CAPM` flying cap and `VNEG` reservoir — §4.1 |
| `XSMT` mute time | 150 × tS + 0.2 ms (soft digital ramp then hard analog mute) | ≈ **3.6 ms at 44.1 kHz**. §7.2 |
| `XSMT` edge rates | tr, tf ≤ 20 ns | A slow or floating edge is out of spec |
| Auto-mute on clock error | Yes — switches to an internal oscillator, ramps down from the last value, then hard-mutes to ground | This is the "click" you hear if the CH445P mux is switched live **[DOC]** §11.2 |

### 2.1 What it is *not*

- **Not a headphone amplifier.** It drives a line-level load; TI's recommendation is a high-impedance line input. It will "work" into 32 Ω headphones only in the sense that you will hear something quiet and distorted. **[INF]**
- **Not a speaker amplifier.** The board contains no speaker and no amplifier.
- **Not a codec.** There is no ADC. The board's microphone is a separate [PDM MEMS device](../../memsensing/msm261d4030h1cpm/README.md) going straight into the S3.

**Documentation for this board should say "3.5 mm stereo *line* output".** See [3.5 mm audio output](../../generic/3.5mm-audio-output/README.md).

---

## 3. Pinout

**[DOC]** pin table, cross-checked against **[SCH]**.

| Pin | Name | Type | Function |
|---:|---|---|---|
| 1 | `CPVDD` | Power | Charge-pump supply |
| 2 | `CAPP` | Analog | Charge-pump flying-capacitor + |
| 3 | `CPGND` | Power | Charge-pump ground |
| 4 | `CAPM` | Analog | Charge-pump flying-capacitor − |
| 5 | `VNEG` | Analog | Charge-pump negative-rail reservoir |
| 6 | `OUTL` | Analog out | Left line output, ground-centred |
| 7 | `OUTR` | Analog out | Right line output, ground-centred |
| 8 | `AVDD` | Power | Analog supply |
| 9 | `AGND` | Power | Analog ground |
| 10 | `DEMP` | Digital in | 44.1 kHz de-emphasis: **Off (low)** / On (high) |
| 11 | `FLT` | Digital in | Interpolation filter: **Normal latency (low)** / Low latency (high) |
| 12 | `SCK` | Digital in | System clock input |
| 13 | `BCK` | Digital in | Bit clock |
| 14 | `DIN` | Digital in | Serial audio data |
| 15 | `LRCK` | Digital in | Word select / frame clock |
| 16 | `FMT` | Digital in | Audio format: **I²S (low)** / Left-justified (high) |
| 17 | `XSMT` | Digital in | Soft mute: **Mute (low)** / Un-mute (high) |
| 18 | `LDOO` | Power | Internal LDO output — decouple only, do not load |
| 19 | `DGND` | Power | Digital ground |
| 20 | `DVDD` | Power | Digital supply, 1.8 V or 3.3 V |

---

## 4. Exact wiring on this board

**[SCH]** sheet `5_DAC.png`, read at magnification.

### 4.1 Power and analog

| Pin | Net | Passives |
|---:|---|---|
| 1 `CPVDD` | `A3V3` | |
| 2 `CAPP` ↔ 4 `CAPM` | — | **`C64` 2.2 µF** flying capacitor |
| 3 `CPGND` | `AGND` | |
| 5 `VNEG` | — | **`C65` 2.2 µF** to `AGND` |
| 6 `OUTL` | `OUTL` | **No series capacitor** → 3.5 mm jack, and to connector `CN1` |
| 7 `OUTR` | `OUTR` | **No series capacitor** → 3.5 mm jack, and to `CN1` |
| 8 `AVDD` | `A3V3` | `C40` 10 µF ∥ `C39` 100 nF |
| 9 `AGND` | `AGND` | Sheet aliases `AGND` → `GND` |
| 18 `LDOO` | — | `C38` 100 nF to GND |
| 19 `DGND` | GND | |
| 20 `DVDD` | `3V3_DAC` | `C37` 100 nF |

`A3V3` is aliased to `3V3_DAC` on the same sheet **[SCH]**, so analog and digital both come from the **SGM2036-3.3 LDO `U20`**, itself fed from **5 V** through ferrite `L8` (`BLM18AG102SN1D`) with `C62` 1 µF in and `C66` 1 µF / `C101` 10 nF out. A dedicated low-noise LDO for the DAC is the right call and worth noting: DAC noise performance does not depend on the switching regulator that runs the rest of the board.

> **⚠ The DAC's supply comes from the 5 V rail, not the main 3V3 rail.** Whether `3V3_DAC` is present on battery-only power depends on the unresolved [charger/power-path](../../generic/charger-power-path/README.md) topology. If it is not, there is no audio at all — and the CH445P mux is unpowered too. **[INF]**

### 4.2 The strapped configuration pins — this is the board's audio personality

All four are hardwired. **You cannot change any of them in firmware.**

| Pin | Strap | Meaning | Evidence |
|---:|---|---|---|
| 10 `DEMP` | **→ AGND (low)** | **De-emphasis OFF** | **[SCH]** sheet-5 alias block shows `DEMP ─ AGND` |
| 11 `FLT` | **→ GND (low)** | **Normal-latency interpolation filter** (the higher-quality, higher-group-delay option) | **[SCH]** ground symbol on pin 11 |
| 12 `SCK` | **→ GND (low)** | **No external system clock ⇒ the internal BCK-referenced PLL is used.** The single most important strap — §5 | **[SCH]** |
| 16 `FMT` | **→ GND (low)** | **I²S (Philips) format**, not left-justified | **[SCH]** ground symbol on pin 16 |

### 4.3 The audio bus

| Pin | Net | Source |
|---:|---|---|
| 13 `BCK` | `I2S_DAC_BCK` | ← CH445P `U18` pin 2 (`DA`) |
| 14 `DIN` | `I2S_DAC_DIN` | ← CH445P pin 5 (`DB`) |
| 15 `LRCK` | `I2S_DAC_LRCK/WS` | ← CH445P pin 7 (`DC`) |
| 17 `XSMT` | `XSMT` | ← **ESP32-U4WDH GPIO32 directly** — *not* through the mux |

Which MCU is on the other side of the mux is set by [CH445P](../../wch/ch445p/README.md): `IN` high ⇒ ESP32-S3 (GPIO39/40/41), `IN` low ⇒ ESP32-U4WDH (GPIO25/27/26).

---

## 5. ⚠ There is no MCLK. The PLL is mandatory, and it constrains your sample rates.

CH445P channel D — the one that would have carried a master clock — is **completely unconnected** on all three of `S1D`, `S2D`, `DD` **[SCH]**. Combined with `SCK` strapped to ground, this puts the DAC permanently in TI's **"Clock Slave Mode with BCK PLL to Generate Internal Clocks (3-Wire PCM)"** **[DOC]** §9.3.5.3.

How it works, quoting the datasheet:

> The device starts up expecting an external SCK input, but if BCK and LRCK start correctly while SCK remains at ground level **for 16 successive LRCK periods**, then the internal PLL starts, automatically generating an internal SCK from the BCK reference.

Two things follow that you must design around.

### 5.1 The 16-LRCK settling requirement

After any event that stops the clocks — power-up, an I²S channel restart, a mux switch — **BCK and LRCK must run cleanly for at least 16 LRCK periods before audio is valid.** At 44.1 kHz that is ~363 µs. In practice: start the I²S channel, wait a few milliseconds, *then* un-mute. §7.2.

### 5.2 ⚠ Not every sample rate works. Table 11 is a hard constraint.

**[DOC]** Table 11, "BCK Rates (MHz) by LRCK Sample Rate for PCM510xA PLL Operation". A dash means **the PLL cannot generate a valid clock at that combination**.

| Sample rate (kHz) | BCK at 32 fS | BCK at 64 fS |
|---:|---:|---:|
| **8** | **—** | **—** |
| 16 | — | 1.024 MHz |
| 32 | 1.024 MHz | 2.048 MHz |
| **44.1** | **1.4112 MHz** | 2.8224 MHz |
| 48 | 1.536 MHz | 3.072 MHz |
| 96 | 3.072 MHz | 6.144 MHz |
| 192 | 6.144 MHz | 12.288 MHz |
| 384 | 12.288 MHz | 24.576 MHz |

**Practical rules for this board:**

- **8 kHz is unusable.** Both columns are dashed. If you are building a voice application and reach for 8 kHz out of habit, you will get silence or noise and **no error message**. Use 16 kHz at 64 fS, or resample to 44.1/48 kHz.
- **16 kHz requires 64 fS** — i.e. 32-bit slots, or 16-bit *stereo*. 16-bit mono at 16 kHz gives 32 fS, which is dashed.
- **Waveshare's example lands exactly on a valid entry.** It uses 44.1 kHz, 16-bit, `I2S_SLOT_MODE_MONO` **[SRC]**. ESP-IDF's standard mode still emits two slots (WS toggles), so BCK = 2 × 16 × 44 100 = **1.4112 MHz = 32 fS** — the 44.1 kHz / 32 fS cell. It works because it happens to be right, not because anything checks.
- **Changing bit depth changes BCK.** Going from 16-bit to 24-bit at 44.1 kHz gives 48 fS, which **is not in the table at all**. 32-bit gives 64 fS, which is valid. Verify against Table 11 before touching `I2S_DATA_BIT_WIDTH_*`.

---

## 6. Firmware: which driver, and what the vendor actually ships

Because the DAC has no control bus, "the driver" is just the MCU's I²S peripheral. **There is no PCM5100A component or library to install for either framework**, and you should be suspicious of anything claiming to be one.

### 6.1 ESP-IDF

Use the **`i2s_std`** driver from ESP-IDF ≥ 5.0 (`driver/i2s_std.h`). The legacy `driver/i2s.h` API is deprecated and should not be used in new work.

~~~c
#include "driver/i2s_std.h"

#define PIN_BCLK  GPIO_NUM_39      // S3 side of the CH445P mux
#define PIN_WS    GPIO_NUM_40
#define PIN_DOUT  GPIO_NUM_41

i2s_chan_handle_t tx;
i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_1, I2S_ROLE_MASTER);
ESP_ERROR_CHECK(i2s_new_channel(&chan_cfg, &tx, NULL));

i2s_std_config_t std_cfg = {
    .clk_cfg  = I2S_STD_CLK_DEFAULT_CONFIG(44100),
    // FMT is strapped LOW = I2S/Philips  ->  use the PHILIPS slot config.  See 6.3.
    .slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT,
                                                    I2S_SLOT_MODE_STEREO),
    .gpio_cfg = {
        .mclk = I2S_GPIO_UNUSED,   // MANDATORY: there is no MCLK path on this board (§5)
        .bclk = PIN_BCLK,
        .ws   = PIN_WS,
        .dout = PIN_DOUT,
        .din  = I2S_GPIO_UNUSED,
        .invert_flags = { false, false, false },
    },
};
ESP_ERROR_CHECK(i2s_channel_init_std_mode(tx, &std_cfg));
ESP_ERROR_CHECK(i2s_channel_enable(tx));
~~~

**Do not configure an MCLK pin.** There is no route for it, and assigning one wastes a GPIO on a signal that goes nowhere.

Remember also to drive the mux: `gpio_set_level(GPIO_NUM_0, 1)` to claim the DAC for the S3. See [CH445P §6](../../wch/ch445p/README.md).

### 6.2 Arduino

Arduino-ESP32 core **3.x** exposes the same underlying driver through the `I2S` class (`#include <ESP_I2S.h>`); or call the IDF `i2s_std` API directly, which is what Waveshare's own Arduino example does — it `#include`s `driver/i2s_std.h` from a `.c` file inside the sketch folder **[SRC]**. On core **2.x** the older `i2s.h` API is what you get.

For file playback, the usual community routes are **[ESP32-audioI2S](https://github.com/schreibfaul1/ESP32-audioI2S)** (`audio.setPinout(bclk, lrc, dout)`; leave MCLK unset) or **ESP8266Audio**'s `AudioOutputI2S`. Neither needs PCM5100A-specific code. **[WEB]**, retrieved 2026-08-21.

### 6.3 ⚠ What the vendor demo actually does, and one discrepancy worth knowing

`artifacts/demo/…/07_Audio_Test/audio_bsp.c` and `user_config.h` **[SRC]**:

| Setting | Vendor value | Comment |
|---|---|---|
| Sample rate | 44 100 Hz | ✅ Valid Table 11 entry (§5.2) |
| Bit width | `I2S_DATA_BIT_WIDTH_16BIT` | ✅ |
| Channel | `I2S_SLOT_MODE_MONO` | Still 2 slots on the wire |
| MCLK | `I2S_GPIO_UNUSED` | ✅ Correct — no MCLK exists |
| Controller | `I2S_NUM_1` for TX, `I2S_NUM_0` for the PDM microphone | Sensible split |
| Pins | BCLK 39, WS 40, DOUT 41 | ✅ Matches **[SCH]** |
| Mux | `gpio_set_level(GPIO_NUM_0, 1)` | ✅ Claims the DAC for the S3 |
| `XSMT` | **never touched** | The S3 physically cannot — §7.1 |
| Volume | Digital scaling of `int16_t` by `volume/100.0f`, default 10, max 50 | §1.2 |
| Slot config | **`I2S_STD_MSB_SLOT_DEFAULT_CONFIG(...)`** | ⚠ **See below** |

> **⚠ Format discrepancy.** The board straps `FMT` **low**, which selects **I²S (Philips)** format **[DOC]** — data delayed by one BCK after the WS edge. The vendor example configures the ESP32 with **`I2S_STD_MSB_SLOT_DEFAULT_CONFIG`**, which is **MSB-aligned / left-justified** — data starting *on* the WS edge, with no one-bit delay. These two do not agree; the DAC will latch each word shifted by one bit position relative to what the MCU intended.
>
> The mismatch is **[SRC]** + **[DOC]** as a fact. What it *sounds like* is **[INF]**: a one-bit shift of a 16-bit two's-complement word should not be subtle in theory, but the practical result depends on how the serial shifter treats the trailing bit and on signal level. Waveshare ships it and presumably tested it. **If your audio sounds distorted, harsh, or has a noise floor that scales with signal level, change to `I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG` first** — it is a one-line change and it is what the hardware strap asks for. Please record the outcome here if you test it on real hardware.

---

## 7. Initialization order, gotchas and pitfalls

### 7.1 ⚠ The `XSMT` ownership trap — read this before you erase anything

`XSMT` (pin 17) is driven by **ESP32-U4WDH GPIO32 and nothing else**. **No ESP32-S3 pin touches this net, and no pull-up or pull-down resistor is fitted** **[SCH]**.

`XSMT` low = muted. **[DOC]** specifies no internal pull on this pin.

Therefore, if the ESP32-U4WDH is held in reset, unprogrammed, erased, or simply running firmware that never configures GPIO32, **`XSMT` floats** and the DAC's mute state is indeterminate. **[INF]**

Practical implications:

- **The S3 alone cannot guarantee audio output.** Every S3-side audio example implicitly depends on the factory U4WDH firmware having driven GPIO32 high.
- **If you flash your own firmware to the ESP32-U4WDH, drive GPIO32 high early**, or you will silently break audio for the S3 side too.
- **"I erased the ESP32 and now there's no sound"** is a predictable failure mode on this board. It is not the S3's fault.
- GPIO32 is the U4WDH's `32K_XP` pad, repurposed because no 32.768 kHz crystal is fitted **[SCH]**. It is a plain GPIO at reset (input, high-Z), which is exactly why it floats.

Minimal U4WDH-side code:

~~~c
#define PCM5100A_XSMT  GPIO_NUM_32     // ESP32-U4WDH only; no other pin reaches this net

gpio_config_t c = { .pin_bit_mask = 1ULL << PCM5100A_XSMT,
                    .mode = GPIO_MODE_OUTPUT };
gpio_config(&c);
gpio_set_level(PCM5100A_XSMT, 0);      // start muted -- see the sequence in 7.2
~~~

### 7.2 The correct bring-up and mute sequence

**[INF]** derived from the two datasheets; no shipped firmware performs a full sequence.

1. Bring up `3V3_DAC`. Hold `XSMT` **low** while the rails settle. (TI's §11.2 "Planned Shutdown" advice is the mirror image: assert `XSMT` low **150 tS + 0.2 ms** *before* removing power, or you may get a pop.)
2. ESP32-S3 sets the CH445P mux (`GPIO0`) to the intended source.
3. Source MCU starts its I²S channel so BCK and LRCK run.
4. **Wait ≥ 16 LRCK periods** for the internal PLL to lock (§5.1). A few milliseconds is comfortably enough.
5. ESP32-U4WDH drives `XSMT` **high**. Audio is live.

To go the other way (mute → switch source → un-mute), see [CH445P §7.2](../../wch/ch445p/README.md); the two records describe the same handover from opposite ends.

### 7.3 Pitfalls, ranked by how likely you are to hit them

1. **No sound because `XSMT` is floating.** §7.1. By far the most likely.
2. **No sound because the mux points at the other MCU.** `gpio_set_level(GPIO_NUM_0, 1)`. See [CH445P](../../wch/ch445p/README.md).
3. **Configuring an MCLK pin.** There is no MCLK on this board (§5). ESP-IDF will happily emit it on a GPIO that goes nowhere, and you will chase the wrong problem.
4. **Choosing 8 kHz.** The PLL cannot lock. §5.2.
5. **Expecting headphone drive.** It is a 2.1 V\_RMS line output with no power amplifier. §2.1.
6. **Clipping the downstream input.** 2.1 V\_RMS is well above the 0.316 V\_RMS (−10 dBV) consumer line convention and above the 1.0 V\_RMS many devices expect. If the receiving device distorts, attenuate — digitally or with a resistive pad. **[INF]**
7. **Switching the mux while unmuted.** Clock error → auto-mute-to-ground → audible click. §7.2 and **[DOC]** §11.2.
8. **Reaching for a register map.** There isn't one. §1.2.
9. **Digital volume scaling at low levels.** Loses resolution. §1.2.
10. **Assuming `DEMP` is on.** It is strapped off. Only matters for pre-emphasised 44.1 kHz material, which in practice means some very old CD masters. **[SCH]**
11. **Assuming the two ESP32s can both drive I²S simultaneously.** They cannot — the mux is exclusive. Driving both is harmless electrically (the unselected bank is open) but only one is heard.

---

## 8. Alternatives and drop-in compatibility

| Part | Relationship | Drop-in for `U12`? |
|---|---|---|
| **PCM5101A** | Same family, 106 dB | ✅ **Pin-, footprint- and strap-compatible.** A straight upgrade |
| **PCM5102A** | Same family, 112 dB | ✅ Same. The best drop-in upgrade available |
| PCM5100A-Q1 / 5101A-Q1 / 5102A-Q1 | Automotive-qualified versions | ✅ Pin-compatible |
| PCM5100 (no `A`) | Predecessor | ⚠ Superseded; do not design in. §1.1 |
| **PCM5121 / PCM5122 / PCM5142 / PCM5242** | Same output stage **plus** I²C/SPI control, miniDSP, digital volume | ❌ **Not drop-in.** Different packages and pinouts, and they need control-bus wiring this board does not have |
| **ES9018K2M / ES9023** | Everest DACs, common in audiophile modules | ❌ Different pinout and clocking requirements |
| **UDA1334A** | Cheap I²S DAC, also MCLK-optional | ❌ Different package/pinout; markedly worse |
| **MAX98357A** | I²S **class-D amplifier** | ❌ Different *function* — drives a speaker directly. Listed because it is the part most often confused with a line-out DAC |

**Bottom line:** if you are respinning this board and want better audio for near-zero effort, fit a **PCM5102A**. Everything else — straps, passives, layout — stays identical.

---

## 9. Open questions

| Question | Status |
|---|---|
| Does the `FMT`-low / MSB-slot mismatch (§6.3) produce audible degradation? | **Open.** Needs a real listening or loopback test. One-line fix if so |
| Is `3V3_DAC` present on battery-only power? | **Open.** Depends on the [charger/power-path](../../generic/charger-power-path/README.md) topology |
| Does the factory U4WDH firmware drive `XSMT` high at boot, or only when a stream starts? | **Open.** Determines whether S3-side audio works out of the box on a virgin board |
| Is there attenuation between `OUTL/OUTR` and the 3.5 mm jack? | **Resolved [SCH]:** direct connection, no series capacitors, no divider. Full 2.1 V\_RMS at the jack |
| Fitted lot / date code | **Open.** Not readable from any published image |

---

## Manufacturer

**Texas Instruments** — see the [Texas Instruments documentation-sourcing guide](../../../vendors/texas-instruments/README.md) for this vendor's document portals, URL patterns, part-numbering conventions, distribution channels and known gotchas.

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — reference designator **`U12`**, marked `PCM5100APWR`. Fed through the [CH445P mux](../../wch/ch445p/README.md) from either MCU; muted by the ESP32-U4WDH alone. See [Pinouts and buses § Audio arbitration](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md).

## Related components

- [WCH CH445P](../../wch/ch445p/README.md) — the input mux; documents the handover sequence from the other side
- [SGMicro SGM2036-3.3](../../sgmicro/sgm2036-3.3/README.md) — the dedicated low-noise LDO feeding `A3V3`/`3V3_DAC`
- [3.5 mm stereo line output](../../generic/3.5mm-audio-output/README.md) — where `OUTL`/`OUTR` terminate
- [Espressif ESP32-U4WDH](../../espressif/esp32-u4wdh/README.md) — owner of `XSMT`
- [Espressif ESP32-S3R8](../../espressif/esp32-s3r8/README.md) — owner of the mux select

---

## Local artifacts and document revisions held

Two copies of the PCM510xA datasheet are held. They are **the same revision in two languages**,
not two revisions — a point an earlier note in this repository got wrong.

| Document | TI literature no. | Language | Date band | Source | Local path | Bytes | SHA-256 |
|---|---|---|---|---|---|---:|---|
| PCM510xA datasheet | **`SLAS859C`** | English | MAY 2012 – REVISED MAY 2015 | TI direct, `ti.com/lit/gpn/PCM5100A` | `artifacts/pcm5100a-datasheet.pdf` | 1,195,126 | `a5220836…` |
| PCM510xA datasheet | `ZHCSA60C` | **Chinese (简体中文)** | MAY 2012 – REVISED MAY 2015 | Waveshare mirror, `files.waveshare.com/wiki/common/Pcm5100a.pdf` | `artifacts/pcm5100a-datasheet-zhcsa60c-zh-waveshare-mirror.pdf` | 1,453,455 | `9822f33d…` |

**Which applies to the fitted part?** Both describe the same silicon at the same revision level —
the trailing `C` matches in both literature numbers, and the revision date band is identical
(*REVISED MAY 2015*). The board fits a **PCM5100A**, covered by both. **Use the English
`SLAS859C`** as the working reference; the Chinese copy is retained because it is what Waveshare
distributes and because TI's translated documents are occasionally withdrawn without an English
equivalent being updated.

> ⚠ **Correction to earlier analysis.** The Waveshare file was previously recorded in this
> repository as literature number `SLAS859` — i.e. an *older, pre-`C`* English revision. That was
> wrong. `pdftotext` on page 1 returns `ZHCSA60C – MAY 2012 – REVISED MAY 2015` with a Chinese
> title block. `ZHCS…` is TI's prefix for Chinese-language translations; the document is neither
> English nor an older revision. The `SLAS859` string that produced the earlier reading appears
> elsewhere in the file as a cross-reference, not as the document's own identifier.

Verified 2026-08-24 by `sha256sum` and
`nix-shell -p poppler-utils --run 'pdftotext -f 1 -l 1 <file> -'`.

The Chinese copy was relocated here on 2026-08-24 from
`devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/datasheets/Pcm5100a.pdf`, so that
component documentation lives in the component record.

### Reacquire

```bash
# English, revision-pinned
curl -L -o pcm5100a-slas859c.pdf https://www.ti.com/lit/ds/slas859c/slas859c.pdf
# English, always-latest revision
curl -L -o pcm5100a.pdf          https://www.ti.com/lit/ds/symlink/pcm5100a.pdf
# Chinese, revision-pinned
curl -L -o pcm5100a-zhcsa60c.pdf https://www.ti.com/lit/ds/zhcsa60c/zhcsa60c.pdf
# The Waveshare mirror this copy came from
curl -L -o Pcm5100a.pdf          https://files.waveshare.com/wiki/common/Pcm5100a.pdf
```

> TI's `lit/ds/symlink/<part>.pdf` form always serves the **latest** revision and will not
> reproduce the hashes above once TI republishes. The `lit/ds/<litno>/<litno>.pdf` form is
> revision-pinned. Waveshare updates its `/wiki/common/` pool in place.

---

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| **TI PCM510xA datasheet, SLAS859C** (May 2012, rev. May 2015) — pin table, §9.3.5.3 BCK PLL, Table 11 BCK rates, §11.2 mute/powerdown | https://www.ti.com/lit/gpn/PCM5100A | 2026-08-21 | `artifacts/pcm5100a-datasheet.pdf` |
| TI PCM5100A product page (lifecycle, packaging, pricing) | https://www.ti.com/product/PCM5100A | 2026-08-21 | – |
| TI PCM5102A product page (the drop-in upgrade) | https://www.ti.com/product/PCM5102A | 2026-08-21 | – |
| Waveshare mirror — **Chinese translation `ZHCSA60C`**, not an English copy | https://files.waveshare.com/wiki/common/Pcm5100a.pdf | 2026-08-21 | `artifacts/pcm5100a-datasheet-zhcsa60c-zh-waveshare-mirror.pdf` |
| Board schematic archive (sheet `5_DAC.png`) | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` |
| Official demo archive — `07_Audio_Test/audio_bsp.c`, `user_config.h` | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` |
| ESP-IDF I2S standard-mode driver reference | https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32s3/api-reference/peripherals/i2s.html | 2026-08-21 | – |
| Arduino-ESP32 `ESP_I2S` API | https://docs.espressif.com/projects/arduino-esp32/en/latest/api/i2s.html | 2026-08-21 | – |
| ESP32-audioI2S library (community playback stack) | https://github.com/schreibfaul1/ESP32-audioI2S | 2026-08-21 | – |
