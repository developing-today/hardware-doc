# Fitipower EK73217BCGA

- **Category:** TFT-LCD **gate (row) driver** — 1200/1152/1080/960 outputs, 2-level, high-voltage CMOS, COG
- **Research status:** full datasheet retained (26 pp, Rev. 1.0). It is a short, complete document for a simple part.
- **Retrieved:** 2026-08-30

The gate driver on the optional **7-inch 1024 × 600 MIPI-DSI panel** sold with Espressif's ESP32-P4 Function EV boards. It is the companion to the [EK79007AD](../ek79007ad/README.md) source driver + TCON.

> ⚠ **This is not a display controller.** It has no host interface, no register map, no command set and no firmware-visible behaviour. It is included in `components/` because board and guide documentation lists it alongside the EK79007AD as a "display driver IC", and readers need to know which of the two they are actually looking for. **If you are writing display code, you want the [EK79007AD](../ek79007ad/README.md).**

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Stated in `artifacts/ek73217bcga-datasheet.pdf` (Rev. 1.0, 2017/07/28) |
| **[VEN]** | Stated by Espressif in board documentation |
| **[INF]** | Inference |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Fitipower Integrated Technology Inc.** | **[DOC]** cover |
| Part | **`EK73217BCGA`** | **[DOC]** cover |
| Function | *"1200/1152/1080/960-Output TFT LCD Gate Driver"* | **[DOC]** cover, §1 |
| Description | 2-level output gate driver for driving the gate electrodes of a TFT LCD panel | **[DOC]** §1 |
| Revision | **Rev. 1.0, 2017/07/28** | **[DOC]** page footer |
| Package | **COG**, die 23 650 µm × 670 µm, output bump pitch 18 µm | **[DOC]** §2 |
| Document length | 26 pages | **[DOC]** |
| Reference designator | On the **panel assembly**; not published | **[INF]** |
| ⚠ Marking verified? | **No.** COG die bonded to the glass | **[VEN]** |

### 1.1 Features **[DOC]** §2

| Property | Value |
|---|---|
| Outputs | **1200 / 1152 / 1080 / 960**, selectable, **plus 2 dummy outputs fixed to `VGL`** |
| Output type | **2-level** (gate-high / gate-low). Not 3-level |
| Max output driving voltage | **+40 V** |
| Logic supply `VCC` | **1.7 – 2.5 V** |
| Shift direction | **Bi-directional** data shift |
| Max operating frequency | **200 kHz** |
| Process | High-voltage CMOS |

### 1.2 Document structure **[DOC]**

1. General description · 2. Features · 3. Block diagram · 4. Pin description · 5. Function description (device operation, power supply, **power ON/OFF sequence**, **start-pulse limitation**, output sequence and frame control) · 6. Electrical specification (absolute maximum ratings, recommended operating range, DC/AC characteristics, timing waveforms, operation timing) · 7. Chip outline dimensions and alignment mark · 8. Bump centre coordinates.

> **Metadata finding.** This PDF's internal `Title` field is **`EK7616DS`**, author `sally.chen` — identical to the [EK79007AD document](../ek79007ad/README.md#12--two-different-documents-both-called-the-ek79007-datasheet). Both were produced by editing a Fitipower **EK7616** datasheet template. Prefer the body text over document properties when they disagree.

---

## 2. What a gate driver does, and why it is listed as a "display driver IC"

An active-matrix TFT panel needs two drive axes:

| Axis | Driven by | On this panel |
|---|---|---|
| **Columns** (source / data lines) | Source driver — carries pixel values | **[EK79007AD](../ek79007ad/README.md)**, 1536 outputs, plus the TCON and the MIPI-DSI receiver |
| **Rows** (gate / scan lines) | Gate driver — switches one row of TFTs on at a time | **EK73217BCGA**, up to 1200 outputs at up to +40 V |

