# Example search log — Xteink X4 Classic

Date **2026-09-11**. Carrying forward the 2026-09-04 sweep's repository census
(~200 Xteink-relevant repos) and adding targeted queries for the X4C.

| # | Service | Exact query | Depth | Useful | Notes |
|---|---|---|---|---|---|
| 1 | GitHub code search | `"XteinkX4Classic"` | all 8 | 5 | `crosspoint-reader` ×2 (+simulator, +lockscreens fork), `freeink-sdk` ×2, `crosspoint-simulator`, `Inkkit`, `esphome-xteink` |
| 2 | GitHub code search | `xteink "X4 Classic"` | first 15 of 47 | 4 | surfaced **`clackups/draftling`** — the only project with hand-written X4C files |
| 3 | GitHub code search | `"X4 V2" xteink` | all 11 | 1 | 9 of 11 hits are inside `clackups/draftling` |
| 4 | GitHub code search | `"X4R2_CLA" xteink` | all 5 | 2 | surfaced **`kycube/x4pro-emu`** |
| 5 | GitHub code search | `"X4R1_CLA"` | — | **0 results** | **a negative result, and the useful one** |
| 6 | GitHub repo metadata | `repos/{clackups/draftling,kycube/x4pro-emu,vjFaLk/esphome-xteink,mohitagw15856/Inkkit}` | — | 4 | dates, licences, stars |
| 7 | GitHub commits API | `repos/Free-Ink/freeink-sdk/commits?path=…/BoardConfig.h&since=2026-09-01` | all | 2 | `3fe3936d`, `39606d5a` |
| 8 | old.reddit | 11 searches, 12 comment trees | 100/query | many | see [`../research-log.md`](../research-log.md) §1.6 |

## Rejections and why

| Candidate | Reason |
|---|---|
| `vjFaLk/esphome-xteink` | vendored verbatim copy of `freeink-sdk`; deduplicated to E01 |
| `mohitagw15856/Inkkit` | copied `BoardConfig.h`; deduplicated to E01 |
| `t0nyz0/crosspoint-reader-lockscreens` | fork of `crosspoint-reader`, lineage preserved, no X4C-specific content |
| `crosspoint-reader/crosspoint-simulator` | host simulator; carries the board enum but exercises no hardware |
| `AsukaLay/xteink_pdf`, `SamLinBIT/xteink-toolkit` | host-side file converters; no board code |

## Not searched

- **Gitee, Codeberg, GitLab** — the Chinese-hosted mirrors of this ecosystem were
  not searched. Given the vendor is China-first, this is a real gap.
- **Package registries** (PlatformIO Registry, Arduino Library Manager) — no
  X4C-specific library is expected, and none was looked for.
- **Bilibili / YouTube** — video examples not surveyed.

## Stopping criterion

Stopped after query 8 returned only repositories already in the catalogue.
**Two consecutive passes produced no new qualifying candidate.**

## Honest limitation

**Nothing in `catalog.json` was built.** No toolchain was installed, no PlatformIO
environment was resolved, and no dependency set was pinned by this repository.
`best.md` is therefore a *reading* recommendation, not a tested one.
