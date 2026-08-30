# Development and examples

Retrieved: 2026-08-21; dual-MCU toolchain guidance added 2026-08-22; **toolchain-version audit against wiki §3/§5/§6/§8.6 added 2026-08-23**.

## The vendor-specified toolchain

Every version Waveshare states, in one place, from wiki revision 111069 (§3 Development Tools, §5.1 Arduino environment setup, §6.1 ESP-IDF environment setup, §8.6 Software Tools). **[SRC]** unless marked.

| Component | Vendor's requirement | Where stated | Held locally |
|---|---|---|---|
| **Arduino IDE** | **no version specified** — "select the corresponding system and system bit to download", install defaults | §5.1.1 | link only |
| **`esp32` by Espressif Systems** board package | **≥ 3.2.0** — "Install Offline" / "Install Online" | §5.1.2 table | — |
| **LVGL** | **v8.4.0**, *"Install **Offline**"* — mandatory, not optional | §5.1.3 table | bundled in demo ZIP |
| **SensorLib** | **v0.3.1**, "Install Online" or "Install Offline" | §5.1.3 table | bundled in demo ZIP |
| **ESP-IDF** | **v5.1.4** — the only pinned IDF version anywhere on the page | §6.1.1 `{{Note}}`, via the `esp-idf/en/**v5.1.4**/esp32s3/get-started/` URL | — |
| **Visual Studio Code** | no version specified | §6.1.1, §8.6.2 | link only |
| **Espressif IDF VS Code plugin** | no version; "generally recommended to use Install Online" | §6.1.2 | — |
| **Flash Download Tool** | no version at the link; the archive currently contains **3.9.11** | §8.6.3 | ✅ `artifacts/tools/flash_download_tool.zip` |
| **FFmpeg** (MJPEG converter) | Waveshare's **"v2.1"** wrapper bundle, FFmpeg binaries dated 2024-09-14 | §8.6.4 | ✅ `artifacts/tools/mjpeg_Conversion_tool_V2.1.zip` |
| **esptool** | no version; §7 screenshots show Python 3.11.9 / pip 24.0 | §7 | — |
| **MicroPython** | **not offered** — the entry exists in the wikitext but is HTML-commented-out and does not render | §3.1 source | — |
| SSCOM serial terminal | **commented out**, does not render | §8.6 source | ✅ `artifacts/tools/Sscom5.13.1.zip` |

Library files for offline installation live inside the demo archive at:

~~~
..\ESP32-S3-Knob-Touch-LCD-1.8-Demo\Arduino\libraries
~~~

Full URL inventory including the tutorial pages: [wiki-resource-links.md](wiki-resource-links.md).

### Reconciliation notes

Discrepancies found by this audit, and how they are resolved:

