# DinMeter — comparisons and recommendations

**Dated 2026-09-04.** Prices are the observations in [`market-and-pricing.md`](market-and-pricing.md).
Applies to the DinMeter family (K134 / K134-V11); where the two differ it is noted.

**Scope discipline.** Nothing below is called "equivalent" unless the interfaces, electrical
behaviour and software requirements actually align for the stated workload. Where they do not,
it says *partial substitute* and names what is missing. No benchmark comparison is offered,
because **no device in this comparison was benchmarked here** — see
[`performance.md`](performance.md).

---

## 1. The one-sentence answer

> Buy a DinMeter if you have a **1/32 DIN panel aperture** or a **12/24 V supply and no 5 V**.
> If you have neither, buy something else — as a knob-with-a-screen it is beaten on almost every
> axis by devices costing similar money.

Those two attributes are not incidental features; they are the entire reason the product exists,
and no competitor in this comparison has either.

---

## 2. Versus the Waveshare ESP32-S3-Knob-Touch-LCD-1.8

The closest thing to a like-for-like "ESP32 knob" competitor documented in this repository:
[`devices/waveshare/esp32-s3-knob-touch-lcd-1.8/`](../../waveshare/esp32-s3-knob-touch-lcd-1.8/README.md).

| | **M5Stack DinMeter** (K134-V11) | **Waveshare ESP32-S3-Knob-Touch-LCD-1.8** (31623) |
|---|---|---|
| Price (2026-09-04) | **USD 24.50** | see the Waveshare record's market section |
| Form factor | 53 × 30 × 32 mm rectangular, **1/32 DIN panel cutout 45 × 22.5 mm** | 66 mm diameter × 22 mm, **CNC-machined metal**, desktop puck |
| Main MCU | ESP32-S3**FN8** — 8 MB flash, **no PSRAM** | ESP32-S3**R8** — **8 MB PSRAM** + 16 MB external W25Q128 flash |
| Second MCU | none | **ESP32-U4WDH** — a whole second SoC, the board's only source of **Bluetooth Classic (BR/EDR)** |
| Display | 1.14 in **135 × 240** SPI, ST7789V2/P3 | 1.8 in **360 × 360** round QSPI, ST77916/SH8601 |
| Touch | **none** | CST816D capacitive |
| Knob | **detented incremental quadrature encoder + push** | **two** Alps SSCM110100 *directional switches* — not conventional encoders, and each is readable only by its own MCU |
| Audio out | magnetic buzzer only | PCM5100A stereo DAC → 3.5 mm line out |
| Audio in | none | PDM microphone |
| Haptics | none | DRV2605L + LRA |
| Storage | none | microSD, 4-bit SDMMC |
| **DC input** | **6 – 36 V** on a screw terminal | **5 V USB only** |
| Battery | 1S Li-ion socket + TP4057 charger + power-path + boost, latched off at **38.4 µA** | optional 102035 LiPo; charger/power-path **not identified** in that record |
| RTC | **BM8563, battery-backed, wakes the board from off** | **none** |
| Expansion | **2 × Grove HY2.0** (I²C + GPIO), 5 V @ 220 mA each | 2 × PH1.27 10-pin headers, **exact pinout not published** |
| USB | native USB-C on the module | USB-C where **plug orientation selects which MCU you talk to** |
| Enclosure | plastic | **CNC metal** |
| ESPHome | **no** | **yes** (that record has a dedicated ESPHome confirmation document) |
| Community | ~13 GitHub projects, 1 Reddit post | materially larger |

### What that table actually means

**The Waveshare is a better knob. The DinMeter is a better instrument.**

Choose the Waveshare when the device sits on a desk and the *interaction* is the point: 360 × 360
round display, touch, haptics, audio in and out, Bluetooth Classic media control. It has 8 MB of
PSRAM, so LVGL with a full framebuffer is comfortable. It looks and feels like a product.

Choose the DinMeter when the device goes **inside something**: a panel, a cabinet, a machine.
Everything the Waveshare adds is irrelevant there, and three things the DinMeter has are not
available at any price on the Waveshare — the DIN cutout, the 6–36 V input, and a
battery-backed RTC that can power the board back on.

**They are not substitutes.** Do not treat "ESP32-S3 + knob + LCD" as a category. A Waveshare
knob cannot be panel-mounted into a 1/32 DIN aperture and cannot be run from a 24 V rail without
an external converter; a DinMeter cannot play Bluetooth audio, has no touch, and has 1/12th the
pixel count.

