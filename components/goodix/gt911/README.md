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

## Artifacts

| File | Bytes | SHA-256 (prefix) | Provenance |
|---|---:|---|---|
| `artifacts/gt911-datasheet-rev-1.0.pdf` | 1,467,494 | `ca79a4ba` | Extracted from SensorLib 0.3.1 `datasheet/GT911 Rev.10.pdf`; originally bundled with <https://github.com/lewisxhe/SensorLib> |

**Redistribution status:** `unknown`. This is a Goodix datasheet redistributed inside an
MIT-licensed library; the MIT licence covers SensorLib's own code, **not** the bundled
third-party document. Held unstaged pending review.

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
