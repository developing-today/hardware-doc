# ChemRxiv — preprint repository record

- **URL:** https://chemrxiv.org/ · article URLs `https://chemrxiv.org/doi/full/<DOI>`
- **Operator:** owned by the **American Chemical Society (ACS)** and operated as a
  multi-society partnership. Crossref lists every deposit under the prefix `10.26434` with
  publisher **"American Chemical Society (ACS)"** (S1) [API]. Partner co-owners, verified
  only to 2019: **Royal Society of Chemistry** (joined 2018), **Gesellschaft Deutscher
  Chemiker / German Chemical Society**, and the **Chinese Chemical Society** and
  **Chemical Society of Japan** (both 2019) (S2) [COM/LIT].
- **Discipline scope:** all of chemistry, plus the large chemistry/materials/computational
  overlap (§3).
- **Launched:** announced 2016, opened **2017**; earliest Crossref-registered deposits
  **2017**, 173 that year (S1, S2) · **Status:** **active**, ~10,000 preprints/year, and
  **on its third platform in nine years** (§2).
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).
- **Access warning:** `chemrxiv.org` returned **HTTP 403 with a Cloudflare
  `cf-mitigated: challenge` interstitial to every user-agent tried** on 2026-09-01
  (default `curl`, Chrome, WhatsApp, ChatGPT-User) — see §9. **Everything below that is
  labelled [API] comes from Crossref, not from ChemRxiv**, and the [WEB] items come from
  the Internet Archive.

## 1. What it is

ChemRxiv is chemistry's answer to arXiv and bioRxiv: a free, non-profit-society-run
preprint server, launched by ACS in 2017 after a 2016 announcement. Its name is
pronounced "chem-archive"; the X is a chi (S2). Unlike bioRxiv it was born inside a
publisher — the largest chemistry publisher in the world — and its early history is
largely the story of that publisher's own journals deciding whether they would accept
preprinted manuscripts. *Angewandte Chemie* said yes in March 2018; **JACS not until
August 2018** (S2) [COM]. That reluctance is why ChemRxiv's first-year volume was tiny
(173 deposits in 2017) and why it took until 2020 to pass 5,000/year.

It is now firmly established: **53,678 distinct preprints** through 2026-09-01, growing
~10,000/year (§4). For this knowledge base it is the single most relevant *chemistry*
server, because chemistry is where your materials come from — see §7.

## 2. Platform history — three platforms in nine years

This is the most consequential operational fact about ChemRxiv and it is not in
Wikipedia. The DOI grammar under prefix `10.26434` changes cleanly at each migration,
which makes the history verifiable from Crossref alone (S1) [API]:

| Era | DOI pattern | Example (verified) | Platform |
|---|---|---|---|
| 2017 – mid-2021 | `10.26434/chemrxiv.<numeric>.v<N>` | `10.26434/chemrxiv.6406505.v1` (2018-06) | **figshare** (Digital Science) |
| mid-2021 – 2025 | `10.26434/chemrxiv-<year>-<slug>[-v<N>]` | `10.26434/chemrxiv-2024-glhqn` (2024-06) | **Cambridge Open Engage** (Cambridge University Press) |
| 2026 – | `10.26434/chemrxiv.<numeric>/v<N>` | `10.26434/chemrxiv.15004130/v1` (2026-06) | **new platform**, provider not stated (§9) |

**figshare → Cambridge Open Engage.** A Wayback capture of `https://chemrxiv.org/` from
**2021-02-10** still carries `<meta name="application-name" content="figshare">` and
loads its assets from `figstatic.com`, with the title "ChemRxiv: the Preprint Server for
Chemistry" (S3) [WEB]. Article URLs of that era were figshare's
`chemrxiv.org/articles/<slug>/<numeric-id>` (S4). The first `chemrxiv.org/engage/…`
captures are from 2021, and the Wayback capture index for
`chemrxiv.org/engage/chemrxiv/public-dashboard` begins **2021-06-20** (S5). So the move
to Cambridge Open Engage happened **between February and June 2021**; I could not pin an
exact announcement date — **[NOT-VERIFIED]**.

