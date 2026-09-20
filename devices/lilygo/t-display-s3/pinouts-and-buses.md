# LilyGO T-Display-S3 — pinouts and buses

> Board: **T-Display-S3** (non-touch and Touch share this map). Research snapshot **2026-09-07**.
> Every row is traceable to a file and commit. Where LilyGO's own sources disagree, both are shown.

## Evidence used

| Tag | Source | Retrieved |
|---|---|---|
| `PIN_CFG` | `Xinyuan-LilyGO/T-Display-S3` → `examples/factory/pin_config.h` @ **`ec889e789b3cf093412689a143f7f37b42b56af7`** (2 069 B, SHA-256 of the file body as fetched) | 2026-09-07 |
| `README` | same repo, `README.md` § *Pinout* @ `ec889e7` | 2026-09-07 |
| `IDF` | `Xinyuan-LilyGO/LilyGo-Display-IDF` → `main/product_pins.h`, block `#elif CONFIG_LILYGO_T_DISPLAY_S3` @ **`b1a1cc54994bf1b417e3bb30c437bbe1036bff7f`** | 2026-09-07 |
| `SCH` | `schematic/T_Display_S3.pdf` @ `ec889e7`, title block **2024-04-29**, one sheet. Text recovered with a locally written extractor; **designator/part strings only** — net connectivity was *not* traced. See [§7](#7-what-was-not-established) | 2026-09-07 |
| `TFT206` | `lib/TFT_eSPI/User_Setups/Setup206_LilyGo_T_Display_S3.h` @ `ec889e7` | 2026-09-07 |
| `ESPH` | `esphome/esphome` → `esphome/components/mipi_spi/models/lilygo.py`, entry `T-DISPLAY-S3`, branch `dev` fetched 2026-09-07 | 2026-09-07 |

`PIN_CFG` verbatim, the authoritative block:

```c
/* examples/factory/pin_config.h @ ec889e789b3cf093412689a143f7f37b42b56af7 */
#define PIN_LCD_BL                   38

#define PIN_LCD_D0                   39
#define PIN_LCD_D1                   40
#define PIN_LCD_D2                   41
#define PIN_LCD_D3                   42
#define PIN_LCD_D4                   45
#define PIN_LCD_D5                   46
#define PIN_LCD_D6                   47
#define PIN_LCD_D7                   48

#define PIN_POWER_ON                 15

#define PIN_LCD_RES                  5
#define PIN_LCD_CS                   6
#define PIN_LCD_DC                   7
#define PIN_LCD_WR                   8
#define PIN_LCD_RD                   9

#define PIN_BUTTON_1                 0
#define PIN_BUTTON_2                 14
#define PIN_BAT_VOLT                 4

#define PIN_IIC_SCL                  17
#define PIN_IIC_SDA                  18

#define PIN_TOUCH_INT                16
#define PIN_TOUCH_RES                21

/* External expansion */
#define PIN_SD_CMD                   13
#define PIN_SD_CLK                   11
#define PIN_SD_D0                    12
```

Nine `pin_config.h` copies exist across the repo's examples (`factory`, `tft`, `touch_test`,
`GetBatteryVoltage`, `sd`, `lv_demos`, `nes`, `ota`, `Sleep`, `PCBClock`, `PokerS3`,
`ImageScroll`, `TFT_Rainbow`). **All agree** on the pin numbers; they differ only in which
subset they define and in unrelated Wi-Fi/LCD-clock constants. That agreement is itself
evidence — a divergent copy would be the interesting case, and there is none.

---

## 1. Master GPIO map

