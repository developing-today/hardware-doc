# bioRxiv and medRxiv — preprint repository record

- **URLs:** https://www.biorxiv.org/ · https://www.medrxiv.org/
  · operator: https://openrxiv.org/ · API: https://api.biorxiv.org/
- **Operator:** **openRxiv**, an independent US non-profit (OPENRXIV CORP, 417 Mace Blvd
  STE J110, Davis, CA 95618), since **2025-03-11** (S1, S6). Before that both were run by
  **Cold Spring Harbor Laboratory** (CSHL); medRxiv under a management partnership of
  CSHL + **Yale University School of Medicine** + **BMJ Group** (S2). Principal funder
  throughout: the **Chan Zuckerberg Initiative** (S2, S3, S6).
- **Discipline scope:** bioRxiv — all of the biological sciences, *excluding* clinical
  work. medRxiv — health sciences, clinical and public-health research. The two are
  co-managed but have **separate scope and screening policies**, and cross-posting is
  forbidden (S6, S7).
- **Launched:** bioRxiv **2013**, medRxiv **2019** (S2) · **Status:** both **active** and
  at record volume (§4).
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What they are

bioRxiv is the arXiv of biology, and it worked. Founded at Cold Spring Harbor Laboratory
in 2013 by John Inglis and Richard Sever with the stated goal of "establishing the use of
preprints as a journal-independent method of distributing life science research results"
(S2), it took a discipline with essentially no preprint culture — biology in 2013 posted
almost nothing ahead of review — and made preprinting normal within about six years.
**347,954 new preprints** through 2026-09-01 (S4). medRxiv, launched 2019 for health and
clinical science, adds **88,194** (S5). openRxiv's own summary — "over 430,000 preprints
… 5,000 new research articles are posted each month" (S2) — matches the API totals to
within rounding, which is a good sign for a self-reported figure.

For a knowledge base about hardware and systems these are mostly out of scope, and this
record is deliberately shorter than the arXiv one. But two things make them worth a
proper entry. First, **bioRxiv's `Bioinformatics` category is one of the largest venues
in the world for announcing scientific software** — Bioconda, Kraken 2, Scanpy, Salmon,
ColabFold and Nextstrain all appeared here before their journal versions (§6). Second,
bioRxiv and medRxiv are the **only major preprint servers that publish a measured,
machine-readable preprint-to-publication rate** (§5). Almost every other record in this
collection has to say "eventual publication rate: not measured". Here you can compute it
yourself, and that number is the single most useful reliability statistic in this pass.

Both are free to post and free to read, carry no article-processing charge, assign
Crossref DOIs under the `10.1101/` prefix, are archived at **Portico**, and are indexed
by Crossref, Google Scholar, Semantic Scholar, Europe PMC and the Web of Science Preprint
Citation Index; NIH-funded preprints are additionally indexed in PubMed (S6, S7).

## 2. Governance — the 2025 move to openRxiv

**Verified.** On **2025-03-11** openRxiv was announced as "an independent nonprofit to
oversee bioRxiv and medRxiv" (S1, dated post). A second post the same day advertised for
its inaugural CEO (S8). What actually changed:

| Before (to 2025-03) | After (openRxiv) |
|---|---|
| Services *of* CSHL, with Yale/BMJ partnership for medRxiv | Separate 501(c)-style non-profit corporation, `OPENRXIV CORP`, Davis CA (S6 DMCA agent address) |
| Governance inside a host laboratory | **6-member board of directors**: Scott Fraser (chair), Edith Heard, Jeff Huber, Harlan Krumholz, Bruce Stillman, Shirley Tilghman (S9) |
| Advisory input ad hoc | **Scientific and Medical Advisory Board (SMAB)**, chaired by John Inglis, deputy chair Theodora Bloom; ~15 members (S2). Inaugural meeting reported **2025-07-22** (S10) |
| CZI grants to CSHL (PI: John Inglis, "sequential major grants … since 2017") (S2) | **CZI provided three years of seed funding** to launch the organisation; one of six board seats has a CZI affiliation (S9) |

The substance, per openRxiv's own Q&A (S9): the board "approves key policies, provides
strategic guidance, and oversees executive leadership"; board members serve "as individual
supporters of its mission, not institutional representatives"; and "funding agreements do
not include stipulations that impact editorial independence". openRxiv is explicit that it
**is not itself a preprint server** and that **no server policies changed** as a result of
the transition — bioRxiv and medRxiv "continue operating as separate platforms but with
common technologies, complementary policies, and a single team" (S2, FAQ).

Personnel since: **Tracy Teal** appointed inaugural CEO **2025-08-18** (S10); Gabriel Stein
Head of Product **2026-06-30** (S11). Inglis and Sever received the Royal Society's 2025
Research Culture Award (S10, dated 2025-08-28) — [COM], as reported by openRxiv itself.

**Honest read [INF]:** the governance change is real and is the right kind of move
(single-institution dependency → dedicated non-profit with an external board), but the
funding concentration did not change much. CZI remains the dominant funder and holds a
board seat. openRxiv says it is "pursuing diversified funding models" (S9); as of
2026-09-01 the published supporter list is still CZI + CSHL + Sergey Brin Family
Foundation + Robert Lourie Foundation + a dozen universities (S2). Treat "sustainable"
as an aspiration with a three-year runway, not an accomplished fact.

