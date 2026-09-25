# Deferred — fragments and targets not applied

Written **2026-09-07** by the index-merge pass.

Rule in force: *"Re-check mtimes before each edit: `find <file> -mmin -15`. If a file was
modified in the last 15 minutes, another agent may be live — skip it, and record the skip
here."*

---

## 1. `vendors/lilygo/README.md` — deferred, then applied

| | |
|---|---|
| **First checked** | 2026-09-07 06:27 — mtime `06:19:02`, **8 minutes old → LIVE, skipped** |
| **Re-checked** | 2026-09-07 06:45 — mtime unchanged at `06:19:02`, **26 minutes old → quiet** |
| **Action** | Appended as **§10** from [`archive/devices/lilygo/t-display-k230/artifacts/research-scratch/vendor-guide-additions.md`](../../../archive/devices/lilygo/t-display-k230/artifacts/research-scratch/vendor-guide-additions.md). +103 lines, 0 deletions (measured against a pre-edit snapshot; the file is **untracked**, so `git diff` reports nothing for it). |

The file is untracked (`??`), created by the LilyGO T-Display-S3 session at 06:17–06:19 with a
numbered §1–§9 structure explicitly *"so a concurrent or later session can append §10+ without
touching existing text"*. That is exactly what was done.

`archive/devices/lilygo/t-display-s3-shared/artifacts/research-scratch/vendor-guide-additions.md` needed **no application**: it is not
content, it is that session's record of checking for an existing guide and finding none. Read
before concluding this.

---

## 2. Targets skipped entirely — none

Every other file named in the task was quiet at the moment it was edited. Full pre-edit
`find <file> -mmin -15` results are in [`README.md`](README.md) §4.

---

## 3. Fragment content deliberately **not** applied, with reasons

These are blocks present in the fragments that this pass did not act on. None was blocked by
mtime; each was out of scope or forbidden by the append-only rule.

| Fragment | Block | Why not applied |
|---|---|---|
| `m5stack-cardputer` §0 | Retire `components/unidentified/m5stack-stamp-s3a/dcdc-u4/` and replace with a redirect stub | **Deleting/replacing another session's record.** Forbidden by the append-only rule. A pointer was *added* instead, in `components/joulwatt/jw5712/README.md` §4 and in the `components/README.md` DinMeter table. Parked in [`corrections-requiring-review.md`](corrections-requiring-review.md) §1 |
| `xteink` §6 | Replace two claims in `devices/m5stack/papermono/comparisons-and-recommendations.md` | Rewrites existing prose in a tree the task did not list. Parked in [`corrections-requiring-review.md`](corrections-requiring-review.md) §4 |
| `xteink` §7 | Fix broken `bm8563` → `pcf8563` links | Explicitly *"do not fix silently"*. Parked in [`corrections-requiring-review.md`](corrections-requiring-review.md) §5 — and note the links **now resolve**, because the T-Display-S3 pass created `components/nxp/pcf8563/README.md` on 2026-09-07 |
| `lora-generations` §6.1, §6.2 | Replace text in `components/semtech/sx1262/README.md` | Editing existing lines. **Dated correction notes were added directly beneath the incorrect lines instead**, leaving the originals visible, per the task. Parked in [`corrections-requiring-review.md`](corrections-requiring-review.md) §2 and §3 |
| `m5stack-lora-expansions` §7.1–§7.4 | Four cross-references into `devices/m5stack/papermono*` | Out of the task's target list, and that tree is owned by another pass. Recorded here so the work is not lost |
| `xteink` §5, §8; `m5stack-dinmeter` §6; `m5stack-cardputer` §5, §6, §8, §8b(partial); `m5stack-lora-expansions` §5, §8; `lora-generations` §4; `lilygo-k230` §D; `lilygo-t-display-s3` §5 | Additions to `software/README.md`, `guides/markets/*` and `ai-crawler-site-access-table.md` | **Not in this task's target list.** `guides/markets/*` was marked protected by three separate sessions. Left for a maintainer — see [`README.md`](README.md) §6 |
| `m5stack-dinmeter` §7 | Proposed new `guides/markets/panel-mount-instrument-heads/` genre guide | The fragment itself says *"proposed rather than written, because one device is not enough to found a genre guide on."* Agreed; not created |
| `m5stack-cardputer` §4 | `vendors/m5stack/README.md` product ids, §5.6/§5.7 traps, change log | Out of the target list. ⚠ **Note:** `vendors/m5stack/README.md` §11 already exists (appended by the DinMeter pass 2026-09-04) but does **not** contain the Cardputer §4 material. Still outstanding |

---

## 4. ⚠ One source fragment was still being written

`archive/devices/lilygo/t-display-s3-shared/artifacts/research-scratch/index-fragments.md` had mtime **2026-09-07 06:23**, four minutes
before this pass began reading it, and the T-Display-S3 session was concurrently writing ~30
component records, `devices/lilygo/t-display-s3-amoled/README.md` and
`vendors/lilygo/README.md`.

The content was applied anyway, because:

- every path it references was verified to exist on disk before any row was written (see
  [`README.md`](README.md) §5);
- the *target* files (`devices/README.md`, `components/README.md`, `guides/hardware/README.md`,
  `vendors/README.md`) were all quiet, and the edits are append-only;
- the fragment reads as complete — it ends with a finished §6 table.

**It may nonetheless have grown since.** The fragment SHA-256 at the time of reading was
`2f3acf08c0bca4e60f28062996a05ba3a9f1e744ba7d971148ff55779012e943`. A merge note recording this
was added inline to `components/README.md` and `artifact-manifest.md`. **Re-diff that fragment
before treating either section as final.**

Other sessions were still active in the repository throughout this merge —
`devices/xteink/firmware-ecosystem.md` and
`guides/markets/handheld-and-eink-device-landscape-2026-09.md` were both modified during it.
Neither is a file this pass touched.
