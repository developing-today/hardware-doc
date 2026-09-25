# T-Display-S3 family — research working set and pinned snapshots (archived)

> **Moved out of this repository, not deleted.** Archived **2026-09-20**.

[`t-display-s3-shared`](../README.md) · [`t-display-s3`](../../t-display-s3/README.md) and the AMOLED/Long/Pro siblings

## Where it went

| | |
|---|---|
| Was | `scratch/lilygo-t-display-s3/` |
| Now | `archive/devices/lilygo/t-display-s3-shared/artifacts/` |
| Destination README | [`devices/lilygo/t-display-s3-shared/artifacts/README`](../../../../archive/devices/lilygo/t-display-s3-shared/artifacts/) |
| Files | 118 |
| Directories | 55 |
| Symlinks | 0 |
| Bytes | 33,563,425 |
| Tree digest | `f78adc6b7c0b80077a7f0457673e1e1564649005b44d639409c9b0ba7e373834` |
| Move method | `mv` only — no copy, no delete, no rename |
| Verification | pre/post manifest of every file, symlink and directory with SHA-256, compared line-for-line: **identical** |

`archive/` is a tracked symlink to this repository's slice of the sibling `repo-archive`
checkout. **It is machine-local — a fresh clone will not have it.** The destination README
carries the per-item provenance needed to reacquire the content without it.

Split in the archive into `source-snapshots/` (eight upstream trees) and `research-scratch/`.

The eight trees are named `<repo>@<full-40-char-commit>` — **the directory name is the
provenance record**; do not rename or abbreviate it. None contains a `.git`, so they carry no
history and no tags.

They are the evidence behind [`schematic-netlist.md`](../schematic-netlist.md) and
[`board-revision-drift.md`](../board-revision-drift.md): the drift finding depends on comparing
these specific pinned revisions, so the commits are load-bearing.

> Some references in `t-display-s3/commands.md` and `acquisition/` name files
> (`magic.py`, `pdfall.py`, `pdfcid.py`, `appdesc.py`, `shop-products.jsonl`) that were **not
> present** in the subject when it was archived — verified against the pre-move manifest. Those
> references were already dangling before this move and are left as-is rather than invented.

## Digest recipe (locale-pinned)

```bash
find . -mindepth 1 \( -type f -o -type l -o -type d \) -print0 | LC_ALL=C sort -z
# regular files hashed with sha256sum; symlinks as SYMLINK:<target>; directories as DIR
# then sha256 over the concatenated "<type> <path> <hash> <size>" lines
```

`LC_ALL=C` is load-bearing: sort order, and therefore the digest, is locale-dependent.

## Restore from the local archive

```bash
mv archive/devices/lilygo/t-display-s3-shared/artifacts <wherever you want it>
```
