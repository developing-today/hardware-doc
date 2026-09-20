# arXiv — preprint repository record

- **URL:** https://arxiv.org/
- **Operator:** arXiv (transitioning to an independent non-profit; hosted at Cornell Tech since 2001)
- **Discipline scope:** physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering & systems science, economics
- **Launched:** 1991 · **Status:** active
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What it is

arXiv is the oldest and largest open-access preprint server in the physical and
computational sciences. A paper deposited here is world-readable, permanently, within
about one business day, at no cost to the author or the reader. It is not a journal: it
performs no peer review, confers no imprimatur of correctness, and makes no claim that
what it hosts is right. What it does provide is a **timestamped, immutable, permanently
addressable public record** that a specific document existed on a specific date under
specific authorship. For large parts of physics, mathematics and computer science, that
record — not the eventual journal version — is the object the field actually reads and
cites.

The server was created in August 1991 by physicist Paul Ginsparg, then at Los Alamos
National Laboratory, as an automated e-print distribution system for high-energy theory
(S3). It ran for a decade at Los Alamos, reachable at the address `xxx.lanl.gov` that a
generation of physicists typed from memory. When Ginsparg moved to Cornell as a professor
in 2001, he brought arXiv with him (S3), and it remained under Cornell's stewardship —
latterly at Cornell Tech — for the next 25 years.

That arrangement ended during the compilation window for this record. **On 1 July 2026
arXiv spun out of Cornell University to become an independent non-profit organisation**
(S4, S5, S3). arXiv's own announcement frames the goal as "greater organizational
flexibility, faster technological development, the ability to enter into expanded
partnerships, and creating a foundation for long-term financial sustainability" (S4).
Headquarters remain physically in Cornell Tech's Tata Innovation Center (S3). Dr. Penelope
Lewis, previously Chief Publishing Officer at AIP Publishing, took office as arXiv's
**inaugural CEO effective 17 August 2026** — two weeks before this record was compiled —
alongside a first Board of Directors (S6). Anyone reading this record should treat arXiv's
governance as *actively in transition*: the operator changed legal form ten weeks ago and
appointed its first chief executive two weeks ago.

Funding is philanthropic and institutional rather than transactional. The Simons
Foundation is the long-standing major funder and financed the cloud migration and code
modernisation project begun in 2023; in November 2025 arXiv announced **$7 million in
gifts and grants from Schmidt Sciences and NASA** to complete that migration and to build
discovery tooling (S7). Beyond that, arXiv is supported by **230 member institutions** plus
sponsors, affiliates and individual donors (S8). Submission and reading are free, and
arXiv's spinout announcement reiterated a commitment to remain "free to read and to submit
to" (S5).

> **Note on the Google Cloud claim.** arXiv publicly documents a "cloud migration and code
> modernization project" started in 2023 with Simons Foundation support and continued with
> Schmidt Sciences money (S7). I could **not** verify from any arXiv-published source that
> the target platform is specifically Google Cloud, nor that a CY2026 cutover occurred. The
> only "Google Cloud" string found anywhere in the harvested corpus was on the Kaggle
> dataset page, which refers to where the *metadata dump* is stored, not to arXiv's
> production infrastructure. **[NOT-VERIFIED]** — see §10.

## 2. Scope and subject taxonomy

arXiv is organised into archives (`cs`, `math`, `eess`, `quant-ph`, …), each divided into
categories with codes like `cs.DC`. Every paper has exactly one **primary** category and
may carry any number of **cross-lists**. The canonical enumeration is the category taxonomy
page (S9). What follows is the complete `cs.*` and `eess.*` listing as retrieved
2026-09-01, with the counts harvested in §3 folded in so the taxonomy and the volume data
can be read together.

### 2.1 Computer science — all 40 `cs.*` categories

Categories flagged ★ are the ones this knowledge base leans on most.

| Code | Name | Notes |
|---|---|---|
| `cs.AI` | Artificial Intelligence | Excludes vision, robotics, ML, multiagent, NLP — those have their own categories |
| ★ `cs.AR` | **Hardware Architecture** | Systems organisation and hardware architecture; ACM C.0, C.1, C.5 |
| `cs.CC` | Computational Complexity | Models of computation, complexity classes, bounds |
| `cs.CE` | Computational Engineering, Finance, and Science | Applications-oriented modelling of complex systems |
| `cs.CG` | Computational Geometry | ACM I.3.5, F.2.2 |
| `cs.CL` | Computation and Language | Natural language processing |
| ★ `cs.CR` | **Cryptography and Security** | All cryptography and security; ACM D.4.6, E.3 |
| `cs.CV` | Computer Vision and Pattern Recognition | Image processing, vision, scene understanding |
| `cs.CY` | Computers and Society | Ethics, IT policy, legal aspects, computing education |
| ★ `cs.DB` | **Databases** | Database management, data mining, data processing; ACM E.2, E.5, H.0, H.2, J.1 |
| ★ `cs.DC` | **Distributed, Parallel, and Cluster Computing** | Fault tolerance, distributed algorithms, parallel computation, clusters |
| `cs.DL` | Digital Libraries | Digital library design, document and text creation |
| `cs.DM` | Discrete Mathematics | Combinatorics, graph theory, applied probability |
| `cs.DS` | Data Structures and Algorithms | ACM E.1, E.2, F.2.1, F.2.2 |
| ★ `cs.ET` | **Emerging Technologies** | Information processing based on alternatives to silicon CMOS — nanoelectronics, photonics, bio-chemical |
| `cs.FL` | Formal Languages and Automata Theory | Automata, formal languages, grammars |
| `cs.GL` | General Literature | Introductory/survey material, biographies, miscellany |
| `cs.GR` | Graphics | All of ACM I.3 except I.3.5 |
| `cs.GT` | Computer Science and Game Theory | Mechanism design, learning in games |
| `cs.HC` | Human-Computer Interaction | Human factors, UIs, collaborative computing |
| `cs.IR` | Information Retrieval | Indexing, retrieval, content analysis |
| `cs.IT` | Information Theory | Alias-linked with `math.IT`; coding theory |
| `cs.LG` | Machine Learning | All aspects of ML research incl. robustness, fairness, methodology |
| `cs.LO` | Logic in Computer Science | Finite model theory, logics of programs, program verification |
| `cs.MA` | Multiagent Systems | Distributed AI, intelligent agents |
| `cs.MM` | Multimedia | ACM H.5.1 |
| `cs.MS` | Mathematical Software | ACM G.4 |
| `cs.NA` | Numerical Analysis | **Alias for `math.NA`** — carries no independent count |
| `cs.NE` | Neural and Evolutionary Computing | Neural nets, connectionism, genetic algorithms, artificial life |
| ★ `cs.NI` | **Networking and Internet Architecture** | Network architecture, protocols, internetwork standards, web caching |
| `cs.OH` | Other Computer Science | Catch-all for documents that fit nowhere else |
| ★ `cs.OS` | **Operating Systems** | ACM D.4.1–D.4.5, D.4.7, D.4.9 |
| `cs.PF` | Performance | Performance measurement and evaluation, queueing, simulation |
| ★ `cs.PL` | **Programming Languages** | Language semantics, features, paradigms; also compilers |
| `cs.RO` | Robotics | ACM I.2.9 |
| `cs.SC` | Symbolic Computation | ACM I.1 |
| `cs.SD` | Sound | Computing with sound, audio UIs, sonification, computer music |
| ★ `cs.SE` | **Software Engineering** | Design tools, metrics, testing, debugging, programming environments |
| `cs.SI` | Social and Information Networks | Design, analysis, modelling of social/information networks |
| `cs.SY` | Systems and Control | **Alias for `eess.SY`** — carries no independent count |

**The two aliases matter operationally.** `cs.NA` and `cs.SY` are not independent
categories: `cs.NA` is an alias for `math.NA` and `cs.SY` an alias for `eess.SY` (S9).
An API query on `cat:cs.NA` or `cat:cs.SY` returns **0** (S1) — not because nothing is
filed there, but because the canonical category string stored on the record is the
`math.NA` / `eess.SY` form. Anyone building a per-category harvest will silently lose
numerical-analysis and control-systems papers if they do not know this. **[API]**

### 2.2 Electrical engineering and systems science — all 4 `eess.*` categories

| Code | Name | Scope |
|---|---|---|
| `eess.AS` | Audio and Speech Processing | Analysis, synthesis, enhancement, transformation, classification of audio/speech signals |
| `eess.IV` | Image and Video Processing | Formation, capture, processing, communication, analysis, display of images/video |
| ★ `eess.SP` | **Signal Processing** | Theory, algorithms, performance analysis of signal and data analysis; physical modelling, detection, parameter estimation |
| ★ `eess.SY` | **Systems and Control** | All facets of automatic control systems; analysis and design using modern control tooling |

`eess` is a young archive relative to `cs` — it was carved out to give electrical
engineers a home that was neither `cs` nor `physics`. For a hardware-oriented knowledge
base, `eess.SP` and `eess.SY` are where communications PHY, radar, sensing, estimation
and control work lands, and they are frequently cross-listed with `cs.IT` and `math.OC`.

### 2.3 Adjacent categories worth knowing

| Code | Name | Why it matters here |
|---|---|---|
| `math.OC` | Optimization and Control | Operations research, LP, control theory, optimal control, game theory. Heavily cross-listed from `eess.SY` and `cs.LG` |
| `stat.ML` | Machine Learning (statistics) | ML with a statistical/theoretical emphasis; the standard cross-list partner of `cs.LG` |
| `quant-ph` | Quantum Physics | Where quantum algorithms, error correction, superconducting-qubit hardware and NISQ-era architecture papers live |
| `math.NA` | Numerical Analysis | Numerical algorithms for analysis and algebra; target of the `cs.NA` alias |
| `math.IT` | Information Theory | Alias for `cs.IT` |
| `physics.app-ph` | Applied Physics | Electronic devices, optics, photonics, microwaves, spintronics, metamaterials, nanotechnology |
| `cond-mat.mtrl-sci` | Materials Science | Synthesis, characterisation, defects, interfaces — the substrate layer under device papers |

## 3. Size and growth

This section is built from two independent primary sources that agree with each other:
arXiv's published monthly-submission series (S10), and a per-category harvest against the
arXiv API (S1). Where arXiv's blog states a milestone, I recompute it from the raw series
rather than repeating it.

### 3.1 Headline totals

| Quantity | Value | Source | Retrieved |
|---|---|---|---|
| Cumulative submissions, all time, through 2026-08 | **3,152,666** | computed from S10 monthly series | 2026-09-01 **[WEB]** |
| Cumulative submissions through 2026-06 | 3,091,806 | computed from S10 | 2026-09-01 **[WEB]** |
| arXiv's own statement, June 2026 | "cumulative submission count exceeds 3.08 million" | S3 | 2026-09-01 **[COM]** |
| arXiv's own statement, July 2026 | "now hosts over 3 million articles"; passed 3M in **April 2026** | S8 | 2026-09-01 **[DOC]** |
| Member institutions | 230 | S8 | 2026-09-01 **[DOC]** |
| Monthly active users | "over 5 million" visiting arxiv.org monthly | S8 | 2026-09-01 **[DOC]** |

**The recomputation matches the operator's claim.** My cumulative-through-June-2026 figure
of 3,091,806, derived by summing arXiv's own monthly CSV, sits exactly inside the Cornell
Chronicle's "exceeds 3.08 million" as of June 2026 (S3). Two independently published arXiv
artifacts agree to three significant figures. **[INF]**

### 3.2 Milestone cross-check — every claim recomputed from the raw series

arXiv's 3-million announcement (S8) makes four historical claims. All four survive
recomputation from the monthly CSV (S10):

| arXiv's claim (S8) | Recomputed cumulative (S10) | Verdict |
|---|---|---|
| "reached 500,000 papers hosted" in 2008 | 515,501 at end of 2008 | ✅ consistent |
| "1 million article mark just after Christmas in 2014" | 1,001,018 at end of 2014 | ✅ strikingly exact |
| "2 million mark in early 2022" | 1,999,642 at end of 2021 | ✅ crosses 2M in Jan 2022 |
| "In the year leading up to … 2 million … 181,630 new submissions" | 181,630 in calendar 2021 | ✅ exact match |

This is a rare case where an operator's promotional numbers are fully reproducible from
its own published data. It raises confidence in the rest of arXiv's self-reported figures.

### 3.3 Annual submission volume