**Cambridge Open Engage → new platform, January 2026.** The last useful capture of the
Engage-era dashboard, **2026-01-21**, is titled "Homepage | ChemRxiv | **Cambridge Open
Engage**" and carries a site notice reading: *"ChemRxiv is no longer accepting new
submissions or versions as we process our queue and prepare to transfer all content to
our new platform on January 21. New submissions will be welcome on the new site when it
launches."* (S6) [WEB]. Three independent signals confirm the migration actually
happened:

1. The DOI grammar changes on schedule — every 2026-posted DOI uses the new
   `chemrxiv.<numeric>/v<N>` form, and **all 6,579 `/v1` and 1,725 `/v2+` DOIs in the
   corpus are 2026 records** (S1) [API].
2. `chemrxiv.org/engage/chemrxiv/public-dashboard` returns **403** in the Wayback index
   from 2026-03-21 onward (S5).
3. **Every** ChemRxiv DOI — figshare-era, Engage-era and new — now has Crossref
   `resource.primary.URL` of the form `https://chemrxiv.org/doi/full/<DOI>` (S7) [API].
   The whole corpus was re-pointed at a single new URL grammar.

**[INF] on who the new provider is:** `/doi/full/<DOI>` is the URL grammar of **Atypon
Literatum**, and it is exactly what ACS uses on `pubs.acs.org/doi/full/10.1021/…`. That,
plus the Cloudflare posture, is consistent with ChemRxiv having been moved onto ACS's own
publishing platform. **This is an inference from URL shape, not a statement from the
operator, and I could not confirm it** — the site is unreachable (§9). Treat as
**[NOT-VERIFIED]**.

**Why it matters.** Two full-corpus migrations in five years, with the DOI *suffix
grammar changing each time*, is a real durability signal. The DOIs do still resolve — that
is the point of DOIs, and ChemRxiv has done it correctly — but any local cache of
ChemRxiv landing-page URLs built before 2026 is now stale, and any scraper written
against the Engage `public-api` is dead.

## 3. Scope and subject taxonomy

Seventeen categories, with article counts as displayed on the ChemRxiv dashboard on
**2026-01-21** (S6) [WEB]. Unlike bioRxiv, **categories are multi-select** — these sum to
70,544 assignments over 36,917 items shown live, ~1.9 categories each [INF]:

| Category | Articles | Category | Articles |
|---|---|---|---|
| **Theoretical and Computational Chemistry** | 10,411 | **Nanoscience** | 3,033 |
| Organic Chemistry | 8,519 | **Energy** | 2,755 |
| **Physical Chemistry** | 7,401 | **Polymer Science** | 2,358 |
| **Catalysis** | 6,373 | **Chemical Engineering and Industrial Chemistry** | 1,944 |
| Biological and Medicinal Chemistry | 6,072 | Organometallic Chemistry | 1,858 |
| **Materials Science** | 5,627 | Earth, Space, and Environmental Chemistry | 1,241 |
| **Materials Chemistry** | 4,957 | Chemical Education | 476 |
| **Inorganic Chemistry** | 3,856 | Agriculture and Food Chemistry | 396 |
| **Analytical Chemistry** | 3,267 | | |

The bolded categories are the ones a hardware person should care about. **Theoretical and
Computational Chemistry is the single largest category on the server** — ChemRxiv is, in
practice, a major venue for computational-methods and machine-learning-for-chemistry work.

## 4. Size and growth

Derived by paginating **every** Crossref record under prefix `10.26434` on **2026-09-01**
(S1) [API]; script and log in
`scratch/preprint-repositories/lifesci/chemrxiv-crossref-scan.txt`.

