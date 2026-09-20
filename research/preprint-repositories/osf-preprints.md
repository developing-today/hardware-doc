# OSF Preprints — preprint repository record

- **URL:** https://osf.io/preprints/ · API root https://api.osf.io/v2/
- **Operator:** Center for Open Science (COS), Charlottesville, Virginia — a US 501(c)(3)
  non-profit. COS builds and runs the infrastructure; the individual *preprint services*
  are branded and moderated by outside research communities (S6, S9).
- **Discipline scope:** advertised as multidisciplinary — *as actually used*, overwhelmingly
  psychology, sociology, education and the social sciences (§2, §3). Engineering and
  computing presence is marginal and shrinking (§7).
- **Launched:** **2016** — COS's own retrospective dates the OSF Preprints service to 2016
  (S6) [DOC]; the oldest live record on the platform is 2016-07-13 (S1) [API]. Wikipedia
  gives 2017 (S10).
- **Status:** **active, but contracting.** The generalist server has been **closed to new
  submissions since 2025-08-25** (S6, S7) and Thesis Commons since **2026-06-03** (S1).
  18 of 32 providers no longer accept submissions (§3.2).
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

> **Why this record exists.** A large fraction of the entries in Wikipedia's *List of
> preprint repositories* — AfricArXiv, AgriXiv, Arabixiv, BioHackrXiv, BodoArXiv,
> EarthArXiv, EcoEvoRxiv, ECSarXiv, EdArXiv, engrXiv, Frenxiv, INA-Rxiv, IndiaRxiv,
> LawArXiv, LISSA, MarXiv, MediArXiv, MetaArXiv, MindRxiv, NutriXiv, PaleorXiv, PsyArXiv,
> SocArXiv, SportRxiv, Thesis Commons — are or were **the same piece of software with
> different logos**. They are not independent repositories. This record documents the
> substrate once, with measured numbers, so the other records can point here instead of
> repeating themselves. §3.2 is the payload.

---

## 1. What it is

The **Open Science Framework (OSF)** is a research-workflow platform: project pages, file
storage, version control, preregistrations, registrations and — since 2016 — preprints. It
is free at the point of use and funded by philanthropy, grants, and institutional/community
memberships. **OSF Preprints** is the preprint module of that platform.

The design idea is *white-labelling*. COS wrote one preprint service and then let outside
communities rent a branded instance of it. In COS's own words the service "was built in two
parts": **community-run preprint servers**, where "COS developed infrastructure that can be
customized and operated by research communities themselves … [allowing] research
communities to set their own standards, build norms for open sharing, and reduce redundant
development costs"; and a **generalist server**, "a multidisciplinary venue that accepts
submissions from any domain of scholarship … managed and moderated directly by COS staff"
(S6) [DOC].

That is why `psyarxiv.com`, `engrxiv.org` and `ecsarxiv.org` all looked identical in 2019:
they were the same Ember front end reading the same Django API, with a different logo,
colour scheme and moderator pool. Each got a slug — `psyarxiv`, `engrxiv`, `ecsarxiv` — and
a landing page at `osf.io/preprints/<slug>`. The community supplied volunteer moderators and
an advisory board; COS supplied everything else.

For a reader of this knowledge base the consequences are practical and mostly unwelcome:

- **A citation to `osf.io/preprints/<slug>/<guid>` has a single point of failure.** If COS
  changes strategy — and it has (§4) — every server on the platform is affected at once.
- **The branded vanity domains are the fragile part.** `engrxiv.org`, `eartharxiv.org`,
  `arabixiv.org` and others now point somewhere else entirely, because the *community*
  moved and took the domain with it while the *content* stayed on OSF (§3.3).
- **"OSF Preprints" is not one repository with 200,000 papers.** It is 32 separate
  collections, of which two (PsyArXiv and the generalist server) hold **70.6%** of
  everything (§3.1) [API].

## 2. Scope and subject taxonomy

OSF has no arXiv-style category codes. There is no `cs.DC` equivalent. The only structural
axes are:

**(a) Provider.** The 32 slugs in §3.2. This is the real taxonomy, and it is a taxonomy of
*communities*, not of subjects.

**(b) `subjects`** — a bibliographic subject tree (bepress-derived) attached per preprint.
It is coarse and optional-in-practice; it is not usable as a discipline filter with any
precision. `/v2/preprints/?filter[provider]=X` is reliable; subject filtering is not, and
this record does not use it.

**(c) Free-text tags** — uncontrolled.

For computing and electronics, the honest statement is: **OSF Preprints has no computing
taxonomy and essentially no computing community.** ECSarXiv (electrochemistry/solid-state)
and the frozen engrXiv archive are the only two providers with any engineering content at
all, and between them they hold 2,356 records — 1.2% of the platform (§3.2, §7) [API].

## 3. Size and growth

### 3.1 Headline

Retrieved 2026-09-01 from `https://api.osf.io/v2/preprints/?page[size]=1` (S1) [API]:

