# Puya PY32L020F15U6

> **32-bit Arm Cortex-M0+ low-power microcontroller** — up to 48 MHz, 24 KB flash, 3 KB SRAM, 1.7–5.5 V, 18 GPIOs, 12-bit ADC, two comparators, SPI/I²C/USART, in a 3 × 3 mm QFN20.
> Research snapshot **2026-09-01**. This is the silicon that M5Stack's schematic identifies as underlying **both** of its custom coprocessors on the [PaperMono](../../../devices/m5stack/papermono/README.md) — the **[M5PM1](../../m5stack/m5pm1/README.md)** power controller and the **[M5IOE1](../../m5stack/m5ioe1/README.md)** I/O expander.

> **This record describes the generic Puya part only.** Everything M5Stack's chips do — register maps, I²C addresses, rail control, PWM behaviour, NeoPixel RAM — is **firmware**, and is documented in the two records linked above. Do not read the PY32L020 datasheet expecting to find `M5PM1_REG_PWM0_L`; it is not silicon.

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Puya `PY32L020 Datasheet` **V2.0**, 2025-05-20, English — local copy `artifacts/py32l020-datasheet-en-v2.0-m5stack-mirror.pdf` | `not-tested` — vendor document reproduced |
| **[SCH]** | `PaperMono_SCH_V0.6.2_20260522.pdf`, sheet + designator | `executed-success` for the extraction; `not-tested` electrically |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **`PY32L020F15U6`** | **[SCH]** sheet 1; **[DS]** Table 1-1 |
| Manufacturer | **Puya Semiconductor (Shanghai) Co., Ltd.** (普冉半导体) | **[DS]** cover |
| Family | PY32L020 series — the **L = Low Power** branch of Puya's PY32 32-bit MCU line | **[DS]** §7 |
| Core | **Arm Cortex-M0+**, 32-bit | **[DS]** cover |
| Datasheet | **V2.0**, released **2025-05-20**, 51 pp | **[DS]** §8 |
| Datasheet history | V1.0 2023-11-28 (initial) → V1.1 2024-03-08 (adds SOP16, SOP8) → **V2.0 2025-05-20 (major version)** | **[DS]** §8 |

### 1.1 Decoding the ordering code **[DS §7]**

```
PY   32    L      020      F1    5     U    6    [xxx]
│    │     │      │        │     │     │    │     └── Options: TR = tape/reel, TU = tube,
│    │     │      │        │     │     │    │                  blank = tray, xxx = programmed-part code
│    │     │      │        │     │     │    └──────── Temperature: 6 = −40…+85 °C
│    │     │      │        │     │     │                          7 = −40…+105 °C
│    │     │      │        │     │     └───────────── Package: U = QFN, P = TSSOP,
│    │     │      │        │     │                             S = SOP,  D = DFN
│    │     │      │        │     └─────────────────── User code memory size: 5 = 24 KB
│    │     │      │        └───────────────────────── Pin count / pinout:
│    │     │      │                                     F1 = 20 pins, Pinout1
│    │     │      │                                     W1 = 16 pins, Pinout1
│    │     │      │                                     L1 =  8 pins, Pinout1
│    │     │      └────────────────────────────────── Sub-family: 020 = PY32L020xx
│    │     └───────────────────────────────────────── Product type: L = Low Power
│    └─────────────────────────────────────────────── Product family: 32-bit MCU
└──────────────────────────────────────────────────── Company
```

**`PY32L020F15U6` = 20-pin Pinout1, 24 KB flash, QFN package, −40 to +85 °C.**

---

## 2. Memory, and why this section exists

| Resource | **PY32L020F15U6** | Evidence |
|---|---|---|
| **Flash** | **24 KB** | **[DS]** Table 1-1, column `PY32L020F15U6` |
| **SRAM** | **3 KB** | **[DS]** Table 1-1 |

These two numbers were the specific thing this research pass was asked not to guess, and they are **read directly out of Puya's own device table** — `Table 1-1 PY32L020x6 series product features and peripheral counts`, which lists `PY32L020F15U6` and `PY32L020L15D6` side by side, both at 24 KB flash / 3 KB SRAM. The ordering-code field `5 = 24 KB` (§1.1) corroborates it independently within the same document.

