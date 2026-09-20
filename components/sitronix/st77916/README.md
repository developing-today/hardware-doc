# Sitronix ST77916

- **Category:** TFT LCD display controller / driver IC for round 360 × 360 panels, QSPI or SPI command and pixel transport
- **Research status:** verified against the board schematic, both vendor example trees (Arduino and ESP-IDF), and the ST77916 specification retrieved into `artifacts/`. **The long-standing "ST77916 vs SH8601" conflict is analysed and resolved here** — see §2.
- **Retrieved:** 2026-08-21

The display controller of the 360 × 360 round panel on the [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md). It is bonded inside the panel module; there is no separate reference designator for the IC itself, only the module connector `U5`.

**This page is the primary display-controller record.** The companion page [SH8601 compatibility driver record](../../generic/sh8601-compatibility-driver/README.md) covers the *software* side of the naming conflict and now defers to §2 here for the analysis.

> 📘 **Writing display code?** See **[ST77916 Programming Reference](st77916-programming-reference.md)** — the command set with hex opcodes and parameter formats, the QSPI wire protocol (and why `lcd_cmd_bits = 32`), spec-backed reset/sleep timing, GRAM addressing, TE behaviour, colour formats and power modes, all extracted from `artifacts/st77916-spec-v1.0.pdf` with page citations and reconciled against the shipped driver. **It corrects two things on this page** — RGB888 is *not* supported (§3 below), and the `0x03` read opcode in §7 below is wrong for this part (it is `0x0B`, and reads additionally require dropping the bus to ≤ 6.67 MHz).

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[SCH]** | Read directly off the board schematic PNGs in `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/` |
| **[DOC]** | Stated by Sitronix in `artifacts/st77916-spec-v1.0.pdf`, or by Espressif in its component documentation |
| **[SRC]** | Read out of the vendor example source in the device's `artifacts/demo/` tree |
| **[COM]** | Community evidence — GitHub issue, library, forum. Attributed |
| **[INF]** | Inference. Not established by the above |
| **[WEB]** | Non-manufacturer web source, dated at retrieval |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Sitronix Technology Corp.** (矽創電子) | **[DOC]** |
| Part | `ST77916` | **[WEB]** Waveshare product page; **[DOC]** spec document header |
| Specification | **ST77916 SPEC V1.0** | **[DOC]** `artifacts/st77916-spec-v1.0.pdf`, mirrored by Espressif at `dl.espressif.com/AE/esp-iot-solution/` |
| Resolution on this board | **360 × 360**, round | **[SRC]** `lcd_config.h`; **[SCH]** panel symbol |
| Colour depth used | **RGB565, 16 bpp** | **[SRC]** `LCD_BIT_PER_PIXEL 16` |
| Interface used | **QSPI** — 1 clock + 4 bidirectional data + CS, no D/C pin | **[SCH]** **[SRC]** |
| Reference designator | Panel module connector **`U5`**; the controller die is inside the module | **[SCH]** |
| ⚠ Marking verified? | **No.** The controller is chip-on-glass/COF inside a bonded module. Nothing in the schematic, the wiki or any published photograph names it. §2 | **[INF]** |

---

## 2. ⚠ The ST77916 / SH8601 conflict — analysed and resolved

This is the single most confusing thing about this board, and it has produced a lot of bad advice. Here is the whole picture.

### 2.1 The conflicting claims

| Claim | Source | Label |
|---|---|---|
| The controller is **ST77916** | Waveshare product page and wiki | **[WEB]** |
| The driver is called **`esp_lcd_sh8601`**, the header is `esp_lcd_sh8601.h`, the constructor is `esp_lcd_new_panel_sh8601()`, the log tag is `"sh8601"` | Both the Arduino and the ESP-IDF example trees | **[SRC]** |
| `#define SH8601_ID 0x86` appears in `lcd_bsp.c` | Arduino example | **[SRC]** |

Taken at face value, these look like a contradiction about the silicon.

### 2.2 They are not in contradiction, and here is why

**Finding 1 — `SH8601_ID 0x86` is dead code.** It is `#define`d at the top of `lcd_bsp.c` alongside `#define CO5300_ID 0xff`, and **neither symbol is referenced anywhere in the file** **[SRC]**. Nothing reads the controller's ID register; nothing compares against `0x86`. These are leftovers from whatever Espressif example the file was copied from. **The code does not prove, or even claim, that the fitted controller answers `0x86`.**

