# viXra — preprint repository record

- **URL:** https://vixra.org/ · mirror: http://rxiv.org/ · AI-assisted sibling: http://ai.vixra.org ·
  general sibling: https://rxiverse.org
- **Operator:** **Scientific God Inc.**, a New York not-for-profit 501(c)(3) corporation. viXra's own
  home page: *"As of October 1, 2019, viXra.org is owned and operated by Scientific God Inc."* (S1);
  Scientific God Inc.'s own announcement of 13 October 2019 confirms the transfer effective
  1 October 2019 and describes viXra as *"an ancillary project"* (S9). Founded July 2009 as a
  UK-based non-profit *"run by unpaid individuals"* (S6). Funded by donations.
- **Discipline scope:** advertised as all of *"Science, Mathematics & Other Scholarly Areas"* — in
  practice ~60% physics, with the physics dominated by relativity/cosmology, quantum foundations and
  "theories of everything" (§2, §3).
- **Launched:** 2009 · **Status:** active, still accepting submissions (most recent listings
  2026-08-31)
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

> **This record exists as a CONTROL CASE.** viXra is included here not because you should use it but
> because it shows, concretely and measurably, what a preprint server with essentially no filter
> looks like. Read it as a calibration point for the other records in this directory.
> **Do not cite viXra as evidence for anything.** See §5.

## 1. What it is

viXra ("arXiv" backwards) was created in July 2009 by the British physicist **Philip Gibbs** as an
explicit protest against arXiv's endorsement and moderation system. The founding argument is set out
on viXra's own *Why viXra?* page and is worth reading in the original because it is a coherent
position, not a crank manifesto (S3):

> *"In 2004 [arXiv moderation] was replaced by a system of endorsements … However many of us who had
> successfully submitted e-prints before then found that we were no longer able to. Even those with
> doctorates in physics and long histories of publication in scientific journals can no longer
> contribute to the arXiv unless they can find an endorser in a suitable research institution."*

> *"Some of us now feel that the time has come to start an alternative archive which will be open to
> the whole scientific community. That is why viXra has been created. viXra will be open to anybody
> for both reading and submitting articles. **We will not prevent anybody from submitting and will
> only reject articles in extreme cases of abuse, e.g. where the work may be vulgar, libellous,
> plagiaristic or dangerously misleading.**"*

And, critically, the founders said in advance what the consequence would be:

> *"It is inevitable that viXra will therefore contain e-prints that many scientists will consider
> clearly wrong and unscientific. However, it will also be a repository for new ideas that the
> scientific establishment is not currently willing to consider."* (S3)

That is the whole design. Everything in §5 follows from it.

## 2. Scope and subject taxonomy — including the computing categories

viXra uses seven broad groups and 38 categories, each with a short slug URL (`vixra.org/<slug>`).
Counts below are the **per-category totals published on viXra's own front page**, retrieved
2026-09-01 (S1). This is unusually good disclosure — few servers expose per-category counts this
plainly.

**Physics (26,503)** — `hep` High Energy Particle Physics 2,198 · `qgst` Quantum Gravity and String
Theory 2,299 · `relcos` Relativity and Cosmology 5,398 · `astro` Astrophysics 3,102 · `quant`
Quantum Physics 5,271 · `nucl` Nuclear and Atomic Physics 927 · `condmt` Condensed Matter 1,635 ·
`therm` Thermodynamics and Energy 472 · `class` Classical Physics 2,383 · `geop` Geophysics 360 ·
`clim` Climate Research 162 · `mathph` Mathematical Physics 1,659 · `histph` History and Philosophy
of Physics 637

**Mathematics (10,281)** — `setlog` Set Theory and Logic 363 · `numth` Number Theory 3,720 ·
`combgt` Combinatorics and Graph Theory 281 · `alg` Algebra 549 · `geom` Geometry 658 · `top`
Topology 198 · `anal` Functions and Analysis 680 · `stat` Statistics 379 · `math` General
Mathematics 3,453

