# ECSarXiv — preprint repository record

- **URL:** https://ecsarxiv.org/ (302 → `https://osf.io/preprints/ecsarxiv/`)
- **Operator:** **The Electrochemical Society (ECS)**, a non-profit scholarly society
  ("more than 8,000 individual members and 48,000 other constituents"), as part of its
  *Free the Science* open-access programme (S1). Hosted on the **Center for Open Science's
  Open Science Framework (OSF) Preprints** platform (S1, S2). Free to submit, free to read.
- **Discipline scope:** "a free preprint service for **electrochemistry and solid state
  science and technology**" (S2, provider `description` field). That second half is the part
  hardware people miss — it covers semiconductor processing, dielectrics, deposition and
  device work, not just wet chemistry (§2).
- **Launched:** earliest deposit **2018-05-11** (S3). ECS's own announcement date is
  **[NOT-VERIFIED]** — the About page carries no launch date.
- **Status:** active but **very small and flat** — ~20–27 deposits/year since 2021 (§3).
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What it is

ECSarXiv is the Electrochemical Society's preprint server. ECS's own framing is worth
quoting because it explains why a society this size bothered: "ECS is a very broad and
diverse community, and has needs that are different from those using preprint services such
as arXiv, bioRxiv, ChemArxiv" — the goal was "faster, more relevant search results for the
field" (S1). It is deliberately cheap to run: ECS did not build a platform, it took a
white-labelled OSF Preprints instance, which it says "has made our service
cost-effective… and provides a robust search interface across other scholarly resources"
(S1).

For someone building embedded hardware, ECSarXiv matters for one reason: **ECS's remit is
the chemistry and physics underneath your components**. The Society's divisions include
Battery, Corrosion, Electrodeposition, Dielectric Science and Technology, Electronics and
Photonics, Luminescence and Display Materials, and Sensor (S1). Its two flagship journals
are the *Journal of The Electrochemical Society* and the *ECS Journal of Solid State
Science and Technology*. ECSarXiv is the preprint front-end to that world: cell ageing,
impedance spectroscopy, electrodeposition, wafer processing, gas and glucose sensors, MEMS.

It is, however, **tiny** — 323 deposits in eight years (§3). Set your expectations
accordingly: this is a place to find a specific well-made document, not a corpus to survey.

## 2. Scope and subject taxonomy

Two taxonomies apply, and they differ.

**(a) ECS's own Topical Interest Areas**, the editorially meaningful list, used across all
ECS publications (S1):

Batteries and Energy Storage · Carbon Nanostructures and Devices · Corrosion Science and
Technology · **Dielectric Science and Materials** · Electrochemical/Electroless Deposition ·
Electrochemical Engineering · **Electronic Materials and Processing** · **Electronic and
Photonic Devices and Systems** · Fuel Cells, Electrolyzers, and Energy Conversion ·
Luminescence and Display Materials, Devices, and Processing · Organic and
Bioelectrochemistry · Physical and Analytical Electrochemistry, Electrocatalysis, and
Photoelectrochemistry · **Sensors**

**(b) The OSF subject tree**, which is what the API actually returns: **270 subject terms**
(S4). It is the standard OSF/bepress tree with an ECS-specific graft, and the graft is where
the hardware relevance lives. Selected leaves, verbatim (S4):

- under **Electronic Materials and Processing**: `2D Materials`, `Atomic Layer Deposition`,
  `Atomic Layer Etching`, `Barrier Layers`, `Chemical Etching`, `Chemical Vapor Deposition`,
  `Cleaning`, `Electronic Devices and Semiconductor Manufacturing`,
  `Group II-VI Semiconductors`, `Group III-V Semiconductors`, `Group IV Semiconductors`,
  `High-k Dielectrics`, `Interconnects`, `Low-k Dielectrics`
- under **Materials Science and Engineering**: `Aqueous Batteries`,
  `Batteries and Energy Storage`, `Ceramic Materials`, `Coatings`, `Corrosion`,
  `Dielectric Science and Materials`, `Electrochemical Capacitors`, `Electrodeposition`,
  `Electroless Deposition`, `Films`, `Flow Batteries`, `LeClanche Batteries`,
  `Lead Acid Batteries`, `Lithium Batteries`, `Metal Carbides`, `NiCd Batteries`,
  `NiMH Batteries`, `Oxides`, `Polymer Fuel Cells`, `Semiconductor and Optical Materials`,
  `Solid Oxide Fuel Cells`
