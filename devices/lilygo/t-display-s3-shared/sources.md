# T-Display-S3 family — sources

Family-scoped sources only. Per-board sources are in each board's own record; the fullest is
[`../t-display-s3/sources.md`](../t-display-s3/sources.md). All retrieved **2026-09-07**.

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| F-1 | `Xinyuan-LilyGO` organisation repository listing, 254 repos | GitHub API | primary | repository | `gh api orgs/Xinyuan-LilyGO/repos?per_page=100` | 2026-09-07 | live | **the family enumeration**, star/fork/issue counts, default branches, licences, push dates | a snapshot; the org changes weekly | [`artifacts/originals/xinyuan-lilygo-org-repos-2026-09-07.tsv`](artifacts/originals/xinyuan-lilygo-org-repos-2026-09-07.tsv) |
| F-2 | LilyGO Shopify product feed, 214 products | LILYGO | primary | store listing | https://lilygo.cc/collections/all/products.json | 2026-09-07 | feed `updated_at` 2026-09-07 | every SKU, price, stock state and `published_at` launch date in the family; **the V1.0/V2.0 concurrency finding** | prices exclude shipping and tax; needs a browser User-Agent | `scratch/lilygo-t-display-s3/shop-products.jsonl` |
| F-3 | `LilyGo-Display-IDF` → `main/product_pins.h` | LILYGO | primary | repository | https://github.com/Xinyuan-LilyGO/LilyGo-Display-IDF/blob/b1a1cc54994bf1b417e3bb30c437bbe1036bff7f/main/product_pins.h | 2026-09-07 | commit 2025-11-03 | **nine boards' pin maps in one file**, behind `CONFIG_LILYGO_*` switches | ESP-IDF only; does not cover the 1.43/1.64/1.75 boards | [`artifacts/originals/LilyGo-Display-IDF-product_pins.h`](artifacts/originals/LilyGo-Display-IDF-product_pins.h) |
| F-4 | `LilyGo-AMOLED-Series` README.MD | LILYGO | primary | repository | https://github.com/Xinyuan-LilyGO/LilyGo-AMOLED-Series/blob/6d1dc008b94578cc34ba4a0f3b223dd808ca963f/README.MD | 2026-09-07 | commit 2026-05-06 | the four AMOLED boards, resolutions, luminance, **the only published current-consumption table in the family**, the T4-S3 GPIO18 warning, library dependencies with versions | vendor prose | scratch |
| F-5 | `T-Display-S3` README.md | LILYGO | primary | repository | https://github.com/Xinyuan-LilyGO/T-Display-S3/blob/ec889e789b3cf093412689a143f7f37b42b56af7/README.md | 2026-09-07 | commit 2026-08-31 | the `USB CDC On Boot` FAQ, the Arduino-core 2.0.14 pin, the GPIO15 requirement | — | scratch |
| F-6 | `esphome/components/mipi_spi/models/{lilygo,amoled}.py` | ESPHome | primary (third-party) | repository | https://github.com/esphome/esphome/tree/dev/esphome/components/mipi_spi/models | 2026-09-07 | branch `dev` | **independent** pin, offset, colour-order and init-sequence data for six boards in the family | **cited by branch, not commit** — the one such citation in this pass | scratch |
| F-7 | Eight LilyGO board schematics | LILYGO | primary | schematic | per-board repositories at the commits in each record | 2026-09-07 | title-block dates 2024-04-29 … 2024-07-19 | the designator/part census that underpins every chip identity claimed here | **net connectivity was not traced for any of them** | per-board `artifacts/schematic/` |
| F-8 | Six issue trackers, 550 issues | LILYGO + community | community | issue | per repository | 2026-09-07 | 2022-06 … 2026-08 | the gotcha corpus, and the open-issue counts in [`product-history-and-family.md`](product-history-and-family.md) | selection biased toward high-engagement threads | `scratch/lilygo-t-display-s3/issues/` |
| F-9 | `old.reddit.com/search.json`, 4 queries | Reddit | community | forum | https://old.reddit.com/search.json | 2026-09-07 | 2023-05 … 2026-08 | 27 family-relevant posts; two read in full | needs a link-preview User-Agent; `www.reddit.com` returns 403 | `scratch/lilygo-t-display-s3/reddit.txt` |
| F-10 | Chip datasheets mirrored inside LilyGO board repos | various makers, mirrored by LILYGO | credible mirror | datasheet | per-repo `datasheet/` and `information/` | 2026-09-07 | various | the identities of ST7789V, RM67162, RM690B0, SH8501B, SH8601Z, CO5300, AXS15231, CST328, CST3530, FT3168, SY6970, ST7796S, MSM261S4030H0R | **all filed under their component records, not here** | `components/**/artifacts/` |

## Family-scoped sources sought and not found

| Sought | Result |
|---|---|
| A LilyGO changelog, revision register or ECN process | **none exists.** The nearest thing is a `//!` comment in the Pro's `utilities.h` |
| A LilyGO documentation portal | none. Everything is GitHub + Shopify |
| Published PCB revision numbers | only for the AMOLED 1.91″ (V1.0/V2.0, in store variant titles) and the Pro (V1.0/V1.1, in a source comment) |
| Schematics for the 1.43/1.64/1.75″ AMOLED boards | **none published.** The only boards in the family without one |
| A licence for `T-Display-S3-Long` and `T-Display-S3-Pro` | **none declared** |
| Any current-consumption figure for the base T-Display-S3 | none |
