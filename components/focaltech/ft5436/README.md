# FocalTech FT5436

- **Category:** **mutual-capacitance** ("true multi-touch") projected-capacitive touch-panel
  controller with an on-chip enhanced MCU + DSP accelerator, I²C slave interface
- **Research status:** mined end-to-end from the datasheet now held at `artifacts/`.
  **No board in this repository is known to use it** — see §9. This is a component capability
  record, not a fitment record.
- **Retrieved:** 2026-09-11 (acquired) · **mined and filed:** 2026-09-20
- **Document:** `D-FT5436-DataSheet-V1.0`, © 2015 FocalTech, **Version 1.0 — "1st Preliminary",
  effective 2015-02-06**, 14 PDF pages numbered "Page *n* of 14"

The largest FocalTech touch controller documented in this repository: **16 TX × 25 RX = 41
channels**, **up to 10 fingers**, ≤ 5.5″ 16:9 phone-class panels. Its two siblings here
([FT6336G](../ft6336g/README.md), [FT3267](../ft3267/README.md)) are *self*-capacitance parts for
≤ 4.0″ and ≤ 1.4″ panels respectively; this one is a genuinely different sensing architecture.

> ⚠ **This document arrived under a URL that named a different part.** It was fetched from
> Crystalfontz as `512.pdf` while probing `crystalfontz.com/controllers/UltraChip/UC8179/<id>/`.
> The `<Vendor>/<Part>` path segments on that host are decorative; only the numeric id selects a
> document. See §10 and
> [`ai-crawler-site-access-table.md` § crystalfontz.com](../../../ai-crawler-site-access-table.md#crystalfontzcom--serves-controller-datasheets-and-the-url-lies).

> ⚠ **The document is stamped confidential on every page** and Crystalfontz serves it publicly
> anyway. See §10 — this is recorded as metadata, not adjudicated.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Read out of `artifacts/ft5436-datasheet-v1.0-2015-02-06-crystalfontz-mirror.pdf`, cited by the document's own printed page number |
| **[DOC-IMG]** | Read off a **rendered page image** of that PDF rather than its text layer |
| **[INF]** | Inference from the above. Not stated by FocalTech |
| **[NEG]** | Negative result — something checked for and **not** found |

### Text-layer validation

**[DOC-IMG]** Page 1 was rendered at 150 dpi and compared against `pdftotext -layout` output before
any number below was transcribed. The headings, the feature bullets and the footer
(`Document Number: D-FT5436-DataSheet-V1.0`) match exactly, and `pdfinfo` reports `Pages: 14`
against the printed `Page 14 of 14`. The text layer is trustworthy.

The render also showed **two things the text layer does not contain**: a Crystalfontz banner strip
across the top of page 1 (§10), and — on page 2 onward — the confidentiality footer that *is* in
the text layer. Nothing was lost; the check is recorded because the [FT3267](../ft3267/README.md)
render of the same batch *did* expose a watermark missing from its text layer.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **FocalTech Systems Co., Ltd.** (敦泰科技) | **[DOC]** p.1 header/footer |
| Part | `FT5436` | **[DOC]** p.1, p.13 ordering table |
| Document | **Version 1.0**, `D-FT5436-DataSheet-V1.0`, "1st Preliminary", **effective 6-Feb-2015** | **[DOC]** p.1, p.14 revision history |
| Sensing | **Mutual capacitance**, full-screen common-mode scan | **[DOC]** p.1 |
| Channels | **16 TX + 25 RX = 41 total** | **[DOC]** p.1, p.3, p.13 |
| Touch points | **Up to 10 fingers** | **[DOC]** p.1 |
| Report rate | **> 100 Hz** sampling; Active-mode frame scan **0 – 120 Hz**, host-configurable | **[DOC]** p.1, p.4 |
| Max panel | **≤ 5.5″** at 16:9, **sensor pitch 5 mm** (FocalTech's own recommendation) | **[DOC]** p.3 |
| Package | **QFN-56L, 6 × 6 × 0.6 mm, 0.35 mm pitch**, 4.0 mm exposed pad | **[DOC]** p.1, p.12, p.13 |
| On-chip memory | **64 KB Flash** | **[DOC]** p.1 |
| ADC | **12-bit** | **[DOC]** p.1 |
| Internal oscillator | **50 MHz** ±2 % (49 / 50 / 51 MHz) | **[DOC]** p.7 |
| Operating temperature | **−40 … +85 °C**; storage −55 … +150 °C | **[DOC]** p.1, p.6 |
| ESD | **HBM ±2000 V, MM ±200 V** | **[DOC]** p.1 |
| PDF metadata | `Title: FocalTech Systems Report Template`, `Author: jk.zhang`, Acrobat PDFMaker 9.0 Word 版, created 2015-03-25 | **[DOC]** `pdfinfo` |

> **Read the metadata.** The `Title` is a *report template*, not a datasheet title — the document
> was produced by filling in a generic FocalTech Word template. That is consistent with what §6
> finds: several tables are inherited wholesale from other parts and were not edited for this one.

### 1.1 Channel-count arithmetic — the pin table is a superset, and the gaps are the finding

The ordering table (p.13) says **16 TX, 25 RX**. The pin table (p.9–11) lists **TX1…TX20** and
**RX1…RX28** — more of each. The difference is not an error: **the extra entries carry no pin
number**, i.e. they are bond-out options that exist on a larger family die and are not brought out
on the FT5436.

| Signal group | Listed in pin table | **With a pin number** | Without |
|---|---:|---:|---|
| TX | TX1 – TX20 (20) | **16** | TX17, TX18, TX19, TX20 |
| RX | RX1 – RX28 (28) | **25** | RX26, RX27, RX28 |

20 − 4 = **16 TX**; 28 − 3 = **25 RX**. **[DOC]** p.9–11, **[INF]** for the reading of a blank
pin-number cell as "not bonded out". Per the skill's rule on explicit no-connects versus omissions:
a blank cell is *weaker* evidence than a drawn `NC`, but here it reconciles exactly with the
ordering table, so the two independent statements corroborate. **Do not design a 20 TX / 28 RX
panel from the pin table.**

---

## 2. Power rails — and which ones you actually supply

This is the part of the document most likely to cause a hardware error, because **the pin table
calls seven different nodes "digital power supply"** and only two of them are inputs.

| Pin | Name | Pin table says **[DOC]** p.10–11 | What it actually is |
|---:|---|---|---|
| **10** | **`VDD3`** | "digital power supply, a 1 µF ceramic capacitor to ground is required" | **The main supply input, 2.7 – 3.6 V.** The only rail in the DC table with a stated range **[DOC]** p.6–7 |
| **13** | **`IOVCC`** | "I/O power supply" | **The host-interface rail, 1.8 – 3.6 V, independent of `VDD3`** **[DOC]** p.1, p.6 |
| 9 | `VDD10` | "digital power supply … 1 µF required" | Internal regulator node **[INF]** |
| 11 | `VDD15` | ditto | Internal 1.5 V digital rail — the overview says *"a voltage regulator to generate 1.5 V for digital circuits from the input VDD3 supply"* **[DOC]** p.4 |
| 12 | `VDD18` | ditto | Internal regulator node **[INF]** |
| 56 | `VDD5_IN` | "**internal generated** 5V power supply, a 1 µF ceramic capacitor to ground is required" | Charge-pump node **[DOC]** |
| 1 | `VDD5_Out` | "digital power supply … 1 µF required" | Charge-pump output **[INF]** |
| 57 | `VSSLF` | "analog ground" | **[DOC]** |
| — | `VSSA` | appears only in the package diagram (p.12), **not in the pin table** | **[NEG]** |

**[INF] Practical reading:** supply **`VDD3`** and **`IOVCC`**. Decouple `VDD5_IN`, `VDD5_Out`,
`VDD10`, `VDD15` and `VDD18` with 1 µF each and drive none of them. Evidence: only `VDD3` and
`IOVCC` appear in the absolute-maximum and DC tables (p.6), `VDD5_IN` is explicitly described as
internally generated, and the architecture text names exactly one regulator input (`VDD3`).
**This is an inference from a document that does not draw a power-tree diagram, and it is the
single biggest thing to confirm against a reference schematic before laying out a board.**

### 2.1 ⚠ The "Absolute Maximum Ratings" table is not absolute maxima

**[DOC]** p.6, Table 3-1 is titled *Absolute Maximum Ratings* and lists:

| Item | Symbol | Value |
|---|---|---|
| Power Supply Voltage | `VDD3 – VSS` | **2.7 ~ 3.6 V** |
| I/O Digital Voltage | `IOVCC` | **1.8 ~ 3.6 V** |
| Operating Temperature | `Topr` | −40 ~ +85 °C |
| Storage Temperature | `Tstg` | −55 ~ +150 °C |

A 2.7 V **lower bound** in an absolute-maximum table is meaningless — absolute maxima are stress
limits, and the lower bound of a stress limit is not the bottom of the operating window. These are
**operating** ranges printed under the wrong heading; the same numbers reappear as operating values
in the DC table on p.7 (`VDD3` min 2.7, max 3.6). **[DOC]** p.6, p.7, **[INF]** for the diagnosis.

**Consequence:** the document states **no** true stress rating — no `VSS − 0.3 V` floor, no
`IOVCC + 0.3 V` ceiling on the digital pins. **[NEG]** Compare [FT3267](../ft3267/README.md#3-electrical),
whose table for the same fields *does* carry `−0.3 ~ +3.6 V`. If you need a stress limit for
FT5436, you do not have one.

### 2.2 DC and current

**[DOC]** p.6–7, Table 3-2.

| Item | Symbol | Value |
|---|---|---|
| Input high | `VIH` | 0.7 × `IOVCC` … `IOVCC` |
| Input low | `VIL` | −0.3 … 0.3 × `IOVCC` |
| Output high | `VOH` | ≥ 0.7 × `IOVCC` at **`IOH` = 3 mA** |
| Output low | `VOL` | ≤ 0.3 × `IOVCC` at **`IOL` = 4.5 mA** |
| I/O leakage | `ILI` | ±1 µA |
| **Active current** | `Iopr` | **11 mA** typ |
| **Monitor current** | `Imon` | **0.43 mA** typ |
| **Sleep current** | `Islp` | **42 µA** typ |

> ⚠ **The current figures are for a panel this part cannot be ordered with.** The table's own note:
> *"Values shown are typical for a **15 Tx × 24 Rx** sensor configured at 80 Hz report rate."*
> **[DOC]** p.7. The FT5436 is a 16 × 25 part. The numbers are indicative, not a specification for
> a full-channel design, and FocalTech says outright that *"actual current will depend on the
> particular sensor design and firmware options."*

Note the output drive: **3 mA sourcing / 4.5 mA sinking** is unusually strong for a touch
controller's `/INT`, and roughly 30–45× the [FT3267](../ft3267/README.md)'s ±0.1 mA. **[DOC]**

### 2.3 Two DC rows that do not make sense as printed

**[NEG]/[DOC]** p.7:

```
Step-up output voltage    VDD5    V    VDD3 = 2.8V    (typ) 0.25
Step-up output voltage    VDD10   V    VDD3 = 2.8V    (typ) 0.5
```

A *step-up* output of **0.25 V** and **0.5 V** from a 2.8 V input is not a step-up. The sibling
[FT3267](../ft3267/README.md) prints the analogous row as `VDD5 … 5 V`, which is coherent. The most
likely reading is that these are **tolerance** figures (±0.25 V, ±0.5 V) whose nominal values were
dropped in editing. **This is not resolved; both columns are recorded as printed and the values are
not usable.**

---

## 3. Analogue front end — TX/RX limits that constrain panel design

**[DOC]** p.1, p.7.

| Parameter | Value |
|---|---|
| Single-channel (TX or RX) **resistance** | up to **100 kΩ** |
| Single-channel (TX or RX) **capacitance** | **40 pF** |
| `ftx` — TX drive clock | **50 – 400 kHz**, typ 150 kHz |
| `Ttxr` / `Ttxf` — TX rise/fall | **210 ns** typ |
| RX input voltage | **1.2 – 1.6 V** |
| Ground shield | **not required** — *"supports various type of panels with no ground shielding layer"* |
| Diagnostics | *"short I/O testing for sense pins"* — a production short-test mode |

The 100 kΩ / 40 pF per-channel budget is the number that decides whether a given ITO or metal-mesh
stack-up will work; it is stated once, on the feature page, and nowhere expanded. **[DOC]** p.1.

> ⚠ The RX row is labelled **`Trxi`** — a *time* symbol — but carries **volts**. **[DOC]** p.7.
> The same mislabelled symbol appears in the [FT3267](../ft3267/README.md) table, which is direct
> evidence that both tables descend from one template.

---

## 4. Host interface

### 4.1 Signals

**[DOC]** p.4–5, p.11.

| Pin | Signal | Type | Behaviour |
|---:|---|---|---|
| 19 | `SDA` | I/O | I²C data. Open-drain behaviour is a **firmware-selected** port mode, not fixed hardware — *"the firmware can also control its output behavior as push-pull or as open-drain that SDA of I2C interface is required"* **[DOC]** p.8 |
| 20 | `SCL` | I/O | I²C clock input |
| 21 | **`RSTN`** | I | **External reset, active low.** Also the wake path out of Sleep |
| 15 | **`INT`** | **I/O** | See §4.3 — **this pin is bidirectional and that is the trap** |
| 14 | `UART` | I/O | "UART port". Single pin, otherwise **undocumented** **[NEG]** |
| 16 | `GPIO3` | I/O | General-purpose |
| 17 | `GPIO2` | I/O | General-purpose, **supports PS2_Data** |
| 18 | `GPIO1` | I/O | General-purpose, **supports PS2_CLK** |

The PS/2 capability on `GPIO1`/`GPIO2` is stated only in the pin table and is not described
anywhere else in the document. **[NEG]** It is presumably a touchpad (notebook) application path.
**[INF]**

Port structures are given as **figures with bare value labels and no topology text**: Figure 3-2
(reset input) labels **`IOVCC`**, **50 kΩ** and **300**; Figure 3-1 (general-purpose I/O) labels
**`IOVCC`**, **`VDDA`** and **2 MΩ**. **[DOC]** p.8. The obvious reading — a 50 kΩ pull-up to
`IOVCC` with 300 Ω in series on `RSTN`, and a 2 MΩ pull element on general I/O — is **[INF]**, not
stated. The **values** are `[DOC]`; the **arrangement** is not.

### 4.2 I²C

**[DOC]** p.5–6. Plain 7-bit I²C slave, no second interface.

| Parameter | Min | Max |
|---|---:|---:|
| `SCL` frequency | **0** | **400 kHz** |
| Bus free, STOP → START | 1.3 µs | — |
| (Repeated) START hold | 0.6 µs | — |
| Data setup | 100 ns | — |
| Repeated-START setup | 0.6 µs | — |
| STOP setup | 0.6 µs | — |

These are **Fast-mode** figures and are internally consistent with the 400 kHz ceiling. Worth
contrasting with [FT3267](../ft3267/README.md) and [FT6336G](../ft6336g/README.md), whose tables
claim the same 400 kHz ceiling while quoting **Standard-mode** spacing (4.7 µs / 4.0 µs / 250 ns) —
a family-wide inconsistency, and FT5436 is the copy that is right. **[DOC]**

### 4.3 ⚠ `INT` is bidirectional and is the documented wake pin

The pin table types `INT` as **`I/O`** and describes it as *"Interrupt request to the host, **or
Wakeup request from the host**."* **[DOC]** p.11. §2.3 then says Sleep mode *"shall only respond to
the 'RESET', 'INT' signal from the host processor."* **[DOC]** p.4.

Two consequences, both easy to get wrong:

1. **You cannot wire `INT` to a host pin that is permanently an input** if you intend to use Sleep
   mode. The host has to be able to drive it.
2. **You cannot fit a hard pull-up/pull-down on `INT` that the host cannot override**, and you
   cannot share it with another interrupt source without arbitration.

⚠ **§2.4 contradicts this.** Two paragraphs earlier the same document says *"The `/RST` signal is
used for the host to wake up FT5436 from the Sleep mode"* and describes `/INT` as
FT5436 → host only. **[DOC]** p.5. **Conflict recorded, not resolved.** The pin table is the more
specific statement and is corroborated by the `I/O` type; the safe implementation is to wire **both**
`RSTN` and `INT` to driveable host GPIOs and use `RSTN` for wake. The evidence that would settle it
is a scope capture on real hardware.

### 4.4 Operating modes

**[DOC]** p.4.

| Mode | Behaviour | Typ. current |
|---|---|---|
| **Active** | Frame scan **0 – 120 Hz**, host-configurable | 11 mA |
| **Monitor** | Most algorithms stopped; a simple presence detector runs. Enters Active immediately on touch. ⚠ **"the serial port is closed and no data shall be transferred with the host processor"** | 0.43 mA |
| **Sleep** | Responds only to `RESET` / `INT` from the host | 42 µA |

Mode switching is **automatic** — the feature list says so explicitly ("Automatic mode switching
(Active, Monitor, Sleep)") **[DOC]** p.1 — which means the host can find the I²C port closed at any
   moment without having asked for it.

> ⚠ **A poll that returns nothing is not the same as "no touch".** Because Monitor mode closes the
> port and the part enters it by itself, a polled driver *must* distinguish a NACK from a
> zero-touch report. **Design for `INT`-driven reads.** This is the same architecture as
> [FT6336G](../ft6336g/README.md) §2.2 and the same trap.

---

## 5. ⚠ Report protocol and register map — they are not in this document

**[NEG]** **Version 1.0 of the FT5436 datasheet contains no I²C slave address, no register map, no
touch-report format and no gesture table.** Full-text search of all 14 pages finds no `0x38`, no
slave-address value, no register table, and no byte-level description of a touch packet. The
document covers architecture, modes, electricals, I²C *framing and timing*, pinout and package —
and stops, exactly as [FT6336G](../ft6336g/README.md) §2.1 records for its part.

What the document *does* fix about the protocol:

- **I²C slave, 7-bit addressing**, `A[6:0]` + R/W bit, byte stream with per-byte ACK, master-write
  and master-read forms both drawn. **[DOC]** p.5, Figures 2-4 / 2-5 / 2-6.
- **No register-pointer convention is shown.** The write figure is `S · addr · W · D[n] · D[n+1] ·
  D[n+2] · P` — a bare byte stream with no leading register byte. **[DOC]** p.5. Whether the first
  data byte is a register address is *not stated*.
- Touch data is signalled ready by `/INT`, not by polling a status bit. **[DOC]** p.4.

**Practical consequence:** you cannot write an FT5436 driver from this datasheet. Use an existing
FT5x06-family driver, or obtain FocalTech's separate register application note (distributed
per-customer, typically under NDA — the same situation as FT6336G).

**Not claimed here:** that the address is `0x38`, or that the FT5x06 6-bytes-per-point layout
applies. Both are *likely* — `0x38` is the long-standing family address and the FT5x06 driver family
is what downstream code uses — but this repository holds **no evidence** for the FT5436
specifically, and the skill's rule against promoting a candidate to a finding applies. See §8 for
what would settle it.

---

## 6. Initialisation and reset — the timing that breaks naïve drivers

**[DOC]** p.8–9, §3.5 and Table 3-5.

| Symbol | Description | Min | Max | Unit |
|---|---|---:|---:|---|
| `Tris` | Supply rise, 0.1 `VDD` → 0.9 `VDD` | — | **5** | ms |
| `Tpdt` | Time supply must stay **below 0.3 V** during a power cycle | **5** | — | ms |
| **`Trtp`** | **Reset held low before power-on** | **100** | — | **µs** |
| `Tvdr` | Reset time after `VDD` power-on | **1** | — | ms |
| **`Trsi`** | Time to first reported point **after reset** | — | **200** | **ms** |
| `Trst` | Reset pulse width | **1** | — | ms |

The prose rules that go with them, quoted because each is a separate failure mode **[DOC]** p.8:

1. **"Reset should be pulled down to be low before powering on and powering down."**
   `RSTN` must be asserted *before* the rail comes up (≥ `Trtp` = 100 µs) **and before it goes
   down**. A design that leaves `RSTN` floating or pulled high through power transitions is outside
   spec in both directions.
2. ⚠ **"I2C shouldn't be used by other devices during Reset time after VDD powering on (Trtp)."**
   **This is a bus-level constraint, not a device-level one.** On a shared I²C bus you must hold off
   *every other slave* for the reset window at power-up. Most integrations never do this.
3. **"INT signal will be sent to the host after initializing all parameters and then start to report
   points to the host."** — so the correct bring-up is *wait for the first `/INT`*, not "sleep and
   hope". `Trsi` (≤ 200 ms) is the bound on how long that takes.
4. **"If Power is down, the voltage of supply must be below 0.3V and `Tpdt` is more than 1ms."**
   ⚠ The prose says **1 ms**; the table says **`Tpdt` min = 5 ms**. **[DOC]** p.8 vs p.9.
   **Conflict recorded, not resolved — use the larger value, 5 ms.** A brown-out that dips to
   0.5 V and recovers leaves the part in an undefined state.

**[INF] Minimum safe sequence**, assembled from the above; **`not-tested`**, no hardware was available:

```text
RSTN = 0                      # before the rail
wait >= 100 us                # Trtp
VDD3, IOVCC on                # rise within Tris <= 5 ms
wait >= 1 ms                  # Tvdr
RSTN = 1                      # pulse width already satisfied; Trst >= 1 ms if re-pulsing
wait for /INT  (bound: Trsi <= 200 ms)   # do NOT poll I2C before this
```

Note what is **absent** from this datasheet and present in others: there is **no** "read the chip-ID
register and log it" step available, because there is no documented ID register (§5). You cannot
tell a dead part from an idle one at bring-up. **[NEG]**

---

## 7. Document defects, collected

Each of these is cited above; gathered here so nobody re-derives them.

| # | Defect | Where |
|---|---|---|
| 1 | "Absolute Maximum Ratings" table contains **operating** ranges; no true stress limits exist in the document | p.6 · §2.1 |
| 2 | `VDD5` / `VDD10` "step-up output voltage" typicals of **0.25 V / 0.5 V** are incoherent | p.7 · §2.3 |
| 3 | RX input **voltage** row carries the time symbol **`Trxi`** | p.7 · §3 |
| 4 | Current figures are specified for a **15 × 24** sensor; the part is **16 × 25** | p.7 · §2.2 |
| 5 | `INT` described as host→chip wake in the pin table, chip→host only in §2.4 | p.5 vs p.11 · §4.3 |
| 6 | `Tpdt` given as **1 ms** in prose and **5 ms** in the table | p.8 vs p.9 · §6 |
| 7 | Seven distinct nodes all called "digital power supply" | p.10–11 · §2 |
| 8 | `VSSA` appears in the package diagram but not the pin table | p.12 vs p.9–11 · §2 |
| 9 | PDF `Title` is `FocalTech Systems Report Template` | metadata · §1 |
| 10 | Marked **"1st Preliminary"** — and no later revision is known to exist | p.14 · §8 |

Ten defects in fourteen pages. **[INF]** Treat every number here as needing confirmation against a
reference design before committing silicon.

---

## 8. Open questions

| Question | Status |
|---|---|
| I²C slave address | **Open.** Not in the document. `0x38` is the family expectation, **not a finding** (§5) |
| Register map / touch-report format | **Open.** Not in the document. Needs FocalTech's register application note or a working open driver identified *for FT5436 specifically* |
| Is `INT` genuinely a host-driven wake input? | **Open.** §4.3 — the document contradicts itself |
| What is the `UART` pin for? | **[NEG]** Named in the pin table, described nowhere |
| Is the PS/2 mode on `GPIO1/2` usable, and how is it selected? | **[NEG]** Named in the pin table, described nowhere |
| Does a revision later than V1.0 "1st Preliminary" exist? | **Open.** The revision history has exactly one row (p.14). Nothing newer was located |
| Which rails are inputs versus internal nodes? | **[INF]** §2 — reasoned, not stated. Confirm against a reference schematic |
| Any fitment in this repository? | **No** — §9 |

---

## 9. Used By

**None.** No device in this repository is documented as using an FT5436, and **no fitment is
claimed here.** The datasheet was acquired incidentally while probing the Crystalfontz
controller-document host during Xteink research (§10); it documents the part, not any board.

If you fit one, add a row here and link back from the device record.

---

## 10. Provenance — the URL that lied, and a stamp that is not in the text layer

| Field | Value |
|---|---|
| Source host | `www.crystalfontz.com` |
| URL form probed | `https://www.crystalfontz.com/controllers/UltraChip/UC8179/<id>/` |
| Numeric id that returned this file | **512** |
| Part the URL claimed | **UltraChip UC8179** (an e-paper driver — unrelated) |
| Part the file actually is | **FocalTech FT5436** |
| Retrieved | **2026-09-11** · re-verified and filed **2026-09-20** |
| SHA-256 | `5aa25ca793a16efcc1a63926c91add366cfc5985b289575df604770a78595933` |
| Byte size | **376 328** |
| Pages | 14 |
| Local artifact | `artifacts/ft5436-datasheet-v1.0-2015-02-06-crystalfontz-mirror.pdf` |
| Disposition | **repository** (primary, 368 KB, FocalTech publishes nothing equivalent) |
| Licence | **restricted.** Every page carries *"THIS DOCUMENT CONTAINS CONFIDENTIAL AND PRIVILEGED INFORMATION. UNAUTHORIZED USE, COPY OR DISCLOSURE IS PROHIBITED"*, plus `Copyright © 2015, FocalTech Systems Co., Ltd. All rights reserved` |
| Redistribution status | **restricted** — recorded as metadata per the skill's licensing rule; not adjudicated here |

### The Crystalfontz page-1 stamp

**[DOC-IMG]** Crystalfontz adds a banner across the top of **page 1 only**:

> *Crystalfontz — This LCD controller datasheet was downloaded from
> https://www.crystalfontz.com/controllers*

It is a **raster overlay** — `pdfimages -list` shows a **1700 × 105 RGB image (8 936 B) plus a
2 601 B grayscale soft mask** on page 1 and on no other page, while `pdftotext` finds **zero**
occurrences of "crystalfontz" anywhere in the document. **A text-only check will not detect that
this copy has been modified.**

**Measured 2026-09-20 (`executed-success`):** that image/smask pair, at byte-identical sizes,
appears on page 1 of **every** document recovered from this host — **FT5436** (id 512),
[FT3267](../ft3267/README.md) (513),
[SSD1683](../../solomon-systech/ssd1683/README.md) (514),
[ST7567S](../../sitronix/st7567s/README.md) (515) and
[ST7567A](../../sitronix/st7567a/README.md) (516). It is a host-wide stamp, not a per-document one,
and the 8 936 B / 2 601 B pair is a reliable **fingerprint for recognising a Crystalfontz copy**.

**Consequence for deduplication:** any Crystalfontz copy of a datasheet will differ in bytes from
the vendor's original *even when the content is identical*, and the difference is one image object
on page 1. A hash mismatch against another mirror is therefore **expected** and is **not** evidence
of a different revision. Compare text layers before concluding anything. (This is exactly what the
id-514 comparison in [SSD1683](../../solomon-systech/ssd1683/README.md) §11 found.)

**The file is genuine; the URL is worthless as identification.** Every numbered document on that
host must be identified by content before filing. The measured id→part map is in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md#appended-2026-09-20--crystalfontz-numeric-id-probe-measured)
and [`archive/devices/xteink/shared-artifacts/research-scratch/datasheets/cfprobe/README.md`](../../../archive/devices/xteink/shared-artifacts/research-scratch/datasheets/cfprobe/README.md).

Filed under `components/focaltech/` rather than under the Xteink device that occasioned the fetch,
per the skill's rule: **a file is filed by what it describes.**

---

## 11. Alternatives and family context

| Part | Sensing | Channels | Points | Panel | In this repo |
|---|---|---|---|---|---|
| **FT5436** | **Mutual** | 16 TX + 25 RX | **10** | ≤ 5.5″ | this record |
| [FT6336G](../ft6336g/README.md) | Self | 31 | 1 + gestures, or 2 | ≤ 4.0″ | ✅ |
| [FT3267](../ft3267/README.md) | Self | 22 | multi (count unstated) | ≤ 1.4″ | ✅ |
| [FT3168](../ft3168/README.md) | self/mutual, unread | — | — | small AMOLED | ✅ partial |
| [Hynitron CST816D](../../hynitron/cst816d/README.md) | Self | 13 | 1 + gestures | small | ✅ |
| [Goodix GT911](../../goodix/gt911/README.md) | Mutual | — | 5 | — | ✅ |

**Mutual versus self is the axis that matters.** Only the mutual-capacitance parts (FT5436, GT911)
give genuinely independent multi-point tracking; self-capacitance parts suffer the classic
two-point ghosting ambiguity and the family datasheets reflect that by quoting "1 point + gestures".
**[INF]**, standard projected-capacitive theory, not stated by FocalTech.

In practice **the controller is chosen by the panel supplier, not by the board designer**. This
table is for understanding what you have, not for substituting it.

---

## Manufacturer

**FocalTech Systems Co., Ltd.** ⚠ **No vendor sourcing guide exists in this repository yet** — the
gap is recorded in [`components/README.md`](../../README.md). The retrieval findings that would seed
one are currently split across three records:

- [FT6336G § Manufacturer](../ft6336g/README.md#manufacturer) — `orientdisplay.com` and
  `focuslcds.com` both 403 ordinary browser UAs; only a **ClaudeBot** UA succeeded, and only on
  `focuslcds.com`.
- **This record and [FT3267](../ft3267/README.md)** — `crystalfontz.com` serves FocalTech datasheets
  by opaque numeric id with no vendor/part validation, and stamps page 1.
- [FT3168](../ft3168/README.md) — LilyGO's board repositories mirror FocalTech PDFs.

Common thread: **FocalTech does not serve its own datasheets.** Every copy in circulation is a
third-party mirror, and the mirrors block, stamp, or misname.

## Related records

- [FocalTech FT6336G](../ft6336g/README.md) · [FT3267](../ft3267/README.md) · [FT3168](../ft3168/README.md)
- [Sitronix ST7567S](../../sitronix/st7567s/README.md) · [ST7567A](../../sitronix/st7567a/README.md) — the other parts recovered from the same Crystalfontz probe
- [Hynitron CST816D](../../hynitron/cst816d/README.md) — a comparable small-panel controller whose datasheet *also* lacks a register map, and where the map was reconstructed from driver source instead

---

## Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| F1 | **FT5436 True Multi-Touch Capacitive Touch Panel Controller — `D-FT5436-DataSheet-V1.0`** | FocalTech Systems Co., Ltd. | **primary** (via credible mirror) | datasheet | `https://www.crystalfontz.com/controllers/UltraChip/UC8179/512/` — ⚠ **the URL names a different part**; see §10 | 2026-09-11 | **V1.0, effective 2015-02-06**, © 2015 | Everything on this page unless marked otherwise | `artifacts/ft5436-datasheet-v1.0-2015-02-06-crystalfontz-mirror.pdf` |
| F2 | Crystalfontz numeric-id probe (`cfprobe`), ids 512–523 | this repository | — | measurement | — | 2026-09-11 / re-verified 2026-09-20 | — | The id→part map, the HTML-under-`.pdf` fall-through, and the page-1 raster stamp | `archive/devices/xteink/shared-artifacts/research-scratch/datasheets/cfprobe/README.md` · [`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md) |

**Local artifacts**

| File | Bytes | SHA-256 | Pages | Licence | Disposition |
|---|---:|---|---:|---|---|
| `artifacts/ft5436-datasheet-v1.0-2015-02-06-crystalfontz-mirror.pdf` | 376 328 | `5aa25ca793a16efcc1a63926c91add366cfc5985b289575df604770a78595933` | 14 | **restricted** (confidentiality notice on every page) | repository |

**Reacquire**

```bash
# Primary, verified working 2026-09-20 — note the URL names UC8179, not FT5436
curl -sSL -o ft5436.pdf "https://www.crystalfontz.com/controllers/UltraChip/UC8179/512/"
# Validate: the host returns HTML with a .pdf-looking URL for out-of-range ids
head -c 5 ft5436.pdf | grep -q '%PDF' || echo "HTML fall-through — not a PDF"
sha256sum ft5436.pdf   # expect 5aa25ca7...
```

> Reacquisition status **`automatic`**. ⚠ The id→document mapping on this host is **not** guaranteed
> stable: it is an internal document id, not a content address. Re-verify by first-page text, never
> by URL. FocalTech itself publishes nothing; no vendor-side fallback exists.
