# Market and pricing — t-display-s3-amoled

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
| T-Display S3 AMOLED | 2023-04-14 | China [For Worldwide] / Touch With Black Shell [H717] | `H717` | **USD 33.98** | ✅ yes |
| T-Display S3 AMOLED | 2023-04-14 | China [For Worldwide] / V2.0 Soldered Pin [H712] | `H712` | **USD 26.94** | ✅ yes |
| T-Display S3 AMOLED | 2023-04-14 | China [For Worldwide] / V2.0 Non-Soldered Pin [H713] | `H713` | **USD 26.44** | ✅ yes |
| T-Display S3 AMOLED | 2023-04-14 | China [For Worldwide] / V1.0 Soldered Pin [H634] | `H634` | **USD 26.94** | ✅ yes |
| T-Display S3 AMOLED | 2023-04-14 | China [For Worldwide] / V1.0 Non-Soldered Pin [H619] | `H619` | **USD 26.44** | ✅ yes |
| T-Display S3 AMOLED | 2023-04-14 | China [For Worldwide] / Touch Soldered pin [H705] | `H705` | **USD 30.44** | ✅ yes |
| T-Display S3 AMOLED | 2023-04-14 | China [For Worldwide] / Touch Non-Soldered Pin [H681] | `H681` | **USD 30.03** | ✅ yes |
| T-Display S3 AMOLED | 2023-04-14 | China [For Worldwide] / Only Camera Shield [H679] | `H679` | **USD 6.33** | ✅ yes |
| T-Display S3 AMOLED | 2023-04-14 | Canada [For CA only] / Touch With Black Shell [H717] | `H717CA` | **USD 32.00** | ✅ yes |
| T-Display S3 AMOLED | 2023-04-14 | United States [For US only] / V2.0 Soldered Pin [H712] | `H712-US` | **USD 30.94** | ❌ no |
| T-Display S3 AMOLED | 2023-04-14 | United States [For US only] / V2.0 Non-Soldered Pin [H713] | `H713US` | **USD 30.94** | ❌ no |
| T-Display S3 AMOLED | 2023-04-14 | Germany [ For Europe only] / Touch With Black Shell [H717] | `DEH717` | **USD 38.48** | ✅ yes |
| T-Display S3 AMOLED | 2023-04-14 | Germany [ For Europe only] / Touch Soldered pin [H705] | `DEH705` | **USD 34.94** | ✅ yes |
| T-Display S3 AMOLED | 2023-04-14 | United States [For US only] / Touch With Black Shell [H717] | `USH717` | **USD 38.48** | ✅ yes |
| T-Display S3 AMOLED | 2023-04-14 | United States [For US only] / Touch Non-Soldered Pin [H681] | `USH681` | **USD 34.63** | ✅ yes |
| T-Display S3 AMOLED | 2023-04-14 | Germany [ For Europe only] / V2.0 Soldered Pin [H712] | `H712-DE` | **USD 33.98** | ❌ no |

Citation form required by [`guides/markets/vendor-comparison.md`](../../../guides/markets/vendor-comparison.md) § *A note on prices*, for the first row:

> *USD 33.98, 1 unit, retrieved 2026-09-11, `https://www.lilygo.cc/products/t-display-s3-amoled`, ships from Shenzhen, CN*

### Normalisation and caveats

⚠ **16 variants.** V1.0 and V2.0 are the **same price** (USD 26.44/26.94), so the revision carries no premium. Touch adds ~USD 3.6. Camera shield alone is USD 6.33. US/DE regional SKUs run USD 4–8 higher than 'China [For Worldwide]'.

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

