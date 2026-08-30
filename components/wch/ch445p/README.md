# WCH CH445P

- **Category:** quad single-pole double-throw (QPDT / 4× 2:1) bidirectional analog switch, 3.3 V rated
- **Research status:** **datasheet located and retrieved 2026-08-21.** Previously recorded as "no PDF available". The truth table, pin map, on-resistance curves and bandwidth are now all **[DOC]**, and the board's select polarity is corroborated independently by the vendor firmware.
- **Retrieved:** 2026-08-21

`U18` on the [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md). It is the arbitration point of the board's audio path: it decides **which of the two MCUs' I²S buses reaches the PCM5100A DAC.**

> **⚠ Supersedes prior records.** The earlier version of this page, and the entry in [`component-download-failures.txt`](../../../component-download-failures.txt), stated that no CH445P datasheet could be obtained and that **"which `IN` level selects which bank is unknown"**. Both are now resolved:
> - The datasheet **does exist**, as `CH440DS1.PDF` v3.2 — a *family* document covering CH440/CH442/CH443/CH444/**CH445**/CH448. Searching for "CH445 datasheet" finds nothing because WCH files it under the CH440 name. It is now at `artifacts/ch440-ch442-ch443-ch444-ch445-ch448-datasheet-v3.2.pdf`.
> - **`IN` = 0 selects the S1 bank (ESP32-U4WDH); `IN` = 1 selects the S2 bank (ESP32-S3).** §4.1.
>
> The corresponding "unknown" note in [Pinouts and buses § Audio arbitration](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md) is superseded by §4 below.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[SCH]** | Read directly off the board schematic PNGs in `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/` |
| **[DOC]** | Stated by WCH in `artifacts/ch440-…-v3.2.pdf` |
| **[SRC]** | Read out of Waveshare's own example source in the device's `artifacts/demo/` tree |
| **[INF]** | Inference. Not established by the above |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Marked part | `CH445P` | **[SCH]** sheet `5_DAC.png`, symbol name on `U18` |
| Manufacturer | WCH — Nanjing Qinheng Microelectronics (南京沁恒微电子) | **[DOC]** |
| Reference designator | **U18** | **[SCH]** |
| Function | **QPDT** — quad single-pole double-throw, i.e. four independent 2:1 bidirectional analog switches sharing one select and one enable | **[DOC]** §5.1 |
| Package | **QFN-16, 3 × 3 mm, 0.50 mm (19.7 mil) pitch**, with an exposed pad designated pin **0# = GND** | **[DOC]** §3 |
| Rated supply | **3.3 V device** (2.9–3.7 V operating; a separate 2.5 V table exists down to 1.5 V) | **[DOC]** §6.5, §6.6 |
| Datasheet | `CH440DS1.PDF` **version 3.2**, dated 2022-06-29, 307 KB | **[DOC]** WCH file metadata, id 135 |
| Lifecycle | Active. WCH lists `CH445P` in the current CH440-family `scope` string | **[DOC]** |

### 1.1 The CH440 family — what the number and letter mean

**[DOC]** §3. The family document covers six distinct *functions*; the **number** chooses the function and voltage class, the **letter** chooses the package.

| Part | Function | Package | Control pins |
|---|---|---|---|
| CH440G | QPDT (4× SPDT), **5 V rated** | SOP-16 | `EN#` + `IN` |
| CH440P | QPDT, 5 V rated | QFN-16 3×3 | `EN#` + `IN` |
| CH440R | QPDT, 5 V rated | TSSOP-16 | `EN#` + `IN` |
| **CH445P** | **QPDT, 3.3 V rated** | **QFN-16 3×3** | **`EN#` + `IN`** |
| CH442E / CH442Q | DPDT (2× SPDT) | MSOP-10 / QFN | `EN#` + `IN` |
| CH443K / CH443L | SPDT (1× SPDT) | SOT-363 6-pin | `SEL` only, no enable |
| CH444G / CH444P | DP4T (2× 4:1 mux) | SOP-16 / QFN-16 | `EN#` + `IN1`,`IN0` |
| CH448F / CH448U | DP8T (2× 8:1, differential 8:1, or 16:1) | QFN-24 4×4 | `XEN#`,`YEN#` + `SEL2..0` |

