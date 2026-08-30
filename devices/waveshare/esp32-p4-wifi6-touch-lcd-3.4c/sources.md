# Sources

> ESP32-P4-WIFI6-Touch-LCD-3.4C / 4C. All retrieved **2026-08-24**.

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | ESP32-P4-WIFI6-Touch-LCD-3.4C wiki | Waveshare | primary | official page | https://www.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-3.4C | 2026-08-24 | unknown | Specs, 3.4in 800×800, feature list, hardware callouts, RTC constraint | Marketing prose; no pin table; no PCB revision | `../esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/source-snapshots/wiki-ESP32-P4-WIFI6-Touch-LCD-3.4C.html` |
| S2 | ESP32-P4-WIFI6-Touch-LCD-4C wiki | Waveshare | primary | official page | https://www.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-4C | 2026-08-24 | unknown | 4in 720×720; otherwise identical text to S1 | Links to the **3.4C** store page; no 4C listing exists | `../esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/source-snapshots/wiki-ESP32-P4-WIFI6-Touch-LCD-4C.html` |
| S3 | Product listing (**both variants**) | Waveshare | primary | store listing | https://www.waveshare.com/esp32-p4-wifi6-touch-lcd-3.4c.htm | 2026-08-24, re-fetched 2026-08-26 | n/a | **SKU 31523 + 31522, both `unsaleable:false`** — decisive for C2/C6; $64.99–$74.99 | Per-SKU price renders client-side, not extractable | `…/source-snapshots/waveshare-product-listing-esp32-p4-wifi6-touch-lcd-xc.html` |
| S4 | 4C store URL probe | Waveshare | primary | store listing | https://www.waveshare.com/esp32-p4-wifi6-touch-lcd-4c.htm | 2026-08-24 | n/a | `HTTP 404` — **no dedicated 4C page, because both variants share one listing** | Accurate observation that was initially **misread**; see C2 | not retained |
| S5 | Waveshare catalogue search | Waveshare | primary | store listing | https://www.waveshare.com/catalogsearch/result/?q=ESP32-P4-WIFI6-Touch-LCD | 2026-08-24 | n/a | Returns **only** the 3.4C | Confirms S4 | not retained |
| S6 | ESP32-P4-WIFI6-Touch-LCD-XC schematic | Waveshare | primary | datasheet | https://files.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-XC/ESP32-P4-WIFI6-Touch-LCD-XC-Schematic.pdf | 2026-08-24 | 2025-05-26 (`Last-Modified`) | ESP32-P4NRW32, ESP32-C6-MINI-1-N4, ES8311, ES7210, CH343P, MP1658, MP1605 | 2-page layout dump; text layer extracts poorly; no clean net list | `../esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/schematic/` |
| S7 | ESP32-P4-WIFI6-Touch-LCD-XC demo archive | Waveshare | primary | repository | https://files.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-XC/ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip | 2026-08-24 | 2025-06-28 (`Last-Modified`) | **All verified pin values**; both JD9365 init tables; DSI timings | 118 MiB; contains unmodified upstream examples that are *not* board-authoritative | archived — see shared record |
| S8 | `Arduino/libraries/displays/displays_config.h` | Waveshare | primary | repository | member of S7 | 2026-08-24 | 2025-05-22 (mtime) | I²C 7/8, `lcd_rst` 27, both panel profiles, `CURRENT_SCREEN` default | Vendor board-support code — strongest evidence available | `…/demo/Arduino/libraries/displays/` |
| S9 | `ESP-IDF/06_displaypanel_3.4inch` | Waveshare | primary | repository | member of S7 | 2026-08-24 | 2025-05-22 (mtime) | 800×800, RST 27, BL 26 active-low, DSI timings | 3.4C only | `…/demo/ESP-IDF/06_displaypanel_3.4inch/` |
| S10 | `ESP-IDF/07_displaypanel_4inch` | Waveshare | primary | repository | member of S7 | 2026-08-24 | 2025-05-22 (mtime) | 720×720, reg `0x40`=`0x04` | 4C only | `…/demo/ESP-IDF/07_displaypanel_4inch/` |
| S11 | `ESP-IDF/05_I2SCodec/main/example_config.h` | Waveshare | primary | repository | member of S7 | 2026-08-24 | 2025 | I²S 13/12/10/9/11, PA 53, I²C 7/8 (P4 branch) | Multi-target file; **read the `CONFIG_IDF_TARGET_ESP32P4` branch only** | `…/demo/ESP-IDF/05_I2SCodec/` |
| S12 | `ESP-IDF/03_sdmmc` | Espressif (shipped by Waveshare) | primary | repository | member of S7 | 2026-08-24 | — | **Nothing about this board** | **Unmodified upstream example**; its P4 defaults are Function-EV-Board values — see C1 | `…/demo/ESP-IDF/03_sdmmc/` |
| S13 | Waveshare MediaWiki API | Waveshare | primary | official page | https://www.waveshare.com/wiki/api.php?action=parse&… | 2026-08-24 | n/a | **PHP fatal error, not JSON** | Documented enumeration method is broken — see C10 | not retained |
| S14 | Espressif Flash Download Tool | Espressif | primary | official page | https://dl.espressif.com/public/flash_download_tool.zip | 2026-08-24 | — | Windows flashing tool linked from both wikis | Unversioned URL, updated in place | archived (knob board record) |

