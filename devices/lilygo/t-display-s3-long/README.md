# LilyGO T-Display-S3 Long (3.4″ bar)

> **Product:** T-Display S3 Long · store handle `t-display-s3-long` · published **2023-10-27** ·
> SKUs `H685` basic **USD 29.35**, `H721` with shell **USD 32.13**, both in stock 2026-09-07.
>
> **Repository default branch is `T-Display-S3-Long-cst3530`, not `main`.** That is not a typo —
> it is how LilyGO shipped a touch-controller change. Commit **`37a7e83af79a98bb395012200f811777e52b9cfc`**.
>
> Research retrieved **2026-09-07**. No hardware. Part of the
> [T-Display-S3 family](../t-display-s3-shared/README.md).

## Identity

| | |
|---|---|
| Panel | 3.4″ bar, **180 × 640** |
| Controller | **AXS15231B** — **display driver and touch controller in one die**, QSPI + I²C |
| Manufacturer | **AXS Technology Corp.** (established from the datasheet cover, not guessed) |
| Alternate touch | later boards add/substitute a discrete **Hynitron CST3530** — see below |
| SoC | ESP32-S3R8, 16 MB flash, 8 MB OPI PSRAM |
| PMIC | **Silergy SY6970** (`U6`) — a real I²C charger/PMIC, unlike the base board's dumb linear charger |
| Backlight | **PT4103B23F** boost (`U5`) |
| Unique feature | a **hardware slide switch** (`SW1` = `MSK12C02-HB`) — the only board in the family with a physical power switch |
| Component records | [`axs-technology/axs15231b`](../../../components/axs-technology/axs15231b/README.md) · [`hynitron/cst3530`](../../../components/hynitron/cst3530/README.md) · [`silergy/sy6970`](../../../components/silergy/sy6970/README.md) · [`espressif/esp32-s3r8`](../../../components/espressif/esp32-s3r8/README.md) |

## Why this board is interesting

**One die drives the panel and reads the touch.** The AXS15231B takes pixels over QSPI and
answers touch queries over I²C at address **`0x3B`** — a command-framed protocol rather than a
conventional register map. LilyGO ships a dedicated note for it:
`examples/GFX_AXS15231B_Image/T-Display-S3-Long_AXS15231B_Touch_Register.pdf`
(63 044 B, "Modified on: 2024.07.19"), which describes the sequence as:

> "Initialize touch IIC: IIC device `0x3B`, touch reset, set external interrupt. … Write the
> command to read touch information: continuously write the following formatted command data to
> the touch IIC address `0x3B`. … Take touching the fingers to count 1 and event `0x08` together
> as the trigger flag."

That last sentence is the operative one and is easy to miss: **a valid touch requires both the
finger count and event code `0x08`**, not either alone.

## Pinout

From `examples/factory/pins_config.h` @ `37a7e83`:

| Signal | GPIO |
|---|---|
| `TFT_QSPI_CS` / `SCK` | 12 / 17 |
| `TFT_QSPI_D0..D3` | 13, 18, 21, 14 |
| `TFT_QSPI_RST` | 16 |
| `TFT_BL` | 1 |
| `TP_RST` / `TP_IRQ` | 2 / 11 |
| `I2C_SDA` / `I2C_SCL` | 15 / 10 |
| `SPI_SD_CS/MOSI/MISO/SCLK` | 38 / 39 / 41 / 40 |
| `PIN_BUTTON_1` | 0 |

SPI clock **32 MHz**; `SEND_BUF_SIZE 28800/2` (RGB565).

### Two defects in that file — do not copy it blindly

```c
#define TFT_QSPI_D2   21     …   #define PIN_BUTTON_2   21     ← collision
#define TP_RST         2     …   #define PIN_BAT_VOLT    2     ← collision
```

Both are copy-paste residue from the AMOLED board's header (where `PIN_BUTTON_2 21` and
`PIN_BAT_VOLT 4` are correct). **`PIN_BUTTON_2` and `PIN_BAT_VOLT` are wrong for this board and
must not be used.** GPIO21 is a display data line; GPIO2 is the touch reset.

Battery voltage on this board is read **from the SY6970 over I²C**, not from an ADC — which is
why no correct `PIN_BAT_VOLT` exists. That is an upgrade over the base board: a real
fuel-gauge-adjacent path with charge status, input current limit and OTG control.

## The CST3530 branch

The repository's **default branch is `T-Display-S3-Long-cst3530`** and it ships **two factory
images**:

| Image | Bytes |
|---|---|
| `firmware/factory.bin` | 1 815 872 |
| `firmware/factory-cst3530.bin` | 2 158 624 |

plus `examples/cst3530_touch/` beside the original AXS15231B touch path, and a
`CST3530数据手册V1.0` datasheet. **Reading:** later production substitutes or adds a discrete
Hynitron CST3530 touch controller. LilyGO handled it by making that branch the default rather
than merging. **How to tell:** flash `factory.bin`; if touch does not respond, flash
`factory-cst3530.bin`. See
[revision R5](../t-display-s3-shared/board-revision-drift.md#r5--t-display-s3-long-cst3530-touch-appears-mid-life-in-a-branch).

## Software

| Route | Status |
|---|---|
| **`Arduino_GFX`** | LilyGO's own choice; the repo vendors `Arduino_GFX-1.3.7` |
| `TFT_eSPI` | **cannot drive it** — QSPI |
| ESPHome | **no model for this board** in `mipi_spi` as of 2026-09-07. AMOLED, base and Pro have models; Long does not |
| LVGL | `examples/lvgl_demo` |

## Power and current

LilyGO's own table @ `37a7e83`: **90–350+ mA** active at 240 MHz with Wi-Fi (notably higher than
the AMOLED boards' 230 mA ceiling — the bar panel and its boost backlight cost real power), and
**≈1.1 mA** deep sleep with GPIO wake. That 1.1 mA is **five times** the AMOLED boards' 230 µA;
this is not a good board for a long-running battery device.

## Two schematics

`T-Display-S3-Long-3.4-V1.0.pdf` (330 477 B, `7ca6e7037f67c844…`) and
`T-Display-S3-Long-3.4-with-SD-slot.pdf` (341 862 B, `157ef432daaefb8f…`). **The SD-slot version
is a second board variant**, and the SPI SD pins in `pins_config.h` (GPIO38–41) belong to it.
Whether the `H685`/`H721` SKUs ship with or without the slot is **not established** — the store
does not say.

## Artifacts

Both schematics retained under `artifacts/schematic/`, retrieved 2026-09-07 at `37a7e83`.
The **AXS15231B datasheet (8.8 MB, V0.4, 2022-11-08)** and its touch-register note are filed
under [`components/axs-technology/axs15231b/artifacts/`](../../../components/axs-technology/axs15231b/artifacts/);
CST3530 under [`components/hynitron/cst3530/artifacts/`](../../../components/hynitron/cst3530/artifacts/);
SY6970 under [`components/silergy/sy6970/artifacts/`](../../../components/silergy/sy6970/artifacts/).

## Gaps and conflicts

See [`gaps-and-conflicts.md`](gaps-and-conflicts.md). The repo has **25 open issues**, the most
of any board in the family — proportionally far more than the base board's 1 open of 318 — which
is itself a signal about maturity.
