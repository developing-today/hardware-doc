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
| [`solderparty/keebdeck_basic_hw`](https://github.com/solderparty/keebdeck_basic_hw) @ `2b537ce` ("Rev 1.1 - Production") | KeebDeck reference/evaluation board. **Schematic PDF retained at [`artifacts/keebdeck-basic/`](artifacts/keebdeck-basic/README.md)** (355 080 B, `593aa32d…`, KiCad 9.0.1 export dated 2025-05-04) and **mined into [`keyboard.md` §2b](keyboard.md#2b-verified-the-keebdeck-basic-reference-board-read-from-its-schematic)** on 2026-09-20 — it is a **6×12 diode-less** board with the backlight and boot button **DNP**, so it is a weaker reference than §2 implied. Repo licence **not read**; recorded `unknown` |
| [`nicolaielectronics/mipi_dsi_abstraction`](https://components.espressif.com/components/nicolaielectronics/mipi_dsi_abstraction) | MIPI DSI setup for the LH397K-IC01 and the ESP32-P4 dev-kit display |
| [`nicolaielectronics/rvswd`](https://components.espressif.com/components/nicolaielectronics/rvswd) | Reprograms CH32V20x/30x from the ESP32-P4 |
| [`ranzbak/konsoolnes`](https://github.com/ranzbak/konsoolnes) | NES emulator |
| [`petrisi/tanmatsu-multimesh`](https://github.com/petrisi/tanmatsu-multimesh) | MeshCore + Meshtastic |
| [`saarbastler/esp32-component-esp-hosted-tanmatsu`](https://github.com/saarbastler/esp32-component-esp-hosted-tanmatsu) | esp-hosted fork with Tanmatsu modifications |
| [`badgeteam/konsool-zero`](https://github.com/badgeteam/konsool-zero) @ `0f0b964` | RFID/NFC/sub-GHz expansion (WIP) — ST25R3916 `U5`, CC1101 `U1`, **CH32V003 `U19`**. ⚠ *not* STM32WB55CC — corrected 2026-09-20, see below |
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
| CH32V203 | <https://www.wch-ic.com/downloads/CH32V203DS0_PDF.html> — ✅ **now held locally**, see below |
| E22-900M22S | <https://www.cdebyte.com/products/E22-900M22S> |
| Display (SWI) | <http://www.swicn.com/> |
| **ESP32-P4** | **Not publicly available** at the time the vendor documentation was written |

## Datasheets recovered from `konsool-zero`'s `docs/` folder · *added 2026-09-20*

The `badgeteam/konsool-zero` clone (@ `0f0b964`) carries a `docs/` folder of reference material
its author collected while designing that expansion board. It held **seven chip documents** plus
six **Flipper Devices Inc.** schematic sheets and a folder of annotated Flipper Zero teardown
photographs — konsool-zero is openly derived from studying the Flipper Zero.

All seven chip documents have now been **mined and filed as component artifacts** (a chip
datasheet is a *component* artifact, even when a device task fetched it). They are no longer in
scratch.

| Document | Revision | Now filed at | Fitment established? |
|---|---|---|---|
| `ch32/CH32V003RM.PDF` | RM **V1.6** | [`components/wch/ch32v003/`](../../../components/wch/ch32v003/README.md) | ✅ **Yes** — `konsool-zero` `U19` = **`CH32V003F4U6`**, QFN-20, from `zero-mcu.kicad_sch`. **Not on the Tanmatsu mainboard** |
| `ch32/CH32V003DS0.PDF` *(unlisted extra)* | DS **V1.4** | same record | ✅ as above |
| `ch32/CH32FV2x_V3xRM.PDF` | RM **V2.1**, 595 pp | [`components/wch/ch32f2x-ch32v2x-ch32v3x/`](../../../components/wch/ch32f2x-ch32v2x-ch32v3x/README.md) | ❌ **No CH32F2x/V3x part fitted anywhere.** ⭐ But this manual **is the register reference for the Tanmatsu's own `CH32V203C8T6`** — WCH documents CH32F2x/V2x/V3x in one manual, and it names `CH32V203C8` as a `CH32V20x_D6` device |
| `ch32/CH32V203DS0.PDF` *(unlisted extra)* | DS **V2.7** | [`components/wch/ch32v203c8t6/artifacts/`](../../../components/wch/ch32v203c8t6/README.md) | ✅ **Yes — Tanmatsu `U12`.** ⭐ This is exactly the datasheet that record listed as *"No local datasheet copy"*. Gap closed |
| `cc1101_datasheet.pdf` | **`SWRS061I`** | [`components/texas-instruments/cc1101/`](../../../components/texas-instruments/cc1101/README.md) | ✅ **Yes** — `konsool-zero` `U1` = **`CC1101RGPR`**, from `sub-ghz-radio.kicad_sch`. **Not on the Tanmatsu mainboard** |
| `ST25R3916.PDF` | **`DS12484 Rev 4`** (Alldatasheet) | [`components/stmicroelectronics/st25r3916/`](../../../components/stmicroelectronics/st25r3916/README.md) | ✅ **Yes** — `konsool-zero` `U5` = **`ST25R3916-AQWT`**, VFQFPN32, from `nfc-block.kicad_sch`. **Not on the Tanmatsu mainboard** |
| `stm32wb55cc.pdf` | **`DS11929 Rev 17`** | [`components/stmicroelectronics/stm32wb55xx/`](../../../components/stmicroelectronics/stm32wb55xx/README.md) | ❌ **NO — and an earlier claim here was wrong.** See below |

### ⚠ Correction: konsool-zero does **not** carry an STM32WB55CC

[`expansion-boards.md` §2](expansion-boards.md) previously listed `STM32WB55CC` under *"Silicon
identified from the KiCad schematics"*, described as *"an on-board processor, not just a
peripheral"*. **The schematics do not support this.** Verified 2026-09-20, `executed-success`:

- A case-insensitive search for `stm32` or `wb55` across **every** `.kicad_sch`, `.kicad_pcb`,
  `.kicad_pro` and `jlcpcb/project.db` in the project returns **zero matches** — and also zero
  across the project's entire git history (one commit).
- A **full reference-designator census** of all nine sheets finds no ST microcontroller. The
  board's only MCU is **`U19` = `CH32V003F4U6`** on `zero-mcu.kicad_sch` — a 16 KB / 2 KB RV32EC
  helper, not a dual-core wireless MCU.

The datasheet is in `docs/` because **the Flipper Zero's own MCU is an STM32WB55**, and the folder
is a Flipper Zero prior-art study — the same folder holds Flipper's NFC, RFID, iButton, Power and
Sub-1 GHz schematics, which independently name the same `CC1101RGPR` and `ST25R3916-AQWT` that
konsool-zero adopted. The earlier pass appears to have read *presence of a datasheet* as *evidence
of a fitted part*.

`expansion-boards.md` has been corrected. Recorded here with evidence and date so it is not
re-investigated.

### ✅ Follow-up completed 2026-09-20 — everything in `docs/` is now filed

The items below were deferred by the earlier pass. **They have since been placed.** Nothing from
`konsool-zero/docs/` remains unfiled.

| Item | Where it went | Rationale |
|---|---|---|
| `docs/*.pdf` — six **Flipper Devices Inc.** schematics (iButton, NFC, Power, Power and vibro, RFID, Sub-1 GHz CC1101) | [`devices/flipper-devices/flipper-zero/artifacts/schematics/`](../../flipper-devices/flipper-zero/README.md) — **in the repository** | They describe a different product, so per *file by what it describes* they belong to it. The record is an explicit **artifact-preservation stub**, not a researched device record, and says so at the top. A SHA-256 sweep confirmed all six were in **no** other location — they existed in exactly one place |
| `docs/flipper-zero-photos/` — 7 PNGs | [`…/flipper-zero/artifacts/teardown-photos`](../../flipper-devices/flipper-zero/artifacts/teardown-photos.ARCHIVED.md) — **archived**, placeholder in place | 4.0 MB of images with **no established provenance or licence**; recorded as `unknown` rather than guessed |
| `docs/link-to-explanation.txt` | Filed beside the schematics | **Still not retrieved.** The URL <https://www.cnblogs.com/shangdawei/p/3729375.html> has not been fetched or assessed in any pass. Recorded as an open item |

**What reading them established** — the design lineage of konsool-zero, which was previously an
assumption:

| | Flipper Zero | konsool-zero |
|---|---|---|
| Sub-GHz transceiver | `CC1101RGPR` | `CC1101RGPR` — **same** |
| RF switches | `BGS13S4N9E6327XTSA1` | `BGS13S4N9E6327XTSA1` — **same** |
| Balun | `B0310J50100AHF` | `B0310J50100AHF` — **same** |
| 125 kHz front end | `LMV331`, `LMV358` | `LMV331IDCKR`, `LMV358` — **same** |
| NFC | `ST25R3916` | `ST25R3916-AQWT` — **same** |
| CC1101 reference | **26 MHz crystal**, sheet labelled 433 MHz | **27 MHz oscillator** — **changed** |
| MCU | **`STM32WB55`** | **`CH32V003F4U6`** — **changed** |

The MCU row is the origin of the fabricated STM32WB55CC claim corrected above: the datasheet was in
`docs/` because the *prior-art device* uses that part.

### konsool-zero's own KiCad source — filed 2026-09-20

The sheets that this correction rests on — `zero-mcu.kicad_sch`, `sub-ghz-radio.kicad_sch`,
`nfc-block.kicad_sch` and the rest — were **still only in `scratch/`** after the correction was
written, so the record cited evidence the repository did not hold. They are now at
[`artifacts/konsool-zero/`](artifacts/konsool-zero/README.md), together with
`tanmantsu-zero.kicad_pcb`, and were mined into
[`konsool-zero-wiring.md`](konsool-zero-wiring.md).

Licence, previously recorded as *"none stated"*: **BSD 3-Clause, Copyright (c) 2024, Nicolai
Electronics** — `LICENSE` is tracked at `0f0b964`. Corrected in `expansion-boards.md` §1 and §2.

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
