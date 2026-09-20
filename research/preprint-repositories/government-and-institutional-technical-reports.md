# Government and institutional technical reports — the grey literature of electronics

- **Compiled:** 2026-09-02. Every figure was measured on that date unless stated otherwise.
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).
- **Companion record:** [`open-access-full-text-sources.md`](open-access-full-text-sources.md) —
  the decision ladder for finding a *published paper* for free. This file is the rung-8 fallback
  in that ladder: **what to do when the thing you are looking for was never a paper.**

> **The claim this record makes.** An enormous fraction of real electronics, firmware and systems
> engineering knowledge was never published as a journal article and was never posted to a preprint
> server. It exists as a **technical report** — a numbered, institutionally-published document from
> a government laboratory, a university department or a corporate research division. None of the
> resolvers in the companion record will find it, because most of it has no DOI. **The RISC-V
> instruction set specification is the cleanest example: it is a Berkeley EECS technical report,
> and [`arxiv.md` §7.5](arxiv.md) already established it is not on arXiv.**

---

## 1. Why grey literature matters for hardware

Three structural reasons, and they compound.

**Reason one: the work was funded to produce a report, not a paper.** A NASA radiation-effects
qualification campaign, a DOE national-laboratory detector build, a DARPA-funded prototype — the
contractual deliverable is a report with a number on it. A conference paper, if one appears at all,
is a compressed summary written afterwards for career reasons. **The report has the data; the paper
has the story.** For anyone actually building hardware, the report is the more useful document: it
contains the test matrix, the part numbers, the failure modes and the appendices.

**Reason two: some documents are constitutionally not papers.** An instruction-set specification, a
calibration procedure, a reliability handbook and a design manual are not research contributions
and no journal would take them. They are still the primary sources for their fields. RISC-V, the
Bell System Technical Journal's device physics, the MIT AI Memo series and the DEC SRC research
reports are all in this category.

**Reason three: this material is disproportionately free, and disproportionately fragile.**
US federal reports are largely public-domain government works — no paywall, no licence, bulk APIs.
But corporate report series depend on one company continuing to host one directory, and companies
get acquired. §4 documents two collections whose original hosts are gone.

**Practical consequence for the ladder:** if Unpaywall, Semantic Scholar and OpenAlex all return
nothing for something that plainly exists, stop searching the article layer and ask *which
institution produced this, and does it run a report series?*

---

## 2. US federal report servers

### 2.1 NASA NTRS — the NASA Technical Reports Server

- **URL:** https://ntrs.nasa.gov/ · **API:** `https://ntrs.nasa.gov/api/citations/search`
- **Coverage:** NASA and NACA output. The `published` facet returns **117 distinct year buckets**
  [API], reaching back through the NACA era. (It also contains obvious date-entry corruption —
  the lowest bucket key is `0202` — so do not build a time series without cleaning.)

NTRS is the single best free source of **spacecraft and avionics electronics engineering** in
existence. Not because NASA is unusually generous, but because NASA's engineering culture produces
documents: radiation-hardness assurance, single-event-effect test campaigns on named commercial
parts, EMC and grounding practice, connector and solder-joint reliability, materials outgassing,
power-system design, FPGA and processor qualification.

**Measured size, 2026-09-02** [API] (S1):

| Measure | Count |
|---|---|
| Total records | **646,950** |
| `disseminated: DOCUMENT_AND_METADATA` (**the PDF is there**) | **358,213** (55.4%) |
| `disseminated: METADATA_ONLY` (citation only) | **288,737** (44.6%) |
| `distribution: PUBLIC` | 646,950 — i.e. **everything the public API returns is public** |

**Read that second row before you rely on NTRS.** Nearly half of NTRS records are citations with
no attached document. The `disseminated` field tells you which, and you can filter on it. A
harvester that assumes every hit has a PDF will be wrong 44.6% of the time.

**Document-type mix** [API] (S1):

| `stiType` | Count |
|---|---|
| `CONFERENCE_PAPER` | 150,828 |
| `REPRINT` (the published version of a journal article) | 150,204 |
| `OTHER` | 99,466 |
| **`CONTRACTOR_REPORT`** | **71,868** |
| `PRESENTATION` | 44,776 |
| **`TECHNICAL_MEMORANDUM`** | **29,425** |
| `PREPRINT` | 22,767 |
| `ABSTRACT` | 22,547 |

`CONTRACTOR_REPORT` and `TECHNICAL_MEMORANDUM` — 101,293 documents between them — are the classic
grey literature: work done under contract by Lockheed, Boeing, Jet Propulsion Lab subcontractors
and universities, that exists nowhere else.

**By centre**: `CDMS` 381,853 (the bulk legacy load), `GSFC` 42,105, `JPL` 41,531, `LaRC` 28,285,
`MSFC` 23,047, `ARC` 22,576, `JSC` 21,051, `GRC` 18,551 [API] (S1).

#### The API

```bash
# search — no key, no UA fallback needed, plain curl works
curl -s "https://ntrs.nasa.gov/api/citations/search?q=radiation%20hardened&size=10"

# single record
curl -s "https://ntrs.nasa.gov/api/citations/20150022446"

# the PDF, straight out of the record's downloads[] array
curl -sL -o out.pdf "https://ntrs.nasa.gov/api/citations/20150022446/downloads/20150022446.pdf"
```

The search response is Elasticsearch-shaped and **the aggregations are the good part**. Every
query returns facet buckets for `author`, `center`, `reportNumber`, `fundingNumber`,
`subjectCategory`, `stiType`, `stiTypeDetails`, `keyword`, `organization`, `distribution`,
`disseminated`, `created`, `modified` and `published` — so one call gives you both the results
*and* a map of who works on the topic and under which contract numbers. `fundingNumber` in
particular lets you walk an entire programme.

**Two traps** [API] (S1, S2):

- **`q=` with an empty value returns `total: 0`.** `?q=&size=1` → 0 records. Omitting `q`
  entirely, or `q=*`, both return the true 646,950. A harvester that builds its URL by string
  concatenation and leaves `q=` empty will silently record zero for everything.
- **Negative control is clean:** `GET /api/citations/99999999999` → **HTTP 404, 40-byte body**.
  NTRS status codes can be trusted, unlike several hosts in
  [`retrieval-notes.md`](retrieval-notes.md).

#### What an electronics engineer actually finds there

Measured hit counts, 2026-09-02 [API] (S1, S3):

| Query | Hits | Sample first result |
|---|---|---|
| `radiation hardened` | **304** | *Decline in Radiation Hardened Microcircuit Infrastructure* (`20150022446`, GSFC) |
| `FPGA single event upset` | **55** | *Single event upset susceptibility testing of the Xilinx Virtex II FPGA* |
| `SpaceCube` | **47** | *Adapting the SpaceCube v2.0 Data Processing System for Mission-Unique…* |

Drill into the `radiation hardened` result set and the shape of NASA's electronics literature is
immediately visible [API] (S1):

- **Subject categories:** *Electronics And Electrical Engineering* 96 · *Space Radiation* 29 ·
  *Computer Operations And Hardware* 14 · *Spacecraft Instrumentation And Astrionics* 14 ·
  *Quality Assurance And Reliability* 9 · *Solid-State Physics* 7
- **Top authors:** Kenneth A. LaBel (21), Andrew S. Keys (12), James H. Adams (8),
  John D. Cressler (7), Melanie D. Berg, Jean-Marie Lauenstein — i.e. the actual NEPP
  (NASA Electronic Parts and Packaging) community, findable by name
