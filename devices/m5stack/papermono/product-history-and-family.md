# Product history, family and culture — M5Stack PaperMono

> Research snapshot **2026-09-01**, eleven days after launch. Every date below comes from a
> machine-readable field — a Shopify `published_at`, a GitHub API `created_at`, a PDF `ModDate`,
> a JSON-LD `datePublished`, a schematic title block or an `esp_app_desc_t` — rather than from
> prose that says "in August". Where a date is an approximation of something else, that is said.
>
> The README carries a nine-row summary of this timeline. **This page is the evidenced version**:
> what each row rests on, what it does and does not establish, and the family comparison in full.

## Contents

- [1. The timeline, row by row, with its evidence](#1-the-timeline-row-by-row-with-its-evidence)
- [2. What the design dates tell you](#2-what-the-design-dates-tell-you)
- [3. The M5Paper family](#3-the-m5paper-family)
- [4. PaperMono is not a successor to the PaperS3](#4-papermono-is-not-a-successor-to-the-papers3)
- [5. What is shared across the family, and what is not](#5-what-is-shared-across-the-family-and-what-is-not)
- [6. PaperMono and PaperMono-Lite](#6-papermono-and-papermono-lite)
- [7. Positioning, audience and product culture](#7-positioning-audience-and-product-culture)
- [8. What is not established](#8-what-is-not-established)

---

## 1. The timeline, row by row, with its evidence

All timestamps normalised to UTC where the source carried a zone.

| Date (UTC) | Event | Evidence | What it establishes — and what it does not |
|---|---|---|---|
| **2026-04-14** | KEY/RGB sub-board schematic dated | Sheet 5 title block, `PaperMono KEY RGB.SchDoc` (S14) | The sub-board carrying both user keys, the power button, the RGB LED and the PDM microphone was drawn by this date. It is a *title-block* date — the date someone typed, not a commit |
| **2026-05-07** | `m5stack/M5PaperMono-UserDemo` repository created on GitHub | GitHub API `created_at` (S41) | **The earliest public trace of the product**, 3½ months before launch. Creation of an empty or private-then-public repo, not publication of its contents |
| **2026-05-22** | Main schematic **V0.6.2** dated | Filename `PaperMono_SCH_V0.6.2_20260522.pdf` (S14) | The revision in the published PDF. A filename date; the PDF itself was created later |
| **2026-06-08** | Schematic PDF created | PDF `CreationDate` (S14) | When the export was produced — 17 days after the design date it carries |
| **2026-07-28** | NFC sub-board schematic **V0.2** dated; schematic PDF last modified | Sheet 6 title block and PDF `ModDate` (S14) | The NFC sub-board is the **latest-revised** part of the design. The PDF was re-exported the same day the NFC sheet is dated, which is why the NFC sheet is V0.2 while the main project is V0.6.2 |
| **2026-08-06 16:12:13** | Factory firmware image built | `esp_app_desc_t` in the shipped binary (S38) | An exact build timestamp from the artifact itself — the most precise date in this table. Built from an **uncommitted tree** ([`factory-firmware.md` §6](factory-firmware.md#6-why-c78f6c5-dirty-means-not-reproducible)) |
| **2026-08-10 17:28:58 +08:00** | `M5PaperMono-UserDemo` HEAD commit `c1099107…` ("update firmware v1.2") | GitHub API (S41) | The published source moved **four days after** the shipped image was built, and does not correspond to it |
| **2026-08-17** | Leak: r/M5Stack post "Paper Mono coming August 21st", citing an M5Stack YouTube Short | Reddit (S70) | The launch date was public four days early, **from the vendor's own channel**. In the same thread, third-party library authors claim support — necessarily written against documentation, not hardware |
| **2026-08-18 06:29 UTC** (14:29 +08:00) | Both storefront products created, unpublished | Shopify `created_at` (S48, S49) | The Lite record was created **three minutes before** the PaperMono's (14:26:42 vs 14:29:31 +08:00) |
| **2026-08-18 09:09 UTC** (17:09 +08:00) | Factory firmware uploaded to M5Burner as v1.2 | M5Burner API `uploadedAt` (S33, S34) | Twelve days after the image was built |
| **2026-08-20** | `m5stack/M5PaperMono-OTP-Demo` repository created | GitHub API (S42) | The panel-maker OTP waveform example — the code M5Stack recommends **over its own graphics library** — appeared one day before launch |
| **2026-08-20** | Documentation published under category "Controllers" | `/en/history` (S13) | The docs release date, distinct from both Shopify dates. Also the mechanical drawing's PDF `CreationDate`/`ModDate` (S15) |
| **2026-08-21 04:00 UTC** (12:00 +08:00) | **Store publishes both SKUs**; vendor blog announcement | Shopify `published_at` (S48, S49); blog `<time datetime>` (S50) | The commercial launch instant. The Lite published **one second before** the PaperMono (12:00:09 vs 12:00:10) |
| **2026-08-21 04:09 UTC** | First independent buyer reports the Lite already sold out — **nine minutes later** | @henry19840301, with four photographs (S72) | The checkable fact is a **9-minute gap** between publication and a sell-out report. The poster's own phrase was "sold out in just one second"; that is colloquial, and the nine minutes is what the evidence supports |
| **2026-08-21 05:19 UTC** | LinuxGizmos article published — **1 h 19 min after the store**, but with a **byline dated Aug 20** | JSON-LD `datePublished` (S76) | The byline predating publication is consistent with an embargoed press push. It does **not** establish that the article was written before launch, only that a date field says so |
| **2026-08-21 04:12 UTC** (06:12 +02:00) · **10:15 UTC** (11:15 +01:00) | OpenELAB (.io, then .de a minute later) and The Pi Hut list the product | Shopify `created_at` (S53–S55) | Resellers listed within hours — OpenELAB **twelve minutes** after the store published. None had stock |
| **2026-08-21 06:59 UTC** | M5Stack YouTube "New Arrivals: PaperMono & PaperMono-Lite" | YouTube `uploadDate` (S81) | Vendor video, 16 938 views at snapshot |
| **2026-08-21 08:44 UTC** | M5Stack posts to r/M5Stack; later states pre-orders "reached the limit" | Reddit API (S71) | **A direct vendor statement**, primary, that the batch was capped |
| **2026-08-21 ~12:00 UTC** | First Hacker News submission — 2 points, 1 comment | HN (S69) | Landed ~8 h post-announcement and already out of stock |
| **2026-08-21 16:43 UTC** | CNX-Software article (modified 08-22) | WP REST `date` (S77) | Contains the only two independent observations in any written piece (§7) |
| **2026-08-22 07:49 UTC** | M5Stack X post "PaperMono vs PaperMono-Lite" | fxtwitter API (S75) | Vendor marketing; the thread root of the restock exchange |
| **2026-08-22 10:09 UTC** | @berryxia asks for a restock, reports stock gone the previous day | fxtwitter API (S73) | Second independent failed-purchase report |
| **2026-08-22 10:54 UTC** | **M5Stack replies 「要等两三个月了」 — "you'll have to wait two or three months"** | fxtwitter API (S74) | **The primary vendor restock statement.** It conflicts with CNX-Software's "next year" ([C7](gaps-and-conflicts.md#c7--restock-timing)). Note also: the widely repeated claim that the delay is an e-ink driver IC shortage **does not appear anywhere in this tweet or its reply chain**, which was retrieved in full |
| **2026-08-22 12:44 UTC** (20:44 +08:00) | Community CrossPoint e-reader image uploaded to M5Burner | M5Burner API (S35) | **One day after launch, a third party had working firmware published.** Built 2026-08-22 19:58:33 |
| **2026-08-23 21:48 UTC** | MuyLinux (ES) publishes a translation of the LinuxGizmos piece | JSON-LD (S78) | Re-syndication, not coverage |
| **2026-08-25** | `MagicCube/free-ink-on-paper-mono` created | GitHub API (S89) | First third-party project. Author is the same person as the 2026-08-21 purchase report — ownership corroborated across two surfaces |
| **2026-08-27** | `hectorzin/M5PaperMono-HomeAssistant-ESPHome` created | GitHub API (S93) | ESPHome bring-up, explicitly labelled a test hypothesis by its own author |
| **2026-08-27 17:50 UTC** | Hacker News front page — **162 points, 58 comments** | HN Algolia (S68) | The largest discussion anywhere, and it contains **no firsthand PaperMono measurement at all** |
| **2026-08-28 12:10 UTC** | Liliputing Lilbits roundup mention | JSON-LD (S79) | Contains the "$55 with NFC and LoRa" error (§6) |
| **2026-08-29 16:21 UTC** | **Volos Projects hands-on video** — the only one found | YouTube `uploadDate` (S80) | Day 8. Self-described first look; carries a vendor referral link |
| **2026-08-30** | `MingRZou/PaperMono-Launcher` created | GitHub API (S91) | Self-described hardware-validated; a **port** of a PaperS3 launcher (§4) |
| **2026-08-31** | `EggUncle/PaperMonoCalendar` created | GitHub API (S92) | Honest about showing software-generated previews rather than device photographs |
| **2026-09-01** | **Research snapshot.** Both SKUs still out of stock at the official store | Shopify `product.available = false` (S48, S49) | Out of stock for all but nine minutes of its commercial life |

### What this timeline is not

It is a **reproducible broad-coverage snapshot dated 2026-09-01**, not proof that nothing else
happened. Two things in particular are outside it: `community.m5stack.com` is auth-walled
(`/api/search` → HTTP 401), so the vendor's own forum — the likeliest first home for owner
reports — could not be searched at all; and Mouser, DigiKey and TinyTronics were bot-walled, so
their listing dates are unknown rather than absent.

## 2. What the design dates tell you

Three readings the raw table does not make obvious.

**The product was in the open, quietly, for 3½ months.** The UserDemo repository was created on
2026-05-07 and the schematic is dated 2026-05-22. Anyone watching `github.com/m5stack` had the
product name in May. That is unremarkable for M5Stack but it is the kind of fact that resolves
"when did this leak" questions later.

**The NFC sub-board is the youngest part of the design.** Main project V0.6.2 dated 2026-05-22;
NFC sub-board V0.2 dated 2026-07-28, and the PDF re-exported that same day. Ten weeks of
divergence between the two, on the one sub-assembly whose schematic is also **incomplete in the
published PDF** — the included NFC sheet is explicitly numbered `2/2` and sheet 1 is absent
([G1](gaps-and-conflicts.md#g1--nfc-schematic-sheet-1-of-2-is-not-published)). Those two facts
are consistent with the NFC section being the last thing finished, which is a plausible reason
an export missed a sheet. **`inferred`; there is no statement from M5Stack about it.**

**The published source does not correspond to the shipped firmware, and the dates show it.**
Image built 2026-08-06 from a `-dirty` tree; repository HEAD committed 2026-08-10. Whatever was
in the working tree on 6 August was never published as such. See
[`factory-firmware.md` §6](factory-firmware.md#6-why-c78f6c5-dirty-means-not-reproducible).

**M5Stack develops on an internal GitLab and publishes to GitHub.** Both demo repositories have
squashed three-commit histories and the OTP demo's HEAD message is literally
`Merge GitLab initial history`. Upstream history is therefore **not available** — which is why
`created_at` on a GitHub repo is the earliest date this record can offer rather than a real
project start.

## 3. The M5Paper family

Every row from M5Stack's own storefront JSON (`shop.m5stack.com/products/<handle>.json`) and
documentation pages, retrieved **2026-09-01**.

| Product | SKU | Store price 2026-09-01 | Storefront published | Store status | Display | Notes |
|---|---|---|---|---|---|---|
| **CoreInk** | `K048` | USD 29.90 | 2020-11-06 | active | 1.54" e-paper | Not a "Paper"-series device; included so the e-paper line is complete |
| **M5Paper** | `K049` | USD 85.00 | **2020-11-27** | **`[EOL]`** in title | 4.7", 960 × 540 | **ESP32**, not S3 |
| **M5Paper V1.1** | `K049-B` | USD 85.00 | 2021-06-23 | active | 4.7", 960 × 540 | Still listed as non-EOL although the original is EOL |
| **M5Paper COMM Edition** | `K049-C` | USD 79.00 | 2022-01-17 | **`[EOL]`** | 4.7" | Comms-oriented variant |
| **M5PaperS3** | `C139` | USD 59.00 | **2024-12-13** | **`[EOL]`** | 4.7" `EPD_ED047TC1`, 960 × 540, **16-level** grey, GT911 two-point touch | ESP32-S3R8, **1800 mAh**, BM8563 RTC, BMI270, 1 button, no frontlight, HC1.25-4PLT expansion port |
| **M5Paper Color** | `C151` | USD 75.00 | 2026-05-15 | active | 4" E Ink **Spectra 6** `ED2208-DOA (EL040EF1)`, 400 × 600 | ESP32-S3R8, 1250 mAh, ES8311 codec + speaker + mic, SHT40, 3 user buttons, RX8130CE RTC |
| **PaperMono** | `C153` | USD 65.00 | **2026-08-21** | active, out of stock | 3.97" `SSD1677`, 480 × 800, **4-level** grey, FT6336G touch, **frontlight** | ESP32-S3R8, 1150 mAh, NFC + LoRa, BMI270, **M5PM1** PMIC, **M5IOE1** expander, RX8130CE RTC, PDM mic |
| **PaperMono-Lite** | `C153-LITE` | USD 55.00 | **2026-08-21** | active, out of stock | same panel, touch and frontlight | Identical **minus NFC and LoRa**. 72.4 g against 74.7 g |

> **`published_at` is a proxy, and here is why it is a good one for this vendor.** Shopify does
> not expose an availability date, only when the storefront record went public. For PaperMono
> that timestamp agrees to within an hour with the vendor blog post, the vendor YouTube upload
> and the first independent buyer report — three unrelated sources. That validation was done for
> the one product where it was possible; for the 2020–2024 rows the proxy is **unvalidated** and
> should be read as "the store record went live then", not "the product shipped then".

> **The original M5Paper's display controller is *not* established here.** A commonly repeated
> attribution is `IT8951`. It appears on **no M5Stack page retrieved in this pass**, and
> `docs.m5stack.com/en/core/Paper` is a JavaScript shell that returned no content. Recorded as
> **unverified** rather than repeated. What M5Stack's current documentation does state is that
> the *PaperS3's* panel is `EPD_ED047TC1`.

### What the family table means in practice

Two of the four generations of the 4.7-inch line are **`[EOL]`** at the snapshot date, including
the PaperS3 — the newest of them, published only twenty months earlier. The line M5Stack is
actually selling into today is **not** the 4.7-inch one: it is PaperColor at 4 inches and
PaperMono at 3.97 inches, both smaller, both at lower resolution than the 960 × 540 boards they
replace in the catalogue.

That is the family-level observation worth carrying away: **M5Stack's e-paper line got smaller
and cheaper, not bigger and sharper.** Whether that is component sourcing, cost, or a read of
the market is not established by anything in evidence.

## 4. PaperMono is not a successor to the PaperS3

Several launch articles described it as one, and the naming invites it. **The vendor's own
specification tables contradict it on every measurable display and power axis.**

| | **M5PaperS3** (`C139`) | **PaperMono** (`C153`) | Which is better for that axis |
|---|---|---|---|
| Store price 2026-09-01 | USD 59.00 | USD 65.00 | **PaperS3**, by $6 |
| Store status 2026-09-01 | **`[EOL]`** — not purchasable new | active but **out of stock** | Neither is purchasable |
| Panel | 4.7" `EPD_ED047TC1`, **parallel** interface | 3.97" `SSD1677`, **SPI** | — |
| Resolution | **960 × 540 = 518 400 px** | 480 × 800 = **384 000 px** | **PaperS3 — ~35 % more pixels** |
| Greyscale | **16 levels** | **4 levels** | **PaperS3** |
| Touch | GT911, **two-point + gestures** | FT6336G, single point, active area clipped to X 5–475 / Y 5–795 | **PaperS3** |
| Frontlight | **none** | **integrated** | **PaperMono** |
| Battery | **1800 mAh** | **1150 mAh** | **PaperS3 — ~57 % more capacity** |
| LoRa / NFC | none | **SX1262 868–923 MHz + ST25R3916** | **PaperMono** |
| Microphone | none | **PDM mic** | **PaperMono** |
| User buttons | 1 (power / reset / download) | **2 user + 1 power** | **PaperMono** |
| Expansion port | **HC1.25-4PLT** (3V3 + GND + 2 × GPIO) | **none at all** | **PaperS3** |
| Power management | conventional | **M5PM1 five-state hardware state machine** | **PaperMono** |
| I/O expander | none | **M5IOE1** | depends — capability *and* a mandatory dependency |
| Published power figures | **yes** — 9.28 µA / 949.58 µA / 154.02 mA at DC 4.2 V | **none published** | **PaperS3** ([`performance.md`](performance.md)) |
| Size / weight | 121.5 × 67.7 × 7.7 mm, 89.0 g | 101.0 × 62.0 × 8.0 mm, 74.7 g | **PaperMono** for pocketability |

**This is a trade, not an upgrade, and the direction of the trade is clear.** If the workload is
*rendering* — a reader, a dashboard, a calendar, anything where pixels and grey levels are the
product — the PaperS3 is the better display, has the better battery, and is cheaper. The
PaperMono wins where you need the **radios**, the **frontlight**, the **power architecture**, or
the **size**. Nothing about the newer product supersedes the older one on the axes the older one
was good at.

Two qualifications that matter as much as the table:

- **The PaperS3 is EOL.** So this comparison mostly tells you what the line lost, not what to
  buy. Neither device could be purchased new from M5Stack on 2026-09-01.
- **They are not software-compatible either.** Different panel interface (parallel vs SPI),
  different display controller, different touch controller (GT911 vs FT6336G), different RTC
  (BM8563 vs RX8130CE), and two auxiliary microcontrollers the older board does not have. The
  concrete demonstration is `MingRZou/PaperMono-Launcher` (S91) — an explicit **port** of
  `bmorcelli/Launcher` from the PaperS3. Somebody had to do work; that is what "not a successor"
  means in practice.

The community reached the same conclusion independently and correctly: u/poulpy123 ("More
expensive, smaller screen and lower resolution that the previous version"), and u/Tsixom, whose
spec comparison on r/M5Stack was **checked line by line against `docs.m5stack.com` and is
accurate on every point**. Recorded in
[`gaps-and-conflicts.md`](gaps-and-conflicts.md#claims-examined-and-rejected) as a rejected
claim, and in [`community.md`](community.md) as one of the few community contributions that
survives checking.

## 5. What is shared across the family, and what is not

| Element | Shared with | Not shared |
|---|---|---|
| **ESP32-S3R8** SoC, 16 MB flash, 8 MB octal PSRAM | PaperS3, PaperColor, PaperMono, PaperMono-Lite | The original M5Paper line is plain **ESP32** |
| **BMI270** IMU | PaperS3, PaperMono | PaperColor (no IMU in its spec table) |
| **RX8130CE** RTC | **PaperColor and PaperMono** | PaperS3 uses **BM8563** |
| Product-line **name** | all of them | — |
| Panel, display controller, touch controller | **nothing** — every generation differs | — |
| **M5PM1** power manager, **M5IOE1** expander | PaperMono and PaperMono-Lite only, in this family | Neither appears on PaperS3 or PaperColor. (The M5PM1 does appear elsewhere in M5Stack's catalogue — the site-wide I²C table lists `M5PM1 (0x6e)` for **StickS3 (K150)**) |
| Frontlight | PaperMono and PaperMono-Lite only | — |
| Firmware | **nothing** | Ports are real work (§4) |

The M5PM1 detail is worth pausing on. Its library's `LICENSE` is dated **2025** while both demo
repositories and the M5IOE1 library are dated 2026, and the site-wide I²C address table
independently places an M5PM1 on the StickS3. Together those say the power manager is a
**reusable M5Stack building block that predates this product**, not something designed for it.
`inferred`. That matters for a buyer: it is more likely to be maintained across products than a
one-off, and its documentation quirks
([C12](gaps-and-conflicts.md#c12--m5pm1-manual-internal-inconsistencies)) are quirks you will
meet again on other M5Stack boards.

## 6. PaperMono and PaperMono-Lite

The full variant record is [`../papermono-lite/README.md`](../papermono-lite/README.md). The
family-level facts:

| | PaperMono `C153` | PaperMono-Lite `C153-LITE` |
|---|---|---|
| Price | USD 65.00 | USD 55.00 |
| Case | grey | white |
| NFC (ST25R3916) | yes | **no** |
| LoRa (Stamp LoRa-1262) | yes | **no** |
| Weight | 74.7 g | 72.4 g |
| Schematic asset | `PaperMono_SCH_V0.6.2_20260522.pdf`, **6 sheets** | `PaperMono-Lite_PRJ_V0.6.2_20260522.pdf`, **4 sheets**, `PRJ` not `SCH` — **not retrieved** (S16) |
| Firmware | **the same image**, `PaperMono / PaperMono-Lite UserDemo` | same |
| Internal firmware name | **`Pro`** | **`Lite`** |
| Storefront record created | 2026-08-18T14:29:31+08:00 | 2026-08-18T14:26:42+08:00 |
| Inventory counter 2026-09-01 | **−129** | **0** |

**The USD 10 difference buys exactly the NFC and LoRa hardware.** Everything else — panel,
touch, frontlight, battery, SoC, both auxiliary microcontrollers, the power architecture — is
identical, and one firmware image serves both, detecting the variant at runtime by probing for
the NFC chip ([`factory-firmware.md` §5](factory-firmware.md#5-what-the-device-does-on-power-up)).

Two details that only appear when you look at both records together:

- **The vendor's own systems disagree about the SKU string**: `C153-Lite` on
  `docs.m5stack.com`, `C153-LITE` in the Shopify record.
- **The firmware calls the full model "Pro"** although no M5Stack marketing material does.
  If you see `Pro` in a log, that is a C153.

**One widely propagated error to know about.** Liliputing (2026-08-28) described the device as
"a **$55** … with … NFC, LoRa". $55 is the **Lite**, which has neither. The NFC/LoRa model is
$65. Recorded in [`gaps-and-conflicts.md`](gaps-and-conflicts.md#claims-examined-and-rejected)
and [`community.md`](community.md).

## 7. Positioning, audience and product culture

**How M5Stack positions it.** The product page's own applications list is: *E-Reader, E-Paper
Signage, Access Control Terminal, Identity Authentication Device, Intelligent Transportation
Terminal* (S01). The blog announcement calls it *"A Compact E-Ink Development Terminal for
Connected Projects"* (S50). Read those together and the intent is clear: the **radios and the
power architecture** are the product, and the display is a low-duty output. Two of the five
listed applications are NFC applications.

**How the market read it.** As an e-reader. The 162-point HN thread is dominated by comparisons
to sealed consumer readers (the XTEINK X4 Pro repeatedly), the single hands-on video frames it
as a "pocket gadget", and the first two third-party projects to appear were an **e-reader
firmware port** and a **reader UI**. The gap between the vendor's framing and the audience's is
the most interesting cultural fact about this launch, and it is visible in the artifacts rather
than asserted: a third party had CrossPoint reader firmware published **one day after launch**,
before any written coverage of the hardware existed.

**M5Stack's disclosure culture, stated fairly.** This board is unusually well documented for its
class in some respects and unusually badly in others, and both are worth recording because they
are the vendor's pattern, not this product's accident:

| Good | Bad |
|---|---|
| Complete published schematic (6 sheets) | **No C153 directory in `m5stack/M5_Hardware`** — the SKU sequence stops at C152, so there is no machine-readable netlist (S45, a verified negative) |
| Vendor-authored datasheets for **both** custom chips (M5PM1, M5IOE1) | Both manuals are internally inconsistent; the M5IOE1's own manual states an I²C address range the board does not use ([C4](gaps-and-conflicts.md#c4--the-m5ioe1s-i²c-address-is-not-in-its-own-manual)) |
| Firmware source published, MIT | The shipped image is `-dirty` and not reproducible from it |
| The vendor **publishes a warning against its own graphics library's waveforms** and points you at the panel maker's example instead | …which means the recommended path bypasses the vendor's own library |
| Pin tables on the product page are accurate everywhere they overlap the schematic ([R6](gaps-and-conflicts.md#r6--the-vendor-product-pages-pin-tables-are-accurate--confirmed-correct)) | They omit USB, UART0 and two expander pins; and the `PYG<n>` notation is ambiguous between two chips ([`pin-naming-and-the-pyg-ambiguity.md`](pin-naming-and-the-pyg-ambiguity.md)) |
| Published power-consumption figures for **PaperS3** and **PaperColor** | **None for PaperMono** — the one board whose headline feature is its power architecture ([`performance.md`](performance.md)) |
| 2025-12-22 | **Main PCB silkscreen date code** `251222`, revision **V0.6** — the earliest hardware date in evidence anywhere in this record, ~8 months before launch (FCC internal photos p. 2, S72) |
| 2026-02-01 | Antenna specification `RSY-E8131` released at V3.0 by Shenzhen Rongshengyuan (S70) |
| 2026-07-14 | Sample received by the SAR laboratory (S69 p. 1) |
| 2026-07-15 | **SAR testing performed** (S69 pp. 5, 25) |
| 2026-07-25 | SAR report `2604T59815E-SA` issued (S69 pp. 1, 4) |
| **2026-08-12** | **FCC grants issued** — two, under FCC ID `2AN3WM5PAPERMONO`, nine days before the board went on sale (S68) |
| — | **Corrected 2026-09-20.** This row previously read *"No certification identifier published for this board"* on the strength of S11's verified negative. M5Stack publishes none — but the board **is** certified, and the exhibits are public. See [`certification.md`](certification.md) and [`gaps-and-conflicts.md` G2](gaps-and-conflicts.md#g2--no-certification-identifiers-exist-on-the-vendor-site) |

The last two rows are the ones a buyer should weigh. A product sold on low power that publishes
no power figure, and a radio product that publishes no regulatory identifier, are both gaps the
vendor has filled for adjacent products in its own catalogue.

**CNX-Software's two independent contributions** are the only added value in any written piece,
and both are small: an observation that **ghosting is visible in the vendor's own demo video**
(an observation of a video, not of hardware), and that the product is **not listed on
AliExpress** (independently reproduced here on 2026-09-01). CNX also disagrees with the vendor
on dimensions — 101 × 61 × 7.95 mm against the docs' 62.0 × 101.0 × 8.0 mm.

## 8. What is not established

- **No announcement or preorder milestone before 2026-08-17** was found. The 2026-05-07
  repository creation is a trace, not an announcement.
- **No discontinuation or lifecycle statement** exists for PaperMono; it is eleven days old.
- **The restock date is contested and unresolved** — vendor "two or three months" (primary,
  2026-08-22) against CNX-Software's "next year" (second-hand, unlinked)
  ([C7](gaps-and-conflicts.md#c7--restock-timing)).
- **The original M5Paper's display controller** is unverified (§3).
- **The Lite's schematic was not retrieved** (S16) — it is `PRJ`-named with 4 sheets against the
  full model's 6, and is the highest-value untaken lead for the family record.
- **`community.m5stack.com` could not be searched** (HTTP 401), so vendor-forum history is a
  blank in this timeline rather than an absence.
- **No hardware revision other than V0.6.2 is in evidence**, and no regional variants were
  found.

## Related

- [`README.md`](README.md) — the summary timeline this page evidences
- [`../papermono-lite/README.md`](../papermono-lite/README.md) — the variant record
- [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) — competitors outside the family
- [`market-and-pricing.md`](market-and-pricing.md) — dated pricing and availability
- [`community.md`](community.md) — coverage, evidence types, and the claims that failed checking
- [`performance.md`](performance.md) — including the published-figures asymmetry within the family
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — every conflict cited here
- [`sources.md`](sources.md) — S01, S04, S11, S13–S17, S33–S42, S45, S48–S50, S68–S81, S89–S93
