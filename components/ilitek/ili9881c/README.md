# Ilitek ILI9881C

- **Category:** amorphous-silicon TFT LCD **single-chip driver**, 800 (RGB) × 1280, 16.7 M colour, MIPI-DSI, **without internal GRAM**
- **Research status:** full Ilitek specification retained (320 pp, V092). **This record also resolves a part-number error** that had propagated through the repository — see the box below.
- **Retrieved:** 2026-08-30

The display controller on the MIPI-DSI panel shipped with **chip-revision v0.0** Espressif ESP32-P4 devkits, and one of the selectable panel targets in Waveshare's ESP32-P4 DSI examples.

---

## ⚠ This part is `ILI9881C`. The repository called it `ILI9981C`. That part does not exist.

`ILI9981C` appears in five places in this repository — [`devices/nicolai-electronics/tanmatsu/display.md`](../../../devices/nicolai-electronics/tanmatsu/display.md) lines 117 and 123, [`guides/hardware/display-interfaces.md`](../../../guides/hardware/display-interfaces.md) lines 236, 610 and 653, and [`guides/markets/device-comparison-matrix.md`](../../../guides/markets/device-comparison-matrix.md) line 495 — always alongside a claimed ESP-IDF component `esp_lcd_ili9981c`.

**The evidence that `ILI9981C` is a transcription error for `ILI9881C`:**

| Test | Result | Verdict |
|---|---|---|
| Espressif component registry: `espressif/esp_lcd_ili9981c` | **HTTP 404** | Does not exist |
| Espressif component registry: `espressif/esp_lcd_ili9881c` | **HTTP 200**, versions 0.1.0 → **1.1.0** | Exists |
| Mainline Linux `drivers/gpu/drm/panel/` | `panel-ilitek-ili9881c.c` present; **no** `ili9981` anything. Ilitek drivers present: ili7807s, ili9322, ili9341, ili9488, ili9805, ili9806e, **ili9881c**, ili9882t | Exists as `9881` only |
| ESP-IDF, esp-bsp, esp-iot-solution repository trees | **No** `ili9981` match anywhere | Does not exist |
| Waveshare's own ESP32-P4 demo `12_camera_dsi/components/dsi_init/Kconfig.projbuild` | `config EXAMPLE_LCD_PATTERN_ILI9881C`, `bool "ILI9881C"`, defaulting to **800 × 1280** | Vendor code says `9881` |

The Waveshare Kconfig is decisive: it is in this repository already, it selects **800 × 1280**, and 800 × 1280 is exactly the ILI9881C's native resolution as printed on its specification cover.

This is the failure mode the research skill singles out — *"a part number that differs by one character from a real part is a particularly common trap"*. **No component record was created under `ili9981c`.**

**Corrected 2026-08-30.** All five live occurrences now read `ILI9881C` and link here: `devices/nicolai-electronics/tanmatsu/display.md` (the panel table and the chip-revision note), `guides/hardware/display-interfaces.md` (the revision-trap paragraph, the controller-gap list and the controller table) and `guides/markets/device-comparison-matrix.md` (the missing-record list). The occurrences retained deliberately are the ones that *document the error*, in this file, [`vendors/ilitek`](../../../vendors/ilitek/README.md) and [`components/README.md`](../../README.md).

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Stated by Ilitek in `artifacts/ili9881c-spec-3lane-mipi-gramless.pdf`, with section reference |
| **[SRC]** | Read out of driver, Kconfig or example source |
| **[VEN]** | Stated by Espressif or Waveshare in board documentation |
| **[INF]** | Inference |
| **[WEB]** | Non-manufacturer web source, dated at retrieval |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **ILI Technology Corp. ("Ilitek")**, 8F No. 38 Taiyuan St, Jhubei City, Taiwan 302 | **[DOC]** cover |
| Part | **`ILI9881C`** | **[DOC]** cover |
| Document | **Specification Version V092**, document no. **`ILI9881C_IDT_V092_20141105`**, 320 pages | **[DOC]** cover |
| Description | *"a-Si TFT LCD Single Chip Driver, 800(RGB) × 1280 Resolution and 16.7M-color"* | **[DOC]** cover |
| Resolution | **800 (RGB) × 1280** | **[DOC]** cover |
| Colour | **16.7 M** (24-bit) | **[DOC]** cover |
| Frame memory | **None — "Without Internal GRAM"** | **[DOC]** cover |
| Interface | **MIPI-DSI** | **[DOC]** §4.1 |
| ⚠ Marking verified? | **No.** COG die inside a bonded panel module | **[INF]** |
| Lifecycle | **Unknown.** The specification dates from **2014-11-05**; this is an old part | **[DOC]** |

### 1.1 Family

