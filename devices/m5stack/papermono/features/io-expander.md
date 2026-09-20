# I/O expander (M5IOE1) — M5Stack PaperMono

> **How do I use the expander, and how do I avoid the two numbering traps that will
> silently target the wrong pin?**
> Hardware revision **V0.6.2** · snapshot **2026-09-01** · nothing tested on hardware.

> ## ⚠ Read this first
>
> Two independent off-by-one hazards meet on this chip:
>
> 1. **`M5IOE1_PIN_3 = 2`** — the label is 1-based, the enum value is 0-based. Passing a
>    documentation `PYG<n>` straight into the API reaches pin **n+1**.
> 2. **`PYG3` denotes an M5IOE1 pin *and* an M5PM1 net**, and they are different signals.
>    Intending frontlight brightness and writing M5IOE1 `IO3` **cuts power to the e-paper
>    panel**, silently.
>
> **[`../pin-naming-and-the-pyg-ambiguity.md`](../pin-naming-and-the-pyg-ambiguity.md) is
> required reading before you write to this chip.**

## 1. Capability summary and why it is not optional

The M5IOE1 is a custom M5Stack part — the **same `PY32L020F15U6` silicon as the
[M5PM1](../../../../components/m5stack/m5pm1/README.md)**, running different firmware —
offering 14 GPIOs, four 12-bit ADC channels, four PWM channels, a NeoPixel driver, a die
temperature sensor and 32 bytes of retention RAM, on I²C `0x4F`.

On the PaperMono it is a load-bearing structural element, not a convenience. Behind it
sit:

| Function | Pin | Guide |
|---|---|---|
| microSD card detect | `IO1` | [`microsd.md`](microsd.md) |
| LoRa antenna switch | `IO2` | [`lora.md`](lora.md) |
| **E-paper 3.3 V rail enable** | `IO3` | [`epaper-display.md`](epaper-display.md) |
| NFC power enable | `IO4` | [`nfc.md`](nfc.md) |
| E-paper reset | `IO5` | [`epaper-display.md`](epaper-display.md) |
| Touch reset | `IO6` | [`touch.md`](touch.md) |
| Own I²C address select (`ADD_SET`) | `IO7` | §4 |
| RGB green (PWM2) | `IO8` | [`buttons-and-rgb-led.md`](buttons-and-rgb-led.md) |
| RGB blue (PWM1) | `IO9` | idem |
| LoRa reset | `IO10` | [`lora.md`](lora.md) |
| **IP2315 charger I²C bus gate** | `IO11` | [`battery-and-charging.md`](battery-and-charging.md) |
| Microphone power enable | `IO12` | [`microphone.md`](microphone.md) |
| Touch power enable | `IO13` | [`touch.md`](touch.md) |
| microSD power enable | `IO14` | [`microsd.md`](microsd.md) |

**Losing I²C means losing the ability to power-cycle the display.**

Component record: [`components/m5stack/m5ioe1`](../../../../components/m5stack/m5ioe1/README.md).
Interrupt output `OD_INTOUT` → ESP32-S3 **GPIO7**.

## 2. ⚠ Trap 1: `M5IOE1_PIN_3 = 2`

`M5IOE1/src/M5IOE1.h:31–45`:

```c
M5IOE1_PIN_NC = -1,
M5IOE1_PIN_1  = 0,
M5IOE1_PIN_2  = 1,
M5IOE1_PIN_3  = 2,     // <-- M5IOE1.h:34
...
M5IOE1_PIN_14 = 13,
```

Compare the companion chip, `M5PM1/src/M5PM1.h:410`:

```c
M5PM1_GPIO_NUM_3 = 3,   // label equals value
```

**Two custom chips on one board with opposite label↔value conventions**, and nothing in
any vendor document says so.

So: documentation label `PYG3` = manual pin `IO3` = enum `M5IOE1_PIN_3` = **raw value 2**
= **register bit 2**. Passing the literal `3` where the enum was expected targets `IO4` —
on this board, that swaps *e-paper power enable* for *NFC power enable*.

