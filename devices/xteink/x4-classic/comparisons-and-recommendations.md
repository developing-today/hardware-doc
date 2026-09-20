# Comparisons and recommendations — Xteink X4 Classic

Dated **2026-09-11**. Prices are vendor-direct, item-only, worldwide from
Shenzhen, read from `xteink.com/products.json`. **Nothing here was benchmarked.**

## 1. Against its own family

| | [X3](../x3/README.md) | [X4](../x4/README.md) | **X4 Classic** | [X4 Pro](../x4-pro/README.md) |
|---|---|---|---|---|
| **Price, 2026-09-11** | **$69** | **withdrawn** | **$79** | **$99** |
| Status | in stock | **gone — accessories withdrawn too** | in stock, 9 days old | in stock |
| SoC | ESP32-C3 | ESP32-C3 | **ESP32-S3** | ESP32-S3 |
| PSRAM | none | none | **8 MB** | 8 MB |
| Panel | 3.7″ 792×528 | 4.26″ 800×480 | 4.26″ 800×480 | 4.26″ 800×480 |
| **PPI** | **~257** | ~219 | ~219 | ~219 |
| Mass | **55 g** | ~74–80 g | **68 g** | not published |
| Thickness | not published | not published | **4.9 mm** | not published |
| Battery | 650 mAh | not published | **920 mAh** | not published |
| Touch | ✗ | ✗ | ✗ | **GT911** |
| Frontlight | ✗ | ✗ | ✗ | **dual warm/cool** |
| Buttons | 6 (ADC ladder) + pwr | 6 (ADC ladder) + pwr | **6 discrete ISR + pwr** | **2** + pwr |
| IMU | **QMI8658** | ✗ | **QMI8658** | ✗ |
| NFC tag | **✅** | ✗ | ✗ | ✗ |
| RTC | DS-series (unresolved) | **none** | BM8563 | BM8563 |
| Gauge | **BQ27220** | bare ADC | CW2017 | CW2017 |
| Storage | SPI, shared with display | SPI, shared | **native SDMMC** | native SDMMC |
| Charging | pogo | **USB-C** | pogo | pogo |
| Panel selection | live bus probe | live bus probe | **NVS only — no MISO** | live bus probe |
| **FCC ID** | `2BTR9-XTEINKX3` | `2BTR9-XTEINKX4` | **`2BTR9-X4C`** | `2BTR9-X4PRO` |
| Public FCC **internal** photos | **✅ since 2026-06-24** | **✅ since 2026-07-04** | **2027-01-16** | **2026-12-12** |

### Reading the table

**The X4 Classic is not an upgrade over the X4 Pro and was never meant to be.**
It is the X4 Pro's board with the two most expensive parts — the capacitive
touch layer and the dual-channel frontlight — deleted, the freed GPIOs turned
into four more buttons, and an IMU added. Priced US$20 below.

**It is also not a straight upgrade over the X4 it replaces.** It gains a much
faster SoC with PSRAM, native SDMMC, a real RTC, an I²C fuel gauge, an IMU, a
published 920 mAh cell, six discrete interrupt-driven buttons instead of an ADC
ladder, and 4.9 mm / 68 g. **It loses USB-C**, and it costs about 30 % more than
the X4 did at the same list price point. The most-repeated community complaint
is exactly that trade, and it is a fair one.

**The X3 still has the sharpest screen in the family** (~257 PPI vs ~219) and
the best battery instrumentation (a BQ27220 that needs no profile upload). The
X4 Classic's advantages over the X3 are size, speed, memory, storage path and
capacity — not image quality.

**One thing the Pro does not have and this does: an IMU.** The Pro has no
QMI8658. If you want motion input on an S3 Xteink, the X4 Classic is the only
one that has it.

## 2. What it is genuinely better at than anything else in the family