## Pass 7 additions — docs platform

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| S25 | Waveshare Documentation Platform — XC | Waveshare | primary | official page | https://docs.waveshare.com/ESP32-P4-WIFI6-Touch-LCD-XC | 2026-08-24, re-fetched 2026-08-26 | **SKUs**; "dual microphones"; 40-pin needs **adapter**; BOOT button; **vendor warning against Arduino on P4** | `…/source-snapshots/waveshare-docs-platform-esp32-p4-wifi6-touch-lcd-xc.html` |

This modern platform supersedes the legacy MediaWiki wiki in practice and, unlike it, is not
broken ([C10](./gaps-and-conflicts.md#c10--waveshare-mediawiki-api-is-broken)). It should be the
first stop for future Waveshare research.

## Pass 10 additions — Chinese-language sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| S26 | 微雪电子 CN storefront | Waveshare | primary | store listing | https://www.waveshare.net/shop/ESP32-P4-WIFI6-Touch-LCD-3.4C.htm | 2026-08-26 | **28 GPIOs on the 40-pin header**; **170° viewing angle**; **optically bonded tempered glass**; dual mics with AEC; 版本选择 = both variants | Prices render client-side | `…/source-snapshots/waveshare-cn-shop-esp32-p4-wifi6-touch-lcd-3.4c.html` |
| S27 | Waveshare CN wiki | Waveshare | primary | official page | https://www.waveshare.net/wiki/ESP32-P4-WIFI6-Touch-LCD-3.4C | 2026-08-26 | `HTTP 200` — a CN wiki exists in parallel | Not yet mined | not retained |

**The Chinese material carries specifications the English material does not.** The 28-GPIO count,
the 170° viewing angle and the optically bonded panel appear only there. The GPIO count
independently corroborates the schematic-derived `J8` mapping — see
[`pinouts-and-buses.md`](./pinouts-and-buses.md#independently-confirmed-28-signal-pins).

It also **independently confirms C2** from a separate storefront: 版本选择 ("version selection")
offers 3.4 英寸 and 4 英寸 as options of one product.

> Reusable lesson for this vendor: **check `waveshare.net` (CN) as well as `waveshare.com`.** They
> are not translations of each other — the CN listing is more specific about the hardware.
> `docs.waveshare.com/zh/…` returns `404`, so the CN content lives on the separate `.net` host.

## Pass 6 — official repository and community (2026-08-24)

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| S15 | ESP32-P4-WIFI6-Touch-LCD-XC repository | Waveshare | primary | repository | https://github.com/waveshareteam/ESP32-P4-WIFI6-Touch-LCD-XC | 2026-08-24 | **Apache-2.0 licence**; HEAD `6948676d6451`; supersedes the ZIP | — |
| S16 | `docs/HARDWARE.md` | Waveshare | primary | repository | raw.githubusercontent.com/…/main/docs/HARDWARE.md | 2026-08-24 | **Independent confirmation of every pin**; GT9271; GD25Q256; **rev1.1**; DSI PHY profiles | `…/source-snapshots/github/HARDWARE.md` |
| S17 | `docs/FIRMWARE.md` | Waveshare | primary | repository | …/main/docs/FIRMWARE.md | 2026-08-24 | Factory images for both variants; rev3.x-only profiles; build flow | `…/github/FIRMWARE.md` |
| S18 | `docs/COMPONENTS.md` | Waveshare | primary | repository | …/main/docs/COMPONENTS.md | 2026-08-24 | Exact dependency pins; touch contract; BSP `3.0.1` | `…/github/COMPONENTS.md` |
| S19 | `docs/GETTING_STARTED.md` | Waveshare | primary | repository | …/main/docs/GETTING_STARTED.md | 2026-08-24 | **ESP-IDF v5.5.5 / v6.0.2** CI matrix | `…/github/GETTING_STARTED.md` |
| S20 | `docs/TROUBLESHOOTING.md` | Waveshare | primary | repository | …/main/docs/TROUBLESHOOTING.md | 2026-08-24 | Arduino `Serial` is USB CDC, not CH343P | `…/github/TROUBLESHOOTING.md` |
| S21 | BSP component registry entry | Waveshare / Espressif | primary | repository | https://components.espressif.com/components/waveshare/esp32_p4_wifi6_touch_lcd_xc | 2026-08-24 | Versions `0.0.1`→`3.0.1`; **Apache-2.0** | — |
| S22 | `EmbeddedWizardGUI/ESP32-P4-WIFI6-Touch-LCD-3.4C` | Embedded Wizard | community | repository | https://github.com/EmbeddedWizardGUI/ESP32-P4-WIFI6-Touch-LCD-3.4C | 2026-08-24 | **Non-LVGL GUI stack** on this exact board; 4 stars | — |
| S23 | `Arno-Z/WaveShare-ESP32-P4-Claude-Desktop-Buddy` | Arno-Z | community | repository | https://github.com/Arno-Z/WaveShare-ESP32-P4-Claude-Desktop-Buddy | 2026-08-24 | BLE on the 3.4C; MIT; 1 star | — |
| S24 | GitHub org search `waveshareteam ESP32-P4-WIFI6` | GitHub | primary | repository | api.github.com/search/repositories | 2026-08-24 | **7-board product family**: 3.5, 4.3, 4B, 5, 7B, X, XC | — |

## Source-class summary

Passes 1–5 were entirely **primary** vendor material. Pass 6 added Waveshare's official repository
— still primary, but **independently authored** from the wiki and schematic, which is why its
agreement on the pin map carries real weight.

Two **community** sources (S22, S23) now exist for the 3.4C, correcting the earlier "no community
evidence" finding. Both are small. **Zero** community sources target the 4C.

Still absent across all passes: forums, blogs, videos, reviews, teardowns, owner photographs,
non-English sources, and regulatory records.

## Evidence hierarchy used

Where sources disagree, this record prefers, in order:

1. **Waveshare's own board-support code** (S8, S9, S10, S11) — what the vendor actually ships and
   builds against.
2. **Schematic** (S6) — authoritative for fitted parts, poor for net tracing as extracted.
3. **Wiki prose** (S1, S2) — accurate for feature presence, silent on pins.
4. **Bundled upstream examples** (S12) — **explicitly distrusted** for board-specific values.

That fourth rule is why the microSD pins are recorded as unknown rather than as 44/43/39.