There is also **no `M5IOE1_PIN_0`**. `M5IOE1.h` defines `_1 … _14` and
`M5IOE1_MAX_GPIO_PINS 14`. A documentation reference to `PYG0` (e.g. `PYG0_RTC_INT`)
**cannot** denote an M5IOE1 pin under any reading — it is an M5PM1 pin the docs
mislabelled with the expander's prefix.

### The three ways vendor code sidesteps it

| Style | Example | Note |
|---|---|---|
| **Library enum** — the safe form | `ioe1.digitalWrite(M5IOE1_PIN_3, HIGH)` | Factory firmware. Use the constant, never a literal |
| **Raw zero-based values** | `ioe.digitalWrite(2, true)` | Vendor OTP demo, with the explicit comment `// M5IOE1 uses zero-based pin indexes.` (`EDP_SPI.cpp:36–38`) |
| **Raw register bit masks** | `lgfx::i2c::bitOn(port, 0x4F, 0x05, 0b00000100, freq)` | M5GFX (`M5GFX.cpp:2088–2096`). Avoids the enum entirely |

A **fourth** naming system exists: M5Unified's own expander abstraction uses
`M5IOE1_Class::gpio11`, which is *not* the M5IOE1 library's enum. Four naming systems for
fourteen pins. Name the chip and the system every time.

## 3. ⚠ Trap 2: outputs default to open-drain

`GPIO_DRV_L = 0xFF`, `GPIO_DRV_H = 0x3F` at reset — **every** GPIO output defaults to
open-drain, **including PWM and NeoPixel**. With no external pull-up, an "output" you set
high does nothing.

Both vendor paths handle it explicitly:

```cpp
ioe1.setDriveMode(TF_EN_PIN, M5IOE1_DRIVE_PUSHPULL);          // factory firmware
ioe.setHighImpedance(IOE_EPD_ENABLE, false);                  // OTP demo / M5Unified
lgfx::i2c::bitOff(port, 0x4F, 0x13, 0b00110100, freq);        // M5GFX, raw
```

A third related rule: **peripheral occupancy overrides the GPIO registers.** When a pin is
claimed by ADC, PWM, I²C, SWD or NeoPixel, its `GPIO_M_x` / `GPIO_O_x` bits become
inoperative.

## 4. ⚠ The address is `0x4F`, and the chip's own manual disagrees

Everything on this board — firmware, product page, M5GFX, M5Unified — uses **`0x4F`**.
The M5IOE1 V1.4 manual states the address range **`0x6F`–`0x76`** in three separate
places, the chip's `IO7` is genuinely wired to an `ADD_SET` divider, and the vendor
library constant is named `M5IOE1_DEFAULT_ADDR_2` with an autodetect that sweeps
**both** ranges (`M5IOE1.h:80–81`).

