# ZeroWriter Ink — source-snapshot provenance working set (archived)

> **Moved out of this repository, not deleted.** Archived **2026-09-20**.

[`devices/zerowriter/zerowriter-ink/`](../README.md) · the finding it backs: [`source-snapshot-provenance.md`](../source-snapshot-provenance.md)

## Where it went

| | |
|---|---|
| Was | `scratch/zerowriter-provenance-2026-08-30/` |
| Now | `archive/devices/zerowriter/zerowriter-ink/artifacts/provenance-2026-08-30/` |
| Destination README | [`devices/zerowriter/zerowriter-ink/artifacts/provenance-2026-08-30/README`](../../../../archive/devices/zerowriter/zerowriter-ink/artifacts/provenance-2026-08-30/) |
| Files | 157 |
| Directories | 45 |
| Symlinks | 0 |
| Bytes | 139,146,677 |
| Tree digest | `e4d8b1dded5f48fca104b996c6868d65beb9562355f684953fda17e5d6b728a4` |
| Move method | `mv` only — no copy, no delete, no rename |
| Verification | pre/post manifest of every file, symlink and directory with SHA-256, compared line-for-line: **identical** |

`archive/` is a tracked symlink to this repository's slice of the sibling `repo-archive`
checkout. **It is machine-local — a fresh clone will not have it.** The destination README
carries the per-item provenance needed to reacquire the content without it.

**This is primary evidence, not intermediates.** It holds the byte-exact upstream tarball
`zerowriter_ink-996207ac.tar.gz` (53,370,137 B) at commit
`996207aca0677300ed5f1fdf762d9c9ec79f516e`, its extraction, and the scripts that proved the
in-repository snapshot is semantically unmodified but **no longer byte-identical** to upstream
(50 of 152 files rewritten by a CRLF→LF pass and a trailing-whitespace strip).

That finding is only reproducible while this tarball survives.

Reacquire:

```bash
curl -L -o zerowriter_ink-996207ac.tar.gz \\
  https://codeload.github.com/zerowriter/zerowriter_ink/tar.gz/996207aca0677300ed5f1fdf762d9c9ec79f516e
```

A re-fetched tarball is not guaranteed byte-stable; the durable check is the per-file hash list
at [`source-snapshots/zerowriter_ink-upstream-996207ac.sha256.txt`](source-snapshots/zerowriter_ink-upstream-996207ac.sha256.txt), which is **in this repository**.

## Digest recipe (locale-pinned)

```bash
find . -mindepth 1 \( -type f -o -type l -o -type d \) -print0 | LC_ALL=C sort -z
# regular files hashed with sha256sum; symlinks as SYMLINK:<target>; directories as DIR
# then sha256 over the concatenated "<type> <path> <hash> <size>" lines
```

`LC_ALL=C` is load-bearing: sort order, and therefore the digest, is locale-dependent.

## Restore from the local archive

```bash
mv archive/devices/zerowriter/zerowriter-ink/artifacts/provenance-2026-08-30 <wherever you want it>
```
