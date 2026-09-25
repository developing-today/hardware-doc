# Solomon Systech SSD1680

- **Category:** active-matrix EPD (e-paper) display driver **with controller** — source/gate drivers, on-chip booster and regulators, oscillator, dual display RAM, programmable waveform engine, OTP waveform store, temperature sensing, SPI MCU interface, **two-chip cascade**
- **Package:** **gold-bump die only** (COG). No packaged part exists; it is bought on waffle pack and bonded to a panel.
- **Document status:** **"Product Preview", Rev 0.14, Jun 2019** — carries a five-entry revision history (0.10 → 0.14, 28-Feb-19 → 5-Jun-19)
- **Research status:** full datasheet retained in `artifacts/`; text layer **validated page-by-page** (§12). **No hardware, no driver source and no board was examined for this part.** This is a **reference-only** record — see §2.
- **Retrieved / written:** 2026-09-20

**The most widely deployed controller of the SSD16xx e-paper family** — the part behind the great majority of 1.54″/2.13″/2.9″ SPI e-paper modules sold by Waveshare, Good Display and their resellers. It is *not* fitted on any device documented in this repository.

---

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[DS]** | Stated in `artifacts/ssd1680-rev0.14-jun2019.pdf`, cited by the document's own section or **PDF page number** (which equals the printed footer page — proven in §12) | `not-tested` — vendor claim reproduced; nothing measured |
| **[CF]** | Crystalfontz controller catalogue, probed live 2026-09-20 | `executed-success` for the probe |
| **[REPO]** | An existing record in this repository | as labelled there |
| **[INF]** | Inference | `inferred` |

**Nothing in this record was verified on hardware.** No value was guessed; anything not in the document is marked as absent rather than filled in from a sibling part.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Solomon Systech Limited** | **[DS]** cover, footer of every page |
| Part | **`SSD1680`** | **[DS]** cover |
| Document title, verbatim | **"176 Source x 296 Gate Red/Black/White — Active Matrix EPD Display Driver with Controller"** | **[DS]** cover |
| Document status, verbatim | **"Product Preview"** — "This document contains information on a product under development. Solomon Systech reserves the right to change or discontinue this product without notice." | **[DS]** cover |
| Revision / date | **Rev 0.14, Jun 2019** | **[DS]** cover, footers, §revision history p. 2 |
| Revision history | 0.10 Initial Release (28-Feb-19) · 0.11 Updated Feature list (02-Apr-19) · 0.12 Updated AC Characteristics, Component list (21-May-19) · 0.13 Updated Component list (24-May-19) · **0.14 Updated Component list, removed case size for C0 and C1 (5-Jun-19)** | **[DS]** p. 2 |
| Ordering parts | **`SSD1680Z`** (gold bump die, **bump face up**) and **`SSD1680Z8`** (**bump face down**). Both: waffle pack, die thickness **300 µm**, bump height **12 µm** | **[DS]** §3, Table 3-1, p. 6 |
| Maximum geometry | **176 source outputs · 296 gate outputs · 1 VCOM · 1 VBD** ⇒ max resolution **176 × 296**; **352 × 296 in cascade mode** | **[DS]** §1 p. 5, §5 Table 5-4 p. 9 (`S[175:0]`, `G[295:0]`), §6.12 p. 19 |
| Colour capability | **Red / Black / White** — two full-size RAM planes, each `176 × 296` bits | **[DS]** §2 p. 5, §6.5 p. 13 |
| MCU interface | **SPI only** — 4-wire (8-bit) or 3-wire (9-bit), selected by the `BS1` pin | **[DS]** §6.1.1 Table 6-1, p. 10 |
| ⚠ Marking verified? | **No, and not applicable.** No unit was inspected. Identification here rests entirely on the document | **[INF]** |

### 1.1 What "Rev 0.14, Product Preview" actually means for you

Every number below is from a document Solomon Systech labelled *"a product under development"* and last touched in **June 2019** — and the entire revision history 0.10 → 0.14 changed **only the feature list, the AC table and the application-circuit component list**. Nothing in the register map was ever revised in any published revision. Either the register map was right first time, or no later revision was published. **This pass located no revision above 0.14 anywhere**, including in Crystalfontz's catalogue, which also holds 0.14 **[CF]**.

Treat it as provisional silicon documentation. In practice the world has been shipping this part for six years against exactly this document.

---

## 2. Used By — nothing here, and why the document was acquired anyway

**No device documented in this repository is known to use an SSD1680.** No schematic, firmware image, driver source or vendor statement in this tree names it as a fitted part. **Absence of evidence is recorded as absence**, not as a negative claim about the world: this part is extremely common in the wider e-paper market and could perfectly well be on a board nobody here has torn down.

It was acquired for two concrete reasons, both of which have already paid off:

1. **It is the SSD1677's decodable sibling.** The [SSD1677](../ssd1677/README.md) fitted on the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) documents command `0x0C` (Booster Soft-start Control) as an opaque 5-byte blob with exactly two legal values and **no bit table anywhere in its 47 pages**. The SSD1680 documents the same command **in full**, with driving-strength, minimum-off-time and per-phase-duration bit fields (§5.3 below). That decode is what
   [`devices/m5stack/papermono/gaps-and-conflicts.md`](../../../devices/m5stack/papermono/gaps-and-conflicts.md)
   used to establish what the PaperMono's booster bytes physically do — it cites *"SSD1680 (Rev 0.14, p.22)"*, which is this file **[REPO]**.
2. **It is the reference point for "the SSD16xx command set".** Community drivers, GxEPD2, and most vendor demo code are written against the SSD1680/SSD1681 command set and then ported sideways. Knowing precisely where the SSD1677 and SSD1683 diverge from it (§9) is the difference between a working port and a panel that resets, runs a waveform and never develops an image.

If a documented board ever turns out to carry one, this record gains a proper **Used By** section. Until then it is reference-only and says so.

---

## 3. Capabilities

**[DS]** §1–§2, pp. 5–6 unless noted.

