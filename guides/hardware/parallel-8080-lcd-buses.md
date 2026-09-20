# Parallel Intel-8080 LCD buses on ESP32 — and why your display library matters more than your board

> Device-independent guide. Written 2026-09-07 while documenting the
> [LilyGO T-Display-S3 family](../../devices/lilygo/t-display-s3-shared/README.md), which
> contains boards using **all three** of the buses compared here, and is therefore an unusually
> good worked example.
>
> Companion to [`display-interfaces.md`](display-interfaces.md), which covers the interface
> landscape generally (SPI, QSPI, RGB/parallel, MIPI-DSI, e-paper). **This page is narrower:**
> it is about the *software* consequences of picking a bus, and specifically about the
> `TFT_eSPI` / `Arduino_GFX` / `LovyanGFX` decision that trips people up.

## 1. The three buses, and what each costs you in software

"Parallel" is ambiguous in this space and the ambiguity causes real errors. Three distinct
things get called it:

| Bus | Also called | Wires (typical) | What the controller receives | ESP32 peripheral used |
|---|---|---|---|---|
| **Intel 8080 (i80), 8-bit** | MCU parallel, DBI Type B, "8080-8" | `D0..D7`, `WR`, `RD`, `DC`, `CS`, `RST` = 13 | commands **and** pixels, byte at a time, strobed by `WR` | ESP32-S3 **LCD_CAM** peripheral, or bit-banged GPIO |
| **RGB parallel** | DPI, "RGB666/565" | `R0..5,G0..5,B0..5`, `PCLK`, `HSYNC`, `VSYNC`, `DE` ≈ 22 | a **continuous video signal**; there is no GRAM in the controller | ESP32-S3 LCD_CAM in RGB mode + PSRAM framebuffer |
| **QSPI (DSPI/QSPI DBI)** | "4-line SPI", quad-SPI display | `CS`, `CLK`, `D0..D3` = 6 | commands and pixels in a `0x02`/`0x32`-framed protocol | generic SPI peripheral in quad mode |

The T-Display-S3 family uses the **first and third**, plus plain 4-wire SPI on the Pro. It uses
no RGB-parallel panel at all. If you take away one thing: **8080 and RGB are not the same
thing, and a library that supports one may not support the other.**

## 2. Why 8080 is fast, and why that is not free

An ST7789V on an 8-bit 8080 bus moves one byte per `WR` strobe, so an RGB565 pixel takes two
strobes. At LilyGO's chosen 16 MHz pixel clock that is nominally ~8 M pixel/s — a 170 × 320
full-screen redraw in roughly 7 ms of bus time, against ~35 ms for the same panel on a 40 MHz
1-bit SPI link. That gap is the entire reason to accept a 13-wire bus.

What it costs:

- **Thirteen GPIOs.** On a board whose SoC already loses GPIO26–37 to in-package octal PSRAM,
  that is most of the pin budget. This is why the T-Display-S3 has so few free pins for a
  45-GPIO part.
- **No read-back in practice.** `RD` is wired but essentially unused; most drivers never read
  the controller.
- **A hard dependency on the ESP32-S3's LCD_CAM peripheral** for the fast path. On plain
  ESP32 (no LCD_CAM) an 8080 bus must be bit-banged, which is why 8-bit parallel boards are an
  S3-era phenomenon.
- **Pixel-clock sensitivity.** LilyGO's own header carries the comment
  *"Too low or too high pixel clock may cause screen mosaic"* beside
  `#define EXAMPLE_LCD_PIXEL_CLOCK_HZ (16 * 1000 * 1000)`. ESPHome independently chose
  **10 MHz** for the same board. Neither is wrong; the panel FPC and the bonded flex set the
  real limit, and it varies between production runs of nominally identical boards.

## 3. The library decision

This is the part that costs people evenings.

| Library | 8080 8-bit | QSPI | 4-wire SPI | RGB | Configured by |
|---|---|---|---|---|---|
| **`TFT_eSPI`** (Bodmer) | **yes**, via `TFT_PARALLEL_8_BIT` | **no** | yes | no | editing a header **inside the installed library** |
| **`Arduino_GFX`** (moononournation) | **yes**, `Arduino_ESP32LCD8` | **yes**, `Arduino_ESP32QSPI` | yes | yes | constructor arguments in your sketch |
| **`LovyanGFX`** (lovyan03) | **yes** | yes | yes | yes | a C++ config class in your sketch |
| **ESP-IDF `esp_lcd`** | **yes**, `esp_lcd_new_panel_io_i80()` | yes | yes | yes | struct initialisers |
| **ESPHome `mipi_spi`** | **yes** (`bus_mode: octal`) | yes (`quad`) | yes | — | YAML, with a named board model |

