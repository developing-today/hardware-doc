# Injoinic IP2315

> Single-cell Li-ion **synchronous buck charger** with integrated power MOSFETs, integrated USB input fast-charge protocol handling (PD / FCP / AFC / PE+), 4.8 A maximum charge current, and an I²C control interface **multiplexed onto its battery-level LED driver pins**.
> Research snapshot **2026-09-01**. Fitted as **`U1`** on sheet 2 of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153). **No hardware was available** — every claim below traces to the Injoinic datasheet, the PaperMono schematic PDF, or M5Stack's published source.

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Injoinic `IP2315` datasheet **V1.0** (Chinese), local copy `artifacts/ip2315-datasheet-v1.0-cn-radxa-mirror.pdf` | `not-tested` — vendor document reproduced |
| **[SCH]** | `PaperMono_SCH_V0.6.2_20260522.pdf`, cited by sheet + designator + pin. Extraction is text-layer parsing of the Altium PDF | `executed-success` for the extraction; `not-tested` electrically |
| **[SRC]** | M5Stack source at a cited `file:line` | `executed-success` for the read |
| **[DOC]** | `docs.m5stack.com/en/core/PaperMono`, retrieved 2026-09-01 | `not-tested` |
| **[INF]** | Inference drawn from two or more of the above | `inferred` |

**Nothing here was verified electrically.** No register, address or pin was guessed.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **IP2315** (the schematic annotates it `IP2315（无后缀）` — "no suffix") | **[SCH]** sheet 2 |
| Manufacturer | **Injoinic Technology** (英集芯), Shenzhen | **[DS]** cover, `service@injoinic.com` |
| Function | Integrated-MOSFET synchronous buck charger for 1S Li-ion with USB input fast-charge protocol negotiation | **[DS]** §概述 |
| Package | **QFN32, 5 mm × 5 mm, 0.5 mm pitch** (31 signal pins + EPAD pin 33) | **[DS]** 特性 |
| Switching frequency | **500 kHz** | **[DS]** §概述 |
| **I²C address** | **`0xEA` write / `0xEB` read (8-bit) = `0x75` 7-bit** | **[DS]** §I2C; **[SRC]** `M5Unified/src/utility/Power_Class.cpp:72`; **[DOC]** |
| I²C rate | up to **400 kbps**; 8-bit register address, 8-bit data, MSB first | **[DS]** §I2C |
| Datasheet revision | **V1.0**, © 2018 Injoinic Corp., 16 pp | **[DS]** footer |
| Copyright year on document | 2018 — the document has not been revised since | **[DS]** |

> ⚠ **The 7-bit address is 0x75 and the datasheet never says so.** The datasheet gives only the 8-bit forms `0xEA`/`0xEB`. `0xEA >> 1 = 0x75`. Anyone comparing the datasheet against M5Stack's `0x75` without doing that shift will conclude the two disagree. They do not. **[INF]**

---

## 2. Key electrical limits and capabilities **[DS]**

| Parameter | Value |
|---|---|
| Input voltage range | **5 V – 12 V** |
| Maximum battery charge current | **4.8 A** at 9 V / 2 A input |
| Battery float voltage | **4.2 / 4.35 / 4.4 / 4.5 V**, selected by a resistor on the `VSET` pin (which is multiplexed with `LED3`) |
| Charge current setting | resistor on `ICHGSET` (pin 27) sets the **input-side** current |
| Efficiency | 94 % @ 5 V in, 93.5 % @ 9 V, 93 % @ 12 V (BAT 3.7 V, 4 A) |
| Input fast-charge protocols | **USB Type-C PD**, Huawei **FCP**, Samsung **AFC**, MTK **PE+ 1.1 / 2.0** |
| Adaptive behaviour | reduces charge current automatically when a weak adapter cannot hold up |
| Status indication | 1 or 2 LEDs, count auto-detected |
| Protections | NTC battery temperature, input over-voltage, chip over-temperature |
| ESD | 4 kV |

### 2.1 `ICHGSET` resistor table **[DS §恒流充电电流设置]**

The resistor from `ICHGSET` (pin 27) to GND sets the **input** current, not the battery current:

| R<sub>ICHG</sub> | Input current set |
|---|---|
| 51 kΩ | 500 mA |
| 130 kΩ | 1000 mA |
| 180 kΩ | 1500 mA |
| > 300 kΩ (NC) | 2000 mA |

### 2.2 `NTC` network **[DS §充电 NTC]**

The `NTC` pin (26) sources **20 µA** into an external network and compares the resulting voltage:

| Condition | Meaning |
|---|---|
| V(NTC) > **1.32 V** | battery too **cold** |
| V(NTC) < **0.43 V** | battery too **hot** |

Normal charging is permitted between roughly **0 °C and 55 °C**. The datasheet's worked example is *"R<sub>NTC</sub> = 100 kΩ @ 25 °C (B = 4100), R2 = 82 kΩ"*.

> ⚠ **`NTC` must never float.** If the function is unused the datasheet requires a **51 kΩ** resistor to GND; a floating pin *"可能导致充电异常"* — may cause abnormal charging. **[DS]**

---

## 3. ⚠ The I²C pins are the LED driver pins — this is the whole hazard

This is the single most important thing to understand about this part, and it is the mechanism behind the warning M5Stack publishes for the PaperMono.

**[DS §引脚说明]** gives the pin functions verbatim:

| Pin | Name | Datasheet description (translated) |
|---:|---|---|
| **8** | **`LED1`** | Battery-level LED drive pin L1; **`SCK` when the I²C function is used** |
| **9** | **`LED2`** | Battery-level LED drive pin L2; **`SDA` when the I²C function is used** |
| **10** | **`LED3`** | Battery-level LED drive pin L3; **multiplexed with `VSET`** |

So the chip has exactly one set of pins that must serve as either a **current-sinking LED indicator driver**, a **battery-voltage select strap**, or an **I²C slave port** — and it decides which at power-up, from what it sees on those pins.

**[DS §I2C]** shows the vendor's reference connection, and the detail that matters is the supply the pull-ups return to:

```
                       VBAT
                        |
        +---------------+---------------+
        |                               |
      2K2                             2K2
        |                               |
  MCU --+-- SCL ----------------- 8  IP2315
  MCU --+-- SDA ----------------- 9
  MCU ------ INT ---------------- 10
```

**Both I²C pull-ups go to `VBAT`, not to the host's logic rail.** That is what M5Stack's product page is describing when it says:

> *"The I2C operating mode of the charging chip IP2315 depends on the I2C pins being pulled up to VBAT voltage. Connecting the device to USB triggers mode detection; if the VBAT voltage is too low, the IP2315 may not initialize into I2C mode properly, which can interfere with other devices on the same I2C bus."* **[DOC]**

### 3.1 The second half of the hazard: a missing NACK wedges the bus

**[DS §I2C, 特别说明]**, translated:

> *"At the end of an I²C read, when the last byte has been read, a **NACK signal must be given**. Otherwise the IP2315 believes the MCU still wants more data, will output the next byte on the following SCLK, will not receive the STOP condition properly, and **this may lock up the I²C bus** (可能会导致 I2C 总线拉死)."*

The vendor also requires read–modify–write on every register and forbids touching reserved bits:

> *"Reserved registers must not be written arbitrarily and their existing values must not be changed, or unpredictable results will occur. Register operations must be performed read-modify-write, changing only the bits in use."*

**Put the two together and the PaperMono's design makes sense as a defensive measure, not a nicety.** A part that (a) may fail to enter I²C mode at all if the battery is flat, and (b) can hold SDA/SCL indefinitely after a mis-terminated read, is a part you do not want permanently attached to a bus shared with the touch controller, RTC, IMU, NFC reader and both M5Stack coprocessors.

---

## 4. Pinout as fitted on the PaperMono **[SCH sheet 2, `U1`]**

Recovered from the Altium PDF's pin markers. The parser attributes markers `PIU10x` to designator `U1` pin `0x`; the second charger-column designator on that sheet is the JW5712 (`U10`), which is a separate part.

