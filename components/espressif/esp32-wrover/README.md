# Espressif ESP32-WROVER

- **Category:** Wi-Fi + Bluetooth + Bluetooth LE **module** — an ESP32 die, SPI flash, **PSRAM**, a 40 MHz crystal, RF matching and an antenna, in one shielded, pre-certified can
- **Defining feature:** the integrated **PSRAM**. That is the entire reason the WROVER line exists alongside the WROOM line, and the reason every Inkplate uses one
- **Package:** 38-pin SMD castellated module, **18.0 × 31.4 × 3.3 mm**, plus a large ground EPAD
- **Fitted on:** `U10` (Inkplate 5), `U11` (Inkplate 5 Gen 2 and the ZeroWriter respin)
- **Research date:** 2026-08-24; datasheets retrieved 2026-08-24

> **⚠ Read §2 before you do anything else.** On a WROVER, **GPIO16 and GPIO17 do not exist as usable pins** — the PSRAM eats them, and module pins 27 and 28 are physically NC. This is the single most common WROVER mistake and it is invisible until you try to use those pins.

---

## Evidence labelling

Same scheme as the sibling records ([TPS65186](../../texas-instruments/tps65186/README.md), [PCAL6416A](../../nxp/pcal6416a/README.md)).

| Marker | Meaning |
|---|---|
| **[DOC]** | Stated by Espressif in a document retrieved into `artifacts/` |
| **[SCH]** | Read out of the KiCad schematic sources under the device `artifacts/hardware/` trees, via net extraction |
| **[SRC]** | Read out of vendor-shipped source (Inkplate Arduino library / MicroPython snapshots) |
| **[COM]** | Distributor/marketplace data — part identity, packaging, stock |
| **[WEB]** | Non-manufacturer web source, dated at retrieval |
| **[INF]** | Inference. Not established by the above |

Anything marked **UNRESOLVED** is a genuine open question, not a hedge.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | Espressif Systems (Shanghai) Co., Ltd. | **[DOC]** |
| Class | 2.4 GHz Wi-Fi 802.11 b/g/n + Bluetooth v4.2 BR/EDR + Bluetooth LE module | **[DOC]** WROVER-E DS v2.4 §1.1 |
| SoC inside | `ESP32-D0WDQ6` (original WROVER) → `ESP32-D0WD` (WROVER-B) → `ESP32-D0WD-V3` / `ESP32-D0WDR2-V3` (WROVER-E) | **[DOC]** each datasheet §1.1 |
| Core | Xtensa **LX6** dual-core 32-bit, 80–240 MHz | **[DOC]** |
| On-chip memory | 448 KB ROM, 520 KB SRAM, 8 KB (B) / 16 KB (E) RTC SRAM | **[DOC]** |
| Integrated crystal | 40 MHz | **[DOC]** |
| Integrated flash | 4 / 8 / 16 MB Quad SPI | **[DOC]** |
| **Integrated PSRAM** | **8 MB Quad SPI** on every non-EOL SKU | **[DOC]** |
| Antenna | PCB trace antenna (WROVER / -B / -E) **or** u.FL/IPEX connector (-I / -IB / -IE) | **[DOC]** |
| Supply | 3.0–3.6 V (3.3 V typ.); **external supply must be able to deliver ≥ 0.5 A** | **[DOC]** WROVER-E DS Table 14 |
| Ambient | −40 … +85 °C | **[DOC]** |
| Module dimensions | 18.0 × 31.4 × 3.3 mm (±0.10 on each axis) | **[DOC]** |
| MSL | Level 3 | **[DOC]** original WROVER DS Table 2 |

### 1.1 What a "WROVER" actually is, and why you would buy one

A WROVER is not a chip. It is a **complete, tested, pre-certified 2.4 GHz radio subsystem** on a 18 × 31.4 mm PCB with a tin can soldered over it. Inside the can:

| Inside the shield | Why it is there |
|---|---|
| ESP32 die (D0WDQ6 / D0WD / D0WD-V3) | The MCU + radio |
| 40 MHz crystal + load caps | The RF reference clock. Getting this wrong is the classic bare-chip failure |
| SPI NOR flash (4/8/16 MB) | Code and data storage, on the `VDD_SDIO` domain |
| **SPI PSRAM (8 MB)** | The differentiator — see §6 |
| RF balun, π-match, harmonic filter | Tuned once, by Espressif, against a real network analyser |
| PCB trace antenna **or** u.FL connector | Ditto |
| RTC 32 kHz oscillator components, decoupling | |

The value proposition is **§8: you inherit Espressif's FCC/CE/BQB certification**, you inherit a matched antenna, and you never have to lay out a 50 Ω line. The cost is 3.3 mm of height, a fixed flash/PSRAM configuration, and the loss of GPIO6–11, 16 and 17.

### 1.2 The variant matrix — this is what you actually need

**[DOC]**, assembled from the three datasheets held in `artifacts/`. Read the **PSRAM voltage** column carefully; it is the difference between a working design and a dead one (§5).

| Module | Die | Flash | PSRAM | PSRAM/flash rail | Antenna | Body (mm) | Lifecycle |
|---|---|---|---|---|---|---|---|
| **ESP32-WROVER** | `ESP32-D0WDQ6` (rev 1) | 4 MB | 8 MB | **1.8 V** ⚠ | PCB | 18.0 × 31.4 × 3.3 | **NRND** (DS v2.7 cover) |
| **ESP32-WROVER-I** | `ESP32-D0WDQ6` | 4 MB | 8 MB | **1.8 V** ⚠ | **u.FL** | 18.0 × 31.4 × 3.5 *(unverified)* | **NRND** |
| **ESP32-WROVER-B** | `ESP32-D0WD` (rev 1) | 4 / 8 / 16 MB | 8 MB | 3.3 V | PCB | 18.0 × 31.4 × 3.3 | **NRND** (DS v2.3 cover) |
| **ESP32-WROVER-IB** | `ESP32-D0WD` | 4 / 8 / 16 MB | 8 MB | 3.3 V | **u.FL** | 18.0 × 31.4 × 3.3 | **NRND** |
| **ESP32-WROVER-E** | `ESP32-D0WD-V3` or `ESP32-D0WDR2-V3` | 4 / 8 / 16 MB | **8 MB** (R8) or 2 MB (R2, **EOL**) | 3.3 V | PCB | 18.0 × 31.4 × 3.3 | **Active** |
| **ESP32-WROVER-IE** | same as -E | same as -E | same as -E | 3.3 V | **u.FL** | 18.0 × 31.4 × 3.3 | **Active** |

Ordering-code suffixes on the -B and -E families **[DOC]**:

```
ESP32-WROVER-E - N4 R8
                 │  └── R<n> = PSRAM in MB   (R8 = 8 MB, R2 = 2 MB and EOL)
                 └───── N<n> = flash in MB   (N4 / N8 / N16)
   I  = u.FL external-antenna connector instead of the PCB antenna
```

