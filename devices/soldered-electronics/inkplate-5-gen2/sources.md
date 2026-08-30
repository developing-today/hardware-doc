# Inkplate 5 Gen 2 — source manifest

> Sources specific to the **Gen 2 / `Inkplate5V2`** board. Retrieved **2026-08-24**; URLs
> re-verified **2026-08-28**. Local paths are relative to this device folder; a dash means link-only.
>
> **Most of the evidence for this board is shared with the Inkplate 5** — the Arduino library, the
> MicroPython driver, the documentation repository and every Soldered web property are catalogued
> once in [`../inkplate-5/sources.md`](../inkplate-5/sources.md) and are **not repeated here**.
> This file records only what is Gen-2-specific, plus the comparison sources that make the
> "one component differs" claim checkable.

`Class` is one of **primary** / **authorized mirror** / **credible mirror** / **standard** / **community**.

---

## 1. Primary design data — Gen 2 hardware repository

Soldered publish the Gen 2 in a **separate upstream repository** from the Inkplate 5. That is the
reason this device keeps its own record at all.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| G2-1 | `SolderedElectronics/Soldered-Inkplate-5-Gen2-hardware-design` | Soldered Electronics (TAVU) | primary | repository | <https://github.com/SolderedElectronics/Soldered-Inkplate-5-Gen2-hardware-design> | 2026-08-24 (HTTP 200 re-checked 2026-08-28) | commit `7450a321`, 2025-03-08 | The complete **V1.1.0** open-hardware design package — KiCad sources, BOM, schematic PDF, gerbers, 3D STEP, compliance certificates | Snapshot is a **plain copy, not a git clone** — no `.git`, so the commit is recorded here rather than being verifiable from the tree. Note the design revision (**V1.1.0**) is *lower* than the Inkplate 5's (V1.2.0); the two repositories version independently | [`artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/`](artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/) |
| G2-2 | `Soldered Inkplate 5 Gen2 BOM.csv` (V1.1.0) | Soldered Electronics | primary | repository | in G2-1, `OUTPUTS/V1.1.0/` | 2026-08-24 | V1.1.0 | **The `ED052TC4` panel identity** and, diffed designator-by-designator against [IP5-2](../inkplate-5/sources.md), the finding that the two generations differ in **exactly one component** | Semicolon-delimited KiCad export. ⚠ **Reference designators shift between the two BOMs** (ESP32 is `U10` on the Inkplate 5, `U11` here; the panel is `U11` then `U9`) — do not match parts across generations by designator | `artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/OUTPUTS/V1.1.0/Soldered Inkplate 5 Gen2 BOM.csv` (3,749 B) |
| G2-3 | `Soldered Inkplate 5 Gen2.kicad_pcb` | Soldered Electronics | primary | repository | in G2-1, `CAD/V1.1.0/` | 2026-08-24 | V1.1.0 | **The pin-map identity result.** Netlist-parsed with [`tools/kicad_pcb_nets.py`](../../../tools/kicad_pcb_nets.py) and diffed against the Inkplate 5 and the ZeroWriter respin: **all 36 connected ESP32-WROVER pads carry the same net names** in all three designs | Establishes identity of the *processor* net map only. It says nothing about off-processor circuitry, which is where ZeroWriter's respin actually differs (charger, USB-C, microSD) | `artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/CAD/V1.1.0/Soldered Inkplate 5 Gen2.kicad_pcb` (4,318,537 B) |
| G2-4 | `Soldered Inkplate 5 Gen2 Schematics.pdf` | Soldered Electronics | primary | schematic | in G2-1, `OUTPUTS/V1.1.0/` | 2026-08-24 | V1.1.0 | Rendered schematic for the six hierarchical sheets | Not traced. Component identity came from G2-2 | `artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/OUTPUTS/V1.1.0/Soldered Inkplate 5 Gen2 Schematics.pdf` (1,170,313 B) |
| G2-5 | KiCad hierarchical schematic sources | Soldered Electronics | primary | repository | in G2-1, `CAD/V1.1.0/` | 2026-08-24 | V1.1.0 | Editable design source: `MCU`, `POWER`, `E-paper`, `CTRL & COMS`, `SD & RTC`, **`TestPoints`** plus the root sheet | Note the Gen 2 carries a **`TestPoints.kicad_sch` sheet the Inkplate 5 does not**. This was not investigated and is not reflected in the "one component differs" claim, which is a **BOM-level** claim | `artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/CAD/V1.1.0/*.kicad_sch` (7 files) |
| G2-6 | `PANEL/Soldered Inkplate 5 Gen2_panel.kicad_pcb` | Soldered Electronics | primary | repository | in G2-1, `CAD/V1.1.0/PANEL/` | 2026-08-24 | V1.1.0 | The production panel layout | Manufacturing aid, not new design information | `artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/CAD/V1.1.0/PANEL/` (8,661,619 B) |
| G2-7 | Gerber set, `…130_59x162_47 2 gerber.zip` | Soldered Electronics | primary | repository | in G2-1, `OUTPUTS/V1.1.0/` | 2026-08-24 | V1.1.0 | Fabrication-ready data; board outline 130.59 × 162.47 mm implied by the filename | ⚠ Note this differs from the Inkplate 5's `267_2x162_47` filename — the two **panel step-and-repeat** dimensions differ, which is a panelisation difference, not necessarily a board-outline difference. Not opened or verified | `artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/OUTPUTS/V1.1.0/Soldered Inkplate 5 Gen2 130_59x162_47 2 gerber.zip` (1,207,969 B) |
| G2-8 | `Soldered Inkplate 5 Gen2 3D.step` and Top/Bottom STEP + STL | Soldered Electronics | primary | repository | in G2-1, `CAD/V1.1.0/Source 3D files/` and `OUTPUTS/V1.1.0/3D files/` | 2026-08-24 | V1.1.0 | Mechanical envelope of the assembled board and the printable enclosure halves | The Gen 2 ships **separate Top/Bottom** parts where the Inkplate 5 ships one `Case` model — the enclosures are **not interchangeable artefacts**, and no dimensional comparison was made | `artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/` (31,054,109 B + 2,655,394 B + 83,768 B + 635,368 B) |
| G2-9 | `Soldered Inkplate 5 Gen2 iBOM.html` | Soldered Electronics (InteractiveHtmlBom) | primary | repository | in G2-1, `OUTPUTS/V1.1.0/` | 2026-08-24 | V1.1.0 | Interactive placement/BOM cross-reference | **Generated output** derived from G2-2 + G2-3. Not independent evidence | `artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/OUTPUTS/V1.1.0/Soldered Inkplate 5 Gen2 iBOM.html` (920,672 B) |
| G2-10 | CE / UKCA declarations and safety instructions (EN + DE) | Soldered Electronics | primary | regulatory record | in G2-1, `OUTPUTS/Compliance/` | 2026-08-24 | undated in-repo | That conformity declarations ship inside the public repository | **Retained but not read.** Note the filenames differ from the Inkplate 5's (`Safety Instructions` here vs `Safety sheet` there) and are **not** byte-identical, so these are Gen-2-specific documents | `artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/OUTPUTS/Compliance/` (5 files, 248,180 B) |
| G2-11 | `LICENSE.md` — TAPR Open Hardware License v1.0 | TAPR, applied by Soldered Electronics | standard | manual | in G2-1, repo root | 2026-08-24 | TAPR OHL v1.0 | The licence grant for the Gen 2 design | **Byte-identical** (SHA-256 `ae647e302f1a8023…`) to the Inkplate 5's copy — each repository correctly carries its own. GitHub reports `NOASSERTION` | `artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/LICENSE.md` (13,919 B) |
| G2-12 | Upstream repository `README.md` | Soldered Electronics | primary | repository | in G2-1, repo root | 2026-08-24 | commit `7450a321` | — (recorded as a **negative** result) | ⚠ **Unedited template**, byte-identical to the Inkplate 5's. Contains only placeholders. Carries no product information; do not cite it | `artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/README.md` (2,736 B) |

