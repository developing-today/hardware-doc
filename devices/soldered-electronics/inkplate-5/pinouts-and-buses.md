# Inkplate 5 — pinouts and buses

> Netlist-derived wiring reference for the Soldered Inkplate 5 (design **V1.2.0**).
> Snapshot **2026-08-24**. Extracted from Soldered's own KiCad PCB with [`tools/kicad_pcb_nets.py`](../../../tools/kicad_pcb_nets.py) — the `.kicad_pcb` stores resolved net names per pad, so this is the actual copper, not a transcription.

Cross-checked against `Inkplate-Arduino-library/src/boards/Inkplate5/` (`pins.h`, `waveforms.h`, `Inkplate5Driver.cpp`). **The schematic net names and the library agree throughout** — Soldered's net naming is unusually disciplined, which makes this board easy to reason about.

Applies to the **Inkplate 5**. The [Gen 2](../inkplate-5-gen2/README.md) differs only in the panel, so the ESP32 pin map below is expected to carry over unchanged — but the Gen 2 PCB was **not** independently netlist-parsed in this pass.

---

## 1. ESP32-WROVER (U10) — complete pin map

| Pad | Net | Function |
|---:|---|---|
| 1, 15, 38, 39 | `GND` | ground |
| 2 | `3V3` | supply |
| 3 | `RST` | module reset — shared with the expander's reset (U9.24) |
| 4 | `GPIO_36` | **SW3** (button) + `R41` pull, broken out at `K36` |
| 5 | `GPIO_39` | broken out at `K35`, via jumper `JP2` |
| 6 | `IO34` | via jumper `JP4` |
| **7** | **`V_BAT`** | **battery sense ADC** — see [§5](#5-battery-sensing-is-a-switched-divider) |
| 8 | `EPD_CKV` | e-paper vertical clock |
| 9 | `EPD_SPH` | e-paper horizontal start pulse |
| 10 | `EPD_D5` | e-paper data bit 5 |
| 11 | `EPD_D6` | e-paper data bit 6 |
| 12 | `EPD_D7` | e-paper data bit 7 |
| 13 | `SPI_SCK` | microSD clock |
| 14 | `SPI_MISO` | microSD data out |
| 16 | `SPI_MOSI` | microSD data in |
| 17–22 | *unconnected* | **module pads 17–22 are no-connects** — internal flash/PSRAM on the WROVER |
| 23 | `SPI_CS` | microSD chip select, via jumper `JP3` |
| 24 | `EPD_LE` | e-paper latch enable |
| 25 | `GPIO_0` | **strapping/boot pin** — also gated by a MOSFET, see [§4](#4-gpio0-is-mosfet-gated-by-the-expander) |
| 26 | `EPD_D0` | e-paper data bit 0 |
| 29 | `EPD_D1` | e-paper data bit 1 |
| 30 | `EPD_D2` | e-paper data bit 2 |
| 31 | `EPD_D3` | e-paper data bit 3 |
| 33 | `I2C_SDA` | I²C data |
| 34 | `RXD` | UART receive (from CH340C) |
| 35 | `TXD` | UART transmit (to CH340C) |
| 36 | `I2C_SCL` | I²C clock |
| 37 | `EPD_D4` | e-paper data bit 4 |

36 connected pads.

**Pads 17–22 being no-connects matters**: on a WROVER those are the SPI flash and PSRAM interface, brought out on the module footprint but not usable. This is the direct analogue of the "GPIO33–37 don't exist" trap on the XIAO ESP32S3 Sense — the pins are physically present on the footprint and completely unusable.

### Mapping net names to GPIO numbers

The PCB gives net *names*; the library gives the GPIO *numbers* they correspond to. Combining both:

| Net | GPIO | Source |
|---|---:|---|
| `EPD_D0` | 4 | `setI2S1pin(4, I2S1O_DATA_OUT0_IDX, 0)` |
| `EPD_D1` | 5 | `…OUT1…` |
| `EPD_D2` | 18 | `…OUT2…` |
| `EPD_D3` | 19 | `…OUT3…` |
| `EPD_D4` | 23 | `…OUT4…` |
| `EPD_D5` | 25 | `…OUT5…` |
| `EPD_D6` | 26 | `…OUT6…` |
| `EPD_D7` | 27 | `…OUT7…` |
| `EPD_CL` | 0 | `GPIO.out` bit `0x01`, `pinMode(0, …)` |
| `EPD_LE` | 2 | `GPIO.out` bit `0x04`, `pinMode(2, …)` |
| `EPD_CKV` | 32 | `GPIO.out1` bit `0x01`, `pinMode(32, …)` |
| `EPD_SPH` | 33 | `GPIO.out1` bit `0x02`, `pinMode(33, …)` |
| `V_BAT` | **35** | module pad 7 |
| `IO34` | 34 | net name states it |
| `GPIO_36` / `GPIO_39` | 36 / 39 | net names state it |

Note `EPD_CL` = **GPIO 0** and `EPD_LE` = **GPIO 2**, which are both ESP32 **strapping pins**. The display bus and the boot-mode straps share pins. In normal operation this is fine because the panel is idle at reset, but it is why the board needs the MOSFET gate described in §4.

---

## 2. E-paper interface

| Signal | Where | Notes |
|---|---|---|
| `EPD_D0`–`EPD_D7` | ESP32 GPIO 4, 5, 18, 19, 23, 25, 26, 27 | **I2S1 parallel output, DMA-fed** |
| `EPD_CL` | GPIO 0 | line clock, bit-banged via `GPIO.out_w1ts/w1tc` |
| `EPD_LE` | GPIO 2 | latch enable |
| `EPD_CKV` | GPIO 32 | via `GPIO.out1` |
| `EPD_SPH` | GPIO 33 | via `GPIO.out1` |
| `EPD_OE` | **expander pin 1** | output enable |
| `EPD_GMODE` | **expander pin 2** | gate mode |
| `EPD_SPV` | **expander pin 3** | vertical start pulse |

The split is deliberate: **fast signals on native GPIO driven by I2S DMA, slow control signals behind I²C.** The ESP32 has no LCD peripheral, so I2S1 in parallel mode is the workaround the entire Inkplate family is built on.

`EPD_CL` also reaches `U8.4` (`SN74LVC1G34` buffer) and `K20.13` — the clock is buffered before it reaches the panel connector.

---

## 3. PCAL6416A I/O expander (U9) — complete pin map

I²C address **0x20** (`IO_INT_ADDR`).

| Pad | Net | Library name | Purpose |
|---:|---|---|---|
| 1 | `EPD_OE` | `OE` (0) | e-paper output enable |
| 2 | `EPD_GMODE` | `GMOD` (1) | e-paper gate mode |
| 3 | `EPD_SPV` | `SPV` (2) | e-paper vertical start |
| 4 | `WAKEUP` | `WAKEUP` (3) | TPS65186 wake |
| 5 | `PWRUP` | `PWRUP` (4) | TPS65186 power-up |
| 6 | `VCOM_CTRL` | `VCOM` (5) | TPS65186 VCOM control |
| 7 | `INT` | — | interrupt |
| 8 | `PWR_GOOD` | — | **from TPS65186 pin 24** — PMIC power-good status |
| 9, 18, 25 | `GND` | | |
| **10** | **`GPIO_0_MOSFET`** | — | **gates ESP32 GPIO0** — see §4 |
| 11 | `Net-(JP6-Pad2)` | `SD_PMOS_PIN` (B2/10) | **microSD power MOSFET**, via jumper `JP6` |
| 12 | `Net-(JP5-Pad2)` | — | via jumper `JP5` |
| 13–17 | `/MCU/GPB_3` … `GPB_7` | GPB3–GPB7 | **free user I/O**, broken out |
| 19 | `I2C_SCL` | | |
| 20 | `I2C_SDA` | | |
| 21, 23 | `3V3` | | |
| 22 | `/MCU/INTB` | | interrupt B |
| 24 | `RST` | | shared reset with the ESP32 |

**`/MCU/GPB_3` through `GPB_7` are five genuinely free expander pins.** Given how thoroughly the native ESP32 GPIO is consumed by the display bus, these are the realistic expansion points for a project — at I²C speed, so suitable for LEDs, buttons and enables, not for anything timing-critical.

---

## 4. GPIO0 is MOSFET-gated by the expander

Net `GPIO_0_MOSFET` connects **expander pin 10** → `Q1.1` (MOSFET gate) → `R19`. Separately `GPIO_0` reaches `U10.25`, `Q1.3`, `Q3.3`, `R21`, `R46` and jumper `JP7`.

GPIO0 is the ESP32's **boot-mode strapping pin** *and* the e-paper line clock (`EPD_CL`). Those two roles conflict: the panel needs to toggle it constantly, but the ROM samples it at reset. The MOSFET lets firmware isolate GPIO0 so display activity cannot influence boot mode, and so the auto-reset circuit can drive it during programming.

**Practical consequence:** if you write bare-metal code that drives GPIO0 without configuring the expander first, behaviour depends on the MOSFET state and you can make the board unbootable until a manual reset. Use the library.

---

## 5. Battery sensing is a switched divider

This is the detail worth knowing, and it is the opposite of the [XIAO ESP32S3 Sense's situation](../../seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md#82-there-is-no-battery-voltage-sense--confirmed-by-the-vendor), where no battery sense exists at all.

```
VBAT ──┬── R29 ──┬── Q4/Q5 (MOSFET switch) ── Net-(Q5-Pad3) ── R30 ──┬── V_BAT ── U10.7 (GPIO35, ADC)
       │         │                                                   │
       └─ …      └── V_BAT_MOS ── R25 ── GND                          └── R31 ── GND
```

Confirmed net members:

- `V_BAT` → `K22.1`, `R30.1`, `R31.2`, **`U10.7`** (the ESP32 ADC input)
- `V_BAT_MOS` → `JP6.1`, `Q4.1`, `R25.2`
- `VBAT` → `C24`, `C25`, `K1.8`, `K4.1`, `PAD1.1`, `Q5.2`, `Q7.3`, `R29.2`, `U4.3` (the MCP73831 charger)

The MOSFET pair (`Q4`/`Q5`) **disconnects the divider when not measuring**. A permanently-connected divider is a continuous drain — the classic mistake on battery devices, and precisely what makes a naive `analogRead` divider cost tens of microamps. Soldered switch it, which is why the Inkplate reaches respectable deep-sleep figures.

The library exposes this as `double readBattery()` (declared in `Inkplate5Driver.h`) and over UART as [Peripheral Mode](features/peripheral-mode.md) command `#P(?)*`.

---

## 6. microSD (K11) — SPI, and power-switched

| Pad | Net |
|---:|---|
| 1 | *unconnected* |
| 2 | `Net-(JP3-Pad1)` → `SPI_CS` |
| 3 | `SPI_MOSI` |
| **4** | **`3V3_MICROSD`** |
| 5 | `SPI_SCK` |
| 6 | `GND` |
| 7 | `SPI_MISO` |
| 8 | *unconnected* |

**1-bit SPI, not 4-bit SDIO** — pads 1 and 8 (DAT1/DAT2) are unconnected.

The card runs from a **separate switched rail**, `3V3_MICROSD`, gated by `Q10` and controlled through `JP6` → expander pin 11 (`SD_PMOS_PIN`, library constant `IO_PIN_B2`). Net members: `C37.2`, `C38.2`, `C39.2`, `JP1.1`, `K11.4`, `Q10.3`, `R43.2`, `R44.2`, `R45.2`.

> **The most common first-time SD failure on an Inkplate is forgetting to power the card.** `SD.begin()` will simply fail because the rail is off. The library's `sdCardInit()` handles it; hand-rolled code must assert the expander pin first.

`R43`/`R44`/`R45` pull `SPI_MOSI`/`SPI_MISO` (and the rail) — note these tie to `3V3_MICROSD`, not `3V3`, so the pull-ups also disappear when the card is powered down. That is correct design (no leakage path into an unpowered device) and worth copying.

---

## 7. Broken-out headers

The BOM lists **34 × `HEADER_MALE_1X1_Inkplate`** pads. Confirmed from the netlist:

| Header | Net |
|---|---|
| `K32` | `SPI_SCK` |
| `K33` | `SPI_MISO` |
| `K34` | `SPI_MOSI` |
| `K35` | `GPIO_39` |
| `K36` | `GPIO_36` |
| `K22` | `V_BAT` |
| `K20.13` | `EPD_CL` (buffered) |

Plus the expander's `GPB_3`–`GPB_7`. In practice your expansion budget is: **`IO34`, `GPIO_36`, `GPIO_39`** (input-capable, and 34/36/39 are **input-only** on the ESP32), the shared **SPI bus**, the **I²C bus** (easyC/Qwiic connector `K3`), and **five expander pins**.

Everything else is committed to the display.

---

## 8. Jumper configuration

Soldered break several functions out to solder jumpers, which is how you reclaim pins:

| Jumper | Function |
|---|---|
| `JP1` | microSD rail |
| `JP2` | `GPIO_39` routing |
| `JP3` | `SPI_CS` ↔ microSD CS |
| `JP4` | `IO34` routing |
| `JP5` | expander pin 12 |
| `JP6` | expander pin 11 ↔ SD power MOSFET / `V_BAT_MOS` |
| `JP7` | `GPIO_0` |
| `JP8` | soldermask-defined trace jumper |

Cutting `JP3` frees `SPI_CS` from the SD card if you want the SPI bus for something else. This is the sanctioned way to repurpose pins on this board, and it is why the BOM carries five `SMD_JUMPER_3_PAD_CONNECTED_LEFT_TRACE` parts.

---

## 9. Related

- [`README.md`](README.md) — device record, BOM, family
- [`features/peripheral-mode.md`](features/peripheral-mode.md) — UART control protocol
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
- [Inkplate 5 Gen 2](../inkplate-5-gen2/README.md)
- Components: [ESP32-WROVER](../../../components/espressif/esp32-wrover/README.md) · [PCAL6416A](../../../components/nxp/pcal6416a/README.md) · [TPS65186](../../../components/texas-instruments/tps65186/README.md) · [ED052TC2/TC4](../../../components/e-ink/ed052tc4/README.md)
