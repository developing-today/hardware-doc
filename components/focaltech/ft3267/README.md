# FocalTech FT3267

- **Category:** **self-capacitance** touch-panel controller with an on-chip 16-bit enhanced MCU,
  **22 combined sensor/driver channels**, I²C slave interface — aimed at **wearables, ≤ 1.4″**
- **Research status:** mined end-to-end from the datasheet now held at `artifacts/`.
  **No board in this repository is known to use it** — see §9. This is a component capability
  record, not a fitment record.
- **Retrieved:** 2026-09-11 (acquired) · **mined and filed:** 2026-09-20
- **Document:** `D-FT3267-DataSheet-V0.1`, © 2015 FocalTech, **Version 0.1**, 13 PDF pages numbered
  "Page *n* of 11"

The smallest FocalTech part documented here, and the only one that markets **single-layer
multi-touch** — FocalTech's "LCST" (Local Capacitance Sensing Technology). Its 22 pins are neither
TX nor RX: every channel is typed `I/O` and acts as both driver and sensor, which is what
self-capacitance means and what lets the panel be one layer of ITO.

> ⚠ **This document arrived under a URL that named a different part.** It was fetched from
> Crystalfontz as `513.pdf` while probing `crystalfontz.com/controllers/UltraChip/UC8179/<id>/`.
> The `<Vendor>/<Part>` path segments on that host are decorative; only the numeric id selects a
> document. See §10 and
> [`ai-crawler-site-access-table.md` § crystalfontz.com](../../../ai-crawler-site-access-table.md#crystalfontzcom--serves-controller-datasheets-and-the-url-lies).

> ⚠ **The document is a V0.1 draft, is marked proprietary, and carries a large diagonal
> "FOCALTECH CONFIDENTIAL" watermark that does not appear in its text layer.** See §1.2 and §10.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Read out of `artifacts/ft3267-datasheet-v0.1-crystalfontz-mirror.pdf`, cited by the document's own printed page number |
| **[DOC-IMG]** | Read off a **rendered page image** of that PDF rather than its text layer |
| **[INF]** | Inference from the above. Not stated by FocalTech |
| **[NEG]** | Negative result — something checked for and **not** found |

### Text-layer validation — and what it missed

**[DOC-IMG]** Page 1 was rendered at 150 dpi and compared against `pdftotext -layout` output before
any number below was transcribed. The introduction, both feature columns and the footer match
exactly, and `pdfinfo` reports `Pages: 13` against the printed `Page 11 of 11` (two unnumbered front
pages). The text layer is trustworthy **for the text it contains**.

⚠ **It does not contain everything on the page.** The render showed **two overlays absent from the
text layer**:

1. A large diagonal **"FOCALTECH CONFIDENTIAL"** watermark across page 1.
2. A Crystalfontz banner strip across the top of page 1 (§10).

This is the concrete case for the skill's rule about rendering a page rather than trusting
extraction: the **licensing status of this artifact is only visible in the raster layer**, and a
text-only pass would have recorded the copyright footer and missed the watermark entirely.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **FocalTech Systems Co., Ltd.** (敦泰科技) | **[DOC]** p.1 header/footer |
| Part | `FT3267` | **[DOC]** p.1, p.1 model table |
| Document | **Version 0.1**, `D-FT3267-DataSheet-V0.1`, © 2015 | **[DOC]** every page footer; PDF `Title` |
| Sensing | **Self-capacitance**, "Local Capacitance Sensing Technology (LCST)" for **single-layer multi-touch** | **[DOC]** p.1 |
| Channels | **22**, each a combined sensor **and** driver (`S1`…`S22`, all typed `I/O`) | **[DOC]** p.1, p.9 |
| Touch points | "supports multi touch" — ⚠ **no maximum point count is stated anywhere** | **[DOC]** p.1 · **[NEG]** |
| Output | **Absolute X and Y coordinates, or gesture** | **[DOC]** p.1 |
| Report rate | **up to 100 Hz**; Active scan **60 fps default**, Monitor **25 fps default**, both host-configurable | **[DOC]** p.1, p.2 |
| Max panel | **≤ 1.4 inch** — wearables | **[DOC]** p.1 |
| Package | **QFN-4×4-32L, 0.5 mm total thickness, 0.4 mm pitch**, 2.7 mm exposed pad | **[DOC]** p.1, p.11 |
| On-chip memory | **48 KB Flash, 5 KB SRAM** | **[DOC]** p.2 |
| Master clock | **18 MHz**, divided from a **36 MHz** RC oscillator (34.64 / 36 / 36.36 MHz) | **[DOC]** p.2, p.5 |
| Operating temperature | **−40 … +85 °C**; storage −55 … +150 °C | **[DOC]** p.1, p.4 |
| ESD | **HBM ≥ 7500 V, MM ≥ 500 V** | **[DOC]** p.1 |
| Shielding | Supports single-film TP and triangle pattern **without an additional shield** | **[DOC]** p.1 |
| PDF metadata | `Title: Microsoft Word - D-FT3267-DataSheet-V0.1`, `Author: lijun`, PScript5 → Acrobat Distiller 9.0, created 2015-12-30 | **[DOC]** `pdfinfo` |

### 1.1 It is the same silicon generation as the FT6336G

The MCU block is **identical in every published figure** to
[FT6336G](../ft6336g/README.md): 48 KB flash, 5 KB SRAM, 18 MHz master clock from a 36 MHz RC
oscillator, the same 1.5 V internal regulator, the same three-mode power management, the same
ESD numbers (HBM ≥ 7500 V, MM ≥ 500 V), the same −40…+85 °C range, the same "single film TP and
triangle pattern without additional shield" claim, and the same I²C timing table. **[DOC]** p.1–5
vs [FT6336G §2](../ft6336g/README.md).

The differences are the analogue front end and the package:

| | **FT3267** | [FT6336G](../ft6336g/README.md) |
|---|---|---|
| Channels | **22** | 31 |
| Panel | **≤ 1.4″** | ≤ 4.0″ |
| Package | **QFN 4 × 4, 32L, 0.4 mm** | QFN 5 × 5, 40L, 0.4 mm |
| Supply | **VDDA 2.8 – 3.6 V** *and* a separate **VDDD** | VDDA 2.8 – 3.6 V |
| Sensor drive | **5 V from an internal charge pump** (§3.2) | not stated |
| Extra pin | **`SYNC`** (§4.1) | — |

**[INF]** These are two members of one family, documented from one template. Do not read that as
register compatibility — see §5.

### 1.2 ⚠ It is a **V0.1 draft**

Every page footer reads `Version 0.1`. There is **no revision-history table** in the document
**[NEG]** — unlike [FT5436](../ft5436/README.md), which at least prints one row. A `0.x` version
number with no history is a pre-release document, and several things in it read that way (§7).

**No later revision was located.** If you are designing with this part, ask FocalTech for the
current document before trusting any number below.

---

## 2. Operation modes and the I²C port that closes itself

**[DOC]** p.2.

| Mode | Behaviour | Typ. current **[DOC]** p.5 |
|---|---|---|
| **Active** | Full scan, **60 fps default**, host-configurable up or down | **4 mA** (`VDDA = VDD3 = 2.8 V`, 25 °C, MCLK 18 MHz) |
| **Monitor** | Reduced scan, **25 fps default**, host-configurable. Most algorithms stopped; a simple presence detector runs. Enters Active *immediately* on touch. ⚠ **"the serial port is closed and no data shall be transferred with the host processor"** | **100 µA** |
| **Hibernation** | Power-down. *"It shall respond to the 'RESET' or 'Wakeup' signal from the host processor"* | **55 µA** (the table calls this "Sleep mode") |

Three things to take from this:

1. ⚠ **Monitor mode closes the I²C port.** A host that polls gets nothing. **The correct
   architecture is interrupt-driven: wait for `/INT`, then read.** Identical to
   [FT6336G](../ft6336g/README.md) §2.2.
2. ⚠ **Hibernation current is only ~1.8× lower than Monitor** (55 µA vs 100 µA) — and Monitor still
   detects touches. **[INF]** On this part, deep sleep buys very little and costs you the wake path;
   for most wearable designs, parking in Monitor and waiting on `/INT` is the better trade.
3. ⚠ **The "Wakeup signal" has no pin.** §2.3 names it; the pin table (p.9) lists only `RSTN` (in)
   and `INT` (typed `I/O` but described as "external interrupt **to the host**"). **[NEG]** There is
   no `WAKE` pin and no statement that `INT` is host-driveable. Compare
   [FT5436 §4.3](../ft5436/README.md), where the pin table *does* say `INT` doubles as a host wake
   input. **Unresolved for FT3267** — see §8.

---

## 3. Electrical

### 3.1 Supplies and limits

**[DOC]** p.4, Table 3-1 (absolute maxima) and p.4–5, Table 3-2 (DC, `VDDA` = 2.8–3.6 V,
Ta = −40…85 °C).

| Rail | Pin | Role | Absolute max | Operating |
|---|---:|---|---|---|
| **`VDDA`** | 25 | Analogue supply. **1 µF ceramic to ground required** | −0.3 … +3.6 V | **2.8 – 3.6 V** |
| **`VDDD`** | 26 | Digital supply. **1 µF required** | −0.3 … +3.6 V *(named `VDD3` in the table — §7)* | **2.8 – 3.6 V** |
| **`IOVCC`** | 28 | **Independent** host-interface rail | **1.8 – 3.6 V** | 1.8 – 3.6 V |
| `VDD5` | 24 | *"High voltage power supply from the **charge pump LDO generated internally**. A 1 µF ceramic to ground is required"* | — | **5 V** typ output |
| `VREF` | 1 | *"**Generated internal** reference voltage. A 1 µF ceramic capacitor to ground is required"* | — | — |

**[INF]** You supply `VDDA`, `VDDD` and `IOVCC`; you decouple `VDD5` and `VREF` and drive neither.
Unlike [FT5436](../ft5436/README.md), this document is explicit that `VDD5` and `VREF` are
internally generated, so the inference is a short one.

Note the abs-max table's own notes: *"Make sure `VDDA` (high) ≥ `VSSA` (low)"* and *"Make sure
`VDD3` (high) ≥ `VSS` (low)"* **[DOC]** p.4 — i.e. the analogue and digital domains have separate
grounds and neither may be driven below its own return.

| DC item | Value |
|---|---|
| `VIH` / `VIL` | 0.7 × `IOVCC` … `IOVCC` / −0.3 … 0.3 × `IOVCC` |
| `VOH` | ≥ 0.7 × `IOVCC` at **`IOH` = −0.1 mA** |
| `VOL` | ≤ 0.3 × `IOVCC` at **0.1 mA** |
| I/O leakage | ±1 µA (`Vin` = 0…`VDDA`) |

> ⚠ **The output drive is 0.1 mA.** That is **30–45× weaker** than
> [FT5436](../ft5436/README.md)'s 3 mA / 4.5 mA. `/INT` on this part will not drive a long trace, a
> heavy pull-up or a level shifter's input capacitance quickly. **[INF]** Keep the pull-up weak
> (≥ 33 kΩ) and the trace short, or expect slow edges. This is a real constraint that the datasheet
> states only as a test condition.

### 3.2 The sensor front end runs at 5 V

**[DOC]** p.5, Table 3-4.

| Item | Symbol | Min | Typ | Max | Unit |
|---|---|---:|---:|---:|---|
| Sensor acceptable clock | `ftx` | **0** | 100 | **300** | kHz |
| Sensor output rise time | `Ttxr` | — | **100** | — | ns |
| Sensor output fall time | `Ttxf` | — | **80** | — | ns |
| Sensor **input voltage** | `Trxi` | — | **5** | — | V |

**The 5 V figure is the point.** It is consistent with `VDD5` — the internally generated charge-pump
rail on pin 24 — being the self-capacitance **drive** voltage. **[INF]** Driving the sensor above
the logic rail is how a self-capacitance part gets signal-to-noise out of a single ITO layer, and it
is why pin 24 needs its own 1 µF capacitor. Get that capacitor wrong and sensitivity, not just
ripple, suffers.

> ⚠ Same inherited defect as [FT5436](../ft5436/README.md): the **voltage** row carries the *time*
> symbol **`Trxi`**. Two parts, same template, same mistake.

Note also `ftx` **min = 0 kHz**, which is not a meaningful lower bound for a drive clock. **[NEG]**

---

## 4. Host interface

### 4.1 Pinout (QFN-4×4-32L)

**[DOC]** p.9, Table 4-1.

| Pin | Name | Type | Notes |
|---:|---|---|---|
| 1 | `VREF` | PWR | internally generated; 1 µF to ground |
| 2 – 23 | **`S1` … `S22`** | **I/O** | Capacitance **sensor / driver** channels — one pin does both |
| 24 | `VDD5` | PWR | internal charge-pump LDO output; 1 µF |
| 25 | `VDDA` | PWR | analogue supply; 1 µF |
| 26 | `VDDD` | PWR | digital supply; 1 µF |
| 27 | **`RSTN`** | I | **External reset, low active** |
| 28 | `IOVCC` | PWR | I/O supply |
| 29 | `SCL` | I/O | I²C clock input |
| 30 | `SDA` | I/O | I²C data |
| 31 | **`INT`** | **I/O** | "External interrupt to the host" — but typed `I/O`; §2 note 3 |
| 32 | **`SYNC`** | **I** | **"External signal"** — and that is the entire description **[NEG]** |

**`S1`…`S22` are contiguous on pins 2–23**, which makes the QFN's channel-to-pin mapping trivial —
`pin = channel + 1`. Worth knowing because the package figure is an image and this is the only place
the mapping is in text. **[DOC]** p.9.

> ⚠ **`SYNC` (pin 32) is undocumented.** It is an **input**, it is named "External signal", and
> nothing else in 11 pages mentions it. **[INF]** In touch controllers a `SYNC` input is almost
> always a display-refresh/noise synchronisation strobe — capacitive sensing and LCD/OLED source
> drive interfere, and scanning in the display's blanking interval is the standard cure. **That
> reading is an inference and FocalTech does not confirm it.** If you are integrating this part
> under a display, ask. See §8.

### 4.2 I²C

**[DOC]** p.3–4. I²C slave only; no SPI, no parallel.

| Parameter | Min | Max | Unit |
|---|---:|---:|---|
| `SCL` frequency | **10** | **400** | kHz |
| Bus free, STOP → START | **4.7** | — | µs |
| (Repeated) START hold | **4.0** | — | µs |
| Data setup | **250** | — | ns |
| Repeated-START setup | **4.7** | — | µs |
| STOP setup | **4.0** | — | µs |

> ⚠ **The timings are Standard-mode (100 kHz) values under a 400 kHz ceiling.** I²C Fast-mode
> specifies `tBUF` ≥ 1.3 µs and `tHD;STA` ≥ 0.6 µs; this table demands **4.7 µs and 4.0 µs**. The
> numbers and the frequency limit cannot both be design targets.
>
> [FT6336G](../ft6336g/README.md) prints the **same** table. [FT5436](../ft5436/README.md) prints
> the coherent Fast-mode set (1.3 µs / 0.6 µs / 100 ns). **[INF]** The FT3267/FT6336G table is
> inherited boilerplate; FT5436's is the edited one. **Conflict recorded, not resolved.**
>
> **Safe path:** run the bus at **400 kHz** (the ceiling is stated twice and in the feature list)
> but do **not** compress inter-transaction spacing below ~4.7 µs. On a typical MCU driver that
> costs nothing, because the gap between transactions already exceeds it.

Framing is plain 7-bit I²C — `S · A[6:0] · R/W · A · D[n] · A · …· P` **[DOC]** p.3, Figures 2-4 /
2-5 / 2-6, with the mnemonic table on p.4. **No register-pointer convention is drawn.**

### 4.3 The interrupt contract

*"The interrupt signal (`/INT`) is used for FT3267 to inform the host that data are ready for the
host to receive. The `RSTN` signal is used for the host to reset FT3267. After resetting, FT3267
shall enter the Active mode."* **[DOC]** p.3.

So: **`/INT` asserted ⇒ a coordinate/gesture report is waiting.** Combined with §2, the whole
interface contract is:

```text
reset  ->  Active  ->  (idle)  ->  Monitor [I2C closed]  ->  touch  ->  Active  ->  /INT  ->  host reads
```

**A read issued at any point other than after `/INT` may hit a closed port.** **[INF]**

---

## 5. ⚠ Report protocol and register map — they are not in this document

**[NEG]** **Version 0.1 of the FT3267 datasheet contains no I²C slave address, no register map, no
touch-report format, no gesture code table, no maximum touch-point count, and no chip-ID register.**
Full-text search of all 13 pages finds no `0x38`, no slave-address value, and no register table.

This is the third FocalTech datasheet in this repository with the same hole — see
[FT6336G](../ft6336g/README.md) §2.1 and [FT5436](../ft5436/README.md) §5. **It is a vendor policy,
not an oversight:** FocalTech distributes register information in separate per-customer application
notes, typically under NDA.

What the document *does* fix:

- I²C slave, 7-bit address, byte-stream framing with per-byte ACK. **[DOC]** p.3.
- The chip **outputs "absolute X and Y coordinates **or** gesture"** — so a gesture engine exists
  and is selectable or concurrent. **[DOC]** p.1. **No gesture is named and no code is given.**
- `/INT` signals data-ready. **[DOC]** p.3.

**Not claimed here:** that the address is `0x38`; that the FT5x06 6-bytes-per-point layout applies;
that any particular gesture set is implemented. All are plausible family expectations and **none is
evidence for FT3267**. The repository's own
[FT3168 record](../ft3168/README.md) §4 makes the same refusal for the same reason, and that
precedent is followed here deliberately.

**To write a driver you need** FocalTech's register application note, or an open driver identified
as targeting **FT3267** specifically. See §8.

---

## 6. Initialisation and reset — the 300 ms you must wait

**[DOC]** p.6–8, §3.5 and Table 3-5.

| Symbol | Description | Min | Max | Unit |
|---|---|---:|---:|---|
| `Tris` | Supply rise, 0.1 `VDD` → 0.9 `VDD` | — | **3** | ms |
| **`Tpon`** | **Time to first reported point after power-on** | **300** | — | **ms** |
| `Tprt` | Time `RSTN` is held low after powering on | **1** | — | ms |
| **`Trsi`** | **Time to first reported point after reset** | **300** | — | **ms** |
| `Trst` | Reset time / minimum time the supply stays below 0.3 V in a power cycle | **5** | — | ms |

The prose rules **[DOC]** p.6:

1. ⚠ **"The GPIO such as INT and I2C are advised to be low before powering on."** Not merely
   `RSTN` — **`/INT`, `SDA` and `SCL` too**. That is awkward: an I²C bus normally sits pulled *high*
   at rest. On a shared bus you cannot hold SDA/SCL low at power-up without disturbing every other
   slave. **[INF]** The practical reading is that this part prefers to be powered from a switched
   rail that comes up *with* the bus, or to be isolated behind a bus switch — the arrangement the
   [PaperMono uses for its FT6336G](../ft6336g/README.md) §4.2, where the translator's `OE`
   follows the touch rail. **Advisory wording ("advised"), not a hard requirement.**
2. **"Reset should be pulled down to be low before powering on."**
3. **"INT signal will be sent to the host after initializing all parameters and then start to
   report points to the host."** — bring-up ends when the first `/INT` arrives.
4. **"If Power is down, the voltage of supply must be below 0.3V and `Trst` is more than 5ms."**
   A brown-out that only dips partway leaves the part in an undefined state.

> ⚠ **`Tpon` and `Trsi` are printed as MINIMA of 300 ms, not maxima.**
> Read literally, the part guarantees it will **not** report a point for at least 300 ms after
> power-on or reset — a *floor* on latency rather than a bound on it, and the opposite polarity to
> [FT5436](../ft5436/README.md), whose analogous `Trsi` is a **max of 200 ms**. Given the surrounding
> prose ("the time of starting to report point after resetting approach to the time of starting to
> report point after powering on") this is most likely a **min/max column error inherited with the
> table**. **[INF]**
>
> **Either reading gives the same engineering advice**, which is why it is safe to act on:
> **allow ≥ 300 ms between reset release and the first expected report, and do not treat silence
> before then as a fault.** Do not, however, transcribe "300 ms max" anywhere — the document does
> not say that. **Conflict recorded, not resolved.**

**[INF] Minimum safe sequence**; **`not-tested`**, no hardware was available:

```text
RSTN = 0                       # and, if you can, INT/SDA/SCL low too
VDDA, VDDD, IOVCC on           # rise within Tris <= 3 ms
hold RSTN low >= 1 ms          # Tprt
RSTN = 1
wait for /INT                  # expect >= 300 ms (Tpon/Trsi); do not conclude failure early
```

As with [FT5436](../ft5436/README.md), there is **no documented ID register to read at bring-up**,
so a dead part and an idle part are indistinguishable until the first touch. **[NEG]**

Reset-pin input structure and the general I/O port circuit are given as figures only (p.6,
Figures 3-1 and 3-2) with **no component values in the text layer** — unlike
[FT5436](../ft5436/README.md), whose equivalent figures carry a 300 Ω / 50 kΩ / 2 MΩ annotation.
**[NEG]**

---

## 7. Document defects, collected

| # | Defect | Where |
|---|---|---|
| 1 | **`VDD3`** in the absolute-maximum and DC tables versus **`VDDD`** in the pin table — the same rail under two names, and `VDD3` appears on no pin | p.4–5 vs p.9 |
| 2 | Sensor **voltage** row carries the time symbol **`Trxi`** (shared with [FT5436](../ft5436/README.md)) | p.5 · §3.2 |
| 3 | `ftx` min = **0 kHz** — not a meaningful lower bound | p.5 · §3.2 |
| 4 | I²C timings are **Standard-mode** values under a **400 kHz** ceiling | p.4 · §4.2 |
| 5 | `Tpon` / `Trsi` printed as **minima**; almost certainly a min/max column error | p.8 · §6 |
| 6 | "Hibernation Mode" in the feature list and §2.3; the current table calls the same state **"Sleep mode"** | p.1–2 vs p.5 |
| 7 | A **"Wakeup" signal** is named in §2.3 with no corresponding pin | p.2 vs p.9 · §2 |
| 8 | **`SYNC`** pin described only as "External signal" | p.9 · §4.1 |
| 9 | **No maximum touch-point count**, despite "supports multi touch" on the cover | p.1 · §1 |
| 10 | **No revision history** at all, in a document versioned **0.1** | — · §1.2 |
| 11 | Table of contents contains a stray `\\` artefact | p.i |

Eleven defects in eleven numbered pages, in a draft-versioned document. **[INF]** Treat every value
here as provisional.

---

## 8. Open questions

| Question | Status |
|---|---|
| I²C slave address | **Open.** Not in the document. `0x38` is the family expectation, **not a finding** (§5) |
| Register map, report format, gesture codes | **Open.** Not in the document |
| **How many simultaneous touch points?** | **Open.** "Multi touch" is claimed; no number is given anywhere (§1) |
| What is `SYNC` (pin 32) for? | **Open.** Display-sync is the **[INF]** reading; unconfirmed (§4.1) |
| How is Hibernation exited, given there is no `WAKE` pin? | **Open.** `RSTN` is the only documented path (§2) |
| Are `Tpon`/`Trsi` minima or maxima? | **Open.** §6 — column error suspected. Both readings give the same ≥ 300 ms advice |
| Does a revision later than **V0.1** exist? | **Open.** None located; the document has no revision history |
| Any fitment in this repository? | **No** — §9 |

---

## 9. Used By

**None.** No device in this repository is documented as using an FT3267, and **no fitment is
claimed here.** The datasheet was acquired incidentally while probing the Crystalfontz
controller-document host during Xteink research (§10); it documents the part, not any board.

If you fit one, add a row here and link back from the device record.

---

## 10. Provenance — the URL that lied, and a watermark the text layer hides

| Field | Value |
|---|---|
| Source host | `www.crystalfontz.com` |
| URL form probed | `https://www.crystalfontz.com/controllers/UltraChip/UC8179/<id>/` |
| Numeric id that returned this file | **513** |
| Part the URL claimed | **UltraChip UC8179** (an e-paper driver — unrelated) |
| Part the file actually is | **FocalTech FT3267** |
| Retrieved | **2026-09-11** · re-verified and filed **2026-09-20** |
| SHA-256 | `e3688f3552fddec595fdb4b3eb73f3487a3e8d54b60a48de4a318ca0248743a3` |
| Byte size | **455 700** |
| Pages | 13 |
| Local artifact | `artifacts/ft3267-datasheet-v0.1-crystalfontz-mirror.pdf` |
| Disposition | **repository** (primary, 445 KB, FocalTech publishes nothing equivalent) |
| Licence | **restricted.** Page footer on every page: *"THIS DOCUMENT CONTAINS INFORMATION PROPRIETARY TO FOCALTECH SYSTEMS CO., LTD., AND MAY NOT BE REPRODUCED, DISCLOSED OR USED IN WHOLE OR PART WITHOUT THE EXPRESS WRITTEN PERMISSION OF FOCALTECH SYSTEMS CO., LTD."* **plus** a diagonal **"FOCALTECH CONFIDENTIAL"** watermark on page 1 that is **[DOC-IMG]** only |
| Redistribution status | **restricted** — recorded as metadata per the skill's licensing rule; not adjudicated here |

### Two overlays, one of which only a render will find

**[DOC-IMG]** Page 1 carries:

1. **"FOCALTECH CONFIDENTIAL"**, large, diagonal, grey — **not in the text layer.** `pdftotext`
   returns the page's body text and the footer and nothing else. **This is the strongest single
   argument in this repository for the skill's render-before-you-trust rule:** the artifact's
   licensing status is visible *only* in the raster.
2. The **Crystalfontz banner** — *"This LCD controller datasheet was downloaded from
   https://www.crystalfontz.com/controllers"*. Also raster-only; `pdftotext` finds **zero**
   occurrences of "crystalfontz".

The Crystalfontz banner is a **1700 × 105 RGB image (8 936 B) with a 2 601 B soft mask**, present on
page 1 and no other page, and **byte-identically the same object** in all five documents recovered
from that host (ids 512, 513, 514, 515, 516). Measured 2026-09-20, `executed-success`. It is a
reliable fingerprint for recognising a Crystalfontz copy — and it means **a Crystalfontz copy will
never hash-match the vendor's original even when the content is identical.** See
[FT5436 §10](../ft5436/README.md) for the full measurement and
[SSD1683](../../solomon-systech/ssd1683/README.md) §11 for the worked text-layer comparison that
proves content equivalence despite the hash difference.

**The file is genuine; the URL is worthless as identification.** The measured id→part map is in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md#appended-2026-09-20--crystalfontz-numeric-id-probe-measured)
and [`archive/devices/xteink/shared-artifacts/research-scratch/datasheets/cfprobe/README.md`](../../../archive/devices/xteink/shared-artifacts/research-scratch/datasheets/cfprobe/README.md).

Filed under `components/focaltech/` rather than under the Xteink device that occasioned the fetch,
per the skill's rule: **a file is filed by what it describes.**

---

## 11. Alternatives and family context

| Part | Sensing | Channels | Points | Panel | In this repo |
|---|---|---|---|---|---|
| **FT3267** | **Self (LCST, single layer)** | **22** | "multi", **unstated** | **≤ 1.4″** | this record |
| [FT6336G](../ft6336g/README.md) | Self | 31 | 1 + gestures, or 2 | ≤ 4.0″ | ✅ |
| [FT5436](../ft5436/README.md) | **Mutual** | 16 TX + 25 RX | **10** | ≤ 5.5″ | ✅ |
| [FT3168](../ft3168/README.md) | unread | — | — | small AMOLED | ✅ partial |
| [Hynitron CST816D](../../hynitron/cst816d/README.md) | Self, 13 ch | 13 | 1 + gestures | small round/square | ✅ — **the closest functional substitute, and the one with a known register map** |
| [Goodix GT911](../../goodix/gt911/README.md) | Mutual | — | 5 | larger | ✅ |

**If you are choosing a controller for a ≤ 1.4″ wearable panel today**, the
[CST816D](../../hynitron/cst816d/README.md) is the better-supported option *in this repository*: its
register map is documented (reconstructed from two independent vendor drivers), its gesture codes
are known, and open drivers exist for ESP-IDF, Arduino and LVGL. The FT3267 has none of that here.
**[INF]** — that is a documentation-availability judgement, not a claim about the silicon.

In practice **the controller is chosen by the panel supplier, not by the board designer**. This
table is for understanding what you have, not for substituting it.

---

## Manufacturer

**FocalTech Systems Co., Ltd.** ⚠ **No vendor sourcing guide exists in this repository yet.** See
[FT5436 § Manufacturer](../ft5436/README.md#manufacturer) for the consolidated retrieval findings —
the short version is that **FocalTech does not serve its own datasheets**, and every copy in
circulation is a third-party mirror that blocks, stamps, or misnames.

## Related records

- [FocalTech FT5436](../ft5436/README.md) · [FT6336G](../ft6336g/README.md) · [FT3168](../ft3168/README.md)
- [Sitronix ST7567S](../../sitronix/st7567s/README.md) · [ST7567A](../../sitronix/st7567a/README.md) — the other parts recovered from the same Crystalfontz probe
- [Hynitron CST816D](../../hynitron/cst816d/README.md) — the comparable small-panel self-capacitance controller, with a reconstructed register map

---

## Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| F1 | **FT3267 Self-Capacitive Touch Panel Controller — `D-FT3267-DataSheet-V0.1`** | FocalTech Systems Co., Ltd. | **primary** (via credible mirror) | datasheet | `https://www.crystalfontz.com/controllers/UltraChip/UC8179/513/` — ⚠ **the URL names a different part**; see §10 | 2026-09-11 | **V0.1**, © 2015 (PDF created 2015-12-30) | Everything on this page unless marked otherwise | `artifacts/ft3267-datasheet-v0.1-crystalfontz-mirror.pdf` |
| F2 | Crystalfontz numeric-id probe (`cfprobe`), ids 512–523 | this repository | — | measurement | — | 2026-09-11 / re-verified 2026-09-20 | — | The id→part map, the HTML-under-`.pdf` fall-through, and the page-1 raster stamp | `archive/devices/xteink/shared-artifacts/research-scratch/datasheets/cfprobe/README.md` · [`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md) |

**Local artifacts**

| File | Bytes | SHA-256 | Pages | Licence | Disposition |
|---|---:|---|---:|---|---|
| `artifacts/ft3267-datasheet-v0.1-crystalfontz-mirror.pdf` | 455 700 | `e3688f3552fddec595fdb4b3eb73f3487a3e8d54b60a48de4a318ca0248743a3` | 13 | **restricted** (proprietary footer + `FOCALTECH CONFIDENTIAL` watermark) | repository |

**Reacquire**

```bash
# Primary, verified working 2026-09-20 — note the URL names UC8179, not FT3267
curl -sSL -o ft3267.pdf "https://www.crystalfontz.com/controllers/UltraChip/UC8179/513/"
head -c 5 ft3267.pdf | grep -q '%PDF' || echo "HTML fall-through — not a PDF"
sha256sum ft3267.pdf   # expect e3688f35...
```

> Reacquisition status **`automatic`**. ⚠ The id→document mapping on this host is **not** guaranteed
> stable: it is an internal document id, not a content address. Re-verify by first-page text, never
> by URL. FocalTech itself publishes nothing; no vendor-side fallback exists.
