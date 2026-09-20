# figshare — preprint repository record

- **URL:** https://figshare.com/
- **Operator:** figshare, a portfolio company of **Digital Science**, which is a subsidiary
  of **Holtzbrinck / Springer Nature** (S6) [WEB]. Founded by Mark Hahnel.
- **Discipline scope:** generalist / multidisciplinary. All output types, no subject gate.
- **Launched:** **January 2011**; relaunched with Digital Science backing January 2012
  (S6) [WEB] · **Status:** active
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What it is

figshare is a **generalist repository** in the same category as Zenodo: upload anything,
get a DOI, no review. It began as a personal tool Mark Hahnel built to publish the figures,
videos and negative results generated during his stem-cell PhD that no journal would take
(S6) [WEB]. That origin still shows in the product — figshare's native unit is the
*figure*, *dataset* or *media object*, not the paper.

The more consequential fact, and the reason this record exists, is that **figshare is
infrastructure**. Far more figshare exists than figshare.com. The same platform is sold as:

- **figshare for Institutions** — white-labelled institutional repositories, frequently on
  the university's *own domain* so the figshare branding is invisible.
- **figshare for Publishers** — supplementary-data hosting behind journals.
- **the substrate under whole preprint servers** — IEEE's TechRxiv, ACS's ChemRxiv and
  SAGE's Advance were all built on it (§4).

That last role makes figshare a systemic dependency of the preprint ecosystem, and makes
its churn a durability question rather than a commercial one (§5.2).

## 2. Scope and item taxonomy

figshare's OAI-PMH `ListSets` exposes **30 sets**, of which 25 are "Article type" sets —
this is the authoritative item vocabulary (S3) [API], retrieved 2026-09-01:

`figure` · `media` · `dataset` · `poster` · `journal contribution` · `presentation` ·
`thesis` · `software` · `online resource` · **`preprint`** · `book` ·
`conference contribution` · `chapter` · `peer review` · `educational resource` · `report` ·
`standard` · `composition` · `funding` · `physical object` · `data management plan` ·
`workflow` · `monograph` · `performance` · `event`

Note that `preprint` is **one of twenty-five types**, and `software`, `workflow` and
`data management plan` are first-class alongside it. Like Zenodo, figshare is not a
preprint server that also does other things; it is a general repository in which preprints
are a minority type.

Distribution of the 100 most recently published items (S1) [API], as a rough indicator
only — this is a single snapshot of the newest items, not the corpus:

| Type | Count (of 100) |
|---|---|
| journal contribution | 49 |
| dataset | 28 |
| report | 5 |
| conference contribution | 4 |
| thesis | 4 |
| figure | 4 |
| preprint | 2 |
| chapter | 2 |
| software | 1 |
| poster | 1 |

## 3. Size and growth

**figshare does not publish a machine-readable total, and its own APIs will not give you
one.** Two independent attempts failed (§6):

- The REST search API uses **opaque cursor pagination** (`x-cursor` header) with no total
  in the response (S1) [API].
- OAI-PMH `ListIdentifiers` returns a `resumptionToken` **without a `completeListSize`
  attribute** (S3) [API], so the standard OAI counting trick is unavailable.

So I obtained counts from **DataCite**, where figshare registers its DOIs. Retrieved
2026-09-01 (S2) [API]:

| DataCite client | DOIs | What it is |
|---|---|---|
| `figshare.ars` | **4,106,613** | figshare Academic Research System — the main figshare.com |
| `si.figshare` | 5,481 | Figshare for Institutions |
| `figshare.asha` | 4,315 | ASHA Publications instance |
| `figshare.orcid` | 2,015 | ORCID integration |
| `figshare.plus` | 762 | Figshare+ |
| `figshare.sage` | **0** | SAGE instance — see §5.2 |
| `figshare.test` | 17 | test datacentre |

