# ZeroWriter Ink — software, shortcuts and Zerowriter Core

> The writing application: keyboard shortcuts, the Core 1.1 feature set, and the release timeline.
> Snapshot **2026-08-24**. Sources: `zerowriter.ink/blogs/news` articles (retrieved with the ClaudeBot UA — see the [vendor guide](../../../vendors/zerowriter/README.md)) and the firmware release notes in the GitHub repository.

The main application is **not published as source** ([`gaps-and-conflicts.md` §3a](gaps-and-conflicts.md)), so this document is assembled from vendor release notes and the user guide rather than from code.

## "Zerowriter Core" is the Ink's software, not just the Fold's

The [Zerowriter Fold](../zerowriter-fold/README.md) page describes Core as the platform "releasing as open source in the coming months", which left open whether it also covered the Ink. **It does.** The blog post *"Zerowriter Core 1.1 Update"* (2025-12-23) is explicitly an Ink update:

> Now that Zerowriter Ink is finally out in the wild, I am happy to announce the first major update to **Zerowriter Core**. This is a significant update and addresses a lot of shortcomings with the software that shipped on **every first batch Zerowriter Ink**. I recommend updating yours.

So Core is the shared application across both products. The open-source release remains **future tense** for both.

⚠ **Two independent version numbering schemes are in play** and they do not obviously reconcile:

| Scheme | Values seen | Where |
|---|---|---|
| **Core** | 1.1 (2025-12-23) | Blog |
| **SD firmware** | 1.24, 1.25, 1.27, 1.28, 1.3 | `firmware_releases/` + repo README ("current public firmware is 1.30") |

Whether "Core 1.1" corresponds to one of the SD releases, or numbers the platform separately, is **not stated**. Do not assume Core 1.1 < SD 1.24.

## Release timeline

| Date | Event |
|---|---|
| 2024-10-17 | Crowd Supply campaign funded (491 %, 585 backers) |
| 2025-09-02 | User Guide published |
| 2025-09-04 | Shortcut Keys Reference published |
| **2025-10-10** | **"Zerowriter Ink Is Shipping!"** — direct orders |
| 2025-12-23 | **Zerowriter Core 1.1** — first major update |
| **2026-01-17** | Crowd Supply: "First Shipments and Resources to Get Started" |
| 2026-02-09 | Crowd Supply: "Progress Report, New Improvements" |
| 2026-04-15 | Crowd Supply: "More Orders Fulfilled Plus a Pre-Launch Announcement" |
| 2026-05-21 | Crowd Supply: "Shipping Status and the Latest Developments" |
| 2026-05-30 | "In The News" — Fold press roundup |

Direct orders shipped in **October 2025**, roughly three months ahead of Crowd Supply backers (**January 2026**). Anyone reconciling the two channels' dates should expect that offset.

**First-batch units shipped with pre-1.1 software** that the developer describes as having "a lot of shortcomings". If you have an early unit, updating is strongly advised — see [`firmware-and-updates.md`](firmware-and-updates.md).

## Keyboard shortcuts

From *"Shortcut Keys Reference"* (2025-09-04).

### Navigation

| Shortcut | Action |
|---|---|
| `CTRL + LEFT/RIGHT` | Jump to start / end of line |
| `ALT + LEFT/RIGHT` | Jump between words |
| `CTRL+ALT+UP` | Go to start of document |
| `CTRL+ALT+DOWN` | Go to end of document |

### Editing

| Shortcut | Action |
|---|---|
| `CTRL+BACKSPACE` | Delete word |
| `ALT+BACKSPACE` | Delete forward (the "Delete" key a 60 % layout lacks) |
| `CTRL+ALT+BACKSPACE` | Delete word forward |
| `CTRL+C` / `CTRL+X` / `CTRL+V` | Copy / Cut / Paste |

### Files

