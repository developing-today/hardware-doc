# How do I read touch input? — ESP32-P4-WIFI6-Touch-LCD-3.4C

> Evidence status: **vendor documentation + vendor source code. Untested on hardware.**
> Applies equally to the [4C](../../esp32-p4-wifi6-touch-lcd-4c/README.md).

## Capability summary

Capacitive multi-touch on the shared I²C bus.

> **The fitted part is a Goodix GT9271, not a GT911.** Waveshare's own hardware audit states:
> *"The official controller is GT9271; the software uses a GT911-compatible driver/API."*
>
> This matters for expectations, not for code: the GT9271 is the higher-point-count sibling, and
> the whole software stack — vendor BSP included — drives it through the GT911 driver. Our local
> [GT911 record](../../../../components/goodix/gt911/README.md) still applies to the *driver*
> contract; the *part* is documented at
> [`components/goodix/gt9271`](../../../../components/goodix/gt9271/README.md).

## Hardware path

```
GT911 (on panel FPC) --I2C--> ESP32-P4
                              SDA = GPIO7
                              SCL = GPIO8
```

| Resource | Value | Evidence |
|---|---|---|
| Controller (fitted) | **GT9271** | Waveshare `docs/HARDWARE.md` |
| Driver API used | GT911-compatible | `esp_lcd_touch_gt911`; vendor BSP 3.0.1 |
| Bus | I²C, **SDA GPIO7 / SCL GPIO8** | `displays_config.h`, `i2c.h` |
| Clock | 100 kHz or 400 kHz | conflicting vendor values — see below |
| Max points | 5 as configured | `ESP_LCD_TOUCH_MAX_POINTS` in Waveshare's library |
| I²C address | **probe `0x5D`, then `0x14`** | Vendor BSP contract |
| Reset GPIO | **23** (`TP_RST`) | Schematic, `R62` 0 Ohm |
| Interrupt GPIO | **not wired to the SoC** | Schematic — see below |

## ESP-IDF — use the vendor BSP

The published BSP already implements the correct touch contract; prefer it over wiring this up
yourself:

```yaml
dependencies:
  waveshare/esp32_p4_wifi6_touch_lcd_xc: "3.0.1"
```

Waveshare describe the contract explicitly: the BSP *"deliberately sets both touch reset and
interrupt to `GPIO_NUM_NC`, installs no interrupt handler, probes I2C address `0x5D` and then
`0x14`, and initializes the address that responds."*

Leaving **reset** unconfigured is deliberate too — driving it would alter the address/reset strap
behaviour. Do not "fix" this by wiring GPIO23 into the driver.

If you must do it manually:

```yaml
dependencies:
  esp_lcd_touch_gt911: "*"    # pin a version in real projects
```

```c
esp_lcd_touch_handle_t tp = NULL;
esp_lcd_touch_config_t cfg = { /* x_max/y_max = panel resolution */ };
esp_lcd_touch_new_i2c_gt911(io_handle, &cfg, &tp);

esp_lcd_touch_read_data(tp);
esp_lcd_touch_get_coordinates(tp, x, y, strength, &count, max_points);
```

Set `x_max`/`y_max` to **800 × 800** on the 3.4C and **720 × 720** on the 4C. Using the wrong pair
yields coordinates that are scaled or clipped rather than absent — a subtle failure.

## Arduino

Waveshare ship `gt911.cpp` / `touch.cpp` in their `displays` library, wired to the same GPIO7/8
bus via `i2c.h`. Using their library is the path of least resistance since it already carries the
correct pins.

## The shared I²C bus is the main constraint

| Device | Bus | Note |
|---|---|---|
| GT911 touch | I²C GPIO7/8 | |
| ES8311 codec | **same bus** | |
| ES7210 echo-cancel ADC | **same bus** | |

Three devices share one bus. Consequences that actually matter:

- A single device holding the bus low stalls **touch and audio together**. Symptoms can look like
  a touch problem when the cause is a codec.
- Touch polling rate competes with audio control traffic. Audio control writes are infrequent, so
  this is usually tolerable, but it is not free.
- `03_i2c_tools` in the shared demo archive is the correct **first** diagnostic: scan the bus and
  confirm all three devices answer before debugging anything higher up.

### Clock rate conflict

Waveshare's own code disagrees: `displays_config.h` sets `i2c_clock_speed = 100000`, while
`i2c.h` sets `EXAMPLE_I2C_MASTER_FREQUENCY (400 * 1000)`. Treat **400 kHz as supported** and
**100 kHz as the conservative fallback**. If touch is erratic, drop to 100 kHz first — it is a
one-line change and rules out signal-integrity issues on a bus with three loads.

Recorded as [C8](../gaps-and-conflicts.md#c8--i²c-clock-rate--resolved-2026-08-26).

## The interrupt line is not connected to the SoC

Resolved from the schematic on 2026-08-24.

`TP_INT` leaves FPC connector pin 6, passes through a **populated 0 Ohm resistor**, and terminates
at **test point TP2**. No GPIO appears on the resistor's far terminal, and `TP_INT` occurs nowhere
else on the schematic.

**Poll the GT911. There is no interrupt to attach to.**

```c
esp_lcd_touch_config_t cfg = {
    .x_max = 800, .y_max = 800,      // 720/720 on the 4C
    .rst_gpio_num = GPIO_NUM_23,     // TP_RST - wired
    .int_gpio_num = GPIO_NUM_NC,     // TP_INT - goes to test point TP2 only
};
```

This is an argument from absence, so it is **high confidence rather than certainty**. TP2 is the
bodge point if you need a real interrupt.

Touch **reset is** wired, on **GPIO23** through `R62`.

> Values like `EXAMPLE_TOUCH_GPIO_INT (GPIO_NUM_3)` appear elsewhere in the demo archive. They
> belong to **bundled upstream examples for other boards**. Do not use them.

Recorded as [C11](../gaps-and-conflicts.md#c11--touch-interrupt-is-not-wired-to-the-soc).

## Limits

| Limit | Value | Kind |
|---|---|---|
| Simultaneous points | 5 | Vendor library config |
| Coordinate range | panel resolution | Board |
| Report rate | **Unknown — not measured** | — |

## Pitfalls

1. Wrong `x_max`/`y_max` for the variant → silently wrong coordinates.
2. Configuring an interrupt pin. There is none — set `int_gpio_num` to `GPIO_NUM_NC` and poll.
3. Debugging touch without first scanning the shared bus.
4. Ignoring that a wedged codec can present as a touch failure.

## Open questions

- Hardware confirmation of the responding address, coordinates, release events and polling
  behaviour. Waveshare state plainly that these remain **HIL-unverified** on their side too.
- Whether the GT9271's extra touch points are reachable through the GT911-compatible driver.
- Actual touch report rate.

## Related

- [GT911 component record](../../../../components/goodix/gt911/README.md)
- [Display](./display.md) · [Audio](./audio.md) — the other bus consumer
- [Gaps and conflicts](../gaps-and-conflicts.md)
