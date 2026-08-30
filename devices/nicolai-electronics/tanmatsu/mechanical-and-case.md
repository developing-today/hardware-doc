# Mechanical design and case — Tanmatsu

> Case, board revisions, and how to regenerate the printable files.
> Snapshot **2026-08-24**. Source: [`tanmatsu-mechanical`](https://github.com/Nicolai-Electronics/tanmatsu-mechanical) @ `c623cd54` (2026-07-03), **CERN-OHL-P**.
> **No hardware was available** — nothing here was printed, fitted or measured.

## What is in the repository

| File | Size | What |
|---|---:|---|
| `Tanmatsu_3D-printed.FCStd` | 16.3 MB | **FreeCAD master design** — all parts integrated |
| `Tanmatsu_3D-printed-ebyte.FCStd` | 20.4 MB | Variant for the **Ebyte LoRa module** build |
| `tanmatsu.step` | 34.1 MB | Mainboard PCB as STEP |
| `frontpanel.step` | 11.4 MB | Front panel PCB as STEP |
| `tools/freecad_export.py`, `tools/export_manufacturing_files.sh` | — | Automated export pipeline |
| `.github/workflows/{build,release}.yml` | — | CI that builds and publishes the printable files |

Printable parts, per the README: **case**, **spacer**, **speaker adapter**.

The design is in **FreeCAD**, not a proprietary CAD tool — consistent with the rest of the project's open-source stance. Individual **STEP files are exported per part** so you can print directly from the repository without opening FreeCAD at all.

Overall device size (from the specifications page): **120 × 135 × 18 mm**, **215 g** including case and battery.

## Board revisions — and how to identify yours

This is the most useful thing in the repository, and it resolves a question the hardware repo cannot answer.

> *"You can find out your mainboard revision by going to `Settings > Device information` in the launcher firmware."*
>
> *"If you have board revision 1 or 2 you need the 'for revision 2' files. If you have a newer board revision you need the 'for revision 3' files."*

So **at least three mainboard revisions exist** (1, 2, 3), and the launcher reports which one you have — a software-readable revision, not a silkscreen hunt.

**The case is not compatible across the rev2/rev3 boundary:**

> *"The breaking change in case design is due to us having to move the audio jack down by two millimetres and outwards by two millimetres to solve a manufacturing problem."*

A 2 mm × 2 mm relocation of the 3.5 mm jack. If you print the wrong case revision, the headphone socket will not line up.

⚠ This matters for the [`tanmatsu-hardware`](https://github.com/Nicolai-Electronics/tanmatsu-hardware) repo too: it carries **no revision marking**, and its last commit is 2026-02-25. The mechanical repo confirms revisions have continued past whatever the KiCad files represent, so **the published schematic may not match a current unit**. See [`gaps-and-conflicts.md` §4](gaps-and-conflicts.md).

## Regenerating the printable files

```bash
# from the repository root, with FreeCAD CLOSED
./tools/export_manufacturing_files.sh
```

STEP and AMF files appear in `./release/` with correct names.

**Prerequisite:** install the **Fasteners** workbench via FreeCAD's add-on manager — the design uses it for bolts.

> ⚠ Known issue, documented by the authors: *"The script does produce some errors from the Fasteners Workbench."* Tracked upstream at [FreeCAD_FastenersWB#454](https://github.com/shaise/FreeCAD_FastenersWB/issues/454). The errors are expected and do not prevent export.

`tools/test_freecad_file.FCStd` is a deliberately small file for debugging the export scripts without waiting on the full design.

> Status: **`reported-working`** — quoted from the repository README. Not executed here (FreeCAD not available in this environment).

## Importing updated PCBs into the case design

If you modify the electronics and need the case to follow, the README gives the exact procedure:

1. Clone both the **mainboard** and a **frontpanel** repository
2. Open the design in **KiCad** → PCB editor → *Export → "STEP / GLB / etc."*
3. Choose **STEP**, default settings, Export
4. Import into the FreeCAD file — **disable the `Linkgroup` setting while importing**, *"otherwise deleting the PCB will become very tiresome"*
5. Position by setting `Data → Placement → Position → z`:

| Part | Z offset |
|---|---|
| **Tanmatsu mainboard PCB** | **−1.55 mm** |
| **Front panel PCB** | **+2.40 mm** |

Those two Z offsets are the practical detail you would otherwise have to reverse-engineer.

## Front panels are a designed extension point

The front panel is a **separate PCB**, and Badge.Team explicitly support custom ones:

> *"Custom front panels are feasible using the provided information, and 3D printable case designs are also available for those interested in additional customization."*

Nicolai Electronics publish two ready-made alternatives:

| Repo | Design |
|---|---|
| [`tanmatsu-frontpanel-cyberdeck`](https://github.com/Nicolai-Electronics/tanmatsu-frontpanel-cyberdeck) | Cyberdeck front panel |
| [`tanmatsu-frontpanel-honeycomb`](https://github.com/Nicolai-Electronics/tanmatsu-frontpanel-honeycomb) | Honeycomb front panel |

Badge.Team also document front-panel artwork at [`konsool/hardware/frontpanel/artwork/`](https://badge.team/docs/badges/konsool/hardware/frontpanel/artwork/).

Since the front panel is what retains the [KeebDeck keypad](keyboard.md), a custom front panel is also a keyboard-mechanics decision — the KeebDeck documentation requires ≥0.2 mm padding if a PCB is used as the retaining cover.

## Licensing and attribution

**CERN-OHL-P**, with copyright shared three ways:

- Copyright 2024–2025 **Nicolai Electronics**
- Copyright 2024–2025 **Ytec Engineering**
- Copyright 2025 **Jelle Haandrikman**

**Ytec Engineering** appears only here — not in the electronics repository — so the mechanical design involved an outside engineering firm. Worth noting if you are tracing who designed what.

As with the electronics, **branding is excluded**: names, logos and artwork remain all rights reserved and may not be reproduced on derivative works.

---

## Extracted from the FreeCAD document (no CAD required)

FreeCAD `.FCStd` files are **ZIP archives**; `Document.xml` inside carries the full object tree. This
lets several "locked in FreeCAD" questions be answered without the application — `unzip -p file.FCStd
Document.xml`. FreeCAD and CadQuery were both unavailable here (CadQuery fails on a missing
`libstdc++`), so this is the fallback path.

`Tanmatsu_3D-printed.FCStd` is **130 MB uncompressed across 4,440 entries**, with a 5.4 MB
`Document.xml` and **1,669 uniquely-labelled objects**.

### Fasteners — answered

| Item | Value |
|---|---|
| **Screws** | **M2 × 12 mm** (`M2x12-Screw`, 7 instances) |
| **Nuts** | **M2** (`M2-Nut`, 7 instances) |

So the case closes with **seven M2×12 screws and seven M2 nuts**. The nuts are captive — there is a
dedicated `sketch_space_nuts` / `space_for_nuts` feature pair in the model. The 18650 expansion board
separately documents **M2 mounting holes**, consistent with M2 throughout.

### Model structure

Named features reveal how the case is composed:

```
spacer · Spacer_outline · sk_screwholes / screwholes
sketch_screen_outline / screen_outline
sketch_keyboard_outline / keyboard_outline
sketch_LED_outlines / LED_outlines
sketch_space_LORA_USB-A / space_LORA_USB-A
sketch_space_buttons / space_buttons
sketch_space_nuts / space_for_nuts
keycord_holes · frontpanel_silkscreen000..017+
```

Two things worth drawing out: there are **`keycord_holes`** — the case is designed for a lanyard — and
a single combined cut-out for **LoRa + USB-A** (`space_LORA_USB-A`), which is why the antenna and host
port sit together on one edge.

The document also embeds full 3D models of fitted parts (ESP32-C6-WROOM-1 module, 0201 passives), which
is why it is 130 MB.

### Extrusion depths

Distinct `Length` values on `Pad` features, i.e. feature thicknesses in mm:

```
1.0  1.5  1.6  1.8  2.0  2.4  2.8  3.0  3.4  3.8  4.2  4.5  5.0(×17)  6.0
7.8  10.0(×3)  12.0(×4)  15.0(×3)  17.5  58.1  199.3
```

**5.0 mm dominates (17 of 48)** and is most likely the principal wall/boss thickness; 12.0 mm matches
the M2×12 screw length. These are **feature extrusions, not a wall-thickness specification** — treat as
indicative, and measure in CAD before relying on any of them.

> Method caveat: this reads labels and property values out of the document XML. It cannot resolve the
> boolean history, so it tells you **what features exist and how deep they extrude**, not the final
> geometry. For tolerances, open the file properly.

---

## Gaps

| Question | Status |
|---|---|
| What changed between revisions 1 → 2? | **Unknown.** Only the rev2 → rev3 audio-jack change is documented |
| Which revision is currently shipping? | **Unknown.** Determinable per-unit via `Settings > Device information`, but not published |
| Print settings — material, layer height, supports, tolerances | **Not published** in the README |
| Case wall thickness, fastener sizes and count | **Largely resolved** — **7 × M2×12 screws + 7 × M2 nuts**, dominant 5.0 mm extrusion. Extracted from `Document.xml`; see above. True wall thickness still needs CAD |
| Is the `-ebyte` variant needed for all LoRa builds, or only some? | **Unclear.** All current Tanmatsus ship with an Ebyte module, so the distinction is unexplained |
| Are `release/` artifacts published? | The directory is an empty `.gitkeep`; CI (`release.yml`) presumably publishes to GitHub Releases — **not checked** |

## Related

- [`README.md`](README.md) — device overview and dimensions
- [`keyboard.md`](keyboard.md) — the front panel retains the keypad
- [`bom.md`](bom.md) — connector and PCB details
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — hardware revision uncertainty
