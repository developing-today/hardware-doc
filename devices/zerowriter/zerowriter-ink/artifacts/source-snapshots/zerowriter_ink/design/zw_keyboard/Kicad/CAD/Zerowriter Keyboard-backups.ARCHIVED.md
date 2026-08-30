# ARCHIVED: `Zerowriter Keyboard-backups/`

> This directory was **moved out of the repository**, not deleted.
> Archived **2026-08-24**.

**What it is:** KiCad's **automatic project backups**. KiCad 7+ writes a timestamped ZIP into
`<project>-backups/` every time the project is saved (`Preferences → Common → Project Backup`).
Each ZIP holds intermediate save states of `.kicad_pcb` / `.kicad_pro` / `.kicad_prl`, plus in some
cases an `_autosave-*.kicad_pcb` crash-recovery file.

**What it is for:** editor crash/undo recovery for the designer. It is **not** a release artifact
and carries no design intent that is not already in the live project files beside it.

**Why removal was OK:**

1. **Nothing unique.** These are intermediate save states of the *panelised* project whose final
   state is still present, uncompressed, in the parent directory. The design's real revision
   history lives in upstream git.
2. **Fully reacquirable.** The entire `zerowriter_ink` snapshot in this repository was verified on
   2026-08-24 to be **byte-identical** to `zerowriter/zerowriter_ink` at commit
   `996207aca0677300ed5f1fdf762d9c9ec79f516e` — `diff -rq` across the whole tree reported
   **zero** differences. These ZIPs are in that commit and can be pulled back verbatim.
3. **Poorly compressible duplication.** ZIP-compressed near-copies of the same multi-MiB
   `.kicad_pcb` defeat git's delta compression, so they cost close to their full size forever.

The **live design files were not touched.** Schematics, PCBs, panels, Gerbers, BOMs, STEP models
and 3D-printable outputs all remain in place.

## Identity

| Field | Value |
|---|---|
| Original repo path | `devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter_ink/design/zw_keyboard/Kicad/CAD/Zerowriter Keyboard-backups` |
| Archived to | `archive/devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter_ink/design/zw_keyboard/Kicad/CAD/Zerowriter Keyboard-backups` |
| Type | directory of ZIP archives |
| Size | **1327732 B** |
| File count | **2** ZIP files |
| Extracted-tree digest (`LC_ALL=C`) | `3b4efb9a836e93da061f2b9e092808f3ceaefd9d3b4ee413757c097eb87a2528` |
| Producer | KiCad automatic project backup |
| Author | Adam Wilk / Zerowriter |
| Upstream repository | <https://github.com/zerowriter/zerowriter_ink> |
| Upstream commit | `996207aca0677300ed5f1fdf762d9c9ec79f516e` ("source files") |
| Upstream author / date | Adam Wilk `<adamwilk@MacBook-Air-3.local>` · 2026-05-13T19:02:20-04:00 |
| Path within upstream repo | `design/zw_keyboard/Kicad/CAD/Zerowriter Keyboard-backups` |
| License | **GPL-3.0** (`zerowriter_ink/LICENSE` — GNU GPL v3, 29 June 2007) |
| Redistribution status | allowed (GPL-3.0; copyleft — redistribution must carry the license and source) |
| Backup timestamps | encoded in the filenames below. The mtimes are all 2026-05-13 — the clone date, not the save date. |

### Files (these are the compressed originals; sizes are pre-extraction)

| File | Bytes | mtime | SHA-256 |
|---|---:|---|---|
| `Zerowriter Keyboard-2026-02-17_161947.zip` | 663866 | 2026-05-13 | `1f1016b4faddb7dde6c480616d07907cdaac43290fcc912d9528ba3c77d96a6b` |
| `Zerowriter Keyboard-2026-04-06_171853.zip` | 663866 | 2026-05-13 | `1f1016b4faddb7dde6c480616d07907cdaac43290fcc912d9528ba3c77d96a6b` |

Post-extraction sizes are not recorded: each ZIP is a snapshot of files that already exist
uncompressed in the parent directory. Inspect on demand with `unzip -l` / `unzip -d`.

## How to get it back

All statuses verified **2026-08-24**.

```bash
# Source 1 — upstream git at the pinned commit (exact, preferred)
git clone https://github.com/zerowriter/zerowriter_ink.git
cd zerowriter_ink && git checkout 996207aca0677300ed5f1fdf762d9c9ec79f516e
#   -> "design/zw_keyboard/Kicad/CAD/Zerowriter Keyboard-backups"

# Source 2 — GitHub tarball at that commit    (HTTP 200 · application/x-gzip)
curl -L -o zerowriter_ink.tar.gz \
  https://codeload.github.com/zerowriter/zerowriter_ink/tar.gz/996207aca0677300ed5f1fdf762d9c9ec79f516e

# Source 3 — GitHub zip at that commit        (HTTP 200 · application/zip, 302 -> codeload)
curl -L -o zerowriter_ink.zip \
  https://github.com/zerowriter/zerowriter_ink/archive/996207aca0677300ed5f1fdf762d9c9ec79f516e.zip

# Source 4 — Wayback Machine
#   https://web.archive.org/web/2/https://github.com/zerowriter/zerowriter_ink
```

## Verify

```bash
# from the directory containing this placeholder
find "Zerowriter Keyboard-backups" -type f | wc -l                                      # 2
find "Zerowriter Keyboard-backups" -type f -printf '%s\n' | awk '{s+=$1}END{print s}'    # 1327732
find "Zerowriter Keyboard-backups" -type f -exec sha256sum {} + | LC_ALL=C sort -k2 | sha256sum
#   3b4efb9a836e93da061f2b9e092808f3ceaefd9d3b4ee413757c097eb87a2528
```

`LC_ALL=C` is pinned deliberately — these filenames contain spaces and digits that sort
differently under a UTF-8 locale.

## Restore from the local archive

```bash
mv "$HOME/repo-archive/devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter_ink/design/zw_keyboard/Kicad/CAD/Zerowriter Keyboard-backups" \
   "devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter_ink/design/zw_keyboard/Kicad/CAD/Zerowriter Keyboard-backups"
```

## See also

- [`../../../../../../vendored-deps/README.md`](../../../../../../vendored-deps/README.md) — the removed-dependency register for this device
- [`../../../../../../../zerowriter1-epaper-driver-notes.md`](../../../../../../../zerowriter1-epaper-driver-notes.md) — analysis of the other archived dependency for this device
