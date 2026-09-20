# Sensirion SHTC3

- **Category:** digital **relative-humidity and temperature sensor**, ultra-low-power, single package
- **Manufacturer:** Sensirion AG
- **Interface:** I²C, **fixed address `0x70`** — not configurable, which matters when planning a bus
- **Document status:** datasheet retained; **version `unknown`** — the mirrored copy carries no revision marking this pass identified
- **Research status:** **stub.** Datasheet held and validated; accuracy tables, timing and the command set have **not** been transcribed
- **Retrieved:** 2026-09-01. **Nothing verified on hardware.**

## What it is

Sensirion's low-cost, low-power humidity/temperature part — the one that shows up on
consumer and hobby boards where a full-accuracy SHT3x/SHT4x is not justified. It has
a sleep mode measured in tenths of a microamp, which is why it pairs naturally with
e-paper: both are chosen for designs that spend nearly all their time doing nothing.

**Its address is fixed at `0x70`.** There is no address-select pin, so **two SHTC3s
cannot share one I²C bus.** Worth knowing before designing one in alongside another
`0x70` device.

## What has not been done

- Accuracy, repeatability and drift figures not transcribed.
- Command set (`measure`, `sleep`, `wake-up`, `soft reset`, ID read), timing and CRC
  scheme not documented.
- No self-heating analysis — relevant for a sensor mounted on a board next to a
  charging PMIC, which is exactly the situation on the board below.
- No comparison against SHT3x / SHT4x / AHT2x alternatives.

## Artifacts

| File | Bytes | SHA-256 | Source | Retrieved | Version |
|---|---|---|---|---|---|
| [`artifacts/shtc3-datasheet-waveshare-mirror.pdf`](artifacts/shtc3-datasheet-waveshare-mirror.pdf) | 928 256 | `d315fe3d00282ece1d8901c0936f8bcbaa87b159bcd0e71f9002d1f03b57a8f1` | `https://files.waveshare.com/wiki/common/SHTC3_Datasheet.pdf` | 2026-09-01 | `unknown` |

**Waveshare's mirror, not Sensirion's own copy** — labelled as such. Sensirion
publishes this document openly and the original should be fetched and hashed against
this one in a future pass; the same board already produced a case where
[Waveshare's mirror was a full revision stale](../../nxp/pcf85063a/README.md).

Validated by magic bytes (`%PDF-`), not by HTTP status. **Licence `unknown`.**
Disposition: `repository`.

## Used by

### [Waveshare ESP32-S3-ePaper-3.97](../../../devices/waveshare/esp32-s3-epaper-3.97/README.md)

Designator `U3`. Provides the board's environmental sensing — one of the features
that distinguishes it from the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md),
which has no environmental sensor at all.

On the board's **single shared I²C bus** (GPIO41 SDA / GPIO42 SCL) alongside the
[AXP2101](../../x-powers/axp2101/README.md) PMIC at `0x34`, the
[PCF85063A](../../nxp/pcf85063a/README.md) RTC and the
[QMI8658A](../../qst/qmi8658a/README.md) IMU. At `0x70` it does not collide with any
of them.

Notably, the schematic's own GPIO allocation table gives the SHTC3 **no column**,
even though the part is fitted and the vendor documents it — a small reminder that
the allocation table is a summary, not a census.

Vendor examples: `Arduino/examples/04_I2C_SHTC3` and ESP-IDF `07_I2C_SHTC3`. Neither
was read in this pass, so **the address above is the datasheet's fixed value rather
than a value observed in this board's source**.

An e-paper display with a temperature sensor is a useful combination beyond weather
display: e-paper waveforms are strongly temperature-dependent, and the
[SSD1677](../../solomon-systech/ssd1677/README.md) can select LUTs by temperature.
Whether the board's firmware feeds SHTC3 readings to the panel driver, or relies on
the controller's own sensing, is **not established**.

## See also

- [All components](../../README.md)
