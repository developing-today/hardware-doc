# Preprint repositories — a source-traceable survey

A record of every repository listed on Wikipedia's [List of preprint repositories][wp], written for
engineers rather than for librarians. The question this pass answers is not "what preprint servers
exist" but:

> **If I find a paper on this server, how much should I believe it, and will the link still work in
> five years?**

- **Compiled:** 2026-09-01 / 2026-09-02. Every figure below was measured on those dates.
- **Scope:** the 65 entries on the Wikipedia list, plus a handful of successors and spin-offs
  discovered while probing (openRxiv, Open Research Africa, VeriXiv, Law Archive, Open Research
  Europe).
- **Bias, stated up front:** this knowledge base is about **hardware, firmware, software and
  systems**. Repositories that carry such work are documented in depth and individually.
  Repositories that carry none are grouped and documented compactly. That is a deliberate
  allocation of effort, not a judgement of their scholarly worth.

[wp]: https://en.wikipedia.org/wiki/List_of_preprint_repositories

---

## Evidence and method

Every record in this directory uses the same labels. They are load-bearing — a claim without one
has not been checked.

| Label | Means |
|---|---|
| **[API]** | A machine-readable API response actually retrieved on the stated date. Strongest evidence here. |
| **[WEB]** | A live web page actually loaded. |
| **[DOC]** | The operator's own published policy, About or FAQ document. |
| **[LIT]** | Scholarly literature *about* the repository. |
| **[COM]** | Press, blog or community report. |
| **[INF]** | Our inference from the above, marked as inference. |
| **[NOT-VERIFIED]** | Could not confirm. The record says what was tried and why it failed. |

Five rules were applied throughout, and they are why this survey disagrees with its own source
material in a dozen places:

1. **An unsourced number is worse than no number.** Where a count could not be obtained, the record
   says `not verified` and describes the attempt. No figure in this directory was written from
   memory.
2. **Prefer machine-readable primary evidence.** Counts come from the operator's own API
   (`api.osf.io`, `api.crossref.org`, `api.biorxiv.org`, `api.archives-ouvertes.fr`,
   `export.arxiv.org`, `zenodo.org/api`, OAI-PMH) rather than from prose. Several findings below
   exist *only* because an API was harvested instead of a page being read.
