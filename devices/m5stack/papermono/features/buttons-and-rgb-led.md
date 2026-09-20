# Buttons and RGB LED — M5Stack PaperMono

> **How do I read the buttons, and why can the indicator not show the colour I asked for?**
> Hardware revision **V0.6.2** · snapshot **2026-09-01** · nothing tested on hardware.

## 1. Capability summary and the hardware path

Three switches and one side-mounted RGB indicator, all on the **KEY/RGB/microphone
sub-board** (`PaperMono KEY RGB.SchDoc`, dated 2026-04-14), reaching the main board
through the 16-pin board-to-board connector `J6`.

```
S2 (KEY1) ──────────────▶ ESP32-S3 GPIO2      Button A
S3 (KEY2) ──────────────▶ ESP32-S3 GPIO3      Button B  (also a strapping pin)
S1 (PWR_BTN) ───────────▶ M5PM1 BTN_PU        on / off / reset / boot

RGB LED (RS-C1415MBAR)
   red   ◀── M5PM1  LED_EN_PP     <- no PWM
   green ◀── M5IOE1 IO8  (PWM2)
   blue  ◀── M5IOE1 IO9  (PWM1)
```

| Element | Where | Record |
|---|---|---|
| User keys | ESP32-S3 GPIO2 / GPIO3 | [`../pinouts-and-buses.md`](../pinouts-and-buses.md#esp32-s3-complete-pin-map) |
| Power button | M5PM1 `BTN_PU` | [`components/m5stack/m5pm1`](../../../../components/m5stack/m5pm1/README.md) |
| LED red die | M5PM1 `LED_EN_PP` | idem |
| LED green / blue dies | M5IOE1 `IO8` / `IO9` | [`components/m5stack/m5ioe1`](../../../../components/m5stack/m5ioe1/README.md) · [`io-expander.md`](io-expander.md) |
| LED part | `RS-C1415MBAR` | **No datasheet exists** — the only web occurrences anywhere are M5Stack's own pages |

## 2. ⚠ The red die has no PWM, so the colour set is limited

M5Stack says so themselves, on the product page:

> "The RGB LED indicator on the side of the PaperMono body consists of three color LED
> dies, with the **red LED connected to `LED_EN_PP` of the M5PM1**. After the device is
> powered on, it will light up according to the M5PM1 default behavior. **Since
> `LED_EN_PP` does not support PWM output mode configuration, the adjustable colors of
> this indicator will be limited.**"

This is a **board** limit — the red die is wired to a pin that is not a PWM output — and
it cannot be worked around in software. What you actually get:

| Channel | Control | Levels |
|---|---|---|
| **Red** | M5PM1 `LED_EN_PP`, via `PWR_CFG` (`0x06`) bit 4 | **on / off only** |
| Green | M5IOE1 `IO8`, PWM channel 2, 12-bit duty | graded |
| Blue | M5IOE1 `IO9`, PWM channel 1, 12-bit duty | graded |

So the indicator is best treated as **a red status light with a two-channel graded
accent**, not as a colour display. Any colour that needs partial red — orange, pink,
warm white, most pastels — is not reachable. Full red, full white-ish (R+G+B all on),
and the green/blue half of the colour wheel are.

### M5Unified is more limited still

`M5Unified/src/utility/led/LED_PaperMono_Class.cpp:53–80` implements `display()` as:

- **red** — threshold: `bitOn`/`bitOff` M5PM1 register `0x06` bit 4 at a 2048 cutoff
- **blue** — `ioe1.digitalWrite(gpio9, b >= 2048)` — **binary, not PWM**
- **green** — `ioe1.setPwmDuty12bit(pwm_ch2, g, normal, g > 0)` — the only true PWM channel

So through `M5.Led` the indicator is **red on/off × blue on/off × green graded**: eight
base combinations with one dimmable axis. Brightness is applied as
`br = (brightness+1)²`, the same squared curve as the [frontlight](frontlight.md#51-the-brightness-curve-is-squared-not-linear).

The vendor's own factory firmware does it differently — `hal_board.cpp:25–28` assigns
**green → `M5IOE1_PWM_CH2` and blue → `M5IOE1_PWM_CH1`**, both at 5 kHz
(`RGB_PWM_FREQ_HZ = 5000`), i.e. two graded channels. **Nothing documents why M5Unified
does not PWM blue.** The M5IOE1 manual's exclusion table lists `IO8 & IO9` as mutually
exclusive **for interrupts**, not for PWM, so a hardware reason is not evident. If you
want graded blue, drive the M5IOE1 directly as the factory firmware does. `inferred`,
`not-tested`.

## 3. Prerequisites

| Item | Value |
|---|---|
| M5Unified | 0.2.21 — `M5.BtnA` / `M5.BtnB` and `M5.Led` are wired up by board autodetect |
| M5IOE1 library | 1.0.9 if you drive green/blue directly |
| M5PM1 library | 1.0.7 if you configure the power button or the red die directly |
| Power state | User keys and the RGB LED red channel live in **L2**; green/blue are behind the expander in **L3B** |

## 4. Resources consumed

| Resource | Value |
|---|---|
| ESP32-S3 GPIO | **GPIO2** (KEY1), **GPIO3** (KEY2) |
| M5PM1 | `BTN_PU` input; `LED_EN_PP` output; registers `0x06` `PWR_CFG`, `0x13` `GPIO_DRV`, `0x48` `BTN_STATUS`, `0x49`/`0x4A` `BTN_CFG_1/2`, `0x45` `IRQ_MASK3` |
| M5IOE1 | `IO8` (PWM2), `IO9` (PWM1); registers `0x1B`–`0x1E` duty, `0x25`/`0x26` frequency |
| PWM frequency | **5000 Hz** in the factory firmware. The M5IOE1's `PWM_FREQ` is **shared by all four channels** |

> **GPIO3 is a strapping pin.** Holding Button B during reset perturbs the ESP32-S3 boot
> straps. The vendor firmware does not appear to guard against this. `inferred` from the
> pin map, `not-tested`. See [`usb-and-serial.md`](usb-and-serial.md).

## 5. Minimal procedure (`inferred`)

```cpp
#include <M5Unified.h>

void setup() {
  M5.begin(M5.config());
  M5.Led.setBrightness(64);
}

void loop() {
  M5.update();                                  // required; polls buttons and touch

  if (M5.BtnA.wasPressed()) { M5.Led.setColor(0, 0x00FF00); M5.Led.display(); }  // green
  if (M5.BtnB.wasPressed()) { M5.Led.setColor(0, 0xFF0000); M5.Led.display(); }  // red
  if (M5.BtnA.pressedFor(1000)) { /* long press */ }
}
```

`M5.Led` reports `getCount() == 1` and `led_type_fullcolor`
(`LED_PaperMono_Class.hpp`) — the "fullcolor" claim is the class's, and §2 is why it
overstates the hardware.

Direct expander control, as the factory firmware does it (`hal_board.cpp:25–28`,
`inferred` as a sketch):

```cpp
#include <M5IOE1.h>
M5IOE1 ioe1;
ioe1.begin(&M5.In_I2C, 0x4F, M5IOE1_I2C_FREQ_100K);
ioe1.setPwmFrequency(5000);
ioe1.setPwmDuty12bit(M5IOE1_PWM_CH2, 2048, ...);   // green,  IO8
ioe1.setPwmDuty12bit(M5IOE1_PWM_CH1, 2048, ...);   // blue,   IO9
```

> ⚠ **M5IOE1 outputs default to open-drain** (`GPIO_DRV_L = 0xFF`, `GPIO_DRV_H = 0x3F`),
> **including PWM**. Switch the pin to push-pull before expecting a drive. M5Unified does
> this with `setHighImpedance(pin, false)`.

## 6. The power button

The power button is **not on the ESP32-S3 at all** — it is an input to the M5PM1, and the
M5PM1 owns what it does.

| Action | Effect | Source |
|---|---|---|
| One short press | Power on / **reset** | vendor product page |
| Two presses in succession | Power off | vendor product page |
| Hold ~2 s until the red LED blinks | **Download mode** | vendor product page + UiFlow2 page |
| Short press | Documented recovery from a wedged I²C bus | vendor product page |

> **The single-click reset is aggressive, and third parties disable it.** Two independent
> hardware-validated third-party projects (`MagicCube/free-ink-on-paper-mono` and
> `Free-Ink/freeink-sdk`) report explicitly disabling the M5PM1's default single-click
> reset while preserving the long-hold download escape. The library call is
> `pm1.setSingleResetDisable(bool)`. This is the strongest independent behavioural
> corroboration in the whole record: two projects, two authors, the same finding.
> `reported-working` by them, `not-tested` here.

The M5PM1 also exposes `btnSetConfig(m5pm1_btn_type_t, m5pm1_btn_delay_t)`,
`btnGetState(bool*)` and `btnGetFlag(bool*)` (`M5PM1/src/M5PM1.h`), and button interrupts
are masked through `IRQ_MASK3` (`0x45`) with status in `BTN_STATUS` (`0x48`).

> **There is no separate reset button.** The schematic shows exactly three switches on the
> sub-board (`S1` `PWR_BTN`, `S2` `G2_KEY1`, `S3` `G3_KEY2`). M5Stack's Arduino tutorial
> page refers to "the reset button on the side"; that page is wrong, and two other vendor
> pages plus the spec table say power button. Resolved in
> [`../gaps-and-conflicts.md` R4](../gaps-and-conflicts.md#r4--download-mode-control--resolved-on-the-balance-of-evidence).

## 7. Silicon / board / framework / observed limits

| Class | Limit |
|---|---|
| **Board** | Red die on a non-PWM pin — colour set permanently limited (§2) |
| **Board** | GPIO3 (Button B) is an ESP32-S3 strapping pin |
| **Board** | Green/blue live behind I²C. **No I²C, no green or blue.** Red survives, because it is on the M5PM1 |
| **Firmware (M5PM1)** | The red die follows "M5PM1 default behaviour" at power-on before your code runs |
| **Framework (M5Unified)** | Only green is PWM'd; blue is binary (§2) |
| **Framework (M5IOE1)** | One shared `PWM_FREQ` register across all four channels |
| **Observed** | Single-click reset disabled by two independent third-party projects (§6) |
| **Unknown** | The LED part `RS-C1415MBAR` has **no obtainable datasheet**, so forward voltages, current limits and colour coordinates are unknown |

## 8. Conflicts and simultaneous use

| Combination | Verdict | Mechanism |
|---|---|---|
| Buttons + [download mode](usb-and-serial.md) | ⚠ | GPIO3 is a strapping pin; holding Button B across reset perturbs the straps |
| RGB green/blue + everything else on I²C | ✅ addresses distinct | But every LED update is an I²C transaction — do not animate it in a tight loop while [NFC](nfc.md) is polling |
| RGB + [microSD](microsd.md) / [mic](microphone.md) / [touch](touch.md) | ✅ | Different expander pins; the vendor's warning is about *reconfiguring* pins M5Unified already owns |
| RGB red + power state L2 | ✅ | Red is on the M5PM1 and available whenever the M5PM1 is alive |
| RGB green/blue + power state below L3B | ❌ | The expander's own rail and the LED drive go down with L3B |
| Buttons + [sleep](power-and-sleep.md) | ⚠ | Sheet 1 lists KEY1/KEY2 as M5PM1 wake inputs, but the UserDemo drives its wake from GPIO2/GPIO3 as *ESP32-S3* pins. Which path is live in which state is **not established** |

## 9. Debugging

| Symptom | Cause |
|---|---|
| `M5.BtnA` never fires | `M5.update()` not called in `loop()` |
| Board will not enter download mode | You are looking for a reset button that does not exist (§6) |
| Board resets when you tap the power button | That is the documented behaviour. Disable it with `setSingleResetDisable(true)` if it is in your way |
| LED shows the wrong colour | §2 — red is binary. Ask for a colour with partial red and you get full red or none |
| LED does nothing at all | M5IOE1 outputs default open-drain; set push-pull |
| Blue will not dim | You are on `M5.Led`, which writes blue as a binary level (§2) |
| Board boots into the wrong mode occasionally | Button B (GPIO3) held during reset |

## 10. Unresolved questions

- **Are KEY1/KEY2 genuinely M5PM1 wake sources, or only ESP32-S3 inputs?** Sheet 1 says
  wake-capable; the firmware only uses them as host GPIOs. Unresolved.
- **Why does M5Unified not PWM blue?** No documented reason (§2).
- **No datasheet for `RS-C1415MBAR`.** Electrical limits unknown.


### ⚠ Both driver chips have a NeoPixel engine. This board does not use it.

A real trap when reading the component records alongside this page: **the M5IOE1
and the M5PM1 each contain a working WS2812 driver**, and neither drives this LED.

| Chip | NeoPixel facility | Used for the RGB LED? |
|---|---|---|
| M5IOE1 | `LED_CFG` `0x24`, `LED_RAM` `0x30`–`0x6F` (32 × RGB565), output on `IO14` | **No** |
| M5PM1 | `NEO_CFG` `0x50`, MUX on `IO0` | **No** |

The PaperMono's RGB LED is **three discrete dies on three separate lines** — red
on the M5PM1's `LED_EN_PP`, green and blue on M5IOE1 `IO8`/`IO9`. There is no
data line and no RMT involvement. Those engines exist for *other* FreeInk-family
boards; on this one `IO14` is microSD power and `IO0` is the RTC interrupt.

Independently corroborated by `osprey74/Nostos` (`firmware/nostos-fw/src/led.rs`),
whose own comment reads: 緑=M5IOE1 `PYG8` / 青=M5IOE1 `PYG9` / 赤=M5PM1 `LED_EN`
（3 線独立・**WS2812 ではない**） — *"three independent lines, **not WS2812**"*.

**Consequence:** `FastLED`, `Adafruit_NeoPixel` and `smart_leds` are all the wrong
tool here. Across ten PaperMono repositories there is **zero** WS2812/SK6812 use
in any LED path.

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**. ⚠ The factory firmware uses the RGB LED's availability as one of its **Pro-vs-Lite discriminators** (`hal_board.cpp:162`) |
| Framework range | M5Unified 0.2.21 · M5IOE1 1.0.9 · M5PM1 1.0.7 |
| Evidence | Red-die limitation: **vendor-documented**, `reported-working`. Wiring: **schematic**. M5Unified behaviour: **read from source**. Single-click-reset behaviour: **community-reported**, two independent projects. Sketches: **`inferred`** |
| Confidence | High on the wiring and the colour limitation; medium on the API sketches |
| Last verified | **2026-09-01** |

## Related

- [`../pinouts-and-buses.md`](../pinouts-and-buses.md) · [`../power-architecture.md`](../power-architecture.md)
- [`power-and-sleep.md`](power-and-sleep.md) · [`usb-and-serial.md`](usb-and-serial.md) · [`io-expander.md`](io-expander.md) · [`frontlight.md`](frontlight.md)
- [`components/m5stack/m5pm1`](../../../../components/m5stack/m5pm1/README.md) · [`components/m5stack/m5ioe1`](../../../../components/m5stack/m5ioe1/README.md)
