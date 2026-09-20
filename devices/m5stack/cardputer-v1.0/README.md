# M5Stack Cardputer (v1.0, K132)

> **SKU `K132`** · product id **`481`** · core module **StampS3** (`Sch_M5StampS3_v0.2`)
> Superseded by [v1.1](../cardputer-v1.1/README.md) on **2025-03-07** and by the
> [ADV](../cardputer-adv/README.md) on **2025-09-05**. No longer listed on M5Stack's store as of
> **2026-09-04** (the store lists only the `[EOL]`-titled v1.1 and the ADV).
> Research snapshot **2026-09-04**.

The original. It defined the format — 84 × 54 mm, 56 keys, 1.14″ screen, magnetic LEGO-compatible
base — and everything since has been a refinement of it.

This record is light by design. The v1.0 and v1.1 **share a mainboard schematic file**, so
everything except the Stamp module is documented at
[`../cardputer-v1.1/README.md`](../cardputer-v1.1/README.md), and the deep treatment of the
shared subsystems is at [`../cardputer-adv/`](../cardputer-adv/README.md).

## Identity

| Field | Value |
|---|---|
| Name | Cardputer |
| SKU | `K132` |
| Product id | `481`; Stamp module `522` |
| Core module | **StampS3** (`Sch_M5StampS3_v0.2.pdf`, 348 884 B, `6d92e1ae…`) |
| SoC | ESP32-S3FN8, 8 MB flash, **no PSRAM** |
| Display | ST7789V2 1.14″ 240 × 135 |
| Keyboard | 56 keys via **74HC138** |
| Audio | NS4168 amp + **SPM1423** PDM mic, no jack |
| Battery | 120 mAh internal + 1400 mAh base |
| Size / weight | 84.0 × 54.0 × 19.7 mm, **92.3 g** — the heaviest of the three |
| Sleep / operating current | 0.26 µA; IR mode 255.6 mA, key mode 165.7 mA |
| Includes | 1 × Cardputer, 1 × **2.0 mm** hex key |

## The only real difference: the Stamp module

| | **StampS3 v0.2** (this board) | Stamp-S3A v0.3.3 (v1.1, ADV) |
|---|---|---|
| 3.3 V rail | `M2` = **Murata `MUN3CAD01-SC`**, a `µPOL` 1 A point-of-load **power module** (converter + inductor + caps in one 2.9 × 2.3 × 1.05 mm package), 2.7–5.5 V in, output set by R16 100 k / R17 22.1 k. Identified by a concurrent session from a retrieved datasheet — this pass had flagged the string as suspect because there is **no page render for product id 522** to check it against. | **JoulWatt `JW5712`** buck |
| Load switch | **SGM2578** (U2) | AW35122FDR (U2) |
| **WS2812 supply** | **`VDD_3V3` — always on** | `BL_3V3` — switched with the backlight |
| Boot button | `SMT_SW_1TS026A`, body 2.6 × 1.6 × 0.55 mm | same part, body 4.0 × 3.0 × 2.0 mm |
| Crystal load caps | 12 pF / 10 pF | 12 pF / 12 pF |
| Solder jumper `JP4` at the WS2812 | **present** | removed |
| Antenna | "standard" | "optimized" |

**The v1.0 is the only Cardputer whose RGB LED works at any backlight level**, because its
WS2812 is not on the switched rail. That is a genuine advantage over both later boards, and it
was traded away for a lower sleep current (0.26 µA → 0.15 µA). Verified by comparing U3's `VDD`
net across the two Stamp schematics.

## ⚠ The published schematics are the same file as the v1.1's

`…/481/Sch_M5Cardputer.pdf` and `…/1127/Sch_M5Cardputer.pdf` are **byte-identical**
(SHA-256 `6016c1fe6099b9e3f0d0c88f07a3fba1aa44a3da8a7a91dd7040ad0fffa2041e`, 717 743 B), as are
the two base schematics (`29542fe1…`, 24 076 B). Read with M5Stack's own comparison table —
which lists only module-level differences — the honest statement is that **no mainboard change
between v1.0 and v1.1 is documented**. Whether one exists is unresolved; see
[`../cardputer-adv/gaps-and-conflicts.md`](../cardputer-adv/gaps-and-conflicts.md) §C3.

For that reason the schematic PDF is retained once, in the
[v1.1 record](../cardputer-v1.1/README.md), rather than duplicated here.

## Pin map

Identical to the v1.1 in every row. See [`../cardputer-v1.1/README.md`](../cardputer-v1.1/README.md#pin-map).
Keyboard: drive `G8/G9/G11` → 74HC138 `A0/A1/A2`; sense `G13, G15, G3, G4, G5, G6, G7`;
battery ADC `G10`; microSD `G12/G14/G40/G39`; display `G33–G38`; RGB `G21`;
audio `G41/G42/G43/G46`; IR `G44`; Grove `G1/G2`. **No internal I²C bus.**

## Components

Same as the v1.1 except the module: [`m5stack/stamp-s3`](../../../components/m5stack/stamp-s3/README.md)
(v0.2) instead of `stamp-s3a`, and [`sgmicro/sgm2578`](../../../components/sgmicro/sgm2578/README.md)
in place of the AW35122FDR, and [`murata/mun3cad01-sc`](../../../components/murata/mun3cad01-sc/README.md) — a `µPOL` power module — in place of the JW5712 buck.

## Development

Identical toolchain and procedure to the v1.1 and ADV — same PlatformIO profile, same
download-mode sequence, same `M5Cardputer` library (which installs `IOMatrixKeyboardReader`).
Factory firmware: `M5Cardputer-UserDemo` **`main`**. EasyLoader:
`m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/core/Cardputer/Cardputer.exe`
— **the same binary the v1.1 page links.**

Library milestones for this board: first commits 2023-10-10, `v1.0.1` with IR/NEC and key
numbering 2023-10-13, USB-keyboard demo 2023-10-16, SD demo 2024-01-19, WAV recording 2024-12-25.

## Community

Every major Cardputer firmware supports it — it is the compatibility baseline. It has no
Meshtastic upstream variant and none of the 2026 ADV-only projects. Buying one new in 2026 is
not possible through M5Stack; second-hand data was not gathered.

## Sources

Product page `https://docs.m5stack.com/en/core/Cardputer` (retrieved 2026-09-04, snapshot at
`artifacts/docs-en-core-Cardputer.html`); StampS3 v0.2 schematic
`https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/522/Sch_M5StampS3_v0.2.pdf`;
`M5Cardputer` @ `f1392858`. Full table: [`../cardputer-adv/sources.md`](../cardputer-adv/sources.md).
