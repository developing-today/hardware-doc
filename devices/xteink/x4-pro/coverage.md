# Xteink X4 Pro — feature coverage

Snapshot **2026-09-04**. "Tested" means tested by *someone*, cited; nothing was
tested by this session.

| Feature | Hardware | Official docs | Community evidence | Feature guide | HW-tested | Gaps |
|---|---|---|---|---|---|---|
| Display 800×480 | SSD1677 / UC8179 / UC8279 | **none** | FreeInk SDK, hardware-confirmed | [display](features/display.md) | ✅ by SDK authors | Panel module part; orientation |
| Controller auto-detect | boot `VER`/`FLG` probe | none | SDK + observed `VER=00 00 01 FF FF` | [display](features/display.md) | ✅ | Whether a 4th controller exists |
| Touch GT911 | 0x5D, INT10/RST4/PWR2 | none | SDK, hardware-confirmed | [touch](features/touch.md) | ✅ | `flipX`/`flipY` conflict |
| Capacitive Home key | GT911 `0x814E & 0x10` | none | SDK, RE-confirmed vs OEM | [touch](features/touch.md) | ✅ | — |
| Buttons (2 + power) | GPIO 0/7/3 | none | SDK, pull-up edge test | [buttons](features/buttons.md) | ✅ | — |
| Frontlight warm/cool | GPIO8/9, LEDC 4/5 | none | SDK, hardware-confirmed | [frontlight](features/frontlight.md) | ✅ | Lux/CCT range unmeasured |
| microSD (SDMMC 1-bit) | GPIO41/42/40 + EN5 | none | SDK, "CONFIRMED WORKING" | [storage](features/storage.md) | ✅ | Max card size untested |
| Battery gauge | CW2017 @0x63 | none | SDK, hardware-confirmed | [battery](features/battery-and-power.md) | ✅ | **Capacity unknown** |
| Charge status | GPIO21 active-HIGH | none | RE (`Cw2017PowerHal`) | [battery](features/battery-and-power.md) | ✅ | Charger IC part |
| RTC BM8563 | 0x51 | none | SDK, "found and initializing" | [rtc](features/rtc.md) | ✅ | Backup power source |
| USB-CDC | GPIO19/20 | none | SDK log transport | [usb](features/usb.md) | ⚠️ reported | — |
| **USB-MSC** | GPIO19/20 | none | **in stock, not ported** | [usb](features/usb.md) | ❌ | Whole feature |
| Wi-Fi | ESP32-S3 | none | inferred + sibling doc | [wifi/bt](features/wifi-and-bluetooth.md) | ❌ | Never demonstrated on this device |
| BLE | ESP32-S3 | none | BLE page-turner forks exist | [wifi/bt](features/wifi-and-bluetooth.md) | ⚠️ reported | Reconnect reportedly fragile |
| Deep sleep | rail polarity | none | SDK implemented | [battery](features/battery-and-power.md) | ❌ | **No current measurement** |
| Pogo charging | magnetic | none | owner reports | [battery](features/battery-and-power.md) | ⚠️ | Pinout/voltage unknown |

## Advertised but not fitted

`NO_AUDIO`, `NO_LEDS`, `NO_MIC`, `ImuType::None`, no PMIC, no GPIO expander.
**The X4 Pro has no IMU** even though the cheaper X3 and the X4 Classic do.

## Combination scenarios — untested

Nobody has reported, and this session did not test:

| Combination | Concern |
|---|---|
| Display refresh **+** SD read | Both are DMA-heavy; SD uses a `MALLOC_CAP_DMA` bounce buffer |
| Wi-Fi **+** frontlight PWM | LEDC + radio power draw on one battery |
| Touch **+** RTC **+** gauge | All three on one `Wire` controller — a stalled bus blocks all |
| BLE **+** Wi-Fi | One 2.4 GHz radio, shared |

## Score

**11 of 16** capabilities are hardware-confirmed by a citable third party.
**0 of 16** were verified by this session.
