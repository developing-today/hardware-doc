# Solomon Systech SSD7317

- **Category:** ⚠ **Not an e-paper part.** Single-chip **OLED/PLED segment/common driver with an integrated capacitive touch controller** — 128 × 96 monochrome display, GDDRAM, contrast control, oscillator, DC-DC enable output, **plus** an in-cell touch analogue/digital front end driven by a **16-bit CPU running host-downloaded firmware**
- **Package:** **gold-bump die only** (COG). Ordering part **`SSD7317Z`**.
- **Document status:** **"Advance Information", Rev 1.3, Oct 2020**
- **Research status:** ⚠ **the retained PDF is an OCR'd scan and its text layer is demonstrably corrupted** (§10). Values below were transcribed only where they are corroborated at two or more places in the document. **No hardware, no driver source and no board was examined.** **Reference-only** — see §2.
- **Retrieved / written:** 2026-09-20

> ⚠⚠ **Two warnings before anything else.**
>
> 1. **This file reached the repository named `ssd1680.pdf` and is not an SSD1680.** It is not an e-paper controller at all. The mechanism is recorded in [`vendors/solomon-systech` §2](../../../vendors/solomon-systech/README.md).
> 2. **The artifact is a 4-document bundle, not a datasheet** — 87 PDF pages comprising a 37-page datasheet, two 13-page software porting guides *at different revisions from the datasheet and from each other*, and a 24-page appendix set. §10.

---

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[DS]** | SSD7317 datasheet Rev 1.3, PDF pages **1–37** of the bundle, cited by the document's own printed page | `not-tested`, and ⚠ **read through an OCR layer** — see §10 |
| **[SPI]** | *SSD7317 SPI Software Porting User Guide*, Rev 1.0, Apr 2019 — PDF pages **38–50** | `not-tested`, OCR |
| **[I2C]** | *SSD7317 I²C Software Porting User Guide*, Rev 1.1, Aug 2019 — PDF pages **51–63** | `not-tested`, OCR (noticeably cleaner scan) |
| **[APP]** | Appendices I–IV — PDF pages **64–87**. ⚠ **Largely unreadable**; see §10 | `not-tested`, **OCR failed** |
| **[CF]** | Crystalfontz catalogue, probed live 2026-09-20 | `executed-success` |
| **[INF]** | Inference | `inferred` |

**Nothing here was verified on hardware, and nothing here should be trusted to the last digit without checking a rendered page image.** Where the OCR is ambiguous this record says so rather than guessing.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Solomon Systech Limited** | **[DS]** cover, footers |
| Part | **`SSD7317`** | **[DS]** cover; also **[CF]** catalogue |
| Document title, verbatim | **"128 x 96 Dot Matrix OLED/PLED Segment/Common Driver with Integrated Touch Controller"** | **[DS]** cover |
| Document status | **"Advance Information"** | **[DS]** cover |
| Revision / date | **Rev 1.3, Oct 2020** | **[DS]** cover, footers |
| Revision history | 1.0 Initial Release **31-Dec-18** · 1.1 feature list, FR formula §6.3, recommended V<sub>CC</sub> at LPM §7, DC table **11-Apr-19** · 1.2 pin description of `DCDCEN`/reserved pins, DC table, touch description §6.10–6.12, system flow **16-Oct-19** · **1.3 block diagram, pin description of `ATP[3:0]`/`RX[3:0]`/`RXT[3:0]`, application example — 08-Oct-20** | **[DS]** p. 2 |
| Ordering part | **`SSD7317Z`** — 128 SEG, 96 COM, **COG**. Min SEG pad pitch **29 µm**, COM **35 µm**, I/O **55 µm**; **die thickness 250 µm**; bump height nominal **9 µm** | **[DS]** §3, Table 3-1, p. 7 |
| Display geometry | **128 segments × 96 commons**, monochrome, **128 × 96-bit embedded SRAM (GDDRAM)** | **[DS]** §1–§2, pp. 6, 23 |
| Touch capability | **In-cell capacitive**, **4-key + 1-D slide** on a conventional panel structure; **out-cell up to 8 keys** | **[DS]** §1–§2, pp. 6–7 |
| MCU interfaces | Display: **8-bit 6800 parallel · 8-bit 8080 parallel · 4-wire SPI · 3-wire SPI · I²C**. Touch: **SPI or I²C**. Pin-selected by `BS[3:0]` | **[DS]** §5, Table 5-2, p. 9 |
| Operating temperature | **−40 to +85 °C** | **[DS]** §2 p. 7 and §8 Table 8-1 p. 28 (corroborated at two places — see §10) |
| ⚠ Marking verified? | **No.** No unit inspected | **[INF]** |

⚠ **Two SSD7317 revisions are published.** Crystalfontz's catalogue carries **id 469 = v0.11** and **id 498 = v1.3** **[CF]**. The v0.11 document was **not fetched in this pass** and is recorded as a known, unretrieved earlier revision — note that **0.11 does not appear in the Rev 1.3 revision history**, which starts at 1.0, so it is a pre-release rather than a superseded release.

---

## 2. Used By — nothing, and this one is a genuine mis-acquisition

**No device documented in this repository uses an SSD7317, and none plausibly could without it being obvious** — it is an OLED driver with an integrated touch controller, an entirely different product category from everything else in this vendor folder. No schematic, firmware image or driver source in this tree names it.