> **The single most important distinction: `CH440P` and `CH445P` are the same package, the same pinout and the same function — but different supply ratings.** CH440P is the 5 V part; **CH445P is the 3.3 V part**, with its own electrical-characteristics tables (datasheet §6.5–6.7). Every table in §6.2–6.4 carries the test-condition note "**excluding CH445**". Do not read CH440P numbers and apply them here.

WCH's own one-line summary of the family **[DOC]** (file metadata `content` field): *"multi-channel low-resistance wideband bidirectional analog switch chips … with 5 Ω on-resistance, high bandwidth supporting 480 Mbps, compatible with video signals, and capable of switching low-speed/full-speed/high-speed USB signals."* The family is aimed at USB and video muxing; using it for a 1.4 MHz I²S bus is far inside its comfort zone.

---

## 2. Pinout

**[DOC]** §4.1, cross-checked pin-for-pin against **[SCH]** `5_DAC.png`. They agree exactly.

| QFN-16 pin | Name | Type | Function |
|---:|---|---|---|
| 0 (EPAD) | `GND` | Power | Exposed pad. Optional but recommended to connect **[DOC]** §3 note 3 |
| 1 | `S2A` | Analog | Channel A input 2 — selected when `IN` is **high** |
| 2 | `DA` | Analog | Channel A **common** |
| 3 | `S1B` | Analog | Channel B input 1 — selected when `IN` is **low** |
| 4 | `S2B` | Analog | Channel B input 2 — `IN` high |
| 5 | `DB` | Analog | Channel B common |
| 6 | `GND` | Power | Digital reference ground — **required connection** |
| 7 | `DC` | Analog | Channel C common |
| 8 | `S2C` | Analog | Channel C input 2 — `IN` high |
| 9 | `S1C` | Analog | Channel C input 1 — `IN` low |
| 10 | `DD` | Analog | Channel D common |
| 11 | `S2D` | Analog | Channel D input 2 — `IN` high |
| 12 | `S1D` | Analog | Channel D input 1 — `IN` low |
| 13 | `EN#` | Digital in | **Global enable, active LOW.** High ⇒ all four channels open-circuit |
| 14 | `VCC` | Power | Positive supply |
| 15 | `IN` | Digital in | **Global select.** Low ⇒ S1 bank; High ⇒ S2 bank |
| 16 | `S1A` | Analog | Channel A input 1 — `IN` low |

Note the interleaved layout: the pin order is *not* A,B,C,D in sequence, and channel A's `S1A` is on pin 16 while `S2A` is on pin 1 — they wrap around the corner. This puts each pair adjacent to its common, but it makes the schematic hard to read at a glance.

---

## 3. Truth table

**[DOC]** §5.1, reproduced verbatim.

| `EN#` | `IN` | `DA` | `DB` | `DC` | `DD` |
|---|---|---|---|---|---|
| 0 | 0 | Select `S1A` | Select `S1B` | Select `S1C` | Select `S1D` |
| 0 | 1 | Select `S2A` | Select `S2B` | Select `S2C` | Select `S2D` |
| 1 | X | All off | All off | All off | All off |

All four channels switch **together**. There is no per-channel control.

---

## 4. Exact wiring on this board — and the resolved select polarity

**[SCH]** sheet `5_DAC.png`.

