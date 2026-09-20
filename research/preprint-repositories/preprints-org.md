# Preprints.org — preprint repository record

- **URL:** https://www.preprints.org/
- **Operator:** MDPI AG, Grosspeteranlage 5, 4052 Basel, Switzerland — the platform's own footer
  reads "Preprints.org is a free preprint server supported by MDPI in Basel, Switzerland" and the
  copyright line is "© 2026 MDPI (Basel, Switzerland)" (S1). Funded by MDPI; free to authors.
- **Discipline scope:** advertised as fully multidisciplinary (11 top-level subjects) — as actually
  used it is dominated by Biology/Life Sciences, Medicine and **Engineering**, with a genuinely
  large Computer Science & Mathematics section (S5).
- **Launched:** 2016 · **Status:** active (10 years; the site runs a "10th Anniversary" banner) (S1)
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What it is

Preprints.org is a general-purpose, all-fields preprint server launched by the open-access publisher
MDPI in 2016. It does what the mainstream servers do: you upload a PDF or Word/LaTeX manuscript, a
staff editor screens it within roughly a day, and it goes live under CC BY 4.0 with a Crossref DOI.
There are no fees. Content is archived with Portico. (S2, S3)

Two things make it structurally different from arXiv or TechRxiv. First, it is operated by a
commercial journal publisher rather than a university, library consortium or learned society, and it
is wired directly into that publisher's submission pipeline — you can tick a box during an MDPI
journal submission to also deposit the preprint, and there is a "Preprints Friendly Journals"
transfer service pointing outward from the server into (almost entirely) MDPI journals (S8). Second,
it runs a real screening step with published criteria, which is more than several larger servers do.

The practical consequence for an engineer is that Preprints.org is a big, fast, well-indexed
repository whose parent company carries a contested reputation. Those are separable questions and
§5 treats them separately.

## 2. Scope and subject taxonomy

Eleven top-level subjects, each with a subcategory list. The full taxonomy was extracted from the
server-rendered Nuxt payload of the subject pages on 2026-09-01 (S5, S6). The two branches a
systems/electronics engineer cares about:

**Computer Science and Mathematics** (subject id 71) — 22 subcategories:

| Subcategory | Subcategory |
|---|---|
| Algebra and Number Theory | Hardware and Architecture |
| Analysis | Information Systems |
| Applied Mathematics | Logic |
| Artificial Intelligence and Machine Learning | Mathematical and Computational Biology |
| Computational Mathematics | Mathematics |
| Computer Networks and Communications | Probability and Statistics |
| Computer Science | Robotics |
| Computer Vision and Graphics | Security Systems |
| Data Structures, Algorithms and Complexity | Signal Processing |
| Discrete Mathematics and Combinatorics | Software |
| Geometry and Topology | Other |

**Engineering** (subject id 94) — 19 subcategories: Aerospace; Architecture, Building and
Construction; Automotive; Bioengineering; Chemical; Civil; Control and Systems; **Electrical and
Electronic**; Energy and Fuel Technology; Industrial and Manufacturing; Marine; Mechanical;
Metallurgy and Metallurgical; Mining and Mineral Processing; Safety, Risk, Reliability and Quality;
**Telecommunications**; Textile; Transportation Science and Technology; Other. (S6)

There is also a **Chemistry and Materials Science** branch containing *Electronic, Optical and
Magnetic Materials*, *Nanotechnology*, *Ceramics and Composites* and *Metals, Alloys and Metallurgy*
— relevant if you are chasing device-materials work (S6).

Unlike arXiv there are no short category codes (`cs.DC`); subjects are addressed by slug, e.g.
`/subject/browse/computer-science-and-mathematics/hardware-and-architecture`.

## 3. Size and growth

The operator publishes a counter. All figures retrieved 2026-09-01.

