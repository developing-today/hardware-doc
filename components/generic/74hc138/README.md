# 74HC138 — 3-to-8 line decoder / demultiplexer

> Generic logic family part. Record created **2026-09-04** from the M5Stack Cardputer
> v1.0/v1.1 schematic and the vendor keyboard driver. Manufacturer **not specified** on the
> schematic — the value string is simply `74HC138`, which is a multi-source industry-standard
> part (NXP, TI, Toshiba, Nexperia, Diodes, and many Chinese second sources all make it).

## Function

Decodes a 3-bit binary address (`A0`, `A1`, `A2`) to **one of eight active-low outputs**
(`/Y0`…`/Y7`), gated by three enables: `/E1`, `/E2` (active low) and `E3` (active high). Exactly
one output is low at a time when enabled; all eight are high when disabled.

In a keyboard it is the cheapest possible way to drive a matrix: three MCU pins select which of
eight column lines is pulled low, and the MCU reads the row lines to see which key shorted.

## Key capabilities

| Property | Value |
|---|---|
| Function | 3-to-8 decoder, **active-low** outputs |
| Enables | `/E1`, `/E2` active low; `E3` active high |
| Supply | 2–6 V (HC family); **3.3 V** on the boards here |
| Package | SOIC-16 / TSSOP-16, 16 pins |
| Propagation delay | tens of ns at 3.3 V — irrelevant beside the firmware's `digitalWrite()` overhead |

## Pinout as fitted (read from the M5Stack schematic)

| Pin | Name | Pin | Name |
|---|---|---|---|
| 1 | `A0` | 16 | `VCC` |
| 2 | `A1` | 15 | `/Y0` |
| 3 | `A2` | 14 | `/Y1` |
| 4 | `/E1` | 13 | `/Y2` |
| 5 | `/E2` | 12 | `/Y3` |
| 6 | `E3` | 11 | `/Y4` |
| 7 | `/Y7` | 10 | `/Y5` |
| 8 | `GND` | 9 | `/Y6` |

This is the standard industry pinout; the M5Stack symbol matches it.

## Used By

### M5Stack Cardputer v1.0 (K132) and v1.1 (K132-V11)

[`devices/m5stack/cardputer-v1.0`](../../../devices/m5stack/cardputer-v1.0/README.md) ·
[`devices/m5stack/cardputer-v1.1`](../../../devices/m5stack/cardputer-v1.1/README.md)
*(the two boards share one published schematic file, SHA-256 `6016c1fe…`)*

Designator **U7**, on the keyboard sheet. It is the **entire** keyboard scanner: there is no
dedicated keypad controller on these boards.

| Signal | Connection |
|---|---|
| `A0` (pin 1) | **G8** |
| `A1` (pin 2) | **G9** |
| `A2` (pin 3) | **G11** |
| `/E1`, `/E2` (pins 4, 5) | **GND** — permanently enabled |
| `E3` (pin 6) | **+3.3 V** — permanently enabled |
| `/Y0`…`/Y7` | through **22 Ω 1 %** series resistors **R34…R27** to the matrix nets `Y0`…`Y7` |
| `VCC` / `GND` | +3.3 V / GND |

The seven **sense** lines (`G13, G15, G3, G4, G5, G6, G7`) go straight to the MCU as
`INPUT_PULLUP`; the pressed key pulls one low when its column is selected.

Vendor driver,
[`IOMatrix.cpp`](https://github.com/m5stack/M5Cardputer/blob/f1392858b9994c3547120e602a57d3553d16ab01/src/utility/Keyboard/KeyboardReader/IOMatrix.cpp):

```cpp
const std::vector<int> output_list = {8, 9, 11};                 // A0, A1, A2
const std::vector<int> input_list  = {13, 15, 3, 4, 5, 6, 7};    // seven sense lines
void set_output(const std::vector<int>& p, uint8_t v) {           // v masked to 3 bits
    digitalWrite(p[0], v & 1); digitalWrite(p[1], v & 2); digitalWrite(p[2], v & 4); }
for (int i = 0; i < 8; i++) { set_output(output_list, i); … }     // eight columns per scan
```

**Cost: ten GPIOs**, which is the entire reason the Cardputer ADV exists. The ADV replaces this
part with a [TCA8418](../../texas-instruments/tca8418/README.md) on I²C, keeps the **identical
matrix** — same 56 switches, same `Y0..Y7` nets, same R27–R34 22 Ω resistors — and spends three
pins instead of ten. The full comparison, including the proof that the two drivers' coordinate
maths are algebraically equivalent, is at
[`devices/m5stack/cardputer-adv/features/keyboard.md`](../../../devices/m5stack/cardputer-adv/features/keyboard.md).

## Practical notes

* **No debounce, no FIFO, no interrupt.** Everything is firmware's problem, and the scan is
  fully synchronous: eight `set_output()` + seven `digitalRead()` per `update()`.
* **No diodes in the Cardputer matrix**, so ghosting is possible on three-key combinations that
  form a rectangle. The vendor driver reports all pressed coordinates and does not attempt to
  detect ghosts.
* The **22 Ω series resistors** are current-limiting/edge-softening on the drive lines, not
  pull-ups. They are shared with the ADV design, which is a strong hint the matrix sub-sheet was
  copied wholesale.
* Because the outputs are **active low**, an unenabled or floating decoder leaves all columns
  high and the keyboard simply reports nothing.

## Substitutes

Any 74HC138/74HCT138/74LVC138 from any vendor, subject to supply voltage. A larger matrix would
want a `74HC154` (4-to-16) or a dedicated scanner. The dedicated-scanner route is what M5Stack
eventually took.

## Gaps

* **No datasheet retained**, and no manufacturer identified — the schematic value is the generic
  family number. Any vendor's HC138 datasheet applies; none was fetched in this pass.
* Package, temperature grade and actual manufacturer on the fitted part: **unknown**. A board
  photograph of U7's top marking would settle it.
