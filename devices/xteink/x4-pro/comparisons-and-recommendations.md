# Xteink X4 Pro — comparisons and recommendations

> Dated **2026-09-04**. Compares against records already in this knowledge base.
> Prices are item-only, region-worldwide-from-Shenzhen unless stated.

## The category confusion to avoid first

The X4 Pro is a **sealed consumer product**. The PaperMono, Waveshare boards and
ZeroWriter are **development platforms**. The community routinely compares them on
price, and that comparison is close to meaningless:

> "Half the price of the XTEINK X4 Pro"
> — Hacker News on the PaperMono launch, recorded in
> [`../../m5stack/papermono/comparisons-and-recommendations.md`](../../m5stack/papermono/comparisons-and-recommendations.md)

A dev board has headers, a published schematic, USB-C, no unlock dance and no
enclosure. A sealed reader has an enclosure, a battery, a case ecosystem and a
locked bootloader. **Pick by what you are building, not by dollars per pixel.**

Notably, the previous pass on the PaperMono recorded *"the XTEINK X4 Pro — the
comparison the community actually makes — was never priced."* **It is now: $99.00
as of 2026-09-04.** See [`market-and-pricing.md`](market-and-pricing.md).

That pass also described the X4 Pro as *"a sealed consumer reader with locked-down
firmware… **You cannot put your own application on it**"*. **That is now known to
be wrong**, and this record supersedes it: the X4 Pro runs at least four
independent open-source firmwares, the vendor sells a developer-unlocked variant,
and USB-locked units can be unlocked over OTA or flashed from SD. See
[`development.md`](development.md#usb-lock).

## Against the rest of the Xteink family

| | **X4 Pro** | [X4](../x4/README.md) | [X3](../x3/README.md) | [X4 Classic](../x4-classic/README.md) |
|---|---|---|---|---|
| SoC | **ESP32-S3** | ESP32-C3 | ESP32-C3 | **ESP32-S3** |
| PSRAM | **8 MB** | none | none | **8 MB** |
| Panel | 4.26″ 800×480 | 4.26″ 800×480 | 3.7″ 792×528 | 4.26″ 800×480 |
| PPI | ~219 | ~219 | **~257** | ~219 |
| Touch | **✅ GT911** | ✗ | ✗ | ✗ |
| Frontlight | **✅ warm/cool** | ✗ | ✗ | ✗ |
| Buttons | 2 + power | 6 + power (ADC ladder) | 6 + power (ADC ladder) | **6 + power (all discrete)** |
| IMU | ✗ | ✗ | **✅ QMI8658** | **✅ QMI8658** |
| RTC | BM8563 @0x51 | **none** | DS-series @0x68 | BM8563 @0x51 |
| Gauge | CW2017 | none (ADC) | BQ27220 | CW2017 |
| SD | **SDMMC 1-bit** | SPI (shared with display) | SPI (shared) | **SDMMC 1-bit** |
| NFC | ✗ | ✗ | **✅ ISO 14443A tag** | ✗ |
| Charging | **pogo only** | USB-C | pogo | not established |
| Price | **$99** | delisted | $69 | not listed |

**The three surprises in that table.** The "Pro" has **no IMU** while both cheaper
siblings do; the X4 has **no RTC at all**; and the **X3 has the highest pixel
density in the family** despite being the cheapest and smallest.

## Against development platforms in this knowledge base

| Device | Price (dated) | Class | Schematic | USB-C | Headers | Unlock needed | Verdict vs X4 Pro |
|---|---|---|---|---|---|---|---|
| **X4 Pro** | $99 (2026-09-04) | sealed reader | ✗ | data only | ✗ | often | — |
| [M5Stack PaperMono](../../m5stack/papermono/README.md) | see its record | dev board | **✅ published** | ✅ | ✅ | ✗ | **Better for development.** Worse as a reader — no enclosure, no case ecosystem |
| [Waveshare e-paper ESP32 boards](../../waveshare/) | varies | dev board | partial | ✅ | ✅ | ✗ | Cheapest route to a panel; you supply everything else |
| [ZeroWriter](../../zerowriter/) | see its record | DIY appliance | ✅ open | ✅ | ✅ | ✗ | Different purpose — a writing appliance, keyboard-first |

**Not equivalents, partial substitutes at most.** They share the "ESP32 driving
e-paper" workload and nothing else: no shared enclosure, battery management, case
ecosystem or panel size.

## Against the S4 — the interesting one

The [S4](../s4/README.md) is Xteink's own **Android 11** device: 2 GB RAM, 32 GB
storage, 1400 mAh, 6.98 mm, 95 g, touch, warm/cool frontlight, at ~**¥339
(≈US$50)** in China.

On paper it beats the X4 Pro on every consumer axis at half the price. It is
**not** a substitute if you intend to run your own firmware: it is a different
platform with no FreeInk SDK support, no board profile, and no community firmware.
**If you will never flash it, the S4 is probably the better buy** — and the
community says so, e.g. *"I probably will abandon both once the S4 is released"*
([r/xteinkereader `1syav96`](https://old.reddit.com/r/xteinkereader/comments/1syav96/), 412 pts).

## Clones

**None found.** No clone or white-label variant of any Xteink device was located
in this session. Given the price point and Shenzhen origin this is mildly
surprising and may simply reflect that Chinese marketplaces were not searched —
see [`research-log.md`](research-log.md).

## Recommendations by scenario

| Scenario | Recommendation | Why |
|---|---|---|
| **Pocket reader you intend to reflash, want touch + light** | **X4 Pro**, 2026-09-04, $99 | Nothing else in the family or price bracket has both, with an active firmware scene |
| Pocket reader, buttons are fine, want the sharpest text | **X3**, $69 | ~257 PPI, plus an IMU and NFC |
| Pocket reader, buttons, want S3 power and an IMU | **X4 Classic** — **if you can buy one** | Not listed internationally |
| **Building a product / need a schematic** | **PaperMono** or a Waveshare board | Published schematic, headers, USB-C, no unlock |
| Want e-paper + Android + apps | **S4** | Different platform; no self-built firmware |
| **Cannot tolerate a proprietary charging cable** | Not the X4 Pro. X4 (USB-C) if you can find one used | This is the single most common owner complaint |
| Need an IMU on an S3 | X4 Classic, **not** the X4 Pro | The Pro has none |

## Honest limits of this comparison

- **No X4 Pro was measured.** No benchmark, power figure or runtime exists here or
  anywhere found.
- **Battery capacity is unknown**, so battery life cannot be compared at all.
- PaperMono/Waveshare/ZeroWriter prices are not restated here because they were
  captured on different dates; follow the links for dated figures.

---

## Cross-references added 2026-09-07

Append-only, from a cross-cutting synthesis pass. Nothing above was changed and no
new evidence was gathered.

- [**Handheld and e-ink device landscape, 2026-09**](../../../guides/markets/handheld-and-eink-device-landscape-2026-09.md)
  — the $30 touch-plus-frontlight premium priced against the rest of the family and
  against the PaperMono, plus the group-level list of comparisons the evidence does
  not support.
- [**Xteink firmware ecosystem**](../firmware-ecosystem.md) — the X4 Pro as the
  ecosystem's **design floor** and the **only target of the native-ELF plugin
  fork**, with the full `VER (0x70)` / `FLG (0x71)` controller-detection procedure
  and the `CHIP_VER = 0x00` negative result that must not be re-broken.
- [**Adding LoRa, NFC and an RGB sidelight to e-ink firmware**](../../../guides/hardware/adding-lora-nfc-and-sidelight-to-eink-firmware.md)
  — **the crux**: the native plugin host runs on this device, and its 81-symbol
  allow-list contains **no I²C, no SPI, no GPIO, no ADC/PWM/LEDC, no Wi-Fi and no
  filesystem**. Every radio or lighting capability therefore needs a firmware
  change — but a small, structured one, not a fork of the reader.
- [**SoC choice for battery e-ink devices**](../../../guides/hardware/soc-choice-for-battery-eink-devices.md)
  — what the 8 MB PSRAM here actually buys over the C3 siblings, and the pin cost
  (**GPIO33–37 and `SPICS1` are consumed in-package**) of the `R8` variant.
