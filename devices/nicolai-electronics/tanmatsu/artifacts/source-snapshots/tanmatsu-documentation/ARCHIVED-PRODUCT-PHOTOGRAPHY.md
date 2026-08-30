# Archived product photography — reacquisition record

**15 images, 5,809,346 bytes**, moved out of the repository on **2026-08-30**. Not deleted.

> **These files are absent from the repository.** They are not symlinks and not placeholders-in-place —
> the paths simply do not exist here any more. This record is the only thing standing in for them,
> which is why it carries a SHA-256, a byte count and a pinned reacquisition URL for every file.
>
> The archive copy is a **convenience for whoever holds it, not part of the contract**: it lives
> outside the repository at a machine-local path, so nothing here may depend on it.

link says *"this file exists elsewhere"*, where a missing file says nothing. **This record, not the
symlink, is the contract**: everything needed to re-obtain and verify each file is below.

## Why these and not the others

Every image in this snapshot was checked for whether any Markdown file references it.

| Kept in the repository | Archived here |
|---|---|
| Images **cited** by upstream docs — `back-annotated.png`, `blockdiagram.png`, `blockdiagram2.png`, `jtag-1.jpg`, `jtag-2.jpg`, `right_side.png`, the `compiling_the_template_app/` walkthrough screenshots, the SAO-adapter photos, `tanmatsu.png` | Images cited by **nothing** — colour variants of the same product shot, side views, and case renders |

The archived set is **product photography**: the same board in black, red, purple and cyberdeck
finishes, two side elevations, an untexted duplicate of a user-manual photo, and seven case
renders. None carries engineering information not already present in the two annotated figures.

**Content was extracted before archiving.** The engineering figures were transcribed to
[`board-annotations-and-block-diagram.md`](../../../board-annotations-and-block-diagram.md) — 22
board callouts, the colour-coded bus legend, the button-routing asymmetry, and a vendor
contradiction ("super-speed 480MBit") that had not previously been recorded. Those two figures
**remain in the repository**; only the uncited photography left.

## Contents

| File | Bytes | SHA-256 |
|---|---:|---|
| `hardware/black-front-2.png` | 2,046,427 | `54c91d88fb64cbfdab787188db029c3ce69da99bb8e54987836c4eb10e50ae22` |
| `hardware/cyberdeck-front.png` | 640,958 | `b34d6f40549928fa4f81f06f4d003489016b1fa473a35ec4c2a1b18960ca351c` |
| `hardware/purple-front.png` | 625,872 | `3d47e7ec63ffa20679f3d742bb96208765a617150e6a0dcabcace1dcf4c2a8cb` |
| `hardware/red-front.png` | 614,346 | `8d71d9b52c9c3e14020b455b94f489561aa5ba12ab6b787601511c7601ddb7aa` |
| `hardware/black-front.png` | 552,643 | `4db9f899de5ad91545ceb7eaaffac6241ed38b05daf1cd44fd777fd433e7de14` |
| `user_manual/right_side_no_text.jpg` | 419,300 | `da9b43654ad1c17d7f2bb590d4cbe44312dfd3cff820f52da9bc7a3b507478bf` |
| `hardware/side1.png` | 192,690 | `cd2f135125590fcd593de2afdda4aed9b98b930a1280c444905463f2d6807379` |
| `hardware/side2.png` | 165,992 | `2f7753a726698a2492c9cb1deaadbbb676b77a5125a6050c09c3f1a53a3326df` |
| `hardware/case/main1.jpg` | 98,352 | `8ca39ad42ddbf598ac645a56b9ac27d0221ced0be0d2543a1a06fcb4cbcf762b` |
| `hardware/case/main2.jpg` | 86,549 | `dfd1ce3948c2360af955e2a84267870e97ea2bf901a0a6118f6df5a5cd02831a` |
| `hardware/case/extra3.jpg` | 84,719 | `8ee358b0e383130b27c8aeafe6361663de4828c1077d8d8b1d3d990c34fabd82` |
| `hardware/case/extra1.jpg` | 84,203 | `7db642faf46c129500e79357bcd54084bfb11c248d1800f4c57c839e8faabc96` |
| `hardware/case/extra2.jpg` | 80,960 | `9338fb491b04d694eedbb603f403e2333b991e13ffc9ad3fa04bc24a766c360e` |
| `hardware/case/extra5.jpg` | 58,358 | `6fb709f306b3fea031464a233584fe377da9d38d34bf66f3f1f967b8ec495d61` |
| `hardware/case/extra4.jpg` | 57,977 | `ad28a3bf7cd1e1ae6000f7f6329c7cbd8b78ccbbb82edd189e62fb837b3984d9` |

Archive root:
`archive/hardware-doc/devices/nicolai-electronics/tanmatsu/artifacts/source-snapshots/tanmatsu-documentation/`

## Reacquisition

All 15 come from the upstream documentation repository at a **pinned commit**, so a re-fetch is
exact and the hashes above will match.

| | |
|---|---|
| Repository | `Nicolai-Electronics/tanmatsu-documentation` |
| URL | <https://github.com/Nicolai-Electronics/tanmatsu-documentation> |
| Commit | **`bd3ded51548433bd7d614f5607b7d36f5eed61fa`** (2026-08-01) |
| Licence | **None stated** — affects redistribution, not reacquisition |
| Retrieved | 2026-08-24 |

```bash
# one file, at the pinned commit
curl -fsSL "https://raw.githubusercontent.com/Nicolai-Electronics/tanmatsu-documentation/bd3ded51548433bd7d614f5607b7d36f5eed61fa/hardware/black-front-2.png" \
  -o black-front-2.png
sha256sum black-front-2.png   # expect 54c91d88fb64cbfdab787188db029c3ce69da99bb8e54987836c4eb10e50ae22

# or the whole tree
git clone https://github.com/Nicolai-Electronics/tanmatsu-documentation
git -C tanmatsu-documentation checkout bd3ded51548433bd7d614f5607b7d36f5eed61fa
```

> ⚠ **`tanmatsu.cloud` is a JavaScript SPA with no server-rendered content**, so the rendered
> documentation site cannot be scraped as a fallback. This GitHub repository is the only usable
> source. See [`sources.md`](../../../sources.md).

## Restoring a file

Re-fetch it from the pinned upstream in the Reacquisition section above and verify against the
SHA-256 in the table. If you happen to hold the local archive, copying from the archive root shown
above is faster and gives the identical bytes.

## Note on modifying a vendored snapshot

This directory is a snapshot of an upstream repository, and removing files is a **local
modification**: a fresh clone at the pinned commit has them present. Reconcile against the table
above before concluding that a diff means something.

