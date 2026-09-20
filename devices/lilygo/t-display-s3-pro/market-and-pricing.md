# Market and pricing — t-display-s3-pro

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
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / With GC0308 Camera / White | `K239` | **USD 46.54** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / With GC0308 Camera / White with Orange | `K240` | **USD 46.54** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / With GC0308 Camera / Black | `K241` | **USD 46.54** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / With GC0308 Camera / Orange | `K242` | **USD 46.54** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / With OV5640 Camera / White | `K232` | **USD 56.99** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / With OV5640 Camera / White with Orange | `K235` | **USD 56.99** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / With OV5640 Camera / Black | `K236` | **USD 56.99** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / With OV5640 Camera / Orange | `K238` | **USD 56.99** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / Without Camera / White | `K231` | **USD 37.99** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / Without Camera / White with Orange | `K233` | **USD 37.99** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / Without Camera / Black | `K234` | **USD 37.99** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / Without Camera / Orange | `K237` | **USD 37.99** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / Only Black Lens Cover / Only Black Lens Cover | `H688` | **USD 6.02** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / Only MVSR Board / Only MVSR Board | `H751` | **USD 10.20** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / Black Mainboard With MVSR Board / Black Mainboard With MVSR Board | `K255` | **USD 42.33** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | China [For Worldwide] / White Mainboard With MVSR Board / White Mainboard With MVSR Board | `K255-01` | **USD 42.33** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | Germany [ For Europe only] / With GC0308 Camera / White | `K239DE` | **USD 48.99** | ✅ yes |
| T-Display S3 Pro | 2023-09-07 | Germany [ For Europe only] / Without Camera / White | `K231DE` | **USD 41.72** | ❌ no |
| T-Display S3 Pro LR1121 | 2025-07-16 | [K252-01] | `K252-01` | **USD 65.29** | ✅ yes |
| T-Display S3 Pro External | 2025-11-28 | T-Display S3 Pro External [H742] | `H742` | **USD 34.05** | ✅ yes |

Citation form required by [`guides/markets/vendor-comparison.md`](../../../guides/markets/vendor-comparison.md) § *A note on prices*, for the first row:

> *USD 46.54, 1 unit, retrieved 2026-09-11, `https://www.lilygo.cc/products/t-display-s3-pro`, ships from Shenzhen, CN*

### Normalisation and caveats

⚠ **Camera tiering dominates the price**: no camera USD 37.99 → GC0308 USD 46.54 → OV5640 USD 56.99. Colour does not affect price. The LR1121 LoRa variant is a **different product** at USD 65.29.

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

