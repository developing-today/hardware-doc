# ARCHIVED: dated vendor product catalogues, 2026-09-11

> Moved out of `scratch/`, **not deleted**. Archived **2026-09-20**; every operation was `mv`.

## Identity

| Field | Value |
|---|---|
| Original path | `scratch/market-and-certification/shopify/` |
| Archived to | `archive/guides/markets/artifacts/vendor-product-catalogues-2026-09-11/` |
| Size | **11,051,031 bytes** (10.5 MiB) |
| File count | **6** |
| Tree digest | `3b092fdc53abdae70fd71b155f5ac8b7f923ea7ddb02d43682145648ef296b54` |
| Captured | **2026-09-11** |

Raw Shopify `/products.json` dumps plus the `extract.py` that read them:

| File | Vendor | Products |
|---|---|---:|
| `shop.m5stack.com-products-p1..p3.json` | M5Stack | 664 |
| `www.lilygo.cc-products-p1.json` | LilyGO | 214 |
| `xteink.com-products-p1.json` | Xteink | 25 |

Directory index: [`archive/guides/markets/artifacts/README.md`](../../archive/guides/markets/artifacts/README.md).

## Why these were kept rather than treated as regenerable

**`/products.json` has no historical endpoint.** It returns the catalogue *as of the request*. The
prices, `updated_at` timestamps, variant lists, stock flags — and the products that were listed on
2026-09-11 and are not listed now — exist only in these six files.

They are the evidence behind:

- the **X4 Classic launch at USD 79** and the **X4's withdrawal** from the Xteink catalogue;
- the store title `(X4 V2)` on the X4 Classic listing;
- the observation that six Xteink line-items are **services, not products**;
- the dated 2026-09-11 rows in four `market-and-pricing.md` records.

## ⚠ The scope limit on every price this supports

No marketplace, clone or used-market observation was obtainable from the host that ran this pass:

| Attempted | Result |
|---|---|
| AliExpress, eBay, `m5stack.aliexpress.com` | bot wall or 403 |
| Amazon search | HTTP 200 with **zero prices in the HTML** — a JS shell. A 200 is not a success |
| Taobao, JD search | HTTP 200, SPA shell, 2.7–34 KB |

So pricing sourced from here is **official-store pricing only**. As of 2026-09-20, marketplace,
clone and used-market pricing for these devices is not sourced from anywhere — see
[`device-comparison-matrix.md`](device-comparison-matrix.md) and
[`clones-and-variants.md`](clones-and-variants.md), neither of which claims otherwise.

## Note on the date

The session was briefed that the date was 2026-09-07. It was not. The host clock, the `date:`
headers from `shop.m5stack.com` and `fccid.io`, and the `updated_at` on every live M5Stack product
all agreed on **2026-09-11**, and that is the date carried on every observation. The reasoning is
preserved in the certification half of the same pass.

## The rest of that working directory

The FCC half — filing pages, `harvest.py`, the user-agent matrix, the control run — is at
`archive/guides/research/artifacts/certification-and-market-2026-09-11/`, with its own
[`ARCHIVED-artifacts.md`](../research/ARCHIVED-artifacts.md). This is the only subject that was
split, and the split is by what the files describe: vendor catalogues here, research technique
there.

## How to get it back

```bash
mv "archive/guides/markets/artifacts/vendor-product-catalogues-2026-09-11" \
   "scratch/market-and-certification/shopify"
```

Re-fetching is one command per vendor and **gives a different answer**:

```bash
curl -fsSL 'https://shop.m5stack.com/products.json?limit=250&page=1'
curl -fsSL 'https://www.lilygo.cc/products.json?limit=250&page=1'
curl -fsSL 'https://xteink.com/products.json?limit=250&page=1'
```

There is no way to retrieve the 2026-09-11 state. If these files are lost, the dated observations
in the records become unverifiable — which is why they are the one part of that pass that was not
consolidated away.