- **200,519** preprint records across all providers.
- Summing the 32 per-provider counts in §3.2 gives **exactly 200,519** — the per-provider
  filter partitions the corpus with no overlap and no unassigned remainder. That is a
  useful internal consistency check and it passed.
- The two largest providers — the generalist `osf` server (78,195) and PsyArXiv (63,368) —
  hold **141,563 records, 70.6% of the total** [INF, from S1].

**Counting caveat — records are versions, not works.** Since OSF added preprint versioning,
each revision becomes its own record with its own GUID suffix (`qa4sz_v2`, `qa4sz_v3`) and
each is counted separately by `meta.total`. Measured by full enumeration, 2026-09-01 (S1)
[API]:

| Provider | Records (`meta.total`) | Distinct base GUIDs | Inflation |
|---|---|---|---|
| ECSarXiv | 323 | 318 | +1.6% |
| LISSA | 335 | 325 | +3.1% |
| BioHackrXiv | 173 | 163 | +6.1% |
| Accounting Research & Thought | 6 | 4 | +50% |

The effect is small in aggregate because versioning is recent: of the **300 oldest** records
on each of PsyArXiv, SocArXiv and the generalist server, **300/300 were `_v1`** — but of the
**100 newest** generalist-server records, only **6 were `_v1`** and the rest were revisions
up to `_v30` (S1) [API]. Treat every count in §3.2 as *records*, an upper bound on *works*,
with a few percent of slack.

### 3.2 The provider table — every COS-hosted preprint service, measured

Authoritative provider list from `https://api.osf.io/v2/preprint_providers/?page[size]=100`
(`meta.total = 32`, one page, no pagination needed) (S2) [API]. Counts, earliest and latest
record dates from `https://api.osf.io/v2/preprints/?filter[provider]=<slug>` with
`sort=date_created` / `sort=-date_created`, all retrieved **2026-09-01** (S1) [API].
"Open?" is the API's own `allow_submissions` flag.

| # | Slug | Display name | Discipline (operator's own words, S2) | Records | Earliest | Latest | Moderation | Open? |
|---|---|---|---|---|---|---|---|---|
| 1 | `osf` | Open Science Framework (generalist) | any domain of scholarship | **78,195** | 2016-08-29 | 2026-09-01 | COS staff | **no** (susp. 2025-08-25) |
| 2 | `psyarxiv` | PsyArXiv | psychological sciences | **63,368** | 2016-08-15 | 2026-09-01 | pre | yes |
| 3 | `socarxiv` | SocArXiv | social sciences | **24,670** | 2016-07-13 | 2026-08-31 | pre | yes |
| 4 | `inarxiv` | INA-Rxiv | Indonesian research (all fields) | **15,987** | 2017-08-20 | 2020-08-17 | pre | no (closed 2020-10-07) |
| 5 | `edarxiv` | EdArXiv | education research | **3,506** | 2019-02-18 | 2026-08-29 | pre | yes |
| 6 | `thesiscommons` | Thesis Commons | theses and dissertations | **2,866** | 2017-04-21 | 2026-08-27 | none set | no (susp. 2026-06-03) |
| 7 | `engrxiv` | engrXiv (Engineering Archive) | engineering | **2,033** | 2016-07-27 | 2022-01-19 | pre | no (moved 2022-01-19) |
| 8 | `lawarchive` | Law Archive | legal scholarship | **1,664** | 2016-07-28 | 2026-08-27 | pre | yes |
| 9 | `eartharxiv` | EarthArXiv | earth science | **1,649** | 2017-10-23 | 2020-09-01 | pre | no (moved to CDL) |
| 10 | `metaarxiv` | MetaArXiv | research transparency & reproducibility | **1,014** | 2017-03-03 | 2026-08-31 | pre | yes |
| 11 | `ecoevorxiv` | EcoEvoRxiv | ecology & evolutionary biology | **909** | 2018-03-21 | 2022-09-30 | pre | no (moved to CDL) |
| 12 | `africarxiv` | AfricArXiv | African research | **479** | 2018-06-22 | 2024-04-07 | pre | no |
| 13 | `marxiv` | MarXiv | marine & conservation science | **454** | 2017-11-09 | 2025-08-12 | post | no |
| 14 | `mediarxiv` | MediArXiv | media, film & communication studies | **443** | 2019-02-02 | 2026-08-19 | pre | yes |
| 15 | `agrixiv` | AgriXiv | agriculture & allied sciences | **397** | 2017-02-15 | 2020-05-18 | pre | no (moved to agriRxiv) |
| 16 | `sportrxiv` | SportRxiv | sport, exercise, performance, health | **377** | 2017-08-18 | 2021-08-18 | pre | no |
| 17 | `lissa` | LIS Scholarship Archive | library & information science | **335** | 2017-07-12 | 2025-12-04 | post | no |
| 18 | `ecsarxiv` | ECSarXiv | electrochemistry & solid state science | **323** | 2018-05-09 | 2026-08-22 | pre | yes |
| 19 | `arabixiv` | Arabixiv | Arabic-language research | **298** | 2018-01-14 | 2020-12-11 | pre | no (moved to Zenodo) |
| 20 | `mindrxiv` | MindRxiv | mind & contemplative practices | **288** | 2017-07-07 | 2024-12-20 | pre | no |
| 21 | `paleorxiv` | PaleorXiv | paleontology | **282** | 2017-08-18 | 2026-08-30 | pre | yes |
| 22 | `biohackrxiv` | BioHackrXiv | biohackathon reports | **173** | 2020-02-17 | 2026-08-26 | pre | yes |
| 23 | `bodoarxiv` | BodoArXiv | medieval studies | **165** | 2019-03-19 | 2026-08-22 | pre | yes |
| 24 | `lawarxiv` | LawArXiv | legal scholarship (superseded) | **165** | 2016-07-16 | 2025-05-14 | none set | no |
| 25 | `frenxiv` | Frenxiv | French-language research | **128** | 2018-07-06 | 2020-12-31 | pre | no |
| 26 | `indiarxiv` | IndiaRxiv | Indian research | **121** | 2019-06-10 | 2020-12-28 | pre | no |
| 27 | `nutrixiv` | NutriXiv | nutritional sciences | **85** | 2017-08-24 | 2024-11-29 | post | no |
| 28 | `focusarchive` | FocUS Archive | focused-ultrasound research | **84** | 2017-09-20 | 2026-08-07 | pre | yes |
| 29 | `coppreprints` | CoP (College of Phlebology) | venous diseases | **48** | 2022-10-24 | 2026-08-04 | pre | yes |
| 30 | `newaddictionsx` | NewAddictionsX | new & emerging addictions | **7** | 2024-08-16 | 2025-11-17 | pre | yes |
| 31 | `acctrt` | Accounting Research & Thought | accounting research | **6** | 2026-03-27 | 2026-06-10 | pre | yes |
| 32 | `livedata` | Research AZ | Arizona institutions | **0** | — | — | none set | no |

