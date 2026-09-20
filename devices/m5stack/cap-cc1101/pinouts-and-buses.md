# Pinouts and buses — Cap CC1101 & NFC (U219)

Snapshot 2026-09-04. Schematic **V0.3 / 2026-05-28**, 3 sheets. Nothing measured.

## 1. Cap-Bus (`P1`, `HDR_14P-P2.54`)

Numbering follows the **Cap page convention** (LEFT 1–7, RIGHT 14–8). See
[`../cap-lora-1262/pinouts-and-buses.md` §1](../cap-lora-1262/pinouts-and-buses.md) for why
two conventions exist for this connector.

| Cap pin | Cap net | Host GPIO (Cardputer-Adv) | Direction | Function |
|---:|---|---|---|---|
| 1 | `CC1101_G0` | **G15** | O → host | CC1101 `GDO0`, via `R4` 330 Ω — packet interrupt |
| 2 | `CC1101_RF_SW0` | **G13** (**G14** on CardputerZero) | I | Band select, bit 0 |
| 3 | `SCL` | **G9** | I/O | I²C — Grove pass-through only |
| 4 | `SDA` | **G8** | I/O | I²C — Grove pass-through only |
| 5 | `5V_OUT` | — | P | 5 V from host |
| 6 | `GND` | — | P | Ground |
| 7 | *(unassigned on the vendor pin map)* | — | — | The LoRa Cap uses this as `5V_IN` |
| **8** | **`POWER_EN`** | **G3** | I | **Enables the whole Cap's 3.3 V rail** |
| 9 | `NFC_IRQ` | **G4** | O → host | ST25R3916 `IRQ` (pin 27) |
| 10 | `NFC_CS` | **G6** | I | ST25R3916 `SS` (pin 29) |
| 11 | `SPI_SCLK` | **G40** | I | shared SPI clock |
| 12 | `SPI_MOSI` | **G14** | I | shared SPI MOSI |
| 13 | `SPI_MISO` | **G39** | O | shared SPI MISO |
| 14 | `CC1101_CS` | **G5** | I | CC1101 `CSN` (pin 7) |

Confirmed by the schematic `P1` symbol (which annotates host GPIO alongside each net), the
vendor pin-map graphic, and the Arduino guide's prose — three agreeing sources. **[SCH]**,
**[DOC]**

### 1.1 Compare with the Cap LoRa-1262 — the same connector, different meanings

| Pin | Cap LoRa-1262 | Cap CC1101 |
|---:|---|---|
| 1 | `GPS_TX` (G15) | `CC1101_G0` (G15) |
| 2 | `GPS_RX` (G13) | `CC1101_RF_SW0` (G13) |
| 7 | `5V_IN` | unassigned |
| **8** | **`LoRa_RST`** (G3) | **`POWER_EN`** (G3) |
| 9 | `LoRa_IRQ` (G4) | `NFC_IRQ` (G4) |
| 10 | `LoRa_BUSY` (G6) | `NFC_CS` (G6) |
| 11–14 | SPI + `LoRa_NSS` | SPI + `CC1101_CS` |

Only the SPI trio and the power/ground pins mean the same thing on both boards. **Firmware
must know which Cap is fitted before it drives anything**, and there is no identity
register on either board to ask (the LoRa Cap is inferred by probing I²C `0x43`; this Cap
has no I²C device at all, so it cannot be probed the same way).

### 1.2 The `GO`/`GI` extraction artifact appears here too

As on the LoRa Cap schematic, the two I²C GPIO labels extract as `GO` and `GI`; there is no
`G8`/`G9` token in the file. Correct values are `G8` = SDA, `G9` = SCL, established from the
vendor pin map. Recorded so nobody chases a nonexistent net.

## 2. Sheet map

