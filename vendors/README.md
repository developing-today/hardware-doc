# Vendor documentation-sourcing guides

Manufacturer-level, **reusable** knowledge about where each vendor publishes primary documentation, what its URL patterns are, how those patterns have changed over time, and how to recover when a naive guess fails.

These guides are deliberately separate from the per-part records under [`components/`](../components/README.md). A component record answers *"what is this part and how is it wired on our board"*; a vendor guide answers *"how do I obtain any document from this manufacturer, for any part, next time"*.

For **board vendors and marketplaces** — where to *buy* rather than where to *read* — see
[`guides/markets/vendor-comparison.md`](../guides/markets/vendor-comparison.md).

---

## Board and device vendors

| Vendor | Guide | Devices we document |
|---|---|---|
| Espressif Systems | [espressif/](espressif/README.md) | [All five ESP32-P4 boards](../devices/README.md#espressif--official-esp32-p4-development-boards) |
| Waveshare Electronics | [waveshare/](waveshare/README.md) | [ESP32-S3-Knob-Touch-LCD-1.8](../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |
| **Soldered Electronics** (ex-*e-radionica*) | [soldered-electronics/](soldered-electronics/README.md) | [Inkplate 5](../devices/soldered-electronics/inkplate-5/README.md) · [Inkplate 5 Gen 2](../devices/soldered-electronics/inkplate-5-gen2/README.md) |
| **Zerowriter** | [zerowriter/](zerowriter/README.md) | [ZeroWriter Ink](../devices/zerowriter/zerowriter-ink/README.md) · [Zerowriter Fold](../devices/zerowriter/zerowriter-fold/README.md) |
| **M5Stack** | [m5stack/](m5stack/README.md) | [PaperMono](../devices/m5stack/papermono/README.md) · [DinMeter](../devices/m5stack/dinmeter/README.md) · [Cardputer family](../devices/README.md#cardputer-family--added-2026-09-04) · [Cardputer expansions](../devices/README.md#cardputer-expansions--lora-sub-ghz-and-nfc--added-2026-09-04). Updated 2026-09-04 (§11) by the DinMeter pass: the **re-served-asset trap** (byte-identical schematics/STLs under new SKU names), `sitemap.xml` as the only working enumeration route, the `id="document"` extraction recipe, shop `.js` JSON and the **`[EOL]` title prefix** as the lifecycle signal, Shopify serving **JPEG under `.webp` URLs**, the Altium **double-draw** glyph trap, and confirmation that specification rows are carried over unedited between product generations |
| **LilyGO / TTGO** | [lilygo/](lilygo/README.md) | [T-Display-S3 family](../devices/README.md#lilygo-shenzhen-xin-yuan-electronic-technology-also-trades-as-ttgo) · [T-Display K230](../devices/lilygo/t-display-k230/README.md). ⚠ **No portal or wiki: everything is GitHub + a Shopify feed.** Covers the public `products.json` feed (the only source of launch dates and revision-bearing SKU titles), the **default branch is often not `main`** trap, inconsistent/absent repository licences, the three pin-header filenames, Altium Form-XObject PDF extraction, **offset text layers in Chinese-vendor datasheets**, and why the closed issue tracker *is* the documentation. ⚠ **LilyGO stock codes collide with chip part numbers** — `K230` is a SKU for an ESP32-S3 board |
| **Xteink** (Shenzhen Xiaohu Xingtong Technology) | [xteink/](xteink/README.md) | [Xteink family](../devices/README.md#xteink-阅星瞳--星瞳-star-pupil) — X3 · X4 · X4 Pro · X4 Classic · [X4 Light](../devices/xteink/x4-light/README.md) · S4 · Nano. ⚠ **Publishes no datasheet, schematic, wiki or support portal — only a stock Shopify store.** Covers the unauthenticated `products.json` / `collections.json` / `<handle>.js` endpoints that are the only source of launch dates, SKUs and stock; the **empty-`body_html` trap** (the X4 Classic's spec table exists only in the rendered HTML); `compare_at_price` and `grams` being neither a former price nor the device mass; and ⭐ **enumerating the FCC grantee code `2BTR9` rather than the product name**, which returns every device the vendor has certified **including ones it never announced** — that is how the X4 Light was found. Plus the **inverted Cloudflare block on `fccid.io`** (403 to Chrome, 200 to `curl`). *Added 2026-09-11* |
| **Solder Party** | [solder-party/](solder-party/README.md) | *none documented yet* — anticipatory guide. Small open-hardware company (Malmö, Sweden; arturo182) |
## Component vendors — parts we document

| Vendor | Guide | Parts we track |
|---|---|---|
| Espressif Systems | [espressif/](espressif/README.md) | [ESP32-P4](../components/espressif/esp32-p4/README.md) · [ESP32-S3R8](../components/espressif/esp32-s3r8/README.md) · [ESP32-U4WDH](../components/espressif/esp32-u4wdh/README.md) |
| Texas Instruments | [texas-instruments/](texas-instruments/README.md) | [DRV2605L](../components/texas-instruments/drv2605l/README.md) · [DRV2605](../components/texas-instruments/drv2605/README.md) · [PCM5100A](../components/texas-instruments/pcm5100a/README.md) · [TLV62569DBVT](../components/texas-instruments/tlv62569dbvt/README.md) · [TPS65186](../components/texas-instruments/tps65186/README.md) |
| **NXP Semiconductors** | [nxp/](nxp/README.md) | [PCAL6416A](../components/nxp/pcal6416a/README.md) · [PCF85063A](../components/nxp/pcf85063a/README.md). ⚠ **`nxp.com` blocks browser UAs and allows the default `curl` UA** |
| **E Ink Holdings** | [e-ink/](e-ink/README.md) | [ED052TC4 / ED052TC2](../components/e-ink/ed052tc4/README.md). ⚠ **No public panel datasheets; `eink.com` returns the same 200 for every path** |
| Winbond | [winbond/](winbond/README.md) | [W25Q128JVPIQ](../components/winbond/w25q128jv/README.md) |
| Sitronix | [sitronix/](sitronix/README.md) | [ST77916](../components/sitronix/st77916/README.md) · [ST7789VW](../components/sitronix/st7789vw/README.md) · [ST7701S](../components/sitronix/st7701s/README.md) |
| **Jadard Technology** | [jadard/](jadard/README.md) | [JD9365](../components/jadard/jd9365/README.md). ⚠ **No vendor portal at all** — documents come from Espressif's CDN and an LCD reseller. `lcddisplay.co` **403s browser UAs**; a `WhatsApp/2.23.20.0` UA works |
| **Fitipower Integrated Technology** | [fitipower/](fitipower/README.md) | [EK79007AD](../components/fitipower/ek79007ad/README.md) · [EK73217BCGA](../components/fitipower/ek73217bcga/README.md). ⚠ Espressif serves **two different EK79007 revisions from two CDN paths**; PDF `Title` metadata is wrong on every document |
| **Ilitek (ILI Technology)** | [ilitek/](ilitek/README.md) | [ILI9881C](../components/ilitek/ili9881c/README.md). ⚠ `internetsomething.com` **520s browser UAs**; WhatsApp UA works. Ilitek **does** publish its paged register map — unusually |
| Hynitron | [hynitron/](hynitron/README.md) | [CST816D](../components/hynitron/cst816d/README.md) |
| WCH (Nanjing Qinheng) | [wch/](wch/README.md) | [CH445P](../components/wch/ch445p/README.md) · [CH340X USB-UART bridge](../components/wch/ch340x/README.md) |
| MEMSensing | [memsensing/](memsensing/README.md) | [MSM261D4030H1CPM](../components/memsensing/msm261d4030h1cpm/README.md) |
| SGMicro | [sgmicro/](sgmicro/README.md) | [SGM2036-3.3](../components/sgmicro/sgm2036-3.3/README.md) |
| Alpha & Omega Semiconductor | [alpha-and-omega-semiconductor/](alpha-and-omega-semiconductor/README.md) | [AO3400A](../components/alpha-and-omega-semiconductor/ao3400a/README.md) |
| Alps Alpine | [alps-alpine/](alps-alpine/README.md) | [SSCM110100](../components/alps-alpine/sscm110100/README.md) |
| **Semtech** | [semtech/](semtech/README.md) | [SX1262](../components/semtech/sx1262/README.md) · [SX1276](../components/semtech/sx1276/README.md) · [SX1268](../components/semtech/sx1268/README.md) · [LLCC68](../components/semtech/llcc68/README.md) · [LR11x0](../components/semtech/lr11x0/README.md) · [LR1121](../components/semtech/lr1121/README.md) · [LR2021](../components/semtech/lr2021/README.md). ⚠ **Documents are not on `semtech.com`.** They are behind a Salesforce content-distribution shell that is `blocked` for automated clients — HTTP 200 for valid *and* invalid tokens. Use **Digi-Key** or **Mouser** (⚠ Mouser needs the WhatsApp UA). ⭐ A **1 984-entry JSON document catalogue** is embedded in one page and is the only complete enumeration. `www.semtech.com/uploads/documents/` **soft-404s** — 200 + HTML for every path, including invented ones |
| **Canaan Creative (Kendryte)** | [canaan/](canaan/README.md) | [K230](../components/canaan/k230/README.md) — the repository's first RISC-V part. Documentation is **Markdown in a Git repository**, not PDFs on a portal. ⚠ Key trap: the **`en/` tree contains no binary hardware artifacts; the `zh/` tree carries every schematic, Gerber and BOM.** Three of four Canaan repositories use a non-obvious default branch (`dev`, `canmv_k230`) |
| [DKE](dke/README.md) | e-paper display modules | [DEPG0397BBS770F3](../components/dke/depg0397bbs770f3/README.md) |
| [Everest Semiconductor](everest-semiconductor/README.md) | audio codecs | [ES8156](../components/everest-semiconductor/es8156/README.md) · [ES8311](../components/everest-semiconductor/es8311/README.md) |
| [OmniVision](omnivision/README.md) | CMOS image sensors | [OV2640](../components/omnivision/ov2640/README.md) · [OV3660](../components/omnivision/ov3660/README.md) · [OV5640](../components/omnivision/ov5640/README.md) |
## Component vendors — datasheets held, README record outstanding

These vendors have **no `README.md` component record**, but this repository **does hold retrieved
datasheets** for them. Almost all were extracted from the `SensorLib/datasheet/` directory bundled in
the Waveshare demo archive — see [vendored-deps § Datasheet disposition](../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/vendored-deps/README.md#datasheet-disposition).

⚠️ **None of these parts is fitted on any device documented here.** They are parts a bundled library
supports. Do not infer a board fitment from their presence.

| Vendor | Guide | Parts held (artifact only) |
|---|---|---|
| NXP Semiconductors | [nxp/](nxp/README.md) | `PCF8563` (Rev. 11) — I²C RTC, artifact only. *(`PCAL6416A` and `PCF85063A` now have full records — see the table above.)* |
| Goodix | [goodix/](goodix/README.md) | `GT911` (Rev. 1.0) — the most likely touch-controller substitution on a clone of our board |
| Chipsemi | [chipsemi/](chipsemi/README.md) | `CHSC5816` (V1, Chinese) — also not register-compatible with our part |
| QST | [qst/](qst/README.md) | `QMC6310` (Rev. C) · `QMI8658A` (Rev. A) |
| Bosch Sensortec | [bosch-sensortec/](bosch-sensortec/README.md) | `BMA423` |
| Lite-On | [lite-on/](lite-on/README.md) | `LTR-553ALS-01` — held **despite every Lite-On host being unreachable on 2026-08-24** |
| Capella Microsystems | [capella-microsystems/](capella-microsystems/README.md) | `CM32181A3OP` + application note — held despite the vendor site being a degraded remnant |
| XLSEMI | [xlsemi/](xlsemi/README.md) | `XL9555` (Rev. 2.3) — an **I/O expander**, which corrected our assumption about this vendor's catalogue |
| Haoyu Microelectronics | [haoyu/](haoyu/README.md) | `HYM8563` RTC. ⚠️ **Not** HAOYU Electronics the retailer — see that guide's §8 |

There is also a vendor-neutral [ALS/proximity selection guide](../components/generic/ambient-light-and-proximity-sensor-selection/artifacts/ambient-light-and-proximity-sensor-selection-zh.pdf) (Chinese) from the same bundle.

**Writing these component records is outstanding work**, tracked here so the gap is visible rather than silent.

---

## Cross-cutting findings

Patterns that recur across vendors, worth knowing before you start on a new one:

- **HTTP 200 does not mean the document exists.** [WCH](wch/README.md) returns an identical
  4,305-byte SPA shell for *every* path; [SGMicro](sgmicro/README.md) soft-404s; Espressif's doc
  platform serves a 13,745-byte app shell. **Always check byte size and magic bytes**, and probe a
  deliberately bogus path as a negative control.
- **The manufacturer is often not the best documentation source.** [Sitronix](sitronix/README.md) came
  from Espressif's CDN; [Hynitron](hynitron/README.md) from Waveshare's mirror;
  [MEMSensing](memsensing/README.md) from LCSC's. For Chinese component vendors, **try LCSC first**.
- **Some URL patterns are genuinely constructible** — [TI](texas-instruments/README.md)'s
  `lit/ds/symlink/<part>.pdf`, [AOS](alpha-and-omega-semiconductor/README.md)'s
  `res/data_sheets/<PART>.pdf`, [Bosch](bosch-sensortec/README.md)'s datasheet path. Most are not.
- **Suffix letters mislead.** Espressif's `H` means a *narrower* temperature range;
  [`DRV2605` ≠ `DRV2605L`](texas-instruments/README.md); `W25Q128` is 128 **Mbit**.
- **Driver source is sometimes the best available primary evidence**, and this repository treats it as
  such where a register manual is unobtainable — see [Sitronix §5](sitronix/README.md#5-documentation-where-it-actually-comes-from).
- Access findings are also recorded in the repository's
  [crawler / site-access table](../ai-crawler-site-access-table.md).

---

## Tool and software vendors

Not hardware manufacturers, but vendors whose tooling is required to build firmware for the devices documented here, and whose distribution channels need the same sourcing discipline.

| Vendor | Guide | What it publishes |
|---|---|---|
| SquareLine Kft. | [squareline/](squareline/README.md) | **SquareLine Studio**, the proprietary drag-and-drop LVGL UI editor. ⚠ The Linux build is **a ZIP, not an AppImage**, `download.squareline.io` **does not exist**, and the real host returns **HTTP 206 for missing files** — `Content-Type` is the only existence signal |

## Conventions for adding a vendor guide

Create `vendors/<vendor-slug>/README.md` and cover at minimum:

1. **Portal structure** — every host the vendor serves documents from, and what each host is for.
2. **URL templates** — concrete, copy-pasteable patterns with placeholders, plus at least one verified working example **and a negative control**.
3. **Migrations and breakage** — documents that moved between hosts or path schemes, because that is the single most common cause of a failed download.
4. **Per-part enumeration checklist** — the full set of document classes the vendor publishes, so research is exhaustive rather than opportunistic.
5. **Gotchas** — SPA shells, soft 404s, redirects, unstable `latest` aliases, language variants.
6. **Validation** — how to prove a downloaded byte stream is the document it claims to be.
7. **Product lines, market position and part-numbering conventions** — so a reader can decode an unfamiliar part number and judge what a BOM choice signals.
8. **A table linking to every component and device of theirs we document**, and back-links from those records.
9. **An explicit evidence boundary** — state plainly what was verified, when, and what is inference or recollection.

Retrieval discipline for any artifact stored under a component's `artifacts/` directory: record URL, retrieval date, version/build identifier, byte size and SHA-256, and validate the file's magic bytes before committing it.

---

## Related

- [Hardware research index](../README.md) · [Components](../components/README.md) · [Devices](../devices/README.md) · [Guides](../guides/README.md)
- [Marketplace / sourcing comparison](../guides/markets/vendor-comparison.md) · [Clones and variants](../guides/markets/clones-and-variants.md)

| [Seeed Studio](seeed-studio/README.md) | XIAO series, Grove, reTerminal, SenseCAP | **The wiki is a GitHub repo** (`Seeed-Studio/wiki-documents`, branch `docusaurus-version`) — the rendered site is a JS shell with one link. Design files are **CC BY-SA 4.0**. Known crossed-document-ID error. |
| [Soldered Electronics](soldered-electronics/README.md) | Inkplate e-paper series, Qwiic/easyC breakouts, Dasduino | **GitHub is the real documentation**, not the website — `Soldered-<Product>-hardware-design` repos carry KiCad, BOM CSVs, gerbers, 3D *and* CE/UKCA certificates. Hardware is **TAPR OHL** but GitHub reports `NOASSERTION`. Org has 200+ repos — paginate. `inkplate.readthedocs.io` is a **JS redirect shim**; use the `.rst` source. |
| [Zerowriter](zerowriter/README.md) | ZeroWriter Ink, Zerowriter Fold | ⚠ **`zerowriter.com` is a parked for-sale domain — the real site is `zerowriter.ink`**, found only inside a firmware readme. Site 403s a Chrome UA on `/pages/*`; ClaudeBot UA works. **Website is authoritative for firmware, GitHub for hardware.** |
