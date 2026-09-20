# Xteink X4 Classic — factory firmware

> Everything here is read from the FreeInk maintainers' analysis of a stock dump
> named **`flashx4c.bin`**, which **this session did not obtain**.
> Retrieved **2026-09-04**.

## Board identity strings

| String | Meaning |
|---|---|
| **`ESP32S3_X4_CLA`** | Board tag |
| **`ESP32S3_X4R2_CLA`** | Board **revision** string — note the `R2` |
| **`ESP32S3_X4_CLA_SSD1677`** | Default panel string |

`ESP32S3_X4R2_CLA` is the only revision identifier of any kind found for any
Xteink device. **Whether an R1 shipped is unknown** — it may be an internal
iteration that never left the factory, or the X4C may already be a second
revision. Recorded as an open question, not as evidence of two field revisions.

## Version

**`xteink_app` v7.0.11** (app0). For comparison, the X4 Pro's contemporaneous
firmware was **7.0.8** and later **7.4.4** — so the C-series and Pro share a
version stream, which is consistent with one codebase serving both S3 boards.

## Partition layout (16 MB, dual-OTA)

`nvs` `0x9000` · `otadata` `0xE000` · `app0` `0x10000` · `app1` `0x7F0000` ·
`spiffs` `0xFD0000` · `coredump` `0xFE4000`.

**Identical to the [X4 Pro](../x4-pro/factory-firmware.md)** and different from the
C3 [X4](../x4/factory-firmware.md), which uses 6400 KiB app slots and a 3456 KiB
SPIFFS.

## NVS `hw_calib/screenType` — the most important byte on this device

| Value | Controller |
|---:|---|
| 1 or `0x0B` | [UC8179](../../../components/ultrachip/uc8179/README.md) |
| 2 or `0x0C` | [UC8279](../../../components/ultrachip/uc8279/README.md) |
| 3, default, or unset | [SSD1677](../../../components/solomon-systech/ssd1677/README.md) |

Written **once by the factory**. Because the display bus has no MISO, this value
is not merely a hint — it is the **only** source of truth, and nothing corrects it
at boot.

**Operational consequence:** a full-flash backup/restore workflow that is safe on
every other Xteink is **not safe here**. If you restore an image captured from a
different unit, you import that unit's `hw_calib` and may drive the wrong
controller. Preferred order:

1. Take **your own** full-flash backup before anything else.
2. If you must use a foreign image, **preserve and re-write your own `nvs`
   partition** (`0x9000`, 20 KiB) afterwards.
3. Verify from the serial log, which prints
   `[XTDET] X4C: NVS screenType=<n> -> <driver> (no MISO, probe skipped)`.

## What stock does that the SDK does not

- **USB-MSC** — the SDK lists the X4C as USB-MSC capable, so unlike the X4 Pro this
  is not a gap.
- Frontlight code paths exist but report *"Frontlight hardware is disabled on this
  board"* — i.e. the vendor ships one firmware across variants and gates on the
  board tag. That also explains why the X4 Pro's dump contains a **vestigial ADC
  button-ladder matcher** for hardware it does not have.

## Dumping and restoring

```bash
# inferred — not executed; requires a USB-unlocked unit
esptool.py --chip esp32s3 --port /dev/ttyACM0 --baud 921600 \
           read_flash 0 0x1000000 x4c-stock-full.bin
sha256sum x4c-stock-full.bin
python3 tools/esp_image_info.py x4c-stock-full.bin
```

```bash
# inferred — see the NVS warning above before writing a foreign image
esptool.py --chip esp32s3 --port /dev/ttyACM0 --baud 921600 \
           write_flash 0 x4c-stock-full.bin
```

## Artifacts held

**None.**

| Wanted | Status | Reacquisition |
|---|---|---|
| `flashx4c.bin` | **Not located publicly.** Referenced only inside the FreeInk SDK's documentation; the maintainers hold it privately | `blocked` — no URL exists. Ask upstream, or dump a unit |
| Any X4C OTA package | Not located | `blocked` |
| Vendor OTA feed for this model | Not queried | `manual` — `gotaserver.xteink.com/api/check-update` |

For comparison, an **[X4 factory dump](../x4/artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin.ARCHIVED.md)**
*was* obtained and is archived in this repository. It is a **different device**
(ESP32-C3) and cannot be flashed here, but it documents the vendor's firmware
conventions — partition style, OTA endpoints, the Arduino-vs-IDF split.

