# Market and pricing — t4-s3

## Dated price observations — 2026-09-11 (certification/market pass)

Added **2026-09-11**, append-only. Earlier sections above are another session's work and are left exactly as written.

> ⚠ **Date note.** The session brief for this pass said 2026-09-07. The host clock, the `date:` response headers from two independent servers, and the `updated_at` field on every live product below all say **2026-09-11**. The later date is used because it is what actually happened. See `scratch/market-and-certification/README.md`.

### Method and source

Single request to the vendor's Shopify catalogue endpoint, `https://www.lilygo.cc/products.json?limit=250&page=<n>`, retrieved **2026-09-11**. This is the **strongest available evidence**: it returns `published_at`, `updated_at`, every variant, SKU, price and stock flag in one response, with no rendering and no scraping heuristics.

- **MSRP vs street price:** these are the **vendor's own list prices** — MSRP, not street. No discount, coupon or quantity break is reflected.
- **Currency:** USD as served by the store. No conversion was applied, so no conversion date applies. ⚠ LilyGO's USD prices carry odd cents (e.g. 8.04, 98.79), which is consistent with **machine conversion from CNY**; the underlying CNY price and its conversion date are **not exposed by the endpoint** and are therefore unknown.
- **Ships from:** Shenzhen, CN.
- **Stock evidence:** the per-variant `available` boolean, quoted verbatim below.
- **Condition:** new. **Genuine** — this is the manufacturer's own storefront.
- **Tax/duty:** not shown by the endpoint; not established.

### Observations

| Product (store title) | Published | Variant | SKU | Price | In stock |
|---|---|---|---|---|---|
| T4 S3 | 2023-11-03 | China [For Worldwide] / With Shell Soldered Female Pin [H711] | `H711` | **USD 58.99** | ✅ yes |
| T4 S3 | 2023-11-03 | China [For Worldwide] / With Shell Soldered Pin [H724] | `H724` | **USD 60.23** | ✅ yes |
| T4 S3 | 2023-11-03 | China [For Worldwide] / Basic [H678] | `H678` | **USD 56.89** | ✅ yes |
| T4 S3 | 2023-11-03 | China [For Worldwide] / Only Sheild [H731] | `H731` | **USD 1.10** | ✅ yes |
| T4 S3 | 2023-11-03 | Germany [ For Europe only] / With Shell Soldered Female Pin [H711] | `H711DE` | **USD 63.49** | ❌ no |
| T4 S3 | 2023-11-03 | United States [For US only] / With Shell Soldered Female Pin [H711] | `H711US` | **USD 63.49** | ✅ yes |

Citation form required by [`guides/markets/vendor-comparison.md`](../../../guides/markets/vendor-comparison.md) § *A note on prices*, for the first row:

> *USD 58.99, 1 unit, retrieved 2026-09-11, `https://www.lilygo.cc/products/t4-s3`, ships from Shenzhen, CN*

### Normalisation and caveats

Basic USD 56.89 → shell + soldered pin USD 60.23. `H731` at USD 1.10 is **a shield only**, not a board — excluding it is why the floor here is 56.89 and not 1.10. ⚠ A naive 'from' price would read USD 1.10.

### Coverage not achieved, and why

The task asked for AliExpress, Amazon/eBay, Taobao/JD and used/refurbished sampling. **None was obtained.** Measured 2026-09-11 from this host:

| Channel | Result |
|---|---|
| AliExpress search | HTTP 200 but **bot-wall page** |
| `m5stack.aliexpress.com` | HTTP 200 but **bot-wall page** |
| eBay search | **HTTP 403** |
| Amazon search | HTTP 200, **zero prices in the HTML** (JS shell) |
| Taobao search | HTTP 200, **34 KB SPA shell**, no listings |
| JD search | HTTP 200, **2.7 KB shell**, no listings |
| Used / refurbished | **not attempted** — every marketplace above was already blocked |

**No marketplace, clone or used-market price is reported, because none was observed.** A 200 response containing no prices is a failure, not a datum. This leaves the sweep's gap *partially* open: official-store pricing is now dated and complete; **street, clone and used pricing remain unsampled.**

### Sample size

Inspected catalogue: **664 products** (`shop.m5stack.com`), **214** (`www.lilygo.cc`), **25** (`xteink.com`), enumerated in full on 2026-09-11. Statements of the form "no such product exists" above are against that complete enumeration, not against a search-result page.

