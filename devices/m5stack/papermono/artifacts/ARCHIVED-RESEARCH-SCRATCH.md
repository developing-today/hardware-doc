# PaperMono — research working set and upstream clones (archived)

> **Moved out of this repository, not deleted.** Archived **2026-09-20**.

[`devices/m5stack/papermono/`](../README.md) · [`papermono-lite`](../../papermono-lite/README.md)

## Where it went

| | |
|---|---|
| Was | `scratch/m5stack-papermono/` |
| Now | `archive/devices/m5stack/papermono/artifacts/` |
| Destination README | [`devices/m5stack/papermono/artifacts/README`](../../../../archive/devices/m5stack/papermono/artifacts/) |
| Files | 1179 |
| Directories | 275 |
| Symlinks | 0 |
| Bytes | 332,765,618 |
| Tree digest | `edfb1197a0fc159c2453b911c09178b98e7941fa68c3177357623afdd920aa4a` |
| Move method | `mv` only — no copy, no delete, no rename |
| Verification | pre/post manifest of every file, symlink and directory with SHA-256, compared line-for-line: **identical** |

`archive/` is a tracked symlink to this repository's slice of the sibling `repo-archive`
checkout. **It is machine-local — a fresh clone will not have it.** The destination README
carries the per-item provenance needed to reacquire the content without it.

Split in the archive into `source-snapshots/` (seven upstream clones + the 57 KB authored
`FINDINGS.md`) and `research-scratch/` (vendor PDFs, EPD pages, market captures, pin tables,
tools).

### Two things a future reader will otherwise get wrong

**`M5_Hardware` is a blobless partial clone — its content is not in the archive.** It was cloned
with `--filter=blob:none` and its working tree removed: 369 files in `HEAD`, **0** on disk,
~348 KB total. Git can name every file but the blobs live on GitHub. If
`github.com/m5stack/M5_Hardware` disappears, this entry yields filenames only. Hydrating it was
**not** done — it is a large unrequested network fetch — and is recorded as an open gap.

**`M5GFX` is the canonical full clone** (877 commits, tag `0.2.28`,
`d91077b9a607b59404e4e4a49f775c792bfae382`) and is the target of two symlinks elsewhere. Both
were retargeted during the move and verified to resolve. If it moves again, retarget them or
convert them to real copies — do not leave them dangling.

## Digest recipe (locale-pinned)

```bash
find . -mindepth 1 \( -type f -o -type l -o -type d \) -print0 | LC_ALL=C sort -z
# regular files hashed with sha256sum; symlinks as SYMLINK:<target>; directories as DIR
# then sha256 over the concatenated "<type> <path> <hash> <size>" lines
```

`LC_ALL=C` is load-bearing: sort order, and therefore the digest, is locale-dependent.

## Restore from the local archive

```bash
mv archive/devices/m5stack/papermono/artifacts <wherever you want it>
```
