# OPSCO SK6805-EC20 (filed under "Normand")

> 2020-package addressable RGB LED with an integrated controller — a NeoPixel-class single-wire device in a 2.0 × 2.0 mm footprint. On the Tanmatsu, six of them run from the PMIC's 5 V boost rail behind a Schmitt-trigger level shifter.
> Research snapshot **2026-08-30**. Fitted as `U27`–`U32` on the Nicolai Electronics Tanmatsu. **No hardware was available.**

---

## Evidence labelling

| Tag | Meaning |
|---|---|
| **[DS]** | 产品规格书 / Product Specification **SK6805-EC20-001, Rev. A1, dated 2025-08-25**, 13 pp, bilingual 中文/English — `artifacts/sk6805-ec20-datasheet.pdf` |
| **[PCB]** | `tanmatsu.kicad_pcb` pad→net assignments (CERN-OHL-P) |
| **[INF]** | Author inference |

---

## 1. ⚠ Identity — the manufacturer in this record's path is wrong

This component is filed at `components/normand/sk6805-ec20/`, because the Tanmatsu BOM cites **LCSC [`C2890036`](https://www.lcsc.com/search?q=C2890036)**, which LCSC attributes to the brand **"Normand"**.

**The datasheet says otherwise.** Every page of [DS] is headed:

> **广东欧思科科技股份有限公司** — **GuangDong OPSCO Technology Co., Ltd.**
> 官网 / web: `www.opscoled.com` · 地址: 东莞市企石镇上美路3号 (Dongguan, Guangdong)
> 电话 (769) 82632725

with document number **`SK6805-EC20-001`**, SAP part number `10205E6805A20003A0`, revision **A1**, dated **2025-08-25**.

| Attribution | Source | Confidence |
|---|---|---|
| **OPSCO (广东欧思科)** | The manufacturer's own specification sheet, which carries its stamp, address and approval signatures (雷梁晨 / 张国保 / 朱更生) | **High — primary** |
| "Normand" | LCSC catalogue brand field | Low — distributor metadata |

"SK68xx" is a widely second-sourced part family, and LCSC's brand attribution for commodity LEDs is unreliable. The conflict is recorded rather than resolved: the **directory path is not corrected here**, because renaming a component directory would break links from device records this session cannot edit. **This is a rename that should be made** — see the session report.

| Property | Value | Source |
|---|---|---|
| Part | **SK6805-EC20** (document `SK6805-EC20-001`) | [DS] |
| Manufacturer | **GuangDong OPSCO Technology Co., Ltd.** | [DS] |
| Package | **EC20** — 2.0 × 2.0 mm, 4-pin, top-emitting | [DS] §4 |
| Lens | **Translucent** | [DS] §Overview |
| Colours | RGB, integrated driver IC | [DS] |
| Greyscale | **256 levels per channel** (8 bit × 3 = 24 bit) | [DS] §Overview |
| Cascade | **Single-line zero-code protocol, infinitely cascadable** | [DS] §Overview |
| Datasheet revision | **A1, 2025-08-25** — recent | [DS] |
| ESD | Marked **ELECTROSTATIC SENSITIVE DEVICE** | [DS] |

---

## 2. Electrical characteristics **[DS] §9**

| Parameter | Symbol | Min | Typ | Max | Unit |
|---|---|---:|---:|---:|---|
| **Working / chip input voltage** | `VDD` | **+3.5** | **5.0** | **+5.5** | V |
| Forward voltage (OUT G/R/B) | — | — | **5 V @ 5 mA** | — | — |
| **Static power consumption** | `IDD` | — | **0.5** | — | mA |
| **Transfer rate** | `FDIN` | — | **800** | — | Kbps |
| Luminous intensity tolerance | — | — | ±10 % Iv | — | — |
| Dominant wavelength tolerance | — | — | ±1.0 nm | — | — |

### 2.1 ⚠ The 3.5 V minimum is the specification that decides your board

**`VDD` minimum is +3.5 V** **[DS] §9**. A 3.3 V rail is **out of specification** — nominally, and with any droop, well out.

This single number is why the Tanmatsu runs its LED chain from the PMIC's 5 V rail rather than the 3.3 V logic rail (§4), and it is the most common reason SK68xx chains behave erratically on 3.3 V microcontroller boards: they often *appear* to work at 3.3 V and then fail on temperature, on a longer chain, or on a different production lot. Design for 5 V.

### 2.2 Power budget

At **0.5 mA static** per device the quiescent cost of a chain is small, but the LEDs themselves are not. Taking the 5 mA per-channel forward current from [DS]:

| State | Per LED | 6 LEDs (Tanmatsu) |
|---|---:|---:|
| Static, all channels off | ~0.5 mA | **~3 mA** |
| One channel at full | ~5.5 mA | ~33 mA |
| White, all three at full | ~15.5 mA | **~93 mA** |

Two consequences for a battery device:

1. **Full white on six LEDs is roughly 93 mA at 5 V ≈ 0.5 W** — a substantial fraction of a handheld's idle budget, before boost-converter losses.
2. **Even "off" is not free.** The 0.5 mA static draw is *per device* and is present whenever `VDD` is applied, regardless of the colour data. The only way to reach zero is to remove the supply — which on the Tanmatsu means disabling the PMIC's boost converter entirely (§4.2).

---

## 3. The single-wire protocol **[DS] §10, §11]**

24 bits per LED, sent **MSB first**, in **GRB** order (not RGB — a classic bug source). Each bit is encoded as a fixed-period pulse whose *duty cycle* carries the value.

### 3.1 Timing — real values from the datasheet

| Symbol | Meaning | Min | **Actual (typ)** | Max | Unit |
|---|---|---:|---:|---:|---|
| **`T`** | Symbol period | 0.90 | **1.20** | 20 | µs |
| **`T0H`** | 0 code, high-level time | 0.20 | **0.30** | 0.40 | µs |
| **`T0L`** | 0 code, low-level time | 0.70 | **0.90** | — | µs |
| **`T1H`** | 1 code, high-level time | 0.70 | **0.90** | — | µs |
| **`T1L`** | 1 code, low-level time | 0.20 | **0.30** | — | µs |
| **`Reset`** | Reset code, low-level time | **200** | — | — | µs |

Points worth extracting:

- **The symbol period maximum is 20 µs, not 1.25 µs.** The device tolerates a very long low time mid-frame — up to 20 µs — before the level is treated as a reset. That is far more forgiving than the 800 kHz nominal rate suggests, and it is why bit-banged drivers survive short interrupt jitter. But **a single low excursion beyond ~200 µs latches the frame**, so a long ISR at the wrong moment splits one frame into two and produces the familiar "half the strip updates" glitch.
- **`T0H` has a hard maximum of 0.40 µs.** This is the tightest constraint in the table and the one that breaks marginal drivers: a 0-bit high pulse longer than 400 ns may be sampled as a 1. `T1H` has *no* specified maximum, so erring long on 1-bits is safe and erring long on 0-bits is not.
- **Reset is ≥ 200 µs**, notably longer than the ~50 µs quoted for older WS2812 parts. A driver ported from WS2812 timing may use too short a latch gap and produce intermittent updates.

### 3.2 Cascading

> *"D1 is the data sent by the MCU end, and D2, D3 and D4 are the data automatically shaped and forwarded by the cascaded circuit."* — [DS] §10

Each device consumes the first 24 bits, **reshapes and regenerates** the remainder, and passes them on. Because every stage retimes the signal, cascade length is not limited by signal integrity — [DS] states the protocol is *"infinitely cascadable"*, and that **at 800 Kbps with a 30 fps refresh rate the cascade length is not less than 1024 devices** **[DS] §Overview**.

That figure is a useful sanity check: 1024 × 24 bits ÷ 800 kbit/s ≈ **30.7 ms per frame**, which is indeed ~30 fps. Frame time scales linearly with chain length, so refresh rate and chain length trade directly.

---

## 4. Exact wiring on the Tanmatsu **[PCB]**

Six devices, `U27` through `U32`, in a cascaded chain.

### 4.1 They run from the PMIC's 5 V boost rail, not from 3.3 V

**All six `VDD` pins are on the `VOTG` net** **[PCB]** — the [BQ25895](../../texas-instruments/bq25895/README.md)'s `PMID` output, its OTG boost converter rail.

The full `VOTG` consumer list:

| Ref | Part | Role |
|---|---|---|
| **`U27`–`U32`** | **SK6805 × 6** | The RGB LEDs |
| **`U26`** | **74LVC1G17GW,125** | Schmitt-trigger buffer — see §4.2 |
| `U14` | SY6280AAC | USB-A host port power switch |
| `J7` pin 1 | Internal add-on port | 5 V out to expansion boards |
| `C49`, `C51`, `C53`, `C54`, `C55` | 5 × 10 µF | Bulk decoupling |
| `U15` pin 23 | BQ25895 `PMID` | The source |

This is the correct design given §2.1 — a 3.3 V rail would be below the 3.5 V minimum.

### 4.2 ⚠ "Turn on an LED" transitively means "enable a boost converter"

Because `VOTG` is the PMIC's OTG output, **the LEDs are dead unless `OTG_CONFIG` (BQ25895 REG03 bit 5) is set**. And on the Tanmatsu the ESP32-P4 has no path to the PMIC at all — the charger sits on a private I²C bus owned by the CH32V203 coprocessor. So the call chain is:

```
application  →  coprocessor (I²C 0x5F)  →  BQ25895 (private I²C 0x6A)  →  OTG boost on
             →  coprocessor drives the LED data line  →  U26 buffer  →  U27..U32
```

Costs that follow:

- The boost converter's own quiescent draw is **~5 mA** typical while switching **[BQ25895 datasheet §7.5]** — an order of magnitude more than the LEDs' 3 mA static draw. Enabling the rail for the sake of one indicator LED is expensive.
- Enabling `VOTG` also powers the **USB-A port switch** and the **add-on connector's 5 V pin**. The rail is shared; you cannot enable it for the LEDs alone.

### 4.3 The level shifter is a Schmitt-trigger buffer, and it is not optional

`U26` = **74LVC1G17GW,125** — a single-gate **Schmitt-trigger buffer**, powered from `VOTG` (5 V) **[PCB]**.

Its job is to translate the coprocessor's **3.3 V** data output up to a **5 V** logic swing for the LED chain. This matters because the SK6805's `DIN` threshold is referenced to its own 5 V `VDD`; a 3.3 V high is marginal against a 5 V-referenced input, and marginal is exactly where single-wire chains produce colour corruption on the first device only.

The choice of a **Schmitt-trigger** part (the `G17`, rather than a plain `G34` buffer) additionally cleans up edges — useful given the 400 ns maximum on `T0H` (§3.1). [INF]

The LEDs are **driven by the CH32V203 coprocessor**, not the ESP32-P4 — consistent with the coprocessor owning the keyboard backlight and the power management. See `leds.c` (146 lines) in the coprocessor firmware.

---

## 5. Driving techniques on ESP32

The protocol needs sub-microsecond timing with a 400 ns tolerance on `T0H`. Three approaches, in descending order of robustness:

| Method | How | Verdict |
|---|---|---|
| **RMT peripheral** | ESP32's Remote Control peripheral generates arbitrary pulse trains from DMA-fed symbol pairs. `led_strip` (Espressif's component) and the ESP-IDF `rmt_tx` driver do this | ✅ **The right answer on ESP32.** Hardware-timed, immune to interrupt jitter, DMA-backed. `espressif/led_strip` supports both RMT and SPI back-ends |
| **SPI MOSI** | Encode each LED bit as 3 or 4 SPI bits at ~2.4–3.2 MHz, so the bit pattern's duty cycle synthesises `T0H`/`T1H` | ✅ Good where RMT channels are exhausted. Costs 3–4× the RAM. Timing granularity is coarser — check the encoding lands inside the 200–400 ns `T0H` window |
| **Bit-banging with interrupts disabled** | `NOP` loops | ⚠ Works, but any missed deadline corrupts the frame, and disabling interrupts for `24 × N × 1.2 µs` (≈ 173 µs for 6 LEDs) is hostile to Wi-Fi and USB |

