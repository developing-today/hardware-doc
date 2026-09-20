# ScienceOpen — preprint repository record

- **URL:** https://www.scienceopen.com/
- **Operator:** ScienceOpen, Inc. — headquarters Pappelallee 78–79, 10437 Berlin, Germany; technical
  office 131 Hartwell Ave., Suite 210, Lexington, MA 02421, USA (S1, S8). Co-founded 2013 by
  Alexander Grossmann (Leipzig Univ. of Applied Sciences, ex-De Gruyter) and Tibor Tscheke (Ovitas);
  the platform technology is provided by Ovitas (S8). Commercially funded by publisher services, not
  by grants or a university.
- **Discipline scope:** the *index* is all-discipline; the *hosted* content is a small,
  heterogeneous multidisciplinary trickle with a visible skew to applied/engineering and
  meta-research topics (§6).
- **Launched:** 2013 (beta November 2013, v1.0 May 2014) · **Status:** active
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What it is

**ScienceOpen is primarily a discovery and post-publication-review layer over other people's
content, with a small hosting operation bolted on.** It aggregates bibliographic records from
Crossref, PubMed, PubMed Central, arXiv, SciELO and hundreds of publisher feeds into a searchable
citation index, lets researchers curate those records into thematic *Collections*, and lets
qualifying researchers attach signed, DOI-bearing peer reviews to any record in the index.

Alongside that it operates three small first-party publication venues: **ScienceOpen Preprints**
(free), **ScienceOpen Posters** (free), and **ScienceOpen Research** (a journal; USD 400 to publish
after two positive reviews) (S3). Its commercial revenue comes from selling publishers and
institutions branded discovery, metadata enrichment, hosting and journal-publishing services (S8).

The homepage strapline is worth quoting because it is the source of most confusion about the
platform: *"100+ million Publications · 500+ Partner Journals · 1,000+ Research Collections"* (S1).

## 2. Scope and subject taxonomy

There is no arXiv-style category scheme for hosted content. Submissions are tagged with free-choice
disciplines and keywords by the author, and the search interface exposes a `preprint` filter plus
discipline and keyword facets applied across the whole aggregated index (S3).

The distinction that matters is not subject but **provenance**: search results mix (a) records
ScienceOpen hosts, (b) records it has ingested from publishers, and (c) preprints it has ingested
from other preprint servers. See §3.

## 3. Size and growth — critically evaluating the ">1,000,000" figure

**Wikipedia's *List of preprint repositories* gives ScienceOpen a size of ">1,000,000"** with the
description *"A research and discovery network allowing scholars with at least 5 publications to
freely review preprints"* (S9). The figure is **unsourced in that table**, and the current Wikipedia
*article* on ScienceOpen contains no such number (S8).

**That figure is wrong as a statement about hosted preprints, by roughly two orders of magnitude.**
The evidence:

| Measure | Value | Source |
|---|---|---|
| Records **indexed / aggregated** (homepage claim) | "100+ million Publications" | homepage, 2026-08-04 snapshot [WEB] (S1) |
| Records aggregated (operator, 2023) | "over 86 million research articles and records" | own peer-review guidelines [DOC] (S2) |
| Preprints **in the index** (operator, 2023) | "over 90 million records – **2 million of which are preprints**" — explicitly *"ScienceOpen aggregates preprints by integrating arXiv, BioRxiv, Preprints.org, PeerJ Preprints, ChemRxiv, and Open Science Framework repositories"* | own publish page [DOC] (S3) |
| DOIs **actually minted by ScienceOpen**, all 7 prefixes | **7,620** total (3,249 "current") | Crossref member 5403 [API] (S4) |
| Prefix 10.14293 (`posted-content` = **hosted preprints**) | **3,584** | Crossref [API] (S5) |
| Prefix 10.14293, conference papers (posters) | 1,118 | Crossref [API] (S5) |
| Prefix 10.14293, peer reviews | 893 | Crossref [API] (S5) |
| Prefix 10.14293, journal articles | 272 | Crossref [API] (S5) |
| *ScienceOpen Research* journal, works in OpenAlex | 143 (1,176 citations) | OpenAlex S2736351211 [API] (S6) |
| *ScienceOpen Posters*, works in OpenAlex | 16 | OpenAlex S2764464541 [API] (S6) |
| Records in Europe PMC (`PUBLISHER:"ScienceOpen"`) | 2,404 | Europe PMC [API] (S7) |

