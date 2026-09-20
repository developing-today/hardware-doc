# Keyboard — TCA8418 QWERTY matrix, backlight and hotkeys

**Question:** *How do I read the physical keyboard, remap the F-keys, and control the backlight?*

| | |
|---|---|
| Scanner | [TI TCA8418](../../../../components/texas-instruments/tca8418/README.md) |
| Bus / address | I²C4 (`GPIO46` SCL / `GPIO47` SDA), **`0x34`** |
| RESET / IRQ | `GPIO43` / `GPIO42` |
| Matrix | **7 ROW × 10 COL** configured; 6 × 11 displayed layout |
| Backlight | **`GPIO52` / PWM4** |
| Expander | [XL9555](../../../../components/xlsemi/xl9555/README.md), address **probed** in `0x20`–`0x27` |
| Where | **nRF9151 keyboard base board** (kit SKUs `K256-04`, `K256-04-A`) — *not* on the bare board |
| Evidence | `reported-working` |

## The full key map

Every key code, its label, and the physical layout are decoded in
[`pinouts-and-buses.md` §8](../pinouts-and-buses.md#8-keyboard-matrix--full-decode). The things
that will surprise you:

- **Two `SPACE` codes** (`5` and `14`) — one wide bar across two intersections.
- **Two `FN` keys** — `9` (left) and `3` (`FN-R`, right); either satisfies `FN`.
- A dedicated **`LILYGO`** key (code `8`) and a dedicated **`MIC`** key (code `11`).
- Arrows are scattered along the bottom two rows, not clustered: `UP` 22, `DOWN` 12, `LEFT` 2,
  `RIGHT` 1.
- **11 F-keys.**

Code → matrix position: `row = (code-1)/10`, `col = (code-1)%10`.

## Reading it

The image ships `evtest`; the scanner appears as a Linux input device. In the launcher, keys are
read through `ui_hardware.c`, which talks to the TCA8418 over I²C directly and maintains its own
`keyboard_key_pressed[row][col]` state under a mutex.

Registers used: `CFG 0x01`, `INT_STAT 0x02`, `KEY_LCK_EC 0x03`, `KEY_EVENT_A 0x04`,
`KP_GPIO_1/2/3 0x1D/0x1E/0x1F`, `DEBOUNCE_DIS_1/2/3 0x29/0x2A/0x2B`. Config mode with IRQ
(`K230_TCA8418_USE_IRQ 1`, default) is `KE_IEN | OVR_FLOW_IEN | OVR_FLOW_M`; without IRQ it is
`OVR_FLOW_M` and the driver polls.

**Repeat timing:** first repeat at **450 ms**, then every **85 ms**.

## The IOMUX detail worth knowing

The launcher **writes the K230 IOMUX register for `GPIO42` directly** —
`TCA8418_IRQ_IOMUX_IO42_OFFSET = 42*4`, value `0x00000344` — to force GPIO-input mode. That is
userspace reaching past the kernel pin controller. If another driver later claims and re-muxes
`GPIO42`, the keyboard IRQ silently stops and the scanner falls back to nothing. If you see keys
stop working after loading an unrelated driver, this is why.

## Hotkeys and remapping

- Preference keys `keyboard.hotkey.f1` … `keyboard.hotkey.f11`.
- **v0.2.4 defaults:** `F3` / `F4` = keyboard backlight down / up, `F7` = screenshot.
- `FN+B` toggles the backlight.
- `keyboard.esc_back` (default on) makes `ESC` act as Back.
- Hotkey activity is logged to `/tmp/k230_keyboard_hotkey.log`; an on-screen OSD shows for
  ~950 ms with a 160 ms fade.

## Backlight

`GPIO52` on **PWM4**, driven from userspace. The reference pin configuration leaves `IO52` as
**input with pull-down until userspace enables PWM4** — a deliberate safe default, and the reason
the backlight is dark before the launcher starts.

⚠ **This is the keyboard backlight, not the display backlight.** The AMOLED's brightness is a DSI
command ([display.md](display.md)).

## Auto-detection

The keyboard base is optional and detected: `EXT_KEY_AUTO_DETECT_DEFAULT 1`, probe interval
default **3 s** (range 3–30 s), `EXT_KEY_FAIL_LIMIT 5` consecutive failures before giving up.
Queues: `EXT_KEY_QUEUE_SIZE 64`, `TCA8418_RAW_QUEUE_SIZE 96`.

## Limits

- **7 × 10 = 70 possible codes**; ~60 keys are named. Code `0` is not a key.
- The TCA8418 supports up to 8 × 10; this board uses 7 rows.
- Rollover behaviour: unstated. The launcher tracks a full pressed-state matrix, so multi-key
  detection works at the software level.
- `tca8414` appears twice in the tree — a probable typo, or fallback support. Unverified.

## Pitfalls

1. **The keyboard is a separate purchase.** No keyboard on `K256*` bare boards.
2. Don't hard-code the XL9555 address; the software probes `0x20`–`0x27`.
3. The keyboard shares I²C4 with the charger and gauge — a stuck bus takes out power management
   too ([`resources-and-conflicts.md`](../resources-and-conflicts.md)).
4. The keyboard base does **not** include a case for the main board (confirmed by an owner,
   2026-08-13).