**Finding 2 — `esp_lcd_sh8601` is a *transport shim*, not a controller-specific driver.** Read `esp_lcd_sh8601.c` **[SRC]** and there is almost nothing SH8601-specific in it. What it actually does:

- Wraps every command in the **generic QSPI display opcodes** `0x02` (write command), `0x03` (read command), `0x32` (write pixel data), by shifting the 8-bit command into bits 8–15 of a 32-bit word:
  ~~~c
  #define LCD_OPCODE_WRITE_CMD    (0x02ULL)
  #define LCD_OPCODE_WRITE_COLOR  (0x32ULL)
  lcd_cmd &= 0xff; lcd_cmd <<= 8; lcd_cmd |= LCD_OPCODE_WRITE_CMD << 24;
  ~~~
  This `02h`/`32h` framing is the **industry-standard QSPI display convention**, used identically by ST77916, SH8601, CO5300, RM69330, NV3041A and others. It is not a controller signature.
- Sends `MADCTL` (`0x36`) and `COLMOD` (`0x3A`) — **universal MIPI DCS commands**.
- Then walks a **vendor-supplied init table** that the *application* passes in via `sh8601_vendor_config_t.init_cmds`.
- Implements `reset`, `draw_bitmap` (`CASET`/`RASET`/`RAMWR` = `0x2A`/`0x2B`/`0x2C`), `invert_color`, `mirror`, `swap_xy`, `set_gap`, `disp_on_off` — all standard DCS.

There is exactly **one** genuinely SH8601-specific thing in the file: the built-in `vendor_specific_init_default[]` fallback. And the Waveshare example **overrides it**.

**Finding 3 — the init table Waveshare actually sends is unmistakably Sitronix, and unmistakably not SH8601.**

The driver's own SH8601 default **[SRC]** is three commands:

~~~c
static const sh8601_lcd_init_cmd_t vendor_specific_init_default[] = {
    {0x44, (uint8_t []){0x01, 0xD1}, 2, 0},   // Set Tear Scanline
    {0x35, (uint8_t []){0x00},       0, 0},   // Tearing Effect Line ON
    {0x53, (uint8_t []){0x20},       1, 25},  // Write CTRL Display (AMOLED brightness ctrl)
};
~~~

That is an **AMOLED** bring-up: no gamma tables, no gate/source timing, no power-rail setup, because an AMOLED driver handles all of that internally and exposes brightness via `0x51`/`0x53`.

The table Waveshare passes in `lcd_bsp.c` / `main.c` is **~190 commands** and looks like this **[SRC]**:

| Command group | What it is | Whose convention |
|---|---|---|
| `0xF0`, `0xF1`, `0xF2`, `0xF3` with values `0x00`/`0x01`/`0x02`/`0x10`/`0x28` | **Command-set page select** — the driver has multiple register banks and you page between them | **Classic Sitronix ST77xx.** ST7796, ST7789V2 and ST77916 all use `F0`-style page/command-set control |
| `0xB0`–`0xBD` | Panel/frame/display-function control | Sitronix ST77xx |
| `0xC0`–`0xCB` | **Power control**: VRH, VDV, VCOM, source/gate drive levels | Sitronix ST77xx |
| `0xD0`–`0xD2` | Further power control | Sitronix ST77xx |
| **`0xE0` and `0xE1` with 14-byte payloads** | **Positive and negative gamma correction, 14 parameters each** | **This is the Sitronix signature.** ST7789/ST7796/ST77916 gamma tables are exactly 14 bytes |
| `0x60`–`0xBF` in page `0x10` | Gate/source scan timing, per-line waveform tables | Sitronix ST77xx panel-timing bank |
| `0x21` | `INVON` — display inversion on | Universal DCS |
| `0x11` + 120 ms delay | `SLPOUT` — sleep out | Universal DCS |
| `0x29` | `DISPON` — display on | Universal DCS |
| `0x36` = `0x00` or `0x60` | `MADCTL` — rotation | Universal DCS |

