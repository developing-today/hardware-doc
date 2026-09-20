# Qeios — preprint repository record

- **URL:** https://www.qeios.com/
- **Operator:** Qeios (UK-based; ISSN 2632-3834, online). Commercially funded: free tier plus a
  **Pro** subscription at **USD 24.99/month** (S3). Editorial team chaired by Giorgio Bedogni
  (Bologna) with a managing/editorial board drawn largely from UCL and European institutions (S9).
- **Discipline scope:** multidisciplinary, organised by Scopus ASJC into four domains — Physical,
  Health, Social and Life Sciences (S2, S4). In practice heavily social/health-sciences and
  philosophy-of-science; a genuine but thin computing stream exists (§6).
- **Launched:** 2019 (Wikipedia's repository list and the platform's own Volume 1 = 2019; Crossref
  shows first DOIs registered September 2018) · **Status:** active
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What it is

Qeios inverts the usual order. You post a paper as a preprint within one business day; **peer review
happens afterwards, in public, under the reviewers' real names, with numeric scores**; and if the
paper accumulates enough positive reviews the author may *elect* to convert it into a "Version of
Record" carrying a **peer-approved** label. Editors never accept or reject: *"reviewers alone decide
on the validity of the papers"* (S9), and the editorial team's remit is limited to disputes and
misconduct.

Two features distinguish it from other open-review platforms. First, **AI is woven through the
pipeline** — for submission pre-checks, for identifying and inviting reviewers, for vetting the
identities and suitability of spontaneous reviewers, for grammar correction, and for the
language/best-practice checks that gate the peer-approved label (§4). Second, Qeios carries a huge
body of short **"Definitions"** — encyclopaedia-style entries, each with its own DOI — alongside
its research papers. Numerically the definitions *are* Qeios: they outnumber the research articles
roughly 25:1 (§3).

## 2. Scope and content types

Four Scopus ASJC domains and their fields; the browse interface offers **Computer Science**,
**Engineering**, **Mathematics**, **Chemical Engineering**, **Materials Science**, **Energy** and
**Physics and Astronomy** among 26 field filters (S5).

The archive exposes four object types (S6):

| Type | `?type=` value | Count (2026-09-01) |
|---|---|---|
| Definitions (wiki/encyclopaedia entries) | `definition` | **106,486** |
| Peer reviews | `peer_review` | **49,803** |
| Preprints | `article.preprint` | **3,979** |
| Peer-approved articles (Version of Record) | `article.peer_approved` | **392** |
| All articles | `article` | 4,372 |

Article sub-genres seen in the live archive include Research Article, Review Article, Commentary
(S6, S7).

## 3. Size and growth

| Measure | Value | Source |
|---|---|---|
| Qeios archive: definitions | 106,486 | own archive counter [WEB] (S6) |
| Qeios archive: peer reviews | 49,803 | own archive counter [WEB] (S6) |
| Qeios archive: preprints | 3,979 | own archive counter [WEB] (S6) |
| Qeios archive: peer-approved articles | 392 | own archive counter [WEB] (S6) |
| **Crossref DOIs, prefix 10.32388 — total** | **175,165** | Crossref API [API] (S8) |
|  · `Entry` (reference-entry = definitions) | 109,765 | Crossref [API] (S8) |
|  · `Peer Review` | 57,288 | Crossref [API] (S8) |
|  · `Posted Content` (preprints) | 6,111 | Crossref [API] (S8) |
|  · `Journal Article` | 2,000 | Crossref [API] (S8) |
| Works in OpenAlex source S4210177074 | 6,879 (28,061 citations) | OpenAlex [API] (S10) |
| Records in Europe PMC (`PUBLISHER:"Qeios"`) | 4,554 | Europe PMC [API] (S11) |
| Registered researchers (operator claim) | "100,000+" (was "90,000+" in Dec 2024) | own about page [DOC] (S2, S12) |
| Monthly readers (operator claim) | "200,000+" | own about page [DOC] (S2) |

