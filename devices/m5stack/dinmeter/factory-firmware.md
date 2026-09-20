# DinMeter — factory firmware

Applies to K134 and K134-V11. **Nothing here was flashed or executed.**

---

## 1. Summary

| Field | Value |
|---|---|
| What ships on it | The **M5DinMeter UserDemo** hardware-evaluation firmware |
| Source | <https://github.com/m5stack/M5DinMeter-UserDemo> — **open, MIT** |
| Source commit analysed | `d2fdfe44e9baf810f82335faa6f5962e9fc59a44` (repo HEAD, last push 2024-03-04) |
| Release | `V0.1`, published 2024-03-04 |
| Target MCU | ESP32-S3 (`esp32s3`), 8 MB flash, **no PSRAM** |
| Framework | Arduino via PlatformIO, `platform = espressif32@6.3.1` |
| CPU | `board_build.f_cpu = 240000000L` |
| Board profile used by the vendor | **`esp32-s3-devkitc-1`** — a generic S3 board, not a DinMeter profile |
| Distribution of the **binary** | **M5Burner only** — "DinMeter User Demo Easyloader" on both product pages |
| ⚠ Prebuilt binary URL | **None located.** M5Burner resolves images at run time from an undocumented endpoint |
| Local snapshot | [`artifacts/source-snapshots/M5DinMeter-UserDemo-d2fdfe44e9baf810f82335faa6f5962e9fc59a44.tar.gz`](artifacts/source-snapshots/M5DinMeter-UserDemo-d2fdfe44e9baf810f82335faa6f5962e9fc59a44.tar.gz) — 74 231 B, SHA-256 `af58e2cdaf565bb3f97daeadd02843a4cd3dc72f504446aa842d865eb9c4ec72` |

> **⚠ Back up before you overwrite.** There is no vendor-published factory image with a stable
> URL. If you flash your own firmware without reading the flash out first, the *binary* is gone —
> though the **source is public and MIT-licensed**, so you can rebuild an equivalent. That is a
> materially better position than most vendor firmware. See §5.

## 2. What it does

`src/main.cpp` is 24 lines: construct a `FactoryTest`, call `init()`, then a view loop. The
substance is in `src/factory_test/components/`:

| Component | Tests |
|---|---|
| `ft_disp_test.cpp` | display |
| `ft_key_test.cpp` | encoder button / keys |
| `ft_io_test.cpp` | GPIO / Grove ports |
| `ft_rtc_test.cpp` | BM8563 RTC |
| `ft_wifi_test.cpp` | Wi-Fi scan/connect |
| `ft_ble_test.cpp` | BLE |
| `ft_arkanoid.cpp` | a playable Arkanoid — the demo that shows off the knob |
| `ft_disp_lgfx_cfg.hpp` | the LovyanGFX panel configuration |

Plus a `src/view/` UI layer with PNG assets converted to headers (`bat_panel`,
`icon_brightness`, `icon_display`, …).

## 3. The panel configuration — the most reusable thing in it

`src/factory_test/components/ft_disp_lgfx_cfg.hpp`, verbatim values:

```cpp
#define LCD_MOSI_PIN 5   #define LCD_SCLK_PIN 6   #define LCD_DC_PIN  4
#define LCD_CS_PIN   7   #define LCD_RST_PIN  8   #define LCD_BL_PIN  9
#define LCD_MISO_PIN -1  #define LCD_BUSY_PIN -1

lgfx::Panel_ST7789 _panel_instance;
lgfx::Bus_SPI      _bus_instance;
lgfx::Light_PWM    _light_instance;

cfg.freq_write   = 40000000;      // 40 MHz
cfg.invert       = true;          // INVON
cfg.panel_width  = 135;  cfg.panel_height = 240;
cfg.offset_x     = 52;   cfg.offset_y     = 40;     // the GRAM gap
// backlight:
cfg.pin_bl = 9; cfg.invert = false; cfg.freq = 200; cfg.pwm_channel = 7;
```

