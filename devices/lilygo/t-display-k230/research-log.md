# T-Display K230 — research log

**Session date: 2026-09-04.** Single pass, no hardware. Every query, its depth, and its outcome.

## Declared scope and exclusions

- **Searched:** LilyGO store (Shopify HTML + `.js` endpoints), LilyGO wiki, GitHub (org listing,
  repository metadata, full recursive trees, code search), Canaan `kendryte/k230_docs`,
  CNX-Software site search, Reddit via `old.reddit.com/search.json` and per-thread JSON.
- **Not searched, and why:** AliExpress, Amazon, Tindie and Taobao — deliberately deferred; all
  three are heavily bot-protected and the vendor's own store gives authoritative dated prices,
  which is what the pricing record needs. Chinese-language sources (Bilibili, Zhihu) were
  **queried only through GitHub and CNX-Software**, not directly; recorded as a gap. YouTube: one
  LilyGO-linked video was identified by URL but not watched.
- **Depth:** every search below was taken to the end of its first result page; Reddit searches
  used `limit=25`–`50` and `t=all`, and returned fewer results than the limit in every case, so
  the result sets are complete rather than truncated.

## Product identification

| # | Service | Query | Result |
|---|---|---|---|
| 1 | lilygo.cc | `/search?q=K230&type=product` | **3 products.** `t-display-k230`, `t-display-k230-kit`, `t-embed-cc1101`. The third is the SKU collision (`K230` = T-Embed CC1101 transparent). **Established the marketed name in one query.** |
| 2 | lilygo.cc | `/products/t-display-k230.js` | Full variant/SKU/price/date record |
| 3 | lilygo.cc | `/products/t-display-k230-kit.js` | Same for the kit; **the description HTML is the fullest published BOM** |
| 4 | GitHub | `search/repositories?q=org:Xinyuan-LilyGO+K230` | 4 repositories |
| 5 | GitHub | `orgs/Xinyuan-LilyGO/repos?per_page=100 --paginate`, filtered for `k230\|k256\|riscv\|canmv\|kendryte\|deck` | **254 repositories** enumerated; confirmed the 4 K230 repos and separately identified T-Deck/T-Deck-Pro/T-Deck-MAX as a *different* family |
| 6 | wiki.lilygo.cc | `/products/t-display-series/t-display-k230/` | Product page; sidebar revealed **`cased-version.html`** and `quick-start.html` |
| 7 | wiki.lilygo.cc | guessed `/t-display-k230-cased-version/` | **404** — wrong shape. Correct path is `/t-display-k230/cased-version.html`. Recorded so the next agent does not repeat it. |
| 8 | wiki.lilygo.cc | `/t-display-series/t-display-keyboard/` | **Different product** — an ESP32 T-Display in a keyboard shell. A name trap; nothing to do with K230. |

**Candidate names tested and refuted:** `T-Deck K230`, `T-K230`, `T-Deck Pro K230`,
`K230 Cardputer`. None returns a LilyGO product. The store search for `K230` returns three
products and none is named any of those.

## Chip documentation

| # | Service | Query | Result |
|---|---|---|---|
| 9 | GitHub | `repos/kendryte/k230_docs/git/trees/main?recursive=1` | **837 entries**, not truncated. The single highest-yield call of the session. |
| 10 | raw.githubusercontent | 6 targeted `en/` document fetches | All 200 |
| 11 | GitHub code search | `repo:kendryte/k230_docs "C908"` | 11 files; led to `en/K230_brief_datasheet.md`, which was **not** in the first directory listing pass because it sits at the tree root, not under `00_hardware/` |
| 12 | local grep | `ethernet\|gmac\|rmii` across both datasheets | **Zero matches** — the negative result that resolves the RJ45 question |
| 13 | local grep | `third core\|small core\|little core\|big core\|C908\|security\|OTP\|boot` | Confirmed exactly two CPU subsystems |
| 14 | tree listing | `zh/00_hardware` filter | **22 binary EDA artifacts the `en/` tree does not have.** Recorded in the vendor guide as the vendor's most important trap. |
| 15 | tree listing | search for `K230_PINOUT` | **Not present.** Cited by the datasheet, never published. |
| 16 | tree listing | search for errata | **None published.** |

