# Cardputer ADV — command ledger

> Every command that mattered, with status. Environment: **Linux (NixOS-style store paths)**,
> **bash 5**, `curl 8.x`, `git 2.x`, `python3` (stdlib only), `gh` CLI authenticated.
> Date **2026-09-04**. Working directory for scratch commands:
> `hardware-doc/archive/devices/m5stack/shared-artifacts/cardputer/`.
>
> Status ∈ `executed-success`, `executed-failed`, `reported-working`, `inferred`, `not-tested`.

## 0. Host limitations that shaped everything below

```bash
which pdftotext qpdf mutool gs        # -> not found (all three)
python3 -c "import pypdf"             # ModuleNotFoundError
python3 -c "import fitz"              # ModuleNotFoundError
python3 -c "import pdfminer"          # ModuleNotFoundError
python3 -c "import PIL"               # not available
which file                            # -> not found
```
`executed-success` (as negative probes). **No PDF or image tooling exists on this host**, which
is why `pdfbbox.py` and `pngcrop.py` were written. `file` is also absent, so MIME validation was
done by reading magic bytes in Python.

## 1. Fetching M5Stack documentation

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
curl -sS -o cardputer-adv.html -w '%{http_code} %{size_download}\n' -A "$UA" -L \
  "https://docs.m5stack.com/en/core/Cardputer-Adv"                      # 200 147339
curl -sS -o cardputer-v1.1.html  -A "$UA" -L "https://docs.m5stack.com/en/core/Cardputer%20V1.1"   # 200
curl -sS -o cardputer-mesh.html  -A "$UA" -L "https://docs.m5stack.com/en/core/Cardputer_Mesh_Kit" # 200
curl -sS -o cardputer-zero.html  -A "$UA" -L "https://docs.m5stack.com/en/CardputerZero"           # 200
curl -sS -o adv.zh.html          -A "$UA" -L "https://docs.m5stack.com/zh_CN/core/Cardputer-Adv"   # 200
```
`executed-success`. **No User-Agent fallback was needed** — every M5Stack host answered 200 to
the first request, confirming `vendors/m5stack` §1.

```bash
curl -sS -A "$UA" -L "https://docs.m5stack.com/en/accessory/Cardputer%20Accessory%20Kit_v1.1"
# -> 404, 4162 bytes
```
`executed-failed` — **useful negative.** The `_v1.1` suffix form does not exist for accessory
pages; the v1.1 accessory kit is a shop SKU only.

## 2. Fetching artifacts, with validation

```bash
dl(){ u="$1"; o="$(basename "$u")"
      c=$(curl -sS -o "$o" -w '%{http_code}' -A "$UA" -L "$u")
      echo "$c $(stat -c%s "$o") $o"; }
dl "https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1178/Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf"
dl "https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1150/Sch_StampS3_v0.3.3.pdf"
dl "https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1127/Sch_M5Cardputer.pdf"
dl "https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/481/Sch_M5Cardputer.pdf"
dl "https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/522/Sch_M5StampS3_v0.2.pdf"
sha256sum *.pdf
```
`executed-success`. Because `file` is unavailable, type validation was:

```bash
python3 -c "
for f in ['Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf']:
    print(f, open(f,'rb').read(8))"     # -> b'%PDF-1.4'
```
`executed-success`.

**The finding that came out of hashing:**

```bash
cmp Sch_M5Cardputer.pdf v10-Sch_M5Cardputer.pdf && echo IDENTICAL
# -> IDENTICAL v1.0 vs v1.1 schematic PDFs
```
`executed-success`. Both are `6016c1fe6099b9e3f0d0c88f07a3fba1aa44a3da8a7a91dd7040ad0fffa2041e`.

## 3. Sheet renders

```bash
for n in 01 02 03 04; do
  curl -sS -A "$UA" -L -o "adv-sch-page_$n.png" \
    "https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1178/Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58_page_$n.png"
done
python3 -c "
import struct,glob
for f in sorted(glob.glob('*.png')):
    d=open(f,'rb').read(33); print(f, *struct.unpack('>II', d[16:24]))"
# -> each 5848 4132
```
`executed-success`.

```bash
curl -sS -A "$UA" -L -o stamps3-sch_01.png \
  "https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/522/Sch_M5StampS3_v0.2_page_01.png"
