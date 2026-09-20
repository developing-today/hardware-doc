# DinMeter — pinouts and buses

Applies to **both** K134 (v1.0) and K134-V11 (v1.1). The two boards share a byte-identical
published schematic (SHA-256 `03ec3353…`) and an identical vendor PinMap; see
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) §3.

**Evidence markers** as in [`README.md`](README.md#evidence-labelling).

---

## 1. How this table was derived

The schematic is an Altium PDF publication. Altium emits an invisible marker layer —
`CO<designator>`, `PI<designator><pin>`, `NL<netname>` — at every component outline, pin
instance and net label. Those markers were extracted with a glyph-position parse
([`artifacts/schematic/parse_dinmeter_sch.py`](artifacts/schematic/parse_dinmeter_sch.py),
`executed-success`), deduplicated (Altium draws the marker layer twice; without dedup the text
interleaves as `PPIIJJ110011` instead of `PIJ10101`), and each `M1` pad was matched to the
visible pin-name and net-label text on its own row.

**Text-layer validation.** Before transcribing any value, the extracted text was checked against
known headings visible in the document: the sheet-frame zone letters `A`/`B`/`C`/`D` and numbers
`1`–`4` appear at the expected page-frame coordinates, `TP4057`, `SY7088`, `BL8075CB5TR33`,
`ME3116AM6G`, `STAMP-S3-SMD`, `RTC8563` and `32.768KHz ±20ppm 12.5pF` all render as legible
strings in the right places, and the marker bodies decode to designators that match the visible
designator text 84 times out of 85. The text layer is sound. **[SCH]**

**Completeness.** 85 `CO` bodies (one of which is a truncated bare `M`, i.e. `M1`), 238 `PI`
markers, 25 `NL` markers, 553 visible text runs. All 31 `M1` pads were recovered. A back-of-
envelope pin count for 84 parts is ~260, so roughly 20 `PI` markers were **not** recovered —
Altium glues some markers to adjacent text in a way the negative-lookbehind rule (needed to stop
`GPIO0` parsing as a `PI` marker) discards. Every `M1`, `J3`, `J4`, `J5`, `FPC1`, `U5` and `U6`
pad *was* recovered, so no table below rests on a missing marker.

---

## 2. `M1` — Stamp-S3 module, all 31 pads

Read directly from the `PIM10xx` pin markers with their row-matched pin names and net labels.
**[SCH]** Cross-checked against the vendor PinMap **[DOC]** and against
`M5Unified/src/M5Unified.cpp` **[SRC]**; agreements and the one disagreement are noted.

| `M1` pad | Stamp pin name | ESP32-S3 GPIO | Board net | Function | Direction | Cross-check |
|---:|---|---|---|---|---|---|
| 1 | `G1` | GPIO1 | `GI` | **PORT.B** signal 1 | I/O | **[SRC]** `M5Unified.cpp:159` port-B p1 |
| 2 | `G2` | GPIO2 | `GO` | **PORT.B** signal 2 | I/O | **[SRC]** `:159` port-B p2 |
| 3 | `G3` | GPIO3 | `beep` | **Buzzer** drive → `Q5` base via `R25` 470 Ω | O | **[SRC]** `:2921-2928` `spk_cfg.pin_data_out = GPIO_NUM_3` |
| 4 | `G4` | GPIO4 | `LCD_RS` | Display D/C | O | **[DOC]** `RS`; **[SRC]** `dc_gpio_num: 4` |
| 5 | `G5` | GPIO5 | `LCD_MOSI` | Display SPI MOSI | O | **[SRC]** `mosi_io_num: 5` |
| 6 | `G6` | GPIO6 | `LCD_SCK` | Display SPI SCLK | O | **[SRC]** `sclk_io_num: 6` |
| 7 | `G7` | GPIO7 | `LCD_CS` | Display chip select | O | **[SRC]** `cs_gpio_num: 7` |
| 8 | `G8` | GPIO8 | `LCD_RESET` | Display reset, active-low | O | **[SRC]** `reset_gpio_num: 8` |
| 9 | `G9` | GPIO9 | `LCD_BL` | Backlight enable → `U6` AW35122FDR | O | **[SRC]** `ledc_backlight gpio_num: 9` |
| 10 | `G10` | GPIO10 | `BATADC` | Battery voltage sense, `R7`/`R8` 1 MΩ divider | AI | **[SCH]** |
| 11 | `GND` | — | `GND` | Ground | P | **[SCH]** |
| 12 | `G11` | GPIO11 | `IN_SDA` | **Internal I²C SDA** (RTC) | I/O | **[SRC]** `:96` In SDA |
| 13 | `5V` | — | `+5VIN` | Module 5 V supply in | P | **[SCH]** |
| 14 | `G12` | GPIO12 | `IN_SCL` | **Internal I²C SCL** (RTC) | I/O | **[SRC]** `:96` In SCL |
| 15 | `G13` | GPIO13 | `SDA` | **PORT.A** — see §5 | I/O | **[SRC]** `:96` EX SDA |
| 16 | `G14` | GPIO14 | `G14` | Power-latch OR network (`D7` 1N4148WT + `R9` 10 kΩ) | I/O | **[SCH]** |
| 17 | `G15` | GPIO15 | `SCL` | **PORT.A** — see §5 | I/O | **[SRC]** `:96` EX SCL |
| 18 | `GND` | — | `GND` | Ground | P | **[SCH]** |
| 19 | `G39/MTCK` | GPIO39 | `G39` | Power-latch OR network (`D6`?/`R10` 10 kΩ) — see §4 | I/O | **[SCH]** |
| 20 | `G0/Boot` | GPIO0 | — | Boot strap; **the button is on the Stamp**, not the carrier | I | **[DOC]**; **[SRC]** `:3504` BtnB |
| 21 | `G40/MTDO` | GPIO40 | `IN_B` | **Encoder channel B**, `R3` 10 kΩ pull-up | I | **[SRC]** `M5DinMeter.h:9` `DIAL_ENCODER_PIN_B 40` |
| 22 | `EN` | — | — | Module reset, driven by `S4` RST | I | **[SCH]** |
| 23 | `G41/MTDI` | GPIO41 | `IN_A` | **Encoder channel A**, `R2` 10 kΩ pull-up | I | **[SRC]** `M5DinMeter.h:8` `DIAL_ENCODER_PIN_A 41` |
| 24 | `G44/Rx` | GPIO44 | *(none)* | **Free — no net label on the sheet** | — | **[SCH]** |
| 25 | `G42/MTMS` | GPIO42 | `WAKE` | **Encoder push-button / wake key**, `R1` 10 kΩ pull-up, `C1` 100 nF | I | **[SRC]** `:3502-3505` `!gpio_in(GPIO_NUM_42)` = BtnA |
| 26 | `G43/Tx` | GPIO43 | *(none)* | **Free — no net label on the sheet** | — | **[SCH]** |
| 27 | `G46` | GPIO46 | `HOLD` | **Power latch, active-high** → `Q4` LN2324DT2AG | O | **[SRC]** `:282` POWER_HOLD `GPIO_NUM_46`; **[DOC]** |
| 28 | `3V3` | — | `3V3` | Module 3.3 V (from `U4` BL8075) | P | **[SCH]** |
| 29 | *(GND)* | — | `GND` | Ground pad | P | **[SCH]** rotated pin number |
| 30 | *(GND)* | — | `GND` | Ground pad | P | **[SCH]** |
| 31 | *(GND)* | — | `GND` | Ground pad | P | **[SCH]** |

> **Pads 29–31.** Their pin numbers are drawn rotated, so the glyphs extract stacked (`9`+`2`,
> `0`+`3`, `1`+`3`) and read bottom-up as 29 / 30 / 31. All three sit on `GND`. This is a
> reading of rotated text, not an inference: the three pad markers `PIM1029`, `PIM1030`,
> `PIM1031` are present at the corresponding coordinates. **[SCH]**

> **Pads 24 and 26 (GPIO43/GPIO44, the UART0 pins) carry no net label.** That is a *blank cell*,
> not a drawn no-connect marker, so it is "unknown but almost certainly unused" rather than a
> designer's positive assertion. Treat them as probably-free but verify with a meter before
> relying on them. **[SCH]** **[INF]**

---

## 3. Bus summary

| Bus | Signals | GPIO | Peripheral | Address / mode | Evidence |
|---|---|---|---|---|---|
| **Internal I²C** | SCL / SDA | 12 / 11 | `U5` BM8563 RTC | 7-bit **0x51** (`0xA2` write / `0xA3` read) | **[SRC]** `M5Unified.cpp:96`, `esp-board-manager` `board_peripherals.yaml`; **[DOC]** BM8563 datasheet |
| **External I²C (PORT.A)** | SCL / SDA | **15 / 13** per M5Unified | user Grove units | 100/400 kHz | **[SRC]** `M5Unified.cpp:96` |
| **Display SPI** | SCLK / MOSI / CS / DC / RST | 6 / 5 / 7 / 4 / 8 | `FPC1` → ST7789V2 | `SPI2_HOST`, mode 0, ≤ 40 MHz, **write-only (no MISO)** | **[SRC]** `esp-board-manager` `spi_display`; **[DOC]** |
| **Backlight PWM** | `LCD_BL` | 9 | `U6` AW35122FDR → panel LED | LEDC ch 0, timer 0, 5 kHz, 10-bit | **[SRC]** `esp-board-manager` `ledc_backlight` |
| **Buzzer PWM** | `beep` | 3 | `Q5` SS8050 → `LS1` | LEDC ch 1, timer 1, ~4 kHz; M5Unified uses `magnification 48`, `buzzer = true` | **[SRC]** `M5Unified.cpp:2921-2928` |
| **Quadrature encoder** | A / B | 41 / 40 | rotary encoder on `J5` | PCNT 2-channel, `max_glitch_ns 1000`, ±1000 limits | **[SRC]** `esp-board-manager` `pcnt_encoder` |
| **PORT.B GPIO** | sig1 / sig2 | 1 / 2 | user | plain GPIO / ADC / PWM | **[SRC]** `M5Unified.cpp:159` |
| **USB** | D+ / D− | 19 / 20 | native USB-OTG / Serial-JTAG, USB-C **on the Stamp module** | — | **[SCH]** Stamp `U1` pins 25/26 |

---

## 4. Power tree and the latch

| Designator | Part | Role | Key passives | Evidence |
|---|---|---|---|---|
| `J1` | 2-pin 2.54 mm screw terminal (`DB2EK-2.54-2P-GN-S`, Ningbo Dibo, green) | **6–36 V DC input** | — | **[SCH]** **[DOC]** |
| `D13`, `D12`, `D11`, `D9` | B5819W / SD36 Schottky | input protection / clamp | — | **[SCH]** |
| `U1` | **ME3116AM6G** | wide-input buck → `+5VIN` | `L1` 10 µH (3015), `C24` 10 µF/35 V, FB `R5` 56 kΩ / `R6` 10 kΩ | **[SCH]** |
| `U7` | **CN809J** | reset supervisor on `+5VIN` | — | **[SCH]** |
| `J2` | 1.25 mm 2-pin JST-style (`1.25WT-2P`) | Li-ion battery | — | **[SCH]** **[DOC]** |
| `U2` | **TP4057** | linear Li-ion charger, 4.24 V float | `R13` 3.3 kΩ (PROG), `D1`/`D2`/`D3` status LEDs | **[SCH]** |
| `Q3`, `Q6` | **AP40P05** P-channel MOSFET | battery power path (`VBAT_IN` → `VBAT_OUT`) | `R14`/`R15` 100 kΩ | **[SCH]** |
| `Q4` | **LN2324DT2AG** | `HOLD` (GPIO46) gate for the latch | `R23` 100 kΩ | **[SCH]** |
| `U3` | **SY7088** | boost `VBAT_OUT` → `+5VOUT` | `L4` 1.5 µH, FB `R16` 52.3 kΩ / `R18` 15 kΩ, `C18`/`C19` 22 µF | **[SCH]** |
| `U4` | **BL8075CB5TR33** | 3.3 V LDO → `+3.3V` | `C30` 22 µF, `C31` 100 nF | **[SCH]** |
| `S1` | `SW-PB` "WAKE" | wake button symbol — **no marker layer, see §6** | `R1` 10 kΩ | **[SCH]** |
| `S4` | `SW-PB` "RST" | module reset | — | **[SCH]** |
| `R7`, `R8` | 1 MΩ each | `BATADC` divider → GPIO10 | — | **[SCH]** |

The vendor prints `Vout = 1.2 V × (R1/R2 + 1)` beside `U3`. With `R16` = 52.3 kΩ and `R18` =
15 kΩ that gives **1.2 × (52.3/15 + 1) ≈ 5.38 V** on `+5VOUT` — the Grove rail. **[SCH]** plus
arithmetic; the vendor states the rail as "5 V" **[DOC]**. If you are powering something
voltage-sensitive from a Grove port, measure it.

**Latch behaviour, from the vendor Learn section** **[DOC]**:

- *Power on (battery only):* press **WAKE**, or let the RTC `INT` fire. Firmware must then set
  `HOLD` (GPIO46) high **during initialisation**, or the board falls back asleep.
- *Power off (no USB):* press **RST**, or set GPIO46 low in software.

`G14` (pad 16) and `G39` (pad 19) each sit on a 10 kΩ + 1N4148WT network tied into this
circuit. Their exact role — most plausibly a diode-OR of wake sources into the latch — was
**not fully traced** in this pass and is recorded as a gap. **[SCH]** **[INF]**

---

## 5. Grove ports — and the colour conflict

Schematic pin order, read from `PIJ30x` / `PIJ40x`: **[SCH]**

| Connector | pin 1 | pin 2 | pin 3 | pin 4 |
|---|---|---|---|---|
| `J3` `HY-2.0_IIC` (**PORT.A**) | `IIC_SCL` → `M1`.17 = **GPIO15** | `IIC_SDA` → `M1`.15 = **GPIO13** | `VCC` = `+5VOUT` | `GND` |
| `J4` `HY-2.0_IO` (**PORT.B**) | `GI` → `M1`.1 = **GPIO1** | `GO` → `M1`.2 = **GPIO2** | `VCC` = `+5VOUT` | `GND` |

Pull-ups `R2`, `R3` = 10 kΩ on PORT.A. Load limit 5 V @ 220 mA per port. **[DOC]**

> ### ⚠ Conflict: which wire is which
>
> The vendor PinMap renders PORT.A as `Black=GND, Red=5V, Yellow=G13, White=G15` and PORT.B as
> `Black=GND, Red=5V, Yellow=G2, White=G1`. **[DOC]**
>
> Under the Grove convention (connector pin 1 = yellow = SCL, pin 2 = white = SDA) the schematic
> says the opposite: **yellow = GPIO15 = SCL, white = GPIO13 = SDA**, and PORT.B yellow = GPIO1.
> M5Unified agrees with the schematic reading — `EX SCL = GPIO_NUM_15, EX SDA = GPIO_NUM_13`
> **[SRC]** `M5Unified.cpp:96` — and its port-B table lists GPIO1 first under the comment
> `p1 close to 5V`. **[SRC]** `:157-160`
>
> **This is unresolved.** It does not affect anyone using M5Unified or UiFlow2, which drive the
> correct pins either way. It affects only hand-wiring to bare Grove leads. Full analysis,
> including the M5Dial cross-check (same table, same ambiguity) and what would settle it, is in
> [`gaps-and-conflicts.md`](gaps-and-conflicts.md) §1.

---

## 6. Reference-designator census, and three that do not resolve

A **complete** census was taken rather than a search for expected parts, so that gaps are
themselves evidence. Full listing:
[`artifacts/schematic/K134_DIN_Meter_v1.0-designator-census.txt`](artifacts/schematic/K134_DIN_Meter_v1.0-designator-census.txt).

**84 designators carry a `CO` component-outline marker:**
C1–C8, C10, C15–C19, C21, C24–C33 · D1–D13 · FPC1 · J1–J5 · L1, L4 · LS1 · M1 · Q1, Q3–Q6 ·
R1–R19, R23–R25 · S4 · U1–U7 · Y2.

**Three designators appear as visible text with no `CO` and no `PI` marker anywhere in the
document** (searched in both single and double-struck glyph forms; zero hits):

| Text | Position | Adjacent text | Assessment |
|---|---|---|---|
| `S1` | (246.7, 242.9) | `SW-PB` 16.8 units below — the same designator/part spacing `S4` uses | A drawn WAKE push-button whose marker layer was not emitted or not recovered. **Not** asserted as DNP |
| `R20` | (249.3, 276.9) | `10 kΩ` below, sitting on the RTC `INT` net | Almost certainly a real 10 kΩ pull-up on `INT` |
| `Y1` | (163.8, 495.0) | immediately right of `SS8050` on the same baseline, under `COQ5`/`Q5` | **Probably not a designator.** `Y1` is the SOT-23 marking code for an SS8050 NPN; this reads as M5Stack annotating the marking |

Whether these are extraction losses or genuine absences is **not established**. Roughly 20 `PI`
markers are missing overall for the same reason, so an extraction loss is the more likely
explanation for `S1` and `R20`. Recorded in [`gaps-and-conflicts.md`](gaps-and-conflicts.md) §2.

`Q2`, `L2`, `L3`, `R21`, `R22`, `S2`, `S3`, `C9`, `C11`–`C14`, `C20`, `C22`, `C23`, `U8`+ have
**no marker and no visible text** — they are simply unused numbers in the designator sequence.

---

## 7. What is *not* on this board

Enumerated so the absence is a positive statement rather than an oversight:

- **No PSRAM** — no designator, and `ESP32-S3FN8` has none in package. **[SCH]** **[DOC]**
- **No SD card** — no SDMMC connector designator.
- **No USB-UART bridge** — USB is the SoC's own OTG/Serial-JTAG, on the Stamp. **[DOC]**
- **No microphone, speaker or codec** — the only audio device is the magnetic buzzer `LS1`.
- **No touch controller** — the LCD is display-only; the knob is the input.
- **No accelerometer/IMU, no environmental sensor.**
- **No RGB LED on the carrier** — the WS2812B-2020 is *inside* the Stamp module on GPIO21.
  **[SCH]** `Sch_M5StampS3_v0.2` `U3`.

---

## Related

- [`resources-and-conflicts.md`](resources-and-conflicts.md) — what collides with what
- [`components/m5stack/stamp-s3/README.md`](../../../components/m5stack/stamp-s3/README.md) — the module's own pinout
- [`components/m5stack/stamp-s3a/README.md`](../../../components/m5stack/stamp-s3a/README.md) — and what changed in v1.1

---

# 2026-09-07 — additions and corrections from schematic net tracing

Appended beneath the existing tables; **nothing above is altered, reworded or reordered.** Full
trace with coordinates: [`schematic-netlist.md`](schematic-netlist.md). Method:
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md).
Corrections indexed in
[`scratch/schematic-tracing/corrections-requiring-review.md`](../../../scratch/schematic-tracing/corrections-requiring-review.md).

