# `research/` — subject surveys and pass reports

Two kinds of thing live here, and neither fits `devices/`, `components/`, `vendors/` or
`guides/`.

| Directory | What |
|---|---|
| [`preprint-repositories/`](preprint-repositories/README.md) | A **source-traceable survey of a research infrastructure** — 40 records covering every repository on Wikipedia's list of preprint servers, written to answer "if I find a paper here, how much should I believe it, and will the link still work in five years?" |
| [`passes/`](passes/README.md) | **Reports on passes over this repository itself** — index merges, cross-cutting synthesis. What was changed, what was deferred, what two sessions disagreed about |

## Why the category exists

The skill's taxonomy is open by design: *"add a category when material genuinely fits none of the
four, and say in the index why it exists."* This is that note.

`preprint-repositories/` describes **where scholarly and technical documents come from**, which is
upstream of every `sources.md` in the repository but is about no device, component, vendor or
development technique. It is not a guide — nobody follows it to build something — it is a survey
with per-server records, evidence labels and dated measurements, structured like the device
records are.

`passes/` describes **what was done to this repository and when**. It is neither research output
nor a guide; it is the audit trail. It lives here rather than at the repository root because
there are several files per pass and the root already carries eight `VERIFICATION-*.md` reports.

## Where the evidence is

Both directories' raw material is in the archive, at the mirrored path:

| Records | Evidence |
|---|---|
| `research/preprint-repositories/` | `archive/research/preprint-repositories/` — 903 files, 232 MiB of probe output, HTML captures and CDX dumps |
| `research/passes/index-merge/` | `archive/research/passes/index-merge/round-two-workdir-2026-09-11/` — 314 files, 60 MiB of pre-edit snapshots and renders |

Both were moved out of `scratch/` on 2026-09-20; see
[`SCRATCH-RELOCATION-2026-09-20.md`](../SCRATCH-RELOCATION-2026-09-20.md).
