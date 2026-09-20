# Sitronix ST7789VW

- **Category:** single-chip TFT-LCD controller/driver with on-chip frame memory, up to 240 × 320, SPI / parallel 8080 / RGB / VSYNC interfaces
- **Research status:** the **full Sitronix specification is retained** in `artifacts/` (317 pages, V1.0). Board-side integration is thin because Espressif does not publish a GPIO map or schematic for the fitted display.
- **Retrieved:** 2026-08-30

The display controller of the 1.54-inch 240 × 240 SPI LCD on the [Espressif ESP32-P4X-EYE](../../../devices/espressif/esp32-p4x-eye/README.md) and its predecessor the [ESP32-P4-EYE](../../../devices/espressif/esp32-p4-eye/README.md). It is bonded inside the `ZJY154KC-IF17` panel module.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Stated by Sitronix in `artifacts/st7789vw-datasheet.pdf`, with page reference |
| **[VEN]** | Stated by Espressif in board documentation or the retained module spec |
| **[SRC]** | Read out of driver or example source |
| **[INF]** | Inference |
| **[WEB]** | Non-manufacturer web source, dated at retrieval |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Sitronix Technology Corp.** (矽創電子) | **[DOC]** |
| Part | **`ST7789VW`** | **[DOC]** cover |
| Document | **ST7789VW Datasheet Version 1.0, 2017/09**, 317 pages | **[DOC]** PDF title `ST7789VW_SPEC_V1.0` |
| Max resolution | **240 RGB (H) × 320 (V)** | **[DOC]** §2 |
| Driver outputs | 720 source channels (240 × RGB) + 320 gate channels + common electrode | **[DOC]** §1, §2 |
| Frame memory | **240 × 320 × 18 bit = 1 382 400 bits** on-chip | **[DOC]** §2 |
| Resolution as used | **240 × 240** (the module is a square 1.54″) | **[VEN]** |
| Interface as used | **SPI** | **[VEN]** |
| Module | `ZJY154KC-IF17`, 1.54-inch, adhesive-and-metal bonded construction | **[VEN]** module spec retained in the device tree |
| Reference designator | **Not published.** Espressif releases no schematic for the EYE boards' display | **[INF]** |
| ⚠ Marking verified? | **No.** The die is COG inside a bonded module. Identification rests on Espressif naming the part and shipping its datasheet | **[VEN]** |

### 1.1 Family and variants

`ST7789` is a large family and the suffixes are **not** interchangeable:

| Part | Difference | Note |
|---|---|---|
| **ST7789VW** | The part documented here | The one Espressif ships the datasheet for |
| ST7789V / ST7789V2 / ST7789VI | Sibling variants with differing interface and NV-memory options | ⚠ **Do not substitute datasheets.** Init sequences commonly transfer, but electrical and NV details do not |
| ST7789S / ST7789H2 | Further variants seen in modules | Not documented here |

The repository elsewhere mentions `ST7789P` and `ST7789VW` in Waveshare context; those are **candidate strings from other boards' material, not findings about this board**.

---

## 2. Capabilities and limits

**[DOC]** §2 unless noted.

| Area | Capability |
|---|---|
| Resolution | Up to **240 × 320**; programmable partial display duty |
| Colour modes | **262 K full colour** (RGB666 max, idle mode off); **8 colour** (RGB111, idle mode on) |
| Pixel formats | **12 bpp** RGB444, **16 bpp** RGB565, **18 bpp** RGB666 — selected by `COLMOD` (`3Ah`) |
| ⚠ No RGB888 | The frame memory is **18 bits deep**. 262 K colours is the hardware maximum |
| Host interfaces | **SPI**; parallel **8080** (8/9/16/18-bit); **RGB** (6/16/18-bit with VSYNC/HSYNC/DOTCLK/ENABLE/DB[17:0]); **VSYNC** interface |
| Frame memory | **Yes** — the host does not need a framebuffer; partial areas can be streamed |
| Gamma | **4 preset gamma curves** with separate RGB gamma setting |
| On-chip | DC/DC converter, adjustable VCOM generation, timing controller |
| NV memory | Non-volatile store for initial register settings and factory defaults (module ID, module version); 8 bits for ID1 |
| Display features | CABC (content adaptive brightness control), colour enhancement |

