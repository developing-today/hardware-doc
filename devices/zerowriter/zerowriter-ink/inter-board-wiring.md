# ZeroWriter Ink — inter-board wiring

> The three-board architecture, both connector pinouts recovered from KiCad, and what the net names reveal about the design's history.
> Snapshot **2026-08-24**. Extracted from the project's own `.kicad_pcb` files with [`../../soldered-electronics/inkplate-5/tools/kicad_pcb_nets.py`](../../soldered-electronics/inkplate-5/tools/kicad_pcb_nets.py).

This document closes two gaps I previously recorded as open: *"which pins of the 6-pin connector carry TX/power/ground"* and *"the breakout board has no schematic"*. **The breakout board does have a full KiCad schematic and PCB** — my earlier claim was wrong, based on looking only at `OUTPUTS/SingleBoardOutputs/`, which contains gerbers. The sources are in `v1.2.0/CAD/`.

## Three boards, two cables

```
┌── Zerowriter Keyboard ──────────────────────┐
│  ESP32-WROOM-32U-N4  ·  5×14 matrix         │
│  K2: 6-pin programmer header                │
└──────────── K1: 6-pin HC-1.25-6PWT ─────────┘
                       │  3V3 · UART · GND
┌── Zerowriter Inkplate 5 Gen2 (main) ────────┐
│  ESP32-WROVER · ED052TC4 · TPS65186         │
│  PCAL6416A · PCF85063A · BQ25306            │
└──────────── K1: 16-pin HC-1.25-16PWT ───────┘
                       │  USB · SD · power · switch · LEDs
┌── Zerowriter breakout board ────────────────┐
│  USB-C (K1) · microSD (K2) · power switch   │
│  charge + power LEDs · 350 mA PTC fuse      │
└─────────────────────────────────────────────┘
```

The **display board sits in the middle**. Both the human-interface board (keyboard) and the I/O board (USB/SD) hang off it.

---

## Keyboard ↔ main board — 6-pin `HC-1.25-6PWT`

| Pin | Net | Function |
|---:|---|---|
| 1 | `+3V3` | supply |
| 2 | `+3V3` | supply |
| 3 | `/USART2_RX` | keyboard RX (unused — keyboard is TX-only) |
| 4 | `/USART2_TX` | **keyboard TX → main board**, 921600 baud |
| 5 | `Earth` | ground |
| 6 | `Earth` | ground |
| (7) | `Earth` | shield/mechanical |

Two power, two ground, two data. This confirms the [keyboard protocol](keyboard.md) analysis: **the RX line is physically present but the firmware disables it** (`Serial.begin(921600, SERIAL_8N1, -1, 1)` — RX pin `-1`).

So the hardware *could* support bidirectional communication; only firmware makes it one-way. A future update could enable main→keyboard messaging without a hardware change. That is a more encouraging conclusion than the firmware alone suggested.

### Keyboard programmer header — 6-pin `K2`

| Pin | Net |
|---:|---|
| 1 | `Earth` |
| 2 | `+3V3` |
| 3 | `/USART2_TX` |
| 4 | `/USART2_RX` |
| 5 | `/NRST` |
| 6 | `/BOOT0` |

A complete flashing header: power, ground, both UART lines, reset and boot-mode. Matches the firmware's comment that the keyboard "has programming pins at the bottom — you can program it using a USB-UART adapter".

Note `/NRST` lands on **U1 pad 3 = `EN`** and `/BOOT0` on **U1 pad 25 = `IO0`** — the ESP32's reset and boot-strap pins under STM32 names.

---

## Main board ↔ breakout — 16-pin `HC-1.25-16PWT`

| Pin | Net | Function |
|---:|---|---|
| 1 | `CHRG-ST` | charge status → charge LED |
| 2 | `PWR_LED` | power LED drive |
| 3 | `PWR_SW` | **power switch** |
| 4 | `3V3_MICROSD` | switched microSD rail |
| 5 | `SPI_SD_CS` | microSD chip select |
| 6 | `SPI_MOSI` | microSD |
| 7 | `SPI_MISO` | microSD |
| 8 | `GND` | |
| 9 | `SPI_SCK` | microSD |
| 10 | `GND` | |
| 11 | `D+` | **USB data +** |
| 12 | `D-` | **USB data −** |
| 13 | `GND` | |
| 14 | `VUSB` | USB 5 V |
| 15 | `VUSB` | USB 5 V |
| 16 | `VUSB` | USB 5 V |
| (17) | `GND` | shield/mechanical |

Three pins for `VUSB` and four grounds — appropriate for charge current. **USB D± cross this connector**, so the cable carries full-speed USB signalling between boards; keep it short and avoid substituting an arbitrary jumper cable.

