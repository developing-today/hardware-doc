# T-Display-K230 — research working set (archived)

> **Moved out of this repository, not deleted.** Archived **2026-09-20**.

[`devices/lilygo/t-display-k230/`](../README.md)

## Where it went

| | |
|---|---|
| Was | `scratch/lilygo-k230/` |
| Now | `archive/devices/lilygo/t-display-k230/artifacts/` |
| Destination README | [`devices/lilygo/t-display-k230/artifacts/README`](../../../../archive/devices/lilygo/t-display-k230/artifacts/) |
| Files | 717 |
| Directories | 172 |
| Symlinks | 0 |
| Bytes | 205,434,499 |
| Tree digest | `6b913f1d11d7bd3e6aff7e7c2c01498553b47abb5932511722ff46b1e11eda8c` |
| Move method | `mv` only — no copy, no delete, no rename |
| Verification | pre/post manifest of every file, symlink and directory with SHA-256, compared line-for-line: **identical** |

`archive/` is a tracked symlink to this repository's slice of the sibling `repo-archive`
checkout. **It is machine-local — a fresh clone will not have it.** The destination README
carries the per-item provenance needed to reacquire the content without it.

Split in the archive into `source-snapshots/` (three upstream clones) and `research-scratch/`
(everything else).

**All three clones are shallow** — one commit each, no history:

| Clone | Upstream | Commit | Tag |
|---|---|---|---|
| `T-Display-K230` | `Xinyuan-LilyGO/T-Display-K230` | `bb831ab358b66f5bd9a87ecd7c580fee4537492e` | `v0.2.4` |
| `T-Display-K230-nRF52840` | `Xinyuan-LilyGO/T-Display-K230-nRF52840` | `4646a728580739d487126f47a521e9b8032b3c2c` | `v0.2.0` |
| `T-Display-K230-nRF9151` | `Xinyuan-LilyGO/T-Display-K230-nRF9151` | `ed4ecbe34162dec9b81213a400198125bbd6e36f` | none |

## Digest recipe (locale-pinned)

```bash
find . -mindepth 1 \( -type f -o -type l -o -type d \) -print0 | LC_ALL=C sort -z
# regular files hashed with sha256sum; symlinks as SYMLINK:<target>; directories as DIR
# then sha256 over the concatenated "<type> <path> <hash> <size>" lines
```

`LC_ALL=C` is load-bearing: sort order, and therefore the digest, is locale-dependent.

## Restore from the local archive

```bash
mv archive/devices/lilygo/t-display-k230/artifacts <wherever you want it>
```
