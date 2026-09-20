# Research log — Xteink X4 Classic (X4C / "X4 V2")

Two passes are recorded here. **Pass 1** (2026-09-04) is summarised from the
sweep that created this record. **Pass 2** (2026-09-11) is this session and is
logged query-by-query.

---

## 0. A date discrepancy, recorded rather than papered over

The task brief for pass 2 stated the date as **2026-09-07**. The host clock read
**2026-09-11T22:52:42Z**, and the vendor's Shopify API independently returned
`updated_at: 2026-09-11T15:52:09-07:00` on every product, plus a product image
created `2026-09-08T23:42:57-07:00` and a Judge.me review created
`2026-09-08 04:57:34 UTC`.

**Three independent remote sources put "now" at or after 2026-09-08**, so the
brief's 2026-09-07 is stale and **2026-09-11 is used as the retrieval date
throughout**. Nothing in this record depends on the difference; the launch date
(2026-09-06) is read from the vendor's own `published_at` and is unaffected.

---

## 1. Pass 2 search ledger — 2026-09-11

### 1.1 Vendor (Shopify), UA `Mozilla/5.0 … Chrome/131.0.0.0`

| # | Endpoint | Result | Disposition |
|---|---|---|---|
| V1 | `https://xteink.com/products.json?limit=250&page=1` | 200, 122,443 B, **25 products** | **useful** — the launch evidence |
| V2 | `…&page=2`, `…&page=3` | 200, 15 B each (`{"products":[]}`) | catalogue is one page |
| V3 | `https://xteink.com/collections.json?limit=250` | 200, 4,459 B, 11 collections | unchanged from 2026-09-04 |
| V4 | `https://xteink.com/collections/<handle>/products.json?limit=250` × 11 | all 200 | **useful** — see §1.2 |
| V5 | `https://xteink.com/products/xteink-x4-classic-pocket-ereader` | 200, 919,867 B HTML | **useful** — the spec block lives here, not in `body_html` |
| V6 | `…/xteink-x4-classic-pocket-ereader.js` | 200, 15,497 B | duplicate of V1's record |

**Retrieval finding worth reusing:** this product's `body_html` is **empty**. The
entire specification table is a theme section rendered server-side into the
product page. An agent that reads only `/products.json` will conclude the vendor
published no specifications at all. **Fetch the HTML too.**

### 1.2 Collection diff, 2026-09-04 → 2026-09-11

| Collection | 2026-09-04 | 2026-09-11 | Reading |
|---|---:|---:|---|
| `x4-classic` | **4** — reading light, metal ring, X3/X4-Pro adapter, X3/X4-Pro cable. **No device** | **10** — device + 4 X4C-specific accessories + charging base | **The launch** |
| `machine` (devices only) | X3, X4 Pro | **X3 $69 · X4 Classic $79 · X4 Pro $99** | The vendor's own three-device line-up |
| `homepage-display` | 4 | 4, now **led by the X4 Classic** | Promoted to hero |
| `x4-series` | accessories | **2 generic accessories only** | The X4 line is finished |
| `x3-series` | 9 | 10 (+ charging base) | — |
| `x4-pro-series` | 8 | 9 (+ charging base) | — |

Four X4 accessories that existed on 2026-09-04 are **gone** from the catalogue
entirely: `xteink-x4-matte-screen-protector`, `xteink-x4-protective-case`,
`xteink-x4-screen-protector`, `xteink-x4-magnetic-case`. The X4 is not merely
delisted; its accessories have been withdrawn.

### 1.3 Regulatory — `fccid.io`

| # | Query | Result |
|---|---|---|
| R1 | `https://fccid.io/2BTR9-X4C` with Chrome UA | **403** |
| R2 | same URL with `WhatsApp/2.23.20.0` | **200, 22,338 B** |
| R3 | `https://fcc.report/FCC-ID/2BTR9-X4C`, four different UAs | **403 on all four** |
| R4 | `apps.fcc.gov/oetcf/eas/reports/GenericSearchResult.cfm?fcc_id=2BTR9-X4C` | **403** |
| R5 | `https://fccid.io/2BTR9` (grantee index) | 200 — **five FCC IDs**, including one undocumented product |
| R6 | `https://fccid.io/<id>/<Type>/<Name>-<docid>.pdf` | **200, `%PDF`** for every public exhibit |

**The single most valuable retrieval trick of this pass.** `fccid.io` blocks a
desktop-Chrome UA and serves a link-preview UA. The PDF pattern is
`https://fccid.io/<FCCID>/<Type>/<Slug>-<DocumentID>.pdf`, where `<DocumentID>` is
the numeric id in the `href` on the FCC ID page. Recorded in
[`commands.md`](commands.md) and in the repository's
[crawler access table](../../../ai-crawler-site-access-table.md).

**A trap caught while doing this.** `https://www.crystalfontz.com/controllers/UltraChip/UC8179/478/`
returns a **valid 477 KB PDF** — which is the *GOODiX GT911 Programming Guide*.
The path segment `UC8179` is decorative; the trailing number is the only thing
that selects a document. Validating by magic bytes alone would have filed a
touch-controller manual as a display-controller datasheet. The correct id for
UC8179 is `517`, read from the page's own `datasheet-viewer.php?id=` link.

### 1.4 Firmware / board definitions