**32 rows. Total 200,519 records.**

Derived facts [INF, from S1/S2]:

- **14 providers accept submissions; 18 do not.** The 14 open ones match exactly the count
  COS gave in its August 2025 announcement — "the 14 community-run preprint servers running
  on the OSF Preprints service" (S6) [DOC]. Independent confirmation of a documented figure
  by API measurement; this is as good as evidence gets here.
- COS's own help page *Preprint services hosted by OSF* lists **13** (S8, last updated
  2026-07-23) [DOC] — it omits `acctrt`, which was created 2026-03-27 and has 6 records.
  The help page lags the API. Prefer the API.
- **9 providers have received nothing since 2022** (`agrixiv`, `arabixiv`, `eartharxiv`,
  `ecoevorxiv`, `engrxiv`, `frenxiv`, `inarxiv`, `indiarxiv`, `sportrxiv`) [INF].
- **`livedata` / "Research AZ" is an empty branded shell** — HTTP 200 landing page, zero
  records. A live demonstration of why "N preprint servers exist" is a meaningless statistic
  (§8 negative controls) [API].
- The median provider holds **~300 records**. Wikipedia's ">100" and ">1,000" buckets for
  these servers are technically true and informationally worthless.

### 3.3 Providers that left the platform (content stayed, community went)

Read from each provider's `description` field in the API, 2026-09-01 (S2) [DOC via API]:

| Provider | What the OSF landing page now says | Destination |
|---|---|---|
| engrXiv | "will be closed to new preprint submissions temporarily and moved to https://engrxiv.org/ beginning Wednesday, January 19th" | self-hosted Janeway at `engrxiv.org` |
| EarthArXiv | "is now hosted by the California Digital Library (CDL). The EarthArXiv.org URL now redirects to the CDL Janeway platform. All article DOIs will redirect to CDL" | CDL Janeway |
| EcoEvoRxiv | "Submissions are currently suspended. EcoEvoRxiv.org is moving to the Janeway platform hosted by the California Digital Library (CDL)" | CDL Janeway |
| AgriXiv | "is moving to agriRxiv and is no longer accepting submissions" | `agrirxiv.org` |
| Arabixiv | "has moved to a new address and accepts submissions through its new platform at: zenodo.org/communities/arabixiv" | Zenodo community |
| INA-Rxiv | "With a heavy heart, we close the INArxiv service starting October 7, 2020" | closed outright |
| Frenxiv, IndiaRxiv, LawArXiv, LISSA, MindRxiv, NutriXiv, SportRxiv | "no longer able to accept new submissions. Existing content … will remain accessible as part of COS's ongoing commitment to Open Science" | nowhere — frozen in place |

The last row is the important one. Seven servers share **verbatim identical wind-down
boilerplate**, which tells you the decision was made centrally by COS, not by seven
independent communities. The `latest` dates in §3.2 cluster in **December 2020** for four
of them (`frenxiv` 2020-12-31, `indiarxiv` 2020-12-28, `arabixiv` 2020-12-11) — a single
coordinated cut, not seven separate community deaths [INF].

## 4. The 2025–2026 COS strategy change — verified

This is current and it is the most consequential thing in this record.

**What actually happened, in order:**