- under **Electrical and Computer Engineering**: `Electronic and Photonic Devices and
  Systems`, `Power and Energy`, `Signal Processing`, `Systems and Communications`,
  **`VLSI and Circuits, Embedded and Hardware Systems`**
- under **Energy**: `Electrolyzers`, `Energy Efficient Electronic Devices`, `Fuel Cells`,
  `Solar Cells`
- under **Physics**: `Plasma Deposition`, `Plasma Etching`, `Plasma Polymerization`,
  `Luminescence and Display Materials and Processing`, `Condensed Matter Physics`
- under **Chemistry**: `Electroanalytical`, `Electrocatalysis`, `Electrodes`,
  `Electrolytes`, `Interfaces`, `Nitrides`, `Semiconductors`, `Sensors`, `Sulfides`,
  `Carbides`
- under **Nanoscience and Nanotechnology**: `Nanofabrication`,
  `Nanocharacterization: Electron Microscopy / Optical Microscopy / Surface Probe Microscopy`,
  `Plasmonics`, `Carbon Nanostructures and Devices`

**Actual subject usage** across all 323 deposits (multi-label; counts are term assignments,
S3):

| Term | Uses | | Term | Uses |
|---|---|---|---|---|
| Engineering | 461 | | Batteries and Energy Storage | 30 |
| Physical Sciences and Mathematics | 218 | | Other Electrochemical Engineering | 24 |
| Chemistry | 143 | | Materials Chemistry | 20 |
| Materials Science and Engineering | 106 | | Mechanical Engineering | 17 |
| Electrochemical Engineering | 105 | | Electronic Materials and Processing | 13 |
| Electrochemistry | 56 | | Electrodes / Electrocatalysis / Corrosion | 13 each |
| Chemical Engineering | 56 | | Nanoscience and Nanotechnology | 12 |
| Energy | 51 | | Electrolyzers | 10 |
| Mathematical Modeling | 35 | | Electrical and Electronics | 10 |
| Physics | 32 | | Sensors / Energy Systems / Fuel Cells | 8 each |
| Electrical and Computer Engineering | 31 | | Polymer Fuel Cells | 8 |

The honest read: batteries, electrochemical engineering and modelling dominate;
semiconductor-processing terms exist in the taxonomy but are lightly used
(`Electronic Materials and Processing`, 13 uses).

## 3. Size and growth

| Measure | Value | Date | Source |
|---|---|---|---|
| OSF JSON:API `links.meta.total` for `filter[provider]=ecsarxiv` | **323** | 2026-09-01 | [API] S3 |
| Records actually harvested by paging that endpoint | **323** (matches) | 2026-09-01 | [API] S3 |
| Records carrying a journal DOI in the `doi` field | **25** (7.7%) | 2026-09-01 | [API] S3 |
| OpenAlex source `ECSarXiv (OSF Preprints)` `works_count` | **17** | 2026-09-01 | [API] S6 |

The OpenAlex figure (17) conflicts violently with the operator's own registry (323). Record
both; **use the OSF API number.** As with engrXiv, OpenAlex has essentially not indexed this
server (S6).

**Deposits by year of publication** (S3):

| 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (to 09-01) |
|---|---|---|---|---|---|---|---|---|
| 31 | 66 | 74 | 23 | 42 | 20 | 20 | 20 | 27 |

This is the shape of a server that launched with society enthusiasm (2018–2020, including
batches of ECS meeting slide decks — several titles literally begin "(ECS 236th)" or
"235th ECS Meeting:", S3), then settled into a trickle of ~20/year. It has not grown, and it
has **not** been hit by the generative-AI submission wave that engrXiv reports — the 2026
partial-year figure of 27 is the highest since 2020, but from a base so small the number is
noise [INF].

**323 deposits is the whole thing.** For context, that is about one twentieth of engrXiv and
about 0.5% of arXiv's `cond-mat` output. Absence from ECSarXiv means nothing whatsoever.

Note also that ECSarXiv accepts **non-article content by policy** — "articles, slide
presentations, datasets, software, etc." (S1) — so the 323 is not 323 papers. Several are
conference slide decks and at least one is a software announcement (§5).

## 4. Screening and moderation — what gets in

