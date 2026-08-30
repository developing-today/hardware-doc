# ZeroWriter Ink — keyboard subsystem

> The second ESP32: how the keyboard works, the wire protocol to the main board, and its pin map.
> Snapshot **2026-08-24**. Everything here is derived from **primary source** — `src/keyboard/zwi_kb_feb2026/zwi_kb_feb2026.ino` (GPL-3.0, © 2025 The Zerowriter Company, 277 lines) and the `Zerowriter Keyboard` KiCad BOM, both in the project repository.

This document closes the open question recorded in [`gaps-and-conflicts.md` §2](gaps-and-conflicts.md#2-the-dual-esp32-architecture--resolved).

## Summary

The keyboard is a **standalone ESP32-WROOM-32U-N4** running its own Arduino firmware. It scans a 5 × 14 matrix locally, sleeps between keystrokes, and sends **one raw byte per key event over a one-way 921600 baud UART** to the main board. The main board owns the keymap; the keyboard has no notion of what any key means.

The author's own comment is worth quoting, because it is unusually candid:

> Architecture improvements we could make:
> - every key could send key down / key up signals instead of just mod keys (which would make full-keyboard mapping doable)
> - **we should move away from esp32 to a STM chip, or a cheaper/lower power alternative** — just need something that offers sleep, low power, serial output

So the choice of an ESP32 for the keyboard is acknowledged by the developer as over-specified. That answers the "why an ESP32 here?" question directly: it is not an architectural requirement, it is convenience.

## Wire protocol

**One byte per event, transmit-only.**

| Setting | Value |
|---|---|
| Baud | **921600** |
| Framing | `SERIAL_8N1` |
| TX pin | **GPIO 1** |
| RX pin | **`-1` — disabled** |

```c
Serial.begin(921600, SERIAL_8N1, -1, 1);
```

The comment explains the choice:

> keyboard operates at **921600 baud**, which is stable […] **RX serial receiving pin is inactive (-1) as this keyboard only sends signal.**

**This is a unidirectional link.** The main board cannot talk back — no LED control, no configuration push, no handshake, no flow control. Any future feature requiring main→keyboard communication needs a firmware change on both sides.

### Byte encoding

| Byte range | Meaning |
|---|---|
| **0–60** | Key index. `0` = top-left (`` ` ``), `60` = bottom-right (Right Arrow) |
| **240** | `MOD_SHIFT_DOWN` |
| **241** | `MOD_SHIFT_UP` |
| **242** | `MOD_CTRL_DOWN` |
| **243** | `MOD_CTRL_UP` |
| **244** | `MOD_ALT_DOWN` |
| **245** | `MOD_ALT_UP` |
| **246** | `MOD_META_DOWN` |
| **247** | `MOD_META_UP` |
| **255** | Sentinel in the matrix table — "no key at this position". Not transmitted |

The asymmetry is the important detail: **modifiers send both down and up events; ordinary keys send only a single byte on press.** There is no key-release event for normal keys. This is precisely the limitation the author flags — it is why full N-key remapping is not currently possible, and why key-repeat has to be synthesised on the keyboard side rather than by the host.

Keymap translation happens **on the main board**, against the user's `keymap.json`. The repository ships an editor for it: [`utils/Ink_Keymap_Editor.html`](artifacts/source-snapshots/zerowriter_ink/utils/Ink_Keymap_Editor.html).

## Matrix and pin map

**5 rows × 14 columns**, 61 keys populated (61 × `1N4148W` diodes in the BOM confirms one diode per key).

```c
const uint8_t rowPins[ROWS] = { 13, 12, 27, 26, 14 };
const uint8_t colPins[COLS] = { 19, 21, 23, 22, 2, 15, 4, 16, 17, 5, 18, 25, 33, 32 };
```

| | GPIO |
|---|---|
| Rows (5) | 13, 12, 27, 26, 14 |
| Columns (14) | 19, 21, 23, 22, 2, 15, 4, 16, 17, 5, 18, 25, 33, 32 |
| UART TX | 1 |

Key index layout (`255` = unpopulated position):

```
row 0:   0   1   2   3   4   5   6   7   8   9  10  11  12  13
row 1:  14  15  16  17  18  19  20  21  22  23  24  25  26  27
row 2:  28  29  30  31  32  33  34  35  36  37  38  39  40   -
row 3:  41  42  43  44  45  46  47  48  49  50  51  52   -   -
row 4:  53   -  54   -  55   -  56   -   -   -  57  58  59  60
```

Special indices:

| Index | Key |
|---|---|
| 28 | Caps Lock |
| 41, 52 | Shift (left, right) |
| 53 | Ctrl |
| 54 | Alt |
| 55 | Meta |
| 57, 58, 59, 60 | Left, Up, Right, Down arrows |

Row 4 is the sparse modifier/space row — matrix positions (4,6) is Space, and (4,10)–(4,13) are the arrow keys, which matches the campaign's "optional arrow keys to replace bottom right modifier keys".

## Power management

This is the part that makes the ~100 hour battery claim plausible.

```c
setCpuFrequencyMhz(80);            // down from 240 MHz
esp_wifi_deinit();
esp_bt_controller_disable();
esp_bt_controller_deinit();
esp_bt_controller_mem_release(ESP_BT_MODE_CLASSIC_BT);
esp_bt_controller_mem_release(ESP_BT_MODE_BLE);
```

Then, after **200 ms idle**, it enters **light sleep** with the column pins as level-triggered wake sources:

```c
for (...) gpio_wakeup_enable((gpio_num_t)colPins[i], GPIO_INTR_LOW_LEVEL);
esp_sleep_enable_gpio_wakeup();
esp_light_sleep_start();
```

Notes:

- **Wi-Fi and Bluetooth are torn down and their memory released** at boot. This is not merely "disabled in software" — the controller memory is returned to the heap, so re-enabling radio on the keyboard is a non-trivial firmware change. It corroborates the campaign's claim that wireless is genuinely off, and reinforces the oddity of the **`U` (external-antenna) module variant** being chosen.
- **CPU is clocked at 80 MHz**, a third of the ESP32's maximum.
- Any column going low wakes it, so latency is a single scan cycle — the comment claims it operates "fairly low power without much latency when waking up".

## Timing / feel constants

| Constant | Value | Effect |
|---|---|---|
| `initialRepeatDelay` | **470 ms** | Before a held key starts repeating |
| `repeatTimer` | **75 ms** | Between repeats (~13 chars/s) |
| `sleepDelay` | **200 ms** | Idle before light sleep |
| `debounceTime` | **10 ms** | Matrix debounce |

These are the knobs to change if the typing feel is wrong — they are plain constants at the top of the file.

## Programming the keyboard

From the firmware header comment:

> Compile for: **ESP32-WROOM-DA Module** (or similar)
>
> Note that the ZW keyboard has **programming pins at the bottom** — you can program it using a **USB-UART adapter** or similar, or via another MCU. You will need to **trigger it into bootloader mode via the boot/reset buttons**.

This matches the BOM: `K2 = NOVA_programmer_header` (6-pin) and `RST1`/`RST2` tactile switches (`TS5215A`, 250 gf).

So the keyboard **is** user-reflashable, but requires an external USB-UART adapter — the product's USB-C port goes to the main board, not the keyboard. Note the recommended Arduino target (`ESP32-WROOM-DA`) does not match the fitted part (`ESP32-WROOM-32U-N4`); "or similar" is doing work there, and the DA target is a dual-antenna variant. Not obviously harmful, since the firmware disables radio entirely.

## Panic signal

There is a vestigial "panic" feature that disables output entirely, keyed on the Space position (`SPACE_R=4, SPACE_C=6`). The author notes:

> it could be removed, as there isn't much need for it anymore

Mentioned only so nobody mistakes it for something load-bearing.

## Remaining unknowns

- **Whether an antenna is fitted** to the WROOM-32U. Radio is torn down in firmware regardless.
- **Which pins on the 6-pin `HC-1.25-6PWT`** carry TX, power and ground — the connector pinout was not traced from the keyboard schematic.
- **Whether the shipped keyboard firmware matches this file.** `zwi_kb_feb2026` is dated Feb 2026; the repo README warns factory units may run older firmware.
- **The main-board side of the protocol** — the decoder that maps bytes 0–60 through `keymap.json` — was not read.

## Related

- [`README.md`](README.md) — device overview and the dual-ESP32 architecture
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
- [ESP32-WROOM-32U component record](../../../components/espressif/esp32-wroom-32u/README.md)
