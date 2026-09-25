# Verification — LilyGO T-Display K230 / Canaan Kendryte K230

**Date: 2026-09-04.** Single research pass, **no hardware in hand**. Nothing was staged or
committed. No shared index file was edited.

## 1. Scope of what was created

| Path | Files |
|---|---:|
| `devices/lilygo/t-display-k230/` | 42 (README + 16 supporting docs + 17 feature guides + 3 example files + 2 acquisition files + artifact placeholders + 14 images + 1 media manifest) |
| `components/canaan/k230/` | 1 README + 10 artifact files |
| `components/{raydium,goodix,galaxycore,realtek×2,nordic-semiconductor×2,texas-instruments,semtech,analog-devices,asair,lontium,xlsemi,unidentified}/` | 15 component READMEs |
| `vendors/canaan/README.md` | 1 |
| `guides/nixos/riscv-and-vendor-sdk-toolchains.md` | 1 (**new file**; `guides/nixos/README.md` unmodified) |
| `archive/devices/lilygo/t-display-k230/artifacts/` | working files + `README.md`, `index-fragments.md`, `vendor-guide-additions.md` |

## 2. Checks run and results

| # | Check | Result |
|---|---|---|
| 1 | **Authored relative Markdown links resolve** | **398 links across 65 authored files. 0 broken.** |
| 2 | **Bundled upstream Markdown excluded from the link check** | Yes — the 7 Canaan documents contain **80** upstream-relative image links that do not resolve locally. Excluded deliberately; stated in [`components/canaan/k230/artifacts/README.md`](components/canaan/k230/artifacts/README.md). Rewriting them would break byte-identity with the pinned commit. |
| 3 | `index-fragments.md` links | ~30 unresolved **by design** — they are relative to each snippet's *destination*, not to the scratch file. Annotated in the file itself. |
| 4 | **SHA-256 of retained chip documents** | `sha256sum -c SHA256SUMS` → **7 / 7 OK** |
| 5 | **SHA-256 + byte size of every retained image** | **14 / 14 match** the manifest |
| 6 | **File type validated from magic bytes, not extension** | All 14 images start `FF D8 FF` (JPEG). `file(1)` is absent on this host; the magic was checked directly. |
| 7 | **Duplicate-hash detection** | **0 duplicate groups** across all new artifacts and media |
| 8 | **JSON schema validity** | `media/manifest.json`, `examples/catalog.json`, `acquisition/manifest.json` all parse |
| 9 | **Filenames portable ASCII** | Yes, no exceptions |
| 10 | **Failed downloads not retained under misleading extensions** | Two 404 responses saved as `.html`; correct. Recorded in `archive/devices/lilygo/t-display-k230/artifacts/research-scratch/README.md`. |
| 11 | **Bidirectional device ↔ component links** | Every component record cited by the device has a **Used By** entry naming the device; every component in the key-spec table links out. Four `Used By` rows for **pre-existing** records were **not applied** (see §4) and are parked in `index-fragments.md`. |
| 12 | **Every URL has a retrieval date** | Yes — all `2026-09-04` unless a document date is given |
| 13 | **Every source row has class + medium + date** | Yes, `sources.md` |
| 14 | **Artifact provenance complete** | Yes; unknown values written as unknown with a reason (e.g. firmware SHA-256 "enumerated from the tree API, not downloaded") |
| 15 | **Redistribution status + disposition on every artifact** | Yes; 19 acquisition records |
| 16 | **Downloader verify-only mode** | ⚠ **Not implemented.** `acquisition/README.md` gives ordered clean-clone commands and a verification recipe, but no committed downloader script exists. Recorded as a gap rather than claimed. |
| 17 | **`local-cache` paths ignored and absent from the index** | N/A — no `local-cache` artifacts were created |
| 18 | **Coverage: every fitted capability appears with a task link** | 32 capabilities in `coverage.md`; 16 feature guides; every one reachable from the README's *Common tasks* index |
| 19 | **Vendor driver audited against datasheets** | **Partially.** Audited: the TCA8418 register usage, the PMU power-key flow, the Goodix driver *choice*, the LVGL and Serial-LTE-Modem patch sets. **Not audited: `vvcam/src/gc2093.c`** — no GalaxyCore datasheet is public, so there was nothing to decode against. Recorded as `GC-6`, not skipped silently. |
| 20 | **No component record built from a candidate or near-miss** | Confirmed. Every part number was read from LilyGO's pin map, product listing, or a source-tree census. The `K230` ↔ T-Embed CC1101 SKU collision and the `RC01812` string were both flagged rather than promoted. |
| 21 | **Refuted hypotheses recorded with evidence and date** | Yes — nine negative results in `gaps-and-conflicts.md`, plus refuted candidate names (`T-Deck K230`, `T-K230`, `T-Deck Pro K230`, `K230 Cardputer`) and the Bruce-firmware association |
| 22 | **PDF text-layer validation** | N/A — no PDF was retrieved. All chip documentation is upstream Markdown. |
| 23 | **Tree digests record their recipe** | N/A — no tree digest was taken |
| 24 | **Prevalence claims backed by a stated sample** | Yes — "four firsthand-ownership reports across 26 comments in the two largest threads, six threads total" |
| 25 | **Launch vs current pricing kept separate** | Yes; launch price for the bare board is explicitly recorded as **not established** |
| 26 | **Repository status** | Only intended paths changed (§1). No shared index touched. |

