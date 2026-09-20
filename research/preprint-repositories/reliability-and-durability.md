# Reliability and durability — a cross-server assessment

The two questions worth asking about any preprint server, answered comparatively:

1. **What does a deposit here actually guarantee?** (reliability)
2. **Will the link still resolve in five years?** (durability)

- **Compiled:** 2026-09-01 / 2026-09-02 from the 29 records in this directory.
- Evidence labels as defined in [`README.md`](README.md#evidence-and-method).
- **Nothing here is a judgement of any individual paper.** These are properties of *servers*.

---

## 1. Reliability is a question about the gate, not about the badge

Every server on the Wikipedia list describes itself in roughly the same language. They differ
enormously in what actually happens to a submission. Sorting by the **gate** rather than by the
marketing is the single most useful thing in this survey.

| Gate type | Servers | What a deposit proves |
|---|---|---|
| **Endorsement + subject moderation** | [arXiv](arxiv.md) | An endorsed author, a plausible subject fit, and a permanent timestamp. **Not** correctness |
| **Named editorial screening** | [Cryptology ePrint](cryptology-eprint-archive.md) (4 published criteria, 3 named editors) · [Optimization Online](optimization-online.md) (coordinators; explicitly instructed to reject work that "should not be obviously crazy or wrong (e.g. P=NP papers)") | Relevance and non-obvious-crackpottery. Both operators **explicitly disclaim** verifying anything further |
| **Staff screening against published criteria** | [bioRxiv/medRxiv](biorxiv-and-medrxiv.md) (incl. dual-use/biosecurity) · [Preprints.org](preprints-org.md) (24 h screen with an explicit pseudoscience filter) | Non-scientific content, plagiarism and harm were checked for. Not the science |
| **Pre-moderation** | [BioHackrXiv](biohackrxiv.md) (`reviews_workflow: pre-moderation`; 172 accepted / 1 withdrawn) | A human looked before it went live |
| **Completeness / scope moderation** | [HAL](hal.md) · [ChinaXiv](chinaxiv.md) (four automated checks + admin review, incl. an explicit **political-content** criterion stated by the operator) | Metadata and institutional fit. Note the ChinaXiv criterion is *not* a scientific one |
| **Affiliation or funder gate** | Wellcome / Gates / HRB / AMRC / Open Research Africa ([life-sciences record](life-science-and-medical-platforms.md)) | The author is funded by the sponsor. That is all |
| **Journal-submission gate** | [Research Square](research-square.md) *In Review* · ARPHA · Beilstein · JMIR | A named journal accepted it **for review**. Nothing about the verdict |
| **Post-hoc open review** | [F1000Research](life-science-and-medical-platforms.md) · [Qeios](qeios.md) · [ScienceOpen](scienceopen.md) | Read the reviews themselves; the label means little |
| **None whatsoever** | [Zenodo](zenodo.md) · [figshare](figshare.md) · [viXra](vixra.md) | A DOI and a timestamp. Zenodo and figshare are honest about this; **viXra is too** — see below |

### The two honest extremes

**Zenodo** accepts anything and says so. That is a *feature* — it is a general-purpose archive, not
a preprint server, and treating a Zenodo DOI as a quality signal is a category error made by the
citer, not by CERN.

**viXra** is more candid than most of the platforms above it. Its own text: *"acceptance in viXra
may not confer scientific credibility"* and *"viXra may contains some work of low value or
usefulness."* It has no endorsement, no correctness review, no DOIs, no licence and no dark archive.
**Do not cite viXra as evidence for anything.** The only defensible uses are a priority timestamp
and studying viXra itself.

---

## 2. Measured outcomes, where they exist

Almost no server publishes what fraction of its deposits are eventually peer-reviewed. Two figures
in this pass are real measurements rather than claims.

| Server | Cohort | Publication rate | Method |
|---|---|---|---|
| **bioRxiv** | 2016 week | **77.8%** (n=108) | API `published` field, deduped by DOI |
| **bioRxiv** | 2018 week | **71.1%** (n=467) | as above |
| **bioRxiv** | 2019 week | **69.1%** (n=661) | as above |
| **bioRxiv** | 2020 week | **71.9%** (n=1,137) | as above |
| **medRxiv** | Oct 2019 | **79.9%** (n=189) | as above |
| **medRxiv** | 2020 week | **64.5%** (n=575) | as above |
| **Cryptology ePrint** | 2017 | **61.7%** (95% Wilson CI 49.0–72.9%, n=60) | systematic sample; a **lower bound**, since the field is author-maintained |

bioRxiv's 69–78% for mature cohorts agrees with the operator's own "75%" claim and with Abdill &
Blekhman (*eLife* 2019). Recent cohorts (2022: 58.9%, 2024: 50.7%, 2025: 47.3%) are **censored, not
declining** — they have not had time to publish.

For **arXiv, OSF Preprints, SSRN, TechRxiv, engrXiv, ECSarXiv, ChinaXiv, Preprints.org and Research
Square** the rate is **[NOT-VERIFIED]** — no citable measurement was found. Preprints.org claims
58.44% "converted to peer-reviewed article" but publishes no method and we found no independent
replication.

A useful negative result on arXiv: **only 6 of the 79 verified landmark papers carry a `journal_ref`
at all.** In machine learning the arXiv document is frequently the permanent version of record, and
absence of venue metadata is therefore *not* evidence of low quality — it is the field's norm.

---

## 3. The AI-slop inflection, 2025

Three independent operators changed policy in the same window, which is worth reading as one event
rather than three.

- **arXiv, October 2025** — surveys and position papers in `cs.*` must now **complete peer review
  before** arXiv will accept them, documented with a DOI or journal reference. Verified and quoted
  in [arXiv §4](arxiv.md). A January 2026 tightening also removed institutional email as sufficient
  grounds for endorsement.
- **Center for Open Science, 2025-08-25** — closed its **generalist** OSF Preprints server to new
  submissions, citing *"suspicious or low-quality submissions … generative AI and paper mills"*.
  Still suspended as of 2026-04-21. Thesis Commons separately suspended 2026-06-03. Note that COS's
  own headline was *"Community Servers Hosted by OSF Preprints Remain Active"* — the community
  servers were **not** wound down.
- **engrXiv, 2025** — the only operator in this survey to publish a rejection rate: submissions rose
  from 60 to 200/month and **roughly half of 2025 submissions were declined**. Their figure
  cross-checks exactly against the registry (1,151 posted in 2025 vs their "nearly 1200").

**Implication.** A deposit dated before ~2024 was screened under a materially weaker filter for
machine-generated text than one dated after. That cuts both ways: older deposits predate the flood,
newer ones passed a stricter gate.

---

## 4. Commercial entanglement — three cases to disclose when citing

Not accusations. Structural facts a reader should know.

**[Preprints.org](preprints-org.md) is operated by MDPI.** MDPI's contested standing concerns
*journal peer review at scale* — special-issue volume, and Clarivate's February 2023 delisting of
IJERPH and JRFM. That does **not** transfer cleanly to a server which makes no peer-review claim,
and MDPI's rebuttals had teeth (the Oviedo-García paper drew an Expression of Concern and a
Correction). What *does* transfer is the funnel: **230 of the 232 "Preprints Friendly Journals" are
MDPI titles.**

