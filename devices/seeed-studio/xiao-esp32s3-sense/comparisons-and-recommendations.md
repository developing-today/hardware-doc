# Comparisons and recommendations — XIAO ESP32S3 Sense

> How it stacks up against the boards you would actually consider instead.
> Snapshot **2026-08-24**. Prices are Seeed official store, USD, same date. **No hardware was benchmarked** — comparisons are on published specification and design evidence, not measurement.

## 1. The competitive question

The Sense competes in a narrow category: **microcontroller boards with an integrated camera**. There are not many, and they differ mostly on size, memory and how much of the sensor you can control.

| Board | Price | SoC | PSRAM | Camera | Mic | SD | Size |
|---|---:|---|---|---|---|---|---|
| **XIAO ESP32S3 Sense** | **$13.99** | ESP32-S3 | **8 MB** | OV3660 3 MP, **detachable** | ✅ PDM | ✅ | **17.8 × 21.1 mm** |
| ESP32-CAM (AI-Thinker) | ~$6–9 | ESP32 | 4 MB | OV2640 2 MP | ❌ | ✅ | 27 × 40.5 mm |
| ESP32-S3-EYE (Espressif) | ~$50 | ESP32-S3 | 8 MB | OV2640 + LCD | ✅ | ✅ | 46 × 52 mm |
| Freenove ESP32-S3-WROOM CAM | ~$14 | ESP32-S3 | 8 MB | OV2640 | ❌ | ✅ | ~25 × 50 mm |
| XIAO ESP32S3 (plain) | $7.49 | ESP32-S3 | 8 MB | ❌ | ❌ | ❌ | 17.8 × 21.1 mm |
| XIAO nRF52840 Sense | $12.99 | nRF52840 | ❌ | ❌ | ✅ PDM | ❌ | 17.8 × 21.1 mm |

> Non-Seeed prices are **approximate street prices from general knowledge, not observed on 2026-08-24**, and are flagged as such. Only the two Seeed rows are dated observations. Treat the non-Seeed figures as indicative ordering, not quotes.

## 2. Versus ESP32-CAM

The ESP32-CAM is the default cheap camera board and the Sense's main real competitor.

**Sense wins on:** size (about a quarter of the area), SoC generation (S3 vs original ESP32 — vector instructions matter for TinyML), PSRAM (8 MB vs 4 MB), **native USB** (the ESP32-CAM famously needs an external USB-TTL adapter and a jumper to flash), an on-board microphone, battery charging, and a **detachable** camera.

**ESP32-CAM wins on:** price (roughly half), **camera `PWDN` and `RESET` lines are wired** — you can reset and power down the sensor, which the Sense cannot — and an enormous body of tutorials.

**Verdict:** if size or USB convenience matters at all, take the Sense. If you are building a mains-powered doorbell camera on a budget and do not care about size, the ESP32-CAM is still fine and cheaper. If you need to reliably recover a wedged sensor without a power cycle, the ESP32-CAM is *architecturally* better.

## 3. Versus ESP32-S3-EYE

Espressif's own vision development kit. Roughly **3.5× the price**, with an LCD, a proper enclosure and first-party ESP-WHO/ESP-DL support.

**Verdict:** the S3-EYE is a *development kit*; the Sense is a *component*. If you are evaluating Espressif's vision stack on a desk, the S3-EYE is more pleasant. If you are embedding a camera into a product or a wearable, the Sense is the only one of the two you can actually fit.

## 4. Versus the plain XIAO ESP32S3

The most important comparison, because it is $6.50 and reversible.

| | Plain | Sense |
|---|---|---|
| Price | $7.49 | $13.99 |
| Deep sleep | **14 µA** | ~34 µA |
| **JTAG debugging** | ✅ **available** | ❌ consumed by sensors |
| Free GPIO | 11 | ~4 (with SD in use) |
| Camera / mic / SD | ❌ | ✅ |

The Sense's daughterboard is **detachable**, so a Sense can become a plain S3 — but a plain S3 cannot become a Sense (the daughterboard is not sold separately for retrofit in the same way).

**Verdict: buy the Sense unless you are certain you will never want a camera.** The $6.50 premium buys optionality. The real costs are the JTAG loss and the sleep current, and both disappear when you unplug the daughterboard.

## 5. Versus XIAO nRF52840 Sense

Same form factor, $1 cheaper, and a completely different design point.

| | ESP32S3 Sense | nRF52840 Sense |
|---|---|---|
| Radio | **Wi-Fi** + BLE | **BLE only** |
| Camera | ✅ | ❌ |
| Microphone | ✅ PDM | ✅ PDM |
| IMU | ❌ | ✅ 6-axis |
| **Battery voltage sense** | ❌ **none** | ✅ |
| Deep sleep | ~34 µA | **~5 µA** |

