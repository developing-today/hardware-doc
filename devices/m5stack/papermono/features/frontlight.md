# Frontlight — M5Stack PaperMono

> **How do I set the frontlight brightness, and why is the curve strange?**
> Hardware revision **V0.6.2** · snapshot **2026-09-01** · nothing tested on hardware.

## 1. Capability summary and the hardware path

An LED frontlight bonded to the e-paper stack, driven by a boost converter producing a
15 V rail, dimmed by a PWM input from the **power-management chip** — not from the
ESP32-S3 and not from the I/O expander.

```
M5PM1 GPIO3 (PWM0) ──▶ AW9967 boost (U11) ──▶ BL_15V_L3B ──▶ frontlight FPC (J1)
                              ▲
                              └── BL_FB current feedback, set by R29
```

| Element | Part | Record |
|---|---|---|
| Dimming PWM source | M5PM1 `G3`, net `PYG3_BL_PWM`, pin 13 | [`components/m5stack/m5pm1`](../../../../components/m5stack/m5pm1/README.md) |
| Boost driver | Awinic **AW9967**, designator `U11` | [`components/awinic/aw9967`](../../../../components/awinic/aw9967/README.md) |
| Connector | `J1`, 6-pin — `PYG3_BL_PWM`, `BL_FB`, `BL_15V_L3B` | [`../pinouts-and-buses.md`](../pinouts-and-buses.md#connectors) |

> ⚠ **`PYG3` is the most dangerous token in this device's documentation.** On the
> **M5PM1** it is the *net* name of the frontlight PWM pin. On the **M5IOE1** it is the
> *symbol pin* name of the **e-paper 3.3 V rail enable**. Writing to the wrong one cuts
> the display's power and reports no error. Read
> [`../pin-naming-and-the-pyg-ambiguity.md`](../pin-naming-and-the-pyg-ambiguity.md)
> before touching either.

## 2. Prerequisites

| Item | Value |
|---|---|
| M5Unified / M5GFX | 0.2.21 / 0.2.28 — `Light_M5PaperMono` is registered as the board's backlight class |
| M5PM1 library | 1.0.7 (registry `m5stack/m5pm1`) if you drive it directly |
| Power state | **L3B** — the boost rail belongs to the top state; enabled during `M5.begin()` |
| I²C | The M5PM1 at `0x6E` must be reachable. No I²C, no dimming |

## 3. Resources consumed

| Resource | Value |
|---|---|
| M5PM1 GPIO | `G3`, driven as **PWM0** (`GPIO_FUNC0` bit pattern `0xC0`, `GPIO_DRV` bit 3 cleared → push-pull) |
| M5PM1 registers | `0x13` drive, `0x16` function, `0x30`/`0x31` PWM0 duty, `0x34`/`0x35` PWM frequency |
| PWM frequency | **5000 Hz**, written by M5GFX |
| ESP32-S3 GPIO | **none** — this costs you no host pin at all |
| Rail | `BL_15V_L3B` (state L3B) |

## 4. Minimal procedure (`inferred`)

The M5GFX route is one call:

```cpp
#include <M5Unified.h>

void setup() {
  M5.begin(M5.config());
  M5.Display.setBrightness(128);   // 0-255; see §5 - this is NOT half brightness
}
```

`M5.Display.setBrightness(0)` writes `0x31 = 0` and turns the boost off.

Driving the M5PM1 directly, if you want a different frequency or a linear curve
(shape taken from the vendor's published M5PM1 examples; `inferred`):

```cpp
#include <M5PM1.h>
M5PM1 pm1;

pm1.begin(&M5.In_I2C, M5PM1_DEFAULT_ADDR, M5PM1_I2C_FREQ_100K);
pm1.gpioSetDrive(M5PM1_GPIO_NUM_3, M5PM1_GPIO_DRIVE_PUSHPULL);
pm1.gpioSetFunc (M5PM1_GPIO_NUM_3, M5PM1_GPIO_FUNC_PWM);
pm1.setPwmFrequency(20000);                       // inside the AW9967's rated 10-100 kHz
pm1.setPwmDuty12bit(M5PM1_PWM_CH0, 2048, false, true);   // ~50 % linear
```

The API names above are transcribed from `M5PM1/src/M5PM1.h`
(`setPwmFrequency`, `setPwmDuty12bit`, `analogWrite`, `gpioSetFunc`, `gpioSetDrive`).
**The channel constant spelling was not verified** — the header's PWM channel enum was
not read in this pass, and the M5PM1 manual is internally inconsistent about
PWM0/PWM1 versus PWM1/PWM2 naming. Check it before compiling.

## 5. Three things M5GFX does that will surprise you

All three are software or documentation issues, not hardware faults, and all three are
fixable without touching the board.

### 5.1 The brightness curve is squared, not linear

`M5GFX.cpp:849`: `br = brightness * brightness`, then the duty registers get
`(br >> 4) & 0xFF` and `(br >> 12) | 0x10`. A commented-out linear write sits directly
above it at `:847`.

So **`setBrightness(128)` is roughly a quarter of full output, not half.** If your UI
shows a linear slider, it is lying to the user. Apply a square-root correction, or write
the registers yourself.

### 5.2 The PWM frequency is below the driver's rated range

M5GFX programs `0x34`/`0x35` to **5000 Hz**. The AW9967 datasheet specifies a
**10–100 kHz** dimming input range. Below the specified range, dimming linearity and
audible behaviour are not guaranteed — a 5 kHz square wave into an inductor-based boost
converter is inside the audible band.

**Framework limit**, not a board limit. Rewriting `0x34`/`0x35` to 20–50 kHz after
`M5.begin()` is a one-line change. Untested — nobody has reported whether the PaperMono
audibly whines. Tracked as
[`../gaps-and-conflicts.md` C5](../gaps-and-conflicts.md#c5--frontlight-pwm-frequency-below-the-drivers-rated-range).

### 5.3 The schematic's own current annotation is stale

The sheet-2 note claims `Iset = 15 mA` with `Rset = 11 R`. The **fitted `R29` is 18 Ω**,
which gives roughly **11 mA**, and the note's arithmetic is internally inconsistent with
its own formula. Treat the annotation as stale; treat 11 mA as the better estimate,
`inferred` and unmeasured.

## 6. Silicon / board / framework / observed limits

| Class | Limit |
|---|---|
| **Silicon (AW9967)** | 10–100 kHz rated dimming input |
| **Board** | LED current set by `R29 = 18 Ω` → ~11 mA. Not adjustable in software |
| **Board** | Boost rail lives in state **L3B**; there is no way to light the frontlight from L0/L1/L2 |
| **Framework** | 5 kHz PWM (out of range) and a squared gamma curve |
| **Observed** | One third-party project (`MagicCube/free-ink-on-paper-mono`, hardware-validated on a Lite) holds the frontlight at a fixed **127/255**. That is the only real-world brightness setting anyone has published |

**No power figure exists.** Nobody has published frontlight current draw or its effect on
battery life, and none was derived here.

## 7. Conflicts and simultaneous use

| Combination | Verdict | Mechanism |
|---|---|---|
| Frontlight + [display](epaper-display.md) | ✅ the intended pairing | Different chips: panel rail is M5IOE1 `IO3`, frontlight is M5PM1 `G3` |
| Frontlight + deep sleep | ❌ mutually exclusive | The boost rail is L3B; sleeping drops below it |
| Frontlight + [battery life](battery-and-charging.md) | ⚠ unquantified | An always-on LED string on a 1150 mAh cell. No measurement exists |
| Frontlight + other M5PM1 PWM users | ⚠ shared frequency | The M5PM1's `PWM_FREQ` register is **global to both its PWM channels** — you cannot give the frontlight 20 kHz and another channel 1 kHz |
| Frontlight PWM + M5PM1 I²C idle-sleep | ⚠ | M5Stack documents that I²C idle sleep is disabled while PWM is enabled on the companion M5IOE1; the M5PM1 manual carries the same restriction |

## 8. Debugging

| Symptom | Cause |
|---|---|
| No light at any brightness | Not in state L3B; or `M5.begin()` was skipped; or the M5PM1 is unreachable on I²C |
| **Screen went blank when you changed brightness** | You wrote **M5IOE1 `IO3`** instead of M5PM1 `G3`. You cut the panel rail |
| Brightness "feels wrong" in the low half | The squared curve (§5.1) |
| Audible whine | 5 kHz PWM below the AW9967's rated range (§5.2). Unconfirmed on hardware |
| Brightness changes but never reaches full | 12-bit duty; check you are writing both duty bytes together |

## 9. Alternatives

There are none. The frontlight has exactly one control path — M5PM1 `G3` → AW9967 — and
no host GPIO reaches it. Your only choices are *how* you drive that PWM (M5GFX's curve,
or your own register writes).

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**; frontlight is fitted on both C153 and C153-LITE |
| Framework range | M5Unified 0.2.21 · M5GFX 0.2.28 · M5PM1 library 1.0.7 |
| Evidence | Wiring: **schematic**, `executed-success` extraction. M5GFX behaviour: **read from source** at `M5GFX.cpp:819–856`. Code sketch: **`inferred`**, and one identifier explicitly unverified |
| Confidence | High on the signal path; **medium on the API sketch**; low on anything electrical |
| Last verified | **2026-09-01** |

## Related

- [`../power-architecture.md#frontlight`](../power-architecture.md#frontlight) · [`../pin-naming-and-the-pyg-ambiguity.md`](../pin-naming-and-the-pyg-ambiguity.md)
- [`epaper-display.md`](epaper-display.md) · [`power-and-sleep.md`](power-and-sleep.md) · [`io-expander.md`](io-expander.md)
- [`components/awinic/aw9967`](../../../../components/awinic/aw9967/README.md) · [`components/m5stack/m5pm1`](../../../../components/m5stack/m5pm1/README.md)
