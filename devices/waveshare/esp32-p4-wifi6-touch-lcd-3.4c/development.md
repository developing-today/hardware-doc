# Development, flashing and recovery

> ESP32-P4-WIFI6-Touch-LCD-3.4C and [4C](../esp32-p4-wifi6-touch-lcd-4c/README.md).
> Evidence status: **vendor documentation + vendor source code. Nothing built or flashed here.**
> Every command below is **inferred from standard ESP-IDF practice** unless marked otherwise, and
> none has been executed against this hardware.

## The central fact: there are two MCUs

| MCU | Role | Flashed via |
|---|---|---|
| **ESP32-P4** | Your application | Type-C port (CH343P USB-UART) |
| **ESP32-C6-MINI-1-N4** | Wi-Fi 6 / BT 5 LE radio co-processor | **Its own SH1.0 4-pin header** |

The board exposes **two** SH1.0 4-pin headers — one brings out the C6 for firmware flashing, the
other brings out the P4 serial port. They are not interchangeable, and the normal Type-C workflow
**never touches the C6**.

This produces the board's most confusing failure mode: **an application that cannot join Wi-Fi may
have perfectly good P4 firmware and stale, mismatched, or missing C6 firmware.** It presents as an
application bug — init failure, timeouts, empty scan results — while the fault is on a chip your
build system never programmed. Before debugging networking code, establish what the C6 is running.

## Toolchain

| Item | Value | Confidence |
|---|---|---|
| Framework | ESP-IDF | Official |
| **CI-validated versions** | **v5.5.5 and v6.0.2** | **Official** — Waveshare's repo CI matrix |
| Declared floor in ZIP manifests | `idf: "^5.0"` | Official but misleading — see below |
| **Official BSP** | **`waveshare/esp32_p4_wifi6_touch_lcd_xc` `3.0.1`** | Official |
| Alternative | Arduino, via Waveshare's `displays` library + Arduino_GFX + LVGL | Official |
| Also documented | Eclipse + Espressif-IDE plug-in | Wiki |

The demo ZIP's `^5.0` floor is not what Waveshare actually test. Their repository CI validates
**exactly v5.5.5 and v6.0.2**. Use one of those.

**Use the published BSP rather than hand-rolled pin constants:**

```yaml
dependencies:
  waveshare/esp32_p4_wifi6_touch_lcd_xc: "3.0.1"
```

