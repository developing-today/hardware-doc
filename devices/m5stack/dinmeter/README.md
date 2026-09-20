# M5Stack DinMeter (SKU K134)

> **Product ID** `K134` · **PCB/board revision** not printed on any published document — the
> published schematic is titled `DIN_Meter_v1.0` · **Region** single worldwide SKU ·
> **Status** superseded by [DinMeter v1.1 (K134-V11)](../dinmeter-v1.1/README.md) and no longer
> listed on `shop.m5stack.com` (verified 2026-09-04) · **Research retrieval date** 2026-09-04

A 1/32-DIN panel-cutout instrument head: a bright **orange rotary encoder knob** over a 1.14 in
135 × 240 IPS LCD, on a carrier board that accepts 6–36 V DC, charges a Li-ion cell, keeps time
with a battery-backed RTC and exposes two Grove ports. The compute is not on the carrier: it is
an [M5Stamp-S3](../../../components/m5stack/stamp-s3/README.md) module soldered as `M1`.

This record covers **K134, the original**. The revision that replaced it is documented
separately at [`devices/m5stack/dinmeter-v1.1/`](../dinmeter-v1.1/README.md); read
[§ Why two records](#why-two-records-and-not-one-or-three) before assuming they differ more than
they do.

---

## Evidence labelling

Every consequential claim below carries one of these markers. Nothing is asserted from a
candidate list or a near-miss part number.

| Marker | Meaning | Evidence status |
|---|---|---|
| **[SCH]** | Read out of `K134_DIN_Meter_v1.0-schematic.pdf` by parsing Altium's invisible `CO`/`PI`/`NL` marker layer plus the visible text, cited by designator | `executed-success` for the extraction; `not-tested` electrically |
| **[SRC]** | Read out of vendor or framework source at a cited `file:line` | `executed-success` for the read; `not-tested` on hardware |
| **[DOC]** | `docs.m5stack.com` / `shop.m5stack.com`, retrieved 2026-09-04 | `not-tested` |
| **[COM]** | Community source, non-authoritative | as stated per item |
| **[INF]** | Inference, with the reasoning given | `inferred` |

**No hardware was in hand for this pass.** Nothing below is `executed-success` on the device
itself. Where a command is given it is labelled.

---

## Identity and variants

| Property | Value | Evidence |
|---|---|---|
| Marketed name | **DinMeter** (the docs page id is `M5DinMeter`; the page title is `DinMeter`) | **[DOC]** |
| SKU | **K134** | **[DOC]** page header `SKU:K134`; **[SRC]** `m5stack/M5_Hardware` path `Products/K134_DinMeter/` |
| Documentation URL | <https://docs.m5stack.com/en/core/M5DinMeter> | **[DOC]** HTTP 200 |
| ⚠ Path trap | `https://docs.m5stack.com/en/core/DinMeter` returns **HTTP 404** — the obvious guess is wrong | **[DOC]** verified 2026-09-04 (negative control) |
| Core module fitted | **Stamp-S3**, schematic symbol `STAMP-S3-SMD`, designator `M1`, 31 pads | **[SCH]** |
| Display controller | **ST7789V2** | **[DOC]** specification row; datasheet mirrored by M5Stack |
| Successor | DinMeter v1.1, SKU `K134-V11`, Stamp-S3A + ST7789P3 | **[DOC]** |
| Regional/bundle variants | **None found.** One SKU, one bundle | **[DOC]** |
| PCB revision markings | **Not established.** No teardown photograph of the silkscreen was inspected in this pass; the schematic PDF is titled `DIN_Meter_v1.0` and that is the only revision string published | **[SCH]**, **[INF]** for the gap |

### Bundle contents

1 × DinMeter, 1 × adhesive tape, 1 × 250 mAh polymer Li-ion battery, 1 × silk-screened sticker,
1 × DC-JACK terminal input (6–36 V), 1 × back bracket. **[DOC]**

---

## Why two records, and not one or three

The evidence for "how different is v1.1?" is unusually blunt, and it points the opposite way
from what two SKUs and two documentation pages suggest:

| Asset | v1.0 (K134) | v1.1 (K134-V11) | SHA-256 |
|---|---|---|---|
| Schematic PDF | `.../500/DIN_Meter_v1.0.pdf` | `.../1211/K134-V11_DIN_Meter_v1.0_2025_11_25_17_15_58.pdf` | **identical** — `03ec3353…6e4c070` |
| Structure/STL | `Products/K134_DinMeter/…/DinMeter.stl` | `Products/K134-V11_DinMeter_v1.1/…/DinMeter_v1.1.stl` | **identical** — `90f04d6a…4aef00fbf7` |
| Full GPIO PinMap | 12 signals | 12 signals | **identical assignments** |

Two different URLs, two different filenames, the same bytes. M5Stack has published **no
v1.1-specific schematic and no v1.1-specific mechanical model** — it re-served the v1.0 files
under v1.1 names. **[SCH]** **[SRC]**

So the honest structure is: **one full record (this one) plus a scoped revision record.**
Writing a second full record would mean asserting differences the published evidence does not
support. The revision record documents what genuinely changed — the core module, the display
controller part number, and the consequences of both — and links here for everything shared.

---

## What it is and visual identification

Front: a **matte-orange knurled rotary knob** occupying roughly the left third of the face,
with the 1.14 in landscape LCD to its right behind a rectangular window. The knob is the single
most identifiable feature and the reason the device is recognisable from a thumbnail; no other
M5Stack product pairs an orange knob with a DIN-cutout body. Body is dark grey/black plastic,
53.0 × 30.0 × 32.0 mm, 17.8 g. **[DOC]**

Rear: USB-C at one end, a 2-pin green screw terminal for 6–36 V DC, two HY2.0-4P Grove sockets
(PORT.A red / PORT.B black), a 1.25 mm 2-pin JST battery socket, and a removable plastic back
clip for mounting.

Panel face: the 1/32 DIN standard cutout is **45 × 22.5 mm**. **[DOC]** That is the whole point
of the industrial-design decision — it drops into an existing instrument panel, PLC cabinet or
control box aperture with no bracket and no filing.

See [`media.md`](media.md) for the retained images with full provenance.

---

## Product history, family and culture

| Date | Event | Evidence |
|---|---|---|
| 2024-02-21 | `m5stack/M5DinMeter` Arduino library repository created — earliest dated artefact | **[SRC]** GitHub API `created_at` |
| 2024-03-01 | `m5stack/M5DinMeter-UserDemo` repository created | **[SRC]** |
| 2024-03-04 | UserDemo release `V0.1` published (the factory-firmware source) | **[SRC]** |
| 2024-03-07 | M5DinMeter library release `1.0.0`; all six bundled examples dated `2024-03-07` | **[SRC]** |
| 2026-01-30 | **DinMeter v1.1 announced.** Shop listing `created_at 2026-01-30T10:02:16+08:00`; r/M5Stack weekly-new-products post the same day | **[DOC]** **[COM]** |
| 2026-08-03 | Last push to `m5stack/M5DinMeter` (library still `1.0.0`, no new release) | **[SRC]** |
| 2026-09-04 | K134 absent from `shop.m5stack.com` search; only `m5stack-din-meter-v1-1-with-m5stamps3a` is listed | **[DOC]** |

**Family.** The DinMeter is the flat, panel-mount member of a small M5Stack cluster that shares
a single M5Unified code path: `board_M5Dial`, `board_M5DinMeter` and `board_M5Capsule` appear in
the *same switch cases* for button reading, buzzer configuration and power-hold. **[SRC]**
`M5Unified/src/M5Unified.cpp:3500-3506`, `:2921-2929`, `:2398-2402`. The M5Dial is the round
one; the DinMeter is the rectangular DIN one; the AirQ is the boxy sensor one. All are Stamp-S3
carriers. The `M5DinMeter.h` header guard is literally `#define M5DIAL_H` and its pin macros are
named `DIAL_ENCODER_PIN_A/B` — the library was copied from M5Dial and the lineage was never
cleaned up. **[SRC]** `M5DinMeter/src/M5DinMeter.h:1,8-9`.

**Culture.** There barely is one. See [`projects-and-community.md`](projects-and-community.md):
a broad search found **five** third-party GitHub repositories naming the device and **one**
relevant Reddit post in the whole of `old.reddit.com`. This is a quiet, professional-niche
product, not a maker phenomenon.

---

## Key specifications

Each functional part links to its component record.

| Specification | Parameter | Component record | Evidence |
|---|---|---|---|
| Core module | **M5Stamp-S3** (`STAMP-S3-SMD`, `M1`) | [`components/m5stack/stamp-s3`](../../../components/m5stack/stamp-s3/README.md) | **[SCH]** **[DOC]** |
| SoC | **ESP32-S3FN8**, Xtensa LX7 dual-core @ 240 MHz | [`components/espressif/esp32-s3r8`](../../../components/espressif/esp32-s3r8/README.md) (same silicon family; **`FN8` = 8 MB in-package flash, no PSRAM**) | **[DOC]** |
| Flash | 8 MB, in-package | ↑ | **[DOC]** |
| PSRAM | **None.** `FN8` has no in-package PSRAM and none is fitted on either board | ↑ | **[DOC]** **[SCH]** (no PSRAM designator in the 84-part census) |
| Wi-Fi / BLE | 2.4 GHz Wi-Fi + Bluetooth 5 LE (SoC), 3D antenna on the module | [`stamp-s3`](../../../components/m5stack/stamp-s3/README.md) | **[DOC]** |
| Display | 1.14 in IPS, **135 × 240**, **ST7789V2**, SPI, 8-pin 0.5 mm FPC (`FPC1`, `FPC-0.5-8P`) | [`components/sitronix/st7789v2`](../../../components/sitronix/st7789v2/README.md) | **[DOC]** **[SCH]** |
| Backlight switch | **AW35122FDR** load switch (`U6`), gate = `LCD_BL` | [`components/awinic/aw35122`](../../../components/awinic/aw35122/README.md) | **[SCH]** |
| Rotary encoder | Incremental quadrature + push switch, on connector `J5` — **part number not published** | [`components/unidentified/m5stack-dinmeter/rotary-encoder`](../../../components/unidentified/m5stack-dinmeter/rotary-encoder/README.md) | **[SCH]** |
| RTC | **BM8563** (`U5`), I²C 0x51, 32.768 kHz `Y2` ±20 ppm 12.5 pF | [`components/generic/bm8563`](../../../components/generic/bm8563/README.md) | **[SCH]** **[DOC]** |
| Buzzer | Magnetic buzzer `LS1`, driven by `Q5` SS8050 NPN + `R25` 470 Ω, flyback `D6` 1N4148WT — **part number not published** | [`components/unidentified/m5stack-dinmeter/buzzer`](../../../components/unidentified/m5stack-dinmeter/buzzer/README.md) | **[SCH]** |
| Wide-input DC-DC | **ME3116AM6G** (`U1`), 6–36 V → +5VIN, `L1` 10 µH, FB `R5` 56 kΩ / `R6` 10 kΩ | [`components/microne/me3116am6g`](../../../components/microne/me3116am6g/README.md) | **[SCH]** |
| Battery charger | **TP4057** (`U2`), linear Li-ion, `R13` 3.3 kΩ programme resistor | [`components/generic/tp4057`](../../../components/generic/tp4057/README.md) | **[SCH]** **[DOC]** |
| Battery boost | **SY7088** (`U3`), boost to +5VOUT, `L4` 1.5 µH, FB `R16` 52.3 kΩ / `R18` 15 kΩ | [`components/silergy/sy7088`](../../../components/silergy/sy7088/README.md) | **[SCH]** |
| 3.3 V LDO | **BL8075CB5TR33** (`U4`) → +3.3V | [`components/belling/bl8075`](../../../components/belling/bl8075/README.md) | **[SCH]** |
| Reset supervisor | **CN809J** (`U7`) on +5VIN | see [`pinouts-and-buses.md`](pinouts-and-buses.md) §Power | **[SCH]** |
| USB | ESP32-S3 native USB OTG / Serial-JTAG, USB-C on the Stamp module | [`stamp-s3`](../../../components/m5stack/stamp-s3/README.md) | **[DOC]** **[SCH]** |
| DC input | **6 – 36 V**, 2-pin 2.54 mm screw terminal `J1`, reverse/clamp `D13`+`D12` B5819W | [`pinouts-and-buses.md`](pinouts-and-buses.md) | **[DOC]** **[SCH]** |
| Charge current | 100 mA | **[DOC]** |
| Grove load | PORT.A 5 V @ 220 mA max; PORT.B 5 V @ 220 mA max | **[DOC]** |
| Standby current | DC 4.2 V @ **38.4 µA** (battery power, latched off) | **[DOC]** |
| Battery socket | 1.25 mm 2-pin (`J2`) | **[DOC]** **[SCH]** |
| Power sources | USB / DC terminal / Li-ion battery | **[DOC]** |
| Operating temperature | 0 – 40 °C | **[DOC]** |
| Size / weight | 53.0 × 30.0 × 32.0 mm / 17.8 g; panel cutout 45 × 22.5 mm (1/32 DIN) | **[DOC]** |

The specification table is the vendor's; the *component* column is not. Every part number in it
was read off the schematic, matched to a designator, and cross-checked against the value text
printed beside that designator. The full census is in
[`artifacts/schematic/K134_DIN_Meter_v1.0-designator-value-census.txt`](artifacts/schematic/K134_DIN_Meter_v1.0-designator-value-census.txt).

---

## Architecture and components

The board is a **three-rail power tree feeding a single Stamp-S3 module**, with a latching
power switch that the firmware must hold on.

```
 J1 6–36 V ──D13/D12──► U1 ME3116AM6G buck ──► +5VIN ──┬──► U7 CN809J supervisor (RESET)
 (screw terminal)                                       │
                                                        ├──► M1 pin13 "5V"  (Stamp-S3 VIN_5V)
 USB-C (on Stamp) ──────────────────────────────────────┘
                                                             Stamp-S3 internal:
 J2 Li-ion 1.25-2P ──► U2 TP4057 charger ──► VBAT_OUT ──►      MUN3CAD01-SC → VDD_3V3
                          U3 SY7088 boost ──► +5VOUT ──► J3/J4 Grove 5 V rails
                          U4 BL8075CB5TR33 ──► +3.3V   ──► U5 RTC, pull-ups, FPC1 LCD
 Q3/Q6 AP40P05 P-FETs + Q4 LN2324DT2AG  =  battery power path / HOLD latch (G46)
```

**Power latch.** `HOLD` is `M1` pin 27 = **GPIO46**. **[SCH]** With no USB present, the board is
held on only while GPIO46 is high; the wake sources are the encoder push-button (`WAKE`,
GPIO42) and the RTC `INT` line. Drive GPIO46 low, or press RST, and the board disconnects the
battery. This is the single most important thing to know before writing firmware — see
[`features/power-and-battery.md`](features/power-and-battery.md).

**Two I²C buses, not one.** The RTC sits on an *internal* bus (GPIO11/12) that is **not** the
Grove PORT.A bus (GPIO13/15). **[SRC]** `M5Unified/src/M5Unified.cpp:96`. A Grove I²C unit
cannot collide with the RTC.

**GPIO38 and GPIO21 are inside the module.** Neither is broken out on the Stamp-S3's 23 IO pins,
and neither appears on the DinMeter schematic. GPIO38 drives the Stamp's LCD-FPC backlight
switch and GPIO21 drives its WS2812B RGB LED. **[SCH]** `Sch_M5StampS3_v0.2` `U1` pins 43 and
27. This matters enormously for the v1.1 delta — see
[`../dinmeter-v1.1/README.md`](../dinmeter-v1.1/README.md).

Full wiring table: [`pinouts-and-buses.md`](pinouts-and-buses.md).
Contention analysis: [`resources-and-conflicts.md`](resources-and-conflicts.md).

---

## Common tasks / How do I...?

| I want to… | Guide |
|---|---|
| Read the orange knob and its push-button | [`features/rotary-encoder-and-buttons.md`](features/rotary-encoder-and-buttons.md) |
| Draw on the 135 × 240 screen, set brightness | [`features/display.md`](features/display.md) |
| Keep time across power-off, wake on a schedule | [`features/rtc-and-timekeeping.md`](features/rtc-and-timekeeping.md) |
| Make it beep | [`features/buzzer.md`](features/buzzer.md) |
| Run it from 24 V, or from the battery, and not have it switch itself off | [`features/power-and-battery.md`](features/power-and-battery.md) |
| Hang an I²C sensor or a GPIO peripheral off the Grove ports | [`features/porta-portb-expansion.md`](features/porta-portb-expansion.md) |
| Get Wi-Fi or BLE up | [`features/wifi-and-ble.md`](features/wifi-and-ble.md) |
| Mount it in a panel / on DIN rail | [`features/din-mounting-and-mechanical.md`](features/din-mounting-and-mechanical.md) |
| Blink the RGB LED (and why it may not work on v1.1) | [`features/rgb-led.md`](features/rgb-led.md) |
| Build and flash anything at all | [`development.md`](development.md) |
| Put the factory firmware back | [`factory-firmware.md`](factory-firmware.md) |

---

## Common uses and representative projects

Demonstrated, with running code (**[COM]**, each a firsthand project by its author):

- **`no-body-in-particular/m5din-hikoki`** (★25, C++, last push 2026-05-05) — a HiKOKI power-tool
  battery analyser. The most-starred DinMeter project found anywhere.
- **`Shark17e/M5DinMeter-KilnController`** (★1, C++, 2026-08-08) — ceramic-kiln PID controller
  with auto-correction. Exactly the panel-instrument use case the form factor is for.
- **`TuF3i/DinMeterDock`** (C, 2026-06-27) — a desktop dock controller.
- **`kaz-mac/M5Authenticator`** — TOTP authenticator with a dedicated `DinMeterUI.h`.
- **`aoiastro/susuFW`** — a multi-function firmware for the DinMeter.
- **`bmorcelli/Launcher` / BruceDevices "Bruce"** — the DinMeter appears as a build target in
  the Bruce pentest-firmware CI matrix.

Vendor-intended, from the product page: smart-home monitoring and control, access control,
industrial control, maker/DIY. **[DOC]**

Full catalogue with lineage and disposition: [`projects-and-community.md`](projects-and-community.md).

---

## Distinctive strengths

- **The 1/32 DIN cutout is the product.** 45 × 22.5 mm is a real, existing aperture size in
  installed panels. Nothing else in the ESP32 hobby/prosumer space drops into one.
- **6–36 V input on-board.** No brick, no buck module glued to the back. A 24 V PLC cabinet
  rail feeds it directly.
- **A knob with real detents on a device that also has a battery, an RTC and a screen.** The
  combination is what makes it a *meter* rather than a display.
- **Genuinely low standby** — 38.4 µA latched off on battery **[DOC]**, because the latch cuts
  the battery rather than sleeping the SoC.
- **First-class framework support.** M5Unified has a `board_M5DinMeter` enum member with I²C,
  Grove, buzzer, button, RGB and power-hold table entries. **[SRC]** Espressif's own
  `esp-board-manager` ships a complete `m5stack_dinmeter` board definition. **[SRC]**

## Shortcomings and constraints

- **No PSRAM.** ESP32-S3FN8. Anything wanting a large LVGL framebuffer, a camera or a big TLS
  heap will feel it. **[DOC]**
- **Only 8 usable free GPIOs**, and four of them are the two Grove ports. The 23 Stamp IOs are
  mostly consumed: display 6, encoder 2, RTC 2, buzzer 1, button 1, hold 1, battery ADC 1.
- **The power latch is a footgun.** Fail to raise GPIO46 in `setup()` and the device dies the
  moment you release the knob. Every first-time user hits this. **[DOC]** documents it; nothing
  enforces it.
- **The Arduino library is a thin M5Dial copy** with a stale header guard and no release since
  `1.0.0` (2024-03-07). **[SRC]**
- **Documentation is inconsistent about the Grove wire colours** — see
  [`gaps-and-conflicts.md`](gaps-and-conflicts.md) §1.
- **0–40 °C operating range** rules out unheated outdoor cabinets. **[DOC]**
- **The rotary encoder part number is not published**, so a replacement knob/encoder cannot be
  sourced from the documentation alone.
- **K134 is discontinued.** New units are v1.1 only.

---

## Performance summary

There are **no independent benchmarks of this device**, and none were produced in this pass. What
exists is the vendor's two power figures and the silicon's headline numbers. Treat everything
else as unmeasured. Details, method notes and what would need measuring:
[`performance.md`](performance.md).

---

## Pricing and availability

| Date | Region | Seller | Item | Price | Status |
|---|---|---|---|---|---|
| 2026-09-04 | Global | shop.m5stack.com | **DinMeter (K134)** | — | **Not listed.** Shop search for "din meter" returns only the v1.1 SKU |
| 2026-09-04 | Global | shop.m5stack.com | DinMeter v1.1 (K134-V11) | **USD 24.50** | In stock |

Full observations, competitor prices, and the caveats: [`market-and-pricing.md`](market-and-pricing.md).

---

## Competitors, equivalents and clones

Detailed treatment — including the **Waveshare ESP32-S3-Knob-Touch-LCD-1.8** already documented
in this repository, the M5Dial, and a roll-your-own encoder+ESP32 build — is in
[`comparisons-and-recommendations.md`](comparisons-and-recommendations.md). Short version: the
Waveshare is a better *knob*, the M5Dial is a better *dial*, and neither fits a 1/32 DIN
aperture or takes 36 V.

No clones of the DinMeter were found on AliExpress or elsewhere in this pass. **[INF]** — that
is a negative search result, not proof of absence; see [`research-log.md`](research-log.md).

---

## Launch-era versus current market fit

**2024 (launch).** Nothing else offered a DIN-cutout ESP32-S3 head with a knob at any price. The
comparison set was "build it yourself" or "buy an industrial HMI at 10×". Strong fit.

**2026 (now).** Still essentially uncontested on the *form factor*, but the SKU you can actually
buy is v1.1. If your reason for choosing it is the cutout and the 6–36 V input, it remains the
only sensible answer. If your reason is "a knob with a screen", the field has widened
considerably and the DinMeter is neither the cheapest nor the nicest. See
[`comparisons-and-recommendations.md`](comparisons-and-recommendations.md).

## When to use / when not to use

**Use it when:** you have a 1/32 DIN aperture; you have 12/24 V available and no 5 V; you want a
detented knob as the primary input; you need timekeeping across power loss; you are building a
setpoint/monitor head rather than a general computer.

**Do not use it when:** you need PSRAM, a camera, more than ~8 free GPIOs, an operating range
outside 0–40 °C, a touchscreen, or a display larger than 1.14 in. Do not use it as a *first*
ESP32 board — the power latch will bite.

## Alternatives by tier

See [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) § Alternatives by
tier, which is dated and scoped by workload rather than repeated here.

---

## Images and teardown/PCB views

Ten official product images retained with full provenance; **no teardown or bare-PCB photograph
of the DinMeter was located in this pass** — a real gap, recorded as such. See
[`media.md`](media.md) and [`media/manifest.json`](media/manifest.json).

---

## Community, editorial and project coverage

[`projects-and-community.md`](projects-and-community.md) — including the searched-and-empty
results, which are findings in their own right.

---

## Documentation map

| File | What is in it |
|---|---|
| [`pinouts-and-buses.md`](pinouts-and-buses.md) | Every net, every Stamp pad, cited to schematic designator or `file:line` |
| [`development.md`](development.md) | Arduino / ESP-IDF / UiFlow2 / MicroPython, with honest command status |
| [`factory-firmware.md`](factory-firmware.md) | What ships on it, where the source is, how to restore |
| [`features/`](features/README.md) | Nine task-oriented guides |
| [`coverage.md`](coverage.md) | Feature → hardware → docs → example → guide → test status |
| [`resources-and-conflicts.md`](resources-and-conflicts.md) | GPIO/bus/timer/peripheral contention |
| [`compatibility-and-status.md`](compatibility-and-status.md) | Working / partial / untested, keyed by revision and library version |
| [`gaps-and-conflicts.md`](gaps-and-conflicts.md) | **Read this.** Four documented source conflicts |
| [`sources.md`](sources.md) | Full source table with class, dates and what each establishes |
| [`research-log.md`](research-log.md) | Every query, including the ones that found nothing |
| [`commands.md`](commands.md) | Command ledger with execution status |
| [`market-and-pricing.md`](market-and-pricing.md) | Dated, normalised price observations |
| [`performance.md`](performance.md) | What is known, what is not, and what to measure |
| [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) | vs Waveshare knob, M5Dial, DIY |
| [`projects-and-community.md`](projects-and-community.md) | Every project, repo, port and forum trace found |
| [`media.md`](media.md) | Image provenance |
| [`examples/`](examples/best.md) | Example survey, catalogue and selection |
| [`acquisition/`](acquisition/README.md) | Clean-clone reacquisition, machine-readable manifest |

## Artifact layout

```
devices/m5stack/dinmeter/artifacts/
├── schematic/
│   ├── K134_DIN_Meter_v1.0-schematic.pdf            433 658 B  03ec3353…  ← primary evidence
│   ├── K134_DIN_Meter_v1.0-schematic.bbox.xml        73 682 B  parsed marker layer
│   ├── parse_dinmeter_sch.py                          3 198 B  the parser (re-runnable)
│   ├── K134_DIN_Meter_v1.0-designator-value-census.txt          85 designators → values
│   ├── K134_DIN_Meter_v1.0-designator-census.txt               full CO/PI/NL census + gaps
│   ├── K134_DIN_Meter_v1.0-plaintext-layout.txt                sheet as readable rows
│   └── M1-stamp-s3-pinout-from-schematic.txt                   all 31 Stamp pads
├── mechanical/
│   ├── K134-din_meter_asm_v1-dimensions.pdf         117 405 B  db42c8a9…
│   └── DinMeter.stl                                 573 284 B  90f04d6a…  (= v1.1's file)
├── docs/
│   ├── docs-en-core-M5DinMeter.pdf → archive/…      7 459 888 B  8b3db00a…  ARCHIVED
│   ├── docs-en-core-M5DinMeter.pdf.ARCHIVED.md        placeholder (recovery URLs, hash)
│   └── docs-en-core-M5DinMeter.txt                    5 214 B  extracted page text
└── source-snapshots/
    ├── M5DinMeter-8ccbad72….tar.gz                    8 532 B  Arduino library @ HEAD
    ├── M5DinMeter-UserDemo-d2fdfe44….tar.gz          74 231 B  factory-firmware source
    └── dinmeter-board_{info,devices,peripherals}.yaml          Espressif esp-board-manager
```

Chip datasheets are **component** artifacts and live under `components/<vendor>/<part>/artifacts/`,
not here — see the key-specification table for the links.

## Known conflicts and unresolved identities

Four, all documented with evidence and with what would settle them, in
[`gaps-and-conflicts.md`](gaps-and-conflicts.md):

1. **PORT.A / PORT.B wire colours.** The vendor PinMap and the schematic + M5Unified imply
   opposite yellow/white assignments. Unresolved.
2. **`S1`, `R20`, `Y1`** appear as visible designator text on the schematic with no recoverable
   `CO`/`PI` marker. Partly an extraction limit, partly possibly real.
3. **v1.1 assets are v1.0 assets.** Byte-identical schematic and STL under v1.1 filenames.
4. **Stamp-S3A "DC-DC: MUN3CAD01-SC"** is contradicted by the v0.3.3 schematic, which contains
   no such string. Carried into the [Stamp-S3A record](../../../components/m5stack/stamp-s3a/README.md).

---

*Researched 2026-09-04. No hardware in hand. Vendor documentation, published Altium schematics,
vendor and framework source, and a broad public-source sweep; see
[`research-log.md`](research-log.md) for depth and exclusions.*
