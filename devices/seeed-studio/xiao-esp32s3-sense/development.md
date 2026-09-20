# Development — XIAO ESP32S3 Sense

> Toolchains, the settings that actually matter, and recovery.
> Snapshot **2026-08-24**. Command status is marked throughout: `executed-success`, `reported-working`, or `inferred`. **No hardware was available**, so no flashing or build command here is `executed-success`.

## 0. The three settings that cause most failures

Before anything else. In the Arduino IDE, with **XIAO_ESP32S3** selected:

| Setting | Required value | Failure if wrong |
|---|---|---|
| **PSRAM** | **OPI PSRAM** | `esp_camera_init()` returns `0x105`; large allocations fail |
| **Partition Scheme** | **8MB with spiffs (3MB APP/1.5MB SPIFFS)** | Sketch too large; upload rejected |
| **Flash Size** | **8MB (64Mb)** | Boot loop or truncated app |

The board has 8 MB of **octal** PSRAM in the ESP32-S3R8 package. "Enabled" alone is not sufficient — it must be **OPI**, not QSPI. This single dropdown is behind a large share of all camera problems reported for this board.

Also relevant: **USB CDC On Boot = Enabled** if you want `Serial` to appear over the native USB port (see [§5](#5-usb-serial-and-recovery)).

---

## 1. Arduino-ESP32

**Board manager URL:**
```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```
Install **esp32 by Espressif Systems**, then select **XIAO_ESP32S3**.

The board variant is upstream in Espressif's repo, not a Seeed add-on — [`variants/XIAO_ESP32S3/pins_arduino.h`](artifacts/source-snapshots/pins_arduino.h) (local copy retrieved 2026-08-24). It declares `USB_VID 0x2886`, `USB_PID 0x0056`, `LED_BUILTIN 21`, and the `D0`–`D10` map.

### The 2.x → 3.x break

Arduino-ESP32 **3.x** is built on ESP-IDF **5.x**; **2.x** on IDF 4.4. Two APIs changed in ways that break most existing XIAO Sense code:

| Area | 2.x | 3.x |
|---|---|---|
| I²S / PDM microphone | `I2S.h` Arduino class | `ESP_I2S.h` / IDF `i2s_pdm` driver — **rewritten** |
| `esp32-camera` | `pin_sscb_sda` | `pin_sccb_sda` (spelling fixed) |
| LEDC | `ledcSetup()` + `ledcAttachPin()` | `ledcAttach()` |

Practical guidance: **decide which major version you are on first**, then pick examples accordingly. The vendor camera repo ships both — `CameraWebServer_for_esp-arduino_2.0.x` and `..._3.0.x` — in [`examples/selected/SeeedStudio-XIAO-ESP32S3-Sense-camera/`](examples/selected/SeeedStudio-XIAO-ESP32S3-Sense-camera/). Most microphone code found in this survey predates 3.x.

The factory firmware itself was built with **core 2.0.7 / IDF v4.4.4** ([`factory-firmware.md`](factory-firmware.md)), which is a useful datum: the vendor's own demo is a 2.x artefact.

## 2. PlatformIO

```ini
[env:seeed_xiao_esp32s3]
platform  = espressif32
board     = seeed_xiao_esp32s3
framework = arduino
monitor_speed = 115200

board_build.partitions = default_8MB.csv
build_flags =
    -DBOARD_HAS_PSRAM
    -DARDUINO_USB_MODE=1
    -DARDUINO_USB_CDC_ON_BOOT=1

lib_deps =
    espressif/esp32-camera @ ^2.0.4
```

`-DBOARD_HAS_PSRAM` is the PlatformIO equivalent of the IDE's PSRAM dropdown. `default_8MB.csv` matches the factory partition layout documented in [`factory-firmware.md` §4](factory-firmware.md#4-flash-map).

> Status: **`inferred`** — assembled from the board definition and the factory partition table, and cross-checked against the `platformio.ini` in [`XIAO-ESP32S3-Sense_Retro_Camera`](examples/selected/XIAO-ESP32S3-Sense_Retro_Camera/platformio.ini), which is the best-pinned real example found. Not built here.

**Pin your dependencies.** The `@ ^2.0.4` above is deliberate; several surveyed projects float `esp32-camera`, which for an actively-developed camera driver is a reproducibility problem ([`examples/vendored-lib-deltas/README.md`](examples/vendored-lib-deltas/README.md)).

## 3. ESP-IDF

Target `esp32s3`. Minimum IDF **5.0** for the current camera/UVC components.

```bash
idf.py set-target esp32s3
idf.py menuconfig
idf.py build flash monitor
```

`sdkconfig` essentials:

```
CONFIG_ESPTOOLPY_FLASHSIZE_8MB=y
CONFIG_SPIRAM=y
CONFIG_SPIRAM_MODE_OCT=y            # octal — the R8 package
CONFIG_SPIRAM_SPEED_80M=y
CONFIG_ESP32S3_DATA_CACHE_64KB=y
CONFIG_ESP32S3_DATA_CACHE_LINE_64B=y
CONFIG_PARTITION_TABLE_CUSTOM=y
```

Add the camera driver via the component manager:

```bash
idf.py add-dependency "espressif/esp32-camera^2.0.4"
```

The cleanest ESP-IDF example located is [`XIAO_Webcam`](examples/selected/XIAO_Webcam/) (USB UVC). Note its `idf_component.yml` uses `"=*"` version specifiers — pin them yourself.

> Status: **`inferred`** — standard IDF workflow plus the octal-PSRAM options the R8 package requires. Not built here.

## 3A. TinyUF2 — drag-and-drop flashing

Seeed's board package ships a **TinyUF2 bootloader** for this board, which is not mentioned anywhere in the wiki's getting-started material. With it the XIAO enumerates as a **USB mass-storage drive** and you flash by copying a `.uf2` file onto it — no `esptool`, no drivers, no serial port.

Contents of [`artifacts/kicad/xiao-esp32s3-package.zip`](artifacts/kicad/xiao-esp32s3-package.zip):

| File | Purpose |
|---|---|
| `bootloader-tinyuf2.bin` | UF2-aware second-stage bootloader |
| `tinyuf2.bin` | the UF2 application, flashed at **`0x410000`** |
| `partitions-8MB-tinyuf2.csv` | the matching partition table |
| `pins_arduino.h` | the board variant |

The UF2 partition layout differs substantially from the factory one:

| Partition | Offset | Size |
|---|---|---|
| `nvs` | `0x9000` | 20 KB |
| `otadata` | `0xe000` | 8 KB |
| **`ota_0`** | `0x10000` | **2,048 KB** |
| **`ota_1`** | `0x210000` | **2,048 KB** |
| `uf2` (factory) | `0x410000` | 256 KB |
| **`ffat`** | `0x450000` | **3,776 KB** |

Trade-off worth understanding: **the app slot shrinks from 3,264 KB to 2,048 KB** — a 37 % reduction — in exchange for a **3.7 MB FAT filesystem** the host can mount. For a camera application already using 90 % of the standard slot, TinyUF2 is likely to be too tight. For a data-logger that wants the host to read its files over USB, it is an excellent fit.

In the Arduino IDE this appears as a **Partition Scheme → "TinyUF2 Compatibility"** option. Status: **`inferred`** — the files, offsets and `boards.txt` entries are read directly from Seeed's package, but flashing was not attempted.

## 4. Other runtimes — what actually works

Honest status. Several of these are advertised but do not support the Sense hardware.

| Runtime | Board | **Camera** | **Microphone** | microSD | Notes |
|---|---|---|---|---|---|
| **Arduino** | ✅ | ✅ | ✅ | ✅ | The mainstream path. Everything here assumes it |
| **ESP-IDF** | ✅ | ✅ | ✅ | ✅ | Most capable; USB device classes only available here |
| **PlatformIO** (Arduino/IDF) | ✅ | ✅ | ✅ | ✅ | Best for reproducible builds |
| **ESPHome** | ✅ | ✅ | ✅ | ⚠ | Easiest route to a Home Assistant camera. See [`xiao-esp32s3-sense-ha-cam`](examples/selected/xiao-esp32s3-sense-ha-cam/) |
| **MicroPython** | ✅ | ❌ **not in mainline** | ⚠ limited | ✅ | Camera needs a custom firmware build with the driver compiled in. See [`Seeed-Studio-XIAO-ESP32S3-GPIOViewer`](examples/selected/Seeed-Studio-XIAO-ESP32S3-GPIOViewer/) |
| **CircuitPython** | ✅ | ⚠ partial | ⚠ | ✅ | Community board support; camera support is not equivalent to Arduino's |
| **Zephyr** | ✅ | ❌ | ❌ | ⚠ | Board defined; sensor peripherals not supported |
| **NuttX** | ✅ | ❌ | ❌ | ⚠ | Wiki has a page; sensors not covered |
| **MicroBlocks** | ✅ | ❌ | ❌ | ❌ | Educational, GPIO-level |
| **Rust** (`esp-hal`) | ⚠ | ❌ | ❌ | ⚠ | One unlicensed community crate located |
| **TinyGo** | ⚠ | ❌ | ❌ | ❌ | XIAO examples exist for the family |

**The headline:** if you want the camera, you want Arduino, ESP-IDF or ESPHome. The "MicroPython supported" claim in Seeed's comparison table refers to the *board*, not the Sense peripherals.

## 5. USB, serial and recovery

The ESP32-S3 has **native USB** — there is no CH340/CP2102 bridge on this board ([`pinouts-and-buses.md` §6](pinouts-and-buses.md#6-usb-boot-and-reset)). Consequences:

- The serial device is **`/dev/ttyACM*`** (Linux) or `/dev/cu.usbmodem*` (macOS), not `ttyUSB*`.
- **The port disappears when your firmware crashes, reconfigures USB, or sleeps.** This is expected behaviour, not a fault.
- With `USB CDC On Boot` disabled, `Serial` goes to the UART pins (`D6`/`D7`) instead of USB.

### Entering the bootloader

Two vendor-documented methods, both `reported-working`:

1. **Hold `BOOT`, then plug in USB**, then release `BOOT`.
2. **Hold `BOOT`, tap `RESET`, release `BOOT`** (for an already-powered board).

This drops into the mask-ROM download mode, which enumerates unconditionally regardless of what the application did. Seeed's own troubleshooting says this "can solve most of the problems of unrecognized devices and failed uploads" — that matches the hardware: `BOOT` is `GPIO0` via K2, `RESET` is `EN` via K1, both with 10 kΩ pull-ups.

### udev rule (Linux)

```
# /etc/udev/rules.d/99-xiao-esp32s3.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="2886", ATTRS{idProduct}=="0056", MODE="0666", SYMLINK+="xiao-esp32s3"
```
VID/PID from `pins_arduino.h`. Status: **`inferred`** — correct VID/PID, standard rule syntax, untested here.

Note the ROM bootloader enumerates with a **different** VID/PID (Espressif's `303a:1001` USB-Serial-JTAG), so a rule matching only `2886:0056` will not match a board in download mode.

### Can you brick it?

Essentially no, by flashing. The ROM bootloader is mask-programmed and cannot be overwritten. The genuinely irreversible operations are **eFuse** burns (`espefuse.py`) — flash encryption, secure boot, or disabling the USB-JTAG bridge. Nothing in the normal workflow touches these.

Crash diagnosis is better than it looks: the factory partition table includes a **64 KB `coredump` partition at `0x7f0000`**, so `espcoredump.py` can extract a backtrace after a panic.

## 6. Hardware debugging — read this before planning

**With the Sense daughterboard attached, JTAG is unavailable.** The camera and microphone occupy `MTCK`/`MTDO`/`MTDI`/`MTMS` = GPIO39/40/41/42. This is a physical conflict, not a configuration one ([`pinouts-and-buses.md` §7.2](pinouts-and-buses.md#72-the-camera-and-microphone-occupy-all-four-jtag-pins)).

Your options:

- Debug with the daughterboard **removed** (works — the S3's internal USB-JTAG bridge is fine).
- Use `printf`/`ESP_LOG` debugging with the daughterboard attached. This is what everyone does.
- Use the `coredump` partition for post-mortem analysis.

If hardware debugging with sensors attached is a hard requirement, this is the wrong board.

## 7. Power sequencing while developing

- **With battery power, there is no voltage on the `5V` pin.** Vendor-documented. Do not rely on `5V` to power peripherals when running untethered.
- **Battery polarity:** Seeed specifies the **negative terminal nearest the USB port** and the **positive terminal away from it**. Reversing a Li-ion cell into `BAT±` will destroy the board. There is no reverse-polarity protection on those pads in the schematic.
- USB and battery can be connected simultaneously; `VIN` is selected automatically between `VBUS` (via D2 Schottky) and `VBAT` (via Q1 P-MOS).
- The `3V3` pin is an **output** of the SGM6029 buck-boost, limited to **600 mA**. Do not back-feed it.

## 8. Cosmetic issue that is not a defect

Seeed FAQ Q2: units frequently have **uneven rounded corners**. This is a PCB panelisation artefact — the board is so densely integrated that the depanelisation tabs could only be placed at the four corners. Vendor states it does not affect function. Worth knowing before you RMA a board.

## 9. Related

- [`factory-firmware.md`](factory-firmware.md) — what ships, flash offsets, restore
- [`pinouts-and-buses.md`](pinouts-and-buses.md) — pin conflicts these settings work around
- [`features/camera.md`](features/camera.md) — camera-specific failure table
- [`examples/best.md`](examples/best.md) — projects using each toolchain
- [`commands.md`](commands.md) — command ledger with execution status