1. **2024** — COS introduced preprint moderation across the service. Stated in COS's own
   2025 announcement: "COS introduced preprint moderation in 2024" (S6) [DOC].
2. **2025-08-21** — COS published *"Suspension of Submissions to Generalist Preprint Server
   for Review and Next Steps — Community Servers Hosted by OSF Preprints Remain Active"*
   (S6) [DOC].
3. **2025-08-25** — effective date. Submissions to the **generalist server only** were
   suspended. The help-centre article confirms: "Effective 8/25/2025, we will be temporarily
   suspending submissions to the generalist server hosted on OSF Preprints" (S7) [DOC].
4. **2026-04-21** — the help-centre article's last-updated date. Still described as a
   suspension; **no resumption and no closure has been announced as of 2026-09-01** (S7)
   [DOC]. Thirteen months of "temporary".
5. **2026-06-03** — separately, **Thesis Commons** suspended submissions: "Effective June 3,
   2026, we will suspend submissions to the Thesis Commons paper service. This does not
   affect the other community-run preprint services hosted by OSF Preprints." (S2, provider
   description) [DOC].

**COS's stated reasons** (S6, quoted) [DOC]:

- *Volume and quality*: "The generalist server has seen increasing numbers of suspicious or
  low-quality submissions … trends such as generative AI and paper mills have introduced new
  risks to research integrity. We hypothesize that this server is a particularly attractive
  target for misuse because of its broad acceptance guidelines."
- *Moderation breadth and sustainability*: "moderating a generalist server requires expertise
  across every field of research, a scale beyond our current capacity."
- *Strategic alignment*: "COS is reviewing how the generalist server fits into the long-term
  vision for OSF."

**What was explicitly NOT affected** (S6, S7) [DOC]: existing preprints remain available;
authors can still revise them; the 14 community servers remain open. This is corroborated by
measurement — the generalist server's most recent records are dated 2026-09-01, but of the
100 newest, only 6 have `_v1` GUIDs; the rest are revisions (`_v2` … `_v30`) of preprints
deposited before the cut (S1) [API]. **The API's `latest` date for `osf` is a revision date,
not a submission date.** Anyone reading that column without checking GUID suffixes would
wrongly conclude the generalist server is still accepting work.

**Correcting the framing in the assignment.** The premise that "COS announced it was winding
down or handing off hosting for community preprint servers" is **not what the record shows**.
COS's 2025 announcement says the opposite in its own headline: *"Community Servers Hosted by
OSF Preprints Remain Active"* (S6) [DOC]. What is verifiable is:

- COS suspended **its own** generalist server, and later Thesis Commons.
- Separately and *earlier* (2020–2022), a wave of **communities** left the platform of their
  own accord — engrXiv and EcoEvoRxiv to CDL's Janeway, EarthArXiv to CDL, AgriXiv to
  agriRxiv, Arabixiv to Zenodo (§3.3) [DOC via API].
- Separately again, COS froze a group of small servers with identical boilerplate (§3.3).

Three distinct phenomena over six years, with different causes. Conflating them into "COS is
winding down preprint hosting" would be wrong. The defensible summary is: **the platform is
contracting at both ends — COS shed the hardest-to-moderate service it owned, and the
best-resourced communities took their servers elsewhere — while a stable core of ~14
social-science-flavoured servers continues.** [INF]

**Not verified:** whether COS has an internal end-date for the generalist server; whether
the review announced in August 2025 has concluded; whether any further servers are scheduled
to close. No public document dated after 2026-07-23 was found.

## 5. Screening and moderation — what gets in

**The model.** Each provider independently sets `reviews_workflow` to one of three values,
readable from the API (S2) [API]:

| `reviews_workflow` | Meaning | Providers |
|---|---|---|
| `pre-moderation` | submission sits **private and pending** until a moderator accepts or rejects | 26 of 32 |
| `post-moderation` | appears immediately, may be withdrawn afterwards | 3 — `lissa`, `marxiv`, `nutrixiv` |
| `null` (none set) | no moderation workflow configured | 4 — `osf`, `lawarxiv`, `livedata`, `thesiscommons` |

**How to tell which applies to a given server — the reliable method.** Do not trust the
landing page. Query:

```
https://api.osf.io/v2/preprint_providers/<slug>/
```

and read `data.attributes.reviews_workflow`. This is the value the software actually
enforces. (The deprecated `/v2/preprint_providers/` route still works and is what §3.2 was
built from; the current route is `/v2/providers/preprints/`, which returns the identical
32-item list — verified 2026-09-01, both `meta.total = 32` (S2, S3) [API].)

**The published policy.** COS's help centre states: "Preprint servers are pre-moderation
services, where submissions are in a private, pending state until a moderator accepts or
rejects them. Authors are given notice of reasoning behind any preprints that are rejected."
(S9, last updated 2026-08-14) [DOC]. Note this is a generalisation that the API contradicts
for 6 of 32 providers — another reason to read the API rather than the prose.

**Platform-wide rules** (S9, verbatim) [DOC]:

