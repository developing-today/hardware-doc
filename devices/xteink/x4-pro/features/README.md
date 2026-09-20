# Xteink X4 Pro — feature guides

Task-oriented guides, one per fitted capability. Each answers "how do I use X on
this device" and states its evidence status.

| Guide | Capability | Evidence status |
|---|---|---|
| [`display.md`](display.md) | 800×480 e-ink, three possible controllers | hardware-confirmed (SDK) |
| [`touch.md`](touch.md) | GT911 capacitive touch + capacitive Home key | hardware-confirmed (SDK) |
| [`buttons.md`](buttons.md) | Two side keys + power | hardware-confirmed (SDK) |
| [`frontlight.md`](frontlight.md) | Dual warm/cool PWM | hardware-confirmed (SDK) |
| [`storage.md`](storage.md) | microSD via native SDMMC | hardware-confirmed (SDK) |
| [`battery-and-power.md`](battery-and-power.md) | CW2017 gauge, charge STAT, rails, sleep | hardware-confirmed (SDK) |
| [`rtc.md`](rtc.md) | BM8563 real-time clock | hardware-confirmed (SDK) |
| [`usb.md`](usb.md) | Native USB-OTG, CDC, MSC | partial — MSC not ported |
| [`wifi-and-bluetooth.md`](wifi-and-bluetooth.md) | ESP32-S3 Wi-Fi + BLE | inferred from SoC |

**Not fitted, so no guide exists:** audio (no codec, no buzzer), LEDs, IMU,
GPIO expander, PMIC, LoRa, camera, IR. The X4 Pro's `BoardProfile` sets
`NO_AUDIO`, `NO_LEDS`, `NO_MIC` and `ImuType::None`.