## 3. Evidence honesty

**Zero commands were executed against hardware. Zero examples were built. Zero measurements were
taken.** The highest evidence class anywhere in this pass is `reported-working`. This is stated at
the top of `development.md`, `factory-firmware.md`, `performance.md`, `coverage.md`,
`compatibility-and-status.md` and every feature guide, and `coverage.md` carries an explicit
"build-tested: 0 / hardware-tested: 0" row.

## 4. Shared files deliberately not edited

Per this session's constraints, and confirmed with `find <file> -mmin -30`:

| File | Why not edited |
|---|---|
| `components/semtech/sx1262/README.md` | modified within 30 min — another session active |
| `components/texas-instruments/tca8418/README.md` | same |
| `components/texas-instruments/bq27220/README.md` | same |
| `components/espressif/esp32-s3r8/README.md` | same **and** the claim is unverified (`GC-2`) — no Used-By added on purpose |
| `components/generic/micro-sd-sdmmc/README.md` | quiet, but batched with the others for a single reviewed paste |
| `README.md`, `devices/README.md`, `components/README.md`, `vendors/README.md`, `software/README.md`, `artifact-manifest.md`, `guides/markets/*`, `devices/m5stack/**`, `guides/nixos/README.md` | out of scope for this session |
| `vendors/lilygo/README.md` | **did not exist**; a sibling session documenting T-Display-S3 may own it. Findings parked in `archive/devices/lilygo/t-display-k230/artifacts/research-scratch/vendor-guide-additions.md`. |

All additions for these are ready to paste in
[`archive/devices/lilygo/t-display-k230/artifacts/research-scratch/index-fragments.md`](archive/devices/lilygo/t-display-k230/artifacts/research-scratch/index-fragments.md).

## 5. Open gaps

Nine tracked conflicts (`GC-1`…`GC-9`) and six unidentified parts (`U1`…`U6`). The three that
would resolve the most:

1. **A PCB photograph** — settles `GC-2` (ESP32-S3), `GC-4` (LT9611), `GC-9` (16 MB flash) and
   four of the six unidentified parts at once.
2. **One session with hardware** — `commands.md` §5 lists the exact commands; most of `GC-1`,
   `GC-3`, `GC-7`, `GC-8` fall in an afternoon, and it would produce the **first published
   performance data for this board**.
3. **`Xinyuan-LilyGO/T-Display-K230_canmv_rt`** — 745 MB, 25 stars, unexamined. The largest
   unexplored artifact.

## 6. Decisions needed from the user

| Item | Question |
|---|---|
| 7 Canaan documents (~256 KB) | Repository licence is BSD-2-Clause; the documents carry a conflicting "shall not disseminate" notice. **Stage, local-cache, or metadata-only?** Currently unstaged. |
| 14 product/wiki images (~3.0 MB) | No licence statement on either LilyGO host. **Stage or keep unstaged?** Currently unstaged. |
| LilyGO repositories and prebuilt firmware | No licence file on any of them. Currently `reference-only`, not downloaded. **Leave as-is?** |
| An acquisition downloader script | Not written. **Worth adding?** |