Full Crossref breakdown across all seven ScienceOpen prefixes (2026-09-01) (S5):
`10.14293` 6,994 · `10.58647` 311 (228 conference papers, 45 posted-content, 31 articles, 7 reports)
· `10.54081` 197 · `10.59081` 64 · `10.54947` 34 (books/chapters) · `10.47959` 14 · `10.55914` 7.

**Plain statement.** ScienceOpen hosts on the order of **3,600 original preprints** and under
**8,000 original objects of all kinds**. The million-plus and hundred-million figures describe an
*index of other people's records*, not a repository. Wikipedia's ">1,000,000" is not a hosting
figure, and citing it as one — as the repository-list table implicitly does — is misleading. The
correct comparator column value would be roughly **">3,500"**.

The operator is not being deceptive about this; its own 2023 publish page says outright that the two
million preprints are aggregated from arXiv, bioRxiv, Preprints.org, PeerJ, ChemRxiv and OSF (S3).
The conflation happens downstream.

**Growth is anaemic.** *ScienceOpen Research* has published 143 works since 2014, with per-year
counts of 61 (2014), 35 (2015), 16 (2016), 2, 0, 1, 3, 2, 3, 16 (2024), 1 (2025), 3 (2026) (S6). The
preprint stream is more active — 10 of the most recent `10.14293/pr2199.*` records were created
27–29 August 2026 (S10) — but the whole first-party operation remains tiny.

## 4. Screening and moderation — what gets in

**Preprints:** *"After submission your preprint will undergo an editorial review to check for
completeness and basic scholarly integrity in line with our general publication guidelines."* (S3)
Those General Publication Requirements (S11) cover COPE-aligned publication ethics, originality
("the same manuscript should not have been published elsewhere to avoid DOI duplication"),
authorship criteria, completeness (single PDF with all figures/tables embedded), reference
formatting, data citation, and SI units. **English is required for articles but explicitly not for
preprints** — *"Preprints in all languages are welcome."*

Explicitly: *"When a manuscript is submitted, it is initially checked only in terms of integrity, as
well as formal and ethical criteria. The public peer review process starts **after** the manuscript
has been approved by the editorial office and made public."* (S11)

**The "5 publications" review gate.** To post a peer review you must have **five records linked to
your ORCID**: *"To perform a peer review, all you need are 5 records associated with your ORCID to
demonstrate that you are an active and professional researcher."* … *"Reviewers are required to have
published at least five scientific manuscripts. To ensure that this condition is met, ScienceOpen has
partnered with the non-profit ORCID."* Exceptions are granted on request for early-career
researchers. Commenting (as opposed to reviewing) requires one or more items. (S2, S8)

Reviews are **signed, public, CC BY 4.0 licensed and Crossref-DOI'd**, and integrate with
ORCID/Publons/ImpactStory (S2).

**Volume reality check.** The same operator page that describes the gate states: *"At the moment we
have more than 86 million research articles and records on our platform… and we have more than 180
post-publication peer reviews to date."* (S2, page dated 26 June 2023). Crossref now records 893
peer-review DOIs under prefix 10.14293 (S5). Either way, the review network's throughput is
negligible relative to the index it sits on. Wikipedia's business-model section records a similar
audit: *"on 2022-08-01 ScienceOpen lists 115 reviews (with only 2 negative) and 77 publications"*
for ScienceOpen Research (S8).

## 5. Reliability — what you can and cannot trust

**What a ScienceOpen *preprint* deposit guarantees:** a Crossref DOI, CC BY 4.0, an editorial
completeness/integrity check, and inclusion in the platform's own index. Nothing about correctness.

**What a ScienceOpen *search result* guarantees: nothing at all about hosting.** The overwhelming
majority of what you see on ScienceOpen is ingested metadata for content hosted elsewhere. Always
resolve the DOI and see where it lands. A record surfacing "on ScienceOpen" is not published by
ScienceOpen.

**What a ScienceOpen *review* guarantees:** that the reviewer had ≥5 ORCID-linked records, signed
their name, and declared competing interests. That is a real, if low, bar — meaningfully better than
anonymous comment sections. But the sample is tiny (§4) and, per the Wikipedia audit, historically
almost never negative (S8) [COM].

**The commercial-collections question.** Collections are curated by volunteer Collection Editors from
the aggregated index and are free to create (S12). *Separately*, ScienceOpen sells publishers
"advanced indexing and promotional services that showcase customer content within the discovery
platform" (S8). So a record's prominence on the platform can reflect a paid promotional
relationship rather than merit. The platform does not, on the pages retrieved, distinguish promoted
from organic content in search results [NOT-VERIFIED as to current practice — the live search UI
could not be retrieved, see §8].

