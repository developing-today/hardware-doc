# engrXiv (Engineering Archive) — preprint repository record

- **URL:** https://engrxiv.org/ (OAI base `https://engrxiv.org/oai`)
- **Operator:** **Open Engineering Inc.** ("openENGR"), a US 501(c)(3) non-profit, which
  also operates *The Journal of Open Engineering* (S1, S7). Directed since launch by
  **Devin R. Berg**, professor of mechanical engineering, University of Wisconsin–Stout
  (S1). Funded by the "Engineering Archive Membership Circle" — institutional/library
  subscriptions at **$500/year** (S3).
- **Discipline scope:** *as advertised* — the broad spectrum of engineering disciplines
  (civil, mechanical, electrical, aerospace, materials, chemical, engineering education).
  *As actually used* — mechanical/civil/structural and applied-ML-in-engineering dominate;
  electrical/electronic content exists but is thin (§2, §6).
- **Launched:** **July 2016** (beta) (S1); earliest deposit dated **2016-07-27** (S5).
  **Status:** active.
- **Platform history:** OSF Preprints (Center for Open Science), 2016 → **19 January 2022**;
  self-hosted **PKP Open Preprint Systems** since (§1).
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What it is

engrXiv is a small, volunteer-moderated, community-run preprint server for engineering. It
was set up in 2016 by engineering academics and engineering librarians who wanted the
discipline to have the thing physics had had since 1991 and biology had just got. It is
explicitly modelled on arXiv — engrXiv states it uses the arXiv name **under trademark
licence from Cornell University**, and warns that the licence "should not be understood to
indicate endorsement of content on engrXiv by Cornell University or arXiv" (S1).

**The migration off OSF is confirmed and dated.** engrXiv originally ran on the Center for
Open Science's OSF Preprints platform (its legacy DOIs still read
`10.31224/osf.io/xjpcm`). The OSF provider record for `engrxiv` is *still live* and its
description field now reads, verbatim:

> "The Engineering Archive will be closed to new preprint submissions temporarily and moved
> to https://engrxiv.org/ beginning Wednesday, January 19th." — `allow_submissions: false` (S6)

The year is **2022**: 19 January 2022 was a Wednesday, and the new PKP instance reports an
OAI-PMH `earliestDatestamp` of **2022-01-21T14:36:57Z** (S5) — the moment the migrated
corpus was written into the new database. The current site runs **Open Preprint Systems
3.3.0.13** (from the `<meta name="generator">` tag, S2). The old OSF landing page
`https://osf.io/preprints/engrxiv/` still returns HTTP 200 but is a redirect target of the
`engrxiv.org` domain only in the API sense — the *domain* `engrxiv.org` now serves OPS
directly, not OSF (S2, S6).

**Reason for the move: [NOT-VERIFIED] in the operator's own words.** I could not retrieve a
statement from engrXiv explaining *why* they left OSF. The engrXiv blog index (S3) lists
posts from 2024–2025 only; older posts announcing the move were not reachable in this pass.
What is verifiable is that they moved to software they control (PKP OPS is open source and
self-hostable) and away from a platform whose preprint service COS has since de-emphasised
[INF]. Do not repeat a funding-crisis or platform-shutdown story without a source.

The corpus was **carried across, not abandoned**: the OPS instance holds records dated back
to 2016 with their original OSF-issued DOIs (§3).

## 2. Scope and subject taxonomy

engrXiv does **not** publish a compact category-code taxonomy the way arXiv does. Its
OAI-PMH `ListSets` exposes exactly two sets — `engrxiv` (Engineering Archive) and
`engrxiv:PRE` (Preprints) (S5) — so there is no machine-readable subject partition to
enumerate. Authors "select their own categories from our subject taxonomy" and moderators
check the choice is "plausible" (S1), but the taxonomy is not exposed via OAI.

What *is* exposed is free-text `dc:subject` keywords. Harvesting all 5,871 records
(2026-09-01, S5), the most common author keywords are:

