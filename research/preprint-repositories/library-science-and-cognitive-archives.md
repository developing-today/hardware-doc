# CogPrints, E-LIS and LISSA — library-science and cognitive-archive record

A grouped record for three small subject repositories: **CogPrints** (cognitive science,
1997–2017), **E-LIS** (library and information science, 2003–) and **LISSA** (LIS, 2017–).

- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

---

## 0. Why these three are worth a record

None of them is important by size. Together they are **the best case study available in
what happens to a subject repository when its founder retires, its grant ends, or its
volunteers move on** — which is the question you should ask before trusting any link into
any small preprint server, including the ones that look healthy today.

Three outcomes, three mechanisms, all verifiable in 2026:

| | Mechanism | Outcome 2026 |
|---|---|---|
| **CogPrints** | founder/host wound it down; university took custody | **Frozen but preserved.** Content survives as an explicitly "permanently archived" static copy at a different hostname. The original HTTPS URL is **broken**, and the failure looks like the site is dead |
| **E-LIS** | distributed volunteer editorial board, institutional host, no single founder | **Alive and depositing.** 27,455 records, 882 with 2026 datestamps |
| **LISSA** | community announced a migration and never executed it | **Stranded.** Announced departure from COS "at the end of December 2020"; six years later it is still on COS, its own website has not been updated since 2020, and COS has closed it to submissions |

The generalisable lesson is in the middle column, not the right one. **A repository's
survival tracks whether its labour is distributed, not whether its content is valuable.**
CogPrints had the most famous founder in open access and died with his retirement from it;
E-LIS has no famous anybody and 22 languages' worth of volunteer editors and is still
running. And LISSA shows the third and most dangerous outcome: a live-looking website
describing a plan that was abandoned.

**Practical consequence for citation.** Two of these three currently present a URL that
either fails outright (CogPrints over HTTPS) or misrepresents its own status (LISSA's
`lissarchive.org`). If you have a citation into a small subject repository, **check it now,
not when you need it**, and archive the PDF.

---

# 1. CogPrints

- **URL (historical):** `http://cogprints.org/` — **now 301-redirects** to
  `https://web-archive.southampton.ac.uk/cogprints.org/`
- **URL (HTTPS):** `https://cogprints.org/` — **fails with a TLS certificate error**, see §1.2
- **Operator:** **University of Southampton**, School of Electronics and Computer Science.
  Founded and moderated by **Stevan Harnad** (S6) [LIT].
- **Discipline scope:** "Psychology, Neuroscience, and Linguistics, and many areas of
  Computer Science (e.g., artificial intelligence, robotics, vision, learning, speech,
  neural networks), Philosophy (e.g., mind, language, knowledge, science, logic), Biology
  … Medicine … Anthropology … as well as any other portions of the physical, social and
  mathematical sciences that are pertinent to the study of cognition." (S1, the site's own
  front page) [DOC]
- **Span:** **1997–2017** per Wikipedia's list (S7); Wikipedia's CogPrints article says
  "launched in 1997" (S6).
- **Status:** **frozen, preserved, and misleadingly unreachable.** The site itself says:
  "**This site has been permanently archived. This is a static copy provided by the
  University of Southampton.**" (S1) [DOC]
- **Size:** "As of 2025, it contains **over 4,000** freely downloadable articles" (S6)
  [LIT]. Wikipedia's list gives ">1,000" (S7). **A live count is [NOT-VERIFIED]** — see
  §1.3 for why I could not obtain one.

## 1.1 What it was

CogPrints was the cognitive-science answer to arXiv, and it was built by the person who
spent the following two decades arguing that everyone should have one. It carried
**Computer Science as a first-class subject alongside psychology, neuroscience, linguistics
and philosophy** — its subject browse had a `comp` branch, and the front page named
"artificial intelligence, robotics, vision, learning, speech, neural networks" explicitly
(S1) [DOC]. For a while in the early 2000s it was the canonical example, next to arXiv, of
what author self-archiving looked like.

Wikipedia's assessment of why it stopped mattering is worth quoting because it is a
structural argument rather than a story about one person: "Over time, under the influence of
the Open Archives Initiative and its OAI-PMH, the focus of self-archiving has shifted from
centralized repositories like CogPrints to distributed self-archiving in institutional
repositories." (S6) [LIT] CogPrints did not fail; the model it embodied was superseded by
one in which every university runs its own repository and a harvester federates them —
which is, incidentally, the same model [RePEc](repec-and-econstor.md) adopted in 1997 and
never abandoned.