- **Keywords** include `single-event effect (SEE)`, `NASA Electronic Parts and Packaging (NEPP)
  Program`, `Radiation Hardness Assurance`, `Shields-1`, `SpaceCube`
- **Contributing organisations** include commercial part vendors — *Celis Semiconductor
  Corporation*, *Linear Technology Corp.*, *National Semiconductor Corp.* — which means **NTRS
  contains vendor radiation data that never appeared on a datasheet**

**Use `reportNumber` as a facet.** It surfaces the real identifier series — `JPL-Publ-`, `E-`
(Glenn), `ARC-E-DAA-TN`, `AED-R-`, and NEPP's own `NNNN-NNN-NEPP` — which is how you find the rest
of a programme once you have one document from it.

### 2.2 OSTI.GOV and DOE PAGES — the US Department of Energy

- **URL:** https://www.osti.gov/ · **API:** `https://www.osti.gov/api/v1/records`
- **DOE PAGES:** https://www.osti.gov/pages/ (200, 125,342 B [WEB])

OSTI is the DOE's Office of Scientific and Technical Information. What is in it, from an
electronics point of view: **national-laboratory instrumentation** (Argonne, Brookhaven, Fermilab,
Oak Ridge, Sandia, Los Alamos, LLNL, PNNL, NREL, SLAC), particle and photon **detectors** and their
readout ASICs, **power electronics** and grid hardware, **battery and energy-storage** work,
**semiconductor materials and process**, pulsed-power and high-voltage engineering, and the
control-system software that runs all of it.

**DOE PAGES** (Public Access Gateway for Energy and Science) is the DOE's public-access mandate
layer: accepted manuscripts of DOE-funded journal articles, free after any embargo. It is to DOE
what PMC is to NIH.

**Measured, 2026-09-02** — OSTI returns totals in an **`x-total-count` response header**, not in
the body, which is easy to miss [API] (S4):

```bash
curl -sD - -o /dev/null "https://www.osti.gov/api/v1/records?rows=1&q=power+electronics" | grep -i x-total-count
```

| Query | `x-total-count` |
|---|---|
| `power electronics` | **377,043** |
| `detector` | **258,839** |
| `battery` | **234,889** |
| `semiconductor` | **90,818** |
| `riscv` | **34** |

**Record shape and the full-text link** [API] (S4, S5) — this is the field that matters:

```json
{ "osti_id": "2584705",
  "title": "Development and Optimization of a 10-Stage Solid-State Linear Transformer Driver",
  "report_number": "DOE/NV/03624-2234",
  "contract_number": "NA0003624",
  "publication_date": "2025-08-25T00:00:00Z",
  "product_type": "Program Document",
  "links": [ {"rel":"citation","href":"https://www.osti.gov/biblio/2584705"},
             {"rel":"fulltext","href":"https://www.osti.gov/servlets/purl/2584705"} ] }
```

**`links[].rel == "fulltext"` → `https://www.osti.gov/servlets/purl/<osti_id>` is a stable direct
PDF route.** Verified: that URL for `2584705` returned **HTTP 200, 6,066,387 bytes, magic
`%PDF-`** (S5). Records without a `fulltext` link are metadata-only.

Note that `doi` was `null` on this record. **This is the whole point of the file.** A DOE report
with a report number and no DOI is invisible to every resolver in the companion record.

**Traps and negative controls** [API] (S4):

- **`q=` empty returns `x-total-count: 0`** — the *same* trap as NTRS. Two independent federal
  services share it; assume it is the default behaviour of this class of API.
- A nonsense search term → `x-total-count: 0` (correct).
- `GET /api/v1/records/999999999999` → **HTTP 404, 105-byte body** (clean).

Other useful query fields on the API: `report_number`, `contract_number` (walk a whole contract),
`research_org`, `sponsor_org`, `product_type`.

### 2.3 DTIC — Defense Technical Information Center

- **URL:** https://discover.dtic.mil/ · Probed 2026-09-02: home **HTTP 200, 466,561 B**;
  `?q=radiation` **HTTP 200, 386,731 B** [WEB] (S6). Chrome-131 UA; no fallback needed.

DTIC is the US defense department's report repository, and it is the deepest single source for
**military electronics, EMC/EMI, RF and antenna engineering, materials, human factors, and
reliability physics** — including a very large body of 1950s–1980s work that predates and
underpins much of the commercial state of the art.

**What is public and what is not — be precise about this:**

- The public `discover.dtic.mil` interface serves documents cleared for **public release with
  unlimited distribution** (the "Distribution Statement A" marking). These are free, full-text
  PDFs, no account.
- **Everything else is not there.** Distribution Statements B–F (limited to government agencies,
  contractors, DoD components) and anything classified are held on a **registered** side that
  requires DoD, federal-agency or approved-contractor credentials. Access is by eligibility, not by
  payment.
- **Do not read absence as non-existence.** A DTIC accession number that returns nothing publicly
  usually means the document exists under a limiting distribution statement. Conversely, do not try
  to route around it — that is an explicit access control, and `AGENTS.md` rule 7 applies.

**Practical note:** DTIC's public site and its own disclaimer text now refer to the
"Department of War" [WEB], reflecting the department's renaming — worth knowing when matching
older citations that say "Department of Defense".

**Historical caution:** an enormous number of scanned DTIC PDFs are OCR of poor microfiche. Search
will miss documents whose OCR failed. Browse by accession-number range around a document you
already have.

### 2.4 NIST — measurement, standards, cryptography, metrology

- **URLs:** https://www.nist.gov/publications (200, 116,978 B) ·
  https://csrc.nist.gov/publications/fips (200, 140,880 B) · full-text host
  `https://nvlpubs.nist.gov/` [WEB] (S7)

NIST publications are **US government works, free, and generally in the public domain**. For this
knowledge base the relevant series are:

| Series | What it is | Hardware relevance |
|---|---|---|
| **FIPS** | Federal Information Processing Standards | FIPS 140-3 (crypto module security), FIPS 197 (AES), FIPS 202 (SHA-3), FIPS 203/204/205 (post-quantum) |
| **SP 800-** | Computer security | Firmware resilience, supply-chain, key management |
| **SP 500-** | Computer systems technology | |
| **NISTIR / NIST TN** | Internal reports and technical notes | Electronics metrology, EMC, calibration, materials |
| **JRes NIST** | *Journal of Research of NIST* | Measurement science, fully free |

**Verified retrieval and negative control** [WEB] (S7), 2026-09-02:

| URL | Result |
|---|---|
| `https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-193.pdf` | **200, 516,802 B, `%PDF-`** |
| `https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-99999.pdf` *(control)* | **404, 1,380 B** |

The `nvlpubs.nist.gov` URL pattern is predictable and the status codes are honest — one of the
cleanest hosts probed across this whole survey. `NIST.SP.800-193` is *Platform Firmware Resiliency
Guidelines*, which is squarely a hardware/firmware document and a good illustration of why NIST
belongs in a hardware knowledge base.

**Cryptography cross-reference:** NIST runs the standardisation process (AES, SHA-3, the
post-quantum competition) whose *research* literature lives in the IACR Cryptology ePrint Archive.
The two are complements: ePrint has the cryptanalysis, NIST has the ratified specification. See
[`cryptology-eprint-archive.md`](cryptology-eprint-archive.md).

### 2.5 NTIS, GAO and CRS