| `U18` pin | Signal | Net on this board | Comes from / goes to |
|---:|---|---|---|
| 16 | `S1A` | `ESP32_I2S_DAC_BCK` | ESP32-U4WDH GPIO25 (I2S0 BCLK) |
| 1 | `S2A` | `S3_I2S_DAC_BCK` | ESP32-S3 GPIO39 |
| 2 | `DA` | `I2S_DAC_BCK` | → PCM5100A `U12` pin 13 `BCK` |
| 3 | `S1B` | `ESP32_I2S_DAC_DIN` | ESP32-U4WDH GPIO26 (I2S0 SDOUT) |
| 4 | `S2B` | `S3_I2S_DAC_DIN` | ESP32-S3 GPIO41 |
| 5 | `DB` | `I2S_DAC_DIN` | → PCM5100A pin 14 `DIN` |
| 9 | `S1C` | `ESP32_I2S_DAC_LRCK/WS` | ESP32-U4WDH GPIO27 (I2S0 WS) |
| 8 | `S2C` | `S3_I2S_DAC_LRCK/WS` | ESP32-S3 GPIO40 |
| 7 | `DC` | `I2S_DAC_LRCK/WS` | → PCM5100A pin 15 `LRCK` |
| 12, 11, 10 | `S1D`, `S2D`, `DD` | *unconnected* | **The MCLK channel is not used** — §4.2 |
| 13 | `EN#` | **GND** | **Permanently enabled** |
| 14 | `VCC` | `3V3_DAC` | From the SGM2036-3.3 LDO `U20`, decoupled by `C100` 100 nF |
| 15 | `IN` | `I2S_SWITCH_IN` | **ESP32-S3 GPIO0** |
| 6, 0 | `GND` | GND | |

### 4.1 ✅ Which level selects which MCU — resolved, two independent ways

**`IN` = 0 (low) → S1 bank → the ESP32-U4WDH drives the DAC.**
**`IN` = 1 (high) → S2 bank → the ESP32-S3 drives the DAC.**

1. **[DOC]** The datasheet truth table (§3): `IN` low selects `S1x`. The schematic puts the ESP32-U4WDH nets on `S1A/S1B/S1C` and the ESP32-S3 nets on `S2A/S2B/S2C` **[SCH]**.
2. **[SRC]** Waveshare's own audio example drives GPIO0 high and says so in a comment. From `artifacts/demo/…/Arduino/examples/07_Audio_Test/audio_bsp.c`, `audio_gpio_init()`:

   ~~~c
   gpio_conf.pin_bit_mask = ((uint64_t)0x01 << GPIO_NUM_0);
   gpio_conf.mode = GPIO_MODE_OUTPUT;
   ESP_ERROR_CHECK_WITHOUT_ABORT(gpio_config(&gpio_conf));
   gpio_set_level(GPIO_NUM_0, 1);
   ~~~

   called from `audio_bsp_init()` under the comment `//把PCM5100A的控制权给到ESP32S3` — *"give control of the PCM5100A to the ESP32-S3."* Setting the pin **high** is what hands control to the S3, exactly as the truth table predicts. Two sources, no conflict.

### 4.2 ⚠ Channel D is unused: there is no MCLK

`S1D`, `S2D` and `DD` have no nets **[SCH]**. **No master clock reaches the PCM5100A from either MCU.** The DAC therefore *must* run in its BCK-derived PLL mode. This is a hard constraint on both firmwares — see [PCM5100A §5](../../texas-instruments/pcm5100a/README.md).

The schematic sheet carries a small legend box reading `DA → DATA`, `DB → LRCK_WS`, `DC → BCK`, `DD → MCK`. **That legend disagrees with the actual nets**, which are `DA → BCK`, `DB → DIN`, `DC → LRCK/WS`. **Trust the nets, not the legend** — the legend appears to be a stale design note carried over from an earlier revision. **[SCH]** **[INF]**

### 4.3 ⚠ `IN` is also the ESP32-S3's BOOT strapping pin

`I2S_SWITCH_IN` is **GPIO0**, which on the ESP32-S3 is the boot-mode strap, is pulled up by `R58` 10 kΩ to 3V3, and is also brought out to connector `CN1` and to the board's BOOT button. Consequences:

- **At power-on and through every reset, `IN` sits high** (via `R58`), so the mux defaults to the **ESP32-S3** bank before any firmware runs. **[INF]** from the pull-up.
- **Holding the BOOT button pulls `IN` low**, momentarily handing the DAC to the ESP32-U4WDH. Harmless, but you may hear a click if you press BOOT during playback. **[INF]**
- **You cannot use GPIO0 for anything else.** Any library that reconfigures GPIO0 (say, as an interrupt input) silently changes who owns the DAC.
- Driving GPIO0 low *while* `EN` is pulsed will put the S3 into download mode. Do not "park" the mux on the U4WDH by leaving GPIO0 low across a reset unless you intend that.

