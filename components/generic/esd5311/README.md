# ESD5311 — bidirectional ESD suppressor (TECH PUBLIC)

> **Single-line bidirectional ESD protection diode**, 5 V standoff, ~0.3 pF, 4 A peak (8/20 µs), IEC 61000-4-2 / -4-5 rated, in a **DFN1006-2** (0402) package.
> Research snapshot **2026-09-01**. **The most-used part on the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) after the passives: 12 instances across 3 sheets** — every one enumerated in [§4](#4-used-by).
> **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | TECH PUBLIC `ESD5311X` datasheet, local copy `artifacts/esd5311x-tech-public-lcsc-mirror.pdf` — ⚠ **image-only, no text layer**, §2 | `not-tested` |
| **[CAT]** | LCSC / JLCPCB catalogue entries `C2844730` (`ESD5311X`), `C2936982` (`ESD5311N`), retrieved 2026-09-01 | `not-tested` |
| **[SCH-V]** | Read off the schematic rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[SCH-T]** | Read from the schematic text layer only | `executed-success` for the extraction; attribution `inferred` |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Value string on the schematic | **`ESD5311`** — with **no suffix** | **[SCH-V]** |
| Manufacturer | **TECH PUBLIC** (泰科源) | **[CAT]** |
| Function | Bidirectional transient-voltage suppressor for ESD protection | **[CAT]** |
| Package | **DFN1006-2** — a 2-terminal 0402 leadless part | **[CAT]** |
| Pins | **2** | **[SCH-M]**, all 12 instances |
| RoHS | yes | **[CAT]** |

### 1.1 ⚠ `ESD5311` with no suffix is not an orderable part number

LCSC's catalogue has **no bare `ESD5311`**. It has two suffixed parts from the
same maker, plus a third-party equivalent:

| Part | Maker | LCSC | V<sub>RWM</sub> | V<sub>BR</sub> | Clamp | I<sub>PP</sub> (8/20 µs) | P<sub>PP</sub> | C | I<sub>R</sub> |
|---|---|---|---|---|---|---|---|---|---|
| **`ESD5311X`** | TECH PUBLIC | `C2844730` | **5 V** | **7.5 V** | **12 V / 21 V** | **4 A** | **80 W** | **0.3 pF** | 80 nA |
| **`ESD5311N`** | TECH PUBLIC | `C2936982` | 5 V | 7.5 V | **15 V** | 4 A | **70 W** | 0.3 pF | 80 nA |
| `ESD5311N` | UMW (Youtai) | `C2987704` | 5 V | 9 V | **21 V** | 4 A @ 8/20 µs | 84 W | 0.25 pF | 1 nA |

**[CAT]**

**Which suffix M5Stack fits is not established.** The schematic prints the family
stem only. The two TECH PUBLIC variants differ in clamping voltage and peak power
— 12 V/21 V and 80 W for the `X`, 15 V and 70 W for the `N` — which is a real
difference for the pin being protected, but not one that changes any design
decision on this board, because in every instance the protected net is a 3.3 V
logic line or a 5 V USB line and both variants stand off 5 V.

**No suffix is asserted here.** The datasheet retained is the `ESD5311X`, chosen
because it is the higher-volume LCSC part; §1 quotes only properties the two
share. **What would resolve it:** the top marking on an assembled board, or
M5Stack's BOM.

---

## 2. ⚠ The datasheet has no text layer

`artifacts/esd5311x-tech-public-lcsc-mirror.pdf` is **4 pages, 953 567 bytes**,
and `pdftotext` extracts **4 bytes** from it. Every page is a scan or a vector
outline.

So **the parametric table in §1.1 is LCSC's transcription, not the
manufacturer's own text**, and no I–V curve, no derating curve, no solder profile
and no marking code were read from the document. The file is retained because it
is the only manufacturer artifact obtainable, and because a future reader can
render its pages to PNG and read them as images — the technique used elsewhere in
this repository for the
[DKE panel manual](../../dke/depg0397bbs770f3/README.md), which has the same
problem.

---

## 3. What it is for

A bidirectional TVS in an 0402 leadless package with **~0.3 pF** of capacitance.
The capacitance is the whole point: 0.3 pF is low enough to sit on a **USB 2.0
high-speed differential pair** without meaningfully degrading the eye, which is
what a general-purpose 5 V TVS at tens of pF cannot do.

The parts are rated to the two standards that matter for a handheld:

- **IEC 61000-4-2** — the ESD test (contact and air discharge to an accessible
  surface).
- **IEC 61000-4-5** — the surge test.

**Bidirectional** matters for the USB data lines, which are referenced to ground
and can swing either way during a discharge, and for switch inputs where a
discharge into a finger-accessible button can drive the pin negative.

---

## 4. Used By

### `devices/m5stack/papermono` — **12 instances**

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md).
Every instance, with the net it protects. Designators use two different prefixes
because they come from two different Altium documents (`TVS…` in the main
project, `DR…` on the KEY/RGB sub-board).

