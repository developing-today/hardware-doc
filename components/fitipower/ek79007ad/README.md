# Fitipower EK79007AD

- **Category:** 1536-channel TFT-LCD **source driver with integrated timing controller (TCON)**, MIPI-DSI input, for 1024 × 600-class a-Si panels
- **Research status:** **two different datasheet revisions were obtained** and both are retained — they are *not* duplicates. See §1.2, which is the most important thing on this page.
- **Retrieved:** 2026-08-30

One half of the display-driver pair on the optional **7-inch 1024 × 600 MIPI-DSI panel** sold with Espressif's ESP32-P4 Function EV boards. The companion gate driver is the [EK73217BCGA](../ek73217bcga/README.md).

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Stated in one of the retained Fitipower datasheets, with the revision identified |
| **[VEN]** | Stated by Espressif in board documentation |
| **[SRC]** | Read out of driver source |
| **[INF]** | Inference |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Fitipower Integrated Technology Inc.** (天鈺科技) | **[DOC]** cover, "fitipower integrated technology Inc." |
| Part | **`EK79007AD`** | **[DOC]** cover |
| Function | *"Single Chip 1536 Channel Source Driver with Timing Controller for 1024(RGB) × 600 TFT LCD"* | **[DOC]** §1 |
| Channels | **1536** source outputs (= 512 RGB) with **dual-gate** function | **[DOC]** §2 |
| Interface | **MIPI-DSI** (the `AD` variant is MIPI-only) | **[DOC]** cover: "MIPI Interface" |
| Package | **COG**, die 24 975 µm × 695 µm, bump height 9 µm, output bump pitch 15 µm | **[DOC]** §2 |
| Revision | **Rev. 1.9, dated 2018/06/14** | **[DOC]** page footer |
| Reference designator | On the **panel / LCD adapter sub-board**, not the main board; not published | **[INF]** |
| ⚠ Marking verified? | **No.** COG die inside the panel assembly; identification rests on Espressif naming it and mirroring its datasheet | **[VEN]** |

### 1.1 Capabilities **[DOC]** §2

| Area | Value |
|---|---|
| Supported resolutions (H × V) | **1024 × 768, 1024 × 600, 800 × 600, 800 × 480** |
| Grey scale | 8-bit, **256 levels** with dithering (6-bit DAC + 2-bit FRC or HFRC) |
| MIPI lane rates | **4 lane: 500 Mbps; 2 lane: 650 Mbps (max)** |
| Supplies | `VDD_IF` (MIPI) **1.8 V**; `VDD` (digital) **1.8 V**; `AVDD` (analogue) **8.0–13.5 V** |
| Gamma | Embedded gamma table; **V1–V14** adjustment points |
| Inversion | **1+2 dot** inversion architecture |
| Built-in | PWM controller for AVDD, charge pump for VGH/VGL, VCOM buffer, **CABC**, auto pattern generator, SDRRS, no-clock detection |
| Cascade | Supported, with bidirectional shift control (CMOS signal) |

The **built-in auto pattern generator** is worth knowing about: it can drive a test pattern without a valid video stream, which makes it possible to separate panel/driver faults from host raster faults during bring-up. **[DOC]**

### 1.2 ⚠ Two different documents, both called "the EK79007 datasheet"

This is the skill's documented near-duplicate case (`.agents/skills/hardware-device-research/SKILL.md`, *Analyze vendored dependencies, near-duplicates and large artifacts*) in its exact form, and getting it wrong would mislead anyone reading the electrical section.

| | `ek79007ad-datasheet.pdf` | `ek79007-datasheet-esp-iot-solution-mirror.pdf` |
|---|---|---|
| Cover part | **EK79007**​**AD** | **EK79007** (no suffix) |
| Cover subtitle | 1536-Output Source Driver with TCON, **MIPI Interface** | 1536-Output Source Driver with TCON, **MIPI/LVDS Interface** |
| Pages | **75** | **92** |
| Revision | **Rev. 1.9**, 2018/06/14 | **REV1.0** |
| PDF `Title` field | `EK7616DS` | `Microsoft Word - EK79007_DS_REV1.0.doc` |
| PDF `Author` | `sally.chen` | `james.chen` |
| PDF created | 2018-06-13 | 2015-09-25 |
| Producer | MS Word 2007 | PScript5 → Mac OS X Quartz |
| Bytes | 3 723 767 | 4 084 080 |
| SHA-256 | `2dbab767…6c8287a4` | `a038ce84…73a6bd28` |
| Source portal | `dl.espressif.com/dl/schematics/` | `dl.espressif.com/AE/esp-iot-solution/` |

