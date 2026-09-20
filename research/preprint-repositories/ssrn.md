# SSRN — preprint repository record

- **URL:** https://www.ssrn.com/ (browse/landing) · https://papers.ssrn.com/ (abstracts,
  full text — **returns HTTP 403 to every scripted client**, §8)
- **Operator:** **Elsevier** (RELX plc). Acquired from Social Science Electronic Publishing
  Inc. in **May 2016** (S9, S10). Every page footer reads "Copyright © 2026 Elsevier Inc.,
  its licensors, and contributors" (S2) [WEB].
- **Discipline scope:** advertised as **69 disciplines** across six top-level areas —
  applied, health, humanities, life, physical and social sciences (S1) [WEB]. *As actually
  used*: overwhelmingly economics, law, finance and political science; **the Economics
  Research Network alone holds 694,156 papers** against 108,252 in the Computer Science
  Research Network (S3) [API].
- **Launched:** **1994**, by financial economists **Michael C. Jensen** and **Wayne Marr**
  (S10) [LIT/COM].
- **Status:** active, large, growing.
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

> **This record folds in two Wikipedia entries.** *Preprints with The Lancet* and *Cell
> Sneak Peek* are listed by Wikipedia as separate repositories. They are **not**. Both are
> SSRN **First Look** channels running on SSRN infrastructure — verified below with SSRN's
> own participant list and live counts (§3.3). Wikipedia's ">1,000" for each is wrong by
> more than an order of magnitude in both cases.

---

## 1. What it is

SSRN began in 1994 as the **Social Science Research Network**, an email-distribution service
for economics and finance working papers. That origin explains almost everything about its
present shape. In economics and law, the *working paper* — circulated, cited and often
career-decisive years before any journal touches it — is the primary unit of scholarly
communication, not a stopgap. SSRN industrialised that habit.

The architecture is a **network of networks**. Papers are not filed into a subject tree;
they are *distributed* to subscriber lists. An author submits once; SSRN classifies the
paper into one or more **Research Networks** (68 of them), and within each network into one
or more **eJournals** (subject-area alert feeds). Subscribers get email digests. In SSRN's
own words, this is the differentiator: "While many preprint servers operate as content
repositories, SSRN maximizes usage and discoverability by classifying papers into
topic-based email alerts that are distributed to subscribers. This results in downloads and
citations that SSRN aggregates into meaningful metrics that authors use for promotion and
tenure purposes and that institutions use in their hiring and ranking activities." (S6)
[DOC].

Read that last sentence carefully. SSRN is explicit that its product is **metrics for
career advancement**, not just archiving. The download counter is the point. This is why
SSRN top-ten download lists appear on law-school faculty pages, and it is also why SSRN's
incentive structure differs sharply from arXiv's.

Since **May 2016** SSRN has been owned by **Elsevier** (S9, S10). It sits alongside Mendeley
and, since then, has been wired into Elsevier's journal workflow: the **First Look**
programme lets authors post a preprint with one click during submission to a participating
Elsevier journal (§3.3). SSRN is now, functionally, Elsevier's preprint server — its own
support hub says so in a headline: *"Welcome to SSRN, Elsevier's Preprint Server"* (S6)
[DOC].

For this knowledge base the summary is: **SSRN is a genuinely important repository that is
mostly not about anything you work on**, plus a real cautionary tale about commercial
ownership of preprint infrastructure (§10).

## 2. Scope and subject taxonomy — the parts that matter here

**Top level:** six discipline groups (Applied / Health / Humanities / Life / Physical /
Social Sciences) (S1) [WEB].

**Second level:** **68 Research Networks**, enumerated exhaustively from the network
selector present on every network page (S2) [WEB]. Note the conflict: the homepage counter
says "**69** Disciplines" (S1); the selector lists **68** (S2). Both retrieved 2026-09-01.
Recorded, not resolved. Wikipedia's "More than 55 disciplines" (S11) is stale on both
counts.

**Third level:** **eJournals** — subject-area feeds within each network. These are the real
categories, closest in function to arXiv's `cs.*` codes, and they are the level at which you
should search.

**The computing and engineering networks, with their eJournals:**

*Computer Science Research Network* (`compscirn`) — 14 subject eJournals (S4) [API]:

| eJournal | Binding ID | Papers (2026-09-01) |
|---|---|---|
| Artificial Intelligence | 3178495 | **56,562** |
| Applied Computing | 3191581 | 21,443 |
| Information Systems | 3178509 | 14,160 |
| Cybersecurity, Privacy, & Networks | 3178533 | 12,247 |
| Computation Theory | 3176750 | 8,624 |
| Human-Computer Interaction | 3177962 | 6,310 |
| **Software Engineering** | 3178522 | **6,122** |
| Robotics | 3178493 | 5,838 |
| Computer Science Education | 3216966 | 5,726 |
| Computing Methodology | 3191574 | 4,253 |
| High Performance Computing | 3191612 | 2,484 |
| Other Computer Science Research | 4578131 | 2,300 |
| Web Technology | 3191618 | 2,105 |
| Computer Science Negative Results | 3216949 | 541 |
| **Sum** | | **148,715** |

*Engineering Research Network* (`engrn`) — 15 eJournals (S4) [WEB]: Aerospace, Automotive,
Bioengineering, Chemical, Civil, Computational Fluid Dynamics, **Electrical Engineering**,
Energy, Engineering Education, Engineering Negative Results, Environmental, Industrial &
Manufacturing, Materials, Mechanical, and a hidden "z-Other Engineering Research".

*Information Systems & eBusiness Network* (`isn`) — 9 eJournals including Information
Technology & Systems, eBusiness & eCommerce, and Emerging Legal Issues in Information
Systems (S4) [WEB].

*Materials Science Research Network* (`matscirn`) — 13 eJournals including **Electronic,
Optical & Magnetic Materials**, Computational Materials Science, Nanomaterials, Corrosion
(S4) [WEB].