| # | Ref | Sheet | Net protected | Function of that net | Evidence |
|---:|---|---:|---|---|---|
| 1 | **`TVS1`** | 2 | **`USB_N`** | USB-C `DN1`/`DN2` — the high-speed pair | **[SCH-V]** |
| 2 | **`TVS2`** | 2 | **`USB_P`** | USB-C `DP1`/`DP2` | **[SCH-V]** |
| 3 | **`TVS3`** | 4 | **`G9_TF_DATA2`** | microSD DAT2 (pull-up `R62` 4.7 kΩ) | **[SCH-T]** |
| 4 | **`TVS4`** | 4 | **`G8_TF_DATA3`** | microSD CD/DAT3 (`R63` 4.7 kΩ) | **[SCH-T]** |
| 5 | **`TVS5`** | 4 | **`G12_TF_CMD`** | microSD CMD (`R64` 4.7 kΩ) | **[SCH-T]** |
| 6 | **`TVS6`** | 4 | **`G13_TF_CLK`** | microSD CLK (`R65` 4.7 kΩ) | **[SCH-T]** |
| 7 | **`TVS7`** | 4 | **`G11_TF_DATA0`** | microSD DAT0 (`R66` 4.7 kΩ) | **[SCH-T]** |
| 8 | **`TVS8`** | 4 | **`G10_TF_DATA1`** | microSD DAT1 (`R67` 4.7 kΩ) | **[SCH-T]** |
| 9 | **`TVS9`** | 4 | **`PYB_TF_DET`** | microSD **card-detect** (`R68` **1 MΩ**) | **[SCH-T]** |
| 10 | **`DR1`** | 5 | **`PWR_BTN`** | power button `S1`, pulled up to **`3V3_L0`** by `R1` 10 kΩ, debounced by `C1` 100 nF | **[SCH-V]** |
| 11 | **`DR2`** | 5 | **`G2_KEY1`** | user button A `S2`, pull-up `R2` 10 kΩ to `3V3_L2`, `C3` 100 nF | **[SCH-V]** |
| 12 | **`DR3`** | 5 | **`G3_KEY2`** | user button B `S3`, pull-up `R5` 10 kΩ to `3V3_L2`, `C4` 100 nF | **[SCH-V]** |

**On the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md):**
`inferred` **yes, and probably all 12** — the Lite drops only NFC and LoRa, and
none of these twelve is on either. The NFC sub-board (sheet 6) carries **no**
ESD5311. Not read from the Lite's own schematic.

### 4.1 The placement pattern is coherent, and it says something about the design

Three groups, and each is an *externally accessible* interface:

| Group | Count | Why it needs protection |
|---|---:|---|
| **USB-C data** | 2 | A connector a user plugs into. Low capacitance is mandatory here |
| **microSD** | **7** | A card slot a user's fingers reach into — and **every single line is protected, including card-detect** |
| **Buttons** | 3 | The only parts of the PCB a user touches during normal operation |

Nothing else on the board gets an ESD5311: not the board-to-board connectors, not
the FPC connectors, not the antenna. That is the correct call — those are internal
joints, not user-accessible surfaces. **[INF]**

The microSD coverage is more thorough than is common. Many designs protect the
data lines and skip card-detect; here **`PYB_TF_DET` gets `TVS9`** even though it
is a slow, 1 MΩ-pulled-up sense line. Its exposure is the same as the data lines'
— it goes to a contact in the slot — so protecting it is consistent rather than
excessive.

### 4.2 The one thing to check before reusing this pattern

`TVS1` and `TVS2` sit on `USB_N`/`USB_P` **at the connector**, upstream of the
`ICMF062P900MFR` common-mode choke `FT1` and the 22 Ω series resistors `R40`/`R41`
on sheet 3. **[SCH-V]** That is the right order: the TVS clamps at the point of
entry, and the choke and series resistance are downstream of it.

The 0.3 pF figure is what makes this legal on a USB 2.0 pair. **Substituting a
"5 V ESD diode" with a conventional TVS at 20–50 pF would put ~100 pF across the
pair once both are counted, and USB 2.0 high-speed would degrade.** If this part
is ever swapped, capacitance — not voltage — is the parameter that must be
matched. **[INF]**

---

## 5. Substitution

