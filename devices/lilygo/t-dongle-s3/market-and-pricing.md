# Market and pricing — t-dongle-s3

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
| T-Dongle S3 | 2022-10-20 | T-Dongle S3 / China [For Worldwide] / With LCD [K193] | `K193` | **USD 11.99** | ✅ yes |
| T-Dongle S3 | 2022-10-20 | T-Dongle S3 / China [For Worldwide] / Without LCD [K194/ K194-B] | `K194` | **USD 10.99** | ✅ yes |
| T-Dongle S3 | 2022-10-20 | T-Dongle S3 / China [For Worldwide] / Without LCD External Antenna [K194-01] | `K194-01` | **USD 10.99** | ✅ yes |
| T-Dongle S3 | 2022-10-20 | T-Dongle S3 / Germany [ For Europe only] / With LCD [K193] | `K193DE` | **USD 16.49** | ✅ yes |
| T-Dongle S3 | 2022-10-20 | T-Dongle S3 / United States [For US only] / With LCD [K193] | `USK193` | **USD 16.49** | ❌ no |
| T-Dongle S3 | 2022-10-20 | T-Dongle S3 Dual / China [For Worldwide] / Without LCD [K194/ K194-B] | `K194-B` | **USD 14.96** | ✅ yes |
| T-Dongle C5 | 2026-01-28 | China [For Worldwide] / With Screen [K193-A] | `K193-A` | **USD 13.98** | ✅ yes |
| T-Dongle C5 | 2026-01-28 | China [For Worldwide] / Without Screen [K194-A] | `K194-A` | **USD 13.02** | ✅ yes |
| T-Dongle C5 | 2026-01-28 | Germany [ For Europe only] / With Screen [K193-A] | `DEK193-A` | **USD 18.48** | ✅ yes |
| T-Dongle C5 | 2026-01-28 | United States [For US only] / With Screen [K193-A] | `USK193-A` | **USD 18.48** | ❌ no |

Citation form required by [`guides/markets/vendor-comparison.md`](../../../guides/markets/vendor-comparison.md) § *A note on prices*, for the first row:

> *USD 11.99, 1 unit, retrieved 2026-09-11, `https://www.lilygo.cc/products/t-dongle-s3`, ships from Shenzhen, CN*

### Normalisation and caveats

`K193` with LCD USD 11.99, `K194` without USD 10.99. **T-Dongle C5 is a different product** (ESP32-C5), listed for contrast only.

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