### 2.1 Limits worth stating

- **On-chip GRAM is the defining feature.** Unlike the GRAM-less MIPI-DSI parts elsewhere in this repository ([JD9365](../../jadard/jd9365/README.md), [ILI9881C](../../ilitek/ili9881c/README.md)), the ST7789VW retains the image. The host writes only what changed, via `CASET`/`RASET`/`RAMWR` (`2Ah`/`2Bh`/`2Ch`), and may then go idle. This is what makes it viable on small MCUs.
- **240 × 240 on a 240 × 320 controller means an offset.** When a 240 × 240 panel is bonded, the visible window may not start at GRAM row 0. If the top or bottom 80 rows are blank or wrapped, you need a row offset (`esp_lcd_panel_set_gap()` or equivalent) — this is the single most common ST7789 integration bug. **[INF]** for this specific module; the required offset is not published by Espressif.
- **262 K colours maximum.** Code written for RGB888 panels must down-convert.

---

## 3. Wiring on the EYE boards

⚠ **Not established.** Espressif publishes **no schematic and no GPIO map** for the ESP32-P4X-EYE or ESP32-P4-EYE display. The board records list the LCD as "1.54-inch, 240 × 240, SPI, ST7789VW controller" and nothing further **[VEN]**.

What is known:

| Property | Value | Evidence |
|---|---|---|
| Interface | SPI | **[VEN]** |
| Resolution | 240 × 240 | **[VEN]** |
| Module | `ZJY154KC-IF17` | **[VEN]** |
| SPI host, CLK/MOSI/CS/DC/RST/backlight GPIOs | **Unknown — not published** | — |

The predecessor ESP32-P4-EYE's published document list included a schematic and PCB layout; the successor's replaced them with a (broken) reference-design ZIP — a **regression in published detail**. If you need the pin map, the P4-EYE schematic is the place to look, and that gap is tracked in the device records rather than here.

---

## 4. Initialization requirements and gotchas

**[DOC]** plus general ST77xx practice.

1. **Reset.** Hardware reset via `RESX`, or software `SWRESET` (`01h`). Sitronix parts need settling time after reset before further commands; the widely used figure is **120 ms**, matching the `SLPOUT` requirement.
2. **`SLPOUT` (`11h`) then wait 120 ms.** Load-bearing on every Sitronix controller. Skipping it produces intermittent blank or corrupted panels.
3. **`COLMOD` (`3Ah`) must be sent.** Choose `0x55` (RGB565), `0x53` (RGB444) or `0x66` (RGB666). Do not rely on the reset default.
4. **`MADCTL` (`36h`)** sets rotation, mirroring and BGR order. On a square 240 × 240 module, rotation also changes which GRAM offset you need — see §2.1.
5. **`INVON` (`21h`) is usually required.** Most 240 × 240 IPS modules ship needing display inversion on. If your image is colour-negative, this is why.
6. **The gap/offset.** §2.1. Symptom: an 80-pixel band of garbage or a vertically shifted image.
7. **The backlight is not a controller function.** It is a separate GPIO/PWM path.
8. **NV memory exists.** The module may already carry factory register settings; a mismatch between those and your init table can produce subtly wrong gamma. **[INF]**

---

## 5. Tearing effect

The ST7789VW provides a **TE output pin** with `TEON` (`35h`), `TEOFF` (`34h`) and set-tear-scanline (`44h`) **[DOC]**. Because the part has GRAM, TE is genuinely useful here — synchronising `RAMWR` bursts to the panel's vertical blanking removes tearing on full-screen animation.

Whether `TE` is bonded out and routed on the EYE boards is **unknown** (§3).

---

## 6. Power and sleep modes

**[DOC]**

