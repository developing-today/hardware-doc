# RePEc and EconStor — economics working-paper infrastructure record

A **combined record**, because the two interlock: RePEc is a metadata federation that owns
no documents, and EconStor is one of the full-text repositories whose documents RePEc
indexes. Reading either alone produces a wrong mental model.

- **RePEc URL:** http://repec.org/ (the initiative) · https://ideas.repec.org/ (largest
  front end) · https://econpapers.repec.org/ (second front end)
- **RePEc operator:** a **volunteer federation**, not an institution. "RePEc is a
  crowd-sourced effort: a) thousands of people and organizations contribute the underlying
  data, b) a core team of contributors manage the system, and c) sponsor organizations
  provide the infrastructure. As such, the RePEc initiative has no central expenses" (S1)
  [DOC].
- **RePEc launched:** **1997-05-12**, at a meeting in Guildford, UK (S6) [DOC].
- **EconStor URL:** https://www.econstor.eu/ · OAI-PMH
  https://www.econstor.eu/oai/request
- **EconStor operator:** **ZBW – Leibniz Information Centre for Economics**, Kiel/Hamburg,
  Germany. DSpace-based (S9) [API].
- **EconStor launched:** **2009** — earliest OAI datestamp **2009-01-28T14:13:20Z** (S9)
  [API], corroborating Wikipedia's 2009 (S11).
- **Status:** both active.
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

> **Relevance warning, stated up front.** A hardware or software engineer will almost never
> need either of these. EconStor's entire *Data processing / Computer science* holding is
> **36 records** out of 320,533 (§5.2) [API]. They are in this collection because Wikipedia
> lists them as preprint repositories, because RePEc is the best working example of an
> architecture (federated metadata, no central store) that the rest of scholarly publishing
> never adopted, and because the *econ.\** / `cs.GT` overlap with arXiv is real if narrow
> (§6).

---

## 1. What RePEc is — and the key finding

**RePEc is not a repository.** It stores no papers. It is a **decentralised metadata
federation** with a shared file format and a shared naming convention, on top of which
several independent websites are built.

The mechanism, in the initiative's own words: "Every publisher or provider puts text files
describing their publications on their own server. These files follow a simple but rigorous
machine-readable syntax. They are then automatically mirrored and made available to the
public on the various RePEc websites. … **RePEc is thus a facilitator that organizes the
data for others to use.**" (S1) [DOC]

So when a central bank, a university department or a commercial publisher "joins RePEc", it
does not upload anything. It puts a directory of plain-text metadata files on its own web or
FTP server, structured according to the **Guildford Protocol**, with fields defined by
**ReDIF** (Research Documents Information Format). RePEc's scripts walk the archives
nightly. The PDF stays wherever the publisher put it.

This has three consequences that matter:

1. **No single point of failure for content, but no guarantee of it either.** If a
   department reorganises its website, its RePEc links rot and RePEc cannot fix them —
   it never had the file.
2. **"RePEc has N papers" is a federation-wide count of *metadata records*, not of
   documents held.** See §3.
3. **RePEc long predates and structurally out-performs OAI-PMH for its purpose.** ReDIF
   dates from 1997; it is a domain-specific format with entity types RePEc actually needs
   (working paper, article, book, chapter, **software component**, person, institution)
   rather than generic Dublin Core.

### 1.1 The architecture — who does what

| Component | Role | Where it runs |
|---|---|---|
| **RePEc** (`repec.org`) | the initiative, protocols, the data itself | Kit Baum (Boston College) is "proprietor of the repec.org domain" (S5) [DOC] |
| **ReDIF / Guildford Protocol** | the metadata format and the archive-discovery convention | specs at `ideas.repec.org/p/rpc/rdfdoc/` (S1) |
| **IDEAS** (`ideas.repec.org`) | the largest front end; browse, search, rankings, author profiles | run by **Christian Zimmermann** (S2, S5) |
| **EconPapers** (`econpapers.repec.org`) | the second front end, same data, different UI | hosted by the **School of Business at Örebro University**, Sweden; run by Sune Karlsson (S3, S5) [WEB] |
| **NEP** (`nep.repec.org`) | *New Economics Papers* — human-edited email/RSS current-awareness reports by field | Thomas Krichel maintains the software; Marco Novarese directs it (S5) |
| **RAS / RePEc Author Service** (`authors.repec.org`) | author registration and profile linking | Krichel/Zimmermann (S5) |
| **EDIRC** (`edirc.repec.org`) | directory of economics institutions | Zimmermann; started 1996-03-07 with 350 entries (S6) |
| **CitEc** (`citec.repec.org`) | citation extraction and analysis | José Manuel Barrueco Cruz, University of Valencia (S5) |
| **LogEc** (`logec.repec.org`) | download/access statistics | Sune Karlsson (S5) |
| **MPRA** (`mpra.ub.uni-muenchen.de`) | Munich Personal RePEc Archive — the deposit-of-last-resort for authors whose institution has no archive | University of Munich library (S1, S5) |
| **CollEc**, **RePEc Genealogy**, **RePEc Biblio**, **EconAcademics**, **SocioRePEc** | co-authorship centrality, academic family tree, curated bibliography, blog aggregator, PDF annotation | various (S1) |
| **RePEc Plagiarism Committee** (`plagiarism.repec.org`) | publishes adjudicated plagiarism cases | volunteer committee (S7) |

