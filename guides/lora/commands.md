# Command ledger — LoRa transceiver generations pass

> **Promoted into the repository 2026-09-20** from
> `archive/guides/lora/artifacts/lora-generations-pass-2026-09-04/commands.md`, because
> [`SKILL.md` § 3](../../.agents/skills/hardware-device-research/SKILL.md) requires a pass to
> maintain a `commands.md` ledger **as a repository document**, and this one was reachable only
> through the archive. Content is unchanged; the archive copy is retained and marked superseded.
> The working directory named below is the path as it was on 2026-09-04 and is left as written —
> it is a record of where the commands ran, not navigation.

Environment: Linux, `bash`, `curl 8.x`, `python3 3.14.7` (system python has **no** `pypdf`,
`pdftotext`, `pdfinfo` or `qpdf`), `gh` authenticated. Working directory
`/home/user/hardware-doc/scratch/lora-generations` unless stated. Date **2026-09-04**.

Status vocabulary: `executed-success` · `executed-failed` · `reported-working` · `inferred` · `not-tested`.

```bash
UA_CHROME='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
UA_WA='WhatsApp/2.23.20.0'
```

---

## 1. Enumerating Semtech

```bash
# Which family does a part live in?  (the lora-connect/lora-edge/lora-plus split is not derivable)
curl -sS -A "$UA_CHROME" https://www.semtech.com/sitemap-products.xml \
  | grep -oE '<loc>[^<]+</loc>' | sed 's/<[^>]*>//g' | grep -Ei 'lora|lr[0-9]{4}|sx1[0-9]{3}'
```
`executed-success` — **the step that found the `lora-plus` family.** Without it the LR2021 is
invisible from every rendered index page.

```bash
# One product's document list (server-rendered, no JS needed)
curl -sS -A "$UA_CHROME" 'https://www.semtech.com/products/wireless-rf/lora-plus/lr2021' \
  | grep -oE '<a[^>]+href="https://semtech\.my\.salesforce\.com/sfc/p/[^"]+"[^>]*>[^<]*</a>'
```
`executed-success` — 21 links for the LR2021.

```bash
# ⭐ EVERY document Semtech publishes, as JSON, in one request
python3 - <<'PY'
import json, urllib.request
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
req=urllib.request.Request('https://www.semtech.com/design-support/development-support-documents/',
                           headers={'User-Agent':UA})
s=urllib.request.urlopen(req).read().decode('utf-8','replace')
i=s.index('var doc_portal = ')+len('var doc_portal = ')
cat,_=json.JSONDecoder().raw_decode(s[i:])          # ⚠ raw_decode: trailing JS follows the object
json.dump(cat, open('semtech-doc-portal.json','w'), indent=1)
print(len(cat), 'entries')                          # 1984
PY
```
`executed-success`. ⚠ **`json.loads()` on a regex capture fails** with
`JSONDecodeError: Extra data: line 1 column 690785` — there is JavaScript after the object. Use
`raw_decode`. Prerequisite: none. Generates `semtech-doc-portal.json` (~700 KB).

---

## 2. Probing, with negative controls

```bash
probe() {  # probe <UA> <label> <url>
  printf '%-70s ' "$2"
  curl -sSL -A "$1" -o /tmp/pb.bin -w '%{http_code} %{size_download} %{content_type}' --max-time 60 "$3"
  printf ' magic=%s\n' "$(head -c 5 /tmp/pb.bin | tr -d '\n\r' | tr -c '[:print:]' '.')"
}
```
`executed-success`. **The `magic=` column is the point** — three separate Semtech-adjacent paths
return HTTP 200 with HTML for a document request, so the status code proves nothing.

```bash
# Honest 404s (safe to probe)
probe "$UA_CHROME" 'real product'  'https://www.semtech.com/products/wireless-rf/lora-plus/lr2021'   # 200 224120
probe "$UA_CHROME" 'bogus product' 'https://www.semtech.com/products/wireless-rf/lora-plus/lr9999'   # 404 106118
probe "$UA_CHROME" 'bogus sitemap' 'https://www.semtech.com/sitemap-DOESNOTEXIST.xml'                # 404 103374

# ⚠ Soft-404 subtree — 200 + 21149 B HTML for EVERY path
probe "$UA_CHROME" 'legacy real'   'https://www.semtech.com/uploads/documents/DS_SX1276-7-8-9_W_APP_V7.pdf'
probe "$UA_CHROME" 'legacy bogus'  'https://www.semtech.com/uploads/documents/DOESNOTEXIST_negative_control.pdf'

# ⚠ Unprobeable — 200 for a fabricated token too
probe "$UA_CHROME" 'sfc valid' 'https://semtech.my.salesforce.com/sfc/p/E0000000JelG/a/RQ00000EZ5fu/L1sOvqDN_QMyCWYAAychIL5ygPsQw1AEq7xzcvpGNZg'  # 200 1359
probe "$UA_CHROME" 'sfc bogus' 'https://semtech.my.salesforce.com/sfc/p/E0000000JelG/a/RQ00000EZ5fu/THIS_TOKEN_DOES_NOT_EXIST_0000000000000000000'  # 200 1363
```
All `executed-success` (as probes).