Applies to **v1.0 and v1.1** alike: the two schematic PDFs extract to the same 873 words and the
same 26 `NL` tokens.

## ⚠ Correction — `J5` (rotary encoder) has **five** pins, not seven

`python3 trace.py grep <bbox> '^PIJ5'` returns `PIJ501`…`PIJ505` and nothing further; a 300 dpi
render confirms five pins. Any statement elsewhere that `J5` is a 7-pad connector is superseded.

| Pin | Symbol name | Token | Net | GPIO |
|---|---|---|---|---|
| 1 | `b1` | `PIJ501` @ 445.50, 361.91 | `BTN` → `WAKE` | **GPIO42** (`G42/MTMS`, pad 25) |
| 2 | `b2` | `PIJ502` @ 503.00, 361.91 | `GND` | — |
| 3 | `A` | `PIJ503` @ 459.50, 389.77 | `IN_A` | **GPIO41** (`G41/MTDI`, pad 23) |
| 4 | `COM` | `PIJ504` @ 474.50, 389.77 | `GND` | — |
| 5 | `B` | `PIJ505` @ 488.50, 389.77 | `IN_B` | **GPIO40** (`G40/MTDO`, pad 21) |

A single 5-terminal part: 3-terminal quadrature encoder with COM grounded, plus an integrated
push switch. `R2`/`R3` 10 kΩ pull-ups to `+3.3V`; `C2`/`C3` 100 nF to `GND`.

