# How do I drive the display? — ESP32-P4-WIFI6-Touch-LCD-3.4C

> **3.4 in round IPS, 800 × 800, JD9365 over MIPI-DSI.**
> Evidence status: **vendor documentation + vendor source code. Untested on hardware.**
> Applies to the 3.4C. For the 4C's 720 × 720 panel see
> [the 4C guide](../../esp32-p4-wifi6-touch-lcd-4c/features/display.md).

## Capability summary

The ESP32-P4 drives this panel over a real **MIPI-DSI** link — not parallel RGB, not SPI. Behind
it sit a pixel-processing accelerator (PPA), a 2D DMA engine, and hardware JPEG decode. That is
what makes an 800 × 800 round panel practical on a microcontroller-class part.

## Hardware path

```
ESP32-P4  --MIPI-DSI 2 lane @1500 Mbps-->  JD9365  -->  3.4in 800x800 round IPS
   |                                          ^
   +-- GPIO27 reset --------------------------+
   +-- GPIO26 backlight (ACTIVE LOW)
```

| Resource | Value | Evidence |
|---|---|---|
| Controller | JD9365 | `06_displaypanel_3.4inch/main/test_esp_lcd_jd9365.c` |
| Interface | MIPI-DSI, **2 lanes** | `JD9365_PANEL_BUS_DSI_2CH_CONFIG()` |
| Lane bit rate | **1500 Mbps** | `displays_config.h` `lane_bit_rate` |
| Active area | **800 × 800** | `TEST_LCD_H_RES` / `TEST_LCD_V_RES` |
| Colour depth | 24 bpp | `TEST_LCD_BIT_PER_PIXEL` |
| hsync pw / bp / fp | 20 / 20 / 40 | `video_timing` |
| vsync pw / bp / fp | 4 / 12 / 24 | `video_timing` |
| Reset | **GPIO27** | `TEST_PIN_NUM_LCD_RST`, `displays_config.h` `lcd_rst` |
| Backlight brightness | **GPIO26**, **active low** | `TEST_PIN_NUM_BK_LIGHT`, `TEST_LCD_BK_LIGHT_ON_LEVEL (0)`; schematic `R65` |
| Backlight **enable** | **GPIO33** (`BL_EN`) | Schematic `R61` — **no demo drives this** |

The backlight polarity is the single most common way to think a board is dead. `BK_LIGHT_ON_LEVEL`
is **0**, so driving the pin high turns the backlight *off*. A board that boots and renders
correctly but looks black is usually this, not a DSI fault.

> **Using the BSP? Polarity is handled for you.** `bsp_display_brightness_set(0..100)` is
> intuitive — the BSP sets LEDC `.flags.output_invert = 1`, so the inversion happens in hardware.
> Drive GPIO26 yourself and you must invert. Mixing BSP init with manual GPIO writes gives a
> backlight that behaves backwards. Also note the BSP defaults to **RGB565**, where the standalone
> demos use 24 bpp. See [`bsp-source-findings.md`](../bsp-source-findings.md).

