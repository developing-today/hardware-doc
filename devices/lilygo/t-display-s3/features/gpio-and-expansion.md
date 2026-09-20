# T-Display-S3 — GPIO, headers and expansion

## What is actually free

Start from 45 GPIOs and subtract:

| Consumed by | Pins | Count |
|---|---|---|
| In-package OPI PSRAM (ESP32-S3**R8**) | 26–37 | 12 |
| LCD 8080 bus | 5, 6, 7, 8, 9, 39, 40, 41, 42, 45, 46, 47, 48 | 13 |
| Backlight | 38 | 1 |
| `V3V` rail gate | 15 | 1 |
| Native USB | 19, 20 | 2 |
| UART0 — [unusable as GPIO under Arduino](../pinouts-and-buses.md#6-gpio43--gpio44-are-not-usable-as-gpio-under-arduino) | 43, 44 | 2 |
| Battery sense (only path) | 4 | 1 |
| Buttons | 0, 14 | 2 |
| I²C (with fitted pull-ups) | 17, 18 | 2 |
| Touch IRQ/RST — **16 has a fitted pull-up even on non-touch boards** | 16, 21 | 2 |

**Genuinely free and unencumbered: GPIO1, 2, 3, 10, 11, 12, 13** — seven pins, three of which
(11, 12, 13) you lose if you fit the TF Shield.

GPIO3 is the ESP32-S3's JTAG-source strapping pin; leaving it floating is fine, but do not
hold it at a fixed level at reset unless you know what you are asking for.

## Headers

Two 12-pin 0.1″ rows (`P1`, `P2` in the schematic, both `Header 12`) plus a 2-pin `P3`.
Sold **soldered** (`H577`) or **unsoldered** (`H569`) — that choice is a purchase option, not
a revision.

| Pin name | Value | Notes |
|---|---|---|
| `VBUS` | 5 V | **output only**, from USB-C. Cannot power the board |
| `VBAT` | 4.2 V | battery rail |
| `3V` | 3.3 V | **≤ 100 mA**, and **gated by GPIO15** |
| `GND` | — | |

The 100 mA figure is LilyGO's own. It is a real constraint: a GPS module or an SD breakout with
a burst current above that will brown out the rail your *display* is on.

## The SH1.0 4-pin connector

A 4-pin 1.0 mm connector carries the I²C bus (GPIO17/18) plus power and ground. LilyGO markets
it loosely as Qwiic-style.

**It is not Qwiic-compatible.** [Issue #181](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/181)
(2023-08-08, 12 comments, "None of my Qwiic (I2C) sensors is recognized") is what happens when
you assume otherwise: the connector is SH1.0, Qwiic is JST-SH 1.0 with a **defined pin order**,
and LilyGO's order is not guaranteed to match. Check continuity before plugging in a sensor —
a reversed power/ground pair kills the sensor, not the board.

The same connector is discussed in [issue #117](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/117)
where a user tried to hang a DS18B20 off it via GPIO43 and could not — that is the UART0
problem, not the connector.

## I²C bus sharing

One bus, GPIO17/18, with **10 kΩ pull-ups fitted on board** (`RIIC`, `RIID`). On a Touch board
the touch controller is already on it. Adding external devices works — different addresses —
but note:

- Two 10 kΩ pull-ups plus whatever your breakout adds can over-pull the bus. Most Qwiic
  breakouts fit 2.2–10 kΩ; three in parallel is too stiff for 3.3 V at 400 kHz on long wires.
- The CST touch parts NAK while idle, which confuses simple scanners.
- **Everything on this bus is on the GPIO15-gated rail.** Drop the rail, lose the bus.

## Add-on boards LilyGO sells for it

| Board | What it adds | SKU / price 2026-09-07 |
|---|---|---|
| **T-Display TF Shield** | 1-bit SDMMC microSD on GPIO11/12/13 | `H609` USD 2.51 · `H610` USD 2.38 |
| **T-Display-S3 MIDI** | MIDI in/out; own schematic `SCH_T-Display-S3-MIDI_V1.1.pdf` | `H656` USD 15.47 |
| **T-Display keyboard** | QWERTY keypad | `t-display-keyboard`, USD 6.88–30.98 |
| **T-Display-S3 Shell** | enclosure, grey or black | `L929`/`L930` USD 5.02 |

## Level and drive

3.3 V logic. No 5 V-tolerant pins. The ESP32-S3's per-pin drive is configurable up to 40 mA
but the sane working figure is 20 mA, and the **total** across the chip is the real limit.