## 1.2 The software-history detail — CogPrints *became* EPrints

This is the part worth stating properly, and it is better than "EPrints came out of
Southampton".

CogPrints ran on **EPrints**, and the page footer says so: "Cogprints is powered by EPrints
3 which is developed by the School of Electronics and Computer Science at the University of
Southampton." (S1) [DOC] But the direction of causation is the interesting bit: **CogPrints'
own software was generalised into EPrints.** Per Wikipedia: "CogPrints was among the first
repositories to adopt OAI compliance. **Its software was later converted into EPrints at the
University of Southampton by Rob Tansley, who later contributed to the development of
DSpace.** EPrints is currently maintained by Christopher Gutteridge at Southampton." (S6)
[LIT]

So the lineage runs: one cognitive-science preprint archive → EPrints, the first widely
deployed open-source institutional-repository platform → and, through the same developer,
into **DSpace**, which is what [EconStor](repec-and-econstor.md) runs on today. **E-LIS
(§2) still runs EPrints 3.4.6** (S3) [WEB]. A single 1997 subject archive is the common
ancestor of two of the three repository platforms in this record. That is a genuine piece of
software history and it is barely documented anywhere.

CogPrints also advertised **SWORD** deposit (`/sword-app/servicedocument`) and **OAI 2.0**
with base URL `http://cogprints.org/cgi/oai2` (S1) [DOC] — early adoption of both, entirely
consistent with Harnad's advocacy.

## 1.3 Its fate — probed, and the failure mode is a trap

**The reported symptom.** A probe of `https://cogprints.org/` on 2026-09-01 fails. This
record's assignment noted a connection failure with no HTTP status. **Independently
reproduced and diagnosed here.**

**What is actually happening** (all probes 2026-09-01, S2) [WEB]:

| Probe | Result |
|---|---|
| `https://cogprints.org/` | **curl exit 60** — `SSL: no alternative certificate subject name matches target hostname 'cogprints.org'`. No HTTP status is ever returned |
| — certificate served | `subject: CN=web-archive.southampton.ac.uk`, `issuer: C=US, O=Let's Encrypt, CN=YR1`, `subjectAltName does not match hostname cogprints.org` |
| `http://cogprints.org/` | **HTTP 200**, 7,419 bytes, after redirect to `https://web-archive.southampton.ac.uk/cogprints.org/` |

**Diagnosis:** the `cogprints.org` DNS record now points at Southampton's web-archive host,
but **no certificate was issued for the `cogprints.org` name**. Southampton preserved the
content and forgot the certificate. The result is that:

- **Plain HTTP works and returns the archive.**
- **HTTPS fails at the TLS layer, before any HTTP status exists** — which is exactly what a
  dead server looks like to a naive probe, and to a browser that upgrades to HTTPS.
- Anyone with an `https://cogprints.org/...` citation — which is what modern link-rewriting
  produces — gets a security error, not a redirect.

**This is a preservation success presenting as a preservation failure**, and it is worth
generalising: **a TLS error is not evidence that content is gone.** Always retry over plain
HTTP and follow the redirect before concluding a small repository is dead.

**Corroboration from the Internet Archive CDX index** (S5) [API], which is not rate-limited
the way the Wayback replay service is:

- `cogprints.org` has captures from **2004-12-09** to **2026-08-31**.
- The **last capture with HTTP status 200** at the root is **2024-08-03**.
- The **first 301** appears **2020-05-10**; from late 2024 onward captures are **301 only**
  (e.g. 2024-12-16, 2025-01-05 … 2026-08-31), consistent with the permanent redirect to the
  Southampton archive host being in place and stable.

**Live counts are [NOT-VERIFIED], and here is why.** The Southampton archive host is itself
behind **Anubis / BotStopper**, a JavaScript proof-of-work anti-scraper gate. The front page
came through (HTTP 200), but every sub-page tested returned **HTTP 401 with a 4,397-byte
challenge page** headed "Ensuring the security of your connection … the administrator of
this website has set up Anubis to protect the server against the scourge of AI companies
aggressively scraping websites" (S2) [WEB]:

| Path | Result |
|---|---|
| `/cogprints.org/` (index) | 200, 7,419 B |
| `/cogprints.org/information.html` | **401**, 4,397 B (Anubis) |
| `/cogprints.org/view/subjects.html` | **401** |
| `/cogprints.org/view/subjects/comp.html` | **401** |
| `/cogprints.org/cgi/oai2?verb=Identify` | **401** |
| **Negative control** `/cogprints.org/definitely-not-real-xyzzy.html` | **401** — *identical to a real page* |

