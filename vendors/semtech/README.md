# Semtech — documentation sourcing guide

Reusable, cross-device knowledge for obtaining official Semtech documentation for **any** Semtech
part. Written and verified **2026-09-04** while researching the
[LR2021](../../components/semtech/lr2021/README.md) and the
[LoRa generation lineage](../../guides/hardware/lora-radio-generations.md), building on the
unresolved sourcing notes left in [`components/semtech/sx1262/README.md` §11](../../components/semtech/sx1262/README.md).

Every URL pattern and every claim about what does and does not resolve was checked live with `curl`
on the date given, **including negative controls** — a path that should not exist, probed alongside
one that should, so that "200" can be distinguished from "200 that means nothing". Where behaviour
is stated as "404" or "soft 404", that is an observed HTTP result.

**The one-paragraph summary.** Semtech's documents are not on `semtech.com`. They are on a
**Salesforce content-distribution front end** that no non-browser client has been shown to get bytes
out of. Everything you need to *find* a document is machine-readable and easy (§3); everything you
need to *download* one is hard (§4). **The practical answer is distributor mirrors** (§6), and the
practical enumeration tool is a **1 984-entry JSON catalogue embedded in one page** (§3.2).

---

## 1. The hosts

| Host | Owns | Stability |
|---|---|---|
| `www.semtech.com` | Product pages, the **document portal index**, `/uploads/*` marketing PDFs, sitemaps. **No datasheets.** | Stable. Returns a genuine **HTTP 404** (103 374 B HTML) for missing pages — pleasantly probeable. ⚠ One legacy subtree soft-404s (§2.3) |
| **`semtech.my.salesforce.com`** | **Almost every technical document** — datasheets, application notes, user guides, reference designs, errata, test reports. **1 726 of 1 984 catalogue entries.** No login required | ⚠ **JavaScript/Lightning content-distribution shell.** HTTP 200 for valid *and* invalid tokens. See §4 |
| **`semtech.my.site.com`** | **mySemtech Document Portal** — the **registration-walled** tier. 120 catalogue entries | Live. Serves a login page, HTTP 200, for valid and invalid `docId` alike |
| ⚠ `semtech.force.com` | The **former** host of the same portal. **103 catalogue entries still point here** | ❌ **Dead.** HTTP **404 "URL No Longer Exists"** for every `docId`, valid or not. Recoverable — §5 |
| `github.com/LoRa-Net` (= `Lora-net`) | Drivers, SDKs, stacks, LoRa Studio installer, firmware images. **30 catalogue entries link here directly** | The most reliable Semtech source there is. Prefer it for anything software |

Two hosts referenced by the catalogue but not worth a row: `apps.apple.com` (2) and
`play.google.com` (1), for companion apps.

**`www.semtech.com/robots.txt`**, retrieved 2026-09-04 — worth reading before scripting, because it
tells you which subtrees Semtech considers app-like rather than content:

```
User-agent: *
Disallow: /form_request/          Disallow: /mysemtech/
Disallow: /quality_search_result/ Disallow: /selector/
Disallow: /cross-reference-search/ Disallow: /uploads/*.html
Disallow: /sfdc/client/           Disallow: /quality/search-pb-lead-free-rohs-green
Disallow: /netcomponent/          Disallow: /hubfs/
Sitemap: https://www.semtech.com/sitemap.xml
```

⚠ Note `Disallow: /uploads/*.html` — **not** `/uploads/*.pdf`. The PDF subtree is fair game; the
HTML under it is not.

---

## 2. URL templates

### 2.1 Product pages

```
https://www.semtech.com/products/wireless-rf/<family>/<part-lowercase>
```

`<family>` is **not** derivable from the part number, and this is the first thing that wastes an
hour:

| `<family>` | Marketing name | Contains |
|---|---|---|
| `lora-connect` | LoRa Connect™ | `sx1272 sx1276 sx1278 sx1261 sx1262 sx1268 llcc68 sx1280 sx1281` **and `lr1121`** |
| `lora-edge` | LoRa Edge™ | `lr1110 lr1120` |
| **`lora-plus`** | LoRa Plus™ | **`lr2012 lr2021 lr2022`** |
| `lora-core` | LoRa Core™ | `sx1250 sx1255 sx1257 sx1258 sx1301 sx1302 sx1303 sx1308` |
| `frequency-shift-keying-fsk` | — | `sx1211 sx1231 sx1276`-era FSK parts |

Verified 2026-09-04, with negative controls:

| URL | Result |
|---|---|
| `…/lora-plus/lr2021` | **200**, 224 120 B |
| `…/lora-connect/lr2021` | **404**, 106 118 B — the family is wrong, and this is the exact mistake to expect |
| `…/lora-plus/lr9999` (**negative control**) | **404**, 106 118 B |
| `…/lora-connect/sx1262` | **200**, 237 397 B |

