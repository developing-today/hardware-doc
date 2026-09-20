# Xteink X4 Pro

> SKU `X4Pro-Black` · Space Black only · **$99.00** observed 2026-09-04 ·
> published to the vendor store **2026-07-21** · in production and in stock ·
> research retrieval date **2026-09-04**.

## Identity and variants

| Field | Value | Evidence |
|---|---|---|
| Marketed name | **Xteink X4 Pro Pocket eReader** | **[VENDOR]** `products.json`, handle `xteink-x4-pro-pocket-ereader` |
| Vendor SKU | `X4Pro-Black` | **[VENDOR]** variant `48382782669041` |
| Colour variants | **One only** — Space Black | **[VENDOR]** single variant |
| Shipping weight | 250 g (packaged; **not** device mass) | **[VENDOR]** `grams: 250` |
| Product created / published | 2026-07-07 / **2026-07-21** | **[VENDOR]** |
| Board tag (stock firmware) | `ESP32S3_X4_TL_SSD1677`, app names itself `XTEink X4 Pro` | **[DUMP]** app1 strings |
| FreeInk profile | `BoardConfig::XTEINK_X4_PRO`, name string `xteink_x4_pro` | **[SDK]** `BoardConfig.h:1495–1497` |
| Build flag | `-DFREEINK_DEVICE_X4PRO=1` | **[SDK]** `docs/xteink-x4pro-support.md:13` |
| Lifecycle | Current flagship. Not discontinued | **[VENDOR]** in stock 2026-09-04 |

### Panel-controller variants — the important one

**The X4 Pro ships with at least three different display controllers depending on
production batch, on identical wiring.**

| Controller | Maker | Status |
|---|---|---|
| **SSD1677** | Solomon Systech | Original batches |
| **UC8179** | UltraChip | Newer batches. *"the variant every unit benched so far has carried"* |
| **UC8279** | UltraChip | Newer batches, distinguished by `LUT_VER` |

This is **not** a cosmetic revision — the command sets differ, and a firmware that
assumes the wrong one produces a panel that resets and runs waveforms but never
develops an image. The SDK resolves it at boot with a bit-banged half-duplex read
of the UC81xx `VER (0x70)` / `FLG (0x71)` registers, which the SSD-family does not
answer at all **[SDK]** `XteinkDetect.cpp:113–119, 366–390`.

There is **no external revision marking** that lets you tell them apart before
powering the unit on. See [`features/display.md`](features/display.md).

## What it is and visual identification

A sealed, pocket-sized 4.26-inch e-ink reader, roughly the footprint of a large
phone, in a single black finish. Distinguishing features versus the rest of the
family, all externally visible:

- **A touchscreen** — the only Xteink ESP32 device with one.
- **A frontlight** with warm/cool colour-temperature control.
- **No USB-C port for charging.** It charges over a **magnetic pogo-pin connector**
  and ships needing a proprietary adapter (`x3-magnetic-pogo-pin-charging-cable`,
  $4.99; `magnetic-charging-adapter-for-x3`, $5.99) **[VENDOR]**. This is the
  single most-complained-about design decision — see [`community.md`](community.md).
- **Only two physical navigation buttons** (side keys) plus power; everything else
  is touch, including a **capacitive "Home" pad below the glass** that is not a
  GPIO but a GT911 key bit.

Teardown photography specific to the X4 Pro was **not found**. The board-level
knowledge below comes from firmware reverse engineering plus on-hardware probing
by the FreeInk maintainers, which for pin-level facts is stronger evidence than a
photograph — but it means **no PCB image is held**. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

## Product history, family and culture

