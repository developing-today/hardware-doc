# Sitronix ST7789V2

- **Category:** single-chip TFT-LCD controller/driver with on-chip GRAM — 240 RGB × 320 dot,
  262 k colours, MCU parallel / SPI / RGB interfaces.
- **Manufacturer:** Sitronix Technology Corporation (Taiwan).
- **Retrieved:** 2026-09-04
- **Sibling records:** [`st7789vw`](../st7789vw/README.md) (already in this repository),
  [`st7789p3`](../st7789p3/README.md), [`st7701s`](../st7701s/README.md), [`st77916`](../st77916/README.md)

The display controller of the **M5Stack DinMeter (K134)**, and of the M5Dial and several other
M5Stack 1.14-inch products. Replaced by the ST7789P3 in DinMeter v1.1 — see
[§ ST7789V2 vs ST7789P3](#st7789v2-vs-st7789p3).

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **ST7789V2** | vendor datasheet title page |
| Datasheet version | **Version 1.0, 2016/11** | datasheet cover, validated against the rendered heading |
| Copyright | © 2016 Sitronix Technology Corporation | datasheet cover |
| GRAM | 240 RGB × 320 dots, 18-bit/pixel capable | datasheet |
| Colour depth in use on DinMeter | 16 bpp (RGB565) | `esp-board-manager` `bits_per_pixel: 16` |
| Panel on DinMeter | 1.14 in IPS, **135 × 240 visible** | M5Stack specification row |
| Interface on DinMeter | 4-wire SPI, **write-only** (MISO not wired) | DinMeter schematic `FPC1`; `esp-board-manager` `miso_io_num: -1` |

## 2. Board-independent facts worth knowing

- **The visible window is a sub-region of the 240 × 320 GRAM.** For a 135 × 240 panel the
  offset is **column +52, row +40**. ESP-IDF's `esp_lcd_panel_set_gap()` (or LovyanGFX's
  `offset_x` / `offset_y`) must apply it or the image is displaced and wraps.
  Source: `espressif/esp-board-manager` `m5stack_boards/m5stack_dinmeter/board_devices.yaml`
  (HEAD `2beb9b22b0892b343bd555a1ebc9929a7edce8fc`, 2026-09-03) — *"The visible window is offset
  inside the controller's 240x320 GRAM (column +52, row +40)."*
- **Colour inversion is required** on the M5Stack panels: `invert_color: true` (i.e. `INVON`,
  command `0x21`). Same source: *"ST7789V2 panel on M5Stack needs inversion"*. This is a panel
  property, not a controller property — an ST7789V2 on a different glass may not need it.
- **Driver:** ESP-IDF's built-in `esp_lcd_panel_st7789` handles it; no extra component
  dependency. In Arduino, M5GFX/LovyanGFX's `Panel_ST7789` class.
- SPI mode 0. The DinMeter clocks it at **40 MHz** (`pclk_hz: 40000000`, same source).

## 3. ST7789V2 vs ST7789P3

M5Stack changed the specified controller between DinMeter v1.0 and v1.1. What is actually
established:

| | ST7789V2 | ST7789P3 |
|---|---|---|
| Named on | DinMeter (K134) page: features, spec row, PinMap heading | DinMeter v1.1 page: same three places |
| Datasheet published by M5Stack | **yes** — `ST7789V2_SPEC_V1.0.pdf`, retained here | **no** — the *Datasheets* section on the v1.1 page has no display entry at all |
| Datasheet published by Sitronix (public) | not located in this pass | not located in this pass |
| Pin assignment on DinMeter | CS G7, SCK G6, RS G4, MOSI G5, RESET G8, BL G9 | **identical** |
| Resolution | 135 × 240 | **identical** |
| Listed in the vendor's own v1.0↔v1.1 comparison table | — | **no** |

**Assessment.** Both are ST7789-family SPI TFT controllers and no software difference is
documented, expected or observed. The substitution is almost certainly a panel-supply decision
rather than a functional one. But this is `inferred`: without an ST7789P3 datasheet the claim
"register-compatible" cannot be verified, and it is not asserted here.
→ [`../st7789p3/README.md`](../st7789p3/README.md)