**Computational Science (2,740)** — the categories this repository cares about:

| Category | Slug | Count | viXra's own scope note |
|---|---|---|---|
| **Digital Signal Processing** | `dsp` | **547** | *"including cryptography"* |
| **Data Structures and Algorithms** | `dsalg` | **500** | *"including software generation"* |
| **Artificial Intelligence** | `ai` | **1,693** | *"including Computational Linguistics"* |

There is **no hardware, electronics, networking, operating-systems, database or security category**.
Cryptography is folded into DSP; anything software-ish lands in `dsalg`.

**Biology (2,615)** — `bioch` 475 · `phbio` 1,493 · `mind` 406 · `qbio` 241
**Chemistry (436)** — `chem` 436
**Humanities (1,823)** — `arch` 77 · `ling` 275 · `econ` 401 · `soc` 768 · `reli` Religion and
Spiritualism 302 *"including mythology"*
**Academics (1,653)** — `edu` 262 · `sci` General Science and Philosophy 1,391

**Note the taxonomy itself.** A repository with a *Religion and Spiritualism* category sitting beside
*Data Structures and Algorithms*, operated by an organisation called Scientific God Inc., is telling
you what it is. That is not a gotcha — it is consistent with the stated mission (S6).

## 3. Size and growth

| Measure | Value | Source |
|---|---|---|
| **Total e-prints (operator counter)** | **46,051** | vixra.org front page, 2026-09-01 [WEB] (S1) |
| Works in OpenAlex source S2883122597 | 23,704 (12,172 citations) | OpenAlex [API] (S10) |
| Crossref DOIs | **none — viXra does not mint DOIs** | [INF] from §8 |
| ai.viXra.org (AI-assisted sibling, launched March 2025) | 1,815 | ai.vixra.org front page [WEB] (S7) |
| rxiVerse (sibling, launched July 2025) | 827 | rxiverse.org front page [WEB] (S8) |
| Not listed in Wikipedia's *List of preprint repositories* | — | [COM] (S11) |

**Conflicts, recorded.** OpenAlex holds 23,704 viXra works — about half the operator's count — and
its per-year figures show OpenAlex effectively **stopped ingesting viXra after 2021**: 2015 2,128 ·
2016 2,575 · 2017 2,779 · 2018 3,112 · 2019 3,071 · 2020 2,394 · **2021 1,446 · 2022 6 · 2023 8 ·
2024 16 · 2025 7 · 2026 22** (S10). OpenAlex does not explain the cut-off [NOT-VERIFIED as to
cause], but the effect is that viXra content has been largely **de-indexed from the main open
bibliographic infrastructure** since 2022. That is itself a strong signal about how the scholarly
record treats this server [INF].

viXra also does not appear in Wikipedia's *List of preprint repositories* at all (S11), despite
having its own Wikipedia article — another indication of how it is categorised by the community.

**Per-category monthly histories** are published on each category page. `dsalg` shows a long thin
stream: 1 submission in its first month (2009-08), a spike of 25 in 2014-05, and 1–11 per month
since; `dsp` shows 69 in 2012-08 and 42 in 2014-05 against a baseline of 1–15 (S12). These are
**tiny** categories — a few hundred documents accumulated over 17 years.

Versions: authors may replace a paper **up to four times**; further replacements require *"a good and
exceptional reason"*. Earlier versions are normally retained (S4).

## 4. Screening and moderation — what gets in

**There is no endorsement requirement, no affiliation requirement, no peer review, and no assessment
of correctness.** The operator says so repeatedly and unambiguously. From the *Info* page (S6):

> *"All scholarly papers in science, mathematics & other scholarly areas will be accepted. …
> Submissions are subject to screening for conformity with the guidelines of viXra.org and adherence
> to scholarly norms. Submissions may be rejected or withdrawn for being in the wrong format, not
> scholarly, or because of legal risks/concerns (e.g., threats, defamation, copyright violations or
> obscenities), **but they are not reviewed or rejected according to the correctness of the work.
> Because of this policy, viXra may contains some work of low value or usefulness.**"*

