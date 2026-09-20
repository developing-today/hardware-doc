# Xteink X3 — product history and family

Full family context: [`../README.md`](../README.md).

## Timeline

| Date | Event | Evidence |
|---|---|---|
| 2025-12-08 | Shopify product record created | **[VENDOR]** |
| **2025-12-09** | **Announced** — *"builds on everything we learned from building the X4 and pushes the idea of true pocket reading even further"*. Spec list: **55 g, 3.7″, 250+ PPI, gyroscope, NFC, magnetic pogo charging, clock + battery %** | **[COMM]** [r/xteinkereader `1pi6ezd`](https://old.reddit.com/r/xteinkereader/comments/1pi6ezd/), 275 pts |
| 2025-12-11 | **Pre-orders open.** *"Super Early Bird units are **non-refundable**"* | **[COMM]** [`1pjw3ay`](https://old.reddit.com/r/xteinkereader/comments/1pjw3ay/) · **[VENDOR]** |
| 2025-12-26 | Community digest: X3 shipping confirmed for 5 Feb; *"Frontlight support (still the **#1 feature request**)"* | **[COMM]** |
| 2025-12-28 | *"Xteink S4 release date?"* — the Android sibling is already awaited | **[COMM]** |
| **2026-02-05** | **Shipping begins** — an **8-week** pre-order-to-ship gap | **[COMM]** |
| 2026-02-22 | *"1 Week Review - Happy that I joined the club :)"*, 83 pts | **[COMM]** |
| 2026-03-22 | *"My Xteink X3 Review (vs X4). The Antidote to Smartphones."* | **[COMM]** r/eink |
| 2026-03-25 | Screen protectors listed | **[VENDOR]** |
| 2026-04-01 | Magnetic case, 6 colours | **[VENDOR]** |
| **2026-04-03** | The **Nano / Tong Card (瞳卡)** surfaces — a separate NFC e-paper product | **[COMM]** [r/xteinkHax `1sbjsr3`](https://old.reddit.com/r/xteinkHax/comments/1sbjsr3/), 110 pts |
| 2026-04-08 | *"Crosspoint on X3 - preview with **smooth antialiasing waveforms**"* — the 4-level grey path working on UC8253 | **[COMM]** r/eink, 55 pts |
| **2026-04-28** | *"X3 vs X4 - actual experience comparison"*, **412 pts** | **[COMM]** |
| 2026-05-15 / 06-19 | Pogo cable ($4.99) and adapter ($5.99) listed **separately** | **[VENDOR]** |
| **2026-06-03** | NFC question raised on the CrossPoint discussion board; **maintainer establishes the tag is firmware-independent** | **[COMM]** [discussion #2259](https://github.com/crosspoint-reader/crosspoint-reader/discussions/2259) |
| 2026-06-20 | 20 % off sale via the CrossPoint affiliate link | **[COMM]** |
| **2026-07-01** | **First public teardown** — 13 images, 650 mAh, ESP32-C3, 128 Mbit Puya flash, *"DS1307 RTC"* | **[TD]** [r/xteinkereader `1uksv6s`](https://old.reddit.com/r/xteinkereader/comments/1uksv6s/) |
| **~2026-07** | **Vendor warns the community of the UC8253 → UC8279d panel switch** — the only pre-announced silent hardware change found in this family | **[SDK]** `docs/xteink-x3-uc8279-support.md` |
| **2026-08-07** | **CrossPoint 1.5** — *"this release DOES support the new x3 display variants"*, **763 pts, 305 c** | **[COMM]** |
| 2026-08-08 | NFC use cases documented by owners | **[COMM]** |
| **2026-08-10** | Two-unit comparison: **four back-casing variants**, a visible contrast/speed difference, and **lock state uncorrelated with channel** | **[COMM]** [`1vkuhbi`](https://old.reddit.com/r/XTEINK/comments/1vkuhbi/) |
| 2026-08-18 | An X3 acquired for **$16**; sharpest published criticism of vendor conduct | **[COMM]** |
| 2026-09-02 | **Rear glass cracking** report; question about metal backing goes **unanswered** | **[COMM]** |
| 2026-09-04 | **$69.00**, both colours in stock | **[VENDOR]** |

## Position in the family

The X3 is the **second** device and the vendor's own stated iteration on the X4:
*"builds on everything we learned from building the X4"*. It went **smaller,
sharper and better-instrumented** rather than more powerful — the SoC, flash,
button scheme and shared-SPI architecture are unchanged.

| Relationship | Device |
|---|---|
| Predecessor / sibling | [X4](../x4/README.md) — same board family, one C3 binary serves both |
| Upmarket sibling | [X4 Pro](../x4-pro/README.md) — S3, PSRAM, touch, frontlight |
| Buttons-only S3 sibling | [X4 Classic](../x4-classic/README.md) — not internationally listed |
| Android sibling | [S4](../s4/README.md) |
| Accessory product | [Nano / Tong Card](../nano/README.md) — NFC e-paper card, **often confused with the X3's NFC tag** |
| Announced successor to the X4 | **"X4 version 2"**, vendor-confirmed for September 2026, spec unknown |

## Manufacturing: outsourced and visibly inconsistent

The four back-casing variants observed by owners — sticker label, engraved text,
completely clean, faint labelling — across purchases from the official site,
Amazon.ca, AliExpress and Xianyu, support a community reading:

> "They'll outsource to a bunch of manufacturers who can meet the specs."

Combined with the **panel-controller change** and **unpredictable USB-lock state
by channel**, the practical conclusion is that **two X3s are not necessarily the
same device**, and nothing external tells you which you have.

## What "learned from the X4" actually produced

| Change | Direction |
|---|---|
| 3.7″ / 792×528 / ~257 PPI vs 4.26″ / 800×480 / ~219 | **sharper, smaller** |
| 55 g vs ~80 g | **lighter** |
| BQ27220 gauge vs bare ADC | **better** |
| RTC added (X4 has none) | **better** |
| QMI8658 IMU + NFC added | **better** |
| SD power enable added (GPIO13) | **better** — the X4 cannot sleep its card |
| **USB-C → magnetic pogo** | **worse, and the most-contested change in the family** |
| Button feel | **worse** per owners — *"mushy and quieter"* |
