# Cardputer ADV — market and pricing

> All observations **2026-09-04** unless stated. Prices are M5Stack's own store in **USD**,
> before shipping and before any tax or duty. Retrieved from Shopify's
> `search/suggest.json` and `<handle>.json` endpoints — machine-readable, so the figures are
> the store's own, not read off a rendered page.

## Official store, dated

| Product | Handle | Price (USD) | In stock | Shopify id | `created_at` | `published_at` |
|---|---|---|---|---|---|---|
| **M5Stack Cardputer Adv Version (ESP32-S3)** | `m5stack-cardputer-adv-version-esp32-s3` | **29.90** | yes | 8904041857281 | 2025-09-04 | 2025-09-05 |
| **`[EOL]` M5Stack Cardputer with M5StampS3 v1.1** | `m5stack-cardputer-with-m5stamps3-v1-1` | **29.90** | yes | 8741357388033 | 2025-03-07 | 2025-03-07 |
| **Cardputer Mesh Kit for Meshtastic (ESP32-S3)** | `cardputer-mesh-kit-for-meshtastic-esp32-s3` | **48.00** | yes | 9135211610369 | 2026-04-30 | 2026-04-30 |
| Cap LoRa 1262 for Cardputer Adv (SX1262, ATGM336H) | `cap-lora-1262-for-cardputer-adv-sx1262-atgm336h` | **14.50** | yes | — | — | — |
| Cap CC1101 & NFC for Cardputer Adv | `cap-cc1101-nfc-for-cardputer` | **18.95** | yes | — | — | — |
| Cardputer Accessory Kit v1.1 (M5StampS3A + Display) | `cardputer-accessory-kit-v1-1-m5stamps3a-display` | **9.95** | yes | 8829253157121 | 2025-07-03 | 2025-07-04 |

**The v1.1 is marked `[EOL]` in its own title but is still listed, still priced at $29.90 and
still marked available.** Read that as "old stock at the same price as the current model", which
makes it a poor buy at parity — see [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md).

### Bundle arithmetic

ADV $29.90 + Cap LoRa-1262 $14.50 = **$44.40**, versus the Mesh Kit at **$48.00**. The $3.60
premium buys the rubber-duck RP-SMA antenna, two M2 screws, a hex key, a green back shell, a
safety sticker — and, materially, **eligibility for Meshtastic device registration**, which
M5Stack states is restricted: *"Only devices in the Cardputer Mesh Kit set can be registered.
Other Cardputer/-Adv devices are not eligible for Meshtastic authorization registration."*

If you want a licensed Meshtastic node, buy the kit. If you want a LoRa radio, buy the parts.
An r/meshtastic thread of **2026-03-11** frames the same question — *"Any reason not to just get
a Cardputer with lora cap for 55 bucks total even after ship?"*, 19 comments — from before the
kit existed.

## Channels

| Channel | Evidence |
|---|---|
| **M5Stack official store** (`shop.m5stack.com`) | prices above, retrieved 2026-09-04 |
| **AliExpress** (`m5stack.aliexpress.com/store/911661199`) | M5Stack's own storefront, linked from every docs page footer. **Prices not retrieved in this pass.** |
| **Amazon** (`amazon.com/shops/m5stack`) | official storefront, linked from the docs footer. **Not retrieved.** |
| **Taobao** (`m5stack.taobao.com`) | official, CN market. **Not retrieved.** |
| **Distributors** (`m5stack.com/distributor`) | regional resellers — Mouser, Digi-Key and others typically carry M5Stack. **Not enumerated.** |
| Used / refurbished | **no observations gathered** |

Only the official-store figures above are dated and verified. **No AliExpress, Amazon,
distributor or used-market price was collected**, so this record cannot support a price *range*,
a street-price claim, or a regional comparison. Stated plainly rather than estimated.

## Clones

**None found.** Searching GitHub for `cardputer` returned 100 repositories, all software or
accessories for the genuine article; no clone hardware appeared in the Reddit sample either.
That is unsurprising: the value is in the keyboard tooling and the case, and the board is
already $29.90.

The nearest thing to a "compatible" is the **Cardputer Accessory Kit v1.1** ($9.95), which is a
genuine M5Stack spare — a Stamp-S3A plus a display. It is **not** an ADV upgrade path; the ADV's
differences are on the mainboard.

⚠ **A negative from one day's searching in English and on GitHub/Reddit is weak evidence.**
Taobao and AliExpress were not searched. Treat "no clones" as *not found*, not *do not exist*.

## Total cost of a working setup

| Configuration | Cost | Notes |
|---|---|---|
| ADV alone | $29.90 | includes the 1750 mAh battery |
| ADV + microSD | ~$35 | no card included; no vendor card guidance exists |
| ADV + Cap LoRa-1262 + antenna | ~$46–50 | antenna sold with the kit, separately otherwise |
| **Mesh Kit** | **$48.00** | complete, licensed, ready to use |
| ADV + Cap CC1101 & NFC | $48.85 | the sub-GHz/NFC configuration |
| Everything | ~$68 | ADV + both Caps |

Shipping, duty and tax are **not** included and vary by destination. The r/CardPuter thread of
2026-05-31 is a reminder that for many buyers these dominate: the poster describes shipping and
customs as the reason a Flipper Zero was out of reach in the first place.

## Second-hand and repair economics

* **Spares are hard to get.** r/M5Stack, 2026-08-05: *"I'm looking for screws and buttons of the
  right height for the Cardputer ADV, but I can't find them on AE."* Replies point at a generic
  M5Stack M3 screw pack and 3D printing. M5Stack does not stock ADV-specific mechanical spares.
* **The battery is internal**, with no published cell part number, so a worn cell is a repair
  job rather than a swap.
* One Reddit reply (2026-05-31) claims people *"resell it x3 price"* — an unsupported assertion
  from a joking comment, recorded only to note that no actual used-market data was found.

## Market fit

**At launch (September 2025):** a same-price replacement for a popular board, offering
peripherals rather than compute. A reasonable first purchase; a marginal upgrade.

**At this snapshot (September 2026):** the ADV is the only Cardputer worth buying new. The v1.1
is `[EOL]` at the same money, the accessory line is ADV-only, and upstream Meshtastic supports
only the ADV. At $29.90 with a 1750 mAh cell, a codec, an IMU and an expansion socket, it is
priced below what the parts alone would suggest.

See the applicable genre guidance and the tier-by-tier alternatives in
[`comparisons-and-recommendations.md`](comparisons-and-recommendations.md).

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
| M5Stack Cardputer Adv Version (ESP32-S3) | 2025-09-05 | Default Title | `K132-ADV` | **USD 29.90** | ✅ yes |

Citation form required by [`guides/markets/vendor-comparison.md`](../../../guides/markets/vendor-comparison.md) § *A note on prices*, for the first row:

> *USD 29.90, 1 unit, retrieved 2026-09-11, `https://shop.m5stack.com/products/m5stack-cardputer-adv-version-esp32-s3`, ships from Shenzhen, CN*

### Normalisation and caveats

SKU `K132-ADV`. In stock.

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

