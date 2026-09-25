# `ideo2004-afk/crosspoint-reader-lua` — archived snapshot

> ⚠ **The upstream repository no longer exists.** `https://github.com/ideo2004-afk/crosspoint-reader-lua`
> returned **HTTP 404** on **2026-09-20** to both the web and the REST API, and
> `git ls-remote` reports *"Repository not found"*. There is **no Wayback Machine
> capture** (`archive.org/wayback/available` returns an empty `archived_snapshots`
> object). **This snapshot is, as far as this project can establish, the only
> surviving copy.**
>
> The owning account `ideo2004-afk` still exists (API 200), so the repository was
> deleted or made private rather than the account being removed.

| | |
|---|---|
| **What it was** | A fork of [CrossPoint Reader](../README.md) that stayed on the **pre-FreeInk** `open-x4-epaper/community-sdk`, on branch `crosspoint-flow` |
| **Cloned** | 2026-09-01 (full history — **not** shallow) |
| **Verified dead** | 2026-09-20 |
| **Archive path** | `archive/software/applications/crosspoint-reader/source-snapshots/ideo2004-afk_crosspoint-reader-lua.bundle` |
| **Reacquisition** | **`lost`** — no public source remains |

## Identity

| Field | Value |
|---|---|
| Origin URL | `https://github.com/ideo2004-afk/crosspoint-reader-lua.git` (**dead**) |
| Branch | `crosspoint-flow` (the clone's HEAD) |
| HEAD commit | `6bc3bcd92f9c8db991ac59a262df3ac00948bae1` |
| HEAD date | 2026-04-03T15:55:49+08:00 |
| `git describe` | `v3.0.1-1-g6bc3bcd` |
| Root commit | `2ccdbeecc8b85a019422f80c5e9b0c70aaf92901` "Public release" — **shared with upstream `crosspoint-reader`**, confirming a true fork with inherited history |
| Commits (all refs) | **784** |
| Refs in bundle | **59** (branches + tags through `v3.0.1`) |
| Licence | MIT (`LICENSE` present in tree) |

## The archived file

| Field | Value |
|---|---|
| Filename | `ideo2004-afk_crosspoint-reader-lua.bundle` |
| Format | `git bundle` (v2, SHA-1) |
| Bytes | **264 162 782** |
| SHA-256 | `86006e0e84e0b66d7b6aaeaa6245a9081f3680303ed2e8d0b591b650961c85f8` |
| Integrity | `git bundle verify` → *"The bundle records a complete history"* |

A bundle rather than a directory tree: it carries **all 59 refs and the complete
784-commit history** in one hashable file, and the working tree is reproducible
from it. The original checkout was 447 MB; the bundle is 264 MB.

**Compression was tested and rejected.** `zstd -19` yields 263 206 355 bytes — a
**0.36 %** saving, because a git bundle is already a zlib-compressed packfile.
Not worth the added decode step. Store as-is.

### Restoring it

```bash
# from the repository root, with the archive present
git clone archive/software/applications/crosspoint-reader/source-snapshots/ideo2004-afk_crosspoint-reader-lua.bundle \
          crosspoint-reader-lua
cd crosspoint-reader-lua && git checkout crosspoint-flow
```

`git clone` from a bundle restores every ref. **Without the archive there is no
recovery path** — see the warning at the top.

## What is permanently lost even *with* this snapshot

**The fork's SDK pin cannot be reconstructed by anyone.** Its `.gitmodules`:

```ini
[submodule "open-x4-sdk"]
	path = open-x4-sdk
	url = https://github.com/open-x4-epaper/community-sdk.git
```

and the gitlink at HEAD records `a75faa8880d28df2b8e6fbd21de5a4a5b2906c67`.

That commit is **gone from every location checked** (`executed-success`, 2026-09-20):

| Location | Result |
|---|---|
| Upstream `open-x4-epaper/community-sdk` (which **is** still live) | `fatal: remote error: upload-pack: not our ref a75faa88…` |
| The clone's own submodule object store | `git cat-file -t` → *"could not get object info"* |

So the exact SDK revision this fork built against **can never be recovered**, and
`git submodule update` will always fail. Whoever took the snapshot worked around
it by checking out the SDK's then-current `main` HEAD
`7d86603ad27709a9a766bb5ad893cfc39e60777e` instead — which is why the bundle's
worktree shows `open-x4-sdk` as modified. **The substituted commit is not what
this fork was built against**, and any build from this snapshot is therefore an
approximation. Record it as such rather than treating a successful build as
evidence about the original.

The upstream SDK itself remains fully recoverable: `open-x4-epaper/community-sdk`
answered `git ls-remote` normally on 2026-09-20, HEAD `7d86603a`.

## Why it was kept

Against the [archiving test](../../../../.agents/skills/hardware-device-research/SKILL.md#when-to-archive),
this fails the "reacquirable" criterion outright — the artifact is **primary and
irreplaceable**, which is the stated reason to retain rather than discard. The
other nine clones taken in the same session were left in scratch precisely
because they *are* reacquirable.

Its research value is modest but real, and it is the reason the loss matters:

- It is the **only preserved example of a CrossPoint fork still on the pre-FreeInk
  `community-sdk`**, i.e. the architecture that existed before the June-2026
  migration documented in [dependency and lineage](../../../ecosystems/crosspoint-freeink/dependency-and-lineage.md).
- Its name implies Lua scripting. **It has none.** A tree-wide grep across upstream
  CrossPoint and all 25 of its remote branches for `lua.h`, `wasm3`, `quickjs`,
  `duk_config`, `berry` and `mruby` matched only a substring false positive inside
  vendored expat. The repository name is **not** evidence of a scripting engine
  anywhere in this family — see the same record's note on the "scripting" hint.

## The generalisable warning

This repository was surveyed on 2026-09-01 as an ordinary, if stale, fork and was
**gone within 19 days**. Nothing flagged it as at-risk beyond being a low-star
personal repository last pushed five months earlier.

**Do not assume a GitHub URL is a durable citation.** Where a personal repository
carries anything load-bearing, bundle it at the time of research — it costs one
command — or at minimum submit the URL to `web.archive.org/save/`. Neither was
done here, and only an incidental full-history clone prevented total loss.

The same profile applies today to `MagicCube/free-ink-on-paper-mono` (10 commits,
single author, **no `LICENSE`**) and `mohitagw15856/Inkkit` (9 commits, 1 star) —
both still live, both unbundled. See the
[scratch README](../../../../scratch/eink-software/README.md) for the full
disposition of the ten clones.

## See also

- [CrossPoint Reader](../README.md) — the fork parent
- [Dependency and lineage](../../../ecosystems/crosspoint-freeink/dependency-and-lineage.md) — where this fork sits, and the `community-sdk` → FreeInk migration it never made
- [Fork network](../../../ecosystems/crosspoint-freeink/fork-network.md) — why detached and stale forks are hard to measure
- [Plugin source snapshots](../plugins/source-snapshots.ARCHIVED.md) — the sibling archive of 18 plugin-ecosystem repositories
