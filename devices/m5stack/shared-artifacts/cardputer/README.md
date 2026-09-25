# Cardputer — shared research artifacts (archived)

> **Moved out of this repository, not deleted.** Archived **2026-09-20**.

[`cardputer-v1.0`](../../cardputer-v1.0/README.md) · [`cardputer-v1.1`](../../cardputer-v1.1/README.md) · [`cardputer-adv`](../../cardputer-adv/README.md) · [`cardputer-mesh-kit`](../../cardputer-mesh-kit/README.md) · [`cardputer-zero`](../../cardputer-zero/README.md)

## Where it went

| | |
|---|---|
| Was | `scratch/m5stack-cardputer/` |
| Now | `archive/devices/m5stack/shared-artifacts/cardputer/` |
| Destination README | [`devices/m5stack/shared-artifacts/cardputer/README`](../../../../archive/devices/m5stack/shared-artifacts/cardputer/) |
| Files | 644 |
| Directories | 187 |
| Symlinks | 1 |
| Bytes | 77,228,067 |
| Tree digest | `1fae34c27b5bf5260e407c0876fd0c4c9aab0ea8860f36eca9d2d03d40f37a2f` |
| Move method | `mv` only — no copy, no delete, no rename |
| Verification | pre/post manifest of every file, symlink and directory with SHA-256, compared line-for-line: **identical** |

`archive/` is a tracked symlink to this repository's slice of the sibling `repo-archive`
checkout. **It is machine-local — a fresh clone will not have it.** The destination README
carries the per-item provenance needed to reacquire the content without it.

This subject spans **five** Cardputer records, so it sits at the vendor level rather than under
one variant — mirroring [`devices/espressif/shared-artifacts/`](../../../espressif/shared-artifacts/README.md).

Split in the archive into `source-snapshots/` and `research-scratch/`.

| Clone | Upstream | Commit | Note |
|---|---|---|---|
| `M5Cardputer` | `m5stack/M5Cardputer` | `f1392858b9994c3547120e602a57d3553d16ab01` | tag `1.2.0` + 2 |
| `M5Cardputer-UserDemo` | `m5stack/M5Cardputer-UserDemo` | `b549eac0a3c65bc108186c276b8fac0a214aaa4e` | **detached HEAD** |
| `M5Unified` | `m5stack/M5Unified` | `8530f5377d782e4a25a6c482de2e71c3f75ca8eb` | **shallow**, 599 commits |
| `M5GFX` | — | — | **symlink** to the papermono canonical clone |

`M5Unified` at this same commit also exists as a **780-commit non-shallow** clone under
`papermono/artifacts/source-snapshots/`. Both were kept; they are not interchangeable.

The schematic PDFs in `research-scratch/` are deliberately split per variant
(`pdf-v11`, `pdf-v11base`, `pdf-adv`, `pdf-stamps3`, `pdf-stamps3a`) — that split is what makes
revision differences visible. Do not merge them.

## Digest recipe (locale-pinned)

```bash
find . -mindepth 1 \( -type f -o -type l -o -type d \) -print0 | LC_ALL=C sort -z
# regular files hashed with sha256sum; symlinks as SYMLINK:<target>; directories as DIR
# then sha256 over the concatenated "<type> <path> <hash> <size>" lines
```

`LC_ALL=C` is load-bearing: sort order, and therefore the digest, is locale-dependent.

## Restore from the local archive

```bash
mv archive/devices/m5stack/shared-artifacts/cardputer <wherever you want it>
```
