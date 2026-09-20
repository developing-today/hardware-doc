# Xteink X3

> SKUs `xteink-x3-white-1` (Mist Gray) and `xteink-x3-black-1` (Space Black) ·
> **$69.00**, both in stock 2026-09-04 · published **2025-12-11**, shipping from
> **2026-02-05** · research retrieval date **2026-09-04**.

**The best-documented Xteink device**, because it is the only one with public
teardowns — two of them, independent, one in English and one in Chinese with a
hand-drawn schematic.

## Identity and variants

| Field | Value | Evidence |
|---|---|---|
| Marketed name | **Xteink X3 Pocket eReader** | **[VENDOR]** handle `xteink-x3` |
| Chinese name | **阅星瞳 X3** / **阅星曈 X3** — *both spellings in live use* | **[CN]** `sunwoods/Xteink-X3` vs `zocs/eink-quick-flasher` |
| SKUs | `xteink-x3-white-1` (Mist Gray), `xteink-x3-black-1` (Space Black) | **[VENDOR]** |
| Shipping weight | 58 g packaged | **[VENDOR]** `grams: 58` |
| Device mass | **55 g** | **[VENDOR]** launch announcement |
| FreeInk profiles | `XTEINK_X3` (UC8253) and `XTEINK_X3_UC8279` (UC8279d) | **[SDK]** `BoardConfig.h:881–947` |
| Build flag | `-DFREEINK_DEVICE_X3=1` — links **both** drivers | **[SDK]** |
| Lifecycle | **Current.** Both colours in stock | **[VENDOR]** |

### Panel-controller variants

| Controller | Batch | Note |
|---|---|---|
| **UC8253** | Original | The shipping default |
| **UC8279d** ("d_B" silicon) | **From ~July 2026** | *"Newer X3 production units (Xteink heads-up, July 2026)"* — the vendor told the community |

Same board, same glass, same pinout — **only the controller changes**. Selected at
boot by fingerprint. **[SDK]** `docs/xteink-x3-uc8279-support.md:3–7`.

**The UC8279d variant has never been on a bench.** The SDK is explicit:
*"Everything below is written from the UC8279d_B 0.1 datasheet (Dec 2025) and is
**Pending hardware validation** — no UC8279 X3 unit has been on the bench yet."*

## What it is and visual identification

The smallest Xteink: a **3.7-inch, 55 g** pocket reader with **six buttons** (four
front, two side) plus power, a **glass back** with embedded magnets, and a
**magnetic pogo-pin charging connector**. No touchscreen, no frontlight.

Externally distinguishable from the X4 by size alone — the X3 is materially
smaller and lighter (55 g vs 80 g) despite having a **higher-resolution** screen.

## Product history

