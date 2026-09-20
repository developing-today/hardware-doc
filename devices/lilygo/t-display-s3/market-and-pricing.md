# T-Display-S3 — pricing and availability

> All observations **2026-09-07**, from LilyGO's own Shopify product feed
> (`https://lilygo.cc/collections/all/products.json`), whose `updated_at` was the same date.
> **Prices exclude shipping, VAT and duty.** Currency USD as listed by the store.

## Launch

| | |
|---|---|
| Store `published_at` | **2022-07-15** |
| Repo created | 2022-06-13 |
| Launch price | **not established.** The feed carries current prices only; no archived listing was retrieved |

## Current — LilyGO official store, 2026-09-07

| SKU | Configuration | USD | Stock |
|---|---|---|---|
| `H569` | bare, **non-soldered** header pins | **9.04** | in stock |
| `H577` | bare, soldered pins | 9.54 | in stock |
| `H587` | **Touch**, non-soldered | 12.61 | in stock |
| `H589` | **Touch**, soldered | 13.02 | in stock |
| `K204` / `K206` | with black / grey shell | 13.22 | in stock |
| `K204-01` / `K206-01` | shell **+ 700 mAh battery** | 20.60 | **out of stock** |
| `H656` | MIDI shield **only** (no board) | 15.47 | in stock |
| `USH577` | soldered, **US warehouse** | 14.04 | out of stock |
| `DEH577` | soldered, **DE warehouse** | 14.04 | out of stock |
| `K204US` / `K204-DE` | black shell, US / DE warehouse | 17.72 | out of stock |

A **second listing** exists under handle `t-display-s3-copy`, published 2026-07-27, offering
`H569` at **USD 9.03** — one cent lower, same SKU. Almost certainly a duplicated product page
rather than a different item; recorded because a price-comparison script will report it as a
distinct product.

### The regional-warehouse premium

`H577` costs **9.54** from China and **14.04** from the US or German warehouse — a **47 %**
markup for local stock, and **every** regional SKU was out of stock on the observation date.
Local warehouses are not a reliable purchase path for this board.

### Accessories

| Item | USD | Note |
|---|---|---|
| T-Display TF Shield `H609` / `H610` | 2.51 / 2.38 | microSD; the only way to get a card slot |
| T-Display-S3 Shell `L929` / `L930` | 5.02 | shell alone |
| T-Display keyboard | 6.88 – 30.98 | separate product |

## Family price context, same date

| Board | From (USD) |
|---|---|
| **T-Display-S3** | **9.04** |
| T-Display (ESP32 predecessor) | 8.04 |
| T-Dongle S3 | 10.99 |
| T-QT Pro | 9.05 |
| T-Display S3 AMOLED (DS) 1.64″ | 22.99 |
| T-Display S3 AMOLED 1.91″ | 26.44 |
| T-Display S3 Long | 29.35 |
| T-Display S3 AMOLED Plus | 32.68 |
| T-Display AMOLED Lite 1.47″ | 35.66 |
| T-Display S3 Pro | 37.99 (no camera) – 56.99 (OV5640) |
| T4-S3 2.41″ AMOLED | 56.89 |

**Adding an AMOLED panel roughly triples the price**, and adding touch to the base board costs
**+USD 3.57** (`H569` → `H587`) — which is the cheapest capacitive touch on any ESP32-S3 board
documented in this repository.

## Marketplace and clones

**Not sampled in this pass.** AliExpress, Amazon, Banggood and the used market were not
surveyed, so no dated marketplace observation is offered — a range quoted without dates,
sellers and shipping is worse than none. Recorded as gap
[K8](gaps-and-conflicts.md).

One dated third-party data point survives in the searched set, and is offered only as such:
a coupon post on r/couponsjet, **2024-11-30**, advertising the **AMOLED** board at
**USD 32.99** on Banggood. Evidence class: *promotional post, unverified, different board.*