Single-chip controllers such as [JD9365](../../jadard/jd9365/README.md), [ILI9881C](../../ilitek/ili9881c/README.md) and [ST7789VW](../../sitronix/st7789vw/README.md) integrate **both** functions plus power generation into one die, which is why they need no companion part. This 7-inch panel instead splits the job, which is common for larger glass where the gate-line count and drive voltage exceed what a single integrated part conveniently provides.

Espressif's board documentation lists **both** parts together as "display driver ICs" **[VEN]**, which is accurate but has caused them to be treated as two interchangeable controller candidates. They are not: they are two halves of one design.

---

## 3. Where it is fitted

Same accessory as the EK79007AD — the **7-inch panel / LCD adapter sub-board** for Espressif's ESP32-P4 Function EV family **[VEN]**:

- [ESP32-P4X-Function-EV-Board](../../../devices/espressif/esp32-p4x-function-ev-board/README.md)
- [ESP32-P4X-C5-Function-EV-Board](../../../devices/espressif/esp32-p4x-c5-function-ev-board/README.md)
- [ESP32-P4-Function-EV-Board](../../../devices/espressif/esp32-p4-function-ev-board/README.md)

Fitted on **chip-revision v0.1** devkit panels; v0.0 devkits shipped an [ILI9881C](../../ilitek/ili9881c/README.md)-based panel instead **[VEN]**.

**Output count on this panel.** The panel is 1024 × 600. A 600-row panel driven with dual-gate structure (which the EK79007AD explicitly implements — "Dual Gate (1024RGB × 600)") needs **1200** gate lines, which is exactly this part's top configuration. **[INF]**, but a well-supported one: it is why the 1200-output option exists and why this pairing was chosen.

---

## 4. Function and power sequencing

This is the only part of this record that affects whether the display works.

**[DOC]** §5 documents:

| Topic | Section |
|---|---|
| Device operation | §5.1 |
| Device power supply | §5.2 |
| **Power ON/OFF sequence** | §5.3 |
| **Start pulse LIMITATION** | §5.4 |
| Output sequence and frame control | §5.5 |

Two of these deserve emphasis:

1. **Power ON/OFF sequence (§5.3).** A high-voltage gate driver sharing glass with a source driver must be sequenced relative to `VGH`/`VGL` and the logic rail. Getting it wrong risks latch-up or panel stress, not merely a bad image. If you are designing your own panel around this pair, read §5.3 in the datasheet — it is not reproduced here because it is a figure with device-specific timings and paraphrasing it would be worse than useless.
2. **Start-pulse limitation (§5.4).** The datasheet calls this out as its own section, which is unusual for a part this simple, so treat it as a real constraint rather than boilerplate.

**On the Espressif panel none of this is your problem** — the panel assembly is a finished module and the sequencing is designed in. It matters if you are (a) debugging a panel that shows horizontal banding or missing rows, or (b) designing new glass.

### 4.1 Symptoms that point at the gate driver

**[INF]** from the part's function, offered as a diagnostic aid rather than a documented failure list:

| Symptom | More likely |
|---|---|
| Whole panel dark, backlight on | Source driver / TCON / DSI link |
| Correct image but **horizontal bands or missing rows** | **Gate driver** or its supply |
| Image present but rows scan in the wrong direction | Gate driver **shift direction** (the part is bi-directional) |
| Colour or gamma wrong | Source driver / TCON |

---

## 5. Software

**None.** This part has no host interface and no driver. It is controlled entirely by the timing signals the [EK79007AD](../ek79007ad/README.md)'s TCON generates. There is no ESP-IDF component, no Arduino library and no Linux driver for it, and there should not be.