Ilitek's `ILI98xx` MIPI-DSI line is large. Mainline Linux carries drivers for **ILI9881C** and **ILI9882T**; **ILI9806E** is a related DSI/SPI part. `ILI9341` and `ILI9488` are much older SPI/parallel controllers **with** GRAM and are not related in architecture despite the similar numbering. **Do not treat the numbering as a compatibility guide.**

The retained document is titled by its source as the **3-lane, MIPI, GRAM-less** variant of the specification. Ilitek publishes per-configuration spec documents, so a 4-lane variant document may exist separately. **[INF]**

---

## 2. Capabilities and limits

| Area | Capability | Evidence |
|---|---|---|
| Resolution | 800 (RGB) × 1280 | **[DOC]** |
| Colour | 16.7 M, 24-bit | **[DOC]** |
| Frame memory | **None.** Host must drive continuous video | **[DOC]** |
| Interface | MIPI-DSI with documented clock and data lane behaviour (§4.1.2.2, §4.1.2.3), LP↔HS transitions (§18.4.6, §18.4.7) | **[DOC]** |
| Lane count | Configurable — `DSI Lanes Control (00h)` on page 7 | **[DOC]** §5.7.1 |
| Command pages | **11 pages (0–10)** | **[DOC]** §5.4.20 |

### 2.1 Limits worth stating

- **No GRAM**, exactly as with the [JD9365](../../jadard/jd9365/README.md). The host streams a continuous raster; there is no partial-update path and no low-power "write once and idle" mode. On ESP32-P4 this means a full framebuffer in PSRAM.
- **At 800 × 1280 × 24 bpp a frame is 2.93 MB** — larger than either Waveshare JD9365 panel. **[INF]** from the stated geometry.
- **It is a 2014 part.** Availability and lifecycle should be checked before designing it in.

---

## 3. ⭐ The command set is fully documented — unlike the JD9365

This is the most useful practical contrast in this repository's display-controller set, and worth stating plainly.