| Issue | Finding | Resolution |
|---|---|---|
| **ESP-IDF 5.1.4 vs the factory ESP32 image** | The wiki pins **5.1.4** for the S3. The **ESP32-U4WDH** factory image was built with **ESP-IDF v5.4-727-g5cbd2a3877**. | **Not a conflict.** The two MCUs are independent; there is no requirement for matching IDF versions. 5.1.4 applies to the eight S3 examples only, and Waveshare ships nothing at all for the U4WDH. Stated correctly below. |
| **"ESP-IDF 5.1.4" is never stated in prose** | It appears *only* inside a documentation URL in a `{{Note}}` box. There is no version table for ESP-IDF equivalent to the Arduino one. | Treat 5.1.4 as **the version Waveshare tested**, not a hard floor. The demo `sdkconfig` files are the authority for what actually builds. |
| **LVGL docs link vs bundled LVGL** | The wiki links `docs.lvgl.io/**master**` (LVGL 9.x) in §8.7 and twice more in `{{Note}}` boxes, while requiring **8.4.0**. | **Vendor error.** Use <https://docs.lvgl.io/8.4/>. LVGL 9 is not API-compatible; the Library Manager will offer it and it will not build. |
| **Arduino core ≥ 3.2.0, no upper bound** | Open-ended. | The 2.x→3.x boundary is the one that matters (different underlying IDF, large peripheral-API break). A 2.x core will not build these examples. |
| **"Arduino IDE" version unspecified** | Only 2.x is currently distributed. | Use current 2.x. The 1.8.x legacy IDE is not a sensible target for an ESP32-S3 core ≥ 3.2.0. |
| **Offline board package hosted on Google Drive** | §8.6.1 links a **personal Google Drive folder** for the offline Arduino-ESP32 package — unversioned, unchecksummed, third-party-controlled. | **Not retained, and not recommended.** Prefer online installation from Espressif. See [wiki-resource-links.md §8.6.1](wiki-resource-links.md). |
| **Flash Download Tool vs the wiki's own procedure** | §8.6.3 links Espressif's Windows GUI flasher, but §7 "BIN File Flashing" walks through **command-line `esptool`**. | Prefer `esptool` — cross-platform, scriptable, and what every community project uses. The GUI is Windows-only. |
| **Vendor MJPEG tool vs plain FFmpeg** | The "FFmpeg" download is an 82 MB Windows .NET wrapper, not FFmpeg. | Unnecessary. The wiki states the target parameters, so plain FFmpeg works on any platform — command in [factory-demo-apps.md §4](factory-demo-apps.md). |
| **PlatformIO not mentioned** | The wiki documents only Arduino IDE and ESP-IDF. | A community PlatformIO board definition exists (`boards/waveshare_knob_18.json` in `IngoDuesentrieb/esp32-s3-knob-hardware-explorer`, MIT). Several projects use PlatformIO successfully. See [examples/catalog.md](examples/catalog.md). |
| **SquareLine Studio has no board profile** | FAQ 11 links only a generic Waveshare tutorial. | Create a 360×360, LVGL **8.x** project. A complete working SquareLine project ships in `joshuacant/BlueKnob` (Apache-2.0, retained locally). |

### Arduino IDE Tools settings

The wiki shows these only as a screenshot (`ESP32-S3-LCD-1.3-1013.png`) and its FAQ says merely "check if Arduino IDE → Tools is correctly configured". The settings that matter, corroborated against community projects:

| Setting | Value |
|---|---|
| Board | **ESP32S3 Dev Module** — *not* "ESP32 Dev Module", which is the other chip |
| Flash Size | 16 MB (128 Mb) |
| PSRAM | **OPI PSRAM** — omitting this is the classic cause of LVGL allocation failures |
| Flash Mode | QIO 80 MHz |
| USB CDC On Boot | Enabled, if using the S3's native USB for the serial monitor |
| Upload Speed | 921600 |
| Partition Scheme | one with ≥ 4 MB app for large sketches |

## Two MCUs, two toolchain targets

