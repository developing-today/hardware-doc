# How do I read the orange knob and its button?

**Applies to:** DinMeter K134 and K134-V11 (identical hardware and pin map).
**Evidence status:** vendor example code (`reported-working` — it is M5Stack's own, shipped and
released); pin assignments `executed-success` from schematic + two independent source trees;
nothing run on hardware here. **Last verified:** 2026-09-04.

---

## Hardware path

```
orange knob  →  encoder module on connector J5  →  IN_A / IN_B  →  Stamp pads 23 / 21
                                                                 →  ESP32-S3 GPIO41 / GPIO40
             ↘  integrated push switch (b1/b2)  →  BTN → WAKE   →  Stamp pad 25 → GPIO42
                                                                 ↘ D4 → power-latch wake
```

- Pull-ups: `R2`, `R3` = 10 kΩ (A, B) and `R1` = 10 kΩ (button) to `+3.3V`; `C1` = 100 nF
  debounce on the button. **No other debounce hardware is fitted.**
- The encoder is **not** soldered to the main PCB — it plugs into a 7-pad connector `J5`.
- The encoder part number is **not published**:
  [`components/unidentified/m5stack-dinmeter/rotary-encoder`](../../../../components/unidentified/m5stack-dinmeter/rotary-encoder/README.md).
- **The button is also the wake key.** Pressing it can power the whole board back on from a
  latched-off state.

## Buttons available

| Button | Where | GPIO | M5Unified name | Notes |
|---|---|---|---|---|
| Knob press | in the encoder | **42** | `M5.BtnA` / `DinMeter.BtnA` | active-low; also a wake source |
| `G0` | **on the Stamp module** | **0** | `M5.BtnB` | boot/download button; usable as a normal button at runtime |
| `RST` (`S4`) | carrier | — | — | hardware reset, drives the Stamp's `EN`. Also the power-off button on battery |

M5Unified reads both in one place:
```cpp
// M5Unified/src/M5Unified.cpp:3500-3506
case board_t::board_M5Capsule:
case board_t::board_M5Dial:
case board_t::board_M5DinMeter:
  use_rawstate_bits = 0b00011;
  btn_rawstate_bits = ((!m5gfx::gpio_in(GPIO_NUM_42)) & 1)
                    | ((!m5gfx::gpio_in(GPIO_NUM_0)) & 1) << 1;
  break;
```
and configures GPIO42 as an input at init (`M5Unified.cpp:2398-2402`).

---

## Arduino — M5DinMeter (the short way)

```cpp
#include "M5DinMeter.h"

void setup() {
    auto cfg = M5.config();
    DinMeter.begin(cfg, /* enableEncoder = */ true);   // <- true, or the encoder never starts
    DinMeter.Display.setRotation(1);
    DinMeter.Display.setTextDatum(middle_center);
    DinMeter.Display.setTextFont(&fonts::Orbitron_Light_32);
    DinMeter.Display.setTextSize(2);
}

long oldPosition = -999;

void loop() {
    DinMeter.update();
    long newPosition = DinMeter.Encoder.read();
    if (newPosition != oldPosition) {
        DinMeter.Speaker.tone(8000, 20);      // click feedback
        DinMeter.Display.clear();
        oldPosition = newPosition;
        DinMeter.Display.drawString(String(newPosition),
            DinMeter.Display.width()/2, DinMeter.Display.height()/2);
    }
    if (DinMeter.BtnA.wasPressed())      DinMeter.Encoder.readAndReset();
    if (DinMeter.BtnA.pressedFor(5000))  DinMeter.Encoder.write(100);
}
```
Verbatim from `M5DinMeter/examples/Basic/encoder/encoder.ino` (release 1.0.0, 2024-03-07).
`reported-working` — vendor-published, not run here.

**API surface** (from the vendored PJRC `Encoder`, MIT, v1.2):
`read()`, `readAndReset()`, `write(long)`. `Button_Class` gives `wasPressed()`,
`wasReleased()`, `isPressed()`, `pressedFor(ms)`, `wasClicked()`, `wasHold()`.

**Counts.** x4 decoding — **one detent is four counts**. Divide by 4 for detent-level UI, or
accept 4× sensitivity. Detents-per-revolution is not published.

`DIAL_ENCODER_PIN_A 41` / `DIAL_ENCODER_PIN_B 40` are `#define`s in `M5DinMeter.h:8-9`; the
`ENCODER` member is constructed with them at `:33`. There is no way to change them without
editing the library, and no reason to.