| Mode | Command | Note |
|---|---|---|
| Sleep in | `SLPIN` (`10h`) | DC/DC and most analogue off; GRAM retained |
| Sleep out | `SLPOUT` (`11h`) | **+120 ms** before further commands |
| Display off / on | `DISPOFF` (`28h`) / `DISPON` (`29h`) | Blanks output without losing GRAM |
| Idle mode on/off | `IDMON` (`39h`) / `IDMOFF` (`38h`) | Drops to **8 colours** for low power |
| Partial mode | `PTLON` (`12h`) + `PTLAR` (`30h`) | Drives only part of the panel — programmable partial duty |
| Normal mode | `NORON` (`13h`) | |

Idle mode plus partial mode is the combination that makes this part attractive for always-on status displays.

---

## 7. Libraries and drivers

### 7.1 ESP-IDF

| Option | Component | Verdict |
|---|---|---|
| **`esp_lcd_panel_st7789`** — built into ESP-IDF | `esp_lcd` core, no dependency needed: `esp_lcd_new_panel_st7789()` | ✅ **Use this.** ST7789 is one of the few controllers with a driver in ESP-IDF itself rather than the component registry |
| `esp_lcd_panel_io_spi` + custom ops | | Only if you need something the core driver does not expose |

Because the driver is in-tree, there is **no component version to pin** — behaviour tracks your ESP-IDF version. MIPI-DSI is irrelevant here; this is a plain SPI panel and works on any ESP32 family member.

Typical bring-up: `spi_bus_initialize()` → `esp_lcd_new_panel_io_spi()` (with a real `dc_gpio_num`, unlike QSPI parts) → `esp_lcd_new_panel_st7789()` → `reset()` → `init()` → `esp_lcd_panel_set_gap()` if needed → `esp_lcd_panel_disp_on_off(true)`.

### 7.2 Arduino

Unusually well served — ST7789 is one of the most widely supported controllers in the hobby ecosystem **[WEB]** 2026-08-30:

| Library | Note |
|---|---|
| **TFT_eSPI** (Bodmer) | Mature, fast, `ST7789_DRIVER` with explicit 240×240 support and offset handling |
| **Adafruit_ST7735/ST7789** | Simple, well documented, GFX-compatible |
| **Arduino_GFX** (moononournation) | Broadest bus/panel coverage; good if you also drive other panels |
| **LovyanGFX** | Fast, good ESP32 support, `Panel_ST7789` class |

All four handle the 240 × 240 row-offset problem explicitly, which is the main reason to prefer one over hand-rolled code.

### 7.3 Linux

`drivers/gpu/drm/tiny/st7789v.c` and the `panel-sitronix-st7789v` bindings exist upstream for SPI ST7789 panels **[WEB]**.

---

## 8. What the vendor demo does

⚠ **Not established for these boards.** No display example source for the EYE boards was inspected during this pass; the device records do not carry a demo tree for them. This section is left explicitly open rather than filled by assumption. If you have the ESP32-P4-EYE demo, its display bring-up would settle §3 and the §2.1 offset in minutes.

---

## 9. Alternatives and compatibility

| Part | Relationship | Compatible? |
|---|---|---|
| **ST7789V / V2 / VI** | Sibling variants | ⚠ Init tables usually transfer; **datasheets do not**. Verify NV and interface details |
| **ST7735 / ST7735S** | Smaller Sitronix sibling, 132 × 162 | ❌ Different resolution class, similar command style |
| **ST7796** | Larger Sitronix sibling, 320 × 480 | ❌ Different resolution |
| **[ST77916](../../sitronix/st77916/README.md)** | Sitronix, 360 × 360 round, QSPI | ❌ Different interface and resolution; shares `F0` page-select and gamma conventions |
| **ILI9341** | The other ubiquitous 240 × 320 SPI controller | ⚠ **Very close functional substitute** — same resolution class, same GRAM model, same `2Ah`/`2Bh`/`2Ch` addressing. Different init table and gamma registers. Most libraries support both |
| **GC9A01** | 240 × 240 **round** SPI controller | ⚠ Same resolution, similar model; frequently confused with ST7789 in round-display projects |
| **[JD9365](../../jadard/jd9365/README.md)** / **[ILI9881C](../../ilitek/ili9881c/README.md)** | MIPI-DSI, GRAM-less | ❌ Fundamentally different architecture (§2.1) |

---

## 10. Open questions

