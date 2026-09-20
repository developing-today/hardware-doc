# Open-access full text after the preprint — where the published paper is legally free

- **Compiled:** 2026-09-02. Every figure below was measured on that date unless stated otherwise.
- **The question:** *I have a citation. I want the published paper as a PDF, legally, without
  paying.* The rest of this directory is about **preprints** — the author's copy, before or
  alongside peer review. This record is about the other half of the problem: **where the version
  of record, or a legitimate copy of it, is openly available**, and the exact order in which to
  look.
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).
- **Companion records:** [`government-and-institutional-technical-reports.md`](government-and-institutional-technical-reports.md)
  (grey literature, which this file deliberately excludes), [`techrxiv.md`](techrxiv.md) (the IEEE
  route), [`cryptology-eprint-archive.md`](cryptology-eprint-archive.md) (the IACR route),
  [`arxiv.md`](arxiv.md), [`hal.md`](hal.md).

> **Scope note, stated up front.** Nothing in this record involves Sci-Hub, Library Genesis, or any
> other infringing source. Every route documented here is either (a) the publisher giving the paper
> away, (b) an author exercising a self-archiving right the publisher granted, or (c) a public
> funder mandating deposit. Where a route is legally grey — ResearchGate is the obvious case —
> that is said plainly in §5.

---

## 1. The decision ladder

Run these in order. Each rung is cheap; the expensive rungs are at the bottom. In practice
**rungs 1–3 resolve the large majority of computing and electronics citations**, and rung 4 —
"is this a USENIX paper?" — resolves a large part of what rungs 1–3 miss.

| # | Rung | Cost | What it catches |
|---|---|---|---|
| **1** | **Unpaywall** on the DOI (§2.1) | one HTTP call | Anything with a DOI-linked OA copy anywhere |
| **2** | **Semantic Scholar** `externalIds.ArXiv` (§2.3) | one HTTP call | **The arXiv copy Unpaywall misses.** See the trap in §2.1 |
| **3** | **OpenAlex** `locations[]` (§2.2) | one HTTP call | Repository copies, and the venue's own OA status |
| **4** | **Is the venue free by policy?** (§3) | zero, if you know | USENIX (all of it), IACR, PMC, DOAJ journals |
| **5** | **CORE / BASE / OpenAIRE** full-text search (§2.4–2.6) | one call each | Institutional-repository copies with no DOI link |
| **6** | **dblp** → conference/journal page → publisher (§2.8) | two calls | Half-remembered CS citations; canonical bibliographic form |
| **7** | **Author's page / institutional repository** (§4) | manual | Everything above missed, especially pre-2000 work |
| **8** | **Grey literature** — is it a tech report, not a paper? | manual | RISC-V, Xerox PARC, DEC SRC — see the [companion record](government-and-institutional-technical-reports.md) |
| **9** | **Email the author** | slow | Genuinely the last legal rung, and it works |

**The single most common mistake** is stopping at rung 1. §2.1 documents a measured case where
Unpaywall *and* OpenAlex both return `closed` for a paper whose full text has been on arXiv since
2017.

---

## 2. Discovery and resolver layer

### 2.1 Unpaywall — the first call you should make

- **URL:** https://unpaywall.org/ · **API:** `https://api.unpaywall.org/v2/<doi>?email=<you>`
- **Operator:** OurResearch (formerly Impactstory), a US 501(c)(3).

Unpaywall answers exactly one question — *for this DOI, is there a legal free copy, and where?* —
and it answers it in one unauthenticated HTTP call. It is the backbone under a large amount of
other infrastructure: OpenAlex's OA fields are Unpaywall's (§2.2), and browser extensions and
library link resolvers consume the same endpoint.

