# Feature coverage map

> ESP32-P4-WIFI6-Touch-LCD-3.4C / 4C. Snapshot **2026-08-24**.
> **No feature has been tested on hardware.** "Evidence" below means documentary evidence only.

| Feature | Hardware | Official demo | Feature guide | Pins established? | Evidence | Gap |
|---|---|---|---|---|---|---|
| Display | JD9365 MIPI-DSI 2-lane | `06_` (3.4C) / `07_` (4C) | [display](./features/display.md) | **Yes** (RST 27, BL PWM 26, **BL_EN 33**) | **Schematic** + vendor source | Refresh rate; reg `0x40`; `BL_EN` default state |
| Touch | **GT9271** I²C (GT911 driver) | Arduino `displays` lib | [touch](./features/touch.md) | **Yes** (SDA 7 / SCL 8, RST 23; **INT not wired**) | **Schematic** + vendor source | I²C address; poll-only |
| Wi-Fi 6 / BT 5 LE | ESP32-C6-MINI-1 over SDIO | `04_wifistation` | [wifi](./features/wifi-and-bluetooth.md) | N/A (SDIO) | Vendor source | C6 firmware + flash procedure; throughput |
| Audio playback | ES8311 + amp | `05_I2SCodec` | [audio](./features/audio.md) | **Yes** (I²S 13/12/10/9/11, PA 53) | Vendor source | Sample rates; amp part number |
| Audio capture | ES7210 AEC + dual MEMS mic | **None** | [audio](./features/audio.md) | **Yes** — I²S RX in BSP | **BSP source** | No *example*, but the BSP implements the RX path |
| Camera | MIPI-CSI 2-lane, ISP, H.264 | `09_video_lcd_display` | [camera](./features/camera.md) | **Yes** — `J5` traced, SCCB on shared I²C | **Schematic** | Which sensor ships; 1080p30 unverified |
| microSD | SDIO 3.0 | `03_sdmmc` (**stock upstream**) | [storage](./features/storage.md) | **Yes** (39–44, **pwr 45**) | **Schematic** | GPIO45 polarity; card-detect; no demo powers the rail |
| USB OTG HS | Type-A OTG + Type-C CH343P | `12_usb_extend_screen` | [usb](./features/usb.md) | **Yes** — `J3` traced | **Schematic** | **Host mode advertised but undemonstrated** |
| USB-UART | CH343P, Type-C | — | [development](./development.md) | N/A | Schematic | — |
| 40-pin header `J8` | GPIO breakout, 2.54 mm | **None** | [expansion-header](./features/expansion-header.md) | **28/40 mapped**, count vendor-confirmed | **Schematic** + CN vendor | 12 power/GND pins unidentified; **not** Pi-compatible; **no example exists** |
| RTC | Backup cell on `ESP_VBAT` | **None** | [pinouts](./pinouts-and-buses.md#rtc-backup-battery-j1) | **Yes** — `J1`, `D2`, `C39` | **Schematic** | **Safety: no charge current limit (C18)** |
| LVGL 9 | — | `08_lvgl_demo_v9` | [display](./features/display.md) | N/A | Vendor source | Bundled LVGL **verified stock** (C5) |
| Brookesia UI | — | `11_` (**not vendored**, 73 MiB) | *(none)* | N/A | Vendor source | Not analysed |

## Where the real gaps are

**Every subsystem is now mapped.** The RTC was the last, and resolving it surfaced a safety issue
([C18](./gaps-and-conflicts.md#c18--rtc-battery-is-charged-through-a-bare-schottky-diode)): the
backup cell is charged through a bare Schottky with no current limit, so fitting a primary CR2032
is hazardous.

`J8` is 28/40 mapped — every named signal is placed, but **12 power/GND pins remain unidentified**
because they are drawn as schematic symbols rather than text labels. Those 12 are the dangerous
ones: connecting to them without a meter risks feeding 5 V into a GPIO. It is also **not**
Pi-compatible — pin 4 is a GPIO where a Pi has 5 V. See
[`pinouts-and-buses.md`](./pinouts-and-buses.md#40-pin-expansion-header-j8).

Connectors `J3` (USB), `J4` (C6 UART), `J5` (MIPI-CSI) and `J6` (I²C) are now fully documented.

microSD was resolved on 2026-08-24 by reading the schematic — see
[`pinouts-and-buses.md`](./pinouts-and-buses.md). The remaining risk there is not the pins but
**GPIO45**, the power switch for the card rail that no demo drives
([C13](./gaps-and-conflicts.md#c13--microsd-sits-on-a-switched-rail-no-demo-enables)).

**Two capabilities are wired but unused by every shipped demo**: `BL_EN` on GPIO33
([C12](./gaps-and-conflicts.md#c12--backlight-has-two-controls-and-the-demos-use-only-one)) and the
microSD power switch on GPIO45. Both are the kind of thing a from-scratch project discovers the
hard way.

**Touch is poll-only**: `TP_INT` terminates at test point TP2 rather than a GPIO
([C11](./gaps-and-conflicts.md#c11--touch-interrupt-is-not-wired-to-the-soc)).

**Audio capture has no example, but is implemented.** No demo exercises the ES7210 — however the
BSP creates both `i2s_tx_chan` and `i2s_rx_chan` and registers the ES7210, so full duplex exists in
the vendor library. Capture is *undemonstrated*, not unsupported.

**Every advertised capability now has a guide**, including [usb.md](./features/usb.md) and
[expansion-header.md](./features/expansion-header.md). What remains are *evidence* gaps: USB host
mode is advertised but undemonstrated, and the 40-pin header has no example at all.

## Untested combinations

None of these has been evaluated; all are listed because they are the realistic ways this board
gets used:

| Combination | Concern |
|---|---|
| Display + camera | PSRAM bandwidth |
| Display + camera + audio | Bandwidth plus audio latency sensitivity |
| Wi-Fi + microSD | **Both are SDIO** — possible host contention |
| Touch + audio | **Shared I²C bus** on GPIO7/8 |
| Everything concurrently | Entirely unknown |

The Wi-Fi + microSD and touch + audio rows are not speculative resource-sharing worries; they
follow directly from the board's wiring. The others are bandwidth questions that only measurement
can settle.

## Now covered by the official BSP

Waveshare's published component `waveshare/esp32_p4_wifi6_touch_lcd_xc` **3.0.1** implements the
display, touch and audio contracts directly. Using it removes most of the pin-level risk in the
table above. See
[`official-repo-and-community.md`](./official-repo-and-community.md#2-the-official-bsp-is-a-published-component).

Note Waveshare state their own contract is **compile-verified, not hardware-verified** — so
"covered by the BSP" still is not "known to work on a board".

## Evidence legend

- **Vendor source** — read from Waveshare's own shipped code. Strongest evidence available here.
- **Wiki only** — vendor marketing/description text; no code corroboration.
- **Schematic** — read from the schematic PDF, rendered to images and inspected visually. The
  strongest evidence available short of hardware.
- **None tested.** No claim in this repository for this board has been validated on hardware, and
  there is **no community corroboration** either — see
  [C9](./gaps-and-conflicts.md#c9--community-evidence--resolved-2026-08-26).
