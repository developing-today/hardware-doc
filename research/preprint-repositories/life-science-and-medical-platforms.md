# Life-science and medical preprint platforms — grouped record

Covers eleven venues that are **not** general-purpose preprint servers: publisher-owned
preview services, funder-restricted publishing platforms, and one genuinely defunct
pioneer. The two big general life-science servers have their own record —
see [bioRxiv and medRxiv](biorxiv-and-medrxiv.md). ChemRxiv is at
[chemrxiv.md](chemrxiv.md); BioHackrXiv and AIJR Preprints are covered elsewhere.

- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 0. The shared pattern — publisher-tied and funder-tied venues

Almost everything in this record shares one structural property that makes it different
from arXiv, bioRxiv or Zenodo: **you cannot just deposit there.** Access is gated on a
relationship with the sponsor.

| Gate type | Examples |
|---|---|
| **You must be funded by the sponsor** | Wellcome Open Research, Gates Open Research, HRB Open Research, AMRC Open Research, Open Research Africa, Open Research Europe |
| **You must be submitting to the sponsor's journals** | Cell Press Sneak Peek, Preprints with The Lancet, JMIR Preprints, ARPHA Preprints, Beilstein Archives |
| **Open, but publisher-run and now closed** | PeerJ Preprints, Nature Precedings |

Three consequences follow, and they are the reason this record exists:

1. **They are not archives, they are shop windows.** A "preprint server" whose corpus is
   defined by "manuscripts on their way into *our* journals" cannot be used to survey a
   field. Coverage is a function of the sponsor's market share, not of the science. When
   you search Cell Press Sneak Peek you are searching Cell Press's review queue.
2. **The eligibility gate suppresses volume by one to three orders of magnitude.**
   AMRC Open Research has **27 articles in its entire existence** (§3). Beilstein Archives
   has 726 in seven years (§10). Compare bioRxiv's 49,318 in 2025 alone.
3. **Durability is poor, and the failure modes are specific.** Of the eleven venues here,
   one is fully defunct (Nature Precedings), one is closed to new deposits (PeerJ
   Preprints), one has lost its domain entirely (agriRxiv), one has been renamed and
   re-hosted (AAS Open Research → Open Research Africa), one is being drained by a
   successor platform (Gates Open Research → VeriXiv), and one has posted nothing for four
   years (AMRC Open Research). That is **six of eleven** with a discontinuity, against a
   median age of about eight years.

The redeeming detail, and it is a real one: **DOIs held up**. Every dead or moved service
in this record still resolves its DOIs to live content, including Nature Precedings, dead
since 2012 (§7), and agriRxiv, whose own domain is now a Namecheap parking page (§11).
Persistent identifiers plus a publisher with an archival obligation turned out to be a
better preservation strategy than the domain name. That is the single transferable lesson
here.

## 1. Status table — probed 2026-09-01

| Platform | URL | Operator | Launched | **Status** | Size (source) |
|---|---|---|---|---|---|
| **F1000Research** | f1000research.com | F1000 Research Ltd | 2012 | **ALIVE**, ~2,000 articles/yr | **12,442** distinct articles (18,667 versioned DOIs) [API] |
| **Wellcome Open Research** | wellcomeopenresearch.org | Wellcome + F1000 | 2016/17 | **ALIVE**, growing | **4,009** [API] |
| **Gates Open Research** | gatesopenresearch.org | Gates Foundation + F1000 | 2017 | **ALIVE but draining** → new work routes via **VeriXiv** since Aug 2024 | **563** [API] |
| **AAS Open Research** | aasopenresearch.org | AAS + F1000 | 2018 | **RENAMED** — 301 → openresearchafrica.org; no records after 2022 | **114** [API] |
| **Open Research Africa** | openresearchafrica.org | (AAS successor) + F1000 | 2019 | **ALIVE**, small but reviving | **138** [API] |
| **AMRC Open Research** | amrcopenresearch.org | AMRC + F1000 | 2019 | **MORIBUND** — nothing registered since 2022 | **27** [API] |
| **HRB Open Research** | hrbopenresearch.org | Health Research Board (IE) + F1000 | 2018 | **ALIVE** | **731** [API] |
| **PeerJ Preprints** | peerj.com/preprints | PeerJ | 2013 | **CLOSED to new deposits (2019)**; content live, DOIs resolve | **5,068** distinct (6,446 versioned) [API] |
| **Preprints with The Lancet** | ssrn.com/…/the-lancet | Elsevier / SSRN | [NOT-VERIFIED] | **ALIVE** — contrary to expectation | **25,550** papers displayed [WEB] |
| **Cell Press Sneak Peek** | ssrn.com/…/cell-press-sneak-peek | Elsevier / SSRN | [NOT-VERIFIED] | **ALIVE** | **12,404** papers displayed [WEB] |
| **Nature Precedings** | ~~precedings.nature.com~~ → nature.com/npre | Nature Publishing Group | 2007 | **DEFUNCT since 2012**; original host **refuses connections**; **content preserved** | **3,449** records [WEB] |
| **JMIR Preprints** | preprints.jmir.org | JMIR Publications | 2009 (claimed) | **ALIVE**, very large | **41,766** `posted-content` DOIs [API] |
| **ARPHA Preprints** | preprints.arphahub.com | Pensoft | 2020 | **ALIVE**, growing | **1,058** [API] |
| **Beilstein Archives** | beilstein-archives.org | Beilstein-Institut | 2019 | **ALIVE but declining** | **726** [API] |
| **agriRxiv** | ~~agrirxiv.org~~ → cabidigitallibrary.org | CABI (+ Open Access India) | 2017 | **DOMAIN DEAD** (parked); **service migrated**, DOIs resolve | **1,054** DOIs under `10.31220` [API] |

