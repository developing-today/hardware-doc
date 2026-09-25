# `research/passes/` — reports on passes over this repository

Promoted out of `scratch/` on **2026-09-20**, because the records in this repository depend on
them. Thirty-three files under `devices/`, `components/` and the repository root cite
`corrections-requiring-review.md` as the authority for a dated correction, and the root
[`README.md`](../../README.md) *Research passes* table links the merge reports. A repository
record cannot depend on a path in `scratch/`, and it cannot depend on one in `archive/` either —
the archive is machine-local and a cloner never has it.

| Directory | Pass | Date | What it records |
|---|---|---|---|
| [`index-merge/`](index-merge/README.md) | Index merge, rounds one and two | 2026-09-07, 2026-09-11 | Applying ten sessions' parked index fragments to the shared indexes; the 174-exhibit artifact split; what was deferred and why |
| [`cross-cutting-synthesis-2026-09-07/`](cross-cutting-synthesis-2026-09-07/README.md) | Cross-cutting synthesis | 2026-09-07 | Four authored guides derived entirely from existing records, with no network retrieval — and the negative results found while writing them |

## What these are for

Seven, then three, parallel research sessions each added records but were **forbidden from editing
shared index files**, so each parked ready-to-paste Markdown in its own scratch directory. The
merge passes applied those fragments. That is bookkeeping — but three things in it are not:

**The corrections.** When two sessions' text lands in one record, contradictions become visible
that neither session could see. `index-merge/corrections-requiring-review.md` and
`corrections-adjudicated.md` hold those: a TP4057 charge-current conflict, a RadioLib licence
error repeated in four places, an unidentified part that turned out to have a record already. They
are **flagged, not adjudicated** — the merge passes researched nothing and verified no technical
claim, and said so.

**The deferrals.** `deferred.md` and `deferred-round2.md` record what was *not* applied and why —
protected files, live sessions, out-of-scope targets. Without them, unapplied fragments look like
oversights.

**The method failures.** Round two found that the prescribed deletion check,
`git diff -- <file> | grep -c '^-[^-]'`, **cannot see a deleted Markdown bullet**: a removed
`- [foo](bar)` appears as `-- [foo](bar)`, which `^-[^-]` excludes by construction. Use
`git diff --numstat` instead. That is a reusable correction to the repository's own working
conventions, and it would have been lost with the directory.

## Evidence boundary

Both passes state it explicitly, and it is worth repeating here: **neither researched anything.**
Every fact they moved into an index is an originating session's, transcribed. What they verified
is mechanical — that every path they linked exists, that their diffs contain no deletions, that
every placeholder carries a hash and two URLs, and that the git index was untouched.

The bulky working evidence for index-merge round two — 314 files of pre-edit snapshots, schematic
renders and FCC label zooms — is in the archive at
`archive/research/passes/index-merge/round-two-workdir-2026-09-11/`.
