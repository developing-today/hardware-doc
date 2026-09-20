# T-Display K230 — example search log

**Date: 2026-09-04.** Scope, queries and dispositions for the example survey.

## Scope

"Examples" for this board means something different from an ESP32 board. There is **no library,
no `examples/` directory and no set of sketches** — the board's software is a single Buildroot
system image with one large LVGL application. The useful unit of study is therefore an
**application module inside the launcher**, a **build script**, or a **companion-MCU firmware
project**, not a standalone sketch.

## Queries

| # | Service | Query / method | Results | Disposition |
|---|---|---|---|---|
| 1 | GitHub | `search/repositories?q=org:Xinyuan-LilyGO+K230` | 4 | all cataloged |
| 2 | GitHub | Full org listing (254 repos), filtered `k230\|k256\|canmv\|kendryte` | 4 | same 4; no others |
| 3 | GitHub tree | `T-Display-K230` @ `bb831ab…` recursive, 624 blobs | ~50 launcher modules | cataloged by function |
| 4 | GitHub tree | `T-Display-K230-nRF52840` @ `4646a72…`, 32 blobs | 1 firmware project + tools | cataloged |
| 5 | GitHub tree | `T-Display-K230-nRF9151` @ `ed4ecbe…`, 40 blobs | 2 firmware profiles | cataloged |
| 6 | GitHub | `kendryte/k230_docs` tree | ~15 demo/tutorial documents | cataloged as chip-level, not board-level |
| 7 | GitHub | `oreboot/oreboot`, `intx82/k230-debian`, `kendryte/canmv_k230`, `sipeed/MaixPy` | 4 | cataloged; **none has a board profile** |
| 8 | Reddit | 3 searches + 4 thread fetches | 1 announced project (Meshtastic UI), 1 tool (`kendryte_boot`) | cataloged, no repository located |
| 9 | CNX-Software | site search `K230` | 5, **none about this board** | rejected — wrong product |

## Explicitly not done

- **`T-Display-K230_canmv_rt` was not cloned.** 745 MB, 25★, created 2025-03-05, last push
  2026-08-03. **This is the largest known gap in the example survey** and should be the first
  thing a follow-up session examines.
- No example was **built**. No Ubuntu host and no XuanTie toolchain were available. Zero
  build-tested examples, stated plainly.
- Chinese-language project sites were not searched.
- GitHub issue and discussion threads on the four LilyGO repositories were not read.

## Stopping criterion

Passes 1 and 2 converged on the same four repositories; pass 3–5 enumerated their contents
exhaustively at pinned commits. A third broad pass produced only duplicates.
