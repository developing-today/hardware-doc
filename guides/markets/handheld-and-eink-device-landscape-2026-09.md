# Handheld and e-ink device landscape — September 2026

> **What to buy, for what, as of 2026-09-07.** Every device record in this
> repository, grouped by the thing a buyer is actually shopping for rather than by
> vendor.
>
> **Nothing here is a new measurement or a new retrieval.** Every cell is read out
> of the linked device or component record. Where a record marks something
> `unknown`, this page marks it `unknown` too — it does not fill the gap.

## How to read this page

This is an **aggregation**, not a source. Where a cell disagrees with the record
it links to, **the record wins** — the standing rule from
[the guides index](../README.md#conventions).

**"—" means the device does not have the thing. "unknown" means no record
establishes it.** The distinction is load-bearing throughout: an absent frontlight
is a design decision, an absent battery capacity is a research gap.

Prices are **item-only, vendor-direct, before shipping and duty**, on the date
given in each table. They are not normalised across currencies or tax regimes;
[the PaperMono pricing record](../../devices/m5stack/papermono/market-and-pricing.md)
explains why a GBP-inclusive figure and a USD-exclusive figure are not the same
kind of number even before an exchange rate is applied.

### Relationship to the existing comparison matrix

[`device-comparison-matrix.md`](device-comparison-matrix.md) already compares
fourteen devices column-by-column and is the better page if you want raw
specification cells for the Waveshare/Espressif P4 boards, the Inkplates, the
XIAO, ZeroWriter and Tanmatsu. **It was compiled 2026-08-30 and predates the
Xteink, M5Stack Cardputer/PaperMono/Cap and LilyGO research passes**, so it does
not contain them.

This page is complementary and differently shaped:

| | [Comparison matrix](device-comparison-matrix.md) | This page |
|---|---|---|
| Organised by | Specification axis (processors, memory, display…) | **What you are shopping for** |
| Covers | 14 devices, as of 2026-08-30 | **Every device record**, as of 2026-09-07 |
| Ends in | Conflicts between records | **Prose recommendations, and where a comparison is not supportable** |

Read the matrix for cells; read this for decisions. Neither is a substitute for
the device record.

---

## Group 1 — Pocket e-ink readers

The question this group answers: *I want a small, battery-powered, e-ink thing to
read on, and I want to be able to reflash it.*

### 1.1 The table

Prices dated **2026-09-04** (Xteink, from the vendor store API) and **2026-09-01**
(M5Stack, Waveshare) and **2026-08-24** (ZeroWriter).

| | [Xteink X3](../../devices/xteink/x3/README.md) | [Xteink X4](../../devices/xteink/x4/README.md) | [Xteink X4 Pro](../../devices/xteink/x4-pro/README.md) | [Xteink X4 Classic](../../devices/xteink/x4-classic/README.md) | [M5Stack PaperMono](../../devices/m5stack/papermono/README.md) | [PaperMono-Lite](../../devices/m5stack/papermono-lite/README.md) | [Waveshare ESP32‑S3‑ePaper‑3.97](../../devices/waveshare/esp32-s3-epaper-3.97/README.md) | [ZeroWriter Ink](../../devices/zerowriter/zerowriter-ink/README.md) | [ZeroWriter Fold](../../devices/zerowriter/zerowriter-fold/README.md) |
|---|---|---|---|---|---|---|---|---|---|
| **SoC** | ESP32‑C3 (RISC‑V) | ESP32‑C3 | **ESP32‑S3** (Xtensa) | **ESP32‑S3** | ESP32‑S3R8 | ESP32‑S3R8 | ESP32‑S3R8 (`WROOM‑1‑N16R8`) | **ESP32‑WROVER ×1 + ESP32‑WROOM‑32U ×1** | unknown ("in‑house") |
| **SRAM / PSRAM / flash** | 400 KB / **none** / 16 MB | 400 KB / **none** / 16 MB | 512 KB / **8 MB** / 16 MB | 512 KB / **8 MB** / 16 MB | 512 KB / **8 MB OPI** / 16 MB | same | 512 KB / **8 MB octal** / 16 MB | WROVER (PSRAM in module) / unknown | unknown |
| **Panel** | 3.7″ **792×528, ~257 PPI**, UC8253 *or* UC8279d | 4.26″ 800×480, ~219 PPI, SSD1677/UC8179/UC8279 | 4.26″ 800×480, same three | 4.26″ 800×480, same three | 3.97″ 480×800, **235 DPI**, DKE panel + SSD1677 | same | 3.97″ 800×480, 235 DPI, SSD1677 | 5.2″ **1280×720** `ED052TC4` | 6″, resolution unknown |
| **Greyscale** | 1 bpp | 1 bpp | 1 bpp | 1 bpp | **4 levels** (vendor claim; panel manual says 2 — unresolved) | same | **4 levels** | unknown | unknown |
| **Frontlight** | — | — | **dual warm/cool** | — | **yes**, AW9967 boost | **yes** | — | — | **yes, 10 levels** (claim) |
| **Touch** | — | — | **GT911** | — | **FT6336G** | **FT6336G** | — | — | unknown |
| **Other input** | 6 buttons on a **2‑pin ADC ladder** + power | same | **2 side keys** + capacitive Home pad | **7 discrete ISR GPIOs** | 2 keys + power | 2 keys + power | **3‑way rotary nav** + PWR + BOOT | **60 % hot‑swap mechanical keyboard** | Choc v1 hot‑swap keyboard |
| **Radios** | Wi‑Fi + BLE | Wi‑Fi + BLE | Wi‑Fi + BLE | Wi‑Fi + BLE | Wi‑Fi + BLE **+ NFC (ST25R3916) + LoRa (SX1262)** | Wi‑Fi + BLE | Wi‑Fi + BLE | Wi‑Fi/BT present, **off by default** | claims "no Wi‑Fi required" |
| **Other sensors** | **BQ27220 gauge**, DS‑series RTC, **QMI8658 IMU**, **passive NFC tag** | none | BM8563 RTC, CW2017 gauge | BM8563, CW2017, **QMI8658 IMU** | BMI270, RX8130CE RTC, PDM mic, buzzer | same | QMI8658A, PCF85063ATL, **SHTC3**, ES8311 + NS4150B audio | RTC | unknown |
| **Battery** | **650 mAh** | unknown | unknown | unknown | **1150 mAh** | 1150 mAh | header only, **capacity unknown** | claim ~100 h | claim 50–100 h |
| **Storage** | microSD on the **display SPI bus** | same, **no power enable** | **native SDMMC** | **native SDMMC** | microSD, 4‑bit SDMMC | same | microSD | microSD | microSD |
| **Expansion** | — (sealed) | — | — | — | **none — no Grove, no M‑Bus** | none | **none** (vendor claim of expansion is [refuted](../../devices/waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md)) | — | — |
| **Price** | **$69** | **delisted**, last $69 | **$99** | **never priced** | **$65** *(out of stock 2026‑09‑01)* | **$55** *(out of stock)* | **$34.99–47.99**, 3 SKUs | **$285** | ~$239 first wave / ~$329 |
| **Vendor's own material** | **Nothing.** No schematic, no SDK, no datasheet; product copy demonstrably false | same | same | same | **6‑sheet schematic**, MIT UserDemo, pinned libraries — but [NFC sheet 1 of 2 unpublished](../../devices/m5stack/papermono/features/nfc.md) | 4‑sheet `PRJ`, not retrieved | Schematic published; sample repo **has no `LICENSE`** → `unknown` | KiCad design published; **application firmware binaries only** | none yet; "open source in the coming months" |
| **Record depth here** | deep | deep | deep | medium | **deepest in the repo** | variant record | full | full | vendor-claims overview |

### 1.2 What the table hides

**"X4 Pro" is not an enhanced X4, and the naming is actively misleading.** They
share a screen size and a brand. Different ISA (Xtensa LX7 vs RISC-V), different
flash layout, different input hardware, different charging connector.
[CrossPlay had to repoint its OTA URL](../../software/applications/crossplay/README.md)
specifically because upstream's release would flash a C3 image onto an S3. Treat
them as unrelated computers that happen to be sold by the same shop.

**The cheapest Xteink has the sharpest screen and the most sensors.** The X3 at
$69 is ~257 PPI against ~219 for the 4.26″ models, is 55 g against ~80 g, and is
the only one with a proper TI impedance-track fuel gauge, an IMU and an NFC tag.
The "Pro" has none of the last three. A price-ordered reading of that family is
wrong in three separate places.

**The frontlight/touch premium is $30 and it costs you the USB-C port.** The X4
Pro charges over a proprietary magnetic pogo connector and ships needing a $4.99
cable. This is the single most-complained-about design decision in that community
([community record](../../devices/xteink/x4-pro/community.md)). The X4 — the only
Xteink with USB-C charging — is delisted and its accessories are exhausted.

**The PaperMono is not competing with the Xteinks on price and should not be
compared to them on it.** At $65 it is roughly an X3 plus $0, but it is a
*development board*: published schematic, USB-C, a documented power architecture,
and no USB lock. It also has NFC and LoRa fitted, which nothing else in this group
does. What it does not have is an expansion connector of any kind, an enclosure
ecosystem, or stock. It was out of stock at the official store on 2026-09-01 and
listed by no reseller anywhere.

**Two boards in this group carry a "3.97-inch 4-greyscale SSD1677" panel with the
same active area to 0.01 mm, transposed** — the PaperMono (480×800) and the
Waveshare (800×480). The Waveshare record asks whether they are the same glass and
[does not resolve it](../../devices/waveshare/esp32-s3-epaper-3.97/README.md). Do
not assume waveforms transfer.

**ZeroWriter is in this group because the brief put it here, and it does not
belong.** The Ink is a 300 × 195 × 15 mm slab with a mechanical keyboard, and the
Fold is 900 g and opens like a laptop. Neither is pocketable and neither is a
reader — they are writing appliances with a text editor and no browser, and the
Fold's marketing is explicit that refusing features is the product. If you want to
*read*, they are the wrong purchase at four times the price.

### 1.3 ⚠ Comparisons this group does **not** support

State these plainly rather than inventing precision:

- **Battery life cannot be compared for any device here.** Only the X3
  (650 mAh) and the PaperMono (1150 mAh) have a published capacity, the Waveshare
  publishes none at all, and **no device in this repository has a measured
  runtime, refresh-power figure or frontlight current from anyone**. The X3
  teardown author explicitly planned to attach a Nordic Power Profiler Kit II and
  never posted results.
- **Refresh speed cannot be compared across vendors.** The Xteink figure
  (~38 ms plane write at 20 MHz) is an SDK source comment for a *plane write*; the
  Waveshare figures (3.5 s full / 0.6 s partial) are whole-refresh vendor claims
  and its own panel manual disagrees with its board page; M5Stack publishes four
  refresh timings with no method. These are three different quantities.
- **"4-level greyscale" is not established on the PaperMono.** M5Stack claims it
  and the vendor demo implements it, but the DKE panel manual's own optical table
  reads `GN — 2Grey Level`. Recorded unresolved.
- **Price-per-pixel comparisons are meaningless here** because the Xteink price
  includes an enclosure, a battery, a case ecosystem and a charging accessory
  market, and the Waveshare and PaperMono prices do not include an enclosure at
  all in the Waveshare's case. A community member's open-source ESP32-S3 e-paper
  dev kit came out at a *"full unit BOM around $60 including display and battery"*
  — roughly the price of a finished X4.

### 1.4 Who should buy which

**Buy an [Xteink X3](../../devices/xteink/x3/README.md) at $69** if you want the
sharpest, lightest pocket reader that has a large live firmware ecosystem, and you
can live with pogo-pin charging and mushy buttons. It is also the best of the
family as a *sensor* platform — gauge, RTC, IMU and an NFC tag — if you are
building something rather than only reading.

**Buy an [Xteink X4 Pro](../../devices/xteink/x4-pro/README.md) at $99** only if
you specifically want touch *and* a frontlight in a sealed pocket device. You are
paying $30 for those two things and losing an IMU and USB-C charging. It is also
the ecosystem's design floor — CrossPlay names it as the reference target — so it
is the best-supported S3 target.

**Buy a [PaperMono](../../devices/m5stack/papermono/README.md) at $65** if you
intend to *develop*. You get a published schematic, a documented five-state power
architecture, USB-C, no unlock dance, and NFC and LoRa hardware nobody else in this
group fits. Accept that you get no enclosure ecosystem, no expansion header, and —
at the snapshot — no stock.

**Buy the [Waveshare ESP32-S3-ePaper-3.97](../../devices/waveshare/esp32-s3-epaper-3.97/README.md)
at $34.99** if you want the cheapest credible ESP32-S3 + PSRAM + e-paper platform
and you do not need a case, a frontlight or touch. Note two corrections that record
makes to its own vendor's marketing: **the PMIC is an AXP2101, not the "TG28" the
storefront names**, and **the board has no expansion header of any kind**.

**Do not buy an [X4](../../devices/xteink/x4/README.md) new** — you cannot; it is
delisted. Buy one used only if USB-C charging matters more to you than everything
else, and note that **at least two X4 board revisions exist that are not externally
distinguishable**, one of which does not self-latch its battery MOSFET.

**Do not buy an [X4 Classic](../../devices/xteink/x4-classic/README.md)** — not
because it is bad (S3 + PSRAM + six real buttons + an IMU is the best silicon
combination in the family) but because it has never been listed internationally,
has no published price, and no photograph of it exists anywhere.

**One warning that applies to every Xteink purchase:** USB-lock state is **not
predictable from the sales channel**. One owner reported an Amazon X3 unlocked, an
official-store X3 locked and an AliExpress X4 locked. Assume you will need the
unlock procedure; see [`firmware-ecosystem.md`](../../devices/xteink/firmware-ecosystem.md).

---

## Group 2 — Keyboard handhelds

The question: *I want a pocket computer with a real keyboard.*

### 2.1 The table

| | [Cardputer v1.1](../../devices/m5stack/cardputer-v1.1/README.md) | [Cardputer ADV](../../devices/m5stack/cardputer-adv/README.md) | [T-Display K230 Kit](../../devices/lilygo/t-display-k230/README.md) | [Tanmatsu](../../devices/nicolai-electronics/tanmatsu/README.md) | [CardputerZero](../../devices/m5stack/cardputer-zero/README.md) |
|---|---|---|---|---|---|
| **Class** | MCU | MCU | **Linux** | MCU | **Linux** |
| **SoC** | ESP32‑S3FN8 | ESP32‑S3FN8 | **Canaan Kendryte K230**, 2× RV64 C908 (1.6 GHz + 0.8 GHz) | **ESP32‑P4NRW32**, 2× RISC‑V | **Raspberry Pi CM0** (RP3A0, 4× Cortex‑A53) |
| **RAM / PSRAM / flash** | 512 KB / **none** / 8 MB in‑package | 512 KB / **none** / 8 MB in‑package | **1 GB LPDDR4** / — / microSD boot | **32 MB in‑package PSRAM** / 16 MB flash | **512 MB LPDDR2** / microSD only |
| **Display** | 1.14″ 240×135 IPS, ST7789V2 | same | **4.1″ 568×1232 AMOLED**, RM69A10, MIPI DSI | 3.97″ 480×800 IPS, ST7701S, **MIPI DSI 2‑lane** | 1.9″ 320×170, ST7789v3 |
| **Keyboard** | 56 keys, **74HC138 GPIO matrix (10 GPIOs)** | 56 keys, **TCA8418 over I²C (3 GPIOs)** | **QWERTY on a separate base board**, TCA8418 7×10 | **69‑key QWERTY** + 6 function keys, backlit, by Solder Party | 46 keys, TCA8418 |
| **Other input** | — | **BMI270 IMU** | GT9895 touch, GC2093 camera | — | touch, IMX219 camera, BMI270 + BMM150 |
| **Radios** | Wi‑Fi + BLE | Wi‑Fi + BLE | **RTL8189FS Wi‑Fi (SDIO)**, BT **via USB dongle only**, SX1262 *or* **LR2021** LoRa, nRF9151 LTE‑M/NB‑IoT + GNSS, nRF52840 BLE | ESP32‑C6 (Wi‑Fi 6 / BLE 5.3 / 802.15.4) + **Ebyte E22 SX1262 LoRa** | Wi‑Fi + **10/100 Ethernet** (SR9900A) |
| **Audio** | NS4168 + SPM1423 PDM mic | **ES8311 codec** + NS4150B + 3.5 mm jack | MAX98357A + mic | yes | ES8389 + AW8737A + **3.5 mm TRRS** |
| **Battery** | 120 mAh + **1400 mAh base** | **1750 mAh** | 21700 pack (base‑dependent) | unknown here | **1750 mAh** |
| **Expansion** | Grove only | Grove + **EXT 2.54‑14P "Cap" socket** | **2×20 header** + two base boards + RJ45 | **36‑pin expansion port** | **EXT 2.54‑14P (not Cap‑compatible)** + Grove |
| **Price** | **$29.90, `[EOL]`** | **$29.90** | main unit **$150.31** (SX1262) / **$153.01** (LR2021) · keyboard base **$113.25** with nRF9151 / **$70.94** without → **$263.56 complete** | **€99.17 ex VAT / €119.99 inc** | **not established** |
| **Openness** | Schematics published; `M5Cardputer` MIT | Schematics published; MIT libs; **no certification published** | **BSP published 17 months after launch**; **no schematic at all** | **Full KiCad under CERN‑OHL‑P, firmware MIT** — the most open device in this repository | Schematic published, **not fetched**; vendor says features subject to change |
| **Depth here** | medium | **full** | **full** | full | light — product unfinished |

### 2.2 What the table hides

**The ADV is not "a faster Cardputer" — it is the same SoC with a different
keyboard controller, and that is the entire point.** Moving the 56-key matrix from
a 74HC138 (10 GPIOs) to a TCA8418 on I²C (3 GPIOs) frees **seven pins**, and those
seven pins *are* the Cap header. The compute is identical. If someone tells you the
ADV is faster, they have not read the schematic — both are ESP32-S3FN8, both have
**no PSRAM**, both are 8 MB flash.

**No Cardputer has PSRAM, and this shapes every ambitious project on the
platform.** The Meshtastic-client author memory-mapped a 2.16 MB Unicode font out
of a flash partition because it cannot live in RAM. If your application needs a
framebuffer or a large working set, this family is the wrong answer at any price.

**"T-Display K230 Kit" is two purchases and the store does not say so.** "Main
Unit" and "Keyboard Only" are separate SKUs. A complete keyboard handheld with
cellular is **$263.56** before shipping — 2.6× the sticker price a casual reader
takes away, and 8.8× a Cardputer ADV. A Reddit user on the launch thread asked
exactly which SKU to buy and got no answer.

**The K230 is the only device in this group where "nothing in the ESP32 ecosystem
applies"** — no Arduino, no PlatformIO for the main SoC, no ESP-IDF, a vendor
toolchain at a hard-coded `/opt/toolchain`, and a documented case of a board
bricked with **no recovery section in any LilyGO document**. It is also the only
one with a real NPU, H.265 encode *and* decode, and a Linux userspace.

**Tanmatsu is a different class of machine and priced accordingly.** ESP32-P4 with
**32 MB of in-package PSRAM**, MIPI DSI, a 69-key backlit keyboard designed by
Solder Party, a 36-pin expansion port, and — uniquely here — the complete KiCad
design published under CERN-OHL-P with MIT firmware. At ~€120 it is 4× a Cardputer
ADV and buys you compute, openness and a much better keyboard.

**CardputerZero is the same shape as a Cardputer and is not one.** It is a
Raspberry Pi CM0 running Linux. Its EXT header is physically identical to the
ADV's and **electrically different** — the left column and the UART pair are not
the same, so a Cap that uses `RESET`/`INT`/`BUSY` (i.e. both M5Stack Caps) will not
work on it. M5Stack's own page carries a "work in progress" banner.

### 2.3 ⚠ Comparisons this group does **not** support

- **No performance comparison is possible between the K230 and the P4.** No
  independent benchmark of the T-Display K230 exists — the BSP *builds CoreMark
  and CoreMark-PRO into the image* and nobody has published a number. The P4's
  6.92 CoreMark/MHz is Espressif's own figure under Espressif's own build. These
  cannot be put in the same table.
- **Battery life is unmeasured on all five.** The Cardputer ADV's ~13–14 h Wi-Fi
  figure is arithmetic on vendor current claims and **ignores backlight**, which
  the record says is likely to dominate. K230 battery life is unmeasured and the
  only community input is scepticism.
- **Keyboard quality cannot be compared from records.** Nobody in this repository
  has typed on more than one of these.

### 2.4 Who should buy which

**Buy a [Cardputer ADV](../../devices/m5stack/cardputer-adv/README.md) at $29.90**
unless you have a concrete reason not to. It is the cheapest keyboard computer here
by a factor of four, it has the broadest community firmware support, its Cap socket
is a genuine expansion bus in the exact shape an SX1262 or CC1101 wants, and board
autodetect means one binary serves both generations. Do not buy the
[v1.1](../../devices/m5stack/cardputer-v1.1/README.md) at the same price — it is
`[EOL]` and strictly worse — **unless** you need a firmware that has not been
ported (Evil-M5Project's ADV support is unconfirmed; NEMO has no ADV config).

**Buy the [Cardputer Mesh Kit](../../devices/m5stack/cardputer-mesh-kit/README.md)
at $48** instead of the parts if you want the Meshtastic licensed-device
registration; the bundle premium over ADV + Cap is $3.60 and registration is
**restricted to the kit**. If the badge does not matter, buy the parts.

**Buy a [Tanmatsu](../../devices/nicolai-electronics/tanmatsu/README.md) at ~€120**
if you need compute, a proper keyboard, or openness. It is the only device in this
repository whose full hardware design you can read, modify and rebuild.

**Buy a [T-Display K230](../../devices/lilygo/t-display-k230/README.md)** only if
you specifically need on-device Linux with an NPU and a MIPI camera, or specifically
want RISC-V, and you are comfortable building an image on Ubuntu with a vendor
toolchain and no documented recovery path. Do not buy it as a Meshtastic node — a
$30 dedicated node does that better and lasts far longer on a charge.

**Do not buy a [CardputerZero](../../devices/m5stack/cardputer-zero/README.md)
yet.** The vendor says its features are subject to change.

---

## Group 3 — Display development boards

The question: *I want an MCU with a screen on it that I can program.*

### 3.1 The table

The [T-Display-S3 family](../../devices/lilygo/t-display-s3-shared/README.md) is
**eleven electrically distinct boards sharing a marketing prefix**, so it is
summarised as a family with the reference board broken out. Prices dated
**2026-09-07** (LilyGO), **2026-08-21** (Waveshare knob), **2026-08-24** (XIAO).

| | [T-Display-S3](../../devices/lilygo/t-display-s3/README.md) (reference) | T-Display-S3 family (10 others) | [Waveshare Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) | [XIAO ESP32S3 Sense](../../devices/seeed-studio/xiao-esp32s3-sense/README.md) |
|---|---|---|---|---|
| **SoC** | ESP32‑S3R8 **bare die** | ESP32‑S3R8 on every board | ESP32‑S3R8 **+ a second full SoC, ESP32‑U4WDH** | ESP32‑S3R8 |
| **RAM / PSRAM / flash** | 512 KB / 8 MB OPI / 16 MB W25Q128JV | same throughout | 512 KB / 8 MB / 16 MB (+ 4 MB on the U4WDH) | 512 KB / 8 MB / 8 MB |
| **Display** | 1.9″ 170×320 ST7789V on an **8‑bit Intel‑8080 parallel** bus | **eight different controllers** across QSPI, parallel and 4‑wire SPI | 1.8″ **round 360×360**, ST77916 *or* SH8601 (unresolved) | **none** |
| **Touch** | — | CST816S · CST328 · CST226SE · CST3530 · CST9217 · FT3168 · CHSC5816 · AXS15231B | CST816D | — |
| **Other input** | BOOT + GPIO14 | not portable between boards | **two directional knobs, one per MCU** | — |
| **Radios** | Wi‑Fi + BLE | Wi‑Fi + BLE | Wi‑Fi + BLE **+ Bluetooth Classic (on the U4WDH only)** | Wi‑Fi + BLE |
| **Notable** | — | **PMIC differs per board**: TP4065 / SY6970 / BQ25896 / AXP2101 | DRV2605L haptics, PCM5100A DAC, PDM mic, **USB‑C plug orientation selects which MCU you talk to** | **camera + PDM mic + microSD daughterboard**, 21 × 17.8 mm |
| **Expansion** | header pins | varies | two PH1.27 10‑pin headers, **pinout not published** | castellated + B2B |
| **Price** | **$9.04** bare / $12.61 Touch / $13.22 with shell | varies | not captured in the record | **$13.99** (+ $11.99 OV5640 option) |
| **Openness** | MIT for `T-Display-S3`, `T-Display-S3-AMOLED`, `LilyGo-AMOLED-Series`; **none declared** for Long and Pro; **GPL‑3.0** for the 1.64 / 1.43‑1.75 repos | as left | wiki + firmware | schematic + **FCC exhibits** published |
| **Depth here** | full | 4 full, 5 medium, 1 stub | full | full |

### 3.2 What the table hides

**"T-Display-S3" is a marketing prefix, not a platform.** The family record is
blunt about it: code written for the base board will not run on any AMOLED board
without changing the display driver, the bus type, the button pins *and* the power
sequence. The only thing that ports unchanged is the Arduino board configuration.
Three traps recur family-wide and catch nearly everyone:

1. **The `USB CDC On Boot` trap.** With `ARDUINO_USB_CDC_ON_BOOT=1` — which
   LilyGO's own instructions require — the Arduino core blocks at startup waiting
   for a host to open the port. Run the same firmware from a battery and it hangs
   before `setup()` finishes, looking like a dead board.
2. **The Arduino-core version pin.** LilyGO tests at **2.0.14** and says versions
   above it may not work; TFT_eSPI is named specifically. Corroborated
   independently: the newest factory binary in the repo is built on ESP-IDF v4.4.6,
   the base of arduino-esp32 2.0.14.
3. **The display-bus split.** `TFT_eSPI` has no QSPI transport at all. Which
   graphics library works depends on the *bus*, not the board name.

**The Waveshare knob board has two full ESP32-class SoCs on it, not a helper
chip.** The ESP32-S3 has no Bluetooth Classic radio — a silicon-level omission no
library can fix — so Waveshare soldered an original ESP32 next to it purely to do
A2DP/AVRCP/HFP/SPP. Consequence: Classic Bluetooth on that board means flashing a
second, separate firmware image **over a differently-oriented USB-C connection**.

**The XIAO ESP32S3 Sense has no display and is in this group only because it is the
other "small ESP32-S3 you develop on" record.** Its two most expensive gotchas are
that **the user LED and the SD chip select are the same pin (GPIO21)** and that
**the camera and microphone occupy all four JTAG pins**.

### 3.3 ⚠ Comparisons this group does **not** support

- **The Waveshare knob board has no captured price**, so it cannot be placed on a
  value axis against the $9.04 T-Display-S3 or the $13.99 XIAO.
- **The knob board's display controller is genuinely unresolved** — marketed
  ST77916, driven by an SH8601 compatibility driver. Do not assume either.
- **Two LilyGO boards have no declared licence at all** (Long, Pro). "MIT
  family" is wrong as a blanket statement.

### 3.4 Who should buy which

**Buy a [T-Display-S3](../../devices/lilygo/t-display-s3/README.md) at $9.04** for
almost any "ESP32-S3 with a screen" job. Nothing else in this repository puts an
ESP32-S3 with 16 MB flash *and* 8 MB OPI PSRAM *and* a colour display at under
ten dollars. Read the family record's three traps first; each of them costs an
evening otherwise.

**Buy a [XIAO ESP32S3 Sense](../../devices/seeed-studio/xiao-esp32s3-sense/README.md)
at $13.99** when the job is a networked camera you need to hide inside something.
It is 21 × 17.8 mm and is the cheapest credible route to one. Do not buy the OV5640
upgrade reflexively — at $11.99 it is 86 % of the board.

**Buy the [Waveshare knob board](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md)**
if you specifically need Bluetooth Classic audio *and* a rotary UI in a CNC metal
enclosure, and you accept a two-image flashing procedure and an undocumented
inter-MCU protocol. Otherwise its dual-MCU architecture is a cost, not a feature.

---

## Group 4 — LoRa, sub-GHz and mesh add-ons

The question: *I want to add a radio to something I already have.*

### 4.1 The table

All prices from `shop.m5stack.com`, retrieved **2026-09-04**.

| | [Cap LoRa-1262](../../devices/m5stack/cap-lora-1262/README.md) | [Cap LoRa868](../../devices/m5stack/cap-lora868/README.md) | [Cap CC1101 & NFC](../../devices/m5stack/cap-cc1101/README.md) | [Unit C6L](../../devices/m5stack/unit-c6l/README.md) | [Stamp C6LoRa](../../devices/m5stack/stamp-c6lora/README.md) | [LoRa Unit E220](../../devices/m5stack/unit-lora-e220/README.md) | [LoRaWAN Unit](../../devices/m5stack/unit-lorawan-stm32wle5/README.md) |
|---|---|---|---|---|---|---|---|
| **SKU** | U214 | U201 **`[EOL]`** | **U219** | U202 | S012 | U170 / U170‑433 | U184‑\* |
| **Published** | 2025‑12‑30 | 2025‑09‑05 | **2026‑08‑28** | 2025‑10‑10 | 2026‑03‑13 | 2023‑10‑20 / 2024‑07‑12 | 2024‑12‑20 |
| **Radio** | **SX1262** + ATGM336H GNSS | SX1262 + ATGM336H | **CC1101** (4 bands) + **ST25R3916 NFC** | SX1262 | SX1262 | **LLCC68** behind an AT modem | **STM32WLE5** (RAK3172) |
| **Host interface** | **SPI** | SPI | **SPI**, both chips | **none — it is its own node** | SPI (module) | **UART, AT commands** | **UART, AT commands** |
| **Attaches to** | Cardputer‑Adv, CardputerZero | same | same | **any Grove host** | solder‑down SMD | **any Grove host** | any Grove host |
| **Bands** | 868–923 MHz, **one wideband SKU** | 868–923 MHz | **315 / 433 / 868 / 915**, switched | 868–923 MHz | 850–960 MHz | 920.6–928 (JP) / 410–493 | **region per SKU** |
| **TX power** | +22 dBm | +20 dBm | **+10 dBm** | +22 dBm | +22 dBm | 13 dBm / 22 dBm | 22 dBm |
| **Certification published** | **none** | **none** | **none** | none | none | **Telec `001-P01730`** (U170 only) | **RAK3172 module cert linked** |
| **Meshtastic** | ✅ upstream variant | ✅ (same variant, degrades gracefully) | ❌ — CC1101 cannot do LoRa | ✅ **own upstream variant**, `M5STACK_C6L = 111` | ❌ no variant | ❌ and cannot have one | ❌ different protocol universe |
| **Price** | **$14.50** | $14.50 | **$18.95** | **$22.90** | $12.95 | $33.00 / $12.95 | $21.50 / $18.95 (CN470) |
| **Depth here** | full, **schematic held** | medium, schematic **not fetched** | full, **schematic held** | light | light | light | light |

### 4.2 What the table hides

**The most useful power data in this whole family is on the discontinued
product.** The `[EOL]` Cap LoRa868's page breaks current into four named states —
GPS on/LoRa standby 29.24 mA, GPS sleep/LoRa standby **3.16 mA**, GPS sleep/LoRa TX
max 129.72 mA, GPS on/LoRa TX max 155.03 mA. Its successor replaces all four with a
single unconditioned "163.4 mA". Read across: **the GNSS dominates idle draw and
sleeping it is worth almost an order of magnitude.** Those numbers are for a
+20 dBm board with no shield can and **must not be transplanted** into a U214 table
— but the *shape* of the tradeoff carries.

**CC1101 cannot do LoRa, and the frequencies overlapping is why people keep
asking.** LoRa is chirp spread spectrum, Semtech owns the patents, TI does not make
LoRa silicon. The Cap CC1101 is a Flipper-Zero-class sub-GHz capture/replay radio
plus an NFC front end. There is **one Cap slot**, so the two Caps are mutually
exclusive — a limitation owners complain about explicitly.

**A house pattern runs through three M5Stack LoRa products: put the SX1262's RF
switch behind an I²C I/O expander rather than spending a host GPIO on it.** Cap
LoRa-1262 uses a PI4IOE5V6408; Stamp C6LoRa uses one and puts the *LNA enable*
there too; the PaperMono uses M5Stack's own M5IOE1. The recurring consequence is
**no I²C, no radio** — an I²C fault takes the RF path down even though SPI is fine.
Anyone porting M5Stack LoRa hardware should look for the expander before concluding
a radio is dead.

**The Cap CC1101's band switching is the single most portable idea in this
group.** One antenna port, four bands, two SP3T switches — and only *one* of the
two control lines is a host GPIO. The other is the **CC1101's own GDO2 pin**, set
over SPI. It costs one host pin instead of two; the price is that you cannot set
the band before the transceiver is talking.

**"Which LoRa for a Cardputer" has a different answer depending on which
Cardputer.** The original K132/K132-V11 has **no expansion bus** — only a Grove
port — so no Cap can attach at any price. Its answers are a Grove/UART modem
(E220, LoRaWAN Unit) or the **Unit C6L, which is its own complete Meshtastic node**
with its own MCU, screen, flash and antenna, cabled to the Cardputer as a
companion.

**Only two products in this family have any regulatory paperwork at all.** The
E220 JP unit carries a Telec number printed in its specification table, and the
LoRaWAN Unit splits by region per SKU and points at RAK3172 module certification.
Every Cap — U201, U214, U219 — is a single wideband SKU spanning EU 868, US 915 and
JP 920 allocations with **no published certification identifier of any kind**.

### 4.3 ⚠ Comparisons this group does **not** support

- **No RF measurement of any kind exists for any product here.** No range, no
  throughput, no sensitivity, no current, from any party. The vendor's
  "435 m / 441 m" for the CC1101 names a modulation and an air rate but no antenna,
  height, terrain or link-margin criterion.
- **The Unit C6L's own vendor table says receive standby draws *more* than
  continuous transmit** (85.18 mA vs 80.02 mA) with no stated conditions. That is
  not impossible — SX1262 receive in LDO mode is expensive and the TX figure may be
  duty-cycled — but do not build a power budget on it.
- **Whether the Cap LoRa868 has an I/O expander is unresolved.** Meshtastic's
  `variant.cpp` says it does; M5Stack's own comparison table says "RF Switch
  Control: None". The U201 schematic is published and would settle it; it was not
  fetched.
- **U201 and U214 current figures must not be merged.** Different TX power,
  different shielding.

### 4.4 Who should buy which

**Cardputer-Adv or CardputerZero, want LoRa/Meshtastic:** the
[Cap LoRa-1262 at $14.50](../../devices/m5stack/cap-lora-1262/README.md). It
supersedes the U201 and is what ships in the Mesh Kit.

**Cardputer-Adv, want sub-GHz capture/replay and NFC:** the
[Cap CC1101 at $18.95](../../devices/m5stack/cap-cc1101/README.md) — and accept
that you cannot have LoRa at the same time. It is also, for anyone reading this
repository for the e-ink firmware work, **the cleanest published example of
"NFC + sub-GHz on one SPI bus with a shared antenna"**; see
[the LoRa/NFC/sidelight guide](../hardware/adding-lora-nfc-and-sidelight-to-eink-firmware.md).

**Original Cardputer (K132/V11), want Meshtastic:** the
[Unit C6L at $22.90](../../devices/m5stack/unit-c6l/README.md). It is a complete
node, it has its own upstream Meshtastic variant, and the Grove cable is a link to
a companion, not a peripheral bus. ⚠ The exact Cardputer↔C6L transport was **not
verified** — check before promising it works.

**You need a point-to-point serial link and do not care about mesh:** the
[E220 unit](../../devices/m5stack/unit-lora-e220/README.md) at $12.95 for 433 MHz.
A DIP switch gets you a working link with no configuration code. It can never run
Meshtastic — the host cannot reach the radio's registers.

**You need something deployable rather than benchtop:** the
[LoRaWAN Unit](../../devices/m5stack/unit-lorawan-stm32wle5/README.md). Region is
baked into the SKU and there is certification to point at, at the cost of giving up
direct radio control.

**Do not buy a [Stamp C6LoRa](../../devices/m5stack/stamp-c6lora/README.md)
expecting a Cardputer accessory.** It is a solder-down SMD module for your own
carrier PCB.

---

## Group 5 — Everything else in `devices/`

Included so this page genuinely covers every record. These are documented
elsewhere and are not re-tabulated.

| Record | One line |
|---|---|
| [Cardputer v1.0](../../devices/m5stack/cardputer-v1.0/README.md) | The original. Same mainboard schematic file as the v1.1, **byte-identical** — every published difference is in the Stamp module |
| [Cardputer Mesh Kit](../../devices/m5stack/cardputer-mesh-kit/README.md) | ADV + Cap LoRa-1262 + antenna, $48, **the only route to Meshtastic device registration** |
| [DinMeter](../../devices/m5stack/dinmeter/README.md) · [v1.1](../../devices/m5stack/dinmeter-v1.1/README.md) | 1/32-DIN panel-cutout instrument head, orange knob, 6–36 V input, $24.50. v1.1 is a **core-module swap only** — M5Stack re-served the v1.0 schematic and STL under v1.1 filenames, byte-identical |
| [Xteink S4](../../devices/xteink/s4/README.md) | Android 11 reader, ~¥339. **Stub — no SoC, no chip, no board fact is established.** Outside the ESP32 firmware ecosystem entirely |
| [Xteink Nano / Tong Card](../../devices/xteink/nano/README.md) | Battery-less **NFC-powered** four-colour e-paper card. Not a reader. Routinely confused with the X3's embedded NFC tag |
| [Inkplate 5](../../devices/soldered-electronics/inkplate-5/README.md) · [Gen 2](../../devices/soldered-electronics/inkplate-5-gen2/README.md) | Soldered Electronics e-paper dev boards; **the Gen 2 is the board ZeroWriter Ink respun** |
| [Waveshare ESP32-S3-ePaper-1.54](../../devices/waveshare/esp32-s3-epaper-1.54/README.md) · [ESP32-C6-ePaper-1.54](../../devices/waveshare/esp32-c6-epaper-1.54/README.md) · [PhotoPainter](../../devices/waveshare/esp32-s3-photopainter/README.md) · [e-Paper ESP32 Driver Board](../../devices/waveshare/e-paper-esp32-driver-board/README.md) | The rest of Waveshare's ESP32 e-paper line |
| [Waveshare ESP32-P4 3.4C](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) · [4C](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md) · [shared](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md) | ESP32-P4 + C6 radio touch panels; see the [comparison matrix](device-comparison-matrix.md) |
| [Espressif P4X-Function-EV](../../devices/espressif/esp32-p4x-function-ev-board/README.md) · [P4X-C5](../../devices/espressif/esp32-p4x-c5-function-ev-board/README.md) · [P4X-EYE](../../devices/espressif/esp32-p4x-eye/README.md) · [P4-Function-EV `EOL`](../../devices/espressif/esp32-p4-function-ev-board/README.md) · [P4-EYE `EOL`](../../devices/espressif/esp32-p4-eye/README.md) | Espressif's own P4 evaluation boards |
| [LilyGO T-Display TTGO](../../devices/lilygo/t-display-ttgo/README.md) · [T-QT](../../devices/lilygo/t-qt/README.md) · [T-Dongle-S3](../../devices/lilygo/t-dongle-s3/README.md) | Lineage stubs — predecessors and cousins of the T-Display-S3 line, **not variants of it** |

---

## Cross-cutting observations

Five things fall out of looking at all of these together that are invisible from
any single record.

**1. Certification is absent almost everywhere, and it is not evenly absent.** No
Xteink device, no Cardputer, no PaperMono, no Cap and no LilyGO K230 has a
published FCC/CE/TELEC identifier. The two exceptions in the whole repository are
the E220-JP unit (a printed Telec number) and the LoRaWAN Unit (a linked RAK3172
module certification). If you are building a product rather than a project, that
narrows the shortlist to almost nothing — and note that
[module-level certification does not transfer automatically](../lora/README.md#10-choosing-a-radio)
into your product with your antenna.

**2. The most open device is also the most expensive, and the relationship is not
a coincidence.** Tanmatsu publishes complete KiCad under CERN-OHL-P at ~€120.
Xteink publishes nothing at $69–99 and its product copy is
[demonstrably false](../../devices/xteink/x3/gaps-and-conflicts.md). M5Stack and
Waveshare publish schematics but no certification. The middle of the market
publishes a schematic and hopes you do not ask about the rest.

**3. Runtime documentation is systematically better than product documentation
for reverse-engineered hardware, and systematically worse for vendor hardware.**
The Xteink X4 Classic's *pinout* is documented to HIGH confidence pin by pin from a
firmware dump, while its price, dimensions, mass, battery and photograph are all
unknown — an inversion the record calls out explicitly. The DinMeter is the
opposite: full vendor documentation, and a v1.1 whose only published evidence of
change is a filename.

**4. Two vendors reuse product names across incompatible hardware, and it costs
real time.** "T-Display-S3" spans eleven boards with eight display controllers and
four different PMICs; LilyGO's stock code `K230` is **a transparent-shell T-Embed
CC1101 with no Kendryte silicon in it at all**, and is the top hit when you search
their store for "K230". "Cardputer" spans an ESP32-S3 MCU and a Raspberry Pi CM0
Linux machine with a physically identical, electrically different expansion header.

**5. Shared-bus architecture is the recurring hazard class.** The Xteink C3
devices share one SPI bus between the panel and the SD card. The Cardputer ADV
shares one SPI bus between the microSD and the Cap header. The PaperMono puts
seven devices on one I²C bus, one of which (the IP2315 charger) has a documented
bus-wedge failure mode. M5Stack's three LoRa products put the RF switch behind
I²C. In every case the failure looks like a dead peripheral and is actually
contention or a missing enable.

---

## Evidence boundary

- **Nothing on this page was retrieved, measured, built or flashed.** It is a
  synthesis of records dated between 2026-08-21 and 2026-09-07.
- Each group's price row carries its own observation date. **Prices move**; the
  Xteink X4 went from listed to delisted inside this repository's own snapshot
  window, and both PaperMono SKUs were out of stock on the day they were priced.
- Where two records disagree with each other, the disagreement is stated rather
  than resolved. The comparison matrix's
  [§10](device-comparison-matrix.md#10-conflicts-between-records) holds the
  equivalent list for the fourteen devices it covers.
- **Record depth is not product quality.** The Xteink family is documented in
  depth because its firmware was reverse-engineered by a large community, not
  because the vendor helped.

## Related

- [Device comparison matrix](device-comparison-matrix.md) — specification-axis view of fourteen devices
- [Vendor and marketplace comparison](vendor-comparison.md) — who to buy from and whether the files will still be hosted next year
- [Clones, siblings and variants](clones-and-variants.md)
- [Adding LoRa, NFC and an RGB sidelight to e-ink firmware](../hardware/adding-lora-nfc-and-sidelight-to-eink-firmware.md)
- [SoC choice for battery e-ink devices](../hardware/soc-choice-for-battery-eink-devices.md)
- [Xteink firmware ecosystem](../../devices/xteink/firmware-ecosystem.md)
- [`guides/lora`](../lora/README.md) · [`guides/nfc`](../nfc/README.md) · [`guides/hardware/e-paper-displays.md`](../hardware/e-paper-displays.md)
