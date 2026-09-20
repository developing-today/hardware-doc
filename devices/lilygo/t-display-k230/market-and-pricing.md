# T-Display K230 — market and pricing

Every observation is dated, sourced and tied to an exact configuration. **All prices below come
from LilyGO's own Shopify JSON endpoints on 2026-09-04**, which return integer cents per variant
and therefore carry no currency-formatting ambiguity.

## Current pricing — 2026-09-04, lilygo.cc, USD, worldwide storefront

| Product | SKU | Configuration | Price | In stock |
|---|---|---|---:|---|
| T-Display K230 | `K256` | bare board, SX1262 **868 MHz** | **$98.79** | yes |
| T-Display K230 | `K256-A` | bare board, SX1262 **915 MHz** | **$98.79** | yes |
| T-Display K230 | `K256-B` | bare board, SX1262 **923 MHz** | **$98.79** | yes |
| T-Display K230 | `K256-C` | bare board, SX1262 **433 MHz** | **$98.79** | yes |
| T-Display K230 Kit | `K256-03` | **Main Unit**, SX1262 868 MHz | **$150.31** | yes |
| T-Display K230 Kit | `K277` | **Main Unit**, **LR2021** 830–940 MHz | **$153.01** | yes |
| T-Display K230 Kit | `K256-04` | **Keyboard only**, **with nRF9151** | **$113.25** | yes |
| T-Display K230 Kit | `K256-04-A` | **Keyboard only**, **without nRF9151** | **$70.94** | yes |

**Shipping, tax and duty are not included and were not observed.** Currency is USD as returned by
the store; no conversion was performed, so no conversion date applies.

### The derived numbers that matter

| Question | Answer | Working |
|---|---|---|
| Cheapest way into a K230 | **$98.79** | bare board, any band |
| Complete keyboard handheld, no cellular | **$221.25** | `K256-03` $150.31 + `K256-04-A` $70.94 |
| Complete keyboard handheld **with cellular** | **$263.56** | `K256-03` + `K256-04` |
| Complete handheld with **LR2021** + cellular | **$266.26** | `K277` $153.01 + `K256-04` |
| Price of the **nRF9151 cellular option** | **$42.31** | `K256-04` − `K256-04-A` |
| Price of the **LR2021 upgrade** | **$2.70** | `K277` − `K256-03` |
| Main Unit premium over bare board | **$51.52** | `K256-03` − `K256` |

**Two of these deserve emphasis.**

The **$2.70 LR2021 upgrade** buys Meshtastic voice and photo transfer, which LilyGO states is
impossible on SX1262 units. That is an unusually cheap capability jump and there is no obvious
reason to choose `K256-03` over `K277`.

The **$51.52 Main Unit premium** is not explained anywhere in the listing. The bare board and the
"Main Unit" both carry an SX1262 at 868 MHz. The difference is presumably the case, the battery
compartment, or the base-board interface — LilyGO's shipping-list graphic was not machine-readable
and the difference remains **unexplained**. Do not assume the two are the same hardware.

## Launch pricing

| Date | Product | Price | Source |
|---|---|---|---|
| 2025-03-21 | T-Display K230, bare board | **not recorded** | Product created and published this date; the store returns only *current* prices, and no archived listing was retrieved |
| 2026-08-20 | T-Display K230 Kit | **not recorded** separately | Published 2026-08-20; the 2026-09-04 prices are 15 days old at most, so they are effectively launch prices for the kit |

**Launch price for the bare board is a genuine gap.** An Internet Archive capture of
`https://lilygo.cc/products/t-display-k230` from March 2025 would settle it; not attempted here.

## Comparative price points, dated

| Board | SoC | RAM | Display | Price | Date | Source |
|---|---|---|---|---:|---|---|
| **BPI-CanMV-K230D-Zero** | K230**D** | 128 MB (SiP) | none | **$29** | 2024-11-18 | CNX-Software launch coverage |
| **CanMV-K230** | K230 | 512 MB | none | not established | 2023-10 | Repeatedly out of stock; see below |
| **T-Display K230** | K230 | **1 GB** | 4.1″ AMOLED | **$98.79** | 2026-09-04 | lilygo.cc |
| **T-Display K230 Kit**, full | K230 | 1 GB | + keyboard + cellular | **$263.56** | 2026-09-04 | lilygo.cc |