```bash
# UA matrix — ⚠ semtech.com is the inverse of mouser.com
for ua in "$UA_CHROME" "$UA_WA" 'curl/8.0.1' \
  'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ClaudeBot/1.0; +claudebot@anthropic.com'; do
  probe "$ua" "${ua:0:20}" 'https://www.semtech.com/products/wireless-rf/lora-connect/sx1262'
done
# Chrome 200 | WhatsApp 403 | bare curl 200 | ClaudeBot 200
```
`executed-success`.

---

## 3. The Salesforce shell — the full failed sequence

Kept because it documents a dead end thoroughly enough that nobody need repeat it.

```bash
T='L1sOvqDN_QMyCWYAAychIL5ygPsQw1AEq7xzcvpGNZg'; R='RQ00000EZ5fu'; ORG='E0000000JelG'

# (a) the shell
curl -sS -A "$UA_CHROME" -c cookies.txt "https://semtech.my.salesforce.com/sfc/p/$ORG/a/$R/$T"
#     200, 1359 B: a <form id="postBack" action="/sfc/p/#ORG/a/R/T"> that JS-submits itself
#     ⚠ the '#' makes everything after it a fragment, so the browser POSTs to bare /sfc/p/

# (b) reproduce the POST
curl -sS -A "$UA_CHROME" -b cookies.txt -c cookies.txt \
     --data-urlencode "compositePageName=$ORG/a/$R/$T" \
     -e "https://semtech.my.salesforce.com/sfc/p/$ORG/a/$R/$T" \
     'https://semtech.my.salesforce.com/sfc/p/'
#     200, 53747 B: Lightning Out bootstrap. Yields distributionId=05DRQ00000EZ5fu and /sfc/ld/...

# (c) every leg from there
curl -sS -A "$UA_CHROME" -b cookies.txt "https://semtech.my.salesforce.com/sfc/ld/$ORG/a/$R/$T"           # 550 B "Unable to Process Request"
curl -sS -A "$UA_CHROME" -b cookies.txt "https://semtech.my.salesforce.com/sfc/ld/$ORG/a/$R/$T/app.js"    # idem
curl -sS -A "$UA_CHROME" -b cookies.txt --data "compositePageName=$ORG/a/$R/$T" \
     "https://semtech.my.salesforce.com/sfc/ld/$ORG/a/$R/$T"                                              # idem
curl -sS -A "$UA_CHROME" -b cookies.txt \
     "https://semtech.my.salesforce.com/sfc/dist/version/download/?oid=00DE0000000JelG&d=%2Fa%2F$R%2F$T&asPdf=false"
#     200 application/json, ZERO bytes — endpoint exists, needs ids=<ContentVersionId>
curl -sS -A "$UA_CHROME" "https://semtech.my.salesforce.com/sfc/servlet.shepherd/document/download/05D$R"  # 200, 787 B HTML
```
All `executed-failed` for the goal; `executed-success` as observations. **Verdict: `blocked`.**

---

## 4. Getting the documents that worked

