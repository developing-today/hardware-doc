# BioHackrXiv — preprint repository record

- **URL:** https://biohackrxiv.org/ (redirects to `https://osf.io/preprints/biohackrxiv/`)
- **Operator:** Hosted on **OSF Preprints**, infrastructure run by the **Center for Open
  Science**. Editorially steered by a community committee drawn from DBCLS, ZB MED, ELIXIR
  Europe and UTHSC (§4).
- **Discipline scope:** advertised as "Preprints for BioHackathons" (S2) [API] — in
  practice, **bioinformatics tooling, workflow systems, semantic-web infrastructure and
  FAIR data engineering** (§2, §6).
- **Launched:** 2020 (earliest deposits date from 2020, S1) [API] · **Status:** active,
  accepting submissions (S2) [API]
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What it is

BioHackrXiv exists to solve a specific and under-served problem: **hackathons produce real
technical work that has no publication venue.** A week-long BioHackathon or CodeFest sprint
yields working code, schema mappings, API bridges, container recipes and workflow modules —
outputs that are too small, too incremental or too infrastructural for a journal, but which
represent genuine engineering effort that should be citable and creditable.

BioHackrXiv gives those outputs a **DOI-bearing project report**. Its own strapline is
"Preprints for BioHackathons" (S2) [API], and its scope covers "works done during
BioHackathons, CodeFests, Sprints or similar events" (S5) [WEB].

For this knowledge base the relevance is direct: **this is a preprint server where the
subject matter is software and data infrastructure**, not laboratory results. If you work on
workflow engines, data standards, ontologies or research-software plumbing, BioHackrXiv is
where the ELIXIR/Galaxy/Nextflow community writes down what it built and why.

It is small — 163 works — and that is the point. It is a **narrow, high-signal corpus**,
not a general repository.

## 2. Scope and taxonomy

BioHackrXiv uses OSF's subject taxonomy. A retrieved record carries
`Life Sciences → Bioinformatics` (S1) [API], plus free-text tags (e.g. `bioinformatics`,
`computational biology`, `federated learning`, `hackathon`).

The corpus's real subject structure is better shown by what the text actually contains.
Keyword occurrence across **all 173 records** (title + description), 2026-09-01 (S1) [API]:

| Term | Records | Term | Records |
|---|---|---|---|
| workflow | **43** | ontology | 19 |
| FAIR | **42** | Galaxy | 16 |
| ELIXIR | **39** | SPARQL | 16 |
| RDF | 25 | Bioschemas | 15 |
| API | 20 | container | 8 |
| Nextflow | 4 | Docker | 2 |
| Snakemake | 4 | WDL | 0 |
| CWL | 4 | | |

**A quarter of the corpus mentions workflows; a quarter mentions FAIR; 39 of 163 works
mention ELIXIR.** That is an unusually concentrated infrastructure focus for a preprint
server.

Note the named workflow engines individually score low (Nextflow 4, Snakemake 4, CWL 4,
WDL 0) while generic "workflow" scores 43. The corpus talks about workflows *as a class* —
portability, provenance, registries, execution — more than it advocates particular engines.
[INF]

## 3. Size and growth

Retrieved from the OSF API, 2026-09-01 (S1) [API]. The complete corpus was paginated in
full, not sampled:

- **173 version-records** (`filter[provider]=biohackrxiv`)
- **163 unique works** after stripping `_vN` suffixes
- **9 works have more than one version**
- **172 published**, 1 withdrawn, 0 orphaned

By publication year (version-records):

| Year | Records |
|---|---|
| 2020 | 10 |
| 2021 | 11 |
| 2022 | 10 |
| 2023 | 29 |
| 2024 | 35 |
| 2025 | **44** |
| 2026 | 34 (year incomplete at retrieval) |

Flat at ~10/year for three years, then a step change from 2023 and sustained growth. With
34 records by 1 September 2026, the year is tracking near the 2025 level. This is a small
but **healthy and growing** venue, not a stalled experiment.

> **Distinguish these two numbers.** "173" is version-records; "163" is distinct works.
> The difference matters at this scale — quoting 173 as the number of reports overstates by
> 6%. Wikipedia's *List of preprint repositories* gives **">100"** with a 2020 year and
> "Center for Open Science" as operator (S4) [WEB]; that is **correct but coarse**, and it
> is the only entry among the five platforms in this batch whose Wikipedia size claim I
> found to be accurate.

