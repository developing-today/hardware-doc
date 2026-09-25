# Scratch relocation — 2026-09-20

`scratch/` was emptied on **2026-09-20**. Its subjects were moved into the archive tier at the
repo-relative path of the record that owns them, or — for authored analysis the repository's own
records depend on — **promoted into this repository**.

**Nothing was deleted.** Every operation was `mv`, every destination was verified by file count
and tree digest, and every destination carries a `README.md` explaining what it holds, when it
was gathered, and what is still owed on it.

This file exists because **~250 references in this repository name a `scratch/…` path** as an
artifact's local location. Those references were left as their authors wrote them — they are
other passes' text, and several are *data about where a file was when it was read*, not
navigation. Use the table below to resolve them.

## How to resolve any `scratch/…` reference

Find the subject in the first column and apply the substitution.

| Reference beginning… | Now at | Notes |
|---|---|---|
| `scratch/preprint-repositories/` | `archive/research/preprint-repositories/` | Subject grouping preserved exactly; nothing renamed |
| `scratch/market-and-certification/shopify/` | `archive/guides/markets/artifacts/vendor-product-catalogues-2026-09-11/` | The only subject that was split |
| `scratch/market-and-certification/` | `archive/guides/research/artifacts/certification-and-market-2026-09-11/` | ⚠ **the 163 exhibit PDFs are not there** — see below |
| `scratch/schematic-tracing/` | `archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/` | |
| `scratch/lora-generations/` | `archive/guides/lora/artifacts/lora-generations-pass-2026-09-04/` | |
| `scratch/esp32-p4-wifi6-touch-lcd-xc/` | `archive/devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/research-scratch/` | |
| `scratch/papermono-plugins-handoff-2026-09-11/` | `archive/software/applications/crosspoint-reader/plugins/papermono-plugins-handoff-2026-09-11/` | |
| `scratch/index-merge/` | **`research/passes/index-merge/`** — *in this repository* | All 33 citing files were rewritten; see below |
| `scratch/cross-cutting-synthesis/` | **`research/passes/cross-cutting-synthesis-2026-09-07/`** — *in this repository* | |
| `scratch/_tmp-sweep-2026-08-26/`, `scratch/workspace/`, `scratch/misc/` | `archive/guides/research/artifacts/tmp-sweeps-2026-08-26/<same name>/` | ⚠ 116 MB of foreign tooling removed — see below |
| `scratch/_rescued-from-tmp-2026-09-20/` | split nine ways — see [the rescue record](archive/guides/research/artifacts/rescued-from-tmp-2026-09-20/README.md) | |

Subjects **not** covered by this pass (`eink-software`, `tanmatsu`, `m5stack-*`, `xteink`,
`lilygo-*`, `zerowriter*`, `waveshare-epaper*`, `xiao-esp32s3-sense`,
`esp32-s3-knob-touch-lcd-1.8`) were relocated by **concurrent sessions** on the same day, to the
same convention: `archive/devices/<vendor>/<product>/artifacts/research-scratch/`.

## The one rewrite that was applied to records

`scratch/index-merge/` → `research/passes/index-merge/` was substituted in **33 files, 90
occurrences**, because those documents were promoted *into* this repository and a repository
record must not depend on a path outside it. Both `scratch/` and `research/` sit at the
repository root, so no `../` depth changed; the edit is a pure string substitution with **zero
lines added or removed**. 36 Markdown links were then resolved against the filesystem: **0
broken**.

Every other `scratch/…` reference in the repository was **left untouched**.

## Where the bulk went, by subject

| Subject | Files | Bytes | Tree digest (verified identical after the move) |
|---|---:|---:|---|
| `preprint-repositories` | 903 | 243,783,241 | `46b31fcd2d337b57f37edbbeee154d7cb4af932c2f06840c12de2f1937cc899b` |
| `_rescued-from-tmp-2026-09-20` | 1,936 | 323,956,202 | `bd4acbfb5f777f22d195468b9bde739b183e998f18321e580af38c6428ec295b` *(split — reconciled per-group)* |
| `_tmp-sweep-2026-08-26` + `workspace` + `misc` | 2,040 + 1,065 + 13 | 81,495,481 + 24,428,090 + 11,961,564 | split: 54 files / 27,671,868 B kept · 3,064 files / 89,213,267 B foreign |
| `market-and-certification` | 54 | 12,367,881 | `17cb1517a44aed28a39e2758b51e7547161de6922e40183be25f5b0fde1d0853` → 48 + 6 after the split |
| `lora-generations` | 147 | 10,897,032 | `f9cb36466c89dade5727ab62b62437648a88a25027aa7982295066c32bf4b223` |
| `esp32-p4-wifi6-touch-lcd-xc` | 23 | 3,065,531 | `ed847572df6c0a232f90f1f20382be97ab9649878e53b252718746793eb611ad` |
| `papermono-plugins-handoff-2026-09-11` | 54 | 499,610 | `11a62e468f936302a9bea43e2940c6f9f9bd1b7e790d811fef13cea467e5cb41` |
| `index-merge` | 12 | 314,480 | `5fbc90c43c33266a99b08c9c86e118fb899b174adae8a99fecabd09344d47700` |
| `schematic-tracing` | 8 | 52,193 | `4c2805ec9a54f6e0129dfcca299bf6bbe8afbb362a8b1cf6d3487865b9a78b19` |
| `cross-cutting-synthesis` | 1 | 4,787 | `dc598e25467377cc4de3ae615ac15e0f9f42cd64954fe9e62f72c82011b06ebd` |

## ⚠ Three things a reader following an old path needs to know

### 1. `scratch/market-and-certification/fcc/<ID>/<exhibit>.pdf` — the exhibits are not there

