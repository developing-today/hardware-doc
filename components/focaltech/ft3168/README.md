# FocalTech FT3168

- **Category:** capacitive touch controller, I²C slave; a self/mutual-capacitance part aimed at
  small round and rectangular AMOLED panels.
- **Manufacturer:** FocalTech Systems Co., Ltd.
- **Retrieved:** 2026-09-07
- **Sibling record here:** [`ft6336g`](../ft6336g/README.md)

The touch controller of the **LilyGO T-Display-S3 AMOLED 1.64″** and of the **1.43″** round
board in both of its display-controller variants.

## 1. Identity and artifact

| Property | Value |
|---|---|
| Part | **FT3168** |
| Local artifact | [`artifacts/ft3168-datasheet-lilygo-mirror.pdf`](artifacts/ft3168-datasheet-lilygo-mirror.pdf) — 926 072 B, SHA-256 `b8c6079df7e94a539629f6dfaf2686899a29b030d15a76f4a5983dcf84f8685b` |
| Mirror sources — **two, identical size** | `Xinyuan-LilyGO/T-Display-S3-AMOLED-1.64` → `information/FT3168.pdf` @ `e236a4dfb3295c473d8ac7c240cbea93313707c0` · `Xinyuan-LilyGO/T-Display-S3-AMOLED-1.43-1.75` → same path @ `87aabe888eea6a7c0f95ce1991ca75fa98c2a172`. One copy retained; the second URL is recorded rather than stored twice |
| Licence | FocalTech copyright. The two mirroring repositories are **GPL-3.0** and **MIT** respectively; neither covers the PDF. **Redistribution status: unknown** |

## 2. Board usage

| Board | Build symbol | Display partner | I²C |
|---|---|---|---|
| [1.64″ AMOLED](../../../devices/lilygo/t-display-s3-amoled-1-64/README.md) | — | [CO5300/ICNA3311](../../chipone/co5300/README.md) | pins **not published** for this board |
| [1.43″ AMOLED](../../../devices/lilygo/t-display-s3-amoled-1-43-1-75/README.md) | `DO0143FMST10` | [CO5300](../../chipone/co5300/README.md) | SDA **GPIO7** / SCL **GPIO6**, `TP_INT` **GPIO9** |
| [1.43″ AMOLED](../../../devices/lilygo/t-display-s3-amoled-1-43-1-75/README.md) | `DO0143FAT01` | [SH8601](../../shenghe-microelectronics/sh8601z/README.md) | as above |

The **1.75″** board in the same family uses a **Hynitron CST9217** instead — so the touch
controller varies with the panel, not with the product name.

> ⚠ **`TP_INT` and `PCF8563_INT` are both GPIO9** in LilyGO's `pin_config.h` @ `87aabe8`.
> Either the two interrupt lines are wire-ORed (plausible — both are open-drain) or one define
> is wrong. **Unresolved**, and no schematic is published for these boards to settle it.

## 3. Software

LilyGO ships `examples/FT3168` and `examples/GFX_FT3168_Image` in both repositories. No
first-party ESPHome component was located. The FocalTech FT6x36/FT3x68 register conventions are
broadly similar across the family, but **that similarity is not evidence** — read the datasheet
before assuming a driver written for an FT6336 will work.

## 4. What was not verified

The datasheet was **not read**; no I²C address, register or timing value is transcribed here.
**The I²C address is therefore unknown in this record.** FocalTech touch parts commonly sit at
`0x38`, and that is the number a scanner will most likely report — but it is stated here as an
expectation, not a finding.

## 5. Gaps

- Address, register map, gesture support: unknown.
- **No pin map at all is published for the 1.64″ board** — no `pin_config.h` and no schematic
  exist in its repository. That is the largest gap around this part.
- Not verified on hardware.
