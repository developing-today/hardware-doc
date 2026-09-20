# Soldered Inkplate 5 Gen 2

> 5.2" **1280 × 720** e-paper development board, ESP32-WROVER. Hardware design rev **V1.1.0**, TAPR OHL.
> Arduino board target: **`Inkplate5V2`**. Research snapshot **2026-08-24**.

**The full technical record for both generations lives in [`../inkplate-5/README.md`](../inkplate-5/README.md).** This page exists so the Gen 2 is findable by name and records what is specific to it.

> **Note on scope:** this generation was documented from primary design files and library source, but **no physical unit was available** and it was researched as the display platform underneath [ZeroWriter Ink](../../zerowriter/zerowriter-ink/README.md) rather than as a board in its own right. Treat this as a solid overview, not an exhaustive record.

## What is different from the Inkplate 5

Exactly one component. Both BOMs were parsed and compared designator-by-designator:

| | Inkplate 5 | **Inkplate 5 Gen 2** |
|---|---|---|
| Panel | `ED052TC2` *(no component record)* | **[`ED052TC4`](../../../components/e-ink/ed052tc4/README.md)** |
| Resolution | 960 × 540 (518,400 px) | **1280 × 720 (921,600 px)** |
| Pixel count | — | **+78 %** at the same 5.2" diagonal |
| Design rev | V1.2.0 | V1.1.0 |
| Arduino define | `ARDUINO_INKPLATE5` | `ARDUINO_INKPLATE5V2` |

Identical: **[ESP32-WROVER](../../../components/espressif/esp32-wrover/README.md)**,
[`TPS65186RGZ`](../../../components/texas-instruments/tps65186/README.md) EPD PMIC,
[`PCAL6416AHF`](../../../components/nxp/pcal6416a/README.md) I/O expander @ 0x20,
[`PCF85063A`](../../../components/nxp/pcf85063a/README.md) RTC,
[`CH340C`](../../../components/wch/ch340c/README.md) USB-UART, `MCP73831T` charger,
`TPS7A2633` LDO, `TPS3840` supervisor, `SN74LVC1G34`, `MC14093B`, NTC temperature sense,
[microSD](../../../components/generic/micro-sd-sdmmc/README.md), easyC/Qwiic connector.

