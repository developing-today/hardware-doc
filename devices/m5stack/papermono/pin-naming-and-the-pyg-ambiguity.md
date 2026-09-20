# PaperMono pin naming: why `PYG3` means two different things

> **Status:** resolved from primary evidence (official schematic), 2026-09-01.
> This document exists because three independent readings of the vendor
> documentation reached three different conclusions, two of them wrong. The
> underlying fact is small and the consequence is not: acting on the wrong
> reading of `PYG3` cuts power to the e-paper panel instead of dimming the
> frontlight.

Related: [`pinouts-and-buses.md`](pinouts-and-buses.md) ·
[`components/m5stack/m5pm1`](../../../components/m5stack/m5pm1/README.md) ·
[`components/m5stack/m5ioe1`](../../../components/m5stack/m5ioe1/README.md) ·
[`gaps-and-conflicts.md`](gaps-and-conflicts.md)

## The short version

The PaperMono carries **two** M5Stack custom chips, and the schematic uses the
`PYG` prefix for **both** — but at different layers of the drawing.

| Chip | `PYG<n>` appears as | The other layer is |
|---|---|---|
| **M5IOE1** (I/O expander, I²C `0x4F`) | the **symbol pin name** — `PYG1` … `PYG14` | net names, which are `PYB_<function>` |
| **M5PM1** (power management, I²C `0x6E`) | the **net name** — `PYG0_RTC_INT`, `PYG2_LoRa_EN`, `PYG3_BL_PWM`, `PYG4_IMU_INT` | symbol pin names, which are `G<n>_WAKEin(...)_IRQout_<cap>` |

The convention is *inverted* between the two chips. So the bare token `PYG3`
denotes an M5IOE1 **pin** and an M5PM1 **net**, in the same document, and they
are not the same signal:

| Token | On M5IOE1 it is | On M5PM1 it is |
|---|---|---|
| `PYG2` | pin 11 → `PYB_LoRa_ANT_SW` (LoRa antenna switch) | pin 20 → `PYG2_LoRa_EN` (LoRa rail enable) |
| `PYG3` | pin 14 → `PYB_EPD_EN` (**e-paper 3.3 V rail enable**) | pin 13 → `PYG3_BL_PWM` (**frontlight brightness PWM**) |
| `PYG4` | pin 16 → `PYB_NFC_EN` (NFC enable) | pin 12 → `PYG4_IMU_INT` (IMU wake interrupt) |

`PYG0` exists only on the M5PM1 — the M5IOE1's pins start at `PYG1`, and its
Arduino library has no `PIN_0` constant. `PYG5`–`PYG14` exist only on the
M5IOE1. The collision is confined to `PYG2`, `PYG3` and `PYG4`.

## Evidence

Recovered from the official schematic
[`artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf`](artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf)
using [`tools/altium_pdf_pin_table.py`](../../../tools/altium_pdf_pin_table.py),
which pairs Altium's invisible `PI<designator><pin>` markers with the
human-readable text sharing their row. Evidence status: `executed-success`
(the extraction was run; the readings below were then checked against the
rendered sheet).

**M5PM1 — designator `U7`, sheet 2.** Symbol pin name on the left, attached net
on the right:

| Pin | Symbol pin name | Net |
|---|---|---|
| 3 | `G0_WAKEin(INT0/2)_IRQout_NEOPIXEL` | `PYG0_RTC_INT` |
| 12 | `G4_WAKEin(INT3/4)_IRQout_PWM` | `PYG4_IMU_INT` |
| 13 | `G3_WAKEin(INT3/4)_IRQout_PWM` | `PYG3_BL_PWM` |
| 17 | `G1_IRQout_ADC` | `G1_PY_IRQ` |
| 20 | `G2_WAKEin(INT0/2)_IRQout_ADC` | `PYG2_LoRa_EN` |

Note pin 17: its net is `G1_PY_IRQ`, **not** `PYG1_…`. The M5PM1 net prefix is
not applied consistently even within its own symbol — which is part of why the
pattern is easy to miss.

**M5IOE1 — designator `U17`, sheet 4.** The relationship is the other way round:

