# Selected examples

> ESP32-P4-WIFI6-Touch-LCD-3.4C / 4C. Selected **2026-08-26** from
> [`catalog.json`](./catalog.json) (20 entries).
>
> ⚠️ **None of these were built or run.** No hardware and no ESP-IDF toolchain run in this session.
> Every `build_status` is `not-built-here`. Selection is on coverage and provenance, not on
> observed behaviour.

## Start here

```bash
git clone https://github.com/waveshareteam/ESP32-P4-WIFI6-Touch-LCD-XC.git
cd ESP32-P4-WIFI6-Touch-LCD-XC && git checkout 6948676d6451   # pin for reproducibility
```

Apache-2.0, CI-tested against **ESP-IDF v5.5.5 and v6.0.2**. Use this rather than the demo ZIP,
which ships no licence and older example numbering.

## Bring-up order

Each step isolates one subsystem so a failure localises:

| # | Example | Proves | Why this one |
|---|---|---|---|
| 1 | `02_HelloWorld` | Toolchain, USB, serial | Nothing else in the way |
| 2 | `03_i2c_tools` | **The shared I²C bus** | See below — highest-value diagnostic on the board |
| 3 | `07_Displaycolorbar` | DSI link + JD9365 | Minimal display path, uses the BSP |
| 4 | `08_lvgl_demo_v9` | Display **+ touch** | First integrated example |
| 5 | `06_I2SCodec` | Audio out | Remember GPIO53 enables the amplifier |
| 6 | `04_wifistation` | ESP32-C6 over SDIO | If 1–5 passed and this fails, suspect **C6 firmware** |
| 7 | `09_video_lcd_display` | CSI → ISP → DSI | The headline capability end-to-end |
| 8 | `10_mp4_player` | Everything at once | SD + decode + display + audio |

## Why `03_i2c_tools` matters more than it looks

GPIO7/8 is a **single bus shared by four device families** — GT9271 touch, ES8311 codec, ES7210
echo-cancel ADC, and the camera's SCCB control (confirmed from the schematic, C16). Plus anything
on header `J6` or `J8` pins 37/39.

So a stuck device takes out touch, audio **and** camera together, and a "camera bug" may be a
wedged codec. Scanning the bus first is the cheapest way to avoid chasing the wrong subsystem.

## Coverage against the feature set

| Feature | Covered by | Gap |
|---|---|---|
| Display | `07`, `08` | — |
| Touch | `08` | Polling only by design (C11) |
| Wi-Fi 6 / BT | `04` | C6 firmware not published |
| Audio **out** | `06`, `10` | — |
| Audio **in** | **nothing** | ⚠️ **No official example exercises the ES7210** |
| Camera | `09` | Which sensor ships is unconfirmed |
| Storage | `05`, `10` | Does not drive **GPIO45**, the card power switch (C13) |
| USB OTG | `12` | Device mode only; host mode uncovered |
| LVGL | `08` | LVGL 9 only in the repo |
| 40-pin header | **nothing** | No example; 12 power pins unidentified |
| RTC | **nothing** | No example; **charge-circuit safety issue (C18)** |

**Three fitted capabilities have no example at all**: audio capture, the expansion header, and the
RTC. Audio capture is the most significant — the ES7210 is on the board and named in vendor
material, but nothing demonstrates it.

## Alternative approaches worth knowing