**The number that matters.** Qeios's *research corpus* is roughly **8,100 objects** (6,111
preprints + 2,000 journal articles at Crossref), matching OpenAlex's 6,879 and Europe PMC's 4,554
within the usual coverage variation. **Everything else — 95% of Qeios's DOIs — is definitions and
reviews.** Wikipedia's repository-list row gives ">1000" for Qeios (S13); that is stale but, unlike
the ScienceOpen row, at least the right order of magnitude for the article corpus.

**Conflicts, recorded.** Qeios's own archive counts (4,371 articles, 106,486 definitions, 49,803
reviews = 160,660) are consistently below Crossref's (8,111 / 109,765 / 57,288 = 175,164). The most
likely cause is that the archive counts current versions while Crossref counts version DOIs [INF];
Qeios does not explain the gap [NOT-VERIFIED].

Growth by year (OpenAlex, articles only, S10): 2016 1 · 2018 16 · 2019 96 · 2020 157 · 2021 70 ·
2022 146 · **2023 1,852 · 2024 2,791 · 2025 1,323** · 2026 (part) 427. The 2023–24 surge and the
subsequent ~50% fall are both large and unexplained by the operator.

## 4. Screening, moderation and the peer-approval gate

**At submission (pre-posting).** *"Submit your paper, and we'll perform AI-assisted pre-checks for
non-scientific content and plagiarism. Your paper will be posted on Qeios as a preprint within 1
business day."* (S2) The ethics page elaborates: the custom AI *"assists with pre-checks at
submission to filter out non-scientific content and detect plagiarism"* (S9).

**Review invitation.** *"Our custom-built AI identifies potential reviewers among qualified
researchers with field expertise. Potential reviewers are contacted and invited to publicly review
the article."* Spontaneous reviewers may also self-select, but *"all identities and reviews undergo
an AI-assisted suitability check."* (S4) On the Pro plan, *"These experts provide over 98% of Qeios
reviews"* (S3) — i.e. the AI-driven Reviewer Recruitment Service is the dominant source of reviews,
and it is a **paid feature** after your first paper.

**The peer-approved gate.** A paper needs *"at least 4 peer reviews with average ratings of 3 out of
5 or higher for overall, clarity, and impact, and 2.5 or higher for novelty"*, after which the author
*may opt* to publish a Version of Record. That version *"has passed further AI-assisted checks for
language quality and adherence to field-specific best practices, such as the WMA Declaration of
Helsinki … and ARRIVE guidelines"* (S2, S4, S9).

**Continuous scrutiny.** If later reviews drag the overall average below 2.5/5, *"the paper will no
longer be considered peer-approved"* (S2, S9). This is a genuinely unusual and, on its face, a good
property: approval is revocable.

**Reviews are never anonymous**, carry 1–5 star ratings for overall/clarity/novelty/impact, require
a competing-interests declaration, get their own DOI and CC BY licence, and can themselves be
upvoted, downvoted and commented on (S4).

**Generative-AI authorship policy** (S4, last updated 2025-04-29): GenAI *"do[es] not qualify for
authorship and must not be listed as an author"*; language/readability use must be disclosed;
GenAI image creation/alteration is **not permitted** unless integral to the methodology.

### On "AI reviewers" — what is and is not verified

**Verified [DOC]:** Qeios uses custom AI to (a) pre-screen submissions for non-scientific content
and plagiarism, (b) identify and invite reviewers, (c) check the identity and suitability of
spontaneous reviewers and their reviews, (d) grammar-correct reviews (the API exposes a
`pre_grammar_correction_contents` field on review objects, S14), and (e) run language and
field-best-practice checks before granting the peer-approved label (S2, S3, S4, S9).

**NOT VERIFIED:** that Qeios publishes reviews *authored* by an AI. What I did to check:
(1) read the current publishing policy, about page and ethics page in full — all describe AI as
assisting reviewer *selection and vetting*, never as writing reviews (S2, S4, S9); (2) read the
archived 2023 about page — same (S15); (3) sampled **3,000 Crossref-registered Qeios peer-review
records** and inspected every author name: **all 3,000 had named human authors, none matching
`AI|GPT|Chat|Bot|Qeios|Artificial|Machine|Assistant|Anonymous`** (S16); (4) pulled a live review
object from the Qeios JSON API — signed by a named researcher with an institutional affiliation
(S14); (5) searched Mojeek for "Qeios AI-generated review", "Qeios review written by AI", "Qeios
artificial intelligence reviewer" — no substantive result (S17). **Anyone repeating the claim that
Qeios posts AI-written reviews should produce a source; I could not.** Note the endorsement Qeios
itself displays from Robert West (UCL): *"It uses AI to find and invite reviewers"* — find and
invite, not write (S12).

