# Solomon Systech SSD1683

- **Category:** active-matrix EPD (e-paper) display driver **with controller** — source/gate drivers, on-chip booster and regulators, oscillator, dual display RAM, programmable waveform engine, OTP waveform store, temperature sensing, SPI MCU interface, **two-chip cascade**
- **Package:** **gold-bump die only** (COG). No packaged part exists.
- **Document status:** **"Advance Information", Rev 1.0, Jan 2021** — *"1.0 Initial Release, 26-Jan-2021"*, the only revision
- **Research status:** full datasheet retained in `artifacts/`; text layer **validated page-by-page** (§11). **No hardware, no driver source and no board was examined.** **Reference-only** — see §2.
- **Retrieved / written:** 2026-09-20

The **400 × 300** member of the family — the controller behind most 4.2-inch SPI e-paper modules. **Its waveform block is genuinely different from the SSD1680/SSD1681's, not a scaled copy** (§4), and its temperature handling dropped from 12-bit to 8-bit (§5). Not fitted on any device documented in this repository.

> ⚠ **The PDF's own `Title` metadata says `SSD1780`.** Every page of the document says SSD1683. See §11 — this is not a trivial curiosity; it is why this file was catalogued under the wrong name by an earlier pass of this repository, and the correction is recorded in §11.

---

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[DS]** | Stated in `artifacts/ssd1683-rev1.0-jan2021.pdf`, cited by section or **PDF page number** (which equals the printed footer page — proven in §11) | `not-tested` — vendor claim reproduced; nothing measured |
| **[DS1680]** | The [SSD1680 datasheet](../ssd1680/README.md), cited for comparison | `not-tested` |
| **[CF]** | Crystalfontz catalogue and document fetch, live 2026-09-20 | `executed-success` |
| **[REPO]** | An existing record in this repository | as labelled there |
| **[INF]** | Inference | `inferred` |

**Nothing here was verified on hardware.**

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Solomon Systech Limited** | **[DS]** cover, footers |
| Part | **`SSD1683`** | **[DS]** cover and all 49 page footers |
| Document title, verbatim | **"400 Source x 300 Gate Red/Black/White — Active Matrix EPD Display Driver with Controller"** | **[DS]** cover |
| Document status, verbatim | **"Advance Information"** — "This document contains information on a new product. Specifications and information herein are subject to change without notice." | **[DS]** cover |
| Revision / date | **Rev 1.0, Jan 2021**; revision history: *"1.0 Initial Release, 26-Jan-2021"* — **no later revision exists in the document and none was located** | **[DS]** cover, p. 2 |
| Copyright line | *"Copyright © **2020** Solomon Systech Limited"* — ⚠ the year on a Jan-2021 document | **[DS]** cover |
| Ordering parts | **`SSD1683Z`** (gold bump die, **bump face up**) and **`SSD1683Z8`** (**bump face down**). Both: waffle pack, die thickness **300 µm**, bump height **12 µm** | **[DS]** §3, Table 3-1, p. 6 |
| Maximum geometry | **400 source outputs · 300 gate outputs · 1 VCOM · 1 VBD** ⇒ max **400 × 300**; **800 × 300 in cascade** | **[DS]** §1 p. 5, §5 Table 5-4 p. 9 (`S[399:0]`, `G[299:0]`), §6.12 p. 21 |
| Colour capability | **Red / Black / White** — two RAM planes, `400 × 300` bits each | **[DS]** §2 p. 5, §6.5 p. 13 |
| MCU interface | **SPI only** — 4-wire (8-bit) or 3-wire (9-bit), pin-selected by `BS1` | **[DS]** §6.1.1 Table 6-1, p. 10 |
| ⚠ Marking verified? | **No.** No unit inspected | **[INF]** |

---

## 2. Used By — nothing here, and why it was kept

**No device documented in this repository is known to carry an SSD1683.** No schematic, firmware image or driver source in this tree names it as a fitted part.

It is retained, and was mined, for three reasons — and one of them is a correction:

1. **It is cited by an existing record.** [`devices/m5stack/papermono/gaps-and-conflicts.md`](../../../devices/m5stack/papermono/gaps-and-conflicts.md) cites *"SSD1683 (Rev 1.0, pp.23-24)"* — **this file, these pages** — among the three siblings that decode the SSD1677's opaque `0x0C` Booster Soft-start Control **[REPO]**. That decode is confirmed here from the primary document (§6.3).
2. **⚠ It corrects a claim that record makes from a secondary source.** The same file states, from a CSDN blog post, that an SSD1683 external waveform is *"a 227-byte waveform payload followed by six parameter bytes (`0x3F`, VGH, VSH1, VSH2, VSL, VCOM)"*. **The primary document confirms the 227 bytes and the total — but the trailing block is five registers in six bytes, not six registers**: WS byte 227 = `0x3F`, 228 = `0x03` (VGH), **229–231 = `0x04` (VSH1, VSH2, VSL — one register, three bytes)**, 232 = `0x2C` (VCOM). 227 + 6 = 233, which the datasheet states explicitly. **[DS]** §6.7, p. 16. The blog's arithmetic was right and its register attribution was one column off; the practical warning it drew — *"changing a waveform silently changes the rail voltages unless you preserve those six bytes"* — **is correct and is now backed by the primary source.**
3. **It documents a family divergence that would silently break a port.** The SSD1683's LUT is not a bigger SSD1680 LUT; it is a different structure with per-colour LUTs, 32 phases instead of 48, one global frame-rate byte instead of twelve, and **8-bit temperature instead of 12-bit** (§4, §5). Anyone assuming "SSD16xx" means one command set will get a panel that resets, runs a waveform and produces nothing.