| Shortcut | Action |
|---|---|
| `CTRL+S` | Save current file — **also "Save As"**: highlight a word and press `CTRL+S` to name the file that |
| `CTRL+N` | Save current file, open a new one |
| `CTRL+D` | Duplicate current file |
| `CTRL+F` | Force save to **failsafe** |
| `CTRL+B` | Bookmark menu (Editor Mode) |
| `CTRL+Q` | **Generate QR code** — the phone transfer path |

### Display and modes

| Shortcut | Action |
|---|---|
| `CTRL+R` | **Refresh e-paper screen** — clears accumulated ghosting |
| `CTRL+M` | Switch mode: Standard ↔ Draft |
| `CTRL+G` | Start a writing-goal session (type a number, highlight it, press) |
| `CTRL+L` | Sleep |

### Hotswap slots (Core 1.1)

| Shortcut | Action |
|---|---|
| `CTRL+ALT+(1–9)` | Assign current file to a hotswap slot |
| `CTRL+(1–9)` | Jump to that slot |

`ALT+BACKSPACE` for forward-delete is the notable one: a 60 % layout has no dedicated Delete key, and this is how it is recovered.

## Zerowriter Core 1.1 features (2025-12-23)

- **Simple Folders** — up to 9 folders labelled 1–9; press a number in the main menu to set the active folder.
- **Save As** — highlight a word, `CTRL+S`, and the file takes that name. Default remains automatic naming.
- **External `.txt` files** — any `.txt` dropped on the SD card is loaded and appears at the bottom of the file list. So the device reads files it did not create.
- **Full Screen** — disable the menu bar for an extra line of workspace.
- **Writing Session Mode** — type a number, highlight, `CTRL+G` to set a goal and track stats.
- **Hotswap Files** — 9 slots; **cursor position is remembered per file**, which makes editing and merging across files practical.

Bug fixes in 1.1, quoted because they indicate what was broken on first-batch units:

- "Fixed line spacing to actually adjust line spacing (oops)"
- Shift-selected text edit bugs
- Diacritical/deadkey system bugs
- Hotkey navigation (jump by word/line)
- Cursor-based navigation and movement
- "Tweaked the refresh speed settings and clarity for the display"

## USB file transfer

`utils/USB_Send.html` in the repository is a **WebSerial** page that receives files from the device.

| | |
|---|---|
| Baud | **115200** |
| Direction | **Device → host only.** You press "Send" on the Zerowriter; the current file arrives in the browser |
| Transport | USB via the CH340; **Bluetooth not supported** |
| Output | Plain text, with a "Copy to Clipboard" button |

An in-page note explains the baud choice:

> the UART baud rate must match the Zerowriter baud rate. **In v1.12+ of Zerowriter, the baud rate is temporarily set to 115200**, as it seems to be the most stable for USB / CH340 or for web serial from my testing.

Note this is **115200**, not the 921600 used on the [keyboard link](keyboard.md) — two different UARTs at different rates. The word "temporarily" suggests the developer intends to raise it later.

The other export path is `CTRL+Q`, which renders the document as a **QR code** for phone capture — no cable, no app.

## Format support

Markdown and Fountain renderers arrived in SD-1.28. From the developer's reply to a user asking for true bold/italic in a word-processor sense:

> Changing styles like bold and italic involve changing the underlying typeface… It would no longer work with plain TXT files (there needs to be some way to store the format change) so you would need to store bold, italic, possibly bold-italic fonts on the machine, and add codes to change them, and a format to support it, which in turn requires a parser…

That is an accurate statement of the constraint, and it explains the design choice: **Markdown/Fountain are rendered as interpreters over plain text**, with the active line always shown as raw text, rather than the device storing rich formatting.

**Arabic and other RTL scripts are not supported** and no commitment was made when a user asked (2026-05-10, unanswered in the thread). The [keymap format](keymap-format.md) is byte-oriented extended ASCII, so RTL would need considerably more than a keymap change.

## Related

- [`keymap-format.md`](keymap-format.md) — customising the layout
- [`firmware-and-updates.md`](firmware-and-updates.md) — how to apply updates
- [`keyboard.md`](keyboard.md) — the hardware behind these shortcuts
- [`README.md`](README.md)
