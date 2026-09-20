# 1.8-inch 360 × 360 round LCD + touch panel module (unidentified)

- **Category:** round capacitive-touch TFT module, integrated LCD + touch + backlight on one FPC
- **Reference designator on this board:** `U5` — drawn as a **28-pin connector/module symbol**, not as a display controller
- **Owning MCU:** **ESP32-S3 only** — QSPI display bus, I2C touch, PWM backlight
- **Research status:** the **connector pinout is now fully resolved** (§2), as are the bus, backlight and resolution. The **module part number, panel maker, controller identity and every optical/mechanical specification remain unknown**
- **Retrieved:** 2026-08-21; the 28-pin symbol re-read pin-by-pin at high magnification 2026-08-23

## Evidence labelling

**[SCH]** schematic PNG · **[SRC]** vendor demo source · **[DOC]** manufacturer datasheet · **[WEB]** vendor page/wiki · **[INF]** inference, reasoning given

---

## 1. What is known, and what is not

### 1.1 Established

| Fact | Value | Evidence |
|---|---|---|
| Resolution | **360 × 360** | [SRC `lcd_config.h`: `EXAMPLE_LCD_H_RES 360`, `EXAMPLE_LCD_V_RES 360`] |
| Diagonal | **1.8 inch** | [WEB] |
| Shape | **Round** | [WEB] and the 360×360 square framebuffer with a circular aperture |
| Colour depth used | **16 bpp (RGB565)** | [SRC `LCD_BIT_PER_PIXEL 16`] |
| Display interface | **QSPI**, 4 data lines + clock + CS | [SCH, SRC] |
| Touch | **Capacitive, CST816D at I2C 0x15**, with INT and RST | [SCH, SRC] |
| Backlight | LED string, anode on 3V3, cathode switched low-side | [SCH] |
| Module integration | **One 28-pin FPC carries display, touch and backlight** | [SCH] |
| Panel supply | **3.3 V**, two pins | [SCH] |

### 1.2 Unknown — and not guessable

| Unknown | Note |
|---|---|
| **Module manufacturer and part number** | Nothing in the published archive names it. The schematic symbol is `U5` with no BOM string |
| **Which display controller is actually fitted** | Waveshare's product page says **ST77916**; the vendor's own driver source is named `esp_lcd_sh8601.c` and checks for ID `0x86` — i.e. **SH8601**. This conflict is board-wide; see [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md) and the two component pages: [sitronix/st77916](../../sitronix/st77916/README.md) and [generic/sh8601-compatibility-driver](../sh8601-compatibility-driver/README.md) |
| Panel technology (IPS vs TN) | **Unknown.** "IPS" is a common Waveshare claim but is not established here |
| Brightness (cd/m²), contrast, colour gamut | **Unknown.** No optical specification published |
| Viewing angles | **Unknown** |
| Backlight LED count, forward voltage, arrangement | **Unknown.** §4 explains why this matters |
| Physical dimensions, active-area diameter, bezel, thickness | **Unknown** |
| Cover glass material and hardness | **Unknown** |
| FPC pitch, length and connector part | **Unknown** — the schematic draws a logical 28-pin symbol, not a connector part number |
| Operating temperature range | **Unknown** |
| Frame rate the panel supports | **Unknown** |
| Whether `TE` is driven by the panel at all | **Unknown.** The pin exists on the connector; nothing consumes it. §3.2 |

**Replacement is therefore not determined.** You cannot buy a spare for this board from the published documentation. If you have opened one and read a marking off the FPC, that is the single most valuable missing datum — please record it here and in [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md).

## 2. The 28-pin connector pinout — fully resolved **[SCH sheet 1 `1_LCD&POWER.png`]**

This was previously undocumented. Read pin-by-pin at high magnification from the `U5` symbol:

| Pin | Net | Function | → ESP32-S3 |
|---:|---|---|---:|
| 1 | `TP_INT` | Touch interrupt, from CST816D | **GPIO9** |
| 2 | `LEDK` | Backlight LED cathode | *(via `R3` to `Q1`)* |
| 3 | `TP_RST` | Touch reset | **GPIO10** |
| 4 | `LEDK` | Backlight LED cathode | *(same net as pin 2)* |
| 5 | `TP_SDA` | Touch I2C data | **GPIO11** |
| 6 | `LEDA` | Backlight LED anode | *(3V3)* |
| 7 | `TP_SCL` | Touch I2C clock | **GPIO12** |
| 8 | `LEDA` | Backlight LED anode | *(same net as pin 6)* |
| 9 | `LCD_QSPI_SCL` | QSPI clock | **GPIO13** |
| **10** | — | **NOT CONNECTED** — marked with an explicit no-connect cross | — |
| 11 | `LCD_QSPI_CS` | QSPI chip select | **GPIO14** |
| 12 | `3V3` | Panel logic supply | — |
| 13 | `LCD_QSPI_D0` | QSPI data 0 | **GPIO15** |
| 14 | `3V3` | Panel logic supply | — |
| 15 | `LCD_QSPI_D1` | QSPI data 1 | **GPIO16** |
| 16 | `GND` | Ground | — |
| 17 | `LCD_QSPI_D2` | QSPI data 2 | **GPIO17** |
| 18 | `GND` | Ground | — |
| 19 | `LCD_QSPI_D3` | QSPI data 3 | **GPIO18** |
| 20 | `GND` | Ground | — |
| 21 | `LCD_RST` | Display reset | **GPIO21** |
| 22 | `GND` | Ground | — |
| 23 | **`LCD_TE`** | Tearing-effect output from the panel | **not routed — see §3.2** |
| 24 | `GND` | Ground | — |
| 25 | `GND` | Shield / mounting tab | — |
| 26 | `GND` | Shield / mounting tab | — |
| 27 | `GND` | Shield / mounting tab | — |
| 28 | `GND` | Shield / mounting tab | — |

Observations:

- **The odd pins carry signal, the even pins carry power, ground and backlight.** That is a deliberate and sensible arrangement for an FPC — every signal has an adjacent return.
- **Nine ground pins** (16, 18, 20, 22, 24, plus four tabs 25–28). Generous, and appropriate for a QSPI bus running at tens of megahertz next to a capacitive touch sensor.
- **Two supply pins and two pins each for `LEDA`/`LEDK`.** The doubled backlight pins normally indicate two parallel LED strings, or simply current-carrying capacity. §4.
- **Pin 10 is explicitly no-connect**, marked with a cross in the schematic. Its function on the module is unknown; on comparable modules this position is often `IM`/interface-mode select or a second reset.

**Caveat.** This table is read from a raster PNG. It is unambiguous at 700% magnification and the odd/even signal/power alternation is self-consistent, but **verify by continuity before you rely on it for a repair or a replacement module.** In particular, an FPC connector's pin 1 orientation is a physical convention that a schematic symbol does not establish.

## 3. The display bus

### 3.1 QSPI, and what it means

The panel is driven over **QSPI** — quad SPI, four bidirectional data lines instead of one — on the ESP32-S3's SPI2 host **[SCH, SRC]**:

| Signal | GPIO |
|---|---:|
| `LCD_QSPI_SCL` (PCLK) | 13 |
| `LCD_QSPI_CS` | 14 |
| `LCD_QSPI_D0` | 15 |
| `LCD_QSPI_D1` | 16 |
| `LCD_QSPI_D2` | 17 |
| `LCD_QSPI_D3` | 18 |
| `LCD_RST` | 21 |

**There is no D/C (data/command) pin.** QSPI display controllers of this class encode the command/data distinction in the transaction itself (a 1-line command phase followed by a 4-line data phase), which is why the pin count is lower than a comparable parallel or 3-wire SPI panel. That also means you cannot drive this panel with a generic SPI display driver — it needs a QSPI-aware one.

Bandwidth arithmetic for a full-screen 16 bpp update **[INF]**:

```
360 × 360 × 2 bytes = 259 200 bytes = 2 073 600 bits
At 4 bits per clock: 518 400 clocks per frame
At 40 MHz PCLK: 13.0 ms per full frame  -> ~77 fps ceiling
At 80 MHz PCLK:  6.5 ms per full frame  -> ~154 fps ceiling
```

