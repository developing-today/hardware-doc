# Xteink X4 — development

> ESP32-C3. Retrieval **2026-09-04**. **Nothing executed against hardware.**

## Toolchain

| Item | Value | Status |
|---|---|---|
| Framework | Arduino-ESP32 under PlatformIO | `reported-working` |
| Build flag | `-DFREEINK_DEVICE_X4=1` | `reported-working` **[SDK]** |
| SDK | [FreeInk SDK](https://github.com/Free-Ink/freeink-sdk), git submodule | `reported-working` |
| Optional | `-DFREEINK_X4_OVERCLOCK_SPI` → 40 MHz panel clock, **out of spec** | `reported-working`, opt-in |
| esptool chip | `esp32c3` | `inferred` |
| Stock toolchain | **Arduino core, ESP-IDF 4.4.7** | **[DUMP]** app descriptor |

`-DFREEINK_DEVICE_X4=1` links both the SSD1677 driver and the UltraChip
siblings, and enables the C3 `XteinkDetect` I²C fingerprint.

**No PSRAM.** Memory pressure is real on this device: CrossPoint moved off GitHub
releases because OTA caused *"out of memory issues on the x3"*, the same SoC.

## Build / flash / monitor

```bash
pio run -e x4                # inferred
pio run -e x4 -t upload      # inferred
pio device monitor -b 115200 # inferred
```

## USB lock

Many units **ship with USB flashing disabled**. Identical situation to the
[X4 Pro](../x4-pro/development.md#usb-lock):

| Path | Status |
|---|---|
| `crosspointreader.com` OTA unlock | `reported-working` — [r/xteinkereader `1tl3gnn`](https://old.reddit.com/r/xteinkereader/comments/1tl3gnn/) |
| SD-card install: `update.bin` on card root, **hold Power + Up at boot** | `reported-working` — [r/XTEINK `1ult9dy`](https://old.reddit.com/r/XTEINK/comments/1ult9dy/). Author warns the combo is unverified per unit |
| Buy the vendor's **developer-unlocked** variant | `reported-working` — [r/xteinkereader `1uan67g`](https://old.reddit.com/r/xteinkereader/comments/1uan67g/) |
| [`OvermindDL1/xteink-unlocker`](https://github.com/OvermindDL1/xteink-unlocker) | Tauri/Rust desktop unlocker, not inspected |

Community firmware authors shout about it: *"If you have an unlocked X4
(!!!UNLOCKED!!!)"* — [r/XTEINK `1tqbcgu`](https://old.reddit.com/r/XTEINK/comments/1tqbcgu/), 514 pts.

There is a documented dual-boot workflow for locked units:
[`lvturner/x4-dual-boot`](https://github.com/lvturner/x4-dual-boot) —
*"MicroSlate + CrossInk dual-boot for a USB-locked Xteink X4 (SD-card install)"*.

## Bricking risks

| Risk | Note |
|---|---|
| **Not asserting the GPIO13 latch** | On the non-self-latching board revision the device only stays on while the button is held. Always assert it |
| **Driving GPIO13 LOW unintentionally** | That is the battery power-off |
| **40 MHz panel overclock** | 2× datasheet. *"can glitch plane writes on marginal wiring"* — validate per unit |
| **Wrong panel driver on a newer batch** | UC8179/UC8279 units need the boot probe |
| **Stale fork on a locked unit** | CrossPoint 1.5: *"Other forks will need to pull the latest SDK to avoid soft bricking locked units"* |
| **OTA failure at `esp_ota_end()`** | A real, named brick on CrossPoint 1.2.0 with a published escape recipe ([`togotago/xteink-x4-escape`](https://github.com/togotago/xteink-x4-escape)) |
| **Out-of-memory during OTA** | No PSRAM; documented on the sibling C3 |

## Debug access

ESP32-C3 **USB-serial-JTAG** over the USB-C port. No exposed header documented; no
teardown of this device exists to check for pads. The X3 teardowns show the same
board family and no obvious debug header was captioned.

## The best starting points

| Project | Why |
|---|---|
| [CrossPoint Reader](https://github.com/crosspoint-reader/crosspoint-reader) | Upstream; the X4 is its original target |
| [`ngxson/pluspoint-reader`](https://github.com/ngxson/pluspoint-reader) | *"Yet another alternative firmware for Xteink X4"* |
| [`CidVonHighwind/microreader`](https://github.com/CidVonHighwind/microreader) | Independent, GPLv2, actively discussed |
| [`Jon-Vii/marigold-os`](https://github.com/Jon-Vii/marigold-os) | **Rust** firmware for X4 and X3 |
| [`HookedBehemoth/TrustyReader`](https://github.com/HookedBehemoth/TrustyReader) | Rust, GPL-2.0 |
| [`adafruit/Adafruit_CircuitPython_Xteink_X4`](https://github.com/adafruit/Adafruit_CircuitPython_Xteink_X4) | **Adafruit** published a CircuitPython helper — a notable third-party endorsement |

Rust appears at least four times (`marigold-os`, `TrustyReader`,
`aimindseye/rustmix-x4-firmware`, `h0rv/rust-xteink-x4`, `h0rv/slint-xteink-backend`),
which is unusual for an ESP32-C3 consumer device and reflects the RISC-V core.

## Related

[`factory-firmware.md`](factory-firmware.md) · [`pinouts-and-buses.md`](pinouts-and-buses.md) ·
[family command ledger](../x4-pro/commands.md)
