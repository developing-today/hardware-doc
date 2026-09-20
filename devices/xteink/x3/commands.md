# Xteink X3 — command ledger

Family-wide research commands: [`../x4-pro/commands.md`](../x4-pro/commands.md).
X4 firmware-analysis commands (reusable here): [`../x4/commands.md`](../x4/commands.md).
Retrieved **2026-09-04**. **No command was executed against X3 hardware.**

## Executed successfully by this session

| # | Command | Purpose | Status |
|---|---|---|---|
| 1 | `curl -sSL "https://imgur.com/ajaxalbums/getimages/OA6CS2C/hit.json"` | **Enumerate the 13-image teardown album.** The album HTML is a JS shell yielding only 2 of 13 | `executed-success` |
| 2 | `for i in $(seq 1 13); do curl -sSL "https://i.imgur.com/<hash>.jpg" -o …; done` | Fetch all 13 teardown images with captions | `executed-success` |
| 3 | `for i in 01..10; do curl -sSL "https://raw.githubusercontent.com/sunwoods/Xteink-X3/main/readme-img/$i.jpg"; done` | Fetch the Chinese teardown set **including the schematic sketch (`02.jpg`)** | `executed-success` |
| 4 | `curl -sSL ".../sunwoods/Xteink-X3/main/README.md"` | The BOM: Puya flash, QMI8658, DS-series RTC, TP4056-class charger, BQ27220, **ISO 14443A NFC tag** | `executed-success` |
| 5 | `curl -sSL ".../zocs/eink-quick-flasher/main/firmware/README.md"` | Stock versions **V1.0.7** and **V5.2.13**, CN+EN, full **and** OTA | `executed-success` |
| 6 | `gh api graphql -f query='{repository(owner:"crosspoint-reader",name:"crosspoint-reader"){discussion(number:2259){…}}}'` | **Resolved the NFC tag's nature and purpose.** Repository *search* does not index discussions — GraphQL is required | `executed-success` |
| 7 | `sha256sum` over all 23 teardown images | Provenance before archiving | `executed-success` |
| 8 | `python3 tools/archive_artifact.py --repo-root . --manifest …` | Archived both teardown sets with placeholders | `executed-success` |

## Reported working — community

| # | Procedure | Source | Status |
|---|---|---|---|
| 9 | Full backup/restore in ~2 min via [`zocs/eink-quick-flasher`](https://github.com/zocs/eink-quick-flasher) GUI, auto COM detect | its README + `X3-FLASHER-GUIDE` (EN and CN) | `reported-working` |
| 10 | `esptool.py --chip esp32c3 --port /dev/ttyUSB0 --baud 921600 read_flash 0 0x1000000 x3-stock-full.bin` | what #9 automates | `reported-working` |
| 11 | `esptool.py --chip esp32c3 … write_flash 0 x3-stock-full.bin` | restore | `reported-working` |
| 12 | Locked unit: reflash via `crosspointreader.com`, or **SD flash** | [r/XTEINK `1uek163`](https://old.reddit.com/r/XTEINK/comments/1uek163/) | `reported-working` |
| 13 | **Write the NFC tag** with any Android NFC-writer app (e.g. "NFC Tools"), payload = vCard or a URL | [r/xteinkereader `1vit43t`](https://old.reddit.com/r/xteinkereader/comments/1vit43t/) | `reported-working` — *"Used an NFC writer app on my Android phone, created a contact card format…"* |
| 14 | **iOS**: use **Shortcuts** to *detect* the tag and run an automation. iOS **cannot read/write** it | [discussion #2259](https://github.com/crosspoint-reader/crosspoint-reader/discussions/2259) | `reported-working` |

## Inferred — never executed, never reported

| # | Command | Would establish |
|---|---|---|
| 15 | `esptool.py --chip esp32c3 --port /dev/ttyUSB0 flash_id` | **The Puya flash part number** from its JEDEC ID |
| 16 | I²C read of registers `0x11`/`0x12` at address `0x68` | **Whether the RTC is a DS3231 (returns a temperature) or a DS1307 (does not).** One read settles a three-way conflict |
| 17 | I²C scan on **SDA 20 / SCL 0 @ 400 kHz** | Confirm 0x55 / 0x68 / 0x6B and therefore the board profile |
| 18 | Read `0x00` at `0x6B` expecting `0x05` | QMI8658 `WHO_AM_I` |
| 19 | Android NFC app reporting **tag technology and UID prefix** | The NFC tag's **type and likely part family** |
| 20 | `pio run -e x3 [-t upload]` | Standard build |
| 21 | Boot with serial attached, read `[XTDET] bus probe VER=… FLG=… -> …` | **Which panel controller a given unit carries** — the unanswered question in the two-unit comparison |

**Commands 15, 16, 19 and 21 would each close a named open conflict in this
record, and each takes under a minute on hardware.**

## Build configuration

```ini
board_build.mcu = esp32c3
build_flags = -DFREEINK_DEVICE_X3=1          ; links BOTH UC8253 and UC8279 drivers
              ; optional UC8279 tuning:
              ; -DFREEINK_UC8279_CONFIG=yourConfig
```

`-DFREEINK_DEVICE_X3=1` and `-DFREEINK_DEVICE_X4=1` **can coexist**: one C3 binary
serves X3-UC8253, X3-UC8279d and X4, resolved at boot by `XteinkDetect`.

## Not run, deliberately

| Command | Why |
|---|---|
| Any `write_flash` | No hardware |
| Git-LFS fetch of the four stock X3 images | Deferred; would need `git lfs`. **Cheap to close** |
| `curl http://gotaserver.xteink.com/api/check-update` | Would contact a vendor server; request format unknown |
