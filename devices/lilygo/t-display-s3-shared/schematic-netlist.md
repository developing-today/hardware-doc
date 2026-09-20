# T-Display-S3 family — net list traced from the schematic PDFs

**Traced:** 2026-09-07 · **Method:**
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md)
· **Tool:** poppler 26.06.0 `pdftotext -bbox-layout`, plus 300 dpi `pdftoppm` crops for the
ambiguous cases.

This file is **new** and adds to the record; it does not replace any existing pinout table. Where
it contradicts one, the contradiction is listed in
[`scratch/schematic-tracing/corrections-requiring-review.md`](../../../scratch/schematic-tracing/corrections-requiring-review.md).

Every row cites the **sheet, the designator/pin token and its page coordinate**, so any claim can
be re-checked with one command. Coordinates are PDF points, top-left origin, as poppler reports
them.

---

## 0. Source files and their traceability

| File | Pages | Producer | Rasters | Helper tokens |
|---|---|---|---|---|
| `artifacts/schematic/T_Display_S3.pdf` | 1 | Altium Designer / llPDFLib 3.x, CreationDate 2024‑04‑29 | **0** | `CO`, `PI` present; **no `NL`** |
| `artifacts/schematic/SCH_T-Display-S3-MIDI_V1.1.pdf` | 1 | — | 2 (a logo + its soft mask) | `CO`, `PI` |

`pdfimages -list` on `T_Display_S3.pdf` prints its two header lines and nothing else: the sheet
contains **no embedded raster at all**. It is pure vector, and fully traceable.

---

## 1. `U6` — the charger. **The schematic draws a 5-pin part.**

This settles a standing conflict. The schematic's part string is `TP4065`
(`T_Display_S3.pdf` p1, x=273.09 y=484.09) and the symbol carries **exactly five pin tokens**:

| Token | Coordinate | Pin | Function text | Coordinate of function text |
|---|---|---|---|---|
| `PIU601` | 241.50, 499.46 | 1 | `CHRG` | 254.13, 499.92 |
| `PIU602` | 264.50, 518.48 | 2 | `GND` | 264.99, 507.91 |
| `PIU603` | 283.50, 496.46 | 3 | `BAT` | 273.02, 496.32 |
| `PIU604` | 264.50, 483.48 | 4 | `VCC` | 264.99, 494.81 |
| `PIU605` | 283.50, 503.46 | 5 | `PROG` | 272.02, 503.27 |

`python3 trace.py grep bbox/tds3.xhtml '^PIU6'` returns those five and **no `PIU606`,
`PIU607` or `PIU608`**. A rendered 300 dpi crop of the region confirms a five-terminal symbol
visually.

The same check on two sibling sheets returns the same five pins and the same five function
names:

| Sheet | Designator | Pin tokens | `PROG` resistor |
|---|---|---|---|
| `T-DISPLAY-S3-AMOLED.pdf` p1 | `U5` | `PIU501`…`PIU505` | `R18` 2.32 kΩ |
| `T-Display-S3-AMOLED-Touch.pdf` p3 | `U6` | `PIU601`…`PIU605` | `R20` 2.2 kΩ |
| `T_Display_S3.pdf` p1 | `U6` | `PIU601`…`PIU605` | `R13` 2 kΩ |

Pin order 1 `CHRG` · 2 `GND` · 3 `BAT` · 4 `VCC` · 5 `PROG` is the LTC4054 / TP4054 / TP4056
SOT‑23‑5 arrangement.

**Charge-current annotation.** The sheet carries a rotated note reading **`IBAT (mA) = 580`**
beside `R13` = 2 kΩ, inside a dashed note box (tokens at x≈311.7, y 510.95–531.81). Poppler
merges it with the adjacent rotated designator `R13` into one apparent line — see the guide's
failure-modes section — but the rendered crop shows the two are separate text objects.

Implication: with the fitted `R13` = 2 kΩ the designed charge current is **580 mA**. That is
*not* consistent with a TP4057 (whose own datasheet, held at
`components/generic/tp4057/artifacts/`, specifies 500 mA typical at `RPROG` = 2 kΩ, and which is
a **SOT‑23‑6** part with a separate `STDBY` pin the symbol does not have). It is close to the
TP4056 family constant.

### Charger periphery

| From | Via | To | Evidence |
|---|---|---|---|
| `VBUS` | — | `U6.4 VCC` | `VBUS` text at 264.55, 449.09, column x≈264.5 down to `PIU604` |
| `U6.4 VCC` | `C21` 100 nF, `C22` 10 µF/16 V | `GND` | `PIC2101/02` at x 294/299.5 y 461.46; `PIC2201/02` y 471.91 |
| `VBUS` | `R9` 2 kΩ → `LED1` (Red) | `U6.1 CHRG` | `PIR901/02` at y 471.91; `PILED101/02` y 499.46; `PIU601` y 499.46 |
| `U6.3 BAT` | — | `VBAT` rail, decoupled by `C28` 100 nF and `C29` 10 µF/16 V | `VBAT` at 338, 470.4; `PIC2801/02` x 327.5 |
| `U6.5 PROG` | `R13` 2 kΩ | `GND` | `PIR1301` 302.5, 536.28 → `GND` 303.05, 561.06 |

