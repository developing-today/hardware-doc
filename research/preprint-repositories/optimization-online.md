# Optimization Online — eprint repository record

- **URL:** https://optimization-online.org/
- **Operator:** Volunteer editorial team — a **Principal Coordinator** (Andreas Wächter,
  Gurobi Organization), a **Deputy Principal Coordinator** (Stephen Wright, University of
  Wisconsin–Madison) and ~17 **Area Coordinators** (S1). **Supported by the Mathematical
  Optimization Society and the Wisconsin Institute for Discovery** at UW–Madison, and
  physically hosted "on the servers within the Discovery Building" (S1).
- **Discipline scope:** "a repository of Eprints about optimization and related topics"
  (S1) — linear, integer, conic/semidefinite, nonlinear, global, stochastic, robust and
  bilevel optimization, plus applications and **optimization software** (§2).
- **Launched:** **2000** — "conceived in 2000 by Jean-Pierre Goux, Sanjay Mehrotra, and Steve
  Wright as an initiative of the **Optimization Technology Center** at Argonne and
  Northwestern" (S1). Oldest eprint on the site: **2000-08-08** (S4). **Status:** active,
  26 years continuous.
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What it is

Optimization Online is the mathematical-optimization community's own eprint archive. It
predates almost every server in this collection except arXiv and the IACR ePrint archive,
and it has run continuously since August 2000 under three generations of custodians: Goux
built the original site; **Steve Wright "maintained the site as lead moderator, and mailed
the monthly digests from 2000–2021"**; Andreas Wächter is the current lead moderator (S1).
The "monthly digest" is not incidental — an email announcement list
(`https://groups.google.com/a/g-groups.wisc.edu/g/optimization-online/`) is linked from the
front page (S2) and is how much of the field actually consumes the archive.

It is a **repository, not a journal**: submission is free, there is no peer review, and the
service explicitly disclaims quality judgement (§4). What it is not is a general
mathematics server — that is arXiv `math.OC` — and the relationship between the two is
discussed in §5.

**The 2022 relaunch.** The site was rebuilt on WordPress and the migration is documented in
the operator's own credits: "Em Craft at the Wisconsin Institute for Discovery has provided
technical support starting in 2011. She conceived and developed the **new WordPress-based
site that went live in 2022**" (S1). Note that this is **2022, not 2023** — if you have seen
"2023 relaunch" written elsewhere, the operator's own About page contradicts it. The live
site reports `<meta name="generator" content="WordPress 6.5.10">` on the GeneratePress
theme (S2). Old URLs survived the rebuild; see §8, which is the durability question this
knowledge base cares about.

## 2. Scope and subject taxonomy

Every eprint carries **between 1 and 3 categories** from a two-level taxonomy (S3). The
counts below are the site's own per-category counters, read from
`https://optimization-online.org/categories/` on **2026-09-01** (S3). Because items carry up
to three, the column sums well above the 9,843 total.