## 3. Scope and subject taxonomy

**bioRxiv: ~25 author-selected categories, one per preprint** (S6). Verified exhaustive
against the API: the 27 category names below sum to exactly the server-wide 2025 total of
49,318 (§4), so the list is complete.

Two of them are **closed to new submissions** — `Clinical Trials` and `Epidemiology` were
retired when medRxiv launched in 2019 and now accept only revisions to existing papers
(S6). Note the API's behaviour here (§10): querying those categories silently returns
*all* categories rather than an error.

**medRxiv: ~50 categories** (S7), health-specialty oriented (Cardiovascular Medicine,
Infectious Diseases, Oncology, Public and Global Health, Health Informatics, …).

Both servers are explicit about what is **out of scope** (S6, S7): no narrative reviews,
no editorials/opinion, no hypothesis-only articles, no theses or teaching material, no
protocols or "tool announcements" on their own, no product advertisements, no standalone
figures or datasets. medRxiv additionally excludes case reports and series, preclinical
work, veterinary studies and rebuttals. **The tool-announcement exclusion matters for the
software reader**: bioRxiv will not take a bare software paper. Its own wording — "software
announcements that do not include detailed methods and research data produced by their
output/application" are not sufficient (S6). A bioinformatics preprint here therefore
tends to come with a benchmark, not just a repository link.

## 4. Size and growth

All figures **[API]**, retrieved **2026-09-01**.

**bioRxiv**, from `https://api.biorxiv.org/sum/y` (S4) — note this endpoint counts *new
papers* separately from *revisions*:

| Year | New preprints | Cumulative | Revisions |
|---|---|---|---|
| 2013 | 109 | 109 | 34 |
| 2014 | 886 | 995 | 372 |
| 2015 | 1,774 | 2,769 | 776 |
| 2016 | 4,718 | 7,487 | 1,903 |
| 2017 | 11,339 | 18,826 | 4,625 |
| 2018 | 20,778 | 39,604 | 7,786 |
| 2019 | 29,179 | 68,783 | 10,683 |
| 2020 | 38,717 | 107,500 | 14,323 |
| 2021 | 36,866 | 144,366 | 14,424 |
| 2022 | 35,750 | 180,116 | 12,838 |
| 2023 | 39,155 | 219,271 | 14,804 |
| 2024 | 43,632 | 262,903 | 16,936 |
| 2025 | 49,318 | 312,221 | 17,893 |
| 2026 (to 09-01) | 35,733 | **347,954** | 13,432 |

**medRxiv**, from `count_new_papers` on `details/medrxiv/<year>` (S5):

| Year | New preprints | Cumulative |
|---|---|---|
| 2019 (from Jun) | 913 | 913 |
| 2020 | 14,070 | 14,983 |
| 2021 | 12,738 | 27,721 |
| 2022 | 10,527 | 38,248 |
| 2023 | 11,046 | 49,294 |
| 2024 | 12,863 | 62,157 |
| 2025 | 15,000 | 77,157 |
| 2026 (to 09-01) | 11,037 | **88,194** |

**Combined: 436,148 preprints.** Growth is *not* flattening: 2025 was bioRxiv's largest
year ever and 2026 is on pace to beat it. The COVID bump is visible as a 2020 spike
followed by a 2021–22 dip on both servers, then recovery.

**Recorded conflict.** The openRxiv homepage on 2026-09-01 displays "**273,956** articles"
for bioRxiv and "**65,414** articles" for medRxiv (S3) [WEB]. Both are far below the API
totals. Cross-referencing the cumulative tables above places 273,956 in bioRxiv's early
2025 and 65,414 in medRxiv's early 2025 — i.e. **the homepage counters appear frozen at
the March-2025 openRxiv launch and have not been updated since** [INF]. The About page on
the same site says "over 430,000", which agrees with the API. Use the API.

**Usage**, from `api.biorxiv.org/usage/y/<server>` (S12): bioRxiv 2025 saw 8,842,153
abstract views, 2,350,894 full-text views and 4,864,664 PDF downloads; cumulative PDF
downloads reached 21,963,655 by end-2025. medRxiv cumulative abstract views 26,052,977.
(medRxiv's series carries a blank-year bucket of 3.28M views, presumably pre-2019
backfill or unattributed — treat the medRxiv year-splits as approximate.)

## 5. The measured preprint-to-publication rate

This is the section to steal for other records. bioRxiv/medRxiv link each preprint to its
journal version automatically (usually within ~2 weeks of publication, S6), and expose
that link in the API. So the rate is *measurable*, not estimated.

**Server-wide, all time** [API], 2026-09-01, from `api.biorxiv.org/pubs/<server>/<range>`
which reports a `total` of preprint→publication links (S13):

| Server | Preprints | With a linked journal publication | Raw rate |
|---|---|---|---|
| bioRxiv | 347,954 | **177,932** | **51.1 %** |
| medRxiv | 88,194 | **39,885** | **45.2 %** |

That raw rate is a **lower bound** and badly censored: a third of bioRxiv's corpus was
posted in the last two years and has not had time to be published.

**Cohort measurement** is the honest version. I sampled fixed calendar windows, deduped
by DOI across versions, and counted records whose `published` field is not `NA`
[API, 2026-09-01, script `scratch/preprint-repositories/lifesci/cohort.py`]:

| Server | Cohort window | Unique preprints | Published | Rate |
|---|---|---|---|---|
| bioRxiv | 2016-05-01 … 05-07 | 108 | 84 | **77.8 %** |
| bioRxiv | 2018-05-01 … 05-07 | 467 | 332 | **71.1 %** |
| bioRxiv | 2019-05-01 … 05-07 | 661 | 457 | **69.1 %** |
| bioRxiv | 2020-05-01 … 05-07 | 1,137 | 817 | **71.9 %** |
| bioRxiv | 2022-05-01 … 05-07 | 951 | 560 | 58.9 % (censored) |
| bioRxiv | 2024-05-01 … 05-07 | 1,077 | 546 | 50.7 % (censored) |
| bioRxiv | 2025-05-01 … 05-07 | 1,080 | 511 | 47.3 % (heavily censored) |
| medRxiv | 2019-10-01 … 10-31 | 189 | 151 | **79.9 %** |
| medRxiv | 2020-05-01 … 05-07 | 575 | 371 | **64.5 %** |
| medRxiv | 2022-05-01 … 05-07 | 246 | 133 | 54.1 % (censored) |
| medRxiv | 2024-05-01 … 05-07 | 330 | 144 | 43.6 % (censored) |

**Headline number: for mature bioRxiv cohorts (2016–2020, ≥6 years elapsed), 69–78 % of
preprints have a linked peer-reviewed journal publication.** medRxiv's small 2019 cohort
is comparable at 80 %; its 2020 COVID cohort is lower at 64.5 %, consistent with a large
volume of pandemic-era material that never cleared review.

This **agrees with the operator's own claim** — openRxiv states "75 % of bioRxiv and
medRxiv preprints go on to be published in peer-reviewed journals" (S9) [DOC] — and with
the published literature: Abdill & Blekhman's *eLife* 2019 study of the whole bioRxiv
corpus found a comparable outcome rate (S14; itself posted as bioRxiv `10.1101/515643`,
2019-01-13, before *eLife* `10.7554/eLife.45133`).

**Caveats on the rate.** (a) The link is Crossref-matched and openRxiv itself admits "on
rare occasions a match is not made for technical reasons" (S6) — so it slightly
*under*-counts. (b) "Published" says nothing about *where*; the linked venue ranges from
*Nature* to predatory. (c) The complement is not "rejected": it mixes rejected work,
abandoned work, work published without a detected link, and work whose authors never
submitted. (d) The trend across cohorts is downward even allowing for censoring — the
2016 cohort is 78 % after 10 years, the 2018 cohort 71 % after 8. [INF] Worth watching,
but do not over-read it from these sample sizes.

## 6. The software angle — bioinformatics and computational biology

`Bioinformatics` is bioRxiv's second-largest category and a first-class venue for
scientific software. Counts [API], year-by-year query of
`details/biorxiv/<year>?category=bioinformatics`, retrieved 2026-09-01 (S15):

| Year | Bioinformatics preprints | | Year | Bioinformatics preprints |
|---|---|---|---|---|
| 2013 | 14 | | 2020 | 3,089 |
| 2014 | 159 | | 2021 | 2,918 |
| 2015 | 313 | | 2022 | 3,003 |
| 2016 | 707 | | 2023 | 3,245 |
| 2017 | 1,286 | | 2024 | 3,609 |
| 2018 | 1,929 | | 2025 | 4,235 |
| 2019 | 2,347 | | 2026 (to 09-01) | 3,509 |

**Total: 30,363 preprints**, 8.7 % of bioRxiv.

Full 2025 category ranking [API] (sums to 49,318 = the server total, so this is complete):

| Rank | Category | 2025 | Rank | Category | 2025 |
|---|---|---|---|---|---|
| 1 | Neuroscience | 9,071 | 15 | Physiology | 1,027 |
| 2 | **Microbiology** | 4,651 | 16 | **Systems Biology** | 892 |
| 3 | **Bioinformatics** | 4,235 | 17 | Animal Behavior & Cognition | 758 |
| 4 | Cell Biology | 2,921 | 18 | Pharmacology & Toxicology | 626 |
| 5 | Cancer Biology | 2,487 | 19 | **Synthetic Biology** | 525 |
| 6 | **Biophysics** | 2,283 | 20 | Pathology | 385 |
| 7 | Immunology | 2,280 | 21 | Zoology | 265 |
| 8 | Biochemistry | 2,261 | 22 | Sci. Communication & Education | 127 |
| 9 | Molecular Biology | 2,118 | 23 | Paleontology | 74 |
| 10 | Ecology | 2,103 | — | Clinical Trials | closed |
| 11 | Genomics | 2,038 | — | Epidemiology | closed |
| 12 | **Bioengineering** | 1,967 | | | |
| 13 | Evolutionary Biology | 1,880 | | | |
| 14 | Plant Biology | 1,789 | | | |

The five bolded computational/physical categories — Bioinformatics, Biophysics,
Bioengineering, Systems Biology, Synthetic Biology — total **9,902 in 2025, 20.1 % of the
server**. `Biophysics` and `Bioengineering` are where the instrumentation lives: cryo-EM
detector and reconstruction work, super-resolution and light-sheet microscopy, patch-clamp
and multi-electrode array electrophysiology, microfluidics, biosensors and lab-on-chip.
`Bioengineering` in particular reads more like an EE/mechatronics section than a biology
one. If you build imaging or sensing hardware, these are the two feeds to subscribe to.