From the *Good practice* page (S5):

> *"viXra is a repository, not a journal so we do not review papers or give feedback. … Unlike
> journals, submissions to viXra are not reviewed or rejected according to the correctness of the
> work. … **This means that acceptance in viXra may not confer scientific credibility, or the lack of
> it, to your work or anyone else's.**"*

**What the gate actually consists of**, from the submission and good-practice pages (S4, S5, S6):

1. Format: PDF only, with title, full author name, abstract and body. No video, no source code, no
   Word/PowerPoint/LaTeX (may be rejected or converted).
2. Scholarly form: laid out as a scientific paper.
3. Legal: no plagiarism, defamation, obscenity, or **journal-formatted PDFs** — viXra *"sometimes
   proactively removes versions of documents that appear to show journal formatting"* to avoid
   take-down notices (S4).
4. No duplicate/near-duplicate resubmission (treated as replacements).
5. **AI-assisted work is routed elsewhere.** Since ~2025 the front page states: *"viXra.org only
   accepts scholarly articles written without AI assistance. Please go to ai.viXra.org to submit new
   scholarly article written with AI assistance or rxiVerse.org."* (S1) In practice viXra admins
   append a note to suspected records — e.g. `viXra:2604.0057` carries *"(Note by viXra Admin: Please
   submit article written with AI assistance to ai.viXra.org)"* (S13). This is a real, if crude,
   provenance signal, and it is more than most servers do.

Every abstract page carries a standing disclaimer (S13):

> *"Vixra.org is a pre-print repository rather than a journal. Articles hosted may not yet have been
> verified by peer-review and should be treated as preliminary. In particular, anything that appears
> to include financial or legal advice or proposed medical treatments should be treated with due
> caution."*

Comment moderation is enforced with an unusual rule: *"If you are being critical you must mention at
least one specific error, otherwise your comment will be deleted as unhelpful."* (S13)

## 5. Reliability — a blunt assessment

**A viXra deposit guarantees exactly three things: a timestamp, a stable URL, and a PDF that is
formatted like a paper.** It guarantees nothing about correctness, novelty, competence, or the
author's identity or existence. The operator states this himself in four separate places (§4).

**Do not cite viXra as evidence for anything.** Not as evidence a result is true, not as evidence a
result is novel, not as evidence a technique works. If a viXra paper contains something you need,
independently reproduce or verify the underlying claim and cite the verification. The only legitimate
citation of a viXra record is as a **priority timestamp** (this idea was public on this date) or as an
**object of study** (e.g. research about fringe science).

### How it is treated in the literature and the press

- **Nature News Blog** covered the launch in July 2009 under the headline *"What's arXiv spelled
  backwards? A new place to publish"*, and characterised viXra as accepting submissions *"without
  requiring authors to have an academic affiliation and without any threshold for quality"* (S14,
  cited via S2).
- **Collins, Bartlett & Reyes-Galindo, "Demarcating Fringe Science for Policy", *Perspectives on
  Science* 25(4):411–438 (2017), doi 10.1162/POSC_a_00248** — the standard science-studies treatment
  that uses viXra as a case in the demarcation problem (S15). 35 citations in OpenAlex.
- **Delfanti A., "Fake archives: The search for openness in scholarly communication platforms",
  ch. 20 in Biagioli & Lippman (eds), *Gaming the Metrics: Misconduct and Manipulation in Academic
  Research*, MIT Press 2020, pp. 261–269** (S16, cited via S2) — note the chapter title.
- **Yudhoatmojo S., De Cristofaro E., Blackburn J., "Understanding the Use of e-Prints on Reddit and
  4chan's Politically Incorrect Board", *Proceedings of the 15th ACM Web Science Conference 2023*,
  doi 10.1145/3578503.3583627** (S17) — a peer-reviewed CS-venue study of how arXiv and **viXra**
  e-prints circulate on Reddit and 4chan's /pol/. This is the most directly relevant scientometric
  work for a computing audience.
