# ZeroWriter Ink source snapshot — provenance against upstream

> What in `artifacts/source-snapshots/zerowriter_ink/` is, and is not, byte-identical to
> `zerowriter/zerowriter_ink` at commit `996207aca0677300ed5f1fdf762d9c9ec79f516e`.
>
> Established **2026-09-20** by a full file-by-file SHA-256 comparison of the repository tree
> (including its archived members) against a byte-exact extraction of the upstream tarball held in
> [`archive/devices/zerowriter/zerowriter-ink/artifacts/provenance-2026-08-30/`](../../../archive/devices/zerowriter/zerowriter-ink/artifacts/provenance-2026-08-30/README.md).
> Evidence label: **executed-success** — every number below was computed, none inferred.

## The headline

**The snapshot is semantically complete and semantically unmodified — but it is no longer
byte-identical to upstream, and published claims that it is are stale.**

| Class | Files | Bytes | Meaning |
|---|---:|---:|---|
| **IDENTICAL** | 89 | 27,181,466 | SHA-256 matches upstream exactly |
| **EOL-ONLY** | 36 | 32,165,119 | differs *only* by CRLF → LF; content otherwise byte-for-byte equal |
| **TRAILING-WS-ONLY** | 14 | 26,313,416 | differs *only* by trailing whitespace stripped from line ends |
| **REAL-DIFF** | **0** | 0 | **no semantic difference anywhere in the tree** |
| **MISSING-IN-REPO** | 13 | 27,268,752 | KiCad `*-backups/` ZIPs — archived, see below |
| **total upstream** | **152** | | |

So: **50 of 152 files were rewritten in place by a normalisation pass**, and 0 files differ in
content. Nothing was lost; but any hash the repository records for those 50 files will **not**
match a fresh upstream checkout, and `diff -rq` against upstream **will** report them.

### When it happened

File mtimes in the repository snapshot fall into three groups:

| mtime | Files | What |
|---|---:|---|
| `2026-05-13 18:02` | 80 | the upstream commit's own timestamp, preserved by `tar` — untouched originals |
| `2026-08-30 00:42` | 37 | the CRLF → LF normalisation |
| `2026-08-30 16:27` | 10 | the trailing-whitespace strip |

Both rewrite passes ran **after** the 2026-08-24 verification, which is why that verification was
correct when it was written and is wrong now.

### It is not git doing this

Checked and ruled out (**executed-success**):

- `core.autocrlf` is **unset** in this repository's config, and no `eol`/`crlf` setting is present.
- No `.gitattributes` exists at the repository root or anywhere in the `zerowriter_ink` snapshot.
  (Three `.gitattributes` files exist elsewhere in the tree — under `zerowriter1/`,
  `xiao-esp32s3-sense/examples/`, `inkplate-5/.../SparkFun_LSM6DS3_Arduino_Library/` and
  `esp32-s3-knob-touch-lcd-1.8/.../SensorLib/` — none of which govern these paths.)

The rewrite was therefore done by a **tool or editor run across the working tree**, not by a
checkout filter. The practical consequence is that it will happen again to any newly added
snapshot unless whatever did it is identified.

### Worked example

`design/src/Zerowriter breakout board/v1.2.0/CAD/Zerowriter breakout board.kicad_pcb`

| | Bytes | CR bytes | Lines |
|---|---:|---:|---:|
| upstream | 494,761 | 11,497 | 11,497 |
| in repo | 483,264 | **0** | 11,497 |

Exactly one byte lost per line — a clean CRLF → LF conversion, no content change. The same
arithmetic holds for all 36 EOL-ONLY files.

For the trailing-whitespace class, `design/src/Zerowriter breakout board/v1.2.0/OUTPUTS/Zerowriter
breakout board 3D.step`: upstream 5,785,268 B vs repo 5,785,156 B, both 127,172 lines, **zero** CR
bytes in either. After `sed 's/[[:space:]]*$//'` both hash to
`b0b4d4bf157a42395efd0e0f383609e5ee2743cd7fc63196ce8360ed4885c94c` — which is also the repo
file's own SHA-256, confirming the repo copy is the stripped one.

## Which files are affected

<details>
<summary><b>EOL-ONLY — 36 files (CRLF → LF)</b></summary>

All under `design/`. The load-bearing ones:

| File | repo | upstream |
|---|---:|---:|
| `src/Zerowriter breakout board/v1.2.0/CAD/PANEL/Zerowriter breakout board.kicad_pcb` | 8,498,943 | 8,702,870 |
| `src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/PANEL/Zerowriter Inkplate 5 Gen2.kicad_pcb` | 6,082,819 | 6,260,552 |
| `src/Zerowriter Keyboard/v1.2.0/CAD/PANEL/Zerowriter Keyboard.kicad_pcb` | 3,503,142 | 3,612,958 |
| `src/Zerowriter Keyboard/v1.2.0/CAD/Zerowriter Keyboard.kicad_pcb` | 3,480,386 | 3,589,136 |
| `zw_keyboard/Kicad/CAD/Zerowriter Keyboard.kicad_pcb` | 3,351,814 | 3,457,301 |
| `src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/Zerowriter Inkplate 5 Gen2.kicad_pcb` | 3,069,517 | 3,158,336 |
| `src/Zerowriter breakout board/v1.2.0/CAD/Zerowriter breakout board.kicad_pcb` | 483,264 | 494,761 |
| `src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/CTRL & COMS.kicad_sch` | 310,705 | 330,462 |
| `src/Zerowriter Keyboard/v1.2.0/CAD/Zerowriter Keyboard.kicad_sch` | 287,627 | 304,984 |
| `zw_keyboard/Kicad/CAD/Zerowriter Keyboard.kicad_sch` | 287,118 | 304,467 |
| `src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/POWER.kicad_sch` | 266,884 | 283,954 |
| `zw_keyboard/PCB Plate/260122_Keyboard Plate.DXF` | 210,835 | 246,433 |
| `src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/E-paper.kicad_sch` | 149,288 | 158,778 |
| `src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/MCU.kicad_sch` | 139,342 | 148,040 |
| `src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/TestPoints.kicad_sch` | 122,414 | 129,939 |
| `src/Zerowriter breakout board/v1.2.0/CAD/Zerowriter breakout board.kicad_sch` | 114,984 | 122,377 |
| `src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/SD & RTC.kicad_sch` | 83,219 | 88,506 |
| `src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/Board Connectors.kicad_sch` | 38,675 | 41,129 |

plus 4 `.kicad_sch-bak` files, 3 copies of `Soldered Engineering SCH template.kicad_wks`,
6 `PCBA/*-pos.csv` position files, `zw_keyboard/Kicad/OUTPUTS/Zerowriter Keyboard BOM.csv`,
`fp-lib-table` and two 3-byte `PANEL/fp-info-cache` stubs.

</details>

<details>
<summary><b>TRAILING-WS-ONLY — 14 files</b></summary>

| File | repo | upstream |
|---|---:|---:|
| `design/src/Zerowriter Inkplate 5 Gen2/v1.2.0/OUTPUTS/Soldered Inkplate 5 Gen2 3D.step` | 14,189,797 | 14,190,575 |
| `design/src/Zerowriter breakout board/v1.2.0/OUTPUTS/Zerowriter breakout board 3D.step` | 5,785,156 | 5,785,268 |
| `design/src/Zerowriter Keyboard/v1.2.0/OUTPUTS/Zerowriter Keyboard 3D.step` | 4,502,629 | 4,502,831 |
| `design/src/Zerowriter Inkplate 5 Gen2/v1.2.0/OUTPUTS/Zerowriter Inkplate 5 Gen2 ibom.html` | 917,154 | 921,961 |
| `design/src/Zerowriter Keyboard/v1.2.0/OUTPUTS/Zerowriter Keyboard ibom.html` | 512,554 | 517,361 |
| `design/src/Zerowriter breakout board/v1.2.0/OUTPUTS/Zerowriter breakout board ibom.html` | 279,398 | 284,205 |
| `design/src/Zerowriter Keyboard/v1.2.0/CAD/fp-info-cache` | 33,118 | 38,096 |
| `design/src/Zerowriter breakout board/v1.2.0/CAD/fp-info-cache` | 33,118 | 33,125 |
| `design/src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/fp-info-cache` | 19,035 | 22,675 |
| `src/keyboard/zwi_kb_feb2026/zwi_kb_feb2026.ino` | 9,551 | 9,609 |
| `utils/USB_Send.html` | 3,488 | 3,490 |
| `firmware_releases/SD-1.3/readme.txt` | 2,582 | 2,583 |
| `firmware_releases/command line/howto.txt` | 1,162 | 1,165 |
| `firmware_releases/updates-readme.txt` | 471 | 472 |

⚠ Note the last three and `zwi_kb_feb2026.ino`: **the only non-`design/` files touched**, and the
`.ino` is ZeroWriter-authored keyboard firmware source. The change is cosmetic, but it means the
snapshot's firmware source is not a bit-exact copy either.

</details>

## What this means in practice

| If you are… | Then… |
|---|---|
| reading a pin assignment, net, footprint or BOM row out of the snapshot | **unaffected.** Zero semantic differences were found; the KiCad and STEP files parse to the same design |
| re-verifying the snapshot against upstream | **do not use `diff -rq`** or a raw SHA-256 comparison — it will report 50 false positives. Compare after `sed 's/[[:space:]]*$//'` and CRLF folding, or compare upstream against the scratch extraction instead |
| citing a file hash as upstream identity | **do not cite the in-repo hash.** Cite the commit `996207ac…` and, if a byte-level hash is needed, take it from the scratch extraction or a fresh checkout |
| rebuilding the boards from these files | **unaffected** for KiCad (tolerant of either line ending). A strict downstream consumer of the `.DXF` or `.step` could in principle care; not tested here — **not-tested** |