**Named examples, every one verified against the bioRxiv API** (server, first-version
posting date, category, linked publication) — all of these are **preprint-first**, i.e.
the bioRxiv version predates the journal article (S16):

| Tool / paper | bioRxiv DOI | Posted | Category | Journal version |
|---|---|---|---|---|
| **Salmon** (transcript quantification) | `10.1101/021592` | 2015-06-27 | Bioinformatics | *Nat Methods* `10.1038/nmeth.4197` |
| **DeepVariant** (deep-learning variant caller) | `10.1101/092890` | 2016-12-14 | Genomics | *Nat Biotechnol* `10.1038/nbt.4235` |
| **Scanpy** (single-cell analysis) | `10.1101/174029` | 2017-08-09 | Bioinformatics | *Genome Biol* `10.1186/s13059-017-1382-0` |
| **Bioconda** (package distribution) | `10.1101/207092` | 2017-10-21 | Bioinformatics | *Nat Methods* `10.1038/s41592-018-0046-7` |
| **Nextstrain** (real-time pathogen phylogenetics) | `10.1101/224048` | 2017-11-22 | Evolutionary Biology | *Bioinformatics* `10.1093/bioinformatics/bty407` |
| **DeepLabCut 3D** (markerless pose tracking) | `10.1101/476531` | 2018-11-24 | Neuroscience | *Nat Protoc* `10.1038/s41596-019-0176-0` |
| **Kraken 2** (metagenomic classification) | `10.1101/762302` | 2019-09-07 | Bioinformatics | *Genome Biol* `10.1186/s13059-019-1891-0` |
| **ColabFold** (accessible protein folding) | `10.1101/2021.08.15.456425` | 2021-08-15 | Bioinformatics | *Nat Methods* `10.1038/s41592-022-01488-1` |
| **ESM-2 / ESMFold** (protein language model) | `10.1101/2022.07.20.500902` | 2022-07-21 | Synthetic Biology | *Science* `10.1126/science.ade2574` |
| **RFdiffusion** (generative protein design) | `10.1101/2022.12.09.519842` | 2022-12-10 | Biochemistry | *Nature* `10.1038/s41586-023-06415-8` |

Bioconda, Nextstrain, ColabFold and DeepLabCut are ordinary open-source projects whose
canonical citation is a bioRxiv-first paper. If you consume any of that stack, you are
already downstream of this server.

## 7. Screening and moderation — what gets in

Neither server peer-reviews. Both run a **real, staffed, multi-step screen**, and it is
stricter than most preprint servers in this collection.

**Shared process** (S9, S6, S7): "All submissions are screened by the in-house Content
Team. **Affiliate scientists**, who are listed on each server site, must approve each
manuscript before it goes live. For articles in challenging areas, e.g. dual use research
of concern, advice is solicited from subject matter experts. Only a small minority of
submissions are declined. The authors are told why and appeals are always considered."
(S9) [DOC]. So there are two gates: paid staff, then a volunteer domain scientist.

**bioRxiv screens for** (S6): plagiarism; non-scientific content; inappropriate article
types (§3); "material that could potentially endanger the health of individual patients or
the public … including … **dual-use research of concern** and works that challenge or
could compromise accepted public health measures and advice regarding infectious disease
transmission, immunization, and therapy"; and any image or information that could identify
an individual (blurring or pixelation is explicitly **not** accepted). English only,
because "we are only able to screen for inappropriate or dangerous content in English".
Typical turnaround **~72 hours**.

**medRxiv is materially stricter**, and the reason is clinical harm — a wrong dose or a
bogus efficacy claim can kill someone before review would have caught it. On top of
everything bioRxiv checks, medRxiv requires (S7) [DOC]:

- **Ethical oversight statement** from a named IRB / Ethics Committee "for all cases in
  which human subjects, samples or data were used". The FAQ explicitly *rejects* decisions
  from online tools, audit bodies, Caldicott Guardians, biosafety or data-protection
  committees, HR, or R&D departments. Oversight must cover the whole study.
- **Clinical trial registration** — a trial ID from an ICMJE-recognised registry for any
  prospective interventional study "regardless of the cohort size"; unregistered studies
  are sent back to register retrospectively.
- **A hard identifiability rule** with an enumerated list: direct identifiers (names,
  document numbers, patient/sample IDs, photographs, biometrics, precise ages, exact
  dates/locations) are banned outright, and there must be **fewer than three indirect
  identifiers** (age range, ethnicity, religion, occupation, family details, medical
  history). If the data cannot be de-identified, medRxiv tells the authors to go to a
  journal instead.
- **A causal-language rule**: "We strongly recommend that authors avoid using causal
  language, unless justified by a robust causal inference framework. Papers with
  inappropriate causal language may be declined."
- Screening takes **2–4 days**, versus ~72 h on bioRxiv.
- Every medRxiv posting carries a stamp that it "**should not be used to directly inform
  clinical decision-making**" (S7) — bioRxiv's stamp has no such clause.

