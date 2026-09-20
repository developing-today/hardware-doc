# Market and pricing — Cap CC1101 & NFC (U219)

Observed **2026-09-04**, M5Stack official store, USD, item price only.

| SKU | Product | Price | Published |
|---|---|---|---|
| **U219** | **Cap CC1101 & NFC for Cardputer Adv** | **USD 18.95** | **2026-08-28** |
| U214 | [Cap LoRa-1262](../cap-lora-1262/market-and-pricing.md) | USD 14.50 | 2025-12-30 |
| U216 | NFC Universal Unit (**same ST25R3916**, Grove) | USD 7.00 | 2026-04-17 |
| M146 | M5Stack CC1101 Module (855–925 MHz, **single band**, Core bus) | USD 10.95 | 2025-11-07 |
| U113 / U114 | RF Unit 433 MHz RX (SYN513R) / TX (SYN115) | USD 4.50 each | 2021-05-14 |

## What the USD 18.95 actually buys

Two radios plus **three antennas**. That last part is not trivial: the LoRa Cap ships one
antenna and North-American owners routinely buy a second
([`../cap-lora-1262/market-and-pricing.md` §3](../cap-lora-1262/market-and-pricing.md)).
Here M5Stack pre-empts the problem by including 315, 433 and 868 MHz whips.

Against the alternatives:

| Want | Cheaper option | What you give up |
|---|---|---|
| NFC only, on any M5Stack host | **NFC Universal Unit (U216), USD 7.00** — same ST25R3916 over Grove | No sub-GHz. And note the M5Unit-NFC README's warning about **SoftwareI2C latency** on some Grove ports being *"too high for ST25R3916 RF timing requirements"* — the SPI Cap is the more robust connection |
| Sub-GHz only, on a Core-series host | **CC1101 Module (M146), USD 10.95** | **Single band, 855–925 MHz.** No NFC, wrong host bus |
| Cheap 433 MHz OOK | **RF Unit U113/U114, USD 4.50** | Fixed-function ASK RX or TX; no FSK, no CC1101 register access |
| **LoRa** | **Cap LoRa-1262, USD 14.50** | Different radio class entirely — [README §6](README.md) |

The band-switching Cap has no direct equivalent in M5Stack's catalogue, and the community
recognised that immediately: *"I've been using the CC1101 modules for some time, but it was
always limited to a single frequency band … This Cap supports multiple frequency bands and
has three antennas covering all of them."* — u/No_Confusion7932,
[r/CardPuter 2026-08-28](https://old.reddit.com/r/CardPuter/comments/1w0nwti/). **[COM]**

## Outside M5Stack

The obvious comparison is the **Flipper Zero**, whose sub-GHz radio is also a CC1101. The
community's own framing: *"It's like the Sub-GHz CC1101 on the Flipper Zero, except this
Cap for the Cardputer has a longer range"* — attributed to the external antenna and per-band
matching versus the Flipper's small internal antenna. That is a **plausible interpretation,
not a measurement**, and the two devices differ enormously in software maturity. A
Cardputer-Adv + Cap CC1101 is roughly USD 49 against a Flipper Zero's much higher street
price, but the Flipper ships a finished application; this Cap ships two vendor examples and
a `TODO` for Bruce.

## Availability and demand

Release-day thread: several *"Ordered!"* / *"I have mine ordered with the Zero"*. Product
JSON shows a single default variant with no backorder tag as of 2026-09-04 (contrast the
Cardputer Mesh Kit, tagged `Backorder`). Too early for a supply picture.

## Caveats

Single seller, single region, single date, seven days after launch. No marketplace, used or
clone observation — declared exclusions in [`research-log.md`](research-log.md). No price
history exists yet.

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
| Cap CC1101 & NFC for Cardputer Adv | 2026-08-28 | Default Title | `U219` | **USD 18.95** | ❌ no |
| M5Stack CC1101 Module (855-925MHz) | 2025-11-07 | Default Title | `M146` | **USD 10.95** | ✅ yes |

Citation form required by [`guides/markets/vendor-comparison.md`](../../../guides/markets/vendor-comparison.md) § *A note on prices*, for the first row:

> *USD 18.95, 1 unit, retrieved 2026-09-11, `https://shop.m5stack.com/products/cap-cc1101-nfc-for-cardputer`, ships from Shenzhen, CN*

### Normalisation and caveats

⚠ **Two different products.** `U219` is the **Cap** for Cardputer ADV (CC1101 **+ NFC**); `M146` is a standalone CC1101 **module**, not a Cap. **Not interchangeable, not one price range.** The Cap is `available: false` — newly listed (2026-08-28) and not yet in stock.

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