Note the negative control: on this host **a 401 tells you nothing about whether the
document exists.** The user-agent ladder in [AGENTS.md](../../AGENTS.md) is the wrong
tool here — Anubis is a JavaScript proof-of-work challenge, not UA filtering, and rotating
agents will not help. The Internet Archive's replay service (`web.archive.org/web/...`) was
returning **HTTP 429** ("suspected abusive bot traffic") throughout this session, so the
archived 2017 subject-browse pages could not be read either. **The subject-level breakdown,
including how many CogPrints items were Computer Science, is therefore not verified.**

The OAI-PMH endpoint at `http://cogprints.org/cgi/oai2` is advertised on the front page but
sits behind the same gate; whether it still answers is **[NOT-VERIFIED]**.

## 1.4 What a computing person would find

Historical AI, robotics, vision, machine learning, speech and neural-network work from the
late 1990s and 2000s, filed under the `comp` subject branch, alongside the
philosophy-of-mind and cognitive-science literature it was in conversation with (S1) [DOC].
The archive is frozen at 2017, so nothing after that. Its practical value today is
**historical**: it is a snapshot of what the AI/cognitive-science boundary looked like
before deep learning, deposited by people who were arguing about symbol grounding.

**No landmark-papers table.** I could not enumerate the holdings (§1.3), and listing papers
I could not confirm are actually there would violate this collection's evidence rules.

---

# 2. E-LIS — E-prints in Library and Information Science

- **URL:** https://eprints.rclis.org/ · OAI-PMH https://eprints.rclis.org/cgi/oai2
- **Operator:** **E-LIS Governance** and **CIEPI**; *hosted* by the **Library System (CAB)
  of the University of Naples Federico II** (S3) [DOC]. Run by "a team of volunteer editors
  that support 22 languages" (S3) [DOC], with a named Administrative Board, Executive Board
  and per-country Editorial Board. Pro-bono legal support from D&P Studio Legale, Milan
  (S3) [DOC].
- **Discipline scope:** "Library and Information Science (LIS), including Communication"
  (S3). Classified with the **JITA Classification Scheme**, maintained by Christophe Dupriez
  (S3) [DOC].
- **Launched:** **2003** — "Established in 2003, e-LIS is an international digital
  repository" (S3) [DOC]; Wikipedia's article says January 2003 (S8); Wikipedia's list says
  2003 (S7). All agree.
- **Status:** **active** — 882 records carry 2026 datestamps (§2.2).
- **Software:** **EPrints 3.4.6** (S3) [WEB] — a current release, which is itself a
  reassuring maintenance signal.

## 2.1 What it is

E-LIS is the librarians' own repository, and it is the healthiest of the three archives in
this record for a reason that is visible in its governance page rather than its statistics:
**the labour is spread across dozens of named volunteer editors in dozens of countries**,
with an institutional host that supplies servers and a legal firm that supplies advice for
free. Nobody's retirement can end it.

Its self-description is unusually reflective about *why* librarians in particular built one:
"Because librarians are so involved in open access advocacy, e-LIS is a key to encourage
open access for all repositories, by giving librarians the experience they need to speak
with confidence when talking with researchers … and the experience to provide the best
possible assistance to self-archiving faculty." (S3) [DOC] The repository is partly a
training exercise in running a repository. That is a good reason for it to exist and a good
reason for it to be well run.

## 2.2 Size — measured

All from the OAI-PMH interface, `completeListSize` in the `resumptionToken`, retrieved
**2026-09-01** (S4) [API]:

- **Total records: 27,455.**
- `Identify`: `repositoryName` E-LIS repository · `protocolVersion` 2.0 ·
  `deletedRecord` **persistent** (deletions are tracked, not silently dropped — good) ·
  `granularity` `YYYY-MM-DDThh:mm:ssZ` · `sampleIdentifier` `oai:eprints.rclis.org:14248`.
- **`earliestDatestamp`: 2013-02-13T10:59:30Z.** **Note the conflict:** E-LIS launched in
  2003, but its OAI datestamps begin in 2013. That is a **platform migration artefact**, not
  a content boundary — a bulk re-index resets every record's modification date. **Do not
  read an OAI `earliestDatestamp` as a founding date.** This is a general trap and E-LIS is
  a clean example of it.