| Sheet | Title block | Contains |
|---:|---|---|
| 1 | *Cardputer-Adv MAP* / `2x7PDCDC` | `P1` Cap-Bus, `U1` JW5712 buck, `J1` Grove, `POWER_EN` |
| 2 | *NFC* | `U2` ST25R3916, `Y1` 27.12 MHz, differential antenna matching, `ANT1`, 16 decoupling caps |
| 3 | *SUB_1GHz* | `U3` CC1101, `B1` balun, `U4`/`U5` SP3T switches, three band paths, `Y2` 26 MHz, `E1` SMA |

## 3. `U3` CC1101 — see the feature guide

Full pin table in [`features/sub-ghz.md` §2](features/sub-ghz.md).

## 4. `U2` ST25R3916 — pins in use

**[SCH]** sheet 2. The complete generic pin table is in the
[component record](../../../components/stmicroelectronics/st25r3916/README.md); this lists
only what this board wires.

| Pin | Name | Net |
|---:|---|---|
| 1 | `VDD_IO` | `VDD_3V3` |
| 2 | `CSO` | — |
| 3 | `VDD_D` | `VDD_3V3` |
| 4 | `XTO` | `Y1` 27.12 MHz |
| 5 | `XTI` | `Y1` 27.12 MHz |
| 6, 12, 16, 26 | `GND` | `GND` |
| 7 | `VDD_A` | `VDD_3V3` |
| 8 | `VDD` | `+5V` |
| 9 | `VDD_RF` | `VDD_3V3` |
| 10 | `VDD_TX` | `+5V` |
| 11 | `VDD_AM` | `VDD_3V3` |
| **13** | `RFO1` | → `L3`/`R3` arm → `ANT1_N` |
| 14 | `VDD_DR` | `VDD_3V3` |
| **15** | `RFO2` | → matching → `ANT1_P` |
| 17 | `EXT_LM` | wired — external load modulation for card emulation |
| **18** | `AAT_A` | automatic antenna tuning |
| **19** | `AAT_B` | automatic antenna tuning |
| **20** | `I2C_EN` | **strapped for SPI** (`inferred` — the strap resistor was not identified) |
| 21 | `VSS` | `GND` |
| **22** | `RFI1` | `RFI_P` ← `C8` 10 pF |
| **23** | `RFI2` | `RFI_N` ← `C17` 10 pF |
| 24 | `AGDC` | — |
| 25 | `CSI` | — |
| **27** | `IRQ` | `NFC_IRQ` → Cap-Bus 9 → host **G4** |
| 28 | `MCU_CLK` | — |
| **29** | `SS` | `NFC_CS` → Cap-Bus 10 → host **G6** |
| **30** | `SCLK` | `SPI_SCLK` → host **G40** |
| **31** | `MOSI` | `SPI_MOSI` → host **G14** |
| **32** | `MISO` | `SPI_MISO` → host **G39** |
| 33 | `EPAD` | `GND` |

> **`VDD` (8) and `VDD_TX` (10) come from `+5V`, not 3.3 V.** The ST25R3916 runs its
> transmit driver from the higher rail for field strength while the digital and analogue
> sections sit on 3.3 V. That is a design choice worth carrying over to any port — see
> [`features/nfc.md` §10](features/nfc.md).

## 5. Bus ownership

| Bus | Devices | Selects |
|---|---|---|
| **SPI** (G40/G14/G39) | CC1101 (`CS` = G5), ST25R3916 (`CS` = G6), **host microSD** (`CS` = G12) | three chip selects, **two different SPI modes** — the NFC part wants mode 1 |
| **I²C** (G8/G9) | **nothing on this Cap**; Grove pass-through only | — |
| UART | **unused by this Cap** | the host's G13/G15 are repurposed as `RF_SW0` / `GDO0` |

**Note what pin 2 costs you:** on the Cardputer-Adv, G13 is the EXT connector's UART pin.
This Cap spends it as a static band-select line, so **you cannot have this Cap and a
UART peripheral on the bus at the same time.**

