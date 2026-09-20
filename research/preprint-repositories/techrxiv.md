# TechRxiv — preprint repository record

- **URL:** https://www.techrxiv.org/
- **Operator:** IEEE (Institute of Electrical and Electronics Engineers). IEEE is Crossref
  member `263` and owns the DOI prefix `10.36227` used by every TechRxiv deposit (S1).
  Funded by IEEE; free to deposit and to read.
- **Discipline scope:** *as advertised* — "engineering, computer science, and related
  technology" (S3). *As actually used* — heavily weighted toward computing/AI; the
  circuits-and-devices core of IEEE is a minority of the corpus (§2, §3).
- **Launched:** first content posted **2019-10-18** (S1); the server is generally described
  as a 2020 launch and 2020 is the first full year of operation. **Status:** active.
- **Platform history:** Figshare (2019/2020 → Dec 2023) → **Authorea** (Wiley) (Dec 2023 →
  present) (§1, S2/S4/S1).
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

> **Access warning up front.** As of 2026-09-01 `www.techrxiv.org` is behind a Cloudflare
> interactive challenge and returns **HTTP 403 `cf-mitigated: challenge`** to every scripted
> request tried (default UA, Chrome UA, WhatsApp UA, ChatGPT-User UA, HTTP/1.1) except
> `/robots.txt` (S5). Every count in this record therefore comes from **Crossref** (the DOI
> registry, [API]) or from **Wayback captures** ([WEB]), never from a live site scrape.
> This is stated so the reader knows which numbers are first-hand.

## 1. What it is

TechRxiv is IEEE's own preprint server. Its purpose is narrow and, for an engineer, very
useful: it lets an author post a manuscript at (or near) the moment they submit it to an
IEEE journal or conference, so the work is citable, timestamped and — crucially —
**openly readable** while the IEEE version is still behind the Xplore paywall. IEEE
permits this; TechRxiv is the sanctioned channel for it.

The server has moved platforms once, and the move matters for anyone writing scrapers or
citing URLs. TechRxiv originally ran on **Figshare** infrastructure: Wayback captures of
the 2022 home page carry a `figshare` footer (S2), and the Figshare ResourceSync manifest
`https://www.techrxiv.org/figshareresourcesync/techrxiv/cresourcelist-0.xml` is archived
from 2020-08-09 through 2023-12-02 (S4). It now runs on **Authorea** (a Wiley property,
served through an Atypon-style front end): the live server emits an HTTP 103 early-hints
`Link:` header preloading `/products/authorea/techrxiv/releasedAssets/...` (S5), the
January 2026 Wayback capture is branded `AUTHOREA` and footers read "Powered by
Authorea.com" (S3), and `/robots.txt` exposes Atypon path conventions (`/action/showJournal`,
`/na101/`, `/doi/metrics/`) (S5).

**The migration date is December 2023.** Two independent [API]/[WEB] signals agree. First,
the DOI syntax changed: Figshare-era DOIs look like `10.36227/techrxiv.23589741.v1`
(Figshare item id, `.vN` suffix), Authorea-era DOIs look like
`10.36227/techrxiv.170244204.41850386/v1` (two numeric segments, `/vN` path suffix). The
earliest Authorea-style DOI was posted **2023-12-13**; the monthly crossover runs
Nov 2023 (0 new-style / 605 old-style) → Dec 2023 (120 / 371) → Jan 2024 (289 / 30) (S1).
Second, the Figshare ResourceSync manifest stops being archived on 2023-12-02 (S4).
Legacy items kept their Figshare-style DOI stems and still receive new versions under the
old syntax — the newest old-style DOI in the registry was posted 2026-02-17 (S1).

## 2. Scope and subject taxonomy

TechRxiv classifies with the **IEEE top-level thesaurus terms**, not arXiv-style codes.
The browse facet counts below are from the Wayback capture of the home page on
**2026-01-04** (S3). An item may carry more than one term, so the column sums to 35,251
against 17,549 public documents — a mean of ≈2.0 terms per item [INF].

| IEEE subject term | Items (2026-01-04) [WEB] |
|---|---|
| computing and processing | 9,416 |
| communication, networking and broadcast technologies | 4,741 |
| signal processing and analysis | 3,972 |
| power, energy and industry applications | 2,541 |
| components, circuits, devices and systems | 2,335 |
| robotics and control systems | 2,186 |
| general topics for engineers | 1,951 |
| engineering profession | 1,878 |
| bioengineering | 1,824 |
| fields, waves and electromagnetics | 1,577 |
| transportation | 939 |
| aerospace | 731 |
| engineered materials, dielectrics and plasmas | 715 |
| photonics and electrooptics | 610 |
| geoscience | 549 |
| nuclear engineering | 186 |