| Measure | Value | Source |
|---|---|---|
| Preprints announced to date | **137,380** | statistics page [WEB] (S4) |
| Total downloads | 109,819,246 | statistics page [WEB] (S4) |
| Total views | 26,832,694 | statistics page [WEB] (S4) |
| Registered authors | 461,413 | home page [WEB] (S1) |
| Median hours to announcement | 25.65 h | statistics page [WEB] (S4) |
| Advisory board members | 322 | statistics page [WEB] (S4) |
| Records in the browse index | 126,194 | browse page Nuxt payload [WEB] (S5) |
| Crossref DOIs under prefix 10.20944 | **135,961** (100% type `posted-content`) | Crossref API [API] (S9) |
| Works in OpenAlex source S6309402219 | 135,032 | OpenAlex API [API] (S10) |
| Records in Europe PMC (`PUBLISHER:"Preprints"`) | 62,604 | Europe PMC API [API] (S11) |

**Conflicts, recorded rather than resolved.** The site's own headline count (137,380) exceeds the
count returned by its own browse index (126,194) by ~11,200 — Preprints.org does not explain the
difference and I did not verify a cause [NOT-VERIFIED]. Crossref sits between the two at 135,961,
which is consistent with the headline number minus a small registration lag. Wikipedia's *List of
preprint repositories* row says ">124,000" with an access date of 2026-03-19 (S12) — plausible for
that date given the growth rate, and now stale.

Per-subject totals (each retrieved individually from `/subject/browse/<slug>`, 2026-09-01) (S5):

| Subject | Preprints |
|---|---|
| Biology and Life Sciences | 24,867 |
| Medicine and Pharmacology | 22,428 |
| **Engineering** | **17,844** |
| **Computer Science and Mathematics** | **15,672** |
| Environmental and Earth Sciences | 9,382 |
| Chemistry and Materials Science | 8,949 |
| Physical Sciences | 7,154 |
| Public Health and Healthcare | 6,959 |
| Social Sciences | 6,780 |
| Business, Economics and Management | 5,167 |
| Arts and Humanities | 1,377 |

These sum to 126,579, marginally above the 126,194 browse total, i.e. a small number of preprints
carry more than one subject [INF].

Selected subcategory counts (2026-09-01) (S5): AI & Machine Learning 5,505; Electrical and Electronic
Engineering 3,147; Mechanical Engineering 2,137; Energy and Fuel Technology 1,630; Computer Science
1,431; Control and Systems Engineering 1,110; Industrial and Manufacturing 1,063; Information Systems
785; Computer Vision and Graphics 778; Computer Networks and Communications 527; Security Systems
451; Telecommunications 332; Software 279; Data Structures, Algorithms and Complexity 247; Robotics
247; Signal Processing 153; **Hardware and Architecture 77**.

Growth by year of record creation, from OpenAlex (S10): 2016 950 · 2017 2,124 · 2018 6,040 · 2019
3,886 · 2020 7,015 · 2021 7,857 · 2022 6,273 · 2023 21,776 · 2024 28,567 · 2025 31,468 · 2026 (part
year) 19,075. The step change in 2023 is stark and unexplained by the operator [NOT-VERIFIED as to
cause].

Published versions **stay**. Each new version receives a different DOI; if a journal version appears
later, Preprints.org links it from the preprint page rather than removing the preprint (S3).

## 4. Screening and moderation — what gets in

Preprints.org does screen, and publishes the criteria. This is the operator's own text.

From the About page (S2): *"All preprints undergo a short screening before being uploaded online…
Screening includes checks for basic scientific content, author background, and compliance with
ethical standards. It is carried out by the Preprints.org staff, with the support of active
researchers and the Preprints.org advisory board."*

From the Instructions for Authors, §Screening (S3), the manuscript is checked to ensure:

- the content is in English;
- it has not been previously published;
- it adheres to basic publishing ethics and international research-ethics regulation;
- the author has not made excessive submissions in a short period (*"excessive submissions within a
  short period may require justification and could be rejected"*);
- all authors are genuine scholars (*"submissions with fake names or email addresses may be
  rejected"*);
- conflicts of interest are disclosed;
- all figures, references and other critical components are present;
- **the content does not contain "harmful, provocative, controversial, or pseudoscientific
  statements"**, and manuscripts *"drawing strong conclusions without fully accessible supporting
  data may also be rejected"*;
- any AI use is disclosed and conforms to the COPE-aligned policy.

Preprints.org *"reserves the right to decline posting a preprint for reasons not explicitly stated
above"*, and screening *"typically takes 24 hours … by our trained editors"* (S3). Institutional
email addresses are recommended for author identification, and screeners are recruited from
"scholars with a track record of published and cited articles" (S2).

Editorials, discussion papers and coursework are *"typically"* not permitted; conference papers are
accepted only if unreviewed and DOI-less; abstracts are refused (S3).

Withdrawal is discretionary and narrow: misconduct, uncorrectable serious error, or serious reader
concern. Outright *removal* happens only under court order, illegality, privacy/legal risk, or
public danger (S3). A withdrawn preprint's DOI persists.

**Assessment.** This is a real gate — comparable in stringency to what Kirkham et al. (BMJ Open 2020)
found across biomedical preprint platforms, where screening ranged from none to full editorial
triage (S13). It is not peer review, and Preprints.org says so plainly: *"Content on Preprints.org
is not peer-reviewed"* (S2).

## 5. Reliability — what you can and cannot trust

### What a deposit here does and does not guarantee

**Does:** a timestamp; a Crossref DOI; a CC BY 4.0 licence; Portico archiving; passage through a
staff screen that checks language, ethics statements, author identity, completeness, and screens out
overt pseudoscience. **Does not:** any assessment of correctness, novelty, statistics, or
reproducibility.

### The operator's own conversion claim

The statistics page states a *"Rate of preprints converted to a peer reviewed article: 58.44%"*
(S4). Treat this as an **operator claim [DOC], not an independent measurement** — Preprints.org does
not publish the method, the denominator, the cohort window, or whether "peer reviewed article"
includes MDPI journals only. I found no independent scientometric replication of that figure
[NOT-VERIFIED].

### The MDPI question — stated fairly

MDPI's standing is genuinely contested, and the contest is documented on both sides.

**The criticisms.**

1. *Special-issue volume.* Paolo Crosetto (INRAE-GAEL) documented in 2021 that MDPI special issues
   grew from ~388 in 2013 to nearly 40,000 in 2021, ~500 per journal, and that at MDPI it is the
   *publisher* rather than the editorial board that solicits them (S14, via S15). Oviedo-García
   (2021) reported that in 2020 *Sustainability* ran 788 special issues, *Applied Sciences* 830 and
   *Materials* 846, with ~95% of MDPI journals publishing more than one special issue per week
   (S16, via S15). *Inside Higher Ed* reported 3,514 special issues with 2023 closing dates for
   *IJMS* alone (S17, via S15). The stated concern is whether peer review can be conducted
   effectively at that scale.
2. *The 2023 Clarivate delistings.* Clarivate discontinued Web of Science coverage of two MDPI
   journals — *International Journal of Environmental Research and Public Health* (IJERPH,
   effective 13 February 2023) and *Journal of Risk and Financial Management* (JRFM, effective 22
   February 2023) (S18). This sat inside a wider Clarivate purge: their SVP/Editor-in-Chief wrote
   that *"more than 500 journals were flagged"* at the start of 2023 and *"more than 50 … have
   subsequently been de-listed"*, spanning *"both major commercial publishing houses and smaller or
   society publishers"* (S19).

**MDPI's published responses.**

1. On the delistings, MDPI's own announcement (S18) states that Clarivate found both journals failed
   the **Content Relevance** criterion — *"highlighting publications that were deemed outside the
   scope of the journal, and not to do with quality of the publications"* — that MDPI *"formally
   appealed the decision to discontinue IJERPH"* on 31 March 2023, and that *"close to 90% of MDPI
   published content is going to be covered by the Web of Science Core Collection going forward."*
   Whether the IJERPH appeal succeeded is **[NOT-VERIFIED]** here.
2. On the Oviedo-García paper, MDPI's objections had editorial effect: *Research Evaluation* issued
   an **Expression of Concern** on the article in 2021 (doi 10.1093/reseval/rvab030) and a formal
   **Correction** in 2023 (doi 10.1093/reseval/rvad014) (S20, S21, S22). A reader weighing the
   "predatory" framing should note that the flagship paper making it was itself flagged and
   corrected.

### Does that reputation transfer to the preprint server?

**Mostly not, and it is important to be precise about why.** The criticisms above are about *journal
peer review at scale* — special-issue guest-editor quality, scope drift, reviewer load. A preprint
server performs none of those functions. Preprints.org states it does not peer review; nothing on it
carries a peer-review claim that could be inflated. On the specific axes that matter for a preprint
server — screening criteria, transparency of policy, DOI assignment, licensing, archiving — its
published policies (§4, §9) are unremarkable and in places stricter than peers'.

**Where the entanglement is real and should worry you** is the *funnel*, not the quality gate. See
§10.

### Known failure modes

- **Prolific single-author revision streams.** The Data Structures, Algorithms and Complexity listing
  on 2026-09-01 was topped by `10.20944/preprints202511.2197.v9` — a **ninth version** of the same
  claimed combinatorial-triangle-detection result (S23). Version churn on hard-open-problem-adjacent
  claims is a well-known preprint pathology and it is present here.
- **Soft 404s.** See §8 — the site returns HTTP 200 for non-existent manuscripts and non-existent
  subject slugs. Do not treat a 200 as proof a record exists.
- **No independent quality measurement.** I found no peer-reviewed scientometric study measuring
  retraction, error or paper-mill rates specific to Preprints.org [NOT-VERIFIED].

### How to sanity-check an individual paper from here

1. Check whether the article page links a peer-reviewed version; if yes, cite that instead.
2. Check the version number — `.v6`+ on a short paper is a warning sign.
3. Check the author's institutional email/ORCID presence (screening nominally requires this).
4. For CS/EE work, check whether the same authors also posted to arXiv; Preprints.org explicitly
   *recommends against* multi-server posting (S3), so a duplicate is worth a second look.
5. Verify claimed numbers independently. A screen for "harmful, provocative, controversial, or
   pseudoscientific statements" is not a screen for *wrong*.

## 6. What you actually find there — examples

Real records, retrieved 2026-09-01 from the Hardware and Architecture, Electrical and Electronic
Engineering, and Data Structures/Algorithms listings (S23):

**Hardware and architecture**

- *nSim-RV: A Configurable RISC-V Framework for Scheduler-Aware Timing-Scalability Evaluation* —
  `10.20944/preprints202606.0599.v1`
- *An Open-Hardware ML-KEM Polynomial Ring Accelerator on Chipyard RISC-V SoC: System-Level
  Integration…* — `10.20944/preprints202605.1405.v1`
- *TALOS: An Ultra-Efficient Area-Space 6G CryptoProcessor Leveraging Reusable Hardware Security
  Modules* — `10.20944/preprints202605.1914.v1`
- *Backlog Metastability in Windowed Quantum Error Correction Decoding* —
  `10.20944/preprints202608.1425.v2`

**Electrical and electronic engineering**

- *A Time-Multiplexed Q16.16 Fixed-Point Neural Network Accelerator for Resource-Efficient FPGA
  Inference* — `10.20944/preprints202608.2059.v1`
- *On Eddy Current Brakes with Anisotropic Material Structures: Electromagnetic Model and Its
  Detailed…* — `10.20944/preprints202608.2206.v1`

**Algorithms / complexity**

- *Parallel Repetition for Entangled Games with Gap Exponent Three* — `10.20944/preprints202608.0830.v1`
- *Hardness of Euclidean Closest Vector Within n^(1/8−ε) and Binary Near…* — `10.20944/preprints202608.0796.v1`
- *Reachable Globally Pareto-Efficient Allocations on Trees Are NP-Complete* — `10.20944/preprints202608.2133.v1`

**Honest quality read.** This is recognisable, ordinary engineering-conference-grade work — RISC-V
simulation frameworks, post-quantum accelerators, FPGA inference. It is *not* the venue where the
field's landmark results appear, and the complexity-theory items sit next to repeatedly-revised
open-problem claims. Treat it as a place to *find* work-in-progress from groups that publish in
MDPI's *Electronics*, *Sensors*, *Micromachines* and *Cryptography*, not as a source of record.

A revealing data point on what actually gets read: the server's own all-time top-5 most-viewed list
is four COVID-19 papers plus *"Raspberry PI for Kill Mosquitoes by Laser"* (02 August 2021, 133,692
views) (S4).

## 7. Landmark papers (software · distributed systems · databases · electronics · security)

Preprints.org hosts no landmark work in these areas. It began in 2016, long after the foundational
CS/EE literature was established, and its CS/EE deposits are overwhelmingly incremental applied
papers destined for mid-tier journals. No table.

## 8. Access, APIs and bulk retrieval

- **No OAI-PMH.** `/oai` and `/oai2` return HTTP 404 (2026-09-01) (S24).
- **No documented public REST API.** `/api` returns 404. The Nuxt SSR payload
  (`<script id="__NUXT_DATA__">`) on browse and subject pages is machine-parseable and is how the
  per-subject counts in §3 were obtained — undocumented and liable to change without notice [INF].
- **RSS:** `https://www.preprints.org/rss` returns HTTP 200, `application/rss+xml`, 127,714 bytes
  (S25).
- **Sitemaps:** `robots.txt` advertises `https://www.preprints.org/sitemap_index.xml`, which chains
  to `/__sitemap__/general.xml` and `/sitemap/index.xml`. `robots.txt` disallows `/search*` (S24).
- **Bulk metadata is best taken from Crossref** (prefix `10.20944`, 135,961 `posted-content`
  records) or OpenAlex (source `S6309402219`) rather than scraped (S9, S10).
- **User-agent gating is real.** As of 2026-09-01 `https://www.preprints.org/` returns **HTTP 403**
  (369-byte body) to `curl`'s default UA *and* to a normal desktop Chrome UA, but **HTTP 200** to
  `WhatsApp/2.23.20.0`. All retrievals here used the WhatsApp UA (S26). Per AGENTS.md rule 6, this
  does **not** mean the site works normally for ordinary clients.
- **Rate limiting is real.** Sequential subject-page requests without delay produced HTTP 429 after
  ~6 requests; ≥4 s spacing was needed (S5).

### Negative controls (2026-09-01) (S27)

| Probe | Result | Interpretation |
|---|---|---|
| `/subject/browse/engineering/quantum-basket-weaving-xyz` | **HTTP 200**, 570,854 bytes, `total = 17844` | Bogus subcategory silently falls back to the **parent Engineering listing**. A 200 proves nothing. |
| `/manuscript/999912.9999/v1` | **HTTP 200**, 289,595 bytes | Renders an empty article shell with `Posted: Invalid Date`, blank abstract, blank keywords. Soft 404. |
| `/help` | HTTP 404 (real) | Some routes do 404 correctly; behaviour is inconsistent. |
| `/subject/browse/computer-science-and-mathematics/hardware-and-architecture` | HTTP 200, `total = 77` | Valid path returns a distinct, plausible count. |

**Rule for this server: verify by DOI at Crossref, never by HTTP status.**

## 9. Licensing and reuse

- **CC BY 4.0, mandatory, no author choice.** *"All preprints are posted using an open access
  Creative Commons CC BY 4.0 license"* (S3). Authors grant Preprints.org "a perpetual, non-exclusive
  license to distribute."
- Authors retain copyright (S2).
- Text and data mining are therefore permitted by licence; the practical obstacle is the UA gating
  above, not the licence.
- **Preservation:** *"All preprints on Preprints.org are permanently archived at Portico"* (S3).
- Manuscripts appear first as PDF; full-text HTML *"typically becomes available within one week"*
  (S3).

## 10. Caveats and controversies

1. **The funnel is real and quantifiable.** The "Preprints Friendly Journals" page lists **232**
   journals offering direct manuscript transfer from Preprints.org. **230 of the 232 are MDPI
   journals** (`www.mdpi.com` URLs); the only two exceptions are `ahr-journal.org` and
   `revistaalergia.mx` (S8). The server also runs "MDPI Topics … offered to authors who want to
   submit to a MDPI journal after posting their paper" (S1), and the About page notes authors *"can
   also choose to submit their manuscripts to Preprints.org when submitting to any MDPI journal"*
   (S2). Depositing does not *oblige* you to submit to MDPI, but every affordance on the site points
   there. The CS/EE targets include *Electronics*, *Sensors*, *Algorithms*, *Cryptography*,
   *Computers*, *Micromachines*, *Drones*, *Journal of Low Power Electronics and Applications* and
   *Machine Learning and Knowledge Extraction* (S8).
2. **Parent-company reputation ≠ server reputation, but disclose the link.** If you cite a
   Preprints.org record in work that will be scrutinised, say who runs it. The MDPI controversies of
   §5 are about journal peer review, not preprint hosting, but a reader is entitled to know.
3. **The 58.44% conversion figure is unaudited** (§5).
4. **The 2023 volume step change** (7× year-on-year in OpenAlex counts) is undocumented by the
   operator (S10).
5. **Soft 404s make automated verification hazardous** (§8).
6. **Multi-posting is discouraged**, which slightly reduces the chance of finding an arXiv mirror to
   cross-check against (S3).
7. **Bot gating.** Retrieval required a non-standard UA (§8) — record this if you build tooling.

## 11. Sources

- **S1** — https://www.preprints.org/ · retrieved 2026-09-01 [WEB] · homepage: author count 461,413,
  "137K+ Total Preprints", MDPI footer, MDPI Topics, 10th Anniversary banner, top-of-page listings.
- **S2** — https://www.preprints.org/about · retrieved 2026-09-01 [DOC] · screening description,
  advisory board and screener roles, CC BY, Crossref DOI, "not peer-reviewed", MDPI address.
- **S3** — https://www.preprints.org/instructions-for-authors · retrieved 2026-09-01 [DOC] · full
  Screening criteria list, accepted article types, withdrawal/removal policy, versioning, Portico,
  CC BY licence grant, multi-posting recommendation.
- **S4** — https://www.preprints.org/statistics · retrieved 2026-09-01 [WEB] · 137,380 announced;
  109,819,246 downloads; 26,832,694 views; 25.65 h median to announcement; 58.44% conversion claim;
  322 advisory board members; all-time top-5 viewed list.
- **S5** — https://www.preprints.org/subject/browse and `/subject/browse/<subject>[/<subcat>]` ·
  retrieved 2026-09-01 [WEB] · per-subject and per-subcategory totals from the `__NUXT_DATA__`
  payload; browse total 126,194; HTTP 429 observed on rapid sequential requests.
- **S6** — https://www.preprints.org/subject · retrieved 2026-09-01 [WEB/DOC] · 11 top-level
  subjects; full subcategory tree with ids extracted from `__NUXT_DATA__`.
- **S8** — https://www.preprints.org/friendly-journals · retrieved 2026-09-01 [DOC] · 232 friendly
  journals, 230 on www.mdpi.com; per-journal impact factor / CiteScore / first-decision days.
- **S9** — https://api.crossref.org/prefixes/10.20944/works?rows=0&facet=type-name:* · retrieved
  2026-09-01 [API] · 135,961 works, all `posted-content`.
- **S10** — https://api.openalex.org/sources/S6309402219 · retrieved 2026-09-01 [API] · 135,032
  works; 279,413 citations; counts_by_year 2016–2026.
- **S11** — https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=PUBLISHER:"Preprints" ·
  retrieved 2026-09-01 [API] · hitCount 62,604.
- **S12** — https://en.wikipedia.org/wiki/List_of_preprint_repositories (wikitext via MediaWiki API)
  · retrieved 2026-09-01 [COM] · row: ">124,000", 2016, MDPI, access-date 2026-03-19.
- **S13** — Kirkham JJ, Penfold NC, Murphy F, Boutron I, Ioannidis JP, Polka J, Moher D.
  "Systematic examination of preprint platforms for use in the medical and biomedical sciences
  setting." *BMJ Open* 2020;10:e041849 · https://doi.org/10.1136/bmjopen-2020-041849 · metadata
  retrieved 2026-09-01 [LIT] · comparative survey of preprint-platform screening practice.
- **S14** — Crosetto P., blog analysis of MDPI special issues, April 2021, as cited and summarised in
  S15 [COM, secondary].
- **S15** — https://en.wikipedia.org/wiki/MDPI (wikitext via MediaWiki API) · retrieved 2026-09-01
  [COM] · "2023 Clarivate delistings" and "Proliferation of special issues" sections with citations.
- **S16** — Oviedo-García MÁ. "Journal citation reports and the definition of a predatory journal:
  The case of the Multidisciplinary Digital Publishing Institute (MDPI)." *Research Evaluation*
  2021 · https://doi.org/10.1093/reseval/rvab020 · metadata retrieved 2026-09-01 [LIT].
- **S17** — Grove J. "3,514 Special Issues a Year?" *Inside Higher Ed*, 15 March 2023, as cited in
  S15 [COM, secondary].
- **S18** — https://www.mdpi.com/about/announcements/5536 · "Clarivate Discontinues IJERPH and JRFM
  Coverage in Web of Science" · retrieved 2026-09-01 [DOC] · MDPI's own statement: dates 13/22
  February 2023, Content Relevance criterion, appeal filed 31 March 2023, "close to 90% of MDPI
  published content" still covered. Retrieved with UA `WhatsApp/2.23.20.0` (default and Chrome UAs
  return 403).
- **S19** — https://clarivate.com/blog/supporting-integrity-of-the-scholarly-record-our-commitment-to-curation-and-selectivity-in-the-web-of-science/
  · Quaderi N., Clarivate · retrieved 2026-09-01 [DOC] · ">500 journals flagged", ">50 de-listed",
  "<15% of journals pass our quality criteria". Does not name MDPI.
- **S20** — https://doi.org/10.1093/reseval/rvab030 · "Expression of concern: Journal citation
  reports and the definition of a predatory journal…" *Research Evaluation* 2021 · metadata
  retrieved 2026-09-01 [LIT].
- **S21** — https://doi.org/10.1093/reseval/rvad014 · "Correction to: …" *Research Evaluation* 2023 ·
  metadata retrieved 2026-09-01 [LIT].
- **S22** — https://api.openalex.org/works?search=MDPI+predatory+journal+citation+reports · retrieved
  2026-09-01 [API] · surfaced S16/S20/S21 and their citation counts (174 / 5 / 5).
- **S23** — https://www.preprints.org/subject/browse/computer-science-and-mathematics/hardware-and-architecture
  , `/…/data-structures-algorithms-and-complexity`, `/subject/browse/engineering/electrical-and-electronic-engineering`
  · retrieved 2026-09-01 [WEB] · titles and DOIs listed in §6; `…202511.2197.v9` observed.
- **S24** — https://www.preprints.org/robots.txt , `/oai` , `/oai2` , `/api` , `/sitemap_index.xml` ·
  probed 2026-09-01 [WEB] · 404s for OAI and API; sitemap chain; `Disallow: /search*`; sitemap
  generation timestamp `2026-09-01T21:39:04.761Z` confirms live retrieval.
- **S25** — https://www.preprints.org/rss · probed 2026-09-01 [WEB] · HTTP 200,
  `application/rss+xml`, 127,714 bytes.
- **S26** — UA matrix probe, 2026-09-01 [WEB] · `curl/8.5.0` → 403/369 B; Chrome 131 desktop UA →
  403/369 B; `WhatsApp/2.23.20.0` → 200/334,859 B; ChatGPT-User and ClaudeBot UAs → 403.
- **S27** — negative-control probes, 2026-09-01 [WEB] · bogus subcategory → 200 with parent total
  17,844; bogus manuscript id → 200 with "Invalid Date" shell.
