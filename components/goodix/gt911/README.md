# Goodix GT911 — capacitive touch controller

> 5-point projected-capacitive touch controller, I²C. Widely used on small and medium embedded
> touch panels. Record created **2026-08-24**.

- **Manufacturer:** Goodix (汇顶科技)
- **Part:** GT911
- **Function:** Capacitive touch screen controller
- **Interface:** I²C, plus INT and RST lines
- **Local datasheet:** [`artifacts/gt911-datasheet-rev-1.0.pdf`](./artifacts/gt911-datasheet-rev-1.0.pdf) — Rev 1.0

## Function and capabilities

| Item | Value |
|---|---|
| Touch points | Up to **5** simultaneous |
| Interface | I²C |
| I²C addresses | **`0x5D` primary, `0x14` backup** — selected at reset by INT/RST timing |
| Extra inputs | Up to 4 capacitive "keys" outside the active area |
| Signals | SDA, SCL, INT, RST |

The dual-address behaviour is the GT911's most common source of confusion. The address is not
strapped by a pin in the usual sense — it is latched from the **state of the INT line during the
reset sequence**. Get the reset timing wrong and the device answers at the *other* address, or at
neither. If a bus scan finds nothing at `0x5D`, check `0x14` before assuming the part is dead.

## Software

| Framework | Component / driver |
|---|---|
| ESP-IDF | `esp_lcd_touch_gt911` (Espressif component registry) |
| ESP-IDF API | `esp_lcd_touch_new_i2c_gt911()`, `esp_lcd_touch_read_data()`, `esp_lcd_touch_get_coordinates()` |
| Linux | `goodix` input driver (`drivers/input/touchscreen/goodix.c`) |
| Arduino | Multiple community libraries; vendors often ship their own |

Typical ESP-IDF use:

```c
esp_lcd_touch_handle_t tp = NULL;
esp_lcd_touch_config_t cfg = {
    .x_max = /* panel width  */,
    .y_max = /* panel height */,
    .rst_gpio_num = /* board-specific */,
    .int_gpio_num = /* board-specific */,
};
esp_lcd_touch_new_i2c_gt911(io_handle, &cfg, &tp);

esp_lcd_touch_read_data(tp);
esp_lcd_touch_get_coordinates(tp, x, y, strength, &count, max_points);
```

`x_max` and `y_max` must match the **panel's** resolution, not the framebuffer's. Mismatched
values produce coordinates that are scaled or clipped rather than absent — a quiet failure that
looks like poor calibration.

## Caveats and unsafe assumptions

1. **Address depends on reset timing**, not a strap pin. See above.
2. **The controller is usually on the panel FPC**, not the mainboard. Its INT/RST GPIOs are a
   property of the *board*, and cannot be inferred from the part number or from another board
   using the same controller.
3. **Firmware varies per panel.** Vendors load panel-specific configuration into the GT911.
   Coordinate orientation, resolution and key behaviour are therefore panel-specific; do not
   assume portability of a working config between boards.
4. **Do not copy INT/RST pin numbers between boards.** This is the most common way GT911 bring-up
   goes wrong.

## Used by

### Waveshare ESP32-P4-WIFI6-Touch-LCD-3.4C and 4C

> **These boards fit a GT9271, not a GT911** — see [`../gt9271/`](../gt9271/README.md). They are
> listed here because the entire software stack, including Waveshare's published BSP, drives the
> part through the **GT911-compatible** driver and API. This record describes that driver contract.

Both variants of the [shared XC platform](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md)
fit a GT911 on the round panel's FPC.

| Item | Value |
|---|---|
| Bus | I²C — **SDA GPIO7, SCL GPIO8** |
| Shared with | **ES8311 codec and ES7210 ADC on the same bus** |
| Clock | 100 kHz or 400 kHz — Waveshare's own sources disagree |
| Max points | 5, per Waveshare's library config |
| RST GPIO | **23** (`TP_RST`, via 0 Ohm `R62`) |
| INT GPIO | **not connected to the SoC** — terminates at test point TP2 |
| Coordinate range | 800 × 800 (3.4C) or **720 × 720** (4C) |

Because touch shares the I²C bus with both audio chips, a stalled codec presents as a touch
failure and vice versa. Scan the bus first.

