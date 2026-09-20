# T-Display-S3 family — research log (family-scoped)

Snapshot **2026-09-07**. The detailed per-query ledger is in
[`../t-display-s3/research-log.md`](../t-display-s3/research-log.md); this page records only
what applies to the family as a whole.

## Date discrepancy

The task brief said 2026-09-04. The host clock said **2026-09-07 10:23 UTC**, and LilyGO's
product feed independently returned `updated_at: 2026-09-07`. Two independent sources against
one assertion, so **2026-09-07 is used throughout**. Subtract three days uniformly if the
brief was right; nothing depends on it.

## How the family was enumerated

The brief listed suspected members and asked for the list to be established from primary
evidence. Method:

1. **List every repository in `Xinyuan-LilyGO`** — 254, via the API, three pages.
2. **List every product in LilyGO's store** — 214, via the public Shopify product feed.
3. **Intersect.** A board is *confirmed* when it has both a repository and a store listing, or
   a repository containing a schematic that names it.
4. **Pin every confirmed repository to a commit** before reading anything from it.
5. **Read the vendor's own cross-board sources** — `LilyGo-AMOLED-Series/README.MD` §1 and
   `LilyGo-Display-IDF/main/product_pins.h` — which each enumerate several boards and are the
   strongest evidence of what LilyGO considers one family.

That produced **11 confirmed members**, three refutations and six out-of-family relatives.
Recorded in [`README.md` §1](README.md#1-the-confirmed-family-enumerated-from-primary-evidence).

## Refutations, with the evidence

| Hypothesis from the brief | Verdict | Evidence |
|---|---|---|
| "T-Display-S3 AMOLED Touch" is a separate board | **refuted** | LilyGO's resource table gives `T-Display-S3-AMOLED-Touch.pdf` as *the* schematic for both touch and non-touch 1.91″ SKUs, and the library README says it supports both from one build |
| "T-Display-S3 Cardputer-style" exists | **refuted** | No such repository or product. The keyboard handhelds are T-Deck / T-Deck-Pro / T-Deck-MAX / T-Display-keyboard |
| "AMOLED 2.41″" is a T-Display-S3 | **partially refuted** | The board exists and is in the same library; LilyGO sells and names it **T4-S3** |
| T-Deck is a T-Display-S3 relative | **out of family** | separate PCB, separate repo |

## Deliberate exclusions

- **Hardware.** None available; nothing is hardware-verified anywhere in this tree.
- **Net-level schematic tracing.** Blocked on poppler being absent from the host. This is the
  largest quality gap and the cheapest to close.
- **Marketplace pricing** (AliExpress, Amazon, Banggood, used). Only LilyGO's own store.
- **Regulatory records** (FCC, CE).
- **Chinese-language community sources** (Bilibili, Zhihu, CSDN) — though Chinese-language
  *datasheets* shipped in the repos were used.
- **YouTube, Hackaday, Discord.**
- **The 273 forks** of the base-board repository.

## Boards documented at less than device depth

Stated so nobody mistakes a stub for a finished record:

| Board | Depth | Principal missing item |
|---|---|---|
| T-Display-S3 | **full** | net-traced schematic |
| T-Display-S3 AMOLED | full-ish | `features/`, examples catalogue |
| T-Display-S3 Long | full-ish | `features/`, examples catalogue |
| T-Display-S3 Pro | full-ish | `features/`, examples catalogue |
| T-Display-S3 Touch | medium (by design — the base record covers the electronics) | — |
| AMOLED Plus, 1.64″, 1.43/1.75″, T4-S3, AMOLED Lite | **medium** | pin tables in some cases, `features/`, examples, acquisition manifests |
| Pro MVSRBoard | **stub** | everything except identity and artifacts |
| T-Display (TTGO), T-QT, T-Dongle-S3 | **lineage stubs** | everything except identity and relationship |

## Stopping criterion

Two consecutive broad passes over the org listing, the store feed, the issue trackers and
Reddit produced only duplicates of findings already recorded. Remaining sources need hardware,
a package manager, or marketplace sampling.
