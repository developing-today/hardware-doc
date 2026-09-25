# DinMeter — research working set and source snapshots (archived)

> **Moved out of this repository, not deleted.** Archived **2026-09-20**.

[`dinmeter`](../README.md) · [`dinmeter-v1.1`](../../dinmeter-v1.1/README.md)

## Where it went

| | |
|---|---|
| Was | `scratch/m5stack-dinmeter/` |
| Now | `archive/devices/m5stack/dinmeter/artifacts/` |
| Destination README | [`devices/m5stack/dinmeter/artifacts/README`](../../../../archive/devices/m5stack/dinmeter/artifacts/) |
| Files | 374 |
| Directories | 78 |
| Symlinks | 0 |
| Bytes | 52,615,031 |
| Tree digest | `6a86ec2227f454699d4984a95191372726f1eb9d2d36421a0628c749554b3fc0` |
| Move method | `mv` only — no copy, no delete, no rename |
| Verification | pre/post manifest of every file, symlink and directory with SHA-256, compared line-for-line: **identical** |

`archive/` is a tracked symlink to this repository's slice of the sibling `repo-archive`
checkout. **It is machine-local — a fresh clone will not have it.** The destination README
carries the per-item provenance needed to reacquire the content without it.

Split in the archive into `source-snapshots/` and `research-scratch/`.

The source snapshots are **commit-pinned tarballs kept alongside their extractions** — the
commit hash is in the filename, which is the identity record:

| Tarball | Upstream | Pinned commit |
|---|---|---|
| `M5DinMeter-8ccbad72….tar.gz` | `m5stack/M5DinMeter` | `8ccbad7297beb82a140f812e5606e060d8a5e0dc` |
| `M5DinMeter-UserDemo-d2fdfe44….tar.gz` | `m5stack/M5DinMeter-UserDemo` | `d2fdfe44e9baf810f82335faa6f5962e9fc59a44` |
| `M5Unified-8530f537….tar.gz` | `m5stack/M5Unified` | `8530f5377d782e4a25a6c482de2e71c3f75ca8eb` |

Both archive and extraction are retained: the tarball is hash-verifiable, the extraction is
readable, and neither substitutes for the other.

## Digest recipe (locale-pinned)

```bash
find . -mindepth 1 \( -type f -o -type l -o -type d \) -print0 | LC_ALL=C sort -z
# regular files hashed with sha256sum; symlinks as SYMLINK:<target>; directories as DIR
# then sha256 over the concatenated "<type> <path> <hash> <size>" lines
```

`LC_ALL=C` is load-bearing: sort order, and therefore the digest, is locale-dependent.

## Restore from the local archive

```bash
mv archive/devices/m5stack/dinmeter/artifacts <wherever you want it>
```