Before anything else: this board has **two independent MCUs** and you must know which one you are targeting. See [dual-MCU architecture](README.md#dual-mcu-architecture).

| | ESP32-S3R8 (`U2`) | [ESP32-U4WDH](../../../components/espressif/esp32-u4wdh/README.md) (`U14`) |
|---|---|---|
| ESP-IDF target | `esp32s3` | **`esp32`** |
| Arduino board selection | ESP32S3 Dev Module | **ESP32 Dev Module** |
| `esptool --chip` | `esp32s3` | **`esp32`** |
| USB path | S3 **native USB** (GPIO19/20) | external **UART bridge `U10`** |
| USB-C plug orientation | one way | **the other way** |
| Owns | LCD, touch, SD, mic, haptics, knob 1, Wi-Fi, BLE 5, CH445P mux select | Bluetooth **Classic**, BLE 4.2, knob 2, I2S to DAC, DAC mute |
| Official examples exist? | Yes, eight | **No — none** |

**Always confirm the target before flashing:**

~~~sh
esptool --port PORT chip_id
~~~

If it names the wrong chip, or no port appears at all, **unplug, rotate the USB-C plug 180°, and reconnect.** Plug orientation selects the MCU. This is the single most common problem people hit with this board.

Because the bridge `U10` drives the ESP32's `EN` from `RTS#` and `IO0` from `DTR#` directly, serial terminals that assert DTR/RTS on port open can reset the ESP32 or drop it into the bootloader unexpectedly. If your monitor session dies the moment you connect, turn that off in your terminal program.

## Arduino (ESP32-S3)

1. Install current Arduino IDE and Espressif's `esp32` board package **>= 3.2.0**.
2. Open a project under `artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Arduino/examples/`.
3. Select **ESP32S3 Dev Module**, the selected USB serial port, and enable USB CDC if using the S3 native USB path.
4. Install bundled `lvgl` **8.4.0** offline for the LVGL demo and SensorLib **0.3.1** for DRV2605. Preserve the bundled license files.
5. If no port appears, disconnect and rotate the USB-C plug 180 degrees; orientation selects the target.

## ESP-IDF (ESP32-S3)

Official setup guidance references **ESP-IDF 5.1.4**. Install that release and the VS Code Espressif extension or use the command line. Open one project directory directly under `artifacts/demo/.../ESP-IDF/`, set target `esp32s3`, select the port, then run `idf.py build flash monitor`. The factory S3 image also identifies an IDF 5.1.4-derived build.

## ESP32-U4WDH (the Bluetooth Classic MCU)

**Waveshare ships no example, no BSP and no documentation for this chip.** The demo archive contains nothing that builds for `esp32` — verified 2026-08-22 by searching the entire Arduino and ESP-IDF trees. You start from Espressif's own examples.

~~~sh
idf.py set-target esp32
idf.py menuconfig      # enable Bluedroid + Classic Bluetooth
idf.py build
idf.py -p PORT flash monitor
~~~

The factory image for this chip was built with **ESP-IDF v5.4-727-g5cbd2a3877** (project `TAIJI_KNOB_32`, 2025-04-18). That is a later IDF than the 5.1.4 Waveshare documents for the S3 side; the two MCUs are independent, so there is no requirement to use matching IDF versions.

Useful starting points in the ESP-IDF tree:

| Example | Maps onto |
|---|---|
| `examples/bluetooth/bluedroid/classic_bt/a2dp_sink` | Board as a Bluetooth speaker, closest to the factory behaviour |
| `examples/bluetooth/bluedroid/classic_bt/a2dp_source` | Board streaming audio out |
| `examples/bluetooth/bluedroid/classic_bt/bt_spp_acceptor` | Bluetooth serial |
| `examples/bluetooth/esp_hid_device` | Media-key / HID remote behaviour |
| `examples/peripherals/i2s/i2s_basic/i2s_std` | I2S output to the PCM5100A |

Board pin configuration for this chip (full table in [pinouts and buses](pinouts-and-buses.md)):

| Function | GPIO |
|---|---:|
| I2S BCLK | 25 |
| I2S WS/LRCK | 27 |
| I2S DOUT | 26 |
| I2S MCLK | **none — disable it** |
| PCM5100A `XSMT` mute | 32 (**high = un-muted**) |
| Knob 2 A / B | 19 / 22 (active low, 10 k pull-ups) |
| Inter-MCU UART1 TX / RX | 23 / 18 |

**Two things to do before writing real code:**

1. **Determine the core count.** This part may be single-core at 160 MHz or dual-core at 240 MHz depending on manufacturing date — see [the caveat](../../../components/espressif/esp32-u4wdh/README.md#2--the-core-count-and-clock-speed-caveat-unresolved). Print `esp_chip_info().cores` on boot. Community practice supports building defensively rather than assuming: `joshuacant/BlueKnob` maintains a `sdkconfig.ci.esp32_singlecore` variant with `CONFIG_FREERTOS_UNICORE=y`.
2. **Drive GPIO32 high.** If your firmware never un-mutes the DAC, the board goes silent — including for audio originating on the ESP32-S3, which cannot reach `XSMT`. See the [Classic Bluetooth guide](classic-bluetooth.md).

### The secondary MCU costs ~50 mA if you leave it alone

Added 2026-08-23 from community evidence **[SRC]**, `svwhisper/lyngdorf-secondary-sleep`:

> "The secondary chip is permanently powered from `3V3` and has no GPIO-controllable enable from the S3 — when left running stock firmware it draws **~50 mA continuously**, dominating idle battery current. […] After flashing, the secondary draws **~10 µA**."

**If your project does not use Bluetooth Classic, the secondary chip is pure battery drain and you cannot switch it off in hardware.** The fix is to flash it with a firmware whose `app_main` does nothing but `esp_deep_sleep_start()` with no wake source — roughly ten lines. Two independent projects ship exactly this (`svwhisper/lyngdorf-secondary-sleep`, and `BlueKnob-ESP32` inside `joshuacant/BlueKnob`); both are retained under [`examples/selected/`](examples/). The former is the **only ESP32-U4WDH source we have found anywhere** — Waveshare ships none.

Note this is a one-way trip for the factory Bluetooth apps: **back up `ESP32-KNOB_ESP32_0.bin` first**, because it is the only copy of the Classic Bluetooth application in existence.

A full walkthrough of Bluetooth Classic development on this chip, including menuconfig settings and Arduino library choices, is in **[classic-bluetooth.md](classic-bluetooth.md)**.

## Official examples (ESP32-S3 only)

| Example | Purpose | Key interfaces |
|---|---|---|
| 01_ADC_Test | Read system/battery-divider voltage | S3 ADC1 channel 0 / GPIO1 |
| 02_SD_Card | Mount/read/write FAT card | 4-bit SDMMC GPIO2-6,42 |
| 03_DRV2605_Test | Cycle haptic waveform effects | I2C GPIO11/12, address 0x5A, SensorLib |
| 04_Encoder_Test | Count knob direction/events | S3 GPIO8/7 — **knob 1 only**; knob 2 is on the other MCU |
| 05_WIFI_AP | Run Wi-Fi access point | ESP32-S3 radio |
| 06_WIFI_STA | Join Wi-Fi network | ESP32-S3 radio |
| 07_Audio_Test | PDM microphone to I2S DAC loop/playback | GPIO45/46 PDM; GPIO39/40/41 I2S; external output device. **Depends on the DAC being un-muted by the other MCU** — see [gaps and conflicts](gaps-and-conflicts.md) |
| 08_LVGL_Test | Display/touch GUI and optional backlight test | QSPI LCD, CST816 I2C, LVGL 8.4.0 |

**There is no Bluetooth Classic example, no Bluetooth-audio example and no inter-MCU UART example anywhere in the archive.**

Verified 2026-08-22 **[SRC]**: all eight ESP-IDF projects set `CONFIG_IDF_TARGET="esp32s3"` and `CONFIG_ESPTOOLPY_FLASHSIZE="16MB"` — none targets `esp32`. No `.c`/`.h`/`.cpp`/`.ino` file in the tree contains `uart_driver_install`, `uart_param_config`, `uart_set_pin`, `UART_NUM_1`, `UART_NUM_2`, `Serial1` or `Serial2`, and nothing references GPIO38 or GPIO48. **Waveshare ships no ESP32-U4WDH source code at all** — the secondary MCU exists in the published materials only as the prebuilt blob `ESP32-KNOB_ESP32_0.bin`. See [Dual-MCU architecture §3.1](dual-mcu-architecture.md#31-the-official-demo-archive-no--and-there-is-no-esp32-source-at-all).

Both Arduino and ESP-IDF trees are retained completely. The archive includes much more bundled library source than the eight board examples; use only what the project requires. The only license file found by filename search is SensorLib's LICENSE, while bundled LVGL carries its upstream files/metadata; absence of a top-level Waveshare license means redistribution rights for original demo files should not be generalized beyond preserving this official archive.

## Inter-MCU communication

> Full treatment: [Dual-MCU architecture §2](dual-mcu-architecture.md#2-the-inter-mcu-link-a-two-wire-uart) — bandwidth arithmetic, flow-control consequences, protocol reconstruction with explicit unknowns, and a working `uart_param_config` skeleton for both ends.

If your project needs the two MCUs to talk, note that **the factory protocol is undocumented and no example uses the link**. The physical layer is two wires (S3 GPIO38 → ESP32 GPIO18, ESP32 GPIO23 → S3 GPIO48, both sides on UART1), cross-connected so the link is **full duplex** — but with **no RTS/CTS wires**, so flow control must be implemented in software. **The configured baud rate is unknown**: every baud literal in the demo tree is a *console* baud in an `sdkconfig`, and the value is not recoverable from firmware strings. What is known about the stock framing — reconstructed from log strings in both factory binaries — is in [section 6 of the ESP32-U4WDH component page](../../../components/espressif/esp32-u4wdh/README.md#6-the-inter-mcu-uart-link) and [Dual-MCU architecture §2.4](dual-mcu-architecture.md#24-the-protocol--what-is-known-and-what-is-not).

Sizing rule of thumb: at 8N1, `bytes/sec = baud/10`. Even at the ESP32's 5 Mbaud silicon ceiling that is 500 kB/s — ample for metadata and album-art JPEGs, **arithmetically impossible for video or uncompressed audio**. This is a control channel, not a data bus.

For a custom project, reflash both MCUs and define your own protocol. You control both ends; the link is just two GPIOs. **Back up the factory ESP32 image first — it is the only copy of the Classic Bluetooth application in existence and Waveshare publishes no source for it.**

## Display driver note

The LVGL example declares 360 x 360, RGB565/16-bit, SPI2 QSPI and a driver named `esp_lcd_sh8601`. Product identity says ST77916. Keep the official command table and timings together with this exact panel until the controller discrepancy is resolved.

Community practice has converged on the **bus parameters** regardless of what the die is called — `esp_lcd_sh8601` at **40 MHz with 32-bit QSPI command frames and `quad_mode` enabled**. Attempts using 8-bit SPI commands at 20 MHz reportedly produce a blank or garbled screen. See [examples/catalog.md §1.4](examples/catalog.md), and note the pin-table caveat recorded there.

## Cross-references

- [**getting-started.md**](getting-started.md) — the practical build guide: exact board settings, build/flash/monitor commands, factory-firmware backup, and the pitfall list
- [tools/README.md](tools/README.md) — `restore-demo-deps.sh`, which restores the LVGL and SensorLib trees the demo archive expects
- [factory-demo-apps.md](factory-demo-apps.md) — the preinstalled apps, and the SD-card layout they depend on
- [faq-and-troubleshooting.md](faq-and-troubleshooting.md) — the vendor FAQ, with the USB-C orientation statement in the vendor's own words
- [wiki-resource-links.md](wiki-resource-links.md) — every downloadable and outbound URL the wiki offers
- [examples/catalog.md](examples/catalog.md) — 28 community projects, with a PlatformIO board definition and a working SquareLine project
- [dual-mcu-architecture.md](dual-mcu-architecture.md) · [classic-bluetooth.md](classic-bluetooth.md) · [gaps-and-conflicts.md](gaps-and-conflicts.md)

## Useful source paths

- Arduino pin definitions: `Arduino/examples/08_LVGL_Test/lcd_config.h`, `07_Audio_Test/user_config.h`, `02_SD_Card/sd_card_bsp.cpp`
- Display driver: `Arduino/examples/08_LVGL_Test/esp_lcd_sh8601.c` and equivalent ESP-IDF component
- Touch driver: `Arduino/examples/08_LVGL_Test/cst816.cpp`
- Haptics: `03_DRV2605_Test` and bundled SensorLib
- ESP-IDF examples: eight independent projects under `ESP-IDF/`
- ESP32-U4WDH: **nothing is supplied** — see above