### 1.2 The Federal Reserve Bank of St. Louis relationship — precisely stated

Wikipedia's list names the **Federal Reserve Bank of St. Louis** as RePEc's operator (S11).
**That is a half-truth and worth correcting.** What is verifiable: IDEAS is run by
**Christian Zimmermann**, who "is Assistant Vice President at the Federal Reserve Bank of St.
Louis" and "is in charge of the IDEAS, EDIRC, RePEc Genealogy and RePEc Biblio sites" (S5)
[DOC]. The Fed therefore hosts and effectively underwrites **IDEAS**, the largest RePEc front
end. It does not operate RePEc. RePEc "has no central expenses" and no central operator at
all (S1) [DOC]; EconPapers runs at Örebro; MPRA at Munich; the metadata sits on 2,400+
publishers' own servers.

The RePEc origin story is worth one line because it is genuine internet history: **Thomas
Krichel**, then a Lecturer in Economics at the University of Surrey, "set up NetEc" on
**gopher** in **February 1993** — a consortium including WoPEc (online papers), BibEc,
CodEc (software), WebEc, BizEc, HoPEc and JokEc. NetEc moved to the web in 1994. RePEc
proper was founded at the Guildford meeting on **1997-05-12**; the LSE Financial Markets
Group was the first archive to join, on 1997-05-27; IDEAS launched in September 1997 with
**40,000 items** (S6) [DOC].

## 2. What EconStor is

**EconStor is an actual repository** — ZBW's DSpace instance, holding full text. It exists
because German economics research institutes, and later a wide international set, needed a
place to put working papers with a persistent handle. Every EconStor record carries a
handle in the `10419/…` namespace (sample identifier `oai:econstor.eu:10419/1234`, S9)
[API].

EconStor is also **a RePEc archive**: it appears on RePEc's own list of "Additional websites
using RePEc" (S1) [DOC], and its holdings surface through IDEAS and EconPapers. This is
exactly the relationship the combined record exists to make visible: **EconStor holds the
PDFs; RePEc indexes the metadata; IDEAS displays it.** Three layers, three operators, one
document.

## 3. Size — RePEc

### 3.1 EconPapers' live counter (the best single source)

`https://econpapers.repec.org/`, retrieved 2026-09-01; the page footer reads "Page updated
2026-09-02" (S3) [WEB]:

| Item type | Count | of which downloadable | in |
|---|---|---|---|
| Working Papers | **1,316,031** | 1,111,325 | 5,915 series |
| Journal Articles | **3,759,295** | 3,681,849 | 4,681 journals |
| Software Items | **6,039** | 6,025 | 37 series |
| Books | **69,352** | 33,618 | 680 series |
| Chapters | **338,841** | 104,243 | 365 series |
| **Total searchable** | **5,489,558** | **4,937,060 available online** | |

Plus "74,118 Authors and 14,568 individuals have registered in the RePEc Author Service".

### 3.2 IDEAS' own holdings page (same federation, independently counted)

`https://ideas.repec.org/stats.html`, retrieved 2026-09-01 (S2) [WEB]:

| | Journals & series | Items | of which online | JEL coded | with abstracts | with references | with citations |
|---|---|---|---|---|---|---|---|
| Working papers | 5,906 | **1,325,878** | 1,121,021 | 572,853 | 1,115,887 | 640,349 | 643,859 |
| Articles | 4,658 | 3,770,404 | 3,692,447 | 580,423 | 3,085,554 | 1,572,075 | 1,721,335 |
| Software components | 37 | 6,039 | 6,025 | 964 | 5,927 | 0 | 336 |
| Books | 657 | 70,609 | 34,438 | 11,950 | 39,507 | 6,697 | 26,110 |
| Chapters | 360 | 332,227 | 97,814 | 30,433 | 308,419 | 14,915 | 46,741 |
| **Total** | **11,618** | **5,505,157** | **4,951,745** | 1,196,623 | 4,555,294 | 2,234,036 | 2,438,381 |

Also: **15,803 economics institutions** in EDIRC, **73,978 registered authors** (who have
authored 2,351,877 indexed items), and **101,367 NEP reports in 106 fields**.

**IDEAS and EconPapers disagree slightly** — 5,505,157 vs 5,489,558 total; 1,325,878 vs
1,316,031 working papers. Both were retrieved on 2026-09-01. The gap (~0.3%) is mirror lag:
the two services harvest the same publisher archives on their own schedules. **Recorded, not
resolved.** It is a useful reminder that in a federation there is no canonical count, only
snapshots taken by different harvesters.

RePEc's own front page rounds it: "Over 2,400 archives from 106 countries have contributed
over 5.5 million research items from 4,600 journals and 5,900 working paper series. Over
74,000 authors have registered in the RePEc Author Service and 75,000 email subscriptions
are served every week." (S1) [DOC]

### 3.3 Reconciling Wikipedia's ">1,000,000"

Wikipedia gives RePEc ">1,000,000" (S11). **The number is defensible only if you read it as
working papers specifically**, which is 1,316,031 (S3) or 1,325,878 (S2). As a total it is
off by a factor of five: the federation indexes **5.49–5.51 million items**.

More importantly, the figure is the wrong *kind* of number. Of that 5.5 million, **3.77
million are journal articles** — not preprints, not working papers, and mostly not open.
Only **1,111,325 working papers are downloadable** (S3). Listing RePEc in a table of
"preprint repositories" alongside arXiv invites the reader to compare 5.5 M against arXiv's
holdings, which is meaningless: RePEc is an *index*, and most of what it indexes is the
published literature. The comparable number is the downloadable-working-paper count, and
even that lives on 2,400 other people's servers.

## 4. Size — EconStor

All figures from EconStor's OAI-PMH interface, `completeListSize` in the `resumptionToken`,
retrieved **2026-09-01** (S9) [API]:

| Set | Records |
|---|---|
| **All records** (`ListIdentifiers`, `oai_dc`) | **320,533** |
| `doc-type:workingPaper` | **166,147** |
| `doc-type:article` | 103,777 |
| `doc-type:report` | 28,252 |
| `doc-type:conferenceObject` | 12,976 |
| `doc-type:book` | 3,707 |
| `doc-type:doctoralThesis` | 675 |
| `doc-type:preprint` | **661** |
| `ddc:330` (Economics) | 275,034 |
| `ddc:000` (Generalities, Science) | 864 |
| `ddc:600` (Technology / Applied sciences) | **43** |
| `ddc:004` (Data processing / Computer science) | **36** |

**320,533 against Wikipedia's ">100,000" (S11)** — the bucket is right but three times too
coarse. Note that **"working paper" (166,147) and "preprint" (661) are different doc-types
in EconStor's own taxonomy**: in economics the working paper *is* the preprint, and the
`preprint` set is a rounding error. Wikipedia's description — "A subject based repository
with a high share of working papers (preprints)" (S11) — is accurate, and the parenthesis
is doing exactly the right work.

EconStor's OAI interface declares **100 sets** in total (S9) [API], mixing Dewey classes
(`ddc:*`) with document types (`doc-type:*`).

## 5. Screening, moderation and reliability

### 5.1 There is no moderation, and that is not a defect

Neither RePEc nor EconStor peer-reviews anything, and **in economics this is the norm rather
than a compromise.** The working paper — an NBER paper, a Fed staff report, a CEPR
discussion paper, a university department's WP series — is a first-class, citable object
that circulates for years, sometimes forever, without a journal version. It carries the
institution's imprimatur, not a reviewer's. A reader who expects arXiv-style moderation, or
who treats "unreviewed" as "unvetted", has the wrong model of the field.

**What actually gates content:**

