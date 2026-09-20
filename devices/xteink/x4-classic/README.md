# Xteink X4 Classic (X4C)

> **Not listed for international sale.** A `x4-classic` collection exists on
> `xteink.com` but contains **no device** — only generic accessories.
> Research retrieval date **2026-09-04**.
> **Depth: medium.** The board is well documented from a firmware dump; the
> *product* is barely documented at all.

## Identity and variants

| Field | Value | Evidence |
|---|---|---|
| Name | **Xteink X4 Classic**, abbreviated **X4C** | **[SDK]** doc title; **[VENDOR]** collection handle `x4-classic` |
| Board tag | **`ESP32S3_X4_CLA`** | **[DUMP]** |
| Board revision string | **`ESP32S3_X4R2_CLA`** | **[DUMP]** — note `R2`, implying at least a revision 2 |
| Default panel string | `ESP32S3_X4_CLA_SSD1677` | **[DUMP]** |
| FreeInk profile | `BoardConfig::XTEINK_X4_CLASSIC` / `Board::XteinkX4Classic` | **[SDK]** `BoardConfig.h:1648–1706` |
| Build flag | `-DFREEINK_DEVICE_X4CLASSIC=1` | **[SDK]** `platformio.sample.ini` `[env:x4c]` |
| Stock firmware analysed | `flashx4c.bin`, app0 = **`xteink_app` v7.0.11** | **[SDK]** |
| Vendor collection | `x4-classic` — exists, **contains 4 generic accessories and no device** | **[VENDOR]** |

**This is a real, shipping product** — a stock flash dump exists and was reverse
engineered — but it appears **not to be sold internationally**. The vendor is
China-first; the S4 followed the same pattern.

## What it is

**The X4 Pro's board with the touchscreen and frontlight removed, and four extra
buttons in their place.**

Same ESP32-S3, same 16 MB flash and 8 MB PSRAM, same 800×480 glass, same display
driver stack, same SDMMC slot, same BM8563 RTC, same CW2017 gauge. Then:

| Removed | Added |
|---|---|
| GT911 touchscreen | **Four extra discrete buttons** on the freed GPIOs |
| Warm/cool frontlight | **A QMI8658 IMU** at 0x6B |

The freed pins are reused directly: touch-power **GPIO2**, SD-power **GPIO5** and
frontlight **GPIO8/GPIO9** all become buttons.

### Discovered before it was announced