**On the Tanmatsu none of this applies to the application processor** — the chain is driven by the CH32V203 coprocessor, and the ESP32-P4 asks the coprocessor over I²C. The techniques above are for the general case.

**Timing configuration for RMT**, from §3.1, at typical values:

```
T0H = 0.30 µs (range 0.20–0.40)   T0L = 0.90 µs (min 0.70)
T1H = 0.90 µs (min 0.70)          T1L = 0.30 µs (min 0.20)
Reset ≥ 200 µs
```

Espressif's `led_strip` component defaults to WS2812 timing (`T0H` 0.3 µs, `T1H` 0.9 µs), which **matches the SK6805 typical values** — so the stock configuration works. The reset gap is the field to check, since WS2812 defaults are often ~50 µs and the SK6805 wants **≥ 200 µs**.

---

## 6. Pitfalls, in priority order

1. **`VDD` minimum is 3.5 V.** Do not run these from 3.3 V. It will appear to work and then not. §2.1.
2. **Colour order is GRB, not RGB.** §3.
3. **`T0H` maximum is 400 ns** — the tightest constraint. Long 0-bit pulses read as 1s. `T1H` has no maximum, so bias long on 1s. §3.1.
4. **Reset is ≥ 200 µs**, not the ~50 µs of older WS2812 drivers. Too short a gap gives intermittent updates. §3.1.
5. **A low excursion beyond ~200 µs mid-frame latches early** and splits the frame — the "only half the strip updated" symptom. Use RMT/DMA, not bit-banging under interrupts. §3.1, §5.
6. **Static draw is 0.5 mA per device, always**, whenever `VDD` is present. "All black" is not "off". §2.2.
7. **On the Tanmatsu, the LEDs require the PMIC boost converter**, which also powers the USB-A port and costs ~5 mA of its own. §4.2.
8. **Level-shift 3.3 V data to 5 V.** A marginal `DIN` high corrupts the *first* device only, which misleads people into suspecting that LED. §4.3.
9. **ESD-sensitive**, per the datasheet's own marking.