| Approach | Example | When |
|---|---|---|
| **LVGL 9** | `08_lvgl_demo_v9` | Default. Widest community support |
| **ESP-Brookesia** | `11_esp_brookesia_phone` | Phone-style shell; also the factory firmware |
| **Embedded Wizard** | [`EmbeddedWizardGUI/…-3.4C`](https://github.com/EmbeddedWizardGUI/ESP32-P4-WIFI6-Touch-LCD-3.4C) | A **non-LVGL** commercial GUI stack on this exact board |
| **Arduino** | `examples/arduino` | ⚠️ Waveshare themselves recommend against it on P4 |

The Embedded Wizard project is the most interesting community find — it proves a completely
different GUI stack works here, which no vendor material mentions. Note it is vendor-affiliated
(Embedded Wizard is a commercial product), so read it as a supplier demonstrating their own
toolchain rather than independent community validation.

## The most valuable community project

[**`netseye/linux-waveshare-xc`**](https://github.com/netseye/linux-waveshare-xc) — a native RV32
NOMMU **Linux** port targeting *both* XC variants.

Worth reading even if you never boot Linux, because it documents things no vendor source does:

| Contribution | Why it matters |
|---|---|
| C6 SDIO pins: D0–D3 **14–17**, CLK **18**, CMD **19**, reset **GPIO54** active-high | The internal radio link, undocumented by Waveshare |
| ESP-Hosted-NG build + `esptool --chip esp32c6 write-flash 0x0` | Closes most of the C6 flashing gap ([C17](../gaps-and-conflicts.md#c17--esp32-c6-flashing-interface--partly-resolved)) |
| *"P4 exposes one DW-MMC host"* → microSD and Wi-Fi **mutually exclusive** | Best answer yet to a question open all through this record |
| ⚠️ *"Do not flash the original WHY2025 C6 firmware"* — it expects different SPI wiring | Bricking-adjacent warning |

It also **independently confirms** two of this record's schematic findings — touch INT/RST are NC
so touch must be polled, and backlight is GPIO26 active-low. Written by an unrelated author from
the same public schematic.

**Caveats:** licence is `NOASSERTION` (terms effectively unknown), 1 star, and the author states
plainly that *"physical-board validation is still required."* Nothing there is hardware-verified
either.

## XiaoZhi — the best audio-capture reference

[`78/xiaozhi-esp32`](https://github.com/78/xiaozhi-esp32) carries a dedicated board config at
`main/boards/waveshare/esp32-p4-wifi6-touch-lcd/config.h` with explicit `3_4C` and `4C` blocks.
**62 code hits across forks.**

It matters for two reasons no vendor source covers:

| Contribution | Why |
|---|---|
| `AUDIO_INPUT_SAMPLE_RATE 24000` + `AUDIO_INPUT_REFERENCE true` | A **working ES7210 capture config with AEC reference** — no official example does this |
| `BOOT_BUTTON_GPIO GPIO_NUM_35` | The **only** source mapping the BOOT button; the BSP declares `BSP_CAPS_BUTTONS 0` |

It also confirms the pin map, the 1500 Mbps lane rate and the active-low backlight **without using
the Waveshare BSP** — an independent fourth derivation.

> ⚠️ That `config.h` is a single `#elif` chain covering **nine** Waveshare P4 boards. Other
> variants use `GPIO_NUM_33`/`GPIO_NUM_32` for reset and backlight. **Isolate the
> `CONFIG_BOARD_TYPE_WAVESHARE_ESP32_P4_WIFI6_TOUCH_LCD_3_4C` (or `_4C`) block before reading any
> value** — a naive grep attributes another board's pins to this one.

## What real projects actually configure

From three working projects' `sdkconfig`:

| Setting | traviscea (3.4C) | garagetinkering (3.4C) | fabkury (4C) |
|---|---|---|---|
| I²C | **400 kHz** | **400 kHz** | **400 kHz** |
| Colour | RGB565 | RGB565 | RGB888 |
| Frame buffers | 1 | 3 | 3 |

All three use 400 kHz — nobody falls back to 100 kHz despite four device families on the bus. Both
colour depths and 1–3 buffers are in real use, so neither is a hidden constraint.

## Deliberately rejected

| Example | Reason |
|---|---|
| `01_HowToCreateProject` | Project skeleton; exercises no hardware |
| [`chvvkumar/ESP32-P4-NINA-Display`](https://github.com/chvvkumar/ESP32-P4-NINA-Display) (46★) | Targets the **4B** — different panel and BSP |
| [`RTechAI/ESP32-P4-LVGL-Boilerplate-3`](https://github.com/RTechAI/ESP32-P4-LVGL-Boilerplate-3) (10★) | Targets the **7B**; licence is `NOASSERTION` |
| [`blk96gt/ha_esp32_dashboard`](https://github.com/blk96gt/ha_esp32_dashboard) (4★) | Targets the **7B** |

The three rejections are the *most popular* projects in the ESP32-P4 display family, and it would
be easy to cite them as evidence for this board. They are not — different panels, different BSP
variants, different resolutions. Their techniques transfer; their pin values and configs do not.

## Version pins worth copying

Waveshare pin these deliberately:

| Component | Pin | Reason |
|---|---|---|
| `waveshare/esp32_p4_wifi6_touch_lcd_xc` | **`3.0.1`** | Must be a published registry version — not a Git URL or local path |
| `esp_audio_codec` | **`2.5.0`** | 2.6+ requires P4 rev ≥ 3.0, breaking the `rev1_3` profile |
| `espressif/tinyusb` | **`0.17.0~2`** | Exact release `usb_device_uac 1.2.0` permits; prevents descriptor drift |
| `esp_video` | `~2.0` | Camera + display pipeline |
| `esp_wifi_remote` / `esp_hosted` | Differs by IDF line | IDF 6: `>=1.6,<2.0` / `>=2.12,<3.0` · IDF 5.5: `0.14.*` / `1.4.*` |

## Not vendored here

None of these examples are copied into this repository. They are all reachable from a single
Apache-2.0 repository at a pinned commit, so vendoring would duplicate ~111 MB for no gain. Only
the **board-specific subset of the demo ZIP** is vendored, under the
[shared platform record](../../esp32-p4-wifi6-touch-lcd-xc-shared/README.md) — chiefly Waveshare's
`displays` library, which is the authoritative source for the pin map and both JD9365 init tables.
