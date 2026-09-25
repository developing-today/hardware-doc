# FreeInk ecosystem source snapshots — ARCHIVED

**Archived to** `archive/software/ecosystems/crosspoint-freeink/source-snapshots/`
**Date:** 2026-09-20 · **3 clones · 202 195 196 B (192.8 MiB) · 1 235 files**

The archive is machine-local and absent from a fresh clone. Reacquisition is below; the archive
path is a convenience, not the contract.

## What is held

The **independent FreeInk SDK consumers** — projects that use `freeink-sdk` but are *not*
CrossPoint forks. Cloned 2026-09-01; upstream re-checked 2026-09-20, all three live.

| Snapshot | Remote `github.com/…` | HEAD | Commits | Licence | Bytes |
|---|---|---|---:|---|---:|
| `Free-Ink_freeink-reader` | `Free-Ink/freeink-reader` | `ca1c53d04e7db0dfcafe7e9dab1414445b33e990` | 12 | MIT | 10 742 448 |
| `MagicCube_free-ink-on-paper-mono` | `MagicCube/free-ink-on-paper-mono` | `34cc879427d5fc0b35f6af5084d4e7a003457665` | 10 | **none** | 190 612 320 |
| `mohitagw15856_Inkkit` | `mohitagw15856/Inkkit` | `5e2f741868eb3d3609ad9b72e74afca2e7cba1fd` (`v0.1.0-rc1`) | 9 | MIT | 840 428 |

All three are full clones, clean working trees, `main`.

**`freeink-reader`** is the FreeInk project's own reference reader — the control case for what
the SDK's authors build with it. **`free-ink-on-paper-mono`** is an unaffiliated third-party
PaperMono consumer that **patches the SDK**; its patch is the evidence behind
[`papermono-window-refresh.md`](../../frameworks/freeink-sdk/papermono-window-refresh.md), and
the patch file is retained in this repository at
[`…/freeink-sdk/artifacts/`](../../frameworks/freeink-sdk/artifacts/). **`Inkkit`** is a
self-declared "shared device-layer HAL" with **zero adoption** — grep for `inkkit` across
`crosspoint-reader/{src,lib,platformio.ini}` and `freeink-sdk/{libs,README.md}` returns nothing
(`executed-success`, 2026-09-20). It is preserved to record that negative result, so the next
reader who meets it advertised as a HAL does not have to re-establish that nobody uses it.

Detail in [`dependency-and-lineage.md`](dependency-and-lineage.md) and
[`fork-network.md`](fork-network.md).

## ⚠ Two of the three carry the profile of the repository that already vanished

`ideo2004-afk/crosspoint-reader-lua` was surveyed on 2026-09-01 as an unremarkable stale fork
and **404'd within 19 days**, with no Wayback capture — see
[its placeholder](../../applications/crosspoint-reader/source-snapshots/ideo2004-afk_crosspoint-reader-lua.ARCHIVED.md).

| Repository | Commits | Authors | Stars | Licence | Bundled? | Wayback? |
|---|---:|---:|---:|---|---|---|
| `MagicCube/free-ink-on-paper-mono` | 10 | 1 | low | **none** | **no** | **not submitted** |
| `mohitagw15856/Inkkit` | 9 | 3 | 1 | MIT | **no** | **not submitted** |

The archived full clones are the only local preservation. Both are non-shallow, so
`git bundle create <name>.bundle --all` would take seconds and produce a single hashable
artifact. **That has not been done** — an open action, recorded rather than quietly skipped.

## Licensing

`MagicCube/free-ink-on-paper-mono` has **no licence file**, so it is all-rights-reserved by
default. It is retained as a **research artifact** — evidence of what existed at a date — not as
redistributable code. The window-refresh patch was copied into this repository because it is the
load-bearing evidence for a correction, and that copy is labelled as coming from an unlicensed
source. Do not vendor further from it.

Per this project's policy, licence is metadata, not a gate on acquisition — see
[*Record licensing as metadata*](../../../.agents/skills/hardware-device-research/SKILL.md#17-record-licensing-as-metadata).

## Reacquisition

Status **`automatic`** for all three as of 2026-09-20:

```bash
git clone https://github.com/<owner>/<name>.git && git -C <name> checkout <HEAD above>
```

## Related archives

| Contents | Placeholder |
|---|---|
| CrossPoint, its forks, the old `community-sdk` | [`…/crosspoint-reader/source-snapshots/README.md`](../../applications/crosspoint-reader/source-snapshots/README.md) |
| The FreeInk SDK itself | [`…/freeink-sdk/source-snapshots.ARCHIVED.md`](../../frameworks/freeink-sdk/source-snapshots.ARCHIVED.md) |
| The simulator | [`…/tooling/source-snapshots.ARCHIVED.md`](../../tooling/source-snapshots.ARCHIVED.md) |
| API captures, fork listings, pre-clone extracts | [`research-captures.ARCHIVED.md`](research-captures.ARCHIVED.md) |
