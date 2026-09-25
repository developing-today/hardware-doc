# ESP32-S3 Knob Touch LCD 1.8 — research working set (archived)

> **Moved out of this repository, not deleted.** Archived **2026-09-20**.

[`devices/waveshare/esp32-s3-knob-touch-lcd-1.8/`](../README.md)

## Where it went

| | |
|---|---|
| Was | `scratch/esp32-s3-knob-touch-lcd-1.8/` |
| Now | `archive/devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/research-scratch/` |
| Destination README | [`devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/research-scratch/README`](../../../../archive/devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/research-scratch/) |
| Files | 2 |
| Directories | 1 |
| Symlinks | 0 |
| Bytes | 12,956 |
| Tree digest | `e80c0e9bea87dc3ce90724ce4988f307ca2711b0edf18514fd09f7205931ce1a` |
| Move method | `mv` only — no copy, no delete, no rename |
| Verification | pre/post manifest of every file, symlink and directory with SHA-256, compared line-for-line: **identical** |

`archive/` is a tracked symlink to this repository's slice of the sibling `repo-archive`
checkout. **It is machine-local — a fresh clone will not have it.** The destination README
carries the per-item provenance needed to reacquire the content without it.

Two files — a community-probe result and the subject README. Kept because a negative or
low-yield search result is still evidence: it records that the probe was run and what it
returned, which saves the next pass from repeating it.

## Digest recipe (locale-pinned)

```bash
find . -mindepth 1 \( -type f -o -type l -o -type d \) -print0 | LC_ALL=C sort -z
# regular files hashed with sha256sum; symlinks as SYMLINK:<target>; directories as DIR
# then sha256 over the concatenated "<type> <path> <hash> <size>" lines
```

`LC_ALL=C` is load-bearing: sort order, and therefore the digest, is locale-dependent.

## Restore from the local archive

```bash
mv archive/devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/research-scratch <wherever you want it>
```