| Keyword | Records | | Keyword | Records |
|---|---|---|---|---|
| machine learning | 211 | | sustainability | 35 |
| deep learning | 97 | | uncertainty quantification | 35 |
| artificial intelligence | 82 | | finite element analysis | 34 |
| additive manufacturing | 81 | | reinforcement learning | 32 |
| optimization | 53 | | internet of things | 32 |
| 3D printing | 50 | | structural health monitoring | 32 |
| simulation | 44 | | civil engineering | 31 |
| CFD | 42 | | mechanical engineering | 30 |
| renewable energy | 41 | | aerodynamics | 30 |
| robotics | 39 | | biomechanics | 29 |

**What the scope explicitly excludes** is as informative as what it includes. The stated
moderation policy rejects (S1):

- works claiming **free energy or perpetual motion**;
- works in **mathematics, theoretical physics, computer science, information technology or
  cybersecurity without a strong engineering connection**;
- work whose only "engineering" content is applying an LLM to something — "the application
  of AI or LLM tools to a particular situation does not necessarily constitute engineering."

So an engineer looking for `cs.AR`-style computer-architecture preprints is in the wrong
place by policy, not just by accident.

## 3. Size and growth

| Measure | Value | Date | Source |
|---|---|---|---|
| OAI-PMH `completeListSize` (all records, live server) | **5,871** | 2026-09-01 | [API] S5 |
| Crossref `prefixes/10.31224/works` total | 5,857 | 2026-09-01 | [API] S8 |
| Preprints remaining on the legacy OSF provider | 2,033 | 2026-09-01 | [API] S6 |
| OpenAlex source `EngrXiv (OSF Preprints)` `works_count` | **28** | 2026-09-01 | [API] S9 |

**Record the conflicts rather than resolving them.**

- *5,871 vs 5,857*: the Crossref `/prefixes/` endpoint filters by DOI-**owner** prefix, and
  it returned some records with `10.31235/...` (SocArXiv) DOIs — both prefixes belong to
  Crossref member 15934, Center for Open Science (S8). Every one of the 5,871 identifiers in
  the OAI dump does start with `10.31224` (S5), so **5,871 is the number to use** and the
  Crossref prefix figure should not be quoted for engrXiv.
- *2,033 on OSF*: this is the legacy corpus that COS still serves. It matches the pre-2022
  OAI records almost exactly (2016–2021 sums to 2,063, S5) [INF]. Content was **copied**,
  not moved — both copies exist, with the same DOIs.
- *OpenAlex 28*: OpenAlex's `EngrXiv (OSF Preprints)` source
  (`https://openalex.org/S4306401210`) records 28 works. That is a catastrophic
  under-count, presumably because OpenAlex still models engrXiv as an OSF sub-provider and
  never picked up the OPS instance (S9). **Do not use OpenAlex to size or search engrXiv.**

**Deposits by year** (from `dc:date` in the OAI harvest, S5):

| 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (to 09-01) |
|---|---|---|---|---|---|---|---|---|---|---|
| 38 | 112 | 227 | 409 | 657 | 620 | 447 | 497 | 635 | 1,151 | 1,078 |

**DOI syntax splits the corpus cleanly**: 2,111 records carry legacy
`10.31224/osf.io/XXXXX` DOIs and 3,760 carry OPS-era `10.31224/NNNN` DOIs (S5). Both
resolve (§8).

**Scale check against arXiv.** engrXiv's *entire lifetime output* is 5,871 items. arXiv's
electrical-engineering-and-systems-science categories alone, queried the same day (S10):

| arXiv category | Items |
|---|---|
| `eess.SY` (Systems and Control) | 47,937 |
| `eess.SP` (Signal Processing) | 41,815 |
| `cs.AR` (Hardware Architecture) | 8,932 |

**engrXiv is roughly one eighth the size of `eess.SY` alone, and smaller than `cs.AR`.**
Be blunt about this: for electrical, electronic, signal-processing, control or
computer-architecture work, arXiv is the primary venue and engrXiv is a distant secondary.
engrXiv's genuine constituency is the parts of engineering arXiv never absorbed — civil,
structural, mechanical, manufacturing, engineering education — where it is one of very few
options.