## 2. Software evidence specific to the Gen 2 target

Catalogued in full in [`../inkplate-5/sources.md` §2](../inkplate-5/sources.md); listed here because
these particular files are what identify **this** board rather than its sibling.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| G2-13 | `src/boards/Inkplate5V2/waveforms.h` | Soldered Electronics | primary | repository | in [IP5-12](../inkplate-5/sources.md) | 2026-08-24 | commit `1751cbe5`, 2026-08-20 | **`E_INK_WIDTH 1280` / `E_INK_HEIGHT 720`** — the resolution claim for this board | Compile-time constants. This is the **strongest available evidence**, because no E Ink panel datasheet exists for the `ED052TC4` | [`../inkplate-5/artifacts/source-snapshots/Inkplate-Arduino-library/src/boards/Inkplate5V2/waveforms.h`](../inkplate-5/artifacts/source-snapshots/Inkplate-Arduino-library/src/boards/Inkplate5V2/waveforms.h) |
| G2-14 | `src/boards/Inkplate5V2/Inkplate5V2Driver.cpp` | Soldered Electronics | primary | repository | in [IP5-12](../inkplate-5/sources.md) | 2026-08-24 | commit `1751cbe5` | The **PSRAM argument**: the driver allocates a 115,200 B 1-bit `_partial` buffer *and* a 460,800 B 4-bit `DMemory4Bit` buffer — beyond ESP32 internal RAM, which is why every Inkplate uses a **WROVER** | Shows what the driver allocates, not the module's actual PSRAM size, which the BOM does not state ([Inkplate 5 gaps §5](../inkplate-5/gaps-and-conflicts.md#5-wrover-variant-not-specified)) | [`../inkplate-5/artifacts/source-snapshots/Inkplate-Arduino-library/src/boards/Inkplate5V2/Inkplate5V2Driver.cpp`](../inkplate-5/artifacts/source-snapshots/Inkplate-Arduino-library/src/boards/Inkplate5V2/Inkplate5V2Driver.cpp) |
| G2-15 | `source/features.rst`, lines 57–84 | Soldered Electronics | primary | manual | in [IP5-21](../inkplate-5/sources.md) | 2026-08-24 | commit `1b3d3329`, 2025-08-25 | The Gen 2's **1.13 s full / 0.26 s fast** refresh figures | **Vendor claim, not measured.** No method, sample count or temperature stated | [`../inkplate-5/artifacts/docs/Inkplate-documentation/source/features.rst`](../inkplate-5/artifacts/docs/Inkplate-documentation/source/features.rst) |