| Date | Event | Evidence |
|---|---|---|
| 2026-06-13 | S4 "June production run" video also shows unannounced hardware | **[COMM]** [r/XTEINK `1u4ty4q`](https://old.reddit.com/r/XTEINK/comments/1u4ty4q/) |
| 2026-06-22 | Community spots a **new X4 variant** in vendor video — *"Physical buttons + frontlight but no touchscreen"*, 300 points | **[COMM]** [r/XTEINK `1ud0d9c`](https://old.reddit.com/r/XTEINK/comments/1ud0d9c/) |
| 2026-07-07 | X4 Pro product record created in Shopify | **[VENDOR]** |
| 2026-07-17 | Public discussion thread, 89 comments, poll "X4 Pro or S4?" | **[COMM]** [r/xteinkereader `1uz9mtg`](https://old.reddit.com/r/xteinkereader/comments/1uz9mtg/) |
| 2026-07-21 | **Launch.** Listed at $99, described as pre-order with restock 6 Aug | **[VENDOR]** product body + published_at |
| 2026-07-21 | Pogo-pin backlash thread, 71 comments | **[COMM]** [r/xteinkereader `1v2txxe`](https://old.reddit.com/r/xteinkereader/comments/1v2txxe/) |
| 2026-07-26/28 | Screen protectors listed (matte, then tempered glass) | **[VENDOR]** |
| 2026-08-27 | Stock firmware **7.4.4** built (ESP-IDF 6.0.1) | **[SDK]** `docs/xteink-x4pro-support.md:84–87` |
| 2026-09-04 | In stock at $99; matte protectors and 2/3-packs sold out | **[VENDOR]** |

The X4 Pro is the ecosystem's **design floor**: CrossPlay's `LOCAL_SCOPE.md` names
it as the reference target and defines the minimum viable input as "two side keys
plus touch" ([CrossPlay record](../../../software/applications/crossplay/README.md)).
Firmware that works here is expected to degrade gracefully elsewhere.

## Key specifications

| Item | Value | Component record | Evidence |
|---|---|---|---|
| SoC | **ESP32-S3**, 16 MB flash, 8 MB PSRAM | [`espressif/esp32-s3r8`](../../../components/espressif/esp32-s3r8/README.md) | **[SDK]** header §X4 Pro |
| Display | 800×480 mono e-ink, 4.26″, ~219 PPI | — | **[SDK]** `BoardConfig.h:1500–1501` |
| Display controller | SSD1677 **or** UC8179 **or** UC8279 | [`solomon-systech/ssd1677`](../../../components/solomon-systech/ssd1677/README.md) · [`ultrachip/uc8179`](../../../components/ultrachip/uc8179/README.md) · [`ultrachip/uc8279`](../../../components/ultrachip/uc8279/README.md) | **[SDK]** |
| Touch | **GT911** capacitive, I²C 0x5D (alt 0x14), portrait-mounted | [`goodix/gt911`](../../../components/goodix/gt911/README.md) | **[SDK]** `BoardConfig.h:1548–1567` |
| Frontlight | Dual-channel warm/cool LED, LEDC PWM 25 kHz / 10-bit | — | **[DUMP]** OEM LEDC init |
| RTC | **BM8563** (PCF8563 register-compatible), I²C 0x51 | [`generic/bm8563`](../../../components/generic/bm8563/README.md) | **[SDK]** hardware-confirmed |
| Fuel gauge | **CW2017**, I²C 0x63, needs an 80-byte BATINFO profile | [`cellwise/cw2017`](../../../components/cellwise/cw2017/README.md) | **[SDK]** hardware-confirmed |
| Storage | microSD via **native SDMMC**, 1-bit, slot 1, 40 MHz | [`generic/micro-sd-sdmmc`](../../../components/generic/micro-sd-sdmmc/) | **[SDK]** hardware-confirmed |
| USB | ESP32-S3 native USB-OTG, D− GPIO19 / D+ GPIO20 | — | **[SDK]** |
| Charging | **Magnetic pogo pins** — no USB-C charge port | — | **[VENDOR]** + **[COMM]** |
| Charger STAT | GPIO21, active-HIGH | — | **[DUMP]** `Cw2017PowerHal` vtable slot 3 |
| Radios | Wi-Fi + BLE (ESP32-S3 integrated) | — | **[SDK]** |
| IMU | **None** — unlike the X3 and X4C | — | **[SDK]** `sensors.imuType = ImuType::None` |
| Audio / LEDs / PMIC | **None fitted** | — | **[SDK]** `NO_AUDIO`, `NO_LEDS` |

**Reading the table.** The three-way controller ambiguity is the only entry that
should change how you write code: everything else is fixed silicon. The absence of
an IMU is worth noting because the X3 and the X4 Classic both have one — a
"Pro" model is not a superset of its siblings here.

## Architecture and components

One ESP32-S3 owns everything; there is no coprocessor, no GPIO expander and no
PMIC. Three subsystems share one I²C bus and one SPI-ish display bus:

```
ESP32-S3 ── SPI(bit-banged CS/DC) ── EPD controller (SSD1677│UC8179│UC8279) ── 800×480 glass
         ├─ I²C  SDA39/SCL38 @400k ─┬─ GT911 touch      0x5D   (rail gated by GPIO2, active-LOW)
         │                          ├─ BM8563 RTC       0x51
         │                          └─ CW2017 gauge     0x63
         ├─ SDMMC 1-bit ── microSD (rail gated by GPIO5, active-LOW)
         ├─ LEDC ch4/ch5 ── frontlight cool(GPIO8) / warm(GPIO9)
         ├─ native USB   ── D−GPIO19 / D+GPIO20
         └─ GPIO1 ── master peripheral rail (HIGH), asserted first at boot
```

**GPIO1 is load-bearing and non-obvious.** The OEM board-init drives it HIGH
before any other bring-up. Without it the panel rail and the SD slot both stay
unpowered, and the symptom is "EPD BUSY never asserts, SD returns 0xFF"
**[SDK]** `BoardConfig.h:1599–1602`.

**Two power enables are active-LOW**, which is the opposite of the convention on
most boards: GPIO2 (touch) and GPIO5 (SD). Driving them HIGH — the naive "enable"
— leaves the GT911 silent on the bus and breaks every SD block read with error
`0x107`.

Full tables: [`pinouts-and-buses.md`](pinouts-and-buses.md).

## Common uses and representative projects

- **As shipped** — a sealed EPUB reader with a Chinese-first stock UI.
- **Reflashed** — the dominant use. CrossPoint Reader, CrossInk and their forks
  replace the stock firmware entirely.
- **As an ESP32-S3 e-paper platform** — `vjFaLk/esphome-xteink` exposes it to
  Home Assistant as an ESPHome component; `thepropm/proink-os` is a from-scratch
  firmware; `parsimo2010/xteink-ft8` turns one into an FT8 amateur-radio display.

See [`projects-and-community.md`](projects-and-community.md) for the full census.

## Distinctive strengths

- **The only sub-$100 sealed e-reader with a touchscreen, a frontlight and a
  fully documented, community-reverse-engineered board.** Every pin below was
  probed on real hardware.
- **8 MB PSRAM.** This is the practical difference from the C3 X4: multi-buffer
  rendering, damage-window partial refresh and large book indices are possible
  here and are not on a C3.
- **Native SDMMC** rather than SPI — meaningfully faster card access.
- **Actively maintained firmware** from several independent projects.

## Shortcomings and constraints

- **Pogo-pin charging with no USB-C charge path.** Lose the adapter and the device
  is unusable. This is the most-cited complaint in the community.
- **Ships USB-locked from the factory** on many units — see [`development.md`](development.md).
- **Panel-controller lottery.** Firmware not carrying all three drivers may brick
  the display on a newer unit.
- **No IMU**, so no motion page-turn, unlike its cheaper siblings.
- **Touch axis mirroring is internally contradicted** in the SDK's own
  documentation — see [`gaps-and-conflicts.md`](gaps-and-conflicts.md).
- **No published schematic, no FCC filing located, no teardown photography.**

## Performance summary

**No measurement of this device was made in this session, and no independent
benchmark was found.** What exists:

| Figure | Value | Status |
|---|---|---|
| Display SPI clock, OEM | **5 MHz** (`SPISettings 0x4C4B40`) | **[DUMP]** recovered constant |
| Display SPI clock, FreeInk | 20 MHz | **[SDK]** chosen, in spec |
| Plane write @20 MHz (X4, same controller) | ~38 ms/refresh | **[SDK]** comment, `BoardConfig.h:836` |
| SDMMC | 1-bit, 40 MHz | **[SDK]** |
| Battery capacity | **unknown** | gap |

The OEM clocking its own panel at **5 MHz when the controller is rated for 20**
is the single most actionable performance finding: stock firmware leaves roughly
a 4× margin on the table for RAM writes.

## Pricing and availability

See [`market-and-pricing.md`](market-and-pricing.md). Headline, **2026-09-04**,
vendor direct, worldwide from Shenzhen: **US$99.00**, Space Black, in stock.

## Competitors, equivalents and clones

See [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md).

## Launch-era versus current market fit

At launch (2026-07-21) the X4 Pro was the only sealed sub-$100 reader with both
touch and a frontlight that also had a live open-source firmware scene. As of
2026-09-04 that is still true, but the **S4** — Android 11, frontlight, touch, at
~¥339 (≈US$50) — undercuts it on paper for anyone who does not care about
programmability. See [`../s4/README.md`](../s4/README.md).

## When to use / when not to use

**Use it when** you want a pocket e-reader you will reflash, you want touch and a
frontlight, and you accept a proprietary charging cable. **Do not use it when**
you need a general-purpose ESP32-S3 dev board (buy a
[PaperMono](../../m5stack/papermono/README.md) or a Waveshare board — you get
headers, USB-C, a schematic and no unlock dance), or when you need USB-C charging,
or when you need an IMU.

## Alternatives by tier

| Tier | Alternative | Why |
|---|---|---|
| Cheaper, same family | [X4](../x4/README.md) $69 / [X3](../x3/README.md) $69 | No touch, no frontlight, C3 not S3 |
| Cheaper, buttons + S3 | [X4 Classic](../x4-classic/README.md) | Same board, no touch/frontlight, **plus** an IMU |
| Development board | [M5Stack PaperMono](../../m5stack/papermono/README.md) | Schematic published, USB-C, headers, no unlock |
| Non-programmable | S4, Kobo, Boox | If you will never flash it, programmability is not worth the pogo pin |

## Images and teardown/PCB views

**None held.** No X4 Pro teardown was located. This is a real gap —
[`media.md`](media.md) records what was searched.

## Community, editorial and project coverage

[`community.md`](community.md) · [`projects-and-community.md`](projects-and-community.md)

## Common tasks / How do I…?

| Task | Guide |
|---|---|
| Drive the display / handle the 3-controller lottery | [`features/display.md`](features/display.md) |
| Read touch and the capacitive Home key | [`features/touch.md`](features/touch.md) |
| Read the two side buttons and power | [`features/buttons.md`](features/buttons.md) |
| Control the warm/cool frontlight | [`features/frontlight.md`](features/frontlight.md) |
| Mount the microSD card | [`features/storage.md`](features/storage.md) |
| Read battery percentage / charge state | [`features/battery-and-power.md`](features/battery-and-power.md) |
| Use USB / USB-MSC | [`features/usb.md`](features/usb.md) |
| Use Wi-Fi and BLE | [`features/wifi-and-bluetooth.md`](features/wifi-and-bluetooth.md) |
| Read the RTC | [`features/rtc.md`](features/rtc.md) |
| Build and flash firmware | [`development.md`](development.md) |
| Unlock a USB-locked unit | [`development.md`](development.md#usb-lock) |
| Dump / restore stock firmware | [`factory-firmware.md`](factory-firmware.md) |

## Documentation map

[`pinouts-and-buses.md`](pinouts-and-buses.md) ·
[`development.md`](development.md) ·
[`factory-firmware.md`](factory-firmware.md) ·
[`sources.md`](sources.md) ·
[`research-log.md`](research-log.md) ·
[`commands.md`](commands.md) ·
[`coverage.md`](coverage.md) ·
[`compatibility-and-status.md`](compatibility-and-status.md) ·
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) ·
[`market-and-pricing.md`](market-and-pricing.md) ·
[`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) ·
[`projects-and-community.md`](projects-and-community.md) ·
[`community.md`](community.md) ·
[`media.md`](media.md)

## Artifact layout

```
artifacts/
├── firmware/           (empty — see factory-firmware.md; no X4 Pro image was located)
└── source-snapshots/   (empty — the FreeInk SDK clone lives in scratch/eink-software/repos/)
```

**No artifact is held for this device.** The X4 Pro OTA package
`xteink_app_update_x4pro_7.4.4_20260827_133901.xota` is named in the SDK docs but
was **not located for download**. See [`factory-firmware.md`](factory-firmware.md).

## Known conflicts and unresolved identities

Summarised in [`gaps-and-conflicts.md`](gaps-and-conflicts.md). The two that
matter most: the SDK's board header and its own device doc **disagree about
whether touch axis flipping is confirmed or pending**, and the **battery capacity,
device mass and dimensions are entirely unestablished**.

---

# ROUND 2 — appended 2026-09-11. **The X4 Pro now has three second custodians.**

**No line above was altered.** The record above, and
[`VERIFICATION-xteink.md`](../../../VERIFICATION-xteink.md) §12, stated the
central weakness plainly: *"for the X4 Pro and X4 Classic, essentially every
technical claim traces to one repository at one commit
(`Free-Ink/freeink-sdk` @ `24003795381a6c23630a26472ae3b06550333e71`), with no
teardown, schematic or regulatory filing to corroborate it."*

**That is no longer true for the X4 Pro.** Three independent custodians now
exist, one of them a US federal record and one of them a person with the device
on a desk running `esptool` against it.

## Custodian 2 — a physical unit, dumped and instrumented

| | |
|---|---|
| Who | [`kycube/x4pro-emu`](https://github.com/kycube/x4pro-emu) — a QEMU emulator for the X4 Pro |
| Commit | **`bf4b86ae0471012d4d07c0bb3042f3f561c9c302`** |
| Repo created | **2026-09-07** — three days after the first sweep |
| Licence | **none stated** → redistribution `unknown`, **reference-only**, not vendored |
| Basis | *"Xteink X4 Pro on the desk"*, read-only operations, 2026-09-06 |

### What it independently confirms

| Claim | Prior evidence | New evidence | Verdict |
|---|---|---|---|
| SoC is **ESP32-S3** | FreeInk profile | **`esptool chip-id`: ESP32-S3 (QFN56) rev v0.2, 40 MHz crystal, USB-Serial/JTAG, MAC `98:c3:77:be:ea:30`** | **confirmed on silicon** |
| **8 MB PSRAM** | FreeInk profile | eFuse `PSRAM_CAP=8M`, `PSRAM_VENDOR=AP_3v3`; boot log *"Embedded PSRAM 8MB"*, octal, 80 MHz | **confirmed** |
| **16 MB flash** | FreeInk profile, image length | boot log `flash io: qio`; a **16,777,216 B** dump | **confirmed** |
| Partition table | FreeInk docs | decoded from the dump: `nvs` `0x9000`/`0x5000`, `otadata` `0xE000`/`0x2000`, `app0` `0x10000`/`0x7E0000`, `app1` `0x7F0000`/`0x7E0000`, `spiffs` `0xFD0000`/`0x14000`, `coredump` `0xFE4000`/`0x1C000` | **confirmed** |
| **GT911 @ 0x5D**, SDA 39 / SCL 38 @ 400 kHz, INT 10, RST 4, power-enable GPIO2 active-low | FreeInk profile | live I²C traces of the stock app | **confirmed** |
| **BM8563 @ 0x51** | FreeInk profile | I²C map | **confirmed** |
| **CW2017 @ 0x63**, needs an 80-byte BATINFO to `0x10..0x5F` | FreeInk + a register dump | I²C map, same addresses and behaviour | **confirmed** |
| Buttons **Left GPIO0, Right GPIO7, Power GPIO3**, active-low `INPUT_PULLUP` | FreeInk, and this repository's own refutation that GPIO7 was a display enable | independent restatement from the running board | **confirmed — the earlier refutation stands** |
| Frontlight **cool GPIO8 / warm GPIO9**, LEDC 25 kHz 10-bit | FreeInk profile | LEDC register traces of the stock app, including hardware fades | **confirmed, and extended** |
| SDMMC **CLK 41 / CMD 42 / DAT0 40**, slot 1, 1-bit; **GPIO5** active-low card-power gate | FreeInk profile | same | **confirmed** |
| Charger `STAT` **GPIO21**, active-high | FreeInk profile | same | restated, still not independently measured |
| **Panel controller varies by batch; VER/FLG probe** | FreeInk `XteinkDetect.cpp` | this unit: NVS `hw_calib/screenType = 2` → **UC8279**, and CrossPoint on the device printed **`VER=00 0F 68 00 00 FLG=13`** → LUT_VER `0x68` → UC8279 | **confirmed on hardware, twice, by two mechanisms** |

### What it adds that nobody had

- **eFuse state**: no secure boot, no flash encryption, all key purposes `USER`,
  USB Serial/JTAG enabled. **The X4 Pro is not locked at the silicon level.**
- **A factory serial in eFuse BLOCK3**: ASCII `X4CB02EN26082416646`.
- **Stock firmware `xteink_app` 7.2.4**, ESP-IDF **v6.0.1**, built
  **2026-08-14 19:25:05**; bootloader built 2026-08-14 19:24:53.
  **This is a fourth version number for X4 Pro stock firmware** — see
  [`factory-firmware.md`](factory-firmware.md).
- **Two independent full-flash dumps hashing identically**
  (`90734554798da8dbe…0143fe`) — the correct way to prove a dump, and the first
  time it has been done in this family.
- **The stock app talks to the panel at 10 MHz** (`SPI2 CLOCK 0x70c7`), not the
  5 MHz the FreeInk comments attribute to the OEM. A 48,000-byte plane takes
  ≈38 ms.
- **The stock UC8279 command stream, traced**: `00 37 4D` PSR, `61 03 20 02 58`
  TRES (**800×600 declared, gates 120–599 used**), `65` GSST, `03 20` PFS,
  `E1 02`, DTM2/DTM1/DTM2, `50 97` CDI, `E0 02`, `E5 1E`, `04` PON (40 ms),
  `00 17 4D`, `12` DRF (1.3 s). And the finding that **the old plane is
  pre-sent immediately after each refresh**, so a trace ending in DTM1 is idle,
  not stalled.
- **Frontlight behaviour**: warm channel at 249 ‰ on wake, **fades out 60 s after
  the last input**, nine colour-temperature presets from Cool 4 to Warm 4 with
  the two channels mixed at roughly constant total, brightness in 10 % steps.
  NVS `user_config/lightBri`, `lightCT`, `lightOn`.
- **The Home pad is a GT911 touch key**, not a GPIO: bit 4 of status `0x814E`,
  key byte at `0x814F + 8·count`. The stock treats it as **Back, one level**.
- **NVS `hw_calib/region`**: `1` = CN, `2` = overseas.

### What it corrects

The FreeInk **support document's** I²C paragraph has **INT and RST swapped** and
is stale; the **struct** is right. Where the two disagree, trust the struct.

## Custodian 3 — a firmware project that tested on hardware

[`clackups/draftling`](https://github.com/clackups/draftling) @
`92ba7e514f66bbe42a7fea6d38eff45eed82617b`, MIT, 71 stars. Its `HARDWARE.md`
states, verbatim: ***"This board has been tested on physical hardware after an
initial blind port."*** Two findings, both of which are things only hardware
tells you:

1. **A real asynchronous-DMA bug in the shared UC8179/UC8279 path.** A full
   refresh *"reproducibly painted only the top third or so of the panel"*. Cause:
   the OLD-plane write reused the same scratch buffer the NEW-plane write had
   just handed to `esp_lcd_panel_io_tx_color()`, whose transfer is queued
   asynchronously and could still be in flight when the next line `memset` it.
   Fixed by streaming the OLD plane's constant white fill from a separate,
   never-mutated buffer. **Anyone writing a driver for this panel from the same
   reverse engineering can hit this.**
2. **A touch-orientation correction made against a physical unit.** FreeInk's
   `swapXY=true, flipY=true` *"had touches landing 180 degrees opposite of where
   the finger was"*; Draftling's `TOUCH_MIRROR_X`/`TOUCH_MIRROR_Y` are now `1`/`0`.
   **This contradicts FreeInk's "confirmed by corner-tap" annotation**, and it is
   recorded as an open conflict — the two projects use different rendering
   stacks with different orientation conventions, so they may not actually
   disagree. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

It also runs the panel at **the OEM's 5 MHz** rather than FreeInk's rate, and
uses a **dual-OTA partition table on purpose** so the stock and CrossPoint
updaters can reinstall — they refuse a table with no `otadata`.

## Custodian 4 — the United States FCC

| Field | Value |
|---|---|
| **FCC ID** | **`2BTR9-X4PRO`** |
| Applicant | **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**, Longhua District, Shenzhen, FRN `0037772233` |
| Granted | **2026-06-16** — five weeks before the store listing of 2026-07-21 |
| Equipment class | DTS, **2412–2462 MHz** |
| Test firm | Shenzhen BKC Testing Co., Ltd. |
| Public now | **External Photos (5.1 MB)**, Label and Information (1.1 MB), Antenna Report, Test Report, RF Exposure, attestations |
| **Internal Photos (1,023 KB)** | **embargoed until 2026-12-12** |
| Schematics · Block Diagram · Operational Description | **permanently confidential** |

Retained: [`artifacts/certification/`](artifacts/certification/README.md) — the
external photographs and the label exhibit. **The internal photographs become
public on 2026-12-12**, which is the dated route to a PCB-level verification of
the remaining single-source claims.

## What is *still* single-source

Be precise about what has and has not been corroborated:

| Still traces only to FreeInk | Why the new custodians do not help |
|---|---|
| **Panel pin assignment** SCLK 12 / MOSI 11 / CS 13 / DC 18 / RST 14 / BUSY 6 | Both new firmware custodians cite FreeInk as their source; neither derived the pins independently |
| The `XteinkDetect` probe **algorithm** | Same lineage. Its *result* on one unit is now confirmed; the bit-banged procedure is not |
| Charge-`STAT` polarity on GPIO21 | Restated, never measured |
| Exact refresh timings (~1800 ms full, ~500 ms fast) | Inherited from FreeInk's docs; the desk unit's own measurement is explicitly marked pending by its author |

**The right summary is: the X4 Pro's *silicon, memory, flash map, I²C map,
button map, SD path, frontlight behaviour and panel identity* are now
hardware-confirmed by a third party. Its *panel pinout* is not.**

## Correction to the record above

`displaySpiHz` for the X4 Pro profile changed from **20 MHz to 10 MHz** in
FreeInk commit
[`39606d5a`](https://github.com/Free-Ink/freeink-sdk/commit/39606d5a)
(2026-09-09), now shared as `XTEINK_DISPLAY_SPI_HZ` across every Xteink board.
The comment that previously justified 20 MHz — *"the OEM clocks the panel at only
5 MHz… but the SSD1677 handles far more"* — is gone. **Independently, the desk
unit's stock app was measured running SPI2 at 10 MHz**, so the OEM's own rate on
at least one shipping unit is 10 MHz, not 5 MHz.

---

## ⚠ Correction, 2026-09-11 — Xteink FCC grants exist

The line(s) below, still present above and deliberately unedited, are **refuted**:

> *line 165:* - **No published schematic, no FCC filing located, no teardown photography.**
>

**Xteink is an FCC grantee.** Applicant **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**, grantee code **`2BTR9`**, registered 2025-12-21, holding **five granted Original Equipment authorisations**:

| FCC ID | Granted | Device |
|---|---|---|
| `2BTR9-X4L` | 2026-08-13 | XTEINK X4 Light |
| `2BTR9-X4C` | 2026-07-20 | XTEINK X4 Classic |
| `2BTR9-X4PRO` | 2026-06-16 | XTEINK X4 Pro |
| `2BTR9-XTEINKX4` | 2026-01-05 | XTEINK X4 |
| `2BTR9-XTEINKX3` | 2025-12-26 | XTEINK X3 |

The original finding confused **"no mark visible in a product photograph"** with **"no grant exists"**. Those are different claims, and only the first was tested.

- ✅ **Survives:** no FCC ID was legible on the exteriors photographed. Not re-tested.
- ❌ **Refuted:** any reading that these devices are uncertified or unauthorised for the US.

47 CFR §2.935 permits an **e-label** in software instead of a printed mark, which is ordinary for a device with a screen. **That is a likely explanation and it was not verified.**

The absence was never re-searched in 2026-09-04 because **no FCC ID was known and the grantee code had not been found**. Enumerating the grantee — not searching the product name — is what resolved it. Method: [`guides/research/finding-certification-records.md`](../../../guides/research/finding-certification-records.md).

Full record, with controls: [`certification-and-compliance.md`](certification-and-compliance.md).

Listed in [`scratch/index-merge/corrections-requiring-review.md`](../../../scratch/index-merge/corrections-requiring-review.md).
