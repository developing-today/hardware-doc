# Xteink X3 — market and pricing

## Current — observed 2026-09-04

Source: `https://www.xteink.com/products.json?limit=250`, retrieved 2026-09-04.
Item price only; shipping, tax and duty excluded. Ships from Shenzhen worldwide.

| Item | Variant | Price | Stock |
|---|---|---|---|
| **Xteink X3 Pocket eReader** | **Mist Gray** (`xteink-x3-white-1`) | **$69.00** | ✅ |
| **Xteink X3 Pocket eReader** | **Space Black** (`xteink-x3-black-1`) | **$69.00** | ✅ |
| X3 Magnetic Case | 6 colours | $8.99 | 5/6; **Space Black sold out** |
| X3 Protective Case | Mist Gray / Mist White | $3.99 | ✅ both |
| X3 Tempered Glass Protector | 1 / 2 / 3-pack | $4.99 / $7.99 / $9.99 | ✅ all |
| X3 Matte Screen Protector | 2 / 4 / 6-pack | $3.99 / $5.99 / $8.39 | ✅ all |
| Magnetic Pogo Pin Charging Cable | — | $4.99 | ✅ |
| Magnetic Charging Adapter | — | $5.99 | ✅ |
| eReader Magnetic Reading Light | single / dual | $9.99 / $15.99 | ✅ |

**The X3's accessory supply is materially healthier than the X4 Pro's** (where all
matte protectors and two of three glass packs are sold out) and incomparably
healthier than the X4's (**everything** sold out).

**Realistic entry price:** $69 + $4.99 spare pogo cable ≈ **$74**, or ~**$78**
with a case.

Note the **eReader Magnetic Reading Light** ($9.99) — an external clip-on light.
It exists because **the X3 has no frontlight**, and it is the vendor's own
acknowledgement of that, in the same catalogue whose X3 description claims
"adjustable warm light settings".

## Launch pricing and terms

| Date | Event |
|---|---|
| 2025-12-11 | Pre-orders open. **"Super Early Bird" units are non-refundable** |
| 2026-02-05 | Shipping begins — an **8-week** pre-order-to-ship gap |
| 2026-06-20 | **20 % off** sale on X3/X4 via the CrossPoint affiliate link — *"the best deal I've seen so far"* |
| 2026-09-04 | $69.00, both colours in stock |

## Conflicting community price

[r/XTEINK `1v5gh6x`](https://old.reddit.com/r/XTEINK/comments/1v5gh6x/) (2026-07-24)
lists *"$69 X4, **$79 X3**, $99 X4 Pro"* — the X3 figure **contradicts** the vendor
API's $69.00 and the ordering is reversed from expectation. Either a price cut
between July and September, or an error in the post. **Unresolved.**

## Secondhand

One observation: **$16**, 2026-08-18
([r/XTEINK `1vrnxnq`](https://old.reddit.com/r/XTEINK/comments/1vrnxnq/)),
described as *"dirt cheap"*, channel not stated, condition not stated.

**A single anecdote.** It is not merged with new pricing and does not establish a
used-market range. It does suggest the used market for these is soft — the same
poster's substantive complaint was about vendor conduct, not the device.

## Chinese market

**Not captured.** The vendor is China-first and Chinese pricing is announced on
Xiaohongshu (RedNote), which was not searched. For scale, the **S4** was announced
at **¥299 / ¥339** (≈US$45–50), which suggests domestic prices run well below the
international store's USD figures.

## Channel and warranty

Vendor-direct only. Note the catalogue's service SKUs: `$50 After-sale`,
`After-sales Fees`, `Exchange Handling Fees`, `Handling Fees`, `Shipping fee`.
**After-sales service is a paid product.** Budget for it rather than assuming
warranty coverage — particularly given the rear-glass fragility report.

## Caveats

- Item prices only; **shipping, tax and duty not captured**.
- Stock is a single-instant snapshot.
- The $16 figure is one anecdote with unknown channel and condition.
- No Chinese-market price captured.

---

## Dated observation — 2026-09-11, vendor store

Source: **`https://xteink.com/products.json?limit=250&page=1`**, retrieved **2026-09-11** by the
certification/market pass. Full catalogue enumerated: **25 products**. Currency USD as served, no
conversion applied. Condition: new, genuine (manufacturer store). Ships from: **not stated by the
endpoint**. Item price only — shipping, tax and duty not captured.

| Product | Published | Variant | SKU | Price | In stock |
|---|---|---|---|---|---|
| Xteink X3 Pocket eReader | 2025-12-11 | X3 Mist Gray | `xteink-x3-white` | **USD 69.00** | ✅ |
| Xteink X3 Pocket eReader | 2025-12-11 | X3 Space Black | `xteink-x3-black` | **USD 69.00** | ✅ |
| Xteink X3 Pocket eReader | 2025-12-11 | X3 + Mist Gray Base | `xteink-x3B+BW` | **USD 85.00** | ✅ |
| Xteink X3 Pocket eReader | 2025-12-11 | X3 + Space Black Base | `X3W+BB` | **USD 85.00** | ✅ |

Citation form per [`guides/markets/vendor-comparison.md`](../../../guides/markets/vendor-comparison.md) § *A note on prices*:

> *USD 69.00, 1 unit, retrieved 2026-09-11, `https://xteink.com/products/xteink-x3-pocket-ereader`, ships from CN (origin not stated by vendor)*

**USD 69.00 is unchanged from the 2026-09-04 observation** — two independent reads of the same
endpoint, one week apart, identical. The community figure of $79 recorded elsewhere in this file
remains in conflict with the vendor API and is **not** resolved by this observation.

⚠ **Not obtained:** AliExpress, Amazon, eBay, Taobao, JD and used/refurbished were **all blocked
or JS-shelled** from the research host on 2026-09-11. **No street, clone or used price is
reported here, because none was observed.** A 200 response containing no prices is a failure, not
a data point.

⚠ Six **service** line-items in the catalogue (handling fees, shipping fee, after-sale charges)
are **not products** and must be excluded from any price range — a naive "cheapest item in the
store" read returns USD 1.00.