**Pre-moderation.** The OSF provider record reports `reviews_workflow: pre-moderation` and
`allow_submissions: true` (S2). ECS's published posting policy states the gate precisely
(S1, verbatim, emphasis original to the source):

> - Preprints may be articles, slide presentations, datasets, software, etc.
> - **PREPRINTS MAY NOT BE ARTICLES THAT HAVE ALREADY BEEN PUBLISHED IN ANY PEER-REVIEWED
>   JOURNAL.**
> - Preprints undergo a screening process to reject offensive and/or nonscientific content
>   and/or content not relevant to the fields ECS covers.
> - Preprints are not peer-reviewed, edited, or typeset before being posted online.
> - Preprints must be in English.
> - Authors must have sufficient rights to post any material submitted to ECSarXiv.
> - Authors may submit a revised version of a preprint to ECSarXiv at any time (prior to
>   publication in a journal).
> - **No endorsement of a preprint's methods, assumptions, conclusions, or scientific
>   quality by ECS is implied by its appearance in ECSarXiv.**

So the gate is: relevance + not-offensive + not-already-published + English. There is no
quality check, no endorsement requirement, no affiliation requirement. Elsewhere the About
page describes it as "quick moderation" (S1). **Who performs the screening, and the
turnaround time, are [NOT-VERIFIED]** — ECS names an Advisory Board section on the page but
the OSF `advisory_board` field is empty (S2).

ECS also gives concrete, correct advice about the ecosystem: "Always check the policies of
the journals where you plan to submit… Some journals allow the author to submit subsequent
revised preprints after submitting to journals, some do not" (S1).

## 5. Reliability — what you can and cannot trust

