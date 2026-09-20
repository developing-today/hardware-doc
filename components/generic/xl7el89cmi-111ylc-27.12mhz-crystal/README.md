# XL7EL89CMI-111YLC — 27.12 MHz crystal for the ST25R3916 NFC front end

> **27.12 MHz quartz crystal**, YXC `XL7EL89CMI-111YLC` series, **SMD2016-4P** (2.0 × 1.6 mm, 4 pad), **10 pF load**, ±10/±20 ppm, −40 to +85 °C.
> Research snapshot **2026-09-01**. Fitted as **`X1` on sheet 6** of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) — the reference for the [ST25R3916](../../stmicroelectronics/st25r3916/README.md) NFC reader on the NFC sub-board.
> ⚠ **The 27.12 MHz variant is not in any catalogue reached; the datasheet held is for the same series at a different frequency.** See [§2](#2--what-was-and-was-not-obtained). **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | YXC `XL7EL89CMI-111YLC-24M` datasheet, local copy `artifacts/xl7el89cmi-111ylc-24m-yxc-lcsc-mirror.pdf` — ⚠ **24 MHz variant, image-only** | `not-tested` |
| **[CAT]** | LCSC / JLCPCB catalogue entries `C2965581` (-24M), `C2965583` (-32M), retrieved 2026-09-01 | `not-tested` |
| **[SCH-V]** | Read off sheet 6 rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[SCH-T]** | Read from the schematic text layer | `executed-success` for the extraction |
| **[ST]** | ST **DS12484** ST25R3916 datasheet, held under the [ST25R3916 record](../../stmicroelectronics/st25r3916/README.md) | `not-tested` |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Value string on the schematic | **`27.12MHZ(XL7EL89CMI-111YLC)`** | **[SCH-T]**, **[SCH-V]** |
| **Frequency** | **27.12 MHz** | **[SCH-V]** |
| Manufacturer | **YXC Crystal Oscillators** (扬兴科技, Yangxing) | **[CAT]** |
| Series | `XL7EL89CMI-111YLC` | **[CAT]** |
| Package | **SMD2016-4P** — 2.0 × 1.6 mm, 4 pads | **[CAT]** |
| **Load capacitance C<sub>L</sub>** | **10 pF** | **[CAT]** |
| Frequency tolerance | **±10 ppm** | **[CAT]** |
| Frequency stability | **±20 ppm** over temperature | **[CAT]** |
| ESR | 100 Ω (‑24M) / 80 Ω (‑32M) — **frequency-dependent, §2** | **[CAT]** |
| Operating temperature | **−40 °C to +85 °C** | **[CAT]** |
| Reference designator | **`X1`**, sheet 6 | **[SCH-V]** |

### 1.1 The ordering code carries the frequency as a suffix

LCSC lists `XL7EL89CMI-111YLC-**24M**` and `XL7EL89CMI-111YLC-**32M**`. The base
code names the *package, load capacitance and grade*; the frequency is appended.
So the part on this board is, by construction, **`XL7EL89CMI-111YLC-27.12M`**.

That form is **not asserted as a confirmed orderable part number** — it was not
found in any catalogue (§2) — but the decomposition itself is established from
two siblings that differ only in the suffix. **[INF]**

---

## 2. ⚠ What was and was not obtained

| | Status |
|---|---|
| **The 27.12 MHz variant's own datasheet** | **Not found.** No catalogue reached lists the part at this frequency |
| The series datasheet, via the 24 MHz sibling | **Obtained** — `artifacts/xl7el89cmi-111ylc-24m-yxc-lcsc-mirror.pdf`, 535 394 B, 1 page |
| That document's text layer | **⚠ None.** `pdftotext` extracts **0 bytes**; the page is a scan or vector outline |

Consequently **every number in §1 comes from LCSC's parametric fields**, not from
YXC's own text, and the retained PDF is useful only as a page image.

**Two properties transfer across the series and two do not.**

| Property | Transfers from the ‑24M document? | Why |
|---|---|---|
| Package, pad layout, dimensions | **Yes** — SMD2016-4P is the series' package | |
| Load capacitance C<sub>L</sub> = 10 pF | **Yes** — the `YLC` field encodes it, and both siblings share it | |
| **ESR** | **No** — 100 Ω at 24 MHz, 80 Ω at 32 MHz; **27.12 MHz is between them and its value is unknown** | ESR falls with frequency in a series like this |
| **Drive level, C<sub>0</sub>, ageing** | **No** — unread; the document has no text layer | |

**Search attempts, all 2026-09-01:**

| Attempt | Result |
|---|---|
| JLCPCB SMT parts API, `XL7EL89CMI-111YLC` | 2 results: **‑24M** and **‑32M** only. No 27.12 MHz SKU |
| Same API, the base code without suffix | same 2 results |
| DuckDuckGo-lite, Mojeek, searx.be via `curl` | **all blocked or captcha'd**; no general web search succeeded |

**What would resolve it:** YXC's own catalogue (`yxc-crystal.com`), a Chinese
crystal distributor listing the 27.12 MHz SKU, or M5Stack's BOM.

---

## 3. Why 27.12 MHz is load-bearing

**NFC's carrier is 13.56 MHz**, defined by ISO/IEC 14443 and ISO/IEC 15693.
**27.12 MHz is exactly 2 ×** that, and the ST25R3916 divides it down internally
to synthesise the carrier and to clock its receiver.

This is not a "system clock" that can be any convenient value. Consequences:

1. **The frequency is fixed by the standard, not by the design.** 24 MHz or
   26 MHz — both far commoner crystal values, and both stocked by the same
   vendor — will not work. The ST25R3916 requires 27.12 MHz.
2. **Carrier accuracy is inherited directly from the crystal.** ISO/IEC 14443
   specifies the carrier as 13.56 MHz **± 7 kHz**, i.e. about **±516 ppm**. The
   crystal's ±10 ppm initial tolerance and ±20 ppm temperature stability are
   comfortably inside that, with roughly **17× margin** on the total ±30 ppm
   worst case. **[INF]** — the ±7 kHz figure is the standard's, quoted from
   general knowledge of ISO 14443 and **not** read from **[ST]** for this record.
3. **Subcarrier timing depends on it too.** The 847.5 kHz load-modulation
   subcarrier is f<sub>c</sub>/16, and bit timing is derived in carrier periods.
   A crystal error scales all of it together, which is why the margin above is
   generous — but it also means **a wrong crystal does not degrade gracefully;
   it fails to communicate at all.**
4. **A drop-in replacement must be 27.12 MHz.** This is the single most important
   line in this record.

---

## 4. Used By

### `devices/m5stack/papermono` — `X1`, sheet 6

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md), on
the **NFC sub-board** (`02 Paper Mono NFC.SchDoc`, `Paper Mono NFC`, `2/2`,
`V0.2`, dated **2026-07-28**), which reaches the mainboard through the
[`BTB0.408-10PLBDR-G41`](../btb0.408-10plbdr-g41/README.md) board-to-board pair.

