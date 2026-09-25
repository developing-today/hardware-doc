# Xteink X3 stock firmware — image teardown

> Parsed from `x3_cn_v5.2.13_ota.bin` — the **CN V5.2.13 OTA image**, 6,254,064 bytes,
> SHA-256 `0b2cbc4a6414aef4ad6e676b59fdefa3b529189758953765b26df02bac77bcb6`.
>
> **All findings below are `executed-success`**, obtained on **2026-09-20** by running
> [`tools/esp_image_info.py`](../../../../../tools/esp_image_info.py) and a string/segment
> extraction over these exact bytes. Nothing here is inferred from another device unless the
> text says so.
>
> The image itself is archived — see
> [`x3_cn_v5.2.13_ota.bin.ARCHIVED.md`](x3_cn_v5.2.13_ota.bin.ARCHIVED.md).

## Why this document exists

The X3 record previously said *"No X3 flash dump was obtained by this session"* and treated the
stock images as an open gap. The image **had** been fetched on 2026-09-11, parsed for its header
only, and then left in a scratch directory while the record continued to describe it as
unobtained. This is the full extraction that should have followed.

**This is an OTA image: the application partition only.** It contains no bootloader, no partition
table and no filesystem image. Anything below about flash layout is what the *application* says
about its own environment, not a map read off a flash dump.

## Image header

| Field | Value |
|---|---|
| Magic | `0xE9` — valid ESP application image |
| **`chip_id`** | **`5` = ESP32-C3** |
| Segment count | 6 |
| Entry point | `0x40381E52` (ESP32-C3 IRAM) |
| Flash mode | **DIO** |
| Flash size in header | **16 MB** |
| Flash frequency | **80 MHz** |

### Segment map

| # | Load address | Region | Length |
|---:|---|---|---:|
| 0 | `0x3C170020` | DROM (constant data, XIP from flash) | 4,670,256 |
| 1 | `0x3FC92000` | DRAM (initialised data) | 16,492 |
| 2 | `0x40380000` | IRAM (vectors / RAM-resident code) | 31,820 |
| 3 | `0x42000020` | IROM (application code, XIP from flash) | 1,493,492 |
| 4 | `0x40387C4C` | IRAM (more RAM-resident code) | 41,828 |
| 5 | `0x50000000` | RTC fast memory | 68 |

Every load address falls inside the **ESP32-C3** memory map, independently corroborating
`chip_id`. Note the shape: **4.67 MB of DROM against 1.49 MB of code** — roughly three quarters
of the image is constant data, overwhelmingly fonts and UI bitmaps rather than program logic.

### `esp_app_desc_t`

| Field | Value |
|---|---|
| `project_name` | **`arduino-lib-builder`** |
| `version` | `esp-idf: v4.4.7 38eeba213a` |
| `idf_ver` | **`v4.4.7-dirty`** |
| Build date/time | `Mar  5 2024 12:29:20` |
| ELF SHA-256 | `a2cb05b71d4552c10daf8fedfef5ffd0799a31826aef80dccd7ba51ce93df726` |

⚠ **Do not read that build date as the firmware's build date.** When a sketch is compiled against
the Arduino-ESP32 2.x core, the `esp_app_desc_t` is inherited from the precompiled
`esp32-arduino-libs` bundle, so `project_name` becomes `arduino-lib-builder` and the timestamp is
the *core's* build date. `Mar 5 2024` is when Espressif built the Arduino core, not when Xteink
built XTOS V5.2.13. **The image carries no trustworthy build timestamp of its own** — this is a
limitation of the artifact, recorded so nobody re-derives it. **inferred**, from the well-known
arduino-lib-builder descriptor behaviour plus the PlatformIO evidence below.

## The real toolchain — from an embedded source path

```
0x0410eec  /C:/Users/32651/.platformio/packages/framework-arduinoespressif32/
           libraries/WebServer/src/detail/RequestHandler.h
```

An `__FILE__` string that survived into the binary. It establishes, directly:

