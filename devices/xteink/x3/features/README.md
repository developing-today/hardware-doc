# Xteink X3 — feature guides

| Guide | Capability | Evidence |
|---|---|---|
| [`display.md`](display.md) | 792×528, UC8253 **or** UC8279d | SDK; UC8279d path **unvalidated on hardware** |
| [`imu.md`](imu.md) | QMI8658 6-axis, motion page turn | SDK + two teardowns |
| [`rtc.md`](rtc.md) | DS-series RTC — **part unresolved** | SDK vs teardown conflict |
| [`battery-and-power.md`](battery-and-power.md) | BQ27220 gauge, 650 mAh, pogo charging | SDK + teardown |
| [`storage.md`](storage.md) | microSD on the shared SPI bus, with a power rail | SDK |
| [`nfc.md`](nfc.md) | ISO 14443A tag — **purpose unknown** | Chinese teardown + vendor claim |
| Buttons | Identical to the X4 | see [`../../x4/features/buttons.md`](../../x4/features/buttons.md) |
| Wi-Fi / BLE | Identical SoC to the X4 | see [`../../x4/features/wifi-and-bluetooth.md`](../../x4/features/wifi-and-bluetooth.md) |

**Not fitted:** touch, frontlight, audio, LEDs, SDMMC, PSRAM.