| Top-level category (count) | Sub-categories (counts) |
|---|---|
| **Nonlinear Optimization** (2,554) | Constrained Nonlinear Optimization (799), Unconstrained (392), Quadratic Programming (309), Systems governed by Differential Equations (135), Nonlinear Systems and Least-Squares (117), Bound-constrained (97) |
| **Convex and Nonsmooth Optimization** (2,177) | Convex Optimization (1,073), Nonsmooth Optimization (684), Generalized Convexity/Monoticity (63) |
| **Integer Programming** (2,088) | (Mixed) Integer Linear Programming (766), (Mixed) Integer Nonlinear Programming (588), Cutting Plane Approaches (306), 0-1 Programming (303) |
| **Applications – OR and Management Sciences** (1,797) | Transportation (368), Scheduling (243), Finance and Economics (196), Production and Logistics (184), **Telecommunications (112)**, Supply Chain Management (98), Airline Optimization (35), Yield Management (20), Marketing (14) |
| **Linear, Cone and Semidefinite Programming** (1,616) | Semi-definite Programming (658), Linear Programming (340), Second-Order Cone Programming (117), Cone Programming (39) |
| **Combinatorial Optimization** (1,412) | Branch and Cut Algorithms (232), Polyhedra (227), Approximation Algorithms (181), Meta Heuristics (172), Graphs and Matroids (160) |
| **Applications – Science and Engineering** (1,350) | Statistics (188), Data-Mining (160), **Control Applications (156)**, Biomedical (106), **Energy (93)**, Facility Planning and Design (89), Basic Sciences (86), Optimization of Systems modeled by PDEs (71), Mechanical Engineering (46), Multidisciplinary Design Optimization (35), Chemical Engineering (33), Civil and Environmental Engineering (30), **VLSI layout (13)** |
| **Stochastic Programming** (1,137) | — |
| **Other Topics** (832) | Multi-Criteria Optimization (300), Dynamic Programming (212), Game Theory (172), Optimization of Simulated Systems (51) |
| **Global Optimization** (768) | Global Optimization Theory (237), Applications (124), Stochastic Approaches (77) |
| **Robust Optimization** (729) | — |
| **Optimization Software and Modeling Systems** (435) | **Parallel Algorithms (137)**, **Optimization Software Benchmark (71)**, **Optimization Software Design Principles (44)**, **Modeling Languages and Systems (39)**, **Problem Solving Environments (22)** |
| **Network Optimization** (320) | — |
| **Complementarity and Variational Inequalities** (297) | — |
| **Optimization in Data Science** (160) | Data Science Algorithms (43), Data Science Applications (14), Data Science Theory (12) |
| **Infinite Dimensional Optimization** (167) | Semi-infinite Programming (66), Distributed Control (11) |
| **Bilevel Optimization** (47) | — |

Free-text **tags** exist alongside categories; the front page surfaces a tag cloud including
`branch-and-bound`, `branch-and-cut`, `column-generation`, `cutting-planes`,
`interior-point-methods`, `mixed-integer-linear-programming`, `benders-decomposition`,
`distributionally-robust-optimization`, `derivative-free-optimization` (S2).

## 3. Why a systems or hardware engineer should care

This is a mathematics repository, so the connection needs stating plainly. Almost every
hard resource-allocation problem in computing systems is an optimization model, and the
people who write the solvers you would use publish their solver papers **here**, not on
arXiv:

- **Solvers you actually link against.** The SCIP Optimization Suite release reports —
  `The SCIP Optimization Suite 9.0` (2024-02-26) and `10.0` (2025-11-24) — are posted here
  (S4). SCIP 10.0's abstract lists "a new solving mode for exactly solving rational
  mixed-integer linear programs", conflict analysis, symmetry handling — the kind of detail
  that only appears in the release report. **IPOPT**'s definitive implementation paper is
  here (§7). `PaPILO: A Parallel Presolving Library for Integer and Linear Optimization with
  Multiprecision Support` (2023-08-04) is here.
- **ILP/MILP formulations.** `Integer Programming` (2,088) plus `(Mixed) Integer Linear
  Programming` (766) is where you find formulations for the problems that show up as
  scheduling, placement, partitioning and register allocation.
- **Compiler and EDA-adjacent work.** The `VLSI layout` sub-category is small (13) but
  real, and includes both classic and current work — `Global Routing in VLSI Design:
  Algorithms, Theory, and Computational Practice` (2010) and `Sequential Nonlinear-Programming
  Approach to Thermal-Aware VLSI Floorplanning using Multi-boundary Shapes` (2026-04-01) (§7).
- **Scheduling and routing.** `Scheduling` (243), `Transportation` (368),
  `Production and Logistics` (184), `Network Optimization` (320).
- **Benchmarks and reproducibility.** `Optimization Software Benchmark` (71) — this is where
  MIPLIB-style benchmark methodology and solver comparisons live.
- **Parallel and HPC solver engineering.** `Parallel Algorithms` (137).
- **Energy and control.** `Energy` (93), `Control Applications` (156) — grid dispatch, unit
  commitment, MPC formulations.
- **QUBO / quantum annealing.** The most-used practical tutorial on encoding constrained
  problems as QUBO — the format D-Wave and Ising-machine hardware consume — is here (§7).

## 4. Screening and moderation — there *is* an editorial check, and it is documented

Unlike arXiv (endorsement-based) or engrXiv (volunteer pre-moderation), Optimization Online
runs a **coordinator-based editorial screen**, and unusually it publishes both the
submitter-facing policy *and* the internal instructions given to coordinators.