Roughly 167 references across ~30 device and component records cite those paths. The exhibits
were removed from that directory on 2026-09-20 by a consolidation pass that first proved, **by
SHA-256 on every one of the 163 files**, that each already existed under `devices/` or
`components/`:

```
163 exhibit PDFs across 26 FCC-ID directories
  → in the repository        57
  → in the archive          106
  → in NEITHER                0        (0 bytes unrepresented)
```

71 extracted internal-photo PNGs were also removed after all 71 were regenerated from the source
PDFs and compared byte-for-byte (`pdfimages -png <ID>-internal-photos.pdf int`, poppler 26.06.0).

**So the citation is still resolvable — just not at that path.** Look under the owning record's
`artifacts/certification/`, where either the PDF or its `*.ARCHIVED.md` placeholder sits.

### 2. 116 MB of what was in `scratch/` was never hardware material

Three `/tmp` sweeps between 2026-08-26 and 2026-09-20 copied *everything* loose in `/tmp`, which
included whatever other tooling was running on the host: `hermes_agent` 0.19.0 (a Python CLI, 974
files), two byte-identical copies of `@earendil-works/pi-coding-agent` v0.84.3 (an npm package,
1,044 files each), a nixpkgs maintainer diff, a NixOS build log, a Hyprland configuration session
and two Firefox extensions.

It is **not** in the archive and it is **not** deleted. It is in
`repo-archive/scratch-foreign/`, grouped by where it was found, with a README stating that it is
unidentified third-party tooling of unknown provenance that does not belong to this knowledge
base. Forcing it into `devices/` or `components/` would have been worse than either alternative.

### 3. Several destinations hold **failure specimens under deliberately misleading names**

These are research evidence and must not be "corrected":

| File | Where it is now | The lie |
|---|---|---|
| `ms.pdf`, `sib.pdf`, `p.bin` | `archive/guides/research/artifacts/tmp-sweeps-2026-08-26/_tmp-sweep-2026-08-26/loose-files/` | HTML LCSC pages served with 200 under binary extensions |
| `bq25306.txt` | same | ⚠ Two READMEs call it "extraction failed". It is **139 KB of correct text**; the *claim* is the specimen |
| `dd.html` | same | correctly named — the control |
| `ocr_*.png` / `ocr_*.jpg` | same, and `…/workspace/tmp-sweep/` | JPEG data under `.png` names in two of the three copies |
| `61979758LR2021_V1_1_datasheet.pdf` | `archive/guides/lora/artifacts/lora-generations-pass-2026-09-04/dl/` | A Mouser *"Access to this page has been denied"* page, HTTP 200, `.pdf` name |
| `cf.bin`, `t.bin`, `t2.bin`, `t3.bin`, `t4.bin` | `archive/components/solomon-systech/shared-artifacts/epaper-controller-research-2026-09-11/` | All five are HTML; `t.bin` is a **404 body** |
| `ssd1677.txt`, `ssd1680.txt` | same | Text of the **wrong parts** (SSD1681 and SSD7317) under those names |
| `adobe-eol.html` | `archive/software/applications/crosspoint-reader/plugins/rescued-from-tmp-2026-09-20/bytebooks-platform-transition/` | A 446-byte Akamai *Access Denied* body next to the 139 KB page that succeeded |
| `cn.html` | `archive/guides/research/artifacts/retrieval-specimens-2026-09-11/` | A Zhihu bot-block token page, served 200, containing no article |

## What was promoted into the repository, and why

| Promoted | Files | Why it could not stay outside the repository |
|---|---:|---|
| [`research/passes/index-merge/`](research/passes/index-merge/README.md) | 12 | `corrections-requiring-review.md` is cited by **30 device and component records** as the authority for a dated correction, and the root README's *Research passes* table links the pass report. The archive is machine-local; a cloner never has it |
| [`research/passes/cross-cutting-synthesis-2026-09-07/`](research/passes/cross-cutting-synthesis-2026-09-07/README.md) | 1 | An authored pass report for four repository documents, with its negative results recorded nowhere else |

Both are small (319 KB combined) and entirely authored text plus the six reproducibility scripts
the report links. The **bulky** evidence for index-merge round two — 314 files, 60 MB of pre-edit
snapshots and renders — stayed in the archive at
[`archive/research/passes/index-merge/round-two-workdir-2026-09-11/`](archive/research/passes/index-merge/round-two-workdir-2026-09-11/README.md).

## Open items this relocation did **not** close

Moving a file is not doing the work. These were pending before and are pending now:

- **`archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/index-fragments.md`**
  — proposed index edits, still unapplied, for the third pass running.
- **The Stanford CS Technical Reports index** (`st.html`) — the last outstanding archival
  candidate in `research/preprint-repositories/retrieval-notes.md` §9. Now filed beside its
  subject; still not verified against CDX, still not written into the record.
- **1,177 extracted URLs** for the deferred preprint link-validation task — preserved, not run.
- **FCC internal photographs are extracted but barely mined.** Outside `papermono`, the phrase
  "internal photo" appears 0–2 times in the certification records for the five filings whose
  photographs were extracted. A part census from them would be high value.
- **The ST25R3916 driver has not been audited against its datasheet.** The corpus gathered to
  enable it is at `archive/components/stmicroelectronics/st25r3916/artifacts/`.
- **Four unfetched PaperMono radio test reports** (main, Wi-Fi 5 MB, BLE 2.8 MB, LoRa 1.8 MB) —
  the only route to per-channel EIRP, band-edge compliance and the **LoRa duty cycle**. Skipped
  by `harvest.py`'s `MAX_TEST_REPORTS = 1`.
- **Nothing in `archive/devices/m5stack/papermono/artifacts/research-scratch/rescued-from-tmp-2026-09-20/`
  has been read end to end.** It was rescued from `/tmp` and filed on the same day.