**On the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md):
NO.** The Lite drops NFC entirely — that and LoRa are the whole difference
between the SKUs. There is no NFC sub-board, so no crystal.

> ⚠ **Sheet 6 has its own `X1`**, unrelated to `X1` on sheet 3 (the
> `CN4040M000157A530001` 40 MHz crystal for the ESP32-S3). The PDF concatenates
> three separate Altium documents; see the
> [BOM's designator-collision table](../../../devices/m5stack/papermono/bill-of-materials.md#3--designators-repeat-across-sheets--a-designator-alone-is-meaningless).

### 4.1 Connections **[SCH-V]**

| `X1` pin | Net | Notes |
|---:|---|---|
| **2** | **`XTO`** — ST25R3916 **pin 4** | with **`C14` = 10 pF** to GND |
| **3** | **`XTI`** — ST25R3916 **pin 5** | with **`C15` = 10 pF** to GND |
| 1, 4 | **GND** | the case/shield pads of the 4-pad package |

Nothing else is in the loop: no series resistor, no external feedback network —
the ST25R3916 contains its own oscillator amplifier.

### 4.2 ⚠ The load capacitors and the specified C<sub>L</sub> do not obviously agree

`C14` = `C15` = **10 pF**, and the crystal's specified **C<sub>L</sub> = 10 pF**.
**[SCH-V]**, **[CAT]**

For a parallel-resonant crystal the oscillator presents

> C<sub>L</sub> ≈ (C1 × C2) / (C1 + C2) + C<sub>stray</sub>

With C1 = C2 = 10 pF that is **5 pF + C<sub>stray</sub>**. Reaching 10 pF would
need about **5 pF of stray**, which is high for a compact 0402-populated layout
but not impossible once the IC's own pin capacitance and the PCB traces are
counted — and the ST25R3916's `XTI`/`XTO` pins contribute several pF of their
own.

**Three readings, none adopted:**

| Reading | Comment |
|---|---|
| The stray really is ~5 pF | Plausible on a small dense sub-board with an IC that has significant pin capacitance |
| ST specifies the external capacitors directly, and 10 pF is ST's recommended value rather than a computed one | ST's application notes for the ST25R39xx family do give recommended values; **not checked against [ST] for this record** |
| The crystal's true C<sub>L</sub> at 27.12 MHz differs from the 10 pF LCSC lists for the ‑24M/‑32M siblings | Possible, since §2 shows ESR does vary across the series |

**Practical consequence if the first reading is wrong:** the oscillator would run
**fast** — pulling a crystal with too little load capacitance raises its
frequency. A few tens of ppm would still be inside the ±516 ppm the carrier
tolerates (§3), so this would most likely be invisible rather than fatal.
**[INF]** Recorded as an open question, not as a defect.

### 4.3 Supporting evidence: the sheet's own annotations

Sheet 6 is unusually forthcoming and worth quoting, because it settles several
things about the NFC front end without needing measurement **[SCH-T]**:

- *"Supply current in Power-down mode: I = 2.5 µA — When Operation control
  register (en=0)"*
- *"Communication mode: `I2C_EN`=VDD ⇒ I²C mode; `I2C_EN`=GND ⇒ SPI mode"* —
  and `R4` = 0 Ω ties `I2C_EN` to `VCC_3V3`, **selecting I²C**
- Antenna construction: *"Turns: 4 · Antenna Length: 25 mm · Antenna Width: 25 mm
  · Line Width: 0.25 mm · Line Spacing: 0.3 mm · Thickness: 17 µm (0.5 oz)"*

---

## 5. Substitution

**Must be 27.12 MHz** (§3). Beyond that:

| Property | Requirement |
|---|---|
| Frequency | **27.12 MHz — non-negotiable** |
| C<sub>L</sub> | match whatever `C14`/`C15` were designed around (§4.2) — **changing C<sub>L</sub> without changing the capacitors pulls the frequency** |
| Tolerance / stability | ±10 / ±20 ppm as fitted; ISO 14443 allows far more (§3), so this is not tight |
| ESR | **unknown at 27.12 MHz** (§2) — a higher-ESR part risks unreliable start-up |
| Package | SMD2016 (2.0 × 1.6 mm) 4-pad |

27.12 MHz crystals in 2016 are a standard NFC-market item from Abracon (`ABM8`),
NDK, Epson, TXC, Hosonic and others, and any ST25R39xx reference design names
one. **Prefer a part whose datasheet you can actually read** — this one's cannot
be (§2).

---

## 6. Integration pitfalls

1. **27.12 MHz, not 27 MHz and not 13.56 MHz** (§3). The single most common way
   to get this wrong.
2. **The exact SKU is not orderable from any catalogue reached** (§2).
3. **The datasheet held is the wrong frequency and has no text layer** (§2). Do
   not quote an ESR or drive level from it.
4. **C<sub>L</sub> vs `C14`/`C15` is unresolved** (§4.2).
5. **A dead crystal presents as "NFC not responding"**, indistinguishable in
   firmware from a bus fault or an unpowered sub-board — and the sub-board's rail
   is switched (see the
   [BTB record §3.4](../btb0.408-10plbdr-g41/README.md#34-pyb_nfc_en--pyb_rfid_rst--a-power-cut-not-a-reset)),
   so "no NFC" has at least three causes before the crystal is suspected.
6. **Drive level is unspecified.** Over-driving a small 2016 crystal ages it and
   can fracture it; the ST25R3916's oscillator drive was not checked. **[INF]**

---

## 7. Open questions

- The 27.12 MHz SKU's ordering code, ESR, drive level, C<sub>0</sub> and ageing
  (§2).
- Whether `C14`/`C15` = 10 pF is ST's recommended value or a computed one, and
  therefore whether §4.2 is a non-issue (checkable against **[ST]** DS12484 and
  ST's ST25R3916 application notes, both already held or reachable).
- The actual C<sub>L</sub> of the fitted part.
- No measurement of frequency, start-up time or drive level.

---

## Manufacturer

**YXC Crystal Oscillators** (扬兴科技). No vendor sourcing guide exists in this
repository yet.

**⚠ Retrieval findings, both worth carrying forward.**

1. **LCSC's `wmsc.lcsc.com` CDN served the document; `www.lcsc.com/datasheet/`
   does not.** The rewrite is mechanical and is documented in full in the
   [SK2302AAT record](../sk2302aat/README.md#manufacturer). **Check the `%PDF`
   magic bytes, never the status code.**
2. **General web search was unavailable.** On 2026-09-01, `lite.duckduckgo.com`
   returned a captcha challenge to `curl` ("Unfortunately, bots use DuckDuckGo
   too… Select all squares containing a duck"), `www.mojeek.com/search` returned
   no parseable results, and `searx.be` served a "Verifying your browser…"
   interstitial. **The only search channel that worked for these Chinese-market
   parts was JLCPCB's SMT parts API**, which answers with compact JSON and is not
   bot-filtered:

   ```bash
   curl -s -X POST -H 'Content-Type: application/json' \
     -d '{"keyword":"XL7EL89CMI-111YLC","currentPage":1,"pageSize":3}' \
     https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList
   ```

   `executed-success`, 2026-09-01. Helper:
   [`scratch/m5stack-papermono/tools/lcsc_lookup.sh`](../../../scratch/m5stack-papermono/tools/lcsc_lookup.sh).

Both belong in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

## 4.4 A second board uses 27.12 MHz for the same reason — part **not** identified · *added 2026-09-04*

The [M5Stack Cap CC1101 & NFC (U219)](../../../devices/m5stack/cap-cc1101/README.md) fits an
**ST25R3916 with a 27.12 MHz crystal** — designator `Y1`, load capacitors `C19`/`C20` = **6.0 pF**,
on `XTI` (5) / `XTO` (4), read from the Cap CC1101 schematic V0.3 (2026-05-28).

**This is *not* recorded as a Used By entry for this part**, because **no part number is
printed on that schematic** — only the frequency and the package-adjacent values. The two
crystals share a frequency and a job; nothing establishes that they are the same component.

What it does confirm is §3's argument: **27.12 MHz appears wherever an ST25R3916 does**,
because the 13.56 MHz NFC carrier is derived from it by division by two. Two independent
M5Stack boards, two years apart, same frequency, same reason.

If the Cap CC1101's crystal part number is ever read from a photograph or a BOM and turns
out to be `XL7EL89CMI-111YLC`, this section should become a proper **Used By** entry with
the pin table and load-capacitor analysis that §4.1–4.2 give for the PaperMono.

## Related pages

- [M5Stack Cap CC1101 & NFC](../../../devices/m5stack/cap-cc1101/features/nfc.md) — the second ST25R3916 board in this repository (**SPI**-strapped, unlike the PaperMono)
- [STMicroelectronics ST25R3916](../../stmicroelectronics/st25r3916/README.md) — **the IC this crystal clocks**
- [BTB0.408-10PLBDR-G41](../btb0.408-10plbdr-g41/README.md) — how the NFC sub-board attaches
- [CN4040M000157A530001 40 MHz crystal](../cn4040m000157a530001-40mhz-crystal/README.md) — the board's *other* crystal, also `X1`, also with no datasheet
- [PaperMono NFC feature guide](../../../devices/m5stack/papermono/features/nfc.md) · [bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| D1 | `XL7EL89CMI-111YLC-24M` crystal datasheet | YXC (via LCSC CDN) | **series-representative**, wrong frequency (§2) | <https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2403291506_YXC-Crystal-Oscillators-XL7EL89CMI-111YLC-24M_C2965581.pdf> | 2026-09-01 | undated, 1 p, **no text layer** | the series' existence and package; **nothing numeric** — every figure in §1 is from **[CAT]** | `artifacts/xl7el89cmi-111ylc-24m-yxc-lcsc-mirror.pdf` |
| C1 | LCSC entries `C2965581`, `C2965583` | LCSC / JLCPCB | distributor | JLCPCB SMT parts API, keyword `XL7EL89CMI-111YLC` | 2026-09-01 | — | manufacturer YXC; SMD2016-4P; **C<sub>L</sub> = 10 pF**; ±10/±20 ppm; −40…+85 °C; ESR 100 Ω @ 24 MHz and 80 Ω @ 32 MHz; **the absence of a 27.12 MHz SKU** | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | `X1` = `27.12MHZ(XL7EL89CMI-111YLC)`; the §4.1 connections; `C14`/`C15` = 10 pF; the §4.3 sheet annotations | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/xl7el89cmi-111ylc-24m-yxc-lcsc-mirror.pdf` | 535 394 | `a04912f4671b1e22bbdc13488eb82e6321fd7a71ffdb3515c111cae3472f0a0c` | 1 |

**Method note.** D1 validated as `%PDF` (`executed-success`) and confirmed
text-layer-free (`pdftotext` yields 0 bytes). It is retained despite being the
wrong frequency because it is the only YXC artifact obtainable for this series and
because its page can be rendered and read as an image by a future pass. **It is
labelled series-representative rather than primary precisely so that no reader
mistakes a 24 MHz figure for a 27.12 MHz one.**
