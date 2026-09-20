# LilyGO T-Display AMOLED Lite (1.47″)

> Store handle `t-display-amoled-lite`, SKU `H593`, **USD 35.66**, in stock 2026-09-07.
> Published **2022-11-12** — **five months before** the T-Display-S3 AMOLED 1.91″, despite the
> "Lite" name. It is the *first* AMOLED board in the line, not a cut-down later one.
>
> Covered by `LilyGo-AMOLED-Series` @ **`6d1dc008b94578cc34ba4a0f3b223dd808ca963f`**.
> Research retrieved 2026-09-07. **Depth: medium.** No hardware.
> Note LilyGO does **not** put "S3" in this product's name.

## Identity — the odd one out

| | | Source |
|---|---|---|
| Panel | 1.47″ AMOLED, **194 × 368**, **450 nits** | library README @ `6d1dc00` |
| Display driver | **SH8501B** — **Shenghe Microelectronics**, established from the datasheet cover | `datasheet/SH8501B0 DataSheet.pdf` |
| **Level shifter `U2`** | **RS0108YTQC20** — the panel runs at **1.8 V** and the ESP32-S3 at 3.3 V. Every display and touch signal crosses a translator (`AM_SPI_*_1V8`, `TP_INT_1V8` nets on the sheet) | schematic |
| Touch | **CHSC5816** (Chipsemi) | library README | 
| **PMU `U5`** | **X-Powers AXP2101** — a full PMU with I²C, ADC and multiple rails. The only board in the family with one | schematic + `examples/PMU_ADC`, `PMU_Interrupt` |
| Ambient light | **CM32181** (Capella) | library README datasheet links |
| RGB LED `U6` | **WS2812B-2020** on GPIO18 | schematic; `BOARD_PIXELS_PIN (18)`, `BOARD_PIXELS_NUM 1` |
| Other | `U4 = BV6804` (unidentified), `Q1 AO3400`, blue LED, USB-C 3.0 receptacle `J1` | schematic |
| Component records | [`shenghe-microelectronics/sh8501b`](../../../components/shenghe-microelectronics/sh8501b/README.md) · [`x-powers/axp2101`](../../../components/x-powers/axp2101/README.md) · [`chipsemi/chsc5816`](../../../components/chipsemi/chsc5816/README.md) · [`capella-microsystems`](../../../components/capella-microsystems/) · [`worldsemi`](../../../components/worldsemi/) |

**The 1.8 V level-shifted panel is the defining difference.** Nothing else in the family has
one, and it explains both the AXP2101 (multiple rails) and why this board's code is not
interchangeable with the other AMOLED boards despite sharing a library.

## Pinout

`product_pins.h` block `#if CONFIG_LILYGO_T_AMOLED_LITE_147` @ `b1a1cc5`:

| Signal | GPIO |
|---|---|
| `DISP_CS` / `SCK` | 4 / 5 |
| `DISP_DATA0..3` | 7, 10, 11, 12 |
| `DISP_RESET` / `TE` | 40 / 6 |
| `I2C_SDA` / `SCL` | 1 / 2 |
| `PMU_IRQ` | 3 |
| `SENSOR_IRQ` | 8 |
| `TOUCH_IRQ` / `TOUCH_RST` | 13 / 14 |
| `BOOT` / `BUTTON1` / `BUTTON2` | 0 / 0 / 21 |
| `PIXELS` (WS2812B) | 18 |

## Vendor-stated limitations

From the library README @ `6d1dc00`, FAQ 3:
> "**1.47 inches AMOLED (T-Display-AMOLED-Lite)** does not support hardware screen rotation
> function"

and the current table:
> **90–230+ mA** active; **≈1.1 mA** deep sleep, **timer wakeup only**

That 1.1 mA is **five times** the 1.91″/2.41″ boards' 230 µA, and the wake source is limited to
a timer where the others support external GPIO0 wake. **This is the worst board in the family
for battery life**, and the vendor says so in a table most people skip.

Examples specific to it: `LumenMeter` (the CM32181 ambient-light sensor), `PMU_ADC`,
`PMU_Interrupt` — the last two are marked *"only support 1.47-inch AMOLED"*.

## Artifacts

`artifacts/schematic/T-Display_AMOLED-Lite.pdf` — 417 259 B,
SHA-256 `3660881df7844a145b7f773fdb41f27679ddb1bce49a95d0122d8b9b014a01ca`, retrieved 2026-09-07
at `6d1dc00`. The SH8501B0 datasheet is filed under
[`components/shenghe-microelectronics/sh8501b/artifacts/`](../../../components/shenghe-microelectronics/sh8501b/artifacts/).

## Sources

| ID | Source | Class | Retrieved |
|---|---|---|---|
| L1 | `LilyGo-AMOLED-Series` README.MD @ `6d1dc00` | primary | 2026-09-07 |
| L2 | `schematic/T-Display_AMOLED-Lite.pdf` @ `6d1dc00` | primary | 2026-09-07 |
| L3 | `LilyGo-Display-IDF/main/product_pins.h` @ `b1a1cc5` | primary | 2026-09-07 |
| L4 | `datasheet/SH8501B0 DataSheet.pdf` @ `6d1dc00` | credible mirror | 2026-09-07 |
| L5 | LilyGO store feed | primary | 2026-09-07 |

## Gaps

- Medium-depth stub: no `features/`, no example catalogue, no acquisition manifest.
- `BV6804` (`U4`) unidentified — same family as the `BV6802` on the 1.91″ AMOLED V1.0.
- **No ESPHome model** for this board (the other three AMOLEDs have one).
- Net connectivity not traced. No hardware.
