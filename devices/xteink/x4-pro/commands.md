# Xteink X4 Pro — command ledger

Every command discovered or executed. **No command was executed against X4 Pro
hardware** — none was available.

## Executed successfully (research, not hardware)

| # | Command | Purpose | Status |
|---|---|---|---|
| 1 | `curl -sSL -A "$UA" "https://www.xteink.com/products.json?limit=250&page=N" -o vendor/products-pN.json` | Vendor catalogue + live pricing | `executed-success` 2026-09-04 |
| 2 | `curl -sSL -A "$UA" "https://www.xteink.com/collections/<handle>/products.json?limit=250"` | Per-line product membership | `executed-success` |
| 3 | `curl -s -A "WhatsApp/2.23.20.0" "https://old.reddit.com/search.json?q=<q>&limit=100&sort=relevance&t=all"` | Community corpus. **200 on all 23 requests** | `executed-success` |
| 4 | `curl -s -H "Authorization: Bearer $(gh auth token)" "https://api.github.com/search/repositories?q=xteink&per_page=100&page=N"` | Project census; token avoids the 60/h anonymous limit | `executed-success` |
| 5 | `curl -sSL "https://imgur.com/ajaxalbums/getimages/<albumid>/hit.json"` | **Enumerate a full Imgur album** — the HTML page yields only 2 of 13 images | `executed-success` |
| 6 | `python3 tools/archive_artifact.py --repo-root . --manifest <m>.json` | Archive bulky artifacts + write placeholders | `executed-success` |
| 7 | `python3 tools/link_archived.py --apply` | Create the in-place archive symlinks | `executed-success` |

### Failed, and the fix

| # | Command | Failure | Diagnosis / fix |
|---|---|---|---|
| 8 | `curl -m 60 "http://web.archive.org/cdx/search/cdx?url=xteink.com*&limit=3000"` | `curl: (28) Operation timed out after 60000 ms with 0 bytes received` | CDX is slow on wildcard prefix queries. **Not retried.** Try a longer timeout, `matchType=prefix`, or paginate with `&limit=200&resumeKey=` | `executed-failed` |
| 9 | `curl "https://xteink.cn/"` / `"https://xteink.net/"` | HTTP 000 | Hosts do not resolve/answer. **But `bofi.xteink.cn` appears inside the X4 firmware**, so a subdomain is live even though the apex is not | `executed-failed` |
| 10 | `python3 tools/archive_artifact.py … ` (first attempt) | `AttributeError: 'str' object has no attribute 'get'` | The manifest's `source` field must be an **object**, not a string, and `notes` must be a **list**. Corrected manifest schema: `{path, reason, notes[], source:{repo,path_in_repo,author,retrieved,license,difficulty,access_notes,url,urls[{url,desc}]}}` | `executed-failed` → fixed |

## Reported working (community, not executed here)

| # | Command / procedure | Source | Status |
|---|---|---|---|
| 11 | `pio run -e x4pro` / `-t upload` | FreeInk `platformio.sample.ini` env exists | `reported-working` |
| 12 | Flash a locked unit: drop `update.bin` on the SD root, **hold Power + Up at boot** | [r/XTEINK `1ult9dy`](https://old.reddit.com/r/XTEINK/comments/1ult9dy/) | `reported-working` — **author warns the button combo is unverified per unit** |
| 13 | OTA-unlock a USB-locked stock device via crosspointreader.com | [r/xteinkereader `1tl3gnn`](https://old.reddit.com/r/xteinkereader/comments/1tl3gnn/) | `reported-working` |
| 14 | Reflash from the web flasher if OTA fails: *"You can simply reflash from the website if you're unlocked or SD flash if you're locked"* | [r/XTEINK `1uek163`](https://old.reddit.com/r/XTEINK/comments/1uek163/) | `reported-working` |

## Inferred (never executed, never reported — do not treat as authoritative)

| # | Command | Note |
|---|---|---|
| 15 | `esptool.py --chip esp32s3 --port /dev/ttyACM0 --baud 921600 read_flash 0 0x1000000 x4pro-stock-full.bin` | Standard 16 MB read. **Requires a USB-unlocked unit** |
| 16 | `esptool.py --chip esp32s3 … write_flash 0 x4pro-stock-full.bin` | Restore. **There is no public X4 Pro image** — this only works with your own backup |
| 17 | `python3 tools/esp_image_info.py <dump>.bin` | Parse the image. Helper already in this repo |
| 18 | `pio device monitor -b 115200` | Serial log over native USB-CDC |

## Build prerequisites

```ini
board = esp32-s3-devkitc1-n16r8
board_build.mcu = esp32s3
build_flags = -DBOARD_HAS_PSRAM -DFREEINK_DEVICE_X4PRO=1
              -DUSE_BLOCK_DEVICE_INTERFACE=1   ; required for SD, in the consumer build
```

## Analysis commands used on the sibling X4 dump

Reusable on any Xteink image; run against `x4-oem-flash.bin`:

```python
# executed-success 2026-09-04 — partition table at 0x8000
for i in range(0, 0x1000, 32):
    e = pt[i:i+32]
    if e[:2] != b'\xAA\x50': break
    off, size = struct.unpack('<II', e[4:12])
    label = e[12:28].rstrip(b'\x00').decode()

# executed-success — esp_app_desc_t at partition_offset + 0x20, magic 0xABCD5432
# fields: version[32]@+16, project[32]@+48, time[16]@+80, date[16]@+96,
#         idf_ver[32]@+112, elf_sha256[32]@+144
```