> **Resource conflict not previously recorded:** GPIO41 is `MTDI` and GPIO40 is `MTDO`. **The
> encoder occupies two of the four JTAG pins**; an external JTAG probe and the encoder cannot be
> used at the same time. GPIO41 is *not* a strapping pin on the ESP32-S3 (straps are 0, 3, 45,
> 46), so the pull-up is safe — checked, not assumed.
>
> **Input bandwidth ceiling:** 10 kΩ external ∥ ~45 kΩ internal (the driver also enables
> `INPUT_PULLUP`) ≈ 8.2 kΩ, with 100 nF ⇒ τ ≈ 0.82 ms, corner ≈ **194 Hz**. Firmware cannot
> exceed this.

## ⚠ The Grove 5 V rail is designed to **5.38 V**, and the arithmetic is the vendor's own

`U3` is an **`SY7088`** boost (value @ 586, 215.2). The sheet prints its formula at (605, 236.7):

```
Vout = 1.2V * (R1/R2 + 1)
```

with `R16` **52.3 kΩ** (@ 663–668, 179.0) over `R18` **15 kΩ** (@ 663–666, 207.7):

```
Vout = 1.2 x (52.3 / 15 + 1) = 1.2 x 4.4867 = 5.384 V
```

**This is not an extraction error and not a mistake to be corrected — it is what the sheet
specifies.** The same idiom appears on the Cardputer ADV, whose SY7088 divider (`R4` 75 kΩ /
`R6` 22 kΩ) gives 5.29 V. Two M5Stack boards, two deliberately-high 5 V rails.

