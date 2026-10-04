# ARCHIVED: raw probe evidence for this survey

> The evidence tier for these 40 records was **moved out of `scratch/`, not deleted**.
> Archived **2026-09-20**. Every operation was `mv`.

**Reason:** bulky (232 MiB), derived from public endpoints, and of no use to a reader who is not
re-auditing a specific claim. The records already carry every finding, its date and its evidence
class.

## Identity

| Field | Value |
|---|---|
| Original repo path | `scratch/preprint-repositories/` |
| Archived to | `archive/research/preprint-repositories/` |
| Type | directory |
| Size | **243,783,241 bytes** (232.5 MiB) |
| File count | **903** (+ 10 later rescued from `/tmp`) |
| Tree digest | `46b31fcd2d337b57f37edbbeee154d7cb4af932c2f06840c12de2f1937cc899b` — verified identical before and after the move |
| Gathered | 2026-09-01 / 2026-09-02, re-probed 2026-09-04 |
| Retrieved by | the pass that wrote the 40 records in this directory |

`VERIFICATION.md` in this directory already recorded it as *"Raw probe evidence retained — 234 MB
in `scratch/preprint-repositories/`"*. Only the location changed.

## Path mapping — one substitution resolves every reference

The records cite this evidence ~31 times. The subject grouping was preserved exactly — nothing
renamed, reorganised or flattened — so:

```
scratch/preprint-repositories/<anything>
  →  archive/research/preprint-repositories/<anything>
```

The citing records were **not** edited; they are another pass's authored text. The archive-side
[`ARCHIVED-probe-evidence.md`](../../archive/research/preprint-repositories/ARCHIVED-probe-evidence.md)
carries the per-directory breakdown, and
[`SCRATCH-RELOCATION-2026-09-20.md`](../../SCRATCH-RELOCATION-2026-09-20.md) carries the map for
every relocated subject.

## What is in it

| Directory | Bytes | Backs |
|---|---:|---|
| `oa-fulltext/` | 104 MB | `open-access-full-text-sources.md`, `government-and-institutional-technical-reports.md` |
| `arxiv/` | 26 MB | `arxiv.md` |
| `missing-servers-v2/`, `missing-servers/` | 44 MB | `additional-preprint-servers.md` |
| `bulk-archives/` | 15 MB | `bulk-libraries-and-shadow-archives.md` |
| `dead-sites/` | 11 MB | `recovering-dead-technical-sites.md`, `closed-and-defunct-servers.md` |
| `engineering/` | 9.8 MB | `techrxiv.md`, `engrxiv.md`, `ecsarxiv.md` |
| `contested/` | 8.7 MB | `research-square.md`, `vixra.md`, `qeios.md`, `scienceopen.md` |
| `cryptology-eprint/` | 6.5 MB | `cryptology-eprint-archive.md` |
| `aggregators/` | 3.8 MB | `osf-preprints.md`, `figshare.md`, `zenodo.md`, `synthical.md` |
| `lifesci/` | 3.4 MB | `biorxiv-and-medrxiv.md`, `chemrxiv.md`, `life-science-and-medical-platforms.md`, `biohackrxiv.md` |
| `humanities/` | 2.5 MB | `social-sciences-and-humanities.md`, `library-science-and-cognitive-archives.md` |
| `platforms/` | 1.2 MB | `preprints-org.md`, `authorea.md`, `ssrn.md`, `repec-and-econstor.md` |
| `regional/` | 1.1 MB | `regional-and-national-servers.md`, `chinaxiv.md`, `hal.md` |
| `theses/` | 652 KB | `theses-and-dissertations.md` |
| `reachability-2026-09-01.txt`, `reprobe-A-2026-09-04.txt`, `reprobe.sh`, ~~`RECORD-TEMPLATE.md`~~ | 16 KB | the directory-wide runs and the record template. ⚠ **`RECORD-TEMPLATE.md` was promoted into this directory on 2026-09-20** — it defines the evidence-label vocabulary every record here uses, and a repository convention cannot live in a machine-local archive. See [`RECORD-TEMPLATE.md`](RECORD-TEMPLATE.md); the archive copy stays with a `.SUPERSEDED.md` sidecar |

