# Cryptology ePrint Archive — preprint repository record

- **URL:** https://eprint.iacr.org/ · short-URL alias `https://ia.cr/YYYY/NNNN` (302 → canonical, S27)
- **Operator:** International Association for Cryptologic Research (IACR), a non-profit incorporated
  in Nevada, USA (S18). Run by a small volunteer editorial board — as of 2026-09-01: Joppe W. Bos,
  Sofía Celi, Matthias J. Kannwischer (S1). **Funding:** IACR income is membership dues and
  conference registration; the Treasurer "publishes the annual Financial Report of the IACR in the
  first quarter of each calendar year" (S19) [DOC]. No ePrint-specific budget line was located
  [NOT-VERIFIED].
- **Discipline scope:** cryptology and related fields, as advertised — in practice also cache and
  microarchitectural attacks, hardware side-channel and fault injection, distributed consensus,
  blockchain, ORAM, MPC and formal protocol verification.
- **Launched:** ePrint debuted **fall 1999** (S2). Its predecessor, the Theory of Cryptography
  Library, was founded **1996** by Oded Goldreich at MIT and migrated in — which is why records
  dated 1996–1999 exist (S2, S5). · **Status:** active (1999–2026)
- **Compiled:** 2026-09-01 (retrievals 2026-09-01/02 UTC)
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

> **Correction.** IACR was *not* founded in 1996. Wikipedia states IACR "was organized at the
> initiative of David Chaum at the CRYPTO '82 conference" (S22) [COM]. 1996 is the founding year of
> the *Theory of Cryptography Library*, ePrint's ancestor (S2) [DOC]. No founding year appears
> anywhere on iacr.org itself — `iacr.org/about/`, `iacr.org/docs/` and the bylaws PDF were all
> checked [NOT-VERIFIED].

## 1. What it is

ePrint is the field-wide preprint server for cryptography. It solves a discipline-specific problem:
cryptography's results are frequently *destructive* — a break of a deployed or standards-track
scheme — and a break that waits nine months for a conference cycle leaves systems exploitable in
the interim. ePrint makes a cryptanalytic result public and timestamped within hours.

Its self-description is modest: papers "did not undergo any refereeing process other than verifying
that the work seems to be within the scope of cryptology and meets some minimal acceptance criteria
and publishing conditions" (S1) [DOC]. IACR's publications page is blunter: "Papers published there
undergo no scientific reviewing process. Some papers may be published there long before they appear
in a peer-reviewed publication venue" (S20) [DOC].

What makes ePrint unusual is its tight coupling to a society that also owns the field's venues. The
IACR bylaws (approved 2025-12-20) enumerate General Conferences (Asiacrypt, Crypto, Eurocrypt), Area
Conferences (CHES, FSE, PKC, TCC), Symposia (Real World Cryptography), and journals: *Journal of
Cryptology*, *IACR Communications in Cryptology*, and Area Journals *ToSC* and *TCHES* (S19) [DOC] —
the same eight events are listed on IACR's conferences index (S21) [WEB].
ToSC and TCHES are diamond-open-access journal/conference hybrids that *are* FSE and CHES (S20)
[DOC]. The same body owns preprint server, conferences and journals — and explicitly encourages
posting to ePrint (S3) [DOC]. That removes the preprint-versus-venue friction seen elsewhere.

## 2. Scope and subject taxonomy

Exactly **seven** author-selected categories plus an uncategorised legacy bucket. Whole-archive
totals from the `categoryData` variable on the statistics page (S4) [WEB], retrieved 2026-09-01:

| Category | Form/feed code | Papers |
|---|---|---:|
| Cryptographic protocols | `PROTOCOLS` | 6,452 |
| Public-key cryptography | `PUBLICKEY` | 5,011 |
| Foundations | `FOUNDATIONS` | 3,205 |
| Secret-key cryptography | `SECRETKEY` | 2,961 |
| **Implementation** | `IMPLEMENTATION` | **2,417** |
| Applications | `APPLICATIONS` | 2,122 |
| Attacks and cryptanalysis | `ATTACKS` | 1,363 |
| *(uncategorised)* | — | 4,021 |
| **Total** | | **27,552** |

Codes confirmed twice: as `<option>` values on the submission form (S12) [DOC] and as the
`?category=NAME` selector for per-category RSS feeds (S9) [DOC]. For this knowledge base the
load-bearing categories are **Implementation** (hardware, microcontroller, countermeasures, FPGA/ASIC)
and **Attacks and cryptanalysis**. The taxonomy is coarse by design — there is no side-channel,
fault-injection or lightweight-crypto code, so category filtering alone will not isolate embedded
work; keyword search is required.

## 3. Size and growth

**27,552 papers archive-wide as of 2026-09-01/02**, confirmed by **five independent paths that agree
exactly**: sum of `/byyear` HTML counts [WEB]; sum of the `byyear` JS array on `/stats` [WEB]; sum of
the `byday` weekday array on `/stats` [WEB]; sum of `categoryData` on `/stats` [WEB]; and
`count(<identifier>)` in the OAI-PMH `ListIdentifiers` dump [API] (S4, S5, S7).

**Method.** `/byyear` publishes an explicit per-year count. I cross-checked *all 31 years* against an
independent count derived from OAI-PMH `ListIdentifiers` (`metadataPrefix=oai_dc`; a single 3.34 MB
response, no resumption token), parsing `YYYY` out of each `oai:eprint.iacr.org:YYYY/NNNN` identifier.
**Zero mismatches.** "Max #" is the highest sequence number present that year; "Gap" is `max − count`,
i.e. numbers allocated but never publicly resolvable (§4, §8).

| Year | Papers | Max # | Gap | Year | Papers | Max # | Gap |
|---|---:|---:|---:|---|---:|---:|---:|
| 1996 | 16 | 16 | 0 | 2012 | 733 | 733 | 0 |
| 1997 | 15 | 15 | 0 | 2013 | 881 | 882 | 1 |
| 1998 | 26 | 26 | 0 | 2014 | 1,029 | 1,029 | 0 |
| 1999 | 24 | 24 | 0 | 2015 | 1,255 | 1,257 | 2 |
| 2000 | 69 | 69 | 0 | 2016 | 1,195 | 1,196 | 1 |
| 2001 | 113 | 113 | 0 | 2017 | 1,262 | 1,262 | 0 |
| 2002 | 195 | 195 | 0 | 2018 | 1,249 | 1,251 | 2 |
| 2003 | 265 | 265 | 0 | 2019 | 1,498 | 1,499 | 1 |
| 2004 | 375 | 377 | 2 | 2020 | 1,620 | 1,620 | 0 |
| 2005 | 469 | 469 | 0 | 2021 | 1,705 | 1,705 | 0 |
| 2006 | 485 | 486 | 1 | 2022 | 1,781 | 1,781 | 0 |
| 2007 | 482 | 482 | 0 | 2023 | 1,971 | 1,973 | 2 |
| 2008 | 545 | 545 | 0 | 2024 | 2,100 | 2,100 | 0 |
| 2009 | 638 | 638 | 0 | 2025 | 2,337 | 2,340 | 3 |
| 2010 | 660 | 661 | 1 | **2026** (partial) | **1,845** | 1,846 | 1 |
| 2011 | 714 | 714 | 0 | **TOTAL** | **27,552** | — | **17** |

