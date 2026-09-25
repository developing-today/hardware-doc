# How do I mount the DinMeter?

**Applies to:** K134 and K134-V11 — **byte-identical published STL** (SHA-256 `90f04d6a…`), same
53 × 30 × 32 mm body, same cutout.
**Evidence status:** dimensions from the vendor drawing and specification tables; **no unit was
physically fitted to a panel here**. **Last verified:** 2026-09-04.

---

## "DIN" here means the panel cutout, not the rail

This is the single most common misunderstanding about the product, and it costs people money.

| | What it means | Does the DinMeter do it? |
|---|---|---|
| **1/32 DIN** (DIN 43700 panel-cutout series) | A standard **aperture** cut into a panel: **45 × 22.5 mm** | **Yes — this is the product** |
| **DIN rail** (TS-35 / EN 60715 hat rail) | The 35 mm rail inside a cabinet that breakers clip onto | **No.** M5Stack's rail-mount product is the StamPLC |

The 1/32 DIN aperture is the size a generation of panel meters and temperature controllers
(Omron E5C, Autonics TZN, Fuji PXR and their many imitators) used, so it exists — already cut,
already wired, often already fed with 24 V — in a very large installed base of machine consoles,
process racks and cabinet doors. **Dropping a modern Wi-Fi UI into that hole with no panel work
is the entire product thesis.**

## Numbers

| Property | Value | Source |
|---|---|---|
| Panel cutout | **45.0 × 22.5 mm** (1/32 DIN) | both product pages, Features list |
| Body | **53.0 × 30.0 × 32.0 mm** | both spec tables |
| Weight | 17.8 g | both spec tables |
| Depth behind the panel | ~32 mm minus the bezel — **allow ~35 mm clear** including the DC terminal and Grove cables | `inferred` from the body depth; the drawing was not dimensioned to a bezel line here |
| Package (v1.0) | 136.0 × 93.0 × 23.0 mm, 47.0 g gross | v1.0 spec table |
| Package (v1.1) | 136.0 × 95.0 × 24.0 mm, 44.9 g gross | v1.1 spec table |
| Operating temperature | **0 – 40 °C** | both spec tables |

Vendor drawing: [`../artifacts/mechanical/K134-din_meter_asm_v1-dimensions.pdf`](../artifacts/mechanical/K134-din_meter_asm_v1-dimensions.pdf)
(117 405 B, SHA-256 `db42c8a995b6d0bf…`).
3D model: [`../artifacts/mechanical/DinMeter.stl`](../artifacts/mechanical/DinMeter.stl)
(573 284 B, SHA-256 `90f04d6a0ae2cbb6…`) — use it for clearance checks, not for tolerancing.

## Two mounting methods

The v1.1 page states them explicitly; the v1.0 bundle contains the same means under different
names.

| Method | Bundled part | When to use |
|---|---|---|
| **Screw-hole fixation** | v1.0 "back bracket" / v1.1 "plastic back clip" | Permanent installs, anything that vibrates, anything a person will push against |
| **Double-sided adhesive** | adhesive tape (both bundles) | Thin panels, prototypes, non-load-bearing faces |

Use the clip for anything real. A 17.8 g device on a machine that vibrates will eventually part
company with adhesive tape, and it will take its 24 V wiring with it.

## Connectors and clearances

Everything is on the back:

| Item | Note |
|---|---|
| **DC screw terminal** `J1` (2-pin 2.54 mm, green — [`dorabo/db2ek-2.54-2p`](../../../../components/dorabo/db2ek-2.54-2p/README.md)) | 6–36 V. **Strain-relieve it** — it is a screw terminal on a small body. The number behind that warning: **M1.6 screws, 0.1 N·m maximum torque**, 5–6 mm strip length, 26–20 AWG |
| USB-C | on the Stamp module; used for flashing and 5 V |
| PORT.A / PORT.B | HY2.0-4P, need ~10 mm of cable bend radius each |
| Battery | 1.25 mm 2-pin JST-style; the bundled cell tucks inside |
| Back clip | removable |

**Plan for depth.** Body depth plus a right-angle DC wire plus two Grove cables is realistically
45–55 mm behind the panel face. In a shallow door, check before you commit.

## Environmental reality check

- **0 – 40 °C is narrow.** A sealed cabinet in summer sun exceeds it; an unheated outbuilding in
  winter goes below it. Neither is a "maybe" — it is outside the vendor's stated range.
- **No IP rating is published.** There is no gasket in the bundle and none is mentioned. Treat
  the front face as **not sealed**: no washdown, no coolant mist, no dust-laden air without
  your own gasket.
- The Wi-Fi antenna is **behind the panel**, inside whatever the enclosure is made of. If that is
  steel, expect attenuation — see [`wifi-and-ble.md`](wifi-and-ble.md).

## Pitfalls

| Mistake | Consequence |
|---|---|
| Buying it expecting DIN-rail mounting | It does not clip to a rail. Buy a StamPLC |
| Not checking rear depth | It will not close the door |
| Adhesive mounting on a vibrating machine | It falls out |
| Assuming an IP rating | None is published |
| 36 V continuous | `C24`, the buck input capacitor, is rated **35 V**. Treat 36 V as absolute maximum; see [`power-and-battery.md`](power-and-battery.md) |
| Deploying outside 0–40 °C | Outside spec |

## Unresolved

- **Bezel dimensions and panel-thickness range are not published.** The maximum panel thickness
  the clip accommodates is unknown. Measure before ordering for a specific panel.
- No IP/NEMA rating published.
- No vibration or shock rating published.
- The published STL is **identical for v1.0 and v1.1**, so it cannot be used to detect any
  mechanical revision — see [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md) §3.
