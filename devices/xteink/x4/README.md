# Xteink X4

> **Delisted from the vendor store as of 2026-09-04** — accessories only, and
> every X4 accessory is sold out. Was $69. ESP32-C3, 4.26″ 800×480.
> Research retrieval date **2026-09-04**.

## Identity and variants

| Field | Value | Evidence |
|---|---|---|
| Marketed name | **Xteink X4** (community nickname "X4 mini" — **not a SKU**) | **[VENDOR]**, **[COMM]** |
| Chinese name | **星瞳 X4** ("Star Pupil") | **[COMM]** [r/ereader `1n5kmpc`](https://old.reddit.com/r/ereader/comments/1n5kmpc/) |
| FreeInk profile | `BoardConfig::XTEINK_X4`, name string `xteink_x4` | **[SDK]** `BoardConfig.h:844–874` |
| Build flag | `-DFREEINK_DEVICE_X4=1` | **[SDK]** |
| Board tag in a sibling dump | `ESP32S3_X4_TL` appears in the **X4 Pro's** app0 — that is an *S3* variant string and is **not** this C3 device | **[SDK]** |
| Colours | at least **Space Black** and a white/grey; the magnetic case shipped in 7 colours | **[VENDOR]** accessory variants |
| Lifecycle | Launched ~Sept 2025 · **delisted before 2026-09-04** | **[VENDOR]** |

### Physical (community-measured, single source)

| Property | Value | Evidence |
|---|---|---|
| Dimensions | ≈ **114 × 70 × 7 mm** (4.5 × 2.75 × 0.25 in) | **[COMM]** [r/Ultralight `1r1jfny`](https://old.reddit.com/r/Ultralight/comments/1r1jfny/), 2026-02-11 |
| Mass | **80 g** including screen protector | same |
| Display | **220 PPI** | same |
| Controls | **4 front-facing buttons + 3 on the right side** | same |

The vendor calls it a **4.3-inch** model (founder, [r/ereader `1o2203h`](https://old.reddit.com/r/ereader/comments/1o2203h/));
the panel is a 4.26″ class part. 800×480 across 4.26″ diagonal = **219 PPI**,
which agrees with the owner's 220 — the two independent figures corroborate.

**Single-source caveat:** the dimensions and mass come from **one** owner post.
No vendor spec sheet was found.

## What it is and visual identification

The original Xteink: a pocket e-reader roughly the size of a large phone, with
**four buttons on the front face and three on the right edge**, a **USB-C port**,
and a magnetic back designed to stick to the back of a phone (MagSafe-style).
It has **no touchscreen, no frontlight and no RTC**.

The MagSafe-on-your-phone use case is how it was marketed and how owners describe
it: *"meant to be attached on the backside of your phone using MagSafe so you can
just flip your phone around and just read"*
([r/eink `1sba4am`](https://old.reddit.com/r/eink/comments/1sba4am/)).

## Product history, family and culture

| Date | Event | Evidence |
|---|---|---|
| 2025-09-01 | First English-language impressions post, titled "Xteink Star Pupil X4 (星瞳X4)" | **[COMM]** [r/ereader `1n5kmpc`](https://old.reddit.com/r/ereader/comments/1n5kmpc/) |
| 2025-10-09 | Founder "Crusoe" introduces the company on Reddit, 1,477 pts, describing the X4 as their 4.3-inch model | **[COMM]** [r/ereader `1o2203h`](https://old.reddit.com/r/ereader/comments/1o2203h/) |
| 2025-10-21/23 | X4 magnetic case and tempered-glass protector listed | **[VENDOR]** |
| 2025-12-09/11 | X3 announced as the smaller successor — *"builds on everything we learned from building the X4"* | **[COMM]** [`1pi6ezd`](https://old.reddit.com/r/xteinkereader/comments/1pi6ezd/) |
| 2025-12 | CrossPoint custom firmware for the X4 appears | **[COMM]** community digest |
| 2026-01-21 | X4 protective case listed | **[VENDOR]** |
| 2026-07-08 | X4 matte screen protector listed — **the last X4 accessory added** | **[VENDOR]** |
| 2026-07-21 | X4 Pro launches | **[VENDOR]** |
| **2026-09-04** | **X4 device absent from the catalogue. All 4 X4 accessory SKUs sold out** | **[VENDOR]** |

**The X4 is the device that created the ecosystem.** Nearly every firmware project
in the family started as "firmware for the Xteink X4" and grew to cover the X3 and
the S3 devices afterwards.

## Key specifications

| Item | Value | Component record | Evidence |
|---|---|---|---|
| SoC | **ESP32-C3** (RISC-V), 16 MB external flash, **no PSRAM** | [`espressif/esp32-c3`](../../../components/espressif/esp32-c3/README.md) | **[SDK]**, **[DUMP]** chip-id 5, **[TD]** X3 sibling |
| Flash | **128 Mbit (16 MB)** SPI NOR, **Puya** | [`unidentified/xteink-x3-x4/spi-nor-flash-128mbit-puya`](../../../components/unidentified/xteink-x3-x4/spi-nor-flash-128mbit-puya/README.md) | **[TD]** (X3 board; assumed shared) |
| Display | 800×480 mono e-ink, 4.26″, ~219 PPI | — | **[SDK]** `:848–849` |
| Controller | **SSD1677**, or **UC8179**/**UC8279** on newer batches | [`solomon-systech/ssd1677`](../../../components/solomon-systech/ssd1677/README.md) · [`ultrachip/uc8179`](../../../components/ultrachip/uc8179/README.md) · [`ultrachip/uc8279`](../../../components/ultrachip/uc8279/README.md) | **[SDK]** |
| Touch | **none** (`NO_TOUCH`) | — | **[SDK]** |
| Frontlight | **none** (`NO_FRONTLIGHT`) | — | **[SDK]** |
| **RTC** | **NONE** — `sensors = NO_SENSORS` | — | **[SDK]** `:866` |
| **Fuel gauge** | **NONE** — `NO_GAUGE`; battery read by **ADC on GPIO0**, ×2.0 divider | — | **[SDK]** `:854–856, 864` |
| Storage | microSD over **SPI, sharing the display bus** | — | **[SDK]** `:852` |
| USB | USB-C, ESP32-C3 USB-serial-JTAG; `usbDetect = GPIO20` | — | **[SDK]** `:855`… see note |
| Charging | **USB-C** — unlike the X3 and X4 Pro | — | **[COMM]** |
| Battery latch | **GPIO13** gates the battery MOSFET | — | **[SDK]** `:868–874` |
| IMU / NFC | **none** | — | **[SDK]** |
| Radios | Wi-Fi + BLE (ESP32-C3 integrated) | — | inferred |

**The X4 is the most stripped-down member of the family.** No RTC, no fuel gauge,
no IMU, no NFC, no touch, no frontlight — the X3, which is *cheaper*, has four of
those six.

## Architecture and components

```
ESP32-C3 ── SPI ──┬── EPD controller (SSD1677│UC8179│UC8279) ── 800×480 glass
                  │      SCLK 8 / MOSI 10 / CS 21 / DC 4 / RST 5 / BUSY 6
                  └── microSD  (SAME bus: SCLK 8 / MOSI 10, MISO 7, CS 12)
         ├─ ADC ladder ── GPIO1 (Back/Confirm/Left/Right) + GPIO2 (Up/Down)
         ├─ GPIO3 ─────── Power button (active-LOW)
         ├─ GPIO0 ─────── Battery voltage ADC (÷2 divider)
         └─ GPIO13 ────── Battery MOSFET latch
```

**One SPI bus serves both the panel and the SD card.** They are not independent:
`sd.separateSpi = false`. Any long card transfer blocks display updates and vice
versa. This is the structural difference from the S3 devices, which have a
dedicated SDMMC slot.

**Six buttons on two ADC pins**, not six GPIOs. See
[`features/buttons.md`](features/buttons.md).

Full tables: [`pinouts-and-buses.md`](pinouts-and-buses.md).

## Distinctive strengths

- **USB-C charging** — the only member of the family with it, and the reason
  several owners refuse to upgrade to the X4 Pro.
- **The largest firmware ecosystem** of any device here; most projects target it
  first.
- **A complete 16 MB factory flash dump is publicly available and archived here** —
  uniquely among Xteink devices.
- Cheap and, latterly, very cheap secondhand.

## Shortcomings and constraints

- **Discontinued.** No new stock from the vendor; accessories exhausted.
- **No RTC and no fuel gauge.** Battery percentage is an ADC estimate; the clock
  is lost on power loss.
- **SD shares the display SPI bus.**
- **No PSRAM.** CrossPoint moved off GitHub releases partly because of
  out-of-memory problems on the C3 devices.
- **Ships USB-locked** on many units.
- **A hardware revision exists that does not self-latch** — see below.

### The self-latch revision, a genuine field hazard

> "GPIO13 gates the battery MOSFET. Known units self-latch through a pull once the
> power button bridges the rail, so firmware never had to assert it — but **at
> least one hardware revision in the field does not self-latch and stays powered
> only while the button is held.** Asserting the latch is a no-op on self-latching
> units. Driving it LOW is the battery power-off."
> — **[SDK]** `BoardConfig.h:868–874`

So there are **at least two X4 board revisions**, they are **not externally
distinguishable**, and firmware that does not assert GPIO13 will appear to work on
one and be unusable on the other. Always assert the latch.

## Performance summary

| Figure | Value | Status |
|---|---|---|
| Display SPI, FreeInk default | **20 MHz** = SSD1677 datasheet write max | in-spec |
| Plane write @20 MHz | **~38 ms/refresh** | **[SDK]** measured comment |
| Optional overclock | **40 MHz** via `-DFREEINK_X4_OVERCLOCK_SPI` | **out of spec (2× datasheet)** |
| Plane write @40 MHz | **~19 ms** — saves ~17–20 ms/refresh | **[SDK]** |

The 40 MHz mode is what the **CrossPoint / Witch Reader** fork used. The SDK
makes it opt-in and warns it "can glitch plane writes on marginal wiring". This is
the clearest performance/reliability trade-off documented anywhere in the family.

## Pricing and availability

**Delisted.** Last vendor price **$69.00** (community-reported 2026-07-24).
Every X4 accessory shows sold out on 2026-09-04. Secondhand is now the only
channel; one X3 was reported at **$16**, which suggests the used market for these
is very soft. See [`market-and-pricing.md`](market-and-pricing.md).

## When to use / when not to use

**Use it** if you find one cheap and want the best-supported target in the
ecosystem with USB-C charging. **Do not use it** if you need PSRAM, an RTC, a real
fuel gauge, or a device you can still buy new.

## Alternatives by tier

| Tier | Alternative |
|---|---|
| Still purchasable, same class | [X3](../x3/README.md) $69 — sharper screen, IMU, NFC, RTC, real gauge, but pogo charging |
| More powerful, still a reader | [X4 Pro](../x4-pro/README.md) $99 — S3, PSRAM, touch, frontlight; **pogo charging** |
| Development platform | [M5Stack PaperMono](../../m5stack/papermono/README.md) — schematic, headers, USB-C |

## Images and teardown/PCB views

**No X4 teardown was located.** The [X3 teardowns](../x3/media.md) show a related
but different board. See [`media.md`](media.md).

## Common tasks / How do I…?

| Task | Guide |
|---|---|
| Drive the display, handle the controller variants | [`features/display.md`](features/display.md) |
| Read the 6-button ADC ladder | [`features/buttons.md`](features/buttons.md) |
| Mount the microSD on the shared SPI bus | [`features/storage.md`](features/storage.md) |
| Read battery voltage, hold the power latch | [`features/battery-and-power.md`](features/battery-and-power.md) |
| Use USB-C | [`features/usb.md`](features/usb.md) |
| Use Wi-Fi / BLE | [`features/wifi-and-bluetooth.md`](features/wifi-and-bluetooth.md) |
| Build and flash | [`development.md`](development.md) |
| **Dump / restore stock firmware** | [`factory-firmware.md`](factory-firmware.md) |

## Documentation map

[`pinouts-and-buses.md`](pinouts-and-buses.md) ·
[`development.md`](development.md) ·
[`factory-firmware.md`](factory-firmware.md) ·
[`sources.md`](sources.md) ·
[`coverage.md`](coverage.md) ·
[`compatibility-and-status.md`](compatibility-and-status.md) ·
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) ·
[`market-and-pricing.md`](market-and-pricing.md) ·
[`media.md`](media.md) ·
[research log](../x4-pro/research-log.md) and
[commands](../x4-pro/commands.md) are family-wide and kept once, under the X4 Pro.

## Artifact layout

```
artifacts/firmware/
└── xteink-x4-oem-full-flash-16mb.bin          → archived (symlink)
    xteink-x4-oem-full-flash-16mb.bin.ARCHIVED.md
```

**The only Xteink factory firmware image obtained by this session.**
16,777,216 B · SHA-256 `b9cf27cc254c737c901f81e7fcf0c48308e29bd979848ab0ac0bf6c6f5e8c245`
· retrieved 2026-09-04. Full analysis in
[`factory-firmware.md`](factory-firmware.md); recovery instructions in the
[placeholder](artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin.ARCHIVED.md).

## Known conflicts and unresolved identities

See [`gaps-and-conflicts.md`](gaps-and-conflicts.md). Headline: **the exact
ESP32-C3 package variant and the exact Puya flash part number have never been
read** — both are family-level identifications from a photograph caption, not part
numbers. And the stock firmware's on-screen version (V5.x) **cannot be recovered
from the app descriptor**, which reports the Arduino lib-builder identity instead.

---

## Round 2 — appended 2026-09-11: FCC internal photographs, and the X4 is withdrawn

**No line above was altered.**

### Withdrawn, completely

On 2026-09-04 the X4's product record was already absent from the vendor API and
its four dedicated accessories were listed but sold out. On **2026-09-11** those
four accessory records are **gone from the catalogue entirely**:
`xteink-x4-matte-screen-protector`, `xteink-x4-protective-case`,
`xteink-x4-screen-protector`, `xteink-x4-magnetic-case`.

The `x4-series` collection now contains **two generic items** — a magnetic
reading light and an adhesive metal ring — both of which fit any device in the
family. The vendor's device-only `machine` collection contains **X3, X4 Classic,
X4 Pro** and no X4.

**Its successor is the [X4 Classic](../x4-classic/README.md)**, listed
2026-09-06 at US$79, marketed by the vendor as "X4 V2". It keeps the buttons-only
reading model and the four bottom keys, moves to an ESP32-S3 with 8 MB PSRAM and
native SDMMC — and **drops USB-C for a pogo connector**, which is the single most
complained-about change in the family's history
([r/xteinkereader `1wagbmu`](https://old.reddit.com/r/xteinkereader/comments/1wagbmu/),
2026-09-08, **616 points / 730 comments**).

**The X4 is the only Xteink reader that ever had USB-C.** That is now a
historical fact rather than a purchasing option.

### A regulatory teardown, public since 2026-07-04

| Field | Value |
|---|---|
| **FCC ID** | **`2BTR9-XTEINKX4`** |
| Applicant | Shenzhen Xiaohu Xingtong Technology Co., Ltd., FRN `0037772233` |
| Granted | **2026-01-05** |
| Equipment class | DTS, 2412–2462 MHz |
| **Internal Photos** | **public since 2026-07-04** |
| Users Manual | **public since 2026-07-04** |
| Schematics · Block Diagram · Operational Description | **permanently confidential** |
| Source | <https://fccid.io/2BTR9-XTEINKX4> |

Retained: `artifacts/certification/2BTR9-XTEINKX4-internal-photos.pdf`,
770,254 B, SHA-256
`fd1623a7c9df42ba8140cea6d2618722726c1f442209c02f8229c1b50658f370`,
**15 embedded images**, from
<https://fccid.io/2BTR9-XTEINKX4/Internal-Photos/Internal-Photos-8956380.pdf>,
retrieved 2026-09-11 with UA `WhatsApp/2.23.20.0`. Validated `%PDF`.

**One image was inspected; the set was not systematically read.** What was seen,
stated as an observation and not as an identification:

- A green PCB carrying a **meandering PCB trace antenna**, a shielded module area
  with an Espressif-logo QFN part, a **40.000 MHz crystal** and an 8-pin SOIC
  flash package.
- A separate board section carrying a **USB-C receptacle**.
- A wide FPC connector (display) and a second smaller FPC connector.

This is consistent with everything this record already says — ESP32-C3, 16 MB
SPI flash, USB-C — and **corroborates it from a regulatory photograph rather than
from a firmware image for the first time**. It is not a component identification:
no top marking was transcribed, because the resolution and angle do not support
it without careful work that this pass did not do.

**Next session:** read all 15 images against
[`pinouts-and-buses.md`](pinouts-and-buses.md) and
[`gaps-and-conflicts.md`](gaps-and-conflicts.md), and against
[`components/unidentified/xteink-x3-x4/`](../../../components/unidentified/xteink-x3-x4/README.md) —
**the four unidentified parts in that record are exactly what these photographs
are for.**

The public `Users Manual`
(<https://fccid.io/2BTR9-XTEINKX4/User-Manual/Users-Manual-8956383.pdf>) was
**not fetched** and is the vendor's own documentation for a device whose store
page no longer exists.
