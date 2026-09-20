# Cap CC1101 (U219) — net list traced from `U219-Cap_CC1101_SCH_V0.3_20260528.pdf`

**Traced:** 2026-09-07 · **Method:**
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md)
· **Tool:** poppler 26.06.0.

**New file.** Corrections to existing claims are appended to `pinouts-and-buses.md` and listed in
[`scratch/schematic-tracing/corrections-requiring-review.md`](../../../scratch/schematic-tracing/corrections-requiring-review.md).

## 0. Traceability

3 pages, `Creator: Altium Designer`, **0 embedded rasters**, 974 words, full `CO`/`PI` coverage,
**no `NL` tokens** (same export setting as the Cap LoRa-1262). **Fully traceable.**

---

## 1. `P1` — Cap-Bus connector, `HDR_14P-P2.54`

Same connector part, same symbol pin names and same host-GPIO aliases as the Cap LoRa-1262. The
functional aliases differ, because they describe what *this* board does with each line.

| Pin | Symbol pin name | Host GPIO | Functional net on U219 | Pin token |
|---|---|---|---|---|
| 1 | `GPS-TX` | `G15` | `CC1101_G0` | `PIP101` @ 648.00, 506.37 |
| 2 | `GPS-RX` | `G13` | `CC1101_RF_SW0` | `PIP102` @ 648.00, 498.91 |
| 3 | `SCL` | `GI` (GPIO1) | `SCL` | `PIP103` @ 647.00, 491.37 |
| 4 | `SDA` | `GO` (GPIO2) | `SDA` | `PIP104` @ 648.00, 484.37 |
| 5 | `5VOUT` | — | `+5VOUT` | `PIP105` @ 648.00, 477.37 |
| 6 | `GND` | — | `GND` | `PIP106` @ 648.00, 470.37 |
| 7 | `5VIN` | — | `+5VIN` | `PIP107` @ 648.00, 462.91 |
| **8** | `RESET` | **`G3`** | **`POWER_EN`** | `PIP108` @ 575.00, 462.91 |
| 9 | `INT` | `G4` | `NFC_IRQ` | `PIP109` @ 575.00, 470.37 |
| 10 | `BUSY` | `G6` | `NFC_CS` | `PIP1010` @ 575.00, 477.37 |
| 11 | `SCK` | `G40` | `SPI_SCLK` | `PIP1011` @ 575.00, 484.37 |
| 12 | `MOSI` | `G14` | `SPI_MOSI` | `PIP1012` @ 575.00, 491.37 |
| 13 | `MISO` | `G39` | `SPI_MISO` | `PIP1013` @ 575.00, 498.91 |
| 14 | `CS` | `G5` | `CC1101_CS` | `PIP1014` @ 575.00, 504.84 |

## 2. Pin 8 — what `POWER_EN` actually controls

`POWER_EN` appears twice on sheet 1: at (535.08, 258.46) beside `P1` pin 8, and at
(146.12, 258.46) in the power block, where `netlist.py --components` reports

```
p1 R1  x=163.00 y=271.66  R1(2) | 100KΩ(11) | B1(20) | A2(21) | POWER_EN(21) | EN(34)
p1 U1  x=189.00 y=250.20  U1(2) | EN(14) | B1(14) | IOUT:(28) | R1(34) | SW(40)
```

`U1` is the board's own step-down converter (`EN`/`SW`/`VIN`/`VOS`/`VSEL1..3`/`GND` ball map,
`IOUT: 0~0.6A` annotation, `L1` `MWTC201608S2R2` 2.2 µH). `R1` is **100 kΩ** here, and the `EN`
ball is driven by `POWER_EN` = host `G3`.

**So on the Cap CC1101 the host GPIO on bus pin 8 gates the daughterboard's own 3.3 V rail.**
On the Cap LoRa-1262 the equivalent ball is instead tied high through `R1` 10 kΩ to the input
rail, and bus pin 8 goes to the SX1262's `NRST`.

This is the whole of the reported "pin 8 conflict":

- the **bus** pinout is identical on both boards — same connector, same pin number, same symbol
  name `RESET`, same host GPIO `G3`;
- the **board function** of that line is defined by the daughterboard, and the two boards define
  it differently.

Practical consequence for firmware: driving `G3` low on a Cap CC1101 **removes power from the
radio**, whereas on a Cap LoRa-1262 it merely asserts the radio's reset. Code written for one
must not be reused on the other without changing the meaning of that pin.

## 3. ⚠ `NFC_IRQ` and `NFC_CS` — vestigial net names

Bus pins 9 and 10 carry the net names `NFC_IRQ` (@ 531.24, 265.65 p1; also @ 192.64, 265.65 p2)
and `NFC_CS` (@ 529.74, 272.84 p1; @ 191.14, 280.03 p2). **No NFC controller appears anywhere in
this document's designator census.** These read as names carried over from a sibling design that
did have one.

Recorded, not resolved: the names are misleading but the electrical routing is what matters, and
it is given above. Do not search for an NFC part on this board on the strength of them.

## 4. Off-sheet nets

Sheet 1 ↔ sheet 3 connectivity is by net name only, and it is the only evidence of it:

| Net | Sheet 1 | Sheet 3 |
|---|---|---|
| `CC1101_CS` | 534.06, 301.59 | 101.69, 107.27 |
| `CC1101_G0` | 706.90, 301.59 | 101.63, 121.64 |
| `CC1101_RF_SW0` | 715.06, 294.40 | 95.41, 380.66 · 563.75, 373.48 |
| `CC1101_RF_SW1` | — | 109.79, 128.83 · 95.41, 373.47 · 563.75, 380.66 |
| `CC1101_RF` | — | 750.13, 359.10 · 750.13, 481.54 |
| `NFC_IRQ`, `NFC_CS` | 531.24 / 529.74, 265.65 / 272.84 | p2: 192.64 / 191.14 |
| `I2C_EN` | — | p2: 259.66, 254.87 |

`CC1101_RF_SW0` / `CC1101_RF_SW1` appear at two x positions on sheet 3 in the same two rows
(95.41 and 563.75, y 373.47/380.66) — an RF switch with the two control lines crossed between
its two ports, which is what an antenna-path selector looks like. `CC1101_RF` appears twice on
sheet 3 at the same x, 122 pt apart in y: the two ends of the RF path.

---

## Reproducing

```bash
nix-shell -p poppler-utils --run 'pdftotext -bbox-layout \
  "devices/m5stack/cap-cc1101/artifacts/schematic/U219-Cap_CC1101_SCH_V0.3_20260528.pdf" /tmp/u219.xhtml'
cd scratch/schematic-tracing
python3 render.py  /tmp/u219.xhtml --page 1 --x0 490 --x1 750 --y0 245 --y1 320
python3 netlist.py /tmp/u219.xhtml --components | grep -E ' (U1|P1|R1) '
python3 trace.py   grep /tmp/u219.xhtml 'CC1101_|NFC_'      # the off-sheet census
```