---

## ESP-IDF — PCNT (the better way for anything real)

The PJRC library is interrupt-driven and costs a pair of ISRs. The ESP32-S3's **pulse counter**
does it in hardware. Espressif's own board definition uses PCNT; its configuration, verbatim:

| Field | Value |
|---|---|
| channels | 2 |
| ch 0 | `edge_gpio_num: 41` (A), `level_gpio_num: 40` (B); pos → DECREASE, neg → INCREASE; high → KEEP, low → INVERSE |
| ch 1 | `edge_gpio_num: 40` (B), `level_gpio_num: 41` (A); pos → INCREASE, neg → DECREASE; high → KEEP, low → INVERSE |
| filter | `max_glitch_ns: 1000` |
| limits | −1000 … +1000, `accum_count: true` |
| watch points | −1000, 0, +1000 |

Source: `espressif/esp-board-manager` `m5stack_boards/m5stack_dinmeter/board_peripherals.yaml`
@ `2beb9b22b0892b343bd555a1ebc9929a7edce8fc`, retained at
[`../artifacts/source-snapshots/dinmeter-board_peripherals.yaml`](../artifacts/source-snapshots/dinmeter-board_peripherals.yaml).

Two traps that file documents, both worth repeating:

1. **Each pin is used twice** — as an edge input on one channel and a level input on the other.
   A conflict checker will flag GPIO40/41 as double-booked. That is the standard IDF
   rotary-decoder pattern and is correct.
2. **Do not set `en_step_notify_up` / `en_step_notify_down`**, even to `false`. Those fields only
   exist under `SOC_PCNT_SUPPORT_STEP_NOTIFY`, which **the ESP32-S3 does not have**; a generator
   that emits them unconditionally breaks the build with
   `'struct <anonymous>' has no member named 'en_step_notify_up'`.

The button in IDF: GPIO42, input, pull-up, active-low, `long_press_time: 2000`,
`short_press_time: 100` — same source, `gpio_button_wake`.

---

## Decision table

| Approach | Use when | Cost |
|---|---|---|
| `DinMeter.Encoder` (PJRC, Arduino) | Arduino, simple UI, you already use M5Unified | 2 GPIO ISRs; fine at human speeds |
| ESP-IDF PCNT | IDF, or you need zero-CPU counting, or the knob is spun fast | one PCNT unit + 2 channels of the ESP32-S3's 4 |
| `ESP32Encoder` (bundled in `M5DinMeter-UserDemo/lib/`) | you want PCNT *from Arduino* | third-party, vendored by M5Stack in the factory-firmware project |
| Bare GPIO polling | never | misses transitions |

---

## Resource cost and conflicts

| Resource | Used |
|---|---|
| GPIO | 41, 40 (encoder), 42 (button), 0 (Stamp button) |
| Interrupts | 2 (PJRC path) or 0 (PCNT path) |
| PCNT units | 1 of 4, 2 channels (PCNT path) |
| Timers | none |

**Conflicts:** GPIO40/41/42 are the ESP32-S3 JTAG pins (`MTDO`/`MTDI`/`MTMS`). Using pin-based
JTAG debug is therefore impossible while the knob works. USB-Serial-JTAG is unaffected.
Nothing else on the board contends. See [`../resources-and-conflicts.md`](../resources-and-conflicts.md).

---

## Debugging and pitfalls

| Symptom | Likely cause |
|---|---|
| `Encoder.read()` always 0 | `begin()` called without `true` |
| Counts jump by 4 per detent | correct — x4 decoding. Divide |
| Direction inverted | swap A/B, or negate; there is no vendor-defined "positive" direction |
| Button seems to reset the app | you are on battery and GPIO46 is not held — the press is waking it, not resetting it. See [`power-and-battery.md`](power-and-battery.md) |
| Jitter at rest | the 1 kΩ-ish pull-ups plus 1 µs glitch filter are usually enough; if not, raise `max_glitch_ns` |
| JTAG adapter cannot attach | GPIO39-42 are occupied. Use USB-Serial-JTAG |

## Unresolved

- Detents per revolution, counts per revolution, rated rotational life, switch rated operations
  — **all unknown**, because the encoder part is unidentified.
- Whether the orange cap is part of the encoder or a separate moulding — unknown.