| Pin | Symbol pin name | Net |
|---|---|---|
| 7 | `PYG1` | `PYB_TF_DET` |
| 11 | `PYG2_ADC1` | `PYB_LoRa_ANT_SW` |
| 12 | `PYG8_PWM2` | `PYB_LED_G` |
| 13 | `PYG9_PWM1` | `PYB_LED_B` |
| 14 | `PYG3` | `PYB_EPD_EN` |
| 15 | `PYG13` | `PYB_TP_EN` |
| 16 | `PYG4_ADC2` | `PYB_NFC_EN` |
| 17 | `PYG5_ADC3` | `PYB_EINK_RST` |
| 18 | `PYG6` | `PYB_TP_RST` |
| 19 | `PYG7_ADC4` | `ADD_SET` |
| 20 | `PYG10_PWM4` | `PYB_LoRa_RST` |
| 10 | `PYG11_PWM3` | `PYB_CHG_IIC` |
| 5 | `PYG12` | `PYB_PDM_EN` |
| 3 | `PYG14` | `PYB_TF_EN` |

The `_ADC<n>` and `_PWM<n>` suffixes match the M5IOE1 manual's channel tables
position for position, which independently confirms that `PYG<n>` on this symbol
is the expander's `IO<n>`.

## Where the prefix comes from

Schematic sheet 1 lists the board's device classes, and gives both custom chips
the same underlying part: **`PY32L020F15U6`**, annotated `PY32L020F15U6_IIC` — a
Puya PY32 Cortex-M0+ microcontroller running M5Stack firmware, not an ASIC. See
[`components/puya/py32l020f15u6`](../../../components/puya/py32l020f15u6/README.md).

`PY` is therefore *the die*, not *the role*, and `PYG<n>` reads as "PY32 GPIO n".
Applying that prefix to two different PY32s in one design is what produces the
ambiguity. `PYB_*` appears to be the companion prefix for signals crossing out of
a PY32 into the rest of the board, but M5Stack does not document either
convention, so this reading is `inferred`.

## What the vendor documentation actually says — a correction

An earlier pass in this research session concluded that the vendor's PaperMono
product page was **defective** where it says the frontlight is driven by
"`PYG3_BL_PWM` of the M5PM1", on the reasoning that `PYG` is an M5IOE1-only
prefix (the M5PM1 Arduino library defines only `M5PM1_GPIO_NUM_0…_4` and no
`PYG` identifier appears in it). It further concluded that the PaperMono-Lite
page, which calls the same pin "`G3_WAKEin` of M5PM1", was the correct one.

**That conclusion is refuted.** The schematic shows `PYG3_BL_PWM` is a real net
name on M5PM1 pin 13. Both vendor pages are correct; they simply quote different
layers of the same drawing — the PaperMono page quotes the net name, the
PaperMono-Lite page quotes the symbol pin name. The Arduino library is a third
naming system again, and its silence about `PYG` is evidence about the library,
not about the schematic.

Recorded here per the evidence rules: a refuted hypothesis is written down with
what refuted it and the date, so it is not re-investigated. Date of refutation
2026-09-01; refuting artifact `PaperMono_SCH_V0.6.2_20260522.pdf`, sheets 2 and 4.

The vendor documentation is, on this point, **already correct**. The defect is
in its ambiguity, not its accuracy.

## The practical hazard

Both readings of `PYG3` are live pins that do something, so a mistake is silent
rather than inert:

- Intending **frontlight brightness** and writing to **M5IOE1 IO3** removes the
  e-paper panel's 3.3 V supply. The display stops updating; nothing reports an
  error.
- Intending **e-paper power** and writing to **M5PM1 G3** changes backlight
  brightness and leaves the panel powered.

A second, independent off-by-one compounds this. In the vendor Arduino
libraries the two chips number their pins differently:

- `M5IOE1_PIN_3 = 2` — the label is 1-based, the enum value 0-based
- `M5PM1_GPIO_NUM_3 = 3` — label and value agree

So passing a documentation "`PYG<n>`" straight into the M5IOE1 API reaches pin
*n+1*. See the warning sections in the two component records for the exact
`file:line` citations.

## Recommendation

Never write `PYG<n>` without naming the chip. In this knowledge base the
convention is:

- **`M5PM1.G3`** for the power-management chip's GPIO 3 (frontlight PWM)
- **`M5IOE1.IO3`** for the expander's IO 3 (e-paper rail enable)

and the raw schematic tokens are quoted only when citing the schematic directly.