Manuscripts submitted to the wrong server are *not* forwarded automatically: the
submission is closed and the author must resubmit, "to ensure that manuscripts are
screened by the appropriate screening team" (S6, S7).

Also worth knowing: **commercial submissions are accepted** but must be research, not
product description; author affiliations are mandatory so company authorship is visible;
on medRxiv, company associations must be disclosed as conflicts (S9).

## 8. Reliability — what you can and cannot trust

**What a deposit here guarantees:** a Crossref DOI under `10.1101/`; a timestamp; a
plagiarism scan; a staff + affiliate-scientist eligibility screen; a Portico archival
copy; full-text XML; permanence (posted preprints are *never* removed — only withdrawn,
with a watermark and a public reason, the original still reachable via Info/History)
(S6, S7). That is a stronger floor than most servers in this collection.

**What it does not guarantee:** correctness, reproducibility, statistical competence, or
that anyone qualified read the results section. The servers say so themselves, in the
banner on every page: articles "might contain errors and report information that has not
yet been accepted or endorsed in any way by the scientific or medical community" (S6).

**How to sanity-check an individual preprint — the API method.** For any `10.1101/` DOI:

```bash
curl -s https://api.biorxiv.org/details/biorxiv/10.1101/207092/na/json
```

Read three fields on the **last** element of `collection`:

- `published` — a journal DOI, or `NA`. Not `NA` means it survived peer review somewhere.
  Then check *where*: resolve the DOI and look at the venue.
- `version` — how many revisions. A v1 from 2019 that was never revised and has
  `published: NA` is a dead preprint; weight accordingly.
- `type` — one of `new results`, `confirmatory results`, `contradictory results`, or
  **`withdrawn`**. A withdrawn preprint is still served by the API and still resolves;
  the flag is the only signal.

`type: withdrawn` is rare. In a 2026-06-01…06-14 census [API]: 2 withdrawn out of 2,843
bioRxiv preprints (0.07 %), 1 of 777 on medRxiv (S17). **Do not treat 0.07 % as a
correctness rate** — it is a self-reporting rate, and it is the floor of the error rate,
not an estimate of it.

**Known failure modes.** (a) Preprints that are wrong and travel anyway — see §9.
(b) The screen is for *danger and eligibility*, not quality: methodologically weak work
posts routinely and the servers do not claim otherwise. (c) Category assignment is
author-chosen, single-valued, and openRxiv calls it "not a formal ontology" (S6) — do not
use it as a taxonomy. (d) The published-link matcher occasionally misses (S6), so `NA` is
weak evidence of non-publication for very recent journal articles. (e) Cross-posting to
another server is forbidden and results in withdrawal (S6) — so unlike arXiv/HAL you will
not find bioRxiv content mirrored elsewhere, which is a single-point-of-failure argument
that Portico only partly answers.

## 9. COVID-19: the stress test

The pandemic is the reason most people outside biology have heard of medRxiv, and it cuts
both ways.

**The surge is measurable** [API, §4]: medRxiv went from **913** preprints in its
half-year of 2019 to **14,070** in 2020 — a 15× jump in a server barely six months old.
bioRxiv rose from 29,179 to 38,717 over the same period.

**The good case.** The first SARS-CoV-2 genome papers went up here days after sequencing.
Wu et al., *"Discovery of a novel coronavirus associated with the recent pneumonia
outbreak in humans and its potential bat origin"*, bioRxiv `10.1101/2020.01.22.914952`,
**posted 2020-01-23**, published in *Nature* `10.1038/s41586-020-2012-7` (S16) [API].
Hoffmann et al. on ACE2/TMPRSS2 entry — the paper that pointed the whole field at
TMPRSS2 inhibitors — bioRxiv `10.1101/2020.01.31.929042`, **posted 2020-01-31**, *Cell*
`10.1016/j.cell.2020.02.052` (S16) [API]. Both are preprint-first by weeks, in a period
when weeks mattered.

**The bad case.** Pradhan et al., *"Uncanny similarity of unique inserts in the 2019-nCoV
spike protein to HIV-1 gp120 and Gag"*, bioRxiv `10.1101/2020.01.30.927871`, posted
2020-01-31, `published: NA` (S16) [API]. It claimed engineered HIV inserts in the
SARS-CoV-2 spike, was demolished in the comments within about 48 hours, and was withdrawn
by the authors — but not before it became foundational material for lab-leak and bioweapon
narratives that outlived the withdrawal by years. This is the canonical demonstration that
**withdrawal does not recall a preprint**; the DOI still resolves, and it should, but the
claim is loose.

The other well-documented policy case is Bendavid et al., *"COVID-19 Antibody
Seroprevalence in Santa Clara County, California"*, medRxiv
`10.1101/2020.04.14.20062463`, posted 2020-04-17 (S16) [API]. It was covered worldwide
within 24 hours and used to argue that infection fatality rates — and therefore the case
for lockdowns — had been overstated; its assay-specificity and weighting assumptions were
contested immediately and publicly. It *was* eventually published (*Int J Epidemiol*
`10.1093/ije/dyab010`, 2021), a year after the policy argument had moved on. The lesson is
not that the preprint was worthless; it is that **the press and policy cycle is faster
than the correction cycle**, and preprint servers widen that gap.

