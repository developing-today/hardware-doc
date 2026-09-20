# LilyGO — documentation-sourcing guide

**LilyGO** (Shenzhen Xin Yuan Electronic Technology Co., Ltd.; formerly and still partly
**TTGO**) publishes **no documentation portal, no wiki and no datasheet archive**. Everything is
in two places: **GitHub** and a **Shopify storefront**. That is unusual enough — and the
consequences are specific enough — to be worth writing down once.

First written **2026-09-07** during the
[T-Display-S3 family](../../devices/lilygo/t-display-s3-shared/README.md) pass.
Other agents: **append a section rather than rewriting.**

---

## 1. Where things actually are

| Document class | Where | Reliability |
|---|---|---|
| Schematics (PDF) | `github.com/Xinyuan-LilyGO/<board>/schematic/` | **good** — most boards have one |
| Chip datasheets (mirrored) | same repo, `datasheet/` or `information/` | **the only source for several parts.** Sitronix, Raydium, Hynitron, AXS, Chipone and Shenghe publish nothing openly |
| Pin maps | `examples/*/pin_config.h`, `pins_config.h` or `utilities.h` — **the name varies by board** | **good, and authoritative** |
| Cross-board pin maps | `Xinyuan-LilyGO/LilyGo-Display-IDF` → `main/product_pins.h` | **excellent** — nine boards in one file |
| Factory firmware | same repo, `firmware/`, plus `firmware/README.MD` | good |
| Mechanical (DWG/DXF/STP/STL/7z) | same repo, `dimensions/` | good |
| Board definitions | `boards/*.json` (PlatformIO) — path is sometimes `board/` singular | good |
| Prices, SKUs, launch dates, stock | `https://lilygo.cc/collections/all/products.json` | **excellent, and machine-readable** |
| Revision history, changelog, ECNs, BOMs, errata | **nowhere.** None exists for any board | — |

## 2. The store's product feed is the best market source there is

Shopify exposes a public JSON feed. One request replaces any amount of page scraping:

```bash
curl -sS -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
  'https://lilygo.cc/collections/all/products.json?limit=250&page=1'
```

It returns, per product: `title`, `handle`, **`published_at`** (the launch date — obtainable
nowhere else), `updated_at`, `product_type`, full-resolution image URLs, and per variant
`title`, `sku`, `price`, **`available`**. 214 products came back on 2026-09-07 in six pages.

