# M5Stack M5IOE1

- **Category:** custom I²C GPIO expander — 14 GPIOs, 4 × 12-bit ADC, 4 × PWM, NeoPixel driver, die temperature sensor, 32 B retention RAM, open-drain interrupt output
- **Not an ASIC.** The schematic identifies the underlying silicon as a **Puya `PY32L020F15U6`** Cortex-M0+ MCU — annotated `PY32L020F15U6_IIC` — running M5Stack's own I/O-expander firmware. Everything below is *firmware* behaviour.
- **I²C address:** **`0x4F`** as fitted on PaperMono — **which is outside the range the V1.4 manual documents.** See §7-C1; this conflict is recorded, not resolved.
- **Research status:** the **full M5Stack manual is retained** in `artifacts/` (V1.4, 10 pages) and has been read end to end. The pin table is corroborated **pin-for-pin, all 21 pads**, by the PaperMono schematic. No hardware was in the loop.
- **Retrieved:** 2026-09-01

The I/O expander of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) and its Lite sibling. It owns the `L3B` power domain — display, touch controller, microSD, PDM microphone — plus the LoRa reset/antenna-switch lines, the NFC rail, two of the three RGB LED channels, and the I²C gate that keeps the IP2315 charger off the bus.

---

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[DS]** | Stated in `artifacts/m5ioe1-chip-user-manual-v1.4-en.pdf`, with page reference | `not-tested` — vendor claim reproduced verbatim; nothing measured |
| **[SCH]** | Read out of `PaperMono_SCH_V0.6.2_20260522.pdf`, cited as sheet + designator + pin | `executed-success` for the extraction; `not-tested` electrically |
| **[SRC]** | Read out of M5Stack source at a cited `file:line` | `executed-success` for the read; `not-tested` on hardware |
| **[DOC]** | `docs.m5stack.com` product/API page, retrieved 2026-09-01 | `not-tested` |
| **[FW]** | String recovered from the shipped factory firmware binary | `executed-success` for the extraction |
| **[INF]** | Inference drawn from two or more of the above | `inferred` |

