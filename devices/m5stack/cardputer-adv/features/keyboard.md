# Cardputer ADV — how the keyboard works

> **Question answered:** *"How do I read the keyboard on a Cardputer ADV, and how is it wired?"*
> Applies to: **Cardputer ADV (K132-Adv)** only. The v1.0/v1.1 answer is
> [`../../cardputer-v1.1/README.md`](../../cardputer-v1.1/README.md) and is completely different.
> Evidence: schematic sheet 2 (rendered), `M5Cardputer` @ `f1392858`, `M5GFX` @ `d91077b9`.
> Last verified **2026-09-04**. Not hardware-tested by this session.

## Summary

56 keys in a **4 rows × 14 columns** legend layout, wired as an **8 × 7 electrical matrix**,
scanned by a **TI TCA8418RTWR** keypad scanner over the internal I²C bus at **`0x34`**, which
raises **GPIO 11** when there is an event to read. Three GPIOs total, two of which are the I²C
bus you wanted anyway.

Component record: [`components/texas-instruments/tca8418`](../../../../components/texas-instruments/tca8418/README.md).

## The hardware path

```
56 × SW-PB (S1..S56)
   │  column side (pairs)          row side (rows + parity)
   ├── ROW0..ROW6  ──────────────► TCA8418 pins 8..2
   └── Y0..Y7 ── R27..R34 22 Ω ──► TCA8418 COL7..COL0 (pins 16..9)
                                        │
                        SDA G8 ─────────┤  (3.3 kΩ pull-up R37)
                        SCL G9 ─────────┤  (3.3 kΩ pull-up R36)
                        INT G11 ────────┘  (3.3 kΩ pull-up R35)
                        RESET ── R38 10 kΩ ── +3V3   ← no GPIO
```

Read off the rendered sheet, U9 block:

| TCA8418 pin | Name | Net | Series R |
|---|---|---|---|
| 1 | `ROW7` | **explicit no-connect (×)** | — |
| 2 | `ROW6` | `ROW6` | — |
| 3 | `ROW5` | `ROW5` | — |
| 4 | `ROW4` | `ROW4` | — |
| 5 | `ROW3` | `ROW3` | — |
| 6 | `ROW2` | `ROW2` | — |
| 7 | `ROW1` | `ROW1` | — |
| 8 | `ROW0` | `ROW0` | — |
| 9 | `COL0` | `Y7` | R27 22 Ω 1 % |
| 10 | `COL1` | `Y6` | R28 |
| 11 | `COL2` | `Y5` | R29 |
| 12 | `COL3` | `Y4` | R30 |
| 13 | `COL4` | `Y3` | R31 |
| 14 | `COL5` | `Y2` | R32 |
| 15 | `COL6` | `Y1` | R33 |
| 16 | `COL7` | `Y0` | R34 |
| 17 | `COL8` | **explicit no-connect (×)** | — |
| 18 | `COL9` | **explicit no-connect (×)** | — |
| 19, 25 | `GND`, `EP` | GND | — |
| 20 | `RESET` | +3V3 via R38 10 kΩ — **no GPIO** | — |
| 21 | `VCC` | +3V3 | — |
| 22 | `SDA` | `G8` | pull-up R37 3.3 kΩ |
| 23 | `SCL` | `G9` | pull-up R36 3.3 kΩ |
| 24 | `INT` (active low) | `G11` | pull-up R35 3.3 kΩ |

Note the **`COL`↔`Y` reversal**: `COL0` is `Y7`, `COL7` is `Y0`. It is not a transcription
slip; it is what the sheet shows, and it is what makes the remap arithmetic below come out.

The three no-connects are drawn as explicit **×** markers, not blanks — the designer asserting
"unused", which is stronger evidence than an empty pin.

## The finding that makes the whole delta legible