[r/XTEINK `1ud0d9c`](https://old.reddit.com/r/XTEINK/comments/1ud0d9c/),
2026-06-22, **300 points**: *"Did we just spot a new X4 model? Physical buttons +
frontlight but no touchscreen in the latest video?"* — the community identified a
buttons-only S3 variant in a vendor video. They were **right about the buttons and
the absence of touch, and wrong about the frontlight**: the X4C has none.

## Key specifications

| Item | Value | Component | Evidence |
|---|---|---|---|
| SoC | **ESP32-S3**, 16 MB flash, 8 MB PSRAM | [`espressif/esp32-s3r8`](../../../components/espressif/esp32-s3r8/README.md) | **[SDK]**, **[DUMP]** |
| Display | 800×480 mono e-ink, 4.26″ | — | **[SDK]** |
| Controller | **SSD1677 · UC8179 · UC8279** | [`solomon-systech/ssd1677`](../../../components/solomon-systech/ssd1677/README.md) · [`ultrachip/uc8179`](../../../components/ultrachip/uc8179/README.md) · [`ultrachip/uc8279`](../../../components/ultrachip/uc8279/README.md) | **[SDK]** |
| **Controller selection** | **NVS `hw_calib`/`screenType`** — **there is no MISO, so the bus probe cannot work** | — | **[SDK]** |
| Touch | **none** — stock instantiates `NoTouchDriver` | — | **[DUMP]** |
| Frontlight | **none** — stock reports *"Frontlight hardware is disabled on this board"* | — | **[DUMP]** |
| Buttons | **Seven discrete active-low GPIOs**, interrupt-driven | — | **[SDK]** |
| RTC | **BM8563** @0x51 | [`generic/bm8563`](../../../components/generic/bm8563/README.md) | **[SDK]** |
| Gauge | **CW2017** @0x63 | [`cellwise/cw2017`](../../../components/cellwise/cw2017/README.md) | **[SDK]** |
| **IMU** | **QMI8658** @0x6B, `WHO_AM_I = 0x05`, **no interrupt line** | [`qst/qmi8658a`](../../../components/qst/qmi8658a/README.md) | **[DUMP]** RE-confirmed |
| Storage | **Native SDMMC** 1-bit, power enable **GPIO6 active-LOW** | — | **[SDK]** |
| USB | Native S3 USB-OTG, D− 19 / D+ 20, **USB-MSC capable** | — | **[SDK]** |
| Charge STAT | GPIO21, active-HIGH | — | **[SDK]**, polarity **pending** |
| Radios | **Wi-Fi and BLE present** | — | **[SDK]** — the most explicit radio statement in the family |
| Audio / LEDs / PMIC / expander | **none** | — | **[SDK]** |

## Pinout

| GPIO | Role | Note |
|---:|---|---|
| 0 | Button **Left** (side) → up / prev | |
| 1 | **Master peripheral/panel rail**, HIGH at boot | |
| 2 | Button **Right** (bottom key) | *was* touch power on the Pro |
| 3 | Button **Power** | |
| **4** | **Plain input, not interrupt-attached** | **Role PENDING** — configured but unused by the SDK |
| 5 | Button **Left** (bottom key) | *was* SD power on the Pro |
| 6 | **SD power enable**, **active-LOW** | *was* BUSY-adjacent on the Pro; **not** a display pin |
| 7 | Button **Right** (side) → down / next | |
| 8 | Button **Confirm** (bottom key) | *was* frontlight cool |
| 9 | Button **Back** (bottom key) | *was* frontlight warm |
| **10** | EPD **RST** | **swapped vs the Pro** |
| 11 | EPD **MOSI** | write-only, no MISO |
| 12 | EPD **SCLK** | |
| 13 | EPD **CS** | |
| **14** | EPD **DC** | **swapped vs the Pro** |
| **18** | EPD **BUSY** | **swapped vs the Pro** |
| 19 / 20 | USB D− / D+ | |
| 21 | Charge STAT | active-HIGH |
| 38 / 39 | I²C SCL / SDA @400 kHz | BM8563 0x51 · CW2017 0x63 · QMI8658 0x6B |
| 40 / 41 / 42 | SDMMC DAT0 / CLK / CMD | |

**The display pins are NOT the same as the X4 Pro's.** DC, RST and BUSY are
permuted:

| Signal | X4 Pro | **X4 Classic** |
|---|---:|---:|
| DC | 18 | **14** |
| RST | 14 | **10** |
| BUSY | 6 | **18** |

SCLK 12 / MOSI 11 / CS 13 are shared. `displaySpiHz` is **20 MHz** on both.
**Porting display code between the two without changing these three pins will
produce a panel that resets and never develops an image** — the exact failure mode
the X4 Pro bring-up spent months on.

## The no-MISO consequence

The X4C display bus has **no MISO line at all**, so the UC81xx `VER`/`FLG` probe
used on every other device in the family **cannot work** — the released line always
floats to `0xFF`.

So the X4C is the **one device where NVS is authoritative**:

```
NVS namespace hw_calib, key screenType (u8):
  1 or 0x0B → UC8179
  2 or 0x0C → UC8279
  3 / default / unset → SSD1677
```

**The factory writes this once.** Its unreliability elsewhere — *"a full-flash from
another unit overwrites it, so it can name the wrong panel"* — becomes a real
hazard here, because there is no live check to override it. **Restoring an X4C
from someone else's full-flash image can leave it with the wrong panel driver and
no way to detect that.**

## Input

Seven discrete, interrupt-driven, active-low GPIOs. Physical layout = the X4 Pro's
**two side keys** plus the C3 X4's **four bottom keys**:

| Action | GPIO |
|---|---:|
| Up / previous page (side Left) | 0 |
| Down / next page (side Right) | 7 |
| Left (bottom key 1) | 5 |
| Right (bottom key 2) | 2 |
| Confirm (bottom key 3) | 8 |
| Back (bottom key 4) | 9 |
| Power | 3 |

The stock array order is **2, 5, 8, 9** ("Bottom Key 1–4"). The SDK notes the
mapping was corrected by hardware testing: *"the old GPIO8/9 left/right assignment
made the physical Confirm/Back keys act as Up/Down."*

**Not an ADC ladder** — unlike the C3 devices, every key is its own GPIO with its
own interrupt. That is strictly better: chords work, no polling, no calibration.

## Evidence quality and confidence

The SDK is unusually explicit about how it decoded this board from
`flashx4c.bin`. The single board-init function `FUN_4214c798` constructs the SPI
bus via `FUN_4214d260(bus,11,12,13,14)` → MOSI 11 / SCLK 12 / CS 13 / DC 14, sets
up I²C at 39/38, and registers every GPIO. **The GPIO mode argument was decoded
from unambiguous pins** — SPI drive lines and the GPIO1 rail use mode 1 = OUTPUT,
the STAT line uses mode 0 = INPUT, buttons use mode 2 = input+ISR.

| Confidence | Items |
|---|---|
| **HIGH** | Display MOSI11/SCLK12/CS13/DC14/RST10/BUSY18; GPIO1 rail; all seven button GPIOs; SD enable GPIO6 (pulsed HIGH 80 ms → LOW 120 ms); charge STAT GPIO21; touch **absent**; frontlight **absent**; the three-controller set; `hw_calib/screenType` |
| **PENDING** | **The role of GPIO4** (an input, but not interrupt-attached, so not a button); charge-STAT polarity; panel orientation |

## Strengths / shortcomings

**Strengths.** S3 + 8 MB PSRAM with **six real navigation keys and an IMU** — the
only Xteink combining those. Native SDMMC. No touchscreen to fail. Cheaper to
build than the Pro.

**Shortcomings.** **Not purchasable internationally.** No frontlight. NVS is the
only panel-controller source of truth, which makes cross-unit flash restores
dangerous. GPIO4's role is unknown. **No teardown, no photograph, no price, no
dimensions, no battery figure.**

## Status: what is and is not known

| Known | Not known |
|---|---|
| Complete pinout, all peripherals, partitions | **Price** — none ever published |
| Stock firmware version (`xteink_app` 7.0.11) | **Availability** — no listing anywhere |
| Board tag and revision string (`ESP32S3_X4R2_CLA`) | **Dimensions, mass, battery capacity** |
| Full build configuration | **Any photograph of the device** |
| That it exists and ships | **Whether it is sold under a different name in China** |

## Partitions

16 MB dual-OTA, **identical to the X4 Pro**: `nvs` `0x9000` · `otadata` `0xE000` ·
`app0` `0x10000` · `app1` `0x7F0000` · `spiffs` `0xFD0000` · `coredump` `0xFE4000`.

## Development

```ini
[env:x4c]
extends = base
board = esp32-s3-devkitc1-n16r8
board_build.mcu = esp32s3
build_flags =
  ${base.build_flags}
  -DBOARD_HAS_PSRAM
  -DUSE_BLOCK_DEVICE_INTERFACE=1   ; SD is 1-bit SDMMC; SdFat needs the block-device interface
  -DFREEINK_DEVICE_X4CLASSIC=1
```
Verbatim from `platformio.sample.ini`. `reported-working`.

Auto-enables `FREEINK_DRIVER_SSD1677`, `FREEINK_DRIVER_UC8179`,
`FREEINK_DRIVER_UC8279_X4`, `FREEINK_CAP_RTC`, `FREEINK_BATTERY_I2C_GAUGE`,
`FREEINK_SD_SDMMC`. Leaves `FREEINK_CAP_TOUCH` and `FREEINK_CAP_FRONTLIGHT` **off**.

Bricking risks, unlock procedure and toolchain are as the
[X4 Pro](../x4-pro/development.md) — same SoC, same flash size, same ecosystem —
**except** that the panel-controller selection cannot self-correct.

## Sources

| ID | What | URL | Retrieved | Establishes |
|---|---|---|---|---|
| XC01 | `BoardConfig.h` `XTEINK_X4_CLASSIC` L1615–1706 | <https://github.com/Free-Ink/freeink-sdk/blob/24003795381a6c23630a26472ae3b06550333e71/libs/hardware/BoardConfig/include/BoardConfig.h#L1615-L1706> | 2026-09-04 | Full pinout, confidence levels, RE offsets |
| XC02 | `docs/xteink-x4c-support.md` | <https://github.com/Free-Ink/freeink-sdk/blob/24003795381a6c23630a26472ae3b06550333e71/docs/xteink-x4c-support.md> | 2026-09-04 | Board identity, NVS mapping, peripherals, partitions |
| XC03 | `XteinkDetect.cpp` `applyXteinkDisplayController()` | <https://github.com/Free-Ink/freeink-sdk/blob/24003795381a6c23630a26472ae3b06550333e71/libs/hardware/XteinkDetect/src/XteinkDetect.cpp> | 2026-09-04 | The no-MISO special case and NVS mapping |
| XC04 | `platformio.sample.ini` `[env:x4c]` | same commit | 2026-09-04 | Build flags |
| XC05 | `x4-classic` collection | <https://www.xteink.com/collections/x4-classic/products.json?limit=250> | 2026-09-04 | **The collection exists and contains no device** |
| XC06 | "Did we just spot a new X4 model?" | <https://old.reddit.com/r/XTEINK/comments/1ud0d9c/> | 2026-09-04 | Community identified it 2026-06-22, ~1 month pre-launch |

## Gaps

**Everything commercial.** No price, no listing, no photograph, no dimensions, no
mass, no battery capacity, no availability date, no regional name. The
**hardware** is better documented than the **product** — an unusual inversion, and
a direct consequence of the only source being a firmware dump.

Open technical questions: **GPIO4's role**; charge-STAT polarity; panel
orientation; whether the `R2` in `ESP32S3_X4R2_CLA` implies an R1 that shipped.

## See also

[Family index](../README.md) · [X4 Pro](../x4-pro/README.md) — the board this is
derived from · [X4](../x4/README.md) — where the four bottom keys come from

---

# ROUND 2 — appended 2026-09-11. The X4 Classic launched.

> **Everything above this line is the 2026-09-04 snapshot and has not been
> altered.** Its headline — *"Not listed for international sale… contains no
> device"* — was **correct on 2026-09-04 and is now superseded**. This section is
> a fresh retrieval dated **2026-09-11** (the working session's clock; the task
> brief said 2026-09-07, and the divergence is recorded in
> [`research-log.md`](research-log.md) §0 because every `published_at` below is
> read from the vendor's own API and must be trusted over either).

## The answer, in one table

| Field | Value | Evidence |
|---|---|---|
| Marketed name | **XTEINK X4 Classic (X4 V2) Pocket eReader** | **[VENDOR]** product title, verbatim |
| **"X4 V2" is not a separate SKU** | The vendor writes the alias **into its own product titles and FAQ** | **[VENDOR]** — see below |
| Shopify product id | `9693091135729` | **[VENDOR]** `/products.json` |
| Handle | `xteink-x4-classic-pocket-ereader` | **[VENDOR]** |
| **`created_at`** | **2026-08-03 05:06:01 −0700** — drafted a month before launch | **[VENDOR]** |
| **`published_at`** | **2026-09-06 19:57:20 −0700** | **[VENDOR]** |
| **Price** | **US$79.00** (`compare_at_price` 89.00) | **[VENDOR]** |
| SKUs | `X4Classic-gray`, `X4Classic-black` | **[VENDOR]** variant `sku` |
| Bundle SKUs | `X4CW+BW`, `X4CB+BW`, `X4CW+BB`, `X4CB+BB` — reader + charging base, **US$95.00** (`compare_at` 105.00), added `2026-09-05` | **[VENDOR]** |
| Colours | **Mist Gray**, **Space Black** | **[VENDOR]** |
| Ship weight | `grams: 250` (packaged, not device mass) | **[VENDOR]** |
| Availability | `available: true` on all six variants at retrieval | **[VENDOR]** |
| FCC ID | **`2BTR9-X4C`**, filed and granted **2026-07-20** | **[REG]** |

**The vendor's own accessory titles settle the naming question.** Four accessories
published 2026-09-06 are named, verbatim:

- `XTEINK X4 Classic (X4 V2) Tempered Glass Screen Protector` — SKUs `X4C-Tempered-{1,2,3}`
- `XTEINK X4 Classic (X4 V2) Matte Screen Protector` — SKUs `X4C-Matte-{2,4,6}`
- `XTEINK X4 Classic (X4 V2) Protective Case` — SKUs `X4C-ProtectiveC-{MW,MG}`
- `XTEINK X4 Classic (X4 V2) Magnetic Case - Multiple Colors` — SKUs `X4C-MagneticC-{FG,MG,BP,RR,SB,CG}`

and the product-page FAQ uses "X4 V2" in running prose for the same device
(*"The **X4 V2** features a built-in magnetic ring on the back, with a slightly
different position from the first-generation X4"*). **The "X4 v2" that the
2026-09-04 sweep flagged as a vendor-confirmed September 2026 product is this
device.** It is not a distinct model, and no distinct model exists between the X4
and the X4 Pro. See [`product-history-and-family.md`](product-history-and-family.md).

## Vendor specification block, retrieved 2026-09-11

Read from the rendered product page's `DETAILS + DIMENSIONS` section, not from the
`body_html` (which is empty for this product).

| Vendor field | Vendor value | Comment |
|---|---|---|
| Display | **4.3 inch** | The firmware and every other Xteink document say **4.26″**. Vendor rounding; see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) §R2-3 |
| Resolution | **219 PPI** | Mislabelled — 219 PPI is a *density*, not a resolution. It is arithmetically consistent with 800×480 on 4.26″ |
| **Dimensions** | **114 × 69 × 4.9 mm** | First dimensional figure ever recorded for this device |
| **Weight** | **68 g** | First mass figure. Lighter than the X3 (55 g is the X3; the X4 is ~74–80 g) |
| Storage | **bundled 16 GB microSD**, expansion to 256 GB | No internal user storage; matches SDMMC-only design |
| Connectivity | **Wi-Fi 2.4 GHz & Bluetooth** | Corroborated by the FCC grant (2412–2462 MHz, DTS) and by BLE power in the RF-exposure exhibit |
| **Ports** | **Pogo Pin** | **No USB-C.** Resolves the "Charging: unknown" gap |
| **Battery** | **920 mAh** | First capacity figure |
| Supported formats | EPUB, TXT / BMP / fonts BIN, XTF | The same page's FAQ says *"TXT, EPUB, MOBI, PDF, XTCH, XTC, XTCZ"* — **the page contradicts itself**; recorded, not resolved |
| Front light | **No** | Confirms the firmware. Refutes the 2026-06-22 community guess |
| Touchscreen | **No** | Confirms the firmware |

**Box contents** (vendor): 1 × X4 Classic reader · 1 × quick-start guide ·
1 × microSD card · 1 × matte screen protector · 2 × adhesive metal ring ·
1 × magnetic charging adapter.

### Two vendor claims that are hardware findings

1. **"Shake-to-Flip lets you turn pages by gently shaking the device."** This is
   independent, vendor-side corroboration of the **QMI8658 IMU at 0x6B** that the
   FreeInk profile lists — previously a single-source claim. A buttons-only reader
   has no other reason to carry a six-axis IMU.
   → [`qst/qmi8658a`](../../../components/qst/qmi8658a/README.md)
2. **"built-in magnetic ring on the back, with a slightly different position from
   the first-generation X4."** The magnet is *in the device*, not in the case, and
   its position moved relative to the X4. Visible as an oval outline in the FCC
   external photographs of the sibling X4 Light.

## Regulatory record — the second custodian this record needed

`ESP32S3_X4R2_CLA` and the FreeInk profile were, until now, the only evidence this
device existed. There is now a US federal one.

| Field | Value |
|---|---|
| **FCC ID** | **`2BTR9-X4C`** |
| Grantee code / product code | `2BTR9` / `X4C` |
| **Legal applicant** | **Shenzhen Xiaohu Xingtong Technology Co., Ltd.** (深圳小狐星曈科技 — note the **曈** spelling) |
| Applicant address | Room 1209, Yichuang International Center, Building 2B, No. 8 Golf Avenue, Guangpei Community, Guanlan Street, Longhua District, Shenzhen |
| Applicant FRN | `0037772233` |
| Responsible party | Chen Chu, `chuchen@xteink.cn` |
| Related domain on the filing | **`xteink.cn`** — the domain the 2026-09-04 sweep found unreachable at the apex but referenced inside X4 stock firmware (`bofi.xteink.cn`). **The filing confirms it is the company's** |
| Test lab | Shenzhen BKC Testing Co., Ltd. |
| Application / final-action date | **2026-07-20** |
| Equipment class | DTS — Digital Transmission System |
| Frequency range | **2412–2462 MHz** (2.4 GHz only; no 5 GHz, consistent with ESP32-S3) |
| BLE conducted peak power | **−0.87 dBm** (ch 0), −1.42 dBm (ch 19) — from the RF-exposure exhibit |
| **Antenna** | **`KH3216-A35`**, Shenzhen Jinhangbiao Electronics Co., Ltd. — 3216 chip antenna, peak gain **2.30 dBi**, VSWR ≤ 2.0, 50 Ω, omnidirectional, efficiency 69–71.2 % → [`generic/kh3216-a35-chip-antenna`](../../../components/generic/kh3216-a35-chip-antenna/README.md) |

### What the FCC filing does *not* yet give you, and exactly when it will

The applicant filed a short-term confidentiality request. Four exhibits exist in
the FCC's system but are served as **metadata only**:

| Exhibit | Size | **Public from** |
|---|---|---|
| **Internal Photos** | 4.5 MB | **2027-01-16** |
| External Photos | 825.3 KB | 2027-01-16 |
| Users Manual | 2.9 MB | 2027-01-16 |
| Test Setup Photos | 305.6 KB | 2027-01-16 |
| Block Diagram · Schematics · Operational Description | 55.2 KB / 540.4 KB / 73 KB | **never** — long-term confidentiality, no release date |

**A PCB teardown of this device is dated, not hypothetical: 2027-01-16.** That is
the cheapest route to resolving the remaining open questions below, and it needs
no hardware. A community member is already asking for PCB photographs for a
specific reason ([r/xteinkereader `1wcgqub`](https://old.reddit.com/r/xteinkereader/comments/1wcgqub/),
2026-09-10) — whether BM8563 `CLKOUT` reaches ESP32-S3 `GPIO15`/`XTAL_32K_P`,
which would allow a low-power always-on BLE mode. Nobody had opened one at that
date.

Retained exhibits: [`artifacts/certification/`](artifacts/certification/README.md).

## `R2` in `ESP32S3_X4R2_CLA` — resolved as far as the evidence allows

The 2026-09-04 record flagged this as "implying an earlier revision 1 nobody has
documented". New evidence changes the reading:

1. An **X4 Pro** stock-firmware dump taken from a physical device on 2026-09-06
   contains **all four board tags in one binary**: `ESP32S3_X4_TL`,
   `ESP32S3_X4_TL_SSD1677`, **`ESP32S3_X4_CLA`** and **`ESP32S3_X4R2_CLA`**
   ([`kycube/x4pro-emu` `docs/device/partitions.md`](https://github.com/kycube/x4pro-emu/blob/bf4b86ae0471012d4d07c0bb3042f3f561c9c302/docs/device/partitions.md)).
   The tags are entries in **one shared vendor codebase compiled for every S3
   board**, not a per-unit revision stamp. A string's presence therefore says
   nothing about the unit it was dumped from.
2. The **FCC grant is a single original-equipment filing**, `2BTR9-X4C`,
   2026-07-20, with **no Class II permissive change** and no earlier X4C
   application under grantee `2BTR9`. If an `R1` had been *sold in the US*, it
   would need its own grant. **There is no such grant.**
3. The vendor's own marketing calls this device the **second** version of the X4
   ("X4 V2"), and the X4 has its own FCC ID (`2BTR9-XTEINKX4`, 2026-01-05). The
   most economical reading of `X4R2` is **"X4, revision 2" — i.e. the X4C *is* the
   R2, and the R1 is the original C3 X4**, not an unreleased X4C.

**Verdict: `not-resolved, strongly constrained.** Reading (3) is consistent with
every piece of evidence and requires no unobserved device. An engineering-sample
X4C R1 that never reached retail cannot be excluded and never will be from public
sources. **What would settle it:** the `SCH`/`BLOCK` exhibits (permanently
confidential), an internal photograph showing a silkscreened revision (2027-01-16),
or a second stock dump from a *known* X4C carrying a different revision string.
The earlier statement that `R2` "implies an earlier revision 1 nobody has
documented" is **narrowed**: it implies a revision 1, and revision 1 is most
likely the plain X4.

## Corrections to the specification table above

| Field above | Was | Now | Source |
|---|---|---|---|
| Availability | "Not listed for international sale" | **Listed, in stock, US$79** | **[VENDOR]** |
| Charging | unknown | **Pogo pin, 4-contact magnetic** | **[VENDOR]** + FCC external photos of the sibling X4L |
| Dimensions / mass / battery | unknown | **114 × 69 × 4.9 mm · 68 g · 920 mAh** | **[VENDOR]** |
| Stock firmware analysed | `xteink_app` v7.0.11 | v7.0.11 remains the only **X4C** version seen. The **X4 Pro** desk unit shipped **7.2.4** (2026-08-14) and a **7.5.4** analysis exists. No X4C-specific number is corroborated | **[DUMP]**, third-party |
| `displaySpiHz` | 20 MHz | **10 MHz** — FreeInk changed every Xteink profile to a shared `XTEINK_DISPLAY_SPI_HZ = 10000000u` in commit `39606d5a` (2026-09-09, *"Fix e-ink display buffer tracking and optimize SPI writes"*) | **[SDK]** |

## New round-2 documents in this record

| File | What it adds |
|---|---|
| [`research-log.md`](research-log.md) | Every query, endpoint, UA and failure of the 2026-09-11 pass |
| [`commands.md`](commands.md) | The Shopify, fccid.io, poppler and GitHub commands, with status labels |
| [`product-history-and-family.md`](product-history-and-family.md) | The dated X4C timeline from first sighting to launch, and the "X4 v2" naming history |
| [`community.md`](community.md) | Owner reports, the launch-week thread census, and the pogo/USB-C controversy |
| [`projects-and-community.md`](projects-and-community.md) | Which firmware projects support the X4C, at which commit |
| [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) | X4C against X4, X4 Pro, X3 and the Boox Picco |
| [`performance.md`](performance.md) | What is and is not measured — mostly the latter, stated plainly |
| [`resources-and-conflicts.md`](resources-and-conflicts.md) | GPIO/bus/rail ownership and the realistic concurrent-use cases |
| [`examples/`](examples/catalog.json) | Example catalogue, search log and selection |
| [`media/manifest.json`](media/manifest.json) | Image provenance |
| [`artifacts/certification/`](artifacts/certification/README.md) | The five public FCC exhibits, hashed |
