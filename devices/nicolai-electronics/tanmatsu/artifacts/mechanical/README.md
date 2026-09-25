# Tanmatsu mechanical design files

Source: **`Nicolai-Electronics/tanmatsu-mechanical`** @
`c623cd548c9cafb95773624fe775001984449a89` (tag `release-5-3-gc623cd5`, Renze Nicolai,
2026-07-03). Licence **CERN-OHL-P**; branding and artwork are explicitly excluded from that
licence. Cloned 2026-08-26, filed 2026-09-20.

Narrative: [`../../mechanical-and-case.md`](../../mechanical-and-case.md) ·
measured dimensions: [`../../pricing-and-dimensions.md`](../../pricing-and-dimensions.md)

## What is here

| File | State | Bytes | Notes |
|---|---|---:|---|
| `upstream-README.md` | in repo | 2 443 | Upstream `README.md`, renamed |
| `mechanical-repo-README.md` | in repo | 2 431 | Earlier pass's copy of the same upstream README — retained, see below |
| ~~`tanmatsu.step`~~ | **archived 2026-09-20** | 34 064 711 | Whole-device STEP assembly → `tanmatsu.step.ARCHIVED.md` |
| ~~`frontpanel.step`~~ | **archived 2026-09-20** | 11 383 533 | Front-panel STEP → `frontpanel.step.ARCHIVED.md` |
| ~~`Tanmatsu_3D-printed.FCStd`~~ | **archived 2026-09-20** | 16 282 079 | FreeCAD case source → `Tanmatsu_3D-printed.FCStd.ARCHIVED.md` |
| ~~`Tanmatsu_3D-printed-ebyte.FCStd`~~ | **archived 2026-09-20** | 20 422 380 | FreeCAD case source, Ebyte LoRa variant → `Tanmatsu_3D-printed-ebyte.FCStd.ARCHIVED.md` |

Each archived file leaves a `*.ARCHIVED.md` placeholder carrying SHA-256, byte size, upstream
commit, author, licence and recovery URLs, plus a relative symlink through the repository's
`archive/` link so a checkout that *does* hold the archive behaves as though nothing moved.
**The placeholders stand alone** — a clone without the archive can still reacquire every file.

> `mechanical-repo-README.md` and `upstream-README.md` are the **same upstream document at
> different commits** — 2 431 vs 2 443 bytes, different SHA-256. Both retained per the
> near-duplicate rule: differing bytes under one name is a finding, not redundancy. The 2 443-byte
> copy is the one at `c623cd5`.

## Why these were archived rather than kept

Per [`SIZE-AUDIT.md`](../../../../../SIZE-AUDIT.md), STEP meshes and enclosure CAD are in the
archivable category. They are **geometry only** — no netlist, no pin assignment, no electrical
data — and the single fact this repository draws from them is already extracted:

> The **~114.9 mm mainboard width** in [`../../pricing-and-dimensions.md`](../../pricing-and-dimensions.md)
> was measured from `tanmatsu.step` with `tools/step_bbox.py`. It is **not vendor-published**.

Applying the skill's test — *if the archive were deleted tomorrow, what would the repository still
know?* — the answer is: the measured dimensions, the case revision history, the FreeCAD workflow
and the front-panel fabrication specifications. That is everything these files were consulted for.

The `.FCStd` files are **source**, not derived output, and are archived for **size alone**. They
are the parametric originals; `tools/freecad_export.py` upstream regenerates the STEP exports from
them.

## Not brought into the repository

| Left in `scratch/tanmatsu/sources/tanmatsu-mechanical/` | Why |
|---|---|
| `tools/export_manufacturing_files.sh`, `tools/freecad_export.py` | Small upstream build scripts; reproducible, and the workflow is described in `mechanical-and-case.md` |
| `tools/test_freecad_file.FCStd` | CI fixture, not a design file |
| `.github/workflows/*.yml` | Upstream CI configuration |

The scratch clone is a **clean, unmodified checkout** at `c623cd5` (`git status` clean,
2026-09-20) and was deliberately left intact: the files above were **copied** into the repository
and then archived from there, so the reproducible upstream snapshot is not damaged. Every copy was
verified byte-identical by SHA-256 before the archive move, and `archive_artifact.py` re-verified
content by fingerprint after it (**7/7 verified**).

---

> **Link-check exclusion.** `upstream-README.md` and `mechanical-repo-README.md` are **vendored
> upstream Markdown** and are excluded from this repository's relative-link check. Both contain a
> `LICENSE` link that resolves in the upstream repository but not here, because the licence text
> lives at [`../schematics/LICENSE-CERN-OHL-P`](../schematics/LICENSE-CERN-OHL-P) (the same
> CERN-OHL-P text covers both repositories). The upstream bytes were **not** modified to fix it.
