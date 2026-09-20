# Natural-science and niche preprint servers — grouped record

- **Compiled:** 2026-09-01 · **All reachability and count probes run:** 2026-09-01 / 2026-09-02 UTC
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

> **Scope note.** These are the small, single-discipline preprint servers of the natural
> sciences. Almost none carry electronics, software or systems content, so — as instructed —
> they are covered compactly and the weight is carried by the **measured status table**
> plus the durability evidence. Two entries get more room:
> - **[FocUS Archive](#10-focus-archive)** — focused-ultrasound therapy: the only entry in
>   this file with genuine **hardware** content (phased-array transducers, drive
>   electronics, MR-guided targeting).
> - **[mp_arc](#12-mp_arc)** — **opened July 1991**, contemporaneous with arXiv, one of the
>   oldest preprint archives in existence. Frozen since December 2023, still fully served,
>   and the best-preserved dead archive measured anywhere in this directory.

## 0. Method, and the OSF status trap

Nine servers here are or were hosted by the **Center for Open Science (COS)** on OSF, whose
web pages are a JavaScript SPA:

> **`https://osf.io/preprints/<anything>` returns HTTP 200 and an identical 4,207-byte
> shell even for providers that do not exist.**

Verified as a negative control: `https://osf.io/preprints/eyexiv/` returned **HTTP 200,
4,207 bytes** on 2026-09-02, yet `eyexiv` does not appear in the authoritative provider list
at `https://api.osf.io/v2/preprint_providers/?page[size]=100` (32 providers) (S1) [API]. All
OSF figures below therefore come from `api.osf.io/v2/preprints/?filter[provider]=<slug>` →
`links.meta.total`, and status claims from `api.osf.io/v2/preprint_providers/<slug>/`, whose
`description` carries the operator's own closure notice (S2) [API] [DOC]. Count-endpoint
negative control: `filter[provider]=bogusprovider12345` → `total: 0`, not an error [API].
Full discussion of the method in
[social-sciences-and-humanities.md §0](social-sciences-and-humanities.md#0-method-and-the-osf-status-trap).

Web reachability used the `AGENTS.md` UA ladder: default `curl` → Chrome 131 →
WhatsApp/2.23.20.0 → ChatGPT-User/1.0 → ClaudeBot/1.0.

## 1. Status and size table

| Server | URL probed 2026-09-02 | Operator | Launched | Status 2026-09-02 | Records | Source of count |
|---|---|---|---|---|---|---|
| **EarthArXiv** | `eartharxiv.org` | **California Digital Library**, on **Janeway 1.8.0** — moved off OSF | 2017 | **ALIVE**, submissions open | **7,525** live | operator's own listing [WEB] |
| ↳ legacy on OSF | `osf.io/preprints/eartharxiv` | COS | 2017 | **FROZEN**, submissions off, content retained | **1,649** | OSF API [API] |
| ↳ Crossref | prefix `10.31223` (CDL) | — | — | — | **8,171** | Crossref [API] |
| **ESS Open Archive** (ex-**ESSOAr**) | `essopenarchive.org` (`essoar.org` redirects here) | **AGU + Wiley**, on **Authorea** infrastructure | 2018 | **ALIVE** — but **HTTP 403 on all five UAs** | **≈23,000–27,000** (estimate, see §4) | Crossref [API] + [INF] |
| **EcoEvoRxiv** | `ecoevorxiv.org` | **California Digital Library**, Janeway — moved off OSF | 2018 | **ALIVE**, submissions open | **3,604** live | operator's own listing [WEB] |
| ↳ legacy on OSF | `osf.io/preprints/ecoevorxiv` | COS | 2018 | **FROZEN**, submissions off | **909** | OSF API [API] |
| **PaleorXiv** | `paleorxiv.org` → `osf.io/preprints/paleorxiv` | COS | 2017 | **ALIVE — submissions OPEN.** *Not frozen; see §6* | **282** | OSF API [API] |
| **MarXiv** | `osf.io/preprints/marxiv` | COS | 2017–2020 | **CLOSED**, content retained | **454** | OSF API [API] |
| ↳ own domain | `marxiv.org` | — | — | **DEAD** — TCP connection refused, port 443 | — | probe [WEB] |
| **NutriXiv** | `osf.io/preprints/nutrixiv` | COS | 2018 | **CLOSED**, content retained | **85** | OSF API [API] |
| ↳ own domain | `nutrixiv.org` | — | — | **DEAD** — DNS NXDOMAIN, all five UAs | — | probe [WEB] |
| **SportRxiv** | `sportrxiv.org` | **STORK** (Society for Transparency, Openness and Replication in Kinesiology); DOIs registered via **University of Ottawa Library** | 2017 | **ALIVE** on **Open Preprint Systems 3.3.0.22** | **761** | OAI `completeListSize` [API] |
| ↳ legacy on OSF | `osf.io/preprints/sportrxiv` | COS | 2017 | **CLOSED 2021-08-27**, content retained | **377** | OSF API [API] [DOC] |
| **FocUS Archive** | `osf.io/preprints/focusarchive` | **Focused Ultrasound Foundation** | 2018 | **ALIVE**, submissions open, pre-moderation | **84** | OSF API [API] |
| **Eyexiv** | `eyexiv.org`, `.com`, `.net`, `.io` | International Virtual Ophthalmic Research Center (S3) | 2022 (S3) | **DEAD or NEVER-RESOLVING** — DNS NXDOMAIN on every domain tried, all five UAs; **not an OSF provider** | **[NOT-VERIFIED]** | — |
| **mp_arc** | `web.ma.utexas.edu/mp_arc/` | **UT Austin** (with Università Roma Tre, Universitat de Barcelona) (S3) | **July 1991** | **FROZEN Dec 2023 — fully served, full text intact** | **6,152** | counted from operator's year indices [API] |
| **Frenxiv** | `osf.io/preprints/frenxiv` | COS | 2018–2022 | **CLOSED**, content retained | **128** | OSF API [API] |
| ↳ own domain | `frenxiv.org` | — | 2018 | **ZOMBIE** — HTTP 200, but frozen at Oct 2020 with a stale maintenance banner | not verified | probe [WEB] |
| **WikiJournal Preprints** | `en.wikiversity.org/wiki/WikiJournal_Preprints` | **WikiJournal User Group** on Wikiversity (**MediaWiki**) | 2017 (S3) | **ALIVE** | **421 pages** under the `WikiJournal Preprints/` prefix | MediaWiki API [API] |

**Conflicts recorded, not resolved.** Wikipedia's buckets (S3) give mp_arc `>10,000` against
my measured **6,152**; EarthArXiv `>1,000` against **7,525**; ESSOAr `>1,000`; SportRxiv,
NutriXiv, FocUS Archive and WikiJournal `<100` or `>100`. Where the two disagree, the
measured figure is stated with its method and Wikipedia's bucket is recorded alongside.

## 2. What the probe evidence shows

**(a) "Moved off OSF" is now the dominant life-cycle event, and it works.** EarthArXiv and
EcoEvoRxiv both migrated to **Janeway at the California Digital Library**, and both did it
*correctly*: the OSF record still exists, the vanity domain resolves to the new host, and the
operator's own OSF description explains the move and promises DOI redirection. EarthArXiv's:
*"EarthArXiv.org is now hosted by the California Digital Library (CDL). The EarthArXiv.org
URL now redirects to the CDL Janeway platform. **All article DOIs will redirect to CDL**"*
(S2) [DOC]. EcoEvoRxiv's is near-identical. **This is the reference example of a
well-executed repository migration** — contrast the vanity-domain losses documented in
[social-sciences-and-humanities.md](social-sciences-and-humanities.md) and
[closed-and-defunct-servers.md](closed-and-defunct-servers.md).

**(b) The self-hosted vanity domain is the component that dies.** `marxiv.org` refuses TCP
connections; `nutrixiv.org` is NXDOMAIN; `frenxiv.org` serves a page frozen in October 2020.
In all three cases the OSF-held content is intact and countable. Same finding as the
regional servers file — see
[regional-and-national-servers.md](regional-and-national-servers.md).

**(c) Bot-defence is now a first-order retrieval problem, and the byte size is a
fingerprint.** `essopenarchive.org` returned **HTTP 403 / 5,622 bytes** on all five UAs.
`www.authorea.com` returned **HTTP 403 / 5,620 bytes**. `www.techrxiv.org` and
`www.scienceopen.com` returned 403 at 5,620 and 5,602 bytes. These are all the same
Cloudflare managed-challenge page; the ~5.6 kB body is a reliable signature of "blocked, not
broken". **Crossref and OAI-PMH remain open in every one of these cases**, which is why every
ESSOAr figure below comes from Crossref.

---

## 3. EarthArXiv

- `eartharxiv.org` · California Digital Library · 2017 · **ALIVE** · **7,525 preprints** [WEB]

The Earth-science preprint server, founded 2017 on OSF and since migrated to **Janeway**, the
open-source journal/repository platform from Birkbeck, University of London.

The migration is verifiable from the machine interface rather than from press releases.
`https://eartharxiv.org/api/oai?verb=Identify`, retrieved 2026-09-02, returns
`repositoryName: EarthArXiv`, `adminEmail: no-reply@escholarship.org`, `earliestDatestamp:
2017-10-23T14:36:42Z`, and a `toolkit` block naming **Janeway 1.8.0**, Birkbeck, and
`http://janeway.systems/` (S4) [API]. The `escholarship.org` admin address and the site
footer — *"Powered by the California Digital Library and Janeway"* — establish the host [WEB].
The earliestDatestamp independently confirms the 2017 launch.

**Counts, three of them, all different and all defensible:** 7,525 on the live site,
1,649 still listed under the frozen OSF provider, and 8,171 works registered to CDL's
Crossref prefix `10.31223` (which mixes native `10.31223/X5…` DOIs with migrated
`10.31223/osf.io/…` ones) (S5) [API]. The Crossref figure is the superset; it includes
withdrawn and superseded deposits.

**Computing content: negligible**, though remote-sensing, geospatial ML and
methane-detection work appears — the live front page on 2026-09-02 led with *"Intelligent
National Map: A Vision for Distributed and Agentic Geospatial Intelligence"* and satellite
methane quantification [WEB].

## 4. ESS Open Archive (formerly ESSOAr)

- `essopenarchive.org` · **American Geophysical Union + Wiley** · 2018 · **ALIVE** ·
  **≈23,000–27,000 records (estimate)** [API] [INF]

Earth and space science preprints *and conference posters* — the poster mandate is unusual
and makes it the main durable home for AGU meeting material.

**It runs on Authorea infrastructure**, and Authorea is Wiley-owned. A sibling record covers
the platform in detail: see **[authorea.md](authorea.md)**. The evidence for the coupling is
direct: DOIs minted for ESS Open Archive today live under Authorea's Crossref prefix
**10.22541** in the `essoar` namespace (e.g. `10.22541/essoar.169290541.19921945/v1`), and
every one of 100 sampled `posted-content` records under that prefix reports
`publisher: Wiley` (S5) [API]. Legacy deposits use Wiley's own prefix in the form
`10.1002/essoar.*` — and a spot-check of `10.1002/essoar.10500599.1` returns
`institution: [{name: "Earth and Space Science Open Archive", acronym: ["ESSOAr"]}]` (S5)
[API].

**Why the count is an estimate, stated honestly.** The website returned **HTTP 403 on all
five user-agents** (5,622-byte Cloudflare challenge), so no operator-published total was
obtainable. Reconstructing from Crossref:

- `filter=prefix:10.1002,type:posted-content` → **13,033** works; a random sample of 100
  found **99 with DOIs of the form `/essoar.*`** (the hundredth was `/oarr.*`) (S5) [API].
  So the legacy corpus is ~12,900.
- `filter=prefix:10.22541,type:posted-content` → **80,496** works; four independent random
  samples of 100 found **17, 16, 12 and 17** `essoar`-namespace DOIs, the rest being generic
  Authorea `au.*` preprints (S5) [API]. At ~15.5% that implies **≈12,500** ESS Open Archive
  records on the Authorea prefix, with sampling error of a couple of thousand.

**Total ≈ 23,000–27,000 [INF from API].** Treat this as an order-of-magnitude figure, not a
count. **[NOT-VERIFIED]:** the operator's own published total.

**Computing content: negligible.** Instrumentation and data-system papers appear
(satellite payloads, sensor networks), but there is no software or electronics category.

## 5. EcoEvoRxiv

- `ecoevorxiv.org` · California Digital Library, Janeway · 2018 · **ALIVE** ·
  **3,604 preprints** [WEB]

Ecology, evolution and conservation. Same story as EarthArXiv and executed the same way: the
OSF description reads *"Submissions are currently suspended. EcoEvoRXiv.org is moving to the
Janeway platform hosted by the California Digital Library (CDL) … All article DOIs will
redirect"* (S2) [DOC]. Live site: 3,604; frozen OSF provider: 909; CDL Crossref prefix
`10.32942`: 3,675 (S5) [API]. The near-agreement between the live count and the Crossref
count (a 2% gap) is a good sign — the migration carried the DOIs across.

**Computing content: none.**

## 6. PaleorXiv

- `paleorxiv.org` → `osf.io/preprints/paleorxiv` · COS · 2017 · **ALIVE** · **282
  preprints** [API]

**Correction to the working assumption.** PaleorXiv was expected to be frozen. It is not:
the OSF provider record on 2026-09-02 reports `allow_submissions: true` and
`reviews_workflow: pre-moderation`, with the plain description *"A preprint archive for
Paleontology"* — **no closure notice** (S2) [API] [DOC]. Compare the four servers in this
file that *do* carry one (MarXiv, NutriXiv, SportRxiv, Frenxiv); the text is boilerplate and
its absence is meaningful. `paleorxiv.org` redirects correctly to OSF.

It is small and slow-moving, but open. **Computing content: none.**

## 7. MarXiv

- `osf.io/preprints/marxiv` · COS · **2017–2020, CLOSED** · **454 preprints retained** [API]

Ocean and marine-climate science. The operator's closure notice is unusually explicit about
preservation: *"Submissions for Marxiv are now closed. **Existing preprints will be
maintained by COS as part of the long-term data preservation plan.**"* (S2) [DOC] — and the
API confirms all 454 are still served, six years on.

`marxiv.org` **refuses TCP connections on port 443** under all five user-agents [WEB]. This
is a cleaner failure than a parking page or a hijack: nothing is served, so nothing
misleading is served. Cite the OSF DOI. See
[closed-and-defunct-servers.md](closed-and-defunct-servers.md).

## 8. NutriXiv

- `osf.io/preprints/nutrixiv` · COS · 2018 · **CLOSED** · **85 preprints retained** [API]

Nutritional sciences, and the smallest server documented in this directory. Standard COS
closure notice: *"NutriXiv is no longer able to accept new submissions. Existing content in
this repository will remain accessible as part of COS's ongoing commitment to Open
Science."* (S2) [DOC]. `nutrixiv.org` is **DNS NXDOMAIN** on all five UAs [WEB].

Worth one line of reflection: 85 records is below the threshold at which a repository is
doing anything a general server would not do better. The COS closure programme was, in
substance, a rational consolidation.

## 9. SportRxiv

- `sportrxiv.org` · **STORK** — Society for Transparency, Openness and Replication in
  Kinesiology · 2017 · **ALIVE on Open Preprint Systems 3.3.0.22** · **761 records** [API]

Sport, exercise, performance and health research, and the one server here that migrated
**off OSF onto self-hosted PKP software** and made it work.

- **Exact migration date, first-party.** The frozen OSF provider says: *"SportRxiv is no
  longer accepting submissions as of **8/27/2021**, and all new submissions can be posted to
  the new platform SportRxiv OPS (sportrxiv.org)"* (S2) [DOC]. 377 legacy records remain on
  OSF.
- **Software and size.** The front page declares `generator: Open Preprint Systems 3.3.0.22`
  (PKP's preprint variant of OJS). OAI-PMH at `sportrxiv.org/index.php/server/oai` reports
  `repositoryName: SportRxiv`, `adminEmail: layan.fessler@storkinesiology.org`,
  `earliestDatestamp: 2021-08-12` — i.e. two weeks before the OSF cutoff, so the two
  overlapped deliberately — and `ListIdentifiers` returns
  **`completeListSize="761"`** (S6) [API].
- **It is genuinely active.** Two of the newest items on the front page carried
  `Submitted 2026-09-01 · Posted 2026-09-01`, DOIs `10.51224/SportRxiv.1053` and `.1052`
  [WEB] — same-day posting on the day of this survey.
- **DOI ownership is a small puzzle worth recording.** Prefix `10.51224` is registered to
  *"Society for Transparency, Openness, and Replication in Kinesiology"* and holds **779**
  works, but sampled records report `publisher: University of Ottawa Library` with DOIs in
  the older `10.51224/srxiv.NNN` form, while the live site mints `10.51224/SportRxiv.NNNN`
  (S5) [API]. Two DOI generations under one prefix, with library hosting behind it. **The
  exact hosting arrangement with uOttawa Library: [NOT-VERIFIED].**

**Computing content: none.** But as a *systems* case study SportRxiv is the positive control
for §2(b): a small community that moved to its own infrastructure, kept the DOIs, kept the
old records readable, ran OAI-PMH, and is still posting five years later.

## 10. FocUS Archive

- `osf.io/preprints/focusarchive` · **Focused Ultrasound Foundation (FUSF)** · 2018 ·
  **ALIVE**, pre-moderation · **84 preprints** [API]

**The only hardware content in this file.** Focused ultrasound is a therapeutic-device
field: hemispherical **phased-array transducers** of 128–1024 elements, per-channel drive
electronics and phase control, **skull-aberration correction** computed from CT, MR
thermometry for closed-loop targeting, cavitation-detection receivers, and — the part a
systems reader will recognise — hard real-time control loops with patient-safety interlocks.
Papers here are as likely to be about array calibration and beamforming as about biology.

The provider is unusually well-specified for its size. The OSF description reads: *"Focus
Archive is an OSF-hosted preprint space for rapid sharing of reports, data, notes, and
methods from **Focused Ultrasound Foundation (FUSF) funded projects**"*, and links a
first-party policy document, *Focus Archive Publication Policies 2025*, at
`https://cdn.fusfoundation.org/2025/11/20165255/Focus-Archive-Publication-Policies-2025.pdf`;
the advisory board is named as **Frederic Padilla** and **Joe Killroy** (S2) [DOC].

**Read the scope restriction carefully before citing.** This is a **funder's** archive for
**its own grantees' outputs**, including "reports, data, notes, and methods" — i.e. grey
literature, not just preprints. A deposit here is evidence that FUSF funded the work and a
moderator passed it; it is not evidence of peer review, and the corpus is *not* a
representative sample of the focused-ultrasound literature. At 84 records it is browsable in
full, which is the right way to use it.

**[NOT-VERIFIED]:** the contents of the 2025 policy PDF — I recorded the URL from the
operator's own metadata but did not retrieve and read the document.

## 11. Eyexiv

- `eyexiv.org` / `.com` / `.net` / `.io` · **all DNS NXDOMAIN** on all five UAs, 2026-09-02 ·
  **status: unreachable** · **count [NOT-VERIFIED]**

Vision science — ophthalmology, optometry. Wikipedia describes it as *"The Eye Open
Repository, Preprints founded by Dr. F. Heidary for ophthalmology, optometry, and vision
science"*, bucket `>100`, launched **2022**, operator **International Virtual Ophthalmic
Research Center** (S3) [COM].

**Everything I could probe failed.** Four TLDs, five user-agents each: NXDOMAIN throughout.
It is **not** in the OSF provider list, and — this is the useful part —
`https://osf.io/preprints/eyexiv/` nonetheless returns **HTTP 200 with the standard
4,207-byte OSF SPA shell**, exactly as a real provider would [API] [WEB]. Eyexiv is
therefore the cleanest available demonstration of why OSF status codes must never be trusted:
had I probed only that URL, I would have "confirmed" a repository that does not exist there.

I could not establish where, if anywhere, Eyexiv's content now lives. **[NOT-VERIFIED]:**
launch, size, current host, and whether it ever served content at a resolvable domain.

## 12. mp_arc

- `https://web.ma.utexas.edu/mp_arc/` · **University of Texas at Austin** (with Università
  Roma Tre and Universitat de Barcelona, per S3) · **July 1991 – December 2023** ·
  **FROZEN, fully served** · **6,152 records** [API]

**Flagged. This is the oldest server in this file by fourteen years and one of the oldest
preprint archives anywhere** — arXiv's first deposit was in August 1991; mp_arc's first
was in **July 1991**.

**Its own front page states the fate, unambiguously** (retrieved 2026-09-02) (S7) [DOC]:

> *"mp_arc is an electronic archive for research papers in Mathematical Physics and related
> areas. It **accepted and posted preprints from July 1991 until December 2023**. Those
> preprints will **stay posted here indefinitely**. But no new submissions will be
> processed. At this point in time, there are enough alternative ways to disseminate
> preprints."*

That is the healthiest shutdown notice in this entire directory: a stated span, a stated
preservation commitment, and a stated reason. Compare the servers that simply stopped
answering.

**Is the content still served? Yes — verified end to end.**

| Probe (2026-09-02) | Result |
|---|---|
| `web.ma.utexas.edu/mp_arc/` | HTTP 200, `Server: Apache/2.4.58 (Ubuntu)` — a **current, maintained** OS release [API] |
| Year index `index-91.html` … `index-23.html` | all 200; **33 index files, 1991–2023** [API] |
| Record CGI `mp_arc-bin/mpa?yn=91-1` | 200 — Koch & Wittwer, *"On the Renormalization Group Transformation for Scalar Hierarchical Models"*, Jul 10 1991 [API] |
| Oldest full text `mp_arc/c/91/91-1.ps.gz` | **200, 120,018 bytes, `application/postscript`.** `file` reports *gzip compressed data, last modified **Sat Apr 26 1997**, original size 426,991* [API] |
| Newest full text `mp_arc/c/23/23-1.pdf` | **200, 351,086 bytes, valid PDF 1.5, 6 pages** [API] |
| **Negative control** `mp_arc-bin/mpa?yn=99-99999` | HTTP **200** but 174 bytes: *"Found no abstract for 99-99999."* — a 200 does **not** mean a record exists |
| **Negative control** `mp_arc/index-77.html` | HTTP **404**, 280 bytes — static paths do 404 correctly |

**The gzip mtime is the detail to take away.** The bytes of mp_arc's first paper were last
written in **April 1997** and are still being served, unaltered, in **2026** — 29 years of
untouched file custody, across at least one operating-system generation (the server is now
Ubuntu with Apache 2.4.58). No CMS, no database, no migration. Static files under a web
server, maintained by a mathematics department.

**Size — and a conflict.** Counting `<dt>YY-` entries across all 33 year indices gives
**6,152 records** (S7) [API]. Wikipedia's bucket is `>10,000` (S3) [COM]. **Both are
recorded; I did not resolve the discrepancy**, and note that my method counts index entries,
which may undercount multi-version submissions. The per-year distribution is itself the
story of the field's migration to arXiv:

```
1991  47   1996 296   2001 359   2006 286   2011 123   2016  59   2021  40
1992  80   1997 331   2002 382   2007 236   2012 118   2017  48   2022  45
1993 171   1998 386   2003 391   2008 172   2013  76   2018  52   2023  34
1994 202   1999 353   2004 326   2009 169   2014  68   2019  47
1995 249   2000 387   2005 341   2010 141   2015  76   2020  61
```

Peak ~391/year in 2003, decaying to 34 in the final year. The archive did not fail; **its
users left for arXiv**, and it closed with dignity.

**Access:** no OAI-PMH, no REST API, no DOIs. Retrieval is by predictable static path —
`mp_arc/index-YY.html` for indices, `mp_arc/c/YY/YY-N.{pdf,ps.gz}` for full text — which is
about as scrape-friendly as an archive gets. **Preservation: [NOT-VERIFIED]** — I found no
statement of a dark archive or successor custodian, and "indefinitely" is a promise from a
university department, not a contract with Portico or CLOCKSS.

## 13. Frenxiv

- `osf.io/preprints/frenxiv` · COS · **2018–2022, CLOSED** · **128 preprints retained** [API]
- `frenxiv.org` · **ZOMBIE — HTTP 200, frozen at October 2020**

The French multidisciplinary server, founded by Khaled Moustafa. Closed on OSF with the
standard notice: *"Frenxiv is no longer able to accept new submissions. Existing content in
this repository will remain accessible as part of COS's ongoing commitment to Open
Science."* (S2) [DOC].

**The interesting artefact is the second, non-OSF instance.** `frenxiv.org` returns HTTP 200
with a 44,186-byte page titled *"Frenxiv Papers"*, with working navigation, a subject
browse, and a steering committee listing Björn Brembs, Sophien Kamoun, Mario Pagliaro and
others. It looks alive. It is not:

- It displays a stuck banner reading *"Notice: The site will undergo maintenance between
  **Oct 28, 2020** 9:19 AM and Oct 28, 2020 9:19 AM (+0000 UTC). Thank you for your
  patience."* — a zero-length maintenance window from six years ago, still rendering [WEB].
- The footer reads *"Copyright © **2011-2020**"* [WEB].

**This is the most deceptive failure state observed in this survey**: a fully-rendering,
professional-looking repository front end that has been frozen for six years and gives a
casual reader no reason to doubt it. A dead site that refuses connections (MarXiv) is
*safer* than one that renders. **Check the copyright year and the newest item date before
trusting any small repository's front page.**

## 14. WikiJournal Preprints

- `en.wikiversity.org/wiki/WikiJournal_Preprints` · **WikiJournal User Group** · 2017 (S3) ·
  **ALIVE** · **421 pages** under the `WikiJournal Preprints/` prefix [API]

The structurally strangest entry in this directory: preprints as **MediaWiki pages** on
English Wikiversity, not as PDFs in a repository. Each submission is a wiki page under
`WikiJournal Preprints/<Title>`, edited, versioned and discussed with the same machinery as
a Wikipedia article, then routed through public peer review into one of the WikiJournals
(*Medicine*, *Science*, *Humanities*, *PPB*).

The self-description on 2026-09-02: *"WikiJournal is an emerging publishing house
specialized in running **open-access, free-to-publish, Wikipedia-integrated** academic
journals"*, with the banner *"Open access • Publication charge free • Public peer review"*
(S8) [WEB].

**The Wikipedia-integration angle is the point.** The model is that a reviewed WikiJournal
article can be merged back into the corresponding Wikipedia article — an attempt to make
peer-reviewed scholarship and the encyclopedia the same artefact. Whatever one thinks of it,
it inverts the usual relationship, in which Wikipedia cites the literature and the
literature ignores Wikipedia.

**Count method:** `https://en.wikiversity.org/w/api.php?action=query&list=allpages&
apprefix=WikiJournal_Preprints/&aplimit=500&format=json` returned **421 pages** with no
continuation token (S8) [API]. This counts *pages*, including drafts and a
`preload draft` template — treat it as an upper bound on genuine submissions.

**Durability profile — quietly excellent.** WikiJournal Preprints inherits **Wikimedia
Foundation** hosting, full public revision history for every item, the MediaWiki API, and
Wikimedia's public database dumps. Of everything in this file, only mp_arc and the
CDL-hosted servers have a comparably credible answer to "will this be readable in 2040". A
wiki page is not a PDF and has no DOI, but it is versioned, mirrored and dumped.

**Computing content: negligible** in practice, though the corpus is genuinely
multidisciplinary (the 421 pages include mathematics, physics and phonology titles).

## 15. Adjacent servers covered elsewhere

- **Optimization Online** — mathematical optimisation, founded 2000, operated by the
  Mathematical Optimization Society. Formally a mathematics server, so it might have landed
  in this file, but it is **computationally relevant** — solver design, integer-programming
  algorithms, convex-optimisation methods that underpin practical scheduling, routing,
  compiler and ML-training work — and it therefore has its own full record:
  **[optimization-online.md](optimization-online.md)**. Wikipedia's bucket is `>10,000`
  since 2000 (S3); it was reachable at HTTP 200 / 98,725 bytes in the 2026-09-01 sweep (S9)
  [WEB].
- **ESS Open Archive's platform** — see **[authorea.md](authorea.md)**.
- **hprints**, the Nordic humanities server on HAL infrastructure, is in
  **[social-sciences-and-humanities.md](social-sciences-and-humanities.md)**; the platform is
  in **[hal.md](hal.md)**.
- **Closed servers** listed here in brief — MarXiv, NutriXiv, Frenxiv, mp_arc — are also
  entered in the cross-cutting
  **[closed-and-defunct-servers.md](closed-and-defunct-servers.md)**.

## 16. Access, APIs and bulk retrieval — summary

| Server | Machine interface | Works from scripts? |
|---|---|---|
| OSF-hosted (PaleorXiv, MarXiv, NutriXiv, FocUS, Frenxiv, legacy EarthArXiv/EcoEvoRxiv/SportRxiv) | `api.osf.io/v2/` JSON:API | **Yes**, no key. URL-encode `filter%5Bprovider%5D=` |
| EarthArXiv, EcoEvoRxiv | **OAI-PMH** at `/api/oai` (Janeway 1.8.0) | **Yes**, plain `curl` |
| SportRxiv | **OAI-PMH** at `/index.php/server/oai` (OPS 3.3.0.22), gives `completeListSize` | **Yes**, plain `curl` |
| ESS Open Archive | none reachable — site 403s on all five UAs | **No.** Use **Crossref** (`prefix:10.22541`, `prefix:10.1002`) |
| mp_arc | none — but fully predictable static paths | **Yes**, trivially |
| WikiJournal Preprints | **MediaWiki API** `en.wikiversity.org/w/api.php` + Wikimedia dumps | **Yes**, excellent |
| Eyexiv | — | **No** — does not resolve |

**Negative controls used:** `osf.io/preprints/eyexiv/` → HTTP 200 / 4,207 B for a
non-existent provider; `filter[provider]=bogusprovider12345` → `total: 0`;
`mp_arc-bin/mpa?yn=99-99999` → HTTP 200 / 174 B "Found no abstract";
`mp_arc/index-77.html` → HTTP 404.

## 17. Sources

- **S1** — OSF preprint-provider list.
  `https://api.osf.io/v2/preprint_providers/?page[size]=100` · retrieved 2026-09-02 · 32
  providers; establishes that `eyexiv` is not among them. [API]
- **S2** — OSF counts and provider records.
  `https://api.osf.io/v2/preprints/?filter[provider]=<slug>&page[size]=1` (`links.meta.total`)
  and `https://api.osf.io/v2/preprint_providers/<slug>/` · retrieved 2026-09-02 · every OSF
  count, and the verbatim closure/migration notices for MarXiv, NutriXiv, Frenxiv,
  SportRxiv, EarthArXiv, EcoEvoRxiv, plus the FocUS Archive description, policy-PDF URL and
  advisory board. [API] [DOC]
- **S3** — Wikipedia, *List of preprint repositories*.
  `https://en.wikipedia.org/wiki/List_of_preprint_repositories` · retrieved 2026-09-02 ·
  launch years, operators, size buckets. Used only where no first-party source existed, and
  always flagged. [COM]
- **S4** — EarthArXiv OAI-PMH. `https://eartharxiv.org/api/oai?verb=Identify` · retrieved
  2026-09-02 · Janeway 1.8.0, `no-reply@escholarship.org`, earliestDatestamp 2017-10-23.
  Live counts from `https://eartharxiv.org/repository/search/` and
  `https://ecoevorxiv.org/repository/search/` ("There are N Preprints listed"). [API] [WEB]
- **S5** — Crossref REST API. `https://api.crossref.org/prefixes/<prefix>`,
  `/prefixes/<prefix>/works?rows=0`, `/works?filter=prefix:…,type:posted-content&sample=100`,
  and `/works/10.1002/essoar.10500599.1` · retrieved 2026-09-02 · prefix ownership
  (10.31223 & 10.32942 → California Digital Library; 10.22541 → Authorea, Inc.; 10.51224 →
  STORK), prefix totals, and the ESSOAr namespace sampling. [API]
- **S6** — SportRxiv. `https://sportrxiv.org/` (generator: Open Preprint Systems 3.3.0.22;
  DOIs and same-day 2026-09-01 postings) and
  `https://sportrxiv.org/index.php/server/oai?verb=Identify` /
  `?verb=ListIdentifiers&metadataPrefix=oai_dc` (`completeListSize="761"`,
  earliestDatestamp 2021-08-12, adminEmail `layan.fessler@storkinesiology.org`) · retrieved
  2026-09-02. [WEB] [API]
- **S7** — mp_arc. `https://web.ma.utexas.edu/mp_arc/` (the 1991–2023 statement, verbatim),
  `index-91.html` … `index-23.html` (per-year counts summing to 6,152),
  `mp_arc-bin/mpa?yn=91-1` and `?yn=23-1`, `mp_arc/c/91/91-1.ps.gz` (gzip mtime 1997-04-26),
  `mp_arc/c/23/23-1.pdf` (valid 6-page PDF), plus the two negative controls · all retrieved
  2026-09-02. [WEB] [DOC] [API]
- **S8** — WikiJournal Preprints.
  `https://en.wikiversity.org/wiki/WikiJournal_Preprints` (self-description, banner) and
  `https://en.wikiversity.org/w/api.php?action=query&list=allpages&apprefix=WikiJournal_Preprints/&aplimit=500&format=json`
  (421 pages, no continuation) · retrieved 2026-09-02. [WEB] [API]
- **S9** — Directory-wide reachability sweep.
  `doc/hardware/scratch/preprint-repositories/reachability-2026-09-01.txt` (run 2026-09-01)
  and the per-URL UA-ladder log in
  `doc/hardware/scratch/preprint-repositories/humanities/` (run 2026-09-02) · supports the
  403/NXDOMAIN/connection-refused claims for `essopenarchive.org`, `www.authorea.com`,
  `marxiv.org`, `nutrixiv.org`, `eyexiv.*` and `frenxiv.org`. [WEB]