**The interrupt line is not wired to the SoC.** Read from the schematic 2026-08-24: `TP_INT`
leaves the FPC, passes through a populated 0 Ohm resistor, and terminates at test point **TP2**.
Set `int_gpio_num = GPIO_NUM_NC` and **poll**. Reset *is* wired, on GPIO23.

This is a useful illustration of the second caveat above: the same GT911 part, on a board that
simply chose not to route its interrupt. See the device's
[touch guide](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/features/touch.md) and
[C11](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c11--touch-interrupt-is-not-wired-to-the-soc).

> Note the resolution differs between the two variants sharing this record. Use **720 × 720** on
> the 4C; using the 3.4C's 800 × 800 yields mis-scaled coordinates.

### [Xteink X4 Pro](../../../devices/xteink/x4-pro/README.md) — *added 2026-09-04*

The **only** touchscreen in the Xteink ESP32 family. On the shared I²C bus
**SDA 39 / SCL 38 @ 400 kHz**, at **0x5D** (alt 0x14), alongside a BM8563 RTC
(0x51) and a [CW2017 fuel gauge](../../cellwise/cw2017/README.md) (0x63).

| Signal | GPIO |
|---|---:|
| INT | **10** |
| RST | **4** |
| **Power enable** | **2 — ACTIVE-LOW** |

Three separate things each leave this controller **completely silent on the bus**
until fixed, and all three were hit during bring-up:

1. **The rail is gated by GPIO2 and it is active-LOW.** The OEM drives GPIO2 **LOW**
   (with GPIO1 HIGH) at boot. Driving it *high* — the naive "enable" — keeps the
   GT911 unpowered; an idle scan then shows only 0x51 and 0x63.
2. **RST = GPIO4, INT = GPIO10.** An earlier reverse-engineering pass had these
   two reversed.
3. **The reset must be long enough.** Too short a reset skips the internal config
   load and the config registers read back all-zero. The SDK uses
   **10 ms / 10 ms / 50 ms / 50 ms** with INT → INPUT.

**No host config upload.** The GT911 self-loads its internal config on the
standard reset dance, and **there is no GT911 config table anywhere in the OEM
firmware dump** (app0, app1, spiffs or nvs) — confirming the vendor relies on
self-load too.

**Point-frame layout:** `gt911CoordsAtByte0 = true` — coordinates start at **byte
0** of the `0x8150` read, not byte 1. The datasheet-standard layout puts a
track-id first; this panel does not. Getting it wrong shifts every coordinate by
one byte.

**Mounting:** the digitizer is **portrait on a landscape panel**, reporting
X: 0–480, Y: 0–800 on an 800 × 480 display → `swapXY = true`.

**Capacitive Home key:** the X4 Pro's "Home" pad is a **GT911 key bit**, status
`0x814E & 0x10`, *not* a GPIO. RE-confirmed that the OEM keys off exactly that
bit. Surfaced as `InputManager::wasHomeKeyPressed()`.

⚠ **Unresolved:** the FreeInk board header sets `flipY = true` commented *"confirmed
by corner-tap"*, while the same repository's device document says in two places
that `flipX`/`flipY` are **pending** a corner-tap test. See
[`devices/xteink/x4-pro/gaps-and-conflicts.md`](../../../devices/xteink/x4-pro/gaps-and-conflicts.md).

→ [`devices/xteink/x4-pro/features/touch.md`](../../../devices/xteink/x4-pro/features/touch.md)

## Artifacts

| File | Bytes | SHA-256 (prefix) | Provenance |
|---|---:|---|---|
| `artifacts/gt911-datasheet-rev-1.0.pdf` | 1,467,494 | `ca79a4ba` | Extracted from SensorLib 0.3.1 `datasheet/GT911 Rev.10.pdf`; originally bundled with <https://github.com/lewisxhe/SensorLib> |

**Redistribution status:** `unknown`. This is a Goodix datasheet redistributed inside an
MIT-licensed library; the MIT licence covers SensorLib's own code, **not** the bundled
third-party document. Kept in the repository; terms noted above.

Reacquire:

```bash
git clone https://github.com/lewisxhe/SensorLib.git
git -C SensorLib checkout v0.3.1
# -> SensorLib/datasheet/GT911 Rev.10.pdf
```