- the firmware is built with **PlatformIO**, not the Arduino IDE and not bare ESP-IDF;
- using **`framework-arduinoespressif32`** — the Arduino core as a PlatformIO package;
- on **Windows**, under the user profile `32651`;
- and it uses the Arduino **`WebServer`** library, which is the on-device HTTP server catalogued
  below.

Other embedded paths give the BLE stack precisely:

```
0x041d3e8  /lib/NimBLE-Arduino-2.3.6/src/nimble/esp_port/esp-hci/src/esp_nimble_hci.c
```

**NimBLE-Arduino 2.3.6**, vendored under `lib/` — a PlatformIO `lib_deps` layout. NimBLE rather
than Bluedroid is a deliberate choice: it is far smaller, which matters on a C3 with no PSRAM.

## Version and product identity

| String | Offset | Meaning |
|---|---|---|
| **`XTOS V5.2.13`** | `0x00038c4` | **The vendor's name for its own firmware is `XTOS`.** Not previously recorded anywhere in this tree |
| `V5.2.13` | `0x0002068` | the version alone, as displayed |
| **`ESP32C3_X3`** | `0x0002b44` | the device-type string sent to the backend — the firmware names both its SoC and its model |
| `xteink_ble`, `XTEPD_BLE_` | `0x000391c`, `0x0003994` | BLE advertised-name prefixes |
| `XTEINK App Connection`, `XTEINK` | `0x0419480` | BLE service / UI label |

`ESP32C3_X3` is the strongest single confirmation of the X3's SoC in this repository: it is the
device's own self-description, in a field it transmits to its vendor.

## Network behaviour

**The device talks to four distinct hosts.** All plain **HTTP**, no TLS — worth knowing before
putting one on a network you care about.

| Endpoint | Offset | Role |
|---|---|---|
| `http://api-prod.xteink.cn/api/v1/` | `0x00025b4` | the production vendor API |
| `http://8.130.157.48:5000/api/v1/sync/check` | `0x000251c` | **a hardcoded bare IP**, port 5000 — sync check. An Alibaba Cloud address range |
| `http://bofi.xteink.cn/index.html?ip=` | `0x0003d50` | a companion web page, handed the device's own IP as a query parameter |
| `https://active.clewm.net/DJsQXv` | `0x00020fc` | 草料二维码 (cli.im) QR-code shortener — the activation/pairing QR |

Query parameters seen alongside: `device_id`, `&device_id=`, `?device_id=`,
`tasks?limit=4&device_id=`, and a JSON body `{"device_id":"…`. So the device identifies itself by
a `device_id` to the vendor backend and polls a task queue.

⚠ This corroborates, on the X3, the `bofi.xteink.cn` reference that an earlier pass found inside
the **X4** stock firmware — the two devices share backend infrastructure as well as a codebase.

### NTP

```
0x040a938  ntp1.aliyun.com
0x040a948  ntp.ntsc.ac.cn
0x040a958  ntp2.aliyun.com
0x040a968  time1.apple.com
0x040a978  time1.google.com
```

A China-first list (`ntsc.ac.cn` is the National Time Service Centre) with Apple and Google as
fallbacks. An X3 with no route to Chinese hosts will still get time, slowly.

## The on-device HTTP server

The firmware runs an Arduino `WebServer` and serves a configuration UI. The Wi-Fi AP is
advertised as **`[E-Paper]`** — from the on-screen help text:

```
0x04135a4  1.Connect your phone to the [E-Paper] Wi-Fi
0x0414804  1.Press Left/Right to navigate to [Upgrade/Transfer]
0x041499c  3.After network setup, select [System Upgrade]
```

and the page itself is titled `E-Paper Web Server` (`0x0003b2c`), `<title>epd</title>`.

### Route table

Recovered as literal route strings. **`not-tested`** — none of these was exercised against
hardware; they are what the binary registers, and parameter names are not established.

