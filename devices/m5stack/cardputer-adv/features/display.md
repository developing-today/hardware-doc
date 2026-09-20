# Cardputer ADV — display

> **Question:** *"How do I draw on the screen, and why does my RGB LED die when I dim it?"*
> Applies to **all Cardputer revisions** — the display path is unchanged from v1.0 to ADV.
> Verified **2026-09-04**.

## Hardware

| Item | Value | Record |
|---|---|---|
| Panel | ST7789V2, 1.14″, **240 × 135** visible | [`sitronix/st7789v2`](../../../../components/sitronix/st7789v2/README.md) |
| Interface | SPI, `SPI3_HOST`, **3-wire** (`spi_3wire = true`, `pin_miso = -1`) | M5GFX |
| Clock | 40 MHz write, 16 MHz read | M5GFX `bus_cfg` |
| Connection | 8-pin 0.5 mm FPC (`FPC1`) from the front panel | schematic sheet 1 |

| Signal | GPIO |
|---|---|
| `SCK` | G36 |
| `MOSI` | G35 |
| `DC`/`RS` | G34 |
| `CS` | G37 |
| `RST` | G33 |
| Backlight PWM / `BL_3V3` enable | **G38** |

M5GFX panel configuration for the Cardputer family:
`panel_width = 135`, `panel_height = 240`, `offset_x = 52`, `offset_y = 40`,
`invert = true`, `readable = true`, `setRotation(1)` — i.e. the panel is a 240-tall portrait
part used in landscape with a window offset. Backlight:
`_set_pwm_backlight(GPIO_NUM_38, 7, 256, false, 16)` — **LEDC channel 7, 256 Hz, offset 16**.

## Minimal procedure

```cpp
#include <M5Cardputer.h>
void setup() {
  auto cfg = M5.config();
  M5Cardputer.begin(cfg, true);
  M5Cardputer.Display.setRotation(1);
  M5Cardputer.Display.setBrightness(255);
  M5Cardputer.Display.fillScreen(TFT_BLACK);
  M5Cardputer.Display.drawString("hello", 10, 10);
}
void loop() {}
```

## ⚠ The backlight rail also powers the RGB LED

On **Stamp-S3A** (so: v1.1 and ADV, not v1.0) `DISP_BL` = **G38** drives the enable pin of an
**AW35122FDR** load switch that produces `BL_3V3`, and `BL_3V3` supplies **both** the LCD
backlight **and** the WS2812 RGB LED. On the older StampS3 v0.2 the WS2812 was fed from the
always-on `VDD_3V3` instead. Verified by comparing U3's `VDD` net across the two Stamp
schematics: `VDD_3V3` on v0.2, `BL_3V3` on v0.3.3.

Consequences:

* **PWM-dimming the backlight chops the WS2812's supply.** M5Stack's v1.1 page says it
  outright: *"Since RGB and LCD backlight share the same power source, when the LCD backlight
  brightness is below 100%, RGB will not be powered properly. Please use the RGB function when
  the backlight is at full brightness."* The ADV page **omits this warning** even though the
  ADV uses the same Stamp-S3A — a vendor documentation gap, recorded in
  [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md).
* The ADV page instead says *"set GPIO38, which controls this switch, to a high level"* before
  using the RGB LED. Both statements describe the same AW35122FDR.
* **Backlight off means RGB LED off.** You cannot have a dark screen and a status LED.
* Component: [`awinic/aw35122`](../../../../components/awinic/aw35122/README.md),
  [`worldsemi/ws2812`](../../../../components/worldsemi/ws2812/README.md).

## Alternatives

| Approach | Notes |
|---|---|
| `M5GFX` / `M5Unified` | default; gets autodetect, rotation, offsets, backlight for free |
| `TFT_eSPI` | what Bruce uses: `ST7789_2_DRIVER`, `TFT_WIDTH=135`, `TFT_HEIGHT=240`, `TFT_RGB_ORDER=1`, `USE_HSPI_PORT`, `SPI_FREQUENCY=20000000`, `MINBRIGHT=160` |
| `meshtastic/st7789` | Meshtastic's fork, pinned at `92bae2e4` |
| LovyanGFX directly | M5GFX *is* a LovyanGFX derivative |

Bruce runs the panel at **20 MHz**, M5GFX at **40 MHz**. Both are reported working; the
difference is margin, not correctness.

## Secondary displays

The CAP header has enough SPI to drive a second panel, and the community does:
`Prokuon/CardputerADV_Cap_TFT-2.8` and `_V2`, `guicmg/cardputer_adv_external_screen`
("Guide to how use Dual Screen with Cardputer ADV"), and ZX Spectrum ports to ILI9341/ILI9488.
The Cap TFT-2.8 announcement on r/CardPuter (2026-06-22) reached ↑989 with 75 comments — the
highest-scoring Cardputer hardware post found in this pass.

## Resources and limits

| Resource | Used |
|---|---|
| SPI host | `SPI3_HOST`, exclusive to the panel |
| GPIO | G33–G38 |
| LEDC | channel 7 |
| DMA | M5GFX uses SPI DMA; no explicit channel pinning found |

| Limit | Class |
|---|---|
| 240 × 135 × 16 bpp = 64 800 B full framebuffer | **board/silicon** — that is 12.7 % of the 512 KB SRAM, and there is **no PSRAM**, so double-buffering plus a network stack is tight |
| No touch | board |
| No MISO wired (`spi_3wire`) | board — panel reads go over the data line |

## Evidence status

Pin map and M5GFX configuration: **official** (source at pinned commit).
Rail sharing: **official** — two vendor schematics compared.
No display timing or refresh-rate measurement was taken: **not tested**.
