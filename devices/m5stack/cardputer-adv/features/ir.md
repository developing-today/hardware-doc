# Cardputer ADV — infrared

> **Question:** *"How do I send IR commands? Can I receive?"*
> Verified **2026-09-04**.

## Hardware

A **single IR emitter, transmit only**, on **GPIO 44**. Designator `IR1` on schematic sheet 1.
There is **no IR receiver** on any Cardputer — the CardputerZero adds one (`IR_RX` on `G13`),
the ADV does not.

| Item | Value |
|---|---|
| TX GPIO | **G44** |
| RX | **none** |
| Emitter designator | `IR1` |
| Range (v1.1 figures; the ADV page gives none) | 410 cm at 0°, 170 cm at 45°, 66 cm at 90° |

`M5Cardputer-UserDemo` `hal_config.h`: `#define HAL_PIN_IR_TX 44`.
Bruce: `-DTXLED=44`, `-DLED_ON=HIGH`, `-DLED_OFF=LOW`.

## Minimal procedure

The `M5Cardputer` library depends on `arduino-irremote/IRremote` and ships
`examples/Basic/ir_nec/ir_nec.ino` (added `0fd54b7`, 2023-10-13):

```cpp
#include <M5Cardputer.h>
#define IR_TX_PIN 44
#define DISABLE_CODE_FOR_RECEIVER
#include <IRremote.hpp>

void setup() {
  auto cfg = M5.config(); M5Cardputer.begin(cfg, true);
  IrSender.begin(IR_TX_PIN);
}
void loop() {
  IrSender.sendNEC(0x0102, 0x34, 0);
  delay(1000);
}
```

ESP-IDF users: the factory firmware's `main/hal/utils/ir_nec/` wraps the RMT peripheral
(`void ir_helper_init(gpio_num_t pin_tx)`).

## Receiving anyway

You cannot without adding hardware. Two routes:

| Route | Pins | Note |
|---|---|---|
| Grove / PORT.A | G1, G2 | M5Stack sells an IR unit; Bruce's `IR_RX_PINS` list offers `{"M5 IR Mod", GROVE_SCL}, {"Grove W", GROVE_SCL}, {"Grove Y", GROVE_SDA}` |
| CAP header | G3, G4, G5, G6, G13, G15 | Bruce also offers `{"ADV 3",3},{"ADV 4",4},{"ADV 5",5},{"ADV 6",6},{"ADV 13",13},{"ADV 15",15}` — a direct acknowledgement that the ADV's freed pins are the general-purpose ones |

Bruce's pin lists are the clearest third-party statement of what the ADV's extra GPIOs are
actually good for. From `boards/m5stack-cardputer/m5stack-cardputer.ini`:

```
-DIR_TX_PINS='{ {"Default", TXLED}, {"M5 IR Mod", GROVE_SDA}, {"Grove W", GROVE_SCL},
                {"Grove Y", GROVE_SDA}, {"ADV 3",3},{"ADV 4",4},{"ADV 5",5},
                {"ADV 6",6},{"ADV 13",13},{"ADV 15",15} }'
```

The same list appears for `RF_TX_PINS`/`RF_RX_PINS`, i.e. for 433 MHz OOK modules.

## Projects

* `geo-tp/Ultimate-Remote` (★200) — "Universal remote control for the M5Cardputer, contains
  3498 remote profiles".
* r/M5Stack 2026-08-19: *"I made an ir sniper for cardputer ADV"*.
* Bruce and Launcher both include IR replay/transmit tooling.

## Resources and limits

| Resource | Note |
|---|---|
| RMT | one channel; shares the RMT peripheral with the WS2812 on G21 |
| Current | the v1.1 page quotes 148.07 mA in IR transmission mode — the highest single-function figure M5Stack publishes for a Cardputer |
| Carrier | standard 38 kHz via RMT/IRremote; not board-limited |

## Evidence status

TX pin: **official** ×3 (docs PinMap, factory firmware, Bruce). Absence of a receiver:
**verified negative** by designator census plus the CardputerZero positive control (which does
list an IR receiver). Range figures: **vendor claim for v1.1**, and **not published for the ADV**
— do not transfer them without saying so.
