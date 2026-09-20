# Vendor documentation sourcing — Canaan Creative (Kendryte)

**Compiled 2026-09-04** while researching the [Kendryte K230](../../components/canaan/k230/README.md)
for the [LilyGO T-Display K230](../../devices/lilygo/t-display-k230/README.md). First Canaan
part in this repository.

Canaan Creative Co., Ltd (嘉楠科技, NASDAQ: **CAN**) publishes its Kendryte SoC documentation in a
way that is unusual enough to be worth writing down once: **as Markdown in a public Git
repository**, not as PDFs behind a portal. Everything below is live-verified on the stated date.

---

## 1. Which host serves what

| Host | Serves | Stability |
|---|---|---|
| `github.com/kendryte/k230_docs` | **The canonical documentation.** Markdown sources, images, and binary EDA artifacts | High — commit-pinnable |
| `raw.githubusercontent.com/kendryte/k230_docs/main/…` | Raw file fetch | High, but `main` moves |
| `www.kendryte.com/k230/<lang>/<branch>/…` | Rendered HTML build of the same repository | Medium — URL shape encodes a branch name |
| `developer.canaan-creative.com` | Developer community; **prebuilt SDK images** under *K230 → Images*; `/resource` index | Medium — SPA-ish, requires navigation |
| `canaan-creative.com` | Corporate site | Marketing only |
| `salesAI@canaan-creative.com` | The **only** sales channel printed in the datasheet | — |

Prefer the repository. It is the source the rendered site is built from, it can be pinned to a
commit, and it contains files the rendered site does not expose.

## 2. URL templates that work

```sh
# Pinned permalink — always prefer this in citations
https://github.com/kendryte/k230_docs/blob/<SHA>/<path>
https://github.com/kendryte/k230_docs/raw/<SHA>/<path>

# Branch-tracking raw fetch — fine for a one-off, wrong for a citation
https://raw.githubusercontent.com/kendryte/k230_docs/main/en/00_hardware/K230_datasheet.md

# Rendered HTML
https://www.kendryte.com/k230/en/main/00_hardware/K230_datasheet.html
https://www.kendryte.com/k230/zh/main/00_hardware/
```

**Enumerate everything published for a product in one call:**

```sh
gh api repos/kendryte/k230_docs/git/trees/main?recursive=1 \
  | python3 -c 'import json,sys;[print(e["size"],e["path"]) for e in json.load(sys.stdin)["tree"] if e["type"]=="blob"]'
```

Use `gh api`, not anonymous `curl`. One recursive tree listing of this repository returns 837
entries and can exhaust the 60/hour anonymous GitHub limit; the resulting 403 carries
`X-RateLimit-Remaining: 0` and **looks exactly like a bot block**. Check that header before
rotating User-Agents — no User-Agent helps, because `api.github.com` limits per identity.

## 3. The trap that matters most: `en/` is not a translation of `zh/`

**The English tree contains no binary hardware artifacts. The Chinese tree does.**

Verified 2026-09-04 at commit `f8e30213963e0ed5cf995c3cd4701218a45e4793`:

| | `en/00_hardware/` | `zh/00_hardware/` |
|---|---|---|
| Datasheet Markdown | yes | yes |
| Hardware design guide | yes | yes |
| **Board schematics (PDF)** | **none** | `K230-DEMO-BOARD-SCH.pdf`, `K230-SIP-EVB-…pdf`, `CanMV-K230-V1.0_2023-09-15.pdf` |
| **OrCAD `.DSN` sources** | **none** | three, 1.7–1.85 MB each |
| **Gerber / PCB / DXF / SMT / BOM** | **none** | full sets for LP3, LP4 and K230D SiP EVB |

An agent that searches only `en/` will report "Canaan publishes no schematics". That conclusion
is wrong, and it is an easy mistake because the two trees have parallel directory names. **Always
list `zh/` as well**, even when you cannot read the prose. Enumerated inventory with sizes:
[`components/canaan/k230/artifacts/CANAAN-EDA-SET.md`](../../components/canaan/k230/artifacts/CANAAN-EDA-SET.md).

## 4. Document-class checklist for a Kendryte part

