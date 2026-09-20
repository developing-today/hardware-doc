# Xteink X4 — feature guides

| Guide | Capability | Evidence |
|---|---|---|
| [`display.md`](display.md) | 800×480 e-ink, SSD1677/UC8179/UC8279 | SDK + measured refresh timing |
| [`buttons.md`](buttons.md) | Six buttons on a two-pin ADC ladder | SDK, with raw values from three real units |
| [`storage.md`](storage.md) | microSD over the **shared** display SPI bus | SDK |
| [`battery-and-power.md`](battery-and-power.md) | ADC sense, MOSFET latch, two board revisions | SDK |
| [`usb.md`](usb.md) | USB-C, USB-serial-JTAG | SDK + owner reports |
| [`wifi-and-bluetooth.md`](wifi-and-bluetooth.md) | ESP32-C3 Wi-Fi + BLE | inferred + firmware strings |

**Not fitted:** touch, frontlight, RTC, fuel gauge, IMU, NFC, audio, LEDs, SDMMC.
