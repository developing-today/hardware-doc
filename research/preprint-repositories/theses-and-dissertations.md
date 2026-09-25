# Theses and dissertations — the long version of the paper

> ⚠ **Dating correction (added 2026-09-11).** This record is stamped **2026-09-04** throughout, but
> its actual research and write date is **2026-09-07** (filesystem mtime) — a stale "today" was
> carried into the research brief. **Read every `2026-09-04` below as "2026-09-06/07".**
> Server-supplied dates (e.g. the EThOS ResourceSync `at=2026-09-06`) are genuine and unaffected.
> Dates have not been rewritten in place, because the exact probe date per claim cannot be
> reconstructed and false precision would be worse than a flagged approximation.
> See [`VERIFICATION.md §1.6`](VERIFICATION.md#16--dating-error-in-the-theses-record).

- **Compiled:** 2026-09-04. Every figure was measured on that date unless another date is stated.
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).
- **Companion record:**
  [`government-and-institutional-technical-reports.md`](government-and-institutional-technical-reports.md).
  That record covers documents that were *never* papers because an institution commissioned a
  report. This one covers documents that were never papers because a **degree committee** demanded
  something longer. The two overlap deliberately and in one place literally — Berkeley EECS files
  its PhD dissertations *inside* its technical-report series, which is why `UCB/EECS-2016-1` is
  both a technical report and the RISC-V design dissertation (§5.4, §9).
- **Sibling records referenced throughout:**
  [`open-access-full-text-sources.md`](open-access-full-text-sources.md) (CORE, BASE, OpenAIRE as
  *paper* sources — this record covers only their ETD angle),
  [`closed-and-defunct-servers.md`](closed-and-defunct-servers.md) (durability failure modes),
  [`reliability-and-durability.md`](reliability-and-durability.md) (the gate taxonomy this record
  extends), [`cryptology-eprint-archive.md`](cryptology-eprint-archive.md) (§7.6 side-channel and
  embedded security — the KU Leuven and TU Graz dissertations in §5.7 are its long-form layer),
  [`hal.md`](hal.md) (TEL runs on HAL infrastructure), and
  [`landmark-papers.md`](landmark-papers.md) (of which §9 below is the thesis-shaped parallel).

> **The claim this record makes.** For a very large amount of real hardware and systems work, **the
> dissertation is the only complete writeup that exists.** The conference paper is 8–12 pages
> because the CFP said so. The dissertation behind it is 150–300 pages, and it is where the
> schematics, the board bring-up log, the measurement setup, the calibration procedure, the failed
> iterations and the negative results ended up — because a committee required them and no page
> limit forbade them. **This is frequently the single highest-value document in the entire
> literature on a given piece of hardware, and it is almost never indexed alongside the papers.**

---

## 1. Why the thesis, and not the paper

### 1.1 The page-limit argument, made concretely

Take the four cases this record verifies in §9 and compare the two artefacts.

| Work | The paper | The thesis | What only the thesis has |
|---|---|---|---|
| **RISC-V** | The ISA is specified in a sequence of manuals; the *design rationale* was never a conference paper at all | **`UCB/EECS-2016-1`**, Waterman, 2016 — a full PhD dissertation (§9) | The argument for *why* the ISA is shaped the way it is: the compressed-encoding tradeoffs, the rejected alternatives, the quantitative comparisons against ARM/x86/MIPS |
| **Semi-invasive attacks** | Scattered CHES/FDTC papers | **`UCAM-CL-TR-630`**, Skorobogatov, 2005, **144 pages** — a PhD dissertation issued as a Cambridge technical report, DOI `10.48456/tr-630` ([companion record §3.5](government-and-institutional-technical-reports.md)) | The decapsulation chemistry, the optical bench, the laser parameters, the per-chip results — i.e. everything needed to *reproduce* an optical fault injection |
| **Switching algebra** | Shannon's 1938 AIEE paper is ~19 pages | **Shannon's 1937 MIT master's thesis** (§9) | The worked relay-circuit designs and the full development of the correspondence between Boolean algebra and contact networks |
| **Sketchpad** | The 1963 AFIPS paper is a summary | **Sutherland's 1963 MIT PhD**, republished 2003 as **`UCAM-CL-TR-574`** (§9) | The constraint solver, the data structures, the display-file format, the light-pen tracking algorithm |

The pattern is not incidental. It is what the two document types are *for*. A conference paper
argues a contribution to a programme committee against a page budget. A dissertation demonstrates
competence to an examining committee, and the standard evidence of competence in an experimental
discipline is **method in enough detail that someone else could do it again.**

### 1.2 Three structural reasons this matters for hardware specifically

**One: hardware work has irreducible setup cost, and setup is what gets cut.** The measurement
chain — probe, fixture, trigger, deskew, calibration, environmental controls — is a page or two in
the paper and a chapter in the thesis. If you are trying to reproduce a side-channel result, a
radiation test, an EM measurement or a timing attack, the chapter is the document you need and the
paper is nearly useless.

**Two: negative results survive only in theses.** No venue publishes "we built the first three
revisions of this board and here is why they did not work". A committee, however, expects the
candidate to account for three years, and the failed spin is part of the account. For anyone
building the same thing, the failed spin is the most valuable page in the document.

**Three: a thesis is often the *only* artefact.** A great deal of instrumentation, FPGA
infrastructure, ASIC test chips and firmware toolchains was built by one student, described once,
and never written up for a venue at all. See §5 for the repositories where this material is
concentrated.

### 1.3 The counter-argument, stated honestly

Theses are not uniformly better than papers, and this record does not claim they are.

- They are **unrefereed by the field**. The gate is a committee of three-to-six people, some of
  whom are the supervisor. §7 works this through properly.
- They are **stale on arrival**. Chapters written in year two are already 18 months old at
  deposit, and the accompanying paper often carries later, better numbers.
- They are **long**, and length is not information density. A 250-page dissertation frequently
  contains 40 pages of literature review you do not need.
- They are frequently **embargoed** (§8), which is precisely the failure mode that hurts most: the
  thesis exists, the record is public, and the file is locked for three years.

The practical position this record takes: **read the paper to know what was claimed, and read the
thesis to know whether you can rebuild it.**

---

## 2. The discovery and aggregation layer — and its 2025–2026 collapse

This is the section where a reader expecting a healthy landscape gets a surprise. **Two of the
three thesis-specific global aggregators are, as of 2026-09-04, either permanently closed or
returning HTTP 503.** The generic open-access aggregators, which are *not* thesis-specific, are now
the working route.

### 2.1 Status table

All probes **2026-09-04**, Chrome-131 user agent unless noted.

| Service | Endpoint | Status | Measured | Verdict |
|---|---|---|---|---|
| **NDLTD** (organisation) | `https://ndltd.org/` | **200**, 135,318 B | — | Organisation alive [WEB] |
| **NDLTD Global ETD Search** | `https://search.ndltd.org/` | **503**, 505 B (nginx default) | last known **6,534,039** ETDs (Wayback 2025-05-16) | **Down** [WEB] |
| **NDLTD union catalogue OAI-PMH** | `https://union.ndltd.org/OAI-PMH/?verb=Identify` | **503**, 505 B | — | **Down** [API] |
| **OATD** | `https://oatd.org/` | **403**, 5,207–5,442 B (Cloudflare "Just a moment…") to **all five** UAs incl. `robots.txt` | **7,407,210** ETDs from "over 1100" institutions (Wayback 2025-03-04) | **Alive, bot-walled** [WEB] |
| **DART-Europe** | `https://www.dart-europe.org/` | **200** after redirect to `ucl.ac.uk` | — | **CLOSED PERMANENTLY 2025-02-03** [DOC] |
| **CORE** | `https://api.core.ac.uk/v3/search/works/` | **200** | **7,921,188** works with `documentType:"thesis"` of **329,911,927** total | **Working, no key needed** [API] |
| **BASE** | `https://www.base-search.net/Search/Results?…` | **200**, 7,846 B — Anubis interstitial `xess.min.css?cachebuster=v1.27.0+dirty` | — | **Proof-of-work walled** [WEB] |
| **OpenAIRE** | `https://api.openaire.eu/search/publications?instancetype=…` | **200** | **3,158,600** Doctoral thesis · **2,661,863** Master thesis · **2,525,725** Thesis | **Working** [API] |

### 2.2 NDLTD — the union catalogue is down