For the panel as a whole, use **`espressif/esp_lcd_ek79007`** — see the [EK79007AD record §4](../ek79007ad/README.md#4-libraries-and-drivers).

---

## 6. Alternatives and compatibility

| Part | Relationship | Compatible? |
|---|---|---|
| **[EK79007AD](../ek79007ad/README.md)** | The companion **source** driver + TCON | ✅ **Designed to pair.** Not a substitute |
| Other 2-level gate drivers with matching output count, voltage and pitch | Functional equivalents | ⚠ Possible in principle, but gate drivers are selected by **bump pitch and die geometry** as much as by electrical spec — this is a COG part bonded to specific glass. Not a field-serviceable choice |
| **EK7616** | The datasheet template's origin part | ❌ Different part; the shared `Title` field is an artefact |
| GIP / gate-in-panel designs | The integrated alternative — gate drive fabricated **into the panel** rather than as a separate chip | ❌ Architectural alternative, not a substitute. The [JD9365](../../jadard/jd9365/README.md)'s large page-2 register block is GIP configuration, which is exactly the function this discrete chip performs |

---

## 7. Open questions

| Question | Status |
|---|---|
| Which output configuration (1200/1152/1080/960) this panel uses | **Open.** §3 argues 1200; unconfirmed |
| Reference designator on the panel assembly | **Open.** Not published |
| Whether more than one of these is fitted (cascade) | **Open.** The EK79007AD supports cascade; whether the gate side is cascaded here is unknown |
| Lifecycle status | **Open.** Rev 1.0 dates from 2017; no PCN or EOL notice found |

---

## Manufacturer

**Fitipower Integrated Technology** — see the [Fitipower documentation-sourcing guide](../../../vendors/fitipower/README.md).

## Used By

- [Espressif ESP32-P4X-Function-EV-Board](../../../devices/espressif/esp32-p4x-function-ev-board/README.md) — gate driver of the **optional 7″ 1024 × 600 MIPI-DSI panel**, paired with the [EK79007AD](../ek79007ad/README.md) source driver + TCON on the LCD adapter sub-board. Fitted on **chip-revision v0.1** devkits.
- [Espressif ESP32-P4X-C5-Function-EV-Board](../../../devices/espressif/esp32-p4x-c5-function-ev-board/README.md) — same optional display accessory.
- [Espressif ESP32-P4-Function-EV-Board](../../../devices/espressif/esp32-p4-function-ev-board/README.md) — same family.

## Related components

- **[Fitipower EK79007AD](../ek79007ad/README.md)** — the companion source driver + TCON, and **the part you actually program**
- [Ilitek ILI9881C](../../ilitek/ili9881c/README.md) — the controller on v0.0 devkit panels
- [Jadard JD9365](../../jadard/jd9365/README.md) — single-chip alternative with integrated (GIP) gate drive
- [Display interfaces guide](../../../guides/hardware/display-interfaces.md)

---

## Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/ek73217bcga-datasheet.pdf` | 1 571 109 | `bd4ec28f5b11ab95536da6cf6162af18ff8d1ec34fa19379444eb5c0e8f7763a` | **EK73217BCGA datasheet Rev. 1.0, 2017/07/28**, 26 pp |

Third-party (Fitipower) copyright, mirrored by Espressif with **no stated licence** — redistribution status **`unknown`**, disposition `repository` pending review.

**Duplication resolved 2026-08-30.** A byte-identical copy used to sit at `devices/espressif/shared-artifacts/ek73217bcga-datasheet.pdf`. This component location is canonical and is now **the only copy**; the device-side copy has been removed and replaced by a cross-link at [`devices/espressif/shared-artifacts/DRIVER-DATASHEETS-MOVED.md`](../../../devices/espressif/shared-artifacts/DRIVER-DATASHEETS-MOVED.md). The deferral noted here previously is discharged.

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published | Establishes |
|---|---|---|---|---|---|---|---|---|
| G-1 | EK73217BCGA datasheet Rev. 1.0 | Fitipower, mirrored by Espressif | authorized mirror | datasheet | <https://dl.espressif.com/dl/schematics/display_driver_chip_EK73217BCGA_datasheet.pdf> | 2026-08-30 | 2017-07-28 | §1, §1.1, §1.2, §4 |
| G-2 | ESP32-P4X-Function-EV-Board record | this repository | primary | board doc | [device record](../../../devices/espressif/esp32-p4x-function-ev-board/README.md) | 2026-08-30 | — | §3 fitted status |