**The ADV's keyboard matrix is electrically identical to the v1.0/v1.1 matrix.** Same 56
switches, same net names `Y0..Y7`, same series resistors down to the same reference designators
`R27`–`R34` at the same 22 Ω 1 %. On a v1.x, `Y0..Y7` are the eight **outputs of a 74HC138**
(U7, pins 15,14,13,12,11,10,9,7 → `Y0..Y7`, also through R34..R27) and the seven column-pair
lines go to seven GPIOs. On the ADV, `Y0..Y7` go to the TCA8418's COL pins and the seven
column-pair lines go to its ROW pins.

M5Stack redrew the driver and left the matrix alone. That is why the logical key coordinates
come out the same on both boards, and why one binary can serve both.

Note the nomenclature trap: **the TCA8418's "ROW" lines are the keyboard's *column pairs*, and
its "COL" lines are the keyboard's *rows*.** Do not read the datasheet's ROW/COL as the
keyboard's rows and columns.

## Matrix topology

| Concept | Value |
|---|---|
| Legend layout | 4 rows × 14 columns = 56 |
| Electrical matrix | **7 (TCA8418 ROW) × 8 (TCA8418 COL)** = 56 |
| `ROW`*n* serves | keyboard **columns 2n and 2n+1** |
| `COL`*m* serves | keyboard **row m mod 4**; `m ≥ 4` selects the **odd** column of the pair |
| Ghosting | no diodes fitted; the TCA8418 does key-event FIFO reporting rather than raw scan, so N-key rollover is bounded by the part, not the matrix |

Verified against the sheet at the corner of the array: **S1** (keyboard column 0, row 0) has its
top terminal on `ROW0` and its bottom terminal on **`Y7`** = `COL0`; **S2** (column 1, row 0)
shares `ROW0` and goes to **`Y3`** = `COL4`. That is exactly what the rule predicts. The `ROW0`
line visibly feeds the first switch pair, `ROW1` the second, `ROW2` the third, in a rendered
crop of the row bus.

Switch designators run **S1..S56**: S1–S14 = legend row 0, S15–S28 = row 1, S29–S42 = row 2,
S43–S56 = row 3. (The automated designator census recovered 41 of 56 because `PIS`*nn*`0m`
markers are ambiguous to split — a limitation of the marker parser, not a gap in the schematic.)

## The vendor driver, and the arithmetic