- "Content completely or mostly generated by large language model (LLM) tools or other
  artificial intelligence (AI) tools is not appropriate for OSF Preprints."
- "Content should be original content created by the user, or posted with explicit
  permission and appropriate attribution of the content creator."
- "Organizations should not use OSF user accounts to act as publication aggregates,
  clearinghouses, or DOI minting services."

The anti-LLM clause is dated — the help page's last-updated stamp is 2026-08-14 — and is
directly downstream of the paper-mill problem that killed the generalist server (§4).

**Provider-specific policies** exist for PsyArXiv, SocArXiv and MetaArXiv and are linked
from S9. SocArXiv's is the most developed: its landing page says "SocArXiv papers are
moderated before appearing. Please read the moderation policy before submitting"
(S2) [DOC].

**What moderation is not.** It is a screen for scope, plausibility, plagiarism and
obvious junk, applied by volunteers from the relevant community. It is not peer review, it
does not check methods, and it does not check numbers. COS says so itself in describing the
generalist server's failure: moderation "requires expertise across every field of research"
and COS did not have it (S6) [DOC].

## 6. Reliability — what you can and cannot trust

**What a deposit here guarantees:**

- A stable OSF GUID and a resolvable URL at `osf.io/preprints/<slug>/<guid>`.
- Usually, but **not always**, a DOI (see below).
- That *a* human looked at it, on 26 of 32 providers.
- Nothing about correctness.

**DOI coverage is materially incomplete, and getting worse.** Measured by full enumeration
and by sampling, 2026-09-01, reading `attributes.preprint_doi_created` (S1) [API]:

| Provider | Records with a minted preprint DOI |
|---|---|
| ECSarXiv (all 323) | 281 (87.0%) |
| LISSA (all 335) | 321 (95.8%) |
| BioHackrXiv (all 173) | 138 (79.8%) |
| Accounting Research & Thought (all 6) | **0** |
| PsyArXiv — 50 oldest | 50/50 |
| PsyArXiv — 50 newest | **0/50** |
| SocArXiv — 50 oldest | 50/50 |
| SocArXiv — 50 newest | **0/50** |
| generalist `osf` — 50 oldest | 50/50 |
| generalist `osf` — 50 newest | **0/50** |
| engrXiv — 50 oldest **and** 50 newest | **0/50 and 0/50** |

Two separate effects, and they should not be confused:

1. **Recent records have no DOI yet.** Every "50 newest" sample returned zero. Spot check:
   ECSarXiv preprint `nbjcm_v1`, deposited 2026-08-22, published 2026-08-23,
   `reviews_state: accepted`, `is_published: true` — and
   `https://api.osf.io/v2/preprints/nbjcm/identifiers/` returns `{"data": []}`. **A live,
   accepted, published OSF preprint with no identifier of any kind** (S1) [API]. Whether
   this is a minting backlog or a policy change is **[NOT-VERIFIED]** — I found no COS
   statement either way. Either reading is bad for citation durability.
2. **engrXiv never had OSF DOIs at all**, at either end of its life — consistent with its
   DOIs having been minted and now redirected elsewhere, as EarthArXiv's landing page
   explicitly says happened for that server (§3.3) [INF].

**Practical rule: do not assume an OSF preprint has a DOI. Check
`/v2/preprints/<guid>/identifiers/` before you cite one, and if it is empty, cite the GUID
URL and archive the PDF yourself.**

**Known failure modes:**

- **Paper-mill and LLM-generated content on the generalist server.** Not a rumour — COS
  named it as the reason for suspension (S6) [DOC]. Any generalist-server preprint deposited
  before 2025-08-25 comes from a corpus its own operator judged to be under sustained
  abuse.
- **Fringe physics and metaphysics.** Visible in the raw feed: the newest generalist-server
  records on 2026-09-01 include "The Ontological Origin of the Universe and Maximal
  Existence" (`ms7rp_v2`), "The Single Pole Battery: a Relativistic Understanding …"
  (`skphf_v8`, on its **eighth** revision) and "CMB, Cosmological Redshift, and Wien's Law"
  (`qa4sz_v3`) (S1) [API]. These are revisions, so the suspension does not stop them
  accumulating.
- **Revision churn as a signal.** `_v8`, `_v21`, `_v28`, `_v30` suffixes appear in the
  newest-100 sample of the generalist server (S1) [API]. A preprint on its thirtieth version
  with no journal outcome is not a manuscript under improvement.
- **Community abandonment.** Nine providers have taken nothing since 2022 (§3.2). Their
  moderator pools are gone; nobody is watching the content that is already there.

**How to sanity-check an individual OSF preprint:**

1. `GET https://api.osf.io/v2/preprints/<guid>/` — check `provider` (which community?),
   `reviews_state` (should be `accepted`), `is_published`.
2. `GET .../identifiers/` — is there a DOI at all?
3. Check the provider's `reviews_workflow` (§5). `null` or `post-moderation` means nothing
   necessarily blocked it.
4. Check `original_publication_date` / `custom_publication_citation` — if populated, the
   work exists elsewhere and you should cite that.
