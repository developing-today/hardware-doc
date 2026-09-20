# Social science and humanities preprint servers — grouped record

- **Compiled:** 2026-09-01 · **All reachability and count probes run:** 2026-09-01 / 2026-09-02 UTC
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

> **Scope note — why these are here at all.** This knowledge base is about hardware,
> software and systems. Most of the servers below have **no electronics or systems
> content**, and the user's instruction was explicit: group them, document them simply,
> and let a measured table carry the weight rather than prose. That is what this file does.
>
> **Four entries are flagged for slightly deeper treatment**, because there is a real
> computing connection:
> - **[Rutgers Optimality Archive](#16-rutgers-optimality-archive-roa)** and
>   **[LingBuzz](#15-lingbuzz)** — computational linguistics, formal grammar, phonology and
>   Optimality Theory: part of NLP's intellectual prehistory. They are also the two most
>   instructive **software-durability case studies** in this entire directory. RoA has run
>   continuously since **1993**.
> - **[PhilSci-Archive](#14-philsci-archive)** and **[PhilArchive](#13-philarchive)** —
>   philosophy of computation, philosophy of AI, AI ethics. PhilSci-Archive runs on
>   **EPrints** at the University of Pittsburgh.
> - **[MetaArXiv](#11-metaarxiv)** — metascience. More relevant than it looks: this is where
>   research-software reproducibility and open-science-tooling work is deposited.
>
> **E-LIS and LISSA are covered elsewhere and are deliberately omitted here.**

## 0. Method, and the OSF status trap

Sixteen of the servers in this file are or were hosted by the **Center for Open Science
(COS)** on the OSF preprints platform. OSF web pages are a JavaScript single-page app:

> **`https://osf.io/preprints/<anything>` returns HTTP 200 and an identical 4,207-byte
> shell even for providers that do not exist.** Status code and byte size are worthless
> signals on that host.

Confirmed here as a live negative control: `https://osf.io/preprints/eyexiv/` returned
**HTTP 200, 4,207 bytes** on 2026-09-02, while the authoritative provider list at
`https://api.osf.io/v2/preprint_providers/?page[size]=100` contains **no `eyexiv` entry at
all** (S1) [API]. Every OSF figure below therefore comes from
`https://api.osf.io/v2/preprints/?filter[provider]=<slug>` → `links.meta.total`, and every
status claim from `https://api.osf.io/v2/preprint_providers/<slug>/` →
`attributes.allow_submissions` and `attributes.description`, which carries the operator's
own closure notice (S2) [API] [DOC].

**Negative control on the count endpoint:** `filter[provider]=bogusprovider12345` returned
`total = 0`, not an error (S2) [API] — so a non-zero total is meaningful, but a zero is
ambiguous.

The OSF provider list contained **32 providers** on 2026-09-02 (S1) [API].

Web reachability used the `AGENTS.md` UA ladder: default `curl` → Chrome 131 →
WhatsApp/2.23.20.0 → ChatGPT-User/1.0 → ClaudeBot/1.0.

## 1. Status and size table

| Server | URL probed 2026-09-02 | Operator | Launched | Status 2026-09-02 | Records | Source of count |
|---|---|---|---|---|---|---|
| **SocArXiv** | `osf.io/preprints/socarxiv` · `socopen.org` | Center for Open Science | 2016 (S3) | **ALIVE**, submissions open, pre-moderation | **24,670** | OSF API [API] |
| **PsyArXiv** | `psyarxiv.com` → `osf.io/preprints/psyarxiv` | Society for the Improvement of Psychological Science (SIPS) + COS | 2016 (S3) | **ALIVE**, submissions open, pre-moderation — **still on OSF** | **63,368** | OSF API [API] |
| **EdArXiv** | `edarxiv.org` → `osf.io/preprints/edarxiv` | COS | 2019 (S3) | **ALIVE**, submissions open | **3,506** | OSF API [API] |
| **APSA Preprints** | `preprints.apsanet.org` | American Political Science Association + Cambridge University Press | 2019 (S3) | **ALIVE** | **1,326** | Cambridge Engage public API [API] |
| **LawArXiv** | `osf.io/preprints/lawarxiv` | COS | 2017–2020 | **CLOSED**, content retained | **165** | OSF API [API] |
| ↳ successor **Law Archive** | `osf.io/preprints/lawarchive` | COS | — | **ALIVE**, submissions open | **1,664** | OSF API [API] |
| ↳ old domain | `lawarxiv.org` | — | — | **DOMAIN LOST** — 114-byte parking redirect to `/lander` | — | probe [WEB] |
| **CrimRxiv** | `crimrxiv.com` | University of Manchester, on **PubPub** | 2020 (S3) | **ALIVE** — but Cloudflare-blocked to most agents | **not verified** | see §8 |
| **MediArXiv** | `mediarxiv.com` · `osf.io/preprints/mediarxiv` | COS | 2019 (S3) | **ALIVE**, submissions open | **443** | OSF API [API] |
| ↳ old domain | `mediarxiv.org` | — | — | **DOMAIN LOST** — redirects to unrelated `afterdispatch.com` | — | probe [WEB] |
| **BodoArXiv** | `osf.io/preprints/bodoarxiv` | ScholarlyHub + COS (S3) | 2019 (S3) | **ALIVE**, submissions open | **165** | OSF API [API] |
| ↳ vanity domain | `bodoarxiv.org` | — | — | **DOMAIN HIJACKED** — now an online-casino page | — | probe [WEB] |
| **hprints** | `hprints.hal.science` · HAL API | CCSD (CNRS) / Nordbib | 2008 (S3) | **ALIVE** — HAL infrastructure | **397** | HAL API [API] |
| **MetaArXiv** | `osf.io/preprints/metaarxiv` | BITSS, UC Berkeley + COS | 2018 (S3) | **ALIVE**, submissions open | **1,014** | OSF API [API] |
| **MindRxiv** | `mindrxiv.org` → `osf.io/preprints/mindrxiv` | COS + Mind & Life Institute | 2018 (S3) | **FROZEN** — submissions closed, content retained | **288** | OSF API [API] |
| **PhilArchive** | `philarchive.org` | PhilPapers Foundation; developed and operated by the **Centre for Digital Philosophy, Western University** | 2009 (S3) | **ALIVE** | **143,707 works** across **6,155 topics** | operator's own front page [WEB] |
| **PhilSci-Archive** | `philsci-archive.pitt.edu` | University of Pittsburgh (D-Scribe Digital Publishing) | 2001 (S3) | **ALIVE** — **EPrints 3.3.15** | **12,586** | sum of operator's browse-by-year [WEB] |
| **LingBuzz** | `lingbuzz.net` (= `ling.auf.net/lingbuzz`) | Michal Starke (Univ. of Tromsø) | ~2004 (S3) | **ALIVE** | **≥9,200** (highest live ID between 009200 and 009300) | ID probing [API] |
| **RoA** | `roa.rutgers.edu` | Rutgers School of Arts and Sciences | **1993** (S3, S9) | **ALIVE but not accepting new deposits since 2022** | operator says **"ca. 1400 … 1993–2022"**; operator's XLSX export has **1,463 rows** | operator front page + export [WEB] [API] |

**Conflicts recorded, not resolved.** Wikipedia's size buckets (S3) put SocArXiv and
PsyArXiv at `>10,000`, PhilArchive and PhilSci-Archive at `>10,000`, LingBuzz at `>10,000`,
and RoA at `>1,000`. The measured OSF/operator numbers above are all consistent with those
buckets except **LingBuzz**, where my ID-space probe supports ~9.2k rather than >10k — but
ID probing measures the *identifier space*, not live records, so treat both as approximate.

## 2. What the probe evidence shows

Three findings are worth more than the individual entries.

**(a) The OSF content survives; the vanity domain does not.** Every closed or frozen
server in this file still serves its full content from OSF, with DOIs, years after
shutdown. What breaks is the branded domain the community was told to use:

| Vanity domain | State on 2026-09-02 | Content still readable? |
|---|---|---|
| `lawarxiv.org` | 114-byte domain-parking stub redirecting to `/lander` | Yes — OSF, 165 records |
| `mediarxiv.org` | redirects to `afterdispatch.com`, an unrelated site | Yes — OSF, 443 records, and `mediarxiv.com` still works |
| `bodoarxiv.org` | **"Mostbet Bangladesh — Online Casino & Sports Betting"** | Yes — OSF, 165 records |

**(b) An operator's own signposting can point at a hijacked domain.** BodoArXiv's OSF
provider description — served live by the Center for Open Science on 2026-09-02 — reads
*"Open Repository for Medieval Studies **Visit BodoArXiv.org** to learn more"* (S2) [DOC].
That domain is now a gambling site. The medieval-studies community's own project blog
survives separately at `bodoarxiv.wordpress.com` (HTTP 200, 65,449 bytes) [WEB]. **Do not
trust a repository's own "visit our website" link as evidence the website is still theirs.**

**(c) PsyArXiv did *not* leave OSF — correcting a common belief.** The OSF API on
2026-09-02 lists `psyarxiv` with `allow_submissions = true`, `reviews_workflow =
pre-moderation`, `domain = https://psyarxiv.com/`, and a description naming SIPS as
maintainer (S2) [API] [DOC]. `psyarxiv.com` returns HTTP 200 and redirects to
`https://osf.io/preprints/psyarxiv/`. What happened is a **platform-side URL
consolidation**: OSF retired branded per-provider front doors in favour of
`osf.io/preprints/<slug>` paths, and the custom domains became redirects. The *service* did
not migrate; the *URL* did. At 63,368 records it is by a wide margin the largest server in
this file. **Exact date of the URL consolidation: [NOT-VERIFIED]** — I could not find a
dated COS announcement.

---

## 3. SocArXiv

- `osf.io/preprints/socarxiv` · blog at `socopen.org` (HTTP 200, 82,394 B) · COS · 2016 ·
  **ALIVE** · **24,670 records** [API]

Founded as an explicitly political alternative to SSRN after Elsevier acquired it. Runs
pre-moderation: the OSF description says *"SocArXiv papers are moderated before appearing.
Please read the moderation policy before submitting"* (S2) [DOC]. Moderation is a
scope-and-plausibility screen, not peer review — a deposit here guarantees a timestamp, a
DOI and that a human glanced at it, nothing more. **Computing content: negligible.**

## 4. PsyArXiv

- `psyarxiv.com` → `osf.io/preprints/psyarxiv` · SIPS + COS · 2016 · **ALIVE** ·
  **63,368 records** [API]

See §2(c) — it is still on OSF. Pre-moderated. The largest single-discipline social-science
preprint server measured in this directory. Relevant to systems work only obliquely: it is
the main venue for the psychology replication-crisis literature, which is the sociological
origin of the reproducibility norms that MetaArXiv (§11) formalises. **Computing content:
negligible**, beyond method/statistics tooling papers.

## 5. EdArXiv

- `edarxiv.org` → `osf.io/preprints/edarxiv` · COS · 2019 · **ALIVE** · **3,506 records** [API]

Education research. Submissions open, pre-moderation. Vanity domain still redirects
correctly — one of the few in this file that does. **Computing content: negligible**
(occasional educational-technology and CS-education work; not enumerated here).

## 6. APSA Preprints

- `preprints.apsanet.org` · American Political Science Association + **Cambridge University
  Press** · 2019 · **ALIVE** · **1,326 items** [API]

The only server in this file on a **commercial publisher's platform** — Cambridge Open
Engage, which is the same ChemRxiv-derived Atypon/Engage stack. That has a concrete
consequence for retrieval: it exposes a genuinely open REST API,
`/engage/apsa/public-api/v1/items`, which returned `totalCount: 1326` with full item records
on 2026-09-02 (S4) [API]. DOIs are minted under Cambridge's prefix **10.33774** (the
`apsa-` namespace; the prefix as a whole held 5,720 works across all Engage servers on
2026-09-02) (S5) [API]. **Computing content: negligible.**

Durability read: publisher-operated is a mixed signal. It is well-run and well-funded
*while the publisher wants it* — and PeerJ Preprints and Nature Precedings show what
happens when a publisher stops wanting it (see
[closed-and-defunct-servers.md](closed-and-defunct-servers.md)).

## 7. LawArXiv / Law Archive

- LawArXiv `osf.io/preprints/lawarxiv` · COS · **2017–2020, CLOSED** · **165 records
  retained** [API]
- Law Archive `osf.io/preprints/lawarchive` · COS · **ALIVE**, pre-moderation ·
  **1,664 records** [API]

**What happened to the content: nothing bad.** The OSF provider record for `lawarxiv` says,
verbatim, *"LawArXiv is no longer able to accept new submissions. Thank you to everyone who
contributed their work to this repository. Existing content in LawArXiv will remain
accessible…"* (S2) [DOC], and the API confirms 165 preprints are still served. A successor,
**Law Archive**, runs on the same platform and is nearly ten times larger.

**What did break: `lawarxiv.org`.** On 2026-09-02 it returned a **114-byte** page whose
entire body is `<script>window.onload=function(){window.location.href="/lander"}</script>`
— the signature of a lapsed domain sitting on a parking service [WEB]. A reader following a
2019 citation to `lawarxiv.org` finds a parking page; the same paper is one API call away on
OSF. **This is the single most compressible lesson in this file: cite the DOI.**

## 8. CrimRxiv

- `crimrxiv.com` · University of Manchester · 2020 (S3) · runs on **PubPub** ·
  **ALIVE** · **count [NOT-VERIFIED]**

Criminology's open archive, and the only server in this file on **PubPub** — the
MIT-Press-originated, open-source community publishing platform. That is a genuine
technical distinction: PubPub is a full CMS with versioning and inline annotation rather
than a deposit-and-serve repository, and it gives each community a **shared DOI prefix**
(`10.21428`, registered to *PubPub*), so DOI-prefix counting cannot isolate CrimRxiv. The
whole prefix held **13,852 works** on 2026-09-02, spanning unrelated publishers including
Vanderbilt University conference proceedings (S5) [API].

**Retrieval is hostile.** `https://www.crimrxiv.com/` returned **HTTP 403 on all five
user-agents** in the ladder; so did `crimrxiv.pubpub.org` and `www.crimrxiv.com/pub/`. The
**apex domain without `www`** succeeded exactly once, under the **WhatsApp/2.23.20.0**
user-agent, returning a 1,029,205-byte page — and three subsequent identical requests
returned Cloudflare's 5,578-byte "Just a moment…" interstitial [WEB]. This is
**intermittent Cloudflare bot-management, not a stable UA whitelist**, and I did not obtain
a record count from it. `mcp_fff`/scripted access to CrimRxiv should be assumed unreliable.

**Computing content: negligible**, beyond computational criminology and predictive-policing
critique.

## 9. MediArXiv

- `mediarxiv.com` (**not** `.org`) · `osf.io/preprints/mediarxiv` · COS · 2019 · **ALIVE**,
  submissions open · **443 records** [API]

Media, film and communication studies. Small but genuinely live. Its interest here is
entirely the **domain split**: the OSF description says *"Visit mediarxiv.com for more
information"* (S2) [DOC] and `mediarxiv.com` does work (HTTP 200, 153,238 B, title
*"MediArXiv | The Open Archive for Media, Film, and Communication Studies"*), while
`mediarxiv.org` now redirects to `afterdispatch.com`, an unrelated site with an empty
`<title>` [WEB]. One character of TLD separates the live archive from a stranger's domain.

## 10. BodoArXiv

- `osf.io/preprints/bodoarxiv` · ScholarlyHub + COS (S3) · 2019 · **ALIVE**, submissions
  open · **165 records** [API]

Medieval studies — manuscript studies, palaeography, medieval Latin. Notable for having
been a **ScholarlyHub** initiative, i.e. one of the few servers here born from a
scholar-owned-infrastructure movement rather than from COS or a publisher.

**The cautionary finding is §2(b): `bodoarxiv.org` is now an online-casino page** ("Mostbet
Bangladesh"), and the operator's own OSF description still tells readers to go there
[WEB] [DOC]. The project's surviving non-OSF presence is `bodoarxiv.wordpress.com`. Cite the
OSF DOI. **Computing content: none.**

## 11. MetaArXiv

- `osf.io/preprints/metaarxiv` · **BITSS — Berkeley Initiative for Transparency in the
  Social Sciences** + COS · 2018 · **ALIVE**, pre-moderation · **1,014 records** [API]

**Flagged as more relevant than it looks.** The OSF description is explicit: *"An
interdisciplinary archive of articles focused on improving research transparency and
reproducibility. Maintained by The Berkeley Initiative for Transparency in the Social
Sciences (BITSS)"* (S2) [DOC].

Why a hardware/software knowledge base should care: **reproducibility is a software
problem** and much of the literature that defines it lands here rather than in CS venues —
preregistration and registered-report mechanics, computational-workflow and
container-based reproducibility, code- and data-availability-policy audits, research-software
sustainability, and meta-analysis of open-science tooling adoption. If you are looking for
the empirical evidence base behind "ship the container, pin the versions, publish the
analysis code", MetaArXiv is one of the places it is deposited. At 1,014 records it is
small enough to browse exhaustively.

Caveat: it is pre-moderated but **not peer-reviewed**, and metascience preprints are
frequently cited in policy argument long before review. Check for a journal version.

## 12. MindRxiv

- `mindrxiv.org` → `osf.io/preprints/mindrxiv` · COS + Mind & Life Institute · 2018 ·
  **FROZEN** · **288 records** [API]

Mind and contemplative-practice research. Closed to new submissions; the OSF description
states *"MindRxiv is no longer able to accept new submissions. Existing content will remain
accessible as part of the Center for Open Science and Mind & Life's ongoing
commitment…"* (S2) [DOC]. The vanity domain still redirects correctly to OSF — a rare
well-behaved shutdown. **Computing content: none.**

## 13. PhilArchive

- `philarchive.org` · PhilPapers Foundation; **developed and operated by the Centre for
  Digital Philosophy, Western University** · 2009 (as the PhilPapers Archive) · **ALIVE** ·
  **143,707 works**, **6,155 topics** [WEB]

**Flagged: philosophy of computing and AI ethics.** PhilArchive is the deposit arm of
PhilPapers, and inherits PhilPapers' unusually fine-grained subject taxonomy. Its top-level
category list, retrieved 2026-09-02, includes **"Philosophy of Computing and Information"**
as a first-class sibling of philosophy of physics and philosophy of biology, alongside
**Philosophy of Cognitive Science**, **Logic and Philosophy of Logic**, **Formal Sciences**
and **Philosophy of Mind** (S6) [WEB]. Between those categories sits essentially the whole
analytic literature on computation, machine consciousness, AI alignment and machine ethics.

It is by a very large margin the biggest archive in this file — larger than every other
entry combined. Retrieval is straightforward: it exposes **OAI-PMH 2.0 at
`https://philarchive.org/oai.pl`**, with `earliestDatestamp 2008-01-01`,
`deletedRecord: transient` and deflate compression advertised (S7) [API]. Access note: the
HTML front page **403s under a bare `curl` UA and succeeds under Chrome 131**; the OAI
endpoint behaves the same way.

**Editorial gate:** none in the peer-review sense. The site states *"PhilArchive consists
entirely of articles submitted by users"* [WEB], with per-item peer-review-status tags
declared by the depositor. Treat a PhilArchive item as self-archived unless the tag says
otherwise.

## 14. PhilSci-Archive

- `philsci-archive.pitt.edu` · **University of Pittsburgh**, D-Scribe Digital Publishing ·
  **2001** · **ALIVE** · **12,586 records** [WEB]

**Flagged: philosophy of science, including philosophy of computation and AI.** Founded
2001 and still running on the same institutional footing 25 years later, which makes it one
of the more durable services documented anywhere in this directory.

**Software: EPrints 3.3.15**, declared in the page's own `generator` meta tag on 2026-09-02
(S8) [WEB]. EPrints is the University of Southampton's Perl repository platform, first
released in 2000 — the same lineage as CogPrints (see
[closed-and-defunct-servers.md](closed-and-defunct-servers.md)), and a useful contrast:
identical software, one survived because a university library kept operating it and one did
not.

**Size, and a metadata caveat worth noting.** Summing the operator's own browse-by-year
index across **51 year buckets spanning 1926–2027** gives **12,586 records** (S8) [WEB].
The distribution is informative: ~638 for 2026 and 789 for 2025 against 175 for 2003 — the
archive is growing, not coasting. The buckets are *work* dates, not deposit dates: 1926,
1956, 1958 and 1962 each hold one item. Independently, OAI-PMH `Identify` reports
`earliestDatestamp 2010-10-07`, `deletedRecord: persistent`, `adminEmail
philsciarchive@groups.pitt.edu` (S8) [API] — i.e. the OAI datestamps begin at a 2010
platform migration and **cannot** be used to date the archive's founding. Conflict recorded.

`ListIdentifiers` paginates 100 at a time with a `resumptionToken` that carries **no
`completeListSize`**, so a full harvest is required for an exact figure — that is why the
count above comes from the browse index rather than the API.

The archive also hosts the **PhilMath Archive** as a sub-collection, and browse views for
open-access journals and books.

## 15. LingBuzz

- `lingbuzz.net` (identical content at `ling.auf.net/lingbuzz`) · **run and hosted
  personally by Michal Starke** · ~2004 · **ALIVE** · **≥9,200 deposits** [API]

**Flagged: computational linguistics and formal grammar.** LingBuzz is the de-facto
preprint venue for theoretical syntax, semantics, phonology and morphology. Its front page
on 2026-09-02 states plainly: *"LingBuzz is run and hosted by Michal Starke"* [WEB]. That
sentence is the entire governance model.

**Why a systems reader should care — the minimalism is the point.** LingBuzz is a
hand-written application behind `nginx/1.14.2` with essentially no modern repository
furniture, and it has outlived roughly half the professionally-run servers in this
directory. Measured characteristics, all 2026-09-02:

- **Flat sequential identifiers.** `lingbuzz/000100` is Noam Chomsky, *"Three factors in
  Language Design"*, June 2004 — which both dates the archive and shows the numbering has
  never been rebased. Live IDs confirmed at 000100, 004000, 008000, 008500, 008800, 009000,
  009100, 009110, 009120, 009150, 009200 [API].
- **No 404 handling.** IDs above the live range (009300, 009400, 009450, 009470, 009480,
  009490, 009999) all return **HTTP 502 Bad Gateway from nginx/1.14.2**, i.e. the backend
  process dies rather than returning "not found" [API]. This is a *useful* negative control
  — 502 means "past the end", 200 means "exists" — but it is not what a maintained
  repository stack does.
- **No HEAD support.** `curl -I https://lingbuzz.net/` returns *"Empty reply from server"*
  [API].
- **No DOIs, no OAI-PMH, no versioned identifiers**, no formal preservation arrangement
  that I could find. **[NOT-VERIFIED]:** whether any dark archive holds LingBuzz content.
- **nginx 1.14.2** is the Debian 10 "buster" stock package, out of upstream support.

**The durability lesson, stated honestly.** LingBuzz demonstrates that a single motivated
maintainer with a flat file store can outlast institutions — and simultaneously that this
model has **exactly one point of failure**, with no succession plan and no dark archive.
Compare `bodoarxiv.org` (§10): the difference between LingBuzz and a casino page is one
person continuing to renew a domain. Content here is AI-adjacent in places — ID 008000 is
*"Speaking_Brains: Recent Papers on AI Neuro"* — but **do not cite LingBuzz as a durable
locus**; find the DOI'd version or archive the PDF yourself.

## 16. Rutgers Optimality Archive (RoA)

- `roa.rutgers.edu` · Rutgers University **School of Arts and Sciences** · **1993** ·
  **ALIVE but not accepting new deposits** · operator says **"ca. 1400 papers uploaded from
  1993–2022"**; operator's own XLSX export contains **1,463 rows** [WEB] [API]

**Flagged, and the most historically important entry in this file.** RoA is the
distribution point for Optimality Theory — Prince & Smolensky's constraint-ranking framework,
which is *the* bridge between generative phonology and constraint-satisfaction computation,
and a direct ancestor of the optimisation framing that pervades computational linguistics.
It began the same year as the first web browsers and **two years after arXiv**.

**Its self-documented systems history is a genuine artefact.** The archive's own `info.html`,
retrieved 2026-09-02, records the full 30-year operational lineage in one paragraph (S9)
[DOC] — reproduced here because nothing else in this directory is comparable:

- **1993** — begins as *"a command-line anonymous ftp server constructed by Alan Prince"*.
- **1996** — a web interface added *"with the help of Mike Strickland (then a high-energy
  graduate student, now a high-energy physicist), who wrote the original search, delivery,
  and upload scripts."*
- **2000–2014** — day-to-day management by Eric Bakovic. Files held *"in the server-cluster
  of the Rutgers University Cognitive Science Center (RuCCS)"*, scripts hosted by
  **webslingerZ**, a commercial provider.
- **2001** — first major overhaul, *"spurred on by difficulties in the RuCCS system"*.
- **2002** — hardware replaced. **2003** — software rewritten by Paul de Lacy.
- **2011** — *"A mild hacking incursion … forced the temporary shutdown of the Archive. It
  was replaced for a year with an html-only site that kept all files available and allowed
  upload via email request."*
- **2012** — rewritten again and moved onto Rutgers SAS's secure servers, where it still is.
- **Today** — Administrator Natalie DelBusso, consultant Eric Bakovic, and Alan Prince
  credited as *"Capo di tutti i capi"*.

**Read that 2011 line again.** Compromised, and the recovery was *to fall back to static
HTML that kept every file downloadable and accept submissions by email for a year*. That is
the correct failure mode for an archive, and it is the opposite of what happened to
`lawarxiv.org` or `bodoarxiv.org`. RoA survived three rewrites, a hardware replacement, a
hosting-provider change, an intrusion and four administrators, because at every step the
**files stayed served**.

**Measured state, 2026-09-02:**

- `Server: Apache`; the index page's `Last-Modified` is **2024-10-17**, while the newest
  paper listed is **ROA 1394, April 2022** [API]. Maintained, but not ingesting.
- Full text verified live: `content/article/files/1922_hideo_kobayashi_1.pdf` downloads as a
  **837,797-byte, 20-page PDF 1.7** [API].
- **The "API" is a spreadsheet.** `article/ROA.xlsx` is a 320,860-byte XLSX offered on the
  front page as *"a fully linked Excel table suitable for search and annotation"*; it parses
  to **1,463 rows** [API]. There is no OAI-PMH, no REST API and no DOI minting.
- Front-page self-description: *"ROA contains ca. 1400 papers uploaded from 1993-2022"* [WEB].
  Wikipedia's bucket is `>1,000` (S3). Conflict recorded; all three figures are consistent
  in magnitude.

**Durability verdict.** RoA is the best argument in this directory for the thesis that
**simplicity, an institutional host and a bulk export beat features**. Static files under
Apache at a university, plus a downloadable manifest of the entire holdings, is a design a
future archivist can rescue. Its risk is not technical — it is that nobody has committed to
operating it now that deposits have stopped, and there is **no named dark archive**
[NOT-VERIFIED].

## 17. hprints

- `hprints.hal.science` · **CCSD (CNRS)** with Nordbib funding · 2008 (S3) · **ALIVE** ·
  **397 records** [API]

The Nordic arts, humanities and social sciences open archive. Its only structural interest
is that it is **not an independent server at all**: it is a *portal view* onto **HAL**, the
French national repository. See [hal.md](hal.md) for the platform, the OAI-PMH and Solr
APIs, deposit moderation and preservation arrangements — all of which hprints inherits, and
which is why an archive with fewer than 400 records has better durability guarantees than
several servers here that are twenty times larger.

**Retrieval note, 2026-09-02.** `hprints.org` is **DNS NXDOMAIN** on all five user-agents —
the original front door is gone [WEB]. `hprints.hal.science` returns HTTP 200 but serves an
**Anubis proof-of-work anti-scraper interstitial** ("Making sure you're not a bot!… This
website is running Anubis version devel") to non-JavaScript clients [WEB]. The **API is
unaffected**: `https://api.archives-ouvertes.fr/search/hprints/?q=*:*&rows=0&wt=json`
returned `numFound: 397` immediately with a plain `curl` (S10) [API]. This is a clean
example of a pattern worth internalising — *when the HTML is defended, the machine interface
usually is not*.

## 18. Access, APIs and bulk retrieval — summary

| Server(s) | Machine interface | Works from scripts? |
|---|---|---|
| All OSF-hosted (SocArXiv, PsyArXiv, EdArXiv, LawArXiv/Law Archive, MediArXiv, BodoArXiv, MetaArXiv, MindRxiv) | JSON:API at `api.osf.io/v2/` | **Yes** — plain `curl`, no key. Use `filter[provider]=` + `links.meta.total`. URL-encode the brackets (`%5B`/`%5D`) or the shell will eat them. |
| APSA Preprints | `preprints.apsanet.org/engage/apsa/public-api/v1/items` | **Yes** — plain `curl`, returns `totalCount` + full records |
| PhilArchive | OAI-PMH at `philarchive.org/oai.pl` | **Yes**, but needs a browser UA |
| PhilSci-Archive | OAI-PMH at `philsci-archive.pitt.edu/cgi/oai2` | **Yes** with default `curl`; **blocked (BIG-IP ASM captcha) under a Chrome UA** — the ladder runs *backwards* here. No `completeListSize`. |
| hprints | HAL Solr API `api.archives-ouvertes.fr/search/hprints/` | **Yes** — HTML front end is behind Anubis PoW |
| RoA | none — but a complete **XLSX manifest** at `article/ROA.xlsx` | **Yes**, effectively |
| LingBuzz | none; sequential IDs, 502 past the end, no HEAD | Scrape-only |
| CrimRxiv | PubPub; no isolable DOI prefix | **No** — Cloudflare 403, intermittent |

**Negative controls used:** `filter[provider]=bogusprovider12345` → `total: 0`;
`osf.io/preprints/eyexiv/` → HTTP 200 / 4,207 B for a provider absent from the API list;
`lingbuzz/009999` → HTTP 502.

## 19. Sources

- **S1** — OSF preprint-provider list. `https://api.osf.io/v2/preprint_providers/?page[size]=100`
  · retrieved 2026-09-02 · authoritative list of 32 providers, with `domain` and
  `allow_submissions` per provider. [API]
- **S2** — OSF preprint counts and provider records.
  `https://api.osf.io/v2/preprints/?filter[provider]=<slug>&page[size]=1` (`links.meta.total`)
  and `https://api.osf.io/v2/preprint_providers/<slug>/` (`attributes.description`,
  `allow_submissions`, `reviews_workflow`) · retrieved 2026-09-02 · every OSF count and every
  operator closure notice quoted above. [API] [DOC]
- **S3** — Wikipedia, *List of preprint repositories*.
  `https://en.wikipedia.org/wiki/List_of_preprint_repositories` · retrieved 2026-09-02 ·
  launch years, operators and order-of-magnitude size buckets. Used only where no
  first-party source was obtainable, and always flagged. [COM]
- **S4** — APSA Preprints public API.
  `https://preprints.apsanet.org/engage/apsa/public-api/v1/items?limit=1` · retrieved
  2026-09-02 · `totalCount: 1326`. [API]
- **S5** — Crossref REST API. `https://api.crossref.org/prefixes/<prefix>` and
  `/prefixes/<prefix>/works?rows=0` · retrieved 2026-09-02 · prefix ownership (10.33774 →
  Cambridge University Press; 10.21428 → PubPub) and prefix-wide work counts. [API]
- **S6** — PhilArchive front page. `https://philarchive.org/` (Chrome 131 UA) · retrieved
  2026-09-02 · "There are currently 143,707 works in the archive. These works fall under
  6,155 topics"; operator statement naming the Centre for Digital Philosophy, Western
  University; full top-level category list including *Philosophy of Computing and
  Information*. [WEB]
- **S7** — PhilArchive OAI-PMH. `https://philarchive.org/oai.pl?verb=Identify` · retrieved
  2026-09-02 · `earliestDatestamp 2008-01-01`, `deletedRecord: transient`. [API]
- **S8** — PhilSci-Archive. `https://philsci-archive.pitt.edu/` (generator meta tag:
  `EPrints 3.3.15`), `https://philsci-archive.pitt.edu/view/year/` (51 year buckets, sum
  12,586), `https://philsci-archive.pitt.edu/cgi/oai2?verb=Identify` (earliestDatestamp
  2010-10-07, adminEmail `philsciarchive@groups.pitt.edu`) · all retrieved 2026-09-02.
  [WEB] [API]
- **S9** — Rutgers Optimality Archive. `https://roa.rutgers.edu/` (front page: "ca. 1400
  papers uploaded from 1993-2022"; newest ROA 1394, Apr/2022) and
  `https://roa.rutgers.edu/static/info.html` (full operational history 1993–2012, named
  staff, the 2011 intrusion, the RuCCS/webslingerZ/SAS hosting chain) ·
  `https://roa.rutgers.edu/article/ROA.xlsx` (320,860 B, 1,463 rows) · retrieved 2026-09-02.
  [WEB] [DOC] [API]
- **S10** — HAL search API. `https://api.archives-ouvertes.fr/search/hprints/?q=*:*&rows=0&wt=json`
  · retrieved 2026-09-02 · `numFound: 397`. [API]
- **S11** — Reachability probes. Raw log in
  `doc/hardware/scratch/preprint-repositories/humanities/` and the directory-wide
  `scratch/preprint-repositories/reachability-2026-09-01.txt` · run 2026-09-01/02 with the
  `AGENTS.md` UA ladder. Supports every `lawarxiv.org`, `mediarxiv.org`, `bodoarxiv.org`,
  `hprints.org`, `crimrxiv.com` and `lingbuzz.net` status claim. [WEB]
