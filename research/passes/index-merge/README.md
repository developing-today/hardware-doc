# Index merge — seven research sessions applied to the shared indexes

**Run 2026-09-07, 06:27 → 06:50 CDT.** Append-only. No git state was changed.

Seven parallel research sessions added ~40 device records and ~90 component records but were
each forbidden from editing shared index files, leaving ready-to-paste Markdown in
`scratch/<session>/index-fragments.md`. This pass applied those fragments.

- **What was deferred, and why** → [`deferred.md`](deferred.md)
- **Corrections that need a human decision** → [`corrections-requiring-review.md`](corrections-requiring-review.md)

---

## 1. Files edited, and the numbers

Every edit is an insertion. The **"mine"** columns are measured against a byte-exact snapshot of
each file taken immediately before this pass touched it, because several of these files already
carried *other* sessions' uncommitted work.

| File | + mine | − mine | What was added |
|---|---:|---:|---|
| `devices/README.md` | 91 | **0** | `## Xteink`, `## LilyGO` (merged from two fragments), and three `###` subsections under the existing `## M5Stack`: DinMeter ×2, Cardputer ×5, Cardputer expansions ×8 |
| `components/README.md` | 199 | **0** | One `## Seven-pass component sweep` section: merged new-manufacturer table (25 makers), then per-pass tables for Xteink, DinMeter, Cardputer, LoRa expansions, Semtech generations, K230 and T-Display-S3 |
| `vendors/README.md` | 4 | **0** | `M5Stack` + `LilyGO / TTGO` rows in *Board and device vendors*; `Semtech` + `Canaan Creative` rows in *Component vendors — parts we document* |
| `guides/README.md` | 3 | **0** | `parallel-8080-lcd-buses.md` and `lora-radio-generations.md` in the Hardware-subsystems table; `riscv-and-vendor-sdk-toolchains.md` in the Host-platform table |
| `guides/hardware/README.md` | 2 | **0** | The same two hardware guides, in that index's own format |
| `README.md` (root) | 12 | **0** | 1 new *Research passes* row, 7 new *Quick entry points* bullets, 4 new *Verification reports* entries |
| `artifact-manifest.md` | 142 | **0** | `## Seven-session sweep` with per-pass artifact tables, hashes, licence flags and totals |
| `vendors/lilygo/README.md` | 103 | **0** | `## 10.` — the K230 pass's LilyGO sourcing findings. **Deferred first, applied after re-check** — see [`deferred.md`](deferred.md) §1 |
| `components/everest-semiconductor/es8311/README.md` | 25 | **0** | Cardputer ADV *Used By* (§3.1) |
| `components/nsiway/ns4150b/README.md` | 18 | **0** | Cardputer ADV *Used By* (§3.2) |
| `components/bosch-sensortec/bmi270/README.md` | 25 | **0** | Cardputer ADV + CardputerZero *Used By* (§3.3) |
| `components/awinic/aw35122/README.md` | 23 | **0** | Stamp-S3A *Used By* (§3.4) |
| `components/joulwatt/jw5712/README.md` | 28 | **0** | ⏳ Stamp-S3A *Used By* (§3.5) + provenance note |
| `components/sitronix/st7789v2/README.md` | 26 | **0** | ⏳ Cardputer v1.0/v1.1/ADV *Used By* (§3.6) |
| `components/generic/tp4057/README.md` | 28 | **0** | ⏳ Cardputer *Used By* (§3.7) + a **new conflict** flagged |
| `components/silergy/sy7088/README.md` | 22 | **0** | ⏳ Cardputer *Used By* (§3.8) |
| `components/m5stack/stamp-s3a/README.md` | 16 | **0** | ⏳ Devices-carrying-this-module table (§3.9) |
| `components/m5stack/stamp-s3/README.md` | 14 | **0** | ⏳ Devices-carrying-this-module table (§3.10) |
| `components/semtech/sx1262/README.md` | 49 | **0** | ⏳ Cardputer Mesh Kit *Used By* (§3.11) + ⏳ LilyGO K230 *Used By* (§F1) + **two dated correction notes** |
| `components/texas-instruments/tca8418/README.md` | 20 | **0** | ⏳ LilyGO K230 Kit *Used By* (§F2) |
| `components/texas-instruments/bq27220/README.md` | 16 | **0** | ⏳ LilyGO K230 Kit *Used By* (§F3) |
| `components/generic/micro-sd-sdmmc/README.md` | 12 | **0** | ⏳ LilyGO K230 *Used By* (§F4) |
| **Total** | **878** | **0** | 22 files |

