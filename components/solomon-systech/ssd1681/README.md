# Solomon Systech SSD1681

- **Category:** active-matrix EPD (e-paper) display driver **with controller** — source/gate drivers, on-chip booster and regulators, oscillator, dual display RAM, programmable waveform engine, OTP waveform store, temperature sensing, SPI MCU interface
- **Package:** **gold-bump die only** (COG). No packaged part exists.
- **Document status:** **"Product Preview", Rev 0.13, Jun 2019** — four revisions (0.10 → 0.13, 09-May-19 → 05-Jun-19), **every one of which changed only the application-circuit component table**
- **Research status:** full datasheet retained in `artifacts/`; text layer **validated page-by-page** (§10). **No hardware, no driver source and no board was examined.** **Reference-only** — see §2.
- **Retrieved / written:** 2026-09-20

The **200 × 200** member of the SSD16xx family — the controller behind essentially every 1.54-inch SPI e-paper module on the market. Not fitted on any device documented in this repository.

> ⚠ **Read §3 before you trust a number in this document.** The SSD1681 datasheet was produced by editing the SSD1680's, and **several values were not updated**. Two of them are the RAM window power-on defaults, which are wrong for a 200 × 200 part.

---

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[DS]** | Stated in `artifacts/ssd1681-rev0.13-jun2019-crystalfontz-mirror.pdf`, cited by section or **PDF page number** (which equals the printed footer page — proven in §10) | `not-tested` — vendor claim reproduced; nothing measured |
| **[DS1680]** | The [SSD1680 datasheet](../ssd1680/README.md), cited for comparison | `not-tested` |
| **[CF]** | Crystalfontz controller catalogue and document fetch, performed live 2026-09-20 | `executed-success` |
| **[INF]** | Inference | `inferred` |

**Nothing here was verified on hardware.** Where this document contradicts itself, both readings are recorded (§3, §8); neither is resolved by preference.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Solomon Systech Limited** | **[DS]** cover, footers |
| Part | **`SSD1681`** | **[DS]** cover |
| Document title, verbatim | **"200 Source x 200 Gate Red/Black/White — Active Matrix EPD Display Driver with Controller"** | **[DS]** cover |
| Document status, verbatim | **"Product Preview"** — "This document contains information on a product under development. Solomon Systech reserves the right to change or discontinue this product without notice." | **[DS]** cover |
| Revision / date | **Rev 0.13**; cover footer says **May 2019**, every other page footer and the revision history say **Jun 2019** | **[DS]** p. 1 vs pp. 2–41 |
| Revision history | 0.10 Initial Release (09-May-19) · 0.11 *"Revised component table and remarks"* (24-May-19) · 0.12 *"Revised component table, added 0402 and criteria for resistor R1"* (28-May-19) · **0.13 *"Revised component table"* (05-Jun-19)** | **[DS]** p. 2 |
| Ordering parts | **`SSD1681Z`** (gold bump die, **bump face up**) and **`SSD1681Z8`** (**bump face down**). Both: waffle pack, die thickness **300 µm**, bump height **12 µm** | **[DS]** §3, Table 3-1, p. 6 |
| Maximum geometry | **200 source outputs · 200 gate outputs · 1 VCOM · 1 VBD** ⇒ max **200 × 200**. **No cascade mode** — §3.2 | **[DS]** §1 p. 5, §5 Table 5-4 p. 9 (`S[199:0]`, `G[199:0]`) |
| Colour capability | **Red / Black / White** — two RAM planes, `200 × 200` bits each | **[DS]** §2 p. 5 |
| MCU interface | **SPI only** — 4-wire (8-bit) or 3-wire (9-bit), pin-selected by `BS1` | **[DS]** §6.1.1 Table 6-1, p. 10 |
| Copyright line | *"Copyright © 2019 Solomon Systech Limited"* | **[DS]** cover |
| ⚠ Marking verified? | **No.** No unit inspected; identification rests on the document alone | **[INF]** |

---

## 2. Used By — nothing here, and why it was kept

**No device documented in this repository is known to carry an SSD1681.** No schematic, firmware image, driver source or vendor statement in this tree names it as a fitted part. That is an **absence of evidence**, not a claim that none exists — the part is one of the most common e-paper controllers in the world.

It earns its place for three reasons:

1. **It is already cited by an existing record.** [`devices/m5stack/papermono/gaps-and-conflicts.md`](../../../devices/m5stack/papermono/gaps-and-conflicts.md) cites *"SSD1681 (Rev 0.13, p.22)"* — **this file, this page** — as one of three siblings that decode the SSD1677's opaque `0x0C` Booster Soft-start Control into driving-strength / minimum-off-time / per-phase-duration bit fields. Same record calls the SSD1681's LUT layout *"the familiar 153-byte SSD1681 LUT"*; §4.1 below confirms that number from the primary document.
2. **It supplies the missing half of an SSD1677 caveat.** [SSD1677 §7-C5](../ssd1677/README.md#7-caveats-errata-and-conflicts) records that two independent vendors write the *undocumented* deep-sleep parameter `0x01`. On the SSD1681 (and SSD1680, and SSD1683) **`01` is documented: Deep Sleep Mode 1, the RAM-retaining variant** (§5.4). That does not prove the SSD1677 behaves the same way, but it is a far better hypothesis than "shared typo", and it is testable.
3. **It is a worked example of a datasheet defect class** that this repository keeps hitting: a document derived by editing another part's document, with values left behind (§3). The skill's own guidance — *"Read a document's own metadata … datasheets derived by editing another part's document"* — is exactly this case, and here it is provable rather than suspected.

---

## 3. ⚠ This datasheet was derived from the SSD1680's, and not all of it was updated

This is the most important thing in the record. Three defects, all verifiable against the primary document, two of them capable of breaking a driver.

### 3.1 The RAM window power-on defaults are the SSD1680's

**[DS]** §7, `0x44` and `0x45`, p. 31:

| Register | SSD1681 states | Implies | Correct for a 200 × 200 part |
|---|---|---|---|
| `0x44` **`XEA`** | **POR `= 15h`** (21) | 22 byte-units × 8 = **176 sources** | `18h` (24) ⇒ 25 bytes ⇒ 200 |
| `0x45` **`YEA`** | **POR `= 127h`** (295) | **296 gate lines** | `0C7h` (199) ⇒ 200 |

**176 × 296 is the SSD1680's geometry, verbatim** **[DS1680]** p. 31. It is not reachable on a part with `S[199:0]` and `G[199:0]`.

That the document was *partly* updated is what proves the defect rather than merely suggesting it: `0x01` Driver Output Control **was** corrected — it reads **`A[8:0] = C7h [POR], 200 MUX`**, and its prose correctly describes `SM=1` as `G0, G2, G4 … G198, G1, G3, … G199` and `TB=1` as `G199 → G0` **[DS]** p. 20. The MUX default was fixed; the window defaults were missed.

> **Practical consequence.** Any driver that relies on power-on window defaults instead of writing `0x44`/`0x45` explicitly is relying on a number this datasheet gets wrong. **Always set the window.** What the silicon actually powers up with is **unknown** — neither reading is verified, and this is `not-tested`.

### 3.2 `0x21` describes a `B` byte that has no bit row and no definition

**[DS]** §7, `0x21` Display Update Control 1, p. 25. The description reads *"A[7:0] = 00h [POR], **B[7:0] = 00h [POR]**"* and then defines only `A[7:4]` (Red RAM option) and `A[3:0]` (BW RAM option). **There is no `B` data row in the bit table and no statement of what `B` does.**

On the SSD1680 the same command has a second row and `B[7]` is **Source Output Mode** — `0` = sources `S0`–`S175`, `1` = `S8`–`S167` **[DS1680]** p. 25. On a 200-source part that centring window would be a different range, and the SSD1681 does not say what it is — or whether the byte exists at all. **Unresolved.** Sending one byte is the conservative choice; sending two is what the description implies. Neither is verified.

### 3.3 The feature list under-reports the silicon its own command table exposes

The §2 feature list (p. 5) **omits**: partial update, auto write RAM for regular patterns, built-in CRC checking, driving-voltage (HV) ready detection, panel break diagnostic, and external/internal OTP burn voltage — all of which the SSD1680's list carries.

But a **complete census of the SSD1681's own §7 command table** (`executed-success`, all 49 command rows extracted) returns a list that is **identical to the SSD1680's, command for command** — including `0x46`/`0x47` (auto write RAM), `0x34`/`0x35` (CRC calculation / CRC status read), `0x14` (HV Ready Detection), `0x2F` bit `A[5]` (HV-ready flag) and `0x39` (internal OTP programming voltage).

So the features are there in the register map and merely absent from the marketing page. The one feature genuinely absent is **cascade mode** — see §3.4. **[INF]** as to why the list is short; the command census is **[DS]**.

### 3.4 `M/S#` and `CL` exist as pins but cascade mode does not

**[DS]** §5 Table 5-2, p. 8. `M/S#` is described as *"Master and Slave selection pin"* and then given exactly one instruction: ***"The M/S# pin should be connected to VDDIO."*** `CL` is *"the clock signal pin and should be left open."* There is **no §6.12 Cascade Mode section** — the functional-block chapter runs §6.11 TR format → **§6.12 VCI Detection** → §6.13 HV Ready Detection, where the SSD1680 has §6.12 Cascade → §6.13 VCI → §6.14 HV.

The SSD1680's `BUSY` pin description also carries *"In the cascade mode, the BUSY pin of the slave chip should be left open"*; the SSD1681's does not. So the vestigial pin names were kept, the mode was removed, and the surrounding text was cleaned up — the reverse of §3.1, where the text was kept and the values were not.

**Tie `M/S#` to `VDDIO` and leave `CL` open.** Tying `M/S#` low on an SSD1680 disables its oscillator, booster and regulator; what it does here is **undocumented**.

---

## 4. Waveforms, RAM and OTP

The SSD1681's waveform engine, RAM mapping, OTP layout and temperature machinery are **identical to the SSD1680's** as documented, and are set out in detail in the [SSD1680 record §5](../ssd1680/README.md#5-waveforms-otp-versus-external-lut). The part-specific numbers, confirmed from *this* document:

### 4.1 Waveform setting — **159 bytes**, `0x32` writes **153**

**[DS]** §6.7, p. 15, and §7 `0x32`, p. 29:

| WS byte | Content | Written by |
|---:|---|---|
| **0–152** | `VS[nX-LUTm]`, `TP[nX]`, `RP[n]`, `SR[nXY]`, `FR[n]` | **`0x32` — "[153 bytes]"** |
| 153 | `EOPT`, option for LUT end | `0x3F` |
| 154 | Gate level | `0x03` |
| 155–157 | Source levels | `0x04` |
| 158 | VCOM level | `0x2C` |

> ⚠ **One real difference from the SSD1680, and it is in the §6.7 text.** The SSD1681 lists WS bytes 0–152 as *"VS[nX-LUTm], TP[nX], RP[n], SR[nXY] **and FR[n]**"* — **`XON[nXY]` is not named**, and the SSD1681's feature list likewise omits the `XON` bullet that the SSD1680 carries (*"XON: All Gate On Selection for each phase A,B and phase C,D"*). The byte-map figure still occupies the same 153 bytes. Whether bytes 150–152 are `XON` bits, reserved, or something else on this part is **not stated**. `unresolved`. **[DS]** §2 p. 5, §6.7 p. 15 vs **[DS1680]** same sections.

Engine: **12 groups × 4 phases = 48 phases**; `TP` 0–255 frames (`0` skips); `RP` and `SR` encoded `n ⇒ n+1` for 1–256 repeats; per-group `FR` 0–7; `VS` 2 bits per phase per LUT (`00` VSS/DCVCOM, `01` VSH1/VSH1+DCVCOM, `10` VSL/VSL+DCVCOM, `11` VSH2 / VCOM **N/A**). **[DS]** §6.6, Table 6-6, pp. 13–14.

### 4.2 OTP — **36 WS + 36 TR**

**[DS]** §6.10, p. 18: *"The OTP memory can store **36 sets** of waveform LUT settings (WS), **36 sets** of temperature range (TR), VCOM value, display mode selection, waveform version and user ID."* WS0–WS35 at 159 bytes each, then TR0–TR35 at 3 bytes each.

Temperature value: **12-bit two's complement, °C = value / 16** **[DS]** §6.8.3, p. 16. TR format: `temp_L[7:0]`, `temp_H[3:0]`:`temp_L[11:8]`, `temp_H[11:4]` **[DS]** §6.11, p. 18.

Selection **[DS]** §6.9, p. 17: search TR0 → TR35 in sequence, `lower < sensed ≤ upper`, **last match wins**; the worked example selects WS7 for 34 °C over the equally-matching TR6.

> ⚠ **Same silent-failure mode as the rest of the family, verbatim:** *"Please ensure the temperature range covers whole range of application temperatures, **display will not be updated if no suitable temperature range matches the sensed temperature**."* **[DS]** p. 17. No status bit reports it. `0x2D` (OTP Register Read) returning the **4-byte waveform version** is the only in-system probe of what was actually programmed.

### 4.3 RAM → colour → LUT

**[DS]** §6.5, Tables 6-4/6-5, p. 13 — identical to the SSD1680: in 3-colour mode `R=0,BW=0` Black/LUT0, `0,1` White/LUT1, `1,0` and `1,1` Red/LUT2 (LUT3 = LUT2); in B/W mode LUT2 = LUT0 and LUT3 = LUT1. LUT4 is reachable only as the border waveform via `0x3C`.

### 4.4 ⚠ DC balance

**This datasheet does not mention it.** Writing your own LUT with `0x32` makes you responsible for net-zero charge delivery; failing at it degrades the ink **irreversibly**. The OTP path cannot get it wrong. Documented for this family by M5Stack and DKE on the SSD1677 — [SSD1677 §4.4](../ssd1677/README.md#44--the-dc-balance-hazard). Recorded here as a family-level hazard, `inferred` for this part.

---

## 5. Command set — what differs from the SSD1680

The command **list** is identical (§3.3). The [SSD1680 record §6](../ssd1680/README.md#6-command-set) is therefore the reference for every command's semantics. Recorded here: the values that are **part-specific**, plus the places the two documents diverge.

### 5.1 Part-specific POR values

| Cmd | SSD1681 POR **[DS]** | Note |
|---|---|---|
| **`0x01`** Driver Output Control | **`A[8:0] = C7h` ⇒ 200 MUX.** `B[2:0] = 000`: `GD=0`, `SM=0` (left/right interlaced `G0,G1,G2…199`), `TB=0` (`G0→G199`). `SM=1` ⇒ `G0,G2,G4…G198,G1,G3,…G199` | ✅ **correctly updated** for this part |
| `0x03` Gate Driving Voltage | `A[4:0] = 00h` ⇒ **VGH 20 V**; table `03h`=10 V … `17h`=20 V | same table as SSD1680, **including the duplicated `07h`/`08h` rows** |
| `0x04` Source Driving Voltage | `A = 41h` ⇒ VSH1 15 V · `B = A8h` ⇒ VSH2 5 V · `C = 32h` ⇒ VSL −15 V. Bit 7 selects the range: `1` ⇒ 2.4–8.8 V (100 mV steps), `0` ⇒ 9–17 V (200 mV). **`VSH1 >= VSH2`** | identical |
| `0x0C` Booster Soft-start | **4 bytes**, POR **`8B 9C 96 0F`**; `[6:4]` driving strength 1–8, `[3:0]` min `GDR` off-time (`0100`=2.6 … `1111`=16.5, `0000`–`0011` **NA**), `D[5:0]` per-phase duration 10/20/30/40 ms | identical — **this is the table §2 cites** |
| `0x11` Data Entry Mode | `A[2:0] = 011` ⇒ Y inc, X inc, counter advances in X | identical |
| **`0x44`** RAM X start/end | **POR `XEA = 15h` — ⚠ wrong, see §3.1.** `A[5:0]`/`B[5:0]`, **units of 8 pixels** | ❌ **not updated** |
| **`0x45`** RAM Y start/end | **POR `YEA = 127h` — ⚠ wrong, see §3.1.** `A[8:0]`/`B[8:0]`, units of **gate lines** | ❌ **not updated** |
| `0x2C` VCOM | `00h` [POR]; `08h` = −0.2 V … `78h` = −3.0 V | identical |
| `0x3C` Border Waveform | **`C0h` [POR] = VBD HiZ.** `A[7:6]`: `00` GS transition · `01` fixed level (`A[5:4]` VSS/VSH1/VSL/VSH2) · `10` VCOM · `11` HiZ. `A[1:0]` selects LUT0–LUT3 | identical |
| `0x3F` `EOPT` | **`02h` [POR]**, with only `22h` (Normal) and `07h` (keep previous source level) defined — **`02h` is not one of them** | identical defect to SSD1680 |
| `0x22` Display Update Control 2 | **`FFh` [POR]**; twelve values `80 01 C0 03 91 99 B1 B9 C7 CF F7 FF`, bit definitions **not published** | identical |
| `0x15` VCI Detection | `A[2:0] = 100` [POR] ⇒ **2.3 V** threshold; `011`–`111` ⇒ 2.2–2.6 V | identical |
| `0x29` VCOM Sense Duration | `9h` ⇒ **10 s**; duration = `(A[3:0]+1)` s | identical |
| `0x46` / `0x47` Auto Write RAM | present in the command table despite being absent from the feature list (§3.3) | — |

### 5.2 `0x0F` does not exist here

The SSD1680 documents **Gate Scan Start Position (`0Fh`)** in its §8.2 — a command that lets a 296-gate controller drive a shorter panel by offsetting which RAM row lands on the first gate. **The SSD1681 has no §8 Command Description chapter at all**: its chapter 8 is *Operation Flow and Code Sequence*, and a full census of its §7 command table (`executed-success`) finds **no `0x0F` row**. On a square 200 × 200 part the need is smaller, but if you are driving a short panel from an SSD1681, this escape hatch is not documented as available.

### 5.3 Deep sleep — **two** modes

**[DS]** §7 `0x10`, p. 23:

| `A[1:0]` | Mode | Current **[DS]** Table 10-1, p. 36 |
|---|---|---|
| `00` | Normal [POR] | — |
| **`01`** | **Deep Sleep Mode 1** — RAM retained, not accessible | **1 µA typ**, max **TBD** |
| **`11`** | **Deep Sleep Mode 2** — RAM **not** retained | **0.7 µA typ**, max **TBD** |

*"To exit Deep Sleep mode, user required to send HWRESET to the driver."* `0x12` SWRESET resets everything **except `R10h`**, and leaves RAM untouched. **[DS]** p. 23.

### 5.4 Status and diagnostics

`0x2F` Status Bit Read [POR `0x01`]: `A[5]` HV-ready, `A[4]` VCI-detect, `A[2]` busy, `A[1:0]` chip ID [POR `01`]. ⚠ **`A[5]`/`A[4]` are invalid after reset until `0x14` and `0x15` have been issued.** `0x14` HV Ready Detection takes a cool-down `10 ms × (n+1)` and a loop count, max `10 ms × (n+1) × m`; `A = 00h` is one-shot. Both require `CLKEN=1` and `ANALOGEN=1`. **[DS]** §7 p. 24.

`0x2D` OTP Register Read (11 bytes: VCOM OTP selection, VCOM register, 5 bytes display mode, **4 bytes waveform version**) · `0x2E` 10-byte User ID · `0x34`/`0x35` CRC calculation and 16-bit status. **[DS]** pp. 28–29.

> ⚠ `0x34` defers to *"the SSD1681 application note"*, `0x09` to *"Application Notes of Initial Code Setting"*, and `0x39` to *"the reference code sequences"*. **None of the three is public and none was located.** OTP *programming* is not achievable from this document alone.

---

## 6. Reference operation flow

**[DS]** §8.1, Figure 8-1, p. 34 — identical in structure to the SSD1680's, and like it, **it omits the `0x46`/`0x47` RAM pre-clear** that the SSD1677's flow performs:

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

Note step 3 writes `0x44`/`0x45` explicitly, which is exactly what neutralises §3.1's bad defaults — **provided you compute the values rather than copy the datasheet's**.

---

## 7. Application circuit

**[DS]** §12, Table 12-1, p. 38. The component table is the *only* thing the 0.10 → 0.13 revisions ever changed, so it is the part of this document with the most vendor attention:

| Part | Value | Requirement |
|---|---|---|
| `C0`–`C1` | 1 µF | X5R/X7R, 6 V or 25 V |
| `C2`–`C7` | 1 µF | 0402/0603/0805, X5R/X7R, **25 V** |
| `C8` (VCOM) | **1 µF** | 0402/0603/0805, X7R, 25 V |
| **`R1`** | **2.2 Ω** | **0402**/0603/0805, **1 %**, ≥ 0.05 W — the `RESE` sense resistor |
| `D1`–`D3` | Schottky | **MBR0530**: V<sub>R</sub> ≥ 30 V, I<sub>o</sub> ≥ 500 mA, **V<sub>F</sub> ≤ 430 mV** |
| `Q1` | NMOS | **Si1304BDL / NX3008NBK**: BV<sub>DSS</sub> ≥ 30 V, V<sub>gs(th)</sub> 0.9 V typ / 1.3 V max, **R<sub>ds(on)</sub> ≤ 2.1 Ω @ V<sub>gs</sub> = 2.5 V** |
| `L1` | **47 µH** | CDRH2D18 / LDNP-470NC, I<sub>o</sub> 500 mA max |
| `U1` | 0.5 mm ZIF | **24 pins, 0.5 mm pitch** |

⚠ **`C8` differs from the SSD1680's.** The SSD1680 allows **0.47 µF or 1 µF** with the binding constraint stated as *"Effective capacitance > 0.25 µF @ 18 V DC bias"* and restricts the package to **0603/0805**; the SSD1681 specifies **1 µF, 0402/0603/0805, with no DC-bias note**. Given that revisions 0.11–0.13 exist purely to adjust this table, the SSD1681's is the more deliberate statement for this part — but the DC-bias physics has not changed, and a 0402 1 µF X7R 25 V part can lose most of its capacitance at 18 V bias. **Check effective capacitance under bias regardless of what the table permits.** `inferred`.

The revision history also records that **0.12 "added 0402 and criteria for resistor R1"** — i.e. the 1 % tolerance on `R1` was added *after* initial release. Anyone working from a Rev 0.10 copy has a looser sense resistor spec. **[DS]** p. 2.

---

## 8. Electrical — and how much of it is `TBD`

### 8.1 Absolute maximum ratings

**[DS]** §9, Table 9-1, p. 35.

| Symbol | Parameter | Rating | Unit |
|---|---|---|---|
| `VCI` | Logic supply voltage | **−0.5 to +6.0** | V |
| `VIN` / `VOUT` | Logic input / output | −0.5 to V<sub>DDIO</sub> + 0.5 | V |
| **`TOPR`** | Operating temperature | **−40 to +85** | °C |
| `TSTG` | Storage temperature | −65 to +150 | °C |

Notes: unused inputs to `VSS` or `VDDIO`; **unused outputs left open**; *"This device may be light sensitive"*; *"This device is not radiation protected."*

### 8.2 DC characteristics

**[DS]** §10, Table 10-1, pp. 35–36. Conditions `VSS = 0 V`, `VCI = 3.0 V`, `VDD = 1.8 V`, `TOPR = 25 °C`.

| Symbol | Parameter | Min | Typ | Max | Unit |
|---|---|---:|---:|---:|---|
| `VCI` | Operating voltage | **2.2** | 3.0 | **3.7** | V |
| `VDD` | Core | 1.7 | **1.8** | 1.9 | V |
| `VCOM_DC` | VCOM DC output | **−3.0** | | **−0.2** | V |
| `VGATE` | Gate output (`G0~G199`) | −20 | | +20 | V |
| `VGATE(p-p)` | Gate peak-to-peak | | | **40** | V |
| `VSH1` / `VSH2` | Positive source | +2.4 | 15 / 5 | +17 | V |
| `VSL` | Negative source | **−17** | −15 | **−9** | V |
| `VPP` | OTP program voltage | 7.25 | **7.5** | 7.75 | V |
| `Islp_VCI` | Sleep mode | | **20** | **TBD** | µA |
| `Idslp_VCI1` | Deep sleep 1 (RAM retained) | | **1** | **TBD** | µA |
| `Idslp_VCI2` | Deep sleep 2 (RAM lost) | | **0.7** | **TBD** | µA |
| `Iopr_VCI` | Operating, `VCI = 3.0 V` | | **1000** | | µA |
| `VGH` | via Master Activation | 19.5 | 20 | 20.5 | V |
| `VIH` / `VIL` | Logic thresholds | 0.8 V<sub>DDIO</sub> | | 0.2 V<sub>DDIO</sub> | V |

Regulator capability **[DS]** Table 10-2, p. 36: `IVSH1`, `IVSH2`, `IVSL` **800 µA max**; `IVCOM` **100 µA max**.

⚠ Same internal disagreement as the SSD1680: the **feature list says `VSL: −5 V to −17 V`** while **Table 10-1 bounds it `−17` to `−9 V`**. **[DS]** pp. 5, 35.

> ⚠ **Every current *maximum* is `TBD`.** Typicals are given; the guaranteed limits are not. For a battery-powered design whose whole premise is a sub-microamp sleep, **this document does not give you a number you can budget against.** That is a Product-Preview gap, not a transcription error.

### 8.3 AC — ⚠ almost entirely `TBD`

**[DS]** §11.1, Table 11-1, p. 37. Conditions `VDDIO − VSS = 2.2–3.7 V`, `TOPR = 25 °C`, `CL = 20 pF`.

| Symbol | Write mode | Read mode |
|---|---:|---:|
| **`fSCL`** max | **20 MHz** | **2.5 MHz** |
| `tCSSU` | **TBD** | **TBD** |
| `tCSHLD` | **TBD** | **TBD** |
| `tCSHIGH` | **TBD** | **TBD** |
| `tSCLHIGH` / `tSCLLOW` | **TBD** / **TBD** | **TBD** / **TBD** |
| `tSISU` / `tSIHLD` | **TBD** / **TBD** | — |
| `tSOSU` / `tSOHLD` | — | 50 ns / 0 ns (typ) |

**Fourteen of sixteen timing parameters are `TBD`.** Only the two clock ceilings and the two read-data typicals carry values. If you need setup/hold numbers for this part, **the SSD1680's are the nearest published figures** (write: `tCSSU` 60, `tCSHLD` 65, `tCSHIGH` 100, `tSCLHIGH`/`tSCLLOW` 25/25, `tSISU`/`tSIHLD` 10/40 ns — **[DS1680]** p. 42) and borrowing them is **`inferred`, not specified**. Say so if you rely on it.

> The 8× write/read clock asymmetry is the one AC fact this document does commit to: **20 MHz write, 2.5 MHz read**, and every diagnostic register in §5.4 is on the read path.

---

## 9. Caveats, errata and conflicts

| # | Issue | Evidence |
|---|---|---|
| **C1** | **⚠ `0x44`/`0x45` power-on defaults are the SSD1680's (176 × 296), not this part's.** Unreachable on a 200 × 200 die. `0x01`'s MUX default *was* corrected, which is what proves the omission. **Always write the window explicitly** | **[DS]** §7 p. 31 vs §7 p. 20; **[DS1680]** p. 31. §3.1 |
| **C2** | **`0x21` names a `B[7:0]` parameter with no bit row and no definition.** On the SSD1680 that byte is Source Output Mode. Whether it exists here, and what its values mean, is unstated | **[DS]** §7 p. 25; **[DS1680]** p. 25. §3.2 |
| **C3** | **The feature list omits six capabilities the command table implements** — partial update, auto write RAM, CRC, HV-ready detection, panel break, OTP burn-voltage selection. Command census `executed-success`: the list is identical to the SSD1680's | **[DS]** §2 p. 5 vs §7 pp. 20–33. §3.3 |
| **C4** | **`M/S#` and `CL` are vestigial.** The pins are described but there is **no cascade section**; `M/S#` has a single instruction ("connect to `VDDIO`") and no slave behaviour is defined. What happens if you pull it low is undocumented | **[DS]** §5 p. 8, §6.12–§6.13 p. 19. §3.4 |
| **C5** | **`XON[nXY]` is named in neither the feature list nor §6.7's byte breakdown**, though the WS is the same 159 bytes and `0x32` the same 153. Bytes 150–152 are unaccounted for | **[DS]** §2 p. 5, §6.7 p. 15; **[DS1680]** same. §4.1 |
| **C6** | **⚠ Fourteen of sixteen SPI AC parameters are `TBD`**, and **all three current maxima are `TBD`**. This is a Product Preview and it shows | **[DS]** §10 p. 36, §11.1 p. 37. §8.2–§8.3 |
| **C7** | **`0x3F` `EOPT` POR `02h` is not one of its two documented values** (`22h`, `07h`) — inherited from the SSD1680 | **[DS]** §7 p. 31 |
| **C8** | **`0x03` VGH code table has duplicate rows** (`07h`=12 and `08h`=12.5 each twice) and omits `01h`/`02h` — inherited | **[DS]** §7 p. 20 |
| **C9** | **`VSL` bound disagrees between the feature list (−5 V) and Table 10-1 (−9 V max)** | **[DS]** pp. 5, 35 |
| **C10** | **`0x22` bit definitions unpublished.** Twelve composite values tabulated; the encoding is transparently a bit-field; no source defines the bits. Copy a tabulated value | **[DS]** §7 p. 26 |
| **C11** | **Three commands defer to application notes that are not public** — `0x09`, `0x34`, `0x39`. OTP programming is out of reach with this document alone | **[DS]** pp. 21, 29, 30 |
| **C12** | **OTP contents unpublished; out-of-range temperature silently prevents refresh.** Which of 36 WS/TR slots a panel maker burned is disclosed by nobody; no status bit reports the miss | **[DS]** §6.9 p. 17 |
| **C13** | **Cover footer says May 2019, all other footers and the revision history say Jun 2019.** Cosmetic, but it means "SSD1681 May 2019" and "SSD1681 Jun 2019" are the same document | **[DS]** p. 1 vs pp. 2–41 |
| **C14** | **`0x0F` Gate Scan Start Position is not available here.** The SSD1680 documents it in §8.2; the SSD1681 has no §8 command-description chapter and no `0x0F` row | **[DS]** §7 census; **[DS1680]** §8.2 p. 36. §5.2 |
| **C15** | **The DC-balance hazard is not stated.** Real for the family; absence here is not absence of the hazard | **[INF]**; [SSD1677 §4.4](../ssd1677/README.md#44--the-dc-balance-hazard) |
| **C16** | **"Product Preview", six years stale.** Rev 0.13 (Jun 2019) is the newest revision located anywhere, including Crystalfontz's catalogue, which also carries 0.13 | **[DS]** cover; **[CF]** |

---

## 10. Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/ssd1681-rev0.13-jun2019-crystalfontz-mirror.pdf` | 645 169 | `df7854a35c740ff9a8ceab208180387cc1f98b34588ed395ca07d3f744d667a9` | **SSD1681 datasheet, "Product Preview", Rev 0.13, Jun 2019.** PDF 1.6, A4, **41 pages**. Creator **PDFCreator 1.5.0**, Producer **GPL Ghostscript 9.05**, CreationDate **2019-06-05**, ModDate **2022-01-25**. `Optimized: yes` |

**Source URL — live-verified.** `https://www.crystalfontz.com/controllers/Solomon%20Systech/SSD1681/500/`, fetched **2026-09-20**: HTTP **200**, `application/pdf`, **645 169 bytes**, SHA-256 **`df7854a3…`** — **byte-identical to the retained file** (`executed-success`). Reacquisition is **`automatic`**.

> ⚠ **The PDF's `Title` metadata is `SSD1681_0.13 Holitech`, and its `Author` is `ringolau`.** Holitech Technology is a panel manufacturer, not Solomon Systech — this is a copy that passed through a module house before reaching Crystalfontz. It carries no confidentiality marking, and its text layer validates cleanly (below), but its **chain of custody is not the silicon vendor's**. Per the skill's guidance to read a document's own metadata: the `Title` is the strongest single clue to this file's real provenance, and it is not the clue the filename gives.

**Text-layer validation — `executed-success`.** `pdftotext -layout` output checked against the cover block (`SOLOMON SYSTECH` / `SEMICONDUCTOR TECHNICAL DATA` / `Product Preview`), the revision-history table and the numbered contents list. Mechanically: **for all 41 pages the PDF page index equals the printed footer `SSD1681 Rev 0.13 P n/41 Jun 2019`**, and 41 == the PDF page count. No dropped pages, no glyph subsetting, no code-point offset. Every value above comes from that validated layer.

**This file arrived misnamed.** It was acquired on 2026-09-11 as **`ssd1677.pdf`** and is not an SSD1677 — the Crystalfontz catalogue **contains no SSD1677 at all** (§11, S-3). The acquiring session evidently noticed and refetched, saving the result as `ssd1677_real.pdf` without renaming the first file, which is how it sat in scratch for nine days. The mechanism, and how to avoid repeating it, is recorded in [`vendors/solomon-systech` §2](../../../vendors/solomon-systech/README.md).

**Licence.** Third-party (Solomon Systech) copyright, *"Copyright © 2019 Solomon Systech Limited"* on the cover. **No per-page confidentiality footer.** No redistribution terms stated. Redistribution status **`unknown`**; disposition **`repository`**.

---

## 11. Authoritative sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | SSD1681 — 200 Source × 200 Gate Red/Black/White Active Matrix EPD Display Driver with Controller | **Solomon Systech Limited**, via Holitech, mirrored by **Crystalfontz America** | credible mirror | datasheet | `artifacts/ssd1681-rev0.13-jun2019-crystalfontz-mirror.pdf`; upstream `https://www.crystalfontz.com/controllers/Solomon%20Systech/SSD1681/500/` | 2026-09-11 (acquired), **2026-09-20** (URL re-verified, hash matched) | **Rev 0.13, Jun 2019 — "Product Preview"** | §1, §3–§9 |
| S-2 | SSD1680 datasheet Rev 0.14 | Solomon Systech | primary | datasheet | [`../ssd1680/artifacts/ssd1680-rev0.14-jun2019.pdf`](../ssd1680/README.md) | 2026-09-20 | Rev 0.14, Jun 2019 | §3, §5, §8.3 — every comparison marked **[DS1680]** |
| S-3 | Crystalfontz controller catalogue | Crystalfontz America | credible mirror | catalogue (embedded JSON) | `https://www.crystalfontz.com/controllers/` | **2026-09-20** | undated | That document id **500** is SSD1681 v0.13; that **no SSD1677 appears in the catalogue**; that 0.13 is the newest SSD1681 revision it carries |
| S-4 | PaperMono gaps and conflicts — booster soft-start decode | this repository | — | record | [`devices/m5stack/papermono/gaps-and-conflicts.md`](../../../devices/m5stack/papermono/gaps-and-conflicts.md) | 2026-09-20 | pass of 2026-09-11 | §2 — the in-repo consumer, citing *"SSD1681 (Rev 0.13, p.22)"* |
| S-5 | SSD1677 component record | this repository | — | record | [`../ssd1677/README.md`](../ssd1677/README.md) | 2026-09-20 | pass of 2026-09-01 | §2, §4.4 — the deep-sleep `0x01` question and the DC-balance hazard |

---

## 12. Related

- [**SSD1680**](../ssd1680/README.md) — 176 × 296. **The document this one was derived from.** Read it for the full command semantics; read §3 here for what was not carried over
- [**SSD1683**](../ssd1683/README.md) — 400 × 300, a 227-byte LUT and a genuinely different waveform block
- [**SSD1677**](../ssd1677/README.md) — 960 × 680, **the family member actually fitted on hardware here**
- [**SSD7317**](../ssd7317/README.md) — unrelated OLED + in-cell touch part, filed alongside because it arrived in the same misnamed batch
- [**Vendor sourcing guide — Solomon Systech**](../../../vendors/solomon-systech/README.md) — ⚠ **§2 is why this file spent nine days in scratch under the wrong name**
- [**Guide — e-paper displays**](../../../guides/hardware/e-paper-displays.md)
