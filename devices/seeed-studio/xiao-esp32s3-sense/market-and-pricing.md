# Market and pricing — XIAO ESP32S3 Sense

> Dated price observations and what they imply. Snapshot **2026-08-24**.
> **Scope warning:** all observations below are from the **official Seeed store, in USD, on one date**. Marketplace (AliExpress/Taobao), distributor, used and clone pricing were **not sampled** — see [§6](#6-what-was-not-sampled).

## 1. Observed prices — Seeed official store, 2026-08-24

Extracted from each product page's structured data (`schema.org/Offer`) and the rendered final price. Raw capture: [`artifacts/pricing-observations.json`](artifacts/pricing-observations.json).

| Product | SKU | List | **Final** | Stock |
|---|---|---:|---:|---|
| **XIAO ESP32S3 Sense** | 113991115 | $13.99 | **$13.99** | In stock |
| XIAO ESP32S3 (plain) | 113991114 | $7.49 | **$7.49** | In stock |
| XIAO ESP32S3 Plus | 102010671 | $7.90 | — | In stock |
| XIAO ESP32C6 | 113991254 | $5.20 | **$5.20** | In stock |
| XIAO ESP32C3 | 113991054 | $4.99 | **$4.99** | In stock |
| XIAO nRF52840 Sense | 102010469 | $15.99 | **$12.99** | In stock |
| OV5640 camera upgrade (with heat sink) | 114993115 | $12.99 | **$11.99** | In stock |
| Wio-SX1262 LoRa for XIAO | 102010611 | $10.90 | — | In stock |

All prices exclude shipping, tax and duty. Currency USD, captured 2026-08-24.

## 2. What the Sense daughterboard costs

$13.99 − $7.49 = **$6.50** for the camera + PDM microphone + microSD slot + board-to-board connector.

That is the central economic fact about this product. $6.50 for a 3 MP camera, a digital microphone and an SD slot — all detachable — is the reason the board dominates its niche. Nothing else in the XIAO line, and very little elsewhere, adds that much capability for that little.

It also frames the buying decision: **if you are unsure whether you need the camera, buy the Sense anyway.** The daughterboard detaches, so you have not committed to anything except $6.50 and a slightly worse deep-sleep figure.

## 3. Upgrading to the OV5640

The OV5640 upgrade at **$11.99** costs **86 % of the entire Sense board**. Buying a Sense ($13.99) plus the OV5640 ($11.99) = **$25.98**, which is more than double the base price.

What you get for it: 5 MP instead of 3 MP, autofocus, 1080p30 instead of 1080p20, and a heat sink. What you also get: **140 mA** active current instead of 98 mA, and a sensor that runs hot enough that Seeed bundles cooling.

**Recommendation:** buy the OV5640 only if you specifically need **autofocus** or resolution above 2048 × 1536. For streaming, machine vision and TinyML — the overwhelming majority of use cases — the stock OV3660 is the better engineering choice *and* costs nothing extra. The ESP32-S3 cannot sustain 5 MP frame rates anyway; you are paying for pixels the board cannot move.

## 4. Position within the XIAO line

| Board | Price | Radio | Buy it for |
|---|---:|---|---|
| XIAO ESP32C3 | $4.99 | Wi-Fi 4 + BLE | Cheapest Wi-Fi. RISC-V, single core |
| XIAO ESP32C6 | $5.20 | **Wi-Fi 6**, BLE, Zigbee, Thread | Matter/Thread. Best value for modern protocols |
| XIAO ESP32S3 | $7.49 | Wi-Fi 4 + BLE | Dual-core Xtensa, **8 MB PSRAM**, native USB |
| **XIAO ESP32S3 Sense** | **$13.99** | Wi-Fi 4 + BLE | **Camera + mic + SD** |
| XIAO ESP32S3 Plus | $7.90 | Wi-Fi 4 + BLE | 16 MB flash, 18 GPIO, 2× UART/SPI |
| XIAO nRF52840 Sense | $12.99 | **BLE only** | IMU + mic, **µA-class sleep**, battery sensing |

Two comparisons worth drawing out:

**The Plus at $7.90 is only $0.41 more than the plain S3** and gives 16 MB flash and 18 GPIOs instead of 11. If you are *not* buying for the camera, the Plus is almost strictly the better board — with the important caveat that **its B2B connector is not compatible with the Sense camera daughterboard** (it does fit the Wio-SX1262 LoRa board).

**The nRF52840 Sense at $12.99 is a dollar cheaper than the ESP32S3 Sense** and is the better choice for battery-powered BLE sensing: it has an IMU, genuinely low sleep current, and — unlike this board — **battery voltage sensing**. It has no camera and no Wi-Fi.

## 5. Cost of a complete build

Realistic bills of materials, official-store prices, excluding shipping:

| Build | Parts | Total |
|---|---|---:|
| Bare Wi-Fi camera | Sense | **$13.99** |
| Battery-powered camera | Sense + 3.7 V LiPo (~$5) + antenna (incl.) | **~$19** |
| Camera + autofocus | Sense + OV5640 | **$25.98** |
| Camera + LoRa | Sense + Wio-SX1262 | **$24.89** — ⚠ but see B2B incompatibility note |
| Wearable | Sense + LiPo + 3D-printed case + heat sink | **~$22–25** |

For context, the "$20 AI smart glasses" (OpenGlass) figure that made this board well known is consistent with these numbers: board + battery + printed mount.

## 6. What was not sampled

Stated plainly, because the omissions materially affect any purchasing conclusion:

- **Marketplace pricing** — AliExpress, Taobao, Amazon, eBay. Seeed is a Shenzhen company and these boards are widely resold; marketplace prices are often meaningfully below official, sometimes with genuine stock, sometimes not.
- **Authorised distributors** — Mouser, DigiKey, Arrow, Farnell. These typically carry official pricing plus volume breaks and are the relevant channel for production quantities.
- **Regional variation** — one currency (USD), one storefront. Seeed operates regional stores with different pricing and shipping.
- **Volume breaks** — not captured; the Seeed store shows tiered pricing on many SKUs.
- **Used / refurbished** — not sampled.
- **Clones and compatibles.** No assessment was made of whether clones of this board exist. Given the CC BY-SA 4.0 design files, clones are *legally straightforward* to produce, which is unusual and makes their existence plausible — but **plausible is not evidence**, and none were located because no marketplace search was performed.
- **Launch pricing** — not established. Only current pricing was observed, so no price-trend claim can be made.
- **Shipping, tax and duty** — excluded throughout, and for a $14 board international shipping can easily exceed the item price.

**Do not treat the table in §1 as a market survey.** It is a single-vendor, single-date, single-currency snapshot. It is reliable for *relative* comparisons within the XIAO line (same store, same day) and unreliable as a statement about what you will actually pay.

## 7. Availability and lifecycle

- All products checked showed **`InStock`** on 2026-08-24.
- The product is **actively maintained**: schematics were re-released 2026-02, the reference-design catalogue is dated 2025-11, and board revision v1.3 dates from 2025-10. This is not a coasting product.
- **The camera sensor changed mid-life** (OV2640 → OV3660) without an SKU change — a supply-chain substitution you should expect to be repeated. Design so your code detects the sensor at runtime rather than assuming one. See [`gaps-and-conflicts.md` §5](gaps-and-conflicts.md#5-the-camera-sensor-fitted-has-changed-and-the-product-page-is-stale).

## 8. Related
- [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) — versus non-XIAO alternatives
- [`README.md`](README.md) — when to use / when not to use
- [`artifacts/pricing-observations.json`](artifacts/pricing-observations.json) — raw capture