## 5. Reliability — what you can and cannot trust

**A Qeios *preprint* guarantees:** a DOI, CC BY 4.0, and passage through an automated
non-scientific-content/plagiarism screen within one business day. Nothing more.

**A Qeios *peer-approved* article guarantees:** ≥4 signed public reviews above stated numeric
thresholds, plus automated language/guideline checks. That is more transparent than a conventional
journal — you can read every review — but note the structural weaknesses:

1. **Reviewer supply is a paid product.** Pro ($24.99/mo) buys the Reviewer Recruitment Service that
   generates >98% of reviews (S3). Free-tier authors depend on spontaneous reviewers. An author who
   pays gets reviewed; an author who doesn't may not. This is not "reviewers are paid to be
   positive", but it does couple *review availability* to *payment*.
2. **No editor can reject.** By design (S9). The upside is no editorial bias; the downside is no
   backstop when four lenient reviewers all give 3/5.
3. **The threshold is low.** 3/5 average on overall/clarity/impact and 2.5/5 on novelty is a modest
   bar for a "Version of Record".
4. **"Median of 10 peer reviews … the most peer-reviewed publishing venue globally"** (S2, S9) is an
   **operator claim** with no published method or dataset [DOC, unaudited]. Crossref's ratio —
   57,288 reviews against 8,111 research objects — is consistent with a high *mean* (~7) but does
   not establish the median [INF].

### Documented incident: conflict with journal dual-submission rules

In December 2024, **Ethan Vishniac, Editor-in-Chief of *The Astrophysical Journal***, posted a
six-part public thread describing a case where an AAS journal referee reported being asked to review
the same manuscript elsewhere. The author had agreed to let Qeios post his preprint and solicit
reviews, *"the issue of peer review was never raised."* Vishniac's position: *"Qeios.com takes the
position that they are not a journal, but a website that vets papers through peer review. The AAS
journals (and as far as I know, all other professional journals) does not regard this as a meaningful
distinction."* AAS bans simultaneous submission *"in order to avoid over-burdening the community with
review requests and because we do not want to encourage people to shop for a referee."* (S18, quoted
in full by Peter Coles, S18)

Coles's own assessment: *"to all intents and purposes Qeios is a journal. It has an ISSN that says as
much too."* A commenter on that post points at Qeios's own wording: *"Once your paper secures at
least 4 peer reviews (…) you can opt to publish it as a regular journal article—known as the Version
of Record—on Qeios."* (S18)

**Practical consequence:** posting to Qeios and letting it recruit reviewers **while your paper is
under review elsewhere may put you in breach of the other journal's dual-submission rule**, and — as
Coles notes — some institutional research-integrity policies treat "artificially proliferating
publications" as misconduct. Qeios's own policy has a "Preprint Posting" section but the platform
does not, on the pages retrieved, warn authors about this specific collision [NOT-VERIFIED that no
such warning exists anywhere on the site].

### Low-quality content

The definitions corpus (106k+ entries) is encyclopaedia-style and not research. Among research
items, the archive shows the usual prolific-single-author pattern — e.g. two separate physics-adjacent
research articles by the same author posted on the same day, 2026-08-31 (S7). I found **no documented
retraction scandal or paper-mill incident specific to Qeios** [NOT-VERIFIED].

### How to sanity-check an item from here

1. Check whether it is `peer-approved` or a bare preprint. Bare preprint = screened by software only.
2. **Read the reviews.** They are signed, public, dated, scored and DOI'd — this is Qeios's genuine
   advantage. Check whether reviewers are in-field.
3. Check the review count and score spread, not just the label.
4. Check whether the same work is under review at a journal (see the incident above).
5. Distinguish `Definition` objects from research articles — they share the DOI prefix.

## 6. What you actually find there — examples

