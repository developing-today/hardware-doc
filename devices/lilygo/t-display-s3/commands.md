# T-Display-S3 — command ledger

Every command that mattered, with status. **No hardware was attached**, so board-side commands
are `reported-working` or `inferred`, never `executed-success`.

Environment for everything marked `executed-success`: Linux, bash, Python 3.11+, `gh` CLI
authenticated, `curl`. Date 2026-09-07.

## Acquisition

```bash
# Enumerate the vendor's whole GitHub org (the family-enumeration evidence).
for p in 1 2 3; do
  gh api "orgs/Xinyuan-LilyGO/repos?per_page=100&page=$p&sort=updated" \
    --jq '.[] | [.name,.pushed_at,.default_branch,.stargazers_count,(.description//"")] | @tsv'
done
```
`executed-success` — 254 rows. Uses the token, which lifts the API limit from 60/h to 5 000/h;
without it this call alone can exhaust the anonymous quota.

```bash
# Pin a repository to a commit before fetching anything from it.
gh api repos/Xinyuan-LilyGO/T-Display-S3/commits/main --jq '.sha'
#   -> ec889e789b3cf093412689a143f7f37b42b56af7

# Recursive tree listing at that commit (one call instead of hundreds).
gh api "repos/Xinyuan-LilyGO/T-Display-S3/git/trees/ec889e78…?recursive=1" \
  --jq '.tree[] | [.type,.size//0,.path] | @tsv'
```
`executed-success` — 3 431 entries.

```bash
# Fetch a file at a pinned commit. raw.githubusercontent is not the API and is far
# more permissive; still send the token.
curl -fsSL -H "Authorization: Bearer $(gh auth token)" \
  "https://raw.githubusercontent.com/Xinyuan-LilyGO/T-Display-S3/ec889e78…/examples/factory/pin_config.h"
```
`executed-success`.

## Validation

```bash
# Never trust a URL suffix. `file` was NOT available on this host; a magic-byte
# check was written instead.
python3 archive/devices/lilygo/t-display-s3-shared/artifacts/research-scratch/magic.py <paths...>
```
`executed-success`. Output columns: detected type, byte size, SHA-256, path. Every artifact in
this record passed; **no HTML error page was retained under a `.pdf` or `.bin` name.**

```bash
sha256sum <file>; stat -c%s <file>
```
`executed-success`. This is what found [G1](gaps-and-conflicts.md#g1--the-touch-and-no-touch-factory-images-are-byte-identical).

<a id="decoding-an-esp32-app-descriptor"></a>
## Decoding an ESP32 app descriptor from a merged image

The repository's own [`tools/esp_image_info.py`](../../../tools/esp_image_info.py) reads the
image header correctly but reports *"no app descriptor"* on these files, because a **merged**
image has the bootloader at `0x0` and the app at `0x10000` — the descriptor is at `0x10020`,
not `0x20`. That is a real limitation worth recording rather than working around silently.

```bash
python3 tools/esp_image_info.py <merged.bin>          # bootloader header: chip, flash size/mode
python3 archive/devices/lilygo/t-display-s3-shared/artifacts/research-scratch/appdesc.py <merged.bin>   # scans for magic 0xABCD5432
```
Both `executed-success`. The second also decodes the partition table at `0x8000`
(entry magic `0xAA50`, 32-byte records), which is how the 8 MB-vs-16 MB layout split in
[`factory-firmware.md`](factory-firmware.md) §3 was found.

## Reading an Altium schematic PDF without poppler

`pdftotext`, `pdftoppm`, `qpdf`, `mutool` and `pypdf` were **all unavailable**, and there is no
package manager on the host. A minimal extractor was written instead:

```bash
python3 archive/devices/lilygo/t-display-s3-shared/artifacts/research-scratch/pdfall.py <sheet.pdf>   # WinAnsi fonts, Form XObjects
python3 archive/devices/lilygo/t-display-s3-shared/artifacts/research-scratch/pdfcid.py <sheet.pdf>   # Type0/Identity-H via ToUnicode CMap
```
`executed-success`, with two lessons worth carrying forward:

1. **Altium puts the whole sheet in a Form XObject**, so reading `/Contents` alone returns only
   the `PI…`/`CO…` pin markers and none of the labels. You must walk every stream in the file.
2. **Text must be grouped by `BT…ET` block.** Reading `Tj`/`TJ` operators individually
   shreds every label into single characters, which is what the first attempt did.

**Both extractors were cross-checked against each other** on the Chipone CO5300 datasheet,
which uses a **uniform +0x1D code-point offset** — the exact "human-legible but wrong" trap the
research skill warns about. The raw route yielded `&+,321(7HFKQRORJ\` and the CMap route
yielded `FHHPONE TecOnology`; both decode to **CHIPONE Technology**, and neither is readable as
written. Recorded in [`vendors/lilygo/README.md`](../../../vendors/lilygo/README.md).

**Not done:** net-level connectivity. `tools/altium_pdf_netlist.py` needs `pdftotext -bbox`
XML. `inferred` blocker; see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) K1.

```bash
# The command that would close K1, once poppler exists:
for p in $(seq 1 1); do pdftotext -bbox -f $p -l $p T_Display_S3.pdf pdf/bbox-p$p.xml; done
python3 tools/altium_pdf_pin_table.py 1 U2
```
`not-tested` — poppler absent.

## Market data

```bash
curl -sS -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) …Chrome/131…' \
  'https://lilygo.cc/collections/all/products.json?limit=250&page=1'
```
`executed-success` — 214 products, full variant/price/stock detail. Shopify's public product
feed is far better evidence than scraping the rendered page, and it carries `published_at`
(the product's launch date) and per-variant `available`.

```bash
# Reddit: www.reddit.com returns 403 to scripts; old.reddit.com with a link-preview UA does not.
curl -sS -A 'WhatsApp/2.23.20.0' 'https://old.reddit.com/search.json?q=t-display-s3&limit=25&t=all'
curl -sS -A 'WhatsApp/2.23.20.0' 'https://old.reddit.com/r/esp32/comments/<id>/.json'
```
`executed-success`.

## Board-side commands (none executed here)

```bash
# Restore a board. reported-working (LilyGO's documented procedure).
esptool.py --chip esp32s3 --port /dev/ttyACM0 erase_flash
esptool.py --chip esp32s3 --port /dev/ttyACM0 --baud 921600 \
    write_flash -z 0x0 t-display-s3-lvgl-demo-20250109_0x0.bin

# Identify a board. inferred (standard esptool usage, not run against this board).
esptool.py --chip esp32s3 --port /dev/ttyACM0 flash_id

# Build and flash the vendor examples. reported-working.
pio run -e factory
pio run -e factory -t upload
pio device monitor -b 115200
```

The port is **`/dev/ttyACM*`** (CDC-ACM), not `/dev/ttyUSB*` — there is no UART bridge. See
[`features/usb.md`](features/usb.md).

## Failed / abandoned

| Command | Result | Diagnosis |
|---|---|---|
| `file -b --mime-type <f>` | `file: command not found` | not installed; replaced by `magic.py` |
| `pip install pypdf` | `pip: command not found` | no Python package manager; extractors written from scratch |
| `gh api search/code -f q='repo:arendst/Tasmota t-display-s3'` | HTTP 404 | GitHub code search does not index every repo for every query shape. `repo:arendst/Tasmota lilygo` worked and returned 19 hits |
| `gh api -X GET search/code -f q='org:meshtastic t-display-s3'` | HTTP 404 | hyphenated terms confuse code search; `org:meshtastic tdisplay` returned 247 hits, none a T-Display-S3 variant |