| Pin | Name | Net on PaperMono | Notes |
|---:|---|---|---|
| 2 | `CC1` | USB-C `CC1` **through `R1` = `NC/1%`** | ⚠ §4.1 |
| 3 | `CC2` | USB-C `CC2` **through `R2` = `NC/1%`** | ⚠ §4.1 |
| 6, 7, 18, 19 | `VSYS` | `VBAT_L0` side, with `C6`, `C7`, `R6`, `R7` | "input intermediate node, requires capacitors" **[DS]** |
| **8** | **`LED1` / `SCL`** | **`CHG_SYS_SCL`** | → B-side of the `AW39112DNR` gate (`U3`) |
| **9** | **`LED2` / `SDA`** | **`CHG_SYS_SDA`** | → B-side of the `AW39112DNR` gate (`U3`) |
| 10 | `LED3` / `VSET` | local network with `R11` (`NC`) / `R12` (`100 kΩ`) and `LED1` (a real indicator LED on sheet 2) | battery float-voltage strap |
| 11–14 | `LX` | `L1` = `FTC252012S2R2MBCA` (2.2 µH) | buck switching node |
| 15 | `BST` | `100 nF/25 V` to `LX` | bootstrap |
| 16 | `HLED` | `Q1` (`CJ3439KDW` dual MOSFET) | fast-charge mode status output **[DS]** |
| 17, 31 | `GND` | `GND` | |
| 20, 21 | `VIN` | **`5V_IN`** — the output of the [AW32901FCR](../../awinic/aw32901/README.md) OVP switch | sheet annotates "PD Only" and "Ipeak 1.5A" |
| 22 | `BAT` | `VBAT_L0` | battery sense / charge output |
| 23 | `DM` | local network with `D1` (`DSK34`), `R3` (1 MΩ) | BC1.2 / legacy adapter detect |
| 24 | `DP` | same network | |
| **26** | **`NTC`** | `R15` = **`100K-RNTC`** thermistor + `R16` = **82 kΩ** | matches the datasheet's worked example exactly |
| **27** | **`ICHGSET`** | one of `R17` = 15 kΩ / `R18` = `NC` | ⚠ §4.2 |
| 33 (EPAD) | `GND` | `GND` | power + thermal ground |

Input bulk on this rail is `C8`–`C11` = 4 × 22 µF/10 V. **[SCH]**

### 4.1 ⚠ PD is depopulated — this is a 5 V charger in practice

The series resistors on both CC pins, `R1` and `R2`, carry the value **`NC/1%`** in the schematic's text layer — i.e. **not fitted**. **[SCH]**

Independently, the IP2315's `VIN` comes from `5V_IN`, the output of the [AW32901FCR](../../awinic/aw32901/README.md), whose over-voltage threshold is **5.95 V typical** — it disconnects the input before 9 V could ever arrive.

**Consequence:** the IP2315's headline capability — asking a PD/FCP/AFC/PE+ adapter for 9 V or 12 V to shorten charge time — **cannot function on this board**, twice over. It runs as a plain 5 V-input buck charger. **[INF]**, from two `executed-success` schematic observations. Anyone reading the IP2315 datasheet and expecting 9 V behaviour from a PaperMono will be surprised; anyone porting this charger design to a board that *does* want fast charge must populate `R1`/`R2` **and** move to a higher-threshold AW329xx.

### 4.2 ⚠ Unresolved: which resistor lands on `ICHGSET`

Four resistors sit in a row under the `NTC` / `ICHGSET` pins: `R15` = `100K-RNTC`, `R16` = `82 kΩ/1%`, `R17` = `15 kΩ/1%`, `R18` = `NC/1%`. **[SCH]**

`R15` + `R16` are unmistakably the NTC network — they reproduce the datasheet's own worked example (100 kΩ NTC @ 25 °C, R2 = 82 kΩ) verbatim. Which of `R17`/`R18` reaches `ICHGSET` was **not resolved** from the PDF text layer, and **15 kΩ does not appear in the datasheet's `ICHGSET` table at all** (51 k / 130 k / 180 k / NC). Sheet 1's block diagram annotates the charge current as **0.5 C**, which for the 1150 mAh cell is ≈575 mA — closest to the 51 kΩ / 500 mA row.

This should be read off the rendered schematic sheet graphically before being relied on. Recorded as an open question rather than guessed.

---

## 5. Used By

### `devices/m5stack/papermono`

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md), designator **`U1`**, schematic sheet 2.

Charges the 1150 mAh single-cell battery from the USB-C port, behind the [AW32901FCR](../../awinic/aw32901/README.md) input over-voltage switch. It is **not permanently attached to the system I²C bus**.

**The gate.** `CHG_SYS_SCL` / `CHG_SYS_SDA` (pins 8/9) reach the shared system bus only through an [**AW39112DNR**](../../awinic/aw39112/README.md) 2-bit level translator, `U3`: **[SCH]** sheet 2

| `U3` pin | Name | Net |
|---:|---|---|
| 1 | `VCCA` | `VBUS_L0` |
| 2 | `A1` | `G48_SYS_SCL` (ESP32-S3 GPIO48) |
| 3 | `A2` | `G47_SYS_SDA` (ESP32-S3 GPIO47) |
| 4 | `GND` | `GND` |
| **5** | **`OE`** | **`PYB_CHG_IIC`** |
| 6 | `B2` | `CHG_SYS_SDA` |
| 7 | `B1` | `CHG_SYS_SCL` |
| 8 | `VCCB` | **`VBAT_L0`** |

