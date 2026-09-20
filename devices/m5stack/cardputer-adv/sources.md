# Cardputer ADV — sources

> Retrieval date for every row below is **2026-09-04** unless a different date is given.
> `Class` ∈ {primary, authorized mirror, credible mirror, standard, community}.
> All HTTP fetches used `curl` with the browser User-Agent recorded in
> [`commands.md`](commands.md); `docs.m5stack.com` and `shop.m5stack.com` served 200 to the
> first request in every case, consistent with
> [`vendors/m5stack`](../../../vendors/m5stack/README.md) §1.

## Primary — M5Stack documentation

| ID | Title | Publisher | Class | Medium | URL | Published/updated | Establishes | Limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|
| **S1** | Cardputer-Adv product page (EN) | M5Stack | primary | official page | `https://docs.m5stack.com/en/core/Cardputer-Adv` | undated | SKU `K132-Adv`, spec table, PinMap, EXT table, schematics/mechanical links, PlatformIO profile, product-comparison table | prose contradicts the v1.1 page on the RGB warning | `artifacts/docs/docs-en-core-Cardputer-Adv.html` (147 339 B, `f05bbb70…`) |
| S1z | Cardputer-Adv product page (zh_CN) | M5Stack | primary | official page | `https://docs.m5stack.com/zh_CN/core/Cardputer-Adv` | undated | translation control | 146 690 B; **no CN-only datasheet delta found** for this product, unlike the PaperMono case | `artifacts/docs/docs-zh_CN-core-Cardputer-Adv.html` (`4a285b02…`) |
| **S2** | Cardputer v1.1 product page | M5Stack | primary | official page | `https://docs.m5stack.com/en/core/Cardputer%20V1.1` | undated | SKU `K132-V11`, 74HC138 PinMap, **the RGB/backlight warning**, Stamp-S3A identification, comparison to v1.0 | — | `../cardputer-v1.1/artifacts/docs-en-core-Cardputer-V1.1.html` |
| **S3** | Cardputer (v1.0) product page | M5Stack | primary | official page | `https://docs.m5stack.com/en/core/Cardputer` | undated | SKU `K132`, StampS3, identical PinMap to v1.1 | — | `../cardputer-v1.0/artifacts/docs-en-core-Cardputer.html` |
| **S4** | Cardputer Mesh Kit page | M5Stack | primary | official page | `https://docs.m5stack.com/en/core/Cardputer_Mesh_Kit` | undated | SKU `K152`, Cap-Bus table, Meshtastic licensing, LoRa/GNSS specs | ⚠ its **EXT table swaps UART TX/RX** and contradicts its own Cap-Bus table | `../cardputer-mesh-kit/artifacts/docs-en-core-Cardputer_Mesh_Kit.html` |
| **S5** | CardputerZero page | M5Stack | primary | official page | `https://docs.m5stack.com/en/CardputerZero` | *"Work in progress"* banner | SKU `C154`/`C155`, CM0 platform, TCA8418 + M5IOE1 + RX8130CE + BQ27220, EXT 2.54-14P on a Linux device | explicitly provisional | `../cardputer-zero/artifacts/docs-en-CardputerZero.html` |
| **S6** | Cardputer Accessory Kit page | M5Stack | primary | official page | `https://docs.m5stack.com/en/accessory/Cardputer%20Accessory%20Kit` | undated | the spare Stamp+display kit; disassembly video reference | the `…_v1.1` URL **404s** (4 162 B) | scratch |
| **S7** | Release history | M5Stack | primary | official page | `https://docs.m5stack.com/en/history` | live | Mesh Kit 2026-04-30; Cap LoRa-1262 2026-01-04; Cap CC1101 2026-08-28, both categorised *"For Cardputer-Adv"* | paginated — older Cardputer entries not on the first page | scratch |
| **A1** | **Cardputer-Adv schematic** | M5Stack | primary | schematic PDF, 4 sheets | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1178/Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf` | file-stamped 2025-06-20 | **the whole component inventory, keyboard matrix, EXT header, power train** | no EDA source published; text layer validated against the PinMap | `artifacts/schematic/…` 878 155 B `9553f5ee…` |
| A1p | Per-sheet renders of A1 | M5Stack | primary | PNG ×4, 5848×4132 | `…/1178/Sch_M5CardputerAdv_v1.0_…_page_0{1..4}.png` | as A1 | every value transcribed in this record was read from these | large | scratch `media/` |
| **A2** | **Stamp-S3A schematic** | M5Stack | primary | schematic PDF | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1150/Sch_StampS3_v0.3.3.pdf` | v0.3.3 | AW35122FDR, JW5712, **WS2812 on `BL_3V3`**, USB front end, no UART bridge | ⚠ linked as *"Stamp-S3A"* but **named `StampS3`** | 369 766 B `2f9610ae…`; belongs to [`components/m5stack/stamp-s3a`](../../../components/m5stack/stamp-s3a/README.md) |
| **A3** | **Cardputer v1.0/v1.1 schematic** | M5Stack | primary | schematic PDF, 2 sheets | `…/1127/Sch_M5Cardputer.pdf` **and** `…/481/Sch_M5Cardputer.pdf` | undated | 74HC138 keyboard, NS4168, SPM1423, same power train | ⚠ **the two URLs are byte-identical** | 717 743 B `6016c1fe…` |
| A3b | Cardputer base schematic | M5Stack | primary | schematic PDF | `…/1127/M5Cardputer_Base.pdf` = `…/481/Sch_M5cardputer_Base.pdf` | undated | base battery board | byte-identical pair | 24 076 B `29542fe1…` |
| **A5** | **StampS3 v0.2 schematic** | M5Stack | primary | schematic PDF | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/522/Sch_M5StampS3_v0.2.pdf` | v0.2 | SGM2578, **WS2812 on `VDD_3V3`**, `M2` regulator | ⚠ **no page render exists** at the `_page_NN.png` convention; the `M2` value string is suspect | 348 884 B `6d92e1ae…` |
| **A4** | Cardputer-Adv mechanical drawing | M5Stack | primary | dimension PDF | `…/1178/K132-Adv-cardputer-ADV.pdf` | undated | 84.0 × 54.0 × 19.6 mm | — | `artifacts/mechanical/…` 127 977 B `6c937ca0…` |
| A6 | IMU axis diagram | M5Stack | primary | image | `…/1178/IMU-Cardputer-Adv.jpg` | undated | IMU orientation | **not retained** — imagery is not licensed for redistribution | see [`media.md`](media.md) |
| A7 | EasyLoader (ADV) | M5Stack | primary | Windows binary | `…/1178/Easy_Loader_for_Cardputer-Adv.exe` | undated | factory image delivery | **not downloaded** | — |
| S8 | UiFlow2 quick start (ADV) | M5Stack | primary | official page | `https://docs.m5stack.com/en/uiflow2/cardputer-adv/program` | — | a **distinct** UiFlow2 path from the v1.x | **not fetched** | — |

