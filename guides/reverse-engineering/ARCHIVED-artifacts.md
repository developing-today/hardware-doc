# ARCHIVED: schematic net-tracing working space, 2026-09-07

> Moved out of `scratch/`, **not deleted**. Archived **2026-09-20**; every operation was `mv`.

## Identity

| Field | Value |
|---|---|
| Original path | `scratch/schematic-tracing/` |
| Archived to | `archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/` |
| Size | **52,193 bytes** (51 KiB) |
| File count | **8** |
| Tree digest | `4c2805ec9a54f6e0129dfcca299bf6bbe8afbb362a8b1cf6d3487865b9a78b19` |
| Worked | 2026-09-07 · poppler 26.06.0, ImageMagick |

Directory index:
[`archive/guides/reverse-engineering/artifacts/README.md`](../../archive/guides/reverse-engineering/artifacts/README.md).

## It is 51 KB because everything of value was promoted into this repository

It started at **121 MB**. The promotions:

| Was in scratch | Now in the repository |
|---|---|
| `traceability-census.md` | [`schematic-pdf-traceability-census.md`](schematic-pdf-traceability-census.md) |
| `corrections-requiring-review.md` | [`schematic-tracing-corrections-2026-09-07.md`](schematic-tracing-corrections-2026-09-07.md) |
| `trace.py` | `tools/altium_pdf_trace.py` |
| `render.py` | `tools/altium_pdf_reflow.py` |
| `netlist.py` | `tools/altium_pdf_bind_nets.py` |

The three scripts had to move: [`tracing-nets-from-schematic-pdfs.md`](tracing-nets-from-schematic-pdfs.md)
§7 invokes `trace.py` in its worked examples, and **a repository guide cannot depend on a file in
scratch**. The existing `tools/altium_pdf_netlist.py` and `tools/altium_pdf_render_sheet.py` were
**not** substitutes — the latter is a 37-line session script with hardcoded paths — and nothing
was overwritten.

⚠ The pass's own closing section claimed *"this directory can be deleted without losing a
finding"*. **That was false**, and the 2026-09-20 consolidation says so: the census and the
corrections index were the two most valuable things in it and neither had been promoted. The
individual corrections *had* been applied, append-only, to their named records (spot-checked
`axpm65611`, `m5stack-dinmeter/rotary-encoder`, `silergy/sy8089`,
`cardputer-adv/gaps-and-conflicts`) — it was the consolidated index of them that was missing.

## What was removed, and why it was safe

| Removed | Files | Bytes | Recipe, proven byte-identical |
|---|---:|---:|---|
| `text/` | 273 | ~121,600,000 | `pdftotext -layout <src.pdf>` |
| `bbox/` | 19 | ~5,560,000 | `pdftotext -bbox-layout <src.pdf>` |

Before removal, **all 273 `text/` files were resolved to their source PDF, and all 273 resolved to
a PDF in the repository** — none archive-only, none missing. Regeneration was then proven on a
13-file spread plus every `bbox/` file sampled: **0 differences**, poppler 26.06.0.

### A decoding trap that nearly caused a wrong call

The `text/` filenames encoded `/` as `__` **and a space as a single `_`**. A first pass reversing
only `__` concluded **21 source PDFs were missing from both repository and archive**, which would
have made those extractions irreplaceable and unsafe to remove. They were not missing:
`GT911 Rev.10.pdf` had been written `GT911_Rev.10`, and `BMA423.PDF` had a second `.pdf` appended
by the reconstruction. **The hypothesis is refuted**, and this is the record of it.

## What is still in the archive

| Path | Status |
|---|---|
| `index-fragments.md` | ⚠ **Proposed index edits, still unapplied** — outside the scope of the 2026-09-07 pass, the 2026-09-20 consolidation, and the relocation. Pending work, not a finding. Cited from `research/passes/index-merge/corrections-requiring-review.md` |
| `traceability-census.md`, `corrections-requiring-review.md` | Byte-identical working originals of the two promoted documents |
| `trace.py`, `render.py`, `netlist.py` | Byte-identical working originals of the three promoted tools |
| `images/README.md` | A 1.5 KB note; the directory holds no images |

## How to get it back

```bash
mv "archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07" \
   "scratch/schematic-tracing"
```

Everything in it except `index-fragments.md` is byte-identical to a file in this repository, so
the archive copy is a convenience. The removed intermediates regenerate with the two commands
above from PDFs the repository already holds — **which is the whole point of the census**: it
records, per file, whether a schematic PDF has a recoverable text layer at all (38 traceable,
5 partly, 6 not, with the `pdffonts` evidence proving the negatives were outlined to vector paths
and are unrecoverable by any tool).
