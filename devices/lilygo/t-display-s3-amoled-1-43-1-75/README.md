# LilyGO T-Display-S3 AMOLED 1.43″ / 1.75″ (round)

> Sold on the same store page as the [1.64″](../t-display-s3-amoled-1-64/README.md)
> (handle `t-display-s3-amoled-1-64`, title *T-Display S3 AMOLED (DS)*).
> SKUs `H741` 1.43″ **USD 23.99**, `H741-01` 1.75″ **USD 27.86**, `H741-02` 1.75″ half-circle
> convex mirror **USD 30.25**. In stock 2026-09-07.
>
> Repo `T-Display-S3-AMOLED-1.43-1.75` @ **`87aabe888eea6a7c0f95ce1991ca75fa98c2a172`**,
> licence **MIT**. Research retrieved 2026-09-07. **Depth: medium.** No hardware.

## Three panels, one Kconfig switch

`components/private_library/pin_config.h` @ `87aabe8` opens with a three-way selector that
**`#error`s if you pick none** — the clearest statement anywhere of what this product is:

```c
#if defined CONFIG_SCREEN_TYPE_DO0143FMST10
#define DO0143FMST10 // 1.43 inches (CO5300 FT3168)
#elif defined CONFIG_SCREEN_TYPE_DO0143FAT01
#define DO0143FAT01  // DO0143FMST02 // 1.43 inches (SH8601 FT3168)
#elif defined CONFIG_SCREEN_TYPE_H0175Y003AM
#define H0175Y003AM  // 1.75 inches (CO5300 CST9217)
#else
#error "Unknown macro definition. Please select the correct macro definition."
#endif
```

| Build symbol | Panel | Display driver | Touch |
|---|---|---|---|
| `DO0143FMST10` | 1.43″ round | **CO5300** (Chipone) | **FT3168** (FocalTech) |
| `DO0143FAT01` / `DO0143FMST02` | 1.43″ round | **SH8601** (Shenghe Microelectronics) | **FT3168** |
| `H0175Y003AM` | 1.75″ round | **CO5300** | **CST9217** (Hynitron) |

**Two different display controllers and two different touch controllers ship under one product
page.** This is the sharpest example of LilyGO's revision culture in the whole family.

## Pinout — QSPI

Verbatim from the same file @ `87aabe8`:

| Signal | GPIO |
|---|---|
| `LCD_SDIO0..3` | 11, 13, 14, 15 |
| `LCD_SCLK` | 12 |
| `LCD_CS` | 10 |
| `LCD_RST` | 17 |
| `LCD_EN` | 16 |
| `IIC_SDA` / `IIC_SCL` | 7 / 6 |
| `TP_INT` | 9 |
| `PCF8563_INT` | **9** — **the same pin as `TP_INT`** |
| `BATTERY_VOLTAGE_ADC_DATA` | 4 |
| `SD_CS` / `MOSI` / `MISO` / `SCLK` | 38 / 39 / 40 / 41 |

**`TP_INT` and `PCF8563_INT` are both GPIO9.** Either the two interrupts are wire-ORed (likely,
both being open-drain) or one define is wrong. **Not resolved** — no schematic is published.

## Resolution conflict

| Source | Value |
|---|---|
| repo README | **466 × 466** |
| `pin_config.h` @ `87aabe8` | `LCD_WIDTH 473` / `LCD_HEIGHT 467` |

Both for both panel sizes. The likely reading is that 473 × 467 is the CO5300/SH8601
**addressable window** and 466 × 466 the visible circle — but that is inference. Recorded as
family conflict [F4](../t-display-s3-shared/README.md#4-family-level-conflicts).

## Chips

| Function | Part | Component record |
|---|---|---|
| SoC | ESP32-S3R8, 16 MB flash, 8 MB OPI PSRAM | [`espressif/esp32-s3r8`](../../../components/espressif/esp32-s3r8/README.md) |
| Display | **CO5300** or **SH8601** | [`chipone/co5300`](../../../components/chipone/co5300/README.md) · [`shenghe-microelectronics/sh8601z`](../../../components/shenghe-microelectronics/sh8601z/README.md) |
| Touch | **FT3168** or **CST9217** | [`focaltech/ft3168`](../../../components/focaltech/ft3168/README.md) · CST9217 *(record pending)* |
| PMIC | **SY6970** | [`silergy/sy6970`](../../../components/silergy/sy6970/README.md) |
| RTC | **PCF8563** | [`nxp/pcf8563`](../../../components/nxp/pcf8563/README.md) |
| microSD | on-board, SPI | [`generic/micro-sd-sdmmc`](../../../components/generic/micro-sd-sdmmc/README.md) |

Examples confirm each: `FT3168`, `SY6970`, `SY6970_OTG`, `PCF8563`, `PCF8563_Scheduled_INT`,
`PCF8563_Timer_INT`, `Deep_Sleep_PCF8563_Scheduled_Wake_Up`, `Deep_Sleep_PCF8563_Timer_Wake_Up`,
`Original_Test`, `GFX_FT3168_Image`, `lvgl_benchmark`, plus a `debug/` tree with `SD_MJPEG`
video-playback examples.

**The RTC-scheduled deep-sleep wake examples are notable** — this and the AMOLED Plus are the
only boards in the family that can wake on a wall-clock time rather than a timer or a pin.

## Documents shipped in `information/`

`CO5300_V0.01.pdf` (13.2 MB) · `SH8601Z.pdf` (4.5 MB) · `FT3168.pdf` · `PCF8563.pdf` ·
a Chinese PCF8563 spec · `AN_SY6970.pdf` · `EVB_SY6970.pdf` ·
`DO0143FMST10-DWO.pdf` (panel drawing) ·
`H0175Y003AM V0 1.75Inches 466X466 MIPI OR QSPI AMOLED.pdf`.
The chip datasheets are filed under their component records; the panel drawings were **not**
retrieved.

Note the 1.75″ panel document's own title says **466 × 466** and "MIPI **OR** QSPI" — the panel
supports both interfaces and LilyGO wires QSPI.

## Sources

| ID | Source | Class | Retrieved |
|---|---|---|---|
| R1 | repo README.md @ `87aabe8` | primary | 2026-09-07 |
| R2 | `components/private_library/pin_config.h` @ `87aabe8` | primary | 2026-09-07 |
| R3 | `information/*.pdf` tree listing @ `87aabe8` | primary | 2026-09-07 |
| R4 | LilyGO store feed | primary | 2026-09-07 |

## Gaps

- **No schematic published.** Searched the full tree; there is none.
- **GPIO9 double-assignment unresolved.**
- **Resolution conflict unresolved.**
- Medium-depth stub: no `features/`, no example catalogue, no acquisition manifest.
- CST9217 has no component record yet.
- No hardware.
