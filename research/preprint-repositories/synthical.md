# Synthical — preprint repository record

- **URL:** https://synthical.com/
- **Operator:** **Fast Flash Corporation** ("Made in France and the US", per the site's own
  footer, S1) [WEB]
- **Discipline scope:** *as advertised by Wikipedia* — computer science, mathematics,
  economics, physics, cryptography, biology, chemistry. *As actually operated* — a reader
  interface over arXiv, bioRxiv, medRxiv and ChemRxiv (§1).
- **Launched:** 2023 (first Wayback capture 2023-07-25, S2; site footer "at 2023", S1)
  [WEB] · **Status:** **unreachable from this host on 2026-09-01** (§5)
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

> **Headline finding: Synthical is not a preprint repository.** It is an AI-assisted
> reader and aggregator over other people's preprint servers. It hosts no original
> deposits, mints no identifiers, and is not registered with any DOI agency. The Wikipedia
> characterisation is **misleading** and its ">1,000,000" figure counts *harvested
> third-party articles*, not deposits. Detail and evidence below.

## 1. What it actually is

The decisive evidence is Synthical's own homepage, captured 2023-07-26 (S1) [WEB]. Quoted
verbatim:

> "Synthical: Science, Simplified"
>
> "Discover, learn, and share research, made easy with our AI."
>
> **"3 million articles and growing — We've assembled all articles from Arxiv, Biorxiv,
> Medrxiv, and Chemrxiv, continually updating with fresh content."**
>
> "Make complex concepts simple with our AI"

The page shows a **Simple / Original** toggle applied to an article labelled **"From
arXiv"**, alongside "Collaborate with your team", a pricing block ("Free for everyone /
$-- for additional features"), and the footer **"© Fast Flash Corporation. Made in France
and the US at 2023."** (S1) [WEB].

That is a complete description of the product: **harvest everything from four established
preprint servers, re-present it with an AI simplification layer and team-collaboration
features, and monetise the premium tier.** There is no deposit workflow, no submission
interface, no moderation policy, and no identifier minting described anywhere on the page.

The listed subject areas — Mathematics, Economics, Computer Science, Statistics, Medicine,
Quantitative Finance, Chemistry, Condensed Matter, Biology, Quantitative Biology, Physics,
Quantum Physics, Astrophysics, Electrical Engineering (S1) [WEB] — are simply **arXiv's and
bioRxiv's own category names**. Synthical did not define a taxonomy; it inherited one.

## 2. Does it host original deposits? — the test

A repository that issues citable records must register identifiers with an agency. Synthical
does not. Retrieved 2026-09-01 (S3) [API]:

| Registry probe | Result |
|---|---|
| Crossref members matching `synthical` | **0** |
| DataCite clients matching `synthical` | **0** |
| Crossref works with `synthical` in bibliographic metadata | **0** |

Cross-checked against method controls used elsewhere in this collection: the Crossref prefix
endpoint returns a clean **HTTP 404** for a nonexistent prefix (`10.99999`), and returns real
counts for genuine preprint platforms (TechRxiv 30,954; ChemRxiv 55,400; Authorea 80,599)
(S3) [API]. So these registry APIs *do* answer correctly for real preprint hosts — the zeros
for Synthical are informative, not an artefact of a broken query.

**Conclusion [INF, well-supported]:** Synthical issues no DOIs and therefore hosts no
independently citable original deposits. Anything you read on Synthical is a rendering of a
record whose canonical home, identifier and version history live on arXiv, bioRxiv, medRxiv
or ChemRxiv.

> One honest limitation: a registry name-search is a weaker instrument than a prefix lookup,
> and I did not obtain a positive control for the exact `members?query=` endpoint. The
> conclusion does not rest on the zeros alone — it rests primarily on Synthical's own
> description of itself (§1), with the registry result as corroboration.

## 3. Size — what the ">1,000,000" actually counts

Wikipedia's *List of preprint repositories* records (S4) [WEB]:

| Field | Wikipedia value |
|---|---|
| Description | "Open access preprint repository for computer science, mathematics, economics, physics, cryptography, biology, and chemistry" |
| Size | **">1,000,000"** |
| Year | 2023 |
| Operator | "Synthical" |

Three problems.

1. **The size figure is self-cited.** Wikipedia's reference for ">1,000,000" is
   `https://synthical.com/?is_viewing=true` — the vendor's own homepage (S4) [WEB]. It is
   marketing copy, not an audited count.