## 3. Comparison sources — the ZeroWriter respin

The claim that a stock Gen 2 and a ZeroWriter Ink main board present the same ESP32 pin map is a
**three-way netlist diff**, and all three inputs need to be citable.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| G2-16 | `zerowriter/zerowriter_ink` — `design/src/Zerowriter Inkplate 5 Gen2/v1.2.0/` | Zerowriter (Adam Wilk) | primary | repository | <https://github.com/zerowriter/zerowriter_ink> | 2026-08-24 | commit `996207ac`, 2026-05-13; **GPL-3.0** | ZeroWriter's respun KiCad design — the third input to the pin-map diff, and the source of the "every connected pad is identical" result | ZeroWriter's KiCad **BOM export uses commas** with different columns than Soldered's semicolon export — sniff the delimiter. Full record: [`../../zerowriter/zerowriter-ink/sources.md`](../../zerowriter/zerowriter-ink/sources.md) (ZW-2) | `../../zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter_ink/` |
| G2-17 | `tools/kicad_pcb_nets.py` | this repository | — (tool) | repository | — | 2026-08-24 | — | The method behind G2-3 and G2-16: extracts pad→net mappings from a `.kicad_pcb` for diffing | ⚠ **Byte-identical copy** (SHA-256 `a8ebbf6d5e6ddce9…`) of [`../inkplate-5/tools/kicad_pcb_nets.py`](../inkplate-5/tools/kicad_pcb_nets.py). Duplicated deliberately so each device tree is self-contained; 2,109 B | [`tools/kicad_pcb_nets.py`](../../../tools/kicad_pcb_nets.py) |

## 4. Cross-referenced records in this repository

| Record | What it supplies |
|---|---|
| [`../inkplate-5/sources.md`](../inkplate-5/sources.md) | **The shared source base** — Arduino library, MicroPython, documentation repository, all Soldered web properties, third-party projects |
| [`../inkplate-5/README.md`](../inkplate-5/README.md) | The full two-generation technical record |
| [`../inkplate-5/pinouts-and-buses.md`](../inkplate-5/pinouts-and-buses.md) | The pin table, which G2-3 verifies applies to this board unmodified |
| [`../../zerowriter/zerowriter-ink/sources.md`](../../zerowriter/zerowriter-ink/sources.md) | Provenance for G2-16 and for the respin's off-processor differences |
| [`../../../vendors/soldered-electronics/README.md`](../../../vendors/soldered-electronics/README.md) | Repository-naming inconsistency (`Gen2` vs `V2` vs "Gen 2"), the BOM-delimiter trap, GitHub pagination |

---

## 5. Evidence notes and known gaps

**No physical unit was available.** This board was researched as the display platform underneath
[ZeroWriter Ink](../../zerowriter/zerowriter-ink/README.md), not as a board in its own right.
Nothing here is hardware-verified.

**The "exactly one component differs" claim is a BOM-level claim.** It rests on G2-2 diffed against
[IP5-2](../inkplate-5/sources.md), and it is accurate at that level. It does **not** account for the
extra `TestPoints` schematic sheet (G2-5), the different panelisation (G2-7) or the different
enclosure geometry (G2-8), none of which appear in a BOM comparison.

**The design revisions run backwards.** The Gen 2 is V1.1.0 while the older Inkplate 5 is V1.2.0.
The repositories version independently; this is not evidence that the Gen 2 is an earlier design.

**No E Ink panel datasheet exists.** Every `ED052TC4` figure derives from G2-2 and G2-13, not from a
manufacturer document — see the [`ED052TC4` component record](../../../components/e-ink/ed052tc4/README.md)
and [Inkplate 5 gaps §6](../inkplate-5/gaps-and-conflicts.md#6-no-e-ink-panel-datasheet).

**No pricing, availability, community or media research was done for this board.**

**Retrieval-date convention.** `2026-08-24` rows were mined then; `2026-08-28` marks a URL
status re-verification only — content behind those URLs was not re-fetched or re-compared.
