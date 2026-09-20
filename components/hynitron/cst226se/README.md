# Hynitron CST226SE

- **Category:** multi-point capacitive touch controller, I²C slave.
- **Manufacturer:** Hynitron Microelectronics.
- **Retrieved:** 2026-09-07
- **Siblings here:** [`cst816d`](../cst816d/README.md) · [`cst328`](../cst328/README.md) ·
  [`cst3530`](../cst3530/README.md)

The touch controller of the **LilyGO T-Display-S3 Pro** and the **LilyGO T4-S3**.

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **CST226SE** | LilyGO's T-Display-S3-Pro README I²C table |
| I²C address | **`0x5A`** | same table, which lists it beside SY6970 `0x6A` and LTR-553ALS `0x23` |
| Datasheet | **not retrieved.** LilyGO links a Chinese Hynitron porting manual hosted in `lewisxhe/SensorLib` (`海栎创触摸芯片移植手册-v3.5-20220701(1).pdf`) rather than mirroring it | `LilyGo-AMOLED-Series` README § *T4-S3 datasheet* |
| Local artifact | **none** | — |

**Acquisition note for the next reader:** the document LilyGO points at is a *touch-chip porting
manual* covering several Hynitron parts, not a CST226SE datasheet, and it lives in a third-party
repository (`lewisxhe/SensorLib`, `datasheet/` directory). Retrieving it and pinning it to a
commit is the obvious next step and was not done here.

## 2. Software

`lewisxhe/SensorLib` is the driver LilyGO uses on both boards — the same author maintains
`XPowersLib` for the SY6970/AXP2101 parts. `LilyGo-AMOLED-Series` declares **SensorLib v0.2.4**
as a dependency; the T-Display-S3-Pro repo uses `TouchLib` instead. Two vendor boards, two
different touch libraries for the same controller — worth knowing before assuming code ports.

## 3. What was not verified

No datasheet, no register map, no timing. The address `0x5A` is from LilyGO's own README table
and is **not** independently confirmed. Note that `0x5A` is also the I²C address of the
DRV2605L haptic driver documented elsewhere in this repository — if you are scanning a bus that
could contain either, the address alone will not tell you which.

## 4. Used by

### LilyGO T-Display-S3 Pro
→ [`devices/lilygo/t-display-s3-pro`](../../../devices/lilygo/t-display-s3-pro/README.md)

I²C `0x5A` on **SDA GPIO5 / SCL GPIO6**, shared with the SY6970 PMIC (`0x6A`), the LTR-553ALS
ambient-light sensor (`0x23`) and the camera. Reset **GPIO13**. Interrupt **GPIO7** per
`product_pins.h` — note the board's own `utilities.h` does **not** define a touch IRQ at all.

### LilyGO T4-S3
→ [`devices/lilygo/t4-s3`](../../../devices/lilygo/t4-s3/README.md)

I²C on **SDA GPIO6 / SCL GPIO7**, interrupt **GPIO8**, reset **GPIO17**.
