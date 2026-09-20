# Buzzer — M5Stack PaperMono

> **How do I make a noise?**
> Hardware revision **V0.6.2** · snapshot **2026-09-01** · nothing tested on hardware.

**This is a short guide because the feature is small.** One pin, one LEDC channel, no
amplifier, no codec, and no acoustic specification from anyone.

## 1. Capability summary and the hardware path

A buzzer on the KEY/RGB sub-board, driven directly from an ESP32-S3 GPIO through the
LEDC (PWM) peripheral. Net `G42_BB_PWM`, reaching the sub-board through `J6`.

```
ESP32-S3 GPIO42 ──LEDC PWM──▶ buzzer (on the KEY/RGB sub-board, via J6)
```

There is **no** speaker, **no** amplifier and **no** DAC on this board. `M5.Speaker` is
not the right abstraction here; the vendor drives LEDC directly.

## 2. Prerequisites and resources

| Item | Value |
|---|---|
| ESP-IDF | 5.5.1 — `driver/ledc.h` |
| ESP32-S3 GPIO | **GPIO42** — the only pin involved |
| Power state | L2 — the buzzer is on the ESP32-S3's own rail; no expander pin, no switched supply |

Vendor LEDC allocation (`M5PaperMono-UserDemo/main/hal/hal_buzzer.cpp:17–29`):

| Setting | Value |
|---|---|
| Speed mode | `LEDC_LOW_SPEED_MODE` |
| **Timer** | **`LEDC_TIMER_3`** |
| **Channel** | **`LEDC_CHANNEL_7`** |
| Resolution | `LEDC_TIMER_10_BIT` |
| Duty when sounding | **512** (50 %) |
| Default frequency | 2000 Hz |
| Frequency clamp | **40 Hz – 12 000 Hz**, enforced in software |

**Timer 3 and channel 7 are deliberately at the top of the range** so they do not collide
with anything a user allocates from channel 0 upward. Keep that convention.

## 3. Minimal procedure (`inferred`)

Direct LEDC, matching the vendor's `setBuzzerOutput()` (`hal_buzzer.cpp:186–195`):

```c
#include <driver/ledc.h>

ledc_timer_config_t t = {};
t.speed_mode = LEDC_LOW_SPEED_MODE;
t.duty_resolution = LEDC_TIMER_10_BIT;
t.timer_num = LEDC_TIMER_3;
t.freq_hz = 2000;
t.clk_cfg = LEDC_AUTO_CLK;
ledc_timer_config(&t);

ledc_channel_config_t c = {};
c.gpio_num = GPIO_NUM_42;
c.speed_mode = LEDC_LOW_SPEED_MODE;
c.channel = LEDC_CHANNEL_7;
c.timer_sel = LEDC_TIMER_3;
c.duty = 0;
ledc_channel_config(&c);

// tone
ledc_set_freq (LEDC_LOW_SPEED_MODE, LEDC_TIMER_3, 1000);
ledc_set_duty (LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_7, 512);   // 50 %
ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_7);

// silence
ledc_stop(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_7, 0);
```

The factory firmware wraps this in a FreeRTOS task with a 6-deep command queue,
supporting `playBuzzer(freq, ms)`, `playBuzzerSweep(start, end, ms)`,
`playBuzzerPattern(tones, count)`, `stopBuzzer()` and `setBuzzerMuted(bool)` — with sweep
steps updated every 2 ms. That structure is worth copying if you want non-blocking tones;
it is application code, not a library.

## 4. Limits

| Class | Limit |
|---|---|
| **Board** | **Square wave only.** 50 % duty, one channel — no volume control, no waveform, no polyphony |
| **Board** | No amplifier, no speaker, no line out |
| **Framework (vendor app)** | 40 Hz – 12 kHz clamp, 10-bit resolution |
| **Unknown** | The buzzer part is not identified in any document retrieved. **Its resonant frequency is unknown**, so the loudest tone is unknown |

Because the resonant frequency is undocumented, "which frequency is loudest" is an
empirical question nobody has answered. Magnetic buzzers of this size typically peak
around 2–4 kHz, and the vendor's 2000 Hz default is consistent with that — but that is a
guess about a part we cannot name, `inferred` and worth nothing without a measurement.

## 5. Conflicts

| Combination | Verdict | Mechanism |
|---|---|---|
| Buzzer + your own `ledcWrite`/LEDC use | ⚠ | Vendor uses **timer 3, channel 7**. Start your allocations at 0 |
| Buzzer + [microphone](microphone.md) | ✅ works, acoustically obvious | The buzzer is audible in any recording |
| Buzzer + [sleep](power-and-sleep.md) | ⚠ | The vendor's shutdown path explicitly **drives GPIO42 low** (`app_shutdown.cpp:118–119`) before powering down. Do the same, or you may leave it energised |
| Buzzer + [display](epaper-display.md) | ✅ | Unrelated |

## 6. Debugging

| Symptom | Cause |
|---|---|
| No sound | Duty left at 0, or `ledc_update_duty()` not called |
| Sound continues after shutdown | GPIO42 not driven low before the rail drops |
| Your PWM elsewhere stopped working | You reused timer 3 or channel 7 |
| Very quiet at some frequencies | Off-resonance; the resonant frequency is undocumented |

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**; fitted on both C153 and C153-LITE |
| Framework range | ESP-IDF 5.5.1 · arduino-esp32 3.3.10 |
| Evidence | Pin and LEDC allocation: **read from vendor source** (`hal_buzzer.cpp`), `executed-success`. Sketch: **`inferred`**. Acoustics: **unknown** |
| Confidence | High on the wiring and driver setup; **none on loudness or tone quality** |
| Last verified | **2026-09-01** |

## Related

- [`../pinouts-and-buses.md`](../pinouts-and-buses.md) · [`microphone.md`](microphone.md) · [`power-and-sleep.md`](power-and-sleep.md) · [`../resources-and-conflicts.md`](../resources-and-conflicts.md)