| Year | Submissions | Cumulative |
|---|---|---|
| 1991 (from Aug) | 306 | 306 |
| 1995 | 13,014 | 33,423 |
| 2000 | 30,601 | 151,390 |
| 2005 | 46,855 | 350,721 |
| 2010 | 70,131 | 649,679 |
| 2014 | 97,517 | 1,001,018 |
| 2015 | 105,280 | 1,106,298 |
| 2016 | 113,380 | 1,219,678 |
| 2017 | 123,523 | 1,343,201 |
| 2018 | 140,616 | 1,483,817 |
| 2019 | 155,866 | 1,639,683 |
| 2020 | 178,329 | 1,818,012 |
| 2021 | 181,630 | 1,999,642 |
| 2022 | 185,692 | 2,185,334 |
| 2023 | 208,493 | 2,393,827 |
| 2024 | 244,031 | 2,637,858 |
| 2025 | 284,486 | 2,922,344 |
| 2026 (Jan–Aug, partial) | 231,929 | 3,154,273 |

Computed from S10, retrieved 2026-09-01. **[WEB]** Note the acceleration: 2022→2025
added 98,794 submissions/year of *additional annual throughput*, a ~53% increase in
three years. The 2026 partial year is already running above 2025's full-year pace.

### 3.4 Record months

arXiv's monthly record was broken three times in the first half of 2026:

| Month | Submissions | Note |
|---|---|---|
| 2026-03 | **30,045** | first month above 30,000 |
| 2026-05 | **31,604** | |
| 2026-06 | **32,040** | current all-time record |
| 2026-07 | 29,687 | seasonal dip |
| 2026-08 | 31,173 | |
| 2026-09 | 1,607 | partial — 1 September only |

All figures from S10, retrieved 2026-09-01 **[WEB]**, and independently confirmed in
arXiv's own narrative for March/May/June (S8) **[DOC]**. The `2026-09` row is a partial
month and must not be read as a monthly total; its presence is a useful sanity check that
the series was retrieved on 2026-09-01.

### 3.5 Is `cs` now arXiv's largest archive? — VERIFIED YES

Harvested against the arXiv API on 2026-09-01 using `search_query=cat:<archive>.*`, which
matches papers carrying that archive as **primary or cross-list**:

| Rank | Archive | Papers |
|---|---|---|
| 1 | **`cs.*`** | **931,100** |
| 2 | `math.*` | 682,304 |
| 3 | `cond-mat.*` | 413,036 |
| 4 | `physics.*` | 313,422 |
| 5 | `astro-ph.*` | 286,297 |
| 6 | `hep-ph` | 198,858 |
| 7 | `quant-ph` | 185,584 |
| 8 | `hep-th` | 185,241 |
| 9 | `eess.*` | 138,247 |
| 10 | `stat.*` | 132,573 |
| 11 | `gr-qc` | 124,304 |
| 12 | `math-ph` | 91,943 |
| 13 | `nucl-th` | 63,420 |
| 14 | `hep-ex` | 61,194 |
| 15 | `q-bio.*` | 55,103 |
| 16 | `nlin.*` | 47,668 |
| 17 | `hep-lat` | 30,729 |
| 18 | `nucl-ex` | 28,870 |
| 19 | `q-fin.*` | 18,931 |
| 20 | `econ.*` | 17,253 |

**[API]** — retrieved 2026-09-01.

**Verdict: the claim is confirmed.** `cs.*` at 931,100 is the largest archive on arXiv by
a margin of ~249,000 papers over `math.*`, and roughly 3× the `physics.*` archive that
arXiv was founded to serve. A server built in 1991 for high-energy theory is now, by
volume, a computer science server. **[API]**

Two caveats on interpretation. (a) These are *cross-list-inclusive* counts, so a paper
that is primary `cs.LG` and cross-listed to `stat.ML` is counted in both `cs.*` and
`stat.*`; the columns do not sum to the archive total. (b) The count is of papers, not of
submissions/versions, so it is not directly comparable to the 3.15M submission figure in
§3.1. **[INF]**

### 3.6 Per-category counts — all 40 `cs.*`, ranked

The single most useful machine-readable artifact in this record. Harvested 2026-09-01 via
`https://export.arxiv.org/api/query?search_query=cat:<CODE>&max_results=1`, reading
`opensearch:totalResults`. **[API]**

| Rank | Code | Name | Papers |
|---|---|---|---|
| 1 | `cs.LG` | Machine Learning | 283,807 |
| 2 | `cs.CV` | Computer Vision and Pattern Recognition | 204,123 |
| 3 | `cs.AI` | Artificial Intelligence | 197,852 |
| 4 | `cs.CL` | Computation and Language | 117,997 |
| 5 | `cs.RO` | Robotics | 57,451 |
| 6 | `cs.IT` | Information Theory | 55,845 |
| 7 | ★ `cs.CR` | Cryptography and Security | 51,581 |
| 8 | `cs.HC` | Human-Computer Interaction | 32,545 |
| 9 | `cs.CY` | Computers and Society | 30,192 |
| 10 | ★ `cs.DC` | Distributed, Parallel, and Cluster Computing | 29,886 |
| 11 | `cs.DS` | Data Structures and Algorithms | 29,806 |
| 12 | ★ `cs.SE` | Software Engineering | 29,164 |
| 13 | ★ `cs.NI` | Networking and Internet Architecture | 28,226 |
| 14 | `cs.IR` | Information Retrieval | 26,920 |
| 15 | `cs.SI` | Social and Information Networks | 23,845 |
| 16 | `cs.SD` | Sound | 21,863 |
| 17 | `cs.LO` | Logic in Computer Science | 20,089 |
| 18 | `cs.NE` | Neural and Evolutionary Computing | 18,206 |
| 19 | `cs.DM` | Discrete Mathematics | 16,052 |
| 20 | `cs.GT` | Computer Science and Game Theory | 15,406 |
| 21 | `cs.MA` | Multiagent Systems | 13,485 |
| 22 | `cs.CC` | Computational Complexity | 13,309 |
| 23 | ★ `cs.DB` | Databases | 12,304 |
| 24 | `cs.CE` | Computational Engineering, Finance, and Science | 11,162 |
| 25 | ★ `cs.PL` | Programming Languages | 10,261 |
| 26 | `cs.MM` | Multimedia | 10,010 |
| 27 | `cs.GR` | Graphics | 9,689 |
| 28 | ★ `cs.AR` | **Hardware Architecture** | 8,932 |
| 29 | `cs.CG` | Computational Geometry | 8,317 |
| 30 | ★ `cs.ET` | **Emerging Technologies** | 7,815 |
| 31 | `cs.DL` | Digital Libraries | 6,294 |
| 32 | `cs.FL` | Formal Languages and Automata Theory | 6,186 |
| 33 | `cs.PF` | Performance | 5,536 |
| 34 | `cs.SC` | Symbolic Computation | 3,231 |
| 35 | `cs.MS` | Mathematical Software | 2,741 |
| 36 | `cs.OH` | Other Computer Science | 2,321 |
| 37 | ★ `cs.OS` | **Operating Systems** | 1,455 |
| 38 | `cs.GL` | General Literature | 245 |
| 39 | `cs.NA` | Numerical Analysis | 0 — *alias for `math.NA`* |
| 40 | `cs.SY` | Systems and Control | 0 — *alias for `eess.SY`* |

### 3.7 `eess.*` and adjacent categories

| Code | Name | Papers |
|---|---|---|
| ★ `eess.SY` | Systems and Control | 47,937 |
| ★ `eess.SP` | Signal Processing | 41,815 |
| `eess.IV` | Image and Video Processing | 31,534 |
| `eess.AS` | Audio and Speech Processing | 22,281 |
| | | |
| `quant-ph` | Quantum Physics | 185,584 |
| `stat.ML` | Machine Learning (statistics) | 79,758 |
| `math.OC` | Optimization and Control | 63,892 |
| `cond-mat.mtrl-sci` | Materials Science | 111,931 |
| `physics.app-ph` | Applied Physics | 24,140 |

**[API]** — retrieved 2026-09-01.

### 3.8 What these numbers do and do not mean

- **The `cs.*` per-category counts sum to 1,424,149**, against an archive total of 931,100.
  The 1.53× ratio is the average number of `cs` categories per `cs` paper. Cross-listing is
  the norm, not the exception, and **you must never sum category counts** to get a total.
  **[INF]**
- **`cs.LG` alone (283,807) exceeds the entire `eess.*` archive (138,247) twofold**, and is
  roughly 32× the size of `cs.AR`. The ML categories dominate arXiv computer science so
  heavily that generic `cs` volume statistics are effectively ML statistics. **[INF]**
- **The hardware-relevant categories are small.** `cs.AR` (8,932), `cs.ET` (7,815) and
  especially `cs.OS` (1,455) are among the smallest on the server. `cs.OS` is smaller than
  `cs.GL`+`cs.OH`+`cs.MS` combined. For an operating-systems or architecture literature
  search, arXiv is a **thin** source and must be supplemented — see §7.8 on what is
  missing. **[INF]**
- **Counts are of current papers, not submissions.** Withdrawn papers remain addressable
  (§5), and a paper with nine versions counts once.

## 4. Screening and moderation — what gets in

arXiv's gate has three independent stages: **endorsement** (who may submit at all),
**moderation** (whether a given submission is announced), and **post-announcement
moderation** (reclassification and withdrawal). None of them is peer review, and arXiv
says so explicitly: *"Please note that the arXiv moderation process is not a peer-review
process. arXiv staff and moderators cannot give feedback on the submission."* (S11)
**[DOC]**

### 4.1 Endorsement — the author-side gate

arXiv requires that users **be endorsed before submitting their first paper to arXiv or a
new category** (S12). The endorsement graph works like this:

- **Endorsement is per-domain, not global.** Endorsement is granted within an
  *endorsement domain* — a high-level subject area. Most archives (`hep-th`, `cond-mat`,
  `q-bio`) are single endorsement domains; `physics` is the notable exception, where
  individual subject classes are separate domains (S12, S13). Being endorsed in `cs` does
  not endorse you in `math`.
- **Who may endorse.** An endorser must have authored a threshold number of papers within
  that endorsement domain. arXiv does not publish the per-domain number, saying only that
  it "has been set so that any active scientist who has been working in their field for a
  few years should be able to endorse." Crucially, **only papers submitted between three
  months and five years ago count** — a recency window that keeps the endorser pool
  active, and that silently strips endorsement power from researchers who have stopped
  posting (S12). **[DOC]**
- **The endorser must themselves be endorsed.** "You must also have an active positive
  endorsement to that area yourself before you may endorse for that subject
  classification" (S12). The graph is therefore rooted and transitively closed —
  endorsement power propagates only from existing endorsed authors.
- **One positive endorsement suffices.** "At least one positive endorsement is required
  per endorsement category to be considered endorsed for that category" (S12).
- **Endorsers are anonymous, and negatives are recorded.** Whether you endorsed is
  "private between you and the arXiv administrators." A declined endorsement is "recorded
  as a negative vote of endorsement" (S12). Neither the requester nor the public sees it.
- **Endorsement is revocable** — arXiv "reserves the right to revoke any submitter's
  endorsement if that submitter has violated arXiv policies" (S12).
- **Endorsement is explicitly not review.** "We do not expect you to read the paper in
  detail, or verify that the work is correct, but you should check that the paper is
  appropriate for the subject area" (S12). An endorsement is a statement about
  *community membership*, not correctness.

#### 4.1.1 The January 2026 endorsement tightening — a material change

This is recent and it changes who can publish on arXiv. **As of 21 January 2026, arXiv no
longer accepts an institutional email address as the sole qualifier for endorsement**
(S14). New submitters now face two paths:

1. **Automatic**: an institutional email address from an academic/research institution
   **AND** previous authorship on an existing arXiv paper in the target endorsement domain.
2. **Personal**: direct endorsement from an established arXiv author in the same domain.

arXiv's stated reason is blunt: *"in recent years, arXiv has received an unsustainable
increase in the number of non-scientific submissions, increasing the rejection rate and
requiring excessive moderation and staff effort. Because of this, we have determined that
institutional email addresses are no longer a sufficient credential for determining
minimum research competence"* (S14). **[DOC]**

The change was piloted in arXiv Mathematics in **December 2025** before the
all-categories rollout (S14, S15). Existing endorsements were grandfathered: "Authors who
were previously endorsed to submit to a particular category will still be endorsed in that
category" (S14).

