# Sitronix ST7567A

- **Category:** monochrome dot-matrix LCD controller + driver, 132 × 65 (132 SEG + 64 COM + 1 icon COM), COG die
- **Research status:** mined end-to-end from the datasheet now held at `artifacts/`. **No board in this repository is known to use it** — see §11. This record is a component capability record, not a fitment record.
- **Retrieved:** 2026-09-11 (acquired) · **mined and filed:** 2026-09-20
- **Document:** ST7567A Datasheet **Version 1.3, 2020/08/04**, 77 pages

A single-chip STN/FSTN monochrome LCD controller-driver with on-chip DDRAM, oscillator, charge-pump
booster, regulator and follower. It needs **no external clock and no external LCD-bias resistor
network** — in the minimum configuration the only external parts are supply decoupling. That is the
whole reason this family is still designed in: a 132 × 64 graphic LCD from a 4-wire I²C bus and two
capacitors.

> ⚠ **This document arrived under a URL that named a different part.** It was fetched from
> Crystalfontz as `516.pdf` while probing `crystalfontz.com/controllers/UltraChip/UC8179/<id>/`.
> The `<Vendor>/<Part>` path segments on that host are decorative; only the numeric id selects a
> document. The file is a genuine Sitronix datasheet, but **nothing about its URL indicated that.**
> Full measurement in [`ai-crawler-site-access-table.md` § crystalfontz.com](../../../ai-crawler-site-access-table.md#crystalfontzcom--serves-controller-datasheets-and-the-url-lies)
> and §12 below.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Read directly out of `artifacts/st7567a-datasheet-v1.3-2020-08-04-crystalfontz-mirror.pdf`, cited by page |
| **[DOC-IMG]** | Read off a **rendered page image** of that PDF, not the text layer — used where the text layer was validated or where a value is suspicious |
| **[INF]** | Inference from the above. Not stated by Sitronix |
| **[WEB]** | Non-manufacturer web source, dated at retrieval |
| **[NEG]** | Negative result — something checked for and **not** found |

### Text-layer validation

**[DOC-IMG]** The PDF's text layer was validated before any number here was transcribed, per the
skill's rule on glyph-subsetted PDFs. Page 40 was rendered at 130 dpi and compared character by
character against the `pdftotext -layout` output: the headings, the `X[7:0]` truth table and the
status-bit table match exactly, **including the datasheet's own typo** (§9.3). Page-footer numbering
(`Ver 1.3  <n>/77  2020/08/04`) also matches `pdfinfo`'s `Pages: 77`. The text layer is trustworthy.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Sitronix Technology Corp.** (矽創電子) | **[DOC]** cover, page-header logo on every page |
| Part | `ST7567A` | **[DOC]** p.1, running header |
| Document | **Datasheet Version 1.3, 2020/08** (revision block dated **2020/08/04**) | **[DOC]** p.1, p.77 |
| Resolution | **132 × 65** dot matrix = 132 SEG × (64 COM + 1 icon COM) | **[DOC]** p.1, p.6, p.25 |
| DDRAM | **132 × 65 = 8 580 bits**, 8 pages of 8 bits + 1 icon page of 1 bit | **[DOC]** p.6, p.25 |
| Host interfaces | 8-bit parallel **8080** · 8-bit parallel **6800** · **4-line SPI** · **3-line SPI (9-bit)** · **I²C** | **[DOC]** p.6, p.15, p.18 |
| Package | **COG** (chip-on-glass die; pad coordinates given, p.7–11) | **[DOC]** p.6, p.7 |
| Operating temperature | **−30 … +85 °C** | **[DOC]** p.6, p.57 |
| PDF metadata title | `Microsoft Word - ST7567A_V1.3`, author `devin_chiu`, produced by *Microsoft: Print To PDF*, 2020-08-04 | **[DOC]** `pdfinfo` |

### 1.1 ⚠ There is no `ST7567Ai`, and Sitronix left the note in the document

At the foot of the feature list on **p.6** there is an untranslated internal annotation:

> ST7567A 6800, 8080, 4-Line, 3-Line
> 因出廠時全部介面都有測，包含 I2C，所以只有一個 ST7567A 料號
> ST7567Ai　I2C Interface
> 無此料號

Translated: *"because all interfaces are tested at the factory, including I²C, there is only one
ST7567A part number"* / *"**ST7567Ai** — I²C interface — **no such part number**."* **[DOC]** p.6.

This matters because sibling Sitronix monochrome parts *do* ship interface-suffixed orderable
variants, and vendor BOMs and forum posts refer to an "ST7567Ai" as though it were one. **It is not
a part number.** One die supports all five interfaces; the interface is chosen by the `SI2`, `PSB`
and `C86` strap pads on the glass (§3). **[DOC]** **[INF]** — the inference is only that the
annotation was left in by mistake; the factual claim is Sitronix's own.

This is also an instance of the skill's "read a document's own metadata" rule paying off: the note
is editorial residue, and it is the most useful sentence on the page.

---

## 2. Capabilities at a glance

| Area | Capability | Evidence |
|---|---|---|
| Duty ratios | **1/65, 1/55, 1/49, 1/33, 1/17, 1/9** | **[DOC]** p.6, p.48 |
| Bias ratios | **1/4, 1/5, 1/6, 1/7, 1/8, 1/9** | **[DOC]** p.48 |
| Frame rate | **70 … 300 Hz**, 7 steps, duty-dependent | **[DOC]** p.48 |
| Booster | Built-in charge pump, **×4 or ×5**, *capacitors on-die* | **[DOC]** p.6, p.45 |
| Regulator | 8 regulation ratios (3.0 … 6.5) × **64 EV levels** | **[DOC]** p.35, p.43 |
| Regulator drift | **−0.05 %/°C** thermal gradient | **[DOC]** p.6 |
| Follower | Built-in, generates VG / VM bias taps | **[DOC]** p.35, p.43 |
| Inversion | Frame inversion, or **N-line inversion, N = 1…32** | **[DOC]** p.46 |
| Icon row | 1 extra common (`COMS1`/`COMS2`), DDRAM page 8, **bit D0 only** | **[DOC]** p.13, p.25, p.39 |
| Read-back | DDRAM read and status read **on parallel and SPI**; **not on I²C** | **[DOC]** p.40, p.46 · §5.4 |
| Supply | VDD1 1.7–3.6 V, VDD2/VDD3 2.0–3.6 V | **[DOC]** p.58 |
| Current | ~80 µA typ. displaying black, **1 µA typ. power-down** | **[DOC]** p.58 |
| LCD drive | V0−XV0 **4.0 … 13.65 V** | **[DOC]** p.58 |

---

## 3. Interface selection — it is strapped on the glass, not configured in software

There is **no runtime interface-selection command.** `SI2`, `PSB` and `C86` are input pads tied to
`VDDH`/`VDD1` or `VSSL`/`VSS1` in the module's ITO layout, and they decide everything. **[DOC]** p.15, p.18.

| `SI2` | `PSB` | `C86` | Interface | Pins used |
|---|---|---|---|---|
| L | L | L | **3-line SPI** (9-bit) | `CSB`, `D0`=SCL, `D[3:1]`=SDA |
| L | L | H | **4-line SPI** | `CSB`, `A0`, `D0`=SCL, `D[3:1]`=SDA |
| L | H | L | **8080 parallel** | `CSB`, `A0`, `ERD`=/RD, `RWR`=/WR, `D[7:0]` |
| L | H | H | **6800 parallel** | `CSB`, `A0`, `ERD`=E, `RWR`=R/W, `D[7:0]` |
| **H** | L | X | **I²C** | `D0`=SCL, `D[3:1]`=SDA, `ERD`=SA0, `RWR`=SA1 |

**[DOC]** p.15 (Table in §5-3), p.18 (Table 1), p.19 (§6-1-4).

Three consequences that bite:

1. **`D[1]`, `D[2]` and `D[3]` must be tied together externally to form SDA.** `D1` is the serial
   data *input*, `D[3:2]` are the serial data *outputs*. The datasheet states "D[1:3] must be
   connected together as SDA" **[DOC]** p.14. Forget this and reads return nothing while writes
   appear to work.
2. **`D[7:4]` become a 4-bit hardware ID** in every serial mode, strapped to `VDDH`/`VSSL`, readable
   as `ID[3:0]` through the *SPI* status read (`0xFC`) **[DOC]** p.14, p.46. It is a board identity
   nibble, nothing to do with the controller.
3. **In I²C mode the parallel handshake pins are recycled as the address bits.** `ERD` → `SA0`,
   `RWR` → `SA1` **[DOC]** p.18. The four reserved 7-bit addresses are
   **`0111100` / `0111101` / `0111110` / `0111111` = `0x3C`–`0x3F`** **[DOC]** p.23.

### 3.1 I²C protocol shape

Standard Philips-style display protocol: `START` → slave address → *control byte* {`Co`, `A0`} →
byte → … **[DOC]** p.23.

- `Co = 1` — another control byte follows the data byte (interleaved command stream).
- `Co = 0` — **this is the last control byte**; only data bytes follow until `STOP` or repeated `START`.
- `A0 = 0` — the following bytes are **commands**; `A0 = 1` — they are **DDRAM data**.

So the familiar `0x00`-prefixed command burst and `0x40`-prefixed data burst used by SSD1306 drivers
is the same idea here: `0x00` = {Co=0, A0=0}, `0x40` = {Co=0, A0=1}. **[INF]** — the datasheet
defines the bit positions; the byte values follow arithmetically.

### 3.2 Unused pins are not "don't care"

Every interface table in the document repeats: *"the un-used pins are marked as `---` and should be
fixed to `H` by VDD1 or VDDH"* **[DOC]** p.18, p.19. And p.14, Note 1: **"After VDD1 is turned ON,
any MPU interface pins cannot be left floating."** §7.3 explains why this is a real failure mode and
not boilerplate.

---

## 4. Power supplies and the internal booster arrangement

### 4.1 The three rails

| Rail | Role | Range | Evidence |
|---|---|---|---|
| `VDD1` / `VSS1` | **Digital.** Logic and MPU interface | 1.7 – 3.6 V (typ. 1.8–3.3) | **[DOC]** p.6, p.16, p.58 |
| `VDD2` / `VSS2` | **Analog.** Booster input | 2.0 – 3.6 V (typ. 2.2–3.3) | **[DOC]** p.6, p.16, p.58 |
| `VDD3` / `VSS3` | **Reference-voltage circuit** | 2.0 – 3.6 V | **[DOC]** p.6, p.16, p.58 |

`VDD1` may equal `VDD2`, in which case they are shorted externally; `VSS1` and `VSS2` are **always**
shorted externally **[DOC]** p.16. Note the asymmetry — the digital rail goes down to **1.7 V** but
the booster input does not go below **2.0 V**, so a 1.8 V-only system cannot run the charge pump.

### 4.2 The generated LCD rails

The power block is three stages in series — **booster → regulator → follower** — each separately
switchable by one bit of the `Power Control` command (`0b00101 VB VR VF`, base `0x28`) **[DOC]** p.43.

```
VDD2 ──► [ Booster ×4 or ×5 ] ──► [ Regulator: RR[2:0] × EV[5:0] ] ──► V0
                                                                        │
                                                       [ Follower ] ────┼──► VG  (segment drive)
                                                                        ├──► VM  (common mid-level)
                                                                        └──► XV0 (negative-frame common)
```

Ordering invariant, stated twice and worth enforcing in code:
**`V0 ≥ VG > VM > VSS ≥ XV0`** during operation **[DOC]** p.16, and in the absolute-maximum notes as
**`V0 ≥ VDD2 > VG > VM > VSS ≥ XV0`** **[DOC]** p.57.

`V0O`/`V0I`, `XV0O`/`XV0I` and `VGO`/`VGI` are separate **output** and **input** pads for the same
node: the regulator drives the `*O` pad, the driver circuits sense the `*I` pad, and the ITO layout
must short them **[DOC]** p.16. This is a chip-on-glass Kelvin-connection arrangement, not two rails.

### 4.3 The booster has its own capacitors on the die

**[DOC]** p.45: *"ST7567A booster is built-in booster capacitors. Booster level can be changed with
instruction only without changing hardware connection."*

This is the headline feature versus older Sitronix/derivative parts (ST7565 and friends) that need
four external flying capacitors. Switching ×4 ↔ ×5 is a **software** change here.

External capacitors are therefore **optional and conditional** **[DOC]** p.34:

| Part | Value | When it is required |
|---|---|---|
| `C1` (V0 reservoir) | 0.1 – 1.0 µF, non-polar, **25 V** | Panel larger than **2 inches**, heavy load, **or the icon row is used** |
| `C2` (VG reservoir) | 0.1 – 1.0 µF, non-polar, **6 V** | Same conditions, **and mandatory whenever High Power Mode is enabled** (p.35) |
| `R1` (bleeder) | 500 kΩ – 1 MΩ | Only if the module can be powered down abnormally, i.e. without §8.3's sequence |

All three default to **N.C.** Higher capacitance is recommended for ripple **[DOC]** p.34.

### 4.4 High Power Mode — what `TSEL` and `0x6B` actually gate

`VG` is derived as `VG = (Vop / bias) × 2` **[DOC]** p.15. When the required `VG` approaches or
exceeds `VDD2`, the normal VG generator cannot supply it and **High Power Mode** must be enabled.

| Mode | `VG` window | Selected by |
|---|---|---|
| Off | `1.6 V ≤ VG < VDD2 − 0.2 V` | `TSEL` pad = L **[DOC]** p.15 |
| On | `VDD2 − 0.2 V ≤ VG < 3.8 V` | `TSEL` pad = H **[DOC]** p.15, *and/or* commands `0xFF`→`0x6B`→`0xFE` **[DOC]** p.47 |

The command form must be wrapped in the extension command set:

```
0xFF   ; Extension Command Set, Mode = 1  (enter)
0x6B   ; High Power Mode ON      (0x64 = OFF)
0xFE   ; Extension Command Set, Mode = 0  (exit)
```
**[DOC]** p.47.

Costs: **`C2` becomes mandatory** **[DOC]** p.35, and current consumption rises **[DOC]** p.59
(Note 2). Benefit is substantial — at VDD = 2.8 V, 1/9 bias, the attainable `Vop` goes from
**8.5–11.5 V** to **8.5–13.5 V**, and at 1/7 bias from **6.5–9.0 V** to **6.5–13.0 V** **[DOC]** p.59.

⚠ **The relationship between the `TSEL` pad and the `0x6B` command is not stated.** p.15 presents
`TSEL` as selecting the mode; p.47 presents `0x6B`/`0x64` as turning it on and off. Whether the
command overrides the pad, is gated by it, or they are ORed is **[NEG]** — not documented anywhere in
the 77 pages. If you are designing a module, strap `TSEL` for the mode you need and treat the command
as unverified. **Conflict recorded, not resolved.**

### 4.5 Application-voltage design inequalities

Worth copying into any module bring-up spreadsheet **[DOC]** p.59, with `BL` = booster stage (4 or 5),
`BE` = booster efficiency (load- and ITO-dependent, *not* given), `N` = bias denominator:

- Positive booster: `VDD2 × BL × BE ≥ Vop`
- Negative booster: `VDD2 × (BL − 1) × BE ≥ (Vop − VG)`, where `VG = Vop × 2 / N`
- Headroom: `Vop ≤ VDD2 × (BL − 1) × BE × N / (N − 2)`
- If `VG ≥ VDD2 − 0.2 V` → **enable High Power Mode**

Sitronix explicitly says to reserve margin **"for the temperature compensation and the contrast
control (for end-customer)"** **[DOC]** p.59 — i.e. do not design at the top of the EV range.

---

## 5. Contrast: `Regulation Ratio` × `EV`, and how the register actually behaves

### 5.1 The formula

**[DOC]** p.43:

```
V0 = RR × [ 1 − (63 − EV) / 162 ] × 2.1
   = RR × [ (99 + EV) / 162 ] × 2.1
```

| Register | Command | Range |
|---|---|---|
| `RR[2:0]` — Regulation Ratio | `0x20 \| RR` (`0x20`–`0x27`) | 3.0, 3.5, 4.0, 4.5, **5.0**, 5.5, 6.0, 6.5 |
| `EV[5:0]` — Electronic Volume | **double byte**: `0x81`, then `0x00 \| EV` | 0 – 63 |

**[DOC]** p.43–44.

### 5.2 Behaviour worth knowing before you write a contrast slider

- **`EV` is a two-byte instruction and the bytes are inseparable.** `0x81` puts the part into
  EV-adjust mode; the *next* command byte is consumed as the value **[DOC]** p.44. Anything that can
  interleave a command between them (an I²C `Co=1` stream, an interrupt-driven command queue) will
  corrupt the setting or the following command.
- **The curve is linear in `EV` but its span scales with `RR`.** At `RR = 5.0`, `EV` sweeps
  `V0` from ≈ 6.4 V to ≈ 10.5 V; at `RR = 3.0` from ≈ 3.85 V to ≈ 6.3 V. Choosing `RR` picks the
  window; `EV` moves inside it. **[INF]** — arithmetic from the p.43 formula.
- **Sitronix recommends centring `EV` near `0x1F`** so the end user has adjustment range in both
  directions **[DOC]** p.44.
- **Reset defaults are `RR[2:0] = 0b100` (5.0) and `EV[5:0] = 0b100000` (32)** — and, unusually, these
  two *are* reset by the **software** `RESET` (`0xE2`) as well as by hardware reset **[DOC]** p.36.
  See §7.2: this is the trap in that table.
- **The maximum achievable `V0` depends on `VDD2` and on panel load**, so the computed value is a
  ceiling, not a promise **[DOC]** p.44.

### 5.3 Temperature compensation — read this, it is a negative result

**[NEG]** **ST7567A has no temperature-compensation command, no slope-select register and no
thermistor input.** The full instruction table (p.37–38) and the extension command set contain
nothing of the kind; a search of all 77 pages for "temperature" returns only the operating range, the
storage range, a current-consumption condition and one revision-history line.

What it *does* have is a fixed characteristic of the regulator:

> **Thermal Gradient: −0.05 %/°C** — "High-accuracy Voltage Regulator for LCD Vop" **[DOC]** p.6.

So `V0` falls by 0.05 % per °C rise, which partially tracks the (much larger) negative temperature
coefficient of STN liquid crystal threshold voltage but does not cancel it.

**Practical consequence [INF]:** if your product must look right across a wide temperature range, you
compensate **in firmware** — read a temperature sensor, and rewrite `EV[5:0]` (and if necessary
`RR[2:0]`). There is no hardware path. Designers migrating from parts that *do* expose a
TC-slope register will find this missing and should not go looking for it in the extension set.

One further note **[DOC]** p.59: Sitronix says to leave `Vop` headroom specifically so that runtime
temperature compensation and end-user contrast adjustment both remain possible — which is a tacit
acknowledgement that the compensation is the host's job.

---

## 6. Memory model and addressing

- DDRAM is **132 columns × 65 rows**, organised as **page 0–7 of 8 bits** plus **page 8 of 1 bit**
  (the icon row, `D0` only) **[DOC]** p.25, p.26, p.39.
- `X = 0…131` (column), `Y = 0…8` (page). **"Addresses outside these ranges are not allowed."**
  **[DOC]** p.26.
- **Column address is a two-command pair:** high nibble `0x10 | X[7:4]`, low nibble `0x00 | X[3:0]`
  **[DOC]** p.37, p.40.
- **Page address must be set before accessing DDRAM** — it is *only* settable by the
  `Set Page Address` command, `0xB0 | Y[3:0]` **[DOC]** p.26.
- **Column auto-increments on every access and wraps to 0** past the last column **[DOC]** p.26, p.40.
  It does **not** advance the page. A 1056-byte full-frame blit is therefore nine explicit
  page-set + column-set sequences, not one stream.
- **`Set Start Line` (`0x40 | S[5:0]`, 0–63)** shifts which DDRAM line is displayed at COM0 — free
  vertical scrolling without touching RAM **[DOC]** p.39.
- **`MX` (SEG direction, `0xA0`/`0xA1`) and `MY` (COM direction, `0xC0`/`0xC8`) remap the outputs.**
  ⚠ **"It is necessary to rewrite the display data into DDRAM after changing `MX` setting."**
  **[DOC]** p.26. `MY` needs no rewrite; `MX` does. Set orientation once, at init.
- **After power-on, DDRAM contents are undefined.** Sitronix: *"It's better to initialize whole
  DDRAM (ex: fill all 00h or write the display pattern) before turning the Display ON"* **[DOC]** p.36.

### 6.1 Read-modify-write

`0xE0` enters it, `0xEE` (`END`) leaves it **[DOC]** p.37, p.42. Inside, **reads do not advance the
column pointer and writes do** — built for cursor blinking and partial redraws. `END` restores the
column address to whatever it was when `0xE0` was issued. Other instructions remain usable inside
the mode.

---

## 7. Initialisation: sequence, timing, and the traps

### 7.1 Power-on

**[DOC]** p.50–51:

| Requirement | Value |
|---|---|
| `VDDI` (VDD1) vs `VDDA` (VDD2/VDD3) order | **Any order; applying them in either order will not damage the IC** (`t_ON-V2 ≥ 0`) |
| Hardware reset after power stable | **Required.** *"If RSTB is Low, High or unstable during power ON, a successful hardware reset by RSTB is required after VDDI is stable"* |
| Recommended reset delay | **1 ms ≤ t_ON-RST ≤ 30 ms** after power is stable, *"to prevent abnormal display"* |
| "Power stable" definition | the **later** of VDDI/VDDA reaching **90 %** of its rated voltage |
| Settling wait in the flow | **5 ms**, and Sitronix says it depends on the panel and the external power components — *verify on the real product* |

Reset pulse width and recovery are supply-dependent **[DOC]** p.68:

| `VDD1` | `t_RW` (RSTB low, min) | `t_R` (reset time, max) |
|---|---|---|
| 3.3 V | 1.0 µs | 1.0 µs |
| 2.8 V | 2.0 µs | 2.0 µs |
| 1.8 V | 3.0 µs | 3.0 µs |

Microseconds, not milliseconds — but scale them as the rail drops.

### 7.2 ⚠ Hardware reset and software reset are **not** the same, and the difference is the trap

The p.36 table is the single most important page in the datasheet. Software `RESET` (`0xE2`) resets
only **six** things; hardware `RSTB` resets **all twenty-two**.

| Reset by **hardware only** (`RSTB` low) | Reset by **both** |
|---|---|
| Display OFF (`D=0`) · Normal display (`INV=0`, `AP=0`) · `MX=0` · serial counter and shift register · `BS=0` · `BL=0` · exit power-save · **`VB=VR=VF=0` (power circuits OFF)** · `NL[4:0]=0b01100` · release N-line · extension set `Mode=0` · `DSM=0` · `DT[3:0]=0` · `BA[2:0]=0` · `FR[2:0]=0` | exit read-modify-write · `S[5:0]=0` · `X[7:0]=0` · `Y[3:0]=0` · `MY=0` · **`RR[2:0]=0b100`** · **`EV[5:0]=0b100000`** |

Two consequences:

1. **`0xE2` cannot initialise the analog power block.** The datasheet says so explicitly: the software
   reset *"cannot initialize the built-in power circuit which is initialized by the RSTB pin"*
   **[DOC]** p.42, p.36. A design that omits `RSTB` and relies on `0xE2` will come up with
   `VB=VR=VF` in an indeterminate state.
2. **`0xE2` silently stamps on your contrast.** `RR` and `EV` are in the "both" column. If you issue
   `0xE2` as a "harmless resync" mid-session — as Sitronix's own refresh routine does (§7.4) — the
   contrast reverts to `RR=5.0, EV=32` and you must rewrite it. This is why the vendor refresh
   sequence rewrites `0x24`/`0x81`/`0x20` immediately after `0xE2`.

Also note `RSTB` needs a **series resistance of 2–3 kΩ** in the ITO layout, *"to prevent the ESD
pulse resetting the internal register"* **[DOC]** p.17 — and the required value *"is different from
modules"*, i.e. it is a per-module tuning parameter.

### 7.3 ⚠ Floating MPU pins cause spurious latches

Stated twice, once as a pin note and once with the mechanism **[DOC]** p.14, p.19:

> *"Some MPU will set the interface to be Hi-Z mode when power saving mode or after hardware reset.
> This is not allowed when the VDD1 of ST7567A is turned ON. Because the floating input (especially
> for those control pins such as CSB, RSTB, RWR or ERD…) maybe cause abnormal latch and cause
> abnormal display."*

And for SPI specifically **[DOC]** p.19: *"the SCL signal quality is very important and external
noise maybe causes unexpected data/instruction latch."*

**[INF]** If your MCU tri-states its GPIOs in deep sleep and the panel stays powered, you will see
intermittent garbage that looks like a driver bug. Pull the control lines, or drop `VDD1` too.

### 7.4 The vendor's own "refresh" sequence — the closest thing to a reference init

Sitronix recommends running this *periodically*, not only at boot **[DOC]** p.52:

```c
WriteCommand(0xE2);  // Software Reset        (or 0xE3 = NOP, if you must not disturb RR/EV)
WriteCommand(0xA2);  // Bias Select: BS=0 -> 1/9 bias at 1/65 duty
WriteCommand(0xA0);  // SEG Direction: MX=0, normal
WriteCommand(0xC0);  // COM Direction: MY=0, normal
WriteCommand(0x24);  // Regulation Ratio = 5.0
WriteCommand(0x81);  // Set EV, byte 1
WriteCommand(0x20);  // Set EV, byte 2 -> EV = 32
WriteCommand(0x2C);  // Power Control: Booster ON   (VB=1, VR=0, VF=0)
WriteCommand(0x2E);  // Power Control: + Regulator  (VB=1, VR=1, VF=0)
WriteCommand(0x2F);  // Power Control: + Follower   (VB=1, VR=1, VF=1)
WriteDisplayData();
```

Four things to read out of it:

- **The offer of `0xE3` (NOP) as an alternative to `0xE2` is deliberate.** Choosing NOP keeps
  `RR`/`EV`/start-line/addresses intact; choosing `0xE2` resets them, which is why they are rewritten
  two lines later. Sitronix does not explain this; §7.2 does.
- **The power block is brought up in three steps — `0x2C`, `0x2E`, `0x2F` — not one write.** That is
  booster, then regulator, then follower, each allowed to settle. The instruction description says
  *"typically, these 3 flags are turned ON at the same time"* **[DOC]** p.43, so the staged form is
  the **flow's** recommendation and the simultaneous form is the *register's*. Prefer the staged
  form; it costs two extra bytes.
- **`DISPON` (`0xAF`) is not in this list** — the refresh flow deliberately leaves the display state
  alone.
- **Bias is set here by `0xA2`/`0xA3` (`BS`), not by the `BA[2:0]` extension register.** The two
  overlap; see §8.

### 7.5 Duty and bias: two mechanisms, and the priority order is explicit

Duty can come from the **`SEL[2:1]` pads** or from the **`DT[3:0]`** field of Display Setting Mode.
Bias can come from the **`BS`** bit (`0xA2`/`0xA3`) or from **`BA[2:0]`** of the same command.

| `SEL2` | `SEL1` | Duty | Bias options via `BS` |
|---|---|---|---|
| L | L | 1/65 | 1/9 or 1/7 |
| L | H | 1/49 | 1/8 or 1/6 |
| H | L | 1/33 | 1/6 or 1/5 |
| H | H | 1/55 | 1/8 or 1/6 |

**[DOC]** p.15. **1/17 and 1/9 duty are reachable only through Display Setting Mode** — there is no
pad combination for them **[DOC]** p.15, p.48.

> **`DT[3:0]` has priority over `SEL[2:1]`. `BA[2:0]` has priority over `BS`.** **[DOC]** p.48.

Display Setting Mode is a four-byte compound command. Opcodes assembled from the bit table on p.48,
with don't-care bits written as 0:

```
0b0111_0010 = 0x72   ; enter (DSM=1)      0b0111_0000 = 0x70 ; exit (DSM=0)
0b1101_DDDD          ; duty   0xD4=65  0xD7=55  0xD5=49  0xD6=33  0xDE=17  0xDA=9
0b1001_0BBB          ; bias   0x90=1/9 0x94=1/8 0x91=1/7 0x95=1/6 0x93=1/5 0x96=1/4
0b1001_1FFF          ; frame rate, 0x98 … 0x9E
```

⚠ Bits D4 and D3 of the enter/exit byte are marked *don't care* in the table; `0x72`/`0x70` are the
all-zeros encoding. **[DOC]** p.48 **[INF]**

⚠ *"The duty, bias, and frame rate **must** be initialized by command when display setting mode is
enabled"* **[DOC]** p.48 — enabling `DSM` and setting only one of the three is not a supported state.

Frame rates **[DOC]** p.48:

| `FR[2:0]` | 9–17 duty | 33–65 duty |
|---|---|---|
| 000 | 70 Hz | **75 Hz** (reset default) |
| 001 | 105 | 110 |
| 010 | 140 | 150 |
| 011 | 175 | 190 |
| 100 | 195 | 220 |
| 101 | 230 | 250 |
| 110 | 275 | 300 |

`111` is not listed. **[NEG]**

### 7.6 N-line inversion — a tuning knob with a hazard attached

`0x85` + `0x00 | NL[4:0]` selects 1- to 32-line inversion; `0x84` releases it and returns to plain
frame inversion **[DOC]** p.37 (instruction table), p.46 (description).

The hazard is Sitronix's own warning **[DOC]** p.46:

> *"The DC bias maybe occurred if the N-line is not set well. Be sure to confirm this factor after
> choosing a value of N."*

DC bias across liquid crystal causes **permanent image sticking and electrochemical degradation.**
N-line inversion is a display-quality optimisation (it moves crosstalk artefacts around); an
arbitrary `N` is not safe by default. The hardware-reset default is `NL[4:0] = 0b01100` with N-line
inversion **released**, i.e. plain frame inversion **[DOC]** p.36. Unless you have a measured reason,
leave it released.

---

## 8. Instruction set summary

Base command set **[DOC]** p.37; extension set **[DOC]** p.38. Opcodes below are assembled from the
bit tables.

| Instruction | Opcode | Notes |
|---|---|---|
| Display ON / OFF | `0xAF` / `0xAE` | |
| Set Start Line | `0x40 \| S[5:0]` | 0–63 |
| Set Page Address | `0xB0 \| Y[3:0]` | `Y=8` is the icon page |
| Set Column Address | `0x10 \| X[7:4]`, then `0x00 \| X[3:0]` | **X ≤ `0x83`**; higher is ignored |
| Read Status | `A0=0, R/W=1` → `{0, MX, D, RST, –,–,–,–}` | **parallel only** |
| Write / Read Data | `A0=1` | |
| SEG Direction (`MX`) | `0xA0` / `0xA1` | ⚠ rewrite DDRAM after changing |
| Inverse Display (`INV`) | `0xA6` / `0xA7` | latch only; DDRAM unchanged |
| All Pixel ON (`AP`) | `0xA4` / `0xA5` | latch only |
| Bias Select (`BS`) | `0xA2` / `0xA3` | overridden by `BA[2:0]` |
| Read-modify-Write / END | `0xE0` / `0xEE` | §6.1 |
| Software RESET | `0xE2` | §7.2 — **partial** |
| COM Direction (`MY`) | `0xC0` / `0xC8` | |
| Power Control | `0x28 \| VB<<2 \| VR<<1 \| VF` | `0x2C`,`0x2E`,`0x2F` staged |
| Regulation Ratio | `0x20 \| RR[2:0]` | |
| Set EV | `0x81`, then `0x00 \| EV[5:0]` | **double byte** |
| Set Booster | `0xF8`, then `0x00` (×4) or `0x01` (×5) | **double byte**; on-die capacitors, §4.3 |
| Power Save | `0xAE` then `0xA5` | compound; §10 |
| NOP | `0xE3` | |
| Set N-Line | `0x85`, then `0x00 \| NL[4:0]` | ⚠ §7.6 |
| Release N-Line | `0x84` | |
| SPI Read Status | `0xFC`, then read `{0,MX,D,RST,ID3..ID0}` | SPI only |
| SPI Read DDRAM | `0xFD`, then read with `A0=1` | SPI only |
| Extension Command Set | `0xFF` (enter) / `0xFE` (exit) | wraps the three below |
| High Power Mode ON / OFF | `0x6B` / `0x64` | inside extension set |
| Display Setting Mode | `0x72` / `0x70` + 3 bytes | §7.5 |

> **"Do not use instructions not listed in these tables."** **[DOC]** p.38.

### 8.1 Reading back — and why I²C cannot

| Interface | Status read | DDRAM read | Dummy |
|---|---|---|---|
| 8080 parallel | ✅ | ✅ | **8 bits** |
| 6800 parallel | ✅ | ✅ | **8 bits** |
| 4-line SPI | via `0xFC` | via `0xFD` | **1 bit** |
| 3-line SPI | via `0xFC` | via `0xFD` | **1 bit** |
| **I²C** | ❌ | ❌ | (8 bits listed, but see below) |

**[DOC]** p.24, p.40, p.46.

The document is self-inconsistent here and it is worth stating plainly. p.40 (§9-2-5) says *"The read
function is not available in serial interface mode"*, yet p.46 defines `0xFC`/`0xFD` as **"SPI read
status"** and **"SPI read DDRAM"** commands, and the v1.2b revision entry is literally *"Modify
Description about Read Function in SPI Interface"* **[DOC]** p.77. **Resolution [INF]:** p.40's
sentence is stale text describing the *parallel-style* read path; SPI reads exist but require the
dedicated `0xFC`/`0xFD` opcodes. For **I²C**, §6-4-5 (p.23) describes **write only** — *"ST7567A
supports command/data write to addressed slaves on the bus"* — and no read protocol is given
anywhere. **Treat I²C as write-only.** Conflict recorded per the skill's Conflict Protocol; the
evidence that would settle it is a bus capture on real glass.

**The dummy-read rule applies to every interface that can read** **[DOC]** p.24: after setting the
address, *"a dummy read cycle is required"* — the first read returns the bus latch, the second
returns the addressed byte.

---

## 9. Errata, document defects and things that will waste your time

### 9.1 `Vop` and `V0` are used interchangeably

The regulator section computes **`V0`**; the design inequalities and the `Vop` reference tables on
p.59 use **`Vop`**; the DC table calls the driving supply **`VLCD = V0 − XV0`**. They are the same
quantity viewed from different nodes. **[INF]** — the datasheet never defines `Vop` explicitly.
**[NEG]** No symbol table exists in the document.

### 9.2 `V0 ≥ VG` vs `V0 ≥ VDD2`

p.16 gives the operating invariant as `V0 ≥ VG > VM > VSS ≥ XV0`; p.57 note 3 gives
`V0 ≥ VDD2 > VG > VM > VSS ≥ XV0`. The second is stricter and inserts `VDD2` into the chain. Satisfy
the p.57 form. **[DOC]** p.16, p.57.

### 9.3 ⚠ A genuine typo in the Set Column Address table — and a rendered-page check

p.40's truth table reads:

```
1 0 0 0 0 0 0 1  →  129
1 0 0 0 0 0 1 0  →  120     ← binary 0x82 = 130, not 120
1 0 0 0 0 0 1 1  →  131
```

**[DOC-IMG]** This is *not* a text-extraction artefact. Page 40 was rendered to PNG and read
visually: the printed table says **120**. It is a Sitronix typographical error; the value is **130**,
as the surrounding rows and the binary weight both require.

The same page carries the constraint the truth table omits: **"The X[7:0] setting must be less than
or equal to `83h`. If X[7:0] setting is greater than 83h, out of DDRAM range will be ignored."**
`0x83 = 131`, consistent with 132 columns numbered 0–131 **[DOC-IMG]** p.40.

This is exactly the failure the skill warns about — a plausible, human-legible wrong number. It was
caught by rendering the page, and it is recorded so nobody re-derives it.

### 9.4 Other small defects

- Figure 6 is captioned **"Definition of STRAT and STOP Condition"** — *STRAT* for *START* **[DOC]** p.21.
- The `Set Start Line` line-address table on p.39 lists `S = 0…63`, but the display can be 65 rows
  tall including the icon common. The icon row is not scrollable. **[INF]**
- `FR[2:0] = 111` is absent from the frame-rate table with no "reserved" marking **[NEG]** p.48.
- The `TSEL` pad / `0x6B` command relationship is undefined — §4.4.

### 9.5 Revision history

**[DOC]** p.77:

| Version | Date | Change |
|---|---|---|
| 1.0 | 2015-08-21 | Remove Preliminary |
| 1.1 | 2015-09-15 | Add Extension Command Table · Modify Bump Height · Add `Vop` reference table |
| 1.1a | 2015-12-09 | Add description of 17-duty and 9-duty |
| 1.2 | 2016-07-13 | Modify Column Address instructions |
| 1.2a | 2016-12-06 | Modify minimum voltage of VDDA · Modify temperature range of current consumption |
| 1.2b | 2017-05-24 | Modify description about read function in SPI interface |
| **1.3** | **2020-08-04** | Add the default value of the Release N-Line register · Modify Read Status register |

Three and a half years between 1.2b and 1.3, and both 1.3 changes are corrections to *documentation of
existing behaviour*. **[INF]** The part is mature and stable; there is no sign of a silicon revision
in this history.

---

## 10. Power-save and power-off

**Power Save is a compound instruction**, not an opcode: `Display OFF (0xAE)` **then**
`All Pixel ON (0xA5)` **[DOC]** p.45. Exit is the mirror image: `0xA4` then `0xAF`.

Entering it stops the oscillator, stops the power circuits and parks COM/SEG at `VSS`. **Display data
and all register settings are preserved** except the `D` and `AP` flags **[DOC]** p.45.

Exit is slow and staged **[DOC]** p.54 — booster, regulator and follower each take **up to 100 ms**
to stabilise, and the IC forces outputs to `VSS` for a **typical 200 ms** during the transition
(measured on a 1.4″ panel, no external capacitors, VDD = 2.7 V, Vop = 9 V). Budget ~300 ms before the
image is trustworthy after wake.

**Power-off has a required sequence and skipping it can damage the panel** **[DOC]** p.55–56:

1. Enter power-save (`0xAE`, `0xA5`) **or** pulse `RSTB` low then high.
2. **Wait 250 ms** (`t_POFF`, internal discharge, 250 ms max).
3. Remove `VDD1`–`VDD3`. `t_V2OFF` min is 0 ms — they may go together.
4. When dropping `VDDA`, respect **20 ms ≤ t_Pfall ≤ 0.2 s**.

⚠ *"It is **NOT** recommended to turn VDDI OFF before VDDA. Without VDDI, the internal status cannot
be guaranteed and the internal discharge process maybe stopped. The un-discharged power maybe flows
into COM/SEG output(s) and **the liquid crystal in panel maybe polarized**."* **[DOC]** p.56.

Polarisation is cumulative and permanent. This is the `R1` bleeder resistor's reason to exist (§4.3):
it is insurance against an abnormal power-down path the firmware cannot control **[DOC]** p.34.

The IC itself is not at risk — *"IC will NOT be damaged if either VDDI or VDDA is OFF while another
is ON"* **[DOC]** p.56. The glass is.

---

## 11. Used By

**None.** No device in this repository is documented as using an ST7567A, and **no fitment is claimed
here.** The datasheet was acquired incidentally while probing the Crystalfontz controller-document
host during Xteink research (§12); it documents the part, not any board.

If you fit one, add a row here and link back from the device record.

---

## 12. Provenance — the URL that lied

| Field | Value |
|---|---|
| Source host | `www.crystalfontz.com` |
| URL form probed | `https://www.crystalfontz.com/controllers/UltraChip/UC8179/<id>/` |
| Numeric id that returned this file | **516** |
| Part the URL claimed | **UltraChip UC8179** (an e-paper driver — unrelated) |
| Part the file actually is | **Sitronix ST7567A** |
| Retrieved | **2026-09-11** |
| SHA-256 | `84acecb59bda61207c0fc1b5ab89d3dc7b7ab1ae66e20aa680418604bb4336c2` |
| Byte size | **3 503 339** |
| Pages | 77 |
| Local artifact | `artifacts/st7567a-datasheet-v1.3-2020-08-04-crystalfontz-mirror.pdf` |
| Disposition | **repository** (primary, 3.3 MB, Sitronix publishes nothing equivalent — see the [vendor guide](../../../vendors/sitronix/README.md)) |
| Licence | **unknown.** No notice, no confidentiality marking, no redistribution statement anywhere in the 77 pages |
| Redistribution status | **unknown** |

**The file is genuine; the URL is worthless as identification.** Every numbered document on that host
must be identified by content before filing. The measured id→part map is in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md#appended-2026-09-20--crystalfontz-numeric-id-probe-measured).

> ⚠ **Added 2026-09-20 — this copy carries a Crystalfontz raster stamp on page 1.** `pdfimages -list`
> shows a **1700 × 105 RGB image (8 936 B) plus a 2 601 B soft mask** on page 1 and on no other page;
> rendered, it reads *"This LCD controller datasheet was downloaded from
> https://www.crystalfontz.com/controllers"*. It is **not in the text layer** — `pdftotext` finds
> zero occurrences of "crystalfontz" in all 77 pages, so the §"Text-layer validation" check above
> could not have detected it. The byte-identical object appears on page 1 of **every** document
> recovered from that host (ids 512–516). **Consequence:** this file will never hash-match Sitronix's
> original even if the content is identical, and a hash mismatch against another mirror is therefore
> **not** evidence of a different revision. Full measurement in
> [FT5436 §10](../../focaltech/ft5436/README.md).

Filed under `components/sitronix/` rather than under the Xteink device that occasioned the fetch,
per the skill's rule: **a file is filed by what it describes.**

---

## 13. Related records and open questions

### Related

- **[Sitronix documentation-sourcing guide](../../../vendors/sitronix/README.md)** — why Sitronix
  publishes nothing, and the ranked list of places that do. **Crystalfontz is now on that list.**
- [Sitronix ST77916](../st77916/README.md) — the colour QSPI sibling; same house conventions,
  completely different register set
- [Sitronix ST7789V2](../st7789v2/README.md) · [ST7789VW](../st7789vw/README.md) ·
  [ST7796S](../st7796s/README.md) · [ST7701S](../st7701s/README.md) — the colour TFT line
- [Display interfaces guide](../../../guides/hardware/display-interfaces.md) — how parallel/SPI/I²C
  command-bus displays compare
- [Chip Wealth Technology CH13620](../../chip-wealth-technology/ch13620/README.md) — the other
  driver recovered from the same Crystalfontz probe, at the opposite end of the display market
- [FocalTech FT5436](../../focaltech/ft5436/README.md) ·
  [FT3267](../../focaltech/ft3267/README.md) — the touch controllers from the same probe

### ⚠ ST7567**S** is a different part — **now filed, mined, and compared**

**Updated 2026-09-20.** This section previously said the `S` document was held unmined in scratch.
It no longer is: Crystalfontz id **515** — **ST7567S, Datasheet Version 1.4, 2016/07/13, 68 pages**
(SHA-256 `75f3c2aaf8d5353d35c32632d7c56089a108399ec6f30e2c42bb18c237026d9a`, 918 094 bytes) — has
been filed at **[`components/sitronix/st7567s/`](../st7567s/README.md)** and mined end to end.

**[ST7567S §2](../st7567s/README.md) is a measured, document-to-document difference table between
the two parts.** Read it before treating them as interchangeable. The headline items:

| | ST7567**A** | ST7567**S** |
|---|---|---|
| Extension command set (`0xFF`/`0xFE`) and everything inside it | ✅ | ❌ **absent** |
| Display Setting Mode, `DT`/`BA`/`FR` | ✅ | ❌ **absent** — duty and bias come only from `SEL[2:1]`/`BS` |
| N-line inversion (`0x85`/`0x84`) | ✅ | ❌ **absent** |
| **High Power Mode** | ✅ — `TSEL` pad selects it | ❌ — **`TSEL` is a test pad that must be tied LOW** |
| Duty ratios | 6 (adds 1/17, 1/9) | 4 |
| **`VDD2`/`VDD3` minimum** | **2.0 V** | **2.4 V** |
| `Vop` design inequalities | ✅ p.59 | ❌ absent |
| Application circuits / ITO layout reference | ❌ | ✅ §15, p.60–67 |

⚠ **The `TSEL` row is the dangerous one**: the same pad is a mode selector on the `A` and a
tie-low test pad on the `S`.

**Base-set code ports between them.** Anything touching `0xFF`, `0x72`, `0x85`, `0x6B`, the `TSEL`
pad, 1/17 or 1/9 duty, or a frame-rate setting **does not**.

### Open questions

| Question | Status |
|---|---|
| Does the `0x6B` High Power Mode command override the `TSEL` pad, or is it gated by it? | **Open.** §4.4. Not stated in 77 pages |
| Can ST7567A be read over I²C at all? | **Open, leaning no.** §8.1. Needs a bus capture on real glass |
| What is the booster efficiency `BE` in the p.59 inequalities? | **Open.** Sitronix says it is module- and ITO-dependent and gives no figure |
| Is there any errata document? | **[NEG]** None found; Sitronix publishes no public errata (see vendor guide) |
| How do ST7567A and ST7567S differ, register for register? | **Partly answered 2026-09-20.** The *documented* feature delta is now tabulated in [ST7567S §2](../st7567s/README.md). **Still open:** whether the two differ in silicon beyond the documented delta — no part was measured |
| Does the ST7567A's "120" column-address typo (§9.3) exist upstream or only in this copy? | **Answered 2026-09-20: it is upstream.** The same typo is in ST7567S v1.4 p.35, and both documents attribute their column-address edit to **2016-07-13**. [ST7567S §8.1](../st7567s/README.md) |
| Is the Read-Status `D` bit really inverted relative to the command `D` bit? | **Open, and shared.** ST7567A §8 reports `D=0: Display ON` in Read Status against `D=1: display ON` in the command; **ST7567S prints the identical inversion**. [ST7567S §8.2](../st7567s/README.md). One bus capture settles it for both |

---

## Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| A1 | **ST7567A Datasheet Version 1.3** | Sitronix Technology Corp. | **primary** (via credible mirror) | datasheet | `https://www.crystalfontz.com/controllers/UltraChip/UC8179/516/` — ⚠ **the URL names a different part**; see §12 | 2026-09-11 | 2020-08-04 | Everything on this page unless marked otherwise | `artifacts/st7567a-datasheet-v1.3-2020-08-04-crystalfontz-mirror.pdf` |
| A2 | Crystalfontz numeric-id probe (`cfprobe`), 12 ids | this repository | — | measurement | — | 2026-09-11 / re-verified 2026-09-20 | — | The id→part map and the HTML-under-`.pdf` fallback | `archive/devices/xteink/shared-artifacts/research-scratch/datasheets/cfprobe/README.md` · [`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md) |
| A3 | ST7567S Datasheet Version 1.4 | Sitronix Technology Corp. | primary (via mirror) | datasheet | `https://www.crystalfontz.com/controllers/UltraChip/UC8179/515/` | 2026-09-11 | 2016-07-13 | That `S` is a distinct, older, shorter part; the §13 difference table; the shared "120" typo and Read-Status polarity | [`../st7567s/artifacts/st7567s-datasheet-v1.4-2016-07-13-crystalfontz-mirror.pdf`](../st7567s/artifacts/st7567s-datasheet-v1.4-2016-07-13-crystalfontz-mirror.pdf) — **filed and mined 2026-09-20**, see [`../st7567s/README.md`](../st7567s/README.md) |
