# LilyGO T4-S3 (2.41″ AMOLED)

> **This is the board people mean by "T-Display-S3 AMOLED 2.41″".** LilyGO does **not** call it
> that. Store handle **`t4-s3`**, title *T4 S3*, published **2023-11-03**.
> SKUs `H678` basic **USD 56.89**, `H724` shell+soldered **60.23**, `H711` shell+female header
> **58.99** (US **63.49**). In stock 2026-09-07.
>
> Covered by `LilyGo-AMOLED-Series` @ **`6d1dc008b94578cc34ba4a0f3b223dd808ca963f`**.
> Research retrieved 2026-09-07. **Depth: medium.** No hardware.
> Part of the [T-Display-S3 family](../t-display-s3-shared/README.md) by library and lineage,
> not by name.

## Identity

| | | Source |
|---|---|---|
| Panel | 2.41″ AMOLED, **450 × 600**, **550 nits** — the brightest and largest in the family | `LilyGo-AMOLED-Series` README @ `6d1dc00` |
| Display driver | **Raydium RM690B0** | vendor datasheet `RM690B0 DataSheet_V0.2.pdf` ships in the repo |
| Touch | **Hynitron CST226SE** | vendor README links the CST226 manual |
| PMIC `U5` | **Silergy SY6970** | schematic designator census |
| SoC `U2` | **ESP32-S3R8**, 16 MB flash (`U3` W25Q128), 8 MB OPI PSRAM | schematic + README |
| Other silicon | `SY8089` buck, `BV6804` (unidentified family), `ULC0511C`, `AO3400` FET, `LTR`-marked ambient-light part | schematic designator census |
| Storage | **microSD**, SPI: `GPIO1 SD_CS`, `GPIO2 SD_MOSI`, `GPIO3 SD_SCK`, `GPIO4 SD_MISO` (net labels drawn on the sheet) | schematic |
| Component records | [`raydium/rm690b0`](../../../components/raydium/rm690b0/README.md) · [`hynitron/cst226se`](../../../components/hynitron/cst226se/README.md) · [`silergy/sy6970`](../../../components/silergy/sy6970/README.md) |

## Pinout

From `LilyGo-Display-IDF/main/product_pins.h`, block `#elif CONFIG_LILYGO_T4_S3_241`
@ **`b1a1cc54994bf1b417e3bb30c437bbe1036bff7f`**:

| Signal | GPIO |
|---|---|
| `DISP_CS` / `SCK` | 11 / 15 |
| `DISP_DATA0..3` | 14, 10, 16, 12 |
| `DISP_RESET` | 13 |
| `DISP_TE` | −1 (not wired) |
| `I2C_SDA` / `SCL` | 6 / 7 |
| `TOUCH_IRQ` / `TOUCH_RST` | 8 / 17 |
| `SD_MISO/MOSI/SCLK/CS` | 4 / 2 / 3 / 1 |
| `BOOT` / `BUTTON1` | 0 / 0 |

**ESPHome disagrees on the QSPI pins.** Its `T4-S3` model gives
`cs_pin=11, reset_pin=13, enable_pin=9, offset_width=16, width=450` — `cs` and `reset` match,
but it adds an `enable_pin=9` that `product_pins.h` does not mention, and `offset_width=16`
(the RM690B0 is 480 wide; 450 sits at column 16). Recorded as a conflict below.

**⚠ Vendor warning, verbatim from the library README:**
> "`T4-S3` **GPIO18** has been assigned to the display TE Pin, please do not use this Pin"

— which contradicts `product_pins.h`'s `BOARD_DISP_TE (-1)`. Two vendor sources, one file and
one README, disagree about whether TE is wired.

## Software

- **`LilyGo-AMOLED-Series`** auto-detects it. `examples/PPM_Example_for_T4S3` is the
  SY6970 example; `TFT_eSPI_Sprite_Rotation` and `LVGL_Rotation` note that hardware rotation is
  available "only for 1.91, 2.41 inches" — i.e. this board and the 1.91″ AMOLED, not the Lite.
- **ESPHome**: model `T4-S3`, extending `RM690B0`, `bus_mode=QUAD`, `requires psram`.
- `TFT_eSPI` cannot drive it (QSPI).

## Power

Vendor figures @ `6d1dc00`: **90–230+ mA** active, **≈230 µA** deep sleep with GPIO0 wake.

## Artifacts

`artifacts/schematic/T4-S3-240719.pdf` — 530 032 B,
SHA-256 `3d3831d215eb5e89c354c8a3677c929c98f6675e5be51d10a15997b3d90f79b3`, retrieved 2026-09-07
at `6d1dc00`. The filename's `240719` is a **2024-07-19** date stamp.

**A note on reading it.** This PDF uses Type0/Identity-H subset fonts with `/ToUnicode` CMaps —
unlike every other LilyGO schematic, which use WinAnsi TrueType. A text extractor that works on
the others returns **nothing** here. Recorded in
[`vendors/lilygo/README.md`](../../../vendors/lilygo/README.md).

RM690B0 and CST226 datasheets are filed under their components.

## Sources

| ID | Source | Class | Retrieved |
|---|---|---|---|
| T4-1 | `LilyGo-AMOLED-Series` README.MD @ `6d1dc00` | primary | 2026-09-07 |
| T4-2 | `schematic/T4-S3-240719.pdf` @ `6d1dc00` | primary | 2026-09-07 |
| T4-3 | `LilyGo-Display-IDF/main/product_pins.h` @ `b1a1cc5` | primary | 2026-09-07 |
| T4-4 | `esphome/components/mipi_spi/models/amoled.py`, `dev` | primary (third-party) | 2026-09-07 |
| T4-5 | LilyGO store feed | primary | 2026-09-07 |

## Conflicts

| # | Item | Status |
|---|---|---|
| T4-C1 | **Is TE wired?** README says GPIO18 is the display TE and must not be used; `product_pins.h` says `BOARD_DISP_TE (-1)` | **Unresolved.** Safest reading: treat GPIO18 as reserved |
| T4-C2 | **`enable_pin=9`** appears in ESPHome and in no vendor source | **Unresolved** |
| T4-C3 | `BV6804`, `ULC0511C` unidentified | **Open** |
| T4-C4 | The name. Marketed as *T4-S3*; grouped with T-Display-S3 boards by library, README table and lineage | recorded, not a defect |

## Gaps

Medium-depth stub: no `features/`, no example catalogue, no acquisition manifest, no GPIO
census beyond the display/touch/SD block above. Net connectivity not traced. No hardware.