Three observations a reader should take away:

1. **"Software Engineering" holds 6,122 papers.** For comparison, arXiv's `cs.SE` is an
   order of magnitude larger and vastly better known. SSRN is not where software
   engineering happens.
2. **"Artificial Intelligence" (56,562) is 38% of the whole CS network** and is the only
   SSRN computing category with real mass. Much of it is AI-and-*something* —
   AI-and-law, AI-and-management, AI-and-policy — which is exactly what you would expect
   from SSRN's social-science centre of gravity. The newest CompSciRN paper on 2026-09-01
   was *"Should We Allow AI to Police Itself? Assessing the Technical Feasibility and Legal
   Implications of LLM-Based Agent Evaluation"* by authors at Oxford Saïd Business School
   and European University Viadrina (S4) [API]. That is the house style.
3. **The eJournal sums exceed the network totals** (148,715 across CS eJournals vs 108,252
   in the CS network) because **papers are multiply classified**. See §3.2 — this is the
   single most important thing to understand before quoting any SSRN number.

## 3. Size and growth

### 3.1 SSRN's own headline counters

From the SSRN homepage, "SSRN by the numbers", retrieved **2026-09-01** (S1) [WEB]:

| Counter | Value |
|---|---|
| Full text papers | **over 1.5 million** |
| Authors | **over 1.9 million** |
| Paper downloads | **over 300 million** |
| Total references | **over 47 million** |
| Total citations | **over 2 million** |
| Disciplines | **69** |

These are rounded marketing figures, not live counts. A dated growth anchor: Inside Higher
Ed, reporting in July 2016, stated "SSRN's database contains more than 557,000 full-text
papers" (S9) [COM]. **1.5 M in 2026 against 557 k in mid-2016 — roughly 2.7× in ten years**
[INF].

### 3.2 The network table — measured, not advertised

Retrieved 2026-09-01 from SSRN's own (undocumented) statistics endpoint
`https://www.ssrn.com/rest/rn/statistics/<network-id>`, one call per network, ids scraped
from each network's landing page (S3) [API]. All 68 networks; sorted by papers.

| # | Slug | Network | Papers | Authors | Downloads |
|---|---|---|---|---|---|
| 1 | `ern` | Economics Research Network | **694,156** | 483,483 | 176,127,090 |
| 2 | `lsn` | Legal Scholarship Network | **424,464** | 195,316 | 123,661,781 |
| 3 | `psn` | Political Science Network | **346,704** | 280,140 | 80,043,922 |
| 4 | `fen` | Financial Economics Network | **269,931** | 170,120 | 108,617,336 |
| 5 | `engrn` | **Engineering Research Network** | **194,984** | 642,236 | 12,842,427 |
| 6 | `srpn` | Sustainability Research & Policy | 162,463 | 336,089 | 32,930,506 |
| 7 | `mrn` | Management Research Network | 152,716 | 188,377 | 55,268,367 |
| 8 | `chemrn` | Chemistry Research Network | 140,072 | 505,586 | 7,620,137 |
| 9 | `matscirn` | **Materials Science Research Network** | 123,100 | 457,254 | 6,698,460 |
| 10 | `environscirn` | Environmental Science Research Network | 115,379 | 383,741 | 11,249,765 |
| 11 | `irpn` | Innovation Research & Policy Network | 115,367 | 132,868 | 38,005,166 |
| 12 | `aarn` | Anthropology & Archaeology Research Network | 114,524 | 104,273 | 26,265,644 |
| 13 | `medrn` | Medical Research Network | 109,129 | 619,963 | 10,577,432 |
| 14 | `compscirn` | **Computer Science Research Network** | **108,252** | 261,370 | 18,572,774 |
| 15 | `energyrn` | Energy Research Network | 91,506 | 278,672 | 7,486,730 |
| 16 | `psychrn` | Psychology Research Network | 77,551 | 170,962 | 16,162,640 |
| 17 | `biorn` | Biology Research Network | 75,303 | 398,103 | 6,416,967 |
| 18 | `physicsrn` | Physics Research Network | 70,929 | 251,986 | 3,044,477 |
| 19 | `cgn` | Corporate Governance Network | 70,405 | 68,712 | 29,784,448 |
| 20 | `erpn` | Entrepreneurship Research & Policy Network | 63,310 | 72,875 | 21,901,238 |
| 21 | `edurn` | Education Research Network | 60,477 | 79,573 | 15,182,463 |
| 22 | `isn` | **Information Systems & eBusiness Network** | **58,848** | 69,961 | 19,563,242 |
| 23 | `arn` | Accounting Research Network | 57,948 | 49,684 | 27,002,726 |
| 24 | `prn` | Philosophy Research Network | 57,293 | 47,084 | 15,827,142 |
| 25 | `sociologyrn` | Sociology Research Network | 42,559 | 61,896 | 7,269,580 |
| 26 | `wgsrn` | Women's & Gender Studies Research Network | 41,056 | 50,217 | 10,048,288 |
| 27 | `agriscirn` | Agricultural Science Research Network | 41,000 | 165,242 | 3,498,387 |
| 28 | `decisionscirn` | Decision Science Research Network | 40,464 | 62,214 | 10,638,834 |
| 29 | `csn` | Cognitive Science Network | 35,870 | 59,384 | 11,624,936 |
| 30 | `mathrn` | Mathematics Research Network | 33,655 | 80,224 | 2,400,434 |
| 31 | `finplanrn` | Financial & Investment Planning Research Network | 31,953 | 34,531 | 10,565,445 |
| 32 | `foodscirn` | Food Science Research Network | 31,883 | 115,185 | 3,215,190 |
| 33 | `earthscirn` | Earth Science Research Network | 29,022 | 98,882 | 2,135,716 |
| 34 | `ecorn` | Ecology Research Network | 28,328 | 115,881 | 2,413,121 |
| 35 | `org` | Organizational Behavior | 26,295 | 43,255 | 9,052,943 |
| 36 | `infoscirn` | Information & Library Science Research Network | 26,055 | 49,710 | 6,752,516 |
| 37 | `oper` | Operations Research Network | 25,468 | 52,401 | 5,752,028 |
| 38 | `transportrn` | Transportation Research Network | 24,620 | 50,745 | 4,076,409 |
| 39 | `biochemrn` | Biochemistry Research Network | 24,429 | 159,987 | 1,313,072 |
| 40 | `publichealthrn` | Public Health Research Network | 23,851 | 81,781 | 2,553,061 |
| 41 | `geographyrn` | Geography Research Network | 23,151 | 58,278 | 3,607,023 |
| 42 | `cjrn` | Criminal Justice Research Network | 21,978 | 21,166 | 5,664,723 |
| 43 | `commrn` | Communication Studies Research Network | 21,038 | 37,552 | 5,768,652 |
| 44 | `pol` | Corporate Strategy & Business Policy Research Network | 17,438 | 31,826 | 6,751,462 |
| 45 | `sirn` | Social Insurance Research Network | 22,506 | 14,248 | 2,468,924 |
| 46 | `mkt` | Marketing Research Network | 19,931 | 25,352 | 7,868,413 |
| 47 | `pharmscirn` | Pharmaceutical Science Research Network | 17,969 | 105,780 | 1,528,327 |
| 48 | `intl` | International Business & Management Research Network | 17,947 | 29,930 | 6,280,369 |
| 49 | `neuroscirn` | Neuroscience Research Network | 16,899 | 77,829 | 1,870,735 |
| 50 | `hen` | Health Economics Network | 16,624 | 27,678 | 4,641,154 |
| 51 | `geologyrn` | Geology Research Network | 15,081 | 63,132 | 1,024,147 |
| 52 | `lingrn` | Linguistics Research Network | 12,217 | 17,682 | 1,760,233 |
| 53 | `historyrn` | History Research Network | 9,778 | 9,160 | 1,539,795 |
| 54 | `lit` | Literature Research Network | 8,871 | 7,488 | 2,347,034 |
| 55 | `bhnp` | Business History & Nonprofit Organizations Research Network | 7,942 | 10,511 | 1,962,619 |
| 56 | `forensicscirn` | Forensic Science Research Network | 6,977 | 12,820 | 2,307,798 |
| 57 | `archrn` | Architecture Research Network | 6,875 | 20,295 | 694,096 |
| 58 | `vetscirn` | Veterinary Science Research Network | 6,526 | 35,738 | 504,962 |
| 59 | `lrn` | Leadership Research Network | 6,423 | 9,924 | 2,244,606 |
| 60 | `rwrn` | Rhetoric & Writing Research Network | 6,153 | 9,538 | 2,466,519 |
| 61 | `neg` | Negotiations & Dispute Resolution Network | 4,879 | 6,090 | 2,912,105 |
| 62 | `artsrn` | Visual, Performing & Fine Arts Research Network | 4,865 | 6,933 | 1,209,691 |
| 63 | `planetscirn` | Space & Planetary Science Research Network | 3,947 | 7,775 | 321,222 |
| 64 | `nursingrn` | Nursing Research Network | 3,642 | 12,092 | 646,406 |
| 65 | `hrn` | Hebrew Research Network | 3,359 | 1,849 | 607,233 |
| 66 | `crn` | Classics Research Network | 1,951 | 2,074 | 641,495 |
| 67 | `dentistryrn` | Dentistry Research Network | 1,754 | 9,235 | 205,948 |
| 68 | `mrcn` | Music Research & Composition Network | 1,062 | 1,689 | 245,784 |

