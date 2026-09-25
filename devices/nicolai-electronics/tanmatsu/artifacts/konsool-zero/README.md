# `konsool-zero` — KiCad EDA source

The complete published design of **`badgeteam/konsool-zero`**, the Flipper-Zero-class RFID / NFC /
sub-GHz / iButton / IR add-on for the Tanmatsu rear 36-pin port.

**These files are the evidence** behind the fitment findings and the STM32WB55CC correction in
[`../../expansion-boards.md` §2](../../expansion-boards.md), and behind the full connector wiring
and host GPIO map in [`../../konsool-zero-wiring.md`](../../konsool-zero-wiring.md). Before this
pass they existed only in `scratch/`, which meant the corrections cited evidence that was not in
the repository.

## Identity

| Field | Value |
|---|---|
| Upstream repository | <https://github.com/badgeteam/konsool-zero> |
| Commit | **`0f0b964107c15dd398ee3e44a064fb853b17aaa8`** |
| Commit subject | *"board elements that were missing."* |
| Author | Paul Honig `<paul@etv.cx>` |
| Committed | **2025-03-22T11:38:10+01:00** |
| Tag / release | **none** — the repository has exactly **one commit** and no releases |
| Retrieved | **2026-08-26** (clone), filed here **2026-09-20** |
| Licence | **BSD 3-Clause, Copyright (c) 2024, Nicolai Electronics** — see `LICENSE-BSD-3-Clause` |
| Redistribution status | `allowed` (BSD-3-Clause), with the attribution and non-endorsement conditions |
| Disposition | `repository` |
| Upstream README | **none** — the repository ships no README |

> ⚠ **Correction, 2026-09-20.** [`../../expansion-boards.md`](../../expansion-boards.md) previously
> recorded this project's licence as *"none stated"* in §1 and *"no stated licence"* in §2. That was
> wrong: a `LICENSE` file **is** tracked at `0f0b964` and carries the BSD 3-Clause text above.
> Both statements have been corrected. The *"no README"* and *"one commit"* claims were checked and
> are **correct**.

## Contents

| Path | Bytes | What it is |
|---|---:|---|
| `kicad/tanmantsu-zero.kicad_pcb` | 2 391 120 | **The authoritative artifact** — PCB with resolved net names on every pad |
| `kicad/tanmantsu-zero.kicad_sch` | 89 740 | Root sheet *(upstream misspelling of "tanmatsu" preserved)* |
| `kicad/tanmantsu-zero.kicad_pro` | 21 097 | Project file |
| `kicad/zero-mcu.kicad_sch` | 62 270 | CH32V003F4U6 (`U19`) and its 25 MHz oscillator |
| `kicad/sub-ghz-radio.kicad_sch` | 71 725 | CC1101RGPR (`U1`), 27 MHz XO (`U2`) |
| `kicad/nfc-block.kicad_sch` | 134 986 | ST25R3916-AQWT (`U5`), 27.12 MHz crystal (`X1`) |
| `kicad/rfid-schematic.kicad_sch` | 208 383 | 125 kHz analog front end |
| `kicad/antenna-balance.kicad_sch` | 74 073 | SP3T switches `U3`/`U4`, band matching |
| `kicad/rf-balance.kicad_sch` | 35 098 | CC1101 balun network |
| `kicad/ir-comms.kicad_sch` | 52 737 | TSOP75338 receiver, three VSMY14940 emitters |
| `kicad/ibutton.kicad_sch` | 12 494 | 1-Wire contact and TVS |
| `kicad/expansion-template.kicad_sch` | 81 314 | **Shared add-on outline template** — see below |
| `kicad/expansion-template.kicad_pcb` | 543 022 | konsool-zero's layout of that template |
| `kicad/fp-lib-table`, `kicad/sym-lib-table` | 425 / 131 | Library tables |
| `kicad/pcb_coils/COIL_GENERATOR.kicad_mod` | 117 869 | Parametric spiral coil footprint |
| `kicad/pcb_coils/COIL_RFID_ZERO.kicad_mod` | 117 869 | The 125 kHz RFID coil as laid out |
| `LICENSE-BSD-3-Clause` | 1 506 | Upstream `LICENSE`, renamed for clarity |

### The expansion template is shared by copy

`kicad/expansion-template.kicad_sch` is **byte-identical** to
`konsool-18650-expansion/expansion-template.kicad_sch`
(`fa79df7fc3988227bebae85eccb74a694b47a6fd14ca758553906ad9f4636dd1`). The
`badgeteam/konsool-expansion-template` repository that was supposed to hold it is
empty, so add-on designers copy this file between projects by hand. See
[`../../konsool-zero-wiring.md` §9](../../konsool-zero-wiring.md).

⚠ It inherits konsool-zero's **pin-7 `VSDCARD` mislabel** (pin 7 is `GND` on the Tanmatsu) and its
**wrong `E8`/`E9`/`E10` names**. Check against
[`../../pinouts-and-buses.md` §2](../../pinouts-and-buses.md) before reusing it.

## Not copied here

| Left in scratch | Why |
|---|---|
| `library/lcsc.3dshapes/` (~68 MB, 42 STEP + WRL pairs) | Generic LCSC package meshes — not board-specific, regenerable from upstream, carry no electrical information |
| `jlcpcb/project.db` (20 480 B) | SQLite cache written by the JLCPCB fabrication-toolkit plugin; a build artifact |
| `docs/` chip datasheets (7 PDFs) | **Component** artifacts — filed under `components/` by the 2026-09-20 pass and removed from the clone. See [`../../sources.md`](../../sources.md) |
| `docs/*.pdf` — six Flipper Devices schematics | Describe a **different product**; filed under [`devices/flipper-devices/flipper-zero/`](../../../../flipper-devices/flipper-zero/README.md) |
| `docs/flipper-zero-photos/` (4.0 MB) | Filed with the Flipper record and archived — see that record's placeholder |

## Re-acquisition

```bash
git clone https://github.com/badgeteam/konsool-zero
git -C konsool-zero checkout 0f0b964107c15dd398ee3e44a064fb853b17aaa8
sha256sum konsool-zero/tanmantsu-zero.kicad_pcb
# expect 21eb0005720cc0a20a2e169e72ef80b4773010b4f14b14afdbce874b8e0e3b2d
```

⚠ The repository has **no `main` branch** — a `raw.githubusercontent.com/.../main/...` URL 404s
(recorded in [`../../commands.md`](../../commands.md)). Always use the pinned commit.

Reacquisition status: **automatic**. Hashes verified against the local checkout on 2026-09-20;
the GitHub endpoint was **not** re-probed in this pass.

## Why these are copies, not moves

`scratch/tanmatsu/sources/konsool-zero/` remains a working KiCad project so the parsers can be
re-run against it. Every file here was verified **byte-identical by SHA-256** to its scratch
counterpart at the moment of copying. The scratch clone is already `dirty` — the 2026-09-20 pass
*moved* the seven chip datasheets out of `docs/` when filing them as component artifacts — so
`git status` there reports seven deletions by design.