The [JD9365's public datasheet documents only the standard DCS commands](../../jadard/jd9365/README.md#4--what-the-public-datasheet-does-and-does-not-contain), leaving its entire ~250-entry vendor init table undocumented. **Ilitek publishes the opposite.** The ILI9881C specification's §5 contains per-page command descriptions across all 11 pages, with bit-field tables, defaults, restrictions and register-availability conditions per power state.

### 3.1 The page-select mechanism **[DOC]** §5.4.20

Page selection uses the **`FFh` EXTC Command Set Enable Register** with a three-byte magic:

| Parameter | Value |
|---|---|
| 1st | `98h` |
| 2nd | `81h` |
| 3rd | `PAGE[7:0]` |

```c
write(0xFF, {0x98, 0x81, page});   // page = 0x00 .. 0x0A
```

| `PAGE[7:0]` | Selects |
|---|---|
| `00h` | Page 0 — standard/DCS-style command set |
| `01h` – `0Ah` | Pages 1 – 10 |
| Others | **Reserved** |

The default is `01h`. The register is available in Normal Mode (idle on or off, sleep out) **and in Sleep In** **[DOC]**.

Compare the three paging conventions now documented in this repository:

| Controller | Page-select | Manufacturer registers documented? |
|---|---|---|
| **Ilitek ILI9881C** | `FFh` + `98h 81h <page>` | ✅ **Yes, fully** (§5) |
| [Jadard JD9365](../../jadard/jd9365/README.md) | `E0h` = page, after an `E1/E2/E3 = 93/65/F8` unlock | ❌ **No** |
| [Sitronix ST77916](../../sitronix/st77916/README.md) | `F0h`–`F3h` | ✅ Yes, in the retained spec |

**If you are reverse-engineering a JD9365 init table, the ILI9881C specification is a genuinely useful analogue** — same architecture class, same era, same kind of paged register file — for understanding *what kinds of things* live in a gate/source-timing page. It is **not** a substitute register map, and values must never be carried across. **[INF]**

### 3.2 Notable documented registers

`DSI Lanes Control (00h)` on page 7 **[DOC]** §5.7.1 — lane count is a register setting, not only a pin strap.

---

## 4. Where it is fitted

| Board | Role | Evidence |
|---|---|---|
| **Espressif ESP32-P4 devkit panel, chip revision v0.0** | The MIPI-DSI panel shipped with **v0.0** devkits. Revision **v0.1** shipped an [EK79007](../../fitipower/ek79007ad/README.md)-based panel instead | **[VEN]** via the [Tanmatsu display record](../../../devices/nicolai-electronics/tanmatsu/display.md) |
| **Waveshare ESP32-P4 Touch-LCD demos** | A selectable panel target: `CONFIG_EXAMPLE_LCD_PATTERN_ILI9881C`, defaulting to 800 × 1280, in `12_camera_dsi` | **[SRC]** |

⚠ **Honest scoping.** Unlike the other four controllers documented in this pass, the ILI9881C is **not fitted on a board that has its own record in this repository**. It is:

- named in the Tanmatsu record as the devkit panel used for cross-development against **v0.0** silicon, and
- present as a build-time panel option in a Waveshare demo tree that *is* in this repository, but which is **not selected** for the fitted panel (`# CONFIG_EXAMPLE_LCD_PATTERN_ILI9881C is not set` in both `sdkconfig` and `sdkconfig.old`) **[SRC]**.

So it is a **real part on real Espressif hardware that this repository's users encounter**, but the "Used By" relationship is weaker than for the JD9365, ST7789VW or EK79007AD. That is stated rather than papered over.

**Practical consequence:** if you cross-develop on an ESP32-P4 devkit, **check which panel you have**. v0.0 → ILI9881C, v0.1 → EK79007. The drivers are not interchangeable and neither is the init sequence.

---

## 5. Libraries and drivers

### 5.1 ESP-IDF

| Option | Component | Verdict |
|---|---|---|
| **`espressif/esp_lcd_ili9881c`** | Component registry. Versions 0.1.0, 0.2.0, 1.0.0–1.0.3, **1.1.0** (current) | ✅ **Use this.** Note there is **no `esp_lcd_ili9981c`** — that name 404s |

As with all MIPI-DSI parts, **ESP-IDF v5.3+** and an ESP32-P4-class chip are required.

### 5.2 Linux

**`drivers/gpu/drm/panel/panel-ilitek-ili9881c.c`** — a mainline DRM panel driver, in-tree for years and covering multiple panels built on this controller. If you are driving an ILI9881C panel from Linux this is the reference implementation, and like the [JD9365's kernel driver](../../jadard/jd9365/README.md#62-linux) it is also a useful source of real init sequences.

### 5.3 Arduino

None specific, and none plausible: MIPI-DSI needs a P4-class host. Call `esp_lcd_*` from an Arduino-ESP32 sketch if you need it.

---

## 6. Initialization and gotchas

1. **Page select is `FFh 98 81 <page>`, not a bare register write.** §3.1. A single-byte `FFh` write will not switch pages.
2. **The default page is `01h`, not `00h`** **[DOC]**. Do not assume you start on the standard command page — select it explicitly.
3. **Pages above `0Ah` are reserved.** Writing them is undefined.
4. **Lane count is a register (`00h` on page 7), not only a strap** — §3.2. A mismatch between the host's lane configuration and the panel's produces a dead or garbled link.
5. **No GRAM.** Any code assuming `CASET`/`RASET`/`RAMWR` partial updates will not work. §2.1.
6. **Check your devkit revision before porting an init table.** §4.
7. **Init commands should be sent in LP mode.** The same HS-vs-LP cost that dominates [JD9365 bring-up](../../jadard/jd9365/README.md#8-pitfalls) applies to any long DSI init sequence. **[INF]** — not measured for this part.

---

## 7. What the vendor demo does

**[SRC]** Waveshare `12_camera_dsi`: the ILI9881C is offered as one of several panel patterns via Kconfig, wired to 800 × 1280 defaults, inside a MIPI-CSI → MIPI-DSI passthrough example. **It is not enabled** in the shipped configuration, because the fitted Waveshare panels are [JD9365](../../jadard/jd9365/README.md)-based. The option exists because the example derives from an Espressif reference that targeted devkit panels.

No Espressif ILI9881C demo was inspected in this pass.

---

## 8. Alternatives and compatibility

| Part | Relationship | Compatible? |
|---|---|---|
| **ILI9882T** | Ilitek sibling, also mainline-supported | ❌ Different register detail; architecturally similar |
| **ILI9806E** | Ilitek DSI/SPI part | ❌ Different class |
| **[JD9365](../../jadard/jd9365/README.md)** | Jadard single-chip DSI, GRAM-less, 800 × 1280 max | ⚠ **The closest functional analogue** — same architecture, same resolution ceiling, same host requirements. Different register set and page scheme; **not** drop-in |
| **[EK79007AD](../../fitipower/ek79007ad/README.md) + [EK73217BCGA](../../fitipower/ek73217bcga/README.md)** | The panel Espressif moved to for **v0.1** devkits | ⚠ System-level alternative for the same slot; a two-chip design rather than single-chip |
| **ILI9341 / ILI9488** | Same vendor, much older, SPI/parallel **with** GRAM | ❌ Unrelated architecture despite the numbering |
| **`ILI9981C`** | **Does not exist** | ❌ See the box at the top |

---

## 9. Open questions

| Question | Status |
|---|---|
| Which Espressif devkit SKUs shipped v0.0 (ILI9881C) panels, and in what date range | **Open.** Only the revision tie-in is documented |
| Panel (glass) manufacturer and part number for the devkit panel | **Open** |
| Whether a 4-lane variant of the specification exists | **Open.** The retained document is the 3-lane, GRAM-less variant. §1.1 |
| Init sequence used by `esp_lcd_ili9881c` | **Open.** Not extracted in this pass; the component and the Linux driver both carry tables |
| Lifecycle / availability of a 2014 part | **Open** |

---

## Manufacturer

**Ilitek (ILI Technology Corp.)** — see the [Ilitek documentation-sourcing guide](../../../vendors/ilitek/README.md).

## Used By

- **Espressif ESP32-P4 devkit panel, chip revision v0.0** — MIPI-DSI display controller. No board record exists in this repository for that devkit configuration; the relationship is documented in the [Tanmatsu display record](../../../devices/nicolai-electronics/tanmatsu/display.md), which uses the devkit for cross-development. Revision v0.1 replaced it with an [EK79007](../../fitipower/ek79007ad/README.md) panel.
- [Waveshare ESP32-P4-WIFI6-Touch-LCD XC family](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md) — **selectable but not selected**: `EXAMPLE_LCD_PATTERN_ILI9881C` is a Kconfig option in the `12_camera_dsi` demo, disabled in the shipped `sdkconfig`. The fitted panels are [JD9365](../../jadard/jd9365/README.md)-based.

## Related components

- [Jadard JD9365](../../jadard/jd9365/README.md) · [programming reference](../../jadard/jd9365/jd9365-programming-reference.md) — the closest analogue, and the record that most benefits from this one's documented page scheme
- [Fitipower EK79007AD](../../fitipower/ek79007ad/README.md) · [EK73217BCGA](../../fitipower/ek73217bcga/README.md) — the v0.1 devkit panel's driver pair
- [Sitronix ST77916](../../sitronix/st77916/README.md) — a third paging convention (`F0h`–`F3h`)
- [Espressif ESP32-P4](../../espressif/esp32-p4/README.md) — the MIPI-DSI host
- [Display interfaces guide](../../../guides/hardware/display-interfaces.md)

---

## Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/ili9881c-spec-3lane-mipi-gramless.pdf` | 9 842 657 | `57b146b880b0ab446cf67a0f73e4e7bda4f271a0acc95b28086a3471f8db7ebf` | **ILI9881C Specification V092**, doc no. `ILI9881C_IDT_V092_20141105`, 320 pp. Includes the **full paged command reference** (§5) |

⚠ **Size note.** At 9.8 MB this is a large artifact, though not the largest in `components/` (the [ST77916 spec](../../sitronix/st77916/README.md) is 16.3 MB and the ESP32-P4 TRM is 23.5 MB, both retained in-repo). It is kept in the repository on the same basis: it is the only complete register reference for the part and is served from a single non-vendor host that has already proven unreliable (§ sources). Flag for review if repository size policy tightens.

Third-party (Ilitek) copyright, obtained from a third-party mirror with **no stated licence** — redistribution status **`unknown`**, disposition `repository` pending review.

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published | Establishes |
|---|---|---|---|---|---|---|---|---|
| I-1 | ILI9881C Specification V092 | Ilitek, via `internetsomething.com` | credible mirror | datasheet | <https://www.internetsomething.com/lcd/ILI9881C-3lane-mipi-gramless.pdf> | 2026-08-30 | 2014-11-05 | §1, §2, §3, §6. ⚠ Plain requests return **HTTP 520**; retrieved with a `WhatsApp/2.23.20.0` UA. This URL is the "Link to datasheet" in Espressif's own `esp_lcd_ili9881c` README, so Espressif also depends on this mirror |
| I-2 | `esp_lcd_ili9881c` component | Espressif | primary | component registry | <https://components.espressif.com/components/espressif/esp_lcd_ili9881c> | 2026-08-30 | v1.1.0 | §5.1, and the 404 that disproves `esp_lcd_ili9981c` |
| I-3 | `panel-ilitek-ili9881c.c` + `drivers/gpu/drm/panel/` listing | Linux | community (upstream, GPL) | repository | <https://github.com/torvalds/linux/tree/master/drivers/gpu/drm/panel> | 2026-08-30 | — | §5.2, and the absence of any `ili9981` driver |
| I-4 | Waveshare `12_camera_dsi` Kconfig + sdkconfig | Waveshare | primary | vendor demo | in-repo | 2026-08-30 | — | §4, §7, and the `ILI9881C` spelling in vendor code |
| I-5 | Tanmatsu display record | this repository | primary | device doc | [display.md](../../../devices/nicolai-electronics/tanmatsu/display.md) | 2026-08-30 | — | §4 devkit revision tie-in — **and the source of the `ILI9981C` typo** |