| Area | Capability |
|---|---|
| Display RAM | **Two on-chip planes**, `176 × 296` bits each — B/W and "Red". No host framebuffer required |
| Supply | `VCI` **2.2–3.7 V**; `VDDIO` **connect to VCI**; `VDD` **1.8 V regulated from VCI** |
| Drive voltages, on-chip | Booster + regulator generate `VGH`, `VGL`, `VSH1`, `VSH2`, `VSL`, `VCOM` — **all six** |
| Gate output | 2 levels (`VGH`, `VGL`), **max 40 Vp-p**; `VGH` **10–20 V** in 500 mV steps; `VGL` = −`VGH` |
| Source / VBD output | 4 levels (`VSH1`, `VSH2`, `VSS`, `VSL`). `VSH1`/`VSH2` **2.4–17 V** (100 mV step to 8.8 V, 200 mV above); `VSL` **−5 to −17 V** (500 mV step) |
| VCOM | `DCVCOM` **−3 V to −0.2 V** in 100 mV steps; `ACVCOM` 3 levels (`VSH1+DCVCOM`, `DCVCOM`, `VSL+DCVCOM`). **Built-in VCOM sensing**, result programmable into OTP |
| Oscillator | **Adjustable frame rate 25 Hz – 200 Hz** |
| Waveform engine | **5 LUTs (LUT0–LUT4)**; **48 phases** (4 phases/group × 12 groups); `TP` max 255 frames/phase; `RP` repeat 1–256; **`SR` state repeat 1–256** for AB and CD independently; **per-group frame rate `FR`**; **`XON` all-gate-on per half-group** |
| OTP store | **36 waveform settings (WS0–WS35)** and **36 temperature ranges (TR0–TR35)**, plus VCOM value, display-mode selection, **4-byte waveform version**, **10-byte User ID**; separate embedded OTP for the **initial code setting** |
| OTP programming | External **or internal** generated voltage; **CRC checking for RAM content and for WS & TR in OTP** |
| Temperature | **Internal sensor, −25 to +50 °C, ±2 °C**, 12-bit value; or **I²C single-master interface** to an external sensor (`TSDA`/`TSCL`); or written by the host over SPI |
| Diagnostics | **VCI low-voltage detection** (programmable threshold) · **HV-ready (driving-voltage) detection with cool-down looping** · **panel break diagnostic** · status read `0x2F` |
| Display features | **Partial update** · **auto write RAM for regular patterns** (`0x46`/`0x47`) · **RAM Ping-Pong** (display mode 2 only) |
| Cascade | **Two chips → 352 × 296**, master/slave selected by the `M/S#` pin |
| MCU interface | 4-wire or 3-wire SPI, **max SPI write 20 MHz** |
| Package | **COG (gold bump die)** |

> The two features most likely to matter in practice are the ones a spec-dump would bury: **`SR` state repeat** and **per-group `FR`**. Between them they are why the SSD1680's LUT is 153 bytes rather than the SSD1677's 105 — the waveform engine here is genuinely more expressive, and a LUT is **not** portable between the two parts (§9-C1).

---

## 4. Interface, pins and the cascade pins you must not leave floating

### 4.1 4-wire vs 3-wire

**[DS]** §6.1.1, Table 6-1, p. 10. Pin-selected by **`BS1`**, not by a command:

| MCU interface | `BS1` | `D/C#` |
|---|---|---|
| **4-wire SPI** | **L** (to `VSS`) | real `D/C#` pin |
| 3-wire SPI (9-bit) | H (to `VDDIO`) | **tied LOW**; the D/C bit is the 9th bit of each frame |

4-wire write **[DS]** §6.1.2 Table 6-2, p. 10: `SDA` shifts in on every **rising** `SCL` edge, MSB first (D7→D0), `CS#` low; **`D/C#` must be held for the whole byte**. Read (3-wire form documented **[DS]** p. 12) shifts out on **falling** edges and applies only to registers `0x1B`, `0x27`, `0x2D`, `0x2E`, `0x2F`, `0x35`.

### 4.2 Pins that carry a hard requirement

**[DS]** §5, Tables 5-1 to 5-5, pp. 7–9. Host-facing and configuration pins only; the `S[175:0]`, `G[295:0]`, `VBD` and `VCOM` outputs and the analogue capacitor pins are in the datasheet's own tables.

| Pin | Type | Requirement / role |
|---|---|---|
| `BS1` | I | **To `VDDIO` or `VSS`** — interface select (§4.1) |
| **`M/S#`** | I | **Must be tied to `VDDIO` for single-chip use.** To `VSS` makes the chip a *slave*: oscillator, booster and regulator are **disabled** and `CL`, `VDD`, `VDDIO`, `VGH`, `VGL`, `VSH1`, `VSH2`, `VSL`, `VCOM` must all come from the master |
| **`CL`** | I/O | **Leave open for single-chip use.** In cascade, slave `CL` ties to master `CL` |
| `RES#` | I | Hardware reset, **active low**. **The only way out of deep sleep** |
| `CS#`, `D/C#`, `SCL` | I | SPI; `CS#` and `D/C#` may sit at `VDDIO` or `VSS` when unused |
| `SDA` | I/O | Serial data |
| `BUSY` | O | **High while busy.** Datasheet lists three causes: outputting display waveform, OTP programming, **talking to the digital temperature sensor**. ⚠ In cascade, the **slave's `BUSY` must be left open** |
| `TSDA` / `TSCL` | I/O, O | I²C to an external temperature sensor. **External pull-ups required**; leave open if unused |
| `GDR` | O | Gate drive for the external boost NMOS |
| `RESE` | I | Current-sense input for the boost control loop |
| `VPP` | P | OTP programming supply, **7.25 / 7.5 / 7.75 V** min/typ/max. Open when unused |
| `VCI`, `VCIA`, `VDDIO` | P | `VCIA` and `VDDIO` **both connect to `VCI`** in the application circuit |
| `VDD` | P | Core 1.8 V. **A capacitor to `VSS` is required under all circumstances** — and in cascade, only on the *master* |
| `VSS`, `VSSA`, `VSSBG`, `VSSGS` | P | Digital / analogue / reference / output grounds — **all connect to `VSS`** |
| `NC`, `RSV`, `TPA`–`TPF`, `TIN`, `TPE`, `FB` | NC | **Keep open, and do not connect to each other.** The datasheet states this explicitly and repeats it |

### 4.3 The external boost network is specified concretely

**[DS]** §13, Table 13-1, p. 43 — unusually, Solomon Systech gives real part numbers:

| Part | Value | Requirement |
|---|---|---|
| `C0`–`C1` | 1 µF | X5R/X7R, 6 V or 25 V |
| `C2`–`C7` | 1 µF | 0402/0603/0805, X5R/X7R, **25 V** |
| `C8` (VCOM) | 0.47 µF or 1 µF | 0603/0805 X7R 25 V — ⚠ **"Effective capacitance > 0.25 µF @ 18 V DC bias"**, which is the real constraint and the one a naive 0402 substitution fails |
| **`R1`** | **2.2 Ω** | 0402/0603/0805, **1 %**, ≥ 0.05 W — the `RESE` current-sense resistor |
| `D1`–`D3` | Schottky | **MBR0530**: V<sub>R</sub> ≥ 30 V, I<sub>o</sub> ≥ 500 mA, **V<sub>F</sub> ≤ 430 mV** |
| `Q1` | NMOS | **Si1304BDL / NX3008NBK**: BV<sub>DSS</sub> ≥ 30 V, V<sub>gs(th)</sub> 0.9 V typ / 1.3 V max, **R<sub>ds(on)</sub> ≤ 2.1 Ω @ V<sub>gs</sub> = 2.5 V** |
| `L1` | **47 µH** | CDRH2D18 / LDNP-470NC, I<sub>o</sub> 500 mA max |
| `U1` | 0.5 mm ZIF | **24 pins, 0.5 mm pitch** |