| Route | Apparent purpose |
|---|---|
| `/status`, `/statusFast` | device status |
| `/Read_info` | device information |
| `/list`, `/fileOpen`, `/folderMove`, `/edit` | file manager |
| `/Read_fileSync` | file synchronisation |
| `/Wifi`, `/Read_scanWifi`, `/Read_scanWifiHistory`, `/Read_staNameIp` | Wi-Fi setup |
| `/restartAPMode` | drop back to soft-AP |
| `/setWallpaper`, `/setFont` | appearance |
| `/systemSet`, `/setRunMode` | system configuration |
| `/webRead_language` | UI language |
| `/webPut_longPress`, `/webRead_longPress` | long-press key binding |
| `/Put_sdInit`, `/Read_sdInit`, `/Put_sdFrequency`, `/Read_sdFrequency` | **SD card init and bus frequency, both settable over HTTP** |
| `/Read_updataAddress` | OTA update URL (vendor's spelling) |
| `/update.bin`, `/complete` | OTA upload endpoint and completion |

`/Put_sdFrequency` is notable: the SD clock rate is a user-exposed setting over the web UI,
which suggests the vendor hit card-compatibility problems in the field.

Static assets served from the filesystem:

```
/system/manager.htm.gz   /system/ace.js.gz        /system/jquery.js.gz
/system/bootstrap.css.gz /system/bootstrapBundle.js.gz
/system/toast.css.gz     /system/toast.js.gz      /system/favicon.ico.gz
/system/iconfont.ttf     /system/GCSBS.html.gz
/system/lan/index.js  /system/lan/EN.js  /system/lan/JA.js  /system/lan/ZH-CN.js
```

**A Japanese language pack ships in the stock image** (`JA.js`) alongside English and
Simplified Chinese. Three UI languages, not two. The vendor's own release note — that CN/EN
naming reflects only the *default* setting and the binaries are identical — is consistent with
this: language is data, not a build.

## Filesystem — LittleFS, not SPIFFS

```
0x0001db8  /littlefs
0x0002fc0  LittleFS
0x04145d8  LittleFS startup failed
```

⚠ **This corrects an inference in [`../../factory-firmware.md`](../../factory-firmware.md).** That
file reproduces the X4's partition table as a "reference" for the X3 and labels its data partition
`spiffs`. The X3 application mounts **LittleFS**. The partition *subtype byte* may well still be
the `spiffs` value `0x82` — that is a common and harmless mismatch, since the subtype is just a
label — but **the on-flash format is LittleFS**, and anything that tries to read the data
partition as SPIFFS will fail. `SPIFFS` appears only once (`0x0001db0 spiffs`), consistent with a
partition label rather than a mounted filesystem.

Still **not established** for the X3: the actual partition offsets and sizes. An OTA image cannot
show them. Getting them needs one of the three 16 MB full-flash images, which remain unfetched.

### On-device directory layout

| Path | Contents |
|---|---|
| `/XTCache/` | the device's working cache |
| `/XTCache/epub`, `/XTCache/xtc/` | book cache |
| `/XTCache/readTime/`, `/XTCache/readStatistics.txt`, `/progress.txt` | reading statistics |
| `/XTCache/bookmark/`, `/bookmark.txt` | bookmarks |
| `/XTCache/stock_sj.json` | **stock-ticker data** |
| `/XTCache/weather_sj.json` | **weather data** |
| `/XTCache/picDir.txt`, `/XTCache/fontPos.txt` | image index, font metrics |
| `/system/` | web UI assets, language packs, `clockFont.ttf` |
| `/system/BLE.txt`, `/BLE Protocol.txt` | **an on-device copy of the BLE protocol description** |
| `/system/txtReturn.txt`, `/system/epubReturn.txt` | per-format resume state |
| `/config.json`, `/id.txt`, `/language.txt`, `/push.txt` | configuration |

### Xteink file formats

| Extension | Role |
|---|---|
| **`.xtc`** (and `.xtc.tmp`) | the cached/processed book format |
| **`.xtg`** | cover image (`/cover.xtg`, `cover.xtg`) |
| **`.xth`** | chapter structure — `00_summary.xth` |

Covers are also accepted as `cover.jpg` / `cover.bmp` / `cover.png`. Fonts as `.ttf` / `.otf`.
None of these three container formats is documented anywhere public that this pass found; they
are named here so a future reader knows what to look for on an SD card.

## Features the strings reveal

Beyond reading, the CJK strings show the firmware ships:

- **a stock ticker** — `成交额` (turnover), `流通股本` (tradable shares), `成交量` (volume),
  backed by `/XTCache/stock_sj.json`;
- **a weather display** — `/XTCache/weather_sj.json`;
- **a factory burn-in mode** — `老化测试` ("aging test"), alongside SD benchmark strings
  `写入速度` / `读取速度` (write/read speed), `卡挂载成功` / `卡挂载失败` (card mount
  succeeded/failed) and error counters. A built-in SD diagnostic, reachable presumably through
  the `/Put_sdInit` route;
- **`恢复出厂设置`** — factory reset;
- Li Bai's *早发白帝城* (`朝辞白帝彩云间…`) embedded as demo/sample text.

## OTA behaviour

`ESP32-http-Update` (`0x041cdb4`) — the Arduino `HTTPUpdate` library, not `esp_https_ota`. With
`/Read_updataAddress` exposing the update URL and every backend being plain HTTP, **the stock
update path is unauthenticated HTTP**. User-visible strings confirm the flow:
`Check updates...`, `System Update Successful`, `System Not Updated`, `Update completed`,
`If stuck during update:`, `Insufficient space to start OTA`,
`Could Not Activate The Firmware`, `Partition Could Not be Found`,
`Update.bin is not a file`, `Unable to load update.bin`.

`esp_ota_*` symbols are present, so the standard two-slot OTA scheme is in use — consistent with
the X4's `app0`/`app1`/`otadata` layout.

## Side-by-side with the X4 full-flash dump

Re-parsed on 2026-09-20 with [`tools/appdesc.py`](../../../../../tools/appdesc.py), which unlike
`tools/esp_image_info.py` scans a **merged** image for the `0xABCD5432` descriptor rather than
looking only at offset `0x20`. On the X4's 16 MB dump, `esp_image_info.py` reports
*"no app descriptor; magic 0xffffffff"* — correct, because at offset `0` a merged image holds the
**bootloader** (3 segments, entry `0x403CC710`), not the app.

| | X3 CN OTA V5.2.13 | X4 OEM full flash |
|---|---|---|
| `project_name` | `arduino-lib-builder` | `arduino-lib-builder` |
| descriptor version | `esp-idf: v4.4.7 38eeba213a` | `esp-idf: v4.4.7 38eeba213a` |
| `idf_ver` | `v4.4.7-dirty` | `v4.4.7-dirty` |
| build date/time | `Mar  5 2024 12:29:20` | `Mar  5 2024 12:29:20` |
| chip | ESP32-C3 | ESP32-C3 |

**Every descriptor field is identical between two different devices' firmware.** Two things
follow:

1. It is **direct confirmation** that the build date is the Arduino core's, not the
   application's — two independently-built applications cannot share a build timestamp to the
   second. This settles the caveat raised above from inference to demonstration.
2. It is **corroboration, not proof, of the shared-codebase reading.** Identical descriptors
   show only a shared *core*; any two sketches built against the same arduino-esp32 release
   would look like this. The stronger evidence for one codebase remains the shared `V5.2.13`
   version number and the shared `bofi.xteink.cn` backend.

### The X4 partition table — existing documentation confirmed correct

`appdesc.py` decoded the table at `0x8000` of the X4 dump:

| Name | Type | SubType | Offset | Size |
|---|---|---|---|---|
| `nvs` | data | `0x02` nvs | `0x009000` | 20 K |
| `otadata` | data | `0x00` | `0x00E000` | 8 K |
| `app0` | app | `0x10` ota_0 | `0x010000` | 6400 K |
| `app1` | app | `0x11` ota_1 | `0x650000` | 6400 K |
| `spiffs` | data | `0x82` | `0xC90000` | 3456 K |
| `coredump` | data | `0x03` | `0xFF0000` | 64 K |

**This matches what [`../../factory-firmware.md`](../../factory-firmware.md) already recorded,
exactly.** Recorded as a confirmed-correct result rather than left silent.

One new detail: **only `app0` carries a descriptor.** `appdesc.py` scans the whole 16 MB and
finds a single app at `0x010020`; the `app1` slot at `0x650000` is empty in this dump. The
donor unit had never taken an OTA update, or had been fully re-flashed.

⚠ Note the X4 subtype `0x82` labelled `spiffs` — and see [Filesystem](#filesystem--littlefs-not-spiffs)
above for why that label does not mean the *format* is SPIFFS on the X3.

## What this changes in the existing records

| Record | Change |
|---|---|
| [`../../factory-firmware.md`](../../factory-firmware.md) | "No X3 flash dump was obtained" → an OTA image **was** obtained, retained and parsed. The `spiffs` inference is corrected to **LittleFS** |
| [`zocs-x3-stock-images.NOT-FETCHED.md`](zocs-x3-stock-images.NOT-FETCHED.md) | "fetched and parsed but not retained" was wrong; disposition changes from `reference-only` to `archive` for this one image. The other three remain genuinely unfetched |
| [`../../features/nfc.md`](../../features/nfc.md) | **no NFC-related string was found in this image**, which is consistent with, and mildly supports, the existing finding that the X3's tag is a passive user-writable tag independent of firmware. **Negative result, recorded deliberately** |
| [`../../README.md`](../../README.md) | `ESP32C3_X3` is a third independent confirmation of the SoC |

## What was looked for and *not* found

Recorded so it is not re-searched:

- **No display-controller part number.** No `UC8253`, `UC8279`, `SSD16xx` or similar string
  appears. The panel driver is compiled in without naming its part. The `UC8253`/`UC8279`
  attribution in the X3 record rests on the teardown photographs and the FreeInk profile, not on
  the firmware.
- **No RTC part number.** No `DS3231`, `DS1307`, `PCF85xx` or `RX8xxx` string. **The three-way
  X3 RTC conflict is not resolved by this image**, and cannot be — an Arduino RTC driver is
  header-only and leaves no marker. That conflict still needs the FCC internal photographs.
- **No fuel-gauge part number.** No `CW2015`/`CW2017`/`BQ27xxx` string.
- **No `hw_calib` / `screenType` NVS key.** The FreeInk SDK reads that namespace on the X4
  family; the X3 stock firmware does not appear to write it. Whether FreeInk's X3 support relies
  on it is **not established**.

## Reproducing

```bash
# from the repository root, with the archive present
python3 tools/esp_image_info.py \
  archive/devices/xteink/x3/artifacts/firmware/x3_cn_v5.2.13_ota.bin
```

For the segment map and strings, the ad-hoc extraction used is trivial to re-derive: read the
6-byte-per-segment headers from offset `0x18`, and `re.finditer(rb"[\x20-\x7e]{5,}", data)` for
ASCII plus `(?:[\xe4-\xe9][\x80-\xbf]{2}){3,}` for UTF-8 CJK runs.

## See also

- [`../../factory-firmware.md`](../../factory-firmware.md) — stock version table, known images
- [`x3_cn_v5.2.13_ota.bin.ARCHIVED.md`](x3_cn_v5.2.13_ota.bin.ARCHIVED.md) — placeholder and LFS recipe
- [`zocs-x3-stock-images.NOT-FETCHED.md`](zocs-x3-stock-images.NOT-FETCHED.md) — the other three images
- [`../../../x4/factory-firmware.md`](../../../x4/factory-firmware.md) — the X4 dump this can be compared against
- [`../../../firmware-ecosystem.md`](../../../firmware-ecosystem.md) — family-wide firmware map