**Submitter-facing policy** (S5, verbatim):

> "Papers can be submitted to Optimization Online only in pdf format. Papers are screened to
> ensure their relevance **by one of the coordinators for the category selected by the
> submitting author as the principal category**. The acceptance/rejection decision of a
> coordinator is **final**. Coordinators check that the submission details given by the
> authors are all present and correct and that the submitted files are readable. They **do
> not usually evaluate the report for quality or mathematical correctness**. Consequently,
> we make no claim about quality or correctness of the reports on the site. Optimization
> Online reserves the right in its sole discretion to remove accepted papers from the
> repository if complaints are received regarding their accuracy or authenticity."

**Coordinator-facing instructions**, published openly on the Help page (S3, verbatim):

> "To approve the EPrint: Verify the following: … The title should not be in ALL CAPS. This
> messes up the uniform look of our pages and digests. **The EPrint should not be obviously
> crazy or wrong (e.g. P=NP papers). But otherwise, be fairly permissive and generous with
> accepts. The EPrint has not already appeared. If the author gives a journal, volume number,
> page number, etc, the work is deemed to have appeared and you should reject it.**"

Three consequences worth internalising:

1. **There is a crank filter.** "Not obviously crazy or wrong (e.g. P=NP papers)" is an
   explicit, named exclusion. This is more of a gate than arXiv's `math.GM` provides.
2. **Already-published work is rejected.** Optimization Online is a *pre*print archive in
   the strict sense. This is why the archive is not a green-OA mirror of the literature —
   and why post-publication the site encourages replacing the full text with a reference:
   "We encourage authors to provide a reference to the paper in place of the full text, once
   it has been published in a journal" (S5).
3. **Authors are responsible for copyright compliance after transfer**: "Authors are
   responsible for removing a paper from the site once copyright for the paper has been
   transferred to a publisher" (S5).

Authors can also self-edit and self-delete: the Help page documents "Move to Trash",
"Update", PDF replacement and restoration from trash, with the note "EPrints in the trash
longer than a week may be permanently removed" (S3).

## 5. Reliability — what you can and cannot trust

