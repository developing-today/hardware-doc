# Xteink X4 Classic — market and pricing

## There is no pricing. That is the finding.

Observed **2026-09-04** from `xteink.com`'s Shopify APIs:

- `/products.json` (23 products, complete — pages 2 and 3 empty) contains **no X4
  Classic**.
- `/collections.json` **does** list a collection with handle **`x4-classic`**.
- `/collections/x4-classic/products.json` returns **four products, none of them a
  device**:

| Product | Price | Note |
|---|---|---|
| eReader Magnetic Reading Light | $9.99 / $15.99 | generic, cross-model |
| eReader Adhesive Metal Ring | $4.99 / $7.99 | generic |
| Magnetic Charging Adapter for X3 & X4 Pro | $5.99 | **named for other models** |
| Magnetic Pogo Pin Charging Cable for X3 & X4 Pro | $4.99 | **named for other models** |

**A collection with no device and no device-specific accessories is a provisioned
SKU, not a product line.** Compare the neighbouring collections, which each carry
their device plus model-specific cases and protectors:

| Collection | Device present? | Model-specific accessories |
|---|---|---|
| `x3-series` | ✅ $69.00 | 6 |
| `x4-pro-series` | ✅ $99.00 | 6 |
| `x4-series` | ❌ (delisted) | 4, **all sold out** |
| **`x4-classic`** | ❌ **never present** | **0** |

The `x4-series` and `x4-classic` collections fail in **different ways**: the X4 is
an end-of-life signature (device gone, its accessories exhausted), while the X4C
is a **pre-launch signature** (nothing was ever there).

## A weak, suggestive inference about the charging connector

The two charging accessories in the `x4-classic` collection are both **magnetic
pogo** parts *"for X3 & X4 Pro"*. That is **not** evidence the X4C uses pogo
charging — they are the only charging accessories Xteink sells, and they appear in
several collections. But it is the only signal that exists, and the question
matters to a buyer.

**Recorded as unresolved**, and flagged in
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) as a first-order unknown.

## Channels searched

| Channel | Result |
|---|---|
| `xteink.com` | Collection exists, device does not |
| Reddit (2,136 posts) | **No purchase report, no price, no listing link** |
| GitHub (~200 repos) | No X4C project of any kind |
| AliExpress / Amazon / Xianyu | **Not searched directly** — a declared exclusion, so this negative is weak |

