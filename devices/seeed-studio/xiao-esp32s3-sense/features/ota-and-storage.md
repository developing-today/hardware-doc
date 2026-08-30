# OTA updates and flash storage — XIAO ESP32S3 Sense

> Where firmware and data live in the 8 MB flash, and how to update over the air.
> Snapshot **2026-08-24**. No hardware testing. Partition data is **parsed from the factory image** ([`../factory-firmware.md`](../factory-firmware.md)), so it is primary evidence.

## 1. The flash map you actually have

Parsed from the shipped `partition-table.bin`:

| Partition | Type | Offset | Size | Purpose |
|---|---|---:|---:|---|
| `nvs` | data/nvs | `0x009000` | 20 KB | Wi-Fi credentials, key-value settings |
| `otadata` | data/ota | `0x00e000` | 8 KB | Which OTA slot to boot |
| **`app0`** | app/ota_0 | `0x010000` | **3,264 KB** | Running application |
| **`app1`** | app/ota_1 | `0x340000` | **3,264 KB** | OTA target |
| `spiffs` | data/spiffs | `0x670000` | 1,536 KB | User filesystem |
| `coredump` | data | `0x7f0000` | 64 KB | Crash dumps |

Total: exactly **8.00 MB**, fully allocated.

**This is the stock Arduino "8M with spiffs" scheme**, and it is what the board ships with.

## 2. ⚠ The 3,264 KB application ceiling is the real constraint

The factory `CameraWebServer.bin` is **2,941,584 bytes — 90 % of the slot.**

That is with camera + Wi-Fi + `esp-dl`. Adding BLE (Bluedroid), a TinyML model, or a TLS stack on top of a camera application will overflow. This is the single most common reason a build fails to flash on this board.

Your options when you run out:

| Scheme | App space | OTA? | Use when |
|---|---:|---|---|
| **8M with spiffs** (default) | 3,264 KB | ✅ | Balanced; what ships |
| **Huge APP (3 MB no OTA)** | ~3,072 KB | ❌ | TinyML, large models — frees `app1` |
| **8M Flash (custom)** | up to ~7 MB | ❌ | Very large single app |
| Custom `partitions.csv` | your choice | your choice | Production designs |

**Choosing "Huge APP" does not double your space** — it removes the OTA slot but does not merge it into `app0` under the stock definitions. To genuinely get >3.3 MB you need a **custom partition table**. That is the honest answer, and it is often misunderstood.

Custom table example (no OTA, ~6.5 MB app, small SPIFFS):

```csv
# Name,   Type, SubType, Offset,   Size,     Flags
nvs,      data, nvs,     0x9000,   0x5000,
phy_init, data, phy,     0xe000,   0x1000,
factory,  app,  factory, 0x10000,  0x650000,
spiffs,   data, spiffs,  0x660000, 0x190000,
coredump, data, coredump,0x7f0000, 0x10000,
```

Status: **`inferred`** — a standard ESP-IDF layout arithmetic-checked against the 8 MB device. Not flashed.

## 3. OTA — how it works here

The dual `app0`/`app1` layout is standard ESP-IDF A/B updating:

1. Running from `app0`, the device downloads a new image into `app1`.
2. On success it writes `otadata` to point at `app1` and reboots.
3. If the new image fails to validate or mark itself good, the bootloader **rolls back** to `app0`.

Arduino sketch outline:

```cpp
#include <WiFi.h>
#include <HTTPUpdate.h>

WiFiClient client;
t_httpUpdate_return ret = httpUpdate.update(client, "http://server/firmware.bin");
switch (ret) {
  case HTTP_UPDATE_FAILED:
    Serial.printf("failed (%d): %s\n", httpUpdate.getLastError(),
                  httpUpdate.getLastErrorString().c_str());
    break;
  case HTTP_UPDATE_NO_UPDATES: Serial.println("no update"); break;
  case HTTP_UPDATE_OK:         Serial.println("ok, rebooting"); break;
}
```

`ArduinoOTA` (push over the network from the IDE) also works and is convenient during development.

Status: **`inferred`** — standard Arduino-ESP32 usage. Not tested on this board.

### Board-specific OTA notes