**Evaluation-kit and shield part numbers get their own product pages** under the same family, e.g.
`…/lora-plus/lr2021evk2xbs1`, `…/lora-connect/sx1262dvk1cas`. They are enumerated in the sitemap.

### 2.2 Sitemaps — the only complete enumeration

```
https://www.semtech.com/sitemap.xml            → index of the six below
https://www.semtech.com/sitemap-products.xml   ← the one you want (319 016 B)
https://www.semtech.com/sitemap-general.xml    (77 650 B)
https://www.semtech.com/sitemap-applications.xml (13 583 B)
https://www.semtech.com/sitemap-lora.xml       (6 804 B)
https://www.semtech.com/sitemap-page.xml       (2 288 B)
https://www.semtech.com/sitemap-videos.xml     (70 179 B)
```

All 200 `text/xml` on 2026-09-04. **Negative control:** `sitemap-DOESNOTEXIST.xml` → **404**,
103 374 B HTML. So the sitemap namespace is honestly probeable.

⚠ **Use the sitemap, not the family index page.** The rendered `…/lora-connect` index page lists
`lr1121` but **not** `lr1110`/`lr1120`, and does not list the LR2021 at all. The
`lora-plus` family is invisible from `lora-connect`. `sitemap-products.xml` is the only place all
of them appear together.

```bash
curl -sS -A "$UA_CHROME" https://www.semtech.com/sitemap-products.xml \
  | grep -oE '<loc>[^<]+</loc>' | sed 's/<[^>]*>//g' | grep -Ei 'lora|lr[0-9]{4}|sx1[0-9]{3}'
```

### 2.3 ⚠ `/uploads/` — one live subtree, one **soft-404** subtree

This is the trap that produces HTML files with `.pdf` names in someone's artifact directory.

| Path | Behaviour (verified 2026-09-04) |
|---|---|
| `/uploads/common/<file>.pdf` | ✅ Live. `PerSe_One_Pager.pdf` → **200**, 345 151 B, `application/pdf`, `%PDF` |
| `/uploads/technology/**` | ✅ Live. `flood-prediction-112210.pdf` → **200**, 188 784 B, `%PDF` |
| `/uploads/quality/<file>.pdf` | ✅ Live |
| `/uploads/common/NEGATIVE_CONTROL_nope.pdf` | ✅ Honest **404**, 103 375 B HTML |
| ⚠ **`/uploads/documents/<anything>.pdf`** | ❌ **HTTP 200 with 21 149 B of HTML titled *"Find Product Documentation"* — for every path, real or invented** |

The `/uploads/documents/` subtree is the **retired legacy datasheet store**, now replaced by a
search page that answers 200 to everything. Every one of these was tried and all four returned the
identical 21 149-byte HTML:

```
DS_SX1276-7-8-9_W_APP_V7.pdf   DS_SX1261-2_V1.2.pdf
DS_SX1280-1_V3.2.pdf           DOESNOTEXIST_negative_control.pdf   ← negative control
```

**Consequence.** Thousands of blog posts, README files, forum answers and vendored `docs/` folders
link `https://www.semtech.com/uploads/documents/DS_*.pdf`. **Every one of them is now dead, and
none of them looks dead.** If you are following an old citation, expect this. Recovery: §5.2.

### 2.4 The technical-document endpoint (Salesforce)

```
https://semtech.my.salesforce.com/sfc/p/E0000000JelG/a/<recordId>/<token>
```

`E0000000JelG` is Semtech's org id (the 15-char form of `00DE0000000JelG`) and is constant.
`<recordId>` looks like `RQ00000EZ5fu`, `2R000000HSNz`, `3n000000v6rK`, `44000000MDqf` — the prefix
varies by the era the document was uploaded. `<token>` is a 43-character opaque string.

**Neither part is derivable.** You must harvest the pair from a product page or from the catalogue
(§3). See §4 for what happens when you fetch one.

### 2.5 The registration-walled endpoint

```
https://semtech.my.site.com/DP/DP_CommunityLogin?docId=<18-char Salesforce Id>
https://semtech.force.com/DP/DP_CommunityLogin?docId=<...>     ← DEAD, see §5.1
```

---

## 3. How to enumerate everything Semtech publishes

### 3.1 Per product — the product page

Each product page carries a *Documents* table rendered server-side, so `curl` + `grep` works. Every
row is an `<a href>` to a `semtech.my.salesforce.com/sfc/p/…` URL, with a human title and a release
date in the adjacent cells.

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
curl -sS -A "$UA" 'https://www.semtech.com/products/wireless-rf/lora-plus/lr2021' \
  | grep -oE '<a[^>]+href="https://semtech\.my\.salesforce\.com/sfc/p/[^"]+"[^>]*>[^<]*</a>'
