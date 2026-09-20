# How do I connect things to PORT.A and PORT.B?

**Applies to:** K134 and K134-V11 (identical).
**Evidence status:** GPIO assignments `executed-success` (schematic + M5Unified agree); wire
colours **unresolved** — see the warning. **Last verified:** 2026-09-04.

---

## What you get

Two HY2.0-4P ("Grove") sockets on the back:

| Port | Connector | Signals | GPIO | Intended for | Rail |
|---|---|---|---|---|---|
| **PORT.A** (red) | `J3` `HY-2.0_IIC` | `IIC_SCL`, `IIC_SDA` | **15**, **13** | I²C units | `+5VOUT` |
| **PORT.B** (black) | `J4` `HY-2.0_IO` | `GI`, `GO` | **1**, **2** | plain GPIO / ADC / PWM | `+5VOUT` |

- Load limit **5 V @ 220 mA per port**.
- PORT.A carries 10 kΩ pull-ups (`R2`, `R3`) to `+3.3V`. **These are 3.3 V-logic buses on a 5 V
  power pin** — the usual M5Stack arrangement. Do not drive 5 V logic into them.
- The 5 V comes from the `U3` SY7088 boost when running on battery.

```cpp
DinMeter.Ex_I2C.begin();                          // PORT.A  (GPIO15/13) - external
DinMeter.In_I2C.begin();                          // internal (GPIO12/11) - the RTC
```
`M5DinMeter.h:28,31`. **These are separate buses.** A Grove unit cannot collide with the RTC even
if it answers at 0x51.

## ⚠ The wire-colour conflict — read before hand-wiring

The vendor PinMap renders:

| | Black | Red | Yellow | White |
|---|---|---|---|---|
| PORT.A | GND | 5V | **G13** | **G15** |
| PORT.B | GND | 5V | **G2** | **G1** |

The schematic says `J3` pin 1 = `IIC_SCL` → GPIO15 and pin 2 = `IIC_SDA` → GPIO13; `J4` pin 1 =
`GI` → GPIO1 and pin 2 = `GO` → GPIO2. Under the Grove convention (pin 1 = yellow, pin 2 =
white) that makes **yellow = GPIO15 = SCL** and **yellow = GPIO1**, i.e. the opposite of the
table. M5Unified agrees with the schematic: `EX SCL = GPIO_NUM_15`, `EX SDA = GPIO_NUM_13`
(`M5Unified.cpp:96`).

**Unresolved.** Full analysis in [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md) §1.

**Practical consequence: none, if you use a Grove cable and a Grove unit** — the cable and the
software both do the right thing. It matters only if you cut a cable and wire to bare pins, in
which case: **buzz it out with a meter first.**

## Using the ports as something else

Both ports are ordinary GPIOs. The most striking demonstration is Bruce/Launcher, which builds a
**software SPI SD-card interface across both ports at once**:

```ini
; bmorcelli/Launcher  boards/m5stack-dinmeter/platformio.ini
-DSDCARD_CS=13    -DSDCARD_SCK=15     ; PORT.A
-DSDCARD_MISO=2   -DSDCARD_MOSI=1     ; PORT.B
```
`reported-working` — that target is in the project's CI matrix and ships as
`Launcher-m5stack-dinmeter.bin`. It is the only evidenced way to get storage onto this board,
and it costs you both ports.

Other uses that follow from the pin capabilities: GPIO1/2 are ADC1 channels (so PORT.B can be
two analogue inputs), all four are LEDC-capable (PWM out), and any of them can be a UART or a
1-Wire line.

## Resource cost and conflicts

| Resource | Used |
|---|---|
| GPIO | 13, 15 (PORT.A); 1, 2 (PORT.B) |
| I²C ports | 1 (if you use PORT.A as I²C) — the ESP32-S3 has 2, and the RTC has the other |
| Rail | shared 220 mA per port from `+5VOUT` |

**No conflict with anything else on the board.** Display, encoder, RTC, buzzer and both ports
can all run simultaneously — this is the one board where the pin budget is tight but the
*peripheral* budget is not.

**The real constraint is quantity.** Four signals total. If you need five, you are out.

## Pitfalls

| Symptom | Cause |
|---|---|
| Grove unit not found on `Ex_I2C` | You initialised `In_I2C` (the RTC bus) instead |
| Unit works on USB, browns out on battery | 220 mA limit, and the boost has to supply it |
| 5 V sensor reads wrong / damaged | The signal pins are **3.3 V**, only the power pin is 5 V |
| Hand-wired I²C dead | The yellow/white conflict — swap and retry |
| Grove rail measures 5.38 V not 5.0 V | Expected: `U3`'s divider computes to 5.38 V. See [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md) §6 |

## Related

[`components/silergy/sy7088`](../../../../components/silergy/sy7088/README.md) (the 5 V boost) ·
[`../pinouts-and-buses.md` §5](../pinouts-and-buses.md#5-grove-ports--and-the-colour-conflict) ·
[`../resources-and-conflicts.md`](../resources-and-conflicts.md)
