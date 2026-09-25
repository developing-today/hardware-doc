# CrossPoint / FreeInk research captures — ARCHIVED

**Archived to** `archive/software/ecosystems/crosspoint-freeink/research-captures/`
**Date:** 2026-09-20 · **42 files · 1 399 800 B (1.33 MiB)**

Non-repository evidence gathered **2026-09-01 / 2026-09-02** alongside the ten upstream clones:
GitHub API captures, fork listings, search transcripts, and partial file extracts pulled
*before* the clones were taken. The archive is machine-local; reacquisition notes are below.

## What is held

| Archived path | Files | Bytes | Contents |
|---|---:|---:|---|
| `research-captures/raw/` | 14 | 407 194 | 8 GitHub REST API repository captures; CrossPlay's README across 4 branches; a 289 KB commit log |
| `research-captures/forks/` | 2 | 761 613 | `cpr_forks.ndjson`, `crossink_forks.ndjson` — behind [`fork-network.md`](fork-network.md) |
| `research-captures/search/` | 2 | 15 295 | GitHub code and name search transcripts |
| `research-captures/partial-extracts/` | 22 | 214 748 | Pre-clone single-file pulls from `cpr`, `crossplay`, `crosspoint`, `fisdk` |
| `research-captures/repos-meta/` | 2 | 952 | `crossplay-head.json`, `crossplay-repo.json` |
| `research-captures/SCRATCH-README-eink-software-2026-09-20.md` | 1 | 17 280 | The subject's original working record, moved verbatim |

## ⚠ One capture is the only surviving record of a deleted repository

`raw/api_ideo2004-afk_crosspoint-reader-lua.json` (6 503 B) holds the GitHub API response for
`ideo2004-afk/crosspoint-reader-lua`, captured 2026-09-01. That URL returned **HTTP 404** on
2026-09-20 and **no Wayback capture exists**. Star count, fork flag, parent, timestamps and
description for that repository exist in this file and nowhere else this project can reach.
Reacquisition: **`lost`**. See
[its placeholder](../../applications/crosspoint-reader/source-snapshots/ideo2004-afk_crosspoint-reader-lua.ARCHIVED.md).

## The extracts are mostly redundant — and the redundancy is proven, not assumed

Re-verified by SHA-256 on 2026-09-20:

| Pair | Result |
|---|---|
| `partial-extracts/fisdk/README.md` vs the `freeink-sdk` clone's | **identical** — `2d09e99bf7adf2e5…` |
| `partial-extracts/crosspoint/platformio.ini` vs `partial-extracts/cpr/platformio.ini` | **identical** — `d747688075bfd0ef…` |
| `partial-extracts/cpr/platformio.ini` vs the `crosspoint-reader` clone's | **differ** — clone is `0b40bd40ad0b3a5e…` |

That last row is why `cpr/` earns its place: it holds the **pristine** upstream `platformio.ini`,
whereas the clone's copy is dirty with the +70 lines of the native-simulator build experiment
described in [`crosspoint-simulator-build-notes.md`](../../tooling/crosspoint-simulator-build-notes.md).
Without it there is no clean baseline to diff the experiment against.

`ma-r-s/crossplay` was **never cloned**, so `partial-extracts/crossplay/` (8 files, including a
43 621 B `USER_GUIDE.md`) is the only local copy of that project's files. Its risk profile is
unassessed. Supports [`applications/crossplay/README.md`](../../applications/crossplay/README.md).

`raw/crossplay-README-main.md` is **14 bytes** — CrossPlay's `main` is effectively an empty
branch, which is itself the finding; `develop` and `master` are byte-identical at 11 916 B each.

## Two empty directories were removed, having held nothing

`scratch/eink-software/freeink/` and `scratch/eink-software/web/` were created and never used:
**0 files, 0 bytes**, tree digest
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (SHA-256 of the empty string)
for both. Recorded so their absence is not later read as a gap.

## Reacquisition

**None of this is a versioned document.** These are point-in-time observations whose value is
that they are dated. Cite 2026-09-01/02, never the current API.

| Set | Status | Command / note |
|---|---|---|
| `raw/api_*.json` (7 of 8) | `manual` | `GET https://api.github.com/repos/<owner>/<name>` returns *today's* values |
| `raw/api_ideo2004-afk_*.json` | **`lost`** | Repository 404s, no Wayback capture |
| `forks/*.ndjson` | `manual` | `gh api --paginate repos/<owner>/<name>/forks` — fork lists change |
| `search/*` | `manual` | Search results are not reproducible |
| `partial-extracts/{cpr,crosspoint,fisdk}` | `automatic` | Fetch at the recorded clone HEADs |
| `partial-extracts/crossplay` | `manual` | Never cloned; no SHA pinned for these files |

## Related archives

| Contents | Placeholder |
|---|---|
| CrossPoint, its forks, the old `community-sdk` | [`…/crosspoint-reader/source-snapshots/README.md`](../../applications/crosspoint-reader/source-snapshots/README.md) |
| The FreeInk SDK | [`…/freeink-sdk/source-snapshots.ARCHIVED.md`](../../frameworks/freeink-sdk/source-snapshots.ARCHIVED.md) |
| Independent FreeInk consumers | [`source-snapshots.ARCHIVED.md`](source-snapshots.ARCHIVED.md) |
| The simulator | [`…/tooling/source-snapshots.ARCHIVED.md`](../../tooling/source-snapshots.ARCHIVED.md) |
| The plugin ecosystem (18 repos, archived 2026-09-11) | [`…/plugins/source-snapshots.ARCHIVED.md`](../../applications/crosspoint-reader/plugins/source-snapshots.ARCHIVED.md) |