Computing/engineering preprints, retrieved via Crossref prefix `10.32388` (S19) and the live archive
(S7):

- *MVD: A Multi-Lingual Software Vulnerability Detection Framework* — `10.32388/4ahqy3` (2025-01-08)
- *A Generalized Space-Efficient Algorithm for Quantum Bit String Comparators* — `10.32388/nrq6w1` (2024-03-14)
- *Quantum Meets SAR: A Novel Range-Doppler Algorithm for Next-Gen Earth Observation* — `10.32388/8q5ow6` (2025-04-10)
- *New Adaptive Numerical Algorithm for Solving Partial Integro-Differential Equations* — `10.32388/r4546k` (2023-11-13)
- *Machine-Checked Bell-Violating Correlations with Deterministic Outcomes and Local Measurement Dynamics: A Lean 4 Formalisation* — live archive, 2026-08-31
- *Beyond Suspicion Scores: Competing-Explanation Inference for Fraud-Shaped Legitimate Activity* — live archive, 2026-08-31

Also present: *Review of: "Evaluating the Application of SOLID Principles in Modern A…"* —
`10.32388/kyv073` (2025-04-17), a signed software-engineering review with its own DOI (S20).

**Honest quality read.** A Crossref bibliographic query for *software / algorithm / network /
hardware / FPGA* across all Qeios preprints returns **63 records total** (S19). That is the size of
the computing corpus: essentially nothing. Alongside the credible items above sit things like
*"Research on Travel Route Planing Problem Based on Greedy Algorithm"* and *"The Algorithm; Mind of a
Virtual Era – Our Code of Codes"*. A systems or electronics engineer will not find a working corpus
here. What Qeios *is* useful for is reading open, signed peer reviews of individual papers — a
genuinely scarce resource.

## 7. Landmark papers

None in software, distributed systems, databases, electronics or security. The computing corpus is
~63 papers (§6).

## 8. Access, APIs and bulk retrieval

- **An undocumented but working public JSON API exists.** `https://www.qeios.com/api/publications/<QEIOS_ID>/published-reviews-of-any-versions`
  returns HTTP 200 `application/json` with the full review objects — body HTML, ratings
  (`borne_rating`, `borne_subrating_for_clarity|novelty|impact`), `declarations.coi`, DOI, view and
  download counts, author records with ORCID, and `pre_grammar_correction_contents` (S14).
  `https://www.qeios.com/api/notable-reviewer-users` also returns 200 with a paginated user list.
  There is **no published documentation, no stated rate limit, and no terms of use for the API** —
  treat it as unstable.
- **Archive faceting is a usable count API:** `https://www.qeios.com/archive?type=<value>` returns an
  "N items" figure. Valid values found by probing: `article`, `article.preprint`,
  `article.peer_approved`, `article.review`, `peer_review`, `definition`, `definition.definition`
  (S6).
- **No OAI-PMH.** `/api/publications`, `/api/stats`, `/api/search`, `/policies`, `/how-it-works` all
  404 (S6).
- **Bulk metadata: use Crossref prefix `10.32388`** (175,165 records, including 57,288 peer reviews
  with their own DOIs — an unusually rich open-review dataset) or OpenAlex source S4210177074
  (S8, S10).
- **Indexing:** the operator claims Europe PMC, Google Scholar and the NIH COVID-19 portfolio
  (S12); Europe PMC independently returns 4,554 records (S11).
- **No user-agent gating observed** — default `curl` returned HTTP 200 throughout (S6).

### Negative controls (2026-09-01)

| Probe | Result | Interpretation |
|---|---|---|
| `/api/publications/ZZZZZZ/published-reviews-of-any-versions` | **HTTP 404**, 6,603 B, `text/html` | Correct hard 404 — the API does not soft-fail. Good. |
| `/api/publications/0DHKFR/published-reviews-of-any-versions` | HTTP 200, 10,742 B, `application/json` | Valid id returns real JSON. |
| `/archive?type=bogus.type` | HTTP 200, **995 B**, no item count | Invalid facet returns a distinct 995-byte error body. |
| `/archive?type=review` | HTTP 200, **995 B**, no item count | Byte-identical to the bogus probe ⇒ `review` is *not* a valid facet value; the correct value is `peer_review`. **This is exactly why negative controls matter** — without the bogus probe, "no count" would have looked like "zero reviews". |
| `/archive?type=definition` | HTTP 200, 73,818 B, "106,486 items" | Valid facet. |

