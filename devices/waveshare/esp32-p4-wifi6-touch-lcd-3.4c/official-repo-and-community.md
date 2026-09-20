# Official repository, BSP and community references

> ESP32-P4-WIFI6-Touch-LCD-3.4C / 4C. Retrieved **2026-08-24**.
>
> **This page supersedes the demo ZIP as the primary software source.** The ZIP is a snapshot;
> the repository below is maintained, version-controlled, CI-tested and **Apache-2.0 licensed**.

## 1. Waveshare's official repository

| Field | Value |
|---|---|
| Repository | **<https://github.com/waveshareteam/ESP32-P4-WIFI6-Touch-LCD-XC>** |
| Description | "ESP32-P4-WIFI6-Touch-LCD-3.4C/4C Engineering Code Examples" |
| **License** | **Apache-2.0** |
| Default branch | `main` |
| Created | 2026-02-09 |
| Last push | 2026-08-21 |
| HEAD at retrieval | `6948676d6451` — *"Merge pull request #6 from waveshareteam/chore/esp-idf-ci"* |
| Stars / forks | 9 / 7 |
| Size | ~111 MB |

Layout: `docs/` (16 files, **bilingual EN + 中文**), `examples/{esp-idf,arduino}/`, `firmware/`,
`hardware/schematics/`, `scripts/`, plus `CONTRIBUTING`, `SUPPORT` and CI under `.github/`.

### Why this matters more than the ZIP