**The USD 400 step.** Publishing to *ScienceOpen Research* after ≥2 positive reviews costs
USD 400 (S3). That is an author-pays journal fee attached to a review process whose reviewers were
invited by the author. Wikipedia's summary of the workflow is blunt: *"the authors need to invite
potential reviewers … After having received at least 2 independent reviews with recommendation for
acceptance, the authors have an option to publish their work on ScienceOpen Research for 400 US$"*
(S8). Author-selected reviewers plus an author-paid publication step is a weak filter; the 115
reviews / 2 negative figure is consistent with that [INF].

### How to sanity-check an item from here

1. Resolve the DOI. Prefix `10.14293` (or `10.58647`, `10.54081`, `10.59081`, `10.54947`, `10.47959`,
   `10.55914`) = ScienceOpen-hosted. Anything else = indexed from elsewhere; go to the real host.
2. Check the object type at Crossref: `posted-content` (preprint), `conference-paper` (poster),
   `journal-article` (ScienceOpen Research), `peer-review`.
3. If reviews are attached, read them — they are signed and public, so they are checkable.
4. Do not treat the search index's coverage claims as a quality signal for any individual record.

## 6. What you actually find there — examples

Most recent hosted preprints, Crossref prefix `10.14293`, created 27–29 August 2026 (S10):

- *Edge-Enabled Autonomous UAV Systems for Disaster Management: Integrating Social…* — `10.14293/pr2199.004356.v1`
- *Advanced Social Drone Networks for Real-Time Disaster Monitoring, Damage Assessment…* — `10.14293/pr2199.004348.v1`
- *PubPeer Reviewing Its Critics: Questioning Qualification, Authority, Moderation…* — `10.14293/pr2199.004278.v1`
- *"Unlocking Pharma's Potential: The AI-aided NLP Revolution"* — `10.14293/pr2199.004344.v1`
- *Waste management as an integrated urban system: a comparative study of infrastructure…* — `10.14293/pr2199.004326.v1`

Computing/software items retrieved by bibliographic query (S13):

- *Quality Assessment of Scalable Software Systems in Production Environments* — `10.14293/pr2199.002759.v1` (2026)
- *Hybrid Quantum Algorithms and Quantum Software Development Frameworks* — `10.14293/pr2199.000298.v1` (2023)
- *Advancing Network Securing Strategies with Network Algorithms for Integrated Air Defense S…* — `10.14293/pr2199.000010.v1`/`.v2` (2023)
- *Minimizing The Number Of Tardy Jobs Algorithm* — `10.14293/pr2199.000488.v1` (2023)
- *AES Algorithm* — `10.14293/s2199-1006.1.sor-.ppoyrim.v1` (2020)
- *Parallelize DSW Algorithm* — `10.14293/s2199-1006.1.sor-.ppvowys.v1` (2019)
- *ADMINISTRATION SYSTEM FOR END TO END LUXURY APARTMENT MANAGEMENT SOFTWARE* — `10.14293/s2199-1006.1.sor-.ppr0hq1.v1` (2021)

**Honest quality read.** The computing content is student-project- to workshop-grade. Titles like
"AES Algorithm" and "Parallelize DSW Algorithm" are not the output of an active research community.
A systems or electronics engineer will find essentially nothing of professional value in
ScienceOpen's *hosted* corpus; the platform's utility, if any, is as a free federated search over
records you could also reach via Crossref, OpenAlex or Europe PMC.

## 7. Landmark papers

None. ScienceOpen hosts no landmark work in software, distributed systems, databases, electronics or
security, and the hosted corpus is too small and too junior for any to be plausible.

## 8. Access, APIs and bulk retrieval

- **The live site is behind a Cloudflare JavaScript challenge and could not be retrieved directly.**
  `https://www.scienceopen.com/` returned **HTTP 403** with a `Just a moment…` Cloudflare interstitial
  to *every* user agent tried on 2026-09-01: default `curl`, Chrome 131 desktop, `WhatsApp/2.23.20.0`,
  ChatGPT-User, ClaudeBot, and a Linux Chrome UA (S14). `sitemap.xml`, `api.scienceopen.com` and
  `blog.scienceopen.com` are likewise 403. Only `robots.txt` is served (200).
