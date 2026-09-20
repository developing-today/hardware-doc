# Solomon Systech SSD1677

- **Category:** active-matrix EPD (e-paper) display driver **with controller** — source/gate drivers, on-chip booster and regulators, oscillator, dual display RAM, programmable waveform engine, OTP waveform store, temperature sensing, SPI MCU interface
- **Package:** **gold-bump die only** (COG). There is no packaged part; you buy this on waffle pack and it gets bonded to a panel.
- **Document status:** **"Advance Information", Rev 1.0, November 2018** — the first and, as far as this pass established, only public revision.
- **Research status:** the **full datasheet is retained** in `artifacts/` and has a valid text layer, cross-checked against rendered headings. Board-side behaviour is unusually well evidenced because M5Stack ships two independent drivers for the same panel and they disagree with each other in instructive ways.
- **Retrieved:** 2026-09-01

The controller bonded into the [DKE DEPG0397BBS770F3](../../dke/depg0397bbs770f3/README.md) panel on the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) and its Lite sibling.

---

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[DS]** | Stated in `artifacts/ssd1677-rev1.0-nov2018-m5stack-mirror.pdf`, cited by the document's own section or page number | `not-tested` — vendor claim reproduced; nothing measured |
| **[MAN]** | DKE module manual, read from rendered page images — held at [`../../dke/depg0397bbs770f3/artifacts/`](../../dke/depg0397bbs770f3/README.md) | `executed-success` for the transcription; `not-tested` for the values |
| **[SRC]** | Read out of M5Stack source at a cited `file:line` | `executed-success` for the read; `not-tested` on hardware |
| **[SCH]** | `PaperMono_SCH_V0.6.2_20260522.pdf`, sheet + designator + pin | `executed-success` for the extraction |
| **[DOC]** | `docs.m5stack.com`, retrieved 2026-09-01 | `not-tested` |
| **[INF]** | Inference | `inferred` |

**Nothing in this record was verified on hardware.** No command, parameter or timing figure was guessed.

---

## 1. Identity, and what the cover says plainly

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Solomon Systech Limited** | **[DS]** cover, footer of every page |
| Part | **`SSD1677`** | **[DS]** cover |
| Document title, verbatim | **"960 Source x 680 Gate Red/Black/White — Active Matrix EPD Display Driver with Controller"** | **[DS]** cover |
| Document status, verbatim | **"Advance Information"** — "This document contains information on a new product. Specifications and information herein are subject to change without notice." | **[DS]** cover |
| Revision / date | **Rev 1.0, Nov 2018** | **[DS]** cover and every page footer |
| Ordering parts | **`SSD1677Z`** (gold bump die, **bump face up**) and **`SSD1677Z8`** (gold bump die, **bump face down**). Both: waffle pack, die thickness **300 µm**, bump height **12 µm** | **[DS]** §3, Table 3-1 |
| Maximum geometry | **960 source outputs · 680 gate outputs · 1 VCOM · 1 VBD** ⇒ max resolution **960 × 680** | **[DS]** §1, §5 Table 5-5 (`S[959:0]`, `G[679:0]`) |
| Colour capability | **Red / Black / White** — two full-size RAM planes, `Mono B/W: 960×680 bits` and `Mono Red: 960×680 bits` | **[DS]** §1, §2 |
| MCU interface | **SPI only** — 4-wire (8-bit) or 3-wire (9-bit), selected by the `BS1` pin | **[DS]** §2, §6.1 |
| ⚠ Marking verified? | **Not applicable / no.** The die is chip-on-glass inside a bonded module. Identification rests on the DKE mechanical drawing naming `DRIVER IC: SSD1677` **[MAN]** p. 6, corroborated by M5Stack listing "SSD1677 Display Driver" in its datasheet set **[DOC]** | **[INF]** |

### 1.1 Say it plainly: the part is bigger and more capable than this panel uses

The title is not a description of the fitted display. Three of its claims do not apply here:

| Datasheet capability | What the PaperMono panel actually uses | Evidence |
|---|---|---|
| **680 gate outputs** (POR default `0x01` `A[9:0] = 0x2A7` ⇒ **680 MUX**) | **480 gate lines** — the driver writes `0x01` `{0xDF, 0x01, 0x02}` ⇒ `A[9:0] = 0x1DF = 479` ⇒ `479 + 1` = **480 MUX**, and `B[2:0] = 010` ⇒ `SM = 1`, interlaced gate scan | **[DS]** §7 (`0x01`), §8.1; **[SRC]** `EDP_OTP_LUT_demo.cpp:222`, `:337`; identical in DKE's own reference program **[MAN]** p. 24 |
| **960 source outputs** | **800 source columns** — `0x44` `{00, 00, 1F, 03}` ⇒ `XSA = 0x000`, `XEA = 0x31F = 799` | **[DS]** §8.3; **[MAN]** p. 24 |
| **Red / Black / White** | **Monochrome.** The second RAM plane (`0x26`, nominally "RED") is repurposed as the **second bit-plane of a four-level greyscale** encoding: `white = 00, light = 10, dark = 01, black = 11` across (`0x24`, `0x26`) | **[DS]** §7 (`0x24`, `0x26`); **[SRC]** `EDP_OTP_LUT_demo.cpp:139-140` |

So: **160 source channels and 200 gate channels are simply unused**, and the "Red" hardware is doing greyscale duty. None of this is unusual — a controller of this class is sold to fit a range of panels — but it means the datasheet's headline numbers must not be quoted as properties of the PaperMono display.

