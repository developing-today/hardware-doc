# Research Square — preprint repository record

- **URL:** https://www.researchsquare.com/
- **Operator:** Research Square (a division of Research Square Company). Research Square Company was
  **fully acquired by Springer Nature**: *The Bookseller*, 1 December 2022 — *"After a period of
  partial ownership Springer Nature has increased its investment in Research Square Company (RSC) to
  take full ownership."* (S12). Research Square Company also owns **American Journal Experts (AJE)**,
  a paid author-services business (S6, S13). ISSN 2693-5015 (online) (S1).
- **Discipline scope:** advertised as multidisciplinary — *"physical, biomedical, and social
  sciences"* (S4) — in practice heavily biomedical/life-sciences, tracking the Springer Nature and
  BMC journal portfolio that feeds it.
- **Launched:** 2018 for the preprint platform (Springer Nature dates *In Review* to October 2018,
  S11; OpenAlex records first works in 2018, S9). Wikipedia's article says the *platform* was
  established 2013 and its repository-list row says 2018 — see §3. · **Status:** active
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What it is

Research Square is the largest preprint server in the world by deposit count, and it got there by a
mechanism no other server uses at scale: **it is plumbed directly into a major publisher's
manuscript-tracking systems.** When you submit to one of ~1,500 participating Springer Nature/BMC
journals, the submission form offers an opt-in called **In Review**. Tick it (with all co-authors'
agreement) and, once the journal's own quality checks pass, your manuscript is converted to HTML,
given a DOI, licensed CC BY 4.0, and posted publicly on Research Square with a live, updating
peer-review status timeline — *while it is still under review at the journal*. (S3, S11)

The rest of the site is a conventional direct-submission preprint server: upload a PDF/Word file,
staff screen it, it posts within ~72 hours (S4).

Around the preprint platform sits a commercial author-services business — AJE English editing,
translation, presubmission review, Rubriq independent peer review, video abstracts, research
promotion — all reachable from the preprint site's own navigation bar (S1, S13). That adjacency is
the source of the conflict-of-interest question in §10.

## 2. Scope and subject taxonomy

There is no formal, code-based taxonomy comparable to arXiv's. The home page advertises 15 "Featured
Subjects", all biomedical/behavioural: Anesthesiology & Pain Medicine, Cancer Biology, Computational
Biology, Dentistry, Developmental Biology, Epigenetics & Genomics, General Microbiology, Infectious
Diseases, Internal Medicine, Neurology, Oncology, Pediatrics, Physiology, Psychology, Structural
Biology (S1). Computer science and electronics appear only via the participating-journal list, not
as a promoted browse facet.

**Accepted content types** are explicitly restricted (S4, §1.2): Research Article, Systematic
Review, Method Article (incl. protocols), Short Report, Case Report, Data Note. And, importantly:
*"Only systematic reviews and research articles with complete methods and results sections will be
considered for posting. Theories, commentaries, and non-systematic reviews are not eligible for
preprinting."* Negative results are explicitly welcome.

**Where the CS/EE content comes in.** The *In Review* participating-journal list contains **1,503
journals and platforms** (extracted 2026-09-01, S5). Of those, ~134 have computing/electronics-facing
titles, including titles a systems or hardware engineer would recognise:

*Algorithmica* · *Distributed Computing* · *Acta Informatica* · *Cryptography and Communications* ·
*International Journal of Information Security* · *EURASIP Journal on Information Security* ·
*EURASIP Journal on Advances in Signal Processing* · *EURASIP Journal on Wireless Communications and
Networking* · *Design Automation for Embedded Systems* · *Analog Integrated Circuits and Signal
Processing* · *Automated Software Engineering* · *Innovations in Systems and Software Engineering* ·
*Cluster Computing* · *Computing and Software for Big Science* · *Computer Supported Cooperative Work
(CSCW)* · *Genetic Programming and Evolvable Machines* · *Information Retrieval Journal* ·
*GeoInformatica* · *Applied Network Science* · *EPJ Data Science* · *Autonomous Robots* ·
*International Journal of Machine Learning and Cybernetics* · *International Journal on Document
Analysis and Recognition (IJDAR)* · *Discover Computing* · *Discover Electronics* · *Discover
Networks* · *Discover Robotics* · *International Cybersecurity Law Review* (S5).

