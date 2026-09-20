# T-Display-S3 — compatibility and status

Keyed by hardware revision where one can be distinguished, and by software version.
**Nothing below was verified on hardware by this pass**; the class column says who did verify.

Classes: **VC** vendor-confirmed · **FM** firsthand measurement · **FO** firsthand ownership ·
**II** informed interpretation · **INF** inferred here.

## Working

| Item | Version / revision | Class | Evidence |
|---|---|---|---|
| Arduino, `TFT_eSPI` + `Setup206` | arduino-esp32 **≤ 2.0.14** | VC | vendor README; the entire example set |
| Arduino, `Arduino_GFX` | 2.0.14 **and** 3.x | FO | vendor README FAQ 2 recommends it as the hardware test |
| PlatformIO | `espressif32@6.5.0` | VC | `platformio.ini` @ `ec889e7` |
| ESP-IDF | v5.x via `LilyGo-Display-IDF` | VC | repo @ `b1a1cc5` |
| **Tasmota** | `Tasmota32-S3 (QIO Flash/OPI PSRAM)` + "Lilygo S3 Display" template | FO | [issue #18](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/18); `Display Model 17`, 320×170. **Needs `displaydimmer 100`** |
| **ESPHome** | `mipi_spi` model `T-DISPLAY-S3`, board `lilygo-t-display-s3` | VC (upstream source) | `esphome/.../lilygo.py`, `dev` |
| **MicroPython** | `russhughes/st7789s3_mpy` | FO | vendor README §6; `tft_config.py` exists for this board |
| LVGL | 8.x | VC | `examples/lv_demos/lv_conf.h` |
| Touch, CST328 boards | `-DTOUCH_MODULES_CST_MUTUAL` | VC | vendor `platformio.ini` default |
| Battery ADC | `analogReadMilliVolts(4) * 2` | FM | [issue #230](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/230) |
| Battery + shell | MakerFocus 3.7 V 1000 mAh #952540 + printed backpack | FO | [r/esp32 2026-08-30](https://old.reddit.com/r/esp32/comments/1tnop7r/lilygo_tdisplay_s3_clock_with_ds18b20_and_pir/) |
| JTAG over USB-C | `USB Mode = CDC and JTAG`, `debug_tool = esp-builtin` | VC | `platformio.ini`, board manifest |

## Partial

| Item | Limitation | Class |
|---|---|---|
| Battery operation with USB serial | must choose: `USB CDC On Boot` on (blocks on battery) or off (serial moves to GPIO43/44) | VC |
| Deep sleep | works; **no current figure published for this board**, and GPIO16/17 pull-ups add unquantified draw | VC + FO |
| Touch under ESP-IDF | `TouchLib` is Arduino-only; use `LilyGo-Display-IDF` or write a driver | FO ([#156](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/156)) |
| ULP | vendor examples state they need **arduino-esp32 3.0.0-rc3**, contradicting the repo's 2.0.14 pin | VC (self-contradictory) |
| I²S audio | no codec fitted; pins scarce | FO ([#158](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/158)) |
| Qwiic sensors on the SH1.0 connector | **not pin-compatible with Qwiic** | FO ([#181](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/181)) |

## Failing

| Item | Symptom | Class |
|---|---|---|
| `TFT_eSPI` on arduino-esp32 **> 2.0.14** | documented broken by the vendor, citing [TFT_eSPI#3329](https://github.com/Bodmer/TFT_eSPI/issues/3329) | VC |
| `ledcSetup` / `ledcAttachPin` on core 3.x | removed; use `ledcAttach`/`ledcDetach` | FM |
| **GPIO43 / GPIO44 as GPIO under Arduino** | claimed by UART0 even with hardware CDC. Reproduced by a second person after initially disputing it | **FM ×2** |
| GPIO16 / GPIO17 as clean inputs or low-side drivers | fitted pull-ups hold them high; they go high again on deep-sleep entry | FO → **VC with photographs** |
| Battery ADC while USB attached | reads ≈2.5 V, not the cell | VC |
| Charging from the 5 V header pin | `VBUS` is not brought out; feeding 5 V in back-powers the charger | VC + FO |
| `analogRead(4) * 3.3 / 4096` | gave 2.14 V for a 3.9 V cell | FM |
| 5 GHz Wi-Fi | not supported by the silicon | II |
| Meshtastic | no LoRa radio | INF (searched; no variant exists) |
| WLED | no S3 board file or usermod | INF (searched) |

## Conflicting reports

| Item | Reports | Status |
|---|---|---|
| Charge current | README 500 mA vs schematic note 580 mA | [G2/G5](gaps-and-conflicts.md) — unresolved |
| Charger part | schematic `TP4065` vs a board marked `65b311` | [G2](gaps-and-conflicts.md) — unresolved |
| Colour order | `TFT_eSPI` says RGB, ESPHome says BGR | [G3](gaps-and-conflicts.md) — unresolved |
| Pixel clock | vendor 16 MHz vs ESPHome 10 MHz | [G4](gaps-and-conflicts.md) — both work; panel-dependent |
| GPIO43/44 usability | one commenter asserted they work, then tested and retracted | **resolved against**: they do not, under Arduino |

## Untested here (everything requiring hardware)

Display refresh rate · deep-sleep current · Wi-Fi RSSI · actual charge current · backlight
linearity · whether the pull-ups are fitted on every production run · whether the `sdkconfig`
workaround frees GPIO43/44 in ESP-IDF. See [`performance.md`](performance.md) for the method.