**Sum of the "papers" column: 4,569,102.** Against a stated corpus of ~1.5 million full-text
papers, that implies **every paper sits in ~3.0 networks on average** [INF]. Any statement
of the form "SSRN has N papers in field X" is therefore an over-count of the same corpus
seen from a different angle, and network figures **must not be added**. The same applies at
eJournal level (§2).

**Downloads column sum: 1,034,254,315** against a stated ~300 million downloads (S1) — the
same ~3.4× multiple, from the same cause [INF].

### 3.3 First Look — where "Preprints with The Lancet" and "Cell Sneak Peek" actually live

**First Look** is SSRN's journal-integration programme: "a partnership between SSRN and some
of the world's most influential journals … With one click during the submission process to
the journal, authors choose to post a preprint of their paper on SSRN" (S5) [DOC]. The
participant list (S5, retrieved 2026-09-01) includes **Cell Press** and **The Lancet**
alongside Acta Materialia, Heliyon, *Journal of Web Semantics*, *Materials Today*,
*NeuroImage: Clinical*, *Journal of Economic Dynamics and Control*, *Scientific African*,
*Surgery Open Science*, *Ultrasonics Sonochemistry* and others.

**Verified: both Wikipedia "repositories" are SSRN channels.**

| Channel | SSRN URL | SSRN binding ID | Papers (2026-09-01) | Wikipedia says |
|---|---|---|---|---|
| **Preprints with The Lancet** | `ssrn.com/index.cfm/en/the-lancet/` | 3184962 | **25,561** (S4) [API]; page counter shows 25,550 (S5) [WEB] | ">1,000" (S11) |
| **Cell Press Sneak Peek** | `ssrn.com/index.cfm/en/cell-press-sneak-peek/` | 3184889 | **12,414** (S4) [API]; page counter shows 12,404 (S5) [WEB] | ">1,000" (S11) |

The Lancet channel's own description states its screening explicitly: "Preprints available
here are not Lancet publications or necessarily under review with a Lancet journal. These
preprints are early-stage research papers that have not been peer-reviewed. **The usual SSRN
checks and a Lancet-specific check for appropriateness and transparency have been applied.**
The findings should not be used for clinical or public health decision-making" (S5) [DOC].