Sources: S5, S4 [WEB]; S7 [API]. 2026 is partial — 1,845 by 2026-09-01, already above every year
before 2023; straight-lining eight months gives ≈2,770 for the full year [INF].

Every year except 2004 begins at sequence number 001; 2004 starts at 002 and its two gaps are
`2004/001` and `2004/056` (S7) [API]. Shape of the curve: ~1,500 papers in the first five years,
"more than doubled" by year ten, 10,000 passed in 2016, over 15,000 by end of year twenty (S2) [DOC]
— my cumulative sums are consistent with all three milestones [INF].

Other archive-wide statistics from `/stats` (S4) [WEB], computed by me from the raw histograms:

- **Mean authors per paper 3.09**; 20.5% single-author; most-authored paper has 32 authors
  (`authorData` sums to 27,552, so this covers the whole archive).
- **Weekday deposits:** Tue 5,016 > Mon 4,986 > Wed 4,767 > Thu 4,413 > Fri 4,348 ≫ Sun 2,167 >
  Sat 1,855. Weekends are ~15% of deposits — a professional, working-hours archive [INF].
- **Version churn:** within the 19,672 records covered by `versionData`, 47.4% have exactly one
  version and 52.6% have been revised at least once; 2,084 have ≥5 versions, 291 have ≥10, and one
  paper has **125 versions**. ⚠️ `versionData` sums to 19,672, **not** 27,552 — it covers only ~71%
  of the archive and the page does not document the subset basis. Do not quote 47.4% as
  archive-wide [NOT-VERIFIED for the full archive].

**Conflict check.** The English Wikipedia article on the Cryptology ePrint Archive publishes **no
size figure at all** (full extract via the MediaWiki API, S23) [WEB]. Recorded as an absence — there
is no Wikipedia-versus-operator conflict here, unlike arXiv.

## 4. Screening and moderation — what gets in

Not peer review, but not nothing. The gate is **editorial screening by the named editors** against
four published criteria. Verbatim (S3) [DOC], submissions must be deemed by the editors to:
(1) "address research in cryptology and related fields"; (2) "be clear, readable, and
self-contained"; (3) "look somewhat new and interesting"; (4) "contain proofs or convincing
arguments for any claims". Plus a hard formal rule: submissions "must not be anonymous and state
title, author name(s), and a contact address or affiliation(s) on the first page" (S3) [DOC].

The submission form additionally enforces machine-checkable constraints: UTF-8 (not TeX escapes or
HTML entities) for names and abstracts, abstract ≥64 characters, keyword phrases ≤40 characters, PDF
only, A4/Letter geometry, and a mandatory licence selection (S12) [DOC].

Criteria 3 and 4 are genuine editorial judgement, which makes this *more* than arXiv-style scope
screening — but the operators immediately disclaim what it means: **"If a paper is accepted, this
does not mean that the editors have verified any claims or arguments. Authors are solely responsible
for the content and the correctness of the published work."** (S3) [DOC].

Editorial turnover is public (Sofía Celi joined 2024-12-10; Matthias J. Kannwischer joined
2023-10-19 replacing Tancrède Lepoint) and `/about.html` lists every past editor since 2000 (S1, S2)
[DOC]. **No rejection rate is published** — `/about.html`, `/operations.html`, `/stats` and
`/news.html` all checked [NOT-VERIFIED].

The 17 numbering gaps in §3 are the only observable trace of records allocated a number that never
became public: 17 of 27,569 allocated numbers, **99.94% dense** [INF from API+WEB]. These are not
rejections — rejected submissions never receive a number, since numbering is assigned at acceptance
[INF].

## 5. Reliability — what you can and cannot trust

### What a deposit guarantees

(a) A **priority timestamp** to the second, publicly visible as `YYYYMMDD:HHMMSS` in the version
archive (S14) [WEB]; (b) **permanence** of the identifier; (c) **named, non-anonymous authorship with
a contact address** (S3) [DOC]; (d) that a human editor thought it was cryptology and looked
plausible. It guarantees **nothing about correctness**, and the operators say so (S3, S20) [DOC].

It does **not** give you a DOI. ePrint mints none; the `doi` field in the recommended BibTeX is for
the *externally published* version, and the citation page tells authors to "cite the original work if
it is published elsewhere" and to "use the DOI for the paper to identify it uniquely" (S13) [DOC].
Paper pages carry no ePrint DOI — verified on 2017/1066, whose metadata block lists only
"Short URL https://ia.cr/2017/1066" (S28) [WEB].

### Why cryptography treats ePrint as authoritative for priority

1. **The venue owner endorses it.** IACR's copyright policy "permits and encourages that authors
   submit their work to the Cryptology ePrint Archive"; all author versions of IACR proceedings
   papers from 2013 onward may be posted (S3) [DOC].
2. **Anonymous-submission conflicts resolve in ePrint's favour.** IACR's position, traced to a Board
   decision of **1999-05-02 in Prague**, is that posting to ePrint while under anonymous review "is
   permitted and that authors should not be penalized by conference program committees for having
   made such a posting" (S3) [DOC]. This single policy is why ePrint-first is the field default.