## 9. Licensing and reuse

- **CC BY 4.0 on everything** — articles, preprints, definitions and **peer reviews** (S4).
  Copyright stays with authors and reviewers; Qeios takes a reproduction licence only.
- **Data: CC0** under the Data Sharing policy (S4).
- Qeios is a Crossref member and a **DORA signatory** (S4).
- No paywalls, no registration required to read (S4).
- **Preservation: not established.** The publishing policy has an "Archiving and Preservation"
  section heading, but I did not retrieve its body text and found no named dark archive (Portico,
  CLOCKSS, LOCKSS) on any page retrieved [NOT-VERIFIED]. Contrast Preprints.org and Research Square,
  which both name Portico explicitly. **Treat durability as unproven.**

## 10. Caveats and controversies

1. **Qeios is mostly a dictionary.** 106,486 definitions vs ~4,400 articles. Do not infer research
   scale from headline DOI counts (§3).
2. **The dual-submission collision is real and documented** — see the Vishniac/AAS incident in §5.
   If your paper is under review at a professional-society journal, letting Qeios recruit reviewers
   may breach that journal's rules.
3. **Reviewer supply is coupled to a paid subscription** (>98% of reviews come from the Pro
   recruitment service) (S3).
4. **No editorial reject power** — by design, but it means the only filter is four reviewers'
   average scores at a low threshold.
5. **The "median of 10 reviews / most peer-reviewed venue globally" claim is unaudited** (§5).
6. **AI is pervasive in the pipeline; AI *authorship of reviews* is unverified** (§4). State the
   distinction accurately.
7. **Preservation arrangements unverified** (§9) — the highest durability risk of the five platforms
   in this cluster after ScienceOpen.
8. **The public API is undocumented** and may be withdrawn without notice (§8).

## 11. Sources

- **S1** — https://www.qeios.com/ · retrieved 2026-09-01 [WEB] · "Research you can trust", ISSN
  2632-3834, four-domain layout, indexing claim, "Over 100,000 researchers already use Qeios".
- **S2** — https://www.qeios.com/about · retrieved 2026-09-01 [DOC] · 100,000+/150+/200,000+ claims;
  three-step model (AI pre-checks → AI-invited reviewers → peer-approved in 4 weeks); the ≥4 reviews
  at ≥3/5 (≥2.5 novelty) threshold; revocable approval; "median of 10 peer reviews".
- **S3** — https://www.qeios.com/plans · retrieved 2026-09-01 [DOC] · Free vs **Pro USD 24.99/mo**;
  Reviewer Recruitment Service — *"These experts provide over 98% of Qeios reviews"*; unlimited
  revisions; grammar correction; cover images; social promotion.
- **S4** — https://www.qeios.com/publishing-policy · last updated 29 April 2025, retrieved 2026-09-01
  [DOC] · aims and scope (Scopus ASJC), CC BY 4.0 + CC0 data, DORA, Crossref, authorship, **Use of
  Generative AI**, competing interests, "How the Reviewing Process Works" (AI reviewer
  identification; AI-assisted suitability check on spontaneous reviewers), rating mechanics,
  evaluation standards, publication criteria and continuous scrutiny.
- **S5** — https://www.qeios.com/preprints · retrieved 2026-09-01 [WEB] · domain and field filters
  including Computer Science, Engineering, Mathematics, Materials Science, Energy.
- **S6** — https://www.qeios.com/archive and `?type=` facet probes · retrieved 2026-09-01 [WEB] ·
  counts for `definition` 106,486, `peer_review` 49,803, `article.preprint` 3,979,
  `article.peer_approved` 392, `article` 4,372, `article.review` 393; negative controls
  `bogus.type` and `review` both 995 B; 404s for `/policies`, `/how-it-works`, `/api/publications`,
  `/api/stats`, `/api/search`.
- **S7** — https://www.qeios.com/archive?type=article.preprint · retrieved 2026-09-01 [WEB] · live
  listing incl. the Lean 4 formalisation and fraud-inference items, and same-author same-day posting.
