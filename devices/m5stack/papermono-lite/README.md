# M5Stack PaperMono-Lite

> **SKU `C153-Lite`** (as the documentation writes it) / **`C153-LITE`** (as the
> Shopify record writes it) · **USD 55.00** · white case · **no NFC, no LoRa** ·
> announced and on sale **2026-08-21** alongside the PaperMono · documentation
> published **2026-08-20** · at the research snapshot of **2026-09-01** it was
> **out of stock at the official store and listed by no reseller anywhere**.

## Read the PaperMono record first

**This is a variant record, not a standalone one.** The PaperMono-Lite is the
same board as the [PaperMono](../papermono/README.md) with two radios removed and
a different case colour. Everything about the SoC, the panel, the power
architecture, the two auxiliary microcontrollers, the pin map, the boot behaviour
and the development workflow is identical, and is documented **once**, there:

| Document | Applies to the Lite? |
|---|---|
| [`../papermono/README.md`](../papermono/README.md) | **Yes**, except the NFC and LoRa rows of the specification table and the NFC/LoRa lines of the architecture diagram |
| [`../papermono/pinouts-and-buses.md`](../papermono/pinouts-and-buses.md) | **Mostly.** See [what does not apply](#which-papermono-documents-apply-unchanged) — six ESP32-S3 GPIOs, two M5IOE1 pins, one M5PM1 GPIO, one I²C address and two connectors are radio-related and are unverified on this variant |
| [`../papermono/power-architecture.md`](../papermono/power-architecture.md) | **Yes**, except the LoRa rail (`3V3_L2_LoRa`, M5PM1 `G2`) and the NFC load switch. The five power states, the charger, the frontlight and every wake source are unchanged |
| [`../papermono/pin-naming-and-the-pyg-ambiguity.md`](../papermono/pin-naming-and-the-pyg-ambiguity.md) | **Yes, in full, and it matters more here** — see [below](#the-pyg-hazard-is-worse-on-the-lite-not-better) |
| [`../papermono/gaps-and-conflicts.md`](../papermono/gaps-and-conflicts.md) | **Yes**, except G5 (the missing `Stamp-LoRa-1262` datasheet) and G1 (the missing NFC schematic sheet), which are not Lite problems |
| [`../papermono/sources.md`](../papermono/sources.md) | **Yes.** Sources **S04**, **S05**, **S06**, **S16**, **S17**, **S49** and **S89** are Lite-specific; every ID cited below is defined there |
| [`../papermono/research-log.md`](../papermono/research-log.md) · [`../papermono/commands.md`](../papermono/commands.md) | **Yes** — one research pass covered both SKUs |

**Nothing in this record was verified against physical hardware.** No
PaperMono-Lite exists in this session and none could be bought.

## Identity

| Field | Value | Evidence |
|---|---|---|
| Marketed name | PaperMono-Lite | vendor product page (S04) |
| SKU | **`C153-Lite`** on `docs.m5stack.com`; **`C153-LITE`** in the Shopify record | S04, S49 — **the case differs between the vendor's own two systems** |
| Internal firmware name | **`Lite`**, against **`Pro`** for the full model | `M5PaperMono-UserDemo/main/hal/hal_board.cpp` (S41) — note the vendor's *firmware* calls the C153 "Pro" although the *product* is just "PaperMono" |
| Manufacturer | M5Stack Technology Co., Ltd (Shenzhen) | vendor site |
| Case colour | **White** | vendor comparison table |
| Store price | **USD 55.00** | S49 |
| Store status 2026-09-01 | Out of stock, `inventory_quantity = 0`, `inventory_policy = "deny"` | S49 |
| Store record created / published | `2026-08-18T14:26:42+08:00` / `2026-08-21T12:00:09+08:00` | S49 — created three minutes *before* and published one second *before* the PaperMono |
| Documentation published | 2026-08-20, category "Controllers" | S13 |
| Schematic asset | `PaperMono-Lite_PRJ_V0.6.2_20260522.pdf` — **`PRJ`, 4 sheets** | S04, S16 — **not retrieved**; see [gaps](#gaps-specific-to-this-record) |

No certification identifier is published for this SKU either: `/en/certification`
(S11) returns zero matches for `PaperMono`, `C153` **and** `C153-Lite`. That is a
verified negative, not a failed search.

## The vendor's own comparison table

Reproduced complete and verbatim from S04. **Both product pages carry the
identical table**, so this is the vendor's considered statement of the difference.

| Product Compare | PaperMono | PaperMono-Lite |
|---|---|---|
| Main Controller | ESP32-S3R8 | ESP32-S3R8 |
| Display | 3.97" 4-level grayscale black-and-white E-Paper, 480x800 | 3.97" 4-level grayscale black-and-white E-Paper, 480x800 |
| Touch | FT6336G | FT6336G |
| Front Light | Integrated | Integrated |
| Wi-Fi | 2.4 GHz | 2.4 GHz |
| **NFC** | **ST25R3916** | **❌** |
| **LoRa** | **Stamp LoRa-1262** | **❌** |
| Expansion Storage | microSD | microSD |
| IMU | BMI270 | BMI270 |
| RTC | RX8130CE | RX8130CE |
| Battery | 1150mAh | 1150mAh |
| **Shell Color** | **Gray** | **White** |

Four rows of that table carry the entire product difference: **NFC, LoRa, shell
colour — and the price, which the table does not show.** The two radios are the
whole of the **USD 10.00** delta.

## What the comparison table leaves out

The table above is accurate and incomplete. Diffing the two pages' **full
specification tables** recovers five further differences the vendor does not
surface, all established from primary vendor text (S01 against S04):

| Specification | PaperMono | PaperMono-Lite | Delta |
|---|---|---|---|
| **Product Weight** | **74.7 g** | **72.4 g** | **−2.3 g** |
| **Gross Weight** | **91.3 g** | **88.9 g** | **−2.4 g** |
| SoC clock wording | "240MHz" | "**up to** 240MHz" | wording only |
| NFC row | `ST25R3916 (ISO14443A/B, FeliCa™, ISO15693)` | **row absent entirely** | the Lite table has no NFC row at all |
| LoRa row | `SX1262 (Stamp LoRa-1262), 868–923 MHz, FPC ant.` | **row absent entirely** | likewise |
| **Schematic asset** | `PaperMono_SCH_V0.6.2_20260522.pdf` — **`SCH`, 6 sheets** | `PaperMono-Lite_PRJ_V0.6.2_20260522.pdf` — **`PRJ`, 4 sheets** | different naming convention and **two fewer sheets** |
| Model-size asset | `1267/C153_PaperMono_model_size.pdf` | `1268/C153-Lite_PaperMono-Lite_model_size.pdf` | separate mechanical drawings |
| Datasheets listed | 7 (incl. ST25R3916 and SX1261/2) | **5** | the Lite drops the two radio datasheets |
| PinMap sections | includes **RFID** and **LoRa** blocks | **both blocks absent** | |
| PlatformIO env | `[env:m5stack-papermono]` | `[env:m5stack-papermono-lite]` | |
| PlatformIO `lib_deps` | 5 libraries, incl. `M5Unit-NFC` and `RadioLib` | **3 libraries** | |
| Applications listed | E-Reader, Signage, Access Control, Identity Auth, Intelligent Transport | E-reader, Electronic shelf label, Information display terminal, **Portable control panel**, **Low-power IoT node** | entirely different positioning |
| Shipping weight (Shopify) | 100 g | 98 g | S48 / S49 |

**The weight difference is the most useful number here**, because it is a
*measurement* rather than a marketing statement: 2.3 g is the mass of the NFC
sub-board, its crystal and antenna, and the `Stamp-LoRa-1262-mini` module with its
FPC antenna. It is consistent with those parts being genuinely absent rather than
merely unpopulated on an otherwise identical assembly — though **the schematic
that would settle that (S16) was not retrieved**, so this remains `inferred`.

Two sheets fewer is the other quantitative hint. The PaperMono schematic
concatenates three Altium documents: the main project (sheets 1–4), the KEY/RGB
sub-board (sheet 5) and the NFC sub-board (sheet 6, itself explicitly numbered
`2/2` with sheet 1 missing). A four-sheet Lite `PRJ` is exactly what you would
expect if the **NFC document were dropped entirely** and one main-board sheet
consolidated — but that is arithmetic on a page count, not a reading of the file.
`inferred`, and it is precisely why S16 is the highest-value untaken lead in this
record.

## Things that are identical, and look as though they should not be

These are worth stating explicitly, because each one is a reasonable assumption
that is **wrong**.

- **The battery is 1150 mAh on both.** The Lite does not get a smaller cell. The
  2.3 g it saves is radio hardware, not capacity.
- **The physical dimensions are identical** — 62.0 × 101.0 × 8.0 mm product,
  113.2 × 69.6 × 21.0 mm package. Same enclosure, different colour.
- **Both pages link the *same* EasyLoader binary, and it lives under the
  PaperMono's asset folder**: `…/1267/C153-PaperMono-UserDemo_0x00.exe` — note
  **`1267`** (PaperMono), not `1268` (Lite). The Lite page has its own asset
  folder for images, the schematic and the mechanical drawing, but not for
  firmware. (S40; the file itself was not retrieved.)
- **Both pages link the same two M5Burner firmware records**, and the official
  one's API metadata reads, verbatim:

  ```json
  "firmwareName": "PaperMono UserDemo",
  "firmwareDescription": "PaperMono / PaperMono-Lite UserDemo",
  "sourceType": "OFFICIAL"
  ```

  **One image serves both SKUs** (S33). The vendor's link label for it —
  "PaperMono-Lite Factory Firmware Restoration" — is also mislabelled in the same
  way as the PaperMono's: the artifact is a demo application, not a factory-reset
  image.
- **Both pages link the same two GitHub repositories**, `M5PaperMono-UserDemo`
  (S41) and `M5PaperMono-OTP-Demo` (S42). The OTP demo's README covers both SKUs
  by name.
- **The M5GFX refresh timings are the same four numbers** — 4.71 / 0.45 / 0.34 /
  0.07 s — and **the Lite page's own caption still says "laboratory test results
  for *PaperMono*"**. The Lite figures appear to be copied rather than separately
  measured. `inferred`, and a good reason not to treat either set as a
  Lite-specific measurement.
- **The UiFlow2 tutorial is one shared page** whose title is literally
  "PaperMono / PaperMono-Lite : Flash Firmware & Run Code" (S09) — and it states
  no required firmware version, no block list and no limitations for either SKU.
- **The Arduino tutorial pages are the PaperMono's**, linked from the Lite page
  under Lite-flavoured titles (S07, S08). The power-management tutorial therefore
  documents the LoRa rail enable and the NFC enable pin to Lite readers as though
  they were theirs.

## How the two variants are actually told apart in software

This is the part with real engineering consequences, and it is established from
vendor source rather than vendor prose (S41, S47).

**M5GFX cannot distinguish them.** Its board-detection probe reads four I²C
addresses and masks the NFC bit out deliberately:

```c
static constexpr uint8_t stopwatch_i2c_addr_list[] = {
  0x32u, // RX8130
  0x68u, // BMI270
  0x15u, // Touch CST820 (for StopWatch)
  0x50u, // NFC (for PaperMono Pro)
};
const bool is_papermono = (i2c_result & ~1u) == ~0b0011u; // no CST820, with NFC == PaperMono,PaperMono Pro
```

Both variants therefore resolve to the **single enum `board_M5PaperMono`**, which
is confirmed afterwards by reading the M5PM1 and M5IOE1 device IDs. From the
graphics library's point of view there is one board.

**Only the application layer distinguishes them**, and it does so twice over:

1. **An NFC identity probe** — register **`0x7F`** is read and compared against
   expected type **`0x05`** (`main/hal/hal_board.cpp:22-23`, used at `:145`).
2. **A write-failure fallback** — the firmware powers the NFC rail through M5IOE1
   `PYG4` and, if either that write or the RGB LED is unavailable, declares the
   board `Lite`:

   ```c
   void Hal::detectBoardVariant()
       if (!_rgb_ready) { _board_variant = BoardVariant::Lite; return; }
       m5ioe1_err_t err = M5IOE1_OK;
       ioe1.digitalWriteWithRes(NFC_EN_PIN, HIGH, &err);
       if (err != M5IOE1_OK) { _board_variant = BoardVariant::Lite; return; }
   ```

**Three consequences worth planning around**, all `inferred` from source and
`not-tested`:

- **Variant detection is a negative test.** "Lite" is what the firmware concludes
  when the NFC probe *fails*. Any unrelated fault on the I²C bus, on the M5IOE1,
  or on the RGB LED path can therefore make a **full PaperMono report itself as a
  Lite**. If you branch on the variant, branch conservatively.
- **A board-enum check is not a capability check.** Code that asks M5GFX which
  board it is running on will get `board_M5PaperMono` on a Lite and may then try
  to talk to hardware that is not fitted. Probe `0x50` yourself.
- **The PlatformIO `lib_deps` difference is a build-time hint, not a guard.**
  Nothing stops a Lite build from including `M5Unit-NFC` and `RadioLib`; they will
  simply find nothing.

## The `PYG` hazard is *worse* on the Lite, not better

The naming ambiguity documented in
[`../papermono/pin-naming-and-the-pyg-ambiguity.md`](../papermono/pin-naming-and-the-pyg-ambiguity.md)
applies unchanged — the same two custom chips, the same inverted `PYG` convention
— with one twist that is specific to this variant.

The PaperMono page says the frontlight is driven by "`PYG3_BL_PWM` of the M5PM1";
**the Lite page says "`G3_WAKEin` of M5PM1"** for the identical pin. Both are
correct: the PaperMono page quotes the *net name*, the Lite page quotes the
*symbol pin name*, and the schematic shows both on M5PM1 pin 13. But a reader who
holds only the Lite page has never seen the `PYG3_BL_PWM` form, and a reader who
holds only the PaperMono page may write to **M5IOE1 IO3** — which is the e-paper
3.3 V rail enable, and cutting it stops the display silently.

On the Lite specifically:

- **`PYG4` still exists on the M5IOE1** and the vendor firmware still writes to it
  as `NFC_EN` — that write is precisely the probe that fails and identifies the
  board as a Lite. It is *not* a spare pin, and it is *not* absent.
- **M5PM1 `G2` (`PYG2_LoRa_EN`)** and **M5IOE1 `PYG2` / `PYG10`** (LoRa antenna
  switch and reset) are documented on the PaperMono pages that the Lite page links
  to. Whether those nets are still routed on the Lite PCB is **unknown** — S16 was
  not retrieved.

Use this repository's convention throughout, on both variants: **`M5PM1.G3`** for
the frontlight PWM, **`M5IOE1.IO3`** for the e-paper rail enable, and never a bare
`PYG<n>`.

## Which PaperMono documents apply unchanged

**Apply in full:**

- The five power states, every rail and enable, charging, the frontlight, and all
  wake sources — [`power-architecture.md`](../papermono/power-architecture.md),
  minus the LoRa rail.
- The ESP32-S3 pin map for everything that is not a radio: I²C on GPIO47/48,
  SPI2 to the e-paper on GPIO14–18, microSD on GPIO8–13, USB on GPIO19/20, UART0
  on GPIO43/44, PDM on GPIO45/46, buzzer on GPIO42, buttons on GPIO2/3.
- Boot, reset and download mode — including that the **M5PM1, not a button**,
  drives GPIO0, and that no separate reset button exists.
- The I²C bus and its two traps: the IP2315 charger gated off the bus behind
  M5IOE1 `IO11`, and the M5IOE1's own undocumented address.
- Every e-paper caution: the 40 MHz-versus-20 MHz clock conflict, the vendor's own
  "M5GFX waveforms are currently unstable" warning, one full refresh per ten
  partial refreshes, and the DC-imbalance damage risk.
- The mandatory octal PSRAM build setting, and the absence of an OTA partition.

**Do not apply:**

- The **LoRa** sections anywhere in this record set — SPI1 on GPIO38–41, `DIO1` on
  GPIO5, `BUSY` on GPIO21, the `U14` `Stamp-LoRa-1262-mini` connector, M5PM1 `G2`,
  M5IOE1 `IO2` and `IO10`, and the `868–923 MHz` regulatory note.
- The **NFC** sections — the `0x50` I²C device, `G6_RFID_INT` on GPIO6, the `J3`
  board-to-board connector to the NFC sub-board, schematic sheet 6, and the
  ST25R3916 component record as a *fitted part*.
- Anything derived from schematic sheet 6, and the open gap about its missing
  sheet 1/2.

**Unknown, and marked so rather than assumed:** whether the six radio-related
ESP32-S3 GPIOs, the two M5IOE1 pins and the one M5PM1 GPIO are left floating,
tied off, or repurposed on the Lite PCB. Only S16 can answer that.

## Components

The Lite carries the same parts as the PaperMono **minus the two radio
subsystems**. Records are shared; nothing below is Lite-specific silicon.

| Function | Part | Record |
|---|---|---|
| SoC | ESP32-S3R8, 8 MB octal PSRAM in package | [esp32-s3r8](../../../components/espressif/esp32-s3r8/README.md) |
| Flash | XM25UH128DHIQT, 16 MB SPI NOR | [xm25uh128dhiqt](../../../components/xmc/xm25uh128dhiqt/README.md) |
| Panel | DKE `DEPG0397BBS770F3`, 3.97" 480 × 800 | [depg0397bbs770f3](../../../components/dke/depg0397bbs770f3/README.md) |
| Display controller | Solomon Systech SSD1677 | [ssd1677](../../../components/solomon-systech/ssd1677/README.md) |
| Frontlight driver | Awinic AW9967 boost WLED driver | [aw9967](../../../components/awinic/aw9967/README.md) |
| Touch | FocalTech FT6336G, I²C `0x38` | [ft6336g](../../../components/focaltech/ft6336g/README.md) |
| Power management | M5PM1, I²C `0x6E` | [m5pm1](../../../components/m5stack/m5pm1/README.md) |
| I/O expander | M5IOE1, I²C `0x4F` | [m5ioe1](../../../components/m5stack/m5ioe1/README.md) |
| Silicon behind both | Puya PY32L020F15U6 | [py32l020f15u6](../../../components/puya/py32l020f15u6/README.md) |
| IMU | Bosch BMI270, I²C `0x68` (`0x69` accepted) | [bmi270](../../../components/bosch-sensortec/bmi270/README.md) |
| RTC | Seiko Epson RX8130CE, I²C `0x32` | record not yet written — datasheet at `components/seiko-epson/rx8130ce/artifacts/` |
| Charger | Injoinic IP2315, I²C `0x75`, gated off the bus | [ip2315](../../../components/injoinic/ip2315/README.md) |
| USB OVP load switch | Awinic AW32901FCR | [aw32901](../../../components/awinic/aw32901/README.md) |
| Main buck | Joulwatt JW5712 | [jw5712](../../../components/joulwatt/jw5712/README.md) |
| LDOs (×4) | SSP7615-33DFR | [ssp7615-33dfr](../../../components/generic/ssp7615-33dfr/README.md) |
| Load switches | Awinic AW35122FDR | [aw35122](../../../components/awinic/aw35122/README.md) |
| Bus gate / level translator | Awinic AW39112DNR | [aw39112](../../../components/awinic/aw39112/README.md) |
| Microphone | `LMD4737T261-AC02` PDM MEMS — ⚠ no datasheet found | [lmd4737t261-ac02](../../../components/generic/lmd4737t261-ac02-pdm-microphone/README.md) |
| RGB LED | `RS-C1415MBAR` — ⚠ no datasheet found; red is on/off only | [rs-c1415mbar](../../../components/generic/rs-c1415mbar-rgb-led/README.md) |
| Crystal | `CN4040M000157A530001`, 40 MHz — ⚠ no datasheet found | [crystal](../../../components/generic/cn4040m000157a530001-40mhz-crystal/README.md) |

**Not fitted on this variant:** the **ST25R3916** NFC front end and the
[Stamp LoRa-1262](../../../components/m5stack/stamp-lora-1262/README.md) module
with its **SX1262** transceiver. Component records for the ST25R3916 and the
SX1262 are **not yet written** — their datasheets are retained at
`components/stmicroelectronics/st25r3916/artifacts/` and
`components/semtech/sx1262/artifacts/` and are catalogued as S23 and S24. Those
parts describe the PaperMono; they do **not** describe this board.

> **Used By / back-link note.** Each component record above carries a **Used By**
> section naming the devices that contain it. Those sections currently name the
> **PaperMono (C153)** as the fitted board, because that is the schematic the
> parts were read from (S14). **They apply to the PaperMono-Lite (C153-Lite)
> equally**, on the strength of the vendor's own specification tables — but not on
> the strength of a Lite schematic, which has not been read. When S16 is
> retrieved, the shared components should gain an explicit `C153-Lite` mention and
> the two radio records should gain an explicit exclusion. Recorded here rather
> than edited into twenty component records on an inference.

## Availability

| Seller | SKU | Price | Stock, 2026-09-01 |
|---|---|---|---|
| shop.m5stack.com | `C153-LITE` | **USD 55.00** | Out of stock, `inventory_quantity = 0` |
| every reseller checked | — | — | **no listing found anywhere** |

The Pi Hut, OpenELAB (.io and .de), Switch Science, Adafruit, Reichelt, Botland,
Core Electronics, MakerLab, Elektor and BerryBase all returned **zero results**
for the Lite, while several of them do list the full PaperMono (S53–S55).
Whether that is a distribution decision or simply lag is **not established**.
Mouser, DigiKey and TinyTronics were bot-walled and returned no determination.

Two details worth keeping apart:

- The Lite's storefront inventory counter reads exactly **`0`**, while the
  PaperMono's reads **`−129`**. The two SKUs are in different inventory states;
  the negative is *consistent with* oversell but is not proof of it.
- **The first public sell-out report is about the Lite, not the PaperMono**:
  posted at 2026-08-21 04:09 UTC, **nine minutes** after the storefront published
  (S72). The poster went on to publish the strongest third-party project on this
  hardware (S89), which is why that ownership claim is corroborated across two
  independent surfaces.

## Community evidence specific to the Lite

There is very little, and what exists is disproportionately valuable.

- **`MagicCube/free-ink-on-paper-mono` (S89) runs on a PaperMono-Lite (C153-Lite),
  not the full board.** Its README claims a complete verified hardware path — RTC
  time from the RX8130, battery/USB/charging telemetry from the M5PM1, touch and
  physical buttons, frontlight held at 127/255, async e-ink refresh with periodic
  full cleanup, and "verified disabling of M5PM1's dangerous default single-click
  reset". Independently corroborated on that last point by
  `Free-Ink/freeink-sdk`'s `PaperMonoBoard.h` (S90). **These claims were read, not
  reproduced.** Neither citation is pinned to a commit — a recorded defect.
- **One widely repeated factual error concerns this SKU.** A launch article
  (S79) described a **$55** model with NFC and LoRa. $55 is the Lite, which has
  neither; the NFC/LoRa model is $65. If you find that claim repeated, it traces
  to a single roundup post.
- Everything else in
  [`../papermono/README.md`](../papermono/README.md#community-editorial-and-project-coverage)
  applies: zero written reviews, one hands-on video, and the real signal being
  code rather than articles.

## Should you buy the Lite instead?

**Yes, unless you specifically need the radios.** That is the whole calculus, and
it is unusually clean because the vendor has changed exactly one thing:

- **Take the Lite** if you want an e-paper platform with a frontlight, touch, an
  IMU, an RTC, a microphone, microSD and a genuinely hardware-level low-power
  architecture. You save USD 10 and 2.3 g and lose nothing else — same SoC, same
  panel, same battery, same enclosure, same firmware image.
- **Take the PaperMono** if NFC or LoRa is load-bearing. USD 10 for an ST25R3916
  and an SX1262 module is a good price for both, and they cannot be added
  afterwards: **there is no expansion connector on either board.** Every GPIO is
  committed, and the only route in is the shared I²C bus.
- **Take neither** for a reading device or a fast/high-fidelity display. Four grey
  levels, 480 × 800, and the vendor's own conservative refresh guidance apply
  equally to both. The [PaperS3 comparison](../papermono/README.md#product-history-family-and-culture)
  is the one that matters, and it is a trade rather than an upgrade.

The Lite's *positioning* differs too, and the vendor is explicit about it: the
PaperMono's application list leads with access control and identity
authentication — radio applications — while the Lite's leads with electronic
shelf labels, information displays and low-power IoT nodes. That is a coherent
split, not marketing noise.

## Gaps specific to this record

- **The Lite schematic (S16) was not retrieved.** It is the only thing that can
  establish what the board actually omits rather than what the comparison table
  says it omits, whether the radio nets are still routed, and what the two "extra"
  PaperMono sheets contained. **The single highest-value action for a follow-up
  pass.**
- **The Lite mechanical drawing (S17) was not retrieved.** The identical outline
  dimensions are a marketing claim, not a measurement.
- **No Lite-specific measurement of anything exists** — not refresh timing (the
  published numbers are captioned as PaperMono results), not power, not battery
  life. This is the same gap the PaperMono has, compounded.
- **No product or teardown photograph** is held. The vendor's imagery is not
  licensed for redistribution and no independent teardown existed at the snapshot
  date.
- **The 2.3 g delta is the only quantitative evidence** that the radio hardware is
  genuinely absent rather than depopulated. It is good evidence and it is not
  proof.
- **No certification identifier** exists for this SKU (S11). Less consequential
  than for the PaperMono, since the Lite ships no radio beyond the ESP32-S3's own
  2.4 GHz — but still unpublished.

## Related

- [PaperMono (C153)](../papermono/README.md) — **the full record; read it first**
- [PaperMono sources](../papermono/sources.md) · [research log](../papermono/research-log.md) · [command ledger](../papermono/commands.md)
- [Devices index](../../README.md) · [Components index](../../../components/README.md)