- **RePEc:** the *archive* gates, not RePEc. Anyone can create a RePEc archive, but in
  practice archives are run by institutions — departments, central banks, publishers — that
  have their own series editors. RePEc checks metadata syntax, not content. **Any
  reliability signal you get from RePEc comes from the series, not from RePEc.**
- **MPRA** is the deliberate exception: the Munich Personal RePEc Archive exists precisely
  so authors "in institutions lacking a participating RePEc archive can submit their papers"
  (S1) [DOC]. It has no institutional filter. **An MPRA-only paper carries no series
  warrant; treat MPRA the way you would treat a generalist preprint server.**
- **EconStor:** ZBW curates which series it hosts; the depositing institution vouches for
  the content.

### 5.2 The one genuine integrity mechanism — the Plagiarism Committee

RePEc runs a **standing plagiarism committee** with a public register of adjudicated cases
(S7) [DOC]. Its stated rationale is unusually blunt:

> "Plagiarism is a serious offense of scientific ethics, yet detected plagiarism too often
> results in consequences that have little bite. Indeed, an offender may be punished by
> his/her current employer, and then move on to another job without further consequences.
> Sometimes, even the employer may not even care and in some rare cases sponsor plagiarism.
> The goal of this page is to highlight cases of plagiarism in Economics. All cases have been
> evaluated by a committee. Each case provides a full description, so that the reader can
> judge by him/herself whether plagiarism occurred. The response of the accused plagiariser
> is also published." (S7)

A named, public offender list with right of reply, run by volunteers, is a stronger
integrity mechanism than most preprint servers in this collection have. It is worth knowing
about even if you never read an economics paper. (I did not enumerate the case list; **the
number of listed offenders is [NOT-VERIFIED]**.)

### 5.3 How to sanity-check an item

1. **Identify the series, not the repository.** `RePEc:nbr:nberwo:…` (NBER Working Papers)
   and `RePEc:pra:mprapa:…` (MPRA) are not the same kind of object. The RePEc handle encodes
   the archive.
2. **Check whether it was ever published.** IDEAS and EconPapers both link working papers to
   their published versions where CitEc or the author has established the link. RePEc's own
   documentation lists "tracking how working papers get published" as a standard use of its
   data (S1) [DOC].
3. **Check the author's RAS profile.** 73,978 authors are registered (S2); an unregistered
   author with a single MPRA deposit is a different proposition from a registered one with a
   department series.
4. **Search the plagiarism register** (S7).
5. **For EconStor, check `dc:rights`.** Licences vary per record (§7).

## 6. Relevance to computing and electronics — limited but non-zero

Be honest: **this is thin, and the numbers are unforgiving.**

- EconStor's whole *Data processing / Computer science* class is **36 records**; *Technology
  (Applied sciences)* is **43** (S9) [API]. To make the point concretely, those 36 records
  include *"Die geschichtliche Entwicklung des V-Modells"* (the historical development of
  the V-Model), *"Learning to play Sokoban from videos"*, *"ChatGPT — A critical view"*,
  *"Machine learning in demand planning: Cross-industry overview"* and *"The BabelNEG System
  — A Protocol-generic Infrastructure for Electronic SLA Negotiations in the Internet of
  Services"* (S9) [API]. Genuinely computing, genuinely obscure, and thirty-six of them.
- RePEc's **6,039 software components in 37 series** (S2, S3) are almost entirely **Stata,
  MATLAB, Gauss and R code for econometrics** — the largest such archive is maintained by
  Kit Baum, who "proposed the inclusion of software components in RePEc" and "often
  contributes Stata components for time series econometrics" (S5) [DOC]. This is a real,
  early, and under-appreciated piece of research-software infrastructure: **RePEc has been
  indexing citable research software since 1997-09-08** (S6) [DOC], twenty years before
  Zenodo's GitHub integration made it fashionable. It has 0 items with references and only
  336 with citations (S2) — the citation graph never reached the software.

**Where the overlap with your world is real:**

The interesting economics for a systems person is classified by **JEL code**, and IDEAS lets
you browse by it at `https://ideas.repec.org/j/<CODE>.html`. The relevant codes, all
confirmed live 2026-09-01 (S8) [WEB]:

| JEL code | Title | Why you might care |
|---|---|---|
| **L86** | Information and Internet Services; **Computer Software** | economics of software, platforms, open source |
| **L63** | **Microelectronics; Computers; Communications Equipment** | semiconductor industry economics, Moore's-law productivity studies |
| **D82** | Asymmetric and Private Information; **Mechanism Design** | auction and market design — the direct overlap with `cs.GT` |
| **C63** | **Computational Techniques** | numerical methods, simulation |
| **C45** | **Neural Networks and Related Topics** | ML in econometrics |
| **C81** | Methodology for Collecting, Estimating, and Organizing Microeconomic Data | data infrastructure |
| **O33** | Technological Change: Choices and Consequences; Diffusion Processes | technology adoption |

**Per-code item counts: [NOT-VERIFIED].** The IDEAS JEL browse pages paginate at 200 items
and expose no total; I did not enumerate them.

**The arXiv overlap.** arXiv's `econ.EM` (econometrics), `econ.TH` (theoretical economics)
and `econ.GN` (general economics) exist since 2017 and overlap RePEc's `C` and `D` codes
directly; `cs.GT` (computer science and game theory) overlaps `D82` almost exactly, with
mechanism-design and auction papers routinely appearing in both literatures. **If a
mechanism-design or market-design result matters to you, it is more likely to be on arXiv
`cs.GT` than reachable through RePEc**, and RePEc will index the *published* version
afterwards. See [arxiv.md](arxiv.md).

**Blunt summary: a hardware or software engineer will essentially never need RePEc or
EconStor.** The exceptions are narrow and identifiable: you are reading about auction/market
design and want the economics-side literature; you are chasing semiconductor-industry or
open-source economics (L63, L86); or you want econometric software with a citable handle.
Everything else in these systems is somebody else's field.

## 7. Access, APIs and bulk retrieval

### 7.1 RePEc — the standard method, and the discouraged one

RePEc's own guidance is explicit and worth quoting because it is the opposite of what most
repositories say (S4, *"RePEc: getting the metadata"*) [DOC]:

> "**We want to discourage you strongly to scrape the data from the websites.** This puts
> unnecessary strain on our servers, and we have repeatedly noticed misconfigured scraping
> scripts running amok. And you [are] very unlikely to get complete data that way."

**The sanctioned route** is to harvest the publisher archives directly: "Each publisher holds
its RePEc metadata on its web or anonymous ftp server. The addresses are listed in their
archive templates. All those templates are listed at the **RePEc:all** archive. This is the
standard way to acquire the core RePEc data." Tooling: **`remi`** to acquire, **`ReDIF-perl`**
to parse (S4) [DOC].

**A consolidated copy** is also offered, with a caveat — "One can also access all the data in
one place. There is, however, no guarantee that this is accurate or up-to-date. Only the
publisher archives can guarantee that" — in these formats (S4) [DOC]:

- **ReDIF** (native)
- **AMF** (Academic Metadata Format)
- **OAI-PMH** — described by RePEc itself as "**sometimes flaky**"
- **rsync**

**Person data** is available through the `RePEc:per` archive. "Email addresses are released
under no circumstances." (S4) [DOC]

**The API is application-gated, not open** (S10) [DOC]: "the API is currently not openly
available, as we have yet to understand the demand for it and how much it could be taxing our
servers." To get access you must email Christian Zimmermann with your identity, purpose,
required data, why the standard method is not usable, source IP, project end date, and
expected call frequency. Approved users get a time-limited access code; "We reserve the right
to throttle the API if needed." Metadata is JSON. **There is no search function in the API.**
Example functions: `getref`, `getrecentpapers`, `getpubsfromwpseries`, `getauthorshortid`.
CitEc has its own separate API.

**Reachability probes, 2026-09-01** (S8) [WEB] — all with a browser User-Agent; no UA
fallback was needed for any RePEc host:

| URL | Result |
|---|---|
| `http://repec.org/` | 200, 14,991 B |
| `https://ideas.repec.org/` | 200, 29,872 B |
| `https://econpapers.repec.org/` | 200, 6,790 B |
| `http://nep.repec.org/` | 200 → `https://nep.repec.org/`, 284,295 B |
| `https://authors.repec.org/` | 200, 5,247 B |
| `http://logec.repec.org/` | 200 → https, 6,337 B |
| `https://edirc.repec.org/` | 200, 13,672 B |
| `https://ideas.repec.org/stats.html` | 200, 19,453 B |
| **Negative control** `https://ideas.repec.org/j/notarealcode999.html` | **404**, 17,657 B |
| **Negative control** `http://repec.org/aboutrepec.html` (invented) | **404**, 408 B |
| `http://repec.org/docs/` (directory listing) | **403** — indexing disabled, as expected |