**How much of TechRxiv is electronics/power/RF/embedded?** Summing the terms an
electronics engineer would care about — components/circuits/devices/systems (2,335),
power/energy/industry (2,541), fields/waves/EM (1,577), photonics (610), engineered
materials/dielectrics/plasmas (715) — gives 7,778 term-assignments, **22% of all
assignments**; add communications (4,741) and signal processing (3,972) and you reach 47%.
By contrast *computing and processing* alone is 27% of assignments [INF from S3]. The
honest summary: TechRxiv is IEEE-shaped on paper and CS/AI-shaped in practice, with a
real but secondary hardware core of a few thousand documents.

## 3. Size and growth

Three different numbers, all correct, all measuring different things. Report them
separately.

| Measure | Value | Date | Source |
|---|---|---|---|
| Crossref DOI records under prefix `10.36227`, all type `posted-content` | **30,954** | 2026-09-01 | [API] S1 |
| Distinct items (DOI records after stripping `.vN` / `/vN` version suffixes) | **18,890** | 2026-09-01 | [API] S1 |
| Site's own "Public Documents" counter | **17,549** | 2026-01-04 | [WEB] S3 |
| Site's cumulative views / downloads counter | 13,580,596 / 5,791,115 | 2026-01-04 | [WEB] S3 |

The site counter (17,549 on 2026-01-04) and the Crossref distinct-item count (18,890 on
2026-09-01) are consistent given eight months of growth [INF]. The 30,954 raw DOI count is
the one to avoid quoting as "TechRxiv has 31,000 preprints" — it double-counts versions.

**Distinct items by year of first posting** [API] S1:

| 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (to 09-01) |
|---|---|---|---|---|---|---|---|
| 73 | 1,009 | 1,836 | 2,429 | 3,103 | 3,528 | 5,611 | 1,301 |

2019 is three months of soft launch (9 items in October, 27 in November, 37 in December).
The 2025 jump to 5,611 is real in the registry; whether it reflects genuine growth or the
same generative-AI submission wave that other servers report is **[NOT-VERIFIED]** here —
IEEE has published no submission/rejection statistics I could retrieve.

**Versioning.** 2,678 of 18,890 distinct items (14.2%) carry more than one numbered
version [API] S1.

## 4. Screening and moderation — what gets in

TechRxiv describes itself as an "**open, moderated** preprint server for unpublished
research" (S3, home-page About blurb, 2026-01-04). That is the only first-hand statement of
policy I could retrieve.

**I could not obtain IEEE's published screening criteria.** The live `/about`,
`/faqs`, `/submission-guidelines` and `/terms-of-use` pages are Cloudflare-blocked (S5), and
the Wayback captures of `https://www.techrxiv.org/about` from 2024-01 through 2025-06 are
**JavaScript shells** — the Authorea SPA never rendered for the crawler, so the archived
HTML contains navigation chrome and nothing else (S6). This is marked
**[NOT-VERIFIED]**: I cannot tell you who moderates, against what checklist, in what
turnaround, or what the rejection rate is. What I can say from evidence:

- The moderation is **pre-publication** in the sense that the browse UI distinguishes
  ordinary preprints from a "**Version of Record**" filter class (S3), so IEEE tracks
  published status as a first-class attribute.
