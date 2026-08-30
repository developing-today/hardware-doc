# Goodix GT9271 — capacitive touch controller

> Multi-point projected-capacitive touch controller, I²C. Driven in practice through the
> **GT911-compatible** driver API. Record created **2026-08-24**.

- **Manufacturer:** Goodix (汇顶科技)
- **Part:** GT9271
- **Function:** Capacitive touch screen controller
- **Interface:** I²C, plus INT and RST lines
- **Sibling / driver record:** [GT911](../gt911/README.md)

## Identity and the GT911 relationship

The GT9271 is a higher-point-count member of the same Goodix family as the GT911 and is
**register- and protocol-compatible enough** that the standard GT911 driver stack drives it
unmodified. That compatibility is not an assumption here — it is stated by the board vendor:

> *"The official controller is GT9271; the software uses a GT911-compatible driver/API."*
> — Waveshare, `docs/HARDWARE.md`, ESP32-P4-WIFI6-Touch-LCD-XC repository, retrieved 2026-08-24

Practical consequence: you use `esp_lcd_touch_gt911` / `esp_lcd_touch_new_i2c_gt911` and it works.
Do **not** conclude the parts are interchangeable in general — see the caveat below.

| | GT911 | GT9271 |
|---|---|---|
| Family | Goodix capacitive touch | same |
| Typical max points | 5 | **higher** — exact figure not established here |
| I²C addresses | `0x5D` / `0x14` | **same pair**, same reset-strap selection |
| ESP-IDF driver | `esp_lcd_touch_gt911` | **same driver used** |

> **Unresolved:** the GT9271's actual maximum touch-point count, and whether those extra points are
> reachable through the GT911-compatible driver or are capped at 5 by it. No GT9271 datasheet was
> obtained. Goodix do not publish these openly.

## Addressing and reset

Like the GT911, the I²C address is **latched from the INT line state during reset**, not strapped
by a dedicated pin — `0x5D` primary, `0x14` backup.

The robust approach, and the one Waveshare's BSP takes, is to **probe `0x5D` then `0x14` and use
whichever answers**, rather than assuming.

If a board does not route INT and RST to the SoC, leave both `GPIO_NUM_NC` and do not attempt to
drive the strap — changing it mid-flight can move the device to the other address.

## Software

| Framework | Driver |
|---|---|
| ESP-IDF | `esp_lcd_touch_gt911` — via `esp_lcd_touch_new_i2c_gt911()` |
| Linux | `goodix` input driver (`drivers/input/touchscreen/goodix.c`) |
| Arduino | Vendor-supplied `gt911.cpp` / `touch.cpp` in board libraries |

## Caveats

1. **"GT911-compatible" is a software statement, not an electrical one.** It means the driver
   works. It does not license you to swap parts, assume identical timing, or reuse a panel
   configuration.
2. **Address depends on reset timing.** Probe both.
3. **The controller sits on the panel FPC**, so its INT/RST routing is a property of the *board*.
   Never infer those GPIOs from the part number.
4. **Panel-specific firmware.** Goodix controllers carry vendor-loaded configuration; coordinate
   orientation and resolution do not transfer between panels.
5. **No datasheet obtained.** Everything here is from vendor board documentation and driver
   behaviour, not from Goodix.

## Used by

### Waveshare ESP32-P4-WIFI6-Touch-LCD-3.4C and 4C

Both variants of the [shared XC platform](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md)
fit a GT9271 on the round panel's FPC.

| Item | Value |
|---|---|
| Bus | I²C — **SDA GPIO7, SCL GPIO8** |
| Shared with | ES8311 codec and ES7210 ADC on the same bus |
| Address | probe **`0x5D`** then **`0x14`** |
| Reset (`TP_RST`) | **GPIO23**, via 0 Ω `R62` — **left `GPIO_NUM_NC` in software by design** |
| Interrupt (`TP_INT`) | **not routed to the SoC** — terminates at test point **TP2** |
| Driver | GT911-compatible, **polling only**, no ISR |
| Coordinate range | 800 × 800 (3.4C) or 720 × 720 (4C) |
| Vendor BSP | `waveshare/esp32_p4_wifi6_touch_lcd_xc` **3.0.1** |

This board is a clean illustration of caveat 3: the interrupt line exists on the FPC, passes
through a populated 0 Ω resistor, and goes to a **test point instead of a GPIO**. Touch is
therefore polled. Reset *is* wired but deliberately left unconfigured, because driving it would
disturb the address strap.

Waveshare are explicit that this contract is **compile-verified but not hardware-verified** on
their side either: the responding address, coordinates, release events and polling behaviour all
remain HIL-unvalidated.

Details:
[touch guide](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/features/touch.md) ·
[C11](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c11--touch-interrupt-is-not-wired-to-the-soc)

## Artifacts

None held. No GT9271 datasheet was located; Goodix do not publish it openly. The
[GT911 datasheet](../gt911/artifacts/gt911-datasheet-rev-1.0.pdf) is a useful proxy for the
register interface given the stated driver compatibility, but is **not** a GT9271 datasheet and
should not be cited as one.

## Open questions

- GT9271 maximum touch-point count.
- Whether a public GT9271 datasheet exists anywhere.
- Whether the extra points are exposed through the GT911-compatible driver.
- Which panel modules besides Waveshare's round DSI panels use this part.

## Related

- [GT911](../gt911/README.md) — the driver contract used to talk to this part
- [ESP32-P4-WIFI6-Touch-LCD-3.4C](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) · [4C](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md)
- [Components index](../../README.md)
