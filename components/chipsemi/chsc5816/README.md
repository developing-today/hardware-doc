# Chipsemi CHSC5816

- **Category:** capacitive touch controller, I²C slave, aimed at small round and rectangular
  panels.
- **Manufacturer:** Chipsemi (Shenzhen) / 海栎创-adjacent Chinese touch vendor. **Not
  independently verified** — see §1.
- **Retrieved:** 2026-09-07

> **This record was created 2026-09-07 to fill a gap.** The directory already held
> [`artifacts/chsc5816-datasheet-v1-20221114-zh.pdf`](artifacts/chsc5816-datasheet-v1-20221114-zh.pdf)
> with **no `README.md` beside it**. The datasheet was **not read** by this pass; nothing below
> is transcribed from it. This is a stub that makes the artifact discoverable and records the
> device that uses it.

## 1. Identity

| Property | Value |
|---|---|
| Part | **CHSC5816** |
| Datasheet | `chsc5816-datasheet-v1-20221114-zh.pdf`, Chinese, dated **2022-11-14** — acquired by an earlier pass; provenance URL not recorded at the time |
| Interface | I²C |
| Address | **not verified here** |
| Manufacturer | the filename and LilyGO's link both point at `lewisxhe/SensorLib`, whose copy is named *"CHSC5816触控芯片使用说明V1-20221114"*. The maker is not stated on any source read by this pass |

**Acquisition route for a fresh copy:** LilyGO links it from
`github.com/lewisxhe/SensorLib/blob/master/datasheet/` — the same third-party library
repository it uses for the Hynitron CST parts. Pin that to a commit if you re-fetch it.

## 2. Used By

### LilyGO T-Display AMOLED Lite (1.47″)
→ [`devices/lilygo/t-display-amoled-lite`](../../../devices/lilygo/t-display-amoled-lite/README.md)

Touch controller of the 194 × 368 AMOLED panel. `TOUCH_IRQ` **GPIO13**, `TOUCH_RST` **GPIO14**,
I²C SDA **GPIO1** / SCL **GPIO2** — `LilyGo-Display-IDF/main/product_pins.h`, block
`CONFIG_LILYGO_T_AMOLED_LITE_147` @ `b1a1cc54994bf1b417e3bb30c437bbe1036bff7f`.

**Its signals cross a 1.8 V level translator.** That board's panel and touch controller run at
1.8 V behind an RS0108 translator — the schematic's net names make it explicit (`TP_INT` ↔
`TP_INT_1V8`). That is unique in the
[T-Display-S3 family](../../../devices/lilygo/t-display-s3-shared/README.md) and is why the
board also carries an [AXP2101 PMU](../../x-powers/axp2101/README.md).

Driver: `lewisxhe/SensorLib` (declared as **v0.2.4** by `LilyGo-AMOLED-Series` @ `6d1dc00`).

## 3. Gaps

Datasheet not read: address, register map, gesture support, timing and electrical limits are
all unrecorded. Original acquisition URL unknown. Not verified on hardware.