Both negative controls return genuine 404s. **RePEc's front ends 404 honestly**, unlike
[OSF](osf-preprints.md) (200 + SPA shell) and [SSRN](ssrn.md) (200 + "Page Cannot be Found").
That is worth stating: it makes RePEc scriptable in a way the others are not — which sits
oddly beside its request that you not script it.

### 7.2 EconStor — open OAI-PMH behind a closed web front end

This is the most interesting access finding in the record.

**The web front end is behind a proof-of-work anti-scraper gate.** `https://www.econstor.eu/`
returns HTTP 200 with a 4,807-byte challenge page titled **"Making sure you're not a bot!"**,
served by **[Anubis](https://github.com/TecharoHQ/anubis)**. The page states EconStor's
reasoning verbatim (S9) [WEB]:

> "You are seeing this because EconStor has set up Anubis to protect the server against the
> scourge of AI companies aggressively scraping websites. This can and does cause downtime
> for the websites, which makes their resources inaccessible for everyone. Anubis is a
> compromise. Anubis uses a Proof-of-Work scheme in the vein of Hashcash … at individual
> scales the additional load is ignorable, but at mass scraper levels it adds up and makes
> scraping much more expensive. … This is required because **AI companies have changed the
> social contract around how website hosting works.**"

Running Anubis version `v1.25.0-38-g0134fc2-dirty`, hosted by ZBW. `https://www.econstor.eu/`
and `https://www.econstor.eu/server/…` both hit it. **A browser User-Agent does not get past
it** — it is a JavaScript proof-of-work challenge, not UA filtering, so the
[AGENTS.md](../../AGENTS.md) user-agent ladder is the wrong tool and rotating agents will
waste your time.

**And yet the OAI-PMH endpoint is completely open.** `https://www.econstor.eu/oai/request`
answered every verb immediately, with no challenge, no UA requirement and no rate limiting,
across ~15 sequential calls (S9) [API]:

```
verb=Identify        → repositoryName EconStor · baseURL https://www.econstor.eu/oai/request
                       protocolVersion 2.0 · adminEmail w.riese@zbw.eu
                       earliestDatestamp 2009-01-28T14:13:20Z · deletedRecord transient
                       granularity YYYY-MM-DDThh:mm:ssZ
                       repositoryIdentifier econstor.eu · sample oai:econstor.eu:10419/1234
verb=ListSets        → 100 sets (ddc:* and doc-type:*)
verb=ListIdentifiers → completeListSize in the resumptionToken (§4)
verb=ListRecords     → oai_dc records with dc:rights
```

**That combination is the finding.** ZBW's position is coherent and worth understanding: the
*metadata* is deliberately, unconditionally open through the standard protocol (and is CC0,
§8); the *website* is defended because bulk HTML scraping is expensive and unnecessary when a
harvesting protocol exists. **If you want EconStor data, use OAI-PMH. That is what it is
for, and using it is the polite path, not a workaround.**

**Negative control** (S9) [API]: `verb=ListIdentifiers&set=notarealset:xyzzy` returns
**HTTP 200** with `<error code="noRecordsMatch">`. A 200 from an OAI endpoint means nothing;
you must parse for `<error>`. Note also that small sets (`ddc:004` at 36 records, `ddc:600`
at 43) return **no `resumptionToken` and therefore no `completeListSize`** — you must count
`<identifier>` elements yourself. A missing `completeListSize` is not an error and not a
zero.

## 8. Licensing and reuse

**RePEc metadata — effectively public domain, with a non-commercial expectation.** The
official policy, dated 12 October 2017 (S12) [DOC]:

> "The RePEc metadata have been contributed by individual RePEc archives for the benefit of
> the research community. **You are free to do whatever you want with metadata from RePEc
> archives** provided that you do not contravene any copyright or license in any of the
> participating archives. You are encouraged to attribute RePEc as the source of the
> metadata."

RePEc's own front page likewise states "The RePEc bibliographic data is in the public
domain" (S1) [DOC]. **But** the data-acquisition page adds a condition the licence page does
not: "the archives participating in RePEc as well as the people volunteering with RePEc do so
with the understanding that the collected data will be put to good use. **This does not
include commercial use.** If you want to use RePEc data for commercial use, please first
contact RePEc. Typically, we would require substantial contributions of data to RePEc for a
commercial use to have a chance of being tolerated." (S4) [DOC] Two RePEc documents, two
different positions. **Recorded, not resolved** — if your use is commercial, ask.

**Full text on RePEc: whatever the publisher says.** RePEc has no licence to grant; the PDF
is on the publisher's server under the publisher's terms. Of 1,325,878 working papers,
1,121,021 are online at all (S2).

**EconStor metadata: CC0 1.0.** The OAI `Identify` response carries an explicit
`<dc:rights>` description: "Creative Commons License CC0 1.0
(https://creativecommons.org/publicdomain/zero/1.0/)" (S9) [API]. Unambiguous, machine-
readable, and about as good as repository metadata licensing gets.

**EconStor full text: mixed, declared per record.** `dc:rights` values observed in a single
`ListRecords` page (S9) [API]: `https://creativecommons.org/licenses/by/4.0/`,
`.../by/4.0/de/legalcode`, `.../by-sa/4.0/`, `http://creativecommons.org/licenses/by-nc-nd/3.0/de/`,
and — crucially — `https://www.econstor.eu/dspace/Nutzungsbedingungen`, EconStor's own
non-CC terms of use. **Check `dc:rights` on the individual record before reusing a PDF.** A
CC0 metadata licence does not make the documents CC0.

## 9. Caveats and controversies

1. **RePEc is not a repository and does not host papers.** This is the headline. Every
   "size" statement about RePEc is a statement about metadata records pointing at other
   people's servers.
2. **Wikipedia's ">1,000,000"** is right only for working papers and wrong for the
   federation, which indexes 5.49–5.51 M items — of which 3.77 M are journal articles, not
   preprints (§3.3).
3. **Wikipedia's "Federal Reserve Bank of St. Louis"** as operator is a half-truth: the Fed
   employs the person who runs IDEAS. RePEc has no operator (§1.2).
4. **IDEAS and EconPapers give different totals on the same day** (§3.2). In a federation
   there is no canonical count.
5. **Link rot is structural.** RePEc points at publishers' own servers. A departmental
   reorganisation breaks links RePEc cannot repair. 204,857 working papers are indexed but
   **not** online (1,325,878 minus 1,121,021, S2) [INF].
6. **MPRA is the soft underbelly.** It is the one RePEc archive with no institutional filter
   (§5.1). Papers that exist only in MPRA deserve the scepticism you would apply to a
   generalist preprint server.
7. **RePEc asks you not to scrape it** and gates its API behind a written application (§7.1)
   — unusual among the repositories in this collection, and a direct consequence of having
   no central budget.
8. **EconStor's website is behind Anubis proof-of-work** and its OAI-PMH is wide open (§7.2).
   Anyone probing EconStor with HTTP tooling will conclude it is down. It is not.
9. **RePEc's own OAI-PMH is self-described as "sometimes flaky"** (S4). Prefer ReDIF or
   rsync for RePEc; prefer OAI-PMH for EconStor.
10. **`doc-type:preprint` on EconStor returns 661 records** and is a red herring; the working
    papers (166,147) are the preprints (§4).

## 10. Sources

- **S1** — RePEc home, `http://repec.org/`. Retrieved 2026-09-01, HTTP 200, 14,991 bytes.
  Supports: the "crowd-sourced effort / no central expenses" description, the operating
  model ("Every publisher or provider puts text files describing their publications on their
  own server"), the full RePEc service list, the "Over 2,400 archives from 106 countries …
  over 5.5 million research items" summary, the "bibliographic data is in the public domain"
  statement, the list of additional services using RePEc (including EconStor), and the
  Guildford Protocol / ReDIF references.
- **S2** — IDEAS holdings statistics, `https://ideas.repec.org/stats.html`, and the IDEAS
  home page `https://ideas.repec.org/`. Retrieved 2026-09-01, HTTP 200. Supports: the §3.2
  holdings table (5,505,157 items, 11,618 serials, 4,951,745 online, JEL/abstract/reference/
  citation coverage), 15,803 institutions, 73,978 registered authors, 101,367 NEP reports in
  106 fields, and IDEAS' "over 5,400,000 items … over 2,000 participating archives" blurb.
- **S3** — EconPapers home, `https://econpapers.repec.org/`. Retrieved 2026-09-01, HTTP 200,
  6,790 bytes; page footer "Page updated 2026-09-02". Supports: the §3.1 breakdown
  (1,316,031 working papers in 5,915 series; 3,759,295 articles; 6,039 software items;
  69,352 books; 338,841 chapters; 5,489,558 total) and EconPapers' hosting by the School of
  Business at Örebro University.
- **S4** — *"RePEc: getting the metadata"*, `https://ideas.repec.org/getdata.html`.
  Retrieved 2026-09-01, HTTP 200, 23,050 bytes. Supports: the anti-scraping request, the
  `RePEc:all` archive and `remi`/`ReDIF-perl` tooling, the ReDIF/AMF/OAI-PMH/rsync bulk
  formats, the "OAI/PMH (sometimes flaky)" characterisation, the `RePEc:per` person archive,
  the email-address policy, and the non-commercial-use condition.
- **S5** — *"The RePEc team"*, `https://ideas.repec.org/team.html`. Retrieved 2026-09-01,
  HTTP 200, 26,356 bytes. Supports: Christian Zimmermann as Assistant Vice President at the
  Federal Reserve Bank of St. Louis and head of IDEAS/EDIRC/Genealogy/Biblio; Kit Baum as
  proprietor of repec.org and originator of RePEc software components; Sune Karlsson running
  EconPapers, LogEc and SWoPEc; Thomas Krichel as founder and maintainer of NEP and the
  Author Service; José Manuel Barrueco Cruz and CitEc; MPRA at the University of Munich.
- **S6** — *"RePEc history"*, `https://ideas.repec.org/history.html`. Retrieved 2026-09-01,
  HTTP 200, 25,671 bytes. Supports: NetEc on gopher, February 1993, by Thomas Krichel at the
  University of Surrey; NetEc's move to the web in 1994; the Guildford meeting of
  1997-05-12 and the named participants; LSE FMG as first archive (1997-05-27); IDEAS launch
  September 1997 with 40,000 items; software components added 1997-09-08; NEP's first
  mailing 1998-05-04; EDIRC's start 1996-03-07 with 350 entries.
- **S7** — RePEc plagiarism page, `https://plagiarism.repec.org/`. Retrieved 2026-09-01,
  HTTP 200, 2,503 bytes. Supports: the existence, rationale and procedure of the RePEc
  Plagiarism Committee and its public offenders register with right of reply.
- **S8** — Reachability and negative-control probes across RePEc hosts, plus IDEAS JEL browse
  pages `https://ideas.repec.org/j/{L86,L63,D82,C63,C45,C81,O33}.html`. All 2026-09-01.
  Supports §6's JEL code titles and §7.1's probe table including the two 404 negative
  controls.
- **S9** — EconStor. OAI-PMH at `https://www.econstor.eu/oai/request` with verbs `Identify`,
  `ListSets`, `ListIdentifiers` (whole repository and per set), `ListRecords`; plus the web
  front page `https://www.econstor.eu/` and `https://www.econstor.eu/server/oai/request`.
  All retrieved 2026-09-01/02 (the endpoint's own `responseDate` was `2026-09-02T04:56:28Z`,
  UTC). Supports: §4's entire size table, the 2009-01-28 earliest datestamp, the 100 sets,
  the `10419/…` handle namespace, the CC0 metadata licence, the per-record `dc:rights`
  variety, the sample `ddc:004` titles, the `noRecordsMatch` negative control, and the Anubis
  proof-of-work block page with its verbatim justification.
- **S10** — *"RePEc API"*, `https://ideas.repec.org/api.html`. Retrieved 2026-09-01, HTTP
  200, 21,999 bytes. Supports: the API's application-gated status, the information required
  of applicants, the JSON delivery, the absence of a search function, the named example
  functions, and the throttling reservation.
- **S11** — Wikipedia, *List of preprint repositories*, wikitext via
  `https://en.wikipedia.org/w/index.php?title=List_of_preprint_repositories&action=raw`.
  Retrieved 2026-09-01. Supports: the RePEc row (Economics, ">1,000,000", 1997, Federal
  Reserve Bank of St. Louis) and the EconStor row ("Economics and Business Studies", "A
  subject based repository with a high share of working papers (preprints)", ">100,000",
  2009, ZBW).
- **S12** — *"Use of RePEc data"*, `http://repec.org/docs/RePEcDataUse.html`, dated
  12 October 2017. Retrieved 2026-09-01, HTTP 200, 1,067 bytes. Supports: the metadata reuse
  policy in full.
