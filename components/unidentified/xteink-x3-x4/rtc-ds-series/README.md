# "DS-series" real-time clock @ 0x68 — Xteink X3 (part unresolved)

- **Category:** I²C real-time clock.
- **Manufacturer:** presumed Maxim/Analog Devices lineage or a second source —
  **not established**.
- **Research status:** 🔴 **Active conflict. Three sources, three answers.**
- **Retrieved:** 2026-09-04

## The conflict

| Source | Class | Claim |
|---|---|---|
| FreeInk SDK `BoardConfig.h:915` | firmware driven in production | **`RtcType::Ds3231`** |
| [Imgur X3 teardown](../../../../devices/xteink/x3/media.md), image 13 | firsthand photograph of the marking | **"DS1307 RTC"** |
| [`sunwoods/Xteink-X3`](https://github.com/sunwoods/Xteink-X3) BOM | firsthand teardown, Chinese | **"DS系列RTC时钟芯片"** — *DS-series*, **deliberately not narrowed** |

**All three are consistent with I²C address 0x68**, which the DS1307 and the
DS3231 both use. The address does not discriminate.

## Why the firmware is not decisive either

`XteinkDetect` probes the RTC by reading `DS3231_SEC_REG = 0x00` — the **seconds
register, which is byte-identical on both parts**. So the code that appears to
confirm a DS3231 confirms only *"something with a DS-family register 0"*.

The SDK's `Ds3231` label may itself be an unfalsified assumption. A working
driver is **not** proof of part identity when the two candidates share the
registers the driver touches.

## Why it matters

| | DS1307 | DS3231 |
|---|---|---|
| Timekeeping registers `0x00`–`0x06` | same layout | same |
| Oscillator | external 32.768 kHz crystal, **uncompensated** | **integrated TCXO**, ±2 ppm |
| Temperature registers | **none** | `0x11` / `0x12` |
| Alarms | none | two |
| Nominal supply | 5 V part | 2.3–5.5 V |

Drift is user-visible on a device that displays a clock — and the X3's launch
announcement explicitly advertises *"Time display and battery percentage"*.
A 5 V-nominal part on a 3.3 V board would also be an unusual design choice worth
knowing about.

## What would resolve it — one register read

**Read registers `0x11` and `0x12`.** The DS3231 returns a temperature there
(8-bit integer + 2-bit fraction). The DS1307 does not implement them and will
return whatever its RAM holds or float.

```c
// inferred, not executed — one I2C read settles a three-way conflict
Wire.beginTransmission(0x68); Wire.write(0x11); Wire.endTransmission(false);
Wire.requestFrom(0x68, 2);   // DS3231: plausible temperature. DS1307: RAM/garbage
```

Alternatively: examine the archived teardown photograph `13-Ay3rpJg.jpg`
(5760 × 3240) at full resolution and judge whether the caption is supported by
the image. **That has not been done.**

## Filed under `unidentified/` deliberately

Per the research method: *"Do not assign a guessed part number. Create an
unidentified/generic record and explain what evidence would resolve it."*
Filing this under `maxim/ds3231` or `maxim/ds1307` would launder a conflict into
a fact.

---

## Used By

### [Xteink X3](../../../../devices/xteink/x3/README.md)

At **0x68** on the secondary I²C bus **SDA 20 / SCL 0 @ 400 kHz**, shared with the
[BQ27220 fuel gauge](../../../texas-instruments/bq27220/README.md) (0x55) and the
[QMI8658 IMU](../../../qst/qmi8658a/README.md) (0x6B).

Also serves as one of the three device-identification fingerprints that
distinguish an X3 from an [X4](../../../../devices/xteink/x4/README.md) at boot.

**Backup power source is unknown** — no supercap or coin cell is identified in
either teardown.

→ [`devices/xteink/x3/features/rtc.md`](../../../../devices/xteink/x3/features/rtc.md)
→ [`devices/xteink/x3/gaps-and-conflicts.md`](../../../../devices/xteink/x3/gaps-and-conflicts.md)

## Family contrast

The S3 devices use a **BM8563 at 0x51** (PCF8563-register-compatible) — a
different part at a different address. The **[X4](../../../../devices/xteink/x4/README.md)
has no RTC at all.** Four devices, three answers.
