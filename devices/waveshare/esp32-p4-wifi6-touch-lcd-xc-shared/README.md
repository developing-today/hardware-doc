# Waveshare ESP32-P4-WIFI6-Touch-LCD-XC — shared board platform

> `XC` is **Waveshare's own family wildcard**, not a product you can buy. It covers the two
> shipping variants, which are the same PCB with different round MIPI-DSI panels:
>
> - [**ESP32-P4-WIFI6-Touch-LCD-3.4C**](../esp32-p4-wifi6-touch-lcd-3.4c/README.md) — 3.4 inch, 800 × 800
> - [**ESP32-P4-WIFI6-Touch-LCD-4C**](../esp32-p4-wifi6-touch-lcd-4c/README.md) — 4 inch, 720 × 720
>
> Research retrieved **2026-08-24**.

## Why this directory exists

Waveshare publishes **one schematic and one demo archive for both boards**, under a literal `XC`
path on their file host:

```
https://files.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-XC/ESP32-P4-WIFI6-Touch-LCD-XC-Schematic.pdf
https://files.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-XC/ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip
```

Both product wikis link the **same two files**. Storing them once here avoids duplicating a
1.8 MiB schematic and a 118 MiB archive across two device records, mirroring the precedent set by
[`devices/espressif/shared-artifacts/`](../../espressif/shared-artifacts/README.md).

This is a *vendor-declared* sharing relationship, not an inference on our part: the shared `XC`
filename is Waveshare's own, and the demo archive contains per-variant projects
(`06_displaypanel_3.4inch` and `07_displaypanel_4inch`) side by side in a single tree.

## What is genuinely shared vs per-variant

Everything below is derived from Waveshare's own board-support code in the demo archive, not from
marketing copy.

| Aspect | 3.4C | 4C | Shared? |
|---|---|---|---|
| PCB, schematic | identical | identical | **Shared** |
| SoC, radio, audio, power, connectors | identical | identical | **Shared** |
| Panel controller | JD9365 | JD9365 | **Shared** |
| MIPI-DSI lanes | 2 | 2 | **Shared** |
| DSI lane bit rate | 1500 Mbps | 1500 Mbps | **Shared** |
| DSI porch timings | pw20/bp20/fp40 · pw4/bp12/fp24 | identical | **Shared** |
| LCD reset / backlight GPIO | 27 / 26 | 27 / 26 | **Shared** |
| **Active resolution** | **800 × 800** | **720 × 720** | **Differs** |
| **Panel diagonal** | **3.4 in** | **4.0 in** | **Differs** |
| **JD9365 init register `0x40`** | **`0x00`** | **`0x04`** | **Differs** |

**Only three things actually differ**: the resolution constants, the physical panel, and a single
byte in the JD9365 initialisation sequence. Everything else — including the horizontal and
vertical porches — is byte-identical between the two variants' code.

That shared-porch detail is worth pausing on. Waveshare uses the *same* blanking intervals and the
*same* 1500 Mbps lane rate for both panels despite an 11% difference in horizontal pixel count.
The DSI link is therefore running with more slack on the 4C than on the 3.4C. This is plausible
and appears to work, but it means the timings are **not** derived per panel; do not assume they
are optimal for either, and re-derive them if you change the pixel clock or colour depth.

## Board architecture

| Function | Part | Interface | Component record |
|---|---|---|---|
| Main SoC | **ESP32-P4NRW32** (32 MB in-package PSRAM) | — | [espressif/esp32-p4](../../../components/espressif/esp32-p4/README.md) |
| Flash | 32 MB NOR, QSPI | QSPI | — |
| Wi-Fi 6 / BT 5 LE radio | **ESP32-C6-MINI-1-N4** | SDIO (`esp_hosted`) | *(record pending)* |
| Display | **JD9365** round IPS, capacitive | MIPI-DSI, 2 lane | [components/jadard/jd9365](../../../components/jadard/jd9365/README.md) |
| Touch | **GT911** | I²C | [goodix/gt911](../../../components/goodix/gt911/README.md) |
| Audio codec | **ES8311** | I²S + I²C | *(record pending)* |
| Echo-cancel ADC | **ES7210** | I²S + I²C | *(record pending)* |
| USB-UART bridge | **CH343P** | USB FS ↔ UART | [wch/ch340x](../../../components/wch/ch340x/README.md) |
| Power regulators | **MP1658**, **MP1605** | — | *(record pending)* |
| Camera | MIPI-CSI 2-lane, 15-pin 1.0 mm FPC | MIPI-CSI | — |
| Storage | microSD, SDIO 3.0 | SDMMC | [generic/micro-sd-sdmmc](../../../components/generic/micro-sd-sdmmc/README.md) |
| Expansion | 40-pin GPIO header, partially Raspberry-Pi-HAT compatible | — | — |
| RTC | Rechargeable RTC battery holder | — | — |