**They are different parts of a family, not two copies of one file.** The base `EK79007` supports **MIPI *and* LVDS**; the `AD` variant is MIPI-only and three years newer. Application-block sections differ too — the older document covers both non-GIP and GIP dual-gate panels, the newer only dual-gate.

**Which applies to the Espressif panel?** The board documentation names **`EK79007AD`** **[VEN]**, so `ek79007ad-datasheet.pdf` (Rev 1.9) is the one the hardware was designed against. The `EK79007` REV1.0 document is retained because it is a **superset on interfaces** and fills gaps the newer, shorter document omits.

> **Metadata finding.** The `AD` document's internal PDF `Title` is **`EK7616DS`** — and so is the [EK73217BCGA](../ek73217bcga/README.md) document's, by the same author. Both were produced by editing a Fitipower **EK7616** datasheet template. This explains inherited section ordering and boilerplate, and it is a reason to prefer the *body text* over any *document property* when the two disagree. Recorded per the skill's "read a document's own metadata" guidance.

---

## 2. Role in the panel: it is half of a pair

The EK79007AD is a **source driver + TCON**. It does not drive gate lines. The 7-inch panel pairs it with the **[EK73217BCGA](../ek73217bcga/README.md)** gate driver:

| Part | Role |
|---|---|
| **EK79007AD** | Receives MIPI-DSI, does timing control, drives **1536 source (column) outputs** |
| **EK73217BCGA** | Drives up to **1200 gate (row) outputs** |

This is a different architecture from the single-chip parts elsewhere in this repository — [JD9365](../../jadard/jd9365/README.md), [ILI9881C](../../ilitek/ili9881c/README.md) and [ST7789VW](../../sitronix/st7789vw/README.md) all integrate source drive, gate control and power into one die. Here the function is split across two chips. Practically this matters for **power sequencing**: two devices must be brought up in the right order (see the EK73217BCGA record §4), and a gate-driver fault presents as horizontal banding rather than a dead panel.

---

## 3. Where it is fitted

⚠ **On an optional accessory, not on the main board.** The EK79007AD lives on the **7-inch panel / LCD adapter sub-board** supplied with, or sold alongside, Espressif's ESP32-P4 Function EV boards **[VEN]**.

| Board | Relationship |
|---|---|
| [ESP32-P4X-Function-EV-Board](../../../devices/espressif/esp32-p4x-function-ev-board/README.md) | Optional 7″ 1024 × 600 MIPI-DSI panel |
| [ESP32-P4X-C5-Function-EV-Board](../../../devices/espressif/esp32-p4x-c5-function-ev-board/README.md) | Same optional display accessory |
| [ESP32-P4-Function-EV-Board](../../../devices/espressif/esp32-p4-function-ev-board/README.md) | Same family |

**Chip-revision tie-in.** Espressif's devkit panels are revision-tied: **chip revision v0.0 devkits shipped an [ILI9881C](../../ilitek/ili9881c/README.md) panel; v0.1 shipped EK79007** **[VEN]**. If you are cross-developing against a devkit, check which one you actually have — the drivers are not interchangeable.

The connector is a **1.0 mm pitch, 15-pin FPC (`1.0K-GT-15PB`)** carrying MIPI-DSI **[VEN]**; its specification is retained in the device tree.

### 3.1 Wiring

The MIPI-DSI lanes run from the ESP32-P4 to the FPC connector; the sub-board schematics and PCB layout are published and retained in the device tree (`lcd-subboard-schematics.pdf`, `lcd-subboard-pcb-layout.pdf`, `lcd-adapter-board-reference-design.zip`). Per-pin detail belongs in the device records and is not duplicated here.

---

