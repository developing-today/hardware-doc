# M5Stack — documentation sourcing guide

Reusable patterns, URL templates and traps for obtaining official M5Stack material.
Established **2026-09-01** during research on the
[PaperMono (C153)](../../devices/m5stack/papermono/README.md) and its two custom chips.
Every technique below was live-verified on that date, with negative controls where noted.

**M5Stack Technology Co., Ltd** (深圳市明栈信息科技有限公司 / Shenzhen Mingzhan
Information Technology Co., Ltd), Bao'an District, Shenzhen. Site ICP filing
`粤ICP备16010631号` — that is a **web registration, not a product certification**.

## 1. The good news: the docs site is server-rendered HTML

**`docs.m5stack.com` is not a JavaScript shell.** Plain `curl` plus an HTML-to-text pass
gets you the complete page — spec tables, pin maps, code blocks, asset URLs, everything.

*Live-verified 2026-09-01:*

```bash
curl -fsSL -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
  (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
  https://docs.m5stack.com/en/core/PaperMono -o page.html
# HTTP 200, Server: nginx/1.24.0 (Ubuntu), Content-Type: text/html; charset=UTF-8
# 153,939 bytes decoded (32,000 on the wire, brotli)
# sha256 1f442a2295bcd4f0aa39bbd367d2b167990c4688df7f9993a0e914b34600aa15
```

**No page required a User-Agent fallback.** `docs.m5stack.com`, `shop.m5stack.com` and
`burner.m5stack.com` all served 200 to the first request. A browser UA was used
throughout anyway; plain `curl/8.5.0` also worked on the shop endpoints.

This is worth stating because it is the opposite of several other vendors' portals — see
[`vendors/seeed-studio`](../seeed-studio/README.md), whose wiki is a Docusaurus SPA that
returns one link per page.

### 1.1 URL template and slug behaviour

```
https://docs.m5stack.com/<lang>/<category>/<Product>
```

| Category | Example |
|---|---|
| `core` | `/en/core/PaperMono`, `/en/core/PaperS3`, `/en/core/PaperColor` |
| `arduino/<product>` | `/en/arduino/papermono/program`, `/en/arduino/papermono/m5pm1_m5ioe1` |
| `uiflow2/<product>` | `/en/uiflow2/papermono/program` |

**Slugs are forgiving about case, via redirect** — verified 2026-09-01:

| Request | Result |
|---|---|
| `/en/core/PaperMono` | **200** |
| `/en/core/papermono` | **302 → `/en/core/PaperMono`** |
| `/en/core/papermono-lite`, `/en/core/coreink` | **302** to the CamelCase canonical form |
| `/en/core/papermono_lite`, `/en/core/PaperMonoLite` | **404** — underscore and concatenated forms do not exist |
| `/en/core/Paper` | **404** — the original M5Paper has no page at this slug |

So **use `curl -L`**, guess in lowercase, and expect a redirect rather than a match. But
do **not** assume the *shape* is forgiving: only the canonical hyphenation exists.

Note the inconsistency: product slugs are CamelCase (`/core/PaperMono`) while tutorial
paths are lowercase (`/arduino/papermono/`). Both are canonical.

### 1.2 Language variants — and why `zh_CN` matters

Three language trees: **`/en/`**, **`/zh_CN/`**, **`/ja/`**.

Verified mechanically across six PaperMono/Lite pages, 2026-09-01:

| Check | Result |
|---|---|
| Table-row count | 89 / 89 / 89 — identical |
| Pin and signal tokens (`G\d+`, `PYG\d+`, `0x..`) | **empty symmetric difference** in all four language pairs, both products |
| Numeric specs | identical in all three |
| Asset URL sets | identical **modulo the delta below** |

**The three languages are complete, faithful translations of each other** — including
faithfully translating the vendor's own factual errors, which is itself the finding.

> ## ⚠ The one substantive delta: `zh_CN` links Chinese-language datasheets the EN and ja pages omit
>
> | EN / ja page links | `zh_CN` page links instead |
> |---|---|
> | `1205/ST25R3916_EN.pdf` | **`1205/ST25R3916_ZH.pdf`** |
> | `1207/M5PM1_Datasheet_EN.pdf` | **`1207/M5PM1_Datasheet_CN.pdf`** |
> | `1210/IO_Expander_Datasheet_EN.pdf` | **`1210/IO_Expander_Datasheet_CN.pdf`** |
> | `472/esp32-s3_datasheet_en.pdf` | `472/esp32-s3_datasheet_cn.pdf` |
>
> **For M5Stack's own custom chips this is not a convenience, it is the primary source.**
> The [M5PM1](../../components/m5stack/m5pm1/README.md) and
> [M5IOE1](../../components/m5stack/m5ioe1/README.md) are M5Stack-designed parts whose
> only vendor documentation is these datasheets. If the EN edition is ambiguous — and both
> are internally inconsistent in places — **the CN edition is the second independent copy
> that can resolve it**, and it may carry material the EN does not.
>
> **The `ja` pages link the EN datasheets.** There are no JA-localised datasheets.
>
> **Always fetch a product page in `zh_CN` as well as `en` and diff the asset URL sets.**
> This is the single highest-value habit in this guide.

*(A related non-finding, recorded so it is not re-investigated: the `zh_CN` package-size
cell reads `113.2 x 69.6 x21.0mm` — a missing space, a typo, not a spec difference.)*

### 1.3 Per-page PDF renders

Every documentation page has a server-side PDF render:

```
https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/static/pdf/static/<lang>/<category>/<Product>.pdf
```

Live examples, 2026-09-01:

```
.../static/pdf/static/en/core/PaperMono.pdf
.../static/pdf/static/zh_CN/core/PaperMono-Lite.pdf
.../static/pdf/static/ja/core/PaperMono.pdf
.../static/pdf/static/en/arduino/papermono/m5pm1_m5ioe1.pdf
.../static/pdf/static/en/uiflow2/papermono/program.pdf
```