**A deposit guarantees:** a DOI (ECS states this explicitly — "preprints in ECSarXiv carry a
DOI", S1), a timestamp, a version chain, an explicit licence, and that a human confirmed the
work is in-scope and not obviously nonsense. Nothing more, and ECS says so ("no endorsement…
is implied").

**Publication linkage is weak.** Only **25 of 323** records carry a journal DOI in the OSF
`doi` field (S3). Where they point is informative: `10.1149/...` (ECS's own journals, via
IOP) and `10.1149/MA...` (ECS Meeting Abstracts) dominate, with occasional
`10.1016/j.jpowsour...`, `10.1021/acsaem...` and one `10.1109/TCST...`. This is a **floor,
not a rate** — the field is author-populated and mostly left blank [INF]. Treat "no journal
DOI" as "unknown", not "unpublished".

**Known failure modes.** (a) A meaningful fraction of the corpus is **conference slide
decks and posters**, not manuscripts — useful, but not a paper, and easy to mis-cite.
(b) Because the corpus is so small and quiet, **stale content is normal**: a 2019 preprint
with no journal DOI has probably been published somewhere without the record being updated.
(c) There is no peer review of any kind, in a field where a single mis-specified impedance
model or an unreported C-rate makes results meaningless. (d) Duplicate/versioned entries
appear in listings (e.g. `rfwug_v1` and `rfwug_v5` both surface as separate dated records,
S3) — deduplicate on the base GUID.

**How to sanity-check an ECSarXiv item.** Read the `is_published` and
`original_publication_date` attributes from the API; search the title in the ECS Digital
Library and Crossref for a journal version; and for battery/impedance work, check the
document actually reports cell chemistry, temperature, C-rate and cycle count — the ECS
community's own reviewers would.

## 6. What you actually find there — and why an embedded engineer should care

Every item below was confirmed present in the 2026-09-01 API harvest, with its OSF GUID
(resolve as `https://osf.io/<guid>/`) (S3).

**Battery modelling and ageing — the strongest cluster on the server:**

- **PyBaMM — *Python Battery Mathematical Modelling*** — `67ckj`, 2020-02-07. The
  announcement of what is now a widely used open-source battery simulation package. If you
  are writing a BMS state estimator, this is the single most directly useful item on
  ECSarXiv.
- *Nonlinear electrochemical impedance spectroscopy of lithium-ion batteries: Experimental
  approach, analysis…* — `t635x`, 2018-06-25. This is the item ECS itself designates as its
  `example` preprint in the provider record (S2).
- *One law to rule them all: Stretched exponential master curve of capacity fade for Li-ion
  batteries* — `zxkbu`, 2019-02-14.
- *Review and performance comparison of mechanical-chemical degradation models for
  lithium-ion batteries* — `zdwsu`, 2019-05-28.
- *Lithium Plating Detection Methods in Lithium-ion Batteries* — `bj9gr`, 2020-08-17.
- *Reversible and Irreversible Expansion of Lithium-ion Batteries Under a Wide Range of
  Stress Factors* — `f79ey`, 2021-08-24 — directly relevant to pack mechanical design.
- *Investigation and modeling of cyclic aging using a design of experiment with automotive
  grade lithium-ion cells* — `vdajp`, 2021-09-22 → `10.1016/j.jpowsour.2021.230952`.
- *A Composite Single Particle Lithium-ion Battery Model through System Identification* —
  `ynufg`, 2019-12-03 → `10.1109/TCST.2020.3047776` (*IEEE Trans. Control Systems
  Technology*) — the clearest preprint→IEEE path on this server.
- *Battery Lifecycle Framework: A Flexible Repository and Visualization Tool for Battery
  Data* — `h7c24`, 2021-03-13.
- *Extending a Multi-physics Li-ion Battery Model from Normal Operation to Short Circuit and
  Venting* — `j6xmv`, 2024-05-26 — thermal-runaway-adjacent.
- *Relevance of classical models/approaches for Battery Digital Twins* — `sxtjw`, 2025-07-19.

**Sensors and MEMS:**

- *Distributed Bridge Circuit for High-Temperature Silicon MEMS Pressure Sensors* — `rfwug`,
  2026-08-06 (revised to `v5`, 2026-08-22). Piezoresistive bridge design — genuinely a
  circuits paper.
- *Enhancing Potentiometric Response of Electrochemical Sensor Using Modified Ion-Sensitive
  Transistor* — `7bukj`, 2019-03-15. ISFET work.
- *Functional Iron Oxide (Fe₂O₃) Nanoparticles Based Gas Sensor Operating at High
  Temperature* — `s9ykg`, 2019-05-29.
- *Determination of the working temperature of the MOS sensors used for the detection of
  ethanol and methanol* — `qmt78`, 2021-06-03. Metal-oxide gas sensor heater calibration.
- *Facile Sensors for Humidity Measurement of Indoor Environment* — `ruwb6`, 2023-01-31;
  *Temperature Sensing of Indoor Environment Using Resistive and Capacitive Sensors* —
  `9teu3`, 2023-02-06.
- *Cost-effective 316L-based glucose sensor architectures* — `zaygq`, 2025-06-13.

**Semiconductor and interconnect processing:**

- *On the roughness analysis of high-index silicon wafers using KOH-IPA solutions* — `d2a6z`,
  2020-08-17. Bulk-micromachining etch chemistry.
- *Homogeneous backside porosification of standard silicon wafers for post-fab process
  integration of porous silicon* — `sfyux`, 2025-05-20.
- *(ECS PRiME 2020) High TEC copper to connect copper bond pads for low temperature wafer
  bonding* — `ns3kf`, 2020-08-28. 3D-integration / hybrid bonding.
- *Examination of Reducing Agents Used for Aluminum Electroless Deposition* — `xsuja`,
  2020-08-17.
- *NaCl-Assisted Chemical Vapor Deposition of Monolayer MoS₂: A Review* — `r4hj6`, 2026-05-14.
- *A study on corrosion resistance of electroplated Gold over Nanocrystalline Ni-W for
  contact applications* — `s5pgz`, 2019-03-15 — connector/contact plating reliability.
- *Comparative evaluation of corrosion effects between nanocrystalline silver alloy and
  traditional gold stack* — `hnpwe`, 2019-03-15.

**Supercapacitors:**

- *High Energy-Density Supercapacitor, Enabled by Carbon Nanostructures* — `b3ec4`, 2020-08-12.
- *Electrochemical Study of the Effect of Prussian Blue as a Mediator in a Solid-state
  Supercapacitor* — `3wnbh`, 2020-08-12.
- *Simultaneous Electrochemical Exfoliation and Chemical Functionalization of Graphene for
  Supercapacitor Electrodes* — `ycbj8`, 2020-05-05.
- *Next Generation Transparent Supercapacitor Materials* (poster) — `pg9y7`, 2019-10-11.
- *Perovskite and Polymer Composites for High-Performance Supercapacitor Electrodes: A
  Review* — `wrpt7`, 2025-10-12.

**Instrumentation and measurement technique** — the category most likely to save you time:

- *Use and misuse of electrochemical impedance spectroscopy in PEFC research* — `hr6nf`,
  2019-11-05.
- *Rapid analytical instrumentation for electrochemical impedance spectroscopy measurements*
  — `w94xh`, 2019-12-03.
- *Real-Time Under Load Electrochemical Impedance Spectroscopy (EIS) Analysis and Modeling* —
  `chmwk`, 2020-08-12.
- *Respirometric In-Situ Methods for Real-Time Monitoring of Corrosion Rates*, Parts I and II
  — `t69j3` (2019-11-22 → `10.1149/1945-7111/ab6c61`) and `g3vaz` (2020-12-01).

## 7. Landmark papers

**ECSarXiv hosts no field-defining papers in software, distributed systems, databases,
electronics or security.** The closest thing to a landmark artifact is the **PyBaMM**
announcement (`67ckj`, §6), which is significant as *software* rather than as a paper. Cited
impact across the server is negligible — ECSarXiv is a small society service, not a priority
venue. Table deleted.

## 8. Access, APIs and bulk retrieval

**Use the OSF JSON:API. Do not scrape osf.io HTML.**

```bash
# total count
curl 'https://api.osf.io/v2/preprints/?filter%5Bprovider%5D=ecsarxiv&meta%5B%5D=total'
# full harvest (page through links.next)
curl 'https://api.osf.io/v2/preprints/?filter%5Bprovider%5D=ecsarxiv&page%5Bsize%5D=100'
# provider metadata: name, description, reviews_workflow, domain, example
curl 'https://api.osf.io/v2/providers/preprints/ecsarxiv/'
# 270-term subject tree
curl 'https://api.osf.io/v2/providers/preprints/ecsarxiv/subjects/?page%5Bsize%5D=100'
```

The whole corpus paged out in seconds; no rate limiting was hit; no user-agent substitution
was needed. Square brackets in the query string **must be percent-encoded** or `curl` fails
with "bad range in position" (S3).

### Negative control — and it is an important one

**`https://osf.io/preprints/zzzznotreal/` returns HTTP 200 with 4,207 bytes — byte-for-byte
the same length as the real `https://osf.io/preprints/ecsarxiv/` page** (S5). osf.io is an
Angular single-page application: *every* path returns the same 200 shell, and the router
decides afterwards whether the content exists. The same applies to `https://osf.io/oai` and
`https://osf.io/oai/?verb=Identify`, which return `Content-Type: text/html` and the SPA
shell rather than an OAI-PMH response (S5).

**Consequences:** (1) on osf.io, HTTP 200 carries **zero** information; (2) `ecsarxiv.org`
resolving with a 200 proves nothing about the archive existing; (3) there is **no working
OAI-PMH endpoint** found for ECSarXiv — `[NOT-VERIFIED]` whether one exists elsewhere.

By contrast the **API** behaves correctly: `https://api.osf.io/v2/providers/preprints/zzzznotreal/`
returns **404, 61 bytes** (S5). That is the discriminator to build tooling on.

**Redirect chain:** `https://ecsarxiv.org/` → 200 at `https://osf.io/preprints/ecsarxiv/`
(S5). Cite OSF GUIDs (`https://osf.io/<guid>/`) or DOIs, never the `ecsarxiv.org` vanity
domain, which is a redirect that ECS could retire.

**Crossref** is a viable secondary route for the 25 items with journal DOIs, but ECSarXiv's
own preprint DOIs are OSF-issued and not consistently exposed in the JSON:API `doi` field
(that field holds the *journal* DOI). Extracting preprint DOIs requires following each
record's `preprint_doi` relationship — not attempted in this pass, **[NOT-VERIFIED]**.

## 9. Licensing and reuse

Authors choose from the OSF licence list. Distribution across all 323 deposits (S3, licence
IDs resolved via `https://api.osf.io/v2/licenses/<id>/`):

| Licence | Records |
|---|---|
| CC BY 4.0 | 180 |
| CC BY-NC-ND 4.0 | 56 |
| GNU LGPL 3.0 | 44 |
| CC BY-SA 4.0 | 14 |
| CC0 1.0 | 14 |
| others (CC BY-NC, MIT, …) | ~15 |

Two things worth flagging. **CC BY is a bare majority (56%), not the norm** — 17% is
CC BY-NC-ND, which forbids derivative works, so you cannot legally re-plot someone's ageing
curves from those. And **44 records are licensed LGPL-3.0**, which is a software licence: a
direct consequence of ECS's policy of accepting software and datasets as first-class
deposits (§4). Check the licence per item; do not assume.

ECS publishes a dedicated "Licensing" section on the About page (S1). Text and data mining
of the metadata via the OSF API is unrestricted in practice.

## 10. Caveats and controversies

- **Size is the dominant caveat.** 323 items. Nothing you fail to find here tells you
  anything.
- **Growth has flatlined** at ~20/year since 2021 (§3). A society preprint server with this
  little traffic is a candidate for quiet discontinuation; archive anything you rely on.
- **It is not a hardware-design venue.** It is a *materials and electrochemistry* venue
  whose output happens to constrain hardware. You will find why your cell fades, not how to
  lay out the BMS.
- **osf.io's 200-for-everything behaviour** (§8) has burned automated pipelines before;
  it is the single most important operational fact in this record.
- **Mixed content types** — slide decks, posters, datasets, software — are policy, not
  accident (§4). Cite accordingly.
- **The "no previously published articles" rule** (§4) means ECSarXiv is *not* a green-OA
  route for already-published ECS papers, unlike engrXiv which explicitly accepts those.
- **OpenAlex records 17 works against a true 323** (§3).
- **ECS's launch announcement and the identity of its moderators are not documented here**
  — [NOT-VERIFIED].

## 11. Sources

- **S1** — `https://www.electrochem.org/ecsarxiv` — ECS's own "About ECSarXiv" page,
  including *Why another preprint service?*, *Benefits of ECSarXiv*, *Technical areas covered
  by ECSarXiv* (the 13 Topical Interest Areas), *Posting policy* (quoted verbatim in §4), and
  *Definition of ECSarXiv preprints*. Also the ECS divisional list. Retrieved 2026-09-01
  (browser UA required; the site returns full HTML). **[DOC]**
- **S2** — OSF JSON:API provider record,
  `https://api.osf.io/v2/providers/preprints/ecsarxiv/` — `name: ECSarXiv`;
  `description: "a free preprint service for electrochemistry and solid state science and
  technology"`; `domain: https://ecsarxiv.org/`; `reviews_workflow: pre-moderation`;
  `allow_submissions: true`; `example: t635x`; `email_support: support+ecsarxiv@osf.io`;
  `advisory_board` empty. Retrieved 2026-09-01. **[API]**
- **S3** — OSF JSON:API preprint harvest,
  `https://api.osf.io/v2/preprints/?filter[provider]=ecsarxiv&meta[]=total&page[size]=100`,
  paged to completion (323 records; dumped to scratch as `osf_ecsarxiv.json`), plus
  `https://api.osf.io/v2/licenses/<id>/` lookups. Retrieved 2026-09-01. **[API]** — supports
  the total, the per-year table, the subject-usage table, the licence table, the
  journal-DOI count, and every example title/GUID/date in §6.
- **S4** — OSF JSON:API subject tree,
  `https://api.osf.io/v2/providers/preprints/ecsarxiv/subjects/?page[size]=100`, paged to
  completion (270 terms). Retrieved 2026-09-01. **[API]**
- **S5** — Live HTTP probes, 2026-09-01: `https://ecsarxiv.org/` (200, 4,207 B, redirected to
  `https://osf.io/preprints/ecsarxiv/`); `https://osf.io/preprints/ecsarxiv/discover` (200,
  4,207 B); **negative control** `https://osf.io/preprints/zzzznotreal/` (**200, 4,207 B**);
  **API negative control** `https://api.osf.io/v2/providers/preprints/zzzznotreal/` (**404,
  61 B**); `https://osf.io/oai?verb=Identify` and `https://osf.io/oai/?verb=Identify` (200,
  `text/html`, SPA shell). **[WEB]**
- **S6** — `https://api.openalex.org/sources?filter=display_name.search:ecsarxiv` →
  `https://openalex.org/S4306402531`, `ECSarXiv (OSF Preprints)`, `works_count: 17`.
  Retrieved 2026-09-01. **[API]**