---

## 7. Alternatives

| Part | vs. SK6805-EC20 | When |
|---|---|---|
| **WS2812B-2020** | Same package class, same protocol, ~5 V | The most common second source; near-drop-in |
| **SK6812** | 5050 package, same protocol, RGBW variants available | When you want white or a bigger emitter |
| **WS2812B-Mini / 3535** | Intermediate sizes | Density trade |
| **SK6805-EC15** | **1.5 × 1.5 mm** — smaller sibling | Extreme density |
| **APA102 / SK9822** | **Two-wire (clock + data) SPI** | ⭐ When timing robustness matters more than pin count — no critical timing at all, immune to interrupt jitter |
| **IS31FL3741 and similar** | I²C matrix driver + discrete LEDs | Many LEDs, no timing constraints, but far more parts |

**If you are designing new and can spare a pin, APA102/SK9822 removes this entire class of problem.** The single-wire protocol's appeal is one pin; its cost is a hard real-time constraint on the host forever after.

---

## 8. Open questions

- **The manufacturer attribution conflict in §1 is unresolved** at the filesystem level; the directory still says "normand".
- Per-channel forward current is given only as "5 V @ 5 mA (OUT GRB)" **[DS] §Overview**; the datasheet's electrical table does not break out per-colour drive current, so §2.2's totals are [INF] extrapolations.
- Whether the Tanmatsu firmware ever enables `VOTG` solely for the LEDs, or only alongside USB-A use, was not established from the coprocessor firmware.
- No hardware measurement of chain current or timing margin.
- Luminous intensity and dominant wavelength per colour bin were not extracted from [DS] §9.

