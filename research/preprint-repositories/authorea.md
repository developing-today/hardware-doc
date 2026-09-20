# Authorea — preprint repository record

- **URL:** https://www.authorea.com/
- **Operator:** **Wiley** (John Wiley & Sons). Originally Authorea, Inc.; acquired by
  **Atypon** in 2018; Atypon has been Wiley-owned since 2016 (S3, S4) [WEB]. Crossref still
  records the DOI prefix owner as "Authorea, Inc." while listing the publisher as "Wiley"
  (S1) [API].
- **Discipline scope:** multidisciplinary. In practice: Wiley journal submissions plus
  Earth/space science (§4).
- **Launched:** **February 2013** (S3) [WEB] · **Status:** active as a corpus, but
  **direct submissions suspended since May 2026** (S3) [WEB] — see §5.
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What it is

Authorea began as a **collaborative writing tool**, not a repository. Alberto Pepe and
Nathan Jenkins — who met at CERN — built a web-based real-time collaborative editor for
scientific manuscripts, with support for embedding data and executable code (S3) [WEB]. The
preprint-hosting function was a consequence of the editor: if the manuscript already lives
on the web at a stable URL, giving it a DOI is a small step.

That origin explains most of what is strange about Authorea. It is a **writing platform
that emits preprints**, so its corpus contains things no curated preprint server would
carry — including editor demonstration documents (§5.1). It also explains why Authorea
became attractive to publishers: it is a manuscript pipeline, and a manuscript pipeline can
be pointed at a journal.

Authorea's second life is as **white-label preprint infrastructure**. Wikipedia records
that it "expanded as a platform to host branded partner preprint archives, such as the
Earth Space Science Open Archive and TechRxiv" (S3) [WEB] — a claim this record confirms
independently from DOI and URL evidence (§4).

Its third life began in **2026**, and is the reason this record is a cautionary tale (§5).

## 2. Scope and content types

Crossref work types under prefix `10.22541`, retrieved 2026-09-01 (S1) [API]:

| Type | Works |
|---|---|
| Posted Content (i.e. preprints) | **80,496** |
| Dataset | 103 |
| **Total** | **80,599** |

There is no subject taxonomy comparable to arXiv's. Content is organised by *which branded
archive* it belongs to, which is expressed in the **DOI infix** (§4).

## 3. Size and growth

**80,599 works** under prefix `10.22541` (Crossref, 2026-09-01, S1) [API].

By publication year (S1) [API]:

| Year | Works | | Year | Works |
|---|---|---|---|---|
| 2017 | 81 | | 2022 | 9,345 |
| 2018 | 87 | | 2023 | 12,744 |
| 2019 | 317 | | 2024 | **17,508** |
| 2020 | **11,076** | | 2025 | 16,229 |
| 2021 | 7,426 | | 2026 | **5,683** |

Two inflection points matter.

**The 2020 jump** (317 → 11,076, a 35× increase) is when Authorea stopped being a niche
writing tool and became publisher infrastructure — consistent with the ESSOAr migration and
the launch of Wiley's "Under Review" service, under which a submission to a participating
Wiley journal is automatically posted as an Authorea preprint (S3) [WEB]. Most of this
corpus is therefore **not** author-initiated preprinting; it is journal submissions
mirrored into a preprint archive. [INF]

**The 2026 collapse** (16,229 → 5,683, with the year two-thirds elapsed) is the migration
and submission suspension described in §5. My Crossref counts and Wikipedia's account were
obtained independently and agree.

**Wikipedia conflict:** the *List of preprint repositories* records Authorea's size as
**">10,000"** and its operator as **Atypon** (S5) [WEB]. The size is technically true but
understates by 8×; the operator is one corporate layer out of date (Atypon is the
subsidiary; Wiley is the owner, S3/S4). Both entries are stale rather than wrong.

## 4. The branded-archive structure — and ESSOAr

**One DOI prefix, multiple archives, distinguished by infix.** From a random sample of 100
works under `10.22541` (S1) [API]:

| Resource host | Share of sample |
|---|---|
| `www.authorea.com` | 83 |
| `essopenarchive.org` | 17 |

The DOI patterns map onto those hosts:

- `10.22541/au.<digits>.<digits>/v1` → Authorea proper, e.g.
  `10.22541/au.175225950.03002018/v1`
- `10.22541/essoar.<digits>.<digits>/v1` → **ESS Open Archive**, e.g.
  `10.22541/essoar.174708101.14406736/v1`, served from
  `https://essopenarchive.org/doi/full/…`

**This confirms the ESSOAr relationship directly.** AGU's Earth and Space Science Open
Archive is not merely "similar to" Authorea — its DOIs are **minted under Authorea's own
Crossref prefix**, registered to Authorea, Inc. ESSOAr runs on Authorea infrastructure with
its own domain and branding. [API]