## 4. Screening and moderation — what gets in

engrXiv runs **pre-moderation by volunteer moderators**, and unusually for a small server it
publishes a detailed, honest policy (S1, S4). Quoting the substance:

- **Turnaround target:** "Subject to volume demands, we expect to review each paper
  submitted for moderation within 3 business days" (S1).
- **What moderation is not:** "We do not assess the quality of the work or verify copyright
  status… acceptance is not a statement about research quality or copyright status" (S1).
- **Grounds for acceptance:** scholarly content; in a supported research area; plausibly
  categorised; compliant with copyright law (author asserts rights at submission); in a
  language they can moderate (non-English submissions must carry an English title and
  abstract) (S1).
- **Rejection is appealable** to `director@engrxiv.org`, but "submissions may be rejected by
  the moderator for any reason" (S1).
- **Deposits are permanent.** The submission checklist requires the author to confirm: "I
  understand that once it has been posted publicly, my submission is permanent and cannot be
  withdrawn" (S4).

### The AI policy — the most substantive thing on this server

engrXiv publishes a detailed **AI Policy** (S11) that is worth reading in full if you care
about preprint hygiene anywhere. Acceptable LLM use: translation, literature search and
idea organisation *with human supervision*, copy-editing, machine-assisted data analysis,
dictation — all of which **must be disclosed**. Unacceptable: verbatim generated text, fake
data, LLMs as co-authors or as "interviewees", fabricated information to mislead
moderators, and "entire papers produced by AI generation with no human-generated components
beyond prompts." They also list explicit red flags — "unsubstantiated grand theories" with
"fanciful equations", "integration of multiple major theories into definitive new
'paradigms'… without substantive engagement", papers "written in many short sections, often
including bullet-point lists and numbered paragraphs" (S11).

**And they publish the consequences.** From the operator's own blog (S3):

- 2025-08-26, *The challenge of AI slop for preprint servers*: submissions grew "from an
  average of 60 submissions per month to closer to 200"; often from "so-called 'independent
  researchers' with no institutional affiliation… They may or may not be real people."
- 2025-12-31, *Wrap of 2025*: posted preprints rose "to nearly 1200, up from about 640 in
  2024"; "this has resulted in **roughly half of submissions being declined** as the
  moderation team has had to become more aggressive."

Those numbers **cross-check against the registry**: the OAI harvest gives 1,151 for 2025 and
635 for 2024 (S5) against the blog's "nearly 1200" and "about 640". The operator's public
statements and the machine-readable record agree — a good sign for this server's honesty
[INF].

## 5. Reliability — what you can and cannot trust

**A deposit guarantees:** a Crossref DOI, a datestamp, a permanent record (no withdrawal),
and that a human moderator glanced at it within a few days. That is all.

**It does not guarantee** peer review, correctness, or copyright cleanliness — the operator
says so explicitly (§4).

**Eventual-publication rate: [NOT-VERIFIED].** engrXiv's OAI `oai_dc` output carries no
`dc:relation` linking to a published version, and unlike TechRxiv, Crossref
`is-preprint-of` relations are not systematically populated for `10.31224` records. I found
no scientometric study measuring engrXiv's publication rate.

**Known failure modes, ranked by how much they should worry you:**

1. **Generative-AI slop is the dominant present risk**, on the operator's own account
   (§4) — half of 2025 submissions declined, and by implication some fraction of the
   accepted 1,151 slipped through. Deposits from 2025 onward warrant more scepticism than
   deposits from 2019.
2. **No withdrawal.** Bad or plagiarised work stays up.
3. **Author-chosen categories** with only a plausibility check.
4. **Citation gaming** — the operator names this as the *historic* spam motive: "attempts
   to artificially exploit Google Scholar indexing to make one's academic profile look more
   prestigious than is deserved" (S3).

**How to sanity-check an individual engrXiv paper.** Look at the deposit date (pre-2023 is
lower-risk); check whether the author has an institutional affiliation and an ORCID
(engrXiv names ORCID identity as a moderation criterion, S11); search the exact title for a
journal version; and read the reference list for hallucinated citations — the specific
failure mode engrXiv's own policy tells you to look for.