2. **It counts other servers' content.** Synthical's own claim at the same period was "3
   million articles… assembled *from* Arxiv, Biorxiv, Medrxiv, and Chemrxiv" (S1) [WEB].
   Whatever the number, it is a measure of **how much of arXiv et al. Synthical has
   ingested**, not of anything deposited with Synthical. Listing it in a table beside
   arXiv's own count double-counts the same documents.
3. **The operator field is circular.** "Synthical" is listed as its own operator; the actual
   corporate entity is **Fast Flash Corporation** (S1) [WEB].

**Verified size of Synthical's original corpus: zero** (§2). **[NOT-VERIFIED]:** the current
size of its harvested index — the site is unreachable (§5).

## 4. Screening and moderation

Not applicable in the repository sense: with no deposit pathway there is nothing to screen.
Whatever editorial screening applies to a given article was applied by **arXiv, bioRxiv,
medRxiv or ChemRxiv** before Synthical ingested it.

The AI layer introduces a *different* risk that no upstream moderation covers: Synthical's
"Simple" mode presents a machine-generated rewrite alongside the "Original" (S1) [WEB]. A
simplified restatement is a derivative work that may drop hedges, conditions or scope
limits. **Never cite a Synthical "Simple" rendering as the content of a paper.** Go to the
original. [INF]

## 5. Durability — current status

**Synthical did not respond on 2026-09-01.** Probe results (S5) [WEB/API]:

| Probe | Result |
|---|---|
| DNS `synthical.com` | resolves to **162.55.17.19** (also `www.synthical.com`) |
| `https://synthical.com/` via curl, Chrome UA, 30 s | **connection timed out** |
| Same, IPv4-forced, 45 s | **connection timed out**, `time_connect = 0.000000` |
| Independent fetch tool, 60 s | **request timed out** |
| Raw TCP to 162.55.17.19:443 | `TimeoutError` |
| Raw TCP to 162.55.17.19:80 | `TimeoutError` |

DNS still resolves, but **no TCP connection is established on either port** — packets are
dropped rather than refused. Control comparison: `zenodo.org` resolved and served requests
normally throughout the same session, so this is not a general network fault at my end.

**Wayback history** (S2) [API]: **68 captures spanning 25 Jul 2023 – 4 Feb 2026**. The
earliest captures return HTTP 200 with real HTML (10,656 bytes on 2023-07-25); captures
from late 2023 onward are predominantly **307/308 redirects** rather than 200s, and the last
capture of any kind is **2026-02-04**.

**What I can and cannot conclude.** I *cannot* declare Synthical dead: an unreachable host
from one network on one day may be a firewall, a geo-block, an outage, or a transient
failure, and this repository's method does not permit upgrading that to "defunct". What I
*can* say is that **the site was not reachable by any means available to me, no capture
exists after February 2026, and no independent liveness confirmation was obtained.** Status
is recorded as **unreachable**, not defunct. **[NOT-VERIFIED]** either way.

**Why this matters regardless of the outcome.** Synthical holds nothing of its own. If it
disappeared tomorrow, **no research record would be lost** — every document it displayed
remains at arXiv, bioRxiv, medRxiv or ChemRxiv under its canonical identifier. That is the
one genuinely reassuring property of a pure aggregator, and it is the direct inverse of the
Authorea situation, where a platform migration *did* put an 80,000-work corpus at the mercy
of a corporate roadmap.

The real durability risk here is to **users, not content**: reading lists, team workspaces,
annotations and any AI-generated summaries created inside Synthical have no external home
and no export guarantee I could verify. [INF]

## 6. Commercial model

From the archived homepage (S1) [WEB]: a freemium structure — "Free for everyone" with
"$-- for additional features" (the price was not rendered in the capture), plus
"Collaborate with your team" and "Synthical for researchers / Try for Free" calls to
action. Contact address `hi@synthical.com`. Operator: **Fast Flash Corporation**.

This is a **venture-style SaaS product built on freely available public content**, not
scholarly infrastructure. It has no institutional backer, no preservation mandate, no
succession plan, and no stated retention policy — none of which it needs, given it holds no
unique content, but all of which matter if you were considering it a repository.

**[NOT-VERIFIED]:** current pricing, funding, corporate status of Fast Flash Corporation,
and terms of service — all unobtainable while the site is unreachable.

