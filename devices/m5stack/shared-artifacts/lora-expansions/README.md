# M5Stack LoRa expansions — shared research artifacts (archived)

> **Moved out of this repository, not deleted.** Archived **2026-09-20**.

[`cap-cc1101`](../../cap-cc1101/README.md) · [`cap-lora-1262`](../../cap-lora-1262/README.md) · [`cap-lora868`](../../cap-lora868/README.md) · [`cardputer-mesh-kit`](../../cardputer-mesh-kit/README.md) · [`stamp-c6lora`](../../stamp-c6lora/README.md) · [`unit-lora-e220`](../../unit-lora-e220/README.md)

## Where it went

| | |
|---|---|
| Was | `scratch/m5stack-lora-expansions/` |
| Now | `archive/devices/m5stack/shared-artifacts/lora-expansions/research-scratch/` |
| Destination README | [`devices/m5stack/shared-artifacts/lora-expansions/research-scratch/README`](../../../../archive/devices/m5stack/shared-artifacts/lora-expansions/research-scratch/) |
| Files | 95 |
| Directories | 14 |
| Symlinks | 0 |
| Bytes | 24,815,288 |
| Tree digest | `2a942d4ae87c46c8649208b37ce624c1b94d82f024ba1bb30c3c149934f8f51b` |
| Move method | `mv` only — no copy, no delete, no rename |
| Verification | pre/post manifest of every file, symlink and directory with SHA-256, compared line-for-line: **identical** |

`archive/` is a tracked symlink to this repository's slice of the sibling `repo-archive`
checkout. **It is machine-local — a fresh clone will not have it.** The destination README
carries the per-item provenance needed to reacquire the content without it.

This subject spans **six** LoRa expansion records, so it sits at the vendor level rather than
under any single unit.

It includes `artifacts/st25r3916_datasheet-m5stack-mirror.pdf` — a **vendor mirror** of an ST
datasheet. Per the filing rule, a chip datasheet is a *component* artifact; its canonical home
is `components/stmicroelectronics/st25r3916/artifacts/`, and the mirror is worth keeping
labelled because vendor mirrors routinely lag the chip maker's revision. Promoting it is a
separate, unperformed task.

## Digest recipe (locale-pinned)

```bash
find . -mindepth 1 \( -type f -o -type l -o -type d \) -print0 | LC_ALL=C sort -z
# regular files hashed with sha256sum; symlinks as SYMLINK:<target>; directories as DIR
# then sha256 over the concatenated "<type> <path> <hash> <size>" lines
```

`LC_ALL=C` is load-bearing: sort order, and therefore the digest, is locale-dependent.

## Restore from the local archive

```bash
mv archive/devices/m5stack/shared-artifacts/lora-expansions/research-scratch <wherever you want it>
```