5. Check the GUID suffix. `_v1` is an original deposit; `_v14` is something else.

**Eventual-publication rate: [NOT-VERIFIED].** I found no measurement of OSF-Preprints
publication rates in the time available. Do not assume the arXiv or bioRxiv figures
transfer.

## 7. Computing and engineering relevance — very little, and say so

**There is almost nothing here for a hardware or software engineer.** Concretely:

- **ECSarXiv** (`ecsarxiv`, 323 records, still open) — electrochemistry and solid-state
  science, run in association with The Electrochemical Society. Battery, fuel-cell,
  electrodeposition and semiconductor-materials work. The single OSF provider with genuine
  electronics-adjacent content. It has its own record in this collection
  ([ecsarxiv.md](ecsarxiv.md)); this record supplies the platform context.
- **engrXiv** (`engrxiv`, 2,033 records, **frozen since 2022-01-19**) — the Engineering
  Archive. The OSF-hosted archive is a historical snapshot; the live service moved to
  `engrxiv.org` on Janeway. See [engrxiv.md](engrxiv.md).
- **BioHackrXiv** (`biohackrxiv`, 173 records, open) — biohackathon project reports.
  Bioinformatics tooling, workflow languages, data-format work. Software, but life-science
  software. See [biohackrxiv.md](biohackrxiv.md).
- **MetaArXiv** (`metaarxiv`, 1,014 records, open) — reproducibility and research
  transparency, run by the Berkeley Initiative for Transparency in the Social Sciences.
  Occasionally relevant to research-software engineering practice.
- **LISSA** (`lissa`, 335 records, frozen) — library and information science; information
  retrieval and repository software at the margins. Covered in
  [library-science-and-cognitive-archives.md](library-science-and-cognitive-archives.md).

That is the whole of it: **2,356 records across ECSarXiv and engrXiv, 1.2% of the
platform**, and 86% of that is a frozen archive [INF, from S1].

The generalist server does receive occasional engineering-flavoured deposits — the ECSarXiv
example above, `nbjcm`, is a solar-PV/BESS/EVSE sizing framework citing NEC 690.7, IEEE
Std 485 and NREL PVWatts (S1) [API] — but these are isolated, unmoderated-by-domain-experts,
and now cut off at the source.

**If you are looking for computing preprints, this is the wrong platform.** Use arXiv
(`cs.*`, `eess.*`), the [Cryptology ePrint Archive](cryptology-eprint-archive.md), or
[TechRxiv](techrxiv.md).

**No landmark-papers table.** OSF Preprints does not host foundational work in software,
distributed systems, databases, electronics or security. I could not identify a single
paper in these areas that appeared on OSF Preprints first and became significant. Stating
that plainly is more useful than padding a table.

## 8. Access, APIs and bulk retrieval

**The REST API is the reason this record has real numbers.** It is public, unauthenticated
for reads, JSON:API-formatted, and it was not rate-limited during roughly 200 sequential
requests on 2026-09-01.

| Endpoint | Purpose | Verified 2026-09-01 |
|---|---|---|
| `https://api.osf.io/v2/providers/preprints/?page[size]=100` | current provider list | 200, `meta.total = 32` (S3) [API] |
| `https://api.osf.io/v2/preprint_providers/?page[size]=100` | **deprecated** provider list | 200, `meta.total = 32`, warns "This route is deprecated and will be unavailable after version 2.7" (S2) [API] |
| `https://api.osf.io/v2/preprints/?filter[provider]=<slug>&page[size]=1` | per-provider count in `links.meta.total` | 200 for all 32 (S1) [API] |
| `https://api.osf.io/v2/preprints/?filter[provider]=<slug>&sort=date_created` | oldest first | 200 (S1) [API] |
| `https://api.osf.io/v2/preprints/<guid>/identifiers/` | DOI, if any | 200, `data: []` when none (S1) [API] |
| `https://api.osf.io/v2/preprint_providers/<slug>/licenses/` | permitted licences | 200 (S1) [API] |
| `https://api.osf.io/v2/search/preprints/?q=…` | — | **404** — does not exist (S1) [API] |

Square brackets must be percent-encoded or curl must be given `-g`; unencoded `[` produces
`curl: (3) bad range in position …`, which is a client error, not a server response.

**Negative controls — read this before trusting any OSF probe.**

| Probe | Result | Lesson |
|---|---|---|
| `https://osf.io/preprints/` | HTTP 200, **4,207 bytes** | the SPA shell |
| `https://osf.io/preprints/ecsarxiv` (real) | HTTP 200, **4,207 bytes** | identical to the shell |
| `https://osf.io/preprints/notarealslugxyzzy999` (bogus) | HTTP 200, **4,207 bytes** | **byte-identical to the real provider — web URLs cannot distinguish a real provider from a fake one.** Directly verified here, 2026-09-01 (S1) [WEB] |
| `https://api.osf.io/v2/preprints/?filter[provider]=notarealprovider999` | HTTP **200**, body 127 bytes, `{"data":[],"links":{"meta":{"total":0}}}` | **an invalid provider slug returns a clean zero, indistinguishable from a genuinely empty provider** |
| `https://help.osf.io/article/999999-this-does-not-exist-xyzzy` | HTTP **404**, 15,028 bytes | the help centre, at least, 404s honestly |