- **406 OAI sets**, mixing publication status (`Status = Published`, `Unpublished`,
  `Submitted`, `In Press`) with the full JITA subject hierarchy.

**Activity, by records with a datestamp in each window** (S4) [API] — note these count
*modifications*, so they overstate new deposits, but they do establish the repository is
being worked on:

| Window | Records |
|---|---|
| 2026-01-01 → 2026-09-01 | **882** |
| 2025 | 736 |
| 2024 | 571 |
| 2023 | 955 |

**27,455 against Wikipedia's ">10,000"** (S7) — the bucket is right but low. Wikipedia's
E-LIS *article* says "Over 12,000 papers have been archived to date", sourced to a 2011
retrieval (S8) [LIT] — a stale figure that has more than doubled since.

## 2.3 Screening — a real editorial board with a real queue

E-LIS is moderated, and its policy is specific (S9, *e-LIS Policies*) [DOC]:

> "Submitted documents will be placed into the **submission buffer**, where they may be
> approved by the e-LIS Editorial Board, rejected, or returned to the author for
> modifications in the metadata or if there are problems with the electronic file. Documents
> in the submission buffer are **manually reviewed** to confirm they fit our policy before
> adding them to e-LIS. e-LIS Editorial Board checks the metadata quality of the document
> and is allowed to make changes if the metadata are incorrect. **Two business days** is the
> allowable time period between when a paper is deposited to e-LIS and when it becomes
> accessible."

Scope: "any scientific or technical document, published or unpublished, in Librarianship,
Information Science and Technology, and related application activities. The criteria for
acceptance is that the eprints are relevant to research in LIS fields and that they have the
form of a finished document that is ready to be entered into a process of communication."
Accepted types include preprints, postprints, conference papers and posters, presentations,
books, chapters, technical reports and working papers, theses, and newspaper/magazine
articles (S9) [DOC].

Multilingual by design: "All languages are supported … If the document is in a language
other than English, it must include an English abstract and keywords in English." (S9) [DOC]

**Copyright is the author's problem, explicitly:** "Authors submitting documents are
responsible for confirming there aren't any restrictions on the electronic distribution of
the submitted document. Copyright issues will be the authors' responsibility. e-LIS is not
responsible for contents submitted by the authors." The deposit agreement grants E-LIS "the
right to store them and make them permanently available publicly for free on-line" (S9)
[DOC]. There is a **Preservation Policy** and a **Bibliographic Data Policy** on the same
page.

Metadata quality is checked and corrected by editors — a stronger commitment than most
preprint servers make, and consistent with the population depositing being professional
cataloguers.

## 2.4 What a computing person would find — and it is more than you would guess

E-LIS's JITA scheme has a **whole computing class, `L. Information technology and library
technology`, with 21 subclasses**. Counts by OAI set, 2026-09-01 (S4) [API]:

| JITA code | Subject | Records |
|---|---|---|
| **L.** | **Information technology and library technology (whole class)** | **4,998** |
| LC | Internet, including WWW | 1,154 |
| LJ | Software | 500 |
| LS | **Search engines** | 465 |
| LZ | None of these, but in this section | 404 |
| LQ | Library automation systems | 395 |
| LR | OPAC systems | 260 |
| LB | **Computer networking** | 258 |
| LN | **Data base management systems** | 212 |
| LK | **Software methodologies and engineering** | 191 |
| LM | **Automatic text retrieval** | 167 |
| LA | Telecommunications | 156 |
| LL | Automated language processing | 155 |
| LP | Intelligent agents | 130 |
| LH | **Computer and network security** | 92 |
| LD | Computers | 90 |
| LT | Mobile devices | 64 |
| LI | Authentication, and access control | 47 |
| LF | Digital cameras | 18 |
| LO | Object-oriented DBMS | 13 |
| LE | Scanners | 12 |
| LG | Photocopiers | 9 |

**4,998 records — 18.2% of the whole repository — are classified as information
technology** [INF, from S4]. That is a far higher computing share than
[EconStor](repec-and-econstor.md) (36 records, 0.011%) or the social-science end of
[OSF Preprints](osf-preprints.md).

The genuinely useful areas for this knowledge base, in order:

1. **Information retrieval** — `LM. Automatic text retrieval` (167) and `LS. Search engines`
   (465). The LIS literature on retrieval is the older sibling of the CS IR literature and
   frequently addresses evaluation methodology that CS papers assume.
2. **Repository software** — `LQ. Library automation systems` (395) and `LR. OPAC systems`
   (260). If you need to know how DSpace, EPrints, Koha or Fedora behave in production,
   this is where the operators write it up. Note the recursion: **E-LIS is an EPrints
   instance containing papers about running EPrints instances.**
3. **Metadata standards** — spread across the `I. Information treatment` class. Dublin Core,
   MARC, OAI-PMH, RDA. If you are implementing a harvester, this is the primary literature.
4. **Bibliometrics** — the LIS side of citation analysis, which is the field that produces
   the studies other records in this collection cite as [LIT].
5. `LK. Software methodologies and engineering` (191) and `LH. Computer and network
   security` (92) — small, and mostly library-systems-flavoured.

The subject vocabulary is dated in an endearing way — `LG. Photocopiers` (9 records),
`LE. Scanners` (12), `LF. Digital cameras` (18) — which is itself a reminder that the
scheme was designed in the early 2000s.

## 2.5 Access

**OAI-PMH is open, standard and unrestricted.** `https://eprints.rclis.org/cgi/oai2`
answered `Identify`, `ListSets`, and `ListIdentifiers` (whole repository and per set) with no
authentication, no UA requirement and no rate limiting across ~30 sequential calls
(S4) [API]. EPrints also exposes `RDFXML` and `RDFN3` full-repository exports
(`/cgi/export/repository/RDFXML/devel.rdf`), a **SWORD** deposit endpoint, OpenSearch, and
RSS/Atom feeds (S3) [WEB]. This is what a well-behaved repository looks like, and it is a
sharp contrast with [SSRN](ssrn.md), which offers none of it.