> ⚠ **Related conflict, recorded in the panel record.** DKE's mechanical drawing states `RESOLUTION: 800gate X 480source`, which is the reverse and is provably wrong: 800 gate lines would exceed this controller's 680 gate outputs. See [DEPG0397BBS770F3 §8-C3](../../dke/depg0397bbs770f3/README.md#c3--the-mechanical-drawing-has-gate-and-source-swapped).

---

## 2. Capabilities

**[DS]** §1–§2 unless noted.

| Area | Capability |
|---|---|
| Display RAM | **Two on-chip planes**, `960 × 680` bits each — B/W and "Red". The host does not need a framebuffer to hold the panel image |
| Drive voltages, on-chip | Booster + regulators generate `VGH`, `VGL`, `VSH1`, `VSH2`, `VSL` and `VCOM`; all five driving rails **can alternatively be supplied externally** |
| Gate output | **2 levels** (`VGH`, `VGL`), **max 40 Vp-p**; `VGH` 15–20 V, `VGL` = −`VGH`; **500 mV** adjustment step |
| Source / VBD output | **4 levels** (`VSH1`, `VSS`, `VSL`, `VSH2`). `VSH1` 9–17 V (200 mV step); `VSH2` 2.4–17 V (100 mV step to 8.8 V, then 200 mV); `VSL` −9 to −17 V (500 mV step) |
| VCOM | `DCVCOM` **−4 V to −0.1 V in 100 mV steps**; `ACVCOM` 3 levels: `VSH1+DCVCOM`, `DCVCOM`, `VSL+DCVCOM`. **Built-in VCOM sensing** (`0x28`/`0x29`), sensed value programmable into OTP (`0x2A`) |
| Waveform engine | **40 phases** (4 phases/group × 10 groups with repeat), repeat count **1–256**, **max 255 frames per phase** |
| OTP store | **34 waveform settings (WS)** including LUT, gate/source voltage and frame rate; **34 temperature ranges (TR)**; VCOM value; waveform version; module ID / user ID; plus embedded OTP for the initial code setting |
| OTP programming | External **or internal** generated voltage; **read-back and built-in CRC** for WS and TR (`0x34`, `0x35`) |
| Temperature | **Internal sensor, −25 to +50 °C, ±2 °C, 9-bit**; or **I²C single-master interface to an external sensor** |
| Diagnostics | Low-voltage (VCI) detect; **high-voltage ready detect with looping**; **panel break diagnostic**; status read (`0x2F`) |
| Display features | **Partial update**; black/white mono **dithering** (`0x25`); **auto write RAM for regular pattern** (`0x46`, `0x47`) |
| MCU interface | **SPI serial peripheral, maximum 20 MHz for write** |
| Power | Low current in operation and sleep; **deep sleep 1 µA typ** |
| Package | **COG (gold bump die)** |

---

## 3. MCU interface

### 3.1 4-wire vs 3-wire, and how the choice is made

**[DS]** §6.1.1, Table 6-1. The interface is **pin-selected by `BS1`**, not by a command:

| MCU interface | `BS1` | Pins used |
|---|---|---|
| **4-wire SPI** | **L** (to `VSS`) | `RES#`, `CS#`, **`D/C#`**, `SCL`, `SDA` |
| 3-wire SPI (9-bit) | H (to `VDDIO`) | `RES#`, `CS#`, `D/C#` **tied LOW**, `SCL`, `SDA` |

`SDI` and `SDO` are bonded together as the single bidirectional `SDA` pad **[DS]** Table 6-1 note 2.

**4-wire (8-bit)** **[DS]** §6.1.2, Table 6-2:

| Function | `SCL` | `SDI` | `D/C#` | `CS#` |
|---|---|---|---|---|
| Write command | ↑ | command bit | **L** | L |
| Write data | ↑ | data bit | **H** | L |

`SDI` shifts into an 8-bit register on every **rising** edge, MSB first (D7 → D0). **`D/C#` must be held for the whole byte.** On read, `SDO` shifts out on every **falling** edge; the first byte after `CS#` goes low is always a command (`D/C#` low), then `D/C#` goes high for the data byte(s).

**3-wire (9-bit)** **[DS]** §6.1.3, Table 6-3: identical, except a **9-bit** frame is shifted, the first bit being `D/C#` itself — `0` ⇒ the byte is a command, `1` ⇒ data. `D/C#` the pin must be tied LOW.

**The PaperMono panel uses 4-wire.** The FPC's `BS` pin (pin 8) is pulled low on the module **[MAN]** p. 7–8; both M5Stack drivers configure a `dc` pin **[SRC]** `EDP_SPI.cpp:29`, `M5GFX.cpp:2109`.

### 3.2 Timing — and the 2× overclock in M5GFX

**[DS]** §12.1, Table 12-1. Conditions `VDDIO − VSS = 2.2–3.7 V`, `TOPR = 25 °C`, `CL = 30 pF`.

| Symbol | Parameter | Min | Max | Unit |
|---|---|---:|---:|---|
| **`fSCL`** | **SCL frequency, write mode** | | **20** | **MHz** |
| `tCSSU` | `CS#` low before the first rising `SCLK` | 20 | | ns |
| `tCSHLD` | `CS#` low after the last falling `SCLK` | 20 | | ns |
| `tCSHIGH` | `CS#` high between transfers | 100 | | ns |
| `tSCLCYC` | SCL cycle time | 50 | | ns |
| `tSCLHIGH` | SCL high time | 25 | | ns |

The DKE module manual restates the identical table and adds the read-mode figures: **`fSCL` read mode max 2.5 MHz** **[MAN]** p. 16 — an **8× asymmetry** between write and read that is easy to miss.

> ⚠ **M5GFX drives this controller at 40 MHz** (`freq_write = 40000000` **[SRC]** `M5GFX/src/M5GFX.cpp:2114`), **double the maximum stated identically by both the silicon vendor and the module vendor**. M5Stack's own recommended OTP demo uses **20 MHz** — exactly at spec **[SRC]** `EDP_SPI.cpp:33`.
>
> This is a driver operating outside a specification, not a documentation ambiguity. Whether it misbehaves is `not-tested` here. It is a concrete, checkable mechanism behind M5Stack's warning that the M5GFX waveforms are "currently unstable" **[DOC]**, and it is the cheapest thing to change first when debugging refresh artefacts.

### 3.3 Signal pins

**[DS]** §5. Only the host-facing pins are listed; the panel-facing `S[959:0]`, `G[679:0]`, `VBD` and `VCOM` outputs, the analogue regulation pins and the reserved/test pads are in the datasheet's own tables.

| Pin | Type | Role |
|---|---|---|
| `BS1` | I | Interface select (§3.1) |
| `RES#` | I | Hardware reset, **active low**. Required to exit deep sleep |
| `CS#` | I | Chip select, active low |
| `D/C#` | I | Data / command |
| `SCL` | I | Serial clock |
| `SDA` | I/O | Serial data (`SDI` + `SDO` bonded) |
| `BUSY` | O | **High while busy** |
| `GDR` | O | Gate driver for the external boost NMOS |
| `RESE` | I | Current-sense input for the boost control loop |
| `VPP` | P | **OTP programming supply** — 7.25 / 7.5 / 7.75 V (min/typ/max) |
| `VCI` / `VDDIO` / `VDD` | P | Logic supply / interface logic supply / core (1.8 V, regulated from `VCI`) |
| `DP[0:33]` | I | **Reserved — connect to `VSS`** |
| `TP1`–`TP9`, `TIN`, `TPE`, `RSV` | — | **Reserved for testing — keep open, and do not connect to each other** |

The external boost network `GDR`/`RESE` requires is specified concretely by the module vendor rather than here — see [DEPG0397BBS770F3 §7.4](../../dke/depg0397bbs770f3/README.md) for the actual FET, diodes, inductor and the **2.2 Ω** sense resistor.

---

## 4. Waveforms: OTP versus external LUT

This distinction is the single most important thing in this record. It determines both image quality and whether you can destroy the panel.

### 4.1 What a waveform is here

A waveform lookup table is **112 bytes** **[DS]** §6.7:

| Bytes | Content | Set by |
|---|---|---|
| 0–104 | `VS[n-XY]`, `TP[n#]`, `RP[n]`, frame rate | **`0x32`** (Write LUT register, **105 bytes**) |
| 105 | Gate level | `0x03` |
| 106–108 | Source level | `0x04` |
| 109 | VCOM level | `0x2C` |
| 110–111 | Reserved | — |

"The waveform LUT of a particular temperature range **can be loaded from OTP or written by MCU**" **[DS]** §6.7. Those are the two paths.

### 4.2 The OTP path

**[DS]** §6.10. The embedded OTP holds **34 waveform settings (WS0–WS33)** at 112 bytes each — addresses 0–3807 — followed by **34 temperature ranges (TR0–TR33)** at 3808–3909, plus VCOM, display-mode selection, waveform version and user ID.

Selection is automatic **[DS]** §6.9:

1. Read the temperature as a 12-bit binary value (internal sensor via `0x18` = `0x80`, or external via I²C).
2. Search `TR0` → `TR33` **in sequence**, applying `lower bound < sensed temperature ≤ upper bound`.
3. **The last match wins** — the datasheet's own worked example makes this explicit: 34 °C matches both `TR6` (30–35 °C) and `TR7` (33–127.9 °C), and `WS7` is selected.
4. The matching WS is loaded into the LUT registers.

> ⚠ **Precaution, verbatim [DS] §6.9:** "Please ensure the temperature range covers whole range of application temperatures, **display will not be updated if no suitable temperature range matches the sensed temperature**."
>
> This is a silent-failure mode: out of range, the panel simply does not refresh. Combined with the DKE module's **0 to +50 °C** operating rating and the fact that **DKE does not publish which of the 34 slots it programmed**, cold-weather behaviour of this panel is undefined in a specific way. Command **`0x2D`** reads back VCOM information, display mode and a 4-byte **waveform version** from OTP, which is the only in-system way to learn anything about what is actually programmed **[DS]** §7.

Temperature range format **[DS]** §6.10.1: three bytes per TR — `temp_L[7:0]`, then `temp_H[3:0]` : `temp_L[11:8]`, then `temp_H[11:4]`.

### 4.3 The external-LUT path

Upload 105 bytes with `0x32`, plus `0x03` / `0x04` / `0x2C` for the gate, source and VCOM levels. This is what M5GFX does, with `lut_quality`, `lut_text`, `lut_fast` and friends held in flash **[SRC]** `M5GFX/src/lgfx/v1/panel/Panel_SSD1677.cpp`.

### 4.4 ⚠ The DC-balance hazard

M5Stack documents this explicitly **[DOC]**:

> "pay attention to **DC balance**; otherwise, **irreversible damage may be caused to the panel**."

Electrophoretic ink requires that the net charge delivered over a waveform sums to zero. A hand-tuned LUT that fails to balance will, over many refreshes, degrade the ink irreversibly — not a glitch, a destroyed display. **The OTP path cannot get this wrong**, because the balance was the panel manufacturer's responsibility when it burned the waveform. The external-LUT path moves that responsibility to whoever wrote the table.

DKE reinforces the same point from the other side: its electrical characteristics "are only guaranteed under the **controller & waveform provided by DKE**" **[MAN]** p. 10 note 3.

### 4.5 Which path M5Stack actually recommends, and why

M5Stack's own documentation **[DOC]**:

> "The e-paper driver waveforms for PaperMono in the M5GFX library are **currently unstable**. It is recommended to prioritize the e-paper manufacturer's **OTP example** below for refresh configuration to achieve better panel life and refresh stability."

The mechanism is visible in the code:

| | M5GFX `Panel_SSD1677` | `M5PaperMono-OTP-Demo` |
|---|---|---|
| Waveform source | **Custom LUTs uploaded from flash** (110 bytes each) | **Controller OTP** — `0x32` is **never issued** |
| DC-balance owner | M5Stack's hand-tuned tables | DKE's factory waveform |
| SPI clock | **40 MHz** (2× spec, §3.2) | **20 MHz** (at spec) |
| Code size | Full panel driver in M5GFX | Two files, ~600 lines total |

Corroboration that the warning is live rather than boilerplate, `executed-success` (branch diff): between M5GFX `master` and `develop`, `Panel_SSD1677.cpp` changed by 114 lines. **`lut_quality` was wholly replaced and the superseded version left commented out in-tree** (17 dead lines); the frame-rate row changed from `0x22 × 5` to `0xFF × 5` and all four greyscale rows differ. **`lut_text` was replaced too**, its comment rewritten from "Text: 64-frame absolute four-gray waveform for Mode 1" to "GC1 binary full-refresh waveform used by epd_text", and a new `Panel_SSD1677_4Gray::_refresh_mode1_text()` path added at `develop:src/lgfx/v1/panel/Panel_SSD1677.cpp:910-940`. A vendor actively swapping waveform tables between branches while keeping the old set commented out is consistent with an unresolved problem. `inferred` as to intent; the diff itself is `executed-success`.

Compounding it: the **shipped factory firmware pins an older M5GFX commit than either branch head** (`02107b828acb3eb782fccd747863638d64c876d7` vs `develop` head `8d6e8b3e…`) **[SRC]** `M5PaperMono-UserDemo/repos.json`. So the factory device runs a **third** waveform set, and M5Stack's published refresh timings correspond to none of the three checked-out versions.

---

## 5. Command set

The full table is **[DS]** §7 (pp. 22–35) with per-command detail in §8. What follows is the subset the vendor's OTP demo actually issues, decoded against that table, with `file:line`. Every call site in the demo was enumerated — **24 in total, all accounted for** — and **none of them is `0x32`**, confirming no LUT is ever uploaded on this path.

### 5.1 Initialisation

| Cmd | Params written | Meaning **[DS]** | Source |
|---|---|---|---|
| `0x12` | — | **SWRESET.** Resets commands/parameters to their S/W-reset defaults **except `R10h` deep sleep**; **RAM is unaffected**; `BUSY` high during the operation | `EDP_OTP_LUT_demo.cpp:206` |
| `0x18` | `{0x80}` | **Temperature Sensor Control** — `0x80` = **internal** sensor (`0x48` [POR] = external) | `:220`, `:356` |
| `0x0C` | `{0xAE,0xC7,0xC3,0xC0,0x80}` | **Booster Soft-start Control.** The datasheet tabulates exactly two legal 5-byte values: **Level 1** `AE C7 C3 C0 40` and **Level 2** `AE C7 C3 C0 80`. This is **Level 2** — the stronger inrush setting | `:221`, `:336`; byte-identical in DKE's reference **[MAN]** p. 24 |
| `0x01` | `{0xDF,0x01,0x02}` | **Driver Output control.** `A[9:0] = 0x1DF = 479` ⇒ **480 MUX gate lines**; `B[2] GD = 0`, `B[1] SM = 1` ⇒ interlaced scan `G0,G2,G4…G678,G1,G3…`, `B[0] TB = 0` ⇒ scan `G0→G679` | `:222`, `:337` |
| `0x3C` | `{0x01}` | **Border Waveform Control.** `A[7:6] = 00` ⇒ VBD follows a **GS transition**; `A[1:0] = 01` ⇒ **LUT1**. (POR is `0xC0` = HiZ) | `:223`, `:355` |
| `0x21` | `{0x00}` | **Display Update Control 1** — `A[7:4] = 0000` Red RAM normal, `A[3:0] = 0000` BW RAM normal | `:224`, and again before mono refresh at `:319` |
| `0x1A` | `{0x5A}` | **Write to temperature register** — forces the value **90** so the OTP LUT search (§4.2) selects a specific waveform bank instead of the sensed one. **Four-grey path only** | `:357` |

### 5.2 Window and cursor

| Cmd | Meaning **[DS]** | Source |
|---|---|---|
| `0x11` | **Data Entry mode.** `A[1:0]` = increment/decrement per axis, `A[2] = AM` = which axis the counter advances. Demo uses **`0x03`** (Y inc, X inc) for mono and **`0x02`** (Y inc, X dec) for four-grey | `:162` (mono), `:340` (four-grey) |
| `0x44` | **Set RAM X start/end.** `A[9:0] = XSA`, `B[9:0] = XEA`; POR `XEA = 0x3BF = 959` | `:164` |
| `0x45` | **Set RAM Y start/end.** POR `YEA = 0x2A7 = 679` | `:168` |
| `0x4E` / `0x4F` | **Set RAM X / Y address counter** | `:172`, `:175` |

The POR end-addresses (`0x3BF`, `0x2A7`) are themselves the clearest statement of the controller's native geometry: **960 × 680, addressed in pixels, not bytes**.

### 5.3 RAM writes

| Cmd | Meaning **[DS]** |
|---|---|
| `0x24` | **Write RAM (Black/White).** **White pixel ⇒ 1, black pixel ⇒ 0.** Address pointers auto-advance until another command is written |
| `0x26` | **Write RAM (RED).** RED ⇒ 1, white/black ⇒ 0. **Used here as the second greyscale bit-plane** (§1.1) |
| `0x25` | Write RAM (Dithering) — routes data into the dithering engine. **Not used by either M5Stack driver** |
| `0x46` / `0x47` | **Auto write RAM for regular pattern.** The datasheet's own operation flow (§9.1) opens with "Clear and fill two RAM by Command 0x46, Data 0xF7 … and Command 0x47, Data 0xF7". **Neither M5Stack nor DKE's reference program does this** — see §7-C3 |

### 5.4 Refresh

`0x22` (Display Update Control 2) selects the sequence; `0x20` (Master Activation) runs it. **[DS]** §7: "The Display Update Sequence Option is located at `R22h`. `BUSY` pad will output high during operation. **User should not interrupt this operation to avoid corruption of panel images.**"

| Mode | `0x22` | Then | Source |
|---|---|---|---|
| Partial refresh | **`0xF8`** | `0x20` | `:264-266` |
| Partial, follow-up | **`0x14`** | `0x20` | `:276-279` |
| Monochrome full refresh | **`0xFF`** | `0x20`, preceded by `0x21 = 0x00` | `:319-321` |
| Four-grey full refresh | **`0xD7`** | `0x20`, after `0x24` and `0x26` RAM writes | `:370-375` |

Partial refresh additionally **floats the border** first — `0x3C = 0x80` with the vendor comment "Float the border during partial refresh" `:251` — versus `0x01` for full refreshes.

The datasheet enumerates twelve `0x22` values **[DS]** §7: `80` (enable clock), `01` (disable clock), `C0`/`03` (enable/disable analog), `91`/`99` (load LUT with display mode 1/2), `B1`/`B9` (load temperature from I²C then LUT, mode 1/2), `C7`/`CF` (display with mode 1/2, then power down), `F7`/`FF` (load temperature ×2 then display, mode 1/2). **Of M5Stack's four values only `FF` appears.** See §7-C4.

### 5.5 Deep sleep

| Cmd | Params | Meaning **[DS]** §7 |
|---|---|---|
| `0x10` | `A[1:0]`: **`00` normal [POR]**, **`11` enter deep sleep** | "After this command initiated, the chip will enter Deep Sleep Mode, **BUSY pad will keep output high**. Remark: **To exit Deep Sleep mode, user required to send HWRESET to the driver.**" |

Deep sleep is the intended resting state: **1 µA typ / 5 µA max** at `VCI`, with DC/DC off, no clock, no MCU access and — importantly — **RAM contents not retained** **[DS]** §11. `SWRESET` (`0x12`) explicitly does **not** reset `R10h`, so you cannot software-reset your way out of it **[DS]** §7.

The vendor demo enters deep sleep **after every refresh** with `{0x01}` — `EDP_OTP_LUT_demo.cpp:236`. Note `0x01` is not one of the two documented values; §7-C5.

### 5.6 Status and diagnostics that neither driver uses

**[DS]** §7. Recorded because they are exactly the registers a robust driver should read and both vendor paths ignore:

| Cmd | What it gives you |
|---|---|
| `0x2F` | **Status Bit Read** — `[5]` HV-ready flag, `[4]` VCI-detection flag, `[2]` busy flag, `[1:0]` chip ID [POR `01`]. `[5]`/`[4]` are invalid after reset until `0x14`/`0x15` are issued **[MAN]** p. 19 |
| `0x14` | **HV Ready Detection** — requires `CLKEN=1` and `ANALOGEN=1`; result read via `0x2F` |
| `0x2D` | **OTP Register Read** — VCOM information, display mode, **4-byte waveform version**. The only way to identify the programmed waveform in-system |
| `0x2E` | **User ID Read** — 10 bytes from OTP |
| `0x34` / `0x35` | **CRC calculation / CRC status read** over the OTP waveform data |
| `0x28` / `0x29` | **VCOM Sense** and sense duration (`setting + 1` seconds, POR `09h` ⇒ 10 s) |
| `0x31` | **Load WS OTP** — explicit OTP load, as opposed to loading via `0x22` |

Neither M5GFX nor the OTP demo issues any of `0x2F`, `0x14`, `0x2D`, `0x2E`, `0x34` or `0x35`. Both poll the `BUSY` pin instead of the status register, which works but discards the VCI and HV-ready flags entirely. `executed-success` — the demo's full command call-list was extracted; `inferred` as to consequence.

---

## 6. Reference operation flow

**[DS]** §9.1, Figure 9-1, transcribed:

```
START
 1. Power On            — supply VCI; wait 10 ms
 2. Set Initial Configuration
                        — define SPI interface; HW reset; SW reset (0x12); wait 10 ms
 3. Send Initialization Code
                        — clear and fill both RAMs: 0x46 data 0xF7 (RAM 0x24), 0x47 data 0xF7 (RAM 0x26)
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

Two deviations in both real implementations:

- **Step 3's RAM pre-clear (`0x46`/`0x47`) is skipped** by DKE's reference program and by M5Stack. §7-C3.
- **Soft-start (`0x0C`) is issued in step 3, not step 5**, by both. Harmless reordering — the value is latched, not triggered. `inferred`.

---

## 7. Caveats, errata and conflicts

| # | Issue | Evidence |
|---|---|---|
| **C1** | **⚠ The document is "Advance Information" and eight years old.** Solomon Systech's own cover disclaims it: "information on a new product. Specifications and information herein are **subject to change without notice**." No later revision was located in this pass. Every figure here should be treated as provisional silicon documentation, not a finalised datasheet | **[DS]** cover |
| **C2** | **⚠ M5GFX exceeds the documented SPI write clock by 2×.** 40 MHz against a 20 MHz maximum stated identically by Solomon Systech and DKE. §3.2 | **[DS]** §12.1; **[MAN]** p. 16; **[SRC]** `M5GFX.cpp:2114` vs `EDP_SPI.cpp:33` |
| **C3** | **Neither vendor path performs the datasheet's prescribed RAM pre-clear.** §9.1 step 3 opens with `0x46`/`0x47` data `0xF7` on both RAMs. DKE's reference program **[MAN]** p. 24 does not; the M5Stack OTP demo does not; M5GFX does not. Since RAM is explicitly **not** reset by `SWRESET` and **not** retained through deep sleep, the first frame after a cold start is drawn against undefined RAM in the plane you did not write. In the mono path only `0x24` is written, so the `0x26` plane is never initialised. **Latent, not obviously active** — `0x21`'s "bypass RAM content as 0" option exists precisely to neutralise this, and the demo writes `0x21 = 0x00` (normal), so it does *not* neutralise it. Worth checking on hardware | **[DS]** §9.1, §7 (`0x12` note); **[MAN]** p. 24; **[SRC]** `EDP_OTP_LUT_demo.cpp:319` |
| **C4** | **The `0x22` values in use are undocumented.** Datasheet lists `80 01 C0 03 91 99 B1 B9 C7 CF F7 FF`; DKE's manual lists `C7`, `90`, `47`; DKE's reference program uses `F7`; M5Stack uses `FF`, `D7`, `F8`, `14`. Only `FF` is common to the datasheet and M5Stack. The values are evidently a **bit-field** — `CF = C7 \| 0x08`, `F7 = C7 \| 0x30` — and M5GFX carries a comment confirming decomposability ("0x07 becomes 0xC7 when the analog section is off: Mode 1 refresh, followed by analog and oscillator power-down"). **But no source in hand publishes the bit definitions**, so `D7`, `F8` and `14` cannot be decoded with confidence. Copy values from a known-working sequence; do not compose your own | **[DS]** §7; **[MAN]** p. 18, p. 24; **[SRC]** `EDP_OTP_LUT_demo.cpp:264-375`, `Panel_SSD1677.cpp` |
| **C5** | **Deep-sleep parameter `0x01` is not a documented value.** The table defines only `00` (normal) and `11` (⇒ `0x03`). **Both** DKE's reference program and M5Stack's demo write `0x01`. Two independent vendors converging on the same undocumented value more likely means loose decoding than a shared typo, but that is **`inferred`** | **[DS]** §7 (`0x10`); **[MAN]** p. 24; **[SRC]** `EDP_OTP_LUT_demo.cpp:236` |
| **C6** | **OTP contents are unpublished and can silently prevent refresh.** How many of the 34 WS/TR slots DKE programmed, and over what span, is not disclosed by anyone. Out of range, the display simply does not update (§4.2). `0x2D` is the only in-system probe and no vendor driver calls it | **[DS]** §6.9, §6.10, §7 |
| **C7** | **Fault and status reporting is entirely unused.** `0x2F` (HV-ready, VCI-detect, busy, chip ID), `0x14`, `0x34`/`0x35` (OTP CRC) are read by neither vendor driver. Both poll the `BUSY` pin. A VCI brown-out or a failed HV ramp therefore surfaces as a bad image rather than an error | **[SRC]**, full call-list extraction; **[DS]** §6.11, §6.12, §7 |
| **C8** | **Page-count discrepancy in the retained file.** The PDF has **46 pages**; the document numbers itself `P n/47` in every footer. Either one page was dropped in the mirroring, or the original's numbering was off by one. Section §1 through §13 and the tables referenced above are all present and internally consistent, so no cited content is missing — but the artifact is **not byte-faithful to a 47-page original** if one existed | `executed-success` — `pdfinfo` reports `Pages: 46`; **[DS]** footers |
| **C9** | **The mirrored file was re-processed.** Producer string is **`PDFill: Free PDF Writer and Tools`**, CreationDate **2019-01-09** — i.e. this is not Solomon Systech's own PDF export but a re-written copy, two months after the stated Nov 2018 publication. Text layer was validated against rendered headings before any value here was transcribed; no corruption found. Related to C8 | `executed-success` — `pdfinfo` metadata |
| **C10** | **`TOPR −25 to +85 °C` is the *die* rating, not the display's.** The DKE module is rated **0 to +50 °C** operating. Quoting the controller's range for the PaperMono display over-states the envelope by 25 °C at one end and 35 °C at the other | **[DS]** §10; **[MAN]** p. 9 |
| **C11** | **Reserved pins are not merely "don't care".** `DP[0:33]` **must be tied to `VSS`**; `TP1`–`TP9`, `TIN`, `TPE` and `RSV` must be **left open and not connected to one another**. On a COG bond this is the panel maker's problem, but it matters if you ever evaluate the bare die | **[DS]** §5, Table 5-6 |

---

## 8. Electrical

### 8.1 Absolute maximum ratings

**[DS]** §10, Table 10-1.

| Symbol | Parameter | Rating | Unit |
|---|---|---|---|
| `VCI` | Logic supply voltage | **−0.5 to +4.0** | V |
| `VIN` | Logic input voltage | −0.5 to V<sub>DDIO</sub> + 0.5 | V |
| `VOUT` | Logic output voltage | −0.5 to V<sub>DDIO</sub> + 0.5 | V |
| `TOPR` | Operating temperature | **−25 to +85** | °C |
| `TSTG` | Storage temperature | −65 to +150 | °C |

Datasheet's own note: unused inputs should be tied to `VSS` or `VDDIO`; unused outputs **must be left open**; **"This device may be light sensitive. Caution should be taken to avoid exposure of this device to any light source during normal operation."** — relevant to bare-die handling.

### 8.2 Supply and currents

**[DS]** §2, §11, Table 11-1.

| Symbol | Parameter | Condition | Min | Typ | Max | Unit |
|---|---|---|---:|---:|---:|---|
| `VCI` | Logic supply | | **2.2** | | **3.3** | V |
| `VDDIO` | Interface logic supply | **connect to `VCI`** | | | | |
| `VDD` | Core | regulated from `VCI` | | **1.8** | | V |
| `VPP` | **OTP program voltage** | | 7.25 | **7.5** | 7.75 | V |
| `Islp_VCI` | **Sleep mode current** | DC/DC off, no clock, no load, MCU + RAM access allowed | | **25** | 40 | µA |
| `Idslp_VCI` | **Deep sleep current** | DC/DC off, no clock, no load, **no MCU access, RAM not retained** | | **1** | 5 | µA |
| `Iopr_VCI` | Operating current | `VCI = 3.0 V` | | **2.0** | | mA |
| `VGH` | Gate output | enabled via Master Activation | 19.5 | 20 | 20.5 | V |
| `VSH1` / `VSH2` / `VSL` | Source outputs | `VGH = 20 V`, `VGL = −VGH` | 14.8 / 4.9 / −15.2 | 15 / 5 / −15 | 15.2 / 5.1 / −14.8 | V |
| `VCOM` | | no transitions, no load | −2.2 | −2 | −1.8 | V |
| `VGATE(p-p)` | Gate peak-to-peak | `G0~G679` | | | **40** | V |
| `VIH` / `VIL` | Logic thresholds | | 0.8 V<sub>DDIO</sub> | | 0.2 V<sub>DDIO</sub> | V |

Regulator source capability **[DS]** Table 11-2: `IVGH`/`IVGL` **1000 µA max**; `IVSH1`/`IVSH2`/`IVSL`/`IVCOM` **2000 µA max**. Note the difference between the controller's ~2 mA operating current and the **module's** 12 mA typical / 120 mA peak **[MAN]** p. 10 — the delta is the panel and the external boost network, not the die.

---

## 9. Libraries

| Option | Where | Verdict |
|---|---|---|
| **`M5PaperMono-OTP-Demo`** — direct SPI, OTP waveforms only | `github.com/m5stack/M5PaperMono-OTP-Demo`, MIT | ✅ **The vendor's own recommendation** for this panel, and the safe path with respect to DC balance (§4.4). Two files: `EDP_SPI.cpp` (bus + reset) and `EDP_OTP_LUT_demo.cpp` (init + three refresh modes). Small enough to read in full |
| **M5GFX `Panel_SSD1677` / `Panel_SSD1677_4Gray`** | `github.com/m5stack/M5GFX`, MIT | ⚠ Full graphics stack, four refresh modes, LVGL-friendly — **but** uploads custom LUTs, runs the bus at 2× spec (§3.2), and its waveforms are being actively changed between branches (§4.5) |
| Roll your own | — | The command set in §5 plus the flow in §6 is complete enough. **Use OTP waveforms.** Do not write `0x32` unless you can prove DC balance |

Framework constraints imposed by the M5Stack path, not by the controller **[SRC]**: ESP-IDF **5.5.1**, target `esp32s3`, arduino-esp32 **3.3.10** as a managed component, and **octal PSRAM is mandatory** — `M5GFX.cpp:2072-2081` aborts display init with `"M5PaperMono need OPI-PSRAM enabled"` if `CONFIG_SPIRAM_MODE_OCT` is missing, leaving a working board with a dark screen and one easily-missed log line.

No mainline Linux DRM driver for the SSD1677 was located in this pass. `not-tested`.

---

## 10. Used By

### [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) — bonded inside panel `J5`, sheet 4

The SSD1677 is **not a board-level component**: it is chip-on-glass inside the [DKE DEPG0397BBS770F3](../../dke/depg0397bbs770f3/README.md) module and has no reference designator of its own. It is reachable only through the panel's 24-pin FPC at `J5`.

| Controller signal | FPC pin | PaperMono net | Host | Evidence |
|---|---:|---|---|---|
| `SDA` (SDI) | 14 | `G14_SPI2_MOSI` | ESP32-S3 **GPIO14** | **[SCH]** `J5`.14; **[SRC]** `EDP_SPI.cpp:26`, `M5GFX.cpp:2106` |
| `SCL` | 13 | `G15_SPI2_CLK` | ESP32-S3 **GPIO15** | **[SCH]** `J5`.13; **[SRC]** `EDP_SPI.cpp:27`, `M5GFX.cpp:2108` |
| `CS#` | 12 | `G16_EINK_CS` | ESP32-S3 **GPIO16** | **[SCH]** `J5`.12; **[SRC]** `EDP_SPI.cpp:28`, `M5GFX.cpp:2085, 2123` |
| `D/C#` | 11 | `G17_EINK_DC` | ESP32-S3 **GPIO17** | **[SCH]** `J5`.11; **[SRC]** `EDP_SPI.cpp:29`, `M5GFX.cpp:2109` |
| `BUSY` | 9 | `G18_EINK_BUSY` | ESP32-S3 **GPIO18** | **[SCH]** `J5`.9; **[SRC]** `EDP_SPI.cpp:30`, `M5GFX.cpp:2125` |
| `RES#` | 10 | `PYB_EINK_RST` | **[M5IOE1](../../m5stack/m5ioe1/README.md) `IO5`** — *not* an ESP32 pin | **[SCH]** `J5`.10; `M5GFX.cpp:2124` sets `cfg.pin_rst = GPIO_NUM_NC` |
| `VDDIO`/`VCI` | 15 | `EPD_3V3_L3B` | Rail gated by **M5IOE1 `IO3`** | **[SCH]** `J5`.15; **[SRC]** `EDP_SPI.cpp:37` |
| `GDR` / `RESE` | 2 / 3 | — | Board-side boost network | **[SCH]** `J5`.2, `J5`.3 |

Integration facts specific to this board:

- **The reset pin is behind the I²C expander.** Since `RES#` is the *only* way out of deep sleep (§5.5), and the OTP demo enters deep sleep after **every** refresh, **a functioning I²C bus and a functioning M5IOE1 are on the critical path for every single screen update**. That is a real coupling: an I²C fault — for instance the IP2315 charger disturbing the bus, which M5Stack documents as a live hazard — takes the display down with it.
- **Reset timing is 50× the module vendor's.** DKE's reference specifies **200 µs** low and 200 µs high **[MAN]** p. 24; `EDP_SPI.cpp`'s `hardware_reset()` uses **10 ms** each way **[SRC]**. Generous, which is the safe direction.
- **Geometry as configured:** 480 gate lines, 800 source columns, interlaced gate scan (`SM = 1`), driven landscape and rotated in software (`offset_rotation = 3`, `M5GFX.cpp:2126-2130`). §1.1.
- **Frame buffers:** the OTP demo allocates `3 × 48 000` bytes in PSRAM (`MALLOC_CAP_SPIRAM`) — 100 bytes/row × 480 rows × 3 planes **[SRC]** `EDP_OTP_LUT_demo.cpp:96`.
- **Bus:** SPI2_HOST, mode 0, half-duplex, 4092-byte chunks, DMA-capable internal staging buffer **[SRC]** `EDP_SPI.cpp:32-34, 225-257`.
- **Neither driver reads the controller's status register**, so the VCI-detect and HV-ready flags are unused on this board (§7-C7).

### [Waveshare ESP32-S3-ePaper-3.97](../../../devices/waveshare/esp32-s3-epaper-3.97/README.md) — bonded inside the panel on FPC `J2` — *added 2026-09-01*

**A second, independent board using this controller — from a different vendor, with a different panel supplier, at the same 3.97-inch size.** As on the PaperMono the die is chip-on-glass with no reference designator of its own, reachable only through the panel's FPC connector (`J2` here).

| Controller signal | Host GPIO | Net | Evidence |
|---|---|---|---|
| `SCL` | GPIO11 | `EPD_SCK` | schematic **and** vendor `DEV_Config.h:49` |
| `SDA` | GPIO12 | `EPD_DIN` | schematic **and** `DEV_Config.h:50` |
| `CS#` | GPIO10 | `EPD_CS` | schematic **and** `DEV_Config.h:51` |
| `D/C#` | GPIO9 | `EPD_DC` | schematic **and** `DEV_Config.h:53` |
| `RES#` | GPIO46 | `EPD_RST` | schematic **and** `DEV_Config.h:52` |
| `BUSY` | GPIO3 | `EPD_BUSY` | schematic **and** `DEV_Config.h:54` |

- **Bus mode:** 4-wire 8-bit SPI. The panel manual documents `BSI` selecting 3-wire (9-bit) versus 4-wire, and the vendor driver defines `D_9PIN 1`.
- **Panel:** [Waveshare 3.97inch e-Paper](../../waveshare/3.97inch-e-paper/README.md), 800 × 480, active area 86.40 × 51.84 mm, DPI 235 — **the same active area and DPI as the DKE panel above, transposed**. Whether it is the same panel is [unresolved](../../../devices/waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws8--is-this-the-same-panel-as-the-papermonos).
- **Power:** no board-level EPD boost. The controller's integrated DC-DC does the work; `GDR`, `RESE`, `VGH`, `VGL`, `VSH1`, `VSH2`, `VSL`, `VCOM` and `VPP` all appear on `J2`. Logic supply comes from an [AXP2101](../../x-powers/axp2101/README.md) rail, and there is **no GPIO panel-power pin** (`EPD_PWR_PIN -1`) — power gating is a PMIC operation.
- **Driver:** Waveshare's own `EPD_3in97.cpp/.h`, which exposes `Init`, `Init_Fast`, `Init_Partial`, `Init_4GRAY` and matching `Display*` entry points including `_Base` variants (the previous-image buffer this controller needs for correct partial refresh).
- **Not audited.** Unlike the PaperMono entry above, **no register-level read of this vendor's driver has been done** — the initialisation sequences, LUT handling and whether §4.4's DC-balance hazard is mitigated are all **unexamined**. That is the obvious next piece of work, and it is tracked as [G2](../../../devices/waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md#gaps).

### [M5Stack PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md)

**Same controller, same panel, same wiring.** The Lite drops NFC and LoRa only; both product pages carry an identical display specification and both link the same "SSD1677 Display Driver" datasheet **[DOC]**. The Lite's schematic is published as a 4-sheet `PRJ` PDF rather than a 6-sheet `SCH`, so its `J5` wiring is **not** independently confirmed here.

### [Xteink X4 Pro](../../../devices/xteink/x4-pro/README.md), [X4](../../../devices/xteink/x4/README.md) and [X4 Classic](../../../devices/xteink/x4-classic/README.md) — *added 2026-09-04*

Three sealed consumer e-readers, all 800 × 480, all carrying this controller **as
the boot default** — and all three of which **also ship in batches carrying an
UltraChip [UC8179](../../ultrachip/uc8179/README.md) or
[UC8279](../../ultrachip/uc8279/README.md) instead**, on identical wiring, with
no external marking to distinguish them.

| Signal | X4 Pro (ESP32-S3) | X4 (ESP32-C3) | X4 Classic (ESP32-S3) |
|---|---:|---:|---:|
| SCLK | 12 | 8 | 12 |
| MOSI (SDA) | 11 | 10 | 11 |
| CS | 13 | 21 | 13 |
| DC | **18** | 4 | **14** |
| RST | **14** | 5 | **10** |
| BUSY | **6** | 6 | **18** |

**Note the X4 Pro and X4 Classic permute DC/RST/BUSY between themselves** despite
sharing SCLK/MOSI/CS — porting display code between the two without changing those
three produces a panel that resets and runs waveforms but never develops an image.

Clocks: X4 Pro **20 MHz** (OEM uses only 5 MHz); X4 **20 MHz** default with an
opt-in, out-of-spec **40 MHz** mode (`-DFREEINK_X4_OVERCLOCK_SPI`) that halves
plane-write time from ~38 ms to ~19 ms *"but can glitch plane writes on marginal
wiring"*; X4 Classic 20 MHz.

**This controller's most consequential property here is a negative one: it does
not answer `VER (0x70)` or `FLG (0x71)`.** That silence is exactly what the
FreeInk SDK's boot probe uses to tell an SSD1677 from its UltraChip substitutes —
a released data line floats to a uniform `0x00`/`0xFF` on an SSD part and returns
a driven, structured pattern on a UC81xx. See
[`components/ultrachip/uc8179`](../../ultrachip/uc8179/README.md) §2 for the
`CHIP_VER = 0x00` false-negative that this matcher had to be corrected for.

No external EPD PMIC and no external charge pump on any of the three: the
controller drives its high-voltage rails from its **internal booster**
(`0x0C` soft-start). An early X4 Pro investigation wrongly concluded otherwise.

Recovered OEM command streams (X4 Pro, firmware 7.4.4): FULL `0x22 = 0xF7`,
FAST `0x22 = 0xFC`, border `0x3C = 0xC0`, master activation `0x20`, wait BUSY.
An earlier X4 Pro image used `0xC7` for FAST — **version-scoped, do not hard-code**.
Driver output control `0x01 = DF 01 02` → gate lines `0x01DF` = 479, MUX 480,
`SM = 1`.

→ [`devices/xteink/x4-pro/features/display.md`](../../../devices/xteink/x4-pro/features/display.md)
→ [`devices/xteink/x4/features/display.md`](../../../devices/xteink/x4/features/display.md)
→ [`devices/xteink/x4-pro/factory-firmware.md`](../../../devices/xteink/x4-pro/factory-firmware.md)

---

## 11. Related components

- [**DKE DEPG0397BBS770F3**](../../dke/depg0397bbs770f3/README.md) — the panel this die is bonded into. **Read that record first** for the FPC pinout, the external boost network, the optical/mechanical specification and the module's much narrower temperature rating
- [**Waveshare 3.97inch e-Paper**](../../waveshare/3.97inch-e-paper/README.md) — *added 2026-09-01*. A second 3.97-inch panel carrying this controller, from a different vendor. Matches the DKE panel's active area to 0.01 mm and its DPI exactly; **its manual states the gate/source orientation the opposite way round** from what §1.1's register evidence establishes here, which is [unresolved](../../../devices/waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws7--gate-versus-source-orientation)
- [**M5Stack M5IOE1**](../../m5stack/m5ioe1/README.md) — supplies `RES#` (`IO5`) and the panel's 3V3 rail (`IO3`)
- [**M5Stack M5PM1**](../../m5stack/m5pm1/README.md) — drives the board's frontlight; this controller has no backlight function
- [Vendor sourcing guides index](../../../vendors/README.md) — no Solomon Systech sourcing guide exists yet. This datasheet was obtained **only** as an M5Stack product-page mirror; no Solomon Systech-hosted copy was located

---

## 12. Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/ssd1677-rev1.0-nov2018-m5stack-mirror.pdf` | 3 602 487 | `daf8b726f822f6907529386b8af6fbea6ec5e8ecc7b7af361340be911d632544` | **SSD1677 datasheet, "Advance Information", Rev 1.0, Nov 2018.** PDF 1.4, A4, **46 pages** (document numbers itself `n/47` — §7-C8). Producer **`PDFill: Free PDF Writer and Tools`**, CreationDate **2019-01-09** — a re-written copy, not Solomon Systech's own export (§7-C9) |

**Text-layer validation.** `pdftotext -layout` output was cross-checked against the cover block (`SOLOMON SYSTECH` / `SEMICONDUCTOR TECHNICAL DATA` / `Advance Information`), the per-page footer (`SSD1677  Rev 1.0  P n/47  Nov 2018`) and the numbered contents list before any value here was transcribed. No glyph subsetting or code-point-offset corruption was observed; extracted section headings match the table of contents exactly.

**Licence.** Third-party (Solomon Systech) copyright — "Copyright © 2018 Solomon Systech Limited" — mirrored by M5Stack with no stated terms. **Redistribution status `unknown`**; disposition `repository` pending review. Unlike some vendor datasheets in this repository, this one carries **no per-page confidentiality footer**, so no strict term was observed.

**Only one acquisition URL is known.** Located solely as an attachment on M5Stack's PaperMono product page, labelled "SSD1677 Display Driver". No Solomon Systech-hosted copy and no second independent mirror were found in this pass. Single-source status recorded deliberately rather than left as a silent gap; a later revision may exist behind Solomon Systech's registration wall.

---

## 13. Authoritative sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | SSD1677 — 960 Source × 680 Gate Red/Black/White Active Matrix EPD Display Driver with Controller | **Solomon Systech Limited**, mirrored by M5Stack | authorized mirror | datasheet | `artifacts/ssd1677-rev1.0-nov2018-m5stack-mirror.pdf`; upstream `static-cdn.m5stack.com/resource/docs/products/core/PaperMono/…` (linked as "SSD1677 Display Driver") | 2026-09-01 | **Rev 1.0, Nov 2018 — "Advance Information"** | §1–§8 |
| S-2 | EPD Module User Manual — `DEPG0397BBS770F3` | DKE Holding Company Limited, mirrored by M5Stack | primary (via mirror) | module specification | [`../../dke/depg0397bbs770f3/artifacts/depg0397bbs770f3-epd-module-user-manual.pdf`](../../dke/depg0397bbs770f3/README.md) | 2026-09-01 | drawing REV A0, 2024-09-29 | §1.1, §3.2, §5, §7-C4/C5/C10 |
| S-3 | `M5PaperMono-OTP-Demo` | M5Stack | primary | source | `github.com/m5stack/M5PaperMono-OTP-Demo` @ `c7c02554f89fd06f80d988b805b2a59050c78a46` | 2026-09-01 | 2026-08-20, MIT | §5, §9, §10 |
| S-4 | `M5GFX` (`master` and `develop`) | M5Stack | primary | source | `github.com/m5stack/M5GFX`, `master` @ `d91077b9a607b59404e4e4a49f775c792bfae382`, `develop` @ `8d6e8b3e0e9629e0bf0702d263e9263b588b6075` | 2026-09-01 | release 0.2.28 | §3.2, §4.5, §9, §10 |
| S-5 | `M5PaperMono-UserDemo` | M5Stack | primary | source | `github.com/m5stack/M5PaperMono-UserDemo` @ `c1099107271d31a0678d661a896e2b04dbb331ea` | 2026-09-01 | 2026-08-10, MIT | §4.5 pinned-commit divergence |
| S-6 | PaperMono schematic | M5Stack | primary | schematic PDF | `PaperMono_SCH_V0.6.2_20260522.pdf` (held in the device tree) | 2026-09-01 | **V0.6.2, 2026-05-22**, 6 sheets | §10 wiring (sheet 4, `J5`) |
| S-7 | PaperMono product page | M5Stack | primary | vendor docs | `docs.m5stack.com/en/core/PaperMono` | 2026-09-01 | undated | §4.4 DC-balance warning, §4.5 OTP recommendation |
