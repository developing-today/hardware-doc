# Command ledger — Waveshare ESP32-S3-ePaper-3.97

> Every command that produced a fact in this record, plus the ones that failed.
> Status vocabulary: `executed-success` · `executed-failed` · `reported-working` ·
> `inferred` · `not-tested`.
>
> Environment for all `executed-*` rows: Linux, bash, `curl 8.x`,
> `python3 3.14.7`, `gh` authenticated. Working directory
> `hardware-doc/scratch/waveshare-epaper-esp32/` unless noted.
> Date: **2026-09-01**.
>
> **No command in this file was run against hardware.** There is no board.

## 0. Shared setup

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
```

A browser User-Agent is required on `www.waveshare.com`; the default `curl/*` agent
is intermittently blocked. Per this repository's
[AGENTS.md](../../../AGENTS.md) rule, the plain request was tried first — it worked
for `files.waveshare.com` and `docs.waveshare.com`, and the UA was set uniformly
anyway because the vendor guide already records the need.
Status: `executed-success`.

## 1. Product enumeration

**Purpose:** find every ESP32 e-paper product Waveshare currently sells.

```bash
curl -sSL -A "$UA" --max-time 90 \
  'https://www.waveshare.com/catalogsearch/result/?q=e-paper+esp32&limit=200' \
  | grep -oE 'https://www\.waveshare\.com/[a-zA-Z0-9.\-]+\.htm' | sort -u
```

Six query families were run: `e-paper esp32`, `epaper esp32-s3`, `photopainter`,
`e-paper driver board`, `esp32 e-ink`, `e-paper esp32 development board`.
Result: **seven** ESP32 e-paper products. `esp32 e-ink` returned **nothing** — the
storefront does not index "e-ink" as a synonym, worth knowing.
Status: `executed-success`.

**Negative result, recorded because it cost time:**

```bash
curl -sS -A "$UA" 'https://www.waveshare.com/product/displays/e-paper.htm' \
  | grep -c 'product-item'      # -> 0
```

The category page returns **HTTP 200, 244 758 bytes, and zero product links** — the
grid is JS-rendered. **Use `/catalogsearch/result/?q=` to enumerate, never the
category page.** Status: `executed-success` (as a negative result).

## 2. SKU and price extraction

**Purpose:** the first pass on this board recorded price as "not established".
It is in the markup.

```bash
python3 - <<'EOF'
import re, html
s = open('survey/esp32-s3-epaper-3.97.html', encoding='utf-8', errors='replace').read()
print(sorted(set(re.findall(r'class="price"[^>]*>\s*\$?([\d,.]+)', s))))
m = re.search(r'waveshare_sku_attributes\s*=\s*(\[.*?\]);', s, re.S)
print(html.unescape(m.group(1)))
EOF
```

Output:

```
['0.00', '34.99', '47.99']
[{"sku ":"33552","attributes":["With Lithium Batt"],"unsaleable":false},
 {"sku ":"33810","attributes":["Without Lithium Batt"],"unsaleable":false},
 {"sku ":"33811","attributes":["Basic Kit (Lithium Batt + TF Card + Card Reader)"],"unsaleable":false}]
```

Note the key is **`"sku "` with a trailing space** — a regex for `"sku"` misses it
entirely, which is the likeliest reason the first pass found no price. The
`unsaleable:false` flags establish availability.
Status: `executed-success`. Extends [vendor guide §8.6](../../../vendors/waveshare/README.md).

## 3. Documentation retrieval

```bash
curl -sSL -A "$UA" -o docs-overview.html   'https://docs.waveshare.com/ESP32-S3-ePaper-3.97'
curl -sSL -A "$UA" -o docs-resources.html  'https://docs.waveshare.com/ESP32-S3-ePaper-3.97/Resources-And-Documents'
```

Both **HTTP 200**. Docusaurus v3.10.2, **server-rendered** — the text is in the HTML
and needs no browser. Status: `executed-success`.

Sub-page slugs follow `https://docs.waveshare.com/<PRODUCT>/<Section>`; the sections
are discoverable by grepping the overview page:

```bash
grep -oE 'ESP32-S3-ePaper-3\.97/[A-Za-z0-9\-]+' docs-overview.html | sort -u
# -> Arduino, ESP-IDF, ESP32-AI-Tutorials, FAQ, Firmware-Flashing,
#    Resources-And-Documents, Technical-Support
```

**Failed, recorded:**

```bash
curl -sSL -A "$UA" -o /dev/null -w '%{http_code}\n' \
  'https://www.waveshare.com/wiki/ESP32-S3-ePaper-3.97'          # 404
curl -sSL -A "$UA" -o /dev/null -w '%{http_code}\n' \
  'https://docs.waveshare.com/E-Paper-ESP32-Driver-Board'        # 404
```

The two hosts are **disjoint**: new products on `docs.`, older ones on `/wiki/`.
Status: `executed-success` (negative results).

## 4. Artifact download and validation

```bash
dl() { curl -sSL -A "$UA" --max-time 300 -o "$2" -w '%{http_code} %{size_download} %s\n' "$1"; }

dl 'https://files.waveshare.com/wiki/ESP32-S3-ePaper-3.97/ESP32-S3_e-Paper-3.97-schematic.pdf' schematic.pdf
dl 'https://files.waveshare.com/wiki/3.97inch_e-Paper_HAT%2B/3.97inch_e-Paper.pdf'             panel.pdf
dl 'https://files.waveshare.com/wiki/common/ES8311.DS.pdf'                                     es8311.pdf
dl 'https://files.waveshare.com/wiki/common/Pcf85063atl1118-NdPQpTGE-loeW7GbZ7.pdf'            pcf85063.pdf
dl 'https://files.waveshare.com/wiki/common/SHTC3_Datasheet.pdf'                               shtc3.pdf
dl 'https://raw.githubusercontent.com/lewisxhe/XPowersLib/master/datasheet/AXP2101_Datasheet_V1.4_en.pdf' axp2101.pdf
```

**Validation — by magic bytes, never by status code:**

```bash
for f in *.pdf; do
  printf '%-45s %-10s ' "$f" "$(stat -c%s "$f")"
  head -c 5 "$f" | od -c | head -1
done
sha256sum *.pdf
```

All six begin `%PDF-`. Hashes are in [`sources.md`](sources.md).
Status: `executed-success`.

**Two failures, both correctly rejected:**

```bash
curl -sSL -A "$UA" -o axp.tmp 'https://files.waveshare.com/wiki/common/AXP2101.pdf'
head -c 5 axp.tmp   # -> '<?xml'   HTTP 404
curl -sSL -A "$UA" -o axp.tmp \
  'https://github.com/lewisxhe/XPowersLib/raw/master/datasheet/AXP2101_Datasheet_V1.0_en.pdf'
head -c 5 axp.tmp   # -> newlines (HTML)   HTTP 404, 267 330 bytes
rm -f axp.tmp
```

Note the second returned **267 KB of HTML** — a plausible-looking size that would
have passed any length check. **Neither was retained under a `.pdf` name.**
Status: `executed-failed`, correctly handled.

The working filename was found by listing the directory through the API rather than
guessing:

```bash
curl -sS -H "Authorization: Bearer $(gh auth token)" \
  'https://api.github.com/repos/lewisxhe/XPowersLib/contents/datasheet'
```

Status: `executed-success`.

## 5. Schematic text extraction

**The problem:** no `pdftotext`, `pdftoppm`, `mutool`, `qpdf`, `pypdf`, `pymupdf` or
`pdfminer` on this host, and no `pip`. The repository's own
`tools/altium_pdf_netlist.py` needs `pdftotext -bbox` XML as input, so it could not
be used directly.

```bash
which pdftotext pdftoppm mutool qpdf   # -> nothing
python3 -c 'import pypdf'              # -> ModuleNotFoundError
pip install pypdf                      # -> pip: command not found
```

Status: `executed-failed`. **This is why `tools/pdftext.py` exists.**

**Step 1 — diagnose the PDF.** A naive page-content walker returns zero text:

```bash
python3 tools/pdftext.py dl/ESP32-S3_e-Paper-3.97-schematic.pdf | wc -l   # -> 0
```

Which looks exactly like "no text layer" and is **wrong**. The whole sheet lives in a
**Form XObject**, not in `/Contents`:

```bash
python3 - <<'EOF'
import sys; sys.path.insert(0,'tools')
from pdftext import objects, inflate
data = open('dl/ESP32-S3_e-Paper-3.97-schematic.pdf','rb').read()
for num,gen,dic,raw in objects(data):
    if raw is None: continue
    d = inflate(dic, raw)
    print(num, len(raw), len(d) if d else None, d.count(b'BT') if d else 0)
EOF
# object 5: /Subtype /Form, 62 453 -> 447 937 bytes inflated, 1 158 BT blocks
```

Status: `executed-success`. **Generalisable finding — see
[vendors/waveshare](../../../vendors/waveshare/README.md).**

**Step 2 — extract and reflow.** Altium emits one glyph per `Tj` with its own `Tm`,
so raw extraction gives 4 318 single characters and 170 distinct strings:

```bash
python3 - > sch.tsv <<'EOF'
import sys; sys.path.insert(0,'tools')
from pdftext import objects, inflate, extract
data = open('dl/ESP32-S3_e-Paper-3.97-schematic.pdf','rb').read()
for num,gen,dic,raw in objects(data):
    if raw is None: continue
    d = inflate(dic, raw)
    if d and d.count(b'BT') > 50:
        for x,y,t in extract(d):
            print(f'{num}\t{x}\t{y}\t{t}')
EOF

python3 tools/reflow.py sch.tsv 1.2 4.5 > sch-words2.tsv
wc -l sch-words2.tsv     # 1 150 tokens
cut -f3 sch-words2.tsv | sort -u | wc -l   # 628 distinct
```

Status: `executed-success`. Output retained as
`artifacts/schematic/schematic-text-reflowed.tsv`.

**Step 3 — read the allocation table** (columns are x-bands):

```bash
awk -F'\t' '$1<166 && $1>35 && $2>150 && $2<425' sch-words2.tsv | sort -k1,1gr
```

Produces the GPIO table transcribed in [`pinouts-and-buses.md`](pinouts-and-buses.md).
Status: `executed-success`.

**Step 4 — the PMIC:**

```bash
rg -n 'AXP2101|TG28|ALDO|BLDO|DLDO|CPUSLDO|PWRON' sch-words2.tsv
# 381:  358.19  210.28  AXP2101      <- and no occurrence of TG28 anywhere
```

Status: `executed-success`. Settles [C-WS2](gaps-and-conflicts.md#c-ws2--tg28-versus-axp2101).

## 6. Panel manual — validating a hostile text layer

The manual's text layer is **human-legible but wrong** if read naively — the exact
failure the method warns about. Raw extraction yields `LQFKH 3DSHU`.

```bash
python3 - <<'EOF'
# Determine the offset from a KNOWN heading: the cover reads "3.97inch e-Paper".
enc = 'LQFKH'; want = 'inche'
print({ord(w)-ord(e) for e,w in zip(enc,want)})    # -> {29}
EOF
```

A single uniform offset of **+29** across letters *and* digits, and a second subset
font at **+26**. Decoder: `tools/deshift.py`.

```bash
python3 tools/deshift.py panel.tsv > panel-dec.txt
rg -i '3\.97inch|e-Paper' panel-dec.txt | head -3      # validation against the heading
rg -i 'driver ic|SSD1' panel-dec.txt
# 66:151  509.4  4-1:Displaymodule3.97«arrayforEPD;4-2:DriverIC:SSD1677;
```

**Only after the heading validated was any value transcribed.** Status:
`executed-success`. This is the method's PDF-text-layer rule applied literally, and
it is what produced the SSD1677 identification.

## 7. Vendor source

```bash
TOKEN=$(gh auth token)
H=(-H "Authorization: Bearer $TOKEN" -H 'Accept: application/vnd.github+json')
SHA=9b12d40731a80213b927ee8a421cae4082952819

curl -sS "${H[@]}" 'https://api.github.com/repos/waveshareteam/ESP32-S3-ePaper-3.97'
curl -sS "${H[@]}" "https://api.github.com/repos/waveshareteam/ESP32-S3-ePaper-3.97/git/trees/$SHA?recursive=1"
# 1 217 entries, truncated=false

curl -sSL -H "Authorization: Bearer $TOKEN" -H 'Accept: application/vnd.github.raw' \
  "https://api.github.com/repos/waveshareteam/ESP32-S3-ePaper-3.97/contents/ESP-IDF/08_ESP32-S3_e-Paper-3.97/components/axpPower/axp_prot.cpp?ref=$SHA"
```

Authenticating with `gh auth token` avoids the 60 req/hour anonymous limit, per the
[`web-retrieval-fallback`](../../../.agents/skills/) guidance.
Status: `executed-success`.

**Pin-map cross-check** — this is the step that makes the pinout trustworthy:

```bash
curl … contents/Arduino/examples/02_E-Paper_Example/DEV_Config.h?ref=$SHA | grep -E 'EPD_.*_PIN'
# EPD_SCK_PIN 11 / EPD_MOSI_PIN 12 / EPD_CS_PIN 10
# EPD_RST_PIN 46 / EPD_DC_PIN 9  / EPD_BUSY_PIN 3
```

All six match the schematic's allocation table. Status: `executed-success`.

## 8. Duplicate detection against the existing knowledge base

```bash
sha256sum components/nxp/pcf85063a/artifacts/*.pdf
# a09223db…  pcf85063a-datasheet.pdf              726 288 B  (already held, NXP, Rev. 7)
sha256sum dl/PCF85063ATL.pdf
# 93b38487…                                        535 722 B  (new, Waveshare, Rev. 6)
```

Different hash **and** different size → per the method, **keep both and investigate**.
Revisions extracted from each PDF confirmed Rev. 7 (2018) vs Rev. 6 (2015).
Status: `executed-success`. See
[C-WS11](gaps-and-conflicts.md#c-ws11--waveshare-mirrors-a-nine-year-old-rtc-datasheet).

## 9. Not run — and why

| Command | Why not | Where recorded |
|---|---|---|
| `git clone` of the vendor repo | ~50 MB; API reads answered the questions asked | [G2](gaps-and-conflicts.md#gaps) |
| Download of `260304.bin` / `260314.bin` | 2 × 16 MB, plus 21 MB of xiaozhi images | [G3](gaps-and-conflicts.md#gaps), [manifest](acquisition/manifest.json) |
| `tools/esp_image_info.py` on the firmware | Depends on the download above | [G3](gaps-and-conflicts.md#gaps) |
| Any `esptool` operation | **No hardware.** The flash command in [`development.md`](development.md) is labelled `inferred` and must not be run unverified | [development.md](development.md#flashing) |
| Rendering schematic page 1 | No rasteriser available on this host | [G1](gaps-and-conflicts.md#gaps) |
