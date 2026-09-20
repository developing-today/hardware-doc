# Xteink X3 — feature coverage

| Feature | Hardware | Official docs | Community evidence | Guide | Tested | Gaps |
|---|---|---|---|---|---|---|
| Display 792×528 (UC8253) | UC8253 | none | SDK, shipping default | [display](features/display.md) | ✅ | Panel module part |
| Display (UC8279d batch) | UC8279d | none | SDK, **datasheet-only** | [display](features/display.md) | ❌ | **No unit ever benched.** No grayscale, no fast waveforms |
| Controller fingerprint | VER/FLG probe | none | SDK | [display](features/display.md) | ⚠️ | What UC8253 answers to 0x70 is **unknown** |
| Buttons (6, ADC ladder) | GPIO1 + GPIO2 | none | SDK, 3 physical devices | [../x4 buttons](../x4/features/buttons.md) | ✅ | — |
| **IMU / motion page turn** | QMI8658 @0x6B | none | SDK + teardown | [imu](features/imu.md) | ✅ presence | No performance data; no interrupt pin |
| **RTC** | @0x68 | none | **3 sources disagree on the part** | [rtc](features/rtc.md) | ⚠️ | **Part identity unresolved** |
| **Fuel gauge** | BQ27220 @0x55 | none | SDK + teardown | [battery](features/battery-and-power.md) | ✅ | Accuracy unmeasured |
| Battery 650 mAh | — | none | **teardown, single source** | [battery](features/battery-and-power.md) | ✅ | Cell part unknown |
| microSD + power rail | GPIO 8/10/7/12 + EN13 | none | SDK + factory-firmware RE | [storage](features/storage.md) | ✅ | Max card size |
| **NFC** | ISO 14443A tag | **vendor claims it** | teardown BOM only | [nfc](features/nfc.md) | ❌ | **Purpose entirely unknown** |
| Pogo charging | magnets glued to cover | none | teardown + vendor | [battery](features/battery-and-power.md) | ⚠️ | Pinout, voltage, charge-state signal |
| Wi-Fi / BLE | ESP32-C3 | none | firmware strings (X4 dump) | [../x4 wifi/bt](../x4/features/wifi-and-bluetooth.md) | ✅ | No measurements |
| Deep sleep | SD rail GPIO13 | none | SDK + factory RE | [battery](features/battery-and-power.md) | ⚠️ | **No current measurement, despite a teardown done expressly to make one** |

## Not fitted

Touch, frontlight, PSRAM, SDMMC, audio, LEDs, GPIO expander, PMIC.

## Advertised features and their status

| Vendor claim (2025-12-09) | Status |
|---|---|
| 55 g, 3.7-inch | ✅ consistent |
| 250+ PPI | ✅ arithmetically confirmed (~257) |
| Gyroscope for motion page turning | ✅ hardware confirmed; feature implementation not verified |
| **NFC support** | ⚠️ hardware present; **function unknown** |
| Magnetic Pogo Pin charging | ✅ confirmed by teardown |
| Time display and battery percentage | ✅ RTC + BQ27220 present |
| *"Adjustable warm light settings"* (product page) | ❌ **FALSE — there is no frontlight** |
| *"Cloud sync"* (product page) | ❌ unsupported; overseas app *"still under development"* per the vendor's own announcement |

## Combination scenarios

| Combination | Status |
|---|---|
| Display refresh **+** SD read | Structurally serialised (one SPI bus). Not benchmarked |
| I²C (gauge + RTC + IMU) **+** SPI | Independent buses; no conflict expected. Untested |
| OTA **+** low free memory | **Known to fail on this device** |

## Score

**10 of 13** capabilities have citable third-party confirmation.
**0 of 13** were verified by this session.
Two are **actively unresolved**: the RTC part and the NFC function.
