# T-Display-S3 — display

| | |
|---|---|
| Panel | 1.9″ IPS, **170 × 320** portrait-native (LilyGO markets it landscape) |
| Controller | **Sitronix ST7789V** → [component](../../../../components/sitronix/st7789v/README.md) |
| Bus | 8-bit **Intel-8080 parallel**, `WR`-strobed |
| Pins | `D0..D7` = 39,40,41,42,45,46,47,48 · `WR` 8 · `RD` 9 · `DC` 7 · `CS` 6 · `RST` 5 |
| Backlight | **GPIO38** → Awinic **AW9364DNR** boost driver → [component](../../../../components/awinic/aw9364/README.md) |
| Panel power | **gated by GPIO15** — must be HIGH |
| GRAM offset | **35 columns** (170-px panel on a 240-wide controller) |
| Colour | inversion **on**; RGB/BGR is [disputed](../gaps-and-conflicts.md#g3--colour-order-rgb-or-bgr) |

## Minimum working sketch

```cpp
#include <TFT_eSPI.h>            // requires Setup206 selected — see below
TFT_eSPI tft = TFT_eSPI();

void setup() {
    pinMode(15, OUTPUT); digitalWrite(15, HIGH);   // panel rail — WITHOUT THIS, NOTHING
    pinMode(38, OUTPUT); digitalWrite(38, HIGH);   // backlight
    tft.init();
    tft.setRotation(1);          // 320x170 landscape
    tft.fillScreen(TFT_BLACK);
    tft.drawString("hello", 10, 10, 4);
}
void loop() {}
```

Two `pinMode`/`digitalWrite` pairs before `tft.init()`. Omit the first and you get a lit
backlight over a dead panel — which reads as a broken screen, and is the most common false
hardware diagnosis on this board.

## Choosing a library

Full decision guide, including why this matters more than usual:
[`guides/hardware/parallel-8080-lcd-buses.md`](../../../../guides/hardware/parallel-8080-lcd-buses.md).

| Library | Verdict for this board |
|---|---|
| **`TFT_eSPI`** | LilyGO's default. Richest API. **Requires editing `User_Setup_Select.h` inside the library** to select `Setup206_LilyGo_T_Display_S3.h`, and that edit is destroyed by any library update. Documented broken on Arduino core > 2.0.14 |
| **`Arduino_GFX`** | Configuration lives in your sketch, so it survives updates and works on core 3.x. **LilyGO's own recommended hardware test** for exactly that reason |
| **`LovyanGFX`** | Best if one codebase must span several boards in this family |
| **ESPHome** | `mipi_spi` with model `T-DISPLAY-S3` — pins, offset and the GPIO15 enable are all built in |
| **LVGL** | 8.x for LilyGO's examples (`examples/lv_demos/lv_conf.h` @ `ec889e7` is an LVGL 8 config). 9.x needs porting |

The `TFT_eSPI` edit, verbatim:

```c
// TFT_eSPI/User_Setup_Select.h
//#include <User_Setup.h>
#include <User_Setups/Setup206_LilyGo_T_Display_S3.h>
```

Community workaround worth knowing, from
[issue #212](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/212) (2024-01-03): keep a
copy of your edited `User_Setup_Select.h` outside the library and restore it after every
update. *"Confusing? YES!"* — the same commenter.

## Backlight and dimming

GPIO38 drives the **enable input of an AW9364 boost driver**, not an LED directly.

- Crude PWM (`ledcAttach(38, 5000, 8); ledcWrite(38, duty)`) works and is what everyone does.
- **Arduino core 3.x renamed the API**: `ledcSetup`/`ledcAttachPin` → `ledcAttach`/`ledcDetach`.
  LilyGO's snippets predate this. Firsthand report:
  [r/esp32, 2026-05-25](https://old.reddit.com/r/esp32/comments/1tnop7r/lilygo_tdisplay_s3_clock_with_ds18b20_and_pir/).
- The AW9364 also implements a **one-wire pulse-count** brightness protocol (16 steps selected
  by counting rising edges inside a timeout). Nothing in LilyGO's examples uses it. If your PWM
  dimming behaves oddly at low duty — flicker, or steps rather than a ramp — that is why: you
  are feeding pulse trains into a part that counts pulses.
- Brightness is **not** linear in duty cycle. Do not build a UI slider on the assumption.

## Rotation and geometry

`setRotation(1)` gives 320 × 170 landscape with the USB-C port on the left. Rotation 3 flips
it. Rotations 0 and 2 give 170 × 320 portrait. The GRAM offset applies in all of them, which
is why it must be a library setting rather than something you subtract yourself.

## Resource cost

| Resource | Taken |
|---|---|
| GPIO | **13** (8 data + WR + RD + DC + CS + RST), plus GPIO38 backlight and GPIO15 rail = **15** |
| Peripheral | ESP32-S3 **LCD_CAM** i80 unit (one of one) |
| DMA | one GDMA channel when using `esp_lcd`/`Arduino_GFX` DMA paths |
| PSRAM | a full 170×320 RGB565 framebuffer is 108.8 KB; LVGL double-buffered at full height needs 217.6 KB — this is why **`PSRAM = OPI PSRAM` is mandatory** for the vendor LVGL demo |

## Known failures and their causes

| Symptom | Cause | Fix |
|---|---|---|
| Backlight on, screen black | GPIO15 not high | two lines in `setup()` |
| Nothing at all, sketch uploaded fine | `User_Setup_Select.h` overwritten | re-select Setup206, or use `Arduino_GFX` to prove the hardware |
| Image shifted, garbage band at one edge | GRAM offset missing | `CGRAM_OFFSET` / `offset_width: 35` / the two `35`s in the `Arduino_GFX` constructor |
| Mosaic, speckle, tearing | pixel clock too high (or too low) | try 10 MHz |
| Half the display garbage | offset **and** wrong width | [issue #128](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/128) |
| Colours inverted or R/B swapped | inversion or colour-order setting | one `#define`, see [G3](../gaps-and-conflicts.md#g3--colour-order-rgb-or-bgr) |
| Compile `#error` about Setup206 | newer TFT_eSPI detecting the unselected setup | [issue #326](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/326) |
| Runs out of memory in LVGL | `PSRAM` not set to OPI | [issue #256](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/256) |