**One shared caution.** Both records carry an unresolved display-controller identity: the
Waveshare's panel is marketed ST77916 but driven by an SH8601 compatibility driver; the DinMeter
v1.1's ST7789P3 has **no published datasheet at all**. Neither vendor is rigorous here.

---

## 3. Versus the M5Stack Dial (K130-V11)

The DinMeter's own sibling, and the more instructive comparison — they share a software path.

| | **DinMeter** (K134-V11) | **M5Dial v1.1** (K130-V11) |
|---|---|---|
| Price (2026-09-04) | **USD 24.50** | **USD 34.90** |
| Shape | rectangular, panel-mount | round puck |
| Display | 1.14 in 135 × 240 | 1.28 in 240 × 240 round |
| Touch | none | **yes (FT3267)** |
| Knob | encoder + push | encoder + push |
| DC input | **6 – 36 V** | 5 V |
| RTC | BM8563 | BM8563 |
| Buzzer | yes | yes |
| Grove ports | PORT.A + PORT.B | PORT.A + PORT.B |
| Core module | Stamp-S3A | Stamp-S3 family |
| M5Unified enum | `board_M5DinMeter` | `board_M5Dial` |

**They are the same board in two shells.** M5Unified handles them in the *same switch cases* for
button reading, buzzer configuration, power hold and I²C
(`M5Unified.cpp:96, 159, 246, 282, 2398, 2921, 3502`), and the DinMeter's Arduino library is a
literal copy of the M5Dial's — its header guard is still `#define M5DIAL_H` and its pin macros
are still named `DIAL_ENCODER_PIN_A/B`.

**So the decision is purely mechanical and electrical:**

- Need a **round** face, a **touchscreen**, or 240 × 240? → M5Dial, and pay USD 10.40 more.
- Need a **panel aperture** or **12/24 V**? → DinMeter. The Dial cannot do either.
- Neither? → DinMeter, because it is cheaper and the software is identical.

---

## 4. Versus rolling your own (encoder + ESP32 + display)

The honest competitor for most hobby use.

| | **DinMeter** (USD 24.50) | **DIY: ESP32-S3 board + EC11 + 1.14 in ST7789** |
|---|---|---|
| Parts cost | 24.50, one SKU | ≈ 6–12 for a generic S3 board + ≈ 1 encoder + ≈ 3–5 display ≈ **10–18** |
| Time | zero | a weekend, plus a case |
| 6–36 V input | included | + a 24 V buck module (≈ 1–3) and the board space for it |
| Li-ion charge + power path + boost + latch | included, and the latch design is genuinely good | + a charger board, and you will not get 38.4 µA standby |
| RTC + crystal + battery backup | included | + a DS3231/PCF8563 module |
| Enclosure to a **standard panel cutout** | included | this is the part you cannot buy |
| Certification / EMC | M5Stack's problem | yours |
| Software | M5Unified + Espressif board def + vendor examples, all working | you write the board file |
| Reproducibility across units | one SKU | you own the BOM forever |

**Build it yourself when** it is a one-off on a bench, cost dominates, or you need something the
DinMeter cannot do (PSRAM, a bigger screen, more GPIOs, a camera).

**Buy the DinMeter when** it goes into a panel, when there will be more than one, when someone
other than you will maintain it, or when you want to be doing application work by lunchtime. The
enclosure and the cutout are the part that is genuinely hard to reproduce, and they are most of
what you are paying for.

---

## 5. Alternatives by tier (2026-09-04, global pricing, hobbyist/prosumer)

| Tier | Pick | Why | Watch out for |
|---|---|---|---|
| **Cheapest working knob UI** | Generic ESP32-S3 + EC11 + 1.14 in ST7789 | ≈ USD 10–18 | No case, no cutout, no RTC, no wide input |
| **Panel-mount instrument, 12/24 V** | **DinMeter v1.1**, USD 24.50 | The only product in this list that fits a 1/32 DIN aperture and takes 36 V | No PSRAM, no touch, 0–40 °C, ~8 free GPIOs |
| **Desktop knob, richest UI** | Waveshace ESP32-S3-Knob-Touch-LCD-1.8 | 360 × 360 round + touch + haptics + audio + PSRAM + Bluetooth Classic | Dual-MCU complexity; USB orientation selects the MCU; 5 V only |
| **Round M5 knob with touch** | M5Dial v1.1, USD 34.90 | Same software as DinMeter, adds touch and a round 240 × 240 | +USD 10.40, 5 V only, no panel cutout |
| **Battery-first Stamp project** | Bare **Stamp-S3A**, USD 7.50 | 6.84 µA sleep on `VIN_5V`; you supply the rest | You are designing a board; budget 0.6 A on 3.3 V, not 1 A |
| **Home Assistant, no code** | Not this device | ESPHome supports neither DinMeter nor M5Dial out of the box | See [`projects-and-community.md`](projects-and-community.md) §1 |
| **Industrial DIN-rail PLC-ish** | M5Stack StamPLC, USD 42.90 | DIN-*rail* (not panel-cutout), relays, CAN, RS485 | Different problem entirely — rail-mounted controller, not a panel head |