## 6. What you actually find there — examples

Titles verified present in the 2026-09-01 OAI harvest, with their DOIs (S5). This is a
deliberately hardware-leaning selection; it is *not* representative of the corpus, which is
mostly mechanical/civil.

- *A Review of Tunable Inductors for Power Electronics: Techniques and Applications*,
  2024-06-30 — `10.31224/3786`
- *Power Circuit AI: Designing Power Electronic Circuits for Motor Drives with Generative
  Artificial Intelligence*, 2026-04-02 — `10.31224/6706`
- *A Power and Area Efficient CMOS Bandgap Reference Circuit with an Integrated
  Voltage-Reference Branch*, 2019-08-08 — `10.31224/osf.io/4x9g8`
- *EMF Inspector: An Open-Source Physics-Based Electromagnetic Interference Estimation Tool
  for KiCad*, 2026-06-01 — `10.31224/7226` — a genuinely useful open-hardware EDA artifact
- *Dry Film Photoresist Application to a Printed Circuit Board (PCB) Using a Maskless
  Photolithography Process*, 2020-07-28 — `10.31224/osf.io/27f49`
- *Backscatter Ex-Nihilo: Single-component, Fully-passive Backscattering for
  Microcontrollers*, 2020-10-09 — `10.31224/osf.io/p57sr`
- *Modelling Gene-Protein-Reaction Associations on an FPGA*, 2019-06-03 —
  `10.31224/osf.io/u48bc`
- *Study of FPGA logic reconfiguration during operation*, 2022-10-20 — `10.31224/2632`
- *Reinforcement Learning based Intelligent Semiconductor Manufacturing Applied to Laser
  Annealing*, 2022-07-05 — `10.31224/2449`
- *Understanding Stability of Low-Inertia Systems*, 2019-02-18 — `10.31224/osf.io/jwzrq` —
  grid-stability work, one of the more-cited electrical items (19 Crossref citations, S8)
- *Fracture Toughness of Li\_xSi Alloys in Lithium Ion Battery*, 2019-04-15 —
  `10.31224/osf.io/zqadm`

**Hardware-adjacent keyword frequencies across all 5,871 titles** (S5), which is the
clearest statement of how thin the electronics layer is: `sensor` 95, `robot` 85,
`battery` 43, `circuit` 38, `embedded` 22, `antenna` 17, `FPGA` 11, `Arduino` 6, `PCB` 4,
`microcontroller` 4, `semiconductor` 4, `power electronic` 3, `inverter` 2, `Raspberry` 1.
Against that: `structural` 96, `concrete` 88, `finite element` 50, `additive manufactur` 43.

## 7. Landmark papers

**engrXiv hosts no landmark software, distributed-systems, database, electronics or
security papers.** No paper on this server changed a field. Its most-cited deposits (S8)
are a 2020 COVID X-ray CNN paper (`10.31224/osf.io/wx89s`, 55 Crossref citations), a
COVID computer-vision survey (`10.31224/osf.io/yt9sx`, 43), a deep-learning activation
function survey (`10.31224/2245`, 26), a cultured-meat techno-economic analysis
(`10.31224/osf.io/795su`, 23) and a material-point-method simulation paper
(`10.31224/osf.io/e24rb`, 23). Respectable, ordinary engineering literature; nothing
field-defining. The table this section normally carries is deleted.

## 8. Access, APIs and bulk retrieval

**Fully open and pleasant to script.** No Cloudflare challenge, no rate-limit encountered,
no user-agent games needed (a plain `curl` with a research UA worked throughout).

**OAI-PMH** — the primary bulk interface, base URL `https://engrxiv.org/oai`:

```bash
curl 'https://engrxiv.org/oai?verb=Identify'
curl 'https://engrxiv.org/oai?verb=ListSets'
curl 'https://engrxiv.org/oai?verb=ListRecords&metadataPrefix=oai_dc'   # then follow resumptionToken
```