Cell Sneak Peek is different in kind — it is *not* an open preprint server but "an author
opt-in preview of the papers under review in our primary research journals" (S5) [DOC], with
a per-journal breakdown on its landing page (Cell 778, Cell Reports 2,545, iScience 3,283,
Current Biology 883, Neuron 488, Joule 395 …). **A Sneak Peek posting means the paper is
under review at a specific Cell Press journal.** That is a meaningfully different signal
from a preprint deposit and Wikipedia's flat listing loses it.

**Consequence for the Wikipedia list:** SSRN's own row claims it "Aggregates over 30 preprint
servers (Preprints with *The Lancet*, Cell Sneak Peek, etc.)" (S11). That is the wrong verb.
SSRN does not aggregate anything; it **hosts** journal-branded channels on one database.
There is no federation and no harvesting. Compare [osf-preprints.md](osf-preprints.md) §10,
where "aggregates" was literally true and is now obsolete — two different errors that happen
to look alike in a table.

## 4. Screening and moderation — what gets in

**SSRN does screen, and it screens harder than most preprint servers.** This is documented,
current, and worth reading in full because it is unusually specific.

**Submission requirements** (S6, *"How do I submit a paper to SSRN?"*, last updated
2026-08-03) [DOC]:

- Free SSRN account with a complete author profile.
- Title and abstract **in English**; full-text **PDF in English** displaying title and all
  authors with affiliations.
- "Names, current affiliations, and valid email addresses of all authors — **Organizations
  cannot be listed as authors** (exceptions are government- or academic-related
  organizations)."
- Copyright-holder permission where applicable.
- "**An AI disclosure statement (if using AI)** — must be included with the abstract and
  display on the PDF. NOTE: AI features used solely for accessibility via disability
  assistive technology are exempt."
- Medical/health papers additionally require patient confidentiality, patient consent, and
  conflict-of-interest/funding disclosures, per SSRN's *Medical or Health Care Preprint
  Checklist*.

**Explicit exclusion list** — "Content types that are typically NOT accepted" (S6, verbatim)
[DOC]:

> Abstract-only submissions · Books / book chapters · Calls for papers · Class assignments /
> course projects · **Conference proceedings** · Frameworks · Guides and how-to's · News
> articles · Non-English content · Non-scholarly articles (including, but not limited to:
> articles with no references, some commercial/marketing material) · **Presentation slides**
> · Published papers in certain disciplines · **Research written by high school students and
> faculty**

Two of those matter for an engineering reader: **conference proceedings are excluded**
(so SSRN is structurally unable to be a systems/architecture venue, where the conference
paper *is* the publication), and **"frameworks"** are excluded — apparently an
anti-content-mill measure.

**And even eligible content may be refused:** "Submissions may be rejected for missing
information, failure to meet Research Integrity standards and editorial policies, or
non-compliance with our Terms of Use." (S6) [DOC]

**Turnaround:** "Most submissions are processed quickly, though some may take up to 10
business days." Named causes of delay include "**Verification Processes**: Verify any
competing interests and confirm author identities" and "**Legal or Rights Clearance**:
Confirming permissions for copyrighted material" (S6, last updated 2026-07-20) [DOC].
SSRN's support site carries a whole help category titled **"Preprint Rejections"** (S6)
[DOC] — a category no other server in this collection has.

**What it is not.** SSRN states it plainly: "SSRN is a platform for the dissemination of
early-stage research. **We are not a peer-reviewed journal**, and we do not publish or
distribute hard copies. Posting a paper to SSRN and/or distributing it in one of SSRN's
email alerts does not make it Accepted or Published" (S6) [DOC].

**Assessment.** The screen is real — identity verification, rights clearance, an AI
disclosure mandate, an explicit exclusion list, a rejections help category. It is closer to
a journal's desk-check than to arXiv's moderation, and much stronger than
[OSF Preprints](osf-preprints.md) or [Zenodo](zenodo.md). It is still **not** a check on
whether the research is correct.

## 5. Reliability — what you can and cannot trust

**Where SSRN is genuinely authoritative:** law, economics, finance, accounting, corporate
governance. In these fields the SSRN working paper is a **primary literature object**.
Central-bank and NBER-style working papers, law-review preprints, and finance research
circulate here first and are cited here for years. A citation to an SSRN abstract ID in a
law-review footnote is unremarkable and appropriate. The download and citation counters,
whatever their distortions, are used in real hiring and tenure decisions (S6) [DOC] — that
is an unusual degree of institutional embedding for a preprint server.

**Where it is thin — be honest about computing.** SSRN's computing content is weak compared
with arXiv, and the numbers say so:

- Software Engineering: **6,122** papers, ever, across the whole life of the server (S4)
  [API].
- High Performance Computing: **2,484**. Web Technology: **2,105**. Computation Theory:
  **8,624**.
- Conference proceedings — the dominant publication form in systems, architecture,
  networking, PL and security — are **explicitly not accepted** (§4) [DOC].
- The corpus skews to *AI-and-policy*, *AI-and-law*, information-systems-as-business-school-
  discipline, and management-of-technology. Real systems work is essentially absent.

**Practical rule: if you are looking for a computing preprint, check arXiv first, the
[Cryptology ePrint Archive](cryptology-eprint-archive.md) for crypto, and
[TechRxiv](techrxiv.md) for IEEE-adjacent engineering. Check SSRN only when the paper has a
law, economics, policy or business-school angle — and then check it seriously, because for
those angles SSRN is where the work is.**

**What a deposit guarantees:**

- A stable abstract ID and URL (`ssrn.com/abstract=NNNNNNN`).
- **A Crossref DOI** in the `10.2139/ssrn.<id>` namespace — "SSRN, as a registered Crossref
  member, pays for this DOI assignment, and automatically assigns a preprint DOI to
  qualifying papers at no cost to authors." Assigned to "posted preprint submissions that
  have completed the SSRN review process and include a full-text PDF", typically "within a
  few business days after the review process has been completed" (S6) [DOC].
