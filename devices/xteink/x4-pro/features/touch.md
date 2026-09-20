# X4 Pro — touch (GT911)

> Capacitive digitizer plus a capacitive Home key. **The only Xteink ESP32 device
> with touch.** Evidence: hardware-confirmed. Last verified 2026-09-04.

## Capability summary

| Property | Value |
|---|---|
| Controller | **GT911** — [`goodix/gt911`](../../../../components/goodix/gt911/README.md) |
| Bus | I²C SDA 39 / SCL 38 @ 400 kHz, shared with RTC + gauge |
| Address | **0x5D** (alt 0x14) |
| INT | GPIO **10** |
| RST | GPIO **4** |
| Power enable | GPIO **2**, **ACTIVE-LOW** |
| Mounting | **Portrait sensor on a landscape panel** → `swapXY = true` |
| Home key | GT911 key bit, status `0x814E & 0x10` |

## Three non-obvious things, each of which leaves the controller totally silent

The FreeInk bring-up notes are unusually explicit that **each of these
independently produced "no ACK on the bus"**:

1. **The rail is gated by GPIO2 and it is ACTIVE-LOW.** The OEM drives GPIO2
   **LOW** (with GPIO1 HIGH) at boot. Driving GPIO2 *high* — the naive "enable" —
   keeps the GT911 unpowered. An idle scan then shows only 0x51 and 0x63.
2. **RST = GPIO4, INT = GPIO10.** An earlier RE had these two reversed, which is
   why the first hardware attempt failed.
3. **The reset must be long enough.** The GT911 loads its own internal config on
   the standard reset dance; a too-short reset skips the load and the config
   registers read back all-zero. The SDK uses 10 ms / 10 ms / 50 ms / 50 ms with
   INT→INPUT.

**There is no GT911 config table anywhere in the OEM dump** (app0, app1, spiffs
or nvs), so the vendor relies on self-load too. Do not upload a config.

## Reset dance and addressing

```
RST LOW, INT driven to select level      → 2 ms
RST HIGH                                  → 8 ms
INT to INPUT + pull                       → 60 ms
probe
```

INT level as RST rises selects the address: **LOW → 0x5D**.

## Reading points

| Register | Meaning |
|---|---|
| `0x814E` | bit7 = data ready; low nibble = point count; **bit4 (`0x10`) = Home key** |
| `0x8150` | first point, 8 bytes per point |

**`gt911CoordsAtByte0 = true`** — coordinates start at **byte 0**, not byte 1.
The datasheet-standard layout puts a track-id first; this panel does not. Getting
this wrong shifts every coordinate by one byte and produces garbage.

## Orientation

The digitizer reports **X: 0–480, Y: 0–800** on an 800×480 landscape panel.
`swapXY` is applied first, then per-axis flip; `rawMinX/rawMaxX` describe the
**post-swap** axes.

**Unresolved:** the board profile sets `flipY = true` and comments *"confirmed by
corner-tap"*, while `docs/xteink-x4pro-support.md` says in two places that
`flipX`/`flipY` are still **pending** a corner-tap test. See
[`../gaps-and-conflicts.md`](../gaps-and-conflicts.md). Taps register and
navigate either way; only mirroring is at stake.

## Home key

Surfaced as `InputManager::wasHomeKeyPressed()` when
`touch.hasHomeKey = true`. RE-confirmed that the OEM keys off exactly
`0x814E & 0x10`. It is **not a GPIO** — do not look for one.

## Resource conflicts

Shares one Arduino `Wire` controller with the BM8563 and CW2017. Also note GPIO10
is listed elsewhere as a *candidate* for `usbDetect`; it is already the touch INT,
so that candidacy should be treated as almost certainly wrong.

## Status

`hardware-confirmed` — *"Touch wiring in the SDK profile: touch.powerEnable =
GPIO2 (active-low), INT=10/RST=4, swapXY = true, gt911CoordsAtByte0 = true, no
config upload."* **Open:** axis flip (documentation conflict).
