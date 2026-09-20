# GPIO, ADC and PWM — XIAO ESP32S3 Sense

> What you can actually connect, given that the daughterboard takes most of the pins.
> Snapshot **2026-08-24**. No hardware testing.

## 1. The eleven pins you get

| Silk | Arduino | GPIO | ADC | Default peripheral | Safe as plain GPIO? |
|---|---|---:|---|---|---|
| D0 | `D0`/`A0` | 1 | ADC1_CH0 | — | ✅ |
| D1 | `D1`/`A1` | 2 | ADC1_CH1 | — | ✅ |
| D2 | `D2`/`A2` | 3 | ADC1_CH2 | — | ⚠ **strapping** (JTAG source select) |
| D3 | `D3`/`A3` | 4 | ADC1_CH3 | — | ✅ |
| D4 | `D4`/`A4` | 5 | ADC1_CH4 | I²C **SDA** | ✅ if not using `Wire` |
| D5 | `D5`/`A5` | 6 | ADC1_CH5 | I²C **SCL** | ✅ if not using `Wire` |
| D6 | `D6`/`TX` | 43 | — | UART0 TX | ⚠ console by default |
| D7 | `D7`/`RX` | 44 | — | UART0 RX | ⚠ console by default |
| D8 | `D8`/`A8` | 7 | ADC1_CH6 | SPI **SCK** | ❌ **microSD** |
| D9 | `D9`/`A9` | 8 | ADC1_CH7 | SPI **MISO** | ❌ **microSD** |
| D10 | `D10`/`A10` | 9 | ADC1_CH8 | SPI **MOSI** | ❌ **microSD** |

Plus `3V3` (output, 600 mA rail), `GND`, and `5V` (`VBUS`, 0 V on battery).

**With the Sense board fitted and an SD card in use, you realistically have four free pins: GPIO1, 2, 3, 4** (and GPIO5/6 if you skip I²C). That is the real constraint of this board and it should shape the design before anything else.

## 2. Pins that do not exist for you

| GPIO | Why |
|---|---|
| **33–37** | **In-package octal PSRAM.** No-connect on the PCB. Using them corrupts memory rather than erroring |
| 26–32 | SPI flash / PSRAM interface |
| 19, 20 | Native USB |
| 10–18, 21, 38–42, 47, 48 | Consumed by the Sense daughterboard |
| 45, 46 | Strapping pins, **no-connect** on this board (safely inert) |

GPIO33–37 deserve emphasis: configuring them raises **no error**. The failure appears as a cache-access panic or a crash the moment the camera allocates a framebuffer — far from the offending line. See [`../pinouts-and-buses.md` §7.5](../pinouts-and-buses.md#75-gpio33gpio37-do-not-exist-for-you).

## 3. ADC

All nine analog-capable pins are **ADC1**. ADC2 is not exposed.

This is a genuinely good outcome: the widely-known ESP32 problem where **ADC2 becomes unusable while Wi-Fi is active does not apply here.** You can sample analog inputs and run Wi-Fi simultaneously without the usual workarounds.

- Resolution: 12-bit by default (`analogRead()` → 0–4095).
- Input range: 0–3.3 V with the default 11 dB attenuation, though the top of the range is non-linear.
- Use `analogReadMilliVolts()` (Arduino) or `esp_adc_cal` (IDF) for calibrated readings — raw counts are not accurate without correction.
- The numbering gap (`A6`/`A7` absent) is real and follows the ESP32-S3 channel map, not a documentation error.

## 4. PWM (LEDC)

The ESP32-S3 LEDC has **8 low-speed channels and 4 timers**. The ESP32-S3 has **no high-speed LEDC mode** — this differs from the original ESP32 and catches ported code out.

**The camera consumes one channel and one timer** (`LEDC_CHANNEL_0` / `LEDC_TIMER_0` by convention) to generate `XCLK`. If you drive servos or LEDs, **start at channel 1** — reusing channel 0 disturbs the camera clock and produces torn or green frames.

That leaves 7 channels and 3 timers, which is far more than the free pin count, so LEDC is not your binding constraint.

```cpp
// Arduino-ESP32 3.x
ledcAttachChannel(D0, 5000 /*Hz*/, 12 /*bits*/, 1 /*channel — NOT 0*/);
ledcWrite(D0, 2048);
```

## 5. I²C

`Wire` on **GPIO5 (SDA) / GPIO6 (SCL)**. **No devices are fitted on this bus** — it is genuinely free, and it is the best way to add peripherals given the pin scarcity, since many devices share two pins.

⚠ The camera's SCCB bus is **GPIO39/40**, a *separate* bus. Scanning `Wire` will never find the camera.

## 6. Strapping pins

| GPIO | Role | Exposed? | Risk |
|---|---|---|---|
| 0 | Boot mode | No (BOOT button) | Low |
| **3** | JTAG source select | **Yes, as `D2`** | External pull-ups/downs affect debug routing |
| 45 | VDD_SPI select | **No-connect** | None |
| 46 | ROM message printing | **No-connect** | None |

Seeed leaving 45/46 unconnected removes two classic ESP32-S3 footguns. Only `D2` needs care — avoid strong external pulls on it if you care about debugging, and prefer `D0`/`D1`/`D3` for anything with a pull-up.

## 7. Electrical limits

Standard ESP32-S3 figures — **not board-specific measurements**:

- Logic level **3.3 V**; inputs are **not 5 V tolerant**.
- Per-pin drive is configurable (5/10/20/40 mA capability); ~20 mA is the practical continuous sink/source.
- Total draw across all your peripherals shares the **600 mA** 3.3 V rail with the SoC and camera.
- The user LED (GPIO21) is **active-LOW** — and is also the SD chip-select. See [`microsd.md` §4](microsd.md#4-the-chip-select-collision).

## 8. Related
- [`../pinouts-and-buses.md`](../pinouts-and-buses.md) · [`../resources-and-conflicts.md`](../resources-and-conflicts.md)
- [ESP-IDF peripheral capabilities](../../../../guides/espressif/esp-idf-peripheral-capabilities.md) — S3 is `LEDC_LOW_SPEED_MODE` only
