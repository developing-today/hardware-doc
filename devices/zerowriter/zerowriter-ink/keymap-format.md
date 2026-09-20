# ZeroWriter Ink — keymap format

> How `keymap.json` works, the complete default US layout, and a conflict between the firmware and the keymap over arrow-key order.
> Snapshot **2026-08-24**. Derived from `utils/keymaps/keymap.json` and `src/keyboard/zwi_kb_feb2026/zwi_kb_feb2026.ino` in the project repository.

## How it fits together

The [keyboard ESP32](keyboard.md) sends **a raw key index (0–60)** over UART. It has no idea what any key means. The main board looks that index up in `keymap.json` and produces a character.

**This means the entire layout is user-editable without touching firmware** — change a JSON file on the SD card and the layout changes. It is the mechanism behind the campaign's claim of support for "most western languages… uses extended ASCII 256 chars".

An in-repo editor is provided: [`utils/Ink_Keymap_Editor.html`](artifacts/source-snapshots/zerowriter_ink/utils/Ink_Keymap_Editor.html) (a standalone HTML page, no install).

## File structure

Eight parallel arrays, **each exactly 61 entries** — one per key index:

```json
{
  "keymapNormal":    ["`", "1", "2", …],
  "keymapShift":     ["~", "!", "@", …],
  "keymapAlt":       ["", "", "", …],
  "keymapShiftAlt":  ["", "", "", …],
  "keymapMeta":      ["", "", "", …],
  "keymapShiftMeta": ["", "", "", …],
  "keymapCtrl":      ["", "", "", …],
  "keymapShiftCtrl": ["", "", "", …]
}
```

| Layer | Modifier combination | Populated by default? |
|---|---|---|
| `keymapNormal` | none | ✅ full US QWERTY |
| `keymapShift` | Shift | ✅ full |
| `keymapAlt` | Alt | ❌ **all 61 empty** |
| `keymapShiftAlt` | Shift+Alt | ❌ all empty |
| `keymapMeta` | Meta | ❌ all empty |
| `keymapShiftMeta` | Shift+Meta | ❌ all empty |
| `keymapCtrl` | Ctrl | ❌ all empty |
| `keymapShiftCtrl` | Shift+Ctrl | ❌ all empty |

**Six of the eight layers ship completely empty.** That is where accented characters, symbols and non-US layouts go — the mechanism exists and is simply unused by the default US map. If you want `é` on Alt+E, you populate `keymapAlt[17]`.

The array length of **61 matches the 61 populated matrix positions** in the keyboard firmware exactly, and the index ordering is the same `keyIndexMap` table.

## Default US layout (all 61 indices)

`·` = empty string (modifier or unmapped). Control characters shown as escapes.

| # | Normal | Shift | | # | Normal | Shift | | # | Normal | Shift |
|---:|---|---|---|---:|---|---|---|---:|---|---|
| 0 | `` ` `` | `~` | | 21 | `u` | `U` | | 42 | `z` | `Z` |
| 1 | `1` | `!` | | 22 | `i` | `I` | | 43 | `x` | `X` |
| 2 | `2` | `@` | | 23 | `o` | `O` | | 44 | `c` | `C` |
| 3 | `3` | `#` | | 24 | `p` | `P` | | 45 | `v` | `V` |
| 4 | `4` | `$` | | 25 | `[` | `{` | | 46 | `b` | `B` |
| 5 | `5` | `%` | | 26 | `]` | `}` | | 47 | `n` | `N` |
| 6 | `6` | `^` | | 27 | `\` | `\|` | | 48 | `m` | `M` |
| 7 | `7` | `&` | | **28** | · | · | **Caps Lock** | 49 | `,` | `<` |
| 8 | `8` | `*` | | 29 | `a` | `A` | | 50 | `.` | `>` |
| 9 | `9` | `(` | | 30 | `s` | `S` | | 51 | `/` | `?` |
| 10 | `0` | `)` | | 31 | `d` | `D` | | **52** | · | · | **Shift (R)** |
| 11 | `-` | `_` | | 32 | `f` | `F` | | **53** | · | · | **Ctrl** |
| 12 | `=` | `+` | | 33 | `g` | `G` | | **54** | · | · | **Alt** |
| **13** | `\x08` | `\x08` | **Backspace** | 34 | `h` | `H` | | **55** | · | · | **Meta** |
| **14** | `\t` | `\t` | **Tab** | 35 | `j` | `J` | | **56** | `' '` | `' '` | **Space** |
| 15 | `q` | `Q` | | 36 | `k` | `K` | | **57** | `LEFT` | · | arrow |
| 16 | `w` | `W` | | 37 | `l` | `L` | | **58** | `UP` | · | arrow |
| 17 | `e` | `E` | | 38 | `;` | `:` | | **59** | `DOWN` | · | arrow |
| 18 | `r` | `R` | | 39 | `'` | `"` | | **60** | `RIGHT` | · | arrow |
| 19 | `t` | `T` | | **40** | `\r` | `\r` | **Enter** | | | |
| 20 | `y` | `Y` | | **41** | · | · | **Shift (L)** | | | |

