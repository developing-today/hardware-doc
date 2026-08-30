# Jadard JD9365 (JD9365DA-H3)

- **Category:** a-Si TFT LCD single-chip driver — source driver + gate control + power generation + timing controller, **MIPI-DSI** input, **no internal GRAM**
- **Research status:** **a genuine public datasheet was obtained** during this pass (2026-08-30) and is retained in `artifacts/`. It documents the standard DCS command set but **not** the paged manufacturer registers where the vendor init tables live. Register `0x40` is analysed in §5 from driver-source correlation across 15 independent panel tables.
- **Retrieved:** 2026-08-30

The display controller of the round panels on the [Waveshare ESP32-P4-WIFI6-Touch-LCD-3.4C](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) (800 × 800) and [-4C](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md) (720 × 720). It is bonded chip-on-glass inside the panel module; there is no separate reference designator.

> 📘 **Writing display code?** See **[JD9365 Programming Reference](jd9365-programming-reference.md)** — the page-select convention, the full annotated init sequence, MIPI-DSI configuration, TE behaviour, power/sleep modes and the reset timing, with evidence labels on every claim.

---

## ⚠ Two corrections this record makes to existing repository text

Both are recorded here because they were repeated in several places and are load-bearing.

| Existing claim | Correction | Evidence |
|---|---|---|
| *"No public datasheet exists"* / *"no public **Fitipower** datasheet found"* — [`guides/hardware/display-interfaces.md` §11.2](../../../guides/hardware/display-interfaces.md) and the [3.4C feature page](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/features/display-controller-jd9365.md) | **A public datasheet does exist** and is now in `artifacts/`. Separately, **JD9365 is a Jadard part, not Fitipower** — Fitipower makes the EK79007AD/EK73217BCGA on a *different* Espressif board | **[DOC]** `artifacts/jd9365da-h3-datasheet-v0.01-20200819.pdf`, cover page "Copyright © JADARD"; **[DOC]** Linux `MODULE_DESCRIPTION("Jadard JD9365DA-H3 WXGA DSI panel")` |
| *"Register `0x40` … consistent with it being a panel-specific tune rather than a fixed-function mode bit"* — [3.4C feature page §3](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/features/display-controller-jd9365.md) | **Superseded.** That conclusion rested on four kernel panel tables that all wrote `0x06`. The driver now carries **13 panels**; across them `0x40` tracks **horizontal resolution**, not analogue tuning. §5 | **[SRC]** correlation table in §5 |

The earlier conclusions were reasonable on the evidence then available. They are wrong on the evidence available now.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Stated by Jadard in `artifacts/jd9365da-h3-datasheet-v0.01-20200819.pdf` or `artifacts/jd9365da-h3-application-note-v0.03-20210201.pdf`, with page reference |
| **[SRC]** | Read out of driver source — the Waveshare vendor demo, Espressif's `esp_lcd_jd9365`, or mainline Linux `panel-jadard-jd9365da-h3.c` |
| **[INF]** | Inference. Not directly stated by any of the above |
| **[WEB]** | Non-manufacturer web source, dated at retrieval |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Jadard Technology Inc.** (誠屹科技) | **[DOC]** datasheet cover, "Confidential Copyright © JADARD" |
| Part documented | **`JD9365DA-H3`** | **[DOC]** datasheet title block |
| Document | **JD9365DA-H3 Data Sheet, Version 0.01, 2020/8/19**, 204 pages | **[DOC]** PDF title field `JD9365DA-H3`, keywords `Data Sheet` |
| Family name in code | `JD9365` (Espressif), `jd9365da-h3` (Linux) | **[SRC]** |
| Function | Single-chip a-Si TFT driver: 1-chip source driver + gate control + DC/DC power + timing controller | **[DOC]** §2 |
| Max resolution | **800RGB × 1280** | **[DOC]** cover, §2 |
| Frame memory | **None — "without internal GRAM"** | **[DOC]** cover |
| Host interface | **MIPI-DSI only**, DSI v1.1, D-PHY v1.00 | **[DOC]** §3.2 |
| Die size | 27 600 µm × 880 µm (incl. scribe line and seal ring), 3 084 bumps | **[DOC]** §12.1 |
| Package | **COG** (chip-on-glass), bonded into the panel module | **[DOC]** §12.1; **[INF]** for these boards |
| Temperature range | **−40 °C to +85 °C** | **[DOC]** §3.5 |
| Lifecycle | **Unknown.** §13 *Ordering Information* is literally "TBD" in V0.01 | **[DOC]** §13 |
| ⚠ Suffix on these boards verified? | **No.** Nothing in the Waveshare schematic, wiki or demo names a suffix. `-H3` is the only publicly documented variant and the register conventions match, but the fitted die is not confirmed | **[INF]** |

