# X4 Pro — battery and power

> CW2017 I²C fuel gauge, a GPIO charge-status line, three power rails and a
> pogo-pin charge connector. Evidence: hardware-confirmed except capacity.
> Last verified 2026-09-04.

## Capability summary

| Item | Value |
|---|---|
| Fuel gauge | **CW2017** @ I²C **0x63** — [`cellwise/cw2017`](../../../../components/cellwise/cw2017/README.md) |
| Charge status | **GPIO21**, **active-HIGH** = charging |
| Battery ADC | **none** (`batteryAdc = PIN_UNASSIGNED`) |
| VBUS / USB detect | **not conclusively identified** |
| Charge connector | **magnetic pogo pins** — no USB-C charge port |
| Capacity | **UNKNOWN** — no teardown, no vendor spec |
| Charger IC | **not on the I²C bus**; part unidentified |

## The CW2017 needs a battery profile or it lies

**The CW2017 reports 0 % until an 80-byte BATINFO battery profile is loaded**
into registers `0x10`–`0x5F`. `BatteryMonitor` verifies the resident profile and
re-uploads the OEM table — recovered from app1's `Cw2017PowerHal` via Ghidra — if
it is missing.

Then:
- **SoC** from register `0x04`
- **VCELL** from registers `0x02`/`0x03`, 14-bit, `mV = (raw·5 + 8) >> 4`

This is the highest-consequence software fact on this device's power path: a
firmware that talks to the gauge without the profile shows a permanently flat
battery.

## Charging state is not observable from the gauge

The CW2017 has **no current register**, and there is **no charger IC on the gauge
bus**. Stock instead reads a **charger `STAT` line on GPIO21**, configured
input/no-pull and read **active-HIGH** (raw level = charging).

Evidence: `Cw2017PowerHal` vtable slot 3 → GPIO getter at IROM `0x4214f67c`,
pin `0x15` (= 21) set in board init `0x4214eeb0`.

`BatteryMonitor` falls back to this pin when the gauge reports charging as
unobservable. Carried as `batteryChargeStatus = 21` +
`batteryChargeStatusActiveHigh = true`.

**The VBUS/USB-detect pin remains unidentified** — stock's battery icon uses the
GPIO21 charge state, not a USB-presence signal.

## Power rails and boot order

| Rail | GPIO | Level | Role |
|---|---:|---|---|
| Master peripheral | **1** | HIGH | Asserted **first**. Panel + SD + touch depend on it |
| Touch | **2** | **LOW** | Active-low. GT911 unpowered until LOW |
| SD | **5** | **LOW** | Active-low. Pulse HIGH→LOW, hold LOW |

Carried as `power.latch0 = {1}` so `holdPowerRails()` asserts GPIO1 early.
Without it: *"EPD BUSY never asserts, SD returns 0xFF."*

## Deep sleep

The sleep path drives each enable to its **off level by polarity**, which on this
board means driving GPIO2 and GPIO5 **HIGH**. Implemented, but the SDK notes a
power-draw check is still **pending** — no measured sleep current exists.

## The pogo connector

The X4 Pro charges over a **magnetic pogo-pin connector**, not USB-C. Required
accessories, both sold separately:

| Accessory | Price (2026-09-04) |
|---|---|
| Magnetic Pogo Pin Charging Cable for X3 & X4 Pro | $4.99 |
| Magnetic Charging Adapter for X3 & X4 Pro | $5.99 |

This is the most-contested design decision in the product's community reception —
71 comments on [r/xteinkereader `1v2txxe`](https://old.reddit.com/r/xteinkereader/comments/1v2txxe/).
The native USB peripheral (GPIO19/20) still exists for data.

## Unknowns

- **Battery capacity.** The X3 is 650 mAh by teardown; the X4 Pro is unmeasured.
- **Charger IC part number.** Not on I²C; the X3 uses a "TP4056-class" part per
  its Chinese teardown, but that is a different board.
- **Sleep current.** Never measured.
- **Runtime.** No figure from any source.

## Status

`hardware-confirmed` for gauge, STAT pin and rails. `unknown` for capacity,
charger part, current draw and runtime.