Note the doubled `static/pdf/static/` — that is genuinely the path, not a typo.

These are **large** (the PaperMono one is 15.3 MB, because it embeds every product image)
and are a *render of the page*, not additional content. Useful as an immutable snapshot of
what the page said on a given date; not a substitute for fetching the HTML.

## 2. Document hosting — two Aliyun OSS buckets

M5Stack serves documents from **two different Aliyun OSS buckets in Shenzhen**, and they
are used for different things.

### 2.1 `m5stack-doc.oss-cn-shenzhen.aliyuncs.com/<numeric-product-id>/<file>`

**Product-scoped assets.** The numeric folder is the **product id** in M5Stack's own CMS.

| Product | id |
|---|---|
| PaperMono (C153) | **`1267`** |
| PaperMono-Lite (C153-LITE) | **`1268`** |
| ST25R3916 (as a "product") | `1205` |
| M5PM1 | `1207` |
| M5IOE1 / IO Expander | `1210` |
| SX1262 | `1177` |
| RX8130CE | `1132` |
| ESP32-S3 | `472` |

Everything under a product id, real examples from `1267`:

```
1267/PaperMono_SCH_V0.6.2_20260522.pdf          schematic, 6 sheets, 1,462,039 B
1267/PaperMono_SCH_V0.6.2_20260522_page_0N.png  per-sheet PNG renders, N = 1..6
1267/C153_PaperMono_model_size.pdf              mechanical drawing
1267/C153_PaperMono_model_size_page_01.png
1267/EPD_Module_User_Manual.pdf                 the DKE panel manual  <- see section 2.3
1267/SSD1677.pdf                                controller datasheet (an M5Stack re-export)
1267/C153_PaperMono_main_pictures_NN.webp       NN = 01..12
1267/C153_PaperMono_poweron_{EN,CN}.mp4
1267/C153_C153-Lite_reflash_mode_demo.mp4
1267/C153_PaperMono_download.gif
1267/C153-PaperMono-UserDemo_0x00.exe           EasyLoader
1267/C153-weight.jpg
```

> ## ⚠ Assets for a variant may live under the *parent* product's folder
>
> **The PaperMono-Lite's EasyLoader is at `1267/C153-PaperMono-UserDemo_0x00.exe` — under
> `1267` (PaperMono), not `1268` (Lite).** Both product pages link the identical binary.
>
> `1268` carries only the Lite's own images, its `PaperMono-Lite_PRJ_V0.6.2_20260522.pdf`
> project file and its own mechanical drawing.
>
> **So enumerating a variant's product id alone will under-collect.** Always enumerate the
> parent product's folder too, and diff. This generalises: for any `-Lite`, `-Plus` or
> revision variant, check the base product's id.

Naming conventions observed:

- `<SKU>_<Product>_<purpose>.pdf` — `C153_PaperMono_model_size.pdf`
- `<Product>_SCH_V<x.y.z>_<YYYYMMDD>.pdf` — **`SCH`** for a full schematic
- `<Product>_PRJ_V<x.y.z>_<YYYYMMDD>.pdf` — **`PRJ`** for a project export. The Lite's is
  `PRJ` with **4 sheets** where the PaperMono's is `SCH` with **6**. *Different suffix,
  different sheet count — do not assume a variant's "schematic" is equivalent.*
- Page renders: `<basename>_page_NN.png`
- Datasheets: `<PART>_{EN,ZH,CN}.pdf`, `<part>_datasheet_{en,cn}.pdf` — **casing is
  inconsistent**, and `ZH` and `CN` are both used for Chinese

### 2.2 `m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/...`

**Site-scoped resources** rather than product-scoped:

```
/resource/docs/static/pdf/static/<lang>/<category>/<Product>.pdf     per-page renders (section 1.3)
/resource/certification/<SKU>/{CE,FCC,MIC,RoHS,WEEE}/<file>.pdf      certification documents
```

The certification path is a **predictable template worth probing directly**, because the
certification index page is unreliable (§5.1). Real examples:

```
/resource/certification/C123/FCC/FCC-ID.pdf
/resource/certification/C008-B-V11/MIC/MIC-Certificate.pdf
/resource/certification/C008-C/RoHS/RoHS-Certificate.pdf
```

Note `C008-B` and `C008-B-V11` as sibling folders: **hardware revisions get their own
certification folders.** If a product has revisions, probe `<SKU>-V<rev>` as well.

## 3. Source code and hardware design files

### 3.1 GitHub is a publishing mirror, not the development repo

`github.com/m5stack/*`, MIT-licensed, and consistently the richest source of pin,
register and address evidence — richer than the documentation.

For the PaperMono, five repositories mattered:

| Repo | What it gives you |
|---|---|
| `M5PaperMono-UserDemo` | The factory firmware. A per-peripheral HAL declaring **every pin as a named constant** — the single best pin source |
| `M5PaperMono-OTP-Demo` | Minimal driver, vendor-recommended over M5GFX |
| `M5PM1`, `M5IOE1` | Dual Arduino/ESP-IDF drivers whose **headers are exhaustively commented bilingual register maps** — `M5PM1.h` is 136 KB and is effectively the datasheet |
| `M5Unified`, `M5GFX` | Board autodetect, panel/touch/LED/power classes |

> **Two habits that paid off here:**
>
> 1. **Read the library header, not just the docs.** `M5PM1.h` and `M5IOE1.h` are
>    bilingual (CN/EN) annotated register maps. For M5Stack's own chips they are more
>    complete and more current than the PDF datasheets.
> 2. **Check `repos.json` / `dependencies.lock` for pinned commits.** M5Stack's demos
>    **do not vendor** their dependencies — `repos.json` + `fetch_repos.py` clone ten
>    repos at pinned commits and apply local patches. Those pins are often *older* than
>    the current branch heads, which means the shipped firmware is not built from anything
>    you can check out. Diffing the pins against `HEAD` is how the M5GFX waveform
>    replacement was found.
>
> Both demo repos have **squashed/imported histories (3 commits each)**; the OTP demo's
> HEAD message is literally `Merge GitLab initial history`. **Development happens on an
> internal GitLab; GitHub is a publishing mirror, and upstream history is not available.**