- **Your image must fit in 3,264 KB.** OTA cannot install an image larger than the target slot, so a build that only just fits `app0` when flashed over USB may still be un-OTA-able.
- **The antenna must be fitted.** A 3 MB download over a [detached U.FL antenna](wifi-and-bluetooth.md#2-the-antenna-is-detachable-and-there-is-no-fallback) will fail or crawl.
- **Power matters.** A ~3 MB download plus flash writes is a sustained load. On battery, with the camera also drawing, this is a bad moment to be near cut-off.
- **`esp32-birdnet-mic` implements OTA on this hardware** — see [`../examples/selected/esp32-birdnet-mic/`](../examples/selected/esp32-birdnet-mic/), which ships both a web flasher and manual OTA images. It is the only surveyed project that does.


## 3A. TinyUF2 — drag-and-drop flashing (undocumented by Seeed)

Seeed's Arduino board package ([`artifacts/kicad/xiao-esp32s3-package.zip`](../artifacts/kicad/xiao-esp32s3-package.zip), retained) contains files that are **not mentioned anywhere in Seeed's wiki**:

```
XIAO_ESP32S3/bootloader-tinyuf2.bin      21,408 B
XIAO_ESP32S3/tinyuf2.bin                141,936 B
XIAO_ESP32S3/partitions-8MB-tinyuf2.csv     397 B
```

**TinyUF2 makes the board appear as a USB mass-storage drive.** You update firmware by dragging a `.uf2` file onto it — no `esptool`, no drivers, no serial port. It is the same mechanism used by Adafruit and Raspberry Pi Pico boards, and it is genuinely useful for handing a device to a non-technical user.

The alternate partition layout it requires:

| Partition | Type | Offset | Size |
|---|---|---:|---:|
| `nvs` | data/nvs | `0x9000` | 20 KB |
| `otadata` | data/ota | `0xe000` | 8 KB |
| `ota_0` | app | `0x10000` | **2,048 KB** |
| `ota_1` | app | `0x210000` | **2,048 KB** |
| **`uf2`** | app/factory | `0x410000` | 256 KB |
| **`ffat`** | data/fat | `0x450000` | **3,776 KB** |

The Arduino board definition calls this **"TinyUF2 Compatibility (2MB APP / 3.7MB FFAT)"**, and flashes `tinyuf2.bin` to `0x410000` alongside a `bootloader_tinyuf2`.

### The trade-off is significant

| | Standard "8M with spiffs" | **TinyUF2** |
|---|---:|---:|
| **App slot** | **3,264 KB** | **2,048 KB** — 37 % smaller |
| Filesystem | 1,536 KB SPIFFS | **3,776 KB FAT** |
| Flashing | esptool / serial | **drag-and-drop** |

**The factory `CameraWebServer.bin` is 2,941,584 bytes — it does not fit in a 2,048 KB TinyUF2 app slot.** So TinyUF2 and a full-featured camera application are effectively mutually exclusive on this board. That is very likely why Seeed ships the standard scheme and does not advertise the UF2 option.

TinyUF2 is worth considering for **non-camera** XIAO ESP32S3 projects that need easy field updates, and for the larger FAT partition if you are storing data on internal flash rather than SD.

> Status: **`inferred`** — the files, the partition CSV and the `boards.txt` menu entries are primary evidence that the option exists and how it is laid out. **Not tested**, and Seeed documents none of it.

## 4. The other storage options

| Store | Size | Survives reflash? | Use for |
|---|---:|---|---|
| **NVS** | 20 KB | ✅ (unless erased) | Wi-Fi credentials, settings, counters |
| **SPIFFS** | 1,536 KB | ✅ | Web assets, config files, small logs |
| **microSD** | ≤ 32 GB | ✅ | Images, audio, bulk logs — [`microsd.md`](microsd.md) |
| **PSRAM** | 8 MB | ❌ volatile | Framebuffers, model arenas |
| `coredump` | 64 KB | — | Post-crash backtraces |

### NVS

```cpp
#include <Preferences.h>
Preferences prefs;
prefs.begin("myapp", false);
prefs.putUInt("boots", prefs.getUInt("boots", 0) + 1);
prefs.end();
```

`nvs` is where the Arduino Wi-Fi stack caches credentials. `esptool.py erase_flash` wipes it — which is often exactly what you want when recovering a confused board.

### SPIFFS

1,536 KB, flat namespace (no directories). Uploadable from the Arduino IDE with the ESP32 Sketch Data Upload plugin, or built with `mkspiffs`.

**Note SPIFFS is deprecated upstream in favour of LittleFS**, which is more robust against power loss and supports directories. Both are available in Arduino-ESP32; LittleFS is the better choice for new work. The partition is the same — only the filesystem driver differs.

## 5. `coredump` — an underused debugging asset

The factory table reserves **64 KB at `0x7f0000`** for crash dumps. Because [JTAG is unavailable with the daughterboard attached](../pinouts-and-buses.md#72-the-camera-and-microphone-occupy-all-four-jtag-pins), this is one of the few real post-mortem tools you have:

```bash
esptool.py --chip esp32s3 --port /dev/ttyACM0 read_flash 0x7f0000 0x10000 core.bin
espcoredump.py info_corefile -c core.bin -t raw build/your_app.elf
```

Status: **`inferred`** — standard ESP-IDF procedure with this board's offsets substituted. Not run.

Worth enabling in any project you cannot debug interactively — which on a Sense board is all of them.

## 6. Practical guidance

- **Do not casually change the partition scheme** on a board whose data you care about — reflashing with a different layout invalidates SPIFFS contents and can strand NVS.
- **Check your binary size early.** `Sketch uses X bytes (Y%) of program storage` in the Arduino output is the number that matters; if Y is above ~85 % you are close to un-OTA-able.
- **If you need OTA *and* a big application, buy the [XIAO ESP32S3 Plus](../comparisons-and-recommendations.md#6-versus-the-xiao-esp32s3-plus--examined-from-the-schematics)** ($7.90, **16 MB** flash) rather than fighting the 8 MB layout — but note it cannot take the camera daughterboard.

## 7. Coverage status

Partition data is **primary evidence** (parsed from the shipped binary with [`tools/esp_image_info.py`](../../../../tools/esp_image_info.py)). The OTA and coredump procedures are **`inferred`** — standard Espressif/Arduino usage with this board's offsets, not executed here.

One vendored project ([`esp32-birdnet-mic`](../examples/selected/esp32-birdnet-mic/)) demonstrates OTA on this hardware in practice.

## 8. Related
- [`../factory-firmware.md`](../factory-firmware.md) — where the partition table came from, and restore procedure
- [`microsd.md`](microsd.md) — bulk storage
- [`../development.md`](../development.md) — partition-scheme selection in the IDE
- [`tinyml.md`](tinyml.md) — the main reason people run out of app space