## 4. Screening and moderation — what gets in

**BioHackrXiv is moderated.** The OSF provider metadata declares
`reviews_workflow: pre-moderation` (S2) [API] — submissions are reviewed **before** they
appear, which is a stronger gate than Zenodo, figshare or Authorea apply.

Corroborated by the records themselves: every record carries a `reviews_state`, distributed
as **`accepted` 172, `withdrawn` 1** (S1) [API]. A moderation state machine is genuinely
in use.

Provider settings also show `allow_submissions: true` and `assertions_enabled: true`
(S2) [API] — the latter meaning OSF's conflict-of-interest and data-availability assertions
are required. Those assertions are populated in practice: `has_data_links` is
`available` for **53** records, `not_applicable` for 108, `no` for 4 (S1) [API]. So a third
of reports link to the data or code they describe, in a structured, machine-readable field.

**Steering Committee**, from the provider's advisory board metadata (S2) [API]:

| Member | Affiliation |
|---|---|
| Toshiaki Katayama | DBCLS |
| Leyla Garcia | ZB MED |
| Jennifer Harrow | ELIXIR Europe |
| Pjotr Prins | UTHSC |
| Alexander Garcia | (affiliation truncated in retrieved metadata) |

That is a genuine bioinformatics-infrastructure committee, not a nominal board.

**What pre-moderation does and does not mean:** it is a scope-and-suitability check, not
peer review. It establishes that a report is a real hackathon output rather than spam. It
does **not** establish that the software works, the benchmarks are sound, or the approach is
novel.

## 5. Reliability — what you can and cannot trust

**What a BioHackrXiv DOI gives you:** a timestamp, a Crossref-resolvable DOI under the
`10.37044` prefix, OSF hosting, a moderation pass (§4), structured COI and data-availability
assertions, and version history where versions exist.

**What it does not give you:** peer review, reproducibility validation, or any guarantee the
described tool still exists. Hackathon reports describe software at a moment of maximum
optimism; a report from a 2021 CodeFest may describe a prototype that was never maintained.
**Check the linked repository's commit history before relying on anything described here.**
[INF]

**Verified resolution behaviour** (S3) [API]:

- `https://doi.org/10.37044/osf.io/h6zqj_v2` → **HTTP 200**, resolving to
  `https://osf.io/h6zqj_v2`.
- Negative control `https://doi.org/10.37044/osf.io/zzzzz_v9` → **HTTP 404**.

So **DOIs discriminate correctly**. Web URLs do not — see the warning below.

> ### ⚠ Negative control: OSF web URLs return 200 for records that do not exist
>
> Probed 2026-09-01 (S3) [WEB]:
>
> | URL | Result |
> |---|---|
> | `https://biohackrxiv.org/` | HTTP 200, **4,207 bytes** |
> | `https://biohackrxiv.org/h6zqj_v2` (real) | HTTP 200, **4,207 bytes** |
> | `https://biohackrxiv.org/ZZZNOTREAL999` (bogus) | HTTP 200, **4,207 bytes** |
>
> All three return **byte-identical** responses, because OSF is a JavaScript
> single-page application that serves the same shell for every path and resolves content
> client-side.
>
> **Consequence:** for OSF-hosted preprint servers, an HTTP 200 — and even a byte-size
> check, which this repository's method normally recommends — proves **nothing**. Link
> checkers will report broken preprints as healthy. **Verify via the OSF API or via DOI
> resolution, never via the web URL.**

## 6. What you actually find there — examples

All verified present in the corpus on 2026-09-01 (S1) [API]. DOIs use the `10.37044/osf.io/`
prefix; the landing page is `https://biohackrxiv.org/<id>`.

**Workflow systems and execution**

| Report | DOI suffix | Date |
|---|---|---|
| Snakemake Hackathon 2026 | `h6zqj_v2` | 2026-04-29 |
| BiocExecute: Make package functions or workflows executable from the command line | `ywsmq_v1` | 2026-06-19 |
| Eurobioc2026 BiocContainer Report | `acxky_v1` | 2026-06-15 |
| Evolving FAIR Image Analysis in Galaxy for Cross-domain and AI-ready Applications | `tsxby_v1` | 2026-03-31 |

**Semantic web, RDF and data standards**