Note `R1 = 2.2 Ω` and `L1 = 47 µH` — **identical to the values DKE specifies for the SSD1677-based PaperMono panel** ([DEPG0397BBS770F3](../../dke/depg0397bbs770f3/README.md)). The family shares one boost topology; see [`papermono/gaps-and-conflicts.md`](../../../devices/m5stack/papermono/gaps-and-conflicts.md) for what that single MOSFET physically does (positive rail = boost, negative rail = charge-pump inversion of the same switch node).

Solomon Systech's own caveat, verbatim: the values are *"subject to change depending on panel loading"* and *"Customer is required to review if the selected component value and part is suitable for their application."* **[DS]** p. 43.

---

## 5. Waveforms: OTP versus external LUT

This is the part of the document that actually decides image quality, and where every SSD16xx port goes wrong.

### 5.1 The waveform setting is **159 bytes**, of which `0x32` writes **153**

**[DS]** §6.7, Figure 6-6, p. 15:

| WS byte | Content | Written by |
|---:|---|---|
| **0–152** | `VS[nX-LUTm]`, `TP[nX]`, `RP[n]`, `SR[nXY]`, `FR[n]`, `XON[nXY]` | **`0x32` (Write LUT register, 153 bytes)** |
| 153 | **`EOPT`** — Option for LUT end | `0x3F` |
| 154 | Gate level (`VGH`) | `0x03` |
| 155–157 | Source levels (`VSH1`, `VSH2`, `VSL`) | `0x04` |
| 158 | VCOM level | `0x2C` |

Byte-level layout **[DS]** Figure 6-6: bytes **0–59** are the `VS` voltage selectors (12 bytes per LUT × 5 LUTs, 4 phases packed 2 bits each per byte); **60–143** are the timing block (`TP`, `SR`, `RP` — 7 bytes per group × 12 groups); **144–149** pack `FR[0..11]` two per byte; **150–152** pack `XON[0..11]` as AB/CD bit pairs.

> ⚠ **This is the "153-byte LUT" that community SSD16xx code passes around**, and it is the layout the
> [SSD1677 record](../ssd1677/README.md) contrasts against — the SSD1677's `0x32` takes **105** bytes for a 40-phase engine, and the SSD1683's takes **227** for a 233-byte WS. **The three are mutually incompatible byte-for-byte.** §9-C1.

### 5.2 The waveform engine

**[DS]** §6.6, Figure 6-5 and pp. 13–14:

- **12 groups × 4 phases (A, B, C, D) = 48 phases.**
- `TP[nX]` = phase length in frames, **0–255**; **`TP = 0` skips the phase**.
- `RP[n]` = group repeat, **encoded `n` ⇒ `n+1` repeats**, so 0–255 means **1–256 times**.
- `SR[nAB]` / `SR[nCD]` = *state* repeat over the A+B and C+D phase pairs, same `n ⇒ n+1` encoding, **1–256**.
- `VS[nX-LUTm]`, 2 bits: `00` = `VSS`/`DCVCOM`, `01` = `VSH1`/`VSH1+DCVCOM`, `10` = `VSL`/`VSL+DCVCOM`, `11` = **`VSH2` / VCOM "N/A"** **[DS]** Table 6-6, p. 14.
- `FR[n]`, 3 bits (0–7), selects the frame rate **per group**.
- `XON[nAB]`/`XON[nCD]`: `1` = **all gates held high** through those phases instead of normal scan.

⚠ **`RP[n]` is documented inconsistently in its own paragraph**: the bullet says *"The range of RP[n] is from 0 to 255"* and then *"the maximum repeat times is 256"*, while the feature list on p. 5 says *"1 to 256 times for repeat count"*. These agree once you apply the `n ⇒ n+1` encoding; the wording does not. Same for `SR`. **[DS]** pp. 5, 14.

### 5.3 RAM bits → colour → LUT

**[DS]** §6.5, Tables 6-4 and 6-5, p. 13. This mapping is the thing to get right, and it **differs between 3-colour and B/W display modes**:

| R RAM (`0x26`) | B/W RAM (`0x24`) | 3-colour mode | B/W mode |
|:---:|:---:|---|---|
| 0 | 0 | Black — **LUT0** | Black — **LUT0** |
| 0 | 1 | White — **LUT1** | White — **LUT1** |
| 1 | 0 | **Red** — LUT2 | Black — **LUT2 = LUT0** |
| 1 | 1 | **Red** — LUT3 = LUT2 | White — **LUT3 = LUT1** |

So in B/W mode the Red plane is **ignored for colour** but still selects LUT2/LUT3, which are aliased to LUT0/LUT1. **LUT4 is not reachable from the RAM bits at all** — it is the border/VBD LUT, selected by `0x3C` `A[1:0]`.

### 5.4 OTP: 36 slots, automatic temperature selection, and the silent-failure mode

**[DS]** §6.9–§6.11, pp. 17–18.

OTP map **[DS]** Figure 6-7: **WS0 at address 0**, 159 bytes each, through **WS35 ending at 5723**; then **TR0 at 5724**, 3 bytes each, through **TR35 ending at 5831**.

TR format **[DS]** Figure 6-8, p. 18 — three bytes: `temp_L[7:0]`, then `temp_H[3:0]`:`temp_L[11:8]`, then `temp_H[11:4]`.

Temperature value format **[DS]** §6.8.3, p. 16 — **12-bit two's complement, value = binary / 16**. `0x190` = 25 °C; `0xE70` = −25 °C; `0x7FF` = 127.9 °C; `0x004` = 0.25 °C.

Selection **[DS]** §6.9:

1. Read the temperature as a 12-bit value (internal sensor via `0x18 = 0x80`, external via I²C, or written by the host via `0x1A`).
2. Search `TR0` → `TR35` **in sequence**, criterion **`lower bound < sensed ≤ upper bound`**.
3. **The last match wins.** The datasheet's own worked example is explicit: 34 °C matches both TR6 (30–35 °C) and TR7 (33–127.9 °C), and **WS7** is selected.
4. The matching WS is loaded into the LUT registers.

> ⚠ **Precaution, verbatim [DS] §6.9 p. 17:** *"Please ensure the temperature range covers whole range of application temperatures, **display will not be updated if no suitable temperature range matches the sensed temperature**."*
>
> This is a **silent** failure: outside the programmed ranges the panel simply does not refresh, with no error and no status bit. What the panel maker actually burned into the 36 slots is **not published by anybody**. `0x2D` (OTP Register Read) returning VCOM, display mode and a **4-byte waveform version** is the only in-system way to learn anything about it.

