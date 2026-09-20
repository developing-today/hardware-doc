# Canaan Kendryte K230 — retained chip documents

Seven Markdown documents retrieved **2026-09-04** from `github.com/kendryte/k230_docs` at commit
**`f8e30213963e0ed5cf995c3cd4701218a45e4793`** (2025-09-12). Hashes and sizes: `SHA256SUMS`.

```sh
sha256sum -c SHA256SUMS       # expect 7 × OK
```

| File | Bytes | Upstream path (under `en/`) |
|---|---:|---|
| `K230_datasheet-v1.0-2023-07-06.md` | 83 002 | `00_hardware/K230_datasheet.md` |
| `K230_brief_datasheet.md` | 7 781 | `K230_brief_datasheet.md` — **tree root, not `00_hardware/`** |
| `K230_Hardware_Design_Guide.md` | 49 061 | `00_hardware/K230_Hardware_Design_Guide.md` |
| `K230_PMU_User_Guide.md` | 10 039 | `01_software/board/osdrv/K230_PMU_User_Guide.md` |
| `K230_nncase_Development_Guide.md` | 81 128 | `01_software/board/ai/K230_nncase_Development_Guide.md` |
| `K230_RVV_In_Action.md` | 12 528 | `02_applications/tutorials/K230_RVV_In_Action.md` |
| `K230_RVV_optimization_performance_description.md` | 12 004 | `02_applications/tutorials/K230_RVV_optimization_performance_description.md` |

Renames: only `K230_datasheet.md` → `K230_datasheet-v1.0-2023-07-06.md`, to carry the document
revision and date in the filename. Contents are byte-identical to upstream.

## ⚠ These are bundled upstream Markdown — their image links do not resolve here

Every one of these files contains image references written **relative to the upstream repository
layout**, mostly pointing into the **`zh/`** tree (Canaan keeps one copy of the images and both
language trees reference it):

```
../../zh/00_hardware/images/K230_block_diagram.png
../../../../zh/01_software/board/osdrv/images/pmu_hw_top_view.jpg
images/K230_application_1.png
```

**80 such links exist across the seven files and none of them resolves locally.** That is
expected, not a defect: the images were not retrieved, and rewriting upstream Markdown would
break byte-identity with the pinned commit and invalidate `SHA256SUMS`.

**Link checks over this repository must exclude `components/canaan/k230/artifacts/*.md`**, or
report 80 false positives. Authored files in this repository are link-checked; bundled upstream
Markdown is not.

To view the images, use the rendered build:
`https://www.kendryte.com/k230/en/main/00_hardware/K230_datasheet.html`, or fetch them from
`https://github.com/kendryte/k230_docs/raw/f8e30213963e0ed5cf995c3cd4701218a45e4793/zh/00_hardware/images/…`.

## Licence

The repository is **BSD-2-Clause**; the documents inside carry a Canaan notice reading "without
the written permission of the company, any unit or individual shall not disseminate part or all
of the content of this document in any form." **These conflict.** Recorded, not resolved. All
seven files are held **unstaged** pending a user decision — see the
[component README §18](../README.md#18-licensing).

## Not retained

[`CANAAN-EDA-SET.md`](CANAAN-EDA-SET.md) — 22 Canaan **reference-board** EDA and PDF files
(~19 MB) enumerated with exact byte sizes and reacquisition URLs. They are only in the `zh/`
tree, and they describe Canaan's own boards, not the LilyGO one.