The middle two are the trap. `livedata` returns `total: 0` and so does `notarealprovider999`.
The **only** way to know a slug is real is that it appears in the provider list (S2/S3) —
which is why §3.2 was built from the provider list first and counts second, not the other
way round.

**OAI-PMH:** OSF does not advertise an OAI-PMH endpoint for preprints. **[NOT-VERIFIED]** —
I did not exhaustively probe candidate paths.

**SHARE / trove.** `https://share.osf.io/` returns HTTP 200 and is alive, but is no longer
the preprint aggregator it was. It now serves a linked-data "trove" index-card search
(`/trove/index-card-search`, `/trove/browse`, `/trove/docs`) returning JSON-LD; a filtered
query for `resourceType=Preprint` returned `totalResultCount: {"@id":
"trove:ten-thousands-and-more"}` — a *bucketed* answer, not a number (S4) [API]. The old
faceted discovery UI is gone: `https://osf.io/preprints/discover` now **302s to
`https://osf.io/search?q=&resourceType=Preprint`** (S1) [WEB], OSF's own search, scoped to
OSF's own content. Note that every Wikipedia citation for OSF-hosted server sizes points at
`osf.io/preprints/<slug>/discover` URLs (S10) — **those URLs no longer resolve to what the
citation claims they showed.**

**Bulk:** no dump. Paginate at `page[size]=100` (the maximum honoured); full enumeration of a
300-record provider takes 4 requests and a couple of seconds.

## 9. Licensing and reuse

`https://api.osf.io/v2/preprint_providers/osf/licenses/` returns `meta.total = 2`
(S1, 2026-09-01) [API]:

- **CC-BY 4.0**
- **CC0 1.0**

Two options, both open, author's choice, no all-rights-reserved default. This is materially
better than SSRN (see [ssrn.md](ssrn.md)) and better than most commercial hosts. Note that
the licence list is *per provider* — the endpoint above is for the generalist server; a
given community server may offer a different set, so query the endpoint for the slug you
care about.

Text and data mining of the API is not blocked and is evidently tolerated (§8).

## 10. Caveats and controversies

1. **The Wikipedia numbers do not survive contact with the API — and the conflict is
   structural, not a typo.** Wikipedia's list gives OSF Preprints ">1,000,000", with the
   prose "Aggregates over 30 preprint servers (all from COS plus other like arXiv, bioRxiv,
   etc.). Number of native OSF Preprints documents: 25,114." (S10) [WEB]. Unpacking that:

   - **(a) Natively deposited on COS-hosted providers: 200,519 records** across 32
     providers, 2026-09-01 (S1) [API]. This is the only number in the vicinity that is both
     meaningful and measurable.
   - **(b) Merely indexed/harvested from elsewhere:** the ">1,000,000" figure came from the
     **SHARE-backed `osf.io/preprints/discover` search**, which used to federate metadata
     from arXiv, bioRxiv, PeerJ, Preprints.org, RePEc and Cogprints alongside OSF's own
     content. The evidence that this is what the number meant is still in the API: the
     deprecated `/v2/preprint_providers/` route returns a `meta.whitelisted_providers` array
     containing exactly **`["arXiv", "bioRxiv", "Preprints.org", "PeerJ", "Cogprints",
     "Research Papers in Economics"]`** (S2) [API] — six external sources, harvested, never
     hosted. **Those records were never on OSF.** A million-strong "OSF Preprints" was
     always mostly arXiv wearing an OSF search box.
   - **(c) "Over 30 preprint servers"** is coincidentally close to right for the wrong
     reason: there are **32 COS-hosted providers** (S2) [API], not "30 servers including
     arXiv and bioRxiv". Wikipedia conflates the hosted set with the harvested set.
   - **(d) "25,114 native documents"** is undated in the source and I could not reproduce it
     from any current endpoint. It is plausibly a snapshot of the generalist `osf` provider
     alone circa 2020–2021 (now 78,195) [INF, NOT-VERIFIED].
   - **Conclusion, stated plainly:** the ">1,000,000" and the "25,114" are not two views of
     the same thing and neither is currently true. The defensible 2026 figure is **200,519
     records natively hosted across 32 COS providers**, of which 70.6% sit in two of them,
     and 18 of which are closed. I am recording the conflict rather than resolving it in
     Wikipedia's favour; the harvested-vs-hosted distinction is the actual finding.

2. **Wikipedia lists the same infrastructure ~25 times.** Reading the list, OSF-hosted
   servers look like two dozen independent institutions. They are one Django application.
   Diversity of logos is not diversity of infrastructure, and the correlated-failure risk is
   exactly as bad as it sounds — §4 shows two services closing on one operator's decision.