- **Everything in this record for the live site therefore comes from (a) the Wayback Machine
  snapshot of 2026-08-04 (S1), (b) archived `about.scienceopen.com` policy pages (S2, S3, S11, S12),
  and (c) third-party APIs (Crossref, OpenAlex, Europe PMC).** Per AGENTS.md rule 6, a successful
  archive retrieval is not evidence the live site is reachable for ordinary clients.
- **No public API found.** `api.scienceopen.com` is 403; no OAI-PMH endpoint is advertised. **No
  documented bulk dump.**
- **robots.txt** (retrievable, S15) advertises five sitemaps — `/sitemap.xml`, `/sitemap-index.xml`,
  `/sitemap-index-featured.xml`, `/sodocs_sitemap.xml`, `/soreviews_sitemap.xml` — all of which are
  themselves 403 to scripted clients. It sets `Crawl-delay: 10`, Cloudflare content signals
  `search=yes, ai-train=no, use=reference`, and `Disallow: /` for CCBot, ClaudeBot, GPTBot,
  Google-Extended, Applebot-Extended, Amazonbot, Bytespider, meta-externalagent, SemrushBot, PetalBot
  and Sogou. It also disallows `/review`, `/discussion`, `/advanced_search`, `/group(s)`,
  `/discipline` and `/external`.
- **Practical route for bulk work: Crossref member 5403** (all seven prefixes) — this is the only
  reliable machine-readable path to ScienceOpen-hosted content (S4).

### Negative controls (2026-09-01)

| Probe | Result | Interpretation |
|---|---|---|
| `https://www.scienceopen.com/about-scienceopen` (invented path) | **HTTP 404**, 18,968 B | Real 404s exist behind the challenge for some routes. |
| `https://www.scienceopen.com/` (valid path) | **HTTP 403**, 5,367–5,656 B, body = Cloudflare `Just a moment…` | A 403 here means *bot challenge*, not *absent*. |
| `https://api.scienceopen.com/`, `blog.scienceopen.com` | HTTP 403, ~5.6 kB Cloudflare page | Same challenge; existence unconfirmed [NOT-VERIFIED]. |
| Crossref prefix `10.14293` | 6,994 records | Independent confirmation the hosting operation is real and small. |

## 9. Licensing and reuse

- **Preprints, posters and journal articles: CC BY 4.0**, applied by the platform; authors retain
  copyright (S3).
- **Peer reviews: CC BY 4.0 with their own Crossref DOI** — reusable, citable, permanent records of
  reviewing activity (S2).
- Submission of preprints and posters is **free of charge**; only the *ScienceOpen Research* journal
  step costs USD 400 (S3).
- Text and data mining are permitted by licence but obstructed in practice by the Cloudflare
  challenge and by robots.txt `ai-train=no` (S15). Use Crossref.

## 10. Caveats and controversies

1. **The size figure is the headline problem.** Any statement that ScienceOpen "has over a million
   preprints" conflates an aggregated citation index with a repository. Hosted preprints ≈ 3,584
   (§3). Correct the record wherever you see it.
2. **Durability risk is material.** ScienceOpen, Inc. is a small commercial company; the hosted
   corpus is ~7,600 DOIs; the technology stack is supplied by a third party (Ovitas); and **no
   preservation arrangement (Portico, CLOCKSS, LOCKSS) is stated on any page retrieved**
   [NOT-VERIFIED — I looked at the publish page, the general publication requirements and the
   archived homepage and found none]. Contrast Preprints.org and Research Square, both of which
   state Portico archiving explicitly. If ScienceOpen ceases operations, the DOIs survive at
   Crossref but the content may not. **Do not treat this as an archival repository.**
3. **Commercial promotion inside the discovery layer.** Publishers pay for "promotional services that
   showcase customer content within the discovery platform" (S8). Prominence ≠ quality here.
4. **Author-invited reviewers plus a USD 400 publication step** is a structurally weak filter (§5).
5. **Bot-hostile.** The live site cannot be retrieved by scripted clients at all; this record depends
   on archives (§8). Anyone verifying claims here should expect the same obstruction.
6. **Wikipedia's article carries maintenance tags** for notability and citation quality dating to
   February 2016 (S8) — treat it as a weak source, which is exactly the problem with the ">1,000,000"
   table entry.

## 11. Sources

- **S1** — https://web.archive.org/web/20260804085502/https://www.scienceopen.com/ · Wayback snapshot
  of 2026-08-04, retrieved 2026-09-01 [WEB] · homepage: "100+ million Publications", "500+ Partner
  Journals", "1,000+ Research Collections"; ScienceOpen Preprints / Posters / Partner Journals
  product structure; Grossmann quotation; Berlin/Lexington addresses.
