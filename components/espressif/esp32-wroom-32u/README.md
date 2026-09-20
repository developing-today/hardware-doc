# Espressif ESP32-WROOM-32U-N4

- **Category:** Wi-Fi + Bluetooth + Bluetooth LE **module** — ESP32 die, SPI flash, 40 MHz crystal, RF front end, in a shielded, pre-certified can
- **Variant meaning:** the **`U` suffix = u.FL/IPEX external-antenna connector, no PCB antenna**. `N4` = 4 MB flash.
- **⚠ No PSRAM.** This is the WROOM line. See §2 — it is the most common confusion about this part
- **Package:** 38-pin SMD castellated module, **18.0 × 19.2 × 3.2 mm** — *shorter* than a PCB-antenna module
- **Fitted on:** `U1` of the **ZeroWriter Keyboard PCB**, JLCPCB/LCSC part **`C328062`**
- **Lifecycle:** ⚠ **NRND** — Not Recommended For New Designs. Superseded by ESP32-WROOM-32UE. §1.3
- **Research date:** 2026-08-24; datasheets retrieved 2026-08-24

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Stated by Espressif in a document retrieved into `artifacts/` |
| **[SCH]** | Read out of the ZeroWriter KiCad schematic sources, via net extraction |
| **[COM]** | Distributor data — LCSC/JLCPCB catalogue record |
| **[WEB]** | Non-manufacturer web source, dated at retrieval |
| **[INF]** | Inference. Not established by the above |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | Espressif Systems (Shanghai) Co., Ltd. | **[DOC]** |
| Full ordering code | **`ESP32-WROOM-32U-N4`** | **[SCH]** BOM value; **[COM]** LCSC `productModel` |
| Distributor part | **LCSC / JLCPCB `C328062`**, brand `ESPRESSIF`, encap `SMD, 19.2 × 18 mm` | **[COM]** |
| SoC inside | **`ESP32-D0WD`** (dual-core, no in-package flash or PSRAM) | **[DOC]** DS v2.7 §1.2; **[COM]** LCSC description |
| Core | Xtensa **LX6** dual-core 32-bit, 80–240 MHz | **[DOC]** DS v2.7 §1.1 |
| On-chip memory | 448 KB ROM, 520 KB SRAM, 8 KB RTC SRAM | **[DOC]** |
| Integrated crystal | 40 MHz | **[DOC]** |
| Integrated flash | **4 MB** Quad SPI | **[DOC]** DS v2.7 Table 2 |
| **Integrated PSRAM** | **None.** §2 | **[DOC]** — absent from the "Integrated Components on Module" list |
| Usable GPIOs | **Up to 32** as counted by DS v2.7 (26 by the -32E datasheet's newer counting) | **[DOC]** |
| Antenna | **u.FL / IPEX external-antenna connector.** No PCB antenna, **no keepout zone** | **[DOC]** DS v2.7 §2.1 note |
| Supply | 3.0–3.6 V (3.3 V typ.); external supply must deliver **≥ 0.5 A** | **[DOC]** DS v2.7 Table 14 |
| Ambient | −40 … +85 °C | **[DOC]** |
| Dimensions | **18 × 19.2 × 3.2 mm** (vs 18 × 25.5 × 3.1 for the -32D) | **[DOC]** DS v2.7 Table 2 |
| FCC ID | **`2AC7Z-ESP32WROOM32U`**, granted 2018-01-22, Single Modular Approval | **[DOC]** `artifacts/esp32-wroom-32u-fcc-wifi-bt40-certificate.pdf` |
| CE / RED | Kiwa Nederland B.V. EU type-examination certificate (Module B) **172141367/AA/02**, NB 0063, issued 2023-03-02, type designation `ESP32-WROOM-32U`, HW **V2.1** | **[DOC]** `artifacts/esp32-wroom-32u-ce-certification.pdf` |
| **Lifecycle** | **NRND.** The datasheet cover carries "NOT RECOMMENDED FOR NEW DESIGNS" and every page is watermarked | **[DOC]** DS v2.7 |

### 1.1 The WROOM-32 lineage, decoded

The suffix letters on this line are three orthogonal things wearing one name. Untangling them:

```
ESP32-WROOM-32 U E -N4
                │ │  └── N<n>  flash in MB   (introduced with the E generation)
                │ └───── generation: (none) -> D -> E
                └─────── antenna: (none/D/E) = PCB trace,  U/UE = u.FL connector
```

| Module | Die | Flash | PSRAM | Antenna | Body (mm) | Lifecycle | Datasheet held |
|---|---|---|---|---|---|---|---|
| **ESP32-WROOM-32** | `ESP32-D0WDQ6` | 4 / 8 / 16 MB | — | PCB | 18.0 × 25.5 × 3.1 | **NRND** | v3.7 |
| **ESP32-WROOM-32D** | `ESP32-D0WD` | 4 MB | — | PCB | 18.0 × 25.5 × 3.1 | **NRND** | v2.7 |
| **ESP32-WROOM-32U** | `ESP32-D0WD` | 4 MB | — | **u.FL** | **18.0 × 19.2 × 3.2** | **NRND** | v2.7 |
| **ESP32-WROOM-32E** | `ESP32-D0WD-V3` / `D0WDR2-V3` | 4 / 8 / 16 MB (`H4`/`H8` = 105 °C) | — *(or **2 MB** on `R2` SKUs)* | PCB | 18.0 × 25.5 × 3.1 | **Active** | v2.1 |
| **ESP32-WROOM-32UE** | `ESP32-D0WD-V3` / `D0WDR2-V3` | 4 / 8 / 16 MB (`H4`/`H8`) | — *(or **2 MB** on `R2`)* | **u.FL** | **18.0 × 19.2 × 3.2** | **Active** | v2.1 |

The general Espressif suffix decode for the *die* part numbers (`D0WD`, `R2`, `-V3`, `Q6`) is in
[guides/espressif/ecosystem-and-product-lines.md §7.1](../../../guides/espressif/ecosystem-and-product-lines.md#71-classic-esp32--the-authoritative-decode).

### 1.2 -32D vs -32E vs -32U — what actually differs

| | **-32D** | **-32E** | **-32U** |
|---|---|---|---|
| Silicon revision | `ESP32-D0WD`, **rev 1** | `ESP32-D0WD-V3`, **rev 3** | `ESP32-D0WD`, **rev 1** |
| Flash options | 4 MB only | 4 / 8 / 16 MB | 4 MB only |
| PSRAM option | none | **2 MB** via `D0WDR2-V3` on `R2` SKUs | none |
| High-temp SKU | no | **`H4`/`H8` = −40…+105 °C** | no |
| Antenna | PCB | PCB | **u.FL** |
| Body length | 25.5 mm | 25.5 mm | **19.2 mm** |
| Keepout zone required | **yes** | **yes** | **no** **[DOC]** |
| RTC SRAM | 8 KB | **16 KB** | 8 KB |
| Bluetooth SIG qualification | separate | Declaration ID **D051055** (2020) | separate |
| Lifecycle | NRND | **Active** | **NRND** |

**The single most consequential row is "silicon revision."** -32D and -32U carry **rev 1** silicon; -32E and -32UE carry **rev 3**. Rev 3 fixes the whole external-SRAM/PSRAM erratum family, the brown-out reset failure, both spurious-watchdog issues and the audio-PLL limitation — see
[guides/espressif/errata-practical.md §2](../../../guides/espressif/errata-practical.md#2-esp32--the-errata-that-actually-bite) and the full revision matrix in
[esp32-u4wdh §21](../esp32-u4wdh/README.md#21-silicon-revisions-the-complete-matrix-and-what-v31-means). **Do not re-derive that here.**

**[INF] Practical translation:** if you are choosing this part today, choose **ESP32-WROOM-32UE-N4**, not -32U. It is the same footprint, the same pinout, the same connector, and it is rev-3 silicon on an active part number. The only reason to fit a -32U is that you already have a reel of them.

> **⚠ A documentation error worth knowing about.** ESP32-WROOM-32D/32U Datasheet v2.7 §1.2 states *"At the core of the modules is ESP32-D0WD\*, an Xtensa® 32-bit **LX7** CPU"*. **The ESP32 is LX6.** LX7 is the ESP32-S2/S3 core. This is a copy-paste error in Espressif's own current document **[DOC]**; the same datasheet's §1.1 feature bullet correctly says LX6. Flagged because it will mislead anyone who greps for "LX7".

### 1.3 Lifecycle: this part is NRND

Both the -32D/-32U datasheet (v2.7) and the -32 datasheet (v3.7) carry **"NOT RECOMMENDED FOR NEW DESIGNS (NRND)"** on the cover and a `NotRecommendedForNewDesigns(NRND)` watermark on every page **[DOC]**.

NRND means: still buildable, still buyable, no new design-ins encouraged, no commitment to indefinite supply. LCSC still lists `C328062` as of 2026-08-24 **[COM]**, so it is currently obtainable, but any product with a multi-year life should be on the -32UE.

---

## 2. ⚠ WROOM has no PSRAM. WROVER does. This is the whole distinction.

This confusion is common enough to deserve its own section, and this repository documents a single product that contains **both** modules, which makes the contrast concrete.

### 2.1 The rule

| | **WROOM-32 / -32D / -32U** | **WROVER / -B / -E** |
|---|---|---|
| SPI flash | 4 MB (or 4/8/16 on -32E) | 4 / 8 / 16 MB |
| **PSRAM** | **none** | **8 MB** |
| Body length | 25.5 mm (19.2 mm for -U/-UE) | **31.4 mm** |
| GPIO16 / GPIO17 | **available** (pins 27, 28) | **absent** — consumed by PSRAM |
| Usable GPIOs | 32 (v2.7 counting) / 26 (v2.1 counting) | 24 (v2.4 counting) |

The WROVER is physically longer *because* there is a second memory die inside the can. That is the entire architectural difference; everything else follows from it.

### 2.2 The one real exception — and it is not what people think

**ESP32-WROOM-32E and -32UE `R2` SKUs *do* have PSRAM.** **[DOC]** DS v2.1 Tables 1–2:

> `ESP32-WROOM-32E-N4R2` — 4 MB flash, **2 MB PSRAM (Quad SPI)**
> `ESP32-WROOM-32UE-N4R2` — 4 MB flash, **2 MB PSRAM (Quad SPI)**

with the feature bullet *"ESP32-D0WDR2-V3 also provides 2 MB PSRAM"*. This PSRAM is **in the SoC package**, not a separate die on the module PCB — which is why the module stays 25.5/19.2 mm long.

So the accurate statements are:

- ✅ *"The ESP32-WROOM-32U-N4 on the ZeroWriter keyboard has no PSRAM."* — **[DOC]**, unambiguous.
- ✅ *"The classic WROOM-32/-32D/-32U line has no PSRAM."* — **[DOC]**.
- ❌ *"WROOM modules never have PSRAM."* — **false** since the -32E generation.
- ⚠ Even on an `R2` SKU you get **2 MB**, versus **8 MB** on a WROVER-E. The 4× difference matters for anything framebuffer-shaped.

### 2.3 The consequence you can see on this very product

ZeroWriter Ink carries two ESP32 modules. On the keyboard's WROOM-32U, GPIO16 and GPIO17 are **real, routed pins carrying key-matrix columns**:

```
NET Col 8: CH8.1, CH22.1, CH36.1, CH49.1, U1.27[IO16]
NET Col 9: CH9.1, CH23.1, CH37.1, CH50.1, U1.28[IO17]
```

**[SCH]** `devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter_ink/design/src/Zerowriter Keyboard/v1.2.0/CAD/Zerowriter Keyboard.kicad_sch`.

On the display board's [ESP32-WROVER](../esp32-wrover/README.md), module pins 27 and 28 are **NC and are not even drawn in the schematic symbol**. Two of the keyboard's fourteen matrix columns would be unroutable on the other module. See [ESP32-WROVER §2](../esp32-wrover/README.md#2--gpio16-and-gpio17-do-not-exist-on-a-wrover).

---

## 3. Pinout, with the ZeroWriter keyboard nets

38 signal pins plus the EPAD. The KiCad symbol used is the **official** `RF_Module:ESP32-WROOM-32U`, which carries all 39 pins including 27/28 **[SCH]**.

Espressif: *"The pin layout of ESP32-WROOM-32U is the same as that of ESP32-WROOM-32D, except that ESP32-WROOM-32U has no keepout zone."* **[DOC]** DS v2.7 §2.1.

| Pin | Name | GPIO | Type | ZeroWriter Keyboard net | Role |
|---:|---|---|---|---|---|
| 1 | `GND` | — | P | `Earth` | |
| 2 | `3V3` / `VDD` | — | P | `+3V3` | From `K1.1`/`K1.2`. Decoupling: `C1` 10 µF 0402 + `C2` 100 nF 0402 |
| 3 | `EN` | — | I | `NRST` | `R1` 10 kΩ pull-up, `C3` 100 nF, `RST1` button, `K2.5` |
| 4 | `SENSOR_VP` | 36 | **input-only** | — | unused |
| 5 | `SENSOR_VN` | 39 | **input-only** | — | unused |
| 6 | `IO34` | 34 | **input-only** | — | unused |
| 7 | `IO35` | 35 | **input-only** | — | unused |
| 8 | `IO32` | 32 | I/O | `Col 14` | matrix column |
| 9 | `IO33` | 33 | I/O | `Col 13` | matrix column |
| 10 | `IO25` | 25 | I/O | `Col 12` | matrix column |
| 11 | `IO26` | 26 | I/O | `Row 4` | matrix row (12 diodes) |
| 12 | `IO27` | 27 | I/O | `Row 3` | matrix row (13 diodes) |
| 13 | `IO14` | 14 | I/O | `Row 5` | matrix row (8 diodes) |
| 14 | `IO12` | 12 | I/O | `Row 2` | matrix row (14 diodes). **⚠ also MTDI** — §5.2 |
| 15 | `GND` | — | P | `Earth` | |
| 16 | `IO13` | 13 | I/O | `Row 1` | matrix row (14 diodes) |
| 17–22 | `SHD/SD2` … `SDI/SD1` | 9,10,11,6,7,8 | — | **unconnected** | internal flash bus. Left floating **[SCH]** |
| 23 | `IO15` | 15 | I/O | `Col 6` | matrix column. **⚠ also MTDO** |
| 24 | `IO2` | 2 | I/O | `Col 5` | matrix column. **⚠ boot strap** — §5.2 |
| 25 | `IO0` | 0 | I/O | `BOOT0` | boot strap; `RST2` button; `K2.6` |
| 26 | `IO4` | 4 | I/O | `Col 7` | matrix column |
| **27** | **`IO16`** | 16 | I/O | **`Col 8`** | **available — this is the WROVER contrast** |
| **28** | **`IO17`** | 17 | I/O | **`Col 9`** | **available** |
| 29 | `IO5` | 5 | I/O | `Col 10` | matrix column. **⚠ SDIO-timing strap** |
| 30 | `IO18` | 18 | I/O | `Col 11` | matrix column |
| 31 | `IO19` | 19 | I/O | `Col 1` | matrix column |
| 32 | `NC` | — | — | unconnected | |
| 33 | `IO21` | 21 | I/O | `Col 2` | matrix column |
| 34 | `RXD0` | 3 | I/O | `USART2_RX` | to `K1.3` (main board) and `K2.4` (programmer) |
| 35 | `TXD0` | 1 | I/O | `USART2_TX` | to `K1.4` and `K2.3` |
| 36 | `IO22` | 22 | I/O | `Col 4` | matrix column |
| 37 | `IO23` | 23 | I/O | `Col 3` | matrix column |
| 38 | `GND` | — | P | `Earth` | |
| 39 | `GND` (EPAD) | — | P | `Earth` | RF/thermal ground pad |

---

## 4. Electrical characteristics

**[DOC]** ESP32-WROOM-32D/32U Datasheet v2.7 §5. Current-consumption figures come from the -32E/-32UE Datasheet v2.1 Table 16 — the -32D/-32U v2.7 dropped its own table and defers to the ESP32 Series Datasheet, but the die and RF front end are the same, so these are the right order of magnitude **[INF]**.

| Symbol | Parameter | Value |
|---|---|---|
| `VDD33` | Supply, recommended | 3.0 / **3.3** / 3.6 V |
| `VDD33` | Absolute maximum | −0.3 … **3.6 V** |
| `IVDD` | **Supply must be able to deliver** | **≥ 0.5 A** |
| `Ioutput` | **Cumulative** I/O output current, absolute max | **1,100 mA** |
| `Tstore` | Storage temperature | −40 … +105 °C |
| `VIH` / `VIL` | Input thresholds | 0.75 × VDD / 0.25 × VDD |
| `VOH` / `VOL` | Output levels | ≥ 0.8 × VDD / ≤ 0.1 × VDD |
| `IOH` | Source current, `VDD3P3_CPU`/`VDD3P3_RTC` | 40 mA/pin, derating to ~29 mA as pin count rises |
| `IOL` | Sink current | 28 mA |
| `RPU` / `RPD` | Internal pulls | ~45 kΩ |
| `VIL_nRST` | `EN` low threshold to shut down | ≤ 0.6 V |

**Current, from the -32E/-32UE datasheet [DOC]:**

| Work mode | Average (mA) | **Peak (mA)** |
|---|---:|---:|
| TX 802.11b, 20 MHz, 1 Mbps @ 19.5 dBm | 239 | **379** |
| TX 802.11g, 20 MHz, 54 Mbps @ 15 dBm | 190 | 276 |
| TX 802.11n, 20 MHz, MCS7 @ 13 dBm | 183 | 258 |
| TX 802.11n, 40 MHz, MCS7 @ 13 dBm | 165 | 211 |
| RX 802.11b/g/n, 20 MHz | 112 | 112 |
| RX 802.11n, 40 MHz | 118 | 118 |

### 4.1 What the ZeroWriter keyboard actually provides

**[SCH]** The entire keyboard power system is: `K1` pins 1 and 2 bring `+3V3` across from the main board through a 6-pin `HC-1.25-6PWT` cable; `C1` (`GRM155R61A106ME11D`, **10 µF 0402 6.3 V**) and `C2` (**100 nF 0402**) sit at the module.

**[INF] Two observations, offered as engineering commentary rather than defect claims:**

1. **There is no bulk capacitor beyond 10 µF, and no local regulator.** Espressif's hardware design guidelines recommend a larger bulk part adjacent to pin 2. A 379 mA TX burst arriving down a 6-pin JST cable from another PCB will produce a measurable droop.
2. **A 0402 10 µF X5R part loses a large fraction of its rated capacitance under DC bias.** At 3.3 V on a 6.3 V-rated 0402, effective capacitance is commonly 30–50 % of nominal.

Neither matters in practice **on this product**, because the keyboard's radio is not used (§6.2). It would matter immediately if someone enabled Wi-Fi on it.

---

## 5. Exact role and wiring on the device

### 5.1 The role: a dual-core Wi-Fi/BLE SoC used as a keyboard scanner

**[SCH]** `Zerowriter Keyboard.kicad_sch`, v1.2.0.

| Item | Detail |
|---|---|
| Designator | `U1` |
| Matrix | **14 columns × 5 rows**, 61 keys populated of 70 positions |
| Columns | `IO19 IO21 IO23 IO22 IO2 IO15 IO4 IO16 IO17 IO5 IO18 IO25 IO33 IO32` (`Col 1`…`Col 14`) |
| Rows | `IO13 IO12 IO27 IO26 IO14` (`Row 1`…`Row 5`) |
| Diodes | 61 × `1N4148W` SOD-123, **cathode to the row net** — so rows are the scanned/driven side and the anodes go to the switches |
| Switches | Kailh **Choc v1** hot-swap sockets (`CPG135001S30`), LCSC `C5333465`; 4 × 2u + 1 × 6.25u stabilisers, all **DNP** |
| Inter-board link | `K1` `HC-1.25-6PWT`: pin 1,2 = `+3V3`; pin 3 = `USART2_RX`; pin 4 = `USART2_TX`; pin 5,6 + shield = `Earth`. **Power and UART only** |
| Programmer header | `K2`, 6-pin `NOVA_programmer_header`: `GND, VCC, TX, RX, RESET, GPIO0` — a standard ESP auto-download pinout |
| Buttons | `RST1` → `NRST`/`EN`; `RST2` → `BOOT0`/`IO0`. Both `TS5215A` 250 gf |
| **Antenna** | **none fitted** — §6.2 |

The net labels `USART2_RX` / `USART2_TX` are an **STM32-ism** (the ESP32 has `UART0/1/2`, not `USART2`) **[INF]** — almost certainly carried over from an earlier keyboard design or a template.

### 5.2 Three strapping pins are in the key matrix

This deserves flagging because it constrains firmware:

| Pin | Strap function | Used as | Risk |
|---|---|---|---|
| `IO2` | **Boot strap** (default pull-**down**, must be low or floating for normal boot) | `Col 5` | If a column drive holds `IO2` high across a reset, boot mode changes |
| `IO15` | **MTDO** — U0TXD-printing control and SDIO-slave timing (default pull-**up**) | `Col 6` | Holding it low at reset silences the ROM boot log |
| `IO12` | **MTDI** — selects `VDD_SDIO` = 3.3 V (low) or 1.8 V (high) | `Row 2` | **Holding it high at reset switches the flash rail to 1.8 V** |
| `IO5` | SDIO-slave timing strap (default pull-up) | `Col 10` | Benign here |

**[INF]** The design is safe *as drawn*: the matrix is passive at reset (columns high-Z, diodes reverse-biased toward the rows), so every strap sees only its internal pull. The hazard is **firmware-created** — a scan routine that leaves `Row 2` (`IO12`) driven high and then calls `esp_restart()` re-samples MTDI as 1, and a 3.3 V flash die ends up on the 1.8 V LDO. The chip then fails to boot.

**Design rule:** drive all rows and columns low, or set them to inputs, before any software reset. The general form of this trap, and the eFuse recovery, is in
[guides/espressif/memory-and-boot.md §5.1](../../../guides/espressif/memory-and-boot.md#51-esp32-vdd_sdio-mtdi-and-the-18-v-trap) and
[esp32-u4wdh §§18.3–18.4](../esp32-u4wdh/README.md). **Not duplicated here.**

### 5.3 Not fitted on the Inkplate boards — and why this record exists anyway

**Not fitted** on [Soldered Inkplate 5](../../../devices/soldered-electronics/inkplate-5/README.md) or [Soldered Inkplate 5 Gen 2](../../../devices/soldered-electronics/inkplate-5-gen2/README.md). Neither product has a keyboard, and both use an [ESP32-WROVER](../esp32-wrover/README.md) — which they must, because their framebuffers do not fit without PSRAM ([WROVER §6](../esp32-wrover/README.md#6-why-an-inkplate-must-be-a-wrover-the-framebuffer-arithmetic)).

This part appears in the knowledge base for three reasons:

1. **It is fitted on the ZeroWriter Keyboard PCB**, which is the second board of the ZeroWriter Ink product and is documented here.
2. **It is the counter-example that makes the WROVER's GPIO16/17 restriction legible** (§2.3). One product, two modules, one uses those pins and one cannot.
3. **It is the module you reach for when the enclosure is metal or the antenna must be remote** (§6), which is a question that comes up on every enclosed ESP32 design.

### 5.4 The design-history oddity: an ESP32-S3 keyboard also exists in the repo

The ZeroWriter source snapshot contains **two** keyboard designs:

| Path | MCU | Scanning |
|---|---|---|
| `design/src/Zerowriter Keyboard/v1.2.0/` | **ESP32-WROOM-32U-N4** (`U1`), LCSC `C328062` | direct 14 × 5 matrix on module GPIOs |
| `design/zw_keyboard/Kicad/` | **ESP32-S3FH4R2** (`U6`) + **5 × MCP23017** I/O expanders + `ABM8-40.000MHZ` crystal | matrix via expanders |

**[SCH]** both BOMs. The `src/…/v1.2.0/` tree is the one that matches the shipped ZeroWriter Ink documentation and carries the `Soldered footprints:` library, i.e. the production respin. **UNRESOLVED** which came first and whether the S3 design was ever built. Recording it because it is the kind of thing that produces contradictory "what MCU is in the keyboard?" answers.

---

## 6. The `-32U` decision: when an external antenna is the right answer

### 6.1 When to choose `-32U`/`-32UE` over `-32D`/`-32E`

| Reason | Explanation |
|---|---|
| **Metal or metallised enclosure** | The decisive one. A PCB trace antenna inside a metal box is inside a Faraday cage. Nothing you do in software recovers this — you must get the radiator outside the shield |
| **The module cannot sit at a board edge** | A PCB antenna needs a **keepout zone**: no copper, no ground plane, no components, on any layer, under and around the antenna. If your layout cannot give it that, the -U removes the requirement entirely — Espressif states the -32U *"has no keepout zone"* **[DOC]** |
| **Board is 19.2 mm shorter** | The -U body is 6.3 mm shorter than the -D/-E because the antenna section is gone. On a cramped board this is real |
| **Range** | An external ¼-wave whip or a tuned dipole beats a compact trace antenna. A 3–5 dBi external antenna versus roughly 2 dBi typical for the PCB trace is a genuine link-budget improvement |
| **Directionality** | A patch or Yagi lets you aim the link. Impossible with a PCB antenna |
| **Antenna diversity / remote placement** | The radio can be deep in a chassis with the antenna on a bulkhead |

**When *not* to:** an external antenna adds a connector, a pigtail, a bulkhead fitting, an assembly step, a mechanical failure point, a BOM line, and — see §6.3 — a regulatory question. If the product is plastic and the module can sit at a board edge, the PCB-antenna variant is strictly simpler.

### 6.2 What ZeroWriter actually did: fitted the connector, fitted no antenna

**[SCH]** The complete ZeroWriter Keyboard v1.2.0 BOM is 16 lines. **There is no antenna, no pigtail, no u.FL-to-SMA lead and no bulkhead connector anywhere in it** — searched across every BOM, every `.kicad_sch` and every pick-and-place file in the design tree. The only hit for "antenna" in the whole tree is the KiCad symbol's own description string.

So: the module ships with its u.FL receptacle (Espressif fits it), and nothing is attached to it.

**[INF]** This is consistent with the product: ZeroWriter Ink ships with wireless disabled and markets itself as a distraction-free writing device. An unloaded u.FL receptacle is electrically harmless — the module simply radiates almost nothing, which is arguably the point. It does mean the keyboard's radio is **non-functional by construction**, not merely disabled in software.

**[INF] If you want to enable it**, you need a u.FL (IPEX MHF-1) 2.4 GHz antenna. Note that the u.FL receptacle is rated for very few mating cycles (a handful; the connector family is intended for one-time factory assembly), so do not treat it as a plug-in port.

### 6.3 ⚠ Antenna selection, matching, and the certification consequence

**The electrical part.** The module presents a **50 Ω** port at the connector. Espressif's RF characterisation is explicit:

> *"The RF data is measured at the antenna port, where RF cable is connected, including the front-end loss. **The external antennas used for the tests on the modules with external antenna connectors have an impedance of 50 Ω.**"* **[DOC]** DS v2.7 §6

So: 50 Ω antenna, 50 Ω coax, keep the pigtail short, and check the antenna's return loss over 2400–2500 MHz. A mismatched antenna does not merely lose range — it reflects power back into the PA, which degrades EVM and can trip the module's own protection.

**The regulatory part — this is the trap.**

Espressif's FCC grant for this module is a **Single Modular Approval**, and the grant text is unambiguous **[DOC]** (`artifacts/esp32-wroom-32u-fcc-wifi-bt40-certificate.pdf`):

> *"Single Modular Approval. Output power listed is conducted. This grant is valid only when the module is sold to OEM integrators and must be installed by the OEM or OEM integrators. **The antenna(s) used for this transmitter must be installed to provide a separation distance of at least 20 cm from all persons and must not be collocated or operating in conjunction with any other antenna or transmitter**, except in accordance with FCC multi-transmitter product guidelines. End-users may not be provided with the module installation instructions. OEM integrators and end-users must be provided with transmitter operating conditions for satisfying RF exposure compliance."*

Modular approval is granted **for the module together with the antenna(s) it was tested with**. The practical consequences:

| If you… | Then… |
|---|---|
| Fit an antenna of the **same type and equal or lower gain** than one in Espressif's tested list | ✅ Generally still covered by the modular grant. Confirm against the grant's antenna list and your integrator documentation |
| Fit a **higher-gain** antenna | ❌ **EIRP rises above what was certified.** The grant no longer covers you. You need at least a Class II permissive change, and possibly retesting |
| Fit a **different antenna type** (patch instead of whip, directional instead of omni) | ❌ Same problem — radiation pattern and gain both changed |
| Give the **end user** a removable, user-replaceable antenna | ❌ FCC generally requires a **unique/non-standard connector** precisely to stop this. A reverse-polarity SMA is the conventional answer; a plain SMA jack that accepts any commodity antenna is a compliance problem |
| Place the antenna **within 20 cm of a person** in normal use | ❌ Violates the grant's RF-exposure condition. Requires SAR evaluation |
| **Collocate** with another transmitter (BLE + Wi-Fi in one product with two radios) | ⚠ Requires the FCC multi-transmitter analysis |
| Ship into the EU | ⚠ The Kiwa Module B certificate is *"limited to products, which are equal to the one(s) assessed"* **[DOC]**, and *"If the equipment is to be modified, Kiwa shall be notified immediately"*. Changing the antenna is a modification |

> **⚠ The one-sentence version: swapping the antenna can invalidate the module's modular certification, and with it the main commercial reason for using a module at all.** The certification value described in [ESP32-WROVER §8](../esp32-wrover/README.md#8-module-versus-bare-chip-the-certification-argument) is conditional on you respecting the antenna constraints in the grant.
>
> **[INF]** None of this is legal advice, and none of it was verified against a specific FCC KDB procedure in this pass. The grant text quoted above is **[DOC]**; the interpretation table is **[INF]** from standard modular-approval practice. If you are shipping a product, get a test house to read the grant with you.

---

## 7. Firmware, drivers and tooling

Nothing here is specific to the `-32U` variant — it is an ESP32-D0WD with 4 MB of flash and no PSRAM — but the version floors are worth stating.

| Framework | Target | Notes |
|---|---|---|
| **ESP-IDF** | `idf.py set-target esp32` | Any 4.x/5.x. **Do not** enable `CONFIG_SPIRAM` — there is no PSRAM and the boot will fail the memory test |
| **Arduino-ESP32** | Board "ESP32 Dev Module", **PSRAM: Disabled**, Flash Size 4 MB, Partition Scheme "Default 4 MB with spiffs" | ZeroWriter's firmware is Arduino-based |
| **esptool** | `esptool --chip esp32 …` | v4.5+ recommended for correct rev reporting. See [esp32-u4wdh §21.7](../esp32-u4wdh/README.md#217-tooling-versions--what-recognises-v31-and-what-mis-reports-it) for which versions mis-report revisions |
| **Keyboard-specific** | — | A 14 × 5 matrix on bare GPIOs needs no library. **[INF]** QMK does not support the ESP32; if you want a maintained firmware, ESP-IDF or Arduino with a hand-rolled scanner is the realistic path |

### 7.1 Programming this board

There is **no USB on the keyboard PCB** — no bridge, no connector. Two routes **[SCH]**:

1. **`K2`, the 6-pin `NOVA` header** — `GND / VCC / TX / RX / RESET / GPIO0`. This is the standard external-programmer pinout; any CH340/CP2102 dongle that breaks out DTR/RTS will drive it, or an "ESP programmer" board directly.
2. **`K1`, the inter-board link** — `+3V3`, `USART2_TX`, `USART2_RX` reach the main board. UART only; **`RESET` and `GPIO0` are not on `K1`**, so this route requires holding `RST2` (BOOT0) and pressing `RST1` by hand to enter download mode.

The main board's [CH340C](../../wch/ch340c/README.md) serves the **display** ESP32 only. It cannot flash the keyboard.

### 7.2 Enabling the radio, if you want to

The `-32U` is a full Wi-Fi + Bluetooth 4.2 BR/EDR + BLE part, identical in capability to any other ESP32. Classic Bluetooth availability by chip family is covered in
[guides/espressif/ecosystem-and-product-lines.md §3](../../../guides/espressif/ecosystem-and-product-lines.md#3-radio-capability--the-decision-that-cannot-be-undone-in-software) — the ESP32 is one of the few Espressif parts that has it, which is precisely why a BT-HID keyboard on this module would be possible where an ESP32-C3 or -S3 could only do BLE HID.

**[INF]** Before doing that: fit an antenna (§6.2), fix the decoupling (§4.1), and read §6.3 about what it does to the product's certification.

---

## 8. Pitfalls, ranked

1. **Expecting PSRAM.** There is none. `ps_malloc()` returns `NULL`. §2.
2. **Assuming a `-32U` drops into a `-32D` footprint.** The pad rows are the same, but the **body is 6.3 mm shorter** and the PCB-antenna keepout is absent. A `-32D` will not fit a `-32U` land pattern; a `-32U` will physically fit a `-32D` land pattern but leaves a hole where the antenna was.
3. **Fitting no antenna and wondering why Wi-Fi is unusable.** Exactly what happens on the ZeroWriter keyboard. §6.2.
4. **Swapping to a higher-gain antenna and assuming the FCC grant still applies.** §6.3.
5. **Using a plain SMA jack** so end users can fit their own antenna. Generally not permitted for modular-approval products. §6.3.
6. **Specifying `-32U` for a new design.** It is NRND rev-1 silicon. Use `-32UE`. §1.2.
7. **Driving strapping pins from a key matrix without clearing them before reset.** `IO12` in particular. §5.2.
8. **Trusting the v2.7 datasheet's "LX7" claim.** It is LX6. §1.2.
9. **Sizing the supply for average current.** 379 mA peaks. §4.
10. **Repeatedly mating the u.FL connector.** It is a factory-assembly connector with a very low mating-cycle rating, not a user port.
11. **Not soldering the EPAD.** Pin 39 is RF and thermal ground.

---

## 9. Alternatives and equivalents

| Part | Drop-in for `U1`? | Comment |
|---|---|---|
| **ESP32-WROOM-32UE-N4** | ✅ **The answer.** Same footprint, same pinout, same u.FL | Rev-3 silicon, active part number, 16 KB RTC SRAM, optional 105 °C SKU |
| ESP32-WROOM-32UE-N8 / -N16 | ✅ | More flash |
| ESP32-WROOM-32UE-N4R2 | ✅ | Adds **2 MB** in-package PSRAM. Irrelevant for a keyboard; useful if the board grows |
| ESP32-WROOM-32E-N4 | ⚠ pads yes, mechanics no | PCB antenna ⇒ 25.5 mm body and a **keepout zone** the layout does not provide |
| **ESP32-WROVER-E** | ❌ | 31.4 mm body, and **loses GPIO16/17** which this design uses for `Col 8`/`Col 9`. §2.3 |
| ESP32-S3-WROOM-1U-N4 | ❌ | Different pinout, different core, but **native USB** — the obvious choice for a *new* keyboard, which is presumably why the `zw_keyboard` branch exists. §5.4 |
| ESP32-C3-MINI-1U-N4 | ❌ | Single-core RISC-V, far fewer GPIOs, **BLE only — no Classic Bluetooth**. Cheaper; would need I/O expanders for a 14 × 5 matrix |
| RP2040 + external radio | ❌ | What most keyboard designs actually use. Cheaper, better USB, better documented for HID |

---

## 10. Open questions

| Question | Status |
|---|---|
| Is the fitted part a `-32U` or has it been substituted with a `-32UE`? | **Open.** The BOM says `ESP32-WROOM-32U-N4` and LCSC `C328062` resolves to exactly that **[COM]**, so the *intent* is clear. Substitution at assembly is undetectable from the files — `esptool flash_id` reporting `ESP32-D0WD-V3` rather than `ESP32-D0WD` would reveal a `-32UE` |
| Chip revision on shipped units | **Open.** `-32U` implies rev 1, but Espressif transitioned production of several NRND modules to `-V3` dice. Only `esptool` on hardware answers it |
| Was the `zw_keyboard` ESP32-S3 design ever built? | **Open.** §5.4 |
| Does ZeroWriter's keyboard firmware clear `IO12` before any software reset? | **Open.** Firmware was not read in this pass. §5.2 |
| Exact list of antennas covered by FCC ID `2AC7Z-ESP32WROOM32U` | **Open.** The grant page held locally does not enumerate them; the full FCC exhibit set on `fccid.io` would |

---

## Manufacturer

**Espressif Systems** — see the [Espressif documentation-sourcing guide](../../../vendors/espressif/README.md) for this vendor's document portals, URL patterns, module part-numbering conventions and known gotchas.

## Used By

| Device | Board | Designator | Role |
|---|---|---|---|
| [ZeroWriter Ink](../../../devices/zerowriter/zerowriter-ink/README.md) | **Zerowriter Keyboard PCB** (not the display board) | `U1` | Key-matrix scanning, own firmware, `NOVA` 6-pin programmer header. Links to the main board over `HC-1.25-6PWT` |

**Not fitted** on [Soldered Inkplate 5](../../../devices/soldered-electronics/inkplate-5/README.md) or [Soldered Inkplate 5 Gen 2](../../../devices/soldered-electronics/inkplate-5-gen2/README.md) — neither product has a keyboard. This part exists only because of ZeroWriter's second PCB. See §5.3 for why the record is kept anyway.

## Related pages

- [espressif/esp32-wrover](../esp32-wrover/README.md) — the *other* ESP32 in ZeroWriter Ink, on the display board; and the PSRAM/GPIO16-17 contrast (§2)
- [espressif/esp32-u4wdh §21](../esp32-u4wdh/README.md#21-silicon-revisions-the-complete-matrix-and-what-v31-means) — ESP32 silicon revisions in depth. **Not duplicated here**
- [guides/espressif/ecosystem-and-product-lines.md](../../../guides/espressif/ecosystem-and-product-lines.md) — part-number decode, Classic-Bluetooth availability, module vs chip
- [guides/espressif/errata-practical.md](../../../guides/espressif/errata-practical.md) — what rev 1 vs rev 3 actually costs you
- [guides/espressif/memory-and-boot.md §4–§5](../../../guides/espressif/memory-and-boot.md#4-strapping-pins-per-chip) — strapping pins and the `VDD_SDIO` 1.8 V trap
- [guides/espressif/soc-peripheral-reference.md](../../../guides/espressif/soc-peripheral-reference.md) — peripheral and GPIO counts
- [wch/ch340c](../../wch/ch340c/README.md) — the main board's USB-UART bridge, which **cannot** flash this module
- [ZeroWriter Ink § the two-processor split](../../../devices/zerowriter/zerowriter-ink/README.md#the-single-most-important-architectural-fact)

---

## 11. Local artifacts and sources

### Artifacts held

| File | Document | Version | Bytes | sha256 |
|---|---|---|---:|---|
| `artifacts/esp32-wroom-32d-wroom-32u-datasheet.pdf` | **ESP32-WROOM-32D & ESP32-WROOM-32U Datasheet** (NRND) — the authoritative document for this part | **v2.7** | 866,305 | `a3f8da7e17d03c0600af4ba62eb161411762de9d93e46755fae6178a294e5216` |
| `artifacts/esp32-wroom-32e-wroom-32ue-datasheet.pdf` | ESP32-WROOM-32E & ESP32-WROOM-32UE Datasheet — the successor; source of the current-consumption table and the `R2` PSRAM SKUs | **v2.1** | 1,230,114 | `4c7a345d1c1bfec34c38665639e39a7f43b79a35a12f6adcc2c7c0f83850f8b8` |
| `artifacts/esp32-wroom-32-datasheet.pdf` | ESP32-WROOM-32 Datasheet (NRND) — the original generation, for lineage | **v3.7** | 619,238 | `a88f0a4376106498732580d8371009b4e6260358db2e9f3ab2deb0ee3e4fa5b6` |
| `artifacts/esp32-wroom-32u-fcc-wifi-bt40-certificate.pdf` | **FCC Grant of Equipment Authorization, FCC ID `2AC7Z-ESP32WROOM32U`**, Telefication B.V., 2018-01-22 | — | 157,379 | `2d9adc350dbdccca77a5f41932adeb70b5eac10f15fc9d2665f32861bcec9cfe` |
| `artifacts/fcc-grant-2ac7z-espwroom32ue-dts.pdf` | FCC Grant, FCC ID `2AC7Z-ESPWROOM32UE`, BACL, 2020-05-07 — the successor's grant | — | 135,451 | `7fe78b80873f1cc55e74cf74c790666a09dd703029d8ff1a23354bda0a9b9c15` |
| `artifacts/esp32-wroom-32u-ce-certification.pdf` | **Kiwa Nederland B.V. EU type-examination certificate (Module B) `172141367/AA/02`**, NB 0063, RED 2014/53/EU, issued 2023-03-02 | — | 310,745 | `0c94347915435db079e00bd1734e30440e4d09827e8fb28c936c888969e7ad2d` |
| `artifacts/lcsc-c328062-datasheet.pdf` | LCSC's mirrored datasheet for `C328062` — the **Chinese** ESP32-WROOM-32D/32U datasheet v2.4. Independent confirmation that `C328062` is this module family | v2.4 (zh) | 949,935 | `8d5e0988fdef1769ec61d867e946de9ebe3bf1db8906055845c24d9b870a8fe0` |

Also present as of 2026-08-24 are byte-identical re-downloads made during this pass under longer names (`esp32-wroom-32d_esp32-wroom-32u-datasheet-v2.7-nrnd.pdf`, `esp32-wroom-32e_esp32-wroom-32ue-datasheet-v2.1.pdf`, `esp32-wroom-32-datasheet-v3.7-nrnd.pdf`). **They duplicate the three datasheets above and carry no new information** — verified by sha256. Prefer the short names.

Chip-level documents live in [`../esp32-u4wdh/artifacts/`](../esp32-u4wdh/README.md#112-local-artifacts) and are not duplicated.

#### Reacquire

```sh
curl -sSL -o esp32-wroom-32d-wroom-32u-datasheet.pdf \
  https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32d_esp32-wroom-32u_datasheet_en.pdf
curl -sSL -o esp32-wroom-32e-wroom-32ue-datasheet.pdf \
  https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.pdf
curl -sSL -o esp32-wroom-32-datasheet.pdf \
  https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf
head -c 4 *.pdf | od -An -c        # expect  %  P  D  F
```

### Retrieval failures, 2026-08-24

Recorded in [`component-download-failures.txt`](../../../component-download-failures.txt). Summary: there is **no standalone `-32U` or `-32UE` datasheet.**

| URL | Result |
|---|---|
| `…/documentation/esp32-wroom-32u_datasheet_en.pdf` | **HTTP 200, `text/html`, 13,745 B** → `documentation.espressif.com/404`. Soft-404 |
| `…/documentation/esp32-wroom-32ue_datasheet_en.pdf` | Same soft-404 |

The `-U` variants are documented **inside** their PCB-antenna sibling's datasheet (`esp32-wroom-32d_esp32-wroom-32u_…`, `esp32-wroom-32e_esp32-wroom-32ue_…`). This is the same "one document per pair/family" convention Espressif uses throughout, and it is why searching for the exact part number fails. The general form of this behaviour — every `documentation.espressif.com` miss returning a 13,745-byte HTML shell with HTTP 200 — is in [vendors/espressif §5.1](../../../vendors/espressif/README.md).

### Design files read

| File | Used for |
|---|---|
| `devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter_ink/design/src/Zerowriter Keyboard/v1.2.0/CAD/Zerowriter Keyboard.kicad_sch` | `U1` symbol (39 pins, `RF_Module:ESP32-WROOM-32U`), every net in §3, matrix map, strapping-pin analysis |
| `…/Zerowriter Keyboard/v1.2.0/OUTPUTS/Zerowriter Keyboard.csv` | `U1 = ESP32-WROOM-32U-N4`, JLCPCB `C328062`; complete 16-line BOM used for the **no-antenna** finding (§6.2); `C1`/`C2` decoupling |
| `…/Zerowriter Keyboard/v1.2.0/PCBA/*-pos.csv` | Confirms `U1` placement and that no antenna part is placed |
| `devices/zerowriter/…/design/zw_keyboard/Kicad/OUTPUTS/Zerowriter Keyboard BOM.csv` | The alternative **ESP32-S3FH4R2 + 5 × MCP23017** keyboard design (§5.4) |
| `devices/zerowriter/…/design/src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/MCU.kicad_sch` | The WROVER on the other board, for the §2.3 contrast |

### Authoritative sources

| Title | URL | Retrieved | Version | Local artifact |
|---|---|---:|---|---|
| ESP32-WROOM-32D & ESP32-WROOM-32U Datasheet (NRND) | https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32d_esp32-wroom-32u_datasheet_en.pdf | 2026-08-24 | v2.7 | `artifacts/esp32-wroom-32d-wroom-32u-datasheet.pdf` |
| ESP32-WROOM-32E & ESP32-WROOM-32UE Datasheet | https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.pdf | 2026-08-24 | v2.1 | `artifacts/esp32-wroom-32e-wroom-32ue-datasheet.pdf` |
| ESP32-WROOM-32 Datasheet (NRND) | https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf | 2026-08-24 | v3.7 | `artifacts/esp32-wroom-32-datasheet.pdf` |
| LCSC product record for `C328062` — resolves the ordering code, brand, package `SMD,19.2x18mm`, die `ESP32-D0WD` | https://www.lcsc.com/product-detail/C328062.html | 2026-08-24 | — | `artifacts/lcsc-c328062-datasheet.pdf` (the mirrored datasheet) |
| FCC Grant, FCC ID `2AC7Z-ESP32WROOM32U` | *(TCB grant, Telefication B.V., cert. 182180022/AA/00, 2018-01-22)* | 2026-08-26 | — | `artifacts/esp32-wroom-32u-fcc-wifi-bt40-certificate.pdf` |
| FCC Grant, FCC ID `2AC7Z-ESPWROOM32UE` | *(TCB grant, Bay Area Compliance Laboratory Corp., 2020-05-07)* | 2026-08-26 | — | `artifacts/fcc-grant-2ac7z-espwroom32ue-dts.pdf` |
| Kiwa EU type-examination certificate `172141367/AA/02` | *(Kiwa Nederland B.V., NB 0063, 2023-03-02)* | 2026-08-26 | — | `artifacts/esp32-wroom-32u-ce-certification.pdf` |
| Espressif certificate portal | https://www.espressif.com/en/certificates | 2026-08-24 | — | – |

### Retrieval notes

`www.lcsc.com/product-detail/C328062.html` returned **HTTP 200 and a usable 378 KB page with a plain Chrome-131 User-Agent** on 2026-08-24; the embedded JSON (`productModel`, `brandNameEn`, `encapStandard`, `productIntroEn`) is the source of the **[COM]** rows in §1. By contrast, `wmsc.lcsc.com/ftps/wm/search/global` returned an Akamai **Access Denied** page and `jlcpcb.com/api/luxService/getComponentDetailByComponentCode` returned an empty body — the product-detail HTML page is the working route. Added to [`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

> **Evidence boundary.** Every electrical figure in §4 and every pin function in §3 is **[DOC]**; the current-consumption table is **[DOC]** but from the *successor* datasheet and is therefore **[INF]** as applied to the `-32U`. Every net and every BOM fact is **[SCH]** from extraction over the ZeroWriter KiCad sources. §6.3's grant text is **[DOC]** verbatim; the interpretation table under it is **[INF]** from standard modular-approval practice and is **not** legal advice. §6.2's "no antenna is fitted" is a **negative** finding from an exhaustive search of the design tree — strong, but a negative.
