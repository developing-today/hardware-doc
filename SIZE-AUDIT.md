# Size audit — ``

> Where the megabytes are, what can be regenerated, and what must stay.
> Measured **2026-08-24**. Total: **442 MB on disk / 429.5 MB in 3,322 files**.

## Executive summary

| Verdict | Bytes | What |
|---|---:|---|
| **Keep — irreplaceable or high-friction to re-obtain** | ~285 MB | Vendor PDFs, firmware binaries, EDA sources |
| **Keep — cheap and high-value** | ~15 MB | 490 authored `.md`, tools, manifests |
| **Prunable — pure duplication** | **0 MB** | None. `shared-assets/` is a working symlink pool — see §5 |
| **Prunable — regenerable outputs** | ~13 MB | Gerbers (~8 MB) regenerable from retained `.kicad_pcb`; see §6 |
| **Already pruned this session** | 950 MB | 29 archive placeholders (STEP, panels, docs build) |

**The tree is in good shape — there is no duplication to remove.** The bulk is vendor documentation that is genuinely worth holding, and an existing symlink pool is already deduplicating the working tree.

---

## 1. Where the bytes are

### By area

| Area | Size | Note |
|---|---:|---|
| `components/` | **199 MB** | Datasheets and TRMs — the largest area by far |
| `devices/` | **235 MB** | Per-board artifacts |
| `shared-assets/` | 6.1 MB | ⚠ see §5 |
| `vendors/` | 872 KB | Sourcing guides |
| `guides/` | 504 KB | Reusable how-tos |
| `tools/` | 20 KB | |

### By file type

| Type | MB | Files | Share | Reproducible? |
|---|---:|---:|---:|---|
| **`.pdf`** | **238.3** | 154 | **55.5 %** | Usually — but see §2 |
| `.png` | 45.1 | 171 | 10.5 % | Mostly |
| `.kicad_pcb` | 30.7 | 9 | 7.1 % | ✅ from pinned commits |
| `.zip` | 21.0 | 37 | 4.9 % | Mixed |
| **`.bin`** | 16.4 | 19 | 3.8 % | ❌ **no** |
| `.dxf` | 12.0 | 8 | 2.8 % | ✅ |
| `.jpg` | 8.4 | 519 | 2.0 % | Mostly |
| `.kicad_sch` | 7.3 | 42 | 1.7 % | ✅ |
| **`.md`** | 6.9 | **490** | 1.6 % | ❌ **authored — the point of the repo** |
| `.html` | 6.4 | 46 | 1.5 % | Sometimes (bot-blocked sites) |

**The 490 authored Markdown files are 1.6 % of the tree.** Everything else is evidence supporting them.

### Largest single files

| MB | File | Verdict |
|---:|---|---|
| 22.4 | `espressif/esp32-p4` TRM | **keep** — 1,500 pp primary reference |
| 15.6 | `sitronix/st77916` spec | **keep** — Sitronix does not publish this publicly |
| 14.5 | `espressif/esp32-s3r8` TRM | **keep** |
| 13.9 | ESP32-S3 TRM **v1.2 Waveshare mirror** | **keep** — different revision (1,477 pp vs 1,531 pp) |
| 10.1 | `tanmatsu.kicad_pcb` | **keep** — netlist source |
| 9.7 ×2 | ESP32 TRM + v5.4 mirror | **keep** — 784 pp vs 779 pp, different revisions |
| 9.4 | `ilitek/ili9881c` spec | **keep** — not publicly published |
| 4.9 | XIAO fruits-classify `.zip` | ⚠ **candidate** — Edge Impulse export, regenerable |
| 4.9 | `XIAO_ESP32-S3_Sense_front_pinout.png` | ⚠ **candidate** — vendor CDN, re-downloadable |
| 4.0 | `zw_latest.merged.bin` | **keep** — ❌ not reproducible |
| 4.1 / 4.0 | Inkplate 5 / Gen 2 `.kicad_pcb` | **keep** — source of all pinout work |

---

## 2. PDFs — 55 % of the tree, and mostly justified

**195 MB of the 238 MB sits in `components/`.** These are datasheets, technical reference manuals and hardware design guidelines.

The instinct is to prune them as "just re-downloadable". **Resist it**, for reasons this research pass documented directly:

- **Sitronix ST77916 and Ilitek ILI9881C (25 MB combined) are not publicly published by their manufacturers.** Both were obtained from *downstream* mirrors (`dl.espressif.com`, Waveshare) — the silicon vendors keep them behind NDA or customer login. If those mirrors rotate, the documents are gone.
- **Espressif rotates slugs and soft-404s.** The vendor guide records slugs that break (`esp32-mini-1_esp32-mini-1u_datasheet_en.pdf` soft-404s while `esp32-mini-1_datasheet_en.pdf` works), and a doc platform that returns a 13,745-byte JS shell for everything.
- **The mirrored TRM pairs are different revisions, not duplicates** — verified by page count. Keeping both is correct: firmware behaviour differs between silicon revisions.

**Verdict: keep all component PDFs.** This is the highest-value content in the repository per byte, and the hardest to re-obtain.

---

## 3. Not reproducible — keep unconditionally