## 4. Libraries and drivers

### 4.1 ESP-IDF

| Option | Component | Verdict |
|---|---|---|
| **`espressif/esp_lcd_ek79007`** | Component registry. Current **v2.0.2** (also published as `2.0.2~1`); the v1.0.x line targets ESP-IDF 5.x | ✅ **Use this.** It is the maintained driver and its README links the datasheet |
| Hand-rolled DPI panel + init walk | | Possible, as for any DSI panel |

Version selection mirrors the [JD9365 situation](../../jadard/jd9365/README.md#61-esp-idf): the **2.0.0 release is the ESP-IDF v6.0 compatibility break**. Pin `~1.0.4` for IDF 5.3–5.4, `^2.0.0` for IDF 6.x. **MIPI-DSI requires ESP-IDF v5.3+**, so an ESP32-P4-class part is mandatory.

### 4.2 Linux

No mainline DRM panel driver named for EK79007 was found in `drivers/gpu/drm/panel/` **[WEB]** 2026-08-30. Panels using it would typically be driven through `panel-simple-dsi` with a device-tree init sequence, or a vendor driver.

### 4.3 Arduino

None specific. As with all MIPI-DSI parts, the practical route is calling `esp_lcd_*` from an Arduino-ESP32 sketch on a P4-class chip.

---

## 5. Initialization and gotchas

1. **Two chips, one power sequence.** The gate driver has its own supply and start-pulse constraints — see the [EK73217BCGA record §4](../ek73217bcga/README.md#4-function-and-power-sequencing). Bringing the source driver up correctly while the gate driver is mis-sequenced gives a lit but blank or banded panel.
2. **`AVDD` is 8.0–13.5 V.** Much higher than the 1.8 V logic rails. Do not assume a single-rail design.
3. **Lane rate ceiling is low.** **500 Mbps at 4 lanes / 650 Mbps at 2 lanes** — well below the 1500 Mbps the JD9365 boards run. At 1024 × 600 × 24 bpp × 60 Hz you need roughly 1.06 Gbps of payload, so **4 lanes are effectively required**; a 2-lane configuration cannot carry 60 Hz at full colour depth. **[INF]** from the §1.1 figures.
4. **Dual gate.** The application block diagram is explicitly "Dual Gate (1024RGB × 600)". Panel timing assumptions that ignore dual-gate structure will be wrong.
5. **Use the auto pattern generator during bring-up.** §1.1.
6. **Prefer the Rev 1.9 `AD` document for electricals**, but consult REV1.0 when the newer one is silent — §1.2.

---

## 6. Alternatives and compatibility

| Part | Relationship | Compatible? |
|---|---|---|
| **EK79007** (base, MIPI/LVDS) | Older sibling, adds LVDS | ⚠ Not a drop-in for a MIPI-only design; see §1.2 |
| **EK73217BCGA** | The companion **gate** driver | ✅ **Designed to pair.** Not a substitute |
| **EK7616** | The part whose datasheet template both documents were derived from | ❌ Different part; the shared `Title` field is an artefact, **not** evidence of equivalence |
| **[ILI9881C](../../ilitek/ili9881c/README.md)** | The controller on **v0.0** Espressif devkits | ❌ Different part and register set; the *panel accessory* is the alternative, not the chip |
| **[JD9365](../../jadard/jd9365/README.md)** | Single-chip DSI driver, 800 × 1280 max | ❌ Different architecture (integrated gate drive) and resolution class |

---

## 7. Open questions

| Question | Status |
|---|---|
| Register map / init sequence actually sent to the fitted panel | **Open.** Not extracted in this pass; `esp_lcd_ek79007`'s default table is the place to start |
| Which lane count the Espressif panel uses | **Open.** §5.3 argues 4 lanes are required; unconfirmed |
| Panel (glass) manufacturer and part number | **Open.** Espressif documents the driver ICs but not the panel maker |
| Reference designator on the sub-board | **Open.** The sub-board schematic is retained in the device tree and would answer it |
| Lifecycle status | **Open.** Rev 1.9 dates from 2018; no PCN or EOL notice found |

---

## Manufacturer

**Fitipower Integrated Technology** — see the [Fitipower documentation-sourcing guide](../../../vendors/fitipower/README.md) for how these documents were located and this vendor's known gotchas.

## Used By

- [Espressif ESP32-P4X-Function-EV-Board](../../../devices/espressif/esp32-p4x-function-ev-board/README.md) — source driver + TCON of the **optional 7″ 1024 × 600 MIPI-DSI panel**, on the LCD adapter sub-board reached via the `1.0K-GT-15PB` 15-pin 1.0 mm FPC connector. Paired with [EK73217BCGA](../ek73217bcga/README.md). Fitted on **chip-revision v0.1** devkits.
- [Espressif ESP32-P4X-C5-Function-EV-Board](../../../devices/espressif/esp32-p4x-c5-function-ev-board/README.md) — same optional display accessory.
- [Espressif ESP32-P4-Function-EV-Board](../../../devices/espressif/esp32-p4-function-ev-board/README.md) — same family.

## Related components

- **[Fitipower EK73217BCGA](../ek73217bcga/README.md)** — the companion gate driver. **Read both; neither works alone**
- [Ilitek ILI9881C](../../ilitek/ili9881c/README.md) — the controller on **v0.0** devkit panels
- [Jadard JD9365](../../jadard/jd9365/README.md) — the other MIPI-DSI controller in this repository, single-chip
- [Espressif ESP32-P4](../../espressif/esp32-p4/README.md) — the MIPI-DSI host
- [Display interfaces guide](../../../guides/hardware/display-interfaces.md)

---

## Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/ek79007ad-datasheet.pdf` | 3 723 767 | `2dbab767e040959f1c7ce1ae3af4e65c888e04d88b066bcb1f3bddee6c8287a4` | **EK79007AD, Rev. 1.9, 2018/06/14**, 75 pp, MIPI-only. **The revision this hardware uses** |
| `artifacts/ek79007-datasheet-esp-iot-solution-mirror.pdf` | 4 084 080 | `a038ce84953f2ec30cc8d94c0148bc008f84a67ad6cee8c0707a4fcb73a6bd28` | **EK79007 REV1.0**, 92 pp, MIPI **and LVDS**. Retained as a superset — §1.2 |

Both are third-party (Fitipower) copyright, mirrored by Espressif with **no stated licence** — redistribution status **`unknown`**, disposition `repository` pending review.

**Duplication resolved 2026-08-30.** `ek79007ad-datasheet.pdf` was byte-identical to a copy at `devices/espressif/shared-artifacts/ek79007ad-datasheet.pdf`. A chip datasheet is a **component** artifact, so this is the canonical and now **the only copy**; the device-side copy has been removed and replaced by a cross-link at [`devices/espressif/shared-artifacts/DRIVER-DATASHEETS-MOVED.md`](../../../devices/espressif/shared-artifacts/DRIVER-DATASHEETS-MOVED.md). The deferral noted here previously is discharged. The `esp-iot-solution` mirror never had a device-side counterpart and is unaffected.

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published | Establishes |
|---|---|---|---|---|---|---|---|---|
| F-1 | EK79007AD datasheet Rev. 1.9 | Fitipower, mirrored by Espressif | authorized mirror | datasheet | <https://dl.espressif.com/dl/schematics/display_driver_chip_EK79007AD_datasheet.pdf> | 2026-08-30 | 2018-06-14 | §1, §1.1, §5 |
| F-2 | EK79007 datasheet REV1.0 | Fitipower, mirrored by Espressif | authorized mirror | datasheet | <https://dl.espressif.com/AE/esp-iot-solution/EK79007.pdf> | 2026-08-30 | 2015-09-25 | §1.2. Found via the `esp_lcd_ek79007` component README |
| F-3 | `esp_lcd_ek79007` component | Espressif | primary | source package | <https://components.espressif.com/components/espressif/esp_lcd_ek79007> | 2026-08-30 | v2.0.2 | §4.1 |
| F-4 | ESP32-P4X-Function-EV-Board record | this repository | primary | board doc | [device record](../../../devices/espressif/esp32-p4x-function-ev-board/README.md) | 2026-08-30 | — | §3 fitted status |