- **S2** — https://web.archive.org/web/20251204075650/https://about.scienceopen.com/peer-review-guidelines/
  · page dated 26 June 2023, snapshot 2025-12-04, retrieved 2026-09-01 [DOC] · the 5-ORCID-record
  review gate; ORCID moderation; CC BY + DOI on reviews; "more than 86 million research articles and
  records"; "more than 180 post-publication peer reviews to date"; reviewer checklist.
- **S3** — https://web.archive.org/web/20240128080242/https://about.scienceopen.com/publish/ · page
  dated 2 August 2023, snapshot 2024-01-28, retrieved 2026-09-01 [DOC] · free preprint/poster
  submission; CC BY 4.0 + Crossref DOI; two-step BASIC model; **USD 400** ScienceOpen Research fee
  after ≥2 positive reviews; *"over 90 million records – 2 million of which are preprints"* and the
  explicit list of aggregated sources (arXiv, bioRxiv, Preprints.org, PeerJ, ChemRxiv, OSF).
- **S4** — https://api.crossref.org/members?query=scienceopen · retrieved 2026-09-01 [API] · member
  5403 "ScienceOpen", prefixes 10.47959 · 10.14293 · 10.54947 · 10.55914 · 10.54081 · 10.58647 ·
  10.59081; total-dois 7,620; current-dois 3,249.
- **S5** — https://api.crossref.org/prefixes/{10.14293,10.47959,10.54947,10.55914,10.54081,10.58647,10.59081}/works?rows=0&facet=type-name:*
  · retrieved 2026-09-01 [API] · per-prefix totals and type breakdowns quoted in §3.
- **S6** — https://api.openalex.org/sources/S2736351211 and /S2764464541 · retrieved 2026-09-01 [API]
  · ScienceOpen Research 143 works / 1,176 citations / ISSN-L 2199-1006 / counts_by_year;
  ScienceOpen Posters 16 works.
- **S7** — https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=PUBLISHER:"ScienceOpen" ·
  retrieved 2026-09-01 [API] · hitCount 2,404.
- **S8** — https://en.wikipedia.org/wiki/ScienceOpen (wikitext via MediaWiki API) · retrieved
  2026-09-01 [COM] · founders, history, Ovitas technology, business model, promotional services, the
  5-publication gate, the "115 reviews (only 2 negative) and 77 publications" audit of 2022-08-01,
  Berlin/Lexington addresses, February 2016 notability and citation maintenance tags.
- **S9** — https://en.wikipedia.org/wiki/List_of_preprint_repositories (wikitext via MediaWiki API) ·
  retrieved 2026-09-01 [COM] · the ">1,000,000" row, unsourced, with the "at least 5 publications"
  description and 2013 launch year.
- **S10** — https://api.crossref.org/prefixes/10.14293/works?filter=type:posted-content&sort=created&order=desc
  · retrieved 2026-09-01 [API] · ten most recent hosted preprints with DOIs and creation dates.
- **S11** — https://web.archive.org/web/20240421184946/https://about.scienceopen.com/general-publication-requirements/
  · page dated 25 July 2019, snapshot 2024-04-21, retrieved 2026-09-01 [DOC] · editorial-office
  integrity/formal/ethical check before publication; COPE alignment; originality; completeness;
  "Preprints in all languages are welcome"; rejection/EoC/retraction reservation.
- **S12** — https://web.archive.org/web/20240128080245/https://about.scienceopen.com/collections/ ·
  page dated 26 June 2023, snapshot 2024-01-28, retrieved 2026-09-01 [DOC] · Collections model,
  Collection Editor role, "over 86 million articles and article records" available to add.
- **S13** — https://api.crossref.org/prefixes/10.14293/works?filter=type:posted-content&query.bibliographic=algorithm+software+network
  · retrieved 2026-09-01 [API] · the computing titles listed in §6.
- **S14** — user-agent matrix probe against https://www.scienceopen.com/ , 2026-09-01 [WEB] ·
  HTTP 403 with Cloudflare `Just a moment…` body for default curl, Chrome 131, WhatsApp/2.23.20.0,
  ChatGPT-User/1.0, ClaudeBot/1.0 and Linux Chrome 125 UAs.
- **S15** — https://www.scienceopen.com/robots.txt · retrieved 2026-09-01 [DOC] · the only
  scriptable-client-accessible resource on the domain; sitemap list, `Crawl-delay: 10`, Cloudflare
  content signals, per-agent blocks, disallowed paths.