3. **HTTP 200 does not mean the document exists.** Every probe was paired with a **negative
   control** — a deliberately bogus path. This caught real traps; see [§ Probing traps](#6-probing-traps).
4. **Record conflicts rather than resolving them by preference.** Where Wikipedia, the operator and
   the API disagree, all three are reported with dates. Six such conflicts are listed in
   [§ Where this survey contradicts its source](#5-where-this-survey-contradicts-its-source).
5. **Landmark papers must resolve.** Every identifier in
   [`landmark-papers.md`](landmark-papers.md) was individually fetched and its title machine-checked
   against the response. Papers that could not be confirmed were dropped, not softened.

**Verification.** This corpus was re-probed on **2026-09-11**; five findings required correction
and one dating error was found. See **[`VERIFICATION.md`](VERIFICATION.md)**.

Cross-cutting companion documents:

- **[`landmark-papers.md`](landmark-papers.md)** — the verified papers in software, distributed
  systems, databases, electronics and security, and which server they landed on.
- **[`reliability-and-durability.md`](reliability-and-durability.md)** — how much to trust each
  server, and how long its links last.
- **[`VERIFICATION.md`](VERIFICATION.md)** — the 2026-09-11 re-probe: what drifted, what was corrected.
- **[`retrieval-notes.md`](retrieval-notes.md)** — bot-blocking, user-agent and API findings from
  this pass, staged for merging into the repository's
  [crawler access table](../../ai-crawler-site-access-table.md).

---

## Start here

| If you want to… | Read |
|---|---|
| **Get the PDF of any paper, legally** | **[`open-access-full-text-sources.md`](open-access-full-text-sources.md)** — the ordered lookup ladder |
| Find MapReduce, GFS, Raft, Spark, ZooKeeper | **USENIX and the ACM DL** — they are on no preprint server ([why](landmark-papers.md#1-the-single-most-important-finding)) |
| Find the RISC-V specifications | [Berkeley EECS technical reports](government-and-institutional-technical-reports.md) — **not** arXiv, and **currently only via Wayback** |
| **Get the long version of a paper — schematics, bring-up, negative results** | **[`theses-and-dissertations.md`](theses-and-dissertations.md)** |
| Find a UK doctoral thesis | [EThOS is metadata-only since the 2023 cyberattack](theses-and-dissertations.md) — go to the university repository |
| Read the *reviews* of an ICLR/NeurIPS paper | [OpenReview](additional-preprint-servers.md) |
| Find complexity-theory results | [ECCC](additional-preprint-servers.md) — absent from Wikipedia's list |
| Find the preprint of a paywalled IEEE paper | [TechRxiv § the Crossref route](techrxiv.md) |
| Understand what an arXiv ID actually guarantees | [arXiv §5](arxiv.md) |
| Find embedded/side-channel security work before it hits a conference | [Cryptology ePrint §7.6](cryptology-eprint-archive.md) |
| Make your own code or firmware citable | [Zenodo § GitHub integration](zenodo.md) |
| Find the CRDT papers, CompCert, or Coq's original manuals | [HAL §7](hal.md) |
| Recover a dead vendor doc portal or datasheet host | [`recovering-dead-technical-sites.md`](recovering-dead-technical-sites.md) |
| Find spacecraft, radiation-hardening or national-lab electronics work | [NTRS and OSTI](government-and-institutional-technical-reports.md) |
| Know whether a small server's links will survive | [`closed-and-defunct-servers.md`](closed-and-defunct-servers.md) |
| Judge a paper from a server you have never heard of | [`reliability-and-durability.md`](reliability-and-durability.md) |
| Understand why a host is 403-ing you | [`retrieval-notes.md`](retrieval-notes.md) |
| Find battery, MEMS or semiconductor-process work | [ECSarXiv](ecsarxiv.md) · [ChemRxiv](chemrxiv.md) |

---

## 1. The technically relevant servers

These carry electronics, hardware, software, distributed-systems or database work. Each has its own
record.

| Server | Operator | Since | Measured size | Technical relevance |
|---|---|---|---|---|
| **[arXiv](arxiv.md)** | independent non-profit (ex-Cornell) | 1991 | **3,152,666** submissions; `cs` alone **931,100** [API] | **The** venue for CS/EE. 40 `cs.*` + 4 `eess.*` categories |
| **[Cryptology ePrint](cryptology-eprint-archive.md)** | IACR | 1999 | **27,552** reports [API] | Dominant for crypto; **primary** for side-channel and embedded security |
| **[HAL](hal.md)** | CCSD / CNRS | 2002 | 2,827,378 notices + **1,788,688 with files** [API] | INRIA/CEA/LIRMM: CRDTs, CompCert, Coq, Frama-C, robotics |
| **[Zenodo](zenodo.md)** | CERN + OpenAIRE | 2013 | **7,231,589** records; **284,518** software concepts [API] | How research code, firmware and datasets become citable |
| **[TechRxiv](techrxiv.md)** | IEEE | 2019 | **18,890** items [API] | The open copy of IEEE-bound work |
| **[Optimization Online](optimization-online.md)** | Math. Optimization Society | 2000 | **9,843** eprints [API] | Solvers, MILP, scheduling — IPOPT, JuMP, SCIP |
| **[engrXiv](engrxiv.md)** | Open Engineering Inc | 2016 | **5,871** records [API] | Broad engineering; mostly civil/mechanical |
| **[ECSarXiv](ecsarxiv.md)** | Electrochemical Society | 2018 | **323** preprints [API] | Batteries, MEMS, gas sensors, semiconductor process |
| **[ChemRxiv](chemrxiv.md)** | ACS-led consortium | 2017 | **53,678** preprints [API] | Battery/electrolyte chemistry, semiconductor materials |
| **[figshare](figshare.md)** | Digital Science / Springer Nature | 2011 | **4,106,613** DOIs (figshare.com) [API] | Generalist; **infrastructure** under other servers |
| **[BioHackrXiv](biohackrxiv.md)** | OSF / DBCLS / ELIXIR | 2020 | **163** unique works [API] | Workflow engines, FAIR tooling, hackathon software reports |
| **[ChinaXiv](chinaxiv.md)** | CAS National Science Library | 2016 | **47,362** native (CS 2,052) [API] | Chinese-language CS; small but real |
| **[SSRN](ssrn.md)** | Elsevier | 1994 | ~1.5 M papers; CS network 108,252 [WEB] | Thin for CS; authoritative for law/econ |

### Marginal or misrepresented

| Server | Verdict |
|---|---|
| **[Synthical](synthical.md)** | **Not a repository.** An AI reader over arXiv/bioRxiv/medRxiv/ChemRxiv. Registered with neither Crossref nor DataCite — mints nothing. Unreachable on 2026-09-01 |
| **[ScienceOpen](scienceopen.md)** | **A discovery layer.** Hosts ~3,584 preprints, *indexes* ~100 M. Wikipedia's ">1,000,000" is wrong as a hosting figure by ~2 orders of magnitude |
| **[Authorea](authorea.md)** | A writing tool that became a preprint host, then a Wiley asset. **Direct submissions suspended May 2026** |
| **[Qeios](qeios.md)** | 95% of its DOIs are wiki-style definitions and reviews. **The computing corpus is 63 papers** |
| **[Preprints.org](preprints-org.md)** | Real screening, real DOIs, 137,380 preprints — but operated by MDPI, and 230 of its 232 "friendly journals" are MDPI titles |
| **[Research Square](research-square.md)** | The largest preprint server on earth (468,390) because Springer Nature auto-posts submissions. **On rejection the journal branding is stripped and the preprint stays** |
| **[viXra](vixra.md)** | 46,051 e-prints, **zero** endorsement or review. Computing categories total 2,740. **Do not cite as evidence for anything** |
| **[OSF Preprints](osf-preprints.md)** | Infrastructure under 32 branded servers, **14 open / 18 closed**. Wikipedia's ">1,000,000" was federated *metadata*, never hosted content |

---

## 2. Grouped records

Servers with little or no hardware/software content, documented compactly.

| Record | Covers |
|---|---|
| [`biorxiv-and-medrxiv.md`](biorxiv-and-medrxiv.md) | bioRxiv (**347,954**) and medRxiv (**88,194**) — deep, because `Bioinformatics` is **30,363** preprints of scientific software |
| [`life-science-and-medical-platforms.md`](life-science-and-medical-platforms.md) | F1000Research and its five funder clones, PeerJ Preprints, Lancet, Cell Sneak Peek, Nature Precedings, JMIR, ARPHA, Beilstein, agriRxiv |
| [`regional-and-national-servers.md`](regional-and-national-servers.md) | Jxiv, SciELO Preprints, AfricArXiv, Arabixiv, IndiaRxiv, INArxiv, LatArXiv, Preprints.ru, AIJR |
| [`repec-and-econstor.md`](repec-and-econstor.md) | RePEc (a federation, **not** a repository) and EconStor |
| [`library-science-and-cognitive-archives.md`](library-science-and-cognitive-archives.md) | CogPrints, E-LIS, LISSA |
| [`social-sciences-and-humanities.md`](social-sciences-and-humanities.md) | SocArXiv, PsyArXiv, EdArXiv, APSA, LawArXiv, CrimRxiv, MediArXiv, BodoArXiv, hprints, MetaArXiv, MindRxiv, PhilArchive, PhilSci-Archive, LingBuzz, Rutgers Optimality Archive |
| [`natural-sciences-and-niche-servers.md`](natural-sciences-and-niche-servers.md) | EarthArXiv, ESSOAr, EcoEvoRxiv, PaleorXiv, MarXiv, NutriXiv, SportRxiv, FocUS, Eyexiv, mp_arc, Frenxiv, WikiJournal Preprints |
| [`closed-and-defunct-servers.md`](closed-and-defunct-servers.md) | Every server that closed, froze, or lost its front door — and whether the content survived |

---

## 3. Beyond preprints — where the rest of the literature lives

A preprint server is only one of several places a technical paper can legitimately be free. These
records were added because the first round made it obvious that **the literature this knowledge base
actually depends on is mostly not on any preprint server at all.**

| Record | Covers | Why it matters here |
|---|---|---|
| **[`additional-preprint-servers.md`](additional-preprint-servers.md)** | **ECCC** (4,832 reports since 1994) · **OpenReview** (4,634 venues) · **ACL Anthology** (131,040 entries) · **INSPIRE-HEP** (1,882,844) · **CERN Document Server** (578,928) · SciPost · Open Research Europe · PCI · VeriXiv · Cambridge Open Engage · **dblp** (8,748,412) | Wikipedia's list **omits the two most important computing servers**: ECCC is the theoretical-CS analogue of Cryptology ePrint, and OpenReview publishes ICLR/NeurIPS **reviews and rebuttals**, not just papers |
| **[`open-access-full-text-sources.md`](open-access-full-text-sources.md)** | Unpaywall · OpenAlex · Semantic Scholar/S2ORC · CORE · BASE · OpenAIRE · DOAJ · dblp · **USENIX** · ACM OPEN · PMC/Europe PMC · HathiTrust · CiteSeerX | **USENIX made every proceedings paper free in 2008.** Given that MapReduce, GFS, Raft, Spark and ZooKeeper are on no preprint server, USENIX *is* the answer for much of the systems literature |
| **[`government-and-institutional-technical-reports.md`](government-and-institutional-technical-reports.md)** | **NASA NTRS** (646,950 records, 358,213 with documents) · **OSTI/DOE PAGES** · DTIC · NIST · **Berkeley EECS** · Cambridge Computer Lab · MIT · **DEC SRC/WRL/CRL** · IETF RFCs | Grey literature is where real electronics engineering lives. **The RISC-V ISA specifications are Berkeley technical reports** — verified here, closing a gap `arxiv.md` had flagged |
| **[`theses-and-dissertations.md`](theses-and-dissertations.md)** | NDLTD · OATD · DART-Europe · **EThOS** · theses.fr/TEL · Shodhganga · DiVA · MIT DSpace · Caltech THESIS · **ETH Research Collection** · Cambridge · ProQuest · **26 verified landmark theses** | **A thesis is often the only complete writeup of a hardware design that exists.** The paper is 8 pages; the dissertation behind it is 150–300, with the schematics, bring-up, measurement setup and negative results the paper had to cut |

**The RISC-V result is the clearest vindication of the whole exercise.** `arxiv.md` recorded that no
canonical RISC-V paper is on arXiv and marked it unresolved. It is resolved now — six Berkeley EECS
technical reports, verified with magic-byte-checked PDFs:

| Report | Title | Date |
|---|---|---|
| **UCB/EECS-2011-62** | The RISC-V Instruction Set Manual, Volume I: Base User-Level ISA | 2011-05-13 |
| **UCB/EECS-2011-63** | Improving Energy Efficiency and Reducing Code Size with RISC-V Compressed | 2011-05-13 |
| **UCB/EECS-2014-54** | …Volume I: User-Level ISA, Version 2.0 | 2014-05-06 |
| **UCB/EECS-2016-1** | Design of the RISC-V Instruction Set Architecture (Waterman PhD) | 2016-01-03 |
| **UCB/EECS-2016-118** | …Volume I: User-Level ISA, Version 2.1 | 2016-05-31 |
| **UCB/EECS-2016-161** | …Volume II: Privileged Architecture Version 1.9.1 | 2016-11-04 |

> ⚠ **Berkeley took these offline mid-survey, then restored them at a new path.**
> During the original pass (2026-09-04) `www2.eecs.berkeley.edu/Pubs/TechRpts/*` 302-redirected to
> `iris.eecs.berkeley.edu`, which served a 58,829-byte themed 404 for every path including the
> series index. **On re-probe 2026-09-11 the series is back on its original host**, at a new
> `/Archive/` path segment:
>
> `https://www2.eecs.berkeley.edu/Pubs/TechRpts/<year>/Archive/<report>.pdf`
>
> All six re-verified HTTP 200 with `%PDF-` magic; `EECS-2016-1` is **959,927 bytes**, exactly
> matching both the pre-outage size and the Wayback capture. Wayback also holds all six
> independently (`2016-1` → `20260409151000`).
>
> For roughly three weeks the canonical RISC-V specifications were unreachable at every published
> URL. The corrected reading is the one this survey reaches everywhere else: **the URLs moved, the
> content was never lost.** See [`VERIFICATION.md §1.1`](VERIFICATION.md#11--berkeley-eecs-is-restored-the-went-dark-finding-was-a-migration-transient).

---

## 4. Recovery, bulk archives and copyright

| Record | Covers |
|---|---|
| **[`recovering-dead-technical-sites.md`](recovering-dead-technical-sites.md)** | Wayback + the CDX API + `save/` · archive.org collection APIs · **bitsavers** · Software Heritage · archive.today Memento · datasheet archives · a decision tree for "the page is gone" |
| **[`bulk-libraries-and-shadow-archives.md`](bulk-libraries-and-shadow-archives.md)** | Sci-Hub · Library Genesis · Anna's Archive · Z-Library · lawful curated collections · the metadata-vs-full-text distinction |

Two things to know before opening either.

**Dead technical sites usually are recoverable.** The DEC SRC/WRL/CRL research-report series —
521 reports across six series — survives **only** because someone mirrored it to bitsavers in 2007.
`hpl.hp.com` still resolves in DNS but its TCP port is dead. The mirror is the archive.

**On shadow libraries, this survey's position is explicit.** They are documented factually — history,
scale, legal status, reliability — and they are documented **last**, after the lawful ladder, because
for technical literature the lawful copy nearly always exists. **No mirror domains, proxy hosts or
access workarounds are recorded anywhere in this directory**: they rotate faster than any document can
track, and they are the circumvention part rather than the reference part. Sci-Hub in particular has
been **frozen since roughly December 2020 – 2021** and is not a route to current research regardless.

The reliability rule matters more than the legal one for our purposes: **a PDF from an unprovenanced
bulk library cannot be verified as the version of record, the correct edition, or unaltered.** Under
[§ Evidence and method](#evidence-and-method) such a file cannot carry an evidence label at all — the
strongest honest label is `[NOT-VERIFIED]`. Resolve the DOI and confirm the record against Crossref,
DataCite or dblp before relying on anything.

---

## 5. Where this survey contradicts its source

Wikipedia's list was the starting point, not the evidence. Six of its claims did not survive
measurement. In each case both readings are recorded in the relevant file.

| Wikipedia says | Measurement says | Record |
|---|---|---|
| OSF Preprints `>1,000,000` | **200,519** hosted across 32 providers. The million was SHARE-federated metadata harvested from six *external* sources | [osf-preprints.md](osf-preprints.md) |
| ScienceOpen `>1,000,000` | **~3,584** hosted preprints; 7,620 DOIs across all prefixes. The rest is an index | [scienceopen.md](scienceopen.md) |
| Synthical `>1,000,000`, "preprint repository" | Hosts **nothing**; zero Crossref and zero DataCite registrations. It is a reader over other servers | [synthical.md](synthical.md) |
| Zenodo created **2011** | Operator's own About page and BibTeX say **May 2013**; Wikipedia's *own Zenodo article* says 2013. The 2011 date probably belongs to a predecessor whose launch we could not confirm | [zenodo.md](zenodo.md) |
| HAL created **2001** | CCSD attributes 2001 to **TEL**, not HAL. HAL's OAI `earliestDatestamp` is **2002-09-23** | [hal.md](hal.md) |
| RePEc provider = "Federal Reserve Bank of St. Louis" | RePEc "has no central expenses" and no operator. Zimmermann runs *IDEAS* and is an AVP there — a half-truth | [repec-and-econstor.md](repec-and-econstor.md) |

Two more, smaller: mp_arc is listed as `>10,000` but its own index yields **6,152** (both recorded,
unresolved); Cell Sneak Peek and Preprints with The Lancet are listed at `>1,000` each but measure
**12,404** and **25,550**.

---

## 6. Probing traps

Findings that will corrupt anyone else's harvest of these servers. All were hit during this pass.

- **`osf.io` returns HTTP 200 and an identical 4,207-byte SPA shell for providers that do not
  exist.** Status code *and* byte size are both uninformative. Use
  `api.osf.io/v2/preprints/?filter[provider]=<slug>` and read `meta.total`. This affects every
  OSF-hosted server on the list.
- **The arXiv API's `max_results=0` is broken** — it returns HTTP 200 with `totalResults=1` and a
  fake entry titled "Error". A harvester using it records **1 for every category**. Use
  `max_results=1`.
- **HAL's subject field is `domainAllCode_s`, not `domain_s`.** The wrong field returns a confident,
  silent `numFound: 0` — the most likely route to a fabricated HAL statistic.
- **Zenodo's API returns HTTP 200 with `total: 0` for invalid facet values**, indistinguishable
  from a genuine zero. Separately, unquoted `RISC-V` returns 422,778 hits against 495 quoted — an
  ~850× inflation from hyphen tokenisation.
- **SSRN networks must never be summed.** The 68 networks total 4,569,102 against ~1.5 M actual
  papers: ≈3.0 cross-listings each.
- **ChinaXiv returns the same 403 for bogus and real IDs** under `/abs/`, so status codes cannot
  test existence there. A bogus `.htm` path does give a true 404.
- **Zenodo, OSF and TechRxiv all count *versions*, not works.** Measured inflation ranged from
  +1.6% to +50% depending on provider; TechRxiv is 30,954 DOI records for 18,890 items.
- **`doi.org` is a usable existence oracle behind a bot wall**: it returns 404 for unregistered DOIs
  but passes through the target's 403 for registered ones. A 403 therefore *confirms* existence.
  **`hdl.handle.net/api/handles/<prefix>/<suffix>` is better still** — it returns JSON
  (`responseCode: 1` vs `100`) from the Handle System rather than the target host, so it works
  straight through Cloudflare and Anubis.
- **`archive.org/wayback/available` returns false negatives.** It reported `archived_snapshots: {}`
  for a URL the CDX API shows continuously archived since 2018. **Confirm absence with CDX**, never
  with `wayback/available` alone — this one fails *toward* phantom link rot.
- **The CDX `length` field is the WARC record length, not the payload size.** Compare the `digest`
  (base32 SHA-1 of the payload) against a local copy instead.

---

## 7. What this pass did not do

Stated so the gaps are visible rather than silent.

- **Nothing here was peer-reviewed, benchmarked or reproduced by us.** This survey documents
  repositories, not the correctness of their contents.
- **No eventual-publication rate was obtained for most servers.** Only bioRxiv/medRxiv publish the
  data (69–78% for mature cohorts), and we derived one for Cryptology ePrint by sampling
  (61.7%, n=60, 95% CI 49.0–72.9%). For arXiv, OSF, SSRN, TechRxiv, engrXiv and ECSarXiv it is
  **[NOT-VERIFIED]** — no citable measurement was found.
- **Eyexiv could not be located at all.** Four TLDs are NXDOMAIN and it is not an OSF provider. It
  is the only entry on the Wikipedia list this pass considers genuinely lost.
- **Moderation rejection rates are unpublished nearly everywhere.** arXiv, ePrint, TechRxiv and
  ChinaXiv all decline to state them. engrXiv is the striking exception — it disclosed that roughly
  **half of 2025 submissions were declined** as AI-generated.
- **No artifact was archived into `archive/`.** This pass produced records, not retained binaries.
  Raw probe output is under [`../../scratch/preprint-repositories/`](../../scratch/preprint-repositories/).
