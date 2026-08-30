# Hirose DF40C-30DP-0.4V(51)

- **Category:** 0.4 mm-pitch board-to-board connector, **30 signal contacts** + 4 mechanical tabs
- **Series:** Hirose **DF40** — stacking board-to-board / floating-mate family
- **Retrieved:** 2026-08-24
- **Evidence:** recovered from the KiCad BOM and PCB netlist of the Seeed XIAO ESP32S3 Sense v1.5 design package. **Hirose's own datasheet was not obtained in this pass** — the part-number decode below is inferred from the Hirose DF40 series convention and should be confirmed against Hirose documentation before use in a new design.

## Part number decode (inferred)

| Field | Meaning |
|---|---|
| `DF40` | Hirose DF40 board-to-board series |
| `C` | series/variant designator |
| `30` | **30 contacts** |
| `D` | dual row |
| `P` | plug (header) — the mating half is a receptacle |
| `0.4V` | **0.4 mm pitch**, vertical mating |
| `(51)` | Hirose packaging/plating suffix |

Board footprint on the XIAO: `BTB30-0.4-7.52X2.97X1.14` — i.e. approximately **7.52 × 2.97 mm body, 1.14 mm height**.

## Why it matters

DF40 is a **fine-pitch, low-stack-height** connector intended for rigid board-to-board stacking in space-constrained consumer devices. At 0.4 mm pitch it is not hand-solderable in practice and is **mechanically fragile** — the dominant failure mode for the device that uses it.

## Limits and caveats

- **0.4 mm pitch.** Bent contacts are not realistically repairable by hand, and a broken receptacle on a mainboard usually ends the board's life.
- **Vertical mating only.** The mating force must be applied perpendicular to the board plane; prying or twisting damages the housing.
- Contact current rating, mated height and durability (insertion cycles) are **not established here** — obtain the Hirose datasheet before designing with it.

## Used by

### Seeed Studio XIAO ESP32S3 Sense

Reference designator **J3**. This is the sole electrical and mechanical interface between the XIAO mainboard and the detachable Sense daughterboard (camera + PDM microphone + microSD).

**Seeed publishes no pinout for this connector.** The complete 34-pad mapping was reconstructed from the PCB netlist and is documented at [../../devices/seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md](../../../devices/seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md#2-the-j3-board-to-board-connector-sense-daughterboard-interface). Summary of what crosses it:

| Group | Pads |
|---|---|
| Camera DVP + SCCB | 6–14, 21–25 (GPIO10–18, 38, 39, 40, 47, 48) |
| PDM microphone | 26, 27 (GPIO41, 42) |
| microSD SPI | 3, 4, 5, 16 (GPIO7, 8, 9, 21) |
| Power | 15, 30 = `VIN` · 18, 19 = `VCC_3V3` |
| Ground | 1, 17, 28, 29, 31, 33, 34 |
| Spare | **2 (GPIO3)** — routed but unused by the stock daughterboard |
| No connect | 20, 32 |

Two design-relevant observations: **pad 2 (GPIO3) is a free signal** already routed across the connector for anyone building a custom daughterboard, and **both `VIN` (unregulated system node) and `VCC_3V3` are available**, so a custom board can do its own regulation instead of loading the mainboard's 600 mA 3V3 rail.

**Handling.** Seeed's own instruction: slide the boards apart laterally, working along one edge first — *never* pull straight up or down, and never twist the pair "like opening a book". See [../../devices/seeed-studio/xiao-esp32s3-sense/features/camera.md](../../../devices/seeed-studio/xiao-esp32s3-sense/features/camera.md#7-handling-the-daughterboard).

## Related
- [ESP32-S3R8](../../espressif/esp32-s3r8/README.md) — the SoC whose pins cross this connector
- [OV3660](../../omnivision/ov3660/README.md) — the camera on the far side
