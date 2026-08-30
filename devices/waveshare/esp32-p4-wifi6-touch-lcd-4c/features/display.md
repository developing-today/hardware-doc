# How do I drive the display? — ESP32-P4-WIFI6-Touch-LCD-4C

> **4 in round IPS, 720 × 720, JD9365 over MIPI-DSI.**
> Evidence status: **vendor documentation + vendor source code. Untested on hardware, and no
> confirmed real unit of this board was located** — see
> [C2](../../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c2--4c-availability--resolved-2026-08-24).

This is the **only** feature guide maintained separately for the 4C, because the display is the
only hardware difference from the 3.4C. Everything else — touch, audio, camera, storage, Wi-Fi —
is identical; use the
[3.4C guides](../../esp32-p4-wifi6-touch-lcd-3.4c/features/README.md).

## The delta in one table

| Parameter | **4C (here)** | 3.4C |
|---|---|---|
| Diagonal | **4.0 in** | 3.4 in |
| Active area | **720 × 720** | 800 × 800 |
| Approx. pixel density | **~255 ppi** *(derived)* | ~333 ppi *(derived)* |
| JD9365 init reg `0x40` | **`0x04`** | `0x00` |
| Controller | JD9365 | same |
| DSI lanes / rate | 2 @ 1500 Mbps | same |
| hsync pw / bp / fp | 20 / 20 / 40 | same |
| vsync pw / bp / fp | 4 / 12 / 24 | same |
| Reset / backlight GPIO | 27 / 26 (active low) | same |
| Full 24 bpp frame buffer | **~1.56 MB** | ~1.92 MB |

Pixel densities are **derived arithmetic** (pixels ÷ diameter), not vendor figures. They exist
because they capture the actual trade-off: the 4C is the **larger, coarser** panel. It shows ~19%
fewer pixels over ~38% more area, so text and fine UI detail will be visibly chunkier. Choose the
4C for viewing distance and physical presence; choose the 3.4C for crispness.

The smaller frame buffer is a modest side benefit — ~1.56 MB versus ~1.92 MB at 24 bpp, roughly
19% less memory and DSI traffic per frame.

## Hardware path

Identical to the 3.4C:

```
ESP32-P4  --MIPI-DSI 2 lane @1500 Mbps-->  JD9365  -->  4in 720x720 round IPS
   |                                          ^
   +-- GPIO27 reset --------------------------+
   +-- GPIO26 backlight (ACTIVE LOW)
```

Backlight is **active low** (`TEST_LCD_BK_LIGHT_ON_LEVEL (0)`). Driving GPIO26 high turns the
backlight off. A board that boots and renders but looks black is usually this.

## ESP-IDF

Reference project:
`../../esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/demo/ESP-IDF/07_displaypanel_4inch/`

**Use 07, not 06.** `06_displaypanel_3.4inch` is the 800 × 800 sibling.

```c
#include "esp_lcd_jd9365.h"

#define TEST_LCD_H_RES (720)
#define TEST_LCD_V_RES (720)

esp_lcd_dsi_bus_config_t bus_config = JD9365_PANEL_BUS_DSI_2CH_CONFIG();
esp_lcd_new_dsi_bus(&bus_config, &mipi_dsi_bus);

esp_lcd_dbi_io_config_t dbi_config = JD9365_PANEL_IO_DBI_CONFIG();
esp_lcd_new_panel_io_dbi(mipi_dsi_bus, &dbi_config, &mipi_dbi_io);

// .video_timing = {
//     .h_size = 720, .v_size = 720,
//     .hsync_back_porch = 20, .hsync_pulse_width = 20, .hsync_front_porch = 40,
//     .vsync_back_porch = 12, .vsync_pulse_width =  4, .vsync_front_porch = 24,
// }
esp_lcd_new_panel_jd9365(mipi_dbi_io, &panel_config, &panel_handle);
```

Component: `espressif/esp_lcd_jd9365`. The demo floats it as `"*"`; pin a version in real projects.

## Arduino — the default is wrong for this board

Waveshare's board library defaults to the **3.4C**:

```c
#define SCREEN_3INCH_4_DSI 1
#define SCREEN_4INCH_DSI   2
#ifndef CURRENT_SCREEN
#define CURRENT_SCREEN SCREEN_3INCH_4_DSI      // <-- default
#endif
```

So you **must** override before including the config, or a stock build silently configures
800 × 800 on a 720 × 720 panel:

```c
#define CURRENT_SCREEN SCREEN_4INCH_DSI
#include "displays_config.h"
```

This is the single most likely 4C-specific mistake. Symptoms would be a shifted, wrapped, or
torn image rather than a blank screen, since the link still trains.

## The `0x40` register

The JD9365 vendor init table is ~250 register writes. Between the two variants **exactly one byte
differs**: register `0x40` is `0x04` here versus `0x00` on the 3.4C. Every other write is
identical.

The official per-register JD9365 datasheet was not obtained in this pass (public aggregation: [`display-controller-jd9365.md`](../../esp32-p4-wifi6-touch-lcd-3.4c/features/display-controller-jd9365.md)), so what `0x40` contols is **unknown** —
plausibly a resolution, gate-line-count, or panel-geometry selector, but that is speculation and
is not recorded as fact. Do **not** port the 3.4C table to this panel assuming the difference is
cosmetic.

## Timing caveat

The porches and 1500 Mbps lane rate are **identical to the 3.4C** despite the lower pixel count,
so this link runs with more slack. It evidently works, but the timings were not derived for this
panel — see
[C4](../../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c4--dsi-porch-timings-are-not-derived-per-panel).
Re-derive rather than scale if you change pixel clock or colour depth.

## Resource conflicts and limits

Identical to the 3.4C apart from buffer size — see the
[3.4C display guide](../../esp32-p4-wifi6-touch-lcd-3.4c/features/display.md#resource-conflicts).
Key points: GPIO26/27 are display-exclusive; the I²C bus on GPIO7/8 is shared by touch and both
audio chips; refresh rate is **not stated by the vendor and is not derived here**.

## Pitfalls

1. **Arduino library defaults to the 3.4C.** Override `CURRENT_SCREEN`.
2. **Wrong ESP-IDF demo.** 07 = 4C, 06 = 3.4C.
3. **Backlight is active low.**
4. **Do not reuse the 3.4C init table** — register `0x40` differs and its meaning is unknown.
5. **No hardware validation exists** for anything in this guide.

## Open questions

- What does register `0x40` control? Panel-specific; no public Fitipower datasheet located.
- Does a real 4C unit exist in the field? No photograph or owner report was located.
- Actual refresh rate.

## Related

- [3.4C display guide](../../esp32-p4-wifi6-touch-lcd-3.4c/features/display.md)
- [All other feature guides (shared with 3.4C)](../../esp32-p4-wifi6-touch-lcd-3.4c/features/README.md)
- [Shared platform record](../../esp32-p4-wifi6-touch-lcd-xc-shared/README.md)
- [Gaps and conflicts](../../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md)
