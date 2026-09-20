# T-Display-S3 — comparisons and recommendations

> Dated **2026-09-07**. Prices are official-store, region "China [For Worldwide]", excluding
> shipping and tax, on that date. Comparisons are scoped to a stated workload; nothing here
> calls two boards "equivalent" without saying at what.

## 1. Against boards already documented in this repository

| | **LilyGO T-Display-S3** | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) | [Seeed XIAO ESP32S3 Sense](../../seeed-studio/xiao-esp32s3-sense/README.md) | [M5Stack Cardputer ADV](../../m5stack/cardputer-adv/README.md) |
|---|---|---|---|---|
| Price, 2026-09-07 | **USD 9.04** | not re-checked this pass | not re-checked this pass | not re-checked this pass |
| SoC | ESP32-S3R8 | ESP32-S3R8 **+ ESP32-U4WDH** | ESP32-S3R8 | ESP32-S3 |
| Flash / PSRAM | 16 MB / 8 MB OPI | 16 MB / 8 MB | 8 MB / 8 MB | — |
| Display | 1.9″ **170×320** IPS, ST7789V | 1.8″ **360×360** round | **none** | 1.14″ 240×135 |
| Display bus | **8-bit 8080 parallel** | QSPI | — | SPI |
| Touch | optional, +USD 3.57 | yes, CST816D | — | — |
| Audio in | — | PDM mic | **PDM mic** | mic + codec |
| Audio out | — | PCM5100A DAC → 3.5 mm | — | codec + speaker + 3.5 mm |
| Camera | — | — | **OV2640** | — |
| microSD | shield only, 1-bit | 4-bit SDMMC | yes | yes |
| Keyboard | — | 2 knobs | — | **56 keys** |
| IMU | — | — | — | yes |
| Battery | JST 1.25, unprotected, ~500 mA charge | optional LiPo | pads | single large cell |
| Classic Bluetooth | **no** | **yes**, via the U4WDH | no | no |
| Size class | 62 × 26 mm | round knob | 21 × 17.8 mm | 84 × 54 mm card |

### What each is actually for

- **T-Display-S3 — the cheapest good screen.** If the job is "put a colour UI on a networked
  thing", this wins on price per pixel and on the parallel bus's refresh rate. It has almost
  no other features, which is the point.
- **Waveshare Knob-Touch-LCD-1.8 — the only one with Classic Bluetooth**, because it carries a
  second MCU for it, and the only one with real line-out audio and haptics. Considerably more
  complex: two MCUs, a shared DAC with a mux, and a documented controller-naming conflict.
  Choose it when you need a *round* UI, audio, or BR/EDR.
- **XIAO ESP32S3 Sense — the only one with a camera**, and by far the smallest. No display at
  all. These two boards are complements, not alternatives; a common pairing is Sense for
  capture and T-Display-S3 for the UI.
- **Cardputer ADV — the only one that is a computer.** Keyboard, speaker, IMU, battery, case.
  If you want to *type* on it, nothing else here comes close. If you want to embed it in
  something, it is the wrong shape.

**No performance comparison is offered**, because none of these four has a measured benchmark
in this repository under a shared method. Saying one is "faster" would be exactly the
unsupported comparison the method forbids.

## 2. Against the obvious market rivals

| Board | ~Price | Display | Why you might prefer it | Why you might not |
|---|---|---|---|---|
| **LilyGO T-Display-S3** | **USD 9.04** | 1.9″ 170×320 IPS, 8080 | cheapest with 16 MB + 8 MB PSRAM + bonded display | 7 free GPIOs; no SD; no protection circuit; vendor pinned to Arduino core 2.0.14 |
| **LilyGO T-Display (ESP32)** | USD 8.04 | 1.14″ 135×240, SPI | cheaper still; huge legacy community (1 192★) | ESP32 not S3, 4 MB flash on the base SKU, smaller/slower panel |
| **ESP32-S3-BOX / BOX-3** | ~USD 45–60 | 2.4″ 320×240 + touch | speech front-end, mic array, speaker, enclosure, first-party Espressif support | 5× the price; a product, not a component |
| **M5Stack CoreS3** | ~USD 55 | 2.0″ 320×240 + touch | enclosure, battery, IMU, huge Unit ecosystem | 6× the price |
| **Waveshare ESP32-S3-Touch-LCD-1.28/1.69** | ~USD 20–30 | round or 240×280 | round option; some have IMU/RTC | 2–3× the price for similar silicon |
| **Sunton / "Cheap Yellow Display" ESP32-2432S028** | ~USD 12–15 | 2.8″ 320×240 resistive | bigger screen, SD slot, cheap | plain ESP32, resistive touch, no PSRAM on most, documentation is community-only |
| **Bare ESP32-S3-DevKitC + separate panel** | ~USD 8 + panel | your choice | full pin freedom | you assemble and wire it; total cost rarely beats USD 9.04 |