**[Research Square](research-square.md) is wholly owned by Springer Nature**, auto-posts manuscripts
from 1,503 Springer Nature/BMC journals via *In Review*, and sells the same authors AJE editing
services. **This ownership is stated nowhere on the preprint site.** The critical mechanic: **on
rejection the preprint stays but the journal branding and review timeline are stripped**, so an
unbranded Research Square preprint is indistinguishable from a rejected one.

**[SSRN](ssrn.md) is owned by Elsevier** (acquired 2016). In 2016–2017 SSRN removed papers over
copyright claims — documented from Inside Higher Ed, including the verbatim revision comment and
Gordon's "about 20 papers". A commercial host can and did delete deposits. Contrast with
[Cryptology ePrint](cryptology-eprint-archive.md), where reports are never removed, and arXiv, where
withdrawal creates a *new version* and prior versions including full text remain accessible
permanently (`deletedRecord=persistent` in OAI-PMH).

---

## 5. Durability — the headline result

**Preprint servers do not lose data. They lose front doors.**

Of eighteen closed, frozen or migrated servers probed in this pass, **seventeen still serve their
corpus**. Full table in [`closed-and-defunct-servers.md`](closed-and-defunct-servers.md); the
representative cases:

| Server | Fate | Retrievable 2026-09-02? |
|---|---|---|
| **Nature Precedings** (2007–2012) | Publisher discontinued it; `precedings.nature.com` refuses TCP | **Yes, incl. full text** at `nature.com/npre`; a `10.1038/npre.*` DOI resolves 200 |
| **CogPrints** (1997–2017) | Founder retired; HTTPS fails on a cert **SAN mismatch** | **Yes** — over plain HTTP it 301s to a Southampton static archive. A preservation *success* presenting as a failure |
| **mp_arc** (Jul 1991 – Dec 2023) | Closed deliberately, with a published preservation promise | **Yes — the best-preserved dead archive measured.** Its 1991 PostScript file still carries a **gzip mtime of 1997-04-26** and downloads intact |
| **INArxiv** (2017–2020) | Closed; successor `rinarxiv.lipi.go.id` serves a self-signed `CN=linux` default | **Yes — 15,987 preprints** via the OSF API |
| **PeerJ Preprints** (2013–2019) | Stopped accepting deposits | **Yes** via DOI; direct fetches 403 on all five UAs |
| **agriRxiv** | **Domain is a Namecheap parking page** | **Yes** — service migrated OSF → CABI Digital Library; DOIs resolve |
| **Eyexiv** (2022) | Four TLDs NXDOMAIN; not an OSF provider | **No.** The only genuinely lost entry on the list |

