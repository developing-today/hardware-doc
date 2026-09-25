# PaperMono — research log

> **Search cutoff: 2026-09-01 (UTC).** Nothing published after that date is in
> this record. Every query below was executed on 2026-09-01 unless a row says
> otherwise. **No query, fetch or command in this pass touched physical
> hardware.**

This is the ledger of *what was looked for and what came back*, including the
things that came back empty. It exists so that a later pass can tell the
difference between "not found" and "not looked for", and does not repeat 94
queries to rediscover that Hackaday published nothing.

Companion documents: [`sources.md`](sources.md) (what was kept, with IDs) ·
[`commands.md`](commands.md) (what was run, with execution status) ·
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) (what disagrees).

## Contents

- [Disposition key](#disposition-key)
- [Method — the user-agent ladder](#method--the-user-agent-ladder)
- [Pass 1 — vendor documentation](#pass-1--vendor-documentation-docsm5stackcom)
- [Pass 2 — vendor storefront](#pass-2--vendor-storefront-shopm5stackcom)
- [Pass 3 — M5Burner firmware distribution](#pass-3--m5burner-firmware-distribution)
- [Pass 4 — vendor source repositories](#pass-4--vendor-source-repositories-github)
- [Pass 5 — community, social, forums, news](#pass-5--community-social-forums-news)
- [Pass 6 — retailers and distributors](#pass-6--retailers-and-distributors)
- [Pass 7 — press, video and third-party code](#pass-7--press-video-and-third-party-code)
- [Dead links and recovery attempts](#dead-links-and-recovery-attempts)
- [Retrieval findings worth reusing](#retrieval-findings-worth-reusing)
- [Not attempted, and why](#not-attempted-and-why)
- [Stopping criterion](#stopping-criterion)
- [Query-count summary](#query-count-summary)

## Disposition key

| Disposition | Meaning |
|---|---|
| **useful** | Retrieved and admitted as evidence; appears in [`sources.md`](sources.md) |
| **duplicate** | Retrieved, but the same content already held by a better path |
| **rejected** | Retrieved and **not** admitted — re-syndication, noise, or a body that is not what the status code implies |
| **inaccessible** | Bot-walled, auth-walled or a JavaScript shell. **No determination possible** — this is *not* a negative |
| **dead** | 404 / 302-to-nowhere / subreddit gone |
| **negative-confirmed** | Successfully retrieved, with full content, and the thing sought is **genuinely absent**. A result, not a failure |

The distinction between **inaccessible** and **negative-confirmed** is the most
load-bearing thing in this file. Mouser returning a bot-wall (§6) and Adafruit
returning "No products found" (§6) look similar in a terminal and mean opposite
things.

## Method — the user-agent ladder

Applied in order, stopping at the first HTTP 200 with a plausible body:

```
curl/8.5.0
  → Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
  → WhatsApp/2.23.20.0
  → Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot
  → Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ClaudeBot/1.0; +claudebot@anthropic.com
```

Two honest caveats about that ladder:

- **`curl/8.5.0` is a hardcoded string, not this host's real default.** The
  documenting host runs curl **8.21.0**. The first rung is therefore a *chosen*
  identity like every other rung, and "plain curl worked" in this log means "a
  request identifying itself as `curl/8.5.0` worked".
- A 200 obtained on a later rung is **not** evidence that the resource works
  normally for ordinary clients. Where that distinction mattered — the vendor's
  own sites — it is stated: `docs.m5stack.com`, `shop.m5stack.com` and
  `burner.m5stack.com` all served 200 to the **first** request.

Helpers: [`archive/devices/m5stack/papermono/artifacts/research-scratch/docs/_tools/fetch.sh`](../../../archive/devices/m5stack/papermono/artifacts/research-scratch/docs/_tools/fetch.sh)
(single-UA, records status/bytes/sha256/date to a `.meta` sidecar) and
`archive/devices/m5stack/papermono/artifacts/research-scratch/market/_raw/fetch.sh` (rotates the ladder and prints
the status of every rung).

## Pass 1 — vendor documentation (`docs.m5stack.com`)

Chrome 131 UA throughout; no fallback required on any page.

| # | Exact query / endpoint | Filters | HTTP | Result depth | Disposition | Notes → ID |
|---|---|---|---|---|---|---|
| 1.1 | `/en/core/PaperMono` | — | 200 | 153 939 B, full page | **useful** | → S01 |
| 1.2 | `/en/core/PaperMono-Lite` | — | 200 | 151 608 B | **useful** | → S04. Basis of the whole variant record |
| 1.3 | `/zh_CN/core/PaperMono` | — | 200 | 152 668 B | **useful** | → S02. The only substantive delta is CN-language datasheet links |
| 1.4 | `/ja/core/PaperMono` | — | 200 | 156 234 B | **useful** | → S03 |
| 1.5 | `/zh_CN/core/PaperMono-Lite` | — | 200 | 150 365 B | **useful** | → S05 |
| 1.6 | `/ja/core/PaperMono-Lite` | — | 200 | 153 791 B | **useful** | → S06 |
| 1.7 | `/en/arduino/papermono/program` | — | 200 | 321 758 B | **useful** | → S07 |
| 1.8 | `/en/arduino/papermono/m5pm1_m5ioe1` | — | 200 | 416 888 B | **useful** | → S08. Richest single vendor page |
| 1.9 | `/en/uiflow2/papermono/program` | — | 200 | 265 217 B | **useful** | → S09 |
| 1.10 | `/en/products` | — | 200 | 560 714 B | **useful** | → S10. Confirms exactly two SKUs |
| 1.11 | `/en/certification`, full-text search for `PaperMono`, `C153` | — | 200 | 382 669 B, **0 / 0 matches** | **negative-confirmed** | → S11 |
| 1.12 | `/en/product_i2c_addr`, full-text search for `PaperMono`, `C153` | — | 200 | 312 908 B, **0 / 0 matches** | **negative-confirmed** | → S12 |
| 1.13 | `/en/history` | — | 200 | 137 555 B | **useful** | → S13. Both SKUs dated 2026-08-20, category "Controllers" |
| 1.14 | `/en/core/PaperS3` | — | 200 | 30 KB | **useful** | Verified every claim in the community's PaperS3 comparison |
| 1.15 | `/en/core/PaperColor` | — | 200 | 30 KB | **useful** | Lineage context: Spectra 6, 400×600, 1250 mAh |
| 1.16 | `/en/core/CoreInk` | — | 200 | — | **useful** | Lineage context |
| 1.17 | `/en/core/Paper` | — | **404** | — | **dead** | The original M5Paper has no page at this slug. See [dead links](#dead-links-and-recovery-attempts) |
| 1.18 | `/en/core/{papermono,papermono-lite,CoreInk}` (lower case) | — | **302** | — | *note* | Slugs are case-sensitive; lower case redirects to CamelCase. Not an error, but it silently rewrites your URL |
| 1.19 | `/en/core/{papermono_lite,PaperMonoLite}` | — | **404** | — | **dead** | Underscore and concatenated forms do not exist |
| 1.20 | Full-text search of the extracted S09 text for a firmware version, a block list, or a limitation | — | — | **0 matches** | **negative-confirmed** | UiFlow2 support is advertised and undocumented. **Verified by search, not assumed** |
| 1.21 | Cross-language diff: table-row counts, `G\d+` / `PYG\d+` / `0x..` token sets, numeric specs, asset URL sets across all six product pages | — | — | 89/89/89 rows; **empty symmetric difference** on tokens in all four language pairs | **useful** | Establishes the three languages are faithful translations — so the frontlight naming defect is in the *source content*, not a translation error |

### Vendor design artifacts and datasheets

| # | Exact endpoint | HTTP | Depth | Disposition | Notes → ID |
|---|---|---|---|---|---|
| 1.22 | `m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1267/PaperMono_SCH_V0.6.2_20260522.pdf` | 200 | 1 462 039 B, 6 sheets | **useful** | → S14 |
| 1.23 | `…/1267/C153_PaperMono_model_size.pdf` | 200 | 21 346 B, 1 page | **useful** | → S15 |
| 1.24 | `…/472/esp32-s3_datasheet_en.pdf` | 200 | 1 083 807 B, 84 pp | **useful** | → S18 |
| 1.25 | `m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/app/Stamp%20Fly/BMI270.PDF` | 200 | 3 830 973 B, 162 pp | **useful** | → S19. Note the path: a **Stamp Fly** asset, which is how it went five years stale |
| 1.26 | `…/1267/SSD1677.pdf` | 200 | 3 602 487 B, 46 pp | **useful** | → S20 |
| 1.27 | `…/1267/EPD_Module_User_Manual.pdf` | 200 | 8 666 208 B, 30 pp | **useful** | → S21 |
| 1.28 | `…/1132/RX8130CE_cn-Register-Datasheet.pdf` | 200 | 2 283 323 B, 70 pp | **useful** | → S22. Filename says `_cn`; content is the English ETM50E-09 |
| 1.29 | `…/1205/ST25R3916_EN.pdf` | 200 | 2 241 765 B, 160 pp | **useful** | → S23 |
| 1.30 | `…/1177/DS_SX1261_2_V2-2.pdf` | 200 | 4 459 535 B, 118 pp | **useful** | → S24. Describes the **chip**; no module datasheet exists |
| 1.31 | `…/1207/M5PM1_Datasheet_EN.pdf` | 200 | 814 731 B, 35 pp | **useful** | → S25 |
| 1.32 | `…/1210/IO_Expander_Datasheet_EN.pdf` | 200 | 398 463 B, 12 pp | **useful** | → S26 |
| 1.33 | `…/1268/PaperMono-Lite_PRJ_V0.6.2_20260522.pdf` | — | — | **not attempted** | URL harvested from S04 only. → S16. **The highest-value untaken lead for the Lite** |
| 1.34 | `…/1268/C153-Lite_PaperMono-Lite_model_size.pdf` | — | — | **not attempted** | → S17 |
| 1.35 | `…/1207/M5PM1_Datasheet_CN.pdf`, `…/1210/IO_Expander_Datasheet_CN.pdf`, `…/1205/ST25R3916_ZH.pdf`, `…/472/esp32-s3_datasheet_cn.pdf` | — | — | **not attempted** | zh_CN-only variants harvested from S02. → S27–S30. A CN↔EN diff of the two M5-designed chips' manuals is the best remaining route to settling the pin-nomenclature question |
| 1.36 | `…/1267/C153-PaperMono-UserDemo_0x00.exe` | — | — | **not attempted** | Windows executable, out of scope. → S40. **The finding is that both product pages link the same file, under `1267/`** |

## Pass 2 — vendor storefront (`shop.m5stack.com`)

Plain `curl/8.5.0` was sufficient throughout — no UA rotation needed.

| # | Exact query | HTTP | Depth | Disposition | Notes |
|---|---|---|---|---|---|
| 2.1 | `/search/suggest.json?q=papermono&resources[type]=product&resources[limit]=10` | 200 | 2 products | **useful** | Both SKUs, prices, `available:false` |
| 2.2 | `/search?q=papermono` | 200 | 448 043 B, 4 results | **useful** | → S51. **The only way the real handles were found** |
| 2.3 | `/search?q=paper` | 200 | 521 KB | **useful** | Enumerated the whole e-paper line including PaperColor and every EOL M5Paper variant |
| 2.4 | `/products/m5papermono-with-lora-nfc-800x480-3-97-eink-display` and `.json` | 200 ×2 | 703 507 / 20 925 B | **useful** | → S48 |
| 2.5 | `/products/papermono-lite-dev-kit-800x480-3-97-e-ink-display` and `.json` | 200 ×2 | 693 406 / 19 938 B | **useful** | → S49 |
| 2.6 | `/products/<handle>.json` × 8 handles across the e-paper lineage | 200 ×8 | full | **useful** | `sku`, `price`, `created_at`, `published_at` for the complete family table |
| 2.7 | `/products/papermono` | **404** | 389 759 B | **dead** | Handle does not exist |
| 2.8 | `/products/papermono-lite` | **404** | 389 759 B | **dead** | Handle does not exist |
| 2.9 | `/products/m5stack-papermono` | **404** | 389 759 B | **dead** | Handle does not exist |
| 2.10 | `/blogs/news/m5stack-launches-papermono-…` | 200 | 448 198 B | **useful** | → S50. `<time datetime="2026-08-21">`; this theme emits no JSON-LD `datePublished` |
| 2.11 | `/blogs/news.atom` | 200 | 30 entries, back to 2021 | **useful** | → S52 |
| 2.12 | `m5stack.com/distributor` | 200 | 101 KB, 37 domains extracted | **useful** | → S56. Seed list for pass 6 |

> **The three 404s are worth a note.** All three returned **exactly 389 759 bytes**
> with **three different SHA-256 values** — a templated Shopify 404 carrying a
> per-request nonce. Byte-length equality is not content equality; hash them.

## Pass 3 — M5Burner firmware distribution

| # | Exact endpoint | HTTP | Depth | Disposition | Notes |
|---|---|---|---|---|---|
| 3.1 | `burner.m5stack.com/firmware/2089640807996628993/` | 200 | 2 735 B | **useful (weakly)** | → S31. React shell, empty `<div id="root">`; only the `og:` tags carry information |
| 3.2 | `burner.m5stack.com/firmware/2091144466157694978/` | 200 | 3 407 B | **useful (weakly)** | → S32 |
| 3.3 | `/assets/index-DpEo0Py5.js` → `/assets/http-ChO34QIa.js` → `/assets/firmware-C6nFrscE.js` | 200 ×3 | 230 198 / 47 846 / 17 403 B | **useful** | → S37. Reversed to recover the API base and the endpoint shapes |
| 3.4 | `/api/firmwares/2089640807996628993` | **401** | `{"msg":"请先登录"}` | **inaccessible** | The obvious path is auth-walled |
| 3.5 | `/api/v1/firmwares/2089640807996628993` | 200 | 1 209 B | **useful** | → S33. **`/api/v1` is public where `/api` is not** |
| 3.6 | `/api/v1/firmwares/2089640807996628993/versions` | 200 | 641 B | **useful** | → S34 |
| 3.7 | `/api/v1/firmwares/2091144466157694978` and `/versions` | 200 ×2 | 1 460 / 638 B | **useful** | → S35, S36 |
| 3.8 | `/api/v1/firmwares/{id}/versions/{vid}/download` ×2 | **302** → CDN, then 200 | 2 868 208 / 10 319 500 B | **useful** | → S38, S39. Both validated by content before being given a `.bin` extension |

## Pass 4 — vendor source repositories (GitHub)

Authenticated through `gh auth token` (5 000 req/h). The token was never printed
and is not recorded anywhere in this repository.

| # | Exact query / command | Depth | Disposition | Notes |
|---|---|---|---|---|
| 4.1 | `gh api repos/m5stack/{M5PaperMono-UserDemo,M5PaperMono-OTP-Demo,M5PM1,M5IOE1,M5_Hardware}` | 5 repos | **useful** | All five exist, are public, none empty → S41–S45 |
| 4.2 | `git clone` of the four small repos + `--filter=blob:none --no-checkout` for `M5_Hardware` | full trees | **useful** | The blobless clone was a deliberate size choice: 348 KB against ~127 MB |
| 4.3 | `git -C M5_Hardware ls-tree -r --name-only HEAD \| grep -iE 'papermono\|c153'` | 369-file tree | **negative-confirmed** | **0 matches.** → S45 |
| 4.4 | `… \| grep -i 'paper'` | same | **negative-confirmed** | 3 matches, none C153 (`C139_PaperS3`, `C151_PaperColor`, `K049-B_Paper_v1.1`) |
| 4.5 | `… \| grep -oE 'C1[0-9]{2}' \| sort -u \| tail` | same | **useful** | SKU sequence reaches **C152** and stops. The gap is at exactly the right place to be meaningful |
| 4.6 | `git clone` M5Unified and M5GFX, then `fetch origin develop:develop` | both branches | **useful** | → S46, S47 |
| 4.7 | `git -C M5GFX grep -n 'board_M5PaperMono' master -- src/lgfx/boards.hpp` | — | **useful** | Board support is on `master`, refuting the vendor's `#develop` requirement |
| 4.8 | `git -C M5Unified grep -q 'board_M5PaperMono' 0.2.21 -- src/` and the same for M5GFX `0.2.28` | — | **useful** | Support ships in the **released tags** |
| 4.9 | `grep -rE 'GPIO_NUM_0\b' main/` in the UserDemo | 2 hits | **useful** | Both benign; the `G0_BOOT_OUT` path is never exercised by the demo |

**A search that was *not* run and should have been:** no commit SHA was recorded
for any **third-party** repository (S89–S96). Those citations are therefore not
pinned and cannot be re-resolved byte-for-byte. Recorded as a defect of this pass.

## Pass 5 — community, social, forums, news

| # | Service | Exact query | Filters | UA | HTTP | Depth | Disposition | Notes |
|---|---|---|---|---|---|---|---|---|
| 5.1 | old.reddit.com | `/search.json?q=papermono&sort=new&limit=100` | site-wide, `sort=new` | WhatsApp/2.23.20.0 | 200 | 100 requested, **2 returned** | **useful (scarcity)** | Both results are bot mirrors (r/hackernews, r/hypeurls). **That is the entire site-wide footprint** |
| 5.2 | old.reddit.com | `/r/{esp32,eink,M5Stack,ereader}/search.json?q=papermono&restrict_sr=1&t=all` | per-sub, all time | WhatsApp | 200 ×4 | 100 requested each | **negative-confirmed** | **0 results in every subreddit — including r/M5Stack** |
| 5.3 | old.reddit.com | same four subs, `q=paper mono` | per-sub, all time | WhatsApp | 200 ×4 | 100 each | **useful** | **Tokenisation gotcha:** the spaced form returned the two real r/M5Stack threads that `papermono` missed entirely. r/esp32 (5 hits) and r/eink (3) were unrelated. → S70, S71 |
| 5.4 | old.reddit.com | `/r/M5Stack/comments/1vquxa5/….json?limit=60` | full comment tree | WhatsApp | 200 | 22 comments | **useful** | → S70 |
| 5.5 | old.reddit.com | `/r/M5Stack/comments/1vuaneb/….json?limit=60` | full comment tree | WhatsApp | 200 | 17 comments | **useful** | → S71. Produced the openelab.de lead |
| 5.6 | old.reddit.com | `/r/{CrossPointReader,einkesp32}/search.json?q=papermono` | per-sub | WhatsApp | 200 ×2 | 100 each | **negative-confirmed** | 0 in both — **including the CrossPoint community that lists PaperMono on its own roadmap** |
| 5.7 | old.reddit.com | **second broad pass**: `M5Stack e-ink`, `papermono lite`, `M5 PaperMono`, `C153 m5stack` | `t=year` | WhatsApp | 200 ×4 | 100 each | **useful (scarcity)** | 24 / 0 / 7 / 0 results. **Only new item was a thread already found.** This is the pass that made the scarcity conclusion defensible |
| 5.8 | hn.algolia.com | `/api/v1/search?query=papermono&hitsPerPage=50` | — | curl | 200 | 9 hits | **useful** | 2 real submissions; the rest false positives (fonts, "Papermoon") |
| 5.9 | hn.algolia.com | `/api/v1/search?query="M5Paper"&hitsPerPage=50` | — | curl | 200 | 42 hits | **useful (context)** | Historical HN interest in the line, 2020–2021 |
| 5.10 | hn.algolia.com | `/api/v1/items/49468593` | — | curl | 200 | **full nested tree, 58 comments in one request** | **useful** | → S68. Also surfaced the two X URLs |
| 5.11 | api.fxtwitter.com | `/M5Stack/status/2091116748686922069` | — | Chrome | 200 | full JSON | **useful** | → S74. Vendor restock statement, verbatim |
| 5.12 | api.fxtwitter.com | `/henry19840301/status/2090652363434647738` | — | Chrome | 200 | full JSON | **useful** | → S72 |
| 5.13 | api.fxtwitter.com | `/i/status/2091105450494238837` (chain parent) | — | Chrome | 200 | full JSON | **useful** | → S73. **This is the fetch that disproved the "e-ink driver IC" attribution** |
| 5.14 | api.fxtwitter.com | `/i/status/2091070115001315474` (chain root) | — | Chrome | 200 | full JSON | **useful** | → S75 |
| 5.15 | x.com | `/M5Stack/status/…`, `/henry19840301/status/…` direct | — | Chrome | 200 | 132 / 188 KB | **rejected** | Gzipped JS shell; `grep` reports "binary file matches". Superseded by 5.11–5.14 |
| 5.16 | community.m5stack.com | `/api/search?term=papermono&in=titlesposts` | — | Chrome | **401** | — | **inaccessible** | `{"code":"not-authorised"}` |
| 5.17 | community.m5stack.com | `/search?term=papermono` | — | Chrome | **302** | — | **inaccessible** | Redirects to login |
| 5.18 | community.m5stack.com | `/api/recent` | — | Chrome | 200 | 198 topics | **negative-confirmed (narrow)** | Open, and no PaperMono topic in the recent window. **A window is not a search** — → S85 |
| 5.19 | public.api.bsky.app | `/xrpc/app.bsky.feed.searchPosts?q=papermono&limit=50` | — | curl, Chrome, WhatsApp | **403** ×3 | — | **inaccessible** | → S86. No working UA found |

## Pass 6 — retailers and distributors

Seed list: the 37 domains extracted from `m5stack.com/distributor` (2.12).

| # | Seller | Exact query | UA | HTTP | Disposition | Result |
|---|---|---|---|---|---|---|
| 6.1 | shop.m5stack.com | see pass 2 | curl | 200 | **useful** | USD 65.00 / 55.00, both out of stock |
| 6.2 | openelab.de | `/search/suggest.json?q=papermono` | Chrome | 200 | **useful** | EUR 79.95, "Vorverkauf" |
| 6.3 | openelab.io | `/search/suggest.json?q=papermono` | Chrome | 200 | **useful** | EUR 79.95, "Pre-sale" |
| 6.4 | openelab.{io,de} | `/products/….json` | Chrome | 200 ×2 | **useful** | SKU `M5-C153`, barcode, listing timestamps → S54, S55 |
| 6.5 | thepihut.com | `/search/suggest.json?q=papermono` | Chrome | 200 | **useful** | GBP 62.40, `available:false` |
| 6.6 | thepihut.com | `/products/m5stack-papermono` + `.json` | Chrome | 200 ×2 | **useful** | `schema.org/OutOfStock`; incl./excl. VAT toggle confirmed in markup → S53 |
| 6.7 | **amazon.com** | `/s?k=m5stack+papermono` | Chrome **+ `--compressed`** | 200 | **negative-confirmed** | "5 results", none is PaperMono → S57. **The first attempt, without `--compressed`, returned raw gzip and was nearly misread as a block** |
| 6.8 | amazon.com | `/s?k=m5stack+m5paper` (control) | Chrome | 200 | **rejected** | 1 330-byte stub — rate-limited on the second consecutive query |
| 6.9 | **aliexpress.com** | `/w/wholesale-papermono.html` | Chrome | 200 | **negative-confirmed** | Only M5Stack **PaperColor** ($127.91 / $182.87). → S58 |
| 6.10 | aliexpress.com | `/w/wholesale-m5stack%20paper%20mono.html` | Chrome | 200 | **rejected** | 50 titles, all unrelated commodity parts — the query broke into noise |
| 6.11 | **switch-science.com** | `/search?q=PaperMono` | Chrome | 200 | **negative-confirmed** | 「PaperMono」の検索結果**0件** → S59 |
| 6.12 | switch-science.com | `/search/suggest.json?q=PaperMono` | Chrome | **417** | **inaccessible** | Expectation Failed; the HTML path works instead |
| 6.13 | **adafruit.com** | `/?q=papermono` | Chrome | 200 | **negative-confirmed** | "No products found for 'papermono'" → S60 |
| 6.14 | **reichelt.com** | `/index.html?ACTION=446&SEARCH=papermono` | Chrome | 200 | **negative-confirmed** | "Die Suche nach papermono hatte 0 Treffer" → S61 |
| 6.15 | **botland.store** | `/search?controller=search&s=papermono` | Chrome | 200 | **negative-confirmed** | 20 string matches, all locale-switch URL echoes; **0 products** → S62 |
| 6.16 | **core-electronics.com.au** | `/catalogsearch/result/?q=papermono` | Chrome | 200 | **negative-confirmed** | 0 products → S63 |
| 6.17 | mouser.com | `/c/?q=papermono` | Chrome | 200 (13.9 KB) | **inaccessible** | Bot-denial page, 0 content matches → S64 |
| 6.18 | digikey.com | `/en/products/filter/keyword?keywords=papermono` | Chrome | **403** | **inaccessible** | → S65 |
| 6.19 | tinytronics.nl | `/en/search?query=papermono`, `/search/suggest.json` | Chrome | **403** ×2 | **inaccessible** | → S66 |
| 6.20 | robu.in | `/search/suggest.json?q=papermono` | Chrome | **403** | **inaccessible** | → S67 |
| 6.21 | makerlab-electronics.com | `/search/suggest.json?q=papermono` | Chrome | 200 | **negative-confirmed** | 0 products |
| 6.22 | elektor.com | `/search/suggest.json?q=papermono` | Chrome | 200 | **negative-confirmed** | 0 products |
| 6.23 | berrybase.de | `/search?sSearch=papermono` | Chrome | 200 (8 MB) | **negative-confirmed** | 0 occurrences of the term in 8 MB of markup |
| 6.24 | core-electronics, botland, cytron, berrybase, mchobby | `/search/suggest.json` | Chrome | **404** ×5 | *note* | Not Shopify, or the endpoint is disabled — use each site's native search path |

### Competitor pricing (for the comparison sections)

| # | Service | Query | HTTP | Disposition | Result |
|---|---|---|---|---|---|
| 6.25 | soldered.com | `/search/suggest.json?q=inkplate`; `/products/inkplate-5-gen2.json` | 200 ×2 | **useful** | EUR confirmed from `Shopify.currency`. **Two variants** — board EUR 74.95, **with enclosure + battery EUR 99.95**; the bundle is the fair comparator against an enclosed device |
| 6.26 | lilygo.cc | `/search/suggest.json?q={t5,epaper}`; three `/products/….json` | 200 ×5 | **useful** | Per-variant LoRa band / GPS / region SKUs. `suggest.json`'s `price` is `price_min` and **understates the real range** |
| 6.27 | lilygo.cc | `/cart.js`, homepage, product page — currency probe | 301 / 200 | **inconclusive** | **No currency token in any fetched markup.** Recorded as "currency unconfirmed" rather than assumed USD |
| 6.28 | internal knowledge base | `devices/soldered-electronics/inkplate-5{,-gen2}`, `devices/zerowriter/zerowriter-ink`, `devices/nicolai-electronics/tanmatsu` | — | **useful** | Cited as internal cross-links; not re-researched |
| 6.29 | internal knowledge base | `devices/waveshare/` | — | **gap** | Existing records cover ESP32-P4/S3 **LCD** boards only, not the e-paper line. A same-diagonal Waveshare 3.97″ ESP32-S3 e-paper board demonstrably exists (r/eink, 2026-06-06) and is unpriced here |

## Pass 7 — press, video and third-party code

| # | Service | Exact query | Filters | HTTP | Depth | Disposition | Result |
|---|---|---|---|---|---|---|---|
| 7.1 | cnx-software.com | `/wp-json/wp/v2/search?search=papermono&per_page=20` | — | 200 | 1 hit | **useful** | Post id 175726 |
| 7.2 | cnx-software.com | `/wp-json/wp/v2/posts/175726` | — | 200 | full content | **useful** | `date` 2026-08-21T16:43:25, `modified` 08-22 → S77 |
| 7.3 | cnx-software.com | `/?s=papermono` (HTML) | — | 200 | 1 result | **duplicate** | Same article; the API path is strictly better |
| 7.4 | **hackaday.com** | `/wp-json/wp/v2/search?search=papermono&per_page=20` | — | 200 | **`[]`** | **negative-confirmed** | **Hackaday published nothing** → S84 |
| 7.5 | hackaday.com | `/wp-json/wp/v2/search?search=m5paper` | — | 200 | 2+ hits | **useful (context)** | 2021 weather display; 2026-07-21 "20 FPS on E-Paper Display Without Help" |
| 7.6 | hackster.io | `/search?q=papermono` | — | 200 (69 KB) | **inaccessible** | JS shell; all 11 term matches are login-redirect URLs |
| 7.7 | hackster.io | `/search.json?q=papermono`, `/api/v2/projects?search=papermono` | — | 200 / 404 | **inaccessible** | Both return HTML, not JSON. **No working path found** → S87 |
| 7.8 | youtube.com | `/results?search_query=M5Stack+PaperMono&sp=CAI%3D` | **sort: newest** | 200 | 20 videos | **useful** | Parsed `ytInitialData` for titles, channels, dates, view counts |
| 7.9 | youtube.com | `/watch?v=…` × 6 (`sRlGOgX9KOA`, `0-qQ0y-WEek`, `gX4cTpS2gUA`, `zTieK3pia6M`, `oPbOK90aJEo`, `cEkv_CP2SlU`) | — | 200 ×6 | full | **useful** | Exact `uploadDate`, `viewCount`, `shortDescription`. **Revealed the `?ref=` affiliate parameter in the only hands-on video** → S80–S82 |
| 7.10 | **mojeek.com** | `/search?q=papermono` | pages 1–5 | 200 | "243 results" | **useful** | → S88. **The only general web engine that worked.** Pages 2–5 were almost entirely Tux Machines re-syndication → **rejected** |
| 7.11 | html.duckduckgo.com | `/html/?q=papermono+m5stack` | — | **202** | 14 KB | **inaccessible** | Anomaly/challenge page. **Not a 403 — easy to mistake for success** |
| 7.12 | lite.duckduckgo.com | `/lite/?q="PaperMono"+review` | — | **202** | 14 KB | **inaccessible** | Same |
| 7.13 | search.marginalia.nu | `/search?query=papermono` | — | 200 | — | **inaccessible** | Bot-wait interstitial with a 5 s JS redirect. Unusable without JS |
| 7.14 | **linuxgizmos.com** | article URL | — | Chrome **403** → curl/8.5.0 **200** | full | **useful** | → S76. **Inverted UA behaviour** |
| 7.15 | liliputing.com | `/lilbits-more-phone-sized-e-ink-gadgets/` | — | 200 | full | **useful** | → S79. Contains the $55/NFC/LoRa conflation |
| 7.16 | muylinux.xyz | article URL | — | 200 | full | **useful** | → S78 |
| 7.17 | news.tuxmachines.org | ≥6 URLs surfaced by 7.10 | — | — | — | **rejected** | Verbatim aggregator re-syndication. Adds nothing; inflates counts |
| 7.18 | api.github.com | `/search/repositories?q=papermono&per_page=50` | — | 200 | 6 hits | **useful** | 4 third-party + 1 M5Stack + 1 unrelated font |
| 7.19 | api.github.com | `/search/repositories?q=M5PaperMono` | — | 200 | 3 hits | **useful** | Adds `hectorzin/M5PaperMono-HomeAssistant-ESPHome` → S93 |
| 7.20 | api.github.com | `/search/repositories?q=paper+mono` | — | 200 | **311 hits** | **rejected** | Dominated by "monocular … paper" ML repos. **Query too loose** — the spaced form that rescues a Reddit search ruins a GitHub one |
| 7.21 | api.github.com | `/search/code?q=PaperMono+in:file+-org:m5stack&per_page=30` | excl. `org:m5stack` | 200 | 1 196 hits, **15 read** | **useful** | Found S90, S94, S96. Many false positives from the "Paper Mono" *font* and from vendored copies of `M5Unified/…/LED_PaperMono_Class.*` |
| 7.22 | api.github.com | `/search/code?q=PaperMono+repo:bitbank2/bb_epaper` | — | 200 | **0** | **negative-confirmed** | → S97. **Contradicts the author's public 2026-08-17 support claim.** Left unresolved |
| 7.23 | raw.githubusercontent.com | `README.md` × 4 third-party repos | — | 200 ×4 | full | **useful** | Hardware-validation claims; `EggUncle`'s honest "not a device photo" disclaimer |
| 7.24 | raw.githubusercontent.com | `Free-Ink/freeink-sdk/…/PaperMonoBoard.h` | — | 200 | full | **useful** | → S90. Strongest code-level third-party hardware evidence — **but fetched without pinning a ref** |
| 7.25 | raw.githubusercontent.com | `crosspoint-reader/…/ROADMAP.md` | — | 200 | full | **useful** | → S94. Line 40 is a roadmap target, not shipped support |
| 7.26 | raw.githubusercontent.com | `bitbank2/bb_epaper/README.md` | — | 200 | full | **negative-confirmed** | 0 matches for `papermono`, `paper mono`, `papercolor` |
| 7.27 | freeink.org | `/` | — | 200 | 964 B | **rejected** | JS-only shell; the GitHub org is the usable source |

## Dead links and recovery attempts

| Target | What happened | Recovery attempted | Outcome |
|---|---|---|---|
| `docs.m5stack.com/en/core/Paper` | **404** — the original M5Paper has no page at this slug | Tried `/en/core/{papermono_lite,PaperMonoLite}` and the lower-case forms to establish the site's slug rules; queried the store instead | The store carries `K049` and `K049-B` listings, so the product is documented commercially but **not** at that docs slug. Left as `dead`; the docs page for the original M5Paper was **not** located |
| `shop.m5stack.com/products/{papermono, papermono-lite, m5stack-papermono}` | **404** ×3 | Recovered via `/search?q=papermono` (2.2) | **Recovered.** The real handles are `m5papermono-with-lora-nfc-800x480-3-97-eink-display` and `papermono-lite-dev-kit-800x480-3-97-e-ink-display` |
| `old.reddit.com/r/eink_displays/…` | **302** — subreddit does not exist or was renamed | Searched r/eink, r/esp32, r/ereader, r/CrossPointReader, r/einkesp32 instead | **Superseded**, not recovered. The renamed target was not identified |
| `burner.m5stack.com/firmware/<id>/` | 200 but content-free React shell | Read the SPA bundle to find the API; then `/api/firmwares/{id}` → 401; then `/api/v1/firmwares/{id}` → 200 | **Recovered in full** |
| `x.com/<user>/status/<id>` | 200 but a gzipped JS shell | `api.fxtwitter.com` | **Recovered in full**, including the reply chain |
| `www.hackster.io/search?q=papermono` | 200 but a JS shell; `/search.json` and `/api/v2/projects` both return HTML | Three paths tried | **Not recovered.** No working path found |
| `public.api.bsky.app/xrpc/…` | 403 to three UAs | Full ladder | **Not recovered.** One post is known only second-hand, from an embed inside S79 |
| `community.m5stack.com` search | 401 / 302 | `/api/recent` | **Partially recovered** — a 198-topic recent window, which is not a search |

**No Wayback submissions were made, and none were needed.** Every source in this
pass is a live, well-mirrored commercial, vendor or aggregator site; none meets
the "few copies online / fragile host" bar for archiving. The vendor's own PDF
assets on `m5stack-doc.oss-cn-shenzhen.aliyuncs.com` are the closest call — they
sit on a single CDN under numeric asset-folder ids that will be reused — and
submitting **S14, S16, S25, S26 and S27–S28** to `web.archive.org/save/` is a
reasonable next action for a future pass, particularly S16 and S27–S28, which
have not been retrieved here at all.

## Retrieval findings worth reusing

These generalise beyond this device. They belong in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md) as
well as here.

**Paths that work where the obvious one does not**

- **`api.fxtwitter.com/i/status/<id>` returns complete tweet JSON** — text,
  author, `created_at`, likes/views, and `replying_to_status` for chain-walking —
  where `x.com/<user>/status/<id>` serves a gzipped JS shell that `grep` reports
  as "binary file matches". The `/i/` form resolves a bare status id **without
  knowing the author handle**, which is what made it possible to walk from a
  quoted tweet up to its parent and root. That is exactly how the "e-ink driver
  IC shortage" claim was checked and found to be absent from the chain it cited.
  Chrome UA.
- **`burner.m5stack.com/api/v1/firmwares/{id}` is public; `/api/firmwares/{id}`
  is auth-walled** (`401 {"msg":"请先登录"}`). The version-neutral path looks like
  the canonical one and is the wrong one. `…/versions` and
  `…/versions/{vid}/download` follow the same rule; the download 302s to a
  numeric CDN object whose name is **not** the `binFileName` the API reports.
- **`old.reddit.com/search.json` with UA `WhatsApp/2.23.20.0` works where
  `www.reddit.com` returns 403.** Re-confirmed in this session.
- **`hn.algolia.com/api/v1/items/<id>` returns the entire nested comment tree in
  one unauthenticated request.** No UA needed.
- **WordPress `/wp-json/wp/v2/search` + `/posts/<id>`** is open on both
  `cnx-software.com` and `hackaday.com`, gives `date`, `modified` and full
  rendered content, and yields *machine-readable negatives* — an empty `[]` is a
  far stronger statement than an empty-looking search page.
- **Shopify storefronts leak more than they render.** `/products/<handle>.json`,
  `/search/suggest.json` and `/blogs/news.atom` are open on most Shopify stores
  and give `sku`, `price`, `created_at`, `published_at`. Additionally, stores
  running the **Stoq / RestockRocket** app embed
  `window._RestockRocketConfig.variantsInventoryQuantity` and
  `variantsInventoryPolicy` **directly in the product page HTML** — exact
  per-variant on-hand counts including negatives. That is where the `−129` came
  from. **`/search/suggest.json` is not universal**: 404 on non-Shopify stores,
  403 on some, and `price` there is `price_min`, which understates a multi-variant
  range.
- **`mojeek.com/search?q=` was the only general web search engine that worked**
  (Chrome UA) while DuckDuckGo HTML *and* Lite returned **HTTP 202** challenge
  pages and Marginalia served a JS bot-wait interstitial. Read the URLs, not the
  result count — aggregator re-syndication inflated it fivefold here.

**Gotchas that will cost you an hour**

- **`linuxgizmos.com` inverts the usual ladder: bare `curl/8.5.0` → 200, Chrome
  131 → 403.** The browser UA is not always the safe default. Always try the
  plain agent before concluding a site is hostile.
- **Reddit tokenises `papermono` and `paper mono` differently.** `papermono`
  returned **0** results in r/M5Stack while `paper mono` returned the two real
  threads. **Search both the closed-up and spaced spellings of any compound
  product name, in every subreddit.** The opposite holds on GitHub, where the
  spaced form (`paper mono`) returned 311 mostly-irrelevant hits.
- **`amazon.com/s?k=` needs `curl --compressed`.** Without it curl returns raw
  gzip that looks like binary garbage and reads exactly like a bot-block. Amazon
  was never blocking. It *does* rate-limit the second consecutive query to a
  ~1.3 KB stub, so budget one query per session.
- **`datasheet.lcsc.com` returns HTTP 200 with `Content-Type: text/html` for PDF
  URLs.** Status and content-type both lie. **Check the first bytes for `%PDF`**,
  not the response metadata — the same discipline applied to the firmware images
  here, which were checked for the ESP32 magic byte `0xE9` before being given a
  `.bin` extension.
- **`community.m5stack.com` (NodeBB) search is auth-walled**: `/api/search` →
  401, `/search?term=` → 302. `/api/recent` is open and is the only usable
  window, but a recent-topics window is not a search.
- **`hackster.io` has no working machine path.** `/search?q=` is a JS shell;
  `/search.json` and `/api/v2/projects` return HTML with a JSON-looking URL.
- **`switch-science.com/search/suggest.json` returns HTTP 417.** The plain HTML
  search works and states result counts in words (「…の検索結果0件」), which is
  better evidence than an empty array.
- **`public.api.bsky.app` 403s every UA tried**, which contradicts a ✓ for
  Bluesky in the access table — that ✓ evidently refers to `bsky.app` HTML, not
  the public XRPC API.
- **Byte-length equality is not content equality.** Three Shopify 404s came back
  at exactly 389 759 bytes with three different hashes.
- **GitHub rate limits are per identity, and no UA helps.** Use
  `gh api` / `Authorization: Bearer $(gh auth token)` — 60/h becomes 5 000/h.
  A 403 carrying `X-RateLimit-Remaining: 0` looks exactly like bot-blocking;
  check the header before rotating agents.

## Not attempted, and why

| Target | Reason | Expected yield |
|---|---|---|
| FCC / IC / CE grantee databases | S11 establishes only that *M5Stack* publishes nothing. A grantee search by company name is the obvious next step and was not run | **High.** The device carries a wideband 868–923 MHz radio on a single SKU |
| The 14 Arduino API sub-pages (`battery`, `display`, `nfc`, `lora`, `wakeup`, …) | Enumerated from S07, not fetched | Medium |
| `PaperMono-Lite_PRJ_V0.6.2_20260522.pdf` (S16) | Not fetched | **High** — it is the only way to know what the Lite's board actually omits rather than what the marketing table says |
| zh_CN-only datasheets (S27–S30) | Not fetched | **High** for S27/S28 — the CN editions of the two M5-designed chips could settle the pin-nomenclature question at the silicon level |
| Mouser / DigiKey product APIs | Both require API keys not available in this session | Medium — would convert two "no determination" rows into determinations |
| Taobao (`m5stack.taobao.com`) | Listed distributor; needs CN-region handling | Medium |
| Tom's Hardware | Nothing surfaced via Mojeek, CNX, HN, Reddit or YouTube; their on-site search is JS-driven and was not forced | Low |
| Adafruit *blog* (`blog.adafruit.com`) | The Adafruit **store** returned a clean negative; the blog was not separately queried | Low |
| Hackaday.io projects (distinct from hackaday.com) | Not queried | Low |
| Google / Bing | Mojeek succeeded; further engine rotation was unnecessary | Low |
| `web.archive.org/save` submissions | None of the community/press sources meets the scarcity bar. The vendor PDF assets arguably do — see [dead links](#dead-links-and-recovery-attempts) | Medium, deferred |
| Anything on physical hardware | **No PaperMono exists in this session, and none could be bought — the product has been out of stock since nine minutes after launch** | — |

## Stopping criterion

**Stated plainly: two consecutive broad passes returned only vendor marketing
copy, its re-syndication, and duplicates of items already held.**

The second pass (5.7) was run specifically as an independent check on the first,
using four different query formulations and a `t=year` filter across the same
services. It produced **one** item, which had already been found. Pages 2–5 of
the only working web search engine (7.10) were, after deduplication, entirely
Tux Machines re-syndicating a single LinuxGizmos article that itself restates a
single vendor blog post.

What that yields, as of 2026-09-01 — eleven days after launch:

- **Zero written reviews.** Not one article anywhere puts hands on the hardware.
- **One hands-on video**, published on day 8, self-described as a first look, and
  carrying a vendor referral link.
- **Zero Hackaday coverage** (a machine-readable `[]`), zero reachable Hackster
  coverage, zero Tom's Hardware coverage.
- **Two Reddit results site-wide for `papermono`, both bot mirrors of an HN
  post.** The only genuine Reddit discussion is two threads in the vendor's own
  subreddit.
- **No measured power figure exists anywhere**, vendor included.
- No teardown, no battery-life test, no independent refresh-rate verification, no
  LoRa range test, no NFC interoperability test.
- **Four third-party GitHub projects and one SDK**, two with credible
  hardware-validation evidence. **That is where the real independent signal is.**

This is the expected shape for an eleven-day-old product that has been out of
stock for all but nine minutes of its commercial life: *you cannot review
hardware nobody can buy.* The near-total absence of independent measurement is a
consequence of supply, not of disinterest — a 162-point HN thread and 61 590
video views say the opposite of disinterest.

**The stopping criterion is therefore about saturation, not completeness.** The
searchable surface was exhausted; the *knowable* surface was not. Anyone
re-running this after a restock should expect the community sections to change
substantially and the vendor sections not to.

## Query-count summary

| Category | Distinct queries | useful | negative-confirmed | inaccessible | rejected / duplicate / dead |
|---|---|---|---|---|---|
| Vendor documentation + artifacts | 36 | 26 | 3 | 0 | 3 (+ 4 not attempted) |
| Vendor storefront | 12 | 9 | 0 | 0 | 3 |
| M5Burner | 8 | 7 | 0 | 1 | 0 |
| Vendor source repositories | 9 | 6 | 3 | 0 | 0 |
| Community / social / forum | 19 | 12 | 3 | 3 | 1 |
| Retailers / distributors | 24 | 6 | 9 | 5 | 4 |
| Competitor pricing | 5 | 3 | 0 | 0 | 2 (1 inconclusive, 1 gap) |
| Press / video / code | 27 | 16 | 4 | 4 | 3 |
| **Total** | **140** | **85** | **22** | **13** | **16** |

The market/community subset of this table (94 distinct queries across 30+
services) is the figure quoted in [`README.md`](README.md); the totals above add
the documentation, artifact, firmware and repository passes.

## Related

- [`sources.md`](sources.md) — what was kept, with stable IDs
- [`commands.md`](commands.md) — what was run, with execution status
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — what the sources disagree about
- [`../../../ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md) — the durable home for the retrieval findings above
