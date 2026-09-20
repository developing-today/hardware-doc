# HAL (Hyper Articles en Ligne) — preprint repository record

- **URL:** https://hal.science/ · API `https://api.archives-ouvertes.fr/search/`
- **Operator:** Centre pour la communication scientifique directe (CCSD), a CNRS service unit
  (CNRS / INRIA / Université de Lyon). Funded as French public research infrastructure. (S1)
- **Discipline scope:** all disciplines — *as actually used*, dominated by SHS (humanities and
  social sciences) and life sciences by volume, but with a large and internationally important
  computer-science and engineering core (S2)
- **Launched:** see §3 — the "2001" date is **contested**; CCSD's own page attributes 2001 to
  **TEL/HAL theses**, and HAL's OAI-PMH `earliestDatestamp` is **2002-09-23** (S3, S4)
- **Status:** active (heavy daily deposit traffic observed 2026-09-01)
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What it is

HAL is France's **national open archive**. It is not a preprint server in the arXiv sense and
reading it as one will mislead you. HAL is a deposit-and-dissemination platform for the *whole*
output of French public research: journal articles (usually author-accepted manuscripts),
conference papers, book chapters, monographs, theses, habilitations, technical/research reports,
patents, software, images and video. A large fraction of its records are **bibliographic notices
with no file attached at all** (§3).

For an anglophone engineer the important consequence is this: **a great deal of foundational
French computer-science work was published as an INRIA *research report* and deposited in HAL,
and never went to arXiv.** If you search only arXiv you will miss it. The INRIA research-report
series (`RR-NNNN`, `RT-NNNN`) is the closest French equivalent to a preprint series, and it is
archived in HAL with stable identifiers and full text.

HAL is operated by the CCSD, a CNRS unit. It is multi-tenant: institutions run **portals**
(`inria.hal.science`, `cea.hal.science`, `theses.hal.science`, …) that are views onto one shared
database, not separate repositories. A document deposited through the INRIA portal is the same
record as the one on `hal.science`, with the same identifier. (S1, S5)

## 2. Scope and subject taxonomy

HAL's domain codes are exposed in the API as `domainAllCode_s`. **Note the schema trap:** the
field is `domainAllCode_s`, *not* `domain_s`; querying `domain_s:info` returns
`numFound: 0` and will silently give you a wrong answer (verified 2026-09-01, [API]).

Top-level domains, whole archive, 2026-09-01 [API] (S2):

| Code | Domain | Records |
|---|---|---|
| `shs` | Humanities & social sciences | 483,057 |
| `sdv` | Life sciences | 420,391 |
| `sde` | Environmental sciences | 152,084 |
| `info` | **Computer science** | **125,067** |
| `spi` | **Engineering sciences** | **120,084** |
| `chim` | Chemistry | 93,930 |
| `phys` | Physics | 84,694 |
| `math` | Mathematics | 53,470 |

**Caveat, and it is a large one:** these facet counts sum to roughly 1.5M against a total of
4,648,085 records. The majority of HAL records carry **no domain code at all**. Domain-filtered
counts are therefore *lower bounds*, not shares. [API] [INF]

Computing subdomains (`info.*`), 2026-09-01 [API] (S2) — the ones a systems/electronics reader
cares about:

| Code | Area | Records |
|---|---|---|
| `info.info-ai` | Artificial intelligence | 42,722 |
| `info.info-im` | Medical imaging | 41,425 |
| `info.info-mo` | Modelling & simulation | 28,635 |
| `info.info-ts` | Signal & image processing | 27,860 |
| `info.info-ni` | Networking & internet architecture | 26,054 |
| `info.info-oh` | Other computer science | 19,048 |
| `info.info-lg` | Machine learning | 15,198 |
| `info.info-ro` | Robotics | 13,517 |
| **`info.info-dc`** | **Distributed, parallel & cluster computing** | **13,058** |
| `info.info-hc` | Human–computer interaction | 12,930 |
| `info.info-cr` | Cryptography & security | 11,969 |
| `info.info-se` | Software engineering | 11,145 |
| `info.info-au` | Automatic control | 10,858 |
| `info.info-rb` | Robotics (alt.) | 10,348 |
| `info.info-lo` | Logic in computer science | 8,380 |
| `info.info-db` | Databases | 8,098 |
| `info.info-es` | Embedded systems | 7,528 |
| `info.info-ar` | Hardware architecture | 5,554 |
| `info.info-pl` | Programming languages | 5,281 |

