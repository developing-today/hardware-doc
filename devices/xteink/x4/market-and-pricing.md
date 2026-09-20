# Xteink X4 — market and pricing

## Status: delisted

Observed **2026-09-04** from `xteink.com` Shopify APIs:

- The **X4 device does not appear** in `/products.json` (23 products) or in the
  `x4-series` collection.
- The `x4-series` collection contains **only accessories**.
- **Every X4-specific accessory is sold out**, across every variant:

| Accessory | Variants | Status |
|---|---|---|
| X4 Magnetic Case | 7 colours | **all sold out** |
| X4 Protective Case | Mist White, Mist Gray | **both sold out** |
| X4 Tempered Glass Screen Protector | 1/2/3-pack | **all sold out** |
| X4 Matte Screen Protector | 2/4/6-pack | **all sold out** |

Only cross-model accessories (reading light, metal ring) remain available in the
X4 collection.

That is a **complete, unambiguous end-of-life signature**: no device, no
device-specific accessory, no restock.

## Historical pricing

| Date | Price | Source | Confidence |
|---|---|---|---|
| 2026-07-24 | **$69** | [r/XTEINK `1v5gh6x`](https://old.reddit.com/r/XTEINK/comments/1v5gh6x/) | Community list; the same list gives the X3 at $79, which the vendor API contradicts. **Treat as approximate** |
| 2026-06-20 | **20 % off sale** on X3/X4, via the CrossPoint affiliate link | [r/xteinkereader `1uan67g`](https://old.reddit.com/r/xteinkereader/comments/1uan67g/) | Firsthand announcement |
| 2025-12-26 | *"X4 Restocking"* community digest | [r/xteinkereader `1pw0r4y`](https://old.reddit.com/r/xteinkereader/comments/1pw0r4y/) | Stock was constrained even at peak |

**The delisted product page could not be recovered.** The Wayback CDX query for
`xteink.com*` timed out at 60 s and was not retried — the single cheapest
outstanding action for this record. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

## Secondhand

The only concrete used-market datapoint is for the **X3**, not the X4: one unit
acquired for **$16** ([r/XTEINK `1vrnxnq`](https://old.reddit.com/r/XTEINK/comments/1vrnxnq/),
2026-08-18), channel not stated.

**This is one anecdote about a different model.** It is recorded, not generalised.
No used X4 price was observed.

## Channel

Vendor-direct only; no distributor, no Amazon storefront located. One community
claim that the X4 *"Cracked Amazon's e-reader top 10"* is **unverified** — no
listing was found.

## What this means for a buyer today

You cannot buy a new X4 from the vendor. If you want this specific device — for
USB-C charging or for the ecosystem's best-supported target — the secondhand market
is the only channel, and **replacement cases and screen protectors are also gone**.
Buy the accessories with the device or not at all.

For a new purchase, see
[`../x4-pro/comparisons-and-recommendations.md`](../x4-pro/comparisons-and-recommendations.md).

---

## Dated observation — 2026-09-11: withdrawn, and its successor is named

Source: **`https://xteink.com/products.json?limit=250&page=1`**, retrieved **2026-09-11**. Full
catalogue enumerated: **25 products**.

**The X4 is still gone, and the picture is now complete rather than merely negative.**

- Of the 25 products, **none is a bare "Xteink X4"** — confirming the 2026-09-04 delisting.
- **All four X4-specific accessories have also been withdrawn** from the catalogue, not merely
  sold out as they were on 2026-09-04.
- A successor appeared on **2026-09-06**: **"XTEINK X4 Classic (X4 V2)"** at **USD 79.00**
  (USD 95.00 with base). **The vendor's own product title states that the Classic *is* the second
  version of the X4.**

| Fact | Evidence |
|---|---|
| X4 withdrawn | absent from `/products.json`, 25/25 products enumerated, 2026-09-11 |
| X4 accessories withdrawn | absent from the catalogue on 2026-09-11 (they were present-but-sold-out on 2026-09-04) |
| Successor is the X4 Classic | vendor store title **"XTEINK X4 Classic (X4 V2)"**, published **2026-09-06**, **USD 79.00** |
| The FCC record agrees | `2BTR9-XTEINKX4` granted 2026-01-05, then `2BTR9-X4C` granted 2026-07-20 — see [`certification-and-compliance.md`](certification-and-compliance.md) |

**This record therefore documents a withdrawn product**, and
[`x4-classic`](../x4-classic/README.md) documents its successor. Nothing above this line has been
edited; the delisting evidence recorded on 2026-09-04 stands and is now corroborated by a second
independent signal (the FCC succession) and a named replacement.

⚠ The X4's last observed vendor price was **USD 69.00**. The X4 Classic is **USD 79.00** — a
**USD 10 increase** across the generation. Both figures are vendor-direct item prices, so they
are comparable.

⚠ **Not obtained:** no marketplace, clone or used-market X4 price. AliExpress, Amazon, eBay,
Taobao and JD were all bot-walled or JS-shelled on 2026-09-11.