So: if a paper was submitted to *Algorithmica* or *Distributed Computing* and the authors opted in,
its preprint is on Research Square. That is a genuinely useful early-access channel for
theory/systems work.

## 3. Size and growth

| Measure | Value | Source |
|---|---|---|
| Preprints in the platform's own browse index | **468,390** | `/browse` `__NEXT_DATA__` `result.total`, 2026-09-01 [WEB] (S2) |
| Crossref DOIs under prefix 10.21203 | **514,618** (512,417 `posted-content` + 2,201 `component`) | Crossref API [API] (S8) |
| Works in OpenAlex source S4306525896 | 484,792 (281,027 citations) | OpenAlex API [API] (S9) |
| Records in Europe PMC (`PUBLISHER:"Research Square"`) | **470,988** | Europe PMC API [API] (S10) |
| Participating *In Review* journals/platforms | **1,503** | `/journals`, 2026-09-01 [WEB] (S5) |
| Manuscripts supported by AJE (parent company) | "over 775,000 … from researchers in 192 countries" | `/about` [DOC] (S6) |

**Conflicts, recorded.** Crossref's 514,618 exceeds the site's own 468,390 by ~46k; the most likely
explanation is version DOIs and `component` records, since Research Square mints a DOI per version
(`10.21203/rs.3.rs-XXXXXXXX/v1`) [INF]. Europe PMC's 470,988 is within 0.6% of the site counter,
which is a good independent corroboration. Wikipedia's *List of preprint repositories* row still says
">100,000" (access date 2023-05-22) and the article body says ">223,000 as of May 2023" (S14) — both
badly stale by a factor of 2–4.

**Launch-year conflict.** Wikipedia's article says the platform "was established in 2013"; its own
repository-list row says 2018 (S14). Springer Nature dates *In Review* to October 2018 (S11).
OpenAlex shows 147 works in 2018, then 11,360 in 2019 (S9). The 2013 date corresponds to Research
Square Company (the AJE parent), not the preprint platform [INF].

Growth by year (OpenAlex, S9): 2018 147 · 2019 11,360 · 2020 49,657 · 2021 74,421 · 2022 75,635 ·
2023 82,330 · 2024 73,144 · 2025 57,101 · 2026 (part year) 60,997. Peak deposit year was 2023;
volume has since declined ~30%.

Published versions **stay**, permanently: *"Once preprints receive a DOI, we cannot remove these
without cause"* (S3).

## 4. Screening and moderation — what gets in

Research Square screens; it does not review. From the Editorial Policies, §6 Screening (S4), verbatim
substance:

> *"Research Square does not conduct peer review on preprints prior to posting. Content submitted to
> Research Square is checked for appropriate ethics and consent statements; disclosure of competing
> interests; absence of patient identifiers; and inappropriate, alarming, highly controversial, or
> pseudoscientific claims. Articles with strong conclusions, especially in the absence of fully
> accessible data, may also be screened out. A submission that has already been published at a
> journal will not be posted as a preprint. Additionally, submissions with missing figures, reference
> lists, or other critical components may be rejected. … Checks at Research Square are carried out by
> our trained editorial staff."*

Two further points from the same policy:

- **In Review submissions carry the journal's checks *plus* the Research Square checks.** *"Preprints
  that are posted to the platform as part of the Springer Nature In Review service indicate the set of
  checks that have been carried out by the journal. They will include any checks the journal performs
  in addition to the above-mentioned Research Square checks."* (S4 §6)
- **Screening rejections cannot be appealed.** *"If we make a decision not to post a manuscript … due
  to concerns identified at the screening step … that decision cannot be appealed."* (S4 §11)

Data availability is a live screening criterion for medical work: *"We may decide not to post certain
preprints on the basis of unavailable or inaccessible data."* (S4 §4)

**Time to post:** direct submissions typically within 72 business hours (S4 §7). In Review preprints
post within **72 hours** of passing the journal's checks, or **48 hours** if the author elects to post
before review begins (journal branding then added later) (S3).

