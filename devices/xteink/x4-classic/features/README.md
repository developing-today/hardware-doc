# Xteink X4 Classic — feature guides

**No per-feature guides are written for this device, deliberately.**

Every capability is documented in [`pinouts-and-buses.md`](../pinouts-and-buses.md)
and [`development.md`](../development.md), and there is **no owner, no build
report and no hardware experience anywhere** to write a task-oriented guide from.
Writing "how do I use the IMU on an X4 Classic" would mean paraphrasing the X4
Pro's guide with different pin numbers and implying an experience base that does
not exist.

Where a capability is shared with a sibling **and the sibling's guide is
evidence-backed**, use that guide and substitute the pins from this device's
pinout page:

| Capability | Guide to read | Pin deltas for the X4C |
|---|---|---|
| Display, controller variants | [X4 Pro display](../../x4-pro/features/display.md) | **DC 14, RST 10, BUSY 18** (permuted); controller from **NVS only**, no bus probe |
| microSD (native SDMMC) | [X4 Pro storage](../../x4-pro/features/storage.md) | power enable **GPIO6**, not GPIO5 |
| Battery / CW2017 gauge | [X4 Pro battery](../../x4-pro/features/battery-and-power.md) | same gauge, same STAT pin; **polarity PENDING** |
| RTC BM8563 | [X4 Pro RTC](../../x4-pro/features/rtc.md) | identical |
| IMU QMI8658 | [X3 IMU](../../x3/features/imu.md) | bus is **SDA 39 / SCL 38**, not SDA 20 / SCL 0 |
| USB | [X4 Pro USB](../../x4-pro/features/usb.md) | **USB-MSC is listed as supported here**, unlike the X4 Pro |
| Buttons | — | **Seven discrete interrupt-driven GPIOs**, not an ADC ladder. See [`pinouts`](../pinouts-and-buses.md#input--seven-discrete-interrupt-driven-buttons) |

**Not fitted:** touch, frontlight, audio, LEDs, PMIC, GPIO expander.
