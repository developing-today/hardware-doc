# BOM and board construction — XIAO ESP32S3 Sense

> Full reference-designator BOM parsed from Seeed's KiCad source, plus physical construction.
> Snapshot **2026-08-24**. Source: `03 XIAO ESP32-S3-Sense.kicad_sch` / `XIAO ESP32S3_V1.5.kicad_pcb`, parsed with [`tools/parse_kicad_sch.py`](../../../tools/parse_kicad_sch.py) and [`tools/kicad_pcb_nets.py`](../../../tools/kicad_pcb_nets.py). **83 placed components.**

## Physical construction

| Property | Value | Source |
|---|---|---|
| Outline | **17.780 × 21.135 mm** | `Edge.Cuts` bounding box |
| Layers | **4** — `F.Cu`, `In1.Cu`, `In2.Cu`, `B.Cu` | `.kicad_pcb` layer table |
| Design licence | **CC BY-SA 4.0** | `U8` = footprint `Misc:LOGO_CC_BY-SA_4.0` on every sheet |
| Passive size | Predominantly **0201**; L4 is 0603 | footprint names |
| Footprint library | `XIAO ESP32S3_V1.3` | corroborates the [revision conflict](gaps-and-conflicts.md#2-the-schematics-own-revision-number-contradicts-its-filename) |
| Construction | **Two-board sandwich** — mainboard + Sense daughterboard via J3 | — |

17.78 mm is exactly 0.700 inch. All SMD components are on one side, which is what lets the XIAO act as a solderable module.

**Uneven rounded corners are normal.** Seeed's FAQ explains these are depanelisation tabs: the board is so dense that panel connections could only be placed at the four corners. Not a defect.

## Active components

| Ref | Part | Function | Footprint |
|---|---|---|---|
| **U1** | **ESP32-S3R8** | Dual-core SoC, 8 MB in-package octal PSRAM | `QFN56G-0.4-7X7MM` |
| **U3** | **SGM6029CYG/TR** | Buck-boost → 3V3, **600 mA max** | `BGA6-0.35-0.745X10.95X0.4MM` |
| **U4** | **SGM40567-4.2XG/TR** | Li-ion linear charger, 4.2 V | `WLCSP-0.4-0.92X1.16X0.4MM` |
| **U5** | **GD25Q64ENIGR** | 8 MB QSPI NOR flash | `USON8-0.8-4X3MM` |
| U8 | — | CC BY-SA 4.0 silkscreen logo | `Misc:LOGO_CC_BY-SA_4.0` |
| **U9** | XIAO-Add-On | 14-pin castellated user header | `XIAO-14P-Add-On` |
| **J3** | **DF40C-30DP-0.4V(51)** | 30-pin B2B → Sense daughterboard | `BTB30-0.4-7.52X2.97X1.14` |
| **USB0** | UBF31-0171 | USB 2.0 Type-C receptacle | `USB2.0-TYPE-C` |
| **ANT1** | U.FL-R-SMT-1 | IPEX-1 antenna receptacle | `U-FL3P-SMD-2.6X2.6X1.0MM` |
| **Q1** | LP0404N3T5G | P-MOS, battery path select | `PMOS_1.0_0.6_0.35MM` |
| **D2** | LMBR4010BST5G | Schottky, USB path select | `DFN1006-2L` |
| **D3** | Yellow LED | User LED (GPIO21, **active-low**) | `LED-0402` |
| **CHG0** | Red LED | Charge status (`NCHG`) | `LED-0402` |
| **K1** | SKTAAAE010/311021459 | **RESET** — shorts `EN` to GND | `SW4-SMD-2.8-2.6X1.6X0.53MM` |
| **K2** | SKTAAAE010/311021459 | **BOOT** — shorts `GPIO0` to GND | idem |
| **X1** | 40 MHz / 306011364 | Main crystal | `X4-SMD-1.6X1.2X0.35MM` |

## Passives

| Ref | Value | Role |
|---|---|---|
| R1, R2 | 5.1 kΩ | USB-C **CC pull-downs** (UFP) — correct for C-to-C charging |
| R3, R4 | 22 Ω | USB D−/D+ series termination |
| R6 | 499 Ω | Series on `U0TXD` (GPIO43) → `D6/TX` |
| R7 | 10 kΩ | `GPIO0` pull-up (BOOT) |
| R8 | 10 kΩ | `EN` pull-up (RESET) |
| R9 | 100 kΩ | VBUS sense divider |
| **R10** | **220 kΩ** | **Charger `IREF` — sets charge current: `24000/220K = 110 mA`** |
| R11 | 10 kΩ | Charge-LED series |
| R13 | 249 kΩ | SGM6029 feedback |
| R15 | 1.5 kΩ | User-LED series |
| L1 | 2 nH | RF supply choke |
| L2 | 3.3 nH | Antenna match |
| L4 | 470 nH | SGM6029 switching inductor (0603) |
| **L5** | **24 nH** | Crystal path — **was R5 = 0 Ω before v1.2** |
| C3–C6, C9–C16, C19, C21–C23, C25, C26, C28–C30 | 10 pF…4.7 µF | Decoupling, filtering, crystal load (C7/C8 = 10 pF) |
| C18 | 1 pF | Antenna match |

**Test points:** TP1 (unconnected), TP2 `PDM_CLK`, TP3 `PDM_DATA`, TP4 `CAM_SDA`, TP5 `CAM_SCL`, TP6 `EN`, TP7 `USB_D−`, TP8 `USB_D+`. Plus pads `BAT0` (`VBAT`) and `GND0`.

TP6/TP7/TP8 are genuinely useful and undocumented: a board with a damaged USB-C receptacle can still be flashed by tacking wires to TP7/TP8, and TP6 lets an external programmer assert reset.

## Do-not-populate parts

Five footprints are marked **DNP**. Their purpose is **not documented by Seeed** — the readings below are inference from placement and are labelled as such.

| Ref | Location | Likely purpose (**inferred**) |
|---|---|---|
| C1, C2 | On `ESP_USB_D+` / `ESP_USB_D−`, tied to the R3/R4 junction | Optional USB EMI/common-mode capacitors. Populating them would degrade USB 2.0 full-speed signal integrity, so they are almost certainly an EMC contingency |
| C17, L3 | In the antenna network between `ANT1.D` and the match | **Alternate antenna match / antenna-select** path. C17 provides a series-cap option and L3 a shunt/series-inductor option |
| C20 | Adjacent to L3 | Part of the same alternate match |

These are ordinary RF/EMC contingency footprints — a designer leaves several match topologies available and populates whichever passes certification. If you retune for a very different antenna, this is where you would work. Nothing in Seeed's documentation sanctions it.

## Revision history

From sheet `01 Descriptions`:

| Rev | Date | By | Change |
|---|---|---|---|
| v1.0 | 2023-01-04 | wei.Xing | Initial version |
| v1.1 | 2023-03-27 | Linus.Liao | — |
| **v1.2** | **2023-07-25** | Linus.Liao | **R5 changed from 0 Ω to L5 = 24 nH** (crystal drive / EMC) |
| **v1.3** | **2025-10-21** | Linus.Liao | Remove silkscreen for K1, K2, U3, U4; adjust C30 and C16 inward; optimise shield positioning-hole clearance |

**No v1.4 or v1.5 entry exists**, despite the package being published as v1.5. See [`gaps-and-conflicts.md` §2](gaps-and-conflicts.md#2-the-schematics-own-revision-number-contradicts-its-filename).

The v1.2 change is the only electrically meaningful one: boards older than v1.2 have a plain 0 Ω link where current boards have a 24 nH inductor in the crystal path.


## Revision comparison — verified against both schematics

The revision table above is Seeed's own text block. I verified it by parsing **both** published schematics and diffing the component lists:

- **v1.1** — `XIAO ESP32S3_v1.1.sch`, EAGLE 9.6.2, 2023-03-28 (107 reference designators)
- **v1.5** — `03 XIAO ESP32-S3-Sense.kicad_sch`, KiCad 9, 2026-02 (71 reference designators)

The raw diff is dominated by **EDA-tool artefacts**, not design changes: EAGLE places a `GND_POWER` symbol per ground connection (`G1`–`G42`), which KiCad does not; `USB` was renamed `USB0`; test points gained explicit designators (`BAT0`, `GND0`); and `U8`/`U9` are the CC BY-SA logo and the header symbol.

Filtering those out, the **entire electrical delta between v1.1 and v1.5** is:

| Change | v1.1 | v1.5 | Matches revision note? |
|---|---|---|---|
| Crystal path | **`R5` = 0 Ω** | **`L5` = 24 nH** | ✅ v1.2, "R5 changed 0R→L5 24nH" |
| Unpopulated positions | `J1`, `J2` (both **DNP**) | *removed* | ❌ **not mentioned in the revision history** |

**Every other component — all capacitors, all resistors, both regulators, the charger, flash, MOSFET, Schottky, crystal, antenna connector, buttons and the B2B connector — is identical in value and designator across the two revisions.**

That is a useful result in two directions:

1. **It confirms Seeed's revision history is accurate.** The single electrically meaningful change in three years is the crystal-path inductor. If you have a pre-v1.2 board, that is the only difference that matters.
2. **It found one omission.** Two DNP positions (`J1`, `J2`) present in v1.1 were dropped by v1.5 without appearing in the revision notes. Their purpose is unknown — DNP headers of this kind are typically factory test or programming points. Low impact, but it means the revision block is not exhaustive.

> Method: [`tools/eagle_netlist.py`](../../../tools/eagle_netlist.py) and [`tools/parse_kicad_sch.py`](../../../tools/parse_kicad_sch.py), both run 2026-08-24. The comparison is **primary evidence** — two independent vendor files, not vendor prose. See the reusable [netlist-recovery guide](../../../guides/reverse-engineering/netlists-from-vendor-eda-files.md).

## Charge-current modification

R10 sets charge current by `I ≈ 24000 / R10(Ω)`:

| R10 | Implied charge current |
|---|---|
| 330 kΩ | ~73 mA |
| **220 kΩ (stock)** | **~110 mA** |
| 150 kΩ | ~160 mA |
| 110 kΩ | ~218 mA |

Useful for larger cells, where ~110 mA is slow. **Cautions:** the SGM40567 is a *linear* charger, so extra current becomes heat in a 0.92 × 1.16 mm WLCSP on a 21 mm board; and this is **`inferred` from a schematic annotation, untested**. See [`components/sgmicro/sgm40567`](../../../components/sgmicro/sgm40567/README.md).

## What is *not* here

The **Sense daughterboard has no published schematic or BOM**. Everything above is the mainboard. The camera, PDM microphone and microSD slot, their decoupling, level shifting and pull-ups are all unknown — see [`gaps-and-conflicts.md` §6](gaps-and-conflicts.md#6-j3-board-to-board-pinout-is-undocumented--resolved-2026-08-24).

## Related
- [`pinouts-and-buses.md`](pinouts-and-buses.md) · [`resources-and-conflicts.md`](resources-and-conflicts.md) · [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