then select `BSP_LCD_TYPE_800_800_3_4_INCH` (3.4C) or `BSP_LCD_TYPE_720_720_4_INCH` (4C). See
[`official-repo-and-community.md`](./official-repo-and-community.md#2-the-official-bsp-is-a-published-component).

## Build and flash the P4

```bash
. $IDF_PATH/export.sh
idf.py set-target esp32p4
idf.py build
idf.py -p /dev/ttyACM0 flash monitor      # port name will vary
```

The Type-C port presents through a **CH343P** USB-UART bridge. On Linux this typically enumerates
without extra drivers; on macOS a WCH driver is usually required. See the
[USB-UART bridge record](../../../components/wch/ch340x/README.md).

> **Arduino uses a different path.** For the tested Arduino FQBN, sketch `Serial` is **Hardware CDC
> on the Type-C USB port**, *not* the CH343P UART. Start the sketch with the monitor closed;
> missing startup lines are expected because the non-blocking logger drops them. This costs people
> an afternoon if they assume one port serves both toolchains.

Waveshare also document Espressif's **Flash Download Tool** (Windows GUI) on the wiki, linked as
`https://dl.espressif.com/public/flash_download_tool.zip`.

## Flash the C6 radio firmware

**The interface is now known; the firmware is not.** Header `J4` (SH1.0 4-pin), read from the
schematic:

| Pin | Signal |
|---:|---|
| 1 | `C6_U0TXD` |
| 2 | `C6_U0RXD` |
| 3 | `GND` |
| 4 | `C6_IO9` — **the C6 boot strap** |

`C6_IO9` held low at reset enters serial download mode, as on any ESP32-C6. So `J4` gives you TX,
RX, GND and the strap — everything a standard USB-UART adapter needs.

**Still unknown:** the firmware image, its version, and the flash offsets. Waveshare do not appear
to publish them. The likely source is Espressif's `esp_hosted` project, which ships co-processor
firmware for the P4+C6 pairing. See
[C17](./gaps-and-conflicts.md#c17--esp32-c6-flashing-interface--partly-resolved).

Do **not** guess offsets. Writing a wrong image to the radio co-processor is a plausible way to
make a working board look broken. Resolve from Waveshare's wiki flashing section or Espressif's
`esp_hosted` documentation before attempting it.

Open question tracked in [gaps-and-conflicts.md](./gaps-and-conflicts.md).

## Recommended bring-up order

Each step isolates one subsystem, so a failure localises cleanly:

1. **`02_HelloWorld`** — toolchain, USB, serial. Nothing else.
2. **`03_i2c_tools`** — scan GPIO7/8. GT911, ES8311 and ES7210 should all answer. This single
   step validates the bus that touch **and** audio depend on.
3. **`06_displaypanel_3.4inch`** (or **`07_displaypanel_4inch`** on the 4C) — DSI link and panel.
4. **`05_I2SCodec`** — audio playback. Remember GPIO53 enables the amplifier.
5. **`04_wifistation`** — exercises the C6 over SDIO. If this fails and steps 1–4 passed, suspect
   C6 firmware before your code.
6. **`12_camera_dsi`** — full CSI → ISP → DSI pipeline.
7. **`09_lvgl_demo_v8`** / **`10_lvgl_demo_v9`** — pick your LVGL major version deliberately.

`03_sdmmc` now has a [known-good pin set](./pinouts-and-buses.md#microsd--connector-sd1), but
remember it does **not** drive **GPIO45**, the card's power switch — see
[storage.md](./features/storage.md).

## Recovery

| Situation | Approach | Confidence |
|---|---|---|
| Bad P4 application | Re-flash over Type-C; ESP32 ROM bootloader is not erasable | High |
| Board appears dead, screen black | **Check backlight first** — GPIO26 PWM is active low, and GPIO33 `BL_EN` may also need asserting | High |
| microSD never enumerates | **GPIO45 powers the card rail**; no demo drives it | High |
| Wi-Fi never works | Suspect C6 firmware, not P4 code | High |
| Bad C6 firmware | Re-flash via SH1.0 header — **procedure not established** | **Unknown** |
| Factory image | **Published for both variants** — see below | High |

### Factory firmware *is* published — correction

An earlier version of this page stated no factory image existed. **That was wrong.** Waveshare's
repository ships 16 MiB merged images for both variants:

```
firmware/ESP32-P4-WIFI6-Touch-LCD-3.4C-FactoryOnly-260821.bin
firmware/ESP32-P4-WIFI6-Touch-LCD-4C-FactoryOnly-260821.bin
```

with `scripts/Flash-CI-Firmware.ps1` / `Flash-CI-Firmware.cmd` as helpers. Flash the matching
image first to establish a known-good baseline before debugging your own code.

**Built for ESP32-P4 rev3.x and 32 MB flash only.** There is no `rev1_3` firmware profile, so a
pre-v3 board cannot run these images as-is — see
[C14](./gaps-and-conflicts.md#c14--esp32-p4-silicon-revision-changes-the-dsi-phy-clock-source).

## Hardware hazards

1. **RTC battery holder accepts rechargeable cells only — this is a safety issue, not a
   preference.** The schematic shows the cell fed from `ESP_3V3` through a **bare B5819WS Schottky
   with no current-limiting resistor**. A primary CR2032 fitted here *will* be charged and can
   vent, leak or rupture. Use ML2032/LIR2032. See
   [C18](./gaps-and-conflicts.md#c18--rtc-battery-is-charged-through-a-bare-schottky-diode).
2. **Backlight is active low.** Not a hazard, but the most common false "dead board".
3. **40-pin header is not a Raspberry Pi HAT socket.** Waveshare say "compatible with *some*"
   HATs. It is a GPIO breakout without Pi power/ID-EEPROM semantics. Check per-HAT.
4. **2 W speaker output** can brown out a marginal USB supply.

## Open questions

- ESP32-C6 firmware: source, version, flash procedure, offsets. Note Waveshare's own components
  doc says hosted-Wi-Fi ranges should be revisited "only when the exact ESP32-C6 image or source
  revision is recorded" — implying they do not publish it either.
- Whether the microSD and the ESP32-C6 SDIO link share an SDMMC host.
- The 40-pin header pinout, MIPI-CSI connector GPIOs and RTC circuit — still unmapped.

## Related

- [Feature guides](./features/README.md)
- [Shared platform record](../esp32-p4-wifi6-touch-lcd-xc-shared/README.md)
- [Gaps and conflicts](./gaps-and-conflicts.md)
