# ARCHIVED: PaperMono working files rescued from `/tmp`, 2026-09-20

> Moved out of `scratch/`, **not deleted**. Archived **2026-09-20**; every operation was `mv`.

This is a **separate set** from the `scratch/m5stack-papermono` subject, which was relocated the
same day by a parallel session to `artifacts/source-snapshots/` and
`artifacts/research-scratch/`. The two overlap in name only.

## Identity

| Field | Value |
|---|---|
| Original path | `scratch/_rescued-from-tmp-2026-09-20/{papermono-research,otpd-repo}/` and one file from `.../misc/` |
| Archived to | `archive/devices/m5stack/papermono/artifacts/research-scratch/rescued-from-tmp-2026-09-20/` |
| Size | **93,128,294 bytes** (88.8 MiB) |
| File count | **1,442** |
| Tree digest | `9816a965ba4944c53f63a72c49967dd4da14ff81135f8ed67dc7b183cb626e0b` |
| Captured | **2026-09-13** (mtimes) · found loose in `/tmp` and rescued **2026-09-20** |

Contents table:
[`archive/devices/m5stack/papermono/artifacts/research-scratch/rescued-from-tmp-2026-09-20/README.md`](../../../../archive/devices/m5stack/papermono/artifacts/research-scratch/rescued-from-tmp-2026-09-20/README.md).

## ⚠ It is not a duplicate of `source-snapshots/` — three of four overlapping clones differ

| Repository | `source-snapshots/` | This set |
|---|---|---|
| `M5Unified` | 191 files, 6,521,957 B, `6a71d829…` | **187 files, 3,660,205 B, `c4cf4a16…`** |
| `M5PaperMono-OTP-Demo` | 45 files, 82,659 B, `f9973dab…` | **46 files, 78,096 B, `04e96b4b…`** |
| `M5PaperMono-UserDemo` | 106 files, 867,868 B, `9b8dde5b…` | **107 files, 856,366 B, `2f49386…`** |
| `M5GFX` | 327 files, 217,692,258 B, `f24ce68b…` | the same bytes — reached by a **symlink** |

Do not assume either copy is "the" snapshot. Cite the one you read, by digest.

`otpd-repo/otpd/` is a **third** copy of `M5PaperMono-OTP-Demo`, and the only one carrying a
`.git` with the upstream remote and ref state (shallow — `.git/shallow` is present).

## What is in it

- `pm-research/hardware.yaml`, `status_led.{md,yaml}`, `pm_docs.{html,txt}` — the board hardware
  description, status-LED behaviour, and a capture of the PaperMono documentation.
- `pm-research/m5ioe1.{cpp,h}`, `m5pm1.{cpp,h}` — driver sources for the **M5IOE1** I/O expander
  and the **M5PM1** PMIC. Both parts have component records.
- `pm-research/repos/` — ten upstream checkouts: `M5GFX` (symlink), `M5Unified`,
  `M5PaperMono-OTP-Demo`, `M5PaperMono-UserDemo`, `PaperMonoCalendar`, `PaperMono-Launcher`,
  `papermono-rs`, `paper_name_plate`, `Nostos`, `m5-touch-card`.
- `bili-papermono-search.html` — a **bilibili search for "PaperMono"**, captured 2026-09-11.

## ⚠ Nothing here has been read end to end

The PaperMono records — including [`certification.md`](../certification.md) and
[`gaps-and-conflicts.md`](../gaps-and-conflicts.md) — were written from the
`scratch/m5stack-papermono` subject and the FCC exhibits, **not from this tree**. It was rescued
and filed on the same day.

Specific things here that are **not** known to be represented in any record:

- the **commit each of the ten checkouts sits at** — only `M5GFX`'s is recorded;
- `m5-touch-card` (60 MB) and `Nostos` — neither appears in
  [`projects-and-community.md`](../projects-and-community.md);
- the `otpd` clone's remote and ref state;
- `bili-papermono-search.html` — Chinese-language video community evidence for this device is a
  gap that record does not fill.

**Do not read the presence of this directory as evidence that its contents have been analysed.**
Provenance is also unverified: the sweep that recovered it stated it did not produce the files and
could not attribute them. Full rescue record:
[`archive/guides/research/artifacts/rescued-from-tmp-2026-09-20/`](../../../../archive/guides/research/artifacts/rescued-from-tmp-2026-09-20/README.md).

## The `M5GFX` symlink

`pm-research/repos/M5GFX` is a relative symlink to
`artifacts/source-snapshots/M5GFX` — the canonical full clone (877 commits, 64 tags, not shallow,
`d91077b9a607b59404e4e4a49f775c792bfae382`, tag `0.2.28`). It has been retargeted twice in two
days as the directories around it moved, and **verified after each move**. Its accompanying
`M5GFX.POINTER.md` carries the commit, the tag, the worktree digest (`7eae4c31…`, 294 files
excluding `.git`), five independent recovery URLs and a locale-pinned verification recipe —
read it before concluding anything is missing. ~150 MB of that clone is six generated CJK font
tables, which is why it is held once rather than three times.

## How to get it back

```bash
mv "archive/devices/m5stack/papermono/artifacts/research-scratch/rescued-from-tmp-2026-09-20" \
   "scratch/_rescued-from-tmp-2026-09-20"
```

The ten checkouts are all public upstreams (`m5stack/M5GFX`, `m5stack/M5Unified`,
`m5stack/M5PaperMono-OTP-Demo`, `m5stack/M5PaperMono-UserDemo`, and the community projects
`PaperMonoCalendar`, `PaperMono-Launcher`, `papermono-rs`, `paper_name_plate`, `Nostos`,
`m5-touch-card`). ⚠ **Only `M5GFX`'s commit is recorded**, so for the other nine a fresh clone
gives you *a* copy, not *this* copy. That is the reason these trees were kept rather than
discarded as regenerable.
