# Verification report — preprint and scholarly-literature repositories

Research pass **2026-09-01 → 2026-09-07**. Verification re-probe **2026-09-11**.
All figures below were re-measured on 2026-09-11 against the values recorded in the corpus.

> **Purpose.** This corpus is entirely built on dated, sourced observations of live hosts. Several
> of those hosts are volatile — three changed state *during* the original pass. This report
> re-probes everything volatile, records drift, and **corrects the record where the original
> finding no longer holds.**

## Inventory

| Metric | Value |
|---|---|
| Records in `research/preprint-repositories/` | **40** Markdown documents |
| Total lines | **~22,900** |
| Wikipedia-list entries covered | **78 / 78** (verified by name search) |
| Landmark identifiers individually verified | **160** (79 arXiv · 41 ePrint · 26 theses · 14 HAL) |
| Broken relative links | **0** |
| Broken heading anchors | **0** |
| `[NOT-VERIFIED]` flags | **221** — each naming what was tried |
| Files staged in git index by this pass | **0** |
| Raw probe evidence retained | **234 MB** in `scratch/preprint-repositories/` |

## Automated checks

| Check | Result |
|---|---|
| Broken relative Markdown links | ✅ **0** |
| Broken heading anchors (GitHub slug rules) | ✅ **0** |
| Wikipedia-list coverage (78 names) | ✅ **0 missing** |
| Landmark PDF magic bytes (Berkeley set) | ✅ 6/6 `%PDF-` |
| Torvalds thesis digest vs Wayback | ✅ **identical** (`ZVCIUY5JU6PJW3CN37K277F2Z4HLXYPV`) |
| Staged deletions/additions from this pass | ✅ **0** (unrelated concurrent Nix work is staged; left untouched) |

---

## 1. Corrections — findings that no longer hold

### 1.1 ⚠ Berkeley EECS is **restored**. The "went dark" finding was a migration transient.

**This was a headline claim and it is now wrong.** The original pass found
`www2.eecs.berkeley.edu/Pubs/TechRpts/*` 302-redirecting to `iris.eecs.berkeley.edu`, which served
a themed 404 for every path.

On 2026-09-11 the series is **back on its original host, at a new `/Archive/` path segment**:

```
https://www2.eecs.berkeley.edu/Pubs/TechRpts/<year>/Archive/<report>.pdf
```

All six RISC-V reports re-verified, HTTP 200, `%PDF-` magic:

| Report | Bytes | Note |
|---|---|---|
| UCB/EECS-2011-62 | 376,630 | matches the size recorded pre-outage |
| UCB/EECS-2011-63 | 472,741 | |
| UCB/EECS-2014-54 | 847,494 | |
| **UCB/EECS-2016-1** | **959,927** | **exactly** the pre-outage size *and* the Wayback capture size |
| UCB/EECS-2016-118 | 777,931 | |
| UCB/EECS-2016-161 | 625,668 | |

The TR index is also back (HTTP 200, 122,784 B). `iris.eecs.berkeley.edu` still serves the
58,829-byte themed 404 — confirmed by negative control — so that host was a staging artefact of a
migration in progress, not a new home.

**What this changes:** the durability alarm was overstated. What it does *not* change is the
lesson — for roughly three weeks the canonical RISC-V specifications were unreachable at every
published URL, and only Wayback had them. The corrected reading is *"URLs moved, content was never
lost"*, which is the same conclusion the corpus reaches everywhere else.

### 1.2 Anubis returns **HTTP 200**, not 403. Reclassified.

The corpus recorded Anubis proof-of-work walls as a ~4.6 kB **403** fingerprint. **That is wrong.**
Re-probed with body inspection:

| Host | Code | Bytes | `<title>` |
|---|---|---|---|
| `rcaap.pt` | **200** | 4,511 | *Making sure you're not a bot!* |
| `portal.dnb.de` | **200** | 4,475 | *Making sure you're not a bot!* |
| `base-search.net` | **200** | 7,846 | *Making sure you're not a bot!* |
| `scipost.org` | **200** | 3,903 | *Making sure you're not a bot!* |
| `helda.helsinki.fi` | **200** | 2,123 | *Oh noes!* (Anubis error page) |

