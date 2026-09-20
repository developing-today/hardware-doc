# DinMeter — command ledger

Every consequential command from this research pass, with status. Shell `bash 5.x` on NixOS,
`curl 8.x`, `python3 3.14.7`, `git`/`gh` present, 2026-09-04.

Status vocabulary: `executed-success` · `executed-failed` · `reported-working` · `inferred` ·
`not-tested`.

---

## 1. Environment — what was missing, and the way round it

```bash
which pdftotext pdfinfo qpdf mutool pdfimages     # executed-failed: none present
python3 -c "import pypdf"                          # executed-failed: ModuleNotFoundError
python3 -m pip --version                           # executed-failed: No module named pip
uv venv /tmp/opencode/.pdfvenv                     # executed-success
uv pip install --python /tmp/opencode/.pdfvenv/bin/python pdfminer.six pymupdf   # executed-success (install)
/tmp/opencode/.pdfvenv/bin/python -c "import fitz" # executed-failed: ImportError: libstdc++.so.6: cannot open shared object file
/tmp/opencode/.pdfvenv/bin/python -c "import pdfminer; print(pdfminer.__version__)"  # executed-success: 20260107
```

**Diagnosis:** `pymupdf`'s compiled extension needs a `libstdc++` that is not on this NixOS host.
`pdfminer.six` is pure Python and works. Corrected approach: use `pdfminer.six` and emit
poppler-compatible bbox XML so the repository's existing Altium tooling conventions still apply.

Also absent: `file`, `xxd`. Use `curl -w '%{content_type}'` and a Python magic-byte check instead.

## 2. Vendor documentation

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

# negative control -- the obvious URL is wrong
curl -sS -A "$UA" -o /dev/null -w '%{http_code}\n' -L https://docs.m5stack.com/en/core/DinMeter
# executed-success -> 404

curl -sS -A "$UA" -o docs-en-core-M5DinMeter.html   -L https://docs.m5stack.com/en/core/M5DinMeter    # 200, 139501 B
curl -sS -A "$UA" -o docs-en-core-DinMeter_v1.1.html -L https://docs.m5stack.com/en/core/DinMeter_v1.1 # 200, 142090 B
# executed-success both
```

Extraction: the pages are Vue/Nuxt shells but the content **is** in the served HTML under
`id="document"`. Naive tag-stripping loses it; slicing from that anchor first works.

```bash
curl -sS -A "$UA" -o sitemap.xml -L https://docs.m5stack.com/sitemap.xml   # executed-success: 200, 499000 B, 5703 <loc>
```
**This is the only reliable way to enumerate M5Stack product pages** — `/en/products` is a JS
shell with no product links in its HTML.

## 3. Artifact acquisition

```bash
dl(){ code=$(curl -sS -A "$UA" -L -o "$2" -w '%{http_code}' "$1"); printf '%s %s %s\n' "$code" "$(stat -c%s "$2")" "$2"; }

dl 'https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/500/DIN_Meter_v1.0.pdf' K134_DIN_Meter_v1.0-schematic.pdf
dl 'https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1211/K134-V11_DIN_Meter_v1.0_2025_11_25_17_15_58.pdf' K134-V11-schematic.pdf
dl 'https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/522/Sch_M5StampS3_v0.2.pdf' Sch_M5StampS3_v0.2.pdf
dl 'https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1150/Sch_StampS3_v0.3.3.pdf' Sch_StampS3_v0.3.3-StampS3A.pdf
# ... 19 files total, all executed-success, all HTTP 200
sha256sum *.pdf   # executed-success
```

**The finding that came out of hashing rather than reading:**

```
03ec335396e4f527119f89f697fca9887505dc1b28077871b2fb361ba6e4c070  K134_DIN_Meter_v1.0-schematic.pdf
03ec335396e4f527119f89f697fca9887505dc1b28077871b2fb361ba6e4c070  K134-V11-schematic.pdf
```
Two URLs, two filenames, **one file**. Same again for `Stamp-S3.stl` / `Stamp-S3A.stl` and
`DinMeter.stl` / `DinMeter_v1.1.stl`.

Magic-byte validation (no `file(1)` on this host):
```bash
python3 -c "
import sys
for f in sys.argv[1:]:
    print(open(f,'rb').read(5), f)" *.pdf     # executed-success: b'%PDF-' for all
