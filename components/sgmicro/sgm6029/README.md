# SG Micro SGM6029

- **Part as fitted:** `SGM6029CYG/TR`
- **Category:** **buck-boost** DC-DC converter, 3.3 V output
- **Package:** BGA-6, footprint `BGA6-0.35-0.745X10.95X0.4MM`
- **Retrieved:** 2026-08-24
- **Evidence:** KiCad BOM + PCB netlist of the XIAO ESP32S3 Sense v1.5 package, plus schematic annotations. **SG Micro datasheet not obtained in this pass.**

## Role and why buck-boost matters

Generates the board's **`VCC_3V3`** rail from `VIN`, where `VIN` is whichever of USB `VBUS` (via D2 Schottky) or the battery `VBAT` (via Q1 P-MOS) is present.

A **buck-boost** topology is the important design choice. A Li-ion cell falls from ~4.2 V to ~3.0 V over discharge, crossing the 3.3 V output. A buck-only regulator or an LDO would lose regulation partway through the discharge; the buck-boost holds 3.3 V across the whole range. Schematic annotation confirms the intended input span: **"3.7~5V"**.

## Key parameters (from schematic annotations)

| Parameter | Value | Source |
|---|---|---|
| Output | 3.3 V (`VCC_3V3`) | netlist |
| **Max output current** | **600 mA** | schematic annotation `Imax=600mA` |
| Input range (as used) | 3.7–5 V | schematic annotation |
| Feedback network | R13 = 249 kΩ (C1 pin), R6-adjacent divider | netlist |
| Inductor | **L4 = 470 nH** | BOM |
| Input caps | C3 2.2 µF, C4 4.7 µF | BOM |
| Output caps | C5 4.7 µF, C6 4.7 µF | BOM |
| `MODE` pin | C1 | netlist |

Pins as wired: `VIN` B1, `EN` C2, `GND` A1, `SW` B2, `VOS` A2, `MODE` C1.

## Limits and caveats

- **600 mA is the whole board's 3.3 V budget** — SoC, flash, and everything across the board-to-board connector (camera, microphone, microSD). The OV5640 alone draws 140 mA. Peripherals added on the user header share what is left.
- The `3V3` header pin is an **output**. Do not back-feed it.
- Switching frequency, efficiency curves, and `MODE` pin semantics (PFM/PWM selection) are **not established here** — obtain the SG Micro datasheet.

## Used by

### Seeed Studio XIAO ESP32S3 Sense

Reference designator **U3**. Supplies `VCC_3V3` to the ESP32-S3R8 (pins 20, 46, 55, 56), the GD25Q64 flash, the 10 kΩ boot/reset pull-ups, the user LED via R15, the 14-pin header pin 12, and the daughterboard via J3 pins 18/19.

Note the revision history: in **v1.3 the silkscreen for U3 was removed** along with K1, K2 and U4 — a cosmetic change on the current board.

Power tree: [../../devices/seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md](../../../devices/seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md#8-power-tree)

## Related
- [SGM40567](../sgm40567/README.md) — the charger upstream
- [ESP32-S3R8](../../espressif/esp32-s3r8/README.md)