Two details make this the correct implementation of §3 rather than a generic isolator:

- **`VCCB` is `VBAT_L0`.** The B-side (charger side) of the translator tracks the battery, so `CHG_SYS_SCL`/`SDA` idle at V<sub>BAT</sub> — exactly the condition the IP2315 requires to come up in I²C mode. The A-side tracks `VBUS_L0`, the system logic rail.
- **`OE` is `PYB_CHG_IIC`**, driven from **M5IOE1 `PYG11_PWM3`** (`U17` pin 10/11, sheet 4). **[SCH]** Deasserting `OE` removes the charger from the bus entirely.

**The firmware side.** `M5Unified/src/utility/Power_Class.cpp` implements exactly this: the charger is connected via IOE1 `gpio11` only for the duration of a transaction, with a **64-attempt** scan loop waiting for `0x75` to appear (`:88–96`), then disconnected again (`:2399`, `:2724`). **[SRC]**

> ⚠ **Callers that talk to the IP2315 without going through `set_papermono_ip2315_enabled()` will simply not find anything at `0x75`.** That is not a bug; it is the design.

**Vendor operating rule, verbatim [DOC]:**

> *"M5IOE1 controls the connection between the IP2315 and the system I2C bus via PYG11_PWM3: during device operation, do not keep the IP2315 mounted on the I2C bus for extended periods; disconnect it promptly after communication to avoid reducing bus communication stability. If an I2C bus communication anomaly occurs, you can reset the device by briefly pressing the power button to restore normal bus operation."*

The suggested recovery — a short press of the power button — works because that is an [M5PM1](../../m5stack/m5pm1/README.md) reset input, and cycling the rails re-runs the IP2315's power-up mode detection. **[INF]**

**Documentation gap.** M5Stack's dedicated power-management page (`/en/arduino/papermono/m5pm1_m5ioe1`) lists the M5IOE1 pins but **omits `M5IOE1_PIN_11` entirely** — the one pin with a published bus-stability hazard. The warning exists only on the two product pages. A developer working from the power-management tutorial alone would not know the gate exists.

---

## 6. Drivers and libraries

| Option | Notes |
|---|---|
| **`M5Unified` `Power_Class`** | The only published driver for this part that we found. Handles the bus gating; PaperMono-specific. See `M5Unified/src/utility/Power_Class.cpp` |
| Linux / Zephyr | **No mainline driver exists for the IP2315.** Injoinic parts are not represented in either tree (checked 2026-09-01) |
| Roll your own | Feasible — the register map is in the datasheet §I2C onward — but you must implement the NACK-on-last-byte rule (§3.1) and read–modify–write discipline yourself |

---

## 7. Integration pitfalls, in priority order

1. **NACK the last byte of every read.** Failing to do so can hold the bus (§3.1). If your I²C driver's "read N bytes" helper ACKs everything, this part will eventually wedge the bus.
2. **Do not leave it on a shared bus.** Either give it a private bus or gate it, as the PaperMono does (§5).
3. **A flat battery can prevent I²C mode entirely** (§3), because mode selection depends on the pins being pulled to V<sub>BAT</sub>. Expect enumeration failures on a deeply discharged pack, and do not treat "charger not found" as a fatal error.
4. **Read–modify–write only.** Reserved bits must be preserved (§3.1).
5. **`NTC` must not float** — 51 kΩ to GND if unused (§2.2).
6. **`ICHGSET` sets the *input* current, not the battery current** (§2.1). Getting this backwards over-dimensions the charge rate.
7. **`VSET` shares a pin with `LED3`.** A design that wants three status LEDs cannot also strap the float voltage on that pin.
8. **The 7-bit address is 0x75**, from the datasheet's 8-bit `0xEA` (§1).

---

## 8. Alternatives

| Part | vs. IP2315 | When to prefer it |
|---|---|---|
| **IP2312 / IP2308 / IP2326** (Injoinic) | Same family, differing input-protocol support and current | Cost/feature trims within the same ecosystem |
| **[TI BQ25895](../../texas-instruments/bq25895/README.md)** | 5 A charger with integrated ADC telemetry and 3.1 A boost, **dedicated I²C pins**, fully public register map at `0x6A` | When you need telemetry, OTG boost, or an I²C port that is not shared with an LED driver. Documented in this repository |
| **[TI BQ25306](../../texas-instruments/bq25306/README.md)** | Much simpler, no boost, no ADC | Charging and nothing else. Documented in this repository |
| **[SG Micro SGM40567](../../sgmicro/sgm40567/README.md)** | Linear charger, resistor-programmed | Low current, no switching noise, no bus at all |

