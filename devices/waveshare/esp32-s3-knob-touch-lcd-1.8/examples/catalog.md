# Community and third-party projects — catalogue

Compiled **2026-08-23**; repository metadata retrieved **2026-08-23**; wiki-sourced entries retrieved **2026-08-21**.

Starting point was the Waveshare wiki's §8.8 "Project Resources" (nine entries, reproduced in [../wiki-resource-links.md](../wiki-resource-links.md)), extended by GitHub repository search across `ESP32-S3-Knob-Touch-LCD-1.8`, `Knob-Touch-LCD-1.8`, `ESP32-S3-Knob-Touch`, `JC3636K518`, and project-name follow-ups.

**28 board-specific repositories found. Waveshare lists eight.** The vendor's list omits nearly everything of engineering value — ESPHome support, secondary-MCU firmware, display-driver resolution, and an as-shipped firmware/SD-card archive.

> **Nothing here is vendor-endorsed or tested by us.** Licences, dates and commit hashes are metadata snapshots taken 2026-08-23. "Build status" is *not determinable* for any entry — we did not build anything, and say so rather than guessing. Treat the whole table as leads.

Machine-readable form: [`catalog.json`](catalog.json).

---

## 1. Highest-value projects

Six entries that answer questions this documentation set has open. Read this section even if you skip the rest.

### 1.1 `nkinnan` — as-shipped firmware + SD card contents, and the clone-board discovery