**Withdrawal and removal** (S4 §8, §9): withdrawal posts a *new version* explaining the withdrawal
while previous versions remain; removal is rare and replaces the text with a removal notice, keeping
title and authors "wherever possible". Research Square may itself initiate a withdrawal on research
conduct/ethics grounds or if a downstream journal version is retracted, and may attach **editorial
notes** to preprints at its discretion.

## 5. Reliability — what you can and cannot trust

### What the "In Review" badge actually tells you

This is the crux, and it is more informative than any other preprint badge in existence — *and also
more easily over-read*.

**It does tell you:**

1. The manuscript **was submitted to a specific named journal**, and that journal is identified on the
   preprint page.
2. It **passed that journal's submission/quality checks** — not peer review, the pre-review triage.
3. The status label is one of **Under Review**, **Under Revision**, or **Published** (S3).
4. If the journal shares the data, a **timestamped peer-review event timeline** is displayed, fed by a
   direct integration with the journal's manuscript-tracking system (S3).

A live example retrieved 2026-09-01 — *CMTD: Cascaded Multi-Token Disambiguation Model for Lip
Reading*, `10.21203/rs.3.rs-10510743/v1`, journal *Multimedia Systems*, status **Under Review** (S7):

```
First submitted to journal          28 Jul 2026
Submission checks completed         31 Jul 2026
Editor assigned by journal          21 Aug 2026
Reviewers invited by journal        25 Aug 2026
Reviewers agreed at journal         26 Aug 2026
Reviewers agreed at journal         27 Aug 2026
Reviews received at journal         29 Aug 2026
Reviews received at journal         30 Aug 2026
```

That is a genuinely valuable transparency artefact: you can see that two referees have reported.

**It does NOT tell you:**

1. **Anything about the reviews' content or verdict.** "Reviews received" ≠ "reviews positive."
2. **That the paper will be accepted.** The page carries the banner *"This is a preprint; it has not
   been peer reviewed by a journal."* (S7)
3. **That the journal is prestigious.** The 1,503-title list spans *Algorithmica* to
   *Zoomorphology*, including a large number of low-selectivity *Discover* and *BMC* titles (S5).
4. **That a timeline exists at all.** *"Journals can participate in In Review with varying levels of
   transparency … some journals opt to not share those details publicly on our preprints."* (S3)

### What happens on rejection — the important asymmetry

From the operator's own In Review page (S3), verbatim:

> *"If the submission is rejected by the journal, the preprint will remain on Research Square, with
> the journal branding and peer review timeline removed."*

Springer Nature states the same from the other side: the preprint *"will permanently remain publicly
available, regardless of whether the journal you submitted it to accepts it or not."* (S11)

**Consequence for a reader:** a Research Square preprint with **no** journal branding and **no**
timeline is ambiguous. It is either (a) a direct submission that never went through In Review, or
(b) an In Review manuscript that was **rejected** and had its branding stripped. **The page does not
distinguish these two cases.** This is the single most important reliability fact about the platform,
and it cuts against the naive reading that "no badge = ordinary preprint". You cannot tell a fresh
preprint from a rejected one.

### Other reliability observations

- **Post-hoc versions after rejection are gated.** New-version posting via the journal route is
  *"only available for manuscripts that are actively under consideration at an open access In Review
  journal"*; rejected authors must post revisions through their own account (S3).
- **Indexing is real:** Crossref, Europe PMC, Google Scholar, Researcher, Meta; PubMed Central
  indexes only a *"limited subset"* (S4 §10). Europe PMC's 470,988 records confirm the depth (S10).
- **No independent conversion-rate measurement found.** Research Square does not publish a
  preprint-to-publication rate, and I found no scientometric study measuring one specifically for
  this platform [NOT-VERIFIED]. Kirkham et al. (BMJ Open 2020) surveyed platform characteristics
  including Research Square but is now five years stale on size and policy (S15).

### How to sanity-check an individual paper from here

1. Read the **status** field and look for journal branding. No branding = unknown provenance (above).
2. If a timeline exists, read the *last* event, not the first.
3. Check whether a `nonDraftVersions[].status == "published"` version exists and follow it.
4. Check the DOI at Crossref; look for a `is-preprint-of` relation to a journal DOI.
5. Remember the content-type gate: theories and commentaries are *not* accepted (S4 §1.2), so a
   speculative essay here is anomalous.