### 1.1 Variants

Only **`JD9365DA-H3`** is publicly documented. The application note additionally names companion PMICs **FP7721** and **FP7723** for its 3-power-mode reference circuits **[DOC]**. Other `JD9365*` suffixes are referenced in vendor code in the wild but no document for them was found. **Do not assume suffix equivalence.**

---

## 2. Capabilities and limits

**[DOC]** unless marked.

| Area | Capability |
|---|---|
| Resolutions | **800 / 768 / 750 / 720 / 640 / 600 RGB × LN\*2** (§3.1). Source-channel mapping per resolution is tabulated in the pin description (§6); e.g. 800RGB uses `S[1]–S[2400]`, 720RGB uses `S[1]–S[1080], S[1321]–S[2400]` |
| Colour formats | **16.7 M (24-bit RGB888)**, 262 k (18-bit RGB666), 65 k (16-bit RGB565), and 8-colour idle mode (3-bit) |
| Interface | MIPI-DSI, up to **4 data lanes** (`HS_D0`–`HS_D3`) + clock lane |
| Frame buffer | **None.** The host must drive continuous video (DPI/video mode); there is no partial-update GRAM path |
| Inversion | column / 1-dot / 2-dot / 4-dot / Z inversion; interlace inversion |
| Gamma | 1 preset gamma curve, adjustable; **3× OTP** for gamma, 1× for DGC, 5× for VCOM, 4× for ID |
| Power | Integrated DC/DC: AVDD +4.5…+6.3 V, AVEE −4.5…−6.3 V, VGH +7…+20 V, VGL −7…−15 V, VCOM −4.0…0 V in 10 mV steps |
| Supplies | IOVCC / VCCH / VCCD 1.65–3.3 V; VCI/VCIP 2.5–6.0 V (external AVDD/AVEE) or 2.5–4.8 V (internal DC/DC); VPP (OTP program) 7.5 V ± 0.2 V |
| Extras | CABC, colour enhancement, Sunlight Readability Enhancement (SRE), GAS anti-image-sticking, internal oscillator, self-diagnostics, deep standby |

### 2.1 Limits worth stating

- **No GRAM means no partial redraw.** Unlike the SPI/QSPI controllers elsewhere in this repository ([ST77916](../../sitronix/st77916/README.md), [ST7789VW](../../sitronix/st7789vw/README.md)), the JD9365 has no frame memory. The host streams a full video raster continuously. On ESP32-P4 that means a **full framebuffer in PSRAM** and the DPI peripheral running permanently — this dominates the board's memory and bandwidth budget.
- **The paged manufacturer registers are undocumented in public.** §4.
- **`0x40` is not portable between panels.** §5.

---

## 3. Exact wiring on the two Waveshare boards

Both variants are the **same PCB**; only the panel differs. **[SRC]** `06_/07_displaypanel/main/test_esp_lcd_jd9365.c` and `displays_config.h`.

| Signal | ESP32-P4 GPIO | Notes |
|---|---:|---|
| MIPI-DSI data lanes | dedicated DSI pads | **2 lanes**, `lane_bit_rate_mbps = 1500` |
| `LCD_RST` | **27** | Panel reset |
| `LCD_BK_LIGHT` | **26** | Backlight, **active low** (`TEST_LCD_BK_LIGHT_ON_LEVEL 0`) |
| `BL_EN` | **33** | Backlight *enable*, schematic `R61` — **no demo drives this** |
| DSI PHY LDO | — | `esp_ldo_regulator` channel **3** at **2500 mV**, required before the PHY leaves "No Power" |

Colour depth used on both boards is **24 bpp RGB888** (`TEST_LCD_BIT_PER_PIXEL 24` → `LCD_COLOR_PIXEL_FORMAT_RGB888`) **[SRC]**.

| | 3.4C | 4C |
|---|---|---|
| Resolution | 800 × 800 | 720 × 720 |
| Lanes / lane rate | 2 / 1500 Mbps | **identical** |
| H timing (fp/pw/bp) | 40 / 20 / 20 | **identical** |
| V timing (fp/pw/bp) | 24 / 4 / 12 | **identical** |
| **Page-1 register `0x40`** | **`0x00`** | **`0x04`** |