*Bonus finds not in the brief but part of the same family:* **Open Research Europe**
(European Commission, F1000-powered, 2021–) — **1,513** distinct articles, growing fast
(628 in 2025) [API]; **VeriXiv** (verixiv.org, Gates + F1000, 2024–) — live, size not
measured.

## 2. F1000Research

- **URL:** https://f1000research.com/ · **HTTP 200**, 114,761 B, 2026-09-01
- **Operator:** Crossref registers prefix `10.12688` to **"F1000 Research Ltd"**, member
  2560 (S1) [API]. Corporate parent commonly reported as **Taylor & Francis / Informa**
  (acquisition 2020) — **[NOT-VERIFIED]**, no statement to that effect on the pages I
  retrieved.
- **Launched 2012**; the `container-title: F1000Research` activity window in Crossref runs
  **2012–2026** (S1).
- **Size: 12,442 distinct articles** from 18,667 versioned DOIs (S1) [API]. Steady at
  ~2,000/year: 1,898 (2022), 2,063 (2023), 2,195 (2024), 2,031 (2025), 1,868 to 2026-09-01.

**The model, properly.** F1000Research is not a preprint server bolted onto a journal; it
is a *publish-then-review platform*, and the mechanism is worth understanding because
several other entries here are literally the same software (§3). From F1000's own
documentation (S2) [DOC]:

1. **Submission → in-house check only.** An editorial team runs "prepublication checks" for
   policy and ethics compliance. There is **"no Editor (or Editor-in-Chief) to make a
   decision on whether to accept or reject the article, or to oversee the peer-review
   process."** That sentence is the whole design.
2. **Publication within about a week**, with the status **"Awaiting Peer Review"**. The
   article is live, citable, DOI'd, and indexed by Google Scholar from that moment.
3. **Open, invited, named peer review, after publication.** Reviewers are invited; their
   **reports and their names** are published on the article page alongside author
   responses and registered-user comments.