Goodix does not publish the GT911 datasheet openly; it typically circulates via module vendors and
library bundles. That makes this copy comparatively valuable and worth preserving.

## Open questions

- Whether a later datasheet revision than Rev 1.0 exists publicly.
- Official Goodix distribution channel for the datasheet and configuration tooling.
- Confirmation on hardware that the P4 round boards' `TP_INT` really has no SoC connection.

## Related

- [ESP32-P4-WIFI6-Touch-LCD-3.4C](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) · [4C](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md)
- [Hynitron CST816D](../../hynitron/cst816d/README.md) — a simpler single-point alternative used on the knob board
- [Components index](../../README.md)

---

## Programming Guide — retrieved 2026-09-11, and how it was found by accident

| Field | Value |
|---|---|
| Local path | [`artifacts/gt911-programming-guide-rev00-2014-08-04-crystalfontz-mirror.pdf`](artifacts/gt911-programming-guide-rev00-2014-08-04-crystalfontz-mirror.pdf) |
| **SHA-256** | `60c6c2284b482a7acdcd2747c47a9a7d25283235ccda8c688c10e2fd3216a98b` |
| **Bytes** | **477,454** |
| Pages | **31**, A4 |
| Source URL | <https://www.crystalfontz.com/controllers/UltraChip/UC8179/478/> |
| Source class | **credible mirror** — Crystalfontz, a display distributor |
| Retrieved | **2026-09-11**, HTTP 200, magic bytes `%PDF` |
| **Document title** | `GOODiX GT911 Programming Guide 2014-08-04_Rev.00` |
| Subject | *"GOODiX GT911 5-Point Capacitive Touch Controller Programming Guide"* |
| Applicability | *"firmware of version 1040 or later"* |
| Author | GOODiX, Shenzhen Huiding Technology Co., Ltd. |
| Producer / dates | Acrobat Distiller 9.0.0; created 2014-08-19, modified 2019-06-24 |
| Redistribution status | **`prohibited` as written** — the document's own first page reads *"**GOODIX CONFIDENTIAL** … Reproduction and/or distribution of this document in whole or in part is strictly prohibited without written consent of GOODIX"* |
| Disposition | `repository`, **unstaged — flagged for the user's decision**, see below |

**Text-layer validated** against the rendered page-1 heading (*"GT911 Programming
Guide (Applicable to firmware of version 1040 or later)"*) and the disclaimer
block.

### The URL is a trap, and it is why this file exists

This document was fetched while trying to obtain a **UC8179** datasheet.
`https://www.crystalfontz.com/controllers/UltraChip/UC8179/478/` returns a valid
PDF — of a **GOODiX touch controller**. The path segment `UltraChip/UC8179` is
decorative; only the trailing number selects a document, and `478` is the GT911
guide. The UC8179 document is `517`.

The file is retained here rather than discarded because **it is the right
document for this component**, filed by what it *describes* rather than by what
was being researched — and because a near-identical mis-file is exactly the
failure this repository's conventions exist to prevent.

### What it adds

Register-level detail the board profiles do not carry: the real-time command
registers, the full configuration block, the coordinate-information layout at
`0x814E`/`0x814F`/`0x8150`, command-status registers, HotKnot registers, the
power-on timing diagram, and **I²C address selection during power-on or reset** —
which is the mechanism the X4 Pro's `beginGt911()` drives with INT held at a
level across the RST pulse to choose between `0x5D` and `0x14`.

It also explains a detail a third party observed on a physical X4 Pro: the Home
pad is a **GT911 touch key**, reported in bit 4 of `0x814E` with its key byte
immediately after the last point record at `0x814F + 8·count` — and that the
Linux `goodix.c` driver reads it the same way.

### ⚠ Decision required from the user

**This document declares itself confidential and forbids redistribution without
GOODiX's written consent.** It is widely mirrored by distributors, which does not
constitute permission. It is left **unstaged**, and the options are:

1. keep it unstaged in the working tree (current state);
2. move it to the local archive with a placeholder carrying this hash, size and
   the reacquisition URL;
3. delete the bytes and keep only this metadata block as the acquisition record.

**Used by:** [Xteink X4 Pro](../../../devices/xteink/x4-pro/README.md) — the only
Xteink device with a touchscreen.
