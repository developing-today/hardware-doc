# Everest Semiconductor ES8156

> High-performance stereo audio DAC with an integrated headphone driver, I²S/PCM serial port and I²C control. Boots in **hardware mode** and must be told to enter software mode before any register you write has an effect.
> Research snapshot **2026-08-30**. Fitted as `U24` on the Nicolai Electronics Tanmatsu. **No hardware was available.**

---

## Evidence labelling

| Tag | Meaning |
|---|---|
| **[DS]** | Everest Semiconductor ES8156 datasheet, **Revision 13.0, February 2026**, 15 pp — `artifacts/es8156-datasheet.pdf` |
| **[ADF]** | `espressif/esp-adf` v2.7, `components/audio_hal/driver/es8156/es8156.c` / `.h` (ESPRESSIF MIT License, © 2021) |
| **[BSP]** | Badge.Team BSP `targets/tanmatsu/badge_bsp_audio.c` (MIT), snapshot in the device tree |
| **[PCB]** | `tanmatsu.kicad_pcb` pad→net assignments (CERN-OHL-P) |
| **[INF]** | Author inference |

> ⚠ **The datasheet contains no register map.** Revision 13.0 documents the pinout, the I²C *protocol*, clock modes and electrical limits, but the register table is not published — it lives in a separate "user guide" Everest supplies to customers. §4 therefore reconstructs the register map **from driver source**, and every value there is labelled **[ADF]**, not **[DS]**. This is stated plainly rather than presented as datasheet fact.

---

## 1. Identity, package and lifecycle