Two incidental findings worth carrying forward: the published `M5IOE1` repository contains
a committed **`.claude/` directory** (agent configuration shipped in a release library),
and `M5PM1`'s LICENSE is dated **2025** while everything else is 2026 — suggesting the
PMIC predates the product and is reused.

### 3.2 ⚠ `M5_Hardware` does not contain everything, and absence there proves nothing

`github.com/m5stack/M5_Hardware` is M5Stack's hardware design-file repository
(`Products/<SKU>_<Name>/`, plus `KiCad` and `Common` libraries). The docs footer links it
as "Hardware Design Files".

**Verified `executed-success` at HEAD `a240115c94b19ecf647f229c47fa9a8ce46ccdc4`, pushed
2026-08-17:**

```bash
git clone --filter=blob:none --no-checkout https://github.com/m5stack/M5_Hardware.git
git -C M5_Hardware ls-tree -r --name-only HEAD | grep -iE 'papermono|c153'   # -> 0 matches
git -C M5_Hardware ls-tree -r --name-only HEAD | grep -oE 'C1[0-9]{2}' | sort -u | tail
#   ... C149 C151 C152
```

**The product tree stops at C152 (`C152_StopWatch`) and contains no C153 entry.** The only
Paper-family entries are `C139_PaperS3`, `C151_PaperColor` and `K049-B_Paper_v1.1`.

The repository was pushed **2026-08-17**, *after* the PaperMono's 2026-08-10 firmware
commit, so this is not simply publishing lag.

> **The lesson generalises: absence from `M5_Hardware` does not mean a schematic was not
> published.** The PaperMono's schematic exists — it is linked directly from the product
> page and served from the OSS bucket (§2.1). **Check the product page's own asset list
> before concluding a design file does not exist.**
>
> Consequence when it *is* absent: there is **no machine-readable netlist** to validate a
> pin map against, and the firmware becomes the primary machine-readable evidence. Clone
> blobless (`--filter=blob:none --no-checkout`) — the full repo is ~128 MB and you only
> need the tree.

## 4. The M5Burner firmware API

Firmware pages at `burner.m5stack.com/firmware/<id>/` are **React SPA shells** with an
empty `<div id="root">` — a plain fetch gets you ~3 KB and the `og:` meta tags, nothing
else. The `og:` tags are still useful: they revealed that the link labelled *"PaperMono
Factory Reset Firmware"* is actually **"PaperMono UserDemo"**.

The real content is behind a **public JSON API**, recovered by reversing the SPA bundle:

```js
var Kn = `${`/api`.replace(/\/$/,``)}/v1`      // assets/http-ChO34QIa.js
```

> ## ⚠ `/api/v1/…` is public; `/api/…` is not
>
> | Endpoint | Result (2026-09-01) |
> |---|---|
> | `burner.m5stack.com/api/firmwares/{id}` | **HTTP 401** `{"msg":"请先登录"}` — "please log in first" |
> | **`burner.m5stack.com/api/v1/firmwares/{id}`** | **HTTP 200, full JSON, no auth** |
>
> The `/v1` segment is the whole difference. Getting a 401 here does **not** mean the
> resource is private.

Working sequence:

```bash
ID=2089640807996628993                       # PaperMono UserDemo
curl -fsSL "https://burner.m5stack.com/api/v1/firmwares/$ID"                 # detail
curl -fsSL "https://burner.m5stack.com/api/v1/firmwares/$ID/versions"        # version list
curl -fsSLo fw.bin "https://burner.m5stack.com/api/v1/firmwares/$ID/versions/$VID/download"
```

The detail JSON carries `firmwareName`, `firmwareDescription`, `sourceType`
(`OFFICIAL` / `COMMUNITY`), `developer` (with `userId`), `currentVersion`,
`supportedDevices`, `statistics.downloadCount` and `uploadedAt` — enough to tell an
official image from a community one and to date it.

> ## ⚠ The download 302s to a CDN object named by a numeric id, not by `binFileName`
>
> ```
> https://m5burner-cdn.m5stack.com/community/{userId}/{firmwareId}/{versionId}/bin/{versionId+1}.bin
> ```
>
> The API reports a human-readable `binFileName` such as
> `C153-PaperMono-ESP32S3R8-UserDemo-V1.2-yaozhenquan-8300e309-20260806_0x00.bin`, and
> **that string does not appear in the URL you are redirected to.** Follow the redirect
> (`curl -L`) and rename locally from `binFileName`; do not try to construct the CDN URL
> from the filename.
>
> Note also that **official images live under `/community/1/…`** — `userId` 1 is
> `m5stack` itself. The path segment says nothing about provenance; `sourceType` does.

**Validate downloads by content, not by extension.** Both images retrieved this way were
checked for HTTP 200, ≥ 4 KiB, first byte `0xE9` (ESP32 image magic) and no HTML/XML in
the first 512 bytes before being given a `.bin` extension.

Parsing the image afterwards is worth the trouble: `esp_app_desc_t` at `0x10020` yields
`project_name`, `app_version`, `build_date`/`time` and `idf_version`. That is how the
PaperMono factory image was found to report **`c78f6c5-dirty`** — built from an
uncommitted tree, therefore not reproducible from any published commit.

## 5. Traps

### 5.1 ⚠ Soft gaps: `/en/certification` and `/en/product_i2c_addr` return 200 with zero matches

These two site-wide reference pages are **incomplete**, and they fail *silently* — HTTP
200, full valid content, other products present, your product simply absent.

| Page | Bytes | PaperMono / C153 matches |
|---|---:|---|
| `docs.m5stack.com/en/certification` | 382,669 | **0** |
| `docs.m5stack.com/en/product_i2c_addr` | 312,908 | **0** |

