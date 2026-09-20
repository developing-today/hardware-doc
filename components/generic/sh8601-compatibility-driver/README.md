# SH8601 compatibility driver record

- **Category:** display-driver software artefact / naming-conflict record. **Not a silicon record.**
- **Research status:** the conflict is **resolved**. `esp_lcd_sh8601` is a generic QSPI-DCS panel shim, not evidence of an SH8601 controller; and the board's backlight rules out an AMOLED controller outright.
- **Retrieved:** 2026-08-21

> **📍 The analysis lives in [Sitronix ST77916 §2](../../sitronix/st77916/README.md).** That page is the primary display-controller record and carries the full four-finding argument, the init-table comparison and the confidence table. **This page is the software-layer companion**: what the driver file actually is, where it comes from, what its API looks like, and how to work with it. It exists as a separate record because the *name* `SH8601` appears in this board's source tree and in community discussion, and people search for it.

---

## 1. The one-paragraph answer

Waveshare's LCD examples for the [ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) drive the display through a file called **`esp_lcd_sh8601.c`**, calling **`esp_lcd_new_panel_sh8601()`**, with the log tag `"sh8601"`. **This does not mean the panel contains an SH8601.** `esp_lcd_sh8601` is Espressif's **generic QSPI display transport shim** — it implements the industry-standard `02h`/`32h` QSPI command/pixel framing plus the universal MIPI DCS operations, and then walks whatever **vendor init table the application hands it**. All the controller-specific behaviour lives in that table, and Waveshare's table is textbook Sitronix ST77xx, not AMOLED. The fitted controller is, to high confidence, the **ST77916** that Waveshare markets. Use the driver as shipped; use the [ST77916 spec](../../sitronix/st77916/README.md) as your command reference.

---

## 2. Evidence labelling

| Marker | Meaning |
|---|---|
| **[SRC]** | Read out of the vendor example source in `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/demo/` |
| **[SCH]** | Read off the board schematic PNGs |
| **[DOC]** | Espressif component documentation |
| **[COM]** | Community evidence, attributed |
| **[INF]** | Inference |

---

## 3. What the artefact is

| Property | Value | Evidence |
|---|---|---|
| Upstream name | **`espressif/esp_lcd_sh8601`** on the ESP Component Registry | **[DOC]** |
| Copyright header | `SPDX-FileCopyrightText: 2023 Espressif Systems (Shanghai) CO LTD`, Apache-2.0 | **[SRC]** |
| Size | ~350 lines of `.c`, ~115 lines of `.h` | **[SRC]** |
| How the ESP-IDF example gets it | Declared in `main/idf_component.yml` as `esp_lcd_sh8601: {version: '*', public: true}` — pulled from the registry at build time | **[SRC]** |
| How the Arduino example gets it | **Vendored** — `esp_lcd_sh8601.c` / `.h` are copied into the sketch folder next to `08_LVGL_Test.ino` | **[SRC]** |
| Version logging | The `ESP_LOGI(TAG, "LCD panel create success, version: …")` line using `ESP_LCD_SH8601_VER_MAJOR/MINOR/PATCH` is **commented out** in the vendored copy, so the archive does not record which upstream version it forked | **[SRC]** |
| Named after | Sino Wealth **SH8601**, a QSPI **AMOLED** driver IC | **[COM]** |
| Actually specific to SH8601? | **Barely.** §4 | **[SRC]** |

---

## 4. What is, and is not, SH8601-specific in the file

**[SRC]** from `esp_lcd_sh8601.c`.

### 4.1 Generic — applies to any QSPI DCS panel

~~~c
#define LCD_OPCODE_WRITE_CMD        (0x02ULL)
#define LCD_OPCODE_READ_CMD         (0x03ULL)
#define LCD_OPCODE_WRITE_COLOR      (0x32ULL)

static esp_err_t tx_param(...)  { lcd_cmd &= 0xff; lcd_cmd <<= 8; lcd_cmd |= LCD_OPCODE_WRITE_CMD   << 24; ... }
static esp_err_t tx_color(...)  { lcd_cmd &= 0xff; lcd_cmd <<= 8; lcd_cmd |= LCD_OPCODE_WRITE_COLOR << 24; ... }
~~~