The K230D Zero at $29 is the reference point for "what a K230 costs as a component". The LilyGO
board's $98.79 buys **8× the RAM**, an AMOLED, a camera, LoRa, Ethernet and a 40-pin header on top
of that. Viewed that way the pricing is reasonable; viewed as a handheld against a $30 Meshtastic
node, it is not.

## Availability

| Date | Observation | Evidence |
|---|---|---|
| 2025-03-26 | "**Already sold out…** any chance to get it back in stock?" — five days after launch | firsthand, r/LilyGO |
| 2025-03-27 | LilyGO: "Don't worry, sales will resume soon" | vendor |
| 2025-07-04 | "T-Display K230 and T-Lora Pager **have some stock available**" | vendor post, r/LilyGO |
| 2026-09-04 | **All eight variants show available** in the Shopify JSON | primary |
| 2024-05-08 | "Where do people buy CANMV K230 from?" — the reference board was hard to source | r/RISCV |

K230 hardware has a persistent history of being hard to buy. As of the research date, the LilyGO
board is not — every SKU is in stock.

## Marketplaces, used market, clones — negative results

- **AliExpress, Amazon, Tindie, Taobao: not searched in this pass.** Deliberate; see
  [`research-log.md`](research-log.md). Third-party listings for LilyGO products are common and
  often carry different prices, so this is a real gap, recorded rather than glossed.
- **Used market: no observations.** The product is too new — the kit is 15 days old.
- **Clones: none found.** No clone or compatible listing was located in any search performed.
- **Regional variants:** LilyGO uses region-suffixed SKUs elsewhere (`…DE`, `…US`) but **none
  exists for the K230 SKUs** — the four bare-board variants differ only by LoRa band.

## Cost-of-ownership notes

Things not in the sticker price:

- **A microSD card** is mandatory — it is the boot medium and the system disk.
- **A 21700 cell** is not confirmed included in any SKU. One early buyer received no battery.
- **A USB Bluetooth dongle** if you need Bluetooth (community estimate: ~$20).
- **A case** for the main board is not included with the keyboard, confirmed 2026-08-13.
- **A build host** — Ubuntu or Docker. No prebuilt image is published.

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
| T-Display K230 | 2025-03-21 | 915Mhz [K256-A] | `K256-A` | **USD 98.79** | ✅ yes |
| T-Display K230 | 2025-03-21 | 868Mhz [K256] | `K256` | **USD 98.79** | ✅ yes |
| T-Display K230 | 2025-03-21 | 433Mhz [K256-C] | `K256-C` | **USD 98.79** | ✅ yes |
| T-Display K230 | 2025-03-21 | 923 Mhz [K256-B] | `K256-B` | **USD 98.79** | ✅ yes |
| T-Display K230 Kit | 2026-08-20 | Main Unit / SX1262/ 868MHz | `K256-03` | **USD 150.31** | ✅ yes |
| T-Display K230 Kit | 2026-08-20 | Main Unit / LR2021/ 830–940MHz | `K277` | **USD 153.01** | ✅ yes |
| T-Display K230 Kit | 2026-08-20 | Keyboard Only / With nRF9151 | `K256-04` | **USD 113.25** | ✅ yes |
| T-Display K230 Kit | 2026-08-20 | Keyboard Only / Without nRF9151 | `K256-04-A` | **USD 70.94** | ❌ no |

Citation form required by [`guides/markets/vendor-comparison.md`](../../../guides/markets/vendor-comparison.md) § *A note on prices*, for the first row:

> *USD 98.79, 1 unit, retrieved 2026-09-11, `https://www.lilygo.cc/products/t-display-k230`, ships from Shenzhen, CN*

### Normalisation and caveats

⚠ **Bare board and kit must not be merged.** Board USD 98.79 flat across all four radio frequencies (433/868/915/923 MHz) — **frequency choice carries no price difference**. The **Kit** is a separate handle at USD 150.31 (SX1262) / USD 153.01 (LR2021), plus a keyboard-only option at USD 113.25 with nRF9151 or USD 70.94 without.

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