3. **The ePrint version is usually the *better* version.** Conference page limits push proofs into
   appendices Springer does not print, and IACR concedes ePrint "contains different versions of
   papers published elsewhere (including corrected or full versions containing details not found)"
   (S20) [DOC]. My sample bears this out — 2010/441 ("Full version of a paper published in the
   proceedings of CHES 2010"), 2012/300 ("an extended version of the paper … at CHES 2012") and
   2013/279 ("the full version of the IEEE Symposium on Security & Privacy 2013 paper") (S28) [WEB].
   **For these the ePrint report is canonical and the proceedings version is the abridgement.**

### Measured eventual-publication rate — derived here

No scientometric study of ePrint was located. I queried the Crossref API twice (`query.bibliographic`
= "Cryptology ePrint Archive scientometric analysis", and a publication-rate variant); all hits
concerned unrelated "eprint" archives (Bioline, law schools, The Lancet) (S30) [NOT-VERIFIED for
[LIT]]. So I measured it.

**Method:** systematic sample of the 2017 cohort (1,262 papers — old enough that outcomes have
settled). Every 21st sequence number from 001, n = 60, fetching each paper page and parsing the
"Publication info" field, throttled to ~3.4 s/request.

| Publication info state | n | % |
|---|---:|---:|
| `Published by` / `revision of an IACR publication` | 16 | 26.7% |
| `Published elsewhere` | 21 | 35.0% |
| `Preprint…` (no publication recorded) | 23 | 38.3% |
| **Records a subsequent publication** | **37 / 60** | **61.7%** |

95% Wilson score interval **[49.0%, 72.9%]** [INF from a [WEB] sample].

⚠️ **A lower bound, not an estimate.** The publication-info field is *self-reported* and must be
updated by the author using their retained submission password (S3) [DOC]; authors who publish and
never return are counted as "Preprint". Read it as "at least three in five 2017 ePrint reports are
known to have been published elsewhere."

### The real failure mode: unreviewed breaks and unreviewed schemes

- **Attacks appear here first, unreviewed, and are frequently correct** — but a report titled
  "Cryptanalysis of X" carries *no* editorial verification that the attack works.
- **"Provably secure" is a claim about a model, not an implementation.** Criterion 4 requires "proofs
  or convincing arguments", not correct ones. Broken proofs of broken schemes get posted, cited and
  sometimes deployed before anyone checks.
- **Post-quantum submissions are the highest-risk zone.** The NIST PQC process pushed a large volume
  of structurally unfamiliar schemes onto ePrint against a standards deadline. Several §7 landmarks
  are breaks of exactly such schemes.

### Case study: the SIKE / SIDH break (verified end to end)

| When | What | Evidence |
|---|---|---|
| **2022-07-05** | NIST announces four algorithms to be standardized plus four **Round 4** candidates; SIKE is Round 4 | S24 [WEB] |
| **2022-07-30 07:20:07 UTC** | Castryck & Decru (KU Leuven) post ePrint **2022/975**, "An efficient key recovery attack on SIDH" — v1 | S25 [WEB] |
| 2022-07-30 14:32:35 UTC | v2, the *same day* | S25 [WEB] |
| 2022-08-05 · 2023-02-22 · 2023-05-15 | v3 · v4 · v5 | S25 [WEB] |
| — | Record now reads "Published by the IACR in EUROCRYPT 2023" | S28 [WEB] |

The abstract states the attack "breaks SIKEp434, which aims at security level 1, in about ten minutes
on a single core", and names SIKE as the instantiation that "recently advanced to the fourth round of
NIST's standardization effort" (S25) [WEB]. **25 days elapsed between NIST advancing SIKE and an
unreviewed ePrint report destroying it**; formal peer-reviewed publication followed ~9 months later.
Any process that waited for peer review would have been nine months wrong.

### How to sanity-check an individual ePrint report

1. **Read "Publication info".** `Published by the IACR in <venue>` or `A minor/major revision of an
   IACR publication in <venue>` means it passed IACR peer review; `Preprint.` means it has not —
   38% of my 2017 sample (S28) [WEB].
2. **Read "History"** — `received` date plus `last of N revisions`. A 2019 report still at v1 in 2026
   is either perfect or abandoned; v14 (Bulletproofs) or v44 (PLONK) means actively maintained.
3. **Open `/archive/versions/YYYY/NNNN`.** Bulletproofs v1 (`20171110:151138`) is titled *"…Efficient
   Range Proofs for Confidential Transactions"*; the current version is *"…Short Proofs for
   Confidential Transactions and More"* (S14, S15) [WEB]. **The title changed** — citing by remembered
   title may cite a version that no longer exists.
4. **Read the `Note:` field**, where corrections live. Bulletproofs' current note: *"This version
   fixes an earlier mistake in the Fiat-Shamir section (Section 4.4) reported by TrailOfBits."*
   (S28) [WEB] — a real soundness bug in a widely deployed proof system, disclosed only in free text.
5. **Check authors and affiliations.** Non-anonymity is mandatory (S3) [DOC]; newer records carry
   per-author institutions (2022/975 shows "KU Leuven" for both) [WEB].
6. **Check whether anything on ePrint attacks it** — `title:` search the scheme name. The archive is
   its own adversarial review layer.
7. **Prefer the ePrint text for technical detail, cite the proceedings DOI for the record** — exactly
   what S13 instructs.

## 6. What you actually find there — examples

Concrete documents a systems or electronics engineer would recognise, all verified to resolve
(details and links in §7): the **reference specs of algorithms now in your TLS stack and your MCU**
(CRYSTALS-Kyber 2017/634, CRYSTALS-Dilithium 2017/633 — NIST's ML-KEM and ML-DSA); the **benchmark
suite embedded PQC is measured against** (`pqm4` 2019/844); **working microcontroller implementation
papers** (2026/235, Keccak/Kyber/Dilithium on the MSP430, TCHES 2026); **cache and microarchitectural
attacks** (Flush+Reload 2013/448, CacheBleed 2016/224); **physical key extraction from consumer
devices** (2016/230, ECDSA from phones by non-intrusive EM/power measurement); **hardware RNG
certification guidance** (2024/301, released CC0); **secure-boot engineering** (2022/1198 and
2022/602); and **withdrawn records left standing as historical evidence** (2017/1065, 2019/1410 —
§10).

## 7. Landmark papers (software · distributed systems · databases · electronics · security)

**41 entries, every one verified by fetching its ePrint page on 2026-09-01/02** and confirming title,
authors, receipt date, version count, licence and publication-info string (S28) [WEB]. "v" = total
versions. `n/a (companion)` means the record itself declares it the full/extended version of a paper
at the named venue, so it is a companion rather than a precedence claim.

### 7.1 Zero-knowledge proofs, verifiable computation, privacy

| Paper | ID | Recv | v | Publication info (as recorded) | Preprint first? |
|---|---|---|---:|---|---|
| Pinocchio: Nearly Practical Verifiable Computation | [2013/279](https://eprint.iacr.org/2013/279) | 2013-05-16 | 1 | full version of IEEE S&P 2013 | n/a (companion) |
| Path ORAM: An Extremely Simple Oblivious RAM Protocol | [2013/280](https://eprint.iacr.org/2013/280) | 2013-05-16 | 2 | Published elsewhere, CCS 2013 | yes |
| Zerocash: Decentralized Anonymous Payments from Bitcoin | [2014/349](https://eprint.iacr.org/2014/349) | 2014-05-19 | 1 | Published elsewhere, IEEE S&P 2014 | n/a (companion) |
| On the Size of Pairing-based Non-interactive Arguments (**Groth16**) | [2016/260](https://eprint.iacr.org/2016/260) | 2016-03-08 | 2 | IACR publication, EUROCRYPT 2016 | yes |
| Bulletproofs: Short Proofs for Confidential Transactions and More | [2017/1066](https://eprint.iacr.org/2017/1066) | 2017-11-10 | 14 | Published elsewhere, IEEE S&P 2018 | **yes** |
| Scalable, transparent, and post-quantum secure computational integrity (**STARK**) | [2018/046](https://eprint.iacr.org/2018/046) | 2018-01-10 | 4 | Preprint. MINOR revision. | **yes — never formally published** |
| **PLONK** | [2019/953](https://eprint.iacr.org/2019/953) | 2019-08-21 | **44** | Preprint. | **yes — never formally published** |

### 7.2 Fully homomorphic encryption

| Paper | ID | Recv | v | Publication info | Preprint first? |
|---|---|---|---:|---|---|
| Fully Homomorphic Encryption without Bootstrapping (**BGV**) | [2011/277](https://eprint.iacr.org/2011/277) | 2011-05-28 | 3 | "Published elsewhere. Unknown where it was published" | **yes** |
| Somewhat Practical Fully Homomorphic Encryption (**BFV**) | [2012/144](https://eprint.iacr.org/2012/144) | 2012-03-22 | 1 | "Published elsewhere. Unknown where it was published" | **yes** |
| Homomorphic Encryption for Arithmetic of Approximate Numbers (**CKKS**) | [2016/421](https://eprint.iacr.org/2016/421) | 2016-05-01 | 5 | IACR publication, ASIACRYPT 2017 | **yes (~18 months)** |

BGV and BFV — two of the three FHE schemes the whole homomorphic-encryption industry implements —
have publication metadata reading literally "Unknown where it was published". The ePrint report is in
practice the citable artifact [INF].

### 7.3 Post-quantum cryptography and its breaks

| Paper | ID | Recv | v | Publication info | Preprint first? |
|---|---|---|---:|---|---|
| Towards quantum-resistant cryptosystems from supersingular elliptic curve isogenies (**SIDH**) | [2011/506](https://eprint.iacr.org/2011/506) | 2011-09-18 | 2 | Published elsewhere, PQCrypto 2011 | n/a (companion) |
| SPHINCS: practical stateless hash-based signatures | [2014/795](https://eprint.iacr.org/2014/795) | 2014-10-10 | 2 | IACR publication, EUROCRYPT 2015 | **yes** |
| Post-quantum key exchange — a new hope (**NewHope**) | [2015/1092](https://eprint.iacr.org/2015/1092) | 2015-11-10 | 9 | Published elsewhere, USENIX Security 2016 | **yes** |
| CRYSTALS — Dilithium: Digital Signatures from Module Lattices (**→ ML-DSA**) | [2017/633](https://eprint.iacr.org/2017/633) | 2017-06-27 | 2 | IACR publication, **TCHES 2018** | **yes** |
| CRYSTALS — Kyber: a CCA-secure module-lattice-based KEM (**→ ML-KEM**) | [2017/634](https://eprint.iacr.org/2017/634) | 2017-06-27 | 2 | Published elsewhere, EuroS&P 2018 | **yes** |
| **An efficient key recovery attack on SIDH** (Castryck–Decru; killed SIKE) | [2022/975](https://eprint.iacr.org/2022/975) | 2022-07-30 | 4 | Published by the IACR in EUROCRYPT 2023 | **yes — ~9 months** |

### 7.4 Distributed systems, consensus, blockchain

| Paper | ID | Recv | v | Publication info | Preprint first? |
|---|---|---|---:|---|---|
| The Bitcoin Backbone Protocol: Analysis and Applications | [2014/765](https://eprint.iacr.org/2014/765) | 2014-09-30 | **17** | IACR publication, EUROCRYPT 2015 | **yes** |
| Ouroboros: A Provably Secure Proof-of-Stake Blockchain Protocol | [2016/889](https://eprint.iacr.org/2016/889) | 2016-09-14 | 8 | IACR publication, CRYPTO 2017 | **yes (~10 months)** |
| ALGORAND AGREEMENT: Super Fast and Partition Resilient Byzantine Agreement | [2018/377](https://eprint.iacr.org/2018/377) | 2018-04-30 | 2 | Preprint. MINOR revision. | **yes — never formally published** |
| Compact Multi-Signatures for Smaller Blockchains (**BLS aggregate sigs**) | [2018/483](https://eprint.iacr.org/2018/483) | 2018-05-23 | 2 | Preprint. MINOR revision. | **yes — never formally published** |
| Sync HotStuff: Simple and Practical Synchronous State Machine Replication | [2019/270](https://eprint.iacr.org/2019/270) | 2019-03-12 | 6 | Preprint. MINOR revision. | **yes** |

### 7.5 Protocol security analysis (TLS, Signal)

| Paper | ID | Recv | v | Publication info | Preprint first? |
|---|---|---|---:|---|---|
| A Cryptographic Analysis of the TLS 1.3 Handshake Protocol **Candidates** | [2015/914](https://eprint.iacr.org/2015/914) | 2015-09-22 | 2 | Published elsewhere, ACM CCS 2015 | **yes — analysed drafts pre-RFC** |
| A Formal Security Analysis of the **Signal** Messaging Protocol | [2016/1013](https://eprint.iacr.org/2016/1013) | 2016-10-27 | 5 | Published elsewhere, IEEE EuroS&P 2017 | **yes** |
| A Cryptographic Analysis of the TLS 1.3 Handshake Protocol (journal version) | [2020/1044](https://eprint.iacr.org/2020/1044) | 2020-08-28 | 2 | IACR publication, **JoC 2021** | **yes** |

### 7.6 Hardware, embedded and side-channel

| Paper | ID | Recv | v | Publication info | Preprint first? |
|---|---|---|---:|---|---|
| Provably Secure Higher-Order Masking of AES | [2010/441](https://eprint.iacr.org/2010/441) | 2010-08-17 | 1 | full version, **CHES 2010** | n/a (companion) |
| High-speed high-security signatures (**Ed25519**) | [2011/368](https://eprint.iacr.org/2011/368) | 2011-07-10 | 2 | full version, **CHES** | n/a (companion) |
| Threshold Implementations of all 3x3 and 4x4 S-boxes | [2012/300](https://eprint.iacr.org/2012/300) | 2012-06-03 | 2 | extended version, **CHES 2012** | **yes (posted pre-CHES)** |
| Flush+Reload: a High Resolution, Low Noise, L3 Cache Side-Channel Attack | [2013/448](https://eprint.iacr.org/2013/448) | 2013-07-22 | 2 | Published elsewhere, USENIX Security 2014 | **yes (~1 year)** |
| CacheBleed: A Timing Attack on OpenSSL Constant Time RSA | [2016/224](https://eprint.iacr.org/2016/224) | 2016-03-01 | 1 | Preprint. MINOR revision. | **yes** |
| ECDSA Key Extraction from Mobile Devices via Nonintrusive Physical Side Channels | [2016/230](https://eprint.iacr.org/2016/230) | 2016-03-02 | 2 | Published elsewhere, ACM CCS 2016 | **yes** |
| Number "Not Used" Once — Practical fault attack on **pqm4** implementations of NIST candidates | [2018/211](https://eprint.iacr.org/2018/211) | 2018-02-26 | 3 | Preprint. | **yes — never formally published** |
| Differential Power Analysis of XMSS and SPHINCS | [2018/673](https://eprint.iacr.org/2018/673) | 2018-07-13 | 1 | Published elsewhere, COSADE 2018 | n/a (companion) |
| **pqm4**: Testing and Benchmarking NIST PQC on ARM Cortex-M4 | [2019/844](https://eprint.iacr.org/2019/844) | 2019-07-19 | 2 | Preprint. MINOR revision. | **yes — never formally published** |
| LadderLeak: Breaking ECDSA With Less Than One Bit Of Nonce Leakage | [2020/615](https://eprint.iacr.org/2020/615) | 2020-05-25 | 2 | Published elsewhere, ACM CCS 2020 | **yes** |
| Minerva: The curse of ECDSA nonces (smartcards / secure elements) | [2020/728](https://eprint.iacr.org/2020/728) | 2020-06-17 | 1 | IACR publication, **TCHES 2020** | **yes** |
| Ascon PRF, MAC, and Short-Input MAC (**NIST lightweight-crypto winner family**) | [2021/1574](https://eprint.iacr.org/2021/1574) | 2021-12-03 | 2 | Published elsewhere, CT-RSA 2024 | **yes — ~2.5 years** |
| Combined Fault Injection and Real-Time Side-Channel Analysis for **Android Secure-Boot Bypassing** | [2022/602](https://eprint.iacr.org/2022/602) | 2022-05-17 | 2 | Published elsewhere, CARDIS 2022 | **yes** |
| When Frodo Flips: End-to-End Key Recovery on FrodoKEM via **Rowhammer** | [2022/952](https://eprint.iacr.org/2022/952) | 2022-07-23 | 2 | Published elsewhere, ACM CCS 2022 | **yes** |
| To Be, or Not to Be Stateful: **Post-Quantum Secure Boot** using Hash-Based Signatures | [2022/1198](https://eprint.iacr.org/2022/1198) | 2022-09-11 | 2 | Published elsewhere, ASHES 2022 | **yes** |
| Recommendations for the Design and Validation of a Physical **TRNG** Integrated in a Cryptographic System | [2024/301](https://eprint.iacr.org/2024/301) | 2024-02-22 | 2 | Preprint. (licence **CC0**) | **yes — never formally published** |
| Optimized Implementations of Keccak, Kyber, and Dilithium on the **MSP430 Microcontroller** | [2026/235](https://eprint.iacr.org/2026/235) | 2026-02-12 | 2 | IACR publication, **TCHES 2026** | **yes** |

### 7.7 Special emphasis — ePrint as primary literature for embedded and hardware security

For embedded work ePrint is not a supplement to the literature; for large stretches it *is* the
literature. **Why:** CHES is an IACR Area Conference whose publication venue is **TCHES**, a
diamond-OA journal operating as a journal/conference hybrid; the same holds for FSE→ToSC, which
carries lightweight and symmetric-cipher work (S19, S20) [DOC]. Because IACR encourages ePrint
posting of author versions from 2013 onward (S3) [DOC], the CHES/TCHES and FSE/ToSC pipelines flow
through ePrint by default. `Implementation` alone holds **2,417 papers** (S4) [WEB]. CHES/TCHES-linked
landmarks above: 2010/441, 2011/368, 2012/300, 2017/633, 2020/728, 2026/235.

- **Side-channel countermeasure theory** — higher-order masking with security proofs (2010/441,
  CHES 2010) and threshold implementations for glitch-resistant hardware (2012/300, CHES 2012): the
  two foundations of essentially every masked AES core shipped since, both present as the *extended*
  versions.
- **Microarchitectural / cache attacks** — Flush+Reload (2013/448) appeared a full year before USENIX
  Security 2014; CacheBleed (2016/224) has *never* left preprint status. These are the primitives
  under the whole Spectre-adjacent literature.
- **Physical key extraction and nonce leakage in deployed parts** — 2016/230 recovers ECDSA keys from
  phones by non-intrusive physical measurement; Minerva (2020/728, TCHES 2020) and LadderLeak
  (2020/615, CCS 2020) together establish that sub-one-bit ECDSA nonce leakage is key-recovering.
  Directly relevant to smartcards, TPM-class parts and HSMs.
- **Fault injection against MCU firmware** — 2018/211 mounts practical fault attacks on the `pqm4`
  Cortex-M4 implementations of NIST PQC candidates and has never been formally published, so ePrint
  is the only citable source; 2022/602 combines fault injection with real-time side-channel analysis
  to bypass Android secure boot; 2022/952 turns Rowhammer bit flips into end-to-end FrodoKEM key
  recovery. (The *original* Rowhammer paper is not on ePrint — §10.)
- **Hardware RNG / TRNG design and certification** — 2024/301 (CC0) gives design and validation
  recommendations for a physical TRNG in a cryptographic system. ePrint also carries AIS-20/31
  compliant PLL-based TRNG designs and critiques of specific published TRNG constructions [WEB,
  title-search results retained in scratch].
- **Secure boot and lightweight crypto for constrained parts** — 2022/1198 works through the
  stateful-versus-stateless hash-based-signature tradeoff, i.e. the LMS/XMSS-versus-SPHINCS+ decision
  an MCU vendor faces now. Ascon, NIST's selected lightweight standard family, has its PRF/MAC modes
  on ePrint (2021/1574) ~2.5 years before CT-RSA 2024; masked Ascon hardware implementations are also
  present [WEB].
- **Benchmark infrastructure** — `pqm4` (2019/844) is the de facto Cortex-M4 PQC benchmark and exists
  as an ePrint preprint only.

**Consequence for this knowledge base:** for claims about side-channel resistance, fault tolerance,
TRNG entropy, secure boot or PQC performance on a microcontroller, ePrint is the first place to look
and frequently the only place. But apply §5's checklist rigorously — a large share of the most-cited
embedded results above carry `Preprint.` and have never been peer-reviewed at all.

## 8. Access, APIs and bulk retrieval

**There is no REST/JSON API.** Confirmed 404 on 2026-09-01: `/api`, `/api/`, `/api/search?q=…`,
`/2017/1066.json`, `/json/2017/1066`. `/search?q=…&format=json` returns `text/html`, not JSON
(S27) [API/WEB].

**OAI-PMH is the real machine interface**, at `https://eprint.iacr.org/oai` (S6) [API]:

| Property | Value |
|---|---|
| `repositoryName` / `repositoryIdentifier` | Cryptology ePrint Archive / `eprint.iacr.org` |
| `protocolVersion` · `adminEmail` | 2.0 · eprint-editor@iacr.org |
| `earliestDatestamp` | **1996-01-01T00:00:00Z** |
| `deletedRecord` | **`persistent`** (machine-readable form of the never-remove policy) |
| `granularity` · sample id | `YYYY-MM-DDThh:mm:ssZ` · `oai:eprint.iacr.org:2022/252` |
| Metadata formats | **`oai_dc` only** |
| Sets | **none** — `<error code="noSetHierarchy">We do not support sets yet.</error>` |
| Declared friends | `tosc.iacr.org/…/oai`, `tches.iacr.org/…/oai` |

**Bulk retrieval works and is easy.** `verb=ListIdentifiers&metadataPrefix=oai_dc` returned **all
27,552 identifiers in a single 3.34 MB response with no resumption token** (S7) [API] — the cheapest
reliable way to enumerate the archive. `GetRecord` returns Dublin Core with a separate `<dc:creator>`
per author, both original and last-modified dates as `<dc:date>`, `<dc:publisher>International
Association for Cryptologic Research (IACR)`, `<dc:type>e-print`, and a per-record `<dc:rights>`
licence URL (S7) [API].

*Minor spec deviation:* the `<request>` element in `GetRecord` responses contains
`http://arXiv.org/oai2` rather than ePrint's own base URL — a leftover template artifact. Harmless,
but it will confuse a strict harvester (S7) [API].

**HTML listing endpoints** paginate at **100 items per page** via `?offset=N`: `/complete/` (298 KB),
`/YYYY/` (note the trailing slash — `/2026` returns HTTP 308 → `/2026/`), `/days/{7,31,183,365}`,
`/curr/`, `/complete/compact` (S27, S29) [WEB].

**RSS/Atom feeds** at `/rss/` (S9) [DOC]: RSS 2.0 with authors in separate fields; a variant ordered
by publication date rather than last-modified; a non-standard RSS 2.0 joining authors into one
`<dc:creator>` (for Feedly-class readers); Atom; and Atom ordered by publication date. All accept
`?category=NAME`. `/rss/rss.xml` returned 243 KB with 100 items (S27) [API]. Operators ask that
"users should set their readers to refresh no more than once a day" (S9) [DOC]. News subscription:
`https://www.iacr.org/news/subscribe` (S1) [WEB].

**Rate limiting is real, Cloudflare-enforced, and self-documenting.** I tripped it during this
compilation: HTTP **429**, `server: cloudflare`, rendered page reading *"Rate limit exceeded — You
have exceeded the rate of **"20 per 1 minute"** on this path. Your IP address has been recorded as
<ip>. If you are an actual human instead of a crawler, then you may contact us at
eprint-abuse@iacr.org."* (S26) [WEB]. **No `Retry-After` header.** Budget ≥3.5 s between paper-page
fetches; use OAI-PMH for anything bulk.

**robots.txt is unusually restrictive and unusually candid** (S10) [DOC]. `User-agent: *` gets
`Disallow: /` — general crawling forbidden, because "Crawlers must be whitelisted and confirmed to be
following rules, which many do not." Named allowances for Googlebot, Claude-User, Claude-SearchBot
(with published IP ranges checked), bingbot and DuckDuckBot (both `Crawl-delay: 5`). AI crawlers
(GPTBot, ChatGPT-User, OAI-SearchBot, Google-Extended, ClaudeBot) get metadata/abstract paths but
**`Disallow: *.pdf`** — no full text. All agents are blocked from `/archive`, `/versions`, `/submit`,
`/search`. The file comments: *"Most AI crawlers willfully ignore the intent of the CC-BY license."*
The OAI `dataPolicy` says the same formally: "current versions of papers may be crawled, but older
versions must not be crawled" (S6) [API].

### Negative controls (2026-09-01/02)

| Probe | Result | Reads as |
|---|---|---|
| `/2017/1066` | HTTP 200, 16,690 B, text/html | real record |
| `/2017/1066.pdf` | HTTP 200, 697,807 B, `application/pdf` | real full text |
| `/2017/99999` · `/2017/9999` · `/2026/9999` | **HTTP 404**, 6,755 B (styled "Unknown paper") | nonexistent |
| `/1995/001` | **HTTP 404**, 6,755 B | pre-archive year |
| `/2017/99999.pdf` | **HTTP 404**, 309 B, `iso-8859-1` | bare server 404 — different shape |
| `/2026/023` (the real 2026 gap) | **HTTP 404**, 6,755 B "Unknown paper" | allocated-but-absent |
| `/2026/022`, `/2026/024` (neighbours) | HTTP 200 | gap is genuine, not a parse artifact |
| `oai?verb=GetRecord&…:2026/023` and `…:2017/99999` | `<error code="idDoesNotExist">` | gap + 404 confirmed via API |
| `/oai2`, `/harvest.html`, `/metadata.html`, `/api` | HTTP 404, 207 B | no such endpoints |

**Two distinct 404 shapes exist** (6,755 B styled vs 207/309 B bare); a byte-size check distinguishes
"the routing layer knows this pattern but the record is absent" from "no route". HTTP status alone
suffices here — ePrint does not serve 200 for missing records.

### Identifier scheme `YYYY/NNNN` — verified behaviour

- **Zero-padded to exactly three digits** below 1000, four above. `/2026/022` → 200; **`/2026/22` →
  404; `/2026/0022` → 404** (S27) [WEB]. Padding is mandatory in OAI identifiers too: `…:2026/22` →
  `idDoesNotExist`, `…:2026/022` → the record (S27) [API].
- **Sequential per calendar year, assigned at acceptance**, and essentially dense — 17 gaps in
  27,569 allocated numbers, 99.94% dense (§3) [INF from API+WEB].
- **Numbers are never reused.** 2017/1065 is a *withdrawn* paper sitting immediately below
  Bulletproofs at 2017/1066; the number was not recycled (S16) [WEB].
- Trailing slash redirects: `/2017/1066/` → HTTP 301 → `/2017/1066` (S27) [WEB].
- Specific versions are addressable as `/archive/YYYY/NNNN/YYYYMMDD:HHMMSS` — the operators document
  this exact form (S13) [DOC] and it resolves (S15) [WEB].

## 9. Licensing and reuse

**Authors choose from a fixed six-item menu** on the submission form (S12) [DOC]: `CC BY` · `CC BY-SA`
· `CC BY-NC` · `CC BY-NC-SA` · `CC BY-NC-ND` · `CC0`. (Note the absence of plain `CC BY-ND`.)
Submission grants IACR "a non-exclusive **and irrevocable** license to distribute the paper"; authors
certify they may grant it and acknowledge "publications cannot be completely removed once accepted"
(S3) [DOC].

**Observed in my landmark sample: 40 of 41 are CC BY; one (2024/301, the TRNG recommendations paper)
is CC0** (S28) [WEB]. I did not measure the archive-wide licence distribution — the per-record
`<dc:rights>` field in OAI would allow it, but I did not run a full `ListRecords` harvest
[NOT-VERIFIED].

**Metadata is CC0.** "Metadata on this site is offered under a Creative Commons CC0 license. Full text
in the PDFs of each paper is covered under a license that is specified with each paper, and you must
obey these licenses." (S9) [DOC]. Harvesting is permitted "subject to the licensing conditions above.
In particular this means attribution must be given to IACR and to authors" (S3) [DOC].

**⚠️ Text and data mining is explicitly reserved — and this cuts against the CC-BY surface.** ePrint
asserts a W3C TDMRep reservation two ways (S11) [API/WEB]: `<meta name="tdm-reservation" content="1">`
on every page checked (home, paper pages, advanced search), and
`https://eprint.iacr.org/.well-known/tdmrep.json` → `{"tdm-reservation": 1}` (HTTP 200). There is no
accompanying `tdm-policy` URL, so no opt-in route is advertised. Combined with `Disallow: /` in
robots.txt and the comment that "Most AI crawlers willfully ignore the intent of the CC-BY license"
(S10) [DOC], the intent is unambiguous: a CC-BY licence on individual PDFs is not blanket permission
to bulk-mine the corpus. `/ai.txt`, `/llms.txt`, `/.well-known/ai.txt` all 404 (S27) [WEB]. If you
need the corpus, use OAI-PMH for metadata and ask — the harvesting page states "We can also provide
other formats upon request" (S9) [DOC].

## 10. Caveats and controversies

**1. Nothing is ever removed — including things authors wish were.** "for papers that have been
withdrawn, the previous versions remain accessible. The aim … is to create transparency and an
accurate historical record … if removals or retrospective changes were implemented, then the archive
would not be considered a publication." Withdrawal is one-way: "Once withdrawn, a paper cannot be
restored; re-submissions of withdrawn papers will not be accepted." (S3) [DOC]. Verified (title-search
`withdrawn` returns 15 such records):

- **2017/1065** — current page shows title `--Withdrawn--`, abstract `---`, "Available format(s):
  `-- withdrawn --`", history `2018-09-22: withdrawn / 2017-11-09: received`. **`/2017/1065.pdf` →
  HTTP 404.** But `/archive/versions/2017/1065` still lists both updates and
  `/archive/2017/1065/20171109:164544` still serves the **original title and full abstract**: *"On the
  Security of a Lightweight Cloud Data Auditing Scheme"* (S16) [WEB].
- **2019/1410** — everything replaced with the literal string `Withdrawn`, but the Note preserves the
  reason: *"Based on several feedback with respect to constant time issues, we have withdrawn the
  paper."* (S17) [WEB].

⚠️ **Recorded conflict.** Policy says the archive "will keep the title and abstract of the paper"
(S3) [DOC]. In practice the *current* record's title and abstract are overwritten with placeholders;
the originals survive only in the version archive — which robots.txt forbids crawlers from indexing
(S10) [DOC]. The PDF is genuinely gone. So "nothing is removed" is true of metadata-in-the-archive and
**false of the current record and the full text**. Both statements sourced; not resolved here.

**2. The "ePrint says X is broken" problem.** A cryptanalysis report has been read by an editor for
plausibility, not correctness (§4). Because breaks are newsworthy, they propagate to press and
procurement *before* any review. SIKE (§5) shows the system working — the break was real. The failure
in the other direction (a widely reported ePrint "break" later shown wrong) is a known hazard of the
design; **I did not verify a specific instance in this pass** [NOT-VERIFIED].

**3. Duplicate and superseded versions.** The archive "actively discourages … posting different
versions of essentially the same material as multiple entries" and asks authors to revise instead
(S3) [DOC] — an admission that it happens. Over half of covered records have been revised at least
once, one 44 times (PLONK) and one 125 times (§3). **Cite a specific version timestamp** via
`/archive/YYYY/NNNN/YYYYMMDD:HHMMSS` (S13) [DOC] when the claim is version-sensitive.

**4. Titles change under a stable identifier.** 2017/1066 v1 was *"Bulletproofs: Efficient Range Proofs
for Confidential Transactions"*; it is now *"…: Short Proofs for Confidential Transactions and More"*
(S14, S15) [WEB]. The number is stable; the title is not. Title-keyed bibliographies rot silently.

**5. Corrections hide in a free-text `Note:` field.** Bulletproofs' note discloses a fix to "an earlier
mistake in the Fiat-Shamir section (Section 4.4) reported by TrailOfBits" (S28) [WEB]. There is no
structured erratum field, no machine-readable correction flag, and the note is **not exposed in the
OAI `oai_dc` record**. A harvester will not see corrections — arguably ePrint's most serious metadata
gap for automated consumers [INF].

**6. Publication metadata is author-maintained and decays.** BGV (2011/277) and BFV (2012/144) both
read "Published elsewhere. Unknown where it was published" (S28) [WEB]. My 2017 sample put 38.3% at
`Preprint.`, an unknown share of which *are* published but never updated (§5).

**7. No DOI, no versioned DOI.** Unlike arXiv or Zenodo, ePrint mints no DOI (§5). Citation managers
keyed on DOI will not resolve an ePrint-only work.

**8. No sets, one metadata format.** OAI exposes only `oai_dc` and no set hierarchy (S6, S8) [API], so
category-scoped harvesting must go via the RSS `?category=` feeds or HTML.

**9. Scope has a hard boundary.** Consensus protocols, ORAM, cache attacks and Rowhammer variants all
appear under a "cryptology" banner — but the *originating* systems papers in adjacent fields generally
do **not**. Searches on 2026-09-01 found **no ePrint record** for: the original HotStuff (Yin et al.),
the original Algorand (Chen–Micali), ROCA / "The Return of Coppersmith's Attack", the original
Rowhammer paper, Spectre/Meltdown, the PRESENT cipher paper, the Keccak/SHA-3 specification, "Short
Signatures from the Weil Pairing", Dwork et al.'s differential-privacy paper, TPM-FAIL, Logjam and
DROWN. Those live on arXiv, in ACM/IEEE/USENIX proceedings, or on project sites. **ePrint is dominant
for cryptology, not for systems security generally** [WEB, negative searches].

**10. Reader-privacy posture (a positive one).** Every page footer: "In order to protect the privacy of
readers, eprint.iacr.org does not use cookies or embedded third party content." (S1) [DOC], consistent
with the absence of third-party asset hosts in the fetched HTML [INF]. Rate-limit pages do, however,
record and display your IP (S26) [WEB].

## 11. Sources

All retrieved **2026-09-01 / 2026-09-02 UTC**. Plain `curl` with a default/`curl` User-Agent succeeded
on every eprint.iacr.org and iacr.org URL below — **no AGENTS.md User-Agent fallback was needed**; the
only failures were HTTP 429 rate limits, resolved by backing off.

- **S1** https://eprint.iacr.org/ — mission statement, current editors, news items, privacy footer.
- **S2** https://eprint.iacr.org/about.html — goals, "Behind the Name", full history (Theory of Cryptography Library 1996 MIT → UCSD 1998 → ePrint fall 1999), size milestones, complete past-editor list.
- **S3** https://eprint.iacr.org/operations.html — **the policy document**: acceptance criteria, licensing, further publication, revised/withdrawn papers, anonymous-submission position, harvesting.
- **S4** https://eprint.iacr.org/stats — JS data variables `byyear`, `byday`, `categoryData`, `authorData`, `versionData`, `counters`.
- **S5** https://eprint.iacr.org/byyear — per-year paper counts and category index.
- **S6** https://eprint.iacr.org/oai?verb=Identify — repository identity, `deletedRecord: persistent`, `earliestDatestamp`, data/metadata/submission policies, friends.
- **S7** https://eprint.iacr.org/oai?verb=ListIdentifiers&metadataPrefix=oai_dc (3.34 MB, 27,552 identifiers) and `verb=GetRecord` for individual records.
- **S8** https://eprint.iacr.org/oai?verb=ListMetadataFormats and `verb=ListSets`.
- **S9** https://eprint.iacr.org/rss/ — harvesting page: feed inventory, per-category feeds, CC0 metadata statement, refresh guidance.
- **S10** https://eprint.iacr.org/robots.txt — crawler whitelist, AI-bot PDF ban, `Disallow: /` default.
- **S11** https://eprint.iacr.org/.well-known/tdmrep.json and the `tdm-reservation` meta tag.
- **S12** https://eprint.iacr.org/submit — category values, field constraints, six-licence menu, confirmation text.
- **S13** https://eprint.iacr.org/citation.html — recommended BibTeX, version-specific URL form, DOI guidance.
- **S14** https://eprint.iacr.org/archive/versions/2017/1066 — 15-entry version history with `YYYYMMDD:HHMMSS` timestamps.
- **S15** https://eprint.iacr.org/archive/2017/1066/20171110:151138 — Bulletproofs v1, showing the original title.
- **S16** https://eprint.iacr.org/2017/1065 + /archive/versions/2017/1065 + /archive/2017/1065/20171109:164544 — withdrawal semantics.
- **S17** https://eprint.iacr.org/2019/1410 — second withdrawal example, reason preserved.
- **S18** https://iacr.org/docs/ — Nevada non-profit, bylaws, articles of incorporation, committee policies, copyright policy.
- **S19** https://iacr.org/docs/bylaws.pdf — bylaws approved 2025-12-20: purposes, conference/journal taxonomy, officers, Treasurer's financial-report duty.
- **S20** https://iacr.org/publications/ — IACR publication inventory; ToSC/TCHES diamond OA; ePrint's role and "no scientific reviewing process".
- **S21** https://iacr.org/conferences/ — Asiacrypt, Crypto, Eurocrypt, CHES, FSE, PKC, TCC, RWC.
- **S22** https://en.wikipedia.org/api/rest_v1/page/summary/International_Association_for_Cryptologic_Research — IACR organised at David Chaum's initiative at CRYPTO '82.
- **S23** https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles=Cryptology%20ePrint%20Archive — full extract; contains no size figures.
- **S24** https://csrc.nist.gov/News/2022/pqc-candidates-to-be-standardized-and-round-4 — dated **July 05, 2022**. (Fetched with the Chrome UA from AGENTS.md step 2; default curl was not tried first on this host.)
- **S25** https://eprint.iacr.org/2022/975 + /archive/versions/2022/975 — SIKE break abstract and five version timestamps from 20220730:072007.
- **S26** HTTP 429 from https://eprint.iacr.org/2016/889 — Cloudflare rate-limit page stating `"20 per 1 minute"` on this path; no `Retry-After`.
- **S27** Probe set (negative controls, identifier padding, endpoint discovery, `ia.cr` redirect, RSS/`/complete/` pagination) — curl transcripts in `doc/hardware/scratch/preprint-repositories/cryptology-eprint/`.
- **S28** The 41 landmark pages `https://eprint.iacr.org/<ID>` in §7, each fetched and parsed for title, authors, receipt date, version count, licence and publication info. Machine-readable: `scratch/preprint-repositories/cryptology-eprint/all_landmarks.json`.
- **S29** https://eprint.iacr.org/2026/?offset=N (19-page full sweep) — 2026 contains 1,845 records, max number 1846, exactly one gap at `2026/023`.
- **S30** https://api.crossref.org/works?query.bibliographic=… (two queries) — no scientometric literature on ePrint located; basis for the [NOT-VERIFIED] [LIT] entry in §5.
