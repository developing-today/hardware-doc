# DinMeter — net list traced from `K134_DIN_Meter_v1.0-schematic.pdf`

**Traced:** 2026-09-07 · **Method:**
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md)
· **Tool:** poppler 26.06.0, plus 300 dpi `pdftoppm` crops.

**New file.** It does not replace `pinouts-and-buses.md`. Corrections to existing claims are
appended there and listed in
[`scratch/schematic-tracing/corrections-requiring-review.md`](../../../scratch/schematic-tracing/corrections-requiring-review.md).

Applies equally to **DinMeter v1.1**: `K134-V11_DIN_Meter_v1.0_2025_11_25_17_15_58-schematic.pdf`
extracts to the same 873 words and the same 26 `NL` tokens.

## 0. Traceability

1 page, `Creator: Altium Designer`, **0 embedded rasters**, 873 words, 26 `NL` tokens, full
`CO`/`PI` coverage. **Fully traceable.**

---

## 1. `J5` — the rotary encoder connector. **Five pins, not seven.**

`python3 trace.py grep <bbox> '^PIJ5'` returns exactly five tokens, and a 300 dpi render of the
symbol shows five pins:

| Pin | Symbol name | Token @ coordinate | Net | Termination |
|---|---|---|---|---|
| 1 | `b1` | `PIJ501` @ 445.50, 361.91 | **`BTN`** (@ 430, 359.2) | → `WAKE` → module pad 25 → **GPIO42** |
| 2 | `b2` | `PIJ502` @ 503.00, 361.91 | `GND` (@ 533, 362.5) | — |
| 3 | `A` | `PIJ503` @ 459.50, 389.77 | **`IN_A`** (@ 457, 419.9) | → module pad 23 → **GPIO41**; `R2` 10 kΩ to `+3.3V`, `C2` 100 nF to `GND` |
| 4 | `COM` | `PIJ504` @ 474.50, 389.77 | `GND` (@ 475, 416.7) | — |
| 5 | `B` | `PIJ505` @ 488.50, 389.77 | **`IN_B`** (@ 486, 419.9) | → module pad 21 → **GPIO40**; `R3` 10 kΩ to `+3.3V`, `C3` 100 nF to `GND` |

The value field reads `Rotary encode` (@ 462–482, 403.8). The push switch (`b1`/`b2`) is drawn
as a separate contact *inside the same symbol*, above the A/COM/B group — not as a second
connector.

**Topology now established:** a standard 3-terminal incremental quadrature encoder
(A / COM / B) with its common pin **grounded**, A and B pulled up by 10 kΩ and RC-filtered by
100 nF, plus an integrated 2-terminal momentary push switch wired between `BTN` and `GND`.

The `IN_A`/`IN_B` → GPIO mapping comes from the module footprint `M1`: the net labels sit at
x ≈ 388 on the right-hand pin column (x = 361 numbers, x ≈ 324 pin names): `IN_A` @ y 474.5 →
pad 23 → pin name `G41/MTDI`; `IN_B` @ y 488.6 → pad 21 → `G40/MTDO`.

> **Resource note, from those pin names:** the encoder occupies **`MTDI` (GPIO41)** and
> **`MTDO` (GPIO40)**. Those are two of the ESP32-S3's four JTAG pins. Using the encoder and an
> external JTAG probe simultaneously is impossible on this board.

## 2. `LS1` — the buzzer. **AC-coupled base drive, inductive load.**

| Element | Value | Tokens |
|---|---|---|
| `LS1` | value field `Buzzer`, 2 pads | `PILS101` @ 142.50, 448.37 · `PILS102` @ 142.50, 455.37 |
| `D6` | `1N4148WT`, **anti-parallel across `LS1`** | `PID602` @ 99.50, 426.57 · `PID601` @ 99.50, 448.57 |
| `Q5` | `SS8050` NPN (`Y1` beside it is the SOT-23 top mark, not a designator) | `PIQ503` collector @ 135.50, 476.77 · `PIQ501` base @ 121, 491.37 · `PIQ502` emitter @ 135.50, 505.77 → `GND` @ 553.60 |
| `R25` | 470 Ω | `PIR2501` @ 45, 491.37 · `PIR2502` @ 67, 491.37 |
| `C27` | **10 µF, in series** | `PIC2701` @ 74, 491.37 · `PIC2702` @ 89, 491.37 |
| `D7` | `1N4148WT`, base clamp | `PID702` cathode @ 99.50, 502.57 · `PID701` anode @ 99.50, 523.57 → `GND` |
| Supply | `+5VIN` | |