The IP2315's distinguishing feature is **input fast-charge protocol negotiation in the charger itself** — no separate PD sink controller. On the PaperMono that feature is depopulated (§4.1), which makes the part choice look like commonality with other M5Stack products rather than a requirement of this board. **[INF]**

---

## 9. Open questions

- Which of `R17` (15 kΩ) / `R18` (NC) is the `ICHGSET` resistor, and therefore what the configured input current actually is (§4.2).
- What `VSET` is strapped to, and hence the float voltage — the `LED3` network shares the pin with a fitted indicator LED, which the datasheet does not show combined with a `VSET` strap.
- Whether the depopulated CC resistors are a cost decision or a deliberate safety choice given the 5.95 V OVP.
- No English-language IP2315 datasheet was found; the only copy obtained is Chinese V1.0 (§10).
- No hardware measurement of charge current, efficiency or bus behaviour.

---

## Manufacturer

**Injoinic Technology (英集芯), Shenzhen.** No vendor sourcing guide exists in this repository yet.

Sourcing notes gathered this session, worth recording because they cost time:

- `https://www.injoinic.com/` is **intermittently unreachable**. Three of four attempts on 2026-09-01 timed out at 25–40 s; one returned a 2 642-byte redirect shell. Do not conclude the site is dead on a single timeout.
- `datasheet.lcsc.com` and `www.lcsc.com/datasheet/...` return **HTTP 200 with `text/html`** for this part's PDF URL — an interstitial, not the document. `https://www.lcsc.com/datasheet/lcsc_datasheet_2402211727_INJOINIC-IP2315_C2764357.pdf` returned 47 427 bytes of HTML. **Always check for the `%PDF` magic bytes, never the status code.**
- The copy that worked is a **Radxa mirror**: `https://dl.radxa.com/rock3/docs/hw/datasheet/IP2315-datasheet-cn-V1.0.pdf`, served as `application/pdf`, `%PDF` verified.

## Related pages

- [Awinic AW39112DNR](../../awinic/aw39112/README.md) — the level translator that gates this chip on and off the shared bus
- [Awinic AW32901FCR](../../awinic/aw32901/README.md) — the input OVP switch upstream of `VIN`
- [M5Stack M5IOE1](../../m5stack/m5ioe1/README.md) — drives `PYB_CHG_IIC`, the gate's `OE`
- [M5Stack M5PM1](../../m5stack/m5pm1/README.md) — owns the rails and the power button used to recover a wedged bus
- [Generic charger / power-path record](../../generic/charger-power-path/README.md)

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | IP2315 数据手册 (datasheet, Chinese) | Injoinic Corp. | primary (via credible mirror) | datasheet | <https://dl.radxa.com/rock3/docs/hw/datasheet/IP2315-datasheet-cn-V1.0.pdf> | 2026-09-01 | **V1.0**, © 2018, 16 pp, 1 217 455 B | Pin table, I²C address `0xEA`/`0xEB`, LED/SCL/SDA multiplexing, VBAT pull-up requirement, NACK bus-lockup warning, `ICHGSET`/`NTC` tables, QFN32 package | `artifacts/ip2315-datasheet-v1.0-cn-radxa-mirror.pdf` |
| D2 | PaperMono product page (charger hazard note) | M5Stack | primary | official page | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | — | The `PYG11_PWM3` gating rule and the bus-stability warning, verbatim | `scratch/m5stack-papermono/docs/pages/en-core-PaperMono.html` |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | schematic | linked from D2 | 2026-09-01 | V0.6.2, 2026-05-22, 6 sheets | Every net and value in §4 and §5 | `devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| S2 | `M5Unified/src/utility/Power_Class.cpp` | M5Stack | primary | repository | <https://github.com/m5stack/M5Unified> | 2026-09-01 | `master` @ `8530f537…`, MIT | The 64-attempt scan loop, connect/disconnect discipline, address `0x75` | `scratch/m5stack-papermono/repos/M5Unified/` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/ip2315-datasheet-v1.0-cn-radxa-mirror.pdf` | 1 217 455 | `412742b36aa816722cc2830420bf660faf214c84acec60f9763ab3ea782951e1` | 16 |

**Method note.** D1 was fetched with `curl` and a Chrome 131 User-Agent, validated as `%PDF` (16 pages), and read via `pdftotext`. LCSC's PDF host was tried first and rejected for serving HTML under a `.pdf` URL with HTTP 200 — see [Manufacturer](#manufacturer).
