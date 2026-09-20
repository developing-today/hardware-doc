# X4 — USB

> **USB-C, and it charges over it.** The only member of the family that does.
> 2026-09-04.

| Property | Value |
|---|---|
| Connector | **USB-C** |
| Peripheral | ESP32-C3 **USB-serial-JTAG** (no external bridge) |
| `usbDetect` | **GPIO20** — but see the conflict below |
| Charging | **over USB-C** |
| USB-MSC | not documented for this device |

## Why USB-C matters here

The X3 and X4 Pro both charge over a **magnetic pogo connector** requiring a
proprietary cable. Owners cite USB-C as a reason to keep an X4 rather than
upgrade:

> "It's enough that I'll happily keep using my original X4 instead of upgrading."
> — [r/xteinkereader `1v2txxe`](https://old.reddit.com/r/xteinkereader/comments/1v2txxe/), 2026-07-21

## The GPIO20 conflict

`usbDetect = 20` in the X4 profile. On the **X3** — same board family —
**GPIO20 is the I²C SDA line**. The X4 has no I²C peripherals so the pin is free,
but neither assignment is marked hardware-confirmed and they cannot both describe
the same silicon function.

Most likely: the X4 uses GPIO20 for USB presence, and the X3 repurposed it when
the RTC, gauge and IMU were added. **Unverified.** See
[`../gaps-and-conflicts.md`](../gaps-and-conflicts.md).

## Flashing over USB

The C3's USB-serial-JTAG is the flash path — **when the unit is not USB-locked**.
See [`../development.md`](../development.md).

## Status

`reported-working` for charging and flashing. `unverified` for the `usbDetect` pin.