So the bus is not the bottleneck for a UI; LVGL's rendering and the PSRAM framebuffer traffic will be. The vendor's LVGL configuration uses a partial buffer of `EXAMPLE_LCD_V_RES / 10` = **36 lines** **[SRC `lcd_config.h`]**, i.e. 36 × 360 × 2 = 25 920 bytes per buffer — a partial-refresh strategy rather than a full framebuffer.

### 3.2 ⚠ `TE` exists on the connector but goes nowhere

Pin 23 is `LCD_TE`, the panel's tearing-effect output. **The net-alias table on schematic sheet 2 leaves its MCU GPIO blank** **[SCH]**, so:

- **No ESP32-S3 GPIO is connected to `TE`.**
- **You cannot synchronise writes to the panel's internal refresh.**
- **Tearing artefacts during fast animation cannot be eliminated in the usual way.**

This is already recorded in [pinouts-and-buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md). It is worth restating here because it is a *panel* limitation with a visible consequence.

Mitigations, in order of effectiveness **[INF]**:

1. **Write in small partial regions** (LVGL's default with a 36-line buffer already does this). A tear across 36 lines is far less visible than one across 360.
2. **Double-buffer in PSRAM** and push a complete, consistent frame each time. Removes intra-frame inconsistency but not the tear itself.
3. **Slow the animation.** Tearing is only visible on fast horizontal motion.
4. **If you are respinning:** route `TE` to a spare S3 GPIO. It is one wire and it is already on the connector.

### 3.3 Reset

`LCD_RST` is on **GPIO21**, direct, with no pull resistor **[SCH]**. The S3's GPIOs are high-impedance out of reset, so the panel's reset state during the boot window is **undefined** — drive `LCD_RST` explicitly and early. The `esp_lcd` panel driver's `reset_gpio_num` handles this if you configure it.

### 3.4 Which driver to use

**This is the board's most-discussed ambiguity and it is not resolved here.** In brief:

- Waveshare's product/wiki text says **ST77916** **[WEB]**
- Waveshare's own shipped source is `esp_lcd_sh8601.c` / `.h` and identifies **SH8601** **[SRC]**
- The vendor demo works, so the SH8601 command set is at minimum *compatible* with whatever is fitted

**Use the vendor's `esp_lcd_sh8601` driver**, because it is the one with empirical support on this hardware. Full treatment on the two dedicated pages: [generic/sh8601-compatibility-driver](../sh8601-compatibility-driver/README.md) and [sitronix/st77916](../../sitronix/st77916/README.md).

## 4. Backlight

### 4.1 The circuit **[SCH sheet 1]**

```
3V3 ── LEDA (U5 pins 6, 8) ──[ panel LED string ]── LEDK (U5 pins 2, 4)
                                                        │
                                                   R3  3.9 Ω
                                                        │
                                                   Q1 (AO3400A) drain
LCD_BLK (GPIO47) ──┬── Q1 gate
                  R4 10 kΩ
                   └── Q1 source ── GND
```

**There is no constant-current LED driver.** `R3` is a plain ballast resistor. The full analysis, including why this makes backlight current strongly dependent on the LEDs' forward voltage and on temperature, is in [tlv62569dbvt §4](../../texas-instruments/tlv62569dbvt/README.md#4--the-backlight-is-the-load-to-worry-about); the switch itself is [alpha-and-omega-semiconductor/ao3400a](../../alpha-and-omega-semiconductor/ao3400a/README.md).

The short version: **backlight current on this board is somewhere in the tens of milliamperes, is not calculable from the schematic because the LED `Vf` is unknown, will vary board-to-board, and will rise as the panel warms.** Measure it across `R3` if you need the number.

Because `LEDA` is tied directly to a **3.3 V** rail, the LED string forward voltage must be **below 3.3 V** — so the LEDs are in **parallel, not in series** **[INF]**. That constrains any replacement module: a panel whose backlight expects a boosted supply (a series string at 9–20 V, which is common) **will not work on this board.**

### 4.2 PWM control

Backlight dimming is LEDC PWM on **GPIO47**, **50 kHz**, 8-bit (256 steps), `LEDC_TIMER_3` / `LEDC_CHANNEL_1`, clock source `LEDC_SLOW_CLK_RC_FAST` **[SRC `lcd_bl_pwm_bsp.c`]**:

```c
void lcd_bl_pwm_bsp_init(uint16_t duty);      // call once
void setUpdutySubdivide(uint16_t duty);       // 0..255
```

Two improvements worth making, both explained at [ao3400a §4](../../alpha-and-omega-semiconductor/ao3400a/README.md#4-driving-it-the-pwm-configuration):

- **Raise the resolution to 10 bits and switch off `RC_FAST`.** 8 bits is coarse at low brightness, and the RC oscillator is imprecise; `LEDC_AUTO_CLK` is a one-line change.
- **Apply a gamma curve.** Linear duty looks wrong to the eye.

One caution specific to this board: **the microphone shares the 3.3 V rail with the backlight**, so a brightness *ramp* is an audio-band current modulation. See [memsensing/msm261d4030h1cpm §6](../../memsensing/msm261d4030h1cpm/README.md#6-power-and-noise).

### 4.3 It is the board's largest steady load

Turning the backlight off is by far the most effective single power saving available. See [generic/lipo-102035](../lipo-102035/README.md) for what that does to runtime.

## 5. Touch

The capacitive touch controller is **on the same module**, reached through connector pins 1, 3, 5 and 7 **[SCH]**:

| Signal | GPIO | Note |
|---|---:|---|
| `TP_INT` | 9 | Interrupt, active low |
| `TP_RST` | 10 | Reset |
| `TP_SDA` | 11 | **Shared I2C bus** |
| `TP_SCL` | 12 | **Shared I2C bus** |

The controller is a **CST816D at I2C address 0x15** **[SCH, SRC]**, sharing GPIO11/12 with the DRV2605L haptic driver at 0x5A. Bus pull-ups are `R5`/`R6`, 5.1 kΩ to 3V3 **[SCH]**. Full treatment on [hynitron/cst816d](../../hynitron/cst816d/README.md).

**The relevant panel-level point:** because the touch controller is integrated into the module, **the touch layer cannot be replaced independently of the display**, and any replacement module must present a CST816-compatible controller at 0x15 on the same four pins — or you will be rewriting the touch driver as well as the display driver.

The touchscreen is also, on this board, **the only "press" input** — neither knob has a push contact. See [alps-alpine/sscm110100 §2.2](../../alps-alpine/sscm110100/README.md#22-there-is-no-push-contact-on-either-knob).

## 6. Round-display and viewing considerations

The panel is round, but the framebuffer is a 360 × 360 **square** **[SRC]**. That has consequences that are easy to get wrong **[INF]**:

1. **The corners exist in memory but are not visible.** Roughly `1 − π/4 = 21%` of the framebuffer is off-panel. Rendering content there wastes bandwidth and, worse, quietly loses UI elements.
2. **The safe area is a circle of radius 180 px centred at (180, 180).** Anything whose bounding box extends beyond `√((x−180)² + (y−180)²) ≤ 180` is at risk. In practice the mechanical bezel eats a few more pixels, and **how many is unknown** because the module's active-area diameter is not documented.
3. **LVGL has no built-in round-display awareness in 8.x** (the vendored version **[SRC]**). You lay out for the circle yourself. `lv_arc`, circular `lv_obj` with `lv_obj_set_style_radius(obj, LV_RADIUS_CIRCLE, 0)`, and radial layouts are your friends. LVGL 9 added better support for non-rectangular displays.
4. **Text near the edge will be clipped by the bezel before it is clipped by the framebuffer.** Keep a generous margin — 20 px is a reasonable starting guess in the absence of a mechanical drawing.
5. **The panel is under a knob that the user rotates.** Fingerprints and the rotation mechanism both mean the visible area in practice is smaller than the optical one.

`EXAMPLE_Rotate_90` exists as a commented-out `#define` in `lcd_config.h` **[SRC]**, so rotation support is at least partially present in the vendor driver — but on a round display, rotation is mostly meaningful for content orientation rather than aspect.

## 7. Pitfalls

1. **Do not treat this as a generic SPI display.** It is QSPI with no D/C pin. §3.1.
2. **Do not expect `TE`.** It is on the connector and unrouted. §3.2.
3. **Do not assume the corners are visible.** §6.
4. **Do not source a "1.8 inch 360×360 round" replacement and expect it to work.** It must match on: QSPI interface, SH8601-compatible command set, CST816-compatible touch at 0x15, **3.3 V parallel backlight** (§4.1), 28-pin FPC with this exact pinout, and the mechanical envelope. That is a lot of coincidences.
5. **Drive `LCD_RST` explicitly at startup.** §3.3.
6. **Backlight current is not a known quantity.** §4.1.
7. **The controller identity conflict is unresolved.** Do not "fix" the driver to match the marketing name. §3.4.
8. **The touch controller is part of the module** and shares an I2C bus with the haptic driver — serialise access. §5.

## 8. Open questions

Everything in §1.2, plus:

| Question | How it could be closed |
|---|---|
| Module part number / maker | Disassembly and a photograph of the FPC marking |
| Which controller is fitted | Read the display ID over QSPI at runtime and log it. The vendor driver already checks for `0x86` |
| Active-area diameter and safe-margin pixels | Mechanical measurement |
| LED `Vf`, string count and backlight current | Measure across `R3` |
| Whether the panel drives `TE` at all | Probe connector pin 23 during a refresh |
| Optical specifications | Only a datasheet or measurement |

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — `U5`, ESP32-S3 QSPI on GPIO13–18 + GPIO21, touch on GPIO9–12, backlight on GPIO47

## Related pages

- [generic/sh8601-compatibility-driver](../sh8601-compatibility-driver/README.md) — the driver the vendor actually ships
- [sitronix/st77916](../../sitronix/st77916/README.md) — the controller the vendor's marketing names
- [hynitron/cst816d](../../hynitron/cst816d/README.md) — the touch controller on this module
- [alpha-and-omega-semiconductor/ao3400a](../../alpha-and-omega-semiconductor/ao3400a/README.md) — the backlight switch and its PWM
- [texas-instruments/tlv62569dbvt](../../texas-instruments/tlv62569dbvt/README.md) — the rail, and the backlight-current analysis
- [Pinouts and buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md)
- [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md)

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Board schematic sheet 1 — the `U5` 28-pin symbol (source of the §2 pinout) and the backlight circuit | — | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/1_LCD&POWER.png` |
| Board schematic sheet 2 — `LCD_*` and `TP_*` nets aliased to S3 GPIOs; `LCD_TE` left blank | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/2_ESP32S3-R8.png` |
| Waveshare demo `08_LVGL_Test` — `lcd_config.h`, `lcd_bsp.c`, `esp_lcd_sh8601.c`, `lcd_bl_pwm_bsp.c`, `cst816.cpp` | — | 2026-08-21 | `.../artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Arduino/examples/08_LVGL_Test/` |
| LVGL (vendored with the demo, 8.x) | https://github.com/lvgl/lvgl | 2026-08-21 | `.../artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Arduino/libraries/lvgl/` |
| ESP-IDF v5.3.2 — LCD (`esp_lcd`) driver, QSPI panel support | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32s3/api-reference/peripherals/lcd.html | 2026-08-23 | closest archived PDF: `../../espressif/esp32-s3r8/artifacts/esp-idf-programming-guide-v5.2.5-esp32s3.pdf` |
| ST77916 specification (the controller the product page names) | — | 2026-08-21 | `../../sitronix/st77916/artifacts/st77916-spec-v1.0.pdf` |
| CST816D datasheet v1.3 | — | 2026-08-21 | `../../hynitron/cst816d/artifacts/cst816d-datasheet-v1.3.pdf` |
| Waveshare product page (the "ST77916" and "1.8 inch / 360×360" claims) | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-product-31623.html` |
| Waveshare wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-wiki-current.html` |
