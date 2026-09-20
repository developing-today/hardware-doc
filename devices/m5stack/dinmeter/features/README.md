# DinMeter — feature guides

Task-oriented guides, one per capability. Each answers a natural question and states its
evidence status, applicable revisions and framework versions.

Applies to **K134 and K134-V11** unless a guide says otherwise — the two boards share a
byte-identical published schematic and an identical GPIO map.

| Guide | Question it answers | Hardware |
|---|---|---|
| [`rotary-encoder-and-buttons.md`](rotary-encoder-and-buttons.md) | How do I read the orange knob and its press? | encoder on `J5` → GPIO41/40/42 |
| [`display.md`](display.md) | How do I draw on the screen and dim it? | ST7789V2/P3 on `FPC1` → GPIO4-9 |
| [`rtc-and-timekeeping.md`](rtc-and-timekeeping.md) | How do I keep time and wake on a schedule? | BM8563 `U5` → GPIO11/12 |
| [`buzzer.md`](buzzer.md) | How do I make it beep? | `LS1` via `Q5` → GPIO3 |
| [`power-and-battery.md`](power-and-battery.md) | How do I run it from 24 V or a cell, and why does it keep switching off? | `U1`/`U2`/`U3`/`U4`, latch on GPIO46 |
| [`porta-portb-expansion.md`](porta-portb-expansion.md) | How do I hang a sensor off the Grove ports? | `J3`/`J4` → GPIO13/15 and GPIO1/2 |
| [`wifi-and-ble.md`](wifi-and-ble.md) | How do I get on the network? | ESP32-S3 radio + module antenna |
| [`rgb-led.md`](rgb-led.md) | How do I light the status LED — and why doesn't it work on v1.1? | WS2812B-2020 inside the Stamp, GPIO21 (+GPIO38 on v1.1) |
| [`din-mounting-and-mechanical.md`](din-mounting-and-mechanical.md) | How do I mount it in a panel? | 1/32 DIN, 45 × 22.5 mm cutout |

**Global evidence caveat.** No DinMeter hardware was available for this research pass. Code in
these guides is `inferred` or `reported-working` (i.e. it is the vendor's own example code)
unless a line says otherwise. None of it was compiled or run here.

See also [`../coverage.md`](../coverage.md) for the feature → evidence → gap matrix, and
[`../resources-and-conflicts.md`](../resources-and-conflicts.md) for what collides with what.