The ESP32-P4 has **no built-in radio**. Wi-Fi and Bluetooth come entirely from the ESP32-C6-MINI-1
over SDIO, using Espressif's `esp_hosted` / `esp_wifi_remote` split-stack model. This is the same
architecture as Espressif's own P4 boards and the single most important thing to understand before
writing networking code for this board — see
[`features/wifi-and-bluetooth.md`](../esp32-p4-wifi6-touch-lcd-3.4c/features/wifi-and-bluetooth.md).

## Verified pin map

Sources are Waveshare's own code. Provenance is given per row because the archive also contains
**unmodified upstream Espressif examples whose pin defaults belong to other boards** — see the
conflict note below.

| Signal | GPIO | Evidence |
|---|---:|---|
| I²C SDA (touch, ES8311, ES7210) | **7** | `Arduino/libraries/displays/displays_config.h`, `i2c.h`; `05_I2SCodec` P4 branch |
| I²C SCL | **8** | same |
| LCD reset | **27** | `06_/07_displaypanel/main/test_esp_lcd_jd9365.c`; `displays_config.h` `lcd_rst` |
| LCD backlight | **26** | `06_/07_displaypanel` `TEST_PIN_NUM_BK_LIGHT`, active **low** |
| I²S MCLK | **13** | `05_I2SCodec/main/example_config.h`, `CONFIG_IDF_TARGET_ESP32P4` branch |
| I²S BCLK | **12** | same |
| I²S WS/LRCK | **10** | same |
| I²S DOUT (to codec) | **9** | same |
| I²S DIN (from codec) | **11** | same |
| Speaker amplifier enable (PA) | **53** | same, `GPIO_OUTPUT_PA` |
| Backlight **enable** (`BL_EN`) | **33** | **Schematic** `R61` — no demo drives this |
| Touch reset (`TP_RST`) | **23** | **Schematic** `R62` |
| Touch interrupt (`TP_INT`) | **not wired to SoC** | **Schematic** — terminates at test point TP2 |
| microSD DAT0–DAT3 | **39, 40, 41, 42** | **Schematic** |
| microSD CMD / CLK | **44** / **43** | **Schematic** |
| microSD VDD power switch | **45** | **Schematic** — AO3401 P-MOSFET gate |

I²C runs at 100 kHz in the Arduino display library and 400 kHz in `i2c.h`; both are present in
Waveshare's own code, so treat 400 kHz as supported but 100 kHz as the conservative default.

### Known conflict — do not trust the SD card pins in `03_sdmmc`

`ESP-IDF/03_sdmmc` is the **stock Espressif SDMMC example, unmodified**. Its Kconfig carries
`default 44 if IDF_TARGET_ESP32P4` (CMD), `43` (CLK), `39` (D0) — these are **Espressif
ESP32-P4-Function-EV-Board defaults**, not values Waveshare established for this board.

Waveshare shipped the example without adding board-specific defaults, so the file looks
authoritative but is not. This is the classic inherited-example trap. **The microSD pin
assignment for this board is unresolved.** Resolve it from the schematic's SDIO net names or by
probing hardware before relying on it. Recorded in
[`gaps-and-conflicts.md`](../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md).

## Artifacts held here

| Path | Bytes | SHA-256 | Notes |
|---|---:|---|---|
| `artifacts/schematic/ESP32-P4-WIFI6-Touch-LCD-XC-Schematic.pdf` | 1,869,787 | `7a12998f1e641c49ab5e38f4765bdaf76aad2269e908e87ccffd572316647d68` | 2 pages, PDF 1.3, validated by `%PDF` magic |
| `artifacts/demo/` | ~2.3 MiB | — | Board-specific demo sources only, extracted from the ZIP below |
| `artifacts/source-snapshots/` | ~204 KiB | — | Both product wiki pages as retrieved 2026-08-24 |

Upstream `Last-Modified`: schematic **2025-05-26**, demo ZIP **2025-06-28**.

### The demo ZIP is archived, not vendored

| Field | Value |
|---|---|
| File | `ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip` |
| Bytes | 117,768,225 (112.3 MiB) |
| SHA-256 | `b5319593738e114270852d84be0fdd8ccdc21ef1dac897b15f4fad5069dd66b8` |
| URL | `https://files.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-XC/ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip` |
| Probe 2026-08-24 | `HTTP/1.1 200`, `Content-Length: 117768225` — **matches local byte size exactly** |
| Extracted | 289 MiB, **5052 files** |
| Extracted tree digest | `a856b1941de93ba892b244f03f139d958cb200807284f4ed66cd5d74b428c838` |
| Location | `archive/devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/originals/` |