- Wikipedia's lead sentence, sourced to Collins et al. and two other refs, is: *"viXra is an
  electronic e-print archive known for unorthodox and fringe science."* (S2)

That is the settled perception: viXra is used in the literature as a **byword** for unfiltered
content, and it is the archive's own stated design that makes that fair.

### The minority of legitimate work — and it does exist

Being fair matters here. A real fraction of viXra content is ordinary, competent work by people
outside the endorsement system, or archival deposits of old material. Verified examples from the
computing categories (S12, S18):

- **`viXra:2607.0056` — "Inverse of the Square Wave Matrix"**, David J. Grabiner, Warren D. Smith,
  Sushanta Srivastava. The author comment reads: *"Based on At&T Bell Labs tech report we wrote in
  1989, now uploaded to VIXRA for archival purposes."* The abstract describes an O(N log N)
  signal↔square-wave transform analogous to the FFT. This is a genuine Bell Labs technical report
  being archived by its authors. **Warren D. Smith is a real computer scientist.** PDF verified: 84,174
  bytes, `%PDF-` magic bytes (S18).
- **`viXra:2607.0099` — "Linear-Time Algorithms to Color Topological Graphs"**, Warren D. Smith.
- **`viXra:2604.0005` — "Some Variations of the Secretary Problem"**, Sarthak Agrawal, Sanjeev Saxena.
- **`viXra:2601.0110` — "Synthetic Aperture Radar Point Target Response"**, Sasan Ardalan (26 pp);
  and `viXra:2512.0073` — "…Singular Value Decomposition (SVD) with Fixed Point CORDIC Operations
  with Application to MIMO-OFDM", same author (33 pp). Real DSP engineering.
- **`viXra:2601.0124` — "Notes on Automata Processing"**, Michael Leventhal, 306 pages.

**And the rest.** The same `dsp` listing also contains, from a single author, a sequence titled *"New
Wireless Technology not Covered by the Existing Ieee Standards of 2017"*, *"New Wireless Technology
for Data Transmission in Chemical Systems"* and *"The Use of Chemical System as Transmission Medium
in Wireless Data Communication Channel"* — 3–5 pages each. The `dsalg` listing includes *"Physical
OS: Genetic-Resilient Deterministic Phase-Coherence for Secure DTx and AGI Humanoid Safety
Interlocks"* and AI-flagged submissions (S12). Quantum-molecular-dynamics papers sit in the
*Data Structures and Algorithms* category.

**Honest summary of the computing categories.** ~2,740 documents across DSP, algorithms and AI,
accumulated over 17 years. Perhaps a low-single-digit percentage is archival or competent
independent work — the Smith/Grabiner and Ardalan items are real. The remainder ranges from
undergraduate-project quality to word-salad. There is **no** hardware, systems, networking or
database content of any kind. **The signal-to-noise ratio makes this useless as a search target for a
practising engineer**, and the sheer smallness of the categories means you would find nothing here
you could not find better elsewhere.

### How to sanity-check a viXra item (if you must)

1. Look up the author independently — DBLP, Google Scholar, ORCID, an institutional page. The
   Bell Labs example above passes; most do not.
2. Check whether the same work exists on arXiv, in a journal, or in a conference proceedings. If it
   does, cite *that*.
3. Check for the admin AI-assistance note in the Comments field.
4. Check the version count and the author's total submission count in the category.
5. **Then verify the actual claim from first principles.** There is no editorial filter standing
   between you and an error.

## 6. Landmark papers

**None.** viXra hosts no landmark work in any field, and specifically none in software, distributed
systems, databases, electronics or security. The most notable computing item is a 1989 AT&T Bell Labs
technical report deposited for archival purposes 37 years later (§5) — notable as provenance, not as
a landmark.

## 7. Access, APIs and bulk retrieval

- **No API. No OAI-PMH. No DOIs. No bulk dump.** viXra does not mint DOIs (nothing in Crossref) and
  advertises no machine interface.