**NTIS / NTRL** — the National Technical Reports Library, https://ntrl.ntis.gov/NTRL/
(200, 115,425 B [WEB]). In NTIS's own words (S8):

> "The National Technical Information Service acquires, indexes, abstracts, and archives the
> **largest collection of U.S. government-sponsored technical reports in existence**. The NTRL
> offers online, **free and open access** to these authenticated government technical reports."

NTIS's historical role was selling reports; the free-access position is comparatively recent and is
the reason NTRL is worth checking. It is the broadest federal net — it catches agencies that have
no NTRS/OSTI-equivalent of their own. **Item count: [NOT-VERIFIED]** — no machine-readable total
was obtained on the probe date.

**GAO** (Government Accountability Office) — **blocked on the probe date.** `https://www.gao.gov/`
→ **HTTP 403, 363-byte body**; `https://www.gao.gov/reports-testimonies` → **HTTP 403, 386 bytes**,
both with the Chrome-131 UA (S9). This is a *third* distinct 403 fingerprint in this survey:
neither the ~5.6 kB Cloudflare challenge nor the ~651 kB SHERPA body documented in the
[companion record §7](open-access-full-text-sources.md#7-probe-status-table). GAO reports are free
in principle; **not verified on this date.**

**CRS** (Congressional Research Service) — `https://crsreports.congress.gov/` → **HTTP 200,
345,391 B** [WEB] (S10). Since 2018 CRS reports have been published officially and free. They are
policy analysis, not engineering, but they are unusually good at *context*: semiconductor supply
chain, export controls, critical minerals, spectrum allocation, defense acquisition. Cite them for
"why is this the way it is", never for a measurement.

---

## 3. University technical-report series

**The key insight: many foundational computing documents are technical reports, not papers.**
Departments assign report numbers, host PDFs, and never submit the document anywhere. The
following are the series that a systems or hardware reader will actually need.

### 3.1 UC Berkeley EECS — where RISC-V actually lives

- **URL:** https://www2.eecs.berkeley.edu/Pubs/TechRpts/
- **Identifier form:** `UCB/EECS-<year>-<n>`
- **URL pattern:** `https://www2.eecs.berkeley.edu/Pubs/TechRpts/<year>/EECS-<year>-<n>.{html,pdf}`

> **Access caveat, stated first.** `www2.eecs.berkeley.edu` (128.32.139.28) was **TCP-unreachable
> from this environment** on 2026-09-02 — raw connections to both port 443 and port 80 timed out,
> and `curl` returned `http=000` after 25 s with every user agent tried (S11). This is *not* the
> same as a 403 or a 404; nothing answered at all. **It is recorded as "unreachable from here", not
> as "dead"** — one host on one day from one network is not evidence of a global outage, and the
> site is widely used. **Every record below was therefore verified from Internet Archive replays,
> which serve the department's own generated report pages verbatim, including their BibTeX and
> EndNote blocks** (S12).

**The RISC-V technical reports — verified, with exact numbers** [WEB via Wayback] (S12):

| Report number | Title | Authors | Date |
|---|---|---|---|
| **UCB/EECS-2011-62** | **The RISC-V Instruction Set Manual, Volume I: Base User-Level ISA** | Andrew Waterman, Yunsup Lee, David A. Patterson, Krste Asanović | **2011-05-13** |
| **UCB/EECS-2011-63** | Improving Energy Efficiency and Reducing Code Size with RISC-V Compressed | Andrew Waterman (MS thesis; advisors Patterson & Asanović) | 2011-05-13 |
| **UCB/EECS-2014-54** | The RISC-V Instruction Set Manual, Volume I: User-Level ISA, **Version 2.0** | Waterman, Lee, Patterson, Asanović | 2014-05-06 |
| **UCB/EECS-2016-1** | **Design of the RISC-V Instruction Set Architecture** | Andrew Waterman (PhD dissertation) | 2016-01-03 |
| **UCB/EECS-2016-118** | The RISC-V Instruction Set Manual, Volume I: User-Level ISA, **Version 2.1** | Waterman, Lee, Patterson, Asanović | 2016-05-31 |
| **UCB/EECS-2016-161** | The RISC-V Instruction Set Manual **Volume II: Privileged Architecture Version 1.9.1** | Waterman, Lee, **Rimas Avizienis**, Patterson, Asanović | 2016-11-04 |

Canonical URLs (from the department's own BibTeX `URL` field, quoted in the archived pages):

```
https://www2.eecs.berkeley.edu/Pubs/TechRpts/2011/EECS-2011-62.pdf   # ISA v1, May 2011
https://www2.eecs.berkeley.edu/Pubs/TechRpts/2011/EECS-2011-63.pdf   # RVC / compressed
https://www2.eecs.berkeley.edu/Pubs/TechRpts/2014/EECS-2014-54.pdf   # User-Level ISA 2.0
https://www2.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-1.pdf    # Waterman PhD
https://www2.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-118.pdf  # User-Level ISA 2.1
https://www2.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-161.pdf  # Privileged 1.9.1
```

Two of the PDFs were retrieved through the Wayback replay and checked for magic bytes (S12):
`EECS-2011-62.pdf` → **376,630 B, `%PDF-1.4`**; `EECS-2016-1.pdf` → **959,927 B, `%PDF-1.4`**.

**Citation form.** The department generates BibTeX for every report. UCB/EECS-2011-62 is a
`@techreport` with `Institution = {EECS Department, University of California, Berkeley}` and
`Number = {UCB/EECS-2011-62}`; UCB/EECS-2011-63 is a `@mastersthesis`. Use those, not an invented
`@misc`.

**Why this matters.** [`arxiv.md` §7.5](arxiv.md) recorded, after searching, that
*"the foundational RISC-V documents are UC Berkeley EECS technical reports and RISC-V International
specifications, not arXiv preprints"*, and marked any canonical RISC-V arXiv landmark
**[NOT-VERIFIED]**. **This record closes that loop with the exact identifiers.** The 250 arXiv
papers matching `ti:"RISC-V" AND cat:cs.AR` are downstream work; the specification itself is
`UCB/EECS-2011-62` and its successors. For the *current* ISA specifications, see §5 — they moved to
RISC-V International in 2015.

**The series is much larger than RISC-V.** Berkeley EECS technical reports include the department's
PhD dissertations and MS theses, which is where a great deal of Chisel, Rocket, BOOM, Hwacha, gem5-
adjacent and BAR/ASPIRE-lab work is documented in far more detail than the conference papers.
**[NOT-VERIFIED]** for specific additional report numbers: further Wayback probes for candidate
numbers returned `http=000`, which is the Internet Archive rate-limiting already recorded in
[`retrieval-notes.md`](retrieval-notes.md), not evidence of absence.

### 3.2 MIT

- **DSpace@MIT:** https://dspace.mit.edu/ — the institutional repository, handle-based
- **CSAIL publications:** https://publications.csail.mit.edu/

Verified 2026-09-02 [WEB] (S13):

| Resource | Result |
|---|---|
| `https://dspace.mit.edu/handle/1721.1/5460` | 200, 460,148 B — collection titled **"AI Memos (1959 – 2004)"** |
| `https://dspace.mit.edu/handle/1721.1/6453` | 200, 558,625 B — an individual memo, *Simplifying Decision Trees* |
| `https://publications.csail.mit.edu/ai/` | 200 — "historical collection of the former Artificial Intelligence Laboratory Publications Series" |

**The AI Memo series (1959–2004) is the single most historically important university report series
in computing**, and it is free. CSAIL's own framing [DOC]: the AI Lab and the Laboratory for
Computer Science merged on **1 July 2003** to form CSAIL, and the AI Memos and AI Technical Reports
are browsable "by number (older documents) or by year (newer documents)".

DSpace@MIT is also where MIT theses live, and MIT theses are frequently the only full description
of a piece of hardware. Handles (`1721.1/nnnn`) are persistent identifiers — prefer them to
`dspace.mit.edu` URLs in citations.

### 3.3 CMU

- **SCS Technical Report Collection:** http://reports-archive.adm.cs.cmu.edu/ — **HTTP 200,
  2,820 B** [WEB] (S14)

A plain, old, working index. Its own sub-collections, quoted from the page (S14):

> "Computer Science Technical Reports · Robotics Institute Technical Reports · Center for Automated
> Learning and Discovery Reports · Machine Learning Department Reports · Language Technologies
> Institute · Human-Computer Interaction Institute · Institute for Software Research · Lane Center
> for Computational Biology · Information Technology Center · **Special Collections: Mach
> Publications, Real-Time Mach Publications, Fox Publications, Parallel Data Laboratory (PDL)
> Publications, Software Engineering Institute (SEI) Publications**"

Those special collections are the reason to care. **Mach** (the microkernel under macOS and iOS),
**Fox** (the Standard ML compiler and networking work) and the **PDL** (RAID, storage systems,
NASD) are documented here at a level of detail the conference papers do not reach. The SEI
collection is the source for CMMI, architecture-tradeoff methods and a large body of software
safety/reliability practice.

**Note the newer host:** `https://kilthub.cmu.edu/` — CMU's figshare-backed repository — returned
**HTTP 202 with a zero-byte body** to a plain GET (S15). That is exactly the figshare behaviour
already recorded in [`retrieval-notes.md` §5](retrieval-notes.md): *"`figshare.com` returned HTTP
202 with a zero-byte body — neither success nor a usable error."* Confirmed on a second figshare
tenant.

### 3.4 Stanford

- **Historical index:** http://i.stanford.edu/TR/ — **HTTP 200, 1,332 bytes** [WEB] (S16)

A 1,332-byte hand-written HTML page, and it is genuinely the map. Its contents, verbatim:

- CS Department technical reports, by decade: `cstr6x.html`, `cstr7x.html`, `cstr8x.html`,
  `cstr9x.html` (**1960s through 1990s**)
- CS Department **Technical Notes**: `cstn.html`
- **Computer Systems Laboratory** technical reports: `csltr6x7x.html`, `csltr8x.html`,
  `csltr9x.html`
- And an explicit pointer: *"For CS technical reports 2000-present, see
  http://hci.stanford.edu/cstr"*

The 1960s–1970s Stanford CS reports are the AI-lab-era documents (SAIL); the Computer Systems
Laboratory series is the hardware side. **This is a good example of the general pattern: the
authoritative index for a 40-year report series is a static page nobody has touched in years, and
it works.** It is also a good candidate for `web.archive.org/save/` under `AGENTS.md` rule 9 —
a single unmaintained page holding the only map of a major series.

### 3.5 Cambridge Computer Laboratory

- **URL:** https://www.cl.cam.ac.uk/techreports/ — **HTTP 200, 10,247 B** [WEB] (S17)
- **ISSN 1476-2986**, published continuously **since 1974** [DOC]

The best-organised university report series probed in this pass. From the department's own page
(S17):

> "The Department of Computer Science and Technology (formerly the Computer Laboratory) has
> published a Technical Report series (ISSN 1476-2986) since **1974**. Technical reports are
> intended primarily for the long-term archival of results and descriptions that are not suitable
> for publication elsewhere, due to their length or nature. Technical reports are also a common way
> to make a departmental PhD thesis widely available. **Most newer technical reports, in particular
> all published since 2002, are available online in PDF.** Older reports can be scanned on request."

**URL pattern and verification** [WEB] (S17, S18):

```
https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-<n>.html   # abstract page
https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-<n>.pdf    # full text
```

| Probe | Result |
|---|---|
| `UCAM-CL-TR-630.pdf` | **200, 11,754,717 B, `%PDF-`** |
| `UCAM-CL-TR-630.html` | 200, 8,215 B |
| `UCAM-CL-TR-99999.pdf` *(negative control)* | **404, 279 B** |
| Highest report number linked from the index on 2026-09-02 | **1009** |

**Note the trailing-slash trap:** `.../techreports/UCAM-CL-TR-630/` (with a slash) returns **404**.
The identifier is a filename, not a directory.

**A worked hardware example.** `UCAM-CL-TR-630` is **Sergei P. Skorobogatov, *Semi-invasive
attacks – A new approach to hardware security analysis*, April 2005, 144 pages** — his PhD
dissertation, issued as a technical report, **with DOI `10.48456/tr-630`** (S18). It is a
foundational document for optical fault injection and chip-level attack methodology, and it is
free. Note that Cambridge **now mints DOIs for its technical reports** (`10.48456/tr-<n>`), which
makes them resolvable by the tools in the companion record — most university series do not.

**Machine access** — Cambridge publishes the catalogue in seven formats (S17):

| Format | File |
|---|---|
| BibTeX | `UCAM-CL-TR.bib` |
| **OAI-PMH** | `UCAM-CL-TR-OAI-SR.xml` (static repository + PMH gateway) |
| Simple Dublin Core in RDF/XML | linked from the index |
| **DBLP XML** | linked from the index |
| RFC 1807 | linked from the index |
| Plain-text abstracts | `tr-abstracts.txt` |
| RSS, HTML table, PDF catalogue with abstracts | linked from the index |

That is more machine-readable surface than most national repositories offer. If you want a clean
corpus of 50 years of one department's output, this is the easiest one to take.

### 3.6 INRIA and HAL

French public research — INRIA, CNRS, CEA, LIRMM — deposits into **HAL**, which this directory
already documents in depth: [`hal.md`](hal.md) records **2,827,378 notices of which 1,788,688 have
files attached** [API], and §7 there covers the CRDT papers, CompCert, Coq and Frama-C.

The point for *this* record is that **HAL is a technical-report repository as much as a preprint
server.** INRIA's `RR-` research-report series and `RT-` technical-report series are deposited
there, and for a lot of INRIA work the research report is the long version with the proofs while
the conference paper is the abstract. If a French systems or formal-methods paper says "see the
extended version", the extended version is an INRIA RR in HAL.

Recall the HAL trap from [README §4](README.md#6-probing-traps): **the subject field is
`domainAllCode_s`, not `domain_s`** — the wrong field returns a silent `numFound: 0`.

---

## 4. Corporate research archives

The most valuable and the most fragile category. A corporate report series survives exactly as
long as somebody at the company keeps paying for a web server, and the *research value* of the
series has no bearing on that decision.

### 4.1 Bell Labs — the Bell System Technical Journal

The **BSTJ (1922–1983)** is arguably the most important single corpus in the history of
electronics: transistor physics, information theory, transmission-line and filter design, the
UNIX papers, switching systems, semiconductor process.

**Where it actually is, verified 2026-09-02** [API] (S19):

| Location | Measured |
|---|---|
| `archive.org` item `bstj-archives`, titled **"The Bell System Technical Journal (1922-1983)"** | metadata API 200; 6 files |
| `archive.org` collection query `collection:"bstj-archives"` | **4,425 items** |
| `archive.org` title search `title:("Bell System Technical Journal")` | 577 items |

```bash
curl -s 'https://archive.org/advancedsearch.php?q=collection%3A%22bstj-archives%22&rows=0&output=json'
# → "numFound": 4425
curl -s 'https://archive.org/metadata/bstj-archives'
```

**4,425 items on the Internet Archive is the durable copy.** Alcatel-Lucent hosted a free BSTJ
archive at `bell-labs.com` for some years after 2008; that route is **[NOT-VERIFIED]** here and
should not be relied on. **The Internet Archive collection is the answer to give.**

**Bell Labs Technical Journal** (the 1996–2020 successor, Lucent/Alcatel-Lucent/Nokia era) was
published through Wiley and then IEEE and is **not** free. Do not conflate the two titles — BSTJ is
free, BLTJ largely is not. **[NOT-VERIFIED]** for any free BLTJ route.

### 4.2 DEC / Compaq — SRC, WRL, CRL, PRL, NSL

This is the case study in corporate archive fragility, and it has a happy ending.

DEC's research labs — **SRC** (Systems Research Center, Palo Alto), **WRL** (Western Research
Lab), **CRL** (Cambridge Research Lab), **PRL** (Paris Research Lab) and **NSL** (Network Systems
Lab) — produced a report series that includes some of the most-cited work in distributed systems,
compilers and computer architecture. After Compaq acquired DEC and HP acquired Compaq, the
collection was hosted at `hpl.hp.com/techreports/Compaq-DEC/`.

**Status of the original host, probed 2026-09-02** [WEB] (S20):

- `www.hpl.hp.com` resolves (15.73.144.188) but **raw TCP to port 443 fails**; `curl` returned
  `http=000` for both `/techreports/Compaq-DEC/` and `/hpjournal/journal.html`.
- The Internet Archive's **last three captures** of `hpl.hp.com/techreports/Compaq-DEC/` are
  **2022-05-17 (302)**, **2022-05-17 (301)** and **2022-12-22 (301)** — i.e. **by 2022 the URL was
  already only a redirect**, not the collection. The directory was gone before the host was.

**Where the collection survives: bitsavers** [WEB] (S21).
`https://www.bitsavers.org/pdf/dec/tech_reports/` — HTTP 200, 68,014 B, an Apache directory index.
Measured file counts by prefix:

| Prefix | Files | Series |
|---|---|---|
| `SRC-RR-` | **170** | SRC Research Reports |
| `SRC-TN-` | **67** | SRC Technical Notes |
| `WRL-` | **108** | Western Research Lab reports |
| `WRL-TN-` | **42** | WRL Technical Notes |
| `CRL-` | **91** | Cambridge Research Lab |
| `PRL-RR-` | **35** | Paris Research Lab |
| `NSL-TN-` / `NSL-NN-` / `NSL-RR-` | 4 / 2 / 1 | Network Systems Lab |
| **`Compaq-DEC_TRs_HPL_mirror_2007.zip`** | 1 | **236,085,636 B (≈236 MB)** — a complete mirror of the HPL-hosted collection taken in **2007**, `Last-Modified: 2023-09-04` |

Negative control: `SRC-RR-99999.pdf` → **HTTP 404, 280 B** (S21). Clean.

**The lesson, and it generalises:** somebody mirrored a corporate research archive in 2007, and
that ZIP is now the reason the collection exists at all. The original host stopped serving it
between 2007 and 2022 and nobody at HP announced it. **When you find a corporate report series that
matters to you, take a copy.**

### 4.3 HP Journal

*Hewlett-Packard Journal* (1949–1998) is the primary source for a great deal of test-and-
measurement instrument design — the internals of HP counters, spectrum analysers, logic analysers
and calculators, written by the engineers who built them.

**Status: [NOT-VERIFIED] / at risk.** `https://www.hpl.hp.com/hpjournal/journal.html` returned
`http=000` (TCP failure) on 2026-09-02 (S20), from the same unreachable host as §4.2. Given that
the adjacent Compaq-DEC directory was already a redirect by 2022, **assume the HP Journal archive
at that URL is gone.** Third-party scans circulate (HP Memory Project, bitsavers' HP tree,
Internet Archive) but **no specific surviving canonical location was verified in this pass.**

### 4.4 IBM Journal of Research and Development

- `https://research.ibm.com/journal` → **302 → `https://research.ibm.com/publications?source=19971`,
  HTTP 200, 80,241 B** [WEB] (S22)

The *IBM Journal of Research and Development* (1957–) and the *IBM Systems Journal* are the primary
sources for System/360 architecture, DRAM and magnetic-recording physics, CMOS process
development, mainframe RAS engineering and a great deal of early database work.

**Access is mixed and this record will not pretend otherwise.** Recent IBM JRD volumes are
published through **IEEE Xplore** and are paywalled. IBM's own `research.ibm.com/publications`
front end is free for abstracts and hosts many full texts. IBM historically ran a public
"DomainoWeb"/`domino.research.ibm.com` report server; `dominoweb.draco.res.ibm.com` returned
`http=000` on the probe date (S22). **A comprehensive free route to the full JRD back file is
[NOT-VERIFIED].**

### 4.5 Xerox PARC

**The host is gone, and the redirect tells the story.** `https://www.parc.com/publications/`
**redirects to `https://www.sri.com/research/future-concepts-division/`** (HTTP 200, 137,588 B)
[WEB] (S23) — PARC having been acquired by SRI International. **The publications index no longer
exists at that address**; you land on a corporate division page.

PARC's foundational work — Ethernet, Smalltalk, the Alto, InterPress, laser printing,
bitmap displays, ubiquitous computing — was published as **Xerox PARC technical reports** with
`CSL-`, `SSL-` and `ISL-` prefixes. Those documents survive, but **scattered**: bitsavers' `xerox`
tree, the Computer History Museum, `worrydream.com`-style curated collections, individual authors'
pages and the Internet Archive. **No single authoritative index was located in this pass —
[NOT-VERIFIED].** This is the most serious unresolved gap in this record and a legitimate
`web.archive.org/save/` target list for future work.

### 4.6 Microsoft Research

- `https://www.microsoft.com/en-us/research/publications/` → **HTTP 200, 1,237,346 B** [WEB] (S24)

MSR maintains a large, live, free publications index — Dryad, Naiad, Orleans, F*, Z3, Project
Catapult (FPGA acceleration in Azure), Farview, silicon photonics, holographic and DNA storage.
Most entries link a free PDF. It is the healthiest corporate research archive probed here.

**Caveat:** the URL slugs are not stable. A deep link built from a paper title
(`.../publication/the-chubby-lock-service-for-loosely-coupled-distributed-systems/`) returned
**HTTP 404** (S24). **Search the index; do not construct URLs from titles.** And, as with all
corporate archives, if a document matters, keep a copy — Microsoft Academic's shutdown at the end
of 2021 (see [companion record §2.2](open-access-full-text-sources.md)) is a reminder that
Microsoft does retire research infrastructure.

---

## 5. Standards bodies — what is free and what is not

Precision matters here because the differences are large and people guess wrong in both directions.

| Body | Free? | Verified |
|---|---|---|
| **IETF / RFC Editor** | **Entirely free. Always has been.** | ✅ [WEB] |
| **RISC-V International** | **Free** — ratified specs published openly | ✅ [WEB] |
| **USB-IF** | **Free** — specifications downloadable from the Document Library | ✅ [WEB] |
| **JEDEC** | **Free of charge, but registration-walled** | ⚠️ partial |
| **IEEE SA** | **Mostly paid.** A subsidised subset is free via the GET Program | ⚠️ partial |

### IETF — the model everyone else should copy

- `https://www.rfc-editor.org/rfc-index.txt` → **HTTP 200, 2,024,501 bytes** — the complete index
  of every RFC ever published, as a single plain-text file (S25).
- `https://www.rfc-editor.org/rfc/rfc9000.txt` → **HTTP 200, 403,442 bytes** — RFC 9000 (QUIC),
  full text, no account, no cookie banner, no paywall (S25).

**Every RFC, from RFC 1 (1969) to today, is free, permanent and machine-readable**, in `.txt`,
`.html`, `.xml` and `.pdf`, plus Internet-Drafts and the working-group mailing-list archives. There
is no other standards body in this table of which that is true. When a protocol is specified in an
RFC, you have the complete authoritative source at zero cost — which is a large part of why the
Internet protocol stack has the implementation diversity it has.

### RISC-V International

- `https://riscv.org/technical/specifications/` → **301 →
  `https://riscv.org/specifications/ratified/`, HTTP 200, 212,511 B** [WEB] (S26)

**RISC-V specifications are free.** The site separates **Ratified Specs** from **Under
Development**, and the specification sources are additionally developed in public on GitHub.

**The historical handoff matters for citation.** The Berkeley technical reports in §3.1 are the
*original* documents (2011–2016). Stewardship moved to the RISC-V Foundation (2015), which became
**RISC-V International**. So:

- Citing the **origin** of RISC-V → `UCB/EECS-2011-62` (and `UCB/EECS-2016-1` for the design
  rationale).
- Citing the **current** ISA → the ratified specification from riscv.org, with its version and
  ratification date.
- Citing "the RISC-V spec" without saying which → ambiguous across a decade of revisions. Don't.

### USB-IF

- `https://www.usb.org/documents` → **HTTP 200, 144,183 B** [WEB] (S27)

A public **Document Library**, filterable by Category (Legal, Presentations, Specification, Tools,
White Paper) and Type (Cable and Connector Specification, etc.). Specifications are downloadable
without membership, under a prominent "AS IS", all-warranties-disclaimed legal notice. There is a
separate **Member Login** for member business, but the specs themselves are public. Note that
specific ZIP filenames are versioned and change — a guessed filename returned **404, 37,583 B**
(S27) — so navigate the library rather than constructing URLs.

### JEDEC

- `https://www.jedec.org/standards-documents` → **HTTP 200, 60,155 B**;
  `https://www.jedec.org/standards-documents/docs/jesd79-5c` → **HTTP 200, 48,268 B** [WEB] (S28)

JEDEC is where the memory standards live — **DDR SDRAM, HBM, LPDDR, UFS, e.MMC, JESD21-C module
configurations, JEP95 registered outlines, JEP30 part-model guidelines, ESD, lead-free
manufacturing, and the GaN/SiC wide-bandgap power semiconductor documents** (all confirmed as
navigation categories on the standards page).

**The access model: documents are free of charge but not anonymous.** Downloading requires a free
registered JEDEC account, which is why an unauthenticated scripted fetch of a document gets you the
landing page and not the PDF. Some items are genuinely commercial — the page also advertises
"Order JEDEC Standard Manufacturer's ID Code", a paid registration service. **The precise
free-account download mechanics were not exercised in this pass — [NOT-VERIFIED] beyond the
landing pages.** Do not describe JEDEC as "paywalled" (it mostly is not) or as "open" (it is not
that either); **registration-walled** is the accurate word.

### IEEE standards

- `https://standards.ieee.org/products-programs/ieee-get-program/` → **HTTP 200, 92,930 B**
  [WEB] (S29)

**IEEE standards are, by default, paid.** IEEE 802.3 (Ethernet), 802.11 (Wi-Fi), 1149.1 (JTAG),
1076 (VHDL), 1364 (Verilog), 1800 (SystemVerilog), 754 (floating point) are sold individually or
through subscription.

The **IEEE GET Program** is the exception. In IEEE SA's own words (S29):

> "The subsidized sponsorship of standards via the IEEE GET Program helps expand the global reach
> of technical knowledge developed by industry, accelerates adoption of IEEE standards, contributes
> to an open knowledge community…"

The mechanism is that **a sponsor pays so that a particular standard can be given away**. The 802
family has historically been the flagship of this (the "Get IEEE 802" programme). **Which specific
standards are currently free is [NOT-VERIFIED]** — the list is dynamic and the page did not yield a
machine-readable enumeration. **Check the GET Program page before assuming you must pay, and before
assuming you need not.**

*(For IEEE **papers**, as opposed to standards, see
[companion record §3.3](open-access-full-text-sources.md#33-ieee) and
[`techrxiv.md`](techrxiv.md).)*

---

## 6. Status table

All probes **2026-09-02**. "Chrome 131" = the rung-2 user agent from
[`AGENTS.md`](../../AGENTS.md); everything else was default `curl`.

| Source | Endpoint | Status | Size / count | Notes |
|---|---|---|---|---|
| **NASA NTRS** | `ntrs.nasa.gov/api/citations/search` | **200** | **646,950** records | 358,213 with document. Bogus id → 404 (40 B). **`q=` empty → 0** |
| **OSTI** | `osti.gov/api/v1/records` | **200** | via `x-total-count` | `links[rel=fulltext]` → `/servlets/purl/<id>`; verified 6,066,387 B PDF. **`q=` empty → 0** |
| DOE PAGES | `osti.gov/pages/` | 200 | 125,342 B | |
| **DTIC** | `discover.dtic.mil/` · `/results/?q=radiation` | **200** | 466,561 B · 386,731 B | Chrome 131. Public = Distribution Statement A only |
| **NIST** | `nvlpubs.nist.gov/.../NIST.SP.800-193.pdf` | **200** | 516,802 B, `%PDF-` | Bogus → **404**, 1,380 B. Clean host |
| NIST | `nist.gov/publications` · `csrc.nist.gov/publications/fips` | 200 | 116,978 B · 140,880 B | |
| NTIS / NTRL | `ntrl.ntis.gov/NTRL/` | 200 | 115,425 B | "free and open access". Count NOT-VERIFIED |
| **GAO** | `gao.gov/` · `/reports-testimonies` | **403** | **363 B · 386 B** | **Third distinct 403 fingerprint.** Blocked |
| CRS | `crsreports.congress.gov/` | 200 | 345,391 B | |
| **UC Berkeley EECS** | `www2.eecs.berkeley.edu` (128.32.139.28) | **000** | — | **Raw TCP timeout on :443 and :80.** All records via Wayback |
| Berkeley via Wayback | `web.archive.org/web/2020id_/…EECS-2011-62.html` etc. | 200 | 6.1–8.0 kB pages | 6 RISC-V reports verified with BibTeX |
| Berkeley PDFs via Wayback | `…EECS-2011-62.pdf` · `…EECS-2016-1.pdf` | 200 | 376,630 B · 959,927 B, `%PDF-1.4` | Further probes → 000 (IA rate limit) |
| **MIT DSpace** | `dspace.mit.edu/handle/1721.1/5460` | **200** | 460,148 B | "AI Memos (1959 – 2004)" |
| MIT CSAIL | `publications.csail.mit.edu/ai/` | 200 | 5,244 B | AI Lab historical series |
| **CMU SCS** | `reports-archive.adm.cs.cmu.edu/` | **200** | 2,820 B | Mach, Fox, PDL, SEI special collections |
| CMU KiltHub | `kilthub.cmu.edu/` | **202** | **0 B** | figshare zero-byte-202 trap, confirmed on a 2nd tenant |
| **Stanford** | `i.stanford.edu/TR/` | **200** | 1,332 B | Decade indexes 1960s–1990s + CSL series |
| Stanford | `i.stanford.edu/TR/CS-TR-listing.html` *(control)* | 404 | 197 B | |
| **Cambridge CL** | `cl.cam.ac.uk/techreports/` | **200** | 10,247 B | ISSN 1476-2986; since 1974; highest TR seen **1009** |
| Cambridge PDF | `UCAM-CL-TR-630.pdf` | **200** | **11,754,717 B**, `%PDF-` | Skorobogatov; DOI `10.48456/tr-630` |
| Cambridge control | `UCAM-CL-TR-99999.pdf` · `UCAM-CL-TR-630/` | 404 | 279 B | Trailing slash also 404s |
| **BSTJ** | `archive.org` `collection:"bstj-archives"` | **200** | **4,425 items** | Item titled "The Bell System Technical Journal (1922-1983)" |
| **DEC/Compaq (original)** | `hpl.hp.com/techreports/Compaq-DEC/` | **000** | — | Wayback's last 3 captures (2022) are 301/302 — gone before the host died |
| **DEC/Compaq (survivor)** | `bitsavers.org/pdf/dec/tech_reports/` | **200** | 68,014 B index | 170 SRC-RR · 67 SRC-TN · 108 WRL · 42 WRL-TN · 91 CRL · 35 PRL-RR |
| bitsavers mirror zip | `Compaq-DEC_TRs_HPL_mirror_2007.zip` | 200 | **236,085,636 B** | Mirror taken 2007 |
| bitsavers control | `SRC-RR-99999.pdf` | 404 | 280 B | Clean |
| **HP Journal** | `hpl.hp.com/hpjournal/journal.html` | **000** | — | **Assume gone.** No canonical survivor verified |
| IBM JRD | `research.ibm.com/journal` | 200 (after 302) | 80,241 B | Recent volumes on IEEE Xplore, paywalled |
| IBM (legacy) | `dominoweb.draco.res.ibm.com/` | **000** | — | |
| **Xerox PARC** | `parc.com/publications/` | 200 | 137,588 B | **Redirects to `sri.com/research/future-concepts-division/`** — index gone |
| Microsoft Research | `microsoft.com/en-us/research/publications/` | 200 | 1,237,346 B | Title-derived deep link → 404; slugs unstable |
| **IETF** | `rfc-editor.org/rfc-index.txt` · `/rfc/rfc9000.txt` | **200** | 2,024,501 B · 403,442 B | Entirely free |
| **RISC-V Intl** | `riscv.org/specifications/ratified/` | **200** | 212,511 B | Free; 301 from `/technical/specifications/` |
| **USB-IF** | `usb.org/documents` | **200** | 144,183 B | Free; guessed ZIP filename → 404 |
| **JEDEC** | `jedec.org/standards-documents` · `/docs/jesd79-5c` | **200** | 60,155 B · 48,268 B | Free but **registration-walled**; mechanics NOT-VERIFIED |
| **IEEE SA GET** | `standards.ieee.org/products-programs/ieee-get-program/` | **200** | 92,930 B | Which standards are free: **NOT-VERIFIED** |

### Explicitly not verified

Listed so the gaps are visible rather than silent.

1. **UC Berkeley EECS was never reached directly.** TCP timed out from this environment. All six
   RISC-V records come from Internet Archive replays of the department's own pages. The *content*
   is first-hand from Berkeley's generator; the *transport* was not.
2. **No Berkeley report numbers beyond the six RISC-V documents were confirmed.** Candidate probes
   for Rocket Chip / Chisel / BOOM reports returned `http=000` from Wayback rate-limiting, which is
   not evidence of absence.
3. **NTIS/NTRL holdings count** — no machine-readable total obtained.
4. **GAO** — 403 on both paths tried; nothing about GAO's holdings was verified first-hand.
5. **HP Journal** — no surviving canonical location verified.
6. **Xerox PARC report series** — no authoritative index located anywhere. The most serious gap.
7. **IBM JRD** — no comprehensive free route to the back file verified.
8. **Bell Labs Technical Journal** (1996–2020, as distinct from BSTJ) — no free route verified.
9. **JEDEC download mechanics** — the free-registration flow was not exercised.
10. **IEEE GET Program contents** — no machine-readable list of currently-free standards.
11. **DTIC's public/restricted split was not quantified.** The distinction is documented from
    policy, not measured.

### Retrieval notes for the crawler access table

Staged for [`retrieval-notes.md`](retrieval-notes.md) and thence
[`ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md):

- **Federal report APIs are open and need no user-agent fallback.** `ntrs.nasa.gov`,
  `www.osti.gov` and `eutils.ncbi.nlm.nih.gov` all answered default `curl`. `discover.dtic.mil`,
  `nist.gov` and `nvlpubs.nist.gov` answered the Chrome-131 UA.
- **New shared trap: `q=` with an empty value returns zero, not everything**, on *both* NTRS and
  OSTI. Two independent agencies, same failure. Omit the parameter or use `q=*`.
- **OSTI puts its result total in the `x-total-count` response header, not the body.** A body-only
  parser sees no count at all.
- **New 403 fingerprint: `www.gao.gov` returns a ~363–386-byte 403.** Distinct from the ~5.6 kB
  Cloudflare challenge and the ~651 kB SHERPA 403 recorded in the
  [companion record §7](open-access-full-text-sources.md#7-probe-status-table).
- **`http=000` (TCP timeout) is a genuinely different signal from 403/404** and appeared for
  `www2.eecs.berkeley.edu`, `www.hpl.hp.com` and `dominoweb.draco.res.ibm.com`. Record it as
  *unreachable*, never as *defunct*, unless corroborated — the same discipline this survey applied
  to `synthical.com` in [`retrieval-notes.md`](retrieval-notes.md).
- **figshare's HTTP-202-with-zero-bytes behaviour is reproducible on institutional tenants**
  (`kilthub.cmu.edu`), not just `figshare.com`.
- **Internet Archive rate-limiting is the binding constraint on grey-literature verification.**
  Roughly a dozen Wayback replay fetches in quick succession degraded to `http=000`, while the
  **CDX API stayed responsive throughout** — corroborating the existing note in
  [`retrieval-notes.md`](retrieval-notes.md). **Use CDX for existence, replay sparingly.**

### Archival candidates (`AGENTS.md` rule 9)

Not submitted in this pass; recommended. All are scarce, unmirrored, and hold the only map of a
significant collection:

- `http://i.stanford.edu/TR/` and its seven decade indexes — a 1,332-byte unmaintained page that is
  the only index of 40 years of Stanford CS/CSL reports.
- `https://www.bitsavers.org/pdf/dec/tech_reports/` — the only surviving index of the DEC
  SRC/WRL/CRL/PRL/NSL collection now that the HPL host is gone.
- `http://reports-archive.adm.cs.cmu.edu/` — the CMU SCS index, including the Mach and PDL special
  collections.
- Any Xerox PARC report index that a future pass manages to locate (§4.5).

---

## 7. Sources

Retrieved **2026-09-02** unless stated. Raw probe output is under
[`../../scratch/preprint-repositories/oa-fulltext/`](../../scratch/preprint-repositories/oa-fulltext/).

- **S1** `https://ntrs.nasa.gov/api/citations/search?size=0` and `…?q=radiation%20hardened&size=1` —
  totals, `disseminated`/`distribution`/`stiType`/`center`/`subjectCategory`/`author`/`keyword`/
  `organization`/`reportNumber` aggregations. Supports §2.1 tables. [API]
- **S2** `https://ntrs.nasa.gov/api/citations/search?q=&size=1` → `total: 0` vs `?size=1` and
  `?q=*&size=1` → 646,950; `https://ntrs.nasa.gov/api/citations/99999999999` → 404, 40 B. Supports
  the NTRS traps and negative control. [API]
- **S3** `https://ntrs.nasa.gov/api/citations/search?q=SpaceCube|FPGA+single+event+upset&size=1`
  and `https://ntrs.nasa.gov/api/citations/20150022446` (record + `downloads[]`). [API]
- **S4** `https://www.osti.gov/api/v1/records?rows=1&q=…` for `power+electronics`, `semiconductor`,
  `battery`, `detector`, `riscv`, an empty `q`, a nonsense term, and
  `/api/v1/records/999999999999`; totals read from the `x-total-count` header. [API]
- **S5** `https://www.osti.gov/servlets/purl/2584705` → 200, 6,066,387 B, `%PDF-`. Supports the
  full-text route. [API/WEB]
- **S6** `https://discover.dtic.mil/` (200, 466,561 B) and `/results/?q=radiation` (200,
  386,731 B), Chrome 131. [WEB]
- **S7** `https://www.nist.gov/publications` (200, 116,978 B);
  `https://csrc.nist.gov/publications/fips` (200, 140,880 B);
  `https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-193.pdf` (200, 516,802 B,
  `%PDF-`); `…NIST.SP.800-99999.pdf` (404, 1,380 B). [WEB]
- **S8** `https://ntrl.ntis.gov/NTRL/` (200, 115,425 B) — the "largest collection… free and open
  access" statement quoted in §2.5. [DOC]
- **S9** `https://www.gao.gov/` → 403, 363 B; `https://www.gao.gov/reports-testimonies` → 403,
  386 B; Chrome 131. [WEB]
- **S10** `https://crsreports.congress.gov/` → 200, 345,391 B. [WEB]
- **S11** `getent hosts www2.eecs.berkeley.edu` → 128.32.139.28; raw TCP to :443 and :80 both time
  out; `curl` `http=000` at 25 s with default and Chrome-131 UAs, HTTP/2 and HTTP/1.1. [WEB]
- **S12** Internet Archive replays `http://web.archive.org/web/2020id_/http://www.eecs.berkeley.edu/
  Pubs/TechRpts/{2011/EECS-2011-62, 2011/EECS-2011-63, 2014/EECS-2014-54, 2016/EECS-2016-1,
  2016/EECS-2016-118, 2016/EECS-2016-161}.html` — titles, author lists, dates, canonical PDF URLs,
  BibTeX and EndNote blocks read directly from the department's generated pages. PDFs for
  `EECS-2011-62` (376,630 B) and `EECS-2016-1` (959,927 B), both `%PDF-1.4`. Supports the §3.1
  table. [WEB]
- **S13** `https://dspace.mit.edu/handle/1721.1/5460` → "AI Memos (1959 - 2004)", 200, 460,148 B;
  `/handle/1721.1/6453` → 200, 558,625 B; `https://publications.csail.mit.edu/ai/` → 200, quoted in
  §3.2. [WEB]
- **S14** `http://reports-archive.adm.cs.cmu.edu/` → 200, 2,820 B; sub-collection list quoted
  verbatim. [WEB]
- **S15** `https://kilthub.cmu.edu/` → HTTP 202, 0 bytes. [WEB]
- **S16** `http://i.stanford.edu/TR/` → 200, 1,332 B; full contents transcribed in §3.4. [WEB]
- **S17** `https://www.cl.cam.ac.uk/techreports/` → 200, 10,247 B — ISSN, 1974 start date, the
  "all published since 2002 are available online in PDF" statement, and the seven catalogue
  formats. [DOC]
- **S18** `https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-630.pdf` (200, 11,754,717 B, `%PDF-`);
  `…-630.html` (200, 8,215 B) giving title, author, April 2005, 144 pages and DOI
  `10.48456/tr-630`; `…-99999.pdf` and `…-630/` both 404 (279 B). [WEB]
- **S19** `https://archive.org/advancedsearch.php?q=collection:"bstj-archives"&rows=0&output=json`
  → `numFound: 4425`; `https://archive.org/metadata/bstj-archives` → item title "The Bell System
  Technical Journal (1922-1983)"; `title:("Bell System Technical Journal")` → 577. [API]
- **S20** `https://www.hpl.hp.com/techreports/Compaq-DEC/` and `/hpjournal/journal.html` →
  `http=000`; `http://web.archive.org/cdx/search/cdx?url=hpl.hp.com/techreports/Compaq-DEC/` → last
  three captures 2022-05-17 (302), 2022-05-17 (301), 2022-12-22 (301). [WEB/API]
- **S21** `https://www.bitsavers.org/pdf/dec/tech_reports/` → 200, 68,014 B; prefix counts by
  `grep`; `HEAD Compaq-DEC_TRs_HPL_mirror_2007.zip` → 236,085,636 B, Last-Modified 2023-09-04;
  `SRC-RR-99999.pdf` → 404, 280 B. [WEB]
- **S22** `https://research.ibm.com/journal` → 302 → `?source=19971`, 200, 80,241 B;
  `https://dominoweb.draco.res.ibm.com/` → `http=000`. [WEB]
- **S23** `https://www.parc.com/publications/` → 200, 137,588 B, final URL
  `https://www.sri.com/research/future-concepts-division/`. [WEB]
- **S24** `https://www.microsoft.com/en-us/research/publications/` → 200, 1,237,346 B; a
  title-derived publication slug → 404, 168,984 B. [WEB]
- **S25** `https://www.rfc-editor.org/rfc-index.txt` → 200, 2,024,501 B;
  `https://www.rfc-editor.org/rfc/rfc9000.txt` → 200, 403,442 B;
  `https://www.rfc-editor.org/about/` → 200, 83,352 B. [WEB]
- **S26** `https://riscv.org/technical/specifications/` → 301 → `/specifications/ratified/`, 200,
  212,511 B. [WEB]
- **S27** `https://www.usb.org/documents` → 200, 144,183 B, Document Library and legal disclaimer;
  a guessed spec ZIP filename → 404, 37,583 B. [WEB]
- **S28** `https://www.jedec.org/standards-documents` → 200, 60,155 B (technology focus areas
  quoted); `https://www.jedec.org/standards-documents/docs/jesd79-5c` → 200, 48,268 B. [WEB]
- **S29** `https://standards.ieee.org/products-programs/ieee-get-program/` → 200, 92,930 B; the
  "subsidized sponsorship of standards" statement quoted in §5. [DOC]
- **S30** [`arxiv.md` §7.5](arxiv.md) — the prior finding that the foundational RISC-V documents are
  Berkeley technical reports and RISC-V International specifications, not arXiv preprints, marked
  [NOT-VERIFIED] there. This record supplies the identifiers. [internal]
