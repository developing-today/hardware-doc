# Xteink X3 — projects

> From the **~200-repository** GitHub census, 2026-09-04. Owner reports are in
> [`community.md`](community.md). The shared ecosystem is documented once, in
> [`../x4/projects-and-community.md`](../x4/projects-and-community.md) — this page
> covers what is **X3-specific**.

## The X3's position in the ecosystem

Almost every project says *"for the Xteink X3 and X4"*. The X3 shares its SoC,
board layout, ADC ladder and shared-SPI design with the X4, and **one C3 binary
serves both** — `XteinkDetect` fingerprints the I²C bus at boot. So X3 support is
usually a by-product of X4 support rather than separate work.

**Except for the panel.** The X3's UC8253 (and now UC8279d) is unique in the
family, and that is where X3-specific effort concentrates.

## X3-specific projects

| Project | Why it is X3-specific |
|---|---|
| [`anki630/crossmosa`](https://github.com/anki630/crossmosa) + [`crossmosa-freeink-sdk`](https://github.com/anki630/crossmosa-freeink-sdk) | ★25. 繁體中文 firmware **and its own SDK fork doing "UC8279 waveform tuning"** — **the only project anywhere working the new X3 panel** |
| [`emezrahi/XTeink-X3-Supafast`](https://github.com/emezrahi/XTeink-X3-Supafast) | Refresh-speed work on the X3 |
| [`kocha01/xteink-x3-pokiink-fw`](https://github.com/kocha01/xteink-x3-pokiink-fw) | PokiInk — an X3 CrossPoint fork |
| [`smalltomatowater-boop/crosspoint-reader-x3`](https://github.com/smalltomatowater-boop/crosspoint-reader-x3) | Japanese UI (Migu1M) **+ a tmux terminal** |
| [`hannah-nula/crosspoint-x3-ble-page-turner`](https://github.com/hannah-nula/crosspoint-x3-ble-page-turner) | *"validated BLE page-turner **reconnect** support"* — implying default reconnect is fragile |
| [`sermelipharo/x3-trmnl`](https://github.com/sermelipharo/x3-trmnl) | **TRMNL BYOD** firmware on the CrossPoint HAL |
| [`evanstoddard/xteink_x3_zephyr`](https://github.com/evanstoddard/xteink_x3_zephyr) | **Zephyr RTOS** — the only non-Arduino/non-IDF attempt in the family |
| [`wiltodelta/xteink-sugartv`](https://github.com/wiltodelta/xteink-sugartv) | Turns an X3 into a **continuous glucose monitor display** for Home Assistant |
| [`padge01/xteink-pokemon-game`](https://github.com/padge01/xteink-pokemon-game) | *"reading-powered Pokemon companion game for the Xteink X3, built on CrossInk"* |
| [`CraigBell/xteink-x3-home-assistant-dashboard`](https://github.com/CraigBell/xteink-x3-home-assistant-dashboard) | HA dashboard |
| [`Eleecho/CrossInk-XTEInk3-ImageTuning`](https://github.com/Eleecho/CrossInk-XTEInk3-ImageTuning) | `.bmp` rendering tweaks |
| [`twil09/xteinkos`](https://github.com/twil09/xteinkos) | *"Custom made OS for the Xteink X3 E-reader"* |
| [`dm807cam/xteink3-bible`](https://github.com/dm807cam/xteink3-bible) | BSB as 66 per-book EPUBs, formatted for small screens |
| [`nerderer/xteink-x3-somatic-cards`](https://github.com/nerderer/xteink-x3-somatic-cards), [`lmagdanello/xteink-x3-extension`](https://github.com/lmagdanello/xteink-x3-extension), [`twbeatles/xteink-x3-websync`](https://github.com/twbeatles/xteink-x3-websync) | Content and sync tooling |
| [`sunwoods/Xteink-X3`](https://github.com/sunwoods/Xteink-X3) | **Not software** — the Chinese hardware census and schematic sketch archived in this record |
| [`ElendilDrac01/xteink-x3-calibre-stock`](https://github.com/ElendilDrac01/xteink-x3-calibre-stock) | Calibre plugin for **stock** firmware — useful if you do not want to reflash |

## The tooling that matters most for the X3

[`zocs/eink-quick-flasher`](https://github.com/zocs/eink-quick-flasher) — ★12,
MIT, Python GUI. It is the best-documented X3 tool in existence:

- **1:1 full-flash backup and restore in ~2 minutes**, auto COM detection.
- Ships **stock images**: `x3_en_v1.0.7_full.bin`, `x3_en_v5.2.13_full.bin`,
  `x3_cn_v5.2.13_full.bin`, `x3_cn_v5.2.13_ota.bin`.
- Carries an `X3-FLASHER-GUIDE` in **both English (13.6 KB) and Chinese
  (16.7 KB)**.

**The X3 is the only Xteink with published full-flash stock images.** The X4 has
only OTA images there (plus the separate community dump this repo archived); the
X4 Pro and X4 Classic have nothing.

## The panel-variant problem, in project terms

Units shipped from ~July 2026 carry a **UC8279d**. CrossPoint 1.5 (2026-08-07)
was the release that added support — *"this release **DOES support the new x3
display variants** that a few of you have received"* — with the warning that
*"Other forks will need to pull the latest SDK to avoid **soft bricking locked
units**"*.

**Practical rule:** on a recently-purchased X3, use CrossPoint ≥ 1.5, CrossInk
≥ 1.5, or a fork synced to a current FreeInk SDK. An older fork may leave a blank
screen or worse.

Only `crossmosa-freeink-sdk` is actively tuning UC8279 waveforms; until that
lands, newer X3s likely run a **full GC-style flash on every page turn** and have
**no grayscale**. See [`features/display.md`](features/display.md).

## Known X3 failure modes with named causes

| Failure | Cause | Fix |
|---|---|---|
| **OTA out-of-memory** | No PSRAM on the ESP32-C3 | CrossPoint stopped using GitHub releases; reflash from the web flasher (unlocked) or SD (locked) |
| Blank screen after flashing | UC8279d unit + firmware without that driver | CrossPoint ≥ 1.5 |
| Soft brick on a locked unit | Fork on a stale SDK | Pull the current SDK |
| Battery drain through sleep | Firmware not declaring the **GPIO13 SD rail** | Declare it; `powerDownRailsForSleep()` then cuts the card |

## See also

[`../x4/projects-and-community.md`](../x4/projects-and-community.md) — the shared
ecosystem: mainlines, flashers, `.XTC` converters, font tooling, localisation,
community service sites.