1. **It resolves the licence question.** The demo ZIP contains no `LICENSE`; the repository is
   explicitly **Apache-2.0**. See [C7](./gaps-and-conflicts.md#c7--demo-licence--resolved-2026-08-24).
2. **It is newer and reorganised.** Example numbering differs from the ZIP — the repo has
   `05_sdmmc`, `07_Displaycolorbar`, `08_lvgl_demo_v9`, `09_video_lcd_display`, `10_mp4_player`,
   `11_esp_brookesia_phone`, `12_usb_extend_screen`.
3. **It has real CI** validating ESP-IDF **v5.5.5** and **v6.0.2** plus an Arduino build matrix.
4. **It ships factory firmware** for both variants.
5. **It documents the hardware contract** in `docs/HARDWARE.md`, which independently confirms
   every pin this repository read off the schematic.

```bash
git clone https://github.com/waveshareteam/ESP32-P4-WIFI6-Touch-LCD-XC.git
cd ESP32-P4-WIFI6-Touch-LCD-XC && git checkout 6948676d6451   # pin for reproducibility
```

## 2. The official BSP is a published component

The single most useful thing found in this pass. Waveshare maintain a real board-support package
on Espressif's component registry — the demo ZIP never mentions it.

| Field | Value |
|---|---|
| Component | **`waveshare/esp32_p4_wifi6_touch_lcd_xc`** |
| Registry | <https://components.espressif.com/components/waveshare/esp32_p4_wifi6_touch_lcd_xc> |
| Published versions | `0.0.1`, `2.0.0`, `2.0.1`, `3.0.0`, **`3.0.1`** |
| Pinned by Waveshare | **exactly `3.0.1`** |
| Licence | Apache-2.0 |

```yaml
dependencies:
  waveshare/esp32_p4_wifi6_touch_lcd_xc: "3.0.1"
```

Display variant is selected by BSP macro, **not** by editing resolution constants:

| Variant | Macro |
|---|---|
| 3.4C | `BSP_LCD_TYPE_800_800_3_4_INCH` |
| 4C | `BSP_LCD_TYPE_720_720_4_INCH` |

Waveshare are explicit that manifests must pin a **published registry version** — not a Git URL,
not a local path, not an unpublished version — because the Component Registry packaging flow
rejects those forms.

The BSP source is **resolved by the Component Manager and is not vendored** in the repository.

## 3. Factory firmware exists

My earlier `development.md` stated Waveshare publish no factory image. **That was wrong.**

| File | Bytes | Profile |
|---|---:|---|
| `firmware/ESP32-P4-WIFI6-Touch-LCD-3.4C-FactoryOnly-260821.bin` | 16,777,216 | `3_4c`, 800 × 800 |
| `firmware/ESP32-P4-WIFI6-Touch-LCD-4C-FactoryOnly-260821.bin` | 16,777,216 | `4c`, 720 × 720 |

Both are 16 MiB merged images dated `260821`. `scripts/Flash-CI-Firmware.ps1` and
`Flash-CI-Firmware.cmd` are the supplied flashing helpers. Source is `firmware/brookesia/`, an
ESP-Brookesia project.

Build profiles are **rev3.x only, 32 MB flash only**:

```bash
cd firmware/brookesia
idf.py -B build-3_4c-rev3_x \
  -D SDKCONFIG_DEFAULTS="sdkconfig.defaults;sdkconfig.defaults.rev3_x;sdkconfig.defaults.3_4c" build
```

Never reuse a generated `sdkconfig`, `managed_components/` or `dependencies.lock` between
profiles. Combined images must come from their own profile build, never a copied or padded
whole-flash image.

**That separate, CI-built, named 4C firmware image is the strongest evidence yet that the 4C is a
real product** — see [C2](./gaps-and-conflicts.md#c2--4c-availability--resolved-2026-08-24).

## 4. Corrections and additions to this repository's records

`docs/HARDWARE.md` confirmed every GPIO read from the schematic — GPIO27 reset, GPIO26 backlight,
GPIO7/8 I²C, GPIO23 `TP_RST`, `TP_INT`→TP2 only, SD on 39–44, audio on 9–13 + PA 53. Two
independent sources agreeing is as strong as evidence gets short of hardware.

It also **corrected and extended** several things:

| Item | Previously recorded | Actual |
|---|---|---|
| Touch controller | GT911 | **GT9271**, driven by a GT911-*compatible* API |
| Flash part | "32 MB NOR" | **GD25Q256** |
| PCB revision | unknown ([C3](./gaps-and-conflicts.md#c3--pcb-revision--resolved-2026-08-24)) | **rev1.1** |
| Factory firmware | "none published" | **Published for both variants** |
| ESP-IDF version | `^5.0`, inferred 5.3+ | **v5.5.5 and v6.0.2**, both CI-tested |
| Touch I²C address | unknown | probe **`0x5D`** then **`0x14`**, use whichever answers |
| Audio pins | code-only evidence | **confirmed** by the BSP contract |
| DPI clock | not established | **80 MHz** |

### ESP32-P4 silicon revision affects the DSI PHY clock

Not previously documented here, and a genuine trap:

- **Pre-v3** silicon uses the legacy **PLL_F20M** DSI PHY reference.
- **rev3.x** uses **XTAL**.
- Waveshare leave **`.phy_clk_src = 0`** so ESP-IDF selects from the active silicon profile.
- The DPI pixel clock stays **80 MHz** either way; both displays use 2 lanes at 1500 Mbps.

Waveshare's audit rule: *"never force the legacy PLL_F20M source for a rev3.x build."*

`rev1_3` and `rev3_x` are **ESP32-P4 silicon compatibility profiles, not PCB revisions** — easy to
misread as board versions.

### Exact dependency pins

Waveshare pin these deliberately; copying them saves real debugging:

| Component | Constraint | Reason given |
|---|---|---|
| `esp_wifi_remote` / `esp_hosted` | ESP-IDF 6: `>=1.6,<2.0` / `>=2.12,<3.0` · ESP-IDF 5.5: `0.14.*` / `1.4.*` | Hosted-Wi-Fi ranges differ per IDF line |
| `esp_video` | `~2.0` | Camera + display pipeline |
| `esp_audio_codec` | **`2.5.0`** | **2.6+ requires ESP32-P4 rev ≥ 3.0**, breaking the `rev1_3` profile |
| LVGL | `^9.*`, Brookesia uses **`9.5.0`** | — |
| `espressif/tinyusb` | **`0.17.0~2`** | Exact release permitted by `usb_device_uac 1.2.0`; prevents silent USB descriptor / P4 PHY changes |

### Arduino serial is Hardware CDC, not the CH343P

From `docs/TROUBLESHOOTING.md`: for the tested Arduino FQBN, sketch `Serial` uses **Hardware CDC on
the Type-C USB port**, *not* the CH343P Type-C UART. Start the sketch with the monitor closed;
missing startup lines are expected because the non-blocking logger drops them.

This is exactly the sort of thing that wastes an afternoon.

## 5. The product family is much larger than two boards

`ESP32-P4-WIFI6-Touch-LCD` is a **family**, not a pair. Waveshare maintain a repository per board:

| Repository | Stars | Last push | Scope |
|---|---:|---|---|
| `ESP32-P4-WIFI6-Touch-LCD-7B` | 33 | 2026-08-21 | 7-inch |
| `ESP32-P4-WIFI6-Touch-LCD-X` | 13 | 2026-08-21 | "X" family |
| `ESP32-P4-WIFI6-Touch-LCD-4.3` | 11 | 2026-08-21 | 4.3-inch |
| **`ESP32-P4-WIFI6-Touch-LCD-XC`** | **9** | **2026-08-21** | **3.4C + 4C — this record** |
| `ESP32-P4-WIFI6-Touch-LCD-5` | 8 | 2026-08-20 | 5-inch |
| `ESP32-P4-WIFI6-Touch-LCD-3.5` | 5 | 2026-08-21 | 3.5-inch |
| `ESP32-P4-WIFI6-Touch-LCD-4B` | 1 | 2026-08-21 | 4B |

Note the naming pattern: **`XC` = the round-display pair**, matching the `X`/`XC` wildcard
convention on the file host. All seven were pushed within two days of each other, suggesting a
coordinated documentation effort in August 2026.

## 6. Community projects

Modest but real — which corrects [C9](./gaps-and-conflicts.md#c9--community-evidence--resolved-2026-08-26)
from "no community evidence" to "a small, identifiable community".

### Specifically targeting the 3.4C

| Project | Stars | Last push | Licence | What it demonstrates |
|---|---:|---|---|---|
| [`EmbeddedWizardGUI/ESP32-P4-WIFI6-Touch-LCD-3.4C`](https://github.com/EmbeddedWizardGUI/ESP32-P4-WIFI6-Touch-LCD-3.4C) | 4 | 2026-07-20 | none stated | **Embedded Wizard GUI** on the 3.4C — a commercial GUI toolchain as an alternative to LVGL |
| [`Arno-Z/WaveShare-ESP32-P4-Claude-Desktop-Buddy`](https://github.com/Arno-Z/WaveShare-ESP32-P4-Claude-Desktop-Buddy) | 1 | 2026-04-23 | MIT | **BLE** integration on the 3.4C |

The Embedded Wizard project is the more interesting of the two: it is evidence that a **non-LVGL**
GUI stack has been brought up on this exact board, which no vendor material mentions.

### Family-adjacent (different board, transferable technique)

| Project | Stars | Board | Note |
|---|---:|---|---|
| [`chvvkumar/ESP32-P4-NINA-Display`](https://github.com/chvvkumar/ESP32-P4-NINA-Display) | 45 | **4B** | Astrophotography (NINA) display. Most-starred P4 display project found — **not** the 3.4C/4C |
| [`RTechAI/ESP32-P4-LVGL-Boilerplate-3`](https://github.com/RTechAI/ESP32-P4-LVGL-Boilerplate-3) | 10 | **7B** | "Production-ready" LVGL + ESP-IDF boilerplate |
| [`blk96gt/ha_esp32_dashboard`](https://github.com/blk96gt/ha_esp32_dashboard) | 4 | **7B** | Home Assistant dashboard |

Do **not** treat these as 3.4C/4C evidence — different panels, different BSP variant. They are
useful as technique references only.

### Honest reading of community size

Seven identifiable projects across the whole P4 display family; **two** target the 3.4C, **zero**
target the 4C. Star counts are single- and low-double digits. This is an **early, small community**
around a recent product line — enough to prove people are building real things, not enough to
expect answers to be already written down.

Still **no** forum threads, blog posts, videos, teardowns or owner photographs were located, and
no evidence at all of a physical 4C in anyone's hands.

## 7. What to do differently as a result

1. **Use the BSP**, not hand-rolled pin constants:
   `waveshare/esp32_p4_wifi6_touch_lcd_xc: "3.0.1"` and select the display macro.
2. **Clone the repository**, don't work from the ZIP. It is newer, licensed, and CI-tested.
3. **Target ESP-IDF v5.5.5 or v6.0.2** — the two versions actually validated.
4. **Copy the dependency pins** above, especially `esp_audio_codec 2.5.0` and `tinyusb 0.17.0~2`.
5. **Flash the factory image first** to establish a known-good baseline.
6. Remember **`Serial` is USB CDC** on Arduino, not the CH343P UART.

## 8. A second, better documentation platform

Waveshare have a modern documentation site that the legacy MediaWiki wiki does not link
prominently:

**<https://docs.waveshare.com/ESP32-P4-WIFI6-Touch-LCD-XC>** — `HTTP 200`, English + 中文,
covering the whole ESP32-P4 line (Core-DEV-KIT, ETH, Module-DEV-KIT, NANO, Pico, WIFI6,
WIFI6-DEV-KIT, WIFI6-POE-ETH, and all seven Touch-LCD boards).

It supersedes the old wiki in practice and, unlike it, **is not broken** — recall the MediaWiki API
returns a PHP fatal error ([C10](./gaps-and-conflicts.md#c10--waveshare-mediawiki-api-is-broken)).

Details found only there:

| Detail | Value |
|---|---|
| **SKUs** | 3.4C = **31523**, 4C = **31522** |
| **Microphones** | **"dual microphones (with echo cancellation)"** — plural, where the old wiki says "microphone" |
| **40-pin header** | 2.54 mm pitch, *"compatible with some Raspberry Pi HATs (**requires pin header adapter**)"* |
| **BOOT button** | *"Press during power-up or reset to enter download mode"* |
| Framing | Both panels presented as *options of one product*, matching the store's Version Options |

### Waveshare's own warning about Arduino

> ⚠️ *"ESP32-P4 currently has limited adaptation on the Arduino platform. To ensure development
> stability, it is recommended to use ESP-IDF for development at this stage."*

That is the **vendor** steering people away from Arduino on this chip. Worth weighing before
starting an Arduino project here, notwithstanding that they ship Arduino examples and CI.

### PSRAM speed differs by silicon profile

| Profile | PSRAM | Arduino FQBN |
|---|---|---|
| `rev3_x` (default) | **250 MHz** | `ChipVariant=postv3` |
| `rev1_3` (pre-v3 compatibility) | **200 MHz** | — |

Waveshare state **`rev1_3` and `rev3_x` binaries are incompatible**. Combined with
[C14](./gaps-and-conflicts.md#c14--esp32-p4-silicon-revision-changes-the-dsi-phy-clock-source),
the silicon profile is a first-class build decision on this board, not a detail.

## Sources

All retrieved 2026-08-24 via the GitHub REST API and `raw.githubusercontent.com`, plus the
Espressif component registry API. Local snapshots of the four key docs are in
[`../esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/source-snapshots/github/`](../esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/source-snapshots/github/).