| | |
|---|---|
| **Repos** | [`nkinnan/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8_and_Guition-K5-Knob-Series-JC3636K518`](https://github.com/nkinnan/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8_and_Guition-K5-Knob-Series-JC3636K518) @ `a7401232f5` · [`nkinnan/manufacturer-firmware-and-sd-card-contents_Guition-K5-Knob-Series-JC3636K518`](https://github.com/nkinnan/manufacturer-firmware-and-sd-card-contents_Guition-K5-Knob-Series-JC3636K518) @ `cee5b94c63` |
| **Author** | nkinnan |
| **Last push** | 2025-09-05 |
| **Framework** | ESPHome (YAML) / firmware blobs + PowerShell |
| **Licence** | **none declared** — and the SD archive contains third-party copyrighted media |
| **Local copy** | **no — deliberately not retained** |

**Why it matters — three separate reasons.**

**(a) It identifies a clone board.** The **Guition K5 Knob Series JC3636K518** is the same product from a different vendor.

> "I wouldn't be surprised if Waveshare and Guition are buying the screens and the housing from the same supplier made on the same production line. There are some very small differences in the PCB between the two of them, enough to know it was re-laid-out […] They are largely identical though, right down to the spot for the battery and the daughter PCB underneath the main PCB, even connected the same way."

**(b) Guition publishes source that Waveshare does not.** The author reports the Guition vendor source (`JC3636K518CN_knob_EN.zip`) appears to be the same application as the Waveshare comprehensive example:

> "The JC3636K518 source code seems to be identical to the shipping Waveshare firmware (or at least an older version of it, I've seen youtube videos showing an identical UI). I have no idea how that happened, I doubt they re-implemented it."

If accurate, **this is the closest thing to source for the factory UI that exists publicly** — directly relevant to the "no source for the comprehensive example" gap. **We could not retrieve it**: `pan.jczn1688.com` is a JavaScript file manager, the direct link returns HTML, and Cloudreve API paths 404. Needs a browser session.

~~~
https://pan.jczn1688.com/s/54f682          (file: JC3636K518CN_knob_EN.zip)
https://pan.jczn1688.com/directlink/1/HMI%20display/JC3636K518CN_knob_EN.zip
~~~

**(c) The as-shipped SD card archive documents four app-asset directories the wiki never mentions** — including evidence of an entire **undocumented tenth app**. Fully analysed in [../factory-demo-apps.md](../factory-demo-apps.md); summary in §2 below.

**One caution and one bonus.** The chip readout in this repo reports the ESP32-U4WDH as *"Dual Core + LP Core, 240MHz"*. That is relevant to the [core-count caveat](../../../../components/espressif/esp32-u4wdh/README.md), but **it is a reading from the Guition clone, not from a Waveshare unit**, and `esptool`'s feature string for U4WDH parts is exactly what that caveat says is unreliable. **It does not settle the question.** The bonus is `chunked_dump_bin.ps1`, a retry-with-4 KB-chunks PowerShell wrapper for `esptool read-flash` — the author found large reads fail on the S3. Useful if your own backup attempts stall.

> **Not retained.** No licence is declared, and `sd_card/` contains commercial anime artwork (Genshin Impact, Honkai) and copyrighted commercial music. Mirroring it is not defensible. Link-only.

---

### 1.2 `svwhisper/lyngdorf-secondary-sleep` — quantifies the secondary MCU's idle draw

| | |
|---|---|
| **Repo** | [`svwhisper/lyngdorf-secondary-sleep`](https://github.com/svwhisper/lyngdorf-secondary-sleep) @ `dfc372fb07` |
| **Last push** | 2026-05-10 · **Framework** ESP-IDF, target `esp32` · **~10 lines of C** |
| **Licence** | **MIT stated in README; no `LICENSE` file present** (GitHub API reports `none`) |
| **Local copy** | ✅ `selected/lyngdorf-secondary-sleep.tar.gz` |

The **only ESP32-U4WDH source we have found anywhere.** Waveshare ships none. It does one thing — `esp_deep_sleep_start()` with no wake source — but it supplies a hard number this documentation lacked:

> "The secondary chip is permanently powered from `3V3` and has no GPIO-controllable enable from the S3 — when left running stock firmware it draws **~50 mA continuously**, dominating idle battery current. […] After flashing, the secondary draws **~10 µA**."

**A 5,000× idle-current reduction, and a design constraint nobody documents:** if your project does not use Bluetooth Classic, the secondary chip is pure battery drain and you cannot switch it off in hardware. Corroborated independently by `joshuacant/BlueKnob` (§1.3), which ships its own deep-sleep image for the same reason.

It also confirms the orientation behaviour from a third party, with a genuinely useful diagnostic:

> "If your flash attempt reports `This chip is ESP32, not ESP32-S3`, you've got the cable in the right orientation for this project."

Its companion [`svwhisper/lyngdorf-knob`](https://github.com/svwhisper/lyngdorf-knob) @ `310b3990cf` (ESP-IDF, no licence) drives a Lyngdorf amplifier from the S3.

---

### 1.3 `joshuacant/BlueKnob` — the best complete reference project

| | |
|---|---|
| **Repo** | [`joshuacant/BlueKnob`](https://github.com/joshuacant/BlueKnob) @ `c71c98ff5b` |
| **Last push** | 2025-10-05 · **7 stars** · ESP-IDF + LVGL + SquareLine Studio |
| **Licence** | **Apache-2.0** (`LICENSE` file present) — the most permissive substantial project found |
| **Local copy** | ✅ `selected/BlueKnob.tar.gz` (33.5 MB) |

A BLE media remote, and **the only project that ships images for both MCUs plus its UI design source**:

- `BlueKnob-ESP32/` — deep-sleeps the secondary at boot (see §1.2)
- `BlueKnob-ESP32S3/` — the application; bundles `esp_lcd_sh8601`, `SensorLib` and `lvgl` as components, each with its licence retained
- `BlueKnob-UI/` — **the complete SquareLine Studio project**, which is exactly what the wiki's SquareLine FAQ fails to provide
- `extras/knob-grip-tpu.stl` — a printable TPU grip ring

**Features exercised:** BLE HID (keyboard + mouse), LVGL UI across four screens, touch gestures, knob, backlight/brightness control, battery gauge, screen-blank and device-sleep timers, hibernation, NVS settings, SquareLine asset pipeline.

Two design decisions worth stealing:

- **The whole UI is rotated 180° in SquareLine**, "to keep the USB C port on the rear of the knob for easier use while charging, **and to avoid any costly software rotation**." Baking rotation into the design instead of rotating framebuffers at runtime is the right call on this hardware.
- **Staged power-down**: screen blank → device sleep → hibernation after 30 min, where hibernation requires a physical power-cycle. A pragmatic answer to §1.2's problem.

Its build matrix includes `sdkconfig.ci.esp32_singlecore` with `CONFIG_FREERTOS_UNICORE=y`, i.e. the author treats the secondary's core count as **something to build defensively around** rather than something known — consistent with our unresolved caveat.

---

### 1.4 `UnkMihai` — display controller, with an important caveat

| | |
|---|---|
| **Repo** | [`UnkMihai/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-first-successful-screen-test`](https://github.com/UnkMihai/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-first-successful-screen-test) @ `3cd890b473` |
| **Last push** | 2026-02-20 · Arduino sketch + `esp_lcd_sh8601` driver |
| **Licence** | **MIT stated in README; no `LICENSE` file** (API reports `none`) |
| **Local copy** | ✅ `selected/Waveshare-…-first-successful-screen-test.tar.gz` |

Bears directly on the **ST77916-vs-SH8601 conflict** tracked in [../gaps-and-conflicts.md](../gaps-and-conflicts.md). The author argues from binary analysis of `WX-ESP32S3-KNOB_V1.2.bin` that the SH8601 path is correct:

| Author's "wrong" | Author's "correct" |
|---|---|
| `Arduino_ST77916` / `Arduino_GFX` | `esp_lcd_sh8601` |
| 8-bit SPI commands | **32-bit QSPI command frames** |
| 20 MHz | **40 MHz** |

~~~c
.pclk_hz        = 40 * 1000 * 1000,
.lcd_cmd_bits   = 32,     // 32-bit QSPI commands
.lcd_param_bits = 8,
.flags.quad_mode = true,
~~~

**⚠️ Read this before trusting the repo's pin table.** The README describes the board as a **1.85-inch round AMOLED (`H0185Y040X`) on "ESP32-S3-KNOB V1.1"** — that is a *different Waveshare product*, the AMOLED sibling, not the 1.8-inch LCD this folder documents. The author appears to have conflated two boards. Checking the pins against our schematic-derived table:

| Signal | Repo | Our record | Verdict |
|---|---|---|---|
| LCD CS / SCLK / D0-D3 / RST / BL | 14 / 13 / 15,16,17,18 / 21 / 47 | identical | ✅ **matches** |
| Encoder A / B / SW | 9 / 10 / 8 | knob 1 is GPIO **8/7** | ❌ **conflicts** |
| `POWER_EN` | 5 | GPIO5 is part of the **SDMMC** group (2-6, 42) | ❌ **conflicts** |

So the **display half is consistent with our board and usable**; the **encoder and power pins are not** and look imported from the other product. Use the QSPI parameters, ignore the rest. The `H0185Y040X` / AMOLED identification should **not** be read across to this board.

---

### 1.5 `IngoDuesentrieb/esp32-s3-knob-hardware-explorer` — a peripheral test app with a real licence

| | |
|---|---|
| **Repo** | [`IngoDuesentrieb/esp32-s3-knob-hardware-explorer`](https://github.com/IngoDuesentrieb/esp32-s3-knob-hardware-explorer) @ `87602cacde` |
| **Last push** | 2026-05-10 · PlatformIO / C++ · 10 files |
| **Licence** | **MIT, `LICENSE` file present** ✅ |
| **Local copy** | ✅ `selected/esp32-s3-knob-hardware-explorer.tar.gz` |

Small, clean, correctly licensed. Ships **`boards/waveshare_knob_18.json`** — a PlatformIO board definition for this product, which is the single most reusable artifact in the whole catalogue if you prefer PlatformIO to Arduino IDE or raw ESP-IDF. Functionally it is the community answer to Waveshare's eight scattered `0x_*_Test` demos: one app that exercises the hardware.

---

### 1.6 `0015/lvgl_kawaii_face` — a properly packaged IDF component

| | |
|---|---|
| **Repo** | [`0015/lvgl_kawaii_face`](https://github.com/0015/lvgl_kawaii_face) @ `d58e1c8f8e` |
| **Author** | Eric N. (That Project) · **26 stars** · 2026-02-27 |
| **Licence** | **MIT, `LICENSE` file present** ✅ |
| **Local copy** | ✅ `selected/lvgl_kawaii_face.tar.gz` |

Wiki entry 4. An animated-face widget with 17+ expressions, packaged as a real ESP-IDF component (`idf_component.yml`) with a runnable `examples/basic_cycle`. Not board-specific — it is a reusable LVGL component that happens to suit a round panel — which is precisely why it is worth having. Video: <https://www.youtube.com/watch?v=iCm50dTcAtc>.

---

## 2. What the as-shipped SD card revealed

From `nkinnan`'s Guition archive (§1.1). The wiki documents **four** SD directories; the shipped card has **nine**.

| Directory | Files | Documented by wiki? | What it is |
|---|---:|:--:|---|
| `music/` | 8 | ✅ | MP3s — **plus one `.pcm`**, an undocumented raw format the player also handles |
| `mjpeg/` | 9 | ✅ | Video for the MJPEG player |
| `pic/` | 19 | ✅ | `1.jpg`–`19.jpg` for the album |
| `txt/` | 6 | ✅ (partly) | 3 × `.txt` **+ 3 × matching `.sav`** — the reader **persists reading position** per file. Undocumented |
| **`weather/`** | **19** | ❌ | `clear`, `rain`, `snow_day/night`, `thunderstorm_day/night`, `windy_day/night`, `fog_day/night`, `hot`, **`nowifi`** … — **evidence of an entire weather app the wiki never mentions** |
| **`aida64/`** | **18** | ❌ | `001`–`017` + `00_ff0000` — selectable backgrounds for the AIDA64 screen |
| **`clockbg/`** | **14** | ❌ | Theme Clock backgrounds — this is where "**Theme** Clock" gets its name. Includes ring/star masks as raw `.bin` |
| **`night7/`** | **4** | ❌ | `boot.mjpeg`, **`rhythmbg.mjpeg`**, `red_disk.bin`, `disk_mask_240.bin` |
| **`fonts/`** | **5** | ❌ | `SYHT_16`, `SYHT_BOLD_16`, `SYST_BOLD_16`, `UI_FONT_16`, `EX_FONT_16` — **binary bitmap fonts** |

Three consequences:

1. **A tenth app exists.** Nineteen weather-condition graphics including a `nowifi` fallback is not decoration; it is an app with state. Waveshare's §4 lists nine.
2. **`night7/rhythmbg.mjpeg`** — "rhythm background" — is almost certainly the **Spectrum Analyzer's** backdrop, giving that app its own asset directory. Further corroboration for the reconciliation in [../factory-demo-apps.md §3.6](../factory-demo-apps.md).
3. **`fonts/` are binary blobs** (`SYHT` = Source Han Sans, `SYST` = Source Han Serif; the shipped `txt/` files are Chinese). This materially supports the explanation for why a string search of the S3 image found no `spectrum`/`fft`/`vu` label: **the UI's text is rendered from off-chip binary font assets, not from ASCII string tables in the firmware.** A negative string search was never going to find these app names.

---

## 3. Full catalogue

Sorted by last push. **W** = listed by Waveshare §8.8. Licence is the GitHub API's SPDX field; `NOASSERTION` means a licence file exists that GitHub could not classify. **Build status: not determinable for any entry** — nothing here was built or run by us.

| Repo | W | Pinned commit | Author | Last push | Framework | Licence | What it demonstrates |
|---|:-:|---|---|---|---|---|---|
| [muness/roon-knob](https://github.com/muness/roon-knob) | ✅ | `575ec31245` | muness | 2026-08-24 | ESP-IDF | NOASSERTION | **39★, most-starred.** Roon/LMS hi-fi controller: transport, volume, now-playing art |
| [chris023/orion-waveshare-rotary-dial](https://github.com/chris023/orion-waveshare-rotary-dial) | ✅ | `4a32427b56` | Chris Meyer | 2026-08-05 | ESP-IDF | NOASSERTION | Bedside dial for Orion Sleep toppers. **On-device Wi-Fi provisioning, OAuth pairing, OTA** — the only OTA example found |
| [knobby-mtg/knobby-mtg-life-counter](https://github.com/knobby-mtg/knobby-mtg-life-counter) | ✅ | `d1bb49395c` | Mat | 2026-07-30 | Arduino | GPL-3.0 | 29★. MTG life counter; multiplayer counters, knob+touch |
| [Chuck3CZ/WS-Knob-MeteoPlaneRadar](https://github.com/Chuck3CZ/WS-Knob-MeteoPlaneRadar) | | `a62e72b152` | Chuck3CZ | 2026-07-22 | Arduino | NOASSERTION | Weather + ADS-B flight radar port. Wi-Fi APIs, map rendering |
| [EmbeddedWizardGUI/ESP32-S3-Knob-Touch-LCD-1.8-EN](https://github.com/EmbeddedWizardGUI/ESP32-S3-Knob-Touch-LCD-1.8-EN) | ✅ | `b954e10dba` | Embedded Wizard | 2026-07-20 | ESP-IDF | none | **Non-LVGL GUI stack.** Commercial toolchain; proves the panel is drivable outside LVGL |
| [svwhisper/lyngdorf-knob](https://github.com/svwhisper/lyngdorf-knob) | | `310b3990cf` | svwhisper | 2026-07-18 | ESP-IDF | none | Lyngdorf amplifier control |
| [mcix/ESP32-S3-Knob-Thermostat](https://github.com/mcix/ESP32-S3-Knob-Thermostat) | | `b9b06d07a5` | mcix | 2026-07-18 | PlatformIO | none | Plugwise thermostat via Homey Pro local REST API |
| [juggernautwins608/Waveshare-1.8-MTG-Life-Counter](https://github.com/juggernautwins608/Waveshare-1.8-Magic-the-Gathering-Life-Counter) | ✅ | `364dd06125` | Anton Belo | 2026-07-04 | Arduino | **MIT** | MTG counter. **Ships a patched `Arduino_GFX` for the "ST77916 V2" panel** — another data point in the controller dispute |
| [jeager/arcmind-life-counter](https://github.com/jeager/arcmind-life-counter) | | `cd52b54075` | jeager | 2026-06-19 | Arduino | GPL-3.0 | Third independent MTG counter |
| [honzup/waveshare_withrottle_dial](https://github.com/honzup/waveshare_withrottle_dial) | | `6530a65474` | honzup | 2026-06-14 | ESP-IDF + SquareLine | NOASSERTION | JMRI WiThrottle model-railway throttle. **270° speed arc** — good round-UI idiom |
| [svwhisper/lyngdorf-secondary-sleep](https://github.com/svwhisper/lyngdorf-secondary-sleep) | | `dfc372fb07` | svwhisper | 2026-05-10 | ESP-IDF (`esp32`) | MIT (README only) | **§1.2** — secondary-MCU deep sleep, ~50 mA → ~10 µA |
| [IngoDuesentrieb/esp32-s3-knob-hardware-explorer](https://github.com/IngoDuesentrieb/esp32-s3-knob-hardware-explorer) | | `87602cacde` | IngoDuesentrieb | 2026-05-10 | PlatformIO | **MIT** | **§1.5** — peripheral test app + PlatformIO board JSON |
| [Yehiaraslan/7akim-voice](https://github.com/Yehiaraslan/7akim-voice) | | `4ce2ed620e` | Yehia Raslan | 2026-03-19 | Arduino | none | Voice assistant — **the only project using the PDM microphone** |
| [Sandjab/Waveshare-Knob](https://github.com/Sandjab/Waveshare-Knob) | | `81287ed31c` | Sandjab | 2026-03-07 | mixed | none | Docs/skills/projects collection; parallels this folder |
| [RickFBAG/…-lvgl-thermostat](https://github.com/RickFBAG/esp32-s3-knob-touch-lcd-1.8-lvgl-thermostat) | | `ba0629de47` | RickFBAG | 2026-03-06 | PlatformIO + SquareLine | none | Thermostat UI |
| [0015/lvgl_kawaii_face](https://github.com/0015/lvgl_kawaii_face) | ✅ | `d58e1c8f8e` | Eric N. | 2026-02-27 | ESP-IDF component | **MIT** | **§1.6** — 26★ animated face component |
| [RickFBAG/…-lvgl-ui](https://github.com/RickFBAG/esp32-s3-knob-touch-lcd-1.8-lvgl-ui) | | `a0041bfa14` | RickFBAG | 2026-02-20 | PlatformIO + SquareLine | none | Generic LVGL UI scaffold |
| [UnkMihai/…-first-successful-screen-test](https://github.com/UnkMihai/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-first-successful-screen-test) | | `3cd890b473` | UnkMihai | 2026-02-20 | Arduino | MIT (README only) | **§1.4** — QSPI display params. **Pin table partly wrong** |
| [gilphilbert/waveshare_esp32s3_knob_touch_platformio](https://github.com/gilphilbert/waveshare_esp32s3_knob_touch_platformio) | | `73d6063d5e` | gilphilbert | 2026-01-21 | PlatformIO | none | Minimal PlatformIO skeleton (17 files) |
| [ihayri/ESP32-S3-1.8inch-Knob-Display-Development-Board](https://github.com/ihayri/ESP32-S3-1.8inch-Knob-Display-Development-Board) | ✅ | `1bb0f613ef` | iHayri | 2026-01-08 | Arduino | none | Combination-lock demo; unboxing video `d2aSVfH3RDM` |
| [mylesdebastion/…-Demo](https://github.com/mylesdebastion/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-Demo) | | `736f2ded93` | mylesdebastion | 2025-12-11 | mixed | none | Fork/extension of the official demo tree |
| [joshuacant/BlueKnob](https://github.com/joshuacant/BlueKnob) | | `c71c98ff5b` | joshuacant | 2025-10-05 | ESP-IDF + SquareLine | **Apache-2.0** | **§1.3** — best complete reference; both MCUs + UI source |
| [warusuke/…-timer-test](https://github.com/warusuke/ESP32-S3-Knob-Touch-LCD-1.8-timer-test) | | `9a2c934e64` | warusuke | 2025-09-29 | Arduino | none | Minimal timer experiment |
| [nkinnan/…_and_Guition-K5-…](https://github.com/nkinnan/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8_and_Guition-K5-Knob-Series-JC3636K518) | | `a7401232f5` | nkinnan | 2025-09-05 | ESPHome | none | **§1.1** — ESPHome config for board **and clone** |
| [nkinnan/manufacturer-firmware-…_Guition-K5-…](https://github.com/nkinnan/manufacturer-firmware-and-sd-card-contents_Guition-K5-Knob-Series-JC3636K518) | | `cee5b94c63` | nkinnan | 2025-09-05 | blobs + PowerShell | none | **§1.1/§2** — as-shipped firmware + SD card |
| [nkinnan/manufacturer-firmware-…_Waveshare-…](https://github.com/nkinnan/manufacturer-firmware-and-sd-card-contents_Waveshare-ESP32-S3-Knob-Touch-LCD-1.8) | | — | nkinnan | 2025-09-05 | — | none | ⚠️ **EMPTY.** `size: 0`, no branches. Never pushed |
| [zwood425/swubasedatapad](https://github.com/zwood425/swubasedatapad) | | `6c29268a39` | zwood425 | 2025-07-17 | mixed + SquareLine | **MIT** | 5★. Star Wars Unlimited game tracker |
| [VolosR/Knob18Meters](https://github.com/VolosR/Knob18Meters) | ✅ | `c238ebe879` | Volos Projects | 2025-07-29 | Arduino + SquareLine | none | 25★. Analogue-style meter/gauge faces |

### Related but not this board

| Repo | Note |
|---|---|
| [KrX3D/WaveShare-Knob-Esp32S3](https://github.com/KrX3D/WaveShare-Knob-Esp32S3) | Prior ESPHome work, credited by `nkinnan` |
| [ikstema/esphome-guition-jc3636k518c-va](https://github.com/ikstema/esphome-guition-jc3636k518c-va) | ESPHome voice assistant for the **clone** |
| [marcinmajkowski44-ship-it/ESP32S3-1.8-inch-JC3636K518C](https://github.com/marcinmajkowski44-ship-it/ESP32S3-1.8-inch-JC3636K518C) | ESPHome sample for the **clone** |

### Non-repository resources

| Resource | URL | Note |
|---|---|---|
| Volos — "Why This 1.8" Knob Board Is Perfect for Remote Projects" | `https://www.youtube.com/watch?v=8pHF0OAG2TI` | Wiki §8.8 entry 1 |
| **Volos — usage demonstration** | `https://www.youtube.com/watch?v=5G4W3irHkks` | **Different video**, cited by wiki §4 and FAQ 2 as the vendor's own "how to use this product" answer |
| iHayri — unboxing/review/combination lock | `https://www.youtube.com/watch?v=d2aSVfH3RDM` | |
| That Project — animated face | `https://www.youtube.com/watch?v=iCm50dTcAtc` | |
| Embedded Wizard — GUI demo | `https://www.youtube.com/watch?v=hxJjh68Yqro` | |
| Eric Haight — "Planes above you" | `https://www.youtube.com/shorts/44ysoSGY22M` | |
| deskrad.com | `https://deskrad.com/` | ⚠️ **Commercial product site**, not a build guide. Name collides with several unrelated repos |
| Waveshare lithium battery install | `https://www.youtube.com/watch?v=RUIXx_-BYDg` | The *entire* content of wiki §2 |
| Roon Labs forum — ESP32-S3 Knob Hifi Controller | `https://community.roonlabs.com/t/50-esp32-s3-knob-hifi-controller/311363` | |
| Lyrion forum — roon-knob + LMS | `https://forums.lyrion.org/forum/user-forums/3rd-party-hardware/1804977-roon-knob-includes-lms-support` | |
| ESPHome discussion #3253 | `https://github.com/orgs/esphome/discussions/3253` | Via `nkinnan` |
| Home Assistant — "Display knob" | `https://community.home-assistant.io/t/display-knob/905249` | Via `nkinnan` |
| Discord thread | `https://discord.com/channels/429907082951524364/1411734762002845789` | Via `nkinnan`; requires membership |

Broader searches (Reddit, Hackaday, Hackster) surfaced **no** board-specific project not already reachable through the above. Recorded as a negative result so the search is not repeated.

---

## 4. Locally retained copies

In [`selected/`](selected/), fetched **2026-08-23** as GitHub source tarballs **pinned to the commits listed above**. Retention required a permissive licence; the tree was checked for a real `LICENSE` file in each case.

| File | Repo @ commit | Licence basis | Bytes |
|---|---|---|---:|
| `BlueKnob.tar.gz` | joshuacant/BlueKnob @ `c71c98ff5b` | **Apache-2.0, `LICENSE` present** ✅ | 33,507,244 |
| `esp32-s3-knob-hardware-explorer.tar.gz` | IngoDuesentrieb/… @ `87602cacde` | **MIT, `LICENSE` present** ✅ | 16,177 |
| `lvgl_kawaii_face.tar.gz` | 0015/… @ `d58e1c8f8e` | **MIT, `LICENSE` present** ✅ | 16,362 |
| `lyngdorf-secondary-sleep.tar.gz` | svwhisper/… @ `dfc372fb07` | ⚠️ MIT **stated in README only** | 2,494 |
| `Waveshare-…-first-successful-screen-test.tar.gz` | UnkMihai/… @ `3cd890b473` | ⚠️ MIT **stated in README only** | 128,227 |

> ⚠️ The last two declare MIT in prose but ship **no `LICENSE` file**, so GitHub's API reports `none`. A README sentence is a weaker grant than a licence file. Both are retained because the statement is explicit and the code is small, but **if you redistribute, confirm with the author first.**

`BlueKnob` additionally vendors LVGL, SensorLib and `esp_lcd_sh8601` as components; each carries its own upstream licence file, preserved in the tarball.

### Not retained, and why

| Repo | Reason |
|---|---|
| `muness/roon-knob`, `chris023/orion-waveshare-rotary-dial`, `Chuck3CZ/…`, `honzup/…` | `NOASSERTION` — unclassifiable licence |
| `knobby-mtg/…`, `jeager/…` | GPL-3.0 — copyleft; link-only avoids obligations |
| `EmbeddedWizardGUI/…`, `ihayri/…`, `VolosR/…`, `mcix/…`, `svwhisper/lyngdorf-knob`, `Sandjab/…`, `RickFBAG/…` ×2, `gilphilbert/…`, `mylesdebastion/…`, `warusuke/…`, `Yehiaraslan/…` | **No licence declared** — default copyright, no redistribution right |
| `nkinnan/…` ×2 | No licence **and** third-party copyrighted media in `sd_card/` |
| `juggernautwins608/…`, `zwood425/…` | MIT, but large and lower value than what is already retained |

### Reacquisition

~~~sh
# Pinned tarball for any row in the table
curl -L -o NAME.tar.gz https://codeload.github.com/OWNER/REPO/tar.gz/COMMIT

# e.g.
curl -L -o BlueKnob.tar.gz https://codeload.github.com/joshuacant/BlueKnob/tar.gz/c71c98ff5b

# Full history
git clone https://github.com/OWNER/REPO && git -C REPO checkout COMMIT
~~~

---

## 5. Reading the catalogue

- **ESP-IDF and PlatformIO both outnumber bare Arduino IDE** among serious projects, despite the wiki documenting only Arduino IDE and ESP-IDF. A community PlatformIO board definition exists (§1.5).
- **SquareLine Studio is the de-facto UI tool** — seven projects use it, and `BlueKnob` ships a complete project. The vendor's SquareLine FAQ links only a generic tutorial.
- **The display controller question is still open**, but community practice has converged on **QSPI, 32-bit commands, 40 MHz**, whatever the die is called. `juggernautwins608` patches `Arduino_GFX` for an "ST77916 V2"; `UnkMihai` and `BlueKnob` use `esp_lcd_sh8601`. Both work, which suggests the naming dispute matters less than the bus parameters.
- **Almost nobody uses the secondary MCU.** Of 28 repos, the only two that touch it (`lyngdorf-secondary-sleep`, `BlueKnob-ESP32`) exist to **switch it off**. Nothing found reimplements Bluetooth Classic on it, and nothing found uses the inter-MCU UART — so the protocol remains undocumented and the factory ESP32 image remains the only Classic Bluetooth application in existence for this board.
- **Three independent MTG life counters** and two card-game trackers. The round dial's most popular application is tabletop gaming.
- **One project uses the microphone** (`7akim-voice`) and **one does OTA** (`orion-waveshare-rotary-dial`). Both are thin areas.

---

## 6. Addendum 2026-08-24 — non-repository community sources

Found while compiling [../techniques.md](../techniques.md). These are **issue threads, discussions and videos**, not repositories, so they do not appear in §3. Several carry more engineering weight than most of the repositories above, because each one **resolves a specific defect** rather than demonstrating an application.

Metadata retrieved **2026-08-24** via the GitHub REST API, except the Tasmota discussion (GraphQL needs a token; metadata parsed from the rendered page).

| Source | Medium | Author | Date | Evidence type | Establishes |
|---|---|---|---|---|---|
| [arendst/Tasmota discussion #23737](https://github.com/arendst/Tasmota/discussions/23737) | GitHub discussion | Tasmota community | 2025-08-01 | **Working port + tested fix** | **CST816 reset timing 10 ms / 10 ms / 50 ms**, and QSPI display bring-up in a third-party firmware |
| [lewisxhe/SensorLib issue #32](https://github.com/lewisxhe/SensorLib/issues/32) | GitHub issue (closed) | `gilphilbert` | 2026-01-19 → closed 2026-01-22 | **Bug report accepted upstream** | **DRV2605 reports chip ID `0x05`, not `0x03`** — stock SensorLib refuses to init; needs a patched ID check |
| [lvgl-micropython/lvgl_micropython issue #547](https://github.com/lvgl-micropython/lvgl_micropython/issues/547) | GitHub issue (closed) | `d51r3verse` | 2026-03-27 → closed 2026-03-31 | **Reproduced crash + user-supplied artefact** | **SDMMC init crash in MMC mode**, plus a **real directory listing of a factory SD card** — independent corroboration of the app-asset layout in §2 |
| [nishad2m8/WS-1.8-Knob](https://github.com/nishad2m8/WS-1.8-Knob) | GitHub repo | nishad2m8 | created 2025-08-17, last push 2025-10-30 | **Complete working project** | USB HID smart knob (DaVinci Resolve control). PlatformIO/Arduino + LVGL + SquareLine; ships a `lib/` set incl. `lcd_bsp`/`lcd_config`. **No licence declared**, 5 stars |
| [nishad2m8 — "ESP32-S3 Smart Knob … USB HID Control for DaVinci Resolve"](https://youtu.be/ACAmAXBgFy0) | YouTube | nishad2m8 | — | Demonstration | The above project running; the board as a **USB HID input device** — an application shape absent from the other 28 repos |

### Notes on these

**The Tasmota thread is titled "ST77916 Display"** — another data point in the controller dispute tracked in [../gaps-and-conflicts.md](../gaps-and-conflicts.md), and notable because it is a *working port*, not a marketing page. It does not settle the question (see §5), but it is the strongest community evidence for the ST77916 naming so far.

**The three issue threads share a pattern worth stating:** all describe **vendor-code defects that only surface off the happy path** — a reset too short to be reliable, a chip ID the vendor never checked against a real part, and an SD init that crashes a non-vendor stack. The Waveshare demos work well enough to demo and not well enough to build on. Consequences are worked through in [../techniques.md](../techniques.md) §2.1, §4.1 and §6.

**Already catalogued above, listed here only for evidence typing:** the **Volos** videos (§ "Non-repository resources" — [`8pHF0OAG2TI`](https://www.youtube.com/watch?v=8pHF0OAG2TI) from wiki §8.8, and [`5G4W3irHkks`](https://www.youtube.com/watch?v=5G4W3irHkks), cited by the wiki itself as its usage answer) and the **iHayri** unboxing/review/combination-lock video ([`d2aSVfH3RDM`](https://www.youtube.com/watch?v=d2aSVfH3RDM), paired with the `ihayri/…` repo in §3). Both authors are **wiki-listed**; evidence type for all three is **demonstration only** — no defect analysis, no measurements, and none is a substitute for the issue threads above.

---

## Cross-references

- [../techniques.md](../techniques.md) — subsystem-by-subsystem patterns built on these sources
- [../project-ideas.md](../project-ideas.md) — feasibility map derived from the constraints
- [../wiki-resource-links.md](../wiki-resource-links.md) — the vendor's own §8.8 list, unassessed
- [../factory-demo-apps.md](../factory-demo-apps.md) — the preinstalled apps, and the SD-card analysis in §2
- [../dual-mcu-architecture.md](../dual-mcu-architecture.md) — the secondary MCU and the UART link
- [../gaps-and-conflicts.md](../gaps-and-conflicts.md) — the display-controller dispute
- [../development.md](../development.md) — official toolchain
- [../community.md](../community.md) — the earlier, shorter snapshot this supersedes