Unresolved. Tracked as
[`../gaps-and-conflicts.md` C4](../gaps-and-conflicts.md#c4--the-m5ioe1s-i²c-address-is-not-in-its-own-manual).
Practically: use `M5IOE1_DEFAULT_ADDR` / `0x4F` and let the library autodetect if it
fails. Note that `IO7` (`ADD_SET`) is **not listed on the vendor product page** — one of
that page's only two omissions.

## 5. Prerequisites

| Item | Value |
|---|---|
| M5IOE1 library | **1.0.9** (registry `m5stack/m5ioe1`) |
| M5Unified | 0.2.21 — brings the expander up during `M5.begin()` and exposes it as `M5.getIOExpander(0)` |
| I²C | Shared bus GPIO47/48, brought up at **100 kHz** ("device default", per the shipped binary's own log string) |
| Power state | The expander is on `3V3_L2`; it is alive whenever the ESP32-S3 is |

## 6. Resources consumed

| Resource | Value |
|---|---|
| I²C address | `0x4F` on the shared bus |
| ESP32-S3 GPIO | **GPIO7** — `OD_INTOUT`. **The factory firmware does not use it** (`M5IOE1_INT_MODE_DISABLED`, `hal_board.cpp:62`) and polls instead |
| Free expander pins | **None.** All fourteen are assigned |
| Unused capabilities | All four ADC channels, PWM3/PWM4 as PWM, the NeoPixel output, the temperature sensor, the retention RAM and the `AW8737A` pulse register are **all unexercised on this board** |

Register map summary (full table in the [component record](../../../../components/m5stack/m5ioe1/README.md)):
direction `0x03`/`0x04`, output `0x05`/`0x06`, input `0x07`/`0x08`, pull-up `0x09`/`0x0A`,
pull-down `0x0B`/`0x0C`, interrupt enable/polarity/status `0x0D`–`0x12`, drive
`0x13`/`0x14`, ADC `0x15`–`0x17`, temperature `0x18`–`0x1A`, PWM duty `0x1B`–`0x22`,
I²C config `0x23`, LED config `0x24`, PWM frequency `0x25`/`0x26`. Low byte covers P8–P1,
high byte P14–P9 in `[5:0]`.

## 7. Minimal procedure (`inferred`)

```cpp
#include <M5Unified.h>
#include <M5IOE1.h>

M5IOE1 ioe1;

void setup() {
  M5.begin(M5.config());                       // M5Unified already owns the expander

  ioe1.begin(&M5.In_I2C, M5IOE1_DEFAULT_ADDR, M5IOE1_I2C_FREQ_100K, M5IOE1_INT_MODE_DISABLED);

  ioe1.pinMode(M5IOE1_PIN_4, OUTPUT);                       // NFC enable
  ioe1.setDriveMode(M5IOE1_PIN_4, M5IOE1_DRIVE_PUSHPULL);   // <- do not skip
  m5ioe1_err_t err = M5IOE1_OK;
  ioe1.digitalWriteWithRes(M5IOE1_PIN_4, HIGH, &err);
  if (err != M5IOE1_OK) { /* on the real board this means "probably a Lite" - see §9 */ }
}
```

API names are transcribed from the factory firmware and the vendor's published examples:
`begin`, `pinMode`, `setDriveMode`, `setPullMode`, `digitalWrite`,
`digitalWriteWithRes`, `digitalRead`, `digitalReadWithRes`, `setPwmFrequency`,
`setPwmDuty12bit`, `setDirection`, `setHighImpedance`, `setLogLevel`.

## 8. ⚠ M5Unified already owns most of these pins

M5Stack's own warning, verbatim:

> "The pins associated with the e-paper display, touch controller, microSD, and PDM
> microphone are **already used by M5Unified**. Before modifying them, ensure that the
> corresponding peripheral has stopped, or the peripheral may stop working or require
> reinitialization."

That covers `IO3`, `IO5`, `IO6`, `IO12`, `IO13`, `IO14` — six of the fourteen. Add
`IO11` (charger gate, owned by `M5.Power`) and there are only seven pins M5Unified is not
already driving, all of which belong to LoRa, NFC or the LED.

**There is no spare expander pin on this board**, just as there is no spare GPIO.

## 9. The expander is the Pro-vs-Lite discriminator

`hal_board.cpp:160–172` — the factory firmware decides which SKU it is running on by
trying to drive `IO4` (NFC enable) and watching for an error:

```cpp
void Hal::detectBoardVariant() {
    if (!_rgb_ready) { _board_variant = BoardVariant::Lite; return; }
    m5ioe1_err_t err = M5IOE1_OK;
    ioe1.digitalWriteWithRes(NFC_EN_PIN, HIGH, &err);
    if (err != M5IOE1_OK) { _board_variant = BoardVariant::Lite; return; }
}
```

combined with an NFC identity read (register `0x7F`, expected type `0x05`).

**M5GFX cannot distinguish Pro from Lite** — both map to the single enum
`board_M5PaperMono`, with NFC masked out of the detection test (`M5GFX.cpp:1945`). Only
the application layer can tell.

## 10. Silicon / board / framework / observed limits

| Class | Limit |
|---|---|
| **Firmware (M5IOE1)** | Off-by-one enum (§2); open-drain default (§3); address disagreement with its own manual (§4) |
| **Firmware (M5IOE1)** | Interrupt exclusion groups — interrupts cannot be enabled simultaneously within `IO1&IO6`, `IO2&IO3`, `IO7&IO12`, `IO8&IO9`, `IO10&IO14`, `IO11&IO13`. **`IO2&IO3` and `IO11&IO13` both straddle live PaperMono signals** |
| **Firmware (M5IOE1)** | One shared `PWM_FREQ` register for all four PWM channels; I²C idle-sleep is disabled outright while PWM is enabled |
| **Board** | All 14 pins assigned. No expansion header |
| **Framework** | Four different pin-naming systems (§2) |
| **Framework** | The factory firmware **polls** rather than using `OD_INTOUT`; the GPIO7 interrupt path is therefore **unexercised by any vendor code** |
| **Observed** | Nothing. No hardware report exists about expander behaviour on this board |

## 11. Conflicts and simultaneous use

| Combination | Verdict | Mechanism |
|---|---|---|
| Expander + everything | ⚠ **it is the single point of failure** | Panel, touch, SD, mic, NFC, LoRa and charger access all route through it |
| Interrupt on `IO11` + interrupt on `IO13` | ❌ | Documented exclusion pair — charger gate vs touch power |
| Interrupt on `IO2` + interrupt on `IO3` | ❌ | LoRa antenna switch vs e-paper rail |
| PWM on green (`IO8`) + PWM on blue (`IO9`) | ✅ *probably* | The documented exclusion for this pair is on **interrupts**, not PWM. M5Unified nonetheless PWMs only green. See [`buttons-and-rgb-led.md`](buttons-and-rgb-led.md) |
| Expander + charger gate held open | ⚠ | The one documented bus-stability hazard |
| Expander + M5Unified-owned pins | ⚠ | §8 — stop the peripheral first |

## 12. Debugging

| Symptom | Cause |
|---|---|
| **Screen went blank when you changed something unrelated** | You wrote `IO3`. §2 or the `PYG3` ambiguity |
| NFC stopped working when you meant to touch the display rail | Off-by-one: you passed a literal and hit `IO4` |
| An output does nothing | Still open-drain (§3) |
| `0x4F` not found | Try the library autodetect; the manual claims `0x6F`–`0x76` (§4) |
| A peripheral dies after you drive "its" expander pin | M5Unified owns it (§8) |
| `digitalWriteWithRes` returns an error on a Pro | You are probably on a Lite (§9) |
| Interrupt on GPIO7 never fires | The chip defaults to polling in vendor code; and `INT_OUT` is **open-drain and needs a pull-up** |

## 13. Unresolved questions

- **The manual's `0x6F`–`0x76` address range vs the board's `0x4F`** (§4).
- **`PYB_NFC_EN` is annotated "spare GPIO"** on schematic sheet 4 while the firmware uses
  it as the NFC enable. Likely a stale annotation; unresolved.
- Whether the GPIO7 interrupt path works at all on this board — **no vendor code exercises
  it**.

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**. Fitted on both C153 and C153-LITE; `IO2`/`IO4`/`IO10` are unused on the Lite |
| Framework range | M5IOE1 1.0.9 · M5Unified 0.2.21 · M5GFX 0.2.28 |
| Evidence | Pin map: **schematic + firmware, cross-confirmed**. Off-by-one: **`M5IOE1.h:34`**, `executed-success` read. Register map: **vendor manual V1.4**. Sketch: **`inferred`** |
| Confidence | High. This is the best-evidenced part of the board — three independent sources agree on the pin map |
| Last verified | **2026-09-01** |

## Related

- [`../pin-naming-and-the-pyg-ambiguity.md`](../pin-naming-and-the-pyg-ambiguity.md) — **read before writing to this chip**
- [`../pinouts-and-buses.md#m5ioe1-expander-pins`](../pinouts-and-buses.md#m5ioe1-expander-pins) · [`../resources-and-conflicts.md`](../resources-and-conflicts.md)
- [`components/m5stack/m5ioe1`](../../../../components/m5stack/m5ioe1/README.md) · [`components/m5stack/m5pm1`](../../../../components/m5stack/m5pm1/README.md) · [`components/puya/py32l020f15u6`](../../../../components/puya/py32l020f15u6/README.md)
- [`vendors/m5stack`](../../../../vendors/m5stack/README.md) — where the M5IOE1 datasheet lives, including the Chinese-only edition