[`TCA8418.cpp`](https://github.com/m5stack/M5Cardputer/blob/f1392858b9994c3547120e602a57d3553d16ab01/src/utility/Keyboard/KeyboardReader/TCA8418.cpp):

```cpp
// line 13
#define DEFAULT_TCA8418_INT_PIN 11
…
// lines 39-49
_tca8418->matrix(7, 8);      // 7 rows, 8 columns
_tca8418->flush();
pinMode(_interrupt_pin, INPUT);
attachInterruptArg(digitalPinToInterrupt(_interrupt_pin), gpio_isr_handler, this, CHANGE);
_tca8418->enableInterrupts();
```

Event decode, lines 75–85 — the TCA8418 FIFO byte is `state<<7 | (row*10 + col + 1)`:

```cpp
ret.state = eventRaw & 0x80;
uint16_t buffer = eventRaw; buffer &= 0x7F; buffer--;
ret.row = buffer / 10;
ret.col = buffer % 10;
```

Remap to Cardputer logical coordinates, lines 88–101 — **this is the whole compatibility layer**:

```cpp
uint8_t col = key.row * 2;          // TCA8418 ROW → keyboard column pair
if (key.col > 3) col++;             //   upper 4 COLs = odd column
uint8_t row = (key.col + 4) % 4;    // == key.col % 4  → keyboard row
key.row = row;  key.col = col;
```

So `x = raw_row × 2 + (raw_col ≥ 4)`, `y = raw_col mod 4`, giving `x ∈ 0..13`, `y ∈ 0..3`.

### Why that is bit-for-bit equivalent to the v1.x reader

The v1.x reader, [`IOMatrix.cpp:91-108`](https://github.com/m5stack/M5Cardputer/blob/f1392858b9994c3547120e602a57d3553d16ab01/src/utility/Keyboard/KeyboardReader/IOMatrix.cpp#L91-L108),
walks `i = 0..7` on the 74HC138 address lines and does:

```cpp
coor.x = (i > 3) ? X_map_chart[j].x_1 : X_map_chart[j].x_2;
coor.y = (i > 3) ? (i - 4) : i;
coor.y = -coor.y; coor.y = coor.y + 3;      //  y = 3 - (i mod 4)
```

Substituting `n = 7 - m` (the `Y` index for TCA8418 `COL`*m*) into the ADV rule gives
`y = (7 - n) mod 4 = 3 - (n mod 4)` and "odd column when `n ≤ 3`" — **identical** to the v1.x
rule expressed in the same `Y` index. The two drivers produce the same `(x, y)` for the same
physical key. That is the reason a single `_key_value_map[4][14]` serves both, and it is a
deliberate design choice, not a coincidence.

## Key legend map

`_key_value_map[4][14]` in
[`Keyboard.h:19-74`](https://github.com/m5stack/M5Cardputer/blob/f1392858b9994c3547120e602a57d3553d16ab01/src/utility/Keyboard/Keyboard.h#L19-L74),
`{value_first, value_second /* Aa layer */, value_third /* fn layer */}`:

| y\x | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **0** | `` ` `` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | - | = | BkSp |
| **1** | Tab | q | w | e | r | t | y | u | i | o | p | [ | ] | \ |
| **2** | **FN** | **SHIFT** | a | s | d | f | g | h | j | k | l | ; | ' | Enter |
| **3** | **CTRL** | **OPT** | **ALT** | z | x | c | v | b | n | m | , | . | / | Space |

The **fn layer** (third value) gives `ESC` on `` ` ``, `F1`–`F12` on the number row, `DELETE`
on Backspace, and arrows on `;` `,` `.` `/` — **↑ ; ← , ↓ . → /**. It was added in
`eccba25` (2026-05-11, PR #15 by GiorgioAresu) and corrected in `84e5201` (2026-05-12); a
library older than that has no fn layer and no arrow keys.

## Minimal procedure — Arduino

```cpp
#include <M5Cardputer.h>

void setup() {
  auto cfg = M5.config();
  M5Cardputer.begin(cfg, true);        // true = enable the keyboard
  M5Cardputer.Display.setTextSize(2);
}

void loop() {
  M5Cardputer.update();                // pumps updateKeyList() + updateKeysState()
  if (M5Cardputer.Keyboard.isChange() && M5Cardputer.Keyboard.isPressed()) {
    auto st = M5Cardputer.Keyboard.keysState();
    for (auto c : st.word)  M5Cardputer.Display.print(c);
    if (st.enter) M5Cardputer.Display.println();
    if (st.del)   M5Cardputer.Display.print("\b \b");
  }
  delay(5);
}
```

`M5Cardputer.begin()` calls `M5.begin()` → M5GFX autodetect → `M5.getBoard()` returns
`board_M5CardputerADV`, and `Keyboard_Class::begin()` then injects the right reader:

```cpp
// Keyboard.cpp:21-28
if (board_type == m5::board_t::board_M5Cardputer)          _keyboard_reader = std::make_unique<IOMatrixKeyboardReader>();
else if (board_type == m5::board_t::board_M5CardputerADV)  _keyboard_reader = std::make_unique<TCA8418KeyboardReader>();
else { printf("[error] Keyboard: Unsupported board type: %d\n", (int)board_type);
       _keyboard_reader = std::make_unique<KeyboardReader>(); }   // ← does nothing
```

If autodetect fails you get the third branch: no error at compile time, a single `printf`, and
a keyboard that never reports a key. **If your keyboard is silent, check the autodetect log
line first.**

### Bring your own reader

`Keyboard_Class::begin(std::unique_ptr<KeyboardReader>)` is public, so you can inject a custom
reader without forking the library — useful if you want polling instead of interrupts, or a
different interrupt pin (`TCA8418KeyboardReader(int interrupt_pin)`).

## Alternatives

| Approach | When | Cost |
|---|---|---|
| `M5Cardputer` library (above) | almost always; you get board autodetect and both generations free | pulls in M5Unified + M5GFX + IRremote |
| `Adafruit_TCA8418` directly | you only want keys and no graphics stack | you write the remap and the legend map yourself; the vendor's vendored copy is at `src/utility/Adafruit_TCA8418/` |
| Poll instead of interrupt | you cannot spare G11, or you are inside a tight render loop | Bruce does exactly this at a 100 ms interval and it is perceptibly less responsive for held keys |
| Raw register access | you want the TCA8418's GPIO/debounce/keylock features the vendor never touches | see the component record |

## Resources consumed

| Resource | Amount |
|---|---|
| GPIO | G8, G9 (shared bus), G11 (dedicated) |
| I²C address | `0x34` on the internal bus |
| GPIO interrupt | one, on G11, `CHANGE` edge |
| Timers | none |
| RAM | `std::vector<Point2D_t>` key list, a few hundred bytes |

## Limits, pitfalls and known failures

* **Silicon:** TCA8418 supports up to 80 keys (10 COL × 8 ROW); 56 are wired, `ROW7`, `COL8`,
  `COL9` are explicit NCs.
* **Board:** `RESET` is strapped high through R38 and reaches **no GPIO**. A wedged scanner
  needs a power cycle. There is no software recovery path.
* **Board:** the scanner shares its bus with the ES8311 and BMI270; a driver that holds the
  bus during a long I²S/codec configuration will delay key events. Not observed to lose them —
  the TCA8418 has a 10-deep FIFO — but latency is real.
* **Framework:** `M5Cardputer` **1.1.1** is the first release with ADV support (added
  2025-08-29…09-02, `c331c7d`…`8ab9f43`). Anything older silently uses the GPIO-matrix reader
  on an ADV and reports no keys.
* **Framework:** without `eccba25` (2026-05-11) there is no fn layer, hence **no arrow keys**.
* **Community-reported:** *"The update today won't allow me to use directional arrows on adv
  anymore."* — u/Big-Bunch2804, r/CardPuter, **2026-08-29**, on the Plai Meshtastic client.
  Firsthand user report; arrow handling in third-party firmware is fragile.
* **Compatibility hazard:** M5GFX's ADV test is "are G8 and G9 pulled up". Anything that pulls
  those high on a **v1.x** makes it misdetect as an ADV and lose its keyboard. See
  [`../compatibility-and-status.md`](../compatibility-and-status.md).

## Debugging

1. Watch the boot log for `[Autodetect] board_M5CardputerADV`. Wrong board → wrong reader.
2. I²C-scan the internal bus (G8/G9). You should see exactly `0x18`, `0x34`, `0x69`.
   `geo-tp/M5-Card-Computer-I2C-Scanner` does this if you want it prebuilt.
3. Read `TCA8418_REG_INT_STAT`. The vendor's `update()` writes `1` to clear it and re-reads;
   if bit 0 stays set there are still queued events.
4. If `INT` never asserts, confirm `matrix(7, 8)` ran — the TCA8418 does not scan pins that are
   not enrolled in the matrix.

## Evidence status

| Claim | Status |
|---|---|
| Pin-by-pin TCA8418 wiring, series resistors, no-connects | **official** — rendered vendor schematic sheet 2 |
| `0x34` address | **official** (Adafruit default, Bruce build flag); not probed by this session |
| Remap arithmetic and its equivalence to the v1.x reader | **official** source + **derived**, arithmetic shown |
| S1 → `ROW0`/`Y7`, S2 → `ROW0`/`Y3` | **official** — read from a 1:1 sheet crop |
| Full per-switch net table for all 56 keys | **not established** — the rule is verified at the array corner and by the driver, but each of the other 54 switches was not individually traced |
| Any timing, latency or rollover number | **not tested** |