Plus three new files in this directory: `README.md`, `deferred.md`,
`corrections-requiring-review.md`.

## 2. Mechanical verification

`git diff -- <file> | grep -c '^-[^-]'` printed **`0` for all 22 files.**

`git diff --stat` over the 12 **tracked** files reports:

```
12 files changed, 973 insertions(+), 1 deletion(-)
```

### ⚠ The single reported deletion is not from this pass

It is in `README.md`, hunk `@@ -74 +74 @@` — 18 lines above this pass's nearest edit. It is
another session's **unstaged** replacement of the *Cross-cutting guides* bullet, adding `[NFC]`
and `[LoRa]` links. Proof:

```
index  (git show :README.md, line 74):  … · [markets and sourcing] …          # no NFC, no LoRa
worktree                    line 74):  … · [NFC](guides/nfc/README.md) · [LoRa](guides/lora/README.md) · …
```

The worktree form was already present when this pass first read the file at 06:27, before any
edit. Measured against pre-edit snapshots, **this pass's own contribution is 878 insertions and
0 deletions.**

### Why tracked-file totals exceed this pass's own

`git diff` compares worktree to **index**, and several targets already held other sessions'
uncommitted work — e.g. `components/README.md` shows 369 insertions, of which **199 are this
pass's** and 170 pre-existed. Nine of the component records edited here are **untracked** (`??`),
so `git diff` reports nothing for them at all; for those the snapshot diff is the only valid
measurement, and it is 0 deletions in every case.

### Links

**956 relative links across the 22 edited files were resolved against the filesystem: 0 broken.**
Every path referenced by a fragment was confirmed to exist *before* its row was written — no
index row points at a record that is not on disk.

## 3. Git state

**Unchanged.** No `add`, `commit`, `rm`, `reset`, `checkout`, `restore`, `stash`, `clean` or
`push` was run. Only `git diff`, `git status`, `git show` and `git rev-parse`.

```
HEAD at start:  4aa02e1030b3b0861e6fc34f23fa2113ec80d324
HEAD at end:    4aa02e1030b3b0861e6fc34f23fa2113ec80d324
```

The index was left exactly as found, including the other session's staged changes to
`README.md`, `components/README.md`, `devices/README.md`, `components/semtech/sx1262/README.md`,
`components/joulwatt/jw5712/README.md` and `components/awinic/aw35122/README.md`.

## 4. mtime checks

`find <file> -mmin -15` immediately before each edit. All **quiet** except one:

| File | Result |
|---|---|
| `vendors/lilygo/README.md` | ⚠ **LIVE at 06:27** (mtime 06:19, 8 min). **Skipped.** Re-checked 06:45 → 26 min old, quiet → applied. See [`deferred.md`](deferred.md) §1 |
| all 21 others | quiet at the moment of editing |

Other sessions remained active in the repository throughout — `devices/xteink/firmware-ecosystem.md`
and `guides/markets/handheld-and-eink-device-landscape-2026-09.md` were both written during this
merge. Neither is a file this pass touched.

## 5. Merges performed

Rule: *where two fragments propose overlapping text for the same file, merge into one coherent
section rather than pasting both.*

