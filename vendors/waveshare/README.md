# Waveshare — Documentation Sourcing Guide

Reusable, cross-device knowledge for exhaustively acquiring documentation and artifacts for **any**
Waveshare product. Written from a full acquisition pass on `ESP32-S3-Knob-Touch-LCD-1.8`
(see `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/`), but the patterns generalise.

> **TL;DR** — The MediaWiki **wikitext** (`action=parse&prop=wikitext`) is the authoritative source of
> truth for a product's download set, not the rendered HTML. Pin the revision with an `oldid`, and use
> `api.php` rather than `index.php` because Waveshare's WAF blocks the `oldid`/`action=history` query
> params on `index.php`.

---

## 1. Site topology and URL patterns

Waveshare runs three distinct properties. Knowing which one holds what saves a lot of time.

| Host | Role | Notes |
|---|---|---|
| `www.waveshare.com/<product-slug>.htm` | Magento storefront product page | Marketing specs, gallery photos, price, "Resources" tab |
| `www.waveshare.com/wiki/<Product_Name>` | MediaWiki documentation | **The real documentation.** Pinouts, tutorials, download links |
| `files.waveshare.com/...` | Static file CDN | All ZIPs/PDFs. **No directory listing** |

### Canonical URL forms

```
# Storefront product page (slug is lowercase, dots retained, spaces -> hyphens)
https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm

# Wiki page (Title_Case_With_Underscores; product names usually keep their exact casing)
https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8

# Product-specific downloads
https://files.waveshare.com/wiki/<Product_Name>/<file>
https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip

# Shared/common downloads (datasheets for onboard ICs, PC tools) — CHECK THIS, it is easy to miss
https://files.waveshare.com/wiki/common/<file>
https://files.waveshare.com/wiki/common/Esp32-s3_datasheet_en.pdf

# Legacy upload path (older products)
https://files.waveshare.com/upload/<a>/<ab>/<file>

# Wiki image originals (MediaWiki content-addressed layout)
https://www.waveshare.com/w/upload/<a>/<ab>/<Filename>
https://www.waveshare.com/w/upload/thumb/<a>/<ab>/<Filename>/<N>px-<Filename>   # thumbnail

# Storefront gallery images (Magento cache; the size segment is substitutable)
https://www.waveshare.com/media/catalog/product/cache/1/image/800x800/9df78eab33525d08d6e5fb8d27136e95/e/s/<slug>-1.jpg
#                                                      ^^^^^^^  swap for 264x, 560x560, 1000x1000 ...

# MediaWiki entry points
https://www.waveshare.com/w/api.php          # ✅ works, use this
https://www.waveshare.com/w/index.php        # ⚠️ works bare, but 404s with oldid/action params
https://www.waveshare.com/wiki/Special:AllPages
https://www.waveshare.com/wiki/Special:Categories
```

### The `oldid` gotcha (important)

The documented immutable-revision URLs **do not work** on Waveshare:

```
https://www.waveshare.com/w/index.php?title=<Page>&oldid=<N>    -> HTTP 404
https://www.waveshare.com/w/index.php?title=<Page>&action=history -> HTTP 404
https://www.waveshare.com/wiki/<Page>?oldid=<N>                 -> HTTP 404
https://www.waveshare.com/w/index.php?title=<Page>              -> HTTP 200 (bare title is fine)
```

Their CDN/WAF strips or rejects those query parameters. **Use the API instead** — it is unfiltered:

```bash
# Pinned, immutable revision: rendered HTML + raw wikitext in one call
curl -sS 'https://www.waveshare.com/w/api.php?action=parse&oldid=111069&prop=text|wikitext|revid&format=json'

# Revision history
curl -sS 'https://www.waveshare.com/w/api.php?action=query&prop=revisions&titles=<Page>&rvlimit=100&rvprop=ids|timestamp|user|comment|size&format=json'
```

Record the `revid` in your `sources.md`. Waveshare edits wiki pages in place **without any version
bump or changelog on the page itself**, so an unpinned citation is worthless.