## How to get it back

This evidence is **re-derivable, not re-downloadable as a set**. There is no archive of it and no
single URL. What exists is:

1. **The local archive** — restore with:

   ```bash
   mv "archive/research/preprint-repositories" "scratch/preprint-repositories"
   ```

2. **Re-probing.** `reprobe.sh` and the per-directory scripts (`lifesci/cohort.py`,
   `lifesci/chemrxiv-scan.py`, `regional/ua-ladder-probe.sh`, `engineering/*`) re-run the API and
   HTTP probes against the same endpoints. ⚠ **The results will differ**: several servers changed
   under the survey (openRxiv's rename, Research Square's journal list), some now block the UAs
   that worked, and some are gone. A 2026-09 answer is not reproducible in 2027.
3. **The records themselves.** Every consequential claim in the 40 documents carries its evidence
   label (`[API]`, `[WEB]`, `[DOC]`, `[LIT]`, `[COM]`, `[INF]`, `[NOT-VERIFIED]`), its date and
   its source. If the archive were deleted tomorrow, the repository would still state every
   finding — what it would lose is the ability to re-read the bytes behind one.

> **Only one recovery route is a true restore, and it is local.** That is unavoidable for probe
> output: the evidence is a measurement of a moment, not a document with a URL. It is why the
> bytes were kept rather than discarded as "regenerable".

## A caveat on reading it

Some captures are of **failures** — bot walls, 403s, throttles, SPA shells — and the records cite
them as negative evidence. A tiny or empty file in this tree is usually a finding, not a broken
download.

## Rescued working files

`archive/research/preprint-repositories/_rescued-from-tmp-2026-09-20/` holds nine working files
recovered from `/tmp`, including **`st.html`** — the Stanford CS Technical Reports index recorded
as the last outstanding archival candidate in [`retrieval-notes.md`](retrieval-notes.md) §9 — and
**`urls.txt`**, 1,177 unique external URLs extracted from these records for the deferred
link-validation task. ⚠ **Both items are still open.** Filing a capture beside its subject is not
the same as verifying it against CDX and writing it into the record.

## Subdirectories worth naming

Added 2026-09-20. An audit of archive-to-repo back-references found these three reachable
only through their parent, with nothing in this repository naming them. Small, but a reader
walking the archive had no way to know what they held.

| Archive path | Files | Size | What it is |
|---|---:|---:|---|
| `missing-servers/eccc-years/` | 35 | 4.7 MB | ECCC yearly listing pages, `1994.html`–`2026.html`, plus **two** negative controls (`1900.html` *and* `2099.html`, both 17,032 B, 0 report IDs). The per-year report counts in [`additional-preprint-servers.md`](additional-preprint-servers.md) were derived by parsing these. |
| `missing-servers-v2/eccc-years/` | 33 | 4.6 MB | ⚠ **A re-harvest of the same 33 pages 44 minutes later the same night — byte-identical, all 33.** See the correction below. |
| `_rescued-from-tmp-2026-09-20/preprint-pass/` | 9 | 368 KB | Working files rescued from `/tmp`. See below. |

### ⚠ Correction, 2026-09-20 — the two ECCC harvests do **not** differ

This table previously described `missing-servers-v2/eccc-years/` as *"a second harvest of the same
pages two days later, kept because the totals differ by one report (4,831 → 4,832) — that
difference is what established the archive was still growing mid-pass."* **The bytes refute every
part of that.** Measured by the bulk-archive audit:

| Check | Result |
|---|---|
| `diff -r` across the two directories | **Identical for all 33 shared pages.** The only difference is that v1 additionally holds the two negative controls |
| Per-file SHA-256, all 33 | **33/33 match** |
| mtimes | v1 `2026-09-02 01:22`, v2 `2026-09-02 02:06` — **44 minutes apart, same night**, not two days |
| Unique `TR<yy>-<nnn>` IDs parsed from each set | **4,831 in both** |
| `2026.html` report count, both copies | **162 in both** |

So the second harvest is a **same-night re-fetch that returned identical bytes** — which is a real
and useful negative result (the ECCC year pages were stable and almost certainly cached over that
interval), but it is the opposite of evidence that the archive grew.

**What this leaves unresolved.** [`additional-preprint-servers.md`](additional-preprint-servers.md)
records *"The 2026-09-02 harvest gave 162 for 2026 and a total of 4,831. The 2026-09-04 re-probe
gives 163 and 4,832."* **No 2026-09-04 ECCC capture exists anywhere in this archive** — the only
file in the whole tree with a 2026-09-04 mtime is `dead-sites/idx-pdf-fresh.txt`, and neither
`reprobe.sh` nor `reprobe-A-2026-09-04.txt` mentions ECCC. The 4,832 / 163 figures may well be
correct, but they were read live and never captured, so **they cannot be checked from the
archive**. That record already flags the pair as *"Recorded, not reconciled"*, which remains the
honest position; this note adds that the evidence tier cannot settle it. The record's own text was
**not edited** — it is another pass's authored prose, and the discrepancy is in the provenance
claim made here, not in its numbers.

### ⚠ Two "suspected duplicate" pairs, finally compared — both are **exact** duplicates

An earlier pass flagged these as near-duplicate harvests and never hashed them. Done 2026-09-20:

| Pair | Bytes each | SHA-256 | Verdict |
|---|---:|---|---|
| `missing-servers/anthology.bib.gz` vs `missing-servers-v2/anthology-fresh.bib.gz` | 12,647,756 | `5688fc19257a63e59d15e9387af621afd64d7c4a0e03e787f7ce067d7b4ca0bc` | **Byte-identical.** Fetched 32 minutes apart (01:38 → 02:10, 2026-09-02). The gzip header preserves the same inner name `anthology.bib` |
| `bulk-archives/idx-pdf.txt` vs `dead-sites/idx-pdf-fresh.txt` | 8,578,234 | `81055e8024abf401ff89faa833d3d09c9a02a4607cb6b7fb528f9606b4ce3ba1` | **Byte-identical.** Fetched **two days apart** (2026-09-02 02:15 → 2026-09-04 02:27) — the bitsavers PDF index did not change across that window |

**Both pairs were kept, deliberately.** The duplication *is* the finding in each case: a `-fresh`
re-harvest that returns identical bytes is a measured negative result about the upstream's
stability, and it is only legible while both copies and their timestamps survive. They cost
21.2 MB between them; if that ever matters, the hashes above are recorded and either copy may be
retired — but not by a pass that has not read this paragraph.

**Nothing else in this tree duplicates anything.** A full SHA-256 sweep of every file ≥ 32 KB
across the repository and the archive found no other byte-identical pair inside
`research/preprint-repositories/` beyond the ECCC set above and a handful of arXiv help pages that
are genuinely the same page served under `…/x` and `…/x_index` URLs.

The rescued working files: `crawler.bak` and `README.bak` are pre-merge backups of the two
index files, superseded by git history. `fulldiff.txt`, `diffleft.txt` and `stale_newer.txt`
are regenerable analysis. `scholarly_section.md` and `tips.md` were merged into both copies of
`ai-crawler-site-access-table.md`. Two have standing value:

- **`urls.txt`** — the 1,177 external URLs extracted from these 40 records. It is the input for
  the deferred link-validation task, and saves re-extracting them.
- **`st.html`** — the 1,332-byte Stanford CS technical-report index, recorded in
  [`retrieval-notes.md`](retrieval-notes.md) §9 as the last outstanding archival candidate.
  **Its presence closes that item**: the page had been captured, it simply was never filed.

