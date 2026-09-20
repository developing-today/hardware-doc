# Commands — Xteink X4 Classic (X4C / "X4 V2")

Every command here was run on **2026-09-11** on Linux, `bash`, unless marked
otherwise. Status labels follow the repository convention:
`executed-success` · `executed-failed` · `reported-working` · `inferred` ·
`not-tested`.

**No command in this file touched an Xteink device.** Every `executed-success`
below is a network fetch, a parse, a hash or a PDF extraction. The device-side
procedures are inherited from the [X4 Pro](../x4-pro/commands.md) and are marked
`inferred` here because no X4 Classic has been in anyone's hands in this
repository.

## 1. Vendor catalogue (Shopify)

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

# Whole catalogue with published_at, SKUs, variants, prices, per-variant stock
curl -s -A "$UA" 'https://xteink.com/products.json?limit=250&page=1' -o products-p1.json

# The device's own record
python3 - <<'PY'
import json
d=json.load(open('products-p1.json'))['products']
p=[x for x in d if x['handle']=='xteink-x4-classic-pocket-ereader'][0]
print(p['published_at'], p['created_at'])
for v in p['variants']:
    print(f"{v['sku']:20} {v['price']:>7}  compare_at={v['compare_at_price']}  avail={v['available']}  grams={v['grams']}")
PY
```

- **Status:** `executed-success`.
- **Expected output:** `2026-09-06T19:57:20-07:00 2026-08-03T05:06:01-07:00`, then
  six variants: `X4Classic-gray` and `X4Classic-black` at `79.00`, and four
  reader+base bundles at `95.00`.
- **Why this and not the product page:** `published_at` is the only machine-readable
  launch date the vendor emits. It cannot be back-dated by a theme edit.

```bash
# Per-collection listings — this is what proves the collection was empty before
for h in accessories pocket-e-reader homepage-display machine x3-edm x3-series \
         x4-classic x4-edm x4-pro-series x4-proedm x4-series; do
  curl -s -A "$UA" "https://xteink.com/collections/$h/products.json?limit=250" -o "coll-$h.json"
done
```

- **Status:** `executed-success` (11/11 HTTP 200).
- **Gotcha:** `collections/<handle>/products.json` silently returns
  `{"products":[]}` for an empty *or* nonexistent handle. Cross-check against
  `/collections.json` before concluding a collection does not exist.

## 2. The specification block is only in the HTML

```bash
curl -sL -A "$UA" 'https://xteink.com/products/xteink-x4-classic-pocket-ereader' \
  -o x4c-product-page.html      # 919,867 bytes

python3 - <<'PY'
import re, html
s = open('x4c-product-page.html', encoding='utf-8', errors='replace').read()
i = s.find('DETAILS + DIMENSIONS')
seg = re.sub(r'<(script|style|svg).*?</\1>', ' ', s[i-200:i+4000], flags=re.S)
seg = html.unescape(re.sub(r'<[^>]+>', '\n', seg))
print('\n'.join(l.strip() for l in seg.split('\n') if l.strip()))
PY
```

- **Status:** `executed-success`.
- **Expected output:** `Display 4.3 inch / Resolution 219 PPI /
  Dimensions 114 × 69 × 4.9 mm / Weight 68g / … / Ports Pogo Pin /
  Battery 920mAh / Front light No / Touchscreen No`.
- **Why it is needed:** this product's `body_html` is the empty string. The
  JSON API reports **no specifications whatsoever** for it.

## 3. FCC — the UA matters, and so does validating the PDF

```bash
UA_OK='WhatsApp/2.23.20.0'

curl -sL -A "$UA_OK" https://fccid.io/2BTR9-X4C  -o x4c.html    # 200
curl -sL -A "$UA_OK" https://fccid.io/2BTR9      -o grantee.html # 200 — lists ALL Xteink FCC IDs

# The document ids are in the page's own hrefs
grep -o 'href="/2BTR9[^"]*"' x4c.html | sort -u

# Exhibit download: append .pdf to the href
curl -sL -A "$UA_OK" \
  'https://fccid.io/2BTR9-X4C/Test-Report/Test-Report-9480917.pdf' \
  -o 2BTR9-X4C-test-report.pdf