## Primary — M5Stack source code

| ID | Repo | Class | Commit / ref | Establishes | Licence | Local |
|---|---|---|---|---|---|---|
| **S10** | `m5stack/M5Cardputer` | primary | **`f1392858b9994c3547120e602a57d3553d16ab01`**, 2026-07-21, v**1.1.1** | keyboard readers, TCA8418 remap, key legend map, board dispatch, examples | **MIT** | `artifacts/source-snapshots/M5Cardputer-f1392858/` (33 files, 284 KB) |
| **S11** | `m5stack/M5Unified` | primary | **`8530f5377d782e4a25a6c482de2e71c3f75ca8eb`**, 2026-08-27 | I²C/SD/RGB pin tables, ES8311 enable callbacks, power class, button map | MIT | not vendored — quoted with permalinks |
| **S12** | `m5stack/M5GFX` | primary | **`d91077b9a607b59404e4e4a49f775c792bfae382`**, 2026-08-25 | **the board-autodetect algorithm and M5Stack's own ADV-vs-Cardputer pin comment block**; panel config | MIT | not vendored — quoted with permalinks |
| **S13** | `m5stack/M5Cardputer-UserDemo`, branch **`CardputerADV`** | primary | **`b549eac0a3c65bc108186c276b8fac0a214aaa4e`**, 2026-06-08 | `hal_config.h`, partition table, sdkconfig, `uart_set_pin` (settles TX/RX), app list | MIT ⚠ pins LGPL-3.0 RadioLib | `artifacts/source-snapshots/M5Cardputer-UserDemo-CardputerADV-b549eac0/` (build config only) |
| S13b | same repo, `main` | primary | `a34d7ebcd508fb903a2b1123be8c8b54abd55d07`, 2026-07-17 | the v1.x factory firmware | MIT | — |

## Primary — M5Stack commerce

| ID | What | Class | URL | Establishes |
|---|---|---|---|---|
| **S9** | Shopify product JSON | primary | `shop.m5stack.com/search/suggest.json?q=cardputer&…` and `/products/<handle>.json` | prices, stock, ids, `created_at`/`published_at`, **the `[EOL]` marking on v1.1** |

## Community — firmware

