# Sources — Waveshare ESP32-S3-ePaper-3.97

> Retrieval date for every row: **2026-09-01**, unless stated otherwise.
> `Class` is authority (`primary` / `credible mirror` / `community`);
> `Medium` is format. Where a publisher gives no version or date, the cell reads
> **`unknown`** rather than being omitted.

## Primary — Waveshare

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope / limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| `S01` | ESP32-S3 3.97inch e-Paper Development Board | Waveshare | primary | store listing | `https://www.waveshare.com/esp32-s3-epaper-3.97.htm` | 2026-09-01 | `unknown` — no date on page | SKUs 33552/33810/33811, price USD 34.99–47.99, variant names, package contents, panel specs, onboard-part list | Marketing copy. **Self-contradictory on flash/PSRAM ([C-WS3](gaps-and-conflicts.md#c-ws3--the-storefront-swaps-flash-and-psram))** and names the PMIC `TG28` against the schematic ([C-WS2](gaps-and-conflicts.md#c-ws2--tg28-versus-axp2101)) | `artifacts/source-snapshots/storefront-esp32-s3-epaper-3.97-2026-09-01.html` |
| `S02` | ESP32-S3-ePaper-3.97 — overview | Waveshare Documentation Platform | primary | official docs | `https://docs.waveshare.com/ESP32-S3-ePaper-3.97` | 2026-09-01 | `unknown` — Docusaurus v3.10.2, no doc date | SKU→variant table, feature list, onboard resources, supported frameworks | **This host is the current documentation platform; the legacy `/wiki/` 404s for this product.** No `oldid`-style pinning available | `artifacts/source-snapshots/docs-overview-2026-09-01.html` |
| `S03` | ESP32-S3-ePaper-3.97 — Resources | Waveshare Documentation Platform | primary | official docs | `https://docs.waveshare.com/ESP32-S3-ePaper-3.97/Resources-And-Documents` | 2026-09-01 | `unknown` | The download set: schematic, panel manual, four IC datasheets, GitHub repo, community projects | The single highest-yield page for this product | `artifacts/source-snapshots/docs-resources-2026-09-01.html` |
| `S04` | Storefront search, six query families | Waveshare | primary | store search | `https://www.waveshare.com/catalogsearch/result/?q=…` | 2026-09-01 | n/a | The **seven-product** ESP32 e-paper population used for the survey | Search index, not a catalogue export; a product absent from it is not proven absent | not retained (queries in [`commands.md`](commands.md)) |
| `S05` | `ESP32-S3_e-Paper-3.97-schematic.pdf` | Waveshare | **primary — design data** | schematic | `https://files.waveshare.com/wiki/ESP32-S3-ePaper-3.97/ESP32-S3_e-Paper-3.97-schematic.pdf` | 2026-09-01 | `unknown` — no revision block found in the text layer | **AXP2101 identity, the full GPIO allocation table, the connector census, panel FPC rails** | Altium PDF, 1 sheet, glyph-per-object text. **Text adjacency, not traced connectivity.** No rendered read ([G1](gaps-and-conflicts.md#gaps)) | `artifacts/schematic/ESP32-S3_e-Paper-3.97-schematic.pdf` — 257 550 B, SHA-256 `b12031451374e2333e8eca2b8290c40b4c67955b1f12df17b96f3ee479e6f0be` |
| `S06` | 3.97inch e-Paper — user manual | Waveshare | **primary** | datasheet/manual | `https://files.waveshare.com/wiki/3.97inch_e-Paper_HAT%2B/3.97inch_e-Paper.pdf` | 2026-09-01 | **Rev 1.0, 2025-04-24** ("New creation") | **Driver IC = SSD1677**, active area 86.40 × 51.84 mm, DPI 235, pixel 0.108 mm, 3-/4-wire SPI, refresh and power figures, temperature ranges | **Text layer is offset-encoded** — two subset fonts at +26/+29. Decoded and validated against the cover heading before any value was transcribed ([C-WS10 method note](gaps-and-conflicts.md)) | `components/waveshare/3.97inch-e-paper/artifacts/3.97inch-e-paper-manual-v1.0-2025-04-24.pdf` — 2 774 287 B, SHA-256 `4f756734dbfa7485c57e7ab7124f59f0afb00ca2600cda24a2285f02e4ab05cf` |
| `S07` | Legacy wiki 404 for this product | Waveshare | primary | wiki | `https://www.waveshare.com/wiki/ESP32-S3-ePaper-3.97` | 2026-09-01 | n/a | **Negative result**: HTTP 404. The product was never on the legacy wiki, or was migrated off it | A 404 on the deprecated host is **not** evidence of product-level absence — see [C-WS10](gaps-and-conflicts.md#c-ws10--first-pass-recorded-absences-that-are-not-real) | not retained |
| `S08` | `E-Paper_ESP32_Driver_Board` wiki page | Waveshare | primary | wiki | `https://www.waveshare.com/wiki/E-Paper_ESP32_Driver_Board` | 2026-09-01 | revisions dated 20220728, 20241230 | The driver board's specs, fixed pin map and 23-model panel compatibility list; establishes the legacy wiki still serves 200 for *older* products | Used for the [sibling stub](../e-paper-esp32-driver-board/README.md) | not retained |

## Primary — Waveshare source code

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Scope / limitations |
|---|---|---|---|---|---|---|---|---|---|
| `S09` | `waveshareteam/ESP32-S3-ePaper-3.97` | Waveshare | **primary — source** | repository | `https://github.com/waveshareteam/ESP32-S3-ePaper-3.97` | 2026-09-01 | commit **`9b12d40731a80213b927ee8a421cae4082952819`**, 2026-03-20; repo created 2026-02-04; default branch `main`; **no `LICENSE` file — licence `unknown`** | E-paper pin map (`DEV_Config.h:49–54`), AXP2101 identity and charge configuration (`axp_prot.cpp`), example inventory, factory firmware images | Read via GitHub API at the pinned commit. **Tree listing and four files read; the examples themselves were not cloned** ([G2](gaps-and-conflicts.md#gaps)) |

## Component-manufacturer documents obtained via Waveshare

Filed under `components/` because **a document is filed by what it describes**, not
by who served it. Waveshare's copy is retained where it differs from the original.

| ID | Document | Publisher | Class | URL | Retrieved | Version | Local path | Note |
|---|---|---|---|---|---|---|---|---|
| `S10` | ES8311 datasheet | Everest Semiconductor, via Waveshare | **credible mirror** | `https://files.waveshare.com/wiki/common/ES8311.DS.pdf` | 2026-09-01 | `unknown` | `components/everest-semiconductor/es8311/artifacts/es8311-datasheet-waveshare-mirror.pdf` | 729 315 B, SHA-256 `be42a2cb…`. Everest original not obtained this pass |
| `S11` | PCF85063A datasheet | NXP, via Waveshare | **credible mirror** | `https://files.waveshare.com/wiki/common/Pcf85063atl1118-NdPQpTGE-loeW7GbZ7.pdf` | 2026-09-01 | **Rev. 6, 2015** | `components/nxp/pcf85063a/artifacts/pcf85063a-datasheet-rev6-waveshare-mirror.pdf` | 535 722 B, SHA-256 `93b38487…`. **Stale** — KB already holds NXP Rev. 7 (2018). Both kept: [C-WS11](gaps-and-conflicts.md#c-ws11--waveshare-mirrors-a-nine-year-old-rtc-datasheet) |
| `S12` | SHTC3 datasheet | Sensirion, via Waveshare | **credible mirror** | `https://files.waveshare.com/wiki/common/SHTC3_Datasheet.pdf` | 2026-09-01 | `unknown` | `components/sensirion/shtc3/artifacts/shtc3-datasheet-waveshare-mirror.pdf` | 928 256 B, SHA-256 `d315fe3d…` |
| `S13` | AXP2101 datasheet V1.4 EN | X-Powers, via `lewisxhe/XPowersLib` | **credible mirror** | `https://raw.githubusercontent.com/lewisxhe/XPowersLib/master/datasheet/AXP2101_Datasheet_V1.4_en.pdf` | 2026-09-01 | **V1.4, English** | `components/x-powers/axp2101/artifacts/axp2101-datasheet-v1.4-en-xpowerslib-mirror.pdf` | 1 554 740 B, SHA-256 `9e51d16d…`. **X-Powers publishes no accessible primary URL found this pass**; two direct attempts failed ([acquisition](acquisition/manifest.json)) |

## Community

Non-authoritative. Listed with what each actually demonstrates.

| ID | Title | Author | Class | Medium | URL | Retrieved | Evidence type | Establishes |
|---|---|---|---|---|---|---|---|---|
| `S14` | Rustmix Wave v1.0.0 — open-source Rust firmware | `aimindseye` | community | repository + forum post | `https://github.com/aimindseye/rustmix-wave` · `https://www.reddit.com/r/esp32projects/comments/1tyngwy/` | 2026-09-01 | **demonstrable project** | Third-party firmware for this exact board exists — so the hardware is programmable outside the vendor stack. Linked from Waveshare's own docs `S03` | 
| `S15` | Folloup Sticky | `alxv2016` | community | repository + model listing | `https://github.com/alxv2016/folloup-sticky/tree/folloup-waveshare` · `https://makerworld.com/en/models/3180226-folloup` | 2026-09-01 | **demonstrable project** | An enclosure and application built on this board |
| `S16` | `78/xiaozhi-esp32` | `78` | community | repository | `https://github.com/78/xiaozhi-esp32` | 2026-09-01 | **upstream of a vendor-shipped binary** | Waveshare ships two prebuilt xiaozhi images for this board and points at this repo as the source of truth |

Neither `S14` nor `S15` was cloned or built in this pass; both are recorded as
catalogued-not-inspected. **No prevalence claim is made** — two projects linked by
the vendor is not a measure of community size.

## Cross-record sources used for comparison

| ID | What | Where |
|---|---|---|
| `S17` | DKE `DEPG0397BBS770F3` panel record — active area, DPI, SSD1677, register-derived gate/source orientation | [`components/dke/depg0397bbs770f3`](../../../components/dke/depg0397bbs770f3/README.md) |
| `S18` | SSD1677 controller record | [`components/solomon-systech/ssd1677`](../../../components/solomon-systech/ssd1677/README.md) |
| `S19` | M5Stack PaperMono record and its performance/comparison pages | [`devices/m5stack/papermono`](../../m5stack/papermono/README.md) |
| `S20` | Waveshare documentation-sourcing guide | [`vendors/waveshare`](../../../vendors/waveshare/README.md) |

## Failed and negative retrievals

Recorded because they save the next pass the attempt.

| Target | URL | Result | Reading |
|---|---|---|---|
| Wiki page | `waveshare.com/wiki/ESP32-S3-ePaper-3.97` | **404** | Product not on legacy wiki; use `docs.waveshare.com` |
| `docs` for driver board | `docs.waveshare.com/E-Paper-ESP32-Driver-Board` | **404** | Older products remain on the legacy wiki only — the two hosts are **disjoint**, not layered |
| `docs` for PhotoPainter | `docs.waveshare.com/ESP32-S3-PhotoPainter` | **404** | ditto |
| e-paper category page | `waveshare.com/product/displays/e-paper.htm` | 200 but **zero product links** | Category pages are JS-rendered; **use `/catalogsearch/result/?q=`** |
| AXP2101 datasheet | `files.waveshare.com/wiki/common/AXP2101.pdf` | **404**, body is XML | Not in Waveshare's common pool |
| AXP2101 datasheet | `github.com/lewisxhe/XPowersLib/raw/master/datasheet/AXP2101_Datasheet_V1.0_en.pdf` | **404**, body is HTML | Wrong filename — actual is `_V1.4_en.pdf`. **Neither was saved under a `.pdf` name** |

## Validation performed

Every retained binary was validated **by content, never by HTTP status**:

```
%PDF-  ESP32-S3_e-Paper-3.97-schematic.pdf        257 550 B
%PDF-  3.97inch_e-Paper.pdf                     2 774 287 B
%PDF-  ES8311.DS.pdf                              729 315 B
%PDF-  Pcf85063atl…pdf                            535 722 B
%PDF-  SHTC3_Datasheet.pdf                        928 256 B
%PDF-  AXP2101_Datasheet_V1.4_en.pdf            1 554 740 B
```

Two candidate downloads failed this check and were **deleted rather than kept under a
misleading extension** — see the table above. Commands in [`commands.md`](commands.md).