Note that the family *is* sold through several third-party channels — owners
report buying an X3 from **Amazon.ca**, an X3 from **Xianyu** (Chinese eBay) and
an X4 from **AliExpress**
([r/XTEINK `1vkuhbi`](https://old.reddit.com/r/XTEINK/comments/1vkuhbi/), 2026-08-10,
firsthand). So a Chinese-marketplace listing for the X4C is plausible and simply
was not looked for.

## Family price context, 2026-09-04

| Device | Price |
|---|---|
| [X3](../x3/market-and-pricing.md) | **$69.00**, in stock |
| [X4](../x4/market-and-pricing.md) | **delisted**; was ~$69 |
| [X4 Pro](../x4-pro/market-and-pricing.md) | **$99.00**, in stock |
| **X4 Classic** | **never priced** |
| [S4](../s4/README.md) | ¥299 / ¥339 ≈ US$47 (China, 2026-04) |

If the X4C ever launches internationally, the plausible slot is **between the X3
and the X4 Pro** — S3 and PSRAM like the Pro, but no touchscreen and no
frontlight, which are the Pro's two most expensive components. **That is
reasoning, not evidence.**

## The one dated commercial observation that exists

A vendor Shopify collection named `x4-classic`, containing zero devices, on
**2026-09-04**. Everything else on this page is an absence.

---

# Round 2 — dated pricing, 2026-09-11

**No line above was altered.** Everything above was written when this device had
no price at all.

## Vendor-direct, read from the store API

All figures `USD`, item-only, worldwide shipping from Shenzhen, retrieved
**2026-09-11** from `https://xteink.com/products.json?limit=250`.

| SKU | Variant | Price | `compare_at_price` | In stock | Grams |
|---|---|---:|---:|---|---:|
| `X4Classic-gray` | Mist Gray | **79.00** | 89.00 | yes | 250 |
| `X4Classic-black` | Space Black | **79.00** | 89.00 | yes | 250 |
| `X4CW+BW` | Mist Gray + Mist Gray base | 95.00 | 105.00 | yes | 250 |
| `X4CB+BW` | Space Black + Mist Gray base | 95.00 | 105.00 | yes | 250 |
| `X4CW+BB` | Mist Gray + Space Black base | 95.00 | 105.00 | yes | 250 |
| `X4CB+BB` | Space Black + Space Black base | 95.00 | 105.00 | yes | 250 |

`compare_at_price` is a Shopify "was" field. It is **not evidence of a former
selling price** — the product was published at 79.00 and has never been listed
at 89.00. Treat it as a marketing anchor.

`grams: 250` is the **shipping weight**, not the device mass. The vendor's own
spec block says the device is **68 g**.

## Accessories, published 2026-09-06

| SKU family | Item | Price |
|---|---|---:|
| `X4C-Tempered-{1,2,3}` | Tempered glass, 1/2/3-pack | 4.99 / 7.99 / 9.99 |
| `X4C-Matte-{2,4,6}` | Matte PET, 2/4/6-pack | 3.99 / 5.99 / 8.39 |
| `X4C-ProtectiveC-{MW,MG}` | Hard polycarbonate case, **14 g** | 3.99 |
| `X4C-MagneticC-{FG,MG,BP,RR,SB,CG}` | Magnetic case, six colours | 8.99 |
| `Batterybase-sage` | `XTEINK Base Stand & Charging Adapter for X3, x4 Classic and X4 Pro`, published 2026-09-04 | 19.99 — **out of stock at retrieval** |
| `XTC2P-1` | Magnetic charging adapter (shared X3 / X4C / X4 Pro) | 5.99 |
| `x3cable-1` | Magnetic pogo-pin cable (shared) | 4.99 |

**The shared-accessory renaming is itself evidence.** Two accessories that on
2026-09-04 were titled *"for X3 & X4 Pro"* now read *"for X3, x4 Classic and X4
Pro"*. The X4 Classic uses the **same pogo interface** as the X3 and the X4 Pro.

## Community-reported prices — other regions, other channels

**Not normalised.** Each row states its own region, date and basis.

| Price | Region | Date | Basis | Source |
|---|---|---|---|---|
| **€89** X4C, **€110** X4 Pro | EU | 2026-09-07 | storefront, seen by the buyer | [r/XTEINK `1w9jzpn`](https://old.reddit.com/r/XTEINK/comments/1w9jzpn/) post body, firsthand |
| *"earlier batches… closer to €40"* (X4) | EU | pre-2026-09 | **hearsay** | same post |
| **£47.70 ≈ €58** for an X4 | UK | *"last minute"*, pre-launch | **firsthand purchase** | u/wowsomuchempty, 11 pts |
| *"the original X4 at around €60"* | EU | pre-2026-09 | recollection | u/ShrubbyFire1729, 24 pts |
| *"about 30 % more than original X4"* | — | 2026-09-10 | derived by the commenter | u/chicco1973, 40 pts |

The US$79 store price and the €89 EU price are **not a contradiction**; they were
not reconciled for VAT, and no EU storefront page was retrieved. **Do not quote a
single price for this device without a region and a date.**

## What replaced what

| | X4 (replaced) | X4 Classic |
|---|---|---|
| Store status 2026-09-11 | **withdrawn**; product record gone; **all four dedicated accessories gone** | listed, in stock |
| Last observed list price | ~$69 | **$79** |
| Observed street/used | as low as **$16** used (2026-08-18), £47.70 new (UK, pre-launch) | none — 5 days old |

**The withdrawal is complete.** On 2026-09-04 the X4's four accessories were
still in the catalogue (all sold out); on 2026-09-11 the product records
themselves are gone and the `x4-series` collection contains only a reading light
and a metal ring — items that fit any device in the family.

## The pricing controversy, stated neutrally

The launch-week price threads are dominated by one argument: that the X4 Classic
costs meaningfully more than the X4 it replaces while adding nothing the
community asked for (a frontlight) and removing something it valued (USB-C).
Counting only figures with a firsthand basis: an X4 was bought in the UK for
**£47.70** shortly before launch; the X4 Classic lists at **US$79 / €89**.

Against that: the X4 Classic is a **different and substantially more capable
board** — ESP32-S3 with 8 MB PSRAM against an ESP32-C3 with none, native SDMMC
against SPI shared with the display, a real RTC and an I²C fuel gauge against
none and a bare ADC, an IMU, six interrupt-driven keys against an ADC ladder, and
a published 920 mAh cell. **Both statements are true.** The disagreement is about
whether that is what buyers of a $69 reader wanted.

## Availability risk

One logistics report worth recording:
[r/XTEINK `1wdbmkb`](https://old.reddit.com/r/XTEINK/comments/1wdbmkb/),
2026-09-11 — *"Why would X4 Classic shipment be rejected by airline and sent back
to xteink?"*. A single firsthand report, almost certainly lithium-battery air
freight, **not** a pattern. Recorded because it is the only shipping datum that
exists for this SKU.

---

## Cross-reference added by the round-2 index merge, 2026-09-11

The round-2 pricing work above was produced by the Xteink session. The
certification/market session independently enumerated the same catalogue on the same date and
agrees: **25 products, X4 Classic published 2026-09-06, USD 79.00 bare / USD 95.00 with base.**
Two sessions, one endpoint, one date, identical figures. Nothing above is changed by this note.

Two items from that session that are **not** already stated above:

- **The store title is `XTEINK X4 Classic (X4 V2)`.** The vendor is asserting that the Classic
  *is* the second version of the X4 — which is the strongest single piece of evidence for the
  replacement relationship argued in *What replaced what*.
- **Six catalogue line-items are services, not products** (handling fees, shipping fee,
  after-sale charges). Exclude them from any price range: a naive "cheapest item in the store"
  read returns **USD 1.00**.

Regulatory record for this device, new on 2026-09-11:
[`certification-and-compliance.md`](certification-and-compliance.md) — FCC `2BTR9-X4C`, granted
**2026-07-20**, seven weeks before the store listing. The grant date is an independent
corroboration of the launch timeline that does not depend on the vendor's own store.
