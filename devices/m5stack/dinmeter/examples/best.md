# DinMeter — selected examples

**7 selected from 22 catalogued** ([`catalog.json`](catalog.json), search method in
[`search-log.md`](search-log.md)). Selection is for *coverage and quality*, not popularity.

> **None of these were built or run.** No toolchain was installed and no hardware was available.
> Every `build_status` in the catalogue is `not-attempted`, and that is stated rather than
> implied.

---

## The portfolio, and why each is in it

| # | Example | Role in the portfolio | Where |
|---|---|---|---|
| **OFF-08** | `esp-board-manager` `m5stack_dinmeter` | **Best reference configuration and best documentation.** Start here for ESP-IDF | [Espressif](https://github.com/espressif/esp-board-manager/tree/2beb9b22b0892b343bd555a1ebc9929a7edce8fc/m5stack_boards/m5stack_dinmeter) · [vendored](../artifacts/source-snapshots/) |
| **OFF-01** | `encoder.ino` | Best minimal example of the defining feature | [pinned](https://github.com/m5stack/M5DinMeter/blob/8ccbad7297beb82a140f812e5606e060d8a5e0dc/examples/Basic/encoder/encoder.ino) |
| **OFF-02** | `display.ino` | Best minimal display example | [pinned](https://github.com/m5stack/M5DinMeter/blob/8ccbad7297beb82a140f812e5606e060d8a5e0dc/examples/Basic/display/display.ino) |
| **OFF-03** | `rtc.ino` | Best *integrated* vendor example — RTC + Wi-Fi + SNTP + display | [pinned](https://github.com/m5stack/M5DinMeter/blob/8ccbad7297beb82a140f812e5606e060d8a5e0dc/examples/Basic/rtc/rtc.ino) |
| **OFF-04** | `wakeup.ino` | **Limit/architecture example** — the GPIO46 latch and RTC wake-from-off | [pinned](https://github.com/m5stack/M5DinMeter/blob/8ccbad7297beb82a140f812e5606e060d8a5e0dc/examples/Basic/wakeup/wakeup.ino) |
| **OFF-07** | `M5DinMeter-UserDemo` | Best complete application; the raw-LovyanGFX reference | [pinned](https://github.com/m5stack/M5DinMeter-UserDemo/tree/d2fdfe44e9baf810f82335faa6f5962e9fc59a44) · [vendored](../artifacts/source-snapshots/M5DinMeter-UserDemo-d2fdfe44e9baf810f82335faa6f5962e9fc59a44.tar.gz) |
| **COM-01** | `bmorcelli/Launcher` DinMeter board | **Independent cross-check** + a distinct implementation approach + Grove-pin-reuse limit test | [board file](https://github.com/bmorcelli/Launcher/blob/main/boards/m5stack-dinmeter/platformio.ini) · [vendored](../artifacts/source-snapshots/launcher-m5stack-dinmeter-platformio.ini) |

## Coverage check

| Feature | Covered by | Gap |
|---|---|---|
| Rotary encoder | OFF-01 (Arduino/PJRC), OFF-08 (IDF/PCNT), COM-01 (mathertel) — **three distinct approaches** | — |
| Button / WAKE | OFF-01, OFF-04, OFF-08 | — |
| Display | OFF-02 (M5GFX), OFF-07 (raw LovyanGFX), OFF-08 (esp_lcd), COM-01 (Arduino_GFX) — **four approaches** | — |
| Backlight / dimming | OFF-07, OFF-08, COM-01 | — |
| RTC + NTP | OFF-03 | — |
| RTC alarm wake-from-off | OFF-04 | — |
| Buzzer | OFF-01 (in context), OFF-08 (LEDC) | — |
| Power latch (GPIO46) | OFF-04, OFF-08 | — |
| Battery ADC | COM-01 only | **No vendor example** |
| Wi-Fi | OFF-03 | — |
| BLE | — | **No selected example.** COM-07 exists but is unlicensed |
| PORT.A / PORT.B | COM-01 (as SD SPI) | **No simple Grove I²C example** |
| **RGB LED** | — | **No example anywhere**, and this is the one feature with a known v1.1 break |
| DIN mounting | n/a (mechanical) | — |

**Three genuine gaps**, stated rather than papered over: no licensed BLE example, no plain Grove
I²C example, and **no RGB-LED example at all** — which is unfortunate, because that is exactly
where DinMeter v1.1 diverges. See [`../features/rgb-led.md`](../features/rgb-led.md).

## Why these, and not the popular ones

- `no-body-in-particular/m5din-hikoki` (★25) is the most-starred DinMeter application and is
  **not selected**: it is a domain-specific instrument that teaches nothing about the board that
  OFF-01/02/03 do not.
- `viniciusbo/m5-palnagotchi` (★81) is the most-starred repository touching the device and is
  **not selected**: DinMeter is one target among many, with nothing device-specific to learn.
- `tarmn3/m5dinmeter-ble-volume-knob` is the **only** BLE example and is **not selected** because
  it declares **no licence**. Pointing people at unlicensed code to copy is not a favour. It is
  catalogued, and reading it is fine.
- **Popularity was not treated as authority.** OFF-08, the best item in the portfolio, is a
  directory of three YAML files with no stars at all.

## Notes on each selection

### OFF-08 — Espressif's board definition · *read this first*

Not an "example" in the usual sense: three YAML files that define the whole board for ESP-IDF.
It is nonetheless the highest-value item found, because its comments document things M5Stack does
not:

- **the GRAM gap** (column +52, row +40) and that the application must apply it via the panel gap
  API, because the board model has no offset field;
- **the two-channel PCNT quadrature pattern**, and that GPIO40/41 appearing double-booked is
  expected and correct;
- **a genuine build break** — `en_step_notify_up`/`_down` exist only under
  `SOC_PCNT_SUPPORT_STEP_NOTIFY`, which the ESP32-S3 lacks, so emitting them (even as `false`)
  fails compilation;
- **the GPIO3-vs-GPIO42 ambiguity** in M5Stack's own pin table, resolved by citing M5Unified;
- **what it deliberately does not model** — the RTC device, both Grove ports, the charger, USB.

One caution: its Grove wire-colour note derives from M5Stack's disputed PinMap (its own header
says so), so it must **not** be counted as independent corroboration on that point.

### OFF-01 — `encoder.ino`

The one thing to notice: `DinMeter.begin(cfg, true)`. The `enableEncoder` parameter **defaults to
`false`**, so `begin(cfg)` leaves the knob dead. It also shows the click-per-detent pattern
(`Speaker.tone(8000, 20)`), which is how the device feels right.

### OFF-04 — `wakeup.ino` · *the architecture lesson*

`Power.timerSleep(5)` is not an ESP32 deep sleep. It programmes the BM8563 alarm and then
**releases the GPIO46 latch**, cutting the battery. That is why the board's standby figure is
38.4 µA rather than a typical deep-sleep number, and why forgetting to hold GPIO46 makes the
device switch itself off. Read this example before writing anything battery-powered.

### OFF-07 — `M5DinMeter-UserDemo` · *the factory firmware*

MIT, all dependencies pinned (`espressif32@6.3.1`, `LovyanGFX 1.1.12`, `SmoothUIToolKit 1.0.1`).
`ft_disp_lgfx_cfg.hpp` is the authoritative raw-LovyanGFX configuration and uses
`lgfx::Panel_ST7789` — the generic class, not a V2-specific one, which is part of why the v1.1
ST7789P3 is expected to behave identically.

**Mixed-licence archive:** the MIT at the root does not cover the bundled `lib/` trees (PJRC
`Encoder`, `ESP32Encoder`, `I2C_BM8563`, `Button`), each of which ships its own licence file.

### COM-01 — `bmorcelli/Launcher` · *the independent check*

Different author, different graphics library (`Arduino_GFX`, not M5GFX), different encoder
library (`mathertel/RotaryEncoder 1.5.3`), and a CI matrix that builds it on every release. It
agrees with the schematic on every point it touches — display pins, GRAM offsets, battery divider
ratio 2.0, no PSRAM — which is the strongest available corroboration short of hardware.

It is also a **limit test**: it bit-bangs an SD card across *both* Grove ports
(`SDCARD_CS=13 SCK=15 MISO=2 MOSI=1`), consuming all four free user pins. That is the only
evidenced way to get storage onto this board, and it shows exactly what it costs.

## What was vendored, and what was not

| Vendored (3) | Why |
|---|---|
| `M5DinMeter` @ `8ccbad72…` (8 532 B) | tiny; contains all six official examples |
| `M5DinMeter-UserDemo` @ `d2fdfe44…` (74 231 B) | MIT, small, and the factory image's only public form |
| `esp-board-manager` DinMeter YAMLs (7 367 B) | tiny, and the single best reference |
| `launcher-m5stack-dinmeter-platformio.ini` (1 601 B) | one file; the corroboration is the point |

**Not vendored:** `M5Unified` and `M5GFX` (large, canonical, and reproducible from the pinned
commits recorded in [`../sources.md`](../sources.md)); all COM-02…COM-10 application projects
(links and immutable-revision notes retained in the catalogue instead).

## If you build one thing

Build **OFF-04 (`wakeup.ino`)** on a real unit. It exercises the encoder button, the RTC, the
power latch and the display in ~40 lines, and it is the fastest way to confirm that the whole
device-specific architecture works on your board. Then add the two lines from
[`../features/rgb-led.md`](../features/rgb-led.md) and settle the outstanding v1.1 question.