The genuine-vs-clone question, with a worked example, is in
[`comparisons-and-recommendations.md`](comparisons-and-recommendations.md#the-clone-question).
Method: [`guides/markets/clones-and-variants.md`](../../../guides/markets/clones-and-variants.md).

## Buying advice, dated 2026-09-07

- **If you do not need touch, do not buy touch.** The non-touch board is USD 3.57 cheaper and
  avoids the CST816S/CST328 driver-flag problem entirely.
- **Buy non-soldered** (`H569`) unless you want the headers exactly as LilyGO fits them; 50 ¢
  is not worth losing the option.
- **Do not buy the regional-warehouse SKUs** at a 47 % premium; they were out of stock anyway.
- **The shell-plus-battery bundle is the only sanctioned battery**, and it was out of stock.
  Any cell you source yourself must be **protected** (no on-board protection) and should be
  ≥ 600 mAh to keep the ~580 mA charge current below 1 C.
- **If you want AMOLED, price it against the alternatives**: at USD 26–33 the 1.91″ AMOLED
  boards compete with entirely different classes of board. See
  [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md).

---

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
| T-Display S3 | 2022-07-15 | China [For Worldwide] / Non-Soldered Pin [H569] | `H569` | **USD 9.04** | ✅ yes |
| T-Display S3 | 2022-07-15 | China [For Worldwide] / Touch Non-Soldered Pin [H587] | `H587` | **USD 12.61** | ✅ yes |
| T-Display S3 | 2022-07-15 | China [For Worldwide] / Touch Soldered [H589] | `H589` | **USD 13.02** | ✅ yes |
| T-Display S3 | 2022-07-15 | China [For Worldwide] / Soldered Pin [H577] | `H577` | **USD 9.54** | ✅ yes |
| T-Display S3 | 2022-07-15 | China [For Worldwide] / With Grey Shell [K206] | `K206` | **USD 13.22** | ✅ yes |
| T-Display S3 | 2022-07-15 | China [For Worldwide] / With Black Shell [K204] | `K204` | **USD 13.22** | ✅ yes |
| T-Display S3 | 2022-07-15 | China [For Worldwide] / With Black Shell and built-in 700 mAh battery [K204-01] | `K204-01` | **USD 20.60** | ❌ no |
| T-Display S3 | 2022-07-15 | China [For Worldwide] / With Grey Shell and built-in 700 mAh battery [K206-01] | `K206-01` | **USD 20.60** | ❌ no |
| T-Display S3 | 2022-07-15 | China [For Worldwide] / Only MIDI Board [H656] | `H656` | **USD 15.47** | ✅ yes |
| T-Display S3 | 2022-07-15 | Germany [ For Europe only] / With Black Shell [K204] | `K204-DE` | **USD 17.72** | ❌ no |
| T-Display S3 | 2022-07-15 | United States [For US only] / Soldered Pin [H577] | `USH577` | **USD 14.04** | ❌ no |
| T-Display S3 | 2022-07-15 | United States [For US only] / With Black Shell [K204] | `K204US` | **USD 17.72** | ❌ no |
| T-Display S3 | 2022-07-15 | Germany [ For Europe only] / Soldered Pin [H577] | `DEH577` | **USD 14.04** | ❌ no |
| T-Display S3 | 2026-07-27 | China [For Worldwide] / Non-Soldered Pin [H569] | `H569` | **USD 9.03** | ✅ yes |

Citation form required by [`guides/markets/vendor-comparison.md`](../../../guides/markets/vendor-comparison.md) § *A note on prices*, for the first row:

> *USD 9.04, 1 unit, retrieved 2026-09-11, `https://www.lilygo.cc/products/t-display-s3`, ships from Shenzhen, CN*

### Normalisation and caveats

⚠ **13 variants under one handle.** Bare non-soldered board USD 9.04 → shell + 700 mAh battery USD 20.60. **Do not quote a single price.** Note a second handle `t-display-s3-copy` (vendor field literally `1`, published 2026-07-27) duplicates the base SKU `H569` at USD 9.03 — a store artefact, not a product. **Region matters:** US/DE variants of the same SKU cost USD 14.04–17.72 vs USD 9.54 for the 'China [For Worldwide]' variant.

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