| ID | Project | Class | Commit / ref at snapshot | Licence | Establishes |
|---|---|---|---|---|---|
| **S14** | `BruceDevices/firmware` (formerly `pr3y/Bruce`) | community | `1d555e0d5b201cc91ad201ac40c2482ec00d1ac1`, 2026-08-28 | **AGPL-3.0** | independent pin map; runtime ADV detection at `0x34`; ES8311 addr `0x18`; ADV pin menus |
| S16 | `bmorcelli/Launcher` (formerly `M5Stick-Launcher`) | community | `3b91484efc5f1a392fac2c4d6066d8306409c688`, 2026-09-04 | MIT | `CardputerADV.md` — independent confirmation of 7×8 matrix, `0x34`, G8/G9/G11; ⚠ contains an I²C-address error |
| **S17** | `meshtastic/firmware` | community | `be2f68b5af806332c9d877d1643007771bd10c36`, 2026-09-03 | GPL-3.0 | `variant.h` — independent confirmation of **`GPS_TX_PIN 13` / `GPS_RX_PIN 15`**, LoRa pins, `KB_INT 11` |
| S18 | `justcallmekoko/ESP32Marauder` | community | `91724fd8e964cb6f55cd7da60a3320570919de5b`, 2026-08-24 | none declared | separate `_adv` user setup ⇒ ADV is a distinct target |
| S19 | `n0xa/m5stick-nemo` | community | `0b8c5c73d5ccf69355be865b07831d47098dbff4`, 2026-07-15 | NOASSERTION | **no ADV config** — a useful negative |
| S20 | `7h30th3r0n3/Evil-M5Project` | community | pushed 2026-08-20 | **none** | ADV not listed — negative |
| S21 | `echo-lalia/MicroHydra` | community | pushed 2026-08-21 | GPL-3.0 | MicroPython route |
| S22 | `d4rkmen/plai` | community | pushed 2026-08-24 | GPL-3.0 | ADV-only Meshtastic client |
| S23 | `terremoth/awesome-m5stack-cardputer` | community | pushed 2026-09-04 | GPL-3.0 | ecosystem index |
| S24 | GitHub repo search `cardputer` | community | 2026-09-04, **100 results — the API cap** | — | ecosystem scale and the 2026 ADV skew |

## Community — forums

| ID | Where | Class | Date | Establishes | Evidence type |
|---|---|---|---|---|---|
| **S15** | r/CardPuter, *"Meshtastic client firmware for the Cardputer ADV — full Unicode on 240x135 with no PSRAM"* — `old.reddit.com/r/CardPuter/comments/1vcxsv8/` | community | **2026-08-01** | the no-PSRAM constraint and a concrete workaround | firsthand engineering account |
| S25 | r/CardPuter `…/1rgdwl0/` Plai first beta + comments | community | 2026-02-27, comments to 2026-08-29 | ADV Meshtastic works; **arrow-key regression 2026-08-29** | firsthand user reports |
| S26 | r/M5Stack `…/1vv4jk3/` *"Cardputer adv black screen only when turning it on"* | community | 2026-08-22 | an unresolved hardware fault report | single anecdote |
| S27 | r/M5Stack `…/1vgmcvn/` *"Search for screws and buttons … for repair"* | community | 2026-08-05 | spares availability | firsthand ownership problem |
| S28 | r/CardPuter `…/1tsr5ke/` *"Guys I messed up big time"* + 74 comments | community | 2026-05-31 | ADV-vs-Zero positioning as owners understand it | opinion / firsthand ownership |
| S29 | r/CardPuter `…/1uclhoi/` Cap TFT-2.8, ↑989 | community | 2026-06-22 | community CAP hardware exists and is popular | demonstrated project |
| S30 | r/meshtastic `…/1rr1r8b/` *"…lora cap for 55 bucks total"* | community | 2026-03-11 | pre-Mesh-Kit purchase reasoning | discussion |
| S31 | r/M5Stack `…/1w6qzfu/` *"cardputer adv or t embed c1101 plus?"* | community | **2026-09-04** | live cross-shopping | discussion |
| — | **`community.m5stack.com`** | primary | — | **could not be searched** — `/api/search` returns `401 not-authorised`, `/search` 302s to login (per `vendors/m5stack` §5.3) | **no determination possible** |

## Repository cross-references

| Record | Why |
|---|---|
| [`vendors/m5stack`](../../../vendors/m5stack/README.md) | documentation-sourcing patterns; every technique it describes was re-verified here |
| [`devices/nicolai-electronics/tanmatsu`](../../nicolai-electronics/tanmatsu/README.md) | comparison target |
| [`devices/m5stack/cap-lora-1262`](../cap-lora-1262/README.md), [`cap-cc1101`](../cap-cc1101/README.md) | the CAP modules — **owned by a sibling session** |
| [`guides/markets/`](../../../guides/markets/README.md) | genre guidance |

## Sources deliberately not used

* Vendor marketing prose for any electrical claim. Where prose and code disagreed, code won —
  four times (§C1 in [`gaps-and-conflicts.md`](gaps-and-conflicts.md) is the clearest case).
* Any AI-generated summary, aggregator page or SEO listicle.
* Reddit vote counts as evidence of correctness. They appear only as evidence of *attention*.