NDLTD (the **Networked Digital Library of Theses and Dissertations**, https://ndltd.org/) is the
international membership organisation for ETD practice: it runs the annual ETD Symposium, publishes
the *ETD Journal*, gives the Innovative ETD Awards, and — historically — operated the **Global ETD
Search**, the single largest thesis-specific union catalogue in the world.

**The organisation is healthy. The search is not.**

- `https://ndltd.org/` — HTTP 200, 135,318 B, a current WordPress site with board, committees,
  membership and symposium pages [WEB] (S1).
- `https://search.ndltd.org/` — **HTTP 503, a 505-byte stock nginx "503 Service Unavailable"
  page** on 2026-09-04 [WEB] (S2). `http://search.ndltd.org/` 301s to the HTTPS form, which then
  503s — i.e. the reverse proxy is up and the backend behind it is not.
- `https://union.ndltd.org/OAI-PMH/?verb=Identify` — **HTTP 503, the same 505-byte nginx page**
  [API] (S2). The OAI-PMH harvest endpoint is down with it.

**When it broke, from the Wayback CDX index** [WEB] (S3):

| Capture | Status |
|---|---|
| 2025-03-06, 2025-04-11, **2025-05-16** | **200** (2,254–2,372 B) |
| 2025-06-13 | (no status recorded) |
| **2025-08-07** onward — 2025-09, -10, -11, -12, 2026-01, -02, -03, -04, -06, -07, -08, **2026-09-01** | **301** (358–562 B) |

So Global ETD Search served normally until at least **2025-05-16** and has been redirect-then-fail
since **2025-08-07** — thirteen consecutive monthly captures. The `union.ndltd.org/OAI-PMH/` path
has its own last-good capture on **2025-04-20** (S3). **This is not a transient outage; it is a
service that has been unavailable for approximately thirteen months.**

**The last measured size of the collection**, read from NDLTD's own front page in the 2025-05-16
Wayback capture (S4):

> "Search the **6,534,039** electronic theses and dissertations contained in the NDLTD archive"

That figure is the best number this record can give for NDLTD, and it is **sixteen months stale**.
Anyone quoting a current NDLTD size is quoting something they did not measure.

**What NDLTD still gives you that nothing else does:** its
[*List of Resources for Finding ETDs*](https://ndltd.org/thesis-resources/find-etds/) — HTTP 200,
132,126 B [WEB] (S5) — is a maintained, country-by-country directory of national and regional ETD
services, and it is the map §3 of this record is built on. It is a WordPress page on a live site
and it is the single most useful surviving NDLTD asset. It is also, on the evidence of the search
outage, a good `web.archive.org/save/` candidate under `AGENTS.md` rule 9.

### 2.3 OATD — alive, and unreadable by a robot

**OATD (Open Access Theses and Dissertations, https://oatd.org/)** is a hand-built ETD-specific
search engine that harvests institutional repositories directly. It is the service most librarians
recommend first, and it is **completely inaccessible to scripted retrieval on 2026-09-04.**

Every path tried, including `robots.txt`, returned **HTTP 403 with a Cloudflare
`<title>Just a moment...</title>` interstitial** [WEB] (S6):

| User agent | Status | Body |
|---|---|---|
| Chrome 131 | 403 | 5,442 B |
| `WhatsApp/2.23.20.0` | 403 | 5,228 B |
| ClaudeBot | 403 | 5,442 B |
| `curl/8.5.0` | 403 | 5,207 B |
| Googlebot | 403 | 5,292 B |
| Chrome 131 → `/robots.txt` | 403 | 5,493 B |
| Chrome 131 → `/oatd/search?q=…` | 403 | 5,821 B |

This is the **~5.2–5.9 kB Cloudflare managed-challenge fingerprint** already tabulated in
[`retrieval-notes.md` §1](retrieval-notes.md). Under this survey's own rule that means **blocked,
not broken** — OATD is running and refusing robots, and a human browser will get in.

**OATD's own explanation, from its front page** [DOC] (S7) — it is candid about why:

> "October 3, 2022. OATD is dealing with a number of misbehaved crawlers and robots, and is
> currently taking some steps to minimize their impact on the system. This may require you to click
> through some security screen. Our apologies for any inconvenience."

**The count, from OATD's own counter** [WEB, via Wayback] (S7):

| Date of capture | OATD's stated index size |
|---|---|
| 2024-04-01 | **7,421,247** |
| 2025-01-01 | **7,206,043** |
| **2025-03-04** (most recent readable capture) | **7,407,210** |

Front-page wording at all three: *"Metadata (information about the theses) comes from over 1100
colleges, universities, and research institutions. OATD currently indexes N theses and
dissertations."*

**Note the non-monotonicity.** The counter went 7,421,247 → 7,206,043 → 7,407,210, a ~215,000-record
dip and partial recovery across eleven months. That is what re-harvesting an OAI-PMH federation
looks like — a source repository that fails to answer during a harvest cycle drops out of the index
and comes back later. **Treat any single OATD figure as ±3%, and never diff two of them to infer
growth.** [INF]

**Current OATD size: [NOT-VERIFIED].** What was tried: five user agents live (all 403), `robots.txt`
(403), a search URL with full browser `Accept`/`Accept-Language` headers (403), and Wayback replay
of the most recent captures (the last 200 in the CDX index is **2025-03-04**; every capture from
2025-06-20 onward is itself a 403 of the Cloudflare page). No OAI-PMH, REST or JSON interface is
advertised.

### 2.4 DART-Europe — closed, permanently, on 2025-02-03

**This is a second durability casualty and it is unambiguous.** `https://www.dart-europe.org/`
returns HTTP 200 — but only after redirecting to a UCL Library Services page titled *"The
DART-Europe e-theses portal has closed down"* [DOC] (S8). UCL's own words, verbatim:

> "Please note that the DART-Europe e-theses portal was closed down permanently on **Monday 03
> February 2025**.
>
> We would like to thank all our partners and contributors over many years. Electronic research
> theses can be found in several general open access aggregators, below, and in institutions'
> individual open access repositories. **BASE · CORE · NDLTD (Global ETD Search and Find ETDs)**
>
> The DART-Europe e-theses portal was a searchable database of open access electronic research
> theses held in European repositories, with links to full text copies."

Two things to draw out.

**First, the successor advice is already partly wrong.** UCL points readers at three services.
Measured on 2026-09-04: **BASE is behind an Anubis proof-of-work wall**, **NDLTD Global ETD Search
returns 503**, and only **CORE** actually answers. A closure notice written in February 2025 has
aged badly in nineteen months. This is exactly the pattern
[`closed-and-defunct-servers.md` §2.4](closed-and-defunct-servers.md) documents for preprint
servers — *the pointer outlives the thing it points at, and nobody updates it* — and it is worth
noting that this is a **university library**, i.e. the institution most likely to maintain such a
notice, and it still went stale.

**Second, the count is unrecoverable in the ordinary way.** DART-Europe historically advertised a
figure in the low millions of theses from several hundred European universities in tens of
countries. **This record will not quote one**, because the portal is gone and no primary
measurement was obtainable on the probe date. **DART-Europe record count and participating-country
count: [NOT-VERIFIED].** What was tried: the live site (redirects to the closure notice, which
contains no figures), and the closure notice itself. A Wayback replay of the pre-closure front page
was not attempted within this pass's Internet Archive budget — it is the obvious next probe and is
flagged in §13.

### 2.5 CORE — the aggregator that actually works

Covered as a *paper* source in
[`open-access-full-text-sources.md`](open-access-full-text-sources.md). The ETD angle only, here.

**CORE's v3 API answers unauthenticated `curl` and has a `documentType` field that includes
`thesis`** [API] (S9), measured 2026-09-04:

```bash
# NOTE the trailing slash on /works/ — see the trap below
curl -s -G "https://api.core.ac.uk/v3/search/works/" \
     --data-urlencode 'q=documentType:"thesis"' --data-urlencode 'limit=1'
```

| Query | `totalHits` |
|---|---|
| `documentType:"thesis"` | **7,921,188** |
| `*` (everything CORE holds) | **329,911,927** |

So **theses are ~2.4% of CORE by record count**, and CORE's thesis holding is *larger than the last
measured NDLTD union catalogue* (6.53 M) and comparable to OATD (7.41 M). Given that NDLTD is down
and OATD is bot-walled, **CORE is currently the only large thesis index this survey could query
programmatically.**

**New API trap, worth propagating to [`retrieval-notes.md`](retrieval-notes.md):** requesting
`https://api.core.ac.uk/v3/search/works` **without** the trailing slash returns **HTTP 200 with a
Cloudflare `cdn-cgi/content` HTML redirect page**, not JSON — a `<meta http-equiv="refresh">`
document pointing at the slashed URL. A JSON parser sees a parse error; a naive harvester that
checks only the status code sees success. `.../works/` **with** the slash returns clean JSON. [API]

CORE also exposes full text (it stores the PDFs it harvests), which for theses is the difference
between a citation and a document.

### 2.6 BASE — walled, and therefore unmeasured

BASE (Bielefeld Academic Search Engine) indexes theses well — its advanced search has a document-type
facet for theses, and NDLTD's own directory describes it as a *"Portal to 70 million documents in
3000 repositories. Use Advanced Search to restrict queries to theses and dissertations."* [DOC]
(S5).

**Measured 2026-09-04:** `https://www.base-search.net/Search/Results?lookfor=riscv&type=all` →
**HTTP 200, 7,846 bytes, `<title>Making sure you're not a bot!</title>`, stylesheet
`/.within.website/x/xess/xess.min.css?cachebuster=v1.27.0+dirty`** [WEB] (S10). That is the
**Anubis proof-of-work interstitial**, and [`retrieval-notes.md` §3](retrieval-notes.md) already
records the decisive finding about it: **no user agent defeats it.** It is a JavaScript
proof-of-work, not a UA filter.

Consistent with the sibling record, **BASE's thesis count is [NOT-VERIFIED]** and its overall size
remains unverified across this whole survey. The 70-million figure above is NDLTD quoting BASE, not
a measurement — label it [DOC], treat it as indicative, and note that BASE publicly claims a
substantially larger figure than that on its own front page, which we could not read.

**The general rule from `retrieval-notes.md` §3 applies and is worth restating for ETDs
specifically: when a thesis portal blocks you, go looking for OAI-PMH before concluding it is
down.** Six of seven Anubis-walled scholarly hosts in the previous pass had an open machine
interface behind the wall. For BASE specifically, no such interface was found.

### 2.7 OpenAIRE — the best type-faceted numbers available

OpenAIRE's legacy search API answers plain `curl`, needs no key, and has an `instancetype`
parameter that distinguishes doctoral from master's work [API] (S11), measured 2026-09-04:

```bash
curl -s "https://api.openaire.eu/search/publications?instancetype=Doctoral+thesis&size=1&format=json"
# → response.header.total.$
```

| `instancetype` | Records |
|---|---|
| **Doctoral thesis** | **3,158,600** |
| **Master thesis** | **2,661,863** |
| **Thesis** (unspecified level) | **2,525,725** |
| *sum of the three* | *8,346,188* |

**Do not sum those in a citation.** OpenAIRE deduplicates across sources but the three type buckets
are separately assigned by contributing repositories, and a repository that labels everything
`Thesis` contributes to the third bucket regardless of level. The sum is an upper bound. [INF]

**API trap:** `?type=doctoralThesis` — the parameter name a reader would guess — returns **HTTP 400
with a helpful exception body enumerating every supported parameter**. That is unusually good API
behaviour and worth recording as a *positive* control: OpenAIRE tells you what it accepts. The
supported list includes `instancetype`, `country`, `fos`, `openaireProviderID`, `peerReviewed`,
`OA`, `green`, `openAccessColor` and `originalId`. [API]

### 2.8 Google Scholar — brief and honest

NDLTD's own directory entry for Google Scholar reads: *"Harvests theses and dissertations from
virtually all registered open-access repositories."* [DOC] (S5)

That is approximately true and it is why Google Scholar is, in practice, how most people find a
thesis. **This record cannot verify anything about it.** Google Scholar has no API, forbids
automated querying in its terms, blocks scripted access, and publishes no coverage statistics. Its
thesis coverage, its recall, and its handling of embargoed records are all **[NOT-VERIFIED]** and
will remain so — not because we did not try but because trying properly would mean circumventing an
explicit access control, which `AGENTS.md` rule 7 forbids.

**Two practical cautions that do not require measurement:**

- Google Scholar's **"All N versions"** cluster is where a thesis usually surfaces next to its
  papers. It is the single most useful UI affordance for this record's whole purpose, and it is
  also the thing that most often silently merges a thesis with a *different* document by the same
  author.
- Scholar indexes the **repository landing page**, so an embargoed thesis appears as a normal hit
  with a normal-looking link. §8 covers how to tell.

---

## 3. The EThOS catastrophe — and its 2026 resolution

This is the most instructive durability case study in this entire directory, because unlike the
preprint-server failures in [`closed-and-defunct-servers.md`](closed-and-defunct-servers.md) — which
were nearly all *front-door* failures with the corpus intact behind them — **EThOS was a genuine
service destruction, and the recovery was partial, structural and permanent.** The service that came
back is not the service that went away.

### 3.1 What EThOS was

EThOS (**E-Theses Online Service**), `https://ethos.bl.uk/`, run by the British Library, was the UK's
national doctoral thesis service. Two functions, and it is essential to keep them apart:

1. **A national union catalogue** of UK doctoral theses — metadata for every PhD awarded by a UK
   higher-education institution, back to the eighteenth century.
2. **A digitisation and supply service.** If a thesis existed only on paper, you could request a
   scan through EThOS; the British Library digitised it, hosted the PDF, and delivered it. For a
   large fraction of pre-2000 UK doctoral work **EThOS was the only digital copy in existence.**

Function (1) survived. **Function (2) did not.**

### 3.2 The attack

The British Library's own statement, `https://www.bl.uk/cyber-incident/` → 302 →
`https://www.bl.uk/about/cyber-attack`, HTTP 200, 133,713 B, retrieved 2026-09-04 [DOC] (S12):

> "In **October 2023** the British Library experienced a significant cyber-attack that disrupted many
> of our services. We are working to restore full functionality."
>
> "In **November 2023** the attackers released some of our data onto the dark web including some
> personal user information."
>
> "The attack caused **multiple capabilities to be destroyed simultaneously** which has required a
> **rebuild of our entire technology infrastructure**, a process of considerable complexity."
>
> "In **March 2024** we published a paper about the attack and its impact … Its goal is to share our
> understanding of what happened and to help others learn from our experience."

Note the phrase *"destroyed simultaneously"* and *"rebuild of our entire technology infrastructure"*.
This was not a defacement or a data breach with systems intact. This is the reason EThOS took
**roughly two and a half years** to return.

**The outage, measured from the Wayback CDX index for `ethos.bl.uk`** [WEB] (S13):

| Period | CDX status |
|---|---|
| 2023-01 → **2023-10-08** | 301 (normal — the apex redirected to the service path) |
| **2023-11, 2023-12, 2024-01, 2024-02** | **no captures at all** |
| 2024-03-21 → 2026-02 | 307 / 308 (302–640 B) — a holding redirect, monthly, unchanging for ~24 months |
| 2026-03-17, 2026-04-13 | 307 (594 B, 598 B) |
| 2026-05-13, 2026-06-21, 2026-07-01 | 302 (589, 549, 553 B) |
| 2026-08-24 | **403, 4,721 B** |
| 2026-09-03 | 301, 1,165 B |

The **four-month capture gap from November 2023 to February 2024** is the attack itself: the host
was not answering at all. Everything from March 2024 to early 2026 is a stub.

### 3.3 EThOS in 2026 — it is back, and it is a different thing

**Verified live, 2026-09-04:** `https://ethos.bl.uk/` → **HTTP 200, 62,214 bytes** [WEB] (S14).

The platform is **Hyku** (the multi-tenant Samvera/Hyrax distribution — the page title on error
routes is literally `Hyku knap sack`), and the footer states: **"Platform provided by CoSector,
University of London."** The British Library did not rebuild it in house.

**The British Library's own statement of what changed**, from `https://ethos.bl.uk/about`, HTTP 200,
57,645 B [DOC] (S15) — this is the single most important quotation in this record:

> "EThOS (e-Theses Online Service) is an open access **discovery platform** for UK doctoral theses,
> managed by the British Library. It aims to provide a national aggregated record of all doctoral
> theses awarded by UK Higher Education institutions.
>
> Following restoration work after a cyber-attack on the British Library in 2023, this platform is a
> **metadata-only discovery service**, which we will continue to update with doctorates awarded since
> October 2023 as part of our rolling programme of updates."

And from the FAQ, `https://ethos.bl.uk/FAQs?locale=en`, HTTP 200, 84,307 B [DOC] (S16):

> "**Why has EThOS been unavailable for a period?** EThOS was badly damaged by a cyber-attack on the
> British Library in 2023 and has been unavailable since. **A new EThOS platform needed to be
> procured, via a public tender process.** The metadata records of over 650,000 theses from UK
> universities have been loaded onto the new platform. This includes around **14,000 additional
> theses** that have been added to the service since the cyber-attack."
>
> "**What is available on EThOS?** The new platform **does not hold full-text theses files to
> download directly** but, where individual theses are available on a university repository, a link
> is provided to access the file."
>
> "It includes metadata records of over 650,000 theses from UK universities from the **1700s**
> onwards. … **Over 400,000 theses are openly available for download from university repositories.**"
>
> "**Can I request a thesis for digitisation?** You can request digitisation of some print-only
> theses **by emailing the relevant university library**. At this stage, universities can still
> request digitisation of theses and the files will be **returned to the university for upload to
> their own repository**."
>
> "**Later in 2026, we will begin the next phase of work** to assess how the restored version of
> EThOS is being received by our users."

**Read those together and the structural change is clear.** The British Library has exited the
business of *holding* UK theses. EThOS is now a pure discovery-and-referral layer over
**institutional repositories**, and the digitisation service has been devolved to individual
university libraries, which now host the resulting files themselves. **The answer to "where are UK
theses now discoverable" is: EThOS for the index, and the awarding university's own repository for
the document.** There is no replacement national full-text store, and none is proposed.

### 3.4 The size of the restored service — measured, not quoted

The British Library says "over 650,000". **We measured it**, and the route is worth documenting
because it is the only machine-readable interface the new platform exposes.

Hyku publishes a **ResourceSync** capability list. `https://ethos.bl.uk/capabilitylist?locale=en` →
HTTP 200, 457 B [API] (S17):

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:rs="http://www.openarchives.org/rs/terms/">
  <rs:ln rel="up" href="https://ethos.bl.uk/.well-known/resourcesync"/>
  <rs:md capability="capabilitylist"/>
  <url><loc>https://ethos.bl.uk/resourcelist</loc><rs:md capability="resourcelist"/></url>
  <url><loc>https://ethos.bl.uk/changelist</loc><rs:md capability="changelist"/></url>
</urlset>
```

`https://ethos.bl.uk/resourcelist` → **HTTP 200, 88,402,587 bytes**, `capability="resourcelist"`,
`at="2026-09-06T16:32:22Z"` [API] (S17). Counted:

| Measure | Value |
|---|---|
| **`<loc>` entries, all `concern/thesis_or_dissertations/`** | **654,832** |
| Lowest record id | 232,781 |
| Highest record id | 906,226 |
| `lastmod` 2026-03 | 47,452 |
| **`lastmod` 2026-04** | **546,764** |
| `lastmod` 2026-05 | 4,539 |
| `lastmod` 2026-06 | 24,773 |
| `lastmod` 2026-07 | 149 |
| `lastmod` 2026-08 | 29,556 |
| `lastmod` 2026-09 (to the 6th) | 1,599 |

**654,832 records.** That is a hard number from the operator's own machine interface and it confirms
"over 650,000" precisely.

**The `lastmod` histogram is the reload signature.** 83.5% of all records were last modified in
**April 2026**, with a further 7.2% in March 2026. That is a bulk ingest, not organic accrual — the
metadata was loaded onto the new platform in **March–April 2026**, and the trickle since (May
onward, ~60,000 records) is the rolling update programme the FAQ describes. [INF, from API data]

Combined with the Wayback capture series (§3.2), which shows the holding redirect changing shape in
March–April 2026 and settling to a 302 by May, the **public relaunch of EThOS falls in roughly
2026-04 to 2026-05.** [INF] No press announcement was located within this pass — **the exact
relaunch date is [NOT-VERIFIED].**

### 3.5 Record shape, identifiers, and the legacy-URL result

A live record, `https://ethos.bl.uk/concern/thesis_or_dissertations/906226` → HTTP 200, 69,494 B
[WEB] (S18). Fields present: **Author · Qualification Name · University · Date Awarded · Awarding
Institution · Language · Subject Discipline · Access Thesis · EThOS ID**.

- **The identifier is `uk.bl.ethos.<n>`** and the numeric part is the URL path component. So
  `uk.bl.ethos.906226` ⇒ `https://ethos.bl.uk/concern/thesis_or_dissertations/906226`. There is **no
  DOI** on EThOS records.
- Where the university repository holds a copy, the record carries an **"Access thesis from
  university"** button. Where it does not, the record says so explicitly — the probed record read:
  *"EThOS does not have a link to a university copy of this thesis. If you would like to view this
  thesis, we recommend that you contact Royal Veterinary College."*
- `Subject Discipline` was **"Not yet classified"** on the record probed. Subject classification is
  visibly incomplete on the reloaded corpus. [WEB]

**The finding that matters most for anyone with old citations: the legacy EThOS URL form still
resolves.**

| Probe | Result |
|---|---|
| `https://ethos.bl.uk/OrderDetails.do?uin=uk.bl.ethos.906226` | **HTTP 200 → redirects to `/concern/thesis_or_dissertations/906226`**, 69,494 B |
| `https://ethos.bl.uk/concern/thesis_or_dissertations/99999999` *(negative control)* | **HTTP 404, 1,676 B** (`Hyku knap sack` error page) — clean |
| `https://ethos.bl.uk/OrderDetails.do?uin=uk.bl.ethos.99999999` *(negative control)* | ⚠ **HTTP 200, 62,214 B — silently lands on the home page** |

**Two consequences.**

*Good news:* the `OrderDetails.do?uin=…` URLs embedded in a decade and a half of bibliographies,
repository records and the EThOS CSV dataset itself **still work**. Someone deliberately built a
compatibility shim into the new platform. Given how rarely that happens — see
[`closed-and-defunct-servers.md` §2.3](closed-and-defunct-servers.md) on platform migrations
breaking URL grammar — it deserves naming as good practice.

*Bad news, and it is a new probing trap:* **the legacy route has no negative signal.** A bogus
`uin` returns HTTP 200 with the 62,214-byte home page, byte-identical to a successful load of `/`.
A link-checker walking a bibliography of `OrderDetails.do` URLs will report **100% success**
regardless of whether the records exist. **Validate against the modern `/concern/…` path, which
404s honestly.** [WEB]

### 3.6 Did the EThOS data survive? Yes — and it is downloadable right now

This was the open question, and the answer is unambiguously yes.

The British Library published the **complete EThOS bibliographic metadata as a CC-BY dataset**,
repeatedly, on its own research repository. Queried via the **DataCite API** on prefix `10.23636`
[API] (S19):

| DOI | Year | Title | Type |
|---|---|---|---|
| **`10.23636/rcm4-zk44`** | **2023** | **UK Doctoral Thesis Metadata from EThOS** | Dataset — **the final release** |
| `10.23636/vtpx-we51` | 2023 | UK Doctoral Thesis Metadata from EThOS | Dataset — superseded by the above |
| `10.23636/j278-4b96` | 2022 | UK Doctoral Thesis Metadata from EThOS | Dataset |
| `10.23636/kvwc-ty06` | 2022 | UK Doctoral Thesis Metadata from EThOS | Dataset |
| `10.23636/ybpt-nh33` | 2021 | UK Doctoral Thesis Metadata from EThOS | Dataset |
| `10.23636/1344` | 2021 | UK Doctoral Thesis Metadata from EThOS | Dataset |
| `10.23636/1188` | 2020 | UK Doctoral Thesis Metadata from EThOS | Dataset |
| `10.23636/1156` | 2020 | EThOS metadata files augmented with identifiers | Dataset |
| `10.23636/1137` | 2019 | UK Doctoral Thesis Metadata from EThOS | Dataset |
| `10.23636/9h0m-3974` | 2023 | Surfacing the impact of international doctoral research: Working with the EThOS collection | Report |
| `10.23636/1181` | 2020 | Introduction to EThOS: the British Library database of UK theses | InteractiveResource |
| `10.23636/1162` | 2014 | Text and Data Mining in EThOS | Text |

**DataCite metadata for the final release `10.23636/rcm4-zk44`** [API] (S19):

- Publisher: **British Library** · Issued **2023** · DataCite record **created 2023-11-27T17:07:22Z**
- Licence: **CC-BY 4.0** (`rightsIdentifier: cc-by-4.0`)
- Abstract, verbatim: *"The data in this collection comprises the bibliographic metadata for all UK
  doctoral theses listed in EThOS, the UK's national thesis service. **We estimate the data covers
  around 98% of all PhDs ever awarded by UK Higher Education institutions, dating back to 1787.**
  Thesis metadata from every PhD-awarding university in the UK is included."*

**The DataCite record was created on 2023-11-27 — a month after the attack.** The dataset release
was pushed out during the incident.

**We verified the file is actually retrievable.** The BL Research Repository has itself migrated
since (from Hyrax to **DSpace-CRIS**, with the old `bl.iro.bl.uk/concern/datasets/<uuid>` URLs
302-redirecting to `bl.iro.bl.uk/entities/product/<new-uuid>`). Using the DSpace 7 REST API
[API] (S20):

```bash
# item → bundles → bitstreams → content
curl -s "https://bl.iro.bl.uk/server/api/core/items/ef18a65d-a839-428b-abbc-2da178007e4e"
curl -s "https://bl.iro.bl.uk/server/api/core/items/ef18a65d-a839-428b-abbc-2da178007e4e/bundles"
curl -sL -H 'Range: bytes=0-3000' \
  "https://bl.iro.bl.uk/server/api/core/bitstreams/a10353df-67a5-4d47-9d33-4c764f605eb5/content"
```

| Property | Value |
|---|---|
| Item handle | **`britishlibrary-iro/19931`** |
| `dc.identifier.doi` | `10.23636/rcm4-zk44` |
| Bundles | `ORIGINAL`, `TEXT`, `TEXT` |
| Bitstream | **`EThOS_CSV_202310.csv`** |
| **Size** | **709,733,446 bytes (≈709.7 MB)** |
| Range fetch | **HTTP 206**, `content-type: text/csv`, `content-range: bytes 0-3000/709733446` |
| Delivery | 302 to a signed `cf002.cdn.4science.cloud` CloudFront URL (`Expires`/`Signature`/`Key-Pair-Id`) |

**The filename is the finding.** `EThOS_CSV_202310` — **October 2023**. The final EThOS metadata
snapshot is dated to the month of the attack, and it is a complete, open, 709 MB CSV that anyone can
download today.

**And the columns are exactly what this record needs** (first 3,001 bytes, verbatim header):

```
Title,DOI,Author,Author ISNI,ORCID,Institution,Institution ISNI,Date,Qualification,
Abstract,Subject Discipline,Supervisor(s),Funder(s),EThOS URL,IR URL
```

Note **`Supervisor(s)`** and **`IR URL`**. This is a 709 MB, CC-BY, offline-queryable table of
~650,000 UK doctorates with **author, supervisor, institution, abstract, funder, and a direct link
to the institutional-repository copy.** For the advisor-lineage technique in §5.8 it is the single
best dataset in this entire survey, and it works with no network access to any thesis portal at all.

A verbatim sample row, showing the `EThOS URL` column uses the legacy `OrderDetails.do` form
(§3.5 — which still resolves):

```
Computation and measurement of turbulent flow through idealized turbine blade passages, ,
"Loizou, Panos A.",https://isni.org/isni/0000000136122593, ,University of Manchester,
https://isni.org/isni/0000000121662407,1989,Thesis (Ph.D.), ,Physical Sciences, , ,
https://ethos.bl.uk/OrderDetails.do?uin=uk.bl.ethos.232781,
```

### 3.7 What was actually lost

Being precise, because the temptation is to over- or under-state it.

| Asset | Fate |
|---|---|
| Bibliographic metadata for ~650,000 UK doctorates | **Survived completely.** On the new platform (654,832 records) *and* as an open 709 MB CC-BY CSV |
| Discovery service | **Restored**, on new infrastructure, ~2.5 years later |
| Legacy `OrderDetails.do` URLs in the literature | **Survived** — compatibility shim in place |
| **The British Library's own digitised full-text thesis files** | **Not restored.** EThOS "does not hold full-text theses files to download directly" [DOC] |
| **The national digitisation-on-demand service** | **Devolved.** Requests now go to the awarding university library; files go to *their* repository |
| Personal user account data | Partly exfiltrated and released on the dark web, Nov 2023 [DOC] |
| The ~2.5 years of UK theses awarded during the outage | Partially caught up — "around 14,000 additional theses" loaded [DOC] |

**The irreplaceable loss is the pre-digital tail.** For a UK thesis from, say, 1962 that was
digitised only because someone once paid EThOS to scan it, the British Library's copy is no longer
served and the awarding university may never have had one. §3.3's FAQ answer is explicit that such
records now show "only the metadata record is available … available as a paper copy in a university
library". **[NOT-VERIFIED]:** how many previously-digitised files fall into this category, and
whether the BL retains them internally. No public statement quantifying this was located.

### 3.8 How this parallels — and departs from — [`closed-and-defunct-servers.md`](closed-and-defunct-servers.md)

That record's headline finding is: **"Preprint servers do not lose data. They lose front doors."**
Seventeen of eighteen dead servers still served their corpus.

**EThOS is the counterexample that sharpens the rule.** Map it onto that record's failure taxonomy:

| Failure mode from `closed-and-defunct-servers.md` §2 | EThOS |
|---|---|
| Publisher strategy change | No |
| Founder retirement / single maintainer | No |
| Platform migration breaking URL grammar | **Inverted** — a migration that *preserved* URL grammar |
| Domain lapse to a squatter | No — `ethos.bl.uk` was held throughout |
| TLS as an abandonment signal | **Useless here.** The domain kept valid certs and served monthly 307s for two years while the service was destroyed |
| **Catastrophic infrastructure destruction** | **Yes — a mode that record did not observe at all** |

And the durability lesson generalises cleanly to this survey's standing advice:

1. **The DOI'd, CC-BY bulk dataset is what saved EThOS**, not the website. `10.23636/rcm4-zk44`
   resolved and delivered a 709 MB file throughout the outage. This is precisely
   [`reliability-and-durability.md` §6](reliability-and-durability.md)'s "cite the DOI, and archive a
   copy yourself", validated by a real disaster.
2. **A live hostname with a valid certificate answering HTTP 307 every month for 24 months looked,
   to every automated checker, exactly like a healthy site.** Reinforces
   [`retrieval-notes.md` §8](retrieval-notes.md): TLS and status codes are not liveness.
3. **Metadata is cheap to preserve and full text is not.** The British Library restored the part
   that fit in a CSV and permanently devolved the part that did not. Expect this asymmetry
   everywhere.

---

## 4. National and regional ETD systems

The pattern below is consistent enough to state up front: **national thesis portals are more fragile
than institutional repositories, and the good ones are the ones with an API.** Three of the fifteen
systems probed here are dead or discontinued; four more are alive but unreadable by a robot.

### 4.1 Status table

All probes **2026-09-04**. "Chrome 131" = the rung-2 agent from
[`AGENTS.md`](../../AGENTS.md). `000` = TCP/TLS failure, not an HTTP status.

| System | Country/region | Endpoint probed | Status | Measured | Verdict |
|---|---|---|---|---|---|
| **theses.fr** | France | `theses.fr/api/v1/theses/recherche/?q=*&nombre=1` | **200** | **564,318** theses · **918,602** persons | **Best API in this table** [API] |
| **TEL** | France | `api.archives-ouvertes.fr/search/tel/` | **200** | **180,693** = 171,839 `THESE` + 8,854 `HDR` | Works; HAL infrastructure [API] |
| TEL (web) | France | `theses.hal.science/` | 200, 12,607 B | — | **Anubis** `xess.css?cachebuster=devel` [WEB] |
| **DiVA** | Sweden / Nordic | `diva-portal.org/dice/oai?verb=Identify` | **200** | **800,381** records (all types) | OAI-PMH open [API] |
| **DNB** | Germany | `services.dnb.de/oai/repository?verb=Identify` | **200**, 779 B | `earliestDatestamp` **1945-01-01** | OAI-PMH open [API] |
| DNB (web) | Germany | `portal.dnb.de/opac.htm` | 200, 4,475 B | — | **Anubis** `xess.min.css?cachebuster=1.25.0` [WEB] |
| **TDX / TDR** | Catalonia / Spain | `tdx.cat/` · `/oai/request` · `/handle/10803/1234` | **403** · 5,658 / 5,769 / 5,730 B | — | **Cloudflare, all paths.** Handle prefix **10803** [WEB] |
| **RCAAP** | Portugal | `rcaap.pt/` · `/OAIHandler?verb=Identify` | 200, 4,511 B | — | **Anubis, incl. OAI** `v1.26.0-pre2` [WEB] |
| **Trove** | Australia | `trove.nla.gov.au/` | 200, 7,745 B | — | **Anubis** `v1.26.2` [WEB] |
| **Shodhganga** | India | `shodhganga.inflibnet.ac.in/` | **200**, 515,934 B (13–21 s; 1 of 4 attempts timed out) | **697,675** full-text theses · 21,723 synopses · **908** contributing universities | Live, slow [WEB] |
| **CiNii Dissertations** | Japan | `cir.nii.ac.jp/opensearch/dissertations?format=json&from=1900` | **200** | **775,786** dissertations | Works; folded into CiNii Research [API] |
| **RISS** | Korea | `riss.kr/index.do` | **200**, 390,685 B | count not extracted | Live [WEB] |
| **CAPES Catálogo de Teses** | Brazil | `catalogodeteses.capes.gov.br/` | **000** | — | **Unreachable** (IPv4 *and* IPv6) [WEB] |
| **BDTD** (IBICT) | Brazil | `bdtd.ibict.br/vufind/` | 200, 1,697 B | — | Challenge page *"Verificando conexão \| Oasisbr"* [WEB] |
| **NARCIS** | Netherlands | `narcis.nl/` → `dans.knaw.nl/nl/data-diensten/narcis/` | 200 (Anubis at target) | — | **SERVICE ENDED 2023-07-03** [DOC] |
| **Cybertesis** | Latin America | `cybertesis.net/` (http) | 200 | — | **DOMAIN PARKED / MONETISED** [WEB] |
| **Theses Canada** | Canada | `bac-lac.gc.ca/…/theses-canada.aspx` · `library-archives.canada.ca/…` · search | **000** · **302 → canada.ca** · **403** 5,775 B | — | Old URLs dead; search Cloudflare-walled [WEB] |
| **TESEO** | Spain | `educacion.gob.es/teseo/…` → `aplicaciones.ciencia.gob.es/teseo` | **302 → 000** | — | Migrated; new host unreachable [WEB] |
| **Tez Merkezi** | Turkey | `tez.yok.gov.tr/UlusalTezMerkezi/giris.jsp` | **200**, 33,811 B | count not extracted | Live [WEB] |
| **CNKI** | China | `cnki.net/` → `oversea.cnki.net/index/` | **200**, 50,542 B | — | Live, **paywalled** [WEB] |
| **Wanfang** | China | `wanfangdata.com.cn/` | **200**, 216,413 B | — | Live, **paywalled** [WEB] |

**The single most striking pattern in that table is Anubis.** Four national thesis portals —
`theses.hal.science`, `portal.dnb.de`, `www.rcaap.pt`, `trove.nla.gov.au` — plus `base-search.net`
are now behind **Anubis proof-of-work interstitials**, at four *different* versions (`devel`,
`1.25.0`, `v1.26.0-pre2`, `v1.26.2`, `v1.27.0+dirty`). [`retrieval-notes.md` §3](retrieval-notes.md)
recorded Anubis on seven scholarly hosts in the previous pass; **it has since spread to the national
ETD layer.** Per that record's decisive finding, **no user agent defeats it** — and this pass
confirms that on `www.rcaap.pt`, where the **OAI-PMH endpoint itself is behind the wall**, breaking
the usual "look for OAI-PMH" escape hatch. RCAAP is the first host in this survey where that rule
failed.

### 4.2 France — theses.fr and TEL, and why there are two

France is the only country in this table with **two** national thesis services, and the split is
worth understanding because it is not redundancy.

**`theses.fr`** (ABES — the Agence bibliographique de l'enseignement supérieur) is the **registry**:
the authoritative record of every French doctorate, including theses *in preparation*. Its API is
the best-documented and most generous encountered anywhere in this record [API] (S21):

```bash
curl -s "https://theses.fr/api/v1/theses/recherche/?q=*&nombre=1"     # → totalHits 564318
curl -s "https://theses.fr/api/v1/personnes/recherche/?q=*&nombre=1"  # → totalHits 918602
curl -s "https://theses.fr/api/v1/theses/these/2016PA066033"          # → one record by NNT
```

| Measure | Value |
|---|---|
| `theses` `totalHits` | **564,318** |
| `personnes` `totalHits` | **918,602** |
| `q=RISC-V` | **102** |

- **The identifier is the NNT** (*Numéro National de Thèse*), e.g. `2016PA066033` — year, then an
  establishment code, then a sequence. It is stable and it is what French bibliographies cite.
- **theses.fr now mints DOIs.** The record for `2016PA066033` carries
  `"doi":"10.70675/ff0868d0z67ecz4e1bzb948zaa766df489f9"` [API]. Prefix **`10.70675`**. This is new
  and it materially improves French thesis citability — most national systems in this table mint
  nothing.
- **The `personnes` endpoint is the advisor-lineage tool.** A person record carries a `roles` object
  counting the person's appearances as *Président / Présidente du jury*, *Examinateur /
  Examinatrice*, *Rapporteur*, and (in the thesis records) `directeurs`. **You can walk a French
  supervisor's entire student list from a public API with no key.** Nothing else in this record
  offers that. See §5.8 and §11.
- **API trap:** `GET /api/v1/theses/these/<bogus-NNT>` returns **HTTP 200 with a zero-byte body** —
  not a 404. Verified with `9999ZZZZ9999`. A harvester checking status codes sees success; a JSON
  parser gets an EOF error. **Test for a non-empty body.** [API]

**TEL** (*thèses-en-ligne*, `https://theses.hal.science/`) is the **full-text archive**, and it is
built on HAL — see [`hal.md`](hal.md), which records that CCSD attributes the year **2001** to TEL
specifically (and 2002 to HAL itself), correcting Wikipedia. TEL is therefore queryable through
HAL's Solr API with the `tel` portal path [API] (S22):

```bash
curl -s "https://api.archives-ouvertes.fr/search/tel/?q=*:*&rows=0&wt=json"
```

| Facet | Count |
|---|---|
| **Total** | **180,693** |
| `docType_s:THESE` | **171,839** |
| `docType_s:HDR` (*habilitation à diriger des recherches*) | **8,854** |

**The HDR bucket is a French-specific bonus.** An *habilitation* is a senior researcher's synthesis
of a decade of work written to qualify them to supervise doctorates. For a reader trying to
understand a French lab's overall programme, an HDR is frequently a better document than any
individual paper — it is a self-written, referenced survey by the person who ran the group. 8,854 of
them are free.

**TEL by subject** [API] (S22) — using `domainAllCode_s`, which is the correct field
([README §6](README.md#6-probing-traps): `domain_s` silently returns zero):

| Code | Subject | Theses |
|---|---|---|
| `spi.other` | Engineering sciences, other | **7,370** |
| `info.info-mo` | Modelling and simulation | **3,408** |
| `chim.mate` | Materials chemistry | 3,683 |
| `spi` | Engineering sciences (top level) | 3,673 |
| `info.info-oh` | Other computer science | 2,977 |
| `spi.nano` | **Micro and nanotechnologies / microelectronics** | **2,831** |
| `info` | Computer science (top level) | 2,813 |
| `spi.auto` | **Automatic control / robotics** | **2,599** |
| `info.info-ai` | Artificial intelligence | 2,574 |
| `info.info-ni` | **Networking and internet architecture** | **2,317** |
| `spi.signal` | **Signal and image processing** | **2,247** |
| `spi.tron` | **Electronics** | **1,754** |
| `info.info-cr` | **Cryptography and security** | **1,035** |
| `spi.elec` | **Power electronics / electrical engineering** | **711** |
| `info.info-es` | **Embedded systems** | **474** |
| `info.info-ar` | **Computer architecture / hardware** | **275** |

**That is the single most useful subject breakdown in this record.** `spi.nano` (2,831),
`spi.tron` (1,754), `spi.signal` (2,247), `info.info-es` (474) and `info.info-ar` (275) are, between
them, roughly **7,500 free full-text French dissertations in microelectronics, electronics, signal
processing, embedded systems and computer architecture** — the LIRMM, TIMA, IEMN, LAAS, CEA-Leti and
INRIA output that [`hal.md`](hal.md) documents at the paper level, in its long form.

**Retrieval note:** the `theses.hal.science` *website* is behind Anubis, but
`api.archives-ouvertes.fr` is **completely open to default `curl`**. This is the canonical instance
of [`retrieval-notes.md` §3](retrieval-notes.md)'s rule — the human-facing site is walled and the
machine interface is not.

### 4.3 Sweden and the Nordics — DiVA

**DiVA** (*Digitala Vetenskapliga Arkivet*, `https://www.diva-portal.org/`) is a shared repository
platform used by around fifty Swedish, and some Norwegian, institutions — including **KTH**,
**Uppsala**, **Linköping**, **Chalmers-adjacent** bodies and **Blekinge Institute of Technology**.

**OAI-PMH is open and clean** [API] (S23):

```bash
curl -s "https://www.diva-portal.org/dice/oai?verb=Identify"
curl -s "https://www.diva-portal.org/dice/oai?verb=ListIdentifiers&metadataPrefix=oai_dc"
```

| Property | Value |
|---|---|
| `repositoryName` | **DiVA - Academic Archive On-line** |
| `baseURL` | `http://services.diva-portal.org/dice/oai` |
| `earliestDatestamp` | **1900-01-01T00:00:00Z** |
| **`deletedRecord`** | **`persistent`** |
| `resumptionToken` **`completeListSize`** | **800,381** |

**`deletedRecord="persistent"` is the good value** — the same guarantee arXiv gives
([`reliability-and-durability.md` §4](reliability-and-durability.md)): deletions are tombstoned, not
silently dropped, so an incremental harvester can stay consistent.

**800,381 is all record types**, not theses. DiVA's set list is organised by broad subject
(`PhysicsChemistryMaths`, `LifeEarthScience`, …) and by contributing institution
(`SwePub-kth`, `SwePub-liu`, `SwePub-bth`, …), with **no publication-type set**, so the
doctoral-thesis subset cannot be isolated through OAI. The `smash` web search *does* have
`publicationTypeCode:comprehensiveDoctoralThesis` / `monographDoctoralThesis` facets, but it
requires a JSF session (`dswid`) and returned a 4,481-byte stub to a stateless request.
**DiVA thesis-only count: [NOT-VERIFIED].**

**Why DiVA matters here:** Sweden's *sammanläggningsavhandling* (compilation thesis) convention means
a large fraction of DiVA doctoral theses are **"kappa + papers"** — an extended synthesis chapter
wrapped around the constituent papers. The kappa is often 40–80 pages and is frequently the only
place the *system*-level argument, the integration work and the cross-paper measurements are written
down. For KTH hardware and networking work specifically, the kappa is the document to read.

### 4.4 Germany — DNB and the fate of DissOnline

**DissOnline** was the DNB's dedicated dissertation portal. It no longer exists as a separate
service; German dissertation records are served through the **Deutsche Nationalbibliothek** catalogue
itself, which by statute receives a copy of every German dissertation.

- `https://portal.dnb.de/opac.htm` → **HTTP 200, 4,475 B, Anubis** [WEB] (S24). The catalogue front
  end is proof-of-work walled.
- `https://services.dnb.de/oai/repository?verb=Identify` → **HTTP 200, 779 B, clean OAI-PMH XML**
  [API] (S24):

```xml
<repositoryName>OAI-Repository of the German National Library V2.0.11</repositoryName>
<baseURL>https://services.dnb.de/oai/repository</baseURL>
<earliestDatestamp>1945-01-01T00:00:00Z</earliestDatestamp>
<deletedRecord>transient</deletedRecord>
<granularity>YYYY-MM-DDThh:mm:ssZ</granularity>
```

Another clean instance of the wall-the-site / open-the-API pattern. Note `deletedRecord="transient"`
— **weaker than DiVA's `persistent`**: the DNB does not promise to keep tombstones, so an
incremental harvester can silently drift.

**German dissertation count: [NOT-VERIFIED].** What was tried: the OAI `Identify` verb (gives no
count), and the walled portal. A `ListIdentifiers` walk over the relevant set would give it but was
not run within this pass's budget. German university repositories are the practical route — see
§5, and note that German doctoral regulations mandate *Veröffentlichung* (publication), which is why
German dissertation availability is unusually good.

### 4.5 Spain and Portugal — TDX/TDR and RCAAP, both walled

**TDX** (*Tesis Doctorals en Xarxa*) / **TDR** (*Tesis Doctorales en Red*),
`https://www.tdx.cat/` — the Catalan-led consortial repository covering Catalonia and much of Spain.
**HTTP 403 with the ~5.7 kB Cloudflare interstitial on every path tried**, including
`/oai/request?verb=Identify` and an individual `/handle/10803/1234` [WEB] (S25).

**But TDX is handle-based, and Handle.net is not walled.** This is the workaround, and it
generalises (§10):

```bash
curl -s "https://hdl.handle.net/api/handles/10803/1234"
# {"responseCode":1,"handle":"10803/1234","values":[{"index":100,"type":"URL",
#  "data":{"value":"https://www.tdx.cat/handle/10803/1234"}, ...}]}

curl -s "https://hdl.handle.net/api/handles/10803/99999999"
# {"responseCode":100,"handle":"10803/99999999"}          ← clean negative control
```

**`responseCode: 1` = exists; `responseCode: 100` = does not.** A JSON existence oracle for any
handle-minting repository, immune to the target's bot wall. This is strictly better than the
`doi.org` 403-passthrough trick in [`retrieval-notes.md` §4](retrieval-notes.md), because it returns
structured data rather than requiring you to interpret an error. **TDX record count:
[NOT-VERIFIED]** — no unwalled count interface found.

**RCAAP** (*Repositório Científico de Acesso Aberto de Portugal*), `https://www.rcaap.pt/` —
**Anubis on the front page and on `/OAIHandler?verb=Identify` alike** (4,511 B, `v1.26.0-pre2`)
[WEB] (S26). `https://www.rcaap.pt/oai/?verb=Identify` returns HTTP 400 with a Thymeleaf-rendered
*"OAI-PMH Data Provider"* error page, confirming a provider exists at some path but not telling us
which. **RCAAP is the one host in this pass where the "go round the wall via OAI-PMH" rule failed.**
Count: **[NOT-VERIFIED].**

### 4.6 Australia — Trove, and the ADT it absorbed

**Trove** (`https://trove.nla.gov.au/`, National Library of Australia) returned **HTTP 200, 7,745 B,
Anubis `v1.26.2`** [WEB] (S27).

Trove absorbed the **Australasian Digital Theses (ADT) Program**, the country's federated ETD
programme, which ceased as a separate service; Australian theses are now discoverable through Trove
and through the individual university repositories. **This record verified Trove's reachability
state and nothing else.** The ADT absorption is **[NOT-VERIFIED] as to date and mechanism** — no
primary source was retrieved for it within this pass, because the NLA's own pages are behind the
proof-of-work wall.

Trove has a well-documented **API requiring a free registered key**. No key was obtained, so no
count was measured. This is an access control, not a bot wall, and `AGENTS.md` rule 7 applies —
register properly rather than routing around it. **Trove thesis count: [NOT-VERIFIED].**

### 4.7 India — Shodhganga, and it is genuinely large

**Shodhganga@INFLIBNET** (`https://shodhganga.inflibnet.ac.in/`) is the Indian national ETD
repository, run by the INFLIBNET Centre under the Ministry of Education, and it is mandatory: UGC
regulations require Indian universities to deposit PhD theses. That mandate is why it is one of the
largest single-country full-text thesis collections on earth.

**Measured from its own front-page counters, 2026-09-04** [WEB] (S28):

| Counter | Value |
|---|---|
| **Full Text Theses** | **697,675** |
| SYNOPSES / MRPs / PDFs / Fellowships (Shodhgangotri) | **21,723** |
| **Universities Contributing** | **908** |
| Universities + CFTIs/INIs with signed MoU | **1,060** |
| (navigation) MoU with Universities · MoU with CFTI | 943 · 117 |

Announcements on the same page give the growth curve in Indian numbering [WEB] (S28):

> "Shodhganga crossed **5,35,000** Theses on **27th May 2024**."
>
> "Shodh ganga has crossed the remarkable milestone of **6,00,000** Theses. The Hon'ble Director,
> INFLIBNET Centre, Prof. Devika P. Madalli, marked this occasion by uploading the 6,00,000th
> thesis."

535,000 (May 2024) → 600,000 → **697,675** (September 2026). Roughly **70,000 theses a year**, all
full text, all free.

**⚠ New probing trap, and it is a nasty one.** The Shodhganga home page contains **a stale counter
block inside an HTML comment**:

```html
<!-- counters -->
<!--
<div class="sg-counts-box">
   ... <p class="sg-p">THESES</p> <span class="sg-span">597316</span>
   ... <p class="sg-p">SYNOPSES</p> <span class="sg-span">15274</span>
-->
```

The live counter, outside any comment, reads `<span class="counter digifont" id="theses1">697675</span>`.
**A text extractor that strips tags but does not strip HTML comments reads 597,316 — 100,359 too
low.** Both numbers look equally plausible. There is also a commented-out `99999` placeholder
immediately below the live counter, which would look like a real figure to a regex. **Strip comments
before scraping any figure from a hand-maintained institutional page.** [WEB]

**Reachability.** Four sequential requests to `https://shodhganga.inflibnet.ac.in/` gave
`200 / 200 / 200 / 000`, with successful responses taking **13.5–21.1 seconds**. An initial
Chrome-131 attempt timed out while a `curl/8.5.0` attempt succeeded, which *looked* like a reversed
user-agent ladder — **but it did not reproduce.** It is a slow, intermittently-overloaded origin,
not a UA filter. Recorded here explicitly because the tempting wrong conclusion was one probe away.
`http://` (port 80) fails outright; use HTTPS. A `/oai/request?verb=Identify` probe returned `000`
on the one attempt made — **Shodhganga OAI-PMH: [NOT-VERIFIED].** [WEB]

**What is in it, and the caveat.** Shodhganga is real and useful — Indian institute-of-technology
and NIT dissertations in VLSI, power electronics, antennas, embedded systems and communications are
there in quantity and in full text. The honest caveat is §7's: quality varies enormously across 908
contributing universities, and Shodhganga applies no quality gate of its own — it is a deposit
mandate, not an editorial process. The page itself links UGC plagiarism notices from 2018 and 2020
and a "Self Plagiarism" public notice, which tells you what the operators consider the live risk.

**Shodhganga's browse interface includes a "Researcher/Guide" index** — i.e. you can browse by
supervisor. That is directly the §5.8 technique, exposed as a first-class navigation option, and it
is rare.

### 4.8 Japan and Korea — CiNii Dissertations, RISS

**CiNii Dissertations has been folded into CiNii Research**, but the dissertation endpoint survives
as a first-class facet. `https://ci.nii.ac.jp/d/` — the old CiNii Dissertations URL, and the one
still listed in NDLTD's directory — **302s to `https://cir.nii.ac.jp/`** [WEB] (S29).

**The OpenSearch API answers JSON with no key** [API] (S29):

```bash
curl -s "https://cir.nii.ac.jp/opensearch/dissertations?format=json&count=1&from=1900"
# → "opensearch:totalResults": 775786
curl -s "https://cir.nii.ac.jp/opensearch/dissertations?q=RISC-V&format=json&count=1"
# → 6
curl -s "https://cir.nii.ac.jp/opensearch/all?q=RISC-V&format=json&count=1"
# → 514
```

| Query | Results |
|---|---|
| `dissertations`, `from=1900` (or `1800`, or `1`) | **775,786** |
| `dissertations`, `q=RISC-V` | **6** |
| `all`, `q=RISC-V` | 514 |
| `dissertations`, bogus term *(negative control)* | **0** — correct |
| **`dissertations` with no parameters at all** | ⚠ **0** |

**775,786 Japanese doctoral dissertations**, covering degrees conferred by Japanese universities and
by NIAD-QE. A named example returned by the RISC-V query: *"Trusted Execution Environment with
Silicon Level Root-of-Trust based on RISC-V Computer System"*.

**⚠ The empty-query trap again.** `?format=json&count=1` with **no** `q` and **no** date range
returns `totalResults: 0`. This is the **third independent instance** in this survey of the
"empty query means match nothing, not match everything" failure —
[`retrieval-notes.md` §7](retrieval-notes.md) already records it for **NASA NTRS** and **DOE OSTI**.
Three unrelated national services, same trap. **Promote it from "a NASA/DOE quirk" to a general
expectation about scholarly search APIs.** The workaround here is a wide date range; `q=*` also
returns 0, so do not use it.

**RISS** (*Research Information Sharing Service*, `https://www.riss.kr/index.do`, KERIS) returned
**HTTP 200, 390,685 B** [WEB] (S30) — alive, no bot wall on the front page. It is the Korean union
catalogue of academic information including domestic dissertations. **No count was extracted** —
the site is a large session-driven Korean-language portal and no unauthenticated count endpoint was
found within budget. **RISS dissertation count: [NOT-VERIFIED].**

### 4.9 Brazil and Latin America — one unreachable, one dead

**CAPES Catálogo de Teses e Dissertações** (`https://catalogodeteses.capes.gov.br/`) — **`000` on
both IPv6 and IPv4** [WEB] (S31). DNS resolves to `2001:12f0:b27:1005::38` (AAAA) and
`200.130.18.68` (A); `curl -4` and default both time out at 30–40 s. **This is recorded as
"unreachable from this environment", not as "dead"** — the discipline
[`retrieval-notes.md` §5](retrieval-notes.md) applies to `www2.eecs.berkeley.edu`. A Brazilian
government host may simply be geofenced or slow. **CAPES status and count: [NOT-VERIFIED].**

**⚠ Retrieval note worth propagating:** the default `getent hosts catalogodeteses.capes.gov.br`
returned **only the AAAA record**, which makes the host look IPv6-only and the failure look like an
IPv6 problem. `getent ahostsv4` shows an A record exists. **Check both families before diagnosing.**

**BDTD** (*Biblioteca Digital Brasileira de Teses e Dissertações*, IBICT,
`https://bdtd.ibict.br/vufind/`) is the better-known Brazilian aggregator and is what NDLTD's
directory lists. It returned **HTTP 200, 1,697 B, a challenge page titled *"Verificando conexão |
Oasisbr"*** [WEB] (S31) — alive, interstitial-walled, not measurable. **[NOT-VERIFIED].**

**Cybertesis is dead, and the domain has been monetised.** This is the clearest single failure in
this section [WEB] (S32):

| Probe | Result |
|---|---|
| `https://www.cybertesis.net/` | **`000`** — TLS/TCP failure |
| `http://www.cybertesis.net/` | **HTTP 200 → redirects to `welcome.lkg-app.com/?clickid=…&dkw=cybertesis.net&pid=…`**, 25,725 B, `<meta name="robots" content="noindex, nofollow">` |
| DNS | `cybertesis.net` and `www.cybertesis.net` → `208.91.196.105` |

`cybertesis.net` is now a **click-monetisation parking page**. This is precisely the failure mode
[`closed-and-defunct-servers.md` §2.4](closed-and-defunct-servers.md) documents for **BodoArXiv**
(an online casino), **LawArXiv** (a 114-byte parking stub) and **agriRxiv** (a Namecheap parking
page) — *"Domain lapse, parking, and hijack — the dangerous one"*. **Add Cybertesis to that table.**

Note that **NDLTD's own directory still links Cybertesis**, though to `cybertesis.unmsm.edu.pe` (the
Universidad Nacional Mayor de San Marcos instance) rather than the dead apex — so the *concept*
survives as individual university installations of the Cyberthèses software while the shared portal
does not. And note again the pattern from §2.4: **the directory outlived the thing it points at.**

**LA Referencia** (`https://www.lareferencia.info/`), the Latin American open-access repository
network, is what NDLTD lists as the regional successor. **Not probed in this pass —
[NOT-VERIFIED].**

### 4.10 Netherlands — NARCIS is confirmed discontinued

**Verified.** `https://www.narcis.nl/` **redirects to `https://dans.knaw.nl/nl/data-diensten/narcis/`**
[WEB]. DANS's own page, retrieved from the Internet Archive because the live DANS site is behind
Anubis (capture **2026-05-10**) [DOC] (S33):

> "As of **3 July 2023**, the NARCIS website was **taken offline and the NARCIS service ended**. The
> content, such as metadata of publications and datasets, is of course still available in the
> repositories of the various institutions and can be accessed or harvested there at any time.
>
> Research information from Dutch institutions can be found via the **'Portal of Research Output
> from the Netherlands'**. This portal was initiated by the **UKB and SURF** as a successor to
> NARCIS."

The same page adds: *"It is no longer possible to deposit data in EASY"* — DANS retired its
long-standing archive alongside NARCIS.

**The Wayback CDX series corroborates the date** [WEB] (S33): monthly 200s for `narcis.nl` through
**2023-07-02**, a 301 on **2023-08-17**, no usable captures Oct 2023 – Jan 2024, and an unbroken run
of 301s every month from **2024-02** to **2026-08**.

**Where Dutch theses went: to the university repositories, plus a national portal.** NDLTD's
directory lists the "Netherlands Research Portal" as **`https://netherlands.openaire.eu/`**, which
returned **HTTP 200, 232,623 B** on 2026-09-04 [WEB] (S33) — an OpenAIRE national portal. Whether
that is the same object as DANS's "Portal of Research Output from the Netherlands" (UKB/SURF) is
**[NOT-VERIFIED]**; the two names may denote two different services. For actual Dutch hardware and
systems dissertations the reliable route is the institutional repository — **TU Delft** in
particular (§5.6).

### 4.11 China — CNKI and Wanfang, and the honest answer

Both are reachable and both are **commercial subscription databases**. This record will not pretend
otherwise.

| Service | Probe | Result |
|---|---|---|
| **CNKI** | `https://www.cnki.net/` | **200 → redirects to `https://oversea.cnki.net/`**, 50,542 B (a `gb2312` JS geo-redirect stub at the apex) [WEB] (S34) |
| **Wanfang** | `https://www.wanfangdata.com.cn/` | **200**, 216,413 B [WEB] (S34) |

- **CNKI's *China Doctoral Dissertations Full-Text Database* (CDFD)** is the largest collection of
  Chinese doctoral dissertations in existence and is the only comprehensive route to them. It is
  **paywalled**, sold by institutional subscription, and NDLTD's own directory annotates the
  ProQuest entry as *"Paywalled resource"* and lists CNKI without such a note — **that annotation
  gap is misleading; CDFD is equally paywalled.** [INF]
- **Neither service was measured.** No count, no coverage figure, no full-text verification.
  Attempting to characterise their holdings from outside the paywall would be guessing.
  **CNKI and Wanfang holdings: [NOT-VERIFIED].**
- Chinese-language *preprints* are a different and partly-open story — see
  [`chinaxiv.md`](chinaxiv.md), which measures ChinaXiv at 47,362 native records (CS 2,052) and
  documents its own 403 trap.
- **Practical note:** a Chinese dissertation you cannot reach through CNKI is sometimes reachable
  through the awarding university's own repository, and increasingly through **CORE** and
  **OpenAIRE** (§2), which harvest some Chinese institutional repositories. Try those before
  concluding the document is unavailable.

### 4.12 Canada, Spain, Turkey — brief

- **Theses Canada** (Library and Archives Canada). The URL in NDLTD's directory,
  `collectionscanada.gc.ca/thesescanada/`, and the `bac-lac.gc.ca` form both fail (`000`);
  `library-archives.canada.ca/eng/services/…/theses-canada.aspx` **302s to `canada.ca/en/library-archives.html`**;
  the current search front end `recherche-collection-search.bac-lac.gc.ca` returns **HTTP 403, 5,775 B
  Cloudflare** [WEB] (S35). The service is believed to continue under LAC's unified collection
  search, but **nothing about it was verified** — **[NOT-VERIFIED]**. Canadian theses are, in
  practice, best found through the university repository or ProQuest (§6), since LAC's programme has
  long been coupled to ProQuest's Canadian dissertation intake.
- **TESEO** (Spain, Ministry). `https://www.educacion.gob.es/teseo/irGestionarConsulta.do` **302s to
  `https://aplicaciones.ciencia.gob.es/teseo`**, which returned **`000`** [WEB] (S36). TESEO is a
  *metadata* registry of defended Spanish theses; the full text is in TDX/TDR (§4.5) or the
  university repository. **[NOT-VERIFIED].**
- **Tez Merkezi** (Turkey, YÖK National Thesis Centre),
  `https://tez.yok.gov.tr/UlusalTezMerkezi/giris.jsp` → **HTTP 200, 33,811 B** [WEB] (S37). Alive
  and unwalled. It is a genuinely comprehensive national full-text system (Turkish doctoral
  regulations require deposit) and is under-known outside Turkey. **No count extracted —
  [NOT-VERIFIED].**

### 4.13 The finding that reframes §2: NDLTD has handed its search to OATD

Discovered while reading NDLTD's own navigation, and it explains the 503 in §2.2.

**Every "Global ETD Search" link on `ndltd.org` now points to `https://oatd.org/`** [WEB] (S38).
Verified in three places on the site — the main navigation menu (twice) and the *List of Resources
for Finding ETDs* table, where the row reads:

```html
<a href="https://oatd.org/" target="_blank" rel="noreferrer noopener">
  Global ETD Search (previously: Union Catalog)</a>
```

**NDLTD is no longer operating its own union catalogue; it is pointing at OATD.** The 503 at
`search.ndltd.org` is therefore not a broken server awaiting repair — it is a **retired service**,
and the redirect in the navigation is the announcement. No formal deprecation notice was located;
the link change *is* the notice. [INF, from the operator's own site]

**The consequence is uncomfortable and should be stated plainly.** The world's ETD union catalogue
has been consolidated onto **a single service that returns HTTP 403 to every automated client,
including `robots.txt`, on every user agent tried** (§2.3). For a human with a browser this is fine.
For anyone building a bibliography programmatically, for any downstream aggregator, and for this
knowledge base, **the global ETD discovery layer is now effectively closed to machines.** CORE
(§2.5) and OpenAIRE (§2.7) are the remaining open routes, and neither is thesis-specific.

Two smaller stale entries in the same directory, worth flagging to NDLTD if anyone is in contact:
its **EThOS** row links `https://bl.iro.bl.uk/` (the British Library *research repository*) rather
than the restored `https://ethos.bl.uk/`; and its **Cybertesis** row survives only because it points
at a university instance rather than the parked apex (§4.9).

---

## 5. Institutional repositories — where the hardware theses actually are

Given §2 and §4, the practical conclusion is unavoidable: **the institutional repository is the
primary source and the aggregators are an increasingly unreliable index over it.** This section is
the useful one.

### 5.1 Status table

All probes **2026-09-04**, Chrome-131 unless noted.

| Repository | URL | Status | Machine interface | Note |
|---|---|---|---|---|
| **MIT DSpace** | `dspace.mit.edu` | **200** | **DSpace 7 REST: `/server/api/discover/search/objects` — open, no key** | Best-behaved repository probed. Handles `1721.1/…` |
| **Caltech THESIS** | `thesis.library.caltech.edu` | **`000`** (both UAs) | — | TCP failure; shares `131.215.225.45` with `eprints.library.caltech.edu` |
| **Caltech AUTHORS** | `authors.library.caltech.edu` | **200**, 17,077 B | — | Cloudflare-fronted, InvenioRDM-style. Reachable |
| **Caltech via DataCite** | prefix **`10.7907`** | **200** | **DataCite REST — open** | **The working route to CaltechTHESIS while the site is down** |
| **UC Berkeley EECS TRs** | `www2.eecs.berkeley.edu/Pubs/TechRpts/…` | **302 → `iris.eecs.berkeley.edu`, then 404** | — | ⚠ **BROKEN SINCE ~2026-08.** See §5.4 |
| **CMU KiltHub** | `kilthub.cmu.edu` | 202 / 0 B (figshare trap) | **DataCite prefix `10.1184` — open** | Use DataCite, not the site |
| **ETH Research Collection** | `research-collection.ethz.ch` | **403**, **1,337 B** custom "Access Restricted" | **OAI-PMH open** at `/server/oai/request`; **DataCite prefix `10.3929` open** | ⚠ **New block fingerprint.** See §5.5 |
| **TU Delft** | `repository.tudelft.nl` | **200**, 925,475 B | not probed | Reachable |
| **KTH** | via **DiVA** (§4.3) | 200 | DiVA OAI-PMH, set `SwePub-kth` | |
| **KU Leuven Lirias** | `lirias.kuleuven.be` | **200 → `kuleuven.limo.libis.be` (Primo)**, 4,784 B | not found | SPA; no open API located |
| **TU Graz Pure** | `graz.elsevierpure.com` | **403**, 6,102 B Cloudflare | — | Walled |
| **TU Graz diglib** | `diglib.tugraz.at` | **200**, 12,844 B | not probed | Visual Library; digitised holdings |
| **U. Helsinki Helda** | `helda.helsinki.fi` | 200, 4,262 B **Anubis** `1.23.0` | **DSpace 7 REST open behind the wall** | Same wall-the-site pattern |
| **Cambridge Computer Lab** | `cl.cam.ac.uk/techreports/` | **200** | BibTeX, OAI-PMH, DBLP XML, RSS | Documented in [the companion record §3.5](government-and-institutional-technical-reports.md) |

**Two cross-cutting operational findings**, both of which are the difference between "I could not
find it" and "here it is":

1. **DSpace 7's REST API is the most useful single tool in this record.** `dspace.mit.edu` and
   `helda.helsinki.fi` both answered `GET /server/api/discover/search/objects?query=…&size=…` with
   full JSON — **including `dc.contributor.advisor`** — with no key, and Helda did so *from behind an
   Anubis wall*. See §10.
2. **When a repository is walled, go to DataCite.** Caltech, CMU and ETH were all measured through
   `api.datacite.org` while their own sites were unreachable or blocking. Any repository that mints
   DOIs is indexable through its prefix.

### 5.2 MIT DSpace

`https://dspace.mit.edu/` — handles of the form `1721.1/<n>`. This is where MIT theses live, and MIT
theses include several of the most consequential documents in the history of computing (§9).

**The API, verified 2026-09-04** [API] (S39):

```bash
curl -s -G "https://dspace.mit.edu/server/api/discover/search/objects" \
     --data-urlencode "query=symbolic analysis of relay and switching circuits" \
     --data-urlencode "size=5"
```

The response is HAL+JSON; the useful path is
`_embedded.searchResult._embedded.objects[]._embedded.indexableObject`, which carries `handle`,
`uuid` and a full `metadata` map. **The `dc.contributor.advisor` field is populated on MIT theses**
— this is the single most important field in this whole record for the §5.8 technique, and MIT
exposes it publicly and for free.

**A worked example — the Shannon record**, verbatim from the API [API] (S39):

| Field | Value |
|---|---|
| `dc.title` | A symbolic analysis of relay and switching circuits |
| `dc.contributor.author` | Shannon, Claude Elwood, 1916-2001. |
| **`dc.contributor.advisor`** | **Frank L. Hitchcock.** |
| `dc.description` | Thesis (M.S.)--Massachusetts Institute of Technology, Dept. of Electrical Engineering, **1940**. |
| `dc.description.degree` | M.S. |
| `dc.format.extent` | 69 leaves |
| `dc.date.issued` / `dc.date.copyright` | 1940 / 1940 |
| `dc.identifier.oclc` | 34541425 |
| `dc.identifier.uri` | `http://hdl.handle.net/1721.1/11173` |
| `dc.date.accessioned` | 2008-05-19T16:55:43Z |
| **`dc.rights`** | **"MIT theses are protected by copyright. They may be viewed, downloaded, or printed from this source but further reproduction or distribution in any format is prohibited without written permission."** |

**Two things in that table matter well beyond Shannon.**

**The date conflict.** MIT's own catalogue record says **1940**. The thesis is universally cited as
**1937** (the year Shannon completed the work at MIT while employed at Bell Labs over the summer of
1937), and the derived AIEE paper is **1938**. MIT's record almost certainly carries the *degree
conferral* year — Shannon received his SM in electrical engineering and his PhD in mathematics in
1940. **This survey records the conflict rather than resolving it** (README rule 4): if you cite the
MIT record, the metadata says 1940; if you cite the thesis, the scholarly convention is 1937. Say
which you mean. **[Conflict recorded; not resolved.]**

**The licence.** *"further reproduction or distribution in any format is prohibited without written
permission."* MIT theses are **free to read and not open-licensed.** That is the normal state of
affairs for theses, and §8 develops it. It is also a reason not to mirror MIT thesis PDFs into a
knowledge base.

**MIT's AI Memo and technical-report series are in the same repository** — handle `1721.1/5460` is
the collection "AI Memos (1959 – 2004)", verified in
[the companion record §3.2](government-and-institutional-technical-reports.md). **Theses and reports
sit side by side under one handle prefix**, and a search hits both. That is a feature: an MIT AI Lab
technical report is frequently a lightly-edited chapter of a thesis, or vice versa.

### 5.3 Caltech THESIS — down, and reachable anyway

`https://thesis.library.caltech.edu/` returned **`000`** (TCP failure) to both Chrome-131 and
`curl/8.5.0` on 2026-09-04. DNS resolves it to **`131.215.225.45`**, shared with
`eprints.library.caltech.edu` — i.e. CaltechTHESIS is (or was) an **EPrints** installation, and the
EPrints host is not answering. `authors.library.caltech.edu` — the separately-migrated CaltechAUTHORS
service — is on Cloudflare and returns **HTTP 200, 17,077 B** [WEB] (S40). A `resolver.caltech.edu`
probe with a plausible `CaltechTHESIS:` identifier returned **HTTP 404, 1,042 B**, so that resolver
is alive but the identifier form was wrong.

**Recorded as unreachable-from-here, not dead** — the same discipline the companion record applies to
`www2.eecs.berkeley.edu` and `hpl.hp.com`.

**The working route is DataCite prefix `10.7907`**, and it is excellent [API] (S41):

```bash
curl -s -G "https://api.datacite.org/dois" \
  --data-urlencode 'query=creators.name:"Dally" AND concurrent' \
  --data-urlencode 'prefix=10.7907' --data-urlencode 'page[size]=10'
```

Caltech has minted DOIs retroactively across the whole collection — **including 1985-vintage
Computer Science technical notes** — and the `types.resourceType` field distinguishes `Dissertation`
from `Technical note`. This is the **Carver Mead / Chuck Seitz VLSI lineage**, and §9 lists what was
verified. Caltech is the single richest source in this record for the analog-VLSI, self-timed-logic
and concurrent-architecture tradition.

### 5.4 ⚠ UC Berkeley EECS — the technical-report series went dark between 2026-08-12 and 2026-09-04

**This is a live, breaking finding, and it invalidates six canonical URLs recorded in
[`government-and-institutional-technical-reports.md` §3.1](government-and-institutional-technical-reports.md).**

Berkeley EECS files its **PhD dissertations and MS theses inside its technical-report series**. That
is why `UCB/EECS-2016-1` is simultaneously a technical report and Andrew Waterman's RISC-V design
dissertation, and why `UCB/EECS-2011-63` is a `@mastersthesis` in the department's own generated
BibTeX. It is the cleanest example anywhere of the report/thesis boundary being an administrative
fiction.

**Measured 2026-09-04** [WEB] (S42):

| URL | Result |
|---|---|
| `https://www2.eecs.berkeley.edu/Pubs/TechRpts/` | **HTTP 302 → `https://iris.eecs.berkeley.edu/Pubs/TechRpts/` → HTTP 404**, 58,829 B WordPress "Page not found \| IRIS" |
| `https://www2.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-1.html` | **302 → 404**, 58,829 B |
| `https://www2.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-1.pdf` | **302 → HTTP 404, 548-byte nginx page** |
| `https://www.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-1.html` | **302 → 404** |
| `https://eecs.berkeley.edu/research/publications/` | **HTTP 404**, 99,227 B |

**The 302 is unconditional.** Chrome-131, `curl/8.5.0` and Googlebot all received the identical
`location: https://iris.eecs.berkeley.edu/Pubs/TechRpts/`. This is not a bot wall.

**DNS shows what happened** [WEB] (S42):

```
www2.eecs.berkeley.edu  → 128.32.139.28  (eecs-haproxy-vip.eecs.berkeley.edu)   ← the old origin
iris.eecs.berkeley.edu  → 141.193.213.10/.11 (wp.wpenginepowered.com)           ← WordPress on WP Engine
www.eecs.berkeley.edu   → 141.193.213.10/.11 (wp.wpenginepowered.com)
```

The department moved to a WP Engine-hosted WordPress site (`IRIS` — *Instructional & Research
Information Systems*, HTTP 200, 83,508 B) and installed a **blanket catch-all redirect** from the
old host into it. The new site has no `/Pubs/TechRpts/` route, so **every URL in the series
resolves to a 404 with a marketing-site chrome around it.**

**Dating the break, from the Wayback CDX index for the series index page** [WEB] (S42):

| Capture | Status |
|---|---|
| 2025-02 → 2026-02 | mostly **200**, 14.5–15.1 kB |
| 2026-04-04 | 403, 4,815 B |
| **2026-05-04, 2026-06-03, 2026-07-11, 2026-08-12** | **200**, 15,122 / 15,264 / 15,270 / **15,267 B** |
| 2026-09-04 (this probe) | **302 → 404** |

**The index was serving normally as recently as 2026-08-12.** The break therefore falls in a
**three-week window, 2026-08-12 to 2026-09-04**. No announcement was located.
**[NOT-VERIFIED]:** whether a replacement location exists. `escholarship.org` — UC's system-wide
repository, the obvious destination — returned **HTTP 202 with a zero-byte body**, the same
figshare-style non-answer already recorded for `figshare.com` and `kilthub.cmu.edu` in
[`retrieval-notes.md` §1](retrieval-notes.md), so it could not be searched.

**The content survives in the Internet Archive, and we re-verified it.** Retrieved 2026-09-04 [WEB
via Wayback] (S42):

```
http://web.archive.org/web/20220425162607id_/https://www2.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-1.pdf
→ HTTP 200, 959,927 bytes, PDF version 1.4
```

**959,927 bytes exactly matches the figure recorded in
[the companion record §3.1](government-and-institutional-technical-reports.md)** from a separate
probe two days earlier — an independent confirmation that the archived artefact is the right one.
The CDX index holds 200-status captures of that PDF from **2017-10-21 (778,143 B)**, **2020-08-06**,
**2020-10-05**, **2020-11-13**, **2021-08-22**, **2021-10-19** and **2022-04-25 (776,543 B)**.

**Three lessons, and they are the ones this whole directory keeps re-learning.**

1. **A blanket redirect into a redesigned site is worse than a 404.** It converts a clean "gone"
   signal into a 200-then-404 chain wrapped in unrelated chrome. A link-checker records "redirect
   OK"; a human sees a marketing page.
2. **`government-and-institutional-technical-reports.md`'s own recommendation was right and should
   be acted on now.** That record said, of the DEC/Compaq series: *"When you find a corporate report
   series that matters to you, take a copy."* The same now applies to a **university** series, and
   to the RISC-V specifications specifically.
3. **The Wayback copy is currently the only verified route to the origin documents of RISC-V.** That
   is an uncomfortable sentence to write about an actively-developed, industrially-significant ISA,
   and it is what the measurement says. See §13.

### 5.5 ETH Zürich Research Collection — SAFARI, and a new block fingerprint

`https://www.research-collection.ethz.ch/` is ETH's DSpace-CRIS repository, and it is directly
relevant here because the **SAFARI group (Onur Mutlu)** deposits its memory-systems and
RowHammer-lineage dissertations there.

**⚠ New block fingerprint — record this.** The DSpace REST API returns **HTTP 403 with a 1,337-byte
custom HTML page**, not a Cloudflare or Anubis interstitial [WEB] (S43). It is *self-documenting*,
which is unusual and welcome:

> **Access Restricted**
>
> "Due to a high volume of automated traffic (scraping), access to the ETH Zurich Research Collection
> is **temporarily restricted from your location / your provider**. This measure helps ensure system
> availability for our users. If you have been blocked accidentially, please contact us at
> `research-collection@library.ethz.ch`."

Distinguishing features for a fingerprint table: **HTTP 403, ~1,337 bytes, `<title>Access
Restricted</title>`, inline `Segoe UI` CSS, German-flavoured spelling "accidentially", a contact
address.** It is **IP/provider-scoped**, not user-agent-scoped — the page says so — so the UA ladder
is the wrong tool. The right response is the contact address.

**Two open routes were found** [API] (S43):

```bash
# 1. OAI-PMH is completely open
curl -s "https://www.research-collection.ethz.ch/server/oai/request?verb=Identify"
#   repositoryName: ETH Research Collection
#   earliestDatestamp: 2017-05-15T06:24:06Z
#   deletedRecord: transient
#   granularity: YYYY-MM-DDThh:mm:ssZ

# 2. DataCite, prefix 10.3929
curl -s -G "https://api.datacite.org/dois" \
  --data-urlencode 'query=DRAM AND types.resourceType:Dissertation' \
  --data-urlencode 'prefix=10.3929'
```

Note `earliestDatestamp: 2017-05-15` — the Research Collection replaced ETH's earlier e-collection
platform, and the OAI datestamps start at the migration, not at the content's origin. **Do not read
it as a coverage floor.**

**The SAFARI dissertations, verified via DataCite** [API] (S43) — full table in §9:

| DOI | Year | Author | Title |
|---|---|---|---|
| `10.3929/ethz-b-000601914` | 2022 | Hasan Hassan | Improving DRAM Performance, Reliability, and Security by Rigorously Understanding Intrinsic DRAM… |
| `10.3929/ethz-b-000691009` | 2024 | A. Giray Yağlıkçı | Enabling Efficient and Scalable DRAM Read Disturbance Mitigation via New Experimental Insights… |
| `10.3929/ethz-b-000698237` | 2024 | Michele Marazzi | Principled DRAM Security against Rowhammer Attacks |
| `10.3929/ethz-b-000542542` | 2021 | Minesh Patel | Enabling Effective Error Mitigation in Memory Chips That Use On-Die Error-Correcting Codes |

**Why this matters concretely.** [`landmark-papers.md` §1](landmark-papers.md) records that the
original RowHammer paper (*Flipping Bits in Memory Without Accessing Them*, ISCA 2014) is **not on
arXiv** — the only hit is the 2023 retrospective. The conference papers in this lineage are 12–13
pages each. **These four dissertations are 150–300 pages each and they contain the actual DRAM
characterisation infrastructure** — the FPGA-based memory controllers, the temperature-controlled
test setups, the per-module scan methodology, the negative results on mitigation schemes that did
not work. If you are trying to reproduce or extend RowHammer work, the dissertations are the
documents. This is §1's argument in its purest form.

DataCite also surfaced, in the same prefix, ETH **bachelor's** theses of real substance — e.g.
`10.3929/ethz-b-000722911`, *"REFault: A Fault Injection Platform for Rowhammer Research on DDR5
Memory"* (Stefan Gloor, 2023). **Do not filter out non-doctoral theses when hunting for hardware
infrastructure.** A bachelor's or master's thesis is frequently where a specific piece of test
apparatus is documented, because that is exactly the size of task a supervisor hands to a
master's student.

### 5.6 TU Delft and KTH

**TU Delft** — `https://repository.tudelft.nl/` → **HTTP 200, 925,475 B** [WEB] (S44). Reachable and
unwalled. TU Delft's repository is the route to Dutch hardware and systems dissertations now that
NARCIS is gone (§4.10), and it is the natural home for the embedded-systems, quantum-hardware and
networking work the university is known for. **No machine interface was probed and no count was
obtained — [NOT-VERIFIED].**

**KTH** deposits into **DiVA** (§4.3), set `SwePub-kth`, harvestable over the open DiVA OAI-PMH
endpoint. The Swedish compilation-thesis convention (§4.3) makes KTH doctoral theses unusually
information-dense: the *kappa* is a purpose-written synthesis, not a stapled bundle.

### 5.7 KU Leuven COSIC and TU Graz IAIK — the hardware-security long form

These two groups are named here because they are the **long-form layer under
[`cryptology-eprint-archive.md` §7.6](cryptology-eprint-archive.md)**, which records ePrint as
*primary* for side-channel and embedded security. The ePrint reports are 15–25 pages. The
dissertations behind them are where the measurement setup lives.

**KU Leuven COSIC.** `https://lirias.kuleuven.be/` **redirects to
`https://kuleuven.limo.libis.be/discovery/search?vid=32KUL_KUL:Lirias`** — an Ex Libris **Primo**
front end, HTTP 200 but a 4,784-byte Angular shell [WEB] (S45). **No open API was located** and
**no COSIC dissertation was verified in this pass — [NOT-VERIFIED].** Primo installations generally
expose a `pnxs` REST endpoint but it is institution-configured and was not found. The practical
route for COSIC specifically is the **group's own publications page**, which has historically listed
its PhD theses with direct PDFs; that was not probed here.

**TU Graz IAIK** — the Spectre/Meltdown lineage (Daniel Gruss, Moritz Lipp, Michael Schwarz and
colleagues). Two hosts:

- `https://graz.elsevierpure.com/…` (the Pure CRIS) → **HTTP 403, 6,102 B Cloudflare** [WEB] (S46).
- `https://diglib.tugraz.at/` → **HTTP 200, 12,844 B**, a Visual Library instance
  ("digitalisierte Zeitschriften und Bücher"); `/dissertationen` returns 200, 10,815 B [WEB] (S46).
  Not searched further.

**What was verified about Gruss's dissertation is only its published summary.** Crossref [API]
(S47):

```
10.1515/itit-2018-0034 · "Software-based microarchitectural attacks" · Gruss
· it - Information Technology (De Gruyter) · 2018-11-20
```

That is the *dissertation abstract/summary* genre — German-speaking computer science publishes
condensed dissertation reports in *it – Information Technology*. **It is not the thesis.** The full
TU Graz dissertations of Gruss and Lipp were **[NOT-VERIFIED]** in this pass: the Pure front end is
Cloudflare-walled, and no unwalled TU Graz repository search was found within budget. This is a real
gap and it is listed in §13.

**A useful generalisation from this failure.** For German, Austrian and Swiss dissertations, check
*it – Information Technology* (De Gruyter) and the equivalent society digests: a Crossref query on
the author's name will often surface a 4-page dissertation summary with a DOI when the full thesis is
hard to locate. It is not a substitute — but it gives you the exact title, the year, the institution
and the supervisor, which is what you need to find the real thing.

### 5.8 How to find a thesis when you know the author and the advisor

This is how it actually works in practice, and it is worth stating as a procedure because the
obvious approach — searching for the thesis title — usually fails, since you do not know the title.
The thesis title is almost never the paper title.

**The core insight: a thesis is indexed under the *institution* and the *year*, not under the topic
you care about.** So you work backwards from the person.

**Step 1 — Establish the institution and the approximate year.**
From any paper by the author, take the affiliation on the *earliest* paper in the line of work. That
is where they were a student. The thesis year is typically **the year of the last first-author paper
in that line, plus zero to one**. If the paper says "this work was performed while the author was at
X", that is your institution.

**Step 2 — Establish the advisor.** The advisor is the last author on the student's papers in most
hardware and systems venues. If the group is one you know (SAFARI, COSIC, IAIK, ASPIRE/BAR), the
advisor is the group head.

**Step 3 — Query the institutional repository by advisor, not by title.** This is the step people
skip. Repository metadata carries a supervisor field far more often than anyone expects:

| Source | Advisor field | Verified |
|---|---|---|
| **MIT DSpace** | `dc.contributor.advisor` — populated, in the public REST API | ✅ (§5.2 — Shannon → "Frank L. Hitchcock.") |
| **theses.fr** | `directeurs` on the thesis record; `roles` counts on `/personnes` | ✅ (§4.2) |
| **Shodhganga** | a browse index literally labelled **"Researcher/Guide"** | ✅ (§4.7) |
| **EThOS bulk CSV** | a **`Supervisor(s)`** column | ✅ (§3.6) |
| DSpace generally | `dc.contributor.advisor` is a standard DSpace thesis field | [INF] |

Concretely, on any DSpace 7 repository:

```bash
curl -s -G "https://dspace.mit.edu/server/api/discover/search/objects" \
     --data-urlencode "query=<advisor surname>" --data-urlencode "size=50" \
| python3 -c 'import json,sys
d=json.load(sys.stdin)["_embedded"]["searchResult"]["_embedded"]["objects"]
for x in d:
    i=x["_embedded"]["indexableObject"]; m=i.get("metadata",{})
    adv=[v["value"] for v in m.get("dc.contributor.advisor",[])]
    if adv: print(i["handle"], adv, i.get("name")[:70])'
```

That returns the advisor's entire student list from the repository, with handles. It is how §9's
MIT entries were found: a query for `Knight implementation of a list processing machine` returned
Tom Knight's own 1979 thesis (advisor **Marvin L. Minsky**) *and* two later theses he supervised —
the lineage falls out of the metadata for free.

**Step 4 — If the institutional repository fails, use the bulk metadata.** For the UK, the 709 MB
`EThOS_CSV_202310.csv` (§3.6) has `Author`, `Supervisor(s)`, `Institution`, `Date`, `Abstract` and
**`IR URL`** in one file. `grep` on a supervisor name is faster and more reliable than any web
search, and it works offline.

**Step 5 — If you still cannot find it, look in the technical-report series.** Berkeley EECS
(§5.4), Cambridge Computer Lab (`UCAM-CL-TR-<n>`), CMU SCS and MIT AI Memos all file dissertations
as numbered reports. A thesis missing from a "theses" collection is often present in the "reports"
collection of the same department. See
[`government-and-institutional-technical-reports.md`](government-and-institutional-technical-reports.md).

**Step 6 — Check the personal page.** This is not a joke and §9 proves it: **Linus Torvalds's
master's thesis is not in Helda, the University of Helsinki repository — it is a PDF on a
professor's departmental home page** (verified, §9). For pre-2005 work especially, the author's or
advisor's `~user` page is a real and frequently the only source. It is also the most fragile one:
these are prime `web.archive.org/save/` candidates under `AGENTS.md` rule 9.

---

## 6. Commercial and restricted routes

### 6.1 ProQuest Dissertations & Theses Global

**PQDT Global** is the commercial dissertation database, and it is genuinely the largest single
index of theses in existence. ProQuest's own product page, `https://about.proquest.com/en/products-services/pqdtglobal/`
→ HTTP 200, 347,146 B, retrieved 2026-09-04 [DOC] (S48):

> "With over **6 million metadata records** including **4 million full text documents**, ProQuest
> Dissertations & Theses Global is the world leader in providing access to dissertation and thesis
> research."
>
> "…more than 6 million dissertations and theses citations from over **3,600 institutions** from more
> than **70 countries**…"

Set that against the open figures in §2 and §4:

| Source | Records | Full text |
|---|---|---|
| **PQDT Global** | **~6,000,000** | **~4,000,000** [DOC] |
| OATD | 7,407,210 (2025-03) | metadata-plus-link [WEB] |
| CORE `documentType:"thesis"` | 7,921,188 | CORE stores full text [API] |
| OpenAIRE (3 thesis types) | ≤8,346,188 | mixed [API] |
| NDLTD Global ETD Search | 6,534,039 (2025-05, now 503) | metadata-plus-link [WEB] |

**PQDT is not obviously larger than the open aggregators by record count.** What it has that they do
not is (a) a curated, deduplicated, consistently-catalogued index, (b) **4 million full texts under
one licence**, including a great deal of pre-1997 North American material that exists nowhere else
digitally, and (c) subject indexing. What it does not have is anything a hardware engineer cannot
usually reach another way, *for recent work*.

**How access actually works, stated precisely:**

- **PQDT Global is a subscription database.** Access is through a subscribing library. This is an
  access control and `AGENTS.md` rule 7 applies — do not attempt to route around it.
- **ProQuest is owned by Clarivate**, and the product page markets PQDT integration with **Web of
  Science**. Disclose that entanglement when citing PQDT coverage figures, in the same spirit as
  [`reliability-and-durability.md` §4](reliability-and-durability.md)'s treatment of Elsevier/SSRN
  and Springer Nature/Research Square.
- **ProQuest acquires the content by being the North American dissertation-deposit intermediary.**
  Many US and Canadian universities have historically submitted every dissertation to ProQuest as
  part of the graduation workflow. That is why its pre-web coverage is unmatched, and it is also why
  the same document is very often *also* in the university's own repository.

### 6.2 PQDT Open — gone as a standalone service

**This is a finding, and it is not good news.** `https://pqdtopen.proquest.com/` — the free,
open-access subset of PQDT — returned **HTTP 302 to `https://www.proquest.com/?defaultdiss=true`** on
2026-09-04 [WEB] (S48). The standalone PQDT Open front door no longer exists; you land on the main
ProQuest platform with a dissertations default filter, which for an unsubscribed visitor is not a
free full-text service.

**PQDT Open's current status and record count: [NOT-VERIFIED].** What was tried: the canonical
hostname (302 as above) and `https://www.proquest.com/pqdtglobal` (302, zero-byte body). Whether the
open-access subset still exists as a searchable, freely-downloadable collection under the main
platform was not established. **Do not cite PQDT Open as a live free route without re-checking it.**

This is the same pattern as §2.4 (DART-Europe) and §4.13 (NDLTD): **a free discovery layer being
folded into, or replaced by, something less open.** Three instances in one pass is a trend worth
naming.

### 6.3 EBSCO Open Dissertations — a free alternative that is easy to miss

`https://www.ebsco.com/products/research-databases/ebsco-open-dissertations` → 301 →
`https://about.ebsco.com/…` → HTTP 200, 68,261 B [DOC] (S49). EBSCO's own words:

> "EBSCO Open Dissertations makes electronic theses and dissertations (ETDs) more accessible to
> researchers worldwide. **The free portal** is designed to benefit universities and their students
> and make ETDs more discoverable. Content Includes: **2,000,000 electronic theses and
> dissertations**; **325 worldwide universities** that have loaded their dissertations to date."

**2 million ETDs, free, from a commercial vendor.** It descends from the old *American Doctoral
Dissertations* index that H. W. Wilson maintained. It appears in NDLTD's directory and almost nowhere
else, and it is a legitimate fourth option alongside CORE, OpenAIRE and OATD. **Not probed
functionally in this pass — the count above is EBSCO's claim, not our measurement.**

### 6.4 The point that makes most of §6 optional: authors self-archive

**The same document is very often in three places at once**, and only one of them is behind a
paywall:

1. The **commercial database** (PQDT), because the university's graduation workflow deposited it.
2. The **institutional repository**, because the university's open-access policy required it.
3. The **author's own website**, because early-career researchers put their thesis on their homepage.

Route (2) is free, canonical and citable. Route (3) is free, fragile and often the only route for
pre-2005 work (§9's Torvalds entry is the proof). **Check the institutional repository before paying
for anything**, and check the author's page before concluding the document is unavailable.

**A caution that cuts the other way.** The three copies are **not necessarily the same file.** See
§7.3 on version semantics: the copy an author put on their homepage in 2004 may be the pre-defence
draft, and the repository copy may be the corrected final. When it matters, cite the repository.

---

## 7. Reliability — what a thesis actually guarantees

### 7.1 The gate, in the terms this survey already uses

[`reliability-and-durability.md` §1](reliability-and-durability.md) sorts preprint servers by their
**gate**, on the principle that *"reliability is a question about the gate, not about the badge"*.
The thesis gate slots into that table, and it is a genuinely different shape from anything on it:

| Gate type | Example | What it proves |
|---|---|---|
| None whatsoever | Zenodo, figshare, viXra | A DOI and a timestamp |
| Endorsement + subject moderation | arXiv | An endorsed author and a plausible subject fit |
| Named editorial screening | Cryptology ePrint, Optimization Online | Relevance and non-obvious-crackpottery |
| Journal peer review | (off this survey's list) | 2–4 anonymous referees read it once, on a deadline, unpaid, and recommended acceptance |
| **Examination and defence** | **a doctoral thesis** | **A named committee read the whole document, questioned the candidate live for 1–3 hours, and required revisions before signing** |

**On three axes the thesis gate is genuinely stronger than journal review:**

- **Completeness.** A referee checks that the claims are supported. A committee checks that the
  *work* is a coherent, sufficient body — which is why the methods chapters exist at all.
- **Interrogation.** The oral defence is the only point in the entire scholarly process at which
  someone can ask a follow-up question and get an answer in real time. A referee cannot. This is
  unusually effective at catching a candidate who does not understand their own apparatus.
- **Accountability.** Committee members are **named** in the document. Referees are anonymous.
  A signed thesis is a public assertion by identified senior researchers that the work is sound.

**On three other axes it is weaker, and these are not small:**

- **The supervisor is on the committee.** The person with the largest stake in a pass outcome is one
  of the assessors. In some systems they chair it.
- **There is no cross-institution standard.** None. A doctorate from two different universities in
  the same country can represent enormously different amounts of work and scrutiny, and there is no
  external body that normalises this. This is the single largest caveat in this section and it
  applies globally, including within highly-regarded systems.
- **The audience is one committee, not a field.** A journal referee is selected for topical
  expertise. A committee is selected for availability and institutional requirements, and may
  contain nobody who has built the thing the candidate built.

### 7.2 Failure modes specific to theses

- **The advisor's framing goes unchallenged.** A thesis is written to satisfy a supervisor; a
  supervisor's idiosyncratic view of the field is therefore over-represented, particularly in the
  literature review. Read the related-work chapter for *pointers*, not for judgement.
- **Self-citation and group-citation are structurally high.** A thesis built on the group's prior
  papers cites them heavily and correctly. That is not misconduct, but it means citation counts
  within a thesis are not a signal of field consensus.
- **Volume mandates dilute.** Systems with a national deposit mandate (§4.7 Shodhganga, Germany,
  Turkey) contain every thesis, not the good ones. **A mandate is a coverage guarantee, not a
  quality gate**, and this survey's standing rule applies: *if you cannot determine the gate, treat
  it as "none"*.
- **Plagiarism and, since ~2023, machine generation.** Shodhganga's own front page links UGC
  plagiarism notices from 2018 and 2020 and a separate self-plagiarism notice — the operator telling
  you what they consider the live risk. [`reliability-and-durability.md` §3](reliability-and-durability.md)
  documents three preprint operators tightening against AI-generated text in 2025; **no equivalent
  measurement exists for theses**, and this record makes no claim about it. **[NOT-VERIFIED].**
- **The paper is often better than the thesis on the same result.** A chapter written in year two
  and lightly updated for submission can carry worse numbers than the conference paper that came out
  of it eighteen months later. **Read both; prefer the paper for the headline result and the thesis
  for the method.**

### 7.3 Version semantics — the part people get wrong

A thesis exists in **at least three** distinct versions, and repositories are inconsistent about
which one they hold.

| Version | What it is | Typical marker |
|---|---|---|
| **Submitted / examination copy** | What went to the committee before the viva | Rare in repositories. Sometimes on the author's homepage |
| **Accepted** | The version the committee passed, *before* required corrections | Occasionally deposited by mistake |
| **Corrected / final / of record** | Post-viva, post-corrections, formally accepted by the graduate school | **What a repository should hold.** Usually carries a degree-conferral date |
| **Published derivative** | A revised commercial monograph (common in some fields), or a dissertation summary such as `10.1515/itit-2018-0034` (§5.7) | A publisher DOI and a different title |

**How to tell which one you have — a practical checklist:**

1. **Look for a signed approval or certification page.** A final version normally carries a signature
   page or a formal statement of acceptance with the conferral date. A submitted copy does not.
2. **Compare the repository's `date.issued` with the degree year.** MIT's Shannon record shows
   `dc.description: "Thesis (M.S.)--…, 1940"` alongside `dc.date.issued: 1940` — internally
   consistent. A file dated a year *before* the recorded degree year is a pre-correction copy.
3. **Check `dc.description.degree` / qualification fields.** EThOS records carry
   `Qualification Name: Thesis (Ph.D.)` and `Date Awarded`; theses.fr carries `dateSoutenance` (the
   defence date) *and* `datePremiereInscriptionDoctorat`. The defence date, not the file date, is the
   citation year.
4. **Beware the author's homepage copy.** It is frequently the version the author was proudest of,
   which is not necessarily the version the university holds.
5. **If a repository offers "Version of Record" versus "Author Accepted Manuscript" labelling for
   theses, believe it; most do not offer it at all.**

**How to cite one defensibly.** Combine four things, and the first is the one people omit:

```
Author. Title. <Degree> thesis, <Institution>, <year of award>.
<persistent identifier>. <access date if no PID>.
```

- **Use the persistent identifier, not the URL.** For theses that means a **handle**
  (`hdl.handle.net/1721.1/11173`), a **DOI** (`10.3929/ethz-b-000601914`,
  `10.7907/f8d5-x741`), an **NNT** (`2016PA066033`), an **EThOS ID** (`uk.bl.ethos.906226`) or a
  **report number** (`UCB/EECS-2016-1`). §5.4 is the argument: the Berkeley URLs died in a
  three-week window and the report numbers did not.
- **State the degree and the institution.** "PhD thesis, ETH Zürich" carries information that the
  DOI alone does not, and it is what tells a reader what gate the document passed.
- **Use the year of award**, and if it conflicts with the repository's `date.issued`, say so —
  Shannon 1937/1940 is the canonical example (§5.2).
- **If you are relying on a specific chapter's method, cite the chapter and page range.** The whole
  point of using a thesis is that the detail is in one chapter; a whole-document citation makes the
  reader find it again.

### 7.4 When to trust a thesis more than the paper

Stated positively, because §7.1–7.3 are all caveats. Prefer the thesis when:

- You need to **reproduce** something. The setup, calibration and part numbers are there and are
  nowhere else (§1.2).
- You need **negative results**. "We tried X and it did not work" survives only here.
- You need the **failure analysis of a physical artefact** — board spins, yield, thermal behaviour,
  process variation.
- The paper is **paywalled and the thesis is not**, which is very common: the thesis chapter
  frequently predates and substantially overlaps the paywalled paper, and the repository copy is
  free and legitimate.
- The work **never became a paper at all.** A great deal of instrumentation and tooling is in this
  category, and for it the thesis is not the long version — it is the *only* version.

---

## 8. Embargoes and licensing

This is the most widely misunderstood part of the thesis landscape, and it is where a naive
"open access" assumption produces wrong conclusions.

### 8.1 Embargoes are normal, not exceptional

A thesis embargo is a period during which the **record is public and the file is not**. Typical
lengths run from **6 months to 5 years**, and permanent restriction exists. The common reasons:

| Reason | Typical length | Notes |
|---|---|---|
| **Patent filing** | 6–24 months | The dominant reason in hardware, materials and EE. The university's technology-transfer office requests it |
| **Publisher / prior-publication concern** | 6–24 months | The candidate intends to turn a chapter into a paper or a monograph and fears a "prior publication" objection |
| **Industrial sponsor or NDA** | 1–5 years, sometimes indefinite | Very common in semiconductor, defence and automotive work. The sponsor owns or restricts disclosure |
| **Commercially sensitive data** | variable | Fab data, yield numbers, customer data |
| **Personal safety / sensitive fieldwork** | variable to permanent | Rare in this knowledge base's fields |
| **Third-party copyright the author could not clear** | often permanent for *part* of the document | Produces the "redacted version" pattern below |

**For hardware specifically, the patent reason dominates**, and it is worth internalising why: the
work most worth reading — a novel circuit, a novel process step, a novel architecture — is exactly
the work most likely to be embargoed. **The embargo rate is not uniform across topics; it is highest
precisely where this knowledge base's interest is highest.** [INF]

**Embargo rates were not measured in this pass. [NOT-VERIFIED].** No repository probed publishes an
aggregate embargo statistic, and none of the APIs used exposes a queryable embargo facet. This is a
real gap and a good target for a future pass: DSpace's `dc.date.available` versus `dc.date.issued`
differential is, in principle, measurable in bulk over OAI-PMH.

### 8.2 How an embargo appears in metadata — and how it appears to *you*

**The crucial point: an embargoed thesis looks exactly like an available one in a search result.**
Google Scholar, CORE, OpenAIRE, OATD and EThOS all index the *record*. The wall is one click deeper.

Recognisable patterns, in rough order of how often you will hit them:

1. **A landing page with no file and no explanation.** Most common. The record renders normally; the
   download section is simply absent.
2. **An explicit availability date.** DSpace's `dc.date.available` is set to a future date; the UI
   says "Available after 2027-06-01" or "Under embargo until…". **This is the good case** — you know
   exactly when to come back.
3. **"Restricted access" / "Access restricted to <institution> users".** The file exists and is
   IP-limited. This is an access control, not a bot wall: `AGENTS.md` rule 7 applies.
4. **A redacted version alongside a full version.** Two files, one public with chapters or figures
   removed. Common where third-party copyright could not be cleared. Look for "redacted",
   "public version" or a suspiciously small PDF.
5. **A metadata-only record with a contact instruction.** EThOS does this explicitly and by design
   now — the record probed in §3.5 read *"EThOS does not have a link to a university copy of this
   thesis. If you would like to view this thesis, we recommend that you contact Royal Veterinary
   College."* **Note that this is indistinguishable, from the outside, from an embargo.** It could
   equally be a pre-digital paper-only thesis, or a repository the harvester has not reached yet —
   the EThOS FAQ lists all three causes for the same visible state (§3.3).
6. **The "request a copy" button.** DSpace and EPrints both ship a feature that emails the author.
   It works more often than people expect, especially for a thesis five or more years old whose
   embargo reason has expired but whose flag nobody cleared.

**Practical consequences:**

- **Absence of a file is not evidence of absence of the thesis.** Check the awarding institution
  directly, then the author, then a later date.
- **An embargo expires and the metadata often does not get updated.** Re-check old embargoed records;
  the file is frequently there now.
- **Do not report an embargoed record as a dead link.** It is neither dead nor broken; it is a
  deliberate temporary state, and confusing the two corrupts durability statistics.

### 8.3 Licensing — the genuine reuse problem

**Theses are free to read and almost never openly licensed.** This is the single most important
practical fact in §8, and it is the opposite of what people assume from the phrase "open access
repository".

**The verified example**, from MIT's own record for Shannon's thesis [API] (§5.2, S39):

> `dc.rights`: "MIT theses are protected by copyright. They may be viewed, downloaded, or printed
> from this source but **further reproduction or distribution in any format is prohibited without
> written permission**."

That is a **read-only permission grant, not an open licence.** No CC-BY, no derivative rights, no
redistribution, and — read strictly — **no text and data mining**. This is normal. The copyright in
a thesis is usually retained by the author; the university takes a non-exclusive licence to hold and
display it; and nobody involved has any incentive to attach a CC licence.

**The picture across the systems measured here:**

| Object | Licence | Evidence |
|---|---|---|
| **MIT theses** | Read/download/print only; redistribution prohibited without permission | [API] `dc.rights`, §5.2 |
| **EThOS bulk metadata dataset** (`10.23636/rcm4-zk44`) | **CC-BY 4.0** — `rightsIdentifier: cc-by-4.0` | [API] DataCite, §3.6 |
| **Individual UK theses** | **Institution-dependent.** EThOS holds no files and asserts nothing about the university copies | [DOC] §3.3 |
| **theses.fr records** | Metadata is public; file licensing is per-institution | [INF] |
| Shodhganga, DiVA, TDX, ETH, Caltech, TU Delft | **Not verified individually** | **[NOT-VERIFIED]** |

**Note the asymmetry, because it is the useful finding:** the **metadata** is frequently CC-BY or
CC0 and bulk-downloadable, while the **documents** carry no licence at all. The British Library gave
away 709 MB of thesis metadata under CC-BY and gave away no theses. That asymmetry is the norm, and
it determines what you can legitimately build.

**Operational rules for this knowledge base:**

1. **Link and cite; do not mirror.** A thesis PDF in `archive/` is very likely a redistribution the
   licence does not permit. Record the handle/DOI and the byte size instead — which is what this
   record does throughout.
2. **Check `dc.rights` before assuming reuse rights.** It is in the DSpace REST API for free (§5.2).
   No `dc.rights` field means "no licence stated", which means **all rights reserved**, not "public
   domain".
3. **Quoting is fine; wholesale extraction may not be.** Quoting a paragraph or a figure with
   attribution is ordinary scholarly use. Bulk-harvesting a thousand thesis PDFs to build a
   derivative corpus is a licence question, and for most of the repositories above the answer is not
   yes.
4. **Metadata is the reusable layer.** OAI-PMH records, DataCite metadata and the EThOS CSV are
   explicitly reusable. Build on those.
5. **Where a thesis *does* carry a CC licence, it will say so** — and increasingly they do, because
   funder open-access mandates propagate to theses. Check; do not assume in either direction.

---

## 9. LANDMARK THESES — verified

The thesis-shaped parallel to [`landmark-papers.md`](landmark-papers.md), and held to the same
standard stated in [`README.md § Evidence and method`](README.md#evidence-and-method) rule 5:
**every identifier below was individually retrieved from its repository's API or abstract page on
2026-09-04, and the title machine-checked against the response. Candidates that could not be
confirmed were dropped, not softened** — §9.4 lists them by name.

**26 entries verified.**

### 9.1 Foundational — the documents that made the field

| # | Thesis | Author | Degree · Institution · Year | Identifier | Verified how | Why it matters |
|---|---|---|---|---|---|---|
| 1 | **A symbolic analysis of relay and switching circuits** | Claude Elwood Shannon | **M.S.**, MIT, Dept. of Electrical Engineering · MIT record says **1940**; universally cited as **1937** | **`hdl:1721.1/11173`** · <https://hdl.handle.net/1721.1/11173> | MIT DSpace REST [API] | **The single most consequential thesis in the history of digital electronics.** Establishes the correspondence between Boolean algebra and relay contact networks — the theoretical basis of every digital circuit since. 69 leaves. **Advisor: Frank L. Hitchcock.** OCLC 34541425. See §5.2 for the 1937/1940 date conflict |
| 2 | **Sketchpad, a man-machine graphical communication system** | Ivan Edward Sutherland | **PhD**, MIT, **1963** (dissertation submitted January 1963) | **`hdl:1721.1/14979`** · and republished as **`UCAM-CL-TR-574`**, DOI **`10.48456/tr-574`** | MIT DSpace REST [API] + Cambridge CL abstract page [WEB] | Interactive computer graphics, constraint solving, object-instance hierarchies, the light pen. **The Cambridge Computer Laboratory republished it in September 2003 as a 149-page technical report with a new preface by Alan Blackwell and Kerry Rodden** — the report page states it "is based on a dissertation submitted January 1963 … to the Massachusetts Institute of Technology". Cross-link: [companion record §3.5](government-and-institutional-technical-reports.md) |
| 3 | **Implementation of a list processing machine** | Thomas F. Knight | MIT, **1979** · advisor **Marvin L. Minsky** | **`hdl:1721.1/16033`** | MIT DSpace REST [API] | The MIT **Lisp Machine**. Tagged architecture, hardware type-checking, microcoded list processing — the design lineage behind Symbolics and LMI, and a primary source for hardware support of dynamic languages |
| 4 | **RABBIT: A Compiler for SCHEME** | Guy Lewis Steele, Jr. | MIT, **1978-05-01** | **`hdl:1721.1/6913`** | MIT DSpace REST [API] | The document that established **proper tail calls, continuation-passing style as a compiler IR, and "lambda: the ultimate…"** as engineering practice rather than theory. Every functional-language compiler descends from it |
| 5 | **The connection machine** | William Daniel Hillis | **PhD**, MIT, **1988** · advisor **Gerald Sussman** | **`hdl:1721.1/14719`** · (the 1981 AI Memo precursor is `hdl:1721.1/5679`, "The Connection Machine", 1981-09-01) | MIT DSpace REST [API] | Massively parallel SIMD architecture; the CM-1/CM-2. The thesis and the 1981 AI Memo sit **in the same repository under the same handle prefix**, which is §5.2's point about MIT filing theses and reports together |

### 9.2 Computer architecture, VLSI and the Mead/Seitz lineage

| # | Thesis | Author | Degree · Institution · Year | Identifier | Verified how | Why it matters |
|---|---|---|---|---|---|---|
| 6 | **Design of the RISC-V Instruction Set Architecture** | Andrew Waterman | **PhD**, UC Berkeley, **2016-01-03** | **`UCB/EECS-2016-1`** | Wayback replay, magic-byte-checked PDF **959,927 B, `%PDF-1.4`** [WEB via Wayback] | **The design rationale for RISC-V**, which exists in no conference paper. Already verified in [`government-and-institutional-technical-reports.md` §3.1](government-and-institutional-technical-reports.md) and re-verified here at the identical byte size. ⚠ **Its canonical URL 404s as of 2026-09-04 — see §5.4** |
| 7 | **Improving Energy Efficiency and Reducing Code Size with RISC-V Compressed** | Andrew Waterman | **MS thesis**, UC Berkeley, **2011-05-13** (advisors Patterson & Asanović) | **`UCB/EECS-2011-63`** | [companion record §3.1](government-and-institutional-technical-reports.md), Wayback [WEB] | The RVC compressed-instruction design. **The department's own generated BibTeX types it `@mastersthesis`** — the cleanest single proof that Berkeley's report series *is* its thesis series |
| 8 | **A VLSI Architecture for Concurrent Data Structures** | William James Dally | **PhD** (Dissertation), Caltech, **1986** | **DOI `10.7907/f8d5-x741`** | DataCite REST, prefix `10.7907` [API] | Concurrent data structures in silicon; the direct ancestry of modern **network-on-chip** and message-passing multicomputer design. Chuck Seitz's group, Mead-lineage Caltech VLSI |
| 9 | **The Torus Routing Chip** | William J. Dally, Charles L. Seitz | Caltech technical note, **1986** | **DOI `10.7907/99gpd-5kg37`** | DataCite REST [API] | **Wormhole routing.** Listed here because it is the companion report to entry 8 and is *the* primary source for the interconnect technique used in essentially every modern many-core and HPC fabric |
| 10 | **VLSI analogs of neuronal visual processing: a synthesis of form and function** | Misha Mahowald | **PhD** (Dissertation), Caltech, **1992** | **DOI `10.7907/4bdw-fg34`** · (a `Technical note` twin exists at `10.7907/z9cz35cd`) | DataCite REST [API] | **The silicon retina.** Carver Mead's student; the founding document of **neuromorphic engineering** and of address-event representation. One of the clearest cases in this record of a thesis being the complete work and the papers being fragments |
| 11 | **Accurate and precise computation using analog VLSI, with applications to computer graphics and neural networks** | David B. Kirk | **PhD** (Dissertation), Caltech, **1993** | **DOI `10.7907/1ykm-yq27`** | DataCite REST [API] | Analog VLSI precision engineering, by the person who later became NVIDIA's Chief Scientist. A direct bridge from Mead-lineage analog VLSI to modern GPU computing |
| 12 | **Performance analysis and optimization of asynchronous circuits** | Steven Morgan Burns | **PhD** (Dissertation), Caltech, **1991** | **DOI `10.7907/kez1-7q52`** | DataCite REST [API] | Alain Martin's **quasi-delay-insensitive asynchronous VLSI** programme. The performance-analysis framework for clockless design |
| 13 | **A General Approach to Performance Analysis and Optimization of Asynchronous Circuits** | Tak Kwan Lee | **PhD** (Dissertation), Caltech, **1995** | **DOI `10.7907/ehzs-y537`** | DataCite REST [API] | Continues entry 12; the standard reference for asynchronous-circuit timing analysis |
| 14 | **Energy-delay complexity of asynchronous circuits** | Paul Ivan Pénzes | **PhD** (Dissertation), Caltech, **2002** | **DOI `10.7907/9jpj-5s67`** | DataCite REST [API] | Energy–delay product as a first-class design objective for clockless logic — the argument that made asynchronous design an energy story rather than a timing story |
| 15 | **The architecture and programming of a fine-grain multicomputer** | Jakov N. Seizovic | **PhD** (Dissertation), Caltech, **1994** | **DOI `10.7907/53vc-hs15`** | DataCite REST [API] | Caltech Mosaic; fine-grain message-passing multicomputers. Direct ancestry of modern manycore |
| 16 | **Large operand division and an asynchronous approach to fault detection** | Kathleen A. Kramer | **PhD** (Dissertation), Caltech, **1991** | **DOI `10.7907/pt8p-9g83`** | DataCite REST [API] | Arithmetic hardware and self-checking logic in the same asynchronous programme |

### 9.3 Hardware security, memory systems and modern systems software

| # | Thesis | Author | Degree · Institution · Year | Identifier | Verified how | Why it matters |
|---|---|---|---|---|---|---|
| 17 | **Semi-invasive attacks – A new approach to hardware security analysis** | Sergei P. Skorobogatov | **PhD**, University of Cambridge, **Darwin College**; dissertation submitted **September 2004**, issued as a technical report **April 2005**, **144 pages** | **`UCAM-CL-TR-630`**, DOI **`10.48456/tr-630`** · PDF **11,754,717 B** | Cambridge CL abstract page [WEB] + PDF `content-type: application/pdf`, 11,754,717 B [WEB] | **The foundational document of optical fault injection and semi-invasive chip attack methodology.** Decapsulation, laser parameters, per-chip results — everything the CHES/FDTC papers had to cut. Directly relevant to [`cryptology-eprint-archive.md` §7.6](cryptology-eprint-archive.md) |
| 18 | **Improving DRAM Performance, Reliability, and Security by Rigorously Understanding Intrinsic DRAM Operation** | Hasan Hassan | **PhD** (Dissertation), **ETH Zürich**, **2022** | **DOI `10.3929/ethz-b-000601914`** | DataCite REST, prefix `10.3929` [API] | SAFARI group (Onur Mutlu). DRAM characterisation infrastructure and intrinsic-behaviour measurement — the apparatus behind a decade of DRAM papers |
| 19 | **Enabling Efficient and Scalable DRAM Read Disturbance Mitigation via New Experimental Insights into Modern DRAM Chips** | A. Giray Yağlıkçı | **PhD** (Dissertation), **ETH Zürich**, **2024** | **DOI `10.3929/ethz-b-000691009`** | DataCite REST [API] | The **RowHammer lineage** in long form. [`landmark-papers.md` §1](landmark-papers.md) records that the original RowHammer paper is **not on arXiv**; this is the deep version of that line of work |
| 20 | **Principled DRAM Security against Rowhammer Attacks** | Michele Marazzi | **PhD** (Dissertation), **ETH Zürich**, **2024** | **DOI `10.3929/ethz-b-000698237`** | DataCite REST [API] | In-DRAM target-row-refresh analysis (PROTRR, REGA, ZenHammer lineage). The mitigation side of entry 19 |
| 21 | **Enabling Effective Error Mitigation in Memory Chips That Use On-Die Error-Correcting Codes** | Minesh Patel | **PhD** (Dissertation), **ETH Zürich**, **2021** | **DOI `10.3929/ethz-b-000542542`** | DataCite REST [API] | On-die ECC and its interaction with error characterisation — the reason modern DRAM reliability measurements are hard to interpret |
| 22 | **REFault: A Fault Injection Platform for Rowhammer Research on DDR5 Memory** | Stefan Gloor | **Bachelor Thesis**, **ETH Zürich**, **2023** | **DOI `10.3929/ethz-b-000722911`** | DataCite REST [API] | Included deliberately. **A bachelor's thesis documenting a DDR5 fault-injection platform is a more useful engineering document than most conference papers on the topic** — §5.5's point about not filtering by degree level |
| 23 | **Improving DRAM Performance, Security, and Reliability by Understanding and Exploiting DRAM Timing Parameter Margins** | Jeremie Kim | **PhD** (Thesis), **Carnegie Mellon University**, **2020** | **DOI `10.1184/r1/13318703`** (version DOI `…13318703.v1`) | DataCite REST, prefix `10.1184` [API] | The CMU half of the same DRAM programme. **Note the concept/version DOI pair** — the figshare version-counting trap recorded in [`retrieval-notes.md` §7](retrieval-notes.md) applies to KiltHub |
| 24 | **Techniques for Shared Resource Management in Systems with Throughput Processors** | Rachata Ausavarungnirun | **PhD** (Thesis), **Carnegie Mellon University**, **2017** | **DOI `10.1184/r1/6723512`** | DataCite REST [API] | GPU memory-system and shared-resource management; the long form of a body of MICRO/ISCA work |
| 25 | **Linux: a Portable Operating System** | **Linus Torvalds** | **Master of Science thesis**, **University of Helsinki**, Department of Computer Science, **31 January 1997**, **52 pages** | **No repository identifier.** PDF at `https://www.cs.helsinki.fi/u/kutvonen/index_files/linus.pdf` — **HTTP 200, 470,861 bytes, `%PDF-1.3`** | Direct PDF retrieval; **title, author, date, degree, page count and keywords extracted from the PDF's own title page and Finnish/Swedish/English abstract form** [WEB] | Torvalds's account of making Linux portable — the Alpha and SPARC ports, and the architectural abstractions that made Linux multi-architecture. Keywords on the abstract form: *"Linux, Operating System, Portability, Alpha, Sparc"*. **⚠ It is NOT in Helda, the University of Helsinki institutional repository** — two separate DSpace REST searches (`"Linux portable operating system Torvalds"`, `"Torvalds"`, 3 and 77 hits) returned it in neither. **It survives on a professor's departmental home page.** §5.8 step 6 exists because of this case, and it is the top `web.archive.org/save/` candidate in §13 |
| 26 | **Abstraction in technical computing** | Jeffrey Werner Bezanson | **PhD**, MIT, **2015** · advisor **Alan Edelman** | **`hdl:1721.1/99811`** · (the 2012 master's, **"Julia: an efficient dynamic language for technical computing"**, is **`hdl:1721.1/74897`**, same advisor) | MIT DSpace REST [API] | **The Julia language**, documented in full. The PhD is the design argument — multiple dispatch, type inference over a dynamic language, the "two-language problem" — at a depth the papers do not reach. Two theses, one language: the master's is the implementation, the PhD is the theory |

### 9.4 Dropped — could not be confirmed

Listed by name, per README rule 5. **These are not claims of absence**; they are claims that this
pass did not verify them.

| Candidate | What was tried | Result |
|---|---|---|
| **Daniel Gruss, PhD, TU Graz** (Spectre/Meltdown lineage) | TU Graz Pure (`graz.elsevierpure.com`, **403 Cloudflare**), `diglib.tugraz.at`, CORE full-text search, DataCite by creator name | **Only the published dissertation *summary* was verified: `10.1515/itit-2018-0034`, "Software-based microarchitectural attacks", *it – Information Technology*, De Gruyter, 2018-11-20 [API Crossref].** That is a ~4-page digest, **not the thesis.** Full dissertation **[NOT-VERIFIED]** |
| **Moritz Lipp, PhD, TU Graz** | DataCite by name, CORE | 0 hits. **[NOT-VERIFIED]** |
| **Jo Van Bulck / KU Leuven COSIC theses** | Lirias (`lirias.kuleuven.be` → Primo SPA, no API found), CORE | CORE returned his **papers** (SGX-Step, Plundervolt, Foreshadow lineage) but no thesis record. **[NOT-VERIFIED]** |
| **Yuval Yarom-adjacent side-channel theses** | Not systematically searched within budget | **[NOT-VERIFIED]** |
| **Onur Mutlu's own PhD** (UT Austin, 2006) | Not probed — UT Austin's repository was not reached in this pass | **[NOT-VERIFIED]**. The ETH theses he *supervised* (entries 18–21) are verified |
| **Yoongu Kim, PhD, CMU** (original RowHammer author) | DataCite `creators.name:"Kim, Yoongu" AND types.resourceType:Thesis`, prefix `10.1184` → **0 hits** (his *papers* are in KiltHub as "Journal contribution") | **[NOT-VERIFIED]** |
| **David Patterson-advised Berkeley RISC theses** | Berkeley EECS TR series **404s** (§5.4); eScholarship returned **HTTP 202 / 0 bytes** | **[NOT-VERIFIED].** The only Berkeley entries here (6, 7) come from Wayback |
| **Additional Carver Mead direct-student theses** beyond Mahowald and Kirk | DataCite prefix `10.7907` topic queries returned mostly biology-retina false positives | Not individually confirmed. **[NOT-VERIFIED]** |
| **Jay Forrester, MIT** (magnetic core memory) | MIT DSpace query returned no plausible match in the top hits | **[NOT-VERIFIED]** |

### 9.5 What the table shows

**Three observations that were not obvious before assembling it.**

**One: 4 of 26 entries are not in a thesis repository at all.** Entries 2 (partly), 6, 7, 9 and 17
are **technical reports**, and entry 25 is a PDF on a personal page. That is ~20% of the most
important theses in computing living outside the thesis infrastructure entirely. **A search
restricted to "theses" collections misses them.** This is the strongest possible argument for
reading this record and
[`government-and-institutional-technical-reports.md`](government-and-institutional-technical-reports.md)
as one document.

**Two: the identifier types are completely heterogeneous.** Handles (`1721.1/…`), DataCite DOIs
(`10.7907/…`, `10.3929/…`, `10.1184/…`), Cambridge's own DOI prefix (`10.48456/tr-…`), Berkeley
report numbers (`UCB/EECS-…`), a French NNT, an EThOS ID, and — for Torvalds — **nothing at all**.
There is no universal thesis identifier and there is not going to be one. Cite whatever the holding
institution mints, and record the institution.

**Three: the modern entries all have DOIs and the historical ones mostly do not.** Everything from
2020 onward in this table (18–23) carries a DataCite DOI assigned at deposit. Everything before
1995 is handle-based or has an identifier retrofitted decades later (Caltech's `10.7907` prefix
covers 1985 technical notes — clearly a retrospective minting exercise, and a good one). **The
durability outlook for theses deposited today is materially better than for the historical corpus**
— which makes §5.4's Berkeley failure, affecting the *un*-DOI'd historical series, the more urgent
problem.

---

## 10. Access, APIs and bulk retrieval

### 10.1 The hierarchy that actually works

Ordered by how reliably each answered during this pass:

| Rank | Route | Why | Verified on |
|---|---|---|---|
| **1** | **DSpace 7 REST** — `GET /server/api/discover/search/objects?query=…&size=…` | Full JSON, **including `dc.contributor.advisor` and `dc.rights`**. No key. Answers **from behind an Anubis wall** | `dspace.mit.edu`, `helda.helsinki.fi`, `bl.iro.bl.uk` |
| **2** | **DataCite REST** — `api.datacite.org/dois?query=…&prefix=…` | Works when the repository does not. Filter with `types.resourceType:Dissertation` / `:Thesis` | Caltech `10.7907`, ETH `10.3929`, CMU `10.1184`, BL `10.23636` |
| **3** | **OAI-PMH** | Open on hosts whose websites are walled. `resumptionToken/@completeListSize` gives you a count in one call | DiVA, DNB, ETH |
| **4** | **`hdl.handle.net/api/handles/<prefix>/<suffix>`** | JSON existence oracle, **immune to the target's bot wall** | TDX `10803`, MIT `1721.1` |
| **5** | **Purpose-built national APIs** | theses.fr, CiNii, HAL/TEL, CORE, OpenAIRE all answer plain `curl` | §2, §4 |
| **6** | **ResourceSync** | Rare, but EThOS's `resourcelist` is a complete 654,832-URL enumeration in one 88 MB response | `ethos.bl.uk` |
| **7** | **Bulk CC-BY dumps** | The EThOS CSV; OpenAlex's S3 snapshot | §3.6 |

### 10.2 Worked invocations

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

# --- DSpace 7: search any repository, get advisor + rights ------------------
curl -s -A "$UA" -G "https://dspace.mit.edu/server/api/discover/search/objects" \
     --data-urlencode 'query=connection machine Hillis' --data-urlencode 'size=5'
#   → _embedded.searchResult._embedded.objects[]._embedded.indexableObject
#       .handle, .uuid, .metadata['dc.contributor.advisor'], .metadata['dc.rights']

# --- DataCite: theses by prefix and type ------------------------------------
curl -s -G "https://api.datacite.org/dois" \
     --data-urlencode 'query=DRAM AND types.resourceType:Dissertation' \
     --data-urlencode 'prefix=10.3929' --data-urlencode 'page[size]=10'

# --- OAI-PMH: identify, then count via completeListSize ---------------------
curl -s "https://www.diva-portal.org/dice/oai?verb=Identify"
curl -s "https://www.diva-portal.org/dice/oai?verb=ListIdentifiers&metadataPrefix=oai_dc" \
  | grep -o 'completeListSize="[0-9]*"'          # → 800381

# --- Handle existence oracle (works through Cloudflare) ---------------------
curl -s "https://hdl.handle.net/api/handles/10803/1234"      # responseCode 1  = exists
curl -s "https://hdl.handle.net/api/handles/10803/99999999"  # responseCode 100 = absent

# --- theses.fr (France) -----------------------------------------------------
curl -s "https://theses.fr/api/v1/theses/recherche/?q=*&nombre=1"        # 564318
curl -s "https://theses.fr/api/v1/personnes/recherche/?q=Asanovic&nombre=5"
curl -s "https://theses.fr/api/v1/theses/these/2016PA066033"

# --- TEL via HAL (France, full text) ---------------------------------------
curl -s 'https://api.archives-ouvertes.fr/search/tel/?q=domainAllCode_s:"spi.tron"&rows=0&wt=json'

# --- CiNii Dissertations (Japan) — NOTE the mandatory date range ------------
curl -s "https://cir.nii.ac.jp/opensearch/dissertations?format=json&count=1&from=1900"

# --- CORE (largest queryable thesis index) — NOTE the trailing slash --------
curl -s -G "https://api.core.ac.uk/v3/search/works/" \
     --data-urlencode 'q=documentType:"thesis" AND "RISC-V"' --data-urlencode 'limit=5'

# --- OpenAIRE type facets ---------------------------------------------------
curl -s "https://api.openaire.eu/search/publications?instancetype=Doctoral+thesis&size=1&format=json"

# --- EThOS: complete record enumeration (88 MB) -----------------------------
curl -s -A "$UA" "https://ethos.bl.uk/capabilitylist?locale=en"
curl -s -A "$UA" "https://ethos.bl.uk/resourcelist" -o ethos-resourcelist.xml

# --- EThOS: the 709 MB CC-BY bulk metadata CSV ------------------------------
curl -s "https://api.datacite.org/dois/10.23636/rcm4-zk44"
curl -s "https://bl.iro.bl.uk/server/api/core/items/ef18a65d-a839-428b-abbc-2da178007e4e/bundles"
curl -sL -H 'Range: bytes=0-3000' \
  "https://bl.iro.bl.uk/server/api/core/bitstreams/a10353df-67a5-4d47-9d33-4c764f605eb5/content"
```

### 10.3 Negative controls — every probe pattern used in this record

Per [README rule 3](README.md#evidence-and-method): a 200 does not mean the document exists.

| Host / pattern | Real | Bogus | Trustworthy? |
|---|---|---|---|
| `dspace.mit.edu/handle/1721.1/<n>` | **200**, 552,361 B | **404**, 444,910 B | ✅ **status yes, byte size no** (both are large Angular shells) |
| MIT DSpace REST `?query=` | `totalElements` > 0 | **`totalElements: 0`** | ✅ clean |
| `api.datacite.org/dois/<doi>` | 200 | **404, 87 B** | ✅ clean |
| `hdl.handle.net/api/handles/<h>` | `responseCode: 1` | **`responseCode: 100`** | ✅ **best oracle in this record** |
| `ethos.bl.uk/concern/thesis_or_dissertations/<n>` | 200, 69,494 B | **404, 1,676 B** | ✅ clean |
| **`ethos.bl.uk/OrderDetails.do?uin=…`** | 200 → redirect to record | ⚠ **200, 62,214 B — silently the home page** | ❌ **no negative signal** |
| **`theses.fr/api/v1/theses/these/<NNT>`** | 200, full JSON | ⚠ **200, zero-byte body** | ❌ **status useless; test body length** |
| `cir.nii.ac.jp/opensearch/dissertations?q=` | > 0 | 0 for a bogus term — ✅ — **but also 0 with no parameters** | ⚠ **the empty-query trap** |
| `api.core.ac.uk/v3/search/works/` | JSON | — | ⚠ **`/works` without the slash → 200 + Cloudflare HTML redirect, not JSON** |
| `api.openaire.eu/search/publications?type=…` | — | **400 + an enumeration of valid parameters** | ✅ **exemplary** |
| **any OAI-PMH `verb=`** | 200 + data | ⚠ **200 + an `<error>` element** (ETH: 200, 488 B) | ❌ **OAI-PMH signals errors in the body, never in the status. By design** |
| `hdl` on Cloudflare-walled TDX | works | works | ✅ routes around the wall |

### 10.4 Bulk retrieval — what is actually available

| Dump | Size | Licence | Contents |
|---|---|---|---|
| **`EThOS_CSV_202310.csv`** (DOI `10.23636/rcm4-zk44`, handle `britishlibrary-iro/19931`) | **709,733,446 B** | **CC-BY 4.0** | ~650,000 UK doctorates: Title, DOI, Author, Author ISNI, ORCID, Institution, Institution ISNI, Date, Qualification, Abstract, **Subject Discipline**, **Supervisor(s)**, **Funder(s)**, EThOS URL, **IR URL** |
| **EThOS ResourceSync `resourcelist`** | **88,402,587 B** | — | 654,832 record URLs + `lastmod` |
| DiVA OAI-PMH full harvest | not measured | — | 800,381 records, `deletedRecord=persistent` |
| DNB OAI-PMH | not measured | — | `earliestDatestamp` 1945 |
| ETH OAI-PMH | not measured | — | `earliestDatestamp` 2017-05-15 (platform migration, **not** a coverage floor) |
| **NDLTD union-catalogue OAI-PMH** | — | — | ❌ **HTTP 503. Gone** |
| **OATD bulk** | — | — | ❌ **None advertised; site is Cloudflare-walled including `robots.txt`** |

**The EThOS CSV deserves emphasis as the single best bulk artefact in this record.** It is the only
large, openly-licensed, supervisor-bearing thesis dataset this survey located. It makes §5.8's
technique work offline for an entire country, and it survived the destruction of the service that
produced it (§3.6).

### 10.5 Rate limits and courtesy

- **Internet Archive is the binding constraint**, exactly as
  [`retrieval-notes.md` §2](retrieval-notes.md) records. This pass hit `000`-flapping again on
  replay fetches while the CDX endpoint continued to answer for a while. **Retry a CDX query at
  least twice before recording "no captures", and use `id_` replay sparingly.**
- **DataCite, Crossref, Handle.net, OpenAIRE, CORE, theses.fr, CiNii, HAL and the DSpace REST APIs
  all answered plain `curl` without complaint** during this pass. None required a key. Be polite
  anyway.
- **`shodhganga.inflibnet.ac.in` is slow (13–21 s) and drops roughly one request in four.** Set a
  long timeout and retry rather than concluding it is down (§4.7).
- **ETH's block is IP/provider-scoped and self-documenting** — it names a contact address (§5.5).
  Use it rather than rotating agents.
- **Anubis-walled hosts cannot be persuaded.** `theses.hal.science`, `portal.dnb.de`, `rcaap.pt`,
  `trove.nla.gov.au`, `helda.helsinki.fi`, `base-search.net`. Go to the API, and if there is no
  API (RCAAP) accept the gap.

---

## 11. A practical recipe

Copy-pasteable. Two entry points.

### 11.1 "I have a paper and I want the long version"

```
 1. Identify the student.
    Usually the first author. Take the AFFILIATION FROM THE EARLIEST PAPER
    in that line of work — that is where they were a student.

 2. Identify the advisor.
    Usually the last author, or the known head of the group.

 3. Estimate the year.
    Year of the last first-author paper in the line, + 0 or 1.

 4. Query the institution's repository REST API by SURNAME, not by title:
      curl -s -G "https://<repo>/server/api/discover/search/objects" \
           --data-urlencode "query=<student surname>" --data-urlencode "size=50"
    Look for dc.contributor.advisor to confirm you have the right person.
    (Works on any DSpace 7 install; MIT and Helda verified.)

 5. If the repository is walled or you do not know it, go to DataCite:
      curl -s -G "https://api.datacite.org/dois" \
           --data-urlencode 'query=creators.name:"<Surname, Given>" AND types.resourceType:Dissertation' \
           --data-urlencode 'page[size]=20'
    Add --data-urlencode 'prefix=10.XXXX' if you know the institution's prefix:
      Caltech 10.7907 · ETH Zurich 10.3929 · CMU 10.1184 · British Library 10.23636
      Cambridge CL 10.48456 · theses.fr 10.70675

 6. Country-specific shortcuts:
      France   curl -s "https://theses.fr/api/v1/theses/recherche/?q=<name>&nombre=20"
               curl -s "https://theses.fr/api/v1/personnes/recherche/?q=<advisor>&nombre=5"
      France (full text, incl. HDR)
               curl -s 'https://api.archives-ouvertes.fr/search/tel/?q=authFullName_s:"<name>"&wt=json'
      UK       grep the 709 MB EThOS CSV on Supervisor(s) or Author, then follow the IR URL column
               (or search https://ethos.bl.uk/ ; legacy OrderDetails.do?uin=uk.bl.ethos.<n> still resolves)
      Japan    curl -s "https://cir.nii.ac.jp/opensearch/dissertations?q=<name>&format=json&from=1900"
      Sweden   DiVA OAI-PMH, or the diva-portal.org web search
      India    https://shodhganga.inflibnet.ac.in/ — browse by "Researcher/Guide"
      Germany  the university repository directly; DNB OAI at services.dnb.de/oai/repository

 7. Cross-institution fallbacks, in order:
      CORE      curl -s -G "https://api.core.ac.uk/v3/search/works/" \
                     --data-urlencode 'q=documentType:"thesis" AND "<phrase>"' --data-urlencode 'limit=10'
                (NOTE the trailing slash on /works/)
      OpenAIRE  https://api.openaire.eu/search/publications?instancetype=Doctoral+thesis&title=<...>&format=json
      OATD      https://oatd.org/  — browser only; 403s every automated client
      BASE      https://www.base-search.net/  — browser only; Anubis proof-of-work

 8. If it is not in a "theses" collection, look in the TECHNICAL REPORT series:
      Cambridge CL   https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-<n>.pdf   (DOI 10.48456/tr-<n>)
      CMU SCS        http://reports-archive.adm.cs.cmu.edu/
      MIT AI Memos   dspace.mit.edu handle 1721.1/5460
      Berkeley EECS  UCB/EECS-<year>-<n>  ⚠ URLs 404 since ~2026-08 — use the Wayback Machine:
        http://web.archive.org/web/2022id_/https://www2.eecs.berkeley.edu/Pubs/TechRpts/<year>/EECS-<year>-<n>.pdf

 9. Still nothing? Check the personal page.
      site:<dept domain> ~<surname>   — Torvalds's thesis lives at
      https://www.cs.helsinki.fi/u/kutvonen/index_files/linus.pdf and nowhere institutional.
      If you find one, submit it to https://web.archive.org/save/ (AGENTS.md rule 9).

10. Record has no file? It is probably an EMBARGO, not a dead link (§8.2).
      Look for dc.date.available in the future; use the repository's "request a copy" button;
      re-check in a year; email the author.
```

### 11.2 "I have an author name and nothing else"

```
 1. Resolve the person, not the string.
      ORCID     https://pub.orcid.org/v3.0/expanded-search/?q=<name>   (public API)
      France    https://theses.fr/api/v1/personnes/recherche/?q=<name>&nombre=10
                → gives PPN, and role counts (directeur / rapporteur / examinateur)
      dblp      https://dblp.org/search/publ/api?q=<name>&format=json  (see open-access record)

 2. From any paper, take the earliest affiliation → institution.

 3. Run step 4/5 of §11.1 against that institution.

 4. If the person is a SUPERVISOR and you want their students:
      MIT-style:  search dc.contributor.advisor (§5.8)
      France:     theses.fr /personnes → the roles object counts their supervisions
      UK:         grep the EThOS CSV Supervisor(s) column
      India:      Shodhganga "Researcher/Guide" browse

 5. Verify before citing.
      Retrieve the record. Check degree, institution, and year of award.
      Check dc.rights before reusing anything (§8.3).
      Cite the handle / DOI / NNT / report number — never the URL (§5.4 is why).
```

---

## 12. Retrieval notes — new fingerprints and traps from this pass

Staged for [`retrieval-notes.md`](retrieval-notes.md) and thence
[`ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md), per `AGENTS.md`
rule 8. Nothing below was obtained by bypassing authentication or an access control.

### 12.1 New block fingerprints

| Fingerprint | Product | Hosts observed (2026-09-04) |
|---|---|---|
| **HTTP 403, ~1,337 B, `<title>Access Restricted</title>`, inline Segoe-UI CSS, contact `research-collection@library.ethz.ch`, text *"temporarily restricted from your location / your provider"*, spelling *"accidentially"*** | **Custom, IP/provider-scoped** — **NEW** | `www.research-collection.ethz.ch` REST API |
| HTTP 403, **5,207–6,102 B**, `<title>Just a moment...</title>` | Cloudflare managed challenge (extends the ~5.58–5.62 kB range already recorded) | `oatd.org` (5,207–5,821, **incl. `robots.txt`**) · `tdx.cat` (5,658–5,769) · `ethos.bl.uk/catalog*` (5,757–5,905) · `recherche-collection-search.bac-lac.gc.ca` (5,775) · `graz.elsevierpure.com` (6,102) |
| HTTP 200, **4,262–12,607 B**, `<title>Making sure you're not a bot!</title>`, `/.within.website/x/xess/xess*.css?cachebuster=<ver>` | **Anubis proof-of-work — now endemic in the ETD layer** | `theses.hal.science` (12,607, `devel`) · `portal.dnb.de` (4,475, `1.25.0`) · `rcaap.pt` (4,511, `v1.26.0-pre2`) · `trove.nla.gov.au` (7,745, `v1.26.2`) · `helda.helsinki.fi` (4,262, `1.23.0`) · `base-search.net` (7,846, `v1.27.0+dirty`) · `dans.knaw.nl` (4,437, `1.25.0`) |
| HTTP 200, 1,697 B, `<title>Verificando conexão \| Oasisbr</title>` | Brazilian challenge page — **NEW** | `bdtd.ibict.br` |
| HTTP 503, **505 B**, stock nginx *"503 Service Unavailable"* | Backend down behind a live proxy | `search.ndltd.org`, `union.ndltd.org` |
| **HTTP 202, 0 bytes** | figshare/eScholarship non-answer (already recorded for `figshare.com`, `kilthub.cmu.edu`) — **now also** | `escholarship.org` |

**The headline: Anubis has spread from scholarly publishers to national libraries.**
[`retrieval-notes.md` §3](retrieval-notes.md) listed seven hosts. This pass adds seven more,
including **three national libraries** (DNB, NLA/Trove, DANS) and **the French national thesis
archive**. Its finding stands and hardens: **no user agent defeats it; find the API.** With one new
exception — **`rcaap.pt` puts its OAI-PMH endpoint behind the wall too**, the first host where the
escape hatch failed.

### 12.2 New soft-200s and API traps

| Host / pattern | Behaviour | Consequence |
|---|---|---|
| **`ethos.bl.uk/OrderDetails.do?uin=uk.bl.ethos.<bogus>`** | **HTTP 200, 62,214 B — the home page**, byte-identical to a successful `GET /` | A link-checker validating legacy EThOS citations reports **100% success regardless**. Validate against `/concern/thesis_or_dissertations/<n>`, which 404s honestly (1,676 B) |
| **`theses.fr/api/v1/theses/these/<bogus NNT>`** | **HTTP 200 with a zero-byte body** | Status code useless; JSON parser gets EOF. **Test body length** |
| **`api.core.ac.uk/v3/search/works`** *(no trailing slash)* | **HTTP 200 + a Cloudflare `cdn-cgi/content` `<meta refresh>` HTML page**, not JSON | Silent corruption. **Always use `/works/`** |
| **`cir.nii.ac.jp/opensearch/dissertations`** with no parameters | **`totalResults: 0`** — and `q=*` also returns 0 | **Third independent instance** of the empty-query trap after NASA NTRS and DOE OSTI. Use a wide `from=`/`until=` range |
| **Any OAI-PMH `verb=<bogus>`** | **HTTP 200** with an `<error>` element in the body (ETH: 200, 488 B) | By design in the protocol. **Never status-check OAI-PMH; parse the body** |
| **`shodhganga.inflibnet.ac.in` home page** | Live counter `697675` sits **beside a commented-out stale block reading `597316`** and a commented-out `99999` placeholder | **A tag-stripping extractor that does not strip HTML comments reads a figure 100,359 too low.** Strip comments first |
| **`web.archive.org/cdx`** | Returned a **negative `length` field**: `20250926194305 403 -6693296525` | A parser doing `int(length)` and summing will produce nonsense. **Validate CDX lengths ≥ 0** |
| `getent hosts catalogodeteses.capes.gov.br` | Returns **only the AAAA record**; an A record exists and is visible via `getent ahostsv4` | Makes an IPv4-reachable host look IPv6-only. **Check both families** |
| KiltHub / figshare DataCite records | Concept DOI and `.v1` version DOI both returned as separate hits | The version-vs-work inflation already recorded for Zenodo/OSF/TechRxiv applies to institutional figshare tenants |

### 12.3 Ladder notes

- **`shodhganga.inflibnet.ac.in` initially looked like a reversed ladder** (`curl/8.5.0` succeeded,
  Chrome-131 timed out) — **it did not reproduce.** Three subsequent Chrome requests gave
  `200 / 200 / 000` at 13.5–21.1 s. It is a **slow, intermittently-overloaded origin**, not a UA
  filter. Recorded because the wrong conclusion was one probe away, and it is the kind of thing that
  ends up in a table and never gets rechecked.
- **`www2.eecs.berkeley.edu` is no longer TCP-dead** — a change from
  [`retrieval-notes.md` §5](retrieval-notes.md), which recorded a timeout on :443 and :80 with all
  UAs on 2026-09-01/02. On 2026-09-04 it **answers and 302s** to `iris.eecs.berkeley.edu`. **The
  host recovered and the content did not** (§5.4).
- **No user-agent fallback was needed anywhere in this pass** except to confirm that fallbacks do
  not work: OATD 403s all five rungs, Anubis hosts are agent-agnostic by construction, and ETH's
  block is IP-scoped and says so. **The UA ladder solved nothing in this record.** What solved
  things was **changing protocol** — OAI-PMH, DataCite, Handle.net, DSpace REST.

---

## 13. Explicitly not verified, and what to do next

Listed so the gaps are visible rather than silent.

### 13.1 Could not verify

1. **OATD's current record count.** Cloudflare-403 on five UAs including `robots.txt`. The 7,407,210
   figure is from a 2025-03-04 Wayback capture and is **18 months stale**.
2. **DART-Europe's record count and participating-country count.** Portal closed 2025-02-03; the
   closure notice carries no figures. **A Wayback replay of the pre-closure front page is the
   obvious next probe and was not run.**
3. **BASE's thesis count and total size** — Anubis, no API found. Unverified across this whole
   survey.
4. **DiVA's doctoral-thesis-only count** — no publication-type OAI set; the web facet needs a JSF
   session.
5. **German dissertation count** — DNB OAI `Identify` gives no total; a `ListIdentifiers` walk was
   not run.
6. **TDX/TDR, RCAAP, Trove, RISS, CAPES, BDTD, TESEO, Tez Merkezi, Theses Canada counts** — all
   walled, unreachable or session-bound.
7. **CAPES reachability** — `000` on IPv4 and IPv6. Recorded as *unreachable from here*, **not** as
   dead.
8. **CNKI and Wanfang holdings** — paywalled; nothing measured.
9. **LA Referencia** — not probed at all.
10. **PQDT Open's current status.** The standalone host 302s into the main ProQuest platform.
    Whether a free full-text open subset still exists is unknown. **Do not cite PQDT Open as live.**
11. **EBSCO Open Dissertations' 2,000,000 / 325 figures** are EBSCO's claim, not a measurement.
12. **TU Graz dissertations of Daniel Gruss and Moritz Lipp** — Pure is Cloudflare-walled; only
    Gruss's 4-page De Gruyter dissertation *summary* (`10.1515/itit-2018-0034`) was verified.
13. **KU Leuven COSIC theses** — Lirias is a Primo SPA; no open API located.
14. **Onur Mutlu's own PhD** (UT Austin) and **Yoongu Kim's CMU PhD** — not found through the routes
    tried.
15. **Berkeley EECS reports beyond the six RISC-V documents**, and **whether the series has a new
    home**. eScholarship returned HTTP 202 / 0 bytes.
16. **Embargo rates anywhere.** No repository publishes one and no API exposes an embargo facet.
    The `dc.date.available` vs `dc.date.issued` differential is measurable in bulk over OAI-PMH and
    would be a genuinely novel contribution.
17. **Licence distribution across thesis repositories.** Only MIT's `dc.rights` was read directly.
18. **Google Scholar coverage of theses** — no API, terms forbid automated querying,
    `AGENTS.md` rule 7 applies. Permanently unverifiable by this method.
19. **The exact EThOS relaunch date.** Inferred as ~2026-04/05 from the `lastmod` histogram and the
    Wayback capture series; no announcement located.
20. **How many previously-digitised EThOS full texts are now unavailable anywhere.** No public
    statement quantifies it. This is the most consequential unquantified loss in the record.
21. **The Trove / Australasian Digital Theses absorption date and mechanism** — Trove is
    Anubis-walled.
22. **Whether `netherlands.openaire.eu` is the same object as DANS's "Portal of Research Output from
    the Netherlands"** (UKB/SURF).

### 13.2 Archival candidates — `AGENTS.md` rule 9

**None were submitted in this pass.** All meet the "scarce, valuable, fragile" bar; the first two
are urgent.

| Candidate | Why it qualifies |
|---|---|
| **`https://www.cs.helsinki.fi/u/kutvonen/index_files/linus.pdf`** | **The most urgent item in this record.** Linus Torvalds's master's thesis, verified **not** to be in the University of Helsinki's institutional repository. It exists as a 470,861-byte PDF on one professor's departmental page. A staff change or a site redesign ends it |
| **`https://www2.eecs.berkeley.edu/Pubs/TechRpts/<year>/EECS-<year>-<n>.pdf` for the six RISC-V reports** | Already 404 at origin (§5.4). Wayback holds them, but the captures date from 2017–2022 and the CDX shows patchy coverage. **Re-verify each of the six and save what is missing** |
| `https://ndltd.org/thesis-resources/find-etds/` | The only maintained country-by-country directory of national ETD services, on a WordPress site whose sibling search service has already gone to 503 |
| `https://ethos.bl.uk/about` and `/FAQs?locale=en` | The British Library's own account of what was lost and what was restored. Primary evidence for the most important durability case study in this directory |
| `https://dans.knaw.nl/en/data-services/narcis/` | DANS's discontinuation notice — the only primary source for NARCIS's 2023-07-03 end date. Already captured 2026-05-10; **re-check** |
| `https://www.ucl.ac.uk/library/dart-europe-e-theses-portal-has-closed-down` | UCL's DART-Europe closure notice. The only primary source for the 2025-02-03 date |

### 13.3 Corrections owed to sibling records

Not applied here — this pass wrote only its own file — but flagged for whoever next edits them.

1. **[`government-and-institutional-technical-reports.md` §3.1](government-and-institutional-technical-reports.md)**
   lists six canonical Berkeley EECS PDF URLs. **All six 404 as of 2026-09-04** (§5.4). The report
   *numbers* remain correct and the Wayback route works. The section's "unreachable from here"
   caveat should become "the URL grammar is gone".
2. **[`retrieval-notes.md` §5](retrieval-notes.md)** lists `www2.eecs.berkeley.edu` under
   "Unreachable by TCP, not by policy". **It now answers and 302s** (§12.3).
3. **[`retrieval-notes.md` §3](retrieval-notes.md)**'s Anubis table should gain seven hosts and the
   `rcaap.pt` exception where OAI-PMH is *also* walled (§12.1).
4. **[`closed-and-defunct-servers.md` §2.4](closed-and-defunct-servers.md)**'s domain-parking table
   should gain **Cybertesis** (`cybertesis.net` → a click-monetisation redirect, §4.9), and the
   record's failure taxonomy has no row for **catastrophic infrastructure destruction**, which
   EThOS supplies (§3.8).
5. **[`README.md` § Probing traps](README.md#6-probing-traps)** could gain the three strongest new
   entries: the **EThOS legacy-URL soft-200**, the **CORE trailing-slash Cloudflare redirect**, and
   the **HTML-comment stale-counter** trap.

---

## 14. Sources

All retrieved **2026-09-04** unless another date is stated. Raw probe output is under
[`../../archive/research/preprint-repositories/theses/`](../../archive/research/preprint-repositories/theses/).
"Chrome 131" = the rung-2 user agent from [`AGENTS.md`](../../AGENTS.md).

**Aggregation layer (§2)**

- **S1** `https://ndltd.org/` — HTTP 200, 135,318 B. NDLTD organisation site. [WEB]
- **S2** `https://search.ndltd.org/` and `https://union.ndltd.org/OAI-PMH/?verb=Identify` — both
  **HTTP 503, 505-byte stock nginx page**. Supports §2.2. [WEB/API]
- **S3** `http://web.archive.org/cdx/search/cdx?url=search.ndltd.org&…&from=2023` and
  `…?url=union.ndltd.org*&…&from=2022` — capture series showing 200s through 2025-05-16 and 301s
  from 2025-08-07; `union.ndltd.org/OAI-PMH/` last 200 on 2025-04-20. [WEB]
- **S4** `http://web.archive.org/web/20250516083247id_/http://search.ndltd.org/` — *"Search the
  **6,534,039** electronic theses and dissertations contained in the NDLTD archive"*. [WEB via Wayback]
- **S5** `https://ndltd.org/thesis-resources/find-etds/` — HTTP 200, 132,126 B. The country-by-country
  ETD directory; source for the §4 target list, the BASE "70 million documents in 3000 repositories"
  quote, and the Google Scholar annotation. [DOC]
- **S6** `https://oatd.org/` — HTTP 403 to Chrome 131 (5,442 B), `WhatsApp/2.23.20.0` (5,228 B),
  ClaudeBot (5,442 B), `curl/8.5.0` (5,207 B), Googlebot (5,292 B); `/robots.txt` 403 (5,493 B);
  `/oatd/search?q=…` with full browser Accept headers 403 (5,821 B). All Cloudflare
  "Just a moment…". [WEB]
- **S7** `http://web.archive.org/web/{20240401084504,20250101215435,20250304050453}id_/https://oatd.org/`
  — OATD's own counter: **7,421,247** / **7,206,043** / **7,407,210**; "over 1100 colleges,
  universities, and research institutions"; the operator's 2022-10-03 anti-crawler notice.
  [WEB via Wayback]
- **S8** `https://www.dart-europe.org/` → 200 after redirect to
  `https://www.ucl.ac.uk/library/dart-europe-e-theses-portal-has-closed-down` (22,863 B) — UCL's
  closure notice, *"closed down permanently on Monday 03 February 2025"*. [DOC]
- **S9** `https://api.core.ac.uk/v3/search/works/?q=documentType:"thesis"&limit=1` →
  `totalHits 7,921,188`; `?q=*` → `329,911,927`. Also the no-trailing-slash Cloudflare
  `cdn-cgi/content` redirect trap. [API]
- **S10** `https://www.base-search.net/Search/Results?lookfor=riscv&type=all` — HTTP 200, 7,846 B,
  Anubis `xess.min.css?cachebuster=v1.27.0+dirty`. [WEB]
- **S11** `https://api.openaire.eu/search/publications?instancetype={Doctoral+thesis,Master+thesis,Thesis}&size=1&format=json`
  → 3,158,600 / 2,661,863 / 2,525,725. Plus the HTTP 400 parameter-enumeration response to
  `?type=x`. [API]

**EThOS (§3)**

- **S12** `https://www.bl.uk/cyber-incident/` → 302 → `https://www.bl.uk/about/cyber-attack`,
  HTTP 200, 133,713 B — the British Library's own cyber-attack statement (October 2023 attack;
  November 2023 dark-web release; *"rebuild of our entire technology infrastructure"*; March 2024
  lessons-learned paper). [DOC]
- **S13** `http://web.archive.org/cdx/search/cdx?url=ethos.bl.uk&…&from=2023` — capture series:
  last pre-attack 2023-10-08; **no captures Nov 2023 – Feb 2024**; 307/308 monthly through 2026-02;
  302 from 2026-05. [WEB]
- **S14** `https://ethos.bl.uk/` — HTTP 200, 62,214 B. Hyku platform, "Platform provided by CoSector,
  University of London", *"now available again following restoration work"*, "over 650,000". [WEB]
- **S15** `https://ethos.bl.uk/about` — HTTP 200, 57,645 B. *"this platform is a metadata-only
  discovery service"*. [DOC]
- **S16** `https://ethos.bl.uk/FAQs?locale=en` — HTTP 200, 84,307 B. Procurement via public tender;
  ~14,000 theses added since the attack; **"Over 400,000 theses are openly available for download
  from university repositories"**; digitisation devolved to universities; "1700s onwards"; next
  phase later in 2026. *(Note: the site's own nav link `/faqs` lowercase returns **404, 1,676 B**;
  the working path is `/FAQs`.)* [DOC]
- **S17** `https://ethos.bl.uk/capabilitylist?locale=en` (200, 457 B) and
  `https://ethos.bl.uk/resourcelist` (**200, 88,402,587 B**, `at="2026-09-06T16:32:22Z"`) —
  **654,832** `<loc>` entries; ids 232,781–906,226; `lastmod` histogram. [API]
- **S18** `https://ethos.bl.uk/concern/thesis_or_dissertations/906226` (200, 69,494 B) — record
  shape, `uk.bl.ethos.906226`, the "no university copy" message. Negative controls:
  `/concern/…/99999999` → **404, 1,676 B**; `OrderDetails.do?uin=uk.bl.ethos.906226` → **200 →
  redirect to the record**; `OrderDetails.do?uin=uk.bl.ethos.99999999` → **200, 62,214 B home
  page**. [WEB]
- **S19** `https://api.datacite.org/dois?query=ethos&prefix=10.23636&page[size]=25` and
  `https://api.datacite.org/dois/10.23636/rcm4-zk44` — 15 EThOS-related DOIs; final dataset
  `10.23636/rcm4-zk44`, CC-BY 4.0, DataCite record created 2023-11-27T17:07:22Z, *"around 98% of all
  PhDs ever awarded by UK Higher Education institutions, dating back to 1787"*. [API]
- **S20** `https://bl.iro.bl.uk/server/api/core/items/ef18a65d-a839-428b-abbc-2da178007e4e`,
  `/bundles`, and `…/bitstreams/a10353df-67a5-4d47-9d33-4c764f605eb5/content` —
  handle `britishlibrary-iro/19931`; bitstream **`EThOS_CSV_202310.csv`, 709,733,446 B**; range
  fetch **HTTP 206, `content-type: text/csv`, `content-range: bytes 0-3000/709733446`**, delivered
  via a signed `cf002.cdn.4science.cloud` URL; column header and first data row quoted in §3.6.
  Also: the old `bl.iro.bl.uk/concern/datasets/<uuid>` URLs 302 to `entities/product/<uuid>` —
  the BL repository migrated Hyrax → DSpace-CRIS. [API]

**National and regional systems (§4)**

- **S21** `https://theses.fr/api/v1/theses/recherche/?q=*&nombre=1` → **564,318**;
  `/personnes/recherche/` → **918,602**; `/theses/these/2016PA066033` → full record incl. DOI
  `10.70675/ff0868d0z67ecz4e1bzb948zaa766df489f9`; `q=RISC-V` → 102; bogus NNT → **200, 0 bytes**.
  [API]
- **S22** `https://api.archives-ouvertes.fr/search/tel/?q=*:*&rows=0&wt=json` → **180,693**;
  `facet.field=docType_s` → THESE 171,839 / HDR 8,854; `domainAllCode_s` facet and the 16
  per-domain counts in §4.2. [API]
- **S23** `https://www.diva-portal.org/dice/oai?verb={Identify,ListSets,ListIdentifiers}` —
  `earliestDatestamp` 1900-01-01, `deletedRecord=persistent`,
  `resumptionToken completeListSize="800381"`, set list. Web search attempt → 4,481-byte stub.
  [API]
- **S24** `https://portal.dnb.de/opac.htm` (200, 4,475 B, Anubis `1.25.0`) and
  `https://services.dnb.de/oai/repository?verb=Identify` (200, 779 B, *"OAI-Repository of the German
  National Library V2.0.11"*, `earliestDatestamp` 1945-01-01, `deletedRecord=transient`). [WEB/API]
- **S25** `https://www.tdx.cat/` (403, 5,658 B), `/oai/request?verb=Identify` (403, 5,769 B),
  `/handle/10803/1234` (403, 5,730 B) — all Cloudflare. `https://hdl.handle.net/api/handles/10803/1234`
  → `responseCode 1`; `…/10803/99999999` → `responseCode 100`. [WEB/API]
- **S26** `https://www.rcaap.pt/` and `/OAIHandler?verb=Identify` — 200, 4,511 B, Anubis
  `v1.26.0-pre2`; `/oai/?verb=Identify` → HTTP 400, 8,698 B Thymeleaf "OAI-PMH Data Provider" page.
  [WEB]
- **S27** `https://trove.nla.gov.au/` — 200, 7,745 B, Anubis `v1.26.2`. [WEB]
- **S28** `https://shodhganga.inflibnet.ac.in/` — 200, 515,934 B (13.5–21.1 s; 1 of 4 attempts
  `000`). Live counters **697,675** Full Text Theses, 21,723 synopses, 908 contributing
  universities, 1,060 MoU; nav MoU 943 + 117; announcements "5,35,000 … 27th May 2024" and
  "6,00,000"; the commented-out stale `597316`/`15274`/`99999` block; "Researcher/Guide" browse.
  `http://` → `000`. `/oai/request?verb=Identify` → `000`. [WEB]
- **S29** `https://ci.nii.ac.jp/d/` → 302 → `https://cir.nii.ac.jp/`;
  `https://cir.nii.ac.jp/opensearch/dissertations?format=json&count=1&from={1,1800,1900}` →
  **775,786**; `?q=RISC-V` → 6; `opensearch/all?q=RISC-V` → 514; bogus term → 0;
  **no parameters → 0**; `q=*` → 0. [API]
- **S30** `https://www.riss.kr/index.do` — HTTP 200, 390,685 B. [WEB]
- **S31** `https://catalogodeteses.capes.gov.br/` and `/catalogo-teses/` — `000` with default and
  with `curl -4`; `getent hosts` returns only AAAA (`2001:12f0:b27:1005::38`) while
  `getent ahostsv4` returns `200.130.18.68`. `https://bdtd.ibict.br/vufind/` — 200, 1,697 B,
  *"Verificando conexão | Oasisbr"*. [WEB]
- **S32** `https://www.cybertesis.net/` → `000`; `http://www.cybertesis.net/` → **200, redirects to
  `https://welcome.lkg-app.com/?clickid=…&dkw=cybertesis.net&pid=…`**, 25,725 B,
  `<meta name="robots" content="noindex, nofollow">`; DNS `208.91.196.105`. [WEB]
- **S33** `https://www.narcis.nl/` → redirect to `https://dans.knaw.nl/nl/data-diensten/narcis/`;
  `http://web.archive.org/web/20260510203109id_/https://dans.knaw.nl/en/data-services/narcis/` —
  *"As of 3 July 2023, the NARCIS website was taken offline and the NARCIS service ended … 'Portal
  of Research Output from the Netherlands' … initiated by the UKB and SURF as a successor"*; also
  *"It is no longer possible to deposit data in EASY"*. CDX series for `narcis.nl` 2022–2026.
  `https://netherlands.openaire.eu/` — 200, 232,623 B. [DOC/WEB]
- **S34** `https://www.cnki.net/` → 302 → `https://oversea.cnki.net/`, 50,542 B;
  `https://www.wanfangdata.com.cn/` — 200, 216,413 B. [WEB]
- **S35** `https://www.bac-lac.gc.ca/eng/services/theses/Pages/theses-canada.aspx` → `000`;
  `https://library-archives.canada.ca/eng/services/services-libraries/theses/Pages/theses-canada.aspx`
  → 302 → `https://www.canada.ca/en/library-archives.html`;
  `https://recherche-collection-search.bac-lac.gc.ca/eng/Home/Search?q=thesis` → 403, 5,775 B. [WEB]
- **S36** `https://www.educacion.gob.es/teseo/irGestionarConsulta.do` → 302 →
  `https://aplicaciones.ciencia.gob.es/teseo` → `000`. [WEB]
- **S37** `https://tez.yok.gov.tr/UlusalTezMerkezi/giris.jsp` — HTTP 200, 33,811 B. [WEB]
- **S38** `https://ndltd.org/` navigation and `https://ndltd.org/thesis-resources/find-etds/` —
  three separate `<a href="https://oatd.org/">Global ETD Search</a>` links, including
  *"Global ETD Search (previously: Union Catalog)"*. Also the stale EThOS row pointing at
  `https://bl.iro.bl.uk/`. [WEB]

**Institutional repositories (§5)**

- **S39** `https://dspace.mit.edu/server/api/discover/search/objects?query=…&size=…` — DSpace 7
  REST, no key. Shannon record (`1721.1/11173`) full metadata map quoted in §5.2, including
  `dc.contributor.advisor: "Frank L. Hitchcock."`, `dc.description: "Thesis (M.S.)--…, 1940."`,
  `dc.format.extent: "69 leaves"`, `dc.identifier.oclc: 34541425` and the verbatim `dc.rights`
  statement. Also entries 2–5 and 26 of §9. Negative controls: `/handle/1721.1/999999999` → 404
  (444,910 B) vs `/handle/1721.1/11173` → 200 (552,361 B); REST bogus query → `totalElements: 0`.
  [API]
- **S40** `https://thesis.library.caltech.edu/` → `000` (Chrome 131 and `curl/8.5.0`);
  DNS `131.215.225.45` shared with `eprints.library.caltech.edu`;
  `https://authors.library.caltech.edu/` → 200, 17,077 B (Cloudflare);
  `https://resolver.caltech.edu/CaltechTHESIS:05282009-153426167` → 404, 1,042 B. [WEB]
- **S41** `https://api.datacite.org/dois?prefix=10.7907&query=…` — Caltech dissertations and
  technical notes; §9 entries 8–16. Negative control `https://api.datacite.org/dois/10.7907/zzzz-zzzz`
  → **404, 87 B**. [API]
- **S42** `https://www2.eecs.berkeley.edu/Pubs/TechRpts/` → **302 → `https://iris.eecs.berkeley.edu/Pubs/TechRpts/`
  → 404, 58,829 B**, identical for Chrome 131, `curl/8.5.0` and Googlebot;
  `…/2016/EECS-2016-1.pdf` → 302 → **404, 548-byte nginx**;
  `https://eecs.berkeley.edu/research/publications/` → 404, 99,227 B;
  `https://iris.eecs.berkeley.edu/` → 200, 83,508 B. DNS: `www2` → 128.32.139.28
  (`eecs-haproxy-vip`), `iris`/`www` → 141.193.213.10/.11 (`wp.wpenginepowered.com`).
  CDX for the index page: 200s through **2026-08-12** (15,267 B). CDX for `EECS-2016-1.pdf`:
  200s in 2017/2020/2021/2022.
  `http://web.archive.org/web/20220425162607id_/…/EECS-2016-1.pdf` → **200, 959,927 B, PDF 1.4**.
  `https://escholarship.org/search/?q=…` → **HTTP 202, 0 bytes**. [WEB]
- **S43** `https://www.research-collection.ethz.ch/server/api/discover/search/objects?query=…` →
  **HTTP 403, 1,337 B "Access Restricted"** (full text quoted in §5.5);
  `…/server/oai/request?verb=Identify` → 200, `earliestDatestamp` 2017-05-15T06:24:06Z,
  `deletedRecord=transient`; bogus verb → **200, 488 B** with an `<error>` element.
  `https://api.datacite.org/dois?prefix=10.3929&query=…` → §9 entries 18–22. [WEB/API]
- **S44** `https://repository.tudelft.nl/` — HTTP 200, 925,475 B. [WEB]
- **S45** `https://lirias.kuleuven.be/` → 200 → `https://kuleuven.limo.libis.be/discovery/search?vid=32KUL_KUL:Lirias`,
  4,784-byte Primo shell. [WEB]
- **S46** `https://graz.elsevierpure.com/en/publications/?type=…` → 403, 6,102 B Cloudflare;
  `https://diglib.tugraz.at/` → 200, 12,844 B; `/dissertationen` → 200, 10,815 B. [WEB]
- **S47** `https://api.crossref.org/works?query.bibliographic=Software-based+microarchitectural+attacks+Gruss&rows=3`
  → `10.1515/itit-2018-0034`, Gruss, *it - Information Technology*, 2018-11-20. [API]

**Commercial routes (§6)**

- **S48** `https://about.proquest.com/en/products-services/pqdtglobal/` — HTTP 200, 347,146 B;
  *"over 6 million metadata records including 4 million full text documents"*, *"over 3,600
  institutions from more than 70 countries"*. `https://pqdtopen.proquest.com/` → **302 →
  `https://www.proquest.com/?defaultdiss=true`**; `https://www.proquest.com/pqdtglobal` → 302,
  0 bytes. [DOC/WEB]
- **S49** `https://www.ebsco.com/products/research-databases/ebsco-open-dissertations` → 301 →
  `https://about.ebsco.com/…`, HTTP 200, 68,261 B; *"The free portal … 2,000,000 electronic theses
  and dissertations; 325 worldwide universities"*. [DOC]

**Landmark theses (§9) — additional**

- **S50** `https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-574.html` — HTTP 200, 9,007 B.
  *"Sketchpad: A man-machine graphical communication system · Ivan Edward Sutherland · September
  2003, 149 pages · New preface by Alan Blackwell and Kerry Rodden. This technical report is based
  on a dissertation submitted January 1963 by the author for the degree of Doctor of Philosophy to
  the Massachusetts Institute of Technology. · DOI https://doi.org/10.48456/tr-574"*. [WEB]
- **S51** `https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-630.html` — *"Semi-invasive attacks – A
  new approach to hardware security analysis · Sergei P. Skorobogatov · April 2005, 144 pages ·
  … dissertation submitted September 2004 … Doctor of Philosophy to the University of Cambridge,
  Darwin College · DOI https://doi.org/10.48456/tr-630"*; `UCAM-CL-TR-630.pdf` → **HTTP 200,
  11,754,717 B, `application/pdf`** — independently reproducing the figure in
  [the companion record §3.5](government-and-institutional-technical-reports.md). [WEB]
- **S52** `https://www.cs.helsinki.fi/u/kutvonen/index_files/linus.pdf` — **HTTP 200, 470,861 B,
  `%PDF-1.3`**. Title page and Finnish/Swedish/English abstract form extracted from the PDF:
  *"Linux: a Portable Operating System · Linus Torvalds · Helsinki, January 31, 1997 · Master of
  Science Thesis · University of Helsinki, Department of Computer Science · Master of Science
  thesis · January 1997 · 52 p. · Linux, Operating System, Portability, Alpha, Sparc"*.
  Absence from Helda confirmed by two DSpace REST searches against
  `https://helda.helsinki.fi/server/api/discover/search/objects` (queries
  `"Linux portable operating system Torvalds"` → 3 hits, `"Torvalds"` → 77 hits; the thesis is in
  neither). `https://helda.helsinki.fi/` itself → 200, 4,262 B, Anubis `1.23.0`. [WEB/API]
- **S53** `https://api.datacite.org/dois?prefix=10.1184&query=DRAM AND dissertation` — CMU KiltHub
  theses, §9 entries 23–24, including the concept/`.v1` DOI pair.
  `https://api.figshare.com/v2/articles/search` POST with `institution:320` → HTTP 200 with a
  2-byte body (`[]`) — the figshare institutional search returned nothing usable. [API]
- **S54** `https://hdl.handle.net/api/handles/1721.1/11173` → `responseCode: 1` with the DSpace URL —
  demonstrating the Handle oracle on a second prefix. [API]