## BSP source mining

| # | Method | Result |
|---|---|---|
| 17 | `git clone --depth 1` × 3 | 172 MB + 9.9 MB + 9.8 MB; commits `bb831ab…`, `4646a72…`, `ed4ecbe…` |
| 18 | Read `HARDWARE_PINMAP.md` | Complete pin/bus/address map — the backbone of this record |
| 19 | Regex sweep for ~30 part-number families across `*.c/cpp/h/md/MD/sh/patch/dts/mk/in/defconfig` | Ranked hit counts: `lr2021` 579, `k230` 532, `nrf9151` 203, `nrf52840` 168, `sx1262` 151, `rm69a10` 124, `tca8418` 72, `bq25896` 59, `bq27220` 57, `aht20` 54, `gc2093` 44, `xl9555` 42, `lt9611` 29, `max98357a` 25, `gt9895` 19, `rtl8723ds` 16, `rtl8189fs` 6, `csr8510` 4. **Zero hits for any Espressif identifier** — the evidence behind `GC-2`. **Zero hits for any PMIC family** — U1. |
| 20 | Grep `ui_hardware.c` for the key map | Full TCA8418 code→label table and 6×11 display layout extracted |
| 21 | Read `linux.fragment` and the defconfig | Toolchain path/flags, kernel repo+commit, driver choices, built-in test tools |
| 22 | Grep for `NET_ETH_IFACE` | `eth0`; and `USB_RTL8152` is **absent** from the fragment |
| 23 | Read `k230_canmv_v3.dts` | IO bank voltage warning; 512 MB memory node (`GC-7`) |

## Community

| # | Service | Query | Results | Note |
|---|---|---|---|---|
| 24 | `old.reddit.com/search.json` (UA `WhatsApp/2.23.20.0`) | `"T-Display K230"` | 6 | **200 OK.** `www.reddit.com` returns 403 to the same request; the documented UA fallback worked exactly as the repository's `ai-crawler-site-access-table.md` says |
| 25 | same | `lilygo k230` | 6 | Revealed **r/LilyGO exists** and is active |
| 26 | same | `kendryte k230` | 8 | Mostly r/RISCV, 2023–2025 |
| 27 | per-thread `.json?limit=100` × 4 | `1vtcjuj`, `1ltxxxo`, `1v8kedv`, `1jgb4kn` | full comment trees | Source of every anecdote in [`community.md`](community.md), including the two most consequential — the brick and the oreboot recovery lead |
| 28 | cnx-software.com | `/?s=K230` | 5 | **None is about this board.** Negative result. |

**Not found despite looking:** any Hackaday article; any independent review; any teardown; any
PCB photograph; any benchmark; any clone listing.

## Method notes worth reusing

- **`gh api` rather than anonymous `curl` for GitHub.** One recursive tree call on `k230_docs`
  returns 837 entries and can exhaust the 60/hour anonymous limit; the resulting 403 is
  indistinguishable from a bot block except by `X-RateLimit-Remaining`.
- **Shopify's `/products/<handle>.js`** gives `created_at`, `published_at`, per-variant SKU and
  integer-cent prices that the rendered page never shows. This is how the launch dates in
  [`product-history-and-family.md`](product-history-and-family.md) were established.
- **`old.reddit.com/search.json` with `User-Agent: WhatsApp/2.23.20.0`** returned 200 on every
  call. No other UA rotation was needed anywhere in this session; `lilygo.cc`,
  `wiki.lilygo.cc`, `raw.githubusercontent.com` and `cnx-software.com` all served a plain request.
- **Grep the vendor tree for part-number *families*, not for parts you expect.** The zero-hit
  results (Espressif, PMIC) were more informative than most of the positive ones.

## Stopping criterion

Two consecutive broad passes produced only duplicates. Remaining unknowns
([`gaps-and-conflicts.md`](gaps-and-conflicts.md)) require **physical hardware, a PCB photograph,
or a schematic LilyGO has not published** — not more searching. This is a reproducible
broad-coverage snapshot dated 2026-09-04, not a claim that nothing else exists.
