# Command ledger

> ESP32-P4-WIFI6-Touch-LCD-3.4C / 4C. Executed **2026-08-24** unless marked otherwise.
> Environment: Linux, bash. `UA` = `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36`

## Acquisition — `executed-success`

```bash
# Wiki pages (both variants)
curl -sSL -A "$UA" "https://www.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-3.4C" -o wiki-3.4C.html   # 200, 98314 B
curl -sSL -A "$UA" "https://www.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-4C"   -o wiki-4C.html     # 200, 98607 B

# Enumerate downloads from rendered HTML (API is broken - see below)
grep -oE 'https?://[^"'"'"' ]*\.(zip|7z|pdf|rar|bin|apk|exe)' wiki-3.4C.html | sort -u

# Shared XC artifacts
curl -sSL -A "$UA" -O "https://files.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-XC/ESP32-P4-WIFI6-Touch-LCD-XC-Schematic.pdf"
curl -sSL -A "$UA" -O "https://files.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-XC/ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip"

# Verify served size matches local bytes
curl -sSI -A "$UA" "<url>" | grep -iE 'HTTP|content-length|last-modified'
```

Results: schematic `HTTP 200` 1,869,787 B, `Last-Modified` 2025-05-26; demo `HTTP 200`
117,768,225 B, `Last-Modified` 2025-06-28. Both matched local sizes exactly.

## Validation — `executed-success`

```bash
file -b ESP32-P4-WIFI6-Touch-LCD-XC-Schematic.pdf   # "PDF document, version 1.3, 2 page(s)"
file -b ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip        # "Zip archive data, at least v2.0 to extract"
sha256sum *
```

Never trust the extension — both were validated by content magic.

## Tree digests — `executed-success`

Reusable, order-independent digest for a directory:

```bash
find . -type f -exec sha256sum {} + \
  | sed 's|^\(.\{64\}\)  \./|\1  |' | sort -k2 | sha256sum
```

> **Pitfall, learned the hard way.** An earlier form of this used
> `sed 's|.*<prefix>/||'`, which is greedy and strips the **hash column** as well as the path,
> silently producing a digest over paths only. Two "identical" trees then compare unequal for no
> reason. Always anchor with `^\(.\{64\}\)  `.

## PDF text extraction — `executed-success` (poor yield)

```bash
nix-shell -p poppler-utils --run 'pdftotext -layout in.pdf out.txt'
grep -oE "(ES8311|ES7210|CH34[0-9][A-Z]?|ESP32-[A-Z0-9-]+|MP[0-9]{4})" out.txt | sort -u
```

Recovered the fitted-parts list. **Did not** recover a usable net list — the schematic is a
2-page layout dump, so SD and touch-INT pins remain unresolved. Read it visually instead.

## Variant diff — `executed-success`

The command that established the entire 3.4C-vs-4C delta:

```bash
diff -u ESP-IDF/06_displaypanel_3.4inch/main/test_esp_lcd_jd9365.c \
        ESP-IDF/07_displaypanel_4inch/main/test_esp_lcd_jd9365.c
```

Output: resolution constants `800`→`720` and JD9365 register `0x40` `0x00`→`0x04`. Nothing else.

## Resolving multi-target `#ifdef` pins — `executed-success`

```bash
sed -n '20,70p' ESP-IDF/05_I2SCodec/main/example_config.h
```

Essential because the file carries ESP32/S2/S3/H2/P4 branches. Only the
`CONFIG_IDF_TARGET_ESP32P4` branch applies. A naive `grep '#define I2S_'` returns five
contradictory answers.

## Known failure — `executed-failed`

```bash
curl -sSL -A "$UA" "https://www.waveshare.com/wiki/api.php?action=parse&page=ESP32-P4-WIFI6-Touch-LCD-3.4C&prop=wikitext&format=json"
```

Returns `HTTP 200` with a **109-byte PHP fatal error**:

```
Parse error: syntax error, unexpected '?' in /yundisk/web/waveshare/dotcom/w/includes/Setup.php on line 472
```