`3V3_MICROSD` crossing the connector confirms the switched-SD-rail architecture inherited from the [Inkplate design](../../soldered-electronics/inkplate-5/pinouts-and-buses.md#6-microsd-k11--spi-and-power-switched) — the card is powered down via the I/O expander, and that control reaches across to the breakout board.

---

## Breakout board — complete BOM and nets

15 component types, no active silicon beyond connectors, LEDs and protection.

| Ref | Part | Function |
|---|---|---|
| **K1** | `U262-161N-4BVC11` | **USB-C receptacle** |
| **K2** | `HYC77-TF09-200` | **microSD socket** |
| **K3** | `HC-1.25-16PWT` | 16-pin cable to main board |
| **S1** | `SK-3296S-01-L1` | **power slide switch** |
| **F1** | `SMD1206-350-6V` | **350 mA / 6 V resettable PTC fuse** |
| D1 | `LTST-S270EKT` | charge-status LED |
| D2 | `LTST-S270TBKT` | power LED |
| R1, R2 | 5k1 | **USB-C CC pull-downs** (correct UFP config) |
| R3 | 2k2 | charge LED series |
| R4 | 1k | power LED series |
| R5, R6, R7 | 100k | SPI pull-ups on `SPI_SD_CS`, `MOSI`, `MISO` |
| C1 | 2u2 | |
| C2, C3 | 100n | |
| H1–H3 | 3.2 mm holes | mounting |

Notable details recovered from the netlist:

- **`R1`/`R2` = 5.1 kΩ on `CC1`/`CC2`** — the standard USB-C sink configuration, so it negotiates 5 V from a C-to-C cable correctly.
- **`F1` is a 350 mA PTC** on `VUSB` — input current is limited to 350 mA. That constrains charge rate regardless of what the `BQ25306` could deliver, and is worth knowing before anyone assumes fast charging.
- **`K1.A8`/`K1.B8` (SBU1/SBU2) are unconnected** — no alternate-mode or debug-accessory capability.
- **The SPI pull-ups tie to `3V3_MICROSD`**, not a permanent rail — so they vanish when the card is powered down. Same correct pattern as the Inkplate.
- `K2.1` and `K2.8` unconnected — **1-bit SPI microSD**, not 4-bit SDIO, consistent with the Inkplate lineage.

---

## What the net names reveal

The keyboard board uses net names that **do not belong to an ESP32 design**:

| Net on keyboard board | ESP32 reality |
|---|---|
| `/USART2_TX`, `/USART2_RX` | ESP32 has `UART0/1/2`, never "USART" |
| `/NRST` | ESP32 calls it `EN` / `CHIP_PU` |
| `/BOOT0` | ESP32 calls it `GPIO0` |
| `Earth` | Soldered's boards use `GND` |
| `+3V3` | Soldered's boards use `3V3` |

`USART`, `NRST` and `BOOT0` are **STM32** naming conventions. The fitted part is unambiguously an `ESP32-WROOM-32U-N4` (`RF_Module:ESP32-WROOM-32U` footprint, and the pad functions are ESP32 — `SENSOR_VP`, `IO34/35`, `SD0–SD3`).

Combined with the keyboard firmware's own comment —

> we should move away from esp32 to a STM chip, or a cheaper/lower power alternative

— the most likely reading is that the keyboard schematic was **drawn from an STM32 template or a prior STM32 revision**, with the labels carried over when an ESP32 was substituted. It also confirms the **keyboard was not designed by Soldered**: the main board uses Soldered's `GND`/`3V3` conventions and their title block, while the keyboard uses `Earth`/`+3V3`.

> Evidence status: the net names and the fitted part are **primary and unambiguous**. The *inference* that an STM32 design preceded it is **plausible but unproven** — a designer's personal naming habit would produce the same artifact.

## Independent confirmation of the firmware pin map

The PCB netlist and the firmware's `rowPins[]`/`colPins[]` arrays agree completely. Mapping ESP32-WROOM-32U module pads to GPIO:

| Pad | GPIO | Net | Firmware |
|---:|---:|---|---|
| 16 | IO13 | `Row 1` | `rowPins[0] = 13` ✅ |
| 14 | IO12 | `Row 2` | `rowPins[1] = 12` ✅ |
| 12 | IO27 | `Row 3` | `rowPins[2] = 27` ✅ |
| 11 | IO26 | `Row 4` | `rowPins[3] = 26` ✅ |
| 13 | IO14 | `Row 5` | `rowPins[4] = 14` ✅ |
| 31 | IO19 | `Col 1` | `colPins[0] = 19` ✅ |
| 33 | IO21 | `Col 2` | `colPins[1] = 21` ✅ |
| 37 | IO23 | `Col 3` | `colPins[2] = 23` ✅ |
| 36 | IO22 | `Col 4` | `colPins[3] = 22` ✅ |
| 24 | IO2 | `Col 5` | `colPins[4] = 2` ✅ |
| 23 | IO15 | `Col 6` | `colPins[5] = 15` ✅ |
| 26 | IO4 | `Col 7` | `colPins[6] = 4` ✅ |
| 27 | IO16 | `Col 8` | `colPins[7] = 16` ✅ |
| 28 | IO17 | `Col 9` | `colPins[8] = 17` ✅ |
| 29 | IO5 | `Col 10` | `colPins[9] = 5` ✅ |
| 30 | IO18 | `Col 11` | `colPins[10] = 18` ✅ |
| 10 | IO25 | `Col 12` | `colPins[11] = 25` ✅ |
| 9 | IO33 | `Col 13` | `colPins[12] = 33` ✅ |
| 8 | IO32 | `Col 14` | `colPins[13] = 32` ✅ |
| 34 | RXD0 | `/USART2_RX` | RX disabled in firmware |
| 35 | TXD0 | `/USART2_TX` | **TX, GPIO 1** ✅ |

**19 of 19 matrix pins match.** The published firmware corresponds to the published hardware — worth establishing, since the repo warns that factory units may run older firmware.

## Related

- [`keyboard.md`](keyboard.md) — protocol, matrix, power management
- [`keymap-format.md`](keymap-format.md) — `keymap.json`
- [`firmware-and-updates.md`](firmware-and-updates.md) — why the keyboard must be unplugged to flash
- [`README.md`](README.md)