**An SH8601 does not have 14-byte `E0`/`E1` gamma tables, does not have `F0` page select, and does not need `C0`–`CB` power control** — because it is an AMOLED driver, and AMOLED panels have no backlight, no VCOM, no gamma-corrected TFT source drivers in the same sense. **[INF]**, but a strong one.

**Finding 4 — the panel has a backlight, so it cannot be an AMOLED.** `LCD_BLK` on S3 **GPIO47** drives an **AO3400A** N-channel MOSFET gate to PWM a backlight **[SCH]**, and the examples ship an `lcd_bl_pwm_bsp` LEDC component to drive it **[SRC]**. **AMOLED panels are emissive and have no backlight.** SH8601 is an AMOLED driver. Therefore **the fitted panel is not an AMOLED and the fitted controller is not an SH8601.** This is the decisive argument and it does not depend on reading any register.

### 2.3 Conclusion

| Question | Answer | Confidence |
|---|---|---|
| Is the fitted controller an SH8601? | **No.** §2.2 Finding 4 is close to dispositive: there is a backlight | **Very high** |
| Is the fitted controller an ST77916? | **Almost certainly.** The marketing says so, the init table is textbook Sitronix, and the resolution and QSPI interface match the ST77916 spec | **High (~90 %)** — the residue is that a *different* Sitronix or Sitronix-alike TFT controller with the same register conventions would also fit the evidence |
| Why is the driver called `sh8601`? | **Because the file was copied.** `esp_lcd_sh8601` is a generic QSPI-DCS panel shim that happens to carry Espressif's SH8601 name and Espressif's 2023 copyright header. Waveshare reused it, swapped in the real panel's init table, and never renamed it | **High** — the code itself is the evidence |
| Does the naming matter functionally? | **No.** All the controller-specific behaviour is in the init table, which is correct for this panel | **High** |

**Neither page was wrong; they were describing different layers.** This page describes the silicon; [the SH8601 record](../../generic/sh8601-compatibility-driver/README.md) describes the software artefact that drives it.

### 2.4 What a developer should actually do

1. **Use `esp_lcd_sh8601` with Waveshare's init table, unmodified.** It works. Do not try to "fix" the naming by swapping in `esp_lcd_st77916`.
2. **Do not substitute an SH8601 datasheet.** If you need a command reference for anything beyond the standard DCS set, use `artifacts/st77916-spec-v1.0.pdf`.
3. **Do not substitute a *different* ST77916 init table either** — including Espressif's own `esp_lcd_st77916` default. Init tables are **panel-specific**, not just controller-specific: gamma, VCOM and gate timing are tuned to the glass. Waveshare's table is the one that was tuned for *this* glass. §5.3.
4. **If you want to settle it empirically**, read the controller ID. §7.
5. **When writing your own docs**, say: *"marketed as ST77916; driven by Espressif's `esp_lcd_sh8601` generic QSPI panel driver with a board-specific init table."* That sentence is true at every layer.

---

## 3. Capabilities and limits

**[DOC]** `artifacts/st77916-spec-v1.0.pdf` is the authority; the summary below is what matters on this board.