| Report | DOI suffix | Date |
|---|---|---|
| Variant representation in RDF | `jazsb_v1` | 2026-08-09 |
| Variant annotation in RDF for clinical trials matching | `2hbqf_v1` | 2026-08-09 |
| Schema-Driven Generation of Synthetic HL7 FHIR RDF Data from Shape Expressions (ShEx) | `3gak2_v2` | 2026-08-06 |
| Rendering SSSOM ontology mappings as RDF named graphs and RDF 1.2 triple terms | `auhzg_v1` | 2026-06-14 |
| Leveraging RDF and CURIE metadata resolution with identifiers.org | `xza73_v1` | 2025-06-02 |

**Research-software ecosystem and registries**

| Report | DOI suffix | Date |
|---|---|---|
| Bidirectional bridge: GitHub ⇄ bio.tools | `8ktd6_v1` | 2026-02-24 |
| Enhancing bio.tools by Semantic Literature Mining | `8m5ey_v1` | 2025-05-04 |
| Software Quality Indicators: extraction, categorisation and recommendations from canonical sources | `etp3g_v1` | 2025-06-11 |
| METRICS — Monitoring of Key Performance Indicators for ELIXIR Services | `2jgk4_v1` | 2026-01-22 |
| BioHackEU24 report: Integrating Bioconductor packages with the ELIXIR Research Software Ecosystem | `dsgnw_v1` | 2025-04-08 |

**Newer machine-learning and LLM infrastructure**

| Report | DOI suffix | Date |
|---|---|---|
| Towards Federated Learning Across Biobanks: Prototype Software from the 2026 CMU–NVIDIA Hackathon | `5psfj_v2` | 2026-08-27 |
| MCP server tools with RDF shapes | `8qeh5_v1` | 2025-12-16 |
| Measure before you rewrite: ablation-driven redesign of LLM-facing RDF schema documentation in TogoMCP | `6v5ra_v1` | 2026-07-26 |

Note `Bidirectional bridge: GitHub ⇄ bio.tools` and the two MCP/LLM entries: this corpus
tracks current tooling practice closely, and the reports are often the **only written record**
of an integration that exists as a few hundred lines of glue code.

## 7. Landmark papers

None, and the concept does not apply. BioHackrXiv publishes **project reports**, not
field-defining results. Its value is documentary and archaeological — it records how
bioinformatics infrastructure actually got built, by whom, and at which event. No table.

## 8. Who should care

- **Workflow and pipeline engineers** — Nextflow, Snakemake, CWL, Galaxy: design
  discussions and integration reports that never reach a journal.
- **Data-standards and semantic-web practitioners** — RDF/SPARQL/ShEx/SSSOM/Bioschemas work
  is disproportionately represented (§2).
- **Research-software engineers** — software quality indicators, registries (bio.tools),
  packaging and container practice.
- **FAIR / open-science infrastructure people** — 42 of 163 works mention FAIR.
- **Anyone tracing provenance of a bioinformatics tool** — hackathon reports frequently
  document the origin of a component whose repository history alone does not explain it.

Not useful for: electronics, firmware, or hardware design. Despite being software-centric,
BioHackrXiv is **life-sciences software** throughout. [INF]

## 9. Access, APIs and bulk retrieval

**OSF API v2 — fully open, no key required for public reads** (S1) [API]:

```
https://api.osf.io/v2/preprints/?filter[provider]=biohackrxiv&page[size]=100
```

- Returns JSON:API with `links.meta.total` (**173**) and `links.next` for pagination.
- **The entire corpus paginates in two requests** at `page[size]=100`. Bulk retrieval is
  trivial at this scale; there is no excuse for sampling.
- Provider metadata: `https://api.osf.io/v2/preprint_providers/biohackrxiv/`
- Licence vocabulary: `https://api.osf.io/v2/preprint_providers/biohackrxiv/licenses/`
- Useful per-record attributes: `date_published`, `doi`, `reviews_state`, `date_withdrawn`,
  `is_latest_version`, `version`, `has_data_links`, `data_links`, `has_coi`, `subjects`,
  `tags`, `license_record`.

**Rate limits:** not observed in headers during retrieval; the full corpus was fetched
without throttling. **[NOT-VERIFIED]** as to published limits — be considerate regardless.

**OAI-PMH:** OSF's endpoint for provider-scoped harvesting was **not verified** in this
pass. The REST API is sufficient at this corpus size.

