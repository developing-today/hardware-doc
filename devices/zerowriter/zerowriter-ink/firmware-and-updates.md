# ZeroWriter Ink — firmware, updates and recovery

> What ships, how to update it, and the one step that makes flashing fail if you skip it.
> Snapshot **2026-08-24**. Binaries parsed locally with [`tools/esp_image_info.py`](../../../tools/esp_image_info.py); procedures quoted from the vendor's own release notes and web updater page.

## ⚠ You must unplug the keyboard before flashing over USB

This is the single most important operational fact about this device, and it follows directly from the [dual-ESP32 architecture](keyboard.md).

> To update with this tool, you must open your Zerowriter Ink and **unplug the keyboard cable from the display board** (the cable on the left side of the screen). **The keyboard itself blocks the update signal from your computer**, so it must be disconnected temporarily.
> — <https://zerowriter.ink/pages/firmware-updates>

The command-line instructions say the same thing:

> This is because the **keyboard signal prevents the computer from sending the update data**. You need to unplug the keyboard cable that is attached to the left side of the display.

**Why:** the keyboard ESP32 transmits at **921600 baud into the main board's UART RX**, continuously and unsolicited. That is the same UART the CH340C bridge uses for flashing. The keyboard is effectively jamming the line. Because the keyboard's own RX is disabled (`Serial.begin(921600, SERIAL_8N1, -1, 1)`), nothing can tell it to be quiet — the only remedy is physical disconnection.

Procedure, from the vendor:

1. Turn off the Zerowriter Ink.
2. Unscrew the back panel.
3. Carefully unplug the keyboard cable on the left of the display (black cable, white connector) — wiggle side-to-side, do not pull straight.
4. Connect USB-C to the computer.
5. Turn the unit **on** via the power switch.
6. Run the updater.

## Update paths

### 1. SD card (normal)

> find the `firmware.bin` you want · place on SD card in root directory · insert SD card · turn on (or reboot) · automatically will install

The bootloader looks for `firmware.bin` in the SD root at startup. **This does not require opening the device** and is the intended route.

### 2. Web flasher (recovery)

<https://zerowriter.ink/pages/firmware-updates> — a browser-based flasher.

