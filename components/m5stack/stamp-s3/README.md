# M5Stack Stamp-S3

- **Category:** ESP32-S3 **core module** — a castellated/SMD minimum-system board carrying an
  Espressif ESP32-S3FN8, its own 5 V→3.3 V converter, USB-C, an RGB LED, a user button and a
  3D chip antenna, breaking out 23 GPIOs.
- **SKU:** **`S007`** (base SMD module). Header variants: `S007-PIN127` (1.27 mm), `S007-PIN254`
  (2.54 mm).
- **Scope of this record:** **module level.** ESP32-S3 silicon architecture, register map, boot
  ROM, radio and errata belong to the SoC and are documented at
  [`components/espressif/esp32-s3r8/`](../../espressif/esp32-s3r8/README.md) — with the caveat
  that this module fits the **FN8** variant (8 MB in-package flash, **no PSRAM**), not the R8.
- **Successor:** [**Stamp-S3A**](../stamp-s3a/README.md), SKU `S007-V033`. Read that record
  before assuming a design that works with one works with the other.
- **Retrieved:** 2026-09-04

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[SCH]** | Read from `Sch_M5StampS3_v0.2.pdf` by parsing the Altium `CO`/`PI`/`NL` marker layer, cited by designator | `executed-success` extraction, `not-tested` electrically |
| **[DOC]** | <https://docs.m5stack.com/en/core/StampS3>, retrieved 2026-09-04 | `not-tested` |
| **[SRC]** | Vendor/framework source at a cited `file:line` | `executed-success` read |
| **[INF]** | Inference, reasoning given | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Marketed name | **Stamp-S3** (also written *M5StampS3*, *StampS3*) | **[DOC]** |
| SKU | `S007` | **[DOC]** page header |
| Documentation | <https://docs.m5stack.com/en/core/StampS3> (HTTP 200) | **[DOC]** |
| Published schematic | `Sch_M5StampS3_v0.2.pdf` — **board revision v0.2** | **[SCH]** filename + `artifacts/` |
| SoC | **ESP32-S3FN8** — Xtensa LX7 dual-core @ 240 MHz, **8 MB in-package flash, no PSRAM** | **[DOC]**; **[SCH]** `U1` symbol `ESP32-S3FN8` |
| DC-DC | **MUN3CAD01-SC** µPOL module (`M2`) | **[DOC]**; **[SCH]** `M2` value text |
| RGB LED | **WS2812B-2020** ×1 (`U3`), data on **GPIO21** | **[DOC]**; **[SCH]** `U1`.27 → `SK_DIN` |
| User button | ×1 (`S1`) on **GPIO0** | **[DOC]**; **[SCH]** |
| Antenna | `ANT1` = **PROANT440** ceramic/chip antenna, "2.4 G 3D antenna" | **[SCH]** value text; **[DOC]** |
| Broken-out IO | **23**: G0, G1–G15, G39–G44, G46 | **[DOC]** |
| IO pitch | 2.54 mm **and** 1.27 mm; SMT / DIP / fly-wire | **[DOC]** |
| Rear LCD FPC | 0.5 mm, **12-pin (`J1`) or 8-pin (`J3`)**, connector `HDGC/0.5K-HX-8PWB/NC` | **[DOC]**; **[SCH]** |
| Size / weight | **24.0 × 18.0 × 4.7 mm** / 3.0 g | **[DOC]** |
| Operating temp | 0 – 40 °C | **[DOC]** |
| Input | 5 V (`VIN_5V` or USB-C) | **[DOC]** |

### Power consumption (vendor-measured, method not published)

| Mode | Supply | Current | Evidence |
|---|---|---|---|
| Sleep | USB Type-C | **400.67 µA** | **[DOC]** |
| Sleep | `VIN_5V` | **310.89 µA** | **[DOC]** |
| Standby | USB Type-C | **33.04 mA** | **[DOC]** |
| Standby | `VIN_5V` | **33.56 mA** | **[DOC]** |