Engineering subdomains (`spi.*`) relevant to electronics, 2026-09-01 [API] (S2):
`spi.signal` 37,799 · `spi.mat` 36,710 · `spi.nano` 31,954 · `spi.auto` 31,875 ·
`spi.nrj` 23,719 · `spi.opti` 20,789 · **`spi.tron` (electronics) 20,471** ·
`spi.elec` 16,946 · `spi.acou` 13,532.

## 3. Size and growth

All figures retrieved **2026-09-01** from the Solr-style search API, `rows=0`, reading
`response.numFound` (S2).

- **Total records: 4,648,085** — `?q=*:*&rows=0&wt=json` [API]

Document-type breakdown (`docType_s` facet), top of list [API]:

| Type | Meaning | Count |
|---|---|---|
| `ART` | Journal article | 2,237,436 |
| `COMM` | Conference paper | 1,056,763 |
| `COUV` | Book chapter | 410,247 |
| `THESE` | Doctoral thesis | 188,835 |
| `OUV` | Book | 125,591 |
| `MEM` | Student dissertation | 96,645 |
| `UNDEFINED` | — | 93,551 |
| `POSTER` | Poster | 82,398 |
| `OTHER` | Other | 80,914 |
| **`REPORT`** | **Research/technical report** | **80,046** |
| `HDR` | Habilitation | 10,356 |
| `PATENT` | Patent / software registration | 8,742 |
| `SOFTWARE` | Software | 2,119 |

(The facet sums to 4,648,030 against `numFound` 4,648,085 — a 55-record discrepancy, i.e. a
handful of records carry no `docType_s`. [API] [INF])

**Full text vs. notice** — the single most important number in this record
(`submitType_s` facet) [API]:

| `submitType_s` | Count | Share |
|---|---|---|
| `notice` (metadata only, **no file**) | 2,827,378 | ~60.8% |
| `file` (full text deposited) | 1,788,688 | ~38.5% |
| `annex` | 32,019 | ~0.7% |

**Roughly three fifths of HAL is a bibliographic catalogue, not a document archive.** Within
computer science the ratio is better but still only about half: `domainAllCode_s:info AND
submitType_s:file` = **62,573** of 125,067 (~50.0%) [API].

Computer-science cross-cuts, 2026-09-01 [API]:
`info AND COMM` = 71,428 · `info AND THESE` = 2,958 · `info AND REPORT` = 2,927 ·
`info AND SOFTWARE` = 479.

Language mix (`language_s` facet) [API] — note English *outnumbers* French:
`en` 2,696,159 · `fr` 1,791,359 · `und` 73,958 · `es` 31,864 · `it` 18,475 · `de` 12,080 ·
`pt` 9,597 · `ru` 2,518.

**Age.** OAI-PMH `Identify` reports `earliestDatestamp` **2002-09-23** (S4) [API]. CCSD's own
HAL page says "Créée en 2001, HAL theses (anciennement TEL)…" — that 2001 refers to **TEL**, the
theses archive, not to HAL itself (S3) [DOC]. The widely repeated "HAL since 2001" claim is
therefore **not confirmed by a primary source in this pass** — recorded as a conflict, not
resolved. [NOT-VERIFIED]

## 4. Screening and moderation — what gets in

HAL **does** moderate, and CCSD publishes what the check is. Verbatim from CCSD's own
documentation (S5) [DOC]:

> « Depuis la création de HAL, on appelle « modération » l'étape de vérification d'un dépôt avant
> sa mise en ligne : **seuls les dépôts avec un fichier sont vérifiés.** Les références
> bibliographiques sont quant à elles mises en ligne immédiatement. »
>
> « Cette étape garantit que les fichiers et les métadonnées qui les décrivent, librement
> accessibles sur internet, sont exploitables par tout utilisateur. L'utilisateur doit, en effet,
> pouvoir **ouvrir et/ou télécharger le fichier, lire le texte intégral** du document déposé,
> **l'utiliser dans le respect de la propriété intellectuelle** et disposer des **informations
> bibliographiques exactes**. »

So the gate is, precisely:

1. **Only file deposits are moderated.** Metadata-only notices go online immediately, unchecked.
2. The check is **completeness and usability**: does the PDF open, is it the full text, are the
   bibliographic metadata correct, are the intellectual-property terms respected (i.e. is the
   depositor allowed to post this version).
3. **It is explicitly not peer review**, and it is not a scientific-merit judgement. The published
   criteria say nothing about whether the result is correct or novel.

Affiliation matters operationally rather than as an admission gate: HAL runs automatic affiliation
matching and portal administrators "patrol" their portal's deposits (S5) [DOC]. Deposit is open to
researchers generally; an author who defended a thesis at any university may deposit to HAL theses
(S3) [DOC].

**A claim I could not confirm:** that deposit in HAL is *mandatory* for French public research.
Institutional and funder mandates of varying force are widely described, but I did not locate a
primary CCSD or ministerial document establishing a general legal deposit obligation in this pass.
**[NOT-VERIFIED]** — treat "mandatory-ish" as folklore until sourced.

## 5. Reliability — what you can and cannot trust

What a HAL deposit **does** guarantee:

- A **stable identifier and a timestamped, immutable version** (`v1`, `v2`, …). Old versions stay
  reachable; they are not overwritten. Verified: `inria-00609399v1` → HTTP 200 (104,253 B) and
  `v2` → HTTP 200 (106,610 B), both live, while `v9` → HTTP 404 (S6) [WEB].
- For file deposits, that a human confirmed the PDF opens and the metadata match it (§4).
- Long-term hosting by a CNRS national infrastructure — institutionally about as durable as
  scholarly hosting gets outside arXiv.

What it **does not** guarantee:

- **Nothing about correctness.** No peer review, no scientific-scope screen on merit.
- **Nothing about whether it is a preprint.** A HAL record is more often a *postprint* — the
  accepted manuscript of an already-published paper. `ART` (2.2M) dwarfs `REPORT` (80k). If you
  need to know whether the HAL copy preceded the journal, you must check the record's version
  dates and the `citationRef_s` field yourself.
- **Nothing about full text existing.** ~61% of records are notices (§3). A `hal-` identifier in a
  citation is *not* a promise that you can read the paper.

How to sanity-check a single HAL record: hit
`https://api.archives-ouvertes.fr/search/?q=halId_s:<id>&fl=*&wt=json` and read `submitType_s`
(is there a file?), `version_i` (how many revisions?), `docType_s` (report or postprint?) and
`citationRef_s` (which venue, if any). The `fileMain_s` field gives the canonical PDF URL, which
follows the pattern `https://<portal>.hal.science/<halId>/document`.

## 6. What you actually find there — examples

- **INRIA research reports** — the real prize. `RR-`/`RT-` numbered technical reports, full text,
  often the *first* public form of work that later appeared at a conference. Example:
  `inria-00069994`, *The Coq Proof Assistant, Reference Manual, Version 5.10*, RT-0177, INRIA,
  **1995** (S7) [API].
- **Theses** via `theses.hal.science` (formerly TEL): 188,835 `THESE` records archive-wide, 2,958
  in computer science [API].
- **Software and formal-methods artefacts**, including software registered through the French IDDN
  scheme and filed under `docType_s:PATENT` — e.g. `hal-03136256`, *Why3 version 1.0*, IDDN
  reference `IDDN.FR.001.420003.000.S.P.2019.000.20600` (S7) [API]. This is a HAL-specific quirk
  worth knowing: **software registrations show up as `PATENT`, not `SOFTWARE`.**
- **CEA-Leti / CEA work** under the `cea-` prefix (19,582 records) — e.g. `cea-05312386`,
  *Typestates specification and verification in Frama-C*, FormaliSE 2025 (S7) [API].
- **LIRMM** robotics and microelectronics under `lirmm-` (8,984 records) — e.g. `lirmm-00798676`,
  Mansard, Khatib & Kheddar, *A unified approach to integrate unilateral constraints in the stack
  of tasks*, IEEE Transactions on Robotics, 2009 (S7) [API].
- **LAAS-CNRS humanoid robotics** — the "Stack of Tasks" line, e.g. `hal-00600959` and
  `hal-00738243`, both IEEE-RAS Humanoids papers (2011, 2012) (S7) [API].