**Practical consequence:** a Grove peripheral on this port sees ≈ 5.4 V. Anything specified as
5 V ± 5 % (4.75–5.25 V) is **outside its rated input range on this port.** USB's own upper limit
is 5.25 V. Check before blaming the peripheral.

## Buzzer drive — `C27` is a series coupling capacitor

All five drive-path tokens share y = 491.37, in x order:
`R25.1`(45) → `R25.2`(67) → `C27.1`(74) → `C27.2`(89) → `Q5.base`(121).

```
beep (G3) ── R25 470Ω ── C27 10µF ──┬── Q5 base (SS8050 NPN, low-side)
                                    └── D7 1N4148WT (cathode up) ── GND
LS1 (Buzzer) between +5VIN and Q5 collector, with D6 1N4148WT anti-parallel across it
```

⚠ `C27` is **in series with the base**, not local bulk decoupling. High-pass corner ≈ 34 Hz. The
transducer therefore **cannot be driven with a DC level** — it needs a waveform. `D6`'s presence
as a flyback catch diode confirms the load is inductive (magnetic), not piezo.

## Module footprint `M1` — complete pad map

Left column, pads 1–17:

| Pad | Pin name | Net | | Pad | Pin name | Net |
|---|---|---|---|---|---|---|
| 1 | `G1` | `GI` | | 10 | `G10` | `BATADC` |
| 2 | `G2` | `GO` | | 11 | `GND` | `GND` |
| 3 | `G3` | **`beep`** | | 12 | `G11` | `IN_SDA` |
| 4 | `G4` | `LCD_RS` | | 13 | `5V` | `+5VIN` |
| 5 | `G5` | `LCD_MOSI` | | 14 | `G12` | `IN_SCL` |
| 6 | `G6` | `LCD_SCK` | | 15 | `G13` | `SDA` |
| 7 | `G7` | `LCD_CS` | | 16 | `G14` | `G14` |
| 8 | `G8` | `LCD_RESET` | | 17 | `G15` | `SCL` |
| 9 | `G9` | `LCD_BL` | | | | |

