# Development — Cap LoRa-1262 (U214)

The Cap has **no processor and no firmware of its own.** Everything here is host-side
(Cardputer-Adv / CardputerZero). Snapshot 2026-09-04.

## 1. Toolchains that know about this board

| Path | Board target | Status |
|---|---|---|
| **Arduino / PlatformIO + RadioLib** | Cardputer-Adv board defs | Vendor examples published; `not-tested` here |
| **Meshtastic** | `m5stack-cardputer-adv` (`board = m5stack-stamps3`) | **Upstream, official**, since 2.7.20 |
| **UiFlow2 / MicroPython** | `cap/lora1262` | Vendor docs at `uiflow-micropython.readthedocs.io/en/latest/cap/lora1262.html` |
| **ESP-IDF** | listed by M5Stack as a supported platform for the Mesh Kit | no Cap-specific component located |
| **Bruce**, **M5Launcher**, **Plai**, **MeshCore**, **WhisperOS** | community | [`projects-and-community.md`](projects-and-community.md) |

## 2. Libraries and exact versions

| Library | Role | Pin |
|---|---|---|
| **RadioLib** (jgromes) | SX1262 driver — this *is* the "Cap LoRa-1262 Arduino LoRa Driver Library" the docs link to | latest release **7.7.1** (2026-05-31); head `187ef24791c3d844939b2be13a68bd890bd04e4c` (2026-08-22). **MIT** |
| **m5stack/TinyGPSPlus** | GNSS — `MultipleSatellite` class. ⚠ **must** be the M5Stack fork, not the Library Manager copy | head `254a10041ac38d17d98dab24c0ae4d2a8d19a677` (2025-01-02). **No LICENSE file in the repo**; upstream TinyGPSPlus is LGPL-2.1 |
| **M5Unified** | `m5::In_I2C`, `m5::PI4IOE5V6408_Class` | version not pinned by the docs |
| **M5GFX** | display | — |

> **There is no M5Stack driver library for this Cap.** A GitHub search of `org:m5stack`
> for `lora`, `1262`, `cap` and `cc1101` returns no matching repository. The vendor's
> "driver library" links are pointers to third-party projects. Recorded as a finding, not
> a gap in the search: `executed-success`, 2026-09-04.

## 3. Build and flash — Arduino path

Nothing about flashing is Cap-specific; it is the host's procedure.

```text
Cardputer-Adv download mode  (vendor instructions, [DOC])
  1. Side power switch -> OFF
  2. Hold the G0 key
  3. Power on, then release
```

`inferred` for anything beyond that: no Cap-specific fuse, strap or recovery step exists,
because the Cap contains no programmable part.

## 4. Meshtastic

```bash
# Reproduce the officially supported build
git clone https://github.com/meshtastic/firmware.git
cd firmware
git submodule update --init --recursive
pio run -e m5stack-cardputer-adv
pio run -e m5stack-cardputer-adv -t upload
```
`not-tested` — transcribed from `variants/esp32s3/m5stack_cardputer_adv/platformio.ini`
and Meshtastic's standard build flow, not executed in this pass.

Prebuilt binaries ship inside the aggregated release asset
`firmware-esp32s3-<version>.zip` (e.g. `firmware-esp32s3-2.7.26.54e0d8d.zip`,
170 272 165 B). There is **no** per-board asset at the release level; the device index
`firmware-<version>.json` is what lists `{"board":"m5stack-cardputer-adv","platform":"esp32s3"}`.

Minimum useful versions:

| Want | Need |
|---|---|
| The board at all | **2.7.20** (2026-03-11) |
| Working antenna switch | **2.7.24** (2026-05-23) — two fixes landed 2026-05-18/19 |
| Current | 2.7.26 (2026-06-24, stable) or 2.8.0 prereleases (2026-08-30 / 2026-09-01) |

Build flags of note from `platformio.ini`: `-D M5STACK_CARDPUTER_ADV`,
`-D ARDUINO_USB_CDC_ON_BOOT=1`, `board_build.partitions = default_8MB.csv`,
`upload_protocol = esptool`.

Dependencies it pulls (pinned as GitHub zips, not registry versions):
`meshtastic/st7789@92bae2e4a307afb430c3b0bc3d661c55ee1565f0`,
`pschatzmann/arduino-audio-driver@v0.3.0`,
`meshtastic/ESP8266Audio@343024632ee78d6216907b2353fc943a62422d80`,
`earlephilhower/ESP8266SAM@1.1.0`.

## 5. UiFlow2 / MicroPython

`https://uiflow-micropython.readthedocs.io/en/latest/cap/lora1262.html` — enumerated from
the product page's link set, **not fetched** in this pass. Recorded as a known-unexplored
source.

## 6. Recovery

**Not applicable to the Cap.** It has no flash, no MCU and no bootloader. If a Cap appears
dead:

1. Confirm the host is providing 5 V on the EXT connector.
2. Probe I²C for `0x43` — if absent, either the Cap is not seated or it is a U201.
3. If `0x43` answers but RF is dead, suspect the antenna-switch init or the connector.
4. There is nothing to reflash.

## 7. Known bricking / damage risks

| Risk | Source |
|---|---|
| **Powering the LoRa radio with no antenna fitted** | M5Stack's own warning box on the product page: *"Do not connect or power on the device without installing the antenna, otherwise the device hardware may be permanently damaged!"* **[DOC]**. Standard for a +22 dBm PA into an open port |
| Wrong-band antenna | Not damaging, but a real range problem — [`features/lora.md` §7](features/lora.md) |
| Grove device at I²C 0x43 | Silently breaks the antenna switch and confuses Cap detection |
| Reversing the 14-pin header | Not investigated. The connector is keyed only by the enclosure fit |

## 8. Related

[`features/lora.md`](features/lora.md) · [`features/gnss.md`](features/gnss.md) ·
[`pinouts-and-buses.md`](pinouts-and-buses.md) · [`commands.md`](commands.md) ·
[`compatibility-and-status.md`](compatibility-and-status.md)
