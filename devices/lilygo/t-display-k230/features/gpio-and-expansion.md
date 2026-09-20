# GPIO and the 40-pin expansion header

**Question:** *What can I actually attach, and which pins are genuinely free?*

| | |
|---|---|
| Header | 2 × 20, 40 pins |
| SoC | [K230](../../../../components/canaan/k230/README.md): **64 GPIO + 8 PMU GPIO**, 5 UART, 5 I²C, 6 PWM, 3 SPI |
| Tools on board | `linux-tools-gpio` (`gpioinfo`, `gpioget`, `gpioset`), `evtest`, launcher I²C scanner |
| Evidence | `reported-working` for the map; electrical characteristics **unverified** |

## Read this first: most of the header is already spoken for

Full pinout: [`pinouts-and-buses.md` §1](../pinouts-and-buses.md#1-40-pin-expansion-header-2--20).
Claimed by on-board or base-board functions:

`GPIO2` nRF9151 enable · `GPIO3`/`GPIO4` nRF52840 UART · `GPIO5` LoRa reset ·
`GPIO14`–`GPIO17`, `GPIO19`, `GPIO20`, `GPIO44` LoRa SPI · `GPIO28`/`GPIO29` nRF9151 UART ·
`GPIO32`–`GPIO35` I²S · `GPIO42`/`GPIO43` keyboard IRQ/reset · `GPIO46`/`GPIO47` I²C4 ·
`GPIO52` keyboard backlight PWM.

**Genuinely uncommitted:** `GPIO6`, `GPIO18`, `GPIO26`, `GPIO27`, `GPIO30`, `GPIO31`, `GPIO45`,
`GPIO53`, `GPIO62`, `GPIO63`, plus `ADC0`, `ADC1`, `ADC2`.

That is **ten digital pins and three analogue inputs** on a fully populated kit. If you need
more, drop a subsystem — not using LoRa frees seven pins, not using the nRF52840 base frees the
I²S four.

## Power on the header

`5V`, `3V3`, two `GND`, and `USB-IN-5V`. No current limits are published.

## ⚠ IO bank voltage — the way to destroy the chip

The K230's IO banks have a **software-selected voltage** and Canaan's own reference device tree
says, in a comment:

> `// Please pay attention to the bank voltage! will damage the chip.`

Reference-design settings: `IO0`–`IO1` fixed **1.8 V**; everything else **3.3 V**. Before
attaching 1.8 V logic, read [`pinouts-and-buses.md` §6](../pinouts-and-buses.md#6-io-bank-voltages--the-hardware-damage-path).
Changing a bank in the device tree changes it for the whole bank, including pins other things
are using.

## I²C4 is shared with power management

Anything you hang on `GPIO46`/`GPIO47` shares a bus with the keyboard scanner, the charger and
the fuel gauge. **Avoid `0x20`–`0x27`** — the XL9555 expander's address is strap-dependent and
software-probed.

## ADC

Three analogue inputs are exposed. **The K230 brief datasheet's peripheral list does not
enumerate an ADC**, so resolution, reference voltage, sample rate and input range are all
unknown — [`GC-8`](../gaps-and-conflicts.md). Canaan's
`K230_Big_Core_Low_Speed_Driver_API_Reference` is the place to look; it was retrieved but not
mined in this pass.

## PWM

Six PWM channels in the SoC. **PWM4 is the keyboard backlight** on `GPIO52`. The others are
available if their pins are.

## Other expansion

- **QWIIC** connector on the Cased Version (wiki) — a standard 4-pin I²C connector. Which bus it
  is on is **not stated**; most plausibly I²C4. Unverified.
- **nRF52840 GPIO expansion header** on the Cased Version (wiki).
- **Two unused MIPI CSI inputs** — arguably the most valuable expansion on the board. See
  [camera.md](camera.md).

## Minimal procedure

```sh
gpioinfo                          # enumerate lines and current consumers
gpioget gpiochip0 6
gpioset gpiochip0 6=1
i2cdetect -y 4                    # or use the launcher's async I2C Scan
```

Adafruit Blinka is built in (`BR2_PACKAGE_PYTHON_ADAFRUIT_BLINKA=y`), so CircuitPython-style
Python drivers for I²C/SPI sensors are available. That is a genuinely convenient path and it is
easy to miss.

## Limits

| Limit | Value | Class |
|---|---|---|
| Free digital pins on a full kit | ~10 | board |
| ADC characteristics | **unknown** | unknown |
| Header current limits | **unpublished** | unknown |
| Max GPIO toggle rate | **unmeasured** | unmeasured |
| PMU GPIO (8 of them, ≤ 25 MHz) | not exposed on the header | board |