**It is here because it was fetched by mistake.** On 2026-09-11 a research pass working on e-paper controllers requested `https://www.crystalfontz.com/controllers/Solomon%20Systech/SSD1680/<id>/` and saved the response as `ssd1680.pdf`. Crystalfontz's `<Part>` path segment is decorative — **only the trailing numeric id selects a document** — so the wrong id returned this bundle. The file then sat in scratch for nine days under a name that guaranteed nobody would open it.

**That is the finding, and it is why this record exists rather than the file being quietly re-filed:**

- It proves the Crystalfontz decorative-path trap ([already recorded in `ai-crawler-site-access-table.md` §`crystalfontz.com`](../../../ai-crawler-site-access-table.md)) produces **silent** wrong-document delivery, not an error — HTTP 200, valid `%PDF` magic, plausible size. **Magic-byte validation does not catch it.**
- The document turned out to be **four documents**, including two software porting guides that are not otherwise indexed anywhere (§5). Had it been discarded as "wrong part", that would have been lost.
- The full retrieval pattern, with live-verified ids, is now in [`vendors/solomon-systech` §2–§3](../../../vendors/solomon-systech/README.md).

Nothing in this record should be read as suggesting this part is on any board here. **If you are looking for an e-paper controller, you want [SSD1677](../ssd1677/README.md), [SSD1680](../ssd1680/README.md), [SSD1681](../ssd1681/README.md) or [SSD1683](../ssd1683/README.md).**

---

## 3. What the part actually is

Two independent subsystems in one die, with **two separate MCU buses, two separate chip selects and two separate resets**:

| | Display side | Touch side |
|---|---|---|
| Chip select | `DCS#` | **`TCS#`** |
| Reset | `RES#` | **`TRES#`** |
| Data bus | `D[7:0]` | **`TD[2:0]`** |
| Interrupt | — | **`IRQ`** |
| Clock options | `CL` + `CLS` (internal/external) | `EXT32` external clock |
| Interface choices | 6800 / 8080 / 4-wire SPI / 3-wire SPI / I²C | **SPI or I²C only** |

**[DS]** §5, Tables 5-1 and 5-2, pp. 9–12.

### 3.1 `BS[3:0]` selects both interfaces at once

**[DS]** Table 5-2, p. 9. `0` = `VSS`, `1` = `VDD`:

| `BS[3:0]` | Display interface | Touch interface |
|---|---|---|
| `0000` | 4-line SPI | **SPI** |
| `0001` | 3-line SPI | SPI |
| `0010` | **I²C** | SPI |
| `0100` | 8-bit 6800 parallel | SPI |
| `0110` | 8-bit 8080 parallel | SPI |
| `1000` | 4-line SPI | **I²C** |
| `1001` | 3-line SPI | I²C |
| `1010` | **I²C** | I²C |
| `1100` | 8-bit 6800 parallel | I²C |
| `1110` | 8-bit 8080 parallel | I²C |

So **`BS3` picks the touch bus and `BS[2:0]` picks the display bus**, and the two are chosen together at power-up by strapping. `BS1` values `0011`, `0101`, `0111`, `1011`, `1101`, `1111` are not listed.

### 3.2 Pin reuse on the display bus

**[DS]** §5, p. 11. When a serial display interface is selected, the parallel data pins are reassigned:

| Display mode | Pin roles |
|---|---|
| **SPI** | **`D2` and `D1` tied together** = `SDIN`; **`D0`** = `SCLK` |
| **I²C** | **`D2` and `D1` tied together** = `SDA` (SDA<sub>OUT</sub>/SDA<sub>IN</sub>); **`D0`** = `SCL` |
| Either serial mode | **`R/W#(WR#)` and `E(RD#)` must be tied to `VSS`/`VLL`** |
| **3-wire SPI** | **`D/C#` must be tied to `VSS`/`VLL`** |

Touch bus **[DS]** p. 11:

| Touch mode | Pin roles |
|---|---|
| **SPI** | `TD2` = `SDOUT`, `TD1` = `SDIN`, `TD0` = `SCLK` — **full duplex, unlike the display side** |
| **I²C** | `TD2` and `TD1` tied together = `SDA`; `TD0` = `SCL` |

### 3.3 I²C addressing — two different address spaces

| Bus | Address | Selected by |
|---|---|---|
| **Display** | **`0111100`–`0111111`** (0x3C–0x3F) | **`E` pin acts as `SA1`, `D/C#` pin acts as `SA0`** **[DS]** §6.1.5, p. 9–10 and pp. 17–18 |
| **Touch** | **`0x53` (normal) + `0x57` (BIOS)**, or **`0x5B` + `0x5F`** | **touch init command `0x35` = `0x0A`** or **`= 0x0B`** **[I2C]** p. 4 |

⚠ **The touch side answers to *two* 7-bit addresses simultaneously** — a normal address and a separate **BIOS** address used during the boot/firmware-download phase (§5). An I²C scan of a live SSD7317 board should therefore show up to **three** addresses: one display, two touch.

⚠ **I²C requires a 200 µs packet delay** after every write and every read transaction **[I2C]** p. 4. This is not a bus-speed parameter; it is a mandatory inter-packet gap, and omitting it is the obvious first cause of an unreliable touch link.

### 3.4 Pins with hard requirements

**[DS]** §5, pp. 9–12:

