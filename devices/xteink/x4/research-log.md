# Xteink X4 — research log

The **family-wide** log — source classes, query ledger, Reddit and GitHub search
depth, dead links and the stopping criterion — is at
[`../x4-pro/research-log.md`](../x4-pro/research-log.md) and covers all six
Xteink products. This page records only what was **X4-specific**, plus the
second sweep performed after the first pass.

## X4-specific queries and outcomes

| Query / target | Depth | Outcome |
|---|---|---|
| `xteink x4` (GitHub repos) | 2 pages, 198 total | Most of the ~200-repo census names this device |
| `abhishek-nerella/XTEINK-OEM-BIN-` repo + tree | full | **Found and retrieved a 16 MB factory dump** — the only Xteink firmware image obtained |
| `zocs/eink-quick-flasher` tree + `firmware/README.md` | full | Stock versions **V5.1.6 (EN)** and **V5.2.13 (CN)**; the `.bin` files are **Git LFS pointers** and were **not** fetched |
| `xteink teardown`, `xteink teardown chip` | 100 results each | **No X4 teardown exists.** Both teardowns found are X3 |
| `/collections/x4-series/products.json` | full | **Device absent; all 4 accessory SKUs sold out** → delisted |
| Wayback CDX for the delisted X4 product page | 1 attempt | **Timed out at 60 s, 0 bytes. Not retried.** Still unrecovered |

## Second sweep — 2026-09-04, after the first pass

The first pass covered the three dedicated subreddits. A second sweep added
**topic subreddits** and **Chinese-language terms**, and materially changed the
record.

| Added | Queries | New posts |
|---|---|---|
| `r/{eink,ereader,esp32,ebookreaders,Kindle,koreader}` with `restrict_sr=1` | 6 | — |
| `xteink nfc`, `xteink ppi`, `xteink x4 pro review`, `xteink x4 classic`, `xteink s4 specs`, `xteink schematic`, `xteink fcc` | 7 | — |
| **`阅星瞳`**, **`星瞳 电纸书`** | 2 | — |
| **Total** | 15 | **+338 → 2,136 unique posts** |

### What the second sweep found that the first missed

| Finding | Why it was missed first time |
|---|---|
| **The earliest X4 evidence is a 2025-06-18 Chinese group buy at €30, 74 g, 5.9 mm** | It is in r/ereader, not a dedicated sub, and predates the brand's English presence |
| **A fifth product: the "Nano" / Tong Card (瞳卡)** | Discussed in r/xteinkHax and r/microreaders only |
| **A sixth subreddit, r/microreaders** | Not in the first sub census |
| **The X3's NFC purpose — resolved** | Required a GitHub *discussion*, not a repository |
| **An "X4 version 2" confirmed by the vendor for Sept 2026** | Posted 2026-08-25, in the vendor-run sub |
| **Xteink devices carry no external CE/FCC marking** | A low-scoring (4 pt) thread that only a targeted `fcc` query surfaced |
| **Amazon.ca / Amazon / Xianyu / AliExpress are real channels, with unpredictable USB-lock state** | Buried in a comment thread about back-casing variants |
| **One of the three subreddits is vendor-operated** | Stated in a comment on a post that had been *removed from that sub* |

**Method note worth keeping:** searching a product's *dedicated* subreddits finds
the enthusiast core and misses the origin story, the adjacent products and the
regulatory reality. The `restrict_sr=1` sweep across topic subreddits cost 6
requests and changed several conclusions.

## Targeted thread retrievals (with comments)

Eight threads were fetched with full comment trees, not just listings —
`old.reddit.com/<permalink>.json?limit=200`, UA `WhatsApp/2.23.20.0`, all 200:

`cefcc` · `tongcard` · `nano` · `x4v2` · `x3newer` · `nfc` · `compare` ·
`starpupil`.

**Comments carried most of the value.** The regulatory finding, the channel/lock
correlation, the vendor-operated-subreddit statement and the NFC use cases were
all in comment bodies, invisible in the listing JSON.

## GitHub discussions — a source class the first pass missed entirely

`gh api graphql` against
`crosspoint-reader/crosspoint-reader` **discussion #2259** returned the
authoritative statement on the X3's NFC tag. **Repository search does not index
discussions**; they must be queried through GraphQL. Recorded as a reusable
technique.

## Dead / failed for this device

| Target | Outcome |
|---|---|
| Wayback CDX, `xteink.com*` | **Timed out, 0 bytes.** The delisted X4 product page and its imagery remain unrecovered |
| `x4_en_v5.1.6_ota.bin`, `x4_cn_v5.2.13_ota.bin` | **Git LFS pointers, not fetched.** Needs an LFS-aware client — cheap to close |
| X4 SPIFFS contents (3.4 MB) | **Not extracted** from the dump |
| `gotaserver.xteink.com/api/check-update` | **Not queried** |
| Any X4 teardown | **Does not exist** |

## Stopping criterion

Two consecutive passes returned only duplicates for X4 *hardware* facts. The
remaining sources are: a teardown (nobody has done one), an LFS fetch (cheap,
deferred), a SPIFFS extraction (cheap, deferred), and Chinese marketplaces
(declared exclusion).

**Reproducible broad-coverage snapshot dated 2026-09-04.** Not proof that no other
resource exists.