## 6. What you actually find there — examples

Retrieved from `/browse` on 2026-09-01 (S2, S7):

| Title | URL | Journal / status |
|---|---|---|
| CMTD: Cascaded Multi-Token Disambiguation Model for Lip Reading | `/article/rs-10510743/v1` | *Multimedia Systems* · Under Review |
| Corrective Retrieval-Augmented Generation Adaptation in Closed Domains for Development… | `/article/rs-10574280/v1` | *Discover Artificial Intelligence* · Under Review |
| Auditing longitudinal data across institutional regimes: a graph-based compatibility protocol… | `/article/rs-10455680/v1` | Research Square (direct) · Posted |
| Inferential Analysis and Predictive Modeling of Wages in Brazil… | `/article/rs-10530787/v1` | Research Square (direct) · Posted |

DOI form is `10.21203/rs.3.rs-<id>/v<n>`, licence CC BY 4.0 (S7).

**Honest quality read.** The In Review-branded CS items are exactly what you would expect from the
mid-tier Springer computing portfolio: competent, incremental, benchmark-driven papers. The
unbranded direct submissions are a mixed bag and include material that reads as ambiguous in
provenance. The platform's centre of mass is biomedical, not computing.

## 7. Landmark papers (software · distributed systems · databases · electronics · security)

Research Square hosts no landmark work in these areas. It has existed only since 2018, its CS/EE
share is a small slice of a biomedical-dominated corpus, and the CS communities that would produce
landmark preprints use arXiv and IACR ePrint. No table.

## 8. Access, APIs and bulk retrieval

- **A JSON API exists but is gated.** The site's own API Access page (S16) states: *"We also provide
  a JSON API of the content on our platform with additional metadata if the Crossref or Europe PMC
  APIs do not satisfy your needs. Please fill out the below form to be granted an access token that
  will allow you to bypass our rate-limits."* There is no open, documented endpoint; access is by
  request form only.
- **The operator explicitly recommends Crossref or Europe PMC for bulk work.** *"Our preprints are
  also available at Europe PMC and Crossref under DOI prefix 10.21203. Researchers looking to analyze
  our preprints would be best served using one of those sources."* (S16) That is unusually helpful
  guidance and you should take it: prefix `10.21203` at Crossref (514,618 records) and
  `PUBLISHER:"Research Square"` at Europe PMC (470,988 records) (S8, S10).
- **No OAI-PMH endpoint found.** `/api`, `/api-access` return 404 (S17).
- **RSS:** `https://www.researchsquare.com/rss.xml` — HTTP 200, valid RSS 2.0 (S18).
- **Sitemap:** `https://www.researchsquare.com/sitemap.xml` — HTTP 200, 5,136 bytes (S17).
- **SSR payload:** `<script id="__NEXT_DATA__">` on `/browse` and `/article/...` carries structured
  metadata (total counts, licence, status, version list). Undocumented; may change [INF].
- **robots.txt** is Cloudflare-managed with content signals: `search=yes, ai-train=no, use=reference`,
  and explicit `Disallow: /` for Amazonbot, Applebot-Extended, Bytespider and others (S19). **A
  general-purpose crawl for AI training is expressly refused by the operator.**
- **No UA gating observed.** Default `curl` UA returned HTTP 200 on all pages tested (S17).

### Negative controls (2026-09-01) (S20)

| Probe | Result | Interpretation |
|---|---|---|
| `/article/rs-99999999/v1` | **HTTP 200**, 16,824 bytes | Soft 404 — non-existent id renders a stub page. |
| `/article/rs-10510743/v9` (real id, absent version) | **HTTP 200**, 16,824 bytes | Same stub. Byte-identical size to the bogus id, which is the tell. |
| `/browse?q=FPGA` , `/browse?subject=computer-science` | HTTP 200, `result.total` = **468,390** in every case | **Query parameters are ignored server-side.** Filtering is client-side only; the SSR total is always the global count. Do not scrape faceted counts from this site. |
| `/in-review`, `/editorial-policies`, `/help` | HTTP 404 (real, 5,028 B) | Correct 404s exist; the canonical paths are `/researchers/in-review` and `/legal/editorial`. |