For the scholarly account, see Fraser et al., *"The evolving role of preprints in the
dissemination of COVID-19 research and their impact on the science communication
landscape"*, *PLOS Biology* 2021, `10.1371/journal.pbio.3000959` — itself preprint-first
as bioRxiv `10.1101/2020.05.22.111294`, posted 2020-05-23 (S18) [API/LIT].

openRxiv's own position on all of this is unusually candid and worth quoting: the public
"should regard preprints as conversations among scientists"; science is "less the parade
of decisive blockbuster discoveries that the press often portrays, and more a slow,
erratic stumble toward ever less uncertainty"; "but as we keep saying, preprints should be
treated with caution" (S9) [DOC].

## 10. Access, APIs and bulk retrieval

**The API is one of the best in this collection.** `https://api.biorxiv.org/`, no key, no
registration, JSON/XML/CSV, documented on one page (S19).

| Endpoint | What it gives | Page size |
|---|---|---|
| `/details/{server}/{from}/{to}/{cursor}` | Full metadata per version; `?category=` filter | 30 |
| `/details/{server}/{doi}/na/json` | Single manuscript, all versions | — |
| `/pubs/{server}/{from}/{to}/{cursor}` | **preprint → journal publication links** | 100 |
| `/pub/{from}/{to}/{cursor}` | published-article view, bioRxiv only | 100 |
| `/publisher/{prefix}/{from}/{to}/{cursor}` | preprints published by a given DOI prefix | 100 |
| `/funder/{server}/{from}/{to}/{ror}/{cursor}` | funder-filtered; **data only from 2025-04-10** | 100 |
| `/sum/{m\|y}` | new + revised counts, interval and cumulative | — |
| `/usage/{m\|y}/{server}` | abstract views, full-text views, PDF downloads | — |

`messages[0]` carries `count_new_papers` (distinct preprints) *and* `total` (rows,
i.e. **versions**). Use `count_new_papers` for sizes; `total` will overcount by ~40 %.

**Probe results, all 2026-09-01:**

| Probe | Result |
|---|---|
| `GET /pubs/biorxiv/2013-01-01/2026-09-01/0` | 200, 207,412 B, `total: 177932` ✅ |
| `GET /pubs/medrxiv/2019-01-01/2026-09-01/0` | 200, 257,683 B, `total: 39885` ✅ |
| `GET /sum/y` | 200, 1,759 B, full yearly series ✅ |
| `GET /details/biorxiv/2013-01-01/2026-09-01/0` | 200 but **0 bytes** — full-range `details` queries never complete. Chunk by year. |
| **Negative control** — `/details/notaserver/2025-06-01/2025-06-30/0` | 200, 74 B, `{"status":"Server not recognized"}`, empty collection ✅ correct rejection |
| **Negative control** — `/details/biorxiv/10.1101/999999.999999/na/json` | 200, 67 B, `{"status":"no posts found"}` ✅ correct rejection |
| **Negative control** — `/details/biorxiv/2025-06-01/2025-06-30?category=quantum_gravity` | 200, **82,363 B**, `"category":"all"`, 3,948 papers ❌ **silently falls back to all categories** |

**That last one is a trap.** A misspelled or retired category (e.g. `epidemiology`,
`clinical_trials` on bioRxiv) returns the *entire server* rather than an error — I hit it
first with `epidemiology` and `clinical trials`, both of which returned exactly 49,318,
the 2025 server-wide total. **Always assert `messages[0].category` equals what you asked
for.** My 2025 table (§6) is validated by the sum-to-total check for exactly this reason.

**Bulk full text — the AWS S3 requester-pays buckets. Verified** from both operators'
own TDM pages (S20, S21) [DOC]:

- `s3://biorxiv-src-monthly` — us-east-1
- `s3://medrxiv-src-monthly` — us-east-1

Both are **requester-pays**: `s3cmd ls s3://biorxiv-src-monthly --requester-pays`. An AWS
account is required. The operators are explicit that the charges "are not a source of
revenue" but exist so the servers "cannot incur unpredictable expense as a consequence of
errant or abusive access". Layout: `Back_Content/Batch_[nn]/` (historical, loaded late
2020) and `Current Content/<Month>_<Year>/`. Files are named `.meca` but are **zip
archives** containing `manifest.xml` plus a `content/` folder with PDF, full-text XML,
figures and supplementary files. Monthly deposit, completing a few days into each month.

**Rate limiting / blocking.** `api.biorxiv.org` is open and did not rate-limit across
several hundred requests on 2026-09-01. The **web** front ends do: `www.biorxiv.org/tdm`
returned **HTTP 429 (17 bytes)** to a Chrome UA, to `curl/8.5.0` and to a ClaudeBot UA,
and **200 (28,613 bytes)** to `WhatsApp/2.23.20.0`. `www.medrxiv.org` served the same page
type fine to Chrome. Per the house rule this is noted only as a retrieval observation and
not as evidence that the page works normally for ordinary clients (S20).

Also available: per-subject RSS/Atom feeds, and `https://connect.biorxiv.org/biorxiv_xml.php?subject=all`
(200, 76,570 B, `application/xml`, 2026-09-01).

## 11. Licensing and reuse

**Authors retain copyright** and pick from six options at submission (S6, S7) [DOC]:
all-rights-reserved ("no reuse/adaptation without permission"), CC-BY-NC-ND, CC-BY-ND,
CC-BY-NC, CC-BY, or CC0.

