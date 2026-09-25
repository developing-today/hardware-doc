# Waveshare e-paper ESP32 range — shared research artifacts (archived)

> **Moved out of this repository, not deleted.** Archived **2026-09-20**.

[`e-paper-esp32-driver-board`](../../e-paper-esp32-driver-board/README.md) · [`esp32-c6-epaper-1.54`](../../esp32-c6-epaper-1.54/README.md) · [`esp32-s3-epaper-1.54`](../../esp32-s3-epaper-1.54/README.md) · [`esp32-s3-epaper-3.97`](../../esp32-s3-epaper-3.97/README.md) · [`esp32-s3-photopainter`](../../esp32-s3-photopainter/README.md)

## Where it went

| | |
|---|---|
| Was | `scratch/waveshare-epaper-esp32/` |
| Now | `archive/devices/waveshare/shared-artifacts/epaper-esp32/research-scratch/` |
| Destination README | [`devices/waveshare/shared-artifacts/epaper-esp32/research-scratch/README`](../../../../archive/devices/waveshare/shared-artifacts/epaper-esp32/research-scratch/) |
| Files | 44 |
| Directories | 6 |
| Symlinks | 0 |
| Bytes | 4,994,528 |
| Tree digest | `094efb4b423f70268e490105961738b03428d9c0fa4f9270980983a8d0b56250` |
| Move method | `mv` only — no copy, no delete, no rename |
| Verification | pre/post manifest of every file, symlink and directory with SHA-256, compared line-for-line: **identical** |

`archive/` is a tracked symlink to this repository's slice of the sibling `repo-archive`
checkout. **It is machine-local — a fresh clone will not have it.** The destination README
carries the per-item provenance needed to reacquire the content without it.

A cross-product survey spanning **five** Waveshare device records, so it sits at the vendor
level.

Seven `search-*.html` / `cat-epaper.html` captures are the **enumeration evidence** — they
record which queries were run against the store and what the result set was, which is what makes
the coverage claim checkable rather than asserted.

`err.txt` is zero bytes and is kept deliberately: an empty error log is the record that the run
completed without errors.

## Digest recipe (locale-pinned)

```bash
find . -mindepth 1 \( -type f -o -type l -o -type d \) -print0 | LC_ALL=C sort -z
# regular files hashed with sha256sum; symlinks as SYMLINK:<target>; directories as DIR
# then sha256 over the concatenated "<type> <path> <hash> <size>" lines
```

`LC_ALL=C` is load-bearing: sort order, and therefore the digest, is locale-dependent.

## Restore from the local archive

```bash
mv archive/devices/waveshare/shared-artifacts/epaper-esp32/research-scratch <wherever you want it>
```