## Reproducing this check

```bash
# byte-exact upstream, for comparison
git clone https://github.com/zerowriter/zerowriter_ink
git -C zerowriter_ink checkout 996207aca0677300ed5f1fdf762d9c9ec79f516e

# or the tarball used here (⚠ a GitHub archive tarball's own hash is NOT stable identity —
# GitHub regenerates them; use it for contents, never as a fingerprint)
curl -L -o zerowriter_ink.tar.gz \
  https://codeload.github.com/zerowriter/zerowriter_ink/tar.gz/996207aca0677300ed5f1fdf762d9c9ec79f516e
```

The classifier used for the table above is
[`archive/devices/zerowriter/zerowriter-ink/artifacts/provenance-2026-08-30/README.md`](../../../archive/devices/zerowriter/zerowriter-ink/artifacts/provenance-2026-08-30/README.md)'s
`classify.py`, re-implemented with an added `EOL-ONLY` class (the original folded CRLF into
`TRAILING-WS-ONLY`, because `str.rstrip()` eats `\r`). **Status: executed-success, 2026-09-20.**

> ⚠ Every script in that scratch directory hard-codes
> `R = "/home/user/code/doc/hardware/devices/zerowriter/..."`, a path that no longer resolves.
> Rewrite the constant to this repository's real root before running anything there, or
> `classify.py` reports the whole tree as `MISSING-IN-REPO` — a pure artefact that looks like a
> catastrophic finding.

## The 13 missing files — resolved 2026-09-20

The `MISSING-IN-REPO` row is **not** a gap in the snapshot. It is three KiCad `*-backups/`
directories that were archived out on 2026-08-24, then lost from the archive when a later pass
archived their parent `PANEL/` directory onto the same archive path and replaced them. The
placeholders were repointed at `scratch/`, leaving a working directory as the only copy.

This pass moved them back into the archive at their repo-relative paths using
`tools/archive_artifact.py`, which verified content by fingerprint after the move
(`verified 3, missing 0, drifted 0`). Byte-identity with the originally-archived material was
proven first: all three `LC_ALL=C` tree digests recorded by the 2026-08-24 placeholders were
reproduced exactly.

| Directory | Files | Bytes | `LC_ALL=C` tree digest |
|---|---:|---:|---|
| `…/Zerowriter breakout board/v1.2.0/CAD/PANEL/Zerowriter breakout board-backups` | 3 | 6,159,721 | `ba50c90380615f724a8cd2afacbd4f12225f4c0dd6e15438c82951511c04c470` |
| `…/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/PANEL/Zerowriter Inkplate 5 Gen2-backups` | 7 | 18,449,694 | `6b42f1da305f87e974d8835416e194fea9aa15fa8a3643a13078042e1ed46f03` |
| `…/Zerowriter Keyboard/v1.2.0/CAD/PANEL/Zerowriter Keyboard-backups` | 3 | 2,659,337 | `4622918c4d871990293f3ece188ead57f941c07c3b9628545ba4e60ee7cd9726` |

A fourth `*-backups/` directory, `design/zw_keyboard/Kicad/CAD/Zerowriter Keyboard-backups`
(2 files), was never affected and has been in the archive throughout.

### The generalisable lesson

`tools/archive_artifact.py` refuses to clobber an existing archive entry — it compares
fingerprints and, on a genuine conflict, stores the incoming copy at
`<dest>.conflict-<timestamp>` rather than overwriting. **That guard did not save this case**,
because the collision was not at the same path: the earlier entry was *nested inside* the later
one (`PANEL/x-backups/` inside `PANEL/`). Archiving a parent directory after its child has
already been archived silently orphans the child's placeholder.

**Check for placeholders beneath a directory before archiving the directory.**

## Unresolved

- **What performed the normalisation is unknown.** The mtimes pin it to 2026-08-30 00:42 and
  16:27, but no tool in `tools/` obviously does this and no git config or `.gitattributes`
  explains it. Until identified, assume any snapshot added to this repository may be rewritten
  the same way. **inferred** from mtime clustering; not directly observed.
- **Whether other source snapshots in this repository suffered the same rewrite is not checked.**
  Only `zerowriter_ink` was compared, because only it had a byte-exact upstream copy available
  locally. **not-tested.**

## See also

- [`README.md`](README.md) — device record
- [`sources.md`](sources.md) — row `ZW-2` pins the upstream commit
- [`inter-board-wiring.md`](inter-board-wiring.md) — pinouts recovered from these KiCad files
- [`keyboard.md`](keyboard.md) — keyboard matrix recovered from these KiCad files
- [`archive/devices/zerowriter/zerowriter-ink/artifacts/provenance-2026-08-30/README.md`](../../../archive/devices/zerowriter/zerowriter-ink/artifacts/provenance-2026-08-30/README.md) — the working directory this comparison used
