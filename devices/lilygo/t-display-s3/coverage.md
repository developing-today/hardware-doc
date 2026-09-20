# T-Display-S3 — feature coverage map

Snapshot 2026-09-07. **Build/hardware test status is `untested` throughout**: no board was
available. That is stated once here rather than repeated in every row.

| Feature | Hardware | Official doc | Official example | Community example | Feature guide | Status |
|---|---|---|---|---|---|---|
| Display (ST7789V, 8080) | ST7789V + AW9364 backlight | README pinout; `Setup206` | `tft`, `Arduino_GFXDemo`, `TFT_Rainbow`, `lv_demos`, `PCBClock`, `PokerS3`, `ImageScroll` | ESPHome model; Tasmota template; many | [`display.md`](features/display.md) | **documented** |
| Backlight / dimming | GPIO38 → AW9364DNR | README table only | inside the display examples | core-3.x LEDC rename (firsthand) | [`display.md`](features/display.md) | **partial** — one-wire protocol undocumented by vendor |
| Touch (Touch SKU) | CST816S **or** CST328 | two datasheets shipped; no prose | `touch_test`, `CapacitiveTouch`, `usb_hid_pad` | issue #125, #168 | [`touch.md`](features/touch.md) | **documented**, with the [R1 revision caveat](../t-display-s3-shared/board-revision-drift.md#r1--t-display-s3-touch-cst816s--cst328) |
| Buttons | GPIO0 (strap), GPIO14, RST | README pinout | `Sleep`, `factory` | AceButton in sibling repos | [`buttons.md`](features/buttons.md) | **documented** |
| Battery / charging | TP4065-or-`65b311`, no protection | README + FAQ 8 | — | issue #230, #42, #291 | [`power-and-battery.md`](features/power-and-battery.md) | **conflicted** — see [G2](gaps-and-conflicts.md) |
| Battery voltage ADC | GPIO4, 100k/100k | README note | `GetBatteryVoltage` | issue #190, #65 | [`battery-voltage-measurement.md`](features/battery-voltage-measurement.md) | **documented**, ratio inferred |
| Peripheral power gate | GPIO15 | README **IMPORTANT** block | every example | issue #79 and ~4 more | [`power-and-battery.md`](features/power-and-battery.md) | **documented** |
| USB (native, CDC/JTAG) | ESP32-S3 USB → Type-C | README FAQ 4, 5 | `usb_hid_pad`, MIDI examples | issues #7, #16, #166, #162 | [`usb.md`](features/usb.md) | **documented** |
| USB HID / MIDI device | USB-OTG mode | — | `usb_hid_pad`, 8 MIDI examples | `@sauloverissimo` upstreamed | [`usb.md`](features/usb.md) | **documented** |
| Wi-Fi | ESP32-S3 radio + ceramic antenna | README antenna note + image | `factory`, `ota` | issues #123, #247, #340 | [`wifi-and-ble.md`](features/wifi-and-ble.md) | **documented; unmeasured** |
| Bluetooth LE | ESP32-S3 radio | links to Espressif examples | `T-Display-S3-BLE-*` | — | [`wifi-and-ble.md`](features/wifi-and-ble.md) | **partial** |
| External antenna (u.FL) | `RX`/`RX2` 0 Ω positions | README + image | — | — | [`wifi-and-ble.md`](features/wifi-and-ble.md) | **documented; unverified** |
| microSD | **shield only**, 1-bit SDMMC | README explicit | `sd` | — | [`microsd.md`](features/microsd.md) | **documented** |
| I²C / SH1.0 connector | GPIO17/18, fitted pull-ups | pinout only | `I2CScan`, `MPR121TouchSensor` | issue #181 (not Qwiic-compatible) | [`gpio-and-expansion.md`](features/gpio-and-expansion.md) | **documented** |
| GPIO / headers | 2 × 12-pin + SH1.0 | pinout + electrical table | — | issues #313, #117 | [`gpio-and-expansion.md`](features/gpio-and-expansion.md) | **documented** |
| Deep sleep | ESP32-S3 RTC | — | `Sleep` | issue #313 (pins go high) | [`deep-sleep.md`](features/deep-sleep.md) | **partial — no current figure exists** |
| ULP | ESP32-S3 ULP-FSM | — | `ULP_ADC`, `ULP_Count` — **require core 3.0.0-rc3**, contradicting the repo's own 2.0.14 pin | — | — | **gap — no guide written** |
| OTA update | — | — | `ota` | — | — | **gap — no guide written** |
| I²S audio | no codec fitted | — | `WIFI_Audio_I2S` (source file only) | issue #158 "Can't manage to use I2S" | — | **gap; and pins are scarce** |
| NES emulation | — | — | `nes` (vendored `arduino-nofrendo`) | — | — | out of scope |
| JTAG debugging | built-in USB-JTAG | `debug_tool = esp-builtin` | — | — | [`usb.md`](features/usb.md) | **documented** |

## Advertised or fitted capabilities with no guide

| Capability | Why no guide | Where it is covered instead |
|---|---|---|
| OTA | thin evidence; the `ota` example is generic Arduino OTA with nothing board-specific | `examples/catalog.json` |
| ULP | vendor's own examples require a core version the rest of the repo forbids; untangling that needs hardware | [`development.md`](development.md), noted as a contradiction |
| I²S audio | **no codec, amplifier or speaker is fitted.** Not a board feature; the example drives an external I²S device | [`resources-and-conflicts.md`](resources-and-conflicts.md) |

## Not fitted, and therefore absent by design

IMU · RTC · audio codec · LoRa · camera · Ethernet · battery protection · fuel gauge ·
USB-UART bridge · onboard microSD. Each is evidenced by the schematic designator census
(`U1`–`U7`, **no `U8`**) in [`gaps-and-conflicts.md`](gaps-and-conflicts.md) § *Negative
results*.