Where the FreeInk / CrossPoint software tree is concerned, note the negative result already recorded in this repository: **the PaperMono's controller was called "SSD1683" in build comments until [crossmux PR #221](https://github.com/0x1abin/crossmux/pull/221) corrected it to SSD1677 on 2026-08-24, and upstream `crosspoint-reader`'s `platformio.ini` still says `SSD1683 800x480`** **[REPO]** [`projects-and-community.md`](../../../devices/m5stack/papermono/projects-and-community.md). **That is a comment-only defect and is not evidence of an SSD1683 anywhere.** This record exists partly so nobody re-promotes that string to a fitment.

---

## 3. Capabilities

**[DS]** §1–§2, pp. 5–6 unless noted.

| Area | Capability |
|---|---|
| Display RAM | **Two on-chip planes**, `400 × 300` bits each — B/W and Red |
| Supply | `VCI` **2.3–3.7 V** ⚠ (the SSD1680/1681 start at **2.2 V**); `VDDIO` connect to `VCI`; `VDD` **1.8 V regulated from VCI** |
| Drive voltages, on-chip | Booster + regulator generate `VGH`, `VGL`, `VSH1`, `VSH2`, `VSL`, `VCOM` |
| Gate output | 2 levels, **max 40 Vp-p**; `VGH` **10–20 V** in 500 mV steps; `VGL` = −`VGH` |
| Source output | 4 levels. ⚠ **`VSH1` and `VSH2` have different ranges here**: `VSH1` **8.6–17 V** (200 mV steps); `VSH2` **2.4–17 V** (100 mV to 8.6 V, 200 mV above). `VSL` **−5 to −17 V** (500 mV steps) |
| VCOM | `DCVCOM` **−3.0 to −0.2 V** in 100 mV steps; `ACVCOM` 3 levels. **VCOM sensing** on-chip |
| Oscillator | **Adjustable frame rate 25 Hz – 125 Hz** ⚠ (SSD1680/1681: 25–200 Hz) |
| Waveform engine | **Two selectable waveform sets, chosen by `0x22`**: **4 LUTs for 3-colour mode**, **5 LUTs for black/white mode** |
| OTP store | **24 waveform settings (WS0–WS23)** and **24 temperature ranges (TR0–TR23)**, plus VCOM, **colour-mode selection**, 4-byte waveform version, 10-byte User ID, and the initial code setting |
| OTP programming | External **or internal** generated voltage; **CRC checking for RAM content and for WS & TR in OTP** |
| Temperature | Internal sensor **−25 to +50 °C, ±2 °C**; or **I²C single-master** to an external sensor; ⚠ **8-bit value, 1 °C resolution** (§5) |
| Diagnostics | **VCI low-voltage detection** · **HV-ready detection with cool-down looping** · status read `0x2F` |
| Display features | **Partial update** · **auto write RAM for regular patterns** · **RAM Ping-Pong** (black/white mode only) |
| Cascade | **Two chips → 800 × 300**, `M/S#` pin **plus** a `0x21` `B[4]` enable bit (§6.2) |
| MCU interface | 4-wire or 3-wire SPI, **max SPI write 20 MHz**, read 2.5 MHz |
| Package | **COG (gold bump die)** |

Notably **absent** from the feature list compared with the SSD1680: the **panel break diagnostic**. Confirmed absent from the command table too (command census, `executed-success`).

---

## 4. ⚠ The waveform block is a different design, not a scaled one

This is the section that matters. An SSD1680/SSD1681 LUT will not work here and vice-versa, and the incompatibility is structural rather than a matter of length.

### 4.1 Waveform setting — **233 bytes**, `0x32` writes **227**

**[DS]** §6.7, Figures 6-6 / 6-7, p. 16, and §7 `0x32`, p. 32:

| WS byte | Content | Written by |
|---:|---|---|
| **0–226** | The waveform LUT proper | **`0x32` — "[227 bytes]"** |
| 227 | **"display off sequence"** — note the wording, not "option for LUT end" | `0x3F` |
| 228 | Gate level (`VGH`) | `0x03` |
| **229–231** | Source levels — **`VSH1`, `VSH2`, `VSL`: one register, three bytes** | `0x04` |
| 232 | VCOM level | `0x2C` |

> ⚠ **Precedence, stated explicitly and worth knowing** **[DS]** §6.7: *"These commands (0x32, 0x3F, 0x03, 0x04 and 0x2C) **can be overridden by the latest register setting**. For example, if waveform setting A is loaded from OTP first, then, MCU has written another waveform setting B into the driver IC after OTP loaded. The driver IC will use the waveform setting B to drive the display."*
>
> So **last writer wins**, and a partial MCU write after an OTP load silently replaces only the bytes you wrote — including, if you touch `0x04`, the rail voltages. This is the mechanism behind the warning quoted in §2.

### 4.2 The LUT layout — per-colour LUTs, 8 groups, 7 bytes per group

**[DS]** Figure 6-6 (3-colour mode), p. 16. The 227 bytes are **four LUTs of 56 bytes each**, plus three trailing bytes:

| Byte range | LUT | Meaning |
|---:|---|---|
| 0–55 | **LUTC** | 8 groups × 7 bytes |
| 56–111 | **LUTR** | ″ |
| 112–167 | **LUTW** | ″ |
| 168–223 | **LUTB** | ″ |
| **224** | — | **`FR` — one global frame-rate byte** |
| 225–226 | — | **`XON[0AB]`…`XON[7CD]`**, 16 bits over two bytes |

Each 7-byte group `n` is laid out: `RP LUTx n` · `VS-nA / TP nA` · `VS-nB / TP nB` · `VS-nC / TP nC` · `VS-nD / TP nD` · `SR LUTx nAB` · `SR LUTx nCD`. Note `VS` and `TP` are **packed into the same byte** (`D7:D6` = VS, `D5:D0` = TP), which is why a group costs 7 bytes instead of the SSD1680's byte-per-parameter layout.

**The four differences that break a port:**

