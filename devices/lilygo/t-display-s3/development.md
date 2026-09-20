# LilyGO T-Display-S3 — development

> Snapshot **2026-09-07**. Every command is labelled `executed-success`, `reported-working`,
> `inferred` or `not-tested`. **No physical board was available to this pass**, so nothing here
> is `executed-success` against hardware; the label distribution is honest, not modest.

## 1. Board target and build configuration

### PlatformIO (LilyGO's own, and the one that works out of the box)

From `platformio.ini` @ **`ec889e789b3cf093412689a143f7f37b42b56af7`**, verbatim `[env]`:

```ini
[platformio]
default_envs = factory
src_dir = examples/${platformio.default_envs}

[env]
platform = espressif32@6.5.0
board = lilygo-t-display-s3
framework = arduino
debug_tool = esp-builtin
upload_protocol = esptool
build_flags =
    -DLV_LVGL_H_INCLUDE_SIMPLE
    -DARDUINO_USB_CDC_ON_BOOT=1
    -DDISABLE_ALL_LIBRARY_WARNINGS
    -DARDUINO_USB_MODE=1
    -DTOUCH_MODULES_CST_MUTUAL
```

Four of those five flags are load-bearing:

| Flag | What it actually does | If you drop it |
|---|---|---|
| `-DARDUINO_USB_CDC_ON_BOOT=1` | `Serial` becomes the native-USB CDC device | Serial output moves to GPIO43/44 and the board **stops blocking at boot** — see [`features/usb.md`](features/usb.md) |
| `-DARDUINO_USB_MODE=1` | selects the **TinyUSB-free "CDC and JTAG"** hardware USB-serial-JTAG peripheral rather than the OTG stack | you lose the built-in JTAG debugger and `debug_tool = esp-builtin` stops working |
| `-DTOUCH_MODULES_CST_MUTUAL` | selects the **mutual-capacitance** branch of the `TouchLib` driver, i.e. **CST328**, not CST816S | a **CST328** board will not be detected. This single flag is the difference between the two touch panel generations |
| `-DLV_LVGL_H_INCLUDE_SIMPLE` | LVGL header-path convention | LVGL examples fail to compile |

`platform = espressif32@6.5.0` pins **Arduino-ESP32 2.0.14**. That is not incidental — see §2.

Board manifest, `boards/lilygo-t-display-s3.json` @ `ec889e7`:
`mcu esp32s3`, `memory_type qio_opi`, `partitions default_16MB.csv`, `f_cpu 240 MHz`,
`f_flash 80 MHz`, `flash_mode qio`, `-DBOARD_HAS_PSRAM`, `flash_size 16MB`,
`maximum_ram_size 327680`, `upload speed 921600`, USB VID/PID **`0x303A:0x1001`**
(Espressif's native USB-serial-JTAG identity — a useful positive ID that no CH340 board can
fake).

### Arduino IDE

LilyGO's required settings, from `README.md` @ `ec889e7`. **Bold = mandatory**; the rest can
follow your needs.

| Setting | Value |
|---|---|
| Board | **ESP32S3 Dev Module** |
| **USB CDC On Boot** | **Enable** |
| CPU Frequency | 240 MHz (WiFi) |
| Flash Mode | QIO 80 MHz |
| **Flash Size** | **16MB (128Mb)** |
| **Partition Scheme** | **16M Flash (3M APP/9.9MB FATFS)** |
| **PSRAM** | **OPI PSRAM** |
| **Upload Mode** | **UART0/Hardware CDC** |
| **USB Mode** | **CDC and JTAG** |
| Upload Speed | 921600 |
| USB DFU On Boot / USB Firmware MSC On Boot | Disable |

> "You can also choose `LilyGo T-Display-S3` as the board, but the partition table is fixed to
> 16M Flash (3M APP/9.9MB FATFS)." — README @ `ec889e7`

