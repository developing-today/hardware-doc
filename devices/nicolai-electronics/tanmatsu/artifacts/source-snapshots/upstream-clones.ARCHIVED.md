# Upstream source clones — ARCHIVED

**Archived to** `archive/devices/nicolai-electronics/tanmatsu/artifacts/source-snapshots/upstream-clones/`
**Date:** 2026-09-20 · **25 directories · 1 181 006 219 B (1.10 GiB) · 2 953 files**

The archive is machine-local and absent from a fresh clone. Everything needed to reacquire these
is below; the archive path is a convenience, not the contract.

## What these are, and how they differ from the directories beside this file

The four directories in *this* repository —
[`badge-bsp/`](badge-bsp/), [`coprocessor-firmware/`](coprocessor-firmware/),
[`i2c_puppet/`](i2c_puppet/) and [`tanmatsu-documentation/`](tanmatsu-documentation/) — are
**hand-picked subsets**: the handful of files that the Tanmatsu records actually cite.

The archive holds the **24 complete upstream git clones** those subsets were cut from, plus one
aborted clone, `.git` directories included. They were taken 2026-08-24 → 2026-08-30 and are the
raw material behind [the device record](../../README.md),
[`pinouts-and-buses.md`](../../pinouts-and-buses.md),
[`konsool-zero-wiring.md`](../../konsool-zero-wiring.md), [`keyboard.md`](../../keyboard.md) and
[`bom.md`](../../bom.md).

Nothing in the archive is required to *use* this repository. It exists so that a claim parsed
from a KiCad file or a coprocessor register map can be re-derived without re-cloning 1.1 GB.

## Inventory

| Snapshot | Remote `github.com/…` | HEAD | Shallow | Licence |
|---|---|---|---|---|
| `appfs-real` | `badgeteam/esp32-component-appfs` | `eee29be489f164884f6e8a7f881ab37270b3cb9f` | **yes (1 commit)** | Apache-2.0 |
| `app-repository` | `Nicolai-Electronics/app-repository` | `f83e1559553497903c083525a10d2aaf53344377` | no (159) | none |
| `badge-bsp` | `badgeteam/esp32-component-badge-bsp` | `9037f0e21d1df072fcdd4b95416885cc7fc77865` `v1.4.0` | no (175) | MIT |
| `badgelink` | `badgeteam/esp32-component-badgelink` | `3e3e6957bc71c4c75eeb0773f1ece9084732575f` `v0.2.0` | **yes (1)** | MIT |
| `esp32-component-tanmatsu-coprocessor` | `Nicolai-Electronics/esp32-component-tanmatsu-coprocessor` | `6eea3735346ee1b689898c77e500fb1d0c4e024e` `v0.8.0` | no (23) | none |
| `esp32-component-tanmatsu-wifi` | `Nicolai-Electronics/esp32-component-tanmatsu-wifi` | `d8ce0bf106141d6bccf4cb9a927bd494facc31af` | no (12) | MIT |
| `i2c_puppet` | `solderparty/i2c_puppet` | `f085518d78ed38c009f18651abc21321ddf6fcfd` | no (17) | MIT |
| `keebdeck_basic_hw` | `solderparty/keebdeck_basic_hw` | `2b537ce5fef3da50b016c18ca66aac520af5abd1` `rev1.1` | **yes (1)** | CERN-OHL v1.2 |
| `keebdeck_keyboard_hw` | `solderparty/keebdeck_keyboard_hw` | `f1c074c47aa48d2eb584dad2ddad2a90ab6b86ed` | **yes (1)** | CERN-OHL v1.2 |
| `konsool-18650-expansion` | `badgeteam/konsool-18650-expansion` | `69504c4d1572358056dc5bb394f21dce1489a0da` | **yes (1)** | none |
| `konsool-expansion-template` | `badgeteam/konsool-expansion-template` | — **aborted clone, 0 commits** | — | none |
| `konsool-template-lvgl` | `badgeteam/konsool-template-lvgl` | `8f8fd1fb36e106bc765d8b68f4e9355a667ee44a` | **yes (1)** | none |
| `konsool-zero` | `badgeteam/konsool-zero` | `0f0b964107c15dd398ee3e44a064fb853b17aaa8` | **yes (1)** | BSD-3-Clause |
| `tanmatsu-coprocessor-firmware` | `Nicolai-Electronics/tanmatsu-coprocessor-firmware` | `57ff2505d7256b55cc5fea4eb9be10a9a077bafa` | no (48) | MIT |
| `tanmatsu-documentation` | `Nicolai-Electronics/tanmatsu-documentation` | `bd3ded51548433bd7d614f5607b7d36f5eed61fa` | no (59) | none |
| `tanmatsu-frontpanel-cyberdeck` | `Nicolai-Electronics/tanmatsu-frontpanel-cyberdeck` | `7e53be2985c0b3b1971d29074bc3cc5b927d2ce4` | **yes (1)** | CERN-OHL-P v2 |
| `tanmatsu-frontpanel-honeycomb` | `Nicolai-Electronics/tanmatsu-frontpanel-honeycomb` | `270c38eff2a431c14c5a7dfcd1d181f2ef70bbd7` | **yes (1)** | CERN-OHL-P v2 |
| `tanmatsu-hardware` | `Nicolai-Electronics/tanmatsu-hardware` | `640805dd4304f4bfaac24965f8eecf81bec97bf1` `rev-7` | no (253) | CERN-OHL-P v2 |
| `tanmatsu-launcher` | `Nicolai-Electronics/tanmatsu-launcher` | `20022fce316d768a1ff966b973ee2127511713f5` `v0.2.6` | no (454) | MIT |
| `tanmatsu-mechanical` | `Nicolai-Electronics/tanmatsu-mechanical` | `c623cd548c9cafb95773624fe775001984449a89` `release-5` | no (54) | CERN-OHL-P v2 |
| `tanmatsu-plugin-startup` | `nullislandspace/tanmatsu-plugin-startup` | `3857321caf6be8b8154bac72a1c1ea80a53c136d` | **yes (1)** | none |
| `tanmatsu-plugin-turret` | `nullislandspace/tanmatsu-plugin-turret` | `a1d223c34dae1ae1e623e4f2b8ee7958f2959e87` | **yes (1)** | none |
| `tanmatsu-radio` | `Nicolai-Electronics/tanmatsu-radio` | `cb4e38c02aa8ad533fd17b24921c4ca4848eeaf6` `v3.4.0` | no (92) | Apache-2.0 |
| `tanmatsu-template` | `Nicolai-Electronics/tanmatsu-template` | `907fb9657658995efab210b754f28a3ace06d03a` | no (45) | none |