The general Espressif suffix decode (`D0WD`, `R2`, `-V3`, `H`, `Q6`) lives in
[guides/espressif/ecosystem-and-product-lines.md §7.1](../../../guides/espressif/ecosystem-and-product-lines.md#71-classic-esp32--the-authoritative-decode) and is **not** repeated here.

Four traps in that table:

1. **The original WROVER's memory is 1.8 V.** The -B and -E are 3.3 V. This is *not* a cosmetic difference — see §5.
2. **`R2` SKUs are EOL.** On a WROVER-E, `R2` means the PSRAM is *in the ESP32-D0WDR2-V3 package*, not a separate die. Espressif has marked every `R2` WROVER-E EOL **[DOC]** DS v2.4 Tables 1–2, so in practice a WROVER-E is an `R8`.
3. **The GPIO count changed between datasheet generations for the same silicon.** WROVER-B DS v2.3 says *"Up to 30 GPIOs"*; WROVER-E DS v2.4 says *"Up to 24 GPIOs"* **[DOC]**. The silicon did not lose six pins — Espressif changed what it was willing to count. **[INF]** Trust the pin table (§3), not the feature bullet. Chip-level GPIO accounting is in [guides/espressif/soc-peripheral-reference.md §11](../../../guides/espressif/soc-peripheral-reference.md#11-gpio--count-restrictions-and-what-the-memory-eats).
4. **The `-B` and `-E` are pin- and footprint-compatible**, so a board drawn for one will accept the other. That is convenient and it is also why boards ship with whichever is in stock, which is why §1.3 is unresolved.

### 1.3 Which variant the Inkplate boards actually fit — **partially resolved**

This was recorded as fully open in the previous revision of this record. It is now narrowed to two candidates.

**What the design files say [SCH]:**

| Board | Designator | Symbol / footprint | File |
|---|---|---|---|
| Soldered Inkplate 5 V1.2.0 | `U10` | `e-radionica.com schematics:ESP32-WROVER` / `e-radionica.com footprinti:ESP32-WROVER` | `devices/soldered-electronics/inkplate-5/artifacts/hardware/soldered-inkplate-5-hardware-design/CAD/V1.2.0/MCU.kicad_sch` |
| Soldered Inkplate 5 V1.2.0 BOM | `U10` | value `ESP32-WROVER`, package `ESP32-WROVER` | `…/OUTPUTS/V1.2.0/Soldered Inkplate 5 BOM.csv` line 57 |
| ZeroWriter Inkplate 5 Gen2 v1.2.0 | `U11` | `Soldered symbols:ESP32-WROVER` | `devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter_ink/design/src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/MCU.kicad_sch` |
| ZeroWriter Inkplate 5 Gen2 BOM | `U11` | value `ESP32-WROVER`, footprint `ESP32-WROVER`, **no JLCPCB part number** | `…/OUTPUTS/Zerowriter Inkplate 5 Gen2.csv` |

**The BOMs carry no suffix and no distributor part number.** Soldered drew a generic symbol and left the buyer to choose.

**What narrows it [DOC]:** Soldered's own hardware reference describes the family's ESP32 as

> *"WiFi with PCB antenna, BLE, 4MB Flash, 8MB PSRAM, 240MHz"*
> — `devices/soldered-electronics/inkplate-5/artifacts/docs/Inkplate-documentation/source/hardware-reference.rst` line 26

| Claim | Excludes |
|---|---|
| **PCB antenna** | -I, -IB, -IE (all u.FL) |
| **8 MB PSRAM** | every WROVER-E `R2` SKU |
| **4 MB flash** | `N8`, `N16` |

That leaves **ESP32-WROVER-N4R8-equivalent, ESP32-WROVER-B-N4R8, or ESP32-WROVER-E-N4R8**.

**Ruling out the original WROVER [SCH] — this is the strong argument.** The original WROVER's flash and PSRAM are 1.8 V parts, and Espressif states the module therefore **pulls MTDI (GPIO12) high internally**:

> *"The MTDI is internally pulled high in the module, as the flash and SRAM in ESP32-WROVER only support a power voltage of 1.8 V (output by VDD_SDIO)."*
> — **[DOC]** original WROVER DS v2.7 §2.3 note

On the Inkplate, **GPIO12 is the microSD `SPI_MISO` line** (`U10.14` → net `SPI_MISO` → `K11.7[MISO]`), with `R45` = 100 kΩ pulling it up **to the switched `3V3_MICROSD` rail** — see §5.3. A module that also pulls GPIO12 high internally would work, but Soldered's schematic treats GPIO12 as an ordinary SPI pin with an external pull-up, which is the -B/-E convention. Combined with the fact that Inkplate 5 Gen 2 is a current product and both the original WROVER and the -B are NRND, the practical answer is:

> **[INF], high confidence: ESP32-WROVER-E-N4R8** on current production of both generations, with **ESP32-WROVER-B-N4R8** possible on early Inkplate 5 units.

**How to close it in ten seconds, on hardware:**

```sh
esptool --chip esp32 --port /dev/ttyUSB0 flash_id
#   "Chip is ESP32-D0WD-V3 (revision v3.1)"  -> WROVER-E
#   "Chip is ESP32-D0WD   (revision v1.0/v1.1)" -> WROVER-B
#   "Chip is ESP32-D0WDQ6 (revision v1.0)"   -> original WROVER
#   "Detected flash size: 4MB"
```

or read the can — the variant is laser-marked on the shield — or, from firmware:

```c
#include "esp_chip_info.h"
#include "esp_psram.h"
esp_chip_info_t ci; esp_chip_info(&ci);
printf("rev %d, psram %u bytes\n", ci.revision, (unsigned)esp_psram_get_size());
```

Silicon-revision decoding (v1 vs v3.0 vs v3.1, the two competing numbering schemes, and what each revision fixed) is covered exhaustively in
[esp32-u4wdh §21](../esp32-u4wdh/README.md#21-silicon-revisions-the-complete-matrix-and-what-v31-means). **Do not re-derive it here.**

---

## 2. ⚠ GPIO16 and GPIO17 do not exist on a WROVER

This is the headline. It catches people who port a WROOM design, people reading a generic "ESP32 pinout" poster, and people copying an Arduino example.

### 2.1 The rule, from Espressif

> *"External connections can be made to any GPIO except for GPIOs in the range 6-11, 16, or 17. GPIOs 6-11 are connected to the module's integrated SPI flash and PSRAM. **GPIOs 16 and 17 are connected to the module's integrated PSRAM.**"*
> — **[DOC]** ESP32-WROVER Datasheet v2.7 §4 note 2 (`artifacts/esp32-wrover-datasheet-v2.7-nrnd-wayback.pdf`)

On the -B and -E the wording moves into the pin table itself, and the pins are simply gone:

| Module pin | ESP32-WROOM-32/32D/32U | **ESP32-WROVER / -B / -E** | Evidence |
|---:|---|---|---|
| 17–22 | `SD2 SD3 CMD CLK SD0 SD1` (GPIO9,10,11,6,7,8 — flash) | `NC` "See note 2" | **[DOC]** WROVER-E DS Table 3 |
| **27** | **`IO16`** | **`NC`** | **[DOC]** WROVER-E DS Table 3 |
| **28** | **`IO17`** | **`NC`** | **[DOC]** WROVER-E DS Table 3 |
| 32 | `NC` | `NC` | **[DOC]** both |

And the module schematic in WROVER-E DS Chapter 8 shows the wiring explicitly: `GPIO16 → SRAM_CLK`, `GPIO17 → SRAM_CS`, both terminating on the PSRAM die inside the can **[DOC]**.

### 2.2 The Inkplate schematic proves it independently

Soldered's own KiCad symbol is the cleanest possible confirmation. The `ESP32-WROVER` symbol has **36 pins, and pins 27, 28 and 32 are not drawn at all** **[SCH]**:

```
 1 GND      9 IO33    17 SD2     25 IO0     33 IO21
 2 VDD33   10 IO25    18 SD3     26 IO4     34 RXD0
 3 EN      11 IO26    19 CMD     ── 27 absent   35 TXD0
 4 SENSOR_VP 12 IO27  20 CLK     ── 28 absent   36 IO22
 5 SENSOR_VN 13 IO14  21 SD0     29 IO5     37 IO23
 6 IO34    14 IO12    22 SD1     30 IO18    38 GND
 7 IO35    15 GND     23 IO15    31 IO19    39 GND (EPAD)
 8 IO32    16 IO13    24 IO2     ── 32 absent
```

Extracted from `MCU.kicad_sch` (Inkplate 5 V1.2.0) and from the ZeroWriter Gen2 respin's `CAD/MCU.kicad_sch`, which uses the identically-shaped `Soldered symbols:ESP32-WROVER` — same 36 pins, same three omissions **[SCH]**.

### 2.3 The same product proves the contrast

ZeroWriter Ink carries **two** ESP32 modules on two boards, and they behave differently on exactly these pins:

| Board | Module | Pin 27 | Pin 28 | What it is used for |
|---|---|---|---|---|
| Zerowriter Inkplate 5 Gen2 | **ESP32-WROVER** (`U11`) | **absent** | **absent** | nothing — cannot be |
| Zerowriter Keyboard | **ESP32-WROOM-32U-N4** (`U1`) | `IO16` | `IO17` | **key-matrix `Col 8` and `Col 9`** |

`NET Col 8: CH22.1, CH36.1, CH49.1, CH8.1, U1.27[IO16]` and `NET Col 9: …, U1.28[IO17]` **[SCH]**, from
`devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter_ink/design/src/Zerowriter Keyboard/v1.2.0/CAD/Zerowriter Keyboard.kicad_sch`.

**Two of the keyboard's fourteen matrix columns would be unroutable if the designer had used a WROVER.** That is the practical size of the trap.

### 2.4 What this costs you, in pins

Of the ESP32's 34 programmable GPIOs, a WROVER hands you **24 usable pins** and a WROOM hands you **26** **[DOC]** (WROVER-E DS v2.4 vs WROOM-32E DS v2.1 feature bullets). The eight you never see are GPIO6–11 (flash + PSRAM data/clock/CS) plus GPIO16–17 (PSRAM clock + CS). GPIO20 does not exist on the ESP32 at all.

**[INF] Design rule:** when you budget pins for a WROVER design, start from the list of module pins in §3 and never from a chip pinout diagram.

---

## 3. Pin table, with the nets on these boards

38 signal pins plus the EPAD (numbered 39 by Espressif and by Soldered's symbol). Nets are from `MCU.kicad_sch`, Inkplate 5 V1.2.0 **[SCH]**; Gen 2 is identical except the designator changes from `U10` to `U11`.

| Pin | Name | GPIO | Type | Inkplate 5 net | Role on the board |
|---:|---|---|---|---|---|
| 1 | `GND` | — | P | `GND` | |
| 2 | `VDD33` | — | P | `3V3` | Also feeds `U9` PCAL6416A `VDD`/`VDD(I2C_bus)`. Local bulk: `C50`–`C54` 100 n + `C55` |
| 3 | `EN` | — | I | `RST` | Driven by `U2` `TPS3840PL27` open-drain `RESET`; shared with `U9.24 nRESET` |
| 4 | `SENSOR_VP` | 36 | **input-only** | `GPIO_36` | Broken out to header pad `K36`; also the `SW3` wake button via `R41` |
| 5 | `SENSOR_VN` | 39 | **input-only** | `GPIO_39` | Header `K35`; **RTC interrupt via solder jumper `JP2` — see §3.1** |
| 6 | `IO34` | 34 | **input-only** | `IO34` | Jumper `JP4` |
| 7 | `IO35` | 35 | **input-only** | `V_BAT` | Battery-voltage ADC divider |
| 8 | `IO32` | 32 | I/O | `EPD_CKV` | E-paper `CKV` |
| 9 | `IO33` | 33 | I/O | `EPD_SPH` | E-paper `SPH` |
| 10 | `IO25` | 25 | I/O | `EPD_D5` | Parallel data bit 5 |
| 11 | `IO26` | 26 | I/O | `EPD_D6` | Parallel data bit 6 |
| 12 | `IO27` | 27 | I/O | `EPD_D7` | Parallel data bit 7 |
| 13 | `IO14` | 14 | I/O | `SPI_SCK` | microSD clock; header `K32` |
| 14 | `IO12` | 12 | I/O | `SPI_MISO` | microSD MISO. **Also MTDI — see §5.3** |
| 15 | `GND` | — | P | `GND` | |
| 16 | `IO13` | 13 | I/O | `SPI_MOSI` | microSD MOSI; header `K34` |
| 17–22 | `SD2 SD3 CMD CLK SD0 SD1` | 9,10,11,6,7,8 | — | **unconnected** | Internal flash bus. Soldered leaves all six floating **[SCH]** |
| 23 | `IO15` | 15 | I/O | `SPI_CS` | microSD chip-select (also MTDO strap) |
| 24 | `IO2` | 2 | I/O | `EPD_LE` | E-paper `LE` (also a boot strap) |
| 25 | `IO0` | 0 | I/O | `GPIO_0` | Boot strap; auto-reset from `Q3`; `R21` 0 Ω to unpopulated `Q1` |
| 26 | `IO4` | 4 | I/O | `EPD_D0` | Parallel data bit 0 |
| **27** | **`NC`** | *(16)* | — | — | **PSRAM `SRAM_CLK` inside the can** |
| **28** | **`NC`** | *(17)* | — | — | **PSRAM `SRAM_CS` inside the can** |
| 29 | `IO5` | 5 | I/O | `EPD_D1` | Parallel data bit 1 (also an SDIO-timing strap) |
| 30 | `IO18` | 18 | I/O | `EPD_D2` | Parallel data bit 2 |
| 31 | `IO19` | 19 | I/O | `EPD_D3` | Parallel data bit 3 |
| 32 | `NC` | — | — | — | |
| 33 | `IO21` | 21 | I/O | `I2C_SDA` | I²C0 data → `U9.20` |
| 34 | `RXD0` | 3 | I/O | `RXD` | From `U3` CH340C `TXD` through `R24` 1 kΩ |
| 35 | `TXD0` | 1 | I/O | `TXD` | To `U3` CH340C `RXD` through `R23` 1 kΩ |
| 36 | `IO22` | 22 | I/O | `I2C_SCL` | I²C0 clock → `U9.19` |
| 37 | `IO23` | 23 | I/O | `EPD_D4` | Parallel data bit 4 |
| 38 | `GND` | — | P | `GND` | |
| 39 | `GND` (EPAD) | — | P | `GND` | Thermal/RF ground pad. **Must be soldered** |

Note pins 4–7: **GPIO34–39 are input-only, with no output driver and no internal pull-up/pull-down** **[DOC]**. Soldered uses all four correctly (battery ADC, RTC interrupt, wake button, jumper).

### 3.1 `GPIO39` is on a solder jumper, and it is not hard-wired to the RTC

The schematic sheets leave this ambiguous — the `GPIO_39` and RTC-`INT` labels are drafted as dangling stubs in `SD & RTC.kicad_sch` and do not resolve by label matching. The **PCB netlist settles it** **[SCH]**, `Soldered Inkplate 5.kicad_pcb`:

```
NET GPIO_39                    : U10.5, K35.1, JP2.2      <- centre pad
NET Net-(JP2-Pad1)             : JP2.1, R42.1, U7.4[INT]  <- PCF85063A interrupt, R42 10k pull-up
NET /SD & RTC/CLKOUT_RTC       : JP2.3, U7.9[CLKOUT]      <- PCF85063A clock output
```

`JP2` is one of five `SMD_JUMPER_3_PAD_CONNECTED_LEFT_TRACE` parts on the board **[SCH]** BOM group 36. Its centre pad (2) is `GPIO39`; pad 1 is the RTC's `INT`; pad 3 is the RTC's `CLKOUT`. The footprint name says the centre is joined to the **left** pad by a fabricated trace.

So, as shipped: **`GPIO39` = `PCF85063A` `INT`**, pulled up by `R42` 10 kΩ to `3V3_RTC`. Cutting the trace and bridging 2–3 instead swaps `GPIO39` onto the RTC's `CLKOUT` — a configurable 1 Hz / 1024 Hz / 32.768 kHz square wave, useful as a wake source or a calibration reference. **[INF]** which position a given unit ships in was not verified on hardware; the "left trace" default is read from the footprint name, not from a fab drawing.

`GPIO36` is unambiguous by comparison: `U10.4, K36.1, R41.1, SW3.2` **[SCH]** — the `SW3` wake button, with `R41` 10 kΩ pulling up to 3V3.

---

## 4. Electrical characteristics and what they mean for the power supply

**[DOC]** WROVER-E/-IE Datasheet v2.4 §6, and original WROVER DS v2.7 §5.

| Symbol | Parameter | Value |
|---|---|---|
| `VDD33` | Supply, recommended | 3.0 / **3.3** / 3.6 V |
| `VDD33` | Absolute maximum | −0.3 … **3.6 V** |
| `IVDD` | **Current the external supply must be able to deliver** | **≥ 0.5 A** |
| — | Average operating current | ~80 mA **[DOC]** original WROVER DS Table 2 |
| — | **Peak TX**, 802.11b 1 Mbps DSSS @ 19.5 dBm | **350 mA** |
| — | Peak TX, 802.11g 54 Mbps OFDM @ 14.0 dBm | 243 mA |
| — | Peak TX, 802.11n HT20 MCS7 @ 13.0 dBm | 233 mA |
| — | RX, 802.11b/g/n HT20 | 108 mA |
| `VIH` / `VIL` | Input thresholds | 0.75 × VDD / 0.25 × VDD |
| `VOH` / `VOL` | Output levels | ≥ 0.8 × VDD / ≤ 0.1 × VDD |
| `IOH` | Source current, `VDD3P3_CPU` / `VDD3P3_RTC` | 40 mA per pin, derating to ~29 mA as more pins source |
| `IOL` | Sink current | 28 mA |
| `RPU` / `RPD` | Internal pull resistors | ~45 kΩ |
| `Ioutput` | **Cumulative** I/O output current, absolute max | 1,100 mA **[DOC]** (WROOM-32D/U DS Table 13; same die) |
| `VIL_nRST` | `EN` low threshold to shut the chip down | ≤ 0.6 V |

### 4.1 The 350 mA peak is a *supply design* number, not a trivia number

The gap between "80 mA average" and "350 mA peak" is the whole story. Wi-Fi TX bursts are short (hundreds of µs) but they are steep, and the module has only its own internal decoupling. Two consequences:

1. **The regulator must not brown out.** Espressif specifies `IVDD ≥ 0.5 A` for exactly this reason. A regulator sized for the *average* current will sag on the first association attempt and the symptom is `brownout detector was triggered` on the serial console, or a Wi-Fi connect that fails only at low battery.
2. **The bulk capacitance must be local.** Espressif's hardware design guidelines call for a large bulk cap near pin 2 in addition to the module's internal decoupling.

**What the Inkplate does [SCH]:** `U10.2` carries `C50`, `C51`, `C52`, `C53`, `C54` (100 nF 0603 each) plus `C55`, a polarised bulk part which the V1.2.0 BOM lists as **`DNP` in a 2917C footprint** — i.e. the pad for a large tantalum is there and *not populated*. The 3V3 rail instead comes from `U6` `TPS7A2633DRVR`, a low-`Iq` LDO chosen for the 22 µA sleep figure Soldered advertises, backed by `C21`/`C27`/`C51` 10 µF parts on the rail. **[INF]** The design leans on the rail's bulk rather than on a dedicated cap at the module; that is a defensible choice given the LDO is a few millimetres away, but it is why `C55` exists as a stuffing option.

**[INF] If you are copying this design:** populate the bulk cap. 22 µF close to pin 2 is Espressif's own recommendation and it costs nothing.

### 4.2 The other 350 mA consumer

On the Inkplate the ESP32 is *not* the peak load — the [TPS65186](../../texas-instruments/tps65186/README.md) EPD PMIC generating ±15 V rails during a refresh is. **[INF]** If you ever plan a design where the panel refreshes while Wi-Fi transmits, size for both. The Inkplate library serialises them in practice, but nothing in hardware enforces it.

---

## 5. ⚠ The `VDD_SDIO` / MTDI question, in its WROVER-specific form

The general form of this trap — MTDI (GPIO12) selecting 1.8 V or 3.3 V for the flash/PSRAM rail at reset, and what happens when you get it wrong — is documented at length in
**[guides/espressif/memory-and-boot.md §5.1](../../../guides/espressif/memory-and-boot.md#51-esp32-vdd_sdio-mtdi-and-the-18-v-trap)** and
**[esp32-u4wdh §§18.3–18.4](../esp32-u4wdh/README.md)**. Read those first. This section only records what is *specific to WROVER modules*.

### 5.1 The original WROVER inverts the usual polarity

Most ESP32 designs want `VDD_SDIO` = 3.3 V and therefore want MTDI **low** at reset. The original ESP32-WROVER wants the **opposite**, because its flash and PSRAM dice are 1.8 V parts:

> *"The MTDI is internally pulled high in the module, as the flash and SRAM in ESP32-WROVER only support a power voltage of 1.8 V (output by VDD_SDIO)."* **[DOC]** DS v2.7 §2.3

and

> *"GPIO12 is internally pulled high in the module and is not recommended for use as a touch pin."* **[DOC]** DS v2.7 §2.2 note 1 and §4 note 1

So on an original WROVER, **GPIO12 is spoken for**: it carries an internal pull-up you cannot remove, it cannot be a touch pin, and pulling it low externally at reset switches a 1.8 V memory die onto the 3.3 V rail. That is the destructive direction for this variant.

### 5.2 WROVER-B and WROVER-E revert to the normal case

Both later datasheets state MTDI's default as **pull-down = 0 → `VDD_SDIO` from `VDD3P3_RTC` (3.3 V)** and carry **no** GPIO12 notice **[DOC]** (WROVER-B DS v2.3 §3.2 and Table 6; WROVER-E DS v2.4 §4.2 and Table 4). The WROVER-E series tables even add an explicit `VDD_SDIO Voltage = 3.3 V` column.

**[INF] Consequence:** the *dangerous* direction flips between variants. On the original WROVER, pulling GPIO12 low is bad. On the -B/-E, pulling GPIO12 high is bad. A board that works with one may not work with the other, even though they are pin-compatible. **UNRESOLVED:** whether Espressif burns `EFUSE_SDIO_FORCE`/`EFUSE_SDIO_TIEH` at the factory on -B/-E modules to make the strap irrelevant. The datasheets describe the eFuse override mechanism but do not say it is pre-burnt. Check with `espefuse.py summary` on your own unit before relying on either behaviour.

### 5.3 The Inkplate puts a pull-up on GPIO12 — and the microSD power switch is what makes it safe

This is a genuine, non-obvious interaction, and it is worth understanding before you modify an Inkplate.

**[SCH]** from `SD & RTC.kicad_sch` (Inkplate 5 V1.2.0):

```
NET SPI_MISO   : K11.7[MISO], R45.1, U10.14[IO12]
NET 3V3_MICROSD: K11.4[VDD], Q10.3[D], R43.2, R44.2, R45.2, C37.2, C38.2, C39.2, JP1.1
NET GPB_2      : Q10.1[G], R40.2            <- PCAL6416A P1_2, via R40 100 k to 3V3
```

- `R45` = **100 kΩ** (BOM group 25), pulling `SPI_MISO` — which is **GPIO12/MTDI** — up to `3V3_MICROSD`.
- `3V3_MICROSD` is gated by `Q10`, a `SSM3J358R` P-channel MOSFET, whose gate `GPB_2` is `P1_2` on the [PCAL6416A](../../nxp/pcal6416a/README.md) I/O expander, with `R40` 100 kΩ pulling the gate up to 3V3.

At power-on the PCAL6416A's ports default to **inputs (high-Z)** and its `nRESET` is tied to the same `RST` net as the ESP32's `EN`, so `P1_2` is high-Z, `R40` holds the PMOS gate at 3V3, the PMOS is **off**, `3V3_MICROSD` is **dead**, and `R45` therefore pulls up to nothing. GPIO12 sees only its internal ~45 kΩ pull-down. **MTDI = 0 → `VDD_SDIO` = 3.3 V.** Correct for a WROVER-B/-E.

> **⚠ [INF] The hazard this creates.** The microSD power switch (documented as a *power-saving* feature in [PCAL6416A §5.2](../../nxp/pcal6416a/README.md#52-the-microsd-power-switch--p1_2)) is *also* what keeps GPIO12 low at reset. Strapping latches re-sample on **any** system reset, and `esp_restart()` does not toggle `EN` or the expander's `nRESET`. So a firmware path that (a) powers the SD card on, then (b) calls `esp_restart()` without first powering it off, leaves `R45` pulling GPIO12 up through a live rail at the moment the latch samples — MTDI reads 1, `VDD_SDIO` switches to the internal 1.8 V LDO, and a 3.3 V flash/PSRAM die is under-volted. The chip typically fails to boot rather than being damaged, but it is a boot loop with no obvious cause.
>
> This is **[INF]** — reasoned from the schematic plus Espressif's strapping-latch semantics, **not observed on hardware.** The 100 kΩ pull-up against the ESP32's ~45 kΩ internal pull-down forms a divider at roughly 3.3 × 45/145 ≈ 1.0 V, which is **below** the 0.75 × VDD ≈ 2.5 V `VIH` — so in the steady state the strap probably still reads 0. **UNRESOLVED**, and worth measuring if you ever see an Inkplate that boot-loops after a soft reset with a card inserted. Safe practice regardless: power the SD rail down before `esp_restart()`.

---

## 6. Why an Inkplate *must* be a WROVER: the framebuffer arithmetic

The previous revision of this record gave two buffers and ~576 KB. The driver actually allocates **four**, and the real number is larger.

**[SRC]** `Inkplate-Arduino-library/src/boards/Inkplate5V2/Inkplate5V2Driver.cpp` `EPDDriver::initializeFramebuffers()`, lines 862–866 (identical shape in `Inkplate5/Inkplate5Driver.cpp` lines 921–925):

```c
DMemoryNew  = (uint8_t *)ps_malloc(E_INK_WIDTH * E_INK_HEIGHT / 8);  // 1 bpp, "old" B/W
_partial    = (uint8_t *)ps_malloc(E_INK_WIDTH * E_INK_HEIGHT / 8);  // 1 bpp, partial-update
_pBuffer    = (uint8_t *)ps_malloc(E_INK_WIDTH * E_INK_HEIGHT / 4);  // 2 bpp, waveform scratch
DMemory4Bit = (uint8_t *)ps_malloc(E_INK_WIDTH * E_INK_HEIGHT / 2);  // 4 bpp, greyscale
GLUT  = (uint32_t *)malloc(256 * 9 * sizeof(uint32_t));              // internal RAM
GLUT2 = (uint32_t *)malloc(256 * 9 * sizeof(uint32_t));              // internal RAM
```

`ps_malloc()` is Arduino-ESP32's PSRAM allocator (`heap_caps_malloc(..., MALLOC_CAP_SPIRAM)`). Working the numbers **[SRC]** (`waveforms.h`: Inkplate 5 = 960 × 540; Inkplate 5 Gen 2 = 1280 × 720):

| Buffer | Bits/px | **Inkplate 5** (518,400 px) | **Inkplate 5 Gen 2** (921,600 px) |
|---|---:|---:|---:|
| `DMemoryNew` | 1 | 64,800 B | 115,200 B |
| `_partial` | 1 | 64,800 B | 115,200 B |
| `_pBuffer` | 2 | 129,600 B | 230,400 B |
| `DMemory4Bit` | 4 | 259,200 B | 460,800 B |
| **PSRAM total** | | **518,400 B ≈ 506 KB** | **921,600 B = 900 KB** |
| `GLUT` + `GLUT2` (internal SRAM) | | 18,432 B | 18,432 B |

Against the ESP32's **520 KB of on-chip SRAM** — of which perhaps 300–320 KB is actually available to the heap once the ROM, the Wi-Fi/BT stacks and FreeRTOS have taken theirs:

- **Inkplate 5 Gen 2 at 900 KB is not close.** It exceeds total on-chip SRAM by 73 %.
- **Inkplate 5 at 506 KB is also not close.** It is 97 % of the *entire* SRAM before anything else exists.

> **A WROOM-based Inkplate of either generation is impossible.** This is not a "PSRAM makes it nicer" situation; it is a hard architectural constraint, and it is why the [ED052TC4](../../e-ink/ed052tc4/README.md) panel's resolution and the choice of module are the same decision.

There is a second, subtler reason. The parallel-EPD bus is clocked by **I2S1 in LCD/parallel output mode with DMA** (the ESP32 has no LCD peripheral — see [Inkplate 5 § e-paper interface](../../../devices/soldered-electronics/inkplate-5/README.md#how-the-e-paper-interface-actually-works)). The DMA line buffer must live in **internal** RAM:

```c
_dmaLineBuffer = (uint8_t *)heap_caps_malloc((E_INK_WIDTH / 4) + 16, MALLOC_CAP_DMA);
_dmaI2SDesc    = (lldesc_s *)heap_caps_malloc(sizeof(lldesc_t), MALLOC_CAP_DMA);
```

**[SRC]** same file, lines 131–132. So the design is: **framebuffers in PSRAM, one row at a time copied into an internal-RAM DMA buffer.** If the framebuffers were in SRAM there would be no SRAM left for the DMA buffer, the Wi-Fi stack, or the TLS session the whole product exists to make. §7.4 explains why the copy is necessary rather than DMA-ing straight out of PSRAM.

---

## 7. PSRAM in software — what actually changes

### 7.1 It is not automatic. You must turn it on.

| Framework | What to do |
|---|---|
| **ESP-IDF** | `idf.py menuconfig` → *Component config → ESP PSRAM* → `CONFIG_SPIRAM=y`, then *SPI RAM config* → **Mode: Quad**, **Type: auto-detect** (or `ESP_PSRAM_TYPE_64MBIT`), **Speed: 40 MHz** (see §7.3) |
| **Arduino-ESP32** | Board menu **PSRAM: Enabled** (`-DBOARD_HAS_PSRAM`). Selecting the wrong board target is the usual cause of `ps_malloc()` returning `NULL` |
| **PlatformIO** | `board_build.arduino.memory_type = qio_qspi` and `build_flags = -DBOARD_HAS_PSRAM` |
| **MicroPython** | Built into the board firmware; the Inkplate port ships PSRAM enabled **[SRC]** |

**If PSRAM is not enabled, `ps_malloc()` silently falls back to internal RAM or returns `NULL`.** The Inkplate driver checks — `initializeFramebuffers()` returns 0 if any allocation fails — and the visible symptom is a display that never initialises. **[SRC]**

Two IDF options change behaviour dramatically and are worth knowing by name:

- **`CONFIG_SPIRAM_USE_MALLOC`** — makes plain `malloc()` able to return PSRAM once internal RAM is under `CONFIG_SPIRAM_MALLOC_ALWAYSINTERNAL`. Convenient, and the source of confusing failures when a DMA-bound buffer silently lands in PSRAM.
- **`CONFIG_SPIRAM_MEMTEST`** — the boot-time PSRAM test. Leave it on during bring-up; it is how you find a bad solder joint on the module.

### 7.2 The 4 MB mapping window and `himem`

> *"External SRAM can be mapped into CPU data memory space. **Up to 4 MB can be mapped at a time.** 8-bit, 16-bit and 32-bit reads and writes are supported."*
> — **[DOC]** ESP32-WROVER Datasheet v2.7 §3.2

The module carries **8 MB** of PSRAM but the ESP32's data cache window is **4 MB**. So:

- With a stock IDF configuration you get **4 MB of directly-addressable PSRAM** and the other 4 MB is invisible.
- The remaining bank is reachable only through the **`himem` API** (`CONFIG_SPIRAM_BANKSWITCH_ENABLE`, `esp_himem_alloc()` / `esp_himem_map()`), which works by **bank-switching 32 KB pages** into a reserved region of the 4 MB window. Every bank-switch reservation *reduces* the flat 4 MB accordingly (`CONFIG_SPIRAM_BANKSWITCH_RESERVE`, default 8 banks = 256 KB).
- `himem` memory is **not** in the heap. It is not `malloc`-able, it is not pointer-addressable without an explicit map call, and the map/unmap costs real cycles.

**[INF] Practical guidance:** treat a WROVER as a **4 MB PSRAM part** unless you have a specific, chunked, streaming workload (video frames, audio buffers) that suits bank switching. The Inkplate needs 900 KB and never goes near `himem`; the Inkplate library contains no `esp_himem` references at all **[SRC]**.

### 7.3 Clock speed: 40 MHz is the safe answer

The PSRAM is specified to 80 MHz **[DOC]** WROVER-E DS Table 18. Running it there is a documented option but couples it to the flash clock and, on some board layouts, is the difference between reliable and intermittent. **[INF]** 40 MHz costs you bandwidth you almost certainly do not need on an e-paper device, whose refresh is measured in hundreds of milliseconds. Start at 40 MHz; raise it only with a measured reason.

### 7.4 The errata that actually matter for PSRAM on this part

The full ESP32 errata treatment lives in [guides/espressif/errata-practical.md](../../../guides/espressif/errata-practical.md); the revision matrix is in [esp32-u4wdh §21](../esp32-u4wdh/README.md#21-silicon-revisions-the-complete-matrix-and-what-v31-means). The PSRAM-relevant summary:

| Issue | Affects | What to do |
|---|---|---|
| **The "PSRAM cache issue"** — certain instruction sequences that touch external RAM return wrong data on **rev 1** silicon | Original WROVER (`D0WDQ6` rev 1) and **WROVER-B** (`D0WD` rev 1) | IDF `CONFIG_SPIRAM_CACHE_WORKAROUND=y`, which compiles the whole app with `-mfix-esp32-psram-cache-issue`. **Costs code size and speed.** Fixed in silicon on rev 3, i.e. on the WROVER-E. **[INF]** — this is the single strongest reason to specify a -E |
| `WDT-3.15` **dual-core cache lock-up** — interrupt-watchdog panics on a dual-core ESP32 running from external flash/PSRAM, and it is *worse* on v3.x | **WROVER-E** | Enable `CONFIG_ESP32_ECO3_CACHE_LOCK_FIX`. See [errata-practical §`WDT-3.15`](../../../guides/espressif/errata-practical.md) |
| Task stacks may not live in PSRAM by default | all | `xTaskCreate` stacks come from internal RAM. `CONFIG_SPIRAM_ALLOW_STACK_EXTERNAL_MEMORY` exists but interacts badly with the cache workaround. **[INF]** leave it off |
| **DMA cannot read most peripheral buffers out of PSRAM** on the ESP32 | all | Allocate every DMA buffer with `MALLOC_CAP_DMA` (= internal). This is exactly what the Inkplate driver does with `_dmaLineBuffer` **[SRC]** |
| Interrupt handlers with `ESP_INTR_FLAG_IRAM` must not touch PSRAM | all | Any cache miss inside a no-flash ISR is a crash |

---

## 8. Module versus bare chip: the certification argument

This is the part that decides real products, and it is usually under-explained.

An ESP32-WROVER-E is a **pre-certified intentional radiator**. Espressif has already obtained, and pays to maintain:

| Regime | What Espressif holds |
|---|---|
| **FCC (US)** | Modular approval per part. The sibling WROOM-32U grant is `FCC ID 2AC7Z-ESP32WROOM32U`, "Single Modular Approval", Equipment Class DTS, 15C, 2402–2480 MHz **[DOC]** `../esp32-wroom-32u/artifacts/esp32-wroom-32u-fcc-wifi-bt40-certificate.pdf` |
| **CE / RED (EU)** | EU type-examination certificate (Module B) issued by a Notified Body — Kiwa Nederland B.V., NB 0063, per Directive 2014/53/EU **[DOC]** `../esp32-wroom-32u/artifacts/esp32-wroom-32u-ce-certification.pdf` |
| **Bluetooth (BQB)** | Bluetooth SIG qualification. Declaration ID **D051055**, listed 2020-07-06, **explicitly covering ESP32-WROVER-E and ESP32-WROVER-IE** (and WROOM-32E/32UE) **[DOC]** `artifacts/esp32-wrover-e-ie-wroom-32e-32ue-bqb-certification.pdf` |
| Environmental | REACH / RoHS **[DOC]** |
| Reliability | HTOL / HTSL / uHAST / TCT / ESD **[DOC]** |

**What you inherit and what you do not:**

- ✅ You may build the module into your product and reference Espressif's FCC ID, rather than paying for full intentional-radiator testing yourself. This typically saves **five figures** and several weeks.
- ✅ The Bluetooth SIG qualification means you can reference an existing Qualified Design rather than qualifying a controller subsystem.
- ⚠ **The grant is conditional.** The WROOM-32U grant text is explicit: *"Single Modular Approval… This grant is valid only when the module is sold to OEM integrators and must be installed by the OEM or OEM integrators… must be installed to provide a separation distance of at least 20 cm from all persons and must not be collocated or operating in conjunction with any other antenna or transmitter"* **[DOC]**.
- ⚠ **You still need product-level testing.** Unintentional-radiator (FCC Part 15B), EMC, and safety obligations remain yours. Modular approval covers the radio, not your board.
- ❌ **A bare ESP32-D0WD-V3 gives you none of this.** You would own the crystal, the balun, the π-match, the antenna, the layout, and the entire certification campaign.

The Inkplate 5's own compliance folder — `Inkplate 5 CE.pdf`, `Inkplate 5 UKCA.pdf` in the hardware repository — is short precisely because the radio is a certified module.

**[INF] The general rule:** use a module unless you are shipping >100 k units/year, in which case the ~$1–2 module premium starts to outweigh a one-time certification campaign. Below that, the module wins on cost, on schedule and on risk. This is discussed generically in [guides/espressif/ecosystem-and-product-lines.md §8](../../../guides/espressif/ecosystem-and-product-lines.md).

---

## 9. Exact role and wiring on these boards

### 9.1 Soldered Inkplate 5 (`U10`) and Inkplate 5 Gen 2 (`U11`)

**[SCH]** `MCU.kicad_sch`, both design repositories.

| Function | Pins | Notes |
|---|---|---|
| **E-paper 8-bit parallel data** | `IO4 IO5 IO18 IO19 IO23 IO25 IO26 IO27` → `EPD_D0`…`EPD_D7` | Driven by **I2S1 in parallel/DMA mode** — the ESP32 has no LCD peripheral |
| **E-paper timing** | `IO32` → `EPD_CKV`, `IO33` → `EPD_SPH`, `IO2` → `EPD_LE` | The three fast lines. The slow lines (`OE`, `GMOD`, `SPV`, `WAKEUP`, `PWRUP`, `VCOM`) live on the [PCAL6416A](../../nxp/pcal6416a/README.md) |
| **I²C0** | `IO21` = `SDA`, `IO22` = `SCL` | Three devices: `0x20` PCAL6416A, `0x48` [TPS65186](../../texas-instruments/tps65186/README.md), `0x51` [PCF85063A](../../nxp/pcf85063a/README.md) |
| **microSD (SPI)** | `IO14` SCK, `IO12` MISO, `IO13` MOSI, `IO15` CS | ⚠ `IO12` is MTDI (§5.3); `IO15` is MTDO |
| **UART0** | `IO3` RXD0, `IO1` TXD0 | Through `R24`/`R23` 1 kΩ to the [CH340C](../../wch/ch340c/README.md) |
| **Battery sense** | `IO35` (input-only) | ADC1 |
| **RTC alarm** | `IO39` / `SENSOR_VN` (input-only) | From `PCF85063A` `INT` **through solder jumper `JP2`** — §3.1 |
| **Wake / user button** | `IO36` / `SENSOR_VP` (input-only) | `SW3` via `R41` |
| **Reset** | `EN` ← `TPS3840PL27` supervisor `RESET` | Shared with the PCAL6416A's `nRESET` — see the [CH340C record §5](../../wch/ch340c/README.md) for the auto-reset path |
| **Boot** | `IO0` | `Q3` auto-reset transistor; `Q1`/`R19` MOSFET path is **DNP** |

Header pads `K22`, `K32`–`K36` break out `V_BAT`, `SPI_SCK`, `SPI_MISO`, `SPI_MOSI`, `GPIO_39`, `GPIO_36` for user expansion **[SCH]**.

### 9.2 ZeroWriter Ink (`U11` on the respun display board)

Electrically the same module in the same role — the ZeroWriter Inkplate 5 Gen2 board reuses Soldered's `MCU.kicad_sch` almost verbatim, with the designator shifted and the expander renumbered to `U10` **[SCH]**. What differs on that board is the charger, the connectors and the USB path, none of which touch the WROVER. See [ZeroWriter Ink](../../../devices/zerowriter/zerowriter-ink/README.md).

The product's *other* ESP32 is on the keyboard PCB and is an [ESP32-WROOM-32U](../esp32-wroom-32u/README.md) — a different module with different pins available. §2.3.

---

## 10. Pitfalls, ranked

1. **Using GPIO16 or GPIO17.** They are not brought out. Your code will compile, `gpio_set_level()` will return `ESP_OK`, and nothing will happen. §2.
2. **Copying a WROOM pinout.** The two modules are the *same footprint* with different pin functions at 27/28. A WROOM design that uses those pins fails silently when re-stuffed with a WROVER.
3. **Forgetting to enable PSRAM in the build.** `ps_malloc()` returns `NULL`, the Inkplate driver's `initializeFramebuffers()` returns 0, and the display stays blank with no error printed. §7.1.
4. **Expecting 8 MB of flat heap.** You get 4 MB mapped; the rest needs `himem`. §7.2.
5. **Sizing the supply for the average current.** 350 mA peaks; Espressif specifies ≥ 0.5 A capability. Symptom is brownout resets during Wi-Fi association only. §4.1.
6. **Mixing up the 1.8 V and 3.3 V variants.** Pin-compatible, oppositely-strapped. §5.
7. **Putting anything on GPIO12.** It is MTDI. Even a scope probe at reset can flip the strap. §5.3.
8. **DMA-ing out of PSRAM.** Use `MALLOC_CAP_DMA`. §7.4.
9. **Assuming rev 1 and rev 3 behave the same under PSRAM load.** The cache-issue workaround is mandatory on rev 1 and free on rev 3. §7.4.
10. **Not soldering the EPAD.** Pin 39 is the RF and thermal ground. A module reflowed with a lifted pad will enumerate, run, and have terrible RF performance that reads as "bad Wi-Fi range".
11. **Placing the module's antenna over copper.** The PCB-antenna variants have a keepout zone specified in the datasheet's land-pattern chapter; the u.FL variants do not need one. **[DOC]**

---

## 11. Alternatives and equivalents

| Part | Drop-in for a WROVER footprint? | Comment |
|---|---|---|
| **ESP32-WROVER-E-N4R8** | ✅ **The answer** | Current, rev 3 silicon, 3.3 V memory, PCB antenna |
| **ESP32-WROVER-IE-N4R8** | ✅ mechanically | u.FL instead of PCB antenna. Needs an antenna and revisits certification (§8, and [WROOM-32U §6](../esp32-wroom-32u/README.md)) |
| ESP32-WROVER-E-N8R8 / -N16R8 | ✅ | More flash, same everything else. Cheap upgrade if you want OTA headroom |
| ESP32-WROVER-B / -IB | ✅ | NRND, rev 1 silicon ⇒ PSRAM cache workaround mandatory. Avoid for new work |
| ESP32-WROVER (original) | ⚠ mechanically yes | NRND, **1.8 V memory**, MTDI pulled high internally. Different boot strap semantics. §5.1 |
| **ESP32-WROOM-32E** | ⚠ same footprint outline, **but 18 × 25.5 mm and no PSRAM** | Will not fit a 31.4 mm land pattern's keepout and cannot run the Inkplate driver. §6 |
| ESP32-WROOM-32E-N4R2 | ❌ for this purpose | Does have 2 MB in-package PSRAM — but 2 MB, and a different body length |
| **ESP32-S3-WROOM-1-N16R8** | ❌ not a drop-in | Different pinout, different core (LX7), **has a real LCD peripheral and native USB**. The correct part for a *new* e-paper design; Soldered used exactly this for the Inkplate 13 SPECTRA **[SRC]**. See [ESP32-S3R8](../esp32-s3r8/README.md) |
| Bare ESP32-D0WD-V3 + external PSRAM | ❌ | You inherit the crystal, the balun, the antenna, and the entire certification campaign. §8 |

---

## 12. Open questions

| Question | Status |
|---|---|
| Exact WROVER suffix on Inkplate 5 / Gen 2 production units | **Narrowed, not closed.** §1.3 rules out the -I/-IB/-IE and every `R2` SKU, and argues against the original WROVER. **-E vs -B remains open** and needs `esptool flash_id` or a look at the can |
| Is `EFUSE_SDIO_FORCE`/`EFUSE_SDIO_TIEH` pre-burnt on -B/-E modules? | **Open.** Datasheets describe the override but do not state factory programming. `espefuse.py summary` answers it |
| Does the `R45` pull-up on GPIO12 ever flip MTDI after `esp_restart()` with the SD rail live? | **Open, [INF] hazard only.** Divider maths suggests no; unverified on hardware. §5.3 |
| Original ESP32-WROVER-I body height (3.5 mm?) | **Open.** The v2.7 datasheet's dimensions chapter is a figure; the text-layer extraction did not resolve it |
| Which flash vendor die Espressif fits | **Not published**, and not stable. Espressif states only the electrical envelope (WROVER-E DS Table 17) |

---

## Manufacturer

**Espressif Systems** — see the [Espressif documentation-sourcing guide](../../../vendors/espressif/README.md) for this vendor's document portals, URL patterns, module part-numbering conventions and known gotchas.

## Used By

| Device | Designator | Role |
|---|---|---|
| [Soldered Inkplate 5](../../../devices/soldered-electronics/inkplate-5/README.md) | `U10` | Main processor. I²C0 on `IO21`/`IO22`; battery ADC on `IO35`; RTC interrupt on `IO39` **via solder jumper `JP2` — [§3.1](#31-gpio39-is-on-a-solder-jumper-and-it-is-not-hard-wired-to-the-rtc)** |
| [Soldered Inkplate 5 Gen 2](../../../devices/soldered-electronics/inkplate-5-gen2/README.md) | `U11` | Main processor, same bus assignment |
| [ZeroWriter Ink](../../../devices/zerowriter/zerowriter-ink/README.md) | `U11` | Main processor on the respun display board — **one of two ESP32s in the product**; the keyboard carries an [ESP32-WROOM-32U](../esp32-wroom-32u/README.md) |

## Related pages

- [espressif/esp32-wroom-32u](../esp32-wroom-32u/README.md) — the second ESP32 in ZeroWriter Ink, and the direct GPIO16/17 counter-example (§2.3)
- [espressif/esp32-u4wdh §21](../esp32-u4wdh/README.md#21-silicon-revisions-the-complete-matrix-and-what-v31-means) — deep ESP32 silicon-revision coverage. **Not duplicated here**
- [guides/espressif/soc-peripheral-reference.md](../../../guides/espressif/soc-peripheral-reference.md) — peripheral counts and GPIO accounting
- [guides/espressif/memory-and-boot.md §5](../../../guides/espressif/memory-and-boot.md#5-flash-and-psram-voltage--the-part-that-destroys-hardware) — flash/PSRAM voltage constraints and the 1.8 V damage risk
- [guides/espressif/errata-practical.md](../../../guides/espressif/errata-practical.md) — the errata that bite, by revision
- [guides/espressif/ecosystem-and-product-lines.md §7.1](../../../guides/espressif/ecosystem-and-product-lines.md#71-classic-esp32--the-authoritative-decode) — the part-number decode
- [e-ink/ed052tc4](../../e-ink/ed052tc4/README.md) — the panel whose framebuffers force the PSRAM requirement
- [nxp/pcal6416a](../../nxp/pcal6416a/README.md) · [nxp/pcf85063a](../../nxp/pcf85063a/README.md) · [texas-instruments/tps65186](../../texas-instruments/tps65186/README.md) — the three I²C peripherals it owns, at `0x20`, `0x51` and `0x48`
- [wch/ch340c](../../wch/ch340c/README.md) — the USB-UART bridge it is programmed through, because this part has no native USB

---

## 13. Local artifacts and sources

### Artifacts held

| File | Document | Version | Bytes | sha256 |
|---|---|---|---:|---|
| `artifacts/esp32-wrover-e-wrover-ie-datasheet.pdf` | ESP32-WROVER-E & ESP32-WROVER-IE Datasheet | **v2.4** | 1,425,347 | `611e8506f352225e9ab09b4c2c3286885022b2f77a44ee8f0ab88a6302616f32` |
| `artifacts/esp32-wrover-b-datasheet.pdf` | ESP32-WROVER-B & ESP32-WROVER-IB Datasheet (**NRND**) | **v2.3** | 982,614 | `4c7a79bf1de750c941101cca54a0f5750bed8409eae31c769ff08970bd7439e3` |
| `artifacts/esp32-wrover-datasheet-v2.7-nrnd-wayback.pdf` | ESP32-WROVER Datasheet (**NRND**, original 1.8 V variant) — **added 2026-08-24** | **v2.7** | 470,491 | `a0dc0b6173afcf7bc145ace8e0862f36d4d32266f78c3112c73906a5a3fbea42` |
| `artifacts/esp32-wrover-e-ie-wroom-32e-32ue-bqb-certification.pdf` | Bluetooth SIG qualification, Declaration ID D051055 | — | 340,138 | `9eb00fd2a31cf15ac70eb7ed4e31b0a536e1c6cc1dbeaea70e4b381f7d629031` |

Also present in this directory as of 2026-08-24 are byte-identical re-downloads made during this pass under longer names (`esp32-wrover-e_esp32-wrover-ie-datasheet-v2.4.pdf`, `esp32-wrover-b_esp32-wrover-ib-datasheet-v2.3-nrnd.pdf`). **They duplicate the two files above and carry no new information** — verified by sha256. Prefer the short names.

Chip-level documents (ESP32 datasheet, TRM, errata, hardware design guidelines) are **not** duplicated here; they live in
[`../esp32-u4wdh/artifacts/`](../esp32-u4wdh/README.md#112-local-artifacts).

#### Reacquire

```sh
# Current documents — legacy static path, redirects to documentation.espressif.com
curl -sSL -o esp32-wrover-e-wrover-ie-datasheet.pdf \
  https://www.espressif.com/sites/default/files/documentation/esp32-wrover-e_esp32-wrover-ie_datasheet_en.pdf
curl -sSL -o esp32-wrover-b-datasheet.pdf \
  https://www.espressif.com/sites/default/files/documentation/esp32-wrover-b_datasheet_en.pdf

# ⚠ The ORIGINAL WROVER datasheet has been withdrawn — the legacy URL now returns
#   HTTP 200 with the 13,745-byte soft-404 SPA shell. Wayback is the only route:
curl -sSL -o esp32-wrover-datasheet-v2.7-nrnd-wayback.pdf \
  'http://web.archive.org/web/20251015143618if_/https://www.espressif.com/sites/default/files/documentation/esp32-wrover_datasheet_en.pdf'

# Always validate:
head -c 4 *.pdf | od -An -c        # expect  %  P  D  F
```

### Retrieval failures, 2026-08-24

Recorded in full in [`component-download-failures.txt`](../../../component-download-failures.txt). Summary:

| URL | Result |
|---|---|
| `…/documentation/esp32-wrover_datasheet_en.pdf` | **HTTP 200, `text/html`, 13,745 B**, final URL `documentation.espressif.com/404`. Soft-404. Recovered from Wayback (snapshot `20251015143618`) |
| `…/documentation/esp32-wrover-i_datasheet_en.pdf` | Same soft-404. **No Wayback snapshot.** The WROVER-I appears never to have had a standalone datasheet — it is covered inside the ESP32-WROVER document |
| `…/esp32-wrover_esp32-wrover-i_datasheet_en.pdf`, `esp32_wrover_datasheet_en.pdf`, `esp32-wrover-b_esp32-wrover-ib_datasheet_en.pdf`, `esp32-wrover-ib_datasheet_en.pdf`, `esp32-wrover-ie_datasheet_en.pdf` | All soft-404 (13,745 B HTML). The `-IB`/`-IE` variants share their siblings' documents |

### Design files read

| File | Used for |
|---|---|
| `devices/soldered-electronics/inkplate-5/artifacts/hardware/soldered-inkplate-5-hardware-design/CAD/V1.2.0/MCU.kicad_sch` | `U10` symbol pin list (§2.2), every net in §3 |
| `…/CAD/V1.2.0/SD & RTC.kicad_sch` | `R45` pull-up on `SPI_MISO`/GPIO12, `Q10` microSD power switch (§5.3) |
| `…/CAD/V1.2.0/CTRL & COMS.kicad_sch` | `R23`/`R24` UART series resistors, reset/boot path |
| `…/CAD/V1.2.0/Soldered Inkplate 5.kicad_pcb` | **Authoritative net cross-check.** Used to resolve `GPIO_39`/`JP2`/RTC (§3.1), which the schematic sheets leave as dangling labels, and to confirm that `U10` pads 17–22 are formally `unconnected-(U10-PadNN)` |
| `…/OUTPUTS/V1.2.0/Soldered Inkplate 5 BOM.csv` | `U10 = ESP32-WROVER`, package `ESP32-WROVER` (line 57); `C55` DNP; resistor values |
| `devices/zerowriter/…/design/src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/MCU.kicad_sch` | `U11` symbol pin list — same 36 pins |
| `devices/zerowriter/…/design/src/Zerowriter Keyboard/v1.2.0/CAD/Zerowriter Keyboard.kicad_sch` | The WROOM-32U counter-example: `IO16`/`IO17` on `Col 8`/`Col 9` (§2.3) |

### Source files read

| File | Used for |
|---|---|
| `Inkplate-Arduino-library/src/boards/Inkplate5V2/Inkplate5V2Driver.cpp` L131–132, L862–866 | DMA buffer capability flags; the four `ps_malloc` framebuffers (§6) |
| `Inkplate-Arduino-library/src/boards/Inkplate5/Inkplate5Driver.cpp` L921–925 | Same, 960 × 540 |
| `Inkplate-Arduino-library/src/boards/Inkplate5/waveforms.h`, `…/Inkplate5V2/waveforms.h` | `E_INK_WIDTH` / `E_INK_HEIGHT` |
| `Inkplate-Arduino-library/src/graphics/Image/Image.cpp`, `…/ImageColor/ImageColor.cpp` | `MALLOC_CAP_SPIRAM` dither/pixel buffers — additional PSRAM consumers beyond the framebuffers |
| `devices/soldered-electronics/inkplate-5/artifacts/docs/Inkplate-documentation/source/hardware-reference.rst` L26 | Soldered's "4MB Flash, 8MB PSRAM, PCB antenna" claim (§1.3) |

### Authoritative sources

| Title | URL | Retrieved | Version | Local artifact |
|---|---|---:|---|---|
| ESP32-WROVER-E & ESP32-WROVER-IE Datasheet | https://www.espressif.com/sites/default/files/documentation/esp32-wrover-e_esp32-wrover-ie_datasheet_en.pdf | 2026-08-24 | v2.4 | `artifacts/esp32-wrover-e-wrover-ie-datasheet.pdf` |
| ESP32-WROVER-B & ESP32-WROVER-IB Datasheet (NRND) | https://www.espressif.com/sites/default/files/documentation/esp32-wrover-b_datasheet_en.pdf | 2026-08-24 | v2.3 | `artifacts/esp32-wrover-b-datasheet.pdf` |
| ESP32-WROVER Datasheet (NRND) — via Wayback | http://web.archive.org/web/20251015143618if_/https://www.espressif.com/sites/default/files/documentation/esp32-wrover_datasheet_en.pdf | 2026-08-24 | v2.7 | `artifacts/esp32-wrover-datasheet-v2.7-nrnd-wayback.pdf` |
| Bluetooth SIG Qualification, Declaration ID D051055 (WROVER-E/IE, WROOM-32E/32UE) | *(obtained 2026-08-26 by a prior pass; Bluetooth SIG listing)* | 2026-08-26 | — | `artifacts/esp32-wrover-e-ie-wroom-32e-32ue-bqb-certification.pdf` |
| FCC Grant 2AC7Z-ESP32WROOM32U (cited in §8 for grant conditions) | *(TCB grant, Telefication B.V., 2018-01-22)* | 2026-08-26 | — | `../esp32-wroom-32u/artifacts/esp32-wroom-32u-fcc-wifi-bt40-certificate.pdf` |
| Kiwa EU type-examination certificate 172141367/AA/02 (RED Module B) | *(Kiwa Nederland B.V., NB 0063, issued 2023-03-02)* | 2026-08-26 | — | `../esp32-wroom-32u/artifacts/esp32-wroom-32u-ce-certification.pdf` |
| ESP-IDF PSRAM / himem API documentation | https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/himem.html | 2026-08-24 | latest | – |
| Soldered Inkplate hardware design (KiCad, TAPR OHL) | https://github.com/SolderedElectronics/Soldered-Inkplate-5-hardware-design | 2026-08-24 | V1.2.0 | `devices/soldered-electronics/inkplate-5/artifacts/hardware/` |

> **Evidence boundary.** Every electrical figure in §4 and every pin assignment in §2/§3 is **[DOC]** from the datasheets above or **[SCH]** from net extraction over the KiCad sources. §1.3's variant conclusion is **[INF]** and is explicitly not closed. §5.3's boot hazard is **[INF]** reasoning from schematic plus documented strapping semantics and has **not** been reproduced on hardware. §7's ESP-IDF option names are **[WEB]** from ESP-IDF documentation and were not exercised against a build in this pass.