The second is remarkable: the PaperMono carries **seven** documented I²C devices and
appears in neither the table nor its index.

**These are soft *gaps*, not soft 404s.** The page is real, complete and correctly served;
the product is missing from it. Distinguish the two, because the response looks identical:

- **Soft 404** → the page is a generic template standing in for something that does not
  exist.
- **Soft gap** → the page is genuine and other products *are* present; yours is not.

The test is a **positive control**: search the same page for a product you know is listed.
Here, `/en/product_i2c_addr` *does* list `M5PM1 (0x6e)` for **StickS3 (K150)** — which
both proved the page was intact and independently corroborated the M5PM1's address.

**Never report "no certification found" without that control.** With it, "no FCC/CE/TELEC
identifier is published for this product" becomes a **verified negative** rather than a
failed search — which is exactly what it is for the PaperMono.

### 5.2 ⚠ Shop 404s have a different hash every time — hash-based detection fails

`shop.m5stack.com` is Shopify. Guessed product handles return a **generic 404 template**:

| Probe | HTTP | Bytes | SHA-256 |
|---|---:|---:|---|
| `/products/papermono` | 404 | **389,759** | `b363da8d68a78dd8…` |
| `/products/m5stack-papermono` | 404 | **389,759** | `0856732748738d0a…` |
| `/products/papermono-lite` | 404 | **389,759** | `b5e831b296344a44…` |

**Exactly 389,759 bytes each — and three different hashes.** The template carries a
per-request nonce. So:

- **Hash-based 404 detection does not work here.** Neither does content-length alone, at
  least not as a *positive* identifier without a known-404 baseline.
- The HTTP status is correct (404), so **trust the status code** — the trap is only for
  tooling that ignores status and fingerprints bodies.

**Handles are not guessable.** The real ones bear no resemblance to the product name:

```
shop.m5stack.com/products/m5papermono-with-lora-nfc-800x480-3-97-eink-display
shop.m5stack.com/products/papermono-lite-dev-kit-800x480-3-97-e-ink-display
```

**Use search instead of guessing:**

```bash
curl -fsSL 'https://shop.m5stack.com/search?q=papermono'
curl -fsSL 'https://shop.m5stack.com/search/suggest.json?q=papermono&resources[type]=product&resources[limit]=10'
```

The `suggest.json` endpoint works with plain `curl/8.5.0`, returns both SKUs with prices
and `available` flags, and is far cheaper than the 448 KB HTML search page.

Once you have a handle, **append `.json`** for structured Shopify data — SKU, price,
`created_at`, `published_at`, `updated_at`, variants, barcode, weight:

```bash
curl -fsSL 'https://shop.m5stack.com/products/<handle>.json'
```

That is how three distinct "launch" dates were disentangled for the PaperMono: Shopify
`created_at` 2026-08-18 (internal record), `docs.m5stack.com/en/history` 2026-08-20
(documentation release), Shopify `published_at` + blog `<time datetime>` 2026-08-21
(public availability). **They do not mean the same thing.**

### 5.3 ⚠ `community.m5stack.com` is auth-walled

M5Stack's own NodeBB forum — where owner reports appear first — is **not searchable
unauthenticated**:

| Endpoint | Result (2026-09-01) |
|---|---|
| `/api/search?term=<q>&in=titlesposts` | **401** `{"code":"not-authorised"}` |
| `/search?term=<q>` | **302** to login |
| **`/api/recent`** | **200**, open — returned 198 topics |

`/api/recent` is the only open window and only covers a recent slice. **A negative result
from the vendor forum is therefore "no determination possible", not "nothing exists"** —
say so explicitly rather than implying an absence you did not establish.

### 5.4 Documentation contradicts itself; expect it and record both sides

M5Stack's pages for one product routinely disagree. On the PaperMono, ten distinct
contradictions were found *within vendor material*, including:

- Prose says an interrupt is active-high; the code on the **same page** sets
  `BMI2_INT_ACTIVE_LOW`.
- One tutorial page names a *"reset button on the side"* that does not exist on the
  schematic; two other pages and the spec table say power button.
