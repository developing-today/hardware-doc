# XIAO ESP32S3 Sense — research working set (archived)

> **Moved out of this repository, not deleted.** Archived **2026-09-20**.

[`devices/seeed-studio/xiao-esp32s3-sense/`](../README.md)

## Where it went

| | |
|---|---|
| Was | `scratch/xiao-esp32s3-sense/` |
| Now | `archive/devices/seeed-studio/xiao-esp32s3-sense/artifacts/research-scratch/` |
| Destination README | [`devices/seeed-studio/xiao-esp32s3-sense/artifacts/research-scratch/README`](../../../../archive/devices/seeed-studio/xiao-esp32s3-sense/artifacts/research-scratch/) |
| Files | 18 |
| Directories | 1 |
| Symlinks | 0 |
| Bytes | 3,379,521 |
| Tree digest | `a2ce92fcc9b070a7e85b7e37f0b0b46d3db472a26468b5b890a7d99687ffbe68` |
| Move method | `mv` only — no copy, no delete, no rename |
| Verification | pre/post manifest of every file, symlink and directory with SHA-256, compared line-for-line: **identical** |

`archive/` is a tracked symlink to this repository's slice of the sibling `repo-archive`
checkout. **It is machine-local — a fresh clone will not have it.** The destination README
carries the per-item provenance needed to reacquire the content without it.

Contains **four more HTML-under-a-misleading-extension specimens**, kept under their original
names and verified by magic bytes:

| File | Bytes | Real content |
|---|---:|---|
| `p.bin` | 905,450 | HTML |
| `sib.pdf` | 905,450 | HTML |
| `ms.pdf` | 66,656 | HTML |
| `t.bin` | 66,656 | HTML |

`ms.pdf` and `t.bin` **are** byte-identical. `p.bin` and `sib.pdf` are the **same size but
different bytes** — checked by SHA-256, not assumed from the size. All four retained.

`sx1262.pdf` here describes a **chip**; by the filing rule its canonical home is
`components/semtech/sx1262/artifacts/`.

## Digest recipe (locale-pinned)

```bash
find . -mindepth 1 \( -type f -o -type l -o -type d \) -print0 | LC_ALL=C sort -z
# regular files hashed with sha256sum; symlinks as SYMLINK:<target>; directories as DIR
# then sha256 over the concatenated "<type> <path> <hash> <size>" lines
```

`LC_ALL=C` is load-bearing: sort order, and therefore the digest, is locale-dependent.

## Restore from the local archive

```bash
mv archive/devices/seeed-studio/xiao-esp32s3-sense/artifacts/research-scratch <wherever you want it>
```
