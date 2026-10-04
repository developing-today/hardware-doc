# Record template — preprint repository records

> **Promoted into the repository 2026-09-20** from
> `archive/research/preprint-repositories/RECORD-TEMPLATE.md`. It defines the evidence-label
> vocabulary (`[API]` `[WEB]` `[DOC]` `[LIT]` `[COM]` `[INF]` `[NOT-VERIFIED]`) and the section
> structure that **all 40 records in this directory use**, so anyone extending the set needs it —
> and a repository convention cannot live in a machine-local archive. Content is unchanged; the
> archive copy is retained and marked superseded.

Copy this structure. Written for `doc/hardware/research/preprint-repositories/` — which is this
directory, so the relative link in *Evidence discipline* below resolves from here.
Working date for this pass: **2026-09-01**.

## Evidence discipline — read before writing anything

This repository's house rule is that **an unsourced number is worse than no number**.

- Every consequential claim carries an **evidence label**:
  - **[API]** — machine-readable API response you actually retrieved (best)
  - **[WEB]** — live web page you actually loaded
  - **[DOC]** — the operator's own published policy/about/FAQ document
  - **[LIT]** — scholarly literature *about* the repository (scientometrics, editorials)
  - **[COM]** — press, blog, community report
  - **[INF]** — your inference from the above, marked as such
  - **[NOT-VERIFIED]** — could not confirm; say so explicitly
- **Never invent a count, a date, a rank or a paper.** If you cannot verify a submission
  count, write `not verified` and explain what you tried.
- **Every landmark paper must carry a stable identifier** (arXiv ID, IACR ePrint number,
  DOI, handle) **and a URL**, and you must state whether the preprint *preceded* a
  venue/journal publication or merely mirrors it. If you cannot confirm the preprint
  actually appeared on that server, do not list it.
- **Record conflicts rather than resolving them by preference.** Wikipedia's size buckets
  frequently disagree with the operator's own counter. Report both and date both.
- **Negative controls matter.** If you probe a URL pattern, also probe a deliberately
  bogus path. HTTP 200 does not mean a document exists — check byte size and magic bytes.

## Section structure

```markdown
# <Name> — preprint repository record

- **URL:** <canonical url>
- **Operator:** <who runs it, and who funds it>
- **Discipline scope:** <as advertised> — <as actually used, if different>
- **Launched:** <year> · **Status:** active | frozen | defunct (<span>)
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What it is

Two or three paragraphs. What problem it solves, why it exists, who it serves.

## 2. Scope and subject taxonomy

For technical repositories, **enumerate the actual computing/electronics categories**
with their codes (e.g. `cs.DC`, `eess.SP`). For others, one short paragraph.

## 3. Size and growth

Real numbers, each with a source and a retrieval date. Distinguish *total deposits* from
*preprints*, and from *records that are actually full text*. Note whether published
versions stay or are replaced.

## 4. Screening and moderation — what gets in

The actual gate: none / automated / staff screening / endorsement / affiliation
requirement / editorial. Say who does it and against what published criteria. Cite the
operator's own policy document.

## 5. Reliability — what you can and cannot trust

The section the reader came for. Be concrete and be honest:
- What a deposit here *does* guarantee (a timestamp, a DOI, a plagiarism scan, nothing).
- Typical eventual-publication rate, if measured in the literature.
- Known failure modes: withdrawn papers, fringe content, paper mills, citation gaming.
- How to sanity-check an individual paper from this server.

## 6. What you actually find there — examples

Concrete, named examples with links. Prefer things a systems/electronics engineer would
recognise. Not a category list — actual documents.

## 7. Landmark papers (software · distributed systems · databases · electronics · security)

Only where the repository genuinely hosts such work. Table:

| Paper | Identifier | Year | Why it matters | Preprint first? |

If the repository hosts nothing in these areas, say so in one line and delete the table.

## 8. Access, APIs and bulk retrieval

OAI-PMH endpoints, REST APIs, bulk dumps, rate limits, whether scripted access is
blocked. Probe results with dates, plus a negative control.

## 9. Licensing and reuse

Default licence, whether authors choose, whether text/data mining is permitted.

## 10. Caveats and controversies

Anything a reader should know before citing something from here.

## 11. Sources

Numbered `S1`, `S2`, … Each: URL · retrieval date · what it supports. Referenced inline
as (S1), (S2).
```