| Overlap | Resolution |
|---|---|
| **LilyGO in `devices/README.md`** — proposed by both `lilygo-k230` §B (a bullet) and `lilygo-t-display-s3` §1 (a 16-row table containing a *"documented separately"* K230 row) | One `## LilyGO` section: the T-Display-S3 table, with the K230 row promoted to a real link, followed by a `### T-Display K230` subsection carrying the K230 fragment's detail and its SKU-collision warning |
| **SX1262 *Used By*** — rows from `m5stack-cardputer` §3.11, `lilygo-k230` §F1, and four already applied by `m5stack-lora-expansions` | Both new subsections appended inside the existing `## 12. Used By`, after the four that were already there. No existing row touched |
| **`semtech/lr2021`** — a new row in both `lora-generations` §1 and `lilygo-k230` §A | Listed once, in the Semtech generations table; the K230 table cross-references it and carries the `DIO11`-not-`DIO1` warning that only matters on that board |
| **`raydium`** — RM69A10 (K230) vs RM67162 / RM690B0 (T-Display-S3) | One `Raydium Semiconductor` row in the merged new-manufacturer table naming all three |
| **`texas-instruments/bq25896`** — new record (K230) and *Used By* target (T-Display-S3) | Listed once as a new record under K230; the T-Display-S3 pass's *Used By* edit noted in that section's trailing list |
| **RadioLib licence** — the same LGPL-3.0 error flagged by `lora-generations` §6.1 and `m5stack-lora-expansions` §5 | One dated correction note in `components/semtech/sx1262/README.md` §9, plus a ⚠ on the new `artifact-manifest.md` row that repeats the claim. Three further occurrences listed in [`corrections-requiring-review.md`](corrections-requiring-review.md) §2 |
| **DinMeter → `vendors/m5stack/README.md` §11** | **Already applied** by the DinMeter session on 2026-09-04; `archive/devices/m5stack/dinmeter/artifacts/research-scratch/vendor-guide-additions.md` is a record of that, not pending content. Verified — §11 exists. No action |
| **`archive/devices/lilygo/t-display-s3-shared/artifacts/research-scratch/vendor-guide-additions.md`** | **Not content.** It is that session's note that no LilyGO guide existed, so it wrote one directly. No action |

## 6. Still outstanding

Fragment content that is real but outside this task's target list. Full table in
[`deferred.md`](deferred.md) §3.

- **`software/README.md`** — entries proposed by six of the seven fragments (CrossPlay/CrossInk,
  M5DinMeter, Bruce, Launcher, Meshtastic, MicroHydra, RadioLib, M5Unit-NFC, TinyGPSPlus, ESPHome,
  Tasmota, MicroPython, WLED, the XuanTie toolchain). **None applied.**
- **`guides/markets/device-comparison-matrix.md` and `clones-and-variants.md`** — ~12 device rows
  and two prose blocks. Marked protected by three sessions independently.
- **`ai-crawler-site-access-table.md`** — access confirmations from three passes, plus **two
  upstream repository renames** worth not losing: `pr3y/Bruce` → `BruceDevices/firmware`, and
  `bmorcelli/M5Stick-Launcher` → `bmorcelli/Launcher`.
- **`vendors/m5stack/README.md`** — the Cardputer pass's nine product ids and its §5.6/§5.7 traps
  are still unapplied; the DinMeter §11 append did not include them.
- **Four vendor guides remain unlinked from `vendors/README.md`**: `dke`,
  `everest-semiconductor`, `omnivision`, `solder-party`. Pre-date these seven passes.

## 7. Source fragments, as read

Hashed at 06:31, before any edit. ⚠ **`lilygo-t-display-s3` was still being written** — see
[`deferred.md`](deferred.md) §4.

| Fragment | SHA-256 | mtime when read |
|---|---|---|
| `xteink/index-fragments.md` | `c204c0906637cff67e55d4e7748287cf1941a50a018cfb4164e9114c6342d3bd` | 2026-09-04 04:21 |
| `m5stack-dinmeter/index-fragments.md` | `aba7399282f65a009ca795c9cb5964de6e8aeafbc8abbf393b4b33c0cbbf9a25` | 2026-09-04 04:22 |
| `m5stack-cardputer/index-fragments.md` | `0b0d9ee2a0ebb8a904a89f5e1e015973cf03b58ed74d92b230f3a2d796023e36` | 2026-09-04 03:41 |
| `m5stack-lora-expansions/index-fragments.md` | `0c35869b5afbaf29d09165d1b38b3f3e1895bb72417cb342b9af1f262e511172` | 2026-09-04 03:28 |
| `lilygo-k230/index-fragments.md` | `6fa7bb16f3d4506efd19afc68d7ee7c329fccda01527035cf2680c59b5fb1c0d` | 2026-09-04 04:39 |
| ⚠ `lilygo-t-display-s3/index-fragments.md` | `2f3acf08c0bca4e60f28062996a05ba3a9f1e744ba7d971148ff55779012e943` | **2026-09-07 06:23 — 4 min before reading** |
| `lora-generations/index-fragments.md` | `132266dde7c315a78994615e1d3677431e1ff16abc80a413153dd81bf7599dc1` | 2026-09-07 06:08 |
| `lilygo-k230/vendor-guide-additions.md` | `3d60da102a5ace935e4a499d875f11623120f8ac5cb72969f11006418f34dfa8` | 2026-09-04 04:06 |
| `lilygo-t-display-s3/vendor-guide-additions.md` | `6f9b72e06e349ba41eedc0207ea1caafce37af848deaf9cf7fc071acdaf8877c` | 2026-09-07 — status note only |
| `m5stack-dinmeter/vendor-guide-additions.md` | `b5156cdf2203de97c61b0c5ec88a93edac9c585aa945bca450a171dd341edd58` | 2026-09-04 04:21 — already applied |