**Negative control** (S4) [API]: `verb=ListIdentifiers&metadataPrefix=oai_dc&set=notarealsetxyzzy`
returns **HTTP 500 Internal Server Error**, 539 bytes — *not* an OAI `<error>` element. That
is a bug rather than protocol-conformant behaviour, but it is at least unmistakably
distinguishable from a valid response. Contrast [EconStor](repec-and-econstor.md), which
returns HTTP 200 with `<error code="noRecordsMatch">` for the same mistake.

**Licensing.** Per-record; the deposit agreement grants E-LIS a permanent right to
distribute, and copyright remains the author's responsibility (§2.3). There is no single
repository-wide licence. Check each record.

---

# 3. LISSA — LIS Scholarship Archive

- **URLs:** community site https://lissarchive.org/ · content
  https://osf.io/preprints/lissa
- **Operator:** the **LISSA Steering Committee** (community); infrastructure by the
  **Center for Open Science**. Site source on GitLab at `gitlab.com/VickySteeves/lissarchive`
  (S10) [WEB].
- **Discipline scope:** "A free, open scholarly platform for library and information
  science" (S11) [API].
- **Launched:** **soft launch 2017-07-19**, full launch announced 2017-10-26 (S10) [DOC].
  Earliest record 2017-07-12 (S11) [API]. Wikipedia's list says 2018 (S7) — **off by a
  year**.
- **Status:** **stranded.** Closed to new submissions by COS; announced migration never
  happened; community site frozen since 2020.
- **Size:** **335 records**, of which **325 distinct works** (10 are later versions) and
  **321 carry a minted preprint DOI**, by full enumeration of the OSF API, 2026-09-01 (S11)
  [API]. Wikipedia says ">100" (S7).
- **Moderation:** `reviews_workflow: post-moderation` (S11) [API] — one of only three
  OSF providers that is not pre-moderated.
- **Record span:** first 2017-07-12, most recent **2025-12-04** (S11) [API].

## 3.1 What it was meant to be

LISSA's ambition was broader than "preprints", and deliberately so. From its own About page:
"Librarians, archivists, and other information professionals engage in a broad range of
scholarship, from creating metadata to writing manuscripts. We acknowledge that much of this
scholarship happens outside the traditional realms of academia, including work that goes
beyond the standard article or book chapter to **oral histories, community works, code,
data, and more**." (S10) [DOC]

Its submission guidelines accept "Articles · Reports · **Metadata** · Oral histories ·
Manuscripts · Pre-/post-prints · **Data** · **Code** · Promotion packets · Student work ·
Posters · Book Chapters" (S10) [DOC] — an unusually inclusive list that treats a metadata
record or a promotion packet as a legitimate scholarly output.

