# Xteink X3 — sources

Retrieved **2026-09-04** unless stated.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published | Establishes | Limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| **X301** | `BoardConfig.h` `XTEINK_X3` + `XTEINK_X3_UC8279`, L881–947 | Free-Ink | community | source (commit-pinned) | <https://github.com/Free-Ink/freeink-sdk/blob/24003795381a6c23630a26472ae3b06550333e71/libs/hardware/BoardConfig/include/BoardConfig.h#L881-L947> | 2026-09-04 | commit 2026-09-01 | Pins, both panel profiles, I²C peripherals, SD rail | Third-party RE | `scratch/eink-software/repos/freeink-sdk/` |
| **X302** | `docs/xteink-x3-uc8279-support.md` | Free-Ink | community | technical note | <https://github.com/Free-Ink/freeink-sdk/blob/24003795381a6c23630a26472ae3b06550333e71/docs/xteink-x3-uc8279-support.md> | 2026-09-04 | same | The UC8279d variant, its detection, and **its explicit unvalidated status** | Datasheet-derived; author states no unit has been benched | same |
| **X303** | `XteinkDetect.cpp` | Free-Ink | community | source | <https://github.com/Free-Ink/freeink-sdk/blob/24003795381a6c23630a26472ae3b06550333e71/libs/hardware/XteinkDetect/src/XteinkDetect.cpp> | 2026-09-04 | same | I²C addresses 0x55/0x68/0x6B, `WHO_AM_I=0x05`, the X3/X4 fingerprint | The RTC probe reads only reg 0x00 — **does not discriminate DS1307 vs DS3231** | same |
| **X304** | **X3 teardown, 13 images** | Reddit user | community | **teardown, firsthand** | <https://old.reddit.com/r/xteinkereader/comments/1uksv6s/xteink_x3_teardown/> · album <https://imgur.com/a/xteink-x3-teardown-OA6CS2C> | 2026-09-04 | **2026-07-01** | **650 mAh battery**, glued magnets, glass back, ESP32-C3, 128 Mbit flash, **"DS1307 RTC"** | Captions are the photographer's reading; rights unknown | [archived](artifacts/teardown/imgur-2026-07-01.ARCHIVED.md) |
| **X305** | **`sunwoods/Xteink-X3` — Chinese hardware census + schematic** | GitHub `sunwoods` | community | **teardown + schematic, firsthand** | <https://github.com/sunwoods/Xteink-X3> | 2026-09-04 | — | Full BOM; **ISO 14443A NFC tag**; Puya flash; TP4056-class charger; **a hand-drawn schematic**; pins *measured with a multimeter* | Schematic uses substitute footprints; some part numbers borrowed from CrossPoint rather than read | [archived](artifacts/teardown/sunwoods-cn.ARCHIVED.md) |
| **X306** | X3 Shopify product record | Xteink | **primary** | store API | <https://www.xteink.com/products.json?limit=250> | 2026-09-04 | created 2025-12-08, published 2025-12-11 | **$69.00**, two SKUs, both in stock, 58 g packaged | **Body prose is AI/SEO and is factually wrong** (claims a frontlight and cloud sync) | `scratch/xteink/vendor/products-p1.json` |
| **X307** | "X3 Is Coming: Smaller, Lighter…" | Xteink via r/xteinkereader | **primary** (vendor announcement) | forum | <https://old.reddit.com/r/xteinkereader/comments/1pi6ezd/> | 2026-09-04 | 2025-12-09, 275 pts | **55 g, 3.7-inch, 250+ PPI, gyroscope, NFC, pogo charging, clock + battery %** | Vendor marketing, but specific and falsifiable — and the PPI checks out arithmetically | `scratch/xteink/reddit/_merged-posts.json` |
| **X308** | "Xteink X3 Live Now" | Xteink via r/xteinkereader | **primary** | forum | <https://old.reddit.com/r/xteinkereader/comments/1pjw3ay/> | 2026-09-04 | 2025-12-11, 147 pts | Same spec list; **shipping from 2026-02-05**; Super Early Bird units non-refundable | same | same |
| **X309** | "X3 vs X4 - actual experience comparison" | r/xteinkereader | community | forum, comparative ownership | <https://old.reddit.com/r/xteinkereader/comments/1syav96/> | 2026-09-04 | 2026-04-28, **412 pts** | X3 buttons *"mushy and quieter"* vs X4's *"clickier and louder"* | Subjective | same |
| **X310** | `zocs/eink-quick-flasher` firmware README | community dev | community | repository doc | <https://github.com/zocs/eink-quick-flasher/blob/main/firmware/README.md> | 2026-09-04 | — | Stock **V1.0.7** and **V5.2.13** (CN + EN, full **and** OTA); **CN/EN differ only by default UI language** | Files are Git LFS pointers; **blobs not fetched** | `scratch/xteink/firmware/zocs-firmware-README.md` |
| **X311** | "CrossPoint 1.5 released" | r/xteinkereader | community | forum | <https://old.reddit.com/r/xteinkereader/comments/1vhvtdd/> | 2026-09-04 | 2026-08-07, **763 pts** | *"DOES support the new x3 display variants"*; soft-brick warning for stale forks | Developer statement | same |
| **X312** | "CrossPoint 1.4.0 released" | r/XTEINK | community | forum | <https://old.reddit.com/r/XTEINK/comments/1uek163/> | 2026-09-04 | 2026-06-24, 350 pts | **X3 OTA out-of-memory**, and the reflash/SD-flash escape | Developer statement | same |
| **X313** | "Anyone confirm which devices have metal backing?" | r/xteinkereader | community | forum, owner report | <https://old.reddit.com/r/xteinkereader/comments/1w56phf/> | 2026-09-04 | 2026-09-02 | **Rear glass cracked** on an X3 | Single anecdote; question went unanswered | same |
| **X314** | "Got an X3 for dirt cheap ($16)" | r/XTEINK | community | forum, owner report | <https://old.reddit.com/r/XTEINK/comments/1vrnxnq/> | 2026-09-04 | 2026-08-18, 24 pts | Used pricing; **CrossMux** (a Chinese CrossPoint fork with WeChat Read support); criticism of vendor–community relations | Single anecdote, channel not stated | same |
| **X315** | `anki630/crossmosa-freeink-sdk` | community dev | community | repository | <https://github.com/anki630/crossmosa-freeink-sdk> | 2026-09-04 | pushed 2026-08-28 | *"UC8279 waveform tuning"* — the only project working the new X3 panel | Not inspected | — |

## Corroboration map

| Claim | Independent sources |
|---|---|
| ESP32-C3 | **[SDK]** · **[TD-EN]** photo 10 · **[TD-CN]** BOM |
| 128 Mbit / 16 MB Puya flash | **[TD-EN]** photo 10 · **[TD-CN]** BOM |
| QMI8658 IMU @0x6B | **[SDK]** ×2 files · **[TD-CN]** BOM |
| BQ27220 gauge @0x55 | **[SDK]** ×2 files · **[TD-CN]** BOM |
| ~257 PPI | **[VENDOR]** *"250+ PPI"* · **arithmetic** from 792×528 / 3.7″ |
| 650 mAh | **[TD-EN]** photo 3 only — **single source** |
| NFC tag | **[TD-CN]** BOM · **[VENDOR]** announcement |
| **RTC part** | **THREE SOURCES DISAGREE** — see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) |

## Not used as evidence

`xteink.com` X3 product prose — demonstrably false (advertises a frontlight the
device does not have).