```
`executed-success`, 2026-09-04 — 21 document links recovered for the LR2021 this way.

The **Dev Kits & Shields**, **Software** and **Resources** tabs are in the same HTML, so one fetch
gets the lot. ⚠ The **inventory/pricing widget is JavaScript-only** and renders as `$ 0` to `curl`.

### 3.2 ⭐ Across the whole company — the embedded JSON catalogue

**This is the single most useful thing in this guide.**

```
https://www.semtech.com/design-support/development-support-documents/
```

That page (805 220 B) contains an inline `<script>` declaring:

```js
var doc_portal = {"0":{"document_entry_id":1,
                       "SemtechWebsitePlatform":"LoRa Connect",
                       "SemtechWebsiteCategory":"Wireless RF",
                       "URL":"https:\/\/semtech.my.salesforce.com\/sfc\/p\/E0000000JelG\/a\/...",
                       "Category":"Application Notes",
                       "Description":"AN1200.44: Bluetooth Immunity of LoRa at 2.4 GHz",
                       "DatePosted":"2019-07-04"}, "1":{...}, ... };
```

**1 984 entries**, covering **every product line Semtech sells**, with publication dates spanning
**2018-11-14 → 2026-08-25**. Extract it with a JSON raw-decoder (there is trailing JavaScript after
the object, so a plain `json.loads` of a naive regex capture fails):

```python
import json, urllib.request
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
req = urllib.request.Request(
    'https://www.semtech.com/design-support/development-support-documents/',
    headers={'User-Agent': UA})
s = urllib.request.urlopen(req).read().decode('utf-8', 'replace')
i = s.index('var doc_portal = ') + len('var doc_portal = ')
catalogue, _ = json.JSONDecoder().raw_decode(s[i:])     # 1984 entries
```
`executed-success`, 2026-09-04.

**Category counts** (the document-class checklist you should run against any part):

| Category | Entries |
|---|---:|
| Datasheets | 1 005 |
| Application Notes | 346 |
| User Guides | 224 |
| Software Releases (Firmware) | 116 |
| Reference Designs | 110 |
| Reliability Report | 54 |
| Product Briefs | 54 |
| Tools & Software | 33 |
| User Manual Hardware | 20 |
| Design Guides | 7 |
| *(blank)* | 7 |
| **Errata** | **5** |
| Technical articles/White papers | 3 |

⚠ **Only five Errata entries exist in the entire catalogue** — `SX1276-7-8 Errata Note` (×2),
`SX1272 Errata Note`, `Corecell Reference design V1 … Errata note`, and one behind the login wall.
**Do not conclude a part has no errata because none is listed.** Semtech's Gen-2 and Gen-4 errata
live *inside the datasheet* — `DS.SX1261-2` §15 "Known Limitations" and `DS.LR20xx` §22 "Known
Limitations and Workarounds" — and Gen-4 workarounds additionally live in the **driver README** on
GitHub. **The errata checklist item is satisfied by reading the datasheet's last chapters and the
driver repo, not by looking for an errata PDF.**

`SemtechWebsitePlatform` gives you a per-line filter — the LoRa-relevant values are
`LoRa® Transceivers` (271), `LoRa Core` (136), `LoRa® Gateways` (40), `LoRa Connect` (18),
`2.4 GHz Transceivers` (14), `LoRa Edge` (4).

⚠ **Three data-quality caveats**, all observed 2026-09-04:
1. **Duplicate rows are normal.** `LR2021/22/12 Datasheet v2.2` appears **three times** with three
   *different* `<recordId>/<token>` pairs — one per platform tag. Deduplicate on `Description`.
2. **One row is malformed:** `document_entry_id: 1773` has a *description string* in its `URL`
   field (`"LR1121 Module w 1x Johanson IPD fliter for 868/915 MHz…"` — Semtech's typo, not mine).
   Validate `URL.startswith('http')`.
3. **103 rows point at the dead `semtech.force.com`** (§5.1).

### 3.3 Per-product checklist

For any Semtech part, work this list. It is derived from the catalogue's own categories plus the
things that are *not* in the catalogue.

- [ ] **Product page** under the right `<family>` (§2.1) — confirm via `sitemap-products.xml`
- [ ] **Datasheet** — note that one datasheet often covers several parts (`DS.SX1261-2` = two parts;
      `DS.LR20xx` = **three**). Check the ordering table before quoting anything
- [ ] **Revision history inside the datasheet**, usually p. 3. This is where silent spec changes are
      confessed
- [ ] **Errata** → ⚠ read the datasheet's *Known Limitations* chapter **and** the driver README on
      GitHub, not just the Errata category
- [ ] **Application notes** — `AN1200.<nn>`; 63 distinct AN numbers appear in the catalogue.
      ⚠ Some ANs a datasheet cites are **not on the product page** (`AN1200.37` is cited by
      `DS.SX1261-2` §4.1.2 and appears nowhere on the SX1262 page)
- [ ] **Reference designs** — ZIPs, per region (`EU868`, `US915`, `CN490`)
- [ ] **Regulatory test reports** — ETSI / FCC prescan ZIPs, where published
- [ ] **User guide / user manual hardware** for the EVK
- [ ] **Product brief**, **reliability report** (⚠ usually login-walled — §4.3)
- [ ] **Driver / SDK** on `github.com/LoRa-Net` — and check for a **standalone** driver repo; its
      absence is itself a finding (the LR20xx has none)
- [ ] **Module and EVK part numbers** — they have their own product pages and their own documents

---

## 4. ⚠ The download problem

### 4.1 What happens when you fetch a `/sfc/p/` URL

`GET https://semtech.my.salesforce.com/sfc/p/E0000000JelG/a/RQ00000EZ5fu/<token>` returns **HTTP
200** and **1 359 bytes** of HTML containing nothing but a self-submitting form:

