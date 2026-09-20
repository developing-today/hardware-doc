# Canaan K230 reference-board EDA and PDF set — enumerated, not retrieved

**Status:** `reference-only` · **Reacquisition:** `automatic` · **Enumerated 2026-09-04**

## What this is

Canaan publishes the complete electrical design of its own K230 evaluation boards inside the
documentation repository — but only under the **Chinese** tree (`zh/00_hardware/`). The English
tree (`en/00_hardware/`) contains no binary hardware artifacts at all. An agent reading only
`en/` will conclude that Canaan publishes no schematics. **It does.** That is the single most
useful fact in this file.

## Why it was not pulled into the repository

None of it describes the **K230 die**, and none of it describes the **LilyGO T-Display K230**.
It is board-level design data for three Canaan reference boards. The set totals roughly
**19 MB** across 20 files, dominated by OrCAD `.DSN` sources and Gerber/PCB archives that are
only useful with the matching EDA tool. The die-level documents that *are* relevant
(`K230_datasheet`, `K230_brief_datasheet`, `K230_Hardware_Design_Guide`) are retained beside
this file in Markdown form.

## What was learned before deciding not to retain it

- `K230_datasheet.md` §"Pin information description" defers ball assignments to a document
  called **`K230_PINOUT_V1.0_20230524`**. A full recursive listing of the repository tree on
  2026-09-04 confirms **that document is not published anywhere in the repository**, in either
  language. The board schematics below are therefore the only public route to K230 ball
  assignments.
- Three distinct reference designs exist and they are *not* interchangeable: `K230_LP3`
  (LPDDR3 demo board), `K230_LP4` (LPDDR4 USIP EVB) and `K230D` (SiP EVB). The LilyGO
  T-Display K230 is an LPDDR4, non-SiP design, so `K230_LP4` is the closest reference.

## Inventory

Repository: `github.com/kendryte/k230_docs`, branch `main`, commit
**`f8e30213963e0ed5cf995c3cd4701218a45e4793`** (2025-09-12). Licence on the repository:
**BSD-2-Clause**; the documents themselves carry a restrictive Canaan notice (see the
component README §18 — the two conflict).

| Upstream path (under `zh/00_hardware/`) | Bytes |
|---|---:|
| `CanMV_K230/CanMV-K230-V1.0_2023-09-15.pdf` | 3 100 623 |
| `CanMV_K230/CanMV-K230_2023-10-11.html` | 11 309 206 |
| `K230D/K230-SIP-EVB-V1.0-A.1-20230317.pdf` | 967 009 |
| `K230D/K230-SIP-EVB-V1_0-A_1-20230316.DSN` | 1 700 864 |
| `K230D/K230-SIP-EVB-V1_0-A_1-20230322-DXF.zip` | 119 817 |
| `K230D/K230-SIP-EVB-V1_0-A_1-20230322-GERBER.zip` | 411 727 |
| `K230D/K230-SIP-EVB-V1_0-A_1-20230322-PCB.zip` | 2 444 898 |
| `K230D/K230-SIP-EVB-V1_0-A_1-20230322-SMT.zip` | 691 376 |
| `K230D/K230-SIP-EVB-V1_0-A_1_20230316-BOM.xlsx` | 22 658 |
| `K230_LP3/K230-DEMO-BOARD-BOM-20230510.xlsx` | 21 132 |
| `K230_LP3/K230-DEMO-BOARD-SCH.DSN` | 1 852 416 |
| `K230_LP3/K230-DEMO-BOARD-SCH.pdf` | 969 203 |
| `K230_LP3/K230_DEMO_BOARD-20230427-DXF.zip` | 168 246 |
| `K230_LP3/K230_DEMO_BOARD-20230427-GERBER.zip` | 472 714 |
| `K230_LP3/K230_DEMO_BOARD-20230427-PCB.zip` | 2 533 161 |
| `K230_LP3/K230_DEMO_BOARD-20230427-SMT.zip` | 653 967 |
| `K230_LP4/K230-USIP-EVB-LP4-SCH-V1.1-A.1-20230330.DSN` | 1 792 512 |
| `K230_LP4/K230-USIP-EVB-LP4-SCH-V1.1-A.1-20230330.xlsx` | 19 378 |
| `K230_LP4/K230-USIP-EVB-LP4-V1_1-A_1-20230412-DXF.zip` | 110 961 |
| `K230_LP4/K230-USIP-EVB-LP4-V1_1-A_1-20230412-GERBER.zip` | 463 329 |
| `K230_LP4/K230-USIP-EVB-LP4-V1_1-A_1-20230412-PCB.zip` | 1 934 860 |
| `K230_LP4/K230-USIP-EVB-LP4-V1_1-A_1-20230412-SMT.zip` | 687 585 |

Sizes are as reported by the Git tree API at the pinned commit and are exact. **SHA-256 is
unknown** because the files were not downloaded — recorded as unknown rather than omitted.

## Reacquisition — two independent URLs per file

1. **Pinned permalink (preferred, immutable):**
   `https://github.com/kendryte/k230_docs/raw/f8e30213963e0ed5cf995c3cd4701218a45e4793/zh/00_hardware/<path>`
2. **Raw host (branch-tracking, mutable):**
   `https://raw.githubusercontent.com/kendryte/k230_docs/main/zh/00_hardware/<path>`
3. **Rendered documentation site (PDFs only, different host):**
   `https://www.kendryte.com/k230/zh/main/00_hardware/`

Whole-set command, verified as the working enumeration method on 2026-09-04:

```sh
gh api repos/kendryte/k230_docs/git/trees/f8e30213963e0ed5cf995c3cd4701218a45e4793?recursive=1 \
  | python3 -c 'import json,sys; [print(e["size"], e["path"]) for e in json.load(sys.stdin)["tree"] if e["path"].startswith("zh/00_hardware")]'
```

`gh api` is required rather than anonymous `curl` — one recursive tree listing can exhaust the
60/hour anonymous limit, and the resulting 403 looks exactly like a bot block.