`Identify` (2026-09-01, S5) reports: `repositoryName` **Engineering Archive**;
`adminEmail` `director@engrxiv.org`; `earliestDatestamp` **2022-01-21T14:36:57Z**;
`deletedRecord` **persistent**; `granularity` `YYYY-MM-DDThh:mm:ssZ`; gzip/deflate
compression supported. A full `ListRecords` harvest of 5,871 records completed in well
under a minute. Note the `dc:title` elements carry an `xml:lang` attribute — naive
`<dc:title>` regexes return nothing.

**HTTP probes and the negative control** (2026-09-01, S2):

| Path | Code | Bytes |
|---|---|---|
| `/` | 200 | 22,323 |
| `/about` | 200 | 17,815 |
| `/about/submissions` | 200 | 10,579 |
| `/preprints` | 200 | 42,575 |
| `/ai-policy` | 200 | 11,954 |
| `/oai?verb=Identify` | 200 | 1,887 |
| **`/definitely-not-a-real-page-zzz9999`** (negative control) | **404** | **22** |
| `/index/preprints` (plausible-looking but wrong) | 404 | 22 |

A 22-byte 404 body is unmistakable, so on this host HTTP status is trustworthy — unlike
osf.io (see the ECSarXiv record) or techrxiv.org.

**DOI resolution, both syntaxes, plus negative control** (S12):

| Probe | Result |
|---|---|
| `https://doi.org/10.31224/osf.io/xjpcm` (legacy) | 302 → `https://engrxiv.org/index.php/engrxiv/preprint/view/1` |
| `https://doi.org/10.31224/3786` (OPS-era) | 302 → `https://engrxiv.org/preprint/view/3786/version/5229` |
| **`https://doi.org/10.31224/9999999999`** | **404** |

Legacy OSF-issued DOIs survived the migration and now point at the OPS instance — a clean
result, and better than most platform migrations manage.

**Crossref** works too, with the owner-prefix caveat in §3:
`https://api.crossref.org/prefixes/10.31224/works?rows=1000&cursor=*`. Crossref records
show `publisher: Center for Open Science`, `member: 15934`, `group-title: engrXiv` (S8).

**OpenAlex is unusable here** — see §3.

## 9. Licensing and reuse

Authors choose. Licence URLs recorded in Crossref for a 3,000-record sample of prefix
`10.31224` (2026-09-01, S8):

| Licence | Records in sample |
|---|---|
| CC BY 4.0 (two URL spellings combined) | 2,023 |
| *(no licence recorded)* | 633 |
| CC0 1.0 | 212 |
| CC BY-NC 4.0 | 114 |
| CC BY-NC-ND 4.0 | 11 |
| CC BY-NC-SA 4.0 | 3 |

≈67% CC BY, but note that **21% of records carry no licence statement at all** [INF] — for
those, you have no reuse permission beyond fair dealing, whatever the site's general tone.

The author agreement grants engrXiv "the irrevocable, non-exclusive rights to reproduce,
publicly display and publish my article… in perpetuity" (S1, S4) — non-exclusive, so authors
retain the right to publish elsewhere, which is the whole point of a preprint server.

Text and data mining: not restricted by any robots directive encountered, and the OAI
endpoint is explicitly there for harvesting.

## 10. Caveats and controversies

- **It is small.** 5,871 lifetime deposits against ~48,000 in `eess.SY` alone (§3). Absence
  from engrXiv means nothing.
- **The corpus exists in two places** with the same DOIs — 5,871 records on OPS, 2,033 on
  OSF. Deduplicate if you aggregate.
- **Discovery infrastructure has not caught up**: OpenAlex sees 28 works (§3). If you build
  on third-party indexes you will silently miss this server.
- **Generative-AI submissions are an active, acknowledged crisis** (§4). The operator is
  candid and is tightening moderation, but volunteer capacity is the binding constraint —
  they explicitly say they are "looking to expand our volunteer moderation team in 2026" (S3).
- **Nothing can be withdrawn** (§4). A retracted-elsewhere paper stays on engrXiv.
- **Funding is thin**: $500/year institutional memberships (S3). This is a server that
  could disappear; archive anything you depend on.