---

## 2. Typical artifact set

What you can usually expect per product. Absence is common — probe, don't assume.

| Artifact | Typical name | Notes |
|---|---|---|
| Schematic | `<Product>-schematic.zip` | **Usually PNG sheets, not PDF.** Gerbers/BOM are rare |
| Demo / examples | `<Product>-Demo.zip` | Arduino + ESP-IDF trees. **Often 50–100 MB** — vendored LVGL, ESP components |
| Factory firmware | `<Product>-BIN.zip` | Prebuilt `.bin` + flash offsets, for restoring the shipped demo |
| Dimension drawing | Often only a **wiki PNG**, not a PDF | Look for images named `...-21.png`, `...-42.png` etc. |
| User manual | Rare for dev boards | The wiki page *is* the manual |
| Product images | Wiki `/w/upload/` + storefront `/media/catalog/` | Two disjoint sets — collect both |
| IC datasheets | `files.waveshare.com/wiki/common/*.pdf` | Third-party datasheets re-hosted by Waveshare |
| PC tools | `files.waveshare.com/wiki/common/*.zip` | SSCOM, CH34x drivers, AIDA64 remote, mjpeg converter |
| 3D / STEP | Rare | Probe `-3D.zip`, `.step`, `-STEP.zip`; usually 404 |

---

## 3. How to enumerate *every* download for a product

Ordered by reliability. Do **all** of them; each catches things the others miss.

### Step 1 — Get the wikitext (highest yield)

Rendered HTML misses links hidden in collapsed sections, templates, and tabbed panes. On the
Knob-LCD board, `Sscom5.13.1.zip` appeared **only** in wikitext, never in the rendered anchors.

```bash
curl -sS 'https://www.waveshare.com/w/api.php?action=parse&page=<Page>&prop=wikitext&format=json' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["parse"]["wikitext"]["*"])' > page.wiki

grep -oiE 'https?://files\.waveshare\.com[^ )|}<>"]*' page.wiki | sort -u
grep -oiE 'https?://[^ )|}<>"]*\.(zip|pdf|7z|rar|exe|step|stp|dxf|xlsx?)' page.wiki | sort -u
```

### Step 2 — Enumerate images via the API, not by scraping `<img>`

Scraped `src` attributes give you **thumbnails** (`/w/upload/thumb/.../600px-Foo.png`). You want the
originals. The API resolves them and gives size/mime/sha1 for free:

```bash
# list image titles on the page
curl -sS 'https://www.waveshare.com/w/api.php?action=query&prop=images&titles=<Page>&imlimit=500&format=json'
# then batch-resolve (<=50 titles per call)
curl -sS 'https://www.waveshare.com/w/api.php?action=query&prop=imageinfo&iiprop=url|size|mime|sha1&format=json&titles=File:A.png|File:B.png'
```

Note wiki pages frequently embed **shared tutorial figures from other products** (e.g. an
`ESP32-S3-AMOLED-1.91-*` screenshot on a Knob-LCD page). Separate board-specific images from shared
ones so your manifest doesn't imply the wrong provenance.

### Step 3 — Scrape the storefront page separately

The gallery images live only on the storefront and are a different photo set from the wiki:

```bash
curl -sS -A 'Mozilla/5.0' 'https://www.waveshare.com/<slug>.htm' \
  | grep -oE 'media/catalog/product/cache/[^"]*<slug>-[0-9]+\.jpg' | sort -u
```

Then request the largest cache size (`800x800`, sometimes `1000x1000`) rather than the `264x` thumb.

### Step 4 — Probe for undiscovered files

`files.waveshare.com` has **no directory index** (a request for the directory returns 200 with empty
body — it is not a listing). Filenames must be discovered from the wiki, or guessed:

```bash
P=https://files.waveshare.com/wiki/<Product_Name>
for f in "<Product>-3D.zip" "<Product>.step" "<Product>-Gerber.zip" "<Product>-BOM.xlsx" \
         "<Product>-UserManual.pdf" "<Product>-Datasheet.pdf" "<Product>-SDK.zip"; do
  printf '%-46s ' "$f"; curl -sSI -A 'Mozilla/5.0' -o /dev/null -w '%{http_code}\n' "$P/$f"
done
```

### Step 5 — Check sibling / platform-mate products

Waveshare copy-pastes wiki pages across a product family. A sibling board sharing the SoC often has a
**better-written** version of the same tutorial, or an extra download. Find them via
`/wiki/Special:AllPages`, the storefront category page, or the "you may also like" rail on the
product page.

### Step 6 — Chinese-language variants

Sometimes richer than the English page. **Verify before citing** — for the Knob-LCD board all of these
404'd:

```
https://www.waveshare.net/wiki/<Product>          # .net is the CN storefront
https://www.waveshare.net/shop/<Product>.htm
https://www.waveshare.com/wiki/<Product>/zh
```

---

## 4. Gotchas

- **Specs disagree between sources.** The storefront page, wiki, schematic, and demo code routinely
  name different driver ICs for the same part. **Trust order: schematic > demo source > wiki >
  storefront.** Record the conflict rather than silently picking one.
- **Connector series are named loosely.** "FPC connector", "1.25mm connector" etc. are often
  approximations. Measure from the schematic/mechanical drawing before ordering mating parts.
- **Demo archives bundle third-party code with mixed licenses.** A `-Demo.zip` typically vendors
  LVGL (MIT), Espressif components (Apache-2.0), and unattributed vendor BSP code with no license
  header at all. Do not assume the archive as a whole is redistributable.
- **Wiki pages are edited in place with no version bump.** Always pin an `oldid`.
- **No directory listing on `files.waveshare.com`.** Filenames come from wiki HTML/wikitext only.
- **`index.php` + `oldid`/`action` → 404.** Use `api.php` (see §1).
- **Rendered HTML hides downloads** in collapsed/tabbed sections. Parse wikitext (see §3 Step 1).
- **Scraped image `src` are thumbnails.** Use `imageinfo` for originals.
- **Image rights are unclear.** Waveshare asserts copyright and publishes no license. Treat all
  images and PDFs as *retained for internal reference*, not redistributable.
- **Re-hosted third-party PDFs may be stale.** `Esp32-s3_datasheet_en.pdf` on Waveshare can lag the
  current Espressif release. Prefer the primary vendor for the authoritative revision; keep
  Waveshare's copy only to document *what Waveshare shipped*.
- **A `.pdf`/`.zip` URL can return an HTML error page with HTTP 200.** Always validate by magic bytes.

---

## 5. Validation

Never trust the extension or the status code alone.

```bash
# magic-byte check
head -c 4 file.pdf | od -c | head -1     # %PDF
head -c 4 file.zip | od -c | head -1     # PK 003 004
head -c 4 file.7z  | od -c | head -1     # 7 z 274 257
file file.*                              # if available
```

Reject anything starting with `<!DOCTYPE` / `<html`. Record `sha256` + byte size for every retained
artifact so later re-fetches can be diffed against the pinned revision.

---

## 6. Concrete curl recipes

```bash
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36'
PAGE='ESP32-S3-Knob-Touch-LCD-1.8'
API='https://www.waveshare.com/w/api.php'

# 1. current revid
curl -sS -A "$UA" "$API?action=query&prop=revisions&titles=$PAGE&rvlimit=1&rvprop=ids|timestamp&format=json"

# 2. pinned snapshot (html + wikitext)
curl -sS -A "$UA" "$API?action=parse&oldid=111069&prop=text|wikitext|revid&format=json" -o wiki-oldid-111069.json

# 3. all image originals
curl -sS -A "$UA" "$API?action=query&prop=images&titles=$PAGE&imlimit=500&format=json"

# 4. a product download (follow redirects, generous timeout — Demo zips are huge)
curl -sSL --max-time 600 -A "$UA" -O \
  "https://files.waveshare.com/wiki/$PAGE/$PAGE-Demo.zip"

# 5. storefront page
curl -sSL -A "$UA" -o product.html "https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm"
```

