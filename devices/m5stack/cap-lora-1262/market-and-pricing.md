# Market and pricing — Cap LoRa-1262 (U214)

All observations **2026-09-04**, region: M5Stack official store (ships from Shenzhen),
currency **USD**, prices as returned by the Shopify product JSON (item price only —
shipping, duty and tax excluded).

## 1. Official store, dated

| SKU | Product | Price | Published | Status |
|---|---|---|---|---|
| **U214** | **Cap LoRa-1262** | **USD 14.50** | 2025-12-30 | current |
| U201 | LoRa+GPS Cap ("Cap LoRa868") | USD 14.50 | 2025-09-05 | **[EOL]** |
| U219 | [Cap CC1101 & NFC](../cap-cc1101/market-and-pricing.md) | USD 18.95 | 2026-08-28 | current |
| K132-ADV | Cardputer Adv (host) | USD 29.90 | 2025-09-05 | current |
| K152 | [Cardputer Mesh Kit](../cardputer-mesh-kit/README.md) = ADV + U214 + antenna | USD 48.00 | 2026-04-30 | Backorder (tag) |

**The successor did not raise the price.** U201 and U214 are both USD 14.50; the +2 dB, the
shield can, the Grove port and the RF switch came at no list-price change.

### 1.1 Is the Mesh Kit worth it?

Bare arithmetic: 29.90 + 14.50 = **44.40** vs **48.00** for K152 — a **USD 3.60 premium**.
What the premium buys: a green-back Cardputer-Adv, the rubber-duck antenna (also included
with a standalone U214), two M2 screws, a hex key, a safety sticker, **Meshtastic
pre-flashed**, and — the only part that cannot be bought separately — **eligibility for
Meshtastic authorised-device registration**. M5Stack states: *"Only devices in the
Cardputer Mesh Kit set can be registered. Other Cardputer/-Adv devices are not eligible."*
**[DOC]**

The community asked this question directly and did not reach consensus:
*"Cardputer Mesh Kit vs buying Cardputer-Adv + Cap LoRa-1262 separately — worth it…?"*
([r/CardPuter 2026-07-13](https://old.reddit.com/r/CardPuter/comments/1uv6gt3/), 9 comments)
and *"meshtastic kit vs cardputer adv"*
([r/CardPuter 2026-07-30](https://old.reddit.com/r/CardPuter/comments/1vb2fmc/), 10 comments).
**[COM]**

## 2. Availability

Sold out repeatedly after launch. Firsthand reports:

- u/resentedpoet, 2025-12-31: *"Ordered one earlier and glad I did. See they are sold out again."*
- u/MadmaxEndGame, 2026-01-02: *"I checked the website and it's out of stock."*
- u/secret-bong, 2026-01-17: *"I think they came back this week."*
- 2026-01-15 post title: *"Cap Lora 1262 module(with grove port) in stock at M5stack"*

([r/M5Stack 1pzazbe](https://old.reddit.com/r/M5Stack/comments/1pzazbe/),
[r/CardPuter 1pzazuu](https://old.reddit.com/r/CardPuter/comments/1pzazuu/),
[r/CardPuter 1qdb75x](https://old.reddit.com/r/CardPuter/comments/1qdb75x/)). **[COM]**
Sample: four independent reports over three weeks. Enough to say launch supply was tight;
not enough to characterise current supply.

## 3. The hidden cost: antennas and adapters

This is the recurring real-world expense, and it is not in the list price.

| Item | Why | Evidence |
|---|---|---|
| 915 MHz antenna | Box contains **one 868 MHz** whip; NA users need 915 | [r/CardPuter 2026-08-22](https://old.reddit.com/r/CardPuter/comments/1vvlcs9/) |
| SMA ↔ RP-SMA gender/polarity adapter | Connector polarity is disputed (conflict **G1**) | u/malonestar bought a four-way adapter pack; u/goattrybe links a converter — [r/CardPuter 2025-09-19](https://old.reddit.com/r/CardPuter/comments/1nkyy4c/), [r/M5Stack 2026-02-03](https://old.reddit.com/r/M5Stack/comments/1pzazbe/) |

u/malonestar, 2025-09-19: *"Had to wait a few extra days for some sma gender converters /
adapters. I cannot for the life of me find an SMA female antenna for the US."* **[COM]**

## 4. Regional price friction

u/[OP], [r/M5Stack 2026-01-17](https://old.reddit.com/r/M5Stack/comments/1qfc24p/),
*"Why would the same cart cost €67 on AliExpress and €44 on the official site"* (18
comments). Recorded as an owner observation about M5Stack pricing generally, **not**
normalised for shipping, duty or bundle contents, and **not** verified here. Marketplace
pricing was a declared exclusion of this pass.

## 5. Alternatives, by intent

| If you want | Consider | Why not the Cap |
|---|---|---|
| Meshtastic on a Cardputer-Adv you already own | **U214** | — |
| Meshtastic on the **original** Cardputer | **[Unit C6L (U202)](../unit-c6l/README.md)**, USD 22.90 | The Cap will not fit. The C6L is a self-contained ESP32-C6 + SX1262 node on a Grove cable |
| Sub-GHz capture/replay + NFC, not LoRa | **[Cap CC1101 (U219)](../cap-cc1101/README.md)**, USD 18.95 | CC1101 cannot do LoRa (chirp spread spectrum is Semtech-proprietary) |
| LoRaWAN with a certified stack | **LoRaWAN Unit (U184-\*, STM32WLE5)**, USD 18.95–21.50 | No LoRaWAN stack has been demonstrated on the Cap |
| Simple point-to-point serial LoRa | **LoRa Unit E220 (U170/U170-433)**, USD 12.95–33.00 | AT-command modem; far less capable but far less work |
| A dedicated mesh node, not a handheld | Heltec V3/V4, LilyGO T-Deck — repeatedly compared by owners | Different product class; the Cardputer's value is the keyboard |

Owner comparisons worth reading: *"Heltec V4 vs Cardputer Adv (Meshcore)"*
([r/CardPuter 2026-06-07](https://old.reddit.com/r/CardPuter/comments/1tzlmx9/), 32 upvotes),
*"Question about heltec v3-4 and cardputer adv"*
([2026-07-09](https://old.reddit.com/r/CardPuter/comments/1urr84f/)). **[COM]**

## 6. Caveats on everything above

Single-seller, single-region, single-date snapshot. No marketplace, used, refurbished or
clone observation was gathered — a declared exclusion in
[`research-log.md`](research-log.md). No clone of this Cap was found, which is unsurprising
for a nine-month-old accessory to a niche host, but absence of evidence here is weak.

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
| Cap LoRa 1262 for Cardputer Adv (SX1262, ATGM336H) | 2025-12-30 | Default Title | `U214` | **USD 14.50** | ✅ yes |
| [EOL] LoRa+GPS Cap for Cardputer Adv (SX1262, ATGM336H) | 2025-09-05 | Default Title | `U201` | **USD 14.50** | ❌ no |

Citation form required by [`guides/markets/vendor-comparison.md`](../../../guides/markets/vendor-comparison.md) § *A note on prices*, for the first row:

> *USD 14.50, 1 unit, retrieved 2026-09-11, `https://shop.m5stack.com/products/cap-lora-1262-for-cardputer-adv-sx1262-atgm336h`, ships from Shenzhen, CN*

### Normalisation and caveats

`U214` is the current part; `U201` is an `[EOL]` predecessor at the **same USD 14.50**.

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