**A posting guarantees:** a stable URL under `optimization-online.org/YYYY/MM/ID/`, a
`Published:` date and an `Updated:` date, a category assignment, a coordinator's judgement
that the work is in scope and not obvious crankery, and a hosted PDF. It does **not**
guarantee correctness — the operator says so ("we make no claim about quality or
correctness", S5).

**No DOIs.** Optimization Online assigns no persistent identifiers. Items are cited by URL,
and the site provides two URL forms (a dated permalink and a `?p=NNNNN` short URL, §8). If
you need a DOI for an optimization preprint, the author has to post to arXiv as well.

**Relationship to arXiv `math.OC` — overlap is large and deliberate.** Scale first (S6, S4):

| Archive | Items | Date |
|---|---|---|
| arXiv `math.OC` | **63,892** | 2026-09-01 |
| Optimization Online | **9,843** | 2026-09-01 |

arXiv `math.OC` is 6.5× larger. So why do authors use Optimization Online at all, and often
*both*?

- **Audience targeting.** Optimization Online's monthly digest goes to the optimization
  community specifically (S1, S2). arXiv `math.OC` is a firehose shared with control theory,
  calculus of variations and machine-learning theory.
- **A curated, single-discipline category tree** (§2) that maps onto how the field actually
  divides itself — you can browse "Cutting Plane Approaches" or "Semi-definite Programming"
  directly, which no arXiv category supports.
- **The "Citation" field.** Every Optimization Online record carries a free-text `Citation`
  line where authors record the eventual journal reference or the originating tech-report
  number. On the IPOPT record it reads "IBM Research Report RC 23149, IBM T.J. Watson
  Research Center…"; on the Julia record it reads "Published in INFORMS Journal on Computing:
  http://dx.doi.org/10.1287/ijoc.2014.0623" (S4). This is a human-maintained
  preprint→publication link, and it is often present where Crossref has nothing.
- **The crank filter** (§4) — a real, if modest, quality signal that arXiv `math.OC` does
  not provide.

Authors who want both the DOI-less community channel *and* arXiv's indexing and permanence
simply post twice. **The fraction that do is [NOT-VERIFIED]** — no cross-matching study was
run in this pass, and Optimization Online exposes no arXiv-ID field to match on.

**Known failure modes.** (a) Authors are supposed to remove full text after copyright
transfer (§4), so **a record can lose its PDF over time** — the archive is not designed to
be permanent full text. (b) No DOI means link rot is a live risk, mitigated but not
eliminated by the redirect layer (§8). (c) `Updated:` dates can be many years after
`Published:` (the IPOPT record shows "Published: 2004/03/15, Updated: 2022/08/04", S4), so
the document you download may not be the one that was posted. (d) No versioning UI — an
update overwrites.

**How to sanity-check an item.** Read the `Citation` field first; if it names a journal,
read the journal version. Compare `Published:` and `Updated:`. Confirm the PDF is still
attached (some records have no "View PDF" link at all — the Julia record is one, S4).

## 6. Size and growth

| Measure | Value | Date | Source |
|---|---|---|---|
| WordPress REST API `X-WP-Total` header on `/wp/v2/posts` | **9,843** | 2026-09-01 | [API] S4 |
| Sum of the site's own month-archive counters (314 months) | **9,843** | 2026-09-01 | [WEB] S1 |

**Two independent counters agree exactly.** That is the strongest size evidence in this
whole collection, and it is worth stating: the WordPress post count and the front-end
archive widget were computed by different code paths and returned the same number.

**Eprints by year** (from the month-archive counters, S1):

| Year | N | | Year | N | | Year | N |
|---|---|---|---|---|---|---|---|
| 2000 | 34 | | 2009 | 312 | | 2018 | 561 |
| 2001 | 167 | | 2010 | 340 | | 2019 | 497 |
| 2002 | 165 | | 2011 | 415 | | 2020 | **601** |
| 2003 | 200 | | 2012 | 393 | | 2021 | 535 |
| 2004 | 219 | | 2013 | 435 | | 2022 | 400 |
| 2005 | 220 | | 2014 | 491 | | 2023 | 370 |
| 2006 | 238 | | 2015 | 515 | | 2024 | 379 |
| 2007 | 284 | | 2016 | 484 | | 2025 | 410 |
| 2008 | 296 | | 2017 | 557 | | 2026 (to 09-01) | 325 |

The shape is a 20-year climb peaking in 2020 (601), a dip to 370 in 2023, and a partial
recovery. 2026 at 325 by 1 September annualises to ~490 [INF] — the highest since 2019.
Notably, **there is no generative-AI submission spike** of the kind engrXiv reports; the
combination of a specialised field, a required PDF and a coordinator screen appears to have
held [INF].

## 7. Landmark and representative entries

All verified live on 2026-09-01 (S4). "Preprint first?" is judged from the record's own
`Published:` date versus the journal version's year.

| Eprint | URL | Published | Why it matters | Preprint first? |
|---|---|---|---|---|
| Wächter & Biegler, *On the Implementation of an Interior-Point Filter Line-Search Algorithm for Large-Scale Nonlinear Programming* | https://optimization-online.org/2004/03/836/ | 2004-03-15 (updated 2022-08-04) | **The IPOPT paper.** The definitive description of the algorithm behind the open-source IPOPT solver, benchmarked on 954 CUTEr problems. One of the most-cited papers in nonlinear optimization. `Citation:` "IBM Research Report RC 23149" | **Yes** — posted March 2004; the journal version is *Math. Program.* 106(1), 2006 |
| Dunning & Lubin, *Computing in Operations Research using Julia* | https://optimization-online.org/2013/05/3883/ | 2013-05-19 (updated 2015-03-18) | The paper that established Julia as a viable language for mathematical optimization; the direct ancestor of **JuMP**. Explicitly about JIT compilation and cross-language benchmarks | **Yes** — `Citation:` "Published in INFORMS Journal on Computing: 10.1287/ijoc.2014.0623" (2015) |
| Du, Glover & Kochenberger, *A Tutorial on Formulating and Using QUBO Models* | https://optimization-online.org/2019/01/7014/ | 2019-01-05 (updated 2019-06-14) | The standard practical reference for encoding constrained combinatorial problems as QUBO — the input format for D-Wave quantum annealers and neuromorphic Ising hardware. Tags: `quantum computing`, `quadratic binary programming` | **Yes** — widely circulated from this posting |
| Hojny, Besançon, Bestuzheva et al., *The SCIP Optimization Suite 10.0* | https://optimization-online.org/2025/11/the-scip-optimization-suite-10-0/ | 2025-11-24 | Release report for the leading open-source MILP/MINLP/CIP solver; 28 authors. Includes exact rational MILP solving, implied-integrality presolve, flower-inequality separation | **Yes** — this *is* the report; SCIP release reports are canonically published here |
| Bestuzheva et al., *The SCIP Optimization Suite 9.0* | https://optimization-online.org/2024/02/the-scip-optimization-suite-9-0/ | 2024-02-26 | Previous SCIP release report | Yes |
| *PaPILO: A Parallel Presolving Library for Integer and Linear Optimization with Multiprecision Support* | https://optimization-online.org/2023/08/papilo-a-parallel-presolving-library-for-integer-and-linear-optimization-with-multiprecision-support/ | 2023-08-04 | The presolver used by SCIP; parallel + multiprecision | Yes |
| Deza, Terlaky, Vannelli, Dickson & Zhang, *Global Routing in VLSI Design: Algorithms, Theory, and Computational Practice* | https://optimization-online.org/2010/12/2852/ | 2010-12-14 | Polynomial-time approximation algorithm for VLSI global routing from an IP formulation, with serial and parallel implementations, on standard benchmarks. Categories: Integer Programming, **VLSI layout** | Yes |
| Morton, *Sequential Nonlinear-Programming Approach to Thermal-Aware VLSI Floorplanning using Multi-boundary Shapes* | https://optimization-online.org/2026/04/sequential-nonlinear-programming-approach-to-thermal-aware-vlsi-floorplanning-using-multi-boundary-shapes/ | 2026-04-01 | Current EDA-adjacent work: thermal-aware soft-macro floorplanning with IO-block placement | Yes |
| *Optimization as an Internet Resource* | https://optimization-online.org/2000/08/190/ | 2000-08-08 | **The oldest eprint on the server** — the Optimization Technology Center's own manifesto, and a nice historical marker | Yes |

Two more worth knowing about, verified present (S4): *Template-based Minor Embedding for
Adiabatic Quantum Optimization* (2019-10-09,
https://optimization-online.org/2019/10/7418/), which is about mapping problems onto D-Wave
Chimera/Pegasus hardware graphs; and *Smoothie: Mixing the strongest MIP solvers to solve
hard MIP instances on supercomputers* (2025-10-27) for HPC-scale solver portfolios.

## 8. Access, APIs, bulk retrieval — and URL durability

**No OAI-PMH, no DOIs.** `/oai` and `/oai2` both return **404** (S7). There is no
machine-readable identifier scheme.

**The WordPress REST API is fully open and is the right bulk interface:**

```bash
curl -I 'https://optimization-online.org/wp-json/wp/v2/posts?per_page=1'   # X-WP-Total: 9843
curl 'https://optimization-online.org/wp-json/wp/v2/posts?per_page=100&page=2&_fields=id,date,link,title'
curl 'https://optimization-online.org/wp-json/wp/v2/posts?search=SCIP&per_page=5&_fields=id,date,link,title'
curl 'https://optimization-online.org/wp-json/'                            # route discovery
```

`X-WP-Total` gives the exact corpus size in a single HEAD request. There is also an RSS feed
(`/feed/`) and a sitemap. `robots.txt` is permissive — it disallows only `/wp-admin/` and
publishes `Sitemap: https://optimization-online.org/wp-sitemap.xml` (S7); no crawl-delay, no
AI-crawler exclusions, no Cloudflare challenge, and no user-agent substitution was needed at
any point.

### URL durability across the 2022 rebuild — probed

This is the question this knowledge base cares about, and the answer is **good**. The
pre-2022 site used `DB_HTML/YYYY/MM/ID.html` for abstracts and `DB_FILE/YYYY/MM/ID.pdf` for
full text. Probed 2026-09-01 (S7):

| Old-style URL | Result | Final location |
|---|---|---|
| `http://www.optimization-online.org/DB_HTML/2005/03/1078.html` | 301 → … → **200** (3 hops) | `https://optimization-online.org/2005/03/1078/` |
| `http://www.optimization-online.org/DB_HTML/2004/03/836.html` (IPOPT) | 301 → … → **200** (3 hops) | `https://optimization-online.org/2004/03/836/` |
| `http://www.optimization-online.org/DB_HTML/2001/12/420.html` | 301 → … → **200** | `https://optimization-online.org/2001/12/420/` |
| `http://www.optimization-online.org/DB_FILE/2004/03/836.pdf` | 301 → … → **200** (3 hops) | `https://optimization-online.org/2004/03/836/` — **the landing page, not the PDF** |
| `https://optimization-online.org/?p=9506` (short URL) | **301** (1 hop) | `https://optimization-online.org/2004/03/836/` |

**Verdict:** old abstract URLs from 2001, 2004 and 2005 all still resolve to the correct
current record, including the `http://` and `www.` forms. That is 20+ year link stability
across a full platform change — better than most publishers manage. **One caveat:** old
direct-PDF links (`DB_FILE/.../ID.pdf`) redirect to the *landing page*, not to a PDF. Any
crawler that stored `DB_FILE` URLs and expects `application/pdf` will now receive HTML with
a 200 status. Current PDFs live at `https://optimization-online.org/wp-content/uploads/YYYY/MM/ID.pdf`.

### Negative controls — three of them

| Probe | Result |
|---|---|
| `https://optimization-online.org/this-page-does-not-exist-zzz9999/` | **404**, 93,532 bytes |
| `http://www.optimization-online.org/DB_HTML/1999/99/999999.html` (bogus old-style) | **404**, 93,528 bytes — *no* redirect issued |
| `http://www.optimization-online.org/DB_HTML/2000/09/1.html` (plausible but non-existent old ID) | **404** after 2 redirect hops |
| `https://optimization-online.org/wp-content/uploads/2004/03/999999.pdf` (bogus PDF) | **404**, 93,551 bytes |
| *Control:* `https://optimization-online.org/wp-content/uploads/2004/03/836.pdf` (real PDF) | **200**, **333,438 bytes**, `Content-Type: application/pdf` |

So the redirect layer is **selective** — it rewrites only IDs that exist, and returns a real
404 otherwise. And a 404 body here is ~93 KB of themed error page, so **content-length is
useless as an existence test; you must read the status code or the Content-Type** (S7).

## 9. Licensing and reuse

**There is no licence.** Optimization Online applies no Creative Commons or other open
licence. The copyright terms are (S5, verbatim):

> "By submitting a paper, all authors of the paper represent and warrant that: (i) the paper
> constitutes an original work of authorship and that any necessary permissions have been
> obtained…; and (ii) **other users of Optimization Online are granted permission to download
> the paper for personal use.**"

"Download for personal use" is the *entire* grant. That means: **no redistribution, no
inclusion in a derived corpus, no text-and-data-mining of the full text under an open
licence.** Metadata harvesting via the WordPress API is a different matter and is not
restricted by robots.txt, but the PDFs themselves are all-rights-reserved-with-a-reading-
permission. Anyone building a mining pipeline should treat this repository differently from
arXiv or TechRxiv.

The site also disclaims liability for copyright violations and requires authors to indemnify
the coordinators, sponsors and hosts (S5).

## 10. Caveats and controversies

- **No DOIs, no OAI-PMH, no versioning.** For a 26-year-old archive this is the biggest
  structural weakness. Cite the dated permalink (`/YYYY/MM/ID/`), which is what the redirect
  layer preserves; the `?p=NNNNN` short URL also works but is opaque.
- **Full text is expected to be withdrawn after journal publication** (§4). The archive is
  explicitly *not* a permanent open-access record; treat it as a preprint announcement
  service. Archive PDFs you depend on.
- **The restrictive licence** (§9) is the strictest in this collection and is easy to miss
  because the site otherwise feels like an open repository.
- **`Updated:` can lag `Published:` by nearly two decades** (§5) — pin what you downloaded.
- **Rejection decisions are final and unappealable** (§4), and coordinators may reject "for
  any reason"; there is no published rejection rate. **[NOT-VERIFIED]**.
- **Relaunch year:** the operator's About page says **2022** (S1). Any secondary source
  claiming 2023 is contradicted by the primary document; this record follows the primary.
- **Overlap with arXiv `math.OC` is unquantified** (§5) — **[NOT-VERIFIED]**.
- **Not indexed as a source in OpenAlex.**
  `https://api.openalex.org/sources?filter=display_name.search:Optimization%20Online` returns
  `meta.count = 0` (S8) — unsurprising given the absence of DOIs, but a real gap for anyone
  doing bibliometrics.
- **Wikipedia has no retrievable article**: the REST summary endpoint for
  `Optimization_Online` returned an internal error on 2026-09-01 (S8), so no independent
  size or history cross-check is recorded here.

## 11. Sources

- **S1** — `https://optimization-online.org/about/` — coordinator roster (Principal, Deputy
  and 17 Area Coordinators with their areas), the *Development* section (conceived in 2000 by
  Goux, Mehrotra and Wright at the Optimization Technology Center, Argonne/Northwestern;
  Wright as lead moderator and digest mailer 2000–2021; Wächter current lead), *Support*
  (Mathematical Optimization Society + Wisconsin Institute for Discovery), *Hosting*
  (Discovery Building), and *Special Credits* ("the new WordPress-based site that went live
  in 2022"). The page also carries the full month-archive widget used for the per-year
  table. Retrieved 2026-09-01. **[DOC]**
- **S2** — `https://optimization-online.org/` — front page; `<meta name="generator"
  content="WordPress 6.5.10">`; GeneratePress theme; tag cloud; link to the announcement
  list `https://groups.google.com/a/g-groups.wisc.edu/g/optimization-online/`. Retrieved
  2026-09-01. **[WEB]**
- **S3** — `https://optimization-online.org/categories/` (the full two-level taxonomy with
  per-category counters, "Each Eprint may have between 1 and 3 categories") and
  `https://optimization-online.org/help/` (the coordinator approval instructions quoted in
  §4, plus the eprint edit/trash lifecycle). Retrieved 2026-09-01. **[DOC]**
- **S4** — WordPress REST API, `https://optimization-online.org/wp-json/wp/v2/posts`
  (`X-WP-Total: 9843`; `?search=` queries for SCIP, MIPLIB, IPOPT, VLSI, compiler, quantum
  annealing, benchmark, scheduling; `?order=asc&orderby=date` for the oldest records) and
  `https://optimization-online.org/wp-json/` for route discovery; plus direct retrieval of
  the individual eprint pages `2004/03/836/`, `2013/05/3883/`, `2019/01/7014/`,
  `2010/12/2852/`, `2025/11/the-scip-optimization-suite-10-0/` and
  `2026/04/sequential-nonlinear-programming-approach-to-thermal-aware-vlsi-floorplanning-using-multi-boundary-shapes/`
  for their `Published:`/`Updated:`/`Categories`/`Citation`/`Short URL` fields. Retrieved
  2026-09-01. **[API]/[WEB]**
- **S5** — `https://optimization-online.org/submit/` — the *Moderation* and *Copyright*
  sections quoted verbatim in §4 and §9. Retrieved 2026-09-01. **[DOC]**
- **S6** — arXiv API,
  `https://export.arxiv.org/api/query?search_query=cat:math.OC&start=0&max_results=1`,
  reading `<opensearch:totalResults>` = **63,892**. Retrieved 2026-09-01. **[API]**
- **S7** — Live HTTP probes, 2026-09-01: `/robots.txt` (200, 124 B, quoted); `/wp-sitemap.xml`
  (200); `/oai` and `/oai2` (both 404); the five old-style URL redirect chains and the
  `?p=9506` short URL in §8; the real PDF `wp-content/uploads/2004/03/836.pdf` (200,
  333,438 B, `application/pdf`); and the four negative controls
  (`/this-page-does-not-exist-zzz9999/`, `DB_HTML/1999/99/999999.html`,
  `DB_HTML/2000/09/1.html`, `wp-content/uploads/2004/03/999999.pdf`). **[WEB]**
- **S8** — `https://api.openalex.org/sources?filter=display_name.search:Optimization%20Online`
  (`meta.count = 0`); Wikipedia REST
  `https://en.wikipedia.org/api/rest_v1/page/summary/Optimization_Online` (internal error).
  Retrieved 2026-09-01. **[API]**
