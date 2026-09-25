# CrossPoint core source snapshots

Snapshots of the **CrossPoint firmware family itself** — the reader, its old SDK, and its forks.
This is distinct from [`../plugins/source-snapshots/`](../plugins/source-snapshots.ARCHIVED.md),
which holds the 18 **plugin-ecosystem** repositories.

**Archived to** `archive/software/applications/crosspoint-reader/source-snapshots/`
**Clones moved 2026-09-20 · bundle archived 2026-09-11.**
The archive is machine-local and absent from a fresh clone; reacquisition is below.

> **Updated 2026-09-20.** This page previously said nine clones *"remain in
> `scratch/eink-software/repos/`"*. **That is no longer true** — the scratch subject was
> emptied and every clone was moved into the archive. Nothing was deleted. The four CrossPoint
> ones are listed below; the other six are [elsewhere in `software/`](#the-other-six-clones).

## Contents

| Snapshot | HEAD | Commits | Upstream 2026-09-20 | Form held |
|---|---|---:|---|---|
| [`ideo2004-afk_crosspoint-reader-lua`](ideo2004-afk_crosspoint-reader-lua.ARCHIVED.md) | `6bc3bcd92f9c8db991ac59a262df3ac00948bae1` | 784 | **404 — deleted, no Wayback capture** | **bundle + full checkout** |
| `crosspoint-reader_crosspoint-reader` | `e6139861a2a8c634aa18c333b7e214ee51a9965c` (`develop`) | 1 537 | live, 2 446 refs | full checkout, **dirty** |
| `uxjulia_CrossInk` | `cab4f24922f05811e7f44be1057f62ea2d978c52` (`main`) | 3 181 | live, 160 refs | full checkout, ⚠ **shallow** |
| `crosspoint-reader_community-sdk` | `198ad267219c25c8ab84418b806c66f1fb5216a3` (`main`) | 69 | live | full checkout |

All four are MIT. Cloned 2026-09-01/02. Total **1 473 986 386 B (1.37 GiB), 8 158 files**, plus
the 264 162 782 B bundle.

**Lineage** (from [`dependency-and-lineage.md`](../../../ecosystems/crosspoint-freeink/dependency-and-lineage.md)):
`CrossInk` and `crosspoint-reader-lua` are both forks of `crosspoint-reader`;
`community-sdk` is CrossPoint's own fork of the pre-FreeInk `open-x4-epaper/community-sdk`,
vestigial since the June-2026 migration.

## The one that cannot be reacquired

`ideo2004-afk/crosspoint-reader-lua` returned **HTTP 404** on 2026-09-20, **19 days** after it
was cloned as an unremarkable stale fork. No Wayback capture. Reacquisition is **`lost`**.

It is held in **two forms deliberately** — the `git bundle` (one file, one hash, all 59 refs,
complete 784-commit history) is the durable archival form; the full checkout additionally
preserves the dirty submodule state the bundle only reproduces approximately. The placeholder
[`ideo2004-afk_crosspoint-reader-lua.ARCHIVED.md`](ideo2004-afk_crosspoint-reader-lua.ARCHIVED.md)
stands alone: hash, size, ref count, restore command, and the fact that the fork's SDK pin
`a75faa88` is unrecoverable from anywhere.

## The other six clones

Taken in the same session, moved in the same pass, filed by what they are:

| Clones | Archive path | Placeholder |
|---|---|---|
| `Free-Ink_freeink-sdk` | `archive/software/frameworks/freeink-sdk/source-snapshots/` | [`…/freeink-sdk/source-snapshots.ARCHIVED.md`](../../../frameworks/freeink-sdk/source-snapshots.ARCHIVED.md) |
| `Free-Ink_freeink-reader`, `MagicCube_free-ink-on-paper-mono`, `mohitagw15856_Inkkit` | `archive/software/ecosystems/crosspoint-freeink/source-snapshots/` | [`…/crosspoint-freeink/source-snapshots.ARCHIVED.md`](../../../ecosystems/crosspoint-freeink/source-snapshots.ARCHIVED.md) |
| `crosspoint-reader_crosspoint-simulator` ×2 | `archive/software/tooling/source-snapshots/` | [`…/tooling/source-snapshots.ARCHIVED.md`](../../../tooling/source-snapshots.ARCHIVED.md) |

The supporting API captures, fork listings, search transcripts and pre-clone file extracts are at
`archive/software/ecosystems/crosspoint-freeink/research-captures/` —
[placeholder](../../../ecosystems/crosspoint-freeink/research-captures.ARCHIVED.md).

## Why the nine live clones were archived rather than left in scratch

The [archiving test](../../../../.agents/skills/hardware-device-research/SKILL.md#when-to-archive)
turns on *derivedness*, and by that test these clones are derived and reacquirable — which is why
an earlier pass left them in scratch. **That reasoning was sound but the storage tier was wrong.**
Scratch is *undecided* working space, and these were long since decided: mined, written up, and
not going to change. Material with a known home does not belong in a tier whose whole purpose is
to hold things that lack one.

They are now at their repo-relative archive paths, where the mapping needs no lookup table.
Reacquisition remains `automatic` for nine of ten regardless.

## Local modifications — do not "clean" them

`crosspoint-reader_crosspoint-reader` is **dirty**: `platformio.ini` carries +70 lines of the
native-simulator build experiment, and `sim-compat.h` is untracked. Both are fully captured in
[`software/tooling/crosspoint-simulator-build-notes.md`](../../../tooling/crosspoint-simulator-build-notes.md)
— `sim-compat.h` verbatim in §4, with the finding that
`-DCROSSPOINT_SIM_USE_NATIVE_DECODERS` **does not work** because of `#include_next` ordering.
The **pristine** `platformio.ini` is preserved at
`archive/software/ecosystems/crosspoint-freeink/research-captures/partial-extracts/cpr/platformio.ini`
(`d747688075bfd0ef…`, verified distinct from the clone's `0b40bd40ad0b3a5e…` on 2026-09-20).

**No clone has any local commit.** Ahead/behind against upstream was `0 0` for all ten at clone
time.

## Reacquisition

**`automatic`** for three of the four here:

```bash
git clone https://github.com/<owner>/<name>.git && git -C <name> checkout <HEAD above>
```

**`lost`** for `crosspoint-reader-lua` — restore from the bundle:

```bash
git clone archive/software/applications/crosspoint-reader/source-snapshots/ideo2004-afk_crosspoint-reader-lua.bundle crosspoint-reader-lua
cd crosspoint-reader-lua && git checkout crosspoint-flow
```

⚠ **`uxjulia_CrossInk` is shallow** — the archived copy does not carry the full graph. Re-clone
from upstream if you need history.

All SHAs, URLs, licences, star counts and LOC are in
[`repo-identity.json`](../../../ecosystems/crosspoint-freeink/repo-identity.json). Note its
`_meta` **overstates shallowness** (it claims `--depth 400` throughout); re-measured 2026-09-20,
only `CrossInk` and `crosspoint-simulator` are shallow. Trust the per-repo measurement.

## Convention

- One `<owner>_<repo>` stem per snapshot, matching the plugin snapshot directory's naming.
- Where a repository is **gone**, preserve history as a `git bundle` — one file, one hash, all
  refs, worktree reproducible — *in addition to* any checkout.
- Every archived entry has a `*.ARCHIVED.md` placeholder here or a directory-level README in the
  archive satisfying the
  [placeholder contract](../../../../.agents/skills/hardware-device-research/SKILL.md#placeholders-must-stand-alone):
  recoverable **without** the archive, or honestly marked `lost`.
- **Bundle personal and low-star repositories at clone time.** `git bundle create x.bundle --all`
  takes seconds. Nothing flagged `crosspoint-reader-lua` as at-risk, and
  `MagicCube/free-ink-on-paper-mono` and `mohitagw15856/Inkkit` carry the same profile today —
  both still unbundled.