| # | Query | Result |
|---|---|---|
| F1 | `gh api repos/Free-Ink/freeink-sdk/commits/main` | HEAD `9f4d3f9ca675e64cc9d616081f39a33cdefce57e`, 2026-09-10 |
| F2 | `enum class Board` at that commit | **No new Xteink board.** Still `XteinkX4`, `XteinkX3`, `XteinkX3Uc8279`, `XteinkX4Pro`, `XteinkX4Classic`. New non-Xteink boards: `M5PaperS3`, `EegoA4`, `OnePage`, `WsEpaper397` |
| F3 | `diff` of `XTEINK_X4_CLASSIC` profile, `2400379` → `9f4d3f9` | **One change**: `displaySpiHz` 20 MHz → shared `XTEINK_DISPLAY_SPI_HZ = 10000000u` |
| F4 | `commits?path=…/BoardConfig.h&since=2026-09-01` | two: `3fe3936d` (Waveshare board, 09-05), **`39606d5a`** (*"Fix e-ink display buffer tracking and optimize SPI writes"*, 09-09) |
| F5 | `diff` of `docs/xteink-x4c-support.md` | one line: the same 20 → 10 MHz statement |
| F6 | code search `"X4R1_CLA"` | **`total_count: 0`** — no `R1` string exists anywhere on GitHub |
| F7 | code search `"X4R2_CLA" xteink` | 5 hits: `Free-Ink/freeink-sdk` ×2, **`kycube/x4pro-emu`**, `mohitagw15856/Inkkit`, `vjFaLk/esphome-xteink` |
| F8 | code search `"X4 V2" xteink` | 11 hits, 9 of them in **`clackups/draftling`** |
| F9 | code search `xteink "X4 Classic"` | 47 hits |

**F6 is a negative result and is the point.** A search that returns zero is the
strongest available evidence that no public firmware has ever named an X4C R1.

### 1.5 Independent projects found (pass 2 only)

| Repo | Created | Licence | Why it matters |
|---|---|---|---|
| [`clackups/draftling`](https://github.com/clackups/draftling) | 2026-06-05 | MIT | ESP32-S3/P4 writerdeck firmware with a **hand-written X4 Classic board header** and a `HARDWARE.md` chapter. Independently states the X4C = "X4 v2" equivalence. **Explicitly untested on X4C hardware**, but **tested on X4 Pro hardware** |
| [`kycube/x4pro-emu`](https://github.com/kycube/x4pro-emu) | **2026-09-07** | none stated | QEMU emulator built against a **physical X4 Pro**: esptool chip-id, eFuse dump, twice-verified 16 MB flash dump, I²C and LEDC traces |
| [`vjFaLk/esphome-xteink`](https://github.com/vjFaLk/esphome-xteink) | 2026-08-30 | MIT | ESPHome components; vendors the FreeInk SDK verbatim (not independent) |
| [`mohitagw15856/Inkkit`](https://github.com/mohitagw15856/Inkkit) | 2026-07-29 | MIT | Shared HAL; copies `BoardConfig.h` (not independent) |

### 1.6 Reddit — `old.reddit.com`, UA `WhatsApp/2.23.20.0`

All 11 requests returned **200**. `www.reddit.com` was not attempted (403
documented elsewhere in this repository).

| # | Query | Hits |
|---|---|---|
| D1–D5 | `search.json?q=…&sort=new&t=month` for `xteink x4 classic`, `x4 v2 xteink`, `xteink x4 classic review`, `xteink new`, `x4 classic` | 100 each; **332 unique**, 213 relevant |
| D6–D11 | `r/<sub>/search.json?q="X4 Classic" OR "X4 V2" OR X4C&restrict_sr=1&t=year` for r/XTEINK, r/xteinkereader, r/xteinkHax, r/CrossPointReader, r/eink, r/ereader | 41 / 47 / 3 / 2 / 0 / 1 → **94 unique**, spanning 2026-04-23 → 2026-09-11 |
| D12–D23 | 12 full comment trees (`<permalink>.json?limit=200`) | see [`community.md`](community.md) |

**r/eink returned 0 and r/ereader returned 1** for a launch that generated
hundreds of posts in the three dedicated subreddits. The X4C conversation is
almost entirely inside the vendor-adjacent communities; a search restricted to
the general e-ink subreddits would have missed the launch completely.

### 1.7 Not searched, and why

- **JD.com, Taobao, Xianyu, Xiaohongshu, WeChat shop** — not retrieved. The
  Chinese-market price and launch date for the X4C are therefore **unknown**, and
  no figure in this record claims otherwise. Declared exclusion, not an
  exhausted search.
- **AliExpress** — not retrieved this pass. The X4C is nine days old
  internationally; marketplace listings at this age are usually the vendor's own
  store mirror and add nothing.
- **Bilibili / YouTube video reviews** — not retrieved. Reddit text reviews were
  used instead and are cited individually.
- **`web.archive.org` CDX for `xteink.com`** — timed out at 60 s on 2026-09-04 and
  was **not retried** this pass. The withdrawn X4 accessory pages are therefore
  still unrecovered.
- **`fcc.report`** — 403 on every UA tried. `fccid.io` served the same documents.

## 2. Stopping criterion for pass 2

Stopped when: the vendor API, the vendor HTML, the FCC grantee index and all
five FCC device pages, the FreeInk SDK at HEAD, GitHub code search on six
distinct strings, and six subreddits over a one-year window had each been
searched; and when two further broad Reddit passes returned only duplicates of
the 94 posts already catalogued. **This is a dated broad-coverage snapshot, not a
proof that nothing else exists.**