| Category | Size | Why |
|---|---:|---|
| **Firmware `.bin`** | 16.4 MB | **ESP-IDF builds are not byte-reproducible.** Rebuilding from source will not recreate these images. `zw_latest.merged.bin`, XIAO `CameraWebServer.bin`, ZeroWriter 1.24–1.3 |
| **Authored `.md`** | 6.9 MB | The research itself |
| **Bot-blocked HTML** | ~1 MB | Crowd Supply updates, `zerowriter.ink` pages. Kickstarter already 403s every UA; these are snapshots of pages that may vanish |
| **Vendor PDFs with no public source** | ~25 MB | ST77916, ILI9881C |

Firmware binaries are the clearest case: a 4 MB `.bin` that cannot be regenerated from its own source tree is exactly what an archive is for.

---

## 4. Reproducible from pinned commits — keep, but they're the fallback tier

| Category | Size | Recovery |
|---|---:|---|
| `.kicad_pcb` / `.kicad_sch` | 38 MB | `codeload.github.com/<repo>/tar.gz/<commit>` |
| `.dxf` | 12 MB | Vendor CDN or KiCad export |
| Gerbers (`.gto`/`.gtl`/…) | ~8 MB | **Generated from the retained `.kicad_pcb`** |

**These are worth keeping** because they are the primary evidence behind every pinout and BOM table — but if space ever became critical, gerbers are the first thing to go, since they are mechanically derivable from files already retained.

⚠ One caveat on "reproducible": it assumes the upstream repo still exists. `zerowriter.com` going dark this year is a reminder that pinned commits protect against *drift*, not *deletion*.

---

## 5. `shared-assets/` — working correctly (I got this wrong first time)

**Correction.** My first pass reported this pool as 6.1 MB of pure duplication. **That was a measurement error on my part**: my duplicate detector opened files with Python's `open()`, which *follows symlinks*, so every symlink pointing into the pool was hashed as though it were an independent copy of the content.

Re-measured with `os.path.islink()` skipped:

```
genuine duplicate sets across the repository root: 0
wasted bytes:                               0
```

The pool is a **symlink-based content-addressed store**, built by [`tools/dedupe_shared_assets.py`](tools/dedupe_shared_assets.py), and the migration **was** applied — there are **154 symlinks** in the tree pointing into it. For example:

```
components/chipsemi/chsc5816/artifacts/chsc5816-datasheet-v1-20221114-zh.pdf
  -> ../../../../shared-assets/670808e30541-chsc5816-datasheet-v1-20221114-zh.pdf
```

**5.9 MB across 48 pooled entries, with 154 references** — so it is saving several megabytes of working-tree space, not wasting it. `manifest.json` is the pool's own index and is regenerable (`--reindex`).

### One caveat worth knowing

**Git deduplicates identical content anyway.** Verified — the pool entry and a symlinked location produce the same blob hash, so in the *object store* the pool saves nothing:

```
pool blob:     3fd72191eb66b4892e0c5363297d428ebd129366
original blob: 3fd72191eb66b4892e0c5363297d428ebd129366   ← same
```

The saving is real but confined to the **working tree** — which is still worthwhile for a 442 MB checkout, and it also makes the shared provenance explicit rather than implicit.

**Verdict: leave it alone.** Nothing to prune here.

### Lesson for future audits

Any duplicate-detection or size-accounting pass over this tree **must skip symlinks**, or it will double-count 154 files and report phantom waste. `du` handles this correctly by default; naive Python/`find -type f` walks do not.

## 6. Prunable candidates — ~13 MB, none urgent

With duplication ruled out (§5), what remains is regenerable output. Ordered by confidence:

| Candidate | Size | Assessment |
|---|---:|---|
| Gerber sets (`.gto`/`.gtl`/`.gbr`/…) | ~8 MB | ✅ **Mechanically regenerable** from the retained `.kicad_pcb`. The safest cut if space is ever needed |
| `xiao-esp32s3-fruits-classify_inferencing.zip` | 4.9 MB | ⚠ Edge Impulse export. Regenerable *only if* the project is still public — not verified |
| Large vendor pinout PNGs (4.9 + 2.5 + 2.5 MB) | ~10 MB | ⚠ Re-downloadable from Seeed's CDN **today**. Seeed is documented in this repo as rotating URLs and crossing document IDs — I would keep these |

**Recommendation: prune nothing right now.** 442 MB is not a problem, everything is either irreplaceable or cheap insurance against the vendor-rotation failures this repository has repeatedly documented. Revisit gerbers first if that changes.

Note the CH340 datasheet appearing at three paths is **not** duplication — two of the three are symlinks into `shared-assets/`.

## 7. Already pruned this session — 950 MB

For context on what was removed rather than kept:

| Pass | Size | Content |
|---|---:|---|
| Inkplate docs `build/` + images | 670 MB | Generated Sphinx output + doc photos |
| Off-board Arduino examples | 122 MB | Examples for Inkplate 2/6/10/13, not the 5 |
| XIAO bulk (firmware images, STL, LaTeX) | 108 MB | |
| STEP models, panelisation, enclosure CAD | 158 MB | Mechanical only |

All 29 have `.ARCHIVED.md` placeholders carrying SHA-256, size, commit, author, licence and multiple recovery URLs, and all **29 resolve to real archive paths** (verified).

---

## Method

```bash
du -sh */ | sort -h                      # areas
find the repository root -type f -printf '%s\t%p\n' | sort -rn | head -40   # largest files
# type aggregation + cross-tree duplicate detection: ad-hoc python, SHA-256 keyed
python3 tools/archive_artifact.py --repo-root . --manifest <m> --verify   # placeholder integrity
```

Duplicate detection hashed every file ≥ 64 KB across the whole tree. PDF revision comparison used `pypdf` page counts, not filenames.