| Area | Capability | On this board |
|---|---|---|
| Resolution | Up to 360 × 360 (and lower) | **360 × 360**, round |
| Colour formats | RGB565 (16 bpp) and RGB666 (18 bpp), selected by `COLMOD` (`0x3A`). **No RGB888** — the GRAM is 18 bits deep and 262K colours is the maximum **[DOC]** p.8/p.190 | **RGB565**; the driver writes `COLMOD` = `0x55` for 16 bpp **[SRC]**. Note the hardware-reset default is **RGB666**, so `COLMOD` must always be sent — see [Programming Reference §6](st77916-programming-reference.md#6-colour-formats) |
| Host interfaces | **QSPI**, standard SPI, and (in the full part) RGB / MIPI-DBI options | **QSPI only** is wired **[SCH]** |
| Frame memory | On-chip GRAM sized for the panel | Means the host does **not** need a full framebuffer — LVGL streams partial areas |
| Tearing effect | `TE` output, `0x35` `TEON` / `0x34` `TEOFF`, `0x44` set-scanline | **`LCD_TE` exists at panel connector `U5` pin 23 but is not assigned to any S3 GPIO** in the schematic's alias table **[SCH]** — see §4.2 |
| Rotation / mirroring | `MADCTL` (`0x36`) | `0x00` normal, `0x60` for the 90° option **[SRC]** |
| Inversion | `INVON` (`0x21`) / `INVOFF` (`0x20`) | Init table sends **`0x21` INVON** **[SRC]** |
| Backlight | **Not a controller function** | Separate PWM on GPIO47 via AO3400A **[SCH]** |

### 3.1 Limits worth stating

- **There is no host-side framebuffer.** The S3 does not have 360 × 360 × 2 = 253 KB of internal SRAM to spare. The vendor examples allocate two DMA-capable partial buffers of `360 × 36 × 2` = 25.9 KB each **[SRC]** and stream them.
- **QSPI is command-and-data only.** There is no continuous pixel-clock RGB bus here; every update is an explicit `CASET`/`RASET`/`RAMWR` burst.
- **No D/C pin.** In QSPI mode the command/data distinction is carried in the `02h`/`32h` opcode, which is why `dc_gpio_num` is `-1` and `lcd_cmd_bits` is **32** in the IO config **[SRC]**.
- **The round panel is still addressed as a square.** 360 × 360 with the corners simply not visible. Draw as if square; LVGL handles the rest.

---

## 4. Exact wiring on this board

**[SCH]** + **[SRC]** `lcd_config.h`.

| Signal | ESP32-S3 GPIO | Notes |
|---|---:|---|
| `LCD_QSPI_SCL` | **13** | QSPI clock, on **SPI2_HOST** **[SRC]** |
| `LCD_QSPI_CS` | **14** | Chip select |
| `LCD_QSPI_D0` | **15** | |
| `LCD_QSPI_D1` | **16** | |
| `LCD_QSPI_D2` | **17** | |
| `LCD_QSPI_D3` | **18** | |
| `LCD_RST` | **21** | Panel reset, active low |
| `LCD_BLK` | **47** | **Backlight PWM** → `AO3400A` gate. *Not* a controller pin |
| `LCD_TE` | **— none** | Present at connector `U5` pin 23; **no S3 GPIO assigned** **[SCH]**. §4.2 |
| Panel supply | 3.3 V | |

### 4.1 Clock rate

The IO config macro sets `pclk_hz = 40 MHz` **[SRC]** with `trans_queue_depth = 10`. At 40 MHz × 4 lines = 160 Mbit/s, a full 360 × 360 RGB565 frame (2 073 600 bits) takes ≈ **13 ms**, i.e. a theoretical ceiling around **77 fps** before any LVGL rendering cost. In practice partial redraws mean you rarely pay the full frame.

### 4.2 ⚠ No tearing-effect line

`LCD_TE` reaches the connector but goes nowhere on the MCU side **[SCH]**. Consequences:

- **You cannot synchronise flushes to the panel's vertical blanking.** Fast full-screen animations can tear.
- `esp_lvgl_port`'s `LV_DISPLAY_RENDER_MODE_DIRECT`/`FULL` with VSync is not available; stick to `PARTIAL` mode with the two-buffer scheme the vendor uses.
- The `0x35` `TEON` and `0x44` set-scanline commands are still *sendable*, they just have no listener.
- **[INF]** If tearing bothers you, the mitigation is to keep redraw regions small and to avoid full-screen wipes, not to look for a software VSync.

### 4.3 The `rounder_cb` — a real constraint, easy to miss

`lcd_bsp.c` registers an LVGL `rounder_cb` that snaps every flush area to **even** start coordinates and **odd** end coordinates **[SRC]**:

~~~c
area->x1 = (x1 >> 1) << 1;          // round start down to even
area->y1 = (y1 >> 1) << 1;
area->x2 = ((x2 >> 1) << 1) + 1;    // round end up to odd
area->y2 = ((y2 >> 1) << 1) + 1;
~~~

i.e. **the panel only accepts window coordinates on a 2-pixel grid.** If you write your own flush path and omit this, you will get skewed or shifted output on odd-aligned areas. Keep it.

---

## 5. Initialization: sequence, timing and gotchas

### 5.1 Reset timing

`panel_sh8601_reset()` **[SRC]**: `RST` low → **10 ms** → `RST` high → **150 ms**. If no reset GPIO is configured it falls back to a software `SWRESET` (`0x01`) plus 80 ms. On this board `RST` is wired to GPIO21, so the hardware path is used. **Do not shorten the 150 ms.**

### 5.2 The full bring-up order

From `lcd_lvgl_Init()` **[SRC]**, in order:

1. `spi_bus_initialize(SPI2_HOST, …)` with `SH8601_PANEL_BUS_QSPI_CONFIG(13, 15, 16, 17, 18, 360*360*16/8)` — note `max_transfer_sz` is a **full frame**, 259 200 bytes.
2. `esp_lcd_new_panel_io_spi()` with `SH8601_PANEL_IO_QSPI_CONFIG(14, cb, ctx)` — `dc_gpio_num = -1`, `lcd_cmd_bits = 32`, `lcd_param_bits = 8`, `flags.quad_mode = true`.
3. `esp_lcd_new_panel_sh8601()` with `reset_gpio_num = 21`, `rgb_ele_order = RGB`, `bits_per_pixel = 16`, and `vendor_config.init_cmds` = the board table, `flags.use_qspi_interface = 1`.
4. `esp_lcd_panel_reset()` — §5.1.
5. `esp_lcd_panel_init()` — sends `MADCTL`, `COLMOD`, then the ~190-entry table.
6. **`esp_lcd_panel_disp_on_off(panel, true)` is commented out** in the vendor code, because the init table already ends with `0x29 DISPON`.
7. LVGL init, two 25.9 KB DMA buffers, `esp_timer` tick at 2 ms, LVGL task at priority 2 with a 4 KB stack and a mutex.

### 5.3 ⚠ Init-table gotchas

1. **`MADCTL` is sent twice.** The driver sends `MADCTL` = `0` from `rgb_ele_order`, and then the init table's **last** entry sends `0x36` again. The driver detects this and logs a warning: *"The %02Xh command has been used and will be overwritten by external initialization sequence"* **[SRC]**. Harmless — but it means **the table wins**, so change rotation there, not in `panel_config`.
2. **`COLMOD` is sent by the driver, not the table.** From `bits_per_pixel`. Do not add a `0x3A` entry to the table.
3. **`{0x11, …, 1, 120}` — the 120 ms `SLPOUT` delay is load-bearing.** Sitronix parts need ~120 ms after sleep-out before further commands. Removing it produces intermittent blank or corrupted panels.
4. **Note the data-length quirk on single-byte "no-parameter" commands.** The table writes `{0x11, (uint8_t[]){0x00}, 1, 120}` and `{0x29, (uint8_t[]){0x00}, 1, 0}` — a **1-byte payload for commands that take none**. The extra byte is harmless on these controllers but is technically out of spec. Do not "fix" it without testing. **[SRC]** **[INF]**
5. **Do not substitute another init table.** §2.4 item 3.
6. **`EXAMPLE_Rotate_90` changes two things.** It swaps the `0x36` value to `0x60` **and** changes the touch-coordinate transform in `example_lvgl_touch_cb()` **[SRC]**. If you rotate by hand, do both — see [CST816D §5.2](../../hynitron/cst816d/README.md).
7. **The backlight is separate.** After `esp_lcd_panel_init()` the panel is live but invisible until you drive GPIO47. A "black screen" that is actually a working display is the classic first-bring-up symptom.

---

## 6. Libraries and drivers

### 6.1 ESP-IDF

| Option | Component | Verdict |
|---|---|---|
| **`espressif/esp_lcd_sh8601`** | Component registry. This is what the vendor ESP-IDF example declares: `esp_lcd_sh8601: {version: '*', public: true}` in `main/idf_component.yml` **[SRC]** | ✅ **Use this.** It is what ships and what is tested |
| `espressif/esp_lcd_st77916` | Registry component genuinely named for this controller | ⚠ **Untested on this board.** Its *default* init table is for Espressif's reference panel, not this glass. If you try it, pass Waveshare's table as `vendor_config.init_cmds`. Report results here |
| Hand-rolled `esp_lcd_panel_io_spi` + your own ops | | Possible; you would reimplement `esp_lcd_sh8601.c`, which is only ~350 lines |

The vendor example also pins **`lvgl/lvgl: "8.4.0"`** **[SRC]**. LVGL 9 changed the display and input-device APIs substantially (`lv_disp_drv_t` → `lv_display_t`); the vendor code will not compile against it unmodified.

### 6.2 Arduino

The vendor Arduino example **vendors the driver into the sketch folder** — `esp_lcd_sh8601.c` and `.h` sit next to `08_LVGL_Test.ino` **[SRC]** — and calls the ESP-IDF `esp_lcd_*` APIs directly from Arduino. That works because the Arduino-ESP32 core is built on ESP-IDF. LVGL is bundled at **8.4.0** under `Arduino/libraries/lvgl/` with a board-specific `lv_conf.h`.

Community alternatives, none of which are known-good on this exact panel:

| Library | Note | Label |
|---|---|---|
| **Arduino_GFX** (moononournation) | Has `Arduino_ST77916` and QSPI bus support; widely used for round QSPI panels | **[COM]** — would need this board's init table |
| **LovyanGFX** | Has QSPI support; no ST77916 panel class as of 2026-08-21 | **[COM]** |
| **TFT_eSPI** | **No QSPI support.** Will not work | **[COM]** |

**[WEB]**, all retrieved 2026-08-21.

---

## 7. How to settle the controller identity empirically

The one thing nobody has done. It is cheap.

`esp_lcd_sh8601.c` already defines the read opcode `LCD_OPCODE_READ_CMD (0x03)` **[SRC]** but never uses it, and does not expose a public read. You can issue the read yourself through the panel-IO handle, which `lcd_bsp.c` conveniently caches in `amoled_panel_io_handle`.

⚠ **Two corrections, both established from the spec** — see [Programming Reference §2.4](st77916-programming-reference.md#24--dummy-cycles-and-why-reads-fail-on-this-board):

1. **The opcode is `0x0B` (FASTREAD), not `0x03`.** `0x03` is what the SH8601 shim inherited; the ST77916 QSPI read instruction is `0x0B`, followed by the 24-bit address and then **8 dummy bits** **[DOC]** p.70.
2. **`0x03` aside, the bus is too fast.** `TSCYCR` (read) has a **150 ns minimum → 6.67 MHz**, against the 40 MHz this board runs **[DOC]** p.39. Writes are fine (limit 62.5 MHz); reads are 6× out of spec.

Together these are almost certainly why this has never worked. Corrected sketch:

~~~c
// RDDID (0x04) returns manufacturer id + module/driver version + driver id.
// Drop the SPI clock to <= 6.67 MHz before doing this, then restore it.
// QSPI framing: 0x0B << 24 | cmd << 8.  Expect leading dummy byte(s).
uint8_t id[4] = {0};
esp_lcd_panel_io_rx_param(amoled_panel_io_handle,
                          (0x0BULL << 24) | (0x04ULL << 8),
                          id, sizeof(id));
ESP_LOGI(TAG, "RDDID: %02X %02X %02X %02X", id[0], id[1], id[2], id[3]);

// RDDST (0x09) and RDID1/2/3 (0xDA/0xDB/0xDC) are also worth dumping.
// Note: RDID1-3 live in Command Table 2 and additionally need F4h (SPIOR)
// toggled around the read.  See Programming Reference §2.5.
~~~

**[INF]** — whether this particular panel answers reads over QSPI at all is unverified; some QSPI panels are write-only in practice, and the module may not have the read path bonded out. If it returns all zeros or all `0xFF`, that is the likely reason, not a driver bug.

**A negative result does not falsify §2.3**, because the backlight argument (§2.2 Finding 4) stands independently. But a positive result would close the last 10 %.

**Please record the outcome here if you run it.**

---

## 8. Alternatives and compatibility

The controller is bonded inside the panel module, so this is about software compatibility and about sourcing a replacement *module*.

| Part | Relationship | Compatible? |
|---|---|---|
| **ST77916** in another 360 × 360 module | Same controller, different glass | ⚠ Electrically yes; **the init table will not transfer.** Gamma/VCOM/gate timing are glass-specific |
| **ST7796** | Sitronix sibling, same `F0` page-select and 14-byte gamma conventions | ❌ Different resolution class; not a drop-in |
| **ST7789 / ST7789V2** | Sitronix, very common | ❌ Max 240 × 320; different |
| **SH8601** | Sino Wealth **AMOLED** driver | ❌ **Not this part.** §2.2. Also implies no backlight |
| **CO5300** | Another QSPI AMOLED driver; its ID (`0xff`) is `#define`d and unused in this board's code | ❌ Not this part |
| **RM69330 / RM67162** | Raydium QSPI AMOLED drivers | ❌ AMOLED |
| **NV3041A** | QSPI TFT controller, similar transport | ❌ Different register set |
| **GC9A01** | The other ubiquitous *round* controller | ❌ 240 × 240, SPI not QSPI. Mentioned because "round ESP32 display" searches surface it constantly |

**Anything using the `02h`/`32h` QSPI opcode framing can reuse `esp_lcd_sh8601.c` verbatim with a different init table.** That is the real reason the file gets copied around under the wrong name.

---

## 9. Open questions

| Question | Status |
|---|---|
| What does the controller return from `RDDID` (`0x04`) / `RDID1-3` (`0xDA`–`0xDC`)? | **Open, and answerable.** §7 |
| Does `esp_lcd_st77916` work on this panel with Waveshare's init table? | **Open.** Worth testing; would let the naming be cleaned up |
| Is `LCD_TE` bonded through the module's FPC at all, or only present at the connector symbol? | **Open.** **[SCH]** shows it at `U5` pin 23 with no MCU endpoint |
| Panel module manufacturer and part number | **Open.** See [LCD panel module](../../generic/lcd-panel-module/README.md) |
| Does LVGL 9 work here? | **Open.** Would need the display/indev porting layer rewritten; the driver itself is LVGL-agnostic |

---

## Manufacturer

**Sitronix** — see the [Sitronix documentation-sourcing guide](../../../vendors/sitronix/README.md) for this vendor's document portals, URL patterns, part-numbering conventions, distribution channels and known gotchas.

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — display controller of the bonded 360 × 360 round panel at connector `U5`. QSPI on S3 GPIO13 (CLK), 14 (CS), 15–18 (D0–D3), reset 21, backlight 47. See [Pinouts and buses § Bus inventory](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md).

## Related components

- **[ST77916 Programming Reference](st77916-programming-reference.md)** — companion page on this component: command set, QSPI wire protocol, init/reset/sleep timing, GRAM addressing, TE, colour formats, power modes, and a consolidated spec-vs-driver conflict table
- [SH8601 compatibility driver record](../../generic/sh8601-compatibility-driver/README.md) — the software-naming side of §2
- [1.8-inch 360 × 360 LCD panel module](../../generic/lcd-panel-module/README.md) — the module this controller is bonded into
- [Hynitron CST816D](../../hynitron/cst816d/README.md) — the touch controller in the same module; note the rotation coupling in §5.3
- [AOS AO3400A](../../alpha-and-omega-semiconductor/ao3400a/README.md) — the backlight switch on GPIO47
- [Espressif ESP32-S3R8](../../espressif/esp32-s3r8/README.md) — the QSPI host

---

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| **Sitronix ST77916 Specification V1.0** | https://dl.espressif.com/AE/esp-iot-solution/ST77916_SPEC_V1.0.pdf | 2026-08-21 | `artifacts/st77916-spec-v1.0.pdf` |
| Waveshare product page (the "ST77916" marketing claim) | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/source-snapshots/waveshare-product-31623-2026-08-21.html` |
| Waveshare wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/source-snapshots/waveshare-wiki-current-2026-08-21.html` |
| Official demo archive — `esp_lcd_sh8601.c/.h`, `lcd_bsp.c`, `lcd_config.h`, `main/idf_component.yml` | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` |
| Espressif `esp_lcd_sh8601` component (the driver actually used) | https://components.espressif.com/components/espressif/esp_lcd_sh8601 | 2026-08-21 | – |
| Espressif `esp_lcd_st77916` component (the correctly-named alternative) | https://components.espressif.com/components/espressif/esp_lcd_st77916 | 2026-08-21 | – |
| ESP-IDF LCD driver guide (QSPI framing, `esp_lcd_panel_io_spi`) | https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32s3/api-reference/peripherals/lcd/index.html | 2026-08-21 | – |
| LVGL 8.4 display porting guide | https://docs.lvgl.io/8.4/porting/display.html | 2026-08-21 | – |
| Board schematic archive | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` |