## 9. Licensing and reuse

- **CC BY 4.0, mandatory, no author choice.** *"All preprints on the platform are published under a
  CC-BY 4.0 license."* (S4 §14). In Review requires all co-authors to agree to CC BY before posting
  (S3).
- Wikipedia flags a real downstream trap: if the manuscript was previously posted elsewhere under a
  more restrictive licence (e.g. CC BY-SA), re-posting it here under CC BY would violate the original
  licence (S14) — the burden is on the author.
- **Preservation:** *"Preprints are held in an archive run by Portico, who will post the full Research
  Square content repository in the event of the site ceasing to exist."* (S4 §13)
- Text/data mining is permitted by licence; the operator's robots.txt nonetheless signals `ai-train=no`
  (S19). Those are different instruments and they point in different directions — use the Crossref /
  Europe PMC mirrors, which is what the operator recommends anyway.

## 10. Caveats and controversies

1. **Publisher ownership is not disclosed on the preprint site.** Research Square Company is wholly
   owned by Springer Nature (S12). The word "Springer" appears **zero times** on the platform home
   page and zero times on the In Review page; it appears twice on the buried Editorial Policies page
   (as "the Springer Nature In Review service") (S1, S3, S4 — grep counts 2026-09-01). The `/about`
   page describes Research Square as *"a division of Research Square Company"* and a *"mission-driven
   business"* without naming the parent (S6). A reader assessing independence has to go and find that
   out.
2. **The conflict-of-interest structure, stated plainly.** One corporate group (a) publishes the
   journal, (b) runs the preprint server the manuscript is auto-posted to, and (c) sells the author
   paid English editing, translation, presubmission review, independent peer review (Rubriq), video
   abstracts and "research promotion" — with those services linked from the top navigation of the
   preprint site itself (S1, S13). AJE advertises that it is *"Nature's preferred provider of author
   services"* (S13). Nothing here is hidden or unlawful, and language editing is a legitimate need;
   but an author who opts into In Review at a Springer Nature journal is inside a single commercial
   funnel at every stage, and the preprint server has a commercial interest in that author becoming
   an AJE customer. **Disclose this if you rely on the platform in an assessment context.**
   *AJE list prices were not retrieved: the pricing page loads figures via JavaScript and rendered as
   "Loading…" to a plain HTTP client* [NOT-VERIFIED] (S13).
3. **The rejection-erasure asymmetry** (§5) — an unbranded preprint may be a rejected manuscript.
   This is the single most consequential caveat.
4. **Screening decisions are unappealable** (S4 §11).
5. **Wikipedia's size and launch-year figures are badly out of date** (§3) — do not propagate them.
6. **The browse endpoint ignores query parameters server-side** (§8) — a tooling trap that silently
   returns the global total.
7. **Editorial notes are at the operator's discretion**: *"Research Square maintains discretion over
   the content of the note"*, though authors are informed (S4 §9).

## 11. Sources

- **S1** — https://www.researchsquare.com/ · retrieved 2026-09-01 [WEB] · navigation (Browse, In
  Review, Journals, AJE Video Bytes, AJE Professional Editing, AJE Rubriq, API Access), 15 featured
  subjects, ISSN 2693-5015, "division of Research Square Company".
- **S2** — https://www.researchsquare.com/browse · retrieved 2026-09-01 [WEB] ·
  `props.pageProps.initialProps.result.total = 468390`; item records with `article_identity`,
  `journal_title`, `status`, `posted_at`, `url`.
- **S3** — https://www.researchsquare.com/researchers/in-review · retrieved 2026-09-01 [DOC] ·
  In Review mechanism, opt-in, CC BY, 72 h / 48 h posting, Under Review / Under Revision / Published
  statuses, **rejection behaviour**, versioning restriction, indexing, Portico.
- **S4** — https://www.researchsquare.com/legal/editorial · retrieved 2026-09-01 [DOC] · Editorial
  Policies §§1–15: content types, LLM authorship, screening criteria, time to post, withdrawal and
  removal, Research Square-initiated withdrawals and editorial notes, indexing, no-appeal rule,
  commenting policy, Portico archiving, CC BY 4.0.