Note `lgfx::Panel_ST7789` — **the generic ST7789 panel class**, not a V2-specific one. That is
one reason to expect the v1.1 ST7789P3 to behave the same.

Note also `freq = 200` for the backlight PWM, where Espressif's board definition uses 5 kHz. See
[`compatibility-and-status.md`](compatibility-and-status.md) §6.

## 4. Licensing

| Item | Licence | Evidence |
|---|---|---|
| `M5DinMeter-UserDemo` itself | **MIT**, © 2024 M5Stack | `LICENSE` in the repository |
| `lib/Button/` | has its own `LICENSE` | bundled |
| `lib/ESP32Encoder/` | `licence.txt` | bundled |
| `lib/I2C_BM8563/` | has its own `LICENSE` | bundled |
| `lib/` vendored trees generally | **mixed-licence** | the archive's own MIT does not cover its bundled dependencies |
| PNG/asset headers | not separately licensed | assumed to follow the project MIT |
| **The compiled binary** distributed via M5Burner | terms not stated | — |

Redistribution status of the **source snapshot**: `allowed` (MIT), with the standard obligation
to preserve the notice — the retained tarball contains `LICENSE` unmodified. Disposition:
`repository`.

Redistribution status of the **binary**: `unknown` — it could not be obtained.

## 5. Backing up and restoring — all `not-tested`

```bash
# 1. Enter download mode: hold G0 on the Stamp module, apply power, release G0.
#    (reported-working -- vendor instruction, both product pages)

# 2. Read the whole 8 MB flash out BEFORE doing anything else.
esptool.py --chip esp32s3 -p /dev/ttyACM0 -b 460800 \
    read_flash 0 0x800000 dinmeter-factory-backup.bin        # not-tested

sha256sum dinmeter-factory-backup.bin                        # record it

# 3. Restore later
esptool.py --chip esp32s3 -p /dev/ttyACM0 -b 460800 \
    write_flash 0 dinmeter-factory-backup.bin                # not-tested
```

**Or rebuild from source** — the better option, and available because M5Stack open-sourced it:

```bash
git clone https://github.com/m5stack/M5DinMeter-UserDemo
cd M5DinMeter-UserDemo
git checkout d2fdfe44e9baf810f82335faa6f5962e9fc59a44
pio run -e esp32-s3-devkitc-1 -t upload                      # not-tested
```
`platform`, `LovyanGFX 1.1.12` and `SmoothUIToolKit 1.0.1` are all pinned in the project file, so
this should be reproducible. **Not verified.**

**Or reflash the vendor image** with M5Burner → search "DinMeter" → *DinMeter User Demo
Easyloader*. `reported-working` — this is the vendor's documented route, not tested here.

## 6. Image metadata — mostly unknown

| Field | Value |
|---|---|
| Version/build identifier | **unknown** — the binary was not obtained; the *source* release is `V0.1` |
| Build date | unknown |
| SHA-256 of the shipped image | **unknown** |
| Byte size | unknown |
| Flash offsets | not published; PlatformIO's `esp32-s3-devkitc-1` defaults apply to this project |
| Partition table | **not published**. The project file sets no `board_build.partitions` |
| Bootloader | stock ESP-IDF second-stage, framework-supplied |
| Companion images | unknown |

**This is a genuine gap**, recorded rather than glossed: without the binary there is no hash to
compare a dumped flash against.

## 7. Third-party alternative

`bmorcelli/Launcher` ships `Launcher-m5stack-dinmeter.bin` through the same M5Burner channel,
with a published MD5 (`bccbefef5284357a2a7c3c7cc196fd98`, from
`support_files/m5burner_post.py`). Its partition layout **is** published:
`support_files/custom_8Mb.csv`, `maximum_size = 8388608`, SPIFFS threshold `0x2F0000`. See
[`projects-and-community.md`](projects-and-community.md) §2.

## Related

[`development.md`](development.md) · [`examples/best.md`](examples/best.md) ·
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) §7