- **Total registered DOIs: 55,403.** All of type `posted-content` / subtype `preprint`.
- Of those, **1,725 are version-2-or-higher DOIs**, all posted in 2026 (the new platform
  registers each version separately; the two earlier platforms did not).
- **Distinct preprints: 53,678.**

| Year posted | DOIs | Distinct preprints |
|---|---|---|
| 2017 | 173 | 173 |
| 2018 | 1,088 | 1,088 |
| 2019 | 2,873 | 2,873 |
| 2020 | 4,985 | 4,985 |
| 2021 | 5,240 | 5,240 |
| 2022 | 6,029 | 6,029 |
| 2023 | 7,277 | 7,277 |
| 2024 | 8,824 | 8,824 |
| 2025 | 10,085 | 10,085 |
| 2026 (to 09-01) | 8,829 | 7,104 |

Growth is steady and monotonic since 2019 — no COVID whipsaw of the kind bioRxiv shows,
and no flattening.

**Recorded conflict.** The ChemRxiv dashboard on **2026-01-21** advertised **"36,917 Live
Content"**, alongside 75,455,050 abstract views, 29,462,885 content downloads and 12,460
citations (S6) [WEB]. Crossref's cumulative count at end-2025 is **46,574**. The two do
not reconcile. Possible explanations [INF]: the dashboard counter was stale (openRxiv's
is, see the sibling record); or "Live Content" excludes withdrawn/removed items and
items whose full text never posted; or the metric was scoped differently. I cannot
resolve it because the live site is unreachable. **Report both, dated.**

Wikipedia's figures are stale and much smaller ("more than 1,000 submissions in the first
eighteen months"; "2,314 in 2019", the latter attributed to Coudert 2020) (S2). Note the
Wikipedia/Coudert 2019 figure of 2,314 is close to but below Crossref's 2,873 for 2019 —
plausibly a submissions-vs-postings or cut-off-date difference.

## 5. Screening and moderation

**Poorly verified, and I want to be explicit about that.** ChemRxiv's policy pages are
behind the Cloudflare challenge (§9) and the Wayback captures I could reach are dashboard
pages, not policy pages.

What is directly attested (S6) [WEB], from the site's own standing notices:

- "Content on ChemRxiv is early research and has not been peer reviewed prior to posting."
- "These are preliminary reports which have not been peer-reviewed. They should not be
  regarded as conclusive, guide clinical practice/health related behaviour, or be reported
  in news media as established information."

The presence of a moderation queue is attested indirectly: the January 2026 migration
notice speaks of "process[ing] our queue", and an older standing notice warns that
"during the holiday season, submission processing times may increase slightly. We will
review all submissions as quickly as possible" (S6) — i.e. human screening with a
turnaround, not instant posting.

Contemporary reporting during COVID-19 describes ChemRxiv among the preprint servers that
tightened screening against low-quality coronavirus submissions (Kwon, *Nature* 581:130–131,
2020, `10.1038/d41586-020-01394-6`) (S8) [COM/LIT] — but I did not retrieve that article's
text, so the specifics of ChemRxiv's screen are **[NOT-VERIFIED]**.

**Do not assume ChemRxiv screening is comparable to bioRxiv's**, which is documented in
detail. It may be; I could not check.

## 6. Reliability — what you can and cannot trust

A ChemRxiv deposit guarantees a Crossref DOI, a timestamp, a version history, and that
*someone* looked at it before posting. It does not guarantee peer review, and the server
says so on every page.

- **Eventual-publication rate: not measured.** Unlike bioRxiv/medRxiv, ChemRxiv exposes no
  machine-readable preprint→publication link, and I found no study measuring it. This is
  the single biggest gap relative to the sibling
  [bioRxiv/medRxiv record](biorxiv-and-medrxiv.md).
- **Checking an individual preprint:** resolve the DOI via Crossref
  (`https://api.crossref.org/works/<doi>`) to confirm it is a real registered deposit and
  read `posted`, `license` and `resource.primary.URL`. Then search Crossref for the same
  title as a `journal-article` to see whether it was ever published — you must do manually
  what the bioRxiv API does for you.
