# Cardputer ADV — selected examples

> Snapshot **2026-09-04**. Full candidate list: [`catalog.json`](catalog.json).
> Discovery method and depth: [`search-log.md`](search-log.md).
> **None of these was built or run by this session** — no toolchain, no hardware. Selection is
> on inspection of source at a pinned commit, not on execution.

## The portfolio

Chosen so that between them they cover every major feature, at least two distinct
implementation approaches, one integrated application, one diagnostic, and one useful negative.

| # | Example | Covers | Why this one |
|---|---|---|---|
| **1** | `M5Cardputer/examples/Basic/keyboard/singlePress` + `multiPress` + `inputText` | keyboard | The minimal per-feature diagnostic. Three sizes of the same idea; `inputText` is the one to copy. Vendored. |
| **2** | `M5Cardputer/examples/Basic/display` | display | Minimal M5GFX. Vendored. |
| **3** | `M5Cardputer/examples/Basic/mic_wav_record` | mic + microSD + audio | The only vendor example that exercises **two** subsystems together, and the one that will expose the ES8311 enable defect if it exists on your unit. Vendored. |
| **4** | `M5Cardputer/examples/Basic/ir_nec` | IR TX | Minimal RMT/IRremote. Vendored. |
| **5** | `M5Cardputer/examples/Basic/sdcard` | microSD | Minimal SPI SD. Vendored. |
| **6** | `M5Cardputer/examples/Basic/keyboard/usbKeyboard` | USB HID | Turns the device into a HID keyboard — the platform's signature trick. Vendored. |
| **7** | `M5Cardputer/examples/UI/REPL` (`REPL.ino` + `ReplView.{h,cpp}`) | **integrated**: keyboard + display + text UI | The best-maintained integrated starting point. Added `9e9ad46`, 2025-09-01 — **the same day as the TCA8418 reader**, i.e. written *for* the ADV. Vendored. |
| **8** | `M5Cardputer/examples/Advanced/SSHClient` | keyboard + display + Wi-Fi + a large dependency | Shows the RAM ceiling in practice. ⚠ needs `LibSSH-ESP32`, which `library.json` does **not** declare (only `library.properties` does). Vendored. |
| **9** | `m5stack/M5Cardputer-UserDemo` @ `CardputerADV` `b549eac0` | **everything**, including IMU, LoRa CAP, GNSS, BLE HID | M5Stack's own full application, ESP-IDF. Not an "example" but the reference integration. `main/hal/hal_config.h` is the most compact authoritative pin list. **Build config vendored; full tree not.** |
| **10** | `meshtastic/firmware` `variants/esp32s3/m5stack_cardputer_adv/` @ `be2f68b5` | CAP LoRa + GNSS + display + keyboard | **A second, independent implementation** of the same hardware by people who do not work at M5Stack. Its `variant.h` is why the G13/G15 question is settled. Not vendored — GPL-3.0, large. |
| **11** | `BruceDevices/firmware` `boards/m5stack-cardputer/` @ `1d555e0d` | **runtime dual-generation support** | The only implementation that serves v1.x and ADV from one binary. Also a **negative example**: it copies M5Unified's ES8311 register-`0x01` divergence verbatim. Not vendored — AGPL-3.0. |
| **12** | `geo-tp/M5-Card-Computer-I2C-Scanner` | diagnostic | Confirms `0x18`/`0x34`/`0x69` on the internal bus in ten seconds. MIT. Not vendored. |

## Why these and not others

* **Vendor examples first**, because they are MIT, small, versioned with the library that
  autodetects your board, and they compile against exactly the API this record documents.
* **The REPL example over a hello-world**, because its commit date proves it was written for the
  ADV and it is the only vendor example that is a *program* rather than a demo.
* **Meshtastic and Bruce included despite not being vendorable**, because independent
  reimplementations are the strongest evidence a pin map is right. Three implementations agreeing
  on `GPS_TX_PIN 13` is worth more than one vendor page.
* **Bruce doubles as a negative example.** Copying a driver defect from upstream is exactly the
  failure mode the skill's §10 audit exists to catch, and here it is, in the wild, in the most
  popular firmware on the platform.

## Not selected, and why

| Candidate | Reason |
|---|---|
| `M5Cardputer/examples/Basic/button`, `buzzer`, `mic` | subsumed by #3 and #7 |
| `bmorcelli/Launcher` | excellent documentation (`CardputerADV.md`), but the code is a boot menu; less instructive than Bruce as an integration |
| Emulators, games, DAWs | large, single-purpose, and none exercises a feature the list above misses |
| `Kezii/Rust-M5Stack-Cardputer` | a distinct and interesting approach, but GPL-3.0 and unmaintained-looking; noted in the catalog |
| `echo-lalia/Cardputer-Micropython-Examples` | MicroPython route, but ADV support unconfirmed — cannot recommend it for this board |

## Coverage check

| Feature | Covered by |
|---|---|
| Keyboard | 1, 7, 9, 10, 11 |
| Display | 2, 7, 9, 10, 11 |
| Audio out | 9, 11 |
| Audio in | 3, 9 |
| microSD | 3, 5, 9, 11 |
| **IMU** | **9 only** (`app_imu`) — thin |
| Battery | 9, 11 |
| Wi-Fi | 8, 11 |
| BLE | 9 (BLE HID) |
| IR | 4, 9, 11 |
| Grove | 12 |
| **CAP header** | 9, 10 |
| USB HID | 6, 9 |
| **RTC** | n/a — none fitted |

**Uncovered:** no example anywhere exercises the **3.5 mm jack detect** (it is hardware-only and
not software-visible), and IMU coverage rests on a single app inside a large ESP-IDF project.

## Build status

**All entries: `not-tested`.** No PlatformIO, no ESP-IDF and no hardware were available. The
correct next step for anyone with a device is `pio run -e m5stack-cardputer` on #7 and
`idf.py build` on #9, and to record the exact output — including failures — in
[`../commands.md`](../commands.md).