It also had a **code of conduct as an acceptance criterion**, which is rare: "We reserve the
right to remove any content that could reasonably be construed as offensive or harassing to
people or groups … Submissions will be reviewed periodically to check for conformation with
these guidelines. Submissions that do not meet these guidelines will be removed, and the
authors notified. If you wish to appeal any decisions … notify the LISSA board." (S10)
[DOC] The guidelines credit "the paleorxiv submission guidelines, the SocArXiv FAQ, and …
the open code of conduct" as sources — a small piece of evidence for how norms propagated
across the OSF provider population.

## 3.2 What actually happened — the stranding, verified

**2020-11-30.** The LISSA Steering Committee published *"LISSA is migrating off COS
infrastructure"* (S10) [DOC]:

> "The Library & Information Science Scholarly Archive (LISSA) will **transition away from
> being hosted by the Center for Open Science (COS) at the end of December 2020**. Materials
> currently hosted by the COS on https://osf.io/preprints/lissa will remain accessible.
> Please read our statement regarding why this decision is necessary, as well as the
> timeline of events that led to this decision."

The post lists three options put to the community — self-host; bring in a technical partner;
bring in a partner handling both technical and legal infrastructure — with a **survey
closing 2020-12-20**.

**2026-09-01 — none of it happened.** Measured:

- LISSA's content is **still on OSF**: 335 records under provider slug `lissa`, with deposits
  continuing to **2025-12-04** (S11) [API].
- **`lissarchive.org` is still live** and still displays the November 2020 migration notice
  as its most recent update. Its "Updates" page contains four posts, the newest dated
  **2020-11-30** and the rest from 2017 (S10) [WEB]. The footer reads "Original contents
  licensed 2020". The site links to `osf.io/preprints/lissa/submit` as though submission
  were open.
- **COS has closed it.** The OSF provider record's `allow_submissions` is **`false`** and its
  description reads: "LISSA is no longer able to accept new submissions. Existing content
  will remain accessible as part of COS's ongoing commitment to Open Science." (S11) [API] —
  the same verbatim boilerplate COS applied to Frenxiv, IndiaRxiv, MindRxiv, NutriXiv,
  SportRxiv and LawArXiv (see [osf-preprints.md](osf-preprints.md) §3.3).
- **`www.lissarchive.org` returns HTTP 525** (Cloudflare SSL handshake failure) while the
  apex `lissarchive.org` returns 200 (S12) [WEB] — a second, smaller certificate defect in
  the same record. Compare CogPrints (§1.2): **abandoned sites decay first at the TLS
  layer.**

**A conflict I am recording rather than resolving.** The API says
`allow_submissions: false`, but records with **`_v1` GUIDs** — genuinely new deposits, not
revisions — appear as recently as **2025-08-17** (`mw67v_v1`), **2025-08-11** (`qy7de_v1`)
and **2025-08-08** (`xz6gq_v1`) (S11) [API]. The most plausible reading is that the flag was
flipped some time between August and December 2025, i.e. **COS closed LISSA roughly five
years after LISSA announced it was leaving, and did so from the other side.** I could find
no COS or LISSA announcement of that closure and its date is **[NOT-VERIFIED]**.

**Content drift.** The ten most recent LISSA records include *"Baptism Without a Pool:
Collaborative Information Behavior Among Storefront Church…"*, *"Browsing the Spirit:
Applying Library Browsing Theory to Storefront Church…"*, *"No Longer Divided: Merging Mega
and Storefront Churches…"* and *"Preserving the Narrative: What Storefront Churches Lose
When Overshadowed…"* (S11) [API] — six of the last ten records are one author's series on
storefront churches. **This is what an unattended post-moderated repository looks like near
the end**: a single depositor becomes most of the recent corpus, and nobody is checking
scope. It is a useful, concrete diagnostic to know about.

## 3.3 What a computing person would find

Very little, and less than E-LIS. LISSA is a third the size, covers the same field, and
skews toward professional-practice outputs (promotion packets, oral histories, student work)
rather than technical LIS. It is worth knowing about for **repository-community history** —
LISSA's 2020 statement is a primary document about the strains of running a community server
on someone else's infrastructure — rather than for its contents.

One thing it did do well and is worth borrowing: **321 of 335 records (95.8%) carry a minted
preprint DOI** (S11) [API], a much better rate than recent deposits elsewhere on OSF, where
newly accepted preprints are currently being published with no identifier at all (see
[osf-preprints.md](osf-preprints.md) §6). LISSA's content is, ironically, more citable than
the live servers around it.

---

# 4. Cross-cutting caveats