- One page requires a library the other page's build config omits.
- A hazard note (the charger's I²C gate) appears **only** on the product page and not on
  the dedicated power-management page most likely to be read.
- A link labelled "Factory Reset Firmware" resolves to a record named "UserDemo".

**And the contradictions are faithfully translated into all three languages** — they are
defects in the source content, not translation errors, so a second language does not
arbitrate them.

**Practical rule:** when vendor prose and vendor code disagree, **the code and the shipped
binary win**. Both were decisive here.

### 5.5 Mirrored third-party datasheets are not necessarily current

M5Stack mirrors other manufacturers' datasheets under its own product ids (§2.1). Those
mirrors are **not** guaranteed to be the current revision, and sometimes not even a clean
copy:

- The mirrored **BMI270** datasheet is **five years behind Bosch's** current revision.
- The mirrored **SSD1677** PDF has 46 pages but numbers itself `n/47`, its PDF Producer is
  **`PDFill`** rather than a Solomon Systech export, and it is marked *"Advance
  Information", Rev 1.0, Nov 2018*. Treat as a re-processed copy of a preliminary
  document.
- The **RX8130CE** register datasheet is mirrored **only in Chinese**.
- The **DKE panel manual** has **no text layer at all** — see
  [`vendors/dke`](../dke/README.md).
- ⚠ **Some "mirrors" are not mirrors of the manufacturer at all.** Both audio datasheets M5Stack
  serves for the Cardputer v1.x —
  `datasheet/core/SPM1423HM4H-B_datasheet_en.pdf` and
  `datasheet/core/NS4168_CN_datasheet.pdf` — carry
  `Title: DATASHEET SEARCH SITE | WWW.ALLDATASHEET.COM` and
  `Author: Provided By ALLDATASHEET.COM(FREE DATASHEET DOWNLOAD SITE)` **in their PDF metadata**.
  M5Stack re-hosted an **aggregator's** copy, so the chain is two hops from the chip maker, and
  the `ModDate` (2013 and 2019 respectively) dates the *re-wrap*, not the document.
  Worse, the NS4168 file's **cover logo is a distributor's**
  (深圳市永阜康科技有限公司 / Shenzhen Yongfukang Technology) and the supposed manufacturer's
  name appears **nowhere in its 15 pages** — see
  [`components/nsiway/ns4168` §6](../../components/nsiway/ns4168/README.md).
  **Read `pdfinfo` on every mirrored datasheet before trusting its provenance.** Verified
  2026-09-20.

**Always prefer the original manufacturer's copy, and hash both.** Keep the M5Stack mirror
anyway when it is the only accessible copy, and **label it as a mirror in the filename**.

### 5.5.1 Connector drawings live under a *different product's* path

The DinMeter's two connector drawings are served from **M5Dial's** documentation path, not
DinMeter's:

```
…/resource/docs/products/core/M5Dial/DB2EK-2.54-2P-GN-S%202.54mm%202Pin%20Green.pdf
…/resource/docs/products/core/M5Dial/1.25WT-2P.pdf
```

This is the same "variant assets live under the parent product" pattern §2.1 records for
EasyLoader binaries, extended to commodity parts: **a connector shared across products gets one
copy, filed under whichever product first needed it.** When a product page links a datasheet,
check the path — it will often tell you which other products share the part. Verified
2026-09-20.

⚠ **And M5Stack's filename is not the vendor's ordering code.** `DB2EK-2.54-2P-GN-S` uses `GN`
for green where the vendor's own decode block on the drawing specifies the numeral `1`; the
orderable part is `DB2EK-2.54-02P-1-S`.

## 6. Document-class checklist

Work through this per product; each line names where it is likely to live.

| Class | Where | PaperMono result |
|---|---|---|
| Product page (spec table, PinMap, precautions) | `docs.m5stack.com/<lang>/core/<Product>` | ✅ |
| **The same page in `zh_CN`** — for CN-only datasheet links | `/zh_CN/core/<Product>` | ✅ **found 4 CN-only datasheets** |
| Arduino quick-start | `/en/arduino/<product>/program` | ✅ |
| Per-feature Arduino API sub-pages | linked from the quick-start | ⚠ **14 enumerated, none fetched** |
| Product-specific tutorial pages | `/en/arduino/<product>/<topic>` | ✅ `m5pm1_m5ioe1` |
| UiFlow2 page | `/en/uiflow2/<product>/program` | ✅ but **empty of substance** |
| Schematic | product page asset list → OSS `<id>/…_SCH_…pdf` | ✅ |
| Mechanical drawing | OSS `<id>/…_model_size.pdf` | ✅ |
| Component datasheets | product page "Datasheets" section | ✅ 7 listed |
| Hardware design files (EDA source) | `github.com/m5stack/M5_Hardware` | ❌ **no C153 entry** (§3.2) |
| Factory firmware source | `github.com/m5stack/<Product>-UserDemo` | ✅ |
| Factory firmware binary | M5Burner API (§4) | ✅ |
| EasyLoader | OSS `<id>/…_0x00.exe` — **check the parent id** | ✅ under `1267` |
| Release date | `docs.m5stack.com/en/history` | ✅ 2026-08-20 |
| SKU / price / stock | `shop.m5stack.com/search/suggest.json` then `<handle>.json` | ✅ |
| Product index (all SKUs, variants) | `/en/products` | ✅ confirmed exactly two SKUs |
| **Certification** | `/en/certification` **+ positive control** (§5.1), and probe `/resource/certification/<SKU>/…` | ❌ **verified absent** |
| **I²C address table** | `/en/product_i2c_addr` **+ positive control** | ❌ **verified absent** |
| Launch announcement | `shop.m5stack.com/blogs/news/…` | ✅ |
| Community reports | `community.m5stack.com` — **auth-walled** (§5.3) | ⚠ no determination |

## 7. Per-product procedure

1. **Fetch the product page in `en` *and* `zh_CN`** (and `ja` if you want the third
   control). Use `curl -L`; lowercase slugs 302 to CamelCase.
2. **Extract every absolute URL from all language variants and diff the sets.** The CN
   delta is where vendor-only Chinese datasheets appear (§1.2).
3. **Note the numeric product id** from the OSS asset URLs. **Also enumerate the parent
   product's id** if this is a `-Lite` / variant SKU (§2.1).
4. Download the schematic, mechanical drawing and every listed datasheet. **Hash
   everything.** Label mirrors as mirrors.
5. **Check the schematic PDF for concatenated sub-documents** — the PaperMono's six
   "sheets" are three separate Altium projects with restarting reference designators, and
   one sub-document is missing its sheet 1 of 2.
6. Clone the `-UserDemo` and any `-Demo` repositories. **Read the HAL headers for pins,
   the library headers for registers, and `repos.json`/`dependencies.lock` for pinned
   dependency commits.**
7. **Diff the pinned dependency commits against current branch heads.** Divergence there
   is a real finding about what the shipped firmware actually is.
8. Pull the firmware binary via the M5Burner **`/api/v1`** endpoint (§4). Validate by
   content. Parse `esp_app_desc_t` and the partition table.
9. Check `M5_Hardware` for EDA source — and **do not conclude anything from its absence**
   (§3.2).
10. Check `/en/certification` and `/en/product_i2c_addr` **with a positive control** (§5.1).
11. Get SKU/price/stock from `search/suggest.json` → `<handle>.json`. Never guess handles
    (§5.2).
12. **Record contradictions rather than picking a value.** When prose and code disagree,
    the code and the shipped binary win — but write down both.

## 8. Rights and licensing observations

| Material | Terms |
|---|---|
| **Source repositories** | **MIT**, "Copyright (c) 2026 M5Stack Technology CO LTD" (M5PM1's says 2025). `SPDX-License-Identifier: MIT` in file headers |
| Schematics and mechanical drawings | **No stated licence.** Published openly on the product page; redistribution status `unknown` |
| M5Stack-authored datasheets (M5PM1, M5IOE1) | Published by *Shenzhen Mingzhan Information Technology Co., Ltd*. No licence statement |
| **Mirrored third-party datasheets** | **Keep their original manufacturers' terms.** Rehosting by M5Stack does not relicense them |
| Firmware binaries | No stated terms; retrievable from a public API |
| Product imagery | **Not licensed for redistribution.** This is why no product photograph is retained in the PaperMono record |
| Documentation prose | Marketing copy; no stated licence |
| ⚠ Bundled third-party code | **Check upstream licences separately.** The MIT-licensed PaperMono demo pins **RadioLib**, which is **LGPL-3.0 upstream**. Flagged, not resolved |

## 9. Products documented with this guide

- [**M5Stack PaperMono (C153)**](../../devices/m5stack/papermono/README.md) — the pass that
  produced these findings
- M5Stack PaperMono-Lite (C153-LITE) — covered inside the PaperMono record as a variant;
  it has no record of its own at the snapshot date
- [**M5PM1**](../../components/m5stack/m5pm1/README.md) — custom power manager; the
  bilingual library header and the CN-only datasheet delta both came from this part
- [**M5IOE1**](../../components/m5stack/m5ioe1/README.md) — custom I/O expander; likewise
- [Stamp-LoRa-1262](../../components/m5stack/stamp-lora-1262/README.md) — the module for
  which **no vendor datasheet exists at all**, a useful negative

Related vendor guide: [`vendors/dke`](../dke/README.md) — for the e-paper panel manual
M5Stack mirrors, which has its own retrieval trap.

## 10. Change log

| Date | Change |
|---|---|
| 2026-09-01 | Guide created during the PaperMono (C153) pass. Established: `docs.m5stack.com` is server-rendered HTML (not an SPA); lowercase slugs 302 to CamelCase while underscore/concatenated forms 404; the three language trees are faithful translations **except** that `zh_CN` links CN-only datasheets for M5Stack's own custom chips; the two OSS buckets and the numeric-product-id scheme (PaperMono = `1267`), including variant assets living under the parent id; the `static/pdf/static/<lang>/…` per-page renders; the M5Burner `/api/v1` public API versus the 401 on `/api`, and the numeric CDN object name that does not match `binFileName`; `M5_Hardware` stops at C152 with no C153 entry as of 2026-08-17, so absence there proves nothing; `/en/certification` and `/en/product_i2c_addr` are soft **gaps** requiring a positive control; Shopify 404s are 389,759 bytes with a **per-request hash**, defeating hash-based detection; `community.m5stack.com` search is 401 auth-walled. |

---

## 11. Findings added by the DinMeter (K134 / K134-V11) pass — 2026-09-04

*Appended 2026-09-04. Nothing above was altered. Everything below was live-probed on that date,
with negative controls, during the pass that produced
[`devices/m5stack/dinmeter`](../../devices/m5stack/dinmeter/README.md) and
[`devices/m5stack/dinmeter-v1.1`](../../devices/m5stack/dinmeter-v1.1/README.md).*

### 11.1 ⚠ The single biggest trap: M5Stack re-serves old assets under new product names

**Hash every artifact at acquisition time. This trap is invisible any other way.**

| Asset | v1.0 URL | v1.1 URL | SHA-256 |
|---|---|---|---|
| DinMeter schematic | `…/500/DIN_Meter_v1.0.pdf` | `…/1211/K134-V11_DIN_Meter_v1.0_2025_11_25_17_15_58.pdf` | **identical** `03ec3353…6e4c070` |
| DinMeter structure STL | `Products/K134_DinMeter/…/DinMeter.stl` | `Products/K134-V11_DinMeter_v1.1/…/DinMeter_v1.1.stl` | **identical** `90f04d6a…` |
| Stamp structure STL | `Products/S007_Stamp-S3/…/Stamp-S3.stl` | `Products/S007-V033_Stamp-S3A/…/Stamp-S3A.stl` | **identical** `f72c1af2…` |
| DinMeter dimension drawing | `…/1211/K134-din_meter_asm_v1.pdf` | **the same URL** | — |

Three different products, two different SKUs each, and in every case the same bytes. Note the
v1.1 schematic's own filename contains `_v1.0_`.

**What it licenses you to conclude:** the vendor has published no revision-specific
documentation. **Not** that the hardware is unchanged.

**Method:** `sha256sum` everything on download, and diff hashes across revision pairs *before*
writing anything. Two `sha256sum` invocations produced three of that pass's central findings.

### 11.2 ⚠ `m5stack-doc` bucket paths are numeric product ids — and they are not the SKU

`https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/<numeric-id>/<filename>`

Observed ids: DinMeter v1.0 schematic `500`; DinMeter v1.1 + dimensions `1211`; Stamp-S3
schematic `522`; Stamp-S3A `1150`; Stamp-S3A 1.27-pin variant `686`; Stamp-S3 pin map `684`;
ESP32-S3 datasheet mirror `472`.

Consistent with §2's PaperMono `1267`. **Variant assets do not always live under the parent id**
here: Stamp-S3A base is `1150` while its 1.27-pin variant is `686`. Read the ids off the rendered
page rather than guessing.

### 11.3 Product-page id patterns — verified, with negative controls

| Probe | Result |
|---|---|
| `/en/core/M5DinMeter` | **200** ← the v1.0 page |
| `/en/core/DinMeter` | **404** ← the obvious guess is wrong |
| `/en/core/DinMeter_v1.1` | **200** ← the v1.1 page uses a *different* naming convention from v1.0 |
| `/en/core/StampS3` | **200** |
| `/en/stamp/StampS3` | **404** |
| `/en/stamp/{Stamp-S3A,M5StampS3,stamps3,StampS3A}` | **404** ×4 |
| `/en/core/Stamp-S3A` | **200** |

**Two lessons.** (1) Core modules live under `/en/core/`, **not** `/en/stamp/` — despite
`/en/stamp/` existing and hosting other Stamp products. (2) M5Stack does **not** use one naming
convention per product family: `M5DinMeter` for v1.0 but `DinMeter_v1.1` for v1.1, `StampS3` but
`Stamp-S3A`. **Do not guess a page id. Use the sitemap (§11.4).**

### 11.4 ✅ `sitemap.xml` is the reliable enumeration route — the `/en/products` index is not

| Probe | Result |
|---|---|
| `https://docs.m5stack.com/sitemap.xml` | **200**, 499 000 B, **5 703 `<loc>` entries** |
| `https://docs.m5stack.com/en/sitemap.xml` | **404** |
| `https://docs.m5stack.com/sitemap_index.xml` | **404** |
| `https://docs.m5stack.com/en/products` | **200**, 565 615 B — but a **JavaScript shell** containing **no product links** in the served HTML |

The `/en/products` index that appears to list every product is useless to a fetcher. The
sitemap has everything.

```bash
curl -sS -A "$UA" https://docs.m5stack.com/sitemap.xml \
| grep -o '<loc>[^<]*</loc>' | sed 's/<[^>]*>//g' | grep -i '<product-name>'
```
Filtering for `Din` returned **6** URLs and immediately exposed the two page-id conventions plus
the 9 `/en/arduino/m5dinmeter/*` tutorial pages and 1 `/en/uiflow2/m5dinmeter/program`.

### 11.5 ✅ Product-page content *is* in the served HTML — but only from `id="document"`

Consistent with §1. The pages are Nuxt/Vue shells whose content is nonetheless server-rendered
inside a `<div id="document">`. Naive tag-stripping over the whole document yields ~5 KB of
navigation chrome and loses the specification table.

**Slice from the anchor first**, then strip:
```python
i = raw.find('id="document"'); seg = raw[i:] if i > 0 else raw
seg = re.sub(r'(?is)<script\b.*?</script>', ' ', seg)
seg = re.sub(r'(?i)</(p|div|tr|li|h[1-6]|table|td|th)>', '\n', seg)
seg = html.unescape(re.sub(r'(?s)<[^>]+>', '', seg))
```
This recovered the complete specification table, PinMap, Learn sections, datasheet list and
product-comparison table from both DinMeter pages.

### 11.6 ✅ Per-page printable renders — path template confirmed on a second product family

`https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/static/pdf/static/<lang>/<section>/<PageId>.pdf`

Verified: `…/static/en/core/M5DinMeter.pdf` (200, 7 459 888 B) and
`…/static/en/core/DinMeter_v1.1.pdf` (200, 11 261 000 B). `<PageId>` is the **page id**, not the
SKU or the product name — so §11.3's naming inconsistency propagates here.

⚠ **These are re-rendered per request**, so the bytes are not stable across fetches even when the
content is. Do not use their hash as a change detector.

### 11.7 ⚠ Chip datasheets are filed under *product* paths

`https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/core/M5DinMeter/tp4057.pdf`

The TP4057 is a chip, not a DinMeter part — yet M5Stack files its datasheet under the board's
directory. Likewise the DinMeter's DC-terminal and battery-socket datasheets are served from
**`…/products/core/M5Dial/…`**, a *different product's* path.

**Consequences for a fetcher:** (a) a chip datasheet may only exist under some unrelated board's
directory, so search the rendered page's links rather than guessing a `datasheet/` path; (b) when
filing locally, ignore the vendor's path and file by **what the document describes**.

Also confirmed: the Stamp-S3A page links `…/datasheet/Stamp/**S007 StampS3**/MUN3CAD01-SC.pdf`
— the *predecessor's* directory — and that part is not on the Stamp-S3A schematic at all (§11.9).

### 11.8 ⚠ Shopify serves JPEG bytes under `.webp` URLs

`https://cdn.shopify.com/s/files/…/1_3a27efc4-….webp?v=1769738162` returns bytes beginning
`ff d8 ff e1 … Exif` — **JPEG**. Shopify content-negotiates the image format and ignores the
path extension.

**Validate by magic bytes, never by URL suffix**, and rename locally so the extension matches the
content. Four of four shop images in that pass were affected.

### 11.9 ⚠ Specification rows are carried over unedited between product generations

The Stamp-S3A page lists `DC-DC: MUN3CAD01-SC`. The string `MUN3CAD01` **does not occur anywhere**
in `Sch_StampS3_v0.3.3.pdf`; the designator `M2` is absent; the fitted part is an 8-ball buck with
`SW`/`VOS`/`VSEL1-3` and an external inductor, annotated `IOUT: 0~0.6A`.

Similarly, the Stamp-S3A's `26.0 × 18.0 × 4.7 mm` size contradicts a **byte-identical** STL and
the complete absence of a new KiCad footprint.

**Rule: treat M5Stack specification tables as marketing copy that lags the hardware. Where a
schematic exists, the schematic wins.** Cross-check every consequential row.

### 11.10 ✅ Shop `.js` JSON is the best source for SKU, price, lifecycle and launch date

`https://shop.m5stack.com/products/<slug>.js` returns Shopify's product JSON directly — far more
reliable than parsing the storefront, and it avoids §5's 389 kB-per-request-hash 404 problem.

Gives: `title`, `variants[].sku`, `price` (integer cents), `available`, `created_at`,
`published_at`, `tags`, `weight`, product and variant ids.

**Two high-value behaviours:**
- **M5Stack prefixes discontinued titles with `[EOL]`.** `"[EOL] M5Stack Din Meter w/ M5StampS3"`,
  `"[EOL] M5Stamp ESP32S3 Module"`. This is the cleanest lifecycle signal the vendor emits
  anywhere — it appears on **no documentation page**.
- **`published_at` is a usable launch-date proxy**, and it cross-checked exactly against an
  independent r/M5Stack announcement post for the DinMeter v1.1 (both 2026-01-30).

⚠ **Slugs are not predictable.** v1.0 is `m5stack-din-meter-**w**-m5stamps3`; v1.1 is
`m5stack-din-meter-v1-1-**with**-m5stamps3a`. `…-with-m5stamps3` **404s**. The working v1.0 slug
was recovered from a third-party README (`bmorcelli/Launcher`), not from M5Stack.

**Enumerate slugs instead of guessing**, with the brackets percent-encoded:
```bash
curl -sS -A "$UA" 'https://shop.m5stack.com/search/suggest.json?q=din+meter&resources%5Btype%5D=product&resources%5Blimit%5D=10'
```
A raw `[` makes curl fail with `curl: (3) bad range in position 70`.

### 11.11 ✅ Altium marker layer in M5Stack schematics — and its double-draw trap

M5Stack publishes Altium PDFs carrying an invisible marker layer (`CO<designator>`,
`PI<designator><pin>`, `NL<netname>`), which makes a full netlist recoverable. This was already
used for PaperMono; two additions from this pass:

1. **Altium draws the marker layer twice at identical coordinates.** Without glyph deduplication
   the two copies interleave and `PIJ10101` extracts as `PPIIJJ110011` — *human-legible and
   wrong*, the most dangerous kind of extraction failure. **Deduplicate on rounded
   `(x0, y0, x1, y1, char)` before grouping glyphs into words.**
2. **On a host with no poppler**, `pdfminer.six` (pure Python) works and can emit
   `pdftotext -bbox`-compatible XML. `pymupdf` installs but fails to import on NixOS
   (`libstdc++.so.6` missing).

Reusable parser:
[`devices/m5stack/dinmeter/artifacts/schematic/parse_dinmeter_sch.py`](../../devices/m5stack/dinmeter/artifacts/schematic/parse_dinmeter_sch.py).

### 11.12 ✅ `m5stack/M5_Hardware` — enumerate the tree; absence is informative

```bash
curl -sS -H "Authorization: Bearer $(gh auth token)" \
  'https://api.github.com/repos/m5stack/M5_Hardware/git/trees/master?recursive=1'
```
931 paths, **not truncated**, one call. Directory naming is `Products/<SKU>_<ProductName>/`, e.g.
`Products/K134_DinMeter/`, `Products/K134-V11_DinMeter_v1.1/`, `Products/S007-V033_Stamp-S3A/`.

Contrary to §3's PaperMono finding that the repo stops at C152: **it does carry DinMeter and
Stamp entries**, so its coverage is patchy by product rather than by date. Check, do not assume.

Most products get **only** `Structures/*.stl`. KiCad footprints exist for a *subset*
(`Stamp-S3-SMD`, `Stamp-S3-DIP`, `Stamp-S3_PIN1.27_Socket`, `Stamp-S3_PIN2.54_DIP`) — and
notably **no `Stamp-S3A` footprint at all**, which is itself evidence for footprint compatibility.
The repository has **no `LICENSE` file** (checked 2026-09-04).

### 11.13 ✅ Espressif's `esp-board-manager` is a better technical source than M5Stack's own docs

`espressif/esp-board-manager` → `m5stack_boards/<board>/{board_info,board_devices,board_peripherals}.yaml`.
For the DinMeter it documented the ST7789 GRAM offset, the PCNT quadrature pattern, an
ESP32-S3-specific build break, and resolved an ambiguity in M5Stack's own pin table by citing
M5Unified source — none of which appears in M5Stack's documentation.

**Check it for every M5Stack board.** Caveat: its headers cite M5Stack's PinMap as its source, so
where it merely restates that table it is a *reproduction*, not independent corroboration.

### 11.14 ⚠ `community.m5stack.com` remains auth-walled — confirmed again

| Probe | Result |
|---|---|
| `…/api/search?term=<x>&in=titlesposts` | **HTTP 401** — `{"status":{"code":"not-authorised",…}}` |
| `…/search?term=<x>&in=titlesposts` (browser UA) | **200**, but a NodeBB **JS shell** with no results in the served HTML |

Independently confirms §5. **Rotating User-Agents must not be attempted** — this is
authentication, not bot-blocking, and the repository's retrieval policy forbids UA substitution
to bypass access controls. Treat M5Stack forum threads as a **blocked** source and say so.

### 11.15 Products documented with these additions

- [**M5Stack DinMeter (K134)**](../../devices/m5stack/dinmeter/README.md)
- [**M5Stack DinMeter v1.1 (K134-V11)**](../../devices/m5stack/dinmeter-v1.1/README.md)
- [**Stamp-S3 (S007)**](../../components/m5stack/stamp-s3/README.md) and
  [**Stamp-S3A (S007-V033)**](../../components/m5stack/stamp-s3a/README.md) — the pair that
  produced §11.1, §11.9 and §11.12

### 11.16 Change log addendum

| Date | Change |
|---|---|
| 2026-09-04 | Appended §11 during the DinMeter (K134 / K134-V11) pass. New: the re-served-asset trap and the hash-everything rule; `m5stack-doc` numeric ids for six more products; page-id naming is inconsistent *within* a product family, with `/en/stamp/` 404 negative controls; `sitemap.xml` works while `/en/products` is a link-free JS shell; the `id="document"` slicing recipe; per-page PDF renders confirmed on a second family and shown to be non-byte-stable; chip datasheets filed under unrelated *product* paths; Shopify serving JPEG under `.webp`; specification rows carried over unedited between generations; shop `.js` as the lifecycle source with the **`[EOL]` title prefix** and unpredictable slugs; the Altium **double-draw** glyph trap and the `pdfminer.six`-on-NixOS workaround; `M5_Hardware` coverage patchy by product, not by date, and no `Stamp-S3A` footprint; `esp-board-manager` as a superior technical source; forum 401 re-confirmed. |