**Community entry points** (S2, S5) [WEB]: `https://guide.biohackrxiv.org/` (about and
submission guidelines) and `https://index.biohackrxiv.org/` (hackathon preprint index).
**[NOT-VERIFIED]** — referenced in provider metadata but not independently loaded.

**Negative controls:** see the boxed warning in §5 — the DOI-level control behaves
correctly (404), the web-URL control does not (false 200). A Zenodo community lookup for
`biohackrxiv` returns **HTTP 404**, confirming BioHackrXiv has no Zenodo presence and lives
solely on OSF (S1) [API].

## 10. Licensing and reuse

**Author-chosen from three options**, retrieved from the provider's licence endpoint,
2026-09-01 (S1) [API]:

| Licence |
|---|
| CC-BY Attribution 4.0 International |
| CC0 1.0 Universal |
| CC-BY Attribution-NonCommercial-NoDerivatives 4.0 International |

Two of the three are fully open; **CC-BY-NC-ND is available and does restrict reuse and
derivative work**, so check `license_record` per item rather than assuming the corpus is
uniformly open. Records carry a `default_license_id` field.

Metadata is served openly through the OSF API, making **metadata mining unproblematic**.
Full-text mining depends on the per-item licence. [INF]

## 11. Caveats and controversies

1. **Small corpus.** 163 works. Do not draw statistical conclusions from keyword counts in
   §2 — they are descriptive, not inferential.
2. **Reports describe software at peak optimism.** Verify the tool still exists (§5).
3. **The OSF SPA false-200 problem** (§5) is the single most important operational caveat,
   and it affects *every* OSF-hosted preprint server, not just this one.
4. **Version-records vs works** — 173 vs 163 (§3).
5. **Platform dependency.** BioHackrXiv has no independent infrastructure; it is a branded
   view of OSF Preprints. Its continuity is the Center for Open Science's continuity. That
   is a considerably better position than a commercial platform, but it is a
   single-point dependency and should be named as one. [INF]
6. **One withdrawn record** exists (§3, §4) — withdrawals do happen and are tracked in
   `date_withdrawn` / `reviews_state`.

## 12. Sources

- **S1** — OSF API v2: `https://api.osf.io/v2/preprints/?filter[provider]=biohackrxiv`
  (full corpus paginated at `page[size]=100`), plus
  `https://api.osf.io/v2/preprint_providers/biohackrxiv/licenses/` and a Zenodo
  communities control (`/api/communities/biohackrxiv` → HTTP 404). Retrieved
  **2026-09-01**. Supports: 173 version-records / 163 unique works / 9 multi-version works,
  the year table, `reviews_state` distribution (172 accepted, 1 withdrawn),
  `has_data_links` distribution, subject and tag structure, the licence vocabulary, and all
  titles, DOI suffixes and dates in §6.
- **S2** — OSF API v2 provider record,
  `https://api.osf.io/v2/preprint_providers/biohackrxiv/`. Retrieved 2026-09-01. Supports:
  provider name and description ("Preprints for BioHackathons"),
  `reviews_workflow: pre-moderation`, `allow_submissions: true`, `assertions_enabled: true`,
  `domain: https://biohackrxiv.org/`, the Steering Committee membership, and the
  `guide.biohackrxiv.org` / `index.biohackrxiv.org` links.
- **S3** — Resolution and negative-control probes, 2026-09-01:
  `https://doi.org/10.37044/osf.io/h6zqj_v2` (HTTP 200 → `osf.io/h6zqj_v2`);
  `https://doi.org/10.37044/osf.io/zzzzz_v9` (HTTP 404); and HTTP probes of
  `https://biohackrxiv.org/`, `https://biohackrxiv.org/h6zqj_v2` and
  `https://biohackrxiv.org/ZZZNOTREAL999`, all returning HTTP 200 at 4,207 bytes.
  Supports: §5 resolution behaviour and the SPA false-200 finding.
- **S4** — Wikipedia, *List of preprint repositories*, wikitext via the MediaWiki API,
  2026-09-01. Supports: the ">100" size claim, 2020 year, and "Center for Open Science"
  operator, as compared against measured values in §3.
- **S5** — BioHackrXiv description and submission-guideline links as published in the OSF
  provider metadata (S2), pointing to `http://guide.biohackrxiv.org/about.html` and
  `http://guide.biohackrxiv.org/submission_guidelines.html`. Retrieved 2026-09-01 via the
  provider record; the guide pages themselves were **not independently loaded**.