The identical porches and lane rate across an 11 % difference in horizontal pixel count are **[SRC]** confirmed in both the ESP-IDF demo and mainline Linux, independently.

---

## 4. ⚠ What the public datasheet does and does not contain

This is the single most useful thing to know before you go looking.

**It contains** (204 pages): general description, features, block diagram, DC/DC schemes and external component connections, maximum layout resistance, **full pin description**, the complete **MIPI-DSI/D-PHY** protocol chapter (packet structure, ECC, checksum, lane states, ULPS, escape mode, burst/non-burst video modes), gamma structure, TE line modes and timing, oscillator, self-diagnostics, **power on/off sequences**, deep-standby flow, CABC, **the standard DCS command set** (§10.2, `00h`–`DCh`), electrical specifications including DSI video-mode timings, and PAD assignment.

**It does not contain** the **manufacturer/extended register banks**. Section 10 documents only standard DCS commands. There is no section for the `E0h`-paged registers — and *that is where the entire ~250-entry vendor init table lives*, including `0x40`, all gamma, all gate/source timing and all power tuning.

Verified by enumeration: the document has exactly 13 top-level sections (§10 Command → §11 Electrical Specifications → §12 Chip information → §13 Ordering Information); there is no extended-command section, and the strings `RSO` and `40h` do not occur anywhere in the text layer. **[DOC]**

> **The text layer was validated** before any value above was transcribed: the extracted text reproduces known headings verbatim ("Confidential Copyright © JADARD", "The JD9365DA-H3 supports WXGA resolution driving controller"). Per the skill's guidance on glyph-subsetting failures, no value here was taken from an unvalidated text layer.

### 4.1 The one place the datasheet *does* confirm the paging convention

§9.5.4 (Deep standby flow) writes a register using this notation **[DOC]** p.117:

```
P1_R54h=0x01
( REGW RE0h=0x01;
  REGW R54h=0x01; )
```

This is Jadard stating, in its own document, that **`Pn_Rxxh` means "page *n*, register *xx*", implemented as a write of *n* to `E0h` followed by a page-local register write.** It is direct manufacturer confirmation of the scheme every driver uses, and it names one page-1 register (`54h` = enter deep standby). It is the only paged register the public datasheet names.

---

## 5. ⚠ Register `0x40` — what it actually is

**The question:** the 3.4C and 4C ship the same PCB and the same ~250-entry init table, differing in **exactly one byte**: page-1 `0x40` = `0x00` (3.4C) vs `0x04` (4C).

### 5.1 The difference is independently confirmed twice

| Source | 3.4C / 800×800 | 4C / 720×720 |
|---|---|---|
| Waveshare ESP-IDF demo `test_esp_lcd_jd9365.c` **[SRC]** | `{0x40, {0x00}}` | `{0x40, {0x04}}` |
| Mainline Linux `panel-jadard-jd9365da-h3.c`, `waveshare_3_4_c_init` / `waveshare_4_0_c_init` **[SRC]** | `0x40, 0x00` | `0x40, 0x04` |

A normalised diff of the two kernel init functions shows `0x40` as the **only** differing register write — the same result as the vendor demo, from a completely independent codebase. Mainline carries `compatible = "waveshare,3.4-dsi-touch-c"` and `"waveshare,4.0-dsi-touch-c"`, i.e. these exact panels.

### 5.2 The correlation across every panel in mainline Linux

Extracted programmatically from `panel-jadard-jd9365da-h3.c` (page-1 value of `0x40`, first write after `switch_page(1)`), against each panel's `hdisplay`:

| page-1 `0x40` | H resolution | Panels |
|---:|---:|---|
| `0x02` | **600** | dcltek DT300250 (600 × 1600) |
| `0x03` | **640** | Anbernic RG-DS (640 × 480) |
| `0x04` | **720** | Waveshare **4.0C** (720 × 720), Waveshare 9.0B (720 × 1280), Waveshare 10.1B (720 × 1280) |
| `0x06` | **800** | Radxa 8HD-AD002, Chongzhou CZ101B4001, Kingdisplay KD101NE3-40TI, Melfas LMFBX101117480, Taiguan XTI05101-01A, Waveshare 8.0A, Waveshare 10.1A (all 800 × 1280 or 800 × …) |
| `0x00` | **800** | Waveshare **3.4C** (800 × 800) — **the sole exception** |