The same pattern independently identifies **TechRxiv** as a migrant onto this stack: current
TechRxiv DOIs resolve to `www.techrxiv.org/doi/full/10.36227/techrxiv.176281113.30584908/v1`
(S2) [API] — the identical `/doi/full/<doi>/v<n>` grammar and paired-numeric suffix, differing
only in that IEEE kept its own prefix. Wikipedia's Authorea article states the same thing in
prose (S3) [WEB]. Two independent lines of evidence, one inferred from data and one
documentary, agree.

> **Practical note:** the version suffix is **load-bearing** for ESSOAr DOIs.
> `https://doi.org/10.22541/essoar.174708101.14406736` returns **HTTP 404**, while the same
> DOI with `/v1` resolves (S2) [API]. Strip the version from an ESSOAr DOI and you break it.

## 5. Reliability, durability and the 2026 migration

### 5.1 Screening — effectively none, historically

Authorea applied no meaningful screening as a writing platform. The clearest evidence is a
record that survives in Crossref with a registered DOI (S1) [API]:

> **"This is an example of an interactive Carto graph in Authorea"** —
> `10.22541/au.155612609.93435564`

That is a **product demonstration page** carrying a permanent scholarly identifier. If a
demo document is indistinguishable, at the identifier layer, from a research preprint, the
identifier is telling you nothing about content.

Note that Wiley's own stated reason for suspending submissions in 2026 is in part to
"improve editorial and integrity screening processes" (S3) [WEB] — an implicit
acknowledgement that the prior screening was inadequate. [INF]

### 5.2 The durability finding — this is the cautionary tale

**What happened.** Per Wikipedia (S3) [WEB], Authorea "now exists as Wiley's own preprint
archive following migration of the Authorea and all partner preprint archives to Wiley's own
**Research Exchange Preprints** platform, launched in **2026**". Further: "Wiley have
temporarily suspended direct submissions following the migration to Research Exchange
Preprints in **May 2026**, in order to 'assess new workflows, improve editorial and
integrity screening processes, and upgrade user support'."

**What I verified independently:**

- Deposits collapsed in 2026 to 5,683 from 16,229 (§3) (S1) [API] — consistent with
  submissions stopping partway through the year.
- The corpus itself is **still identified and still resolving**: DOI
  `10.22541/au.164141365.55966776/v1` resolves through `doi.org` to a live Authorea article
  URL (S2) [API].

**What this means for anyone who deposited on Authorea.** In under a decade the platform
went Authorea, Inc. → Atypon (2018) → Wiley → Research Exchange Preprints (2026), with
submissions suspended at the last step. **The corpus survived each transition; author
control did not.** A researcher who chose Authorea in 2015 for its collaborative editor is
now a Wiley platform customer with submissions frozen, and had no say in any of it.

The generalisable lesson: **a preprint that lives inside a product is hostage to that
product's roadmap.** Zenodo's retention promise is tied to an institution with a 20-year
research programme; Authorea's was tied to a startup that was acquired twice. Both preserved
the bits. Only one of them made a commitment about it.

### 5.3 Are the preprints still reachable and citable?

**Citable: yes.** 80,599 DOIs remain registered in Crossref with resolvable targets (S1,
S2) [API].

**Reachable by a machine: not reliably.** `www.authorea.com` and `essopenarchive.org`
returned **HTTP 403 to every User-Agent tried** — default, Chrome 131, WhatsApp,
ChatGPT-User, ClaudeBot, Googlebot 2.1 and Firefox 128 (S2) [WEB]. Body sizes were
near-identical per agent (5,385–5,622 bytes), indicating a uniform edge bot-block rather
than agent-specific filtering. I could not read a single Authorea page.

**Reachable by a human: [NOT-VERIFIED].** A 403 to automated clients does not establish
that a browser is blocked, and per this repository's method I must not claim otherwise. But
it does mean Authorea content is **effectively invisible to text mining, automated
citation checking and archival crawlers**, which is itself a durability defect.

A useful discriminator emerged: `doi.org` returns **404** for an unregistered DOI
(`10.36227/techrxiv.999999999` → 404) but passes through to the target's **403** for a
registered one. So a 403 here *confirms* the record exists even though it cannot be read
(S2) [API].

### 5.4 How to sanity-check an Authorea record

1. **Read the DOI infix**: `/au.` = Authorea proper; `/essoar.` = ESS Open Archive. These
   are different editorial contexts.
2. **Keep the `/vN` suffix** — required for resolution (§4).
3. **Ask whether it is a Wiley "Under Review" auto-post**, in which case it is a journal
   submission under consideration, not an author's deliberate preprint. [INF]
4. **Do not assume a human curated it** (§5.1).
5. Query Crossref (`api.crossref.org/works/<doi>`) rather than scraping — the site will
   refuse you (§5.3).

## 6. Access, APIs and bulk retrieval

- **No public repository API was reachable.** Authorea exposes no documented REST or
  OAI-PMH endpoint that I could retrieve, and the website is bot-blocked (§5.3).
