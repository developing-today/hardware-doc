# Xteink X4 — factory firmware

> **A complete 16 MB factory flash dump was obtained and analysed.** It is the
> only Xteink factory image this session acquired. Retrieved **2026-09-04**.

## The artifact

| Field | Value |
|---|---|
| File | `artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin` (archived; symlink + placeholder in place) |
| Size | **16,777,216 B** exactly |
| SHA-256 | `b9cf27cc254c737c901f81e7fcf0c48308e29bd979848ab0ac0bf6c6f5e8c245` |
| Source | [`abhishek-nerella/XTEINK-OEM-BIN-`](https://github.com/abhishek-nerella/XTEINK-OEM-BIN-) `flash.bin`, branch `main` |
| Retrieved | 2026-09-04 |
| Licence | **None declared.** Vendor firmware re-uploaded by a third party. Redistribution **unknown, probably prohibited**. Disposition: archived, **unstaged** |
| Provenance of the dump itself | **Unknown.** The upstream README is 55 bytes and does not say which unit or which stock version |

Recovery instructions and alternate URLs:
[`artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin.ARCHIVED.md`](artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin.ARCHIVED.md).

## Partition table — parsed from offset `0x8000`

| Label | Type | Subtype | Offset | Size |
|---|---|---|---:|---:|
| `nvs` | data (0x01) | nvs (0x02) | `0x009000` | `0x005000` — 20 KiB |
| `otadata` | data (0x01) | ota (0x00) | `0x00E000` | `0x002000` — 8 KiB |
| `app0` | app (0x00) | ota_0 (0x10) | `0x010000` | `0x640000` — **6400 KiB** |
| `app1` | app (0x00) | ota_1 (0x11) | `0x650000` | `0x640000` — **6400 KiB** |
| `spiffs` | data (0x01) | spiffs (0x82) | `0xC90000` | `0x360000` — **3456 KiB** |
| `coredump` | data (0x01) | coredump (0x03) | `0xFF0000` | `0x010000` — 64 KiB |

`executed-success` — parsed by this session directly from the image.

**This differs from the X4 Pro's layout** (`0x7E0000` app slots, `0x14000` spiffs).
The X4 devotes **3.4 MB to SPIFFS**, ten times the Pro's, which is consistent with
the stock firmware serving a web file-manager UI from flash.

## Boot state of this particular dump

| Field | Value |
|---|---|
| Image magic @ `0x0` | `0xE9` ✓ |
| Bootloader chip-id | **5 = ESP32-C3** — independent confirmation of the SoC |
| `otadata` seq | slot 0 = 1, slot 1 = 0 → **boots app0** |
| `app1` | **erased (all `0xFF`)** — this unit had never taken an OTA |

## The app descriptor — and why it does not give you a version

`esp_app_desc_t` at `app0 + 0x20` (magic `0xABCD5432`):

| Field | Value |
|---|---|
| `project_name` | **`arduino-lib-builder`** |
| `version` | `esp-idf: v4.4.7 38eeba213a` |
| `idf_ver` | `v4.4.7-dirty` |
| build date/time | **2024-03-05 12:29:20** |
| `elf_sha256` | `8b41832ff60a0ffa1cfb9f810a569a3b6237c34bc4ce81e5d280069f8f76d438` |
| `secure_version` | 0 |

**Finding: the stock X4 firmware is an Arduino-framework build, and its app
descriptor carries the Arduino `lib-builder` identity rather than a product
version.** The on-screen version numbers users see (V5.1.6, V5.2.13) are **not
recoverable from the descriptor**, and the 2024-03-05 date is the Arduino core's
build date, **not the firmware's**.

This matters for anyone identifying a dump: do not report `arduino-lib-builder /
2024-03-05` as "the firmware version". It is a toolchain fingerprint.

By contrast the **X4 Pro's** 7.4.4 image is a **native ESP-IDF 6.0.1** build whose
descriptor *does* self-identify as `xteink_app 7.4.4`. **Xteink changed framework
between the C3 and S3 generations.**

## Network endpoints recovered by string extraction

| String | Role |
|---|---|
| `http://gotaserver.xteink.com/api/check-update` | OTA update check — **plain HTTP** |
| `http://bofi.xteink.cn/index.html` | On-device web file manager |
| `http://bofi.xteink.cn/index.html?ip=` | same, with the device IP passed in |
| `XT-EPD` | Probable AP SSID or BLE name — **not confirmed** |
| `192.168.3.3` | An address literal, role unestablished |

`bofi.xteink.cn` is the **only evidence that the `.cn` domain is in service** —
the apex `xteink.cn` does not answer.

**Security observation, stated without alarm:** OTA is checked over **plain HTTP**
and `secure_version` is 0, so there is no anti-rollback. Whether the payload is
signed or encrypted was **not determined** — the X4 Pro's OTA container uses a
`.xota` extension and the SDK refers to *"the decrypted"* app, implying some
protection exists at the package level.

## Known stock firmware versions

From [`zocs/eink-quick-flasher/firmware/README.md`](https://github.com/zocs/eink-quick-flasher/blob/main/firmware/README.md),
retrieved 2026-09-04:

| File | Device | Language | Version | Type |
|---|---|---|---|---|
| `x4_en_v5.1.6_ota.bin` | X4 | EN | **V5.1.6** | OTA, ~6 MB |
| `x4_cn_v5.2.13_ota.bin` | X4 | CN | **V5.2.13** | OTA, ~6 MB |
| `x3_en_v1.0.7_full.bin` | X3 | EN | V1.0.7 | full 16 MB |
| `x3_en_v5.2.13_full.bin` | X3 | EN | V5.2.13 | full 16 MB |
| `x3_cn_v5.2.13_full.bin` | X3 | CN | V5.2.13 | full 16 MB |
| `x3_cn_v5.2.13_ota.bin` | X3 | CN | V5.2.13 | OTA |

**Useful fact from that README:** *"CN/EN designation only indicates the default
UI language. Firmware content is identical; language can be switched in settings
after flashing."* So there is **no CN/EN hardware or firmware split** — only a
default setting.

**Not downloaded.** Those files are **Git LFS pointers** (~130 bytes each in the
tree); fetching the real blobs requires an LFS-aware client. Recorded as a gap.

## How to dump

```bash
# reported-working (zocs/eink-quick-flasher does this; ~2 minutes for 16 MB)
esptool.py --chip esp32c3 --port /dev/ttyUSB0 --baud 921600 \
           read_flash 0 0x1000000 x4-stock-full.bin
sha256sum x4-stock-full.bin
```
Requires a **USB-unlocked** unit. See [`development.md`](development.md).

## How to restore

```bash
# reported-working
esptool.py --chip esp32c3 --port /dev/ttyUSB0 --baud 921600 \
           write_flash 0 x4-stock-full.bin
```

Community tooling, in order of usefulness:

| Tool | What |
|---|---|
| [`zocs/eink-quick-flasher`](https://github.com/zocs/eink-quick-flasher) | GUI, auto COM detection, **1:1 full-flash backup & restore in ~2 min**, and ships stock images. Includes an `X3-FLASHER-GUIDE` in EN and CN |
| [`bigbag/papyrix-flasher`](https://github.com/bigbag/papyrix-flasher) | Go CLI, auto-detection, embedded bootloader, MD5 verification |
| `crosspointreader.com` | Web flasher including "flash back to stock" |
| [`togotago/xteink-x4-escape`](https://github.com/togotago/xteink-x4-escape) | *"Escape recipe for Xteink X4 e-readers stuck on CrossPoint Reader 1.2.0 with OTA failing at `esp_ota_end()`"* — a named, documented brick and its cure |

## Parsing recipe (reusable)

```python
# executed-success 2026-09-04
d = open('flash.bin','rb').read()
pt = d[0x8000:0x9000]                       # partition table
for i in range(0, 0x1000, 32):
    e = pt[i:i+32]
    if e[:2] != b'\xAA\x50': break
    off, size = struct.unpack('<II', e[4:12])
    label = e[12:28].rstrip(b'\x00').decode()

p = APP_OFFSET + 0x20                       # esp_app_desc_t, magic 0xABCD5432
version = d[p+16 :p+48 ].rstrip(b'\0')
project = d[p+48 :p+80 ].rstrip(b'\0')
date    = d[p+96 :p+112].rstrip(b'\0')
idf     = d[p+112:p+144].rstrip(b'\0')
```

## Related

[`development.md`](development.md) · [`../x4-pro/factory-firmware.md`](../x4-pro/factory-firmware.md)