---

## 6. The DIN question, stated properly, because it is the whole point

**"DIN" in this product's name means the panel-cutout standard, not the rail.** That distinction
costs people money.

- **1/32 DIN** (DIN 43700) specifies a panel aperture of **45 × 22.5 mm**. That aperture exists,
  already cut, in an enormous installed base of instrument panels, PLC cabinet doors, machine
  consoles and process racks — because it is what a generation of temperature controllers and
  panel meters used. The DinMeter drops into one.
- **DIN rail** (TS-35) is the 35 mm hat-rail inside the cabinet. The DinMeter does **not** clip
  to it. M5Stack's own DIN-rail product is the StamPLC.

If you are retrofitting a machine and there is a dead Omron/Autonics/Fuji panel meter in the
front door, the DinMeter is a straight swap into that hole, powered from the 24 V that was
already feeding the old unit, and you can be showing a modern UI with Wi-Fi in it the same
afternoon. **That is the use case, and nothing else in this comparison can do it.**

Conversely: if you do not have that hole, you are paying for an enclosure shape you will not use,
and one of the cheaper options above is a better buy.

Mechanical detail: [`features/din-mounting-and-mechanical.md`](features/din-mounting-and-mechanical.md).

---

## 7. Who should *not* buy it

- Anyone who needs **PSRAM** — a large LVGL framebuffer, a camera, a heavy TLS workload. There
  is none, on either revision.
- Anyone who needs a **touchscreen**, or more than 135 × 240 pixels.
- Anyone who needs **more than ~8 free GPIOs** — four of the free ones are the two Grove ports.
- Anyone deploying outside **0 – 40 °C**. An unheated cabinet in winter, or a sealed panel in
  summer sun, is outside spec.
- Anyone who wants **ESPHome/Tasmota/Meshtastic** to work today. None of them support it.
- **First-time ESP32 users.** The GPIO46 power latch will catch you, and the failure looks like
  a hardware fault.

---

## 8. Clones

**None found.** No AliExpress or marketplace clone of the DinMeter was located on 2026-09-04.
That is a **negative search result**, not proof of absence — see
[`research-log.md`](research-log.md) for the queries run. The likely reason is that the value is
in the enclosure and the DIN fit rather than in a copyable PCB, and the volumes are small.

---

## Related

[`market-and-pricing.md`](market-and-pricing.md) · [`performance.md`](performance.md) ·
[`projects-and-community.md`](projects-and-community.md) ·
[`../dinmeter-v1.1/stamp-s3-to-s3a-delta.md`](../dinmeter-v1.1/stamp-s3-to-s3a-delta.md) ·
[`devices/waveshare/esp32-s3-knob-touch-lcd-1.8/`](../../waveshare/esp32-s3-knob-touch-lcd-1.8/README.md)

---

## Cross-references added 2026-09-07

Append-only, from a cross-cutting synthesis pass. Nothing above was changed and no
new evidence was gathered.

- [**Handheld and e-ink device landscape, 2026-09**](../../../guides/markets/handheld-and-eink-device-landscape-2026-09.md)
  — a buyer-oriented survey of every device record in the repository. The DinMeter
  sits outside its four shopping groups (it is a panel-mount instrument, not a
  handheld) and is carried in the completeness section, with the v1.0/v1.1
  byte-identical-assets finding preserved as the headline.
- [**SoC choice for battery e-ink devices**](../../../guides/hardware/soc-choice-for-battery-eink-devices.md)
  — the Stamp-S3 → Stamp-S3A change documented in this tree is used there as the
  worked example that **board sleep current is dominated by the power tree, not the
  SoC**: 310.89 µA → 6.84 µA on `VIN_5V`, bought by swapping a µPOL module for a
  discrete buck and moving the WS2812 onto a switched rail — and paid for with the
  RGB LED's always-on supply.