### 4.4 The split-ownership problem

| Control | Owner | Consequence |
|---|---|---|
| **Mux select** (`IN`) | **ESP32-S3 only** — GPIO0 | The S3 alone chooses the source |
| **DAC mute** (`XSMT`) | **ESP32-U4WDH only** — GPIO32, direct to PCM5100A pin 17, **not through the mux** | The U4WDH alone can un-mute |

**Neither MCU can produce audio by itself.** Any source handover has to be coordinated across the inter-MCU UART. The failure mode this creates is documented under [PCM5100A §7.1](../../texas-instruments/pcm5100a/README.md): if you erase or hold the U4WDH, nothing drives `XSMT`.

---

## 5. Electrical specifications

**[DOC]** §6. **Only the CH445-specific tables are reproduced** (§6.5–6.7); §6.2–6.4 are explicitly marked "excluding CH445" and do **not** apply.

### 5.1 Absolute maximum ratings (§6.1)

| Symbol | Parameter | Min | Max | Unit |
|---|---|---:|---:|---|
| `TA` | Operating ambient temperature | −40 | 85 | °C |
| `TS` | Storage temperature | −55 | 125 | °C |
| `VCC` | Supply voltage, **3.3 V device** | −0.5 | **4.4** | V |
| `VIO` | Voltage on any digital or analog pin | −0.5 | VCC + 0.4 | V |
| `Isw` | Continuous current through one analog switch | 0 | 30 | mA |
| `Iall` | Total continuous current, all switches | 0 | 120 | mA |

### 5.2 DC characteristics at VCC = 3.3 V (§6.5, TA = 25 °C, CH445 only)

| Symbol | Parameter | Min | Typ | Max | Unit |
|---|---|---:|---:|---:|---|
| `VCC` | Supply voltage | 2.9 | 3.3 | 3.7 | V |
| `ICC` | Static supply current, digital pins at rail | | 0.1 | 6 | µA |
| `ICCX` | Static supply current, digital pins at 2.3 V | | 0.07 | 0.3 | mA |
| `VIL` | Digital input low | 0 | | 0.9 | V |
| `VIH` | Digital input high | **2.0** | | VCC | V |
| `ILEAK` | Digital input leakage | | 0.1 | 6 | µA |
| `IOFF` | Off-state analog leakage | | ±0.01 | ±1 | µA |
| `VANA` | **Recommended** analog signal range | 0 | | **2.0** | V |
| `VANAX` | **Allowed** analog signal range | −0.3 | | VCC + 0.3 | V |
| `RON1` | On-resistance at V\_signal = 0 V | | 3.5 | 6 | Ω |
| `RON2` | On-resistance at V\_signal = 1.5 V | | 4.5 | 8 | Ω |
| `RON3` | On-resistance at V\_signal = 2.3 V | | **7** | **11** | Ω |
| `RON4` | On-resistance at V\_signal = 3.3 V | | 5.5 | 9 | Ω |

A 2.5 V table also exists (§6.6): `VCC` 1.5–2.8 V, `VIH` 1.5 V min, `RON` peaking at 11 Ω typ / 16 Ω max around 1.8 V. Not used on this board.

### 5.3 Timing at VCC = 3.3 V (§6.7, CH445 only)

| Symbol | Parameter | Min | Typ | Max | Unit |
|---|---|---:|---:|---:|---|
| `CIN` | Digital input capacitance @ 1 MHz | | 3 | 6 | pF |
| `COFF` | Analog pin capacitance, switch off @ 1 MHz | | 6 | 10 | pF |
| `CON` | Analog pin capacitance, switch on @ 1 MHz | | 9 | 15 | pF |
| `BW` | **−3 dB bandwidth** | **400** | 500 | | MHz |
| `TON` | Switch turn-on delay, RL = 75 Ω, CL = 10 pF | | 2.5 | 5 | ns |
| `TOFF` | Switch turn-off delay | | 1.8 | 5 | ns |

### 5.4 What these numbers mean in practice here