## 7. Landmark papers (software · distributed systems · databases · electronics · security)

Every row below was confirmed by direct API lookup on **2026-09-01** (S7) [API]. `Preprint first?`
is answered conservatively; where I could not establish deposit-versus-publication ordering from
the API fields available, I say so rather than guess.

| Paper | Identifier | Year | Why it matters | Preprint first? |
|---|---|---|---|---|
| Shapiro, Preguiça, Baquero, Zawirski, *A comprehensive study of Convergent and Commutative Replicated Data Types* | `inria-00555588` v1 · [link](https://inria.hal.science/inria-00555588v1) | 2011 | **The** CRDT reference text. INRIA Research Report **RR-7506**, 50 pp. Foundation of every modern eventually-consistent store, Automerge/Yjs, collaborative editors | Yes — research report, `docType_s:REPORT`; predates the Oct 2011 SSS paper [INF] |
| Shapiro, Preguiça, Baquero, Zawirski, *Conflict-free Replicated Data Types* | `inria-00609399` v2 · [link](https://inria.hal.science/inria-00609399v2) | 2011 | INRIA **RR-7687**, 18 pp. The condensed statement of the CRDT result | Yes — report form [INF] |
| Shapiro, Preguiça, Baquero, Zawirski, *Conflict-free Replicated Data Types* (SSS 2011) | `hal-00932836` v1 · [link](https://inria.hal.science/hal-00932836v1) | 2011 | The peer-reviewed SSS 2011 (Grenoble) paper — the canonical citation | No — this is the conference version; deposit date not verified [NOT-VERIFIED] |
| Preguiça, Baquero, Shapiro, *Conflict-free Replicated Data Types (CRDTs)* | `hal-01793586` v1 | 2019 | Encyclopedia of Big Data Technologies entry; the readable modern summary | No — book chapter |
| Leroy, *Formal verification of a realistic compiler* | `inria-00415861` v1 · [link](https://inria.hal.science/inria-00415861v1) | 2009 | **CompCert.** CACM 52(7):107–115. Proof that an optimising C compiler can be machine-verified | No — `ART`, mirrors CACM [INF] |
| Leroy, *A formally verified compiler back-end* | `inria-00360768` v3 | 2009 | The full CompCert back-end paper, J. Automated Reasoning 43(4):363–446 | No — `ART`; 3 versions on HAL |
| Cornes, Courant, Filliâtre, Huet, Manoury et al., *The Coq Proof Assistant, Reference Manual, Version 5.10* | `inria-00069994` v1 | **1995** | Primary-source Coq documentation, INRIA **RT-0177**. Underpins CompCert, Iris, seL4-adjacent work | Yes — INRIA report, no journal version |
| Barras, Boutin, Cornes, Courant, Filliâtre et al., *The Coq Proof Assistant Reference Manual: Version 6.1* | `inria-00069968` v1 | 1997 | INRIA **RT-0203**; the Coq 6.x lineage | Yes — INRIA report |
| Pedregosa, Varoquaux, Gramfort, Michel, Thirion et al., *Scikit-learn: Machine Learning in Python* | `hal-00650905` v2 · [link](https://inria.hal.science/hal-00650905) | 2011 | JMLR. One of the most-cited software papers in existence; INRIA Parietal origin | No — `ART`, mirrors JMLR [INF] |
| Duprat, Moya Lamiel, Kirchner, Correnson, Delmas, *Spreading Static Analysis with Frama-C in Industrial Contexts* | `hal-01260276` v1 | 2016 | ERTS 2016. Frama-C in real embedded/avionics practice | No — conference paper |
| Patte, Prevosto, *Typestates specification and verification in Frama-C* | `cea-05312386` v1 | 2025 | Current CEA formal-methods work; shows the `cea-` portal is live | No — FormaliSE 2025 |
| Filliâtre, Paskevich, Melquiond, Marché, Bobot, *Why3 version 1.0* | `hal-03136256` v1 | 2018 | Deductive program verification platform, filed as an IDDN software registration | n/a — software registration |
| Mansard, Khatib, Kheddar, *A unified approach to integrate unilateral constraints in the stack of tasks* | `lirmm-00798676` v1 | 2009 | IEEE Trans. Robotics. Whole-body control; ancestor of modern ROS-adjacent task-priority stacks | No — `ART` |
| Ramos Ponce, Saab, Hak, Mansard, *Dynamic Motion Capture and Edition using a Stack of Tasks* | `hal-00600959` v1 | 2011 | IEEE-RAS Humanoids 2011, LAAS-CNRS | No — conference paper |

**Searched for and NOT found**, recorded so the next reader does not repeat the work:
`title_t:"Pinocchio"` restricted to `domainAllCode_s:info` returned `numFound: 0` on 2026-09-01
[API]. The LAAS *Pinocchio* rigid-body-dynamics library may be in HAL under a different title
form; **not verified** here — do not cite it from this record.

## 8. Access, APIs and bulk retrieval

All probed **2026-09-01** with **default curl UA — no user-agent substitution was needed anywhere
on `*.hal.science` or `*.archives-ouvertes.fr`.** [API] [WEB]

- **Search API (Solr-style):** `https://api.archives-ouvertes.fr/search/`
  Parameters behave like Solr: `q`, `rows`, `wt=json`, `fl`, `facet=true`, `facet.field`,
  `facet.prefix`, `sort`. `rows=0` + `response.numFound` is the counting idiom. Field schema is
  published at `https://api.archives-ouvertes.fr/docs/search/schema/fields` (HTTP 200, 631,727 B)
  (S8). No authentication, no rate-limit refusal encountered across ~60 queries.
- **OAI-PMH:** `http://api.archives-ouvertes.fr/oai/hal/` — `Identify` returns
  `repositoryName: HAL`, `earliestDatestamp: 2002-09-23`, `granularity: YYYY-MM-DD`,
  `deletedRecord: no`. Metadata formats: `oai_dc`, `oai_dcterms`, `oai_openaire`, `oai_datacite`,
  `xml-tei` (S4) [API]. The TEI format is unusually rich for a repository and is the one to use
  for structured harvesting.
- **SWORD deposit:** documented at `https://api.archives-ouvertes.fr/docs/sword` (HTTP 200,
  31,139 B, title "Import SWORD") (S8) [WEB]. Endpoint *documentation* verified to exist; I did
  not attempt an authenticated deposit. Behaviour **[NOT-VERIFIED]**.
- **X2HAL** bulk import from BibTeX is documented (S5) [DOC].
- **TripleStore / SPARQL** is listed in CCSD's documentation navigation (S5) [DOC]; endpoint not
  probed. **[NOT-VERIFIED]**

**arXiv bridge — verified, and it is one-directional.** CCSD documents a
**HAL → arXiv transfer** (S9) [DOC]. Verbatim conditions: offered only if the deposit has files;
the document type is arXiv-compatible ("all HAL types except: patent, thesis, HDR, image, video,
map, audio"); no arXiv identifier already in the metadata for a v1. The submission must have an
English abstract, a chosen domain that is an **arXiv sub**domain (a root domain is rejected), each
file < 3 MB and ≤ 10 MB total, and LaTeX sources (plus `.bbl`) if the PDF was LaTeX-generated.
And critically: *"The transfer is carried out when the deposit is put online in HAL. The repository
is then moderated by the teams of arXiv before it is put online on the archive."*
**The reverse direction (arXiv → HAL as an automatic bridge) was not confirmed.** HAL records
*store* arXiv identifiers (S10), and X2HAL imports bibliographic data, but I found no documented
automatic arXiv-to-HAL push. **[NOT-VERIFIED]**

**Negative controls** (all 2026-09-01) — these matter because HTTP 200 proves nothing:

| Probe | Result | Reading |
|---|---|---|
| `q=halId_s:hal-99999999` | `numFound: 0` | API does not invent hits |
| `q=domainAllCode_s:zzzz` | `numFound: 0` | Bogus facet value returns empty, not everything |
| `q=domain_s:info` (**wrong field**) | `numFound: 0` | Silent wrong answer — the schema trap of §2 |
| `https://hal.science/hal-99999999` | HTTP **404** (47,875 B) | Bogus record 404s properly |
| `https://hal.science/inria-00555588` | HTTP **200** (91,062 B) | Real record resolves |
| `https://inria.hal.science/inria-00609399v9` | HTTP **404** | Bogus *version* 404s |
| `https://inria.hal.science/inria-00555588v1/file/RR-7506.pdf` | HTTP **404** | **Guessed** PDF filenames fail — use `fileMain_s` from the API, not a constructed path |

Identifier-prefix census via `halId_s:<prefix>*` wildcard, 2026-09-01 [API] (S2):
`hal-` 3,621,611 · `tel-` 193,911 · `in2p3-` 47,493 · `medihal-` 42,038 · **`inria-` 29,882** ·
**`cea-` 19,582** · **`lirmm-` 8,984** · `pastel-` 3,720 · `sic_` 2,571 · `ijn_` 1,147 ·
`hprints-` 390 · **`irisa-` 0**.

> **Correction to a common assumption:** there is **no `irisa-` identifier prefix** — the wildcard
> returns 0. IRISA work is present in HAL, but under `hal-` and portal collections, not a legacy
> prefix. Do not cite an `irisa-` ID. [API]

## 9. Identifiers, versioning and legacy prefixes

- Current form: **`hal-NNNNNNNN`** (8 digits), resolving at `https://hal.science/hal-NNNNNNNN`.
- **Versions are part of the identifier**: `hal-XXXXXXXXv1`, `v2`, … Every version stays
  addressable and byte-distinct (§5). Citing without a version number resolves to the latest.
- **Legacy prefixes** are permanent, not rewritten. `inria-`, `lirmm-`, `cea-`, `in2p3-`,
  `pastel-`, `sic_`, `ijn_`, `hprints-`, `medihal-` are historical deposit-channel prefixes that
  remain the record's canonical ID forever. This is why the CRDT paper is **`inria-00555588`** and
  not a `hal-` number — and why searching only for `hal-*` misses INRIA's back catalogue.
- **`tel-`** (193,911 records) is the theses archive. `tel.archives-ouvertes.fr` now **redirects to
  `https://theses.hal.science/`** (verified, HTTP 200 after redirect, 2026-09-01) (S6) [WEB].
- **Portal subdomains** (`inria.hal.science`, `cea.hal.science`) serve the same record; the API's
  `uri_s` field tells you the canonical portal URL.
- HAL also stores **external** identifiers alongside its own: DOI, arXiv ID, PMID, PMCID,
  **SWHID (Software Heritage)**, PPN (Sudoc), ADS bibcode, and bioRxiv/medRxiv/ChemRxiv DOIs
  (S10) [DOC]. The SWHID linkage is genuinely useful for software-artefact provenance.

## 10. Licensing and reuse

- **Authors choose the file licence** at deposit time; HAL presents a licence selector, and the
  licence is a first-class metadata field ("La licence du fichier (uniquement si le fichier est le
  fichier principal)") (S5) [DOC]. There is **no single default licence** across HAL content — you
  must read each record.
- Depositing grants CCSD a distribution licence ("En déposant ce document, le contributeur (je)
  accorde la licence suivante à HAL") (S5) [DOC]. Exact terms not transcribed here.
- Publisher-produced files (typeset PDFs) may be deposited only "sous certaines conditions"
  (S5) [DOC] — this is the publisher-policy question, and HAL's moderation checks it (§4).
- **Metadata** are openly harvestable via OAI-PMH without restriction encountered; CCSD's own
  documentation site is published **CC BY 4.0** (footer, S5) [DOC].
- Embargo is supported (`acces-a-un-fichier-sous-embargo` in the documentation sitemap) (S5) [DOC].
- I did not find an explicit TDM (text-and-data-mining) policy document. **[NOT-VERIFIED]**

## 11. Caveats and controversies

1. **HAL is not a preprint server, and citing it as one is an error.** ~48% of records are `ART`
   and ~61% have no file. Check `docType_s` and `submitType_s` before describing a HAL record as a
   preprint.
2. **The 2001 founding date is unconfirmed.** CCSD's own text ties 2001 to TEL; the OAI earliest
   datestamp is 2002-09-23. Report both (§3).
3. **Domain facets undercount badly** (§2) — most records have no domain code. Never compute a
   "share of HAL that is computer science" from these numbers.
4. **The `domain_s` vs `domainAllCode_s` trap** returns a confident, wrong `0`. This is the single
   most likely way to produce a fabricated-looking statistic about HAL.
5. **Language.** English (2.70M) exceeds French (1.79M) archive-wide, so the "it's all in French"
   assumption is wrong — but French-language technical reports are a real and under-indexed part
   of the CS corpus, and Google Scholar surfaces them poorly.
6. **Software appears as `PATENT`.** French IDDN software registrations are filed under
   `docType_s:PATENT` (§6), so a naive `SOFTWARE`-only query (2,119 records) undercounts.
7. **Moderation covers only file deposits.** Metadata-only notices are unreviewed and go online
   immediately (§4) — the majority of the archive.
8. **arXiv transfer is HAL→arXiv only** as documented; the reverse is not established (§8).

## 12. Sources

- **S1** — HAL home page, https://hal.science/ · retrieved 2026-09-01 (HTTP 200, 31,509 B,
  default UA). Establishes operator and live status.
- **S2** — HAL search API, `https://api.archives-ouvertes.fr/search/` · retrieved 2026-09-01.
  All counts in §2, §3 and the prefix census in §8: `?q=*:*&rows=0&wt=json` (total);
  `&facet=true&facet.field=docType_s|submitType_s|language_s|domainAllCode_s`;
  `&facet.prefix=info|spi`; `q=halId_s:<prefix>*`.
- **S3** — CCSD, "Archive ouverte nationale" (HAL), https://www.ccsd.cnrs.fr/hal/ · retrieved
  2026-09-01 (HTTP 200, 188,614 B). Source of "Créée en 2001, HAL theses (anciennement TEL)" and
  of the HAL-SHS 2005 date. Supports the §3 date conflict.
- **S4** — HAL OAI-PMH `Identify` and `ListMetadataFormats`,
  `https://api.archives-ouvertes.fr/oai/hal/?verb=Identify` · retrieved 2026-09-01.
  `earliestDatestamp` 2002-09-23, formats list.
- **S5** — CCSD HAL documentation, https://documentation.hal.science/ · retrieved 2026-09-01.
  Moderation text quoted in §4 from
  `https://documentation.hal.science/administrer-un-portail/verification-des-depots-avant-leur-mise-en-ligne/`
  (HTTP 200, 57,398 B). Deposit/licence text from
  `https://documentation.hal.science/deposer/`. Sitemap (217 URLs) used to locate pages.
  **Retrieval note:** `doc.archives-ouvertes.fr` is a stale host — most paths return HTTP 404 with
  the notice *"La documentation HAL a fait peau neuve en migrant vers un nouveau site."* Use
  `documentation.hal.science`.
- **S6** — Live URL probes on `hal.science` / `inria.hal.science` / `tel.archives-ouvertes.fr` ·
  2026-09-01. Version and negative-control results in §5, §8, §9.
- **S7** — HAL search API record lookups by title and `halId_s` · 2026-09-01. Every row of the §7
  table and the §6 examples, with `halId_s`, `version_i`, `docType_s`, `producedDateY_i`,
  `domainAllCode_s`, `uri_s`, `fileMain_s`.
- **S8** — HAL API documentation, `https://api.archives-ouvertes.fr/docs`,
  `/docs/search`, `/docs/search/schema/fields`, `/docs/sword` · retrieved 2026-09-01 (all HTTP
  200). Supports §8.
- **S9** — CCSD, "Arxiv transfert", https://documentation.hal.science/en/arxiv-transfer/ ·
  retrieved 2026-09-01. All HAL→arXiv conditions quoted in §8.
- **S10** — CCSD, "Identifiants utilisés dans HAL",
  https://documentation.hal.science/en/identifiants-utilises-dans-hal/ · retrieved 2026-09-01.
  External identifier list in §9 (DOI, arXiv, PMID, PMCID, SWHID, PPN, ADS bibcode, bioRxiv,
  ChemRxiv, medRxiv, InSPIRE).

### Retrieval / crawler note

**No user-agent substitution was required for any HAL host.** Default `curl` obtained HTTP 200
from `hal.science`, `inria.hal.science`, `theses.hal.science`, `api.archives-ouvertes.fr`,
`documentation.hal.science` and `www.ccsd.cnrs.fr`, across roughly 60 API calls and 30 page
fetches on 2026-09-01, with no rate limiting, no CAPTCHA and no bot-block page. HAL is one of the
most scripting-friendly scholarly hosts in this survey. The only failing host was the deprecated
`doc.archives-ouvertes.fr`, which fails for content-migration reasons, not bot filtering.
