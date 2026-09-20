# Touch — M5Stack PaperMono

> **How do I read touch input, and why can I not press the edge of the screen?**
> Hardware revision **V0.6.2** · snapshot **2026-09-01** · nothing tested on hardware.

## 1. Capability summary and the hardware path

A self-capacitance projected-capacitive touch layer laminated to the e-paper stack,
read by a FocalTech controller on the shared system I²C bus, with an interrupt line
straight to the ESP32-S3 that doubles as a **wake source**.

```
FT6336G (I2C 0x38)  ──SDA/SCL──▶ system I²C bus (GPIO47/48)
      │  INT ─────────────────▶ ESP32-S3 GPIO4     (wake source)
      │  RSTN ◀──────────────── M5IOE1 IO6
      └  VDD  ◀──────────────── TP_VDD, AW35122 load switch, enabled by M5IOE1 IO13
```

| Element | Part | Record |
|---|---|---|
| Touch controller | FocalTech **FT6336G**, I²C `0x38` | [`components/focaltech/ft6336g`](../../../../components/focaltech/ft6336g/README.md) |
| Reset + power enable | M5IOE1 `IO6` / `IO13` | [`components/m5stack/m5ioe1`](../../../../components/m5stack/m5ioe1/README.md) · [`io-expander.md`](io-expander.md) |
| Power switch | Awinic `AW35122` load switch (`U18`) | [`components/awinic/aw35122`](../../../../components/awinic/aw35122/README.md) |
| Connector | `J4`, 8-pin FPC | [`../pinouts-and-buses.md`](../pinouts-and-buses.md#connectors) |

## 2. ⚠ The effective touch area is smaller than the display

**This is the fact that will cost you a UI redesign if you learn it late.**

M5Stack, on the product page:

> "The touch IC firmware internally shrinks the touch boundary. The effective touch
> coordinate range is limited to: **X-axis: 5 ~ 475** (total width 480 px),
> **Y-axis: 5 ~ 795** (total height 800 px)."

| Axis | Panel | **Usable touch** | Dead border |
|---|---|---|---|
| X | 0 – 479 (480 px) | **5 – 475** (471 px) | 5 px leading, 4 px trailing |
| Y | 0 – 799 (800 px) | **5 – 795** (791 px) | 5 px leading, 4 px trailing |

This is a property of firmware **inside the touch controller**. It is not mechanical, it
is not a driver setting, and **a host cannot widen it.** Consequences:

- **Never place a hit target within 5 px of any screen edge.** A button drawn flush to
  the edge has a strip that cannot be pressed.
- **Edge-swipe gestures that begin at coordinate 0 will never register.** If your UI
  design leans on edge swipes, it will not work here.
- Full-screen "tap anywhere to wake" is fine. Corner affordances are not.

### Does M5GFX compensate? No — and that is the right answer

M5GFX configures the touch object with `x_min = 0, x_max = 479, y_min = 0, y_max = 799`
(`M5GFX/src/M5GFX.cpp:2135–2138`). That is an **identity mapping** — the controller's raw
coordinates are passed through unscaled.

So there is **no scale error and no systematic offset**: reported coordinates are true
pixel coordinates. The only consequence is that values below 5 or above 475 / 795 are
never emitted. This resolves an open question left in the
[FT6336G component record §4.4](../../../../components/focaltech/ft6336g/README.md),
which speculated about a possible ~2 % scale error from a full-range assumption. There is
no rescale, so there is no such error. `executed-success` on the source read;
`not-tested` on hardware.

## 3. Prerequisites

| Item | Value |
|---|---|
| M5Unified / M5GFX | 0.2.21 / 0.2.28 — `lgfx::Touch_FT5x06` is registered automatically for `board_M5PaperMono` |
| Power state | **L3B** — `TP_VDD` comes up via M5IOE1 `IO13` during `M5.begin()` |
| I²C | Bus configured by M5GFX at **400 kHz** for the touch object, on `I2C_NUM_1` |

## 4. Resources consumed

| Resource | Value |
|---|---|
| I²C address | **`0x38`** on the shared bus (GPIO47 SDA / GPIO48 SCL) |
| I²C port / speed | `I2C_NUM_1`, `freq = 400000` in the M5GFX touch config |
| ESP32-S3 GPIO | **GPIO4** — `INT`, also the deep-sleep touch-wake pin |
| Expander pins | `IO6` reset, `IO13` `TP_VDD` enable |
| Rail | `TP_VDD` (state L3B) |

## 5. Minimal procedure (`inferred`)

```cpp
#include <M5Unified.h>

void setup() {
  M5.begin(M5.config());          // touch comes up with the display
  M5.Display.setEpdMode(epd_mode_t::epd_fast);
}

void loop() {
  M5.update();                    // required - polls the touch controller
  if (M5.Touch.getCount() > 0) {
    auto t = M5.Touch.getDetail();
    if (t.wasPressed()) {
      M5.Display.fillCircle(t.x, t.y, 6, TFT_BLACK);
      M5.Display.display();
    }
  }
}
```

`M5.Touch.getCount()`, `M5.Touch.getDetail()` and `M5.Touch.getTouchPointRaw()` are the
three entry points the vendor's own firmware uses
(`M5PaperMono-UserDemo/main/hal/hal_touch.cpp:15`, `:20`, `:28`).

**Do not redraw the whole screen on every touch.** See
[`epaper-display.md` §8](epaper-display.md#8-panel-safety--the-rules-that-are-not-optional):
one full refresh per ten partials, and never a continuous partial-refresh loop. Touch
handling is exactly the code path that produces such a loop by accident.

## 6. Wake on touch

Sheet 1 of the schematic marks touch as an **L2 wake source**, and M5Unified implements
it in an unusual way worth knowing about:

```cpp
// M5Unified/src/utility/Power_Class.cpp:1654, :1786
uint_fast8_t wpin = _wakeupPin;                 // GPIO_NUM_1 (M5PM1 IRQ) by default
if (touch_wakeup && (M5.getBoard() == board_t::board_M5PaperMono)) {
  wpin = GPIO_NUM_4;                            // ... becomes the touch INT instead
}
```

**The `touch_wakeup` argument to `M5.Power.deepSleep()` does not add touch wake — it
substitutes it.** On this board it *replaces* the M5PM1 IRQ (GPIO1) as the EXT0 wake pin
with the touch INT (GPIO4). If you pass `touch_wakeup = true`, you get touch wake and you
lose the M5PM1's interrupt-driven wake path on the same call. `executed-success` on the
source read; `not-tested`.

Deeper sleep states (L1, L0) power the ESP32-S3 down entirely, and touch is not among the
sources that reach the M5PM1 — those are the power button, the
[RTC](rtc.md) and the [IMU](imu.md). See [`power-and-sleep.md`](power-and-sleep.md).

## 7. Silicon / board / framework / observed limits

| Class | Limit |
|---|---|
| **Silicon (FT6336G)** | **2 touch points maximum**, self-capacitance. No reliable independent tracking of two points — the classic two-point ghosting ambiguity applies. No pinch-zoom you should trust |
| **Silicon (FT6336G)** | 31 channels, panels **≤ 4.0 inch**. The 3.97" panel is at the ceiling |
| **Silicon (FT6336G)** | Controller firmware inset of 5 px on every edge (§2) — **unchangeable** |
| **Silicon (FT6336G)** | "Monitor mode" closes the I²C port; design for interrupt-driven reads rather than tight polling |
| **Board** | `RSTN` is behind the I²C expander. **Resetting touch requires a working I²C bus** — awkward when the reason you want to reset is that the bus is unhappy |
| **Board** | `TP_VDD` can be cut (M5IOE1 `IO13`); after a power cycle the driver must be re-initialised |
| **Framework** | M5GFX passes raw coordinates through unscaled (§2) |
| **Observed** | None. **Nobody has reported touch behaviour on real hardware** beyond one third-party project claiming touch works |

### The FT6336G datasheet does not contain the register map or the I²C address

Worth stating because it changes how you plan: you **cannot** write a driver for this
part from FocalTech's datasheet. Use `lgfx::Touch_FT5x06`, LVGL's FT6x06 driver,
`Adafruit_FT6206`, or read Linux's `drivers/input/touchscreen/edt-ft5x06.c`, which is the
de-facto public documentation of the register interface.

## 8. Conflicts and simultaneous use

| Combination | Verdict | Mechanism |
|---|---|---|
| Touch + [display](epaper-display.md) | ✅ intended | M5GFX resets both together by pulsing M5IOE1 `IO5`/`IO6` |
| Touch + six other I²C devices | ✅ | All addresses distinct. FT6336G tolerates 10 kHz–400 kHz, and the bus runs 100 kHz (IMU, M5PM1, M5IOE1) to 400 kHz (RTC, NFC, touch) per transaction |
| Touch + [NFC](nfc.md) | ⚠ bandwidth, not address | NFC polling is chatty on the same single bus. No measurement exists |
| Touch + [charger](battery-and-charging.md) access | ⚠ | Gating the IP2315 onto the bus is the one documented bus-stability hazard on this board. Keep it brief |
| Touch wake + M5PM1 IRQ wake | ❌ mutually exclusive on one `deepSleep()` call | §6 — `touch_wakeup` substitutes GPIO4 for GPIO1 |
| Touch + deep sleep below L2 | ❌ | Touch is not a wake source that reaches the M5PM1 |

## 9. Debugging

| Symptom | Cause |
|---|---|
| No touches at all | `TP_VDD` not enabled (M5IOE1 `IO13`), or touch reset (`IO6`) still asserted |
| Touch worked, then stopped after you poked the expander | You changed `IO6` or `IO13`. M5Stack's own warning: *"The pins associated with the e-paper display, touch controller, microSD, and PDM microphone are already used by M5Unified. Before modifying them, ensure that the corresponding peripheral has stopped"* |
| A button at the screen edge never fires | §2 — the 5 px dead border |
| Coordinates look mirrored or transposed | Display rotation vs `offset_rotation = 0` on the touch object; the panel is rotated in software but the touch layer is not |
| Second finger tracks erratically | Self-capacitance two-point ghosting — **silicon limit** |
| `0x38` missing from an I²C scan | Power (`IO13`) is off, or the scan ran before `M5.begin()` |

## 10. Unresolved questions

- **`J4`'s pin ordering was not resolved** from the schematic.
- **Nobody has reported real touch accuracy, latency or rejection behaviour** on a
  PaperMono. One third-party project
  (`MagicCube/free-ink-on-paper-mono`) claims a verified touch path on a Lite; no detail.
- Whether the display's rotation and the touch layer's orientation agree in every
  `setRotation()` value was not checked. A third-party ESPHome port explicitly labels its
  display/touch rotation section *"hipótesis de prueba"* — test hypothesis.

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**; touch is fitted on both C153 and C153-LITE |
| Framework range | M5Unified 0.2.21 · M5GFX 0.2.28 (touch is registered by board autodetect) |
| Evidence | Coordinate limit: **vendor-documented**, `reported-working`. Wiring and M5GFX config: **read from source**. Code sketch: **`inferred`** |
| Confidence | High on the coordinate limit and the wiring; **none on real-world touch quality** |
| Last verified | **2026-09-01** |

## Related

- [`../pinouts-and-buses.md#i²c-bus--the-one-shared-bus`](../pinouts-and-buses.md#i²c-bus--the-one-shared-bus)
- [`epaper-display.md`](epaper-display.md) · [`power-and-sleep.md`](power-and-sleep.md) · [`io-expander.md`](io-expander.md)
- [`components/focaltech/ft6336g`](../../../../components/focaltech/ft6336g/README.md) · [`components/awinic/aw35122`](../../../../components/awinic/aw35122/README.md)
