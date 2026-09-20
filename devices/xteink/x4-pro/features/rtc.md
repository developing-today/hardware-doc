# X4 Pro — real-time clock

> BM8563 on the shared I²C bus. Evidence: hardware-confirmed. 2026-09-04.

| Property | Value |
|---|---|
| Part | **BM8563** — PCF8563 **register-compatible** |
| Component | [`generic/bm8563`](../../../../components/generic/bm8563/README.md) |
| Address | **0x51** |
| Bus | SDA 39 / SCL 38 @ 400 kHz, controller 0 (`Wire`) |
| SDK type | `RtcType::Pcf8563` |
| Class in OEM dump | `XTEink::BM8563Driver` |
| Driver init | IROM `0x420a2834` — adds device 0x51; bus object configured `{39, 38, 400000}` |

Confirmed **found and initializing on hardware**.

**BM8563 is not PCF8563.** It is a separate part (originally Holtek/BesTek
lineage, widely used by M5Stack) that is register-compatible with the PCF8563.
Driving it with a PCF8563 driver works; calling it a PCF8563 in a bill of
materials does not.

Note the family split: the X4 Pro and X4 Classic use the **BM8563 at 0x51**,
while the [X3](../../x3/features/rtc.md) uses a **DS-series RTC at 0x68** and the
[X4](../../x4/README.md) has **no RTC at all**. Four devices, three different
answers.

## Backup power

Not established. No teardown exists to check for a supercap or coin cell, and the
firmware does not reveal it.

## Status

`hardware-confirmed` for presence, address and initialisation.
