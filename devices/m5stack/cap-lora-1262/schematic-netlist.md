# Cap LoRa-1262 (U214) — net list traced from `U214-Cap-LoRa1262_SCH_V1.1_20251029.pdf`

**Traced:** 2026-09-07 · **Method:**
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md)
· **Tool:** poppler 26.06.0 plus a 300 dpi `pdftoppm` crop.

**New file.** Corrections to existing claims are appended to `pinouts-and-buses.md` and listed in
[`guides/reverse-engineering/schematic-tracing-corrections-2026-09-07.md`](../../../guides/reverse-engineering/schematic-tracing-corrections-2026-09-07.md).

## 0. Traceability

1 page, `Creator: Altium Designer`, **0 embedded rasters**, 516 words, full `CO`/`PI` coverage.
**No `NL` tokens on this export** — every label is ordinary visible text, so bindings were made
geometrically and then verified against a rendered crop.

---

## 1. `P1` — the Cap-Bus connector. **`HDR-SMD_14P-P2.54`.**

Fourteen pins, 2.54 mm pitch, SMD. **Each net carries two labels**: a functional alias and a
host-GPIO alias, both drawn on the same wire. The render was needed to establish that — from the
text layer alone one of them looks like an annotation.

| Pin | Symbol pin name | Host-GPIO alias | Functional alias | Pin token |
|---|---|---|---|---|
| 1 | `GPS-TX` | `G15` | — | `PIP101` @ 705.00, 506.37 |
| 2 | `GPS-RX` | `G13` | — | `PIP102` @ 705.00, 498.91 |
| 3 | `SCL` | **`GI`** (= GPIO1) | `SCL` | `PIP103` @ 705.00, 491.37 |
| 4 | `SDA` | **`GO`** (= GPIO2) | `SDA` | `PIP104` @ 705.00, 484.37 |
| 5 | `5VOUT` | — | `+5VOUT` | `PIP105` @ 705.00, 477.37 |
| 6 | `GND` | — | `GND` | `PIP106` @ 705.00, 470.37 |
| 7 | `5VIN` | — | `+5VIN` | `PIP107` @ 705.00, 462.91 |
| 8 | `RESET` | `G3` | **`RST`** | `PIP108` @ 633.00, 462.91 |
| 9 | `INT` | `G4` | `IRQ` | `PIP109` @ 633.00, 470.37 |
| 10 | `BUSY` | `G6` | `BUSY` | `PIP1010` @ 633.00, 477.37 |
| 11 | `SCK` | `G40` | `SCK` | `PIP1011` @ 633.00, 484.37 |
| 12 | `MOSI` | `G14` | `MOSI` | `PIP1012` @ 633.00, 491.37 |
| 13 | `MISO` | `G39` | `MISO` | `PIP1013` @ 633.00, 498.91 |
| 14 | `CS` | `G5` | `NSS` | `PIP1014` @ 633.00, 506.37 |

`GI` = GPIO1 and `GO` = GPIO2 is established independently on the Cardputer ADV, where the same
two net names land on module pins whose printed names are `G1` and `G2` — see
[`devices/m5stack/cardputer-adv/schematic-netlist.md`](../cardputer-adv/schematic-netlist.md) §2.
**Here the sheet corroborates it directly**: pin 3's symbol name is `SCL` and carries `GI`;
pin 4's is `SDA` and carries `GO`. That matches M5Unified's `EX SCL = GPIO_NUM_1`,
`EX SDA = GPIO_NUM_2` exactly.

## 2. Where pin 8 goes on **this** board

`RST` → `M1` pin 2, whose symbol pin name is `NRST` — the **`SX1262` reset** on the
`Stamp LoRa-1262 Mini` module (`M1`, 13 pins, value string at 649–696, 164.6).

`M1` pin map as printed:

| `M1` pin | Name | Net |
|---|---|---|
| 1 | `GND` | `GND` |
| 2 | `NRST` | `RST` |
| 3 | `BUSY` | `BUSY` |
| 4 | `IRQ` | `IRQ` |
| 5 | `3V3` | `VDD_3V3` |
| 6 | `CLK` | `SCK` |
| 7 | `MOSI` | `MOSI` |
| 8 | `MISO` | `MISO` |
| 9 | `NSS` | `NSS` |
| 10 | `BUSY` | — |
| 11 | `GND` | `GND` |
| 12 | `GND` | `GND` |
| 13 | `ANT` | to `E4` `SMA-KE` |

## 3. `U3` — on-board buck is a **JW5712**, and it is **permanently enabled**

The value string `JW5712` is printed at (140, 186.3), directly below the `U3` symbol, with the
vendor annotation **`IOUT: 0~0.6A`** at (155–175, 92.9).

| Ball | Name | Net |
|---|---|---|
| `A1` | `SW` | `L2` `WPN201610U2R2MT` 2.2 µH → `VDD_3V3` |
| `A2` | `VIN` | `+5V` / `+5VOUT` |
| `B1` | `EN` | **`R1` 10 kΩ pull-up to `+5V`** — `PIR102` @ 100, 121.1 · `PIR101` @ 100, 142.4 |
| `B2` | `GND` | `GND` |
| `C1` | `VSEL1` | strap |
| `C2` | `VOS` | `VDD_3V3` (remote sense) |
| `D1` | `VSEL2` | strap |
| `D2` | `VSEL3` | strap |

