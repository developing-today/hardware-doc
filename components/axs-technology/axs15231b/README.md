# AXS Technology AXS15231 / AXS15231B

- **Category:** **combined display driver and capacitive touch controller in one die** —
  the display side takes pixels over QSPI/SPI/MIPI; the touch side answers over I²C.
- **Manufacturer:** **AXS Technology Corp.** — established from the datasheet's own cover page
  and copyright notice, not inferred.
- **Retrieved:** 2026-09-07

The controller of the **LilyGO T-Display-S3 Long**'s 3.4″ 180 × 640 bar display. Integrating
the digitiser into the display driver is unusual and is the board's defining characteristic.

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **AXS15231** (LilyGO and every driver write it **AXS15231B**) | datasheet title page |
| Datasheet version | **V0.4**, dated **2022-11-08** | cover page, read directly |
| Copyright notice | *"The information contained herein is the exclusive property of **AXS Technology Corp.** and shall not be distributed, reproduced, or disclosed in whole or in part without prior written permission of AXS Technology Corp."* | cover page, read directly |
| Local artifact | [`artifacts/axs15231-datasheet-v0.4-20221108-lilygo-mirror.pdf`](artifacts/axs15231-datasheet-v0.4-20221108-lilygo-mirror.pdf) — 8 808 542 B, SHA-256 `61281aff757afeda3ae6fd75267439b8b841d5019e0190e47380be9eb613cff4` |
| Mirror source | `Xinyuan-LilyGO/T-Display-S3-Long` → `datasheet/AXS15231_Datasheet_V0.4_20221108.pdf` @ `37a7e83af79a98bb395012200f811777e52b9cfc` |
| Touch note | [`artifacts/axs15231b-touch-register-note-20240719-lilygo.pdf`](artifacts/axs15231b-touch-register-note-20240719-lilygo.pdf) — 63 044 B, SHA-256 `7e9d8c3fa2302fed51b60bd08c9f3ac65cdee7625db7c98cf15a8f46fcff50ef` |

> ⚠ **Redistribution.** The cover page carries an explicit no-distribution notice, quoted above.
> The copy is retained here because it is a **unique, hard-to-obtain document** — AXS Technology
> publishes no open portal and no other copy was located — and because the research method
> requires acquiring before judging. **Redistribution status: `prohibited` on the face of the
> document.** It should remain **unstaged** pending a decision by the repository owner.
> The [`components/README.md`](../../README.md) index should not link it as freely
> redistributable.

## 2. The touch interface — command-framed, not a register map

LilyGO ships a two-page note, `T-Display-S3-Long_AXS15231B_Touch_Register.pdf`
("Modified on: 2024.07.19"), whose text reads (extracted and cross-checked two ways):

> "Initialize touch IIC: IIC device **`0x3B`**, touch reset, set external interrupt. …
> Waiting for external interrupt to trigger. … Write touch commands and read touch data. …
> Processing touch data (**take touching the fingers to count 1 and event `0x08` together as
> the trigger flag**). …
> Write the command to read touch information: continuously write the following formatted
> command data to the touch IIC address `0x3B`."

Three things follow, and all three catch people:

1. **The I²C address is `0x3B`.**
2. **You do not read a register — you write a formatted command block and then read a
   response.** This is why generic touch libraries do not work with it.
3. **A valid touch requires *both* a finger count of 1 *and* event code `0x08`.** Treating
   either alone as a touch produces spurious events. This is stated once, in a two-page PDF,
   in slightly awkward English, and it is the single most important line about this part.

## 3. Display interface as used

| Property | Value | Source |
|---|---|---|
| Bus | **QSPI** | `pins_config.h` @ `37a7e83` |
| Clock | 32 MHz, mode 0, `SPI2_HOST` | same |
| Resolution | 180 × 640 | vendor README |
| Transfer chunk | `SEND_BUF_SIZE (28800/2)` RGB565 | `pins_config.h` |
| Driver | `Arduino_GFX` with an AXS15231B init; the repo vendors `Arduino_GFX-1.3.7` | tree listing |
| `TFT_eSPI` | **cannot drive it** — no QSPI transport | — |
| ESPHome | **no model exists** for this controller as of 2026-09-07 | `esphome/components/mipi_spi/models/` |

## 4. What was verified, and how

The cover page **was** read, and the extraction was validated: two independent extraction
routes (a WinAnsi/Form-XObject reader and a Type0/ToUnicode CMap reader) were run against the
family's PDFs, and the AXS15231 cover produced consistent, legible English through the first.
That matters because a sibling document in this pass (Chipone's CO5300) has a **uniform +0x1D
code-point offset** that yields human-legible but wrong text — see
[`vendors/lilygo/README.md`](../../../vendors/lilygo/README.md).

**Not read:** the register map, timing specifications, electrical characteristics, or the
display command set. No numeric value beyond the I²C address and event code is transcribed
into this record.

## 5. Gaps

- Register map and display command set not extracted.
- Whether **AXS15231** (datasheet) and **AXS15231B** (every driver and LilyGO) are the same die
  or a revision is **not established**.
- The full touch command block format is described only by prose and a flowchart in the
  two-page note; the byte-level format was not transcribed.
- No hardware.

## 6. Used by

### LilyGO T-Display-S3 Long
→ [`devices/lilygo/t-display-s3-long`](../../../devices/lilygo/t-display-s3-long/README.md)

Sole display driver **and** the original touch controller. QSPI on GPIO 12 (CS), 17 (SCK),
13/18/21/14 (D0–D3), 16 (RST); backlight GPIO1 via a PT4103B23F boost. Touch I²C on
GPIO15 (SDA) / GPIO10 (SCL) at address `0x3B`, with `TP_RST` GPIO2 and `TP_IRQ` GPIO11.

**Later production adds or substitutes a discrete
[Hynitron CST3530](../../hynitron/cst3530/README.md)** — the repository's default branch is
`T-Display-S3-Long-cst3530` and two factory images ship. See
[R5](../../../devices/lilygo/t-display-s3-shared/board-revision-drift.md#r5--t-display-s3-long-cst3530-touch-appears-mid-life-in-a-branch).