1. **A TLS error is not evidence of deletion.** CogPrints' content is fully preserved and
   HTTPS to its historical hostname still fails (§1.3). Retry over HTTP, follow the
   redirect, and check the certificate's `CN` before writing anything off.
2. **Anti-scraper gates now sit in front of preserved archives.** Southampton's web-archive
   host runs **Anubis/BotStopper** and returns **HTTP 401 for real and bogus paths alike**
   (§1.3); ZBW runs Anubis in front of EconStor (see
   [repec-and-econstor.md](repec-and-econstor.md) §7.2); the Internet Archive was returning
   **429** to replay requests throughout this session. Three independent anti-bot walls
   encountered in one afternoon of ordinary archival probing. **Expect this to get worse and
   budget for it.** Where a repository exposes OAI-PMH, use it — that path was open in every
   case where it existed.
3. **An OAI `earliestDatestamp` is a migration date, not a founding date.** E-LIS launched
   in 2003 and its OAI datestamps begin in 2013 (§2.2).
4. **A live community website can describe a plan that was abandoned six years ago.** LISSA's
   `lissarchive.org` still fronts a November 2020 migration announcement and links to a
   submission form that COS has disabled (§3.2). **Check the content endpoint, not the
   community site.**
5. **Wikipedia's dates and sizes for all three are wrong or stale**: LISSA 2018 (actually
   2017); E-LIS ">10,000" (actually 27,455) and its article's "over 12,000" is a 2011
   figure; CogPrints ">1,000" against "over 4,000" in Wikipedia's own CogPrints article
   (S6, S7, S8).
6. **Post-moderation degrades silently.** LISSA's recent corpus is dominated by one
   depositor on a single topic (§3.2). Where a repository's `reviews_workflow` is
   `post-moderation` or unset, check *who deposited the recent records* before trusting the
   collection's stated scope.
7. **Survival correlates with distributed labour, not with content quality.** E-LIS survives
   on volunteer editors across 22 languages plus a university host; CogPrints and LISSA both
   depended on small groups and both stopped. If you are assessing whether a small
   repository will still be there in ten years, count the maintainers, not the papers.

---

# 5. Sources

- **S1** — CogPrints front page, retrieved via `http://cogprints.org/` which redirects to
  `https://web-archive.southampton.ac.uk/cogprints.org/`. Retrieved 2026-09-01, HTTP 200,
  7,419 bytes. Supports: the full scope statement, the "This site has been permanently
  archived. This is a static copy provided by the University of Southampton." notice, the
  "powered by EPrints 3 which is developed by the School of Electronics and Computer Science
  at the University of Southampton" footer, the advertised OAI 2.0 base URL
  `http://cogprints.org/cgi/oai2`, the SWORD service document, and the six subject branches
  (`psyc`, `neuro`, `ling`, `comp`, `phil`, `bio`).
- **S2** — CogPrints access probes, 2026-09-01: `https://cogprints.org/` (curl exit 60, TLS
  SAN mismatch, certificate `CN=web-archive.southampton.ac.uk` issued by Let's Encrypt
  `CN=YR1`); `http://cogprints.org/` (200 via redirect); and
  `https://web-archive.southampton.ac.uk/cogprints.org/{information.html,view/subjects.html,view/subjects/comp.html,cgi/oai2?verb=Identify,definitely-not-real-xyzzy.html}`
  (all HTTP 401, ~4,397 bytes, Anubis/BotStopper challenge page). Supports §1.3 in full.
- **S3** — E-LIS front page `https://eprints.rclis.org/` (200, 13,476 B) and About page
  `https://eprints.rclis.org/information.html` (200, 19,626 B). Retrieved 2026-09-01.
  Supports: "Established in 2003", the 22-language volunteer editor claim, hosting by the
  Library System (CAB) of the University of Naples Federico II, the named Administrative /
  Executive / Editorial boards, the JITA Classification Scheme and its maintainer, the
  pro-bono legal support, the EPrints 3.4.6 version string, the OAI base URL, and the
  RDFXML/RDFN3/SWORD/OpenSearch endpoints.
- **S4** — E-LIS OAI-PMH, `https://eprints.rclis.org/cgi/oai2`, verbs `Identify`,
  `ListSets`, `ListIdentifiers` (whole repository, per `from`/`until` window, and per set for
  all 22 `L.` subject sets). Retrieved 2026-09-01. Supports: 27,455 total records, the
  `Identify` fields including `earliestDatestamp` 2013-02-13T10:59:30Z and
  `deletedRecord: persistent`, the 406 sets, the activity-by-year table, the entire §2.4
  JITA `L.` table, and the HTTP 500 negative control.