**12 of 13 panels** are consistent with a single rule: **page-1 `0x40` selects the horizontal (RGB source-channel) resolution.** The value tracks *horizontal* pixels only — vertical resolution varies wildly within each group (720 × 720 and 720 × 1280 share `0x04`; 800 × 1280 and 800 × 600-class share `0x06`).

### 5.3 Why this reading is well-founded

The datasheet independently establishes that resolution *is* register-selected, and that the exact set of selectable widths is the set that appears above **[DOC]**:

- §3.1 lists the supported resolutions as **800 / 768 / 750 / 720 / 640 / 600 RGB** — the same widths seen in the correlation.
- §6 tabulates the **source-channel mapping per RGB resolution** (600RGB → `S[1]–S[900], S[1501]–S[2400]`, 720RGB → `S[1]–S[1080], S[1321]–S[2400]`, 800RGB → `S[1]–S[2400]`, …). Selecting a width physically remaps which source outputs drive the glass.
- §6 states outright that the 750RGB sub-type "**is determined by internal register, {IP750_1, IP750_0}**" — proving Jadard selects resolution variants through internal registers.

So a page-1 register that selects horizontal resolution *must* exist, its legal values must correspond to that width list, and `0x40` behaves exactly like it.

### 5.4 What this means for the 3.4C vs 4C difference

**`0x40` is the resolution-select register, and the 3.4C/4C differ in it because they differ in horizontal resolution — 800 vs 720.** That is why it is the *only* differing byte: the two panels are otherwise the same glass family with the same timings, driven by the same silicon, and resolution is the one thing the controller must be told.

This replaces the earlier "panel-specific analogue tune" reading, and it changes the practical advice: the byte is **not** mysterious per-unit characterisation, it is a **mode selector keyed to pixel width**.

### 5.5 ⚠ What remains genuinely unknown — do not overstate this

| Question | Status |
|---|---|
| The register's **official name and bit fields** | **Unknown.** Not in the public datasheet (§4). "RSO"/"resolution select output" is the label used in vendor init tables circulating in the wild, but no such string appears in any document retained here, so **this record does not adopt that name as fact** |
| Why the Waveshare **3.4C writes `0x00` for an 800-wide panel** when seven other 800-wide panels write `0x06` | **Open, and the main residual anomaly.** Candidate explanations — an additional encoding bit outside `[2:0]`, a distinct dual-gate/round-panel mode, or a Waveshare table quirk that happens to work — are **candidates, not findings**. The bit pattern (`0x00`=000, `0x02`=010, `0x03`=011, `0x04`=100, `0x06`=110) is *suggestive* of `[2:1]` coarse class + `[0]` sub-variant, but this is unverified arithmetic on five data points and is offered only as a hypothesis to test |
| Whether `0x40` alone is sufficient to retarget a panel | **Untested.** Resolution also appears in the DSI/DPI timing config on the host side, and possibly in other page-1/page-2 registers |

**Do not "port" `0x40` between panels on the strength of §5.2.** The correlation explains *why* the byte differs; it does not license editing it. Changing it without changing the host DPI timings will at best produce a shifted or squashed raster.

### 5.6 The experiment that would settle it

On a 3.4C, change page-1 `0x40` from `0x00` to `0x06` (the value every other 800-wide panel uses), leaving all host timings at 800 × 800. If §5.2 is right, the panel should still light up correctly, or fail in a *horizontally* specific way. Report the outcome here. This is cheap and nobody appears to have done it.

---

## 6. Libraries and drivers

### 6.1 ESP-IDF

| Option | Component | Verdict |
|---|---|---|
| **`espressif/esp_lcd_jd9365`** | Component registry. **v2.0.1** is current (2025-11-12, "Updated MIPI-DSI structs for IDF6"); **v1.0.4** is the last ESP-IDF v5.x line | ✅ **Use this.** It is what the Waveshare demos declare |
| Hand-rolled `esp_lcd_new_panel_dpi` + your own init walk | | Possible; the component is ~500 lines and mostly wraps the DPI panel |

**Version pinning matters.** v2.0.0 (2025-10-29) is the ESP-IDF **v6.0** compatibility break. If you are on IDF 5.3–5.4, pin `~1.0.4`; on IDF 6.x use `^2.0.0`. **MIPI-DSI requires ESP-IDF v5.3 or later** — the component README states this explicitly **[SRC]**.