**Corpus size: [NOT-VERIFIED].** `unpaywall.org` serves a **1,421-byte SPA shell for every path
tried** — `/`, `/products/api`, `/products/data-feed`, `/faq` all returned HTTP 200 with exactly
1,421 bytes (S1). This is the same failure mode as the `osf.io` trap recorded in
[README §4](README.md#6-probing-traps): status code *and* byte size are both uninformative. No
claimed corpus figure could be read from the operator's own site. What *can* be measured is the
data snapshot (below) and the OA totals in OpenAlex (§2.2), which are derived from Unpaywall.

**The `oa_status` colour taxonomy.** This is the vocabulary the whole field uses, and the
distinctions are load-bearing:

| Value | Means | Durability |
|---|---|---|
| `gold` | Published in a fully-OA journal. The version of record is free at the publisher | High — the journal's business model depends on it |
| `hybrid` | A subscription journal, but this article was made OA (usually by an APC) | High |
| `bronze` | **Free to read at the publisher, but with no open licence.** A promotional or discretionary decision | **Low — this can be revoked at any time** |
| `green` | Free copy in a repository (arXiv, PMC, an institutional repo), not at the publisher | Medium–high; depends on the repository |
| `closed` | No free copy known to Unpaywall | — |

**`bronze` is the one to be suspicious of.** It means the publisher is currently choosing to let
you read it and has granted no licence to redistribute or mine it. If a `bronze` link matters to
your work, save a copy.

**`best_oa_location`** is Unpaywall's own pick among `oa_locations[]`. It prefers the
`publishedVersion` at the publisher over an `acceptedVersion` in a repository. The fields that
matter on it are `url_for_pdf` (direct PDF, may be null), `url_for_landing_page`, `version`
(`publishedVersion` / `acceptedVersion` / `submittedVersion`), `host_type`
(`publisher` / `repository`), and `license`.

#### Worked examples [API], all retrieved 2026-09-02 (S2)

```bash
curl -s "https://api.unpaywall.org/v2/10.1109/SP.2019.00002?email=you@your.org" | jq '{
  title, oa_status, is_oa,
  best: .best_oa_location | {host_type, version, url_for_pdf},
  n: (.oa_locations | length) }'
```

| DOI | Paper | `oa_status` | `best_oa_location` | n locations |
|---|---|---|---|---|
| `10.1038/nature12373` | (control, a Nature article) | *see note* | publisher, `publishedVersion`, `nature.com/articles/nature12373.pdf` | — |
| `10.1109/SP.2019.00002` | **Spectre Attacks** | **gold** | `publishedVersion`, `ieeexplore.ieee.org/ielx7/8826229/8835208/08835233.pdf` | 4 |
| `10.1145/2517349.2522738` | **Naiad** | **gold** | `publishedVersion`, `dl.acm.org/ft_gateway.cfm?id=2522738&type=pdf` | 1 |
| `10.1109/ISCA.2014.6853210` | **RowHammer** (Kim et al. 2014) | **closed** | `null` | 0 |
| `10.1109/JPROC.2017.2761740` | Sze et al., *Efficient Processing of DNNs* | **closed** | `null` | 0 |
| `10.1145/3079856.3080246` | **In-Datacenter Performance Analysis of a TPU** | **closed** | `null` | 0 |

#### The trap that matters most in this whole file

The last two rows are **wrong in practice**. Both papers have been openly readable on arXiv for
years — [`1703.09039`](https://arxiv.org/abs/1703.09039) and
[`1704.04760`](https://arxiv.org/abs/1704.04760), both verified in
[`arxiv.md` §7.5](arxiv.md). Unpaywall reports `closed`, `oa_locations: []`, for both.

The reason is structural, not a bug: **Unpaywall is a DOI-keyed index.** If the arXiv record does
not carry the publisher DOI, and the publisher's Crossref record does not carry a relation to the
arXiv ID, there is no edge for Unpaywall to follow. Most authors never add the DOI to their arXiv
metadata after acceptance.

**Consequence for the ladder: a `closed` from Unpaywall is not an answer, it is a prompt to check
arXiv.** Rung 2 exists entirely because of this. Measured cross-check on the TPU paper, same day
(S3, S4):

| Service | Verdict |
|---|---|
| Unpaywall | `oa_status: closed`, 0 locations |
| OpenAlex | `open_access.is_oa: false`, `oa_status: closed`, `best_oa_location: null`, `any_repository_has_fulltext: false` |
| **Semantic Scholar** | `externalIds.ArXiv: "1704.04760"` — **the answer, sitting in a metadata field** |

Note also that Semantic Scholar contradicts *itself* on this record: `isOpenAccess: true` while
`openAccessPdf.status: "CLOSED"` and `openAccessPdf.url` points at an ACM gateway. Do not trust
`isOpenAccess`; read `externalIds`.

#### Access, limits and negative controls (S1, S2)

- **The `email` parameter is mandatory and is filtered.** No email → HTTP **422**, 142-byte JSON,
  `"Email address required in API call"`. Using the obvious shared placeholder
  `research@example.com` → HTTP **422**, 154 bytes, `"Please use your own email address in API
  calls."` A distinct address on the same domain worked. **Use a real address you control.**
- **Negative control:** `10.1109/ZZZZ.9999.9999999` → HTTP **404** with a 207-byte Flask HTML
  body. Unpaywall's status codes are trustworthy, unlike several hosts in
  [`retrieval-notes.md`](retrieval-notes.md).
- **No published numeric rate limit was found** (the FAQ is inside the unreadable SPA).
  **[NOT-VERIFIED]** — treat 100k/day as folklore, not fact, and throttle.

#### Bulk data

The full snapshot bucket is **listable anonymously** [API] (S5):

```bash
curl -s "https://unpaywall-data-snapshots.s3.us-west-2.amazonaws.com/?list-type=2" | less
```

| Snapshot | Size (gzipped JSONL) |
|---|---|
| `unpaywall_snapshot_2018-03-29T113154.jsonl.gz` (oldest) | 16,291,678,484 B (≈16.3 GB) |
| `unpaywall_snapshot_2022-03-09T083001.jsonl.gz` | 29,470,830,470 B (≈29.5 GB) |
| **`unpaywall_snapshot_2024-11-27T031702.jsonl.gz` (newest in the bucket)** | **39,234,162,157 B (≈39.2 GB)** |

**Flag:** the newest public snapshot in that bucket is dated **2024-11-27**, i.e. ~21 months stale
as of this record's compile date. The live API is current; the free bulk drop is not. Current bulk
data moved to a paid "Data Feed" product [INF, from the product URL existing]. If you need
up-to-date OA status in bulk, use **OpenAlex's snapshot** (§2.2), which is free and current.

### 2.2 OpenAlex — the graph around the paper

- **URL:** https://openalex.org/ · **API:** `https://api.openalex.org` · **Operator:** OurResearch
  (the same non-profit as Unpaywall).
- **Lineage:** the declared successor to **Microsoft Academic Graph**, which Microsoft shut down at
  the end of 2021. The MAG identifiers survive inside OpenAlex and Semantic Scholar records — the
  TPU paper above still carries `MAG: 2953212265` in S2 (S4).

**Measured size, 2026-09-02** [API] (S6):

| Entity | Count |
|---|---|
| `works` | **321,988,823** |
| `authors` | 126,403,013 |
| `sources` (journals, conference series, repositories) | 256,025 |
| `institutions` | 136,136 |
| `publishers` | 10,708 |

**OA breakdown of all 321,988,823 works** — `GET /works?group_by=open_access.oa_status` (S7).
The buckets sum **exactly** to the total, so nothing is double-counted:

| `oa_status` | Works | Share |
|---|---|---|
| closed | 199,957,917 | 62.1% |
| **green** | **66,803,663** | **20.7%** |
| diamond | 17,714,822 | 5.5% |
| gold | 15,248,052 | 4.7% |
| bronze | 13,156,096 | 4.1% |
| hybrid | 9,108,273 | 2.8% |
| **Total OA** | **122,030,906** | **37.9%** [INF, summed] |

Two things worth noticing. First, **OpenAlex has added a `diamond` bucket that Unpaywall's classic
five-colour taxonomy does not have** — gold-without-an-APC, split out of `gold`. If you are
comparing an OpenAlex figure to a pre-2023 Unpaywall figure, they are not the same denominators.
Second, **`green` is by far the largest OA category**: repository self-archiving, not publisher
generosity, is what makes most of the literature readable.

**Fields to read on a work:**

- `open_access` → `{is_oa, oa_status, oa_url, any_repository_has_fulltext}`. The last flag is the
  useful one for rung 3 — it tells you a repository copy exists even when `best_oa_location` is a
  publisher.
- `best_oa_location` → same shape as Unpaywall's, plus a nested `source` object naming the host.
- **`locations[]`** → *every* known copy, each with `version`, `pdf_url`, `license`, `source`.
  This is the field to iterate when you are hunting; `best_oa_location` is the field to read when
  you just want one link.

**Rate limits — these changed, and the change is not folklore.** OpenAlex now returns credit- and
cost-denominated headers [API] (S8):

```
x-ratelimit-limit: 1000          x-ratelimit-limit-usd: 0.1
x-ratelimit-remaining: 742       x-ratelimit-remaining-usd: 0.0742
x-ratelimit-cost-usd: 0.0001     x-ratelimit-credits-used: 1
x-ratelimit-reset: 63043
```

and the JSON body carries `meta.cost_usd: 0.0001` per call. Anonymous access is metered at
**1,000 credits / $0.10 per reset window** (reset counter observed at 63,043 s ≈ 17.5 h).
A `db_response_time_ms` is also returned. **Read these headers in your harvester** — a scraper
written against the old "polite pool, 100k/day, add your email" documentation will silently start
failing.

**Bulk snapshot** — free, anonymous, and current [API] (S9):

```bash
curl -s "https://openalex.s3.amazonaws.com/?list-type=2&delimiter=/"
# → LICENSE.txt, README.txt, RELEASE_NOTES.txt, browse.html
#   data/ , legacy-data/
curl -s "https://openalex.s3.amazonaws.com/?list-type=2&delimiter=/&prefix=data/"
# → data/jsonl/ , data/parquet/
```

The **parquet** layout is new relative to the widely-cited jsonl-only descriptions; both are
present. Note the `legacy-data/` prefix — an older layout is retained, so scripts written against
the old paths will still work but will get stale data. `data/works/` — the path many older
tutorials use — returned `KeyCount 0`.

### 2.3 Semantic Scholar and S2ORC

- **API:** `https://api.semanticscholar.org/graph/v1` · **Operator:** Allen Institute for AI (AI2).

Semantic Scholar earns its place at **rung 2** for one reason: `externalIds`. A single call gives
you the DOI, the arXiv ID, the DBLP key, the legacy MAG ID, the PubMed IDs and the S2 CorpusId —
which means one call converts *any* identifier you happen to have into all the others. Measured
example (S4):

```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3079856.3080246\
?fields=title,isOpenAccess,openAccessPdf,externalIds"
```
```json
{"paperId":"2dfeb5a90abc49ab2a80a492a01a4e2c8e92ec22",
 "externalIds":{"DBLP":"conf/isca/JouppiYPPABBBBB17","MAG":"2953212265",
                "ArXiv":"1704.04760","DOI":"10.1145/3079856.3080246","CorpusId":4202768},
 "title":"In-datacenter performance analysis of a tensor processing unit",
 "isOpenAccess":true,
 "openAccessPdf":{"url":"http://dl.acm.org/ft_gateway.cfm?id=3080246&type=pdf","status":"CLOSED","license":null}}
```

`openAccessPdf` gives `{url, status, license}` where `status` reuses the Unpaywall colour
vocabulary. **As shown, `isOpenAccess` and `openAccessPdf.status` can disagree inside one record.**
Prefer `openAccessPdf.status` and, above all, `externalIds.ArXiv`.

- **Auth:** the `graph/v1` endpoint answered unauthenticated. Bogus DOI → HTTP **404** (clean).
- **Rate limits without a key are real but unpublished in the response headers**
  **[NOT-VERIFIED]**; AI2 issues free API keys on application.

**S2ORC — the full-text corpus.** Semantic Scholar's differentiator is that it parses open-access
PDFs into structured full text. The bulk datasets API is public even though the downloads are not
(S10, release `2026-08-25`):

```bash
curl -s https://api.semanticscholar.org/datasets/v1/release/latest   # public, no key
curl -s https://api.semanticscholar.org/datasets/v1/release/latest/dataset/s2orc
# → 401 {"error":"A valid API key is required"}      (40 bytes)
```

Datasets in release `2026-08-25`: `abstracts`, `authors`, `citations`,
`embeddings-specter_v1`, `embeddings-specter_v2`, `paper-ids`, `papers`, `publication-venues`,
`s2orc`, `s2orc_v2`, `tldrs`. Sizes from the operator's own descriptors [API]:

| Dataset | Contents |
|---|---|
| `papers` | "The core attributes of a paper… **200M records in 30 1.5 GB files**" |
| `s2orc` | "Full-body paper text parsed from open-access PDFs… **10M records in 30 4 GB files**" |
| **`s2orc_v2`** | "…structural elements such as sentences and paragraphs, and bibliographic references. **16M records in 30 6 GB files**" |

**How to get bulk access:** request a free API key from AI2 (the `/datasets/` endpoints return
`401 {"error":"A valid API key is required"}` until you attach one as `x-api-key`). The
*listing* is open; the *payload* is not.

### 2.4 CORE — the largest aggregator of open-access full text

- **URL:** https://core.ac.uk/ · **Operator:** The Open University (UK), community-governed,
  not-for-profit.

CORE is the one to reach for at rung 5, because it is the only service in this section that
**harvests and stores the full text** at scale rather than linking to it. Its own home page, as
served on 2026-09-02, states **"Search 452M papers from around the world"** and describes itself
as "The world's largest collection of open access research papers" [WEB] (S11). That 452 M is a
*paper* count across ~thousands of harvested repositories; it is not 452 M distinct full texts,
and CORE does not, on that page, separate the two. Recorded as stated, with the caveat.

**API.** `https://api.core.ac.uk/v3/search/works` — **requires a key**. An unauthenticated call
returned HTTP **301** (776-byte body), not a 401, which is a mildly misleading signal (S12).
Keys are free on registration.

**Bulk dataset** [DOC] (S13) — CORE's differentiator, and genuinely large:

| Release | Compressed | Extracted |
|---|---|---|
| **2024-07-12** (latest listed) | **749 GB** | ~2.7 TB |
| 2023-03-18 | 393 GB | 3.5 TB |
| 2022 | 393 GB | 3.5 TB |

The 2024 release is split into per-batch archives indexed by a credentialed
`dataset_index.xml`; access is by registration, and CORE's documentation explicitly recommends
`aria2`/`wget -c` because of the size.

Other CORE services worth knowing: **FastSync** (incremental sync rather than a full re-download),
the **OAI Resolver** (maps OAI identifiers to records), and a **Recommender** widget.

### 2.5 BASE — Bielefeld Academic Search Engine

- **URL:** https://www.base-search.net/ · **Operator:** Bielefeld University Library.

BASE is the other classic repository aggregator and is a major upstream source for Unpaywall.

**Probe result, 2026-09-02: blocked.** `https://www.base-search.net/` returned HTTP 200 with a
**7,846-byte Anubis proof-of-work challenge page**, `Anubis version v1.27.0+dirty`, footer "This
website is hosted by Bielefeld University Library" [WEB] (S14). This is the *third* scholarly host
in this survey behind Anubis — see [`retrieval-notes.md` §3](retrieval-notes.md), which records
the same wall on `econstor.eu` and `hprints`. **The user-agent ladder in
[`AGENTS.md`](../../AGENTS.md) does not defeat a JS proof-of-work.**

**Size: [NOT-VERIFIED] on this date** — the counter is behind the wall. BASE's documented
machine interface is an IP-whitelisted OAI-style API granted on written application, consistent
with the general rule from `retrieval-notes.md`: *when the web front end is walled, look for the
machine interface.*

### 2.6 OpenAIRE Explore

- **URL:** https://explore.openaire.eu/ (200, 66,171 B) · **API:** `https://api.openaire.eu`
- **Operator:** the OpenAIRE AMKE, EU-funded; the research-output layer of the European Open
  Science Cloud.

**Measured size, 2026-09-02** [API] (S15):

```bash
curl -s "https://api.openaire.eu/search/publications?size=0"
# <total>238449827</total>
```

**238,449,827 publications** for the query `(oaftype exact result) and (resulttypeid exact
publication)`. JSON is available with `&format=json`. Note that `https://v3.openaire.eu/api/...`
— the endpoint some documentation points at — **timed out entirely** (`http=000`) on the probe
date; the `api.openaire.eu` host is the one that answers.

OpenAIRE's distinctive value is **funder linkage**: it connects publications to EU grant numbers,
so it answers "what came out of this project" in a way that Unpaywall and CORE cannot.

### 2.7 DOAJ — Directory of Open Access Journals

- **URL:** https://doaj.org/ · **API:** `https://doaj.org/api/search/{journals,articles}/<q>`

DOAJ operates one level up: it curates **journals**, not articles, against a published set of
criteria. It is the answer to *"is this journal actually open access, or is it a predatory
lookalike?"* — inclusion is a positive quality signal, and DOAJ removes titles that stop meeting
its criteria.

**Measured, 2026-09-02** [API] (S16):

```bash
curl -s "https://doaj.org/api/search/journals/*?pageSize=1" | jq .total   # 23384
curl -s "https://doaj.org/api/search/articles/*?pageSize=1" | jq .total   # 13535801
```

| | Count |
|---|---|
| Journals indexed | **23,384** |
| Article records indexed | **13,535,801** |

The API answered unauthenticated with no fallback UA needed. Practical use: before citing a
journal you have not heard of, look it up in DOAJ. Absence is not proof of anything, but presence
means a human checked the licence, the peer-review statement and the editorial board.

Cross-reference: [`preprints-org.md`](preprints-org.md) documents why "is it in DOAJ" is a weaker
test than it looks when one publisher operates both the preprint server and the journals.

### 2.8 dblp — the canonical CS bibliography

- **URL:** https://dblp.org/ · **Operator:** Schloss Dagstuhl – Leibniz-Zentrum für Informatik.

**dblp hosts no full text at all.** It is in this file anyway, because it solves the *other* half
of the problem: **it is where you resolve a half-remembered CS citation into a canonical one.**
"That Jouppi TPU paper, ISCA, around 2017" is not a query Unpaywall can answer — it needs a DOI.
dblp will take the fragment and give you the exact title, the full author list, the venue, the
year, the DOI and the arXiv ID, and *then* rungs 1–3 become possible.

dblp's discipline is its real product: author-name disambiguation, one record per publication with
its journal/conference versions linked, and stable `conf/isca/JouppiYPPABBBBB17`-style keys —
which, as §2.3 showed, Semantic Scholar carries in `externalIds.DBLP`.

**API** [API] (S17), no key, no UA fallback needed:

```bash
curl -s "https://dblp.org/search/publ/api?q=RISC-V&format=json&h=1" | jq '.result.hits."@total"'
# 2313
curl -s "https://dblp.org/search/publ/api?q=<title words>&format=json&h=10"   # publications
curl -s "https://dblp.org/search/author/api?q=<name>&format=json"             # authors
curl -s "https://dblp.org/search/venue/api?q=<venue>&format=json"             # venues
```

`RISC-V` returns **2,313** publication hits — worth comparing with the 250 `ti:"RISC-V" AND
cat:cs.AR` arXiv hits recorded in [`arxiv.md` §7.5](arxiv.md). dblp indexes the *published*
literature; arXiv indexes what authors posted.

**Bulk XML dump** [API] (S18):

```
https://dblp.org/xml/dblp.xml.gz
  HTTP/2 200 · content-length: 1,099,942,370 (≈1.10 GB gzipped)
  last-modified: Tue, 01 Sep 2026 23:47:15 GMT
```

Rebuilt daily — the dump measured here was **less than 24 hours old**. The accompanying
`dblp.dtd` must be fetched alongside it or the XML will not parse. The dump is released under
**CC0**, which makes dblp the least legally encumbered bibliographic dataset in this file.

---

## 3. Publisher-side venues that are genuinely free

### 3.1 USENIX — the single most important entry in this file

- **URL:** https://www.usenix.org/

**Every paper in every USENIX proceedings is free to download, with no registration, no
membership and no paywall.** This covers **OSDI, NSDI, ATC (USENIX Annual Technical Conference),
FAST, USENIX Security, SOUPS, HotOS, LISA, OSDI/EuroSys-adjacent workshops** and the rest of the
USENIX programme.

**Why this is the headline.** A sibling record in this directory established that the canonical
systems literature is largely **absent from preprint servers** —
[`arxiv.md`](arxiv.md) and [`landmark-papers.md`](landmark-papers.md) both record that the
foundational OSDI/NSDI/FAST-line papers were never posted to arXiv. If you have been looking for
those papers on a preprint server, you have been looking in the wrong place for a decade.
**USENIX is where they actually are, and they have been free the entire time.**

**The policy, in USENIX's own words** [DOC], retrieved 2026-09-02 from `usenix.org/about` and
`usenix.org/conferences/open-access` (S19, S20):

> "We banished paywalls in **2008** for both conference authors and readers, providing conference
> proceedings and recordings free of charge under our open access policy."

> "USENIX compiles and publishes accepted research papers as proceedings for each of these
> conferences, making them freely available on [our website]."

USENIX also states it relies on **sponsor support** to fund this, and notes that "recorded
presentations of our events are publicly available after each event" — so the *talks* are free
too, which is unusual and frequently more useful than the paper for a systems result.

**Verified retrieval** [WEB] (S21), 2026-09-02, plain Chrome-131 UA, no auth:

| URL | Result |
|---|---|
| `https://www.usenix.org/conference/osdi24/technical-sessions` | HTTP 200, 259,550 B |
| `https://www.usenix.org/system/files/osdi24_full_proceedings.pdf` | **HTTP 200, 83,779,378 B, magic `%PDF-`** |
| `https://www.usenix.org/system/files/osdi24_proceedings_interior.pdf` | HTTP 200, 82,578,353 B, `%PDF-` |
| *negative control* `.../osdi24-nonexistent-author-xyz.pdf` | HTTP **404**, 16,889-byte themed body |

The negative control matters: USENIX returns a **correct 404 status** but with a large themed HTML
body, so a harvester must check the status code or the magic bytes, not the content length.

**Practical shortcuts.**

- Every conference has a `/conference/<venue><yy>/technical-sessions` page listing every paper
  with a direct PDF link, a BibTeX entry, the slides and usually the video.
- The whole proceedings ship as one PDF (`<venue><yy>_full_proceedings.pdf`) — 84 MB for OSDI '24.
  Grab it once rather than 60 individual files.
- Papers also appear in ACM DL and IEEE Xplore for some co-sponsored events. **Always take the
  USENIX copy** — same content, no paywall, no login.

**Caveat, stated honestly:** URLs under `/system/files/` and `/sites/default/files/` are Drupal
paths and are not obviously permanent identifiers. Conference landing pages have been stable for
many years [INF], but the file paths carry no DOI. If a USENIX paper is load-bearing for your
work, keep a local copy.

### 3.2 ACM Digital Library

More complicated than USENIX, and the honest summary is **"partly, and it depends".**

- **ACM OPEN** is ACM's transformative read-and-publish agreement. From ACM's own library-facing
  page, retrieved 2026-09-02 [DOC] (S22): *"ACM OPEN is our transformative read and publish model,
  offering participating institutions unlimited open access publishing in the Digital Library and
  unlimited read access to its full text contents."* The mechanism is **institutional**: if the
  corresponding author's institution is an ACM OPEN participant, that paper is published OA in the
  DL at no cost to the author. If not, it is not. ACM maintains a public **Participant List** and a
  **FAQ** off `libraries.acm.org/acmopen`.
- **Consequence you can act on:** whether an ACM paper is free depends on *who wrote it*, not on
  which conference it appeared at. Two papers in the same SIGCOMM proceedings can differ. This is
  why Naiad (SOSP '13) resolves `gold` with a working `dl.acm.org/ft_gateway.cfm` PDF (§2.1) while
  the TPU paper (ISCA '17, ACM-published) resolves `closed`.
- **OpenTOC** is the older mechanism: ACM grants a SIG the right to host a free table of contents
  with working full-text links for a conference, usually for a limited period around the event.
  **Probe result:** `https://dl.acm.org/opentoc` returned HTTP **403 with a 5,635-byte body** —
  the Cloudflare challenge fingerprint documented in
  [`retrieval-notes.md` §1](retrieval-notes.md). Blocked, not broken; the current per-conference
  OpenTOC list is **[NOT-VERIFIED]** (S23).
- **Author-izer** was ACM's older per-author free-link generator, embedded on author home pages.
  Links minted through it still circulate. **[NOT-VERIFIED]** whether new links can still be
  created.
- `www.acm.org/publications/openaccess` and `libraries.acm.org/acmopen` both served HTTP 200
  (76,905 B and 43,294 B) to the Chrome-131 UA; `libraries.acm.org/acmopen/faq` returned **404**
  (S22, S24) — ACM had recently relaunched that site and invites feedback on broken paths in the
  page footer.

**Practical rule for ACM:** check Unpaywall first (`gold` on an ACM DOI usually means a working
`ft_gateway.cfm` link); if `closed`, check arXiv via Semantic Scholar; if still nothing, check
whether the same paper appeared at a USENIX venue or as an institutional tech report.

### 3.3 IEEE

**Mostly paywalled, and there is no way to soften that.** Xplore is a subscription product. Three
legitimate routes:

1. **TechRxiv, via the Crossref `is-preprint-of` relation.** This is the highest-yield route for
   IEEE-bound work and it is documented in detail in the sibling record
   **[`techrxiv.md`](techrxiv.md)** — including the fact that `www.techrxiv.org` is behind a
   Cloudflare challenge (403, 5,620 B) so the *Crossref* API, not the site, is how you query it.
   IEEE sanctions posting to TechRxiv, so the copy is legitimate.
2. **IEEE's own OA journals** — *IEEE Access* is the large one (fully gold OA, APC-funded), plus a
   growing set of topical OA titles and hybrid OA articles in the classic transactions. When an
   IEEE article *is* OA, Unpaywall picks it up cleanly: Spectre (`10.1109/SP.2019.00002`) resolved
   `gold` with a direct `ieeexplore.ieee.org/ielx7/.../08835233.pdf` PDF (§2.1).
3. **Author self-archiving.** IEEE permits authors to post the accepted version to their own
   site, their institutional repository and arXiv/TechRxiv. This is why so much IEEE-published
   work is reachable as `green` OA — recall that `green` is 66.8 M works, 20.7% of OpenAlex (§2.2).

**IEEE *standards* are a separate and worse problem** — see the
[companion record §5](government-and-institutional-technical-reports.md).

### 3.4 IACR — diamond open access done properly

The International Association for Cryptologic Research runs what is, for this survey's purposes,
the cleanest publishing pipeline in computing:

- **Cryptology ePrint Archive** — the preprint layer. Fully documented in
  **[`cryptology-eprint-archive.md`](cryptology-eprint-archive.md)** (27,552 reports [API]),
  which also records the practical access details: no UA fallback needed, but a hard Cloudflare
  **"20 requests per 1 minute" per-path limit with no `Retry-After`**, and an OAI-PMH endpoint
  that returns all identifiers in a single 3.34 MB response.
- **TCHES** (*Transactions on Cryptographic Hardware and Embedded Systems*), **ToSC**
  (*Symmetric Cryptology*) and the **Journal of Cryptology** — the journal layer, published by
  IACR as **diamond OA**: free to read *and* free to publish.

**Why an electronics engineer should care:** TCHES *is* the venue for side-channel analysis, fault
injection, hardware masking, PUFs and post-quantum hardware implementations, and every issue of it
is free. See [`cryptology-eprint-archive.md` §7.6](cryptology-eprint-archive.md).

### 3.5 PMC and Europe PMC

- **PMC:** https://pmc.ncbi.nlm.nih.gov/ (US National Library of Medicine)
- **Europe PMC:** https://europepmc.org/ (EMBL-EBI + Wellcome + a funder consortium)

**Relevant even if you have never touched biology**, for one reason: the **NIH Public Access
Policy** requires deposit of the accepted manuscript of anything NIH funded. That mandate sweeps in
a large amount of **instrumentation, imaging, signal processing, embedded-device and
biomedical-electronics engineering** that was published in paywalled engineering journals. If a
paper had any NIH money behind it, PMC probably has it.

**Measured sizes, 2026-09-02:**

| Measure | Count | Source |
|---|---|---|
| PMC records (`db=pmc`, `all[sb]`) | **12,570,099** | E-utilities [API] (S25) |
| PMC `"open access"[filter]` | **8,192,003** | E-utilities [API] (S25) |
| Europe PMC, all (`*:*`) | **48,813,426** | REST [API] (S26) |
| Europe PMC `SRC:MED` (MEDLINE-sourced) | 41,029,618 | REST [API] (S26) |
| Europe PMC `HAS_FT:Y` (has full text) | **12,106,121** | REST [API] (S26) |
| Europe PMC `OPEN_ACCESS:Y` | **8,056,165** | REST [API] (S26) |

The two OA figures — 8,192,003 (PMC) and 8,056,165 (Europe PMC) — agree to within 1.7%, which is
reassuring given they are computed by different organisations from partly different pipelines
[INF].

**APIs.**

```bash
# Europe PMC — no key, no UA fallback needed, JSON or XML
curl -s "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=OPEN_ACCESS:Y&format=json&pageSize=1"

# NCBI E-utilities — counts and ID lists
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=all%5Bsb%5D&retmax=0"
```

Europe PMC's query language is the one to learn: `HAS_FT:Y`, `OPEN_ACCESS:Y`, `SRC:PPR`
(preprints), `GRANT_AGENCY:"..."`, `METHODS:"..."` (searches inside the methods section — genuinely
useful for finding instrument descriptions).

**Bulk.** The **PMC Open Access Subset** is distributed as bulk packages over FTP/HTTPS and on
AWS S3 (`pmc-oa-opendata`), split into a **Commercial Use** collection (CC0/CC-BY/CC-BY-SA) and a
**Non-Commercial Use** collection (CC-BY-NC variants) — read the licence split before mining.
**Caveat from the probe:** the classic OA web service `.../pmc/utils/oa/oa.fcgi?id=PMCnnnnn`
returned **HTTP 404** on both `www.ncbi.nlm.nih.gov` and `pmc.ncbi.nlm.nih.gov` on 2026-09-02
(S27) — PMC moved to a new domain and the legacy endpoint path in most tutorials is dead. The
exact current OA-service path is **[NOT-VERIFIED]**; the E-utilities and Europe PMC endpoints
above both work and are the safer dependency.

### 3.6 Fully open-access publishers

One paragraph, because the rule is simple: **at a fully-OA publisher every article is free at the
publisher, permanently, under a named Creative Commons licence.** Unpaywall reports them as `gold`
(or `diamond`, in OpenAlex's finer taxonomy). The ones a technical reader meets most:
**PLOS** (non-profit, CC-BY, *PLOS ONE* is a large multidisciplinary venue that carries a lot of
instrumentation and methods work); **Frontiers** (large, fast, CC-BY, uneven — judge the specialty
section, not the brand); **eLife** (non-profit; since 2023 it publishes *reviewed preprints* with
public review reports and no accept/reject decision, which makes it structurally closer to a
preprint server than to a journal — read the reviews, they are the point); and **MDPI**.

**MDPI carries a specific caveat that this directory has already documented.** MDPI is fully OA and
its articles are genuinely free — but see [`preprints-org.md`](preprints-org.md), which records
that MDPI operates **Preprints.org** and that **230 of its 232 "friendly journals" are MDPI
titles**. That is a closed loop between a preprint server and a publisher, and it should inform how
much independent signal you read into an MDPI acceptance. The *access* is real; the *filtering* is
what is in question.

### 3.7 HathiTrust and JSTOR Open Content — older material

Both matter for pre-1990 engineering literature, and both need precision about what is actually
*downloadable* versus merely *readable*.

**HathiTrust** (https://www.hathitrust.org/) — a not-for-profit collaborative of academic and
research libraries, **founded 2008**, "now preserving **19+ million digitized items**" [WEB],
retrieved 2026-09-02 (S28).

- **What you can actually get:** items determined to be **public domain** (in the US, broadly
  pre-1930 plus US government works plus rights-cleared material) are **full-view and downloadable
  as PDF**. Everything else is **search-only** — HathiTrust will tell you the page numbers your
  term appears on and show you nothing else.
- **Full-book PDF download of public-domain items is generally gated on login via a member
  institution**; page-at-a-time viewing is open. Practically: if you are not at a member
  institution, expect to read, not to download.
- Its strength is **serial runs and monographs** — old handbooks, IRE/AIEE-era volumes,
  manufacturer references — not journal articles.

**JSTOR Open Content** (https://about.jstor.org/oa-and-free/) [WEB], retrieved 2026-09-02 (S29):

- **"more than 80,000 open access research reports from 187 think tanks"** — freely downloadable,
  no account. This is a genuine grey-literature collection and overlaps the
  [companion record](government-and-institutional-technical-reports.md).
- **Open Access ebooks** and **open images** collections, also free.
- **"Registered users can read online for free… and access up to 100 free articles every 30
  days."** Note the wording: **read online**, not download. The free tier is a reading room, not a
  file service.
- Everything else on JSTOR is subscription.

**Blunt summary:** HathiTrust and JSTOR are where you *find* old material and often where you
*read* it. Neither is reliably where you *download* it without an institutional affiliation.

### 3.8 CiteSeerX — probed, and the news is bad

- **Historic URL:** https://citeseerx.ist.psu.edu/ (Penn State)

CiteSeerX was, from 1998 onward, the first system to do automated citation indexing over crawled
CS PDFs — the direct ancestor of Google Scholar and Semantic Scholar. For years it was the only
place some 1990s CS papers were indexed in full text.

**Probe result, 2026-09-02 — CiteSeerX has been retired and replaced with a blanket redirect to a
single Internet Archive capture** [WEB] (S30).

Every path tested returned **HTTP 301** to
`https://web.archive.org/web/20251230112235/https://citeseerx.ist.psu.edu//<path>`:

| Path requested | Response |
|---|---|
| `https://citeseerx.ist.psu.edu/` | 301 → Wayback `20251230112235` |
| `https://citeseerx.ist.psu.edu/search?q=raft` | 301 → Wayback, same timestamp |
| `https://citeseerx.ist.psu.edu/robots.txt` | 301 → Wayback, same timestamp |
| `https://citeseerx.ist.psu.edu/bogus-nonexistent-path-xyz` *(negative control)* | 301 → Wayback, same timestamp |
| `http://citeseerx.ist.psu.edu/` (plain HTTP) | 301 → Wayback, same timestamp |

**The negative control is the finding.** A bogus path redirects identically to a real one, and
even `robots.txt` is redirected — meaning nothing is being served from Penn State any more. The
redirect target is a **fixed timestamp, 2025-12-30 11:22:35 UTC**, not a "latest capture" URL. And
following it once returned **HTTP 429** from `web.archive.org` (620-byte body), the Wayback
rate-limit already recorded in [`retrieval-notes.md`](retrieval-notes.md).

**What this means in practice:**

- CiteSeerX is **defunct as a service**. Treat any `citeseerx.ist.psu.edu/viewdoc/...` link in an
  old bibliography as dead, and expect the Wayback replay of it to be slow and rate-limited.
- Its **unique value — cached PDFs of 1990s/2000s CS papers whose original hosts are gone** — is
  not obviously preserved anywhere queryable. The Wayback capture is a *page*, not the index.
- **Substitute:** Semantic Scholar absorbed much of CiteSeerX's role and considerably more of its
  corpus; **CORE** (§2.4) is the right place to search for old repository-held full text.
- This belongs in [`closed-and-defunct-servers.md`](closed-and-defunct-servers.md)'s frame of
  reference even though CiteSeerX was never a preprint server.

---

## 4. Institutional and repository layer

When rungs 1–5 fail, the copy usually still exists — in the author's institutional repository,
where a mandate put it and where no DOI-level link points at it.

**How to find it, in order:**

1. **OpenAlex `locations[]`** (§2.2) already lists repository copies with a `source.display_name`.
   Check this before anything manual.
2. **Search the author's institution directly.** Most universities run EPrints, DSpace or Pure at a
   predictable host (`eprints.<uni>`, `dspace.<uni>`, `research-information.<uni>`,
   `<uni>.figshare.com`). Google site-search works: `site:eprints.example.ac.uk "<title>"`.
3. **CORE** (§2.4) indexes the full text of most of these repositories, which is exactly why it is
   rung 5 rather than rung 8.
4. **National aggregators** where relevant — **HAL** for anything French
   ([`hal.md`](hal.md): 1,788,688 notices **with files** [API]), **NARCIS**-successor services for
   the Netherlands, **CONICET Digital** for Argentina, etc.

**Registries of repositories** — use these to find *which* repository to search:

| Registry | URL | Probe, 2026-09-02 |
|---|---|---|
| **OpenDOAR** | https://v2.sherpa.ac.uk/opendoar/ | **HTTP 403**, **651,922-byte** body (S31) |
| **ROAR** | https://roar.eprints.org/ | **HTTP 200**, 8,593 B (S32) |

**Counts for both are [NOT-VERIFIED].** OpenDOAR's 403 is *not* the ~5.6 kB Cloudflare fingerprint
from [`retrieval-notes.md` §1](retrieval-notes.md) — a 651,922-byte 403 body is a different and
undocumented mechanism, and the same 403 was returned for both `/opendoar/` and
`/view/repository_by_country/`. Jisc's SHERPA v2 API requires a registered `api-key`; the
key-less call returned the same 403 page. ROAR (University of Southampton, EPrints-based) *is*
reachable and is the usable registry of the two today.

Related SHERPA services worth naming even though they were unreachable on the probe date:
**SHERPA RoMEO** (per-journal self-archiving policy — "may I post the accepted version?") and
**SHERPA Juliet** (funder OA mandates). Both live behind the same `v2.sherpa.ac.uk` host.

---

## 5. Green OA and self-archiving — including the parts that are not archives

**Green OA is the largest source of free full text there is** — 66,803,663 works, 20.7% of
OpenAlex, versus 15,248,052 gold and 17,714,822 diamond (§2.2). Most publishers, including IEEE,
ACM, Elsevier and Springer, permit authors to post *some* version somewhere. Which version and
where is the whole game:

| Version | Typical name | Usually allowed |
|---|---|---|
| `submittedVersion` | preprint, as submitted | Almost always |
| `acceptedVersion` | AAM / post-print — peer-reviewed content, publisher's typesetting absent | Usually, often after an embargo |
| `publishedVersion` | version of record, publisher PDF | Only if the article is OA |

An `acceptedVersion` is scientifically equivalent to the version of record. **Its page and line
numbers are not.** If you are quoting or citing a page number, say which version you read.

**Author home pages** remain the single highest-yield manual route, especially for pre-2005 work
and for systems researchers who keep a `publications.html`. Many papers that Unpaywall calls
`closed` are one click from the author's name.

### ResearchGate and Academia.edu — use with your eyes open

Both are **for-profit social networks**, not archives, and this record will not soften that:

- **They are not preservation infrastructure.** No commitment to persistence, no DOIs of their own,
  no succession plan. A link to a ResearchGate PDF is a link to a company's product page.
- **A large share of the full texts were uploaded by authors who did not hold the right to upload
  them.** Publishers have litigated over exactly this; takedowns happen in bulk and the file you
  linked last year may be gone.
- **Access is gated and degrading.** Probed 2026-09-02 with the Chrome-131 UA: `researchgate.net`
  → **HTTP 403** (1,714-byte body); `academia.edu` → **HTTP 403** (5,599 B) (S33). Both refuse
  scripted access; Academia.edu additionally gates much content behind a paid tier.
- **The "Request full-text" button is fine.** It is a mechanised version of emailing the author,
  which is rung 9 and entirely legitimate.

**Recommendation:** treat a ResearchGate hit as evidence the paper exists in reachable form, then
go find a copy in a repository that will still be there in five years. If the ResearchGate copy is
the only one, save it locally and record where it came from.

---

## 6. Practical recipes

Copy-pasteable. `jq` assumed; substitute your own address for `you@your.org` — Unpaywall rejects
shared placeholders (§2.1).

### 6.1 You have a DOI

```bash
DOI="10.1145/3079856.3080246"
EMAIL="you@your.org"

# Rung 1 — Unpaywall
curl -s "https://api.unpaywall.org/v2/${DOI}?email=${EMAIL}" \
  | jq '{title, oa_status, is_oa,
         best: .best_oa_location | {host_type, version, license, url_for_pdf},
         all: [.oa_locations[] | {host_type, version, url_for_pdf}]}'

# Rung 2 — the arXiv ID Unpaywall does not know about   <-- do not skip this
curl -s "https://api.semanticscholar.org/graph/v1/paper/DOI:${DOI}?fields=title,externalIds,openAccessPdf" \
  | jq '{title, arxiv: .externalIds.ArXiv, dblp: .externalIds.DBLP, pdf: .openAccessPdf}'
# if .externalIds.ArXiv is non-null:  https://arxiv.org/pdf/<that id>

# Rung 3 — every location OpenAlex knows
curl -s "https://api.openalex.org/works/doi:${DOI}" \
  | jq '{oa: .open_access,
         locs: [.locations[] | {src: .source.display_name, version, pdf_url, license}]}'

# Rung 5 — full-text aggregators (CORE needs a free key)
curl -s -H "Authorization: Bearer $CORE_KEY" \
  "https://api.core.ac.uk/v3/search/works?q=doi:%22${DOI}%22&limit=5"
curl -s "https://api.openaire.eu/search/publications?doi=${DOI}&format=json" | jq '.response.results'
```

### 6.2 You have only a title (or a fragment of one)

```bash
T="In-Datacenter Performance Analysis of a Tensor Processing Unit"

# Rung 6 first — dblp is the best title->citation resolver in CS. No key.
curl -s -G "https://dblp.org/search/publ/api" \
     --data-urlencode "q=${T}" --data "format=json&h=5" \
  | jq -r '.result.hits.hit[]?.info | "\(.year)  \(.venue)  \(.title)  DOI=\(.doi // "-")  \(.ee // "-")"'

# Then Semantic Scholar's title search, which also gives you the arXiv ID
curl -s -G "https://api.semanticscholar.org/graph/v1/paper/search" \
     --data-urlencode "query=${T}" \
     --data "fields=title,year,venue,externalIds,openAccessPdf&limit=5" | jq '.data'

# Then OpenAlex full-text-ish search, filtered to things that are actually free
curl -s -G "https://api.openalex.org/works" \
     --data-urlencode "filter=title.search:${T},open_access.is_oa:true" \
     --data "per-page=5" \
  | jq -r '.results[] | "\(.publication_year)  \(.display_name)  \(.open_access.oa_url // "-")"'

# feed the DOI you just found back into 6.1
```

### 6.3 You suspect it is a systems paper

```bash
# 1. Is it USENIX? If yes you are already done.
#    https://www.usenix.org/conference/<venue><yy>/technical-sessions
#    e.g. osdi24, nsdi24, atc24, fast24, usenixsecurity24
#    Whole proceedings: https://www.usenix.org/system/files/<venue><yy>_full_proceedings.pdf

# 2. dblp's venue index tells you which venue it was, and dblp links the free copy in `ee`
curl -s "https://dblp.org/search/venue/api?q=OSDI&format=json" | jq -r '.result.hits.hit[]?.info.url'

# 3. If IEEE-published: check TechRxiv via Crossref, not via the (Cloudflare-blocked) site.
#    See techrxiv.md for the is-preprint-of relation query.

# 4. If it is crypto/embedded-security: IACR ePrint + TCHES are both free.
#    See cryptology-eprint-archive.md.

# 5. If it is architecture/ISA-level and nothing above worked, it is probably a
#    TECHNICAL REPORT, not a paper. Go to:
#    government-and-institutional-technical-reports.md
```

### 6.4 Bulk / offline work

```bash
# OpenAlex — free, anonymous, current
curl -s "https://openalex.s3.amazonaws.com/?list-type=2&delimiter=/&prefix=data/"   # jsonl/ , parquet/

# Unpaywall — free but the newest public snapshot is 2024-11-27 (~39.2 GB)
curl -s "https://unpaywall-data-snapshots.s3.us-west-2.amazonaws.com/?list-type=2"

# dblp — daily, CC0, ~1.10 GB gzipped. Fetch the DTD too or it will not parse.
curl -O https://dblp.org/xml/dblp.xml.gz
curl -O https://dblp.org/xml/dblp.dtd

# Semantic Scholar / S2ORC — listing is public, downloads need a free API key
curl -s https://api.semanticscholar.org/datasets/v1/release/latest | jq '.release_id, [.datasets[].name]'

# CORE — 749 GB compressed (2024-07-12), by registration
# PMC OA subset — FTP/HTTPS packages + AWS S3 `pmc-oa-opendata`; check the commercial/
#   non-commercial licence split before mining
```

---

## 7. Probe status table

All probes 2026-09-02 unless noted. UA = default `curl` unless "Chrome 131" is stated
(Chrome 131 = the `AGENTS.md` rung-2 agent).

| Service | Endpoint probed | Status | Notes |
|---|---|---|---|
| Unpaywall API | `api.unpaywall.org/v2/<doi>` | **200** | 422 without email; 422 for shared placeholder address; **404** for bogus DOI (207 B) |
| Unpaywall site | `unpaywall.org/*` | 200 | **1,421 B SPA shell for every path** — size carries no information |
| Unpaywall S3 | `unpaywall-data-snapshots.s3...` | 200 | Anonymous listing OK; newest snapshot **2024-11-27** |
| OpenAlex | `api.openalex.org/works` | **200** | Credit+USD rate-limit headers; `meta.cost_usd` |
| OpenAlex S3 | `openalex.s3.amazonaws.com` | 200 | `data/jsonl/`, `data/parquet/`, `legacy-data/`. `data/works/` → KeyCount 0 |
| Semantic Scholar | `api.semanticscholar.org/graph/v1` | **200** | No key needed; 404 for bogus DOI |
| S2 datasets | `.../datasets/v1/release/latest` | 200 | Listing public; `/dataset/s2orc` → **401**, 40 B |
| CORE | `api.core.ac.uk/v3/...` | **301** (776 B) | Key required; misleading status |
| CORE site | `core.ac.uk` | 200, 91,189 B | "452M papers" on home page |
| **BASE** | `base-search.net` | 200 | **Anubis PoW wall v1.27.0+dirty** — size unmeasurable |
| OpenAIRE | `api.openaire.eu/search/publications` | **200** | 238,449,827. `v3.openaire.eu` → **timeout (000)** |
| DOAJ | `doaj.org/api/search/...` | **200** | 23,384 journals · 13,535,801 articles |
| dblp API | `dblp.org/search/publ/api` | **200** | No key, no UA fallback |
| dblp dump | `dblp.org/xml/dblp.xml.gz` | 200 | 1,099,942,370 B, last-modified 2026-09-01 |
| **USENIX** | `usenix.org/system/files/osdi24_full_proceedings.pdf` | **200** | 83,779,378 B, `%PDF-`. Chrome 131. Bogus → 404 (16,889 B themed) |
| USENIX policy | `usenix.org/about`, `/conferences/open-access` | 200 | "banished paywalls in 2008" |
| ACM | `acm.org/publications/openaccess` | 200 | |
| ACM OPEN | `libraries.acm.org/acmopen` | 200 | `/acmopen/faq` → 404 |
| **ACM OpenTOC** | `dl.acm.org/opentoc` | **403, 5,635 B** | Cloudflare fingerprint — blocked, not broken |
| PMC | `eutils.ncbi.nlm.nih.gov/.../esearch.fcgi?db=pmc` | 200 | 12,570,099 / 8,192,003 OA |
| PMC OA service | `.../pmc/utils/oa/oa.fcgi` | **404** | Legacy path dead on both hosts |
| Europe PMC | `ebi.ac.uk/europepmc/webservices/rest/search` | **200** | 48,813,426 total |
| HathiTrust | `hathitrust.org`, `/about/` | 200 | "19+ million digitized items" |
| JSTOR open | `about.jstor.org/oa-and-free/` | 200 | 80,000+ reports, 187 think tanks |
| **CiteSeerX** | every path incl. `robots.txt` and a bogus path | **301 → Wayback** | **Retired.** Fixed target `20251230112235`; following it → 429 |
| **OpenDOAR** | `v2.sherpa.ac.uk/opendoar/` | **403, 651,922 B** | Not the Cloudflare fingerprint. Count NOT-VERIFIED |
| ROAR | `roar.eprints.org` | 200, 8,593 B | Reachable; count not extracted |
| ResearchGate | `researchgate.net` | **403**, 1,714 B | Chrome 131 |
| Academia.edu | `academia.edu` | **403**, 5,599 B | Chrome 131 |

**User-agent findings for [`retrieval-notes.md`](retrieval-notes.md) / the
[crawler access table](../../ai-crawler-site-access-table.md):**

- **No UA fallback was needed** for any API in §2 — Unpaywall, OpenAlex, Semantic Scholar,
  OpenAIRE, DOAJ, dblp, E-utilities and Europe PMC all answered default `curl`.
- **Chrome 131 was used for all HTML pages** and sufficed for `usenix.org`, `core.ac.uk`,
  `acm.org`, `libraries.acm.org`, `hathitrust.org`, `about.jstor.org`, `roar.eprints.org`.
- **Chrome 131 did not help** against `dl.acm.org/opentoc` (Cloudflare), `base-search.net`
  (Anubis PoW), `v2.sherpa.ac.uk` (403 with a 651 kB body), `researchgate.net`, `academia.edu`.
- **New fingerprint to record: a ~651 kB HTTP 403 from `v2.sherpa.ac.uk`.** It is neither the
  ~5.6 kB Cloudflare challenge nor the Anubis PoW page. Worth adding to the table alongside them.
- **New trap to record: `unpaywall.org` serves a byte-identical 1,421-byte SPA shell for every
  path**, exactly like the `osf.io` 4,207-byte shell already in
  [README §4](README.md#6-probing-traps).

---

## 8. Sources

All retrieved **2026-09-02** unless stated. Raw probe output is under
[`../../scratch/preprint-repositories/oa-fulltext/`](../../scratch/preprint-repositories/oa-fulltext/).

- **S1** `https://unpaywall.org/`, `/products/api`, `/products/data-feed`, `/faq` — all HTTP 200,
  all exactly 1,421 bytes. Supports: SPA-shell trap; corpus size NOT-VERIFIED. [WEB]
- **S2** `https://api.unpaywall.org/v2/<doi>?email=…` for `10.1038/nature12373`,
  `10.1109/ISCA.2014.6853210`, `10.1109/SP.2019.00002`, `10.1145/2517349.2522738`,
  `10.1109/JPROC.2017.2761740`, `10.1145/3079856.3080246`; plus 422/404 controls. Supports: §2.1
  worked-example table, taxonomy, negative controls. [API]
- **S3** `https://api.openalex.org/works/doi:10.1145/3079856.3080246` — `oa_status: closed`,
  `any_repository_has_fulltext: false`. Supports: the three-way arXiv blind-spot comparison. [API]
- **S4** `https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3079856.3080246` —
  `externalIds.ArXiv: 1704.04760`, `isOpenAccess: true` vs `openAccessPdf.status: CLOSED`.
  Supports: rung 2, the self-contradiction note. [API]
- **S5** `https://unpaywall-data-snapshots.s3.us-west-2.amazonaws.com/?list-type=2` — snapshot
  keys, sizes and `LastModified`. Supports: the bulk table and the staleness flag. [API]
- **S6** `https://api.openalex.org/{works,authors,sources,institutions,publishers}?per-page=1` →
  `meta.count`. Supports: the entity-count table. [API]
- **S7** `https://api.openalex.org/works?group_by=open_access.oa_status`. Supports: the OA
  breakdown; buckets sum exactly to 321,988,823. [API]
- **S8** Response headers from `https://api.openalex.org/works?per-page=1` —
  `x-ratelimit-limit: 1000`, `x-ratelimit-limit-usd: 0.1`, `x-ratelimit-cost-usd: 0.0001`,
  `x-ratelimit-reset: 63043`. Supports: §2.2 rate limits. [API]
- **S9** `https://openalex.s3.amazonaws.com/?list-type=2&delimiter=/` and `&prefix=data/`.
  Supports: snapshot layout. [API]
- **S10** `https://api.semanticscholar.org/datasets/v1/release/latest` (release `2026-08-25`) and
  `/dataset/s2orc` → 401. Supports: S2ORC sizes and access route. [API]
- **S11** `https://core.ac.uk/` — "Search 452M papers from around the world". [WEB]
- **S12** `https://api.core.ac.uk/v3/search/works?q=test&limit=1` → HTTP 301, 776 B. [API]
- **S13** `https://core.ac.uk/documentation/dataset` — 2024-07-12 749 GB / ~2.7 TB; 2023-03-18 and
  2022 393 GB / 3.5 TB. [DOC]
- **S14** `https://www.base-search.net/` — Anubis `v1.27.0+dirty` challenge page, 7,846 B, hosted
  by Bielefeld University Library. [WEB]
- **S15** `https://api.openaire.eu/search/publications?size=0` → `<total>238449827</total>`;
  `https://v3.openaire.eu/api/publications/count` → timeout. [API]
- **S16** `https://doaj.org/api/search/{journals,articles}/*?pageSize=1` → 23,384 / 13,535,801. [API]
- **S17** `https://dblp.org/search/publ/api?q=RISC-V&format=json&h=1` → `@total: 2313`. [API]
- **S18** `HEAD https://dblp.org/xml/dblp.xml.gz` → 1,099,942,370 B, last-modified
  2026-09-01 23:47:15 GMT. [API]
- **S19** `https://www.usenix.org/about` — "We banished paywalls in 2008…". [DOC]
- **S20** `https://www.usenix.org/conferences/open-access` — the fuller statement quoted in §3.1. [DOC]
- **S21** `https://www.usenix.org/conference/osdi24/technical-sessions` (200, 259,550 B);
  `osdi24_full_proceedings.pdf` (200, 83,779,378 B, `%PDF-`); `osdi24_proceedings_interior.pdf`
  (200, 82,578,353 B); bogus filename → 404, 16,889 B. [WEB]
- **S22** `https://libraries.acm.org/acmopen` — ACM OPEN description quoted in §3.2. [DOC]
- **S23** `https://dl.acm.org/opentoc` → HTTP 403, 5,635 B (Cloudflare fingerprint). [WEB]
- **S24** `https://www.acm.org/publications/openaccess` (200, 76,905 B);
  `https://libraries.acm.org/acmopen/faq` (404). [WEB]
- **S25** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=all%5Bsb%5D` →
  12,570,099; `term="open access"[filter]` → 8,192,003. [API]
- **S26** `https://www.ebi.ac.uk/europepmc/webservices/rest/search` for `*:*`, `SRC:MED`,
  `HAS_FT:Y`, `OPEN_ACCESS:Y`. [API]
- **S27** `https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC5334499` → 404 (1,584 B);
  `https://pmc.ncbi.nlm.nih.gov/utils/oa/oa.fcgi?id=PMC5334499` → 404 (48,716 B). [WEB]
- **S28** `https://www.hathitrust.org/about/` — "founded in 2008… now preserving 19+ million
  digitized items". [WEB]
- **S29** `https://about.jstor.org/oa-and-free/` — "more than 80,000 open access research reports
  from 187 think tanks"; "up to 100 free articles every 30 days". [WEB]
- **S30** `citeseerx.ist.psu.edu` — five paths incl. `robots.txt` and a deliberately bogus path,
  all HTTP 301 → `web.archive.org/web/20251230112235/…`; following → 429. [WEB]
- **S31** `https://v2.sherpa.ac.uk/opendoar/` and `/view/repository_by_country/` → HTTP 403,
  651,922 B, Chrome 131. [WEB]
- **S32** `https://roar.eprints.org/` → HTTP 200, 8,593 B. [WEB]
- **S33** `https://www.researchgate.net/` → 403, 1,714 B; `https://www.academia.edu/` → 403,
  5,599 B; both Chrome 131. [WEB]
- **S34** [`arxiv.md` §7.5](arxiv.md) — arXiv IDs `1703.09039` and `1704.04760`, previously
  verified in this directory; used as the ground truth against which Unpaywall's `closed` verdicts
  are judged wrong in practice. [internal]