## 2. `U2` — ESP32-S3R8 module, signal names as printed

Read directly from the module symbol on `T_Display_S3.pdf` p1 (symbol body x≈600–690).

| ESP32-S3 pin name | Net on this board |
|---|---|
| `GPIO0` | `GPIO0` (boot, to `S2` `SW-PB` and `R1` 10 kΩ pull-up to `VDD3V3`) |
| `GPIO1` | `GPIO1` |
| `GPIO2` | `GPIO2` |
| `GPIO3` | `GPIO3` |
| `GPIO4` | `BAT_ADC` |
| `GPIO5` | `ESP_LCD_RES` |
| `GPIO6` | `ESP_LCD_CS` |
| `GPIO7` | `ESP_LCD_D/C` |
| `GPIO8` | `ESP_LCD_WR` |
| `GPIO9` | `ESP_LCD_RD` |
| `GPIO10` | `II2C_SDA` |
| `GPIO11` | `II2C_SCL` |
| `GPIO12` | `ESP_TP_RESET` |
| `GPIO13` | `ESP_TP_INT` |
| `GPIO14` | `KEY` |
| `GPIO15` | `PWR_EN` — the sheet prints, at (622–748, 341.4), **"Battery power must set IO15 to HIGH"** |
| `GPIO38` | `ESP_LCD_BLK` (to `U4.EN`) |
| `GPIO39`…`GPIO48` | `ESP_LCD_D0`…`ESP_LCD_D7`, `ESP_USB_DM`, `ESP_USB_DP` (see §4) |
| `CHIP_PU` | `CHIP_PU` — `SW` `SW-PB`, `RW` 10 kΩ to `VDD3V3`, `CU` 1 µF/6.3 V |

## 3. Power tree

| Designator | Part (as printed) | Function | Key nets |
|---|---|---|---|
| `U7` | `AP2112K-3.3V(RT9013)` | 3.3 V LDO | `1 IN` ← `V3V`; `5 OUT` → `VDD3V3`; `3 EN`; `4 NC`; `2 GND`. In: `C23` 47 µF/10 V, `C24` 22 µF/10 V, `C25` 100 nF. Out: `C30`/`C31`/`C32`, `C26` 10 µF/16 V, `C27` 100 nF |
| `U6` | `TP4065` (5-pin, §1) | Li-ion charger | — |
| `U4` | `AW9364DNR` | backlight boost | `3 EN` ← `ESP_LCD_BLK`; `4 VIN`; `1 PGND`; `2 EP`; `9/8/7/5` → `LED1`…`LED4` → `LEDK1`…`LEDK4` |
| `Q1` | `PMBT3904` | NPN, power-latch | with `R5` 10 kΩ, `R6` 1 kΩ, `D1`/`D2` 1N4148 |
| `Q2`, `Q3` | `SI2301` | P-FET | `VBUS`/`V3V` path, `R7`/`R8` 100 kΩ |
| `Q4` | `SI2307` | P-FET | `+5V` path, `D3` 1N5819, `R12`/`R14` 100 kΩ |
| `U5` | `TYPE-C` receptacle | USB-C | `A4/A9 VBUS`, `A6 DP1+`, `A7 DN1-`, `A5 CC`, `A8 SUB1`, `A12/B1 GND`; `B6 DP+`, `B7 DN-`, `B8 SBU2`, `B5 VCONN`, `B4/B9 PWR` |
| `U1` | 40 MHz crystal | — | `XIN`/`XOUT`, `C2` 12 pF, `C4` 15 pF |
| `U3` | `W25Q128JV` | 16 MB SPI flash | `1 CS`→`SPICS0`, `2 DO`→`SPIQ`, `3 WP`→`SPIWP`, `4 GND`, `5 DI/IO0`→`SPID`, `6 CLK`→`SPICLK`, `7 HOLD`→`SPIHD`, `8 VCC`→`VDD_SDIO`; `C19` 100 nF |

`VBAT` is annotated **`(3.7V~~4.2V)`** at (468, 491.0). The 5 V input path carries the note
`5V/2A 保险丝` (“5 V / 2 A fuse”) at (359–365, 495.3) beside `R10`.

## 4. `CN1` — display FPC, `KH-FG0.5-H2.0-30PIN`

Pin count on the symbol is 31 (`PICN101`…`PICN1031`); the part string says 30 pin. Named pins:

| CN1 pin | Net |
|---|---|
| 4 | `ESP_LCD_RES` |
| 5 | `ESP_LCD_CS` |
| 6 | `ESP_LCD_D/C` |
| 7 | `ESP_LCD_WR` |
| 8 | `ESP_LCD_RD` |
| 11–18 | `ESP_LCD_D0` … `ESP_LCD_D7` |
| 21–24 | `LEDK1` … `LEDK4` |
| 26 | `ESP_TP_RESET` |
| 27 | `II2C_SCL` (pull-up `RIIC` 10 kΩ to `VDD3V3`) |
| 28 | `II2C_SDA` (pull-up `RIID` 10 kΩ) |
| 29 | `ESP_TP_INT` (pull-up `RINT` 100 kΩ) |