- **Bandwidth is a non-issue.** The fastest signal on the mux is BCK at 1.4112 MHz (44.1 kHz × 32 fs) — about 0.35 % of the 400 MHz minimum. **[INF]**
- **On-resistance is a non-issue.** 5–11 Ω into the PCM5100A's high-impedance CMOS digital inputs is negligible; with `CON` ≈ 9–15 pF the RC corner is in the hundreds of MHz. **[INF]**
- **⚠ The signals exceed the *recommended* analog range.** `VANA` recommends 0–2.0 V at VCC = 3.3 V, but these are full 3.3 V CMOS logic swings. They are inside `VANAX` (VCC + 0.3 V) so nothing is stressed, and `RON4` at 3.3 V (5.5 Ω typ) is actually *better* than `RON3` at 2.3 V (7 Ω typ) because of the complementary-FET topology — the worst case is the **mid-rail crossing**, not the rails. **[DOC]** Worth knowing if you ever repurpose this part for a genuine analog signal, where the 2.0 V recommendation is about distortion, not damage.
- **`IN` VIH is 2.0 V min.** The ESP32-S3 drives a full 3.3 V, so there is margin — but only if `3V3_DAC` is up. §7.1.
- **Switching is fast (2.5 ns) and unsynchronised.** Toggling `IN` mid-frame chops BCK, DIN and WS simultaneously and mid-bit. The PCM5100A will register a clock error. **Mute first.** §7.2.

---

## 6. Software: there is no API

CH445P has **no register interface, no I²C address and no serial protocol**. It is three GPIO-level facts.

~~~c
// ESP-IDF: hand the DAC to the ESP32-S3
#define I2S_SWITCH_IN  GPIO_NUM_0    // also the S3 BOOT strap -- see §4.3

gpio_config_t cfg = {
    .pin_bit_mask = 1ULL << I2S_SWITCH_IN,
    .mode         = GPIO_MODE_OUTPUT,
    .pull_up_en   = GPIO_PULLUP_ENABLE,     // matches R58; keeps the reset default sane
    .pull_down_en = GPIO_PULLDOWN_DISABLE,
    .intr_type    = GPIO_INTR_DISABLE,
};
ESP_ERROR_CHECK(gpio_config(&cfg));

gpio_set_level(I2S_SWITCH_IN, 1);    // 1 = S2 bank = ESP32-S3   (this board's normal state)
// gpio_set_level(I2S_SWITCH_IN, 0); // 0 = S1 bank = ESP32-U4WDH
~~~

Arduino equivalent: `pinMode(0, OUTPUT); digitalWrite(0, HIGH);`

`EN#` is hard-wired to ground **[SCH]**, so the "all off" row of the truth table is **not reachable in software on this board**. If you want silence you must mute the DAC (`XSMT`, owned by the U4WDH) or stop the I²S peripheral — you cannot open the mux.

---

## 7. Initialization order, gotchas and pitfalls

### 7.1 Power sequencing

`VCC` is `3V3_DAC` from the SGM2036-3.3 LDO (`U20`), fed from **5 V** through ferrite `L8` (`BLM18AG102SN1D`) **[SCH]** — *not* from the main 3V3 rail. Two consequences:

- Whether `3V3_DAC` is up on battery-only power depends on the [charger / power-path topology](../../generic/charger-power-path/README.md), which is unresolved. **If `3V3_DAC` is down, the mux is unpowered and every channel is open** — no audio, regardless of what either MCU does. **[INF]**
- With `VCC` at 0 V and the MCUs driving 3.3 V into `S1x`/`S2x`, you are forward-biasing the switch's ESD structures: `VANAX` max is `VCC + 0.3 V` **[DOC]**, so this is an absolute-maximum violation. Waveshare presumably relies on the rails coming up together. **[INF]** Do not replicate the pattern in your own design without gating the MCU outputs.

### 7.2 Switching order — always mute first

All four channels break simultaneously in ~2 ns, so a live switch produces a torn frame and a clock error at the DAC. The PCM5100A responds by switching to its internal oscillator and hard-muting to ground **[DOC]** PCM5100A §11.2 — audible as a click.

Correct handover sequence **[INF]** — no shipped firmware performs a handover, so this is derived from the two datasheets:

1. Source MCU stops its I²S channel (`i2s_channel_disable()`).
2. ESP32-U4WDH asserts `XSMT` low; wait **150 × tS + 0.2 ms** (≈ 3.6 ms at 44.1 kHz) for soft-then-hard mute to complete **[DOC]**.
3. ESP32-S3 toggles `I2S_SWITCH_IN`.
4. New source MCU starts its I²S channel; let BCK/LRCK run for at least **16 LRCK periods** so the DAC's PLL relocks **[DOC]** PCM5100A §9.3.5.3.
5. ESP32-U4WDH releases `XSMT` high.

Steps 2 and 5 require the inter-MCU UART, because the S3 owns step 3 and the U4WDH owns steps 2 and 5.

### 7.3 Other pitfalls

1. **Reading CH440P's numbers.** §6.2–6.4 of the datasheet say "excluding CH445" in the test-conditions line. The 5 V part's `VANA` is 0–2.8 V and its `RON` curve peaks at 23 Ω. Use §6.5–6.7.
2. **Searching for "CH445 datasheet".** WCH files it as `CH440DS1.PDF`. There is no standalone CH445 document. This is why the previous research pass failed — see the retrieval notes.
3. **Assuming `EN#` is software-controllable.** It is tied to GND on this board.
4. **Assuming the mux is unidirectional.** It *is* bidirectional (a pass-gate), but the board wires all three used channels source→DAC only. There is no return path.
5. **Forgetting GPIO0's other jobs.** §4.3.
6. **Treating CH445P as a USB-C orientation switch or a codec.** It is neither. On this board it touches only the three I²S lines. (WCH *does* market this family for USB muxing, which is probably where that confusion originates.)
7. **The exposed pad.** WCH says pad 0# is "optional but recommended" for CH445P — mandatory only for CH448F **[DOC]** §3 note 3. If you are reworking `U18`, reflow the pad.

---

## 8. Alternatives and drop-in compatibility

| Part | Function | Package | Drop-in? |
|---|---|---|---|
| **WCH CH440P** | QPDT, **5 V rated** | QFN-16 3×3 | **Pin-compatible and footprint-compatible.** Works at 3.3 V but with the §6.3 characteristics — `RON` 23 Ω typ at 2.0 V versus CH445P's 7 Ω at 2.3 V. Functional but inferior here **[DOC]** |
| WCH CH440G | QPDT, 5 V | SOP-16 | Same function, different package |
| WCH CH440R | QPDT, 5 V | TSSOP-16 | Same function, different package |
| TI **TS3A5017** | Quad SPDT | TSSOP-16 / QFN | Similar function but **four independent selects**, not one global — not drop-in |
| TI **TS5A23157**, ON **NLAS4599** | Dual SPDT | | Would need two devices |
| **74HC4053** | Triple SPDT, logic family | SOP-16 | Three channels only, and `RON` ~70 Ω — 10× worse. Adequate for 1.4 MHz logic but not equivalent |
| **74CBTLV3257 / SN74CB3Q3257 / QS3257** | Quad 2:1 FET bus switch | TSSOP-16 | Closest *standard-logic* equivalent: quad 2:1, one select, one `OE#`, sub-10 Ω on-resistance. Different pinout, but the same idea and multiply second-sourced |

**If you need a second source for this exact footprint, CH440P is the answer** — same QFN-16 3×3, same pin assignment, same truth table, just the 5 V-rated die.

---

## 9. Open questions

| Question | Status |
|---|---|
| Is `3V3_DAC` present when running on battery only? | **Open.** Depends on the unresolved [charger/power-path](../../generic/charger-power-path/README.md) topology. Determines whether audio works off USB power |
| Does any shipped firmware ever set `I2S_SWITCH_IN` low? | **Open.** The S3-side examples only ever set it high **[SRC]**. The factory application must do so to act as a Bluetooth speaker, but that path lives in the binary, not in the published source archive |
| The `DA/DB/DC/DD → DATA/LRCK_WS/BCK/MCK` legend on sheet 5 | **Contradicts the nets.** §4.2. Treated as a stale note |
| Silicon revision / date code of the fitted `U18` | **Open.** Not readable from any published image |