- **Version count is visible in the DOI suffix** on both the figshare-era (`.vN`) and
  post-2026 (`/vN`) records, and often on Engage-era ones (`-vN`). A `-v3` or `/v4` is a
  paper that has been reworked; a bare v1 from 2019 has not.
- **ACS ownership is a structural conflict worth naming.** The server is owned by the
  largest commercial-scale chemistry publisher, whose journals are the most likely
  destination for the content. Nothing observed suggests misuse, but it is a materially
  different governance position from openRxiv's independent non-profit or arXiv's
  university host. The multi-society partnership (RSC, GDCh, CCS, CSJ) exists partly to
  answer exactly that objection (S2).

## 7. Why an electronics or hardware person should care

Chemistry is upstream of every component you buy. ChemRxiv is where the pre-review version
of that work appears. Concrete examples, **each verified as a real ChemRxiv deposit via
Crossref** (DOI, posted date) (S9) [API]:

**Semiconductor process chemistry and photoresists**

- *Synthesis of End-Cap Enabled Self-Immolative Photoresists for Extreme Ultraviolet
  Lithography* — `10.26434/chemrxiv-2022-1ps85`, 2022-07-04
- *Extreme Ultraviolet and Beyond Extreme Ultraviolet Lithography using Amorphous Zeolitic
  Imidazolate frameworks* — `10.26434/chemrxiv-2025-s1n4s`, 2025-06-18
- *On the limitations of thermal atomic layer deposition of InN using ammonia* —
  `10.26434/chemrxiv-2022-s9dvr`, 2022-12-06
- *In0.5Ga0.5N Layers by Atomic Layer Deposition* — `10.26434/chemrxiv.14671575.v1`,
  2021-05-25
- *Opportunities and Challenges of Machine Learning in Atomic Layer Deposition* —
  `10.26434/chemrxiv-2025-v35x7`, 2025-12-10
- *Chemical Vapor Deposition of Uniform and Large-Scale MoS2 Using Heterogeneous
  Precursors* — `10.26434/chemrxiv-2025-tz2gv`, 2025-10-08

**Batteries and electrolytes**

- *Reactive molecular dynamics simulations of Lithium-ion battery electrolyte degradation*
  — `10.26434/chemrxiv-2024-bd6mh`, 2024-04-29
- *Lithium-Ion Battery Electrolyte Structural Transport Mechanism: Attempt Frequencies and
  Activation Free energies* — `10.26434/chemrxiv.15004288/v1`, 2026-06-04 (v2 2026-07-16)
- *Synergistic Effects of Solid Electrolyte Mild Sintering and Lithium Surface Passivation*
  — `10.26434/chemrxiv-2025-cdks6`, 2025-09-29 (v2 2025-12-16)
- *High-Throughput Ionic Conductivity Trend Predictions of Lithium Argyrodites and Garnets
  as Solid State electrolytes* — `10.26434/chemrxiv.15006536/v1`, 2026-07-24

**Conductive polymers, displays and photovoltaics**

- *Transparent conductive PEDOT–graphene films from large-flake graphite* —
  `10.26434/chemrxiv-2024-rbc36`, 2024-10-03
- *Efficient Orange Organic Light-Emitting Diodes Employing a Central Aniline Bridged
  Multiresonant TADF emitter* — `10.26434/chemrxiv-2023-wk0nc`, 2023-12-07
- *Understanding the full zoo of perovskite solar cell impedance spectra with the standard
  drift-diffusion model* — `10.26434/chemrxiv-2024-rfv0n`, 2024-02-04

**Analytical instrumentation and lab automation** — the `Analytical Chemistry` (3,267) and
`Chemical Engineering` (1,944) categories carry spectrometer, chromatography and detector
methodology, and increasingly robotics:

- *A Self-Driving Lab for Nano- and Advanced Materials Synthesis* —
  `10.26434/chemrxiv-2024-f13l1`, 2024-12-08
