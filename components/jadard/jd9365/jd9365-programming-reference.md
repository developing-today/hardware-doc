# JD9365 Programming Reference

Companion to the [Jadard JD9365 component record](README.md). Everything here is either extracted from `artifacts/jd9365da-h3-datasheet-v0.01-20200819.pdf` with a section reference, or read out of driver source and labelled as such.

**Retrieved 2026-08-30.**

> ⚠ **Read [README §4](README.md#4--what-the-public-datasheet-does-and-does-not-contain) first.** The public datasheet documents the **standard DCS command set only**. The `E0h`-paged manufacturer registers — which is where the entire vendor init table lives — are **not** publicly documented. This page therefore mixes two very different grades of evidence, and marks every claim accordingly.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Jadard datasheet, with section/page reference. Authoritative |
| **[SRC]** | Driver source: Waveshare vendor demo, Espressif `esp_lcd_jd9365` v2.0.1, or mainline Linux `panel-jadard-jd9365da-h3.c` |
| **[INF]** | Inference from structure or correlation. **Not** stated by any source |

---

## 1. Architecture in one paragraph

The JD9365 is a single-chip a-Si TFT driver with **no frame memory**. The host must supply a continuous MIPI-DSI video raster; the chip generates source drive, gate control and all LCD bias rails internally. Configuration is done once at power-up by walking a long list of register writes, addressed through a **paged register file**. Standard MIPI DCS commands (`SLPOUT`, `DISPON`, `MADCTL`, `COLMOD`, `TEON`…) live on **page 0**; everything panel-specific — gamma, power, gate timing, resolution — lives on **pages 1, 2 and 4**.

---

## 2. The page-select convention

### 2.1 The mechanism

Writing register **`E0h`** sets the active page. All subsequent register addresses are **page-local** until the next `E0h` write.

```c
write(0xE0, page);   // select page
write(reg, value);   // reg is now page-local
```

**[DOC]** confirms this notation directly. §9.5.4 specifies the deep-standby control as:

```
P1_R54h=0x01
( REGW RE0h=0x01;
  REGW R54h=0x01; )
```

i.e. `Pn_Rxxh` = page *n*, register *xx*, implemented as a write of *n* to `E0h` then a page-local write. This is the only place the public document uses the notation, and the only paged register it names.

### 2.2 Pages seen in public code

| Page | Contents | Evidence |
|---:|---|---|
| `0x00` | **Standard DCS command set.** `SLPOUT`, `DISPON`, `MADCTL`, `COLMOD`, `TEON`, plus the `E1/E2/E3/80` unlock | **[DOC]** §10 for the DCS set; **[SRC]** for the unlock |
| `0x01` | **Power, VCOM, gate/source levels, gamma tables, resolution select.** The largest block | **[SRC]**; **[DOC]** names only `R54h` (deep standby) |
| `0x02` | **GIP / gate-in-panel scan timing.** Two sub-blocks: `0x00`–`0x57` (per-stage waveform mapping) and `0x58`–`0x78` (GIP control) | **[SRC]** |
| `0x04` | Additional chip control. Espressif's default table writes `0x00, 0x02, 0x09, 0x0E, 0x36` here | **[SRC]** |
| `0x03` | Not used by any public table inspected | **[SRC]** (absence) |

Espressif's driver names page 0 explicitly: `#define JD9365_CMD_PAGE (0xE0)`, `#define JD9365_PAGE_USER (0x00)` **[SRC]**.

### 2.3 ⚠ The page-aware `MADCTL`/`COLMOD` trap

`36h` and `3Ah` are `MADCTL` and `COLMOD` **only on page 0**. On other pages those addresses are unrelated registers.

Espressif's driver gets this right and it is worth copying **[SRC]**:

```c
// after each command is sent:
if ((init_cmds[i].cmd == JD9365_CMD_PAGE) && (init_cmds[i].data_bytes > 0)) {
    is_user_set = (((uint8_t *)init_cmds[i].data)[0] == JD9365_PAGE_USER);
}
// ...and the MADCTL/COLMOD "already used" check only fires when is_user_set
```

The proof that this matters is in Espressif's own default init table, which writes **`{0x36, 0x59}` on page 4** **[SRC]**. Without the guard, a naive walker would parse that as `MADCTL = 0x59`, cache it as the panel's rotation state, and emit a spurious *"The 36h command has been used and will be overwritten"* warning. **If you write your own init walker, replicate the guard.**

---

## 3. The unlock prologue

Every public init table — Waveshare's, Espressif's default, and all 13 in mainline Linux — begins identically **[SRC]**:

```c
{0xE0, {0x00}},   // select page 0
{0xE1, {0x93}},
{0xE2, {0x65}},
{0xE3, {0xF8}},
{0x80, {0x01}},   // Waveshare;  Espressif's default and several kernel tables use 0x03
```

`E1/E2/E3 = 93/65/F8` is a **magic unlock key** enabling access to the manufacturer pages — the same idea as Sitronix's `FFh 77 01` or Ilitek's `FFh 98 81`. It is **[INF]** that this is its function: no retained document describes it, but no table omits it and the manufacturer pages are inaccessible in DCS-only mode.

`0x80` differs between tables (`0x01` on both Waveshare panels, `0x03` in Espressif's default and most kernel tables). **[INF]** it selects lane count or a related interface mode — the Waveshare boards are **2-lane** while most kernel panels are **4-lane**, which fits, but this is a hypothesis, not a finding. Do not change it speculatively.

---

## 4. The init sequence, annotated

Structure of Waveshare's ~250-entry table **[SRC]** (`06_displaypanel_3.4inch/main/test_esp_lcd_jd9365.c`). The 4C table is byte-identical except for one register — see [README §5](README.md#5--register-0x40--what-it-actually-is).

| Order | Page | Registers | What it configures | Evidence |
|---:|---:|---|---|---|
| 1 | `0x00` | `E1 E2 E3 80` | Unlock. §3 | **[SRC]** |
| 2 | `0x01` | `00 01 03 04` | VCOM / initial power | **[INF]** by position |
| 3 | `0x01` | `17–1C` | VGH/VGL and gate-level setup (`18=D0`, `1B=D0`) | **[INF]** |
| 4 | `0x01` | `24 35 37` | Panel control; `37` plausibly SS/GS/BGR-type flags (`0x09` on both Waveshare panels, `0x19` on many 800×1280 panels) | **[INF]** |
| 5 | `0x01` | `38–3F` | Frame/timing tunables (`3C=78`, `3D/3E/3F=FF`) | **[INF]** |
| 6 | `0x01` | **`40`** | **Horizontal resolution select.** `0x00` on 3.4C, `0x04` on 4C — [README §5](README.md#5--register-0x40--what-it-actually-is) | **[INF]**, strongly evidenced |
| 7 | `0x01` | `41–45` | Resolution-adjacent block (`41=0x64` on both Waveshare panels; `0xA0` on the 800×1280 family, `0xC8` on a 600×1600 panel) | **[INF]** |
| 8 | `0x01` | `55 57 59 5A 5B` | Power/charge-pump control | **[INF]** |
| 9 | `0x01` | **`5D–6F`** | **Positive gamma, 19 entries** (`5D=7F` … `6F=0F`) | **[INF]** |
| 10 | `0x01` | **`70–82`** | **Negative gamma, 19 entries** — mirrors the positive table exactly | **[INF]** |
| 11 | `0x02` | `00–57` | **GIP stage mapping.** Values are gate-stage selectors (`0x5F` = unused/dummy, then ascending pairs). Two symmetric halves (`00–2B`, `2C–57`) = the two gate-driver sides | **[INF]** |
| 12 | `0x02` | `58–78` | **GIP control**: clock counts, start pulses, overlap (`5B=30`, `60=30`, `64=A6`, `67=73`, `6F=88`) | **[INF]** |
| 13 | `0x02` | `75–78` | Trailing GIP config (`75=D9`, `77=33`, `78=43`) | **[SRC]** |
| 14 | `0x00` | `11` +120 ms | **`SLPOUT`** | **[DOC]** §10.2.16 |
| 15 | `0x00` | `29` +20 ms | **`DISPON`** | **[DOC]** §10.2.24 |
| 16 | `0x00` | `35` | **`TEON`** | **[DOC]** §10.2.26 |

### 4.1 Notes on the structure

- **Gamma tables are 19 bytes**, not the 14 that Sitronix parts use. If you are pattern-matching init tables to guess a vendor, that is a useful discriminator.
- **The positive and negative gamma blocks are identical in length and shape**, at `5D–6F` and `70–82`.
- **Page 2 is almost half the table.** GIP mapping is the most panel-specific part and the least portable.
- **Note step 16:** Waveshare sends `TEON` *after* `DISPON`. Harmless; see §8.
- Espressif's default table additionally uses **page 4** (`00=0E, 02=B3, 09=60, 0E=2A, 36=59`) which Waveshare's does not **[SRC]**.
- **[INF] warning:** every "what it configures" above for pages 1, 2 and 4 is inferred from position, value patterns and cross-panel comparison. None of it is documented. Treat it as a map for exploration, **not** as a register reference, and do not derive new register values from it.

---

## 5. MIPI-DSI configuration

### 5.1 Silicon capability **[DOC]**

| Property | Value | Source |
|---|---|---|
| DSI version | **1.1** | §3.2 |
| D-PHY version | **1.00** | §3.2 |
| Data lanes | up to **4** (`HS_D0P/N` … `HS_D3P/N`) plus `HS_CP/CN` clock | §4.1 block diagram, §6 |
| Lane count select | pin `LANSEL1X` / register — "Select number for MIPI DSI data lane" | §6 |
| Video modes | non-burst sync pulse, non-burst sync event, **burst** | §7.1.27–7.1.29 |
| Pixel formats | packed 16-bit, packed 18-bit, loosely-packed 18-bit, **packed 24-bit** | §7.1.17–7.1.20 |
| Virtual channels | supported; VC in `DI[7:6]` | §7.1.12 |

### 5.2 As configured on the Waveshare boards **[SRC]**

```c
esp_lcd_dsi_bus_config_t bus_config = JD9365_PANEL_BUS_DSI_2CH_CONFIG();
//  .bus_id = 0, .num_data_lanes = 2, .phy_clk_src = 0, .lane_bit_rate_mbps = 1500

esp_lcd_dbi_io_config_t dbi_config = JD9365_PANEL_IO_DBI_CONFIG();
//  .virtual_channel = 0, .lcd_cmd_bits = 8, .lcd_param_bits = 8
```

| Parameter | 3.4C | 4C |
|---|---|---|
| Active | 800 × 800 | 720 × 720 |
| H front / sync / back porch | 40 / 20 / 20 | **identical** |
| V front / sync / back porch | 24 / 4 / 12 | **identical** |
| Lanes / lane rate | 2 / 1500 Mbps | **identical** |
| Pixel format | RGB888 (24 bpp) | **identical** |

The DPI pixel clock follows Espressif's documented relation **[SRC]**:

```
refresh_rate = (dpi_clock_freq_mhz * 1e6)
             / (h_res + hsync_pulse_width + hsync_back_porch + hsync_front_porch)
             / (v_res + vsync_pulse_width + vsync_back_porch + vsync_front_porch)
```

Mainline Linux encodes the same timings as a DRM mode **[SRC]**, e.g. for the 3.4C:

```c
.clock = (800 + 40 + 20 + 20) * (800 + 24 + 4 + 12) * 60 / 1000,   /* 60 Hz */
.hdisplay = 800, .hsync_start = 840, .hsync_end = 860, .htotal = 880,
.vdisplay = 800, .vsync_start = 824, .vsync_end = 828, .vtotal = 840,
.width_mm = 88, .height_mm = 88,
```

with mode flags `MIPI_DSI_MODE_VIDEO | MIPI_DSI_MODE_VIDEO_HSE | MIPI_DSI_MODE_LPM | MIPI_DSI_CLOCK_NON_CONTINUOUS` and `MIPI_DSI_FMT_RGB888`. **`MIPI_DSI_MODE_LPM` is significant** — it is what forces init commands into low-power mode; see §9.

### 5.3 The PHY power rail

On ESP32-P4 the DSI PHY needs an LDO before it will leave the "No Power" state **[SRC]**:

```c
esp_ldo_channel_config_t ldo_cfg = { .chan_id = 3, .voltage_mv = 2500 };
esp_ldo_acquire_channel(&ldo_cfg, &ldo_mipi_phy);
```

Omitting this is a common first-bring-up failure; bus creation fails rather than the display simply staying dark.

---

## 6. Reset timing

### 6.1 As implemented by `esp_lcd_jd9365` **[SRC]**

```c
gpio_set_level(rst, !reset_level);  vTaskDelay(5   ms);
gpio_set_level(rst,  reset_level);  vTaskDelay(10  ms);   // asserted
gpio_set_level(rst, !reset_level);  vTaskDelay(120 ms);   // released, settle
```

With no reset GPIO it falls back to DCS `SWRESET` (`01h`) plus 120 ms. On the Waveshare boards `RST` is GPIO 27, so the hardware path runs.

### 6.2 As implemented by mainline Linux **[SRC]**

`jadard_prepare()` uses a longer sequence: VCCIO/VDD enable → optional LP11 hold → reset low 5 ms → high 10 ms → low 130 ms, with per-panel tunables (`lp11_before_reset`, `vcioo_to_lp11_delay_ms`, `lp11_to_reset_delay_ms`, …).

**The two differ**, and the difference is real: the kernel driver carries per-panel delay overrides because some panels need LP11 on the bus *before* reset is released. Espressif's fixed sequence works on the Waveshare panels but is not universal. **[SRC]**

### 6.3 Datasheet timings **[DOC]** §9.5.4

| Symbol | Parameter | Min |
|---|---|---:|
| `t_discharge` | Sleep-in → deep standby | **100 ms** |
| `t_rstlow` | Reset low pulse | **5 ms** |
| `t_initial` | Reset high → initial setting | **10 ms** |

Notes in the document add "t_discharge suggested delay time over 100 ms" and "t_initial suggested delay time over 10 ms".

---

## 7. Standard command set

**[DOC]** §10.2 — the complete list the datasheet documents, all on page 0.

| Cmd | Name | Cmd | Name |
|---|---|---|---|
| `00h` | NOP | `35h` | **TEON** — tearing effect line on |
| `01h` | SWRESET | `36h` | **MADCTL** — memory access control |
| `04h` | RDDIDIF — read display ID | `38h` / `39h` | IDMOFF / IDMON — idle mode |
| `05h` | RDNUMPE — parity error count | `3Ah` | **COLMOD** — interface pixel format |
| `06h`/`07h`/`08h` | Read red / green / blue | `3Ch` | Write memory continue |
| `09h` | RDDST — display status | `3Eh` | RAMRDCON — read memory continue |
| `0Ah` | RDDPM — power mode | `44h` | **TESL** — set tear scanline |
| `0Bh` | RDDMATCDL — read MADCTL | `45h` | GETSCAN — current scanline |
| `0Ch` | RDDCOLMOD — read COLMOD | `51h` / `52h` | WRDISBV / RDDISBV — brightness |
| `0Dh` | Read display image mode | `53h` / `54h` | WRCTRLD / RDCTRLD — CTRL display |
| `0Eh` | RDDSM — signal mode | `55h` / `56h` | WRCABC / RDCABC |
| `0Fh` | RDDSDR — self-diagnostic result | `5Eh` / `5Fh` | WRCABCMB / RDCABCMB — CABC min brightness |
| `10h` | **SLPIN** | `A1h` / `A8h` | RDDDB — read DDB start / continue |
| `11h` | **SLPOUT** | `AAh` / `AFh` | RDFCS / RDCCS — checksums |
| `13h` | NORON — normal mode | `DAh`/`DBh`/`DCh` | **RDID1 / RDID2 / RDID3** |
| `20h` / `21h` | INVOFF / INVON | | |
| `22h` / `23h` | ALLPOFF / ALLPON — all pixels off/on | | |
| `26h` | GAMSET — gamma set | | |
| `28h` / `29h` | **DISPOFF / DISPON** | | |
| `34h` | TEOFF | | |

`22h ALLPOFF` / `23h ALLPON` are handy bring-up diagnostics: if `ALLPON` whitens the panel, the DSI link, power rails and gate/source drive are all working and any fault is in your raster.

### 7.1 Reading the controller ID

`RDID1`/`RDID2`/`RDID3` (`DAh`–`DCh`) and `RDDIDIF` (`04h`) are documented **[DOC]** §10.2.3, §10.2.47–49. Nothing in the Waveshare demos reads them. Since the fitted suffix is unconfirmed ([README §1](README.md#1-identity)), dumping these over the DBI path would be a cheap way to learn something real. **[INF]** — untested here, and DSI read transactions need the bus in a state that supports peripheral-to-processor transmission (**[DOC]** §7.1.21).

---

## 8. Tearing effect

**[DOC]** §9.1 documents TE line modes and timing; §6 documents two output pins:

| Pin | Function |
|---|---|
| `TE` | Tearing effect output, MPU interface |
| `TE1` | TE "of each scan line" |

Commands: `TEON` (`35h`), `TEOFF` (`34h`), `TESL` (`44h`, set scanline), `GETSCAN` (`45h`).

**On these boards TE is inert.** The init table sends `TEON`, but no TE signal is routed to an ESP32-P4 GPIO and nothing consumes it **[SRC]**. That is not a defect: in DSI **video mode** the host drives the raster continuously and owns the timing, so TE is a command-mode concept. Since the JD9365 has no GRAM it cannot do meaningful command-mode operation anyway.

---

## 9. ⚠ Init commands must go out in LP mode

The most expensive mistake available on this part.

Sending the ~250-entry table with the DSI host in **high-speed** mode costs roughly **17 ms per command**, because each write incurs an HS→LP→command→HS transition. In **low-power** mode each write costs about **25 µs**.

| Mode | Per command | ~250 commands |
|---|---:|---:|
| HS | ~17 ms | **~3.5 s** |
| LP | ~25 µs | **~5 ms** |

Documented in the upstream LKML series for this panel driver (v2–v7, Jun–Jul 2024), and why mainline sets `MIPI_DSI_MODE_LPM` **[SRC]**.

**Symptom if you hit it:** a multi-second stall between panel reset and first frame — *not* corruption, which makes it easy to misdiagnose as a slow boot. Espressif's DBI path sends commands before enabling HS video, so ESP32-P4 users are not normally affected; this bites ports to hosts that come up in HS.

---

## 10. Colour formats

**[DOC]** §3.1 and §7.1.17–7.1.20.

| Format | Bits | DSI packing | `COLMOD` value in `esp_lcd_jd9365` |
|---|---:|---|---|
| RGB565 | 16 | Packed pixel stream, 16-bit | `0x55` |
| RGB666 | 18 | Packed **or** loosely-packed 18-bit | `0x66` |
| **RGB888** | 24 | Packed pixel stream, 24-bit | `0x77` |
| Idle mode | 3 | 8 colours, via `39h IDMON` | — |

Both Waveshare boards use **RGB888** **[SRC]**. The driver derives `COLMOD` from `bits_per_pixel` and rejects anything other than 16/18/24 **[SRC]**.

Note the cost: at 800 × 800 × 24 bpp a single frame is **1.92 MB**, which must live in PSRAM on ESP32-P4 and be streamed continuously — there is no GRAM to fall back on.

---

## 11. Power and sleep modes

**[DOC]** §9.5, §4.4.

### 11.1 Sequences

| Transition | Steps | Timings |
|---|---|---|
| Power on | Rails → reset → init table → `SLPOUT` → `DISPON` | `t_rstlow` ≥ 5 ms, `t_initial` ≥ 10 ms, `SLPOUT` +120 ms |
| Power off | `DISPOFF` (`28h`) → `SLPIN` (`10h`) → rails down | `tDISOFF` 50 ms, `tSLPIN` 100 ms, `tCMD_OFF` ≥ 1 ms, `tMIPIOFF2` ≥ 0 ms |
| **Deep standby** | `SLPIN`, then `P1_R54h = 0x01` | `t_discharge` ≥ 100 ms. Exit **only** by hardware reset |
| Uncontrolled power off | GAS circuit discharges the panel | Display must blank within **1 s** (§9.6) |

### 11.2 DC/DC arrangements

Three are documented **[DOC]** §4.4, selected by `BOOSTM`:

| Mode | `BOOSTM` | AVDD/AVEE | VCI / VCIP range |
|---|---|---|---|
| External power mode 1 | `00` | External AVDD/AVEE **and** VGH/VGL | 2.5–6.0 V |
| External power mode 2 | `01` | External AVDD/AVEE only | 2.5–6.0 V |
| Internal DC/DC (mode 4) | `10` | Internal, **with FP7721** under driver-IC control | 2.5–4.8 V |

The application note adds worked circuits pairing the JD9365DA-H3 with **FP7721** and **FP7723** for six BOE panels (10.1″, 8.9″ QV089WXQ-N80-3QP0, 8″ TV080WXQ-N86, 10.5″ TT105WXB-NW0, 6.95″ TV070WSU-N40, LTPS 10.1″ TS101WXQ-NW0) **[DOC]**. **Which arrangement the Waveshare modules use is unknown** — the module is a sealed COG assembly and Waveshare publishes no panel-side schematic.

---

## 12. Conflicts and unknowns

| Item | Status |
|---|---|
| Reset sequence: Espressif 5/10/120 ms vs Linux 5/10/130 ms + LP11 handling | **Both work on their targets.** Not a contradiction — Linux carries per-panel overrides Espressif's fixed path lacks. §6 |
| `0x80` = `0x01` (Waveshare, 2-lane) vs `0x03` (most others, 4-lane) | **Unexplained.** Lane-count hypothesis in §3 is **[INF]** only |
| Page-1 `0x40` on the 3.4C (`0x00` for an 800-wide panel) | **Open anomaly.** [README §5.5](README.md#55--what-remains-genuinely-unknown--do-not-overstate-this) |
| Meaning of any page-1/2/4 register other than `P1_R54h` | **Undocumented in public.** §4.1 |
| Whether these panels answer `RDID1-3` | **Untested.** §7.1 |
| Fitted JD9365 suffix | **Unconfirmed.** COG die inside a sealed module |

---

## Related

- [Jadard JD9365 component record](README.md) — identity, capabilities, wiring, drivers, register `0x40` analysis
- [Jadard vendor sourcing guide](../../../vendors/jadard/README.md) — where these documents live and how to get them
- [Display interfaces guide](../../../guides/hardware/display-interfaces.md) — MIPI-DSI in context
- [Waveshare 3.4C](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) · [4C](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md) · [XC shared record](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md)