```bash
# Digi-Key — any UA, honest 404s
curl -sSL -A "$UA_CHROME" -o lr20xx-v2.1.pdf \
  'https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8924/600_62785538.LR20xxDatasheet_V2_1.pdf'
#  200  5,809,234 B  application/pdf
curl -sSL -A "$UA_CHROME" -o /dev/null -w '%{http_code} %{size_download}\n' \
  'https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8924/600_00000000.NEGATIVE_CONTROL.pdf'
#  404  3,340 B    ← negative control passes

# ⚠ Mouser — Chrome is BLOCKED, WhatsApp works
curl -sSL -A "$UA_CHROME" -o bad.pdf 'https://www.mouser.com/pdfDocs/61979758LR2021_V1_1_datasheet.pdf'
#  200  13,895 B  text/html   ← an "Access Denied / captcha" page saved with a .pdf name
curl -sSL -A "$UA_WA"     -o good.pdf 'https://www.mouser.com/pdfDocs/61979758LR2021_V1_1_datasheet.pdf'
#  200  5,158,757 B  application/pdf  %PDF ✓

# Wayback, for the pre-2020 generations. Note the `if_` modifier (original bytes, not a framed page)
curl -sS 'https://web.archive.org/cdx/search/cdx?url=semtech.com/*&matchType=domain&output=text\
&fl=timestamp,original,statuscode,length&filter=mimetype:application/pdf&limit=6000' -o cdx2.txt
curl -sSL -A "$UA_CHROME" -o sx1276-v5.pdf \
  'https://web.archive.org/web/20180903190247if_/https://www.semtech.com/uploads/documents/DS_SX1276-7-8-9_W_APP_V5.pdf'

# Preserve a scarce, bot-hostile source
curl -sS -o /dev/null -w '%{http_code}\n' -A "$UA_CHROME" \
  'https://web.archive.org/save/https://www.mouser.com/pdfDocs/61979758LR2021_V1_1_datasheet.pdf'   # 302 = accepted
```
All `executed-success`.

```bash
# ⚠ MANDATORY after every download from this vendor
for f in *.pdf; do
  head -c 5 "$f" | grep -q '%PDF' || { echo "NOT A PDF: $f"; continue; }
  printf '%s  %s  %s\n' "$(sha256sum "$f" | cut -d' ' -f1)" "$(stat -c%s "$f")" "$f"
done
```
`executed-success` — and it is what caught the Mouser captcha page.

---

## 5. Reading PDFs without poppler

The host has no `pdftotext`, `pdfinfo` or `qpdf`, and the system `python3` has no PDF library.

```bash
python3 -m venv /tmp/.pdfvenv && /tmp/.pdfvenv/bin/pip install --quiet pypdf   # pypdf 6.17.0
/tmp/.pdfvenv/bin/python pdftxt.py lr20xx-v2.1.pdf ds-v2.1.txt                 # 243 pages -> 468,733 B
```
`executed-success`. ⚠ Two caveats, both observed on Semtech documents:

- `pypdf` emits a long `fontTools is required to fully parse the encoding of a CFF Type1 font`
  warning per font. **Harmless for body text**, and it dumps a several-KB widths array into stderr.
  Redirect stderr or it drowns the output.
- **The micro sign is dropped.** `µA` extracts as `A`, `µs` as `s`. Cross-check any small-unit value
  against the PDF or against the document's own front-page summary.
- **Figures have no text layer**, so pin-out diagrams and package markings extract as bare word
  lists or as nothing. Never transcribe a figure.

```bash
# Verify the extraction against the document's own footer before trusting a page
grep -c 'Final Datasheet Rev. 2.1' ds-v2.1.txt      # should be ~= page count
grep -n '23.8 Compatibility of Generation 1-4' ds-v2.1.txt
```
`executed-success`.

---

## 6. GitHub — always authenticate

```bash
gh api "orgs/LoRa-Net/repos?per_page=100&sort=updated" \
  --jq '.[] | "\(.name)\t\(.pushed_at)\t\(.license.spdx_id // "none")\t\(.description // "")"'

# Which RELEASE first shipped a feature? Tag-by-tag content probing beats reading a changelog
for t in 7.2.1 7.3.0 7.4.0 7.5.0 7.6.0 7.7.0 7.7.1; do
  n=$(gh api "repos/jgromes/RadioLib/contents/src/modules/LR2021?ref=$t" --jq 'length' 2>/dev/null || echo MISSING)
  echo "$t -> $n"
done
# 7.2.1..7.5.0 MISSING (404) ; 7.6.0+ -> 15
```
`executed-success` — **this is how "first shipped in 7.6.0" was established**, and it is more
reliable than a changelog because it tests the artifact.

