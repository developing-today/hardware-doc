# Alpha & Omega Semiconductor AO3400A — the backlight switch

- **Category:** 30 V N-channel logic-level MOSFET, SOT-23
- **Reference designator on this board:** `Q1`
- **Marking in the schematic BOM field:** `AO3400A` (drawn as `A03400A` — the schematic uses a zero where the datasheet uses a letter O)
- **Owning MCU:** **ESP32-S3**, via GPIO47
- **Role:** the low-side switch for the LCD backlight LED string. **This is its only job on the board** — it appears exactly once in the five schematic sheets
- **Research status:** fully established. Datasheet retrieved and validated
- **Retrieved:** 2026-08-21; schematic re-read and PWM configuration audited 2026-08-23

## Evidence labelling

**[SCH]** schematic PNG · **[SRC]** vendor demo source · **[DOC]** manufacturer datasheet · **[INF]** inference, arithmetic shown

---

## 1. Role on this board

`Q1` is the backlight enable/dimming switch. The circuit, in full **[SCH sheet 1 `1_LCD&POWER.png`]**:

```
3V3 ──── LEDA ──[ panel LED string, connector U5 pins 6, 8 ]
                     │
                 LEDK  (connector U5 pins 2, 4)
                     │
                    R3  3.9 Ω
                     │
                  Q1 drain
   LCD_BLK ────┬── Q1 gate
  (GPIO47)     │
              R4  10 kΩ
               │
              Q1 source ──── GND
```

| Element | Value | Purpose |
|---|---|---|
| `Q1` | **AO3400A**, SOT-23 | Low-side switch |
| `R3` | **3.9 Ω** | Ballast for the LED string. **The only current-limiting element** |
| `R4` | **10 kΩ** | Gate-to-source pull-down |
| Gate net | `LCD_BLK` → **ESP32-S3 GPIO47** | PWM dimming |

There is **no inductor, no constant-current LED driver and no current sense**. This is the simplest possible backlight: a resistor and a switch.

### 1.1 Why `R4` matters more than it looks

The 10 kΩ gate-source pull-down guarantees `Q1` is **off** whenever GPIO47 is not actively driving it. That covers three real situations:

1. **Before the ESP32-S3 boots.** The S3's GPIOs are high-impedance out of reset; without `R4` the gate would float and the backlight state would be undefined during the boot window.
2. **During deep sleep**, if GPIO47 is not held.
3. **If the panel or the S3 is reset independently.**

Without it, the gate's parasitic capacitance would hold charge and the backlight could latch on — or worse, sit at a partially-on gate voltage with `Q1` in linear mode, dissipating real power. **`R4` is not optional and should be preserved in any rework.**

## 2. Key specifications **[DOC, AO3400A rev. 3.1, July 2023]**

| Parameter | Value | Unit |
|---|---:|---|
| `VDS` drain-source voltage | **30** | V |
| `VGS` gate-source voltage | **±12** | V |
| `ID` continuous drain current, `TA` = 25 °C | **5.7** | A |
| `ID` continuous drain current, `TA` = 70 °C | 4.7 | A |
| `IDM` pulsed drain current | 30 | A |
| `RDS(on)` at `VGS` = **10 V** | < **26.5** | mΩ |
| `RDS(on)` at `VGS` = **4.5 V** | < **32** | mΩ |
| `RDS(on)` at `VGS` = **2.5 V** | < **48** | mΩ |
| Power dissipation `PD`, `TA` = 25 °C, steady state | **1.4** | W |
| Power dissipation `PD`, `TA` = 70 °C, steady state | 0.9 | W |
| `RθJA` maximum junction-to-ambient, steady state | **125** | °C/W |
| `RθJA` maximum junction-to-ambient, t ≤ 10 s | 90 | °C/W |
| `RθJL` maximum junction-to-lead | 63 | °C/W |
| Junction / storage temperature | −55 to 150 | °C |
| Package | **SOT-23** (G/D/S) | — |

AOS's own summary: *"combines advanced trench MOSFET technology with a low resistance package to provide extremely low `RDS(ON)`. This device is suitable for use as a load switch or in PWM applications."* **[DOC]** — which is precisely how it is used here.

### 2.1 The specification that makes this the right part

