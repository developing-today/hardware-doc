# M5Stack M5PM1

- **Category:** custom I²C power-management controller — rail enables, battery charging control, ADC monitoring, power button/state machine, timed wake, 5 multiplexed GPIOs
- **Not an ASIC.** The schematic identifies the underlying silicon as a **Puya `PY32L020F15U6`** Cortex-M0+ MCU running M5Stack's own power-management firmware. Everything below is *firmware* behaviour, not silicon behaviour, and can change with a firmware revision.
- **I²C address:** `0x6E` (fixed; no address-select pin)
- **Research status:** the **full M5Stack manual is retained** in `artifacts/` (V1.9, 33 pages) and has been read end to end. The pin table is independently corroborated pin-for-pin by the PaperMono schematic. No hardware was in the loop.
- **Retrieved:** 2026-09-01

The power-management controller of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) and its Lite sibling. It owns the battery, the 3.3 V LDO and DC/DC rails, the power button, the ESP32-S3 `BOOT` strap and the frontlight PWM — i.e. on this board the ESP32-S3 does not control its own power at all.

---

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[DS]** | Stated in `artifacts/m5pm1-chip-user-manual-v1.9-en.pdf`, with page reference | `not-tested` — vendor claim reproduced verbatim; nothing measured |
| **[SCH]** | Read out of `PaperMono_SCH_V0.6.2_20260522.pdf`, cited as sheet + designator + pin | `executed-success` for the extraction (PDF parsed, pin markers enumerated); `not-tested` electrically |
| **[SRC]** | Read out of M5Stack source at a cited `file:line` | `executed-success` for the read; `not-tested` on hardware |
| **[DOC]** | `docs.m5stack.com` product/API page, retrieved 2026-09-01 | `not-tested` |
| **[FW]** | String recovered from the shipped factory firmware binary | `executed-success` for the extraction |
| **[INF]** | Inference drawn from two or more of the above | `inferred` |