**Who is effectively exempt.** There is no formal exemption list, but three groups pass
the gate without friction: (a) anyone already endorsed in the domain, (b) anyone who has
claimed authorship on a prior arXiv paper in the domain *and* holds an institutional
address, and (c) co-authors submitting through an already-endorsed submitting author —
endorsement attaches to the *submitter*, so a student's paper submitted by their advisor
requires no endorsement of the student. **[INF from S12, S14]**

**Who is now excluded.** Independent researchers without institutional affiliation,
industry researchers on corporate email, and researchers changing fields all now require
a personal endorsement they must solicit by cold email. arXiv states flatly that "arXiv
staff cannot waive endorsement requirements or provide a personal endorsement" (S14).
This is a real and widening barrier — see §10.

### 4.2 Moderation — the submission-side gate

Moderation happens **after submission and before public announcement** (S11). Grounds for
declining, per arXiv's own published list (S11) **[DOC]**:

| Ground | Substance |
|---|---|
| Scholarly standards | Form: "appropriate and carefully prepared sections, figures, tables, references"; professional language; "sufficiently neutral tone"; "general scrupulousness and care of preparation" |
| Scholarly interest | May be declined if it "lacks originality, novelty, significance, and/or contains falsified, plagiarized content or serious misrepresentations of data, affiliation, or content" |
| Not research | "course projects, research proposals, news, or information about political causes" |
| Content type | Research articles are "the primary content-type"; other types are governed by specific policies |
| Out of scope | "Submissions may be declined if they do not fit into our current classification scheme or we do not currently serve the community" |
| Duplicated content | Multiple similar submissions may be required to be "consolidated or versioned" |
| Rights | Must be the author's original work, no verbatim referee comments, no third-party-barred material |
| Excessive submission rate | **"we ask that they submit no more than three papers per day"** |
| Images | Images "likely to cause egregious offense may be declined or removed" — arXiv names the "Lena" image explicitly as a problem case |

**Generative AI policy** (S11): arXiv requires authors "to report in their work any
significant use of sophisticated tools … we now include in particular text-to-text
generative AI"; reminds authors that they "take full responsibility for all its contents,
irrespective of how the contents were generated"; and rules that "generative AI language
tools should not be listed as an author."

**Prior publication is neither necessary nor sufficient.** "arXiv moderation decisions may
be influenced by the publication status of the submission, but prior publication does not
guarantee acceptance in arXiv" (S11). And there is an escalating-scrutiny rule: "Submitters
who have had works previously delayed or declined by arXiv should anticipate closer
scrutiny on future submissions. In some cases, authors may be required to establish a
conventional publication record and limit their submissions to works that are published in
conventional journals" (S11). **[DOC]**

**Who the moderators are.** "arXiv moderators are volunteer subject matter experts with
terminal degrees in their field … approved by their discipline-level advisory committees
and by arXiv staff" (S11). arXiv reports "hundreds of volunteer moderators" (S8).
Moderation is confidential — moderators "consider the submissions to arXiv as privileged
information, as they would with a paper being refereed for a journal" (S11). **It is
"inappropriate to contact any moderator directly regarding your submission"** (S11).

**Holds.** A submission that is neither announced nor declined sits *on hold*. arXiv does
not publish hold durations or a hold-rate statistic. Its own stated rationale for the
October 2025 review-article change includes the goal to "reduce submission hold times"
(S16), which is an implicit admission that hold times had become a problem, but **I could
not find any published figure for mean or median hold time, nor a published
accept/decline/hold rate. [NOT-VERIFIED]**

### 4.3 The October 2025 `cs.*` review-article and position-paper policy — VERIFIED

The user asked me to verify a recent policy change requiring prior peer review for surveys
in `cs.*`. **It exists.** Announced 31 October 2025 (S16). Direct quote:

> "arXiv's computer science (CS) category has updated its moderation practice with respect
> to review (or survey) articles and position papers. **Before being considered for
> submission to arXiv's CS category, review articles and position papers must now be
> accepted at a journal or a conference and complete successful peer review.** When
> submitting review articles or position papers, authors must include documentation of
> successful peer review to receive full consideration. Review/survey articles or position
> papers submitted to arXiv without this documentation will be likely to be rejected and
> not appear on arXiv." (S16) **[DOC]**

Key details, all quoted from S16:

- **Scope: `cs.*` only.** Other archives were unaffected at announcement. arXiv said other
  categories "may choose to change their moderation practices in a similar manner" if they
  see a similar rise, and "We will make these updates public if and when they do occur."
- **arXiv denies it is a policy change**: *"Technically, no! … review articles and position
  papers are not (and have never been) listed as part of the accepted content types."*
  They had previously been accepted "only at moderator discretion."
- **The stated cause is LLM-generated volume**: *"arXiv has been flooded with papers.
  Generative AI / large language models have added to this flood by making papers –
  especially papers not introducing new research results – fast and easy to write."*
- **The scale**: arXiv "now receive[s] hundreds of review articles every month," and "the
  majority of the review articles we receive are little more than annotated bibliographies,
  with no substantial discussion of open research issues."
- **Workshop review does not count**: *"the review conducted at conference workshops
  generally does not meet the same standard of rigor of traditional peer review and is not
  enough."*
- **Evidence required**: "include the peer reviewed journal reference and DOI metadata. If
  you do not provide this, your review article or position paper will likely be rejected."
- **Carve-out**: scientific research papers *studying* the societal impact of technology
  are unaffected — "arXiv has always released these types of scientific papers, for example
  in `cs.CY` or `physics.soc-ph`."
- **Appeals**: a rejected survey may be resubmitted only after an accepted appeal following
  successful peer review; "Do not resubmit … without an accepted appeal."

**Practical consequence for this knowledge base.** Any `cs.*` survey or benchmark-review
posted to arXiv **after 31 October 2025** should carry a journal/conference reference and
DOI. A `cs.*` survey from that period *without* one is anomalous and worth a second look.
Conversely, the huge stock of pre-2025 `cs` surveys on arXiv was never subject to this bar
and carries no such implied vetting. **[INF]**

### 4.4 After announcement — reclassification, withdrawal, permanence

**Once announced, a paper is permanent.** "Once a paper is announced it becomes part of the
permanent scholarly record. arXiv will only consider requests for removal if the submitter
did not have the legal right to agree to the license" (S11). **[DOC]**

**Reclassification** happens both before and after announcement: "arXiv may reclassify
already announced papers if the moderators determine there is a more appropriate category,"
and cross-lists "may be removed by moderators when the classification is deemed
inappropriate" (S11).

**Withdrawal semantics — the critical detail.** A withdrawal does **not** remove the paper.
Per arXiv's own withdrawal page (S17) **[DOC]**:

> "Articles that have been announced and made public cannot be completely removed. **A
> withdrawal creates a new version of the paper marked as withdrawn.** That new version
> displays the reason for the withdrawal and does not link directly to the full text.
> **Previous versions will still be accessible, including the full text.**"

So a withdrawn paper's v1 PDF remains publicly retrievable forever at
`arxiv.org/abs/<id>v1`. Retraction on arXiv is a *labelling* operation layered on top of an
append-only store, not a deletion. This is the single most important thing to understand
about arXiv's error model — see §5.4.

arXiv further constrains *why* you may withdraw (S17): it is "not appropriate to withdraw a
paper because it is published or submitted to a journal" (add a `journal-ref` instead), nor
"because it is being updated" (submit a replacement instead), nor for copyright infringement
(a separate process). Withdrawal reasons "will be displayed publicly."

Before announcement the picture is different: an unannounced submission can be genuinely
**deleted** or **unsubmitted** back to incomplete status (S17). The permanence rule attaches
at announcement, not at submission.

## 5. Reliability — what you can and cannot trust

### 5.1 What an arXiv ID guarantees

An arXiv identifier is a strong claim about **provenance and time**, and a null claim about
**correctness**.

| Guaranteed | Not guaranteed |
|---|---|
| The document existed in that exact form on that date (per-version timestamps to the second, exposed via the API `published`/`updated` fields) **[API]** | That it is correct |
| The version is immutable — v1 never changes; edits create v2, v3, … (S18) | That it was peer reviewed |
| Every prior version stays retrievable, including for withdrawn papers (S17) | That the claimed affiliations are real |
| Permanent addressability: `arxiv.org/abs/<id>` and `arxiv.org/abs/<id>vN` | That the results replicate |
| The submitter passed the endorsement gate in that domain (§4.1) | That the submitter is the author (endorsement checks community membership, not authorship) |
| A moderator judged it in-scope and minimally scholarly (§4.2) | That a moderator read it carefully — arXiv says they cannot give feedback (S11) |

The timestamp is the product. Everything else is a by-product.

### 5.2 Versioning and priority claims

Version numbers are the mechanism by which arXiv supports priority claims. A useful
worked example from the verified landmark set: **`1706.03762` (*Attention Is All You Need*)
was published 2017-06-12 and last updated 2023-08-02, at v7** (S1) **[API]**. Six years of
revisions to a paper that was "finished" in 2017, all publicly diffable by fetching each
`v1`…`v7`. Similarly `1412.6980` (*Adam*) sits at **v9** and `1409.0473` (Bahdanau
attention) at **v7** (S1).

Practical consequences:

- **Always cite a version if the claim matters.** "As shown in 1706.03762" is ambiguous
  across seven documents. `1706.03762v1` is not.
- **The v1 date, not the paper date, is the priority date.** The API `published` field is
  the v1 timestamp; `updated` is the latest version. Reading `updated` as the publication
  date is a common and serious error in automated bibliometrics. **[INF]**
- **A high version count is not a quality signal in either direction.** It can mean
  sustained community engagement (Adam, v9) or repeated correction.

### 5.3 The eventual-publication rate — what I could and could not establish

The template asks for measured eventual-publication rates from the scientometric
literature. **I could not verify a specific rate from a source I actually retrieved.**
**[NOT-VERIFIED]**

What I tried, all on 2026-09-01 against the arXiv API (S1):

| Query | Result |
|---|---|
| `abs:"fraction of arXiv preprints" AND abs:"published"` | 0 results |
| `ti:"preprint" AND ti:"publication rate" AND cat:cs.DL` | 0 results |

I am aware of commonly-cited figures in the region of 60–75% for arXiv-wide eventual
journal publication, but **I did not retrieve a primary source for any of them during this
pass and will not launder a remembered number into this record.** Anyone extending this
record should look at the `cs.DL` literature and at Cornell/arXiv's own annual reports.

**What can be measured directly, and is more useful anyway:** arXiv exposes `journal_ref`
and `doi` metadata fields via the API, so the "has it been published" question is
answerable per-paper and in bulk without relying on any literature estimate. In the
71-paper verified landmark harvest (§7), **only 6 carry a `journal_ref`** — Shor
(`quant-ph/9508027`), the transmon paper (`cond-mat/0703002`), surface codes (`1208.0928`),
Preskill's NISQ paper (`1801.00862`), the Google quantum-supremacy supplement
(`1910.11333`), the LSM survey (`1812.07527`), and DeepSeek-R1 (`2501.12948`) carries a
*Nature* reference. **[API]** That is a striking result and it is the subject of §5.5:
almost none of the most influential CS papers on arXiv have journal metadata attached, even
when they were in fact published.

> **Caveat on that measurement.** A missing `journal_ref` means *the author never added
> one*, not that the paper was never published. `1706.03762` was published at NeurIPS 2017
> and has no `journal_ref`. So `journal_ref` coverage is a **lower bound** on publication
> and a poor proxy for it. Do not invert it. **[INF]**

### 5.4 Failure modes

**Permanence of error.** Because withdrawal is a labelling operation over an append-only
store (§4.4), a wrong result posted to arXiv is retrievable forever. The v1 PDF of a
withdrawn paper stays at `arxiv.org/abs/<id>v1`. Citation managers, scrapers, LLM training
corpora and the S3 bulk buckets (§8) all captured it. Retraction propagates weakly: the
abstract page shows the withdrawal notice, but a cached PDF, a `ar5iv` HTML rendering or a
third-party mirror generally does not.

**LLM-generated submissions.** This is not speculative — it is arXiv's own stated reason
for two policy changes inside twelve months. The October 2025 review-article rule cites
LLMs "making papers … fast and easy to write" and characterises the majority of incoming
surveys as "little more than annotated bibliographies" (S16). The January 2026 endorsement
change cites an "unsustainable increase in the number of non-scientific submissions" (S14).
arXiv's incoming CEO named "the rise of AI-generated preprints" as one of three challenges
she was appointed to address (S6). **[DOC]**