Tick these off before declaring a sourcing pass complete. Status column is for **K230 as of
2026-09-04**.

| Class | Expected path | K230 status |
|---|---|---|
| Full datasheet | `en/00_hardware/K230_datasheet.md` | ✅ V1.0, 2023-07-06 |
| Brief datasheet | `en/K230_brief_datasheet.md` | ✅ (note: **not** under `00_hardware/`) |
| Hardware design guide | `en/00_hardware/K230_Hardware_Design_Guide.md` | ✅ |
| **Pinout / ball map** | `《K230_PINOUT_V1.0_20230524》` | ❌ **cited by the datasheet, not published** |
| **Errata** | — | ❌ **none published** |
| Reference-board resource guide | `en/00_hardware/K230_DEMO_BOARD_Resource_Usage_Instructions.md` | ✅ |
| SDK user manual | `en/01_software/board/K230_SDK_User_Manual.md` | ✅ |
| Per-subsystem API references | `en/01_software/board/mpp/*` | ✅ — Audio, DMA, DPU, FFT, GPU, VICAP, video codec, video output, system control, non-AI 2D |
| Driver API references | `en/01_software/board/osdrv/*` | ✅ — big-core and little-core driver APIs, DRM, PMU |
| Boot / flashing tool guide | `en/01_software/pc/burntool/K230_SDK_Burntool_User_Guide.md` | ✅ |
| ISP tuning | `en/01_software/pc/ISP_tuning/*` | ✅ |
| nncase / AI toolchain | `en/01_software/board/ai/K230_nncase_Development_Guide.md` | ✅ |
| nncase↔SDK version table | `en/03_other/K230_SDK_nncase_version_correspondence.md` | ✅ — **read this before compiling any model** |
| Release notes | `en/03_other/K230_SDK_Release_Notes.md` | ✅ |
| FAQ set | `en/03_other/K230_FAQ.md`, `K230_SDK_FAQ_C.md`, … | ✅ |

Two of those are the ones to remember: **no pinout document and no errata document**. Both are
absences confirmed by full recursive listing, not by a failed search.

## 5. Licence conflict — expect it, record it

The `k230_docs` repository is licensed **BSD-2-Clause** (GitHub's licence detection, repository
metadata). The datasheet inside it carries:

> "This document is only suitable for the development and design of K230 platform, without the
> written permission of the company, any unit or individual shall not disseminate part or all of
> the content of this document in any form."

These cannot both be true of the same bytes. Canaan appears to have applied a standard corporate
notice to a document it then released permissively and never reconciled the two. **Record the
conflict; do not pick a side.** Retained copies in this repository are held **unstaged**.

## 6. Repositories worth knowing

| Repository | Branch | Licence | Purpose |
|---|---|---|---|
| `kendryte/k230_docs` | `main` | BSD-2-Clause | Documentation (above) |
| `kendryte/k230_sdk` | `main` | BSD-2-Clause | Original dual-OS SDK (RT-Smart on CPU1 + Linux on CPU0). Docker image `ghcr.io/kendryte/k230_sdk`. Last push 2025-09-12. |
| `kendryte/k230_linux_sdk` | **`dev`** | BSD-2-Clause | **Linux-only** SDK, actively maintained. Note the default branch is `dev`, not `main` — a `main` clone gets nothing. |
| `kendryte/canmv_k230` | `canmv_k230` | none declared | MicroPython. **Default branch is `canmv_k230`**, another non-obvious name. |

**Non-default branch names are this vendor's recurring trap.** Three of four repositories use a
default branch that is neither `main` nor `master`. Always read `.default_branch` from the API
rather than assuming.

## 7. Getting prebuilt images

`developer.canaan-creative.com` → *K230* → *Images*. LilyGO's wiki cites the same path
(`https://developer.canaan-creative.com/resource`). This is the route for a factory-style
recovery image when you do not want to build the SDK. Not retrieved in this pass; access
behaviour and whether a login is required are **unverified**.

## 8. Products that produced these findings

- [Kendryte K230](../../components/canaan/k230/README.md) — component record
- [LilyGO T-Display K230](../../devices/lilygo/t-display-k230/README.md) — device record
