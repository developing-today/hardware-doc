# Xteink X3 — development

> ESP32-C3. Retrieval **2026-09-04**. **Nothing executed against hardware.**

## Toolchain

| Item | Value | Status |
|---|---|---|
| Framework | Arduino-ESP32 under PlatformIO | `reported-working` |
| Build flag | `-DFREEINK_DEVICE_X3=1` | `reported-working` |
| Effect | Links **both** X3 drivers — `FREEINK_DRIVER_UC8253_X3` **and** `FREEINK_DRIVER_UC8279`. Which one runs is decided at boot | **[SDK]** |
| esptool chip | `esp32c3` | `inferred` |
| Optional | `-DFREEINK_UC8279_CONFIG=yourConfig` to inject a UC8279 config | **[SDK]** |

Nothing extra is needed for the newer panel: *"Build: nothing new."*

## One binary, two devices

`-DFREEINK_DEVICE_X3=1` and `-DFREEINK_DEVICE_X4=1` can coexist:
`XteinkDetect::selectXteinkDevice()` fingerprints the I²C bus (SDA20/SCL0) for the
BQ27220, DS-series RTC and QMI8658 and picks the profile at runtime. Then a second
probe picks the panel controller. **A single C3 image can serve X3-UC8253,
X3-UC8279d and X4.**

## Build / flash / monitor

```bash
pio run -e x3                 # inferred
pio run -e x3 -t upload       # inferred
pio device monitor -b 115200  # inferred
```

## USB lock

Same as the rest of the family. See
[`../x4/development.md`](../x4/development.md#usb-lock). X3-specific note from the
CrossPoint 1.4.0 release:

> "Seems x3 users are having issues OTA updating. You can simply **reflash from the
> website if you're unlocked or SD flash if you're locked.** You won't lose any
> settings. … I'd like to stop using github releases moving forward as it causes
> **out of memory issues on the x3**."
> — [r/XTEINK `1uek163`](https://old.reddit.com/r/XTEINK/comments/1uek163/), 2026-06-24

## Bricking risks — X3-specific

| Risk | Note |
|---|---|
| **OTA out-of-memory** | **Observed on this device**, not theoretical. No PSRAM. GitHub-release OTA was abandoned because of it |
| **New panel variant** | Units shipped from ~July 2026 carry a **UC8279d**. Firmware without that driver leaves a blank screen. CrossPoint 1.5 (2026-08-07) added support: *"this release DOES support the new x3 display variants"* |
| **Stale fork + locked unit** | *"Other forks will need to pull the latest SDK to avoid **soft bricking locked units**"* |
| **Forgetting the SD rail** | GPIO13 must be driven HIGH in setup, LOW on sleep. Omitting the LOW causes battery drain through sleep |
| **Running the C3 I²C probe on an S3** | SDA20/SCL0 are USB D+ and a boot strap on S3. The SDK compiles it out; a hand-rolled build must too |

## Debug access

ESP32-C3 USB-serial-JTAG. **Board photographs exist** in
[`artifacts/teardown/`](media.md) — unlike every other Xteink device, test points
could in principle be identified from them. **Not attempted.**

## Flashing / backup tooling

| Tool | Note |
|---|---|
| [`zocs/eink-quick-flasher`](https://github.com/zocs/eink-quick-flasher) | The best X3 tool: GUI, auto COM detect, **1:1 full-flash backup and restore in ~2 min**, ships stock images, and includes a dedicated `X3-FLASHER-GUIDE` in **both EN and CN** (13.6 KB / 16.7 KB) |
| `crosspointreader.com` | Web flasher, unlock, flash-to-stock |
| [`bigbag/papyrix-flasher`](https://github.com/bigbag/papyrix-flasher) | Go CLI with MD5 verification |

## X3-specific projects worth reading

| Project | Why |
|---|---|
| [`anki630/crossmosa`](https://github.com/anki630/crossmosa) + [`crossmosa-freeink-sdk`](https://github.com/anki630/crossmosa-freeink-sdk) | 繁體中文 firmware **and its own SDK fork doing "UC8279 waveform tuning"** — the only project actively working the new panel |
| [`emezrahi/XTeink-X3-Supafast`](https://github.com/emezrahi/XTeink-X3-Supafast) | Refresh-speed work |
| [`kocha01/xteink-x3-pokiink-fw`](https://github.com/kocha01/xteink-x3-pokiink-fw) | PokiInk fork |
| [`sermelipharo/x3-trmnl`](https://github.com/sermelipharo/x3-trmnl) | TRMNL BYOD firmware on the CrossPoint HAL |
| [`evanstoddard/xteink_x3_zephyr`](https://github.com/evanstoddard/xteink_x3_zephyr) | **Zephyr** — the only non-Arduino/non-IDF RTOS attempt found |
| [`hannah-nula/crosspoint-x3-ble-page-turner`](https://github.com/hannah-nula/crosspoint-x3-ble-page-turner) | *"validated BLE page-turner reconnect support"* |
| [`wiltodelta/xteink-sugartv`](https://github.com/wiltodelta/xteink-sugartv) | Turns an X3 into a **continuous glucose monitor display** |
| [`ElendilDrac01/xteink-x3-calibre-stock`](https://github.com/ElendilDrac01/xteink-x3-calibre-stock) | Calibre plugin for **stock** firmware — useful if you do not want to reflash |

## Related

[`factory-firmware.md`](factory-firmware.md) · [`pinouts-and-buses.md`](pinouts-and-buses.md) ·
[family command ledger](../x4-pro/commands.md)