This `02h`/`32h` wrapping is the **de-facto standard QSPI display framing**, shared by ST77916, SH8601, CO5300, RM69330, RM67162, NV3041A and others. It is not a controller signature.

Everything else in the file is standard MIPI DCS:

| Function | Commands used |
|---|---|
| `panel_sh8601_reset` | GPIO reset (10 ms low, 150 ms settle), or `SWRESET` `0x01` + 80 ms |
| `panel_sh8601_init` | `MADCTL` `0x36`, `COLMOD` `0x3A`, then the vendor table |
| `panel_sh8601_draw_bitmap` | `CASET` `0x2A`, `RASET` `0x2B`, `RAMWR` `0x2C` |
| `panel_sh8601_invert_color` | `INVON` `0x21` / `INVOFF` `0x20` |
| `panel_sh8601_mirror`, `_swap_xy` | `MADCTL` bit manipulation |
| `panel_sh8601_disp_on_off` | `DISPON` `0x29` / `DISPOFF` `0x28` |

`COLMOD` is derived from `panel_dev_config->bits_per_pixel`: `0x55` for RGB565, `0x66` for RGB666, `0x77` for RGB888 — again universal.

### 4.2 The only SH8601-specific thing — and this board overrides it

~~~c
static const sh8601_lcd_init_cmd_t vendor_specific_init_default[] = {
    {0x44, (uint8_t []){0x01, 0xD1}, 2, 0},   // Set Tear Scanline
    {0x35, (uint8_t []){0x00},       0, 0},   // TEON
    {0x53, (uint8_t []){0x20},       1, 25},  // Write CTRL Display -- AMOLED brightness control
};
~~~

Three commands. That is an AMOLED bring-up: no gamma, no power control, no gate timing, because an AMOLED driver does that internally and exposes brightness through `0x51`/`0x53`.

**Waveshare passes a ~190-entry Sitronix-style table instead**, so this default is never executed on this board. The comparison is laid out in [ST77916 §2.2](../../sitronix/st77916/README.md).

### 4.3 Dead code that has misled people

`lcd_bsp.c` opens with **[SRC]**:

~~~c
#define SH8601_ID 0x86
#define CO5300_ID 0xff
~~~

**Neither symbol is referenced anywhere in the file.** Nothing reads a controller ID register; nothing compares against `0x86`. These are copy-paste residue. Any claim of the form "the code says the controller ID is `0x86`, therefore it is an SH8601" is reading a `#define` that the program never evaluates.

---

## 5. API surface

**[SRC]** from `esp_lcd_sh8601.h`.

### 5.1 Types

~~~c
typedef struct {
    int          cmd;          // 8-bit LCD command
    const void  *data;         // command payload
    size_t       data_bytes;   // payload length
    unsigned int delay_ms;     // delay AFTER this command
} sh8601_lcd_init_cmd_t;

typedef struct {
    const sh8601_lcd_init_cmd_t *init_cmds;   // your panel's table
    uint16_t                     init_cmds_size;
    struct { unsigned int use_qspi_interface : 1; } flags;
} sh8601_vendor_config_t;

esp_err_t esp_lcd_new_panel_sh8601(const esp_lcd_panel_io_handle_t io,
                                   const esp_lcd_panel_dev_config_t *panel_dev_config,
                                   esp_lcd_panel_handle_t *ret_panel);
~~~

### 5.2 Configuration macros

| Macro | Purpose | Key values on this board |
|---|---|---|
| `SH8601_PANEL_BUS_QSPI_CONFIG(sclk, d0, d1, d2, d3, max_trans_sz)` | `spi_bus_config_t` | `13, 15, 16, 17, 18, 360*360*16/8` |
| `SH8601_PANEL_BUS_SPI_CONFIG(sclk, mosi, max_trans_sz)` | 1-line SPI fallback | unused here |
| `SH8601_PANEL_IO_QSPI_CONFIG(cs, cb, cb_ctx)` | `esp_lcd_panel_io_spi_config_t` | `cs = 14`; **`dc_gpio_num = -1`**, **`lcd_cmd_bits = 32`**, `lcd_param_bits = 8`, `pclk_hz = 40 MHz`, `trans_queue_depth = 10`, `flags.quad_mode = true` |
| `SH8601_PANEL_IO_SPI_CONFIG(cs, dc, cb, cb_ctx)` | 1-line SPI variant | `lcd_cmd_bits = 8` |

