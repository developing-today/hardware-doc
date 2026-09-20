# DinMeter v1.1 — market and pricing

All observations **2026-09-04**, from `shop.m5stack.com`'s Shopify JSON (`/products/<slug>.js`).
USD, item price only, excluding shipping, tax and duty. Global store.

Full market context, competitor prices and caveats:
[`../dinmeter/market-and-pricing.md`](../dinmeter/market-and-pricing.md).

---

## 1. The listing

| Field | Value |
|---|---|
| Title | **M5Stack Din Meter v1.1 with M5StampS3A** |
| Slug | `m5stack-din-meter-v1-1-with-m5stamps3a` |
| SKU | **`K134-V11`** |
| Shopify product id | `9014041182465` |
| Variant id | `47570426593537` |
| **Price** | **USD 24.50** |
| Availability | **in stock** |
| Created | `2026-01-30T10:02:16+08:00` |
| Published | `2026-01-30T12:30:47+08:00` |
| Tags | `ESP32-S3`, `STAMP` |
| Shipping weight | 70 g |
| Barcode | none |

## 2. The headline: same price, and the old one is gone

| Product | SKU | Price | Availability |
|---|---|---|---|
| **DinMeter v1.1** | K134-V11 | **USD 24.50** | in stock |
| `[EOL]` DinMeter | K134 | USD 24.50 | **out of stock** |
| `[EOL]` Stamp-S3 | S007 | USD 7.50 | **out of stock** |
| Stamp-S3A | S007-V033 | USD 7.50 | in stock |

**No premium was charged for the module upgrade.** Identical price, better module, and the older
SKU withdrawn. From a buyer's point of view there is no decision to make: v1.1 is the only
option, and it costs what the old one did.

The `[EOL]` prefix is **M5Stack's own**, present in the title string returned by the API — not an
inference.

## 3. Lifecycle reading

The DinMeter K134 and the Stamp-S3 S007 went end-of-life **together**. The Stamp-S3A appeared
2025-09-11; the DinMeter v1.1 followed 4½ months later on 2026-01-30.

That ordering is exactly what you would expect if the carrier was re-released to consume a new
module whose predecessor was being retired — a **module-lifecycle event, not a product
refresh** — and it is consistent with every other piece of evidence: no new schematic, no new
STL, no new footprint, no new library release, no new board enum, and factory firmware untouched
since 2024.

## 4. Is it worth upgrading from v1.0?

| Your situation | Answer |
|---|---|
| You own a working v1.0 | **No.** The only functional gains are module-level sleep-current figures, and the *board* still cuts its battery with a latch at 38.4 µA — a figure **identical on both product pages**. You would be paying USD 24.50 for a microamp improvement you cannot use |
| You are buying new | **v1.1, obviously** — it is the only one in stock, at the same price |
| You need K134 specifically to match a fleet | Vendor stock is gone. Distributors may hold some; **no distributor inventory was surveyed** (declared exclusion). Firmware compatibility is not a reason to insist on K134 — see [`compatibility-and-status.md`](compatibility-and-status.md) |
| You are designing a new board around a Stamp | Use the **Stamp-S3A** (USD 7.50, in stock). Budget **0.6 A** on the 3.3 V rail, not 1 A, and add the GPIO38 line if you want the LED |

## 5. Other Stamp-S3A products, same date

| Product | Price | Note |
|---|---|---|
| M5StampS3A ESP32S3 Module (SMD) | USD 7.50 | |
| M5StampS3A with 1.27 Header Pin | USD 7.50 | |
| M5StampS3A with 2.54 Header Pin | USD 7.50 | SKU `S007-PIN254-V033`, published 2025-09-11 |
| Air Quality Kit v1.1 with M5StampS3A (SEN55, SCD40) | USD 89.90 | the other v1.1-suffixed carrier M5Stack refreshed |

The Air Quality Kit's parallel "v1.1 with M5StampS3A" naming is worth noting: **M5Stack applied
the same module-substitution-and-rename treatment to more than one product**, which further
supports reading the DinMeter v1.1 as a fleet-wide module transition rather than a redesign.

## 6. Caveats

Single seller (`shop.m5stack.com` only), item price only, no currency conversion, no price
history available from the public JSON, one observation on one date, no used/refurbished market
found, no clones found (a negative search result, not proof of absence), and **no distributor or
marketplace sweep**. See [`../dinmeter/market-and-pricing.md`](../dinmeter/market-and-pricing.md) §6.

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
| M5Stack Din Meter v1.1 with M5StampS3A | 2026-01-30 | Default Title | `K134-V11` | **USD 24.50** | ✅ yes |

Citation form required by [`guides/markets/vendor-comparison.md`](../../../guides/markets/vendor-comparison.md) § *A note on prices*, for the first row:

> *USD 24.50, 1 unit, retrieved 2026-09-11, `https://shop.m5stack.com/products/m5stack-din-meter-v1-1-with-m5stamps3a`, ships from Shenzhen, CN*

### Normalisation and caveats

SKU `K134-V11`. Same USD 24.50 as the EOL v1.0 kit — **the revision did not change the price**.

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