```bash
# Full commit history for a path (⚠ --paginate: 135 commits, well past one page)
gh api --paginate "repos/jgromes/RadioLib/commits?path=src/modules/LR2021&per_page=100" \
  --jq '.[] | "\(.sha)\t\(.commit.author.date)\t\(.commit.message | split("\n")[0])"' > lr2021-commits.tsv
tail -1 lr2021-commits.tsv     # the FIRST commit

# ⚠ Licence files are not always named LICENSE
curl -sS -H "Authorization: Bearer $(gh auth token)" \
  https://raw.githubusercontent.com/jgromes/RadioLib/7.2.1/license.txt | head -3    # MIT
#     .../LICENSE  -> 404. This is probably why "RadioLib is LGPL-3.0" circulates.

# Snapshot a subtree of a large monorepo rather than the whole thing (usp is 47 MB / 1419 files)
SHA=512a095e303872f900021361a619b7b1e6e29469
gh api "repos/LoRa-Net/usp/git/trees/$SHA?recursive=1" \
  --jq '.tree[] | select(.type=="blob") | "\(.size)\t\(.path)"' > usp-tree.txt
grep -E 'smtc_rac_lib/radio_drivers/lr20xx_driver/|^[0-9]+\s+(README.md|LICENSE.txt|LICENSES.txt|CHANGELOG.md)$' \
  usp-tree.txt | cut -f2 > files.txt
while read -r p; do
  mkdir -p "out/$(dirname "$p")"
  curl -sSL -H "Authorization: Bearer $(gh auth token)" -o "out/$p" \
    "https://raw.githubusercontent.com/LoRa-Net/usp/$SHA/$p"
done < files.txt

# Deterministic tarball, so the hash is reproducible
tar --sort=name --owner=0 --group=0 --numeric-owner --mtime='2026-04-16T18:51:03Z' \
    -czf usp-lr20xx_driver-v2.0.2-512a095.tar.gz -C out .
```
All `executed-success`. ⚠ **Never print or commit the token.**

---

## 7. Reddit

```bash
# ⚠ www.reddit.com 403s automated clients; old.reddit.com + the WhatsApp UA does not
curl -sS -A "$UA_WA" 'https://old.reddit.com/search.json?q=LR2021&sort=new&limit=25&t=all' -o r.json
curl -sS -A "$UA_WA" 'https://old.reddit.com/r/meshcore/comments/1txo9ii.json?limit=100' -o thread.json
```
`executed-success`. ⚠ **Single-token queries only.** `q=LoRa fourth generation LR2021` caused the
endpoint to fall back to a global recency feed and return 25 completely unrelated posts —
`executed-failed`, and a failure that looks like success. Sleep ~1 s between thread fetches.

---

## 8. Archiving an artifact

```bash
cd /home/user/hardware-doc
cat > /tmp/arch-manifest.json <<'JSON'
[{"path":"components/semtech/lr2021/artifacts/lr2021-datasheet-v1.1-mouser-mirror.pdf",
  "reason":"Superseded revision, retained per the keep-both-revisions rule ...",
  "source":{"repo":"","commit":"","path_in_repo":"https://www.mouser.com/pdfDocs/...",
            "author":"Semtech Corporation","committed":"2025-10-13","license":"unknown"}}]
JSON
python3 tools/archive_artifact.py --repo-root . --manifest /tmp/arch-manifest.json
```
`executed-success`. Produces the symlink + `*.ARCHIVED.md` + `*.ARCHIVED.link` trio and verifies the
move by content fingerprint. ⚠ **It warns `only 0 recovery URL(s)`** if the manifest has no
`source.urls[]` — the placeholder must then be extended by hand with at least two independent
recovery routes before it is fit for purpose. That was done here.

---

## 9. Failures worth not repeating

| Command / approach | Result |
|---|---|
| `curl … 'https://www.semtech.com/products/wireless-rf/lora-connect/lr2021'` | **404** — wrong family, use the sitemap |
| Any route into `semtech.my.salesforce.com` (§3) | **`blocked`** — use a distributor |
| `curl -A "$UA_CHROME" …/mouser.com/pdfDocs/…` | 200 + HTML captcha. Use `$UA_WA` |
| `curl 'https://www.mouser.com/c/?q=LR2021'` | 13 895 B Access Denied to **every** UA |
| `curl 'https://html.duckduckgo.com/html/?q=…'` | **202** to Chrome and to WhatsApp |
| Repeated Bing queries in one session | ⚠ Returns **wrong** results, not zero — thesaurus and Xbox pages for datasheet queries |
| `curl 'https://www.nicerf.com/lora-module/lora2021f33-2g4.html'` | **403** to Chrome and WhatsApp |
| `pip install pypdf` against the system python | `ModuleNotFoundError` — the environment is externally managed. Use a venv |
| `gh api repos/.../contents/LICENSE` on RadioLib | **404** — the file is `license.txt` |
| `json.loads(re.search(r'var doc_portal = (\{.*?\});', s).group(1))` | `JSONDecodeError: Extra data` — use `raw_decode` |
| `old.reddit.com/search.json` with a multi-word query | Silently returns an unrelated global feed |