## 8. Evidence boundary

This pass **researched nothing and verified no technical claim**. Every fact now in the indexes
is the originating session's, transcribed and reorganised for house style. Where two sessions
disagreed the disagreement was **preserved and flagged**, never adjudicated — see
[`corrections-requiring-review.md`](corrections-requiring-review.md), which includes one conflict
(§6, TP4057 charge current) that only became visible *because* two sessions' text now sits in one
record.

What this pass did verify, mechanically: that every path it linked exists, that its diff contains
no deletions, and that the git index was untouched.

---
---

# Round two — 2026-09-11

**Run 2026-09-11, 18:50 → 19:40 CDT.** Append-only. No git state was changed.

> **Dating note.** Earlier briefs in this sweep said 2026-09-07 and were **stale** — the host
> clock and the upstream `date:` headers agree on **2026-09-11**. This pass dates its own work
> 2026-09-11 and **did not retro-date anyone else's**; where a round-two session dated itself
> 2026-09-07 (the schematic-tracing census does), that date is left as its author wrote it.

Three further sessions completed and parked fragments in
`scratch/{xteink/index-fragments-round2,schematic-tracing/index-fragments,market-and-certification/index-fragments}.md`.
This pass applied them, landed the Xteink certification work, and decided where 174 FCC exhibits
live.

- **What was deferred, and why** → [`deferred-round2.md`](deferred-round2.md)
- **Corrections** → [`corrections-requiring-review.md`](corrections-requiring-review.md), from `## R0`

## 1. Files edited — 38 files, 2,289 insertions, **0 deletions**

Measured against a byte-exact snapshot taken immediately before each edit, because much of this
tree is untracked and `git diff` is blind to it.

| Target | + | − | What |
|---|---:|---:|---|
| `devices/README.md` | 89 | **0** | Xteink round-two corrections (X4 Classic launch, X4 withdrawal, X4 Light, certification reversal) + a section on the two new per-record file types |
| `components/README.md` | 84 | **0** | Round-two component work: KH3216-A35, five datasheets acquired, the resolved `unidentified/*` records, parts named on sheets with no record |
| `artifact-manifest.md` | 133 | **0** | The 174-exhibit split decision, per-record table, licensing, placeholder contract, open decisions |
| `VERIFICATION-sweep-2026-09-04.md` | 220 | **0** | Round-two section, R1–R8 |
| `VERIFICATION-xteink.md` | 92 | **0** | Corrections C1–C4 |
| `README.md` (root) | 7 | **0** | 1 *Research passes* row, 3 *Quick entry points*, 3 *Verification reports* |
| `guides/README.md` | 3 | **0** | The two new guides + a missing *Research technique* row in the top table |
| `guides/hardware/README.md` | 29 | **0** | Cross-links to the tracing and certification guides |
| `vendors/README.md` | 1 | **0** | The new Xteink row |
| 13 Xteink records | 410 | **0** | Dated certification corrections |
| 4 `market-and-pricing.md` | 133 | **0** | Dated 2026-09-11 pricing |
| 5 `artifacts/certification/README.md` | 103 | **0** | Licensing corrections and orphan notes |
| 5 `acquisition/manifest.json` | 1,044 | **0** | FCC exhibit entries, **inserted textually** after `"artifacts": [` |
| `corrections-requiring-review.md` | 172 | **0** | R0–R8 |

**New files: 174** — 106 placeholders, 21 `artifacts/certification/README.md`, 24 manifests,
5 `certification-and-compliance.md`, `x4-light/market-and-pricing.md`, `vendors/xteink/README.md`,
`deferred-round2.md`, and 6 scripts in this directory.

## 2. ⚠ The prescribed deletion check has a blind spot

The brief specifies `git diff -- <file> | grep -c '^-[^-]'` → must print `0`. **That check cannot
see a deleted Markdown bullet.** A removed `- [foo](bar)` line appears in the diff as
`-- [foo](bar)`, which `^-[^-]` excludes by construction.