A `User-Agent` is required — the default `curl/*` UA gets intermittently blocked on `www.`.
`files.waveshare.com` is more permissive but set it anyway.

---

## 7. Checklist

Per product, work top to bottom:

- [ ] Resolve storefront slug + wiki page title
- [ ] Fetch current `revid`; record it
- [ ] Snapshot wiki at pinned `oldid` (HTML **and** wikitext) via `api.php`
- [ ] Snapshot revision history (API JSON)
- [ ] Snapshot storefront product page HTML
- [ ] Extract all `files.waveshare.com` links from **wikitext** (not just HTML)
- [ ] Check `files.waveshare.com/wiki/common/` links — IC datasheets and PC tools
- [ ] Enumerate wiki images via `imageinfo`; download **originals**, not thumbs
- [ ] Separate board-specific images from shared tutorial figures
- [ ] Scrape storefront gallery images at max cache size
- [ ] Probe for `-3D.zip` / `.step` / `-Gerber.zip` / `-BOM.xlsx` / `-UserManual.pdf`
- [ ] Check sibling/platform-mate product wikis for extras
- [ ] Check `waveshare.net` / `/zh` Chinese variants
- [ ] Validate every file by magic bytes; reject HTML-as-PDF/ZIP
- [ ] Record name / bytes / sha256 / source URL / retrieval date for each artifact
- [ ] Note rights status (Waveshare's; redistribution unclear)
- [ ] Log every failure and every 404 probe in `component-download-failures.txt`

---

## 8. Findings added 2026-08-24 → 2026-08-26 (ESP32-P4-WIFI6-Touch-LCD-XC)

### 8.1 The MediaWiki API is broken — use rendered HTML

`https://www.waveshare.com/wiki/api.php?action=parse&…` returns **`HTTP 200` with a PHP fatal
error**, not JSON:

```
Parse error: syntax error, unexpected '?' in /yundisk/web/waveshare/dotcom/w/includes/Setup.php on line 472
```

So §3's wikitext-enumeration method **does not currently work**. Workaround that does:

```bash
curl -sSL -A "$UA" "https://www.waveshare.com/wiki/<PRODUCT>" -o wiki.html
grep -oE 'https?://[^"'"'"' ]*\.(zip|7z|pdf|rar|bin|apk|exe)' wiki.html | sort -u
```

This recovered **every** download link. Consequence: no immutable `oldid` pinning is available;
snapshot the rendered HTML instead.

### 8.2 There is a newer documentation platform

**`https://docs.waveshare.com/<PRODUCT>`** — a modern, working, bilingual site that the legacy
wiki does not link prominently. It carried details the wiki omitted (SKUs, "dual microphones",
"40-pin requires pin header adapter", a vendor warning against Arduino on ESP32-P4).

**Check it first.** Note `docs.waveshare.com/zh/<PRODUCT>` returns `404` — Chinese content is not
served from a `/zh/` path.

### 8.3 `waveshare.net` (CN) is not a translation of `waveshare.com` (EN)

They are **different content**, and the Chinese site is often **more technically specific**.

| Host | Example |
|---|---|
| `waveshare.com` | "40PIN GPIO header" |
| `waveshare.net` | "板上引出 2 * 20 排座，引出 **28** 个剩余可编程 GPIO 接口" |

For the XC boards, the CN storefront was the **only** source giving the GPIO count, the 170°
viewing angle and the optically bonded tempered glass panel. The GPIO count independently
corroborated a schematic-derived pinout.

**Always check both hosts:**

```
https://www.waveshare.com/<product>.htm          # EN store
https://www.waveshare.net/shop/<PRODUCT>.htm     # CN store
https://www.waveshare.net/wiki/<PRODUCT>         # CN wiki
```

### 8.4 Waveshare maintain official GitHub repositories

**`https://github.com/waveshareteam/<PRODUCT>`** — neither the wiki nor the demo ZIP mentions
these, yet they are strictly better sources:

- **Apache-2.0 licensed**, where the demo ZIP ships no `LICENSE` at all
- CI-tested against declared framework versions
- Include `docs/`, factory firmware, and the schematic
- Often name a **published BSP component** on the Espressif registry
  (e.g. `waveshare/esp32_p4_wifi6_touch_lcd_xc`)

**Search GitHub for the product before deep artifact analysis.** Doing so late in the XC research
meant hand-extracting facts that were already written down.

### 8.5 A shared file pool means shared artifacts

Two patterns to recognise:

- `files.waveshare.com/wiki/common/…` — shared across **many** products; stable, and a 404 on a
  product page does not remove it.
- `files.waveshare.com/wiki/<FAMILY>/…` where `<FAMILY>` is a wildcard such as
  `ESP32-P4-WIFI6-Touch-LCD-**XC**` — one schematic and one demo ZIP covering **several** boards.
  Store such artifacts once rather than per-device.

### 8.6 Absence of a product page ≠ absence of a product

Waveshare sell variants as **Version Options on one listing**. During XC research a `404` on a
guessed per-variant URL, plus a catalogue search returning one result, briefly led to the wrong
conclusion that a board might not exist.

The listing's own embedded JSON settled it:

```bash
python3 -c "import re,html; s=open('product.html',encoding='utf-8',errors='replace').read(); \
m=re.search(r'\[\{"sku\s*":"\d+".{0,400}?\]',s); print(html.unescape(m.group(0)))"
# [{"sku":"31523",...,"unsaleable":false},{"sku":"31522",...,"unsaleable":false}]
```

**Read the listing's SKU/option data before inferring anything from a missing URL.**

### 8.7 Schematics have no usable text layer

Waveshare schematic PDFs are layout dumps. GPIO-to-net mapping goes through **0 Ω series
resistors** drawn as three separate text runs at one y-coordinate, so no grep recovers the pairing.
Render and read visually; use `pdftotext -bbox-layout` only to locate regions.

Also: for the XC schematic, **page 2 is the PCB layout, not circuitry**. All circuit detail is on
page 1.

## 9. Findings added 2026-09-01 (ESP32-S3-ePaper-3.97)

Source: [`ESP32-S3-ePaper-3.97`](../../devices/waveshare/esp32-s3-epaper-3.97/README.md).
Two of these **correct earlier sections of this guide**; they are dated rather than
silently overwritten.

### 9.1 ⚠ The two documentation hosts are *disjoint*, not layered — and this cost a whole pass

§8.2 already says to check `docs.waveshare.com` first. **That is not strong enough.**
The observed rule is:

| Product era | `docs.waveshare.com/<PRODUCT>` | `waveshare.com/wiki/<Product>` |
|---|---|---|
| Newer (e.g. `ESP32-S3-ePaper-3.97`, `ESP32-S3-ePaper-1.54`, `ESP32-C6-ePaper-1.54`) | **200** | **404** |
| Older (e.g. `E-Paper_ESP32_Driver_Board`) | **404** | **200** |

**A 404 on one host says nothing about the product.** In this pass a first attempt
tested only the legacy wiki, got a 404, and concluded the vendor publishes *no
documentation, no schematic, no pinout, no sample code and no panel controller* for
the board. **All of those were false** — the docs site carried a schematic, a panel
manual, four IC datasheets and a link to an official example repository.

**Always probe both hosts before recording an absence.**

```bash
for h in "https://docs.waveshare.com/$P" "https://www.waveshare.com/wiki/$P"; do
  printf '%-70s ' "$h"; curl -sSL -A "$UA" -o /dev/null -w '%{http_code}\n' "$h"
done
```

The new platform is Docusaurus and **server-renders its text**, so `curl` + strip-tags
is sufficient; no browser needed. Sub-pages follow
`docs.waveshare.com/<PRODUCT>/<Section>`, discoverable with:

```bash
grep -oE "$P/[A-Za-z0-9\-]+" docs.html | sort -u
# -> Arduino, ESP-IDF, FAQ, Firmware-Flashing, Resources-And-Documents, Technical-Support …
```

**`Resources-And-Documents` is the single highest-yield page per product** — it is the
new equivalent of the old wiki's Resources section, and it lists the schematic, the
panel datasheet, the onboard-IC datasheets, the GitHub repo and community projects.

### 9.2 ⚠ Correction to §8.7 — schematic PDFs *do* have a usable text layer

§8.7 states Waveshare schematics "have no usable text layer" and must be read
visually. **For the ESP32-S3-ePaper-3.97 schematic that is wrong**, and the reason a
naive attempt fails is worth knowing:

1. **The sheet lives in a Form XObject, not in `/Contents`.** A page-content walker
   returns **zero** text and looks exactly like "no text layer". The content was in
   one object: 62 KB compressed → 448 KB inflated → 1 158 `BT` blocks.
2. **Altium emits one glyph per `Tj`, each with its own `Tm`.** Raw extraction gives
   4 318 single characters and 170 distinct strings — useless to `grep`, which is
   presumably how the original "no usable text layer" conclusion was reached.
3. **Reflowing by baseline recovers real tokens.** Grouping by `y`, sorting by `x` and
   joining runs under a gap threshold produced **1 150 tokens / 628 distinct**,
   including every net label, part label and — critically — an entire **GPIO
   allocation table** drawn on the sheet.

Tools that do this, kept beside the device record and reusable for any Waveshare
Altium export:

- [`pdftext.py`](../../devices/waveshare/esp32-s3-epaper-3.97/tools/pdftext.py) — inflates every stream **including Form XObjects**, interprets `BT`/`Tm`/`Td`/`Tj`/`TJ`
- [`reflow.py`](../../devices/waveshare/esp32-s3-epaper-3.97/tools/reflow.py) — glyph → word reassembly

These need no poppler, no `pypdf`, no `pip` — which mattered, because none was
available. The repo's own `tools/altium_pdf_netlist.py` is better where
`pdftotext -bbox` **is** available; these are the fallback.

**§8.7 still holds in one respect:** the result is **text adjacency, not connectivity**.
0 Ω series resistors still break the GPIO-to-net pairing, and unlabelled wire-only
connections are invisible. Treat the output as a reading aid and confirm anything
load-bearing against the rendered sheet.

### 9.3 Panel manuals may have offset-encoded text layers

The `3.97inch_e-Paper.pdf` panel manual embeds **two subset fonts whose code points
are uniformly displaced** — `+29` for one, `+26` for the other. Naive extraction
yields `LQFKH 3DSHU` where the document reads `inch e-Paper`.

This is the dangerous variant: after a shift the text is **human-legible but wrong**,
so it does not look like a failure.

```bash
# Recover the offset from a KNOWN heading, never by guessing:
python3 -c "print({ord(w)-ord(e) for e,w in zip('LQFKH','inche')})"   # -> {29}
```

**Validate against a known heading before transcribing any value.** Doing so is what
recovered `Driver IC: SSD1677` — a fact available nowhere else in Waveshare's material
for that board. Decoder:
[`deshift.py`](../../devices/waveshare/esp32-s3-epaper-3.97/tools/deshift.py).

### 9.4 Storefront: category pages are JS-rendered; use `catalogsearch`

```bash
curl -sS -A "$UA" 'https://www.waveshare.com/product/displays/e-paper.htm' | grep -c 'product-item'
# -> 0     (HTTP 200, 244 758 bytes, and no products)
```

**Enumerate with `/catalogsearch/result/?q=<terms>&limit=200`**, which returns real
product URLs. Run several query families — the index is literal:

| Query | Result |
|---|---|
| `e-paper esp32` | 7 products |
| `e-paper driver board` | 6, partly different set |
| `esp32 e-ink` | **zero** — "e-ink" is not indexed as a synonym for "e-Paper" |

### 9.5 Extension to §8.6 — the SKU JSON key has a **trailing space**

§8.6's regex misses the current markup. The listing embeds:

```javascript
var waveshare_sku_attributes = [{"sku ":"33552","attributes":["With Lithium Batt"],"unsaleable":false}, …];
var waveshare_attributes2sku  = {"With Lithium Batt":"33552", …};
```

Note **`"sku "`, not `"sku"`**. A search for `"sku"` returns nothing, which in this
pass caused a price to be recorded as "not established" when it was plainly on the
page. Use:

```bash
python3 -c "import re,html,sys; s=open(sys.argv[1],encoding='utf-8',errors='replace').read(); \
m=re.search(r'waveshare_sku_attributes\s*=\s*(\[.*?\]);',s,re.S); print(html.unescape(m.group(1)))" product.html
```

Prices come from `class="price"` and are a **range** across variants:

```bash
grep -oE 'class="price"[^>]*>\s*\$?([\d,.]+)' product.html | sort -u
```

`"unsaleable":false` on every variant is the availability signal.

### 9.6 Third confirmation: `files.waveshare.com/wiki/common/` mirrors run stale

Already warned about in §4. Now quantified for a third part:

| Document | Waveshare mirror | Manufacturer |
|---|---|---|
| ESP32-S3 datasheet | v1.6 | v2.x (Espressif) |
| **PCF85063A** | **Rev. 6, 2015** (535 722 B) | **Rev. 7, 2018** (726 288 B) |

**Always hash a `common/` mirror against the manufacturer's copy and record both.**
The mirror documents what Waveshare ships its customers; the manufacturer's copy is
what you design against.

### 9.7 Correction to §8.4 — `waveshareteam` repos are **not** reliably licensed

§8.4 records that Waveshare's GitHub repositories are "**Apache-2.0** licensed, where
the demo ZIP ships no `LICENSE` at all". That was true of the ESP32-P4 repositories.
It is **not a vendor-wide guarantee**:

```
github.com/waveshareteam/ESP32-S3-ePaper-3.97   ->  license: null,  no LICENSE file
```

**Check per repository.** The finding that repos *exist* and are strictly better than
the demo ZIP still holds — this one carries Arduino and ESP-IDF examples, factory
firmware and a docs link that the storefront does not mention.

Also note this repo vendors third-party libraries (`XPowersLib`, `SensorLib`) with no
version pin and no upstream commit recorded, so their modification status cannot be
assessed without diffing.

### 9.8 Marketing part names may not match the silicon

The storefront **and** the official docs name this board's PMIC **"TG28"**. The
schematic labels it **`AXP2101`** with X-Powers pin names throughout, and Waveshare's
own firmware drives it through XPowersLib's AXP2101 path.

§4's trust order (**schematic > demo source > wiki > storefront**) resolved it
correctly — but note that here **the docs site was wrong too**, so "it is on the
official documentation platform" is not a promotion in that order. Treat
`docs.waveshare.com` as equivalent to the wiki, not as design data.

## Devices sourced with this guide

- [`ESP32-S3-Knob-Touch-LCD-1.8`](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md)
- [`ESP32-P4-WIFI6-Touch-LCD-3.4C`](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) and [`-4C`](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md), sharing [`-XC`](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md) — source of findings §8
- [`ESP32-S3-ePaper-3.97`](../../devices/waveshare/esp32-s3-epaper-3.97/README.md) — source of findings §9, plus stubs for [`e-Paper ESP32 Driver Board`](../../devices/waveshare/e-paper-esp32-driver-board/README.md), [`ESP32-S3-ePaper-1.54`](../../devices/waveshare/esp32-s3-epaper-1.54/README.md), [`ESP32-C6-ePaper-1.54`](../../devices/waveshare/esp32-c6-epaper-1.54/README.md) and [`ESP32-S3-PhotoPainter`](../../devices/waveshare/esp32-s3-photopainter/README.md)