There is **no default open licence**, and the actual mix matters. Census of every preprint
posted 2026-06-01…06-14 [API] (S17):

| Licence | bioRxiv (n=2,843) | medRxiv (n=777) |
|---|---|---|
| CC-BY | 996 (35.0 %) | 228 (29.3 %) |
| CC-BY-NC-ND | 804 (28.3 %) | 181 (23.3 %) |
| **all rights reserved** (`cc_no`) | **553 (19.5 %)** | **115 (14.8 %)** |
| CC-BY-NC | 350 (12.3 %) | 58 (7.5 %) |
| CC-BY-ND | 100 (3.5 %) | 24 (3.1 %) |
| CC0 (incl. `cc0_ng`) | 40 (1.4 %) | 20 (2.6 %) |
| *(blank / unrecorded)* | 0 | 151 (19.4 %) |

**Roughly one preprint in five on bioRxiv is all-rights-reserved, and only ~36 % carry a
fully open CC-BY/CC0 licence.** If you are building a corpus, you must read the
per-record `license` field — there is no blanket permission. The TDM buckets do not change
this: both TDM pages state the bucket "is *not* intended as a source for further
redistribution … nor does it grant others permission to re-host content", that indexing
services "must link back to the text hosted at bioRxiv rather than re-host content", and
that reuse of individual articles is governed by the author's chosen licence — "in most
cases, this will require you to contact the copyright holder in advance" (S20, S21).

Bulk TDM itself is permitted: authors "explicitly consent to [it] during submission" and
the operators consider it "consistent with fair use doctrine applied to US copyright law"
(S20, S21). Note that is a **US fair-use** argument, not a licence grant.

openRxiv posted "Preprint licensing updates" on **2026-05-20** (S11); I did not retrieve
the post body, so **what changed in that update is [NOT-VERIFIED]** — the six options
above are what the two FAQs listed on 2026-09-01.

## 12. Caveats

1. **The openRxiv homepage article counters are stale by roughly 18 months** (§4). Use
   the API for any size claim.
2. **A bad `category` parameter returns the whole server, not an error** (§10). Every
   category-conditioned number anyone quotes from this API should be checked.
3. **`total` in the `details` response counts versions, not papers.** ~40 % inflation.
4. **medRxiv's `type` field is not comparable to bioRxiv's.** bioRxiv returns
   `new results` / `confirmatory results` / `contradictory results` / `withdrawn`;
   medRxiv returned `PUBLISHAHEADOFPRINT` for 776 of 777 records in the June-2026 census
   (S17) — an artefact, not a content type. Only `WITHDRAWN` is informative there.
5. **19 % of medRxiv records in that census had an empty `license` field.** Absent ≠ open.
6. **`published: NA` is not proof of non-publication** (matcher misses, S6).
7. **Withdrawal is not retraction and not removal.** The DOI still resolves, and the
   original PDF is still reachable under Info/History (S6, S7).
8. **No cross-posting**, so no independent mirror. Portico is the only preservation
   backstop named by the operators (S6, S7).
9. **English only**, by explicit policy, because screening capacity is English-only (S6).
10. **Funding concentration.** CZI is the dominant funder and holds one of six board seats;
    the seed grant to openRxiv is three years (S9). [INF] The governance risk is lower
    than it was in 2024, but it is not gone.

## 13. Sources

- **S1** https://openrxiv.org/introducing-openrxiv/ · retrieved 2026-09-01 · openRxiv
  launch announcement, dated **March 11, 2025**; CZI as "major early funding"; independent
  non-profit framing. [DOC]