It was caught here: `README.md` reports `grep_del=0` but `git diff --numstat` reports **1
deletion**. Use `git diff --numstat` (field 2) as the authority for tracked files.

**The deletion is not this pass's.** It is another session's unstaged replacement of the
*Cross-cutting guides* bullet at line 74, adding `[NFC]` and `[LoRa]` links — the same one round
one documented. Proof, byte-exact:

```
pre-edit snapshot line 74 : 0976573de72594ccbb7bb24b…
current worktree line 74  : 0976573de72594ccbb7bb24b…   identical
git index          line 74: 8aae03fdf078558f499f4b15…   differs
```

The worktree form was already present when this pass first read the file.

## 3. The artifact split

| | Files | Size |
|---|---:|---:|
| Retained in the repository | **59** | **57.80 MiB** |
| Archived + placeholder | **106** | **130.59 MiB** |
| Parked (PaperMono, live) | 11 | 10.27 MiB |
| Not copied — byte-identical to bytes already present | 5 | — |

Repo working tree **617.46 → 657.41 MiB** (+39.95 MiB, +200 files). Archive
**2 558.32 → 2 688.91 MiB** (+130.59 MiB). `.git` untouched.

⚠ **Copied, not moved.** 24 authored records cite `scratch/market-and-certification/fcc/<ID>/`
as their local path, and the method forbids tidying another session's scratch.

## 4. Merges performed

| Overlap | Resolution |
|---|---|
| **X4 Classic pricing** — proposed by the Xteink fragment *and* already written in full by that session into `x4-classic/market-and-pricing.md` | Not duplicated. A short cross-reference records that the certification pass enumerated the same catalogue on the same date and agreed, plus the two facts it added (the `(X4 V2)` store title; six service line-items that are not products) |
| **Certification controls** — the certification fragment references them once; five Xteink records need them | **Reproduced in full in each of the five records**, not referenced. A reader arriving at one device record must be able to judge that record's evidence without chasing a link |
| **`dcdc-u4` = JW5712** — claimed by the certification pass (§6, hash-matched PNG) and the tracing pass (§2, sheet text) | One adjudication note in `components/README.md`, citing both. The `⚠` on the original row is untouched |
| **The certification reversal** — in all three fragments | One correction, applied once per stale claim (13 records) and once per report (2), all pointing at `corrections-requiring-review.md` §R1 |
| **New guides** — tracing proposed by the tracing fragment, certification by the market fragment | Both added to `guides/README.md` in its own two-table format, plus one genuinely missing *Research technique* row in the top table |
| **X4 Pro price USD 99** — round one parked it as unresolved; round two re-observed it | Closed in `x4-pro/market-and-pricing.md`; ⚠ the PaperMono record that contradicts it is **live** and was not edited |

## 5. Scripts, so this is reproducible

| Script | Does |
|---|---|
| [`plan-artifact-split.py`](plan-artifact-split.py) | Parses every `_filing.html`, matches 174 PDFs to their exhibit rows, assigns owners, classifies repo/archive/park → [`plan.json`](plan.json) |
| [`apply-artifact-plan.py`](apply-artifact-plan.py) | Copies and writes the 106 placeholders. Idempotent, never overwrites, `--apply` to execute |
| [`write-cert-records.py`](write-cert-records.py) | Directory READMEs + acquisition manifests |
| [`write-xteink-certification.py`](write-xteink-certification.py) | The five `certification-and-compliance.md` |
| [`write-cert-corrections.py`](write-cert-corrections.py) | The 13 dated corrections. Skips live files and already-corrected files |
| [`verify-round2.py`](verify-round2.py) | Links, magic bytes, orphans, placeholder completeness, counts |

All six default to a dry run.

## 6. Evidence boundary

**This pass researched nothing and verified no technical claim.** Every fact now in the indexes
is an originating session's, transcribed and reorganised. What it verified mechanically: that
every path it linked exists (10,970 links, 1 broken and pre-existing), that its diff contains no
deletions, that all 106 placeholders it wrote carry a hash, a size, an original path and ≥2
distinct URLs, that every copied byte hash-matches its source, and that the git index was
untouched.

It did make **one editorial judgement** the fragments left open: that internal photographs and
ID-label exhibits are worth repository bytes and test reports are not. That is argued in
`artifact-manifest.md` §1 and is reversible from the placeholders.
