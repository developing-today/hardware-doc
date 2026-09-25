# KeebDeck Basic — reference-board schematic and KiCad source

Solder Party's **KeebDeck Basic** evaluation board — the reference design for driving a KeebDeck
keypad. The Tanmatsu does **not** ship this board; it is prior art for the Tanmatsu's own keyboard
section.

| | |
|---|---|
| `keebdeck-basic-schematic-rev1.1.pdf` | the exported schematic — filed 2026-09-20, mined in [`../../keyboard.md` §2b](../../keyboard.md) |
| `kicad/` | **the EDA source it was exported from** — added 2026-09-20, see §"KiCad source" |
| `mechanical/` | STEP models — **archived** 2026-09-20, placeholders in place |
| `LICENSE-CERN-OHL-v1.2.md` | upstream `LICENSE.md` — **read 2026-09-20**, see the correction below |
| `upstream-README.md` | upstream `README.md` |

## The PDF

`keebdeck-basic-schematic-rev1.1.pdf`

| Field | Value |
|---|---|
| What it is | Schematic of the **Solder Party KeebDeck Basic** evaluation board — the reference design for driving a KeebDeck keypad |
| Upstream repository | <https://github.com/solderparty/keebdeck_basic_hw> |
| Commit | **`2b537ce`** — commit subject *"Rev 1.1 - Production"* |
| Member path in repo | `schematics.pdf` |
| Source file | `keebdeck_basic.kicad_sch`, exported by KiCad E.D.A. **9.0.1** (Eeschema-PDF) |
| PDF `CreationDate` | **2025-05-04** |
| Title-block `Date:` / `Rev:` | **blank** — the "Rev 1.1" label comes from the Git commit only |
| Bytes | **355 080** |
| SHA-256 | `593aa32d45e70aaa331f82b558a5675666e5bd2d0f7f9584e36abfbb66b8b0a4` |
| Pages | 1 (A4 landscape, 841.896 × 595.296 pt) |
| Retrieved | **2026-08-24** (with the rest of the Tanmatsu source clones) |
| Filed here | **2026-09-20** |
| Renamed | from `schematics.pdf` → `keebdeck-basic-schematic-rev1.1.pdf` |
| Licence | **CERN Open Hardware Licence v1.2** — ✅ **resolved 2026-09-20**, see the correction below |
| Redistribution status | `conditional` — CERN-OHL v1.2 requires notice and licence retention |
| Disposition | `repository` |

> ### ✅ Correction — the licence is now known
>
> This record previously said: *"**unknown** — the upstream repo ships a `LICENSE.md` that was
> **not read** in this pass. The sibling `keebdeck_keyboard_hw` is CERN-OHL v1.2; do **not** assume
> the same applies here."* That caution was correct procedure and is now discharged.
>
> `LICENSE.md` (9 121 B) **was read on 2026-09-20** and is the **CERN Open Hardware Licence
> v1.2** — the same licence as `keebdeck_keyboard_hw` after all. It is retained here as
> `LICENSE-CERN-OHL-v1.2.md`.
>
> ⚠ The file contains **mojibake**: typographic quotes appear as `?` replacement characters
> (`?Licence? means this CERN OHL`). That is how upstream ships it — the bytes were **not**
> altered. It does not affect the licence's identity, which is stated in plain ASCII on line 1.

## Why this is a copy, not a move

`scratch/tanmatsu/sources/keebdeck_basic_hw/` is a **complete, unmodified `git` checkout** at
`2b537ce` (`git status` clean, 2026-09-20). Moving one file out of it would break a reproducible
upstream snapshot for no benefit, so the file was **copied** and the checkout left intact. The
same treatment was given to `keebdeck_keyboard_hw/dimensions.pdf` in the 2026-08-24 pass.

## What was mined out of it