Right column, pads 18–28:

| Pad | Pin name | Net | | Pad | Pin name | Net |
|---|---|---|---|---|---|---|
| 18 | `GND` | `GND` | | 24 | `G44/Rx` | — |
| 19 | `G39/MTCK` | `G39` | | 25 | `G42/MTMS` | **`WAKE`** |
| 20 | `G0/Boot` | — | | 26 | `G43/Tx` | — |
| 21 | `G40/MTDO` | **`IN_B`** | | 27 | `G46` | `HOLD` |
| 22 | `EN` | — | | 28 | `3V3` | `3V3` |
| 23 | `G41/MTDI` | **`IN_A`** | | | | |

**Two I²C buses, clearly separated by the sheet:** `IN_SDA`/`IN_SCL` on `G11`/`G12` (internal, to
`U5` `RTC8563`) and `SDA`/`SCL` on `G13`/`G15` (external Grove, to `J4`).

## Named parts recovered

`U1` `ME3116AM6G` buck · `U2` `TP4057` charger · `U3` `SY7088` Grove boost ·
`U4` `BL8075CB5TR33` 3.3 V regulator · `U5` `RTC8563` · `U6` load switch on the Grove rail ·
`U7` `CN809J` reset supervisor · `Q3`/`Q6` `AP40P05` P-FET · `Q4` `LN2324DT2AG` ·
`Q5` `SS8050` · `D1`/`D9`/`D11` `B5819W SL` · `D2`–`D5`,`D10` `B5819WT` · `D8` `SS34` ·
`D12` `SD36` · `Y2` 32.768 kHz ±20 ppm 12.5 pF with `C28`/`C29` 6.0 pF · `FPC1` `FPC-0.5-8P` ·
`J1` `Header 2` `6V~36V` · `J3`/`J4` `HY-2.0_IIC`.

> `Y1` next to `Q5` is the **SOT-23 top mark of the SS8050**, not a crystal — this confirms the
> existing note in § 6 above.
