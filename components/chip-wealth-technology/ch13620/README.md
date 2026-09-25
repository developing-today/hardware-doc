# Chip Wealth Technology CH13620

- **Category:** LTPS **AMOLED** mobile single-chip driver + controller, up to 368 RGB × 448 dot, with internal GRAM, on-chip DC/DC generation and gate driver control
- **Research status:** mined end-to-end from the specification now held at `artifacts/`. **The manufacturer is not named anywhere in the document's text** — it was recovered from the cover logo; see §1.1. **No board in this repository is known to use it** (§12).
- **Retrieved:** 2026-09-11 (acquired) · **identified, mined and filed:** 2026-09-20
- **Document:** CH13620 specification **V0.00, dated 2023-08-02**, 121 pages

A single-chip driver for small LTPS AMOLED panels — the class of part that sits behind a smartwatch
or fitness-band screen. It integrates the source driver (186 channels), the panel gate-driver control
(GOA + MUX outputs), the whole AMOLED power tree (four charge pumps plus six LDOs), digital gamma
correction and 1,978,368 bits of frame memory, and it talks to the host over **SPI / Dual-SPI /
Quad-SPI only**.

> ⚠ **This document arrived under a URL that named a different part.** It was fetched from
> Crystalfontz as `518.pdf` while probing `crystalfontz.com/controllers/UltraChip/UC8179/<id>/`.
> The `<Vendor>/<Part>` path segments on that host are decorative; only the numeric id selects a
> document. Full measurement in
> [`ai-crawler-site-access-table.md` § crystalfontz.com](../../../ai-crawler-site-access-table.md#crystalfontzcom--serves-controller-datasheets-and-the-url-lies)
> and §13 below.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Read directly out of `artifacts/ch13620-spec-v0.00-2023-08-02-crystalfontz-mirror.pdf`, cited by page |
| **[DOC-IMG]** | Read off a **rendered page image** or an **embedded raster** of that PDF, not the text layer |
| **[INF]** | Inference. Not stated by the vendor |
| **[NEG]** | Negative result — checked for and **not** found |

### Text-layer validation

**[DOC]** The extracted text was cross-checked against the document's own page furniture before any
value here was transcribed: every page footer carries `<n>  V0.00`, and the highest is `121`, which
matches `pdfinfo`'s `Pages: 121`. Headings in the extracted text match the 121-entry table of
contents on pp.2–3 line for line. The text layer is trustworthy. The **one** thing the text layer
does *not* contain is the manufacturer name — because it is a picture (§1.1).

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| **Manufacturer** | **芯颖科技有限公司 — CHIP WEALTH TECHNOLOGY LTD.** | **[DOC-IMG]** §1.1 |
| Part | `CH13620` | **[DOC]** p.1, running header on every page |
| Document version | **V0.00**, "Original", **2023-08-02** | **[DOC]** p.1, p.121 |
| Native resolution | **368 RGB × 448 dot** | **[DOC]** p.1, p.4, and `CASET`/`RASET` defaults (§5.1) |
| Panel technology | **LTPS AMOLED** | **[DOC]** p.4 |
| Source outputs | **186 channels**, `S1`–`S186` | **[DOC]** p.5, p.14 |
| Gate control outputs | `GOA1`–`GOA18`, `MUX1`–`MUX28` | **[DOC]** p.14 |
| GRAM | **1 978 368 bits** = 368 × 448 × 24 × ½ | **[DOC]** p.5 |
| Host interface | **SPI 8-bit / 9-bit / 16-bit and Quad-SPI**, strapped on `IM[1:0]`; **Dual-SPI** as a register-enabled overlay on 8/9-bit mode (§4.1) | **[DOC]** p.4, p.13, p.76, p.80 |
| Package | **COF / COG** | **[DOC]** p.6 |
| Die size | **12 000 µm × 850 µm** | **[DOC]** p.6 |
| Operating temperature | **−40 … +85 °C** | **[DOC]** p.113 |
| Stated applications | *"wearable device applications, including I-watch and smart band"* | **[DOC]** p.4 |
| PDF metadata | Title `SPEC`, author `chip`, `pdfx:Company = Microsoft`, created **2024-01-22** | **[DOC]** `pdfinfo -meta` |

### 1.1 ⚠ Identifying the manufacturer — the name is a raster, not text

**`CH13620` is not a searchable part number, and the document body never names its maker.** Searching
all 121 pages of extracted text for `Co., Ltd`, `Corporation`, `Copyright`, `Technology`,
`Semiconductor`, `reserved`, `www.`, `有限公司` or `科技` returns **nothing** except two unrelated
uses of the word "reserved" in register tables **[NEG]**. The PDF metadata is equally useless: title
`SPEC`, author `chip`, producer `Adobe PDF Library 9.0`, and `pdfx:Company: Microsoft` — the Word
default, not a vendor.

The `CH` prefix is an active trap: **WCH (Nanjing Qinheng)** owns it in this repository already
([CH340C](../../wch/ch340c/README.md), [CH445P](../../wch/ch445p/README.md),
[CH32V203C8T6](../../wch/ch32v203c8t6/README.md), [CH334R](../../wch/ch334r/README.md)). **WCH does
not make AMOLED drivers, and this is not a WCH part.** Guessing from the prefix would have filed it
under the wrong vendor.

**How it was actually resolved:** `pdfimages -list` showed a 707 × 150 raster on page 1 and a
596 × 85 raster repeated as the running header. Extracting them gives the company logo:

> **芯颖科技有限公司 · CHIP WEALTH TECHNOLOGY LTD.**

**[DOC-IMG]** The extracted cover raster is kept beside the PDF as
`artifacts/ch13620-cover-logo-chip-wealth-technology.png`
(SHA-256 `c19745389b29f63ed2552e3520d5c3c9a315359d3dae483c843c9636964d7760`, 117 088 bytes) so the
attribution can be re-checked in two seconds without opening a 121-page document. This also
retroactively explains the PDF author string `chip`.

Vendor slug used here: **`chip-wealth-technology`**.

**[NEG] No vendor documentation-sourcing guide exists for Chip Wealth Technology** — see §14. That
gap is recorded rather than filled with a stub, per the skill's instruction not to create a thin
guide.

---

## 2. Resolutions — the part is a family, and 368 × 448 is only its maximum

The description page lists eleven supported panel geometries **[DOC]** p.4:

> 368×448, 360×360, 320×360, 320×320, 320×290, 300×300, 272×340, 264×296, 240×240, 240×320, 180×360

The feature page restates them as **width × (100 + 2·NL)** — i.e. the *row* count is programmable in
steps of two via a gate-timing parameter `NL`, and only the **column** count (368 / 360 / 320 / 300 /
272 / 264 / 240 / 180 RGB) is quantised by the source-driver mapping **[DOC]** p.5.

| Statement | Where | What it means |
|---|---|---|
| 186 source channels | p.5, p.14 | 186 outputs × MUX 1:6 = **1116 subpixels = 372 RGB columns**, enough for 368 with margin **[INF]** |
| Source MUX **1:6** and **1:9** | p.5 | The same 186 pads serve narrower, taller panels at 1:9 |
| GRAM = 368 × 448 × 24 × **½** | p.5 | ⚠ §3.1 — the frame buffer is **half** a full 24-bit frame |
| `CASET` default `EC[8:0]` = **0x16F = 367** | p.37 | 368 columns, 0-indexed |
| `RASET` default `EP[9:0]` = **0x1BF = 447** | p.38 | 448 rows, 0-indexed |

The default window is therefore exactly the full 368 × 448 panel — confirming the headline number
from the register defaults, not just the marketing line. **[DOC]** pp.37–38.

---

## 3. Colour, memory and the GRAM arithmetic

### 3.1 ⚠ The frame memory is half a 24-bit frame

**[DOC]** p.5 gives the RAM size as `368 × 448 × 24 bits × 1/2` = **1 978 368 bits** = 247 296 bytes.

368 × 448 × 3 bytes would be 494 592 bytes. The GRAM holds **half** of that. **[INF]** The practical
reading is that a full-panel buffer exists only at ≤ 12 bits/pixel; at RGB888 the host can hold at
most half a frame on-chip and must stream. The document does not spell out the consequence, and
**this is not stated as a restriction anywhere** **[NEG]** — treat the inference as unconfirmed and
verify against real silicon before designing a full-frame RGB888 update path.

### 3.2 Pixel formats — `IPF` (`3Ah` / `3A00h`), default `0x07`

**[DOC]** p.48:

| `IFPF[2:0]` | Format | Bits/pixel |
|---|---|---|
| `001` | SPI 1-1-1 | 3 bpp (8 colours) |
| `010` | SPI 3-3-2 | 8 bpp (256 colours) |
| `011` | SPI 256-Gray | 8 bpp greyscale |
| `101` | RGB565 | 16 bpp (65 536) |
| `110` | RGB666 | 18 bpp (262 144) |
| **`111`** | **RGB888** | **24 bpp (16.7 M)** — **reset default** |
| others | reserved | |

Note the default is the *widest* format, so a host that forgets `IPF` will be feeding 24-bit pixels.
`000` and `100` are reserved **[DOC]** p.48.

Display-mode colour depths **[DOC]** p.5: full colour 16.7 M; reduced 262 K / 65 K / 4096; idle mode
16.7 M / 262 K / 65 K / 4096 / **8** colours.

### 3.3 Addressing and partial update

- `CASET` (`2A00h`–`2A03h`) sets `SC[8:0]` / `EC[8:0]`; `RASET` (`2B00h`–`2B03h`) sets `SP[9:0]` /
  `EP[9:0]` **[DOC]** pp.37–38.
- ⚠ **Both carry the same restriction:** *"When partial update, the `SC`/`SP` and
  `EC−SC+1` / `EP−SP+1` must be divisible by 2."* **[DOC]** pp.37–38. **Windows must start on an even
  coordinate and have an even extent.** This is the same class of constraint as the ST77916's
  2-pixel-grid rounder; if you write your own flush path and ignore it you get shifted or skewed
  output.
- `RAMW` (`2Ch`) starts a write, `RAMWC` (`3Ch`) continues one; `RAMR` (`2Eh`) / `RAMRDC` (`3Eh`)
  read **[DOC]** pp.39–40, 50–51.
- Horizontal and vertical partial-display areas have their own commands, `HPTLAR` (`3000h`–`3003h`)
  and `VPTLAR` (`3100h`–`3101h`) **[DOC]** pp.41–42, with `PTLON` (`12h`) / `NORON` (`13h`) to
  enter and leave partial mode **[DOC]** pp.29–30.

---

## 4. Host interface — SPI only, and the MIPI question

### 4.1 `IM[1:0]` selects the mode, on hardware pads

**[DOC]** p.13, p.76:

| `IM[1:0]` | Display data | Command |
|---|---|---|
| `00` | 9-bit SPI (3-wire) | 9-bit SPI |
| `01` | 8-bit SPI (4-wire, uses `DCX`) | 8-bit SPI |
| **`10`** | **Quad-SPI** | **Quad-SPI** |
| `11` | — | 16-bit rising-edge SPI |

`IM[1:0]` must be tied to `VDDIO` or `VSSIO` **[DOC]** p.13. There is no software override.

⚠ **Dual-SPI is not in that table.** The feature list advertises "dual serial peripheral interface
(Dual-SPI)" **[DOC]** pp.4–5, but `IM[1:0]` has no Dual-SPI setting. p.80 resolves it: **Dual-SPI is
an overlay on 8-bit or 9-bit SPI mode**, enabled by a register bit `DSPI_EN = 1` (together with
`SPI_WRAM = 1`) and configured by `DSPI_CFG[1:0]`:

| `DSPI_CFG[1:0]` | Mode | `IM[1:0]` | Pixel formats |
|---|---|---|---|
| `00` | 1P1T 1-wire | 9-bit or 8-bit SPI | RGB888 / RGB666 / RGB565 |
| `01` | 1P1T 2-wire | 9-bit or 8-bit SPI | RGB888 / RGB666 / RGB565 |
| `10` | 2P3T 2-wire | 9-bit or 8-bit SPI | RGB888 / RGB666 **only** |

With `SPI_WRAM = 0` and `DSPI_EN = 0`, RAM writes are **not supported at all** **[DOC]** p.80.

⚠ **`DSPI_EN` and `DSPI_CFG[1:0]` have no entry in the published command set** **[NEG]** — like
`SWIRE_ONF[5:0]` (§5.5) and the `TE1` output selector (§8.3), they live in the manufacturer command
set this document does not publish. **Dual-SPI is therefore documented but not usable from this
document.** §11.

Pins: `CSB`, `SCL`, `SDI` (I/O), `SDO` (O), `DCX`, `D0`, `D1` **[DOC]** pp.12–13. In Quad-SPI the four
data lanes are **`SDI` / `DCX` / `D0` / `D1`** **[DOC]** p.83 — i.e. the D/C pin is repurposed as a
data lane, exactly as on other QSPI display controllers. Unused inputs have stated safe states
(`CSB`→`VDDIO`; `SCL`, `DCX`, `D0`, `D1`→`VSSIO`; `SDI`/`SDO` open) **[DOC]** pp.12–13.

### 4.2 Quad-SPI framing — the familiar `02h` / `32h` convention, plus a `12h`

**[DOC]** pp.83–84. Every QSPI transaction is `<instruction byte> <24-bit command address> <payload>`:

| Instruction | Command lanes | Data lanes | Use |
|---|---|---|---|
| **`0x02`** | 1-wire | 1-wire | Write command + parameters, or write RAM 1-wire |
| **`0x32`** | 1-wire | **4-wire** | Write RAM, pixel data on all four lanes |
| **`0x12`** | **4-wire** | 4-wire | Write RAM with the command address also sent 4-wire |
| **`0x03`** | 1-wire | 1-wire | Read command / read RAM |

The 24-bit command address is the register address from the **"Others"** column of every command
table — e.g. `RAMW` is sent as `0x02` `0x002C00`, and `CASET`'s four parameter bytes live at
`0x002A00`–`0x002A03` **[DOC]** p.83.

⚠ **Read has a dummy:** *"The 1st read parameter is dummy packet in read ram."* **[DOC]** p.84.

⚠ **RAM writes over SPI must be explicitly enabled.** `SPI_WRAM = 1` is required in addition to
`IM[1:0] = 10`; with `SPI_WRAM = 0` the part does **not support write RAM** at all **[DOC]** p.84.
All six pixel formats are available over Quad-SPI **[DOC]** p.84.

⚠ **Register reads must be enabled too, and it is a four-step dance** **[DOC]** p.72 (`SPIRDC`,
`6D00h`) and p.66 (`SPIRDC`, `6500h`):

```
1. write 6Dh, SPI_READ_EN = 1        ; enable 8/9-bit/Quad SPI read
2. write 65h, SPI_CNT[7:0] = n       ; how many parameters will be read
3. issue the read command, read n bytes
4. write 6Dh, SPI_READ_EN = 0        ; disable read, re-enable write
```

*"Note: 6Dh only support SPI write."* **[DOC]** p.72. Both commands are confusingly given the same
mnemonic `SPIRDC` in the table of contents; they are distinct registers.

### 4.3 Bus speed

**[DOC]** pp.116–117:

| | 8/9-bit SPI | Quad-SPI |
|---|---|---|
| Write clock cycle `t_SCYCW` min | **20 ns → 50 MHz** | **20 ns → 50 MHz** |
| **Register-read** clock cycle `t_SCYCR` min | **300 ns → 3.33 MHz** | **100 ns → 10 MHz** |
| Access time `t_ACC` max | 120 ns | 40 ns |
| `CSB` high pulse `t_CHW` min | 45 ns | 45 ns |

**Writes run 15× (single) or 5× (quad) faster than reads.** As on the ST77916, a host that leaves the
bus at write speed and tries to read will get nothing — and it will look like a driver bug. **Drop
the clock before reading.** **[INF]**

### 4.4 ⚠ Unresolved: the document contains MIPI DSI remnants, but the part has no DSI pins

Four places in the specification refer to MIPI/DSI:

| Where | Text |
|---|---|
| p.11 | `VDDIO` — *"Power supply for interface system **except MIPI interface**"* |
| p.113, abs-max | Differential input voltage rows for **`CLKP/N`, `D0P/N`, `D1P/N`**, −0.3 … +1.45 V |
| p.114, DC | *"Logic High/Low level leakage **(MIPI)**"*, `Vin = 0 to 1.2 V` |
| p.54 | `DSTBON` note 4 — *"the lane status of **DSI** must keep to **LP-00**"* |
| p.120 | Current-consumption note — *"For sleep in mode, **MIPI in stop state (LP11)**"* |

But the **pin description (pp.11–14) lists no differential pads**, the `IM[1:0]` table offers **no
MIPI mode**, and §6 "Interface" opens with *"The CH13620 supports serial peripheral interfaces
(SPI)"* **[DOC]** p.76.

**Recorded as a conflict, not resolved.** Two readings, both plausible **[INF]**:

1. **Family document.** CH13620 shares a specification template (and possibly a die floorplan) with a
   MIPI-DSI sibling; the DSI pads exist on silicon but are not bonded out in this configuration, and
   the electrical tables were not pruned.
2. **Editorial residue.** The document was derived by editing another part's specification — the
   classic case the research method warns about — and the MIPI rows are simply stale.

Reading 1 is mildly favoured because the absolute-maximum table names *specific* pad groups
(`CLKP/N`, `D0P/N`, `D1P/N` = a clock lane and two data lanes, i.e. a 2-lane DSI) with a
DSI-appropriate 1.45 V limit, which is more effort than a careless copy-paste usually involves.
**Neither reading is established.** What *is* established: **you cannot drive this part over MIPI
DSI using this document**, because no DSI pins are described and no DSI mode is selectable.

Separately — and this is **not** evidence of DSI — every command table has an **"Address: MIPI /
Others"** column pair. That is an addressing convention, not an interface claim: the "MIPI" column
gives the one-byte DCS command (`2Ah`) and the "Others" column gives the 16-bit register address used
by the SPI/QSPI 24-bit command-address framing (`2A00h`…`2A03h`). Do not read that column as proof
the part speaks DSI. **[DOC]** pp.37–38, 83 **[INF]**

---

## 5. The AMOLED power tree — this is most of the chip

An AMOLED driver has to manufacture many more rails than an LCD controller, and CH13620 does nearly
all of it on-die.

### 5.1 Input rails

| Rail | Role | Range | Typ. |
|---|---|---|---|
| `VDDIO` | Interface I/O supply | **1.65 – 3.6 V** | 1.8 V |
| `VDDR` | Regulator/logic supply | **1.65 – 3.6 V** | 1.8 V |
| `VDDA` | Analog supply | **2.7 – 3.6 V** | 2.8 V |
| `VDDB` | **DC/DC converter supply** | **2.7 – 3.6 V** | 2.8 V |

**[DOC]** p.5, p.11, p.114. Grounds are separated by function — `VSSIO`, `VSSR`, `VSSB`, `VSSG`,
`AVSS`, `DVSS` — all tied to GND **[DOC]** p.11. `DVDD` is an *output*: an on-chip regulator for the
logic core, gated by the `DVDD_EN` pin (internally pulled high) **[DOC]** pp.11, 13.

### 5.2 Four charge pumps

**[DOC]** pp.8, 11, 114:

| Output | Generated from | Range | Typ. | Flying caps |
|---|---|---|---|---|
| `AVDD` | `VDDB` | **4.5 – 6.5 V** (2× or 3× `VDDB`) | 5.6 V | `C11P/N`, `C12P/N` |
| `AVEE` | `VDDB` | **−5.5 V … −1×`VDDB`** | −5.5 V | `C21P/N`, `C22P/N` |
| `VGH` | step-up 3 | `AVDD` … `2×AVDD` | 8.4 V | `C31P/N` |
| `VGL` | step-up 4 | `AVEE−AVDD` … `AVEE` | −11.1 V | `C41P/N` |

Constraint: **`VGH − VGL ≤ 30 V`** **[DOC]** p.115. Absolute maximum for `VGH−VGL` (and
`VGHO−VGLO`) is **32 V** **[DOC]** p.113.

### 5.3 Six LDOs off those pumps

**[DOC]** pp.5, 11, 114:

| Output | From | Range | Step | Purpose |
|---|---|---|---|---|
| `VGM` | `AVDD` | 2.0 – 6.3 V (max `AVDD−0.2`) | 10 mV | Gamma **highest** reference |
| `VGS` | `AVDD` | 0, or 0.2 – 4.5 V | 10 mV | Gamma **lowest** reference |
| `VREFP` | — | 0.5 – 5.0 V (max `AVDD−0.2`) | 100 mV | **Pixel reset** voltage, positive |
| `VREFN` | — | −5.0 – −0.2 V (max `AVEE+0.2`) | 100 mV | **Pixel reset** voltage, negative |
| `VEP` | `AVDD` | 2.0 – 5.0 V (DC table: 0.5 – 5.0) | 100 mV | Panel **ELVDD** |
| `VEN` | `AVEE` | 0, or −0.2 … −5.0 V | 100 mV | Panel **ELVSS** |

`VGHO` (3.0 – 10 V) and `VGLO` (−10 – −3.0 V), 0.5 V steps, are the gate-control swing rails for the
panel's GOA circuitry **[DOC]** pp.5, 14.

⚠ **ELVDD/ELVSS drive current is small:** `I_VEP ≤ 4.5 mA` (at `AVDD = 2×VDDB`) or **3.7 mA** (at
`3×VDDB`); `I_VEN ≤ 4 mA` or **3.5 mA**, all for a 50 mV droop **[DOC]** p.114. **This is enough for
a small band/watch panel and nothing larger.** Bigger panels use an external PMIC — which is what
`OLED_EN` and `SWIRE` are for (§5.5).

### 5.4 External components

Every rail needs its own capacitor **[DOC]** p.9:

- **2.2 µF** on `VDDIO`/`VDDR`, `VDDA`/`VDDB`, `DVDD`, `AVEE`, `VGL`, `VREFP`, `VREFN`, `VEP`, `VEN`, `VREF`
- **4.7 µF** on `AVDD`
- **1.0 µF** on every flying-cap pair and on `VGH`, `VGHO`, `VGLO`
- **`VGM` and `VGS` need no capacitor**
- ⚠ **`VGL` additionally needs a Schottky diode to GND** — recommended part **RB521CS-30**
  (V<sub>F</sub> = 0.35 V @ 10 mA, V<sub>R</sub> = 30 V) **[DOC]** p.9, note 1
- Leave `VREFP` / `VEP` / `VEN` **open** if unused **[DOC]** p.9, note 2

Voltage ratings matter: 6 V caps on the input rails and `DVDD`/`VREF`, 10 V on `AVDD`/`AVEE`/
`VREFP`/`VREFN`/`VEP`/`VEN` and the `C11`–`C22` flying caps, **16 V** on `VGH`/`VGL`/`VGHO`/`VGLO`
and the `C31`/`C41` flying caps **[DOC]** p.9.

**Maximum ITO series resistance** is tabulated per pad for chip-on-glass use **[DOC]** p.10 — 5 Ω on
`VDDR`, `VDDB`, `VSSR`, `VSSB`, `DVSS`, `DVDD`, `AVDD`/`AVEE` and the `C1x`/`C2x` caps; 10 Ω on
`AVSS`, `C31`/`C41`, `VGH`/`VGL`/`VGHO`/`VGLO`; 15 Ω on `VDDA`, `VSSG`, `VREF` and the gamma/ELVDD
LDO outputs; 20 Ω on `VDDIO`/`VSSIO`; **30 Ω on every logic pin** including `RSTB`, `CSB`, `SCL`,
`DCX`, `D[1:0]`, `SDI`, `SDO`, `IM[1:0]`, `DVDD_EN`, `OLED_EN`, `SWIRE`.

### 5.5 External power IC control — `OLED_EN` and `SWIRE`

`OLED_EN` is a power-IC enable output; `SWIRE` is the **single-wire protocol** pin used to program an
external ELVDD/ELVSS power IC **[DOC]** p.14. `SWIREMANU` (`6C00h`) forces it manually:
`0xA5` = ELVDD/ELVSS **on**, `0x5A` (and any other value) = **off**, default `0x5A` **[DOC]** p.71.
There is a dedicated S-Wire timing-control section at p.108 **[DOC]**.

The power-on timing diagram shows `SWIRE` activity gating the `ELVDD`/`ELVSS` ramp with a delay `t1`
*"controlled by `SWIRE_ONF[5:0]`"* **[DOC]** p.97, note 1. ⚠ **`SWIRE_ONF[5:0]` is named in that note
but has no register entry in the user command set** **[NEG]** — it is presumably in the manufacturer
command set, which this document does not publish. §11.

---

## 6. Power-on and power-off sequences

### 6.1 Power on **[DOC]** pp.96–97

```
VDDIO/VDDR  ──┐
              ├─ ≥ 0 ms ──► VDDA/VDDB
                            └─ ≥ 5 ms ──► VPWR_IC (external ELVDD/ELVSS power IC)
                                          └─ ≥ 1 ms ──► RSTB released   (RSTB low ≥ 10 ms; ≥ 5 ms after VDDA/VDDB)
                                                        └─ ≥ 10 ms ──► Initial Code
                                                                       └─ SLPOUT ──► > 60 ms ──► Display On ──► video data
```

Stated tolerances: *"There is **not** a limit for rise/fall time on VDDA/VDDB/VDDIO/VDDR"*, and
*"there will be **no damage** to the display module if the power sequences are not met"* — but
correct function is only guaranteed if they are **[DOC]** p.96. Reset cancel time is **5 ms**
**[DOC]** p.96, note 6.

⚠ *"If `RSTB` is not held stable by the host during the power-on sequence … it will be necessary to
apply a hardware reset after the host power-on sequence is complete to ensure correct operation.
Otherwise function is not guaranteed."* **[DOC]** p.96, note 4.

### 6.2 Power off **[DOC]** pp.96, 98

- If the panel is in **Sleep Out**: `VDDA`/`VDDB`/`VDDIO`/`VDDR` must stay up for a **minimum of
  5 frames** after `RSTB` is released — annotated **"> 83 ms @ 60 Hz"**.
- If the panel is in **Sleep In**: they may drop **immediately** (0 ms).
- Sequence: `DISPOFF` + `SLPIN` → wait 5 frames → drop `VPWR_IC` → drop `VDDA`/`VDDB` → drop
  `VDDIO`/`VDDR`.

### 6.3 Uncontrolled power off

*"e.g. there is removed a battery without the controlled power off sequence. There will not be any
damages … the display will go blank and there will not be any visible effects **within 1 second**"*
**[DOC]** p.99. Unlike the ST7567A (whose glass can be permanently polarised by a bad power-down),
CH13620 declares an uncontrolled cut safe.

---

## 7. Power level modes

**[DOC]** pp.100–102, in descending consumption:

| Mode | DC/DC | Oscillator | Panel driver | Host interface | Registers | Exit |
|---|---|---|---|---|---|---|
| Normal On, Sleep Out | on | on | on | working | kept | — |
| Normal On + **Idle Mode** On | on | on | on | working | kept | `IDMOFF` (`38h`) |
| **Sleep In** (`SLPIN` `10h`) | **stopped** | **stopped** | **stopped** | working (on `VDDIO`) | **kept** | `SLPOUT` (`11h`) |
| **Deep Standby** (`DSTBON` `4F00h`) | stopped | stopped | stopped | **not working** | **lost** | **`RSTB` low pulse only** |
| Power Off | — | — | — | — | default | power-on sequence |

### 7.1 Deep Standby — enter and exit correctly or not at all

**[DOC]** p.54, p.104:

```
DISPOFF (28h)
SLPIN   (10h)
  ... wait ≥ 2 frames ...
DSTBON  (4F00h), DSTB = 1
  ... to exit: RSTB low pulse > 3 ms  (p.104)  /  > 1 ms  (p.54)
  ... wait ≥ 50 ms ...
full re-initialisation + data, then display on
```

Four traps, all stated **[DOC]** p.54:

1. **You cannot write `4F00h` while in Sleep-Out or Display-On.** Enter Sleep In and Display Off first.
2. **Clearing `DSTB` from 1 to 0 does not exit the mode.** Only an `RSTB` pulse does.
3. **All registers are lost.** Deep Standby requires a complete re-initialisation, not a resume.
4. ⚠ **The minimum `RSTB` pulse is given as `> 1 msec` on p.54 and `> 3 msec` on p.104.** The two
   pages disagree. **Use 3 ms.** Conflict recorded, not resolved.

### 7.2 Sleep in / out timing

`SLPIN` and `SLPOUT` each require **≥ 120 ms** before the next instruction **[DOC]** p.103 — the same
figure the whole DCS-descended display world uses, and the same one that is load-bearing on
[ST77916](../../sitronix/st77916/README.md#53--init-table-gotchas).

### 7.3 Current consumption is **not specified**

**[NEG]** **[DOC]** p.120: sleep-out/display-on, sleep-in and deep-standby currents are all **`TBD`**.
So are source and GOA rise/fall times (`TSr/TSf`, `TGr/TGf`, p.115) and several `Iload` conditions in
the DC notes. **This is a V0.00 document and it is visibly incomplete.** Do not quote a power figure
for this part from this document, because there is not one.

---

## 8. Display features and the algorithm blocks

Command set **[DOC]** pp.15–75. The base is standard MIPI-DCS-descended (`SWRESET` `01h`, `SLPIN/OUT`
`10h`/`11h`, `INVOFF/ON` `20h`/`21h`, `DISPOFF/ON` `28h`/`29h`, `CASET`/`RASET` `2Ah`/`2Bh`,
`RAMW`/`RAMR` `2Ch`/`2Eh`, `TEOFF`/`TEON` `34h`/`35h`, `IPF` `3Ah`, `RDID1-3` `DAh`–`DCh`). What is
*not* standard is more interesting.

### 8.1 Brightness and emission

| Command | Address | Function | Default |
|---|---|---|---|
| `WDB` / `RDB` | `5100h` / `5200h` | Display brightness `DBV[7:0]`, `00h` dimmest … `FFh` brightest | **`FFh`** |
| `HBMSEL` / `RHBM` | `5300h` / `5400h` | **High Brightness Mode**: `A5h` enable, `5Ah` disable | `5Ah` |
| `NEM` | `5500h` | Emission width, **normal** mode | — |
| `IEM` | `5600h` | Emission width, **idle** mode | — |
| `HEM` | `5700h` | Emission width, **HBM** mode | — |
| `BACTR` | `6000h` | Brightness adjustment control | — |
| `DECTR` | `6200h` | **Dynamic ELVSS** control | — |
| `SRECTR` | `6300h` | **Sunlight-readability enhancement** | — |
| `GACMSET` | `6400h` | Gamma set and colour-mode set | — |

**[DOC]** pp.55–65. Note the magic-value convention (`A5h` = enable, `5Ah` = disable) used throughout
— a deliberate hamming-distance choice so a single-bit bus error cannot toggle a brightness mode.
**[INF]**

**Emission width** is the AMOLED equivalent of a duty cycle: the fraction of each frame the pixels
emit. Having three separate registers (normal / idle / HBM) means the panel's PWM dimming depth is
per-mode.

**Dynamic ELVSS** (`6200h`) modulates the negative panel rail with content — the standard technique
for cutting AMOLED power on dark frames.

### 8.2 The four geometry-optimisation algorithms — an unusual feature set

**[DOC]** pp.67–70:

| Command | Address | What it is for |
|---|---|---|
| `CICEN` | `6700h` | **Circular edge optimisation** |
| `OLOAEN` | `6800h` | **Oblique line optimisation** |
| `NOTCHEN` | `6900h` | **Notch algorithm** |
| `INCIREN` | `6A00h` | **Inside-circular algorithm** |

These exist because the target panels are **not rectangular**. A round watch face, a rounded-corner
band, or a panel with a sensor notch has a boundary that does not follow the pixel grid, and the
driver corrects the resulting staircase artefacts in hardware. Together with `AOD` support (p.6),
this is an unambiguous smartwatch/fitness-band part. **[INF]** on the reasoning, **[DOC]** on the
features.

### 8.3 Tearing effect

- `TEON` (`35h`) / `TEOFF` (`34h`); `STESL` (`4400h`–`4401h`) sets the scan line `N[15:0]` at which
  `TE` asserts **[DOC]** pp.43–44, 52.
- `STESL` with `N = 0000h` **is equivalent to `TEON` with `M = 0`** **[DOC]** p.52.
- *"The Tearing Effect Output line consists of V-Blanking information only."* **[DOC]** p.52.
- **`TE` is active low in sleep-in mode** **[DOC]** p.52.
- Changes take effect **on the following frame** **[DOC]** p.52.
- `GSL` (`4500h`–`4501h`) reads back the current scan line; **undefined in sleep-in** **[DOC]** p.53.
- **There are two TE pins.** `TE` is the frame-sync output; **`TE1` is a per-scan-line output
  intended for touch-panel noise sensing**, at `VDDIO` level, and can be repurposed to emit other
  control signals by register **[DOC]** p.13. The register that selects what `TE1` emits is **not in
  the published command set** **[NEG]**.
- The datasheet devotes pp.109–112 to the classic "MPU write faster / slower than panel read"
  tearing analysis **[DOC]**.
- ⚠ *"To avoid tearing effect, it is recommended to synchronize the `TE` signal when writing RAM."*
  **[DOC]** p.84.

### 8.4 Gamma

Digital, per-channel: *"built-in digital R/G/B separate gamma correct circuit"* **[DOC]** p.5. The
grey-scale amplifier resolves **1024 voltage levels between `VGM` and `VGS`**, shaped by
**28 key points**, with reference / amplitude / micro-adjustment registers **[DOC]** p.106.
Gamma and timing parameters can be stored in **OTP** **[DOC]** p.6, with an MTP write sequence at
p.107 **[DOC]**.

### 8.5 Status read-back

`RDDID` (`0400h`–`0402h`) returns manufacturer ID / module-driver version / module-driver ID, with
**reset defaults `00h`, `80h`, `00h`** **[DOC]** p.20 — and `RDID1`/`RDID2`/`RDID3` (`DAh`/`DBh`/
`DCh`) return the same three bytes individually **[DOC]** pp.20, 73–75. `RDDPM` (`0A00h`) exposes
booster / idle / partial / sleep / normal / display-on status in one byte, default `08h` **[DOC]**
p.21. `RDDSDR` (`0F00h`) is a self-diagnostic result **[DOC]** p.26.

⚠ Remember §4.2: **reads must be unlocked via `6Dh`/`65h` and the clock must be slowed** (§4.3).
A driver that issues `RDDID` at 50 MHz without unlocking will read nothing, and the failure looks
like a dead panel.

---

## 9. Electrical summary

**[DOC]** pp.113–115.

| Parameter | Value |
|---|---|
| `VDDA`, `VDDB`, `VDDIO`, `VDDR` abs max | −0.3 … **+5.5 V** |
| `AVDD − VSS` abs max | −0.3 … +6.6 V |
| `AVEE − VSS` abs max | +0.3 … −5.5 V |
| `VGH − VSS` / `VGL − VSS` abs max | ±15 V |
| `VGH − VGL` (`VGHO − VGLO`) abs max | −0.3 … **+32 V** |
| Logic I/O abs max | −0.3 … `VDDIO`+0.3 V |
| `V_IH` / `V_IL` | 0.7 `VDDIO` / 0.3 `VDDIO` |
| `V_OH` / `V_OL` | 0.8 `VDDIO` @ −1 mA / 0.2 `VDDIO` @ +1 mA |
| Logic leakage | ±1 µA |
| **Oscillator tolerance** | **±8 %** over −40 … +85 °C |
| Source output offset `V_OFFSET` | ≤ **15 mV** |
| Source output deviation `V_dev` | **5 mV** typ. (2.0 V < S_out < 5.0 V) |
| ESD | HBM **> 2500 V**, MM **> 250 V** |
| Latch-up | no latch-up below **±200 mA** |
| Operating / storage temp | −40 … +85 °C / −55 … +125 °C |

The ±8 % oscillator tolerance is worth noting: **the frame rate is not precise**, so anything timing
off the panel must use `TE`, not a host timer. **[INF]**

---

## 10. How it compares to the other display controllers here

| | **CH13620** | [ST77916](../../sitronix/st77916/README.md) | [ST7567A](../../sitronix/st7567a/README.md) |
|---|---|---|---|
| Technology | **LTPS AMOLED** | TFT LCD | monochrome STN LCD |
| Max resolution | 368 × 448 | 360 × 360 | 132 × 65 |
| Colour | up to **RGB888** | RGB565 / RGB666 (**no** 888) | 1 bpp |
| Interface | SPI / Dual / **Quad-SPI** | SPI / **QSPI** / RGB / DBI | 8080 / 6800 / SPI-4 / SPI-3 / **I²C** |
| QSPI framing | `02h` / `32h` / `12h` / `03h` | `02h` / `32h` / `03h` | — |
| GRAM | ✅ 1.98 Mbit (**half-frame**, §3.1) | ✅ | ✅ 8 580 bits |
| Backlight | **none — emissive** | external PWM | external |
| Brightness control | **on-chip**, `51h`/`53h` + emission width | host-side backlight | contrast via `RR`×`EV` |
| Panel power | **generated on-chip** (4 pumps, 6 LDOs) | panel-internal | booster + regulator + follower |
| Non-rectangular panel help | **4 algorithm blocks** | ❌ | ❌ |

The middle column is the part [that record's §2](../../sitronix/st77916/README.md#2--the-st77916--sh8601-conflict--analysed-and-resolved) is about: a
**backlight** proves a panel is not AMOLED. CH13620 is the shape of driver an actual AMOLED panel
needs — note how much of this page is power generation that an LCD controller simply does not have.
It is a useful reference point when someone claims an AMOLED driver is fitted behind a backlit panel.

---

## 11. What this document does *not* contain

**[NEG]** All confirmed absent from the 121 pages:

| Missing | Consequence |
|---|---|
| **The manufacturer command set** | The user command set is published; the init sequence that any real panel needs — gate timing, `NL`, MUX ratio, gamma key points, `SWIRE_ONF[5:0]`, `SPI_WRAM`, `DSPI_EN`/`DSPI_CFG`, the `TE1` output selector — is not. **You cannot bring up a panel from this document alone.** |
| Current consumption | All `TBD` (§7.3) |
| Source/GOA rise-fall times | All `TBD` |
| Pad coordinates / COG bump map | No pad-location table (contrast the ST7567A, which has four pages of them) |
| Any application circuit | Only the external-capacitor table, p.9 |
| Errata, revision history beyond "Original" | One row: V0.00, 2023-08-02 |
| Company name in text | §1.1 — logo only |
| Copyright or confidentiality notice | **None anywhere.** No redistribution statement of any kind |

**[INF]** This is an NDA-track specification that leaked or was mirrored, at its **first** version,
for a part aimed at module houses. Treat every number as provisional.

---

## 12. Used By

**None.** No device in this repository is documented as using a CH13620, and **no fitment is claimed
here.** The specification was acquired incidentally while probing the Crystalfontz controller-document
host during Xteink research (§13); it documents the part, not any board.

If you identify one — most plausibly inside a smartwatch or band module — add a row here and link
back from the device record.

---

## 13. Provenance — the URL that lied

| Field | Value |
|---|---|
| Source host | `www.crystalfontz.com` |
| URL form probed | `https://www.crystalfontz.com/controllers/UltraChip/UC8179/<id>/` |
| Numeric id that returned this file | **518** |
| Part the URL claimed | **UltraChip UC8179** (an e-paper driver — unrelated) |
| Part the file actually is | **Chip Wealth Technology CH13620** |
| Retrieved | **2026-09-11** |
| SHA-256 | `17034a7cb393f651901a9a02a84bd37baa76b2eb2de4deb33e0cc1f361c02700` |
| Byte size | **1 832 569** |
| Pages | 121 |
| Local artifact | `artifacts/ch13620-spec-v0.00-2023-08-02-crystalfontz-mirror.pdf` |
| Derived artifact | `artifacts/ch13620-cover-logo-chip-wealth-technology.png` — the manufacturer evidence, §1.1 |
| Disposition | **repository** (primary, 1.8 MB; no other copy of this document is known to us) |
| Licence | **unknown.** No copyright line, no confidentiality marking, no redistribution statement anywhere in the 121 pages |
| Redistribution status | **unknown** |

**The file is genuine; the URL is worthless as identification.** The measured id→part map is in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md#appended-2026-09-20--crystalfontz-numeric-id-probe-measured).

Filed under `components/chip-wealth-technology/` rather than under the Xteink device that occasioned
the fetch, per the skill's rule: **a file is filed by what it describes.**

---

## 14. Manufacturer

**芯颖科技有限公司 / Chip Wealth Technology Ltd.**

⚠ **There is no vendor documentation-sourcing guide for this manufacturer in this repository**, and
one is *not* being created here — writing a guide from a single logo and a single leaked PDF would
produce exactly the thin, low-evidence page the research method warns against. The gap is recorded
instead.

**What a future pass would need to establish**, and what is currently unknown:

| Question | Status |
|---|---|
| Corporate identity, domicile, registration | **[NEG]** Unknown. Nothing in the document |
| Official website and document portal | **[NEG]** Unknown. Not searched this pass |
| Part-numbering convention (`CH` + 5 digits) | **[NEG]** Unknown. ⚠ Collides with **WCH's** `CH` prefix — see §1.1 |
| Relationship to a panel maker or fab | Unknown |
| Whether any CH136xx document is published openly | Unknown |
| Other parts in the family | Unknown; the eleven resolutions in §2 suggest a family, not a single part |

See [`vendors/README.md`](../../../vendors/README.md) for the guides that do exist.

---

## 15. Related records and open questions

### Related

- [Sitronix ST7567A](../../sitronix/st7567a/README.md) — the other driver recovered from the same
  Crystalfontz probe, at the opposite end of the display market
- [Sitronix ST77916](../../sitronix/st77916/README.md) — QSPI TFT controller; its §2 is the canonical
  worked example of *"is this panel AMOLED or not"*
- [SH8601 compatibility driver record](../../generic/sh8601-compatibility-driver/README.md) — how the
  generic `02h`/`32h` QSPI framing (§4.2) gets reused across unrelated AMOLED and TFT controllers
- [Display interfaces guide](../../../guides/hardware/display-interfaces.md)
- [WCH documentation-sourcing guide](../../../vendors/wch/README.md) — the `CH`-prefix collision that
  makes this part number misleading (§1.1)

### Open questions

| Question | Status |
|---|---|
| Does the silicon have MIPI DSI pads that are simply not bonded out? | **Open.** §4.4. Two readings; neither established |
| Is the Deep Standby exit pulse 1 ms or 3 ms? | **Open.** §7.1. The document contradicts itself; use 3 ms |
| What are the actual operating currents? | **Open.** All `TBD` in V0.00 |
| Where is the manufacturer command set? | **Open.** §11. Not published; needed for any real bring-up |
| What selects `TE1`'s alternate output signals? | **Open.** Register not in the user command set |
| What is `SWIRE_ONF[5:0]` and where does it live? | **Open.** Named on p.97, defined nowhere |
| Is there a version later than V0.00? | **Open.** V0.00 is dated 2023-08-02; the PDF was produced 2024-01-22 |
| Does the half-size GRAM (§3.1) restrict full-frame RGB888? | **Open.** Inferred, not stated |

---

## Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| C1 | **CH13620 specification V0.00** | Chip Wealth Technology Ltd. (芯颖科技有限公司) | **primary** (via credible mirror) | datasheet | `https://www.crystalfontz.com/controllers/UltraChip/UC8179/518/` — ⚠ **the URL names a different part**; see §13 | 2026-09-11 | 2023-08-02 | Everything on this page unless marked otherwise | `artifacts/ch13620-spec-v0.00-2023-08-02-crystalfontz-mirror.pdf` |
| C2 | Cover-page logo raster extracted from C1 | Chip Wealth Technology Ltd. | primary (derived) | image | — (embedded object 11844 of C1) | 2026-09-20 | — | **The manufacturer's identity** — §1.1 | `artifacts/ch13620-cover-logo-chip-wealth-technology.png` |
| C3 | Crystalfontz numeric-id probe (`cfprobe`), 12 ids | this repository | — | measurement | — | 2026-09-11 / re-verified 2026-09-20 | — | The id→part map and the HTML-under-`.pdf` fallback | `archive/devices/xteink/shared-artifacts/research-scratch/datasheets/cfprobe/README.md` · [`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md) |