**Verdict:** for a battery-powered BLE sensor or motion wearable, the nRF52840 Sense is clearly better — an order of magnitude lower sleep current, an IMU, and it can actually tell you its battery level. Choose the ESP32S3 Sense when you need **a camera** or **Wi-Fi**. Those are the only two reasons, but they are decisive ones.

## 6. Versus the XIAO ESP32S3 Plus — examined from the schematics

At **$7.90** the Plus is $0.41 more than the plain S3. Seeed's wiki states its B2B connector "is compatible with [the] Wio-SX1262 extension board **but not with [the] Plug-in camera sensor board**".

I parsed the Plus's published KiCad source to understand why. The result is more nuanced than the wiki suggests, and worth knowing before you choose.

### What is identical

| Property | Sense mainboard | **Plus** |
|---|---|---|
| Board outline | 17.78 × 21.14 mm | **17.78 × 21.14 mm** — identical |
| B2B footprint | `BTB30-0.4-7.52X2.97X1.14` | **same footprint** |
| J3 pin count | 34 pads (30 signal + 4 mech) | same |
| **J3 pin assignment** | DVP, PDM, SD SPI, VIN, VCC_3V3, GND | **pin-for-pin the same** |

The Plus carries the same camera DVP bus, the same PDM microphone pins, the same SD SPI, and the same power on the same connector pads.

### What differs

| | Sense mainboard | Plus |
|---|---|---|
| **B2B part** | Hirose **`DF40C-30DP-0.4V(51)`** | **`LBF11-G30P-BOR`** |
| Flash | GD25Q64E (8 MB) | **PY25Q128HA (16 MB)** |
| Castellated header | 14-pin | **23-pin** (`XIAO-HALF-HOLE-23P`) |
| GPIO10 | `XMCLK` only | `XMCLK` **+ `ADC_BAT`** |
| J3 pad 1 | GND | unconnected |

**The connector is a different manufacturer's part on the same land pattern.** The Sense daughterboard's mating half is a Hirose `DF40HC(3.0)-30DS-0.4V(51)` — the `HC(3.0)` denoting a 3.0 mm stacking height. Whether an `LBF11-G30P-BOR` plug mates reliably with a Hirose DF40 socket, at the correct height, is **not something I can determine from the schematic**, and is the most likely basis for Seeed's incompatibility statement.

**Treat the wiki's claim as authoritative.** A shared land pattern is not proof of mating compatibility, and the vendor is in a position to have tested it. But note the incompatibility appears to be **mechanical/connector-vendor, not electrical** — the signals line up exactly.


### Why LoRa and the camera are mutually exclusive — resolved from the schematic

Seeed's wiki says the Plus B2B "is compatible with the Wio-SX1262 extension board but not with the plug-in camera sensor board", which reads like a connector problem. Parsing [Seeed's published Wio-SX1262 schematic](artifacts/accessories/wio-sx1262-for-xiao-v1.0-sch.pdf) (KiCad 8, dated 2024-09-19) shows the real reason is much simpler: **the two daughterboards want the same pins.**

The Wio-SX1262 uses **GPIO14, 15, 16, 17, 18, 21, 47 and 48** across the B2B connector for its SPI bus, `BUSY`, `DIO1`, `RST`, `NSS` and RF switch.

| GPIO | Wio-SX1262 uses it for | Sense daughterboard uses it for |
|---:|---|---|
| 14 | LoRa | `DVP_Y6` |
| 15 | LoRa | `DVP_Y2` |
| 16 | LoRa | `DVP_Y5` |
| 17 | LoRa | `DVP_Y3` |
| 18 | LoRa | `DVP_Y4` |
| 21 | LoRa | `USER_LED` / `SD_CS` |
| 47 | LoRa | `DVP_HREF` |
| 48 | LoRa | `DVP_Y9` |

**All eight of the eight GPIOs the LoRa board needs are already consumed by the camera board.** There is one B2B connector and the two accessories contend for the same signals on it.

So:

- **On a Sense**, you cannot add LoRa — the connector is occupied and the pins clash even if it were not.
- **On a plain XIAO ESP32S3 or a Plus**, the LoRa board fits because no camera board is competing for those pins.
- This is a **pin-allocation conflict, not a connector-compatibility problem** — which is a more useful way to understand it, because it means no adapter or riser can solve it.