## 7. Access, APIs and bulk retrieval

**None verified.** No public API, OAI-PMH endpoint, bulk dump or documented machine
interface could be identified, and the site is unreachable (§5). `robots.txt` and
`sitemap.xml` both timed out.

For the underlying content, use the real sources, all of which have proper bulk interfaces:
arXiv (API + OAI-PMH + S3 bulk), bioRxiv/medRxiv (APIs), ChemRxiv. Harvesting Synthical
would be strictly worse than harvesting upstream, even if it were reachable.

## 8. Landmark papers

None. Synthical is not the venue of first publication for anything — by construction (§2).
No table.

## 9. Licensing and reuse

**[NOT-VERIFIED]** for Synthical's own terms (§6).

The material Synthical displays carries **the licences assigned by depositors on the
originating servers** — arXiv's per-item licences (including non-commercial and
arXiv-perpetual variants), bioRxiv/medRxiv Creative Commons selections, and ChemRxiv's
terms. Those licences govern reuse; Synthical's presentation layer does not and cannot
relicense them. AI-generated "Simple" renderings are derivative works whose status is
**unclear and unverified**. [INF]

## 10. Caveats and controversies

1. **The Wikipedia entry should not be relied on.** It calls Synthical a "preprint
   repository", self-cites the vendor for its size, lists the company as its own operator,
   and places a harvested index count in the same column as genuine deposit counts (§3).
   **This record's finding is that the characterisation is misleading on the central point.**
2. **Aggregator ≠ repository.** The distinction is not pedantry. A repository accepts
   deposits, assigns identifiers, and takes on preservation duty. Synthical does none of
   these. Conflating the two inflates apparent preprint-ecosystem capacity and misdirects
   citations away from canonical identifiers.
3. **Cite upstream, always.** A Synthical URL is not a stable scholarly identifier. Use the
   arXiv ID or DOI.
4. **Do not cite AI-simplified text** as the paper's content (§4).
5. **Currently unreachable** (§5) — with the status deliberately left open rather than
   declared defunct.

## 11. Sources

- **S1** — Synthical homepage, archived snapshot
  `http://web.archive.org/web/20230726125245/https://synthical.com/`, retrieved
  **2026-09-01**. Supports: the "assembled all articles from Arxiv, Biorxiv, Medrxiv, and
  Chemrxiv" statement, "3 million articles and growing", the AI Simple/Original feature and
  "From arXiv" labelling, the inherited category list, the freemium pricing block, the
  `hi@synthical.com` contact, and the "© Fast Flash Corporation. Made in France and the US
  at 2023" footer. Retrieved via an alternate fetch path after direct requests to the live
  site timed out.
- **S2** — Internet Archive Wayback APIs:
  `https://archive.org/wayback/available?url=synthical.com` and
  `http://web.archive.org/cdx/search/cdx?url=synthical.com&output=json`. Retrieved
  2026-09-01. Supports: 68 captures spanning 25 Jul 2023 – 4 Feb 2026, the 2023-07-25
  earliest 200 capture at 10,656 bytes, and the shift to 307/308 responses in later captures.
- **S3** — Registry probes: `https://api.crossref.org/members?query=synthical`,
  `https://api.datacite.org/clients?query=synthical`,
  `https://api.crossref.org/works?query.bibliographic=synthical`; controls
  `https://api.crossref.org/prefixes/10.99999` (HTTP 404) and prefix counts for
  `10.36227` / `10.26434` / `10.22541`. Retrieved 2026-09-01. Supports: §2, zero identifier
  registration and the validity of the comparison.
- **S4** — Wikipedia, *List of preprint repositories*, wikitext retrieved via the MediaWiki
  API, 2026-09-01. Supports: the ">1,000,000" size claim and its self-citation to
  `synthical.com/?is_viewing=true`, the 2023 year, the "Synthical" operator field, and the
  disciplinary description quoted in §3.
- **S5** — Live probes 2026-09-01: DNS resolution of `synthical.com` and
  `www.synthical.com` to 162.55.17.19; HTTPS requests via curl (default and Chrome 131 UA,
  IPv4-forced, 30–45 s timeouts); an independent fetch tool at 60 s; and raw TCP socket
  connections to 162.55.17.19 on ports 443 and 80. All timed out. `zenodo.org` served
  requests normally in the same session as a control.
