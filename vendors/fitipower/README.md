# Fitipower — Documentation Sourcing Guide

**Fitipower Integrated Technology Inc.** (天鈺科技) — Taiwanese fabless supplier of display driver ICs and power-management ICs.

Research retrieved **2026-08-30**.

> **The one-line answer:** as with [Jadard](../jadard/README.md), no usable vendor portal was found; both Fitipower documents in this repository come from **Espressif's CDN**. Unlike Jadard, Fitipower's documents are substantive and complete — but **two different revisions circulate under the same name**, and their PDF metadata is misleading.

---

## 1. Who they are

A display-driver and PMIC house. Two product-line prefixes matter here:

| Prefix | Line | Example |
|---|---|---|
| `EK` | Display driver ICs — source drivers, TCONs, gate drivers | `EK79007AD`, `EK73217BCGA`, `EK7616` |
| `FP` | Power management ICs, including LCD bias PMICs | `FP7721`, `FP7723` |

The `FP` line shows up as the recommended power companion in **[Jadard's](../jadard/README.md)** JD9365DA-H3 application note — so Fitipower parts appear on boards whose display *controller* is a competitor's. This is one reason the two vendors get conflated; this repository previously misattributed the [JD9365](../../components/jadard/jd9365/README.md) to Fitipower.

---

## 2. Parts we document

| Part | Record | What it is |
|---|---|---|
| **EK79007AD** | [components/fitipower/ek79007ad](../../components/fitipower/ek79007ad/README.md) | 1536-ch source driver + TCON, MIPI-DSI, 1024×600 class |
| **EK73217BCGA** | [components/fitipower/ek73217bcga](../../components/fitipower/ek73217bcga/README.md) | 1200/1152/1080/960-output gate driver, 2-level, +40 V |

**They are a pair**, not alternatives: source driver + gate driver for one 7-inch panel. See [EK79007AD §2](../../components/fitipower/ek79007ad/README.md#2-role-in-the-panel-it-is-half-of-a-pair).

---

## 3. Documentation: where it actually comes from

No public Fitipower datasheet index or download portal was found. Both documents came from Espressif, from **two different paths on the same CDN**:

| Document | URL | Notes |
|---|---|---|
| EK79007**AD** datasheet, Rev 1.9 (2018), 75 pp | `https://dl.espressif.com/dl/schematics/display_driver_chip_EK79007AD_datasheet.pdf` | The `dl/schematics/` path — board-support documents |
| EK79007 datasheet, REV1.0 (2015), 92 pp | `https://dl.espressif.com/AE/esp-iot-solution/EK79007.pdf` | The `AE/esp-iot-solution/` path — component-library documents |
| EK73217BCGA datasheet, Rev 1.0 (2017), 26 pp | `https://dl.espressif.com/dl/schematics/display_driver_chip_EK73217BCGA_datasheet.pdf` | `dl/schematics/` |

All three fetch cleanly with a normal browser UA.

### 3.1 Two Espressif paths, two different revisions

**This is the reusable finding.** Espressif hosts driver-IC documents under at least two path families, and they do **not** carry the same revisions:

| Path | Populated from | Naming |
|---|---|---|
| `dl.espressif.com/dl/schematics/` | Board/devkit support material | `display_driver_chip_<PART>_datasheet.pdf` |
| `dl.espressif.com/AE/esp-iot-solution/` | ESP-IDF component library | `<PART>.pdf`, `<PART>_DS_<ver>_<date>.pdf` |

For EK79007 these two paths served **genuinely different documents** — a 2015 REV1.0 covering MIPI **and LVDS** in 92 pages, and a 2018 Rev 1.9 covering the MIPI-only `AD` variant in 75 pages. Different sizes, different hashes, different content.

**Check both paths before concluding you have "the" datasheet.** The [ESP-IDF component README trick](../jadard/README.md#31--the-highest-yield-trick-read-the-esp-idf-component-readme) surfaces the `AE/esp-iot-solution/` copy; board documentation surfaces the `dl/schematics/` one.

---

## 4. ⚠ Gotcha: the PDF metadata is wrong on every document

Both Fitipower datasheets retained here have an internal PDF **`Title` of `EK7616DS`**, author `sally.chen`:

| File | Cover part | PDF `Title` | PDF `Author` |
|---|---|---|---|
| `ek79007ad-datasheet.pdf` | EK79007AD | **`EK7616DS`** | `sally.chen` |
| `ek73217bcga-datasheet.pdf` | EK73217BCGA | **`EK7616DS`** | `sally.chen` |
| `ek79007-...-mirror.pdf` | EK79007 | `Microsoft Word - EK79007_DS_REV1.0.doc` | `james.chen` |

Fitipower produces datasheets by **editing an existing `EK7616` document template**. Practical consequences:

1. **Never identify a Fitipower document by its metadata.** Read the cover page and the running header.
2. **Do not build tooling that files or deduplicates these by `Title`** — two unrelated parts would collide.
3. Inherited section ordering and boilerplate across `EK` datasheets is explained by this, and it is a reason to prefer body text when a document contradicts itself.
4. Conversely, the metadata *is* useful evidence of document lineage and revision date — the `CreationDate` fields (2015-09-25 / 2017-07-28 / 2018-06-13) are consistent with the cover revisions and helped establish that the two EK79007 files are distinct revisions rather than a corrupted download.

Recorded per the research skill's *"read a document's own metadata"* guidance, which is what surfaced this.

---

## 5. Part numbering

`EK` + digits + variant letters, e.g. `EK79007AD`, `EK73217BCGA`, `EK7616`.

- The **base number** identifies the family (`79007`, `73217`).
- **Trailing letters are significant.** `EK79007` and `EK79007AD` differ in interface support (MIPI+LVDS vs MIPI-only) and are three years apart. **Do not treat a base-number datasheet as authoritative for a suffixed part.**
- Source drivers and gate drivers are numbered in the same space with no obvious prefix distinguishing function — `EK79007AD` is a source driver, `EK73217BCGA` a gate driver, and only the cover subtitle tells you which.

`FP` + digits for PMICs, e.g. `FP7721`, `FP7723`.

---

## 6. What the documents contain

Substantively better than [Jadard's](../jadard/README.md#4--what-the-jd9365da-h3-datasheet-does-not-contain):

| Present | Absent / thin |
|---|---|
| General description, full feature list, block diagram | **No MIPI-DSI register/command map** in the EK79007AD document as surveyed |
| Application block diagrams (dual-gate, GIP and non-GIP variants) | Panel-specific init sequences |
| Pad sequence, application power circuit | |
| Function description incl. **power ON/OFF sequencing** and start-pulse limits (gate driver) | |
| Full electrical spec, timing waveforms, operation timing | |
| Chip outline, bump pitch, bump centre coordinates | |

For the actual init sequence, use the **`espressif/esp_lcd_ek79007`** component (§7).

---

## 7. Software

| Part | Driver |
|---|---|
| EK79007(AD) | **`espressif/esp_lcd_ek79007`** — component registry, current **v2.0.2** (also `2.0.2~1`). v2.0.0 is the ESP-IDF v6.0 break; pin `~1.0.4` for IDF 5.x |
| EK73217BCGA | **None, and none needed** — it has no host interface |

No mainline Linux DRM panel driver named for EK79007 was found as of 2026-08-30.

---

## 8. Access notes

| Item | Status |
|---|---|
| `dl.espressif.com` | Clean with a normal browser UA; supports range requests (`HTTP 206`) |
| Vendor site | No usable public document portal found |
| Search engines | Ineffective for these parts, as for Jadard |
| Licensing | Third-party copyright, mirrored by Espressif with **no stated licence**. Redistribution status **`unknown`** for all three files |

---

## 9. Checklist for the next Fitipower part

1. Try **both** Espressif paths (§3.1) — `dl/schematics/display_driver_chip_<PART>_datasheet.pdf` and `AE/esp-iot-solution/<PART>.pdf`.
2. Check the **ESP-IDF component registry** for `esp_lcd_<part>` and read its README's datasheet link.
3. **Hash whatever you get.** If two paths give different hashes, keep both — they are probably different revisions (§3.1).
4. **Ignore the PDF `Title` field** (§4). Identify from the cover page.
5. Check whether the part is a **source driver, gate driver or TCON** — the numbering does not tell you, and a panel usually needs two chips.
6. Validate `%PDF-` magic.
7. Record failures in [`component-download-failures.txt`](../../component-download-failures.txt).

---

## 10. Sources

| Title | URL | Retrieved | Notes |
|---|---|---|---|
| EK79007AD datasheet Rev 1.9 | <https://dl.espressif.com/dl/schematics/display_driver_chip_EK79007AD_datasheet.pdf> | 2026-08-30 | 3 723 767 B, `2dbab767…` |
| EK79007 datasheet REV1.0 | <https://dl.espressif.com/AE/esp-iot-solution/EK79007.pdf> | 2026-08-30 | 4 084 080 B, `a038ce84…`. **Different document**, §3.1 |
| EK73217BCGA datasheet Rev 1.0 | <https://dl.espressif.com/dl/schematics/display_driver_chip_EK73217BCGA_datasheet.pdf> | 2026-08-30 | 1 571 109 B, `bd4ec28f…` |
| `esp_lcd_ek79007` component | <https://components.espressif.com/components/espressif/esp_lcd_ek79007> | 2026-08-30 | v2.0.2 |

## Related

- [EK79007AD component record](../../components/fitipower/ek79007ad/README.md) · [EK73217BCGA component record](../../components/fitipower/ek73217bcga/README.md)
- [Jadard sourcing guide](../jadard/README.md) — the vendor whose parts were misattributed to Fitipower, and whose PMIC companions are Fitipower `FP` parts
- [Ilitek sourcing guide](../ilitek/README.md) — the controller on the *other* Espressif devkit panel revision
- [Espressif sourcing guide](../espressif/README.md) — the CDN doing the hosting, and its path conventions
- [Vendor guides index](../README.md)
