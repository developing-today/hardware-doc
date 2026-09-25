# ZeroWriter — shared research artifacts (archived)

> **Moved out of this repository, not deleted.** Archived **2026-09-20**.

[`zerowriter-ink`](../zerowriter-ink/README.md) · [`zerowriter-fold`](../zerowriter-fold/README.md)

## Where it went

| | |
|---|---|
| Was | `scratch/zerowriter/` |
| Now | `archive/devices/zerowriter/shared-artifacts/research-scratch/` |
| Destination README | [`devices/zerowriter/shared-artifacts/research-scratch/README`](../../../archive/devices/zerowriter/shared-artifacts/research-scratch/) |
| Files | 49 |
| Directories | 1 |
| Symlinks | 0 |
| Bytes | 2,972,954 |
| Tree digest | `9d10176f05588b3324fe6bf6b790cbc76162998d0be6da298e46f18a6451675d` |
| Move method | `mv` only — no copy, no delete, no rename |
| Verification | pre/post manifest of every file, symlink and directory with SHA-256, compared line-for-line: **identical** |

`archive/` is a tracked symlink to this repository's slice of the sibling `repo-archive`
checkout. **It is machine-local — a fresh clone will not have it.** The destination README
carries the per-item provenance needed to reacquire the content without it.

This subject covers **both** ZeroWriter models plus an Inkplate cross-reference, so it sits at
the vendor level rather than under `zerowriter-ink/`.

`cs/` and `cs-updates.html` are the Crowd Supply campaign updates — usually the only place
**design rationale** exists for a product like this.

Some `blog-*.html` / `zwi-*.html` captures here also exist inside the repository under
`zerowriter-ink/artifacts/`. The in-repo copies were **left untouched**; this is the working set
they were promoted from, retained rather than deduplicated.

## Digest recipe (locale-pinned)

```bash
find . -mindepth 1 \( -type f -o -type l -o -type d \) -print0 | LC_ALL=C sort -z
# regular files hashed with sha256sum; symlinks as SYMLINK:<target>; directories as DIR
# then sha256 over the concatenated "<type> <path> <hash> <size>" lines
```

`LC_ALL=C` is load-bearing: sort order, and therefore the digest, is locale-dependent.

## Restore from the local archive

```bash
mv archive/devices/zerowriter/shared-artifacts/research-scratch <wherever you want it>
```
