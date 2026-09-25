# Xteink X4 Pro — research log

Session **2026-09-04**. Searcher: automated agent, no hardware available.
This log covers the whole Xteink family; device-specific results are marked.

## Declared scope and cutoff

- **Cutoff:** 2026-09-04.
- **Languages:** English throughout; Chinese for brand-name and repo searches.
- **Not searched:** FCC/CE/SRRC databases, JD.com, Taobao, AliExpress, Bilibili,
  Zhihu, 52pojie, Baidu Tieba, YouTube (beyond links surfaced in Reddit posts).
  These are **declared exclusions**, not "nothing found".

## Source classes searched

| Class | Searched | Result |
|---|---|---|
| Manufacturer product pages | ✅ `xteink.com` (Shopify JSON APIs) | **Useful** — the only primary source that exists |
| Manufacturer support / wiki / manual | ✅ | **None exists.** No datasheet, no manual, no dev docs, no schematic |
| Component-manufacturer datasheets | ⚪ deferred to component records | — |
| Standards / certification bodies | ❌ **not searched** | No FCC ID known to query |
| Framework / SDK documentation | ✅ FreeInk SDK, CrossPoint | **Highest-value source in the subject** |
| Authorized distributors | ✅ none exist — vendor-direct only | — |
| Community repositories | ✅ GitHub, 5 queries × 2 pages | ~200 relevant repos |
| Forums | ✅ Reddit, 23 queries | 1,798 unique posts |
| Teardowns | ✅ | 2 found — **both X3**, none for X4 Pro |
| Archives | ⚠️ attempted, timed out | Wayback CDX |

## Query ledger

### Vendor store — `xteink.com`

| Query | Depth | Result |
|---|---|---|
| `/products.json?limit=250&page=1..3` | 3 pages | 23 products; p2/p3 empty → complete |
| `/collections.json?limit=250` | 1 | 11 collections |
| `/collections/{machine,x4-classic,x4-series,x3-series,x4-pro-series,homepage-display,x3-edm,x4-edm,x4-proedm}/products.json` | 9 | **Established the X4 is delisted and the X4 Classic has no listed device** |
| `https://xteink.net/`, `https://xteink.cn/` | — | **Dead** (HTTP 000). `.cn` apex unreachable *but* `bofi.xteink.cn` is embedded in the X4 firmware |

### Reddit — `old.reddit.com`, UA `WhatsApp/2.23.20.0`

All 23 requests returned **200**.

| Query | Result |
|---|---|
| `search.json?q=xteink` and 12 further term queries | see below |
| `r/xteinkereader/{new,top}`, `r/XTEINK/{new,top}`, `r/xteinkHax/{new,top}`, `r/CrossPointReader/{new,top}` | 100 each |
| Terms used | `xteink`, `xteink x4 pro`, `xteink x3`, `xteink teardown`, `crosspoint reader`, `xteink x4c`, `xteink classic`, `xteink teardown chip`, `xteink esp32`, `xteink x5`, `xteink x2`, `xteink mini`, `xteink brand`, `xteink aliexpress`, `xteink unlock`, `xteink firmware flash`, `crossink`, `crossmux`, `xteink s4 android`, `xteink battery mah`, `xteink x4 pro chip`, `xteink brick` |

**Yield: 1,798 unique posts** across `_merged-posts.json`.

**Discovery worth recording:** the community is spread over **three** subreddits
with confusingly similar names — r/XTEINK (416 posts), r/xteinkereader (406),
r/xteinkHax (180) — plus r/CrossPointReader. Searching only one misses most of it.

**Negative results, deliberately preserved:**
- `x5` → 8 hits, **all speculation**; one self-corrected ("EDIT: It's X4 not X5")
- `x4 mini` → 6 hits, **all colloquial**, one video body names "the XTEINK X4"
- `x2` → 3 hits, **all false positives** ("quantity ×2")
- `xteink teardown` → **no X4 Pro teardown exists**

### GitHub — authenticated API