- **S5** — https://www.researchsquare.com/journals · retrieved 2026-09-01 [WEB] · 1,503 participating
  journals/platforms extracted from the rendered list; CS/EE titles enumerated in §2. Full list saved
  to `scratch/preprint-repositories/contested/rs-journals-list.txt`.
- **S6** — https://www.researchsquare.com/about · retrieved 2026-09-01 [DOC] · "largest author
  services company, American Journal Experts (AJE)"; "over 775,000 manuscripts from researchers in
  192 countries".
- **S7** — https://www.researchsquare.com/article/rs-10510743/v1 · retrieved 2026-09-01 [WEB] ·
  live In Review example: banner text, DOI `10.21203/rs.3.rs-10510743/v1`, licence CC BY 4.0,
  status `under-review`, full peer-review event timeline quoted in §5.
- **S8** — https://api.crossref.org/prefixes/10.21203/works?rows=0&facet=type-name:* · retrieved
  2026-09-01 [API] · 514,618 total; 512,417 `posted-content`, 2,201 `component`.
- **S9** — https://api.openalex.org/sources/S4306525896 · retrieved 2026-09-01 [API] · 484,792 works,
  281,027 citations, counts_by_year 2018–2026.
- **S10** — https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=PUBLISHER:"Research Square"
  · retrieved 2026-09-01 [API] · hitCount 470,988.
- **S11** — https://www.springernature.com/gp/authors/campaigns/in-review · retrieved 2026-09-01
  [DOC] · Springer Nature's own In Review page: launched October 2018, "brought to you by our
  partners at Research Square", opt-in flow, and the permanence statement quoted in §5.
- **S12** — https://www.thebookseller.com/news/springer-nature-completes-acquisition-of-research-square-company
  · Brown L., *The Bookseller*, 1 December 2022 · retrieved 2026-09-01 [COM] · headline and lede
  visible without subscription: full ownership after partial ownership. Body behind a soft paywall.
- **S13** — https://www.aje.com/services/editing/ and https://www.aje.com/pricing/ · retrieved
  2026-09-01 [DOC] · AJE service tiers (Standard / Premium / VIP / Scientific Editing, translation,
  presubmission review, Rubriq, plagiarism check, Video Bytes); "We're also Nature's preferred
  provider of author services"; "1 million+ authors served in 192 countries". Prices render via JS
  and were not retrieved.
- **S14** — https://en.wikipedia.org/wiki/Research_Square and
  https://en.wikipedia.org/wiki/List_of_preprint_repositories (wikitext via MediaWiki API) ·
  retrieved 2026-09-01 [COM] · owner "Springer Nature", launch 2013 (article) vs 2018 (list),
  ">223,000 as of May 2023" and ">100,000" size claims, CC BY licence-conflict warning.
- **S15** — Kirkham JJ, Penfold NC, Murphy F, Boutron I, Ioannidis JP, Polka J, Moher D. *BMJ Open*
  2020;10:e041849 · https://doi.org/10.1136/bmjopen-2020-041849 · metadata retrieved 2026-09-01
  [LIT] · comparative survey of preprint-platform screening including Research Square.
- **S16** — https://www.researchsquare.com/request-api · retrieved 2026-09-01 [DOC] · token-gated
  JSON API; explicit recommendation to use Crossref prefix 10.21203 or Europe PMC for analysis.
- **S17** — path probes on www.researchsquare.com (`/api`, `/api-access`, `/in-review`,
  `/editorial-policies`, `/help`, `/sitemap.xml`) · 2026-09-01 [WEB] · 404/200 codes and byte sizes
  as tabulated.
- **S18** — https://www.researchsquare.com/rss.xml · probed 2026-09-01 [WEB] · HTTP 200, RSS 2.0,
  channel title "Preprints".
- **S19** — https://www.researchsquare.com/robots.txt · retrieved 2026-09-01 [DOC] · Cloudflare
  content signals `search=yes,ai-train=no,use=reference`; per-agent `Disallow: /` blocks.
- **S20** — negative-control probes, 2026-09-01 [WEB] · `/article/rs-99999999/v1` → 200/16,824 B;
  `/article/rs-10510743/v9` → 200/16,824 B; `/browse?q=…` → `total` unchanged at 468,390.