- **DOIs are not removable**: "Once a DOI is assigned, it becomes a permanent record of that
  preprint … neither the DOI string nor the assignment itself can be changed or deleted
  after registration. If a paper is retracted or withdrawn, its DOI will redirect to a
  retraction or withdrawal notice on SSRN's website." (S6) [DOC] This is a materially
  stronger persistence commitment than OSF currently honours (see
  [osf-preprints.md](osf-preprints.md) §6, where recent deposits have no DOI at all).
- That a human checked identity, rights, language and content type (§4).
- Nothing about correctness.

**Known failure modes:**

1. **Author self-removal is one click.** SSRN's own instructions: My Papers → Modify →
   "Make it Inactive — Remove it from SSRN's eLibrary … The status will change to REMOVED"
   and the paper becomes unavailable to SSRN and external search engines (S6) [DOC]. The
   DOI survives and redirects to a notice; the PDF does not. **If an SSRN paper matters to
   you, keep your own copy.**
2. **Publisher lock-in on some records.** "Why does my submission not have a Modify button,
   and why is it Restricted by Publisher? The publisher, journal, or series does not allow
   changes to submissions." (S6) [DOC] — for First Look records, the journal, not the
   author, controls the object.
3. **Operator-initiated removal over copyright.** This has actually happened. §10.2.
4. **Download-count gaming.** SSRN's rankings are career-relevant (§1), which creates the
   obvious incentive. SSRN has published rank-manipulation countermeasures; I did not
   retrieve a current policy document. **[NOT-VERIFIED].**
5. **Under-review ≠ preprint.** A Cell Sneak Peek record means "under review at journal X"
   (§3.3). Do not cite it as a stable preprint; it may vanish into a paywalled version of
   record.

**How to sanity-check an individual SSRN paper:**

1. Resolve `https://doi.org/10.2139/ssrn.<abstract_id>` — a DOI redirecting to a withdrawal
   notice is the loudest available signal. (Note: the resolution itself will land on a 403
   for a scripted client; use a browser — §8.)
2. Look at which network(s) and eJournal(s) it is filed under. A "computer science" paper
   filed only in Legal Scholarship Network is telling you something.
3. Check `publication_status` — SSRN records carry values such as `UNDER REVIEW` and
   `Working Paper Series` (S4) [API].
4. Search for a journal version. In economics and law, the SSRN version is often the *only*
   version and that is normal; in CS it usually means the work went nowhere.
5. Archive the PDF. See failure mode 1.

**Eventual-publication rate: [NOT-VERIFIED].** I found no measurement I could cite within
this pass. It would in any case be misleading to quote a single figure across a corpus where
law and economics working papers are frequently terminal by design.

## 6. What you actually find there — examples

Retrieved live from the CompSciRN paper feed, 2026-09-01 (S4) [API]:

- *"Should We Allow AI to Police Itself? Assessing the Technical Feasibility and Legal
  Implications of LLM-Based Agent Evaluation"* — Matthias Holweg (Oxford, Saïd Business
  School) and Philipp Hacker (European University Viadrina, European New School of Digital
  Studies). Abstract ID 7378338, `Working Paper Series`, `publication_status: UNDER REVIEW`,
  35 pages, approved 2026-09-02.

That single record is a fair sample of SSRN computing content: a technically literate paper
about computing, written from a law/business-school vantage, by authors who would never
consider arXiv `cs.SE`. It is good work in its own frame. It is not a systems paper.

Structurally, what you find on SSRN is:

- **Law-and-technology**: platform regulation, AI liability, data protection, algorithmic
  accountability — Legal Scholarship Network, 424,464 papers, the second-largest network.
- **Economics of technology**: innovation, IP, network effects, digital markets —
  Innovation Research & Policy Network, 115,367 papers.
- **Information systems as a business-school discipline** — 58,848 papers.
- **Applied engineering and materials** — Engineering Research Network 194,984 and
  Materials Science 123,100, which are *larger* than CompSciRN, and are the parts of SSRN
  a hardware engineer is most likely to touch.
- **Medical preprints via The Lancet channel** — 25,561.

**No landmark-papers table.** SSRN hosts nothing foundational in software, distributed
systems, databases, electronics or security; those literatures live on arXiv, in ACM/IEEE
proceedings, and in the [Cryptology ePrint Archive](cryptology-eprint-archive.md). SSRN
*is* foundational in law and financial economics, which is outside this collection's scope.
Listing a table would be padding.

## 7. Access, APIs and bulk retrieval — SSRN is hostile to scripted access

**Verified 2026-09-01. This section is the practical one.**

### 7.1 What is blocked

| Target | Default UA | Browser UA | Verdict |
|---|---|---|---|
| `https://www.ssrn.com/index.cfm/en/` | **403** (5,421 B) | **200** (70,049 B) | UA-gated; browser UA works |
| `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7378338` | **403** | **403** | **hard-blocked** |
| `https://papers.ssrn.com/sol3/DisplayAbstractSearch.cfm` | — | **403** | **hard-blocked** |
| `https://doi.org/10.2139/ssrn.7378338` (follows redirect) | — | **403** at `papers.ssrn.com` | **the DOI resolver lands on a block page** |
| `https://api.ssrn.com/` (root) | **403** (23 B) | — | root is closed |

**Full user-agent ladder against a `papers.ssrn.com` abstract page** (per
[AGENTS.md](../../AGENTS.md) §Web retrieval fallback), all 2026-09-01:

| User-Agent | Result |
|---|---|
| curl default | 403, 5,526 B |
| Chrome 131 desktop | 403, 5,761 B |
| `WhatsApp/2.23.20.0` | 403, 5,526 B |
| `ChatGPT-User/1.0` | 403, **896,437 B** |
| `ClaudeBot/1.0` | 403, **896,437 B** |
| `Googlebot/2.1` | 403, 5,589 B |

