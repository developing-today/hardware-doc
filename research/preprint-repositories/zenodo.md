# Zenodo — preprint repository record

- **URL:** https://zenodo.org/
- **Operator:** CERN (European Organization for Nuclear Research), originating from the
  OpenAIRE programme funded by the European Commission. Runs on CERN Data Centre
  infrastructure; software stack is InvenioRDM.
- **Discipline scope:** advertised as "All fields of research. All types of research
  artifacts" (S3) — *as actually used*, the corpus is dominated by bulk-ingested
  biodiversity/taxonomic literature and figures, with a substantial but minority
  research-software and dataset population (§3).
- **Launched:** **May 2013** (operator's own statement, S2) · **Status:** active
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

> **Launch-year conflict — resolved, see §10.1.** Wikipedia's *List of preprint
> repositories* gives Zenodo's year as **2011**; Zenodo's own About page and Wikipedia's
> *own Zenodo article* both give **May 2013**. Both figures are recorded below with
> sources; the 2011 date appears to refer to the predecessor service, not Zenodo.

## 1. What it is

Zenodo is a **catch-all repository**. It exists to give a citable, persistent home to any
research output that has nowhere else to go — and, critically for this knowledge base, to
outputs that are *not papers*: source code, firmware images, datasets, KiCad projects,
simulation inputs, conference artifact packages, slide decks, lesson material.

Its origin is a policy problem rather than a scholarly one. The European Commission
required that EC-funded research be deposited openly, but many researchers had no
institutional or subject repository that would take their material. OpenAIRE was tasked
with providing a "catch-all" and CERN supplied the capability (S2). Zenodo is therefore
designed around the removal of barriers: "Zenodo does not impose any requirements on
format, size, access restrictions or licence. Quite literally we wish there to be no
reason for researchers not to share!" (S2) [DOC]

That design choice is the single most important fact about Zenodo, and it cuts both ways.
It is why a firmware release or a board design can get a DOI in ninety seconds; it is also
why **a Zenodo DOI carries no scholarly warrant whatsoever** (§5).

For a hardware or software engineer, Zenodo matters mainly for one mechanism: the **GitHub
integration** (§6), which turns a git tag into an archived, DOI-bearing, citable software
release. This is the dominant route by which open-source research software becomes
formally citable, and it is worth understanding precisely.

Zenodo is *not* primarily a preprint server, despite being listed as one. Preprints are
about 3.4% of its records (§3). Calling it a preprint repository is a category error that
the Wikipedia list propagates.

## 2. Scope and subject taxonomy

Zenodo does not use a discipline taxonomy like arXiv's `cs.DC`. It has no subject
categories that gate deposit. Instead it has:

**(a) Resource types** — a controlled vocabulary, the real structural axis. Retrieved from
the `resource_type` aggregation of the search API, 2026-09-01 (S1) [API]:

| Resource type | Records (latest version) |
|---|---|
| publication | 4,760,348 |
| image | 1,229,242 |
| dataset | 687,267 |
| software | 284,518 |
| presentation | 92,470 |
| other | 65,300 |
| poster | 38,299 |
| video | 21,932 |
| lesson | 17,638 |
| model | 16,819 |

Publication subtypes (same query, S1) [API]:

| Subtype | Records |
|---|---|
| publication-article | 2,462,351 |
| publication-taxonomictreatment | 714,681 |
| **publication-preprint** | **242,779** |
| publication-conferencepaper | 240,109 |
| publication-book | 184,941 |
| publication-section | 151,673 |
| publication-other | 120,480 |
| publication-report | 91,590 |
| publication-journal | 55,387 |
| publication-deliverable | 39,461 |

Subtypes retrieved individually (S1) [API]: `datamanagementplan` 1,636 ·
`softwaredocumentation` 3,958 · `technicalnote` 18,847 · `workingpaper` 36,307 ·
`patent` 3,119. Software has one subtype: `software-computationalnotebook` 8,119.

> **Facet-name trap.** Querying `&type=publication&subtype=thesis` returns
> `{"hits":{"total":0}}` with **HTTP 200**. So does `&type=notarealtype123`. An invalid
> facet value is *indistinguishable from a genuine zero* (§8, negative controls). `thesis`
> is simply not in Zenodo's vocabulary — the aggregation above is the authoritative list.
> Do not infer "there are no theses on Zenodo" from that zero. [API]

**(b) Communities** — see §6.3. Self-service, curator-run collections. 42,971 exist
(S1, 2026-09-01) [API]. They are the closest thing Zenodo has to subject structure, and
they are weak (§6.3).

**(c) Free-text keywords** — uncontrolled. The `subject` aggregation is dominated by
`Biodiversity` (2,161,233), `Taxonomy` (1,825,897), `Animalia` (1,240,408), `Arthropoda`
(918,857), `Insecta` (664,605), and `BHL-Corpus` / `Source: Biodiversity Heritage Library`
(310,066 each) (S1) [API].

## 3. Size and growth

**Headline (S1, retrieved 2026-09-01) [API]:**

- **7,231,589** records, latest-version only (`/api/records/?size=1`).
- A second identical call minutes later returned **7,231,598** — the corpus grows by
  roughly ten records per minute during a working day. Treat any single figure as a
  snapshot, not a constant.
- **8,242,934** records counted with `allversions=true`.

The gap between those last two numbers is the versioning model made visible: about
1.01 million records are superseded prior versions.

**Versions per type — the software signal** (S1) [API]:

| Type | Latest-version | All versions | Versions per work |
|---|---|---|---|
| software | 284,518 | 712,318 | ≈2.50 |
| publication/preprint | 242,779 | 357,701 | ≈1.47 |
| all records | 7,231,598 | 8,242,934 | ≈1.14 |

Software carries **2.5 versions per work** against a corpus average of 1.14. That ratio is
direct evidence of the GitHub release integration doing its job: each tagged release
produces a new version record under a shared concept DOI (§6.1).

**Access status** (S1) [API]: open 6,976,693 (96.5%) · restricted 243,832 · embargoed
11,071 · metadata-only 2.

**File types** (S1) [API]: pdf 3,846,843 · png 767,864 · html 765,134 · jpg 556,380 ·
**zip 487,961** · txt 188,831 · docx 120,760 · json 107,229 · xlsx 106,637 · csv 98,627.
The zip count is the practical proxy for "packaged code or data".

**Growth by publication year** (S1) [API]. Note this is the *metadata* publication date,
which for bulk-ingested legacy literature is the original publication year, not the
deposit date — so early years are retrospective ingest, not 2013 activity:

| Year | Records | | Year | Records |
|---|---|---|---|---|
| 2011 | 74,334 | | 2019 | **503,221** |
| 2013 | 99,825 | | 2020 | 276,649 |
| 2015 | 127,316 | | 2022 | 396,082 |
| 2017 | 193,863 | | 2024 | 660,197 |
| 2018 | 222,575 | | 2025 | 936,029 |
| | | | 2026 | **1,228,268** |

Two anomalies worth flagging [INF]: the **2019 spike** (503,221, more than double 2018 and
well above 2020) and the **2026 figure of 1,228,268** — already the largest year on record
on 2026-09-01, i.e. two-thirds through the year. Both are consistent with bulk machine
deposit rather than organic growth. The subject aggregation (§2c) points to the likely
source: biodiversity/taxonomic pipelines. `publication-taxonomictreatment` alone is
714,681 records — **nearly three times the entire preprint corpus**.

**What this means:** Zenodo's headline "7.2 million" is not 7.2 million research papers.
It is dominated by figures (1.23M images) and bulk taxonomic literature. Anyone quoting
Zenodo's size as evidence of scholarly scale is misreading it. [INF]

**Conflict with Wikipedia:** the *List of preprint repositories* records Zenodo's size as
**">100,000"** (S7). Against 242,779 preprint records — or 7.23M total — that entry is
stale by more than an order of magnitude on either reading. [API] vs [WEB]

## 4. Screening and moderation — what gets in

**The gate is: registration, and nothing else.**

From Zenodo's General Policies v1.0 (S3) [DOC], quoted:

> **Eligible depositors:** "Anyone may register as user of Zenodo. All users are allowed to
> deposit content for which they possess the appropriate rights."

> **Status of research data:** "Any status is accepted, from any stage of the research
> lifecycle."

> **Data quality:** "All information is provided 'as-is', and the user shall hold Zenodo
> and information providers supplying data to Zenodo free and harmless in connection with
> the use of such information."

There is **no peer review, no editorial board, no subject-matter screening, no endorsement
requirement, and no affiliation requirement.** There is no moderation queue. Content is
live and has a DOI immediately on publish.

Moderation is **reactive and post-hoc**, on a revocation model (S3) [DOC]:

> **Revocation:** "Content not considered to fall under the scope of the repository will be
> removed and associated DOIs issued by Zenodo revoked. Please signal promptly, ideally no
> later than 24 hours from upload, any suspected policy violation. Alternatively, content
> found to already have an external DOI will have the Zenodo DOI invalidated and the record
> updated to indicate the original external DOI."

Constraints that do exist: files must not "violate privacy or copyright, or breach
confidentiality or non-disclosure agreements"; a licence must be specified for all publicly
available files; total file size per record is capped at **50 GB**, with higher quotas
case-by-case (S3) [DOC].

## 5. Reliability — what you can and cannot trust

### 5.1 What a Zenodo DOI *does* mean

- **A timestamp.** The record existed in this form at this datetime.
- **A fixity guarantee.** "All data files are stored along with a MD5 checksum of the file
  content. Files are regularly checked against their checksums" (S3) [DOC].
- **Bit preservation with replication.** "All data files are stored in CERN Data Centres,
  primarily Geneva, with replicas in Budapest… backed up to tape on a nightly basis" (S3).
- **Immutability of a version.** A version DOI points at files that cannot change.
- **DataCite registration**, so the metadata propagates to aggregators (S6) [DOC].

### 5.2 What a Zenodo DOI does **not** mean

- **Not peer review.** Nothing was refereed.
- **Not a correctness, novelty or originality check.** Nothing was read.
- **Not a plagiarism scan.** None is performed or claimed.
- **Not authorship verification.** Nobody checked that the depositor is the author, or that
  they hold the rights they assert.
- **Not scope screening.** "All fields of research" is enforced only reactively.
- **Not a guarantee the software runs.** Explicitly disclaimed: "Zenodo makes no promises
  of usability and understandability of deposited objects over time" (S3) [DOC].

A concrete illustration of how low the bar is: a record titled *"This is an example of an
interactive Carto graph in Authorea"* exists with a registered DOI on a *different*
platform (§ see `authorea.md`), and the equivalent is trivially true here. A DOI is a
plumbing fact, not a quality signal.

### 5.3 No SLA — by stated design

Zenodo's Principles page (S4) [DOC]:

> "Zenodo does not sign SLAs (service-level agreements). This is not a weakness, it is by
> design and marks a philosophy that we believe is most appropriate for Science… Service
> failure can never be undone. Enforcing an SLA means being prepared to litigate against
> the contract."

Read that honestly: you have **no contractual recourse** if Zenodo loses your data. What
you have instead is CERN's operational competence and published practice.

### 5.4 Retention — the actual commitment, quoted

This is the sustainability question, and Zenodo answers it unusually plainly (S3) [DOC]:

> **Retention period:** "Items will be retained for the lifetime of the repository. This is
> currently the lifetime of the host laboratory CERN, which currently has an experimental
> programme defined for the next 20 years at least."

> **Succession plans:** "In case of closure of the repository, best efforts will be made to
> integrate all content into suitable alternative institutional and/or subject based
> repositories."

So the promise is: *as long as CERN exists*, bounded below by a ~20-year programme horizon,
with a **best-efforts** (not guaranteed) succession plan. Wikipedia adds that Zenodo is
supported by CERN "as a marginal activity", with contributions via the CERN & Society
Foundation (S8) [WEB] — i.e. it is not separately endowed. That is a real, if
well-managed, concentration risk.

### 5.5 Records are not deleted

The versioning/longevity policy (S3) [DOC]:

> **Versions:** "Data files are versioned. Records are not versioned… Records can be
> retracted from public view; however, the data files and record are preserved."

> **Withdrawal:** "…the reason for the withdrawal will be indicated on a tombstone page,
> which will henceforth be served in its place. Withdrawal is considered an exceptional
> action… The DOI and the URL of the original object are retained."

Practical consequence: **a Zenodo DOI should not rot into a 404.** A withdrawn item becomes
a tombstone, not a dead link. Confirmed by the OAI-PMH `Identify` response, which declares
`<deletedRecord>no</deletedRecord>` (S5) [API] — Zenodo does not emit deletion records to
harvesters, because in its model records are not deleted.

### 5.6 Spam and abuse

An open-to-all repository that mints DOIs is an obvious target for SEO spam, warez and
link-laundering. Zenodo's published countermeasures are the reactive revocation clause
(§4) and the 24-hour reporting request (S3) [DOC]. Zenodo also publishes an "AI usage
notice" in its policy navigation (S3) [WEB].

**[NOT-VERIFIED]** I could not retrieve a Zenodo-published spam-incident report, a
quantified abuse rate, or a documented anti-spam pipeline description. The policy text
implies an active trust-and-safety function but does not describe it. Do not assume a
figure; I have none.

### 5.7 How to sanity-check an individual Zenodo record

1. **Read the resource type and subtype.** `software` with a GitHub
   `isSupplementTo` relation is a very different object from `publication/article`.
2. **Follow the `related_identifiers`.** Genuine software releases link to
   `github.com/OWNER/REPO/tree/TAG`. Genuine supplements link to a journal DOI.
3. **Check concept vs version DOI** (§6.1). Citing the wrong one changes what you promised
   your reader.
4. **Check whether a peer-reviewed version exists** via the `isDocumentedBy` /
   `isSupplementTo` relations — e.g. record 8409685 (*Scientific colour maps*) carries
   `isDocumentedBy → 10.5194/gmd-2017-328` (S1) [API].
5. **Treat the deposit as self-published unless a relation proves otherwise.**

## 6. What you actually find there — examples

### 6.1 The GitHub integration — how a release becomes citable

This is the mechanism the record exists to explain. Verified against Zenodo's own docs
(S9, S10) [DOC] and against live API records (S1) [API].

**Setup, once per repository** (S9) [DOC], quoted steps:
1. Connect your GitHub account to Zenodo (profile menu → **GitHub**).
2. Click **Sync now**.
3. Find the repository and **toggle the slider** to enable it.
4. The repository is now connected; refresh to confirm.

Zenodo installs a webhook. Thereafter, **"new releases from the repository will be
automatically ingested and archived"** (S9) [DOC].

**Per release:** you create a GitHub Release (a tag). Zenodo receives the webhook,
downloads GitHub's source tarball for that tag, creates a new record, and mints a DOI.

**Describing the software** — two files, with a documented precedence rule (S10) [DOC]:
- `.zenodo.json` — Zenodo's native metadata file.
- `CITATION.cff` — the Citation File Format, which GitHub also renders as a "Cite this
  repository" box.
- **Precedence, quoted:** *"If your repository also contains a `.zenodo.json` file, Zenodo
  will only use the `.zenodo.json` metadata and ignore the `CITATION.cff` entirely."*
  Zenodo still recommends shipping `CITATION.cff` for GitHub's benefit, and states a
  "long-term preference for open metadata formats like CITATION.cff to eventually make the
  `.zenodo.json` format unnecessary" (S10) [DOC].
- Zenodo implements only **a subset** of the CITATION.cff schema (S10) [DOC].

**The resulting record has a recognisable signature** (S1) [API]:
- Title formatted `owner/repo: Release Name`
- `related_identifiers` containing
  `{"identifier": "https://github.com/OWNER/REPO/tree/TAG", "relation": "isSupplementTo"}`

**Concept DOI vs version DOI — the part people get wrong.**

Every versioned Zenodo work has *two kinds* of DOI:

| | Concept DOI | Version DOI |
|---|---|---|
| Identifies | the software *as a whole*, across all releases | one specific release |
| Stability of target | resolves to the **latest** version | resolves to **that** version, forever |
| API fields | `conceptdoi`, `conceptrecid` | `doi`, `id` |
| Cite it when | you mean "this project" | you mean "the exact code I ran" |

**Verified live, 2026-09-01** (S11) [API]:
- `https://doi.org/10.5281/zenodo.3509134` (pandas **concept** DOI) →
  redirects to `https://zenodo.org/records/21500199`, which is pandas **v3.0.5**.
- `https://doi.org/10.5281/zenodo.21500199` (pandas **version** DOI for v3.0.5) →
  redirects to the same `https://zenodo.org/records/21500199`.

Today those land in the same place because v3.0.5 is current. **When pandas cuts v3.0.6,
the concept DOI will move and the version DOI will not.** For reproducibility — the entire
reason an engineer cites software — **cite the version DOI**. Cite the concept DOI only
when you mean the project generically.

Negative control: `https://doi.org/10.5281/zenodo.999999999` → **HTTP 404**, and
`https://zenodo.org/api/records/999999999` → `{"status": 404, "message": "The persistent
identifier does not exist."}` (S11) [API]. So unregistered Zenodo DOIs fail cleanly.

**Software Heritage.** Zenodo's GitHub/Software docs state the section "provides details on
how software records are archived in **Software Heritage**", and that "all the software
records with a single compressed file are considered for archival" (S12) [DOC]. So an
eligible Zenodo software deposit is also pushed into Software Heritage's universal source
archive, giving it a second, independent preservation copy and an SWHID.
**[NOT-VERIFIED]** I did not confirm the coverage fraction, the latency, or the SWHID
back-link from an individual Zenodo record — the detail sub-pages under
`/docs/github/archive-software/` returned 404 on retrieval (§8).

### 6.2 Representative and landmark deposits (all verified live)

All rows below were retrieved from the Zenodo API on 2026-09-01 (S1) [API]. Concept DOIs
given where present.

| Deposit | Concept DOI | Type | Note |
|---|---|---|---|
| `pandas-dev/pandas` | 10.5281/zenodo.3509134 | software | v3.0.5 current at retrieval; BSD-3-Clause |
| `ultralytics/yolov5` | 10.5281/zenodo.3908559 | software | 1,353,587 views — most-viewed software record found |
| Scientific colour maps (Crameri) | 10.5281/zenodo.1243862 | software | MIT; `isDocumentedBy → 10.5194/gmd-2017-328` |
| `desihub/fastspecfit` | 10.5281/zenodo.10253420 | software | BSD-3-Clause; astronomy pipeline |
| scikit-learn | 10.5281/zenodo.591564 | software | concept record for the ML library |
| Astropy | 10.5281/zenodo.4670728 | software | astronomy core package |
| `yt-project/unyt` | 10.5281/zenodo.1344604 | software | units library |
| India ISIN Database | 10.5281/zenodo.6508187 | software | CC0; v2026.9.1 — a *data* release using the software/GitHub pipeline |

The last row is instructive: the GitHub-release-to-DOI pipeline is routinely used to
version **datasets** that happen to live in a git repo, not just code. [INF]

### 6.3 Conference artifact-evaluation packages

ACM and USENIX artifact-evaluation committees badge reproducibility artifacts, and Zenodo
is a common archival target. Verified by search, 2026-09-01 (S1) [API]:

- Query `"USENIX" AND "artifact"` → **254** records.
- Query `"Artifacts Available"` → **31** records.
- Query `"artifact appendix"` → **47** records.
- Query `"artifact evaluation"` → **945** records.

Named, verified examples:

| Artifact | DOI | Venue |
|---|---|---|
| `sqlright-artifact` | 10.5281/zenodo.6672457 | USENIX Security 2022 AE |
| DICE* Artifact | 10.5281/zenodo.4471637 | USENIX Security '21 AE |
| PETAL | 10.5281/zenodo.14725819 | USENIX 2025, "Artifacts Available" |
| `congcongmiao/FlexWAN` | 10.5281/zenodo.8309931 | SIGCOMM 2023, "Artifacts Available" |
| *Relaxing the One Definition Rule in Interpreted C++* | 10.5281/zenodo.3579302 | CC'20 AE |
| *Optimizing Persistent Memory Transactions* | 10.5281/zenodo.3346054 | PACT19 AE |

All six are resource type `software` (S1) [API]. For a systems engineer this is the most
directly useful corner of Zenodo: badged, reviewed-for-reproducibility code from top
systems and security venues, with permanent identifiers.

> **Query caveat:** the search `"OSDI" OR "NSDI"` returned 231 records whose top hits were
> about air-quality sensors and double ionization — the boolean was not honoured as
> intended. Zenodo's `q` parameter is not a reliable boolean engine; verify hits by eye.
> [API]

### 6.4 Hardware and electronics content

Counts by phrase search, 2026-09-01 (S1) [API], all record types:

| Query | Records |
|---|---|
| `Arduino` | 5,337 |
| `FPGA` | 3,334 |
| `firmware` | 1,878 |
| `Verilog` | 692 |
| `"RISC-V"` (quoted) | 495 |
| `RISCV` | 436 |
| `"open source hardware"` | 277 |
| `title:"RISC-V"` | 179 |
| `KiCad` | 58 |

> **Tokenisation trap — important.** The *unquoted* query `RISC-V` returns **422,778**
> records. The quoted phrase `"RISC-V"` returns **495**. The hyphen is being treated as a
> query operator, inflating the count roughly 850×. Negative controls
> `zzzqqxnotaword12345` (quoted and unquoted) both return 0, so the engine is not simply
> matching everything. **Always quote hyphenated technical terms against this API.** [API]

**Honest conclusion on hardware:** Zenodo hosts real but thin electronics content. 58 KiCad
hits is a rounding error against 7.2M records. Zenodo is not where open hardware lives; it
is where open hardware occasionally gets archived.

### 6.5 Communities — including hardware ones

42,971 communities exist (S1) [API]. Communities are self-service collections with
depositor-side curation. Verified record counts, 2026-09-01 (S1) [API]:

| Community slug | Title | Records |
|---|---|---|
| `swcarpentry` | Software Carpentry | 49 |
| `hardwarex` | HardwareX | 44 |
| `sosy-lab-software` | SoSy-Lab Software Collection | 32 |
| `artifact-evaluation` | Artifact Evaluation | 10 |
| `openhardware_academy` | The archive of open hardware academy lessons and materials | 8 |
| `ohresearch` | Open Hardware researchers group | 5 |
| `hardware-fab` | Hardware-Fab | 2 |
| `hw_security` | Hardware Security | 1 |

Community *search* totals: `hardware` 652, `electronics` 702, `software` 3,382,
`"open hardware"` 12 (S1) [API].

**Read those numbers carefully.** The hardware and open-hardware communities contain
between **one and forty-four records each**. The `artifact-evaluation` community has 10
records while free-text search finds 945 artifact-evaluation records — i.e. **communities
capture a negligible fraction of the relevant corpus**. Communities are a discovery
aid at best; they are not a curation layer you can rely on, and you should not use
community membership as a filter when surveying Zenodo. [INF]

Negative control: `https://zenodo.org/api/communities/zzz-not-a-real-community-999`
returns **HTTP 404 NOT FOUND**, so community slugs *do* fail cleanly (unlike facet
values) (S1) [API].

> **Community search is also fuzzy:** querying communities for `FPGA` returned 37 results
> whose top hits were `fp7-bmc`, `fp7-dirtpol`, `eurofusion-fp8` — i.e. "FP7"/"FP8"
> matches, not FPGA. [API]

## 7. Landmark papers (software · distributed systems · databases · electronics · security)

Zenodo is not where landmark *papers* in these fields first appear — that is arXiv and
IACR ePrint. What Zenodo holds is the **landmark software and artifacts** behind papers.
The genuinely notable deposits are those in §6.2 (pandas, scikit-learn, Astropy, YOLOv5,
Scientific colour maps) and the artifact packages in §6.3.

For the template's "preprint first?" question: **none of these are preprints.** They are
software releases and supplementary artifacts, in every case deposited *alongside or after*
a publication, not in advance of one. Where a relation exists it is
`isSupplementTo` (to a GitHub tag) or `isDocumentedBy` (to a journal DOI) — e.g. Scientific
colour maps → `10.5194/gmd-2017-328` (S1) [API]. I found **no** case of a field-defining
CS/EE paper whose first public appearance was a Zenodo preprint, and I am not going to
manufacture one.

## 8. Access, APIs and bulk retrieval

### 8.1 REST API

- Base: `https://zenodo.org/api/records/`
- Key parameters, all verified working (S1) [API]: `size`, `page`, `q`, `type`, `subtype`,
  `sort` (`newest`, `mostviewed`), `allversions` (`true`/`false`).
- `size=0` is rejected: `{"status":400,…"Must be greater than or equal to 1."}` — so the
  cheapest count query is `size=1`.
- Response carries `hits.total` plus `aggregations` for `resource_type`,
  `access_status`, `subject`, `file_type`, `publication_date`. **The aggregations are the
  best bulk-characterisation tool on the service** and cost one request.
- No API key is required for public reads. Deposit requires OAuth.

### 8.2 Rate limits

Observed response headers, 2026-09-01 (S1) [API]:

```
x-ratelimit-limit: 133
x-ratelimit-remaining: 114
x-ratelimit-reset: 1788321021
retry-after: 1
access-control-expose-headers: …X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
```

So an unauthenticated client gets **133 requests per window** with the reset exposed in
headers. Honour them; they are machine-readable, so there is no excuse for not doing so.

### 8.3 OAI-PMH

Endpoint `https://zenodo.org/oai2d`. `Identify` response, 2026-09-01 (S5) [API]:

```xml
<repositoryName>Zenodo</repositoryName>
<baseURL>https://zenodo.org/oai2d</baseURL>
<protocolVersion>2.0</protocolVersion>
<adminEmail>info@zenodo.org</adminEmail>
<earliestDatestamp>2014-02-03T14:41:33Z</earliestDatestamp>
<deletedRecord>no</deletedRecord>
<granularity>YYYY-MM-DDThh:mm:ssZ</granularity>
```

Metadata formats offered (`ListMetadataFormats`, S5) [API]: `marcxml`, `oai_dc`, `dcat`,
`marc21`, `datacite`, `oai_datacite`, `datacite4`, `oai_datacite4`.

Two things to note. First, `earliestDatestamp` is **2014-02-03**, nine months after the
May 2013 launch — OAI-PMH does not expose the earliest deposits' original datestamps.
Second, `deletedRecord: no` means **harvesters are never told about withdrawals**; a
mirror built from OAI-PMH will silently retain tombstoned material. [INF]

### 8.4 Negative controls (as required by house method)

| Probe | Result | Lesson |
|---|---|---|
| `?type=notarealtype123` | **HTTP 200**, `total: 0` | Invalid facets look like empty results |
| `?type=publication&subtype=notarealsubtype123` | **HTTP 200**, `total: 0` | Same |
| `q=zzzqqxnotaword12345` | HTTP 200, `total: 0` | Text search behaves correctly |
| `/api/records/999999999` | **HTTP 404** + explicit message | Record IDs fail cleanly |
| `https://doi.org/10.5281/zenodo.999999999` | **HTTP 404** | Unregistered DOIs fail cleanly |
| `/api/communities/zzz-not-a-real-community-999` | **HTTP 404** | Community slugs fail cleanly |
| `oai2d?verb=NotAVerb` | `<error code="badArgument">` | OAI-PMH validates properly |
| `help.zenodo.org/docs/<bogus>/` | HTTP 404, 9,379 bytes (consistent) | Docs 404s are identifiable by size |

**The single most important row is the first.** Facet-value typos are silent on this API.
Any count you take from a `type=`/`subtype=` filter must be cross-checked against the
`resource_type` aggregation, which enumerates only real values.

### 8.5 robots.txt

`https://zenodo.org/robots.txt` (S1) [WEB] disallows `/search`, `/api`, `/uploads`,
`/records/*/preview` and `/api/records/*/files-archive`; allows `/api/records/*/files`;
sets `Crawl-delay: 10`. Note the tension: `/api` is *disallowed to crawlers* while
simultaneously being the documented, rate-limit-headered public interface. Read it as "do
not spider the API as if it were pages"; scripted API use within the published rate limits
is the intended path. [INF]

### 8.6 Reacquiring a deposit

1. `GET /api/records/<id>` → JSON metadata including a `files` array with
   `key`, `size`, `checksum` (MD5), and a download `links.self`.
2. Fetch each file; **verify the MD5** against the `checksum` field. Zenodo stores and
   re-checks these itself (§5.1), so this is a genuine end-to-end integrity check.
3. For a concept DOI, resolve it first to learn the current version, or use
   `allversions=true` with the `conceptrecid` to enumerate every version.
4. For whole-corpus work, harvest OAI-PMH with `datacite4` rather than scraping.

## 9. Licensing and reuse

- **Author-chosen, and mandatory.** "Users must specify a license for all publicly
  available files" (S3) [DOC]. There is no default licence and no blanket grant to Zenodo.
- **Ownership is unaffected:** "By uploading content, no change of ownership is implied and
  no property rights are transferred to CERN. All uploaded content remains the property of
  the parties prior to submission" (S3) [DOC].
- **Licences observed in practice** on software records (S1) [API]: `bsd-3-clause`
  (pandas, fastspecfit), `mit-license` (Scientific colour maps), `cc-zero` (India ISIN
  Database), `other-open` (YOLOv5).
- **Metadata is CC0.** "Metadata is licensed under CC0, except for email addresses. All
  metadata is exported via OAI-PMH and can be harvested" (S3) [DOC]. **Text and data
  mining of metadata is therefore unambiguously permitted.**
- **Full-text/file mining is *not* blanket-permitted** — it depends on each record's
  licence, which varies per record. `other-open` on a heavily used record like YOLOv5 shows
  you cannot assume a standard licence even for prominent software. Check per record.

## 10. Caveats and controversies

### 10.1 The launch-year conflict (recorded, not resolved by preference)

| Source | Claim |
|---|---|
| Zenodo About page (S2) [DOC] | "Zenodo was launched in **May 2013**" |
| Zenodo's own citation BibTeX (S2) [DOC] | `year = {2013}` |
| Wikipedia, *Zenodo* article (S8) [WEB] | "launched on **8 May 2013**, as the successor of the OpenAIRE Orphan Records Repository" |
| Wikipedia, *List of preprint repositories* (S7) [WEB] | **2011** |

**Assessment [INF]:** the weight of evidence is overwhelmingly on **May 2013**, including
from Wikipedia itself. Wikipedia's *list* is internally inconsistent with Wikipedia's own
*article*. The most plausible explanation is that 2011 refers to the **OpenAIRE Orphan
Records Repository**, the predecessor service Zenodo succeeded, whose content Zenodo
inherited. **I could not verify a launch date for the Orphan Records Repository itself**,
so I cannot confirm 2011 is even correct *for the predecessor* — that specific attribution
remains **[NOT-VERIFIED]**. Report the record as 2013; note the list entry is unreliable.

Wikipedia's article adds a further wrinkle: "It was relaunched as Zenodo in 2015 to provide
a place for researchers to deposit datasets" (S8) [WEB]. That 2015 "relaunch" claim is
**[NOT-VERIFIED]** against any operator source and sits oddly with the 2013 launch; treat
with caution.

### 10.2 It is not really a preprint server

Preprints are 242,779 of 7,231,598 records — **3.4%** (S1) [API]. Zenodo appears on
preprint-repository lists because it accepts preprints, not because it is one. Surveys that
count Zenodo as a preprint server alongside arXiv are comparing different kinds of object.

### 10.3 The corpus is dominated by bulk deposit

`publication-taxonomictreatment` (714,681) is nearly 3× the preprint corpus; the top
subject keywords are all biodiversity terms; 310,066 records are tagged as sourced from the
Biodiversity Heritage Library (S1) [API]. Any statistical claim about "research on Zenodo"
that does not control for this is measuring a taxonomic ingestion pipeline. [INF]

### 10.4 Zero-cost DOIs invite abuse

Anyone can register and mint DOIs at no cost with no screening (§4). The published control
is post-hoc revocation. See §5.6 — I have **no verified figures** on abuse volume.

### 10.5 Concept-DOI mis-citation

Because the concept DOI silently follows the latest version (§6.1, verified), a paper that
cites a concept DOI has *not* pinned the code it ran. This is a widespread and under-noticed
reproducibility failure. [INF]

### 10.6 Single-institution concentration

Retention is explicitly tied to CERN's institutional lifetime, with no SLA and a
best-efforts succession plan (§5.3–5.4). This is a well-run, transparently-documented risk
— but it is a risk, and Zenodo says so itself more clearly than most.

## 11. Sources

- **S1** — Zenodo REST API, `https://zenodo.org/api/records/` (with `size`, `type`,
  `subtype`, `allversions`, `q`, `sort` parameters), `https://zenodo.org/api/communities`,
  and `https://zenodo.org/robots.txt`. Retrieved **2026-09-01** (server timestamps
  2026-09-02T03:4x–03:5xZ). Supports: all record counts, resource-type and subtype tables,
  access-status and file-type distributions, publication-year growth, version ratios,
  community counts, keyword counts, rate-limit headers, landmark deposit metadata,
  artifact-evaluation examples, negative controls.
- **S2** — Zenodo, *About*, `https://about.zenodo.org/`. Retrieved 2026-09-01. Supports:
  May 2013 launch, OpenAIRE/EC origin, catch-all design philosophy, InvenioRDM, the
  Zenodotus naming, citation BibTeX with `year = {2013}`.
- **S3** — Zenodo, *General Policies v1.0*, `https://about.zenodo.org/policies/`.
  Retrieved 2026-09-01. Supports: eligible depositors, data-quality disclaimer, 50 GB
  limit, licence requirement, CC0 metadata, revocation and withdrawal, versioning,
  replicas, retention period, functional-preservation disclaimer, fixity, succession plans.
- **S4** — Zenodo, *Principles*, `https://about.zenodo.org/principles/`. Retrieved
  2026-09-01. Supports: the no-SLA statement and FAIR mapping.
- **S5** — Zenodo OAI-PMH, `https://zenodo.org/oai2d?verb=Identify`,
  `?verb=ListMetadataFormats`, `?verb=NotAVerb`. Retrieved 2026-09-01. Supports:
  earliestDatestamp 2014-02-03, `deletedRecord: no`, eight metadata formats, error handling.
- **S6** — Zenodo FAIR/metadata statements within S4 (DataCite schema compliance, DOI on
  every published record).
- **S7** — Wikipedia, *List of preprint repositories*, wikitext retrieved via the MediaWiki
  API, 2026-09-01. Supports: the "2011" launch year and ">100,000" size claim for Zenodo,
  and the comparison entries for figshare, Authorea, Synthical, BioHackrXiv.
- **S8** — Wikipedia, *Zenodo*, retrieved via MediaWiki API, 2026-09-01. Supports: "8 May
  2013", OpenAIRE Orphan Records Repository predecessor, CERN "marginal activity" and
  CERN & Society Foundation funding, Invenio, the (unverified) 2015 relaunch claim.
- **S9** — Zenodo Docs, *GitHub and Software → Enable a repository*,
  `https://help.zenodo.org/docs/github/enable-repository/`. Retrieved 2026-09-01.
  Supports: the four setup steps and automatic ingest of new releases.
- **S10** — Zenodo Docs, *Describe software → CITATION.cff file*,
  `https://help.zenodo.org/docs/github/describe-software/citation-file/`. Retrieved
  2026-09-01. Supports: `.zenodo.json` precedence over `CITATION.cff`, subset-schema
  implementation, cff-convert validation, Zenodo's stated long-term metadata direction.
- **S11** — DOI resolution probes via `https://doi.org/…` for
  `10.5281/zenodo.3509134` (concept), `10.5281/zenodo.21500199` (version) and
  `10.5281/zenodo.999999999` (negative control); plus `/api/records/999999999`.
  Retrieved 2026-09-01. Supports: §6.1 concept-vs-version resolution behaviour.
- **S12** — Zenodo Docs, *GitHub and Software* index and *Archive software*,
  `https://help.zenodo.org/docs/github/` and
  `https://help.zenodo.org/docs/github/archive-software/`. Retrieved 2026-09-01.
  Supports: the Software Heritage archival relationship and the single-compressed-file
  eligibility rule. Sub-pages below `archive-software/` returned HTTP 404 at retrieval.
- **S13** — Zenodo Docs, *Manage versions*,
  `https://help.zenodo.org/docs/deposit/manage-versions/`. Retrieved 2026-09-01.
  Supports: new-version workflow, file import between versions, "completely new record
  with separate metadata, files and persistent identifier… linked to all previous and
  future versions".