Parts named without a link have **no record** under [`components/`](../../../components/README.md) —
see [the Inkplate 5 BOM table](../inkplate-5/README.md#complete-bill-of-materials-inkplate-5-v120).

Designator numbering shifts slightly between the two (the ESP32 is `U10` on the Inkplate 5 and `U11` on the Gen 2; the panel is `U11` then `U9`), so do not match parts across the two BOMs by reference designator alone.

Resolutions confirmed from `Inkplate-Arduino-library/src/boards/Inkplate5V2/waveforms.h`:

```c
#define E_INK_WIDTH  1280
#define E_INK_HEIGHT 720
```

## Pin map verified identical to the Inkplate 5

**Verified 2026-08-24** by netlist-parsing the Gen 2's own `.kicad_pcb` and diffing the ESP32-WROVER pad-to-net mapping against the Inkplate 5. **All 36 connected pads carry the same net names.** The Gen 2 is genuinely a panel swap — the processor wiring is untouched.

Full pin table: [`../inkplate-5/pinouts-and-buses.md`](../inkplate-5/pinouts-and-buses.md). It applies to this board without modification.

The same comparison against **ZeroWriter's respun variant** also shows an identical ESP32 pin map — see [§ ZeroWriter compatibility](#zerowriter-compatibility).

## Why the higher resolution costs you something

The [ESP32-WROVER](../../../components/espressif/esp32-wrover/README.md)'s PSRAM is what makes this panel viable — a 1280 × 720 buffer is 921,600 px, which at 1 bit per pixel is 115 KB and at 4 bits (greyscale) is **450 KB**. The Arduino driver allocates both a `_partial` 1-bit buffer and a `DMemory4Bit` greyscale buffer:

```c
memset(_partial,    0,   E_INK_WIDTH * E_INK_HEIGHT / 8);   // 115,200 B
memset(DMemory4Bit, 255, E_INK_WIDTH * E_INK_HEIGHT / 2);   // 460,800 B
```

That is comfortably beyond the ESP32's internal RAM and is why every Inkplate uses a **WROVER** (PSRAM) module rather than a WROOM. It also means refresh times are longer than the Inkplate 5's — more data to clock out over the same I2S1 parallel bus.

## ZeroWriter compatibility

[ZeroWriter Ink](../../zerowriter/zerowriter-ink/README.md) ships a **respun** version of this board. Diffing the ESP32-WROVER net map between Soldered's stock Gen 2 and ZeroWriter's variant:

**Every connected pad is identical.** The only differences are cosmetic labels on the six *unconnected* module pads:

| Pad | Soldered | ZeroWriter |
|---|---|---|
| 17–22 | `unconnected-(U11-Pad17…22)` | `unconnected-(U11-SD2/SD3/CMD/CLK/SD0/SD1-Pad…)` |

ZeroWriter's naming is more informative and confirms what those pads are: the WROVER's **SDIO/flash interface** (`SD0`–`SD3`, `CMD`, `CLK`), brought out on the module footprint but unusable.

**Practical conclusion: firmware targeting a stock Inkplate 5 Gen 2 will find the same pins on a ZeroWriter Ink main board.** The Inkplate Arduino library applies. What differs is *off*-processor — charging (switch-mode [`BQ25306`](../../../components/texas-instruments/bq25306/README.md) vs linear `MCP73831T`), [USB-C](../../../components/generic/usb-c-interface/README.md) and [microSD](../../../components/generic/micro-sd-sdmmc/README.md) relocated to a breakout PCB, and an added 16-pin inter-board connector.

## Known uses

- **[ZeroWriter Ink](../../zerowriter/zerowriter-ink/README.md)** — ships a *respun* variant of this board with a switch-mode [`BQ25306`](../../../components/texas-instruments/bq25306/README.md) charger replacing the linear `MCP73831T`, [USB-C](../../../components/generic/usb-c-interface/README.md) and [microSD](../../../components/generic/micro-sd-sdmmc/README.md) relocated to a separate breakout PCB, and a 16-pin inter-board connector added. The panel, processor, PMIC, expander and RTC are unchanged, so the Inkplate Arduino library applies. Note the Ink also carries a **second processor** — an [ESP32-WROOM-32U](../../../components/espressif/esp32-wroom-32u/README.md) on its keyboard PCB — which has no counterpart on this board.

## Artifacts

```
artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/   TAPR OHL
                                                commit 7450a321 (2025-03-08)
├── CAD/V1.1.0/       KiCad hierarchical sheets + .kicad_pcb + panel
├── OUTPUTS/V1.1.0/   BOM.csv, Schematics.pdf, iBOM.html, gerbers, 3D .step
└── OUTPUTS/Compliance/  CE, UKCA, safety sheets
```

Software, examples and the full e-paper interface description are shared with the Inkplate 5 — see [`../inkplate-5/README.md`](../inkplate-5/README.md) and [Peripheral Mode](../inkplate-5/features/peripheral-mode.md).

## Related

- [Source manifest](sources.md) — Gen-2-specific sources; the shared base is in [`../inkplate-5/sources.md`](../inkplate-5/sources.md)
- [Inkplate 5 (both generations, full record)](../inkplate-5/README.md) · [its component index](../inkplate-5/README.md#component-records)
- [Pinouts and buses](../inkplate-5/pinouts-and-buses.md) — verified to apply to this board unmodified
- [Soldered Electronics vendor guide](../../../vendors/soldered-electronics/README.md)
- [ZeroWriter Ink](../../zerowriter/zerowriter-ink/README.md)
- [Component index](../../../components/README.md) · [Device index](../../README.md)