**Every agent is refused.** The two AI-crawler agents get a 403 with a ~900 kB body — an
interstitial/challenge page rather than the short block page. The ladder does not open this
door; **`papers.ssrn.com` requires a real browser session and there is no polite workaround.
Do not spend time rotating agents against it.**

`robots.txt` (identical on `www.` and `papers.`, 2026-09-01) (S7) [DOC]:

```
User-agent: GPTBot          Disallow: /
User-agent: ChatGPT-User    Disallow: /
User-agent: Google-Extended Disallow: /
User-agent: *               Crawl-Delay: 5
                            Disallow: /admin/ /tasks/ /config/
Sitemap: https://papers.ssrn.com/sitemap/sitemaps.cfm
Sitemap: https://papers.ssrn.com/sitemap/sitemaps.cfm?dir=authors
```

Named AI crawlers are banned outright; everything else is nominally allowed at a 5-second
crawl delay, which the 403s on `papers.ssrn.com` contradict in practice.

### 7.2 What works

**There is no documented public API. There is an undocumented one, and it is how every
number in §2 and §3.2 was obtained.** Both endpoints are the JSON backends of SSRN's own
web widgets, discovered from `data-url` attributes in the network page HTML:

| Endpoint | Returns |
|---|---|
| `https://www.ssrn.com/rest/rn/statistics/<network-id>` | `{"statistics":[{"number":…,"name":"authors"},{…"papers"},{…"downloads"},{…"abstractviews"}]}` |
| `https://www.ssrn.com/rest/rn/subject-areas/<network-id>` | the network's eJournal list with `journal_id`s |
| `https://www.ssrn.com/rest/rn/recent-papers/<network-id>?limit=N` | recent items |
| `https://api.ssrn.com/content/v1/bindings/<binding-id>/papers` | `{"total": N, "papers":[…]}` with title, authors, affiliations, page count, `publication_status`, download counts, approval date |

Caveats: undocumented, unversioned in any published contract, subject to change without
notice, and served with HTML whitespace prepended to the JSON on the `/rest/rn/` paths (parse
from the first `{`). No authentication was required and no rate limit was hit across ~150
sequential calls. Use `Crawl-Delay: 5` as your conscience dictates; I did not.

### 7.3 Negative controls

| Probe | Result | Lesson |
|---|---|---|
| `https://api.ssrn.com/content/v1/bindings/999999999/papers?size=1` | **HTTP 200**, `{"total": 0, "papers": []}` | **a bogus binding ID returns a clean zero.** Identical to a genuinely empty eJournal. Only IDs harvested from a real subject-areas response can be trusted |
| `https://www.ssrn.com/index.cfm/en/networks/` (invented path) | **404**, 19,267 B | www.ssrn.com 404s honestly — good |
| `https://www.ssrn.com/index.cfm/en/cspn/` (invented slug) | **404**, 19,267 B | same |
| `https://papers.ssrn.com/oai` | **HTTP 200**, 19,157 B, `<title>Page Cannot be Found</title>` | **soft-404.** A 200 here means nothing |
| `https://papers.ssrn.com/definitely-not-a-real-path-xyzzy` | **HTTP 200**, 19,157 B, same "Page Cannot be Found" | confirms the soft-404 |
| `https://papers.ssrn.com/sol3/oai` | **HTTP 200**, 19,157 B, same | confirms |

### 7.4 OAI-PMH — verified absent

**SSRN has no OAI-PMH endpoint.** `papers.ssrn.com/oai`, `papers.ssrn.com/sol3/oai` and
`www.ssrn.com/oai/request?verb=Identify` were all probed 2026-09-01: the first two return the
soft-404 "Page Cannot be Found" page with HTTP 200 (byte-identical to a deliberately bogus
path), and the third returns a genuine 404 (S8) [WEB]. No OAI-PMH base URL is advertised
anywhere on SSRN's site or support hub. This is a real structural difference from
[EconStor](repec-and-econstor.md), [E-LIS](library-science-and-cognitive-archives.md) and
essentially every repository built on DSpace or EPrints, and it means SSRN's metadata is not
harvestable by BASE, CORE or OpenAIRE through the standard route.

**Bulk dumps:** none offered. **Sitemaps** are advertised in `robots.txt` and are the only
sanctioned enumeration path; they live on the 403-blocked host.

## 8. Licensing and reuse

**Copyright stays with the author.** SSRN: "You do not transfer copyright for any papers (or
other documents) you post on SSRN. When you upload a paper, you give SSRN the **non-exclusive
right** to post and distribute your paper. You retain the right to remove your paper from
SSRN at any time." (S6) [DOC]

**There is no default open licence.** Unlike [OSF Preprints](osf-preprints.md) (CC-BY or CC0,
enforced) or [Zenodo](zenodo.md), SSRN does not require or offer a standard Creative Commons
selection at deposit. The author's own rights position governs, and SSRN puts the burden of
verifying it on the author: "Each publisher has their own rights and self-archiving policies
regarding what version of your article you can make available … you should review your
publishing agreement, the publisher's copyright policies … prior to posting" (S6) [DOC]. SSRN
maintains a *Copyright Reference Guide* for this.

**Not everything is free to read.** "The vast majority of papers can be downloaded free of
charge as well. **The only exceptions are papers whose copyright is held by third parties
that request a download fee.**" (S6) [DOC] There are paywalled items in an "open access
research platform".

**Text and data mining is explicitly reserved.** Every SSRN page footer, 2026-09-01: "All
content on this site: Copyright © 2026 Elsevier Inc., its licensors, and contributors. **All
rights are reserved, including those for text and data mining, AI training, and similar
technologies.** For all open access content, the relevant licensing terms apply." (S2) [WEB]

