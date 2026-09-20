# Xteink (阅星瞳 / 星瞳 "Star Pupil")

> Shenzhen-based compact e-reader brand. Five products established as of the
> research snapshot **2026-09-04**. Four are ESP32-based and are the hardware
> targets of the CrossPoint Reader / FreeInk firmware ecosystem; the fifth is an
> Android device and is a different platform entirely.

## The confirmed family

| Device | SoC | Panel | Size / res | Touch | Frontlight | Record | Depth |
|---|---|---|---|---|---|---|---|
| [**X4 Pro**](x4-pro/README.md) | ESP32-S3, 16 MB flash, 8 MB PSRAM | SSD1677 · UC8179 · UC8279 (batch-dependent) | 4.26″ 800×480 | **GT911** | **dual warm/cool** | `x4-pro/` | deep |
| [**X4**](x4/README.md) | ESP32-C3, 16 MB flash | SSD1677 · UC8179 · UC8279 | 4.26″ 800×480 | none | none | `x4/` | deep |
| [**X3**](x3/README.md) | ESP32-C3, 16 MB flash | UC8253 · UC8279d | 3.7″ 792×528 | none | none | `x3/` | deep |
| [**X4 Classic (X4C)**](x4-classic/README.md) | ESP32-S3, 16 MB flash, 8 MB PSRAM | SSD1677 · UC8179 · UC8279 | 4.26″ 800×480 | none | none | `x4-classic/` | medium |
| [**S4**](s4/README.md) | **Android 11**, 2 GB RAM / 32 GB | not established | not established | yes | yes | `s4/` | **stub** |
| [**Nano** / Tong Card 瞳卡](nano/README.md) | **none — passive, NFC-powered** | four-colour e-paper, part unknown | not established | n/a | n/a | `nano/` | **stub** |

The **Nano** is not a reader. It is a battery-less NFC-powered e-paper display
card that snaps to a phone's back, written from a phone app. It is included
because it is a genuine Xteink product line, it is sold internationally on
AliExpress, and it is **routinely confused with the X3's embedded NFC tag** —
which is a completely different thing.

