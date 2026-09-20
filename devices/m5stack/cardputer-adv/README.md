# M5Stack Cardputer ADV (K132-Adv)

> **SKU `K132-Adv`** · M5Stack CMS product id **`1178`** · Shopify product `8904041857281`
> Board revision on the published schematic: **`Sch_M5CardputerAdv_v1.0`, dated 2025-06-20**
> Status **in production** (the v1.1 it replaces is marked `[EOL]` on M5Stack's own store)
> Research snapshot **2026-09-04** · vendor library `M5Cardputer` at `f1392858` · `M5Unified` at `8530f537` · `M5GFX` at `d91077b9`

The Cardputer ADV is the third mainboard in M5Stack's card-sized ESP32-S3 computer line and
the first that is a genuinely different *board*, not just a different plug-in module. It keeps
the 84 × 54 mm card format, the 56-key keyboard and the 1.14″ 240 × 135 LCD, and changes
almost everything behind them: an I²C keypad scanner instead of a GPIO matrix, a real audio
codec instead of a bare I²S amplifier, an IMU, a 3.5 mm jack, a single large battery, and a
14-pin expansion header — the **CAP bus** — that turns the underside of the device into a
module socket.

**The single most consequential fact for software:** the ADV frees **seven GPIOs**
(G3, G4, G5, G6, G7, G13, G15) that on every earlier Cardputer were consumed by the keyboard
matrix, and spends **two** (G8, G9) to gain an internal I²C bus. Those seven pins are what
the CAP header is made of.

---

## Common tasks / How do I…?

| Question | Answer |
|---|---|
| **What changed versus the v1.1?** | [§ Generation-to-generation delta](#generation-to-generation-delta) · [`product-history-and-family.md`](product-history-and-family.md) |
| **How does the keyboard work?** | [`features/keyboard.md`](features/keyboard.md) — full matrix, TCA8418 config, the remap maths |
| How do I drive the display? | [`features/display.md`](features/display.md) |
| How do I play sound / record audio? | [`features/audio.md`](features/audio.md) — **read the shared-codec warning** |
| How do I use the microSD card? | [`features/microsd.md`](features/microsd.md) |
| How do I read the IMU? | [`features/imu.md`](features/imu.md) |
| How do I read battery voltage / charge safely? | [`features/battery-and-power.md`](features/battery-and-power.md) |
| How do I use Wi-Fi and BLE? | [`features/wifi-and-ble.md`](features/wifi-and-ble.md) |
| How do I send IR? | [`features/ir.md`](features/ir.md) |
| How do I use the Grove / PORT.A connector? | [`features/grove-port.md`](features/grove-port.md) |
| **How do I build my own CAP board?** | [`features/cap-header.md`](features/cap-header.md) — pinout, three conflicting numbering schemes, electrical limits |
| How do I use USB / act as a HID keyboard? | [`features/usb.md`](features/usb.md) |
| Is there an RTC? | [`features/rtc.md`](features/rtc.md) — **no**, and what to do instead |
| What pin is what? | [`pinouts-and-buses.md`](pinouts-and-buses.md) |
| What fights with what? | [`resources-and-conflicts.md`](resources-and-conflicts.md) |
| How do I flash it / recover it? | [`development.md`](development.md) · [`factory-firmware.md`](factory-firmware.md) |
| **Which community firmware works on ADV?** | [`projects-and-community.md`](projects-and-community.md) · [`compatibility-and-status.md`](compatibility-and-status.md) |
| What does it cost? | [`market-and-pricing.md`](market-and-pricing.md) |
| Should I buy this or a T-Deck / Tanmatsu? | [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) |
| What is unresolved or contradictory? | [`gaps-and-conflicts.md`](gaps-and-conflicts.md) |
| Where did all this come from? | [`sources.md`](sources.md) · [`research-log.md`](research-log.md) · [`commands.md`](commands.md) |

---

## Identity and variants

| Field | Value | Evidence |
|---|---|---|
| Marketed name | **Cardputer-Adv** (docs) / **M5Stack Cardputer Adv Version (ESP32-S3)** (store) | S1, S9 |
| SKU | `K132-Adv` | S1 |
| CMS product id | `1178` | asset URLs on S1 |
| Shopify id / handle | `8904041857281` / `m5stack-cardputer-adv-version-esp32-s3` | S9 |
| Schematic revision | `Sch_M5CardputerAdv_v1.0`, file-stamped `2025_06_20_17_19_58` | A1 |
| Core module | **Stamp-S3A**, schematic `Sch_StampS3_v0.3.3` | S1, A2 |
| Colour variants | Standard (orange/black); **green back shell** version is exclusive to the Cardputer Mesh Kit (K152) | S4 |
| Regional variants | None found. No FCC/CE/TELEC identifier published — see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) | — |

There is **one** ADV mainboard SKU. `K132-Adv` and `K152` (Mesh Kit) contain the same board;
the kit adds a Cap LoRa-1262, an antenna, screws and a Meshtastic registration entitlement.

---

## Generation-to-generation delta

This is the table the rest of the record exists to justify. Everything in it is from a
schematic, a rendered schematic sheet, or vendor board-support source — not from marketing
copy. "v1.x" means v1.0 and v1.1 together, because **their published schematics are the same
file** (see below).

| Subsystem | Cardputer v1.0 (K132) | Cardputer v1.1 (K132-V11) | **Cardputer ADV (K132-Adv)** | Evidence |
|---|---|---|---|---|
| Core module | **StampS3** (`Sch_M5StampS3_v0.2`) | **Stamp-S3A** (`Sch_StampS3_v0.3.3`) | **Stamp-S3A** (same file as v1.1) | S1, S2, S3, A2, A5 |
| SoC | ESP32-S3FN8 | ESP32-S3FN8 | ESP32-S3FN8 | A2, A5 |
| Flash / PSRAM | 8 MB in-package / **none** | 8 MB / **none** | 8 MB / **none** — unchanged | A2, A5, S1 |
| **Keyboard scanner** | **74HC138** 3-to-8 decoder, 8 drive + 7 sense GPIOs | 74HC138, identical | **TCA8418RTWR** I²C keypad scanner @ `0x34`, 3 GPIOs | A1 sheet 2, A3 sheet 2, S1 |
| Keyboard matrix wiring | 8 × 7, nets `Y0..Y7` via R27–R34 22 Ω | identical | **identical 8 × 7 matrix, identical `Y0..Y7` nets, identical R27–R34 22 Ω** | A1, A3 |
| GPIOs freed / spent | — | — | **frees G3,G4,G5,G6,G7,G13,G15; spends G8,G9,G11** | M5GFX comment block, A1 |
| Internal I²C bus | **none** | none | **SDA G8 / SCL G9**, 3.3 kΩ pull-ups R36/R37 | A1 sheet 2, M5Unified `_pin_table_i2c_ex_in` |
| Display | ST7789V2 1.14″ 240×135 | same | same | S1–S3 |
| Backlight / RGB LED rail | WS2812 on **always-on `VDD_3V3`** | WS2812 on **`BL_3V3`**, gated by AW35122FDR from `DISP_BL` (G38) | same as v1.1 | A5 vs A2, S2 |
| Audio out | NS4168 I²S class-D → cavity speaker | same | **ES8311 codec** @ `0x18` + **NS4150B** amp → speaker **and 3.5 mm jack** | A1 sheet 3, S1 |
| Audio in | **SPM1423** PDM MEMS mic | same | **MSM381A3729H9BP analog MEMS mic** → ES8311 ADC | A1 sheet 3, A3 |
| 3.5 mm jack | none | none | **yes** (PJ-342), with `HP_DET`; inserting a plug mutes the speaker amp | A1 sheet 3, S1 |
| IMU | none | none | **BMI270** @ `0x69` | A1 sheet 3, S1 |
| RTC | none | none | **none** | A1 designator census |
| Battery | 120 mAh internal + 1400 mAh base | same | **single 1750 mAh** | S1–S3 |
| Charger / rails | TP4057 + SY7088 boost + SY8089 buck | same | **same parts, same designators** (TP4057 U1, SY7088 U2, SY8089 U4, CN809J U3) | A1, A3 |
| Grove / PORT.A | HY2.0-4P, G1/G2 | same | same | S1–S3 |
| **CAP / EXT header** | none | none | **EXT 2.54-14P** (`HDR-SMD_14P-P2.54`, designator P3) | A1 sheet 4, S1 |
| Lanyard hole | no | no | **yes** | S1 |
| Product weight | 92.3 g | 90.0 g | 81.0 g | S1–S3 |
| Thickness | 19.7 mm | 19.7 mm | 19.6 mm | S1–S3 |
| Sleep current (4.2 V) | 0.26 µA | 0.15 µA | **0.23 µA** (switch OFF) | S1–S3 |
| Launch (store `published_at`) | — | **2025-03-07** | **2025-09-05** | S9 |
| Price (2026-09-04) | — | $29.90, **`[EOL]`** | $29.90 | S9 |

### The v1.0-vs-v1.1 finding: the mainboard did not change

`m5stack-doc…/481/Sch_M5Cardputer.pdf` (linked from the v1.0 page) and
`m5stack-doc…/1127/Sch_M5Cardputer.pdf` (linked from the v1.1 page) are
**byte-identical**, SHA-256 `6016c1fe6099b9e3f0d0c88f07a3fba1aa44a3da8a7a91dd7040ad0fffa2041e`,
717 743 B. So are the two base schematics (`29542fe1…`, 24 076 B).

Read together with M5Stack's own comparison table — which lists *only* module-level
differences (core module, RGB LED logic, antenna, boot-key size, power) — the honest
statement is: **every published difference between Cardputer v1.0 and v1.1 lives in the
Stamp module, not on the mainboard.** I cannot rule out an unpublished mainboard change;
I can say M5Stack published no evidence of one. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

### The Stamp delta, from the two Stamp schematics

| | StampS3 `v0.2` (id 522) | Stamp-S3A `v0.3.3` (id 1150) |
|---|---|---|
| 3.3 V rail | module `M2` = **Murata `MUN3CAD01-SC` µPOL** 1 A power module, FB divider R16 100 k / R17 22.1 k | **JoulWatt `JW5712`** buck, 0–0.6 A, `VSEL1/2/3` strapped, `MWTC201608S2R2` 2.2 µH |
| Load switch | **SGM2578** (U2) | **AW35122FDR** (U2), enabled by `DISP_BL` |
| **WS2812 supply** | **`VDD_3V3`** — always on | **`BL_3V3`** — the switched backlight rail |
| Boot button | `SMT_SW_1TS026A` | `SMT_SW_1TS026A` (vendor says the *body* is larger: 4.0×3.0×2.0 mm vs 2.6×1.6×0.55 mm) |
| Crystal load caps | 12 pF / 10 pF | 12 pF / 12 pF |
| Solder jumper `JP4` at WS2812 | present | removed |

That single rail change is the whole "RGB LED power supply" story M5Stack tells in prose,
and it has a consequence the prose only half-states: because the WS2812 now shares the
PWM-dimmed backlight rail, **dimming the backlight browns out the RGB LED**. M5Stack's v1.1
page says so plainly; the ADV page does not repeat the warning even though the ADV inherits
the same Stamp-S3A. See [`features/display.md`](features/display.md).

> **Both regulators are identified, and one of them was contested.** The v0.2's `MUN3CAD01-SC`
> string looked wrong here — it resembles an ON Semi digital transistor and there is no page
> render for product id `522` to check it against — but a concurrent session retrieved a
> datasheet and confirmed it is a **Murata `µPOL` 1 A power module**, which is exactly the
> 5-terminal EN/VIN/VOUT/FB/GND symbol drawn.
> Conversely, that session recorded the **Stamp-S3A's `U4` as "part number not established"**;
> it **is** labelled **`JW5712`** in the Altium comment field directly under the symbol, which a
> marker-layer-only parse never sees. Both corrections, with evidence, are in
> [`gaps-and-conflicts.md`](gaps-and-conflicts.md) §C7 and §U1.

---

## Key specifications

| Item | Value | Component record |
|---|---|---|
| SoC | Xtensa LX7 dual-core @ 240 MHz, 512 KB SRAM, 8 MB in-package flash, **no PSRAM** | [`espressif/esp32-s3fn8`](../../../components/espressif/esp32-s3fn8/README.md) |
| Core module | Stamp-S3A, 24-pin 1.27 mm castellated DIP | [`m5stack/stamp-s3a`](../../../components/m5stack/stamp-s3a/README.md) |
| Display | ST7789V2, 1.14″, 240 × 135, 4-wire SPI (3-wire in M5GFX), 40 MHz write | [`sitronix/st7789v2`](../../../components/sitronix/st7789v2/README.md) |
| Keyboard | 56 keys (4 × 14), 160 gf, scanned by TCA8418RTWR over I²C `0x34` | [`texas-instruments/tca8418`](../../../components/texas-instruments/tca8418/README.md) |
| Audio codec | ES8311, I²C `0x18`, I²S slave | [`everest-semiconductor/es8311`](../../../components/everest-semiconductor/es8311/README.md) |
| Speaker amp | NS4150B mono class-D, 8 Ω 1 W, `CTRL` = `AMP_EN` | [`nsiway/ns4150b`](../../../components/nsiway/ns4150b/README.md) |
| Microphone | MSM381A3729H9BP analog MEMS, SNR 65 dB | [`memsensing/msm381a3729h9bp`](../../../components/memsensing/msm381a3729h9bp/README.md) |
| Headphone jack | PJ-342 3.5 mm, `HP_DET` via Q4 2N7002T | [`generic/3.5mm-audio-output`](../../../components/generic/3.5mm-audio-output/README.md) |
| IMU | BMI270 6-axis, I²C `0x69` (SDO pulled high by R43 3.3 kΩ) | [`bosch-sensortec/bmi270`](../../../components/bosch-sensortec/bmi270/README.md) |
| RGB LED | WS2812 on the Stamp, data G21, supply `BL_3V3` | [`worldsemi/ws2812`](../../../components/worldsemi/ws2812/README.md) |
| Storage | microSD, 1-bit SPI on the shared SPI bus | [`generic/micro-sd-sdmmc`](../../../components/generic/micro-sd-sdmmc/README.md) |
| Charger | TP4057 linear, `R_PROG` = 3.3 kΩ | [`generic/tp4057`](../../../components/generic/tp4057/README.md) |
| 5 V boost | SY7088, FB 75 k / 22 k → ≈ 5.29 V | [`silergy/sy7088`](../../../components/silergy/sy7088/README.md) |
| 3.3 V buck | SY8089, FB 68 k / 15 k | [`silergy/sy8089`](../../../components/silergy/sy8089/README.md) |
| Supervisor | CN809J reset generator on `+5VIN` | [`consonance/cn809`](../../../components/consonance/cn809/README.md) |
| Power path FETs | LP3218DT1G × 3 (Q1, Q2, Q3) | [`unidentified/cardputer/lp3218dt1g`](../../../components/unidentified/cardputer/lp3218dt1g/README.md) |
| Battery | 1 × 1750 mAh Li-ion, ADC divider on G10 | [`generic/charger-power-path`](../../../components/generic/charger-power-path/README.md) |
| IR | single emitter on G44, no receiver | — |
| Expansion | HY2.0-4P Grove (G1/G2) + **EXT 2.54-14P CAP header** | [`features/cap-header.md`](features/cap-header.md) |
| Size / weight | 84.0 × 54.0 × 19.6 mm, 81.0 g | A4 |

Numbers marked *inferred* — the SY7088 and SY8089 output voltages and the TP4057 charge
current — come from reading the feedback/programming resistors off the rendered schematic and
applying the datasheet formula printed **on the sheet itself** (`Vout = 1.2 V × (R1/R2 + 1)`).
They have not been measured. The charge current works out at roughly 300 mA for
`R_PROG = 3.3 kΩ`; treat that as an order-of-magnitude statement, not a spec.

---

## Architecture and components

One processor, one bus tree. There is no coprocessor, no PMIC, and no I/O expander on the
mainboard — the TCA8418 is a *keypad* scanner and exposes nothing else.

```
                                    ESP32-S3FN8 (inside Stamp-S3A)
                                             │
   ┌──────────────┬──────────────┬───────────┼───────────┬──────────────┬─────────────┐
   │              │              │           │           │              │             │
 SPI2/3         I²S1        internal I²C   ADC1      RMT/LEDC        USB-OTG      GPIO0
 G36 SCK       G41 BCK      G8 SDA         G10        G44 IR TX      native       BOOT
 G35 MOSI      G43 LRCK     G9 SCL         batt       G21 WS2812
 G37 LCD CS    G42 DOUT       │            ÷2
 G33 RST       G46 DIN        ├── TCA8418  0x34  keypad   (INT → G11)
 G34 DC        G45 (unused)   ├── ES8311   0x18  codec
   │                          └── BMI270   0x69  IMU
   ├── ST7789V2 (FPC1, 8-pin 0.5 mm)                     external I²C (PORT.A)
   ├── microSD  (CS G12, on SPI G40/G14/G39)             G1 SCL / G2 SDA  ← Grove
   └── CAP header P3 (SPI G40/G14/G39 + CS G5,
        RESET G3, INT G4, BUSY G6, UART G13/G15,
        and the same internal I²C G8/G9)
```

Two facts fall straight out of that picture and drive most of
[`resources-and-conflicts.md`](resources-and-conflicts.md):

1. **The microSD and the CAP header share one SPI bus** (G40 SCK, G14 MOSI, G39 MISO) with
   separate chip selects (G12 and G5). A LoRa transceiver and a filesystem on one bus is
   workable but needs care around clock speed and long transactions.
2. **The CAP header carries the *internal* I²C bus**, not the Grove one. Anything you hang on
   CAP pins 10/11 shares a bus with the keyboard scanner, the audio codec and the IMU, and
   must not collide with `0x34`, `0x18` or `0x69`.

---

## What it is, and visual identification

An 84 × 54 mm slab — the footprint of a credit card, 19.6 mm thick — with a 56-key rubber-dome
keyboard filling the lower two-thirds and a small landscape LCD above it. The Stamp-S3A module
is user-removable from the front panel; a ribbon FPC runs from the panel to the display, and
M5Stack warns explicitly that lifting the module carelessly damages the display connector.

Distinguishing an ADV from a v1.x **without powering it on**:

| Tell | v1.0 / v1.1 | ADV |
|---|---|---|
| 3.5 mm jack on the edge | absent | **present** |
| Lanyard hole | absent | **present** |
| 14-pin 2.54 mm header on the underside | absent | **present** |
| Base | separate battery base, held by four M2 screws | single-piece body |

And *with* power: M5GFX prints `[Autodetect] board_M5CardputerADV` versus
`[Autodetect] board_M5Cardputer`. The mechanism is in [§ Board autodetect](#board-autodetect).

> **No product photograph is retained in this record.** M5Stack's product imagery carries no
> redistribution licence (see [`vendors/m5stack`](../../../vendors/m5stack/README.md) §8).
> [`media.md`](media.md) and [`media/manifest.json`](media/manifest.json) record the URLs,
> provenance and what each image shows.

---

## Board autodetect

M5GFX identifies the board *before* any user code runs, and the mechanism is worth
understanding because it is also a compatibility hazard. From
[`M5GFX/src/M5GFX.cpp`](https://github.com/m5stack/M5GFX/blob/d91077b9a607b59404e4e4a49f775c792bfae382/src/M5GFX.cpp#L2583-L2624) — the comment block is M5Stack's own:

```c
/*
Here, VAMeter/Cardputer/CardputerADV will be automatically recognized.
The usage of each pin is as follows.
|    |  VAMeter  | Cardputer  |CardputerADV|
|:--:+:---------:+:----------:+:----------:|
| G5 | SYS_SDA   | KEY_MATRIX |  External  |
| G6 | SYS_SCL   | KEY_MATRIX |  External  |
| G7 |  NC       | KEY_MATRIX |Internal FPC|
| G8 | External  |  74HC138   |  SYS_SDA   |
| G9 | External  |  74HC138   |  SYS_SCL   |
*/
```

The probe drives G9, G8, G6, G5 as *input-pulldown* and reads them in that order;
`gpio::command()` accumulates `result = (result << 1) + res`, so **G9 → bit 3, G8 → bit 2,
G6 → bit 1, G5 → bit 0**. Then:

* `(result & 0x0C) == 0x0C` — G8 **and** G9 read high against an internal pulldown → **ADV**.
  On the ADV those are the internal I²C bus, held up by R36/R37 (3.3 kΩ each). On a v1.x they
  are 74HC138 address lines with no pull-up.
* `(result & 3) == 3` first triggers a VAMeter probe on G5/G6 for I²C `0x40`/`0x41`.

**Hazard.** The test is "are there pull-ups on G8/G9", nothing more. Fit a v1.x Cardputer
with anything that pulls G8 and G9 high — an ill-advised Grove hack, a probe clip, a
mis-wired matrix — and M5GFX will declare it an ADV, install the TCA8418 keyboard reader, and
the keyboard will simply stop working. Recorded in [`compatibility-and-status.md`](compatibility-and-status.md).

---

## Common uses and representative projects

The Cardputer's community is unusually large for a $30 board and skews four ways: **security
tooling**, **mesh radio**, **music**, and **"tiny OS"** projects. The 2026 pattern is that the
ADV, not the v1.x, is where new work happens — of the 100 `cardputer` repositories GitHub
returned on 2026-09-04, the ones created in 2026 overwhelmingly say "ADV" in the title.

Highlights, with full detail and build status in [`projects-and-community.md`](projects-and-community.md):

* **Bruce** (`BruceDevices/firmware`, AGPL-3.0, ★6 642) — the dominant offensive-security
  firmware. One `m5stack-cardputer` build serves **both** generations, switching at runtime on
  whether a TCA8418 answers at `0x34`.
* **Launcher** (`bmorcelli/Launcher`, MIT, ★2 054) — multi-firmware boot menu; ships a
  dedicated `CardputerADV.md` documenting its TCA8418 port.
* **Meshtastic** (GPL-3.0, ★8 250) — first-class `m5stack-cardputer-adv` variant. The Mesh Kit
  is an officially licensed Meshtastic device.
* **Evil-M5Project / "EvilCardputer"** (★2 570) — Wi-Fi auditing suite; the long-running
  community favourite on v1.x.
* **MicroHydra** (GPL-3.0, ★314) — MicroPython app switcher, the main MicroPython route.
* **Picoware** (GPL-3.0, ★320) — cross-device firmware that explicitly lists Cardputer ADV.
* Emulators (`geo-tp/Cardputer-Game-Station-Emulators`, `romalik/m5cardputer_doom`,
  `matteofo/gb_cardputer`), a groovebox/DAW scene (`urtubia/miniacid`, `CHARL3X/GLIDE`,
  BKLVA Pocket DAW), and a local-LLM experiment (`therezor/cardputer-ai`, "8 M params, Q4").

---

## Distinctive strengths

* **A real keyboard on a $30 ESP32.** Nothing else at the price has 56 keys and a screen in a
  pocketable case.
* **The keyboard costs almost nothing in GPIO now.** Three pins instead of fifteen, and two of
  those three are a bus you wanted anyway.
* **The CAP header is a genuine socket, not a breakout.** SPI + CS + RESET + IRQ + BUSY + UART
  + I²C + switched 5 V, in the exact shape an SX1262 or a CC1101 wants. M5Stack ships two
  boards for it and the community has already built at least four more (TFT-2.8, TFT V2,
  CC1101/NRF24/LoRa combos).
* **Board autodetect actually works**, so one binary can serve both generations. Bruce proves it.
* **Audio is a step change.** A codec with a real ADC path, a headphone jack with detection, and
  an amplifier that mutes itself — versus a PDM mic and a bare class-D on the v1.x.

## Shortcomings and constraints

* **No PSRAM. None. On any Cardputer.** `ESP32-S3FN8` is flash-in-package with no PSRAM die.
  This is the constraint that shapes every ambitious project on the platform — see the
  Meshtastic-client author's account of memory-mapping a 2.16 MB Unicode font out of a flash
  partition because it cannot live in RAM (S15).
* **No RTC.** Wall-clock time is lost on every power cycle. The CardputerZero has an RX8130CE;
  the ADV does not.
* **One SPI bus for microSD *and* the CAP header.**
* **One codec for speaker *and* microphone**, and the vendor's two enable callbacks disagree
  about how to configure it — see the driver audit in [`features/audio.md`](features/audio.md).
  This is a live bug, not a theoretical one.
* **TCA8418 `RESET` is tied high through R38 and reaches no GPIO.** If the scanner wedges,
  software cannot reset it; only a power cycle will.
* **The backlight rail powers the RGB LED**, so you may have PWM dimming or a stable RGB LED,
  not both.
* **Charging requires the power switch to be ON** — M5Stack says so on every Cardputer page.
* **0 – 40 °C operating range**, and a sealed Li-ion cell you cannot swap without opening the case.
* **No published certification.** See [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

---

## Performance summary

See [`performance.md`](performance.md). Briefly: 240 MHz dual LX7, 512 KB SRAM, no PSRAM,
40 MHz SPI display writes (M5GFX `freq_write = 40000000`), 1 500 000 baud upload in M5Stack's
own PlatformIO profile. Vendor current figures at 4.2 V: 120.2 mA idle-operating,
132.3 mA Wi-Fi, 154.6 mA BLE, 0.23 µA with the switch off. Against a 1750 mAh cell that is
roughly 13–14 h of continuous Wi-Fi operation at the vendor's own numbers — a figure I have
**not** measured and which ignores display backlight, which is likely to dominate.

---

## Pricing and availability

$29.90 at M5Stack's own store on **2026-09-04**, in stock. The Mesh Kit is $48.00, the Cap
LoRa-1262 $14.50, the Cap CC1101 & NFC $18.95. The v1.1 it replaces is listed at the same
$29.90 but titled `[EOL] M5Stack Cardputer with M5StampS3 v1.1`.
Full dated observations, other channels and caveats: [`market-and-pricing.md`](market-and-pricing.md).

---

## Competitors, equivalents and clones

Detailed treatment in [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md),
which compares the ADV against the Cardputer v1.1, the **LilyGO T-Deck**, and the
[**Nicolai Electronics Tanmatsu**](../../nicolai-electronics/tanmatsu/README.md) already in
this repository. Short version: the T-Deck trades the ADV's keyboard quality and expansion
socket for a BlackBerry keyboard, PSRAM and on-board LoRa; the Tanmatsu is a different class
of machine entirely (ESP32-P4, MIPI DSI, fully open KiCad, ~4× the price) and is the right
answer when you need the openness or the compute, not when you need $30.

No clones of the Cardputer ADV were found on 2026-09-04. See
[`market-and-pricing.md`](market-and-pricing.md) for the searches that establish that.

---

## Images and teardown/PCB views

[`media.md`](media.md) — 13 vendor product renders, a weight photo, an IMU axis diagram, four
schematic sheet renders and the crops derived from them, each with source URL, retrieval date,
rights status and what it demonstrates.

---

## Documentation map

| File | Contents |
|---|---|
| [`pinouts-and-buses.md`](pinouts-and-buses.md) | Every GPIO, both connectors, three CAP numbering schemes |
| [`resources-and-conflicts.md`](resources-and-conflicts.md) | SPI/I²C/I²S/timer/DMA contention, realistic combinations |
| [`features/`](features/README.md) | Twelve task-oriented guides |
| [`development.md`](development.md) | Arduino, ESP-IDF, PlatformIO, UiFlow2, MicroPython |
| [`factory-firmware.md`](factory-firmware.md) | UserDemo, partitions, EasyLoader, recovery |
| [`compatibility-and-status.md`](compatibility-and-status.md) | What works on which revision |
| [`projects-and-community.md`](projects-and-community.md) | 40+ catalogued projects, forum evidence |
| [`product-history-and-family.md`](product-history-and-family.md) | Dated timeline, the whole family |
| [`market-and-pricing.md`](market-and-pricing.md) | Dated prices, channels, availability |
| [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) | Versus v1.1, T-Deck, Tanmatsu |
| [`performance.md`](performance.md) | Vendor figures, silicon limits, what is unmeasured |
| [`coverage.md`](coverage.md) | Feature → evidence → guide → gap matrix |
| [`gaps-and-conflicts.md`](gaps-and-conflicts.md) | Ten recorded contradictions and unknowns |
| [`sources.md`](sources.md) | Full source table |
| [`research-log.md`](research-log.md) | Every query and its disposition |
| [`commands.md`](commands.md) | Every command, with status labels |
| [`examples/`](examples/best.md) | Example catalogue and selection |
| [`acquisition/`](acquisition/README.md) | Machine-readable artifact manifest |

## Artifact layout

```
artifacts/
├── schematic/Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf   878 155 B  9553f5ee…
├── mechanical/K132-Adv-cardputer-ADV.pdf                       127 977 B  6c937ca0…
├── docs/docs-en-core-Cardputer-Adv.html                        147 339 B  f05bbb70…
├── docs/docs-zh_CN-core-Cardputer-Adv.html                     146 690 B  4a285b02…
└── source-snapshots/
    ├── M5Cardputer-f1392858/                     MIT, 33 files, 284 KB
    └── M5Cardputer-UserDemo-CardputerADV-b549eac0/   MIT, build config only
```

The Stamp-S3A schematic is **not** duplicated here — it belongs to the module and lives at
[`components/m5stack/stamp-s3a/artifacts/`](../../../components/m5stack/stamp-s3a/README.md),
which another session was creating at the time of writing. Chip datasheets likewise file under
their components, per the skill's placement rule.

## Known conflicts and unresolved identities

Ten are recorded in [`gaps-and-conflicts.md`](gaps-and-conflicts.md). The three that matter most:

1. **The Mesh Kit page's EXT table swaps UART TX and RX.** Three independent sources — the ADV
   product page, the schematic's own net labels, M5Stack's factory firmware `uart_set_pin()`
   call, *and* Meshtastic's variant header — agree that **G13 is TX and G15 is RX**. Only the
   Cardputer Mesh Kit page says otherwise, and it contradicts itself two tables later.
2. **The CAP header has three different pin numberings in circulation** (product page,
   schematic, Cap-board side). They describe the same physical connector.
   [`features/cap-header.md`](features/cap-header.md) reconciles them.
3. **The StampS3 v0.2 3.3 V regulator is unidentified.**

---

*Snapshot 2026-09-04. This is a broad-coverage snapshot of what was publicly retrievable on
that date, not a claim that nothing else exists.*