- *Human–Robot Collaborative Reaction Development with a Self-Driving Laboratory* —
  `10.26434/chemrxiv.15008166/v1`, 2026-09-01
- *New Self-supporting Polymer Thin Film for Nanoparticle Analysis in STEM/TEM* —
  `10.26434/chemrxiv-2025-50x35`, 2025-07-29

If you want one sentence: **ChemRxiv is where EUV resist chemistry, ALD precursor
chemistry, electrolyte formulation and TADF emitter design show up six to eighteen months
before the ACS/RSC/Wiley paper.**

## 8. Boundary with ECSarXiv

There is a real overlap with **[ECSarXiv](ecsarxiv.md)**, the Electrochemical Society's
OSF-hosted server, and the boundary is worth stating because you will otherwise miss half
the literature:

| | ChemRxiv | [ECSarXiv](ecsarxiv.md) |
|---|---|---|
| Size | 53,678 preprints (§4) | ~323 deposits total |
| Owner | ACS + partner societies | The Electrochemical Society |
| Platform | own/Atypon-style (2026–) | OSF Preprints (white-label) |
| Centre of mass | synthesis, computation, materials chemistry | electrochemistry + **solid state science and technology** |
| Overlap | batteries, electrolytes, electrodeposition, corrosion, sensors | same |

ChemRxiv is ~165× larger and is where almost all of the battery- and
materials-chemistry volume actually goes. ECSarXiv is worth checking anyway for two
reasons: ECS's remit explicitly includes *Dielectric Science and Materials*, *Electronic
Materials and Processing* and *Electronic and Photonic Devices and Systems*, which
ChemRxiv's taxonomy does not name; and ECSarXiv content is on OSF, so it is trivially
machine-accessible while ChemRxiv currently is not (§9). **Search both; expect ChemRxiv
to have 99 % of the hits and ECSarXiv to occasionally have the device-oriented one.**

## 9. Access, APIs and bulk retrieval

**The live site is not machine-accessible as of 2026-09-01.** Probe results:

| Probe | UA | Result |
|---|---|---|
| `https://chemrxiv.org/` | `curl/8.5.0` | **403**, 5,360 B |
| `https://chemrxiv.org/` | Chrome 131 | **403**, 5,595 B |
| `https://chemrxiv.org/` | `WhatsApp/2.23.20.0` | **403**, 5,381 B |
| `https://chemrxiv.org/` | `ChatGPT-User/1.0` | **403**, 5,616 B |
| `https://chemrxiv.org/engage/chemrxiv/public-api/v1/items?limit=1` | Chrome 131 | **403**, 5,803 B |

Response headers show `server: cloudflare`, **`cf-mitigated: challenge`**, and a
`Just a moment…` JS-challenge body. This is a browser-integrity challenge, not an
IP block and not a robots policy. Per house rules I am recording this as a retrieval
observation only; it says nothing about whether a normal browser can read the site, and I
did not attempt to defeat it. **A sibling agent reached the same result independently.**

**The Engage-era public API existed** at
`https://chemrxiv.org/engage/chemrxiv/public-api/v1/items` — the Wayback Machine holds a
**HTTP 200, 14,978-byte** JSON capture from **2024-03-21**, plus captures of
`…/public-api/documentation` (200, 2,531 B, 2025-12-25; **404** by 2026-05-19) (S5) [WEB].
That API went away with the platform. **Whether the 2026 platform exposes any API is
[NOT-VERIFIED].**

**The route that does work: Crossref.**

```bash
# every ChemRxiv deposit, paginated
curl -s 'https://api.crossref.org/prefixes/10.26434/works?rows=1000&cursor=*&select=DOI,posted,license,title&mailto=you@example.org'
# a single record
curl -s 'https://api.crossref.org/works/10.26434/chemrxiv-2022-1ps85'
```