| Pin | Requirement |
|---|---|
| `VCI` | **Must be ≥ `VDD`** — stated three times in the document |
| `VSL` | Segment output-low reference. **If external VSL is unused, tie to `VSSA`.** If used, resistor + diode to ground per application |
| `VLH` / `VLL` | Internal logic high/low rails. **No external connection needed** |
| `V33` / `V38` | Same level as `VCC` / `VCOMH`. **No external connection needed** |
| `VCOMH` | **Capacitor to `VSS` required** |
| `BGGND` | Reserved — **must be connected to ground** |
| `IREF` | Segment current reference. **External: resistor to `VSS` sized for ≈ 18.75 µA. Internal: keep NC** |
| `CLS` | **HIGH (to `VDD`) = internal clock.** LOW requires an external clock on `CL` |
| `CL` | When `CLS` is HIGH, **connect to `VSS`/`VLL`** |
| `EXT32` | External touch clock — **tie to `VSS`/`VLL` if unused** |
| **`DCDCENI`** | *"This pin is **recommended to tie `VDD`**."* When HIGH, `DCDCENO` becomes firmware/command controllable |
| `DCDCENO` | Enable output for the external DC-DC. **Keep NC if unused** |
| `TEST` | **Must be connected to `VSS`/`VLL`** |
| `FR` | RAM-write synchronisation output (tearing-effect avoidance). **Keep NC if unused** |
| **`ATP[3:0]`** | *"**must** be connected to external FPC to GND **separately**, OR reserve test pad on FPC"* — not optional, and not commoned |
| `RX[3:0]` / `RXT[3:0]` | **Out-cell** / **on-cell** touch sensing channels |
| `VBREF`, `T0`/`T1`, `DR[3:0]`, `SHA`–`SHN`, `TR[19:0]`, `NC` | Reserved — **keep NC** |
| `SEG0`–`SEG127` | **At `VSS` when display is off** |
| `COM0`–`COM95` | **High impedance when display is off** |

---

## 4. Display side

### 4.1 GDDRAM — ⚠ the datasheet says "eight pages" and means twelve

**[DS]** §6.7, p. 23, verbatim: *"The size of the RAM is 128 x 96 bits and the RAM is divided into **eight** pages, from PAGE0 to PAGE11…"*

**PAGE0 to PAGE11 is twelve pages**, and twelve is arithmetically required: 96 commons ÷ 8 rows per page = 12. The figure on the same page draws all twelve (`PAGE0 (COM0–COM7)` … `PAGE11 (COM88–COM95)`), and the row-remapped column draws twelve as well. **"Eight" is wrong**, and it is wrong in a way that betrays the document's lineage — eight pages is the SSD1306/SSD130x family's 64-row layout. §7-C2.

Addressing **[DS]** p. 23: writing one data byte fills a whole 8-row column of the current page; **`D0` is the top row, `D7` the bottom**. Segment and common outputs can each be **re-mapped in software**, and a display-start-line register (command **`D3h`**) shifts the RAM window vertically.

### 4.2 Display features

**[DS]** §2, pp. 6–7:

- **256-step contrast control**; segment current **600 µA typ at contrast `FFh`**, 412 µA at `AFh`, 150 µA at `3Fh` (`VDD` 1.8 V, `VCI` 3.3 V, `VCC` 12 V, `IREF` 18.75 µA) **[DS]** Table 9-1, p. 29
- **Segment max source current 600 µA; common max sink current 76.8 mA**
- Segment output-current uniformity **±3 %**; adjacent-pin uniformity **±2 %** **[DS]** Table 9-1
- **Continuous scrolling** horizontally and vertically, plus **infinite content scrolling** (screen-saving functions)
- **Programmable frame rate and multiplex ratio**; row and column re-mapping
- **Dynamic greyscale**
- **Power-on reset (POR)**, on-chip oscillator, internal or external `IREF`
- `FR` pin gives a **RAM-write synchronisation signal** to avoid tearing

> The command set in the bundle's Appendix III is recognisably the **SSD130x family command set** — `AFh`/`AEh` display on/off, `22h` set page address, `D3h` set display offset, `D5h` display clock divide / oscillator frequency, 256-step contrast. **[APP]**, heavily OCR-damaged, and **[DS]** §6.9. If you have written an SSD1306 driver, the display half of this part will be familiar. **`inferred` as to register-level compatibility** — the appendix is too damaged to assert it, and §7-C1 explains why you should not rely on this paragraph.

### 4.3 Power-on and power-off sequences — these are not optional

**[DS]** §6.9, Figures 6-17 and 6-18, p. 25.

**Power on:**

1. Power on **`VDD` and `VCI`** (`VCI` must be ≥ `VDD`).
2. After both are stable, **wait at least 20 ms (`t0`)**, then pull `RES#` **LOW for at least 3 µs (`t1`)**, then HIGH.
3. After `RES#` goes low, **wait at least 3 µs**, then power on **`VCC`**.
4. After `VCC` is stable, send **`AFh`** (display on). **`SEG`/`COM` become active after 40 ms (`tAF`).**

**Power off:**

1. Send **`AEh`** (display off).
2. Power off **`VCC`**.
3. Power off `VDD` and `VCI` after **`tOFF`** — **minimum 0 ms, typical 100 ms**.

Notes, verbatim **[DS]** p. 25:

- *"`VCC` should be kept **float** (i.e. disable) when it is OFF."*
- *"**Power Pins (`VDD`, `VCI`, `VCC`) can never be pulled to ground under any circumstance.**"*
- *"The register values are reset after `t1`."*
- *"`VDD`, `VCI` should not be Power OFF before `VCC` Power OFF."*

---

## 5. Touch side — ⚠ the firmware lives on the host

This is the single most consequential fact about the part, and it is the reason the bundle contains two porting guides.

### 5.1 There is a CPU, and it boots empty

**[DS]** §6.12, p. 26: *"SSD7317 has integrated with **16-bit CPU, 16 kB program and data memory**. It is able to process all the raw touch data, generate the gesture report and communicate with the MCU host."*

**[DS]** §2, p. 6: *"**16 kB firmware-based system operation by host**."*

**[SPI]** §3.3.1, p. 8 (bundle p. 45): *"SSD7317 has 16 K ram size which is divided into 3 blocks. PM is 12 K bytes, DM is 2 K bytes and PM is 2 K bytes."*

> ⚠ **That sentence names `PM` twice.** The three blocks referenced everywhere else in the same guide are **`PM`, `TM` and `DM`**, with distinct memory-select codes and distinct download steps, and 12 + 2 + 2 = 16 kB. The second **"PM"** is a typo for **`TM`**. The FW header file is stated to contain *"3 code blocks: PM_Content, TM_Content, DM_Content"*. **[SPI]** §3.3.2.

**There is no on-chip non-volatile store for the touch firmware.** Every power-up, the host must push ~16 kB into the part before touch works at all. A board using this chip therefore carries a vendor-supplied firmware blob and a bootloader in its own MCU, and **a firmware image you do not have is a hard blocker**, not an inconvenience.

### 5.2 Boot sequence

**[SPI]** §3.1, p. 7 (bundle p. 44):

1. Send the **display and touch initial code**; touch init command **`0x35` set to `0x10`** for SPI (**`0x0A`/`0x0B` for I²C — that byte *is* the I²C address selector**, §3.3).
2. Hold **touch hardware reset LOW for > 10 µs**.
3. From HW reset to the **BIOS Reset Interrupt**, expect **> 20 ms**.
4. **1st interrupt = BIOS Reset Interrupt** → IC initialise → **download FW** → **CPU Unstall** (enter CPU mode).
5. **2nd interrupt = Touch Initialise Interrupt** → issue Clear Interrupt.

### 5.3 Firmware download

**[SPI]** §3.3.3, p. 8. Memory is selected, then written in **512-byte bursts**:

| Block | Memory-select code |
|---|---|
| **PM** (12 kB) | **`0x01`** |
| **DM** (2 kB) | **`0x02`** |
| **TM** (2 kB) | **`0x03`** |

Each block: issue the select command, then repeated **`0x06` (data burst write)** transactions with an incrementing address and 512 bytes of payload, finishing with a short "remaining data" burst.

Then **CRC checksum** **[SPI]** §3.3.4, p. 9: clear CRC → trigger CRC → read Status-and-Length → **read the CRC value back**. The status register exposes **`CRC_BSY`** (bit 13) so the host can poll for completion.

Then **CPU Unstall** **[SPI]** §3.3.5, p. 10 — a four-command sequence; *"After IC receiving this command, **`IRQ` pin will be automatically cleared**."*

> ⚠ **There is a CRC over the downloaded firmware and a status bit for it. Use them.** A partially-written PM block produces a chip that answers on the bus and reports nothing sensible — exactly the failure that is hardest to diagnose from the host side.

### 5.4 SPI transaction format

**[SPI]** §1.1, p. 4:

- **CPOL 0, CPHA 0.**
- **All command, address and data are 16-bit wide.**
- **Byte order: LSB byte first, then MSB byte** — *"In most cases"*, with the guide's own asterisked caveat.
- **Bit order: MSB first, in all cases.**
- **Read/write operations differ between BIOS mode and CPU mode.**

Opcodes: **`0x02`** register write · **`0x03`** register read · **`0x06`** data burst write · **`0x07`** data burst read (with a dummy byte before the first read data).

> ⚠ **"LSB byte first, MSB bit first"** is an unusual mixed-endianness convention, it is qualified with *"in most cases"*, and the guide does not enumerate the exceptions. Treat byte order as something to verify against a known-good host implementation.

### 5.5 Status register and touch reporting

**[SPI]** §2.1, p. 5 — SPI control status register:

| Bit | Name | Meaning |
|---:|---|---|
| **15** | `INT_RST` | Set: interrupt caused by HW reset |
| **14** | `OSC_EN` | Set: oscillator enabled |
| **13** | `CRC_BSY` | Set: CRC busy |
| 12:1 | — | reserved |
| **0** | `SPIS_BUSY` | Set: SPI slave busy |

**Status and Length (`SnL`), 2 bytes, at address `0x0AF0`** **[SPI]** §2.2 / **[I2C]** §2.1 — identical on both buses:

- **LSB = length**, in bytes, of the upload data to read.
- **MSB = status**: flags `Boot`, `Aux`, `Gesture`, `Move`, `Up`, `Down`, `Exist`.

**Gesture upload data, 6 bytes, at address `0x0AF1`**:

| Byte | Content |
|---:|---|
| 0 | **Gesture** — fixed `0xF6` |
| 1 | **Gesture ACT** |
| 2 | **Gesture Detail** |
| 3 | Tap Down Key / Tap Up Key |
| 4 | Reserved |
| 5 | Reserved / **Slide Direction ID** |