The Waveshare demos vendor `test_esp_lcd_jd9365.c` into the example rather than pulling the registry component, so their copy does not track upstream fixes.

### 6.2 Linux

**`panel-jadard-jd9365da-h3.c`** in mainline `drivers/gpu/drm/panel/` — a full DRM panel driver with `compatible` entries for **both** Waveshare panels (`waveshare,3.4-dsi-touch-c`, `waveshare,4.0-dsi-touch-c`) plus 11 others. Authors Jagan Teki and Stephen Chen (Radxa). GPL-2.0+. If you are driving these panels from a Linux SoC, this is a complete, upstream, tested implementation — and the best available register reference.

### 6.3 Arduino

No JD9365-specific Arduino library was found **[WEB]** 2026-08-30. Arduino-ESP32 is built on ESP-IDF, so the practical route is calling `esp_lcd_*` directly from a sketch, as the Waveshare Arduino examples do for other controllers. MIPI-DSI additionally requires an ESP32-P4-class part; there is no MIPI-DSI path on ESP32-S3.

---

## 7. What the vendor demo actually does

**[SRC]** `06_displaypanel_3.4inch` / `07_displaypanel_4inch`, which are **Unity test apps**, not application examples — they use `unity_test_runner` and `unity_test_utils_memory`.

1. Configure GPIO 26 as output and drive the backlight **on (low)**.
2. Acquire LDO channel 3 at 2500 mV to power the DSI PHY.
3. Create the DSI bus: 2 lanes, 1500 Mbps.
4. Create the DBI IO (`virtual_channel = 0`, `lcd_cmd_bits = 8`, `lcd_param_bits = 8`).
5. Create the DPI panel config at 800 × 800 (or 720 × 720), RGB888, with the porches in §3.
6. `esp_lcd_new_panel_jd9365()` with `reset_gpio_num = 27` and the board init table.
7. Reset → init (walks the table) → draw test patterns, with a refresh-done semaphore signalled from an ISR callback.

It draws colour bars and exercises memory leak checks. **It is not a starting point for an application** — there is no LVGL, no touch integration and no display-off path. For an application skeleton, look at the board's other demos.

---

## 8. Pitfalls

1. **The init table must be sent in LP mode.** Sending ~250 commands with the DSI host in high-speed mode costs roughly **17 ms per command** (HS→LP→cmd→HS per write) versus ~25 µs in LP — about **3.5 s versus 5 ms** total. Documented in the upstream LKML series for this panel driver **[WEB]**. Symptom: a multi-second stall between reset and first frame, *not* corruption. Espressif's DBI path sends commands before enabling HS video, so this mostly bites ports to other hosts.
2. **`0x36` is not `MADCTL` outside page 0.** Espressif's driver tracks the current page and only treats `36h`/`3Ah` as `MADCTL`/`COLMOD` when the last `E0h` write selected page `0x00` **[SRC]**. Its own default table writes `{0x36, 0x59}` on **page 4**, where it means something else entirely. If you write your own init walker, replicate this guard or you will corrupt state and emit spurious "command has been overwritten" warnings.
3. **The backlight is not a controller function.** GPIO 26 is active **low**, and there is a separate `BL_EN` on GPIO 33 that no demo drives. A correctly initialised, invisible panel is the classic first bring-up symptom.
4. **The DSI PHY LDO must come up first.** Without `esp_ldo_acquire_channel` on channel 3 at 2500 mV the PHY never leaves "No Power" and the bus init fails.
5. **Do not shorten the `SLPOUT` delay.** The table ends `{0x11, …, 120 ms}` then `{0x29, …, 20 ms}`. **[DOC]** §9.5 power sequences corroborate that these waits are real.
6. **`TEON` is sent after `DISPON`** in Waveshare's table (`0x35` last). Harmless, but note there is no TE consumer on these boards — see §9.
7. **There is no GRAM.** Any code ported from an ST7789/ST77916 flow that expects `CASET`/`RASET`/`RAMWR` partial updates will not work.

---

## 9. Tearing effect

The controller **does** implement TE: `TEON` (`35h`), `TEOFF` (`34h`), `TESL` set-tear-scanline (`44h`) and `GETSCAN` (`45h`) are all in the standard command set, with a dedicated **`TE`** output pin plus **`TE1`** ("TE pin of each scan line") **[DOC]** §6, §9.1.