| Alternative | vs. ESD5311 | Note |
|---|---|---|
| **`ESD5311N`** (TECH PUBLIC) | Same family; 15 V clamp, 70 W | The other variant of this very part (§1.1) |
| **`ESD5311N`** (UMW/Youtai) | 9 V V<sub>BR</sub>, 21 V clamp, 0.25 pF, 1 nA | A second source at LCSC |
| Nexperia **PESD5V0X1BL** / **PESD5V0S1BL** | Documented, qualified, ~0.4 pF class | When the missing datasheet (§2) is unacceptable |
| ON Semi **ESD9B5.0ST5G** | 0.35 pF, AEC-Q101 | Automotive-grade |
| Any generic "5 V TVS" | ⚠ **usually 20–500 pF** | **Not** a substitute on the USB pair (§4.2) |

**Match capacitance first, standoff voltage second.**

---

## 6. Integration pitfalls

1. **`ESD5311` alone is not orderable** (§1.1). Pick `X` or `N` deliberately.
2. **The datasheet is image-only** (§2). Any number quoted from this record for
   the part traces to LCSC, not to TECH PUBLIC.
3. **Capacitance, not voltage, is the substitution constraint** on USB (§4.2).
4. **Two designator prefixes for one part** (`TVS…` and `DR…`) across two Altium
   documents. A search for "TVS" finds 9 of the 12.
5. **12 instances is a real BOM line.** At 0402 leadless, placement yield matters
   more than unit cost.
6. **These protect against ESD, not against a shorted or over-voltage supply.**
   A 5 V standoff on a 3.3 V logic line means the part is invisible in normal
   operation and stays invisible right up to 7.5 V — it is not a rail clamp.

---

## 7. Open questions

- **Which suffix is fitted** (§1.1) — resolvable only from a board or a BOM.
- The datasheet's own electrical tables, curves and marking code (§2) — present
  in the file as images, not yet transcribed.
- Whether the PaperMono-Lite carries all 12 (`inferred`, §4).
- No measurement of anything: no ESD gun, no TLP, no eye diagram.

---

## Manufacturer

**TECH PUBLIC** (泰科源) is a Shenzhen protection-device maker distributed through
LCSC. No vendor sourcing guide exists in this repository yet.

**⚠ Retrieval finding — the LCSC PDF host trap.** The working URL is on
**`wmsc.lcsc.com`**, not on `www.lcsc.com`:

| URL form | Result |
|---|---|
| `https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2108072230_TECH-PUBLIC-ESD5311X_C2844730.pdf` | **200, `%PDF` ✓**, 953 567 B |
| `https://www.lcsc.com/datasheet/lcsc_datasheet_<stamp>_<name>_<code>.pdf` | **HTTP 200 with `text/html`** for every part tried |

`www.lcsc.com/datasheet/*.pdf` returns **HTTP 200 and HTML** under a `.pdf` URL.
**Check the `%PDF` magic bytes; the status code proves nothing.** The rewrite that
works is `www.lcsc.com/datasheet/lcsc_datasheet_<stamp>_<name>_<code>.pdf` →
`wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/<stamp>_<name>_<code>.pdf`. This
reproduces the finding already recorded in the
[IP2315 record](../../injoinic/ip2315/README.md#manufacturer) and belongs in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

## Related pages

- [XUNPU TYPEC-302-BRP16SC08](../typec-302-brp16sc08/README.md) — the connector `TVS1`/`TVS2` guard
- [microSD / SDMMC interface](../micro-sd-sdmmc/README.md) — the interface `TVS3`–`TVS9` guard
- [Panasonic AXE612124D](../../panasonic/axe612124d/README.md) — the sub-board `DR1`–`DR3` live on
- [PaperMono bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| D1 | `ESD5311X` datasheet | TECH PUBLIC (via LCSC CDN) | primary, via distributor mirror | <https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2108072230_TECH-PUBLIC-ESD5311X_C2844730.pdf> | 2026-09-01 | undated, 4 pp | retained as the only manufacturer artifact; **no text layer**, §2 | `artifacts/esd5311x-tech-public-lcsc-mirror.pdf` |
| C1 | LCSC entries `C2844730`, `C2936982`, `C2987704` | LCSC / JLCPCB | distributor | JLCPCB SMT parts API, keyword `ESD5311` | 2026-09-01 | — | the §1.1 parametric table; the existence of `X` and `N` suffixes and the UMW second source | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | all 12 instances and their nets (§4) | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/esd5311x-tech-public-lcsc-mirror.pdf` | 953 567 | `00acc3ed39fa5ede6b73405949bbd89446867336962d41f4115dc260d91740ab` | 4 |

**Method note.** D1 validated as `%PDF` (`executed-success`) and confirmed
text-layer-free (`pdftotext` yields 4 bytes). The 12-instance census in §4 comes
from the schematic's `CO` marker layer, enumerated across **all six sheets** —
proving the set is complete rather than searching for the instances expected. The
`TVS1`/`TVS2` and `DR1`–`DR3` rows were additionally re-read from 200 dpi page
renders; the seven microSD rows were not, and are marked **[SCH-T]** accordingly.