| Query | Pages | Result |
|---|---|---|
| `repositories?q=xteink` | 2 | 378 total, 100/page |
| `repositories?q=crosspoint+reader` | 2 | 105 total |
| `repositories?q=freeink` | 2 | 17 total |
| `repositories?q=xteink+x4` | 2 | 198 total |
| `repositories?q=crossink` | 2 | — |
| `code?q=FREEINK_DEVICE_X4PRO` / `XTEINK_X4_PRO` / `xteink_x4_classic` | 1 each | — |
| Repo metadata + recursive trees | 5 repos | `XTEINK-OEM-BIN-`, `Xteink-X3`, `xteink-unlocker`, `xteink-x4`, `eink-quick-flasher` |

### Dead / failed / inaccessible

| Target | Outcome |
|---|---|
| `web.archive.org/cdx/search/cdx?url=xteink.com*` | **Timed out at 60 s, 0 bytes.** Not retried. The delisted X4 product page remains unrecovered |
| `https://xteink.net/`, `https://xteink.cn/` | Connection failure |
| `imgur.com/a/<id>` HTML | Returns 2 of 13 images — JS shell. **Recovered** via `imgur.com/ajaxalbums/getimages/<id>/hit.json` |
| X4 Pro stock firmware image | **Does not exist publicly.** Searched GitHub repo names and the flasher projects; only X3/X4 images are published |
| `xteink_app_update_x4pro_7.4.4_…xota` | Named in SDK docs; **no download URL found anywhere** |

## Stopping criterion

Reached the point where two consecutive broad passes returned only duplicates for
the X4 Pro specifically: the FreeInk SDK is the sole source of board-level fact,
and no independent corroboration (teardown, schematic, regulatory filing) exists
to find. Remaining sources require **hardware**, **a teardown**, or **regulatory
database access** — the first two unavailable, the third not attempted.

This is a **reproducible broad-coverage snapshot dated 2026-09-04**, not proof
that no other resource exists.

---

## ⚠ Correction, 2026-09-11 — Xteink FCC grants exist

The line(s) below, still present above and deliberately unedited, are **refuted**:

> *line 10:* - **Not searched:** FCC/CE/SRRC databases, JD.com, Taobao, AliExpress, Bilibili,
>
> *line 21:* | Standards / certification bodies | ❌ **not searched** | No FCC ID known to query |
>

**Xteink is an FCC grantee.** Applicant **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**, grantee code **`2BTR9`**, registered 2025-12-21, holding **five granted Original Equipment authorisations**:

| FCC ID | Granted | Device |
|---|---|---|
| `2BTR9-X4L` | 2026-08-13 | XTEINK X4 Light |
| `2BTR9-X4C` | 2026-07-20 | XTEINK X4 Classic |
| `2BTR9-X4PRO` | 2026-06-16 | XTEINK X4 Pro |
| `2BTR9-XTEINKX4` | 2026-01-05 | XTEINK X4 |
| `2BTR9-XTEINKX3` | 2025-12-26 | XTEINK X3 |

The original finding confused **"no mark visible in a product photograph"** with **"no grant exists"**. Those are different claims, and only the first was tested.

- ✅ **Survives:** no FCC ID was legible on the exteriors photographed. Not re-tested.
- ❌ **Refuted:** any reading that these devices are uncertified or unauthorised for the US.

47 CFR §2.935 permits an **e-label** in software instead of a printed mark, which is ordinary for a device with a screen. **That is a likely explanation and it was not verified.**

The absence was never re-searched in 2026-09-04 because **no FCC ID was known and the grantee code had not been found**. Enumerating the grantee — not searching the product name — is what resolved it. Method: [`guides/research/finding-certification-records.md`](../../../guides/research/finding-certification-records.md).

Full record, with controls: [`certification-and-compliance.md`](certification-and-compliance.md).

Listed in [`research/passes/index-merge/corrections-requiring-review.md`](../../../research/passes/index-merge/corrections-requiring-review.md).