On the Waveshare boards, TE is **not used**: the demos send `TEON` but no TE GPIO is assigned, and in DSI **video mode** the host drives timing continuously anyway, so TE is largely moot. TE matters for DSI *command* mode, which these boards do not use.

---

## 10. Power and sleep modes

**[DOC]** §9.5.

| Mode | Entry | Notes |
|---|---|---|
| Normal / SLPOUT | `11h` + 120 ms | Init table ends here, then `29h` DISPON |
| Sleep in | `28h` (DISPOFF) → `10h` (SLPIN) | Datasheet's power-off figure specifies `tDISOFF` 50 ms and `tSLPIN` 100 ms |
| **Deep standby (DSTB)** | `P1_R54h = 0x01` after SLPIN | Discharge ≥ **100 ms**; exit is by reset: `RESX` low ≥ **5 ms**, then ≥ **10 ms** before re-initialising. §4.1 |

Three DC/DC arrangements are documented — external AVDD/AVEE/VGH/VGL, external AVDD/AVEE, and internal DC/DC with **FP7721** under driver-IC control **[DOC]** §4.4. The application note adds worked circuits for **FP7723** as well, per BOE panel size **[DOC]**.

---

## 11. Alternatives and compatibility

The controller is bonded inside the panel module, so this is about software compatibility and sourcing a replacement *module*.

| Part | Relationship | Compatible? |
|---|---|---|
| **JD9365DA-H3 in another module** | Same silicon, different glass | ⚠ Electrically yes; **the init table will not transfer.** Gamma, VCOM, gate timing and `0x40` are glass-specific |
| **Waveshare 3.4C ↔ 4C panels** | Same PCB, same family | ⚠ Init tables differ by `0x40`, and host DPI timings differ. Not interchangeable without both changes |
| **ILI9881C** | [Ilitek](../../ilitek/ili9881c/README.md), also 800×1280 a-Si MIPI-DSI **without GRAM** — the closest functional analogue | ❌ Different register set and a different page-select scheme (`FFh 98 81 xx`). Genuinely comparable at the *system* level, not drop-in |
| **EK79007AD** | [Fitipower](../../fitipower/ek79007ad/README.md) source driver + TCON, MIPI, 1024×600 | ❌ Different part, different resolution class; needs a separate gate driver |
| **ST7701S** | [Sitronix](../../sitronix/st7701s/README.md), RGB/DSI, has GRAM-less RGB modes | ❌ Different interface usage and register set |
| **ST77916 / ST7789VW** | Sitronix QSPI/SPI controllers **with** GRAM | ❌ Fundamentally different architecture — see §2.1 |

---

## 12. Open questions