| | SSD1680 / SSD1681 | **SSD1683** |
|---|---|---|
| Groups × phases | 12 × 4 = **48 phases** | **8 × 4 = 32 phases** |
| LUT identity | **LUT0–LUT4**, selected by RAM bit pair | **LUTC / LUTR / LUTW / LUTB** — named for the *colour transition* they drive |
| Frame rate | **`FR[0..11]`, per group**, 6 bytes | **one global `FR` byte** |
| `VS` / `TP` packing | separate byte regions (`VS` bytes 0–59, `TP`/`SR`/`RP` bytes 60–143) | **`VS` and `TP` share a byte, per phase** |

**[DS]** Figure 6-6 p. 16 vs **[DS1680]** Figure 6-6 p. 15.

### 4.3 RAM bits → colour → LUT

**[DS]** §6.5, Tables 6-4 / 6-5, p. 13. The SSD1683 names the LUTs after the transition rather than numbering them:

| R RAM (`0x26`) | B/W RAM (`0x24`) | 3-colour mode | Black/white mode |
|:---:|:---:|---|---|
| 0 | 0 | Black — **LUTB** | Black — **LUTBB** |
| 0 | 1 | White — **LUTW** | White — **LUTWB** |
| 1 | 0 | **Red — LUTR** | Black — **LUTBW = LUTBB** |
| 1 | 1 | *(row absent from Table 6-4)* | White — **LUTWW = LUTWB** |

⚠ **Table 6-4 has only three rows** — the `R=1, BW=1` case is simply not listed for 3-colour mode. On the SSD1680 the equivalent row is *"Red, LUT3 = LUT2"*. What this part does with that bit pattern is **not stated**. Unresolved; write `R=1, BW=0` for red and avoid the combination.

⚠ **The B/W-mode LUT names in Table 6-5 (`LUTBB`, `LUTWB`, `LUTBW`, `LUTWW`) do not appear in the Figure 6-6 byte map**, which uses `LUTC` / `LUTR` / `LUTW` / `LUTB` (that is the 3-colour figure; Figure 6-7 is the black/white one, on the following page). Expect the mapping between the two naming schemes to need care.

### 4.4 OTP — 24 slots, and the arithmetic checks out

**[DS]** §6.10, Figure 6-8, p. 20: **WS0 at address 0**, 233 bytes each, through **WS23 ending at 5591**; then **TR0 at 5592**, **2 bytes each**, through **TR23 ending at 5639**. Total **5640 bytes**.

That total is independently confirmed inside the command table: `0x41`'s CRC counter-mode default is *"`{C[7:0], B[7:0]}` : default is `0x1608`, **as the LUT bytes is 5640 bytes**"* — and `0x1608` = 5640 **[DS]** §7 p. 34. `24 × 233 + 24 × 2 = 5640`. ✅ The two statements agree; recorded because family documents this old frequently do not.

Selection **[DS]** §6.9, p. 19: read the temperature, search **TR0 → TR23 in sequence**, criterion `lower < sensed ≤ upper`, **last match wins** (worked example: 34 °C selects WS7 over the equally-matching TR6).

> ⚠ **Same silent-failure mode, verbatim:** *"Please ensure the temperature range covers whole range of application temperatures, **display will not be updated if no suitable temperature range matches the sensed temperature**."* **[DS]** p. 19. No status bit reports it. `0x2D` returning the 4-byte waveform version is the only in-system probe of what a panel maker actually burned.

### 4.5 ⚠ DC balance