# ALWAYS validate by content, never by extension
python3 -c "print(open('2BTR9-X4C-test-report.pdf','rb').read(4))"   # -> b'%PDF'
```

- **Status:** `executed-success` for all 12 exhibits fetched across five FCC IDs.
- **Failure modes actually observed, preserved:**
  - `fccid.io` + desktop-Chrome UA → **403**. `WhatsApp/2.23.20.0` → **200**.
  - `fcc.report/FCC-ID/2BTR9-X4C` → **403 on four different UAs**. No workaround found.
  - `apps.fcc.gov/oetcf/eas/reports/GenericSearchResult.cfm?fcc_id=…` → **403**.
- **Expected surprise:** exhibits marked *"Metadata only"* with a future date are
  under a short-term confidentiality order. Requesting `<slug>-<id>.pdf` for them
  does **not** return the document.

## 4. PDF extraction (poppler via nix)

```bash
nix-shell -p poppler-utils --run 'pdftotext -layout in.pdf out.txt'
nix-shell -p poppler-utils --run 'pdfinfo in.pdf'
nix-shell -p poppler-utils --run 'pdfimages -png -f 1 -l 30 in.pdf outdir/p'
```

- **Status:** `executed-success`. poppler 26.06.0, verified 2026-09-11.
- **Applied to:** `2BTR9-X4C-{test-report,antenna-report,rf-exposure,label}.pdf`
  and the sibling X4L/X4Pro/X4/X3 exhibits.
- **Text-layer validation performed:** the string `XTEINK X4 Classic` extracted
  from `rf-exposure` matches the heading visible in the rendered page, and the
  extracted `FCC ID 2BTR9-X4C` matches the page header stamped on every page.
  **No value in this record was transcribed from an unvalidated text layer.**
- **Trap:** `pdfinfo` on a saved HTML page emits dozens of
  `Syntax Error … Illegal character` lines and then *"May not be a PDF file
  (continuing anyway)"*. Treat that as a failed download, not a damaged PDF.

## 5. Board-definition diff against the SDK at HEAD

```bash
SHA=9f4d3f9ca675e64cc9d616081f39a33cdefce57e
gh api "repos/Free-Ink/freeink-sdk/contents/libs/hardware/BoardConfig/include/BoardConfig.h?ref=$SHA" \
  --jq '.content' | base64 -d > BoardConfig-HEAD.h

# Has a new Xteink board appeared?
awk '/enum class Board/,/};/' BoardConfig-HEAD.h

# What changed in this profile since the last sweep?
diff <(awk '/constexpr BoardProfile XTEINK_X4_CLASSIC/,/^};/' BoardConfig-2400379.h) \
     <(awk '/constexpr BoardProfile XTEINK_X4_CLASSIC/,/^};/' BoardConfig-HEAD.h)
```

- **Status:** `executed-success`.
- **Expected output:** the enum is unchanged for Xteink; the profile diff is one
  line, `20000000` → `XTEINK_DISPLAY_SPI_HZ` (`10000000u`).
- **Why this is the first check to run:** a new board reaches the SDK **before**
  it reaches the shop. A silent enum is real evidence that no new SKU exists.

## 6. Proving a string's absence

```bash
gh api -X GET search/code -f q='"X4R1_CLA"' --jq '.total_count'   # -> 0
gh api -X GET search/code -f q='"X4R2_CLA" xteink' \
  --jq '.items[] | "\(.repository.full_name)  \(.path)"'
```

- **Status:** `executed-success`.
- **Gotcha:** an unquoted, unscoped query such as `X4R1` returns ~50,000 junk
  hits (it tokenises). **Quote the exact identifier** and add a scoping term.

## 7. Reddit

```bash
UA_R='WhatsApp/2.23.20.0'
curl -s -A "$UA_R" \
  'https://old.reddit.com/r/XTEINK/search.json?q=%22X4+Classic%22+OR+%22X4+V2%22+OR+X4C&restrict_sr=1&sort=new&limit=100&t=year'

# Comment trees carry the evidence; listings do not
curl -s -A "$UA_R" 'https://old.reddit.com/r/XTEINK/comments/1v4824q.json?limit=200'
```

- **Status:** `executed-success`, 11/11 HTTP 200.
- The FCC ID `2BTR9-X4C` was first published by a community member in a
  **post body**, not a title — it is invisible to a title-only search.

## 8. Device-side procedures — NOT executed

| Procedure | Status | Note |
|---|---|---|
| Enter ROM download mode | `inferred` | The X4C has **no USB-C**. Native USB is on GPIO19/20 and reaches a pad set, not a socket. **The X4 Pro procedure does not transfer**; how a user gets a cable onto an X4C is **unknown and untested** |
| `esptool chip-id` | `not-tested` on X4C | `executed-success` **on an X4 Pro by a third party** — see [`kycube/x4pro-emu` `docs/device/chip_id.txt`](https://github.com/kycube/x4pro-emu/blob/bf4b86ae0471012d4d07c0bb3042f3f561c9c302/docs/device/chip_id.txt) |
| `esptool read-flash 0 0x1000000 flash.bin` | `reported-working` on X4 Pro | Third party dumped twice and both dumps hashed identically — the right way to prove a dump |
| `pio run -e x4c -t upload` | `not-tested` | Build env exists in `platformio.sample.ini`; nobody in this repository has built it |
| CrossPoint OTA install | `reported-working` | [r/CrossPointReader `1wbmagp`](https://old.reddit.com/r/CrossPointReader/comments/1wbmagp/) 2026-09-09, "Xteink X4 Classic support" — community thread, not verified here |

**Do not present any row in that table as a verified X4C procedure.** The only
hardware-executed commands anywhere in this family were run on an X4 Pro by a
third party.