Decoupling on the FPC rail: `C17`, `C18` 100 nF, `C20` 1 µF/6.3 V; `V3V` feeds pin 20 area.

## 5. `P1` / `P2` — the two 12-way headers

Both symbols are `Header 12`. **Verified against a 300 dpi crop**, because the text-layer offsets
alone are ambiguous at ±1.7 pt: pin 12 of `P2` runs unbroken to a `VDD3V3` power port, which
fixes the binding as "label sits above its wire".

| `P2` pin | Net | | `P1` pin | Net |
|---|---|---|---|---|
| 12 | `VDD3V3` | | 12 | `GND` |
| 11 | `GPIO1` | | 11 | `U0TXD` |
| 10 | `GPIO2` | | 10 | `U0RXD` |
| 9 | `GPIO3` | | 9 | `II2C_SDA` |
| 8 | `GPIO10` | | 8 | `II2C_SCL` |
| 7 | `GPIO11` | | 7 | `ESP_TP_RESET` |
| 6 | `GPIO12` | | 6 | `ESP_TP_INT` |
| 5 | `GPIO13` | | 5 | **unlabelled stub** |
| 4 | **✗ no-connect** (X marker) | | 4 | **✗ no-connect** (X marker) |
| 3 | **✗ no-connect** (X marker) | | 3 | `GND` |
| 2 | `GND` | | 2 | `GND` |
| 1 | `+5V` | | 1 | `VDD3V3` |

⚠ **Recorded, not resolved.** `P1` pins 9/8/7/6 carry `II2C_SDA`/`II2C_SCL`/`ESP_TP_RESET`/
`ESP_TP_INT`, and §2 shows those are `GPIO10`/`GPIO11`/`GPIO12`/`GPIO13` — the *same four
signals* that `P2` pins 8/7/6/5 expose under their raw GPIO names. Two readings are possible:
the board genuinely brings the same four GPIOs to both headers, or `P1` and `P2` are two
renderings of one physical header. **The sheet does not distinguish them, and no attempt is made
to here.** A continuity check between `P1.9` and `P2.8` on a physical board settles it in
seconds.

## 6. `AXPM65611` — function established (AMOLED variants)

Not on the base board. On `T-Display-S3-AMOLED-Touch.pdf` p3 (`U5`) and
`T-Display-S3-AMOLED-Plus.pdf` p3 (`U4`) the symbol has **12 pins**, identical on both sheets:

| Pin | Name | Plus-sheet rail annotation |
|---|---|---|
| 1 | `SWP` | → `L6`/`L3` `DFP252012TF-100M` |
| 2 | `PGND` | |
| 3 | `VPOS` | **`+4.6V`** |
| 4 | `EN` | |
| 5 | `GND` | |
| 6 | `TEST` | |
| 7 | `CTRL` | net `SWIRE` |
| 8 | `AVDD` | |
| 9 | `VNEG` | **`-2.2V`**, also labelled `EAVDD` on the Touch sheet |
| 10 | `SWN` | → `L7`/`L4` `DFP252012TF-100M` |
| 11 | `VIN` | `+3.3V` |
| 12 | `VIN` | `+3.3V` |

Two switch nodes with two separate 10 µH inductors, one positive and one negative output at
ELVDD/ELVSS-typical voltages, plus a `SWIRE` control line: this is **an AMOLED bipolar display
bias supply**, confirmed rather than hypothesised. The manufacturer and orderable part number
remain unknown. See
[`components/unidentified/lilygo-t-display-s3-family/axpm65611`](../../../components/unidentified/lilygo-t-display-s3-family/axpm65611/README.md).

## 7. `SCH_T-Display-S3-MIDI_V1.1.pdf`

Traceable (711 words, `CO`/`PI` tokens present). The 2 objects reported by `pdfimages -list`
are one RGB image and its greyscale soft mask — a logo, not schematic content. No net-level
conflict with the base board was found; the MIDI variant's additions are not covered here.

## 8. What could **not** be traced

The **1.64″ AMOLED variant** (`devices/lilygo/t-display-s3-amoled-1-64/`) has **no schematic in
this repository at all** — the directory contains only `README.md`. This is therefore not a
tracing failure but a *missing artifact*: no poppler invocation can help. Its pin map remains
unestablished, and the only routes to it are LilyGO publishing the sheet, or a `pin_config.h`
appearing in a per-board repository. Recorded here so the gap is not mistaken for one this
session could have closed.

---

## Reproducing any row above

```bash
nix-shell -p poppler-utils --run \
  'pdftotext -bbox-layout devices/lilygo/t-display-s3-shared/artifacts/schematic/T_Display_S3.pdf /tmp/tds3.xhtml'
cd scratch/schematic-tracing
python3 trace.py   grep    /tmp/tds3.xhtml '^PIU6'          # pin tokens for U6
python3 trace.py   cluster /tmp/tds3.xhtml --x 262 --y 500 --r 75
python3 render.py  /tmp/tds3.xhtml --hide-pi --x0 200 --x1 420 --y0 440 --y1 560
```
