# No schematic exists for this board

**Verified 2026-09-04.** This is a negative result, recorded so it is not re-investigated.

LilyGO's wiki page for the T-Display K230 contains a heading `## Schematic` with **no link, no
file and no content beneath it**. The same is true of `## Dimension Diagram` on the bare-board
page. This is a *soft* gap: there is no 404, no broken link, and nothing for a link checker to
catch — the section is simply empty.

Checked and empty:

- `https://wiki.lilygo.cc/products/t-display-series/t-display-k230/` — `#schematic` heading, no content
- `https://wiki.lilygo.cc/products/t-display-series/t-display-k230/cased-version.html` — no schematic
- `https://github.com/Xinyuan-LilyGO/T-Display-K230` @ `bb831ab358b66f5bd9a87ecd7c580fee4537492e` — no schematic, no EDA files
- `https://lilygo.cc/products/t-display-k230` and `/t-display-k230-kit` — product descriptions only

**For comparison**, LilyGO *does* publish a schematic for older products in the same series — the
T-Display wiki page links "T-Display V1.0 Schematic". So this is a per-product omission, not a
vendor-wide policy, and it may appear later.

## What this costs

Every pin claim in [`../../pinouts-and-buses.md`](../../pinouts-and-buses.md) rests on a **single
vendor document** (`HARDWARE_PINMAP.md`) with nothing to cross-check it against. And six parts
remain unidentified because there is no netlist and no PCB photograph:
[`components/unidentified/t-display-k230`](../../../../../components/unidentified/t-display-k230/README.md).

## Nearest available substitutes

Canaan publishes complete EDA sources for its **own** K230 reference boards — schematic PDFs,
OrCAD `.DSN`, Gerbers, PCB, DXF, SMT and BOM — under the **Chinese** tree of `kendryte/k230_docs`.
The LilyGO board is an LPDDR4, non-SiP design, so `K230_LP4` (the USIP EVB) is the closest
reference. Full inventory with exact sizes and two reacquisition URLs each:
[`components/canaan/k230/artifacts/CANAAN-EDA-SET.md`](../../../../../components/canaan/k230/artifacts/CANAAN-EDA-SET.md).

Tracked as [`GC-5`](../../gaps-and-conflicts.md). Reacquisition status: **lost** — because the
document was never created, not because it was missed.
