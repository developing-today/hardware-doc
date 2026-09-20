# Xteink X4 — command ledger

Family-wide research commands are in [`../x4-pro/commands.md`](../x4-pro/commands.md).
This page holds X4-specific commands. Retrieved **2026-09-04**.

## Executed successfully by this session

| # | Command | Purpose | Status |
|---|---|---|---|
| 1 | `curl -sSL -H "Authorization: Bearer $(gh auth token)" "https://raw.githubusercontent.com/abhishek-nerella/XTEINK-OEM-BIN-/main/flash.bin" -o x4-oem-flash.bin` | Fetch the **16 MB factory dump**. HTTP 200, 16,777,216 B | `executed-success` |
| 2 | `sha256sum x4-oem-flash.bin` → `b9cf27cc254c737c901f81e7fcf0c48308e29bd979848ab0ac0bf6c6f5e8c245` | Hash before doing anything else | `executed-success` |
| 3 | Partition-table parse at `0x8000` (see below) | Recovered the full 6-partition layout | `executed-success` |
| 4 | `esp_app_desc_t` parse at `app0 + 0x20` | Recovered `arduino-lib-builder` / IDF v4.4.7 / 2024-03-05 / `elf_sha256` | `executed-success` |
| 5 | Printable-string extraction over `app0` | Recovered the OTA endpoint, the web file-manager URL and `XT-EPD` | `executed-success` |
| 6 | `python3 tools/archive_artifact.py --repo-root . --manifest …` | Archived the dump with a placeholder | `executed-success` |

### The parsing recipe, verbatim

```python
# executed-success 2026-09-04
import struct, re
d = open('x4-oem-flash.bin','rb').read()
assert len(d) == 16777216 and d[0] == 0xE9              # image magic
print("chip id", struct.unpack('<H', d[0x0c:0x0e])[0])  # 5 = ESP32-C3

pt = d[0x8000:0x9000]                                   # partition table
for i in range(0, 0x1000, 32):
    e = pt[i:i+32]
    if e[:2] != b'\xAA\x50': break
    off, size = struct.unpack('<II', e[4:12])
    print(e[12:28].rstrip(b'\0').decode(), hex(off), hex(size))

p = 0x10000 + 0x20                                      # esp_app_desc_t
assert struct.unpack('<I', d[p:p+4])[0] == 0xABCD5432
print(d[p+48:p+80].rstrip(b'\0'))    # project_name
print(d[p+96:p+112].rstrip(b'\0'))   # build date
print(d[p+112:p+144].rstrip(b'\0'))  # idf_ver
print(d[p+144:p+176].hex())          # elf_sha256

# otadata: which slot boots
print(struct.unpack('<I', d[0xE000:0xE004])[0],
      struct.unpack('<I', d[0xF000:0xF004])[0])
```

**Reusable on any Xteink image** — it is how the X4 Pro and X4 Classic layouts in
this tree could be verified if their dumps were ever obtained.

## Reported working (community, not executed here)

| # | Command / procedure | Source | Status |
|---|---|---|---|
| 7 | `esptool.py --chip esp32c3 --port /dev/ttyUSB0 --baud 921600 read_flash 0 0x1000000 x4-stock-full.bin` | What `eink-quick-flasher` automates (~2 min for 16 MB) | `reported-working` |
| 8 | `esptool.py --chip esp32c3 … write_flash 0 x4-stock-full.bin` | Full restore | `reported-working` |
| 9 | SD-card install on a **locked** unit: drop `update.bin` on the card root, **hold Power + Up at boot** | [r/XTEINK `1ult9dy`](https://old.reddit.com/r/XTEINK/comments/1ult9dy/) | `reported-working` — **author warns the combo is unverified per unit** |
| 10 | OTA-unlock a USB-locked stock device via `crosspointreader.com` | [r/xteinkereader `1tl3gnn`](https://old.reddit.com/r/xteinkereader/comments/1tl3gnn/) | `reported-working` |
| 11 | Recover from a 1.2.0 OTA brick (`esp_ota_end()` failure) | [`togotago/xteink-x4-escape`](https://github.com/togotago/xteink-x4-escape) | `reported-working` |

## Inferred — never executed, never reported

| # | Command | Note |
|---|---|---|
| 12 | `esptool.py --chip esp32c3 --port /dev/ttyUSB0 flash_id` | **Would identify the Puya flash part number** from its JEDEC ID — the cheapest open identification in the subject |
| 13 | `pio run -e x4 [-t upload]` | Standard PlatformIO |
| 14 | `python3 tools/esp_image_info.py x4-stock-full.bin` | Helper already in this repo |
| 15 | `esptool.py --chip esp32c3 … read_flash 0xC90000 0x360000 spiffs.bin` then a SPIFFS extractor | **Would recover the on-device web UI.** Not attempted |

## Build configuration

```ini
board_build.mcu = esp32c3
build_flags = -DFREEINK_DEVICE_X4=1
              ; optional, OUT OF SPEC (2x datasheet):
              ; -DFREEINK_X4_OVERCLOCK_SPI
```

## Commands deliberately not run

| Command | Why not |
|---|---|
| Any `write_flash` | No hardware |
| `curl http://gotaserver.xteink.com/api/check-update` | Recovered from the dump but **not queried** — request format unknown and it would contact a vendor server. Recorded as an open action |