- **S5** — Internet Archive CDX API,
  `https://web.archive.org/cdx/search/cdx?url=cogprints.org&output=json&…`. Retrieved
  2026-09-01. Supports: first capture 2004-12-09, last capture 2026-08-31, last HTTP 200 at
  the root 2024-08-03, first 301 2020-05-10, 301-only from late 2024 onward. (The Wayback
  *replay* service `web.archive.org/web/…` returned HTTP 429 throughout this session and
  could not be used.)
- **S6** — Wikipedia, *CogPrints*, wikitext via
  `https://en.wikipedia.org/w/index.php?title=CogPrints&action=raw`. Retrieved 2026-09-01.
  Supports: launch 1997, moderation by Stevan Harnad, "As of 2025, it contains over 4,000
  freely downloadable articles", early OAI compliance, the conversion of its software into
  EPrints by Rob Tansley (later a DSpace contributor), current EPrints maintenance by
  Christopher Gutteridge, and the analysis of the shift from centralised subject archives to
  institutional repositories. [LIT]
- **S7** — Wikipedia, *List of preprint repositories*, wikitext via
  `https://en.wikipedia.org/w/index.php?title=List_of_preprint_repositories&action=raw`.
  Retrieved 2026-09-01. Supports: the CogPrints row (Multidisciplinary; "Psychology,
  Neuroscience, Linguistics, Computer Science, Philosophy, and Biology"; ">1,000"; span
  1997–2017; University of Southampton), the E-LIS row (Library science; "Eprints in Library
  and Information Science"; ">10,000"; 2003; E-LIS Governance & CIEPI), and the LISSA row
  (Library science; ">100"; 2018; Center for Open Science).
- **S8** — Wikipedia, *E-LIS*, wikitext via
  `https://en.wikipedia.org/w/index.php?title=E-LIS&action=raw`. Retrieved 2026-09-01.
  Supports: launch date January 2003, "22 languages", ownership by E-LIS Governance and
  CIEPI, and the stale "Over 12,000 papers have been archived to date" claim sourced to a
  2011-08-02 retrieval. [LIT]
- **S9** — *e-LIS Policies: Check before submitting your papers*,
  `https://eprints.rclis.org/policies.html`. Retrieved 2026-09-01, HTTP 200, 21,453 bytes.
  Supports: the submission policy, the submission-buffer/manual-review process, the two
  business day turnaround, the accepted document types, the all-languages/English-abstract
  rule, the deposit agreement text, the author-bears-copyright-responsibility clause, and
  the existence of the preservation and bibliographic-data policies.
- **S10** — LISSA community site: `https://lissarchive.org/` (200, 8,648 B),
  `/updates/lissa-cos/` (200, 8,039 B), `/updates/` (200, 13,788 B), `/about/` (200,
  6,386 B), `/guidelines/` (200, 8,621 B). All retrieved 2026-09-01. Supports: the
  2020-11-30 migration announcement and its three options and 2020-12-20 survey deadline,
  the 2017-07-19 soft launch and 2017-10-26 full-launch posts, the accepted-content list,
  the code-of-conduct acceptance criterion and its attribution to PaleorXiv/SocArXiv, the
  GitLab source location, and the fact that the newest update is dated 2020-11-30.
- **S11** — OSF REST API v2, `https://api.osf.io/v2/preprints/?filter[provider]=lissa` (full
  enumeration, 4 pages) and `https://api.osf.io/v2/preprint_providers/`. Retrieved
  2026-09-01. Supports: 335 records / 325 distinct base GUIDs / 321 with
  `preprint_doi_created`, `reviews_workflow: post-moderation`, `allow_submissions: false`,
  the provider description boilerplate, the 2017-07-12 earliest and 2025-12-04 latest record
  dates, the `_v1` deposits in August 2025, and the ten most recent titles.
- **S12** — LISSA reachability probes, 2026-09-01: `https://lissarchive.org/` → 200;
  `https://www.lissarchive.org/` → **HTTP 525** (SSL handshake failed), 16 bytes;
  `https://osf.io/preprints/lissa` → 200 with the 4,207-byte OSF SPA shell (which, per
  [osf-preprints.md](osf-preprints.md) §8, is byte-identical to the response for a
  nonexistent provider and therefore carries no information).