`lcd_cmd_bits = 32` and `dc_gpio_num = -1` are the two settings that make QSPI work: the command *is* the 32-bit opcode word, so there is no separate data/command pin.

### 5.3 Minimal usage

~~~c
#include "esp_lcd_sh8601.h"

static const sh8601_lcd_init_cmd_t my_panel_init[] = { /* ~190 entries, panel-specific */ };

const spi_bus_config_t bus = SH8601_PANEL_BUS_QSPI_CONFIG(13, 15, 16, 17, 18, 360*360*2);
ESP_ERROR_CHECK(spi_bus_initialize(SPI2_HOST, &bus, SPI_DMA_CH_AUTO));

esp_lcd_panel_io_handle_t io = NULL;
const esp_lcd_panel_io_spi_config_t io_cfg =
    SH8601_PANEL_IO_QSPI_CONFIG(14, on_color_trans_done, &disp_drv);
ESP_ERROR_CHECK(esp_lcd_new_panel_io_spi((esp_lcd_spi_bus_handle_t)SPI2_HOST, &io_cfg, &io));

sh8601_vendor_config_t vendor = {
    .init_cmds      = my_panel_init,
    .init_cmds_size = sizeof(my_panel_init) / sizeof(my_panel_init[0]),
    .flags = { .use_qspi_interface = 1 },     // MUST be set for QSPI
};
const esp_lcd_panel_dev_config_t dev = {
    .reset_gpio_num = 21,
    .rgb_ele_order  = LCD_RGB_ELEMENT_ORDER_RGB,
    .bits_per_pixel = 16,
    .vendor_config  = &vendor,
};
esp_lcd_panel_handle_t panel = NULL;
ESP_ERROR_CHECK(esp_lcd_new_panel_sh8601(io, &dev, &panel));
ESP_ERROR_CHECK(esp_lcd_panel_reset(panel));
ESP_ERROR_CHECK(esp_lcd_panel_init(panel));
// DISPON is already in the table -- esp_lcd_panel_disp_on_off() is not needed
~~~

---

## 6. Gotchas specific to this driver

1. **Forgetting `flags.use_qspi_interface = 1`.** Without it, `tx_param`/`tx_color` skip the opcode wrapping and the panel sees nonsense. Symptom: a completely dead display with no errors.
2. **The `MADCTL` double-send warning.** The driver sends `MADCTL` from `rgb_ele_order`, then the table sends `0x36` again, and the driver logs *"The 36h command has been used and will be overwritten by external initialization sequence"* **[SRC]**. **This warning is expected on this board and is not a bug.** The table wins — set rotation there.
3. **Same for `COLMOD` (`0x3A`)** if you add one to your table. Don't; use `bits_per_pixel`.
4. **Reset delays are load-bearing.** 10 ms low, **150 ms** after release. Shortening this produces intermittent blank panels.
5. **`max_transfer_sz` must cover your largest flush.** The vendor sets a full frame. If you set it smaller than your LVGL buffer, transfers are silently split or fail.
6. **The driver never reads anything.** `LCD_OPCODE_READ_CMD` is defined and unused; there is no public read helper. To read an ID register you must call `esp_lcd_panel_io_rx_param()` yourself with hand-built framing — see [ST77916 §7](../../sitronix/st77916/README.md).
7. **The `rounder_cb` in `lcd_bsp.c` is not part of this driver but is required.** It snaps flush areas to a 2-pixel grid. See [ST77916 §4.3](../../sitronix/st77916/README.md).
8. **Version macros exist but the log is commented out** in the vendored copy **[SRC]**, so you cannot tell from the archive which upstream release Waveshare forked. If you pull from the registry with `version: '*'`, you get whatever is current — which is a reproducibility hazard. **Pin a version** in your own `idf_component.yml`.

