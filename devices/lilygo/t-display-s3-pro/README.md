# LilyGO T-Display-S3 Pro (2.33″)

> **Product:** T-Display S3 Pro · store handle `t-display-s3-pro` · published **2023-09-07** ·
> **18 SKUs**: no camera **USD 37.99**, GC0308 camera **46.54**, OV5640 camera **56.99**, four
> shell colours, plus MVSR-board bundles. All in stock 2026-09-07.
> Repo `T-Display-S3-Pro` @ **`08b8b2bbcb8b263131af119476403080cd30224f`**.
>
> Research retrieved **2026-09-07**. No hardware. Part of the
> [T-Display-S3 family](../t-display-s3-shared/README.md).

## Identity

| | |
|---|---|
| Panel | 2.33″, **222 × 480** (README also writes it 480 × 222) |
| Controller | **Sitronix ST7796** on **4-wire SPI** — *not* parallel, *not* QSPI. **Naming conflict**: the README says **ST7796U**, the repo ships **`ST7796S-Sitronix.pdf`** |
| Touch | **Hynitron CST226SE**, I²C **`0x5A`** |
| PMIC | **Silergy SY6970**, I²C **`0x6A`** — charging, OTG, ADC, input-current limit |
| Ambient light | **Lite-On LTR-553ALS**, I²C **`0x23`** |
| IMU | **BHI260AP** *or* an ICM-209xx-class part — **two schematics ship** |
| Storage | microSD on the shared SPI bus, `CS` GPIO14 |
| Buttons | **three**: GPIO0, GPIO12, GPIO16 |
| Extras | vibration motor GPIO16, camera FPC, a hardware power switch |
| Component records | [`sitronix/st7796s`](../../../components/sitronix/st7796s/README.md) · [`hynitron/cst226se`](../../../components/hynitron/cst226se/README.md) · [`silergy/sy6970`](../../../components/silergy/sy6970/README.md) · [`lite-on/ltr-553als-01`](../../../components/lite-on/ltr-553als-01/README.md) · [`bosch-sensortec/bhi260ap`](../../../components/bosch-sensortec/bhi260ap/README.md) |

This is the most complete board in the family — the only one that is close to being a product
rather than a module. It is also the one with the most revision ambiguity.

## Pinout

From `examples/factory/utilities.h` @ `08b8b2b`, verbatim in structure:

```c
// LTR553 , TOUCH , SY6970 , Camera share I2C Bus
#define BOARD_I2C_SDA       5
#define BOARD_I2C_SCL       6
#define VIBRATING_MOTOR    16
// SD , TFT share SPI Bus
#define BOARD_SPI_MISO      8
#define BOARD_SPI_MOSI     17
#define BOARD_SPI_SCK      18
#define BOARD_TFT_CS       39
#define BOARD_TFT_RST      47
#define BOARD_TFT_DC        9
#define BOARD_TFT_BL       48
#define BOARD_SD_CS        14
#define BOARD_SENSOR_IRQ   21
#define BOARD_TOUCH_RST    13
#define BOARD_TFT_WIDTH   222
#define BOARD_TFT_HEIHT   480      // sic
#define BOARD_USER_BUTTON  {0, 12, 16}
#define BOARD_USER_BTN_NUM 3
```

**`VIBRATING_MOTOR` and the third user button are both GPIO16.** That is in LilyGO's own file
and is not obviously an error — a haptic driven by the same pin as a button read would be —
but it is worth verifying before using either. `product_pins.h` @ `b1a1cc5` gives
`BOARD_TOUCH_IRQ 7`, which `utilities.h` does not define at all.

Camera pins are in the same file (`CAMERA_PIN_*`, XCLK GPIO11 at 20 MHz, PWDN GPIO46, white LED
GPIO38) and apply to the Camera Shield.

## V1.0 vs V1.1 — the backlight scale

Directly from `examples/factory/utilities.h` @ `08b8b2b`:

```c
//! Using T-Display-Pro V1.0 , uncomment use V1.1 ,
//! The difference between V1.0 and V1.1 is the backlight driver.
// #define USING_DISPLAY_PRO_V1
…
#ifdef USING_DISPLAY_PRO_V1
#define BRIGHTNESS_MAX_LEVEL        255
#else
#define BRIGHTNESS_MAX_LEVEL        16
#endif
```