### `TFT_eSPI`: fast, ubiquitous, and configured in the worst possible place

`TFT_eSPI` does not take pin assignments as constructor arguments. It reads them from
`User_Setup.h` / `User_Setups/SetupNNN_*.h`, selected by editing
**`User_Setup_Select.h` inside the library installation directory**. That single design
decision produces a specific, extremely repetitive failure:

> **Symptom:** the sketch compiles and uploads, and the screen stays black — or shows garbage,
> or half a screen of noise.
> **Cause:** the library was updated (or reinstalled, or the IDE did it for you) and your edit
> to `User_Setup_Select.h` was overwritten.

For the LilyGO T-Display-S3 the required edit is:

```c
// TFT_eSPI/User_Setup_Select.h
//#include <User_Setup.h>                                   // <- comment this out
#include <User_Setups/Setup206_LilyGo_T_Display_S3.h>        // <- uncomment this
```

Newer `TFT_eSPI` refuses to build silently and emits
`#error "Error! Please make sure <User_Setups/Setup206_LilyGo_T_Display_S3.h> is selected in <TFT_eSPI/User_Setup_Select.h>"`
— which is an improvement, and is exactly what
[LilyGO issue #326](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/326) (2026-02-23,
11 comments) is about.

Two further `TFT_eSPI` facts worth knowing before you choose it:

- **It has no QSPI transport at all.** On the AMOLED boards, LilyGO's "TFT_eSPI examples" are
  really `TFT_eSPI` **Sprites** (off-screen buffers) that a vendor QSPI routine pushes to the
  panel. You get TFT_eSPI's drawing API and none of its display driver. Do not expect
  `tft.init()` to talk to an RM67162.