- **RSS:** `http://viXra.org/feed/rss.xml` — HTTP 200, `application/xml`, 89,393 bytes, valid RSS
  2.0 with `<category>` per item. This is the only structured feed (S19).
- **Stable URL patterns** (all verified 2026-09-01, S18):
  - abstract page: `https://vixra.org/abs/YYMM.NNNN`
  - PDF: `https://vixra.org/pdf/YYMM.NNNNvV.pdf`
  - category listing: `https://vixra.org/<slug>` (e.g. `/dsalg`, `/dsp`, `/ai`)
  - policy pages: `/why`, `/submit`, `/practices`, `/info.html`, `/access`, `/faq.html`
- **Mirror:** `http://rxiv.org/` returns a byte-identical 10,486-byte home page (S20).
- **Submission is by web form only** (`fs23.formsite.com/viXra/form2/`); e-mail submission is
  explicitly no longer accepted (S4).
- **No user-agent gating and no rate limiting observed** — default `curl` returned HTTP 200
  throughout (S18).
- The `/access` page states flatly: *"We regret that we cannot make copies of papers available in any
  other shape or form. Nor can we send them to you in any other way including e-mail, FTP or the
  post."* (S21)

### Negative controls (2026-09-01) (S18)

| Probe | Result | Interpretation |
|---|---|---|
| `/abs/9999.0001` | **HTTP 404**, 746 B, `text/html` | Correct hard 404. |
| `/pdf/9999.0001v1.pdf` | **HTTP 404**, 746 B, `text/html` | Correct hard 404 — no fake PDF. |
| `/nosuchcategory` | **HTTP 404**, 746 B | Correct hard 404. |
| `/abs/2607.0056` (valid) | HTTP 200, 7,100 B | Real record. |
| `/pdf/2607.0056v1.pdf` (valid) | HTTP 200, **84,174 B**, `%PDF-` magic bytes | Real PDF, verified by magic bytes not status code. |

**viXra's HTTP behaviour is, ironically, the most honest of the five platforms in this cluster** —
static hosting, real 404s, no soft failures, no bot walls. Preprints.org and Research Square both
return HTTP 200 for non-existent records.

## 8. Licensing and reuse

- **No licence is applied.** viXra states no CC licence, no author licence grant, and no reuse terms
  on any page retrieved. Authors are simply responsible for their content: *"It is the authors'
  responsibility to ensure that they only upload content they have the legal right to share"* is the
  posture, and viXra "sometimes proactively removes" journal-formatted PDFs to avoid take-down
  notices (S4). [NOT-VERIFIED that any licence statement exists anywhere on the site.]
- **Practical consequence: default all-rights-reserved.** You cannot assume any right to
  redistribute, mine or reuse viXra content. This is materially worse than every other server in
  this cluster, all of which apply CC BY 4.0.
- **No preservation arrangement.** No Portico, CLOCKSS or LOCKSS statement exists on any page
  retrieved [NOT-VERIFIED]. The only redundancy is the `rxiv.org` mirror (S20), which is
  same-operator and therefore not an independent archive.
- **Durability risk: high.** A single small US non-profit, donation-funded, no DOIs, no dark archive,
  no licence permitting third-party mirroring. If Scientific God Inc. stops paying the hosting bill,
  46,051 documents disappear and nothing at Crossref or Portico points at them.

## 9. Caveats and controversies

1. **The Wikipedia "Scientific God Inc." provider claim is ACCURATE — verified against two primary
   sources.** Wikipedia's infobox lists `owner = Scientific God Inc.` (S2). viXra's own front page
   states: *"As of October 1, 2019, viXra.org is owned and operated by Scientific God Inc."* (S1).
   Scientific God Inc.'s own site carries a post dated 13 October 2019, *"viXra.org Is Now an
   Ancillary Project of Scientific God Inc."*, explaining that *"With EU legislation such as GDPR and
   upload filters becoming more restrictive, it was decided in 2019 to move viXra under the umbrella
   of a US-based non-profit organisation. Its ownership and operation was therefore transferred
   effective October 1, 2019 to Scientific God Inc."* SGI describes itself as *"a New York
   not-for-profit corporation with 501(c)(3) tax[-exempt status]"* (S9). Note that SGI is not a
   general-purpose scientific charity: its own navigation lists *Journal*, *SG Prize*, *Sciurch*,
   *Gcience*, *Scibible*, *Institute* — it publishes the *Scientific GOD Journal*, which viXra
   advertises on its front page (S1, S9).