**The honest summary:** at USD 9 the T-Display-S3 has no direct competitor that includes a
bonded 170×320 IPS panel, 16 MB flash and 8 MB PSRAM. Everything cheaper drops one of those;
everything comparable costs at least twice as much. What you pay for that is a **very** tight
GPIO budget and a vendor whose documentation lags its hardware.

## 3. Who should buy which — concrete, dated

| You want to… | Buy | Why |
|---|---|---|
| put a networked colour UI in a box, cheaply | **T-Display-S3 `H569`, USD 9.04** | nothing else is close at this price |
| …and poke it with a finger | **T-Display-S3 Touch `H587`, USD 12.61** | cheapest capacitive touch on any ESP32-S3 board here; check whether your board is CST816S or CST328 before writing code |
| …with a case and a battery | `K204`/`K206` USD 13.22 + a **protected** ≥600 mAh cell | the bundled-battery SKU was out of stock 2026-09-07 |
| a display you can read outdoors / at an angle | **T-Display-S3 AMOLED**, USD 26.44 | AMOLED contrast; but you inherit the V1.0/V2.0 question |
| a long thin bar display (VU meter, ticker, dashboard) | **T-Display-S3 Long**, USD 29.35 | 180×640 is a shape nothing else offers; note the vendor's own header has [pin collisions](../t-display-s3-long/gaps-and-conflicts.md) |
| a handheld with camera, microSD and 3 buttons | **T-Display-S3 Pro**, USD 37.99–56.99 | closest thing to a product in the family; **check V1.0 vs V1.1** for the backlight scale |
| the biggest AMOLED | **T4-S3**, USD 56.89 | 450×600; sold under the T4 name, not T-Display-S3 |
| a camera, not a display | **XIAO ESP32S3 Sense** | different job entirely |
| something you type on | **Cardputer ADV** | different job entirely |
| Classic Bluetooth (BR/EDR) | **not any of these** — the Waveshare Knob board, via its second MCU | the ESP32-S3 has no BR/EDR at all. This catches people |
| LoRa / Meshtastic | **not any T-Display-S3** | no radio. Look at T-Beam, T-Deck, T3-S3, or T-Display-S3 Pro **LR1121** (USD 65.29) |

## 4. Do not use a T-Display-S3 when…

- **You need more than ~7 free GPIOs.** Count them first
  ([`features/gpio-and-expansion.md`](features/gpio-and-expansion.md)). This is the number-one
  reason people regret the choice.
- **You need Classic Bluetooth.** ESP32-S3 is BLE-only.
- **You need an unattended battery product.** No battery protection, no fuel gauge, a fixed
  ~500 mA charge current, and the battery ADC reads nonsense while USB is attached.
- **You need reliable serial on battery.** `USB CDC On Boot` forces a choice; see
  [`features/usb.md`](features/usb.md).
- **You need a supported, versioned platform.** There is no PCB revision scheme, no changelog,
  and the vendor's tested Arduino core is two major versions behind.
- **You need known Wi-Fi range.** It has never been measured, and it is the most-complained-of
  characteristic.

<a id="the-clone-question"></a>
## 5. The clone question — worked example

Method: [`guides/markets/clones-and-variants.md`](../../../guides/markets/clones-and-variants.md)
(read for this pass; **not edited**). Applied to this board:

**What "clone" means here is unusually murky, because LilyGO is itself a rebadger.** The
company trades as *Shenzhen Xin Yuan Electronic Technology* (the copyright line in its own
source headers), sells under **LilyGO** and historically **TTGO**, and its GitHub org is
`Xinyuan-LilyGO`. The predecessor board is called *TTGO T-Display* in the repo and *T-Display*
in the store. There is no "original" brand to be cloned *from* in the way there is with, say,
an Arduino Uno.

### What can be established

| Test | Result |
|---|---|
| Does LilyGO publish a schematic? | **Yes, one sheet.** So a copyist has the design |
| Are the design files licensed? | The **repository** is MIT. Whether that covers the PDF schematic is unstated — MIT is a software licence, and LilyGO applies no hardware licence |
| Is there a serial number, QR or authentication? | **No.** None found on the board, in the schematic, or in the firmware |
| Does the firmware identify the board? | **No.** The app descriptors say `arduino-lib-builder`; there is no LilyGO string, no version, no board id |
| Is there a distinguishing USB VID/PID? | **No.** `303A:1001` is **Espressif's** native USB-Serial-JTAG identity, shared by every ESP32-S3 using the built-in USB. It proves the SoC, not the vendor |
| Does the vendor sell through marketplaces? | Yes — a Banggood coupon for the AMOLED board was posted to Reddit on 2024-11-30. So a marketplace listing is **not** evidence of a clone |

### What follows

**There is no reliable way to tell a genuine LilyGO T-Display-S3 from a competent copy**, and
this record does not claim one exists. The available discriminators are all weak:

- **Silkscreen and logo.** Present on genuine boards; trivially copied.
- **LED behaviour.** LilyGO documents specific charge-LED semantics (dim/flashing with no
  battery, solid charging, off when full). A copy using a different charger will behave
  differently. **This is behavioural evidence, and it is the strongest cheap test available** —
  but it fails against a copy that uses the same charger.
- **The `65b311` charger marking.** Since even LilyGO's own schematic does not match its own
  board here, chip markings cannot distinguish genuine from copy without a known-good
  reference.
- **Price.** A listing far under USD 9 for a bare board is suspicious in the sense that
  margins are already thin; it is not proof.

**The practical risk is not counterfeiting, it is silent revision drift** — which affects
genuine boards too, and is documented at
[`../t-display-s3-shared/board-revision-drift.md`](../t-display-s3-shared/board-revision-drift.md).
Treat any board you did not buy from LilyGO directly as an **unidentified member of the
T-Display-S3 set**, run the identification checklist in that document, and write code that
probes rather than assumes.

---

## Cross-references added 2026-09-07

Append-only, from a cross-cutting synthesis pass. Nothing above was changed and no
new evidence was gathered. ⚠ This file was last modified less than an hour before
this append; the section was added at the end of the file only, and nothing else in
this tree was touched.

- [**Handheld and e-ink device landscape, 2026-09**](../../../guides/markets/handheld-and-eink-device-landscape-2026-09.md)
  — the T-Display-S3 family in a display-dev-board group against the Waveshare
  ESP32-S3-Knob-Touch-LCD-1.8 and the XIAO ESP32S3 Sense, with the family's three
  traps (the `USB CDC On Boot` block, the Arduino-core 2.0.14 pin, the display-bus
  split) carried through, and the note that **two boards in the family declare no
  licence at all**.
- [**SoC choice for battery e-ink devices**](../../../guides/hardware/soc-choice-for-battery-eink-devices.md)
  — this board is the price anchor for the guide's central argument: **$9.04 buys
  an ESP32-S3 with 16 MB flash and 8 MB OPI PSRAM *and* a colour LCD**, the same
  memory configuration as a $65 PaperMono and a $99 Xteink X4 Pro. PSRAM is not
  what makes an e-ink device expensive, so choosing an `R8` over a no-PSRAM part is
  close to free — and the C3's memory ceiling is the most expensive constraint in
  this repository measured in developer time. The guide also carries this family's
  **GPIO26–37 / GPIO33–37 OPI-PSRAM pin cost** as the practical price of `R8`.