Full-text is **not** in Crossref — you get metadata, DOI, posted date, licence URL and the
landing-page URL only. **There is no verified bulk full-text dump for ChemRxiv**
(contrast the bioRxiv/medRxiv S3 requester-pays buckets). [NOT-VERIFIED]

**Negative controls, 2026-09-01** [API]:

- `https://api.crossref.org/prefixes/10.99999/works?rows=0` → **HTTP 404**, 19 bytes,
  `Resource not found.` — Crossref rejects an unregistered prefix outright. ✅
- `https://api.crossref.org/prefixes/10.26434/works?rows=0&query.bibliographic=zzzqqqxxnotarealthing`
  → **HTTP 200**, 186 bytes, `total-results: 0` — a real 200 with an empty result set, so a
  200 alone proves nothing; always read the count. ✅
- `https://api.crossref.org/prefixes/10.26434/works?rows=0` → `total-results: 55403`,
  facet `type-name` = **`Posted Content: 55403`**, i.e. the prefix contains nothing but
  preprints. Good: the prefix is not shared with ACS journal content.

ISSN **2573-2293 (Online)** is registered to ChemRxiv (S6).

## 10. Licensing and reuse

Authors choose. Distribution over all 53,678 distinct preprints, from the Crossref
`license` field (S1) [API], 2026-09-01:

| Licence | Preprints | Share |
|---|---|---|
| **CC BY-NC-ND 4.0** | 31,711 | 59.1 % |
| **CC BY 4.0** | 10,215 | 19.0 % |
| **CC BY-NC 4.0** | 5,127 | 9.6 % |
| *no licence recorded in Crossref* | 6,612 | 12.3 % |
| ChemRxiv terms-of-use URL | 13 | <0.1 % |

**Three-fifths of ChemRxiv is CC BY-NC-ND** — no derivatives, no commercial use. Only
19 % is CC BY. That is a markedly more restrictive corpus than bioRxiv (~36 % CC-BY/CC0)
and much more restrictive than arXiv-plus-CC. If you intend to build a derivative dataset,
this matters.

The 12.3 % with no licence in Crossref is **entirely a 2026 phenomenon** — every one of the
500 most recent records sampled had `license: none` (S1). Either the new platform is not
depositing licence metadata to Crossref, or it has changed the model. **[NOT-VERIFIED];
do not assume "no licence recorded" means "openly licensed".**

## 11. Caveats

1. **The site is Cloudflare-challenged to automated clients.** Plan on Crossref, not
   scraping (§9).
2. **Two full-corpus platform migrations (2021, 2026)** with three different DOI suffix
   grammars. Old landing-page URLs and the old public API are dead; only the DOIs survive.
3. **No published preprint-to-publication rate.** Unlike bioRxiv, you cannot ask the
   server whether a preprint made it through review.
4. **Screening policy could not be retrieved** (§5). Treat the gate as "unknown but
   non-zero".
5. **The dashboard "Live Content" figure (36,917 at 2026-01-21) disagrees badly with
   Crossref (46,574 at end-2025).** Unresolved (§4).
6. **Licence field went blank in 2026** (§10).
7. **Wikipedia's article is materially out of date** — it does not mention either platform
   migration and its size figures stop in 2019 (S2).
8. **Owned by a publisher.** Not a fatal objection — the society partnership exists to
   dilute it — but it is not the openRxiv model.

## 12. Sources

- **S1** Crossref REST API, prefix `10.26434` — `https://api.crossref.org/prefixes/10.26434/works`
  (full cursor pagination, 55,403 records, `select=DOI,posted,license`) · retrieved
  **2026-09-01** · totals, per-year counts, version-suffix analysis, licence distribution,
  publisher string "American Chemical Society (ACS)", facet `type-name: Posted Content`.
  Script and log: `scratch/preprint-repositories/lifesci/chemrxiv-scan.py`,
  `chemrxiv-crossref-scan.txt`. [API]