- **Use Crossref instead.** Everything quantitative in this record came from
  `https://api.crossref.org/prefixes/10.22541/works`, which supports `rows`, `sample` and
  `facet=published` / `facet=type-name` (S1) [API]. This is the practical bulk-access path
  for Authorea and ESSOAr metadata.
- **DataCite returns nothing:** `prefix:10.22541` gives `total: 0` in DataCite (S1) [API].
  Authorea registers with **Crossref**, not DataCite. A zero in one registry is not absence
  — Crossref's own negative control (`10.99999`) correctly returns **HTTP 404**, so the
  Crossref counts above are trustworthy while the DataCite zero is merely uninformative.
- **Full text is not bulk-retrievable** by any route I found. [NOT-VERIFIED]

## 7. Landmark papers

None verified. Authorea is a general-purpose host whose corpus is dominated by Wiley
journal submissions and Earth/space science; I found no landmark software, systems or
electronics work that originated here, and I am not going to nominate one on the strength
of a title search. No table.

## 8. Licensing and reuse

**[NOT-VERIFIED].** I could not retrieve Authorea's licensing policy, its default licence,
or its text-and-data-mining terms, because every page request was refused with HTTP 403
(§5.3) and no policy document was reachable by any other route.

What can be said: Crossref metadata for the prefix is available under Crossref's normal
terms, and the works are typed `Posted Content`. **Assume nothing about reuse rights for
Authorea full text.** Given Wiley ownership, the prudent default is to treat individual
items as all-rights-reserved unless the item itself states otherwise.

## 9. Caveats and controversies

1. **Ownership is three layers deep and the public record lags.** Crossref says "Authorea,
   Inc."; Wikipedia's list says "Atypon"; the actual owner is Wiley (S1, S3, S4, S5).
2. **Much of the corpus is not voluntary preprinting** but Wiley "Under Review" auto-posting
   (§3) [INF]. Treating Authorea deposit counts as evidence of preprint culture would be a
   mistake.
3. **Submissions are suspended** as of May 2026 (S3) [WEB]. Anyone planning to deposit
   should verify current status first.
4. **Demo content carries DOIs** (§5.1).
5. **The platform is closed to machines** (§5.3), which compromises independent verification
   — including this record's. Every claim here about Authorea's *content* is mediated through
   Crossref, not through reading the site.
6. **Wikipedia is load-bearing for the 2026 migration narrative.** The Research Exchange
   Preprints migration, the May 2026 suspension date and the quoted Wiley rationale all rest
   on S3, since the primary notice sits on a page I cannot load. My independent Crossref
   evidence corroborates the *timing and magnitude* of a submission stoppage but not the
   stated reasons. Flagged as partially **[NOT-VERIFIED]**.

## 10. Sources

- **S1** — Crossref API: `https://api.crossref.org/prefixes/10.22541`,
  `/prefixes/10.22541/works` with `rows`, `sample=100`, `facet=published:30` and
  `facet=type-name:20`; plus DataCite `https://api.datacite.org/dois?query=prefix:10.22541`
  and the Crossref negative control `/prefixes/10.99999` (HTTP 404). Retrieved
  **2026-09-01**. Supports: 80,599 total, 80,496 Posted Content / 103 Dataset, the
  year-by-year table, prefix owner "Authorea, Inc." with publisher "Wiley", the
  authorea.com/essopenarchive.org host split, the Carto demo record, DataCite absence.
- **S2** — DOI resolution and HTTP probes: `https://doi.org/10.22541/au.164141365.55966776/v1`,
  `https://doi.org/10.22541/essoar.174708101.14406736` (404 without version suffix),
  `https://doi.org/10.36227/techrxiv.176281113.30584908/v1`,
  `https://doi.org/10.36227/techrxiv.999999999` (negative control, 404); direct requests to
  `https://www.authorea.com/` and `https://essopenarchive.org/` under seven User-Agents.
  Retrieved 2026-09-01. Supports: §4 version-suffix requirement, §5.3 bot-block findings and
  the 403-vs-404 discriminator.
- **S3** — Wikipedia, *Authorea*, retrieved via the MediaWiki API 2026-09-01. Supports:
  February 2013 launch by Alberto Pepe and Nathan Jenkins with Matteo Cantiello (met at
  CERN), 2018 Atypon acquisition, Wiley ownership, branded partner archives including ESSOAr
  and TechRxiv, Wiley "Under Review" auto-posting, the 2026 migration to Research Exchange
  Preprints, and the May 2026 suspension of direct submissions with the quoted rationale.
- **S4** — Wikipedia, *Atypon*, retrieved via the MediaWiki API 2026-09-01. Supports:
  Atypon founded 1996, Literatum platform, **owned by John Wiley & Sons since October 2016**
  — the link that makes Authorea a Wiley property.
- **S5** — Wikipedia, *List of preprint repositories*, wikitext via MediaWiki API,
  2026-09-01. Supports: the ">10,000" size entry, 2013 launch year, and "Atypon" as listed
  operator, all compared against measured values in §3.