**Getting `PSRAM = OPI PSRAM` wrong is silent and fatal**: with the default `QSPI PSRAM` the
ESP32-S3R8's in-package octal PSRAM is not detected, `ps_malloc()` returns `NULL`, LVGL falls
back to internal RAM and the board runs out of heap in ways that look like random crashes.
Related: [issue #256](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/256).

Likewise `Flash Size = 16MB` — [issues #8](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/8)
and [#41](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/41) are both "16 MB flash
setting not working" and both resolve to the partition scheme, not the board.

<a id="arduino-core-versions"></a>
## 2. The Arduino board-package version dependency

This is the single most expensive undocumented dependency in the family, so it gets exact
versions and independent corroboration rather than a warning.

### What LilyGO says

> "**Note:** The test phase uses version **2.0.14**. Versions above 2.0.14 may not work
> correctly — please downgrade if you encounter issues. As of **2024/08/02**, **TFT_eSPI does
> not work on versions higher than 2.0.14** (see
> [TFT_eSPI#3329](https://github.com/Bodmer/TFT_eSPI/issues/3329))."
> — `T-Display-S3/README.md` @ `ec889e7`, § *Arduino IDE Manual Installation*

### What the shipped binaries independently show

Every factory image in `firmware/` carries an ESP-IDF **app descriptor** at flash offset
`0x10000` whose `project_name` is `arduino-lib-builder` — i.e. it records the Arduino core's
own build stamp. Decoded locally (`executed-success`, host-side, 2026-09-07):

| Factory image | ESP-IDF in descriptor | Core build date | Implies arduino-esp32 |
|---|---|---|---|
| `t-display-s3-touch-20230417_0x0.bin` | `v4.4.4 e8bdaf9198` | 2023-02-08 | **2.0.7** |
| `t-display-s3-no-touch-20231013_0x0.bin` | `v4.4.4 e8bdaf9198` | 2023-02-08 | **2.0.7** (byte-identical to the above — see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) G1) |
| `t-display-s3-screen-detect-20230315_0x0.bin` | `v4.4.4 e8bdaf9198` | 2023-04-20 | 2.0.8–2.0.9 |
| `t-display-s3-midi-v1.0.1-20231013_0x0.bin` | `v4.4.4 e8bdaf9198` | 2023-04-20 | 2.0.8–2.0.9 |
| `t-display-s3-tft-espi-20231113_0x0.bin` | `v4.4.5 ac5d805d0e` | 2023-06-12 | 2.0.9–2.0.11 |
| `t-display-s3-lvgl-demo-20250109_0x0.bin` | **`v4.4.6 3572900934`** | **2023-10-04** | **2.0.14** |

The newest image LilyGO shipped — dated January 2025 — is still built on the **2.0.14** core.
The ESP-IDF/core mapping is the published arduino-esp32 correspondence (2.0.14 ↔ IDF v4.4.6);
the *descriptor contents* are firsthand measurement, the *mapping* is documentation.
Method: [`commands.md`](commands.md#decoding-an-esp32-app-descriptor).

### Practical version table

| Component | Known-good | Known-broken | Evidence |
|---|---|---|---|
| **arduino-esp32 core** | **2.0.14** | > 2.0.14 with TFT_eSPI | vendor README; TFT_eSPI#3329 |
| PlatformIO platform | **`espressif32@6.5.0`** (= core 2.0.14) | untested above | `platformio.ini` @ `ec889e7` |
| `TFT_eSPI` | any version **with** `Setup206` selected, on core ≤ 2.0.14 | any version on core 3.x | vendor README, issue #326 |
| `Arduino_GFX` | the vendored `GFX Library for Arduino` copy; also works on 3.x | — | vendor README FAQ 2 recommends it as the *hardware* test precisely because it does not depend on `User_Setup_Select.h` |
| `LovyanGFX` | community-reported working on 3.x | — | *reported-working*, not verified here |
| `lvgl` | **8.x** for LilyGO's examples | 9.x needs the examples ported | `examples/lv_demos/lv_conf.h` @ `ec889e7` is an LVGL 8 config |
| ESP-IDF (direct) | **v5.x**, via `LilyGo-Display-IDF` | v5.0 had teething problems | [issue #103](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/103) |
| ESPHome | ≥ the release adding `mipi_spi` model `T-DISPLAY-S3` | older `st7789v` platform needed manual pins | `esphome/components/mipi_spi/models/lilygo.py`, `dev` @ 2026-09-07 |

**The core-3.x situation, stated carefully.** LilyGO's warning is specifically about
`TFT_eSPI`, and it is dated 2024-08-02. Core 3.x also renames the LEDC API — a
[firsthand community report](https://old.reddit.com/r/esp32/comments/1tnop7r/lilygo_tdisplay_s3_clock_with_ds18b20_and_pir/)
(2026-05-25) notes `ledcSetup`/`ledcAttachPin` are gone in favour of `ledcAttach`/`ledcDetach`,
which breaks LilyGO's backlight-dimming snippets. Boards **do** run on core 3.x if you use
`Arduino_GFX` and fix the LEDC calls; the vendor examples do not.

## 3. Build, flash, monitor

`reported-working` (LilyGO's documented procedure), `not-tested` here.

```bash
# PlatformIO, from the repo root
pio run -e factory                 # build
pio run -e factory -t upload       # flash
pio device monitor -b 115200       # monitor
```

Selecting a different example means editing `default_envs` in `platformio.ini`; LilyGO drives
`src_dir` from it, so exactly one line must be uncommented.

### When the port keeps disappearing — manual download mode

The most-repeated instruction in the whole family, quoted from the README:

1. Connect the board via USB.
2. Press and **hold BOOT**.
3. While still holding BOOT, press **RST**.
4. Release **RST**.
5. Release **BOOT**.
6. Upload. Then press **RST** to leave download mode.

This is needed because the native USB device is re-enumerated by the *application*; if the
application crashes, reconfigures USB, or blocks, the port vanishes. There is no auto-reset
circuit to fall back on — a CH340 board would have one. See
[`features/usb.md`](features/usb.md).

## 4. Debugging

`debug_tool = esp-builtin` in LilyGO's `platformio.ini` selects the **ESP32-S3's built-in
USB-JTAG**, which requires `USB Mode = CDC and JTAG` (`-DARDUINO_USB_MODE=1`). You get JTAG
over the same USB-C cable, with no external probe. Choosing the OTG USB mode to get TinyUSB
features costs you the debugger — that trade-off is not obvious from either menu.

`openocd_target` is `esp32s3-builtin.cfg` per the board manifest.

## 5. Recovery

Full procedure and offsets: [`factory-firmware.md`](factory-firmware.md). Summary: the shipped
images are **merged images starting at `0x0`** (bootloader + partition table + app), so a
single `esptool.py write_flash 0x0 <file>` restores a board, and LilyGO also hosts a web
flasher. Note the trap that the two 8 MB-layout images will leave a 16 MB board with a
partition table that only addresses the first 8 MB.

## 6. MicroPython and other languages

| Runtime | Status | Source |
|---|---|---|
| **MicroPython** | Supported through **`russhughes/st7789s3_mpy`** — a C-level ST7789 driver with an 8-bit parallel backend written for this board — and LilyGO's `Xinyuan-LilyGO/lilygo-micropython`. There is also `Xinyuan-LilyGO/T-Display-S3-MicroPython` (created recently, `board/lilygo-t-displays3.json`, pushed 2026-09-04) | vendor README §6; org repo listing |
| **CircuitPython** | **No board definition located** in Adafruit's repository during this pass. Recorded as a gap, not as an absence proof | [`research-log.md`](research-log.md) |
| **Rust** | asked in [issue #160](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/160); `esp-hal` targets the SoC, not the board. No board-support crate found | — |

**MicroPython carries the GPIO15 trap too**, and it bites harder because there is no `setup()`
convention: [issue #79](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/79) contains an
exchange (2024-04-23) where a MicroPython user could not make GPIO15 work and asked whether a
wire would do instead. It will not; the pin must be driven by code every boot.