Combined with §7, the position is unambiguous: **SSRN does not want you to mine it, says so
in the footer, blocks the attempt at the CDN, and bans the named AI crawlers in
`robots.txt`.** Treat everything in §2–§3 of this record as manually-obtained reference
figures, not as a licence to scrape.

## 9. Caveats and controversies

### 9.1 The Elsevier acquisition (May 2016)

SSRN was bought from Social Science Electronic Publishing Inc. by **Elsevier in May 2016**
(S10) [LIT]. Founder and chairman **Michael C. Jensen** wrote to the community on 17 May
2016, acknowledging the obvious objection in advance: "We realize that this change may create
some concerns about the intentions of a legacy publisher acquiring an open-access working
paper repository. **I shared this concern.** But after much discussion … I am convinced that
they would be good stewards of our mission." CEO **Gregg Gordon** wrote that users should feel
"assured that our ethos will remain intact" and that "existing and future SSRN content will
be largely unaffected" (S9, quoting both) [COM].

The **Authors Alliance** issued an 11-point list of principles it asked SSRN to adopt to
reassure users; SSRN "offered more general reassurances" but "would not commit to adopting
even one of our principles" (S9, quoting the Authors Alliance) [COM].

### 9.2 The July 2016 takedowns — the cautionary tale

**What happened.** In mid-July 2016, two months after the acquisition, Stephen E. Henderson
(Professor of Law, University of Oklahoma) found that a PDF he had uploaded to SSRN had been
removed. The revision comment read: *"It appears that you do not retain copyright to the
paper, and the PDF has been removed from public view. Please provide us with the copyright
holder's written permission to post. Alternatively, you may replace this version with a
working paper or preprint version, if you so desire."* (S9) [COM]

Henderson emailed a law-professor listserv — "It appears that the corporate takeover of SSRN
is already having a real impact" — the message was picked up by *PrawfsBlawg* and spread. Other
authors reported the same. Techdirt covered it under the headline *"Just As Open Competitor
To Elsevier's SSRN Launches, SSRN Accused Of Copyright Crackdown"* (S12) [COM].

**SSRN's response.** On Twitter, 15 July 2016: "To be clear, we haven't changed any policies
about copyright. A couple of processing emails were sent incorrectly and in the wrong order.
… There isn't some big conspiracy happening." Gordon's follow-up statement on Monday 18 July:
a staff member had reviewed Henderson's PDF and removed it **by mistake**; the paper was
reposted once SSRN was made aware. "Some have taken this mistake to suggest there has been a
copyright policy change resulting from our recent acquisition by Elsevier. This is not true …
While we worked to improve our compliance part of our submission process, we fell short in
thinking through the communications with the authors." Gordon estimated **about 20 papers**
were affected, out of a corpus then numbering more than 557,000 (S9) [COM].

