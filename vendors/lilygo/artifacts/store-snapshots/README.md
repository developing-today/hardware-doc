# LilyGO shop snapshot — 2026-09-07

Dated capture of the LilyGO Shopify storefront feed. **Primary evidence** for pricing,
availability, SKU and variant claims across the entire LilyGO device family in this repository.

> **Promoted out of `archive/devices/lilygo/t-display-s3-shared/artifacts/` on 2026-09-20.** These were the only local
> copy of the evidence behind the family's `market-and-pricing.md` pages. The feed **changes
> daily** and has no public history, so a dated snapshot cannot be re-created — which is exactly
> why it is kept in the repository rather than archived.

| File | Bytes | SHA-256 | What |
|---|---:|---|---|
| [`lilygo-shop-products-2026-09-07.jsonl`](lilygo-shop-products-2026-09-07.jsonl) | 2,503,053 | `ad5644747d27890b…` | The raw feed — **214 products**, 6 JSON lines (one per `?page=`). Each product carries `id`, `title`, `handle`, `body_html`, `published_at`, `created_at`, `updated_at`, `tags`, and every variant with its SKU, price and availability |
| [`lilygo-shop-variants-2026-09-07.txt`](lilygo-shop-variants-2026-09-07.txt) | 9,137 | `—` | Derived per-SKU price/stock table for the T-Display-S3 family, flattened out of the feed |

## Retrieval date

**2026-09-07**, machine-verified. The task brief for that session said 2026-09-04; the host clock
and the feed's own `updated_at: 2026-09-07` both disagreed with it, and the verified date is used
here and in every citing record.

**Never take a retrieval date from a task brief or a directory name.** Take it from the data.

## Why the raw feed and not just the extracted numbers

The prose in `body_html` is marketing copy of low reliability, but the **structured** fields are
platform-generated and therefore evidential:

- `published_at` dates a product's appearance, which is the only hard evidence available for
  LilyGO launch timing — the vendor publishes no press releases.
- Per-variant `available` distinguishes "discontinued" from "temporarily out of stock", which
  the rendered page does not.
- Variant SKUs disambiguate the family's many near-identically-named boards far better than
  titles do.

Keeping the raw feed means a future question ("when did the AMOLED 1.64 appear?", "was the Pro
ever cheaper?") can be answered without a new fetch that would return today's data.

## Reacquisition

`automatic`, but **it will not reproduce these bytes** — that is the point of the snapshot.

```bash
D=$(date +%F)
for p in 1 2 3 4 5 6; do
  curl -s "https://lilygo.cc/products.json?limit=250&page=$p"
done > "lilygo-shop-products-$D.jsonl"
```

Take the retrieval date from the response's `updated_at` values, not from the shell.

## Licence and disposition

| Field | Value |
|---|---|
| Licence | **unknown** — public storefront API output, no terms stated |
| Redistribution status | `unknown` |
| Disposition | **`repository`** — 2.5 MB, primary, and not re-obtainable |
| Retrieved | 2026-09-07 |

## Cited by

The `market-and-pricing.md` of the LilyGO device records, notably
[`devices/lilygo/t-display-s3/market-and-pricing.md`](../../../../devices/lilygo/t-display-s3/market-and-pricing.md),
and [`vendors/lilygo/README.md`](../../README.md).
