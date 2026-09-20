# E Ink ED052TC4 (and ED052TC2)

- **Category:** **5.2-inch active-matrix electrophoretic display (AMEPD) panel** — parallel source/gate-driver interface, 8 grey levels as driven, requiring an external multi-rail bias supply and a temperature-selected waveform
- **Panels covered:** **`ED052TC4`** (1280 × 720) and **`ED052TC2`** (960 × 540)
- **Research status:** ⚠ **No manufacturer datasheet exists publicly.** See §1. What follows is reconstructed from **primary design files** (three KiCad boards, complete connector pinouts), **primary driver source** (Inkplate Arduino library v11.1.4 and the MicroPython port), and **one genuine E Ink Corporation specification document** that a board vendor mirrored — `800-1101 Rev01`, the AF waveform-file spec, which is the authoritative source for §7 and §8
- **Retrieved:** 2026-08-24

---

## 1. ⚠ Start here: E Ink panel datasheets are NDA-gated, and this one is not public

This has to be stated plainly, because much of what circulates online about E Ink panels is guesswork presented as fact.

**What we tried, 2026-08-24:**

| Probe | Result |
|---|---|
| `https://www.eink.com/product/ED052TC4` | **HTTP 200 — but it serves the generic product-category page.** No per-part page exists |
| `https://www.eink.com/products` | 204 kB of marketing. A scan of the extracted text for `/ED\d{3}[A-Z0-9]*/` returned **zero part numbers**. E Ink does not publish a public part catalogue at all |
| `panelook.com` (the panel-specification database that does index E Ink part numbers) | **Slider-CAPTCHA bot block** on every request, with and without a browser User-Agent |
| `crystalfontz.com/product/ed052tc4` | 404 |
| DuckDuckGo HTML/lite endpoints | Bot-challenge page |

**And E Ink says so themselves.** The one E Ink-authored document we did obtain carries this on its first page **[DOC-EINK]**:

> *"This specification document is for use by **E Ink Corporation and their customers under non-disclosure agreements**. E Ink Corporation will be responsible for maintaining and controlling specification revisions."*

That is the business model, not an accident. E Ink sells to module integrators who receive a full panel specification, a per-lot waveform file and an applications engineer. A hobbyist reading a schematic is not a customer. Compare the identical posture at [Hynitron](../../../vendors/hynitron/README.md) and Sitronix.

**Consequences you must accept when working with this panel:**

- There is **no published pixel pitch, contrast ratio, reflectance, viewing angle, operating-temperature range, storage limit, ESD rating, mechanical drawing or bend radius** for the `ED052TC4`. Anything you find quoting such numbers is unsourced unless it cites an E Ink document.
- There is **no published interface timing diagram** — no setup/hold, no maximum `CL` frequency, no `CKV` pulse-width requirement. The Inkplate driver's numbers (§6.3) are the *de facto* spec because they demonstrably work, not because they are documented.
- There is **no published waveform**. The look-up tables in the Inkplate library (§7.2) were derived by Soldered for these specific panels and are the only ones in public circulation.

**What this record does instead:** it separates, explicitly and per-claim, what is *established from primary artifacts we hold* from what is *inferred*. Where something is unknown, it says so.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC-EINK]** | Stated by **E Ink Corporation** in `artifacts/eink-af-16-tone-grayscale-5bit-waveform-flash-file-spec-800-1101-rev01.pdf`. This is a genuine E Ink document (§9), but it is a **waveform-file format specification**, not a panel datasheet, and it does not name the `ED052TC4` |
| **[SCH]** | Read out of **resolved net names in the KiCad `.kicad_pcb`** files of the three boards (§9), via `devices/soldered-electronics/inkplate-5/tools/kicad_pcb_nets.py` |
| **[SRC]** | Read out of the Inkplate Arduino library **v11.1.4** or the Inkplate MicroPython library, with `file:line` |
| **[COM]** | Community or third-party evidence, attributed |
| **[INF]** | Inference. **Not** established by the above |

---

## 2. Identity and the two variants

| | **`ED052TC2`** | **`ED052TC4`** |
|---|---|---|
| Resolution | **960 × 540** | **1280 × 720** |
| Pixels | 518,400 | **921,600** |
| Diagonal | 5.2" | 5.2" |
| Relative pixel density | 1.0 | **1.78 ×** |
| Aspect | 16:9 | 16:9 |
| Grey levels as driven | **8** (3-bit) | **8** (3-bit) |
| Mainboard connector | **`AXE540127`**, 40-way | **`WP27D-S050VA3-R15000`**, 50-way |
| Used in | [Inkplate 5](../../../devices/soldered-electronics/inkplate-5/README.md) (`U11`) | [Inkplate 5 Gen 2](../../../devices/soldered-electronics/inkplate-5-gen2/README.md) (`U9`), [ZeroWriter Ink](../../../devices/zerowriter/zerowriter-ink/README.md) |
| Arduino board define | `ARDUINO_INKPLATE5` | `ARDUINO_INKPLATE5V2` |
| Waveform table | `boards/Inkplate5/waveforms.h` | `boards/Inkplate5V2/waveforms.h` — **different values** (§7.2) |

Part designators from the KiCad BOMs **[SCH]**; resolutions independently from the library headers **[SRC]**:

```c
// src/boards/Inkplate5/waveforms.h     #define E_INK_WIDTH 960   / E_INK_HEIGHT 540
// src/boards/Inkplate5V2/waveforms.h   #define E_INK_WIDTH 1280  / E_INK_HEIGHT 720
```

**This panel is the *only* difference between the two Inkplate 5 generations.** Same ESP32-WROVER, same [TPS65186](../../texas-instruments/tps65186/README.md), same [PCAL6416A](../../nxp/pcal6416a/README.md), same RTC, same bridge.

### 2.1 Reading the part number

**[INF]** — E Ink publishes no part-numbering guide. From the pattern across widely-observed E Ink parts (`ED060SC4`, `ED060XC3`, `ED097OC4`, `ED052TC2/TC4`):

```
ED  052  TC  4
│   │    │   └─ Revision / variant within the size+family. Here: resolution differs
│   │    └───── Two-letter family/technology code
│   └────────── Diagonal in hundredths of an inch: 052 = 5.2"
└────────────── "E Ink Display"
```

The `052` → 5.2" mapping is confirmed by the product listings for both Inkplate generations. **The meaning of `TC` is not established.** Do not repeat a decode of it without a source.

### 2.2 What generation of E Ink film is this?

**Unknown.** Not stated by Soldered, not marked on the panel, not derivable from the design files. The plausible candidates are **Carta** or the older **Pearl**; the E Ink document we hold (§9) is a *Carta* waveform specification, but that document was obtained from an unrelated Waveshare product page and **says nothing about the `ED052TC4`**. Treat any claim that this is "Carta 1.2" as unsupported. **[INF]**

### 2.3 Availability

You cannot buy an `ED052TC4` as a component from a distributor. It reaches the world in exactly two ways **[INF]** from the market structure described above:

1. Bonded into a finished product — an Inkplate 5 Gen 2 or a ZeroWriter Ink.
2. As pulls / grey-market stock on AliExpress and Taobao, unwarranted and undocumented.

