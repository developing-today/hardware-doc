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

## Devices sourced with this guide

- [`ESP32-S3-Knob-Touch-LCD-1.8`](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md)
- [`ESP32-P4-WIFI6-Touch-LCD-3.4C`](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) and [`-4C`](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md), sharing [`-XC`](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md) — source of findings §8
