# Chipone CO5300 (also marketed / referenced as ICNA3311)

- **Category:** AMOLED display driver IC, QSPI/MIPI host interfaces.
- **Manufacturer:** **Chipone Technology (Beijing) Co., Ltd.** — `www.chipone-ic.com`.
  Established from the datasheet cover; see [§2](#2-reading-that-cover-was-not-trivial).
- **Retrieved:** 2026-09-07

The display driver of the **LilyGO T-Display-S3 AMOLED 1.64″** (280 × 456) and of two of the
three round panels sold as **T-Display-S3 AMOLED 1.43″/1.75″** (466 × 466).

## 1. Identity

| Property | Value |
|---|---|
| Part | **CO5300** |
| Datasheet version | **V0.01**, 2023 |
| Publisher | Chipone Technology (Beijing) Co., Ltd. |
| Local artifact | [`artifacts/co5300-datasheet-v0.01-lilygo-mirror.pdf`](artifacts/co5300-datasheet-v0.01-lilygo-mirror.pdf) — **archived**, see the placeholder beside it. 13 236 092 B, SHA-256 `2ad0461aec31aa046e2661f52f43e9c36b36218c58c53f07217c73bef7d710c6` |
| Mirror sources (two, identical size) | `Xinyuan-LilyGO/T-Display-S3-AMOLED-1.64` → `information/CO5300_V0.01.pdf` @ `e236a4dfb3295c473d8ac7c240cbea93313707c0` · `Xinyuan-LilyGO/T-Display-S3-AMOLED-1.43-1.75` → same filename @ `87aabe888eea6a7c0f95ce1991ca75fa98c2a172` |
| Licence | Chipone copyright. The 1.64 repo is **GPL-3.0** and the 1.43-1.75 repo **MIT**; neither covers the PDF. **Redistribution status: unknown** |

Archived rather than kept in-tree at 12.6 MiB — it is the largest single artifact this pass
produced. The placeholder carries the hash, size and both re-acquisition URLs.

## 2. Reading that cover was not trivial

The PDF's text layer uses a **uniform +0x1D code-point offset**. Extracted naively it reads
`&2||2/(' … &+,321(7HFKQRORJ\`, and through the `/ToUnicode` CMap it reads
`FOD300 … FHHPONE TecOnology` — *human-legible and wrong*, which is the most dangerous
extraction failure there is.

Both decode consistently to **`CO5300 … CHIPONE Technology (Beijing) Co., Ltd.
www.chipone-ic.com Datasheet V0.01 2023`**. Two independent routes converging is what makes the
identification safe; either alone would have produced a plausible-looking error.

Recorded as a vendor trap in
[`vendors/lilygo/README.md`](../../../vendors/lilygo/README.md), because it will recur on any
Chinese-vendor datasheet exported by the same toolchain.

## 3. The ICNA3311 question

LilyGO's 1.64″ README writes the display driver as **"ICNA3311(CO5300)"**. ICNA3311 is also a
Chipone part number. Whether they are:

- the same die under two order codes,
- a rebadge for a particular panel maker, or
- a successor/predecessor pair,

is **not established.** The datasheet LilyGO ships says only *CO5300*. Recorded as an open
question rather than resolved by assumption.

## 4. Board usage

| Board | Panel | Touch partner | Bus |
|---|---|---|---|
| [T-Display-S3 AMOLED 1.64″](../../../devices/lilygo/t-display-s3-amoled-1-64/README.md) | 280 × 456 | [FT3168](../../focaltech/ft3168/README.md) | QSPI |
| [T-Display-S3 AMOLED 1.43″](../../../devices/lilygo/t-display-s3-amoled-1-43-1-75/README.md), build symbol `DO0143FMST10` | 466 × 466 round | FT3168 | QSPI |
| [T-Display-S3 AMOLED 1.75″](../../../devices/lilygo/t-display-s3-amoled-1-43-1-75/README.md), build symbol `H0175Y003AM` | 466 × 466 round | CST9217 | QSPI |

The 1.43″ board's **other** build option, `DO0143FAT01`, uses an
[SH8601](../../shenghe-microelectronics/sh8601z/README.md) instead — so one product page ships
two different display controllers.

**Resolution conflict:** LilyGO's README says 466 × 466 while its `pin_config.h` says
`LCD_WIDTH 473 / LCD_HEIGHT 467`. The likely reading is addressable window versus visible
circle, but that is inference. See the device record.

Pins on the 1.43/1.75 board: `LCD_SDIO0..3` GPIO 11/13/14/15, `LCD_SCLK` 12, `LCD_CS` 10,
`LCD_RST` 17, `LCD_EN` 16.

## 5. What was not verified

Beyond the cover, **the datasheet was not read** — no register, timing or electrical value is
transcribed here. Given the text-layer offset, anyone extracting values from it **must**
validate against a rendered page first.

## 6. Used by

- [`devices/lilygo/t-display-s3-amoled-1-64`](../../../devices/lilygo/t-display-s3-amoled-1-64/README.md) — 280 × 456; **no schematic and no pin map published for that board**, which is its principal gap
- [`devices/lilygo/t-display-s3-amoled-1-43-1-75`](../../../devices/lilygo/t-display-s3-amoled-1-43-1-75/README.md) — 466 × 466 round, two of three build variants