Per-directory byte counts, file counts and tree digests are in the archive's own
`README.md`. `none` means **no licence file exists** — retained as research artifacts, not as
redistributable code.

## Reacquisition

Status: **`automatic`** for all 24 real clones.

```bash
git clone https://github.com/<owner>/<name>.git <name>
git -C <name> checkout <HEAD from the table above>
```

⚠ **Eleven clones are shallow** (`.git/shallow` present, exactly one reachable commit) — measured
2026-09-20. Their archived copies reproduce the HEAD tree but **not history**. Re-clone from the
remote if you need it.

⚠ **`konsool-expansion-template` is `not-applicable`.** Its upstream genuinely has no commits;
the archived directory holds a `.git` with no `objects/` and no `refs/`, `HEAD` reading
`ref: refs/heads/.invalid`, and zero working files. That absence is the evidence confirming
[`expansion-boards.md` §1](../../expansion-boards.md). **`git -C` on it silently walks up and
reports the enclosing repository's HEAD** — a real SHA belonging to a different repo, with no
warning. Use `GIT_DIR=…/.git git rev-parse HEAD`, which fails loudly instead.

⚠ **No upstream URL was re-probed.** Availability is assumed, not tested. The sibling e-ink
corpus lost a repository to a 404 nineteen days after cloning; none of these is bundled.

## What was already extracted from them

Archiving happened only after mining. Findings that no longer depend on reopening these clones:

- [`konsool-zero-wiring.md`](../../konsool-zero-wiring.md) — the 36-pin expansion comparison,
  machine-parsed from the konsool-zero PCB and the Tanmatsu IPC fabrication netlist
- [`keyboard.md` §2b](../../keyboard.md) — the KeebDeck Basic reference schematic: 6 × 12 / 71
  keys, no matrix diodes, `ROW3` = `BOOT0`, `COL0`/`COL1` = `SWDIO`/`SWCLK`
- [`pinouts-and-buses.md`](../../pinouts-and-buses.md) and
  [`bom.md`](../../bom.md) — from `tanmatsu-hardware`'s KiCad sources and production files
- [`badgelink-and-appfs.md`](../../badgelink-and-appfs.md) — from `badgelink` and `appfs-real`
- [`gaps-and-conflicts.md` §14](../../gaps-and-conflicts.md) — badge.team's wrong E-numbering,
  refuted from copper

The KiCad symbols, footprints, schematics, production BOM/positions/netlist and the coprocessor
sources that these records cite are **in this repository**, under
[`../schematics/`](../schematics/), [`../konsool-zero/`](../konsool-zero/),
[`../keebdeck-basic/`](../keebdeck-basic/) and the four subset directories beside this file.
They were **copied** out of the clones, never cut — the clones remain complete checkouts.

## Sibling archive directories from the same move

| Archive path | Placeholder |
|---|---|
| `archive/devices/nicolai-electronics/tanmatsu/artifacts/web-captures/` | [`../web-captures.ARCHIVED.md`](../web-captures.ARCHIVED.md) |
| `archive/devices/nicolai-electronics/tanmatsu/tools/scratch-scripts-duplicates/` | described in `../web-captures.ARCHIVED.md` |

## Note on this directory's `README.md`

`artifacts/source-snapshots/README.md` in this repository is **not** an index of this directory
— it is the upstream `nicolaielectronics/tanmatsu_coprocessor` component README, filed under a
generic name. Elsewhere in this tree that content is named `upstream-README.md`
(see [`../mechanical/upstream-README.md`](../mechanical/upstream-README.md) and
[`../keebdeck-basic/upstream-README.md`](../keebdeck-basic/upstream-README.md)). It was left
alone rather than renamed, but do not mistake it for a description of the snapshots.
