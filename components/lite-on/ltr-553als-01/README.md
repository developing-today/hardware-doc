# Lite-On LTR-553ALS-01

- **Category:** combined **ambient-light sensor and proximity sensor** with an integrated IR
  LED driver, I²C interface.
- **Manufacturer:** Lite-On Technology Corporation.
- **Retrieved:** 2026-09-07

> **This record was created 2026-09-07 to fill a gap.** The directory already held
> [`artifacts/ltr-553als-01-datasheet.pdf`](artifacts/ltr-553als-01-datasheet.pdf) with **no
> `README.md` beside it**. The datasheet was **not read** by this pass; nothing below is
> transcribed from it. A stub, to make the artifact discoverable and record its user.

## 1. Identity

| Property | Value |
|---|---|
| Part | **LTR-553ALS-01** |
| Datasheet | `ltr-553als-01-datasheet.pdf` — acquired by an earlier pass; version and provenance URL not recorded at the time |
| Interface | I²C |
| Address | **`0x23`** — from LilyGO's own I²C table for the T-Display-S3 Pro, not from the datasheet |

Related record already here:
[`generic/ambient-light-and-proximity-sensor-selection`](../../generic/ambient-light-and-proximity-sensor-selection/) *(artifacts only; no record yet)*.

## 2. Used By

### LilyGO T-Display-S3 Pro
→ [`devices/lilygo/t-display-s3-pro`](../../../devices/lilygo/t-display-s3-pro/README.md)

Ambient-light and proximity sensor at I²C **`0x23`**, on **SDA GPIO5 / SCL GPIO6** — a bus it
shares with the [CST226SE touch controller](../../hynitron/cst226se/README.md) (`0x5A`), the
[SY6970 PMIC](../../silergy/sy6970/README.md) (`0x6A`) and the camera. LilyGO's own
`examples/factory/utilities.h` @ `08b8b2bbcb8b263131af119476403080cd30224f` says so in a
comment: `// LTR553 , TOUCH , SY6970 , Camera share I2C Bus`.

Vendor example: `examples/LTR553ALS_Sensor`.

**A caution for auto-brightness code on this board.** The Pro ships in two revisions whose
backlight scales differ by 16× — `BRIGHTNESS_MAX_LEVEL` is **255** on V1.0 and **16** on V1.1,
selected by an `#ifdef USING_DISPLAY_PRO_V1`. Any closed loop from this sensor to the backlight
must know which board it is on. See
[board-revision-drift R6](../../../devices/lilygo/t-display-s3-shared/board-revision-drift.md#r6--t-display-s3-pro-v10-vs-v11-backlight-driver).

## 3. Gaps

Datasheet not read: register map, lux conversion, integration times, proximity configuration
and electrical limits are unrecorded. The `0x23` address is LilyGO's claim, not independently
confirmed. Original acquisition URL unknown. Not verified on hardware.