**Nothing in this record was verified electrically.** No pin, register or address below was guessed.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Marketing name | **`M5IOE1`** | **[DS]** cover; **[SCH]** sheet 4 block label next to `U17` |
| Publisher of the manual | **Shenzhen Mingzhan Information Technology Co., Ltd.** (M5Stack's legal entity) | **[DS]** cover |
| Document | **M5IOE1 Chip User Manual V 1.4**, 10 pp., dated **2025-11-25** in its own revision table | **[DS]** cover, p. 10 |
| **Underlying silicon** | **`PY32L020F15U6`** — Puya PY32 series, Cortex-M0+ | **[SCH]** sheet 1, power/IO map block diagram: the legend row `PYB` is annotated **`PY32L020F15U6_IIC`**. The `_IIC` suffix distinguishes the I²C-expander firmware build from the PMIC build on the same die (row `PMIC` → `PY32L020F15U6`) |
| Nature of the part | A **general-purpose MCU pre-programmed with M5Stack firmware** | **[DS]** §I: "provides fixed IO management, ADC, interrupt and other functions **by burning custom IO function firmware**" |
| I²C address, per the manual | **`0x6F`–`0x76`**, selected by the voltage on **`IO7` (PA6)** sampled at power-on | **[DS]** §I.2(4), §V.5, Table 6 (p. 9) |
| I²C address, **as fitted on PaperMono** | **`0x4F`** | **[SRC]** `M5PaperMono-UserDemo/main/hal/hal_board.cpp:14`; **[SRC]** `M5IOE1/src/M5IOE1.h:80` (`M5IOE1_DEFAULT_ADDR_2`); **[SRC]** `M5GFX/src/M5GFX.cpp:213`; **[DOC]** product page PinMap |
| ⚠ Address conflict | **Unresolved.** `0x4F` does not appear anywhere in the V1.4 manual. See §7-C1 | — |
| I²C speed | **100 kHz default**, 400 kHz selectable via `I²C_CFG[4] SPD`. PaperMono runs it at **100 kHz** | **[DS]** §I.2(4); **[FW]** `Initializing M5IOE1 with 100KHz (device default)` |
| Package | **21 pads** on the schematic symbol: 20 signal/power pins per the manual's Table 1, plus **pin 21 = `VSS`** | **[DS]** Table 1 (p. 2) gives pins 1–20; **[SCH]** sheet 4 `U17`.21 = `VSS` |
| Reference designator on PaperMono | **`U17`**, sheet 4 | **[SCH]** |
| Identity registers | `UID_L`/`UID_H` (`0x00`/`0x01`) — 16-bit factory-programmed unique ID; `REV` (`0x02`) — firmware major version, default **`A`** (ASCII) | **[DS]** Table 3 p. 4, §IV.1 |
| ⚠ Marking verified? | **No.** No teardown photograph of `U17` was inspected; the `PY32L020F15U6` identification rests on the schematic's block diagram | **[INF]** |

### 1.1 Same die, two firmwares

The M5IOE1 and the [M5PM1](../m5pm1/README.md) are the **same Puya part with different M5Stack firmware**, which explains a great deal of the two manuals' shared structure — identical section layout, identical publisher, identical wording in §Resource/§Function, an `AW8737A PULSE` register in both, 32 bytes of retention RAM in both, the same "all GPIO outputs default to open-drain" caveat in both.

It also explains the differences that matter:

- The PMIC firmware exposes **5** GPIOs, the expander firmware **14** — because the two builds bond out different numbers of the same die's pins to the same 20-pin footprint.
- The PMIC has a **fixed** address, the expander a **pin-selected** one.
- **They number their pins differently** (§6). That is a firmware/API decision, not silicon.
- Electrical limits are the PY32's, and **neither manual states them** — no supply range, no absolute maximum ratings, no I/O drive strength. Component record pending at `components/puya/py32l020f15u6/`.

---

## 2. Pin table

Manual Table 1 and the PaperMono schematic symbol agree on all 20 signal pins, in order. Both naming conventions are given because they differ: the manual says `IOn`, the schematic says `PYGn`.

| Pin | Manual name **[DS]** p. 2 | Manual type | Schematic symbol name **[SCH]** `U17` | PaperMono net **[SCH]** | PaperMono function |
|---:|---|---|---|---|---|
| 1 | `NRST` | NRST | `NRST` | `RST` (via `R53`) | Expander reset, **active low** |
| 2 | `INT_OUT` | Interrupt output | `OD_INTOUT` | `G7_PYB_IRQ` | Interrupt to ESP32-S3 GPIO7 |
| 3 | `IO14` | GPIO | `PYG14` | `PYB_TF_EN` | microSD power enable |
| 4 | `VSS` | VSS | `VSS` | `GND` | |
| 5 | `IO12` | GPIO | `PYG12` | `PYB_PDM_EN` | PDM microphone power enable |
| 6 | `VCC` | VCC | `VCC` | `3V3_L2` | |
| 7 | `IO1` | GPIO | `PYG1` | `PYB_TF_DET` | microSD card-detect (active low) |
| 8 | `SDA` | I²C | `I2C_SDA` | `G47_SYS_SDA` | |
| 9 | `SCL` | I²C | `I2C_SCL` | `G48_SYS_SCL` | |
| 10 | `IO11` | GPIO | `PYG11_PWM3` | `PYB_CHG_IIC` | **IP2315 charger I²C bus gate** |
| 11 | `IO2` | GPIO | `PYG2_ADC1` | `PYB_LoRa_ANT_SW` | SX1262 antenna switch |
| 12 | `IO8` | GPIO | `PYG8_PWM2` | `PYB_LED_G` | RGB LED green channel |
| 13 | `IO9` | GPIO | `PYG9_PWM1` | `PYB_LED_B` | RGB LED blue channel |
| 14 | `IO3` | GPIO | `PYG3` | `PYB_EPD_EN` | **E-paper 3V3 rail enable** |
| 15 | `IO13` | GPIO | `PYG13` | `PYB_TP_EN` | Touch controller VDD enable |
| 16 | `IO4` | GPIO | `PYG4_ADC2` | `PYB_NFC_EN` | NFC/RFID power enable |
| 17 | `IO5` | GPIO | `PYG5_ADC3` | `PYB_EINK_RST` | **E-paper reset** |
| 18 | `IO6` | GPIO | `PYG6` | `PYB_TP_RST` | Touch controller reset |
| 19 | `IO7` | GPIO | `PYG7_ADC4` | **`ADD_SET`** | **I²C address select** (see §1, §7-C1) |
| 20 | `IO10` | GPIO | `PYG10_PWM4` | `PYB_LoRa_RST` | SX1262 `NRST` |
| 21 | *(not in Table 1)* | — | `VSS` | `GND` | |

The `PYGn` ↔ `IOn` mapping is **exact and independently confirmed 7-for-7** by the suffixes: the schematic's `PYG2_ADC1`, `PYG4_ADC2`, `PYG5_ADC3`, `PYG7_ADC4`, `PYG9_PWM1`, `PYG8_PWM2`, `PYG11_PWM3`, `PYG10_PWM4` match the manual's channel assignments and the library's channel comments without exception **[DS]** Table 2, **[SCH]** `U17`, **[SRC]** `M5IOE1/src/M5IOE1.h`.

Note the pin order is **not** monotonic in `IOn` — the physical sequence is 14, 12, 1, 11, 2, 8, 9, 3, 13, 4, 5, 6, 7, 10. Never infer a pin number from position.

### 2.1 Pin capabilities and mutual exclusions

**[DS]** Table 2, p. 3.

| Pin | MUX | Interrupt exclusion / note |
|---|---|---|
| `IO1` | — | Interrupt mutually exclusive with `IO6` |
| `IO2` | **ADC1** | Excl. with `IO3`; interrupt auto-disabled while ADC is enabled |
| `IO3` | — | Excl. with `IO2` |
| `IO4` | **ADC2** | Interrupt auto-disabled while ADC is enabled |
| `IO5` | **ADC3** | **Interrupt disabled during I²C idle sleep**; also disabled while ADC is enabled |
| `IO6` | — | Excl. with `IO1` |
| `IO7` | **ADC4** | Excl. with `IO12`; also the **power-on address-select input** (§1) |
| `IO8` | **PWM2** | Excl. with `IO9`; interrupt auto-disabled while PWM is enabled |
| `IO9` | **PWM1** | Excl. with `IO8` |
| `IO10` | **PWM4** | Excl. with `IO14` |
| `IO11` | **PWM3** | Excl. with `IO13` |
| `IO12` | **SWDIO** | Excl. with `IO7`. **SWDIO disabled by default** |
| `IO13` | **SWCLK** | Excl. with `IO11` |
| `IO14` | **NeoPixel output** | Excl. with `IO10` |
| `INT_OUT` | — | **Open-drain; external pull-up required.** Pulled low on interrupt, released after `GPIO_IS` is cleared |
| `SDA`, `SCL` | — | **Open-drain; external pull-ups required** |
| `NRST` | — | **Active-low reset** |

Consolidated exclusion groups **[DS]** Table 5, p. 9 — *interrupts* cannot be enabled simultaneously within a pair: `IO1 & IO6` · `IO2 & IO3` · `IO7 & IO12` · `IO8 & IO9` · `IO10 & IO14` · `IO11 & IO13`.

> ⚠ **All GPIO outputs default to open-drain** (`GPIO_DRV_L` = `0xFF`, `GPIO_DRV_H` = `0x3F`), including NeoPixel and PWM. With no external pull-up you must switch the pin to push-pull. **[DS]** Table 2 note 1, Table 3.
>
> ⚠ **ADC / PWM / I²C / SWD / NeoPixel occupancy overrides the GPIO registers.** When a pin is claimed by a peripheral, `GPIO_M_x` and `GPIO_O_x` become inoperative for that pin. **[DS]** §IV.2(9).

---

## 3. I²C address selection

**[DS]** §V.5, Table 6 (p. 9). At power-on the firmware samples `IO7` (die pin PA6) and picks an address from an eight-step voltage ladder:

| Voltage on `IO7` at power-on | I²C address |
|---|---|
| **Floating** | **randomly assigned** in `0x6F`–`0x76` |
| 0 – 412.5 mV | `0x6F` |
| 412.5 – 825 mV | `0x70` |
| 825 – 1237.5 mV | `0x71` |
| 1237.5 – 1650 mV | `0x72` |
| 1650 – 2062.5 mV | `0x73` |
| 2062.5 – 2475 mV | `0x74` |
| 2475 – 2887.5 mV | `0x75` |
| 2887.5 – 3300 mV | `0x76` |

Manual's own warnings: do not sit on a boundary voltage, and **do not leave `IO7` floating at power-on** or the address is random.

On PaperMono `IO7` is netted `ADD_SET` **[SCH]** `U17`.19 — the mechanism is used as designed — yet the address the firmware and documentation both use is **`0x4F`**, outside this table entirely. §7-C1.

---

## 4. Register map

Transcribed from **[DS]** Table 3 (pp. 4–5) and §IV (pp. 5–9). Library symbol names from **[SRC]** `M5IOE1/src/M5IOE1.h`.

Layout convention: every GPIO register is split **`_L` covering P8–P1** in bits `[7:0]` and **`_H` covering P14–P9** in bits `[5:0]`, with `[7:6]` reserved.

> ⚠ **Burst access is range-limited.** I²C sequential read/write works only within the blocks `0x00–0x2F`, `0x30–0x6F`, `0x70–0x8F`, `0x90`. Crossing a boundary requires separate transactions. **[DS]** Table 3 note 2.

| Addr | Register | Access | Default | Function |
|---|---|---|---|---|
| `0x00` / `0x01` | `UID_L` / `UID_H` | R | — | 16-bit factory-programmed unique identifier |
| `0x02` | `REV` | R | `A` | Firmware major version, `SW7–SW0` (ASCII since `SW:A`) |
| `0x03` / `0x04` | `GPIO_M_L` / `_H` | R/W | `0x00` | Direction. **0 = input (default), 1 = output** |
| `0x05` / `0x06` | `GPIO_O_L` / `_H` | R/W | `0x00` | Output level; effective only when `M[n] = 1` |
| `0x07` / `0x08` | `GPIO_I_L` / `_H` | R | — | Real-time input level |
| `0x09` / `0x0A` | `GPIO_PU_L` / `_H` | R/W | `0x00` | Pull-up enable |
| `0x0B` / `0x0C` | `GPIO_PD_L` / `_H` | R/W | `0x00` | Pull-down enable |
| `0x0D` / `0x0E` | `GPIO_IE_L` / `_H` | R/W | `0x00` | Interrupt enable |
| `0x0F` / `0x10` | `GPIO_IP_L` / `_H` | R/W | `0x00` | Interrupt polarity — **1 = rising/high, 0 = falling/low** |
| `0x11` / `0x12` | `GPIO_IS_L` / `_H` | R/W | `0x00` | Interrupt status — **write 0 to clear** |
| `0x13` / `0x14` | `GPIO_DRV_L` / `_H` | R/W | **`0xFF` / `0x3F`** | **1 = open-drain (default), 0 = push-pull** |
| `0x15` | `ADC_CTRL` | R/W | `0x00` | `[7]` `BUSY` (R), `[6]` `START`, `[2:0]` channel |
| `0x16` / `0x17` | `ADC_D_L` / `_H` | R | — | 12-bit result: `_H[3:0]` + `_L[7:0]` |
| `0x18` | `TEMP_CTRL` | R/W | `0x00` | `[7]` `TBUSY` (R), `[6]` `TSTART` |
| `0x19` / `0x1A` | `TEMP_D_L` / `_H` | R | — | 12-bit die temperature, **°C** |
| `0x1B` / `0x1C` | `PWM1_L` / `_H` | R/W | `0x00` | **`IO9`** — PaperMono RGB **blue**. `_H`: `[7]` EN, `[6]` POL, `[3:0]` duty `[11:8]` |
| `0x1D` / `0x1E` | `PWM2_L` / `_H` | R/W | `0x00` | **`IO8`** — PaperMono RGB **green** |
| `0x1F` / `0x20` | `PWM3_L` / `_H` | R/W | `0x00` | **`IO11`** |
| `0x21` / `0x22` | `PWM4_L` / `_H` | R/W | `0x00` | **`IO10`** |
| `0x23` | `I²C_CFG` | R/W | `0x00` | `[6]` `INTERNAL_PU/PD` (**0 = enabled, 1 = disabled**), `[5]` `WAKE_TYPE` (0 = falling, 1 = rising), `[4]` `SPD` (0 = 100 k, 1 = 400 k), `[3:0]` `SLEEP` idle-sleep seconds (0 = none) |
| `0x24` | `LED_CFG` | R/W | `0x00` | `[6]` `REFRESH` (self-clearing), `[5:0]` NeoPixel count 0–32 (0 = all off) |
| `0x25` / `0x26` | `PWM_FREQ_L` / `_H` | R/W | `0xF4` / `0x01` | Frequency in **Hz**; default `0x01F4` = **500 Hz** |
| `0x27` / `0x28` | `REF_VOLTAGE_L` / `_H` | R | — | 16-bit ADC reference, **mV** |
| `0x29` | `RESET` | W | — | **Write `0x3A`** to restore factory configuration |
| `0x30`–`0x6F` | `LED_RAM` | R/W | `0x00` | 64 bytes: 32 NeoPixels × RGB565 |
| `0x70`–`0x8F` | `RTC_RAM` | R/W | `0x00` | **32 bytes** power-off retention memory |
| `0x90` | `AW8737A PULSE` | R/W | `0x00` | `[7]` REFRESH, `[6:5]` pulse count 0–3, `[4:0]` target GPIO **0–13 ⇒ GPIO1–GPIO14** |

### 4.1 ADC

`ADC_CTRL[2:0]` **[DS]** §IV.3(1): `000` disabled · `001` **ADC1 = `IO2`** · `010` **ADC2 = `IO4`** · `011` **ADC3 = `IO5`** · `100` **ADC4 = `IO7`**.

Flow: write channel + `START = 1` → poll until `BUSY = 0` → read `ADC_D_H/L` **[DS]** §V.1. Convert with `REF_VOLTAGE` (`0x27`/`0x28`).

Note `ADC4` is on `IO7`, the **same pin that selects the I²C address at power-on** — so on any board that uses address selection, ADC4 is effectively spoken for by a fixed divider.

### 4.2 Pull configuration is a two-register truth table

**[DS]** Table 4, p. 6. `PU[n]`/`PD[n]` are separate registers and `1/1` is **not** an error state, it is "no pull":

| `PU[n]` | `PD[n]` | Result |
|:--:|:--:|---|
| 1 | 0 | Pull-up |
| 0 | 1 | Pull-down |
| 0 | 0 | None |
| **1** | **1** | **None** |

### 4.3 PWM

Duty = `DUTY[11:0] / 0xFFF`, `0x000` = 0 %, `0xFFF` ≈ 100 % **[DS]** §IV.5(3). All four channels share the single `PWM_FREQ` register. High and low duty bytes must be written together to avoid a transient wrong duty **[DS]** §IV.5(5).

**I²C idle sleep is disabled outright while PWM is enabled** **[DS]** §V.4 — the same restriction as on the M5PM1.

---

## 5. Libraries

| Option | Where | Verdict |
|---|---|---|
| **`M5IOE1`** — M5Stack's own dual Arduino/ESP-IDF driver | `github.com/m5stack/M5IOE1`, ESP-IDF registry `m5stack/m5ioe1`, latest **1.0.9**; MIT | ✅ **Use this** — but read §6 first. `src/M5IOE1.h` is a bilingual annotated copy of the register map |
| Raw I²C / register masks | — | What M5GFX does: `lgfx::i2c::bitOn(port, 0x4F, reg, mask, freq)` **[SRC]** `M5GFX/src/M5GFX.cpp:2088-2096`. Avoids the off-by-one entirely |
| Raw values with the library object | — | What the vendor's own OTP demo does: `ioe.digitalWrite(2, true)` with the comment `// M5IOE1 uses zero-based pin indexes.` **[SRC]** `EDP_SPI.cpp:36-38` |

Version pinned by the PaperMono factory firmware: **`m5stack/m5ioe1` 1.0.9** **[SRC]** `M5PaperMono-UserDemo/dependencies.lock`.

Examples shipped: `interrupt_hardware`, `interrupt_polling`, `pin_test`. Note the repository also ships a committed `.claude/` directory — agent configuration published in a release library **[SRC]**.

---

## 6. ⚠ The `M5IOE1_PIN_n = n − 1` off-by-one

> **This is the single most damaging trap on any board carrying both M5Stack expanders.**
>
> ```c
> // M5IOE1/src/M5IOE1.h:31-45
> M5IOE1_PIN_NC = -1,
> M5IOE1_PIN_1  = 0,
> M5IOE1_PIN_2  = 1,
> M5IOE1_PIN_3  = 2,     // <-- M5IOE1.h:34
> ...
> M5IOE1_PIN_14 = 13,
> ```
>
> | Part | Enum | Value | Rule | Evidence |
> |---|---|---|---|---|
> | **M5IOE1** | `M5IOE1_PIN_3` | **`2`** | Label **1**-based, enum value **0**-based — **off by one** | **[SRC]** `M5IOE1/src/M5IOE1.h:34` |
> | [**M5PM1**](../m5pm1/README.md) | `M5PM1_GPIO_NUM_3` | **`3`** | 0-based; **label equals value** | **[SRC]** `M5PM1/src/M5PM1.h:410` |
>
> **Consequences.**
>
> 1. The documentation label `PYG3` = manual pin `IO3` = enum `M5IOE1_PIN_3` = **raw value 2** = **register bit 2**. Passing the literal `3` where the enum was expected targets `IO4` — on PaperMono, that swaps *e-paper power enable* for *NFC power enable*.
> 2. The two chips sit on the same bus in the same vendor documentation with **different conventions**. Code that is correct for one is wrong for the other.
> 3. **There is no `M5IOE1_PIN_0`.** `M5IOE1.h` defines `M5IOE1_PIN_1 … _14` and `M5IOE1_MAX_GPIO_PINS 14` **[SRC]**. So a documentation reference to `PYG0` (e.g. `PYG0_RTC_INT`) **cannot** denote an M5IOE1 pin under any reading — it is an M5PM1 pin that the docs mislabelled with the expander's prefix.
> 4. M5GFX sidesteps the whole thing by writing register bit masks directly, and its inline comments independently confirm the mapping — **[SRC]** `M5GFX/src/M5GFX.cpp:2088-2092`:
>
> ```
> // bit2==IO3: EPD EN
> // bit4==IO5: EPD RST
> // bit5==IO6: TP RST
> // bit12==IO13: TP EN
> // bit13==IO14: TF EN
> ```
>
> 5. The vendor's own recommended e-paper demo distrusts the enum enough to bypass it with an explicit warning comment **[SRC]** `M5PaperMono-OTP-Demo/components/EDP_OTP_LUT_demo/src/EDP_SPI.cpp:36-38`.
>
> **Neither the manual nor any `docs.m5stack.com` page states this.** It is visible only in the header.

---

## 7. Caveats, errata and conflicts

| # | Issue | Evidence |
|---|---|---|
| **C1** | **⚠ Address `0x4F` is undocumented.** The V1.4 manual states the address range is **`0x6F`–`0x76`** in three places (§I.2(4), Table 2 note 2, Table 6) and gives an eight-step voltage ladder on `IO7` to select within it. PaperMono uses **`0x4F`**, and `IO7` *is* wired to `ADD_SET`. The library's constant is named `M5IOE1_DEFAULT_ADDR_2`, implying a second scheme, and its auto-detect sweeps **both** `0x6F–0x76` **and** `0x4F–0x50`. **Unresolved.** The two credible readings are (a) the fitted firmware is newer than V1.4 documents and adds a low-address bank, or (b) Table 6 is incomplete. Least-risky implementation path: **do not hardcode either address — use the library's auto-detection, or probe both ranges**, and read `REV` (`0x02`) to learn which firmware you are talking to | **[DS]** §I.2(4), §V.5, Table 6 vs **[SRC]** `M5IOE1/src/M5IOE1.h:80-81`, `hal_board.cpp:14`, `M5GFX.cpp:213`, and **[DOC]** |
| **C2** | **Pin-numbering off-by-one vs the M5PM1.** §6. Not stated in any vendor document | **[SRC]** `M5IOE1.h:34` vs `M5PM1.h:410` |
| **C3** | **The `LED_RAM` note contradicts itself.** §IV.7(2) says "PIX0_L = 0x30, **PIX0_H = 0x37**, …, PIX31_H = 0x6F". With 2 bytes per LED starting at `0x30`, `PIX0_H` is `0x31`; `0x37` would be `PIX3_H`. The identical defect appears in the M5PM1 manual's corresponding note | **[DS]** §IV.7(2) p. 8 |
| **C4** | **`AW8737A PULSE` GPIO field width is inconsistent.** Table 3 draws five `GPIO` bits at `0x90`; §IV.11(3) calls the field `GPIO[4:0]` with range 0–13. Both are self-consistent, but the M5PM1's equivalent register is documented as `[6:5] NUM` / `[5:0] GPIO` — **overlapping bit 5** — so the two manuals cannot both be right about the shared field layout | **[DS]** Table 3 p. 5, §IV.11 p. 8; cf. M5PM1 manual §IV.9 |
| **C5** | **`REV` default is `A`, an ASCII character in a hex table.** The changelog's last entry is "`SW:A` — Update firmware version to A (ASCII); remove hardware version". Reading `0x02` yields `0x41`, not `0x0A`. Straightforward to get wrong | **[DS]** Table 3 p. 4, appendix p. 10 |
| **C6** | **No electrical specification whatsoever.** No supply range, no absolute maximum ratings, no I/O drive strength, no ADC input ceiling, no timing. The M5PM1 manual at least states a 3.3 V ADC limit; this one does not | **[DS]** whole document |
| **C7** | **`ADC4` and address-select share `IO7`.** Any board that biases `IO7` to pick an address has committed that pin, so only three of the four ADC channels are practically available. Not called out by the manual | **[INF]** from **[DS]** §IV.3(1) + §V.5 |
| **C8** | **`SWDIO`/`SWCLK` are on `IO12`/`IO13`.** These are the PY32's debug pins. SWDIO is "disabled by default", but `IO13` (SWCLK) is used on PaperMono as the touch-controller power enable. Whether re-enabling SWD is possible at runtime, and what that does to a live board, is not documented | **[DS]** Table 2 p. 3; **[SCH]** `U17`.15 |
| **C9** | **Docs omit `IO4` and `IO11`.** M5Stack's dedicated power-management API page lists eleven M5IOE1 pins and mentions **neither `PIN_4`** (NFC power enable, `hal_board.cpp:29`) **nor `PIN_11`** (the IP2315 I²C gate — the one pin with a published bus-stability hazard). A reader working only from that page would not know either exists | **[DOC]** vs **[SRC]** `hal_board.cpp:29`, `Power_Class.cpp:78-80` |
| **C10** | **A stale comment in M5GFX misdescribes an expander write.** `M5GFX.cpp:2096` reads `bitOn(..., 0x06, 0b00110000, ...)` with the comment `// Set LOW io11, HIGH io13,14`. Register `0x06` is `GPIO_O_H` (P14–P9 in `[5:0]`); mask `0b00110000` is bits 4–5 ⇒ **`IO13` and `IO14` only**, and `bitOn` cannot set anything low. The **code** is consistent with the rest of the bring-up; the comment is wrong. Inert, but misleading to anyone reverse-engineering the pin map from comments | **[SRC]** `M5GFX/src/M5GFX.cpp:2096` |
| **C11** | **`INTERNAL_PU/PD` polarity is inverted relative to intuition:** `0 = Enabled`, `1 = Disabled` | **[DS]** §IV.6(1) p. 7 |

---

## 8. Used By

### [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) — designator `U17`, sheet 4

The M5IOE1 sits on rail **`L2`** (so it is powered only when the ESP32-S3 is) and in turn owns rail **`L3B`**. That ordering matters: the expander is **not** available while the board is in its deepest sleep state, and the peripherals it gates come up only after M5Unified has initialised it **[DOC]**.

| Role on PaperMono | Pin / enum | Evidence |
|---|---|---|
| System I²C slave at **`0x4F`** on the shared internal bus, **GPIO47 = SDA / GPIO48 = SCL**, 100 kHz | pins 8/9 | **[SCH]** `U17`.8/.9; **[SRC]** `hal_board.cpp:14`; **[FW]** |
| Interrupt out to **ESP32-S3 GPIO7** | pin 2 `INT_OUT` → `G7_PYB_IRQ` | **[SCH]** `U17`.2; **[DOC]**. ⚠ **Not exercised by the factory firmware** — it initialises the expander with `M5IOE1_INT_MODE_DISABLED` (`hal_board.cpp:62`) and polls instead; `GPIO_NUM_7` appears **zero** times in the UserDemo **[SRC]** |
| Expander reset | pin 1 `NRST` ← `RST` via `R53` | **[SCH]** `U17`.1 |
| **Address select** | pin 19 `IO7` ← `ADD_SET` | **[SCH]** `U17`.19. See §7-C1 |
| microSD card-detect (active low) | `IO1` / `M5IOE1_PIN_1` (value **0**) | **[SRC]** `hal_tf_card.cpp:16` |
| **SX1262 antenna switch** | `IO2` / `M5IOE1_PIN_2` (value **1**) | **[SRC]** `hal_lora.cpp:31` |
| **E-paper 3V3 rail enable** (`EPD_3V3_L3B`) | `IO3` / `M5IOE1_PIN_3` (value **2**) | **[SRC]** `app_sleep_wake.cpp:73`; `EDP_SPI.cpp:37` (raw `2`); `M5GFX.cpp:2088` (`bit2`) — **three independent sources** |
| **NFC/RFID power enable** | `IO4` / `M5IOE1_PIN_4` (value **3**) | **[SRC]** `hal_board.cpp:29`, `app_sleep_wake.cpp:74`. Also the **Pro-vs-Lite discriminator**: if this write fails the firmware declares the board a Lite (`hal_board.cpp:160-172`) |
| **E-paper reset** | `IO5` / `M5IOE1_PIN_5` (value **4**) | **[SRC]** `app_sleep_wake.cpp:75`; `EDP_SPI.cpp:38` (raw `4`); `M5GFX.cpp:2089` (`bit4`) |
| FT6336G touch reset | `IO6` / `M5IOE1_PIN_6` (value **5**) | **[SRC]** `app_sleep_wake.cpp:76`; `M5GFX.cpp:2090` (`bit5`) |
| RGB LED **green**, PWM channel **2** | `IO8` / `M5IOE1_PIN_8` (value **7**) | **[SRC]** `hal_board.cpp:25,27` |
| RGB LED **blue**, PWM channel **1** | `IO9` / `M5IOE1_PIN_9` (value **8**) | **[SRC]** `hal_board.cpp:26,28` |
| **SX1262 `NRST`** | `IO10` / `M5IOE1_PIN_10` (value **9**) | **[SRC]** `hal_lora.cpp:30` |
| **IP2315 charger I²C bus gate** | `IO11` (`gpio11`, value **10**) | **[SRC]** `M5Unified/src/utility/Power_Class.cpp:78-80, 85` |
| PDM microphone power enable | `IO12` / `M5IOE1_PIN_12` (value **11**) | **[SRC]** `hal_mic.cpp:13`; `hal_board.cpp:30` |
| FT6336G touch VDD enable | `IO13` / `M5IOE1_PIN_13` (value **12**) | **[SRC]** `app_sleep_wake.cpp:81`; `M5GFX.cpp:2091` (`bit12`) |
| microSD power enable | `IO14` / `M5IOE1_PIN_14` (value **13**) | **[SRC]** `hal_tf_card.cpp:15`; `M5GFX.cpp:2092` (`bit13`) |

**The RGB LED is split across two chips.** Red is `LED_EN` on the [M5PM1](../m5pm1/README.md); green and blue are `IO8`/`IO9` here. Both use 5 kHz PWM **[SRC]** `hal_board.cpp:24`.

**The IP2315 gate is a structural mitigation, not advice.** M5Stack's warning reads: "do not keep the IP2315 mounted on the I²C bus for extended periods; disconnect it promptly after communication to avoid reducing bus communication stability" **[DOC]**. In code the charger is physically gated **off** the bus by `IO11` and connected only for the duration of a transaction, with a **64-attempt** scan loop waiting for it to appear, then disconnected again **[SRC]** `Power_Class.cpp:88-96`, `:2399`, `:2724`. Any caller that talks to `0x75` without going through `set_papermono_ip2315_enabled()` simply will not find it.

**M5Unified already owns several of these pins.** M5Stack's own warning **[DOC]**: "The pins associated with the e-paper display, touch controller, microSD, and PDM microphone are already used by M5Unified. Before modifying them, ensure that the corresponding peripheral has stopped, or the peripheral may stop working or require reinitialization."

**Not verified on this board:** the interrupt output (polled instead); all four ADC channels (`IO2`, `IO4`, `IO5`, `IO7` are all used as digital lines or as `ADD_SET`); PWM3/PWM4 (`IO11`/`IO10` used as digital); NeoPixel on `IO14`; the temperature sensor; the retention RAM; the `AW8737A` pulse register.

### [M5Stack PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md)

**Same part, same designator, same address.** The Lite drops NFC and LoRa, so `IO2`, `IO4` and `IO10` lose their consumers; the vendor pin table on the Lite product page renames `TF_EN`/`TF_DET` to `EN`/`DET` but the pins are identical **[DOC]**. M5Stack publishes a 4-sheet `PRJ` PDF for the Lite rather than the 6-sheet `SCH`, so the Lite's expander wiring is **not** independently confirmed against a schematic here.

---

## 9. Related components

- [**M5PM1**](../m5pm1/README.md) — the sibling custom PMIC: same publisher, same PY32 die, **different pin-numbering convention** (§6) and a fixed address
- `components/puya/py32l020f15u6/` — the underlying MCU. *Record pending.* The only source of electrical limits, which this manual omits entirely (§7-C6)
- [**Solomon Systech SSD1677**](../../solomon-systech/ssd1677/README.md) — the e-paper controller whose power and reset lines are `IO3` and `IO5`
- [**DKE DEPG0397BBS770F3**](../../dke/depg0397bbs770f3/README.md) — the panel behind it
- [**Semtech SX1262**](../../semtech/sx1262/README.md) · [**M5Stack Stamp-LoRa-1262**](../stamp-lora-1262/README.md) — reset and antenna switch on `IO10` / `IO2`
- [Vendor sourcing guides index](../../../vendors/README.md) — no M5Stack chip-documentation guide exists yet

---

## 10. Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/m5ioe1-chip-user-manual-v1.4-en.pdf` | 398 463 | `9204d99cb2e03395ffc905e05fbeddf7f9f25de5698a31a65fa439dee700d8d2` | **M5IOE1 Chip User Manual V1.4**, 10 pp., English. PDF metadata: Author `洋 熊`, Creator/Producer `Microsoft® Word 2021`, created **2026-01-26**. Text layer validated against rendered headings before transcription |

**Text-layer validation.** `pdftotext -layout` output was cross-checked against the running headers (`M5IOE1 Chip User Manual`), footers (`n / 10`, `The Innovator of Modular IoT Development Platform | M5Stack`) and section numbering. No subsetting or code-point-offset corruption observed.

**Metadata note.** The same author string (`洋 熊`) and toolchain produced the M5PM1 manual, and the two documents share their section structure — consistent with one document having been derived by editing the other. Where they disagree about a shared feature (e.g. the `AW8737A` bit layout, §7-C4), neither is automatically authoritative.

**A Chinese-language edition exists and was not retrieved.** The `zh_CN` product page links `1210/IO_Expander_Datasheet_CN.pdf` where `en`/`ja` link `IO_Expander_Datasheet_EN.pdf` **[DOC]**. Note the upstream *filename* is `IO_Expander_Datasheet_EN.pdf`, not `M5IOE1_…` — worth knowing when searching. A CN↔EN diff is the most promising route to settling §7-C1.

**Licence.** M5Stack copyright, no licence statement on the document. Redistribution status **`unknown`**; disposition `repository`.

---

## 11. Authoritative sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | M5IOE1 Chip User Manual | **M5Stack** (imprint: Shenzhen Mingzhan Information Technology Co., Ltd.) | primary | chip manual | `artifacts/m5ioe1-chip-user-manual-v1.4-en.pdf`; upstream `static-cdn.m5stack.com/resource/docs/products/core/PaperMono/1210/IO_Expander_Datasheet_EN.pdf` | 2026-09-01 | **V1.4, 2025-11-25** | §1–§4, §7 |
| S-2 | PaperMono schematic | M5Stack | primary | schematic PDF | `PaperMono_SCH_V0.6.2_20260522.pdf` (held in the device tree) | 2026-09-01 | **V0.6.2, 2026-05-22**, 6 sheets | §1 silicon identity (sheet 1), §2 pin table (sheet 4 `U17`), §8 wiring |
| S-3 | `M5IOE1` Arduino/ESP-IDF driver | M5Stack | primary | source | `github.com/m5stack/M5IOE1` @ `846eec7d05e25c09013be2acdb8804487f48a62e` | 2026-09-01 | tag **1.0.9**, MIT | §4 symbol names, §6 enum values, §7-C1 |
| S-4 | `M5PaperMono-UserDemo` factory firmware source | M5Stack | primary | source | `github.com/m5stack/M5PaperMono-UserDemo` @ `c1099107271d31a0678d661a896e2b04dbb331ea` | 2026-09-01 | 2026-08-10, MIT | §8 board roles |
| S-5 | `M5PaperMono-OTP-Demo` | M5Stack | primary | source | `github.com/m5stack/M5PaperMono-OTP-Demo` @ `c7c02554f89fd06f80d988b805b2a59050c78a46` | 2026-09-01 | 2026-08-20, MIT | §5, §6 raw-index workaround |
| S-6 | `M5GFX` / `M5Unified` | M5Stack | primary | source | `github.com/m5stack/M5GFX` @ `d91077b9…`; `github.com/m5stack/M5Unified` @ `8530f537…` | 2026-09-01 | 0.2.28 / 0.2.21 | §6 bit-mask confirmation, §7-C10, §8 IP2315 gate |
| S-7 | PaperMono product page + `arduino/papermono/m5pm1_m5ioe1` API page | M5Stack | primary | vendor docs | `docs.m5stack.com/en/core/PaperMono`, `.../en/arduino/papermono/m5pm1_m5ioe1` | 2026-09-01 | undated | §7-C9, §8 power tree and IP2315 warning |
| S-8 | `C153-PaperMono-ESP32S3R8-UserDemo-V1.2` firmware image | M5Stack via M5Burner | primary | binary | firmware id `2089640807996628993`, SHA-256 `72c290bc2ffa216041b276660277369bd17ecef92315e367d98bb2c96c8428fa` | 2026-09-01 | v1.2, built 2026-08-06 | §1 100 kHz default, address `0x4F` |
