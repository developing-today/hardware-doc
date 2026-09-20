# Xteink X4 — feature coverage

| Feature | Hardware | Official docs | Community evidence | Guide | Tested | Gaps |
|---|---|---|---|---|---|---|
| Display 800×480 | SSD1677/UC8179/UC8279 | none | SDK + timing measurements | [display](features/display.md) | ✅ | Panel module part |
| Controller detect | boot VER/FLG probe | none | SDK | [display](features/display.md) | ✅ | — |
| 40 MHz overclock | — | none | SDK + Witch Reader fork shipped it | [display](features/display.md) | ⚠️ out of spec | Per-unit reliability |
| Buttons (6, ADC ladder) | GPIO1 + GPIO2 | none | **SDK, 3 physical devices** | [buttons](features/buttons.md) | ✅ | — |
| Power button | GPIO3 | none | SDK | [buttons](features/buttons.md) | ✅ | — |
| microSD (SPI, shared) | GPIO 8/10/7/12 | none | SDK | [storage](features/storage.md) | ✅ | Max card size |
| Battery ADC | GPIO0, ÷2 | none | SDK | [battery](features/battery-and-power.md) | ⚠️ | **Capacity unknown**; accuracy unquantified |
| Power latch | GPIO13 | none | SDK, two revisions | [battery](features/battery-and-power.md) | ✅ | **No revision marking known** |
| USB-C / flashing | USB-serial-JTAG | none | Owner reports; flasher tools | [usb](features/usb.md) | ✅ | `usbDetect` pin unverified |
| Wi-Fi | ESP32-C3 | none | **Firmware strings + many projects** | [wifi/bt](features/wifi-and-bluetooth.md) | ✅ | No throughput data |
| BLE | ESP32-C3 | none | BLE page-turner ecosystem | [wifi/bt](features/wifi-and-bluetooth.md) | ✅ | Reconnect reportedly fragile |
| Deep sleep | — | none | SDK | [battery](features/battery-and-power.md) | ❌ | **Card cannot be powered down**; no current figure |

## Not fitted

Touch, frontlight, **RTC**, **fuel gauge**, IMU, NFC, audio, LEDs, SDMMC,
GPIO expander, PMIC.

## Combination scenarios

| Combination | Status |
|---|---|
| Display refresh **+** SD read | **Structurally serialised** — one SPI bus. Not benchmarked |
| Wi-Fi **+** display refresh | Untested; no PSRAM makes memory pressure likely |
| OTA **+** low free memory | **Known to fail** — CrossPoint moved off GitHub releases over C3 OOM |

## Score

**9 of 12** capabilities have citable third-party confirmation.
**0 of 12** were verified by this session.