```html
<form id="postBack" name="postBack" action="/sfc/p/#E0000000JelG/a/RQ00000EZ5fu/<token>" method="POST">
   <input type="hidden" name="compositePageName" value="E0000000JelG/a/RQ00000EZ5fu/<token>">
</form>
<script>document.postBack.submit()</script>
```

⚠ **Note the `#` in the form action.** Everything after it is a URL fragment, so a browser actually
POSTs to bare **`/sfc/p/`** carrying `compositePageName`. Reproducing that exactly:

```bash
CPN='E0000000JelG/a/RQ00000EZ5fu/L1sOvqDN_QMyCWYAAychIL5ygPsQw1AEq7xzcvpGNZg'
curl -sS -A "$UA_CHROME" -b cookies.txt -c cookies.txt \
     --data-urlencode "compositePageName=$CPN" \
     'https://semtech.my.salesforce.com/sfc/p/'
```

…returns **53 747 bytes** — and it is not the document. It is a **Lightning Out bootstrap**:

```js
var lightningDistUri = '/sfc/ld/' + 'E0000000JelG' + '/a/RQ00000EZ5fu/<token>';
var distributionId = '05DRQ00000EZ5fu';
$Lightning.use('forceContent:contentDistributionApp', function() {
    $Lightning.createComponent('forceContent:contentDistributionViewer',
        { recordId:'05DRQ00000EZ5fu', distSuffix:'/a/RQ00000EZ5fu/<token>',
          orgId:'00DE0000000JelG', ... }, 'wrapper', function(cmp) {});
}, this.location.origin + lightningDistUri);
```

The real download URL is built **client-side by an Aura component** after an authenticated
framework round-trip. Everything tried against it, `executed-failed` 2026-09-04:

| Attempt | Result |
|---|---|
| `GET /sfc/ld/E0000000JelG/a/<rec>/<token>` | 200, **550 B**, *"Unable to Process Request — We couldn't access the content delivery"* |
| `POST` the same with `compositePageName` | identical 550 B |
| `…/app.js`, `…/app.js?aura.format=JSON&…`, `…/aura?r=1` under `/sfc/ld/` | identical 550 B |
| `GET /sfc/dist/version/download/?oid=00DE0000000JelG&d=/a/<rec>/<token>&asPdf=false` | **200 `application/json`, zero bytes** — the endpoint exists but wants an `ids=<ContentVersionId>` that only the Aura round-trip yields |
| `GET /sfc/servlet.shepherd/document/download/05DRQ00000EZ5fu` | 200, 787 B of HTML |
| `GET /sfc/p/<...>/<token>?download=1` | 200, the same 1 359 B shell |

**Verdict: `blocked` for automated clients.** A real browser is required. This corroborates and
extends the finding first recorded in
[`components/semtech/sx1262/README.md` §11](../../components/semtech/sx1262/README.md), and adds the
`/sfc/ld/` and `/sfc/dist/version/download/` legs that were not previously traced.

### 4.2 ⚠ The negative control that matters most

```bash
curl -sS -A "$UA_CHROME" -o /dev/null -w '%{http_code} %{size_download}\n' \
  'https://semtech.my.salesforce.com/sfc/p/E0000000JelG/a/RQ00000EZ5fu/THIS_TOKEN_DOES_NOT_EXIST_0000000000000000000'
# 200 1363
```

**An invented token returns HTTP 200 and a 1 363-byte shell — four bytes different from the valid
one.** So:

- **The `/sfc/p/` endpoint tells you nothing about whether a document exists.** You cannot probe it,
  you cannot validate a harvested URL with it, and a 200 from it is not evidence of anything.
- Any script that treats "HTTP 200 from Semtech" as success will happily write 1 359 bytes of HTML
  into `datasheet.pdf`. **Validate by magic bytes** (`%PDF`), never by status code or URL suffix.

### 4.3 What actually requires registration, exactly

Two different gates, and they are frequently conflated. **The Salesforce `/sfc/p/` shell is *not* a
login wall** — it needs no account, only a browser. The genuine login wall is the **mySemtech
Document Portal** on `semtech.my.site.com`, and it covers a specific, measurable slice:

| Document class | Public `/sfc/p/` | **Login-walled** |
|---|---:|---:|
| Datasheets | 970 | **35** |
| Application Notes | 311 | **35** |
| User Guides | 183 | **41** |
| Software Releases (Firmware) | 47 | **35** *(+34 direct GitHub links)* |
| Reference Designs | 102 | **8** |
| **Reliability Report** | 6 | **48** ← the most-gated class by far |
| Product Briefs | 44 | **10** |
| User Manual Hardware | 10 | **10** |
| Errata | 4 | **1** |
| Tools & Software · Design Guides · White papers | 32 · 7 · 3 | 0 |

**And the finding that matters for anyone reading this guide for LoRa work:**

> **Zero LoRa documents are login-walled.** All 271 `LoRa® Transceivers`, 136 `LoRa Core`, 40
> `LoRa® Gateways`, 18 `LoRa Connect`, 14 `2.4 GHz Transceivers` and 4 `LoRa Edge` entries resolve
> either to the public `/sfc/p/` endpoint or straight to GitHub. **Not one points at
> `DP_CommunityLogin`.**

The login wall is overwhelmingly **Signal Integrity, Crosspoints, Clocks and reliability
qualification reports** — Semtech's non-LoRa businesses.

**How the gate behaves**, verified 2026-09-04:

```bash
curl -sSL -A "$UA_CHROME" 'https://semtech.my.site.com/DP/DP_CommunityLogin?docId=a0G2R00000zilgEUAQ'
# 200  322 432 B  text/html   <title>mySemtech Document Portal | Semtech</title>   (login form)

curl -sSL -A "$UA_CHROME" 'https://semtech.my.site.com/DP/DP_CommunityLogin?docId=a0GBOGUS'
# 200  322 006 B  ← also a login page
```

⚠ **Both return HTTP 200 and a login page.** The two bodies differ slightly (322 432 vs 322 006 B),
so a valid `docId` leaks *something*, but neither response distinguishes "needs login" from "does
not exist". **Do not treat a 200 here as document existence either.**

Registration is free but is an account-creation flow; **this pass did not create one**, so what lies
beyond the wall is `not-tested`.

---

## 5. Known migrations and how to recover from them

### 5.1 `semtech.force.com` → `semtech.my.site.com`

The classic Salesforce Communities → Experience Cloud domain move. Semtech did it and **did not
rewrite its own catalogue**: 103 of 1 984 entries still point at `semtech.force.com`.

**Detection.** Every `semtech.force.com/DP/DP_CommunityLogin?docId=…` returns:

```
HTTP 404, 1 972 B
<span ...>URL No Longer Exists</span>
You have attempted to reach a URL that no longer exists on salesforce.com.
```

⚠ **Identical for a valid `docId` and an invented one** — verified with both. So the 404 is the
host, not the document.

**Recovery: swap the host, keep the `docId`.** `executed-success` 2026-09-04 —
`docId=a0G2R00000q7EOCUA2` (an errata note, dead on `force.com`) returns **200** and the mySemtech
login page on `semtech.my.site.com`:

```bash
sed 's|semtech\.force\.com|semtech.my.site.com|' <<< "$URL"
```

### 5.2 The two dead `semtech.com` document stores

| Old path | Era | Now | Recovery |
|---|---|---|---|
| `www.semtech.com/images/datasheet/<file>.pdf` | ~2011–2016 | ❌ gone | **Wayback.** The CDX index has hundreds of them |
| `www.semtech.com/uploads/documents/<file>.pdf` | ~2017–2020 | ⚠ **soft 404** (§2.3) | **Wayback**, then the catalogue for the current revision |

