# Retrieval notes — scholarly and archival hosts

Findings from probing ~120 scholarly, archival and repository hosts on **2026-09-01 → 2026-09-04**.

> **Status: MERGED into the shared crawler table on 2026-09-20.**
> Per [`AGENTS.md`](../../AGENTS.md) rule 8, these findings now live in
> [`ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md) under a new
> **Scholarly / preprint / archival** section, plus seven additions to *General retrieval tips* and
> a **dated correction** to that file's existing `archive.org/wayback/available` guidance, which
> this pass disproved (see §9). The merge appended only — no existing content was restructured, and
> concurrent unstaged work in that file was left intact.
>
> **This file remains the fuller record**, with per-host byte sizes, probe dates and the reasoning
> behind each finding. The crawler table carries the operational summary.
>
> Nothing below was obtained by bypassing authentication or access control — only public pages, and
> only with the user-agent ladder already documented in `AGENTS.md`. No shadow-library service was
> probed; see [`bulk-libraries-and-shadow-archives.md`](bulk-libraries-and-shadow-archives.md).

---

## 1. Block fingerprints — telling "blocked" from "broken"

The single most reusable output of this pass. **A 403 with a characteristic body size identifies the
blocking product**, which tells you whether to retry, switch route, or give up.

| Body size | Product | Hosts observed |
|---|---|---|
| **~5.2–6.1 kB** | Cloudflare managed challenge (`cf-mitigated: challenge`) | `techrxiv.org` 5,620 · `authorea.com` 5,620 · `essopenarchive.org` 5,622 · `scienceopen.com` 5,602 · `chemrxiv.org` 5,595 · `africarxiv.pubpub.org` 5,583 · `alldatasheet` 5,603 · Advance/SAGE 5,388–5,623 · **`oatd.org`** (incl. `robots.txt`) · `tdx.cat` · `ethos.bl.uk/catalog*` · `graz.elsevierpure.com` |
| ~2.1–7.8 kB | ⚠ **Anubis — but it answers HTTP 200, not 403.** See the soft-200 table below and §3 | `archive.softwareheritage.org` · `rcaap.pt` · `portal.dnb.de` · `base-search.net` · `scipost.org` · `helda.helsinki.fi` |
| **~651 kB** | SHERPA/OpenDOAR block page | `v2.sherpa.ac.uk` 651,922 |
| **1,337 B** | **ETH Zürich custom "Access Restricted"** — self-documenting, gives a contact address, and is **IP/provider-scoped, not UA-scoped** | `research-collection.ethz.ch`. OAI-PMH is open behind it |
| **1,697 B** | Oasisbr "Verificando conexão" interstitial | `bdtd.ibict.br` |
| **~370 B** | minimal 403 (not Cloudflare) | `gao.gov` |
| **369 B** | minimal 403 | `preprints.org` |
| **283 B** | origin UA filter | `bitsavers.org` (to `Wget/1.21.4` and default `curl`) |

**Rule: record the byte size, not just the status.** A ~5.6 kB 403 means the host is alive and
refusing a robot; it does not mean the resource is absent.

### The complement: soft-200s

Worse than a 403, because they look like success.

| Host | Behaviour |
|---|---|
| `osf.io` | **HTTP 200, identical 4,207-byte SPA shell for providers that do not exist.** Confirmed independently — `ecsarxiv.org`, `biohackrxiv.org`, `arabixiv.org`, `psyarxiv.com`, `osf.io/preprints/` all returned exactly 4,207 bytes |
| `unpaywall.org` | **HTTP 200, byte-identical 1,421-byte SPA shell for every path** |
| `eccc.weizmann.ac.il` | **HTTP 200 + 17,041 bytes** for any nonexistent path (17,032 for a bogus year) |
| `openreview.net` | `forum?id=<real>` and `forum?id=ZZZZZZZZZZ` **both** return HTTP 200, 4,787 bytes |
| `papers.ssrn.com/oai` | HTTP 200 "Page Cannot be Found", byte-identical to a bogus path. **SSRN has no OAI-PMH** |
| `optimization-online.org` | ~93,500-byte themed 404 bodies — content-length useless as an existence test |
| `iris.eecs.berkeley.edu` | **58,829-byte themed 404 for every path**, including the technical-report index. See §5 |
| `figshare.com`, `kilthub.cmu.edu` | **HTTP 202 with a zero-byte body** to a plain GET — neither success nor a usable error |
| `escholarship.org` | **HTTP 202 / 0 bytes** — the same non-answer on a third independent tenant |
| `ethos.bl.uk` | **`OrderDetails.do?uin=<bogus>` returns HTTP 200 and the home page.** A link-checker reports 100% success on any legacy EThOS bibliography |
| Google cache | **HTTP 200 with a 91,694-byte Google Search shell.** Silent-corruption hazard — the cache route is gone but returns 200 |
| **Anubis proof-of-work** (`rcaap.pt` 4,511 · `portal.dnb.de` 4,475 · `base-search.net` 7,846 · `scipost.org` 3,903) | **HTTP 200 with a challenge body.** Re-verified 2026-09-11. Detect by `<title>Making sure you're not a bot!</title>` — *not* by status or size. `helda.helsinki.fi` serves Anubis's error page, `<title>Oh noes!</title>`, also at 200 |
| `chinaxiv.org/abs/*` | Same 403 for real and bogus identifiers. Existence untestable. A bogus `.htm` path *does* give a true 404 |

**Clean, trustworthy status codes** — rare enough to be worth naming: `engrxiv.org` (22-byte 404s),
`bitsavers.org` (280-byte 404s), `vixra.org`, and the `api.osf.io` JSON API (61-byte 404s).

---

## 2. The Internet Archive — the most important operational section

Sibling passes measured this twice, two days apart, and **the two runs disagree on both the ceiling
and the failure mode.** The corrected picture:

1. **There is no fixed quota.** One run blocked after ~3 requests; the other made **16 consecutive
   200s and blocked at #17**. The low figure was measured inside an already-throttled window.
2. **429 and TCP-refusal are alternative modes, not an escalation.** One run went straight to
   connection refusal and **never emitted a single 429 in ~60 requests**.
3. **⚠ The throttled state flaps.** Identical Chrome requests one second apart:
   `200 200 000 000 000 200 200 000 000 000`. **A bulk fetch through a throttle window yields a
   silent mixture of retrieved and missing files, with nothing distinguishing "not archived" from
   "refused".** This is the finding most likely to corrupt a harvest.
4. **CDX does *not* stay open.** It lives on `web.archive.org`, the same host as replay, and
   degraded in both runs (`000` in refusal-mode, `503` in 429-mode). The earlier note claiming CDX
   survives while replay blocks is **wrong**.
5. **What actually survives is the `archive.org` host.** During a live block, `wayback/available`,
   `metadata/<id>` and `advancedsearch.php` all returned 200. **Route around by host, not by agent.**
6. **UA rotation is useless here and actively dangerous.** While blocked, `curl` and ClaudeBot
   returned 200 in the same second that Googlebot and no-UA returned `000`. Sampling once would
   record a spurious "working user agent" that is really just the flapping.
7. **Byte sizes drift day-to-day** (replay 16,004→16,006; metadata 4,438→4,437). Good for
   recognising a *class* of response; useless for equality tests.

**Practical rule: retry a CDX query at least twice before recording "no captures".**

### archive.today

**Correction to an earlier note.** `archive.ph/timemap/<url>` **works** — a valid RFC 7089 Memento
TimeMap, HTTP 200 / 1,497 B, 5/5 attempts, plain Chrome UA, no CAPTCHA. Only `/newest/` is walled
(429, 63,290 B). With the Memento Aggregator dead this is the one remaining scriptable way to ask
archive.today what it holds. The previous "no API, everything CAPTCHA-walled" claim was costing a
recovery route. Caveat: undocumented endpoint, verified on one day only.

---

## 3. Proof-of-work walls defeat the UA ladder entirely

A newer obstacle than Cloudflare. **Anubis / BotStopper** issue a JS proof-of-work challenge, and
rotating user agents cannot help — there is no agent that is exempt.

| Host | Behaviour | Way around it |
|---|---|---|
| `www.econstor.eu` | Website behind Anubis | **OAI-PMH wide open.** Probing only over HTTP wrongly concludes EconStor is down |
| `cds.cern.ch` | ~~HTML and REST behind Anubis~~ — **no longer walled** as of 2026-09-11: HTTP 200, 41,946 B, real page | OAI-PMH open — 578,928 records |
| `scipost.org` | Anubis — **HTTP 200** challenge, 3,903 B (re-verified 2026-09-11) | Crossref prefix `10.21468` — 12,558 works |
| `base-search.net` | Anubis v1.27.0+dirty | None found. BASE's size is unverified as a result |
| `archive.softwareheritage.org` | Anubis interstitial (4,667 B) to a browser UA | **A `curl`-style request gets JSON (1,643 B).** The ladder runs *backwards* here |
| `web-archive.southampton.ac.uk` | HTTP **401** for real *and* bogus paths | None found. CogPrints' item count stays unverified |
| `hprints` | Anubis wall | Open API behind it |
| **`theses.hal.science`** (`devel`) · **`portal.dnb.de`** (1.25.0) · **`trove.nla.gov.au`** (v1.26.2) · **`helda.helsinki.fi`** (1.23.0) · **`dans.knaw.nl`** (1.25.0) | Anubis, national-library layer | Protocol change — OAI-PMH / REST |
| **`rcaap.pt`** (v1.26.0-pre2) | Anubis — **HTTP 200** challenge, 4,511 B (re-verified 2026-09-11) | **None — the first host where the OAI-PMH escape hatch is *also* behind the wall.** The general rule below has an exception |

**Anubis has spread from a handful of sites to the national-library layer during this survey** — nine hosts now, versions 1.23.0 through 1.27.0. Treat it as the emerging default, not an oddity.

**General rule worth promoting to the main table: when a scholarly site blocks you, look for OAI-PMH, Crossref, Handle.net or a REST API before concluding it is unreachable.** In eight of nine cases here the machine-readable interface was open while the human-facing one was walled — `rcaap.pt` is the sole counter-example.

**The UA ladder solved nothing in the thesis pass.** What worked was **changing protocol**: DSpace 7 REST, DataCite, OAI-PMH, Handle.net. Record that alongside the ladder, because rotating agents against a proof-of-work wall is wasted effort by construction.

---

## 4. Existence oracles that work behind a bot wall

### `hdl.handle.net` — the best one found

`https://hdl.handle.net/api/handles/<prefix>/<suffix>` returns JSON with `responseCode: 1` for a
handle that exists and `100` for one that does not. It is **served by the Handle System, not by the
target repository, so it is immune to the target's bot wall.** Verified against Cloudflare-walled
TDX (prefix `10803`) and MIT DSpace (prefix `1721.1`).

**Strictly better than the `doi.org` trick below** wherever a handle exists — it gives a positive
JSON answer rather than an inference from a status code. Most DSpace and EPrints repositories mint
handles, so this covers most institutional repositories and nearly all ETD systems.

### `doi.org` — the fallback

- `doi.org` returns **404 for an unregistered DOI**.
- For a **registered** DOI it redirects and **passes through the target host's 403**.

**A 403 from a `doi.org` redirect therefore confirms the record exists**, even when the landing page
cannot be read. This made it possible to measure PeerJ Preprints, ChemRxiv and TechRxiv while all
three were unreadable.

---

## 5. Per-host reachability

Measured directly on **2026-09-01**, following redirects, Chrome 131 UA. `bytes` is the body size.

| Host | Code | Bytes | Note |
|---|---|---|---|
| `arxiv.org` | 200 | 38,051 | |
| `eprint.iacr.org` | 200 | 14,117 | 20/min per-path limit, see §6 |
| `zenodo.org` | 200 | 69,556 | |
| `hal.science` | 200 | 12,606 | default `curl` sufficient |
| `optimization-online.org` | 200 | 98,725 | 404 bodies ~93.5 kB |
| `engrxiv.org` | 200 | 22,323 | honest 404s |
| `chinaxiv.org` | 200 | 104,948 | but `/abs/*` 403s all agents |
| `jxiv.jst.go.jp` | 200 | 44,900 | |
| `preprints.scielo.org` | 200 | 39,311 | |
| `preprints.ru` | 200 | 27,658 | |
| `preprints.aijr.org` | 200 | 31,101 | |
| `researchsquare.com` | 200 | 22,147 | |
| `qeios.com` | 200 | 411,206 | |
| `vixra.org` | 200 | 10,486 | correct hard 404s |
| `ssrn.com` | 200 | 70,049 | but `papers.ssrn.com` 403s everything |
| `ideas.repec.org` | 200 | 29,872 | asks you not to scrape |
| `econstor.eu` | 200 | 4,806 | Anubis; OAI open |
| `biorxiv.org` | 200 | 31,863 | **429 to Chrome/curl/ClaudeBot; 200 to `WhatsApp/2.23.20.0`** |
| `medrxiv.org` | 200 | 39,119 | |
| `philarchive.org` | 200 | 635,810 | |
| `philsci-archive.pitt.edu` | 200 | 45,028 | **ladder runs backwards — default `curl` beats Chrome** |
| `lingbuzz.net` | 200 | 16,418 | **HTTP 502 for out-of-range IDs; no `HEAD`** |
| `roa.rutgers.edu` | 200 | 6,278 | "API" is a 1,463-row XLSX |
| `eprints.rclis.org` | 200 | 13,476 | EPrints 3.4.6 |
| `web.ma.utexas.edu/mp_arc/` | 200 | 5,516 | frozen archive, intact |
| `eartharxiv.org` | 200 | 11,141 | |
| `socopen.org` | 200 | 82,394 | |
| `indiarxiv.in` | 200 | 97,976 | relaunch, 0 records |
| `osf.io/preprints/` · `ecsarxiv.org` · `biohackrxiv.org` · `arabixiv.org` · `psyarxiv.com` | 200 | **4,207** | identical SPA shell — meaningless |
| `figshare.com` | **202** | **0** | zero-byte body |
| `techrxiv.org` | 403 | 5,620 | every path except `/robots.txt` |
| `authorea.com` | 403 | 5,620 | |
| `scienceopen.com` | 403 | 5,602 | |
| `chemrxiv.org` | 403 | 5,595 | |
| `essopenarchive.org` | 403 | 5,622 | |
| `africarxiv.pubpub.org` | 403 | 5,583 | block page **differs by agent** — ChatGPT-User got 25 B |
| `preprints.org` | 403 | 369 | |
| `synthical.com` | **000** | 0 | DNS resolves `162.55.17.19`; TCP :443 and :80 both time out |
| `cogprints.org` | **000** | 0 | **TLS SAN mismatch** (cert is `CN=web-archive.southampton.ac.uk`). ⚠ **The plain-HTTP recovery route has since degraded** — on 2026-09-11 it 301s to Southampton and returns **HTTP 401** (7,493 B, BotStopper), not 200 |

**Blocking all agents tried:** `papers.ssrn.com` (including Googlebot) · `peerj.com` ·
`hrbopenresearch.org` · `amrcopenresearch.org` · `cell.com` · `cabidigitallibrary.org` ·
`dl.acm.org/opentoc` · `doabooks.org` · `science.org` (no Wayback snapshot either) ·
`crimrxiv` (apex + WhatsApp UA succeeded exactly once, then reverted).

**Unreachable by TCP, not by policy:** `hpl.hp.com` (DNS resolves `15.73.144.188`, TCP times out) ·
`datasheetcatalog.com` (NXDOMAIN) · Berkeley CS262A reading list (connect failure) ·
`catalogodeteses.capes.gov.br` (`getent hosts` returns **only AAAA**; an A record exists via
`ahostsv4` — an IPv6-only resolution path that looks like a dead host).

### Berkeley EECS went dark mid-survey, then came back at a new path

**Corrected on re-probe 2026-09-11.** During the original pass `www2.eecs.berkeley.edu` 302-redirected
to `iris.eecs.berkeley.edu`, which served a 58,829-byte themed 404 for every path including the
technical-report index.

**The series is now restored on its original host**, at a new `/Archive/` path segment:
`https://www2.eecs.berkeley.edu/Pubs/TechRpts/<year>/Archive/<report>.pdf`. All six RISC-V reports
return HTTP 200 with `%PDF-` magic; `EECS-2016-1` is **959,927 bytes**, matching both the pre-outage
size and the Wayback capture. The index is back at 200 / 122,784 B.

`iris.eecs.berkeley.edu` still serves the 58,829-byte themed 404 (negative control confirmed), so it
was a staging artefact of a migration in progress rather than a new home. The earlier note in this
file recording `www2.eecs.berkeley.edu` as *TCP-dead* was a transient and is withdrawn.


---

## 6. Rate limits and terms

- **`eprint.iacr.org`** — no UA fallback needed, but a hard Cloudflare **"20 per 1 minute" per-path
  limit with no `Retry-After`**. `robots.txt` is `Disallow: /` by default while whitelisting
  `Claude-User`/`Claude-SearchBot` for metadata and banning all PDFs. **TDM explicitly reserved
  despite the PDFs being CC-BY.** OAI-PMH returns all 27,552 identifiers in one 3.34 MB response.
- **arXiv** — "no more than one request every three seconds." Honour it.
- **OpenAlex** — **rate limiting is now credit/USD denominated**: `x-ratelimit-limit: 1000`,
  `x-ratelimit-limit-usd: 0.1`, `meta.cost_usd: 0.0001`. **Harvesters written against the old
  "polite pool, 100k/day" documentation fail silently.**
- **RePEc** — asks you not to scrape; API behind a written application. Two RePEc documents
  disagree on commercial use.
- **ECCC** — no OAI-PMH, no API, no dump; licence permits only "interactive viewing and/or printing
  for personal use", i.e. **TDM forbidden**.
- **Semantic Scholar** — HTTP 429 unauthenticated; HTTP 500 on bulk. Needs a key.
- **NASA ADS** — HTTP 401; token mandatory.
- **`bitsavers.org`** — blocks `Wget` and default `curl` (403/283 B) but serves Chrome. **Its
  `robots.txt` is HTTP 200 with zero bytes**, so a naive crawler reads an open invitation and then
  gets 403. Correct route is the operator-sanctioned `rsync://bitsavers.org/`, or a mirror —
  **mirrors do not apply the origin's block**, which is the right answer rather than UA substitution
  (`AGENTS.md` rule 7).
- **`dblp`** — all three mirrors returned 503 on the bulk `dblp.xml.gz` dump. Retry later; the data
  is CC0.

---

## 7. API traps that silently corrupt a harvest

Not access control, but they will poison a dataset without erroring. Cross-referenced in
[`README.md § Probing traps`](README.md#6-probing-traps).

- **arXiv API `max_results=0` is broken** — HTTP 200, `totalResults=1`, and a fake entry titled
  "Error". A harvester using it records **1 for every category**. Use `max_results=1`. The API also
  returns 200 with an empty feed for nonexistent papers, while the web front end 404s.
- **arXiv aliases `cs.NA` and `cs.SY` return 0** on API queries — silent data loss.
- **HAL's subject field is `domainAllCode_s`, not `domain_s`** — the wrong field returns a
  confident, silent `numFound: 0`.
- **Zenodo returns HTTP 200 with `total: 0` for invalid facet values.** Separately, unquoted
  `RISC-V` returns 422,778 hits against 495 quoted — an **~850× inflation** from hyphen
  tokenisation.
- **NTRS and OSTI both treat an empty `q=` as "match nothing", not "match everything"** — two
  independent federal agencies, same trap. **CiNii Dissertations makes it three** (no parameters →
  `totalResults: 0`; `q=*` → 0). **Promote this to a general rule: never trust an empty or wildcard
  query to mean "everything" — always cross-check against a known-populated facet.** NTRS holds
  646,950 records but **only 358,213 (55.4%) actually have a document attached**. OSTI puts its
  total in the `x-total-count` **header**, and `links[rel=fulltext]` → `/servlets/purl/<id>` is a
  verified direct-PDF route.
- **OAI-PMH signals errors in the body with HTTP 200.** An invalid verb against ETH's endpoint
  returns 200 with a 488-byte error document. **Never status-check an OAI-PMH endpoint** — parse it.
- **`api.core.ac.uk/v3/search/works` without the trailing slash returns HTTP 200 and a Cloudflare
  `cdn-cgi/content` HTML redirect**, not JSON.
- **`theses.fr/api/v1/theses/these/<bogus>` returns HTTP 200 with a zero-byte body.**
- **Shodhganga carries a stale count inside an HTML comment** — `597316` in `<!-- -->` beside the
  live `697675`. A tag-stripper that ignores comments reads **100,359 too low**.
- **`web.archive.org/cdx` returned a negative `length` field**: `20250926194305 403 -6693296525`.
  Validate numeric fields from CDX before arithmetic.
- **OpenReview's per-venue counts cap at 10000.** ICLR 2025 and 2026 both read exactly `10000` —
  that is a ceiling, not a count. Between 2026-09-02 and 09-04 all `/notes` endpoints moved behind
  `ChallengeRequiredError` (403) to **six different user agents**, so the figures could not be
  re-derived.
- **SSRN networks must never be summed** — 68 networks total 4,569,102 against ~1.5 M actual papers
  (≈3.0 cross-listings each).
- **Zenodo, OSF and TechRxiv count *versions*, not works.** Measured inflation +1.6% to +50%;
  TechRxiv is 30,954 DOI records for 18,890 items.
- **Unpaywall is DOI-keyed and has a measurable arXiv blind spot.** `10.1145/3079856.3080246` (the
  TPU paper) returns `oa_status: closed` with zero locations; OpenAlex agrees because it inherits
  Unpaywall. **Semantic Scholar returns `externalIds.ArXiv: "1704.04760"`.** If the author never
  added the DOI to the arXiv record, no edge exists. Always cross-check Semantic Scholar.
- **Unpaywall's free bulk snapshot is ~21 months stale** (newest 2024-11-27, 39.2 GB). OpenAlex's S3
  snapshot is free and current.
- **`CiteSeerX` is dead, and its negative control proves it**: every path — including `robots.txt`
  and a deliberately bogus path — 301s to a *fixed* Wayback timestamp `20251230112235`. Following it
  returns 429.
- **`api.biorxiv.org` returns two plausible totals in one object** — `total` (479,561, every
  version) and `count_new_papers` (348,506, distinct preprints). The obvious field is the wrong one
  for counting preprints. Verified 2026-09-11.
- **Follow redirects when probing APIs.** `zenodo.org/api/*` and `export.arxiv.org` over HTTP both
  301; omitting `-L` yields an empty body that reads as a block. Two false "rate-limited"
  conclusions in this pass traced to exactly this.
- **PMC's legacy `oa.fcgi` endpoint 404s** on both `ncbi.nlm.nih.gov` and `pmc.ncbi.nlm.nih.gov`.

---

## 8. TLS state as an abandonment signal

Expired or never-issued certificates found: `africarxiv.ubuntunet.net` (expired 2026-07-25),
`latarxiv.org` (expired 2026-08-20 19:26:19), `rinarxiv.lipi.go.id` (self-signed `CN=linux`, 2023).
`www.inarxiv.id` is **NXDOMAIN**.

**The converse does not hold.** `bodoarxiv.org`, `lawarxiv.org`, `mediarxiv.org` and `frenxiv.org`
all carry fresh auto-renewed certificates while being, respectively, an online casino, a 114-byte
parking stub, a stranger's redirect and a six-year-frozen zombie. **Parking services run ACME.**
In this dataset TLS automation outlived editorial staffing in every divergent case. See
[`reliability-and-durability.md` §5](reliability-and-durability.md#5-durability--the-headline-result).

---

## 9. Archival candidates

**Every candidate examined in this pass turned out to be already archived.** That conclusion was
reached twice — the first time wrongly, in the opposite direction — and the reason is important
enough to lead with.

### ⚠ `archive.org/wayback/available` returns false negatives. Use CDX.

The canonical "is this URL archived?" endpoint **reported no captures for a URL that has been
continuously archived since 2018.**

```
archive.org/wayback/available?url=cs.helsinki.fi/u/kutvonen/index_files/linus.pdf
  → {"archived_snapshots": {}}          # 2026-09-04, repeated, two separate sessions

web.archive.org/cdx/search/cdx?url=...&output=json
  → captures 2018-05-11 … 2026-08-07, HTTP 200        # same URL, same minute
```

**This is the worst failure mode in the whole survey**, because it fails *toward* unnecessary work
and false alarm: it tells you a document is unpreserved when it is safe. Anyone auditing link rot
with `wayback/available` will manufacture phantom losses.

**Rule: `wayback/available` is advisory only. Confirm absence with the CDX API before declaring
anything unarchived.** Note this compounds with the throttling in §2 — CDX itself degrades under
load, so retry twice before trusting a negative from *either*.

### Resolved: the Torvalds thesis was never at risk

Recorded in an earlier revision of this file as unarchived and needing urgent rescue. **It is fully
preserved and byte-identical.**

| Property | Value |
|---|---|
| URL | `cs.helsinki.fi/u/kutvonen/index_files/linus.pdf` |
| Live size / type | **470,861 B**, `%PDF-1.3`, `Last-Modified: 2019-04-10` |
| Live SHA-256 | `9fc48f477a9edc9592c52e912b3924da4595056b858486631d26f0f996b85714` |
| Live SHA-1 (base32) | `ZVCIUY5JU6PJW3CN37K277F2Z4HLXYPV` |
| Wayback CDX digest | `ZVCIUY5JU6PJW3CN37K277F2Z4HLXYPV` — **identical** |
| Coverage | 2018-05-11 → **2026-08-07**, one digest throughout: the file has never changed |

The **CDX `length` field is the WARC record length, not the payload size** (422,587 / 418,490 /
438,660 across captures of the same bytes). **Never compare `length` to a file size** — compare the
digest, which is a base32 SHA-1 of the payload and is directly checkable against a local copy, as
above.

### Berkeley EECS — the whole RISC-V set is recoverable

Despite the live series being down (§5), **all six reports have HTTP 200 Wayback captures**:

| Report | Newest 200 capture |
|---|---|
| UCB/EECS-2011-62 | `20260505221228` |
| UCB/EECS-2011-63 | `20250521085055` |
| UCB/EECS-2014-54 | `20251231214818` |
| UCB/EECS-2016-1 | `20260409151000` |
| UCB/EECS-2016-118 | `20251115022521` |
| UCB/EECS-2016-161 | `20220621081911` |

Durable form: `https://web.archive.org/web/<timestamp>/https://www2.eecs.berkeley.edu/Pubs/TechRpts/<year>/<report>.pdf`

### Remaining candidates

| Candidate | Status |
|---|---|
| **Stanford CS/CSL technical-report index** (1,332 bytes) | **OPEN** — the only genuinely unchecked item. Verify with CDX, not `wayback/available` |
| `web.ma.utexas.edu/mp_arc/` · `roa.rutgers.edu/info.html` · `optimization-online.org` old `DB_HTML` | Already captured |

**Note on `save/` semantics:** HTTP **523** means the job was refused (throttling) and nothing was
saved; HTTP **302** means it was accepted. Neither confirms a capture — **re-check via CDX**.

**Standing finding worth propagating:** the DEC SRC/WRL/CRL research-report series survives *only*
because someone mirrored it to bitsavers in 2007 — 521 reports plus a 236,085,636-byte
`Compaq-DEC_TRs_HPL_mirror_2007.zip`, while `hpl.hp.com` is TCP-dead. See
[`recovering-dead-technical-sites.md`](recovering-dead-technical-sites.md). Berkeley is the same
story caught earlier, and with a better outcome.
