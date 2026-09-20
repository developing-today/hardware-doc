# T-Display-S3 — deep sleep

> **No current measurement exists for this board**, from LilyGO or from this pass. What follows
> is the mechanism and the known traps, clearly separated from the numbers we do not have.

## Reference example

`examples/Sleep/Sleep.ino` @ **`ec889e789b3cf093412689a143f7f37b42b56af7`** — LilyGO's own,
and the only vendor guidance. It uses the standard `esp_sleep_*` API.

## What to switch off before sleeping

In this order:

```cpp
// 1. Backlight
digitalWrite(38, LOW);
// 2. Put the panel to sleep (controller-level), then
// 3. Drop the whole V3V rail — panel, 3V header pin, touch controller
digitalWrite(15, LOW);
// 4. Hold GPIO15 low through sleep, or it floats and the rail may come back
gpio_hold_en((gpio_num_t)15);
gpio_deep_sleep_hold_en();
// 5. Sleep
esp_sleep_enable_ext0_wakeup((gpio_num_t)0, 0);   // BOOT button, active low
esp_deep_sleep_start();
```

**Step 4 is the one people miss.** Without `gpio_hold_en()`, GPIO15 is released when the
digital core powers down, and the rail's behaviour then depends on the gate's pull network —
which was not traced by this pass ([`../gaps-and-conflicts.md`](../gaps-and-conflicts.md) K3).
Holding it is cheap and removes the question.

## Wake sources

| Source | Pin | Works |
|---|---|---|
| `ext0` / `ext1` | GPIO0 (BOOT), GPIO14 | yes, both are RTC-capable |
| Timer | — | yes |
| Touch IRQ | GPIO16 | RTC-capable, **but** the controller is on the gated rail, so it cannot signal if you dropped `V3V` |
| ULP | — | supported; `examples/ULP_ADC` and `examples/ULP_Count` exist in the repo and note they need *"arduino_esp32 version: 3.0.0-rc3"* — i.e. **a core newer than the 2.0.14 the rest of the repo pins**. That is an internal contradiction in LilyGO's own repo, recorded here |

## The pins that go high in sleep

Firsthand report, [issue #313](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/313)
(2025-07-28), MicroPython:

> "After I do LOW it turns off and stays off during 10 seconds of normal sleep, but immediately
> when I go into deep sleep mode it turns on again with a weak light."

Cause, confirmed by LilyGO with PCB photographs: **fitted pull-up resistors on GPIO16 and
GPIO17**. When the driver stops holding them low at sleep entry, they go high. If anything is
connected to those pins it will be driven — and it will also **draw current for the whole sleep
period**, which is the part the reporter did not raise but which matters for a battery device.

Mitigation: `gpio_hold_en()` on 16 and 17 as well, or remove the resistors (LilyGO's own
suggestion; they are on the back of the panel).

## The other sleep-current unknown

The battery-sense divider is two `100K` resistors. If it is permanently across `VBAT` — i.e. if
`Q4` does not disconnect it — that is **≈ 21 µA at 4.2 V**, continuously. On a board whose
whole deep-sleep budget is plausibly in the hundreds of microamps, that is not negligible, and
it is exactly what was not established. See
[`battery-voltage-measurement.md`](battery-voltage-measurement.md) §5.

## Numbers we have, and their provenance

| Figure | Board | Source | Applies here? |
|---|---|---|---|
| ~230 µA deep sleep, external GPIO0 wake | T-Display-S3 **AMOLED** | `LilyGo-AMOLED-Series/README.MD` @ `6d1dc00`, vendor table | **No.** Different display, different regulators, different charger. Quoted only for order of magnitude |
| ~1.1 mA deep sleep, timer wake | T-Display AMOLED **Lite** | same table | No |
| 90–230+ mA active at 240 MHz with Wi-Fi | AMOLED boards | same table | Roughly, since the SoC dominates |

**LilyGO publishes no deep-sleep figure for the base T-Display-S3.** Anyone quoting one is
quoting a different board.

## Also relevant

`USB CDC On Boot` interacts with sleep in a way that surprises people: on wake, if CDC is
enabled and no host is attached, the core can block again. Battery devices should build with
`-UARDUINO_USB_CDC_ON_BOOT`. See [`usb.md`](usb.md).