Six of eleven platforms in the life-sciences group had a discontinuity. **DOIs survived every one of
them. Hostnames survived none.**

### The TLS signal, and its limit

An expired or never-issued certificate is a **high-precision** abandonment signal. Verified:
`africarxiv.ubuntunet.net` expired 2026-07-25; `latarxiv.org` expired 2026-08-20 19:26:19;
`rinarxiv.lipi.go.id` runs a self-signed `CN=linux` default from 2023.

**But the converse is false.** `bodoarxiv.org` (now an **online-casino page**), `lawarxiv.org` (a
114-byte parking stub), `mediarxiv.org` (redirects to an unrelated site) and `frenxiv.org` (frozen
since October 2020) all hold **fresh, auto-renewed certificates**. Parking services run ACME too.
In this dataset, **TLS automation outlived editorial staffing in every divergent case.** A valid
certificate proves nothing.

Worse, COS's own live provider description for BodoArXiv still directs readers to the casino domain.

### What actually breaks

| Failure mode | Example | Content lost? |
|---|---|---|
| Grant expiry / founder retirement | CogPrints, LISSA | No |
| Publisher strategy change | Nature Precedings, PeerJ Preprints | No |
| Platform migration breaking URL grammar | TechRxiv (figshare → Authorea, Dec 2023); ChemRxiv (figshare → Cambridge Open Engage → **a third platform, Jan 2026**) | No — DOIs held |
| Self-hosted successor never configured | INArxiv → rinarxiv, AfricArXiv → ubuntunet | No — original survived on OSF |
| Domain lapse to a squatter | BodoArXiv, agriRxiv, LawArXiv | No |
| Everything at once | **Eyexiv** | **Yes** |

---

## 6. Practical rules

**Citing.**
1. **Cite the DOI or the server-native identifier, never the URL.** DOIs survived every
   discontinuity measured here; hostnames survived almost none.
2. **On Zenodo, cite the *version* DOI, not the concept DOI** — the concept DOI silently moves to
   the next release.