## 6. Host resource cost

Nine host GPIO (G3, G4, G5, G6, G13, G14, G15, G39, G40) plus a share of SPI and the I²C
pass-through — the same order of cost as the LoRa Cap, which is why the original Cardputer
cannot take either.

---

# 2026-09-07 — Cap-Bus pinout confirmed from the schematic

Appended beneath the existing tables; **nothing above is altered.** Full trace with coordinates:
[`schematic-netlist.md`](schematic-netlist.md). Method:
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md).

## Connector `P1` = `HDR_14P-P2.54` — the same bus as the Cap LoRa-1262

| Pin | Symbol pin name | Host GPIO | Functional net on U219 | Token |
|---|---|---|---|---|
| 1 | `GPS-TX` | `G15` | `CC1101_G0` | `PIP101` @ 648.00, 506.37 |
| 2 | `GPS-RX` | `G13` | `CC1101_RF_SW0` | `PIP102` @ 648.00, 498.91 |
| 3 | `SCL` | `GI` = **GPIO1** | `SCL` | `PIP103` @ 647.00, 491.37 |
| 4 | `SDA` | `GO` = **GPIO2** | `SDA` | `PIP104` @ 648.00, 484.37 |
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

## Pin 8 — the reported conflict, resolved

The connector, the pin number, the symbol pin name (`RESET`) and the host GPIO (`G3`) are
**identical** to the Cap LoRa-1262's. Only the board function differs:

- **U214 Cap LoRa-1262:** `G3` → net `RST` → `M1` pin 2 `NRST` — the SX1262's reset.
- **U219 Cap CC1101:** `G3` → net `POWER_EN` (@ 535.08, 258.46 and 146.12, 258.46) → `R1`
  100 kΩ and `U1`'s `EN` ball. `U1` is this board's own step-down converter — the same
  `JW5712` ball map (`EN`/`SW`/`VIN`/`VOS`/`VSEL1..3`/`GND`), `IOUT: 0~0.6A` annotation,
  `L1` `MWTC201608S2R2` 2.2 µH.

**So `G3` gates the CC1101 board's own 3.3 V rail.** Driving it low removes power from the radio,
rather than resetting it. That is a materially different behaviour from the LoRa board and must
not be assumed portable between them.

⚠ The reported "conflict" was therefore never a disagreement about the bus pinout. It is a
per-board function assignment on a stable, shared bus line.

## ⚠ `NFC_IRQ` and `NFC_CS` are vestigial net names

Bus pins 9 and 10 carry the names `NFC_IRQ` (@ 531.24, 265.65 p1; 192.64, 265.65 p2) and
`NFC_CS` (@ 529.74, 272.84 p1; 191.14, 280.03 p2). **No NFC controller appears anywhere in this
document's designator census.** They read as names inherited from a sibling design. Recorded so
nobody goes looking for a part that is not fitted; the routing above is what matters.

## Off-sheet nets (sheet 1 ↔ sheet 3)

Connectivity between sheets is by net name only, and these occurrences are the only evidence of
it:

| Net | Sheet 1 | Sheet 3 |
|---|---|---|
| `CC1101_CS` | 534.06, 301.59 | 101.69, 107.27 |
| `CC1101_G0` | 706.90, 301.59 | 101.63, 121.64 |
| `CC1101_RF_SW0` | 715.06, 294.40 | 95.41, 380.66 · 563.75, 373.48 |
| `CC1101_RF_SW1` | — | 109.79, 128.83 · 95.41, 373.47 · 563.75, 380.66 |
| `CC1101_RF` | — | 750.13, 359.10 · 750.13, 481.54 |
| `I2C_EN` | — | p2: 259.66, 254.87 |

`CC1101_RF_SW0`/`SW1` appear at two x positions on sheet 3 in the same two rows, crossed — the
signature of an antenna-path RF switch driven by two complementary control lines.
