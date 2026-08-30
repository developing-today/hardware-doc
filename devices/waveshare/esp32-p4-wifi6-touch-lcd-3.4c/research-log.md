# Research log

> ESP32-P4-WIFI6-Touch-LCD-3.4C / 4C. Single pass, **2026-08-24**.
> This is a reproducible broad-coverage snapshot, not proof no other resource exists.

## Pass 1 — vendor identity and downloads

| # | Source/service | Action | Result | Disposition |
|---|---|---|---|---|
| 1 | waveshare.com/wiki | GET `ESP32-P4-WIFI6-Touch-LCD-3.4C` | `HTTP 200`, 98,314 B | **Useful** → S1, snapshotted |
| 2 | waveshare.com/wiki | GET `ESP32-P4-WIFI6-Touch-LCD-4C` | `HTTP 200`, 98,607 B | **Useful** → S2, snapshotted |
| 3 | waveshare.com/wiki | MediaWiki API `action=parse&prop=wikitext` for both | `HTTP 200` but **109 B PHP fatal error** | **Failed** → C10; worked around |
| 4 | rendered wiki HTML | regex `https?://…\.(zip\|7z\|pdf\|rar\|bin\|apk\|exe)` | 4 URLs (3.4C), 5 URLs (4C) | **Useful** — recovered all downloads |
| 5 | files.waveshare.com | HEAD schematic + demo | Both `HTTP 200`; `Content-Length` matched local bytes exactly | **Verified** |
| 6 | files.waveshare.com | GET both | 1,869,787 B + 117,768,225 B; magic validated | **Retained** |

Query family used: exact product names, the `XC` family wildcard, and file-extension patterns.

## Pass 2 — commercial status

| # | Source | Action | Result | Disposition |
|---|---|---|---|---|
| 7 | waveshare.com | GET `/esp32-p4-wifi6-touch-lcd-3.4c.htm` | `HTTP 200`; **$64.99 – $74.99**; 5 option slugs | **Useful** → S3 |
| 8 | waveshare.com | GET `/esp32-p4-wifi6-touch-lcd-4c.htm` | **`HTTP 404`** | **Useful negative** → C2 |
| 9 | waveshare.com | GET `/product/esp32-p4-wifi6-touch-lcd-4c.htm` | **`HTTP 404`** | **Useful negative** |
| 10 | waveshare.com | catalogue search `ESP32-P4-WIFI6-Touch-LCD` | Only the **3.4C** returned | **Useful negative** → C2 |
| 11 | 4C wiki HTML | extract product links | Links to the **3.4C** store page | **Key finding** → C2 |

Item 11 is the strongest single piece of evidence in this pass: the 4C's own page has no 4C
product link.

## Pass 3 — artifact analysis

| # | Target | Action | Result |
|---|---|---|---|
| 12 | Schematic PDF | `pdftotext -layout` + part-number regex | ESP32-P4NRW32, ESP32-C6-MINI-1-N4, ES8311, ES7210, CH343P, MP1658, MP1605 |
| 13 | Schematic PDF | net-name grep for SD/touch | **Poor yield** — 2-page layout dump, no clean net list |
| 14 | Demo ZIP | extract | 5052 files, 289 MiB |
| 15 | Demo ZIP | subtree sizing | LVGL 186 MB, brookesia 73 MB, Arduino_GFX 27 MB dominate |
| 16 | `06_` vs `07_` | `diff -u` | **Only** resolution constants + reg `0x40` differ |
| 17 | `displays_config.h` | read | I²C 7/8, `lcd_rst` 27, both panel profiles, `CURRENT_SCREEN` default |
| 18 | `05_I2SCodec` | read P4 `#ifdef` branch | I²S 13/12/10/9/11, PA 53 |
| 19 | Demo-wide | grep `#define …GPIO…` | **Rejected most hits** — bundled upstream examples for other boards |
| 20 | `03_sdmmc` | read Kconfig | **Unmodified upstream**; P4 defaults are Function-EV-Board values → **C1** |

Step 19 → 20 is the methodological core of this pass. A naive grep produced dozens of
plausible-looking pin defines; most belong to other boards. Only values traceable to code
Waveshare *wrote* were accepted.

## Pass 4 — component identification