```

## 4. Schematic parsing

```bash
# emit poppler `pdftotext -bbox`-compatible XML from pdfminer.six
/tmp/opencode/.pdfvenv/bin/python /tmp/opencode/pdf_bbox.py K134_DIN_Meter_v1.0-schematic.pdf \
  > K134_DIN_Meter_v1.0-schematic.bbox.xml
# executed-success: 900 <word> elements, 1 page

python3 artifacts/schematic/parse_dinmeter_sch.py K134_DIN_Meter_v1.0-schematic.bbox.xml
# executed-success: words=900 plain=553 CO=85 PI=238 NL=25
```

### The failure worth preserving

The **first** parse produced designators like `PPIIJJ110011` and `LP3218DT1GPPIIJJ110011`.

**Diagnosis:** Altium's PDF publisher draws the invisible marker layer **twice** at identical
coordinates. The word-grouping step interleaved the two copies character by character, yielding
*human-legible but wrong* text — the most dangerous kind of extraction failure, because it does
not look broken.

**Fix:** deduplicate glyphs on rounded `(x0, y0, x1, y1, char)` before grouping. `executed-success`
after the fix; the pre-fix output was discarded, not published.

### Proving absence

```bash
python3 -c "
from pdfminer.high_level import extract_text; import re
t=re.sub(r'\s+','',extract_text('K134_DIN_Meter_v1.0-schematic.pdf'))
def dbl(s): return ''.join(c*2 for c in s)
for p in ['COS1','COR20','COY1','COQ2','COS4','COU1','COM1']:
    print(p,'single=',t.count(p),'doubled=',t.count(dbl(p)))"
# executed-success:
#   COS1 0/0   COR20 0/0   COY1 0/0   COQ2 0/0
#   COS4 1/0   COU1 1/0    COM1 1/0
```
A **complete** census, not a search for expected parts. Result recorded in
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) §2.

## 5. GitHub (authenticated — `api.github.com` limits per identity, no UA helps)

```bash
T="$(gh auth token)"
curl -sS -H "Authorization: Bearer $T" -G \
  --data-urlencode 'q=DinMeter in:name,description,readme' --data 'per_page=50' \
  https://api.github.com/search/repositories                       # executed-success: 19
curl -sS -H "Authorization: Bearer $T" -G \
  --data-urlencode 'q=repo:esphome/esphome dinmeter' \
  https://api.github.com/search/code                               # executed-success: 0

gh api repos/m5stack/M5DinMeter                                    # executed-success
curl -sSL -H "Authorization: Bearer $T" \
  -o M5DinMeter-8ccbad72….tar.gz \
  https://api.github.com/repos/m5stack/M5DinMeter/tarball/8ccbad7297beb82a140f812e5606e060d8a5e0dc
# executed-success: 8532 B, sha256 de47c4109635870506bb7a02040db496f82e5bbb22a5b1befe600a3985eb0f02

curl -sSL -o dinmeter-board_peripherals.yaml \
  https://raw.githubusercontent.com/espressif/esp-board-manager/main/m5stack_boards/m5stack_dinmeter/board_peripherals.yaml
