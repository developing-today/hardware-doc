# FreeInk SDK — pinned source snapshots

Individual files from [`Free-Ink/freeink-sdk`](https://github.com/Free-Ink/freeink-sdk), each
pinned to a commit, kept because they are cited as **primary hardware evidence** for the Xteink
device family rather than as reading material.

> **Promoted out of `archive/devices/xteink/shared-artifacts/research-scratch/sdk-2026-09-11/` on 2026-09-20.** Both were the only local
> copy of evidence cited from `devices/xteink/x4-classic/sources.md` (rows XC16 and XC17). They
> are 114 KB and commit-pinned, so they are kept in the repository.

| File | Upstream path | Commit | Retrieved | Bytes |
|---|---|---|---|---:|
| [`BoardConfig-9f4d3f9.h`](BoardConfig-9f4d3f9.h) | `libs/hardware/BoardConfig/include/BoardConfig.h` | [`9f4d3f9ca675e64cc9d616081f39a33cdefce57e`](https://github.com/Free-Ink/freeink-sdk/blob/9f4d3f9ca675e64cc9d616081f39a33cdefce57e/libs/hardware/BoardConfig/include/BoardConfig.h) (2026-09-10) | 2026-09-11 | 109,812 |
| [`xteink-x4c-support.md`](xteink-x4c-support.md) | `docs/xteink-x4c-support.md` | [`9f4d3f9…`](https://github.com/Free-Ink/freeink-sdk/blob/9f4d3f9ca675e64cc9d616081f39a33cdefce57e/docs/xteink-x4c-support.md) (2026-09-10) | 2026-09-11 | 4,557 |

## Why these two files

`BoardConfig.h` carries the SDK's `enum class Board` and the per-board pin, bus and panel
profiles. For four of the five Xteink devices it is the **only** machine-readable hardware
description in existence — the vendor publishes no schematic, and the FCC schematics are
permanently confidential. It is reverse-engineered but **hardware-confirmed** by its authors.

These copies exist to support a specific comparison. An earlier pass used a full clone at commit
`24003795381a6c23630a26472ae3b06550333e71` (2026-09-01); this is the same file at HEAD nine days
later, fetched **to diff the two**. What the diff established:

- **No new Xteink board** appeared in `enum class Board` between the two commits — evidence that
  the then-rumoured "X4 v2" was not a separate SKU. It was right; the X4 Classic *is* the "X4 V2".
- `displaySpiHz` became a **shared 10 MHz** (down from 20 MHz on some profiles).

**"Diff `enum class Board` between two SDK commits" is the cheapest available test for "is there
a new SKU"** — a new board reaches the firmware SDK before it reaches the shop. Reusable
technique, recorded here rather than buried in one device's log.

## Evidence limitations

⚠ **Single lineage.** Everything downstream — the Draftling board headers, the community wikis —
derives from this same reverse-engineering effort. Two documents agreeing does **not** mean two
independent confirmations. Treat FreeInk-derived profiles as *one* source.

⚠ **Not a vendor document.** `community` class. It is the best available, not authoritative.

## Reacquisition — `automatic`

```bash
curl -fsSL -o BoardConfig-9f4d3f9.h \
  https://raw.githubusercontent.com/Free-Ink/freeink-sdk/9f4d3f9ca675e64cc9d616081f39a33cdefce57e/libs/hardware/BoardConfig/include/BoardConfig.h
curl -fsSL -o xteink-x4c-support.md \
  https://raw.githubusercontent.com/Free-Ink/freeink-sdk/9f4d3f9ca675e64cc9d616081f39a33cdefce57e/docs/xteink-x4c-support.md
```

Fallbacks: the `blob/` URLs in the table, `https://cdn.jsdelivr.net/gh/Free-Ink/freeink-sdk@9f4d3f9/…`,
or `https://web.archive.org/web/2/https://github.com/Free-Ink/freeink-sdk`.

The fuller clone at commit `2400379` is recorded in
[`scratch/eink-software/repos/freeink-sdk`](../../../../../scratch/eink-software/repos/freeink-sdk) —
a different session's working directory; **do not edit it**, cite it.

## Licence and disposition

| Field | Value |
|---|---|
| Licence | see the upstream repository's `LICENSE`; not restated here |
| Redistribution status | `unknown` |
| Disposition | **`repository`** — 114 KB, commit-pinned, cited as primary hardware evidence |

## Cited by

[`../../README.md`](../../README.md) ·
[`../../architecture.md`](../../architecture.md) ·
[`devices/xteink/x4-classic/sources.md`](../../../../../devices/xteink/x4-classic/sources.md) (XC16, XC17) ·
[`devices/xteink/x4-pro/sources.md`](../../../../../devices/xteink/x4-pro/sources.md)