- **S8** — https://api.crossref.org/prefixes/10.32388/works?rows=0&facet=type-name:* · retrieved
  2026-09-01 [API] · 175,165 total; Entry 109,765 · Peer Review 57,288 · Posted Content 6,111 ·
  Journal Article 2,000 · Journal 1. Oldest records sampled: `10.32388/942977` ("Definition",
  created 2018-09-07).
- **S9** — https://www.qeios.com/ethics · retrieved 2026-09-01 [DOC] · separation of roles;
  continuous scrutiny; misconduct monitoring; the AI / reviewers / editorial-team triad and the
  explicit list of what the custom AI does.
- **S10** — https://api.openalex.org/sources/S4210177074 · retrieved 2026-09-01 [API] · 6,879 works,
  28,061 citations, ISSN-L 2632-3834, counts_by_year 2016–2026.
- **S11** — https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=PUBLISHER:"Qeios" ·
  retrieved 2026-09-01 [API] · hitCount 4,554.
- **S12** — https://web.archive.org/web/20241227174226/https://www.qeios.com/about · snapshot
  2024-12-27, retrieved 2026-09-01 [DOC] · "90,000+" researchers (vs 100,000+ now); identical
  three-step AI description; Robert West endorsement *"It uses AI to find and invite reviewers"*
  (also on the live home page, S1).
- **S13** — https://en.wikipedia.org/wiki/List_of_preprint_repositories (wikitext via MediaWiki API)
  · retrieved 2026-09-01 [COM] · Qeios row: ">1000", 2019, operator Qeios, cited to Coy P., *New
  York Times*, 28 January 2022.
- **S14** — https://www.qeios.com/api/publications/0DHKFR/published-reviews-of-any-versions ·
  retrieved 2026-09-01 [API] · full review object schema incl. `borne_rating`,
  `borne_subrating_for_*`, `declarations.coi`, `pre_grammar_correction_contents`, DOI
  `10.32388/6JWF94`, named human reviewer with ORCID and institution.
- **S15** — https://web.archive.org/web/20230206083212/https://www.qeios.com/about · snapshot
  2023-02-06, retrieved 2026-09-01 [DOC] · 2023-era manifesto and ethics statement referring to
  *"articles and definitions published on Qeios"*; editorial team list; no mention of AI-authored
  reviews.
- **S16** — https://api.crossref.org/prefixes/10.32388/works?filter=type:peer-review (cursor-paged,
  3,000 records sampled) · retrieved 2026-09-01 [API] · zero records without an author; zero author
  names matching AI/GPT/Chat/Bot/Qeios/Artificial/Machine/Assistant/Anonymous; top reviewers are
  named researchers (Changqing Sun 10, Robert West 8, Clive Bates 7…).
- **S17** — Mojeek searches for "Qeios AI-generated review ChatGPT", "Qeios review written by AI",
  "Qeios artificial intelligence reviewer" · 2026-09-01 [COM] · no substantive result. (DuckDuckGo
  HTML endpoint returned empty result sets to scripted clients on this date.)
- **S18** — https://telescoper.blog/2024/12/15/qeios-and-the-nature-of-a-journal/ · Coles P., "Qeios
  and the Nature of a Journal", 15 December 2024 · retrieved 2026-09-01 [COM] · reproduces in full
  the six-part Bluesky thread by Ethan Vishniac (@ethan-vishniac.bsky.social, 2024-12-06) quoted in
  §5, plus Coles's own analysis and a reader comment quoting Qeios's Version-of-Record wording.
- **S19** — https://api.crossref.org/prefixes/10.32388/works?filter=type:posted-content&query.bibliographic=software+algorithm+network+hardware+FPGA
  · retrieved 2026-09-01 [API] · **63 matching records total**; titles and DOIs listed in §6.
- **S20** — https://api.crossref.org/prefixes/10.32388/works?filter=type:peer-review (sample) ·
  retrieved 2026-09-01 [API] · e.g. `10.32388/kyv073`, *Review of: "Evaluating the Application of
  SOLID Principles in Modern A…"*, Abdul Qayum, 2025-04-17.
