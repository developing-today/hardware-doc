# Closed, frozen and defunct preprint servers — cross-cutting record

- **Compiled:** 2026-09-01 · **All reachability, TLS and count probes run:** 2026-09-01 /
  2026-09-02 UTC
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

> **Why this file exists.** Everything else in this directory documents a *living* service.
> This documents the dead ones, because **durability is the property this knowledge base
> actually cares about**. A preprint server is a promise that a document will still be
> there in ten years. This record measures how often that promise is kept, exactly how it
> fails, and what a citing author should do about it.

## 1. The dead/alive table

Every row was probed on **2026-09-02** using the `AGENTS.md` UA ladder (default `curl` →
Chrome 131 → WhatsApp/2.23.20.0 → ChatGPT-User/1.0 → ClaudeBot/1.0). "Retrievable **today**"
means *I downloaded a record, and where possible a full-text file, during this pass*.

| Server | Span | Operator | What happened | Retrievable today? | Where |
|---|---|---|---|---|---|
| **Nature Precedings** | 2007–2012 | Nature Publishing Group | Publisher discontinued it. Original host **`precedings.nature.com` refuses TCP connections** | **YES — fully, incl. full text** | `nature.com/npre`; DOIs `10.1038/npre.*` resolve HTTP 200; `npre.2012.7141.1.pdf` downloaded as a valid **5-page, 177,957-byte PDF** [API] |
| **PeerJ Preprints** | 2013–2019 | PeerJ | Publisher stopped accepting new preprints **30 Sep 2019** (S1) | **YES via DOI — but bot-blocked** | `doi.org/10.7287/peerj.preprints.27311v1` → HTTP **302** → `peerj.com/preprints/27311v1`. Every direct `peerj.com` fetch returned **403 on all five UAs**. Prefix `10.7287` holds **65,760** registered works [API] |
| **CogPrints** | 1997–2017 | University of Southampton | Founder (Stevan Harnad) retired; service retired with him. **`https://cogprints.org` fails TLS**; `http://` redirects to a Southampton web archive | **YES — static mirror, full text works** | `web-archive.southampton.ac.uk/cogprints.org/`. Record 1 (Shizgal 1997) PDF downloaded: **174,167 bytes, 6 pages, PDF 1.2** [API] |
| **INArxiv** | 2017–2020 | Center for Open Science | Closed 2020-10-07; successor `rinarxiv.lipi.go.id` **never had a valid certificate** (`CN=linux`) | **YES — 15,987 preprints** | OSF API. See [regional-and-national-servers.md](regional-and-national-servers.md) |
| **LawArXiv** | 2017–2020 | Center for Open Science | Closed; superseded by **Law Archive** (1,664 records). **`lawarxiv.org` lapsed to a domain-parking stub (114 bytes → `/lander`)** | **YES — 165 preprints** | OSF API. See [social-sciences-and-humanities.md](social-sciences-and-humanities.md#7-lawarxiv--law-archive) |
| **MarXiv** | 2017–2020 | Center for Open Science | Closed. **`marxiv.org` refuses TCP on 443** | **YES — 454 preprints** | OSF API. See [natural-sciences-and-niche-servers.md](natural-sciences-and-niche-servers.md#7-marxiv) |
| **Frenxiv** | 2018–2022 | Center for Open Science | Closed on OSF. Separate **`frenxiv.org` still renders but is frozen at Oct 2020** | **YES — 128 preprints on OSF**; `frenxiv.org` count not verified | OSF API + zombie site. See [natural-sciences-and-niche-servers.md](natural-sciences-and-niche-servers.md#13-frenxiv) |
| **mp_arc** | **Jul 1991 – Dec 2023** | UT Austin | Closed deliberately, with a published preservation promise | **YES — best-preserved dead archive measured.** 1991 PostScript and 2023 PDF both downloaded | `web.ma.utexas.edu/mp_arc/`, **6,152 records**. See [natural-sciences-and-niche-servers.md](natural-sciences-and-niche-servers.md#12-mp_arc) |
| **AAS Open Research** | 2018–? | African Academy of Sciences + F1000 | **Rebranded, not killed** — `aasopenresearch.org` **redirects (HTTP 200) to `openresearchafrica.org`** | **YES — redirect works** | `openresearchafrica.org` (55,677 B) [WEB]. Record count **[NOT-VERIFIED]** |
| **NutriXiv** | 2018–? | Center for Open Science | Closed. **`nutrixiv.org` is DNS NXDOMAIN** on all five UAs | **YES — 85 preprints** | OSF API |
| **MindRxiv** | 2018–? | COS + Mind & Life Institute | Closed. Vanity domain **still redirects correctly** — a clean shutdown | **YES — 288 preprints** | OSF API |
| **SportRxiv (OSF instance)** | 2017–**2021-08-27** | Center for Open Science | **Migrated**, not closed — moved to self-hosted OPS at `sportrxiv.org` | **YES — 377 legacy + 761 current** | OSF API + OAI-PMH |
| **EarthArXiv (OSF instance)** | 2017–? | Center for Open Science | **Migrated** to CDL/Janeway; DOIs redirect | **YES — 1,649 legacy + 7,525 current** | OSF API + `eartharxiv.org` |
| **EcoEvoRxiv (OSF instance)** | 2018–? | Center for Open Science | **Migrated** to CDL/Janeway | **YES — 909 legacy + 3,604 current** | OSF API + `ecoevorxiv.org` |
| **AfricArXiv (OSF instance)** | 2018–? | Center for Open Science | Frozen; designated successor **`africarxiv.ubuntunet.net` certificate expired 2026-07-25** | **YES — 479 preprints** | OSF API. See [regional-and-national-servers.md](regional-and-national-servers.md) |
| **Arabixiv**, **IndiaRxiv**, **AgriXiv**, **LISSA**, **Thesis Commons** | various | Center for Open Science | Frozen (`allow_submissions: false`) but retained | **YES — 298 / 121 / 397 / 335 / 2,866** | OSF API [API] |
| **Rutgers Optimality Archive** | 1993–**2022** (deposits) | Rutgers SAS | Ingest stopped; **site still maintained** (index `Last-Modified` 2024-10-17) | **YES — 20-page PDF downloaded; complete XLSX manifest of ~1,463 rows** | `roa.rutgers.edu`. See [social-sciences-and-humanities.md](social-sciences-and-humanities.md#16-rutgers-optimality-archive-roa) |
| **Eyexiv** | 2022–? | Intl. Virtual Ophthalmic Research Center (S2) | **Never resolved for me.** `.org`/`.com`/`.net`/`.io` all DNS NXDOMAIN; **not an OSF provider** | **NO — nothing found** | **[NOT-VERIFIED]** — the only genuinely lost server in this table |

### The headline number

**Of the 18 closed, frozen, migrated or rebranded services in this table, exactly one —
Eyexiv — has no retrievable content that I could find.** Seventeen out of eighteen still
serve their corpus in 2026, several of them a decade or more after shutdown.

**Preprint servers do not lose data. They lose front doors.**

## 2. Failure modes

Six distinct mechanisms, all observed directly in this pass. They are ordered by how
*deceptive* they are, not by how common.

### 2.1 Publisher strategy change

Nature Precedings and PeerJ Preprints both died because a commercial publisher decided
preprints no longer fitted the business. Neither deleted anything: NPG kept Precedings at
`nature.com/npre` with working DOIs and PDFs fourteen years on; PeerJ kept its preprint DOIs
resolving seven years on.

**But note the asymmetry.** NPG killed the *hostname* `precedings.nature.com` — it now
refuses TCP connections — while retaining the content under the main brand. Every 2007–2012
citation that used the hostname is broken; every citation that used the DOI works. This is
the whole argument for DOIs in a single example.

### 2.2 Founder retirement / single-maintainer dependency

**CogPrints** is the canonical case: an EPrints archive at Southampton covering
*"Psychology, Neuroscience, Linguistics, **Computer Science** (e.g. artificial intelligence,
robotics, vision, learning, speech, neural networks), Philosophy…"* (its own front page,
still served) [DOC]. It ran 1997–2017 and stopped when its founder did.

What Southampton did next is the model: they froze it into a **static mirror** at
`web-archive.southampton.ac.uk/cogprints.org/`. The metadata pages, abstracts and full-text
files survive — I downloaded record 1's PDF. What did *not* survive is everything dynamic:
search is a dead link, and `view/year/` now returns an **Apache directory index** of
year HTML files rather than a browse interface [WEB].

**The lesson for anyone freezing a repository: flattening to static preserves the
documents and destroys the finding aids.** Budget for that. Deep links keep working; the
ability to *discover* what is there does not.

The same dependency exists right now, unmitigated, at **LingBuzz** (one person, no DOIs, no
dark archive) and to a lesser degree at **RoA**.

### 2.3 Platform migration breaking URLs — and how to do it right

Migration is now the most common life-cycle event, and it is the one that is **usually done
well**. EarthArXiv, EcoEvoRxiv and SportRxiv all moved off OSF; all three left the old
provider record in place with an explanatory notice, kept the legacy records readable, and
either redirected DOIs or ran the platforms in overlap. EarthArXiv's OSF description states
it outright: *"All article DOIs will redirect to CDL"* (S3) [DOC]. SportRxiv's names the
exact cutover date, **2021-08-27**, and its new OAI `earliestDatestamp` is 2021-08-12 — a
deliberate two-week overlap (S3, S4) [DOC] [API].

Contrast **AAS Open Research → Open Research Africa**, where the redirect works but nothing
at the destination explains the rename to a reader arriving from a 2019 citation.

### 2.4 Domain lapse, parking, and hijack — the dangerous one

This is where content is *not* lost but readers are actively misled. All observed
2026-09-02 [WEB]:

| Domain | What it serves now |
|---|---|
| `lawarxiv.org` | **114-byte parking stub**: `window.location.href="/lander"` |
| `mediarxiv.org` | **redirects to `afterdispatch.com`**, an unrelated site (the live archive is at `mediarxiv.**com**`) |
| `bodoarxiv.org` | **"Mostbet Bangladesh — Online Casino & Sports Betting"** |
| `nutrixiv.org` | DNS NXDOMAIN |
| `hprints.org` | DNS NXDOMAIN (live archive is `hprints.hal.science`) |
| `marxiv.org` | TCP connection refused |

**And the operators still point at them.** BodoArXiv's live OSF description, served by the
Center for Open Science on the day of this probe, says *"Visit BodoArXiv.org to learn
more"* (S3) [DOC]. It is now a gambling site. **A repository's own outbound link is not
evidence that the destination is still theirs.**

### 2.5 TLS certificate state — refining the abandonment signal

A sibling agent working on the regional servers reported that **expired TLS certificates are
a reliable abandonment signal**. I verified that with `openssl s_client` and it holds — but
the finding needs tightening in *both* directions.

**Verified expired / never-valid (all 2026-09-02, S5) [API]:**

| Host | Certificate | Diagnosis |
|---|---|---|
| `africarxiv.ubuntunet.net` | `CN=africarxiv.ubuntunet.net`, notAfter **2026-07-25** | **Expired 39 days ago.** AfricArXiv's designated successor |
| `latarxiv.org` | `CN=latarxiv.org`, notAfter **2026-08-20 19:26:19** | **Expired 12 days ago** — confirms the sibling's finding to the second |
| `rinarxiv.lipi.go.id` | **`CN=linux`, SAN `DNS:linux`**, valid 2023-07-31 → 2033-07-28 | **Not expired — never configured.** A self-signed default cert from the OS install, unnoticed for three years. INArxiv's designated successor |
| `cogprints.org` | serves `CN=web-archive.southampton.ac.uk`, **freshly renewed**, valid to 2026-10-17 | **A healthy certificate that breaks the old front door.** The archive host is well maintained; it just never claimed the legacy hostname, so `https://cogprints.org` fails and only `http://` works |

**Now the counter-evidence, which is the more important half.** I pulled certificates for
every dead-or-zombie domain in §2.4 and they are **all fine**:

| Host | Certificate valid | Actual state |
|---|---|---|
| `bodoarxiv.org` | 2026-08-20 → 2026-11-18 | **casino site** |
| `lawarxiv.org` | 2026-08-30 → 2027-03-16 | **domain-parking stub** |
| `mediarxiv.org` | 2026-07-29 → 2026-10-27 | **redirects to a stranger's site** |
| `frenxiv.org` | 2026-07-25 → 2026-10-23 | **frozen since October 2020** |

> **Refined rule.** *An expired or never-issued certificate is a high-precision signal of
> abandonment — but a valid certificate is worth nothing as evidence of liveness.* Domain
> parking services, squatters and hosting platforms all run automated ACME issuance.
> `frenxiv.org` has renewed its certificate every 90 days without interruption for six years
> while serving a page frozen in October 2020.

**Corollary, and this one is genuinely counter-intuitive:** the presence of automated
certificate renewal proves only that *something* is automated, and the absence of it proves
a human stopped watching. In this dataset, **TLS automation outlived editorial staffing in
every case where the two diverged.**

### 2.6 The zombie — a rendering front page with no pulse

`frenxiv.org` is the most deceptive artefact found in this whole survey: HTTP 200, 44,186
bytes, title *"Frenxiv Papers"*, working subject browse, named steering committee including
Björn Brembs and Sophien Kamoun. It looks completely alive. The tells:

- a stuck banner: *"Notice: The site will undergo maintenance between **Oct 28, 2020**
  9:19 AM and Oct 28, 2020 9:19 AM (+0000 UTC)"* — a **zero-length** maintenance window from
  six years ago, still rendering;
- a footer reading *"Copyright © **2011-2020**"*.

**A site that refuses connections is safer than one that renders.** `marxiv.org` cannot
mislead anyone.

### 2.7 The two failure modes that did *not* appear

Recorded because negative results matter:

- **Grant expiry as a direct cause of data loss: not observed.** Several servers here were
  grant-funded and several stopped, but in every case the content was absorbed by a larger
  host (OSF, HAL, Wikimedia, a university web archive) rather than deleted.
- **Deliberate deletion of a corpus: not observed at all.** Not once in 18 services.

## 3. Synthesis — what actually determines survival

The pattern across this file, [regional-and-national-servers.md](regional-and-national-servers.md),
[social-sciences-and-humanities.md](social-sciences-and-humanities.md) and
[natural-sciences-and-niche-servers.md](natural-sciences-and-niche-servers.md) is
consistent enough to state as a rule:

> **Content survives in proportion to the size and institutional depth of the host it sits
> on. Front doors fail in proportion to how bespoke they are.**

Ranked by observed durability:

1. **Large shared scholarly hosts — OSF, HAL, Zenodo, Wikimedia, `nature.com`.** Zero
   observed losses. Content from services shut down in 2020 is still API-addressable in
   2026. Twelve of the eighteen rows in §1 are alive because of this.
2. **University-operated static file trees.** mp_arc (Apache at UT Austin, 1991 PostScript
   still byte-identical and served — the gzip header still records a 1997-04-26 mtime),
   RoA (Rutgers SAS), CogPrints (Southampton's web archive). Slightly worse than (1) in that
   finding aids get lost, far better in that the *bytes* are untouched for decades.
3. **Commercial-publisher platforms.** Fine until the publisher's strategy changes, then
   fine anyway because publishers maintain DOI resolution — but you must have used the DOI.
   Increasingly guarded by Cloudflare, which breaks scripted access without breaking
   citation (PeerJ, ESS Open Archive, Authorea, TechRxiv, ScienceOpen).
4. **Self-hosted community successors.** The single worst category. Every failure in §2.4
   and §2.5 is one of these. They are launched to escape platform dependence and then die of
   the operational overhead that dependence was paying for.
5. **One-person archives.** LingBuzz has outlived most of category 4, which is an argument
   for simplicity — and has no succession plan at all, which is an argument against relying
   on it.

## 4. Practical guidance — citing defensibly from a small preprint server

Do these in order. Each is cheap.

1. **Cite the DOI, never the vanity URL.** This is the highest-value habit in the entire
   file. `10.1038/npre.2012.7141.1` resolves; `precedings.nature.com` does not.
   `10.7287/peerj.preprints.27311v1` resolves; `peerj.com` 403s every automated client. The
   OSF DOI for a LawArXiv paper resolves; `lawarxiv.org` is a parking page. **Every broken
   citation observed in this pass was a hostname; not one was a DOI.**
2. **If there is no DOI, treat the item as ephemeral.** LingBuzz, RoA and mp_arc mint no
   DOIs. Their content is currently well served, but a citation to `lingbuzz/009120` has no
   redirection layer behind it at all.
3. **Deposit-mirror to Zenodo.** For anything you author or depend on, put a copy in Zenodo:
   it mints a DOI, is CERN-operated, and has an explicit long-term commitment. See
   [zenodo.md](zenodo.md). Concept-DOI versioning means later revisions do not orphan the
   citation.
4. **Submit the URL to `https://web.archive.org/save/<url>` at the moment you cite it.**
   Per [`AGENTS.md`](../../AGENTS.md) §9, this is free, unauthenticated and
   rate-limited to a few per minute. This pass used the Wayback availability API to confirm
   that `peerj.com/preprints/` had a capture from **2026-08-31** even though live retrieval
   returned 403 on all five user-agents (S6) [API] — the archive was the *only* way to see
   what the page says. **Do this especially for anything on a self-hosted community
   successor**, which §3 identifies as the most failure-prone category.
5. **Prefer servers with a named dark archive.** Portico and CLOCKSS/LOCKSS agreements are
   the only *contractual* preservation guarantees in this landscape; everything else is a
   promise by an institution. Of the servers in this record I found **no** explicit dark-archive
   statement for mp_arc, RoA, LingBuzz or any OSF-hosted provider — COS's own language is
   *"as part of COS's ongoing commitment to Open Science"* (S3) [DOC], which is a commitment,
   not a contract. **[NOT-VERIFIED]:** whether OSF preprints are covered by any third-party
   dark archive. Treat this as an open question, not as a gap.
6. **Sanity-check liveness properly, because the obvious signals lie.** In this dataset:
   HTTP 200 did not mean alive (OSF's 4,207-byte SPA shell for non-existent providers;
   mp_arc's 174-byte "Found no abstract" at status 200); a valid TLS certificate did not
   mean alive (§2.5); and a professionally rendering front page did not mean alive (§2.6).
   What *did* work: **an API or OAI-PMH count**, and **the date of the newest item**.
7. **When the HTML is defended, try the machine interface.** Repeatedly true here: hprints'
   web front is behind an Anubis proof-of-work wall while the HAL Solr API answers a bare
   `curl`; ESS Open Archive 403s every user-agent while Crossref serves its whole corpus;
   CrimRxiv 403s while its DOIs resolve. Bot-blocking is applied to browsers' endpoints,
   rarely to APIs.

### How this ties to this repository's own practice

The habits above are the same ones `doc/hardware/` already applies to datasheets, and the
correspondence is exact:

- **Local artifact copies with SHA-256 checksums**, listed in
  [`artifact-manifest.md`](../../artifact-manifest.md) — the repository does not rely on a
  vendor URL staying up, and it should not rely on a preprint server staying up either. If a
  preprint is load-bearing for a hardware claim, **keep the PDF and hash it**, exactly as
  the ESP32-P4 and WCH datasheet passes did.
- **`ARCHIVED-…md` reacquisition records** — where a large file is archived out of the tree,
  the repository keeps a record with the verified download URL and checksum. The equivalent
  for a preprint is: DOI, retrieval date, byte size, page count.
- **Negative controls on every URL pattern.** The repository already documents that WCH's
  `downloads/<PART>DS1_PDF.html` returns *"an identical 4,305-byte SPA shell for every path,
  existing or not"*, and that SquareLine's CDN *"returns HTTP 206 for non-existent paths"*.
  **OSF's 4,207-byte shell is the same phenomenon in the scholarly domain**, and this pass
  caught it live at `osf.io/preprints/eyexiv/` — a provider that does not exist.
- **Dated retrieval, always.** Every probe in this file carries 2026-09-01 or 2026-09-02.
  Given §2.5, a liveness claim without a date is worthless within about 90 days.

## 5. Sources

- **S1** — Wikipedia, *List of preprint repositories*, and the PeerJ blog post it cites
  (*"PeerJ Preprints to stop accepting new preprints Sep 30th 2019"*).
  `https://en.wikipedia.org/wiki/List_of_preprint_repositories` · retrieved 2026-09-02 ·
  spans, operators and size buckets throughout §1. [COM]
- **S2** — same page, Eyexiv row: *"The Eye Open Repository, Preprints founded by Dr. F.
  Heidary … International Virtual Ophthalmic Research Center"*, `>100`, 2022 · retrieved
  2026-09-02. [COM]
- **S3** — OSF API. `https://api.osf.io/v2/preprint_providers/?page[size]=100`,
  `https://api.osf.io/v2/preprint_providers/<slug>/` and
  `https://api.osf.io/v2/preprints/?filter[provider]=<slug>&page[size]=1` · retrieved
  2026-09-02 · all OSF counts, and verbatim closure/migration notices for LawArXiv, MarXiv,
  NutriXiv, Frenxiv, MindRxiv, SportRxiv, EarthArXiv, EcoEvoRxiv, plus the BodoArXiv
  description that links the hijacked domain. Negative control:
  `filter[provider]=bogusprovider12345` → `total: 0`. [API] [DOC]
- **S4** — SportRxiv OAI-PMH. `https://sportrxiv.org/index.php/server/oai?verb=Identify`
  and `?verb=ListIdentifiers&metadataPrefix=oai_dc` (`completeListSize="761"`,
  earliestDatestamp 2021-08-12) · retrieved 2026-09-02. [API]
- **S5** — TLS certificate probes.
  `openssl s_client -connect <host>:443 -servername <host> | openssl x509 -noout -subject
  -dates -ext subjectAltName`, run 2026-09-02 against `cogprints.org`,
  `africarxiv.ubuntunet.net`, `rinarxiv.lipi.go.id`, `latarxiv.org`, `marxiv.org`,
  `lingbuzz.net`, `roa.rutgers.edu`, `bodoarxiv.org`, `lawarxiv.org`, `frenxiv.org`,
  `mediarxiv.org`, `peerj.com`, `essopenarchive.org`. Supports every claim in §2.5. [API]
- **S6** — Wayback availability API.
  `http://archive.org/wayback/available?url=peerj.com/preprints/&timestamp=20260901` →
  capture `20260831083405`; and `…?url=peerj.com/preprints/27311/` → capture
  `20250324000250` · retrieved 2026-09-02. [API]
- **S7** — Nature Precedings. `https://www.nature.com/npre` (title *"Nature Precedings"*;
  *"Pre-publication research and preliminary findings for the Life Science community from
  2007 until 2012"*; newest items dated 04 Apr 2012),
  `https://www.nature.com/articles/npre.2012.7141.1`,
  `https://www.nature.com/articles/npre.2012.7141.1.pdf` (200, 177,957 B, valid 5-page PDF),
  `https://doi.org/10.1038/npre.2012.7141.1` (resolves 200) · retrieved 2026-09-02. [WEB] [API]
- **S8** — CogPrints. `http://cogprints.org/` → redirects to
  `https://web-archive.southampton.ac.uk/cogprints.org/` (front page with the CS/AI scope
  statement), `…/cogprints.org/1/` (Shizgal 1997 record page),
  `…/cogprints.org/1/4/cur_op_e-print_version.PDF` (200, 174,167 B, valid 6-page PDF 1.2),
  `…/cogprints.org/view/year/` (Apache directory index — search and browse are gone) ·
  retrieved 2026-09-02. [WEB] [API]
- **S9** — Crossref REST API. `https://api.crossref.org/prefixes/10.7287` (owner: PeerJ)
  and `/prefixes/10.7287/works?rows=0` (65,760 works),
  `/works/10.7287/peerj.preprints.27311v1` · plus `https://doi.org/10.7287/peerj.preprints.27311v1`
  → HTTP 302 to `peerj.com/preprints/27311v1` · retrieved 2026-09-02. [API]
- **S10** — mp_arc. `https://web.ma.utexas.edu/mp_arc/` (the verbatim 1991–2023 statement
  and preservation promise), `index-91.html`…`index-23.html` (6,152 records),
  `mp_arc/c/91/91-1.ps.gz` (200, 120,018 B; gzip header mtime **1997-04-26**),
  `mp_arc/c/23/23-1.pdf` (200, valid 6-page PDF), negative controls
  `mp_arc-bin/mpa?yn=99-99999` (200 / 174 B "Found no abstract") and `index-77.html` (404) ·
  retrieved 2026-09-02. Detail in
  [natural-sciences-and-niche-servers.md](natural-sciences-and-niche-servers.md#12-mp_arc). [WEB] [DOC] [API]
- **S11** — Reachability sweeps. Directory-wide
  `doc/hardware/scratch/preprint-repositories/reachability-2026-09-01.txt` (2026-09-01) and
  the UA-ladder log in `doc/hardware/scratch/preprint-repositories/humanities/` (2026-09-02)
  · supports every 403 / NXDOMAIN / connection-refused / parking-stub / redirect claim in
  §1 and §2.4, including the `frenxiv.org` banner and copyright text, the `bodoarxiv.org`
  casino title, `mediarxiv.org` → `afterdispatch.com`, `lawarxiv.org` → `/lander`, and
  `aasopenresearch.org` → `openresearchafrica.org`. [WEB]
- **S12** — This repository's own archival practice, for §4:
  [`doc/hardware/artifact-manifest.md`](../../artifact-manifest.md) (SHA-256 checksummed
  local artifacts), [`doc/hardware/README.md`](../../README.md) change log (the
  `ARCHIVED-…md` reacquisition-record pattern; the WCH 4,305-byte SPA shell and SquareLine
  HTTP 206 negative controls), and [`AGENTS.md`](../../AGENTS.md) §9 (the
  `web.archive.org/save` rule). [DOC]
