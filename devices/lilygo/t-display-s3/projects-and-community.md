# T-Display-S3 — software, firmware and projects

> Family-level software survey lives here because the base board has the widest support.
> Per-variant status is in the "Which variants" column. Snapshot **2026-09-07**.

## 1. Framework and firmware support matrix

| Project | Supports | Which variants | Build | Status / evidence |
|---|---|---|---|---|
| **ESPHome** | **Yes, first-class** | `T-DISPLAY-S3`, `T-DISPLAY-S3-PRO`, `T-DISPLAY-S3-AMOLED`, `T-DISPLAY-S3-AMOLED-PLUS`, `T4-S3`, plus the ESP32 `T-DISPLAY` | YAML: `esp32: board: lilygo-t-display-s3` + `display: platform: mipi_spi, model: T-DISPLAY-S3` | **Confirmed in source.** `esphome/components/mipi_spi/models/lilygo.py` and `amoled.py`, `dev` branch fetched 2026-09-07. Board id `lilygo-t-display-s3` is in `esp32/boards.py`. Licence **MIT + GPLv3** (ESPHome dual) |
| **Tasmota** | **Yes, via runtime template** | base board only | Flash `Tasmota32-S3 (QIO Flash/OPI PSRAM)` with the web installer, then auto-configure with the **"Lilygo S3 Display"** template | **Firsthand user reports**, [issue #18](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/18). A Tasmota maintainer (`Jason2866`) participated. Reported working state: `Display Model 17, 320×170`. **You must run `displaydimmer 100`** or the screen is nearly black — the single most useful line in that thread. Licence **GPLv3** |
| **Meshtastic** | **No, and cannot** | — | — | **Negative result.** No LoRa radio on any T-Display-S3 variant. Searched `org:meshtastic tdisplay` (247 hits) — no variant exists. The LoRa members of the wider LilyGO catalogue (T-Beam, T-Deck, T3-S3, **T-Display-S3 Pro LR1121**) are separate products |
| **WLED** | **No** | — | — | **Negative result.** `wled/WLED` carries `usermods/TTGO-T-Display/` for the **ESP32** predecessor only. No S3 board file, no usermod |
| **MicroPython** | **Yes** | base board; others vary | `russhughes/st7789s3_mpy` — a C ST7789 driver with an 8-bit-parallel backend, with `tft_config.py` for this board. Also `Xinyuan-LilyGO/lilygo-micropython` and the newer `Xinyuan-LilyGO/T-Display-S3-MicroPython` (`boards/lilygo-t-displays3.json`, pushed 2026-09-04) | Linked from LilyGO's own README §6. **GPIO15 must still be driven in Python** — a MicroPython user's confusion about exactly this is in [issue #79](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/79), 2024-04-23 |
| **CircuitPython** | **Unknown** | — | — | No board definition located. **Absence not proven** — [K6](gaps-and-conflicts.md) |
| **LVGL** | **Yes, 8.x** | all | `examples/lv_demos` @ `ec889e7`; `lv_conf.h` is an LVGL 8 config | 9.x needs porting. The AMOLED library ships an `lv_conf.h.v9` you rename — see [`../t-display-s3-amoled/README.md`](../t-display-s3-amoled/README.md) |
| **ESP-IDF** | **Yes** | nine boards | `Xinyuan-LilyGO/LilyGo-Display-IDF` @ `b1a1cc5`, MIT. `menuconfig` selects the board via `CONFIG_LILYGO_*` | The `product_pins.h` in it is the best cross-variant pin source in the family |
| **Arduino** | **Yes, pinned to core 2.0.14** | all | see [`development.md`](development.md) | Vendor-pinned; TFT_eSPI documented broken above 2.0.14 |
| **Rust (`esp-hal`)** | SoC yes, board no | — | — | Asked in [issue #160](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/160). No board-support crate found |

### ESPHome, in detail

The `mipi_spi` model is worth reading because it encodes board knowledge you would otherwise
have to discover:

```python
ST7789V.extend("T-DISPLAY-S3",
    height=320, width=170, offset_width=35,
    color_order=MODE_BGR, invert_colors=True, draw_rounding=1,
    dc_pin=7, cs_pin=6, reset_pin=5,
    enable_pin=[9, 15],          # LCD_RD *and* the GPIO15 power gate
    data_rate="10MHz", bus_mode=TYPE_OCTAL,
    requires={"psram"})
```

`enable_pin=[9, 15]` is ESPHome doing the GPIO15 dance for you. `requires={"psram"}` makes the
OPI-PSRAM requirement a build error rather than a runtime mystery. This is why ESPHome is the
lowest-friction route onto this board for anyone who does not need custom C++.

One caution: an ESPHome regression report exists in this repo's tracker
([issue #314](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/314), 2025-08-08,
`Setup Failed: ESP_ERR_NOT_SUPPORTED` after upgrading to 2025.7.5) — but it turned out to be a
**T-Camera S3**, not a T-Display-S3, and the cause was an `esp32_camera` API change requiring an
I²C bus id instead of pins. Recorded so the next reader does not mis-attribute it.

## 2. Notable community projects

Evidence class in the last column: **DP** = demonstrable project (code or photos published),
**FO** = firsthand ownership report, **H** = hearsay.

| Project | What | Date | Where | Class |
|---|---|---|---|---|
| `teastainGit/LilyGO-T-display-S3-setup-and-examples` | The de-facto setup guide. Written because the vendor docs omitted GPIO15; **endorsed by LilyGO's maintainer in-thread** (2023-03-13) | 2023-01 → | [repo](https://github.com/teastainGit/LilyGO-T-display-S3-setup-and-examples) | DP |
| **NerdMiner V2** | Lottery Bitcoin miner; the T-Display-S3 is one of its headline targets | — | referenced in [issue #212](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/212) by an owner who had it running when nothing else worked | FO |
| **ESP32 Internet Weather Station** | Full LVGL weather UI, code published | 2024-08-16 | [r/esp32, 1312↑, 68 comments](https://old.reddit.com/r/esp32/comments/1ethutq/i_made_another_esp32_internet_weather_station_i/) | DP |
| **DIY auto gauge UI (LVGL)** | Automotive gauge cluster | 2025-03-11 | [r/esp32, 840↑](https://old.reddit.com/r/esp32/comments/1j8zvbc/diy_auto_gauge_ui_using_lvgl_on_lilygo_tdisplay_s3/) | DP |
| **Weather Micro Station** | Compact weather display | 2025-11-07 | [r/esp32, 105↑](https://old.reddit.com/r/esp32/comments/1oqx825/weather_micro_station_for_tdisplay_s3/) | DP |
| **Claude usage meter** | API-quota display; a 2026 genre | 2026-07-05 | [r/esp32](https://old.reddit.com/r/esp32/comments/1uo0m7i/claude_usage_meter_on_a_lilygo_tdisplay_s3/) | DP |
| **DS18B20 + PIR clock** | Notable for its **negative results**, not its output — see [`community.md`](community.md) | 2026-05-25 | [r/esp32](https://old.reddit.com/r/esp32/comments/1tnop7r/lilygo_tdisplay_s3_clock_with_ds18b20_and_pir/) | FO + measurement |
| **MIDI ecosystem** (`@sauloverissimo`) | Eight examples upstreamed **into the vendor repo**: BLE MIDI sender/receiver, USB MIDI piano visualiser, chord detection, event-queue debugger, BLE→USB MIDI bridge, music-theory explorer | 2025 | `examples/T-Display-S3-*` @ `ec889e7` | DP |
| **`@VolosR` PCBClock / PokerS3** | TFT_eSPI showcase sketches, also upstreamed | — | `examples/PCBClock`, `examples/PokerS3` | DP |
| **`@Rudi Ackermann` ImageScroll** | Smooth image scrolling with world time zones | — | `examples/ImageScroll` | DP |
| **NES emulator** | `arduino-nofrendo` vendored in the repo, playable | — | `examples/nes` | DP |
| **Bruce firmware** | Pentest/RF multi-tool; r/brucefw discusses the **AMOLED** variant | 2026-04-12 | [r/brucefw](https://old.reddit.com/r/brucefw/comments/1sjplql/lilygo_tdisplay_s3_amoled/) | H (for the base board) |
| **Battery backpack for the LilyGO shell** | Printable, referenced with a working cell part number | 2026-08 | [printables.com/model/1065538](https://www.printables.com/model/1065538-lilygo-t-display-s3-shell-battery-backpack) | DP |

**On prevalence:** the Reddit sample above is **27 family-relevant posts out of four
`search.json` queries at `t=all`**, not a census. It establishes that these projects exist and
were built; it does not establish how common any use is.

## 3. Vendor-shipped examples

Twenty-nine directories under `examples/` @ `ec889e7`. Catalogued with selection decisions in
[`examples/catalog.json`](examples/catalog.json); the recommended subset is in
[`examples/best.md`](examples/best.md).

## 4. Where to ask

| Venue | Useful for | Note |
|---|---|---|
| [`Xinyuan-LilyGO/T-Display-S3` issues](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues) | **the best resource.** 318 issues, nearly all closed, maintainer-answered | A bot closes issues after 30 days stale + 14 days. Answers survive; threads die |
| r/esp32 | project help, library problems | highest signal of the subreddits |
| r/LilyGO | vendor-specific | small, low traffic |
| r/Esphome | ESPHome YAML | active; the AMOLED board is well liked there |
| Tasmota Discord | Tasmota | issue #18 was explicitly redirected there |