---

## Round 2 — 2026-09-11

**No line above was altered.**

### The board tags are a shared enum, not a per-unit stamp

A **physical Xteink X4 Pro** was dumped twice on 2026-09-06 by a third party, both
dumps hashing identically
(`90734554798da8dbe1961bf876a7bf44f2ea66a572ae2ed9b7ed395c9a0143fe`). Its stock
`xteink_app` binary contains, in one image:

```
ESP32S3_X4_TL      ESP32S3_X4_TL_SSD1677      ESP32S3_X4_CLA      ESP32S3_X4R2_CLA
XTEink::SSD1677_800x480    UC8179_800x480    UC8279_800x480    ZHX_UC8279Base
GT911Driver    BM8563Driver    Cw2017PowerHal
```

Source:
[`kycube/x4pro-emu` `docs/device/partitions.md`](https://github.com/kycube/x4pro-emu/blob/bf4b86ae0471012d4d07c0bb3042f3f561c9c302/docs/device/partitions.md),
commit `bf4b86a`.

**Consequence for this record:** finding `ESP32S3_X4R2_CLA` inside a dump tells
you the vendor builds one firmware for both S3 boards. It does **not** tell you
the unit it came from is an "R2" of anything. See [`README.md`](README.md) §`R2`.

### Stock-firmware versions across the S3 family

| Version | Board | Built | Toolchain | Source |
|---|---|---|---|---|
| `xteink_app` **7.0.11** | **X4 Classic** | unknown | unknown | FreeInk's private `flashx4c.bin` — **the only X4C version ever named** |
| `xteink_app` **7.2.4** | X4 Pro (desk unit) | **2026-08-14 19:25:05** | **ESP-IDF v6.0.1** | third-party dump, 2026-09-06 |
| **7.4.4** / package `V7.4.5` | X4 Pro | — | — | conflict already recorded in `VERIFICATION-xteink.md` item 4 |
| **7.5.4** | X4 Pro | — | — | third-party analysis doc `docs/stock-7.5.4.md` |

**Four different version numbers now exist for the X4 Pro's stock firmware and
one for the X4 Classic.** They are not reconcilable from public evidence — the
vendor ships regional and OTA-staged builds, and no changelog is published.
**No X4 Classic shipping version is corroborated by anyone.**

### Partition layout, now with a hardware witness

The 16 MB dual-OTA layout recorded above matches, exactly, the table read off a
**physical X4 Pro**:

| Name | Type | Offset | Size |
|---|---|---|---|
| `nvs` | data/nvs | `0x009000` | `0x005000` |
| `otadata` | data/ota | `0x00E000` | `0x002000` |
| `app0` | app/ota_0 | `0x010000` | `0x7E0000` |
| `app1` | app/ota_1 | `0x7F0000` | `0x7E0000` |
| `spiffs` | data/spiffs | `0xFD0000` | `0x014000` |
| `coredump` | data/coredump | `0xFE4000` | `0x01C000` |

On that unit `otadata` held `seq=1 state=2 (VALID)`, selecting **`app0`**, and
`app1` was erased `0xFF`. **This is an X4 Pro, not an X4 Classic** — but it is
the first non-SDK confirmation of the layout anywhere in this family.

### NVS keys seen on the sibling board

`hw_calib` → `screenType` (**the panel identity**), `region` (1 = CN, 2 =
overseas), `lightDS`. `user_config` → Wi-Fi credentials, `lightBri`, `lightCT`,
`lightOn`, `timeZone`, `language`, `activate`, `cloud_bind_st`, `otaPromptDay`,
`pwrTimingVer`. Plus `xteink_sys`, `misc`, `nvs.net80211`, `phy`.

The X4 Classic has no frontlight, so `lightBri` / `lightCT` / `lightDS` are
expected to be absent or inert there — **not verified**.

### The recovery warning, restated with its new weight

The X4 Classic's panel bus has **no MISO**. `hw_calib/screenType` is the only
thing that tells firmware which of three controllers is fitted, and it is written
**at the factory**.

**A full-chip erase destroys it, and there is no documented way to recover it
except by trial.** On every sibling board a bus probe would repair the mistake
automatically. On this one it cannot. Preserve `nvs` at `0x9000` across any
reflash, and note that Draftling keeps an `otadata` partition specifically so the
stock and CrossPoint OTA updaters can reinstall — which matters far more here
than on a board with a USB socket, because **the X4 Classic has none**.
