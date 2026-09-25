# Market and pricing — M5Stack PaperMono

> **Every observation on this page is dated 2026-09-01 (UTC)** unless a row says otherwise.
> Eleven days after launch, at which point **both SKUs were out of stock at the official store
> and had been for all but nine minutes of the product's commercial life.**
>
> ## Three rules this page follows, stated up front
>
> 1. **Launch pricing and current pricing are kept separate.** For this product they happen to
>    coincide — see [§1](#1-launch-pricing-versus-current-pricing) — and that is itself recorded
>    rather than glossed over.
> 2. **No currency conversion is performed anywhere.** Three sellers, three currencies, three VAT
>    regimes, three shipping arrangements. A converted "equivalent" would be a fabricated number
>    ([§3](#3-why-there-is-no-converted-comparison)).
> 3. **PaperMono and PaperMono-Lite are never merged**, and bare units are never merged with
>    bundles. They are distinct SKUs at distinct prices.

## Contents

- [1. Launch pricing versus current pricing](#1-launch-pricing-versus-current-pricing)
- [2. Current observations — PaperMono (C153)](#2-current-observations--papermono-c153)
- [3. Why there is no converted comparison](#3-why-there-is-no-converted-comparison)
- [4. Current observations — PaperMono-Lite (C153-LITE)](#4-current-observations--papermono-lite-c153-lite)
- [5. Method — where these numbers came from](#5-method--where-these-numbers-came-from)
- [6. Stock evidence, and what the −129 means](#6-stock-evidence-and-what-the-129-means)
- [7. Availability history](#7-availability-history)
- [8. Restock: the vendor and the press disagree](#8-restock-the-vendor-and-the-press-disagree)
- [9. Confirmed not sold](#9-confirmed-not-sold)
- [10. No determination possible](#10-no-determination-possible)
- [11. Used, clone and marketplace supply](#11-used-clone-and-marketplace-supply)
- [12. What this pricing picture is worth](#12-what-this-pricing-picture-is-worth)
- [13. Gaps](#13-gaps)

---

## 1. Launch pricing versus current pricing

The method requires these to be recorded separately. For an eleven-day-old product they are the
same numbers, and the honest statement is *why*:

| | Launch (2026-08-21) | Current (2026-09-01) |
|---|---|---|
| PaperMono `C153`, M5Stack store | **USD 65.00** | **USD 65.00** |
| PaperMono-Lite `C153-LITE`, M5Stack store | **USD 55.00** | **USD 55.00** |
| Evidence | Shopify `published_at` 2026-08-21T12:00:10+08:00 with the price field as read on 2026-09-01 | Shopify `price` field, read 2026-09-01 |
| Confidence | **Inferred, not observed.** Shopify exposes no price history | **Observed** |

**The launch row is an inference and must be read as one.** Shopify's product JSON gives the
current price and the publication timestamp, not a price history. The product has been out of
stock since minutes after launch, so there has been no commercial reason to reprice it, and no
source anywhere reports a price change. That is a reasonable basis for saying the launch price
equals the current price — and it is still an inference. **Nobody observed the price on
2026-08-21.**

These are **MSRP / list prices at the manufacturer's own store**. There is no crowdfunding
price, no introductory price, no observed street price, and no discount in evidence: the product
has never been in a state where a street price could form.

## 2. Current observations — PaperMono (C153)

| Field | Observation 1 | Observation 2 | Observation 3 | Observation 4 |
|---|---|---|---|---|
| **Date** | 2026-09-01 | 2026-09-01 | 2026-09-01 | 2026-09-01 |
| **Seller** | **M5Stack official store** | **The Pi Hut** | **OpenELAB (.io)** | **OpenELAB (.de)** |
| **Region** | Global — a single Shopify market (`market_setup_type: single_market`) | UK | International / EU | Germany |
| **Condition** | new | new | new | new |
| **Configuration** | **Bare unit.** The vendor "Includes" list is literally `1 x PaperMono` — no bundle, no accessories | Bare unit, SKU `C153` | Bare unit, SKU `M5-C153`, barcode `17841945721489` | Same SKU |
| **Genuine / clone** | **genuine — manufacturer direct** | genuine — listed M5Stack reseller | genuine — listed reseller | genuine — listed reseller |
| **Item price** | **65.00** | **62.40** | **79.95** | **79.95** |
| **Currency** | **USD** (confirmed: `Shopify.currency.active = "USD"`) | **GBP** | **EUR** (`Shopify.currency.active = "EUR"`) | **EUR** |
| **Tax treatment** | **not stated pre-checkout** | page markup says **`incl. VAT`** for domestic, with an `excl. VAT` toggle for international | not stated | not stated |
| **Shipping** | not shown pre-checkout | not shown | not shown | not shown |
| **Stock evidence** | **Out of stock.** `product.available = false`; variant `50199717249281`, `inventory_policy = "deny"`, **`inventory_quantity = -129`** | **Out of stock.** JSON-LD `availability: http://schema.org/OutOfStock`; page carries "Sold out" / "Pre-order" / "Coming soon" | **`available = true`, but the title itself is suffixed "(Pre-sale)"** — a pre-order, not stock on hand | Same, suffixed **"(Vorverkauf)"** |
| **Listing created** | `2026-08-18T14:29:31+08:00` | `2026-08-21T11:15:48+01:00` | `2026-08-21T06:12:30+02:00` | `2026-08-21T06:13:28+02:00` |
| **Source** | S48 | S53 | S54 | S55 |

### What these four rows actually mean

**None of them is a purchasable unit on 2026-09-01.** Two say "out of stock" outright, and two
say "available" while their own titles say "pre-sale". The OpenELAB rows are the trap: a naive
scrape reads `available: true` and reports EUR 79.95 as a live price. It is a **pre-order at an
announced price**, which is a different commercial object from stock on a shelf, and it is
recorded as such.

**The Pi Hut's number is the only one whose tax treatment is stated**, and it is stated as
*inclusive*. So GBP 62.40 and USD 65.00 are not the same kind of number even before exchange
rates enter the picture: one contains UK VAT and one does not contain any sales tax at all.

**The EUR 79.95 rows carry a reseller markup of unknown composition.** Whether the gap over the
manufacturer price is VAT, import duty, margin, or all three is not established — none of the
three sellers exposes a tax breakdown pre-checkout.

## 3. Why there is no converted comparison

The method explicitly warns against merging observations "into one range without explicit
normalization". Here, normalisation is not available:

| Obstacle | Detail |
|---|---|
| **Three currencies** | USD, GBP, EUR — each confirmed from the storefront's own currency token, not assumed |
| **Three tax regimes** | M5Stack: not stated. The Pi Hut: **incl. VAT** (UK), with an explicit ex-VAT toggle for international buyers. OpenELAB: not stated |
| **Three shipping arrangements** | None of the three shows shipping before checkout. A US-direct order, a UK domestic order and an EU pre-order have materially different landed costs |
| **Two commercial states** | Two out-of-stock listings and two pre-orders |
| **No conversion date would be honest** | A rate on 2026-09-01 applied to a price that includes VAT in one row and excludes it in another produces a number that is wrong in a way the reader cannot see |

**So: read each row on its own terms.** The one comparison that *is* safe is the internal one —
`C153` at USD 65.00 against `C153-LITE` at USD 55.00, same seller, same currency, same day,
same tax treatment. **That USD 10 buys exactly the NFC and LoRa hardware** and nothing else;
everything else about the two boards is identical
([`product-history-and-family.md` §6](product-history-and-family.md#6-papermono-and-papermono-lite)).

## 4. Current observations — PaperMono-Lite (C153-LITE)

| Field | Value |
|---|---|
| **Date** | 2026-09-01 |
| **Seller** | M5Stack official store |
| **Region** | Global (single Shopify market) |
| **Condition / configuration** | New; bare unit. "Includes": `1 x PaperMono-Lite` |
| **Genuine / clone** | genuine — manufacturer direct |
| **Item price** | **55.00 USD** |
| **Tax / shipping** | not stated pre-checkout |
| **Stock evidence** | **Out of stock.** `product.available = false`; variant `50199714988289`, `inventory_policy = "deny"`, **`inventory_quantity = 0`** |
| **Listing created / published** | `2026-08-18T14:26:42+08:00` / `2026-08-21T12:00:09+08:00` |
| **Source** | S49 |

**No Lite listing was found at any reseller anywhere.** The Pi Hut, OpenELAB (.io and .de),
Switch Science, Adafruit, Reichelt, Botland and Core Electronics all returned zero results for
it, on the same day those same sellers were checked for the full model. Whether that is a
distribution decision or simply lag is **not established** — it is eleven days old and the full
model reached three resellers, so lag is plausible but unevidenced.

**Note the two SKUs are in different inventory states**: `-129` for the C153, exactly `0` for
the Lite. That difference is the single most interesting number on this page (§6).

## 5. Method — where these numbers came from

Every M5Stack-family price was taken from **Shopify storefront JSON** rather than rendered page
text:

| Endpoint | Gives |
|---|---|
| `/products/<handle>.json` | `price`, `sku`, `created_at`, `published_at`, variant IDs |
| `/search/suggest.json` | `product.available` (a boolean) |
| Product page HTML | the *Stoq / RestockRocket* app embeds `window._RestockRocketConfig.variantsInventoryQuantity` and `variantsInventoryPolicy` — **exact per-variant on-hand counts, including negatives** |

This matters for reproducibility: a screenshot of a price is a claim, a `price` field with a
`published_at` beside it is a record. `shop.m5stack.com` served all of this to a plain
`curl/8.5.0` with no user-agent rotation needed.

The RestockRocket detail is a general technique, not an M5Stack quirk — any Shopify store
running that app leaks per-variant on-hand counts in its product HTML. It is what produced the
`-129`, and it is worth looking for before concluding that a store exposes only a boolean.
Recorded for reuse in [`research-log.md`](research-log.md) and the vendor guide
[`vendors/m5stack`](../../../vendors/m5stack/README.md).

## 6. Stock evidence, and what the −129 means

Shopify reports a **negative** on-hand quantity when fulfilled or accepted orders exceed counted
stock.

**The literal, defensible statement is:** *the storefront's inventory counter for variant
`50199717249281` stood at **−129** on 2026-09-01.* Evidence type: **firsthand measurement of
vendor storefront data.**

**The interpretation is weaker than the measurement**, and the two must not be conflated:

- It is **consistent with** 129 units of oversell or backorder, which would match the vendor's
  own statement that pre-orders "reached the limit" (S71) and the community's independent
  reports of a capped pre-order batch.
- It is **also consistent with** a stock-count correction, a fulfilment adjustment, or a
  migration artefact. Shopify negatives arise from several mechanisms.
- Therefore: **corroborating evidence, not proof of a 129-unit backlog.** Evidence type for the
  interpretation: **inferred.**

The contrast with the Lite's exact `0` is what makes the number interesting at all. Two SKUs
launched in the same second, from the same store, in different inventory states eleven days
later. That is a real, measured asymmetry between the two products' demand or allocation — and
this record does **not** know which.

`inventory_policy = "deny"` on both means the store refuses to sell past zero, which is why
neither is purchasable regardless of the counter's sign.

## 7. Availability history

| Date | State | Evidence |
|---|---|---|
| 2026-08-18 06:29 UTC | Both storefront records created, unpublished | Shopify `created_at` (S48, S49) |
| **2026-08-21 04:00 UTC** | **Both SKUs published.** Lite at 12:00:09 +08:00, full model at 12:00:10 +08:00 | Shopify `published_at` |
| **2026-08-21 04:09 UTC** | **First independent sell-out report — nine minutes later**, with photographs | @henry19840301 (S72) |
| 2026-08-21 08:44 UTC | Vendor posts to r/M5Stack; later states pre-orders **"reached the limit"** | Reddit (S71) |
| 2026-08-21 ~12:00 UTC | HN submitter reports it was already out of stock ~8 h post-announcement | HN (S69) |
| 2026-08-21 | Multiple independent failed-purchase reports: `shackburger` ("woke up … saw the launch email and it was already sold out"), `9mini-paralyses` ("probably the quickest sellout on their site that I've seen") | r/M5Stack (S71) |
| 2026-08-22 10:09 UTC | @berryxia reports stock gone, asks for restock | X (S73) |
| **2026-09-01** | **Still out of stock. Eleven days.** | Shopify (S48, S49) |

> **On "sold out in one second".** That phrasing originated with the buyer who posted at 04:09
> UTC and was repeated on Hacker News, where another user pushed back on it at the time. **The
> checkable fact is a nine-minute gap** between storefront publication and a sell-out report,
> which is an upper bound on how long stock lasted, not a measurement of it. Record the nine
> minutes. Evidence type: **firsthand ownership report** for the purchase, **opinion/colloquial**
> for the "one second".

## 8. Restock: the vendor and the press disagree

| Date | Source | Statement | Evidence type |
|---|---|---|---|
| 2026-08-21 | **CNX-Software** | "The company says the quantity is limited, and **the next batch will be available next year**." | **Reproduced vendor statement, second-hand** — CNX neither quotes nor links a vendor source |
| **2026-08-22 10:54 UTC** | **@M5Stack on X**, replying to @berryxia | 「要等两三个月了」 — ***"you'll have to wait two or three months"*** | **Direct vendor statement, primary** (S74) |
| 2026-08-21 | u/No-Connection1900 (M5Stack's Reddit account) | pre-orders "reached the limit" | Direct vendor statement, primary (S71) |
| 2026-08-27 | HN user `notatoad` | "i can't remember where i read it, but a few days ago i saw they didn't expect a restock until next year" | **Hearsay, self-flagged as unsourced** |

**Both recorded; neither preferred.** "Two or three months" from 2026-08-22 lands in
October–November 2026; "next year" is at least January 2027. They are not reconcilable and no
evidence chooses between them. Tracked as
[C7](gaps-and-conflicts.md#c7--restock-timing).

> ### The e-ink driver IC shortage claim is hearsay — checked and rejected
>
> HN user `big_toast` wrote on 2026-08-27 that "M5Stack's twitter says 2 to 3 months to restock
> **because they're out of eink driver ic**", citing
> `x.com/M5Stack/status/2091116748686922069`.
>
> **That tweet was retrieved in full, along with its parent and the thread root.** It says only
> 「要等两三个月了」. The parent (@berryxia, 10:09 UTC) merely asks for a restock. The thread root
> (@M5Stack, 07:49 UTC) is a "PaperMono vs PaperMono-Lite" marketing post. **The driver-IC
> reason does not appear anywhere in the cited chain.**
>
> This is the one place in this record where a widely repeated commercial explanation was
> checked against its own citation and failed. Do not propagate it without a new source.

## 9. Confirmed not sold

All checked 2026-09-01. **These negatives are as valuable as the positives**, and they are
negatives — each search returned HTTP 200 with a working result page.

| Seller | Query | Result |
|---|---|---|
| **Amazon.com** | `m5stack papermono` | Page reports "5 results": an A5 loose-leaf paper refill and four unrelated M5Stack items. **No PaperMono listing** (S57) |
| **AliExpress** | `wholesale-papermono` | One product returned — M5Stack **PaperColor** at US $127.91 / $182.87 from third-party sellers. **No PaperMono or Lite** (S58). Independently corroborates CNX-Software's 2026-08-21 note that it is "not listed on AliExpress (anymore)" |
| **Switch Science** (JP, official M5 distributor) | `PaperMono` | 「PaperMono」の検索結果**0件** (S59) |
| **Adafruit** | `papermono` | "No products found for 'papermono'" (S60) |
| **Reichelt** | `papermono` | "Die Suche nach papermono hatte **0 Treffer**" (S61) |
| **Botland** | `papermono` | 0 products (S62) |
| **Core Electronics** (AU) | `papermono` | 0 products (S63) |
| Secondary sweep — MakerLab Electronics, Elektor, BerryBase, Robu.in, Cytron, MC Hobby | various | no listings (S67) |

**The AliExpress row deserves a second look.** It returned PaperColor at **$127.91 and $182.87**
— against M5Stack's own $75.00 for that product. That is what third-party marketplace pricing of
this vendor's e-paper boards looks like: roughly **1.7× to 2.4× the manufacturer price**. It is
one product and two listings on one day, so it is an **illustration, not a rate**, but it is the
only marketplace datapoint anywhere in this pass and it is worth knowing before assuming a
marketplace restock would be cheap.

## 10. No determination possible

Recorded separately from §9 so a later pass does not mistake a bot-wall for an absence.

| Seller | Result | Why it matters |
|---|---|---|
| **Mouser** | 13.9 KB bot-denial page (S64) | **On M5Stack's own distributor list** (`m5stack.com/distributor`, S56) |
| **DigiKey** | HTTP 403 (S65) | Also on the distributor list |
| **TinyTronics** | HTTP 403 (S66) | — |

**Absence at Mouser and DigiKey is genuinely unknown, not negative.** One adjacent datapoint:
a YouTube creator reported on 2026-07-14 that **DigiKey still stocked the EOL M5Paper v1.1** —
evidence that DigiKey carries this product family, not that it carries PaperMono.

Next steps for a later pass are known: Mouser publishes a **Search API** and DigiKey has an
OAuth API. Neither was used here.

## 11. Used, clone and marketplace supply

**There is none, and the reason is structural.**

| Market | Finding |
|---|---|
| Used / refurbished | **No observation anywhere.** No eBay, marketplace or forum sale was located |
| Clones / compatibles | **None found.** No clone listing on AliExpress or Amazon |
| Liquidation | not applicable — the product is eleven days old |

A device that has been purchasable for approximately nine minutes cannot have a secondary
market. **This is a statement about 2026-09-01, not a property of the product**, and it is the
row most likely to change first after a restock.

The absence of clones is likewise uninformative at eleven days. What *would* be informative
later: this board's two custom chips (M5PM1, M5IOE1) are M5Stack-proprietary parts, which is a
practical barrier to a drop-in clone in a way that a WROVER-and-expander design is not.
`inferred`.

## 12. What this pricing picture is worth

Four conclusions a buyer can actually use, each with its limits stated:

1. **The list price is USD 65.00 (C153) / USD 55.00 (C153-LITE), direct from the manufacturer.**
   Firm, measured, single-source-but-authoritative.
2. **You cannot buy one.** Firm on 2026-09-01, at every seller checked, including two that say
   "available" and mean "pre-order".
3. **A reseller pre-order at EUR 79.95 is the only route with a stated availability path** — and
   it is a pre-order against an unrestocked product with contested restock guidance, so the
   delivery date is effectively unknown.
4. **Price comparison against alternatives is not meaningful from this data alone.** Not because
   the alternatives are unknown — see
   [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) — but because a
   price you cannot transact at is not a price. The nearest in-family alternative, the PaperS3 at
   USD 59.00, is **EOL** and equally unpurchasable.

The one genuinely durable commercial fact here is the **USD 10 delta between the two SKUs**,
because it is a same-seller, same-day, same-currency, same-tax comparison of two products that
differ in exactly two components. Everything else on this page has a caveat attached to it.

## 13. Gaps

| Gap | Why it matters | Next step |
|---|---|---|
| **Mouser / DigiKey / TinyTronics unknown** | All are or are adjacent to listed M5Stack distributors; bot-walled, so absence is unproven | Mouser Search API; DigiKey OAuth API |
| **No Lite listing at any reseller** | Distribution decision or lag is unresolved | Re-check after restock |
| **No price history for any row** | Shopify exposes none; the launch-price row in §1 is therefore an inference | Wayback captures of the product pages, if any exist |
| **Tax and shipping unresolved at three of four sellers** | Landed cost is the number a buyer actually pays, and it is unknown for USD and EUR rows | Requires a checkout simulation, which was not attempted |
| **XTEINK X4 Pro not priced** | It is the comparison the community actually makes ([`community.md`](community.md)) | `xteink.com` product page, linked from a 2026-01-24 YouTube description |
| **Waveshare e-paper line not priced** | Named as a competitor; this knowledge base's Waveshare records cover **LCD** boards only | See [`comparisons-and-recommendations.md` §5](comparisons-and-recommendations.md#5-waveshare--gap-closed-2026-09-01) |
| **No used or clone market observation** | Nothing to observe yet (§11) | Re-run after restock |

## Related

- [`product-history-and-family.md`](product-history-and-family.md) — the dated launch chronology these prices sit in
- [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) — what else the money buys, by tier
- [`community.md`](community.md) — the sell-out reports and the rejected shortage claim, as evidence
- [`../papermono-lite/README.md`](../papermono-lite/README.md) — the USD 55 variant
- [`gaps-and-conflicts.md` C7](gaps-and-conflicts.md#c7--restock-timing) — the restock conflict
- [`research-log.md`](research-log.md) — every query, filter and disposition, including the bot-walls
- [`sources.md`](sources.md) — S48–S67 (retail), S71–S79 (statements and coverage)