The family's headline "Up to 24 KB Flash / up to 3 KB SRAM" on the datasheet cover is therefore not a range across variants — every published PY32L020 part has the same memory. **[DS]** Tables 1-1 and 1-2.

**Why this matters for the M5Stack chips:** 24 KB of flash is the entire budget for M5Stack's power-management or I/O-expander firmware, including its I²C slave stack, its register file and its bootloader if it has one. That is a real constraint on what those chips can plausibly do, and it bounds any speculation about hidden capability. **[INF]**

---

## 3. Full feature set **[DS Features]**

### Core and clocking

| Item | Value |
|---|---|
| Core | Arm 32-bit Cortex-M0+ |
| Max frequency | **48 MHz** |
| High-speed internal RC (HSI) | **24 / 48 MHz**, configurable, "high precision" |
| Low-speed internal RC (LSI) | **32.768 kHz** |
| Low-speed external crystal (LSE) | 32.768 kHz supported |
| External clock input | Supported |

### Power

| Item | Value |
|---|---|
| **Operating voltage** | **1.7 – 5.5 V** |
| Low-power modes | **Sleep / Stop / Deep_stop** |
| Reset sources | Power-on / power-down reset (POR/PDR), **brown-out reset (BOR)** — BOR threshold selectable by option byte |
| Operating temperature | −40 to +85 °C (`6`) or −40 to +105 °C (`7`) |

The 1.7–5.5 V range is the notable one: it means the part can be run directly from a Li-ion cell without a regulator, which is exactly what a power-management coprocessor needs. **[INF]**

### Peripherals — `PY32L020F15U6` counts **[DS Table 1-1]**

| Peripheral | Count / detail |
|---|---|
| **GPIO** | **18**, all usable as external interrupts |
| **ADC** | 1 × **12-bit**, **8 external + 2 internal** channels. Reference options: embedded **1.5 V / 2.048 V / 2.5 V** or `VCC` |
| **Comparators** | **2** |
| Advanced-control timer | 1 × 16-bit (`TIM1`) |
| General-purpose timer | 1 × 16-bit (`TIM14`) |
| Low-power timer | 1 × `LPTIM` — **can wake from Stop mode** |
| Independent watchdog | 1 × `IWDG` |
| SysTick | 1 |
| **SPI** | 1 |
| **I²C** | 1 — Standard (100 kHz) and Fast (400 kHz) modes, 7-bit addressing |
| **USART** | 1, with **automatic baud-rate detection** |
| CRC | Hardware **CRC-32** module |
| Unique ID | Yes |
| Debug | **SWD** (serial wire debug) |

### Packages **[DS Features, §6]**

QFN20, TSSOP20, SOP16, SOP8, DFN8.

**QFN20 dimensions [DS §6.1]:** body **3.000 mm × 3.000 mm** (D, E; 2.900–3.100), height **0.550 mm** (A; 0.500–0.600), standoff A1 0.000–0.050 mm, ball/lead width b 0.150–0.250 mm, **exposed pad 1.650 mm × 1.650 mm** (D2, E2; 1.550–1.750). The package outline drawing is titled `Puya QFN20L 3x3X0.55-0.4PITCH POD`, i.e. **0.4 mm pitch**.

### QFN20 pinout **[DS Figure 3-1, "QFN20 Pinout1 PY32L020F15U6 (Top view)"]**

| Pin | Name | | Pin | Name |
|---:|---|---|---:|---|
| 1 | *(see note)* | | 11 | `PB4` |
| 2 | `PA6` | | 12 | `PB3` |
| 3 | `PA7` | | 13 | `PB2` |
| 4 | `PC0-NRST` | | 14 | `PB1` |
| 5 | `PC1` | | 15 | `PB0` |
| 6 | `PB7` | | 16 | `PA0` |
| 7 | `VSS` | | 17 | `PA1` |
| 8 | `PB6-SWD` | | 18 | `PA2-SWC` |
| 9 | `VCC` | | 19 | `PA3` |
| 10 | `PB5` | | 20 | `PA4` |

> **Pin 1's label was not recovered cleanly** from the datasheet's figure by text extraction; the remaining 19 assignments are contiguous and unambiguous, and `PA5` is the only port pin unaccounted for. It is very likely `PA5`, but that is **[INF]** and is not asserted. Read the figure directly if pin 1 matters to you.