3. **Vanity-domain rot.** `engrxiv.org`, `eartharxiv.org`, `arabixiv.org`, `psyarxiv.com`
   and others are community-controlled, not COS-controlled. When a community leaves, the
   domain leaves with it and the OSF content stays behind. **A link to a vanity domain and a
   link to `osf.io/preprints/<slug>` can point at different corpora.** Always record the
   `osf.io` GUID.

4. **Wikipedia's own citations are dead URLs.** Every OSF-server size claim in the list cites
   `osf.io/preprints/<slug>/discover` (S10); those paths now redirect to a generic OSF search
   (§8). The citations cannot be checked as written.

5. **The generalist server is a corpus under acknowledged abuse.** COS says so (S6). Treat
   pre-2025 generalist-server deposits accordingly, and note that revisions to them continue
   to appear with 2026 dates.

6. **DOI minting has stopped, or stalled, on recent deposits** (§6). Unexplained, and it is
   the single most citation-relevant thing on this page.

7. **The API route you are using is deprecated.** `/v2/preprint_providers/` warns it "will be
   unavailable after version 2.7" (S2) [API]. Scripts built on it — including the one that
   produced §3.2 — will break. `/v2/providers/preprints/` is the replacement and returns the
   same 32 (S3) [API].

## 11. Sources

- **S1** — OSF REST API v2, `https://api.osf.io/v2/preprints/` with `filter[provider]`,
  `sort`, `page[size]` parameters; plus `/v2/preprints/<guid>/identifiers/`,
  `/v2/preprint_providers/osf/licenses/`. Retrieved 2026-09-01. Supports: all counts,
  earliest/latest dates, DOI coverage, version-inflation measurements, licence list,
  negative controls, the `osf.io/preprints/discover` redirect.
- **S2** — `https://api.osf.io/v2/preprint_providers/?page[size]=100`. Retrieved 2026-09-01.
  `meta.total = 32`. Supports: the provider list, display names, descriptions,
  `reviews_workflow`, `allow_submissions`, the deprecation warning, and the
  `meta.whitelisted_providers` array naming the six externally harvested sources.
- **S3** — `https://api.osf.io/v2/providers/preprints/?page[size]=100` (current route).
  Retrieved 2026-09-01. `meta.total = 32`. Corroborates S2.
- **S4** — `https://share.osf.io/` and
  `https://share.osf.io/trove/index-card-search?cardSearchFilter[resourceType]=Preprint`.
  Retrieved 2026-09-01. Supports: SHARE's survival as "trove" and its bucketed result count.
- **S5** — `https://www.cos.io/products/osf-preprints`. Retrieved 2026-09-01 (HTTP 200,
  62,612 bytes). Supports: "OSF Preprints is open source infrastructure for communities to
  advance open scholarship dissemination. It is built using the core OSF platform"; the
  stated goal to "Provide a single search interface to access preprints and papers from
  many disciplinary services"; and "Contact us for more information about setting up an OSF
  Preprint service." [DOC]
- **S6** — Center for Open Science blog, *"Suspension of Submissions to Generalist Preprint
  Server for Review and Next Steps — Community Servers Hosted by OSF Preprints Remain
  Active"*, dated **August 21st, 2025**.
  `https://www.cos.io/blog/suspension-of-submissions-to-generalist-preprint-server-for-review-and-next-steps-community-servers-hosted-by-osf-preprints-remain-active`
  Retrieved 2026-09-01. Supports: the 2025-08-25 effective date, the two-part architecture,
  the "14 community-run preprint servers" figure, the paper-mill/LLM reasoning, the 2024
  introduction of moderation, and the service's 2016 origin.
- **S7** — OSF Support, *"OSF Preprints Generalist Server Suspension"*,
  `https://help.osf.io/category/689-osf-preprints-generalist-server-suspension`. Retrieved
  2026-09-01; page states "Last updated on April 21, 2026". Supports: the suspension's
  status as of 2026 and the "existing preprints remain available / authors can revise"
  guarantee.
- **S8** — OSF Support, *"Preprint services hosted by OSF"*,
  `https://help.osf.io/article/686-preprint-services`. Retrieved 2026-09-01; page states
  "Last updated on July 23, 2026". Supports: the 13-service list and its divergence from
  the API's 14.
- **S9** — OSF Support, *"Preprint moderation policies"*,
  `https://help.osf.io/category/693-preprint-moderation-policies`. Retrieved 2026-09-01;
  "Last updated on August 14, 2026". Supports: the pre-moderation statement, the anti-LLM
  clause, the anti-aggregator clause, provider-specific policy links.
- **S10** — Wikipedia, *List of preprint repositories*, wikitext via
  `https://en.wikipedia.org/w/index.php?title=List_of_preprint_repositories&action=raw`.
  Retrieved 2026-09-01. Supports: the ">1,000,000" / "over 30 preprint servers" / "25,114
  native documents" claims, the 2017 launch year, and the `…/discover` citation URLs.
- **S11** — Negative control: `https://help.osf.io/article/999999-this-does-not-exist-xyzzy`
  → HTTP 404, 15,028 bytes. Retrieved 2026-09-01.