**The X4 Pro and the X4 are different computers.** They share a screen size and a
brand and nothing else: different SoC architecture (Xtensa LX7 vs RISC-V),
different flash layout, different input hardware, different charging connector.
Firmware built for one will not run on the other, and
[CrossPlay's `OtaUpdater` had to be repointed](../../software/applications/crossplay/README.md)
specifically because upstream's release URL would flash a C3 image onto an S3.

## Models that do **not** exist

Recorded so they are not re-investigated:

| Name | Verdict | Evidence |
|---|---|---|
| **X5** | **Does not exist.** Community speculation about a successor only | 8 Reddit mentions, all wishlist/rumour. One post titled "Got my white (?) X5" was edited by its own author: *"EDIT: It's X4 and not X5."* ([r/xteinkereader `1o8vw7y`](https://old.reddit.com/r/xteinkereader/comments/1o8vw7y/got_my_white_x5/), 2025-10-17) |
| **X4 Mini** | **Not a SKU.** A colloquial nickname for the X4 | Six uses across r/EDC, r/eink, r/writerDeck. The r/eink video titled "XTEINK X4 mini e-Reader" says in its own body *"the XTEINK X4"* ([`1sba4am`](https://old.reddit.com/r/eink/comments/1sba4am/), 2026-04-03) |
| **X1 / X2** | **No evidence.** Zero substantive mentions | 3 apparent hits were all false positives (`x2` = "quantity two") |
| **X4 Plus / Air / Pro Max** | **No evidence** | Not present in the vendor catalogue, the vendor's collection handles, the FreeInk board enum, or 1,798 Reddit posts |

The vendor's own Shopify collection handles are the tightest available list, and
they are exactly: `x3-series`, `x4-series`, `x4-classic`, `x4-pro-series`
(plus marketing duplicates `x3-edm`, `x4-edm`, `x4-proedm`, `machine`,
`homepage-display`, `accessories`, `pocket-e-reader`).

## Naming and transliteration

| Form | Where used |
|---|---|
| **Xteink** | Official Latin brand, `xteink.com` |
| **XTeink**, **XT-eink**, **XTEINK** | All appear in community and repo names; the vendor's own store title is uppercase `XTEINK` |
| **星瞳** ("Star Pupil") | Chinese product name — [r/ereader `1n5kmpc`](https://old.reddit.com/r/ereader/comments/1n5kmpc/xteink_star_pupil_x4_星瞳x4_first_impressions/) is titled "Xteink Star Pupil X4 (星瞳X4)" |
| **阅星瞳** | Chinese brand form used by [`sunwoods/Xteink-X3`](https://github.com/sunwoods/Xteink-X3) |
| **阅星曈** | A **different second character** (曈 "dawn light" vs 瞳 "pupil"), used by [`zocs/eink-quick-flasher`](https://github.com/zocs/eink-quick-flasher) and `AsukaLay/xteink_pdf`. **Both spellings are in live community use.** Search both |
| **星曈** | Short form with 曈, used by `SamLinBIT/xteink-toolkit` |
| `XTEink::` | The C++ namespace in the vendor's own stock firmware, recovered by Ghidra |

## Company

A **small team based in Shenzhen**. The founder posts publicly as **"Crusoe"** and
introduced the company on Reddit on 2025-10-09
([r/ereader `1o2203h`](https://old.reddit.com/r/ereader/comments/1o2203h/hi_everyone_im_crusoe_from_xteink_a_small_ereader/),
1,477 points) — *"I'm Crusoe, founder of Xteink, a small team based in Shenzhen."*
The company is China-first: the S4 launched domestically months before any
international availability, and firmware/pricing announcements appear on
Xiaohongshu (RedNote) before they reach the English store.

## Why this family matters

These are the **cheapest programmable e-paper devices with a usable enclosure,
battery, buttons and SD slot** currently in circulation — $69–$99 new, and
observed as low as **$16** used ([r/XTEINK `1vrnxnq`](https://old.reddit.com/r/XTEINK/comments/1vrnxnq/), 2026-08-18).
A bare 4.26″ panel alone typically costs more than a whole X4.

That, plus a stock firmware that turned out to be reverse-engineerable, produced
an unusually large third-party firmware ecosystem — **~200 public repositories**
census'd on 2026-09-04. See each device's `projects-and-community.md`.

## Documentation map

| Per-device file | What it holds |
|---|---|
| `README.md` | Identity, specs, architecture, market fit, task index |
| `pinouts-and-buses.md` | Full GPIO/bus tables reconstructed from firmware source |
| `development.md` | Toolchain, build, flash, unlock, bricking risks |
| `factory-firmware.md` | Stock images, dumping, restoring, partition layout |
| `features/` | Task-oriented guides per capability |
| `sources.md` · `research-log.md` · `commands.md` | Evidence trail |
| `coverage.md` · `compatibility-and-status.md` · `gaps-and-conflicts.md` | What is and is not established |
| `projects-and-community.md` · `community.md` | Firmware ecosystem and owner reports |
| `market-and-pricing.md` · `comparisons-and-recommendations.md` | Dated commercial evidence |

## Shared reading

- [FreeInk SDK board profiles](https://github.com/Free-Ink/freeink-sdk/blob/24003795381a6c23630a26472ae3b06550333e71/libs/hardware/BoardConfig/include/BoardConfig.h)
  — the single most authoritative hardware document for four of these five devices.
- [CrossPlay](../../software/applications/crossplay/README.md) — a fork analysis
  that explains the X4 Pro's position as the ecosystem's "design floor".
- [M5Stack PaperMono](../m5stack/papermono/README.md) — the development-board
  alternative the community repeatedly compares these to.

## Evidence standard used here

Every board-level pin, address and chip in these records traces to one of:
**[SDK]** the FreeInk SDK board profile or its `docs/xteink-*-support.md`;
**[DUMP]** a parsed OEM flash image; **[TD]** a teardown photograph;
**[VENDOR]** the vendor's own store API or a founder statement; or
**[COMM]** a community report, always labelled as such.

Vendor **marketing prose is not used as evidence anywhere in this tree.** The
`xteink.com` product copy is AI/SEO-generated and is demonstrably wrong: the X3
listing advertises "adjustable warm light settings" and "Cloud sync", and the X3
has no frontlight at all. See [`x3/gaps-and-conflicts.md`](x3/gaps-and-conflicts.md).

---

## Cross-model comparison

Dated **2026-09-04**. Prices are vendor-direct, item-only, worldwide from
Shenzhen. **Nothing in this table was measured by this research** — see each
device's `performance.md`.

### The four ESP32 devices

| | [**X3**](x3/README.md) | [**X4**](x4/README.md) | [**X4 Pro**](x4-pro/README.md) | [**X4 Classic**](x4-classic/README.md) |
|---|---|---|---|---|
| **Price** | **$69, in stock** | **delisted** (~$69) | **$99, in stock** | **never priced** |
| SoC | ESP32-C3 (RISC-V) | ESP32-C3 | **ESP32-S3** (Xtensa) | **ESP32-S3** |
| PSRAM | none | none | **8 MB** | **8 MB** |
| Flash | 16 MB Puya | 16 MB Puya | 16 MB | 16 MB |
| Panel | **3.7″ 792×528** | 4.26″ 800×480 | 4.26″ 800×480 | 4.26″ 800×480 |
| **PPI** | **~257** | ~219 | ~219 | ~219 |
| Controller | UC8253 · **UC8279d** | SSD1677 · UC8179 · UC8279 | SSD1677 · UC8179 · UC8279 | SSD1677 · UC8179 · UC8279 |
| Controller selection | live bus probe | live bus probe | live bus probe | **NVS only — no MISO** |
| Mass | **55 g** | ~74–80 g | unknown | unknown |
| Battery | **650 mAh** | unknown | unknown | unknown |
| Touch | ✗ | ✗ | **GT911** | ✗ |
| Frontlight | ✗ | ✗ | **dual warm/cool** | ✗ |
| Buttons | 6 (**ADC ladder**) + pwr | 6 (**ADC ladder**) + pwr | **2** + pwr | **6 discrete, ISR** + pwr |
| RTC | DS-series 0x68 **(unresolved)** | **none** | BM8563 0x51 | BM8563 0x51 |
| Fuel gauge | **BQ27220** (no profile needed) | **none — bare ADC** | CW2017 (needs BATINFO) | CW2017 |
| IMU | **QMI8658** | ✗ | ✗ | **QMI8658** |
| **NFC** | **✅ writable tag** | ✗ | ✗ | ✗ |
| Storage | SPI, **shared with display** | SPI, **shared**, no power enable | **native SDMMC** | **native SDMMC** |
| SD sleep power-down | ✅ GPIO13 (active-HIGH) | **✗** | ✅ GPIO5 (active-LOW) | ✅ GPIO6 (active-LOW) |
| Charging | pogo | **USB-C** | pogo | **unknown** |
| USB-MSC | — | — | in stock, **unported** | **SDK-supported** |
| Public firmware image | **4 stock images** (Git LFS) | **1 community dump, archived here** | **none** | **none** |
| Teardown | **2, both archived here** | none | none | none |

### Five things this table gets wrong if you skim it

1. **"X4 Pro" is not an enhanced X4.** Different SoC architecture, flash layout,
   input hardware and charging connector. Firmware for one will not run on the
   other, and upstream release URLs have flashed C3 images onto S3 devices.
2. **The Pro is not a superset.** It has **no IMU**; the cheaper X3 and its own
   board sibling both do.
3. **The cheapest model has the sharpest screen.** ~257 PPI vs ~219.
4. **The X3 has the best battery instrumentation.** A BQ27220 needing no profile
   upload, against the Pro's CW2017 (reports 0 % until an 80-byte BATINFO table is
   written) and the X4's bare ADC.
5. **GPIO13 means three different things** across the family — SD rail on the X3
   (active-HIGH), battery power-off latch on the X4, unused on the S3 boards. Never
   port power code between them.

### Against platforms already in this repository

| Device | Class | Schematic | USB-C | Headers | Unlock | Verdict |
|---|---|---|---|---|---|---|
| Xteink X3 / X4 / X4 Pro | **sealed reader** | ✗ (X3: a hand-drawn sketch) | X4 only | ✗ | often needed | Pocketable, cased, battery-managed, cheap |
| [M5Stack PaperMono](../m5stack/papermono/README.md) | dev board | **✅ published, 6 sheets** | ✅ | ✅ | ✗ | **Better for development.** Bigger, thicker, no enclosure or case ecosystem |
| [Waveshare ESP32-S3-ePaper-3.97](../waveshare/esp32-s3-epaper-3.97/README.md) | dev board | partial | ✅ | ✅ | ✗ | ESP32-S3 + PSRAM + SSD1677 + a QMI8658 — the closest dev-board analogue to an X3's silicon |
| [ZeroWriter](../zerowriter/) | DIY appliance | ✅ open | ✅ | ✅ | ✗ | Different purpose: keyboard-first writing appliance |

**These are partial substitutes, not equivalents.** They share "ESP32 driving
e-paper" and nothing else — no enclosure, no battery management, no case
ecosystem, no pocketability. The community routinely compares them on price, and
that comparison is close to meaningless: a dev board is the right answer if you
want to **build** something, a sealed Xteink if you want to **read** on something
you can also reflash.

A useful calibration: a community member built an **open-source ESP32-S3 e-paper
dev kit** — KiCad files, 650 mAh cell, USB-C OTG, 4-bit SDMMC, hand-solderable
parts — at a *"full unit BOM around $60 including display and battery"*
([r/XTEINK `1s3osv3`](https://old.reddit.com/r/XTEINK/comments/1s3osv3/),
2026-03-25, 104 pts). **A DIY equivalent costs roughly what a finished X4 cost.**

### Buying guidance, dated 2026-09-04

| You want… | Buy | Confidence |
|---|---|---|
| Sharpest text, lightest, most sensors, cheapest new | **X3, $69** | high |
| Touch **and** a frontlight | **X4 Pro, $99** | high |
| **USB-C charging** | **X4, used only** — it is delisted and its accessories are exhausted | high |
| Six real buttons on an S3, plus an IMU | **X4 Classic** — **if you can find one**; never listed internationally | n/a |
| Android, apps, a browser, half the price | **S4** — but **no community firmware, ever** | medium |
| A schematic, headers and no unlock dance | **PaperMono** or a **Waveshare** board | high |
| To wait | An **"X4 version 2"** was vendor-confirmed for September 2026, spec unknown | **low — hearsay** |

**One warning that applies to every purchase in this family:** USB-lock state is
**not predictable from the sales channel**. An owner who bought three units
reported an Amazon X3 unlocked, an official-store X3 **locked**, and an AliExpress
X4 locked ([r/XTEINK `1vkuhbi`](https://old.reddit.com/r/XTEINK/comments/1vkuhbi/),
2026-08-10, firsthand). Assume you will need the unlock procedure.

---

## Cross-references added 2026-09-07

Appended by a cross-cutting synthesis pass. **No line above was changed**, and
nothing below is a new retrieval or a new measurement — these are syntheses built
from the records in this tree.

| Document | What it adds that is not here |
|---|---|
| [**`firmware-ecosystem.md`**](firmware-ecosystem.md) | **The hardware-side map of CrossPoint / FreeInk / CrossPlay** — which firmware supports which model, at which commit and board target, the full `VER (0x70)` / `FLG (0x71)` panel-controller detection trick and its X4 Classic exception, and a checklist of what a *new* board must provide to be supported |
| [Handheld and e-ink device landscape, 2026-09](../../guides/markets/handheld-and-eink-device-landscape-2026-09.md) | These four ESP32 devices placed against the PaperMono, the Waveshare e-paper boards and ZeroWriter, with the comparisons that are **not** supportable stated explicitly |
| [SoC choice for battery e-ink devices](../../guides/hardware/soc-choice-for-battery-eink-devices.md) | Why the C3 → S3 split inside this family matters more than the price difference suggests, with the framebuffer and heap arithmetic — and the finding that **no ESP32-C3 or ESP32-S3 deep-sleep figure exists anywhere in this repository** |
| [Adding LoRa, NFC and an RGB sidelight to e-ink firmware](../../guides/hardware/adding-lora-nfc-and-sidelight-to-eink-firmware.md) | ⚠ **Why the X3's passive NFC tag is not an NFC reader**, and what adding real radios to this class of firmware would actually cost |

---

# ROUND 2 — appended 2026-09-11

> **No line above this rule was changed.** Several statements above are
> **superseded**, and they are superseded here rather than edited in place, so
> the 2026-09-04 snapshot stays readable as what was knowable then.
>
> Retrieval date **2026-09-11**. (The task brief said 2026-09-07; the host clock,
> the vendor's Shopify `updated_at` and a dated store review all put "now" at or
> after 2026-09-08. The later date is used. See
> [`x4-classic/research-log.md`](x4-classic/research-log.md) §0.)

## The headline: the family is **six** products, not five, and the X4 is gone

| # | Device | Status 2026-09-11 | Price | Record |
|---|---|---|---|---|
| 1 | [**X4 Pro**](x4-pro/README.md) | listed, in stock | **$99** | deep — **now three independent custodians** |
| 2 | [**X4 Classic (X4 V2)**](x4-classic/README.md) | **LISTED 2026-09-06, in stock** | **$79** | deep |
| 3 | [**X3**](x3/README.md) | listed, in stock | **$69** | deep |
| 4 | [**X4**](x4/README.md) | **withdrawn — product record and all four dedicated accessories removed** | — | deep |
| 5 | [**X4 Light**](x4-light/README.md) | **FCC-certified 2026-08-13. Never announced, never listed** | — | **NEW — certification-only** |
| 6 | [**S4**](s4/README.md) | Android, separate platform | — | stub |
| + | [**Nano / Tong Card**](nano/README.md) | passive NFC card, not a reader | — | stub |

## Three corrections to the tables above

### 1. "X4 v2" was not a future product. It is the X4 Classic.

The buying-guidance table above ends with *"An **'X4 version 2'** was
vendor-confirmed for September 2026, spec unknown — **low — hearsay**."*

**That is now resolved, and the confidence label was right to be low, because the
thing being described was mis-modelled rather than mis-dated.** "X4 V2" is the
vendor's own parenthetical for the X4 Classic:

- vendor Reddit post, 2026-09-03: *"**X4 Classic (X4 V2) is coming soon**"*
- store product title: `XTEINK X4 Classic (X4 V2) Pocket eReader`
- four accessory titles, all `XTEINK X4 Classic (X4 V2) …`
- the product-page FAQ, in prose: *"The **X4 V2** features a built-in magnetic
  ring on the back…"*

**There is no separate model between the X4 and the X4 Pro.** The FreeInk
`enum class Board` at HEAD (`9f4d3f9`, 2026-09-10) still contains exactly five
Xteink entries, and GitHub code search for `"X4R1_CLA"` returns **zero**.

### 2. The X4 Classic collection is populated. The record's headline is superseded.

`x4-classic/README.md` opened with *"contains **no device** — only generic
accessories."* Correct on 2026-09-04; **wrong from 2026-09-06 19:57:20 −0700**,
the `published_at` on the vendor's own API.

### 3. "Models that do not exist" needs one line added, and one caveat

The table above is still correct as written: **X5**, **X4 Mini**, **X1/X2** and
**X4 Plus / Air / Pro Max** remain unevidenced. But its stated method — *"the
vendor's own Shopify collection handles are the tightest available list"* — **is
not the tightest list.** The tightest list is the vendor's **FCC grantee code**:

| FCC ID | Granted | Device |
|---|---|---|
| `2BTR9-XTEINKX3` | 2025-12-26 | XTEINK X3 |
| `2BTR9-XTEINKX4` | 2026-01-05 | XTEINK X4 |
| `2BTR9-X4PRO` | 2026-06-16 | XTEINK X4 Pro |
| `2BTR9-X4C` | 2026-07-20 | XTEINK X4 Classic |
| **`2BTR9-X4L`** | **2026-08-13** | **XTEINK X4 Light** ← unlisted, unannounced |

**Procedural lesson worth keeping: enumerate the grantee code, not the product
name.** `https://fccid.io/2BTR9` lists every device this company has certified
for the US, including ones it has never mentioned. The 2026-09-04 sweep could
not do this because no FCC ID had been read off a board and the grantee was
unknown; the ID was published by a community member on 2026-07-23 and the
grantee index followed from it.

## Corrected family table

Same evidence conventions as above. **Nothing here was measured by this research.**

| | [**X3**](x3/README.md) | [**X4**](x4/README.md) | [**X4 Classic**](x4-classic/README.md) | [**X4 Pro**](x4-pro/README.md) | [**X4 Light**](x4-light/README.md) |
|---|---|---|---|---|---|
| **Price, 2026-09-11** | **$69** | **withdrawn** | **$79** | **$99** | **unpriced** |
| Listed | 2025-12-11 | — | **2026-09-06** | 2026-07-21 | **never** |
| **FCC ID** | `2BTR9-XTEINKX3` | `2BTR9-XTEINKX4` | `2BTR9-X4C` | `2BTR9-X4PRO` | **`2BTR9-X4L`** |
| FCC granted | 2025-12-26 | 2026-01-05 | 2026-07-20 | 2026-06-16 | **2026-08-13** |
| **FCC internal photos public** | **✅ 2026-06-24** | **✅ 2026-07-04** | 2027-01-16 | 2026-12-12 | 2027-02-09 |
| SoC | ESP32-C3 | ESP32-C3 | **ESP32-S3** | **ESP32-S3** | **unknown** |
| PSRAM | none | none | **8 MB** | **8 MB** | unknown |
| Panel | **3.7″ 792×528** | 4.26″ 800×480 | 4.26″ 800×480 | 4.26″ 800×480 | unknown |
| **PPI** | **~257** | ~219 | ~219 | ~219 | unknown |
| **Mass** | **55 g** | ~74–80 g | **68 g** | not published | unknown |
| **Thickness** | not published | not published | **4.9 mm** | not published | unknown |
| **Battery** | **650 mAh** | not published | **920 mAh** | not published | unknown |
| Touch | ✗ | ✗ | ✗ | **GT911** | unknown |
| Frontlight | ✗ | ✗ | **✗ — settled** | **dual warm/cool** | **unknown; "Light" is not defined by the filing** |
| Buttons | 6 ADC ladder + pwr | 6 ADC ladder + pwr | **6 discrete ISR + pwr** (+ unused GPIO4) | **2** + pwr | ≥3 visible on the case |
| IMU | **QMI8658** | ✗ | **QMI8658** | ✗ | unknown |
| NFC tag | **✅** | ✗ | ✗ | ✗ | unknown |
| RTC | DS-series **(unresolved)** | **none** | BM8563 | BM8563 | unknown |
| Gauge | **BQ27220** | bare ADC | CW2017 | CW2017 | unknown |
| Storage | SPI, shared with display | SPI, shared | **native SDMMC** | **native SDMMC** | unknown |
| Charging | pogo | **USB-C** | **pogo** | pogo | **pogo — 4 contacts visible in the FCC photos** |
| Panel selection | live bus probe | live bus probe | **NVS only — no MISO** | live bus probe | unknown |
| **Antenna** | not read | not read | **KH3216-A35, 2.30 dBi** | not read | **internal, 5.19 dBi** |
| Wi-Fi | 2.4 GHz | 2.4 GHz | 2.4 GHz | 2.4 GHz | 2.4 GHz, 8.13 dBm max |
| Public teardown | 2 community + **FCC internal photos** | **FCC internal photos** | **none** | **none** | **none** |

### Where the X4 Classic actually sits

**Between the X4 and the X4 Pro on price, and it is not a compromise between
them on hardware.** It is the **X4 Pro's board** with the touch layer and the
frontlight deleted and their GPIOs turned into four more buttons, plus a
QMI8658 IMU the Pro does not have. What it inherits from the C3 X4 is the
buttons-only *reading model* and the four bottom keys — not the board.

The community's own one-line summary, offered as criticism and accurate as
description: *"disadvantages of the X4 + disadvantages of the Pro = Classic"* —
it keeps the X4's missing frontlight and the Pro's missing USB-C.

## Two family-wide facts established this pass

### The company has a legal identity

**Shenzhen Xiaohu Xingtong Technology Co., Ltd.** — Room 1209, Yichuang
International Center, Building 2B, No. 8 Golf Avenue, Guangpei Community,
Guanlan Street, Longhua District, Shenzhen. FCC grantee `2BTR9`, registered
**2025-12-21**; FRN `0037772233`; responsible party Chen Chu, `chuchen@xteink.cn`.

Two consequences for the naming section above: the romanisation **Xingtong**
corresponds to **星曈** (the *dawn-light* character), which the table above records
as a *"different second character"* in live community use — **the company's own
legal name uses it**. And the filing lists **`xteink.cn`** as the applicant's
domain, confirming the domain the 2026-09-04 sweep found unreachable at the apex
but referenced inside X4 firmware (`bofi.xteink.cn`) really is theirs.

### FreeInk halved the display SPI clock

Commit [`39606d5a`](https://github.com/Free-Ink/freeink-sdk/commit/39606d5a),
2026-09-09, *"Fix e-ink display buffer tracking and optimize SPI writes"*,
replaced every Xteink profile's `displaySpiHz` with a shared
`XTEINK_DISPLAY_SPI_HZ = 10000000u` — **20 MHz → 10 MHz** on the X4, X3,
X3-UC8279, X4 Pro and X4 Classic alike. Anyone carrying a build pinned before
that commit is clocking the panel twice as fast as upstream now recommends.

## The evidence position has changed materially

`VERIFICATION-xteink.md` §12 named **source concentration** as this tree's
principal weakness: for the X4 Pro and X4 Classic, every technical claim traced
to one repository at one commit, with no teardown, schematic or regulatory
filing.

| Device | 2026-09-04 | 2026-09-11 |
|---|---|---|
| X4 Pro | **1 custodian** (FreeInk) | **4** — FreeInk · a **physically dumped unit** ([`kycube/x4pro-emu`](https://github.com/kycube/x4pro-emu)) · an **on-hardware-tested firmware** ([`clackups/draftling`](https://github.com/clackups/draftling)) · **FCC `2BTR9-X4PRO`** |
| X4 Classic | **1 custodian** (FreeInk) | **3** — FreeInk · **vendor listing + spec block** · **FCC `2BTR9-X4C`**. Still **no board-level second custodian**; the FCC internal photos are embargoed to 2027-01-16 |
| X3, X4 | teardowns + a flash dump | **+ FCC internal photographs, already public** (2026-06-24 / 2026-07-04) |

**What has not changed: nothing in this tree has been verified on hardware by
this repository.** Zero devices have been in anyone's hands here. Every
"confirmed" above means *confirmed by a cited third party*.

## Round-2 verification

[`VERIFICATION-xteink-round2.md`](../../VERIFICATION-xteink-round2.md).
Proposed additions to shared and protected indexes are staged, unapplied, in
[`scratch/xteink/index-fragments-round2.md`](../../scratch/xteink/index-fragments-round2.md).