**Diagnosis:** Waveshare's MediaWiki install is broken server-side; not a UA, rate-limit or
parameter problem. **Workaround:** parse the rendered HTML (see Acquisition above), which
recovered every download URL. **Consequence:** no immutable `oldid` pinning for Waveshare wiki
pages at present. → [C10](./gaps-and-conflicts.md#c10--waveshare-mediawiki-api-is-broken)

## Reading a schematic that has no usable text layer — `executed-success`

This is the method that resolved the microSD, touch and backlight pins after `pdftotext` failed.
It generalises to any vendor schematic exported as a layout dump.

```bash
# 1. Confirm geometry
pdfinfo sch.pdf                      # -> 2 pages, 842 x 595 pts (A4)

# 2. Render to images
pdftoppm -r 200 -png sch.pdf sch/pg  # -> pg-1.png 2339x1653, pg-2.png

# 3. Get word coordinates - used ONLY to locate regions, never to read the netlist
pdftotext -bbox-layout sch.pdf sch/bbox.xml

# 4. Find where a signal family lives (points; origin top-left)
python3 - <<'EOF'
import re
s=open('sch/bbox.xml',encoding='utf-8',errors='replace').read()
p=re.split(r'<page ',s)[1]
pat=re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" [^>]*>([^<]*)</word>')
for a,b,t in pat.findall(p):
    if re.match(r'(?i)^(TF|SD|CMD|CLK|D[0-3]|TP_|CTP)', t.strip()):
        print(f"({float(a):6.0f},{float(b):6.0f})  {t}")
EOF

# 5. Crop that region and read it.  px = pts * dpi/72   (here 200/72 = 2.7778)
magick pg-1.png -crop 260x140+1370+130 +repage -resize 500% -sharpen 0x1 crop.png
```

Then **look at `crop.png`**. Steps 1–4 only narrow the search; the mapping is read from the image.

### Why the text layer was useless

The board maps GPIOs to nets through **0 Ohm series resistors**, drawn as
`GPIOxx — Rnn 0R — NET_NAME` in three separate text runs at the same y coordinate. Extracted
linearly they interleave with hundreds of unrelated designators, so no grep recovers the pairing.
Read visually, the rows are obvious.

### Results

| Region | Crop (page 1) | Recovered |
|---|---|---|
| MicroSD | `556x334+1222+0` | D2=41, CD/D3=42, CMD=44, CLK=43, D0=39, D1=40, VDD switch=45 (AO3401) |
| LCD/touch FPC `P1` | `460x300+700+980` | 32-pin map; CTP_RESET, CTP_INT, CTP_SCL/SDA, DSI lanes, panel RESET |
| GPIO-to-net map | `230x120+620+1095` | GPIO27→RESET, GPIO33→BL_EN, GPIO23→TP_RST, GPIO26→LCD_BL_PWM, TP_INT→**TP2 test point** |

Cross-validation: GPIO27 (panel reset) and GPIO26 (backlight) match Waveshare's demo source
exactly, and GPIO7/8 (I²C) match too. Two independent sources agreeing is what makes these rows
**Confirmed** rather than merely *schematic*.


## Commercial-status probes — `executed-success`

```bash
for u in "https://www.waveshare.com/esp32-p4-wifi6-touch-lcd-4c.htm" \
         "https://www.waveshare.com/product/esp32-p4-wifi6-touch-lcd-4c.htm"; do
  curl -sSI -A "$UA" "$u" | head -1
done                       # both HTTP/2 404
curl -sSL -A "$UA" "https://www.waveshare.com/catalogsearch/result/?q=ESP32-P4-WIFI6-Touch-LCD" -o s.html
grep -oE 'ESP32-P4-WIFI6-Touch-LCD-[0-9.]+C' s.html | sort -u   # only "...-3.4C"
```

Negative results, deliberately retained — and **deliberately misread at the time**. They are
accurate observations that supported a wrong conclusion; see
[C2](./gaps-and-conflicts.md#c2--4c-availability--resolved-2026-08-24).

### The command that actually answered it — `executed-success`

The listing embeds its purchase options as JSON. Reading that, rather than probing for a
per-variant URL, settles availability in one step:

```bash
python3 - <<'EOF'
import re, html
s = open('prod-ESP32-P4-WIFI6-Touch-LCD-3.4C.html', encoding='utf-8', errors='replace').read()
m = re.search(r'\[\{"sku\s*":"\d+".{0,400}?\]', s)
print(html.unescape(m.group(0)))
EOF
```

Output:

```json
[{"sku":"31523","attributes":["3.4inch Round Touch Display (800 × 800 pixels)"],"unsaleable":false},
 {"sku":"31522","attributes":["4inch Round Touch Display (720 × 720 pixels)"],"unsaleable":false}]
```

**Generalisable lesson:** on a storefront, check the listing's own **option/SKU data** before
concluding anything from a `404` on a guessed product URL. The page had been downloaded hours
earlier; the answer was already on disk.

## Not executed — `not-tested`

No build, flash, or hardware command was run. Everything in
[`development.md`](./development.md) is **inferred** from standard ESP-IDF practice and is
labelled as such there. In particular the **ESP32-C6 firmware flash procedure is unknown** and no
offsets should be guessed.