4. **Each reviewer picks one of three statuses**: **Approved** ("no or only minor changes
   required"), **Approved with Reservations** ("academic merit, but … a number of small
   changes … or specific, sometimes more significant revisions"), **Not Approved** ("very
   poor quality … fundamental flaws … that seriously undermine the findings").
5. **Versioned articles.** Authors publish revised versions; **every version is separately
   DOI'd and independently citable**, all versions stay public, the latest is the default,
   and invited reviewers are re-invited to re-review each new version. Articles are
   explicitly "living" — updatable even after review completes.
6. **A hard, published indexing threshold.** An article is indexed in PubMed, PubMed
   Central, MEDLINE, Europe PMC, Scopus, CAS, DOAJ and Embase **only** once it has
   received "at least two 'Approved' statuses, or one 'Approved' and two 'Approved with
   Reservations' statuses from independent and invited peer reviewers" (S2). Posters,
   slides and "documents" are never peer reviewed and never indexed.

**Why this is genuinely distinctive.** The reviewer's identity, verdict and full report
are attached to the object permanently, and the *object's own indexing status* encodes
whether it passed. So — unlike every conventional preprint server in this collection — an
F1000Research article carries its own machine-readable review outcome. You can look at an
article and see three named people saying "Approved" or one saying "Not Approved". The
cost is that you must actually look: **the "Awaiting Peer Review" and "Not Approved"
articles sit at the same URL, with the same DOI, under the same brand as the approved
ones.** Citing "an F1000Research paper" without checking the reviewer statuses is a
mistake, and it is a mistake people make.

**Scope** is far broader than the name suggests: "basic scientific, scholarly,
translational and clinical research across the physical and life sciences, engineering,
medicine, social sciences and humanities", explicitly including **software tools and
method articles**, and explicitly welcoming "confirmatory and negative results, as well as
null studies" (S2). At least one author must be "a qualified researcher, scholar or
clinician actively working in their speciality".

**Licensing:** overwhelmingly **CC BY 4.0** — 30,379 of 31,780 journal-article records
under prefix `10.12688` carry a CC BY 4.0 licence URL, plus 567 CC BY 3.0; only 760 have
none (S1) [API]. That is a far more open corpus than bioRxiv or ChemRxiv. It is not free
to publish, though — F1000Research levies **article processing charges** (S2).

## 3. The F1000-powered funder platforms — one platform, many badges

Wikipedia lists these as separate entities. They are not separate software: they are
**white-labelled instances of the F1000Research platform**, all minting DOIs under the
**same Crossref prefix `10.12688`, registered to F1000 Research Ltd** (S1) [API]. Same
submission flow, same in-house checks, same open named post-publication review, same
three approval statuses, same versioned DOIs, same CC BY default, same indexing threshold
(§2). What differs is the **eligibility gate** and the branding.

Gates Open Research states its gate plainly: an article requires "**at least one author
who has been, or still is, a recipient of a Gates Foundation grant**" (S3) [DOC]. Every
sibling has the equivalent rule for its own funder. Publication costs are met by the
funder rather than the author.

Sizes and activity windows, all from Crossref facets on prefix `10.12688`, retrieved
**2026-09-01** (S1) [API]:

| Platform | Sponsor | Records | Distinct articles | Active years | Recent volume |
|---|---|---|---|---|---|
| Wellcome Open Research | Wellcome Trust | 5,468 | **4,009** | 2016–2026 | 908 (2024), 822 (2025), 702 (2026 ytd) |
| Open Research Europe | European Commission | 2,429 | **1,513** | 2021–2026 | 463 (2024), 628 (2025), 532 (2026 ytd) |
| HRB Open Research | Health Research Board (Ireland) | 1,134 | **731** | 2018–2026 | 128 (2024), 192 (2025), 115 (2026 ytd) |
| Gates Open Research | Gates Foundation | 887 | **563** | 2017–2026 | 87 (2024), **42 (2025), 25 (2026 ytd)** |
| Open Research Africa | (AAS successor) | 181 | **138** | 2019–2026 | 13 (2024), 36 (2025), 62 (2026 ytd) |
| **AAS Open Research** | African Academy of Sciences | 172 | **114** | **2018–2022** | 38 (2021), **3 (2022), then nothing** |
| **AMRC Open Research** | Assoc. of Medical Research Charities | 38 | **27** | **2019–2022** | 16 (2021), **4 (2022), then nothing** |

Three status findings, each independently probed:

- **AAS Open Research → Open Research Africa. Confirmed.** `https://aasopenresearch.org/`
  returns **HTTP 200 after a redirect to `https://openresearchafrica.org/`** (S4) [WEB],
  and the Crossref record shows AAS Open Research stopping in 2022 while Open Research
  Africa continues (S1). This was a rename/rehome, not a closure, and the successor is
  actually growing again (62 records in 2026 to date, its best year).
- **AMRC Open Research is effectively dead.** **27 distinct articles ever**, none
  registered since 2022 (S1). The site itself could not be evaluated:
  `https://amrcopenresearch.org/` returned **HTTP 403 with `cf-mitigated: challenge`,
  `server: cloudflare`** to all four user-agents tried (S4) — a bot challenge, *not* a
  404, so the site is probably still served to browsers. **The Crossref record is the
  evidence, not the HTTP status.** Same 403-challenge situation for
  `https://hrbopenresearch.org/`, which is clearly alive from its Crossref activity.
- **Gates Open Research is being superseded from inside.** Gates' own about page states
  that "**for papers submitted after August 2024, all articles are first published as
  preprints on our associated preprint server, VeriXiv**", with peer review happening on
  VeriXiv and only the final version of record landing on Gates Open Research (S3) [DOC].
  That explains the collapse from 87 records in 2024 to 42 in 2025 and 25 in 2026.
  `https://verixiv.org/` returns HTTP 200 (a 55,677-byte F1000-platform SPA shell, byte-
  identical in size to the Open Research Africa and Wellcome shells — the same software
  again) (S4) [WEB/INF].

**Assessment.** These are good platforms — open named review, CC BY, funder-paid, fast —
and Wellcome Open Research at 4,009 articles is a real body of work. But as *archives*
they are useless: the corpus of Wellcome Open Research is, by construction, "things
Wellcome paid for". And the family's durability record over eight years is one rename, one
abandonment and one internal succession out of seven instances.

## 4. PeerJ Preprints (2013–2019) — closed, content intact

- **URL:** https://peerj.com/preprints/ · Crossref prefix `10.7287`
- **Status: CLOSED to new deposits.** Crossref shows `posted-content` under `10.7287`
  running **2013–2019 and stopping dead**: 220 (2013), 730, 1,067, 1,352, 1,042, 1,297,
  **738 (2019), then zero** (S5) [API].
- **Size: 6,446 preprint DOIs → 5,068 distinct preprints** (versions are separate DOIs,
  suffix `v1`, `v2`, …) (S5) [API].

**What happened to the content — probed, and the answer is good.** All 6,446 records still
carry a Crossref landing URL of the form `https://peerj.com/preprints/<id>v<n>` (S5).
Resolution test, 2026-09-01 (S6) [WEB]:

- `https://doi.org/10.7287/peerj.preprints.27295v2` → **302 → `https://peerj.com/preprints/27295v2`**
- `https://doi.org/10.7287/peerj.preprints.1097v2` → **302 → `https://peerj.com/preprints/1097v2`**
- **Negative control:** `https://doi.org/10.7287/peerj.preprints.99999999v1` → **HTTP 404
  at doi.org**, no redirect at all. ✅ The DOI system distinguishes real from fabricated
  PeerJ preprint DOIs.

The final fetch of the real landing pages returns **HTTP 403 with `cf-mitigated: challenge`,
`server: cloudflare`** — peerj.com bot-challenges automated clients (S6). So: **the DOIs
resolve and the pages exist; only scripted access is blocked.** Treat PeerJ Preprints as a
frozen but intact archive.

**Licensing is the best in this record: essentially the whole corpus is CC BY.** 6,088 of
6,446 records carry CC BY 4.0, 325 CC BY 3.0, 30 CC0 (S5) [API].

**Why it matters to a software reader:** PeerJ Preprints is where **QIIME 2** was
announced. *"QIIME 2: Reproducible, interactive, scalable, and extensible microbiome data
science"*, `10.7287/peerj.preprints.27295v2`, posted **2018-12-03**, later *Nature
Biotechnology* 2019 (S6) [API]. One of the most-used pieces of scientific software in
microbiology has its preprint of record on a server that no longer accepts submissions.

## 5. Preprints with The Lancet (Elsevier / SSRN) — alive

- **URL:** https://www.ssrn.com/index.cfm/en/the-lancet/ · **HTTP 200**, 20,451 B,
  2026-09-01 (S7) [WEB]
- **Status: ALIVE.** I expected to find this discontinued; it is not. The page renders a
  live series with **"All Journals (25550)"** papers listed.
- **Launch year: [NOT-VERIFIED].**

Self-description, verbatim (S7) [DOC]: "a collaboration between The Lancet Group of
journals and SSRN to facilitate the open sharing of preprints for early engagement,
community comment, and collaboration. **Preprints available here are not *Lancet*
publications or necessarily under review with a *Lancet* journal.** … **The usual SSRN
checks and a *Lancet*-specific check for appropriateness and transparency have been
applied.** The findings should not be used for clinical or public health decision-making
or presented without highlighting these facts."

Two things to note. The disclaimer that a posting is not necessarily under *Lancet* review
makes this closer to a genuine open preprint server than Cell Sneak Peek (§6). And SSRN's
footer asserts "**All rights are reserved, including those for text and data mining, AI
training, and similar technologies**" (S7) — SSRN is an Elsevier property and its default
posture is restrictive, per-paper licences notwithstanding. **Do not plan on bulk TDM
here.**

*(Caveat: I report "25550" as the figure the page displayed under the heading "Preprints
with The Lancet Papers". Whether that counter is scoped to this series or to a wider SSRN
grouping is [NOT-VERIFIED].)*

## 6. Cell Press Sneak Peek (Elsevier / SSRN) — alive

- **URL:** https://www.ssrn.com/index.cfm/en/cell-press-sneak-peek/ · **HTTP 200**,
  23,986 B, 2026-09-01 (S8) [WEB]. Note `…/en/cell-sneak-peek/` and `…/en/sneak-peek/`
  both **404** — the working slug is `cell-press-sneak-peek`, and the 404 page carries the
  notice "SSRN is no longer supporting commercial products such as Research Paper Series",
  which is easy to mistake for a closure notice for this service. It is not.
- **Status: ALIVE.** **12,404 papers**, with a live per-journal breakdown.
- **Launch year: [NOT-VERIFIED].**

Self-description (S8) [DOC]: "**an author opt-in preview of the papers under review in our
primary research journals.** An invitation to submit to Sneak Peek is provided to all
authors of primary research articles at the time they are first sent for peer review."

That is the purest example of the shop-window pattern in §0: **the inclusion criterion is
"currently under review at a Cell Press journal"**. Per-journal counts as displayed
2026-09-01: Cell Reports 2,545 · Cell 778 · Cell Reports Medicine 328 · Cell Reports
Physical Science 300 · Cell Reports Methods 242 · Chem 210 · Cell Host & Microbe 203 ·
Cell Stem Cell 189 · Cell Metabolism 173 · Cell Chemical Biology 169 · Cancer Cell 144 ·
Cell Systems 126 · Cell Genomics 66 · Cell Biomaterials 3 · Chem Catalysis 0 · Cell
Reports Sustainability 0 (S8).

**Assessment:** useful for one narrow purpose — seeing a specific paper months before Cell
publishes it — and useless for anything else. Not an archive, not comprehensive, and the
selection is doubly filtered (Cell Press sent it for review *and* the author opted in).

## 7. Nature Precedings (2007–2012) — defunct, but the content survived

**The cautionary tale of this group, and the good news is better than expected.**

- **Original host is gone.** `https://precedings.nature.com/` and
  `http://precedings.nature.com/`: DNS resolves (192.129.25.40) but **both ports refuse
  the connection** — `curl: (7) Failed to connect … Could not connect to server`,
  2026-09-01 (S9) [WEB]. A live DNS record pointing at a dead host is the worst
  combination: link checkers see a name that resolves, users see nothing.
- **The content is alive at a different URL.** `https://www.nature.com/npre` returns
  **HTTP 200, 126,578 B**, headed *"Welcome to Nature Precedings — Pre-publication
  research and preliminary findings for the Life Science community **from 2007 until
  2012**"*, with a browsable, dated article listing (S9) [WEB].
- **Size: 3,449 records** — 2,837 "Research" plus 612 "Multimedia" — from the
  nature.com search facet `journal=npre`, 2026-09-01 (S9) [WEB].
- **DOIs still resolve.** `https://doi.org/10.1038/npre.2012.7027.1` → **HTTP 200** at
  `https://www.nature.com/articles/npre.2012.7027.1` (S9) [WEB].
  **Negative control:** `https://doi.org/10.1038/npre.1999.99999.1` → **HTTP 404 at
  doi.org**. ✅

**The lesson.** Nature Publishing Group shut a preprint server after five years — this is
the canonical case of a major publisher closing one — and yet, fourteen years on, every
citation to a Precedings DOI still lands on the paper. What broke was the *hostname*.
What held was the *DOI* plus the publisher's willingness to keep serving the objects under
its main domain. If you are choosing where to deposit, note carefully which of those two
things you are actually relying on. Note also the asymmetry of luck: Nature is still in
business. A publisher that had folded would have taken the content with it.

Content skews to 2007–2012 life science, and includes instrumentation work — the
2012-04-04 listing alone includes *"A novel apparatus/protocol designed for optogenetic
manipulation and recording of individual neurons during a motivation and working memory
task in the rodent"* (S9).

## 8. JMIR Preprints (JMIR Publications)

- **URL:** https://preprints.jmir.org/ · **HTTP 200**, 2,113,332 B, 2026-09-01 (S4) [WEB]
- **Status: ALIVE and, by volume, the largest thing in this record.**
- **Size: 41,766 `posted-content` DOIs under prefix `10.2196`**, 2013–2026 (S10) [API].
  Yearly: 1 (2013), 1, 5, 48, 1,235 (2017), 2,599, 2,663, **5,634 (2020)**, 5,024, 4,653,
  5,564, 5,354, 5,437 (2025), 3,548 (2026 ytd).
- **Launch year:** JMIR's own claim is **2009**; Crossref shows essentially nothing before
  2016 and the service only becomes substantial in **2017**. Report the discrepancy rather
  than resolving it — **the 2009 date is [NOT-VERIFIED]**, and a 2016/2017 effective start
  is what the DOI record supports [INF].

**The model:** JMIR Preprints is the *open-peer-review-of-submissions* variant. Manuscripts
submitted to a JMIR journal are, at the author's option, posted immediately as preprints
and opened to public review while the formal editorial process runs. So it sits between
Cell Sneak Peek (pure preview, no public review) and F1000Research (publish-then-review as
the actual publication route): the preprint is a real, citable, DOI'd object that anyone
can review, but the journal decision is still made conventionally behind it.

**Assessment.** The volume is startling — roughly 5,000/year, comparable to medRxiv — but
remember what it is: **the submission stream of one publisher's journal portfolio**, in
one field (digital health / medical informatics). It is not a field-wide archive. Within
digital health it is close to comprehensive for JMIR-bound work and worth searching. The
41,766 figure should not be compared with bioRxiv's 347,954 as though they measured the
same thing.

## 9. ARPHA Preprints (Pensoft)

- **URL:** https://preprints.arphahub.com/ · **HTTP 200**, 91,498 B, 2026-09-01 (S4) [WEB]
- **Operator:** **Pensoft Publishers**, on its own ARPHA publishing platform.
- **Launched 2020** (first Crossref `posted-content` records under `10.3897`: 16 in 2020).
- **Status: ALIVE and growing**: 119 (2021), 158, 193, 185, **221 (2025)**, 166 (2026 ytd);
  **1,058 total** (S10) [API].
- **Licence:** the site states content is under **CC BY 4.0** (S4) [WEB].

**Gate:** limited to manuscripts being submitted to ARPHA/Pensoft journals — the same
publisher-tied pattern. Content reflects Pensoft's specialisms: biodiversity, taxonomy,
ecology, natural-history collections and their data infrastructure. The front page on
2026-09-01 was showing, among others, *"From collection trays to AI-ready data: An
operational framework…"* and EU-project deliverables *"D3.1 Availability of image & sound
datasets for training…"* and *"D5.1 Strategy for establishing a European-wide
consortium…"* (S4). That last pair is worth noting: **ARPHA Preprints is used as a
citable home for EU project deliverables**, which is a genuinely useful niche and not
something bioRxiv would accept.

**Assessment:** small, healthy, narrow. Relevant to this knowledge base only for
biodiversity-informatics data infrastructure.

## 10. Beilstein Archives (Beilstein-Institut)

- **URL:** https://www.beilstein-archives.org/ → 200 at `/xiv/`, 85,673 B, 2026-09-01
  (S4) [WEB]
- **Operator:** the **Beilstein-Institut**, a German non-profit foundation; the same body
  that publishes the *Beilstein Journal of Organic Chemistry* and *Beilstein Journal of
  Nanotechnology*, both fully open access and free to authors.
- **Launched 2019.** **Size: 726 preprints** (Crossref `posted-content` under prefix
  `10.3762`) (S10) [API].
- **Status: ALIVE but shrinking** — 161 (2019), 145, 93, 92, 68, 73, **66 (2025)**, 28
  (2026 ytd). The trend is down by roughly 60 % from its first year.

**Gate:** deposits are limited to manuscripts submitted to a Beilstein journal. Subject
areas advertised on the site include **Nanotechnology**, organic chemistry, bioorganic
chemistry/chemical biology, catalysis and supramolecular chemistry (S4).

**Relevance:** the Nanotechnology stream is the only part likely to matter here — SPM,
nanofabrication, self-assembly, surface chemistry. But at ~70 deposits a year across all
subjects, expect a handful of relevant items annually. See [chemrxiv.md](chemrxiv.md) for
the large chemistry server, and [ecsarxiv.md](ecsarxiv.md) for the electrochemistry one.

## 11. agriRxiv — the domain is dead, the service moved

The most instructive failure in this record, because the two halves came apart.

- **`https://agrirxiv.org/` times out** (connection timed out after 30 s, 2026-09-01).
  `http://agrirxiv.org/` redirects to `https://www.agrirxiv.org/`, which returns **HTTP
  200, 2,963 bytes** — and the body is a **Namecheap domain-parking page**: *"has been
  recently registered with namecheap.com … Want a domain name like this? Discover domains
  on auction now."* DNS confirms it: `www.agrirxiv.org` resolves to
  `parkingpage.namecheap.com` (S11) [WEB]. **The agriRxiv domain has lapsed and been
  re-registered by a parking service.**
- **But the DOIs are fine.** Crossref prefix `10.31220` (CABI) holds **1,054 records**,
  1,051 of them `posted-content`, spanning **2017–2026 and still receiving deposits**: 10
  (2017), 230 (2018), 190, 178, 88, 46, 58, 71, **94 (2025), 89 (2026 ytd)** (S12) [API].
- **Two hosting eras, visible in the DOI suffixes** (S12) [API]:
  - **2017–~2020: OSF Preprints.** Records like `10.31220/osf.io/k6d8f` with landing URL
    `https://osf.io/k6d8f` — agriRxiv began as a white-labelled OSF Preprints instance,
    like [ECSarXiv](ecsarxiv.md).
  - **~2021–present: CABI Digital Library.** Records like
    `10.31220/agriRxiv.2024.00270` with landing URL
    `http://www.cabidigitallibrary.org/doi/10.31220/agriRxiv.2024.00270`.
- **Resolution test:** `https://doi.org/10.31220/agriRxiv.2021.00061` → redirects to
  `https://www.cabidigitallibrary.org/doi/10.31220/agriRxiv.2021.00061`, which returns
  **403 with a Cloudflare challenge** (S12) [WEB] — same bot-challenge situation as PeerJ;
  the record exists, scripted access is blocked.

So: **agriRxiv is not dead, but every human-facing entry point to it is broken.** The
brand domain is a parking page, the OSF-era landing pages are orphaned from the current
service, and the current host bot-challenges. Anyone Googling "agriRxiv" in 2026 lands on
a domain auction. This is a governance failure, not a technical one — nobody renewed the
domain. **The DOIs saved it, again.**

*(Operator note: the brief lists agriRxiv as CABI + Open Access India, 2017. The 2017 start
and CABI's DOI prefix are confirmed (S12); the Open Access India co-founding role is
**[NOT-VERIFIED]** here.)*

## 12. Sources

- **S1** Crossref REST API, prefix `10.12688` — full cursor pagination of all 33,289
  records (`select=DOI,container-title,license,type`) plus `container-title` and
  `published` facets · retrieved **2026-09-01** · per-platform record and distinct-article
  counts, activity windows, licence distribution; prefix registered to **"F1000 Research
  Ltd"**, Crossref member 2560. Log:
  `scratch/preprint-repositories/lifesci/f1000-scan.txt`. [API]
- **S2** https://f1000research.com/about (How It Works) · retrieved 2026-09-01 ·
  publishing model, "no Editor (or Editor-in-Chief)…", the three reviewer statuses and
  their verbatim definitions, versioning policy, the two-Approved indexing threshold and
  the list of indexes, scope statement, posters/slides exclusion. [DOC]
- **S3** https://gatesopenresearch.org/about · retrieved 2026-09-01 · the Gates-grant
  eligibility rule; the August-2024 switch to first-publication on **VeriXiv**; CC BY
  statement. [DOC]
- **S4** Live reachability probes, 2026-09-01, Chrome-131 UA unless noted:
  `f1000research.com` 200/114,761 · `wellcomeopenresearch.org` 200/56,615 ·
  `gatesopenresearch.org` 200/111,640 · `aasopenresearch.org` **200 after 301 →
  openresearchafrica.org**/55,677 · `openresearchafrica.org` 200/55,677 ·
  `verixiv.org` 200/55,677 · `amrcopenresearch.org` **403** (also 403 to
  `curl/8.5.0`, `WhatsApp/2.23.20.0`, ClaudeBot) · `hrbopenresearch.org` **403** (same
  four UAs) · `preprints.jmir.org` 200/2,113,332 · `preprints.arphahub.com` 200/91,498 ·
  `beilstein-archives.org` 200 → `/xiv/` /85,673. Response headers for the 403s:
  `server: cloudflare`, `cf-mitigated: challenge`. [WEB]
- **S5** Crossref REST API, prefix `10.7287`, `filter=type:posted-content`, full
  pagination of 6,446 records · retrieved 2026-09-01 · 5,068 distinct base DOIs, year
  distribution 2013–2019, landing-URL shape, licence distribution. [API]
- **S6** DOI resolution probes 2026-09-01: `10.7287/peerj.preprints.27295v2` and
  `…1097v2` → 302 to `peerj.com/preprints/…` then 403 Cloudflare challenge;
  `10.7287/peerj.preprints.99999999v1` → **404 at doi.org** (negative control). Crossref
  record for `10.7287/peerj.preprints.27295v2`: type `posted-content`, title "QIIME 2:
  Reproducible, interactive, scalable, and extensible microbiome data science", posted
  2018-12-03. [API/WEB]
- **S7** https://www.ssrn.com/index.cfm/en/the-lancet/ · retrieved 2026-09-01 · HTTP 200,
  20,451 B · self-description quoted in §5; "All Journals (25550)"; the Elsevier
  all-rights-reserved / no-TDM footer. [WEB/DOC]
- **S8** https://www.ssrn.com/index.cfm/en/cell-press-sneak-peek/ · retrieved 2026-09-01 ·
  HTTP 200, 23,986 B · self-description quoted in §6; "All Journals (12404)" and the
  per-journal breakdown. Also probed `…/en/cell-sneak-peek/` and `…/en/sneak-peek/`, both
  **404** with the "SSRN is no longer supporting commercial products" text. [WEB/DOC]
- **S9** Nature Precedings probes, 2026-09-01: `precedings.nature.com` — DNS resolves to
  192.129.25.40, **connection refused on both 80 and 443**; `https://www.nature.com/npre`
  — HTTP 200, 126,578 B, "from 2007 until 2012"; `https://www.nature.com/search?journal=npre`
  — facet "Nature Precedings (3449)", "Showing 1–50 of 3449 results", article types
  Research 2,837 / Multimedia 612; `https://doi.org/10.1038/npre.2012.7027.1` → 200 at
  `nature.com/articles/npre.2012.7027.1`; `https://doi.org/10.1038/npre.1999.99999.1` →
  **404 at doi.org** (negative control). [WEB]
- **S10** Crossref REST API, `filter=type:posted-content` with `published` facet on
  prefixes `10.2196` (JMIR, 41,766), `10.3897` (Pensoft/ARPHA, 1,058) and `10.3762`
  (Beilstein, 726) · retrieved 2026-09-01. [API]
- **S11** agriRxiv domain probes, 2026-09-01: `https://agrirxiv.org/` connection timeout;
  `http://agrirxiv.org/` → 200 at `https://www.agrirxiv.org/`, 2,963 B, Namecheap parking
  page; `getent hosts www.agrirxiv.org` → `parkingpage.namecheap.com`. [WEB]
- **S12** Crossref REST API, prefix `10.31220` · retrieved 2026-09-01 · 1,054 records
  (1,051 `posted-content`, 3 `journal-article`), year distribution 2017–2026, the two DOI
  suffix families (`10.31220/osf.io/<id>` → `osf.io`, `10.31220/agriRxiv.<year>.<n>` →
  `cabidigitallibrary.org`); plus DOI-resolution probe of
  `10.31220/agriRxiv.2021.00061` → CABI Digital Library, 403 Cloudflare challenge. [API/WEB]

### Not verified

- **F1000Research's corporate parent.** Crossref says "F1000 Research Ltd" (S1). The
  Taylor & Francis / Informa acquisition is not stated on any page I retrieved.
- **Launch years for Preprints with The Lancet and Cell Press Sneak Peek.**
- **JMIR Preprints' claimed 2009 launch** — the Crossref record supports 2016/2017 as the
  effective start (§8).
- **Whether SSRN's "25550" counter is scoped to Preprints with The Lancet** or to a wider
  grouping (§5).
- **Open Access India's role in agriRxiv** (§11).
- **Whether `amrcopenresearch.org` and `hrbopenresearch.org` render for a real browser** —
  both returned Cloudflare challenges to every automated client tried (S4). The
  alive/dead calls for those two rest on Crossref activity, not on HTTP status.
- **VeriXiv's size, launch date and exact relationship to Gates Open Research** beyond the
  August-2024 statement in S3.
- **Eligibility-gate wording for Wellcome, HRB, AMRC and Open Research Africa** — those
  About pages are JavaScript-rendered SPA shells and returned no readable policy text to
  a scripted fetch. The Gates wording (S3) is quoted as representative of the family;
  that generalisation is **[INF]**.
- **Whether any of these platforms publishes a preprint-to-publication rate.** None found.
