# QST QMI8658A

- **Category:** **6-axis inertial measurement unit** — 3-axis accelerometer + 3-axis gyroscope, with an integrated motion engine (tap, step, pedometer, no-motion/any-motion)
- **Manufacturer:** QST Corporation (矽睿科技)
- **Interface:** I²C or SPI. I²C 7-bit address **`0x6A`** (`SA0` low) / **`0x6B`** (`SA0` high) — **`inferred` from the part's documented defaults, not confirmed against any board's source in this pass**
- **Document status:** datasheet **Rev A** retained in [`artifacts/`](artifacts/)
- **Research status:** **stub.** This page exists so that the boards citing the part have somewhere to link and the artifact is not orphaned. The register map has **not** been mined.
- **Retrieved:** artifact 2026-08-23; this page written 2026-09-01. **Nothing verified on hardware.**

## Why this page is thin

The datasheet has been held in this repository since **2026-08-23** with no record
page beside it. That is the condition the method warns about — an artifact nobody has
read is a download, not research. This page converts it from an orphan into a stub
with an honest scope, and names what remains.

**Not done:** register map, ODR/range/bandwidth tables, the motion-engine command
interface, self-test, calibration, noise and offset specifications, power modes and
their currents, package/pinout, lifecycle and pricing, or any comparison against the
obvious alternatives ([BMI270](../../bosch-sensortec/bmi270/README.md) is already in
this knowledge base; LSM6DS3/QMI8658C are the other usual candidates).

## What is established

- QST's mainstream 6-axis part for consumer and hobby designs, widely used on ESP32
  boards as the cheaper alternative to Bosch's BMI2xx family.
- Supports **both** I²C and SPI, selectable by a mode pin — so a board's choice is a
  board fact, not a part fact.
- Ships a **motion engine** (pedometer, tap, significant-motion) that offloads the
  host. This is the feature that makes it attractive on a battery-first device: the
  host can stay asleep until the IMU decides something happened.

Whether any given board actually uses that engine, rather than polling raw samples,
is a per-board question and is **not** answered here for any of them.

## Artifacts

| File | Bytes | Source | Retrieved | Version |
|---|---:|---|---|---|
| [`artifacts/qmi8658a-datasheet-rev-a.pdf`](artifacts/qmi8658a-datasheet-rev-a.pdf) | 3 085 534 | *not recorded when acquired* | 2026-08-23 | **Rev A** |

**The acquisition URL for this artifact was not recorded** by the pass that fetched
it. That is a provenance gap, recorded rather than back-filled with a guess — per the
method, a plausible-looking URL invented after the fact is worse than an honest
`unknown`. A future pass should locate QST's own copy, hash it against this one, and
record the source properly.

**Licence `unknown`.** Disposition: `repository`.

## Used by

### [Waveshare ESP32-S3-ePaper-3.97](../../../devices/waveshare/esp32-s3-epaper-3.97/README.md)

Named `QMI8658A` on the schematic, marketed by Waveshare as "QMI8658". On the board's
**single shared I²C bus** (GPIO41 SDA / GPIO42 SCL) alongside the
[AXP2101](../../x-powers/axp2101/README.md) PMIC, the
[PCF85063A](../../nxp/pcf85063a/README.md) RTC, the
[ES8311](../../everest-semiconductor/es8311/README.md) codec and the
[SHTC3](../../sensirion/shtc3/README.md).

| Signal | GPIO | Schematic net |
|---|---|---|
| `INT1` | GPIO39 | `AXIS_INT1` |
| `INT2` | GPIO40 | `AXIS_INT2` |
| `SDA` / `SCL` | GPIO41 / GPIO42 | `AXIS_SDA` / `AXSI_SCL` *(vendor's typo, verbatim)* |

**`INT1` on GPIO39 is contested** — the schematic's allocation table puts the audio
amplifier gate `AudioCTR_PIN` on the same pin. Unresolved; see
[C-WS9](../../../devices/waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws9--gpio39-carries-two-functions).

Vendor examples: `Arduino/examples/06_QMI8658A` (using the bundled `SensorLib`) and
ESP-IDF `05_QMI8658A`. Neither was read in this pass, which is why the I²C address
above remains `inferred`.

### [Xteink X3](../../../devices/xteink/x3/README.md) and [Xteink X4 Classic](../../../devices/xteink/x4-classic/README.md) — *added 2026-09-04*

Two Xteink e-readers carry a QMI8658 at **I²C 0x6B**, with **`WHO_AM_I`
(register `0x00`) == `0x05`** and **no interrupt line** on either board.

| | X3 | X4 Classic |
|---|---|---|
| SoC | ESP32-C3 | ESP32-S3 |
| Bus | SDA **20** / SCL **0** @ 400 kHz | SDA **39** / SCL **38** @ 400 kHz |
| Address | 0x6B (alt 0x6A probed) | 0x6B |
| Interrupt | **none** | **none** |
| Bus neighbours | BQ27220 0x55, DS-series RTC 0x68 | BM8563 RTC 0x51, CW2017 gauge 0x63 |
| Init observed | — | `CTRL1/2/3/7` written at 0x6B (RE-confirmed) |

**This record's `inferred` I²C address is now corroborated.** The FreeInk SDK
declares 0x6B for both boards, `XteinkDetect` probes it as a device fingerprint,
and the Chinese X3 teardown BOM lists *"QMI8658 姿态传感器"* independently —
three lines of evidence, one of them a physical teardown.

**The X3 uses it as a product feature:** the vendor's launch announcement lists
*"Built-in **gyroscope** for motion-based page turning"*
([r/xteinkereader `1pi6ezd`](https://old.reddit.com/r/xteinkereader/comments/1pi6ezd/), 2025-12-09).
Whether any community firmware implements that is **not established**.

**It also does a second, load-bearing job on the X3:** it is one of three parts
`XteinkDetect::detectXteinkVerdict()` scores on the C3 boards' secondary I²C bus
to decide at boot whether it is running on an **X3** (parts present) or an
**[X4](../../../devices/xteink/x4/README.md)** (bus empty). A missing or
mis-addressed IMU therefore selects the wrong board profile entirely, not merely
a dead sensor.

**No interrupt line means no wake-on-motion** on either device — the part must be
polled, which costs power on a battery reader. Neither board's ODR, range or noise
performance has been measured or reported.

Notably, the **[X4 Pro](../../../devices/xteink/x4-pro/README.md) has no IMU at
all**, so the "Pro" model is not a superset of its cheaper siblings.

→ [`devices/xteink/x3/features/imu.md`](../../../devices/xteink/x3/features/imu.md)

## See also

- [Bosch BMI270](../../bosch-sensortec/bmi270/README.md) — the comparable part already recorded here
- [QMC6310](../qmc6310/) — the other QST part in this knowledge base. **Artifacts-only directory; no record page yet**, in the same condition this one was until 2026-09-01
- [All components](../../README.md)