2. **The founding grievance is worth taking seriously even if the archive is not.** arXiv's
   endorsement system does exclude unaffiliated researchers, and viXra's *Why viXra?* page makes that
   case with specifics (S3). The critique is legitimate; the remedy — removing the filter entirely —
   produced exactly the corpus its founders predicted it would (§1).
3. **AI content is now segregated but the boundary is porous.** viXra routes AI-assisted work to
   ai.viXra.org (1,815 e-prints) and rxiVerse (827), but detection is manual admin annotation, and
   AI-flagged items remain visible in viXra's own listings pending author action (S1, S7, S8, S13).
4. **OpenAlex has effectively de-indexed viXra since 2022** (§3). Whatever the reason, it means
   citation-graph tools will not see this content.
5. **viXra maintains a public list of journals that asked authors to remove papers from viXra**, with
   the advice *"You should therefore avoid these at all costs"* (S4). Treat that list as advocacy,
   not as an assessment of those journals.
6. **No licence, no DOIs, no dark archive** (§8). Anything you need from here should be saved
   locally, and if it is genuinely scarce, submitted to `web.archive.org/save/`.

## 10. Sources

- **S1** — https://vixra.org/ · retrieved 2026-09-01 [WEB] · total 46,051; all 38 per-category
  counts quoted in §2; Scientific God Inc. ownership statement; AI-routing notice to ai.viXra.org and
  rxiVerse.org; mirror `rxiv.org`; *Scientific GOD Inc.* advertisement banner.
- **S2** — https://en.wikipedia.org/wiki/ViXra (wikitext via MediaWiki API) · retrieved 2026-09-01
  [COM] · infobox `owner = Scientific God Inc.`, `founder = Philip Gibbs`, `launch_date = 2009`;
  lead sentence "known for unorthodox and fringe science"; seven-category description; references to
  Collins et al. 2017, the Nature News Blog piece and Delfanti 2020.
- **S3** — https://vixra.org/why · retrieved 2026-09-01 [DOC] · the founding argument against arXiv
  endorsement, and the "we will not prevent anybody from submitting" / "it is inevitable that viXra
  will contain e-prints that many scientists will consider clearly wrong" passages quoted in §1.
- **S4** — https://vixra.org/submit · retrieved 2026-09-01 [DOC] · PDF-only requirement, required
  metadata, four-replacement limit, journal-formatting removal policy, withdrawal form, no e-mail
  submission, list of journals that requested removals.
- **S5** — https://vixra.org/practices · retrieved 2026-09-01 [DOC] · "viXra is a repository, not a
  journal so we do not review papers"; "acceptance in viXra may not confer scientific credibility";
  no source code / video / file-sharing; replacement discipline.
- **S6** — https://vixra.org/info.html · retrieved 2026-09-01 [DOC] · founding rationale, 2009
  founding date, "All scholarly papers … will be accepted", the "not reviewed or rejected according
  to the correctness of the work … viXra may contains some work of low value or usefulness" passage.
- **S7** — http://ai.vixra.org · retrieved 2026-09-01 [WEB] · *"launched here in March, 2025 &
  accepts AI assisted scholarly articles"*; 1,815 e-prints; computational-science counts DSP 7,
  Data Structures and Algorithms 30, AI 120.
- **S8** — https://rxiverse.org · retrieved 2026-09-01 [WEB] · *"launched here in July, 2025"*;
  827 e-prints; same category structure; operated by Scientific God Inc.
