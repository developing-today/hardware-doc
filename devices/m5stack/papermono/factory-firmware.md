# Factory firmware — M5Stack PaperMono

> Two whole-flash ESP32-S3 images for SKU **C153 / C153-LITE**, retrieved from the M5Burner
> public API on **2026-09-01** and retained in [`artifacts/firmware/`](artifacts/firmware/).
> Both were validated by content (`0xE9` ESP32 image magic), parsed, and mined for strings
> **before** anything was written here.
>
> ## ⚠ Nothing was flashed, and nothing was run
>
> Every parse on this page is `executed-success` **as static analysis of a file on disk**
> ([`commands.md` §5](commands.md#5-firmware-image-inspection)). Every statement about what the
> device *does* when these bytes run is `inferred` from strings and source, never observed.
> No serial port was opened in this session; `esptool` was never invoked.

## Contents

- [1. Both images at a glance](#1-both-images-at-a-glance)
- [2. The official image — `C153-PaperMono-UserDemo-v1.2.bin`](#2-the-official-image--c153-papermono-userdemo-v12bin)
- [3. The community image — `crosspoint-paper-mono-cjk-1.5.0-RC.bin`](#3-the-community-image--crosspoint-paper-mono-cjk-150-rc)
- [4. Partition maps — three different layouts are in evidence](#4-partition-maps--three-different-layouts-are-in-evidence)
- [5. What the device does on power-up](#5-what-the-device-does-on-power-up)
- [6. Why `c78f6c5-dirty` means not reproducible](#6-why-c78f6c5-dirty-means-not-reproducible)
- [7. Flashing and recovery — authoritative versus inferred](#7-flashing-and-recovery--authoritative-versus-inferred)
- [8. Provenance, distribution and licensing](#8-provenance-distribution-and-licensing)
- [9. Open questions](#9-open-questions)

---

## 1. Both images at a glance

The fields the method requires to be prominent, for both images:

| Field | `C153-PaperMono-UserDemo-v1.2.bin` | `crosspoint-paper-mono-cjk-1.5.0-RC.bin` |
|---|---|---|
| **Target MCU** | **ESP32-S3** (`chip_id 9`), `min_rev 0` | **ESP32-S3** (`chip_id 9`), `min_rev 0` |
| **Compatible hardware** | **C153 and C153-LITE** — one image serves both; the variant is detected at runtime | PaperMono (M5Burner lists `deviceName: Paper`) |
| **Image role** | **Merged whole-flash image**: second-stage bootloader + partition table + application in one file | **Merged whole-flash image**, same structure |
| **Expected flash offset** | **`0x0`** | **`0x0`** |
| **Companion images required** | **None.** Bootloader and partition table are inside the file | **None** |
| **Version identifier** | app version **`c78f6c5-dirty`**, M5Burner version **v1.2** | app version **`paper-mono-v2-15-g87a191f`**, M5Burner version **1.5.0-RC** |
| **Build date** | **2026-08-06 16:12:13** | **2026-08-22 19:58:33** |
| **SDK / toolchain** | **ESP-IDF v5.5.1** | **ESP-IDF 5.5.2.260206**, built through **PlatformIO** with the arduino-esp32 framework |
| **Project name** | `PaperMono-UserDemo` | `crosspoint-reader-mono` |
| **Flash settings in header** | **DIO**, 80 MHz, 16 MB | **DIO**, 80 MHz, 16 MB |
| **Bootloader entry** | `0x403c8924` | `0x403c88b8` |
| **App entry** | `0x40375bec` | `0x40375fe0` |
| **Segments** (bootloader / app) | 3 / 7 | 3 / 7 |
| **Byte size** | **2 868 208** | **10 319 500** |
| **SHA-256** | `72c290bc2ffa216041b276660277369bd17ecef92315e367d98bb2c96c8428fa` | `e2dee32b468da1d743b9fe8889eca959f5c0acdbe09c8f4cc3e69c69f8ebe935` |
| **Class** | primary (vendor, `sourceType: OFFICIAL`) — **S38** | community (`sourceType: COMMUNITY`) — **S39** |
| **Local path** | [`artifacts/firmware/C153-PaperMono-UserDemo-v1.2.bin`](artifacts/firmware/C153-PaperMono-UserDemo-v1.2.bin) | [`artifacts/firmware/crosspoint-paper-mono-cjk-1.5.0-RC.bin`](artifacts/firmware/crosspoint-paper-mono-cjk-1.5.0-RC.bin) |

**Both hashes were recomputed from the retained files on 2026-09-01 and match the values in
[`acquisition/manifest.json`](acquisition/manifest.json) and [`sources.md`](sources.md).**

Reading this table practically: the two images are the same *shape* — whole-flash, ESP32-S3,
DIO/80 MHz/16 MB, three-plus-seven segments — and differ in everything above that line. Anything
you learn about flashing one applies mechanically to the other. What does **not** transfer is
the flash *map*: they carve the 16 MB up completely differently (§4), so writing one over the
other leaves stale partitions from the previous occupant anywhere the new table does not reach.

**Both images report DIO although the vendor's published build config says `qio_opi`.** The
hardware supports QIO — all four flash data lines are routed and the fitted
`XM25UH128DHIQT`'s `QE` bit is factory-set — and `sdkconfig.defaults` pins no flash mode, so
DIO is an ESP-IDF default rather than a hardware limit. Not a defect; resolved as
[R2](gaps-and-conflicts.md#r2--qio-versus-dio-flash--resolved).

## 2. The official image — `C153-PaperMono-UserDemo-v1.2.bin`

### 2.1 Headers, as parsed

```
-- bootloader image header @0x0 --
  magic 0xe9  segments 3  flash_mode DIO  flash_size 16MB  flash_freq 80MHz
  entry 0x403c8924  chip_id 9 (ESP32-S3)  min_rev 0

-- app image header @0x10000 --
  magic 0xe9  segments 7  flash_mode DIO  flash_size 16MB  flash_freq 80MHz
  entry 0x40375bec  chip_id 9 (ESP32-S3)  min_rev 0

-- esp_app_desc_t @0x10020 --
  project_name  PaperMono-UserDemo
  app_version   c78f6c5-dirty
  build_time    16:12:13
  build_date    Aug  6 2026
  idf_version   v5.5.1
```

`min_rev 0` means the image declares no minimum silicon revision, so it will load on any
ESP32-S3 stepping. That is the permissive default and carries no information about which
stepping the board actually carries — the package marking is not published and no unit was in
hand.

### 2.2 M5Burner catalogue metadata

From the public API (S33, S34 — `/api/v1/firmwares/{id}` is open, while `/api/firmwares/{id}`
returns `401 请先登录`):

| Field | Value |
|---|---|
| `firmwareId` | `2089640807996628993` |
| `firmwareName` | **"PaperMono UserDemo"** |
| `firmwareDescription` | **"PaperMono / PaperMono-Lite UserDemo"** |
| `sourceType` | `OFFICIAL`; developer `m5stack`, `userId 1` |
| `sourceUrl` | `null` |
| Categories | "Development & Learning", "E-books & Reading" |
| `uploadedAt` / `publishTime` | **2026-08-18T17:09:29+08:00** |
| `versionName` | **v1.2** |
| `binFileName` | `C153-PaperMono-ESP32S3R8-UserDemo-V1.2-yaozhenquan-8300e309-20260806_0x00.bin` |
| `deviceName` | `Paper` |
| `downloadCount` | **16** (point-in-time, 2026-09-01) |

Three things fall straight out of this record.

**The description is the proof that one image serves both SKUs.** *"PaperMono / PaperMono-Lite
UserDemo"* — and the EasyLoader executable both product pages link (S40) lives under
PaperMono's asset folder `1267/`, not the Lite's `1268/`. That is why the firmware performs
runtime variant detection (§5).

**The catalogue's `binFileName` is not the name of the object served, and it embeds a
*different* build identifier.** The served object is `…/bin/2089640808000823299.bin`; the
catalogue name encodes a developer (`yaozhenquan`), a build id **`8300e309`** and the date
`20260806`. But `esp_app_desc_t` inside those same bytes says **`c78f6c5-dirty`**. Two
identifiers, same artifact, and they do not agree — recorded as an open question in §9 rather
than resolved by picking one.

**The `_0x00` suffix is the vendor's own statement of the flash offset**, and it corroborates
the parse: this is a whole-flash image written at `0x0`.

### 2.3 Notable strings, and what they establish

Extracted with `strings -n 6` — 8 192 lines, working copy at
`archive/devices/m5stack/papermono/artifacts/research-scratch/docs/firmware/C153-PaperMono-UserDemo-v1.2.strings.txt`
(regenerable from the retained `.bin` by [`commands.md` §5](commands.md#5-firmware-image-inspection)).
These are the rows that establish something the vendor's prose does not.

| String | What it establishes |
|---|---|
| `I (%lu) %s: [Autodetect] board_M5PaperMono` | The board enum the Arduino board name maps to — independent corroboration of the target in [`development.md` §2](development.md#2-board-target-and-profile) |
| `[I][%s] M5PM1 initialized at address 0x%02X (I2C: %lu Hz)` | The M5PM1 address and bus clock are read from the device at runtime, not hard-coded in prose |
| `[I][%s] M5IOE1 initialized at address 0x%02X (I2C: %lu Hz)` | Same for the expander |
| `PM1 shutdown, wake by BMI270 INT1 -> PM1 G4 falling edge` | **M5PM1 G4 = IMU wake, and it is falling-edge.** The vendor's prose says the IMU interrupt is active-high; the code and this binary both say active-low ([R3](gaps-and-conflicts.md#r3--bmi270-interrupt-polarity--resolved-against-the-vendor-prose)) |
| `PM1 shutdown, wake by RX8130 timer -> PM1 G0 falling edge` | **M5PM1 G0 = RTC wake.** Also that these are *M5PM1* pins, not expander pins |
| `ESP32 deep sleep, wake by touch INT GPIO%d low` | Touch wake is an **ESP32-S3 EXT0** wake, i.e. a different mechanism from the two M5PM1 wakes |
| `IMU wake line still active, shutdown canceled` · `RTC wake line still active, shutdown canceled` | The firmware **refuses to shut down while a wake line is asserted** — a real design decision that prevents an immediate self-wake |
| `W (%lu) %s: M5PM1/M5IOE1 init failed; RGB/NFC/TF controls are disabled` | Confirms the architectural claim: without the two auxiliary MCUs you lose LED, NFC and card control |
| `I (%lu) %s: NFC identity probe: ok=%d identity=0x%02X type=0x%02X rev=0x%02X` | The runtime SKU probe (§5) |
| `I (%lu) %s: Board variant detected: %s` | …and that its result is logged |
| `Found %luMB PSRAM device` · `SPI SRAM memory test OK` | PSRAM is brought up and **tested** at boot |
| `/sdcard`, `NO FOUND` / `CARD FOUND` / `DET READ FAIL` | The microSD mount point and the card-detect state machine's three outcomes |
| `time.google.com`, `time.nist.gov`, `pool.ntp.org` | The three NTP servers the clock app tries |
| `QWERTYUIOP` / `asdfghjkl` / `@#$&*()'"` | There is an **on-screen keyboard** — for SSID and password entry |
| `FeliCa Lite-S`, `FeliCa Lite`, `Tag-it HF-I Pro` | Tag-type names the NFC app can print. **Evidence of intent, not of interoperability** — no card has been read on a real board by anyone |
| `AppBattery` `AppBrightness` `AppBuzzer` `AppClock` `AppImu` `AppLora` `AppMicWave` `AppNfcScan` `AppRgb` `AppShutdown` `AppSleepWake` `AppTfCard` `AppWifiScan` | The thirteen application symbols that survive in the binary |

On that last row: the source analysis of `M5PaperMono-UserDemo/main/apps/` records **fifteen**
application directories, including a keyboard app. Only thirteen `App…` class-name strings
survive in the shipped binary — the keyboard, for instance, is visible only through its layout
strings. **Do not read "thirteen" as a count of features**; it is a count of symbols that
happened to survive compilation. `inferred`.

### 2.4 The build environment left no developer path in the binary

Every IDF source path in the official image is stripped to a `//IDF/components/…` prefix — for
example `//IDF/components/esp_psram/system_layer/esp_psram.c`. No home directory, no user name,
no absolute build path appears anywhere. Contrast §3.3, where the community image leaks its
builder's home directory in full. Recorded because it is the kind of detail that identifies a
build system, and because it is the *only* thing in the official binary that resembles build
provenance beyond `esp_app_desc_t`.

## 3. The community image — `crosspoint-paper-mono-cjk-1.5.0-RC`

Retained because it is **not vendor firmware and is not reproducible**, and because it is the
only independent binary evidence that units actually shipped and ran third-party code.

### 3.1 Headers, as parsed

```
-- bootloader image header @0x0 --
  magic 0xe9  segments 3  flash_mode DIO  flash_size 16MB  flash_freq 80MHz
  entry 0x403c88b8  chip_id 9 (ESP32-S3)  min_rev 0

-- app image header @0x10000 --
  magic 0xe9  segments 7  flash_mode DIO  flash_size 16MB  flash_freq 80MHz
  entry 0x40375fe0  chip_id 9 (ESP32-S3)  min_rev 0

-- esp_app_desc_t @0x10020 --
  project_name  crosspoint-reader-mono
  app_version   paper-mono-v2-15-g87a191f
  build_time    19:58:33
  build_date    Aug 22 2026
  idf_version   5.5.2.260206
```

**`paper-mono-v2-15-g87a191f` is a `git describe` string**, and it is the interesting contrast
with the official image: it names tag `paper-mono-v2`, **15** commits of distance, and commit
**`87a191f`**. That is enough to identify a source revision. The official image's
`c78f6c5-dirty` is not (§6). The community build is, on this narrow measure, better documented
than the vendor build.

### 3.2 M5Burner catalogue metadata

| Field | Value |
|---|---|
| `firmwareId` | `2091144466157694978` |
| `firmwareName` | **"CrossPoint-PaperMono-CJK"** |
| `sourceType` | `COMMUNITY`; developer **`IAMLIUBO`**, `userId 3966`, website `https://github.com/imliubo` |
| `sourceUrl` | `https://github.com/MarsTechHAN/crosspoint-reader-mono` |
| `uploadedAt` | **2026-08-22T20:44:29+08:00** — one day after launch |
| `versionName` | **1.5.0-RC**; description 「针对PaperMono做了CJK的优化, 与官方版本有所不同」 ("CJK optimisation for PaperMono; differs from the official version") |
| `binFileName` | `crosspoint-paper-mono-full-with-cjk.bin` |
| `downloadCount` | **24** (point-in-time, 2026-09-01) |

**The uploader and the upstream author are different people.** `sourceUrl` points at
`MarsTechHAN/crosspoint-reader-mono` while the uploading account is `IAMLIUBO`. Do not read a
M5Burner `sourceUrl` as the identity of the person who built the bytes.

**The community image had been downloaded more times than the official one** — 24 against 16,
as counted on 2026-09-01. Both counters are tiny and point-in-time, so this establishes almost
nothing about popularity; it is recorded because it is a *measured* number in a record that has
very few of them, and because it is consistent with the community's interest in this board
being reader-shaped rather than dev-board-shaped.

### 3.3 Notable strings

| String | What it establishes |
|---|---|
| `/Users/imliubo/.platformio/packages/framework-arduinoespressif32/libraries/Wire/src/Wire.cpp` (and `SPI`, `WiFi`, `Network…`) | **Built with PlatformIO and the arduino-esp32 framework, on macOS, by `imliubo`** — which independently corroborates the M5Burner developer record's `github.com/imliubo` website field. Two unrelated surfaces, same identity |
| `CrossPoint version: 1.5.0-paper-mono` | The application's own version string, matching the catalogue |
| `cjkfont`, `Built-in CJK font partition not found`, `Could not mmap %u-byte CJK font` | The 4 MB `cjkfont` partition is **memory-mapped**, not read through a filesystem |
| `stbtt__GetGlyphShapeTT`, `stbtt_FindGlyphIndex` | Font rasterisation is `stb_truetype` |
| `/.crosspoint/settings.json`, `/opds.json`, `/recent.json`, `/wifi.json`, `/koreader.json` | It keeps its state in a `.crosspoint` directory **on the microSD card**, and it interoperates with **KOReader** progress data and **OPDS** catalogues |
| `/.fonts`, `.cpfont`, `/.cover.jpg`, `/.cover.png` | User fonts and book covers are read from the card too |
| `OTA app partition slot`, `ota data partition invalid, falling back to factory` | These are stock IDF bootloader strings and are present in **both** images. **They do not mean OTA is configured** — the partition table is what decides that, and neither image has an `otadata` partition (§4) |

That last row is worth stating plainly because it is an easy misreading: finding OTA strings in
a binary tells you the bootloader was compiled with OTA support, which it always is. It says
nothing about whether the flash map has anywhere to put a second app.

## 4. Partition maps — three different layouts are in evidence

### 4.1 The shipped official layout (= both vendor projects' `partitions.csv`)

| Name | Type | SubType | Offset | Size | |
|---|---|---|---:|---:|---|
| `nvs` | data (1) | `0x02` nvs | `0x009000` | `0x006000` | 24 K |
| `phy_init` | data (1) | `0x01` phy | `0x00F000` | `0x001000` | 4 K |
| `factory` | app (0) | `0x00` factory | `0x010000` | `0xF00000` | **15 360 K** |

~960 K of the 16 MB device is left unallocated above the app. **No OTA slot, no `otadata`, no
SPIFFS/FAT partition, no coredump partition.** `M5PaperMono-UserDemo/partitions.csv` and
`M5PaperMono-OTP-Demo/partitions.csv` are the same three lines, and the shipped binary's table
matches them exactly — so the published source and the shipped bytes agree about the flash map
even though they disagree about the application (§6).

### 4.2 The community CrossPoint layout

| Name | Type | SubType | Offset | Size | |
|---|---|---|---:|---:|---|
| `nvs` | data (1) | `0x02` nvs | `0x009000` | `0x005000` | 20 K |
| `app0` | app (0) | `0x00` factory | `0x010000` | `0x640000` | 6 400 K |
| `cjkfont` | data (1) | `0x40` *(custom)* | `0x650000` | `0x400000` | 4 096 K |
| `spiffs` | data (1) | `0x82` spiffs | `0xC90000` | `0x360000` | 3 456 K |
| `coredump` | data (1) | `0x03` coredump | `0xFF0000` | `0x010000` | 64 K |

Note `app0` carries subtype `0x00` — it is a **factory** app under an OTA-style name, and there
is no `otadata`, so this image has no OTA path either despite the naming.

**These offsets are not arbitrary.** `app0` at `0x10000` sized `0x640000`, the next partition
starting at `0x650000`, `spiffs` at `0xC90000` and `coredump` at `0xFF0000` are exactly the
arrangement of arduino-esp32's stock `default_16MB.csv`, with the **`app1` OTA slot repurposed
as the 4 MB `cjkfont` partition** and `otadata` dropped. Combined with the PlatformIO build
paths in §3.3, the reading is that CrossPoint started from the Arduino default 16 MB scheme and
edited it. **`inferred` from offsets and sizes — no copy of `default_16MB.csv` was retrieved in
this pass to diff against.**

### 4.3 The layout the vendor's own build block would give you

The published PlatformIO block sets `board_build.partitions = default_16MB.csv` — that same
Arduino default scheme, which is **not** the three-entry layout the product actually ships. So
the vendor's build instructions and the vendor's product disagree about the flash map.

Practical consequences, in order of how much they will cost you:

- **Building from the vendor's PlatformIO block does not reproduce the shipped geometry.** You
  get a smaller app slot, an unused second app slot and a SPIFFS partition the product does not
  have.
- **Writing one whole-flash image over another leaves debris.** Flashing CrossPoint over the
  official image and back again does not clear regions the new table does not describe;
  `nvs` in particular starts at the same offset in all three layouts but is 24 K in one and
  20 K in another.
- **If you intend to ship, pick the map first.** With no OTA slot, changing it later means
  physically reflashing every unit — see
  [`development.md` §8.4](development.md#84-there-is-no-ota-partition).

## 5. What the device does on power-up

Reconstructed from the string ordering in the official image and from the HAL source (S41).
**`inferred` throughout — no boot has been observed.**

1. **Second-stage bootloader** at `0x0` validates and loads the app at `0x10000`.
2. **PSRAM is found and memory-tested** — `Found %luMB PSRAM device`, `Speed: %dMHz`,
   `SPI SRAM memory test OK`, then pools are added to the heap allocator. If the build lacks
   octal PSRAM support the display later refuses to initialise
   ([`development.md` §8.1](development.md#81-octal-psram-is-mandatory--and-the-failure-looks-like-dead-hardware)).
3. **`M5.begin()`** runs — `M5.begin start` … `M5.begin done board=%d display_count=%d`. Board
   autodetection prints `[Autodetect] board_M5PaperMono`. Display init failure is reported
   distinctly as `count=0` versus a wrong size.
4. **Peripheral bring-up, with retries** — `Board peripheral init attempt %u/%u`, initialising
   M5PM1 and M5IOE1 (each with its own failure log), the IMU (`IMU init attempt %u/%u`), and the
   buzzer. A combined failure degrades gracefully:
   `M5PM1/M5IOE1 init failed; RGB/NFC/TF controls are disabled`.
5. **SKU detection** — the NFC rail is powered through M5IOE1 `PYG4` and the ST25R3916's
   identity register is read (`NFC identity probe: ok=… identity=… type=… rev=…`, expecting
   `ic_type 0x05`). Failure at either step means `Lite`. The result is logged as
   `Board variant detected: %s`, with values `Pro` / `Lite` in the source — note the firmware
   calls the C153 **"Pro"** although the product is just "PaperMono".
6. **The application launcher** runs the thirteen-plus demo apps listed in §2.3.
7. **Sleep and shutdown** are guarded: before entering M5PM1 shutdown the firmware verifies the
   selected wake line is idle and **cancels the shutdown if it is not**, then arms either
   `PM1 G4` (IMU, falling) or `PM1 G0` (RTC timer, falling). ESP32-S3 deep sleep uses touch
   `EXT0` on GPIO4 instead.

The load-bearing observation here is step 4: **this firmware is written to survive its own
auxiliary microcontrollers failing.** That is not defensive boilerplate — the M5PM1 and M5IOE1
sit between the application processor and most of the board, so a bus problem at boot has to
degrade rather than hang. It is also an indirect confirmation of how much of the board is behind
those two chips.

## 6. Why `c78f6c5-dirty` means not reproducible

`esp_app_desc_t.app_version` is populated by ESP-IDF from `git describe` at build time. The
`-dirty` suffix is `git describe`'s own marker for **"the working tree contained uncommitted
modifications when this was built"**.

So the official image was built from `c78f6c5` **plus an unknown set of uncommitted edits**.
The consequences are exact:

- **No commit of `m5stack/M5PaperMono-UserDemo` will regenerate these bytes.** The published
  HEAD is `c1099107271d31a0678d661a896e2b04dbb331ea` (2026-08-10, "update firmware v1.2") —
  four days *after* the image's build date of 2026-08-06, and a different object from `c78f6c5`
  in any case.
- **The delta is not published and cannot be recovered.** `git describe` records that
  modifications existed, never what they were.
- **Byte-for-byte reproduction is impossible even with the right tree**, because ESP-IDF stamps
  the build time into the image; but that is the *lesser* problem. The substantive problem is
  that the source state itself is unknown.
- **Therefore the bytes are the artifact.** This is precisely the case
  [`SIZE-AUDIT.md`](../../../SIZE-AUDIT.md) describes as irreplaceable: the image is retained in
  the repository rather than referenced by URL, because a URL to a CDN object is not a
  recovery plan for something no source tree can rebuild.

**A short digression worth having, because it is a general trap.** `-dirty` here is *not*
evidence of sloppiness that invalidates the firmware — vendors ship builds from working trees
routinely and the binary is perfectly valid. What it invalidates is the *audit chain*: you
cannot diff this image against source, cannot confirm the published repository is what runs on
the device, and cannot rebuild it to add a fix. If you need a reproducible baseline for this
board, build from the published HEAD and accept that you are building **something adjacent to**
the shipped firmware, not the shipped firmware.

By contrast, the community image's `paper-mono-v2-15-g87a191f` carries no `-dirty` marker and
names a commit. Whether that commit is reachable in the public repository was **not checked**
in this pass.

## 7. Flashing and recovery — authoritative versus inferred

### 7.1 Authoritative — what M5Stack actually documents

> Use **M5Burner** (or the Windows **EasyLoader** executable `C153-PaperMono-UserDemo_0x00.exe`,
> S40), select the *PaperMono UserDemo* firmware, put the device in download mode by
> **holding the power button about 2 seconds until the red LED blinks**, then release and flash.

`reported-working` — transcribed from S01, S04 and S09. **Not executed.** The Arduino
quick-start page (S07) contradicts the download-mode instruction by referring to "the reset
button on the side"; there is no reset button on this board, and that page is wrong
([R4](gaps-and-conflicts.md#r4--download-mode-control--resolved-on-the-balance-of-evidence)).

M5Burner's own device filter lists both images under `deviceName: "Paper"`, the family key
shared with the rest of M5Stack's Paper line, so **the catalogue will not stop you selecting an
image meant for a different Paper product.** `inferred` from the API records; `not-tested`.

### 7.2 Inferred — the `esptool` equivalent

**Never executed, on any board.** Written down because the method requires recovery
instructions to exist rather than be silently omitted, and because the vendor route is
Windows-GUI-shaped.

```bash
# INFERRED. NOT VERIFIED. Confirm the port and chip before running anything like this.
esptool.py --chip esp32s3 --port /dev/ttyACM0 --baud 921600 \
  write_flash --flash_mode dio --flash_freq 80m --flash_size 16MB \
  0x0 C153-PaperMono-UserDemo-v1.2.bin
```

Where each argument comes from:

| Argument | Evidence |
|---|---|
| `--chip esp32s3` | `chip_id 9` in both image headers |
| `0x0` | Bootloader header **is** at offset 0 in the file; the vendor's own object name ends `_0x00.bin` |
| `--flash_mode dio`, `--flash_freq 80m`, `--flash_size 16MB` | The image's own header fields — self-consistent by construction |
| `/dev/ttyACM0` | A guess. Native USB CDC enumerates as ACM on Linux; **the device was never enumerated here** |
| `--baud 921600` | A conventional value. **Not documented by the vendor for this board** |

### 7.3 Verifying what is on a board

`inferred`; not run:

```bash
esptool.py --chip esp32s3 --port PORT read_flash 0x10020 256 desc.bin   # esp_app_desc_t
esptool.py --chip esp32s3 --port PORT read_flash 0x8000 0xC00 ptab.bin  # partition table
```

Parsing either with [`commands.md` §5](commands.md#5-firmware-image-inspection)'s tooling
identifies the running application and its flash map. Both offsets are established from the
parses above.

### 7.4 What a reflash does not fix

**The M5PM1 runs its own firmware in its own part** (a `PY32L020F15U6`) and nothing you write
into the ESP32-S3's flash touches it. It owns `SOC_RESET` and the GPIO0 boot strap. If the
power manager is misconfigured — for example with its download mode locked through
`BTN_CFG_1[7] DL_LOCK` — reflashing the application processor is not the recovery path, because
you cannot get the application processor into download mode in the first place. See
[`development.md` §8.3](development.md#83-the-m5pm1-owns-reset-and-the-boot-strap--this-is-the-real-bricking-vector).

## 8. Provenance, distribution and licensing

| | Official image | Community image |
|---|---|---|
| Retrieved | 2026-09-01T05:05:22Z | 2026-09-01T05:05:25Z |
| API URL | `burner.m5stack.com/api/v1/firmwares/2089640807996628993/versions/2089640808000823298/download` | `…/2091144466157694978/versions/2091144466157694979/download` |
| CDN URL (after 302) | `m5burner-cdn.m5stack.com/community/1/2089640807996628993/2089640808000823298/bin/2089640808000823299.bin` | `m5burner-cdn.m5stack.com/community/3966/2091144466157694978/2091144466157694979/bin/2091144466157694980.bin` |
| HTTP status / content type | 200, `application/macbinary` | 200, `application/macbinary` |
| Validation | first byte `0xE9` — **ESP32 image**, not an HTML error page | same |
| Licence | **unknown** — no notice in the image or the API record | **unknown** — the upstream project is open source; the *binary* carries no notice |
| Redistribution | `unknown` | `unknown` |
| Disposition | `repository` | `repository` |
| Reacquisition | `automatic` (two URLs recorded) | `automatic` (two URLs recorded) |

`application/macbinary` is the CDN's content type for an opaque blob and means nothing about the
file; this is exactly the case where validating by **content** rather than by extension or
content-type matters, and both files were validated by magic byte before being named.

> **A numbering inconsistency to be aware of.** [`acquisition/manifest.json`](acquisition/manifest.json)
> refers to these two images as **`S30`** and **`S31`**, whereas [`sources.md`](sources.md) —
> which is the current, canonical source table — calls them **`S38`** and **`S39`**. The
> manifest predates the source table's renumbering. **This page uses the `sources.md` IDs.**
> The hashes, byte sizes and URLs agree in both files, so nothing is ambiguous about *which*
> artifact is meant.

## 9. Open questions

| # | Question | Why it is open |
|---|---|---|
| 1 | **`8300e309` versus `c78f6c5-dirty`** | The M5Burner `binFileName` and the in-image `esp_app_desc_t` carry different build identifiers for the same bytes. Neither is a commit in `M5PaperMono-UserDemo`'s published history that was checked. Possibly a CI build id, possibly a commit in an internal GitLab (both demo repos have squashed histories whose HEAD message is literally `Merge GitLab initial history`) |
| 2 | **Is `87a191f` reachable publicly?** | The community image names a commit; whether it exists in `MarsTechHAN/crosspoint-reader-mono` was not checked |
| 3 | **Does the M5Burner record's `nvs` survive a reflash?** | Depends on tool and offsets; not tested |
| 4 | **What is in the ~960 K unallocated tail** of the official layout? | Nothing in the partition table describes it; the region was not dumped |
| 5 | **Is there an M5PM1 firmware image anywhere?** | None was located. The power manager's firmware is not distributed through M5Burner and no update artifact for it was found |
| 6 | **The EasyLoader executable was not retrieved** | A Windows binary was out of scope. The *finding* is that both product pages link the same file from PaperMono's asset folder (S40) |

## Related

- [`development.md`](development.md) — frameworks, versions, build/flash/monitor, bricking risks
- [`features/usb-and-serial.md`](features/usb-and-serial.md) — ports, download mode, flashing routes
- [`resources-and-conflicts.md` §5](resources-and-conflicts.md#5-memory-flash-and-partitions) — flash and partition resources
- [`commands.md` §4](commands.md#4-m5burner-firmware-retrieval) and [§5](commands.md#5-firmware-image-inspection) — how these files were retrieved and parsed
- [`acquisition/manifest.json`](acquisition/manifest.json) · [`acquisition/README.md`](acquisition/README.md) — machine-readable provenance
- [`sources.md`](sources.md) — S31–S40 (M5Burner), S41–S42 (vendor source)
- [`community.md`](community.md) — who built the community image, and what that establishes