## 4. Artifacts

| File | Size | SHA-256 | Version | Licence | Redistribution | Disposition |
|---|---:|---|---|---|---|---|
| [`artifacts/ST7789V2_SPEC_V1.0.pdf`](artifacts/ST7789V2_SPEC_V1.0.pdf) | 3 216 854 | `8937678475e20598c8deb17c3cdd41403da6317a3b6518f86144b8a609de9f46` | v1.0, 2016/11 | unknown — Sitronix copyright asserted, no redistribution grant | `unknown` | `repository` (unstaged pending review) |

**Provenance.** Retrieved 2026-09-04 from M5Stack's mirror
`https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/datasheet/unit/lcd/ST7789V2_SPEC_V1.0.pdf`
(HTTP 200, `%PDF` magic validated, text layer parses and the cover heading matches).

This is an **authorized-mirror copy**: M5Stack links it from its own product page, but Sitronix
is the publisher. No copy on a Sitronix host was located in this pass. Filed under the
component, not the device, per the "file by what it describes" rule — it was fetched while
researching the DinMeter but it describes a chip.

---

## Used By

### M5Stack DinMeter (SKU K134)

1.14 in 135 × 240 IPS panel on an 8-pin 0.5 mm FPC (`FPC1`, `FPC-0.5-8P`). Write-only 4-wire
SPI on `SPI2_HOST`: SCLK GPIO6, MOSI GPIO5, CS GPIO7, D/C GPIO4, RESET GPIO8. Backlight is not
a controller pin — GPIO9 gates an [AW35122FDR](../../awinic/aw35122/README.md) load switch
(`U6`) that feeds the panel LED string. GRAM gap +52/+40; `INVON` required.

→ [`devices/m5stack/dinmeter/features/display.md`](../../../devices/m5stack/dinmeter/features/display.md)
→ [`devices/m5stack/dinmeter/pinouts-and-buses.md`](../../../devices/m5stack/dinmeter/pinouts-and-buses.md)

### M5Stack DinMeter v1.1 — *not* this part

v1.1 specifies **ST7789P3**. → [`../st7789p3/README.md`](../st7789p3/README.md)

### M5Stack Cardputer v1.0, v1.1 and ADV

Identical display path on all three: 1.14″, **240 × 135**, 4-wire SPI driven 3-wire by M5GFX
(`spi_3wire = true`, `pin_miso = -1`), on `SPI3_HOST` at **40 MHz write / 16 MHz read**.
Connected through an 8-pin 0.5 mm FPC (`FPC1`) from the front panel.

`SCK` G36 · `MOSI` G35 · `DC` G34 · `CS` G37 · `RST` G33 · backlight **G38**.

M5GFX panel configuration: `panel_width = 135`, `panel_height = 240`, `offset_x = 52`,
`offset_y = 40`, `invert = true`, `readable = true`, `setRotation(1)`, backlight
`_set_pwm_backlight(GPIO_NUM_38, 7, 256, false, 16)` — **LEDC channel 7, 256 Hz**.

M5GFX identifies the panel by reading its ID on G37 and testing `(id & 0xFB) == 0x81`; that test
is the **gate for the whole Cardputer/VAMeter/CardputerADV autodetect branch**, so a failed panel
read means the board is not recognised at all.

⚠ **G38 is not only a backlight PWM.** On Stamp-S3A boards it also enables the `BL_3V3` rail
through an [AW35122FDR](../../awinic/aw35122/README.md), and that rail powers the
[WS2812](../../worldsemi/ws2812/README.md). Dimming the backlight browns out the RGB LED.

Records: [v1.0](../../../devices/m5stack/cardputer-v1.0/README.md) ·
[v1.1](../../../devices/m5stack/cardputer-v1.1/README.md) ·
[ADV](../../../devices/m5stack/cardputer-adv/README.md)

*Added 2026-09-07 from `scratch/m5stack-cardputer/index-fragments.md` §3.6.*
