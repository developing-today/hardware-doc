# ESP32-S3 ePaper 3.97 — research working set (archived)

> **Moved out of this repository, not deleted.** Archived **2026-09-20**.

[`devices/waveshare/esp32-s3-epaper-3.97/`](../README.md)

## Where it went

| | |
|---|---|
| Was | `scratch/waveshare-epaper/` |
| Now | `archive/devices/waveshare/esp32-s3-epaper-3.97/artifacts/research-scratch/` |
| Destination README | [`devices/waveshare/esp32-s3-epaper-3.97/artifacts/research-scratch/README`](../../../../archive/devices/waveshare/esp32-s3-epaper-3.97/artifacts/research-scratch/) |
| Files | 4 |
| Directories | 0 |
| Symlinks | 0 |
| Bytes | 232,661 |
| Tree digest | `9e5325d55223bb43006a536656efa043e56cedf404391fe9e9cf519075e907b7` |
| Move method | `mv` only — no copy, no delete, no rename |
| Verification | pre/post manifest of every file, symlink and directory with SHA-256, compared line-for-line: **identical** |

`archive/` is a tracked symlink to this repository's slice of the sibling `repo-archive`
checkout. **It is machine-local — a fresh clone will not have it.** The destination README
carries the per-item provenance needed to reacquire the content without it.

Four files. Preserves a small real finding: Waveshare's wiki serves the **same page under two
different capitalisations** of the product name — `wiki-ESP32-S3-ePaper-3.97.html` and
`wiki-ESP32-S3-EPaper-3.97.html`, both 13,451 B. Both are kept; the duplication is the
observation, and it is the sort of URL-casing trap worth recording in the Waveshare vendor
guide.

## Digest recipe (locale-pinned)

```bash
find . -mindepth 1 \( -type f -o -type l -o -type d \) -print0 | LC_ALL=C sort -z
# regular files hashed with sha256sum; symlinks as SYMLINK:<target>; directories as DIR
# then sha256 over the concatenated "<type> <path> <hash> <size>" lines
```

`LC_ALL=C` is load-bearing: sort order, and therefore the digest, is locale-dependent.

## Restore from the local archive

```bash
mv archive/devices/waveshare/esp32-s3-epaper-3.97/artifacts/research-scratch <wherever you want it>
```