**`EN` is tied high through a resistor to the input rail. There is no host control of this
converter on U214.** Contrast with the Cap CC1101, where the same ball is driven by the host —
see §4.

## 4. Cap-Bus is identical on the Cap CC1101; only the *function* of each line differs

`U219-Cap_CC1101_SCH_V0.3_20260528.pdf` p1 uses the same connector (`HDR_14P-P2.54`), the same
symbol pin names and the **same host-GPIO aliases**. What changes is the functional alias:

| Pin | Symbol name | Host GPIO | U214 alias | U219 alias |
|---|---|---|---|---|
| 1 | `GPS-TX` | `G15` | — | `CC1101_G0` |
| 2 | `GPS-RX` | `G13` | — | `CC1101_RF_SW0` |
| 3 | `SCL` | `GI` (GPIO1) | `SCL` | `SCL` |
| 4 | `SDA` | `GO` (GPIO2) | `SDA` | `SDA` |
| 5–7 | `5VOUT`/`GND`/`5VIN` | — | same | same |
| **8** | `RESET` | **`G3`** | **`RST`** | **`POWER_EN`** |
| 9 | `INT` | `G4` | `IRQ` | `NFC_IRQ` |
| 10 | `BUSY` | `G6` | `BUSY` | `NFC_CS` |
| 11 | `SCK` | `G40` | `SCK` | `SPI_SCLK` |
| 12 | `MOSI` | `G14` | `MOSI` | `SPI_MOSI` |
| 13 | `MISO` | `G39` | `MISO` | `SPI_MISO` |
| 14 | `CS` | `G5` | `NSS` | `CC1101_CS` |

**The reported pin-8 conflict is not a conflict in the bus.** The connector part, the pin
number, the symbol pin name (`RESET`) and the host GPIO (`G3`) are identical on both boards. The
two documents disagree only about what each daughterboard *does* with that host line:

- **U214** routes `G3` to the SX1262's `NRST`.
- **U219** routes `G3` to `R1` 100 kΩ and to its own `U1` `JW5712` `EN` ball — the net is named
  `POWER_EN` (@ 146.12, 258.46 and 535.08, 258.46), and it **switches the CC1101 board's own
  3.3 V converter on and off.**

So `G3` is a per-board control line whose meaning the daughterboard defines, and the bus pinout
itself is stable. That is a materially different — and more useful — statement than "the
documents contradict each other".

> ⚠ **Worth flagging for the Cap CC1101 record, not resolved here:** U219's pins 9 and 10 are
> named `NFC_IRQ` and `NFC_CS`, but no NFC part appears on that board's designator census. These
> look like net names inherited from a sibling NFC design. They do not affect the bus pinout, but
> anyone reading the U219 sheet should not go looking for an NFC controller.

## 5. Other parts on U214

| Des | Part | Function |
|---|---|---|
| `U1` | `MAX2659` | GNSS LNA — `VCC`, `RFIN`, `SHDN`, `RFOUT`, `GND`; `L1` 6.8 nH ±5 %, `C5` 470 pF, `J1` `ANT181804` |
| `U2` | `PI4IOE5V6408ZTAEX` | I²C GPIO expander — `SCL`, `SDA`, `INT`, `ADDR`, `RESET`, `P0`…`P7`; `R7/NC` 10 kΩ on `ADDR` |
| `U3` | `JW5712` | §3 |
| `M1` | `Stamp LoRa-1262 Mini` | §2 |
| `M2` | `GP-02` | GNSS module — `TXD1`, `RXD1`, `1PPS`, `ON/OFF`, `VBAT`, `VCC`, `NRST`, `ANT`, `VCC_RF`, `SCL`, `SDA`; `R4` 0 Ω into `G15`/`G13` |
| `J1` | `ANT181804` | antenna |
| `J2` | `GROVE 4P` | `SCL`/`SDA`/`5V`/`GND`, `R3` 10 kΩ |
| `BT1` | `Battery` | with `FB3` 120 Ω/MB, `C8` 22 µF, `C9` 100 nF |
| `E4` | `SMA-KE` | LoRa antenna |

The `M2` `GP-02` GNSS module explains why bus pins 1 and 2 are named `GPS-TX`/`GPS-RX`: on
**this** board they genuinely are the GNSS UART. On the CC1101 board the same two lines are
re-used for `CC1101_G0` and `CC1101_RF_SW0`.

---

## Reproducing

```bash
nix-shell -p poppler-utils --run 'pdftotext -bbox-layout \
  "devices/m5stack/cap-lora-1262/artifacts/schematic/U214-Cap-LoRa1262_SCH_V1.1_20251029.pdf" /tmp/u214.xhtml'
cd scratch/schematic-tracing
python3 netlist.py /tmp/u214.xhtml --des P1
python3 render.py  /tmp/u214.xhtml --x0 560 --x1 842 --y0 400 --y1 560
# the crop that settled the two-labels-per-net question:
nix-shell -p poppler-utils imagemagick --run '
  pdftoppm -r 300 -png <pdf> /tmp/u214 &&
  magick /tmp/u214-1.png -crop 900x300+2350+1865 +repage -resize 180% /tmp/u214-p1.png'
```
