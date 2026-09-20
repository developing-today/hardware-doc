# T-Display-S3 — recommended examples

Selected from the 32 catalogued in [`catalog.json`](catalog.json). **None was built or run**
(no hardware, no toolchain). These are reasoned selections, not validated ones.

## Start here, in this order

| Order | Example | Why this one |
|---|---|---|
| 1 | **`Arduino_GFXDemo`** | LilyGO's own recommended first test (README FAQ 2). It needs **no** library-internal configuration, so if it draws, the hardware is fine and any later problem is `TFT_eSPI` config. Running this first saves the most time of anything in the repo |
| 2 | **`I2CScan`** | Thirty seconds, and it tells you whether you have a Touch board, and whether it is CST816S (`0x15`) or CST328 (`0x1A`). Also proves GPIO15 is high, because the touch controller sits on the gated rail |
| 3 | **`tft`** | The minimal `TFT_eSPI` path. If step 1 worked and this does not, you have the `User_Setup_Select.h` problem and nothing else |
| 4 | **`GetBatteryVoltage`** | The vendor reference for the GPIO4 divider — read it next to [issue #190](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/190), where the naive arithmetic gives a wrong-but-plausible answer |

## Portfolio, by purpose

| Purpose | Example | Notes |
|---|---|---|
| **Diagnostic** | `Arduino_GFXDemo`, `I2CScan` | isolate hardware from configuration |
| **Minimal per feature** | `tft` (display) · `touch_test` (touch) · `GetBatteryVoltage` (ADC) · `Sleep` (deep sleep) · `T-Display-S3-BLE-Sender` (BLE) | one feature each, small enough to read |
| **Integrated** | `factory` · `lv_demos` | `factory` exercises display + touch + Wi-Fi + NTP + LVGL + buttons + battery. `lv_demos` is the LVGL starting point and the reason `PSRAM = OPI` matters |
| **Limit testing** | `Arduino_GFX_PDQgraphicstest` | the vehicle for the pixel-clock measurements in [`../performance.md`](../performance.md) |
| **Alternative approach** | `usb_hid_pad` | requires `USB Mode = USB-OTG`, which **disables the built-in JTAG debugger** — the clearest demonstration of that trade-off |
| **Negative / cautionary** | `tft` (fails without the `User_Setup_Select.h` edit) · `ULP_ADC` (demands a core version the repo forbids) · `WIFI_Audio_I2S` (a `.cpp` with no `.ino`) | each teaches something the docs do not |
| **ESP-IDF starting point** | `LilyGo-Display-IDF` @ `b1a1cc5` | MIT; nine boards behind `CONFIG_LILYGO_*` |

## Feature coverage of the selection

| Feature | Covered by |
|---|---|
| Display | `Arduino_GFXDemo`, `tft`, `lv_demos`, `factory` |
| Touch | `touch_test`, `factory` |
| Buttons | `Sleep`, `factory` |
| Battery ADC | `GetBatteryVoltage`, `factory` |
| Deep sleep | `Sleep` |
| Wi-Fi | `factory` |
| BLE | `T-Display-S3-BLE-Sender` |
| USB device (OTG) | `usb_hid_pad` |
| I²C | `I2CScan` |
| PSRAM | `lv_demos` |
| Performance | `Arduino_GFX_PDQgraphicstest` |

**Not covered by any selected example, and not covered well by any example at all:**
microSD (needs the shield), OTA (generic), I²S audio (broken as shipped), ULP (version
conflict), external antenna (no example possible). See
[`../coverage.md`](../coverage.md).

## Not vendored here

The vendor examples are **not copied into this repository**. They are ~180 MB of repo including
multi-megabyte image headers and nine vendored libraries, they are one `git clone` away, and
every entry in [`catalog.json`](catalog.json) carries a commit-pinned permalink. Reacquisition:
[`../acquisition/README.md`](../acquisition/README.md).
