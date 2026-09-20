# Factory firmware and flash restore

Retrieved: 2026-08-21; image internals parsed 2026-08-22; source/URL coverage re-verified 2026-08-22. There are **two** complete monolithic images — **one per MCU** — and each is published inside **two different Waveshare archives** (the `-BIN.zip` and the `-Demo.zip`), byte-identical in both. Full provenance, hashes and fallback URLs are in [Provenance](#provenance-where-each-binary-comes-from-and-its-fallback). Verify hashes before writing.

**This board has two MCUs and therefore two firmwares.** Restoring the board means flashing *both*, through *two different USB-C plug orientations*. Flashing one does not touch the other. See [dual-MCU architecture](dual-mcu-architecture.md), and in particular [§6.2 on backing up before you overwrite](dual-mcu-architecture.md#62--back-up-the-factory-esp32-image-before-you-touch-it) — **`ESP32-KNOB_ESP32_0.bin` is the only copy of the Classic Bluetooth application that exists and Waveshare publishes no source for it.**

## The two images

| Target | File | Build metadata | Size | SHA-256 | Flash offset |
|---|---|---|---:|---|---:|
| [ESP32-U4WDH](../../../components/espressif/esp32-u4wdh/README.md) (`U14`, Bluetooth Classic) | `ESP32-KNOB_ESP32_0.bin` | project `TAIJI_KNOB_32`, app version `1`, built 09:24:52 Apr 18 2025; IDF v5.4-727-g5cbd2a3877 | 1,130,672 B | `0c1c21b9822d4c2d80d58534b33eb0083880de4ed7354a38b4c78ba51757349d` | 0x0 |
| [ESP32-S3R8](../../../components/espressif/esp32-s3r8/README.md) (`U2`, GUI) | `WX-ESP32S3-KNOB_V1.2.bin` | V1.2; built 2025-02-28; IDF v5.1.4-972-g632e0c2a9f-dirty; Arduino 3.0.7 | 2,138,224 B | `f7c1cc18b687559f3bd69e5c9ab526bc61c2b2d9c502f38367f7f2bfe4ff8e87` | 0x0 |

Local directory: `artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/`. The separate BIN extraction was removed because both files were byte-identical to these copies. The original BIN ZIP remains in `artifacts/originals/`; hashes are in the [artifact manifest](../../../artifact-manifest.md).

Both are **merged** images: they begin with `0xFF` padding, contain the bootloader, partition table and application, and are written at offset `0x0`.

## Provenance: where each binary comes from, and its fallback

Re-verified 2026-08-22 by re-listing and re-extracting both archives locally and re-hashing every copy.

**Each of the two binaries is obtainable from two separate Waveshare archives.** They are not two different builds — the members are byte-identical across archives, confirmed by SHA-256 below. If one download URL ever fails, the other yields exactly the same firmware.

### `ESP32-KNOB_ESP32_0.bin` — ESP32-U4WDH (`U14`), Bluetooth Classic MCU

| Field | Value |
|---|---|
| Filename | `ESP32-KNOB_ESP32_0.bin` |
| Target MCU | [ESP32-U4WDH](../../../components/espressif/esp32-u4wdh/README.md), ESP-IDF target `esp32`, flash at `0x0` |
| Size | 1,130,672 bytes |
| SHA-256 | `0c1c21b9822d4c2d80d58534b33eb0083880de4ed7354a38b4c78ba51757349d` |
| App build date | 09:24:52 Apr 18 2025 (from the app descriptor) |
| IDF version | `v5.4-727-g5cbd2a3877` |
| Project / app version | `TAIJI_KNOB_32`, app version `1` |
| ZIP member timestamp | 2025-05-27 14:03 (identical in both archives) |
| Local extracted path | `artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/ESP32-KNOB_ESP32_0.bin` |

Obtainable from **both**:

| # | Archive | Path inside archive | Download URL |
|---:|---|---|---|
| 1 | `ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip` | `ESP32-S3-Knob-Touch-LCD-1.8-BIN/ESP32-KNOB_ESP32_0.bin` | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip |
| 2 | `ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` | `ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/ESP32-KNOB_ESP32_0.bin` | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip |

### `WX-ESP32S3-KNOB_V1.2.bin` — ESP32-S3R8 (`U2`), GUI MCU

| Field | Value |
|---|---|
| Filename | `WX-ESP32S3-KNOB_V1.2.bin` |
| Target MCU | [ESP32-S3R8](../../../components/espressif/esp32-s3r8/README.md), ESP-IDF target `esp32s3`, flash at `0x0` |
| Size | 2,138,224 bytes |
| SHA-256 | `f7c1cc18b687559f3bd69e5c9ab526bc61c2b2d9c502f38367f7f2bfe4ff8e87` |
| App build date | 2025-02-28 |
| IDF version | `v5.1.4-972-g632e0c2a9f-dirty` |
| Arduino-ESP32 core | 3.0.7 |
| Version string | `V1.2` (in the filename and the app descriptor) |
| ZIP member timestamp | 2025-06-09 14:06 (identical in both archives) |
| Local extracted path | `artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/WX-ESP32S3-KNOB_V1.2.bin` |

Obtainable from **both**:

| # | Archive | Path inside archive | Download URL |
|---:|---|---|---|
| 1 | `ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip` | `ESP32-S3-Knob-Touch-LCD-1.8-BIN/WX-ESP32S3-KNOB_V1.2.bin` | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip |
| 2 | `ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` | `ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/WX-ESP32S3-KNOB_V1.2.bin` | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip |

### The containing archives

| Archive | Size | SHA-256 | Local original | Contains firmware? | Notes |
|---|---:|---|---|---|---|
| `ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip` | 2,032,893 B | `7d29fc1fb356059f7291eccd74bfb5c9fa7538998bc3f5ff811cd87f04c1691c` | `artifacts/originals/` | Both images, at the archive root under `ESP32-S3-Knob-Touch-LCD-1.8-BIN/` | Small, firmware-only. Preferred download — ~34x smaller |
| `ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` | 68,704,748 B | `11e382444fe93470fbe463829c1e0ebad5bdb5115fd2d72f6159cd7700015030` | `artifacts/originals/` | Both images, under `ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/` | Full Arduino + ESP-IDF source tree; the firmware is a bonus payload inside it |

Practical guidance: **download the BIN ZIP for a restore** — it is 2 MB rather than 69 MB and contains nothing else. Fall back to the Demo ZIP only if the BIN URL fails; it is worth knowing the fallback exists, because Waveshare's file paths are not versioned and have no redirect layer, so a rename would break the direct URL silently.

### Verifying a fresh download

~~~sh
sha256sum ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip
# expect 7d29fc1fb356059f7291eccd74bfb5c9fa7538998bc3f5ff811cd87f04c1691c
unzip -j ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip '*.bin' -d fw && sha256sum fw/*
# expect 0c1c21b9... ESP32-KNOB_ESP32_0.bin
#        f7c1cc18... WX-ESP32S3-KNOB_V1.2.bin
~~~

The same two binary hashes must result from the Demo ZIP. If they differ, Waveshare has published a new build — record it rather than assuming corruption.

### Source pages that publish these archives

The download URLs above are not discoverable on their own; they are linked from the pages below, all of which are recorded as sources for the firmware.

| Source | URL | Role | Local snapshot |
|---|---|---|---|
| Wiki page (live) | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | The canonical resource list linking both archives | `artifacts/source-snapshots/waveshare-wiki-current.html`, `...-current-2026-08-21.html` |
| Wiki page pinned to revision 111069, via the MediaWiki API | `https://www.waveshare.com/w/api.php?action=parse&oldid=111069&prop=text|wikitext|revid` | Immutable citation of the resource list as it stood at 2026-08-07T13:19:04Z. `index.php?oldid=` returns HTTP 404 behind Waveshare's WAF; the `api.php` path works | `artifacts/source-snapshots/waveshare-wiki-oldid-111069.html`, `...-parse.json`, `waveshare-wiki-wikitext-oldid-111069.txt` |
| Storefront product page, ID 31623 | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | Product identity and the "Resources" link into the wiki | `artifacts/source-snapshots/waveshare-product-31623.html`, `...-31623-2026-08-21.html` |

Reading the **wikitext** rather than the rendered HTML matters here: some resource links on Waveshare wiki pages appear only in the wikitext. See the [Waveshare vendor sourcing guide](../../../vendors/waveshare/README.md).

### Mirrors and alternative URLs — searched, none found

Checked 2026-08-22. Recorded as negative results so the search is not repeated:

| Candidate | Result |
|---|---|
| Internet Archive Wayback, both ZIP URLs | **No snapshots.** `archive.org/wayback/available` returns an empty `archived_snapshots` object for both |
| `https://files.waveshare.com/upload/<file>` | HTTP 404 |
| `https://www.waveshare.com/w/upload/<file>` | HTTP 404 (this path serves wiki *images*, not resource ZIPs) |
| `https://www.waveshare.com/wiki/File:<file>` | HTTP 404 — the ZIPs are not MediaWiki file-namespace uploads |
| Both canonical `files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/...` URLs | HTTP 200, `application/zip` — both still live |

**There is no third-party mirror and no archival copy of these archives that we could locate.** The only redundancy that exists is the one documented above: two Waveshare archives carrying the same two binaries, on the same host. That is redundancy against a *path* change, not against the host disappearing. The local copies in `artifacts/originals/` are therefore the only offline guarantee, and should be treated as the authoritative retained copy. Uploading a snapshot to the Wayback Machine would be a cheap improvement but has not been done.

## ESP32-U4WDH image internals

Parsed directly from the binary:

- Bootloader at `0x1000` (ESP32 convention), header chip-id `0` = ESP32, flash config byte `0x20` → **4 MB @ 40 MHz**
- Application at `0x10000`, app descriptor magic `0xABCD5432`, `secure_version` 0 (no Secure Boot / anti-rollback)

Partition table at `0x8000`:

| Label | Type | Subtype | Offset | Size |
|---|---|---|---:|---:|
| `nvs` | data | nvs | `0x9000` | `0x6000` (24 KB) |
| `phy_init` | data | phy | `0xF000` | `0x1000` (4 KB) |
| `factory` | app | factory | `0x10000` | `0x190000` (1.5625 MB) |
| `storage` | data | **SPIFFS** (subtype `0x82`) | `0x1A0000` | `0x160000` (1.375 MB) |

Notes:

- **Single app slot, no OTA partitions, no `otadata`.** This firmware cannot self-update over the air and there is no rollback slot. Nor is there room to add one: `factory` is 1.5625 MB and the only reclaimable space is `storage`. **The U4WDH is not OTA-capable at any layer** — updating it always means a USB cable and a plug flip. See [Dual-MCU architecture §5](dual-mcu-architecture.md#5-ota-the-s3-can-the-u4wdh-cannot).
- The image *does* contain `esp_ota_ops.c` and `Error in write_otadata operation` strings, linked in by the IDF's `app_update` component. **This is dead code** — with no `otadata` partition and one app slot it can never succeed. Do not read it as OTA support.
- **Correction (2026-08-22):** the `storage` subtype byte is `0x82` = `ESP_PARTITION_SUBTYPE_DATA_SPIFFS`, not FAT. Earlier revisions of this page said FAT.
- The `storage` partition is **not present in the shipped file** (the image ends at `0x1101B0`), so it is formatted on first boot. Anything Waveshare intended to live there is not recoverable from this file — **only a full `read_flash` backup off a factory-state board captures it.**
- Only 3 MB of the 4 MB is partitioned; the top 1 MB is unallocated.
- The `nvs` partition holds the **Bluetooth pairing state** — key `PEERADDR`. See "Resetting Bluetooth pairing" below.

## ESP32-S3R8 image internals

Parsed directly from the binary 2026-08-22.

- Bootloader at `0x0` (ESP32-S3 convention), image header chip-id `0x0009` = ESP32-S3, flash config byte `0x4F` → **16 MB @ 80 MHz**
- Application at `0x10000`, app descriptor magic `0xABCD5432`, project name `arduino-lib-builder`, version `599b76d`, built 12:10:29 Feb 28 2025, IDF `v5.1.4-972-g632e0c2a9f-dirty`

Partition table at `0x8000`:

| Label | Type | Subtype | Offset | Size |
|---|---|---|---:|---:|
| `nvs` | data | nvs (`0x02`) | `0x009000` | `0x5000` (20 KB) |
| **`otadata`** | data | **ota (`0x00`)** | `0x00E000` | `0x2000` (8 KB) |
| **`app0`** | app | **ota_0 (`0x10`)** | `0x010000` | `0x300000` (3 MB) |
| **`app1`** | app | **ota_1 (`0x11`)** | `0x310000` | `0x300000` (3 MB) |
| `spiffs` | data | spiffs (`0x82`) | `0x610000` | `0x9E0000` (9.875 MB) |
| `coredump` | data | coredump (`0x03`) | `0xFF0000` | `0x10000` (64 KB) |

Notes:

- **Two app slots plus `otadata` — this layout is genuinely OTA-capable**, with rollback, and 3 MB of headroom per slot. Exactly the opposite of the U4WDH image.
- **But the shipped application does not implement OTA.** No `esp_https_ota`, `ArduinoOTA` or `Update.h` strings appear in the image, and the embedded HTTP server's complete URI set — `/aida64`, `/clockbg`, `/configwifi`, `/docmd`, `/getstatus`, `/mjpeg`, `/music`, `/pic`, `/root`, `/save`, `/saveweather`, `/spiffs`, `/txt`, `/wifilist` — contains no `/update` or `/ota` endpoint, and the web control panel's JavaScript exposes no firmware field. **Capable ≠ implemented.** Your own S3 firmware can add OTA trivially on top of this existing layout.
- The `spiffs` partition is **not present in the shipped file** (2,138,224 B ends inside `app0`), so it is formatted on first boot.
- The application is a **third-party PlatformIO/Arduino build**, not built from Waveshare's demo tree — its build paths point at `C:/Users/Fei/.platformio/…`. `arduino-lib-builder` is the Arduino-ESP32 libs-builder placeholder project name, not the application's real name.

## Restore procedure

### 1. Back up before you overwrite anything

~~~sh
esptool --chip esp32   --port PORT --baud 921600 read_flash 0x0 0x400000  esp32-u4wdh-backup.bin
esptool --chip esp32s3 --port PORT --baud 921600 read_flash 0x0 0x1000000 esp32-s3-backup.bin
~~~

(4 MB and 16 MB respectively. Remember these are two different USB-C orientations.)

### 2. Identify which MCU you are connected to

~~~sh
esptool --port PORT --baud 115200 chip_id
~~~

Confirm the reported target. **If it is the wrong MCU, or no port appears, disconnect, rotate the Type-C plug 180 degrees, and reconnect.** Plug orientation selects which MCU the single USB-C receptacle reaches:

| Orientation | Reaches | Via |
|---|---|---|
| one way | ESP32-S3R8 | S3 native USB peripheral (GPIO19/20) |
| the other way | ESP32-U4WDH | USB-UART bridge `U10`, auto-reset from `RTS#`→`EN` and `DTR#`→`IO0` |

While you are here, **note the chip revision and core count that `chip_id` reports for the ESP32-U4WDH** — that is the cheapest way to answer the [single-core vs dual-core question](../../../components/espressif/esp32-u4wdh/README.md#2--the-core-count-and-clock-speed-caveat-unresolved).

### 3. Flash the matching image at offset 0x0

~~~sh
# ESP32-U4WDH — the Bluetooth Classic MCU
esptool --chip esp32 --port PORT --baud 921600 write_flash -z 0x0 ESP32-KNOB_ESP32_0.bin

# ESP32-S3R8 — the GUI MCU
esptool --chip esp32s3 --port PORT --baud 921600 write_flash -z 0x0 WX-ESP32S3-KNOB_V1.2.bin
~~~

### 4. Rotate the plug and flash the other MCU

Then power-cycle / toggle the power switch after both succeed. Reduce baud to 115200 if the connection is unreliable.

### 5. Verify

~~~sh
esptool --chip esp32   --port PORT verify_flash 0x0 ESP32-KNOB_ESP32_0.bin
esptool --chip esp32s3 --port PORT verify_flash 0x0 WX-ESP32S3-KNOB_V1.2.bin
~~~

## Restoring only one MCU

You can, and often should. The two images are independent and the flashing operations do not interact.

But **do not leave the halves mismatched for long.** The two firmwares cooperate over an undocumented UART protocol and share the audio hardware, so a mismatched pair will behave oddly rather than fail cleanly:

- The DAC's `XSMT` mute line is driven **only** by the ESP32-U4WDH (GPIO32). If you replace that firmware with something that never drives GPIO32 high, **all audio dies — including audio originating on the ESP32-S3**, which has no way to un-mute the DAC.
- The CH445P audio mux select is driven **only** by the ESP32-S3 (GPIO0). If you replace the S3 firmware, the ESP32's audio may never be routed to the DAC.
- Track metadata and album art on the LCD come over the inter-MCU UART. Replace either side and the display simply stops updating with now-playing information.

See [shared audio output](dual-mcu-architecture.md#43-the-awkward-exception-split-audio-control), and [§6.3 on exactly what breaks when you replace one side](dual-mcu-architecture.md#63-does-replacing-the-s3-firmware-break-bluetooth).

## Resetting Bluetooth pairing without a full reflash

The ESP32-U4WDH stores its paired peer address in NVS (key `PEERADDR`). Erasing the NVS partition forces re-pairing while leaving the application intact:

~~~sh
esptool --chip esp32 --port PORT erase_region 0x9000 0x6000
~~~

The stock firmware also exposes a "Clear BT A2DP pair" action through the S3's UI, which relays the request over the inter-MCU UART — use that first if the stock firmware is still installed.

## Safety

These commands overwrite each target's bootloader, partition table and application, because each file is a merged image beginning at `0x0`. Back up custom flash first.

**Never flash the ESP32 image to the ESP32-S3 or vice versa.** Check `chip_id`, filename and hash each time. `esptool` will normally refuse on the chip-id check, but only if you let it auto-detect rather than forcing `--chip`.

Neither image uses Secure Boot or flash encryption (`secure_version` 0 on the ESP32 image), so there is no risk of burning an irreversible eFuse during a normal `write_flash` — but do not run `espefuse burn_*` commands casually while investigating the chip revision. `espefuse summary` is read-only and safe.