See [`../../keyboard.md` §2b](../../keyboard.md#2b-verified-the-keebdeck-basic-reference-board-read-from-its-schematic).
The headline findings:

- The reference board is a **6 × 12 / 71-key** matrix, **not** the 6 × 13 the finished KeebDeck
  keypad and the Tanmatsu use.
- **No diodes in the matrix.** Ghosting is mitigated by swapping the TAB and E columns, per a
  note on the sheet.
- The **whole backlight block and the boot button are marked DNP**.
- **`ROW3` is `BOOT0`**, and **`COL0`/`COL1` are `SWDIO`/`SWCLK`** — three pins that are both
  matrix lines and system-critical.

## Re-acquisition

```bash
git clone https://github.com/solderparty/keebdeck_basic_hw
git -C keebdeck_basic_hw checkout 2b537ce
sha256sum keebdeck_basic_hw/schematics.pdf
# expect 593aa32d45e70aaa331f82b558a5675666e5bd2d0f7f9584e36abfbb66b8b0a4
```

Reacquisition status: **automatic**. Verified present at that commit on **2026-09-20** from the
local checkout; the GitHub URL was **not** re-probed in this pass.

---

## KiCad source · *added 2026-09-20*

The PDF above is an export. These are the files it was exported from — primary, load-bearing EDA
source, so they belong in the repository rather than the archive.

| File | Bytes | SHA-256 (first 16) |
|---|---:|---|
| `kicad/keebdeck_basic.kicad_sch` | 519 853 | `cc0ce3ffbe3693c6…` |
| `kicad/keebdeck_basic.kicad_pcb` | 2 928 754 | `39b66d2d24ff7a37…` |
| `kicad/keebdeck_basic.kicad_pro` | 16 331 | `4782c9f31bb75540…` |
| `kicad/keebdeck_basic_faceplate.kicad_pcb` | 379 374 | `141f51ef272c238b…` |
| `kicad/keebdeck_basic_faceplate.kicad_pro` | 14 179 | `14ce7942a8c5a528…` |
| `kicad/fp-lib-table`, `kicad/sym-lib-table` | 647 / 611 | library tables |

`keebdeck_basic.kicad_pcb` carries **resolved net names on every pad**, so it — not the PDF, and
not the `.kicad_sch` — is the authoritative statement of this board's connectivity. Re-parse with:

```bash
python3 tools/kicad_pcb_nets.py \
  devices/nicolai-electronics/tanmatsu/artifacts/keebdeck-basic/kicad/keebdeck_basic.kicad_pcb --all
```

### Not copied here

| Left in `scratch/tanmatsu/sources/keebdeck_basic_hw/` | Why |
|---|---|
| `fp-info-cache` (3 950 153 B) | KiCad footprint-index cache — regenerated on open |
| `library/`, `modules/`, `keebdeck_keyboard_hw/` | Git submodule/vendored library trees; the keypad library is already filed at [`../keebdeck-keyboard/`](../keebdeck-keyboard/README.md) |
| `img/basic.jpg` | Product photo, not needed for the electrical record |

## Mechanical models · **archived** 2026-09-20

| File | State | Bytes |
|---|---|---:|
| ~~`mechanical/keebdeck_basic.step`~~ | **archived** → `mechanical/keebdeck_basic.step.ARCHIVED.md` | 46 777 091 |
| ~~`mechanical/keebdeck_basic_faceplate.step`~~ | **archived** → `mechanical/keebdeck_basic_faceplate.step.ARCHIVED.md` | 2 846 452 |

Geometry only, for a board the Tanmatsu does not ship — the clearest possible archive case. Both
placeholders carry SHA-256, byte size, commit `2b537ce`, tag `rev1.1`, author, licence and two
independent recovery URLs, and stand alone without the archive.

## Why these are copies, not moves

Unchanged from the reasoning above: `scratch/tanmatsu/sources/keebdeck_basic_hw/` is a **clean,
unmodified checkout** at `2b537ce` (`git status` clean, 2026-09-20). Every file here was verified
**byte-identical by SHA-256** to its scratch counterpart at copy time; the STEP files were then
archived out of the repository by `tools/archive_artifact.py`, which re-verified content by
fingerprint after the move.
