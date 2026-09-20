# Cardputer ADV — Grove / PORT.A

> **Question:** *"How do I attach a Grove sensor?"*
> Identical connector on v1.0, v1.1 and ADV. Verified **2026-09-04**.

## Hardware

One **HY2.0-4P** connector, schematic designator **P1**, part value `HY-2.0_IIC`, protected by
`PESDNC2FD3V3B`/`PESDNC2FD5VB` ESD arrays (D6–D8) and fed from `+5VOUT`.

| Wire | Signal | GPIO |
|---|---|---|
| Black | GND | — |
| Red | +5 V (from the SY7088 boost) | — |
| Yellow | `G2` | GPIO 2 |
| White | `G1` | GPIO 1 |

M5Stack labels the port **`PORT.CUSTOM`** in the PinMap rather than `PORT.A`, but M5Unified
treats it as the external I²C bus for the whole Cardputer family.

## ⚠ Which line is the clock?

| Source | SCL | SDA |
|---|---|---|
| `M5Unified.cpp:99`, header `// In SCL,SDA, EX SCL,SDA` → `{…, GPIO_NUM_1, GPIO_NUM_2}` | **G1** (white) | **G2** (yellow) |
| M5Stack's usual Grove colour convention | yellow | white |
| Bruce `m5stack-cardputer.ini` | `-DGROVE_SCL=1` | `-DGROVE_SDA=2` |

Two independent software sources say **SCL = G1, SDA = G2**; only the colour convention
disagrees, and M5Stack calls this port `PORT.CUSTOM` rather than `PORT.A` precisely because it
is not the standard assignment. **Use G1 = SCL, G2 = SDA.** Recorded in
[`../gaps-and-conflicts.md`](../gaps-and-conflicts.md).

## Minimal procedure

```cpp
#include <M5Cardputer.h>
void setup() {
  auto cfg = M5.config(); M5Cardputer.begin(cfg, true);
  M5Cardputer.Ex_I2C.begin();                 // G1 SCL / G2 SDA
  for (uint8_t a = 8; a < 120; a++)
    if (M5Cardputer.Ex_I2C.start(a, false, 100000)) {
      M5Cardputer.Display.printf("0x%02X\n", a);
      M5Cardputer.Ex_I2C.stop();
    }
}
void loop() {}
```

`geo-tp/M5-Card-Computer-I2C-Scanner` (★23, MIT) does this as a finished app.

## It is not only I²C

G1 and G2 are ordinary GPIOs. Bruce exposes them as candidate pins for IR TX/RX, 433 MHz
OOK TX/RX, a CC1101 `GDO0`, an NRF24 `CE`, a W5500 `INT` and an SPI `SS`
(`-DSPI_SS_PIN=GROVE_SCL`). On a **v1.x**, where the CAP header does not exist, the Grove port
is the *only* general-purpose I/O available — which is why Bruce's pin menus are written the way
they are.

## Advantages over the CAP header for I²C

| | Grove (G1/G2) | CAP (G8/G9) |
|---|---|---|
| Other devices on the bus | **none** | TCA8418 `0x34`, ES8311 `0x18`, BMI270 `0x69` |
| Address freedom | full | avoid three |
| Latency impact on the keyboard | none | real |
| Pull-ups | on your peripheral | already fitted, 3.3 kΩ |
| Connector | keyed 2 mm, cable | 2.54 mm header, board-to-board |

**Put slow or chatty I²C peripherals on Grove.** Keep the internal bus for things that must be
on it.

## Limits

* Power comes from `+5VOUT` (SY7088 boost, **≈ 5.29 V inferred**). No published current limit
  for this port on the ADV; the CardputerZero's equivalent is specified at **< 500 mA**.
* 3.3 V logic on G1/G2 with a 5 V supply pin — the usual Grove arrangement. A 5 V-logic
  peripheral needs level shifting.
* One connector. Chain on the bus if you need more.

## Evidence status

Pin assignment: **official** ×3. SCL/SDA orientation: **conflict recorded, software sources
preferred**. Current limit: **unknown**.