Practical consequence for anyone wanting a **LoRa camera node** (a recurring request in the Meshtastic community): it needs **two XIAOs**, or a custom daughterboard that muxes the bus. Both are real projects, not configuration changes.

### The Plus has battery voltage sensing

The most consequential difference for many designs: **GPIO10 on the Plus is `ADC_BAT` as well as `XMCLK`**, and it is routed to the 23-pin header.

The Sense [has no battery voltage sense at all](features/battery-and-power.md#4-you-cannot-read-the-battery-voltage) — the single most-requested missing feature. The Plus appears to address it, at the cost of sharing the pin with the camera master clock (which is consistent with the camera board not being supported on it).

> Status: **`inferred` from the Plus KiCad netlist**, retrieved 2026-08-24. I have not verified a divider's resistor values or tested it. The Plus is not the subject of this research pass and has no record of its own here.

**Verdict:** if you want a camera, buy the Sense — the Plus is not supported for it and the connector differs. If you do **not** need a camera, the Plus is the better board on nearly every axis: double the flash, 23 exposed pins instead of 14, dual UART/SPI, and battery sensing, for $0.41 more than the plain S3.

## 7. Recommendations by scenario

Each states the workload, the constraint, and the date the pricing applies (2026-08-24, USD, Seeed store).

| Scenario | Recommendation | Why |
|---|---|---|
| **Wi-Fi camera in a tight space** | **XIAO ESP32S3 Sense** | Nothing else this small does it |
| **AI/vision wearable** | **Sense** | The category-defining use; large body of prior art |
| **TinyML vision** | **Sense** | S3 vector instructions + 8 MB PSRAM + SSCMA/Edge Impulse support |
| **USB webcam** | **Sense** | Native USB UVC — see [`features/usb.md`](features/usb.md) |
| **Cheap mains-powered security camera** | ESP32-CAM | Half the price; size irrelevant |
| **Evaluating Espressif's vision stack** | ESP32-S3-EYE | Kit with display and first-party demos |
| **Battery BLE sensor / motion wearable** | **XIAO nRF52840 Sense** | ~5 µA sleep, IMU, battery sensing |
| **Matter / Thread / Zigbee** | XIAO ESP32C6 ($5.20) | Wi-Fi 6 + 802.15.4 |
| **General S3 work, no camera** | **XIAO ESP32S3 Plus** ($7.90) | 16 MB flash, 18 GPIO, same price bracket |
| **You need JTAG debugging with sensors** | **None of these** | Architectural conflict on the Sense; reconsider the board |
| **Bluetooth Classic audio (A2DP/HFP)** | **Not the Sense** | ESP32-S3 is BLE-only. Use original-ESP32 silicon |
| **Battery telemetry required** | Not the Sense without external hardware | No divider fitted; see [`features/battery-and-power.md` §4](features/battery-and-power.md#4-you-cannot-read-the-battery-voltage) |

## 8. Where the Sense is genuinely unmatched

Stripping away the marketing, three things are hard to get elsewhere at any price:

1. **A camera + microphone + SD in 17.8 × 21.1 mm.** This is the product. If your constraint is volume, the comparison table above collapses to one row.
2. **A detachable sensor module.** You can prototype with sensors and ship without them, on the same PCB footprint — or service a broken camera without replacing the MCU.
3. **CC BY-SA 4.0 design files.** Full KiCad sources for a commercial board is rare, and it is what made the netlist-derived documentation in this tree possible. For anyone designing a carrier board or a custom daughterboard, this is worth real money.

## 9. Where it is genuinely weak

1. **No JTAG with sensors attached** — not fixable.
2. **No battery voltage sense** — fixable with external parts, at a quiescent-current cost.
3. **No camera power-down** — not fixable; caps deep-sleep performance and prevents sensor recovery without a power cycle.
4. **~4 free GPIOs** in a realistic configuration.
5. **Thermal behaviour** under sustained camera load; heat sinks are sold for a reason.

## 10. Evidence limitations

- **No hardware was tested.** No throughput, thermal, power or image-quality comparison was measured.
- **Non-Seeed prices are indicative, not observed** — only the Seeed store was queried, on one date, in USD.
- Comparisons rest on published specifications and design files. Where a claim depends on measurement (e.g. "the S3 is faster for TinyML"), it is stated as a specification-level expectation, not a benchmark result.
- No marketplace, distributor, used or clone pricing was sampled — see [`market-and-pricing.md` §6](market-and-pricing.md#6-what-was-not-sampled).

## 11. Related
- [`market-and-pricing.md`](market-and-pricing.md) · [`README.md`](README.md) · [`performance.md`](performance.md) · [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
