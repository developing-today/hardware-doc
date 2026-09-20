# Additional preprint servers — what Wikipedia's list leaves out

- **Compiled:** 2026-09-02. Every figure below was measured on that date unless stated otherwise.
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).
- **Scope:** repositories, overlay platforms and open-review venues that are **absent from**
  [Wikipedia's *List of preprint repositories*][wp] but that a working engineer will hit anyway.

[wp]: https://en.wikipedia.org/wiki/List_of_preprint_repositories

---

## Premise

**Wikipedia's list has significant omissions, and several of them matter more to computing than
most of the entries it does include.**

The list's composition is not random. It over-represents two things:

1. **COS/OSF-branded servers.** A large block of its entries are OSF Preprints providers —
   SocArXiv, PsyArXiv, EdArXiv, MetaArXiv, MindRxiv, PaleorXiv, MarXiv, NutriXiv, SportRxiv,
   LawArXiv, BodoArXiv, Frenxiv, AfricArXiv, Arabixiv, IndiaRxiv, INArxiv, LatArXiv, EcoEvoRxiv,
   BioHackrXiv, ECSarXiv, engrXiv, agriRxiv and more. Eighteen of the thirty-two OSF providers are
   **closed to new submissions** (see [`osf-preprints.md`](osf-preprints.md)), yet each still gets a
   line of its own. The `-Xiv`/`-Rxiv` naming convention is doing a lot of the work of *looking
   like* a category.
2. **Life sciences and social sciences.** bioRxiv, medRxiv, F1000Research and its five funder
   clones, PeerJ Preprints, Lancet, Cell Sneak Peek, JMIR, ARPHA, Beilstein, agriRxiv, NutriXiv,
   Nature Precedings.

What it under-represents is **computing**. arXiv, Cryptology ePrint and TechRxiv are on the list.
The following are not, and every one of them is a place where computing research is *first*
published, permanently archived, or bulk-retrievable:

| Omission | Why it matters | Section |
|---|---|---|
| **ECCC** | The theoretical-CS analogue of Cryptology ePrint. Running since 1994. **4,832** reports. Reingold's `SL=L`, Dinur's PCP proof, Williams's ACC lower bound all landed here first | [§1](#1-eccc--electronic-colloquium-on-computational-complexity) |
| **OpenReview** | Where ICLR and NeurIPS actually run peer review, in public. Submissions, reviews, rebuttals, scores and decisions are all fetchable | [§2](#2-openreview) |
| **ACL Anthology** | Every ACL/EMNLP/NAACL/COLING paper since 1979, free full text, no paywall, bulk BibTeX | [§3](#3-acl-anthology) |
| **CERN Document Server** / **INSPIRE-HEP** | Detector electronics, FPGA triggers, radiation-hard ASICs, CERN technical reports and theses that exist nowhere else | [§4](#4-cern-document-server-and-inspire-hep) |
| **dblp** | Metadata only, but *the* canonical CS bibliography, with a full XML dump | [§14](#14-overlays-indexes-and-one-shutdown) |

A defensible reading is that the list is a **library-science artifact**: it enumerates things that
self-identify as "preprint repositories" and were catalogued as such. ECCC calls itself a
*colloquium*, OpenReview calls itself a *review platform*, the ACL Anthology calls itself an
*anthology*, CDS calls itself a *document server*, and dblp calls itself a *bibliography*. None of
them applied for the label. All of them are, functionally, where you go to read the paper before or
instead of paying a publisher. [INF]

This record documents them to the same standard as the rest of this directory. Where a claim could
not be checked it says so.

---

## Note on dates

The bulk harvest behind this record was taken on **2026-09-02**. Every figure that this record
leans on was **re-verified with a fresh live query on 2026-09-04**. Where the two passes disagree,
both are given — the disagreements are small and are themselves evidence that the server is live.

---

# TIER 1 — the major computing omissions

## 1. ECCC — Electronic Colloquium on Computational Complexity

- **URL:** https://eccc.weizmann.ac.il/
- **Operator:** Weizmann Institute of Science, "under the auspices of the Computational Complexity
  Foundation (CCF)" [WEB, masthead on every page, 2026-09-04]
- **Editor-in-chief:** Oded Goldreich [WEB, `/colloquium/scientific_board/`, 2026-09-04]
- **ISSN:** 1433-8092 [WEB, page footer, 2026-09-04]
- **Discipline scope:** computational complexity theory, strictly
- **Launched:** 1994 · **Status:** active — 163 reports posted in 2026 alone
- **On Wikipedia's list:** **no.** Not under ECCC, not under "Electronic Colloquium", not under
  Weizmann.

### 1.1 What it is

ECCC is what Cryptology ePrint is to cryptography, for computational complexity: the place a
complexity theorist posts a result the week it is finished, months to years before a conference or
journal version exists. It has been doing this continuously since **December 1994**, which makes it
older than every server on Wikipedia's list except arXiv (1991) and SSRN (1994).

It is *not* a general-purpose preprint server and does not want to be. Its call for papers demands
submissions with "relevance to computational complexity, clear mathematical profile, and strictly
mathematical format", and requires that a submission "be in scope, look somewhat new and
interesting, **contain all proofs**, and be in a readable form" [DOC,
`https://eccc.weizmann.ac.il/colloquium/call_for_papers/`, 2026-09-04]. The "contain all proofs"
clause is the important one: an ECCC report is expected to be a *complete* technical report, not an
extended abstract. This is the opposite of the conference culture the same community operates in.

The institutional history is documented in the scholarly literature by its own founders. ECCC began
at the University of Trier under Christoph Meinel; the operator's own reading list cites Bern, Damm
& Meinel, *"The Electronic Colloquium on Computational Complexity (ECCC): A Digital Library in
Use"*, ECDL 1997, pp. 405–421; Bern, Meinel & Sack, *"Electronic colloquia: idea and practice"*,
ACM SIGDOC 1998, pp. 113–119; and Meinel & Klotz, *"The first 10 years of the ECCC digital
library"*, **Communications of the ACM 49(1):131–134, 2006** [DOC,
`https://eccc.weizmann.ac.il/static/colloquium/read_more/`, 2026-09-04]. It is now hosted at
Weizmann. Two retrospective PDFs are served from the site itself:
`/resources/pdf/eccc_10_years.pdf` and `/resources/pdf/eccc_digital_library.pdf` [WEB, links
present in the homepage HTML, 2026-09-02].

### 1.2 Identifiers — `TRYY-NNN`

Every report gets an identifier of the form **`TRYY-NNN`**: `TR` for *technical report*, a
two-digit year, a hyphen, and a **three-digit sequence number within that year**, zero-padded,
starting at `001`. `TR94-001` is the first report ever posted. `TR26-163` is the 163rd of 2026.

The canonical URL rewrites the identifier into a path with the **four-digit** year:

```
TR04-094  ->  https://eccc.weizmann.ac.il/report/2004/094/
TR94-001  ->  https://eccc.weizmann.ac.il/report/1994/001/
```

The PDF hangs off the same path: `https://eccc.weizmann.ac.il/report/2004/094/download/` returns
`application/pdf`, 187,575 bytes, PDF 1.2, 19 pages [API/probe, 2026-09-04]. Note the trailing
slash — without it a `HEAD` returns HTTP 200 with `Content-Length: 0`, which will silently defeat a
size-based existence check.

There is **no DOI**. No report page inspected in this pass carried one, and there is no Crossref or
DataCite registration visible for ECCC content. Citations to ECCC are by `TRYY-NNN` and URL only.
[INF from WEB inspection of eleven report pages, 2026-09-04] — the negative is asserted only for
the pages actually inspected.

### 1.3 Size and growth — per-year counts

Counted by extracting unique `TRYY-NNN` identifiers from each year index page
(`https://eccc.weizmann.ac.il/year/<YYYY>/`). Harvest 2026-09-02; 2026 re-verified live 2026-09-04.

| Year | Reports | Year | Reports | Year | Reports |
|---:|---:|---:|---:|---:|---:|
| 1994 | 27 | 2005 | 163 | 2016 | 206 |
| 1995 | 62 | 2006 | 160 | 2017 | 193 |
| 1996 | 66 | 2007 | 137 | 2018 | 213 |
| 1997 | 58 | 2008 | 110 | 2019 | 187 |
| 1998 | 76 | 2009 | 148 | 2020 | 193 |
| 1999 | 48 | 2010 | 203 | 2021 | 182 |
| 2000 | 91 | 2011 | 175 | 2022 | 186 |
| 2001 | 103 | 2012 | 186 | 2023 | 213 |
| 2002 | 74 | 2013 | 191 | 2024 | 202 |
| 2003 | 87 | 2014 | 184 | 2025 | 215 |
| 2004 | 121 | 2015 | 209 | **2026 (part)** | **163** |

- **Total 1994 – 2026-09-04: 4,832 reports** [API/probe — 33 year-index pages parsed, 2026-09-02;
  2026 re-verified live 2026-09-04]
- The 2026-09-02 harvest gave **162** for 2026 and a total of **4,831**. The 2026-09-04 re-probe
  gives **163** and **4,832**. One report was posted in between. Both figures are recorded rather
  than reconciled.
- **Shape of the curve:** ~27 in the first (partial) year, crossing 100/yr in 2001, crossing 200/yr
  in 2010, and then **flat at roughly 180–215 reports a year for fifteen straight years**. ECCC is
  not growing. That is a real and slightly unusual finding: almost every other server in this
  survey shows compounding growth. [INF from the table above]
- 2025's **215** is the highest annual figure in the archive's history, by two reports over 2018's
  and 2023's 213.

For scale: **4,832 reports in 32 years** against Cryptology ePrint's **27,552** in 27 years
(see [`cryptology-eprint-archive.md`](cryptology-eprint-archive.md)) and arXiv's `cs` at
**931,100** (see [`arxiv.md`](arxiv.md)). ECCC is *small on purpose*. It is a filter, not a firehose.

### 1.4 The editorial gate — what does not get in

This is the sharpest difference from arXiv and from every OSF-branded server on Wikipedia's list.
ECCC screens **editorially**, not for plausibility, and it says so in writing.

Published criteria [DOC, `/colloquium/call_for_papers/`, 2026-09-04]:

> To be posted on ECCC, a submission should meet the following criteria: be in scope (see below),
> look somewhat new and interesting, contain all proofs, and be in a readable form.

And, in a sentence with no analogue on any other server in this survey:

> **Submissions claiming to resolve a grand challenge, such as the P vs. NP problem, may be
> rejected without further consideration.**

That single line is why ECCC does not have a viXra problem. It is an explicit, published, prior
refusal to spend reviewer attention on the highest-volume category of crank submission in the
field. Compare [`vixra.md`](vixra.md), where the same category is the *house speciality*.

The scope statement is likewise narrowing rather than welcoming. It lists sixteen topics
— algebraic and arithmetic complexity; average-case complexity; circuit complexity; coding theory
*(complexity aspects only)*; communication complexity; cryptography *(complexity aspects only)*;
data structure lower bounds; game theory *(complexity aspects only)*; inapproximability;
interactive and probabilistic proof systems; Kolmogorov complexity; learning *(complexity aspects
only)*; proof complexity; property testing *(complexity aspects only)*; pseudorandomness and
derandomization; quantum computation *(complexity aspects only)*; structural complexity — and then
excludes most of algorithms research outright:

> typically, **algorithmic improvements are not in scope of ECCC**, except in cases where either
> the improved complexity bounds are closely related to a conjectured lower bound or the techniques
> are of natural interest to complexity-theoretic studies.

The gate is staffed by a **named scientific board of ~60 researchers** with public email addresses,
Oded Goldreich as editor-in-chief. The list includes Scott Aaronson, Noga Alon, Boaz Barak, Paul
Beame, Irit Dinur, Venkatesan Guruswami, Johan Håstad, Yuval Ishai, Subhash Khot, Kurt Mehlhorn,
Christoph Meinel, Ryan O'Donnell, Toniann Pitassi, Ran Raz, Alexander Razborov, Oded Regev, Omer
Reingold, Peter Shor, Madhu Sudan, Salil Vadhan, Virginia Vassilevska Williams and others [WEB,
`/colloquium/scientific_board/`, 2026-09-04]. **The rejection rate is not published** —
[NOT-VERIFIED]; no figure was found on the site or in the cited literature.

There is a **registration requirement**: submission is by registered author account only, with
name, email and affiliation, and email activation. Submitted files must be PDF. Abstracts accept
LaTeX and are rendered to MathML [DOC, `/static/colloquium/how_to_use/`, 2026-09-04].

### 1.5 Revision and comment semantics — the part that matters for citing

ECCC's versioning model is materially different from arXiv's and is the reason an ECCC citation
needs care.

- **A report is never removed.** The operator's own words: *"once a report has been posted on ECCC
  its record cannot be removed"* [DOC, `/static/colloquium/how_to_use/`, 2026-09-04]. There is no
  withdrawal mechanism at all.
- **Withdrawal is performed by revision, not deletion.** *"the authors may withdraw its claims by
  posting a revision with the adequate contents. It is recommended to write a short description
  that details which parts of the original report are withdrawn and which remain valid, and the
  reasons for the withdrawal."* [DOC, same source] **Consequence: a retracted ECCC result looks
  exactly like a live one at the identifier level.** You must open the report page and read the
  revision list. `TRYY-NNN` alone tells you nothing about whether the claim still stands.
- **Revisions are numbered and separately dated**, and the report page presents the *latest*
  revision by default while retaining the original. `TR05-046` (Dinur, PCP by gap amplification)
  displays as *"Revision #1 to TR05-046, 26th September 2005"* with the base report of 2005 still
  present [WEB, 2026-09-04]. `TR15-119` (Chattopadhyay–Zuckerman) is on **Revision #5, accepted 11
  February 2019** — nearly four years after the original posting [WEB, 2026-09-04]. Citing
  "TR15-119" without a revision number is ambiguous across a four-year span.
- **Comments are a first-class object.** ECCC advertises *"the feature of an ongoing public
  scientific discussion. Corrections, improvements, remarks etc. concerning an existing report"*
  [DOC, `/colloquium/call_for_papers/`, 2026-09-04]. `TR05-046` carries **six** comment blocks
  alongside its revisions [WEB, 2026-09-04]. This is post-publication review, in public, twenty
  years before the term was fashionable — and it long predates OpenReview (§2).
- **There is a caveat in the copyright notice that cuts the other way:** *"The author may withdraw
  the paper from the digital library of ECCC iff the paper is accepted for publication elsewhere.
  In particular, it is the responsibility of the author to do this if he/she signs a copyright
  agreement which does not allow electronic distribution by ECCC"* [DOC,
  `/static/colloquium/copyright_notice/`, 2026-09-04]. This **directly contradicts** the "cannot be
  removed" statement in the how-to-use page. Both are live on the site on the same date. Recorded
  as a conflict, not resolved. [WEB ×2, 2026-09-04]

Every report page also shows a **public download counter** — `TR04-094` reads 11,435 downloads,
`TR94-010` reads 10,511, `TR94-001` reads 4,803 [WEB, 2026-09-04]. No other server in this survey
exposes per-item usage this plainly. Treat it as an unaudited operator-supplied number, not a
metric.

### 1.6 Landmark results, with verified identifiers

Every row below was fetched individually on **2026-09-04** and the title and author list read off
the live report page. Rows that could not be confirmed were dropped (see the note after the table).

| Paper | Identifier | Posted | Authors (as shown on ECCC) | Why it matters | Preprint first? |
|---|---|---|---|---|---|
| On Rank vs. Communication Complexity | **TR94-001** | 1994-12-12 | Noam Nisan, Avi Wigderson | The first report in the archive. Log-rank conjecture gap | Yes — ECCC's report #1 |
| Natural Proofs | **TR94-010** | 1994-12-12 | Alexander Razborov, Steven Rudich | *The* barrier result: why the circuit-lower-bound programme stalled. Gödel Prize 2007 | ECCC copy contemporaneous with STOC'94/JCSS'97 |
| Entropy Waves, the Zig-Zag Graph Product, and New Constant-Degree Expanders and Extractors | **TR01-018** | 2001-02-23 | Omer Reingold, Salil Vadhan, Avi Wigderson | The zig-zag product. Gödel Prize 2009. Underpins modern expander and extractor constructions | Yes — Feb 2001, before FOCS'00/Annals 2002 print |
| Undirected ST-Connectivity in Log-Space | **TR04-094** | 2004-11-10 | Omer Reingold | **SL = L.** Gödel Prize 2009. One of the cleanest derandomization results ever proved | Yes — Nov 2004, before STOC'05 |
| The PCP Theorem by gap amplification | **TR05-046** | 2005 (Rev #1 2005-09-26) | Irit Dinur | The combinatorial reproof of the PCP theorem. Gödel Prize 2019 | Yes — ECCC, then STOC'06/JACM 2007 |
| Optimal Inapproximability Results for MAX-CUT and Other 2-Variable CSPs? | **TR05-101** | 2005-09-20 | Guy Kindler, Ryan O'Donnell, Subhash Khot, Elchanan Mossel | Unique Games ⇒ Goemans–Williamson is optimal for MAX-CUT. Gödel Prize 2018 | ECCC copy Sept 2005; FOCS'04 preceded it |
| Delegating Computation: Interactive Proofs for Muggles | **TR17-108** | 2017 (Rev #1 2017-12-24) | Shafi Goldwasser, Yael Tauman Kalai, Guy Rothblum | **GKR.** The doubly-efficient interactive proof that verifiable-computation and zk-rollup systems are built on | ECCC copy postdates STOC'08; this is the canonical open full version |
| Pseudorandom Sets in Grassmann Graph have Near-Perfect Expansion | **TR18-006** | 2018 (Rev #2 2018-05-19) | Subhash Khot, Dor Minzer, Muli Safra | Completed the proof of the **2-to-2 Games Theorem** | Yes — ECCC first |
| Explicit Two-Source Extractors and Resilient Functions | **TR15-119** | 2015 (Rev #5 2019-02-11) | Eshan Chattopadhyay, David Zuckerman | Two-source extraction at polylog min-entropy — a 30-year open problem. Directly relevant to hardware RNG post-processing | Yes — ECCC, then STOC'16/Annals |
| Locally testable codes via high-dimensional expanders | **TR20-072** | 2020-05-05 | Yotam Dikstein, Irit Dinur, Prahladh Harsha, Noga Ron-Zewi | On the road to c³-LTCs; the coding-theory side of HDX | Yes |
| A VLSI Circuit Model Accounting For Wire Delay | **TR23-186** | 2023-11-28 | Ce Jin, Ryan Williams, Nathaniel Young | Keywords: *circuit complexity, systolic arrays, VLSI, wire delay*. The closest thing to hardware on ECCC | Yes |

**Explicitly not claimed.** Ryan Williams's *"Non-Uniform ACC Circuit Lower Bounds"* (CCC 2011,
JACM 2014) is frequently assumed to be an ECCC report. **It is not one** — a title scan across all
33 year-index pages found no matching entry. What *does* exist is **TR11-017**, *"NEXP does not
have non-uniform quasi-polynomial-size ACC circuits of o(loglog n) depth"* by **Fengming Wang**, a
different paper by a different author [WEB, 2026-09-04]. This is exactly the kind of error the
"landmark papers must resolve" rule exists to catch.

### 1.7 What an engineer actually finds there

ECCC is a lower-bounds archive, and lower bounds are about what hardware *cannot* be made to do.
Concretely useful strands, all present in the harvested year indexes:

- **Randomness extraction** — TR15-119, TR16-088, TR21-075, TR24-176 and dozens more. This is the
  theory under TRNG post-processing: how much entropy you can extract from a biased, correlated
  physical noise source. If you are designing a ring-oscillator RNG, the extractor literature here
  is the thing that tells you whether your conditioning is sound.
- **Circuit complexity and VLSI** — TR23-186 explicitly models wire delay and systolic arrays;
  TR21-023 gives `3.1n − o(n)` circuit lower bounds for explicit functions.
- **Expander graphs** — TR01-018, TR23-089 (*New Explicit Constant-Degree Lossless Expanders*),
  TR23-160. Expanders are the construction behind LDPC-adjacent codes and interconnect topologies.
- **Error-correcting and locally testable codes** — TR20-072, TR23-127, TR25-132 (*Time and Space
  Efficient Deterministic List Decoding*), TR25-170 (Reed–Solomon list decoding).
- **Interactive proofs / verifiable computation** — TR17-108 (GKR), TR17-102 (RRR overview),
  TR22-014. This is the theory layer under zk-SNARK and rollup engineering.
- **Matrix multiplication** — TR14-154 (*Fast Matrix Multiplication: Limitations of the Laser
  Method*), TR20-029, TR20-030 (*Barriers for Rectangular Matrix Multiplication*), TR25-031 and
  TR25-066 on error-correcting matrix-multiplication algorithms.
- **Communication complexity** — the whole TR94-001 lineage. This is where distributed-system and
  memory-hierarchy lower bounds come from.

What you will **not** find: systems papers, measurement studies, algorithm engineering, benchmarks,
anything with an implementation section. The scope statement excludes them by design (§1.4).

### 1.8 Access, APIs and bulk retrieval

| Facility | Status | Evidence |
|---|---|---|
| Year index `/year/<YYYY>/` | **Works.** Full list of that year's reports with titles and authors, one HTML page. This is the practical bulk-harvest route | [probe] HTTP 200, 159,555 B for 2026, 2026-09-04 |
| Report page `/report/<YYYY>/<NNN>/` | Works. Title, authors, date, keywords, abstract, revisions, comments, download count | [probe] 2026-09-04 |
| PDF `/report/<YYYY>/<NNN>/download/` | Works, `application/pdf`. **Trailing slash required** | [probe] 187,575 B for TR04-094, 2026-09-04 |
| RSS `/feeds/reports/` | **Works.** `application/rss+xml`, 13,841 B, latest reports | [probe] 2026-09-04 |
| RSS `/feeds/latestReports` | Linked from homepage | [WEB] 2026-09-02 |
| Keyword index `/keywords/` | Works — **382 distinct keyword pages** under `/keyword/<id>` | [probe] 45,380 B, 2026-09-04 |
| **OAI-PMH** | **Absent.** `/oai2d?verb=Identify` returns the soft-404 body | [probe] 2026-09-04 |
| **REST/JSON API** | **None found.** [NOT-VERIFIED] — no documented API endpoint located | 2026-09-04 |
| **Bulk dump** | **None found.** [NOT-VERIFIED] | 2026-09-04 |
| `robots.txt` | Disallows `/submit/paper/`, `/search`, `/password`, `/register`. **`/report/`, `/year/` and `/keyword/` are not disallowed** | [probe] 97 B, 2026-09-04 |
| Bot blocking | **None observed.** Plain `curl` with a default UA succeeded throughout. No Cloudflare, no Anubis, no rate limiting hit at ~35 requests | [probe] 2026-09-02 and 2026-09-04 |

**Probing trap — ECCC serves HTTP 200 for things that do not exist.** This is the most important
operational finding in this section, and it will corrupt any harvest that trusts status codes:

| Request | HTTP | Bytes | Reality |
|---|---:|---:|---|
| `/year/2026/` | 200 | 159,555 | Real, 163 reports |
| `/year/2099/` | **200** | **17,032** | **Does not exist** — empty year shell |
| `/year/1900/` | 200 | 17,032 | Does not exist — byte-identical to 2099 |
| `/report/1994/001/` | 200 | 19,714 | Real (Nisan–Wigderson) |
| `/report/1994/999/` | **200** | **17,041** | **Does not exist** |
| `/about/`, `/faq/`, `/imprint/`, `/oai2d?verb=Identify` | **200** | **17,041** | All soft-404s |

The 17,041-byte body renders the literal text *"404 page not found — The page you requested is not
available!"* while returning HTTP 200. The 17,032-byte body is the empty-year variant. **Use body
size or a title-string check, never the status code.** This is the same class of trap as
`osf.io`'s 4,207-byte SPA shell and `unpaywall.org`'s 1,421-byte shell, and it is worth adding to
the index's [§ Probing traps](README.md#6-probing-traps).

### 1.9 Licensing and reuse — the restrictive surprise

ECCC does **not** use Creative Commons. Its copyright notice [DOC,
`/static/colloquium/copyright_notice/`, 2026-09-04] states:

- *"There is no copyright transfere from the Author to the Colloquium... all rights are held by the
  authors, their institutions, or their designees."*
- *"use of the ECCC reports for commercial purpose is strictly forbidden; no one may sell copies of
  reports without explicitely written permission of the copyright holders."*
- *"Access to ECCC reports is limited to **interactive viewing and/or printing for personal
  use**."*

Read literally, that last clause forbids bulk text mining and forbids redistribution — a
**stricter** licence than arXiv's default and far stricter than the CC-BY that most servers on
Wikipedia's list default to. The metadata is open in practice (no `robots.txt` block on `/report/`)
but the full texts are not licensed for corpus construction. Anyone building an LLM training set or
a citation corpus from ECCC PDFs should read that sentence first. [DOC, 2026-09-04]

### 1.10 Reliability — what a `TRYY-NNN` actually guarantees

**What it does guarantee:** a dated timestamp; a stable URL that has survived an institutional move
from Trier to Weizmann; that a named board with a published scope statement let it through; that
the document contains complete proofs *as claimed by the author*; and that the record can be found
forever, because nothing is deleted.

**What it does not guarantee:** correctness. ECCC screening is a **scope-and-seriousness gate, not
peer review.** No referee verifies the proofs. The eventual-publication rate is **[NOT-VERIFIED]**
— no measurement was found in the literature or on the site, and this pass did not sample for one.

**How to sanity-check an individual ECCC report:**

1. Open the report page and **read the revision list**. A late revision usually means an error was
   found. Withdrawals are performed *as* revisions (§1.5).
2. **Read the comments.** ECCC comments are where the community records refutations.
3. Check whether a conference/journal version exists (dblp — §14 — is the right tool).
4. If the report claims a grand-challenge resolution and it is *on* ECCC, that is mildly
   informative, because the call for papers says such submissions may be rejected outright. It is
   not a guarantee.

---

## 2. OpenReview

- **URL:** https://openreview.net/ · **API:** `https://api2.openreview.net` (v2),
  `https://api.openreview.net` (v1, legacy)
- **Operator:** OpenReview.net, a project of the **Allen Institute for Artificial Intelligence
  (AI2)** and UMass Amherst's IESL [COM — widely reported; not independently re-verified in this
  pass, see §2.6]
- **What it is:** a **peer-review platform**, not a preprint server — but functionally the largest
  open archive of *machine-learning submissions and their reviews* in existence
- **On Wikipedia's list:** **no.**

### 2.1 Why it belongs in this survey

Every other entry in this directory archives a *paper*. OpenReview archives the **paper, its
reviews, the reviewer scores and confidences, the author rebuttals, the reviewer replies to the
rebuttals, the area chair's meta-review, and the final decision** — for the largest conferences in
machine learning, permanently, publicly, and behind an API.

For a working engineer this inverts the usual value proposition. **The reviews are frequently worth
more than the paper.** A paper tells you what worked. Four signed-by-number reviews plus a rebuttal
thread tell you: which baselines the authors were forced to add, which ablation a reviewer did not
believe, what the failure modes are, whether the claimed speed-up survived contact with someone
who read the appendix, and — uniquely — *how confident the experts were*. Nothing in the published
PDF carries that. `arXiv` does not have it. `dblp` does not have it. The publisher's version of
record deliberately deletes it.

### 2.2 Which venues actually use it

The `venues` group is the operator's own registry of venues hosted on the platform.

- **4,621 venue members** [API] `https://api2.openreview.net/groups?id=venues`, retrieved
  **2026-09-02**
- **4,634 venue members** [API] same endpoint, re-verified live **2026-09-04**. Thirteen venues
  added in two days.

Distribution by hosting organisation, from the 2026-09-02 snapshot (a "venue" here is a specific
conference *or workshop* instance, so ICLR contributes one main-conference entry plus dozens of
workshops per year):

| Org prefix | Venue entries | Includes |
|---|---:|---|
| `thecvf.com` | 476 | CVPR, ICCV, ECCV and their workshops |
| `NeurIPS.cc` | 423 | NeurIPS main track, datasets & benchmarks track, workshops |
| `aclweb.org` | 339 | ACL, ARR (ACL Rolling Review) |
| `IEEE.org` | 273 | assorted IEEE conferences |
| `ICLR.cc` | 180 | ICLR main conference + workshops, 2013 onward |
| `ICML.cc` | 176 | ICML + workshops |
| `ACM.org` / `acmmm.org` | 142 / 132 | ACM venues, ACM Multimedia |
| `AAAI.org` | 127 | AAAI |
| `EMNLP` | 121 | EMNLP |
| `MICCAI.org` | 116 | medical imaging |
| `KDD.org` | 72 | data mining |
| `robot-learning.org` / `roboticsfoundation.org` | 73 / 74 | CoRL, RSS |
| `colmweb.org` | 42 | COLM (LLM conference) |
| `auai.org` | 22 | UAI |
| `automl.cc` | 22 | AutoML |
| `JSYS` | 44 | **Journal of Systems Research** — an open systems journal |

[API] `groups?id=venues`, 2026-09-02, counted by prefix.

**ICLR is the flagship case.** ICLR has run its entire review process in public on OpenReview since
2013 — reviews visible during the process, not after. **NeurIPS** moved its review data onto the
platform later and publishes reviews for accepted papers. **TMLR** (Transactions on Machine
Learning Research) is an OpenReview-native journal with no conference deadline at all.

### 2.3 Counts — and an important caveat

The 2026-09-02 harvest queried per-venue note counts through both API versions. Those numbers are
reproduced here **with a warning**, because the exact query string was not recorded alongside them
and the endpoint could not be re-queried on 2026-09-04 (§2.5):

| Venue | v1 `count` | v2 `count` |
|---|---:|---:|
| ICLR 2018 | 1,007 | — |
| ICLR 2019 | 1,562 | — |
| ICLR 2020 | 2,579 | — |
| ICLR 2021 | 3,002 | — |
| ICLR 2022 | 3,412 | — |
| ICLR 2023 | 4,946 | — |
| ICLR 2024 | — | 7,382 |
| ICLR 2025 | — | **10,000** |
| ICLR 2026 | — | **10,000** |
| NeurIPS 2021 | 2,767 | — |
| NeurIPS 2022 | 2,816 | — |
| NeurIPS 2023 | — | 3,385 |
| NeurIPS 2024 | — | 4,230 |
| NeurIPS 2025 | — | 5,493 |

[API] `api.openreview.net` / `api2.openreview.net` note queries, 2026-09-02.

**The two `10,000` values are a cap, not a measurement.** Two consecutive years returning the same
round number, immediately after a year returning 7,382, is the signature of a server-side result
limit. **Do not cite ICLR 2025 or ICLR 2026 submission counts from this table.** Marked
**[NOT-VERIFIED]**. The pre-2024 v1 figures rise monotonically and are not round, which is
consistent with real counts — but because the filter semantics (all submissions vs. accepted only
vs. non-withdrawn) could not be re-established, **every number in this table should be treated as
an order-of-magnitude indication only**. The one figure in this section that is solid is the venue
count in §2.2, which was re-verified live.

### 2.4 How to fetch a paper *and its reviews*

The data model is uniform: everything is a **Note**. A submission is a note; each review is a note
whose `forum` field points at the submission's note id; so is each rebuttal, each reply, the
meta-review and the decision. A forum id is a short opaque string like `AL1fq05o7H`.

```
# the submission itself
GET https://api2.openreview.net/notes?forum=<FORUM_ID>&limit=1000
# every note in the thread — submission + reviews + rebuttals + meta-review + decision
GET https://api2.openreview.net/notes?forum=<FORUM_ID>&details=replies
# all submissions to a venue
GET https://api2.openreview.net/notes?content.venueid=ICLR.cc/2025/Conference&limit=1000&offset=0
# the venue registry
GET https://api2.openreview.net/groups?id=venues
# human-readable
https://openreview.net/forum?id=<FORUM_ID>
https://openreview.net/pdf?id=<FORUM_ID>
```

There is an official Python client (`pip install openreview-py`, `openreview.api.OpenReviewClient`)
which handles v1/v2 differences and pagination.

**Fields worth knowing.** `content.venueid` carries the *outcome*, not just the venue —
`ICLR.cc/2024/Conference` for accepted, `ICLR.cc/2024/Conference/Rejected_Submission` for rejected,
`.../Withdrawn_Submission` and `.../Desk_Rejected_Submission` for the rest. Review notes carry
`content.rating`, `content.soundness`, `content.confidence`, `content.strengths`,
`content.weaknesses`, `content.questions`. That means the outcome and the numeric scores are
machine-readable, at scale, for hundreds of thousands of papers.

### 2.5 A worked example — and why the reviews beat the paper

The single best demonstration is **Mamba**. Retrieved on 2026-09-02 [API]:

```
FORUM AL1fq05o7H
title:   Mamba: Linear-Time Sequence Modeling with Selective State Spaces
authors: Albert Gu, Tri Dao
venue:   Submitted to ICLR 2024
venueid: ICLR.cc/2024/Conference/Rejected_Submission
```

Four reviews are attached, and the API returns their scores verbatim:

| Review id | Rating | Soundness | Confidence | Sample of the recorded objection |
|---|---|---|---|---|
| `eIarHE3vGs` | **3: reject, not good enough** | 2 fair | 5: absolutely certain | "The motivation of Mamba is to address the drawbacks of recurrent models… There are many works following the same direction: S4-diagonal, SGConv, MEGA, SPADE…" |
| `bq8XeiBhwY` | 6: marginally above threshold | 3 good | 2: quite likely did not understand central parts | "The model still has a quadratic memory requirement during training like Transformers." |
| `ZJCXkIMKQY` | 8: accept, good paper | 4 excellent | 4: confident | "I do not identify any major weaknesses of the paper." |
| `t7w5AlzJfq` | 8: accept, good paper | 4 excellent | 5: absolutely certain | missing citations to linear-attention and LongConv work |

[API] `api2.openreview.net`, forum `AL1fq05o7H`, retrieved 2026-09-02.

Mamba was **rejected from ICLR 2024**. It went on to become one of the most-cited architecture
papers of the following two years, and the state-space-model line of work it anchors now runs on
production accelerators. The permanent, public, timestamped record of a **confidence-5 reviewer
scoring it 3/reject** is not available anywhere else, and it is exactly the kind of evidence you
want when deciding how much weight a conference decision deserves. It is also a genuine data point
about review reliability: two confidence-5 reviewers on the same paper gave it 3 and 8.

Note the second row as well — a reviewer self-reporting confidence 2 ("quite likely that you did
not understand the central parts of the submission") whose stated weakness is factually wrong about
the architecture. That is on the record forever. On arXiv there is no such record at all.

### 2.6 Access, reachability and the 2026-09-04 blackout

**This is the durability finding of this section.** OpenReview's state changed between the two
probe dates in this pass.

| Endpoint | 2026-09-02 | 2026-09-04 |
|---|---|---|
| `api2.openreview.net/groups?id=venues` | works, 4,621 members | **works**, 4,634 members |
| `api2.openreview.net/notes?...` | works, JSON returned | **HTTP 403 `ChallengeRequiredError`** |
| `api.openreview.net/notes?...` (v1) | works | **HTTP 403 `ChallengeRequiredError`** |
| `openreview.net/forum?id=AL1fq05o7H` | works | **HTTP 200, 4,787-byte challenge shell** |
| `openreview.net/pdf?id=AL1fq05o7H` | works | **HTTP 403, 12,692-byte HTML** (not a PDF) |
| `openreview.net/group?id=ICLR.cc/2025/Conference` | — | works, 164,976 B |

The 403 body is JSON:

```json
{"name":"ChallengeRequiredError","message":"Challenge verification required (2026-09-04-…)",
 "status":403,"details":{"challengeUrl":"https://openreview.net/challenge?redirect=…"}}
```

**User-agent rotation does not help.** Chrome 131, `curl/8.21.0`, `python-requests/2.31.0`,
`WhatsApp/2.23.20.0`, `ChatGPT-User/1.0` and `ClaudeBot/1.0` all received the identical 403 on
2026-09-04 [probe ×6]. This is a JS browser-verification interstitial ("Verifying your
browser | OpenReview"), not a UA filter — the AGENTS.md fallback ladder is the wrong tool for it.

**Probing trap.** `https://openreview.net/forum?id=<anything>` returns **HTTP 200 and a
4,787-byte challenge shell for a real forum id and for the deliberately bogus `ZZZZZZZZZZ`
alike** [probe, negative control, 2026-09-04]. Byte-identical. Same failure class as `osf.io`'s
4,207-byte shell. Under the challenge regime, **neither the status code nor the body size can test
whether a paper exists.**

**Practical guidance:** use `openreview-py` with an authenticated account, or expect to solve the
interstitial. The `groups` endpoint remained open on both dates, so venue enumeration still works
unauthenticated.

### 2.7 Reliability, licensing, caveats

- **A note on OpenReview is not a preprint deposit.** There is no DOI, no independent archive, no
  guarantee of persistence beyond the platform. Compare arXiv, which has an institutional
  preservation commitment.
- **Withdrawn and desk-rejected submissions may be hidden.** Visibility is set per venue by the
  organisers. Mamba's rejection is visible because ICLR publishes rejected submissions; most
  venues do not. **Absence of a paper from OpenReview is not evidence it was not submitted.**
- **Licensing is per-venue and inconsistent.** Some venues attach CC-BY, many attach nothing. There
  is no site-wide default. Treat bulk reuse of OpenReview PDFs as unlicensed unless you check the
  specific note.
- **The operator attribution above is [COM], not [DOC].** The AI2/UMass-IESL provenance is widely
  reported and matches the platform's own history, but the About page could not be loaded on
  2026-09-04 because of the challenge, so it is not carried here as [DOC].
- **Reviews are not signed.** Reviewer identities are pseudonymous (`Reviewer_xY3z`). You get the
  argument and the self-reported confidence, not the person.

---

## 3. ACL Anthology

- **URL:** https://aclanthology.org/ · **Operator:** Association for Computational Linguistics
- **Scope:** computational linguistics and NLP · **Coverage from:** 1952 (entries), the modern
  ACL series from 1979 · **On Wikipedia's list:** **no.**

### 3.1 What it is

The complete, free, full-text archive of everything the ACL publishes: **ACL, EMNLP, NAACL, EACL,
AACL, COLING, CoNLL, *SEM, SemEval, TACL, CL** and every workshop attached to them. No paywall, no
membership, no embargo — the PDF is up the day the proceedings appear, and it has been that way for
decades. In a field where the top venues are conferences, this means **the entire canon of NLP is
open access by default**. Nothing else in this survey has that property.

Given that the last five years of ACL-venue work is the intellectual substrate of every deployed
language model, an archive that is 100% open and bulk-downloadable is not a niche resource.

### 3.2 Size — measured from the bulk BibTeX

The operator publishes **the whole bibliography as one gzipped BibTeX file**:
`https://aclanthology.org/anthology.bib.gz`.

| Measurement | Value | Evidence |
|---|---:|---|
| File size | **12,647,756 bytes** | [API] 2026-09-02 |
| File size (re-fetch) | **12,648,737 bytes** | [API] 2026-09-04, `application/x-gzip` |
| BibTeX entries | **131,027** | [API] parsed, 2026-09-02 |
| BibTeX entries (re-fetch) | **131,040** | [API] parsed live, 2026-09-04 — 13 added in two days |
| `@inproceedings` | 124,477 | [API] 2026-09-02 |
| `@article` (TACL, CL) | 3,362 | [API] 2026-09-02 |
| `@proceedings` (volume records) | 2,968 | [API] 2026-09-02 |
| `@book` | 220 | [API] 2026-09-02 |
| Year range | **1952 – 2026** | [API] 2026-09-02 |

**Growth, by year of publication** [API] parsed from the 2026-09-02 dump:

| 1979 | 1990 | 2000 | 2010 | 2015 | 2020 | 2023 | 2024 | 2025 | 2026 (part) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 50 | 515 | 1,254 | 3,072 | 2,911 | 7,330 | 9,094 | 12,135 | **14,919** | 10,413 |

The curve is the LLM boom rendered as bibliography: roughly flat 2010–2015, then a 5× increase to
2025. 2026 is at 10,413 by early September and on track to exceed 2025. Note that ~2,968 of the
131,027 entries are *volume* records rather than papers, so the paper count is ≈128,000. [INF]

### 3.3 Access and bulk retrieval

| Facility | Result |
|---|---|
| `https://aclanthology.org/anthology.bib.gz` | **Works**, 12.6 MB, whole corpus [API] 2026-09-04 |
| Landing page `https://aclanthology.org/N19-1423/` | HTTP 200, 42,299 B, title *"BERT: Pre-training of Deep Bidirectional Transformers…"* [WEB] 2026-09-04 |
| PDF `https://aclanthology.org/N19-1423.pdf` | HTTP 200, 786,279 B, PDF 1.3, 16 pages [API] 2026-09-04 |
| **Negative control** `https://aclanthology.org/Z99-9999/` | **HTTP 404**, 9,185 B — an *honest* 404 [probe] 2026-09-04 |
| Bot blocking | **None.** No challenge, no UA filtering, no rate limit hit |
| Other bulk formats | Per-volume BibTeX/MODS/Endnote; the site is generated from a public GitHub repo of XML |

**The ACL Anthology is the best-behaved server in this entire survey.** It returns a real 404 for a
nonexistent identifier — which ECCC (§1.8), OpenReview (§2.6), CDS (§4.4), `osf.io` and
`unpaywall.org` all fail to do — it serves a complete bulk dump over plain HTTP with no
registration, and it does not challenge scripted clients. If you need a reference implementation of
how an open archive should behave, this is it.

**Licensing:** most modern ACL papers carry **CC-BY 4.0**, stated on the landing page. Older
material predates the policy and is not uniformly licensed. Check per paper before bulk reuse.
[WEB]

### 3.4 Why the arXiv and Anthology versions differ

Almost every ACL-venue paper also exists on arXiv under `cs.CL`, and they are **not the same
document**. Which one you should read depends on what you want:

- **The Anthology version is the version of record.** It is camera-ready, page-limit-compliant,
  post-review, and it is what the DOI and the citation point at.
- **The arXiv version is usually the *later* one.** Authors commonly post the submission before the
  deadline and then update after acceptance — but they update *inconsistently*. An arXiv `v3` may
  contain an extra appendix, extra ablations added during rebuttal, corrected numbers, or the
  reviewer-demanded baseline that would not fit in the camera-ready page limit.
- **The arXiv version can also be the *earlier*, worse one.** A `v1` posted before review may
  contain results the reviewers rejected. There is no automatic propagation from the Anthology back
  to arXiv.
- **Consequence:** if you are reproducing a numeric result, take the Anthology PDF and treat the
  arXiv PDF as a possible superset. If you are citing, cite the Anthology. If a number does not
  reproduce, check whether the other version reports a different one. [INF]
- Three-way triangulation is available and cheap: Anthology (record) + arXiv (extended) +
  OpenReview (§2, for ARR/ACL-Rolling-Review venues — the reviews that caused the difference).

---

## 4. CERN Document Server and INSPIRE-HEP

Two CERN-adjacent systems, both absent from Wikipedia's list, both of direct interest to hardware
engineers for a reason that has nothing to do with particle physics: **the LHC experiments are the
largest sustained real-time-electronics programme on earth**, and they publish their engineering.

### 4.1 Why a hardware engineer cares

The material that lives in these two systems and nowhere else:

- **Trigger systems** — Level-1 trigger designs are hard-real-time FPGA pipelines with fixed
  microsecond latency budgets processing terabits per second. The ATLAS and CMS trigger technical
  design reports are the most detailed public documents of their kind.
- **Front-end ASICs** — custom readout chips (Timepix, VeloPix, RD53, the ALICE and LHCb front
  ends), with process-node choices, power budgets, and measured noise.
- **Radiation-hardened design** — total-ionising-dose and single-event-upset behaviour of
  commercial and custom parts, characterised on real beamlines. **1,932 INSPIRE records** match
  `"radiation hard"` [API, 2026-09-04].
- **High-speed optical links, clock distribution, timing** — GBT/lpGBT, sub-picosecond distribution
  over kilometres.
- **Silicon detector technology** — the semiconductor-device physics behind pixel and strip sensors.
- **CERN technical reports, notes and theses** — CERN doctoral theses are deposited in CDS and are
  frequently the *only* complete write-up of a subsystem's electronics.

Search counts on INSPIRE, all [API] 2026-09-04: `FPGA` **5,380**, `trigger electronics` **5,430**,
`ASIC` **2,869**, `"radiation hard"` **1,932**, `ATLAS FPGA` **526**.

### 4.2 INSPIRE-HEP — the API works and is pleasant

- **URL:** https://inspirehep.net/ · **API base:** `https://inspirehep.net/api/`
- **Operator:** a collaboration of CERN, DESY, Fermilab, IHEP, IN2P3, SLAC and others
- **Lineage:** successor to **SPIRES** (SLAC, 1974) — the database that the *first web server
  outside Europe* was built to serve. Predates arXiv by seventeen years.

| Collection | Records | Evidence |
|---|---:|---|
| `literature` | **1,882,221** | [API] `/api/literature/?q=&size=1`, 2026-09-02 |
| `literature` (re-verified) | **1,882,844** | [API] same, live 2026-09-04 — **+623 in two days** |
| `conferences` | 31,706 | [API] 2026-09-04 |
| `jobs` | 31,675 | [API] 2026-09-04 |
| `institutions` | 12,315 | [API] 2026-09-04 |
| `data` | 11,615 | [API] 2026-09-04 |
| `experiments` | 4,002 | [API] 2026-09-04 |

**Negative control:** `?q=zzqqxx_nonexistent_term_9999` returns HTTP 200 with `hits.total: 0` and an
empty `hits.hits` array — a **truthful** empty result, verified on both dates. INSPIRE does not
inflate and does not fake. [API]

Usage:

```
GET https://inspirehep.net/api/literature?q=<query>&size=<n>&page=<n>&fields=titles,authors
GET https://inspirehep.net/api/literature/1483465                       # single record
GET https://inspirehep.net/api/literature/1483465?format=bibtex         # also latex-eu, latex-us, cv, json-expanded
GET https://inspirehep.net/api/literature/?q=refersto%3Arecid%3A1483465 # citations to a record
GET https://inspirehep.net/api/doi/<doi>   /api/arxiv/<id>              # resolve by external id
```

Every record carries a `links` object with those alternate formats pre-built, plus a
`fields=` projection parameter to keep responses small. No authentication, no challenge, no UA
filtering observed on either probe date. The `q` syntax supports the legacy SPIRES operators
(`t `, `a `, `refersto:`, `citedby:`) as well as plain full text.

An arbitrary record retrieved as a sanity check on 2026-09-02: **id 1483465, "The Silicon-Tungsten
Tracker of the DAMPE Mission"** — i.e. a detector-instrumentation paper, which is representative of
what the collection is full of. [API]

### 4.3 CERN Document Server (CDS)

- **URL:** https://cds.cern.ch/ · **Operator:** CERN
- **Scope:** CERN's institutional repository — papers, preprints, **technical reports, internal
  notes, theses, talks, scanned historical documents, photos, video**
- **OAI-PMH base:** `http://cds.cern.ch/oai2d` · **`earliestDatestamp`: 2003-06-02T08:06:23Z**
  [API] `verb=Identify`, 2026-09-02 **and** re-verified 2026-09-04
- **Deleted-record policy:** `persistent` · **granularity:** `YYYY-MM-DDThh:mm:ssZ` [API]
- **Submission policy, in CDS's own words:** *"Submission restricted."* **Metadata policy:** *"Free
  and unlimited use by anybody with obligation to refer to original record."* **Data policy:**
  *"Refer to the copyright and license statement of each specific record."* [DOC, embedded in the
  OAI `Identify` response, 2026-09-02]

That "submission restricted" line is the key structural fact: **CDS is not a preprint server anyone
can post to.** It is an institutional repository. Deposits come from CERN members and CERN
processes. That is precisely why it holds material — internal notes, engineering reports — that
would never be submitted to arXiv.

**Set sizes**, measured via `ListIdentifiers` and reading `completeListSize` from the
`resumptionToken` [API, all 2026-09-04]:

| Set | Records | What it is |
|---|---:|---|
| *(no set — whole repository)* | **578,928** | Everything harvestable over OAI |
| `cerncds:BOOK` | 172,038 | CERN library book records |
| `cerncds:CERN` | 158,072 | CERN-authored documents |
| `cerncds:FULLTEXT` | **316,404** | **Records that actually have full text attached** |
| `cerncds:CONF` | 34,467 | Conference contributions |
| `cerncds:REPORT` | 28,956 | **Technical reports** |
| `cerncds:THESES` | 11,992 | **Theses** |
| `cerncds:SCAN` | 10,391 | Scanned historical documents |
| `cerncds:pauli-archive` | 3,821 | The Pauli archive |
| `cerncds:atlas-conf` | 1,295 | ATLAS conference notes |
| `cerncds:cms-notes` | 932 | CMS internal notes |
| **`zzz:bogus`** *(negative control)* | — | `noRecordsMatch` error — **correct behaviour** |

**578,928 total against 316,404 with full text** is the number to carry: **just over half of CDS is
full text**; the rest is catalogue metadata (books, photos, talks). Do not quote 578,928 as a
document count.

Other sets present but not sized here: `cerncds:TALK`, `cerncds:TALK:FULLTEXT`,
`cerncds:CERN:FULLTEXT`, `cerncds:CONF:FULLTEXT`, `cerncds:SCAN:FULLTEXT`, `cerncds:alice-pub`,
`cerncds:atlas-pub`, `cerncds:cms-pas`, `cerncds:lhcb-conf`, `cerncds:lhcb-pub`, `cerncds:EuCARD`,
`cerncds:MEMORIAV`, `DOI`, `INSPIRE`, `INSPIRE:HEP`, `forINSPIRE`, `forSciTalks`, `ForCDS`,
`openaire`, `INIS`, and arXiv-style subject sets `cerncds:hep-ex|hep-ph|hep-th|hep-lat|nucl-ex|
nucl-th|astro-ph|gr-qc|quant-ph|math|math-ph|physics|cs` [API, `verb=ListSets`, 2026-09-02].
Note that **`cerncds:cs` exists but returned no `completeListSize`** on 2026-09-04 —
[NOT-VERIFIED], not sized.

CDS names its OAI *friends*: `http://cds.cern.ch/oai2d`, `http://openaire.cern.ch/oai2d`,
`http://export.arxiv.org/oai2` [API, `Identify`, 2026-09-02].

### 4.4 CDS probing trap — Anubis, and the way past it

**`cds.cern.ch` is behind an Anubis proof-of-work bot wall on its HTML and REST interfaces, but its
OAI-PMH endpoint is wide open.** This is the single most useful retrieval finding in this record.

| Endpoint | 2026-09-02 | 2026-09-04 |
|---|---|---|
| `cds.cern.ch/api/records?q=&size=1` | **HTTP 200, 7,519-byte Anubis challenge** | **HTTP 200, 7,619-byte Anubis challenge** |
| `cds.cern.ch/search?p=FPGA&of=hx` | — | **HTTP 200, 7,619-byte Anubis challenge** |
| `cds.cern.ch/oai2d?verb=Identify` | **HTTP 200, real XML, 2,384 B** | **HTTP 200, real XML, 2,384 B** |
| `cds.cern.ch/oai2d?verb=ListSets` | **HTTP 200, real XML, 4,260 B** | works |
| `cds.cern.ch/oai2d?verb=ListIdentifiers&…` | works | works |

Two things make this a *trap* rather than a mere block:

1. **The challenge is served with HTTP 200, not 403.** A harvester checking status codes records a
   success and stores the challenge page as if it were data. The tell is the `<title>Making sure
   you're not a bot!</title>` and the `anubis_challenge` JSON block, and the ~7.5 kB body size.
   (Note: this is a *different* signature from the ~5.6 kB Cloudflare 403 body documented in the
   index — same idea, different vendor, and Anubis uses 200 where Cloudflare uses 403.)
2. **User-agent rotation does not defeat it.** The challenge body from 2026-09-02 embeds the
   metadata it saw: `"User-Agent":"curl/8.21.0"`, `"X-Real-Ip":"…"`, `"algorithm":"fast"`,
   `"difficulty":4`. It is a JavaScript SHA proof-of-work, not a UA filter. Chrome-UA requests on
   2026-09-04 received the same challenge.

**Use OAI-PMH.** `verb=ListRecords&metadataPrefix=marcxml&set=cerncds:REPORT` (or `oai_dc`) gets you
the CERN technical-report corpus with no challenge at all. Add this to the crawler access table.

---

# TIER 2 — smaller omissions, compact records

Measured 2026-09-02, re-verified 2026-09-04. Crossref DOI-prefix counts use
`https://api.crossref.org/prefixes/<prefix>/works?rows=0` and read `message.total-results`.
A deliberately bogus prefix (`10.99999`) returns an **error, not a zero** — so a numeric answer from
that endpoint is meaningful. [API, negative control, 2026-09-04]

## 5. SciPost

- **URL:** https://scipost.org/ · **Operator:** SciPost Foundation (Netherlands) · **DOI prefix:**
  `10.21468`
- **Model:** genuine diamond open access — no author charges, no reader charges, **public referee
  reports with named or anonymous referees, and public author replies**. Physics-dominant, with
  chemistry, astronomy and computational-science sections.
- **Size: 12,558 registered DOIs** [API] Crossref prefix `10.21468`, 2026-09-04. That figure
  includes journal articles, reports and versions, so it is an upper bound on articles.
- **Reachability [WEB, 2026-09-04]: `scipost.org` is behind an Anubis proof-of-work challenge.**
  `https://scipost.org/` and `https://scipost.org/api/` both return **HTTP 200 with a 3,903-byte
  Anubis body** (`<title>Making sure you're not a bot!</title>`, `anubis_challenge` JSON,
  `algorithm: fast, difficulty: 4`). Same vendor as CDS (§4.4), different body size. The Crossref
  route above is therefore the only unauthenticated way to size SciPost from a script.
- **Relevance here:** the closest thing to a working *diamond OA + open referee report* journal.
  Almost no direct hardware content, but the governance model is the one every "reform scholarly
  publishing" argument points at.

## 6. Open Research Europe (ORE)

- **URL:** https://open-research-europe.ec.europa.eu/ · **Operator:** European Commission, published
  on F1000Research's platform (**DOI prefix `10.12688`**, shared with all F1000 properties)
- **Model:** publish-then-review. Horizon Europe / Horizon 2020 grantees post; open peer review
  follows; the article is indexed once it passes.
- **Size — and a conflict this pass could not resolve:**

  | Measurement | Value | Evidence |
  |---|---:|---|
  | Crossref `container-title:"Open Research Europe"` | **2,437** | [API] 2026-09-04 |
  | Crossref, restricted to `type:journal-article` | **2,437** | [API] 2026-09-04 |
  | DOIs harvested under `10.12688/openreseurope` | **2,430** | [API] 2026-09-02 |
  | Figure reported by a sibling record in this pass | **1,513** | [see caveat] |

  **The 1,513 does not reproduce.** Two independent 2026-09-02/04 measurements land at 2,430–2,437.
  The most likely explanation is that 1,513 counted *indexed/approved* articles while the Crossref
  figures count every registered DOI including awaiting-peer-review versions and revisions — but
  that explanation was **not confirmed**. Both readings are recorded; **1,513 is [NOT-VERIFIED]**
  and should not be carried forward without re-measurement.
- **Reachability:** front page HTTP 200, **55,677 bytes** [WEB, 2026-09-04]. See the trap in §8.
- **Relevance:** small but growing; EU-funded engineering and computing does appear. The Europe PMC
  route (`PUBLISHER:"Open Research Europe"`) returned **hitCount 0**, so Europe PMC is *not* a valid
  index for ORE — a live negative worth recording [API, 2026-09-04].

## 7. Peer Community In (PCI) and PCI Registered Reports — the *overlay* model

- **URL:** https://peercommunityin.org/ · **DOI prefix:** `10.24072` · **Size: 3,975 registered
  DOIs** [API] Crossref, 2026-09-04 · front page HTTP 200, 225,655 B [WEB, 2026-09-04]

**PCI is not a preprint server, and this is the single most commonly misunderstood entry in this
whole document.** It hosts nothing. It is an **overlay**: a network of ~20 thematic communities
(PCI Evolutionary Biology, PCI Ecology, PCI Registered Reports, PCI Math & Comp Sci, …) that
organise peer review of preprints **that live somewhere else** — on bioRxiv, on OSF, on Zenodo, on
arXiv.

The mechanism:

1. An author deposits the preprint on a real server and gets a real DOI there.
2. The author submits *the DOI*, not the file, to a PCI community.
3. A PCI recommender (an editor) organises real referee reports.
4. If it passes, PCI publishes a **Recommendation** — a short, citable, DOI'd editorial endorsement
   under `10.24072` — plus the full referee reports and author replies, all public.
5. **The preprint never moves.** It stays on bioRxiv/Zenodo/arXiv, now carrying a badge that says a
   named editor and named referees signed off.

**Why this matters structurally:** it decouples *hosting* from *certification*. A server gives you a
timestamp; PCI gives you the peer-review layer, separately, on top, without a journal. **PCI
Registered Reports** goes further: it reviews the *protocol* before the data are collected — in-
principle acceptance — which is the strongest available defence against p-hacking and HARKing, and
it applies equally well to a benchmarking methodology as to a clinical trial.

Consequences for anyone counting things: **3,975 PCI DOIs do not represent 3,975 hosted documents.**
They represent recommendations and reviews *about* documents held elsewhere. Adding PCI's count to a
sum of preprint-server sizes double-counts. This is the same error as summing SSRN networks, or
treating ScienceOpen's index as its holdings. [INF]

## 8. VeriXiv

- **URL:** https://verixiv.org/ · **Operator:** on the F1000Research/Gates Foundation platform,
  DOI prefix `10.12688/verixiv` · **Focus:** Gates-funded global-health research, with an explicit
  **integrity-check gate** before posting (image forensics, plagiarism, data availability).
- **Size: 812 records** [API] Europe PMC `PUBLISHER:"VeriXiv"`, 2026-09-04. Europe PMC's negative
  control (`PUBLISHER:"ZZQQNotAPublisher"`) returns `hitCount 0`, so the endpoint is truthful.
- Sample record from the 2026-09-02 harvest [API]: `PPR1310064`,
  `10.12688/verixiv.3676.1`, *"Extrusion Cooking Enhances the Shelf Life of Grain Amaranth…"*,
  `pubYear 2026`, `firstPublicationDate 2026-09-01`, `versionNumber 1`, **`isOpenAccess: "N"`,
  `hasPDF: "N"`** — i.e. Europe PMC indexes the metadata but does not hold the full text.
- **Probing trap — the identical-shell problem, again.** `https://verixiv.org/` and
  `https://open-research-europe.ec.europa.eu/` both return **HTTP 200 and exactly 55,677 bytes**
  [probe ×2, 2026-09-04]. They are the same F1000/ARPHA SPA shell rendered under two brands. **Byte
  size cannot distinguish these two sites, let alone distinguish a real page from a missing one.**
  Add to the family that already contains `osf.io` (4,207 B) and `unpaywall.org` (1,421 B).
- **Relevance to computing: essentially nil.** Listed because it is a recent, real, *missing* entry
  and because of the shell trap.

## 9. Advance (SAGE) — probably moribund, and here is why that is hard to prove

- **URL:** https://advance.sagepub.com/ · **Operator:** SAGE Publishing · **DOI prefix:** `10.31124`
  · social sciences and humanities.
- **Front door: HTTP 403.** Body sizes **5,388 bytes** (`curl/8.21.0`), **5,623 bytes** (Chrome UA),
  **5,388 bytes** (`WhatsApp/2.23.20.0`) [probe ×3, 2026-09-04]. **This is the ~5.6 kB Cloudflare
  challenge signature.** Per this repository's own rule: **blocked, not broken.** A 403 here is
  evidence about Cloudflare, not about SAGE.
- **So go around it.** Crossref knows what SAGE has registered:

  | Measurement | Value | Evidence |
  |---|---|---|
  | Total DOIs under `10.31124` | **4,417** | [API] Crossref, 2026-09-04 |
  | **Most recent deposit** | **2026-04-21T16:11:19Z** | [API] Crossref `sort=created&order=desc`, 2026-09-04 |
  | Titles of the three newest | *"Geopolitical Tightrope in Taiwan…"*, *"Political Change and Smallholder farming…"*, *"Gender Equality in Cambodian Higher Education…"* | [API] 2026-09-04 |

- **Verdict: dormant, not confirmed dead.** All three newest DOIs were created in the *same
  second*, which is a batch deposit, and **nothing has been registered in the four and a half
  months since**. That is a strong signal for a server that was posting continuously. But a
  Cloudflare-blocked front door plus a deposit gap is not a closure announcement. **Status:
  [NOT-VERIFIED] as closed; recorded as dormant with the evidence above.** Anyone with a browser
  should check the front page and, if it is live, correct this line.

## 10. Cambridge Open Engage — alive, and busier than before

- **URL:** https://www.cambridge.org/engage/coe/ · **Operator:** Cambridge University Press ·
  **DOI prefix:** `10.33774`
- **Size: 5,738 registered DOIs** [API] Crossref, 2026-09-04.
- **Most recent deposit: 2026-09-04T05:50:58Z** — *hours* before the probe [API]. The three newest:
  `10.33774/coe-2026-zl7cd`, `10.33774/coe-2026-0bntp`, `10.33774/apsa-2025-l4d92-v4` [API].
- **This settles a question raised elsewhere in this directory.** Per
  [`chemrxiv.md`](chemrxiv.md), **ChemRxiv left the Cambridge Open Engage platform again in January
  2026.** The obvious worry was that COE would collapse without its largest tenant. It did not:
  COE was registering new DOIs on the morning of the probe, and the `apsa-` slug in the third row
  shows it is still hosting partner communities (APSA Preprints). **Alive.**
- Note the platform's public REST path is *not* the ChemRxiv one:
  `…/engage/api-gateway/coe/public-api/v1/items` returns `Cannot GET` [probe, 2026-09-04], and the
  equivalent ChemRxiv endpoint now returns a **Cloudflare "Just a moment…" interstitial**
  [probe, 2026-09-04]. Crossref remains the reliable measurement route for both.
- **Relevance to computing:** low. Listed because it is platform infrastructure under several
  branded servers, and because its survival after ChemRxiv's exit is a durability data point.

## 11. J-STAGE

- **URL:** https://www.jstage.jst.go.jp/ · **Operator:** Japan Science and Technology Agency (JST)
- **What it is:** the national electronic platform for Japanese scholarly societies — well over
  3,000 journals, including the **IEICE Transactions** (Electronics / Communications / Information
  and Systems) and **IPSJ** titles. Much of it is free to read; a lot of it is **in Japanese only**
  and is invisible to English-language search.
- **Why it is here:** for anyone doing device physics, semiconductor process, communications or
  signal processing, J-STAGE holds a large body of work that has **no arXiv copy and no Western
  mirror**. It is the single biggest blind spot in an English-only literature search in electronics.
- **Reachability:** browse page HTTP 200, 86,304 B [WEB, 2026-09-04]. **The OAI-PMH handler at
  `/oai/OAIHandler?verb=Identify` returned HTML, not XML** [probe, 2026-09-04] — so the endpoint
  either moved or is gated. **No total record count was obtained: [NOT-VERIFIED].** J-STAGE does
  publish a WebAPI requiring registration, which this pass did not use.
- **Honest caveat:** J-STAGE is a *journal* platform, not a preprint server. It is included because
  the omission that matters is not "preprints" but "where the electronics literature actually is".

## 12. KISTI ScienceON

- **URL:** https://scienceon.kisti.re.kr/ · **Operator:** Korea Institute of Science and Technology
  Information (KISTI), a government research institute
- **What it is:** Korea's national aggregator — journal articles, **patents**, reports, theses,
  research data and Korean-language technical literature, over a domestic corpus that is largely
  absent from Scopus and Web of Science.
- **Reachability:** the bare root returns **HTTP 200 with a 217-byte body** — a JS bootstrap, not
  content. `https://scienceon.kisti.re.kr/main/mainForm.do` returns **HTTP 200, 336,305 B**, an
  `lang="KO"` page [probe ×2, 2026-09-04]. **Another 200-means-nothing case: 217 bytes of shell.**
- **Size: [NOT-VERIFIED].** No unauthenticated count endpoint was found. KISTI operates an OpenAPI
  behind a key.
- **Honest caveat:** most content is Korean-language and a meaningful share is **abstract-only or
  paywalled** to non-Korean users. Useful for *knowing a paper exists*; frequently not useful for
  reading it.

## 13. SSOAR

- **URL:** https://www.ssoar.info/ · **Operator:** GESIS – Leibniz Institute for the Social Sciences
- **What it is:** Social Science Open Access Repository. Green OA, mostly German-language social
  science, DSpace-based.
- **Size: 101,200 records** [API] OAI-PMH `verb=ListIdentifiers&metadataPrefix=oai_dc`,
  `completeListSize` read from the `resumptionToken`, harvested 2026-09-02. The 2026-09-04 re-probe
  of the same endpoint returned no `completeListSize` on the first page, so the figure is carried
  from the 2026-09-02 harvest only.
- Sets are DSpace community/collection ids (`com_community_1`, `com_community_10000`, …) [API].
- **Reachability:** front page HTTP 200, 24,461 B [WEB, 2026-09-04]. No bot wall observed.
- **Relevance to computing: none.** Listed for completeness — it is a large, well-run, genuinely
  open repository that Wikipedia's list omits while listing much smaller social-science servers.

---

# TIER 3 — layers, indexes, and things that look like servers

## 14. Overlays, indexes and one shutdown

None of these hosts original literature. All of them will be mistaken for a repository by someone.

### 14.1 alphaXiv

- `https://alphaxiv.org/` **301 → `https://www.alphaxiv.org/`**, HTTP 200, 627,924 B, title
  *"Explore | alphaXiv"* [probe, 2026-09-04].
- `https://www.alphaxiv.org/abs/2312.00752` → HTTP 200, 239,067 B, title *"Mamba: Linear-Time
  Sequence Modeling with Selective State Spaces | alphaXiv"* [probe, 2026-09-04].
- **What it is:** a discussion and annotation layer over arXiv — swap `arxiv.org` for `alphaxiv.org`
  in a URL and you get the same paper with a comment thread and AI tooling attached. **Hosts
  nothing.** Same category error as Synthical (see [`synthical.md`](synthical.md)); the difference
  is that alphaXiv was reachable and functioning on the probe date and Synthical was not.

### 14.2 ar5iv

- `https://ar5iv.labs.arxiv.org/html/1706.03762` → HTTP 200, **167,302 B**, title
  *"[1706.03762] Attention Is All You Need"* [probe, 2026-09-04].
- **Negative control:** `…/html/9999.99999` → **HTTP 404, 2,475 B**. Honest 404 [probe, 2026-09-04].
- **What it is:** an arXiv Labs service that renders arXiv LaTeX source to **HTML5**. Not a
  repository — a *format converter* over arXiv's own holdings. It is genuinely useful for two
  things: reading papers on a phone, and **machine-parsing equations and tables** without going
  through PDF extraction. If you are building a pipeline over arXiv content, ar5iv HTML beats PDF.

### 14.3 Hugging Face Papers

- `https://huggingface.co/papers` → HTTP 200, 314,513 B [probe, 2026-09-04].
- `…/papers/1706.03762` → HTTP 200, 292,900 B, *"Paper page - Attention Is All You Need"*.
- `…/papers/2312.00752` → HTTP 200, 285,472 B, *"Paper page - Mamba: …"*.
- **Negative control:** `…/papers/9999.99999` → **HTTP 404, 52,935 B**. Honest 404 [probe ×3,
  2026-09-04].
- **What it is:** a curated daily feed and discussion page over arXiv ML papers, cross-linked to
  models, datasets and Spaces on the same platform. **Hosts no papers.** Its real value is the
  **link from paper to running artifact** — the weights and the demo, not the PDF.

### 14.4 Papers with Code — **shut down; the data survived**

This is the durability finding of Tier 3, and it is verified.

| Probe | Result | Date |
|---|---|---|
| `https://paperswithcode.com/` | **HTTP 302 → `https://huggingface.co/papers/trending`**, final 200, 1,507,368 B, title *"Trending Papers - Hugging Face"* | 2026-09-04 |
| `https://huggingface.co/api/datasets/pwc-archive/papers-with-abstracts` | **HTTP 200**, `lastModified 2026-08-17T10:40:27Z`, 690 downloads, `private: false` | 2026-09-04 |
| `https://huggingface.co/api/datasets/pwc-archive/links-between-paper-and-code` | **HTTP 200**, `lastModified 2025-09-10T12:20:22Z` | 2026-09-04 |
| `…/pwc-archive/evaluation-tables` | HTTP 200 | 2026-09-04 |
| `…/pwc-archive/methods` | HTTP 200 | 2026-09-04 |
| `…/pwc-archive/datasets` | HTTP 200 | 2026-09-04 |

**What happened.** Papers with Code — the paper↔code↔leaderboard index that a decade of ML work was
navigated through — **no longer exists as an independent site.** Its domain now redirects to
Hugging Face's trending-papers page. Meta had acquired it via Facebook AI Research; Hugging Face
absorbed the front-end function.

**Where the data went.** The project's own dataset README, harvested 2026-09-02 [DOC], now points
all five bulk dumps at the **`pwc-archive` organisation on Hugging Face**:

- `pwc-archive/papers-with-abstracts`
- `pwc-archive/links-between-paper-and-code`
- `pwc-archive/evaluation-tables`
- `pwc-archive/methods`
- `pwc-archive/datasets`

All five resolve HTTP 200 and are public [API, 2026-09-04]. Licence is stated as **CC-BY-SA 4.0**
[DOC]. The same README still says *"At the moment, data is regenerated daily"* — **that sentence is
now false**: `links-between-paper-and-code` was last modified **2025-09-10**, a year before the
probe. It is an **archive**, not a live feed.

**The lesson, which is the reason this record exists.** A widely-used, well-funded, corporate-backed
research index disappeared, and the *only* reason its corpus is still retrievable is that somebody
deliberately mirrored the bulk dumps to a third-party platform under an open licence. The website
died; the CC-BY-SA dumps did not. **Bulk dumps under an open licence are what durability actually
looks like** — which is precisely why the presence or absence of a bulk dump is a column in the
table in §15.

### 14.5 Semantic Scholar / S2ORC

- **URL:** https://www.semanticscholar.org/ · API `https://api.semanticscholar.org/graph/v1/`
- **What it is:** AI2's corpus and citation graph over ~200 M papers, with **S2ORC** (the Semantic
  Scholar Open Research Corpus) as the full-text-and-parsed-references bulk product used for
  training and for citation-context analysis. Not a repository — an *index with parsed full text
  where licensing permits*.
- **Probe result: HTTP 429 `Too Many Requests`** on `graph/v1/paper/search`, and **HTTP 500** on
  `graph/v1/paper/search/bulk`, both unauthenticated [probe ×2, 2026-09-04]. **Blocked/broken, not
  absent — no count obtained: [NOT-VERIFIED].** The documented fix is a free API key; this pass did
  not apply for one. The 429 body links the key request form, which is a well-behaved way to be
  refused.

### 14.6 NASA ADS

- **URL:** https://ui.adsabs.harvard.edu/ (HTTP **202**, empty body [probe, 2026-09-04]) · API
  `https://api.adsabs.harvard.edu/v1/`
- **Probe result:** `v1/search/query?q=FPGA` returns **HTTP 401 `Missing "Authorization" in
  headers`** [probe, 2026-09-04]. **An API token is mandatory.** No count obtained:
  **[NOT-VERIFIED]**.
- **Why it is here anyway:** ADS is the astrophysics literature system, and astrophysics is a
  *hardware* discipline — detector arrays, cryogenic readout, CCD/CMOS sensor characterisation,
  radio-telescope DSP and correlator design, spaceflight electronics. ADS indexes instrumentation
  papers and observatory technical reports that INSPIRE does not.

### 14.7 dblp — metadata only, and the canonical CS bibliography

- **URL:** https://dblp.org/ · **Operator:** Schloss Dagstuhl – Leibniz-Zentrum für Informatik
- **What it is:** the computer-science bibliography. **No abstracts, no full text, no PDFs** — just
  author-disambiguated, editorially curated bibliographic records for essentially every CS
  conference and journal that matters. It is the tool for answering *"did this preprint ever get
  published, and where?"*, which is step 3 of the ECCC sanity-check in §1.10.

**Size, by publication type** [API] parsed from the operator's own *Records in DBLP* statistics
export (`dblp.org/statistics/recordsindblp.html`, CSV download), harvested 2026-09-02, page
regenerated `03/09/2026 05:24:20`:

| Type | Records |
|---|---:|
| `INPROCEEDINGS` (conference papers) | **3,949,286** |
| `ARTICLE` (journal papers) | **3,482,111** |
| `INFORMAL` (**preprints — mostly arXiv**) | **974,897** |
| `BOOK` | 177,401 |
| `EDITOR` | 67,532 |
| `INCOLLECTION` | 55,879 |
| `DATA` | 26,738 |
| `REFERENCE` | 14,279 |
| `WITHDRAWN` | **289** |
| **Total** | **8,748,412** |

Two things to notice. **`INFORMAL` = 974,897** is dblp counting *preprints* as a first-class
publication type — that is dblp's own measure of how large the CS preprint literature has become,
and it is broadly consistent with arXiv's `cs` count of 931,100 in [`arxiv.md`](arxiv.md).
**`WITHDRAWN` = 289** is dblp tracking retractions explicitly, which almost nothing else in this
survey does.

**Bulk retrieval.** dblp publishes the entire database as **one gzipped XML file**,
`https://dblp.org/xml/dblp.xml.gz`, with its DTD alongside, under **CC0** — no registration, no
rate limit, no API key. That single file is the reason dblp is durable in the sense §14.4 defines:
thousands of independent copies exist. There is also an **RDF dump**, a **SPARQL endpoint**, and a
REST search API (`https://dblp.org/search/publ/api?q=<query>&format=json&h=<n>`).

**Reachability on the probe date — dblp was in trouble** [probe, 2026-09-04]:

| Probe | Result |
|---|---|
| `dblp.org/search/publ/api?q=RISC-V` | Failed twice with a non-JSON body, **succeeded on the third attempt: `@total` = 2,313** |
| `dblp.org/xml/dblp.xml.gz` | **HTTP 503**, 107-byte body |
| `dblp.uni-trier.de/search/publ/api` | **HTTP 500** (30,521 B error page) |
| `dblp.dagstuhl.de/search/publ/api` | **HTTP 503**, "No server is available to handle this request" |
| `dblp.uni-trier.de/xml/dblp.xml.gz` | **HTTP 503** |
| `dblp.dagstuhl.de/xml/dblp.xml.gz` | **HTTP 503** |

The operator's own statistics page carries two banners that explain it: *"Due to maintenance work,
this server will become temporarily unavailable during the next hour(s)"* and *"Over the past few
days, you may have noticed significant server instability across all dblp servers… there may still
be extended downtime on all dblp servers in the coming days."* [DOC, 2026-09-02].

**This is a transient outage, not a closure — and it is a nice illustration of the difference.**
All three mirrors were down for the XML dump simultaneously; the API answered on retry. Anyone
harvesting dblp should **retry with backoff and treat 503 as transient**, and should not conclude
anything from a single failed request. The `RISC-V` query result also shows dblp normalising the
query to `RISC* V` — hyphen handling again, the same class of issue flagged for Zenodo in the index.

---

## 15. Status and size table, with probe dates

Every row below was probed on the stated date(s). "Bulk dump" is called out because §14.4 shows it
is the single best predictor of whether a corpus survives its host.

| # | Server | Kind | Measured size | Metric | Evidence | Probe date(s) | Status | Open bulk dump? |
|---|---|---|---:|---|---|---|---|---|
| 1 | **ECCC** | repository | **4,832** | reports, 1994→ | [API] 33 year-index pages | 2026-09-02, 2026-09-04 | **active** | ✗ (no OAI, no API, no dump) |
| 2 | **OpenReview** | review platform | **4,634** | venue entries | [API] `groups?id=venues` | 2026-09-02 (4,621), 2026-09-04 (4,634) | **active, API challenge-gated** | ✗ |
| 3 | **ACL Anthology** | archive | **131,040** | BibTeX entries, 1952→ | [API] `anthology.bib.gz` parsed | 2026-09-02 (131,027), 2026-09-04 | **active** | ✓ **12.6 MB, one file** |
| 4 | **INSPIRE-HEP** | index + repository | **1,882,844** | literature records | [API] `/api/literature` | 2026-09-02 (1,882,221), 2026-09-04 | **active** | ✓ (API, unrestricted) |
| 5 | **CERN Document Server** | institutional repo | **578,928** total / **316,404** full text | OAI records | [API] OAI `completeListSize` | 2026-09-04 | **active; HTML+REST behind Anubis, OAI open** | ✓ (OAI-PMH) |
| 6 | **SciPost** | diamond OA journal | **12,558** | Crossref DOIs, prefix `10.21468` | [API] Crossref | 2026-09-04 | **active; site behind Anubis** | ✗ (site gated) |
| 7 | **Open Research Europe** | publish-then-review | **2,437** (Crossref) / 2,430 (DOI harvest) | works | [API] Crossref | 2026-09-02, 2026-09-04 | **active** | ✗ |
| 8 | **Peer Community In** | **overlay, hosts nothing** | **3,975** | Crossref DOIs, prefix `10.24072` | [API] Crossref | 2026-09-04 | **active** | ✗ |
| 9 | **VeriXiv** | repository | **812** | Europe PMC records | [API] Europe PMC | 2026-09-02, 2026-09-04 | **active** | ✗ |
| 10 | **Advance (SAGE)** | repository | **4,417** | Crossref DOIs, prefix `10.31124` | [API] Crossref | 2026-09-04 | **dormant** — no deposit since **2026-04-21**; front door Cloudflare 403 | ✗ |
| 11 | **Cambridge Open Engage** | platform | **5,738** | Crossref DOIs, prefix `10.33774` | [API] Crossref | 2026-09-04 | **active** — newest DOI **2026-09-04 05:50Z** | ✗ |
| 12 | **J-STAGE** | journal platform | *not measured* | — | [WEB] front page 200, 86,304 B | 2026-09-04 | **active**; OAI handler returned HTML | ✗ (WebAPI needs registration) |
| 13 | **KISTI ScienceON** | national aggregator | *not measured* | — | [WEB] `mainForm.do` 200, 336,305 B | 2026-09-04 | **active**; root is a 217-byte JS shell | ✗ (OpenAPI needs key) |
| 14 | **SSOAR** | repository | **101,200** | OAI records | [API] OAI `completeListSize` | 2026-09-02 | **active** | ✓ (OAI-PMH) |
| 15 | **alphaXiv** | **overlay on arXiv** | hosts nothing | — | [WEB] 200, 627,924 B | 2026-09-04 | **active** | n/a |
| 16 | **ar5iv** | **LaTeX→HTML renderer** | hosts nothing | — | [WEB] 200, 167,302 B; bogus id → true 404 | 2026-09-04 | **active** | n/a |
| 17 | **Hugging Face Papers** | **feed over arXiv** | hosts nothing | — | [WEB] 200, 314,513 B; bogus id → true 404 | 2026-09-04 | **active** | n/a |
| 18 | **Papers with Code** | index | — | — | [probe] 302 → `huggingface.co/papers/trending` | 2026-09-04 | **SHUT DOWN**; data at `hf.co/datasets/pwc-archive/*` (5 datasets, all HTTP 200) | ✓ **CC-BY-SA, mirrored** |
| 19 | **Semantic Scholar / S2ORC** | index + corpus | *not measured* | — | [probe] HTTP **429** / **500** unauthenticated | 2026-09-04 | **active, rate-limited** | ✓ (S2ORC, needs key) |
| 20 | **NASA ADS** | index | *not measured* | — | [probe] HTTP **401**, token mandatory | 2026-09-04 | **active, token-gated** | ✓ (API, needs token) |
| 21 | **dblp** | **bibliography, metadata only** | **8,748,412** (incl. **974,897** preprints, **289** withdrawn) | records | [API] operator statistics export | 2026-09-02 (page built 2026-09-03) | **active but unstable** — all 3 mirrors 503 on the dump; API OK on 3rd retry | ✓ **`dblp.xml.gz`, CC0** — when it serves |

### Probing-trap summary for these servers

Additions to the index's [§ Probing traps](README.md#6-probing-traps):

| Server | Trap | Correct test |
|---|---|---|
| **ECCC** | Soft-404: **HTTP 200** + **17,041 B** for any nonexistent path (`/about/`, `/report/1994/999/`); **17,032 B** for a nonexistent year | Body size, or grep the title for `404 page not found` |
| **OpenReview** | Under the challenge regime, `forum?id=<real>` and `forum?id=ZZZZZZZZZZ` both return **HTTP 200, 4,787 B** | Authenticate (`openreview-py`), or do not test existence at all |
| **OpenReview** | Per-venue `count` **caps at 10,000** — ICLR 2025 and 2026 both read exactly `10000` | Paginate with `offset`; never trust a round `count` |
| **CDS** | **Anubis** challenge served with **HTTP 200**, ~7.5 kB body, on HTML *and* REST. UA rotation does not help | Use OAI-PMH at `/oai2d` — completely open |
| **SciPost** | Same Anubis wall, **HTTP 200**, **3,903 B**, on the site *and* `/api/` | Crossref prefix `10.21468` |
| **Advance (SAGE)** | **HTTP 403**, 5,388–5,623 B = Cloudflare. **Blocked, not broken** | Crossref prefix `10.31124` + `sort=created&order=desc` for liveness |
| **VeriXiv / ORE** | Return **HTTP 200 and byte-identical 55,677 B** — same F1000 SPA shell under two brands | Crossref / Europe PMC |
| **KISTI ScienceON** | Root returns **HTTP 200, 217 B** — a JS bootstrap, not content | Request `/main/mainForm.do` |
| **dblp** | All three mirrors returned **503** for `dblp.xml.gz` simultaneously; the API failed twice then worked | Retry with backoff; 503 here is transient, not closure |
| **Crossref prefix endpoint** | *Positive* note: a bogus prefix (`10.99999`) returns an **error, not `0`** — so a number from `/prefixes/<p>/works?rows=0` is trustworthy | — |
| **Well-behaved (use as controls)** | **ACL Anthology** (true 404), **INSPIRE** (`total: 0`), **ar5iv** (true 404), **Hugging Face Papers** (true 404), **CDS OAI** (`noRecordsMatch`), **Europe PMC** (`hitCount: 0`) | — |

---

## 16. What is still missing

Stated so the gaps are visible rather than silent. This section is the honest counterpart to §15.

### 16.1 Numbers this pass could not obtain

| Wanted | Why not |
|---|---|
| **ICLR / NeurIPS true submission counts** | The API went behind a browser challenge between probe dates, and the harvested `count` values cap at 10,000. **The entire table in §2.3 is order-of-magnitude only.** |
| **OpenReview total note count** | Same cause. Never measured. |
| **ECCC rejection rate** | Unpublished. Not on the site, not in the three papers the operator cites about itself. |
| **ECCC eventual-publication rate** | No measurement found in the literature; this pass did not sample for one. |
| **J-STAGE record count** | OAI handler returned HTML; the WebAPI requires registration. |
| **KISTI ScienceON record count** | OpenAPI requires a key. |
| **Semantic Scholar / S2ORC corpus size** | HTTP 429 unauthenticated; needs a free API key not obtained. |
| **NASA ADS record count and `FPGA` hit count** | HTTP 401; token mandatory. |
| **CDS `cerncds:cs` set size** | The set is listed by `ListSets` but returned no `completeListSize`. |
| **SSOAR re-verification** | The 101,200 figure is from 2026-09-02 only; the 2026-09-04 re-probe did not return `completeListSize` on the first page. |
| **ECCC keyword→report counts** | 382 keyword pages exist; none were individually sized. |
| **Whether Advance (SAGE) is formally closed** | Front door is Cloudflare-blocked. Dormancy is evidenced (§9); closure is not. |

### 16.2 Conflicts recorded but not resolved

- **ORE: 1,513 vs 2,437.** A sibling record in this pass reports 1,513; two independent
  measurements here give 2,430–2,437. The likely explanation (approved articles vs all registered
  DOIs) was **not confirmed**. Both stand.
- **ECCC's own two removal policies contradict each other.** `/static/colloquium/how_to_use/` says
  a posted report *"cannot be removed"*; `/static/colloquium/copyright_notice/` says the author
  *"may withdraw the paper… iff the paper is accepted for publication elsewhere"*. Both live on
  2026-09-04.
- **ECCC total: 4,831 (2026-09-02) vs 4,832 (2026-09-04).** Recorded, not reconciled — the
  difference is one new report.
- **Papers with Code's README says data is "regenerated daily".** The dataset `lastModified`
  timestamps (2025-09-10, 2026-08-17) say otherwise. The README is stale.

### 16.3 Things not attempted at all

- **No landmark-paper verification outside ECCC.** §1.6 fetched and title-checked eleven ECCC
  reports individually. Nothing comparable was done for OpenReview, the ACL Anthology, CDS or
  INSPIRE. The Mamba example in §2.5 is verified [API] but is one paper.
- **No CDS or INSPIRE bulk harvest.** Set sizes were read from `completeListSize`; no records were
  actually pulled, so no claim is made about record quality or full-text availability per set.
- **No hardware-specific corpus analysis.** The INSPIRE keyword counts in §4.1 (`FPGA` 5,380,
  `ASIC` 2,869, `"radiation hard"` 1,932) are raw full-text search hits with **no de-duplication,
  no false-positive check and no negative control on the query terms themselves**. Treat them as
  evidence that the material exists, not as measurements of how much.
- **No eventual-publication rate for anything in this record.**
- **No licence audit.** Licensing statements in §1.9, §3.3, §14.4 are from operator pages; no
  per-record sampling was done.
- **Wikipedia's list was not re-read during this pass.** The "absent from Wikipedia's list" claims
  rest on the [index](README.md)'s enumeration of the 65 entries, not on a fresh check of the live
  article. Marked **[INF]**.

### 16.4 Servers deliberately not covered

Named so the next pass knows they were considered:

- **arXiv-adjacent overlay journals** (Discrete Analysis, SIGMA, Quantum) — real journals over
  arXiv, but journals, not repositories.
- **PubPeer** — post-publication comment layer; adjacent to §7's overlay logic but not a host.
- **CiteSeerX, CORE, BASE, OpenAIRE, OpenAlex** — aggregators/indexes. OpenAlex in particular is
  large enough to deserve its own record and did not get one.
- **National repositories** other than the three here (SSOAR, KISTI, J-STAGE): CNKI, Wanfang,
  CiNii, RePEc-adjacent national systems.
- **Institutional repositories generally** — DSpace/EPrints installations number in the thousands
  and are out of scope.
- **GitHub, GitLab, Zenodo software records** — covered in [`zenodo.md`](zenodo.md).

---

## 17. Sources

Primary evidence for this record is machine-readable and was retrieved on 2026-09-02 and
re-verified on 2026-09-04. Raw output is under
[`../../scratch/preprint-repositories/missing-servers/`](../../scratch/preprint-repositories/missing-servers/).

| # | URL | Retrieved | Supports |
|---|---|---|---|
| S1 | `https://eccc.weizmann.ac.il/year/<1994..2026>/` | 2026-09-02, 2026 re-verified 2026-09-04 | §1.3 per-year counts, §1.6 title scan |
| S2 | `https://eccc.weizmann.ac.il/report/<YYYY>/<NNN>/` (×11) | 2026-09-04 | §1.6 landmark verification, §1.5 revisions |
| S3 | `https://eccc.weizmann.ac.il/colloquium/call_for_papers/` | 2026-09-04 | §1.4 scope and editorial criteria |
| S4 | `https://eccc.weizmann.ac.il/colloquium/scientific_board/` | 2026-09-04 | §1.4 editorial board |
| S5 | `https://eccc.weizmann.ac.il/static/colloquium/how_to_use/` | 2026-09-04 | §1.5 revision/withdrawal semantics |
| S6 | `https://eccc.weizmann.ac.il/static/colloquium/copyright_notice/` | 2026-09-04 | §1.9 licensing |
| S7 | `https://eccc.weizmann.ac.il/static/colloquium/read_more/` | 2026-09-04 | §1.1 institutional history and [LIT] citations |
| S8 | `https://eccc.weizmann.ac.il/robots.txt`, `/feeds/reports/`, `/keywords/` | 2026-09-04 | §1.8 access surface |
| S9 | `https://api2.openreview.net/groups?id=venues` | 2026-09-02, 2026-09-04 | §2.2 venue counts |
| S10 | `https://api2.openreview.net/notes?forum=AL1fq05o7H` | 2026-09-02 | §2.5 Mamba reviews and scores |
| S11 | `https://api2.openreview.net/notes?...` (v1 and v2) | 2026-09-02 | §2.3 per-venue counts (caveated) |
| S12 | `https://openreview.net/forum?id=…`, `/pdf?id=…`, UA rotation ×6 | 2026-09-04 | §2.6 challenge blackout |
| S13 | `https://aclanthology.org/anthology.bib.gz` | 2026-09-02, 2026-09-04 | §3.2 size, types, per-year growth |
| S14 | `https://aclanthology.org/N19-1423/`, `.pdf`, `Z99-9999/` | 2026-09-04 | §3.3 access + negative control |
| S15 | `https://inspirehep.net/api/literature/…` and `/api/{conferences,jobs,institutions,data,experiments}` | 2026-09-02, 2026-09-04 | §4.1, §4.2 counts + negative control |
| S16 | `http://cds.cern.ch/oai2d?verb=Identify` | 2026-09-02, 2026-09-04 | §4.3 policies, `earliestDatestamp` |
| S17 | `http://cds.cern.ch/oai2d?verb=ListSets` | 2026-09-02 | §4.3 set inventory |
| S18 | `http://cds.cern.ch/oai2d?verb=ListIdentifiers&set=…` (×9 + bogus) | 2026-09-04 | §4.3 set sizes + negative control |
| S19 | `https://cds.cern.ch/api/records`, `/search` | 2026-09-02, 2026-09-04 | §4.4 Anubis trap |
| S20 | `https://api.crossref.org/prefixes/{10.21468,10.31124,10.33774,10.24072,10.12688,10.99999}/works` | 2026-09-04 | §5–§11 sizes + negative control |
| S21 | `https://api.crossref.org/prefixes/10.31124/works?sort=created&order=desc` | 2026-09-04 | §9 Advance dormancy |
| S22 | `https://api.crossref.org/prefixes/10.33774/works?sort=created&order=desc` | 2026-09-04 | §10 Cambridge Open Engage liveness |
| S23 | `https://api.crossref.org/works?filter=container-title:Open+Research+Europe` | 2026-09-04 | §6 ORE size conflict |
| S24 | `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=PUBLISHER:…` (×3) | 2026-09-04 | §6, §8 VeriXiv/ORE + negative control |
| S25 | `https://www.ssoar.info/OAIHandler/request?verb=ListIdentifiers` | 2026-09-02 | §13 size |
| S26 | `https://scipost.org/`, `/api/` | 2026-09-04 | §5 Anubis wall |
| S27 | `https://advance.sagepub.com/` with UA ×3 | 2026-09-04 | §9 Cloudflare 403 |
| S28 | `https://scienceon.kisti.re.kr/`, `/main/mainForm.do` | 2026-09-04 | §12 shell trap |
| S29 | `https://www.jstage.jst.go.jp/browse/-char/en`, `/oai/OAIHandler` | 2026-09-04 | §11 reachability |
| S30 | `https://paperswithcode.com/` (redirect chain) | 2026-09-04 | §14.4 shutdown |
| S31 | `https://huggingface.co/api/datasets/pwc-archive/*` (×5) | 2026-09-04 | §14.4 data survival + staleness |
| S32 | Papers with Code dataset README | 2026-09-02 | §14.4 dump list, CC-BY-SA licence |
| S33 | `https://dblp.org/statistics/recordsindblp.html` + CSV export | 2026-09-02 (page built 2026-09-03) | §14.7 record counts |
| S34 | `https://dblp.org/xml/dblp.xml.gz`, `dblp.uni-trier.de`, `dblp.dagstuhl.de` | 2026-09-04 | §14.7 outage |
| S35 | `https://dblp.org/search/publ/api?q=RISC-V` | 2026-09-04 | §14.7 retry behaviour, query normalisation |
| S36 | `https://ar5iv.labs.arxiv.org/html/{1706.03762,9999.99999}` | 2026-09-04 | §14.2 |
| S37 | `https://huggingface.co/papers/{1706.03762,2312.00752,9999.99999}` | 2026-09-04 | §14.3 |
| S38 | `https://www.alphaxiv.org/`, `/abs/2312.00752` | 2026-09-04 | §14.1 |
| S39 | `https://api.semanticscholar.org/graph/v1/paper/search*` | 2026-09-04 | §14.5 rate limit |
| S40 | `https://api.adsabs.harvard.edu/v1/search/query` | 2026-09-04 | §14.6 token requirement |
| S41 | [LIT] Meinel & Klotz, *"The first 10 years of the ECCC digital library"*, CACM 49(1):131–134, 2006; Bern, Meinel & Sack, SIGDOC 1998:113–119; Bern, Damm & Meinel, ECDL 1997:405–421 | cited by S7 | §1.1 — **citations taken from the operator's page; the papers themselves were not retrieved** |