**There are two backlight controls, and the demos use only one.** `BL_EN` on **GPIO33** is a
separate enable line that no shipped demo touches; the demos drive only the PWM on GPIO26. If
`BL_EN` has a default-on bias the demos work regardless — which presumably explains the omission —
but a from-scratch project that configures only GPIO26 may get a dark panel for no visible reason.
The schematic does not resolve the default state, so **drive both**. See
[C12](../gaps-and-conflicts.md#c12--backlight-has-two-controls-and-the-demos-use-only-one).

## ESP-IDF

Component: `espressif/esp_lcd_jd9365` (declared as `"*"` in the demo's `idf_component.yml`).
Pin an explicit version in your own project rather than copying `"*"`.

```yaml
# idf_component.yml
dependencies:
  idf: "^5.0"
  espressif/esp_lcd_jd9365: "*"   # pin this in real projects
```

Sequence, from Waveshare's demo:

```c
#include "esp_lcd_jd9365.h"

esp_lcd_dsi_bus_config_t bus_config = JD9365_PANEL_BUS_DSI_2CH_CONFIG();
esp_lcd_new_dsi_bus(&bus_config, &mipi_dsi_bus);

esp_lcd_dbi_io_config_t dbi_config = JD9365_PANEL_IO_DBI_CONFIG();
esp_lcd_new_panel_io_dbi(mipi_dsi_bus, &dbi_config, &mipi_dbi_io);

// DPI config carries the timing table:
//   .h_size = 800, .v_size = 800,
//   .hsync_back_porch = 20, .hsync_pulse_width = 20, .hsync_front_porch = 40,
//   .vsync_back_porch = 12, .vsync_pulse_width =  4, .vsync_front_porch = 24,
esp_lcd_new_panel_jd9365(mipi_dbi_io, &panel_config, &panel_handle);

esp_lcd_panel_reset(panel_handle);
esp_lcd_panel_init(panel_handle);
esp_lcd_panel_disp_on_off(panel_handle, true);
```

Reference project: `../../esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/demo/ESP-IDF/06_displaypanel_3.4inch/`

**Use 06, not 07.** `07_displaypanel_4inch` is the 720 × 720 sibling.

### The vendor init table

Both variants send a long JD9365 vendor initialisation sequence (roughly 250 register writes:
gamma, gate timing, power). It is reproduced verbatim in both the ESP-IDF demo and
`Arduino/libraries/displays/displays_config.h`.

Between the 3.4C and the 4C, **exactly one byte differs**: register `0x40` is `0x00` here and
`0x04` on the 4C. Everything else in the table is identical. The official per-register datasheet
remains unobtained, so what `0x40` controls is **unnamed** — do not port the table between panels on
the assumption it is cosmetic. However, public sources now document the controller's architecture
(page banking via `0xE0`, command-unlock prologue, comparable panel init tables): see
[`display-controller-jd9365.md`](display-controller-jd9365.md).

## Arduino

Waveshare ship their own board library at
`../../esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/demo/Arduino/libraries/displays/`, on top of
`Arduino_GFX` 1.6.0 and LVGL 9.3.0.

```c
// 3.4C is the library default; this is here for clarity
#define CURRENT_SCREEN SCREEN_3INCH_4_DSI
#include "displays_config.h"
// exposes: display_cfg.width/height, .init_cmds, .lcd_rst, .i2c_sda_pin, ...
```

The library defaults to `SCREEN_3INCH_4_DSI`, so a stock build already targets this board.

> Note the library's `DisplayConfig` carries **both** `rst_pin = -1` and `lcd_rst = 27`. The
> ESP-IDF demos use 27. **Inference:** `rst_pin` is an unused Arduino_GFX-level field and
> `lcd_rst` is the real one. Not verified — if reset misbehaves in Arduino, check which field the
> library actually consumes.

## LVGL

Both major versions ship: `09_lvgl_demo_v8` (LVGL 8) and `10_lvgl_demo_v9` (LVGL 9), plus
`08_lvgl_display_panel`. The Arduino side bundles **LVGL 9.3.0**.

LVGL 8 and 9 are **not source-compatible**. Pick a major version deliberately at project start;
migrating later is a rewrite of UI code, not a version bump.

A round 800 × 800 panel also means LVGL's default rectangular layouts waste corners. Budget design
time for circular layouts — this is a real ergonomic cost of the form factor, not a software
limitation.

## Resource conflicts

| Resource | Shared with | Note |
|---|---|---|
| GPIO26, GPIO27, GPIO33 | Nothing else known | Display-exclusive |
| MIPI-DSI PHY | Nothing else | Dedicated |
| PSRAM bandwidth | Camera, LVGL buffers | 800 × 800 × 3 B ≈ **1.92 MB** per full frame |
| I²C GPIO7/8 | **Touch, ES8311, ES7210** | Not a display pin, but touch shares it — see [`touch.md`](./touch.md) |

The frame-buffer figure matters. A single 24 bpp 800 × 800 buffer is ~1.92 MB; double buffering is
~3.84 MB. The board has 32 MB of PSRAM so capacity is not the constraint — **bandwidth** is,
especially with the camera streaming concurrently. The demo uses `.num_fbs = 1`.

Display + camera + audio + SD running together is **untested and unmeasured**. It is bandwidth-
bound in principle. No throughput number exists in this record because none was measured.

## Limits

| Limit | Value | Kind |
|---|---|---|
| DSI lanes | 2 | Board (FPC wiring) |
| Lane rate | 1500 Mbps | Vendor-configured |
| Active area | 800 × 800 | Panel |
| Colour depth in demo | 24 bpp | Vendor-configured |
| Refresh rate | **Unknown** | Not stated by vendor; not derived here |

Refresh rate is deliberately absent. It could be computed from the pixel clock and porches, but
the demo's `prefer_speed` (80 MHz) and the DPI clock are not unambiguously the same quantity, and
guessing a frame rate would be exactly the kind of invented precision this repository avoids.

## Pitfalls

1. **Backlight is active low**, and there are **two** controls — GPIO26 PWM and GPIO33 enable.
   Black screen != dead board.
2. **Wrong demo.** 06 = 3.4C, 07 = 4C. Running 07 here configures 720 × 720 on an 800 × 800 panel.
3. **Porches are not per-panel.** See [C4](../gaps-and-conflicts.md#c4--dsi-porch-timings-are-not-derived-per-panel).
4. **`"*"` version pins.** The demo's `idf_component.yml` floats `esp_lcd_jd9365`; a future release
   could change behaviour under you.
5. **LVGL 8 vs 9.** Choose once, deliberately.

## Open questions

- What does JD9365 register `0x40` control? Characterised as panel-specific ([C15](../gaps-and-conflicts.md#c15--jd9365-register-0x40-is-panel-specific-and-undocumented)) but no public Fitipower datasheet was found.
- Actual refresh rate at the shipped timings.
- ~~Whether the bundled LVGL 9.3.0 is patched~~ — **resolved: it is stock.** See [C5](../gaps-and-conflicts.md#c5--bundled-third-party-libraries--resolved-2026-08-24).
- Whether `rst_pin` or `lcd_rst` is authoritative in the Arduino library.

## Related

- [4C display guide](../../esp32-p4-wifi6-touch-lcd-4c/features/display.md) — the 720 × 720 sibling
- [Touch](./touch.md) — shares the I²C bus
- [Shared platform record](../../esp32-p4-wifi6-touch-lcd-xc-shared/README.md)
- [Gaps and conflicts](../gaps-and-conflicts.md)