- **S2** https://en.wikipedia.org/wiki/ChemRxiv (raw wikitext) · retrieved 2026-09-01 ·
  launch history (announced 2016, opened 2017), ACS/RSC/GDCh ownership, CCS and CSJ
  joining 2019, *Angewandte* March 2018 / JACS August 2018, early size figures. Its own
  cited sources are Chemistry World, C&EN, *Nature* and Coudert, *Nat Chem* 12:499–502
  (2020) `10.1038/s41557-020-0477-5`. **Stale**: no mention of either platform migration.
  [COM/LIT]
- **S3** Wayback Machine capture of `https://chemrxiv.org/` at **20210210095447** ·
  retrieved 2026-09-01 · `<meta name="application-name" content="figshare">`,
  `figstatic.com` asset host — proof the server was still on figshare in Feb 2021. [WEB]
- **S4** Wayback CDX index, `chemrxiv.org/articles*` · retrieved 2026-09-01 · figshare-style
  article URLs (`/articles/<slug>/12440012`) captured 200 through mid-2020, 301 by 2025.
  [WEB]
- **S5** Wayback CDX index, `chemrxiv.org/engage*` and
  `chemrxiv.org/engage/chemrxiv/public-api*` · retrieved 2026-09-01 · dashboard captures
  2021-06-20 → 2026-03-21 (403 from 2026-03-21); `public-api/v1/items` 200/14,978 B at
  2024-03-21; `public-api/documentation` 200 at 2025-12-25, 404 at 2026-05-19. [WEB]
- **S6** Wayback capture of `https://chemrxiv.org/engage/chemrxiv/public-dashboard` at
  **20260121073522** · retrieved 2026-09-01 · title "Homepage | ChemRxiv | Cambridge Open
  Engage"; the migration notice quoted in §2; the 17 category counts in §3; key metrics
  "36,917 Live Content / 75,455,050 Abstract Views / 29,462,885 Content Downloads / 12,460
  Citations"; ISSN 2573-2293; the "not peer reviewed" standing notices. [WEB]
- **S7** Crossref `resource.primary.URL` for `10.26434/chemrxiv.15004130/v1`,
  `10.26434/chemrxiv-2024-glhqn`, `10.26434/chemrxiv.6406505.v1` · retrieved 2026-09-01 ·
  all three now resolve to `https://chemrxiv.org/doi/full/<DOI>`. [API]
- **S8** Kwon D. "How swamped preprint servers are blocking bad coronavirus research."
  *Nature* 581:130–131 (2020-05-07), `10.1038/d41586-020-01394-6`. Cited via S2; **article
  text not retrieved**. [COM]
- **S9** Crossref `query.bibliographic` searches restricted to prefix `10.26434` ·
  retrieved 2026-09-01 · every DOI, title and posted date listed in §7. [API]
- **S10** Direct probes of `https://chemrxiv.org/` and
  `https://chemrxiv.org/engage/chemrxiv/public-api/v1/items` with four user-agents, plus
  `curl -I` response headers (`server: cloudflare`, `cf-mitigated: challenge`) · 2026-09-01.
  [WEB]

### Not verified

- **Current consortium membership.** Verified to 2019 via S2 only. Whether RSC, GDCh, CCS
  and CSJ are all still partners in 2026, and whether **CAS** (Chemical Abstracts Service,
  a division of ACS) is a named partner, could not be confirmed — the About page is behind
  the Cloudflare challenge.
- **Exact date of the figshare → Cambridge Open Engage migration** (narrowed to
  Feb–Jun 2021).
- **Identity of the 2026 platform provider.** The `/doi/full/` URL grammar is
  Atypon-Literatum-shaped and matches `pubs.acs.org`, but this is inference only.
- **Screening policy and criteria** (§5).
- **Any preprint-to-publication rate** for ChemRxiv.
- **Whether the 2026 platform exposes a public API or any bulk full-text route.**
- **Why 12.3 % of records (all 2026) carry no Crossref licence.**
