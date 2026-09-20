# LilyGO T-Display-S3 AMOLED 1.64″ (sold as "T-Display S3 AMOLED (DS)")

> **Product:** store handle **`t-display-s3-amoled-1-64`**, title *T-Display S3 AMOLED (DS)*,
> published **2024-07-18**. That one page sells **four different panels**; this record covers
> the **1.64″**, SKU `H708`, **USD 22.99** (in stock 2026-09-07). The 1.43″ and 1.75″ are
> [a separate record](../t-display-s3-amoled-1-43-1-75/README.md) with a separate repository.
>
> Repo `T-Display-S3-AMOLED-1.64` @ **`e236a4dfb3295c473d8ac7c240cbea93313707c0`**,
> **default branch `arduino-esp32-libs_V2.0.14`** — not `main`.
> Licence **GPL-3.0**. Research retrieved 2026-09-07. **Depth: medium.** No hardware.

## Identity

| | | Source |
|---|---|---|
| Panel | 1.64″ AMOLED, **280 × 456** | repo README @ `e236a4d` |
| Display driver | **ICNA3311 (CO5300)** — the README writes both names | repo README |
| CO5300 maker | **Chipone Technology (Beijing) Co., Ltd.** — established from the datasheet cover, decoded through a code-point-offset text layer and confirmed two ways | `information/CO5300_V0.01.pdf` |
| Touch | **FocalTech FT3168**, I²C | repo README + `information/FT3168.pdf` |
| PMIC | **Silergy SY6970**, I²C | repo README; `examples/SY6970`, `examples/SY6970_OTG` |
| SoC | ESP32-S3R8, **16 MB flash, 8 MB OPI PSRAM** | repo README |
| Panel spec | `SPEC-DO0164FMST02-20240126.pdf` ships in `information/` | tree listing |
| Component records | [`chipone/co5300`](../../../components/chipone/co5300/README.md) · [`focaltech/ft3168`](../../../components/focaltech/ft3168/README.md) · [`silergy/sy6970`](../../../components/silergy/sy6970/README.md) |

## The naming problem

The store page title is **"T-Display S3 AMOLED (DS)"**. "DS" is not explained anywhere. The
same page sells:

| SKU | Panel | USD 2026-09-07 |
|---|---|---|
| `H708` | **1.64 inch** | 22.99 |
| `H741` | 1.43 inch | 23.99 |
| `H741-01` | 1.75 inch | 27.86 |
| `H741-02` | 1.75 inch **half-circle convex mirror** | 30.25 |

…and two different GitHub repositories cover them, with different display controllers and
different touch controllers. **Buying "T-Display S3 AMOLED (DS)" without specifying the SKU
tells you nothing about what arrives.**

## Toolchain — pinned, and visible in the branch name

The default branch is literally called **`arduino-esp32-libs_V2.0.14`**, and the README's
example table repeats per example:
`[Platformio IDE][espressif32-v6.5.0]` / `[Arduino IDE][esp32_v2.0.14]`.
Board settings: `QIO 80MHz`, `16MB (128Mb)`, `16M Flash (3MB APP/9.9MB FATFS)`, `OPI PSRAM` —
the family standard.

## Examples

`FT3168` (touch), `GFX_FT3168_Image`, `SY6970` (PMU), `SY6970_OTG`, `Lvgl_benchmark`.
The **`Lvgl_benchmark`** is notable: it exists here and **not** in the base-board repo, so this
is the only board in the family with a vendor LVGL benchmark.

## Firmware

`firmware/` holds deep-sleep and light-sleep wake-up images plus a `deprecated/` directory with
seven more, including a Wi-Fi iperf image and a screen colour test. Filenames use bracketed
tags: `[T-Display-S3-AMOLED-1.64_V1.0][Deep_Sleep_Wake_Up]_firmware_V1.0.0.bin`.
**None retrieved by this pass.**

## Sources

| ID | Source | Class | Retrieved |
|---|---|---|---|
| S64-1 | repo README.md @ `e236a4d` | primary | 2026-09-07 |
| S64-2 | `information/CO5300_V0.01.pdf` (13 236 092 B) | credible mirror | 2026-09-07 — **archived**, see [`components/chipone/co5300/artifacts/`](../../../components/chipone/co5300/artifacts/) |
| S64-3 | `information/FT3168.pdf` (926 072 B) | credible mirror | 2026-09-07 → [`components/focaltech/ft3168/artifacts/`](../../../components/focaltech/ft3168/artifacts/) |
| S64-4 | LilyGO store feed | primary | 2026-09-07 |

## Gaps

- **Medium-depth stub.** No pinout table: `boards/esp32s3_flash_*.json` exist but **no
  `pin_config.h` was found in this repository** — the pin map for the 1.64″ was **not
  established** by this pass. That is the biggest single gap here.
- No schematic is published for this board. Searched the full tree at `e236a4d`; there is no
  `schematic/` directory. **This is the only board in the family with no published schematic.**
- Firmware not retrieved; `SPEC-DO0164FMST02` panel spec not retrieved.
- The relationship between `ICNA3311` and `CO5300` (same die? rebadge? successor?) is
  **unresolved** — LilyGO writes "ICNA3311(CO5300)" and the datasheet says only CO5300.