| Property | Value | Source |
|---|---|---|
| Part | **ES8156** | [DS] |
| Function | **Stereo audio DAC** — playback only. Not a codec in the ADC sense, despite common labelling | [DS] |
| Package | **QFN-20** (Tanmatsu BOM: VQFN-20-1EP, 3 × 3 mm, 0.4 mm pitch, EP 1.7 × 1.7 mm) | [DS], BOM |
| Temperature range | **−40 °C to +125 °C** | [DS] |
| Supply | 1.8 V to 3.3 V operation; three domains — `DVDD`, `PVDD`, `AVDD` | [DS] |
| Absolute max supply | **−0.3 V to +3.6 V**, analog and digital | [DS] |
| Control | **I²C** | [DS] |
| I²C 7-bit address | **`0b0001_00x`** where `x` = the **`CE` pin** ⇒ **`0x08`** (CE low) or **`0x09`** (CE high) | [DS] §6 |
| Datasheet revision | **13.0, February 2026** — recent and actively maintained | [DS] |
| Lifecycle | Active | [INF] |
| LCSC | [`C2887138`](https://www.lcsc.com/search?q=C2887138) | BOM |

### 1.1 Performance **[DS]**

| Parameter | Value |
|---|---|
| SNR | **110 dB** |
| THD+N | **−80 dB** |
| Resolution / sample rate | **24-bit, 8 kHz – 96 kHz** |
| Architecture | Multi-bit delta-sigma |
| Output | **Differential** (for higher SNR and CMRR), or single-ended |
| Headphone driver | Integrated, with a **capless option** via `HPCOM` |
| DSP features | **7-band fully adjustable EQ**, dynamic range compression, automute, pop/click suppression |
| Serial port | I²S / PCM, **master or slave** |
| Clocking | 256/384 Fs, **USB 12/24 MHz**, and non-standard system clocks |

### 1.2 ⚠ The address is `0x08`, `0x09`, `0x10` or `0x11` depending on who is counting

This trips people constantly. The datasheet gives the address as the 7-bit pattern `0001 00x`:

| CE pin | 7-bit address | 8-bit write | 8-bit read |
|---|---|---|---|
| **Low (GND)** | **`0x08`** | `0x10` | `0x11` |
| High (supply) | `0x09` | `0x12` | `0x13` |

- The Tanmatsu documentation says **`0x08`** — the 7-bit form.
- ESP-ADF's driver says `#define ES8156_ADDR 0x10` **[ADF]** `es8156.c:33` — the 8-bit form.

**These are the same address.** If a bus scan finds a device at 0x08 and your driver is configured for 0x10, check whether the library expects 7- or 8-bit before changing anything.

---

## 2. Pinout **[DS] §2**

| Pin | Name | Dir | Description |
|---:|---|---|---|
| 1 | `CDATA` | I/O | I²C data (SDA) |
| 2 | `CCLK` | I | I²C clock (SCL) |
| 3 | `MCLK` | I | Master clock |
| 4 | `DVDD` | — | Digital power supply |
| 5 | `PVDD` | — | Power supply for the digital input/output |
| 6 | `DGND` | — | Digital ground |
| 7 | `SCLK` | I/O | Serial data bit clock / DMIC bit clock |
| 8 | `SDIN` | I | **DAC serial data input** |
| 9 | `LRCK` | I/O | Left/right frame clock |
| 10 | `HPCOM` | Analog | **Virtual ground for capless headphone — software mode only** |
| 11, 12 | `ROUTP`, `ROUTN` | O | Right channel differential output |
| 13 | `AGND` | — | Analog ground |
| 14, 15 | `LOUTN`, `LOUTP` | O | Left channel differential output |
| 16 | `AVDD` | — | Analog power supply |
| 17 | `VRP` | Analog | Filtering capacitor connection |
| 18 | `VMID` | Analog | Filtering capacitor connection |
| **19** | **`CE`** | I | **I²C address select** — see §1.2 |
| 20 | `SDOUT` | O | Playback signal feedback |

> ⚠ **`HPCOM` (capless headphone virtual ground) is "Only available in software mode"** **[DS] §2**. A board that relies on capless output *must* switch the chip to software mode; in hardware mode that pin does nothing and the output is silent or DC-offset.

---

## 3. Hardware mode vs software mode — the first real gotcha **[DS] §4**

> **"The device works either in hardware mode (HW mode) or software mode (I²C mode). The default is hardware mode. Software mode is enabled by setting bit 2 of configuration register `0x02`."** — [DS] §4

This is the single most important sentence in the datasheet.

**In hardware mode (the power-on default):**
- `LRCK` and `SCLK` must be supplied externally and derived synchronously from the system clock.
- The chip **auto-detects the MCLK/LRCK ratio** from a fixed list (§3.1).
- Volume, EQ, mute, ALC and the capless `HPCOM` function are **unavailable**.

**In software mode**, everything is register-controlled, master or slave clocking is available, and the full feature set unlocks.

⚠ **Every register write you make before setting `REG02` bit 2 configures a chip that is not listening in the way you think.** A driver that writes its whole init table without first entering software mode produces a DAC that plays audio (because hardware mode works) at a volume it cannot change. That is exactly the "sound works but volume control does nothing" symptom.

ESP-ADF's `es8156_codec_init()` does it correctly, writing `0x02 = 0x04` — **bit 2 set** — as one of the very first operations **[ADF]** `es8156.c:150`.

### 3.1 Clocking **[DS] §4, §5, Table 1**

**Hardware/slave mode** — the *only* supported MCLK/LRCK ratios, single speed, Fs 8 kHz – 50 kHz:

> **32, 64, 96, 128, 192, 256, 384, 512, 640, 768, 1024, 1152, 1280, 1536**

`SCLK/LRCK` is normally **64**. Anything not on that list will not lock.

**Software mode** additionally supports standard audio clocks (32/64/128/256/384/512 Fs), **USB clocks (12 / 24 MHz)** and common non-standard clocks (16 MHz, 25 MHz, 26 MHz).

**Speed modes:** single speed Fs 8–48 kHz; double speed Fs 64–96 kHz.

**Master vs slave:** in slave mode `LRCK`/`SCLK` come from outside and must be synchronous with `MCLK`. In master mode both are derived internally from `MCLK`.

---

## 4. Register map — reconstructed from driver source

**Not from the datasheet.** Revision 13.0 documents the I²C access protocol but omits the register table. The map below is transcribed from ESP-ADF's `es8156.h` **[ADF]**, which is MIT-licensed and is the most complete public description of this chip's registers that exists.

| Addr | Name **[ADF]** | Group |
|---|---|---|
| `0x00` | `RESET_REG00` | **Reset control** |
| `0x01` | `MAINCLOCK_CTL_REG01` | Clock management |
| **`0x02`** | **`SCLK_MODE_REG02`** | **Clock management — bit 2 selects software mode** (§3) |
| `0x03` | `LRCLK_DIV_H_REG03` | Clock management |
| `0x04` | `LRCLK_DIV_L_REG04` | Clock management |
| `0x05` | `SCLK_DIV_REG05` | Clock management |
| `0x06` | `NFS_CONFIG_REG06` | Clock management |
| `0x07` | `MISC_CONTROL1_REG07` | Clock management |
| **`0x08`** | **`CLOCK_ON_OFF_REG08`** | Clock management — clock gating |
| `0x09` | `MISC_CONTROL2_REG09` | Clock management |
| `0x0A` | `TIME_CONTROL1_REG0A` | Clock management |
| `0x0B` | `TIME_CONTROL2_REG0B` | Clock management |
| `0x0C` | `CHIP_STATUS_REG0C` | System control |
| `0x0D` | `P2S_CONTROL_REG0D` | System control |
| `0x10` | `DAC_OSR_COUNTER_REG10` | System control |
| **`0x11`** | **`DAC_SDP_REG11`** | **SDP control — I²S format / word length** |
| `0x12` | `AUTOMUTE_SET_REG12` | SDP control |
| **`0x13`** | **`DAC_MUTE_REG13`** | **SDP control — mute** |
| **`0x14`** | **`VOLUME_CONTROL_REG14`** | **SDP control — digital volume** (§4.1) |
| `0x15` | `ALC_CONFIG1_REG15` | ALC |
| `0x16` | `ALC_CONFIG2_REG16` | ALC |
| `0x17` | `ALC_CONFIG3_REG17` | ALC |
| `0x18` | `MISC_CONTROL3_REG18` | ALC |
| `0x19` | `EQ_CONTROL1_REG19` | EQ |
| `0x1A` | `EQ_CONTROL2_REG1A` | EQ |
| `0x20` | `ANALOG_SYS1_REG20` | **Analog system control** |
| `0x21` | `ANALOG_SYS2_REG21` | Analog system control |
| `0x22` | `ANALOG_SYS3_REG22` | Analog system control |
| `0x23` | `ANALOG_SYS4_REG23` | Analog system control |
| `0x24` | `ANALOG_LP_REG24` | Analog low-power |
| `0x25` | `ANALOG_SYS5_REG25` | Analog system control |
| `0xFC` | `I2C_PAGESEL_REGFC` | Chip information — page select |
| **`0xFD`** | **`CHIPID1_REGFD`** | **Chip ID high** |
| **`0xFE`** | **`CHIPID0_REGFE`** | **Chip ID low** |
| `0xFF` | `CHIP_VERSION_REGFF` | Chip version |

The expected chip-ID values are not stated in either the datasheet or the ADF driver, which never reads them. That is a real gap: **there is no documented way to positively identify an ES8156 on the bus.** [INF]

### 4.1 `REG14` volume — the actual scale **[ADF]** `es8156.c:38–49`

ESP-ADF's volume descriptor is the only published statement of the scale:

```c
.max_dac_volume   =  32,      // dB
.min_dac_volume   = -95.5,    // dB
.volume_accuracy  =  0.5,     // dB per step
.zero_volume_reg  =  0xBF,    // register value for 0 dB
```

From which:

> **dB = (REG14 − 191) × 0.5**

| REG14 | dB |
|---:|---:|
| `0x00` (0) | **−95.5 dB** (minimum) |
| `0xBF` (191) | **0 dB** (unity) |
| `0xFF` (255) | **+32 dB** (maximum) |

ESP-ADF's init writes `0x14 = 179`, commented `// volume 70%` **[ADF]** `es8156.c:160` — which is **(179 − 191) × 0.5 = −6 dB**. Note that the "70 %" is a percentage of the *register range*, not of amplitude or of perceived loudness. This distinction matters; see §6.1.

### 4.2 ESP-ADF's power-down and power-up sequences **[ADF]**

These are the closest thing to a documented sequencing requirement, and the ordering is deliberate.

**Start-up / init** `es8156.c:150–167`:

```c
es8156_write_reg(0x02, 0x04);   // ENTER SOFTWARE MODE (bit 2) -- must be first
es8156_write_reg(0x20, 0x2A);   // analog system
es8156_write_reg(0x21, 0x3C);
es8156_write_reg(0x22, 0x00);
es8156_write_reg(0x24, 0x07);   // analog low-power
es8156_write_reg(0x23, 0x00);
es8156_write_reg(0x0A, 0x01);   // time control
es8156_write_reg(0x0B, 0x01);
es8156_write_reg(0x11, 0x00);   // SDP: I2S format
es8156_write_reg(0x14, 179);    // volume, -6 dB
es8156_write_reg(0x0D, 0x14);   // P2S control
es8156_write_reg(0x18, 0x00);   // un-mute path
es8156_write_reg(0x08, 0x3F);   // clocks ON
es8156_write_reg(0x00, 0x02);   // reset sequence, step 1
es8156_write_reg(0x00, 0x03);   // reset sequence, step 2
es8156_write_reg(0x25, 0x20);   // analog system 5 -- output enable
```

**Power-down** `es8156.c:102–111` then **power-up** `es8156.c:118–126` are near-mirror images, and the mirroring is the pop-suppression strategy:

```c
/* down */ 0x14=0x00 (mute by volume); 0x19=0x02; 0x21=0x1F; 0x22=0x02;
           0x25=0x21; 0x25=0xA1; 0x18=0x01; 0x09=0x02; 0x09=0x01; 0x08=0x00
/* up   */ 0x08=0x3F; 0x09=0x00; 0x18=0x00; 0x25=0x20; 0x22=0x00;
           0x21=0x3C; 0x19=0x20; 0x14=179
```

Two observations worth keeping:

- **Volume is ramped to zero *first* on the way down and restored *last* on the way up.** That is the pop/click suppression the datasheet advertises, implemented in software rather than by a single register bit.
- **`0x25` is written twice on the way down** (`0x21` then `0xA1`) — a two-stage analog shutdown. Reordering or collapsing these writes is likely to reintroduce the pop. [INF]

---

## 5. Exact wiring on the Tanmatsu **[PCB]**

| Pin | Name | Net | Notes |
|---:|---|---|---|
| 1 | `CDATA` | `INT_SDA` | Internal I²C bus (ESP32-P4 GPIO9) |
| 2 | `CCLK` | `INT_SCL` | Internal I²C bus (ESP32-P4 GPIO10) |
| 3 | `MCLK` | `I2S_MCLK` | Master clock from the P4 |
| 4, 5, 16 | `DVDD`, `PVDD`, `AVDD` | `+3.3V` | All three supplies on one 3.3 V rail |
| 6, 13, 19, 21 | `DGND`, `AGND`, EP | `GNDA` | **Analog ground** — separated from digital `GND` |
| 7 | `SCLK` | `I2S_SCLK` | Bit clock |
| 8 | `SDIN` | `I2S_DATA` | DAC data in |
| 9 | `LRCK` | `I2S_LRCK` | Frame clock |
| 10 | `HPCOM` | `Net-(U24-HPCOM)` | Capless headphone virtual ground — **requires software mode** |
| **11** | **`ROUTP`** | `Net-(U24-ROUTP)` | Right output (positive only) |
| **12** | **`ROUTN`** | **unconnected** | ⚠ see below |
| **14** | **`LOUTN`** | **unconnected** | ⚠ see below |
| **15** | **`LOUTP`** | `Net-(U24-LOUTP)` | Left output (positive only) |
| 17 | `VRP` | `Net-(U24-VRP)` | Filter cap |
| 18 | `VMID` | `Net-(U24-VMID)` | Filter cap |
| 20 | `SDOUT` | `Net-(U24-SDOUT)` | Playback signal feedback |

**Two integration facts follow:**

1. ⚠ **The board uses single-ended output.** `LOUTN` and `ROUTN` are unconnected; only the `P` outputs plus `HPCOM` as a common return are used. The datasheet lists differential output as the route to *"higher SNR and CMRR"* **[DS]**, so this board **deliberately gives that up** in exchange for a capless single-ended headphone drive. Expect the 110 dB SNR figure to be optimistic for this configuration. [INF]
2. **`HPCOM` is in use, which makes software mode mandatory**, not optional — see §3 and [DS] §2.

Because `HPCOM` and the `P` outputs are the audio path, the ES8156 here is a **headphone driver**. The board's speaker path is separate: an **FM8002A** amplifier whose enable is controlled by the **CH32V203 coprocessor**, not by the ES8156 **[BSP]** `badge_bsp_audio.c:97–107`.

The chip shares the internal I²C bus with the coprocessor (0x5F) and the [BMI270](../../bosch-sensortec/bmi270/README.md) (0x68). No conflict at 0x08.

---

## 6. Driver audit — Tanmatsu BSP

The BSP uses a **handle-based ES8156 driver** (`es8156_initialize()` / `es8156_configure()` / `es8156_write_volume_control()` / `es8156_handle_t`) that is *not* the ESP-ADF driver — it is an ESP-IDF component with a different API. The chip-level register semantics are unchanged, so the ADF-derived scale in §4.1 applies.

### 6.1 🔴 The volume mapping discards the top of the range and is linear in decibels

```c
// badge_bsp_audio.c:90
esp_err_t bsp_audio_set_volume(float percentage) {
    float value = 180.0 * (percentage / 100.0);
    return es8156_write_volume_control(codec_handle, value);
}
```

Mapping 0–100 % linearly onto register codes **0–180**, against the scale in §4.1:

| Caller passes | REG14 | Actual gain |
|---:|---:|---:|
| **100 %** | 180 | **−5.5 dB** |
| **90 %** (the BSP's own default, `:81`) | 162 | **−14.5 dB** |
| 75 % | 135 | −28 dB |
| **50 %** | 90 | **−50.5 dB** |
| 25 % | 45 | −73 dB |
| 0 % | 0 | −95.5 dB |

Three distinct problems:

1. **"100 %" is −5.5 dB, not 0 dB.** Register codes 181–255 — unity gain through +32 dB of available digital gain — are **unreachable through this API**. The board permanently forfeits its top 5.5 dB even at maximum.
2. **The scale is linear in register code, and register code is linear in *decibels*.** So the "percentage" is a percentage of a **logarithmic** scale. **50 % gives −50.5 dB**, which is essentially inaudible. Almost all of the usable loudness range is compressed into roughly the top 20 % of the slider. A user dragging a volume control to the middle hears near-silence — a classic and very visible UX defect.
3. **No clamping.** Nothing bounds `percentage` to [0, 100]. A value of 200 computes 360, which on truncation to an 8-bit register wraps to 104 → −43.5 dB — *quieter* than 100 %. Negative percentages behave equally badly.

**Consequence:** live and user-visible on every Tanmatsu. Default volume is −14.5 dB.

**Fix:** map percentage to decibels perceptually rather than linearly, and use the full range. A conventional approach is `dB = min_dB + (max_dB − min_dB) × (pct/100)^γ` with γ ≈ 2–3, or a straightforward `REG14 = 191` at 100 % with a taper below. Clamp the input either way.

### 6.2 🟠 `bsp_audio_get_volume()` is unimplemented

```c
// badge_bsp_audio.c:87
esp_err_t bsp_audio_get_volume(float* out_percentage) {
    return ESP_ERR_NOT_SUPPORTED;
}
```

`REG14` is readable over I²C, so this is an omission rather than a hardware limitation. Any UI must shadow the value it last set, and cannot recover after a codec reset. Combined with §6.1 the two mean the volume state is neither correct nor observable.

### 6.3 🟡 The I²S configuration is fixed at 16-bit stereo, 44.1 kHz

**[BSP]** `badge_bsp_audio.c:22–58`:

```c
.slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_STEREO),
.gpio_cfg = { .mclk = BSP_I2S_MCLK, .bclk = BSP_I2S_BCLK,
              .ws = BSP_I2S_WS,     .dout = BSP_I2S_DOUT,
              .din = I2S_GPIO_UNUSED },
...
return initialize_i2s(44100);
```

- **Philips I²S format, 16-bit, stereo, ESP32-P4 as master** — matches the ES8156's slave-mode expectations and the netlist in §5.
- `din = I2S_GPIO_UNUSED` correctly reflects that this is a **DAC only**; there is no capture path. (Pin 20 `SDOUT` is "playback signal feedback", not a microphone input.)
- **16-bit only**, though the chip is 24-bit **[DS]**. The board forfeits 8 bits of resolution. `bsp_audio_set_rate()` can retune the clock but **cannot change the word length**, because `slot_cfg` is fixed at channel-init time and never revisited.
- 44.1 kHz default is a sensible choice and is comfortably inside the supported 8–48 kHz single-speed range **[DS] §5**.

### 6.4 🟡 Power-saving hooks exist only as a comment

```c
/* For future use when implementing I2S power saving:
   es8156_powerdown(codec_handle);
   es8156_standby_nopop(codec_handle);
   es8156_reset(codec_handle); */
```

The driver exposes the pop-free standby path (the §4.2 sequence), and the BSP does not use it. The codec's analog blocks therefore stay powered whenever audio is initialised. On a battery device that is a measurable, avoidable idle cost. [INF]

### 6.5 ✅ Correct

- Takes the shared-bus semaphore (`concurrency_semaphore`) before I²C access — necessary, given the coprocessor and IMU share the bus.
- Keeps the speaker amplifier enable in the coprocessor domain rather than conflating it with codec control (`bsp_audio_set_amplifier`, `:97`).
- Initialises the codec **before** starting I²S (`:78–83`), which is the right order — clocks should be stable and the codec configured before data arrives.

### 6.6 Summary

| # | Severity | Location | Defect | Live? |
|---|---|---|---|---|
| 6.1 | 🔴 | `badge_bsp_audio.c:90` | Volume linear in dB; "100 %" = −5.5 dB; top of range unreachable; no clamping | **Yes, user-visible** |
| 6.2 | 🟠 | `:87` | `get_volume` unimplemented despite a readable register | Yes |
| 6.3 | 🟡 | `:33` | 16-bit fixed on a 24-bit DAC; word length not reconfigurable | By design |
| 6.4 | 🟡 | `:117` | Pop-free standby unused; codec always powered | Omission |

---

## 7. Pitfalls, in priority order

1. **Enter software mode first** — `REG02` bit 2. Nothing else works properly until you do, and the failure mode is "audio plays but nothing is controllable". §3.
2. **`HPCOM` capless output requires software mode.** §2.
3. **Know whether your library wants 7-bit (`0x08`) or 8-bit (`0x10`).** §1.2.
4. **In hardware/slave mode, only the listed MCLK/LRCK ratios lock.** §3.1.
5. **Ramp volume down before powering down and up after powering up**, or accept pops. §4.2.
6. **Do not expect the datasheet to contain the register map.** Use the ESP-ADF driver. §4.
7. **There is no documented chip-ID value**, so you cannot positively identify the part on the bus. §4.
8. **Volume is 0.5 dB per step with 0 dB at `0xBF` (191)** — not a percentage, not linear in amplitude. §4.1, §6.1.
9. **Single-ended wiring costs SNR** versus the datasheet's differential figures. §5.

---

## 8. Alternatives

| Part | vs. ES8156 | When |
|---|---|---|
| **ES8388** | Everest codec with **ADC** as well as DAC | When you need audio input too |
| **ES7210 / ES7243** | Everest ADC-only | Microphone arrays |
| **[TI PCM5100A](../../texas-instruments/pcm5100a/README.md)** | Documented in this repository. **No I²C at all** — hardware-configured, so no software mode to forget | When you want a DAC that just works with three strapping pins |
| **TI PCM5102A** | Similar, very widely used | Same |
| **Cirrus CS4344** | Simple, cheap, no control interface | Minimal designs |
| **TI TLV320AIC3204** | Far more capable codec, excellent documentation | When you need real DSP and can afford the complexity |

**The ES8156's case is cost plus features**: 110 dB SNR, a 7-band EQ, DRC and a capless headphone driver in a 3 × 3 mm QFN at a low price. The cost is documentation — no public register map, and a hardware/software mode trap. If your design does not need the EQ or the capless driver, the PCM5100A-class parts are much less trouble.

---

## 9. Open questions

- **The register map is not authoritatively published.** §4 is a reconstruction from MIT-licensed driver source. Bit-level field definitions within each register remain unknown; only register *names* and the values vendor drivers write are established.
- **Expected `CHIPID1`/`CHIPID0` values are unknown.** Neither the datasheet nor ADF states them, and ADF never reads them.
- Whether Everest's separate register user guide is obtainable without a customer relationship was not established. `info@everest-semi.com` is the contact the datasheet gives.
- The `0x25` two-stage write in the power-down sequence (§4.2) is inferred to be pop suppression; no document confirms it.
- No measurement of actual output SNR in the Tanmatsu's single-ended configuration.

---

## Manufacturer

**Everest Semiconductor Co., Ltd.** (Beijing) — see [`vendors/everest-semiconductor/README.md`](../../../vendors/everest-semiconductor/README.md).

Sourcing note: the datasheet is served directly from `http://www.everest-semi.com/pdf/<PART>%20PB.pdf` — note **plain HTTP** and the `%20PB` (product brief) suffix, which despite its name is the full 15-page datasheet. Every page is stamped *"Everest Semiconductor Confidential"* and footed *"Latest datasheet: www.everest-semi.com or info@everest-semi.com"*. Four other mirrors were tried first and all returned 404; see §10.

## Used By

| Device | Ref | Role |
|---|---|---|
| [Nicolai Electronics Tanmatsu](../../../devices/nicolai-electronics/tanmatsu/README.md) | `U24` | Stereo audio DAC at I²C **0x08** on the internal bus, fed by the ESP32-P4's I²S (Philips, 16-bit, 44.1 kHz, P4 as master). **Single-ended output with capless `HPCOM`** — headphone path. The speaker amplifier (FM8002A) is separate and coprocessor-controlled. See [`bom.md`](../../../devices/nicolai-electronics/tanmatsu/bom.md), [`pinouts-and-buses.md`](../../../devices/nicolai-electronics/tanmatsu/pinouts-and-buses.md) §1.1 |

## Related pages

- [`components/texas-instruments/pcm5100a/README.md`](../../texas-instruments/pcm5100a/README.md) — the no-I²C alternative
- [`components/generic/3.5mm-audio-output/README.md`](../../generic/3.5mm-audio-output/README.md)
- [`components/bosch-sensortec/bmi270/README.md`](../../bosch-sensortec/bmi270/README.md) — shares the internal I²C bus
- [`components/wch/ch32v203c8t6/README.md`](../../wch/ch32v203c8t6/README.md) — owns the speaker amplifier enable

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | ES8156 datasheet | Everest Semiconductor | primary | datasheet | <http://www.everest-semi.com/pdf/ES8156%20PB.pdf> | 2026-08-30 | **Revision 13.0, February 2026**, 15 pp, 1 441 871 B | Pinout, I²C address rule, HW/SW mode, clock ratios, electrical limits, performance. **No register map** | `artifacts/es8156-datasheet.pdf` |
| D2 | `esp-adf` ES8156 driver — `es8156.c`, `es8156.h` | Espressif | primary | repository | <https://github.com/espressif/esp-adf/tree/v2.7/components/audio_hal/driver/es8156> | 2026-08-30 | tag **v2.7**; ESPRESSIF MIT License, © 2021 | **The entire §4 register map**, the §4.1 volume scale, the §4.2 sequences, the 8-bit address | `/tmp` working copy, not vendored |
| S1 | `badge_bsp_audio.c` (120 lines) | Nicolai Electronics / Badge.Team | primary | repository | in-tree snapshot | 2026-08-30 | MIT, SPDX 2025 | All §6 findings; I²S configuration | `devices/nicolai-electronics/tanmatsu/artifacts/source-snapshots/badge-bsp/tanmatsu/badge_bsp_audio.c` |
| S2 | `tanmatsu.kicad_pcb` | Nicolai Electronics | primary | repository | in-tree snapshot | 2026-08-24 | `tanmatsu-hardware` @ `640805dd`, CERN-OHL-P | §5 pin table, including the unconnected `LOUTN`/`ROUTN` | `devices/nicolai-electronics/tanmatsu/artifacts/schematics/kicad/` |

### 10. Acquisition record

D1 required five attempts. Recorded in `component-download-failures.txt`:

| URL | Result |
|---|---|
| `https://dl.radxa.com/rock3/docs/hw/datasheet/ES8156%20DS.pdf` | HTTP 404 |
| `http://www.everest-semi.com/pdf/ES8156%20PB.pdf` | ✅ **HTTP 200, %PDF, 1 441 871 B** — plain HTTP, Chrome 131 UA |
| `https://dl.radxa.com/rock5/docs/hw/datasheet/ES8156_DS.pdf` | not reached (succeeded earlier) |
| `https://files.seeedstudio.com/wiki/ReSpeaker/ES8156.pdf` | not reached |
| `https://raw.githubusercontent.com/espressif/esp-adf/master/docs/_static/ES8156.pdf` | not reached |

> **Redistribution: `unknown`.** Every page is marked *"Everest Semiconductor Confidential"*, but the file is served without authentication from the manufacturer's own public web root and contains no explicit redistribution clause. Disposition: `repository (unstaged)`, flagged for user review.
