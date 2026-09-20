# T-Display-S3 — feature guides

Every advertised or fitted capability, one guide each. Evidence status is stated inside each
guide; **none of these were verified against physical hardware by the 2026-09-07 pass**.

| Guide | Covers | Evidence status |
|---|---|---|
| [`display.md`](display.md) | ST7789V, 8-bit 8080 bus, library choice, backlight, offsets | vendor source + independent library configs |
| [`touch.md`](touch.md) | CST816S / CST328, the two-generation split, I²C | vendor source + shipped datasheets |
| [`buttons.md`](buttons.md) | BOOT/GPIO0, GPIO14, RST, wake sources | vendor source |
| [`power-and-battery.md`](power-and-battery.md) | GPIO15 gate, charger, charge current, no protection | vendor doc + firsthand reports |
| [`battery-voltage-measurement.md`](battery-voltage-measurement.md) | GPIO4 ADC, divider, the pin conflict | schematic designators + firsthand reports |
| [`usb.md`](usb.md) | native USB, **the `USB CDC On Boot` trap**, USB Mode, recovery | vendor doc, repeatedly corroborated |
| [`wifi-and-ble.md`](wifi-and-ble.md) | on-board vs u.FL antenna, the resistor move, reported range | vendor doc + user reports |
| [`microsd.md`](microsd.md) | TF Shield only, 1-bit SDMMC | vendor doc |
| [`gpio-and-expansion.md`](gpio-and-expansion.md) | headers, SH1.0 connector, what is actually free | vendor source + issue tracker |
| [`deep-sleep.md`](deep-sleep.md) | wake sources, what to switch off, the pins that go high | vendor example + firsthand report |

Not fitted, and therefore not documented as features: IMU, audio codec, RTC, LoRa, camera,
Ethernet, battery protection. See [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md)
§ *Negative results*.
