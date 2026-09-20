# How do I make the DinMeter beep?

**Applies to:** K134 and K134-V11 (identical).
**Evidence status:** wiring `executed-success` from the schematic; GPIO confirmed by two
independent sources; code `reported-working` (vendor examples). **Last verified:** 2026-09-04.

---

## Hardware path

```
ESP32-S3 GPIO3 ──"beep"──► R25 470Ω ──► Q5 SS8050 (NPN, low-side) ──► LS1 buzzer ──► +5VIN
                                                                        D6 1N4148WT flyback
```

The flyback diode across `LS1` means this is an **electro-magnetic (inductive) buzzer, not a
piezo**. It is **passive**: it needs a square wave. Writing a DC level makes one click.

Component: [`components/unidentified/m5stack-dinmeter/buzzer`](../../../../components/unidentified/m5stack-dinmeter/buzzer/README.md)
— the part number is not published.

## Which GPIO — and why that needed checking

The vendor PinMap renders `BEEP` (G3) and `BTN(WAKE)` (G42) in adjacent rows of the same table,
which is easy to misread. Espressif's board definition flags exactly this and resolves it from
M5Unified:

> *"The vendor pin table renders GPIO3 and GPIO42 in adjacent rows; M5Unified settles it:
> `board_M5DinMeter` sets `spk_cfg.pin_data_out = GPIO_NUM_3` with `spk_cfg.buzzer = true`
> (`M5Unified.cpp`, `_set_speaker` branch), and reads the encoder button as
> `!gpio_in(GPIO_NUM_42)` (`_update_button_state`)."*

The schematic agrees: `M1` pad 3 = `G3`, net `beep`. **Buzzer = GPIO3. Button = GPIO42.**

## Arduino

```cpp
#include "M5DinMeter.h"
void setup() {
    auto cfg = M5.config();
    DinMeter.begin(cfg, true);
}
void loop() {
    DinMeter.Speaker.tone(10000, 100);   // 10 kHz for 100 ms
    delay(1000);
    DinMeter.Speaker.tone(4000, 20);     // 4 kHz for 20 ms
    delay(1000);
}
```
Verbatim from `M5DinMeter/examples/Basic/buzzer/buzzer.ino` (release 1.0.0).
`reported-working`.

`DinMeter.Speaker` is a reference to `M5.Speaker`, a `Speaker_Class` (`M5DinMeter.h:24`), which
M5Unified configures for this board as:

```cpp
// M5Unified/src/M5Unified.cpp:2921-2928
case board_t::board_M5Dial:
case board_t::board_M5DinMeter:
  if (cfg.internal_spk) {
    spk_cfg.pin_data_out  = GPIO_NUM_3;
    spk_cfg.buzzer        = true;
    spk_cfg.magnification = 48;
  }
  break;
```

`buzzer = true` puts `Speaker_Class` into square-wave mode rather than PWM-audio mode, so
`tone()` works but `playWav()` / `playRaw()` will be a buzz, not speech. `magnification = 48`
is the vendor's volume scaling.

Useful idiom, from `encoder.ino` — a 20 ms click at 8 kHz per detent gives the knob tactile
audio feedback:
```cpp
if (newPosition != oldPosition) DinMeter.Speaker.tone(8000, 20);
```

## ESP-IDF

There is no "buzzer" abstraction; use **LEDC**. Espressif's board definition supplies the
configuration and explains why:

> *"A passive buzzer is driven by a PWM tone, so the LEDC channel is the peripheral; there is no
> bmgr buzzer device type, and `ledc_ctrl` models a duty percentage rather than a frequency."*

| Field | Value |
|---|---|
| `gpio_num` | 3 |
| `channel` | `LEDC_CHANNEL_1` |
| `timer_sel` | `LEDC_TIMER_1` |
| `freq_hz` | 4000 (starting point; change per note) |
| `duty` | 0 (silent until you raise it) |
| `duty_resolution` | `LEDC_TIMER_10_BIT` |
| `speed_mode` | `LEDC_LOW_SPEED_MODE` |

Change pitch with `ledc_set_freq()`, change loudness with duty (50 % is loudest for a square
wave). `inferred` for the loudness statement.

## Frequencies

The vendor's own examples use **4 000 Hz**, **8 000 Hz** and **10 000 Hz**. The buzzer's
resonant frequency — where it is loudest — is **not published**, and a magnetic buzzer's output
falls off sharply away from resonance. If loudness matters, sweep and measure. `not-tested`.

## Resource cost and conflicts

| Resource | Used |
|---|---|
| GPIO | 3 |
| LEDC | channel 1 + **timer 1** |

⚠ **The backlight also wants LEDC** (channel 0, timer 0). They are on different timers by
design, so both work together — but if you write your own LEDC setup, do not put the backlight
and the buzzer on the same timer: changing the buzzer's frequency would change the backlight's
PWM frequency too. This is the only real resource conflict on the board. See
[`../resources-and-conflicts.md`](../resources-and-conflicts.md).

**Power note.** `LS1` is driven from `+5VIN`. On battery-only operation that rail comes from a
boost; expect the buzzer to be quieter and to load the boost during a tone.

## Pitfalls

| Symptom | Cause |
|---|---|
| One click, then silence | DC level instead of a square wave — it is a passive buzzer |
| Silent | `cfg.internal_spk` disabled, or duty still 0 |
| Backlight flickers when the buzzer sounds | you put both on the same LEDC timer |
| Very quiet | off resonance, or running on battery |
| Tone blocks the UI | `Speaker.tone()` is non-blocking in M5Unified; `delay()` after it is what blocks |
