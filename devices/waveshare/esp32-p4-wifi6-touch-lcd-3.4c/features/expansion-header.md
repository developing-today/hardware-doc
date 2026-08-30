# How do I use the 40-pin expansion header? — ESP32-P4-WIFI6-Touch-LCD-3.4C

> Evidence status: **schematic-derived, corroborated by the vendor's own GPIO count.
> Untested on hardware.** Applies equally to the [4C](../../esp32-p4-wifi6-touch-lcd-4c/README.md).

## ⚠️ Read this before connecting anything

**This is not a Raspberry Pi header, and 12 of its 40 pins have unidentified power/ground roles.**

| | This board | Raspberry Pi |
|---|---|---|
| Power/GND pins | 1, 2, 3, 10, 14, 17, 24, 25, 30, 33, 38, 40 | 1, 2, 4, 6, 9, 14, 17, 20, 25, 30, 34, 39 |

Only six of twelve coincide, and the mismatches are decisive:

- **Pin 4 is a GPIO here, but 5 V on a Pi.**
- **Pin 6 is a GPIO here, but GND on a Pi.**

A HAT built to Pi conventions would drive 5 V into a GPIO. Waveshare's own wording is
*"compatible with **some** Raspberry Pi HATs (**requires pin header adapter**)"* — read both
qualifiers literally.

**Verify every connection with a meter before fitting any HAT.**

## What the header carries

Designator **`J8`**, 2 × 20, 2.54 mm pitch.

| Group | Signals |
|---|---|
| GPIO (24) | 2, 3, 4, 5, 20, 21, 22, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 46, 47, 48, 49, 50, 51, 52 |
| I²C | `ESP_I2C_SDA` (GPIO7) pin 39, `ESP_I2C_SCL` (GPIO8) pin 37 |
| USB | `USB1P1_N` pin 15, `USB1P1_P` pin 16 |
| Power | `ESP_3V3`, `VCC_5V`, 9 × `GND` — **positions not individually identified** |

**28 signal pins + 12 power/GND = 40.** That split is corroborated: Waveshare's Chinese storefront
states *"引出 **28** 个剩余可编程 GPIO 接口"* — 28 remaining programmable GPIO interfaces. Two
independent derivations agreeing is good evidence none were missed, though it still does not tell
you which pin is 5 V.

Full per-pin table: [`pinouts-and-buses.md`](../pinouts-and-buses.md#40-pin-expansion-header-j8).

## The I²C pins are the shared bus

Pins 37/39 are **the same physical bus** as the GT9271 touch controller, ES8311 codec, ES7210 ADC
and the camera's SCCB control. Four device families already sit on GPIO7/8.

Practical consequences for anything you attach:

- **Check the address first.** Touch answers at `0x5D` or `0x14`; the codecs have their own. A
  collision breaks whichever device loses.
- **A stuck peripheral takes out touch, audio and camera together.** Symptoms will not point at
  your add-on board.
- Run `03_i2c_tools` before and after connecting anything, and compare.
- Bus capacitance rises with every device, which interacts with the unresolved
  100 kHz vs 400 kHz question ([C8](../gaps-and-conflicts.md#c8--i²c-clock-rate--resolved-2026-08-26)).

There is also a dedicated SH1.0 4-pin I²C header **`J6`** (GND, 3V3, SDA, SCL) — a Qwiic/STEMMA-style
breakout of the same bus. For simple I²C peripherals it is tidier than the 40-pin header, with
identical sharing caveats.

## Using the GPIOs

Nothing special — standard ESP-IDF:

```c
gpio_config_t io = {
    .pin_bit_mask = 1ULL << 47,        // any GPIO from the list above
    .mode = GPIO_MODE_OUTPUT,
};
gpio_config(&io);
```

Before choosing a pin, check it against the [full pinout](../pinouts-and-buses.md) — the header
GPIOs are distinct from the display, audio, SD and touch pins, but confirm rather than assume.

## Limits and unknowns

| Item | Status |
|---|---|
| Signal pins | **28**, mapped |
| Power/GND pins | **12, roles unidentified** |
| Logic level | 3.3 V (ESP32-P4) |
| Per-pin current | Not established for this board |
| 5 V rail current budget | **Unknown** |
| Pi HAT compatibility | **Per-HAT; not general** |

## No example exists

**No official or community example uses this header.** It is an advertised capability with zero
demonstrated use, which is worth weighing if you are planning to depend on it.

## Pitfalls

1. **Treating it as a Pi header.** The single most likely way to damage something.
2. **Connecting to an unidentified power pin.** Twelve of forty. Meter first.
3. **Adding an I²C device without an address check.** Four families already share the bus.
4. **Assuming a HAT's device tree or library maps across.** This is a GPIO breakout, not a Pi.

## Open questions

- Which of pins 1, 2, 3, 10, 14, 17, 24, 25, 30, 33, 38, 40 are 5 V, 3V3 and GND.
- Current budget on `VCC_5V` and `ESP_3V3`.
- What `USB1P1_N/P` on pins 15/16 connect to — the same controller as the Type-A port, or a second
  interface. See [usb.md](./usb.md).
- Which HATs, if any, Waveshare have actually validated.

## Related

- [Full pinout, including the per-pin table](../pinouts-and-buses.md#40-pin-expansion-header-j8)
- [Touch](./touch.md) · [Audio](./audio.md) · [Camera](./camera.md) — the other bus users
- [USB](./usb.md) — the header's USB pair