Three encoding conventions worth noting:

- **Control keys are literal control characters**, not names: Backspace is `\x08`, Tab is `\t`, Enter is `\r` (carriage return, not `\n`).
- **Arrow keys are magic strings** — the literal words `LEFT`, `UP`, `DOWN`, `RIGHT` — not characters. So the format supports named actions alongside literal text.
- **Modifier positions map to empty strings.** Shift/Ctrl/Alt/Meta/Caps are handled by the [dedicated modifier byte protocol](keyboard.md#byte-encoding) (240–247), not through the keymap.

Since entries are *strings*, not single characters, a key can almost certainly emit **multi-character text** — a macro. Not confirmed against the main-board decoder (which is not published), so treat as probable rather than certain.

## ⚠ Conflict: firmware and keymap disagree on arrow order

The 1.3 changelog says:

> can remap UP,DOWN,LEFT,RIGHT keys in `keymap.json` file … **they are the last 4 keys in the keymapnormal array**

The last four entries are indices 57–60. But the two published sources disagree about which is which:

| Index | **Keyboard firmware** (`zwi_kb_feb2026.ino`) | **`keymap.json`** |
|---:|---|---|
| 57 | `LEFT` (`LEFT_C = 10`) | `LEFT` ✅ |
| 58 | `UP` (`UP_C = 11`) | `UP` ✅ |
| 59 | **`RIGHT`** (`RIGHT_C = 12`) | **`DOWN`** ❌ |
| 60 | **`DOWN`** (`DOWN_C = 13`) | **`RIGHT`** ❌ |

The firmware's matrix constants are:

```c
constexpr uint8_t LEFT_R  = 4, LEFT_C  = 10;   // → keyIndexMap[4][10] = 57
constexpr uint8_t UP_R    = 4, UP_C    = 11;   // → 58
constexpr uint8_t RIGHT_R = 4, RIGHT_C = 12;   // → 59
constexpr uint8_t DOWN_R  = 4, DOWN_C  = 13;   // → 60
```

while `keymap.json` has `[…, "LEFT", "UP", "DOWN", "RIGHT"]` at 57–60.

> ✅ **RESOLVED 2026-08-24.** The developer states on Reddit: *"The last 4 entries on the first keymap layer determine the arrow key layout."* **The keymap is authoritative**; the firmware constants are not used for key identity — reading (1) below is correct. Arrow remapping requires firmware **≥ 1.30**, and the **online keymap editor greys the arrows out**, so edit the JSON directly. See [`community-and-ecosystem.md`](community-and-ecosystem.md#the-arrow-key-conflict--resolved-by-the-developer).

**Two readings were possible before that confirmation:**

1. The firmware constants are used **only** for the vestigial "panic" chord (they appear nowhere else — see [`keyboard.md`](keyboard.md#panic-signal)), so their naming may simply be wrong without affecting anything. The keymap would then be correct.
2. The physical bottom-right key order really is Left/Up/Right/Down and the shipped keymap has Down and Right transposed — in which case those two keys are swapped out of the box.

Reading (1) is more likely, because a transposed arrow key is the kind of bug users report immediately. But it is worth a 30-second check on hardware.

**If your Down and Right arrows are swapped, this is why** — edit `keymap.json` and exchange indices 59 and 60.

> Evidence status: both sources read directly and quoted. The conflict is **firsthand and reproducible from the repository**. Which one matches physical hardware is **untested** — no unit available.

## Editing

1. Mount the microSD card.
2. Edit `keymap.json` (or use `utils/Ink_Keymap_Editor.html` in a browser and export).
3. Replace the file on the card.

Since the keymap lives on the SD card alongside your documents, it survives firmware updates — the SD-card updater explicitly does not touch your files, and the vendor's web flasher states it "does NOT affect anything on the Zerowriter Ink SD card".

Populating the empty modifier layers is the intended route to non-US layouts. The campaign's claim of "support for most western languages… extended ASCII 256 chars" is a claim about *this file format*, not about shipped layouts — only US English is provided.

## Related

- [`keyboard.md`](keyboard.md) — the key-index protocol these arrays are indexed by
- [`firmware-and-updates.md`](firmware-and-updates.md) — the 1.3 changelog entry
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
- [`README.md`](README.md)