```bash
# what was ever published under those paths, as PDFs
curl -sS "https://web.archive.org/cdx/search/cdx?url=semtech.com/*&matchType=domain\
&output=text&fl=timestamp,original,statuscode,length&filter=mimetype:application/pdf&limit=6000"
```
`executed-success` 2026-09-04 — 6 000 rows, including `sx1276_77_78_79.pdf` (2015-07-31, 2 378 028 B),
`DS_SX1276-7-8-9_W_APP_V5.pdf` (2018-09-03, 1 983 317 B), `sx1276_77_78-errata.pdf`,
`sx1272_73_errata.pdf`, `DS_SX1261-2_V1.1.pdf`, `sx1280-1.pdf`. Fetch with the `if_` modifier so
Wayback serves the original bytes rather than a framed page:

```bash
curl -sSL -A "$UA_CHROME" -o out.pdf \
  'https://web.archive.org/web/20180903190247if_/https://www.semtech.com/uploads/documents/DS_SX1276-7-8-9_W_APP_V5.pdf'
head -c5 out.pdf   # %PDF-
```

⚠ **Wayback gives you an old revision, not the current one.** Use it for Gen-1/Gen-2 history and for
recovering a dead citation — not as a substitute for §6.

⚠ **And a hard negative result:** the Wayback CDX index for `semtech.com` contains **zero LR11xx and
zero LR20xx PDFs**, because those documents have only ever lived behind the Salesforce shell, which
Wayback cannot crawl. `semtech.my.salesforce.com` has captures only of the bare host root, all
redirects. **There is no archive route to a Gen-3 or Gen-4 document.**

---

## 6. ⭐ The route that works: distributor mirrors

Since §4 is `blocked` and §5.2 only reaches pre-2020 documents, **authorised distributors are the
practical source for any current Semtech datasheet.** Both were verified 2026-09-04.

### 6.1 Digi-Key — the good one

```
https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/<dir>/<num>_<Filename>.pdf
```

| Probe | Result |
|---|---|
| `…/docus/8924/600_62785538.LR20xxDatasheet_V2_1.pdf` | **200**, 5 809 234 B, `application/pdf`, `%PDF` |
| `…/docus/8924/600_00000000.NEGATIVE_CONTROL.pdf` | **404**, 3 340 B HTML |

**No User-Agent games needed; honest 404s; correct content type.** This is the best-behaved Semtech
mirror found. ⚠ The `<dir>` and `<num>` components are Digi-Key's opaque internal ids and are **not
derivable** — harvest the full URL from a search engine or from the Digi-Key product page.

### 6.2 Mouser — works, but only with an unusual User-Agent

```
https://www.mouser.com/pdfDocs/<opaque-id><Filename>.pdf
```

⚠ **Mouser blocks the ordinary browser agent on this path and serves the WhatsApp link-preview
agent.** This is the reverse of the usual pattern:

| UA | Result for `61979758LR2021_V1_1_datasheet.pdf` |
|---|---|
| `Mozilla/5.0 … Chrome/131.0.0.0 …` | **200**, 13 895 B, `text/html` — an *"Access Denied / captcha"* page. ⚠ **HTTP 200**, so a naive script saves it as a PDF |
| **`WhatsApp/2.23.20.0`** | **200**, **5 158 757 B**, `application/pdf`, `%PDF` ✅ |

**Negative control:** guessed filenames (`LR2021_datasheet.pdf`, `DS_LR2021_V1.0.pdf`) return
**403**, 1 140 B. And `https://www.mouser.com/c/?q=<part>` returns the 13 895 B Access-Denied page to
**every** agent tried — so Mouser is usable as a fetcher, not as a search engine.

### 6.3 ⚠ Mirrors are revision-frozen, and that is a feature

Three sources, three revisions of the same document, on the same day:

| Source | Revision | Bytes | SHA-256 (first 16) |
|---|---|---:|---|
| **Semtech** (canonical, `blocked`) | **v2.2, 2026-08-08** | — | — |
| **Digi-Key** | **Rev 2.1, 13/04/26**, 243 pp | 5 809 234 | `0d9051db78b243bf` |
| **Mouser** | **Rev 1.1, 10/14/25**, 236 pp | 5 158 757 | `926b88cbfb6434e3` |

**A distributor mirror tells you which revision that distributor's customers were designing
against.** Keep both, name each for its source, and record which is current — the reasoning is in
[`components/semtech/lr2021/README.md` §14.2](../../components/semtech/lr2021/README.md) and the
[archive placeholder](../../components/semtech/lr2021/artifacts/lr2021-datasheet-v1.1-mouser-mirror.pdf.ARCHIVED.md).

### 6.4 Vendor mirrors

Board vendors sometimes mirror the chip datasheet openly, and those mirrors are the fastest route of
all when they exist. Known-good, recorded by the SX1262 pass:

```
https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1177/DS_SX1261_2_V2-2.pdf   # open, 200, application/pdf
```

⚠ **Vendor mirrors serve the revision the board was designed against**, which may be years old.
File them under the **component**, name them `…-<vendor>-mirror.pdf`, and hash them.

