# Bosch Sensortec BHI260AP

- **Category:** smart sensor hub — a 6-axis IMU (3-axis accel + 3-axis gyro) with an integrated
  programmable **Fuser2** 32-bit microcontroller running Bosch's sensor-fusion firmware.
  I²C/SPI host interface.
- **Manufacturer:** Bosch Sensortec GmbH.
- **Retrieved:** 2026-09-07
- **Siblings here:** [`bmi270`](../bmi270/README.md) · [`bma423`](../bma423/) *(artifacts only; no record yet)*

Fitted to **some** LilyGO **T-Display-S3 Pro** boards. Which IMU any given Pro carries is
**not determined by the product name** — see §2.

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **BHI260AP** | `schematic/T-BHI260.pdf` and `T-BHI260_V1.1.pdf` in `Xinyuan-LilyGO/T-Display-S3-Pro` @ `08b8b2bbcb8b263131af119476403080cd30224f` |
| KiCad footprint | `schematic/kicad_sensor.pretty/T-BHI260.kicad_mod` (4 541 B) | same |
| Firmware naming it | `firmware/v1.1/UnitTest_V1.1_DisChg_BHI260_241111.bin` | same |
| Datasheet | **not retrieved.** Bosch publishes BHI260AP openly at `bosch-sensortec.com`; acquisition is straightforward and simply was not done | — |
| Local artifact | **none** | — |

**What distinguishes a BHI260AP from an ordinary IMU** is that it is a *sensor hub*: the
on-chip Fuser2 core runs downloadable firmware that performs orientation fusion, step counting,
activity recognition and gesture detection **without waking the host**. That is why it appears
on a handheld board — it is the part that lets the ESP32-S3 sleep.

The corollary is that a BHI260AP is useless without its firmware image. Bosch's
`BHY2-Sensor-API` and a `.fw` blob must be flashed to it (from host RAM or an external EEPROM)
at every boot or from a dedicated flash. Anyone expecting a BMI270-style register interface will
be surprised.

## 2. Which IMU is on your Pro?

The repository ships schematics and footprints for **two** sensors:

| Document | Part |
|---|---|
| `T-BHI260.pdf`, `T-BHI260_V1.1.pdf`, `T-BHI260.kicad_mod` | **BHI260AP** |
| `T-ICM29048.pdf`, `T-CIM29048.kicad_mod` | an **ICM-20948**-class TDK part (LilyGO spells it `ICM29048` / `CIM29048`) |

Two schematics, two footprints, one product name. **Scan I²C to find out what you have.**
Recorded as [board-revision-drift R7](../../../devices/lilygo/t-display-s3-shared/board-revision-drift.md#r7--t-display-s3-pro-two-different-imu-daughter-boards).

Note also that the sensor appears to sit on a **daughter-board or module** (the schematics are
separate sheets named `T-BHI260`, `T-ICM29048`, with their own footprints) rather than on the
mainboard — which is how a single product can ship either.

## 3. Board integration

`BOARD_SENSOR_IRQ` is **GPIO21** (`examples/factory/utilities.h` @ `08b8b2b`). The sensor shares
the board's single I²C bus — SDA **GPIO5**, SCL **GPIO6** — with the
[CST226SE touch](../../hynitron/cst226se/README.md) at `0x5A`, the
[SY6970 PMIC](../../silergy/sy6970/README.md) at `0x6A`, the
[LTR-553ALS](../../lite-on/ltr-553als-01/README.md) at `0x23` and the camera. The file's own
comment says so: `// LTR553 , TOUCH , SY6970 , Camera share I2C Bus`.

**The BHI260AP's I²C address is not stated by LilyGO** and is not recorded here.

## 4. Software

`lewisxhe/SensorLib` — the same author's library that covers the CST touch parts — is what
LilyGO uses across its boards. Bosch's own `BHY2-Sensor-API` is the reference implementation.

## 5. Gaps

- Datasheet not retrieved; no register, address or electrical value here.
- **Which board revisions carry which sensor is unknown.**
- The ICM-209xx alternative has no record in this repository.
- Whether the sensor is on the mainboard or a module is inferred from the schematic file
  structure, not confirmed.
- Not verified on hardware.

## 6. Used by

### LilyGO T-Display-S3 Pro (some units)
→ [`devices/lilygo/t-display-s3-pro`](../../../devices/lilygo/t-display-s3-pro/README.md)

Interrupt GPIO21; I²C shared with touch, PMIC, ambient-light sensor and camera on GPIO5/6.
**Presence is not guaranteed by the product name.**