**Salami slicing.** arXiv's countermeasure is the explicit rate limit — "we ask that they
submit no more than three papers per day" — plus the duplicated-content rule under which
moderators "may request that the submissions be consolidated or versioned" (S11). Both are
requests backed by discretion, not hard technical limits.

**Unreviewed claims propagating via press.** arXiv IDs look like citations and are treated
as such by journalists and by downstream automated systems. Nothing in an arXiv ID
distinguishes a NeurIPS best-paper from a submission that a volunteer moderator waved
through as in-scope. The endorsement gate filters *who*, the moderation gate filters
*whether it is science*; neither filters *whether it is right*.

**Category gaming.** Because cross-listing is free and near-universal (§3.8: 1.53 `cs`
categories per `cs` paper), authors can and do cross-list into high-traffic categories for
visibility. Moderators may remove inappropriate cross-lists (S11), but this is reactive.

### 5.5 The ML/systems dynamic — when arXiv *is* the version of record

In machine learning and increasingly in ML systems, the arXiv version is not a preprint of
the real paper; **it is the real paper**. The evidence from the verified landmark harvest
(§7) is direct:

- **Of 71 verified landmark papers, 65 carry no `journal_ref` at all** (S1) **[API]**,
  including *Attention Is All You Need*, ResNet, Adam, BERT, GPT-3, ViT, CLIP, LLaMA,
  FlashAttention, vLLM and Mamba. These are among the most-cited papers in modern computing
  and their arXiv records are bare of publication metadata.
- Several were **never conventionally published at all**. `1603.04467` (TensorFlow) is a
  whitepaper. `2302.13971` (LLaMA) and `2005.14165` (GPT-3, though it appeared at NeurIPS)
  were consumed by the field as arXiv documents on the day they appeared.
- arXiv itself makes the claim: "arXiv is such a foundational infrastructure for sharing
  research that **many papers appear *only* on arXiv**" (S8). **[DOC]**
- The `1512.03385` (ResNet) record carries the author comment **"Tech report"** (S1) — the
  authors' own framing of a paper that won CVPR 2016 and became one of the most-cited works
  in the history of computer science.

The practical upshot: in these fields, "is it peer reviewed?" is close to the wrong
question, because the community's actual quality signal is post-hoc — reproduction,
citation, and whether the code runs. But the corollary is that **the reader inherits the
entire burden of evaluation**, with none of the (imperfect) filtering a venue would supply.

### 5.6 How to sanity-check an individual arXiv paper

A concrete procedure, all steps machine-executable against the API (S1):

1. **Resolve the ID and confirm the title matches your citation.** Mismatch means a
   transposed digit — see the negative control in §8.6.
2. **Check `published` vs `updated`.** A large gap means substantive revision; diff v1
   against vN if the claim is load-bearing.
3. **Check for a withdrawal notice** on the abstract page. Remember the full text is still
   there, so absence of a broken link is not absence of a retraction.
4. **Read `journal_ref` and `doi` if present** — but treat absence as uninformative (§5.3).
5. **Check the primary category against the content.** A hardware claim filed primary
   `cs.GL` or `cs.OH` is a signal.
6. **Check the author comment field**, which conventionally carries venue acceptance
   ("Accepted at NeurIPS 2024"), page counts, and errata notes.
7. **For post-2025-10-31 `cs.*` surveys, require a journal-ref/DOI** — arXiv now does
   (§4.3).
8. **Check whether the endorsement path is plausible**: a paper by authors with no other
   arXiv presence in that domain, posted after January 2026, went through a personal
   endorsement.

## 6. What you actually find there — examples

Concrete document types a systems or electronics engineer will actually encounter:

- **Model and system release papers that never go to a venue.** `1603.04467` —
  *TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems*
  (2016-03-14, primary `cs.DC`) is a whitepaper. `1912.01703` — *PyTorch: An Imperative
  Style, High-Performance Deep Learning Library* (2019-12-03). `2302.13971` — *LLaMA*
  (2023-02-27). These are the primary technical documentation for infrastructure that
  millions of people run. **[API]**
- **Simulator and toolchain papers.** `2007.03152` — *The gem5 Simulator: Version 20.0+*
  (2020-07-07, `cs.AR`), the citable reference for the standard computer-architecture
  simulator. `2002.11054` — *MLIR: A Compiler Infrastructure for the End of Moore's Law*
  (2020-02-25, `cs.PL`). **[API]**
- **Vulnerability disclosures.** `1801.01203` (*Spectre*) and `1801.01207` (*Meltdown*)
  were both posted 2018-01-03 — the coordinated-disclosure day. arXiv served as the
  publication channel for two of the most consequential hardware security findings ever
  made. **[API]**
- **Retrospectives and "selected papers" reissues.** `1904.09724` *RowHammer: A
  Retrospective* and `2306.16093` *Retrospective: Flipping Bits in Memory Without Accessing
  Them*. Note the second one: the **original** RowHammer paper (ISCA 2014) is not on arXiv
  — only its 2023 retrospective is. A title search for "Flipping Bits in Memory Without
  Accessing Them" returns exactly **1** hit, and it is the retrospective (S1). **[API]**
- **Industrial hardware measurement papers.** `1704.04760` — *In-Datacenter Performance
  Analysis of a Tensor Processing Unit* (2017-04-16, `cs.AR`), Google's TPUv1 paper.
- **Blockchain and consensus protocol specifications.** `1607.01341` (*Algorand*, at v9),
  `1803.05069` (*HotStuff*), `1807.04938` (*The latest gossip on BFT consensus* — the
  Tendermint paper), `1710.09437` (*Casper the Friendly Finality Gadget*). For this
  subfield arXiv, alongside IACR ePrint, is the primary venue.
- **Communications theory that became standards.** `0807.3917` — Arıkan's *Channel
  polarization* (2008-07-24, `cs.IT`), the paper behind the polar codes adopted for 5G NR
  control channels.
- **Category-defining surveys** — from before the October 2025 rule (§4.3). `1703.09039`
  *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*; `1812.07527`
  *LSM-based Storage Techniques: A Survey* (with a VLDB Journal reference attached).
- **Benchmarks as papers.** `2310.06770` *SWE-bench*, `2107.03374` *Evaluating Large
  Language Models Trained on Code* (the HumanEval/Codex paper).
- **Foundational quantum results.** `quant-ph/9508027` (Shor, 1995) and `quant-ph/9605043`
  (Grover, 1996) are on arXiv, in the original archive, with 30-year-old identifiers that
  still resolve.

## 7. Landmark papers

This is the core deliverable. **Every row below was verified on 2026-09-01 by querying the
arXiv API and confirming that the identifier resolves to an entry whose title matches**
(S1). Dates are the **v1 `published` timestamp** from the API — the priority date, not the
last-updated date. **[API]** for every identifier, date, primary category and `journal_ref`
in these tables.

**Method note on the "arXiv first?" column.** I do not assert venue publication dates I
did not retrieve. The column reports one of:

- **✅ proven** — the record carries a `journal_ref` or `doi` whose year is *later* than the
  arXiv v1 date, so arXiv demonstrably came first. Provable from the API alone.
- **✅ de facto** — no venue metadata is attached at all. arXiv is the only citable record
  the authors ever supplied; whatever happened at a venue, the arXiv document is what the
  field reads and cites. (See §5.3 — absence of `journal_ref` does **not** prove absence of
  publication.)
- **≈ same-year** — venue metadata exists with the same year as v1; ordering within the year
  is not provable from the metadata I retrieved.

### 7.1 Machine learning — foundational