Gesture encoding (`ACT`, `Detail`) **[I2C]** p. 5 — the cleaner of the two scans:

| Gesture | ACT | Detail | Action | Modes |
|---|---|---|---|---|
| Single Tap Key 1–4 | `0x01` | `0x01`–`0x04` | D-U | NM |
| **Single Tap AnyKey** | `0x01` | **`0x00`** | D-U | **NM, LPM** |
| Long Tap Key 1–4 | `0x02` | `0x01`–`0x04` | D-Delay-U | NM |
| **Long Tap AnyKey** | `0x02` | **`0x00`** | D-Delay-U | **NM, LPM** |
| Double Tap Key 1–4 | `0x03` | `0x01`–`0x04` | D-U-D-U | NM |
| **Double Tap AnyKey** | `0x03` | **`0x00`** | D-U-D-U | **NM, LPM** |
| **Slide LR** | `0x04` | `0x01` | D-Move-U; key numbers in `[6:4]` and `[2:0]` | NM |
| **Slide RL** | `0x04` | `0x02` | D-Move-U | NM |
| **Error** | **`0xFF`** | `0x00` | **Time out / Palm / etc.** | NM, LPM |

⚠ **Only the "AnyKey" variants are reported in low-power mode**, and **slides are not reported in LPM at all**. Per-key discrimination requires the display to be on.

### 5.6 Modes

**[DS]** §7, p. 27:

| Mode | Display | Touch scan rate | Notes |
|---|---|---|---|
| **Normal (NM)** | ON | **= frame rate, typ 105 Hz** | Segment drivers are **time-multiplexed** between display and touch sensing; touch is reported at the end of each touch slot **[DS]** §6.10 p. 26 |
| **Low power (LPM)** | OFF | **20 Hz, software programmable** (6 Hz also characterised) | Wake on single tap, double tap or long tap. ⚠ *"It is recommended to turn off the external DC-DC circuit for display panel driving during LPM. **In this case, `VCC` must be higher or equivalent to `VCI` − 0.6 V**"* |
| **Sleep** | OFF | OFF | *"It shall respond **only** to the Touch enable command during the sleep mode"* |

Transitions: `Display On`/`Display Off` commands move between NM and LPM; `Touch Enable`/`Touch Disable` move to and from Sleep. **A programmable timeout automatically drops NM → LPM.**

### 5.7 Touch performance claims

**[DS]** §2, pp. 6–7 — vendor claims, `not-tested`:

- **Water and moisture immunity:** *"No false touch with condensation or water drop up to **5 mm** diameter"*; *"One-finger tracking with condensation or water drop up to 5 mm diameter"*
- **Gloved operation** for 4-key touch *"with plastic materials up to **0.2 mm** thickness"*
- **Large object report flag** (palm rejection input)
- **Auto calibration**
- Works *"with all proprietary sensor patterns recommended by SSL for On-cell structure"*

---

## 6. Electrical

### 6.1 Absolute maximum ratings

**[DS]** §8, Table 8-1, p. 28. Referenced to `VSS`.

| Symbol | Parameter | Value | Unit |
|---|---|---|---|
| `VDD` | Supply voltage | **−0.3 to +4** | V |
| `VCI` | Supply voltage | **−0.3 to +4** | V |
| **`VCC`** | Supply voltage | **0 to 19** | V |
| `VSEG` | SEG output voltage | 0 to `VCC` | V |
| **`VCOM`** | COM output voltage | **0 to 0.9 × `VCC`** | V |
| `VIN` | Input voltage | `VSS` − 0.3 to `VDD` + 0.3 | V |
| **`TA`** | Operating temperature | **−40 to +85** | °C |
| `TSTG` | Storage temperature | −65 to +150 | °C |

*"This device may be light sensitive"*; *"This device is not radiation protected."*

### 6.2 DC characteristics

**[DS]** §9, Table 9-1, p. 29. Conditions: `VDD` 1.65–3.5 V, `VCI` 3.0–3.5 V (**`VCI` ≥ `VDD`**), `TA` 25 °C.

| Symbol | Parameter | Min | Typ | Max | Unit |
|---|---|---:|---:|---:|---|
| **`VCC`** | Operating voltage | **8** (NM) / **`VCI` − 0.6** (LPM) | | **18** | V |
| **`VDD`** | Logic supply | **1.65** | | **3.5** | V |
| **`VCI`** | Touch controller supply | **3.0** | | **3.5** | V |
| `VOH` / `VOL` | Logic output, `IOUT` = 100 µA @ 3.3 MHz | 0.9 × `VDD` | | 0.1 × `VDD` | V |
| `VIH` / `VIL` | Logic input | 0.8 × `VDD` | | 0.2 × `VDD` | V |
| `ICC,SLEEP` · `IDD,SLEEP` · `ICI,SLEEP` | **Sleep mode**, display off, no panel, no touch | | | **10 each** | µA |
| `IDD,LPM` | **LPM**, `VDD` 1.8 V, `VCI` 3.3 V, `VCC` 2.7 V, display off, touch running | | **25 @ 20 Hz** / **10 @ 6 Hz** | | µA |
| `ICI,LPM` | ″ | | **20 @ 20 Hz** / **5 @ 6 Hz** | | µA |
| `ICC,NM` | **Normal mode**, `VCC` 12 V, `IREF` 18.75 µA, no load, display all-ON, contrast `FFh` | | **680** | **750** | µA |
| `ICI,NM` | ″, with touch, normal mode | | **500** | **650** | µA |
| `IDD,NM` | ″, NM scan rate 105 Hz | | **800** | **1000** | µA |
| `ISEG` | Segment output current, contrast `FFh` / `AFh` / `3Fh` | | **600** / **412** / **150** | | µA |
| `ISEG Dev` | Segment uniformity at contrast `FFh` | −3 | | +3 | % |
| `Adj. Dev` | Adjacent-pin uniformity | −2 | | +2 | % |