---

## Manufacturer

**GuangDong OPSCO Technology Co., Ltd.** (广东欧思科科技股份有限公司), Dongguan, Guangdong — `www.opscoled.com`. No vendor sourcing guide exists in this repository yet; the datasheet was not obtained from OPSCO but from **LCSC's mirror** (§9).

The repository path attributes this part to **Normand**, following LCSC's brand field. See §1 for why that is likely wrong.

## Used By

| Device | Refs | Role |
|---|---|---|
| [Nicolai Electronics Tanmatsu](../../../devices/nicolai-electronics/tanmatsu/README.md) | `U27`, `U28`, `U29`, `U30`, `U31`, `U32` | Six cascaded addressable RGB LEDs, powered from the BQ25895's **`VOTG` 5 V boost rail**, data driven by the **CH32V203 coprocessor** through a **74LVC1G17GW Schmitt buffer** (`U26`) that level-shifts 3.3 V → 5 V. See [`bom.md`](../../../devices/nicolai-electronics/tanmatsu/bom.md), [`keyboard.md`](../../../devices/nicolai-electronics/tanmatsu/keyboard.md) |

## Related pages

- [`components/texas-instruments/bq25895/README.md`](../../texas-instruments/bq25895/README.md) — supplies `VOTG`; §5.6 there lists every consumer of the rail
- [`components/wch/ch32v203c8t6/README.md`](../../wch/ch32v203c8t6/README.md) — drives the LED chain
- [`components/generic/lcd-panel-module/README.md`](../../generic/lcd-panel-module/README.md)

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | SK6805-EC20 产品规格书 / Product Specification | **GuangDong OPSCO Technology Co., Ltd.** | primary (via LCSC mirror) | datasheet | <https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2110250930_Normand-SK6805-EC20_C2890036.pdf> | 2026-08-30 | **`SK6805-EC20-001` Rev. A1, 2025-08-25**, 13 pp, 804 947 B | **All §2 electricals and §3 timing**; the §1 manufacturer identity | `artifacts/sk6805-ec20-datasheet.pdf` |
| S1 | `tanmatsu.kicad_pcb` | Nicolai Electronics | primary | repository | in-tree snapshot | 2026-08-24 | `tanmatsu-hardware` @ `640805dd`, CERN-OHL-P | §4 — the `VOTG` rail, the `U26` buffer, the six refdes | `devices/nicolai-electronics/tanmatsu/artifacts/schematics/kicad/tanmatsu.kicad_pcb` |

