# Tanmatsu — sources

> Every source used, with pinned commits. Retrieved **2026-08-24**.
> All ten repositories were cloned at the commits below; the clones are the primary evidence for this research pass.

## Official repositories (Nicolai-Electronics)

| Repository | Commit | Commit date | Author | Licence | Contents |
|---|---|---|---|---|---|
| [`app-repository`](https://github.com/Nicolai-Electronics/app-repository) | [`f83e1559`](https://github.com/Nicolai-Electronics/app-repository/tree/f83e1559553497903c083525a10d2aaf53344377) | 2026-08-22 | Renze Nicolai | *none* | Official application repository (57 apps) |
| [`esp32-component-tanmatsu-coprocessor`](https://github.com/Nicolai-Electronics/esp32-component-tanmatsu-coprocessor) | [`6eea3735`](https://github.com/Nicolai-Electronics/esp32-component-tanmatsu-coprocessor/tree/6eea3735346ee1b689898c77e500fb1d0c4e024e) | 2026-06-17 | Renze Nicolai | *none* | ESP-IDF driver for the coprocessor |
| [`esp32-component-tanmatsu-wifi`](https://github.com/Nicolai-Electronics/esp32-component-tanmatsu-wifi) | [`d8ce0bf1`](https://github.com/Nicolai-Electronics/esp32-component-tanmatsu-wifi/tree/d8ce0bf106141d6bccf4cb9a927bd494facc31af) | 2026-08-01 | Senna Hijlkema | MIT | ESP-IDF Wi-Fi/BLE wrapper (esp-hosted to the C6) |
| [`tanmatsu-coprocessor-firmware`](https://github.com/Nicolai-Electronics/tanmatsu-coprocessor-firmware) | [`57ff2505`](https://github.com/Nicolai-Electronics/tanmatsu-coprocessor-firmware/tree/57ff2505d7256b55cc5fea4eb9be10a9a077bafa) | 2026-06-17 | Renze Nicolai | MIT | CH32V203 coprocessor firmware |
| [`tanmatsu-documentation`](https://github.com/Nicolai-Electronics/tanmatsu-documentation) | [`bd3ded51`](https://github.com/Nicolai-Electronics/tanmatsu-documentation/tree/bd3ded51548433bd7d614f5607b7d36f5eed61fa) | 2026-08-01 | CJvanSoest | *none* | Sphinx/MyST source of the official documentation site |
| [`tanmatsu-hardware`](https://github.com/Nicolai-Electronics/tanmatsu-hardware) | [`640805dd`](https://github.com/Nicolai-Electronics/tanmatsu-hardware/tree/640805dd4304f4bfaac24965f8eecf81bec97bf1) | 2026-02-25 | Renze Nicolai | CERN-OHL-P | KiCad design, schematic PDF, production BOM/positions/IPC netlist |
| [`tanmatsu-launcher`](https://github.com/Nicolai-Electronics/tanmatsu-launcher) | [`20022fce`](https://github.com/Nicolai-Electronics/tanmatsu-launcher/tree/20022fce316d768a1ff966b973ee2127511713f5) | 2026-08-23 | Renze Nicolai | MIT | Launcher firmware |
| [`tanmatsu-mechanical`](https://github.com/Nicolai-Electronics/tanmatsu-mechanical) | [`c623cd54`](https://github.com/Nicolai-Electronics/tanmatsu-mechanical/tree/c623cd548c9cafb95773624fe775001984449a89) | 2026-07-03 | Renze Nicolai | CERN-OHL-P | Case and mechanical design files |
| [`tanmatsu-radio`](https://github.com/Nicolai-Electronics/tanmatsu-radio) | [`cb4e38c0`](https://github.com/Nicolai-Electronics/tanmatsu-radio/tree/cb4e38c02aa8ad533fd17b24921c4ca4848eeaf6) | 2026-08-01 | Senna Hijlkema | Apache-2.0 | ESP32-C6 radio firmware |
| [`tanmatsu-template`](https://github.com/Nicolai-Electronics/tanmatsu-template) | [`907fb965`](https://github.com/Nicolai-Electronics/tanmatsu-template/tree/907fb9657658995efab210b754f28a3ace06d03a) | 2026-07-30 | Renze Nicolai | *none* | Template app (PAX graphics) |

Clone any of them at the exact state used here:

```bash
git clone https://github.com/Nicolai-Electronics/tanmatsu-hardware
git -C tanmatsu-hardware checkout 640805dd4304f4bfaac24965f8eecf81bec97bf1
```

## Related official resources

| Resource | URL | Class | Notes |
|---|---|---|---|
| Official site / app portal | <https://tanmatsu.cloud> | primary | `tanmatsu.com` redirects here. A JavaScript SPA — **no server-rendered content**, so text extraction and search engines see nothing useful |
| Documentation site | built from `tanmatsu-documentation` | primary | Source snapshot retained locally |
| Issue tracker | <https://github.com/Nicolai-Electronics/tanmatsu-issue-tracker/issues> | primary | |
| Project board | <https://github.com/orgs/Nicolai-Electronics/projects/2/views/2> | primary | Development roadmap |
| Vendor site | <https://nicolaielectronics.nl> | primary | |
| Discord | <https://discord.gg/KkY6JqNCqT> | community | |
| Telegram | <https://t.me/+SueEz5IWYR05NzU8> | community | |
| Badge.team | <https://badge.team> | primary (ecosystem) | Parent software ecosystem |

## Ecosystem repositories (badgeteam and others)

| Repository | Role |
|---|---|
| [`badgeteam/esp32-component-badge-bsp`](https://github.com/badgeteam/esp32-component-badge-bsp) | Board support package; 11 targets including `tanmatsu`, `konsool`, `why2025`. **Authoritative keymap** in `targets/tanmatsu/badge_bsp_input.c` |
| [`badgeteam/esp32-component-badgelink`](https://github.com/badgeteam/esp32-component-badgelink) | BadgeLink protocol + Python/WebUSB host tools |
| [`badgeteam/appfs`](https://components.espressif.com/components/badgeteam/appfs) | App filesystem + bootloader modification. Originally by Jeroen Domburg (sprite_tm) for the PocketSprite |
| [`solderparty/keebdeck_keyboard_hw`](https://github.com/solderparty/keebdeck_keyboard_hw) @ `f1c074c` | **KeebDeck keypad footprints, symbol, dimensional drawing, 3D models.** CERN-OHL v1.2. KiCad subset retained at `artifacts/keebdeck-keyboard/` |
| [`solderparty/keebdeck_basic_hw`](https://github.com/solderparty/keebdeck_basic_hw) @ `2b537ce` | KeebDeck reference/evaluation board |
| [`nicolaielectronics/mipi_dsi_abstraction`](https://components.espressif.com/components/nicolaielectronics/mipi_dsi_abstraction) | MIPI DSI setup for the LH397K-IC01 and the ESP32-P4 dev-kit display |
| [`nicolaielectronics/rvswd`](https://components.espressif.com/components/nicolaielectronics/rvswd) | Reprograms CH32V20x/30x from the ESP32-P4 |
| [`ranzbak/konsoolnes`](https://github.com/ranzbak/konsoolnes) | NES emulator |
| [`petrisi/tanmatsu-multimesh`](https://github.com/petrisi/tanmatsu-multimesh) | MeshCore + Meshtastic |
| [`saarbastler/esp32-component-esp-hosted-tanmatsu`](https://github.com/saarbastler/esp32-component-esp-hosted-tanmatsu) | esp-hosted fork with Tanmatsu modifications |
| [`badgeteam/konsool-zero`](https://github.com/badgeteam/konsool-zero) @ `0f0b964` | RFID/NFC/sub-GHz expansion (WIP) — ST25R3916, CC1101, STM32WB55CC |
| [`badgeteam/konsool-18650-expansion`](https://github.com/badgeteam/konsool-18650-expansion) @ `69504c4` | 18650 battery expansion, CERN-OHL-P v2 |
| [`badgeteam/konsool-expansion-template`](https://github.com/badgeteam/konsool-expansion-template) | ⚠ **empty repository** — no commits |
| [`badgeteam/konsool-template-lvgl`](https://github.com/badgeteam/konsool-template-lvgl) | LVGL app template, CC0-1.0 |
| [`Nicolai-Electronics/tanmatsu-frontpanel-cyberdeck`](https://github.com/Nicolai-Electronics/tanmatsu-frontpanel-cyberdeck) @ `7e53be2` | Decorative front panel, CERN-OHL-P. Artwork by Ankhaneko |
| [`Nicolai-Electronics/tanmatsu-frontpanel-honeycomb`](https://github.com/Nicolai-Electronics/tanmatsu-frontpanel-honeycomb) @ `270c38e` | Decorative front panel, CERN-OHL-P |

A GitHub search for `tanmatsu` returned **117 repositories** on 2026-08-24, dominated by community apps (`nullislandspace`, `Z6543`, `at.cavac`, `CJvanSoest` and others). Note that `snowdrop4/tanmatsu` and `d3npa/GB-tanmatsu` are **unrelated projects** that share the word.

## Component datasheets referenced by the vendor

| Part | Source |
|---|---|
| ESP32-C6-WROOM-1 | <https://www.espressif.com/sites/default/files/documentation/esp32-c6-wroom-1_wroom-1u_datasheet_en.pdf> |
| CH32V203 | <https://www.wch-ic.com/downloads/CH32V203DS0_PDF.html> |
| E22-900M22S | <https://www.cdebyte.com/products/E22-900M22S> |
| Display (SWI) | <http://www.swicn.com/> |
| **ESP32-P4** | **Not publicly available** at the time the vendor documentation was written |

## Attribution

Electronics design: **Nicolai Electronics** and **Paul Honig** ([@ranzbak](https://github.com/ranzbak)).
Acknowledged in the hardware repo: **Jay Visschedijk** (ergonomic board outline), **Wietse Boonstra** (component footprints), **Kliment Yanev** and **Jelle Haandrikman** (review).
Keyboard designed by **[Solder Party](https://www.solder.party/)**.
Documentation contributions from **CJvanSoest**; radio firmware and Wi-Fi component by **Senna Hijlkema**.

## Evidence boundary

- Everything documented is from **primary vendor sources** — design files, production data, and the vendor's own documentation source.
- **No hardware was available.** No measurement, no build, no flash, no photograph taken.
- **Community sources were only lightly sampled** (a GitHub repository search). Discord and Telegram — where most day-to-day Tanmatsu discussion happens — were **not** mined, and neither were forum threads, blogs or videos. That is the largest gap in this pass.
- Pricing and availability were **not** researched; the webshop was not scraped.