Datasheet note: *"`ICI, NM` and `IDD, NM` may vary under different [firmware] version"* — the OCR mangles the qualifier, but the meaning is clear and it is a real caveat: **normal-mode current depends on the firmware blob you download**, not only on the silicon. **[DS]** p. 29, note ⟨1⟩.

> **Power budget shape.** Sleep is ~30 µA across three rails; LPM at 6 Hz is ~15 µA of `VDD`+`VCI` (plus whatever `VCC` costs, not tabulated for LPM); normal mode is ~2 mA total across the three rails **before** the panel. Dropping LPM from 20 Hz to 6 Hz roughly halves `VDD` and quarters `VCI` — a large, cheap lever.

### 6.3 AC

**[DS]** §10, Tables 10-1 to 10-6, pp. 30–35 — separate timing tables for **6800-series parallel**, **8080-series parallel**, **serial** and **I²C** interfaces. **Not transcribed**: these are dense numeric tables and the OCR layer is not reliable enough to reproduce them value-by-value (§10). **Read them from rendered page images if you need them.** Recorded as a deliberate gap rather than transcribed unsafely.

---

## 7. Caveats, errata and conflicts

| # | Issue | Evidence |
|---|---|---|
| **C1** | **⚠⚠ The retained PDF's text layer is OCR and is corrupted.** Subscripted rail names are systematically wrong (`VDD`→`Yoo`, `VCI`→`Ver`/`Va`, `VCC`→`Vee`, `VSSA`→`Vr.ss`), **`I²C` renders as `PC`, `re`, `12C` or `e`**, dates lose digits (`16-0ct-19`), and the part number itself appears as `S8D7317`, `SSD731 7` and `lss07317`. **Every value in this record was taken only where corroborated in two or more places.** Do not transcribe anything further from this file without checking a rendered page image | `executed-success` — direct observation across the extracted text |
| **C2** | **The datasheet says the GDDRAM is "divided into eight pages, from PAGE0 to PAGE11".** Twelve pages are required (96 ÷ 8) and twelve are drawn in the figure. **"Eight" is the SSD130x family's 64-row number**, left behind in a derived document | **[DS]** §6.7 p. 23 |
| **C3** | **The porting guides are at different revisions from the datasheet and from each other** — datasheet **Rev 1.3 (Oct 2020)**, SPI guide **Rev 1.0 (Apr 2019)**, I²C guide **Rev 1.1 (Aug 2019)**. The datasheet's own history records changes to the touch description at Rev 1.2 (Oct 2019) and to the system flow — **after the SPI guide was written.** Prefer the datasheet where they disagree, and expect the SPI guide to lag | **[DS]** p. 2; **[SPI]** p. 2; **[I2C]** p. 2 |
| **C4** | **`PM`/`TM`/`DM` block sizes are stated with `PM` named twice** — *"PM is 12 K bytes, DM is 2 K bytes and PM is 2 K bytes"*. The second is `TM`; 12 + 2 + 2 = 16 kB and three distinct select codes exist (`0x01`/`0x02`/`0x03`) | **[SPI]** §3.3.1 p. 8 |
| **C5** | **Touch firmware is volatile and host-supplied.** ~16 kB must be downloaded over SPI or I²C at **every** power-up before touch works. **No firmware image is held in this repository and none was located.** Without the vendor blob the touch half of this part is unusable | **[DS]** §2 p. 6, §6.12 p. 26; **[SPI]** §3.3 |
| **C6** | **SPI byte order is "LSB first, in most cases"** with the exceptions unenumerated, while bit order is MSB-first. Mixed endianness plus an unqualified "most cases" is a porting hazard | **[SPI]** §1.1 p. 4 |
| **C7** | **I²C needs a mandatory 200 µs inter-packet delay** on both read and write. Not a clock-rate parameter | **[I2C]** §1.2–1.3 p. 4 |
| **C8** | **The touch side occupies two I²C addresses** (normal + BIOS), selected by init command `0x35` = `0x0A` (0x53/0x57) or `0x0B` (0x5B/0x5F). A bus scan shows up to three addresses for one chip | **[I2C]** §1.1 p. 4 |
| **C9** | **Per-key gestures and slides are not reported in low-power mode** — only the "AnyKey" tap variants and the error code. Waking to identify *which* key was pressed requires the display on | **[I2C]** p. 5; **[SPI]** p. 6 |
| **C10** | **Normal-mode supply current is firmware-version dependent**, by the datasheet's own note. A measured figure is specific to a blob, not to the part | **[DS]** §9 p. 29 note ⟨1⟩ |
| **C11** | **⚠ Power sequencing is strict and asymmetric.** `VCI` ≥ `VDD` always · ≥ 20 ms after supplies before `RES#` · `RES#` low ≥ 3 µs · `VCC` only after `RES#` low · `AFh` only after `VCC` stable · 40 ms to `SEG`/`COM` · on shutdown `AEh` → `VCC` off → `VDD`/`VCI` off. **`VCC` must float when off, and no power pin may ever be pulled to ground** | **[DS]** §6.9 p. 25 |
| **C12** | **`ATP[3:0]` must be grounded separately through the FPC** (or brought to reserved test pads) — a positive requirement, not a "tie unused inputs" convention | **[DS]** §5 p. 12 |
| **C13** | **`DCDCENI` is "recommended to tie `VDD`"**, which is the setting that makes `DCDCENO` controllable. This pin's description changed at Rev 1.2 — a Rev 1.1 or earlier copy will describe it differently | **[DS]** §5 p. 11, p. 2 |
| **C14** | **Appendices I–IV are effectively unreadable in the text layer** — bump coordinates, die pad floor plan, the fundamental command table and command descriptions, and die-tray information. Long runs extract as `!"#$%&()**A+,`. **The command table in particular must be read from page images.** §10 | **[APP]**, direct observation |
| **C15** | **`BS[3:0]` enumerates 10 of 16 codes.** `0011`, `0101`, `0111`, `1011`, `1101`, `1111` are unlisted | **[DS]** Table 5-2 p. 9 |
| **C16** | **An earlier revision (v0.11) exists and was not fetched.** Crystalfontz carries it as id **469**. It predates the Rev 1.3 revision history (which starts at 1.0), so it is a pre-release | **[CF]** |
| **C17** | **"Advance Information", five years old.** Rev 1.3 (Oct 2020) is the newest located anywhere | **[DS]** cover; **[CF]** |