---

## 7. User-Agent behaviour, measured

`www.semtech.com/products/wireless-rf/lora-connect/sx1262`, 2026-09-04:

| User-Agent | Result |
|---|---|
| `Mozilla/5.0 … Chrome/131.0.0.0 …` | **200**, 237 397 B |
| **`curl/8.0.1` (default)** | **200**, 237 397 B — ⚠ **no UA spoofing is needed for `semtech.com`** |
| `…ClaudeBot/1.0; +claudebot@anthropic.com` | **200**, 237 397 B |
| ⚠ **`WhatsApp/2.23.20.0`** | ❌ **403**, 919 B |

**So `semtech.com` is the exact inverse of `mouser.com`**, and the inverse of `www.st.com` (which
serves the WhatsApp agent and resets Chrome). There is no single agent that works everywhere. The
rule for this vendor:

| Host | Use |
|---|---|
| `www.semtech.com` | anything **except** WhatsApp. Default `curl` is fine |
| `semtech.my.salesforce.com` | Chrome UA + cookie jar — and it still will not give you bytes (§4) |
| `mm.digikey.com` | any UA |
| **`www.mouser.com/pdfDocs/`** | **`WhatsApp/2.23.20.0`** — Chrome is blocked |
| `api.github.com` | authenticate with `gh auth token`; UA is irrelevant |

