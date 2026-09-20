# Texas Instruments TCA8418 — I²C keypad scanner / GPIO expander

> **Exact part on the boards documented here: `TCA8418RTWR`** — 24-pin WQFN (RTW), tape and reel.
> Record created **2026-09-04** from the M5Stack Cardputer ADV schematic and three independent
> driver implementations. **No TI datasheet was retrieved in this pass** — see *Gaps*.

## Function

A dedicated **keypad scan and key-event FIFO** controller on I²C. It owns the matrix: it drives
the columns, senses the rows, debounces, and presents *events* (key down / key up, encoded as a
single byte) through a 10-deep FIFO, asserting an interrupt when the FIFO is non-empty. Unused
matrix pins can be repurposed as general GPIO.

The value proposition is pin count. A 56-key matrix costs **ten** MCU GPIOs scanned directly; it
costs **three** through a TCA8418 (SDA, SCL, INT), two of which are a bus you probably already
have.

## Key capabilities

| Property | Value | Evidence |
|---|---|---|
| Interface | I²C, up to 400 kHz | driver usage |
| Matrix | up to **8 ROW × 10 COL = 80 keys** | pin complement `ROW0..7`, `COL0..9`, both fully visible on the Cardputer ADV schematic symbol |
| Event FIFO | 10 deep | Adafruit driver + Bruce comments |
| Event encoding | one byte: `bit7` = state (1 = press), `bits6..0` = `row × 10 + col + 1` | derived from the vendor decode, below |
| Interrupt | active-low, open-drain, needs a pull-up | Cardputer ADV fits **3.3 kΩ** |
| Supply | 3.3 V on both boards seen | schematic |
| Package | WQFN-24 (RTW) with an exposed pad | schematic symbol has pins 1–24 **plus `EP` (25)** |
| Reset | active-low `RESET` pin | see the hazard below |

### Event decode

From `M5Cardputer/src/utility/Keyboard/KeyboardReader/TCA8418.cpp:75-85`:

```cpp
ret.state = eventRaw & 0x80;          // 1 = pressed
uint16_t buffer = eventRaw & 0x7F;
buffer--;                             // FIFO encodes 1-based
ret.row = buffer / 10;                // base 10, not base 8 -- because COL goes to 9
ret.col = buffer % 10;
```

The **base-10** arithmetic is the thing to remember: the FIFO packs `(row, col)` as
`row × 10 + col + 1` because the part supports ten columns. Implementations that assume base 8
will decode correctly only for `col < 8` on `row 0`.

## Pins seen in use

| Pin | Name | Note |
|---|---|---|
| 1–8 | `ROW7`…`ROW0` (descending) | pin 8 is `ROW0` |
| 9–18 | `COL0`…`COL9` (ascending) | |
| 19 | `GND` | |
| 20 | `RESET` | active low |
| 21 | `VCC` | |
| 22 | `SDA` | |
| 23 | `SCL` | |
| 24 | `INT` | active low, open drain |
| 25 | `EP` | exposed pad → GND |

Read from the rendered M5Stack Cardputer ADV schematic sheet 2. **This ordering is worth
checking against TI's datasheet before you lay out a board** — it is a reading of one vendor's
symbol, and vendor symbols are occasionally wrong.

## Addressing

`0x34` on every board seen here, and it is the Adafruit library's default.

> ⚠ **A community document gets this wrong.** `bmorcelli/Launcher`'s `CardputerADV.md` lists
> "`0x18`: Likely accelerometer/IMU" and "`0x69`: Likely additional sensor" alongside `0x34`.
> On the Cardputer ADV, `0x18` is the **ES8311 codec** and `0x69` is the **BMI270**. The `0x34`
> entry is right.

## Software

| Option | Notes |
|---|---|
| **`adafruit/Adafruit TCA8418`** (`^1.0.2`) | the de-facto driver. M5Stack **vendors a modified copy** at `M5Cardputer/src/utility/Adafruit_TCA8418/`; Bruce pulls it from the registry |
| `M5Cardputer` `TCA8418KeyboardReader` | interrupt-driven wrapper, board-specific remap |
| Bruce `boards/m5stack-cardputer/interface.cpp` | polling wrapper with key repeat |
| ESP-IDF | `M5Cardputer-UserDemo` `main/hal/utils/adafruit_tca8418/` |

Minimal initialisation, from the vendor reader:

```cpp
Adafruit_TCA8418 tca;
tca.begin(0x34, &Wire1);
tca.matrix(rows, cols);        // enrol the matrix -- pins NOT enrolled are never scanned
tca.flush();                   // drain stale events
tca.enableInterrupts();
```

Clearing the interrupt (note the read-back — a single write is not enough if events are queued):

```cpp
tca.writeRegister(TCA8418_REG_INT_STAT, 1);
if ((tca.readRegister(TCA8418_REG_INT_STAT) & 0x01) == 0) isr_flag = false;
```

## Driver audit findings

Reading the three implementations side by side, with the caveat that **no datasheet was
available to check them against**:

* **None of the three touches the GPIO, debounce-configuration, key-lock or GPI-event registers.**
  Everything uses defaults. The part's debounce behaviour on these boards is therefore whatever
  TI ships from reset — undocumented in every downstream project.
* **None reads a device-ID or performs any presence check beyond `begin()` succeeding.** Bruce
  uses exactly that as its board-detection mechanism, which works but conflates "no TCA8418" with
  "I²C bus broken".