### 5.5 ⚠ DC balance — the hazard that destroys panels

Electrophoretic ink requires the net charge delivered over a waveform to sum to zero. **The OTP path cannot get this wrong** — balance was the panel maker's responsibility when it burned the waveform. **Writing `0x32` moves that responsibility to you**, and getting it wrong degrades the ink irreversibly over many refreshes. That is a destroyed display, not a glitch.

This datasheet does **not** state the warning; it is inherited from the family — see [SSD1677 §4.4](../ssd1677/README.md#44--the-dc-balance-hazard), where M5Stack documents it explicitly ("*irreversible damage may be caused to the panel*") and DKE states its electrical characteristics are *"only guaranteed under the controller & waveform provided by DKE"*. **Recorded here as a family-level hazard, `inferred` for this specific part** because this document is silent on it. The silence is itself worth knowing.

---

## 6. Command set

Full table **[DS]** §7, pp. 20–33; per-command detail **[DS]** §8, pp. 34–38. Reproduced below is what a driver actually has to get right, with the POR values, because **POR values are the single most-copied-wrong thing in SSD16xx ports**.

### 6.1 Geometry and windowing

| Cmd | Bytes | Meaning and POR **[DS]** |
|---|---|---|
| **`0x01`** | 3 | **Driver Output Control.** `A[8:0] = 0x127` **[POR] ⇒ 296 MUX**; gate lines = `A[8:0] + 1`, **16 MUX to 296 MUX**. `B[2] GD` first gate; `B[1] SM` scan order — `SM=0` [POR] left/right interlaced `G0,G1,G2…`, **`SM=1` ⇒ `G0,G2,G4…G294,G1,G3…G295`**; `B[0] TB` direction, `0` [POR] = `G0→G295` |
| **`0x0F`** | 2 | **Gate Scan Start Position.** `SCN[8:0]`, POR `0x000`. Selects which RAM row lands on the first gate — the mechanism for driving a panel with fewer gates than the RAM holds. ⚠ **Documented only in §8.2 (p. 36); it is absent from the §7 command table.** §9-C14 |
| **`0x11`** | 1 | **Data Entry Mode.** `A[2:0] = 011` **[POR]** = Y increment, X increment, counter advances in **X**. `A[1:0]` = ID[1:0] per-axis inc/dec; `A[2]` = AM axis |
| **`0x44`** | 2 | **Set RAM X start/end.** ⚠ **`XSA`/`XEA` are in units of 8 pixels (bytes), not pixels.** POR `XSA = 0x00`, **`XEA = 0x15` (21 ⇒ 22 bytes ⇒ 176 sources)** |
| **`0x45`** | 4 | **Set RAM Y start/end**, in **gate lines**. POR `YSA = 0x000`, **`YEA = 0x127` (295 ⇒ 296 gates)** |
| `0x4E` / `0x4F` | 1 / 2 | **Set RAM X / Y address counter.** POR `0x00` / `0x000` |

> ⚠ **X is addressed in bytes and Y in lines. They are not symmetric, and the SSD1677 does it differently** (that part addresses X in *pixels*, POR `XEA = 0x3BF = 959`). Porting window code between the two without changing the unit produces a window 8× too wide or 8× too narrow. §9-C1.

> ⚠ **The datasheet contradicts itself on the width of `XSA`/`XEA`.** The command table (p. 31) writes them as **`A[5:0]`/`B[5:0]` — 6 bits**; §8.4 (p. 38) writes them as **`XSA[4:0]`/`XEA[4:0]` — 5 bits**, and constrains `00h ≤ XSA, XEA ≤ 15h`. The POR value `0x15` fits either. For a 176-source part 5 bits is sufficient (22 byte-units); the 6-bit form is what the 400-source [SSD1683](../ssd1683/README.md) needs. **[INF]** the command table was carried over from the wider sibling. Use the §8.4 range limit — it is the constraint that is actually stated.

### 6.2 Voltages

| Cmd | Meaning and POR **[DS]** |
|---|---|
| **`0x03`** | **Gate Driving Voltage.** `A[4:0] = 0x00` **[POR] ⇒ VGH = 20 V.** Table runs `03h`=10 V … `17h`=20 V in 0.5 V steps. ⚠ The table **lists `07h`=12 and `08h`=12.5 twice** and omits `01h`/`02h`; `00h` = 20 V sits outside the monotonic run |
| **`0x04`** | **Source Driving Voltage**, 3 bytes. **`A = 0x41` [POR] ⇒ VSH1 = 15 V · `B = 0xA8` ⇒ VSH2 = 5 V · `C = 0x32` ⇒ VSL = −15 V.** ⚠ **The encoding is split by bit 7**: `A[7]/B[7] = 1` selects the 2.4–8.8 V range (`8Eh`–`CEh`, 100 mV steps), `= 0` selects 9–17 V (`23h`–`4Bh`, 200 mV steps). `C[7] = 0`, VSL `0Ah`–`3Ah` in 500 mV steps. **Remark: `VSH1 >= VSH2`** |
| **`0x2C`** | **Write VCOM register.** `A[7:0] = 0x00` [POR]. `08h` = −0.2 V … `78h` = −3.0 V in 0.1 V steps (step of 4 in the code) |
| `0x2B` | **Write Register for VCOM Control.** *"used to reduce glitch when ACVCOM toggle. **Two data bytes `D04h` and `D63h` should be set**"* — a magic pair with no explanation. Worth issuing if you see VCOM glitching |

### 6.3 Booster soft-start — the command the SSD1677 hides

**[DS]** §7, `0x0C`, p. 22. **Four bytes**, POR **`8B 9C 96 0F`**.

| Byte | Role |
|---|---|
| `A` | Soft-start setting, **phase 1** — POR `8Bh` |
| `B` | Soft-start setting, **phase 2** — POR `9Ch` |
| `C` | Soft-start setting, **phase 3** — POR `96h` |
| `D` | **Duration** — POR `0Fh` |

Bit fields of `A`/`B`/`C` (bit 7 is written as a literal `1`):

| Bits | Meaning |
|---|---|
| `[6:4]` | **Driving strength**, `000` = 1 (weakest) … `111` = 8 (strongest) |
| `[3:0]` | **Minimum off-time of `GDR`** [time units]: `0000`–`0011` = **NA**; `0100` = 2.6, `0101` = 3.2, `0110` = 3.9, `0111` = 4.6, `1000` = 5.4, `1001` = 6.3, `1010` = 7.3, `1011` = 8.4, `1100` = 9.8, `1101` = 11.5, `1110` = 13.8, `1111` = 16.5 |

`D[5:4]` / `D[3:2]` / `D[1:0]` = **duration of phase 3 / 2 / 1**, `00` = 10 ms, `01` = 20 ms, `10` = 30 ms, `11` = 40 ms.

So POR `8B 9C 96 0F` decodes to: phase 1 strength 1 / off-time 8.4, phase 2 strength 2 / off-time 9.8, phase 3 strength 2 / off-time 3.9, all three phases 40/40/40 ms → wait, `0Fh = 00 00 1111` ⇒ phase 3 = `00` = 10 ms, phase 2 = `11` = 40 ms, phase 1 = `11` = 40 ms. **[INF]** on the decode arithmetic; the field definitions are **[DS]**.

> This table is the entire reason this document is in the repository. The SSD1677 takes **five** bytes here with only two legal values tabulated and **no bit definitions published anywhere** — see [`papermono/gaps-and-conflicts.md`](../../../devices/m5stack/papermono/gaps-and-conflicts.md), which applies this decode to the SSD1677's `AE C7 C3 C0 80` and finds A/B/C fit and **D does not**. The 5-byte SSD1677 encoding remains unresolved.

### 6.4 Refresh: `0x22` then `0x20`

`0x22` (Display Update Control 2) selects the sequence; `0x20` (Master Activation) runs it. **[DS]** §7, pp. 25–26: *"BUSY pad will output high during operation. **User should not interrupt this operation to avoid corruption of panel images.**"*

**Twelve documented `0x22` values** — POR `0xFF`:

| Value | Sequence |
|---|---|
| `0x80` / `0x01` | Enable / disable clock signal |
| `0xC0` / `0x03` | Enable clock + enable analog / disable analog + disable clock |
| `0x91` / `0x99` | Enable clock → **load LUT with display mode 1 / 2** → disable clock |
| `0xB1` / `0xB9` | Enable clock → **load temperature** → load LUT mode 1 / 2 → disable clock |
| `0xC7` / `0xCF` | Enable clock → enable analog → **display mode 1 / 2** → disable analog → disable OSC |
| `0xF7` / `0xFF` | Enable clock → enable analog → **load temperature** → **display mode 1 / 2** → disable analog → disable OSC |

The values are clearly a bit-field (`CF = C7 | 0x08`, `F7 = C7 | 0x30`, `B1 = 91 | 0x20`) but **the bit definitions are not published**. Copy a value from this table; do not compose one.

`0x21` **Display Update Control 1** — `A[7:4]` Red RAM option, `A[3:0]` BW RAM option, each `0000` normal [POR] / `0100` **bypass RAM content as 0** / `1000` inverse. `B[7]` **Source Output Mode**: `0` = sources `S0`–`S175`, **`1` = sources `S8`–`S167`** (a 160-wide centred window).

### 6.5 RAM access

| Cmd | Meaning **[DS]** |
|---|---|
| `0x24` | **Write RAM (Black/White).** **White pixel ⇒ 1, black ⇒ 0.** Pointers auto-advance until another command |
| `0x26` | **Write RAM (RED).** Red ⇒ 1, non-red ⇒ 0 |
| `0x27` | **Read RAM.** Plane selected by `0x41`. ⚠ **The first byte read is dummy data** |
| `0x41` | **Read RAM Option.** `A[0] = 0` [POR] ⇒ read `0x24` plane; `1` ⇒ `0x26` plane |
| `0x46` / `0x47` | **Auto Write RED / B/W RAM for Regular Pattern.** POR `0x00`. `A[7]` first step value; `A[6:4]` step **height** (8/16/32/64/128/256/**296**); `A[2:0]` step **width** (8/16/32/64/128/**176**). BUSY high during operation |
| `0x7F` | **NOP** — terminates a frame-memory write or read |

### 6.6 Deep sleep — **two** modes, and the RAM-retention difference

**[DS]** §7, `0x10`, p. 23:

| `A[1:0]` | Mode |
|---|---|
| `00` | **Normal [POR]** |
| **`01`** | **Enter Deep Sleep Mode 1** — *RAM data retained but not accessible* |
| **`11`** | **Enter Deep Sleep Mode 2** — *RAM data not retained* |

*"After this command initiated, the chip will enter Deep Sleep Mode, BUSY pad will keep output high. Remark: **To exit Deep Sleep mode, user required to send HWRESET to the driver.**"* And `0x12` SWRESET *"resets the commands and parameters to their S/W Reset default values **except R10h-Deep Sleep Mode**"*, with *"**RAM are unaffected by this command**"* — so you cannot software-reset out of deep sleep, and a SWRESET does not clear the image.

Currents **[DS]** Table 11-1, p. 41: mode 1 **1 µA typ / 3 µA max**, mode 2 **0.7 µA typ / 3 µA max**, sleep mode 20 µA typ / 35 µA max.

> ⚠ **This resolves an open question in the [SSD1677 record](../ssd1677/README.md#7-caveats-errata-and-conflicts) (§7-C5).** That record notes that both DKE's reference program and M5Stack's demo write `0x10` `{0x01}` although the SSD1677 datasheet documents only `00` and `11`, and calls the convergence *"loose decoding or a shared typo"*. **On the SSD1680, SSD1681 and SSD1683, `01` is a documented value — Deep Sleep Mode 1, the RAM-retaining variant.** The obvious reading is that the SSD1677 silicon implements the same two-mode encoding and its datasheet omitted mode 1, and that both vendors' code came from a family reference that used it. **This is `inferred`** — it is evidence from sibling parts, not from the SSD1677 document or from hardware — but it is a far better explanation than a typo, and it is checkable: on an SSD1677, `0x10` `{0x01}` should leave RAM intact across the sleep where `{0x03}` does not.

### 6.7 Status, diagnostics and OTP

**[DS]** §7, pp. 24, 29–30. These are the registers a robust driver reads and almost no driver does.

| Cmd | What it gives you |
|---|---|
| **`0x2F`** | **Status Bit Read** [POR `0x01`]. `A[5]` **HV-ready** (0 ready / 1 not ready) · `A[4]` **VCI detection** (0 normal / 1 VCI below threshold) · `A[2]` busy · `A[1:0]` **chip ID [POR `01`]**. ⚠ **`A[5]` and `A[4]` are invalid after reset until `0x14` and `0x15` have been issued** |
| **`0x14`** | **HV Ready Detection.** Requires `CLKEN=1` **and** `ANALOGEN=1`. `A[6:4] = n` cool-down `10 ms × (n+1)`; `A[2:0] = m` loop count; max duration `10 ms × (n+1) × m`. **`A = 0x00` = one-shot** |
| **`0x15`** | **VCI Detection.** `A[2:0] = 100` [POR] ⇒ threshold **2.3 V**; `011`=2.2, `101`=2.4, `110`=2.5, `111`=2.6 V. Requires `CLKEN=1` and `ANALOGEN=1` |
| `0x2D` | **OTP Register Read for Display Option** — 11 bytes: VCOM OTP selection, VCOM register, **5 bytes display mode**, **4 bytes waveform version**. The only in-system way to identify the programmed waveform |
| `0x2E` | **User ID Read** — 10 bytes from OTP |
| `0x34` / `0x35` | **CRC calculation** and **CRC status read** (16-bit) over OTP waveform data. *"refer to SSD1680 application note"* — **that application note is not public and was not located** |
| `0x28` / `0x29` | **VCOM Sense** and sense duration, `(A[3:0]+1)` seconds, POR `9h` ⇒ **10 s** |
| `0x30` / `0x31` | **Program / Load WS OTP** |
| `0x2A` | Program VCOM register into OTP |
| `0x36` / `0x37` / `0x38` | Program OTP selection · Write Display Option register (display mode per WS, **`F[6]` RAM Ping-Pong**, module ID / waveform version) · Write 10-byte User ID |
| `0x39` | **OTP program mode.** `00` normal [POR], `11` **internal generated programming voltage**. *"User is required to **EXACTLY** follow the reference code sequences"* — and those sequences are not in this document |
| `0x08`/`0x09`/`0x0A` | Program / write / read **Initial Code Setting** OTP. *"Details refer to Application Notes of Initial Code Setting"* — **also not public** |

> ⚠ Three separate commands defer to **application notes that are not published**: `0x09` (initial code setting), `0x34` (CRC), `0x39` (OTP programming sequence). If you intend to *program* OTP rather than just read it, this datasheet is not sufficient and you need the panel maker.

### 6.8 `0x3C` Border Waveform Control, and the `0x3F` oddity

`0x3C` POR **`0xC0` = VBD HiZ**. `A[7:6]`: `00` GS transition (defined by `A[2]` and `A[1:0]`) · `01` fixed level (`A[5:4]`: VSS/VSH1/VSL/VSH2) · `10` VCOM · `11` **HiZ [POR]**. `A[1:0]` picks LUT0–LUT3 for the transition.

⚠ **`0x3F` (End Option, `EOPT`) has a POR value that is not one of its documented values.** The datasheet gives `A[7:0] = 02h` **[POR]**, then lists exactly two meanings: **`22h` Normal** and **`07h` Source output level keep previous output before power off**. `02h` is undefined. **[DS]** p. 31. The SSD1683 resolves this by dropping the POR and simply instructing *"Set this byte to 22h"* — which is probably the right advice here too, but **this document does not say so** and it is marked `inferred`.

---

## 7. Reference operation flow

**[DS]** §9.1, Figure 9-1, p. 39, transcribed:

```
START
 1. Power On            — supply VCI; wait 10 ms
 2. Set Initial Configuration
                        — define SPI interface; HW reset; SW reset (0x12); wait 10 ms
 3. Send Initialization Code
                        — set gate driver output: 0x01
                        — set display RAM size: 0x11, 0x44, 0x45
                        — set panel border: 0x3C
 4. Load Waveform LUT   — sense temperature by int/ext TS: 0x18
                        — load waveform LUT from OTP by 0x22, 0x20 — or by MCU
                        — wait BUSY low
 5. Write Image and Drive Display Panel
                        — write image data: 0x4E, 0x4F, 0x24, 0x26
                        — set soft-start: 0x0C
                        — drive panel: 0x22, 0x20
                        — wait BUSY low
 6. Power Off           — deep sleep: 0x10; power off
END
```

> ⚠ **Note what is *not* in step 3.** The SSD1677's otherwise-identical flow opens step 3 with *"Clear and fill two RAM by Command 0x46 data 0xF7 and 0x47 data 0xF7"* — **the SSD1680's flow omits the RAM pre-clear entirely**, even though it has both commands. Since RAM survives SWRESET but not deep sleep mode 2, the first frame after a cold start is drawn against undefined RAM in whichever plane you did not write. Neutralise it with `0x21`'s *"bypass RAM content as 0"*, or write both planes. **[DS]** §9.1 vs [SSD1677 §6](../ssd1677/README.md); consequence `inferred`.

---

## 8. Electrical

### 8.1 Absolute maximum ratings

**[DS]** §10, Table 10-1, p. 40.

| Symbol | Parameter | Rating | Unit |
|---|---|---|---|
| `VCI` | Logic supply voltage | **−0.5 to +6.0** | V |
| `VIN` / `VOUT` | Logic input / output voltage | −0.5 to V<sub>DDIO</sub> + 0.5 | V |
| **`TOPR`** | Operating temperature | **−40 to +85** | °C |
| `TSTG` | Storage temperature | −65 to +150 | °C |

⚠ **`VCI` absolute max is +6.0 V here, against +4.0 V on the [SSD1677](../ssd1677/README.md#81-absolute-maximum-ratings).** Do not carry a headroom assumption across the family in either direction.

Datasheet's own notes: unused inputs to `VSS` or `VDDIO`; **unused outputs must be left open**; *"This device may be light sensitive. Caution should be taken to avoid exposure of this device to any light source during normal operation."*; *"This device is not radiation protected."*

### 8.2 DC characteristics

**[DS]** §11, Table 11-1, pp. 40–41. Conditions `VSS = 0 V`, `VCI = 3.0 V`, `VDD = 1.8 V`, `TOPR = 25 °C`.

| Symbol | Parameter | Condition | Min | Typ | Max | Unit |
|---|---|---|---:|---:|---:|---|
| `VCI` | Operating voltage | | **2.2** | 3.0 | **3.7** | V |
| `VDD` | Core | | 1.7 | **1.8** | 1.9 | V |
| `VCOM_DC` | VCOM DC output | | **−3.0** | | **−0.2** | V |
| `VGATE` | Gate output | `G0~G295` | −20 | | +20 | V |
| `VGATE(p-p)` | Gate peak-to-peak | | | | **40** | V |
| `VSH1` / `VSH2` | Positive source outputs | | +2.4 / +2.4 | 15 / 5 | +17 / +17 | V |
| `VSL` | Negative source output | | **−17** | −15 | **−9** | V |
| `VPP` | OTP program voltage | | 7.25 | **7.5** | 7.75 | V |
| `Islp_VCI` | **Sleep mode** | DC/DC off, MCU + RAM access allowed | | **20** | 35 | µA |
| `Idslp_VCI1` | **Deep sleep 1** | RAM retained, not accessible | | **1** | 3 | µA |
| `Idslp_VCI2` | **Deep sleep 2** | RAM not retained | | **0.7** | 3 | µA |
| `Iopr_VCI` | Operating | `VCI = 3.0 V` | | **1000** | | µA |
| `VGH` | | via Master Activation | 19.5 | 20 | 20.5 | V |
| `VIH` / `VIL` | Logic thresholds | | 0.8 V<sub>DDIO</sub> | | 0.2 V<sub>DDIO</sub> | V |
| `VOH` / `VOL` | Logic outputs | ±100 µA | 0.9 V<sub>DDIO</sub> | | 0.1 V<sub>DDIO</sub> | V |

⚠ **`VSL` min/max is `−17 / −9 V` in the DC table but the feature list says `−5 V to −17 V`** and the `0x04` `C[7:0]` code table starts at `0Ah` (the row's value cell is blank in the text layer) and runs `0Ch = −5.5 V`. The −9 V bound in Table 11-1 is the narrower claim. **[DS]** pp. 5, 21, 41. Unresolved; the register clearly *accepts* values above −9 V.

Regulator source capability **[DS]** Table 11-2, p. 41: `IVSH1`, `IVSH2`, `IVSL` **800 µA max each**; `IVCOM` **100 µA max**. ⚠ **These are far below the SSD1677's** (2000 µA source / 2000 µA VCOM) — this is a smaller-panel part and its regulators say so.

### 8.3 AC — SPI timing

**[DS]** §12.1, Table 12-1, p. 42. `VDDIO − VSS = 2.2–3.7 V`, `TOPR = 25 °C`, **`CL = 20 pF`**.

| Symbol | Parameter | Write | Read | Unit |
|---|---|---:|---:|---|
| **`fSCL`** | **SCL frequency (max)** | **20** | **2.5** | **MHz** |
| `tCSSU` | `CS#` low before first rising `SCLK` (min) | 60 | 100 | ns |
| `tCSHLD` | `CS#` low after last falling `SCLK` (min) | 65 | 50 | ns |
| `tCSHIGH` | `CS#` high between transfers (min) | 100 | 250 | ns |
| `tSCLHIGH` / `tSCLLOW` | Clock high / low (min) | 25 / 25 | 180 / 180 | ns |
| `tSISU` / `tSIHLD` | Data setup / hold, write (min) | 10 / 40 | — | ns |
| `tSOSU` / `tSOHLD` | Data valid / hold, read (typ) | — | 50 / 0 | ns |

All timings **20 % to 80 % of `VDDIO − VSS`**.

> ⚠ **Read is 8× slower than write.** 20 MHz write, **2.5 MHz read**. Every register in §6.7 is on the slow path. A driver that sets one clock for the whole bus and then reads `0x2F` is out of spec on the read.

---

## 9. Caveats, errata and conflicts

| # | Issue | Evidence |
|---|---|---|
| **C1** | **⚠ SSD1677, SSD1680/1681 and SSD1683 LUTs are mutually incompatible, and so is window addressing.** `0x32` takes **105 / 153 / 227** bytes respectively; the WS is **112 / 159 / 233** bytes; the engine is **40 / 48 / 48** phases; the SSD1680/1681 have `SR` state-repeat and `XON` which the SSD1677 lacks. And **the SSD1677 addresses RAM X in *pixels* (POR `XEA = 0x3BF = 959`) while the SSD1680/1681/1683 address it in *bytes*** (POR `0x15` / `0x15` / `0x31`). A "SSD16xx" driver is not a thing; a per-part driver is | **[DS]** §6.7 p. 15, §7 `0x32` p. 29, §7 `0x44` p. 31; [SSD1677 §4.1, §5.2](../ssd1677/README.md) |
| **C2** | **The `XSA`/`XEA` bit width is stated two ways** — `A[5:0]` in the command table (p. 31), `XSA[4:0]` in §8.4 (p. 38) with range `≤ 15h`. Both admit the POR value. **[INF]** the 6-bit form was carried from a wider sibling | **[DS]** pp. 31, 38 |
| **C3** | **`0x3F` `EOPT` POR value `02h` is not one of its two documented values** (`22h`, `07h`). The SSD1683 drops the POR and just says *"Set this byte to 22h"* | **[DS]** p. 31; [SSD1683 §6](../ssd1683/README.md) |
| **C4** | **`VSL` lower bound disagrees between the feature list (−5 V) and the DC table (−9 V max).** The register encoding supports values above −9 V | **[DS]** pp. 5, 21, 41 |
| **C5** | **The `0x03` VGH code table contains duplicate rows.** `07h = 12` and `08h = 12.5` each appear twice; `01h`/`02h` are absent; `00h` [POR] = 20 V sits outside the monotonic 10→20 V run. Probably a layout artefact of a two-column table, but it is what is printed | **[DS]** p. 20 |
| **C6** | **`0x22` bit definitions are unpublished.** Twelve composite values are tabulated and are transparently a bit-field, but no source in hand defines the bits. Copy a tabulated value; do not compose one | **[DS]** p. 26 |
| **C7** | **Three commands defer to application notes that are not public** — `0x09` initial code setting, `0x34` CRC, `0x39` OTP programming. OTP *programming* is out of reach with this document alone | **[DS]** pp. 21, 29, 30 |
| **C8** | **OTP contents are unpublished and out-of-range temperature silently prevents refresh.** Which of the 36 WS/TR slots a given panel maker burned, and over what span, is disclosed by nobody. `0x2D` is the only in-system probe | **[DS]** §6.9 p. 17, §7 p. 28 |
| **C9** | **The datasheet's own operation flow omits the RAM pre-clear** that the SSD1677's flow performs with `0x46`/`0x47`. First frame after a cold start is drawn against undefined RAM in the unwritten plane | **[DS]** §9.1 p. 39 |
| **C10** | **"Product Preview", six years stale.** Rev 0.14 (Jun 2019) is the newest revision located, including in Crystalfontz's catalogue. Solomon Systech disclaims it as *"a product under development"* | **[DS]** cover; **[CF]** |
| **C11** | **`M/S#` and `CL` are not optional.** Single-chip designs must tie `M/S#` to `VDDIO` and leave `CL` open. Tying `M/S#` low silently disables the oscillator, booster and regulator — the symptom is a chip that accepts commands and never drives the panel | **[DS]** §5 p. 8, §6.12 p. 19 |
| **C12** | **Read timing is 8× slower than write** (2.5 MHz vs 20 MHz), and every diagnostic register is on the read path | **[DS]** §12.1 p. 42 |
| **C13** | **The DC-balance hazard is not stated in this document.** It is real for the whole family and is documented by M5Stack and DKE for the SSD1677. Its absence here should not be read as absence of the hazard | **[INF]**; [SSD1677 §4.4](../ssd1677/README.md#44--the-dc-balance-hazard) |
| **C14** | **`0x0F` exists but is missing from the command table.** §7's table (pp. 20–33) enumerates 49 commands and `0x0F` is not among them — a full census of the table was taken, `executed-success`. §8.2 (p. 36) then documents *Gate Scan Start Position (0Fh)* in full, with a POR value, a bit layout and a worked example at three MUX ratios. A driver author reading only the command table will never find it, and it is precisely the command needed to drive a short panel off a 296-line controller | **[DS]** §7 pp. 20–33 (census), §8.2 p. 36 |

---

## 10. Libraries

**No library was audited against this datasheet in this pass** — that is the obvious next piece of work and it is recorded as a gap rather than guessed at. What is known:

| Option | Status |
|---|---|
| **GxEPD2** (`ZinggJM/GxEPD2`) | The dominant Arduino library for SSD1680-class panels. **Not examined here.** |
| **Waveshare / Good Display vendor demos** | Per-panel C demos in the SSD16xx house style. **Not examined here.** |
| Mainline Linux DRM | **No SSD1680 driver was located in this pass.** `not-tested` |
| Roll your own | §6 plus §7 is a complete enough command surface. **Use OTP waveforms** unless you can prove DC balance (§5.5) |

The [SSD1677 record §9](../ssd1677/README.md#9-libraries) contains a worked, line-cited audit of two vendor drivers against a sibling datasheet, including a 2× SPI-overclock finding. That is the template for what should happen here.

---

## 11. Related components and records

- [**Solomon Systech SSD1677**](../ssd1677/README.md) — the 960 × 680 sibling, **fitted on real hardware in this repository**. Read it for the driver-audit findings and the DC-balance hazard
- [**Solomon Systech SSD1681**](../ssd1681/README.md) — 200 × 200. **Near-identical document to this one**; §1.1 there records the copy-paste defect it inherited
- [**Solomon Systech SSD1683**](../ssd1683/README.md) — 400 × 300, the larger sibling with a 227-byte LUT
- [**Solomon Systech SSD7317**](../ssd7317/README.md) — unrelated: OLED + in-cell touch. Filed here because it arrived in the same mis-named batch
- [**Vendor sourcing guide — Solomon Systech**](../../../vendors/solomon-systech/README.md) — ⚠ **read §2 before fetching any Solomon Systech PDF.** Mirror-sourced copies arrive misnamed
- [**UltraChip UC8179**](../../ultrachip/uc8179/README.md) / [**UC8279**](../../ultrachip/uc8279/README.md) — the competing e-paper controller family. Family trait: **UC81xx answer `VER (0x70)`/`FLG (0x71)`; SSD16xx do not**, which is how runtime controller detection works
- [**Guide — e-paper displays**](../../../guides/hardware/e-paper-displays.md) — integrated-controller modules versus raw parallel AMEPD panels

---

## 12. Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/ssd1680-rev0.14-jun2019.pdf` | 2 759 375 | `b28ec2b412a866c9846940e035b7e38701db0ac8d80b1beccac39a26743e595f` | **SSD1680 datasheet, "Product Preview", Rev 0.14, Jun 2019.** PDF 1.4, A4, **46 pages**. `Title`/`Subject`/`Keywords` all `SSD1680`. Creator **PDFCreator 1.5.0**, Producer **GPL Ghostscript 9.05**, CreationDate **2019-06-05**, ModDate **2020-05-06**. `Optimized: no` |

**Text-layer validation — `executed-success`.** `pdftotext -layout` output was checked against the cover block (`SOLOMON SYSTECH` / `SEMICONDUCTOR TECHNICAL DATA` / `Product Preview`), the revision-history table and the numbered contents list. Then, mechanically: **for all 46 pages the PDF page index equals the printed footer `SSD1680 Rev 0.14 P n/46 Jun 2019`**, and 46 == the PDF page count. No dropped pages, no glyph subsetting, no code-point offset. Extracted section headings match the contents list exactly. Every value transcribed above comes from that validated layer.

**A second, byte-different copy of the same document exists and was identified.** Crystalfontz serves this datasheet at `https://www.crystalfontz.com/controllers/Solomon%20Systech/SSD1680/497/` — **857 636 bytes, SHA-256 `c6d3090bcd8a65120e6e1f23f71fddd931662e0dd15a360b6d13fd7b2c8a4748`**, fetched and hashed 2026-09-20 (`executed-success`). It is **not a different revision**: identical `CreationDate` (2019-06-05), identical Creator and Producer, identical 46 pages, and **whitespace-normalised `pdftotext` output is byte-identical to the copy retained here**. The difference is that Crystalfontz's copy has `Optimized: yes` and a later `ModDate` (2021-05-10) — it is a re-optimised derivative, ~3.2× smaller. **Only the larger, unoptimised copy is retained**, because it is the earlier and less-processed artifact; the Crystalfontz hash is recorded here so a future agent can identify that file on sight instead of re-deriving the comparison. This is a deliberate departure from "keep both", justified by having *proven* equivalence rather than assumed it.

**Provenance of the retained copy is incomplete.** It reached this repository as `SSD1680_gh.pdf` in a 2026-09-11 scratch batch; the `_gh` suffix suggests a GitHub-hosted copy but **no URL was recorded by the acquiring session and none was recovered**. Recorded as `unknown` rather than guessed. The Crystalfontz URL above is a **verified working reacquisition path for an equivalent document**.

**Licence.** Third-party (Solomon Systech) copyright — the cover carries *"Copyright © 2019 Solomon Systech Limited"*. **No per-page confidentiality footer**, unlike some vendor datasheets in this repository; no redistribution terms stated. Redistribution status **`unknown`**; disposition **`repository`**.

---

## 13. Authoritative sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | SSD1680 — 176 Source × 296 Gate Red/Black/White Active Matrix EPD Display Driver with Controller | **Solomon Systech Limited** | primary (via unrecorded mirror) | datasheet | `artifacts/ssd1680-rev0.14-jun2019.pdf`; upstream URL **unknown** | 2026-09-11 (acquired), 2026-09-20 (verified, filed) | **Rev 0.14, Jun 2019 — "Product Preview"** | §1, §3–§9 |
| S-2 | Same document, Crystalfontz-optimised copy | Solomon Systech, mirrored by **Crystalfontz America** | credible mirror | datasheet | `https://www.crystalfontz.com/controllers/Solomon%20Systech/SSD1680/497/` | **2026-09-20** | Rev 0.14, Jun 2019 | §12 — a working reacquisition path; content equivalence proven |
| S-3 | Crystalfontz controller catalogue | Crystalfontz America | credible mirror | catalogue (embedded JSON) | `https://www.crystalfontz.com/controllers/` | **2026-09-20** | undated | §12, and [vendors/solomon-systech §3](../../../vendors/solomon-systech/README.md) — that document id **497** is SSD1680 v0.14, and that **no SSD1677 exists in the catalogue** |
| S-4 | PaperMono gaps and conflicts — booster soft-start decode | this repository | — | record | [`devices/m5stack/papermono/gaps-and-conflicts.md`](../../../devices/m5stack/papermono/gaps-and-conflicts.md) | 2026-09-20 | pass of 2026-09-11 | §2, §6.3 — the in-repo consumer of this document |