**Anubis belongs in the soft-200 trap category, not the 403-fingerprint table** — it is strictly
more dangerous than a 403, because a status-code check reads it as success. The reliable
discriminator is the title string, not the byte size.

### 1.3 Two hosts are no longer walled

- **`cds.cern.ch`** — HTTP 200, **41,946 B**, `<title>CERN Document Server</title>`. A real page.
  The corpus records it as "HTML and REST behind Anubis"; that is no longer true.
- **`research-collection.ethz.ch`** — HTTP 200, 782 B real page. The 1,337-byte custom 403 is gone,
  **confirming the original finding that ETH's block is IP/provider-scoped rather than UA-scoped.**

### 1.4 OpenReview's API block was transient

`api2.openreview.net/groups?id=venues` answers again: **4,653 venues** (recorded 4,634, +19). The
`ChallengeRequiredError` that defeated six user agents during the original pass has lifted. The
recorded venue figure is confirmed; the per-venue submission counts remain `[NOT-VERIFIED]` because
of the `10000` cap documented in `additional-preprint-servers.md`.

### 1.5 CogPrints' recovery route has degraded

The corpus records that CogPrints fails over HTTPS (TLS SAN mismatch) but that **plain HTTP 301s to
Southampton's archive and returns 200**. On 2026-09-11 that redirect now lands on **HTTP 401**
(7,493 B) — the Southampton BotStopper wall documented elsewhere in the corpus has been extended to
the archive path. **The documented recovery route no longer works for scripted clients.**

### 1.6 ⚠ Dating error in the theses record

`theses-and-dissertations.md` is stamped **2026-09-04** throughout. Its actual write time is
**2026-09-07** (filesystem mtime), because a stale "today" was carried forward into the research
brief. Its server-supplied dates (e.g. the EThOS ResourceSync `at=2026-09-06`) are genuine.

**Read every `2026-09-04` in that file as "2026-09-06/07".** The dates in all other records match
their mtimes and are correct. Not silently rewritten, because the exact probe date per claim cannot
be reconstructed and false precision would be worse than a flagged approximation.

---

## 2. Confirmed unchanged

Re-probed 2026-09-11; all matched the recorded values.

| Finding | Recorded | Now |
|---|---|---|
| NDLTD Global ETD Search dead | 503, 505 B | ✅ 503, 505 B |
| DART-Europe closed | closed 2025-02-03 | ✅ redirects to UCL closure notice |
| OATD blocks all clients | 403 Cloudflare | ✅ 403 (5,442 B; `robots.txt` 5,493 B) |
| EThOS metadata-only | 200, 62,214 B | ✅ 200, 62,214 B |
| EThOS bogus-`uin` trap | 200 + home page | ✅ reproduces exactly |
| `bodoarxiv.org` is a casino | 200 | ✅ 200, 83,368 B |
| `lawarxiv.org` parking stub | 114 B | ✅ 114 B |
| `mediarxiv.org` stranger's redirect | → unrelated site | ✅ → `afterdispatch.com` |
| `frenxiv.org` frozen zombie | 200 | ✅ 200, 44,186 B |
| `latarxiv` · `inarxiv.id` · `marxiv` · `nutrixiv` · `africarxiv.ubuntunet` · `rinarxiv` | dead / TLS-broken | ✅ all `000` |
| `hpl.hp.com` TCP-dead | timeout | ✅ timeout |
| CiteSeerX dead | 301 → fixed Wayback ts | ✅ `20251230112235` |
| Cloudflare 5.6 kB family | 5,583–5,623 B | ✅ techrxiv 5,620 · authorea 5,620 · chemrxiv 5,595 · scienceopen 5,602 · essopenarchive 5,622 · advance 5,623 · **ssrn 5,731** |
| `preprints.org` minimal 403 | 369 B | ✅ 369 B |
| CORE theses | 7,921,188 | ✅ **7,921,188** — exact |

**`synthical.com` is still TCP-unreachable**, ten days after first observation. The corpus
deliberately recorded it as *unreachable*, not *defunct*, on the grounds that one host on one day
proves nothing. Three observations across ten days now support the stronger reading, but the record
is left as-is — that caution was correct and the distinction still matters.

---

## 3. Growth — confirms the records