- **S9** — https://scigod.org · retrieved 2026-09-01 [DOC] · post of 13 October 2019, *"viXra.org Is
  Now an Ancillary Project of Scientific God Inc."*, with the GDPR rationale and the effective date
  of 1 October 2019; "Scientific GOD, Inc. ('SGI') is a New York not-for-profit corporation with
  501(c)(3) tax[-exempt status]"; site navigation listing Journal / viXra / SG Prize / Sciurch /
  Gcience / Scibible / Institute.
- **S10** — https://api.openalex.org/sources/S2883122597 · retrieved 2026-09-01 [API] · 23,704 works,
  12,172 citations, homepage `http://vixra.org/`; counts_by_year showing the post-2021 collapse
  quoted in §3.
- **S11** — https://en.wikipedia.org/wiki/List_of_preprint_repositories (wikitext via MediaWiki API)
  · retrieved 2026-09-01 [COM] · **viXra is absent from the table** (string `[[viXra]]` not found).
- **S12** — https://vixra.org/dsalg and https://vixra.org/dsp · retrieved 2026-09-01 [WEB] ·
  per-month submission histories 2009–2026; 173 and 52 records parsed from the listing pages
  respectively; the titles and authors quoted in §5.
- **S13** — https://vixra.org/abs/2604.0057 and https://vixra.org/abs/2607.0056 · retrieved
  2026-09-01 [WEB/DOC] · the admin AI-assistance note; the standing per-paper disclaimer quoted in
  §4; the comment-moderation rule; unique-IP download counter.
- **S14** — "What's arXiv spelled backwards? A new place to publish", *Nature News Blog*,
  16 July 2009 · https://web.archive.org/web/20111201185937/http://blogs.nature.com/news/2009/07/whats_arxiv_spelled_backwards.html
  · cited via S2 [COM, secondary — the archived URL was not independently fetched in this pass].
- **S15** — Collins H., Bartlett A., Reyes-Galindo L., "Demarcating Fringe Science for Policy",
  *Perspectives on Science* 25(4):411–438, July–August 2017 · https://doi.org/10.1162/posc_a_00248 ·
  Crossref and OpenAlex metadata retrieved 2026-09-01 [LIT] · 35 citations in OpenAlex.
- **S16** — Delfanti A., "Fake archives: The search for openness in scholarly communication
  platforms", in Biagioli M. & Lippman A. (eds), *Gaming the Metrics: Misconduct and Manipulation in
  Academic Research*, MIT Press, 2020, ch. 20, pp. 261–269, ISBN 978-0-262-53793-3 · cited via S2
  [LIT, secondary — bibliographic record not independently retrieved].
- **S17** — Yudhoatmojo S., De Cristofaro E., Blackburn J., "Understanding the Use of e-Prints on
  Reddit and 4chan's Politically Incorrect Board", *Proceedings of the 15th ACM Web Science
  Conference 2023* · https://doi.org/10.1145/3578503.3583627 · Crossref metadata retrieved
  2026-09-01 [LIT] · preprint version at arXiv:2111.02455.
- **S18** — direct probes of vixra.org, 2026-09-01 [WEB] · negative controls `/abs/9999.0001`,
  `/pdf/9999.0001v1.pdf`, `/nosuchcategory` → HTTP 404, 746 B; positive controls `/abs/2607.0056`
  → 200/7,100 B and `/pdf/2607.0056v1.pdf` → 200/84,174 B with `%PDF-` magic bytes.
- **S19** — http://viXra.org/feed/rss.xml · retrieved 2026-09-01 [WEB] · HTTP 200,
  `application/xml`, 89,393 bytes; `lastBuildDate Mon Aug 31 18:37:27 EDT 2026`; per-item
  `<category>` element.
- **S20** — http://rxiv.org/ · probed 2026-09-01 [WEB] · HTTP 200, 10,486 bytes — byte-identical in
  size to the viXra home page; same-operator mirror.
- **S21** — https://vixra.org/access · retrieved 2026-09-01 [DOC] · PDF-only distribution; no
  alternative delivery channels; no login required.