---

## 8. Libraries

**None located, and none audited.** No SSD7317 driver was found in this pass — no Arduino library, no Linux driver, no vendor SDK beyond the two porting guides in the bundle itself. Given §7-C5 (host-supplied volatile firmware), a usable driver needs the vendor's firmware blob as well as code, and **neither is held here**.

`not-tested`. This is recorded as a negative result with a date rather than left as a silent gap.

---

## 9. Related

- [**Vendor sourcing guide — Solomon Systech**](../../../vendors/solomon-systech/README.md) — ⚠ **§2 and §3**: why this file arrived named `ssd1680.pdf`, and the live-verified document ids
- [**SSD1677**](../ssd1677/README.md) · [**SSD1680**](../ssd1680/README.md) · [**SSD1681**](../ssd1681/README.md) · [**SSD1683**](../ssd1683/README.md) — the e-paper controllers this part was mistaken for. **Unrelated silicon**
- [`ai-crawler-site-access-table.md` §`crystalfontz.com`](../../../ai-crawler-site-access-table.md) — the decorative-path trap that produced the mis-fetch, recorded before this pass and confirmed by it
- [**Hynitron CST816D**](../../hynitron/cst816d/README.md) · [**Goodix GT911**](../../goodix/gt911/README.md) / [**GT9271**](../../goodix/gt9271/README.md) · [**FocalTech FT6336G**](../../focaltech/ft6336g/README.md) — the capacitive touch controllers this repository actually documents on hardware, all of them **discrete** parts rather than display-integrated
- [**Sitronix**](../../../vendors/sitronix/README.md) §3 — Solomon Systech named as a competitor in the small-panel driver market

---

## 10. Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/ssd7317-rev1.3-oct2020-plus-porting-guides-crystalfontz-mirror.pdf` | 11 181 786 | `6c82537617e3d70003045b4360265ca5e44e5d3c3586c62d88f20817f794d6d8` | **A four-document SSD7317 bundle**, 87 pages. PDF 1.6, A4. `Optimized: yes`, `Form: AcroForm`. **No `Title`, `Author`, `Creator` or `Producer` metadata at all** — consistent with a scan-and-recombine rather than a publisher export. **Every page carries the footer `Downloaded from www.crystalfontz.com/controllers`** (87/87, counted) |

### What is actually in the 87 pages

Established by extracting per-page footers across the whole file (`executed-success`):

| Bundle pages | Document | Printed pagination | Revision |
|---:|---|---|---|
| **1–37** | **SSD7317 datasheet** — "Advance Information", 128 × 96 OLED/PLED driver with integrated touch controller | `P n/37` | **Rev 1.3, Oct 2020** |
| **38–50** | **SSD7317 SPI Software Porting User Guide** | `P n/13` | **Rev 1.0, Apr 2019** |
| **51–63** | **SSD7317 I²C Software Porting User Guide** | `P n/13` | **Rev 1.1, Aug 2019** |
| **64–87** | **Appendices I–IV** — I: bump die pad coordinates · II: `SSD7317Z` die pad floor plan · III: fundamental command table and command descriptions · IV: `SSD7317Z` die tray information | `P n/24` | undated |

**This structure is the finding.** A reader who opens the file expecting a datasheet and stops at page 37 will miss the *only* documentation of the firmware-download protocol (§5) and the *only* copy of the display command table. Nothing in the filename, the metadata or the first page indicates that three further documents follow.

### ⚠ Text-layer validation — **FAILED**

`pdftotext -layout` succeeds and produces human-legible output, which is exactly the dangerous case the research method warns about. It is **not** a publisher text layer; it is OCR over a scan, and it is wrong in systematic ways:

| Correct | Extracts as |
|---|---|
| `VDD` | **`Yoo`** |
| `VCI` | **`Ver`**, **`Va`**, **`Vc,`** |
| `VCC` | **`Vee`**, **`Vcc`** |
| `VSSA` | **`Vr.ss`** |
| **`I²C`** | **`PC`**, **`re`**, **`12C`**, **`e`** |
| `SSD7317` | **`S8D7317`**, **`SSD731 7`**, **`lss07317`**, **`sso7317`**, **`ISS07317`** |
| `Solomon Systech` | **`Solomon Systach`**, **`Solomon Syst&ch`** |
| `16-Oct-19` | **`16-0ct-19`** |
| `notice` | **`ncxice`** |
| `P 28/37` | **`P 28/371`** |

**Appendices I–IV (pages 64–87) are worse than corrupted — they are largely non-recoverable.** Long runs extract as mojibake (`!!"#$%&()**A+,`, `!"#$%&"'$(*+%%$"#,$-(&`, `COM-Pa~e H-mode (A[3 :QJ=QQQ l b}`). **The fundamental command table is in that range.** Any register-level work on the display half requires reading rendered page images.

**Mitigation applied.** Only values corroborated at two or more independent places in the document were transcribed — for example, operating temperature `−40 to +85 °C` appears in both the §2 feature list and Table 8-1; `VDD 1.65–3.5 V` appears in both §2 and the §9 conditions block; `128 × 96` appears in the title, §1, §2 and §6.7. **Dense numeric tables that could not be corroborated were deliberately not transcribed** — see §6.3.

### Provenance — verified, and the misnaming explained

**Source URL, live-verified 2026-09-20 (`executed-success`):**
`https://www.crystalfontz.com/controllers/Solomon%20Systech/SSD7317/498/` → HTTP **200**, `application/pdf`, **11 181 786 bytes**, SHA-256 **`6c82537617e3d70003045b4360265ca5e44e5d3c3586c62d88f20817f794d6d8`** — **byte-identical to the retained file**. Reacquisition **`automatic`**.

Crystalfontz's catalogue entry, read from the embedded JSON at `https://www.crystalfontz.com/controllers/`:
`{"id":498,"name":"SSD7317","version":"1.3","summary":"Advance Information\r\n128 x 96 Dot Matrix\r\nOLED/PLED Segment/Common Driver\r\nwith Integrated Touch Controller"}` — and a second entry `{"id":469,"name":"SSD7317","version":"0.11", …}` for the unfetched earlier revision.

**The file arrived in this repository as `ssd1680.pdf`.** Because Crystalfontz's `<Vendor>` and `<Part>` path segments are decorative and only the trailing id selects a document, a request naming `SSD1680` with the wrong id returns this instead — with a 200, a valid `%PDF` header and a plausible size. §2. The full pattern and the correct ids are in [`vendors/solomon-systech` §3](../../../vendors/solomon-systech/README.md).

**Licence.** Third-party (Solomon Systech) copyright. The datasheet's back page carries the standard *"Solomon Systech reserves the right to make changes without notice…"* disclaimer. **No per-page confidentiality footer**; the only per-page stamp is Crystalfontz's *"Downloaded from www.crystalfontz.com/controllers"*, which is a **mirror watermark added by the distributor**, not a restriction by the rights-holder. No redistribution terms stated. Redistribution status **`unknown`**; disposition **`repository`**.

---

## 11. Authoritative sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | SSD7317 — 128 × 96 Dot Matrix OLED/PLED Segment/Common Driver with Integrated Touch Controller | **Solomon Systech Limited**, mirrored by **Crystalfontz America** | credible mirror | datasheet (bundle pp. 1–37) | `artifacts/ssd7317-rev1.3-oct2020-plus-porting-guides-crystalfontz-mirror.pdf`; upstream `https://www.crystalfontz.com/controllers/Solomon%20Systech/SSD7317/498/` | 2026-09-11 (acquired), **2026-09-20** (URL verified, hash matched) | **Rev 1.3, Oct 2020 — "Advance Information"** | §1, §3–§4, §6 |
| S-2 | SSD7317 SPI Software Porting User Guide | Solomon Systech, same bundle | credible mirror | porting guide (bundle pp. 38–50) | same file | 2026-09-20 | **Rev 1.0, Apr 2019** | §5 — boot, FW download, CRC, CPU unstall, SPI framing |
| S-3 | SSD7317 I²C Software Porting User Guide | Solomon Systech, same bundle | credible mirror | porting guide (bundle pp. 51–63) | same file | 2026-09-20 | **Rev 1.1, Aug 2019** | §3.3, §5.5 — I²C addressing, packet delay, gesture table |
| S-4 | SSD7317 Appendices I–IV | Solomon Systech, same bundle | credible mirror | appendix (bundle pp. 64–87) | same file | 2026-09-20 | undated | §4.2 (command family), §7-C14 — ⚠ **text layer non-recoverable** |
| S-5 | Crystalfontz controller catalogue | Crystalfontz America | credible mirror | catalogue (embedded JSON) | `https://www.crystalfontz.com/controllers/` | **2026-09-20** | undated | That ids **498** (v1.3) and **469** (v0.11) are both SSD7317; the decorative-path trap |
| S-6 | `ai-crawler-site-access-table.md` — `crystalfontz.com` | this repository | — | retrieval note | [`../../../ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md) | 2026-09-20 | pass of 2026-09-11 | §2, §10 — the trap, recorded before this pass and confirmed by it |