**What followed.** Authors publicly deleted their SSRN accounts ("I am depublishing every
single article from #SSRN immediately"). Others migrated to the newly launched **SocArXiv**
— which is the same SocArXiv now holding 24,670 records on
[OSF Preprints](osf-preprints.md). The Authors Alliance told members "it may be time to leave
SSRN and adopt more author-friendly alternatives" (S9) [COM]. Henderson himself did not
withdraw his papers, but his verdict is the fairest summary anyone offered: "overall I believe
SSRN has done much good … Unfortunately, to date their actions often don't mirror those
words, as in this latest takedown craze" (S9) [COM].

**What it actually demonstrates — read carefully.** The strong version of the story (Elsevier
purged papers to protect journal revenue) is **not supported by the sources**; the contemporary
reporting supports a staff error affecting ~20 papers, compounded by bad automated emails
(S9) [COM]. The *real* lesson is structural and survives the debunking intact:

- **A commercial host has both the technical ability and the legal motivation to remove your
  paper unilaterally**, and it does not need a conspiracy to do so — a compliance workflow
  and an ordinary mistake are sufficient.
- **Authors found out by accident.** There was no notice; Henderson discovered it by checking
  a revision comment.
- **The reaction was disproportionate to the incident and proportionate to the risk.** Twenty
  papers is a rounding error; the *possibility* was what moved people, and moving to
  community-run infrastructure was the rational response.
- **SSRN's rights-clearance screen (§4) is exactly the mechanism that misfired.** The same
  policy that makes SSRN's screening better than its peers' is the one that removes papers.
  You cannot have one without the other.

Compare the failure modes across this collection: OSF Preprints' risk is **operator strategy
change** ([osf-preprints.md](osf-preprints.md) §4); CogPrints' risk was **founder retirement**
([library-science-and-cognitive-archives.md](library-science-and-cognitive-archives.md));
SSRN's risk is **rightsholder compliance under commercial ownership**. All three are real and
all three are different.

### 9.3 Other caveats

1. **Network paper counts must never be summed** (§3.2). The 68 networks total 4.57 M against
   ~1.5 M actual papers.
2. **Wikipedia lists SSRN's channels as separate repositories** and undercounts both by 20×
   (§3.3).
3. **Wikipedia's "more than 55 disciplines"** (S11) is stale — SSRN says 69, the selector
   shows 68 (§2).
4. **`papers.ssrn.com` cannot be reached by any script**, including via the DOI resolver
   (§7). Any pipeline that resolves SSRN DOIs will fail, and it will fail with a 403 that
   looks like an error in your code.
5. **No OAI-PMH, no bulk dump, no documented API** (§7.4). SSRN is absent from harvester-based
   discovery in a way that arXiv, EconStor and E-LIS are not.
6. **TDM and AI training rights are reserved in the footer** (§8).
7. **Papers can be removed by their authors in three clicks**, and some records are locked by
   the publisher rather than the author (§5).

## 10. Sources

- **S1** — SSRN homepage, `https://www.ssrn.com/index.cfm/en/`. Retrieved 2026-09-01 with a
  Chrome 131 User-Agent (default UA returns 403 — see §7). HTTP 200, 70,049 bytes. Supports:
  the "SSRN by the numbers" counters (1.5 M papers, 1.9 M authors, 300 M downloads, 47 M
  references, 2 M citations, 69 disciplines), the six top-level discipline groups, and the
  Economics/Medical/Computer Science network blurbs.
- **S2** — SSRN Computer Science Research Network landing page,
  `https://www.ssrn.com/index.cfm/en/compscirn/`. Retrieved 2026-09-01, HTTP 200, 27,393
  bytes. Supports: the 68-entry network selector (the exhaustive network list and slugs), the
  CompSciRN description, and the Elsevier copyright/TDM footer text.
- **S3** — SSRN internal statistics endpoint,
  `https://www.ssrn.com/rest/rn/statistics/<network-id>`, one call per network with ids
  scraped from each network landing page. Retrieved 2026-09-01. Supports: the entire
  68-network table in §3.2 (papers, authors, downloads).
- **S4** — SSRN internal content API, `https://api.ssrn.com/content/v1/bindings/<id>/papers`
  and `https://www.ssrn.com/rest/rn/subject-areas/<network-id>`. Retrieved 2026-09-01.
  Supports: the CS eJournal table and binding IDs, the engrn/isn/matscirn eJournal lists,
  the Lancet (25,561) and Cell Sneak Peek (12,414) totals, the sample CompSciRN record
  (abstract ID 7378338), and the bogus-binding negative control.
- **S5** — SSRN First Look `https://www.ssrn.com/index.cfm/en/first-look/`; Preprints with
  The Lancet `https://www.ssrn.com/index.cfm/en/the-lancet/`; Cell Press Sneak Peek
  `https://www.ssrn.com/index.cfm/en/cell-press-sneak-peek/`. All retrieved 2026-09-01,
  HTTP 200. Supports: the First Look participant list including Cell Press and The Lancet,
  the Lancet screening statement, the Cell Sneak Peek per-journal breakdown, and the on-page
  counters.
- **S6** — SSRN Support Center on Elsevier's support hub, `https://www.elsevier.support/ssrn`
  and the answer pages `/ssrn/answer/what-is-ssrn` (updated 2026-08-03),
  `/ssrn/answer/get-started` (2026-08-03), `/ssrn/answer/ssrn-review-process` (2026-07-20),
  `/ssrn/answer/copyright-policy` (2026-08-03), `/ssrn/answer/doi` (2026-08-03),
  `/ssrn/answer/is-ssrn-a-publisher` (2026-08-03), `/ssrn/answer/remove-my-paper`
  (2026-08-03), `/ssrn/answer/why-am-i-getting-a-firewall-alert` (2026-08-03), and the
  category `/ssrn/category/19203` ("Preprint Rejections"). All retrieved 2026-09-01.
  Supports: §4 in full, the DOI policy, the copyright/non-exclusive-licence position, the
  paper-removal mechanism, the "not a peer-reviewed journal" statement, and the
  metrics-for-tenure framing.
- **S7** — `https://www.ssrn.com/robots.txt` and `https://papers.ssrn.com/robots.txt`.
  Retrieved 2026-09-01, HTTP 200, 209 and 333 bytes. Supports: the GPTBot / ChatGPT-User /
  Google-Extended bans, `Crawl-Delay: 5`, and the sitemap URLs.
- **S8** — Access probes: `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7378338`
  against six user-agents; `https://papers.ssrn.com/oai`; `https://papers.ssrn.com/sol3/oai`;
  `https://www.ssrn.com/oai/request?verb=Identify`;
  `https://papers.ssrn.com/definitely-not-a-real-path-xyzzy`;
  `https://doi.org/10.2139/ssrn.7378338`; `https://api.ssrn.com/`. All 2026-09-01. Supports
  §7 in full, including the OAI-PMH absence and the soft-404 finding.
- **S9** — Carl Straumsheim, *"'There Isn't Some Big Conspiracy Happening'"*, **Inside Higher
  Ed**, 18–19 July 2016.
  `https://www.insidehighered.com/news/2016/07/19/social-science-research-network-confusion-leads-calls-boycott`
  Retrieved 2026-09-01 (HTTP 200 with default curl UA — no fallback needed). Supports: the
  Henderson takedown, the verbatim revision comment, SSRN's tweet and Gordon's statement,
  the "about 20 papers" figure, the **557,000 full-text papers** size anchor for July 2016,
  Jensen's and Gordon's acquisition-day statements, the Authors Alliance 11-point episode,
  and the author migration to SocArXiv.
- **S10** — Wikipedia, *Social Science Research Network*, wikitext via
  `https://en.wikipedia.org/w/index.php?title=Social_Science_Research_Network&action=raw`.
  Retrieved 2026-09-01. Supports: founding in 1994 by Michael C. Jensen and Wayne Marr, the
  May 2016 Elsevier acquisition, and the pointers to S9 and S12. [LIT — used as a citation
  index; the underlying primary sources were retrieved independently where possible.]
- **S11** — Wikipedia, *List of preprint repositories*, wikitext via
  `https://en.wikipedia.org/w/index.php?title=List_of_preprint_repositories&action=raw`.
  Retrieved 2026-09-01. Supports: the SSRN row (">1,000,000", "Aggregates over 30 preprint
  servers", "More than 55 disciplines", 1994, Elsevier) and the separate ">1,000" rows for
  *Preprints with The Lancet* (2018, Elsevier) and *Cell Sneak Peek* (2018, Cell
  Press/Elsevier).
- **S12** — Mike Masnick, *"Just As Open Competitor To Elsevier's SSRN Launches, SSRN Accused
  Of Copyright Crackdown"*, **Techdirt**, 18 July 2016.
  `https://www.techdirt.com/2016/07/18/just-as-open-competitor-to-elseviers-ssrn-launches-ssrn-accused-copyright-crackdown/`
  Retrieved 2026-09-01, HTTP 200 with default curl UA. Supports: contemporaneous community
  reaction to the takedowns. [COM]
