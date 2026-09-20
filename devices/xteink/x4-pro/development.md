# Xteink X4 Pro — development

> Retrieval date **2026-09-04**. **No command in this document was executed
> against an X4 Pro by this session — no hardware was available.** Every entry is
> labelled `reported-working`, `inferred` or `not-tested`. Nothing here is
> `executed-success`.

## Toolchain and framework

| Item | Value | Status |
|---|---|---|
| Framework | Arduino-ESP32 under **PlatformIO** | `reported-working` |
| PlatformIO board | `esp32-s3-devkitc1-n16r8` — 16 MB flash + 8 MB PSRAM | `reported-working` **[SDK]** `platformio.sample.ini` |
| MCU override | `board_build.mcu = esp32s3` | `reported-working` |
| SDK | [FreeInk SDK](https://github.com/Free-Ink/freeink-sdk), consumed as a **git submodule** | `reported-working` |
| Stock firmware toolchain | **ESP-IDF 6.0.1** (native, not Arduino) for 7.4.4 | **[DOC]** app descriptor |

There is **no official vendor SDK, no vendor board-support package and no vendor
documentation of any kind.** Every development path is community-built.

## Required build flags

```ini
[env:x4pro]
extends = base
board = esp32-s3-devkitc1-n16r8   ; 16 MB flash + 8 MB PSRAM (matches the X4 Pro dump)
board_build.mcu = esp32s3
build_flags =
  ${base.build_flags}
  -DBOARD_HAS_PSRAM
  -DFREEINK_DEVICE_X4PRO=1
```

Verbatim from `platformio.sample.ini` at commit `2400379`. `reported-working`.

`-DFREEINK_DEVICE_X4PRO=1` auto-enables `FREEINK_DRIVER_SSD1677`,
`FREEINK_DRIVER_UC8179`, `FREEINK_CAP_TOUCH` and `FREEINK_CAP_FRONTLIGHT`.

**The SD path additionally needs `USE_BLOCK_DEVICE_INTERFACE=1` in the *consumer*
build** — the `x4pro` env defines it; a hand-rolled env that forgets it will
compile and then fail to mount the card. `reported-working` **[DOC]** line 16.

## Build, flash, monitor

```bash
# not-tested by this session; the standard PlatformIO triple
pio run -e x4pro
pio run -e x4pro -t upload
pio device monitor -b 115200
```

`inferred` — these are generic PlatformIO invocations, not quoted from any
Xteink-specific source. The upload path depends entirely on whether the unit is
**USB-locked** (below).

## USB lock

**This is the single most important thing to know before buying or flashing.**

Many X4 Pro units — and X3/X4 units — **ship from the factory with USB flashing
disabled**. `esptool` cannot see them. The community calls these "USB-locked"
or "locked" units.

| Path | What it does | Status |
|---|---|---|
| **CrossPointReader.com web flasher** | *"OTA Unlock usb locked stock devices by flashing CrossPoint and CrossInk"* | `reported-working` — [r/xteinkereader `1tl3gnn`](https://old.reddit.com/r/xteinkereader/comments/1tl3gnn/), 2026-05-23, 346 pts |
| **SD-card update** | Drop `update.bin` on the SD root, hold **Power + Up** at boot; the **stock bootloader** picks it up and flashes it. No cable, no unlock | `reported-working` — [r/XTEINK `1ult9dy`](https://old.reddit.com/r/XTEINK/comments/1ult9dy/), 2026-07-02 |
| **Developer-unlocked units** | Xteink sells an explicitly unlocked variant through CrossPoint's affiliate link | `reported-working` — [r/xteinkereader `1uan67g`](https://old.reddit.com/r/xteinkereader/comments/1uan67g/), 2026-06-20 |

The SD path's author is candid about its risk: *"that path relies on
stock-bootloader behavior I don't control, so confirm the button combo for your
unit first."* Treat the button combination as **unverified per unit**.

`OvermindDL1/xteink-unlocker` is a Tauri/Rust desktop application implementing the
unlock; it carries a `com.sofriendly.crosspoint.unlocker.helper` privileged helper
on macOS. Not inspected in depth this session.

## Bricking risks

| Risk | Mechanism | Mitigation |
|---|---|---|
| **Flashing a C3 image onto the S3** | Upstream CrossPoint release URLs point at C3 builds. CrossPlay had to repoint `OtaUpdater.cpp` specifically to avoid this | Verify the artifact names the S3 / `x4pro` |
| **Wrong panel driver** | Newer batches carry UC8179/UC8279, not SSD1677. A firmware without those drivers leaves a blank screen | Use a firmware carrying all three; the boot probe selects |
| **Stale fork on locked hardware** | CrossPoint 1.5 release notes: *"Other forks will need to pull the latest SDK to avoid **soft bricking locked units**"* — [r/xteinkereader `1vhvtdd`](https://old.reddit.com/r/xteinkereader/comments/1vhvtdd/), 2026-08-07 | Prefer forks synced to current SDK |
| **OTA out-of-memory** | Reported on the X3; CrossPoint moved off GitHub releases because of it | Not X4 Pro-specific but the same OTA path |
| **Probing GPIO19/20** | Native USB D−/D+. The C3 detect fingerprint pokes SDA20/SCL0, which here is D+ and a boot strap | `XteinkDetect` compiles that path out unless a C3 profile is in the build |
| **Holding GPIO0 at reset** | It is the Left button *and* the boot strap | Do not power on with Left held unless you want download mode |

**Being behind upstream is a brick-risk signal in this ecosystem, not a tidiness
one** — the vendor revises hardware silently and upstream carries the fixes.

## Debug access

- **USB CDC** over the native USB peripheral. `FREEINK_LOG_TRANSPORT_USB_CDC_WRITE`
  is a supported log transport **[SDK]** `InputManager.cpp:59`.
- **No exposed UART header, no JTAG header, no test points documented.** No
  teardown photograph of this device exists to check for pads.

## Factory restore

See [`factory-firmware.md`](factory-firmware.md). Short version: **make your own
full-flash backup before you do anything**, because no X4 Pro stock image was
located anywhere public in this session.

## Known-good project starting points

| Project | Why |
|---|---|
| [CrossPoint Reader](https://github.com/crosspoint-reader/crosspoint-reader) | Upstream; the reference |
| [CrossInk](https://github.com/uxjulia/CrossInk) | The other major line; has an SDL simulator |
| [CrossPlay](../../../software/applications/crossplay/README.md) | Analysed in this knowledge base; `x4pro` is its design floor |
| [`MrStu82/crosspoint-llama-pro`](https://github.com/MrStu82/crosspoint-llama-pro) | Explicitly *"for the Xteink X4 Pro (ESP32-S3, GT911 touch, dual warm/cold frontlight)"* |
| [`thepropm/proink-os`](https://github.com/thepropm/proink-os) | From-scratch firmware on the FreeInk SDK |

## Related

[`commands.md`](commands.md) · [`factory-firmware.md`](factory-firmware.md) ·
[`pinouts-and-buses.md`](pinouts-and-buses.md)
