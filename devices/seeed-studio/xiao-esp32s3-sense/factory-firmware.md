# XIAO ESP32S3 Sense — factory firmware

> What actually ships on the board, recovered by parsing the vendor's own binaries.
> Research snapshot **2026-08-24**. All hashes and header fields below were computed locally from the downloaded artifacts using [`tools/esp_image_info.py`](../../../tools/esp_image_info.py) — they are **executed-verified**, not quoted from the vendor.

## Summary

The board ships running Espressif's **`CameraWebServer`** Arduino example, built by Seeed with **Arduino-ESP32 core 2.0.7 / ESP-IDF v4.4.4** on **2023-02-08**, and — most importantly — **with Seeed's own Wi-Fi credentials hardcoded into the binary**. See [§5](#5-the-factory-demo-cannot-connect-to-your-network). It will not do anything useful on your desk until you reflash it.

---

## 1. Artifact inventory

Two vendor bundles exist for the Sense, both retrieved 2026-08-24:

| File | Local path | Bytes | SHA-256 (full) |
|---|---|---:|---|
| `XIAO-ESP32S3-Sense-firmware-20240814.zip` | [`artifacts/firmware/`](artifacts/firmware/) | 9,520,580 | *(see [`acquisition/manifest.json`](acquisition/manifest.json))* |
| `XIAOESP32S3-Sense-firmware.zip` ("legacy") | [`artifacts/firmware/`](artifacts/firmware/) | 9,516,661 | *(idem)* |

### 1.1 The two releases contain identical firmware

A file-by-file hash comparison shows every **binary** is byte-identical between the "legacy" bundle and the "20240814" bundle:

| Member | SHA-256 (first 16) | Bytes | legacy | 20240814 |
|---|---|---:|:-:|:-:|
| `CameraWebServer.bin` | `8b2f3c7ca30b1ad9` | 2,941,584 | ✅ | ✅ |
| `bootloader.bin` | `a82c5cf7828dfaff` | 21,408 | ✅ | ✅ |
| `partition-table.bin` | `1d9cca96de0fe07a` | 3,072 | ✅ | ✅ |
| `boot_app0.bin` | `f94c5d786a7a8fab` | 8,192 | ✅ | ✅ |
| `esptool.exe` | `ce5a63d638cf8544` | 7,671,328 | ✅ | ✅ |

Only the **flashing wrapper** changed: the legacy bundle nests everything in `Auto_flash_User_firmware_v1.0/` and drives it with `0.testcode_flash.py`; the 2024 bundle flattens the layout and ships `esp32_flasher.py` v2.0.0 (MIT, by Spencer Yan, spencer@seeed.cc) plus a `project_config.json`.

**Therefore the `20240814` in the filename is a repackaging date, not a build date.** The firmware itself is from February 2023. Anyone who downloaded the "newer" file expecting a fix received the same application image. This is not stated anywhere in Seeed's documentation.

---

## 2. Image headers (parsed)

All images carry chip ID **9 = ESP32-S3**, confirming target compatibility.

| Image | Magic | Segments | Entry | Flash mode | Flash size | Flash freq |
|---|---|---:|---|---|---|---|
| `bootloader.bin` | 0xE9 | 3 | `0x403b622c` | **DIO** | 8 MB | 80 MHz |
| `CameraWebServer.bin` | 0xE9 | 5 | `0x40376aac` | **DIO** | 8 MB | 80 MHz |
| `boot_app0.bin` | — | — | — | — | — | not an ESP image (an 8 KB OTA-select blob) |

Note the factory images are built for **DIO** flash mode, while the Arduino IDE's default for this board and most community advice is **QIO**. Both work on the GD25Q64; QIO is faster. Mixing is safe because the mode byte in the *bootloader* header is what the ROM honours — but if you reflash only the application and leave the vendor bootloader in place, you keep DIO timing.

## 3. Application descriptor (`esp_app_desc_t`)

Read from offset `0x20` of `CameraWebServer.bin`:

| Field | Value |
|---|---|
| Project name | `arduino-lib-builder` |
| App version | `esp-idf: v4.4.4 e8bdaf9198` |
| **Build date/time** | **`Feb 8 2023 18:07:54`** |
| **ESP-IDF version** | **`v4.4.4`** |
| ELF SHA-256 | `06d08da8437626efbe8f85d8d2e7e937c2863a28e526cb33a422ee72de5873da` |

Embedded build paths in the binary pin the toolchain precisely:

```
C:\Users\Administrator\AppData\Local\Arduino15\packages\esp32\hardware\esp32\2.0.7\...
E:\cache\CameraWebServer\app_httpd.cpp
```

So: **Arduino-ESP32 core 2.0.7**, built on Windows under an `Administrator` account, from a working copy at `E:\cache\CameraWebServer`. The binary also links `esp-dl` (Espressif's deep-learning library) — the CameraWebServer example includes optional face detection/recognition, which is why the image is 2.9 MB.

The driver supports **OV2640, OV3660 and OV5640** — all three sensor strings are present — which is why the same factory image works across the sensor variants Seeed has shipped over the product's life.

## 4. Flash map

Parsed from `partition-table.bin` (magic `0xAA50`, 32-byte entries):

| Name | Type | SubType | Offset | Size | Notes |
|---|---|---|---:|---:|---|
| `nvs` | data | nvs | `0x009000` | 20 KB | Wi-Fi credentials, preferences |
| `otadata` | data | otadata | `0x00e000` | 8 KB | OTA slot selector |
| `app0` | app | ota_0 | `0x010000` | 3,264 KB | **factory application lives here** |
| `app1` | app | ota_1 | `0x340000` | 3,264 KB | OTA target |
| `spiffs` | data | spiffs | `0x670000` | 1,536 KB | user filesystem |
| `coredump` | data | `0x3` | `0x7f0000` | 64 KB | crash dumps |

Total: exactly **8.00 MB**, fully allocated. This is the stock Arduino **"8M with spiffs (3MB APP / 1.5MB SPIFFS)"** scheme.

Two practical consequences:

- **Your application must fit in 3,264 KB.** The factory image already uses 2,941,584 bytes — **90 % of the slot**. Adding anything to the CameraWebServer example as-shipped will overflow. If you need more room, switch to a no-OTA partition scheme (`Huge APP`, 3 MB app / no OTA) which frees the `app1` slot.
- The non-Sense bundle uses a near-identical table but with **1,600 KB** of SPIFFS and **no coredump partition**, so the two are not interchangeable if you care about the filesystem offset.

---

## 5. The factory demo cannot connect to your network

Strings extracted from `CameraWebServer.bin` around the connection logic:

```
"Camera init failed with error 0x%x"
"WiFi connected"
"Camera Ready! Use 'http://"   "' to connect"
"seeedstudio"
"XIAO_ESP32S3_Sense"
```

The stock `CameraWebServer.ino` declares:

```cpp
const char *ssid     = "...";
const char *password = "...";
```

and the two adjacent string-table entries here are **`seeedstudio`** and **`XIAO_ESP32S3_Sense`**. The image is a **station-mode** build — there is no SoftAP fallback in the stock example — so on power-up it repeatedly attempts to join an access point named after Seeed's internal network and never succeeds anywhere else.

**This fully explains the very common report that a new XIAO ESP32S3 Sense "does nothing" / "the LED just blinks" out of the box.** It is not faulty. The demo is doing exactly what it was built to do, on the wrong continent.

There is no way to supply credentials to the factory image at runtime — no provisioning portal, no serial prompt, no NVS override, because the SSID is a compile-time constant, not read from `nvs`. **The only path to a working camera demo is to rebuild the sketch with your own credentials**, which is what [`development.md`](development.md) and [`features/camera.md`](features/camera.md) cover.

> Evidence status: the credential strings are **observed in the binary** (firsthand, reproducible). The *mapping* of which string is the SSID and which is the password is **inferred** from their adjacency and from the stock example's declaration order. It has not been confirmed on hardware. Treat the pairing as probable, not certain.

Once connected, the app serves the usual CameraWebServer endpoints — `/capture` (also offering `image/x-windows-bmp`), a stream endpoint, and a control endpoint with permissive `Access-Control-Allow-*` headers.

---

## 6. Restoring the factory firmware

### 6.1 What the vendor ships

`xiao_esp32s3_sense_firmware_win.bat`, in full:

```bat
python esp32_flasher.py --project xiao_esp32_sense_factory
pause
```

`project_config.json` defines the offsets:

```json
"xiao_esp32_sense_factory": {
    "0x0":     "bootloader.bin",
    "0x8000":  "partition-table.bin",
    "0xe000":  "boot_app0.bin",
    "0x10000": "CameraWebServer.bin"
}
```

and `esp32_flasher.py` builds this command (verbatim from the source, lines 117–119):

```
{tool} --chip esp32s3 --port {port} --baud 921600 \
    --before default_reset --after hard_reset write_flash -z \
    --flash_mode dio --flash_freq 80m --flash_size 8MB
```

Status: **`reported-working`** — this is the vendor's shipped procedure. Not executed here (no hardware in this environment).

### 6.2 Cross-platform equivalent

The `.bat` is Windows-only and the bundled `esptool.exe` is a Windows binary, but the wrapper is plain Python and the underlying command is portable. Composing the offsets and flags above gives:

```bash
esptool.py --chip esp32s3 --port /dev/ttyACM0 --baud 921600 \
  --before default_reset --after hard_reset write_flash -z \
  --flash_mode dio --flash_freq 80m --flash_size 8MB \
  0x0     bootloader.bin \
  0x8000  partition-table.bin \
  0xe000  boot_app0.bin \
  0x10000 CameraWebServer.bin
```

> **Status: `inferred`.** This command is mechanically derived from `esp32_flasher.py` lines 117–119 plus `project_config.json`, both quoted above. It has **not** been executed against hardware in this research pass. The argument values are the vendor's; the assembly into a single invocation is mine.

Notes for actually running it:

- The port is a **native USB CDC** device (`/dev/ttyACM*` on Linux, `/dev/cu.usbmodem*` on macOS), not a USB-UART bridge — see [`pinouts-and-buses.md` §6](pinouts-and-buses.md#6-usb-boot-and-reset).
- If the board is not detected, force the ROM bootloader: **hold BOOT, tap RESET, release BOOT.** `--before default_reset` cannot always do this for you over native USB.
- `--baud 921600` is aggressive over USB-CDC; drop to `460800` or `115200` if you get checksum errors.
- Erasing first (`esptool.py erase_flash`) clears `nvs`, which is usually what you want when recovering a confused board.

### 6.3 Identifying what is currently on a board

Since the factory app has a known ELF SHA-256 and a known build date, you can positively identify an unmodified board by reading back the app descriptor:

```bash
esptool.py --chip esp32s3 --port /dev/ttyACM0 read_flash 0x10000 0x100 head.bin
python3 tools/esp_image_info.py head.bin   # will not fully parse a 256-byte slice
```

More practically, read the whole app slot and parse it:

```bash
esptool.py --chip esp32s3 --port /dev/ttyACM0 read_flash 0x10000 0x330000 app0.bin
python3 tools/esp_image_info.py app0.bin
```

An untouched board reports IDF `v4.4.4`, build `Feb 8 2023 18:07:54`. Status: **`inferred`** — the read-back commands follow standard esptool usage; the parser is **`executed-success`** against the vendor's distributed image.

---

## 7. Bricking and recovery risk

The ESP32-S3 keeps a **mask-ROM** bootloader that cannot be overwritten by `write_flash`. Consequently:

- **You cannot brick this board by flashing bad firmware.** BOOT+RESET always returns you to a flashable state.
- You *can* make it stop enumerating over USB by writing an application that reconfigures or disables USB, or that crashes before USB init. That is not a brick; it is the same BOOT+RESET recovery.
- The genuinely irreversible risks are **eFuse** operations (`espefuse.py`) — enabling flash encryption or secure boot, or burning `DIS_USB_JTAG`. Nothing in the vendor bundle touches eFuses, and you should not either unless you mean it.
- The `coredump` partition at `0x7f0000` is worth knowing about: after a crash, `espcoredump.py` can pull a backtrace out of it, which is far more informative than watching the serial monitor reboot.

## 8. Licensing of these artifacts

| Artifact | Terms | Redistribution status |
|---|---|---|
| `esp32_flasher.py` | **MIT**, declared in-file (`__license__ = "MIT"`) | `allowed` |
| `CameraWebServer.bin`, `bootloader.bin`, `boot_app0.bin`, `partition-table.bin` | No accompanying licence. Derived from Arduino-ESP32 (LGPL-2.1) + ESP-IDF (Apache-2.0) + `esp-dl`; distributed by Seeed as a support download without stated terms | **`unknown`** — retained pending review |
| `esptool.exe` | Espressif esptool is **GPL-2.0**; this is a PyInstaller-packed Windows binary, 7.6 MB | `conditional` (GPL source-offer obligations), and redundant — upstream `esptool.py` is trivially installable |

See [`acquisition/manifest.json`](acquisition/manifest.json) for the per-file disposition and the recommendation on `esptool.exe`.

---

## Related

- [`development.md`](development.md) — building your own firmware
- [`pinouts-and-buses.md`](pinouts-and-buses.md) — USB, boot, reset hardware
- [`commands.md`](commands.md) — full command ledger with execution status
- [`features/camera.md`](features/camera.md) — getting the camera working properly