Drift consistent with ordinary accumulation over 7–10 days. No record needs changing.

| Metric | Recorded | 2026-09-11 | Δ |
|---|---|---|---|
| Zenodo records | 7,231,589 | **7,267,019** | +35,430 |
| arXiv `cs.AR` | 8,932 | **9,019** | +87 |
| bioRxiv `count_new_papers` | 347,954 | **348,506** | +552 |
| ECCC newest report | TR26-163 | **TR26-173** | +10 |
| OpenReview venues | 4,634 | **4,653** | +19 |

### A methodology check that vindicated the record

An initial re-probe read bioRxiv at **479,561** against a recorded 347,954 — an apparent 38%
discrepancy. It was not drift. The bioRxiv API exposes **both** `total` (479,561, counting every
version) and `count_new_papers` (348,506, distinct preprints). **The original record used the
correct field; the verification query used the wrong one.**

Worth propagating as a trap: `api.biorxiv.org` returns two plausible totals in the same object, and
the obvious one is wrong for counting preprints.

---

## 4. Open items closed

| Item | Resolution |
|---|---|
| **Stanford CS/CSL technical-report index** — the last unchecked archival candidate | **CLOSED.** Live at HTTP 200 / **1,332 B** (matching the recorded size) **and archived** — CDX shows `i.stanford.edu/TR/` captured `20241119002302`, with individual report pages back to 2015. No submission needed |
| **Torvalds thesis "unarchived"** | **CLOSED — the original alarm was false.** Continuously archived 2018-05-11 → 2026-08-07, digest identical to the live file. Cause: `archive.org/wayback/available` returns false negatives (see below) |
| **Berkeley series unreachable** | **CLOSED** — restored at `/Archive/`, §1.1 |

---

## 5. Standing methodological findings

Produced or hardened by this verification pass; all are in
[`retrieval-notes.md`](retrieval-notes.md).

1. **`archive.org/wayback/available` returns false negatives.** It reported no captures for a URL
   CDX shows continuously archived since 2018. It fails *toward* phantom link rot. **Confirm absence
   with the CDX API.**
2. **The CDX `length` field is the WARC record length, not the payload size.** Compare the `digest`
   (base32 SHA-1) against a local file instead — done here for the Torvalds thesis.
3. **Anubis answers HTTP 200.** Detect it by `<title>Making sure you're not a bot!</title>`.
4. **`hdl.handle.net/api/handles/<prefix>/<suffix>`** is the best existence oracle found — served by
   the Handle System, so it works straight through the target's bot wall.
5. **Follow redirects when probing APIs.** `zenodo.org/api/*` and `export.arxiv.org` over HTTP both
   301; omitting `-L` yields empty bodies that look like blocks. Two false "rate-limited"
   conclusions in this pass traced to exactly that.
6. **Empty or wildcard queries mean "nothing", not "everything"** on NTRS, OSTI **and** CiNii —
   three independent implementations.

---

## 6. Not re-derived

Honest gaps in this verification, not in the original records.

- **Cryptology ePrint total** (27,552) — the per-year page structure defeated a quick scrape; not
  re-derived. The original figure was cross-checked five independent ways at the time.
- **OSF Preprints total** (200,519) — `api.osf.io` timed out on three attempts.
- **arXiv `cs.DC`, `cs.OS`** — arXiv's one-request-per-three-seconds limit; probing stopped rather
  than pushed, consistent with this corpus's own guidance.
- ~~**`ai-crawler-site-access-table.md` merge**~~ — **DONE 2026-09-20.** Merged as a new
  *Scholarly / preprint / archival* section, seven *General retrieval tips* additions, and a dated
  correction to that file's existing `archive.org/wayback/available` advice, which this pass
  disproved. Append-only; concurrent unstaged work in that file was preserved.

---

## 7. Verdict

**The corpus survives verification.** Of ~40 volatile findings re-probed, **five required
correction** (§1) and **one dating error** was found and flagged. Everything else either matched
exactly or drifted by an amount consistent with normal accumulation.

The two most consequential corrections — Berkeley restored, and Anubis returning 200 — both make
the corpus *more* accurate about the thing it is actually measuring: **content is rarely lost;
addresses and access paths change constantly, and status codes lie.**
