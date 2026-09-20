# Cardputer ADV — feature guides

Task-oriented guides. Each answers a natural question, names the exact hardware path,
the software options, the resources consumed and the ways it fails.

| Guide | Question it answers | Hardware |
|---|---|---|
| [`keyboard.md`](keyboard.md) | How do I read the keyboard? | TCA8418RTWR @ I²C `0x34`, INT G11 |
| [`display.md`](display.md) | How do I draw on the screen and dim it? | ST7789V2, SPI3, backlight G38 |
| [`audio.md`](audio.md) | How do I play sound and record? | ES8311 `0x18` + NS4150B + MEMS mic + 3.5 mm jack |
| [`microsd.md`](microsd.md) | How do I use the SD card? | SPI G40/G14/G39, CS G12 |
| [`imu.md`](imu.md) | How do I read motion? | BMI270 @ I²C `0x69` |
| [`rtc.md`](rtc.md) | How do I keep the time? | **there is no RTC** — read this before designing around one |
| [`battery-and-power.md`](battery-and-power.md) | How do I read the battery and charge safely? | ADC G10, TP4057, SY7088/SY8089 |
| [`wifi-and-ble.md`](wifi-and-ble.md) | How do I use Wi-Fi and BLE? | ESP32-S3 radio, Stamp-S3A antenna |
| [`ir.md`](ir.md) | How do I send IR? | emitter on G44, **TX only** |
| [`grove-port.md`](grove-port.md) | How do I attach a Grove sensor? | HY2.0-4P, G1/G2, external I²C |
| [`cap-header.md`](cap-header.md) | How do I use or build a CAP board? | EXT 2.54-14P, P3 |
| [`usb.md`](usb.md) | How do I flash it, or make it a HID keyboard? | native USB-OTG on the Stamp |

Cross-cutting contention between these lives in
[`../resources-and-conflicts.md`](../resources-and-conflicts.md); which of them work on which
Cardputer revision lives in [`../compatibility-and-status.md`](../compatibility-and-status.md).