# -> 402 bytes, not a PNG
```
`executed-failed` — **useful negative.** The `_page_NN.png` render convention does **not** apply
to product id `522`. Do not assume renders exist for every schematic. The file was **not**
retained under a `.png` name (per the skill's rule about misleading extensions); it was deleted
after the magic-byte check.

## 4. PDF text extraction (custom tool)

```bash
python3 pdfbbox.py artifacts/Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf - pdf-adv
# page 1: 712 words -> pdf-adv/bbox-p1.xml   (etc.)
```
`executed-success`, after three corrections that are worth recording because each failed
*silently*:

| Attempt | Symptom | Cause | Fix |
|---|---|---|---|
| 1 | 865 "words", all `CO`/`PI`/`NL` markers, characters doubled (`PPIICC110022`) | Altium draws each glyph twice (fill + stroke) | de-duplicate on `(char, round(x,2), round(y,2))` |
| 2 | every character its own word | glyph advance computed as `w/1000×fsize`, ignoring the scale Altium hides in `Tm` | transform the pen position before and after each glyph; take the device-space distance |
| 3 | 296 words, **no readable text at all** — only the marker layer | the `Do` operator was ignored, and the entire drawing lives in a **Form XObject** | recurse into Form XObjects |

**Text-layer validation** (mandatory before transcribing anything):

```bash
grep -oiE '(TCA8418[A-Z]*|ES8311|NS4150B|NS4168|BMI270|SPM1423[A-Z0-9-]*|74HC138)' pdf-adv/all.txt pdf-v11/all.txt | sort | uniq -c
#  ADV: TCA8418RTWR, ES8311, NS4150B, BMI270
#  v11: 74HC138, NS4168, SPM1423HM4H-B
```
`executed-success`. These match the corresponding product pages' PinMap tables exactly — a clean
positive control. **Every value actually transcribed was additionally read off a rendered crop.**

## 5. Reference-designator census

```bash
python3 netlist.py pdf-adv     # wraps hardware-doc/tools/altium_pdf_netlist.py
# pdf-adv: pages=[1,2,3,4] distinct designators=155
#   U n=9 1..9 gaps=[]      <- nine ICs, no gaps: the inventory is complete
python3 pintable.py pdf-adv 2 U9 2.5     # TCA8418 pin table
python3 pintable.py pdf-adv 4 P3         # EXT header
```
`executed-success`. The `U` sequence having **no gaps** is what makes the "no RTC / no fuel gauge
/ no bridge" statements *verified negatives* rather than failed searches.

## 6. Sheet crops (custom tool)

Scale factor: 5848 px / 842 pt = 4132 / 595 = **6.945 px per PDF point**.

```bash
python3 pngcrop.py media/adv-sch-page_02.png media/crop-adv-kbd-u9.png     200  800 1900 2150 2
python3 pngcrop.py media/adv-sch-page_02.png media/crop-adv-kbd-matrix.png 1650 1300 3300 2900 2
python3 pngcrop.py media/adv-sch-page_02.png media/crop-adv-kbd-s1s2.png   1650 1380 2560 1800 1
python3 pngcrop.py media/adv-sch-page_02.png media/crop-adv-kbd-rowbus.png 1600  850 3300 1420 2
python3 pngcrop.py media/v11-sch_02.png      media/crop-v11-kbd-u7.png      200 1350 1900 2150 2
python3 pngcrop.py media/adv-sch-page_01.png media/crop-adv-pwr1.png        200  200 2450 1300 3
python3 pngcrop.py media/adv-sch-page_01.png media/crop-adv-pwr2.png       2400  200 4700 1300 3
python3 pngcrop.py media/stamps3a-sch_01.png media/crop-stamp-a.png         200  200 3000 2200 4
python3 pngcrop.py media/stamps3a-sch_01.png media/crop-stamp-b.png        2800  200 5800 2200 4
```
`executed-success`, ~1.4 s each. The `den` argument min-pools rather than point-samples, which
matters: point-sampling erases the thin strokes that *are* the schematic.

These nine crops produced, between them: the complete TCA8418 pinout, the three explicit
no-connects, the S1/S2 → `Y7`/`Y3` verification, the ROW-bus pairing, the 74HC138 pinout, the
TP4057/CN809J/SY7088 power train with its FB divider values, the DNP marking on R3/D3, and the
AW35122FDR/WS2812 rail relationship.

## 7. Source repositories

```bash
git clone -q --depth 50 https://github.com/m5stack/M5Cardputer.git
git clone -q --depth 50 https://github.com/m5stack/M5Unified.git
git clone -q --depth 50 https://github.com/m5stack/M5GFX.git
git clone -q          https://github.com/m5stack/M5Cardputer-UserDemo.git
git -C M5Cardputer-UserDemo checkout -q origin/CardputerADV
for d in M5Cardputer M5Unified M5GFX M5Cardputer-UserDemo; do
  git -C $d log -1 --format='%H %ad %s' --date=iso; done