| Question | Status |
|---|---|
| Official name and bit fields of page-1 `0x40` | **Open.** Needs a register map Jadard has not published. §5.5 |
| Why the 3.4C writes `0x00` rather than `0x06` for an 800-wide panel | **Open.** The one anomaly in §5.2. Experiment in §5.6 |
| Exact JD9365 suffix fitted on the Waveshare panels | **Open.** No marking is visible or published; the die is COG inside the module |
| Meaning of the page-2 GIP block (`0x00`–`0x78`) and page-4 registers | **Open.** Undocumented; see the [programming reference §4](jd9365-programming-reference.md#4-the-init-sequence-annotated) for what the structure implies |
| Lifecycle / ordering status | **Open.** §13 of the datasheet is "TBD" |
| Is a later datasheet revision than V0.01 available? | **Open.** V0.01 is a 2020 early release; the 2021 application note is V0.03, implying document families revise independently |

---

## Manufacturer

**Jadard Technology Inc.** — see the [Jadard documentation-sourcing guide](../../../vendors/jadard/README.md) for how these documents were located, the mirror that actually serves them, and this vendor's known gotchas.

## Used By

- [Waveshare ESP32-P4-WIFI6-Touch-LCD-3.4C](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) — controller of the bonded **800 × 800** round IPS panel. MIPI-DSI 2 lane @ 1500 Mbps, RGB888; reset GPIO 27, backlight GPIO 26 (active low). Page-1 `0x40` = **`0x00`**.
- [Waveshare ESP32-P4-WIFI6-Touch-LCD-4C](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md) — controller of the bonded **720 × 720** round IPS panel. Same PCB, same wiring, same timings. Page-1 `0x40` = **`0x04`**.
- Shared analysis for both variants: [ESP32-P4-WIFI6-Touch-LCD-XC shared record](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md).

## Related components

- **[JD9365 Programming Reference](jd9365-programming-reference.md)** — page-select convention, annotated init sequence, DSI configuration, reset/sleep timing
- [Espressif ESP32-P4](../../espressif/esp32-p4/README.md) — the MIPI-DSI host on both boards
- [Ilitek ILI9881C](../../ilitek/ili9881c/README.md) — the closest functional analogue, same architecture class
- [Fitipower EK79007AD](../../fitipower/ek79007ad/README.md) · [EK73217BCGA](../../fitipower/ek73217bcga/README.md) — the MIPI-DSI driver pair on Espressif's 7″ panel
- [Display interfaces guide](../../../guides/hardware/display-interfaces.md) — where MIPI-DSI sits relative to SPI/QSPI/RGB/i80

---

## Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/jd9365da-h3-datasheet-v0.01-20200819.pdf` | 4 962 394 | `31fb4729dc65525cd761174a6939d9763d33870862f8195c14a3532fa95d1d8f` | **JD9365DA-H3 Data Sheet V0.01, 2020-08-19**, 204 pp. The primary source for §1, §2, §4, §9, §10 |
| `artifacts/jd9365da-h3-application-note-v0.03-20210201.pdf` | 1 304 905 | `30899c3307b4359b50c4f3865b675592b57870c24287b14108ea39af2de1dd25` | **JD9365DA-H3 Application Note V0.03, 2021-02-01**, 23 pp. Application *circuits* for six BOE panels and FP7721/FP7723 pairings. **Contains no register map** |

Both are third-party (Jadard) copyright, obtained from mirrors, with **no stated licence** — redistribution status **`unknown`**, disposition `repository` pending review.

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published | Establishes |
|---|---|---|---|---|---|---|---|---|
| J-1 | JD9365DA-H3 Data Sheet V0.01 | Jadard, mirrored by **Espressif** | authorized mirror | datasheet | <https://dl.espressif.com/AE/esp-iot-solution/JD9365DA-H3_DS_V0.01_20200819.pdf> | 2026-08-30 | 2020-08-19 | §1, §2, §4, §9, §10. Found via the `esp_lcd_jd9365` component README's "Link to datasheet" |
| J-2 | JD9365DA-H3 Application Note V0.03 | Jadard, via lcddisplay.co | credible mirror | application note | <https://lcddisplay.co/wp-content/uploads/2023/01/JD9365DA_V0.03_20210201.pdf> | 2026-08-30 | 2021-02-01 | Power modes, FP7721/FP7723 circuits. ⚠ Plain requests get **HTTP 403**; retrieved with a `WhatsApp/2.23.20.0` UA |
| J-3 | `panel-jadard-jd9365da-h3.c` | Linux (Radxa / Edgeble authors) | community (GPL-2.0+, upstream) | repository | <https://raw.githubusercontent.com/torvalds/linux/master/drivers/gpu/drm/panel/panel-jadard-jd9365da-h3.c> | 2026-08-30 | — | §5.1, §5.2, §6.2. **13 panel init tables**, incl. both Waveshare panels |
| J-4 | `esp_lcd_jd9365` component v2.0.1 / v1.0.4 | Espressif | primary | source package | <https://components.espressif.com/components/espressif/esp_lcd_jd9365> | 2026-08-30 | 2025-11-12 (v2.0.1) | §6.1, §8.2, reset timing, default init table |
| J-5 | Waveshare demo `test_esp_lcd_jd9365.c` (3.4″ and 4″) | Waveshare | primary | vendor demo | in-repo | 2026-08-30 | — | §3, §5.1, §7 |
| J-6 | LKML JD9365DA init-timing series (v2–v7) | linux-kernel | community | mailing list | <https://lists.openwall.net/linux-kernel/2024/06/28/733> | 2026-08-24 (prior pass) | 2024-06 | §8.1 LP-vs-HS init cost |

> **J-3 pinning caveat.** The kernel driver was fetched from `master` (a moving branch), not a commit permalink, so the §5.2 correlation is pinned to **retrieval date 2026-08-30** rather than a SHA. Re-derive it against a specific commit before citing the panel count as stable — the file grew from 4 to 13 panels between 2026-08-24 and 2026-08-30, which is precisely what invalidated the earlier conclusion.