| Question | Status |
|---|---|
| GPIO map for the LCD on the EYE boards | **Open.** Not published by Espressif. §3 |
| Required GRAM row/column offset for this 240 × 240 module | **Open.** §2.1 |
| Is `TE` bonded out and routed? | **Open.** §5 |
| Colour format and rotation actually used by the factory firmware | **Open.** §8 |
| `ZJY154KC-IF17` module manufacturer | **Open.** The module spec is retained in the device tree but the maker is not clearly identified |

---

## Manufacturer

**Sitronix** — see the [Sitronix documentation-sourcing guide](../../../vendors/sitronix/README.md) for document portals, URL patterns, part-numbering conventions and known gotchas.

## Used By

- [Espressif ESP32-P4X-EYE](../../../devices/espressif/esp32-p4x-eye/README.md) — controller of the **1.54-inch 240 × 240 SPI** LCD, module `ZJY154KC-IF17`. GPIO map not published.
- [Espressif ESP32-P4-EYE](../../../devices/espressif/esp32-p4-eye/README.md) — the EOL predecessor; **same display, same controller**. Its published document set included a schematic, which the successor's does not.

## Related components

- [Sitronix ST77916](../../sitronix/st77916/README.md) · [ST77916 programming reference](../../sitronix/st77916/st77916-programming-reference.md) — the QSPI sibling, with a much deeper command reference that is broadly applicable to Sitronix conventions
- [Sitronix ST7701S](../../sitronix/st7701s/README.md) — the RGB/DSI sibling
- [Espressif ESP32-P4](../../espressif/esp32-p4/README.md) — the SPI host
- [Display interfaces guide](../../../guides/hardware/display-interfaces.md) — SPI vs QSPI vs MIPI-DSI

---

## Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/st7789vw-datasheet.pdf` | 3 135 599 | `1f9e956057e3909c0714bdab9e682205e03cf52adefd5b4a01093fa3167d398b` | **ST7789VW Datasheet V1.0, 2017/09**, 317 pp. PDF title `ST7789VW_SPEC_V1.0` |

**Provenance note.** Upstream this file is served under a **percent-encoded Chinese filename**, `ST7789VW芯片手册.pdf` (`ST7789VW%E8%8A%AF%E7%89%87%E6%89%8B%E5%86%8C.pdf` — "ST7789VW chip manual"). It was renamed to portable ASCII on retrieval, per the repository filename policy.

**Duplication resolved 2026-08-30.** A byte-identical copy used to sit at `devices/espressif/shared-artifacts/st7789vw-datasheet.pdf`. Per the repository taxonomy a chip datasheet is a **component** artifact, so **this is the canonical and now the only copy**; the device-side copy has been removed and replaced by a cross-link at [`devices/espressif/shared-artifacts/DRIVER-DATASHEETS-MOVED.md`](../../../devices/espressif/shared-artifacts/DRIVER-DATASHEETS-MOVED.md). The deferral noted here previously is discharged.

Third-party (Sitronix) copyright, mirrored by Espressif with no stated licence — redistribution status **`unknown`**, disposition `repository` pending review. The document carries an explicit confidentiality footer on every page ("Sitronix Confidential … shall not be distributed, reproduced, or disclosed in whole or in part without prior written permission"), which is a **strict term** and should be reviewed before this artifact is published anywhere.

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | ST7789VW Datasheet V1.0 | Sitronix, mirrored by **Espressif** | authorized mirror | datasheet | <https://dl.espressif.com/AE/esp-dev-kits/ST7789VW%E8%8A%AF%E7%89%87%E6%89%8B%E5%86%8C.pdf> | 2026-08-30 | 2017-09 | §1, §2, §4–§6 |
| S-2 | ESP32-P4X-EYE board record | Espressif via this repository | primary | board doc | [device record](../../../devices/espressif/esp32-p4x-eye/README.md) | 2026-08-30 | — | §1 fitted status, §3 what little is published |
| S-3 | `ZJY154KC-IF17` module specification | Espressif mirror | authorized mirror | module spec | `dl.espressif.com/AE/esp-dev-kits/` (percent-encoded Chinese filename) | 2026-08-21 (prior pass) | — | Module identity |