---

## Manufacturer

**WCH (Nanjing Qinheng)** — see the [WCH (Nanjing Qinheng) documentation-sourcing guide](../../../vendors/wch/README.md) for this vendor's document portals, URL patterns, part-numbering conventions, distribution channels and known gotchas.

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — reference designator **`U18`**, selecting which MCU's I²S reaches the PCM5100A. See [Pinouts and buses § Audio arbitration](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md) and [Dual-MCU architecture](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md).

## Related components

- [Texas Instruments PCM5100A](../../texas-instruments/pcm5100a/README.md) — the sink, and owner of the other half of the arbitration (`XSMT`)
- [SGMicro SGM2036-3.3](../../sgmicro/sgm2036-3.3/README.md) — supplies `3V3_DAC` to this device
- [Espressif ESP32-S3R8](../../espressif/esp32-s3r8/README.md) — drives `IN` from GPIO0
- [Espressif ESP32-U4WDH](../../espressif/esp32-u4wdh/README.md) — the `S1` bank source
- [USB-UART bridge `U10` (CH340X)](../../wch/ch340x/README.md) — the other WCH part on this board

---

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| **WCH CH440/CH442/CH443/CH444/CH445/CH448 Datasheet, version 3.2** (2022-06-29) — pin definitions §4.1, truth table §5.1, CH445 electricals §6.5–6.7 | https://www.wch-ic.com/download/file?id=135 | 2026-08-21 | `artifacts/ch440-ch442-ch443-ch444-ch445-ch448-datasheet-v3.2.pdf` |
| WCH file metadata for the above (confirms `scope` includes `CH445P`) | https://www.wch-ic.com/api/official/website/files/getFilesById?id=135 | 2026-08-21 | – |
| WCH CH440 product page | https://www.wch-ic.com/products/CH440.html | 2026-08-21 | – |
| Board schematic archive (sheet `5_DAC.png`) | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` |
| Official demo archive — `07_Audio_Test/audio_bsp.c`, the select-polarity corroboration | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` |

### Retrieval notes — how the "missing" datasheet was found

The previous pass recorded two failures in [`component-download-failures.txt`](../../../component-download-failures.txt): `https://www.wch-ic.com/search?q=CH445` exposed no PDF, and `https://www.wch.cn/downloads/file/337.html` returned JavaScript. Both are accurate observations with a common cause and a common fix.

- `www.wch-ic.com` is a Vue single-page app that answers **HTTP 200 with a 4305-byte HTML shell for every path it does not recognise**, including every `…_PDF.html` documentation URL and every `downloads/file/<id>.html` page. Nothing in the response distinguishes "wrong URL" from "here is your document", which is why the earlier attempt could only conclude "not a PDF". (`www.wch.cn`, the Chinese site, behaves identically with a 4271-byte shell.)
- **There is no `CH445DS1.PDF`.** WCH publishes one document for the whole analog-switch family, named after its first member: `CH440DS1.PDF`. Searching document *titles* for "CH445" therefore returns nothing. The string only appears in the document's `scope` metadata field.

The route that works, discovered 2026-08-21:

1. `GET https://www.wch-ic.com/api/official/website/files/getFilesById?id=<N>` returns JSON with `name`, `version`, `uploadTime`, `size`, `content` and — crucially — **`scope`**, a comma-separated list of every part number the document covers. Enumerating `N` over roughly 1–800 and grepping `scope` for `CH445P` locates id **135** immediately. For this document `scope` reads: `CH440G, CH440P, CH440R, CH442E, CH442Q, CH443K, CH443L, CH444G, CH444P, CH445P, CH448F, CH448U`.
2. `GET https://www.wch-ic.com/download/file?id=135` returns a genuine `%PDF-1.4`, 314 459 bytes, matching the API's declared "307KB".

A plain default User-Agent sufficed; no substitution was needed. Requests above ~24-way concurrency time out silently, so enumeration should be throttled. Chinese-language sources (Baidu-indexed mirrors, LCSC, datasheet aggregators) were not needed once the API route was found. Recorded in [`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).