| Date | Event | Evidence |
|---|---|---|
| 2025-12-08 | Product record created | **[VENDOR]** |
| 2025-12-09 | **Announced** — *"builds on everything we learned from building the X4"* | **[COMM]** [r/xteinkereader `1pi6ezd`](https://old.reddit.com/r/xteinkereader/comments/1pi6ezd/) |
| 2025-12-11 | **Pre-orders open.** *"Super Early Bird units are non-refundable"* | **[COMM]** [`1pjw3ay`](https://old.reddit.com/r/xteinkereader/comments/1pjw3ay/), **[VENDOR]** |
| **2026-02-05** | Shipping begins | **[COMM]** both announcements |
| 2026-03-25 | Screen protectors listed | **[VENDOR]** |
| 2026-04-01 | Magnetic case, 6 colours | **[VENDOR]** |
| 2026-04-28 | "X3 vs X4 - actual experience comparison", 412 pts | **[COMM]** [`1syav96`](https://old.reddit.com/r/xteinkereader/comments/1syav96/) |
| 2026-05-15 / 06-19 | Pogo cable and adapter listed separately | **[VENDOR]** |
| **2026-07-01** | **First public teardown** (13 photos) | **[TD]** [r/xteinkereader `1uksv6s`](https://old.reddit.com/r/xteinkereader/comments/1uksv6s/) |
| ~2026-07 | Vendor warns of the **UC8279d** panel switch | **[SDK]** |
| 2026-08-07 | CrossPoint 1.5 *"DOES support the new x3 display variants"* | **[COMM]** [`1vhvtdd`](https://old.reddit.com/r/xteinkereader/comments/1vhvtdd/) |
| 2026-09-04 | $69, both colours in stock | **[VENDOR]** |

## Key specifications

| Item | Value | Component | Evidence |
|---|---|---|---|
| SoC | **ESP32-C3**, no PSRAM | [`espressif/esp32-c3`](../../../components/espressif/esp32-c3/README.md) | **[SDK]**, **[TD]** ×2 |
| Flash | **Puya 128 Mbit (16 MB)** SPI NOR | [`unidentified/…/spi-nor-flash-128mbit-puya`](../../../components/unidentified/xteink-x3-x4/spi-nor-flash-128mbit-puya/README.md) | **[TD]** EN + **[CN]** |
| Display | **792 × 528**, 3.7″, **~257 PPI** | — | **[SDK]** `:886–887`, **[VENDOR]** *"250+ PPI"* |
| Controller | **UC8253**, or **UC8279d** on newer batches | [`ultrachip/uc8253`](../../../components/ultrachip/uc8253/README.md) · [`ultrachip/uc8279`](../../../components/ultrachip/uc8279/README.md) | **[SDK]** |
| **Fuel gauge** | **TI BQ27220** @ I²C **0x55** | [`texas-instruments/bq27220`](../../../components/texas-instruments/bq27220/README.md) | **[SDK]**, **[CN]** BOM |
| **RTC** | **DS-series** @ I²C **0x68** — **see conflict** | [`unidentified/…/rtc-ds-series`](../../../components/unidentified/xteink-x3-x4/rtc-ds-series/README.md) | **[SDK]** DS3231 vs **[TD]** "DS1307" |
| **IMU** | **QMI8658** 6-axis @ I²C **0x6B** (alt 0x6A), `WHO_AM_I = 0x05` | [`qst/qmi8658a`](../../../components/qst/qmi8658a/README.md) | **[SDK]**, **[CN]** BOM |
| **NFC** | **ISO/IEC 14443A tag** | [`unidentified/…/nfc-tag-iso14443a`](../../../components/unidentified/xteink-x3-x4/nfc-tag-iso14443a/README.md) | **[CN]** BOM + **[VENDOR]** announcement |
| Charger | **TP4056-class** battery-management IC | [`unidentified/…/battery-charger-tp4056-class`](../../../components/unidentified/xteink-x3-x4/battery-charger-tp4056-class/README.md) | **[CN]** BOM |
| **Battery** | **650 mAh**, glued to the back cover | [`generic/lipo-102035`](../../../components/generic/) (class only) | **[TD]** photo caption |
| Storage | microSD over **SPI shared with the display**; **power enable GPIO13** | — | **[SDK]** |
| Charging | **Magnetic pogo pins**, magnets glued to the back cover | — | **[TD]**, **[VENDOR]** |
| Touch / frontlight | **none** | — | **[SDK]** |
| Radios | Wi-Fi + BLE (ESP32-C3) | — | inferred |

**The X3 has more silicon than the X4 and the X4 Pro in three respects**: it is the
only Xteink with **NFC**, one of two with an **IMU**, and the only one with a
**BQ27220** (a proper TI impedance-track gauge rather than the Pro's CW2017 or the
X4's bare ADC).

### Resolution sanity check

√(792² + 528²) = 951.7 px diagonal ÷ 3.7″ = **257 PPI**, which agrees with the
vendor's *"over 250 PPI"* and is the **highest pixel density in the family**
(the 4.26″ models are ~219). Two independent figures, arithmetically consistent.

## Architecture and components

```
ESP32-C3 ── SPI ──┬── UC8253 │ UC8279d ── 792×528 glass
                  │     SCLK 8 / MOSI 10 / CS 21 / DC 4 / RST 5 / BUSY 6
                  └── microSD  (same bus; MISO 7, CS 12, rail = GPIO13 active-HIGH)
         ── I²C SDA 20 / SCL 0 @400 kHz ─┬── BQ27220 fuel gauge   0x55
                                         ├── DS-series RTC        0x68
                                         └── QMI8658 IMU          0x6B
         ├─ ADC ladder ── GPIO1 (Back/Confirm/Left/Right) + GPIO2 (Up/Down)
         ├─ GPIO3 ─────── Power button
         ├─ GPIO0 ─────── Battery voltage ADC (÷2)
         └─ NFC tag ───── passive, ISO 14443A, not on any host bus
```

**The I²C bus is the X3/X4 discriminator.** `XteinkDetect` probes SDA20/SCL0 for
0x55, 0x68 and 0x6B; finding them means X3, finding nothing means X4. One C3
binary drives both devices.

Full tables: [`pinouts-and-buses.md`](pinouts-and-buses.md).

## Distinctive strengths

- **Highest PPI in the family** (~257) and **lightest** (55 g).
- **The most complete sensor set**: real fuel gauge, RTC, IMU, NFC.
- **Motion-based page turning** via the gyroscope — a genuine feature the others
  lack.
- **SD card can be powered down for sleep** (GPIO13), unlike the X4.
- **Two independent public teardowns**, including a schematic sketch.
- **Cheapest currently-purchasable Xteink** at $69.

## Shortcomings and constraints

- **Pogo-pin charging**, like the X4 Pro. No USB-C charge path.
- **Glass back that cracks.** An owner reported *"My glass cracked a bit on the
  rear side"* and asked which models have metal backing — **unanswered**
  ([r/xteinkereader `1w56phf`](https://old.reddit.com/r/xteinkereader/comments/1w56phf/), 2026-09-02).
- **Buttons feel worse than the X4's**: *"The X3's buttons are somewhat mushy and
  quieter"* — [r/xteinkereader `1syav96`](https://old.reddit.com/r/xteinkereader/comments/1syav96/).
- **No PSRAM**, and the X3 is the device where **OTA out-of-memory was actually
  observed** — CrossPoint stopped using GitHub releases because of it.
- **The UC8279d variant is unvalidated on hardware** and currently has no
  grayscale and probably a full flash on every page turn. See
  [`features/display.md`](features/display.md).
- **Vendor marketing for this device is false** — see below.

### The vendor's own product page is wrong about this device

The `xteink.com` X3 listing advertises:

> "This tool includes **adjustable warm light settings**. You can transition to
> bedtime stories with total visual comfort…"
> "**Cloud sync** keeps your notes organized across all of your many mobile
> devices."

**The X3 has no frontlight** (`NO_FRONTLIGHT` in the board profile; no frontlight
in either teardown; the X4 Pro is the only Xteink with one). The copy is
AI/SEO-generated boilerplate. **No claim from vendor prose is used as evidence
anywhere in this tree** — this is why.

## Performance summary

| Figure | Value | Status |
|---|---|---|
| Display SPI | **20 MHz** = UC8253 datasheet max (`TSCYCW`) | **[SDK]**, in-spec |
| Prior fork (Witch Reader) | 16 MHz | ~25 % slower on plane writes |
| Battery | **650 mAh** | **[TD]** |
| Runtime | **unknown** | — |

No power measurement exists. The teardown author explicitly set out to attach a
**Nordic Power Profiler Kit II** *"to see if I can make any power optimizations to
crosspoint firmware"* — **and never posted results.**

## Pricing and availability

**$69.00**, both colours, in stock 2026-09-04. Full accessory pricing and the $16
used-market anecdote: [`market-and-pricing.md`](market-and-pricing.md).

## Competitors, equivalents and clones

See [`../x4-pro/comparisons-and-recommendations.md`](../x4-pro/comparisons-and-recommendations.md)
for the family and platform comparison. Within the family the X3 is the value
pick: it costs the same as the (delisted) X4, has a sharper screen and far more
sensors, and gives up USB-C and button feel.

## When to use / when not to use

**Use it** for the sharpest, lightest pocket reader in the family, or if you want
the IMU/NFC/RTC/gauge for a project. **Do not use it** if you need USB-C charging,
if you want the best button feel, or if your firmware is memory-hungry.

## Images and teardown/PCB views

**Two independent teardowns, both archived.** See [`media.md`](media.md).

## Common tasks / How do I…?

| Task | Guide |
|---|---|
| Drive the display; handle UC8253 vs UC8279d | [`features/display.md`](features/display.md) |
| Read the 6-button ADC ladder | [`../x4/features/buttons.md`](../x4/features/buttons.md) (identical) |
| Read the fuel gauge | [`features/battery-and-power.md`](features/battery-and-power.md) |
| Read the IMU / motion page turn | [`features/imu.md`](features/imu.md) |
| Read the RTC | [`features/rtc.md`](features/rtc.md) |
| Use the SD card and power it down for sleep | [`features/storage.md`](features/storage.md) |
| Do anything with the NFC tag | [`features/nfc.md`](features/nfc.md) |
| Build and flash | [`development.md`](development.md) |
| Dump / restore stock firmware | [`factory-firmware.md`](factory-firmware.md) |

## Documentation map

[`pinouts-and-buses.md`](pinouts-and-buses.md) ·
[`development.md`](development.md) ·
[`factory-firmware.md`](factory-firmware.md) ·
[`sources.md`](sources.md) ·
[`coverage.md`](coverage.md) ·
[`compatibility-and-status.md`](compatibility-and-status.md) ·
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) ·
[`market-and-pricing.md`](market-and-pricing.md) ·
[`media.md`](media.md).
Family-wide [research log](../x4-pro/research-log.md) and
[command ledger](../x4-pro/commands.md).

## Artifact layout

```
artifacts/teardown/
├── imgur-2026-07-01/   → archived — 13 photos, English captions, manifest.json
└── sunwoods-cn/        → archived — 10 photos incl. a hand-drawn SCHEMATIC + upstream README
```

Both carry `*.ARCHIVED.md` placeholders with per-file SHA-256, sizes and
reacquisition instructions.

## Known conflicts and unresolved identities

**The RTC.** The FreeInk SDK drives a **DS3231**; the English teardown captions the
chip **"DS1307"**; the Chinese BOM says only **"DS-series RTC"**. All three are at
address 0x68. Unresolved — see [`gaps-and-conflicts.md`](gaps-and-conflicts.md).
The component record is filed under `unidentified/` for exactly this reason.

---

## Round 2 — appended 2026-09-11: the X3 has an FCC teardown, and it is public

**No line above was altered.**

| Field | Value |
|---|---|
| **FCC ID** | **`2BTR9-XTEINKX3`** |
| Applicant | **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**, Longhua District, Shenzhen, FRN `0037772233` |
| Granted | **2025-12-26** — sixteen days before the store listing of 2025-12-11… *no*: the store listing **preceded** the grant. Recorded as-is; both dates come from their own primary sources |
| Equipment class | DTS, **2412–2462 MHz** |
| Source | <https://fccid.io/2BTR9-XTEINKX3> |

### The important part: the confidentiality has already expired

| Exhibit | Public from |
|---|---|
| **Internal Photos (849.3 KB)** | **2026-06-24 — already public** |
| **Users Manual (1.3 MB)** | **2026-06-24 — already public** |
| External Photos, Label, Test Setup Photos, 3 test reports, RF exposure | 2025-12-26 |
| Block Diagram · Schematics · Operational Description | **permanently confidential** |

**This is a third teardown of the X3**, alongside the two community teardowns
already archived in this record — and it is the only one produced under a
regulatory obligation to photograph the board as shipped.

Retained: `artifacts/certification/2BTR9-XTEINKX3-internal-photos.pdf`,
869,708 B, SHA-256
`b3affd56115e9c3e49428f9727ba194c0eec6705ddd0b039fd9b4ce28b430a45`,
**16 embedded images**, from
<https://fccid.io/2BTR9-XTEINKX3/Internal-Photos/Internal-Photos-8932226.pdf>,
retrieved 2026-09-11 (UA `WhatsApp/2.23.20.0`; a desktop-Chrome UA is served
403). Validated `%PDF`.

**It has not been read in detail by this pass.** It is retained, hashed and
cited so the next session can open it against
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) — in particular against
**conflict #1, the unresolved RTC part** (`DS3231` per firmware vs `DS1307` per a
teardown caption vs "DS-series" per a Chinese BOM). **A regulatory photograph of
the RTC's top marking would settle a conflict that has stood since the first
sweep**, and it is sitting in this repository unread.

`Users Manual` at <https://fccid.io/2BTR9-XTEINKX3/User-Manual/Users-Manual-8932229.pdf>
is also public and **was not fetched** — it is the vendor's own manual, which
would be a far better source than the SEO-generated store prose this record
correctly distrusts.