All five drive-path pin tokens share **y = 491.37** and run left to right in x: `R25.1`(45) →
`R25.2`(67) → `C27.1`(74) → `C27.2`(89) → `Q5.base`(121). The chain is therefore

```
beep ── R25 470Ω ── C27 10µF ──┬── Q5 base
                               └── D7 (cathode up) ── GND
```

**Findings this establishes:**

- `C27` is **in series with the base drive, not a decoupling capacitor.** The base is
  AC-coupled; `D7` clamps the negative excursion. The high-pass corner is
  1 / (2π · 470 Ω · 10 µF) ≈ **34 Hz**, so the whole audio band passes.
- The **flyback diode `D6` across `LS1` means the load is inductive** — an electromagnetic
  (magnetic) transducer, not a piezo. A piezo would need no catch diode.
- AC coupling plus a GPIO-driven tone confirms a **passive** transducer requiring a driven
  waveform, consistent with M5Unified modelling it as a PWM tone source.

Control net: `beep` (`NLbeep` @ 29.50, 488.20) → module pad 3 → pin name `G3` → **GPIO3**.

## 3. `U3` — the Grove 5 V boost. **The rail is designed to 5.38 V.**

`U3` is an **`SY7088`** (value @ 586, 215.2). Its printed formula, at (605, 236.7), is

```
Vout = 1.2V * (R1/R2 + 1)
```

The divider is `R16` **52.3 kΩ** (@ 663–668, 179.0) over `R18` **15 kΩ** (@ 663–666, 207.7),
with `FB` at `U3` pin (`LX`/`OUT`/`IN`/`EN`/`FB`/`PGND`/`GND` symbol, x ≈ 568–626).

```
Vout = 1.2 × (52.3 / 15 + 1) = 1.2 × 4.4867 = 5.384 V
```

**The arithmetic is correct and the sheet means it.** The rail labelled `+5VOUT` is a nominal
**5.38 V**, not 5.00 V. This is a design choice, not an extraction error: the same vendor uses
the same idiom on the Cardputer ADV, where `R4` 75 kΩ / `R6` 22 kΩ on an SY7088 gives
1.2 × (75/22 + 1) = **5.29 V**. Two boards, two deliberately-high 5 V rails.

Practical consequence: a Grove peripheral on this port sees **~5.4 V**, which is inside USB's
5.25 V upper limit by margin only if the peripheral tolerates it. Anything specified as
"5 V ± 5 %" (4.75–5.25 V) is **out of specification on this port.** Worth knowing before
blaming a peripheral.

## 4. Module footprint `M1` — complete pad map

Left column, pads 1–17 (pin tokens at x = 272.50, net labels ~2.8 pt above the wire at
x ≈ 233–257):

| Pad | Pin name | Net |
|---|---|---|
| 1 | `G1` | `GI` |
| 2 | `G2` | `GO` |
| 3 | `G3` | **`beep`** |
| 4 | `G4` | `LCD_RS` |
| 5 | `G5` | `LCD_MOSI` |
| 6 | `G6` | `LCD_SCK` |
| 7 | `G7` | `LCD_CS` |
| 8 | `G8` | `LCD_RESET` |
| 9 | `G9` | `LCD_BL` |
| 10 | `G10` | `BATADC` |
| 11 | `GND` | `GND` |
| 12 | `G11` | `IN_SDA` |
| 13 | `5V` | `+5VIN` |
| 14 | `G12` | `IN_SCL` |
| 15 | `G13` | `SDA` |
| 16 | `G14` | `G14` |
| 17 | `G15` | `SCL` |