**A plain request is served; a browser User-Agent is safer.** Recorded in
[`ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md).

**Traps in the feed:**

- **Variant titles carry hardware revisions.** `H619 "V1.0 Non-Soldered Pin"` and
  `H713 "V2.0 Non-Soldered Pin"` are two PCB revisions in one dropdown, both in stock. This is
  often the *only* place a revision is named.
- **Regional SKUs are the same board at a markup** (`H577` USD 9.54 vs `USH577` USD 14.04) and
  are frequently out of stock.
- **Duplicate product pages exist** — `t-display-s3` and `t-display-s3-copy` both list SKU
  `H569` one cent apart.
- **One product page can sell several different boards.** `t-display-s3-amoled-1-64` sells
  1.43″, 1.64″ and two 1.75″ variants with **different display and touch controllers**.

## 3. GitHub: authenticate, and never assume the branch

`api.github.com` limits **per identity**, so rotating User-Agents does nothing. Use the token —
60/h becomes 5 000/h:

```bash
gh api "orgs/Xinyuan-LilyGO/repos?per_page=100&page=1" \
  --jq '.[] | [.name,.default_branch,.pushed_at,.stargazers_count] | @tsv'
```

A 403 carrying `X-RateLimit-Remaining: 0` is the rate limit, **not** bot-blocking. Check that
header before rotating anything.

### ⚠ The default branch is often not `main`

This is LilyGO's most distinctive trap, and it will silently give you the wrong file.

| Repository | Default branch | What it encodes |
|---|---|---|
| `T-Display-S3-Long` | **`T-Display-S3-Long-cst3530`** | a **touch-controller revision** |
| `T-Display-S3-AMOLED-1.64` | **`arduino-esp32-libs_V2.0.14`** | a pinned Arduino core |
| `T-CameraPlus-S3`, `T-Circle-S3` | `arduino-esp32-libs_V2.0.14` | as above |
| `T-Encoder-Pro` | `arduino-esp32-libs_V3.0.7` | a *different* pinned core |
| `T5S3-4.7-e-paper-PRO` | `H752-01` | an SKU |
| `LilyGo-EPD47` | `esp32s3` | a target |

**Always read `.default_branch` from the API and resolve it to a commit SHA before fetching.**
Cite the SHA, never the branch — LilyGO force-pushes.

```bash
SHA=$(gh api repos/Xinyuan-LilyGO/T-Display-S3/commits/main --jq .sha)
gh api "repos/Xinyuan-LilyGO/T-Display-S3/git/trees/$SHA?recursive=1" \
  --jq '.tree[] | [.type,.size//0,.path] | @tsv'
```

One recursive tree call replaces hundreds of directory listings. Repo trees run 84–5 008
entries; the display repos are 60–300 MB and mostly image headers and vendored libraries, so
**fetch individual files from `raw.githubusercontent.com` rather than cloning** unless you need
the whole tree.

### Naming is inconsistent between repo and product

`T-Display-S3-AMOLED` is a repo *and* a product; but the S2 board's repo is
**`LilyGo-T-Display-S3`**-style (`LilyGo-T-Display-S2`), not `T-Display-S2`. `gh api
repos/Xinyuan-LilyGO/T-Display-S2` 404s. Search the org listing rather than guessing paths.

### Licences are inconsistent, and sometimes absent

| Repo | Licence |
|---|---|
| `T-Display-S3`, `T-Display-S3-AMOLED`, `LilyGo-AMOLED-Series`, `T-Dongle-S3`, `T-QT`, `LilyGo-Display-IDF` | MIT |
| `T-Display-S3-AMOLED-1.64`, `T-Display-S3-Pro-MVSRBoard`, `T-Display-S3-Pro-MVSRLora` | GPL-3.0 |
| **`T-Display-S3-Long`, `T-Display-S3-Pro`, `T-Touchbar-AMOLED`** | **none declared** |

Note that MIT is a *software* licence and LilyGO applies no hardware licence at all, so **the
redistribution status of a schematic PDF inside an MIT repository is unstated**, and inside an
unlicensed repository it is doubly unknown. Mirrored **chip** datasheets are third-party
copyright regardless of the repo licence, and several are marked CONFIDENTIAL — see §5.

## 4. Pin maps: three filenames, one job

| Filename | Boards |
|---|---|
| `pin_config.h` | T-Display-S3; the 1.43/1.75″ AMOLED (under `components/private_library/`) |
| `pins_config.h` | AMOLED 1.91″, Long |
| `utilities.h` | Pro |
| `main/product_pins.h` | **`LilyGo-Display-IDF` — nine boards in one file, behind `CONFIG_LILYGO_*`** |

**Read `product_pins.h` first.** It is the single best cross-board source in the catalogue and
several boards' pin maps are *only* correct there.

**Per-board headers contain copy-paste defects.** `T-Display-S3-Long`'s
`examples/factory/pins_config.h` @ `37a7e83` defines `PIN_BAT_VOLT 2` while also defining
`TP_RST 2`, and `PIN_BUTTON_2 21` while also defining `TFT_QSPI_D2 21` — both inherited from the
AMOLED board's header, where they are correct. **Cross-check any pin map against
`product_pins.h` and against the schematic before using it.**

## 5. Reading LilyGO's PDFs — two real traps

### 5.1 Altium exports hide the sheet in a Form XObject

Board schematics are Altium PDF exports. Reading `/Contents` alone returns only the
`PI…`/`CO…` pin-marker text and **none of the labels**. You must walk **every** content stream
in the file, including Form XObjects. Then group text by `BT…ET` block — reading `Tj`/`TJ`
operators individually shreds every label into single characters.

The repository's [`tools/altium_pdf_netlist.py`](../../tools/altium_pdf_netlist.py) and
[`altium_pdf_pin_table.py`](../../tools/altium_pdf_pin_table.py) do the real work but need
`pdftotext -bbox` XML, i.e. **poppler**. Without it you can recover a **designator and part-name
census** but **not net connectivity** — which is exactly the limitation stamped on every LilyGO
schematic claim in this repository as of 2026-09-07.

**One schematic is different.** `T4-S3-240719.pdf` uses **Type0/Identity-H subset fonts with
`/ToUnicode` CMaps**, where every other LilyGO sheet uses WinAnsi TrueType. An extractor that
works on the others returns **nothing** on it. You need a CMap decoder.

### 5.2 Chinese-vendor datasheets can have offset text layers

**Chipone's `CO5300_V0.01.pdf` has a uniform `+0x1D` code-point offset.** Extracted naively it
reads `&2||2/(' … &+,321(7HFKQRORJ\`; through its `/ToUnicode` CMap it reads
`FOD300 … FHHPONE TecOnology` — **human-legible and wrong**, the most dangerous failure mode
there is. Both decode consistently to *CO5300 … CHIPONE Technology (Beijing) Co., Ltd.*

Shenghe's `SH8501B0` and `SH8601Z` datasheets show the same pattern.

**Rule:** on any LilyGO-mirrored datasheet, run **two** independent extraction routes and
require them to agree, or validate against a rendered page, **before transcribing a single
value**. Nothing in this repository's LilyGO records transcribes a numeric value from an
unvalidated text layer.

## 6. Chip identities recovered from LilyGO mirrors

Several parts have **no public datasheet anywhere else**. Establishing who makes them is a
recurring win from mirrors:

| Part | Maker, established from the mirrored datasheet cover |
|---|---|
| **AXS15231(B)** | **AXS Technology Corp.** — with an explicit no-redistribution notice |
| **CO5300** | **Chipone Technology (Beijing) Co., Ltd.** |
| **SH8601Z**, **SH8501B** | **SHENGHE MICRO ELECTRONICS** — both marked CONFIDENTIAL |

That last one settles a naming question that predates this pass: this repository's
[`generic/sh8601-compatibility-driver`](../../components/generic/sh8601-compatibility-driver/README.md)
record could establish that `esp_lcd_sh8601` is a generic QSPI shim, but not who would make a
real SH8601. **Shenghe does**, and LilyGO fits one.

## 7. Where LilyGO's knowledge actually lives: closed GitHub issues

This is the most important practical observation in this guide.

LilyGO's maintainer (`lewisxhe`) answers issues quickly, accurately, and often **with
photographs of the PCB**. What does not happen is any of that reaching the README, a revision
number or a changelog. So:

- **The issue tracker is the documentation.** `T-Display-S3` has 318 issues, of which 1 is
  open; the answers are in the closed ones.
- **A stale-bot closes threads after 30 + 14 days.** "Closed as inactive" does not mean
  resolved, and several of the most valuable findings in this repository sit in such threads.
- **Search closed issues first**, before the README.

Examples of facts that exist *only* in an issue thread:
GPIO16/17 have fitted pull-ups on non-touch T-Display-S3 boards (with photographs,
[#313](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/313)); there is no battery
protection on the board ([#230](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/230),
2025-02-06); `VBUS` is deliberately not on the header and LilyGO's suggested fix is to solder a
wire ([#42](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/42)).

And one revision is documented **only in a `//!` source comment**:
`T-Display-S3-Pro/examples/factory/utilities.h` @ `08b8b2b` —
*"The difference between V1.0 and V1.1 is the backlight driver"* — with a 255-vs-16 brightness
scale behind an `#ifdef`.

## 8. Per-product checklist

Before declaring a LilyGO board researched:

1. Resolve the repo's **`.default_branch`**, then its **commit SHA**. Cite the SHA.
2. Pull the **recursive tree** and inventory `schematic/`, `datasheet/`, `information/`,
   `firmware/`, `dimensions/`, `boards/` or `board/`.
3. Read **`LilyGo-Display-IDF/main/product_pins.h`** for the board's `CONFIG_LILYGO_*` block,
   and cross-check it against the per-board `pin_config.h` / `pins_config.h` / `utilities.h`.
4. Pull the **store feed** and record `published_at`, every SKU, price and stock state — and
   check whether any **variant title names a hardware revision**.
5. Search the **issue tracker including closed issues**, sorted by comment count.
6. Grep the vendor's own source for `V1.0`, `V1.1`, `//!`, `#ifdef USING_`, and any
   `-DTOUCH_MODULES_*`-style build flag. **Revisions hide there.**
7. Check whether **ESPHome** carries a named model — `esphome/components/mipi_spi/models/` has
   pins, offsets, colour order and init sequences for several LilyGO boards, and it is an
   **independent** source against LilyGO's own.
8. Extract the schematic text **two ways** and require agreement before transcribing anything.
9. Record what LilyGO does **not** publish: BOM, revision history, errata, certification.

## 9. Products cross-referenced from this guide

- [T-Display-S3 family (11 boards)](../../devices/lilygo/t-display-s3-shared/README.md) —
  produced §§2–8 of this guide
- [T-Display K230 Kit](../../devices/lilygo/t-display-k230/README.md) — documented separately

---

## 10. Findings added by the T-Display K230 pass — 2026-09-04

Appended **2026-09-07** from [`scratch/lilygo-k230/vendor-guide-additions.md`](../../scratch/lilygo-k230/vendor-guide-additions.md).
That pass ran on 2026-09-04, when `vendors/lilygo/README.md` did **not yet exist**, and parked
its reusable sourcing findings in scratch rather than race the sibling T-Display-S3 session that
later wrote §§1–9. All observations below were live-verified **2026-09-04**. Where they overlap
§§1–9 they **corroborate independently** — they were written without sight of that text.

### 10.1 Hosts

| Host | Serves | Notes |
|---|---|---|
| `lilygo.cc` | Shopify storefront | The **authoritative source of SKUs and prices** |
| `wiki.lilygo.cc` | VitePress documentation site | Server-rendered — content **is** in the initial HTML, no JS execution needed |
| `github.com/Xinyuan-LilyGO` | Board repositories | **The best primary evidence LilyGO produces**, better than either of the above |
| `cdn.shopify.com/s/files/1/0617/7190/7253/files/<name>` | Product images | Stable direct URLs; `?v=<epoch>` is a cache buster and can be dropped |

### 10.2 Enumeration — the Shopify JSON endpoints

```sh
# Full structured product record: every variant, SKU, price in cents, availability,
# created_at / published_at, the complete description HTML, and every image URL
curl -s https://lilygo.cc/products/<handle>.js | python3 -m json.tool

# Search, returning handles
curl -s 'https://lilygo.cc/search?q=<term>&type=product'
```

`.js` gives you things the HTML page does not surface at all:

- `created_at` and `published_at` — **exact product launch dates**, e.g. T-Display K230 Kit
  `created 2026-08-06`, `published 2026-08-20`.
- Per-variant `sku` strings, which are LilyGO's internal stock codes.
- Prices as integer cents per variant, avoiding currency-formatting ambiguity.
- The full description HTML, which is where the specification table lives.

A `curl` with the default UA is enough; no User-Agent rotation was needed on any `lilygo.cc`
URL during this pass. `wiki.lilygo.cc` likewise returned 200 to a plain request, though a
browser UA was used throughout as a precaution.

### 10.3 ⚠ The SKU trap — LilyGO stock codes collide with chip names

**`K230` is a LilyGO SKU for the transparent-case variant of the T-Embed CC1101**, which is an
ESP32-S3 board with no Kendryte silicon in it whatsoever. Searching the store for `K230`
returns three products and one of them is that. Meanwhile the actual Kendryte K230 board's SKUs
are **`K256`, `K256-A`, `K256-B`, `K256-C`** (bare board, band variants) and **`K256-03`,
`K256-04`, `K256-04-A`, `K277`** (kit variants).

The general rule: **LilyGO stock codes are an opaque letter+number namespace that freely
collides with chip part numbers.** Never infer silicon from a SKU. Other observed forms include
region suffixes appended to the same base code — `K230DE` (Europe), `K230US` (United States),
`K230-ADE`, `K230-AUS` — which encode *warehouse*, not hardware.

### 10.4 ⚠ Wiki reliability — treat as marketing, verify against GitHub

The wiki is useful for orientation and for identifying part numbers that the shop listing omits,
but during this pass it produced three errors on one product page:

1. **Claimed an ESP32-S3-R8 co-processor** on the T-Display K230 for Wi-Fi/Bluetooth, complete
   with PlatformIO and Arduino instructions. The board's own BSP contains zero references to any
   Espressif part; its Wi-Fi is RTL8189FS over SDIO and its Bluetooth is a USB dongle.
2. **Inverted the K230's core roles** — "big core runs Linux, little core runs RT-Thread" —
   where Canaan's datasheet says CPU1 (1.6 GHz, big) runs the RTOS and CPU0 (800 MHz, little)
   runs Linux.
3. **Headings with no content.** The page has `#schematic` and `#dimension-diagram` headings and
   **no link or file under either**. This is a soft gap, not a 404, and it will not show up in
   any link check.

The corresponding GitHub repository (`Xinyuan-LilyGO/<Board-Name>`) was correct on every point
where the two disagreed. **Default to the repository.**

### 10.5 Repository conventions

- `README.MD` **and** `README_CN.MD` — uppercase `.MD` extension, both maintained. The Chinese
  file occasionally has content the English one lacks; diff them.
- `CHANGELOG.MD` / `CHANGELOG_CN.MD` with dated, semantic-versioned entries — this is the best
  available product timeline for firmware features.
- `.github/workflows/issues.yaml` and `.github/LilyGo_logo.png` in every repository — a reliable
  fingerprint for "this is an official LilyGO repository" versus a fork.
- Accessory silicon gets its **own repository**, named `<Board>-<Chip>`: `T-Display-K230-nRF52840`,
  `T-Display-K230-nRF9151`. If a board has a companion MCU, look for a sibling repository before
  concluding the firmware is unpublished.
- `bsp-patches/` inside the accessory repository duplicates the relevant patch from the main
  board repository, so the two can drift. Compare them.
- Default branches vary per repository (`main` vs `master`) even within one product family.
  Read `.default_branch` from the API. *(Independently corroborates §3.)*

### 10.6 Support channel

LilyGO staff answer publicly and quickly under the account **`u/LilyGoXinyuan`** on
**r/LilyGO**, typically within a day, and they link to the GitHub repository and wiki when
users report problems. Observed responses on 2025-03-25, 2025-03-27, 2026-07-28, 2026-08-21 and
2026-08-25. For a product this new, the subreddit is a better support channel than the wiki and
is frequently where a specification is first corrected.

### 10.7 Products that produced these findings

- [`devices/lilygo/t-display-k230`](../../devices/lilygo/t-display-k230/README.md)
- [`components/canaan/k230`](../../components/canaan/k230/README.md) — and its
  [Canaan vendor guide](../canaan/README.md)
