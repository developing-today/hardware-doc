# DinMeter — market and pricing

All observations **2026-09-04**, from `shop.m5stack.com`'s Shopify JSON endpoints (`/products/<slug>.js`),
which give SKU, price, availability and publication dates directly rather than through rendered
HTML. Prices are **USD, item price only**, excluding shipping, tax and duty. Region: the global
M5Stack store.

---

## 1. Launch pricing

| Product | SKU | Shop first published | Launch price | Evidence |
|---|---|---|---|---|
| **DinMeter** | `K134` | **2024-03-08** | USD 24.50 | shop `.js` `published_at`; the price observed today is the same figure and no price history is available, so treat "launch price" as *the current price of an EOL listing*, not as a verified 2024 observation |
| **DinMeter v1.1** | `K134-V11` | **2026-01-30** | USD 24.50 | shop `.js` `created_at 2026-01-30T10:02:16+08:00`, `published_at 2026-01-30T12:30:47+08:00` |
| Stamp-S3 | `S007` | 2023-02-10 | USD 7.50 | shop `.js` |
| Stamp-S3A | `S007-PIN254-V033` | 2025-09-11 | USD 7.50 | shop `.js` |

**The v1.1 launched at exactly the same price as the v1.0.** No premium was charged for the
module upgrade.

The 2026-01-30 launch date is corroborated independently by the official r/M5Stack weekly-products
post of the same day.

## 2. Current observations — 2026-09-04

| Date | Region | Seller | Item | Configuration | Condition | Price | Ship | Stock | Genuine? |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-04 | Global | shop.m5stack.com | **`[EOL]` M5Stack Din Meter w/ M5StampS3** | K134, full bundle | new | USD 24.50 | n/a | **out of stock** | genuine |
| 2026-09-04 | Global | shop.m5stack.com | **M5Stack Din Meter v1.1 with M5StampS3A** | K134-V11, full bundle | new | **USD 24.50** | not captured | **in stock** | genuine |
| 2026-09-04 | Global | shop.m5stack.com | `[EOL]` M5Stamp ESP32S3 Module | S007 | new | USD 7.50 | — | **out of stock** | genuine |
| 2026-09-04 | Global | shop.m5stack.com | M5StampS3A ESP32S3 Module | S007-V033 | new | USD 7.50 | — | in stock | genuine |
| 2026-09-04 | Global | shop.m5stack.com | M5StampS3A with 1.27 / 2.54 Header Pin | S007-PIN127/254-V033 | new | USD 7.50 each | — | in stock | genuine |

**The `[EOL]` prefix is M5Stack's own**, present in the product title string returned by the API.
It is not an inference.

Shipping weight for K134-V11 is **70 g** per the Shopify variant record.

## 3. Competitor and sibling prices, same source and date

| Product | SKU | Price | Note |
|---|---|---|---|
| **DinMeter v1.1** | K134-V11 | **USD 24.50** | — |
| M5Stack Dial v1.1 | K130-V11 | USD 34.90 | +USD 10.40 for round + touch, but 5 V only |
| StamPLC Controller w/ M5StampS3 | — | USD 42.90 | DIN-**rail** controller — different product category |
| Air Quality Kit v1.1 w/ M5StampS3A | — | USD 89.90 | another Stamp-S3A carrier |
| M5StampS3 BAT Module | — | USD 9.95 | — |
| M5StampS3 BreakOut | — | USD 1.95 | — |
| M5Stack VA Meter w/ M5StampS3 | — | USD 29.90 | the other Stamp-S3 instrument |

## 4. What the numbers mean

**USD 24.50 for what is in the box.** The bundle includes the device, a 250 mA·h Li-ion cell, a
screw terminal, a back clip, adhesive tape and a pin sticker. Priced against components, the
board alone (ESP32-S3 module, ST7789 panel, encoder, RTC, three converters, charger) is roughly
what you would pay for the parts — the enclosure, the DIN fit and the assembly are effectively
free. That is unusual and is the strongest value argument for the product.

