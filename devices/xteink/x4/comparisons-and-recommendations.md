# Xteink X4 — comparisons and recommendations

Dated **2026-09-04**. The full cross-model table lives in the
[family index](../README.md#cross-model-comparison); this page covers the X4's
own position and the platform comparison.

## The headline: it is discontinued, and that changes every recommendation

The X4 is **delisted**, and every X4-specific accessory is **sold out**. A
recommendation to buy one is a recommendation to buy **used, without spare cases
or screen protectors**.

Owners of all three models are blunt about it:

> "As someone with all 3, **the pro makes the other two feel obsolete.**"
> "The regular X4 definitely feels obsolete (**and also literally discontinued**)."
> — [r/XTEINK `1vw6haq`](https://old.reddit.com/r/XTEINK/comments/1vw6haq/), 2026-08-23 · firsthand owners

## The one thing that keeps it alive: USB-C

The X4 is **the only Xteink that charges over USB-C**. The X3 and X4 Pro use a
proprietary magnetic pogo connector with a $4.99 cable and a $5.99 adapter sold
separately.

> "Call me stubborn, but I'm **sticking with my X4 just because of the usb c
> port**. If it dies, I'm looking elsewhere."
> — same thread · firsthand owner

> "It's enough that I'll **happily keep using my original X4 instead of
> upgrading**."
> — [r/xteinkereader `1v2txxe`](https://old.reddit.com/r/xteinkereader/comments/1v2txxe/), 2026-07-21 · firsthand owner

And the counter-view, also from owners: *"the pogo charger is really a non-issue"*
(2 separate commenters). **The community is genuinely split**; this record does not
adjudicate it.

## Within the family

| | **X4** | [X3](../x3/README.md) | [X4 Pro](../x4-pro/README.md) | [X4 Classic](../x4-classic/README.md) |
|---|---|---|---|---|
| Price 2026-09-04 | **delisted** (~$69) | **$69** | **$99** | never priced |
| SoC / PSRAM | C3 / none | C3 / none | **S3 / 8 MB** | **S3 / 8 MB** |
| Panel | 4.26″ 800×480, ~219 PPI | 3.7″ 792×528, **~257 PPI** | 4.26″ 800×480 | 4.26″ 800×480 |
| Charging | **USB-C** | pogo | pogo | unknown |
| Touch / frontlight | ✗ / ✗ | ✗ / ✗ | **✅ / ✅** | ✗ / ✗ |
| RTC | **none** | DS-series 0x68 | BM8563 0x51 | BM8563 0x51 |
| Fuel gauge | **none — bare ADC** | **BQ27220** (best) | CW2017 | CW2017 |
| IMU / NFC | ✗ / ✗ | **✅ / ✅** | ✗ / ✗ | ✅ / ✗ |
| SD | SPI, **shared with display, no power enable** | SPI shared, **with** power enable | **native SDMMC** | **native SDMMC** |
| Buttons | 6 (ADC ladder) + power | 6 (ADC ladder) + power | 2 + power | **6 discrete** + power |

**The X4 is the most stripped-down member.** The cheaper X3 has four things it
lacks (RTC, real gauge, IMU, NFC) and a sharper screen. What the X4 has is USB-C,
the largest firmware ecosystem, and — uniquely — **a publicly available factory
flash dump**.

## Against development platforms in this repository

| Device | Class | Schematic | USB-C | Headers | Unlock needed | Verdict vs X4 |
|---|---|---|---|---|---|---|
| **Xteink X4** | sealed reader | ✗ | ✅ | ✗ | often | — |
| [M5Stack PaperMono](../../m5stack/papermono/README.md) | dev board | **✅ published** | ✅ | ✅ | ✗ | **Better for development**; worse as a pocket reader — no enclosure, no case ecosystem, and *"It's thicccccc tho"* per an r/xteinkereader commenter |
| [Waveshare ESP32-S3-ePaper-3.97](../../waveshare/esp32-s3-epaper-3.97/README.md) | dev board | partial | ✅ | ✅ | ✗ | ESP32-**S3** with PSRAM and a 3.97″ SSD1677 panel — strictly more capable silicon, no enclosure or battery management |
| [ZeroWriter](../../zerowriter/) | DIY appliance | ✅ open | ✅ | ✅ | ✗ | **Different purpose** — a keyboard-first writing appliance, not a pocket reader |

**These are partial substitutes, not equivalents.** They share "ESP32 driving
e-paper" and nothing else: no enclosure, no battery, no case ecosystem, no
pocketability. A dev board is the right answer if you want to *build* something; a
sealed X4 is the right answer if you want to *read* on something you can also
reflash.

The comparison is sharpened by a community datapoint: someone **built their own
open-source ESP32-S3 e-paper dev kit** with KiCad files, a 650 mAh cell,
**USB-C with OTG, no pogo pins**, 4-bit SDMMC and hand-solderable parts — at a
*"full unit BOM around $60 including display and battery"*
([r/XTEINK `1s3osv3`](https://old.reddit.com/r/XTEINK/comments/1s3osv3/), 2026-03-25,
104 pts · demonstrable project). **A DIY equivalent costs about what the X4 cost**,
which tells you the X4's margin was in manufacturing scale, not components.

## Direct competitors named by owners

| Device | Community verdict |
|---|---|
| **Murphy M3 / M4 (HamGeek, 墨菲)** 3.7″/4.26″ | *"texts on the X4 is 'sharper' and better software supports"*; the M4 claims a 2500 mAh battery that the reviewer **doubts**; M4 **has** a warm frontlight. [r/ereader `1uh14ww`](https://old.reddit.com/r/ereader/comments/1uh14ww/) · firsthand |
| **OBOOK5** | 219 PPI, 1200 mAh, ~23 GB usable — *"smaller than the boox palmas, and cheaper too"* |
| **Boox Palma / Go 7 / Picco** | Repeatedly raised; Android, much more expensive |
| **Kobo Clara BW / Libra 2** | The "grown-up" comparison; owners keep both |
| **Kindle Basic (2011!)** | An actual r/kindle thread compares them: *"Basic 4th vs Xteink X4. 2011 vs 2025"* |

## Recommendations

| Scenario | Recommendation | Confidence |
|---|---|---|
| **You want USB-C and a pocket e-reader you will reflash** | **X4, used** — and buy any case/protector you want *with* it, because they are gone | high |
| You want to buy new, today | **X3 ($69)** or **X4 Pro ($99)**. The X4 is not purchasable | high |
| You want the sharpest screen | **X3** (~257 PPI) | high |
| You want touch + frontlight | **X4 Pro** | high |
| **You want to build a product** | **PaperMono** or a **Waveshare** board — published schematic, headers, no unlock dance | high |
| You want an IMU or NFC | **X3** | high |
| You are waiting | **X4 v2 was confirmed by the vendor for September 2026** — spec unknown, and comment rumour suggests it may move to pogo charging | **low — hearsay** |

## Honest limits

- **No X4 was measured.** The only figures are two developer-reported plane-write
  timings and a three-unit ADC sample. See [`performance.md`](performance.md).
- **Battery capacity is unknown**, so battery life cannot be compared at all.
- Competitor prices and specs above are **community-reported**, not verified.
- PaperMono / Waveshare / ZeroWriter figures are dated differently — follow the
  links.

---

## Cross-references added 2026-09-07

Append-only, from a cross-cutting synthesis pass. Nothing above was changed and no
new evidence was gathered.

- [**Handheld and e-ink device landscape, 2026-09**](../../../guides/markets/handheld-and-eink-device-landscape-2026-09.md)
  — the X4 placed in the pocket-reader group, including the point that it is the
  **only member of the family with USB-C charging** and that this is now only
  available secondhand.
- [**Xteink firmware ecosystem**](../firmware-ecosystem.md) — why the X4 is *"the
  device that created the ecosystem"*, and the concrete hazard that follows from
  "X4" being a C3 while "X4 Pro" is an S3: **CrossPlay had to repoint
  `OtaUpdater.cpp` because upstream's release URL would flash a C3 image onto an
  S3.**
- [**SoC choice for battery e-ink devices**](../../../guides/hardware/soc-choice-for-battery-eink-devices.md)
  — the C3 memory ceiling, and the observation that an ESP32-S3 **with** 8 MB PSRAM
  is available on a $9.04 board, so PSRAM is not what makes a device expensive.
- [**Adding LoRa, NFC and an RGB sidelight to e-ink firmware**](../../../guides/hardware/adding-lora-nfc-and-sidelight-to-eink-firmware.md)
  — why adding a radio to an X4 is a hardware project rather than a firmware one:
  the panel and the SD card **share one SPI bus**, and there is no free interrupt
  line, no antenna and no RF path.