- **S2** https://openrxiv.org/about/ · retrieved 2026-09-01 · founding history (bioRxiv
  2013 CSHL / Inglis & Sever; medRxiv 2019 CSHL + Yale + BMJ; named founders), "over
  430,000 preprints", "5,000 new research articles … each month", funder list, board and
  SMAB rosters, embedded FAQ ("openRxiv is not a preprint server", "policies are not
  changing"). [DOC]
- **S3** https://openrxiv.org/ · retrieved 2026-09-01 · homepage counters "273,956
  articles" (bioRxiv) and "65,414 articles" (medRxiv) — the stale figures in §4. [WEB]
- **S4** https://api.biorxiv.org/sum/y · retrieved 2026-09-01 · bioRxiv yearly new and
  revised counts, cumulative to 347,954. [API]
- **S5** `https://api.biorxiv.org/details/medrxiv/<year>-01-01/<year>-12-31/0`, 2019–2026 ·
  retrieved 2026-09-01 · `count_new_papers` per year; total 88,194. Local log:
  `scratch/preprint-repositories/lifesci/medrxiv-by-year.txt`. [API]
- **S6** https://www.biorxiv.org/about/FAQ · retrieved 2026-09-01 · bioRxiv screening
  criteria, out-of-scope list, ~25 categories, closed Clinical Trials/Epidemiology,
  licence options, withdrawal policy, Portico, indexing, DMCA agent (OPENRXIV CORP,
  Davis CA), 249 integrated journals, bioinformatics/computational-paper policy. [DOC]
- **S7** https://www.medrxiv.org/about/FAQ · retrieved 2026-09-01 · medRxiv screening,
  ethical-oversight requirement, trial-registration requirement, direct/indirect
  identifier rules, causal-language rule, 2–4 day screening, ~50 categories, "should not
  be used to directly inform clinical decision-making". [DOC]
- **S8** https://openrxiv.org/seeking-inaugural-ceo/ (listed on
  https://openrxiv.org/news/page/2/) · retrieved 2026-09-01 · dated March 11, 2025. [DOC]
- **S9** https://openrxiv.org/qa-governance-funding-future/ · retrieved 2026-09-01 ·
  dated May 21, 2025 · named six-member board; "CZI provided three years of seed funding";
  "One person on the six-member board has a CZI affiliation"; screening description
  (in-house Content Team + affiliate scientists + subject-matter experts); **"75% of
  bioRxiv and medRxiv preprints go on to be published in peer-reviewed journals"**;
  commercial-submission policy; the "conversations among scientists" quote. [DOC]
- **S10** https://openrxiv.org/news/page/2/ · retrieved 2026-09-01 · dated index: CEO
  appointment 2025-08-18, Royal Society award 2025-08-28, Dryad partnership 2025-09-18,
  DOI policy post 2025-11-18. [DOC]
- **S11** https://openrxiv.org/news/ · retrieved 2026-09-01 · dated index: "Preprint
  licensing updates" 2026-05-20, "Launching openRxiv Labs" 2026-06-01, Hypothesis
  commenting 2026-04-07, SMAB inaugural meeting 2026-07-22, Head of Product 2026-06-30,
  "openRxiv 2025 year in review" 2025-12-31 ("In March we launched openRxiv"). [DOC]
- **S12** https://api.biorxiv.org/usage/y/biorxiv and `/usage/y/medrxiv` · retrieved
  2026-09-01 · view and download series. [API]
- **S13** `https://api.biorxiv.org/pubs/biorxiv/2013-01-01/2026-09-01/0` and
  `.../medrxiv/2019-01-01/2026-09-01/0` · retrieved 2026-09-01 · `total` = 177932 and
  39885 preprint→publication links. [API]
- **S14** Abdill RJ, Blekhman R. "Tracking the popularity and outcomes of all bioRxiv
  preprints." *eLife* 8:e45133 (2019-04-24), `10.7554/eLife.45133`; preprint bioRxiv
  `10.1101/515643`, posted 2019-01-13. Both verified 2026-09-01 (Crossref + bioRxiv API).
  [LIT]
- **S15** `https://api.biorxiv.org/details/biorxiv/<year>?category=bioinformatics` and the
  27-category 2025 sweep · retrieved 2026-09-01 · local logs
  `scratch/preprint-repositories/lifesci/bioinformatics-by-year.txt`, `cats-2025.txt`,
  `cats-2025b.txt`. Category counts sum exactly to 49,318. [API]
- **S16** `https://api.biorxiv.org/details/{server}/{doi}/na/json` for each DOI in §6 and
  §9 · retrieved 2026-09-01 · confirms server, first-version date, category and linked
  publication DOI. Local logs `landmarks1.txt`, `landmarks2.txt`. [API]
- **S17** Census of `details/{server}/2026-06-01/2026-06-14` (all pages, deduped by DOI) ·
  retrieved 2026-09-01 · licence and `type` distributions; 2 withdrawn / 2,843 on bioRxiv,
  1 / 777 on medRxiv. Local log `licence-dist.txt`. [API]
- **S18** Fraser N, et al. "The evolving role of preprints in the dissemination of COVID-19
  research and their impact on the science communication landscape." *PLOS Biology* 19(4):
  e3000959 (2021-04-02), `10.1371/journal.pbio.3000959`; preprint bioRxiv
  `10.1101/2020.05.22.111294`, posted 2020-05-23 as "Preprinting a pandemic". Both verified
  2026-09-01. [LIT]
- **S19** https://api.biorxiv.org/ · retrieved 2026-09-01 · full endpoint documentation,
  page sizes, `count_new_papers` vs `total` semantics, funder-metadata inception date
  2025-04-10. [DOC]
- **S20** https://www.biorxiv.org/tdm · retrieved 2026-09-01 (HTTP 429 to a Chrome UA and
  to `curl/8.5.0`; HTTP 200, 28,613 B with `WhatsApp/2.23.20.0`) · `s3://biorxiv-src-monthly`,
  us-east-1, requester-pays, `.meca` = zip, Back_Content/Current Content layout, no
  re-hosting permission. [DOC]
- **S21** https://www.medrxiv.org/tdm · retrieved 2026-09-01 (HTTP 200, 28,748 B, default
  Chrome UA) · `s3://medrxiv-src-monthly`, identical terms. [DOC]

### Not verified

- The exact **calendar date medRxiv opened for submissions in 2019** — openRxiv says only
  "2019" (S2) and bioRxiv's FAQ says the clinical pilot completed "In June 2019" (S6).
  Recorded as **2019** only.
- The **content of the 2026-05-20 "Preprint licensing updates" post** (§11).
- **`api.biorxiv.org/covid19/{cursor}`** is documented but returned 200 / 0 bytes on
  2026-09-01. Non-functional at time of retrieval.
- Any **claim about acceptance/decline rates**: openRxiv says only "a small minority of
  submissions are declined" (S9). No numeric decline rate is published.