# executed-success: 5014 B
```

## 6. Shop / pricing

```bash
curl -sS -A "$UA" -L https://shop.m5stack.com/products/m5stack-din-meter-v1-1-with-m5stamps3a.js
# executed-success -> K134-V11, price 2450 (USD 24.50), available true, created 2026-01-30
curl -sS -A "$UA" -L https://shop.m5stack.com/products/m5stack-din-meter-with-m5stamps3.js
# executed-failed: HTTP 404 -- wrong slug guess
curl -sS -A "$UA" -L https://shop.m5stack.com/products/m5stack-din-meter-w-m5stamps3.js
# executed-success -> "[EOL] M5Stack Din Meter w/ M5StampS3", K134, 2450, available FALSE
```
The working slug was recovered from a link in `bmorcelli/Launcher`'s README, not from M5Stack.

Suggest-endpoint enumeration (note the brackets **must** be percent-encoded — a raw `[` makes
curl try to parse a range):
```bash
curl -sS -A "$UA" -L 'https://shop.m5stack.com/search/suggest.json?q=din+meter&resources%5Btype%5D=product&resources%5Blimit%5D=10'
# executed-success
curl -sS -A "$UA" -L 'https://shop.m5stack.com/search/suggest.json?q=din meter&resources[type]=product'
# executed-failed: curl: (3) bad range in position 70
```

## 7. Reddit

```bash
curl -sS -A 'WhatsApp/2.23.20.0' -G \
  --data-urlencode 'q=DinMeter' --data 'limit=50&sort=relevance&t=all&raw_json=1' \
  https://old.reddit.com/search.json          # executed-success: 200, 838509 B
```
`www.reddit.com` returns 403 to automated clients; `old.reddit.com` with the WhatsApp
link-preview UA returns 200. Consistent with this repository's existing access table.

## 8. M5Stack forum — both attempts failed

```bash
curl -sS -A "$UA" -L 'https://community.m5stack.com/api/search?term=dinmeter&in=titlesposts'
# executed-failed: HTTP 401
# {"status":{"code":"not-authorised","message":"A valid login session was not found. Please log in and try again."}}

curl -sS -A "$UA" -L 'https://community.m5stack.com/search?term=dinmeter&in=titlesposts'
# executed-success (HTTP 200, 16986 B) but useless: NodeBB JS shell, no results in the HTML
```
Recorded rather than worked around. Rotating User-Agents would not help — this is
authentication, not bot-blocking, and per the repository's retrieval policy UA substitution must
not be used to bypass access controls.

## 9. Repository hygiene

```bash
find vendors/m5stack/README.md -mmin -30            # executed-success: empty -> safe to append
find components/awinic/aw35122/README.md -mmin -30  # executed-success: empty -> safe to append a Used By row
git status --porcelain                              # executed-success (read-only)
```
No state-changing git command was run at any point in this pass.

---

## 10. Commands for the reader — **none of these were run here**

Everything below is `not-tested` on the device and is labelled so.

```bash
# Back up the factory image BEFORE overwriting it. There is no vendor-published binary.
esptool.py --chip esp32s3 -p /dev/ttyACM0 -b 460800 read_flash 0 0x800000 dinmeter-factory-backup.bin
# not-tested

# Identify the chip and flash size
esptool.py --chip esp32s3 -p /dev/ttyACM0 flash_id            # not-tested

# Restore
esptool.py --chip esp32s3 -p /dev/ttyACM0 write_flash 0 dinmeter-factory-backup.bin   # not-tested

# Arduino
arduino-cli board listall | grep -i din      # not-tested -- run this to LEARN the FQBN;
                                             # `m5stack:esp32:m5stack_dinmeter` is a GUESS
arduino-cli compile -b <fqbn> sketch/        # not-tested
arduino-cli upload -b <fqbn> -p /dev/ttyACM0 sketch/          # not-tested

# ESP-IDF
idf.py set-target esp32s3 && idf.py build && idf.py -p /dev/ttyACM0 flash monitor   # not-tested

# Download mode (hardware step, not a command)
#   hold the G0 button on the Stamp module, apply power, release G0.   reported-working (vendor)
```

## 11. Reusable scripts checked in

| Script | Purpose | Status |
|---|---|---|
| [`artifacts/schematic/parse_dinmeter_sch.py`](artifacts/schematic/parse_dinmeter_sch.py) | Parse the Altium `CO`/`PI`/`NL` marker layer from bbox XML: designator census, net labels, pin→net mapping | `executed-success` |
| [`acquisition/README.md`](acquisition/README.md) | Clean-clone reacquisition, in execution order | commands `not-tested` from a clean clone |