Note `PC0` doubles as `NRST`, and `PB6`/`PA2` carry `SWD`/`SWCLK` — so debug and reset consume three of the 18 GPIOs unless deliberately repurposed.

### Family siblings **[DS Tables 1-1, 1-2]**

| Part | Flash | SRAM | GPIO | ADC ch. | Comparators | Package | Temp |
|---|---:|---:|---:|---|---:|---|---|
| **`PY32L020F15U6`** | 24 KB | 3 KB | **18** | 8 ext + 2 int | **2** | QFN20 | 85 °C |
| `PY32L020L15D6` | 24 KB | 3 KB | 7 | 4 ext + 2 int | — | DFN8 | 85 °C |
| `PY32L020F15P7` | 24 KB | 3 KB | — | — | — | TSSOP20 | 105 °C |
| `PY32L020W15S7` | 24 KB | 3 KB | — | — | — | SOP16 | 105 °C |
| `PY32L020L15S7` | 24 KB | 3 KB | — | — | — | SOP8 | 105 °C |

The `F15U6` is the **largest-GPIO, comparator-bearing** member — which is why it, and not a cheaper sibling, is the one M5Stack ships as a 14-GPIO expander.

---

## 4. Used By

### `devices/m5stack/papermono`

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md).

**This part appears twice on the board, under two different M5Stack marketing names.** Schematic sheet 1's power/IO map block diagram annotates both custom chips with the silicon part number **[SCH]**:

| Block label on sheet 1 | Annotation | M5Stack name | Designator | I²C address |
|---|---|---|---|---|
| `PMIC` | **`PY32L020F15U6`** | **[M5PM1](../../m5stack/m5pm1/README.md)** | `U7` (sheet 2) | `0x6E` |
| `PYB` | **`PY32L020F15U6_IIC`** | **[M5IOE1](../../m5stack/m5ioe1/README.md)** | `U17` (sheet 4) | `0x4F` |

#### 4.1 The package count corroborates the identification

Both schematic symbols carry **21 pin markers** — 20 signal/power pins plus a 21st netted to `GND`. **[SCH]**

That is exactly a **QFN20 plus exposed pad** (§3), and the PY32L020F15U6 is the only PY32L020 variant with a 20-pin QFN package. The pin counts are independent of M5Stack's own manuals, which describe pins 1–20 plus a ground pad. **[INF]** — a consistency check, not proof of the die.