Right column, pads 18–28 (pin numbers at x ≈ 361, pin names at x ≈ 324–342, net labels at
x ≈ 386–390):

| Pad | Pin name | Net |
|---|---|---|
| 18 | `GND` | `GND` |
| 19 | `G39/MTCK` | `G39` |
| 20 | `G0/Boot` | — |
| 21 | `G40/MTDO` | **`IN_B`** |
| 22 | `EN` | — |
| 23 | `G41/MTDI` | **`IN_A`** |
| 24 | `G44/Rx` | — |
| 25 | `G42/MTMS` | **`WAKE`** |
| 26 | `G43/Tx` | — |
| 27 | `G46` | `HOLD` |
| 28 | `3V3` | `3V3` |

Two distinct I²C buses are visible: **`IN_SDA`/`IN_SCL`** (pads 12/14 → `G11`/`G12`, the internal
bus, to `U5` `RTC8563`) and **`SDA`/`SCL`** (pads 15/17 → `G13`/`G15`, the external Grove bus to
`J4`).

## 5. Designator census with values, as printed

| Des | Value / part | Function |
|---|---|---|
| `U1` | `ME3116AM6G` | wide-input buck (`VIN`/`BST`/`EN`/`LX`/`FB`/`GND`), `L1` 10 µH `3015` |
| `U2` | `TP4057` | Li-ion charger — `BAT`, `CHRG`, `STDBY`, `PROG`, `VCC`, `GND` |
| `U3` | `SY7088` | Grove 5 V boost — §3 |
| `U4` | `BL8075CB5TR33` | 3.3 V regulator (`VIN`/`VOUT`/`EN`/`NC`/`GND`) |
| `U5` | `RTC8563` | RTC — `OSCI`, `OSCO`, `INT`, `VSS`, `VDD`, `CLKOUT`, `SCL`, `SDA` |
| `U6` | — | load switch (`EN`/`VIN`/`VOUT`, `A1`/`A2`) on the Grove rail |
| `U7` | `CN809J` | reset supervisor — `RESET`, `VCC`, `GND` |
| `Q1` | — | `VBAT_IN` path |
| `Q3`, `Q6` | `AP40P05` | P-FET, `VBAT_IN` → `VBAT_OUT` |
| `Q4` | `LN2324DT2AG` | `HOLD` latch |
| `Q5` | `SS8050` | buzzer driver — §2 |
| `D1`,`D9`,`D11` | `B5819W SL` | Schottky |
| `D2`,`D3`,`D4`,`D5`,`D10` | `B5819WT` | Schottky, wake/latch network |
| `D6`,`D7` | `1N4148WT` | §2 |
| `D8` | `SS34` | |
| `D12` | `SD36` | |
| `Y1` | (top mark of `Q5`) | — **not a crystal** |
| `Y2` | 32.768 kHz ±20 ppm 12.5 pF | RTC crystal, `C28`/`C29` 6.0 pF |
| `J1` | `Header 2`, `6V~36V` | DIN-rail supply input |
| `J3`,`J4` | `HY-2.0_IIC` | Grove ports |
| `J5` | `Rotary encode` | §1 |
| `FPC1` | `FPC-0.5-8P` | LCD — `LCD_CS`, `LCD_SCK`, `LCD_MOSI`, `LCD_RS`, `LCD_RESET`, `FPC_LCD_BL` |
| `LS1` | `Buzzer` | §2 |
| `S1`,`S4` | `SW-PB` | `BTN` |
| `M1` | Stamp module | §4 |

---

## Reproducing

```bash
nix-shell -p poppler-utils --run 'pdftotext -bbox-layout \
  "devices/m5stack/dinmeter/artifacts/schematic/K134_DIN_Meter_v1.0-schematic.pdf" /tmp/din.xhtml'
cd scratch/schematic-tracing
python3 netlist.py /tmp/din.xhtml --des J5
python3 trace.py   col /tmp/din.xhtml --x 143 --tol 8      # the LS1 / Q5 column
python3 render.py  /tmp/din.xhtml --x0 430 --x1 580 --y0 345 --y1 430
```