| GPIO | Signal | Direction | Bus / role | Shared / strap | Source |
|---|---|---|---|---|---|
| 0 | `BUTTON_1` / **BOOT** | in, active-low | strap | **Strapping pin.** Held low at reset = download mode | `PIN_CFG`, `SCH` (`S2/S3/SW` = `SW-PB`) |
| 1 | free | — | header | — | `README` (absent from pin map ⇒ unused) |
| 2 | free | — | header | — | `README` |
| 3 | free | — | header | JTAG-select strap on ESP32-S3 | `README` |
| 4 | `BAT_VOLT` | in (ADC1_CH3) | ADC | **Conflict:** also the only battery sense. Cannot be reused | `PIN_CFG`, `SCH` (`R2`,`R4` = `100K %1`) |
| 5 | `LCD_RES` | out | 8080 | — | `PIN_CFG`, `IDF`, `TFT206`, `ESPH` |
| 6 | `LCD_CS` | out | 8080 | — | all |
| 7 | `LCD_DC` | out | 8080 | — | all |
| 8 | `LCD_WR` | out | 8080 | — | all |
| 9 | `LCD_RD` | out | 8080 | ESPHome treats it as an *enable* pin, tied high | `PIN_CFG`; `ESPH` `enable_pin=[9, 15]` |
| 10 | free | — | header | — | `README` |
| 11 | `SD_CLK` | out | SDMMC (**shield only**) | free unless the TF Shield is fitted | `PIN_CFG`, `README` |
| 12 | `SD_D0` | i/o | SDMMC (**shield only**) | as above | `PIN_CFG` |
| 13 | `SD_CMD` | i/o | SDMMC (**shield only**) | as above | `PIN_CFG` |
| 14 | `BUTTON_2` | in, active-low | — | the *other* user button; **not** RST | `PIN_CFG` |
| 15 | **`POWER_ON`** | out | power gate | **Must be driven HIGH** or nothing works on battery — [§3](#3-the-gpio15-power-gate) | `PIN_CFG`, `README`, `IDF` |
| 16 | `TOUCH_INT` | in | I²C IRQ | **Pulled up by a fitted resistor even on non-touch boards** — [§5](#5-gpio16--gpio17-are-not-free) | `PIN_CFG`, issue #313 |
| 17 | `IIC_SCL` | out | I²C | 10 kΩ pull-up `RIIC` fitted | `PIN_CFG`, `SCH` (`RIIC 10K`) |
| 18 | `IIC_SDA` | i/o | I²C | 10 kΩ pull-up `RIID` fitted | `PIN_CFG`, `SCH` (`RIID 10K`) |
| 19 | USB D− | — | native USB | not a GPIO in practice | `SCH` (`ESP_USB_DM`) |
| 20 | USB D+ | — | native USB | not a GPIO in practice | `SCH` (`ESP_USB_DP`) |
| 21 | `TOUCH_RES` | out | touch reset | free on non-touch boards, but see §5 | `PIN_CFG` |
| 26–32 | **unusable** | — | in-package OPI PSRAM | ESP32-S3R8 reserves them | ESP32-S3 datasheet |
| 33–37 | **unusable** | — | in-package OPI PSRAM (`SPIIO4..7`, `SPIDQS`) | ESP32-S3R8 reserves them | `SCH` (`SHICLK 33`, `SHICS0 32`, `SHIPD 30`, `SHIWP 31`) |
| 38 | `LCD_BL` | out | backlight enable → `U4 AW9364DNR` | **not a raw LED PWM** — [§4](#4-the-backlight-is-a-one-wire-boost-driver-not-a-pwm-pin) | `PIN_CFG`, `SCH` |
| 39 | `LCD_D0` | out | 8080 data | — | `PIN_CFG` |
| 40 | `LCD_D1` | out | 8080 data | — | `PIN_CFG` |
| 41 | `LCD_D2` | out | 8080 data | — | `PIN_CFG` |
| 42 | `LCD_D3` | out | 8080 data | — | `PIN_CFG` |
| 43 | `U0TXD` | out | UART0 | **Claimed by UART0 in Arduino even with CDC on** — [§6](#6-gpio43--gpio44-are-not-usable-as-gpio-under-arduino) | `SCH`, community |
| 44 | `U0RXD` | in | UART0 | as above | `SCH`, community |
| 45 | `LCD_D4` | out | 8080 data | **Strapping pin** (`VDD_SPI` voltage select) | `PIN_CFG` |
| 46 | `LCD_D5` | out | 8080 data | **Strapping pin** | `PIN_CFG` |
| 47 | `LCD_D6` | out | 8080 data | — | `PIN_CFG` |
| 48 | `LCD_D7` | out | 8080 data | — | `PIN_CFG` |

**Note on GPIO45/46.** Both are ESP32-S3 strapping pins *and* LCD data lines. They are sampled
only at reset, and the LCD driver only drives them afterwards, so there is no conflict in
normal operation — but if you hang anything on the LCD data bus (you should not) you can
change the boot behaviour. This is a board-level constraint, not a silicon defect.

---

## 2. Buses

### 2.1 The display: 8-bit Intel-8080 parallel

| Property | Value | Source |
|---|---|---|
| Controller | **Sitronix ST7789V** → [component record](../../../components/sitronix/st7789v/README.md) | `datasheet/ST7789V_SPEC_V1.4.pdf` shipped in the repo |
| Panel | 1.9″ IPS, **170 × 320** visible | `README` |
| Controller window offset | **`offset_width = 35`** — the ST7789V is a 240-wide part; the 170-px panel sits at column 35 | `ESPH`; corroborated by `TFT206` `#define TFT_WIDTH 170` + LilyGO's `Arduino_GFX` args |
| Bus | 8-bit parallel, `WR` strobed, `RD` unused in practice | `PIN_CFG`, `TFT206` `#define TFT_PARALLEL_8_BIT` |
| Pixel clock used by LilyGO | **16 MHz** — `#define EXAMPLE_LCD_PIXEL_CLOCK_HZ (16 * 1000 * 1000)` with the in-file comment *"Too low or too high pixel clock may cause screen mosaic"* | `PIN_CFG` |
| Pixel clock used by ESPHome | **10 MHz** (`data_rate="10MHz"`) | `ESPH` |
| Colour order | **Conflict.** `TFT_eSPI` setup says **RGB**; ESPHome says **BGR**. Both apply colour inversion | `TFT206` `#define TFT_RGB_ORDER TFT_RGB` vs `ESPH` `color_order=MODE_BGR` — see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) G3 |
| Colour inversion | **on** in both | `TFT206` `#define TFT_INVERSION_ON`; `ESPH` `invert_colors=True` |
| Init sequence | `INIT_SEQUENCE_3` — TFT_eSPI's alternate ST7789 init, with LilyGO's comment *"Using this initialisation sequence improves the display image"* | `TFT206` |

`TFT206` **verbatim and complete** — the file you must select by hand in
`TFT_eSPI/User_Setup_Select.h`:

```c
// ST7789 using 8-bit Parallel
// lib/TFT_eSPI/User_Setups/Setup206_LilyGo_T_Display_S3.h @ ec889e7

#define USER_SETUP_ID 206

#define USE_HSPI_PORT
#define ST7789_DRIVER
#define INIT_SEQUENCE_3 // Using this initialisation sequence improves the display image

#define CGRAM_OFFSET
#define TFT_RGB_ORDER TFT_RGB  // Colour order Red-Green-Blue
//#define TFT_RGB_ORDER TFT_BGR // Colour order Blue-Green-Red

#define TFT_INVERSION_ON
// #define TFT_INVERSION_OFF

#define TFT_PARALLEL_8_BIT

#define TFT_WIDTH 170
#define TFT_HEIGHT 320

#define TFT_CS  6
#define TFT_DC  7
#define TFT_RST 5

#define TFT_WR 8
#define TFT_RD 9

#define TFT_D0 39
#define TFT_D1 40
#define TFT_D2 41
#define TFT_D3 42
#define TFT_D4 45
#define TFT_D5 46
#define TFT_D6 47
#define TFT_D7 48

#define TFT_BL 38
#define TFT_BACKLIGHT_ON HIGH

#define LOAD_GLCD
#define LOAD_FONT2
#define LOAD_FONT4
#define LOAD_FONT6
#define LOAD_FONT7
#define LOAD_FONT8
#define LOAD_GFXFF

#define SMOOTH_FONT
```

Two things in that file are worth reading twice. **`CGRAM_OFFSET`** is what makes TFT_eSPI
apply the 35-column offset into the ST7789V's 240-wide GRAM — remove it and the image shifts.
**`USE_HSPI_PORT`** is vestigial for a parallel setup and does nothing here; it is left over
from TFT_eSPI's SPI setups and is not a mistake worth "fixing".

*(Reproduced from the retained copy at
[`../t-display-s3-shared/artifacts/tft-espi/Setup206_LilyGo_T_Display_S3.h`](../t-display-s3-shared/artifacts/tft-espi/Setup206_LilyGo_T_Display_S3.h),
SHA-256 `809949416716286a5b2db0821608251a1d69463ceea5721ccc5598a7fd841a5c`, 906 B.)*

### 2.2 I²C

| Property | Value |
|---|---|
| `SCL` / `SDA` | GPIO17 / GPIO18 |
| Pull-ups | **fitted on-board**, `RIIC` and `RIID` = 10 kΩ each (`SCH`) |
| Devices on a **Touch** board | touch controller only — **CST816S** at `0x15` (early boards) or **CST328** at `0x1A` (later). Both datasheets ship in the repo, which is itself the revision evidence |
| Devices on a non-touch board | **none** — the bus is free, but GPIO16 still carries a pull-up |
| Also on this bus | the 4-pin `SH1.0` "Qwiic-ish" connector, which is **not** Qwiic-pinout-compatible — see [issue #181](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/181) |

### 2.3 SDMMC — shield only

`PIN_SD_CMD 13 / PIN_SD_CLK 11 / PIN_SD_D0 12` describe the **T-Display TF Shield**
(store SKU `H609`/`H610`, USD 2.38–2.51 as of 2026-09-07), a separate PCB. The README states
plainly:

> "SD card pins (SD CMD/CLK/D0) are only available on boards with the SD Shield add-on. The
> standard T-Display-S3 board does not have an onboard SD card slot."

1-bit SDMMC. Do not expect 4-bit.

### 2.4 USB

Native ESP32-S3 USB on GPIO19/20 straight to the Type-C receptacle (`U5`, a 16-pin
`TYPEY-C` part in `SCH`). **There is no USB-UART bridge on this board** — no CH340, no CP210x.
Consequences in [`features/usb.md`](features/usb.md).

### 2.5 UART0

GPIO43 (TX) / GPIO44 (RX), brought out to the header. This is where `Serial` goes when
`USB CDC On Boot` is disabled.

---

## 3. The GPIO15 power gate

> "**Note:** GPIO15 is the peripheral power control pin. You must set it HIGH before using the
> board, otherwise the LCD and other peripherals will not work."
> — `README` @ `ec889e7`

```cpp
void setup() {
    pinMode(15, OUTPUT);
    digitalWrite(15, HIGH);   // V3V rail on — LCD, headers' 3V pin
    pinMode(38, OUTPUT);
    digitalWrite(38, HIGH);   // backlight on
}
```

`SCH` shows GPIO15 as net `PWR_EN`, gating a P-channel MOSFET (`Q2`/`Q3` = `SI2301`) that
feeds the `V3V` rail. The board's **green LED8** is on that rail, which gives you a free
indicator: *green LED off while on battery = you forgot GPIO15*.

When USB is connected the LDO output is present regardless, which is exactly why this bug
only appears on battery — the single most-reported problem with this board. The vendor FAQ
entry, [issue #79](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/79) and dozens of
duplicates all trace to it.

## 4. The backlight is a one-wire boost driver, not a PWM pin

`SCH` shows `U4 = AW9364DNR` with `LEDK1..LEDK4` — an **Awinic AW9364** LED backlight boost
driver → [component record](../../../components/awinic/aw9364/README.md). GPIO38 is its
enable/one-wire control input, not a current sink.

Practical effect: ordinary `ledcWrite()` PWM on GPIO38 *works* for coarse dimming, because the
driver's output follows the enable duty cycle, but the AW9364 also implements a **one-wire
pulse-count brightness protocol** (count rising edges within the timeout window to select one
of 16 levels). LilyGO's own `Dimming` notes and community code use the crude PWM route. Do not
assume linear brightness. See [`features/display.md`](features/display.md).

## 5. GPIO16 / GPIO17 are not free

From [issue #313](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/313) (2025-07-28),
answered by LilyGO maintainer `lewisxhe` with two PCB photographs:

> "Pull-up resistors are already added to the 16 and 17 boards, so when you set it to floating,
> it's pulled high by default. … If you must use these two GPIOs, you can remove these two
> resistors. The resistors are located on the back of the screen, please remove them carefully."

Reporter's firsthand symptom: an LED on GPIO16 or GPIO17 glows faintly with no code running,
and glows again the moment the chip enters deep sleep (when the driver stops holding the pin
low). **This applies to the non-touch board too** — the reporter confirmed they had the
non-touch version.

Evidence class: *vendor confirmation of a firsthand user report, with photographs.*

## 6. GPIO43 / GPIO44 are not usable as GPIO under Arduino

Firsthand, and reproduced by a second person in the same thread:

> "**GPIO 43 and 44 on ESP32-S3** are blocked by UART0 in Arduino IDE even when using Hardware
> CDC — can't be used for OneWire or digital input"
> — u/Alarming_Breadfruit5, [r/esp32, 2026-05-25](https://old.reddit.com/r/esp32/comments/1tnop7r/lilygo_tdisplay_s3_clock_with_ds18b20_and_pir/)
>
> "OKAY! I just tried it and it does not work on 43 or 44! TIL"
> — u/MrBoomer1951, same thread, 2026-05-26, after initially disputing it

> "The UART0 pins can be used if you disabled it in sdkconfig (esp-idf). Harder to do in
> Arduino." — u/Extreme_Turnover_838, same thread

Evidence class: **firsthand measurement, independently reproduced, with a stated workaround
that was not itself tested here.** Corroborates the earlier
[issue #117](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/117) (DS18B20 on GPIO43).

## 7. What was *not* established

Stated plainly so the next reader does not assume more rigour than exists.

- **Net connectivity was not traced from the schematic.** The PDF is an Altium export whose
  text layer yields designators, part strings and pin markers but not wires. What is asserted
  above from `SCH` is *the existence and part number of a designator*, plus the value printed
  beside it. The repo's [`tools/altium_pdf_netlist.py`](../../../tools/altium_pdf_netlist.py)
  can close this gap but needs `pdftotext -bbox` XML, and poppler was not available on this
  host. Recorded in [`gaps-and-conflicts.md`](gaps-and-conflicts.md).
- **The ADC divider ratio is inferred**, not traced: `R2` and `R4` are both `100K %1` and the
  vendor's own example multiplies the reading by 2. That is consistent, not proven.
- **No hardware was available.** Nothing in this record is `executed-success` against a
  physical board. Every command in [`commands.md`](commands.md) is labelled accordingly.