**Nothing in this record was verified electrically.** No pin, register or address below was guessed; every one is transcribed from a cited document, schematic pin marker or source line.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Marketing name | **`M5PM1`** | **[DS]** cover; **[SCH]** sheet 2 block label next to `U7` |
| Publisher of the manual | **Shenzhen Mingzhan Information Technology Co., Ltd.** (深圳市明栈信息科技有限公司 — M5Stack's legal entity) | **[DS]** cover |
| Document | **M5PM1 Chip User Manual V 1.9**, 33 pp., dated **2026-01-22** in its own revision table | **[DS]** cover, p. 33 |
| **Underlying silicon** | **`PY32L020F15U6`** — Puya Semiconductor PY32 series, Cortex-M0+ | **[SCH]** sheet 1, power/IO map block diagram: the legend row `PMIC` is annotated `PY32L020F15U6` |
| Nature of the part | A **general-purpose MCU pre-programmed with M5Stack firmware**, not a purpose-built PMIC | **[DS]** §I: "M5PM1 is a power management IC **programmed with M5Stack custom power management firmware**" |
| I²C address | **`0x6E`**, fixed | **[DS]** §I.2(4); **[SRC]** `M5PM1/src/M5PM1.h:73` (`M5PM1_DEFAULT_ADDR`); **[SRC]** `M5PaperMono-UserDemo/main/hal/hal_board.cpp:13` |
| I²C speed | **100 kHz default**, 400 kHz selectable via `I2C_CFG[4]` | **[DS]** §I.2(4), §IV.1(10) |
| Package | **21 pads** on the schematic symbol: 20 signal/power pins per the manual's Table 1, plus **pin 21 = GND** (exposed pad) | **[DS]** Table 1 (p. 2) gives pins 1–20; **[SCH]** sheet 2 `U7` shows a 21st marker netted to `GND` |
| Reference designator on PaperMono | **`U7`**, sheet 2 | **[SCH]** |
| Device identity registers | `Device_ID` (`0x00`) = **`0x50`**, `Device_Model` (`0x01`) = **`0x20`**, `HW_REV` (`0x02`) = **`0x05`**, `SW_REV` (`0x03`) = **`0x06`** | **[DS]** Table 3 (p. 4), §IV.1(1)–(4) |
| ⚠ Marking verified? | **No.** No teardown photograph of `U7` was inspected. The `PY32L020F15U6` identification rests on the schematic's own block diagram, which is a primary vendor document but not a photograph of the die or top marking | **[INF]** |

### 1.1 Why "it is a PY32" matters

Three practical consequences follow from the part being a stock MCU with vendor firmware rather than dedicated silicon:

1. **The register map is a firmware API, not a hardware datasheet.** The manual's appendix carries a *Firmware Modification History* running from `HW:2 / SW:1` (2025-06-30) to `HW:5 / SW:S` (2026-01-06), and register addresses genuinely moved between those revisions (see §11-C4). Read `SW_REV` (`0x03`) before assuming a layout.
2. **"Download mode" is an MCU bootloader.** `SYS_CMD` (`0x0C`) `CMD=11` and a long press of `PWR_BTN` both put the part into a firmware-update mode **[DS]** §IV.1(13), §V.3. That is a real re-flash path for the PY32, and `BTN_CFG_1[7] DL_LOCK` exists specifically to disable it **[DS]** §IV.7(2).
3. **Electrical limits are the PY32's, and the manual does not restate them.** The manual gives no absolute maximum ratings, no supply range and no I/O current ratings — only "ADC channel input voltage must not exceed 3.3 V" **[DS]** §VI.3(2). For anything else you must consult Puya's `PY32L020` documentation (component record pending at `components/puya/py32l020f15u6/`).

---

## 2. Pin table

The manual's Table 1 (custom-firmware pin arrangement) and the PaperMono schematic symbol agree on all 20 signal pins, in order. Both are reproduced so the two naming conventions can be reconciled — they are **not** the same names.

| Pin | Manual name **[DS]** p. 2 | Manual type **[DS]** | Schematic symbol name **[SCH]** `U7` | PaperMono net **[SCH]** |
|---:|---|---|---|---|
| 1 | `BAT_ADC_EN` | Push-pull output | `BAT_ADC_EN_OD` | `BAT_ADC_EN` |
| 2 | `CHG_EN` | Push-pull output | `CHG_EN_PP` | charger enable |
| 3 | `IO0` | GPIO | `G0_WAKEin(INT0/2)_IRQout_NEOPIXEL` | `PYG0_RTC_INT` |
| 4 | `VSS` | Power | `GND` | `GND` |
| 5 | `LED_EN` | Push-pull output | `LED_EN_PP` | `PY_LED_R` |
| 6 | `VCC` | Power | `VCC` | `3V3_L0` |
| 7 | `PWR_BTN` | Input, pull-up | `BTN_PU` | `PWR_BTN` |
| 8 | `SDA` | I²C | `I2C_SDA_OD` | `G47_SYS_SDA` |
| 9 | `SCL` | I²C | `I2C_SCL_OD` | `G48_SYS_SCL` |
| 10 | `DCDC_5V_EN` | Push-pull output | **`BOOST5V_EN_PP`** | 5 V boost enable |
| 11 | `BAT_ADC` | ADC | `BAT_ADC_IN` | `BAT_ADC` |
| 12 | `IO4` | GPIO | `G4_WAKEin(INT3/4)_IRQout_PWM` | `PYG4_IMU_INT` |
| 13 | `IO3` | GPIO | `G3_WAKEin(INT3/4)_IRQout_PWM` | `PYG3_BL_PWM` |
| 14 | `DCDC_3V3_EN` | Push-pull output | `DCDC3V3_EN_PP` | `3V3_L2_EN` |
| 15 | `BOOT_OUT` | **Open-drain** output | `BOOT_OUT_OD` | `G0_BOOT_OUT` |
| 16 | `5VIN_ADC` | ADC | `5VIN_ADC_IN` | `5VIN_ADC` |
| 17 | `IO1` | GPIO | `G1_IRQout_ADC` | `G1_PY_IRQ` |
| 18 | `LDO_3V3_EN` | Push-pull output | `LDO3V3_EN_PP` | `3V3_L1_EN` |
| 19 | `5VOUT_ADC` | ADC | `5VOUT_ADC_IN` | *(5 V output sense)* |
| 20 | `IO2` | GPIO | `G2_WAKEin(INT0/2)_IRQout_ADC` | `PYG2_LoRa_EN` |
| 21 | *(not in Table 1)* | — | `GND` | `GND` |

Two naming deltas worth carrying forward:

- **Pin 10.** The manual calls it `DCDC_5V_EN`; the schematic symbol calls it `BOOST5V_EN_PP`. Same pin, same function (5 V boost enable). **[INF]**
- **Pins 12/13 are `IO4`/`IO3`, in that order** — the higher-numbered GPIO comes first. Reading the schematic symbol top-to-bottom and assuming ascending GPIO numbers gets this wrong.

### 2.1 Pin functional description

**[DS]** Table 2, p. 3, unless noted.

| Pin | Description | Default state | Note |
|---|---|---|---|
| `IO0` | GPIO 0, **supports wake-up**; MUX = **NeoPixel output** | GPIO | Wake is **mutually exclusive with `IO2`** |
| `IO1` | GPIO 1; MUX = **ADC1** | GPIO | **Cannot wake** — its interrupt line conflicts with `SDA` **[DS]** Table 3 note on `GPIO_WAKE_EN` |
| `IO2` | GPIO 2, supports wake-up; MUX = **ADC2** | GPIO | Wake mutually exclusive with `IO0` |
| `IO3` | GPIO 3, supports wake-up; MUX = **PWM** | GPIO | Wake mutually exclusive with `IO4` |
| `IO4` | GPIO 4, supports wake-up; MUX = **PWM** | GPIO | Wake mutually exclusive with `IO3` |
| `BAT_ADC_EN` | Battery-sampling enable, active high | **High** | |
| `CHG_EN` | Battery-charging enable, active high | **High** (charging on) | Push-pull; polarity was inverted at `HW:3 / SW:2` **[DS]** p. 32 |
| `DCDC_5V_EN` | 5 V DC/DC (boost) control, active high | **Low** | |
| `DCDC_3V3_EN` | 3.3 V DC/DC control, active high | **High** | Drives `3V3_L2_EN` on PaperMono |
| `LDO_3V3_EN` | 3.3 V LDO control, active high | **High** | Drives `3V3_L1_EN` on PaperMono |
| `5VIN_ADC` | 5 V input sense | ADC | **Divider ratio 1:1** |
| `5VOUT_ADC` | 5 V output sense | ADC | **Divider ratio 1:1** |
| `BAT_ADC` | Battery voltage sense | ADC | **Divider ratio 1:1** |
| `PWR_BTN` | Power-button input | Button detection | Internal pull-up enabled by default |
| `LED_EN` | Status-indicator LED control | LED control | **High** by default. "Uses M5PM1 proprietary LED self-control logic and is **not recommended for other purposes**" |
| `BOOT_OUT` | Controls the main controller's (ESP32) `BOOT` strap | **High** | **Open-drain output** |
| `SDA` / `SCL` | I²C | I²C | **Open-drain; external pull-ups required** |

> ⚠ **All GPIO outputs default to open-drain**, including NeoPixel and PWM output. With no external pull-up you must set `GPIO_DRV` to push-pull or the pin will not drive high. **[DS]** Table 2 note 1. `GPIO_DRV` has **higher priority than the mux function** — configuring a pin as PWM does not override an open-drain setting. **[DS]** §IV.2(4).

### 2.2 GPIO mux summary

| GPIO | Wake | IRQ out | ADC | PWM | NeoPixel | Schematic symbol suffix |
|---|:--:|:--:|:--:|:--:|:--:|---|
| `IO0` | ✅ (excl. `IO2`) | ✅ | — | — | ✅ | `_WAKEin(INT0/2)_IRQout_NEOPIXEL` |
| `IO1` | ❌ | ✅ | ✅ ch1 | — | — | `_IRQout_ADC` |
| `IO2` | ✅ (excl. `IO0`) | ✅ | ✅ ch2 | — | — | `_WAKEin(INT0/2)_IRQout_ADC` |
| `IO3` | ✅ (excl. `IO4`) | ✅ | — | ✅ | — | `_WAKEin(INT3/4)_IRQout_PWM` |
| `IO4` | ✅ (excl. `IO3`) | ✅ | — | ✅ | — | `_WAKEin(INT3/4)_IRQout_PWM` |

The schematic symbol annotates pins 13 and 20 with 唤醒源二选一 — "wake source: pick one of two" — which is the same mutual-exclusion rule drawn on the symbol itself **[SCH]** `U7` pins 13, 20.

---

## 3. Register map

Transcribed from **[DS]** Table 3 (pp. 4–11) and §IV (pp. 12–25). Library symbol names are from **[SRC]** `M5PM1/src/M5PM1.h`; that header is an exhaustively commented bilingual copy of this same map and is the practical reference when writing code.

> ⚠ **Burst access is range-limited.** I²C sequential read/write works **only within** `0x00–0x0C`, `0x10–0x19`, `0x20–0x2A`, `0x30–0x35`, `0x38–0x3D`, `0x40–0x45`, `0x48–0x4A`, `0x50`, `0x53`, `0x60–0x9F`, `0xA0–0xBF`. Crossing a range boundary requires separate transactions. **[DS]** §IV preamble, p. 12.

### 3.1 System

| Addr | Name | Access | Default | Function |
|---|---|---|---|---|
| `0x00` | `Device_ID` | R | `0x50` | Device type |
| `0x01` | `Device_Model` | R | `0x20` | Device model |
| `0x02` | `HW_REV` | R | `0x05` | Hardware revision |
| `0x03` | `SW_REV` | R | `0x06` | Firmware revision |
| `0x04` | `PWR_SRC` | R | — | `[2]` BAT valid, `[1]` 5VINOUT valid *(only while the 5 V boost is disabled)*, `[0]` 5VIN valid |
| `0x05` | `WAKE_SRC` | R/W | — | `[6]` 5VINOUT insert, `[5]` GPIO wake, `[4]` command reset, `[3]` reset button, `[2]` power button, `[1]` 5VIN insert, `[0]` timer. **Writing only clears flags; it cannot select a source** |
| `0x06` | `PWR_CFG` | R/W | `0x17` | `[4]` LED_EN level, `[3]` 5 V boost enable, `[2]` 3V3 LDO enable, `[1]` 3V3 DC/DC enable, `[0]` charge enable |
| `0x07` | `HOLD_CFG` | R/W | `0x00` | Retain-across-power-off: `[6]` 5VIN/OUT, `[5]` LDO 3V3, `[4:0]` GPIO4–GPIO0. **Reset to `0x00` by any reset or Download mode** |
| `0x08` | `BATT_LVP` | R/W | `0x40` | Low-voltage cut-off = **2000 mV + n × 7.81 mV** (default ⇒ 2.5 V) |
| `0x09` | `I2C_CFG` | R/W | `0x00` | `[4]` SPD (0 = 100 k, 1 = 400 k), `[3:0]` `SLP_TO` idle-sleep seconds (0 = disabled) |
| `0x0A` | `WDT_CNT` | R/W | `0x00` | Watchdog countdown in **seconds**; 0 disables |
| `0x0B` | `WDT_KEY` | W | — | Write **`0xA5`** to feed |
| `0x0C` | `SYS_CMD` | W | — | `[7:4]` KEY = `0xA`, `[1:0]` CMD: **`01` power off, `10` restart, `11` Download mode** |

### 3.2 GPIO

| Addr | Name | Access | Default | Function |
|---|---|---|---|---|
| `0x10` | `GPIO_MODE` | R/W | `0x00` | `[4:0]` direction, 1 = output. Effective only when the matching `GPIO_FUNC` = `00` |
| `0x11` | `GPIO_OUT` | R/W | `0x00` | `[4:0]` output level. Effective only when `GPIO_FUNC` = `00` **and** `GPIO_MODE` = 1 |
| `0x12` | `GPIO_IN` | R | — | `[4:0]` real-time input level |
| `0x13` | `GPIO_DRV` | R/W | **`0x1F`** | `[5]` LED_EN, `[4:0]` GPIO4–0. **1 = open-drain, 0 = push-pull.** Overrides the mux function |
| `0x14` | `GPIO_PU/PD_0` | R/W | `0x00` | 2 bits per pin, GPIO3–GPIO0: `00` none, `01` pull-up, `10` pull-down |
| `0x15` | `GPIO_PU/PD_1` | R/W | `0x00` | `[1:0]` GPIO4 |
| `0x16` | `GPIO_FUNC0` | R/W | `0x00` | 2 bits per pin, GPIO3–GPIO0: `00` GPIO, `01` IRQ, `10` reserved, **`11` mux (NeoPixel / ADC / PWM)** |
| `0x17` | `GPIO_FUNC1` | R/W | `0x00` | `[1:0]` GPIO4 |
| `0x18` | `GPIO_WAKE_EN` | R/W | `0x00` | `[4:0]`, 1 = wake enabled. **GPIO1 unsupported**; GPIO0/GPIO2 and GPIO3/GPIO4 are pairwise exclusive |
| `0x19` | `GPIO_WAKE_CFG` | R/W | `0x00` | `[4:0]` edge, **1 = rising, 0 = falling**. GPIO1 unsupported |

> **Wake configuration survives Reset, Download mode and power-off.** `GPIO_WAKE_EN`/`GPIO_WAKE_CFG` are explicitly exempted from the state reset that clears everything else. **[DS]** §IV.2(7) note 1, §IV.2(8) note.

### 3.3 ADC

| Addr | Name | Access | Function |
|---|---|---|---|
| `0x20` / `0x21` | `VREF_L` / `_H` | R | Internal ADC reference, **mV** |
| `0x22` / `0x23` | `VBAT_L` / `_H` | R | Battery voltage, **mV** |
| `0x24` / `0x25` | `VIN_L` / `_H` | R | 5 V input voltage, **mV** |
| `0x26` / `0x27` | `5VOUT_L` / `_H` | R | 5 V output voltage, **mV** |
| `0x28` / `0x29` | `ADC_RES_L` / `_H` | R | Raw 12-bit result `[11:0]`; `_H[3:0]` is the high nibble |
| `0x2A` | `ADC_CTRL` | R/W | `[3:1]` `CH_SEL` — **1 = GPIO1, 2 = GPIO2, 6 = internal die temperature (°C)**; `[0]` `START`, self-clearing |

Flow: write `ADC_CTRL` with channel + `START=1` → poll until busy clears → read `ADC_RES_H/L` **[DS]** §V.1. Actual voltage = `raw × VREF / 4096` **[DS]** §VI.3. Channels 1 and 2 only work when the corresponding `GPIO_FUNC` is `11`.

The three dedicated rail sense inputs (`BAT_ADC`, `5VIN_ADC`, `5VOUT_ADC`) are **not** reachable through `ADC_CTRL`; they are read from their own `VBAT`/`VIN`/`5VOUT` register pairs in millivolts and are used internally for low-voltage protection and insert/remove detection **[DS]** §V.1(2).

### 3.4 PWM

| Addr | Name | Access | Default | Function |
|---|---|---|---|---|
| `0x30` | `PWM0_L` | R/W | `0x00` | PWM0 duty `[7:0]` — **this is the PaperMono frontlight** |
| `0x31` | `PWM0_HC` | R/W | `0x00` | `[5]` POL (1 = active-low), `[4]` EN, `[3:0]` duty `[11:8]` |
| `0x32` | `PWM1_L` | R/W | `0x00` | PWM1 duty `[7:0]` |
| `0x33` | `PWM1_HC` | R/W | `0x00` | `[5]` POL, `[4]` EN, `[3:0]` duty `[11:8]` |
| `0x34` / `0x35` | `PWM_FREQ_L` / `_H` | R/W | `0xF4` / `0x01` | Frequency in **Hz**; default `0x01F4` = **500 Hz** |

Duty = `DUTY[11:0] / 0xFFF`. **Both channels share one timer, therefore one frequency** **[DS]** §VI.4(2). High and low bytes must be written together or a transient wrong duty/frequency occurs **[DS]** §V.2.

### 3.5 Timer

| Addr | Name | Access | Function |
|---|---|---|---|
| `0x38`–`0x3B` | `TIM_CNT_BYTE_0..3` | R/W | Countdown in **seconds**, 31-bit (`0x3B[6:0]`), max **214 748 364 s** ≈ 6.8 years |
| `0x3C` | `TIM_CFG` | R/W | `[3]` `ARM` (self-clearing at zero), `[2:0]` `ACTION` |
| `0x3D` | `TIM_KEY` | W | Write **`0xA5`** to reload |

`ACTION` truth table **[DS]** Table 4, p. 20: `000` stop · `001` set wake flag · `010` system restart · `011` **system power on** · `100` system power off.

`TIM_ACTION_POWERON` is the mechanism behind "shut down and come back in N seconds" — the M5PM1 stays alive on `L0` while everything else is off. **[DOC]**

### 3.6 Interrupts and button

| Addr | Name | Access | Function |
|---|---|---|---|
| `0x40` | `IRQ Status 1` | R/W | `[4:0]` GPIO4–0 level-change flags. **Set by hardware, cleared only by the user** |
| `0x41` | `IRQ Status 2` | R/W | `[5]` battery remove, `[4]` battery add, `[3]` 5VINOUT remove, `[2]` 5VINOUT add, `[1]` 5VIN remove, `[0]` 5VIN add — all thresholded at **2400 mV** |
| `0x42` | `IRQ Status 3` | R/W | `[2]` double-click, `[1]` wakeup, `[0]` single-click |
| `0x43` / `0x44` / `0x45` | `IRQ Status 1/2/3 Mask` | R/W | 1 = masked |
| `0x48` | `BTN_Status` | R | `[7]` `BTN_Event` (press occurred; **cleared on read**), `[0]` `BTN_Status` (1 = currently pressed) |
| `0x49` | `BTN_CFG_1` | R/W `0x2A` | `[7]` `DL_LOCK` (1 = disable Download mode), `[6:5]` double-click window (125 ms / 250 ms / 500 ms / 1 s), `[4:3]` long-press (1/2/3/4 s), `[2:1]` single-click window, `[0]` `SINGLE_RESET_DIS` |
| `0x4A` | `BTN_CFG_2` | R/W `0x00` | `[0]` `DOUBLE_POWEROFF_DIS` |

### 3.7 NeoPixel, audio pulse and retention RAM

| Addr | Name | Access | Function |
|---|---|---|---|
| `0x50` | `NEO_CFG` | R/W | `[6]` `REFRESH`, `[5:0]` LED count 0–32 (0 = driver off) |
| `0x53` | `AW8737A PULSE` | R/W | `[7]` REFRESH, `[6:5]` pulse count 0–3, `[4:0]` target GPIO 0–4 |
| `0x60`–`0x9F` | `NEO_PIXn_L/H` | R/W | 32 × RGB565, 64 bytes |
| `0xA0`–`0xBF` | `RTC_MEM` | R/W | **32 bytes of retention RAM** |

The retention RAM survives *the ESP32's* power-off, **not** the M5PM1's: "M5PM1 power-off does not retain data" **[DS]** §IV.11.

`0x53` drives an **AW8737A** audio power amplifier by counting pulses on a GPIO. No amplifier appears in the PaperMono specification — only a buzzer and a PDM microphone — so this register is most likely a generic firmware feature unused on this board. **[INF]**; the same feature exists in the sibling [M5IOE1](../m5ioe1/README.md) at `0x90`.

---

## 4. Behaviours you have to know before writing code

### 4.1 The first I²C transaction after idle sleep always fails

**[DS]** §IV.1(10) note 2, restated on the vendor API page **[DOC]**:

> After the idle-sleep function is configured and triggered, M5PM1 enters sleep. If woken via I²C, **the first I²C transaction is used only for wake-up and will fail.** Subsequent communications operate normally. Within **300 ms** after that first wake transaction, if M5PM1 does not receive a complete address it will sleep again.

Idle sleep is **not self-clearing** — once `I2C_CFG[3:0]` is set, only the user can clear it. Wake-up is driven by a **fixed 100 ms internal timer that cannot be changed** **[DS]** §V.7 note. Idle sleep is also **disabled outright while any PWM channel is enabled**, and in Download mode **[DS]** §V.6 note.

### 4.2 IRQ is a wired-OR, and clearing it is all-or-nothing

**[DS]** §V.8. When *any* GPIO is configured as an IRQ pin (`GPIO_FUNC` = `01`):

- The IRQ pin is pulled **low** while `IRQ Status 1`, `2` **or** `3` is non-zero, and is released **only when all three are clear**.
- Configuring an IRQ pin also switches on scanning of the *other* GPIOs (those with `GPIO_FUNC` = `00`, `GPIO_MODE` = 0) and of power events. Nothing is scanned if no IRQ pin exists.
- Conversely, **when no GPIO is an IRQ pin, all three status registers are cleared** — including by a reset or by entering Download mode, since both reset the GPIO configuration.

The last point is a trap: if you need `IRQ Status 3[1] WAKEUP` after a reset, **do not clear `WAKE_SRC` (`0x05`)** until you have re-armed a GPIO as IRQ, or the wakeup interrupt can never fire **[DS]** §IV.6 "IRQ Attention" 2 / §V.8(4).

### 4.3 Driving NeoPixels resets the I²C peripheral

Setting `IO0` to its mux function makes the firmware **switch the core clock to 24 MHz** for RGB timing, and "switching the clock will reset I²C, so you must wait before communicating; otherwise communication will fail" **[DS]** §VI.2(2)1. During a refresh, interrupts are disabled and **32 LEDs take ≈ 7 ms** with I²C blocked throughout **[DS]** §IV.8. Only `IO0` supports NeoPixel.

### 4.4 Power button semantics

**[DS]** §V.3: **single click = reset, double click = power off, long press = enter Download mode**, with the intervals set by `BTN_CFG_1`. Both destructive behaviours can be disabled (`SINGLE_RESET_DIS`, `DOUBLE_POWEROFF_DIS`), and when they are, the same gesture instead raises an interrupt in `IRQ Status 3` **[DS]** §IV.6(3).

On power-off the 3.3 V DC/DC and `LED_EN` go off but **charging is unaffected** **[DS]** §V.3(1).

### 4.5 Low-voltage protection latches

When neither 5VIN nor 5VINOUT is present and the battery falls below `BATT_LVP`, the system powers off automatically. To leave the low-voltage standby loop, the battery must exceed **`BATT_LVP` + 100 mV** — or 5VIN/5VINOUT must be inserted **[DS]** §V.5, §IV.1(9).

Related trap: **with charging enabled and no battery fitted, the battery ADC floats** and power-source detection becomes unstable. The manual recommends disabling charging when no battery is present **[DS]** §IV.1(5) note 2.

### 4.6 LED blink codes

`LED_EN` is driven by internal logic and its blink rate is a status indication **[DS]** §V.4(2):

| Pattern | Meaning |
|---|---|
| Flashes once | Reset occurred |
| Flash every **500 ms** | Download mode |
| Flash every **200 ms** | Button reset disabled **and** a GPIO has IRQ enabled |
| Flash every **100 ms** | Double-click power-off disabled **and** a GPIO has IRQ enabled |

---

## 5. Libraries

| Option | Where | Verdict |
|---|---|---|
| **`M5PM1`** — M5Stack's own dual Arduino/ESP-IDF driver | `github.com/m5stack/M5PM1`, ESP-IDF registry `m5stack/m5pm1`, latest **1.0.7**; MIT | ✅ **Use this.** `src/M5PM1.h` is a bilingual annotated copy of the whole register map — 136 KB of it — and is more usable than the PDF **[SRC]** |
| Raw I²C | — | Viable; the map above is complete. Mind the burst-range limits (§3) |
| M5Unified | `M5Unified` `Power_Class` | Only partially wraps the part; M5GFX reaches the PMIC directly for the frontlight **[SRC]** `M5GFX/src/M5GFX.cpp:819-856` |

Version pinned by the PaperMono factory firmware: **`m5stack/m5pm1` 1.0.7** **[SRC]** `M5PaperMono-UserDemo/dependencies.lock`.

Representative API surface **[DOC]**:

```
pm1.begin(&M5.In_I2C, M5PM1_DEFAULT_ADDR, M5PM1_I2C_FREQ_100K)
pm1.setLdoEnable(bool) / setDcdcEnable(bool) / ldoSetPowerHold(bool)
pm1.shutdown() / setSingleResetDisable(bool) / setLedEnLevel(bool)
pm1.timerSet(uint32_t seconds, m5pm1_tim_action_t action)
pm1.setI2cSleepTime(uint8_t seconds)
pm1.gpioSetMode / gpioSetPull / gpioSetDrive / gpioSetFunc / gpioSetOutput
pm1.gpioSetWakeEnable(M5PM1_GPIO_NUM_n, bool)
pm1.gpioSetWakeEdge(M5PM1_GPIO_NUM_n, M5PM1_GPIO_WAKE_FALLING)
pm1.analogRead(M5PM1_ADC_CH_n, &v) / readTemperature(...) / readVref(&v)
pm1.setPwmFrequency(hz) / setPwmDuty(M5PM1_PWM_CH_n, pct, pol, en)
pm1.setLeds(rgb*, n, count, refresh)
pm1.irqClearGpioAll / irqClearSysAll / irqClearBtnAll / irqSetGpioMask...
```

---

## 6. ⚠ Pin-numbering: M5PM1 is 0-based and label-matching — its sibling is not

> **This is the single most damaging trap on any board carrying both M5Stack expanders.**
>
> | Part | Enum | Value | Rule |
> |---|---|---|---|
> | **M5PM1** | `M5PM1_GPIO_NUM_3` | **`3`** | 0-based; **label equals value** — **[SRC]** `M5PM1/src/M5PM1.h:404-412`, specifically `M5PM1_GPIO_NUM_3 = 3` at `M5PM1.h:410` |
> | [**M5IOE1**](../m5ioe1/README.md) | `M5IOE1_PIN_3` | **`2`** | Label is **1**-based, enum value is **0**-based — **[SRC]** `M5IOE1/src/M5IOE1.h:34` |
>
> Two expanders on the same I²C bus with **different label↔value conventions**. Passing a documentation "`PYGn`" number straight into the M5IOE1 API silently targets pin *n+1*'s neighbour. The M5Stack OTP demo bypasses the M5IOE1 enum entirely and hardcodes raw values with the comment `// M5IOE1 uses zero-based pin indexes.` **[SRC]** `M5PaperMono-OTP-Demo/components/EDP_OTP_LUT_demo/src/EDP_SPI.cpp:36-38`.
>
> The hazard is not symmetric: M5PM1 code written from the label is correct, M5IOE1 code written from the label is off by one. But the two chips sit side by side in the same vendor documentation, so the reader has to know which convention applies to which part.

A second, related notation hazard: **M5Stack's own documentation applies the `PYGn` prefix to M5PM1 pins, which have no such prefix.** `PYG3_BL_PWM` on the product page denotes **M5PM1 GPIO3**, while `PYG3` in the IO-expander context denotes **M5IOE1 IO3 = e-paper power enable**. Writing to the wrong one cuts power to the display instead of dimming the frontlight. The M5PM1 header contains **no `PYG` identifier at all** **[SRC]** `M5PM1/src/M5PM1.h`; the shipped firmware writes `PM1 G4`, not `PYG4` **[FW]**.

---

## 7. Caveats, errata and internal inconsistencies in the manual

| # | Issue | Evidence |
|---|---|---|
| **C1** | **PWM channels are numbered inconsistently within the same document.** Table 2 (p. 3) labels the `IO3` mux **`PWM1`** and the `IO4` mux **`PWM2`**; the register map and §IV.4 call the same two channels **`PWM0`** and **`PWM1`**; §VI.4's example maps `M5PM1_PWM_CH_0` → GPIO3 and `M5PM1_PWM_CH_1` → GPIO4. **Take the register/API numbering (0-based) as operative**; the Table 2 column is the outlier | **[DS]** Table 2 vs §IV.4 vs §VI.4; corroborated by **[SRC]** `M5PM1.h` comment "GPIO3 (can be PWM0)" |
| **C2** | **`PWM0_HC` and `PWM1_HC` both describe themselves as "PWM1 duty cycle high 8 bits"** — and "high 8 bits" is wrong in both cases; the field is `[3:0]`, four bits. Copy-paste defect in the register table | **[DS]** Table 3, p. 8 |
| **C3** | **The NeoPixel buffer note contradicts the register map.** Table 3 places `NEO_PIXn_L/H` at `0x60–0x9F`, but §IV.10's note says "PIX0_L = 0x36, PIX0_H = 0x37, …, PIX31_H = 0x75". `0x36` is a *reserved* address in the same table. The `0x60–0x9F` range is the one the library uses | **[DS]** Table 3 p. 10 vs §IV.10 p. 25; **[SRC]** `M5PM1.h` `M5PM1_REG_NEO_DATA_START` = `0x60` |
| **C4** | **The appendix cites register addresses that no longer exist.** The firmware changelog refers to "GPIO_Power_Hold register (**0x33**)", "IRQ Status 3 (**0x23**)", "BTN_CFG_2 (**0x31**)" and repeatedly to "WAKE_SRC (**0x2F**)". In the current map these are `0x07`, `0x42`, `0x4A` and `0x05`. The addresses moved at `HW:5 / SW:6` ("Updated the register map") and the historical entries were not renumbered. **Use Table 3, not the appendix** | **[DS]** pp. 32–33 vs Table 3; the `0x2F` reference also leaks into §IV.6(3) on p. 21 |
| **C5** | **`SW_REV` default disagrees with the changelog.** Table 3 gives `SW_REV` default `0x06` (firmware V6, doc V1.7, 2025-12-13), but the latest changelog entry is `HW:5 / SW:S` (2026-01-06) — firmware version "S" as ASCII. The register-map default was not updated. **Read `0x03` from the device rather than assuming either** | **[DS]** Table 3 p. 4 vs appendix p. 33 |
| **C6** | **§V.1(2) lists "5VOUT" twice and never 5VIN**, so one of the three internal ADC channel descriptions is mislabelled | **[DS]** p. 26 |
| **C7** | **`I2C_CFG` bit `[7:5]` is called `DBL` in §IV.1(10)** but `Reserved` in Table 3. `DBL` is the `BTN_CFG_1` field name — a copy-paste from the button section | **[DS]** Table 3 p. 5 vs §IV.1(10) p. 14 |
| **C8** | **`IRQ Status 2[3]` "5VINOUT Remove" and `[2]` "5VINOUT Add" carry identical threshold text** ("voltage ≤ 2400 mV → > 2400 mV") in both the status and mask sections, so the Remove condition is printed backwards. §V.8's power-event list gives the correct Remove condition (`≥ 2400 mV → < 2400 mV`) | **[DS]** §IV.6(2)/(5) pp. 21–22 vs §V.8(3) p. 28 |
| **C9** | **No electrical specification whatsoever.** No V<sub>CC</sub> range, no absolute maximum ratings, no I/O drive strength, no quiescent current, no timing. The only limit stated anywhere is the 3.3 V ADC input ceiling. This is a real gap for anyone designing with the part rather than merely programming a fitted one | **[DS]** whole document |
| **C10** | **`5VOUT` is bidirectional and mis-sequencing it is a hardware hazard.** "Before enabling the 5VOUT boost, the 5VOUT voltage must be detected first to ensure there is no external power input; otherwise it should remain in input mode." Enabling a boost converter into an externally driven rail is exactly the kind of thing that damages parts | **[DS]** §V.1(2) *Attention* 1 |

Additionally: the **M5PM1 library's LICENSE is dated 2025** while every other PaperMono repository is dated 2026, which is consistent with the part predating this board and being reused across M5Stack products **[SRC]**; `product_i2c_addr` on `docs.m5stack.com` lists `M5PM1 (0x6e)` for the **StickS3 (K150)**, independently confirming the address on a different product **[DOC]**.

---

## 8. Used By

### [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) — designator `U7`, sheet 2

> **FCC label exhibit and internal photographs — 2026-09-20.** M5Stack filed its
> full architecture diagram as the FCC "ID Label" exhibit for
> `2AN3WM5PAPERMONO`
> ([retained here](../../../devices/m5stack/papermono/artifacts/certification/2AN3WM5PAPERMONO-label-and-label-location.pdf)).
> It independently confirms, from a source other than the schematic:
>
> - **I²C address `0x6E`**, and the host interrupt on **`G1`**
> - **`PM_G0`** ← RX8130 RTC interrupt · **`PM_G4`** ← BMI270 IMU interrupt —
>   both landing here rather than on the ESP32-S3, which is the mechanism behind
>   deep-state wake
> - **`PM_G3`** → frontlight PWM · **`PM_LED`** → the RGB LED's red channel
> - **`PM_L1_EN`** → the `3V3_L1` LDO · **`PM_L2_EN`** → the `3V3_L2` JW5712 buck
> - **`PM_5VIN_ADC`**, **`PM_BAT_ADC_EN`**, **`PM_BAT_ADC`**, `Btn_PWR`
> - The part numbers this record's power tree depends on: `SSP7615` LDOs
>   (including the `3V3_L0` one marked **"AlwaysOn"**), `JW5712` buck,
>   `IP2315` charger, `AW32901` on the USB input
> - **Power-button semantics**, matching §4.4 exactly:
>   **Press = ON/RST · Double = OFF · HOLD = BOOT**
> - **`CHG CURRENT = 500 mA`** — see
>   [C18](../../../devices/m5stack/papermono/gaps-and-conflicts.md#c18--ip2315-charge-current-cannot-be-read-from-the-datasheet-table),
>   which this **does not resolve**: the schematic annotates `0.5C` ≈ 575 mA, so
>   there are now two M5Stack figures and no measurement
>
> **SWD is broken out to test pads.** The internal-photograph exhibit shows the
> main board's bottom side carrying **`SWD1`/`SWC1`/`RESET1`** and
> **`SWD2`/`SWC2`/`RESET2`** — one pair for this part, one for the
> [M5IOE1](../m5ioe1/README.md). Also present: `SOC_BOOT`, `SOC_RST`, `Tx`,
> `Rx`, `GND`, `VBUS_L0`, and all four switched rails `3V3_L0`, `3V3_L1`,
> `3V3_L2`, `3V3_L2_LoRa`.
>
> ⚠ **Untested and risky.** Which SWD pair belongs to which chip is **not
> marked**. Nothing has been probed. This part owns the ESP32-S3's reset and boot
> straps, so attaching a debugger to it while the board is live is a plausible
> route to bricking it — see
> [`development.md`](../../../devices/m5stack/papermono/development.md). Status:
> `not-tested`, `inferred` from silkscreen only.
> [`certification.md` §6](../../../devices/m5stack/papermono/certification.md#the-test-pad-census-on-the-bottom-side).

The M5PM1 is the **only always-on active device** on the board. It sits on rail `L0` (straight off the battery, alongside the RTC) and every other rail exists downstream of a pin it controls. Consequences for the board specifically:

| Role on PaperMono | Pin / register | Evidence |
|---|---|---|
| System I²C slave at `0x6E`, on the shared internal bus **GPIO47 = SDA, GPIO48 = SCL**, brought up at 100 kHz | pins 8/9 → `G47_SYS_SDA` / `G48_SYS_SCL` | **[SCH]** `U7`.8, `U7`.9; **[SRC]** `hal_board.cpp:13,15` |
| **`L1` rail enable** (powers the BMI270 IMU) | pin 18 `LDO_3V3_EN` → `3V3_L1_EN`; `pm1.setLdoEnable()` | **[SCH]** `U7`.18; **[DOC]** |
| **`L2`/`L3A` rail enable** (powers the ESP32-S3, LoRa, NFC, the M5IOE1 itself, button pull-ups, touch INT, buzzer, RGB red) | pin 14 `DCDC_3V3_EN` → `3V3_L2_EN`; `pm1.setDcdcEnable()` | **[SCH]** `U7`.14; **[DOC]** |
| **Battery charge enable** to the AW32901/IP2315 charging path | pin 2 `CHG_EN` | **[SCH]** `U7`.2; **[SCH]** sheet 1 power-tree block |
| **Battery / 5 V-in / 5 V-out monitoring**, and the battery-sampling enable | pins 11, 16, 19, and pin 1 `BAT_ADC_EN` | **[SCH]** `U7`.1/.11/.16/.19 |
| **ESP32-S3 `BOOT` strap**, open-drain | pin 15 `BOOT_OUT` → net `G0_BOOT_OUT` → ESP32-S3 `GPIO0[strap]` | **[SCH]** `U7`.15 and sheet 1 I/O map. ⚠ **Not exercised by the factory firmware** — `grep -rE 'GPIO_NUM_0\b' main/` returns only `M5PM1_GPIO_NUM_0` hits **[SRC]**, so this net's behaviour is documented but unverified |
| **Power button**, the board's single multi-function ON/OFF/RESET/BOOT control | pin 7 `PWR_BTN` | **[SCH]** `U7`.7 |
| **Red channel of the status LED** | pin 5 `LED_EN` → `PY_LED_R` | **[SCH]** `U7`.5. Green/blue come from the M5IOE1 instead |
| `IO0` = **RX8130CE RTC interrupt**, used as a wake source (falling edge) | `PYG0_RTC_INT` | **[SCH]** `U7`.3; **[SRC]** `app_sleep_wake.cpp:67`; **[FW]** `PM1 shutdown, wake by RX8130 timer -> PM1 G0 falling edge` |
| `IO1` = **IRQ output toward the host**, wired to ESP32-S3 **GPIO1** | `G1_PY_IRQ` | **[SCH]** `U7`.17; **[SRC]** `app_sleep_wake.cpp:46,69` |
| `IO2` = **LoRa module power enable** (gates `3V3_L2_LoRa`) | `PYG2_LoRa_EN` | **[SCH]** `U7`.20; **[SRC]** `hal_lora.cpp:29` |
| `IO3` = **frontlight PWM** (PWM0), 5 kHz, gamma-squared brightness curve | `PYG3_BL_PWM` | **[SCH]** `U7`.13; **[SRC]** `M5GFX/src/M5GFX.cpp:826-853` |
| `IO4` = **BMI270 IMU interrupt**, wake source, **active-low / falling edge** | `PYG4_IMU_INT` | **[SCH]** `U7`.12; **[SRC]** `app_sleep_wake.cpp:68`; **[FW]** `PM1 shutdown, wake by BMI270 INT1 -> PM1 G4 falling edge` |

How M5GFX programs the frontlight, exactly **[SRC]** `M5GFX/src/M5GFX.cpp:819-856`:

| Step | Register | Value | Meaning | Line |
|---|---|---|---|---|
| Clear `GPIO_DRV` bit 3 | `0x13` | `bitOff 1<<3` | GPIO3 → **push-pull** (mandatory, see §2 note) | 826 |
| Set `GPIO_FUNC0` | `0x16` | `bitOn 0xC0` | GPIO3 `[7:6]` → `11` = mux (PWM) | 829 |
| Set `PWM_FREQ_L/H` | `0x34`/`0x35` | 5000 | **5 kHz** | 833–836 |
| Brightness off | `0x31` | `0` | disable | 845 |
| Brightness on | `0x30`, `0x31` | `br = brightness²`, `(br>>4)&0xFF`, `(br>>12)\|0x10` | squared/gamma duty; `0x10` is the `EN` bit | 850–853 |

A linear brightness write sits commented out at `M5GFX.cpp:847`, superseded by the squared curve. Note the driver never reads `VREF`, never checks `PWR_SRC`, and never surfaces `IRQ Status 2`'s battery-insert/remove events.

**Not verified on this board:** `BOOT_OUT` (above); the NeoPixel mux on `IO0` (used as an RTC interrupt input instead); the `AW8737A` pulse register; the ADC channels on `IO1`/`IO2` (both used as digital lines).

### [M5Stack PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md)

**Same part, same designator, same wiring** — the Lite drops NFC and LoRa but keeps the entire power tree. `IO2` still drives `PYG2_LoRa_EN` in the shared schematic naming; whether the net is populated on the Lite board is not established here, because M5Stack publishes a 4-sheet `PRJ` PDF for the Lite rather than the 6-sheet `SCH` **[DOC]**.

---

## 9. Related components

- [**M5IOE1**](../m5ioe1/README.md) — the sibling custom expander, same publisher, same PY32 lineage, **different pin-numbering convention** (§6)
- `components/puya/py32l020f15u6/` — the underlying MCU. *Record pending; not yet written at the time of this pass.* Consult it for absolute maximum ratings, supply range and I/O characteristics, none of which the M5PM1 manual provides
- [**Semtech SX1262**](../../semtech/sx1262/README.md) — powered through `IO2`
- [**M5Stack Stamp-LoRa-1262**](../stamp-lora-1262/README.md) — the module carrying that SX1262
- [Vendor sourcing guides index](../../../vendors/README.md) — no M5Stack chip-documentation guide exists yet; the M5PM1/M5IOE1 manuals are reachable only from the product pages' *Datasheets* list and from `docs/` inside the driver repositories

---

## 10. Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/m5pm1-chip-user-manual-v1.9-en.pdf` | 814 731 | `c6daffd0ab89d8de50c0a19f35f94321bc6c9511ad017dd242a3e765d88a96b6` | **M5PM1 Chip User Manual V1.9**, 33 pp., English. PDF metadata: Author `洋 熊`, Creator/Producer `Microsoft® Word 2021`, created **2026-05-22**. Text layer validated against the rendered page headings before any value here was transcribed |
| `artifacts/m5pm1-chip-user-manual-en-github-M5PM1-repo-2026-02-04.pdf` | 828 393 | `f008794c8a6b672b61452c77a9359b6332d82194dce92f9a21494e283783b656` | **Same manual, earlier export, English** — the copy shipped in `docs/` of the `m5stack/M5PM1` driver repo. Word 2021, created **2026-02-04**. Retained because it is **not** byte-identical to the docs-site copy and **is missing a behavioural note** — see §10.1 |
| `artifacts/m5pm1-chip-user-manual-cn-github-M5PM1-repo-2026-02-04.pdf` | 1 063 504 | `38ea524938d923d829c5771f0a0b080be1e05ca00c2f60fa2f1a31257f20b9b8` | **Chinese edition**, 33 pp., Word 2021, created **2026-02-04**, from the same repo. Closes the open item below |

### 10.1 ⚠ Two different M5Stack-published English exports — one is missing a register note

*Added 2026-09-20.* M5Stack publishes this manual from **two** places, and they are **not the
same file**:

| Source | Bytes | SHA-256 (16) | Created | Pages |
|---|---:|---|---|---:|
| `static-cdn.m5stack.com/.../1207/M5PM1_Datasheet_EN.pdf` (docs site) | 814 731 | `c6daffd0ab89d8de` | 2026-05-22 | 35 |
| `github.com/m5stack/M5PM1` → `docs/M5PM1_Datasheet_EN.pdf` | 828 393 | `f008794c8a6b672b` | 2026-02-04 | 35 |

Both carry the **same revision history**, ending at `HW:5 / SW:6` — so neither is a newer
*specification*. The text differs by only 173 bytes out of ~98 800, almost all of it reflow.
**One difference is substantive**, and it is a trap:

> **The docs-site copy contains this note on the wake-up-source register; the GitHub copy does
> not contain it anywhere in the document.**
>
> > *"Note: Writing to this register can only clear the flag bit to ensure valid detection of
> > the wake-up source the next time; it cannot specify a wake-up source."*

Verified by full-text search: the string `wake-up source` occurs **twice** in the docs-site
export and **zero** times in the GitHub export.

**Consequence.** A reader working from the copy bundled with the driver library — the copy most
likely to be opened, since it arrives with the code — has no warning that this register is
**write-to-clear only**. Writing a bit pattern to select a wake source does nothing. Cite the
**docs-site copy** (`…v1.9-en.pdf`) for anything touching wake sources.

This also corrects the licence note below, which said the driver library "ships the same PDF in
`docs/`". **It does not** — it ships a different export.

### 10.2 The Chinese edition — retrieved, and substantively equivalent

*Added 2026-09-20. This closes the open item that previously read "A Chinese-language edition
exists and was not retrieved … the highest-value untaken lead."*

The CN edition was found already present in `docs/` of the `m5stack/M5PM1` repo clone and is now
retained at `artifacts/m5pm1-chip-user-manual-cn-github-M5PM1-repo-2026-02-04.pdf`.

**It does not settle the §7 nomenclature inconsistencies, because it does not differ in
substance.** Language-independent comparison: the CN and EN exports contain the **same 85
distinct `0xNN` register-address tokens**, and the CN is 33 pp against the EN's 35 pp with the
difference being typographic. The EN text's untranslated Chinese fragments (`低 8 bit`,
`电池移除`, `唤醒源二选一`) are therefore not evidence of a richer Chinese original — they are
an incomplete translation pass over the same content.

**The English copy remains the primary source for this part.** The CN is retained because the
two are not byte-identical and because recording *that the lead was followed and yielded
nothing* is worth more than leaving it open. Negative result, dated.

**Text-layer validation.** `pdftotext -layout` output was cross-checked against the document's own running headers (`M5PM1 Chip User Manual`), footers (`n / 33`, `The Innovator of Modular IoT Development Platform | M5Stack`) and section numbering before transcription. No glyph-subsetting or code-point-offset corruption was observed. Some cells retain untranslated Chinese (`低 8 bit`, `电池移除`, `唤醒源二选一`), which is a property of the source document, not of the extraction.

**A Chinese-language edition exists and was not retrieved.** The `zh_CN` product page links `1207/M5PM1_Datasheet_CN.pdf` where the `en`/`ja` pages link `M5PM1_Datasheet_EN.pdf` **[DOC]**. Since these two are the only vendor documentation of this part at all, a CN↔EN diff is the highest-value untaken lead — it would likely settle the nomenclature inconsistencies in §7. Recorded as an open item rather than a gap.

> ✅ **Superseded 2026-09-20 — the lead was taken and came back empty.** The CN edition is now
> retained (§10.2). It is **substantively equivalent** to the English and does **not** settle
> §7. Leaving the paragraph above in place so the reasoning is visible, but do not re-open it.

**Licence.** M5Stack copyright, no licence statement on the document. Redistribution status **`unknown`**; disposition `repository`. The driver library that ships the same PDF in `docs/` is MIT, but that licence covers the code, not the manual.

---

## 11. Authoritative sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | M5PM1 Chip User Manual | **M5Stack** (imprint: Shenzhen Mingzhan Information Technology Co., Ltd.) | primary | chip manual | `artifacts/m5pm1-chip-user-manual-v1.9-en.pdf`; upstream `static-cdn.m5stack.com/resource/docs/products/core/PaperMono/1207/M5PM1_Datasheet_EN.pdf` | 2026-09-01 | **V1.9, 2026-01-22** | §1–§5, §7 |
| S-2 | PaperMono schematic | M5Stack | primary | schematic PDF | `PaperMono_SCH_V0.6.2_20260522.pdf` (held in the device tree) | 2026-09-01 | **V0.6.2, 2026-05-22**, 6 sheets | §1 silicon identity (sheet 1), §2 pin table (sheet 2 `U7`), §8 wiring |
| S-3 | `M5PM1` Arduino/ESP-IDF driver | M5Stack | primary | source | `github.com/m5stack/M5PM1` @ `be9a5456c007c333e7ac963f33bfde1ffa5d82ee` | 2026-09-01 | tag **1.0.7**, MIT | §3 symbol names, §6 enum values |
| S-4 | `M5PaperMono-UserDemo` factory firmware source | M5Stack | primary | source | `github.com/m5stack/M5PaperMono-UserDemo` @ `c1099107271d31a0678d661a896e2b04dbb331ea` | 2026-09-01 | 2026-08-10, MIT | §8 board roles |
| S-5 | `M5GFX` | M5Stack | primary | source | `github.com/m5stack/M5GFX`, `master` @ `d91077b9a607b59404e4e4a49f775c792bfae382` | 2026-09-01 | release 0.2.28 | §8 frontlight sequence |
| S-6 | PaperMono product page + `arduino/papermono/m5pm1_m5ioe1` API page | M5Stack | primary | vendor docs | `docs.m5stack.com/en/core/PaperMono`, `docs.m5stack.com/en/arduino/papermono/m5pm1_m5ioe1` | 2026-09-01 | undated | §5 API surface, §6 notation hazard, §8 power tree |
| S-7 | `C153-PaperMono-ESP32S3R8-UserDemo-V1.2` firmware image | M5Stack via M5Burner | primary | binary | firmware id `2089640807996628993`, SHA-256 `72c290bc2ffa216041b276660277369bd17ecef92315e367d98bb2c96c8428fa` | 2026-09-01 | v1.2, built 2026-08-06, IDF v5.5.1 | §6, §8 wake-source strings |
| S-8 | `product_i2c_addr` reference table | M5Stack | primary | vendor docs | `docs.m5stack.com/en/product_i2c_addr` | 2026-09-01 | undated | §7 — independent `0x6E` confirmation via StickS3 (K150); **negative result:** PaperMono itself is absent from this table |