**The USD 10.40 gap to the M5Dial** buys a round 240 × 240 display and a touchscreen, and costs
you the DIN cutout and the 6–36 V input. See
[`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) §3.

**A DIY equivalent lands around USD 10–18** in parts and cannot produce the enclosure. §4 of the
comparisons document works this through.

## 5. Availability and lifecycle

| | Status 2026-09-04 |
|---|---|
| DinMeter K134 | **EOL, out of stock** at the vendor |
| DinMeter v1.1 K134-V11 | current, in stock |
| Stamp-S3 S007 | **EOL, out of stock** |
| Stamp-S3A S007-V033 | current, in stock |

So the K134 and the Stamp-S3 went end-of-life **together**, which is consistent with the v1.1
being a module-substitution driven by the module's own lifecycle rather than by a product
redesign. The Stamp-S3A appeared 2025-09-11, and the DinMeter v1.1 followed 4½ months later on
2026-01-30 — the ordering you would expect if the carrier was re-released to consume the new
module.

**If you need a K134 specifically** (e.g. to match an existing deployment), the vendor no longer
sells it. Distributors may still hold stock; **no distributor inventory was surveyed in this
pass** — a declared exclusion.

## 6. Caveats on these observations

- **Single seller.** Only `shop.m5stack.com` was surveyed. Mouser, DigiKey, Amazon, AliExpress
  and regional distributors were **not** checked. Do not read these as market-wide prices.
- **Item price only.** Shipping from Shenzhen, import VAT/duty and any distributor margin are
  excluded and can be a large fraction of a USD 24.50 item.
- **No currency conversion** was performed; all figures are the store's USD.
- **No price history.** Shopify's public JSON gives the current price only. The "launch price"
  rows are the current price of a listing published on that date, not an archived observation.
- **No used/refurbished market observed.** None found; not systematically searched.
- **No clones found.** Negative search result, not proof of absence — see
  [`research-log.md`](research-log.md).
- **Sample size is one observation per product on one date.** No range, no variance.

## Related

[`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) ·
[`product-history-and-family.md`](product-history-and-family.md) ·
[`../dinmeter-v1.1/market-and-pricing.md`](../dinmeter-v1.1/market-and-pricing.md)

---

## Dated price observations — 2026-09-11 (certification/market pass)

Added **2026-09-11**, append-only. Earlier sections above are another session's work and are left exactly as written.

> ⚠ **Date note.** The session brief for this pass said 2026-09-07. The host clock, the `date:` response headers from two independent servers, and the `updated_at` field on every live product below all say **2026-09-11**. The later date is used because it is what actually happened. See `scratch/market-and-certification/README.md`.

### Method and source

Single request to the vendor's Shopify catalogue endpoint, `https://shop.m5stack.com/products.json?limit=250&page=<n>`, retrieved **2026-09-11**. This is the **strongest available evidence**: it returns `published_at`, `updated_at`, every variant, SKU, price and stock flag in one response, with no rendering and no scraping heuristics.

- **MSRP vs street price:** these are the **vendor's own list prices** — MSRP, not street. No discount, coupon or quantity break is reflected.
- **Currency:** USD as served by the store. No conversion was applied, so no conversion date applies. ⚠ LilyGO's USD prices carry odd cents (e.g. 8.04, 98.79), which is consistent with **machine conversion from CNY**; the underlying CNY price and its conversion date are **not exposed by the endpoint** and are therefore unknown.
- **Ships from:** Shenzhen, CN.
- **Stock evidence:** the per-variant `available` boolean, quoted verbatim below.
- **Condition:** new. **Genuine** — this is the manufacturer's own storefront.
- **Tax/duty:** not shown by the endpoint; not established.

### Observations

| Product (store title) | Published | Variant | SKU | Price | In stock |
|---|---|---|---|---|---|
| [EOL] M5Stack Din Meter w/ M5StampS3 | 2024-03-08 | Default Title | `K134` | **USD 24.50** | ❌ no |

Citation form required by [`guides/markets/vendor-comparison.md`](../../../guides/markets/vendor-comparison.md) § *A note on prices*, for the first row:

> *USD 24.50, 1 unit, retrieved 2026-09-11, `https://shop.m5stack.com/products/m5stack-din-meter-w-m5stamps3`, ships from Shenzhen, CN*

### Normalisation and caveats

SKU `K134`. This is the **original** DinMeter kit. It is flagged `[EOL]` in the store title and `available: false` — superseded by v1.1.

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