These are the numbers the Stamp-S3A improves on by roughly 4.5× (sleep, USB) and 45× (sleep,
`VIN_5V`). See [Stamp-S3A § Power](../stamp-s3a/README.md#5-power-the-headline-change).

---

## 2. Internal architecture (from the v0.2 schematic)

`Sch_M5StampS3_v0.2.pdf`, one sheet, **54 designators with `CO` markers** plus `C26` recovered
from visible text only (55 total). Full parsed layout:
[`artifacts/Sch_M5StampS3_v0.2.plaintext-layout.txt`](artifacts/Sch_M5StampS3_v0.2.plaintext-layout.txt).

| Designator | Part / value | Role | Evidence |
|---|---|---|---|
| `U1` | **ESP32-S3FN8** | SoC, 57 pads on the symbol | **[SCH]** |
| `M2` | **MUN3CAD01-SC** | 5 V → 3.3 V µPOL module, 6 pins (EN, GND, VIN, GND, FB, VOUT) | **[SCH]** |
| `R6` / `R17` | 100 kΩ / 22.1 kΩ | `M2` feedback divider | **[SCH]** |
| `C21`, `C22` | 10 µF/10 V ×2 | `M2` in/out bulk | **[SCH]** |
| `U2` | **SGM2578** (second value text `WS4622C-4/TR`) | **Load switch** — VIN=`VDD_3V3`, EN=`DISP_BL`, VOUT→ LCD-FPC backlight rail | **[SCH]** |
| `U3` | **WS2812** (WS2812B-2020) | RGB LED. **`VDD` = `VDD_3V3`, always powered** | **[SCH]** |
| `ANT1` | **PROANT440** | 2.4 GHz antenna | **[SCH]** |
| `L1` 2.2 nH, `C1` 2.2 pF, `C2` 2.0 pF | — | antenna π-match (3 elements) | **[SCH]** |
| `X1` + `L3` 10 nH, `C9` 10 pF | — | 40 MHz crystal network | **[SCH]** |
| `J2` | USB Type-C receptacle | `A6/B6` = D+, `DP1/DP2`, `VCC` | **[SCH]** |
| `R1`, `R2` | 5.1 kΩ/1 % ×2 | USB-C CC pull-downs | **[SCH]** |
| `F1`, `D14`, `JP3` (`Type-A`) | — | USB protection / ESD | **[SCH]** |
| `S1` | tactile `BTN-USER` | GPIO0 boot/user button | **[SCH]** |
| `D6` | 1N4148WT | on `ESP_EN` | **[SCH]** |
| `R7` 10 kΩ, `R16` 100 kΩ, `C23` 1 µF | — | `ESP_EN` RC / pull-up | **[SCH]** |
| `R3` | 10 kΩ/1 % | on GPIO2 | **[SCH]** |
| `R4` 10 kΩ, `R5` | — | strapping / GPIO42-41 network | **[SCH]** |
| `M1` | header/edge symbol | module pin field, `GPIO1`… | **[SCH]** |
| `J1` | 12-pin 0.5 mm FPC | rear LCD option A | **[SCH]** |
| `J3` | 8-pin 0.5 mm FPC (`HDGC/0.5K-HX-8PWB/NC`) | rear LCD option B | **[SCH]** |
| `JP1`, `JP2`, `JP4`, `PHD1`, `L5`, `D1`–`D4`, `C3`–`C14`, `C17` | — | jumpers, mounting, decoupling | **[SCH]** |

### Internal-only GPIOs — the ones that are not on the 23-pin list

| ESP32-S3 GPIO | `U1` pad | Net | Goes to | Evidence |
|---|---|---|---|---|
| **GPIO21** | 27 | `SK_DIN` | `U3` WS2812B-2020 data in | **[SCH]** |
| **GPIO33** | 38 | `DISP_RST` | FPC `J1`/`J3` | **[SCH]** |
| **GPIO34** | 39 | `DISP_RS` | FPC | **[SCH]** |
| **GPIO35** | 40 | `DISP_MOSI` | FPC | **[SCH]** |
| **GPIO36** | 41 | `DISP_SCK` | FPC | **[SCH]** |
| **GPIO37** | 42 | `DISP_CS` | FPC | **[SCH]** |
| **GPIO38** | 43 | `DISP_BL` | `U2` load-switch **EN** | **[SCH]** |

GPIO33–38 are the pins an ESP32-S3**R8**/**R16V** would spend on octal PSRAM. Because the module
fits the **FN8** (no PSRAM), M5Stack was free to route them to the rear display header. That is
the design decision that makes the whole Stamp-S3 family work. **[SCH]** **[INF]**

### Rear LCD FPC pin order (v0.2)

| `J1` (12P) pin | Net | | `J3` (8P) pin | Net |
|---:|---|---|---:|---|
| 1 | `VIN_5V` | | 1 | GPIO2 / `VIN`/`VOUT` node |
| 2 | GPIO18 | | 2 | GPIO3 |
| 3 | GPIO17 | | 3 | `DISP_RST` |
| 4 | GPIO16 | | 4 | `DISP_RS` |
| 5 | (GPIO2 node) | | 5 | `DISP_MOSI` |
| 6 | GPIO3 | | 6 | `DISP_SCK` |
| 7 | `DISP_RST` | | 7 | `VDD_3V3` |
| 8 | `DISP_RS` | | 8 | `DISP_CS` |
| 9 | `DISP_MOSI` | | | |
| 10 | `DISP_SCK` | | | |
| 11 | `VDD_3V3` | | | |
| 12 | `DISP_CS` | | | |

**[SCH]** — from `PIJ10x` / `PIJ30x` markers. **The Stamp-S3A numbers these connectors in the
opposite direction for the same net order**; see
[Stamp-S3A § FPC numbering](../stamp-s3a/README.md#6-the-fpc-numbering-question).

---

## 3. Boot, strapping and download mode

- **Download mode:** hold the `G0` button on the module while applying power, release after.
  **[DOC]**
- **GPIO46 is pulled down by default** on this module. **[DOC]** ("Additional Notes"). GPIO46 is
  an ESP32-S3 strapping pin: pulling it high before boot prevents the chip starting.
- **GPIO0** is pulled up by default and is the boot strap.
- Consequence for carriers: a board that uses **GPIO46 as an output power latch** — which the
  [DinMeter](../../../devices/m5stack/dinmeter/README.md) does — is relying on the pin being low
  at reset and only driven high by firmware afterwards. That is safe by construction here, but
  it is the reason you must never fit an external pull-up on GPIO46.

---

## 4. Software support

| Framework | Identifier | Evidence |
|---|---|---|
| Arduino / M5Unified | `board_t::board_M5StampS3` | **[SRC]** `M5Unified/src/M5Unified.cpp:93, 242, 2392, 3484` |
| M5Unified button | BtnA = `!gpio_in(GPIO_NUM_0)`, `use_rawstate_bits = 0b00001` | **[SRC]** `M5Unified.cpp:3484-3490` |
| M5Unified RGB LED | `_pin_table_other0` → `GPIO_NUM_21` | **[SRC]** `M5Unified.cpp:242` |
| M5Unified external I²C | EX SCL `GPIO_NUM_15`, EX SDA `GPIO_NUM_13`; **no internal I²C** (255/255) | **[SRC]** `M5Unified.cpp:93` |
| Example | `m5stack/STAMP-S3` → `examples/Led/Led.ino` | **[DOC]** link |
| ESP-IDF | plain `esp32s3` target, no special board package required | **[DOC]** |
| UiFlow2 | supported | **[DOC]** |

---

## 5. Mechanical and footprints

M5Stack publishes KiCad support in `m5stack/M5_Hardware` (HEAD `a240115c94b19ecf647f229c47fa9a8ce46ccdc4`,
2026-08-17):

| File | Local artifact | SHA-256 (16) |
|---|---|---|
| `KiCad/Footprints/M5Stack.pretty/Stamp-S3-SMD.kicad_mod` | [`artifacts/Stamp-S3-SMD.kicad_mod`](artifacts/Stamp-S3-SMD.kicad_mod) | `2435abbd80d39803` |
| `KiCad/Footprints/M5Stack.pretty/Stamp-S3-DIP.kicad_mod` | [`artifacts/Stamp-S3-DIP.kicad_mod`](artifacts/Stamp-S3-DIP.kicad_mod) | `1e1a32ffa34603d5` |
| `Products/S007_Stamp-S3/Structures/Stamp-S3.stl` | [`artifacts/Stamp-S3.stl`](artifacts/Stamp-S3.stl) | `f72c1af2d42930fc` |
| `KiCad/3D/M5Stack.3dshapes/Stamp-S3.step` | **archived** → [`artifacts/Stamp-S3.step.ARCHIVED.md`](artifacts/Stamp-S3.step.ARCHIVED.md) | `7f29337cdac90c80` |

`Stamp-S3-SMD.kicad_mod` is the footprint the DinMeter's `M1` uses.

> **There is no `Stamp-S3A` footprint and no `Stamp-S3A.step`** in the library at that commit,
> and `Stamp-S3A.stl` is byte-identical to `Stamp-S3.stl`. See the
> [placeholder](artifacts/Stamp-S3.step.ARCHIVED.md#important-there-is-no-stamp-s3astep) and the
> [Stamp-S3A record](../stamp-s3a/README.md#7-mechanical).

---

## 6. Artifacts

| File | Size | SHA-256 (16) | What it is | Licence | Redistribution | Disposition |
|---|---:|---|---|---|---|---|
| [`artifacts/Sch_M5StampS3_v0.2.pdf`](artifacts/Sch_M5StampS3_v0.2.pdf) | 348 884 | `6d92e1aef6577838` | **Primary evidence.** Altium-published schematic, board rev v0.2 | unknown | unknown | repository |
| [`artifacts/Sch_M5StampS3_v0.2.plaintext-layout.txt`](artifacts/Sch_M5StampS3_v0.2.plaintext-layout.txt) | 7 646 | `7139bba1dc9404cd` | derived: sheet text as positioned rows | derived work of ↑ | — | repository |
| [`artifacts/Stamp-S3-SMD.kicad_mod`](artifacts/Stamp-S3-SMD.kicad_mod) | 364 492 | `2435abbd80d39803` | KiCad SMD footprint | unknown (`M5_Hardware` has no `LICENSE`) | unknown | repository |
| [`artifacts/Stamp-S3-DIP.kicad_mod`](artifacts/Stamp-S3-DIP.kicad_mod) | 365 014 | `1e1a32ffa34603d5` | KiCad DIP footprint | unknown | unknown | repository |
| [`artifacts/Stamp-S3.stl`](artifacts/Stamp-S3.stl) | 158 484 | `f72c1af2d42930fc` | mechanical model | unknown | unknown | repository |
| [`artifacts/S007_PinMap_01.jpg`](artifacts/S007_PinMap_01.jpg) | 631 459 | `37249f2574a8702c` | official pin-map diagram | unknown | unknown | repository |
| `artifacts/Stamp-S3.step` | 2 904 597 | `7f29337cdac90c80` | STEP model — **archived**, [placeholder](artifacts/Stamp-S3.step.ARCHIVED.md) | unknown | unknown | archive |

Sources for each are in [`../../../devices/m5stack/dinmeter/sources.md`](../../../devices/m5stack/dinmeter/sources.md).

### Datasheets that belong to other components

- **ESP32-S3 datasheet** — M5Stack mirrors it at
  `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/472/esp32-s3_datasheet_en.pdf`. That file is
  **byte-identical** (SHA-256 `b6db403d6d5db8d1b4db0c8390ff7e0a7db714b8388e986e1c64bff563f76b61`)
  to `components/espressif/esp32-s3r8/artifacts/esp32-s3-datasheet-v2.0-m5stack-mirror.pdf`
  already held in this repository. **Not duplicated**; the extra URL is recorded here and in the
  device source table.
- **MUN3CAD01-SC datasheet** → [`components/murata/mun3cad01-sc/`](../../murata/mun3cad01-sc/README.md)
- **SGM2578 load switch** → [`components/sgmicro/sgm2578/`](../../sgmicro/sgm2578/README.md)

---

## 7. Caveats and unsafe assumptions

- **`FN8`, not `R8`.** There is **no PSRAM**. Enabling PSRAM in a build will fail or silently
  degrade. The repo's `esp32-s3r8` record describes different silicon options; read it for the
  core, not for memory.
- **GPIO33–38 are not yours.** They are wired to the rear FPC header and the RGB LED inside the
  module. A carrier board cannot use them.
- **Do not pull GPIO46 up.** Strapping pin, pulled down by design.
- **`ANT1 = PROANT440` is read from the schematic value text, not from a chip marking.** No
  teardown photograph was inspected. **[SCH]** **[INF]**
- **The 33 mA standby figure is the vendor's, with no stated method** (clock, radio state,
  peripherals). Do not use it for a battery-life calculation without measuring.

---

## Used By

### M5Stack DinMeter (SKU K134)

Fitted as **`M1`**, `STAMP-S3-SMD` footprint, 31 pads. The carrier supplies 5 V on pad 13
(`+5VIN`) and takes 3.3 V back on pad 28. All 23 module IOs are broken out to the carrier; the
DinMeter uses 20 of them and leaves GPIO43/GPIO44 (UART0) unlabelled and GPIO0 to the module's
own button.

The module's **internal** GPIO21 RGB LED and GPIO38 backlight switch are *not* wired to anything
on the DinMeter carrier — the DinMeter drives its own panel backlight from GPIO9 through its own
`U6` AW35122FDR. So on this board the Stamp's RGB LED is simply an always-lit status LED on
GPIO21, with no enable step required.

Full wiring: [`devices/m5stack/dinmeter/pinouts-and-buses.md`](../../../devices/m5stack/dinmeter/pinouts-and-buses.md) §2.

### M5Stack DinMeter v1.1 (SKU K134-V11) — *not* this module

v1.1 fits the [Stamp-S3A](../stamp-s3a/README.md) instead. That substitution is the entire
content of the revision; see
[`devices/m5stack/dinmeter-v1.1/README.md`](../../../devices/m5stack/dinmeter-v1.1/README.md).

### Devices carrying this module

| Device | Record |
|---|---|
| **Cardputer v1.0** (`K132`) | [`devices/m5stack/cardputer-v1.0`](../../../devices/m5stack/cardputer-v1.0/README.md) |
| Cardputer Accessory Kit (original) | sold as a spare: StampS3 + display |

The Cardputer v1.0 is **the only Cardputer whose RGB LED is independent of the LCD backlight**,
because this module feeds the WS2812 from the always-on `VDD_3V3`. The Stamp-S3A moved it to the
switched `BL_3V3` rail, buying sleep current (0.26 µA → 0.15 µA) at the cost of that
independence.

*Added 2026-09-07 from `scratch/m5stack-cardputer/index-fragments.md` §3.10.*