### 9. Acquisition record

Three attempts failed before one succeeded. All are recorded in `component-download-failures.txt`:

| URL | Result |
|---|---|
| `https://cdn-shop.adafruit.com/product-files/4960/4960_SK6805-EC20_REV02_EN.pdf` | HTTP 404 (9-byte `Not found`) |
| `https://cdn-shop.adafruit.com/product-files/4960/4960_SK6805-EC20_REV01_EN.pdf` | HTTP 404 |
| `https://cdn-shop.adafruit.com/product-files/4492/Datasheet.pdf` | ⚠ **HTTP 200, valid `%PDF`, 3 094 006 B — but the WRONG PART.** A 17-page image-only **iPixel LED** (Shenzhen) catalogue with no extractable text and no occurrence of "SK6805". Archived to `archive/components/normand/sk6805-ec20/artifacts/WRONG-PART-ipixel-catalog-adafruit-4492.pdf` rather than deleted |
| `https://datasheet.lcsc.com/lcsc/2110250930_Normand-SK6805-EC20_C2890036.pdf` | HTTP 200 but **`text/html`** anti-bot interstitial, 56 572 B. Rejected by magic-byte check |
| **`https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2110250930_Normand-SK6805-EC20_C2890036.pdf`** | ✅ **HTTP 200, `%PDF`, 804 947 B** — with a Chrome 131 UA and an `https://www.lcsc.com/` referer |

> **Reusable finding.** For LCSC-sourced datasheets, `datasheet.lcsc.com` serves an HTML interstitial to automated clients, but **`wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/<same-filename>`** serves the real PDF, given a Chrome User-Agent and an `lcsc.com` referer. A previous session recorded `wmsc.lcsc.com` returning only a 91-byte script stub for a different part; this session found the **`/v2/`** path works. Worth trying both.
>
> The Adafruit case is the cautionary one: **a valid 3 MB PDF that passes every automated check and is simply the wrong document.** Magic-byte validation is necessary but not sufficient — the content must be confirmed to mention the part.