> Requires **Google Chrome** from a Desktop or Laptop computer (does not work on mobile). Use Chrome (Safari/Firefox won't work for USB flashing).

Uses WebSerial, hence the Chrome requirement. Intended for units where SD updating fails, or:

> It can be used if your Zerowriter Ink **does not have a Version number in the menu at the bottom**

That is a useful diagnostic: **no version number in the menu = firmware too old to self-update.** Web-flash first, then SD updates work thereafter.

> **This update tool does NOT affect anything on the SD card**, but you should always back up your work.

### 3. Command line (factory reset)

> Why use the command line tool? It is kind of like a **"Factory Reset"** that will rebuild your Zerowriter Ink. These files build a **new partition structure**… This means **you will lose your saved settings in the menu**.

```bash
esptool.py --chip esp32 -p /dev/cu.usbserial-10 write_flash 0x0000 zw_123.merged.bin
```

Replace the port (`ls /dev/tty.*` on macOS, `/dev/ttyUSB*` on Linux) and the filename. Install esptool with `python3 -m pip install --user esptool`.

Status: **`reported-working`** — quoted verbatim from `firmware_releases/command line/howto.txt`. Not executed here (no hardware).

Note the offset is **`0x0000`** and the image is a **merged** binary — it contains bootloader, partition table and application in one file, which is why it rebuilds the partition structure and wipes settings.

## Firmware images (parsed)

| Release | Size | Type | SHA-256 (first 16) |
|---|---:|---|---|
| **SD-1.3** (current public) | 1,256,992 | ESP app image | `849038d0eba05d5d` |
| SD-1.27 (archived) | 1,244,768 | ESP app image | — |
| SD-1.25 (archived) | 1,244,592 | ESP app image | — |
| SD-1.24 (archived) | 1,279,888 | ESP app image | `bb605889a10912e7` |
| `zw_latest.merged.bin` | **4,194,304** | merged full-flash | `a7d41dda2de8cc8e` |

Build metadata from the `esp_app_desc_t` of `SD-1.3/firmware.bin`:

| Field | Value |
|---|---|
| Chip ID | **0 = ESP32** (not S3/C3 — consistent with the ESP32-WROVER) |
| Flash config | **DIO, 4 MB, 80 MHz** |
| Segments | 6 |
| Entry point | `0x40082a0c` |
| Project | `arduino-lib-builder` |
| App version | `bb76cb1` |
| **Build date** | **`Mar 28 2025 06:14:09`** |
| **ESP-IDF version** | **`v5.4.1-1-g2f7dcd862a-dirty`** |
| ELF SHA-256 | `de9446c7a0d555ad…` |

Two observations:

- **The `esp_app_desc_t` build date is identical (`Mar 28 2025 06:14:09`) across SD-1.24 and SD-1.3**, despite different application content and different ELF hashes. That timestamp belongs to the **Arduino core** (`arduino-lib-builder` / IDF v5.4.1) baked into the image, not to the ZeroWriter application build. Do **not** use it to date a release — use the directory name and the changelog.
- The `-dirty` suffix on the IDF version means the core was built from a modified working tree. Normal for Arduino core builds; noted for completeness.

The merged image is exactly **4,194,304 bytes = 4 MB**, matching the `ESP32-WROOM-32U-N4`/WROVER 4 MB flash and the `flash size=4MB` header field.

## Changelog (from `SD-1.3/readme.txt`)

### 1.3
- **Arrow keys remappable** in `keymap.json` — "they are the last 4 keys in the keymapnormal array" (indices 57–60, matching the [keyboard matrix](keyboard.md#matrix-and-pin-map))
- Bookmarks mode redesigned
- Fixed umlauts not working in dead keys
- Added markdown escape character `\` (type `\*` for a literal asterisk)
- Cleaned up markdown and Fountain formatting
- Increased the time window for passcode entry

### 1.28
- Fixed the editor adding extra spaces to sentences when reopening existing files
- **Added Markdown and Fountain modes** — bold, italics, etc. Explicitly framed as "demonstration for the kinds of extensions we can build". Renderers act as interpreters over the plain file; the **active line always renders as plain text**; both operate at **80 % width** to avoid overflow. [Fountain](https://fountain.io/syntax/) is a screenwriting format.
- Added "Reset Persistent Settings" for settings that fail to save
- Added an optional **lock code** on wake (`CTRL+L` or timer) — "not meant for security, but for preventing accidental input"
- Added "Are you sure?" confirmations for destructive actions

The Markdown/Fountain support is the most interesting entry: it makes the device useful for screenwriters, and the vendor is explicitly signposting the extension mechanism for community renderers.

## Known keyboard shortcut

`CTRL+L` puts the device to sleep.

## Resolved / still open

**Resolved by this analysis:**
- The main-board target is a plain **ESP32** (chip ID 0) with **4 MB** flash.
- Why flashing requires opening the case — the keyboard jams the UART.
- What "factory reset" means — a merged image rewriting the partition table, losing settings.
- What the version-number-missing symptom indicates.

**Still open:**
- The **factory-shipped firmware version** is still not stated. The repo README warns factory units may be older than 1.30, and the `firmware_releases/` directory tops out at **1.3** — note "1.30" in the README and "1.3" in the directory name are probably the same release, but this is not confirmed.
- Changelogs for 1.24–1.27 were not shipped in the archived directories.
- The main-board application source is **not in the repository** — only compiled `.bin` files. The keyboard source *is* published. So the writing application itself is, in practice, **not open source** despite the project's positioning, unless it is published elsewhere.

That last point is worth flagging clearly: the campaign says "Our source code will all be published on GitHub", and the hardware design files and keyboard firmware are indeed there. The **main application firmware is binary-only** in this snapshot.

## Related

- [`README.md`](README.md) — device overview
- [`keyboard.md`](keyboard.md) — why the keyboard blocks flashing
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