| Use | Why |
|---|---|
| **Buttons-only reading on an S3** | Six discrete ISR keys, no touch layer between you and the glass. The Pro has two keys; the C3 X4 has six but on an ADC ladder and a much slower SoC |
| **Firmware development with real storage** | Native SDMMC *and* 8 MB PSRAM *and* a dual-OTA table with a free 8 MB slot. The X3 and X4 share their SD bus with the display |
| **Motion input** | The only S3 Xteink with an IMU |
| **Pocket weight** | 68 g / 4.9 mm for a 4.26″ panel |

## 3. What to buy instead, by need — dated 2026-09-11

| You want… | Buy | Confidence |
|---|---|---|
| Sharpest text, lightest, most sensors, cheapest new | **X3, $69** | high |
| Touch **and** a frontlight | **X4 Pro, $99** | high |
| **Any frontlight at all** | **Nothing in this family.** Wait for the [X4 Light](../x4-light/README.md), FCC-certified 2026-08-13, **unannounced and unpriced** — or buy a Kindle | **low — the X4L's feature set is not established** |
| **USB-C** | **Used X4 only.** It is withdrawn and its accessories are gone | high |
| Six real buttons on an S3, plus an IMU, plus SDMMC | **X4 Classic, $79** | high |
| A schematic, headers, and no unlock dance | [M5Stack PaperMono](../../m5stack/papermono/README.md) or a Waveshare board | high |
| Cheapest possible entry into this ecosystem | **Used X4, ~$16–58 observed** | medium |

## 4. Against the outside world

### Boox Picco — the live competitive question

Announced at **US$100**, *expected November 2026*
([r/XTEINK `1w938ab`](https://old.reddit.com/r/XTEINK/comments/1w938ab/),
2026-09-06, 282 pts / 175 comments; and
[`1wdurfy`](https://old.reddit.com/r/XTEINK/comments/1wdurfy/), 2026-09-11).

**This repository has no primary data on the Picco** — no specification page, no
FCC filing, no teardown was retrieved. The only thing that can honestly be said
is that a $100 Android-class competitor is expected two months out, and that the
X4 Classic's $79 is not a comfortable margin against it. **Do not treat any
X4C-vs-Picco comparison in this repository as evidence.**

### Development boards

The comparison the community makes constantly, and it remains close to
meaningless:

| | X4 Classic | [PaperMono](../../m5stack/papermono/README.md) | [Waveshare ESP32-S3-ePaper-3.97](../../waveshare/esp32-s3-epaper-3.97/README.md) |
|---|---|---|---|
| Class | **sealed reader** | dev board | dev board |
| Schematic | ✗ (FCC schematic exhibit is **permanently confidential**) | **✅ 6 sheets** | partial |
| Headers | ✗ | ✅ | ✅ |
| Enclosure, battery, case ecosystem | **✅** | ✗ | ✗ |
| Unlock needed | often | ✗ | ✗ |
| Price | $79 | — | — |

**These are partial substitutes, not equivalents.** A dev board is the right
answer if you want to *build*; a sealed Xteink if you want to *read* on something
you can also reflash. The X4 Classic is a slightly better development target
than its siblings — S3, PSRAM, SDMMC, dual-OTA — and a slightly worse one in one
specific way: **no MISO on the panel bus**, so a wiped NVS leaves firmware unable
to identify its own display controller.

## 5. Honest verdict

Buy the X4 Classic if you want a **buttons-only 4.26″ pocket reader on modern
silicon** and you can live without a frontlight and without USB-C. It is, on the
vendor's own numbers, the thinnest and second-lightest device in the family, with
the largest published battery.

Do **not** buy it as an upgrade from an X4 or X3. The most careful reviewer with
all three devices in hand concluded exactly that — *"if you already have an X4 or
X3, save your coins"* — and the panel density, which is what most people mean
when they say "better screen", **has not changed**.

Do **not** buy it expecting the frontlight the community has been asking for
since April. That is a different, already-certified device that has not been
announced.
