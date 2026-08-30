# Feature guides — ESP32-P4-WIFI6-Touch-LCD-4C

The 4C is the **same PCB** as the [3.4C](../../esp32-p4-wifi6-touch-lcd-3.4c/README.md) with a
different panel. Only the display guide is maintained separately.

| Guide | Answers | Where |
|---|---|---|
| [display.md](./display.md) | Drive the 4 in **720 × 720** round JD9365 panel | **Here** |
| Touch | GT911 over I²C GPIO7/8 | [3.4C](../../esp32-p4-wifi6-touch-lcd-3.4c/features/touch.md) |
| Wi-Fi / Bluetooth | ESP32-C6 over SDIO | [3.4C](../../esp32-p4-wifi6-touch-lcd-3.4c/features/wifi-and-bluetooth.md) |
| Audio | ES8311 + ES7210 | [3.4C](../../esp32-p4-wifi6-touch-lcd-3.4c/features/audio.md) |
| Camera | MIPI-CSI | [3.4C](../../esp32-p4-wifi6-touch-lcd-3.4c/features/camera.md) |
| Storage | microSD — **pins unresolved** | [3.4C](../../esp32-p4-wifi6-touch-lcd-3.4c/features/storage.md) |
| Development / flashing | Dual-MCU workflow | [3.4C](../../esp32-p4-wifi6-touch-lcd-3.4c/development.md) |

When following a 3.4C guide, substitute **720 × 720** wherever a resolution appears — most
importantly `x_max`/`y_max` in the GT911 touch config, where the wrong value yields silently
mis-scaled coordinates rather than an obvious failure.

**Evidence status:** vendor documentation and vendor source code, 2026-08-24. Untested on
hardware, and **no confirmed real unit of this board was located** — see
[C2](../../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c2--4c-availability--resolved-2026-08-24).