The `RDS(on)` at **2.5 V** `VGS` is the one that matters. The S3 drives GPIO47 at 3.3 V, so the gate sees 3.3 V, comfortably above the 2.5 V characterisation point. **This is a genuine logic-level FET** — a standard 4.5 V or 10 V threshold part would be only partially enhanced at 3.3 V, would run in a higher-resistance state, and would heat up.

At the board's operating point:

- `VGS` = 3.3 V → `RDS(on)` somewhere between the 2.5 V figure (48 mΩ) and the 4.5 V figure (32 mΩ). Call it **~35 mΩ [INF]**
- The FET is switching a load of at most ~150 mA (§3)
- `ID` rating headroom: **5.7 A rated against ~0.15 A used — a 38× margin**
- `VDS` headroom: **30 V rated against 3.3 V maximum — a 9× margin**

This part is enormously over-specified for the job, which is fine: AO3400A is one of the cheapest and most widely second-sourced SOT-23 N-FETs in existence, so there was no reason to pick anything smaller.

## 3. Dissipation — negligible, and here is why

Backlight current is not precisely known (see [tlv62569dbvt §4](../../texas-instruments/tlv62569dbvt/README.md#4--the-backlight-is-the-load-to-worry-about) for why: `R3` is a ballast resistor, not a current source, so the current depends on the LED forward voltage). Taking a generous 150 mA upper bound:

```
P(Q1) = I² × RDS(on) = 0.15² × 0.035 = 0.79 mW
```

Junction rise at `RθJA` = 125 °C/W:

```
ΔT = 0.00079 × 125 = 0.1 °C
```

**[INF]** — arithmetic ours; `RDS(on)` and `RθJA` from **[DOC]**.

Effectively zero. Compare with `R3`, which dissipates `I² × R = 0.15² × 3.9 = 88 mW` — **110× more heat in the ballast resistor than in the FET.** If anything in this circuit runs warm, it is `R3`, and a 3.9 Ω resistor dissipating 88 mW needs to be at least an 0603 (0.1 W) part; the schematic does not state the package **[SCH]**.

Switching losses are similarly negligible at 50 kHz with a sub-nanocoulomb gate charge into 150 mA.

## 4. Driving it: the PWM configuration

The vendor's implementation is `lcd_bl_pwm_bsp.c` **[SRC, `Arduino/examples/08_LVGL_Test/`]**:

| Setting | Value | Comment |
|---|---|---|
| Peripheral | **LEDC** (`driver/ledc.h`) | The right choice — hardware PWM, no CPU cost |
| Speed mode | `LEDC_LOW_SPEED_MODE` | |
| Timer | `LEDC_TIMER_3` | |
| Channel | `LEDC_CHANNEL_1` | |
| Duty resolution | `LEDC_TIMER_8_BIT` | **256 steps**, 0–255 |
| **Frequency** | **50 kHz** (`50 * 1000`) | See §4.1 |
| Clock source | `LEDC_SLOW_CLK_RC_FAST` | See §4.2 |
| GPIO | `EXAMPLE_PIN_NUM_BK_LIGHT` = **47** | |
| `hpoint` | 0 | Phase |

```c
ledc_timer_config_t timer_conf = {
    .speed_mode      = LEDC_LOW_SPEED_MODE,
    .duty_resolution = LEDC_TIMER_8_BIT,      // 256
    .timer_num       = LEDC_TIMER_3,
    .freq_hz         = 50 * 1000,
    .clk_cfg         = LEDC_SLOW_CLK_RC_FAST,
};
ledc_channel_config_t ledc_conf = {
    .gpio_num   = EXAMPLE_PIN_NUM_BK_LIGHT,   // 47
    .speed_mode = LEDC_LOW_SPEED_MODE,
    .channel    = LEDC_CHANNEL_1,
    .intr_type  = LEDC_INTR_DISABLE,
    .timer_sel  = LEDC_TIMER_3,
    .duty       = duty,
    .hpoint     = 0,
};
```

Set brightness with `ledc_set_duty()` then `ledc_update_duty()` — the vendor wraps this as `setUpdutySubdivide(uint16_t duty)`.

### 4.1 Why 50 kHz is a good choice

- **Well above audible.** A backlight PWM in the 200 Hz – 20 kHz range can make ceramic capacitors and the LED package sing. 50 kHz is clear of it.
- **Well above the display refresh rate**, so no visible beating or banding with the panel.
- **Well above the camera-shutter range**, so the screen photographs without rolling bands.
- **Low enough** that a SOT-23 FET's switching losses stay irrelevant and no gate driver is needed.

There is one caveat: **50 kHz is above the audio band but its *envelope* is not.** If you dim the backlight by ramping duty cycle, the ramp itself is a low-frequency current modulation on the 3V3 rail — and the microphone is on that rail. See [memsensing/msm261d4030h1cpm §6](../../memsensing/msm261d4030h1cpm/README.md#6-power-and-noise). If you record audio while animating a brightness fade, expect to hear the fade.

### 4.2 ⚠ `LEDC_SLOW_CLK_RC_FAST` is a questionable choice

The vendor selects `LEDC_SLOW_CLK_RC_FAST` as the LEDC timer clock source **[SRC]**. That is the internal **RC fast oscillator** (~17.5 MHz on the ESP32-S3), not the crystal-derived APB clock.

Implications **[INF]**:

- **The RC oscillator is not precise and drifts with temperature and supply voltage.** The actual PWM frequency will not be exactly 50 kHz and will wander.
- For a backlight this genuinely does not matter — nothing is synchronised to it, and a few percent of frequency drift is invisible.
- **But** RC_FAST plus 8-bit resolution at a nominal 50 kHz needs a source of at least `50 000 × 256 = 12.8 MHz`. RC_FAST at ~17.5 MHz clears that, but not by a lot. **If you raise either the frequency or the resolution, this configuration will silently fail to achieve what you asked for** — LEDC will clamp, and `ledc_timer_config()` returns an error that the vendor's code swallows with `ESP_ERROR_CHECK_WITHOUT_ABORT`.

If you want 10-bit or 12-bit dimming resolution (worth having — 8 bits is coarse at the bottom of the range, where human brightness perception is most sensitive), **switch to `LEDC_AUTO_CLK` or an APB-derived source** and check the return code:

```c
ledc_timer_config_t timer_conf = {
    .speed_mode      = LEDC_LOW_SPEED_MODE,
    .duty_resolution = LEDC_TIMER_10_BIT,   // 1024 steps
    .timer_num       = LEDC_TIMER_3,
    .freq_hz         = 50 * 1000,           // needs >= 51.2 MHz source
    .clk_cfg         = LEDC_AUTO_CLK,       // let the driver pick APB
};
ESP_ERROR_CHECK(ledc_timer_config(&timer_conf));   // and actually check it
```

Also worth knowing: `LEDC_SLOW_CLK_RC_FAST` is one of the few LEDC sources that keeps running in light sleep, which may well be why it was chosen. If backlight-during-light-sleep is not a requirement for you, prefer the APB source.

### 4.3 Perceptual dimming

Human brightness perception is roughly logarithmic, so a linear duty ramp looks wrong — most of the visible change happens in the bottom quarter. With 8-bit resolution there are only ~64 useful steps in the perceptually important region. A gamma curve helps:

```c
// duty = 255 * (level/255)^2.2, precomputed into a 256-entry table
```

This is a firmware improvement, not a hardware limitation, but it is the difference between a backlight that feels smooth and one that steps visibly. Combining it with the 10-bit change in §4.2 is the right fix.

### 4.4 GPIO47 is not a strapping pin

Unlike GPIO45 and GPIO46 (which carry the microphone and *are* strapping pins), **GPIO47 has no strapping function on the ESP32-S3** **[DOC ESP32-S3 datasheet]**. It is an ordinary GPIO with no boot-time constraints, which is a sensible place to put a backlight.

## 5. Pitfalls

1. **`R3` is a ballast resistor, not a current regulator.** Backlight current depends on the LED forward voltage and drifts with temperature. See [tlv62569dbvt §4](../../texas-instruments/tlv62569dbvt/README.md#4--the-backlight-is-the-load-to-worry-about). **Measure it; do not calculate it from the schematic and expect to be right.**
2. **Do not remove `R4`.** §1.1. The backlight state during boot and reset depends on it.
3. **Do not swap in a non-logic-level FET.** §2.1. A 4.5 V-threshold part at `VGS` = 3.3 V will run partially enhanced and hot.
4. **Check `ledc_timer_config()`'s return value** if you change frequency or resolution. §4.2. The vendor code uses `ESP_ERROR_CHECK_WITHOUT_ABORT`, which logs and continues.
5. **The backlight is the largest steady load on the 3.3 V rail.** Turning it off is by far the most effective single power saving available on this board — much more so than any MCU sleep mode while the screen is on.
6. **Do not drive GPIO47 as an open-drain or leave it as an input** and expect the backlight off; `R4` handles that case, but only because it is fitted.
7. **`R3`'s package is not stated in the schematic.** At 88 mW it needs at least an 0603. If you are rebuilding this circuit, do not fit an 0402.

## 6. Alternatives

| Part | Why you might |
|---|---|
| **AO3400A** (this) | 30 V, 5.7 A, ~32 mΩ at 4.5 V, SOT-23, extremely cheap and second-sourced everywhere. Correct choice |
| AO3400 (no `A`) | Earlier revision of the same part. Broadly interchangeable; check the `RDS(on)` grade |
| SI2302, 2N7002 | 2N7002 is **not** a good substitute — it is ~1–5 Ω, three orders of magnitude worse. SI2302 is fine |
| DMG3414U, BSS138 | BSS138 has the same objection as 2N7002. DMG3414U is a reasonable logic-level equivalent |
| A dedicated LED driver (e.g. constant-current boost) | Would fix the `Vf`-sensitivity problem in §5.1 and give proper brightness matching board-to-board. Costs an inductor and a part |

Any SOT-23 N-FET with `RDS(on)` well under 100 mΩ at `VGS` = 2.5 V and `VDS` ≥ 20 V will work here. The margins are so large that the choice is essentially free.

## 7. Open questions

| Question | Status |
|---|---|
| Actual backlight current, and the panel's LED `Vf` | **Unknown.** Depends on the unidentified panel — see [generic/lcd-panel-module](../../generic/lcd-panel-module/README.md). Measure across `R3` |
| Whether the panel has one LED string or two in parallel | **Probably two** — the connector wires `LEDA` on two pins and `LEDK` on two pins **[SCH, INF]**, but this is not confirmed |
| `R3` package/power rating | **Not stated** in the schematic |
| `Q1` date code / lot | **Unknown** |

## Manufacturer

**Alpha & Omega Semiconductor** — see the [Alpha & Omega Semiconductor documentation-sourcing guide](../../../vendors/alpha-and-omega-semiconductor/README.md) for this vendor's document portals, URL patterns, part-numbering conventions, distribution channels and known gotchas.

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — `Q1`, LCD backlight low-side switch, gate on ESP32-S3 GPIO47

## Related pages

- [generic/lcd-panel-module](../../generic/lcd-panel-module/README.md) — the panel and its LED string
- [texas-instruments/tlv62569dbvt](../../texas-instruments/tlv62569dbvt/README.md) — the rail the backlight loads, and the ballast-resistor analysis
- [memsensing/msm261d4030h1cpm](../../memsensing/msm261d4030h1cpm/README.md) — why backlight dimming ramps can end up in a recording
- [Pinouts and buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md)

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| AO3400A datasheet, rev. 3.1 (July 2023) — source of every figure in §2 | https://aosmd.com/res/data_sheets/AO3400A.pdf | 2026-08-21 | [artifacts/ao3400a-datasheet.pdf](artifacts/ao3400a-datasheet.pdf) |
| AOS AO3400A product page | https://aosmd.com/products/mosfets/n-channel/AO3400A | 2026-08-21 | — |
| Board schematic sheet 1 — `Q1`, `R3` 3.9 Ω, `R4` 10 kΩ, `LEDA`/`LEDK`, `LCD_BLK` | — | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/1_LCD&POWER.png` |
| Board schematic sheet 2 — `LCD_BLK` aliased to GPIO47 | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/2_ESP32S3-R8.png` |
| Waveshare demo `08_LVGL_Test` — `lcd_bl_pwm_bsp.c`, the LEDC configuration | — | 2026-08-21 | `.../artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Arduino/examples/08_LVGL_Test/` |
| ESP-IDF v5.3.2 LEDC driver | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32s3/api-reference/peripherals/ledc.html | 2026-08-23 | closest archived PDF: `../../espressif/esp32-s3r8/artifacts/esp-idf-programming-guide-v5.2.5-esp32s3.pdf` |
| ESP32-S3 datasheet (GPIO47 has no strapping function) | https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf | 2026-08-21 | `../../espressif/esp32-s3r8/artifacts/esp32-s3-datasheet.pdf` |