- **The reason for the OSF exit is not documented here** (§1) — [NOT-VERIFIED].

## 11. Sources

- **S1** — `https://engrxiv.org/about` ("About the Server", including General Information,
  Purpose of Moderation, Moderation Policy, Moderation Procedure, Author Agreement, and the
  arXiv trademark-licence notice). Retrieved 2026-09-01. **[DOC]**
- **S2** — Live HTTP probes of `https://engrxiv.org/`: `/`, `/about`, `/about/submissions`,
  `/about/editorialTeam`, `/preprints`, `/search/search`, `/ai-policy`, `/announcement`,
  `/index/preprints`, `/oai?verb=Identify`, and the negative control
  `/definitely-not-a-real-page-zzz9999`. Includes the `<meta name="generator"
  content="Open Preprint Systems 3.3.0.13">` tag. Retrieved 2026-09-01. **[WEB]**
- **S3** — `https://blog.engrxiv.org/` — posts *Wrap of 2025* (2025-12-31) and *The
  challenge of AI slop for preprint servers* (2025-08-26). Retrieved 2026-09-01. **[DOC]** —
  supports the submission-rate figures, the ~50% decline rate, the $500 Membership Circle,
  and the citation-gaming remark.
- **S4** — `https://engrxiv.org/about/submissions` (Submission Preparation Checklist,
  Copyright Notice, Privacy Statement). Retrieved 2026-09-01. **[DOC]**
- **S5** — engrXiv OAI-PMH, `https://engrxiv.org/oai`: `verb=Identify`, `verb=ListSets`, and
  a complete `verb=ListRecords&metadataPrefix=oai_dc` harvest (5,871 records; dumped to
  scratch as `engrxiv_recs.json`). Retrieved 2026-09-01. **[API]** — supports the total,
  the per-year table, the DOI-syntax split, the keyword frequencies, the example titles and
  the `Identify` parameters.
- **S6** — OSF JSON:API: `https://api.osf.io/v2/providers/preprints/engrxiv/` (the migration
  notice in `description`, `allow_submissions: false`, `reviews_workflow: pre-moderation`,
  steering-committee list) and
  `https://api.osf.io/v2/preprints/?filter[provider]=engrxiv&meta[]=total` (`total: 2033`).
  Retrieved 2026-09-01. **[API]**
- **S7** — Wikipedia REST summary, `https://en.wikipedia.org/api/rest_v1/page/summary/EngrXiv`.
  Retrieved 2026-09-01. **[COM]** — supports "launched July 2016", the 2019 incorporation
  into Open Engineering Inc, and the Menomonie, Wisconsin base. (Wikipedia gives no size
  figure to conflict with §3.)
- **S8** — Crossref REST API: `https://api.crossref.org/prefixes/10.31224/works`
  (`rows=0&facet=…`; `sort=is-referenced-by-count`; a 3,000-record `select=DOI,license`
  sample) and `https://api.crossref.org/works/10.31224/osf.io/xjpcm`. Retrieved 2026-09-01.
  **[API]** — supports the 5,857 conflict, the owner-prefix contamination, the licence
  table, and the most-cited list.
- **S9** — `https://api.openalex.org/sources?filter=display_name.search:engrxiv` →
  `S4306401210`, `EngrXiv (OSF Preprints)`, `works_count: 28`. Retrieved 2026-09-01. **[API]**
- **S10** — arXiv API, `https://export.arxiv.org/api/query?search_query=cat:<cat>&max_results=1`,
  reading `<opensearch:totalResults>` for `eess.SY` (47,937), `eess.SP` (41,815),
  `cs.AR` (8,932). Retrieved 2026-09-01. **[API]** — note this endpoint only works over
  **https**; the `http://export.arxiv.org` form returned an unparseable response.
- **S11** — `https://engrxiv.org/ai-policy`. Retrieved 2026-09-01. **[DOC]**
- **S12** — `doi.org` HEAD probes: `10.31224/osf.io/xjpcm`, `10.31224/3786`, and the
  negative control `10.31224/9999999999` (404). Retrieved 2026-09-01. **[WEB]**