Not mentioned in this document. Writing `0x32` makes you responsible for net-zero charge delivery; failing degrades the ink **irreversibly**. The OTP path cannot get it wrong. Documented for the family on the SSD1677 by M5Stack (*"irreversible damage may be caused to the panel"*) and DKE — [SSD1677 §4.4](../ssd1677/README.md#44--the-dc-balance-hazard). Family-level hazard, `inferred` for this part. §4.1's "last writer wins" precedence makes the trap sharper here: you can lose DC balance by writing *part* of a waveform over an OTP-loaded one.

---

## 5. ⚠ Temperature is 8-bit here, and the text says otherwise

**[DS]** §6.8.3, p. 18. *"The temperature value is defined by **8-bit binary**."* The worked table gives `0x19` = 25 °C, `0x32` = 50 °C, `0x00` = 0 °C, `0xFF` = −1 °C, `0xE7` = −25 °C, `0xC9` = −55 °C.

So: **value = degrees Celsius directly, two's complement, 1 °C resolution.** The SSD1680/SSD1681 use a **12-bit** value at **1/16 °C** resolution (`0x190` = 25 °C). This is consistent throughout the SSD1683: `0x1A`/`0x1B` (write/read temperature register) are **one byte** here (`A[7:0] = 7Fh` [POR]) against **two bytes** (`A[11:0] = 7FFh` [POR]) on the SSD1680, and a TR entry is **2 bytes** here against **3 bytes** there.

> ⚠ **Two residues of the 12-bit original survive in the text.**
> 1. The rule statement still reads ***"If the Temperature value MSByte bit D11 = 0…"*** — **there is no bit D11 in an 8-bit value.** The intended bit is plainly D7.
> 2. The table's first row prints `0111 1111` / `7F` / **`12B`** as the °C value. `0x7F` is **127**; the 12-bit table's corresponding row reads `127.9`. `12B` is neither. §6.9's own prose says *"33 DegC < Temperature ≤ **127** DegC"* for the same `7F` bound, so **127 is the value and `12B` is a typo.**
>
> The *encoding* is unambiguous and self-consistent across four independent places in the document. It is the *prose* that was not updated. **[DS]** §6.8.3 p. 18, §6.9 p. 19, §7 `0x1A` p. 27, §6.11 p. 20.

TR format **[DS]** §6.11, Figure 6-9, p. 20: two bytes — `temp_L[7:0]` (lower limit), `temp_H[7:0]` (upper limit). ⚠ The §6.11 prose says *"as shown in Figure 6-**8**"* while the figure is labelled **6-9** and Figure 6-8 is the OTP address map. Cosmetic.

---

## 6. Command set — what differs from the SSD1680

A **full census of §7's command table** (`executed-success`) returns the SSD1680's list **plus `0x16` and `0x17`, minus `0x2B`**. Everything else is common, and the [SSD1680 record §6](../ssd1680/README.md#6-command-set) is the reference for shared semantics. Recorded here: the part-specific values and the divergences.

### 6.1 Two commands the SSD1680 does not have

| Cmd | Meaning **[DS]** §7, p. 27 |
|---|---|
| **`0x16`** | **Program WS password to OTP.** *"Program R4C Password to OTP."* One byte. *"Require clock is active. And Busy = 1 during operation."* ⚠ **Register `0x4C` is referenced but does not appear anywhere else in the document** — not in the command table, not in §8. The waveform store is password-protected by a mechanism this datasheet does not describe |
| **`0x17`** | **Program Automated.** One byte selecting an OTP area: `0x08` init code (→ Cmd08) · `0x16` password (→ Cmd16) · `0x2A` VCOM (→ Cmd2A) · `0x30` LUT (→ Cmd30) · `0x36` User_ID (→ Cmd36). *"Command 17 only operating in internal program mode. Command 17 action performed: **open clock → analog on → program OTP → analog off → clock off.** Busy = 1 during operation"* — i.e. it wraps the whole power sequence that the SSD1680 makes you perform by hand |

`0x2B` (*Write Register for VCOM Control*, the SSD1680's magic `D04h`/`D63h` anti-glitch pair) **is absent** from the SSD1683's table.

### 6.2 Part-specific POR values and changed semantics

| Cmd | SSD1683 **[DS]** | Differs from SSD1680? |
|---|---|---|
| **`0x01`** Driver Output Control | **`A[8:0] = 12Bh` [POR] ⇒ 300 MUX**; MUX range **16 to 300**. `B[2:0] = 000`; `SM=1` ⇒ `G0,G2,G4…G294,G1,G3,…G299`; `TB=1` ⇒ `G299→G0` | ✅ correctly scaled |
| `0x03` Gate Driving Voltage | `00h` [POR] ⇒ **20 V**; `03h`=10 V … `17h`=20 V | same table, **same duplicated `07h`/`08h` rows** |
| `0x04` Source Driving Voltage | 3 bytes; ⚠ **`VSH1` min is 8.6 V here**, not 2.4 V | **range changed** |
| **`0x0C`** Booster Soft-start | **4 bytes**, POR **`8B 9C 96 0F`**; `[6:4]` strength 1–8, `[3:0]` min `GDR` off-time (`0100`=2.6 … `1111`=16.5; `0000`–`0011` **NA**), `D[5:0]` per-phase duration 10/20/30/40 ms | **identical** — this is the table §2 cites |
| **`0x1A` / `0x1B`** Temperature register | **one byte**, `A[7:0] = 7Fh` [POR] | ⚠ **two bytes / `7FFh` on the SSD1680.** §5 |
| **`0x21`** Display Update Control 1 | `A[7:4]` Red RAM, `A[3:0]` BW RAM (normal / bypass-as-0 / inverse). **`B[4]` = `ckouten`, Cascade selection: `0` single chip, `1` cascade.** *"For cascade mode, connect CL pin between Master sample with Slave sample"* | ⚠ **`B[7]` Source Output Mode on the SSD1680; `B[4]` cascade enable here.** Same command, same byte position, **different meaning** |
| **`0x22`** Display Update Control 2 | **`FFh` [POR]**; same twelve values `80 01 C0 03 91 99 B1 B9 C7 CF F7 FF` — but **relabelled**: mode 1 ⇒ **3-colour mode**, mode 2 ⇒ **black/white mode**. Also, `F7`/`FF` here **load the LUT as well as the temperature** before displaying, which the SSD1680's description of the same codes does not mention | ⚠ **semantics named differently and the F7/FF sequence is longer** |
| `0x2C` VCOM | `00h` [POR]; `08h` = −0.2 V … `78h` = −3.0 V | identical |
| **`0x3C`** Border Waveform | `C0h` [POR] = HiZ. `A[7:6]` VBD option; `A[5:4]` fixed level; `A[1:0]` LUT0–LUT3. ⚠ **The `A[2]` "GS Transition control" bit is gone** and a contradictory extra line appears — *"VBD Level Selection: 00b: VCOM ; 01b: VSH1; 10b: VSL; 11b: VSH2"* sits immediately above the `A[1:0]` table that says `00`=LUT0 … `11`=LUT3. **`A[1:0]` is given two incompatible meanings on the same page** | ⚠ **conflict, §9-C4** |
| **`0x3F`** `EOPT` | ***"Set this byte to 22h"*** — **no POR value, no alternatives listed** | ✅ **cleaner than the SSD1680's undefined `02h` POR.** But it also removes the documented `07h` "keep previous source level" option |
| **`0x41`** Read RAM Option | `A[0]` selects the `0x24`/`0x26` plane. **`A[4]` selects CRC check mode**: `0` = window mode per `0x44`/`0x45`; `1` = **counter mode** over `{C[7:0], B[7:0]}` bytes, **default `0x1608` = 5640** | ⚠ **three parameter bytes here; one on the SSD1680** |
| **`0x44`** RAM X start/end | `A[5:0]`/`B[5:0]`, **units of 8 pixels**. POR `XSA = 00h`, **`XEA = 31h` (49 ⇒ 50 bytes ⇒ 400 sources)** ✅ | ✅ **correct for this part** — unlike the [SSD1681](../ssd1681/README.md#31-the-ram-window-power-on-defaults-are-the-ssd1680s) |
| **`0x45`** RAM Y start/end | `A[8:0]`/`B[8:0]`, units of **gate lines**. POR `YSA = 000h`, **`YEA = 12Bh` (299 ⇒ 300 gates)** ✅ | ✅ correct |
| `0x46` / `0x47` Auto Write RAM | step height 8/16/32/64/128/256/**300**; step width 8/16/32/64/128/256/**400** | scaled correctly |
| `0x15` VCI Detection | `A[2:0] = 100` [POR] ⇒ **2.3 V**; `011`–`111` ⇒ 2.2–2.6 V | identical |
| `0x37` Write Register for Display Option | **Only `B`/`C`/`D` carry display mode** (WS[7:0], WS[15:8], WS[23:16]) — 24 slots, not 36. `0`= mode 1 (3-colour), `1`= mode 2 (black/white). `F[6]` **Ping-Pong**, *"not supported for 3-color mode"* | scaled to 24 WS |
| `0x2E` User ID Read | 10 bytes | identical |
| `0x2D` OTP Register Read | 11 bytes: VCOM OTP selection, VCOM register, 5 bytes display mode, **4 bytes waveform version** | identical |
| `0x34` / `0x35` | CRC calculation / 16-bit CRC status read | identical |
| **`0x10`** Deep Sleep | `00` Normal [POR] · **`01` Deep Sleep Mode 1** (RAM retained, inaccessible) · **`11` Deep Sleep Mode 2** (RAM lost). HWRESET required to exit | identical two-mode encoding — §9-C8 |

### 6.3 `0x0F` does not exist here either

Like the SSD1681, the SSD1683 has **no `0x0F` Gate Scan Start Position**: its §8 chapter covers only `0x01`, `0x11`, `0x44`/`0x45` and `0x4E`/`0x4F`, and the §7 census finds no `0x0F` row. If you need to drive a shorter panel from a 300-gate controller, this escape hatch is undocumented.

---

## 7. Reference operation flows — **two** of them

**[DS]** §9, pp. 41–42. Unlike the SSD1680, the SSD1683 publishes two flows, and the second is the one a battery device wants.

**§9.1 — drive with power on/off** (p. 41): identical in structure to the SSD1680's — power on / 10 ms → HW reset, SW reset `0x12`, 10 ms → `0x01`, `0x11`, `0x44`, `0x45`, `0x3C` → `0x18` then `0x22`+`0x20` to load the LUT, wait BUSY → `0x4E`, `0x4F`, `0x24`, `0x26`, `0x0C`, `0x22`+`0x20`, wait BUSY → power off.

**§9.2 — enter deep sleep mode 2 after display update** (p. 42): the same five steps, ending with ***"Enter Deep sleep mode 2 without RAM retention — Deep sleep by Command 0x10, data `0x03`"***.

> ⚠ **`0x10` `{0x03}` is the concrete, documented encoding of "Deep Sleep Mode 2".** `A[1:0] = 11` with the upper bits zero ⇒ `0x03`. This is worth noting precisely because the [SSD1677 record §7-C5](../ssd1677/README.md#7-caveats-errata-and-conflicts) flags that two vendors send `{0x01}` there against a datasheet documenting only `00` and `11`. **On this part `0x01` and `0x03` are both legal and mean different things** — RAM retained versus RAM discarded. `inferred` as to whether the SSD1677 silicon behaves the same way; **[DS]** for the SSD1683 itself.

Both flows still **omit** the `0x46`/`0x47` RAM pre-clear that the SSD1677's flow performs, despite having both commands. First frame after a cold start is therefore drawn against undefined RAM in whichever plane you did not write — and after deep sleep mode 2 that is *both* planes. `inferred` as to consequence.

---

## 8. Electrical

### 8.1 Absolute maximum ratings

**[DS]** §10, Table 10-1, p. 43.

| Symbol | Parameter | Rating | Unit |
|---|---|---|---|
| `VCI` | Logic supply voltage | **−0.5 to +6.0** | V |
| `VIN` / `VOUT` | Logic input / output | −0.5 to V<sub>DDIO</sub> + 0.5 | V |
| **`TOPR`** | Operating temperature | **−40 to +85** | °C |
| `TSTG` | Storage temperature | −65 to +150 | °C |

Notes: unused inputs to `VSS` or `VDDIO`; **unused outputs left open**; *"This device may be light sensitive"*; *"This device is not radiation protected."*

### 8.2 DC characteristics

**[DS]** §11, Table 11-1, pp. 43–44. Conditions `VSS = 0 V`, `VCI = 3.0 V`, `VDD = 1.8 V`, `TOPR = 25 °C`.

| Symbol | Parameter | Min | Typ | Max | Unit |
|---|---|---:|---:|---:|---|
| **`VCI`** | Operating voltage | **2.3** | 3.0 | 3.7 | V |
| `VDD` | Core | 1.7 | **1.8** | 1.9 | V |
| `VCOM_DC` | VCOM DC output | −3.0 | | −0.2 | V |
| `VGATE` | Gate output (`G0~G299`) | −20 | | +20 | V |
| `VGATE(p-p)` | Gate peak-to-peak | | | **40** | V |
| **`VSH1`** | Positive source 1 | **+8.6** | 15 | +17 | V |
| `VSH2` | Positive source 2 | +2.4 | 5 | +17 | V |
| **`VSL`** | Negative source | −17 | −15 | **−5.0** | V |
| `VPP` | OTP program voltage | 7.25 | **7.5** | 7.75 | V |
| `Islp_VCI` | Sleep mode | | **25** | **35** | µA |
| `Idslp_VCI1` | **Deep sleep 1** (RAM retained) | | **3** | **5** | µA |
| `Idslp_VCI2` | **Deep sleep 2** (RAM lost) | | **1** | **4** | µA |
| `Iopr_VCI` | Operating, `VCI = 3.0 V` | | **1000** | | µA |
| `VGH` | via Master Activation | 19.5 | 20 | 20.5 | V |
| `VIH` / `VIL` | Logic thresholds | 0.8 V<sub>DDIO</sub> | | 0.2 V<sub>DDIO</sub> | V |

Regulator capability **[DS]** Table 11-2, p. 44: `IVSH1`, `IVSH2`, `IVSL` **800 µA max**; `IVCOM` **100 µA max** — same as the SSD1680/1681 despite driving 2.3× the sources.

> ⚠ **This part sleeps three times worse than the SSD1680.** Deep sleep 1: **3 µA typ / 5 µA max** here against 1 µA typ / 3 µA max there; deep sleep 2: **1 µA / 4 µA** against 0.7 µA / 3 µA; sleep mode 25 µA typ against 20 µA. Bigger die, more leakage. For a battery design that budgeted from the SSD1680's numbers, that is a real difference. **[DS]** Table 11-1 p. 44 vs **[DS1680]** Table 11-1 p. 41.
>
> ⚠ **`VSL` max is −5.0 V here** against −9 V on the SSD1680/1681 — and unlike those parts, **the DC table and the feature list agree** (both say −5 to −17 V). The SSD1683 fixed the inconsistency its siblings carry.

### 8.3 AC — SPI timing

**[DS]** §12.1, Table 12-1, p. 45. `VDDIO − VSS = **2.3**–3.7 V`, `TOPR = 25 °C`, `CL = 20 pF`. **Fully populated**, unlike the [SSD1681](../ssd1681/README.md#83-ac---almost-entirely-tbd):

| Symbol | Parameter | Write | Read | Unit |
|---|---|---:|---:|---|
| **`fSCL`** | **SCL frequency (max)** | **20** | **2.5** | **MHz** |
| `tCSSU` | `CS#` low before first rising `SCLK` (min) | 60 | 100 | ns |
| `tCSHLD` | `CS#` low after last falling `SCLK` (min) | **60** | 50 | ns |
| `tCSHIGH` | `CS#` high between transfers (min) | 100 | 250 | ns |
| `tSCLHIGH` / `tSCLLOW` | Clock high / low (min) | 25 / 25 | 180 / 180 | ns |
| `tSISU` / `tSIHLD` | Data setup / hold, write (min) | 10 / 40 | — | ns |
| `tSOSU` / `tSOHLD` | Data valid / hold, read (typ) | — | 50 / 0 | ns |

All timings **20 % to 80 % of `VDDIO − VSS`**. The only numeric difference from the SSD1680 is `tCSHLD` write: **60 ns here, 65 ns there**.

> **Read is 8× slower than write.** Every diagnostic register in §6.2 is on the 2.5 MHz path.

---

## 9. Application circuit

**[DS]** §13, Table 13-1, p. 46 — essentially the SSD1680's, with the **0402 package option removed throughout**:

| Part | Value | Requirement |
|---|---|---|
| `C0`–`C1` | 1 µF | X5R/X7R, 6 V or 25 V |
| `C2`–`C7` | 1 µF | **0603/0805**, X5R/X7R, 25 V |
| `C8` (VCOM) | **1 µF** | **0603/0805**, X7R, 25 V |
| **`R1`** | **2.2 Ω** | **0603/0805**, 1 %, 0.05 W — the `RESE` sense resistor |
| `D1`–`D3` | Schottky | **MBR0530**: V<sub>R</sub> ≥ 30 V, I<sub>o</sub> ≥ 500 mA, **V<sub>F</sub> ≤ 430 mV** |
| `Q1` | NMOS | **Si1304BDL / NX3008NBK**: BV<sub>DSS</sub> ≥ 30 V, V<sub>gs(th)</sub> 0.9 V typ / 1.3 V max, **R<sub>ds(on)</sub> ≤ 2.1 Ω @ V<sub>gs</sub> = 2.5 V** |
| `L1` | **47 µH** | CDRH2D18 / LDNP-470NC, I<sub>o</sub> 500 mA max |
| `U1` | 0.5 mm ZIF | **24 pins, 0.5 mm pitch** |

The same caveats apply verbatim: values *"subject to change depending on panel loading"*, and *"Customer is required to review if the selected component value and part is suitable for their application."*

⚠ The SSD1680's **DC-bias constraint on `C8`** (*"Effective capacitance > 0.25 µF @ 18 V DC bias"*) is **not repeated here**, though the physics is unchanged. Treat it as still binding. `inferred`.

**`R1 = 2.2 Ω`, `L1 = 47 µH`, `MBR0530`, `Si1304BDL`** are constant across SSD1677, SSD1680, SSD1681 and SSD1683 — one boost topology for the whole family. See [`papermono/gaps-and-conflicts.md`](../../../devices/m5stack/papermono/gaps-and-conflicts.md) for what that single MOSFET physically does.

---

## 10. Caveats, errata and conflicts

| # | Issue | Evidence |
|---|---|---|
| **C1** | **⚠ The LUT is structurally incompatible with the SSD1680/SSD1681's** — 227 vs 153 bytes via `0x32`, **32 vs 48 phases**, per-colour LUTs vs numbered LUTs, **one global `FR` byte vs twelve**, `VS`/`TP` packed into one byte vs separate regions. And incompatible with the SSD1677's 105-byte / 40-phase engine. **"An SSD16xx driver" does not exist** | **[DS]** §6.7 p. 16; **[DS1680]** §6.7 p. 15; [SSD1677 §4.1](../ssd1677/README.md) |
| **C2** | **⚠ Temperature is 8-bit (1 °C) here, 12-bit (1/16 °C) on the SSD1680/1681.** `0x1A`/`0x1B` are one byte, TR entries two bytes. **The prose still refers to "MSByte bit D11"**, which does not exist, and one table row prints the °C value as `12B` where §6.9 says `127` | **[DS]** §6.8.3 p. 18, §6.9 p. 19, §6.11 p. 20, §7 p. 27. §5 |
| **C3** | **⚠ `0x21` byte `B` means something different.** `B[4]` = cascade enable here; `B[7]` = source output mode on the SSD1680. Same command, same parameter byte, unrelated function. Cascade also requires `CL` wired between master and slave | **[DS]** §7 p. 28; **[DS1680]** §7 p. 25 |
| **C4** | **⚠ `0x3C` `A[1:0]` is given two incompatible meanings on one page.** A line reading *"VBD Level Selection: 00b: VCOM ; 01b: VSH1; 10b: VSL; 11b: VSH2"* sits directly above the `A[1:0]` table that says `00`=LUT0 … `11`=LUT3. The `A[2]` GS-transition-control bit present on the SSD1680 is also gone. **Unresolved** — use `A[7:6]=01` fixed level with `A[5:4]` if you need a deterministic border | **[DS]** §7 p. 34; **[DS1680]** §7 p. 31 |
| **C5** | **`0x16` programs a password into "register `0x4C`", and `0x4C` appears nowhere else in the document.** The waveform store has a protection mechanism this datasheet does not describe | **[DS]** §7 p. 27 |
| **C6** | **Table 6-4 (3-colour RAM→LUT mapping) has only three rows** — the `R=1, BW=1` combination is unlisted. The SSD1680 defines it as Red/LUT3=LUT2 | **[DS]** §6.5 p. 13; **[DS1680]** p. 13 |
| **C7** | **Waveform registers are last-writer-wins, explicitly.** A partial MCU write after an OTP load replaces only what you wrote — including rail voltages if you touch `0x04`. This is how a waveform change silently changes `VGH`/`VSH1`/`VSH2`/`VSL`/`VCOM` | **[DS]** §6.7 p. 16 |
| **C8** | **Two deep-sleep modes, and §9.2 gives the concrete parameter `0x10` `{0x03}` for mode 2.** Relevant to the open [SSD1677 §7-C5](../ssd1677/README.md#7-caveats-errata-and-conflicts) question about the undocumented `{0x01}`: on this part `01` and `03` are both legal and differ in RAM retention. `inferred` for the SSD1677 | **[DS]** §7 p. 25, §9.2 p. 42 |
| **C9** | **⚠ Deep-sleep current is ~3× the SSD1680's** (3 µA typ / 5 µA max mode 1). Do not inherit a power budget across the family | **[DS]** Table 11-1 p. 44 |
| **C10** | **`VSH1` cannot go below 8.6 V** on this part, against 2.4 V on the SSD1680/1681. A source-voltage table copied across the family will be rejected at the low end | **[DS]** §2 p. 5, Table 11-1 p. 43 |
| **C11** | **Frame rate tops out at 125 Hz**, against 200 Hz on the SSD1680/1681 — with **one global `FR` byte** instead of per-group control | **[DS]** §2 p. 5, Figure 6-6 p. 16 |
| **C12** | **`0x22` bit definitions unpublished**, as everywhere in the family. Twelve composite values tabulated; copy one, do not compose one. Note the labels changed: "display mode 1/2" here means **3-colour / black-white** | **[DS]** §7 p. 29 |
| **C13** | **Three commands defer to material that is not public** — `0x09` initial code setting (*"Application Notes"*), `0x34` CRC, `0x39` (*"EXACTLY follow the reference code sequences"*). Plus `0x16`'s password. **OTP programming is not achievable from this document alone** | **[DS]** pp. 26, 27, 32, 33 |
| **C14** | **OTP contents unpublished; out-of-range temperature silently prevents refresh.** 24 WS/TR slots, burned by the panel maker, disclosed by nobody. `0x2D` is the only in-system probe | **[DS]** §6.9 p. 19 |
| **C15** | **No panel-break diagnostic.** Present in the SSD1680's feature list, absent here — confirmed absent from the command table by census | **[DS]** §2 p. 5, §7 census |
| **C16** | **`0x0F` Gate Scan Start Position is not available.** No §8 entry, no command-table row | **[DS]** §7 census, §8 pp. 37–40 |
| **C17** | **The PDF's `Title` metadata says `SSD1780`** — a part number that does not appear anywhere in the document body. This has already caused a mis-catalogue in this repository; see §11 | `executed-success` — `pdfinfo` |
| **C18** | **Copyright line says 2020 on a document dated Jan 2021**, and *"Advance Information"* with a single revision in five years. Provisional documentation | **[DS]** cover, p. 2 |
| **C19** | **The DC-balance hazard is not stated.** Real for the family; §4.1's override semantics make partial waveform writes an easy way to lose it | **[INF]**; [SSD1677 §4.4](../ssd1677/README.md#44--the-dc-balance-hazard) |

---

## 11. Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/ssd1683-rev1.0-jan2021.pdf` | 3 931 534 | `77c188ba55b1b81129f8c0557f845fde25ca97d73ee86ed1ba907ea87a0b5e9c` | **SSD1683 datasheet, "Advance Information", Rev 1.0, Jan 2021.** PDF 1.5, A4, **49 pages**. ⚠ `Title` **`SSD1780`**, `Author` **`ivanl`**, Creator **Microsoft® Word 2016**, Producer **PDFill PDF Editor 15.0**, CreationDate **2021-01-26** (matching the stated release date), ModDate **2021-04-20**. `Optimized: no`, `Tagged: yes` |

**Text-layer validation — `executed-success`.** `pdftotext -layout` output checked against the cover block (`SOLOMON SYSTECH` / `SEMICONDUCTOR TECHNICAL DATA` / `Advance Information`), the revision-history table and the numbered contents list. Mechanically: **for all 49 pages the PDF page index equals the printed footer `SSD1683 Rev 1.0 P n/49 Jan 2021`**, and 49 == the PDF page count. No dropped pages, no glyph subsetting, no code-point offset. Every value above comes from that validated layer.

### ⚠ The `SSD1780` metadata, and a correction to an existing record

`pdfinfo` reports this file's `Title` as **`SSD1780`**. **No page of the document says SSD1780**; all 49 footers and the cover say SSD1683, and the revision history is headed *"IC Revision history of SSD1683 Specification"*. The `Title` is a stale Word document property.

This has already cost this repository once. [`components/ultrachip/uc8279/README.md`](../../ultrachip/uc8279/README.md) records, from a 2026-09-11 Crystalfontz document-id probe over ids 512–523, that the returned documents included *"FocalTech, D-FT3267, **SSD1780**, ST7567S/A, CH13620 and Hynitron CST816D"*. **Verified 2026-09-20 (`executed-success`): Crystalfontz's own catalogue entry for id 514 is `{"id":514,"name":"SSD1683","version":"1.0","summary":"400 Source x 300 Gate Red/Black/White Active Matrix EPD Display Driver with Controller"}`.** The probe was reading the PDF's `Title` rather than the catalogue name. **"SSD1780" is not a part; it is this document.** The UC8279 record's conclusion — that no UC8279 was found — is unaffected and stands.

### A second, byte-different copy exists and was identified

Crystalfontz serves this datasheet at `https://www.crystalfontz.com/controllers/Solomon%20Systech/SSD1683/514/` — **1 877 699 bytes, SHA-256 `f40921acc7cabb8330dc08204d97822c216c44b9724bef34a5996835724b6152`**, fetched and hashed 2026-09-20 (`executed-success`). **Not a different revision**: identical `Title`/`Author`/`Creator`/`Producer`, identical `CreationDate` (2021-01-26), identical 49 pages, and **whitespace-normalised `pdftotext` output is byte-identical to the copy retained here**. The difference is `Optimized: yes` and a much later `ModDate` (2025-07-21) — a re-optimised derivative, ~2.1× smaller. **Only the larger, unoptimised copy is retained**; the Crystalfontz hash is recorded so a future agent can identify that file on sight rather than re-deriving the comparison. A deliberate departure from "keep both", justified by *proven* rather than assumed equivalence.

**Provenance of the retained copy is incomplete.** It arrived as `ssd1683.pdf` in a 2026-09-11 scratch batch. Given its `ModDate` (2021-04-20) predates Crystalfontz's optimisation pass, it is **not** the Crystalfontz copy, but **no URL was recorded by the acquiring session and none was recovered.** Recorded as `unknown` rather than guessed. The Crystalfontz URL above is a **verified working reacquisition path** for an equivalent document; reacquisition status **`automatic`**.

**Licence.** Third-party (Solomon Systech) copyright — *"Copyright © 2020 Solomon Systech Limited"* on the cover. **No per-page confidentiality footer.** No redistribution terms stated. Redistribution status **`unknown`**; disposition **`repository`**.

---

## 12. Authoritative sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | SSD1683 — 400 Source × 300 Gate Red/Black/White Active Matrix EPD Display Driver with Controller | **Solomon Systech Limited** | primary (via unrecorded mirror) | datasheet | `artifacts/ssd1683-rev1.0-jan2021.pdf`; upstream URL **unknown** | 2026-09-11 (acquired), 2026-09-20 (verified, filed) | **Rev 1.0, Jan 2021 — "Advance Information"** | §1, §3–§10 |
| S-2 | Same document, Crystalfontz-optimised copy | Solomon Systech, mirrored by **Crystalfontz America** | credible mirror | datasheet | `https://www.crystalfontz.com/controllers/Solomon%20Systech/SSD1683/514/` | **2026-09-20** | Rev 1.0, Jan 2021 | §11 — working reacquisition path; content equivalence proven |
| S-3 | Crystalfontz controller catalogue | Crystalfontz America | credible mirror | catalogue (embedded JSON) | `https://www.crystalfontz.com/controllers/` | **2026-09-20** | undated | §11 — that id **514** is catalogued as **SSD1683 v1.0**, correcting the "SSD1780" reading in the UC8279 record |
| S-4 | SSD1680 datasheet Rev 0.14 | Solomon Systech | primary | datasheet | [`../ssd1680/artifacts/ssd1680-rev0.14-jun2019.pdf`](../ssd1680/README.md) | 2026-09-20 | Rev 0.14, Jun 2019 | every **[DS1680]** comparison |
| S-5 | PaperMono gaps and conflicts | this repository | — | record | [`devices/m5stack/papermono/gaps-and-conflicts.md`](../../../devices/m5stack/papermono/gaps-and-conflicts.md) | 2026-09-20 | pass of 2026-09-11 | §2 — the in-repo consumer, and the 227+6-byte claim this record corrects in detail |
| S-6 | UC8279 component record | this repository | — | record | [`../../ultrachip/uc8279/README.md`](../../ultrachip/uc8279/README.md) | 2026-09-20 | pass of 2026-09-11 | §11 — the "SSD1780" probe result now explained |
| S-7 | SSD1677 component record | this repository | — | record | [`../ssd1677/README.md`](../ssd1677/README.md) | 2026-09-20 | pass of 2026-09-01 | §4.5, §7, §10 — DC balance and the deep-sleep `0x01` question |

---

## 13. Related

- [**SSD1680**](../ssd1680/README.md) — 176 × 296. The family's reference command set; read it for shared semantics
- [**SSD1681**](../ssd1681/README.md) — 200 × 200, and a worked example of an inherited-defect datasheet
- [**SSD1677**](../ssd1677/README.md) — 960 × 680, **the only family member fitted on hardware documented here**
- [**SSD7317**](../ssd7317/README.md) — unrelated OLED + in-cell touch part; filed alongside because it arrived in the same misnamed batch
- [**Vendor sourcing guide — Solomon Systech**](../../../vendors/solomon-systech/README.md) — ⚠ **§2**: why a Solomon Systech PDF's filename and its `Title` metadata are both untrustworthy
- [**UltraChip UC8179**](../../ultrachip/uc8179/README.md) · [**UC8279**](../../ultrachip/uc8279/README.md) — the competing controller family
- [**Guide — e-paper displays**](../../../guides/hardware/e-paper-displays.md)