- **It is version-coupled to the Arduino core.** LilyGO's README, dated 2024-08-02: *"As of
  2024/08/02, TFT_eSPI does not work on versions higher than 2.0.14"*, citing
  [TFT_eSPI#3329](https://github.com/Bodmer/TFT_eSPI/issues/3329).

**The diagnostic that separates hardware faults from configuration faults**, and LilyGO's own
recommended first move: run an `Arduino_GFX` example. It needs no library-internal
configuration, so if `Arduino_GFX` draws and `TFT_eSPI` does not, the board is fine and
`User_Setup_Select.h` is not.

### `Arduino_GFX`: configuration lives in your sketch

```cpp
// 8-bit 8080, LilyGO T-Display-S3 pin assignment
Arduino_DataBus *bus = new Arduino_ESP32LCD8(
    7 /* DC */, 6 /* CS */, 8 /* WR */, 9 /* RD */,
    39, 40, 41, 42, 45, 46, 47, 48 /* D0..D7 */);
Arduino_GFX *gfx = new Arduino_ST7789(bus, 5 /* RST */, 0 /* rotation */,
                                      true /* IPS */, 170, 320, 35, 0, 35, 0);
```

The two trailing `35`s are the **column offset** into the ST7789's 240-wide GRAM. A 170-pixel
panel on a 240-wide controller must be offset, or the image sits 35 columns to the left with a
band of garbage. `TFT_eSPI` does the same thing through `#define CGRAM_OFFSET`; ESPHome calls
it `offset_width: 35`. **Three libraries, three names, one hardware fact** — and the single
most common "half the display shows garbage" cause
([LilyGO issue #128](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/128)).

Because everything is a constructor argument, `Arduino_GFX` survives library updates. Its
drawing API is smaller than `TFT_eSPI`'s and its font handling is less pleasant; that is the
trade.

### `LovyanGFX`: the compromise

Config lives in your project as a `lgfx::LGFX_Device` subclass, so it survives updates, and it
supports every bus here including QSPI and RGB. It has `TFT_eSPI`-compatible API shims. It is
the right default for a project that must run on more than one of these boards. The cost is a
noticeably steeper first hour — you write ~40 lines of config class before you draw a pixel.

### ESPHome: none of the above, and it already knows your board

Since the `mipi_spi` component landed, ESPHome carries **named models** with pins and offsets
baked in. From `esphome/components/mipi_spi/models/lilygo.py` (`dev`, fetched 2026-09-07):

```python
ST7789V.extend(
    "T-DISPLAY-S3",
    height=320, width=170,
    offset_width=35,
    color_order=MODE_BGR, invert_colors=True,
    dc_pin=7, cs_pin=6, reset_pin=5,
    enable_pin=[9, 15],
    data_rate="10MHz",
    bus_mode=TYPE_OCTAL,
    requires={"psram"},
)
```

Note `enable_pin=[9, 15]` — ESPHome drives both `LCD_RD` **and the board's GPIO15 power gate**
as enables. That is the kind of board-specific knowledge a named model buys you, and the reason
ESPHome "just works" on this board where a hand-written `st7789v:` block usually does not.

## 4. Recommendation by bus

| You have | Use | Second choice | Avoid |
|---|---|---|---|
| 8-bit 8080 (T-Display-S3, T-Display-S3 Touch) | **`TFT_eSPI` + `Setup206`** if you want the richest 2D API and are on core ≤ 2.0.14 | **`Arduino_GFX`** if you are on core 3.x, or want config in your sketch | hand-rolled `esp_lcd` unless you need DMA control |
| QSPI AMOLED (all T-Display-S3 AMOLED, T4-S3, Lite) | **LilyGO's `LilyGo-AMOLED-Series`** — it wraps the panel init tables you would otherwise have to transcribe from the RM67162/RM690B0 datasheets | `Arduino_GFX` `Arduino_ESP32QSPI` | `TFT_eSPI` as a *driver* — it cannot do it |
| QSPI with integrated touch (T-Display-S3 Long, AXS15231B) | `Arduino_GFX` + the vendor's AXS15231B init | LovyanGFX | anything that assumes a separate touch chip |
| 4-wire SPI (T-Display-S3 Pro, ST7796S) | `Arduino_GFX` (LilyGO's choice) | `TFT_eSPI` | — |
| Any of the above, in Home Assistant | **ESPHome `mipi_spi` with the named model** | — | writing pins by hand |
| One codebase across several of them | **LovyanGFX** | ESP-IDF `esp_lcd` | `TFT_eSPI` |

## 5. Debugging checklist for a black screen on an 8080 board

In the order that resolves the most cases first:

1. **Is the panel powered?** Many boards gate the panel rail behind a GPIO — GPIO15 on the
   T-Display-S3. A backlight that is on proves the *backlight* rail, not the panel rail.
2. **Is the backlight on?** Separate pin (GPIO38 here), separate driver chip.
3. **Run an `Arduino_GFX` example.** If it works, your problem is `User_Setup_Select.h`.
4. **Check the column/row offset** if you get an image but it is shifted or has a garbage band.
5. **Halve the pixel clock.** Mosaic, tearing and speckle on an otherwise-correct image is
   almost always the bus running faster than the flex will carry.
6. **Check `PSRAM = OPI`** if you are using a full-screen framebuffer and it crashes rather
   than draws.
7. **Only then** suspect hardware.

## 6. Boards in this repository using each bus

| Bus | Boards documented here |
|---|---|
| 8-bit 8080 | [LilyGO T-Display-S3](../../devices/lilygo/t-display-s3/README.md), [T-Display-S3 Touch](../../devices/lilygo/t-display-s3-touch/README.md) |
| QSPI | [T-Display-S3 AMOLED](../../devices/lilygo/t-display-s3-amoled/README.md), [AMOLED Plus](../../devices/lilygo/t-display-s3-amoled-plus/README.md), [1.64″](../../devices/lilygo/t-display-s3-amoled-1-64/README.md), [1.43/1.75″](../../devices/lilygo/t-display-s3-amoled-1-43-1-75/README.md), [T4-S3](../../devices/lilygo/t4-s3/README.md), [AMOLED Lite](../../devices/lilygo/t-display-amoled-lite/README.md), [T-Display-S3 Long](../../devices/lilygo/t-display-s3-long/README.md) |
| 4-wire SPI | [T-Display-S3 Pro](../../devices/lilygo/t-display-s3-pro/README.md) |
| MIPI-DSI | [Waveshare ESP32-P4-WIFI6-Touch-LCD-XC](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md) |

## See also

- [`display-interfaces.md`](display-interfaces.md) — the broader interface landscape
- [`e-paper-displays.md`](e-paper-displays.md)
- [`components/sitronix/st7789v`](../../components/sitronix/st7789v/README.md) — the controller
  behind the 8080 examples above