A prefix query for `10.6084` (figshare's main prefix) independently returned
**4,106,628** at a slightly later moment (S2) [API] — the ~15-record difference across a
few minutes is live growth, not disagreement.

**The federation is larger than figshare.com.** A DataCite client search for "figshare"
returns **33 clients** (S2) [API]. Summing the 25 retrieved gives **4,244,934** DOIs.
Institutional instances carry their own prefixes and client IDs, and several do not have
"figshare" in the repository name at all:

| Client | DOIs | Institution |
|---|---|---|
| `swin.repo2` | 37,062 | Swinburne University of Technology |
| `au.ir` | 33,882 | American University Research Archive |
| `bl.lboro` | 25,789 | Loughborough University Research Repository |
| `dk.dtic` | 6,369 | DTU Data |
| `bl.shef` | 5,378 | ORDA — University of Sheffield |
| `ardcx.deakin` | 4,776 | Deakin University |
| `mmu.fig` | 4,179 | Manchester Metropolitan University |
| `snd.su` | 2,029 | Stockholm University Figshare Repository |

> **Total corpus size: [NOT-VERIFIED].** ~4.1M for figshare.com proper is well evidenced;
> the true federation total is unknown because (a) the client list is not exhaustively
> enumerable by name-matching, and (b) publisher instances mint DOIs under *the publisher's*
> prefix, not figshare's, and are therefore invisible to any figshare-centric count. Do not
> quote a single "figshare size" figure.

**Evidence for (b):** among 100 newest items the DOI prefixes included `10.1021` (ACS, 11
items), `10.3389` (Frontiers, 4), `10.1016` (Elsevier, 2), `10.1038` (Springer Nature, 1)
and `10.1177` (SAGE, 1) alongside `10.6084` (33) and institutional prefixes `10.26187`
(17), `10.25439` (4), `10.26181` (3), `10.25447` (1), `10.25909` (1) (S1) [API]. Public
URLs in the same sample included `https://dro.deakin.edu.au/...` and
`https://frontiersin.figshare.com/...` — a figshare-powered repository on a university's
own domain, and a publisher-branded subdomain, both served by the same API.

**Wikipedia conflict:** the *List of preprint repositories* records figshare's size as
*"unknown"* (S7) [WEB]. That is at least honest, and consistent with my finding — but the
figshare.com figure of ~4.1M *is* obtainable via DataCite and can now be cited.

## 4. Screening and moderation — what gets in

**No peer review and no subject screening.** figshare is a self-deposit generalist
repository; items are published by the depositor and receive a DOI immediately.

**[NOT-VERIFIED]** I did not retrieve figshare's own published moderation/curation policy
document. figshare.com was reachable via its API throughout, but I did not locate and load
a policy page equivalent to Zenodo's General Policies. **Do not assume figshare's terms
match Zenodo's** — treat the specifics of its takedown, curation and retention rules as
unverified in this record.

One structural point *is* verifiable: on **institutional** instances the customer
institution, not figshare, controls curation policy. So "deposited on figshare" does not
denote a single screening regime — it denotes a software platform that may sit behind
anything from an uncurated public upload to a librarian-mediated institutional deposit.
[INF]

## 5. Reliability — what you can and cannot trust

### 5.1 What a figshare DOI means

A DOI, a timestamp, and hosting. **Not review, not validation, not curation** (§4). The
same warning that applies to Zenodo applies here: the identifier is plumbing.

An additional figshare-specific caution: because the platform is white-labelled, **you
often cannot tell from the URL that you are looking at figshare**. `dro.deakin.edu.au` is
figshare. Assessing "who stands behind this record" requires identifying the operator of
the *instance*, not the platform.

### 5.2 The infrastructure-churn finding — the durability point

figshare has powered several major publisher preprint servers. Their subsequent movement
is the most useful durability evidence in this record. All figures retrieved from Crossref
2026-09-01 (S4) [API]:

| Server | Prefix | Crossref owner | Works | Status found |
|---|---|---|---|---|
| **TechRxiv** | 10.36227 | Institute of Electrical and Electronics Engineers (IEEE) | 30,954 | **migrated off figshare** |
| **ChemRxiv** | 10.26434 | American Chemical Society (ACS) | 55,400 | migrated off figshare |
| **SAGE Advance** | 10.31124 | SAGE Publications | 4,417 | still on figshare URLs; no 2026 deposits |

**How the TechRxiv migration is visible in the data.** Resolving two TechRxiv DOIs
2026-09-01 (S5) [API]:

- Old: `10.36227/techrxiv.14420315` →
  `www.techrxiv.org/articles/preprint/Smart_Assistant_for_Accident_Prevention_and_Rescue/14420315`
  — the **figshare URL grammar** (`/articles/<type>/<title-slug>/<numeric-id>`), with a
  bare 8-digit figshare item ID.
- New: `10.36227/techrxiv.176281113.30584908/v1` →
  `www.techrxiv.org/doi/full/10.36227/techrxiv.176281113.30584908/v1`
  — a **completely different grammar** (`/doi/full/…/v1`) with a paired-numeric DOI suffix.

That second pattern is byte-for-byte the pattern used by Authorea
(`www.authorea.com/doi/full/10.22541/au.175225950.03002018/v1`, S4) [API]. TechRxiv also
returns the *same* Cloudflare-style 403 body size as authorea.com and essopenarchive.org
(5,620 / 5,620 / 5,622 bytes, S5) [WEB]. The combined evidence is that **TechRxiv moved
from figshare onto the Atypon/Wiley "Authorea" stack**. [INF]

ChemRxiv shows the same `/doi/full/` grammar
(`chemrxiv.org/doi/full/10.26434/chemrxiv-2025-g5cqm-v2`, S4) [API] and is likewise no
longer on figshare URLs. [INF]

**The good news for durability:** the *old* figshare-era TechRxiv DOI still resolves, and
still resolves to a figshare-shaped path on the new host. Legacy identifiers were carried
across rather than broken. That is the outcome you want, and it did not happen by accident.

**SAGE Advance** is the counter-case worth watching: its DOIs still resolve to
`advance.sagepub.com/articles/preprint/…` (figshare grammar), and Crossref shows deposits
2018–2025 (167 / 641 / 982 / 819 / 494 / 410 / 517 / 387) with **zero works dated 2026** as
of 2026-09-01 (S4) [API]. That is consistent with a server that has stopped accepting new
material, though I did not obtain a closure announcement — **[NOT-VERIFIED]** as to whether
Advance is formally discontinued.

> **A correction I had to make mid-research, recorded as a method note.** The DataCite
> client `figshare.sage` shows **0** DOIs, which looks like evidence that SAGE's instance is
> dead. It is not: SAGE Advance registers with **Crossref** (4,417 works), not DataCite.
> A zero in one registry is not absence. Always check both registries before concluding a
> platform has no content.

### 5.3 How to sanity-check a figshare item

1. Identify the **instance** (public figshare.com, institutional, or publisher) from the
   host and DOI prefix — these have different curation regimes.
2. Check `defined_type_name`: a `preprint` and a `journal contribution` are different
   claims.
3. Check the licence field per item (§8) — it varies, including non-commercial terms.
4. If the item is a supplement, find the parent article; the supplement inherits none of
   the parent's peer review by being adjacent to it.

## 6. Access, APIs and bulk retrieval

**REST API** — `https://api.figshare.com/v2/`, no key needed for public reads (S1) [API]:

- `POST /v2/articles/search` with a JSON body (`{"page_size":100}`) — **works**, HTTP 200.
- `GET /v2/articles/<id>` — full item record including `license`, `defined_type_name`,
  `doi`, `is_public`.
- `GET /v2/licenses` — the licence vocabulary (§8).
- **No total count is returned anywhere.** Pagination is by opaque `x-cursor` header.

**OAI-PMH** — `https://api.figshare.com/v2/oai` (S3) [API]. `Identify` returns:

```xml
<repositoryName>figshare</repositoryName>
<earliestDatestamp>1800-01-01T00:00:00Z</earliestDatestamp>
<deletedRecord>transient</deletedRecord>
<granularity>YYYY-MM-DDThh:mm:ssZ</granularity>
```

Two observations. `earliestDatestamp` of **1800-01-01** is a placeholder, not a real
date — do not use it for anything. `deletedRecord: transient` means figshare **may** report
deletions but does not guarantee their persistence, so an OAI-based mirror can silently
drift out of sync. (Contrast Zenodo, which declares `no`.)

`ListSets` returns 30 sets (§2). `ListIdentifiers` returns a resumption token but,
as noted, **no `completeListSize`**.

**Negative controls** (S1, S3) [API]:

| Probe | Result |
|---|---|
| `stats.figshare.com/total/views/article` | HTTP **400**, `{"code":"InvalidParams"…"Unknown or usupported item type"}` — endpoint rejects bad params properly |
| `oai?verb=Identify` vs a real fetch | valid XML, correct structure |
| DataCite client-name search for a real vs absent term | see §5.2 method note |

## 7. Landmark papers

figshare hosts no landmark software, systems or electronics *papers* that I could verify as
originating there. Its significance to this knowledge base is **as infrastructure**
(§1, §5.2), not as a venue. No table.

## 8. Licensing and reuse

**Author-chosen from a controlled list.** The `GET /v2/licenses` endpoint returns the
global vocabulary (S1) [API], retrieved 2026-09-01:

| Licence | URL |
|---|---|
| CC BY 4.0 | creativecommons.org/licenses/by/4.0/ |
| CC0 | creativecommons.org/publicdomain/zero/1.0/ |
| MIT | opensource.org/licenses/MIT |
| GPL | gnu.org/copyleft/gpl.html |
| GPL 2.0+ | gnu.org/licenses/gpl-2.0.html |
| GPL 3.0+ | gnu.org/licenses/gpl-3.0.html |
| Apache 2.0 | apache.org/licenses/LICENSE-2.0.html |

Note that this list includes **software licences as first-class options**, which is
consistent with `software` being a supported item type.

**Instances extend the list.** A retrieved institutional item
(`10.25447/sit.33412894.v2`) carries licence value **12, "CC BY-NC-ND 4.0"** (S1) [API] —
a licence absent from the global vocabulary above. So:

- The seven-item list is **not** exhaustive across the federation.
- **Non-commercial and no-derivatives terms occur in practice.** You cannot assume figshare
  content is openly reusable, and you certainly cannot assume it is TDM-friendly. Check
  `license` per item.

**[NOT-VERIFIED]:** figshare's default licence for new deposits, and its text-and-data-mining
policy, were not confirmed from an operator policy document.

## 9. Caveats and controversies

1. **No single "figshare".** The name covers figshare.com, dozens of white-labelled
   institutional repositories on their own domains, and publisher data instances. Claims
   about "figshare policy" are usually claims about one instance. [INF]
2. **Size is not honestly summarisable in one number** (§3). ~4.1M for figshare.com is
   defensible; a federation total is not available.
3. **Commercial ownership.** figshare sits inside Digital Science / Springer Nature (S6)
   [WEB]. A repository whose continuity depends on a commercial parent's product strategy
   carries a different risk profile from CERN-hosted Zenodo — and the preprint-server
   migrations in §5.2 are exactly what that risk looks like in practice, even though in
   those cases the *customers* left rather than the platform failing.
4. **Registry split.** figshare content is registered across **both** DataCite and Crossref
   depending on instance and customer. Any bibliometric study that queries one registry
   will undercount (§5.2 method note).
5. **Operator policy documents not verified** (§4, §8). This is the weakest part of this
   record and is flagged rather than papered over.

## 10. Sources

- **S1** — figshare REST API: `POST https://api.figshare.com/v2/articles/search`,
  `GET /v2/articles/33412894`, `GET /v2/licenses`, and
  `https://stats.figshare.com/total/views/article` (negative control). Retrieved
  **2026-09-01**. Supports: item-type distribution, DOI-prefix and host diversity,
  cursor pagination with no totals, licence vocabulary, CC BY-NC-ND instance licence.
- **S2** — DataCite API: `https://api.datacite.org/clients?query=figshare` and
  `https://api.datacite.org/dois?query=prefix:10.6084`, plus per-client DOI counts.
  Retrieved 2026-09-01. Supports: 33 matching clients, `figshare.ars` = 4,106,613,
  prefix `10.6084` = 4,106,628, institutional client counts, the 4,244,934 partial sum.
- **S3** — figshare OAI-PMH: `https://api.figshare.com/v2/oai?verb=Identify`,
  `?verb=ListSets`, `?verb=ListIdentifiers&metadataPrefix=oai_dc`. Retrieved 2026-09-01.
  Supports: 30 sets and the 25 article types, placeholder `earliestDatestamp`,
  `deletedRecord: transient`, absence of `completeListSize`.
- **S4** — Crossref API: `https://api.crossref.org/prefixes/{10.36227,10.26434,10.31124,
  10.22541}` and `/works` with `facet=published`. Retrieved 2026-09-01. Supports: TechRxiv
  30,954 works (IEEE), ChemRxiv 55,400 (ACS), SAGE Advance 4,417 with per-year breakdown
  2018–2025 and no 2026 works, current resource URLs and their grammars.
- **S5** — DOI resolution probes via `https://doi.org/` for
  `10.36227/techrxiv.14420315`, `10.36227/techrxiv.176281113.30584908/v1`,
  `10.6084/m9.figshare.33412879.v1`, and `10.36227/techrxiv.999999999` (negative control,
  HTTP 404); plus direct HTTP probes of `www.techrxiv.org`, `chemrxiv.org`,
  `advance.sagepub.com`. Retrieved 2026-09-01. Supports: §5.2 migration evidence and the
  403-fingerprint observation.
- **S6** — Wikipedia, *Figshare*, retrieved via the MediaWiki API 2026-09-01. Supports:
  January 2011 launch by Mark Hahnel, January 2012 Digital Science relaunch, Digital
  Science / Springer Nature ownership, PLOS and ImpactStory integrations, hosted
  institutional repository service from September 2013.
- **S7** — Wikipedia, *List of preprint repositories*, wikitext via MediaWiki API,
  2026-09-01. Supports: the "unknown" size entry, 2011 year, Springer Nature operator.

## 11. Retrieval note

`www.techrxiv.org`, `chemrxiv.org` and `advance.sagepub.com` returned **HTTP 403 to every
User-Agent tried** — default, Chrome 131, WhatsApp, ChatGPT-User, ClaudeBot, Googlebot and
Firefox 128 — with near-identical body sizes per agent, indicating an edge bot-block rather
than agent-specific filtering. All substantive claims about those servers in this record
were therefore obtained from **Crossref and DOI resolution behaviour instead of page
scraping**. A useful discriminator emerged: `doi.org` returns **404** for an unregistered
DOI but passes through to the target's **403** for a registered one, so a 403 confirms the
DOI exists even when the page cannot be read.
