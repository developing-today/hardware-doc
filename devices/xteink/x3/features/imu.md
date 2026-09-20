# X3 — IMU (QMI8658)

> Six-axis accelerometer + gyroscope. Powers the advertised **motion-based page
> turning**. 2026-09-04.

| Property | Value |
|---|---|
| Part | **QMI8658** — [`qst/qmi8658a`](../../../../components/qst/qmi8658a/README.md) |
| Address | **0x6B**, alternate **0x6A** |
| Bus | I²C SDA **20** / SCL **0** @ 400 kHz |
| `WHO_AM_I` | register `0x00` == **`0x05`** |
| Interrupt line | **none** — polled |
| SDK type | `ImuType::Qmi8658` |

## Corroboration

Three independent sources agree:

1. **[SDK]** `BoardConfig.h:915` — `ImuType::Qmi8658`, address 0x6B
2. **[SDK]** `XteinkDetect.cpp` — used as an X3-detection fingerprint, checking
   `WHO_AM_I == 0x05`
3. **[CN]** `sunwoods/Xteink-X3` BOM — *"QMI8658 姿态传感器"* (attitude sensor)

This is one of the few parts in the whole family confirmed by both firmware and a
physical teardown.

## What it is used for

The vendor's X3 launch announcement lists *"Built-in **gyroscope** for
motion-based page turning"* — [r/xteinkereader `1pi6ezd`](https://old.reddit.com/r/xteinkereader/comments/1pi6ezd/),
2025-12-09. That is a stock-firmware feature.

Whether any community firmware implements it was **not established**.

## Role as a device fingerprint

`XteinkDetect::detectXteinkVerdict()` scores the presence of the QMI8658 (0x6B),
BQ27220 (0x55) and DS-series RTC (0x68) on SDA20/SCL0. **Finding them means X3;
finding nothing means X4.** So the IMU is load-bearing for correct board
selection, not just a feature.

## Limits

- **No interrupt pin**, so wake-on-motion is not available — the part must be
  polled, which costs power.
- Shares one I²C bus with the gauge and RTC.
- No ODR, range or noise figures were measured or reported for this board.

## Cross-device note

The **X4 Classic** also carries a QMI8658 at 0x6B with the same no-interrupt
arrangement. The **X4 Pro has no IMU at all**, and neither does the X4.

## Status

`hardware-confirmed` for presence and address (firmware + teardown).
`not-tested` for any performance property.
