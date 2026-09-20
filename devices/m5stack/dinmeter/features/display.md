# How do I draw on the DinMeter's screen?

**Applies to:** K134 (**ST7789V2**) and K134-V11 (**ST7789P3**) — identical pins, identical
resolution, identical driver path.
**Evidence status:** pin assignments and panel geometry `executed-success` from three
independent sources that agree exactly; code `reported-working` (vendor-published) or
`inferred`. **Last verified:** 2026-09-04.

---

## Hardware path

```
ESP32-S3  SPI2_HOST ──► FPC1 (FPC-0.5-8P) ──► 1.14" IPS 135×240, ST7789V2 (v1.0) / ST7789P3 (v1.1)
   GPIO6 SCLK, GPIO5 MOSI, GPIO7 CS, GPIO4 D/C, GPIO8 RESET     [no MISO — write-only]
   GPIO9 ──► U6 AW35122FDR load switch ──► FPC1 pin 8 ──► backlight LED string
```

Components: [`sitronix/st7789v2`](../../../../components/sitronix/st7789v2/README.md) ·
[`sitronix/st7789p3`](../../../../components/sitronix/st7789p3/README.md) ·
[`awinic/aw35122`](../../../../components/awinic/aw35122/README.md)

## The three numbers that matter

Three independent sources agree, which is why these can be stated flatly:

| Setting | Value | M5Stack's own factory firmware | Espressif's board definition |
|---|---|---|---|
| **GRAM offset** | **x +52, y +40** | `cfg.offset_x = 52; cfg.offset_y = 40;` | *"column +52, row +40"*, applied via the panel gap API |
| **Colour inversion** | **on** (`INVON`, 0x21) | `cfg.invert = true;` | `invert_color: true` — *"ST7789V2 panel on M5Stack needs inversion"* |
| **SPI write clock** | **40 MHz** | `cfg.freq_write = 40000000;` | `pclk_hz: 40000000` |

Sources: `m5stack/M5DinMeter-UserDemo` `src/factory_test/components/ft_disp_lgfx_cfg.hpp`
(commit `d2fdfe44e9baf810f82335faa6f5962e9fc59a44`), and
`espressif/esp-board-manager` `board_devices.yaml` (`2beb9b22b…`).

**Get the offset wrong and the image is displaced and wraps.** It is the single most common
ST7789-on-a-small-panel bug.

## Panel geometry

| Property | Value |
|---|---|
| Physical | 1.14 in IPS |
| Native orientation | **135 wide × 240 tall** (portrait) |
| Controller GRAM | 240 × 320 — the panel is a window inside it |
| Colour | 16 bpp RGB565 |
| Vendor examples' rotation | `setRotation(1)` → **240 × 135 landscape**, which is how the product is used |
| MISO | not wired — you **cannot read** the framebuffer or the controller back |

---

## Arduino — M5DinMeter / M5GFX

```cpp
#include "M5DinMeter.h"
void setup() {
    auto cfg = M5.config();
    DinMeter.begin(cfg, false);            // display comes up inside M5.begin()
    DinMeter.Display.setRotation(1);       // 240x135 landscape
    DinMeter.Display.setBrightness(128);   // 0..255, drives GPIO9 PWM
    DinMeter.Display.setTextColor(GREEN);
    DinMeter.Display.setTextDatum(middle_center);
    DinMeter.Display.setTextFont(&fonts::Orbitron_Light_32);
    DinMeter.Display.drawString("42.0 V",
        DinMeter.Display.width()/2, DinMeter.Display.height()/2);
}
```
Adapted from `M5DinMeter/examples/Basic/display/display.ino` and `button.ino`
(release 1.0.0). `reported-working`.

`DinMeter.Display` is a reference to `M5.Display` (`M5DinMeter.h:20`), i.e. an `M5GFX` — the
full LovyanGFX API: `fillRect`, `drawCircle`, sprites (`M5Canvas`), `pushImage`, `drawPng`,
fonts, `startWrite`/`endWrite` batching.

**Raw LovyanGFX** (no M5Unified) is also viable and is what the factory firmware does — see
`ft_disp_lgfx_cfg.hpp`, which builds a `LGFX_Device` with `Panel_ST7789` + `Bus_SPI` +
`Light_PWM`. Pinned at `lovyan03/LovyanGFX @ 1.1.12`.

## Backlight

| Path | Detail |
|---|---|
| M5GFX | `Display.setBrightness(0..255)` |
| Factory firmware | `Light_PWM`, `pin_bl = 9`, `invert = false`, **`freq = 200`**, `pwm_channel = 7` |
| esp-board-manager | LEDC **channel 0, timer 0, 5 kHz, 10-bit**, `default_percent: 100` |

⚠ **The two vendor-adjacent sources disagree on PWM frequency: 200 Hz vs 5 kHz.** Both work —
200 Hz can be visible as flicker to some people and in video; 5 kHz cannot. Neither is
authoritative over the other. Pick 5 kHz unless you have a reason not to. `not-tested`.

The backlight is *off* at reset: the AW35122FDR's `EN` has an internal ~7.1 MΩ pull-down, so
nothing lights until firmware drives GPIO9. That is why there is no white flash at boot.

## ESP-IDF

`esp_lcd_panel_st7789` is built into ESP-IDF; no extra component is needed (Espressif's board
definition says so explicitly). Bus: `SPI2_HOST`, `max_transfer_sz: 6480` (= 135 × 24 lines ×
2 bytes). Then:

```c
esp_lcd_panel_set_gap(panel, 52, 40);      // ← the offset
esp_lcd_panel_invert_color(panel, true);   // ← INVON
```
`inferred` from the board definition's own comment that *"bmgr's display model has no offset
field; the application applies it via the panel gap API."*

## Resource cost and conflicts

| Resource | Used |
|---|---|
| GPIO | 4, 5, 6, 7, 8 (bus) + 9 (backlight) |
| SPI host | `SPI2_HOST` — the *only* SPI peripheral used on this board, so it is yours alone |
| LEDC | 1 channel + 1 timer for the backlight; the buzzer wants another (ch 1/timer 1) |
| DMA | optional; `max_transfer_sz` 6480 suggests a 24-line band buffer |
| RAM | 135 × 240 × 2 = **64 800 B** for a full framebuffer. **There is no PSRAM**, so a full-screen sprite is ~63 KB of the ESP32-S3's ~512 KB SRAM. Band buffers are the sensible default |

**No conflicts** with the encoder, RTC, buzzer or Grove ports. Display + Wi-Fi + encoder + RTC
simultaneously is fine; the constraint is SRAM, not pins.

## Pitfalls

| Symptom | Cause |
|---|---|
| Image shifted and wrapping | GRAM gap not set to (52, 40) |
| Colours inverted | `INVON` not applied |
| Nothing visible, backlight dark | GPIO9 never driven; `EN` pull-down keeps the switch off |
| Reads return garbage | MISO is not wired — the panel is write-only. Keep your own shadow buffer |
| Tearing on fast updates | no TE line is wired; use sprites/band buffers and `startWrite`/`endWrite` |
| Portrait when you wanted landscape | `setRotation(1)` |

## Unresolved

- **ST7789P3 has no datasheet.** Command-compatibility with ST7789V2 is assumed, not verified.
  See [`components/sitronix/st7789p3`](../../../../components/sitronix/st7789p3/README.md).
- No measured frame rate at 40 MHz for this panel. Nothing was benchmarked. See
  [`../performance.md`](../performance.md).