3. **Check whether the preprint was later published.** bioRxiv/medRxiv expose this in the API;
   ePrint carries a publication-info string; arXiv has `journal_ref` (but absence proves nothing —
   see §2).
4. **Disclose operator entanglement** when citing Preprints.org, Research Square or SSRN.
5. **Never cite viXra as evidence.**

**Depositing.**
1. Prefer a server with a **named dark archive**. Preprints.org states Portico. **We found no
   Portico/CLOCKSS/LOCKSS statement for ScienceOpen, Qeios, viXra, mp_arc, Rutgers Optimality
   Archive, LingBuzz or any OSF provider** — recorded as unverified, not as "none".
2. **Mirror to Zenodo.** It is CERN-backed, versioned, never deletes, and is the closest thing to a
   durability floor available.
3. **Submit valuable, hard-to-find URLs to `web.archive.org/save/`** — consistent with this
   repository's [existing archival practice](../../AGENTS.md).
4. For research **software**, the deposit that matters is the Zenodo/GitHub release DOI, not a
   paper.

**Judging an unfamiliar server, in order.**
1. Find its gate in §1. If you cannot determine the gate, treat it as "none".
2. Check whether it mints DOIs and with which registrar (Crossref `posted-content`, DataCite).
   [Synthical](synthical.md) is registered with **neither** — it hosts nothing.
3. Compare its *hosted* count with its *advertised* count. ScienceOpen advertises ~100 M and hosts
   ~3,584; OSF's ">1,000,000" was federated metadata.
4. Probe a **bogus path**. If it returns 200, no status-code check on that host means anything —
   see [`README.md § Probing traps`](README.md#6-probing-traps).
5. Check the operator's most recent deposit date, not its launch date.

---

## 7. Ranked summary

Combining gate strength, measured outcomes, technical relevance and durability. **Reliability here
means "how much does a deposit tell you", not "how good is the science".**

| Tier | Servers | Rationale |
|---|---|---|
| **Use with confidence** | [arXiv](arxiv.md) · [Cryptology ePrint](cryptology-eprint-archive.md) · [HAL](hal.md) · [bioRxiv/medRxiv](biorxiv-and-medrxiv.md) | Real gates, institutional backing, permanent versioning, measured or structurally sound outcomes. In their fields the deposit is frequently the version of record |
| **Use, with the operator disclosed** | [Zenodo](zenodo.md) · [TechRxiv](techrxiv.md) · [ChemRxiv](chemrxiv.md) · [Optimization Online](optimization-online.md) · [ECSarXiv](ecsarxiv.md) · [engrXiv](engrxiv.md) · [BioHackrXiv](biohackrxiv.md) · [SSRN](ssrn.md) | Sound but each has a specific caveat — no review (Zenodo), commercial owner (SSRN, TechRxiv), tiny corpus (ECSarXiv), or a restrictive licence (Optimization Online: **download for personal use only, no CC licence at all**) |
| **Verify independently before relying** | [Preprints.org](preprints-org.md) · [Research Square](research-square.md) · [ChinaXiv](chinaxiv.md) · [figshare](figshare.md) · [OSF providers](osf-preprints.md) · [Qeios](qeios.md) | Usable for discovery. The gate is weak, absent, or measures something other than quality |
| **Discovery only — hosts little or nothing** | [ScienceOpen](scienceopen.md) · [Synthical](synthical.md) · [RePEc](repec-and-econstor.md) | Index or aggregation layers. RePEc is explicit that it stores nothing; Synthical mints nothing |
| **Do not cite as evidence** | [viXra](vixra.md) | No gate of any kind, by design and by the operator's own statement |
| **Durability risk regardless of content** | [Authorea](authorea.md) (submissions suspended May 2026) · [ScienceOpen](scienceopen.md) (no preservation arrangement found) · the frozen [regional servers](regional-and-national-servers.md) · [Eyexiv](natural-sciences-and-niche-servers.md) (lost) | Cite the DOI, and archive a copy yourself |