| Paper | arXiv ID | v1 date | Primary | Why it matters | arXiv first? |
|---|---|---|---|---|---|
| Improving neural networks by preventing co-adaptation of feature detectors (Dropout) | [1207.0580](https://arxiv.org/abs/1207.0580) | 2012-07-03 | `cs.NE` | Introduced dropout regularisation | ✅ de facto |
| Efficient Estimation of Word Representations in Vector Space (word2vec) | [1301.3781](https://arxiv.org/abs/1301.3781) | 2013-01-16 | `cs.CL` | Made dense word embeddings standard | ✅ de facto |
| Playing Atari with Deep Reinforcement Learning (DQN) | [1312.5602](https://arxiv.org/abs/1312.5602) | 2013-12-19 | `cs.LG` | Launched deep reinforcement learning | ✅ de facto |
| Generative Adversarial Networks | [1406.2661](https://arxiv.org/abs/1406.2661) | 2014-06-10 | `stat.ML` | Created the GAN research programme | ✅ de facto |
| Neural Machine Translation by Jointly Learning to Align and Translate | [1409.0473](https://arxiv.org/abs/1409.0473) | 2014-09-01 | `cs.CL` | The attention mechanism itself; now at v7 | ✅ de facto |
| Very Deep Convolutional Networks for Large-Scale Image Recognition (VGG) | [1409.1556](https://arxiv.org/abs/1409.1556) | 2014-09-04 | `cs.CV` | Depth-scaling of CNNs; standard backbone for years | ✅ de facto |
| Sequence to Sequence Learning with Neural Networks | [1409.3215](https://arxiv.org/abs/1409.3215) | 2014-09-10 | `cs.CL` | Encoder–decoder framing of translation | ✅ de facto |
| Adam: A Method for Stochastic Optimization | [1412.6980](https://arxiv.org/abs/1412.6980) | 2014-12-22 | `cs.LG` | The default optimiser of deep learning; now at **v9** | ✅ de facto |
| Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift | [1502.03167](https://arxiv.org/abs/1502.03167) | 2015-02-11 | `cs.LG` | Made very deep networks trainable | ✅ de facto |
| Distilling the Knowledge in a Neural Network | [1503.02531](https://arxiv.org/abs/1503.02531) | 2015-03-09 | `stat.ML` | Knowledge distillation; basis of modern model compression | ✅ de facto |
| Deep Residual Learning for Image Recognition (ResNet) | [1512.03385](https://arxiv.org/abs/1512.03385) | 2015-12-10 | `cs.CV` | Residual connections; author comment reads **"Tech report"** | ✅ de facto |
| Concrete Problems in AI Safety | [1606.06565](https://arxiv.org/abs/1606.06565) | 2016-06-21 | `cs.AI` | Framed the empirical AI-safety agenda | ✅ de facto |
| Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer | [1701.06538](https://arxiv.org/abs/1701.06538) | 2017-01-23 | `cs.LG` | Sparse MoE — the basis of today's frontier-model scaling | ✅ de facto |
| **Attention Is All You Need** | [1706.03762](https://arxiv.org/abs/1706.03762) | 2017-06-12 | `cs.CL` | The Transformer. Now at **v7**, last updated 2023-08-02 | ✅ de facto |
| Proximal Policy Optimization Algorithms (PPO) | [1707.06347](https://arxiv.org/abs/1707.06347) | 2017-07-20 | `cs.LG` | Default policy-gradient method; underpins RLHF | ✅ de facto |
| UMAP: Uniform Manifold Approximation and Projection | [1802.03426](https://arxiv.org/abs/1802.03426) | 2018-02-09 | `stat.ML` | Standard high-dimensional embedding/visualisation tool | ✅ de facto |
| Loss Surfaces, Mode Connectivity, and Fast Ensembling of DNNs | [1802.10026](https://arxiv.org/abs/1802.10026) | 2018-02-27 | `stat.ML` | Mode connectivity of loss landscapes | ✅ de facto |
| BERT: Pre-training of Deep Bidirectional Transformers | [1810.04805](https://arxiv.org/abs/1810.04805) | 2018-10-11 | `cs.CL` | Made pretrain-then-finetune the NLP default | ✅ de facto |
| Massively Multilingual Neural Machine Translation in the Wild | [1907.05019](https://arxiv.org/abs/1907.05019) | 2019-07-11 | `cs.CL` | Scaling limits of multilingual translation | ✅ de facto |
| Scaling Laws for Neural Language Models | [2001.08361](https://arxiv.org/abs/2001.08361) | 2020-01-23 | `cs.LG` | Power-law scaling; made compute budgeting predictive | ✅ de facto |
| Language Models are Few-Shot Learners (GPT-3) | [2005.14165](https://arxiv.org/abs/2005.14165) | 2020-05-28 | `cs.CL` | In-context learning at 175B parameters | ✅ de facto |
| An Image is Worth 16x16 Words (ViT) | [2010.11929](https://arxiv.org/abs/2010.11929) | 2020-10-22 | `cs.CV` | Transformers displace CNNs in vision | ✅ de facto |
| Learning Transferable Visual Models From Natural Language Supervision (CLIP) | [2103.00020](https://arxiv.org/abs/2103.00020) | 2021-02-26 | `cs.CV` | Contrastive image–text pretraining; basis of multimodal models | ✅ de facto |
| On the Opportunities and Risks of Foundation Models | [2108.07258](https://arxiv.org/abs/2108.07258) | 2021-08-16 | `cs.LG` | Named and framed the "foundation model" category | ✅ de facto |
| High-Resolution Image Synthesis with Latent Diffusion Models | [2112.10752](https://arxiv.org/abs/2112.10752) | 2021-12-20 | `cs.CV` | Latent diffusion — the Stable Diffusion architecture | ✅ de facto |
| Training Compute-Optimal Large Language Models (Chinchilla) | [2203.15556](https://arxiv.org/abs/2203.15556) | 2022-03-29 | `cs.CL` | Corrected the scaling laws; reset industry training budgets | ✅ de facto |
| LLaMA: Open and Efficient Foundation Language Models | [2302.13971](https://arxiv.org/abs/2302.13971) | 2023-02-27 | `cs.CL` | Opened the open-weights ecosystem | ✅ de facto |
| Mamba: Linear-Time Sequence Modeling with Selective State Spaces | [2312.00752](https://arxiv.org/abs/2312.00752) | 2023-12-01 | `cs.LG` | Selective SSMs as a Transformer alternative | ✅ de facto |
| KAN: Kolmogorov-Arnold Networks | [2404.19756](https://arxiv.org/abs/2404.19756) | 2024-04-30 | `cs.LG` | Learnable-activation alternative to MLPs; now at v5 | ✅ de facto |
| DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via RL | [2501.12948](https://arxiv.org/abs/2501.12948) | 2025-01-22 | `cs.CL` | RL-trained reasoning; `journal_ref` = *Nature* 645:633–638 (2025) | **✅ proven** |

### 7.2 ML systems, training and inference infrastructure

This is the subgroup most relevant to a hardware/systems knowledge base — and it lives on
arXiv almost exclusively.

| Paper | arXiv ID | v1 date | Primary | Why it matters | arXiv first? |
|---|---|---|---|---|---|
| Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding | [1510.00149](https://arxiv.org/abs/1510.00149) | 2015-10-01 | `cs.CV` | Model compression pipeline that drove accelerator design | ✅ de facto |
| TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems | [1603.04467](https://arxiv.org/abs/1603.04467) | 2016-03-14 | `cs.DC` | The TensorFlow whitepaper — never a venue paper | ✅ de facto |
| Ray: A Distributed Framework for Emerging AI Applications | [1712.05889](https://arxiv.org/abs/1712.05889) | 2017-12-16 | `cs.DC` | Task+actor model for distributed ML | ✅ de facto |
| Horovod: fast and easy distributed deep learning in TensorFlow | [1802.05799](https://arxiv.org/abs/1802.05799) | 2018-02-15 | `cs.LG` | Ring-allreduce data-parallel training | ✅ de facto |
| Megatron-LM: Training Multi-Billion Parameter Models Using Model Parallelism | [1909.08053](https://arxiv.org/abs/1909.08053) | 2019-09-17 | `cs.CL` | Tensor/model parallelism for LLM training | ✅ de facto |
| ZeRO: Memory Optimizations Toward Training Trillion Parameter Models | [1910.02054](https://arxiv.org/abs/1910.02054) | 2019-10-04 | `cs.LG` | Sharded optimiser/gradient/parameter state; DeepSpeed's core | ✅ de facto |
| Fast Transformer Decoding: One Write-Head is All You Need (MQA) | [1911.02150](https://arxiv.org/abs/1911.02150) | 2019-11-06 | `cs.NE` | Multi-query attention — the KV-cache bandwidth fix | ✅ de facto |
| PyTorch: An Imperative Style, High-Performance DL Library | [1912.01703](https://arxiv.org/abs/1912.01703) | 2019-12-03 | `cs.LG` | The PyTorch reference paper | ✅ de facto |
| Reformer: The Efficient Transformer | [2001.04451](https://arxiv.org/abs/2001.04451) | 2020-01-13 | `cs.LG` | LSH attention + reversible layers for long context | ✅ de facto |
| Automatic Cross-Replica Sharding of Weight Update in Data-Parallel Training | [2004.13336](https://arxiv.org/abs/2004.13336) | 2020-04-28 | `cs.DC` | Weight-update sharding (ZeRO-1-style) on TPU pods | ✅ de facto |
| LoRA: Low-Rank Adaptation of Large Language Models | [2106.09685](https://arxiv.org/abs/2106.09685) | 2021-06-17 | `cs.CL` | Made fine-tuning cheap; now ubiquitous | ✅ de facto |
| Evaluating Large Language Models Trained on Code (Codex / HumanEval) | [2107.03374](https://arxiv.org/abs/2107.03374) | 2021-07-07 | `cs.LG` | Code LLMs and the HumanEval benchmark | ✅ de facto |
| FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness | [2205.14135](https://arxiv.org/abs/2205.14135) | 2022-05-27 | `cs.LG` | IO-aware attention kernel; a hardware-architecture result | ✅ de facto |
| GPTQ: Accurate Post-Training Quantization for GPT | [2210.17323](https://arxiv.org/abs/2210.17323) | 2022-10-31 | `cs.LG` | Practical 3–4 bit post-training quantisation | ✅ de facto |
| FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning | [2307.08691](https://arxiv.org/abs/2307.08691) | 2023-07-17 | `cs.LG` | Better parallelism and work partitioning | ✅ de facto |
| Efficient Memory Management for LLM Serving with PagedAttention (vLLM) | [2309.06180](https://arxiv.org/abs/2309.06180) | 2023-09-12 | `cs.LG` | Virtual-memory paging applied to the KV cache | ✅ de facto |
| SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | [2310.06770](https://arxiv.org/abs/2310.06770) | 2023-10-10 | `cs.CL` | The dominant agentic software-engineering benchmark | ✅ de facto |

### 7.3 Distributed systems and consensus

| Paper | arXiv ID | v1 date | Primary | Why it matters | arXiv first? |
|---|---|---|---|---|---|
| Majority is not Enough: Bitcoin Mining is Vulnerable (selfish mining) | [1311.0243](https://arxiv.org/abs/1311.0243) | 2013-11-01 | `cs.CR` | Showed <50% attacks on Bitcoin; now at v5 | ✅ de facto |
| Lightweight Asynchronous Snapshots for Distributed Dataflows | [1506.08603](https://arxiv.org/abs/1506.08603) | 2015-06-29 | `cs.DC` | Apache Flink's checkpointing algorithm | ✅ de facto |
| Algorand | [1607.01341](https://arxiv.org/abs/1607.01341) | 2016-07-05 | `cs.CR` | Byzantine agreement via verifiable random functions; at **v9** | ✅ de facto |
| Casper the Friendly Finality Gadget | [1710.09437](https://arxiv.org/abs/1710.09437) | 2017-10-25 | `cs.CR` | PoS finality overlay; the basis of Ethereum's transition | ✅ de facto |
| HotStuff: BFT Consensus in the Lens of Blockchain | [1803.05069](https://arxiv.org/abs/1803.05069) | 2018-03-13 | `cs.DC` | Linear-communication, pipelined BFT; basis of DiemBFT | ✅ de facto |
| Conflict-free Replicated Data Types (CRDTs) — encyclopedia entry | [1805.06358](https://arxiv.org/abs/1805.06358) | 2018-05-16 | `cs.DC` | Shapiro/Preguiça reference entry; `doi` 10.1007/978-3-319-63962-8_185 | ≈ same-year |
| Conflict-free Replicated Data Types: An Overview | [1806.10254](https://arxiv.org/abs/1806.10254) | 2018-06-27 | `cs.DC` | Widely used CRDT tutorial/overview | ✅ de facto |
| The latest gossip on BFT consensus (Tendermint) | [1807.04938](https://arxiv.org/abs/1807.04938) | 2018-07-13 | `cs.DC` | The Tendermint consensus specification | ✅ de facto |
| Study of Firecracker MicroVM | [2005.12821](https://arxiv.org/abs/2005.12821) | 2020-05-26 | `cs.OS` | One of only 1,455 papers in all of `cs.OS`; microVM isolation | ✅ de facto |

> **Important caveat on CRDTs.** The two CRDT entries above are a 2018 encyclopedia entry
> and a 2018 overview. The **original** CRDT work (Shapiro, Preguiça, Baquero, Zawirski,
> 2011 — INRIA technical report and SSS 2011) is **not** on arXiv. A title search for
> "Conflict-free Replicated Data Types" returns 11 hits, none of them the 2011 original
> (S1). **[API]** Cite the INRIA report for priority, not `1805.06358`.

### 7.4 Databases and data management

`cs.DB` is small (12,304 papers, rank 23 of 40 — §3.6) and most canonical database systems
work is *not* here (§7.8). What is here is mostly the learned-systems line of work.

| Paper | arXiv ID | v1 date | Primary | Why it matters | arXiv first? |
|---|---|---|---|---|---|
| The Missing Piece in Complex Analytics: Low Latency, Scalable Model Management | [1409.3809](https://arxiv.org/abs/1409.3809) | 2014-09-12 | `cs.DB` | Early framing of model management as a DB problem (CIDR line) | ✅ de facto |
| **The Case for Learned Index Structures** | [1712.01208](https://arxiv.org/abs/1712.01208) | 2017-12-04 | `cs.DB` | Launched the learned-index/learned-systems research programme | ✅ de facto |
| LSM-based Storage Techniques: A Survey | [1812.07527](https://arxiv.org/abs/1812.07527) | 2018-12-18 | `cs.DB` | The reference survey for LSM engines; `journal_ref` = VLDB Journal **2019** | **✅ proven** |
| Neo: A Learned Query Optimizer | [1904.03711](https://arxiv.org/abs/1904.03711) | 2019-04-07 | `cs.DB` | Learned query optimisation; `doi` 10.14778/3342263.3342644 (PVLDB 2019) | **✅ proven** |

### 7.5 Computer architecture, hardware and accelerators

| Paper | arXiv ID | v1 date | Primary | Why it matters | arXiv first? |
|---|---|---|---|---|---|
| EIE: Efficient Inference Engine on Compressed Deep Neural Network | [1602.01528](https://arxiv.org/abs/1602.01528) | 2016-02-04 | `cs.CV` | Sparse-weight inference accelerator; ISCA-line work | ✅ de facto |
| Efficient Processing of Deep Neural Networks: A Tutorial and Survey | [1703.09039](https://arxiv.org/abs/1703.09039) | 2017-03-27 | `cs.CV` | The standard tutorial on DNN accelerator design (Sze et al.) | ✅ de facto |
| **In-Datacenter Performance Analysis of a Tensor Processing Unit** | [1704.04760](https://arxiv.org/abs/1704.04760) | 2017-04-16 | `cs.AR` | Google's TPUv1 — the defining industrial DSA measurement paper | ✅ de facto |
| Eyeriss v2: A Flexible Accelerator for Emerging DNNs on Mobile Devices | [1807.07928](https://arxiv.org/abs/1807.07928) | 2018-07-10 | `cs.DC` | Flexible NoC dataflow accelerator for sparse/compact DNNs | ✅ de facto |
| **The gem5 Simulator: Version 20.0+** | [2007.03152](https://arxiv.org/abs/2007.03152) | 2020-07-07 | `cs.AR` | The citable reference for the standard architecture simulator | ✅ de facto |

**On RISC-V, chiplets, HLS and EDA.** These topics are *present* but as a long tail of
ordinary papers, not landmarks. Counts from title searches on 2026-09-01 (S1) **[API]**:
`ti:"RISC-V" AND cat:cs.AR` → **250**; `ti:"chiplet"` → **111**; `ti:"High-Level
Synthesis" AND cat:cs.AR` → **81**; `ti:"gem5"` → **16**; `ti:"MLIR"` → **58**. The
foundational RISC-V documents are **UC Berkeley EECS technical reports and RISC-V
International specifications, not arXiv preprints**, and I found no arXiv-hosted canonical
RISC-V ISA paper. **[API / NOT-VERIFIED for any canonical RISC-V arXiv landmark]**

### 7.6 Security, cryptography and hardware security

| Paper | arXiv ID | v1 date | Primary | Why it matters | arXiv first? |
|---|---|---|---|---|---|
| **Spectre Attacks: Exploiting Speculative Execution** | [1801.01203](https://arxiv.org/abs/1801.01203) | 2018-01-03 | `cs.CR` | Speculative-execution side channels; broke the CPU security model | ✅ de facto |
| **Meltdown** | [1801.01207](https://arxiv.org/abs/1801.01207) | 2018-01-03 | `cs.CR` | Out-of-order execution reads kernel memory; forced KPTI worldwide | ✅ de facto |
| RowHammer: A Retrospective | [1904.09724](https://arxiv.org/abs/1904.09724) | 2019-04-22 | `cs.CR` | Mutlu & Kim's synthesis of DRAM disturbance research | ✅ de facto |
| Retrospective: Flipping Bits in Memory Without Accessing Them | [2306.16093](https://arxiv.org/abs/2306.16093) | 2023-06-28 | `cs.CR` | Retrospective on the 2014 RowHammer paper (original not on arXiv) | ✅ de facto |

Spectre and Meltdown are worth dwelling on: **both were posted on the same day,
2018-01-03**, which was the coordinated disclosure date. arXiv functioned as the
disclosure channel for an industry-wide embargoed vulnerability — a role no journal could
have played on that timescale.

### 7.7 Programming languages, compilers and networking

| Paper | arXiv ID | v1 date | Primary | Why it matters | arXiv first? |
|---|---|---|---|---|---|
| **MLIR: A Compiler Infrastructure for the End of Moore's Law** | [2002.11054](https://arxiv.org/abs/2002.11054) | 2020-02-25 | `cs.PL` | Multi-level IR; now the substrate for ML compilers and much EDA tooling | ✅ de facto |
| **Programming Protocol-Independent Packet Processors (P4)** | [1312.1719](https://arxiv.org/abs/1312.1719) | 2013-12-05 | `cs.NI` | Defined programmable data planes; the P4 language | ✅ de facto |
| Channel polarization: A method for constructing capacity-achieving codes | [0807.3917](https://arxiv.org/abs/0807.3917) | 2008-07-24 | `cs.IT` | Arıkan's polar codes — adopted for 5G NR control channels; at v5 | ✅ de facto |
| What Will 5G Be? | [1405.2957](https://arxiv.org/abs/1405.2957) | 2014-05-12 | `cs.IT` | The agenda-setting 5G survey; `journal_ref` = IEEE JSAC | ≈ same-year |

### 7.8 Quantum computing and quantum hardware

`quant-ph` is arXiv's 7th-largest archive (185,584 papers, §3.5) and unlike `cs.OS` or
`cs.DB`, the field's **canonical** results really are here.

| Paper | arXiv ID | v1 date | Primary | Why it matters | arXiv first? |
|---|---|---|---|---|---|
| Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms (Shor) | [quant-ph/9508027](https://arxiv.org/abs/quant-ph/9508027) | 1995-08-30 | `quant-ph` | Shor's algorithm; `journal_ref` SIAM **1997**, doi 10.1137/S0097539795293172 | **✅ proven** |
| A fast quantum mechanical algorithm for database search (Grover) | [quant-ph/9605043](https://arxiv.org/abs/quant-ph/9605043) | 1996-05-29 | `quant-ph` | Grover's algorithm; quadratic search speedup | ✅ de facto |
| Charge insensitive qubit design derived from the Cooper pair box (transmon) | [cond-mat/0703002](https://arxiv.org/abs/cond-mat/0703002) | 2007-02-28 | `cond-mat.mes-hall` | **The transmon** — the qubit in essentially every superconducting QC today | ≈ same-year |
| Surface codes: Towards practical large-scale quantum computation | [1208.0928](https://arxiv.org/abs/1208.0928) | 2012-08-04 | `quant-ph` | The reference surface-code QEC architecture paper | ≈ same-year |
| Quantum Computing in the NISQ era and beyond | [1801.00862](https://arxiv.org/abs/1801.00862) | 2018-01-02 | `quant-ph` | Preskill's NISQ framing; `journal_ref` Quantum 2, 79 (2018) | ≈ same-year |
| Supplementary information for "Quantum supremacy using a programmable superconducting processor" | [1910.11333](https://arxiv.org/abs/1910.11333) | 2019-10-23 | `quant-ph` | The Sycamore supremacy supplement; `journal_ref` Nature 574:505 (2019) | ≈ same-year |

### 7.9 Verified-row count and the honest summary

| Group | Verified rows |
|---|---|
| 7.1 Machine learning — foundational | 30 |
| 7.2 ML systems and infrastructure | 17 |
| 7.3 Distributed systems and consensus | 9 |
| 7.4 Databases | 4 |
| 7.5 Architecture and accelerators | 5 |
| 7.6 Security and hardware security | 4 |
| 7.7 PL, compilers, networking, comms | 4 |
| 7.8 Quantum | 6 |
| **Total** | **79** |

All 79 identifiers were resolved against the arXiv API on 2026-09-01 and their titles
confirmed to match (S1). **[API]**

The distribution is itself the finding: **47 of 79 rows (59%) are machine learning or ML
infrastructure.** That is not an artifact of my selection — it tracks §3.6, where `cs.LG`
+ `cs.CV` + `cs.AI` + `cs.CL` account for 803,779 of the 1,424,149 category-assignments in
`cs.*`. arXiv is, in computing, overwhelmingly an ML archive with other subfields attached.

### 7.10 What is NOT on arXiv — the most useful negative result in this record

Anyone treating arXiv as *the* systems literature will silently miss most of the canon.
I ran explicit title searches against the API on 2026-09-01 (S1). **[API]**

| Canonical paper | Actual venue | arXiv title-search result |
|---|---|---|
| **MapReduce: Simplified Data Processing on Large Clusters** | OSDI 2004 | **0 hits** |
| **The Google File System** | SOSP 2003 | **0 hits** |
| **Bigtable: A Distributed Storage System for Structured Data** | OSDI 2006 | 2 hits, **neither is the paper** (a compaction paper and a Graphulo paper) |
| **Dynamo: Amazon's Highly Available Key-value Store** | SOSP 2007 | **0 hits** |
| **In Search of an Understandable Consensus Algorithm (Raft)** | USENIX ATC 2014 | **0 hits** |
| **Paxos Made Simple** | ACM SIGACT News 2001 | 1 hit, and it is *"Moderately Complex Paxos Made Simple"* (1704.00082), a different 2017 paper |
| **ZooKeeper: Wait-free coordination for internet-scale systems** | USENIX ATC 2010 | 2 hits, **neither is the paper** (a TLA+ verification paper and FaaSKeeper) |
| **Spanner: Google's Globally-Distributed Database** | OSDI 2012 | 291 hits — **all of them about graph spanners**, an unrelated combinatorics object |
| **Resilient Distributed Datasets (Spark)** | NSDI 2012 | **0 hits** |
| **RAMCloud** | SOSP/TOCS | **0 hits** |
| **Bitcoin: A Peer-to-Peer Electronic Cash System** | self-published, bitcoin.org | **0 hits** |
| **Flipping Bits in Memory Without Accessing Them (RowHammer)** | ISCA 2014 | 1 hit, and it is the **2023 retrospective** (2306.16093), not the original |
| **The Chubby lock service** | OSDI 2006 | not separately probed — **[NOT-VERIFIED]**, but no arXiv record surfaced in any adjacent query |
| **seL4: Formal verification of an OS kernel** | SOSP 2009 | 5 hits, **none is the original** — all are later derivative works |
| **CompCert (formally verified C compiler)** | POPL 2006 / CACM 2009 | 4 hits, **none is the original** — all are later derivative works |
| **BBR: Congestion-Based Congestion Control** | ACM Queue 2016 | 34 hits, **none is the original** — all are third-party evaluations |

**The `Spanner` case is the instructive one.** A naive keyword search returns 291 results
and a careless reader concludes the paper is there. It is not — every hit is about *graph
spanners*. **HTTP 200 and a non-empty result set do not mean the document exists.**

**Why this pattern exists.** The systems community (SOSP, OSDI, NSDI, ATC, ISCA, VLDB,
SIGMOD) publishes through venue proceedings and the ACM/USENIX digital libraries. USENIX
in particular makes proceedings open access at no charge, so there was never a paywall
pressure driving authors to arXiv. The ML community, which had no comparable open venue
culture and moves faster than any review cycle, went to arXiv instead. **The result is a
sharp disciplinary split that maps almost exactly onto the category-size data in §3.6:
`cs.LG` has 283,807 papers and `cs.OS` has 1,455.** **[INF]**

**Practical rule.** Use arXiv as a *primary* source for machine learning, ML systems,
consensus/blockchain protocols, information theory, and quantum computing. Use it as a
*supplementary* source for operating systems, databases, computer architecture and
networking — and always check ACM DL, USENIX, IEEE Xplore and DBLP before concluding a
systems paper does not exist.

## 8. Access, APIs and bulk retrieval

arXiv is unusually generous and unusually well documented for scripted access. All probes
below were run 2026-09-01.

### 8.1 The legacy arXiv API (Atom over HTTP)

Base URL: `https://export.arxiv.org/api/query` (S1). Returns Atom XML with an
`opensearch:totalResults` count and `<entry>` elements carrying `id`, `title`, `published`,
`updated`, `summary`, `author`, `arxiv:primary_category`, `arxiv:journal_ref`, `arxiv:doi`
and `arxiv:comment`.

Two query modes:

```
# by category, count only
https://export.arxiv.org/api/query?search_query=cat:cs.AR&max_results=1
# by identifier, batched (comma-separated)
https://export.arxiv.org/api/query?id_list=1706.03762,2312.00752&max_results=40
```

> **⚠ Gotcha found during this pass — `max_results=0` is broken.** The obvious way to ask
> for a count without payload is `max_results=0`. On 2026-09-01 this returned **HTTP 200
> with a fake result**: `totalResults` = **1**, and a single `<entry>` whose title is
> "Error" and whose summary reads *"The server encountered an internal error and was unable
> to complete your request."* The same query with `max_results=1` returned the correct
> `totalResults` = **8932** for `cs.AR`. **A naive harvester using `max_results=0` will
> silently record 1 for every category.** Use `max_results=1`. **[API]**

Reproducibility check: cat counts for `cs.AR`, `cs.OS`, `eess.SP` and `cs.ET` were
harvested twice, hours apart, and returned identical values (8932 / 1455 / 41815 / 7815),
confirming the §3.6 table is stable and not a transient. **[API]**

### 8.2 Rate limits — quoted exactly

From arXiv's Terms of Use for arXiv APIs (S19) **[DOC]**:

> "When using the legacy APIs (including OAI-PMH, RSS, and the arXiv API), **make no more
> than one request every three seconds, and limit requests to a single connection at a
> time.**"

And, importantly:

> "Please note that the following rate limits apply to **all of the machines under your
> control as a whole**. You should not attempt to overcome these limits by increasing the
> number of machines used to make requests."

Explicit prohibitions from the same document: do not "Store and serve arXiv e-prints
(PDFs, source files, or other content) from your servers, unless you have the permission of
the copyright holder"; do not "Attempt to circumvent rate limits"; do not represent your
project as arXiv-endorsed. Explicitly permitted: "Retrieve, store, transform, and share
descriptive metadata"; "Retrieve, store, and use the content of arXiv e-prints for your own
personal use, or for research purposes"; build search interfaces, notification apps,
visualisations and citation graphs. (S19)

All harvesting for this record used a 3.5 s inter-request delay and a single connection.

### 8.3 OAI-PMH

Endpoint: `https://oaipmh.arxiv.org/oai`. An `Identify` request returned (S20) **[API]**:

| Field | Value |
|---|---|
| `repositoryName` | arXiv |
| `protocolVersion` | 2.0 |
| `adminEmail` | help@arxiv.org |
| `earliestDatestamp` | **2005-09-16** |
| `deletedRecord` | **persistent** |
| `granularity` | YYYY-MM-DD |
| metadataPolicy | "Metadata harvesting permitted through OAI interface" |
| **dataPolicy** | **"Full-content harvesting not permitted (except by special arrangement)"** |
| submissionPolicy | "Author self-submission preferred, submissions screened for appropriateness." |

Two things matter here. **`earliestDatestamp` is 2005-09-16, not 1991** — the OAI-PMH
datestamp reflects arXiv's record-keeping epoch, not the corpus start. Incremental
harvesting from OAI-PMH will not walk you back to Shor 1995; use the bulk buckets or the
Kaggle dump for full history. And **`deletedRecord=persistent`** is the machine-readable
statement of the permanence rule in §4.4.

**The `arXivRaw` metadata prefix is the useful one** because it carries the licence:

```
https://oaipmh.arxiv.org/oai?verb=GetRecord&identifier=oai:arXiv.org:1706.03762&metadataPrefix=arXivRaw
```

returned HTTP 200, 4,099 bytes, with `<title>Attention Is All You Need</title>`,
`<categories>cs.CL cs.LG</categories>` and
`<license>http://arxiv.org/licenses/nonexclusive-distrib/1.0/</license>` (S20). **[API]**
This is the programmatic licence check referenced in §9.3.

### 8.4 S3 bulk source and PDF buckets

arXiv publishes the full corpus in **requester-pays** S3 buckets in `us-east-1` (N.
Virginia) — the downloader pays AWS for bandwidth, arXiv pays nothing (S21) **[DOC]**.

| Item | Value | Source |
|---|---|---|
| Bucket | `s3://arxiv` | S21 |
| PDF key pattern | `pdf/arXiv_pdf_YYMM_NNN.tar` (~500 MB chunks) | S21 |
| PDF manifest | `pdf/arXiv_pdf_manifest.xml` — includes `md5sum`, `content_md5sum`, `num_items`, `size`, `first_item`, `last_item` per chunk | S21 |
| Complete PDF set size | **~2.7 TB as of March 2023** | S21 |
| Complete set (PDF + source) | **~9.2 TB as of April 2025**, growing ~100 GB/month | S21 |
| Region | Eastern US (N. Virginia) | S21 |

The manifest carrying per-chunk MD5s is what makes this a serious archival source rather
than a scrape: you can verify integrity offline.

**Negative control on the bucket.** An unauthenticated anonymous GET against the bucket
returned `<Error><Code>AccessDenied</Code><Message>Access Denied</Message>` (S21 probe).
Requester-pays means you need credentials and must pass the requester-pays header; there is
no anonymous path. **[API]**

**Licence constraint on bulk data.** arXiv states plainly on the same page: *"Most articles
submitted to arXiv are submitted with the default arXiv license, which grants arXiv a
perpetual, non-exclusive license to distribute the article, but does not assign copyright
to arXiv, nor grant arXiv the right to grant any specific rights to others. **We are thus
unable to grant others the right to distribute arXiv articles.** If you build indexes or
tools based on the full-text, you must link back to arXiv for downloads."* (S21) You may
download 9.2 TB; you may not rehost it. See §9.

### 8.5 Other access paths — all probed live 2026-09-01

| Path | URL pattern | Probe result | Notes |
|---|---|---|---|
| Abstract page | `arxiv.org/abs/<id>` | HTTP **200**, 43,644 bytes for `1706.03762` | Canonical landing page |
| Native HTML | `arxiv.org/html/<id>v<n>` | HTTP **200**, 668,209 bytes for `2312.00752v2` | arXiv's own LaTeX→HTML, newer papers only |
| **ar5iv** | `ar5iv.labs.arxiv.org/html/<id>` | HTTP **200**, 167,302 bytes | Title confirmed *"[1706.03762] Attention Is All You Need"*. Covers older papers native HTML does not |
| **alphaXiv** | `alphaxiv.org/abs/<id>` | HTTP **200**, 367,300 bytes | Title *"Attention Is All You Need \| alphaXiv"*. Third-party discussion/annotation layer |
| **HuggingFace Papers** | `huggingface.co/papers/<id>` | HTTP **200**, 292,855 bytes | Third-party curation + model/dataset links |
| **Kaggle metadata dump** | `kaggle.com/datasets/Cornell-University/arxiv` | HTTP 200, page title *"arXiv Dataset \| Kaggle"* | JSON metadata for the whole corpus; the only "Google Cloud" reference found anywhere in the corpus refers to *this dataset's* storage |
| OAI-PMH | `oaipmh.arxiv.org/oai` | HTTP 200 | §8.3 |
| S3 | `s3://arxiv` | AccessDenied anonymous | §8.4 |

**[WEB]** / **[API]** as marked. Note that ar5iv, alphaXiv and HuggingFace Papers are
**third-party or labs services, not core arXiv infrastructure**, and none carries arXiv's
permanence guarantee.

### 8.6 Negative control — bogus identifiers

Per the house rule that HTTP 200 does not mean a document exists, I probed two deliberately
invalid identifiers alongside a real one:

| URL | HTTP | Bytes | Body |
|---|---|---|---|
| `arxiv.org/abs/1706.03762` (real) | **200** | 43,644 | Full abstract page |
| `arxiv.org/abs/9999.99999` (bogus) | **404** | 7,229 | *"Article identifier '9999.99999' not recognized"* |
| `arxiv.org/abs/2599.88888` (bogus) | **404** | 7,229 | Identical error page — byte-identical size confirms a constant template |
| **API** `?id_list=9999.99999` | **200** ⚠ | — | Valid Atom feed, `totalResults` = **0**, zero `<entry>` elements |

**[WEB]** / **[API]**

**Two distinct behaviours, and the second is the trap.** The web front end returns a proper
**404** for a bad ID. **The API returns HTTP 200** with a well-formed, entirely valid Atom
document containing no entries. Any harvester that checks only the HTTP status code will
treat a nonexistent paper as a successful retrieval. **You must check
`opensearch:totalResults` or count `<entry>` elements, not the status code.** The
byte-identical 7,229-byte 404 pages for two different bogus IDs also confirm that the web
error page is a fixed template and cannot be mistaken for a short real record.

## 9. Licensing and reuse

### 9.1 The default is restrictive, and this surprises people

arXiv is open *access*, not open *licence*. The default and most common choice is the
**arXiv.org perpetual, non-exclusive license 1.0**, which arXiv describes as giving
"limited rights to arXiv to distribute the article, and also **limits re-use of any type
from other entities or individuals**" (S22) **[DOC]**. arXiv's API Terms of Use put it
bluntly: *"The vast majority of e-prints are submitted under the arXiv.org non-exclusive
right to distribute"* and *"a very small subset of arXiv e-prints are submitted with
licenses that permit redistribution"* (S19).

So: you may read and download anything on arXiv. You generally may **not** rehost the PDFs.

### 9.2 The full licence menu

From arXiv's licence page (S22) **[DOC]**:

| Licence | Commercial use | Derivatives | Redistribution by third parties | Notes |
|---|---|---|---|---|
| **arXiv.org perpetual, non-exclusive 1.0** (default) | — | — | **No** | Grants arXiv distribution rights only; author keeps copyright |
| **CC BY 4.0** | ✅ | ✅ | ✅ with attribution | arXiv's recommended liberal option |
| **CC BY-SA 4.0** | ✅ | ✅ (share-alike) | ✅ with attribution + identical terms | |
| **CC BY-NC-SA 4.0** | ❌ | ✅ (share-alike) | ✅ non-commercial only | |
| **CC BY-NC-ND 4.0** | ❌ | ❌ (unadapted only) | ✅ non-commercial, verbatim | Common for publisher "accepted manuscripts", often with embargo |
| **CC0 1.0** (public domain) | ✅ | ✅ | ✅ no conditions | **Author gives up copyright**; "conflicts with many publishers' requirements" |

Critical operational rules from the same page:

- **"The license chosen is irrevocable and cannot be changed."**
- **"different versions of the work can have different licenses"** — so a licence check must
  be *per version*, not per paper.
- For all licences except CC0, "the original copyright holder retains ownership."
- If an author needs a licence not on the menu, they select the arXiv licence and state the
  desired licence on the first page of the article.

### 9.3 Metadata is CC0 — and that is the important carve-out

**"A Creative Commons CC0 1.0 Universal Public Domain Dedication will apply to all
metadata."** (S22) The API Terms of Use repeat this: you are "free to use descriptive
metadata about arXiv e-prints under the terms of the Creative Commons Universal (CC0 1.0)
Public Domain Declaration" (S19). Descriptive metadata is defined there as "title,
abstract, authors, identifier…".

**For a knowledge base like this one, that is the whole ballgame.** Titles, abstracts,
authors, IDs, categories, dates, `journal_ref` and `doi` — everything in the §7 tables and
the §3.6 counts — is CC0 and freely redistributable. The full-text PDFs generally are not.

### 9.4 How to check a paper's licence programmatically

Use OAI-PMH with `metadataPrefix=arXivRaw` and read the `<license>` element (§8.3):

```
https://oaipmh.arxiv.org/oai?verb=GetRecord&identifier=oai:arXiv.org:<ID>&metadataPrefix=arXivRaw
```

I sampled ten landmark papers from §7 on 2026-09-01 (S20) **[API]**:

| Paper | arXiv ID | Licence |
|---|---|---|
| Attention Is All You Need | 1706.03762 | `arxiv.org/licenses/nonexclusive-distrib/1.0/` |
| ResNet | 1512.03385 | `arxiv.org/licenses/nonexclusive-distrib/1.0/` |
| GPT-3 | 2005.14165 | `arxiv.org/licenses/nonexclusive-distrib/1.0/` |
| TPU (In-Datacenter Performance Analysis) | 1704.04760 | `arxiv.org/licenses/nonexclusive-distrib/1.0/` |
| DeepSeek-R1 | 2501.12948 | `arxiv.org/licenses/nonexclusive-distrib/1.0/` |
| LLaMA | 2302.13971 | **CC BY 4.0** |
| vLLM / PagedAttention | 2309.06180 | **CC BY 4.0** |
| Mamba | 2312.00752 | **CC BY 4.0** |
| gem5 v20.0+ | 2007.03152 | **CC BY 4.0** |
| MLIR | 2002.11054 | **CC BY 4.0** |

**6 of 10 restrictive, 4 of 10 CC BY.** There is a rough temporal trend toward CC BY in
papers from 2020 onward, but it is not reliable — DeepSeek-R1 (2025) is under the
restrictive default. **Never assume; always query.** In particular, *Attention Is All You
Need*, *ResNet* and the TPU paper — three of the most reproduced papers in computing —
cannot lawfully be rehosted from your own server. **[API]**

## 10. Caveats and controversies

**1. Volume growth in `cs.*` is straining the system, and arXiv says so.** Submissions rose
from 185,692 (2022) to 284,486 (2025), a 53% increase in three years (§3.3), with three
consecutive monthly records in 2026 (§3.4). arXiv's own language is not neutral: "arXiv has
been flooded with papers" (S16), "an unsustainable increase in the number of non-scientific
submissions" (S14). Two significant gates were tightened within twelve months as a direct
result (§4.1.1, §4.3).

**2. The October 2025 `cs.*` review-article rule is a genuine departure.** Requiring prior
peer review before a preprint may be posted inverts the purpose of a preprint server for
one content type in one archive. arXiv's framing — that surveys "are not (and have never
been) listed as part of the accepted content types" (S16) — is technically defensible but
the practical effect is new. The published comments on arXiv's own announcement include the
substantive objection that "surveys become outdated quickly. Requiring full peer review
before posting risks making them obsolete by the time they appear" (S16). **[COM]** Note
also that the rule is **archive-specific**: a survey rejected from `cs.*` may still be
acceptable in another archive, which creates an incentive to mis-file.

**3. Endorsement is a real and now higher barrier.** The January 2026 change removed
institutional email as a sufficient credential (§4.1.1). The people affected are precisely
those without institutional backing: independent researchers, industry practitioners on
corporate email, and researchers from institutions with weak arXiv presence. arXiv states
it "cannot waive endorsement requirements" (S14). A commenter on arXiv's own spinout
announcement raised exactly this: hoping "arXiv will consider improving the endorsement
system, since requiring new authors to obtain approval from previous authors" is a barrier
(S5). **[COM]**

**4. Moderation opacity — sourced criticism.** arXiv publishes criteria (§4.2) but not
outcomes. There is no published accept/decline/hold rate, no published hold-time
distribution, and **[NOT-VERIFIED]** on my attempts to find any. The process is structurally
opaque by design: moderators are anonymous to submitters, contacting them is
"inappropriate", "decisions upon appeal are final", and "no feedback will be provided with
the decision" (S11). Endorsement refusals are likewise invisible — a negative endorsement is
"recorded as a negative vote" but never disclosed (S12).

The main *published* critique I could verify is Silagadze, **"On arXiv moderation system"**,
[2307.11791](https://arxiv.org/abs/2307.11791), 2023-07-23 (S23) **[LIT]**. Its argument, in
the author's words: arXiv "gave a powerful impetus to the democratization of science,
freeing young scientists … especially from totalitarian countries, from authoritarian
oppression," but "many of arXiv's innovative features have been blurred by the introduction
of a moderation system." The author accepts that "a moderation system is essential to
maintain the quality of arXiv content" and proposes reform modelled on MathOverflow's
transparent moderation rather than abolition.

> Note the reflexivity: the most accessible published critique of arXiv moderation is itself
> an arXiv preprint that passed arXiv moderation. A title search for `arXiv` AND
> `moderation` returns exactly **1** result (S1) — the scholarly literature specifically on
> arXiv moderation is essentially a single paper. **[API]**

**5. The permanence-of-error problem.** Withdrawal is a labelling operation, not a deletion
(§4.4): "Previous versions will still be accessible, including the full text" (S17), and
OAI-PMH advertises `deletedRecord=persistent` (S20). A wrong or fabricated result posted to
arXiv is permanently retrievable. Retraction does not propagate to the S3 bulk tarballs, to
ar5iv renderings, to third-party layers like alphaXiv or HuggingFace Papers, or to any LLM
corpus already trained on it. **arXiv's error model is append-only and its retraction
mechanism is advisory.**

**6. LLM-generated content is now a first-order operational problem.** Not speculation:
arXiv cites it as the cause of the review-article rule (S16), implies it in the endorsement
change (S14), and the incoming CEO named "the rise of AI-generated preprints" as a defining
challenge (S6). arXiv's response so far is disclosure-based — authors must report
"significant use of … text-to-text generative AI" and AI "should not be listed as an
author" (S11) — which is unenforceable at 32,000 submissions/month.

**7. Mirrors are gone.** The historical arXiv mirror network **shut down after 15 September
2024** (S24) **[DOC]**. arXiv's reasoning: "arXiv has updated to a fully cloud-centric
architecture," most mirrors "have shut down on their own or stopped accepting updates," and
the Fastly CDN now provides global delivery. Practical consequence: **any `xxx.lanl.gov`-era
or national-mirror URL you find in an old citation is dead**, and there is no longer an
independent geographic replica of the corpus operated by third parties.

**8. Preservation is now handled by dark archives instead.** In February 2026 arXiv
announced agreements with **Portico** and **TIB (Leibniz Information Centre for Science and
Technology)** to hold the corpus as *dark* archives — "preserved but not available for use"
until a catastrophic-failure scenario (S25) **[DOC]**. This partially replaces what mirrors
once provided, but it is disaster recovery, not distributed availability.

**9. Governance is in flux — treat 2026 statements as provisional.** arXiv changed legal
form on 1 July 2026, seated its first Board, and installed its first CEO on 17 August 2026
(§1, S4–S6). Two Simons Foundation figures sit on the eight-person Board (S6), alongside two
Cornell/Cornell Tech representatives. arXiv is now formally independent of Cornell while
remaining physically headquartered in a Cornell Tech building (S3) and structurally close to
both its former host and its largest funder. That is not an accusation of anything; it is a
statement that the independence is ten weeks old and its practical meaning is untested.

**10. The Google Cloud migration claim.** **[NOT-VERIFIED]** — see §1. arXiv documents a
cloud migration but names no provider in any source I retrieved.

**11. `cs` volume statistics are ML statistics.** Any claim of the form "computer science
research is growing at X%" derived from arXiv is dominated by four ML categories holding
803,779 of 1,424,149 `cs` category-assignments (§3.6, §7.9). `cs.OS` has grown to 1,455
papers in 35 years. Do not generalise from the archive to the discipline.

**12. Absence of a paper on arXiv means nothing.** §7.10 is the evidence: MapReduce, GFS,
Dynamo, Raft, Spark RDDs, ZooKeeper, Spanner, seL4, CompCert and BBR are all absent. arXiv
is a *sample* of the computing literature with a strong and non-random disciplinary bias,
not a census.

## 11. Sources

| ID | Source | URL | Retrieved | Supports |
|---|---|---|---|---|
| **S1** | arXiv legacy API (Atom), incl. `search_query`, `id_list`, `opensearch:totalResults` | `https://export.arxiv.org/api/query` | 2026-09-01 | §3.5–3.7 counts; all 79 landmark verifications (§7); §7.10 negative title searches; §8.1 gotcha; §10 note 4 |
| **S2** | arXiv category taxonomy | https://arxiv.org/category_taxonomy | 2026-09-01 | §2 full `cs.*`/`eess.*` enumeration, names, descriptions, alias notes |
| **S3** | Cornell Chronicle, "Digital research repository arXiv to start new chapter as nonprofit" | https://news.cornell.edu/stories/2026/06/digital-research-repository-arxiv-start-new-chapter-nonprofit | 2026-09-01 | §1 LANL/Ginsparg founding Aug 1991, HEP origin, 2001 Cornell move, HQ at Tata Innovation Center, ">3.08 million" June 2026 |
| **S4** | arXiv blog, "arXiv is becoming an independent nonprofit" (2026-04-02) | https://blog.arxiv.org/2026/04/02/arxiv-is-becoming-an-independent-nonprofit/ | 2026-09-01 | §1 spinout announcement, 1 July 2026 date, Simons Foundation + Cornell roles, rationale |
| **S5** | arXiv blog, "arXiv's next chapter: Updates on our spin out from Cornell University" (2026-06-30) | https://blog.arxiv.org/2026/06/30/arxivs-next-chapter/ | 2026-09-01 | §1 spinout confirmation, "free to read and to submit to"; §10 note 3 endorsement comment |
| **S6** | arXiv blog, "arXiv welcomes inaugural CEO and Board of Directors" (2026-07-30) | https://blog.arxiv.org/2026/07/30/arxiv-welcomes-inaugural-ceo-and-board-of-directors/ | 2026-09-01 | §1 Penelope Lewis CEO eff. 2026-08-17, full Board roster; §5.4, §10 AI-preprint challenge |
| **S7** | arXiv blog, "arXiv receives $7 million in gifts and grants from Schmidt Sciences and NASA" (2025-11-24) | https://blog.arxiv.org/2025/11/24/arxiv-receives-7-million-in-gifts-and-grants-from-schmidt-sciences-and-nasa/ | 2026-09-01 | §1 funding; cloud migration begun 2023 with Simons support |
| **S8** | arXiv blog, "arXiv now hosts over 3 million articles" (2026-07-09) | https://blog.arxiv.org/2026/07/09/arxiv-now-hosts-over-3-million-articles/ | 2026-09-01 | §3.1–3.4 milestones, 230 members, 5M monthly users, record months, "many papers appear only on arXiv" |
| **S9** | arXiv category taxonomy (same page as S2, cited separately for alias statements) | https://arxiv.org/category_taxonomy | 2026-09-01 | §2.1 `cs.NA`→`math.NA`, `cs.SY`→`eess.SY` aliases |
| **S10** | arXiv monthly submission statistics (CSV export) | https://arxiv.org/stats/monthly_submissions | 2026-09-01 | §3.1–3.4 all computed totals, annual series, record months, milestone recomputation |
| **S11** | arXiv moderation policy | https://info.arxiv.org/help/moderation/ | 2026-09-01 | §4.2 decline grounds, 3/day rate limit, GenAI policy, moderator identity, appeals; §4.4 permanence and reclassification |
| **S12** | arXiv endorsement help | https://info.arxiv.org/help/endorsement.html | 2026-09-01 | §4.1 endorsement graph, domains, 3-month–5-year window, anonymity, revocability, "not peer review" |
| **S13** | arXiv endorsement domains note (within S12/S14) | https://info.arxiv.org/help/endorsement.html | 2026-09-01 | §4.1 physics-as-exception domain structure |
| **S14** | arXiv blog, "Attention Authors: updated endorsement policy" (2026-01-21) | https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/ | 2026-09-01 | §4.1.1 two-path endorsement, institutional email no longer sufficient, rationale, grandfathering |
| **S15** | arXiv blog, "Updated endorsement policy for arXiv Mathematics" (2025-12-10) | https://blog.arxiv.org/2025/12/10/updated-endorsement-policy-for-arxiv-mathematics/ | 2026-09-01 | §4.1.1 December 2025 math pilot |
| **S16** | arXiv blog, "Attention Authors: Updated Practice for Review Articles and Position Papers in arXiv CS Category" (2025-10-31) | https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/ | 2026-09-01 | §4.3 the verified `cs.*` survey/position-paper policy, all quotes; §10 notes 1–2 |
| **S17** | arXiv withdrawal help | https://info.arxiv.org/help/withdraw.html | 2026-09-01 | §4.4 withdrawal creates a new version; prior versions incl. full text remain; valid/invalid reasons |
| **S18** | arXiv version availability help | https://info.arxiv.org/help/versions.html | 2026-09-01 | §5.1 version immutability |
| **S19** | Terms of Use for arXiv APIs | https://info.arxiv.org/help/api/tou.html | 2026-09-01 | §8.2 rate limits (exact quote), permitted/prohibited uses; §9.1, §9.3 metadata CC0 and default-licence statements |
| **S20** | arXiv OAI-PMH endpoint (`Identify`, `GetRecord`/`arXivRaw`) | https://oaipmh.arxiv.org/oai | 2026-09-01 | §8.3 Identify fields, `earliestDatestamp` 2005-09-16, `deletedRecord=persistent`, data policy; §9.4 licence sampling |
| **S21** | arXiv Bulk Data Access — Amazon S3 | https://info.arxiv.org/help/bulk_data_s3.html | 2026-09-01 | §8.4 bucket layout, manifest fields, 2.7 TB / 9.2 TB sizes, requester-pays, no-redistribution statement |
| **S22** | arXiv License Information | https://info.arxiv.org/help/license/ | 2026-09-01 | §9.1–9.3 full licence menu, irrevocability, per-version licences, metadata CC0 |
| **S23** | Z. K. Silagadze, "On arXiv moderation system" | https://arxiv.org/abs/2307.11791 | 2026-09-01 | §10 note 4 sourced moderation critique (abstract retrieved via S1) |
| **S24** | arXiv blog, "Attention arXiv users: arXiv mirrors to shut down September 15th, 2024" (2024-09-13) | https://blog.arxiv.org/2024/09/13/attention-arxiv-users-arxiv-mirrors-to-shut-down-september-15th-2024/ | 2026-09-01 | §10 note 7 mirror shutdown, Fastly CDN, cloud-centric architecture |
| **S25** | arXiv blog, "arXiv future proofs access to research with third-party digital preservation" (2026-02-03) | https://blog.arxiv.org/2026/02/03/arxiv-future-proofs-access-to-research-with-third-party-digital-preservation/ | 2026-09-01 | §10 note 8 Portico and TIB dark-archive agreements |
| **S26** | *Science*, "ArXiv, the pioneering preprint server, declares independence from Cornell" | https://www.science.org/content/article/arxiv-pioneering-preprint-server-declares-independence-cornell | 2026-09-01 — **retrieval FAILED** | §1 — **[NOT-VERIFIED]**, see note below |
| **S27** | arXiv blog, "A Year in Review: arXiv's 2025 Annual Report" (2026-06-26) | https://blog.arxiv.org/2026/06/26/a-year-in-review-arxivs-2025-annual-report/ | 2026-09-01 | §1 — annual report PDF retrieved but text extraction failed; not relied upon for any figure |

### Note on S26 — the *Science* article

The URL is **confirmed to exist**: arXiv's own blog post of 2026-04-02 links to it directly
as "this article in Science, where both Paul Ginsparg, arXiv's founder, and Greg Morrisett,
dean and vice provost of Cornell Tech … discuss some of the challenges arXiv has faced as it
grows" (S4). **I could not load it.** `science.org` returned an interstitial
Cloudflare challenge page ("Just a moment… Enable JavaScript and cookies to continue") on
every attempt. Following the user-agent ladder in `AGENTS.md`, I tried: default `curl`,
Chrome 131 desktop, `WhatsApp/2.23.20.0`, and `ChatGPT-User/1.0` — **HTTP 403 on all**. The
Wayback availability API reports **no archived snapshot** for that URL. The 2026-03-18
publication date given in the assignment brief is therefore **[NOT-VERIFIED]**.

**However, the substance is fully covered by better primary sources**: the Cornell Chronicle
article (S3) carries direct quotes from both Ginsparg and Morrisett on the same subject, and
arXiv's own announcements (S4, S5, S6) document the transition authoritatively. Nothing in
§1 depends on S26.

### Method note

Category counts, landmark verifications and negative-control title searches were performed
with a 3.5-second inter-request delay against a single connection, in compliance with S19.
Working scripts and raw responses are retained in
`doc/hardware/scratch/preprint-repositories/arxiv/`.