---

## 7. When you should *not* use this driver

| Situation | Use instead |
|---|---|
| You want a correctly-named driver and are willing to test | `espressif/esp_lcd_st77916`, passing Waveshare's init table as `vendor_config.init_cmds`. **Untested on this board — report results** |
| Your panel is a 1-line SPI part | `SH8601_PANEL_BUS_SPI_CONFIG` / `SH8601_PANEL_IO_SPI_CONFIG` with `use_qspi_interface = 0`, or a controller-specific driver |
| You are on Arduino and want a graphics library rather than raw `esp_lcd` | **Arduino_GFX** has `Arduino_ST77916` and QSPI bus support — but you must supply this panel's init table **[COM]** |
| You are on LVGL 9 | The vendor porting layer is LVGL 8.4 **[SRC]**; the driver itself is LVGL-agnostic and can be reused |
| You genuinely have an SH8601 AMOLED | This driver, with its built-in default table — and note **your panel will have no backlight** |

---

## 8. Why the naming keeps propagating

**[INF]**, offered as an explanation rather than a fact. `esp_lcd_sh8601.c` is the smallest, most complete, Apache-2.0-licensed reference implementation of QSPI display transport that Espressif publishes. Any vendor bringing up *any* QSPI panel finds it, copies it, swaps the init table, and ships. The file name survives; the controller does not. The result is a long tail of boards whose source says `sh8601` and whose glass says something else — and a corresponding tail of forum answers confidently telling people their ST77916 panel is an SH8601 AMOLED.

The tell is always the same and always cheap to check: **does the board have a backlight?** If yes, it is not an AMOLED, and it is not an SH8601. This board has one — `LCD_BLK` on GPIO47 driving an AO3400A gate **[SCH]**.

---

## 9. Open questions

| Question | Status |
|---|---|
| Which upstream `esp_lcd_sh8601` version did Waveshare fork? | **Open.** The version log is commented out **[SRC]** |
| Does `esp_lcd_st77916` drive this panel with Waveshare's table? | **Open.** Would let the naming be cleaned up |
| Does the panel answer `RDDID`/`RDID1-3` over QSPI? | **Open.** See [ST77916 §7](../../sitronix/st77916/README.md) |

---

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — the driver used by both the Arduino (`08_LVGL_Test`, vendored) and ESP-IDF (`08_LVGL_Test`, from the registry) LCD examples, on the same QSPI pins as the [ST77916](../../sitronix/st77916/README.md): GPIO13 CLK, 14 CS, 15–18 D0–D3, 21 reset, 47 backlight.

## Related components

- **[Sitronix ST77916](../../sitronix/st77916/README.md) — the primary display-controller record and the home of the conflict analysis**
- [1.8-inch 360 × 360 LCD panel module](../../generic/lcd-panel-module/README.md)
- [AOS AO3400A](../../alpha-and-omega-semiconductor/ao3400a/README.md) — the backlight switch that settles the AMOLED question

---

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Official demo archive — `esp_lcd_sh8601.c/.h`, `lcd_bsp.c`, `main/idf_component.yml` | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` |
| Espressif `esp_lcd_sh8601` component page | https://components.espressif.com/components/espressif/esp_lcd_sh8601 | 2026-08-21 | – |
| Espressif `esp_lcd_st77916` component page | https://components.espressif.com/components/espressif/esp_lcd_st77916 | 2026-08-21 | – |
| ST77916 specification (the command reference you should actually use) | https://dl.espressif.com/AE/esp-iot-solution/ST77916_SPEC_V1.0.pdf | 2026-08-21 | `../../sitronix/st77916/artifacts/st77916-spec-v1.0.pdf` |
| ESP-IDF LCD driver guide (QSPI framing, `esp_lcd_panel_io_spi`) | https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32s3/api-reference/peripherals/lcd/index.html | 2026-08-21 | – |
| Board schematic archive (backlight on GPIO47 → AO3400A) | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` |
