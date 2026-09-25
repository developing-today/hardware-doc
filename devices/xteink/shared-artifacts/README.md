# XTEInk — shared research artifacts (archived)

> **Moved out of this repository, not deleted.** Archived **2026-09-20**.

[`x3`](../x3/README.md) · [`x4`](../x4/README.md) · [`x4-classic`](../x4-classic/README.md) · [`x4-light`](../x4-light/README.md) · [`x4-pro`](../x4-pro/README.md) · [`nano`](../nano/README.md) · [`s4`](../s4/README.md)

## Where it went

| | |
|---|---|
| Was | `scratch/xteink/` |
| Now | `archive/devices/xteink/shared-artifacts/research-scratch/` |
| Destination README | [`devices/xteink/shared-artifacts/research-scratch/README`](../../../archive/devices/xteink/shared-artifacts/research-scratch/) |
| Files | 505 |
| Directories | 73 |
| Symlinks | 0 |
| Bytes | 269,581,091 |
| Tree digest | `43841e95f52e990a2e32785c28a71e7223c01f2dc91c26061b32b4c85630fc29` |
| Move method | `mv` only — no copy, no delete, no rename |
| Verification | pre/post manifest of every file, symlink and directory with SHA-256, compared line-for-line: **identical** |

`archive/` is a tracked symlink to this repository's slice of the sibling `repo-archive`
checkout. **It is machine-local — a fresh clone will not have it.** The destination README
carries the per-item provenance needed to reacquire the content without it.

**Sixteen `.pdf` files in there are not PDFs.** They are preserved acquisition failures — vendor
portals answering a document URL with an HTML error page, a login wall or a JSON error blob —
kept under their misleading names on purpose, because the name records which URL lies. Twelve
are in `datasheets/`, four in `datasheets/cfprobe/`. The destination README lists all sixteen
with byte counts and actual magic bytes.

It also holds two upstream checkouts: `github-2026-09-11/x4pro-emu`
(<https://github.com/kycube/x4pro-emu> @ `bf4b86ae0471012d4d07c0bb3042f3f561c9c302`, **shallow**)
and `github-2026-09-11/draftling`, each beside its own acquisition metadata.

## Digest recipe (locale-pinned)

```bash
find . -mindepth 1 \( -type f -o -type l -o -type d \) -print0 | LC_ALL=C sort -z
# regular files hashed with sha256sum; symlinks as SYMLINK:<target>; directories as DIR
# then sha256 over the concatenated "<type> <path> <hash> <size>" lines
```

`LC_ALL=C` is load-bearing: sort order, and therefore the digest, is locale-dependent.

## Restore from the local archive

```bash
mv archive/devices/xteink/shared-artifacts/research-scratch <wherever you want it>
```