**255 levels on V1.0, 16 on V1.1.** Build for the wrong one and brightness is 16× off. The repo
also ships `firmware/v1.0/` and `firmware/v1.1/` as separate directories. This is documented
**nowhere but that comment** — see
[revision R6](../t-display-s3-shared/board-revision-drift.md#r6--t-display-s3-pro-v10-vs-v11-backlight-driver).

## Which IMU?

The repo ships **both** `schematic/T-BHI260.pdf` (+ a `_V1.1` version) and
`schematic/T-ICM29048.pdf`, KiCad footprints for both (`T-BHI260.kicad_mod`,
`T-CIM29048.kicad_mod`), and firmware named `UnitTest_V1.1_DisChg_BHI260_241111.bin`.
**The product name does not tell you which sensor is fitted.** Scan I²C.
Recorded as [R7](../t-display-s3-shared/board-revision-drift.md#r7--t-display-s3-pro-two-different-imu-daughter-boards).

## Power

- **SY6970** at `0x6A` — full I²C charger/PMIC. Battery voltage, charge state, input current
  limit and OTG boost are all readable/settable in software. `examples/PMU_Example` is the
  reference. This is a genuine step up from the base board.
- **A hardware power switch**, with a vendor caveat worth quoting: *"The power switch is only
  effective when the battery is connected; disconnect the battery from the motherboard."*
  It gates the battery, not USB.

## Software

| Route | Status |
|---|---|
| `Arduino_GFX` | LilyGO's choice; the repo vendors `GFX Library for Arduino` |
| `TFT_eSPI` | plain SPI, so it *can* work, but no vendor setup file ships |
| **ESPHome** | model **`T-DISPLAY-S3-PRO`** exists: `ST7796`, `width=222, height=480, offset_width=49, cs_pin=39, reset_pin=47, dc_pin=9, backlight_pin=48, invert_colors=True`. Note `offset_width=49` — the 222-px panel sits in a 320-wide ST7796 window |
| Libraries | `TouchLib`, `ESP32_USB_Stream v0.0.1`, `ESP32-audioI2S v3.0.8`, `SensorLib`, `XPowersLib` |

## Add-on backplates

| Board | What it adds | Repo |
|---|---|---|
| **MVSRBoard** (`H751`, USD 10.20) | MAX98357A speaker amp, MSM261S4030H0R mic, PCF85063ATL RTC, vibration — "extremely low static current" | [`t-display-s3-pro-mvsrboard`](../t-display-s3-pro-mvsrboard/README.md) |
| **MVSRLora** | the above **plus LoRa** | `T-Display-S3-Pro-MVSRLora` |
| **Camera Shield** | GC0308 or OV5640 | in-repo |
| **T-Display S3 Pro LR1121** (USD 65.29) | LoRa variant sold as its own product | store |

## Artifacts

`artifacts/schematic/`: `T-Display-Pro.pdf` (275 972 B, `3d21d23987d83013…`),
`T-BHI260_V1.1.pdf` (362 516 B, `afc9bc9a426a0626…`),
`T-ICM29048.pdf` (371 702 B, `76effd69dd22b519…`),
`Camer-Shield.pdf` [sic] (92 889 B, `cf36beb70a7653b7…`). All retrieved 2026-09-07 at `08b8b2b`.
Chip datasheets (ST7796S, SY6970, MAX98357A, MSM261S4030H0R, PCF85063ATL) are filed under
their components.

**Repo licence: none declared.** Redistribution status of these PDFs is **unknown**.

## Gaps and conflicts

| # | Item | Status |
|---|---|---|
| P1 | **ST7796U (README) vs ST7796S (shipped datasheet) vs `ST7796` (ESPHome)** | **Unresolved.** The S and U are different parts with different max resolutions. ESPHome's `offset_width=49` implies a 320-wide controller, consistent with either |
| P2 | **GPIO16 is both `VIBRATING_MOTOR` and user button 3** | **Unresolved.** In the vendor's own file |
| P3 | **Which IMU is fitted** | **Unresolved by documentation.** Scan I²C |
| P4 | **V1.0 vs V1.1** backlight scale, documented only in a source comment | **Vendor-documented, badly** |
| P5 | `BOARD_TOUCH_IRQ` absent from `utilities.h`, present as GPIO7 in `product_pins.h` | **Resolved in favour of `product_pins.h`** |
| P6 | 22 open issues | maturity signal |
| P7 | `datasheet/C492375.PDF.pdf` is named by **LCSC part number**, so what it documents is not knowable from the filename | **Open** — not retrieved by this pass |