The M5IOE1's advertised resource set also lines up with the silicon: **14 GPIOs** (of the part's 18, minus `NRST`, the two SWD pins and the I²C pair), **4 PWM channels** (from `TIM1`/`TIM14`), a **12-bit ADC** (the part's), and a **die temperature sensor** (`[DS]` lists temperature-sensor characteristics in §5.3.15). None of that requires custom silicon. **[INF]**

#### 4.2 What is silicon and what is firmware

This distinction is the whole reason this record exists separately from the M5PM1/M5IOE1 records.

| Behaviour | Where it comes from |
|---|---|
| Cortex-M0+ core, 24 KB flash, 3 KB SRAM, 48 MHz, 1.7–5.5 V, QFN20 | **Silicon** — this record |
| 12-bit ADC, 2 comparators, TIM1/TIM14/LPTIM, SPI/I²C/USART, CRC-32, UID, SWD | **Silicon** — this record |
| I²C addresses `0x6E` and `0x4F`; the `M5PM1_REG_*` / `M5IOE1_REG_*` maps; NeoPixel RAM; 32 B retention RAM; the wake-source state machine; the power-button long/short/double-press logic; `PWM_FREQ` registers; the `AW8737A_PULSE` register | **M5Stack firmware** — see the [M5PM1](../../m5stack/m5pm1/README.md) and [M5IOE1](../../m5stack/m5ioe1/README.md) records |
| The `PYG`*n* pin naming, and its 1-based-label / 0-based-enum trap | **M5Stack convention**, not Puya's. Puya calls the pins `PA0`–`PB7` |

> ⚠ **All of the firmware behaviour can change with a firmware revision.** M5Stack ships version registers (`M5PM1_REG_SW_REV` at `0x03`, `M5IOE1_REG_REV` at `0x02`) precisely because it can. The silicon in this record cannot change; the layer above it can.

#### 4.3 The chips are not field-reprogrammable in practice

The PY32L020's programming interface is **SWD** on `PB6-SWD` / `PA2-SWC` (§3). Neither pin appears on any PaperMono net that reaches a header, test point or connector in the extracted schematic text. **[SCH]**, **[INF]**

So although the underlying part is an ordinary, cheap, publicly documented MCU that anyone could reflash, on this board it is effectively a fixed-function device. Recovering a bricked M5PM1 would require physically probing a 0.4 mm-pitch QFN.

---

## 5. Development ecosystem for the bare part

Relevant only if you are **using a PY32L020 in your own design**, not if you are talking to an M5PM1.

| Item | Notes |
|---|---|
| Vendor SDK | Puya publishes an HAL/LL driver package and CMSIS device headers for the PY32 series |
| Toolchain | Standard `arm-none-eabi-gcc` targeting Cortex-M0+ (`-mcpu=cortex-m0plus`) |
| Debug/flash | **SWD**, with common probes (ST-LINK, DAPLink, J-Link). Puya also supports a serial bootloader on some family members |
| Community | The PY32F0 series has an active open-source community (`IOsetting/py32f0-template` and similar) whose toolchain and linker setup carry over to the PY32L020 with a different device header. **[INF]** — not verified for the L020 specifically |
| Arm CMSIS-Pack | Availability for PY32L020 was **not** verified this session |

**No driver is needed to use an M5PM1 or M5IOE1** — those speak I²C and have their own libraries. See the linked records.

---

## 6. Integration pitfalls (bare part)

1. **24 KB flash is the whole budget.** With a printf-heavy libc you will run out.
2. **Reset shares `PC0`, SWD shares `PB6`/`PA2`.** Repurposing them as GPIO costs you debug or reset access, and getting that wrong on a QFN20 means a dead board.
3. **BOR is off by default** and is enabled through an **option byte**, not at runtime **[DS §2.5.2.2]**. On a battery design that is exactly backwards from what you want, and option bytes are set at programming time.
4. **The ADC reference is selectable** between 1.5 V / 2.048 V / 2.5 V and `VCC` (§3). On a 1.7–5.5 V part, defaulting to `VCC` gives you a ratiometric measurement whose scale moves with the battery.
5. **`LPTIM` is the only timer that wakes from Stop** (§3). Waking on `TIM1` will not work.
6. **Two datasheet major versions exist** (§1). V1.0/V1.1 predate the V2.0 "major version" of 2025-05-20; if you have an older PDF, check what changed before trusting a table.

---

## 7. Alternatives

| Part | vs. PY32L020 | When |
|---|---|---|
| Puya **PY32F002 / PY32F003 / PY32F030** | The non-`L` PY32 branch — more flash, less aggressive low power | General-purpose use |
| ST **STM32L011 / STM32G030** | Very similar class; the PY32 family is widely described as a low-cost STM32-alike | When you want ST's documentation and ecosystem |
| **[WCH CH32V203](../../wch/ch32v203c8t6/README.md)** | RISC-V, more flash/RAM, USB | Documented in this repository — used as the Tanmatsu's coprocessor in exactly the same architectural role |
| Nuvoton **N76E003**, Padauk **PMS150** | 8-bit, cheaper | When 24 KB of Cortex-M0+ is overkill |
| A dedicated PMIC | Purpose-built silicon | When you do not want to write and maintain power-management firmware — see [TI BQ25895](../../texas-instruments/bq25895/README.md) for what a real PMIC's register map looks like |

**The interesting comparison is the last two rows.** M5Stack's choice — a general-purpose MCU running vendor firmware, presented as a custom part — trades silicon cost and flexibility against documentation quality: every behaviour is a vendor manual away rather than a datasheet away, and every behaviour can change. The Tanmatsu makes the same trade with a CH32V203, and the Waveshare knob board makes it with a second ESP32. It is a common pattern in this repository and worth recognising as one.

---

## 8. Open questions

- **Pin 1 of the QFN20** (§3) — almost certainly `PA5`, not confirmed.
- Whether M5Stack's firmware uses the `LPTIM`, the comparators or the CRC unit; nothing in the published register maps suggests the last two are exposed.
- Whether the M5PM1 and M5IOE1 dies are literally the same part or differ in a way the schematic annotation glosses over. Sheet 1 annotates one `PY32L020F15U6` and the other `PY32L020F15U6_IIC`; the `_IIC` suffix is **not** a Puya ordering-code field (§1.1) and is presumably M5Stack's own note that this instance is the I²C-slave one. **[INF]**
- Whether SWD is reachable anywhere on the PaperMono (§4.3).
- No hardware was in the loop; nothing was measured or programmed.

---

## Manufacturer

**Puya Semiconductor (Shanghai) Co., Ltd.** No vendor sourcing guide exists in this repository yet.

**Sourcing note, and a small finding in its own right.** The copy retained here did not come from Puya. It came from **M5Stack's own documentation CDN**:

```
https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1205/PY32L020_Datasheet_EN.pdf
https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1205/PY32L020_Datasheet_ZH.pdf
```

Asset folder `1205` is the same pool the PaperMono's zh_CN documentation page uses for `ST25R3916_ZH.pdf` — i.e. **M5Stack hosts the datasheet of the silicon behind its "custom" chips, in the same place as the PaperMono's other component datasheets, but does not link it from the PaperMono product page.** The page's Datasheets list names ESP32-S3, ST25R3916, SSD1677, the touchscreen, RX8130CE, BMI270 and SX1262 — and neither PY32L020 nor the M5PM1/M5IOE1 manuals. Whether it is linked from some other M5Stack page was not checked.

Both files were served as `application/pdf` to plain `curl` with a Chrome 131 User-Agent; `%PDF` verified; no fallback User-Agent and no login required. Puya's own site (`www.puyasemi.com`) is reachable but was not needed.

## Related pages

- [M5Stack M5PM1](../../m5stack/m5pm1/README.md) — this silicon running M5Stack's power-management firmware, I²C `0x6E`
- [M5Stack M5IOE1](../../m5stack/m5ioe1/README.md) — this silicon running M5Stack's I/O-expander firmware, I²C `0x4F`
- [WCH CH32V203C8T6](../../wch/ch32v203c8t6/README.md) — the same architectural pattern on a different board
- [Espressif ESP32-S3R8](../../espressif/esp32-s3r8/README.md) — the host that both coprocessors serve

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | PY32L020 Datasheet (English) | Puya Semiconductor (Shanghai) Co., Ltd. | primary (via vendor-of-board mirror) | datasheet | <https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1205/PY32L020_Datasheet_EN.pdf> | 2026-09-01 | **V2.0**, 2025-05-20, 51 pp, 2 262 732 B | **24 KB flash / 3 KB SRAM for `PY32L020F15U6`**, ordering-code decode, full peripheral table, QFN20 pinout and dimensions, family comparison, version history | `artifacts/py32l020-datasheet-en-v2.0-m5stack-mirror.pdf` |
| D2 | PY32L020 数据手册 (Chinese) | Puya | primary (via mirror) | datasheet | <https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1205/PY32L020_Datasheet_ZH.pdf> | 2026-09-01 | 49 pp, 2 652 633 B | Same content, Chinese; retained because the EN and ZH page counts differ (49 vs 51), so the two are not straight translations of one layout | `artifacts/py32l020-datasheet-zh-m5stack-mirror.pdf` |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | schematic | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | Sheet 1's `PMIC = PY32L020F15U6` and `PYB = PY32L020F15U6_IIC` annotations; the 21-pad symbols for `U7` and `U17` | `devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/py32l020-datasheet-en-v2.0-m5stack-mirror.pdf` | 2 262 732 | `b55f52c3c0a73e2d5256f715caf93ef36aca351c66974ed47838ed7a146c972d` | 51 |
| `artifacts/py32l020-datasheet-zh-m5stack-mirror.pdf` | 2 652 633 | `ddb566b4ab1fec1cc61a5c76668003b089cb37880151a4474b18add2e6b3a5ff` | 49 |

**Method note.** Both files validated as `%PDF` with intact text layers. The 24 KB / 3 KB figures in §2 were taken from `Table 1-1` by locating the `PY32L020F15U6` column explicitly, not from the cover's "up to" wording, and cross-checked against the ordering-code field `5 = 24 KB` in §7 of the same document.