| # | Target | Result |
|---|---|---|
| 21 | Touch driver refs | `esp_lcd_touch_gt911` → **GT911**, record already exists |
| 22 | Panel driver refs | `esp_lcd_jd9365` → **JD9365** (20 hits) |
| 23 | `idf_component.yml` across demos | `espressif/es8311`, `esp_hosted`, `esp_wifi_remote`, `esp_video`, `esp_h264`, `esp_lcd_jd9365`, `lvgl/lvgl` |
| 24 | Bundled lib versions | LVGL **9.3.0**, Arduino_GFX **1.6.0** |

## Pass 5 — visual schematic reading (2026-08-24, follow-up)

Undertaken specifically to close C1. Method and crop coordinates are in
[`commands.md`](./commands.md#reading-a-schematic-that-has-no-usable-text-layer--executed-success).

| # | Region | Result |
|---|---|---|
| 25 | Render both pages at 200 dpi | 2339x1653 px each |
| 26 | MicroSD block | **C1 RESOLVED** — D0–D3 = 39–42, CMD 44, CLK 43; **VDD switched by GPIO45** via AO3401 |
| 27 | LCD/touch FPC `P1` | Full 32-pin map: CTP_RESET/INT/SCL/SDA on pins 3–6, DSI lanes, panel RESET pin 25 |
| 28 | GPIO-to-net resistor map | GPIO27→RESET, GPIO33→**BL_EN**, GPIO23→**TP_RST**, GPIO26→LCD_BL_PWM |
| 29 | Trace `TP_INT` | Terminates at **test point TP2** — **not connected to the SoC** → C11 |
| 30 | Cross-check I²C | SDA=GPIO7, SCL=GPIO8 — **matches demo source** |

Three findings that no amount of source reading would have produced: the **SD power switch**
(GPIO45), the **second backlight control** (`BL_EN`, GPIO33), and the **unwired touch interrupt**.
All three are wired on the board and used by **no** shipped demo.

Also corrected: C1's original conclusion. The upstream defaults in `03_sdmmc` turned out to be
**correct** for this board because Waveshare followed Espressif's reference pin assignment. The
caution was right as method; the conclusion was wrong. Recorded rather than quietly fixed.

## Pass 6 — online references and community (2026-08-24)

Undertaken because passes 1–5 had searched **no** community source at all.

| # | Service | Query | Result |
|---|---|---|---|
| 31 | GitHub repo search | `ESP32-P4-WIFI6-Touch-LCD` | 37 hits — **found Waveshare's official org repos** |
| 32 | GitHub repo search | `ESP32-P4-WIFI6-Touch-LCD-3.4C` | 3 hits, 2 community |
| 33 | GitHub org search | `org:waveshareteam ESP32-P4-WIFI6` | **7-board family**: 3.5, 4.3, 4B, 5, 7B, X, XC |
| 34 | GitHub API | repo metadata for `…-XC` | **Apache-2.0**; HEAD `6948676d6451`; 9★/7 forks |
| 35 | GitHub contents API | `docs/`, `hardware/`, `firmware/`, `examples/`, `scripts/` | 16 bilingual docs; **factory firmware for both variants** |
| 36 | raw.githubusercontent | 6 key docs | Fetched and snapshotted locally |
| 37 | Espressif component registry API | `waveshare/esp32_p4_wifi6_touch_lcd_xc` | Versions `0.0.1`→`3.0.1`, Apache-2.0 |
| 38 | GitHub API | 3 community repos | Embedded Wizard (3.4C), Claude Buddy (3.4C), NINA (4B) |

### Why this pass mattered most

It found the things the vendor's own ZIP and wiki never mention: a **maintained Apache-2.0
repository**, a **published BSP component**, **factory firmware**, and **exact CI-tested ESP-IDF
versions**. It also independently **confirmed the entire schematic-derived pin map**, and produced
five corrections — GT9271 not GT911, GD25Q256 flash, PCB rev1.1, factory firmware exists, and
ESP-IDF v5.5.5/v6.0.2 rather than `^5.0`.

Lesson worth keeping: **searching for the vendor on GitHub should come before deep artifact
analysis**, not after. Several hours of schematic work would still have been needed for GPIO45 and
`BL_EN` — which Waveshare's docs do *not* mention — but the rest was already written down.

## Pass 7 — closing technical gaps (2026-08-24)

| # | Target | Method | Result |
|---|---|---|---|
| 39 | Store option data | Read the listing's embedded SKU JSON | **C2 + C6 resolved** — SKU 31523/31522, both `unsaleable:false` |
| 40 | `docs.waveshare.com` | Direct fetch | **New docs platform** — SKUs, dual mics, HAT adapter caveat, Arduino warning |
| 41 | Bundled LVGL | `diff -rq` vs upstream `v9.3.0` | **C5 resolved** — 0 differing files, stock |
| 42 | Bundled Arduino_GFX | `diff -rq` vs upstream `v1.6.0` | **C5 resolved** — 0 differing files, stock |
| 43 | 40-pin header `J8` | Coordinate pairing + visual | Signal set established; **per-pin mapping deliberately not published** |
| 44 | JD9365 `0x40` | Espressif component registry, driver source | **C15** — panel-specific; three values across three panels |
| 45 | JD9365 datasheet | Registry, GitHub, vendor docs | **Not found** — Fitipower publishes none |

### Two lessons worth keeping

**The 4C answer was already on disk.** I concluded it might not be a product from a `404` on a
guessed URL, having already downloaded the store page whose embedded JSON says
`{"sku":"31522",…,"unsaleable":false}`. *Check a listing's own option data before inferring
anything from a missing URL.*

**Run the diff, don't predict it.** The knob board's LVGL 8.4.0 carried a real functional patch;
this board's LVGL 9.3.0 is byte-identical to upstream. Same vendor, same archive style, opposite
answer.

## Pass 8 — remaining connectors (2026-08-24)

| # | Target | Result |
|---|---|---|
| 46 | Schematic page 2 | **It is the PCB layout, not schematic.** All circuitry is on page 1 — closes that gap |
| 47 | `J5` MIPI-CSI | 2 data lanes + clock, **plus `ESP_I2C_SDA`/`SCL`** → **C16 resolved** |
| 48 | `J4` C6 UART | `C6_U0TXD`, `C6_U0RXD`, `GND`, **`C6_IO9`** (boot strap) → **C17 partly resolved** |
| 49 | `J6` I²C header | `GND`, `ESP_3V3`, SDA, SCL — Qwiic-style breakout of the shared bus |
| 50 | `J3` USB | `VBUS`, `VBUS_OUT`, `USBD_N/P`, `GND` |
| 51 | `J8` 40-pin | **28/40 signals mapped**; 12 power/GND pins deliberately unidentified |

### Method note

`J4` and `J6` are small enough to read directly, so they served as **validation cases** for the
coordinate-pairing extraction used on `J8`. Both matched exactly, which is what justified
publishing the `J8` signal rows — while still withholding the 12 power pins, whose ground symbols
produce no text token to pair against.

## Pass 9 — RTC and /tmp archive (2026-08-26)

| # | Target | Result |
|---|---|---|
| 52 | RTC circuit | **Mapped** — `J1` 2-pin, `D2` B5819WS Schottky from `ESP_3V3`, `C39` 1 µF. **No current-limiting resistor** → **C18, a safety finding** |
| 53 | Re-verify demo ZIP | Re-downloaded 2026-08-26: SHA-256 **matches the recorded manifest hash exactly** — vendor still serving identical bytes |
| 54 | `/tmp` durability | Set up `/tmp/repo-archive/` after `/tmp/p4r` and `/tmp/hw` were both reclaimed mid-session, losing downloads |

The RTC finding is the clearest example in this research of **why schematic reading pays off**:
Waveshare's "rechargeable cells only" note reads like a preference in prose. The circuit shows it
is a hard requirement — there is nothing between the 3V3 rail and the cell but a diode.

## Pass 10 — Chinese-language sources (2026-08-26)

| # | Target | Result |
|---|---|---|
| 55 | `waveshare.net` CN wiki | `HTTP 200` — a parallel CN wiki exists |
| 56 | `waveshare.net` CN storefront | **New specs**: 28 GPIOs on the header, 170° viewing angle, optically bonded tempered glass, dual mics with AEC |
| 57 | `docs.waveshare.com/zh/…` | `HTTP 404` — CN content lives on `.net`, not a `/zh/` path |
| 58 | Cross-check `J8` | CN page says **28 programmable GPIOs**; my schematic extraction found **exactly 28** named signal pins + 12 power/GND = 40 ✅ |

### Why this mattered

Two things the English sources never said:

1. **The 28-GPIO count independently corroborates the `J8` extraction.** A vendor marketing figure
   and a coordinate-paired schematic read agreeing on the same split is meaningful validation.
2. **Panel specs** — 170° viewing angle and optical bonding — appear in no English source.

**Reusable vendor lesson:** `waveshare.net` (CN) and `waveshare.com` (EN) are **not translations
of each other**. The CN listing is more technically specific. Check both.

## Pass 11 — examples catalogue and deeper community search (2026-08-26)

| # | Target | Result |
|---|---|---|
| 59 | Build `examples/` catalogue | 21 entries: 12 selected, 5 catalogued, 4 rejected |
| 60 | GitHub repo search `esp32_p4_wifi6_touch_lcd_xc` (the **BSP component name**) | **2 hits — found `netseye/linux-waveshare-xc`**, missed by every earlier product-name query |
| 61 | GitHub **code** search for `BSP_LCD_TYPE_800_800_3_4_INCH` | `HTTP 401` — code search requires authentication |
| 62 | Read `netseye/linux-waveshare-xc` docs | **C6 SDIO pins, ESP-Hosted-NG flash procedure, one-DW-MMC-host finding**, plus independent confirmation of C11 and C12 |

### Why query 60 worked when product-name searches did not

Searching the **BSP component name** rather than the product name found a project that never says
"ESP32-P4-WIFI6-Touch-LCD-3.4C" prominently enough to rank. Its README says "Waveshare XC".

**Reusable technique:** search for the *dependency* a project must declare — the BSP component,
a driver name, a distinctive macro — not only the marketing name. Code search would be better
still, but needs an authenticated token.

## Not searched / known exclusions

Declared honestly rather than implied:

- **GitHub searched (pass 6); everything else still not.** No forum, Reddit, YouTube, blog, or
  image search. → [C9](./gaps-and-conflicts.md#c9--community-evidence--resolved-2026-08-26)
- **No Chinese-language sources** searched, despite Waveshare being a Chinese vendor with a
  separate `.cn` presence. Likely to yield material.
- **No regulatory databases** (FCC/CE) searched.
- **No distributor/marketplace** pricing beyond Waveshare's own store — no AliExpress, Amazon, or
  reseller observations, so there is exactly **one** price data point.
- **`esp-brookesia` still undiffed** — the demo pins no version, so there is no upstream revision
  to compare against. LVGL and Arduino_GFX are done ([C5](./gaps-and-conflicts.md#c5--bundled-third-party-libraries--resolved-2026-08-24)).
- **JD9365 datasheet does not appear to be public.** Fitipower publish none; the register is
  characterised but not explained ([C15](./gaps-and-conflicts.md#c15--jd9365-register-0x40-is-panel-specific-and-undocumented)).
- **2026-08-24 update:** public sources located — JD9365DA-H3 Application Note V0.03 PDF (archived) and the mainline `panel-jadard-jd9365da-h3.c` kernel driver with four full panel init tables and the controller's page-banking protocol. Per-register map still missing, so `0x40` remains *unnamed* (see [`features/display-controller-jd9365.md`](features/display-controller-jd9365.md)).
- **Schematic only partially read.** Pass 5 covered microSD, the LCD/touch FPC and the GPIO-to-net
  resistor map. The 40-pin expansion header, MIPI-CSI connector, RTC circuit and card-detect net
  are still unmapped, as is page 2.
- **No hardware.** Nothing built, flashed, or measured.

## Stopping criterion

Stopped after primary vendor sources were exhausted and cross-validated, **not** after two
null passes. Community, non-English, and regulatory source classes remain **unsearched**, so this
pass does not meet the skill's full stopping criteria. It is a complete *vendor-documentation*
snapshot and is labelled as such.

## Highest-value next actions

1. ~~Read the schematic visually to resolve microSD and GT911 INT/RST pins~~ — **done, pass 5.**
   Remaining schematic work: 40-pin header, MIPI-CSI connector, RTC circuit, card-detect net.
2. ~~Search community sources~~ — **GitHub done, pass 6.** Remaining: forums, YouTube, Chinese
   sources (Waveshare's repos ship 中文 docs, so Chinese community material likely exists),
   image search for a physical 4C.
3. ~~Diff bundled LVGL/Arduino_GFX~~ — **done, pass 7. Both stock.**
4. ~~Obtain the JD9365 datasheet~~ — **attempted, not public.**
5. Finish `J8` per-pin mapping from the schematic at high zoom, or with a meter.
6. ~~Map the MIPI-CSI connector~~ — **done, pass 8.** ~~Page 2~~ — **it is the PCB layout.**
   ~~RTC circuit~~ — **done, pass 9.**
7. ~~Chinese-language vendor sources~~ — **done, pass 10.** Chinese *community* sources
   (立创开源, 电子发烧友, Bilibili, CSDN) remain unsearched.
8. **GitHub code search needs an authenticated token** — would find projects using the BSP macro
   without naming the board.