- IEEE runs periodic house-organ notices soliciting deposits ("TechRxiv: Share Your
  Preprint Research With the World!") in *IEEE Potentials* and *IEEE Network* across
  2022–2025 (S7) — [LIT], but these are one-page promotional notices, not policy.
- Content is clearly **not peer reviewed**; the most-cited items (§7) are unrefereed
  survey articles.

If you need the authoritative policy, the route is a browser session on techrxiv.org or an
IEEE Author Center page — neither of which is scriptable from here.

## 5. Reliability — what you can and cannot trust

**What a TechRxiv deposit guarantees:** a Crossref DOI, a posting timestamp, a version
chain, and an explicit licence (§9). Nothing about correctness.

**What it does not guarantee:** peer review, novelty, or that the author has the right to
post. There is no endorsement system and no affiliation requirement that I could verify.

**Eventual-publication rate — a real measured number.** Of the 18,890 distinct items,
**5,457 (28.9%) carry a Crossref `is-preprint-of` relation** pointing at a published
article [API] S1. Where those links point:

| Target DOI prefix | Publisher | Link records |
|---|---|---|
| `10.1109` | IEEE | 6,297 |
| `10.1016` | Elsevier | 832 |
| `10.1007` | Springer | 335 |
| `10.2139` | SSRN | 282 |
| `10.3390` | MDPI | 235 |
| `10.1088` | IOP | 67 |
| `10.1038` | Nature Portfolio | 64 |
| `10.1080` | Taylor & Francis | 61 |
| `10.1049` | IET | 55 |
| `10.1002` | Wiley | 54 |

Treat 28.9% as a **floor**, not the true publication rate: the relation is populated when
the link is made, and items posted in the last 18 months have not had time to be published
or linked [INF]. Note the 282 links to SSRN — those are not journal publications and are a
reminder to check what a link actually points at.

**Known failure modes.** (a) The citation-weighted top of the corpus is dominated by
unrefereed LLM/AI survey articles with many co-authors (§7) — a pattern associated
elsewhere with citation-farming; treat high TechRxiv citation counts as weak evidence of
quality. (b) Version proliferation: one legacy item has reached `.v13` (S1), so "the
TechRxiv version" is ambiguous unless you pin the version. (c) Because the platform
migrated, older links and older DOI syntax coexist; both still resolve (§8) but tooling
that assumes one syntax will break.

**How to sanity-check an individual TechRxiv paper.**
1. `curl -s https://api.crossref.org/works/<techrxiv-doi>` and read `relation.is-preprint-of`.
   If present, the paper reached a journal — go read that instead.
2. Read `posted.date-parts` and compare against the published version's date. A preprint
   posted *after* the journal article is a mirror, not a priority claim.
3. Read `license` — CC BY-NC-SA content cannot be redistributed the way CC BY content can.
4. Check the version suffix. `/v1` and `/v4` can differ substantially.

## 6. What you actually find there — examples

Real deposits, each verified to exist via Crossref and to resolve through `doi.org` on
2026-09-01 (S1, S8):

- **Power devices.** *4 A / 300 V switching of lateral β-Ga₂O₃ MOSFET devices*, Tetzner et
  al., posted 2025-06-19 — `10.36227/techrxiv.175037428.81899126/v1`. Linked as preprint of
  *IEEE Electron Device Letters* `10.1109/LED.2025.3590836`. Genuine wide-bandgap power
  electronics, on the server months ahead of the paywalled letter.
- **Magnetics for converters.** *Non-Linear Inductors Characterization in Real Operating
  Conditions for Power Density Optimization*, Scirè et al., 2021-06-04 —
  `10.36227/techrxiv.14485221`.
- **FPGA / on-board processing.** *CloudSatNet-1: FPGA-based Hardware-Accelerated Quantized
  CNN for Satellite On-Board Cloud Cover Classification*, Pitoňák et al., 2022-03-17 —
  `10.36227/techrxiv.19367825.v1`, preprint of `10.3390/rs14133180`.
- **RISC-V microarchitecture.** *Configurable Hardware Acceleration for Hyperdimensional
  Computing Extension on RISC-V*, Martino et al., 2024-12-05 —
  `10.36227/techrxiv.173337827.72919533/v1`, preprint of *IEEE Trans. Computers*
  `10.1109/TC.2025.3642250`.
- **Cryogenic / quantum control electronics.** *Cryogenic Embedded System to Support
  Quantum Computing: From 5nm FinFET to Full Processor*, Genßler et al., 2023-06-27 —
  `10.36227/techrxiv.23548242.v1`, preprint of `10.1109/TQE.2023.3300833`.
- **6G channel modelling.** *Overview of 3GPP Release 19 Study on Channel Modeling
  Enhancements to TR 38.901 for 6G*, Poddar et al., 2025-08-03 —
  `10.36227/techrxiv.175423889.90938399/v1`. Directly useful standards-tracking material.
- **Analog design automation.** *LADAC: Large Language Model-driven Auto-Designer for
  Analog Circuits*, Liu et al., 2024-01-08 — `10.36227/techrxiv.170473941.10097233/v1`.
- **Hardware security.** *Algorithmic Security is Insufficient: A Comprehensive Survey on
  Implementation Attacks Haunting Post-Quantum Security*, Canto et al., 2023-05-23 —
  `10.36227/techrxiv.23071079.v1`.
- **Neuromorphic sensing.** *Hardware, Algorithms, and Applications of the Neuromorphic
  Vision Sensor: a Review*, Cimarelli et al., 2025-04-18 —
  `10.36227/techrxiv.174494936.63871491/v1`, preprint of `10.3390/s25196208`.
- **IIoT security dataset.** *Edge-IIoTset: A New Comprehensive Realistic Cyber Security
  Dataset of IoT and IIoT Applications*, Ferrag et al., 2022-01-27 —
  `10.36227/techrxiv.18857336.v1`, preprint of `10.1109/ACCESS.2022.3165809`. A dataset
  paper that is actually used.

## 7. Landmark papers — an honest assessment

**TechRxiv has essentially no field-defining papers, and that is by design.** It is not a
priority-claiming venue like arXiv `hep-th` or the IACR ePrint archive; it is an
early-dissemination and green-OA channel attached to IEEE's submission pipeline. Nobody
"scoops" a competitor on TechRxiv.

The empirical proof is the citation distribution. Sorting all 30,954 records by Crossref
`is-referenced-by-count` (S1), the top of the corpus is unrefereed AI survey literature,
not electronics:

| Paper | Identifier | Posted | Crossref citations (2026-09-01) | Preprint first? |
|---|---|---|---|---|
| A Survey on Large Language Models: Applications, Challenges, Limitations, and Practical Usage | `10.36227/techrxiv.23589741.v1` | 2023-07-10 | 247 | Yes — no `is-preprint-of` recorded; never linked to a journal version |
| Engineering Education in the Era of ChatGPT: Promise and Pitfalls of Generative AI for Education | `10.36227/techrxiv.21789434.v1` | 2022-12-30 | 127 | Yes |
| Artificial Intelligence in the Battle against Coronavirus (COVID-19): A Survey | `10.36227/techrxiv.12743933` | 2020-08-01 | 87 | Yes |
| Prompt Engineering For ChatGPT: A Quick Guide | `10.36227/techrxiv.22683919` | 2023-05-04 | 87 | Yes |
| A Survey on Mixture of Experts | `10.36227/techrxiv.172055626.64129172/v1` | 2024-07-09 | 71 | Yes |
| CERT: Contrastive Self-supervised Learning for Language Understanding | `10.36227/techrxiv.12308378.v1` | 2020-05-21 | 70 | Yes |

The highest-cited *electronics/communications* items are far lower: the 6G rural-connectivity
survey `10.36227/techrxiv.10253336.v1` (2019-11-06, 13 citations) and
`10.36227/techrxiv.11634669` (2020-01-17, 13 citations) are among the most-cited comms
deposits, and the Edge-IIoTset dataset paper reaches 18 (S1). For genuinely landmark
electronics preprints, look at arXiv `eess.*`/`cs.AR` or the IACR ePrint archive, not here.

**What TechRxiv *is* good for is covered in §8 — finding the open version of a paywalled
IEEE paper.**

## 8. Access, APIs and bulk retrieval

**The live site is not scriptable.** Every path except `/robots.txt` returned HTTP 403 with
`cf-mitigated: challenge` and a Cloudflare "Just a moment…" body on 2026-09-01, under four
different user agents (S5). `robots.txt` additionally sets `User-agent: GPTBot / Disallow: /`
and `Crawl-delay: 1`, and points at a sitemap (`/sitemap-index-1.xml`) that is itself 403 (S5).

**Negative control.** `https://www.techrxiv.org/robots-not-real.txt` → **403, 5,464 bytes**
(the same challenge page), while `https://www.techrxiv.org/robots.txt` → **200, 808 bytes**
of real text (S5). So on this host a 403 tells you nothing about whether a document exists,
and only byte-size/content inspection distinguishes a real response.

**Use Crossref instead.** It is complete, fast and unblocked:

```bash
# every TechRxiv DOI, paged
curl 'https://api.crossref.org/prefixes/10.36227/works?rows=1000&select=DOI,title,posted,relation&cursor=*'
# one item
curl 'https://api.crossref.org/works/10.36227/techrxiv.19367825.v1'
```

**DOI resolution works fine** (doi.org is not behind the challenge). Both syntaxes resolve:

| Probe | Result (2026-09-01) |
|---|---|
| `https://doi.org/10.36227/techrxiv.23589741.v1` (Figshare-era) | 302 → `https://www.techrxiv.org/doi/full/10.36227/techrxiv.23589741.v1` |
| `https://doi.org/10.36227/techrxiv.170244204.41850386/v1` (Authorea-era) | 302 → `.../doi/full/10.36227/techrxiv.170244204.41850386/v1` |
| **Negative control** `https://doi.org/10.36227/techrxiv.99999999999.99999999/v1` | **404** |

So Figshare-era DOIs survived the migration intact — a good durability result (S8).

**No OAI-PMH.** `/oai?verb=Identify` and `/api/oai?verb=Identify` both return the Cloudflare
403 (S5); no working OAI endpoint was found. **[NOT-VERIFIED]** whether one exists behind
the challenge.

**OpenAlex does not index TechRxiv as a source.** `https://api.openalex.org/sources?search=TechRxiv`
and `?filter=display_name.search:techrxiv` both return `meta.count = 0` on 2026-09-01 (S9).
This conflicts with the fact that OpenAlex indexes engrXiv and ECSarXiv as sources; do not
plan a TechRxiv pipeline around OpenAlex source filters.

### The one thing TechRxiv is genuinely best at: finding the open version of a paywalled IEEE paper

This is the property that justifies an engineer knowing the server exists. **6,297 Crossref
link records point from TechRxiv preprints to `10.1109` DOIs** (S1) — and the link is
recorded **in both directions**. Spot-checking five IEEE journal articles that are targets
of a TechRxiv `is-preprint-of` relation, all five carried the reverse `has-preprint`
relation on their own Crossref record (S1: `10.1109/TSG.2020.3010866`,
`10.1109/TBCAS.2020.2982824`, `10.1109/TSTE.2020.3004630`, …).

Practical recipe — you have an Xplore DOI and no subscription:

```bash
curl -s 'https://api.crossref.org/works/10.1109/TBCAS.2020.2982824' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["message"].get("relation",{}).get("has-preprint"))'
# -> [{'id': '10.36227/techrxiv.10049843', 'id-type': 'doi', ...}]
```

Then resolve that DOI. This works without touching techrxiv.org's HTML, and it is more
reliable than title-searching, because the publisher asserted the link.

**Is the TechRxiv copy the accepted (post-review) version? [NOT-VERIFIED].** I could not
confirm this. What the evidence shows: TechRxiv's browse UI has a "Version of Record"
filter, so *some* items are flagged as VoR (S3); and **22.3% of the 5,457 journal-linked
items carry more than one numbered version**, versus 14.2% of the corpus overall (S1) —
consistent with a meaningful minority of authors uploading an updated (probably accepted)
manuscript after acceptance, but consistent with several other stories too. Practically:
**assume `/v1` is the submitted manuscript, check for a later version, and diff against the
published abstract before relying on numbers.**

## 9. Licensing and reuse

Authors choose, and the default is permissive. Licence URLs recorded in Crossref for a
3,000-record sample of prefix `10.36227` (2026-09-01, S1):

| Licence | Records in sample |
|---|---|
| CC BY 4.0 | 2,389 |
| CC BY-NC-SA 4.0 | 465 |
| CC BY-SA 4.0 | 120 |
| CC0 1.0 | 26 |

≈80% CC BY [INF]. Every record in the sample carried *some* licence — unusual and welcome.
For text/data mining this means the metadata is reusable via Crossref without restriction,
but **bulk full-text mining of the site itself is blocked** by Cloudflare and by the
explicit `GPTBot: Disallow` in robots.txt (S5), regardless of the per-item CC licence.

## 10. Caveats and controversies

- **Platform churn is the biggest risk to citations.** TechRxiv has already moved once
  (Figshare → Authorea, Dec 2023). Old DOIs still resolve today (§8), but cite the **DOI**,
  never a `techrxiv.org/articles/...` or `techrxiv.org/doi/full/...` URL.
- **Scriptable access has regressed.** Wayback shows the site was crawlable through at
  least 2026-01-04; 2026-07 captures are already 403 (S4). A knowledge base that depends on
  scraping TechRxiv will rot.
- **Two DOI syntaxes** (`....v1` vs `.../v1`) coexist forever. Regexes must handle both.
- **The citation leaderboard is not a quality signal.** See §7.
- **IEEE's own policy documents were not retrievable** (§4). Anything you read elsewhere
  about "IEEE screens TechRxiv submissions for scope and plagiarism" is not confirmed by
  this record.
- **OpenAlex blind spot** (§8) — a real gap if you build discovery tooling.
- Wikipedia's REST summary endpoint returned an internal error for `TechRxiv` on
  2026-09-01 (S9), so no Wikipedia cross-check of size or launch date is recorded here.

## 11. Sources

- **S1** — Crossref REST API, prefix `10.36227`: `https://api.crossref.org/prefixes/10.36227/works`
  (full cursor dump of 30,954 records with `DOI,posted,relation,license`; plus
  `?rows=0&facet=type-name:*,published:30`, `?sort=is-referenced-by-count`, and individual
  `https://api.crossref.org/works/<doi>` lookups). Retrieved 2026-09-01. **[API]** —
  supports every deposit count, the year distribution, the version analysis, the
  `is-preprint-of` statistics and target-prefix table, the licence table, the citation
  ranking, all landmark/example metadata, and the December-2023 migration crossover.
  Also `https://api.crossref.org/members?query=institute+of+electrical` (IEEE = member 263,
  owns prefixes 10.1109, 10.36227, …), retrieved 2026-09-01.
- **S2** — Wayback capture of the Figshare-era home page,
  `http://web.archive.org/web/20220901140901/https://www.techrxiv.org/`, retrieved
  2026-09-01. **[WEB]** — supports "figshare" footer branding pre-migration.
- **S3** — Wayback capture of the Authorea-era home page,
  `http://web.archive.org/web/20260104143925/https://www.techrxiv.org/`, retrieved
  2026-09-01. **[WEB]** — supports the About blurb ("open, moderated preprint server…"),
  `AUTHOREA` branding, the "Public Documents 17549" counter, the 13,580,596 views /
  5,791,115 downloads counters, the full IEEE subject-term table, and the existence of the
  "Version of Record" browse filter.
- **S4** — Internet Archive CDX API,
  `http://web.archive.org/cdx/search/cdx?url=www.techrxiv.org*`, several queries including
  `.../figshareresourcesync*` and date-bounded home-page listings. Retrieved 2026-09-01.
  **[WEB]** — supports the ResourceSync manifest span (2020-08-09 → 2023-12-02) and the
  2026-07 onset of 403 responses to the crawler.
- **S5** — Live probes of `https://www.techrxiv.org/` on 2026-09-01: `/` (403,
  `cf-mitigated: challenge`, under 4 user agents and HTTP/1.1), `/robots.txt` (200, 808 B,
  content quoted), `/sitemap.xml`, `/sitemaps.xml`, `/sitemap_index.xml`, `/action/sitemap.xml`,
  `/api/docs`, `/oai?verb=Identify`, `/api/oai?verb=Identify` (all 403), and the negative
  control `/robots-not-real.txt` (403, 5,464 B). **[WEB]**
- **S6** — Wayback captures of `https://www.techrxiv.org/about` (20240101085028,
  20250609162951) and `/faqs` (20240109100643), retrieved 2026-09-01. **[WEB]** — these are
  the captures that turned out to be empty JS shells; they are the basis for the
  **[NOT-VERIFIED]** verdict on IEEE's screening policy.
- **S7** — Crossref search for literature about the server,
  `https://api.crossref.org/works?query.bibliographic=TechRxiv+preprint+IEEE`, retrieved
  2026-09-01. **[LIT]** — IEEE house notices, e.g. `10.1109/mpot.2022.3196554`,
  `10.1109/mpot.2023.3263350`, `10.1109/mnet.2025.3540148`. Contents not read (paywalled).
- **S8** — `doi.org` HEAD probes for `10.36227/techrxiv.23589741.v1`,
  `10.36227/techrxiv.170244204.41850386/v1`, the ten example DOIs in §6, and the negative
  control `10.36227/techrxiv.99999999999.99999999/v1` (404). Retrieved 2026-09-01. **[WEB]**
- **S9** — `https://api.openalex.org/sources?search=TechRxiv` and
  `?filter=display_name.search:techrxiv` (both `meta.count = 0`); Wikipedia REST
  `https://en.wikipedia.org/api/rest_v1/page/summary/TechRxiv` (internal error). Retrieved
  2026-09-01. **[API]**