Soldered sells the Inkplate as a *board*; there is no published spare-panel SKU.

---

## 3. What is actually established, at a glance

| Claim | Status |
|---|---|
| Resolutions 960×540 and 1280×720 | ✅ **[SRC]** + **[SCH]** |
| 5.2" diagonal | ✅ **[SCH]** part number + vendor product listing |
| 8 grey levels as driven by the Inkplate | ✅ **[SRC]** — the waveform table has 8 rows |
| Complete connector pinout, both variants | ✅ **[SCH]** — §5. This is the most useful thing in this record |
| Bias rails and their voltages | ✅ **[SCH]** + TPS65186 **[DOC]** |
| Signal names and which are fast vs slow | ✅ **[SCH]** + **[SRC]** |
| On-FPC SPI EEPROM exists | ✅ **[SCH]** — four SPI pins on the connector, unconnected on all three boards |
| On-FPC thermistor exists | ✅ **[SCH]** — `THERM` pin, unconnected on all three boards |
| Waveform LUT values used by Inkplate | ✅ **[SRC]** — §7.2 |
| Waveforms are temperature-dependent | ✅ **[DOC-EINK]** — §8.4 |
| Standard E Ink update-mode taxonomy and typical times | ✅ **[DOC-EINK]** — §8.1 (⚠ for *a* Carta panel, not necessarily this one) |
| Panel refresh times on Inkplate | ⚠ **[INF]** — calculated from the driver, §6.4. Not measured |
| Pixel pitch, contrast, reflectance, viewing angle | ❌ **Unknown** |
| Operating/storage temperature range | ❌ **Unknown.** The *board's* limit is the PMIC's −10 °C |
| Panel lifetime, update-count endurance | ❌ **Unknown.** No E Ink figure for this part |
| Maximum `CL` frequency and interface timing | ❌ **Unknown.** Only "what the Inkplate does" — §6.3 |
| Which E Ink film generation | ❌ **Unknown** — §2.2 |
| Correct VCOM | ❌ **Per-panel-lot by construction.** See [TPS65186 §9](../../texas-instruments/tps65186/README.md) |

---

## 4. Interface concept

These are **parallel "DES"-style** panels — the same architecture as the well-known `ED060SC4` used in early Kindles — **not** SPI e-paper modules like the small Waveshare/Good Display parts.

The critical distinction: **there is no controller chip in this panel.** A small SPI e-paper module contains an integrated controller (SSD1680, UC8151, IL0373…) with its own frame buffer, its own LUT registers, and a `display()` command. This panel has **row and column driver ICs only**. It has no memory. Every phase of every refresh must be clocked in from the host, in real time, line by line.

Everything a controller would normally do — hold the framebuffer, hold the previous image, sequence the waveform phases, time the gate scan, select a waveform by temperature — is the host's job. On an Inkplate that host is an ESP32 abusing its I2S peripheral as an LCD interface, with four framebuffers in PSRAM.

### 4.1 The signals

| Signal | Direction | Role | Where it is driven from |
|---|---|---|---|
| `D0`–`D7` | in | **Source data**, 8 bits = **4 pixels × 2 bits** (§6.2) | ESP32 GPIO 4, 5, 18, 19, 23, 25, 26, 27 via **I2S1 DMA** |
| `CL` | in | **Source shift clock** — one byte per pulse | ESP32 GPIO 0 (I2S BCK) via buffer `U8` |
| `LE` | in | **Latch enable** — transfers the shift register to the source drivers | ESP32 GPIO 2 |
| `SPH` | in | **Horizontal start pulse** | ESP32 GPIO 33 |
| `CKV` | in | **Gate clock** — advances the row scan | ESP32 GPIO 32 |
| `SPV` | in | **Vertical start pulse** — begins a frame | **Expander `P0_2`** |
| `OE` | in | **Output enable** for the source drivers | **Expander `P0_0`** |
| `GMOD` | in | **Gate mode** | **Expander `P0_1`** |
| `XON` | ? | Purpose **not established**. Pulled up 10 kΩ to `3V3-EINK` and broken out to a header pad; not driven by anything | **[SCH]** |
| `THERM` | out | Panel-internal thermistor | **Not connected** — header pad only |
| `SDI`/`SDO`/`SCL`/`NCS` | — | On-FPC **SPI EEPROM** (panel ID / factory VCOM) | **Not connected** — header pads only |
| `VDD2` (TC2) / `VDD_1V8` (TC4) | in | Secondary logic supply | **Not connected** — header pad only |

---

## 5. Connector pinouts

**This is the most concretely useful part of this record**, because it is a complete, primary-sourced pinout for a panel whose datasheet is not public. Extracted from the resolved PCB netlists **[SCH]**.

> **Caveat.** These are the pinouts of the **mainboard connectors that mate with the panel's flex**, read from Soldered's own design files. Soldered derived them from the panel specification we do not have. They are therefore an accurate description of *the Inkplate's* interface to the panel, and — since a mating connector must match — a strong reconstruction of the panel FPC pinout. Pin-1 orientation and any signals the panel presents but the mainboard leaves unrouted **cannot** be verified this way. **[SCH]** + **[INF]**

### 5.1 `ED052TC4` — 50-way, `WP27D-S050VA3-R15000` (`K21` on Gen 2 and ZeroWriter Ink)

| Pin | Net | Pin | Net |
|---:|---|---:|---|
| 1 | `VDDH` (+22 V) | 26 | `SPI-SDO` *(nc)* |
| 2 | `VDDH` | 27 | `SPI-NCS` *(nc)* |
| 3 | `GND` | 28 | `GND` |
| 4 | **`VCOM`** | 29 | *unconnected* |
| 5 | `VDD_1V8` **(nc)** | 30 | *unconnected* |
| 6 | `CKV` | 31 | *unconnected* |
| 7 | `D0` | 32 | `GND` |
| 8 | `D2` | 33 | `VPOS` (+15 V) |
| 9 | `D4` | 34 | `VPOS` |
| 10 | `D6` | 35 | `GND` |
| 11 | `LE` | 36 | `XON` |
| 12 | `CL` | 37 | `THERM` **(nc)** |
| 13 | `GND` | 38 | `AGND` **(nc)** |
| 14 | `3V3-EINK` | 39 | `OE` |
| 15 | `3V3-EINK` | 40 | `SPH` |
| 16 | `GND` | 41 | `D7` |
| 17 | `VNEG` (−15 V) | 42 | `D5` |
| 18 | `VNEG` | 43 | `D3` |
| 19 | `GND` | 44 | `D1` |
| 20 | *unconnected* | 45 | `SPV` |
| 21 | *unconnected* | 46 | `GMOD` |
| 22 | *unconnected* | 47 | `GND` |
| 23 | `GND` | 48 | `GND` |
| 24 | `SPI-SDI` *(nc)* | 49 | `VEE` (−20 V) |
| 25 | `SPI-SCL` *(nc)* | 50 | `VEE` |