289 MiB extracted is dominated by three bundled third-party trees that are reproducible from
upstream and were **not** vendored:

| Bundled tree | Bytes | Files | Tree digest (prefix) | Upstream | Modified? |
|---|---:|---:|---|---|---|
| `Arduino/libraries/lvgl` | 186,517,201 | 4267 | `ae0606a48e68723a` | LVGL **v9.3.0** | **No — stock** |
| `Arduino/libraries/GFX_Library_for_Arduino` | 27,130,057 | 309 | `f18c8606b56faebf` | Arduino_GFX **v1.6.0** | **No — stock** |
| `ESP-IDF/11_esp_brookesia_phone` | 73,198,225 | 306 | `e76fab6f24efafd1` | `espressif/esp-brookesia` | **Unknown** — no version pinned |

**LVGL and Arduino_GFX were diffed against upstream on 2026-08-24: zero differing files in either.**
Rebuild from the pinned tags with no patch step. The only additions are stripped dotfiles, an inert
`.vscode/settings.json`, and LVGL's `src/demos/` copy (an Arduino build convenience, one file
adjusted for include depth).

This is worth contrasting with the **knob board**, where the same check found a real one-line
functional patch in LVGL 8.4.0. Same vendor, same archive style, opposite answer — run the check,
don't assume. Detail:
[C5](../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c5--bundled-third-party-libraries--resolved-2026-08-24).

`esp-brookesia` remains undiffed because the demo pins no version to compare against.

What *was* vendored is the high-value remainder: all board-specific ESP-IDF projects, the Arduino
examples, `lv_conf.h`, and — most importantly — `Arduino/libraries/displays`, which is
**Waveshare's own board-support library** and the authoritative source for the pin map and both
JD9365 initialisation sequences above.

Reacquire:

```bash
curl -L -O https://files.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-XC/ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip
sha256sum ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip
# expect b5319593738e114270852d84be0fdd8ccdc21ef1dac897b15f4fad5069dd66b8
```

> **Single-source risk.** Unlike Waveshare's `/wiki/common/` shared pool, these files live under a
> product-specific directory with no third-party mirror located. Strong candidate for
> `https://web.archive.org/save/`.

## Demo inventory

| Project | Demonstrates | Board-specific? |
|---|---|---|
| `01_HowToCreateProject`, `02_HelloWorld` | Toolchain bring-up | Generic |
| `03_i2c_tools` | I²C bus scan — best first diagnostic | Generic tool, useful here |
| `03_sdmmc` | microSD | **Stock upstream — pins unverified** |
| `04_wifistation` | Wi-Fi via ESP32-C6 over SDIO | Board-relevant |
| `05_I2SCodec` | ES8311 playback | **P4 branch is board-accurate** |
| `06_displaypanel_3.4inch` | JD9365 800 × 800 | **3.4C only** |
| `07_displaypanel_4inch` | JD9365 720 × 720 | **4C only** |
| `08_lvgl_display_panel`, `09_lvgl_demo_v8`, `10_lvgl_demo_v9` | LVGL 8 and 9 | Board-relevant |
| `11_esp_brookesia_phone` | Phone-style UI | Not vendored (73 MiB) |
| `12_camera_dsi` | MIPI-CSI → MIPI-DSI passthrough | Board-relevant |
| `13_usb_extend_screen` | USB external display | Board-relevant |

Note both LVGL 8 and LVGL 9 demos ship, and the Arduino side bundles LVGL 9.3.0. Pin your LVGL
major version deliberately; the two APIs are not source-compatible.

## Licensing

| Artifact | Redistribution status | Disposition |
|---|---|---|
| Schematic PDF | `unknown` — Waveshare states no licence | repository, unstaged |
| Demo sources (Waveshare-authored) | `unknown` — no LICENSE file in archive | repository, unstaged |
| Bundled LVGL / GFX / brookesia | MIT / Apache-2.0 upstream, but **not verified in this copy** | not vendored |
| Wiki HTML snapshots | `unknown` | repository, unstaged |

No `LICENSE` file exists anywhere in the demo archive. Waveshare's demo code is conventionally
treated as freely usable example code, but that is **convention, not evidence**. Held unstaged
pending review.

## Related

- [ESP32-P4-WIFI6-Touch-LCD-3.4C](../esp32-p4-wifi6-touch-lcd-3.4c/README.md)
- [ESP32-P4-WIFI6-Touch-LCD-4C](../esp32-p4-wifi6-touch-lcd-4c/README.md)
- [ESP32-P4 chip record](../../../components/espressif/esp32-p4/README.md)
- [Espressif's own P4 boards](../../espressif/) — for comparison
- [Waveshare vendor documentation guide](../../../vendors/waveshare/README.md)