Recorded in [`ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md).

---

## 8. Validation requirements

Non-negotiable for this vendor, because **three separate Semtech-adjacent paths return HTTP 200 with
HTML for a document request**: the `/sfc/p/` shell (1 359 B), the `/uploads/documents/` soft-404
(21 149 B), and Mouser's Access-Denied page (13 895 B).

```bash
# after every download
head -c 5 "$f" | grep -q '%PDF' || { echo "NOT A PDF: $f"; exit 1; }
sha256sum "$f"; stat -c%s "$f"
```

Then record, for every artifact:

- **Document number and revision** — Semtech prints both in the running footer of every page, e.g.
  `LR2021/LR2022/LR2012 · Final Datasheet Rev. 2.1 · DS.LR20xx 13/04/26 · N of 243`. **Use the
  footer, not the filename** — the Digi-Key filename says `V2_1` but the footer says `Rev. 2.1`
  *and* gives the date and the document number
- **The revision history table**, usually page 3, which is where silent spec changes are confessed
- SHA-256, byte size, retrieval date, canonical URL **and** mirror URL

⚠ **Text-layer defects are common in Semtech PDFs and they are the quiet kind.** Two observed:

| Document | Defect |
|---|---|
| `DS.SX1261-2` Rev 2.2 | **Figure fonts carry a uniform +31 code-point offset** — block-diagram labels extract as human-legible but *wrong* text (`-P3B¥` for `LoRa®`, `41*` for `SPI`). Body text and tables are clean |
| `DS.LR20xx` Rev 2.1 | The **micro sign is dropped** — sleep currents extract as `A` where the page says `µA`, PA ramp times as `s` where the page says `µs`. Figures are **vector art with no text layer at all**, so pin-out diagrams and the package-marking drawing extract as bare word lists or as nothing |

**Cross-check every extracted value against the running footer and page numbering before
transcribing, and never transcribe a figure label.**

---

## 9. Rights and licensing observations

- Semtech datasheets carry **"Semtech Proprietary & Confidential" in the footer of every page** —
  on documents that Digi-Key and Mouser mirror openly and that Semtech itself links from a public
  product page. ⚠ **That is a genuine conflict, not an oversight.** Record redistribution status as
  `unknown`, keep the artifact unstaged, and say so. Do not resolve it by preference.
- **LR-FHSS is patent-encumbered.** Every datasheet covering an LR-FHSS-capable part carries a
  notice that using Semtech's LR-FHSS software grants **no** patent rights; rights come *"by
  purchasing Semtech SX1261, SX1262, SX1268, LR1110, LR1120, LR1121, LR2012, LR2021 or LR2022
  semiconductor devices, or their authorized counterparts"*.
- **Bluetooth:** parts with a BLE PHY carry *"not certified or qualified Bluetooth products"*.
- **Software is far more permissive than documents.** `LoRa-Net` driver repos are
  **BSD-3-Clause-Clear** (`sx126x_driver`, `llcc68_driver`, `SWDR001`, `SWL2001`, and the
  `lr20xx_driver` subtree inside `usp`), some are Apache-2.0 or MIT. ⚠ **GitHub's repo-level label
  is often `NOASSERTION`** for monorepos — check the subtree's own `LICENSE.txt`, which is where
  `usp`'s BSD-3-Clause-Clear text actually lives.
- Preserve `LICENSE.txt` / `LICENSES.txt` when snapshotting a driver; the Clear BSD disclaimer is
  part of the obligation.

---

## 10. Working command examples

```bash
UA_CHROME='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
UA_WA='WhatsApp/2.23.20.0'

# 1. Find the family a part lives in
curl -sS -A "$UA_CHROME" https://www.semtech.com/sitemap-products.xml \
  | grep -oE '<loc>[^<]+</loc>' | sed 's/<[^>]*>//g' | grep -i 'lr2021'

# 2. Enumerate one product's documents
curl -sS -A "$UA_CHROME" 'https://www.semtech.com/products/wireless-rf/lora-plus/lr2021' \
  | grep -oE '<a[^>]+href="https://semtech\.my\.salesforce\.com/sfc/p/[^"]+"[^>]*>[^<]*</a>'

# 3. Enumerate EVERYTHING (§3.2) — see the Python snippet there

# 4. Fetch a datasheet, Digi-Key (preferred)
curl -sSL -A "$UA_CHROME" -o ds.pdf \
  'https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8924/600_62785538.LR20xxDatasheet_V2_1.pdf'

# 5. Fetch a datasheet, Mouser (⚠ WhatsApp UA)
curl -sSL -A "$UA_WA" -o ds.pdf 'https://www.mouser.com/pdfDocs/61979758LR2021_V1_1_datasheet.pdf'

# 6. Validate — ALWAYS
head -c 5 ds.pdf | grep -q '%PDF' && sha256sum ds.pdf && stat -c%s ds.pdf

# 7. Recover a dead force.com portal link
echo "$URL" | sed 's|semtech\.force\.com|semtech.my.site.com|'

# 8. Recover a dead semtech.com/uploads/documents/ link
curl -sS "https://web.archive.org/cdx/search/cdx?url=semtech.com/*&matchType=domain\
&output=text&fl=timestamp,original,statuscode,length&filter=mimetype:application/pdf&limit=6000" \
  | grep -i 'sx1276'

# 9. Software — always prefer GitHub, always authenticate
gh api repos/LoRa-Net/usp/git/trees/<sha>?recursive=1
curl -fsSL -H "Authorization: Bearer $(gh auth token)" \
  "https://raw.githubusercontent.com/LoRa-Net/usp/<sha>/<path>"
```

⚠ **`github.com/LoRa-Net` and `github.com/Lora-net` are the same organisation** (GitHub org names
are case-insensitive) and return identical repository lists. Semtech's own pages use both spellings
— the LR2021 product page links `github.com/LoRa-Net` while `DS.LR20xx` §22 cites
`https://github.com/lora-net/usp`. Neither is wrong.

---

## 11. Parts documented using this guide

| Part / family | Record |
|---|---|
| **LR2021** (Gen 4) | [`components/semtech/lr2021`](../../components/semtech/lr2021/README.md) |
| LR1121 (Gen 3) | [`components/semtech/lr1121`](../../components/semtech/lr1121/README.md) |
| LR1110 / LR1120 (Gen 3) | [`components/semtech/lr11x0`](../../components/semtech/lr11x0/README.md) |
| SX1262 (Gen 2) | [`components/semtech/sx1262`](../../components/semtech/sx1262/README.md) — §11 of that record is what prompted this guide |
| SX1268 (Gen 2) | [`components/semtech/sx1268`](../../components/semtech/sx1268/README.md) |
| LLCC68 (Gen 2) | [`components/semtech/llcc68`](../../components/semtech/llcc68/README.md) |
| SX1276 / SX127x (Gen 1) | [`components/semtech/sx1276`](../../components/semtech/sx1276/README.md) |
| Cross-cutting | [`guides/hardware/lora-radio-generations.md`](../../guides/hardware/lora-radio-generations.md) |

---

## 12. Change log for this guide

| Date | Change |
|---|---|
| **2026-09-04** | Created, during the LoRa generation-lineage pass. Everything above live-verified on this date with negative controls. New findings not previously recorded anywhere in this repository: the **embedded 1 984-entry JSON document catalogue** (§3.2); the **`/uploads/documents/` soft-404** (§2.3); the **`semtech.force.com` → `semtech.my.site.com` migration and its 103 stale catalogue rows** (§5.1); the **exact scope of the registration wall**, and the finding that **no LoRa document is behind it** (§4.3); the **`/sfc/ld/` and `/sfc/dist/version/download/` legs** of the Salesforce shell (§4.1); the **invalid-token negative control returning 200** (§4.2); **Digi-Key and Mouser URL templates with negative controls**, and Mouser's **inverted User-Agent requirement** (§6); and the measured **UA matrix** showing default `curl` is fine on `semtech.com` while WhatsApp is 403'd (§7) |