*(Pad "51" in the netlist is the connector's mechanical shield, tied to `GND`.)*

Note the layout: **data lines are split across the two halves** — even-numbered data (`D0`, `D2`, `D4`, `D6`) on pins 7–10, odd (`D1`, `D3`, `D5`, `D7`) on pins 41–44 — and **every power rail is doubled** (`VDDH` ×2, `VNEG` ×2, `VPOS` ×2, `VEE` ×2, `3V3-EINK` ×2), with heavy ground interleaving. That is a deliberate high-current, low-inductance flex layout. **[SCH]** + **[INF]**

### 5.2 `ED052TC2` — 40-way, `AXE540127` (`K20` on Inkplate 5)

| Pin | Net | Pin | Net |
|---:|---|---:|---|
| 1 | `VNEG` | 21 | `D4` |
| 2 | `VPOS` | 22 | `D5` |
| 3 | `VNEG` | 23 | `D6` |
| 4 | `VPOS` | 24 | `D7` |
| 5 | `GND` | 25 | `CKV` |
| 6 | `GND` | 26 | `SPV` |
| 7 | `3V3-EINK` | 27 | `GMOD` |
| 8 | `XON` | 28 | `GND` |
| 9 | `3V3-EINK` | 29 | **`VCOM`** |
| 10 | `GND` | 30 | `GND` |
| 11 | `THERM` **(nc)** | 31 | `GND` |
| 12 | `OE` | 32 | `VDD2` **(nc)** |
| 13 | `CL` | 33 | `SCL` *(nc)* |
| 14 | `SPH` | 34 | `NCS` *(nc)* |
| 15 | `LE` | 35 | `SDI` *(nc)* |
| 16 | `GND` | 36 | `SDO` *(nc)* |
| 17 | `D0` | 37 | `GND` |
| 18 | `D1` | 38 | `AGND` **(nc)** |
| 19 | `D2` | 39 | `VDDH` |
| 20 | `D3` | 40 | `VEE` |

Here the data lines are contiguous on pins 17–24. **The two panels are not connector-compatible** — different pin count, different pitch, different ordering. A Gen 1 panel will not fit a Gen 2 board or vice versa. **[SCH]**

### 5.3 Three panel resources the Inkplate leaves on the table

All three are present on the flex and terminate on unpopulated header pads on **all three boards** **[SCH]**:

1. **The on-FPC SPI EEPROM** (`SCL`, `NCS`, `SDI`, `SDO`). On a normal E Ink integration this carries the panel's identity, its factory VCOM and often a waveform file. Because it is unrouted, **Inkplate firmware cannot discover which panel it is attached to, or what VCOM that panel wants.** VCOM must be programmed into the PMIC at manufacture; swap a panel and you inherit the previous one's calibration. See [TPS65186 §9.6](../../texas-instruments/tps65186/README.md).
2. **The panel thermistor** (`THERM`, with `AGND` as its return). Unrouted. The PMIC instead reads a **board-mounted** NTC (`R2`) sitting next to itself. Since waveform selection is temperature-driven, the sensor that matters is the one measuring the film — and it is on a pad. See [TPS65186 §6.3](../../texas-instruments/tps65186/README.md).
3. **`VDD_1V8` / `VDD2`.** A secondary logic supply pin, unrouted on both generations. The panels evidently do not require it in this configuration. **[SCH]**; why it exists is **[INF]** — most likely an alternative low-voltage interface option.

`XON` is the fourth oddity: pulled to `3V3-EINK` through a 10 kΩ (`R48` / `R47` depending on board) and broken out. **Its function is not established.** **[SCH]**

---

## 6. How the Inkplate actually drives it

### 6.1 The ESP32 has no LCD peripheral, so Soldered uses I2S

`pinsAsOutputs()` routes the I2S1 peripheral onto the panel bus **[SRC]** (`Inkplate5V2Driver.cpp:624-650`, `setI2S1pin(0, …)` at line **633**):

```c
setI2S1pin(0,  I2S1O_BCK_OUT_IDX,   0);   // CL   <- GPIO0  (through buffer U8)
setI2S1pin(4,  I2S1O_DATA_OUT0_IDX, 0);   // D0
setI2S1pin(5,  I2S1O_DATA_OUT1_IDX, 0);   // D1
setI2S1pin(18, I2S1O_DATA_OUT2_IDX, 0);   // D2
setI2S1pin(19, I2S1O_DATA_OUT3_IDX, 0);   // D3
setI2S1pin(23, I2S1O_DATA_OUT4_IDX, 0);   // D4
setI2S1pin(25, I2S1O_DATA_OUT5_IDX, 0);   // D5
setI2S1pin(26, I2S1O_DATA_OUT6_IDX, 0);   // D6
setI2S1pin(27, I2S1O_DATA_OUT7_IDX, 0);   // D7
```

with the peripheral in **LCD mode** **[SRC]** (`system/UtilI2S/UtilI2S.cpp:54-70`):

```c
_i2sDev->conf2.lcd_en             = 1;
_i2sDev->conf2.lcd_tx_wrx2_en     = 1;
_i2sDev->sample_rate_conf.tx_bits_mod    = 8;
_i2sDev->sample_rate_conf.tx_bck_div_num = 2;
_i2sDev->clkm_conf.clkm_div_num   = _clockDivider;   // default 5
// "Do not use APLL, divide by 5 by default, BCK should be ~16MHz."
```

`CKV`, `SPH`, `LE` are bit-banged from the same loop through direct `GPIO.out_w1ts` / `out1_w1ts` register writes **[SRC]** (`boards/Inkplate5V2/pins.h:66-101`) — no `digitalWrite()` anywhere near the hot path.

### 6.2 ⚠ Two bits per pixel on the wire, and what the four codes mean

Each byte on `D0`–`D7` carries **four pixels, two bits each**. The four codes are recoverable from `clean()` **[SRC]** (`Inkplate5V2Driver.cpp:730-760`), which fills a whole line with one repeated code and documents what it does:

| 2-bit code | `clean(c, …)` fill byte | Meaning |
|---|---|---|
| `00` | `c = 2` → `0b00000000` | **Discharge** — "discharge the screen" |
| `01` | `c = 1` → `0b01010101` | **Drive dark** — "darken the screen" |
| `10` | `c = 0` → `0b10101010` | **Drive light** — "light screen" |
| `11` | `c = 3` → `0b11111111` | **Skip** — "skip all pixels", no drive |

That `11` = *no drive* is the key to partial update: unchanged pixels are simply never driven. `partialUpdate()` builds each byte as `LUTW[diffw] & LUTB[diffb]` **[SRC]** (`Inkplate5V2Driver.cpp:492-497`), where both tables default to `0xFF` (all-skip) and each bit that must move to white or to black replaces its pixel's `11` with `10` or `01` **[SRC]** (`graphics/GraphicsDefs.h:3-14`):

```c
const uint8_t LUTW[16]  = {0xFF, 0xFE, 0xFB, 0xFA, ... 0xAA};   // bit set -> 10 (light)
const uint8_t LUTB[16]  = {0xFF, 0xFD, 0xF7, 0xF5, ... 0x55};   // bit set -> 01 (dark)
const uint8_t LUT2[16]  = {0xAA, 0xA9, 0xA6, 0xA5, ... 0x55};   // full frame, no skip
const uint8_t discharge[16] = {0xFF, 0xFC, ... 0x00};           // bit set -> 00
```

### 6.3 Frame and line timing — the de facto interface spec

There is no published timing spec (§1), so this **is** the spec, in the sense that it demonstrably works on the shipping product.

**Frame start** — `vscan_start()` **[SRC]** (`Inkplate5V2Driver.cpp:170-192`): a fixed `CKV`/`SPV` dance with hard-coded microsecond delays totalling **71 µs**, described in the source as skipping "the first two lines that are invisible on screen":

```
CKV↑ 7µs, SPV↓ 10µs, CKV↓ CKV↑ 8µs, SPV↑ 10µs, CKV↓ CKV↑ 18µs, CKV↓ CKV↑ 18µs, CKV↓ CKV↑
```

**Per line** — one DMA burst of `E_INK_WIDTH/4 + 16` bytes (**336** bytes for the TC4, **256** for the TC2), then `vscan_end()`: `CKV↓`, `LE↑`, `LE↓`.

**Between phases** — `delayMicroseconds(230)` after every full-screen pass **[SRC]**.

> ⚠ **All of these constants are magic numbers with no published justification.** Change them and you are experimenting on a panel with no datasheet and no replacement supply. The 16 extra bytes per line, the 7/8/10/18 µs `CKV` intervals and the 230 µs inter-phase gap are the working values for these two panels. **[SRC]** + **[INF]**

### 6.4 Estimated refresh times

**[INF]** — calculated, **not measured**. Shown with the arithmetic so it can be checked or corrected.

At the vendor's stated ~16 MHz byte clock, a 336-byte TC4 line takes ≈ 21 µs, so one full-screen pass over 720 lines ≈ **15.1 ms** + 71 µs frame start + 230 µs inter-phase.

| Operation (`ED052TC4`) | Passes | Estimate |
|---|---:|---:|
| `clean()` sequence preceding every full update — `(0,1) (1,11) (2,1) (0,11) (2,1) (1,11) (2,1) (0,11)` | **48** | ≈ 740 ms |
| 1-bit image data — 3 × `LUTB`, 1 × `LUT2`, 1 × discharge | **5** | ≈ 77 ms |
| **`display()` in `INKPLATE_1BIT`** | **53** | **≈ 0.8 s** |
| 3-bit greyscale image data — 9 waveform phases | **9** | ≈ 139 ms |
| trailing `clean(3,1)` discharge | 1 | ≈ 15 ms |
| **`display()` in `INKPLATE_3BIT`** | **58** | **≈ 0.9 s** |
| **`partialUpdate()`** — 4 data passes + `clean(2,2)` | **6** | **≈ 92 ms** |
| `einkOn()` PMIC sequencing overhead, per update unless `leaveOn` | — | ≈ 30–100 ms |

> ⚠ **Two caveats on the byte rate.** First, `lcd_tx_wrx2_en = 1` may halve the effective data rate relative to BCK; we have not resolved this against the ESP32 TRM, so the true figures could be up to **2× longer**. Second, these are calculations, not measurements. Treat the table as an order-of-magnitude guide: **full refresh ≈ 1 s, partial ≈ 0.1 s.** Recording measured values here would be a genuinely useful contribution.

**The clean sequence dominates.** Roughly **90 %** of a full refresh is the black-white-black-white flashing, not the image. That is inherent to a high-quality e-paper update (§8.1) and it is why partial update exists.

**The two panels use different clean sequences** — `ED052TC2` uses nine stages with 14 repetitions, `ED052TC4` eight stages with 11 **[SRC]** (`Inkplate5Driver.cpp:261-269` vs `Inkplate5V2Driver.cpp:271-278`). Further evidence that these are genuinely different panels with different drive requirements, not one panel at two resolutions.

---

## 7. Waveforms and LUTs

### 7.1 The concept

An electrophoretic pixel is not addressed by a voltage — it is addressed by a **sequence of voltage pulses over time**. Getting a pixel from grey level 3 to grey level 6 means applying a specific, calibrated pattern of push-pull-rest frames. That pattern is the *waveform*, and it depends on:

- the **starting** grey level and the **target** grey level (so a full waveform is a 2-D table over transitions),
- the **temperature** of the film,
- the **panel lot** — E Ink states that each waveform file *"is specifically adjusted for a particular display module lot"* **[DOC-EINK]**.

This is why a proper E Ink integration ships a **waveform file** — a binary blob of temperature-indexed LUTs, CRC-protected, with a serial number, an FPL lot number, and a mode-version byte (§8.2). It is also why there is no such thing as a generic e-paper waveform.

### 7.2 What the Inkplate actually uses

An **8 × 9 table of 2-bit drive codes**: 8 grey levels × 9 phases. Values are the codes of §6.2 — `0` = discharge, `1` = darken, `2` = lighten **[SRC]**.

```c
// src/boards/Inkplate5V2/waveforms.h   -- ED052TC4
#define WAVEFORM3BIT \
    {{0,0,1,1,2,1,1,1,0}, {1,1,2,2,1,2,1,1,0}, {0,1,2,2,1,1,2,1,0}, \
     {0,0,1,1,1,1,1,2,0}, {1,2,1,2,1,1,1,2,0}, {0,1,1,1,2,0,1,2,0}, \
     {1,1,1,2,2,2,1,2,0}, {0,0,0,0,0,0,0,0,0}}
```
```c
// src/boards/Inkplate5/waveforms.h     -- ED052TC2
#define WAVEFORM3BIT \
    {{0,0,1,1,0,1,1,1,0}, {0,1,1,1,1,2,0,1,0}, {1,2,2,0,2,1,1,1,0}, \
     {1,1,1,2,0,1,1,2,0}, {0,1,1,1,2,0,1,2,0}, {0,0,0,1,1,2,1,2,0}, \
     {1,1,1,2,0,2,1,2,0}, {0,0,0,0,0,0,0,0,0}}
```

Observations, all **[SRC]**:

- **Row 7 (white, index 7) is all zeros** in both — the white end state requires no drive at all, because the clean sequence has already left the panel white.
- **Column 8 (the last phase) is all zeros** in both — every level ends with a discharge phase.
- **Row 4 is byte-identical between the two panels** (`0,1,1,1,2,0,1,2,0`); every other row differs. Coincidence or shared derivation is unknown.
- These are **absolute-target** waveforms, not transition tables: the index is the destination grey level only. That is legitimate **only because the clean sequence resets the whole panel to a known state first**, which is exactly why greyscale mode cannot skip it.

At runtime the table is expanded into a 256 × 9 byte look-up (`GLUT`/`GLUT2`, 2 × 9 kB in internal RAM) so that the inner loop can convert a packed byte of two 4-bit pixels straight into a bus byte **[SRC]** (`Inkplate5V2Driver.cpp:152-165` (`calculateLUTs()`)).

> ⚠ **These tables are Soldered's, not E Ink's.** They are a hand-tuned approximation to what a per-lot E Ink waveform file would provide, with **no temperature dimension at all** (§8.4). They are the only public waveforms for these panels.

### 7.3 A worked example of waveform tampering: the ZeroWriter 1 LUT patch

The predecessor device, ZeroWriter 1 (Raspberry Pi + a Waveshare 3.7" module), ships a Waveshare Python driver with **two waveform LUTs replaced**. The analysis is in [`zerowriter1-epaper-driver-notes.md`](../../../devices/zerowriter/zerowriter-ink/zerowriter1-epaper-driver-notes.md).

It is worth reading here because it illustrates the failure mode concretely, even though it concerns a **different panel, a different controller and a different device**:

- The LUTs in that driver are 105 bytes: ten 10-byte phase rows plus a 5-byte trailing group. In the stock tables the trailing group is `22 22 22 22 22`.
- ZeroWriter's patched `lut_4Gray_GC` moves the one surviving drive row to position 1 and **zeroes the trailing group**.
- If that trailing group is the per-phase frame count — the reading in those notes, marked there as **inferred and unconfirmed** — then every phase runs for zero frames and the **4-grey update is neutered**: the driver clocks data and triggers an update that does no driving.
- The two LUTs ZeroWriter left alone (`A2`, `DU`) are precisely the ones the fast 1-bit text path uses. Consistent with a product that only ever wants monochrome text.

**Scoping, restated:** ZeroWriter *Ink* — the device that uses the `ED052TC4` — does **not** use that Python library, that controller, or those LUTs. It runs ESP32 firmware on an Inkplate 5 Gen 2 respin. Treat the 3.7" LUT patch as lineage evidence about how these projects tune displays, not as documentation of this panel. **[COM]**

---

## 8. Refresh modes, ghosting and temperature

### 8.1 E Ink's own mode taxonomy — the authoritative version

**[DOC-EINK]**, §2.3 and Table 1 of `800-1101 Rev01`. This is E Ink Corporation's own description of the standard update modes for a Carta panel with an approved controller and PMIC, with **typical update times at 25 °C and 85 Hz frame rate**:

| Mode | Transitions supported | Ghosting | Intended use | Typical time |
|---|---|---|---|---:|
| **INIT** | anything → white | n/a | *"completely erase the display and leave it in the white state… useful where the display information in memory is not a faithful representation of the optical state"* | **2000 ms** |
| **DU** | any grey → **black or white only** | **Low** | Monochrome menus, text input, touch/pen | **260 ms** |
| **GC16** | 16 greys → 16 greys | **Very low** | **High-quality images.** The reference full update | **450 ms** |
| **GL16** | 16 greys → 16 greys | Medium | Text on a white background | 450 ms |
| **GLR16** | + states 29/31 | Low | Text on white, with an image-preprocessing algorithm | 450 ms |
| **GLD16** | + states 29/31 | Low | Text and graphics on white, reduced flash | 450 ms |
| **A2** | black/white only | **Medium** | **Fast page flipping**, animation, at reduced contrast | **120 ms** |
| **DU4** | any grey → 4 greys | Medium | Anti-aliased text in menus | 290 ms |

Two pieces of E Ink guidance that directly explain why e-readers behave the way they do **[DOC-EINK]** §2.3.8:

> *"The recommended update sequence to transition **into** repeated A2 updates… The use of a white image in the transition from 4-bit to 1-bit images will reduce ghosting and improve image quality for A2 updates."*
>
> *"It is also recommended to use a white image after a sequence of A2 updates"* — followed by a **GC16**.

**That is the white flash you see on a Kindle every few page turns**, specified by the manufacturer, not a bug.

> ⚠ **Applicability caveat.** `800-1101` describes the **AF** waveform for E Ink Carta panels driven by an *E Ink-approved Generation-II controller* with a flash waveform file. The Inkplate has none of that — no controller, no waveform file, no temperature LUTs, 8 greys rather than 16. **Use this table for the concepts and the relative magnitudes, not as specifications for the `ED052TC4`.** It is nevertheless the best primary description of e-paper update modes available outside an NDA.

### 8.2 What a real waveform file contains

**[DOC-EINK]** §3, Table 3 — useful because it shows exactly what the Inkplate approach is doing without:

| Offset | Field | Note |
|---|---|---|
| `0x00` | CRC32 checksum | over the whole file |
| `0x04` | File length | |
| `0x08` | Serial number | unique per released waveform file |
| `0x0E` | **FPL lot number** | **the film lot this waveform was tuned for** |
| `0x10` | Mode version | which of INIT/DU/GC16/… are present |
| `0x13` | Waveform type | `0x51` = AF |
| `0x15` | **AMEPD part number** | which panel |
| `0x18` | Frame rate | e.g. `0x55` = 85 Hz |
| `0x19` | **VCOM offset** | *"User should set the Vcom to VCOM stored in the module flash plus the VCOM_OFFSET"* |
| `0x1C` | XWIA | pointer to the waveform filename |

Note `0x19`: E Ink's model is **VCOM = the value in the panel's own flash + a waveform-specific offset**. The Inkplate cannot do this — the panel's SPI EEPROM is unrouted (§5.3) — so its VCOM is a single fixed number in the PMIC's EEPROM. **[DOC-EINK]** + **[SCH]** + **[INF]**

### 8.3 Ghosting, and why the library forces periodic full refreshes

**Ghosting** is residual optical state from a previous image, caused by pixels being left partly-driven. It accumulates: each partial update touches only changed pixels, so errors in untouched pixels never get corrected, and errors in touched pixels compound.

The Inkplate library's mitigation is a hard counter **[SRC]** (`Inkplate5V2Driver.h:99`, `Inkplate5V2Driver.cpp:448-455, 530-533, 549-560`):

```c
uint16_t _partialUpdateLimiter = 10;    // default
...
if (_partialUpdateCounter >= _partialUpdateLimiter && _partialUpdateLimiter != 0) {
    display1b(leaveOn);                 // force a FULL update
    _partialUpdateCounter = 0;
}
```

**After 10 partial updates, the eleventh silently becomes a full refresh** — the ~0.8 s flashing one. Tunable:

```c
display.setFullUpdateThreshold(n);   // n = 0 disables the forced full refresh entirely
display.partialUpdate(true);         // _forced: bypass the limiter for this call once
```

> ⚠ **`setFullUpdateThreshold(0)` disables ghosting mitigation.** Tempting for a typewriter, a clock, or anything latency-sensitive. The cost is cumulative image degradation with no automatic recovery; you must then call `display()` yourself on some schedule. Also note `_blockPartial` — after certain operations the library forces the *next* update to be full regardless **[SRC]**.

There is a second, independent reason for periodic full refreshes: the Inkplate's greyscale waveform is an **absolute-target** table (§7.2), which is only valid from a known panel state. Partial updates leave the panel in an *unknown* state, so a greyscale update always runs the full clean sequence first — that is not optional and cannot be skipped.

### 8.4 ⚠ Temperature: the Inkplate does not compensate

E Ink's model is a **temperature-indexed set of LUTs** — *"The waveform flash file contains multiple temperature look-up-tables (LUTs)"*, and the controller selects one at update time **[DOC-EINK]** §2.1.

The Inkplate has:

- ✅ a temperature sensor — the [TPS65186](../../texas-instruments/tps65186/README.md)'s ADC on a **board-mounted** NTC (`R2`), readable as `display.readTemperature()`;
- ✅ the panel's own thermistor brought to the connector — **but unrouted** (§5.3);
- ❌ **no temperature dimension in `WAVEFORM3BIT` at all.** One table. All temperatures. **[SRC]**

`readTemperature()` is exposed to the application and used by Soldered's examples to *display* a temperature. **Nothing in the display path reads it.** **[SRC]** — searched the Inkplate 5 / 5V2 driver sources; the waveform tables are compile-time constants with no temperature index.

**Practical consequences [INF]:**

- Refreshes in the cold will be slower to settle and more prone to ghosting; in the heat, more prone to over-drive and flashing artefacts. This matches the general behaviour of e-paper devices without waveform compensation.
- The board's own floor is −10 °C anyway, set by the PMIC ([TPS65186 §2.1](../../texas-instruments/tps65186/README.md)).
- **If you deploy outdoors and see seasonal image-quality changes, this is why.** There is no library setting that fixes it; it would require per-temperature waveform tables that do not exist publicly.

### 8.5 Burn-in and panel lifetime

**No E Ink lifetime, update-count or image-retention figure exists publicly for this panel.** What we have is Soldered's mitigation API **[SRC]** (`Inkplate5V2Driver.cpp:1015-1032`; `Inkplate5Driver.cpp:1074-1091`):

```c
void EPDDriver::burnInClean(uint8_t clear_cycles, uint16_t cycles_delay);
// each cycle: clean(1,21) clean(2,1) clean(0,12) clean(2,1)
//             clean(1,21) clean(2,1) clean(0,12) clean(2,1)
//             then delay(cycles_delay)
```

That is a far more aggressive black/white cycling than a normal refresh — 68 passes per cycle versus 48 — with a caller-specified inter-cycle delay. The `clean()` documentation carries an explicit constraint **[SRC]**:

> *"@note Should not be used in intervals smaller than 5 seconds"*

and `burnInClean()` repeats it for `cycles_delay`. **Why 5 seconds is not explained**, but the obvious reading is thermal and charge-recovery: back-to-back full-panel drive without settling stresses the film. **[SRC]** + **[INF]**

**Practical guidance [INF]:** if a device shows a fixed element for long periods — a clock face, a status bar, a typewriter's header — invert or move it periodically, and run `burnInClean(2, 5000)` occasionally. That is standard e-paper practice; there is no vendor figure to calibrate it against.

---

## 9. Driver and library guidance

### 9.1 Arduino

**Inkplate Arduino library `InkplateLibrary` v11.1.4** **[SRC]**. Board: `Soldered Inkplate5` (`ED052TC2`) or **`Soldered Inkplate5v2`** (`ED052TC4`).

> ⚠ **The board selection determines the resolution *and* the waveform table at compile time.** Selecting `Inkplate5` on a Gen 2 board gives you a 960 × 540 framebuffer, the wrong clean sequence and the wrong waveform. The library will build and run. The display will be wrong.

```c
#include <Inkplate.h>
Inkplate display(INKPLATE_3BIT);        // or INKPLATE_1BIT

void setup() {
    display.begin();                    // expander + PMIC + framebuffers + GLUT
    display.setFullUpdateThreshold(10); // default; 0 disables forced full refresh
    display.clearDisplay();             // clears the BUFFER only
    display.display();                  // ~0.9 s, full flashing refresh
}
```

| Call | Notes |
|---|---|
| `Inkplate display(INKPLATE_1BIT / INKPLATE_3BIT)` | 1-bit: 1 buffer bit/px. 3-bit: 4 bits/px in PSRAM, 8 levels |
| `display.display(bool leaveOn = false)` | Full refresh. `leaveOn = true` keeps the PMIC rails up |
| `display.partialUpdate(bool forced = false, bool leaveOn = false)` | ~0.1 s. **1-bit mode only** |
| `display.setFullUpdateThreshold(n)` | §8.3 |
| `display.clean(uint8_t c, uint8_t rep)` | Raw drive-code access. **≥ 5 s between calls** |
| `display.burnInClean(cycles, delay_ms)` | §8.5 |
| `display.readTemperature()` | Board NTC via the PMIC — **not** used for waveform selection (§8.4) |
| `display.setVCOM(double)` | **[TPS65186 §9.4](../../texas-instruments/tps65186/README.md) — 100 writes, ever** |
| `display.selectDisplayMode(uint8_t)` | Switch 1-bit ↔ 3-bit at runtime |

**PSRAM is mandatory for the `ED052TC4`.** Four framebuffers at 1280 × 720 — `DMemoryNew` 115 kB, `_partial` 115 kB, `_pBuffer` 230 kB, `DMemory4Bit` 461 kB = **921,600 bytes (900 KiB)**, all `ps_malloc` **[SRC]** (`Inkplate5V2Driver.cpp:860-886`). It does not fit in ESP32 internal RAM. `initializeFramebuffers()` returns 0 and `begin()` fails if PSRAM is absent or not enabled in the board settings.

### 9.2 MicroPython

`SolderedElectronics/Inkplate-micropython`, board module `boards/inkplate5/inkplate5.py`. Supports **both** variants through a `variant` argument, with per-variant clean repetitions and X-mirroring **[SRC]**:

```python
cls._clean_reps               = _CLEAN_REPS[variant]
cls._clean_trailing_discharge = _CLEAN_TRAILING_DISCHARGE[variant]
inkplate.gfx_set_mirror_x(_MIRROR_X[variant])
```

The pixel-pushing loop is **native C** (`epd_control.c`), called from Python, with a callback into Python only to toggle the expander-hosted `SPV` — MicroPython cannot meet the timing otherwise **[SRC]**.

### 9.3 ESP-IDF

**There is no `esp_lcd` driver, and there cannot be a straightforward one.** `esp_lcd` targets panels with controllers; this panel has none. The ESP32 (original, not S3) also has no LCD_CAM peripheral — the I2S-in-LCD-mode approach of §6.1 is the only route, and ESP-IDF's modern `i2s_std`/`i2s_tdm` drivers do not expose LCD mode. You would be programming `I2S1` registers directly, exactly as `system/UtilI2S/UtilI2S.cpp` does.

**If you are starting an IDF project for this panel, port `UtilI2S.cpp` rather than looking for a component.** **[SRC]** + **[INF]**

*(On an **ESP32-S3** you would instead use the `esp_lcd_panel_io_i80` interface with the LCD_CAM peripheral, which is a much better fit — but that is a different board.)*

---

## 10. Pitfalls, ranked

1. **Selecting the wrong Arduino board for the panel you have.** Wrong resolution, wrong waveform, wrong clean sequence, no error. §9.1.
2. **Building without PSRAM enabled.** `begin()` fails silently on the `ED052TC4`. §9.1.
3. **Expecting SPI e-paper semantics.** There is no controller, no frame buffer in the panel, no `display()` command on the wire. §4.
4. **Calling `partialUpdate()` in 3-bit mode.** Partial update is a 1-bit path only.
5. **Disabling the full-update threshold and then being surprised by ghosting.** §8.3.
6. **`clean()` or `burnInClean()` in a tight loop.** ≥ 5 s between cleans. §8.5.
7. **Assuming `readTemperature()` affects the image.** It does not. §8.4.
8. **Assuming the panel's thermistor or its EEPROM is readable.** Both are on unpopulated pads. §5.3.
9. **Swapping panels between an Inkplate 5 and a Gen 2.** Different connectors, different pin counts. §5.2.
10. **Swapping a panel and keeping the board's VCOM.** VCOM is per-panel-lot and cannot be read from the panel. §5.3.
11. **Tuning the magic timing constants in `vscan_start()`.** No datasheet, no spare panels. §6.3.
12. **Clocking data with the bias rails down.** The driver guards against it (`if (!einkOn()) return;`) — do not bypass that guard. See [TPS65186 §5.3](../../texas-instruments/tps65186/README.md).
13. **Quoting an update time from this record as measured.** §6.4 is arithmetic.
14. **Trusting an "ED052TC4 datasheet" found online.** §1. Check for an E Ink header and a document number before believing anything in it.

---

## 11. Alternatives and equivalents

| Panel | Relationship | Drop-in? |
|---|---|---|
| **`ED052TC2`** ↔ **`ED052TC4`** | The two Inkplate 5 generations | ❌ **Not interchangeable.** Different connector (40 vs 50 way), different resolution, different waveform, different clean sequence |
| `ED060SC4` and the 6" DES family | Same interface architecture; the classic hacker-accessible E Ink panel (early Kindle) | ❌ Different size, resolution, connector. **But the closest thing to a public reference** for how this class of panel is driven |
| `ED097OC4` (9.7") | Same architecture, larger | ❌ Different everything except the concept |
| **Any SPI e-paper module** (SSD1680, UC8151, IL0373, and the Waveshare/Good Display range) | A different product category | ❌ **Has an integrated controller.** Simpler, slower, smaller, and needs no external PMIC |
| **Inkplate 6FLICK / Inkplate 10** | Other Soldered boards with parallel panels + TPS65186 | ❌ Different panels — but **the library structure and driver code are near-identical**, which makes them useful cross-references |

**Practical position:** if you have an Inkplate-class board, you have the panel it shipped with. There is no aftermarket. Design a new product around a panel you can actually buy. **[INF]**

---

## 12. Open questions

| Question | Status | How to close it |
|---|---|---|
| **Measured** full-refresh, greyscale and partial-update times | **Open.** §6.4 is calculated | `micros()` around `display()` / `partialUpdate()` on real hardware. **The single most useful contribution to this record** |
| Does `lcd_tx_wrx2_en = 1` halve the effective byte rate? | **Open** | ESP32 TRM §I2S, LCD mode. Would resolve §6.4's 2× uncertainty |
| What is `XON` for? | **Open.** Pulled up, broken out, undriven | No public source. Would need the panel spec |
| Which E Ink film generation (Pearl / Carta / Carta 1.2)? | **Open** | §2.2 |
| Pixel pitch, contrast ratio, reflectance, viewing angle | **Unknown — NDA** | §1 |
| Operating and storage temperature range of the *panel* | **Unknown — NDA.** The *board* floor is −10 °C | §1 |
| Panel lifetime / update-count endurance | **Unknown — NDA** | §8.5 |
| Does `ED052TC4` appear in Table 4 (AMEPD part numbers) of `800-1101`? | **Open.** The mirrored PDF is a 5-page excerpt and Table 4 is not in the extracted text | A complete copy of `800-1101` |
| Why must `clean()` calls be ≥ 5 s apart? | **Open.** Asserted by Soldered, unexplained | §8.5 |
| Would adding temperature-indexed waveform tables measurably improve cold-weather quality? | **Open** | Requires per-temperature LUTs that do not exist publicly. §8.4 |
| Is the panel FPC pin-1 orientation as implied by §5? | **Open** | Physical inspection or a panel photo |

---

## Manufacturer

**E Ink Holdings Inc. / E Ink Corporation** — see the [E Ink documentation-sourcing guide](../../../vendors/e-ink/README.md) for what E Ink does and does not publish, the NDA structure, and where panel information actually comes from.

## Used By

| Device | Designator | Panel |
|---|---|---|
| [Soldered Inkplate 5](../../../devices/soldered-electronics/inkplate-5/README.md) | **`U11`**, connector `K20` | **`ED052TC2`** — 960 × 540 |
| [Soldered Inkplate 5 Gen 2](../../../devices/soldered-electronics/inkplate-5-gen2/README.md) | **`U9`**, connector `K21` | **`ED052TC4`** — 1280 × 720 |
| [ZeroWriter Ink](../../../devices/zerowriter/zerowriter-ink/README.md) | **`U9`**, connector `K21` | **`ED052TC4`** — designator, connector and net list all unchanged from the stock Gen 2 |

## Related components

- [Texas Instruments TPS65186](../../texas-instruments/tps65186/README.md) — generates every rail on this connector, plus VCOM. **Read it before doing anything with this panel**
- [NXP PCAL6416A](../../nxp/pcal6416a/README.md) — carries `OE`, `GMOD` and `SPV`
- [ZeroWriter 1 e-paper driver notes](../../../devices/zerowriter/zerowriter-ink/zerowriter1-epaper-driver-notes.md) — a worked example of waveform-LUT tampering on the predecessor device (§7.3)

---

## 13. Local artifacts and sources

### Artifacts held

| Document | Origin | Local path | Bytes | SHA-256 |
|---|---|---|---:|---|
| **E Ink Corporation `800-1101 REV01` — "AF 16 Tone Grayscale 5-Bit Waveform Flash File Product Specification"** | **E Ink Corporation.** Mirrored by Waveshare on an unrelated product page | `artifacts/eink-af-16-tone-grayscale-5bit-waveform-flash-file-spec-800-1101-rev01.pdf` | 362,418 | `9396d7af46bdd0adcbb9dcca8591105787734b1b2692497dd672942a22863649` |

Validated 2026-08-24: `%PDF-1.5` magic; 5 pages; `pdfinfo` title `800-1101 REV01 AF 16 TONE GRAYSCALE 5-BIT WAVEFORM FLASH FILE PRODUCT SPECIFICATION.pdf`; produced 2017-01-11.

> **What this document is and is not.** It **is** a genuine, E Ink-authored specification — the source for §8.1 and §8.2, and for the NDA statement in §1. It **is not** a datasheet for the `ED052TC4`; it never names that part. It describes the AF waveform file format for E Ink Carta panels driven by an approved Generation-II controller. It appears to be a **5-page excerpt** — the "Verified AMEPDs" table (Table 4) referenced in §1 of the document is not present in the extracted text.
>
> **Provenance is third-party.** It was obtained from `waveshare.com`, not from E Ink. Given the NDA notice on its own first page, its public availability is presumably unintentional. It is retained here because it is the only primary E Ink source we could obtain and because its own front matter is the best evidence for §1's central claim.

**Archival: ✅ already preserved, and verified byte-identical.** The Wayback Machine holds a snapshot
taken **2026-06-30 17:52:41 UTC**:

```
http://web.archive.org/web/20260630175241/https://www.waveshare.com/w/upload/c/c4/E-paper-mode-declaration.pdf
```

Fetched 2026-08-24: HTTP 200, `application/pdf`, **362,418 bytes**, SHA-256
`9396d7af46bdd0adcbb9dcca8591105787734b1b2692497dd672942a22863649` — **identical to the local copy**.
The archived copy is therefore a trustworthy substitute if Waveshare ever removes the file.
(A fresh `web.archive.org/save/` submission timed out on the first attempt and returned HTTP 503 on
the second; unnecessary, given the existing snapshot.)

#### Reacquire

```bash
curl -L -o e-paper-mode-declaration.pdf \
  https://www.waveshare.com/w/upload/c/c4/E-paper-mode-declaration.pdf
```

**No manufacturer datasheet for the `ED052TC4` or `ED052TC2` was obtained.** Failures recorded in [`../../../component-download-failures.txt`](../../../component-download-failures.txt).

### Design files read

| File | What it established |
|---|---|
| `devices/soldered-electronics/inkplate-5/artifacts/hardware/.../CAD/V1.2.0/Soldered Inkplate 5.kicad_pcb` | Complete `K20` 40-way pinout (§5.2); data-line → ESP32 GPIO mapping; `XON` pull-up; unrouted `THERM`/SPI/`VDD2` |
| `.../CAD/V1.2.0/E-paper.kicad_sch` | `U11` = **`ED052TC2`**; `K20` = `AXE540127`; `U8` = `SN74LVC1G34DBV`; `R48` = 10 k |
| `devices/soldered-electronics/inkplate-5-gen2/artifacts/hardware/.../CAD/V1.1.0/Soldered Inkplate 5 Gen2.kicad_pcb` | Complete `K21` 50-way pinout (§5.1); unrouted `VDD_1V8`/`THERM`/SPI |
| `.../CAD/V1.1.0/E-paper.kicad_sch` | `U9` = **`ED052TC4`**; `K21` = `WP27D-S050VA3-R15000` |
| `devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter_ink/design/src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/Zerowriter Inkplate 5 Gen2.kicad_pcb` | `K21` identical to the stock Gen 2 |

All read with `devices/soldered-electronics/inkplate-5/tools/kicad_pcb_nets.py`.

### Source files read

Under `devices/soldered-electronics/inkplate-5/artifacts/source-snapshots/`:

| File | Lines cited |
|---|---|
| `Inkplate-Arduino-library/library.properties` | version **11.1.4** |
| `Inkplate-Arduino-library/src/boards/Inkplate5V2/waveforms.h` | 5–14 (`WAVEFORM3BIT`, `E_INK_WIDTH/HEIGHT`) |
| `Inkplate-Arduino-library/src/boards/Inkplate5/waveforms.h` | 5–14 |
| `Inkplate-Arduino-library/src/boards/Inkplate5V2/Inkplate5V2Driver.cpp` | 152–165 `calculateLUTs()`, 170–193 `vscan_start()`, 198–203 `vscan_end()`, 265–318 `display3b()`, 328–430 `display1b()`, 439–536 `partialUpdate()`, 549–556 `setFullUpdateThreshold()`, 624–650 `pinsAsOutputs()`, 730–770 `clean()`, 777–785 `hscan_start()`, 860–886 `initializeFramebuffers()`, 1015–1032 `burnInClean()` |
| `Inkplate-Arduino-library/src/boards/Inkplate5/Inkplate5Driver.cpp` | 261–269 / 349–357 (14-rep clean sequence), 1074–1091 `burnInClean()` |
| `Inkplate-Arduino-library/src/boards/Inkplate5V2/Inkplate5V2Driver.h` | 99 (`_partialUpdateLimiter = 10`) |
| `Inkplate-Arduino-library/src/boards/Inkplate5/pins.h` | 66–101 (`CL`/`CKV`/`SPH`/`LE` direct GPIO macros) |
| `Inkplate-Arduino-library/src/graphics/GraphicsDefs.h` | 3–14 (`LUT2`, `LUTW`, `LUTB`, `discharge`) |
| `Inkplate-Arduino-library/src/system/UtilI2S/UtilI2S.cpp` | 30–95 (I2S LCD-mode configuration) |
| `Inkplate-Arduino-library/src/system/UtilI2S/UtilI2S.h` | 37 (default clock divider 5) |
| `Inkplate-micropython/boards/inkplate5/inkplate5.py` | 80–150 (variant handling, C callback) |

### Authoritative sources

| ID | Title | Class | URL | Retrieved | Version | Establishes | Local artifact |
|---|---|---|---|---|---|---|---|
| S1 | **E Ink `800-1101 Rev01` — AF waveform flash file product specification** | **primary (E Ink), redistributed** | https://www.waveshare.com/w/upload/c/c4/E-paper-mode-declaration.pdf | 2026-08-24 | **Rev01**, dated 2017-01-11 | §1 NDA statement; §8.1 mode taxonomy and update times; §8.2 waveform-file header; §7.1 per-lot tuning and temperature LUTs | `artifacts/eink-af-…-rev01.pdf` |
| S2 | Negative probe — E Ink product pages | probe | https://www.eink.com/product/ED052TC4 · https://www.eink.com/products | 2026-08-24 | live | `/product/<part>` serves the generic category page; a regex scan of the products page for `ED\d{3}` returns **zero** part numbers. **E Ink publishes no public part catalogue** | – |
| S3 | Negative probe — Panelook | probe | https://www.panelook.com/ (model search, `ED052TC`) | 2026-08-24 | — | **Slider-CAPTCHA bot block** on every request, with and without a browser UA | – |
| S4 | Inkplate Arduino library | primary | https://github.com/SolderedElectronics/Inkplate-Arduino-library | 2026-08-24 | **v11.1.4** | All **[SRC]** — resolutions, waveform tables, drive codes, timing constants, clean sequences, ghosting limiter, burn-in API | snapshot, §13 |
| S5 | Inkplate MicroPython library | primary | https://github.com/SolderedElectronics/Inkplate-micropython | 2026-08-24 | snapshot | §9.2 variant handling | snapshot, §13 |
| S6 | Soldered Inkplate 5 hardware design (TAPR OHL) | primary | https://github.com/SolderedElectronics/Soldered-Inkplate-5-hardware-design | 2026-08-24 | **V1.2.0** | §5.2 `ED052TC2` connector pinout | local |
| S7 | Soldered Inkplate 5 Gen2 hardware design | primary | https://github.com/SolderedElectronics/Soldered-Inkplate-5-Gen2-hardware-design | 2026-08-24 | **V1.1.0** | §5.1 `ED052TC4` connector pinout | local |
| S8 | ZeroWriter Ink design files | primary | https://github.com/zerowriter/zerowriter_ink | 2026-08-24 | **v1.2.0** | `K21` unchanged in the respin | local |
| S9 | Inkplate documentation | secondary | https://docs.soldered.com/inkplate/ | 2026-08-24 | live | `einkOn()` rail list; API descriptions | `devices/soldered-electronics/inkplate-5/artifacts/docs/Inkplate-documentation/` |
| S10 | ZeroWriter 1 driver-modification analysis | derived, in-repo | [`zerowriter1-epaper-driver-notes.md`](../../../devices/zerowriter/zerowriter-ink/zerowriter1-epaper-driver-notes.md) | 2026-08-24 | — | §7.3 — **different panel and controller**; lineage evidence only | local |

> **Evidence boundary for this record.** Every dimension, timing figure and material property that would normally come from a panel datasheet is **absent**, and this record does not invent any. What it establishes instead is: the complete electrical interface (from three independent board designs), the complete drive protocol (from vendor driver source), and the general E Ink waveform model (from one genuine E Ink document about a different, related product). Claims that go beyond those three sources are marked **[INF]**.