```
`executed-success`. Commits recorded in [`sources.md`](sources.md).

Dating the ADV support:
```bash
git -C M5Cardputer log --format='%h %ad %s' --date=short --all | head -30
# c331c7d 2025-08-29 basic extract          <- reader interface refactor
# 6928513 2025-09-01 add basic tca8418 reader
# 8ab9f43 2025-09-02 Merge PR #9 add-cardputer-adv-support
# eccba25 2026-05-11 add fn layer support   <- arrow keys arrive
```
`executed-success`.

## 8. GitHub ecosystem survey

```bash
gh search repos cardputer --limit 100 --json fullName,description,stargazersCount,updatedAt,license,url
```
`executed-success` — returned **100, the API cap**, so the true count is higher.

```bash
gh api repos/BruceDevices/firmware --jq '"\(.full_name) ★\(.stargazers_count) \(.license.spdx_id) \(.pushed_at)"'
gh api repos/pr3y/Bruce            # -> redirects to BruceDevices/firmware
gh api repos/bmorcelli/M5Stick-Launcher  # -> redirects to bmorcelli/Launcher
gh api "search/code?q=repo:justcallmekoko/ESP32Marauder+cardputer" --jq '.total_count, (.items[].path)'
gh api repos/meshtastic/firmware/contents/variants --jq '.[].name' | grep -i card   # -> (none at top level)
gh api "search/code?q=repo:meshtastic/firmware+cardputer" --jq '.items[].path'
#   -> variants/esp32s3/m5stack_cardputer_adv/platformio.ini
```
`executed-success`. **Two upstreams have been renamed** — `pr3y/Bruce` and
`bmorcelli/M5Stick-Launcher`. Old links redirect but old *names* are what the community uses.

```bash
curl -s "https://raw.githubusercontent.com/BruceDevices/firmware/HEAD/boards/m5stack-cardputer/m5stack-cardputer.ini"
curl -s "https://raw.githubusercontent.com/meshtastic/firmware/HEAD/variants/esp32s3/m5stack_cardputer_adv/variant.h"
```
`executed-success`. `raw.githubusercontent.com` needs no auth and does not count against the API
limit — the right tool for file contents, per `hardware-doc/AGENTS.md`.

## 9. Reddit

```bash
UA='WhatsApp/2.23.20.0'
curl -sS -A "$UA" -G --data-urlencode "q=cardputer adv" --data-urlencode "sort=relevance" \
     --data-urlencode "limit=25" --data-urlencode "t=all" "https://old.reddit.com/search.json"
curl -sS -A "$UA" "https://old.reddit.com/comments/1vcxsv8.json?limit=20"
```
`executed-success`. `old.reddit.com` + that UA returns **200** where `www.reddit.com` returns
403 to plain clients — the technique from `AGENTS.md`, re-confirmed 2026-09-04.

## 10. Shopify

```bash
curl -sSg -A "$UA_BROWSER" \
  'https://shop.m5stack.com/search/suggest.json?q=cardputer&resources%5Btype%5D=product&resources%5Blimit%5D=10'
curl -sSg -A "$UA_BROWSER" 'https://shop.m5stack.com/products/m5stack-cardputer-adv-version-esp32-s3.json'
```
`executed-success`.

⚠ **Without `-g`, curl rejects the URL**: `curl: (3) bad range in position 68` — it parses
`[type]` as a glob range. Use `-g` or percent-encode the brackets. `executed-failed` on the
first attempt; recorded because the error message does not obviously point at the brackets.

## 11. Commands NOT executed

| Command | Why | Status |
|---|---|---|
| `pio run -e m5stack-cardputer` | no toolchain, no hardware | `not-tested` |
| `idf.py build` for the `CardputerADV` branch | no ESP-IDF 5.4.2 | `not-tested` |
| `python fetch_repos.py` (UserDemo) | would clone five more repos; pins recorded from `repos.json` instead | `not-tested` |
| `esptool.py write_flash …` | no hardware. Offsets in [`development.md`](development.md) are **inferred** from `partitions.csv` | `inferred` |
| M5Burner `/api/v1/firmwares/{id}` | **no firmware id resolved for the ADV** | not attempted |
| `curl …/1178/Easy_Loader_for_Cardputer-Adv.exe` | Windows binary; deferred | not attempted |
| `python3 tools/audit_archive.py` | nothing was archived by this pass | n/a |

## 12. Reusable scripts left in scratch

`archive/devices/m5stack/shared-artifacts/cardputer/`: `pdfbbox.py`, `pngcrop.py`, `h2t.py`, `dump.py`, `netlist.py`,
`pintable.py`. The first two are general-purpose and are candidates for promotion to
`hardware-doc/tools/` — `pdfbbox.py` in particular removes this repository's dependency on
`pdftotext` being installed, which the three existing `altium_pdf_*.py` tools assume.