* **Bruce polls at ~100 ms** with its own repeat timers (`TCA8418_REPEAT_START_MS 350`,
  `TCA8418_REPEAT_MS 150`) rather than using `INT`. Perceptibly less responsive on held keys than
  the vendor library's interrupt path. A deliberate adaptation, not a defect — but a real
  behavioural difference between firmwares on identical hardware.
* **`matrix(rows, cols)` is load-bearing and silent.** Pins not enrolled are never scanned and
  never produce events. A wrong argument produces a partly-working keyboard with no error.

## Used By

### M5Stack Cardputer ADV (K132-Adv) — [`devices/m5stack/cardputer-adv`](../../../devices/m5stack/cardputer-adv/README.md)

Designator **U9**. `matrix(7, 8)` — 7 ROW × 8 COL = 56 keys.
`SDA` ← **G8**, `SCL` ← **G9**, `INT` ← **G11**, all with **3.3 kΩ** pull-ups (R37, R36, R35).
`COL0..COL7` reach the matrix through **22 Ω 1 %** series resistors R27–R34, and the
**`COL`→net mapping is reversed**: `COL0 → Y7` … `COL7 → Y0`.
**`ROW7`, `COL8` and `COL9` are explicit no-connects** (drawn `×`, a positive assertion).

⚠ **`RESET` (pin 20) is tied to +3.3 V through R38 (10 kΩ) and reaches no GPIO.** There is no
software recovery from a wedged scanner on this board; only a power cycle.

The board's I²C pull-ups on `SDA`/`SCL` are also what **M5GFX uses to identify the ADV**: it
drives G8/G9 as input-pulldown and tests whether they still read high.
Full treatment: [`devices/m5stack/cardputer-adv/features/keyboard.md`](../../../devices/m5stack/cardputer-adv/features/keyboard.md).

### M5Stack CardputerZero (C154 / C155) — [`devices/m5stack/cardputer-zero`](../../../devices/m5stack/cardputer-zero/README.md)

Same part, same address `0x34`, on a **Raspberry Pi CM0** host rather than an ESP32-S3.
**46 keys.** `SDA`/`SCL` on `G2`/`G3` (`I2C1`), `KB_INT` on `G27`.
Its `RESET` **is** controllable — but indirectly, and it is **shared with the USB hub**:
`PYG3_KB_HUB_RST` on the M5IOE1 expander resets the TCA8418 **and** the GL852G-OHY60 together.
That is a better arrangement than the ADV's (recovery is possible) with a caveat (you cannot
reset the keyboard without also resetting USB).

### LilyGO T-Display K230 Kit — [`devices/lilygo/t-display-k230`](../../../devices/lilygo/t-display-k230/README.md) · *added 2026-09-07*

On the **nRF9151 keyboard base board**, not the main board. I²C4 shared bus:
`SDA` ← `GPIO47`, `SCL` ← `GPIO46`, 7-bit address **`0x34`**, `RESET` ← `GPIO43`,
`IRQ` → `GPIO42`. Configured **`matrix(7, 10)`** — 7 ROW × 10 COL — while the launcher draws a
6 × 11 layout. Code → position is `row = (code-1)/10`, `col = (code-1)%10`.

Registers driven by LilyGO's userspace driver: `CFG 0x01`, `INT_STAT 0x02`, `KEY_LCK_EC 0x03`,
`KEY_EVENT_A 0x04`, `KP_GPIO_1/2/3 0x1D/0x1E/0x1F`, `DEBOUNCE_DIS_1/2/3 0x29/0x2A/0x2B`.
Config mode `KE_IEN | OVR_FLOW_IEN | OVR_FLOW_M` with IRQ (default), or `OVR_FLOW_M` with polling.

⚠ **Userspace rewrites the K230 IOMUX register for `GPIO42` directly** (offset `42*4`, value
`0x00000344`) to force GPIO-input mode, bypassing the kernel pin controller. If another driver
later re-muxes that pin, the keyboard IRQ stops with no error.

Full key map (60 named keys, two `SPACE` codes, two `FN` keys, a `LILYGO` key and a `MIC` key):
[`pinouts-and-buses.md` §8](../../../devices/lilygo/t-display-k230/pinouts-and-buses.md#8-keyboard-matrix--full-decode).

*Source: `scratch/lilygo-k230/index-fragments.md` §F2.*

## Substitutes

| Part | Trade-off |
|---|---|
| **74HC138 + N sense GPIOs** | what the Cardputer v1.0/v1.1 do. Free and simple; costs 10 GPIOs and CPU time, and gives no debounce or FIFO |
| Adafruit/Microchip `MCP23017` etc. | a general expander, not a scanner — you still implement scanning and debounce in firmware |
| `TCA8418E` | the same part in a different package/temperature grade; not seen here |
| An MCU with enough pins | the honest alternative when pin count is not the constraint |

## Gaps

* **No TI datasheet retrieved.** Register addresses, debounce timing, electrical limits, the
  official pinout and the GPIO-mode configuration are all **not verified against a primary
  document** in this pass. Everything above comes from a vendor schematic and three drivers.
  `https://www.ti.com/product/TCA8418` is the place to start.
* Pricing, lifecycle status and package variants: **not researched**.
* The `EP`/pin-25 numbering is as drawn by M5Stack; TI may number it differently.
