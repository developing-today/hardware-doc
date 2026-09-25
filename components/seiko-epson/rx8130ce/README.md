# Seiko Epson RX8130CE

- **Category:** I²C **real-time clock / calendar module** with a built-in, frequency-adjusted 32.768 kHz crystal, wakeup timer, alarm, time-update interrupt, FOUT clock output, reset output, 4 bytes of user RAM, a digital offset trim, and an **integrated backup-supply switchover and battery-charge controller**
- **I²C address:** **`0x32`** (7-bit, fixed; write byte `0x64`, read byte `0x65`). No address-select pin
- **Package:** 10-terminal ceramic module; Epson product number **`X1B000311000100`**
- **Research status:** the **full Epson application manual is retained in two revisions** — the M5Stack mirror (`ETM50E-09`, 70 pp) and Epson's current `ETM50E-10`, both read end to end and diffed. The PaperMono schematic symbol was parsed pin-by-pin, and M5Unified's `RX8130_Class` driver was audited against the manual. No hardware was in the loop.
- **Retrieved:** 2026-09-01

The real-time clock of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) and, identically, of the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md) (C153-LITE). The board-specific fact that matters is that its **interrupt output does not reach the ESP32-S3 at all** — it goes to the [M5PM1](../../m5stack/m5pm1/README.md) power manager, which is what lets an alarm wake a board whose application processor is unpowered.

---

## ⚠ The document filed here as "Chinese" is in English

This needs stating before anything else, because the repository's own source table, the device record and this record's own filename all say otherwise.

The artifact `artifacts/rx8130ce-register-datasheet-cn-m5stack-mirror.pdf`, mirrored by M5Stack as `RX8130CE_cn-Register-Datasheet.pdf`, **is the English-language Epson application manual `ETM50E-09`**, cover to cover. `executed-success` — the full 70-page text layer was extracted and read.

The cause was traced to Epson, not to M5Stack. **Epson's own download server serves the English manual under a `_cn` filename:**

| Epson URL | Bytes | SHA-256 | Language |
|---|---:|---|---|
| `https://download.epsondevice.com/td/pdf/app/RX8130CE_en.pdf` | 2 008 845 | `db027a5f…` | **English**, `ETM50E-10` |
| `https://download.epsondevice.com/td/pdf/app/RX8130CE_cn.pdf` | 2 008 853 | `0ff562f2…` | **English**, `ETM50E-10` — same document, 8 bytes of metadata apart |
| `https://download.epsondevice.com/td/pdf/app/RX8130CE_ja.pdf` | 2 986 434 | `32913ca0…` | **Japanese**, `ETM50J-10`, 64 pp |

So at Epson the `_cn` suffix means **"served on the China site"**, not "Chinese language". M5Stack mirrored that file and kept the suffix. All three verified `HTTP 200` on 2026-09-01.

**Therefore, on the repository's multi-language policy:**

- The copy held **is** the English edition. There is no separate English equivalent to go and get, and no translation-equivalence question to answer, because no Chinese-language edition of this manual was found to exist anywhere — not at Epson, not at M5Stack.
- A **Japanese** edition (`ETM50J-10`) does exist and is a genuinely independent document — 64 pages against the English 70, and the English text still carries an untranslated Japanese figure caption (`初回周期誤差`, "first-cycle error", in Figure 20 **[DS-09]** p. 28), which shows the English is a translation of the Japanese original. It is recorded **reference-only** with size, hash and URL in [§12](#12-local-artifacts) rather than retained, since the English is authoritative for this repository's readers and the file is freely re-fetchable from a stable vendor URL.
- **Epson's current revision was retrieved and is now held beside the mirror** (§12). It is **`ETM50E-10`, 2026-01-30** — the M5Stack mirror is **one revision behind**, and the difference runs the *unexpected* way; see [§11-C1](#11-caveats-errata-and-a-driver-audit).

The filename of the mirror is left unchanged, because renaming it would break the hash-and-path chain recorded in [`devices/m5stack/papermono/sources.md`](../../../devices/m5stack/papermono/sources.md) S22. The mislabelling is documented instead.

---

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[DS-09]** | Stated in `artifacts/rx8130ce-register-datasheet-cn-m5stack-mirror.pdf` (`ETM50E-09`), with section/table reference | `not-tested` — manufacturer specification reproduced; nothing measured |
| **[DS-10]** | Stated in `artifacts/rx8130ce-application-manual-etm50e-10-en-epson.pdf` (`ETM50E-10`, Epson's current) | `not-tested` |
| **[SCH]** | Read out of `PaperMono_SCH_V0.6.2_20260522.pdf`, **sheet 4**, designator `U16` | `executed-success` for the extraction (all 10 pads enumerated from the text-position layer); `not-tested` electrically |
| **[SRC]** | Read out of M5Stack source at a cited `file:line` | `executed-success` for the read; `not-tested` on hardware |
| **[DOC]** | `docs.m5stack.com`, retrieved 2026-09-01 | `not-tested` |
| **[FW]** | String recovered from the shipped factory firmware binary | `executed-success` for the extraction |
| **[INF]** | Inference | `inferred` |

Unless marked **[DS-10]**, register and electrical values are quoted from `ETM50E-09`, the revision the board's software was written against; the two revisions agree on every value in this record (§11-C1).

**Text-layer validation.** Both PDFs were checked against their own running headers (`RX8130CE`, `ETM50E-09` / `ETM50E-10`) and page footers before transcription; the two were then normalised and diffed against each other, which is a stronger check than either alone. No glyph subsetting or code-point offset was observed. Residual Japanese in figure captions is a property of the source document, not the extraction.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Seiko Epson Corporation** | **[DS-09]** cover |
| Part | **RX8130CE**, "Build-in backup battery charge control function / SERIAL-INTERFACE REAL TIME CLOCK MODULE" | **[DS-09]** §1 |
| Epson product number | **`X1B000311000100`** | **[DS-09]** cover |
| Document | **Application manual `ETM50E-09`**, 70 pp, revision dated **2025-06-30** | **[DS-09]** cover, revision history |
| Epson's current document | **`ETM50E-10`**, 70 pp, revision dated **2026-01-30** | **[DS-10]** |
| I²C address | **`0x32`** — slave address bits `0110010` + R/W | **[DS-09]** §19.4; **[SRC]** `hal_board.cpp:17` (`RX8130_ADDR = 0x32`) |
| I²C speed | up to **400 kHz** | **[DS-09]** §1; **[SRC]** `hal_board.cpp:19` (`RX8130_I2C_FREQ_HZ = 400000`) |
| Reference | **built-in, frequency-adjusted 32.768 kHz crystal** — no external crystal, no load capacitors | **[DS-09]** §1 |
| Operating voltage | **1.6 – 5.5 V** (`VDD`); **1.1 – 5.5 V** timekeeping | **[DS-09]** §1, Table 5 |
| Interface supply `VIO` | **1.6 – 5.5 V**, independent of `VDD` | **[DS-09]** Table 5 |
| Reference designator on PaperMono | **`U16`, sheet 4** | **[SCH]** |
| ⚠ Marking verified? | **No.** No teardown photograph of `U16` was inspected; identity rests on the schematic's value string | **[INF]** |

### 1.1 Accuracy

**[DS-09]** Table 4, at V<sub>DD</sub> = 3.0 V:

| Parameter | Value |
|---|---|
| Output frequency | 32.768 kHz |
| **Frequency stability at +25 °C** | **±5 × 10⁻⁶** (Epson prints "5 ± 23 × 10⁻⁶" for the ±23 ppm bin — the datasheet's own note reads "monthly error is equal to 60 s Max., excluding offset") |
| Frequency vs. voltage, 1.1–5.5 V | −2 to +2 × 10⁻⁶ per volt |
| **Frequency vs. temperature**, −20…+70 °C | **−120 to +10 × 10⁻⁶** |
| Ageing, first year at +25 °C | ±5 × 10⁻⁶ / year |
| Oscillation start time `t_str` | 0.19 s typ., **1.0 s max** |

The temperature coefficient is the number that dominates: **−120 ppm at the edges of the range is roughly −5 minutes per month**, and this is an ordinary (not temperature-compensated) tuning-fork crystal, so the curve is parabolic about ~+25 °C. Anyone expecting minute-per-year accuracy from this part in a pocket device will be disappointed. The digital offset function (§6) can trim a *static* error but not a thermal one.

---

## 2. Pin table

**[DS-09]** §3.1, Table 1. The PaperMono column is **[SCH]** sheet 4 `U16` — all ten pads enumerated.

| Pin | Name | I/O | Datasheet function | PaperMono net **[SCH]** |
|---:|---|---|---|---|
| 1 | `VIO` | P | **Interface supply.** "Connect the same power supply as the MCU" | **`3V3_L0`** — see §2.1 |
| 2 | `SCL` | I | Serial clock input | **`G48_SYS_SCL`** → ESP32-S3 **GPIO48** |
| 3 | `SDA` | I/O | Data input and output | **`G47_SYS_SDA`** → ESP32-S3 **GPIO47** |
| 4 | `FOUT` | O | Frequency output, CMOS. 32.768 kHz / 1024 Hz / 1 Hz, or off | *(no net label — unused)* |
| 5 | `/RST` | O | **N-ch open drain.** Asserted low when `VDD` falls below `VDET1`; released 60 ms after `VDD` rises. **Operates in backup mode too** | via **`R47` 22 Ω / 1 %** |
| 6 | `/IRQ` | O | **N-ch open drain.** Alarm and timer interrupt output. **Can output in backup mode** | **`PYG0_RTC_INT`** → **M5PM1 pin 3 (`IO0`)** |
| 7 | `GND` | P | Ground | `GND` |
| 8 | `VDD` | P | Supply for internal logic | main RTC supply — see §2.1 |
| 9 | `VOUT` | P | **Internal voltage output.** "Connect smoothing capacitor of 1.0 µF" | local, with `R47` |
| 10 | `VBAT` | P | Backup supply pin — EDLC, secondary or primary battery | see §2.1 |

Local passives on sheet 4: **`C60`, `C61`, `C62`, all 1 µF / 25 V**, and **`R49`** on the `PYG0_RTC_INT` net, which is the mandatory pull-up for the open-drain `/IRQ` **[SCH]**.

Datasheet notes worth keeping **[DS-09]** §3.2:

- Input pins accept up to **5.5 V regardless of the `VIO` voltage**.
- The open-drain pins may be **pulled up to 5.5 V regardless of `VIO`**.
- **Leave `FOUT`, `/RST` and `/IRQ` open when unused — do not tie them to GND or `VDD`.**
- A bypass capacitor of at least 0.1 µF is required on every supply pin.

### 2.1 ⚠ Which rail is it on? Two primary sources point different ways

M5Stack's published power-tree table places the RTC on **`3V3_L1`**, the rail enabled by the M5PM1's `LDO_3V3_EN` **[DOC]**, and the device record's [`power-architecture.md`](../../../devices/m5stack/papermono/power-architecture.md) reproduces that: *"L1 Standby — `3V3_L1` — RTC and IMU powered"*.

The schematic's text layer puts **`3V3_L0`** — the always-on rail — on the `VIO` (pin 1) row, and `3V3_L0` also appears beside `R49` on the `PYG0_RTC_INT` net **[SCH]**. Separately, the [M5PM1 record](../../m5stack/m5pm1/README.md) describes the M5PM1 as sitting on `L0` *"straight off the battery, alongside the RTC"*.

**These are not necessarily in conflict, and the part is designed for exactly this.** The RX8130CE has *two* independent supplies — `VDD` for the internal logic and `VIO` for the bus interface — and the manual devotes §4.1 to a "separated power source" configuration in which they differ. A design that puts `VIO` and the `/IRQ` pull-up on the always-on `L0` rail while running `VDD` from switched `L1` is coherent: it keeps the open-drain interrupt able to drive the M5PM1 (which lives on `L0`) while `L1` is down.

**What is not established** is the `VDD` (pin 8) and `VBAT` (pin 10) nets. Neither carried a recoverable net label adjacent to its pad, and the extraction tool recovers *text adjacency, not connectivity* — its own documentation says so. **No net is asserted for `VDD` or `VBAT` here.** Reading the rendered sheet graphically would settle it in minutes, and it is the first thing to check before relying on any statement about this board's behaviour at `L0`.

The consequence, if the vendor table is right about `VDD`: **in state L0 the RTC's logic supply is off and the time is lost**, because there is no coin cell or supercapacitor in evidence — only three 1 µF ceramics, one of which is the manual's required `VOUT` smoothing cap. A 1 µF backup at ~300 nA holds up for well under a second. See [`features/rtc.md` §7](../../../devices/m5stack/papermono/features/rtc.md).

---

## 3. Register map

**[DS-09]** Table 12 (§13.2.1). **The clock and calendar registers start at `10h`, not `00h`.**

| Addr | Function | b7 | b6 | b5 | b4 | b3 | b2 | b1 | b0 |
|---|---|---|---|---|---|---|---|---|---|
| `10` | `SEC` | 0 | 40 | 20 | 10 | 8 | 4 | 2 | 1 |
| `11` | `MIN` | 0 | 40 | 20 | 10 | 8 | 4 | 2 | 1 |
| `12` | `HOUR` | 0 | 0 | 20 | 10 | 8 | 4 | 2 | 1 |
| `13` | `WEEK` | 0 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
| `14` | `DAY` | 0 | 0 | 20 | 10 | 8 | 4 | 2 | 1 |
| `15` | `MONTH` | 0 | 0 | 0 | 10 | 8 | 4 | 2 | 1 |
| `16` | `YEAR` | 80 | 40 | 20 | 10 | 8 | 4 | 2 | 1 |
| `17` | **`MIN Alarm`** | `AE` | 40 | 20 | 10 | 8 | 4 | 2 | 1 |
| `18` | **`HOUR Alarm`** | `AE` | • | 20 | 10 | 8 | 4 | 2 | 1 |
| `19` | **`WEEK`/`DAY Alarm`** | `AE` | 6 / • | 5 / 20 | 4 / 10 | 3 / 8 | 2 / 4 | 1 / 2 | 0 / 1 |
| `1A` | `Timer Counter 0` | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
| `1B` | `Timer Counter 1` | 32768 | 16384 | 8192 | 4096 | 2048 | 1024 | 512 | 256 |
| `1C` | **`Extension Register`** | `FSEL1` | `FSEL0` | `USEL` | `TE` | `WADA` | `TSEL2` | `TSEL1` | `TSEL0` |
| `1D` | **`Flag Register`** | **`VBLF`** | 0 | `UF` | `TF` | `AF` | `RSF` | **`VLF`** | `VBFF` |
| `1E` | **`Control Register 0`** | `TEST` | `STOP` | `UIE` | `TIE` | `AIE` | `TSTP` | `TBKON` | `TBKE` |
| `1F` | **`Control Register 1`** | `SMPTSEL1` | `SMPTSEL0` | **`CHGEN`** | **`INIEN`** | 0 | `RSVSEL` | `BFVSEL1` | `BFVSEL0` |
| `20`–`23` | **User RAM** | — 32 bits, 4 bytes, free for any data — | | | | | | | |
| `30` | `Digital offset` | `DTE` | `L7` | `L6` | `L5` | `L4` | `L3` | `L2` | `L1` |
| `31` | `Extension Register 1` | – | – | – | – | – | – | – | `VBLFE` |

Reset values **[DS-09]** Table 13 — identical after a **software** reset:

| Addr | Value at power-on reset |
|---|---|
| `10`–`16`, `17`–`19`, `1A`, `1B`, `20`–`23` | **undefined** (`X`; normally retains the pre-reset content) |
| `1C` | `0000 0100` → `TSEL2 = 1` |
| `1D` | **`0000 0110`** → **`RSF = 1`, `VLF = 1`** |
| `1E`, `1F`, `30`, `31` | `0000 0000` |

Rules that matter **[DS-09]** Table 12 footnotes:

- Bits printed **`0`** are write-invalid and always read 0. Bits printed **`•`** are free RAM bits. Bits printed **`-`** are TEST bits: **initialise them to 0 and keep them 0.**
- **The `TEST` bit (`1E` bit 7) is a manufacturer test bit. Always write 0.**
- "RTC has different registers not mentioned above table which are programmed by the manufacturer. Please make sure to only access above mentioned user registers." — the software-reset procedure (§7.2) is the sanctioned exception, and it writes to `50h`, `53h`, `66h` and `6Bh`.
- Unused-function registers double as RAM: the alarm registers `17h`–`19h` when `AIE = 0`, the timer counters `1Ah`/`1Bh` when `TE = TIE = 0`.

### 3.1 ⚠ Auto-increment wraps inside 16-byte blocks

**[DS-09]** §19.6:

```
10h -> 1Fh -> 10h
20h -> 2Fh -> 20h
30h -> 3Fh -> 30h
```

A burst that runs off the end of a block **wraps to the start of the same block**; it does not continue into the next. A 7-byte read from `10h` (`SEC`…`YEAR`) is safe; a burst starting at `1Ch` will wrap onto `10h` after four bytes and quietly overwrite the seconds register if you were writing. There is no cross-block burst.

### 3.2 ⚠ The manual mis-states where the clock registers live

§13.3.1 is headed *"Clock and calendar registers (0h ~ 16h)"*. There are **no user registers below `10h`** — Table 12 places `SEC` at `10h` and the address-circulation table starts at `10h`. The heading is an error, present identically in `ETM50E-09` and `ETM50E-10`. Take Table 12.

This matters because most I²C RTCs *do* start their clock registers at `00h`; a driver ported from one will read zeros.

---

## 4. Interrupt sources

Three independent interrupt sources share the single open-drain `/IRQ` pin. Each has a flag bit in `1D` and an enable bit in `1E`. **All flags are write-0-to-clear; writing 1 is ignored.** **[DS-09]** §14.2–§14.4.

| Source | Flag | Enable | Auto-releases `/IRQ`? |
|---|---|---|---|
| **Wakeup timer** | `TF` (`1D`.4) | `TIE` (`1E`.4) | **Yes**, after `tRTN2` |
| **Alarm** | `AF` (`1D`.3) | `AIE` (`1E`.3) | **No — latched until cleared** |
| **Time update** | `UF` (`1D`.5) | `UIE` (`1E`.5) | **Yes**, `tRTN1` ≈ 7.57 ms (max 15.63 ms) |

The asymmetry in the third column is the practical point: **the alarm holds `/IRQ` low forever until you clear `AF`**, whereas the timer and update interrupts release themselves. **[DS-09]** §14.3: *"/IRQ='L' output when occurs alarm interruption event is not cancelled automatically unless giving intentional cancellation."*

Note also that `AIE`/`TIE`/`UIE` only gate the *pin*, not the flag. Clearing `AIE` releases `/IRQ` but leaves `AF` set; the flag must be cleared separately.

### 4.1 Wakeup timer

A 16-bit down-counter (`1A`/`1B`, preset 1…65535) clocked from one of five sources selected by `TSEL2:0` (`1C`.2:0) **[DS-09]** Table 16:

| `TSEL2:0` | Source clock | Period per count | `/IRQ` auto-release `tRTN2` (min) |
|---|---|---|---|
| `000` | 4096 Hz | **244.14 µs** | **122 µs** |
| `001` | 64 Hz | 15.625 ms | 7.57 ms |
| `010` | 1 Hz | 1 s | 7.57 ms |
| `011` | 1/60 Hz | 1 min | 7.57 ms |
| `100` | 1/3600 Hz | 1 h | 7.57 ms |

Full range **244.14 µs to 65 535 hours** (≈ 7.5 years). `TE` (`1C`.4) starts and stops it; while `TE = 0` the counter registers read back the *preset*, while `TE = 1` they read the live count.

Two traps, both stated by Epson:

- **The first countdown is short.** With 4096/64/1 Hz sources the error is up to one source-clock period; with 1/60 and 1/3600 Hz it is up to **1 second** **[DS-09]** Figure 20.
- **Reading the live count is not atomic** — "when access to timer counter data, counting value is not held". Epson's own advice: read twice and accept the value only when two reads agree **[DS-09]** §14.2.1.

`TSTP`, `TBKON` and `TBKE` (`1E`.2:0) control the *Long-Timer* variant, which accumulates run time separately on the main and backup supplies and sums them — a usage counter rather than a periodic timer **[DS-09]** §13.1(3).

### 4.2 Alarm

Minute, hour, and either day-of-month or day-of-week, selected by `WADA` (`1C`.3): `0` = WEEK, `1` = DAY **[DS-09]** §14.3.

**There is no seconds field.** The alarm resolution is one minute, and `AF`/`/IRQ` may lag the match by up to **1.46 ms**.

**`AE` is low-active, and this is the part people get wrong.** Each of `17h`/`18h`/`19h` has an `AE` bit in bit 7; setting `AE = 1` makes that field a *don't-care*. So:

| Want | `17h` `AE` (min) | `18h` `AE` (hour) | `19h` `AE` (week/day) |
|---|---|---|---|
| Once per hour, at a given minute | **0** | 1 | 1 |
| Once per day, at a given time | 0 | 0 | 1 |
| Once per week | 0 | 0 | 0 |
| **Once per minute** (all fields ignored) | 1 | 1 | 1 |

With `WADA = 0` (WEEK), **multiple days can be set at once** — the week alarm register is a bitmask, so "Monday, Wednesday, Friday" is a single alarm.

Two cautions: **when `STOP` (`1E`.6) is 1, no alarm event occurs**; and if the alarm registers are being reused as RAM while `AIE = 1`, `/IRQ` can be driven low by accident **[DS-09]** §14.3.1.

### 4.3 Time update

`USEL` (`1C`.5) picks a **1-second** or **1-minute** tick, synchronised to the update of the second or minute register **[DS-09]** §14.4. `/IRQ` self-releases after `tRTN1` (min 7.57 ms). Clearing `UF` releases `/IRQ` immediately — a behaviour Epson added in `ETM50E-08`.

### 4.4 `VLF` — the flag that means "your time is garbage"

**[DS-09]** §14.5: `VLF` (`1D`.**1**) goes 0 → 1 when clock oscillation stopped or a power-on reset occurred, i.e. when data loss may have happened, and stays 1 until written 0.

> *"During the initial power-on (from 0 V) and/or if the value of the VLF bit is '1', be sure to initialize all registers before using them."*

`VLF` reads **1** after a power-on reset (Table 13) and **1** after a software reset (§7.2 note). It is the single most important bit on the device for a battery product — and the vendor driver on this board **does not read it**. See [§11-C4](#11-caveats-errata-and-a-driver-audit).

Do not confuse it with `VBLF` (`1D`.**7**), which is *low-backup-voltage* detection, or with `VBFF` (`1D`.**0**), which is *backup full-charge*.

---

## 5. Backup switchover and battery charging

This is the feature that distinguishes the RX8130CE from an ordinary RTC, and it is the most intricate part of the manual (§15, twelve pages).

Three MOS switches (`SW1`, `SW2A`, `SW2B`) sit between `VDD`, `VBAT` and the internal `VOUT` node, arbitrated by a supply-voltage detector. When `VDD` falls below `−VDET2` the RTC's internal supply is switched from `VDD` to `VBAT`; reverse current from `VBAT` into `VDD` is blocked. **While in backup mode the I²C bus and `FOUT` are switched off and their pins go Hi-Z** — but `/IRQ` and `/RST` keep working **[DS-09]** §3.2, §15.1.

### 5.1 Detection thresholds

**[DS-09]** Table 38, with the measured tolerances from Table 5:

| Symbol | What it does | Typ. rising / falling | Selected by |
|---|---|---|---|
| `VDET1` | **Reset assert / release** — also gates I²C and FOUT when `INIEN = 1` | 2.80 V / **2.75 V** | `RSVSEL = 0` *(default)* |
| `VDET1` | idem | 2.70 V / 2.65 V | `RSVSEL = 1` |
| `VDET2` | **Backup switchover / recover** | 1.35 V / **1.30 V** | — |
| `VDET3` | **`VBAT` full-charge / recharge** | 3.02 / 2.97 V | `BFVSEL = 00` *(default)* |
| `VDET3` | idem | 3.08 / 3.03 V | `BFVSEL = 01` |
| `VDET3` | idem | 2.92 / 2.87 V | `BFVSEL = 10` |
| `VDET3` | **charging with no limit** | — | `BFVSEL = 11` |
| `VDET4` | **`VBAT` low / end voltage** → sets `VBLF` | 2.40 V | — |

> ⚠ **Table 39 and Table 38 disagree about `BFVSEL`.** Table 38 maps `01` → 2.92 V and `10` → 3.08 V; Table 39, on the facing page, maps `01` → 3.08 V and `10` → 2.92 V. **The two encodings are transposed.** Both revisions carry the defect. This is a live hazard: pick the wrong one and a rechargeable backup cell is charged to the wrong ceiling. Do not use either table alone — the safe reading is that the two non-default settings are 2.92 V and 3.08 V, and which code selects which is **unresolved** in the vendor documentation. See §11-C2.

### 5.2 `INIEN` — the bit that latches on and cannot be un-latched

**[DS-09]** Table 35. `INIEN` (`1F`.4) defaults to **0**, in which state *"the power switching function is not operating"* and the supply is fixed to `VDD`. Setting it to 1 starts the switching circuit and **initialises and stabilises it**. Epson recommends setting it at least once.

The two sentences that matter:

> *"If this bit is set to 1 even once, the power switching function will start operating. After that, the power switching function continues to operate even if this bit is cleared to zero."*

> *"Setting INIEN from 0 to 1 with VDD < VDET1 disables I2C and FOUT outputs immediately. Therefore, I2C cannot clear INIEN to 0 while VDD < VDET1."*

So `INIEN` is **a one-way latch for the switching hardware**, and setting it at the wrong moment locks you out of the bus with no way back except a supply cycle. On the PaperMono, M5Unified sets it on every `begin()` (§11-C3).

Its second effect is the one that surprises people: with `INIEN = 1`, **I²C and `FOUT` stop working whenever `VDD` < `VDET1` (2.75 V)**. With `INIEN = 0` they keep working below `VDET1`. A 3.3 V rail sagging under load can therefore make the RTC vanish from the bus at 2.7 V rather than degrade gracefully.

### 5.3 `CHGEN` — charging a backup cell

`CHGEN` (`1F`.5), default **0** = *"For non-re-chargeable battery use"*, `SW2` off, no charging. Setting it to 1 puts `SW1`/`SW2` under automatic control for a rechargeable cell or EDLC, and requires `INIEN = 1` **[DS-09]** Table 34.

Charging stops at `+VDET3` and resumes at `−VDET3`; `VBFF` (`1D`.0) reports full-charge, updated every second. `VBLF` (`1D`.7) reports `VBAT` below `VDET4` (2.4 V), and needs `VBLFE` (`31h`.0) plus `INIEN = 1` to have been set at least once. **`VBLF` detection does not work in backup mode** — it is evaluated after returning to normal mode **[DS-09]** Table 42.

Detection cadence **[DS-09]** Table 36: reset detection and power-switching detection run continuously in normal mode; `VDET3`/`VDET4` are sampled **once per second**; in backup mode, switching detection drops to **once per 31.25 ms** and everything else is off.

> ⚠ **`STOP = 1` breaks backup switching.** In backup mode, `STOP` halts the 31.25 ms `VDET2` sampling, *"power supply switching becomes insufficient, and there is the possibility that a leak current occurs"*. Epson's instruction: if you enter backup mode with `STOP = 1`, clear it immediately after `VDD` returns **[DS-09]** §15.6(9).

### 5.4 Leakage

`ISW1`/`ISW2` off-leak between `VDD`/`VBAT` and `VOUT` are **5 nA max** each **[DS-09]** Table 5, and backup-mode consumption `IBAT` is **300 nA typ., 500 nA max** at `VBAT` = 3.0 V. Those are the numbers that make a supercapacitor backup workable — and the numbers that make a **1 µF ceramic** backup last microseconds, which is why the PaperMono's L0 behaviour matters (§2.1).

---

## 6. Reset output, FOUT and digital offset

**Reset output** (§16). `/RST` is an N-ch open drain asserted whenever `VDD` < `VDET1` and released **60 ms** after `VDD` recovers. It works in backup mode. `RSF` (`1D`.2) latches that a reset-level excursion happened, and reads **1** after power-on reset. On the PaperMono `/RST` is not routed to any processor; it sits behind `R47`, a 22 Ω 1 % resistor **[SCH]**, whose purpose was not established.

**FOUT** (§14.6). `FSEL1:0` (`1C`.7:6) selects **32.768 kHz** (`00`, the power-on default), **1024 Hz** (`01`), **1 Hz** (`10`) or **off** (`11`). Output stops and goes Hi-Z below `VDET1`. ⚠ **`STOP = 1` disables the 1 Hz output but leaves 32.768 kHz and 1024 Hz running.** On the PaperMono `FOUT` is unrouted, and because the power-on default is *enabled at 32.768 kHz*, an unused `FOUT` is toggling at 32 kHz until firmware turns it off. It is left open as the manual requires, so this is a (small) current cost rather than a fault. `inferred`.

**Digital offset** (§17). `30h`: `DTE` (bit 7) enables it; `L7`…`L1` is a sign-magnitude trim with `L7` as the sign, over **+192.26 to −195.31 × 10⁻⁶ in 3.05 × 10⁻⁶ steps**. Correction is applied to the sub-second counter **every 10 seconds**. It does **not** change the crystal frequency, so a 32.768 kHz `FOUT` is unaffected, but 1 Hz and 1024 Hz outputs acquire jitter, and **the alarm and any wakeup-timer source slower than 4096 Hz are affected by it**.

---

## 7. Bring-up

### 7.1 Epson's initialization flow

**[DS-09]** §18.1, in order:

1. Power on.
2. **Wait > 30 ms.** (Not the oscillation start time — a separate settling requirement.)
3. **Dummy read** — one read of a free address, ignoring ACK/NACK. Needed when the power ramp did not satisfy the power-on-reset conditions.
4. **Read `VLF`.** If `VLF = 1`, the part did not return from backup cleanly → perform a **software reset** (§7.2), starting from its step 4.
5. **Clear `VLF` to 0.** It cannot be cleared until internal oscillation has started, so allow a wait.
6. Set `INIEN`, then the rest of the configuration, then the clock.

§10.1 adds the timing detail: **`VLF` becomes readable 30 ms after power-on**; register access is possible once `VLF` reads 0, but *"clock updating is invalid while `t_str`"* — up to 1.0 s.

§10.2 adds two conditions that are easy to violate on a battery board: **`VDD` = `VBAT` = GND for ≥ 10 s before power-on** is required for the power-on reset to work, and if the `tR1` ramp condition is not met *"power-on reset may not work. As a result, the time accuracy and current consumption may not meet the specifications. Please reset by software."*

### 7.2 Software reset writes outside the documented map

**[DS-09]** §18.2, reproduced because it is not derivable and the addresses appear nowhere else:

```
1) Power ON
2) Wait > 30 ms
3) Dummy read                (ignore NACK/ACK)
4) Write 00h to 1Eh
5) Write 80h to 1Eh          -> then complete the rest immediately
6) Write 6Ch to 50h
7) Write 01h to 53h
8) Write 03h to 66h
9) Write 02h to 6Bh
10) Write 01h to 6Bh         -> TEST bit self-clears here
12) Wait 125 ms
```

Notes attached to it: leakage may occur between steps 6 and 10 because **all power switches are on** during that window; `/RST` goes low for **up to 95 ms** from step 10; **`VLF` is set to 1** and must be cleared; and **the clock and calendar registers are *not* reset** — the time survives.

### 7.3 I²C protocol constraints

**[DS-09]** §19.2, §19.6:

- Standard I²C, up to 400 kHz. Address `0110010` + R/W.
- **A single transfer must not exceed 0.95 seconds** between START and STOP. There is no byte-count limit, only that time limit.
- Epson explicitly warns: *"Please make sure to send I2C start condition before actual transmission of the RTCs slave address as otherwise the slave address appears to be shifted by 1 bit."*
- ⚠ **The clock stops during I²C communication.** §13.1(1): *"At the start of a I2C communication, the time and clock counting stops (which causes loss of time), and clock starts automatically again at the end of the I2C communication."* See §11-C5.

---

## 8. Libraries

| Option | Where | Verdict |
|---|---|---|
| **`M5Unified` → `M5.Rtc`** | `github.com/m5stack/M5Unified`, backed by `src/utility/rtc/RX8130_Class.{hpp,cpp}` | ✅ **What the PaperMono uses.** Competent, and better than it looks — but see the audit in §11 |
| Raw I²C | — | Entirely reasonable; §3–§7 above is the whole device. Mind the block-wrapping auto-increment (§3.1) |
| Epson tools | Epson publishes an Excel clock-accuracy calculator and a digital-offset calculator, linked from the manual | Not retrieved |

API surface **[SRC]** `RX8130_Class.cpp`:

```
begin(I2C_Class*)
getDateTime(rtc_date_t*, rtc_time_t*) / setDateTime(...)
setTimerIRQ(uint32_t msec)   -> returns the period actually programmed, in ms
setAlarmIRQ(const rtc_date_t*, const rtc_time_t*)
getIRQstatus()   // 0x1D & 0x18  -> TF | AF
clearIRQ()       // write 0xA7 to 0x1D  (write-0-clear: clears TF and AF only)
disableIRQ()     // clear TIE|AIE, then clearIRQ()
getVoltLow()     // 0x1D & 0x80  -> VBLF     <-- see C4
```

The factory firmware simply aliases it: `m5::RTC_Class& rtc = M5.Rtc;` **[SRC]** `hal.h:70`, and uses **4 bytes of the RTC's user RAM from `0x20`** **[SRC]** `hal_board.cpp:18` (`RX8130_RAM_BASE = 0x20`, `RX8130_RAM_SIZE = 4`) — that is the full `20h`–`23h` block.

---

## 9. Vendor driver audit — `M5Unified::RX8130_Class` against `ETM50E`

Read side by side, as the method requires. **Most of it is good**, and two of the findings are the opposite of defects.

### 9.1 What the driver does well

- **`clearIRQ()` writes `0xA7`.** Every flag in `1D` is write-0-to-clear with writes of 1 ignored, so `0b1010_0111` clears exactly `TF` (bit 4) and `AF` (bit 3) and touches nothing else. `RSF`, `VLF`, `UF`, `VBLF` and `VBFF` are all preserved. The in-code comment says `// W0C: clear TF and AF only`, and it is correct. **Not a defect.**
- **`setAlarmIRQ()` gets `AE` polarity right.** The buffer is initialised `{0x80, 0x80, 0x80}` — all fields disabled — and a field is *enabled* by overwriting it with its BCD value, which clears `AE`. It sets `WADA` (`1C`.3) according to whether a date or a weekday was supplied, encodes the weekday as a bitmask, and sets `AIE` only if at least one field was given. Matches §14.3 exactly. **Not a defect.**
- **`setTimerIRQ()` is unusually careful.** It picks a source clock from a table, and **deliberately treats 4096 Hz as a last resort** with the comment *"its /IRQ pulse is only 122us"* — which is precisely Epson's `tRTN2` figure for `TSEL = 000` (§4.1). It bounds the first-countdown error (§4.1's stated trap) by requiring at least 16 counts. It writes `1A`/`1B` while `TE = 0` and then **reads them back and retries up to three times**, with the comment: *"a corrupted preset was observed on a shared bus"*. That is a real-world observation about this board's seven-device I²C bus, recorded in vendor code.
- **`getDateTime()` validates before committing** — BCD range checks on every field, a one-hot check on the weekday register, and a `validateDateTime()` pass — returning `false` rather than a plausible-looking wrong date. The rationale is in the comment.

### 9.2 `getVoltLow()` reports the wrong flag — this is the finding

```cpp
bool RX8130_Class::getVoltLow(void)
{
  // 0x80: VBLF
  return readRegister8(0x1D) & 0x80;
}
```

`0x80` is bit 7 of the Flag Register, which is **`VBLF` — "Low-VBAT has been detected (`VDET4`)"** **[DS-09]** Table 41. The flag that means *the clock stopped and the register data are invalid* is **`VLF`, bit 1** (`0x02`) **[DS-09]** Table 31.

Two things follow, and they compound:

1. **After a power-on reset, `1D` reads `0000 0110`** — `VLF = 1`, `VBLF = 0` **[DS-09]** Table 13. So on the exact occasion the method exists to catch, **`getVoltLow()` returns `false`.**
2. **`VBLF` detection is conditional.** It requires `VBLFE` (`31h`.0) and `INIEN = 1` to have been set, and it *"is not available in backup mode"* **[DS-09]** Table 42. `RX8130_Class::begin()` never writes `31h`. With `CHGEN = 1` (which `begin()` does set) and `VBLFE = 0`, Epson's table says detection is available *"during normal mode re-chargeable battery charging"* — which, on a board where `VBAT` may be a 1 µF ceramic rather than a cell (§2.1), is a condition that may never meaningfully arise.

**Severity: latent, and the documentation amplifies it.** The device record's [`features/rtc.md` §5](../../../devices/m5stack/papermono/features/rtc.md) currently advises: *"`getVoltLow()` is the one worth wiring into a first-boot path: it tells you the RTC lost its supply and the time is not trustworthy."* On the evidence above it does not tell you that. Code that trusts it will accept an uninitialised clock as valid.

**What to do instead:** read `1D` yourself and test **bit 1**. If set, follow §7.1 — software-reset if necessary, clear `VLF`, then set the time. Recorded here rather than patched into the other record; that is the device record's author's call.

*(Whether the name `getVoltLow` was intended to mean "backup voltage low" rather than "the RTC lost power" is unknowable from the source. Either way the datasheet-facing behaviour is as described, and the `RX8130_Class` implementation is the only accessor M5Unified exposes for `1D`.)*

### 9.3 `begin()` skips Epson's entire initialization procedure

```cpp
bool RX8130_Class::begin(I2C_Class* i2c)
{
  ...
  bool res = bitOn(0x1F, 0x30);          // CHGEN=1 (0x20) and INIEN=1 (0x10)
  res &= writeRegister8(0x30, 0x00);     // digital offset off
  res &= writeRegister8(0x1E, 0x00);     // Control Register 0 = 0
  ...
}
```

Against §18.1, this omits: the **> 30 ms wait**, the **dummy read**, the **`VLF` check**, the **software reset when `VLF = 1`**, and **clearing `VLF`**. Writing `1E` = `0x00` does correctly clear `TEST` and `STOP` along with the interrupt enables, which is good hygiene.

Two specific consequences:

- **`INIEN` is set on every `begin()`, and it is a one-way latch** (§5.2). Epson also warns that setting it while `VDD` < `VDET1` immediately kills the I²C interface with no software route back. On a board where `begin()` may run during a rail ramp, that is a real if unlikely wedge. **Latent.**
- **`CHGEN = 1` enables backup-battery charging** (§5.3). Epson's default is 0, *"for non-re-chargeable battery use"*. **If `VBAT` on this board carries a primary cell or nothing but a ceramic capacitor rather than a rechargeable cell or EDLC, this write is at best pointless and at worst wrong.** Since the `VBAT` net could not be established from the schematic text layer (§2.1), **this cannot be resolved here** — and that is exactly why the `VBAT` net is the highest-value open item in this record. Note that `M5Unified`'s `RX8130_Class` is shared across M5Stack products, so the setting is not necessarily a PaperMono decision at all.

### 9.4 Registers the driver never touches

`1C` `FSEL1:0` — so **`FOUT` is left at its power-on default of 32.768 kHz enabled** (§6). `1C` `USEL` and `1E` `UIE` — the time-update interrupt is unreachable through `M5.Rtc`. `1F` `RSVSEL`, `BFVSEL1:0`, `SMPTSEL1:0` — reset threshold, charge ceiling and sampling cadence all stay at defaults. `31h` `VBLFE`. `1E` `TSTP`/`TBKON`/`TBKE` — the Long-Timer / usage-counter mode. `30h` is written once, to zero, so the digital offset trim is explicitly disabled and never used.

---

## 10. Used By

### [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) — designator `U16`, sheet 4

> **FCC internal photographs — 2026-09-20.** The PaperMono's FCC filing
> (`2AN3WM5PAPERMONO`) includes an internal-photograph exhibit, now retained at
> [`devices/m5stack/papermono/artifacts/certification/`](../../../devices/m5stack/papermono/artifacts/certification/README.md).
> It is the first physical-hardware evidence for this part on this board.
>
> **Confirmed.** Exhibit p. 3 shows a 12-pad ceramic package marked
> **`R8130`** / `○3581K` beside the SX1262 module, corroborating the fitted part
> from hardware rather than from the schematic alone. The `CE` suffix is not on
> the package marking — Epson's `R8130` house mark does not carry it — so the
> exact ordering variant is **not** confirmed by the photograph.
>
> Extraction: [`certification.md` §6](../../../devices/m5stack/papermono/certification.md#6--what-the-internal-photographs-show).

| Role on PaperMono | Pin | Evidence |
|---|---|---|
| I²C slave at **`0x32`** on the shared system bus, driven at **400 kHz** | 2 `SCL` → `G48_SYS_SCL` (GPIO48); 3 `SDA` → `G47_SYS_SDA` (GPIO47) | **[SCH]** `U16`.2/.3; **[SRC]** `hal_board.cpp:17,19` |
| **`nIRQ` → M5PM1 pin 3 (`IO0`)**, *not* to any ESP32-S3 GPIO | 6 → `PYG0_RTC_INT`, pulled up by `R49` | **[SCH]** `U16`.6; **[SRC]** `app_sleep_wake.cpp:67` |
| Interface supply | 1 `VIO` → **`3V3_L0`** (always-on rail) | **[SCH]** — see §2.1 |
| Logic supply | 8 `VDD` → vendor power tree says **`3V3_L1`**; net not recoverable from the schematic text layer | **[DOC]** vs **[SCH]**, §2.1 |
| Backup supply | 10 `VBAT` → **not established** | §2.1 |
| Reset output | 5 `/RST` behind `R47` **22 Ω / 1 %**; not routed to a processor | **[SCH]** |
| `FOUT` | 4 — **unrouted**, left open as the manual requires | **[SCH]** |
| User RAM | `20h`–`23h`, **all 4 bytes used by the factory firmware** | **[SRC]** `hal_board.cpp:18` |
| Local passives | `C60`, `C61`, `C62` — 1 µF / 25 V each; `R49` `/IRQ` pull-up | **[SCH]** |

#### 10.1 The interrupt path is the whole point

There is **no route from this RTC to any ESP32-S3 pin.** An ESP32 wake source configured for an RTC alarm can never fire.

The shipped factory binary states the path and the polarity in as many words **[FW]**:

```
PM1 shutdown, wake by RX8130 timer  -> PM1 G0 falling edge
```

M5Unified configures the board to match **[SRC]** `Power_Class.cpp:528` onward: `_rtcIntPin = GPIO_NUM_1` — which is the **M5PM1's IRQ output toward the host**, not the RTC line — with `setGPIOIRQMaskBits(0x1E)` enabling M5PM1 `G0`'s interrupt and masking the other four, `G0` as a plain input, and `G1` as a push-pull IRQ output.

So the chain is:

- **Host awake:** RX8130CE `/IRQ` → M5PM1 `IO0` → M5PM1 `IO1` → ESP32-S3 **GPIO1**.
- **Host asleep in L1:** the chain stops at the M5PM1, which **powers the application processor back up**. That is the capability this part exists to provide on this board.

The falling edge is the RTC's open-drain `/IRQ` pulling low, and the M5PM1's `G0` wake is configured falling-edge to match **[SRC]** `app_sleep_wake.cpp:67`.

⚠ Note the vendor firmware **disables both M5PM1 wake sources at startup** (`clearPm1WakeIrqState()`, `hal_board.cpp:42-43`), so it does not itself demonstrate the RTC-wake path end to end. The firmware string proves the path was designed and exercised by someone; nothing located here proves it *works*.

#### 10.2 Practical consequences for this board

- **Choose the right timer for the job.** For "wake me in N seconds", the [M5PM1's own 31-bit second timer](../../m5stack/m5pm1/README.md) needs no RTC at all and is the vendor-demonstrated path. Use the RX8130CE alarm when you need a wall-clock time — "07:30 on weekdays" — which the M5PM1 cannot express. See [`features/rtc.md` §6](../../../devices/m5stack/papermono/features/rtc.md).
- **The alarm has minute resolution and latches `/IRQ`** (§4.2). Clear `AF` in the wake handler or the M5PM1's `G0` never returns high.
- **Keep `L1` alive across a shutdown** (`ldoSetPowerHold(true)`) or the RTC loses its supply along with everything else.
- **The bus is shared with a chatty NFC poller.** §11-C5 explains why that is not merely a bandwidth question for this particular device.

### [M5Stack PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md) — **fitted, identically**

The Lite drops **NFC and LoRa and nothing else**; the RX8130CE, its `0x32` address, its `PYG0_RTC_INT` line to M5PM1 `IO0` and the whole power tree carry over unchanged **[DOC]**. The shared `M5PaperMono-UserDemo` firmware image serves both SKUs and distinguishes them by probing the **NFC** rail, never the RTC **[SRC]** `hal_board.cpp:160-172`.

One caveat on the strength of that claim: M5Stack publishes a **4-sheet `PRJ` PDF** for the Lite rather than the 6-sheet `SCH` published for the PaperMono, so the Lite's RTC wiring is asserted from the vendor specification table and the shared firmware, **not** from a Lite schematic. `inferred`.

---

## 11. Caveats, errata and a driver audit

| # | Issue | Evidence |
|---|---|---|
| **C1** | **The mirror is one revision behind — and carries *more* text than Epson's current file.** `ETM50E-09` (2025-06-30) vs `ETM50E-10` (2026-01-30). The two were normalised and diffed line by line: apart from table-of-contents renumbering and whitespace, **the only substantive change is that `-10` deletes items (1)–(7) of §14.4.2**, the seven-step operation description of the time-update interrupt. Epson's own changelog entry reads *"Deleted (1) to (7) in the operation description."* **Every register, threshold and timing value in this record is identical in both.** Both revisions are retained | `executed-success` — full-text diff, 2026-09-01 |
| **C2** | ⚠ **`BFVSEL` is encoded two contradictory ways on facing pages.** Table 38 gives `01` → 2.92 V, `10` → 3.08 V; Table 39 gives `01` → 3.08 V, `10` → 2.92 V. Present in both revisions. **A backup cell charged to the wrong ceiling is a safety-adjacent error.** Unresolved — do not rely on either table alone | **[DS-09]**/**[DS-10]** §15.6 |
| **C3** | **`INIEN` is a one-way latch, and M5Unified sets it on every `begin()`.** Once set, the power-switching circuit stays on even if the bit is cleared; and setting it while `VDD` < `VDET1` disables the I²C interface *with no software route back* | **[DS-09]** Table 35; **[SRC]** §9.3 |
| **C4** | ⚠ **`getVoltLow()` reads `VBLF` (bit 7, low-backup-battery), not `VLF` (bit 1, oscillation stopped / data invalid).** After a power-on reset `VLF = 1` and `VBLF = 0`, so the method returns `false` on precisely the occasion it is used to detect. **The device record's `features/rtc.md` §5 currently recommends it for exactly that purpose.** Full analysis in §9.2 | **[DS-09]** Tables 13, 31, 41 vs **[SRC]** `RX8130_Class.cpp` |
| **C5** | ⚠ **I²C communication stops the clock.** §13.1(1): *"At the start of a I2C communication, the time and clock counting stops (which causes loss of time), and clock starts automatically again at the end."* A transfer may run up to **0.95 s**. On a board whose single I²C bus also carries an NFC poller running 180 ms detect calls with 60 ms gaps for seconds at a time, this is a **timekeeping-accuracy** concern, not just a bandwidth one. **Unresolved:** the manual does not say whether counting halts for *any* bus activity or only for transactions addressed to `0x32`. Nothing was measured | **[DS-09]** §13.1, §19.2 |
| **C6** | **Auto-increment wraps inside 16-byte blocks** (`10h`–`1Fh`, `20h`–`2Fh`, `30h`–`3Fh`), it does not carry into the next block (§3.1) | **[DS-09]** §19.6 |
| **C7** | **§13.3.1 says the clock registers are at "0h ~ 16h". They are at `10h`–`16h`.** Present in both revisions. Most I²C RTCs start at `00h`, so a ported driver will read zeros (§3.2) | **[DS-09]**/**[DS-10]** §13.3.1 vs Table 12 |
| **C8** | **`AE` is low-active.** Setting an alarm field's `AE` bit to **1** makes it a *don't-care*; all three set to 1 gives an alarm every minute (§4.2) | **[DS-09]** §14.3.1 |
| **C9** | **The alarm latches `/IRQ` indefinitely; the timer and update interrupts self-release.** Failing to clear `AF` leaves the line low forever (§4) | **[DS-09]** §14.3 |
| **C10** | **The 4096 Hz timer source releases `/IRQ` after only 122 µs**, versus 7.57 ms for every other source. An interrupt that short can be missed by a polling host. M5Unified deliberately avoids it (§9.1) | **[DS-09]** Table 16 |
| **C11** | **Reading the live timer counter is not atomic.** Epson recommends reading twice and accepting the value only when two reads agree | **[DS-09]** §14.2.1 |
| **C12** | **`STOP = 1` has three unrelated side effects:** no alarm events; 1 Hz `FOUT` disabled while 32.768 kHz and 1024 Hz keep running; and backup switching becomes unreliable with possible leakage | **[DS-09]** §14.3.1, §14.6.2, §15.6(9) |
| **C13** | **`FOUT` defaults to *enabled* at 32.768 kHz.** On this board it is unrouted and unconfigured, so it toggles until firmware disables it. Left open as the manual requires, so this is a small current cost rather than a fault. `inferred` | **[DS-09]** §14.6.2; **[SCH]**; **[SRC]** — negative result, M5Unified never writes `FSEL` |
| **C14** | **The power-on-reset preconditions are demanding:** `VDD` = `VBAT` = GND for **≥ 10 seconds** before power-on, plus a `tR1` ramp condition. If unmet, Epson says accuracy and current consumption may be out of specification and a **software reset is required**. Whether a PaperMono coming out of L0 satisfies this is **unknown** | **[DS-09]** §10.2 |
| **C15** | **M5Unified's `begin()` performs none of Epson's §18.1 flow** — no 30 ms wait, no dummy read, no `VLF` check, no software reset, no `VLF` clear (§9.3) | **[SRC]** vs **[DS-09]** §18.1 |
| **C16** | **The `VDD` and `VBAT` nets on this board are not established.** The schematic text layer yields adjacency, not connectivity, and no label was recoverable at either pad. Statements about L0 timekeeping, and the correctness of `CHGEN = 1`, both hang on this (§2.1, §9.3) | **[SCH]** — explicit gap |
| **C17** | **Nothing about this part has been measured on this board by anyone.** No drift figure, no accuracy report, no backup-hold-up time, no confirmation that an RTC alarm has ever woken a PaperMono | **[DOC]**, community — negative result |

---

## 12. Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/rx8130ce-register-datasheet-cn-m5stack-mirror.pdf` | 2 283 323 | `7157dc5692e5e0d84203027b600858e57880ef7a38b9c7d7f8c661a93fc8f3f5` | **Epson application manual `ETM50E-09`, 70 pp — in English despite the `cn` in the filename** (see the note at the top of this record). PDF metadata: Producer `Microsoft® Word for Microsoft 365`, created 2025-06-23, modified 2025-07-16, AES-256 encrypted with print/copy permitted. **This is the revision M5Stack ships and the one the board's software was written against.** |
| `artifacts/rx8130ce-application-manual-etm50e-10-en-epson.pdf` | 2 008 845 | `db027a5fa2dd17b333da81e95063764eb5536d2878c63b64949348d2ec4b8a22` | **Epson application manual `ETM50E-10`, 70 pp, English — Epson's current revision, retrieved direct from the manufacturer in this pass.** PDF metadata: Author `Seiko Epson Corporation`, Creator `Pdf_as`, Producer `iTextSharp 5.4.5`, created 2026-02-01, RC4 encrypted with print/copy permitted. Retained **because the diff is a finding** (§11-C1): it is one revision *newer* but carries *less* text |

Both files, in the schema the manifest uses:

| Field | `…-cn-m5stack-mirror.pdf` | `…-etm50e-10-en-epson.pdf` |
|---|---|---|
| Version / revision | **`ETM50E-09`** | **`ETM50E-10`** |
| Publication date | **2025-06-30** (document revision table) | **2026-01-30** (document revision table) |
| Retrieval date | **2026-09-01** | **2026-09-01** |
| Byte size | 2 283 323 | 2 008 845 |
| SHA-256 | `7157dc56…befef1`⁠ → `7157dc5692e5e0d84203027b600858e57880ef7a38b9c7d7f8c661a93fc8f3f5` | `db027a5fa2dd17b333da81e95063764eb5536d2878c63b64949348d2ec4b8a22` |
| **Canonical URL** | `https://download.epsondevice.com/td/pdf/app/RX8130CE_en.pdf` *(now serves `-10`; `-09` is no longer offered by Epson)* | `https://download.epsondevice.com/td/pdf/app/RX8130CE_en.pdf` |
| **M5Stack mirror URL** | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1132/RX8130CE_cn-Register-Datasheet.pdf` | *(not mirrored by M5Stack)* |
| Additional URL | — | `https://download.epsondevice.com/td/pdf/app/RX8130CE_cn.pdf` — **the same English document**, 2 008 853 B, `0ff562f25f4b5a8cf5f3df98632c5bc31030cdd4ebf7d7e53fbb03091d4c63d2` |
| Product page | `https://www5.epsondevice.com/en/products/rtc/rx8130ce.html` → redirects to `https://www.epsondevice.com/crystal/en/products/rtc/rx8130ce.html` | idem |
| Licence | **`unknown`** — © Seiko Epson Corporation. ⚠ the document's own notice 2 states: *"This document may not be copied, reproduced, or used for any other purposes, in whole or in part, without Epson's prior consent."* | **`unknown`**, identical notice |
| Redistribution status | **`restricted`** — the document states a limitation in as many words | **`restricted`** |
| Disposition | **`repository`** | **`repository`** |
| Type validated | Yes — `%PDF-1.7`, 70 pp, A4 | Yes — `%PDF-1.4`, 70 pp, A4 |

> **Note on the redistribution status.** Both files carry an explicit no-redistribution notice, so they are marked `restricted` rather than `unknown` — this is the honest reading of the text, recorded as metadata, not as a legal conclusion. They are retained under the repository's stated policy of gathering the artifact and recording the terms. Flagged here for review rather than acted on.

Recorded reference-only, not retained:

| Item | URL | Bytes | SHA-256 | Status |
|---|---|---:|---|---|
| Application manual, **Japanese** — `ETM50J-10`, 64 pp | `https://download.epsondevice.com/td/pdf/app/RX8130CE_ja.pdf` | 2 986 434 | `32913ca00eadaeaa263e448bf0049a492d808449fa41ee3f1aabb46c9409011c` | Downloaded, hashed and identified, **not retained**. Metadata: Creator `Microsoft® Word for Microsoft 365`, created 2025-06-23, AES-256. Six pages shorter than the English. **Equivalence not assessed.** Freely re-fetchable from a stable vendor URL; disposition `reference-only` |
| Datasheet brief | `https://download.epsondevice.com/td/pdf/brief/RX8130CE_en.pdf` | — | — | **Not retrieved.** Confirmed listed on the Epson product page |
| RoHS / REACH / TSCA / CA65 declarations, package-and-reflow guide | `https://download.epsondevice.com/td/pdf/rohs/RX8130CE.pdf` and siblings | — | — | **Not retrieved.** Enumerated from the product page; compliance paperwork, not technical |

**Retrieval note.** `www.epsondevice.com` served every one of these to a plain modern-Chrome user-agent on the first attempt, HTTP 200, correct `application/pdf`. No user-agent rotation was needed. The only trap is the redirect from the `www5.` host to `www.epsondevice.com/crystal/…`, which `curl -L` follows without complaint. `executed-success`, 2026-09-01.

---

## 13. Related components

- [**M5Stack M5PM1**](../../m5stack/m5pm1/README.md) — where this RTC's interrupt actually lands (`IO0`), and the owner of the `3V3_L0`/`3V3_L1` rails. Its **own** 31-bit second timer is the simpler wake mechanism on this board
- [**Espressif ESP32-S3R8**](../../espressif/esp32-s3r8/README.md) — the host. GPIO47/48 carry the bus; **no ESP32-S3 pin touches this part's interrupt**
- [**M5Stack M5IOE1**](../../m5stack/m5ioe1/README.md) — the other coprocessor on the same bus, with 32 bytes of its own retention RAM at `0x70`–`0x8F` that nothing uses
- [**STMicroelectronics ST25R3916**](../../stmicroelectronics/st25r3916/README.md) — the NFC front end whose polling shares this bus (§11-C5)
- [**Bosch Sensortec BMI270**](../../bosch-sensortec/bmi270/README.md) — the other M5PM1 wake source, on `IO4`
- [**NXP PCF85063A**](../../nxp/pcf85063a/README.md) — the comparable RTC used on the Inkplate boards in this repository, for contrast: 220 nA, I²C `0x51`, **no** backup-charge controller
- [Vendor sourcing guides index](../../../vendors/README.md) — **no Seiko Epson guide exists yet**; the retrieval notes in §12 are what one would open with
- [Components index](../../README.md)

---

## 14. Authoritative sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | RX8130CE Application Manual | **Seiko Epson Corporation**, mirrored by M5Stack | credible mirror | application manual | `artifacts/rx8130ce-register-datasheet-cn-m5stack-mirror.pdf`; mirror URL `m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1132/RX8130CE_cn-Register-Datasheet.pdf` | 2026-09-01 | **`ETM50E-09`, 2025-06-30**, 70 pp | §1–§7, §11. **The revision the board's software targets** |
| S-2 | RX8130CE Application Manual | **Seiko Epson Corporation** | primary | application manual | `artifacts/rx8130ce-application-manual-etm50e-10-en-epson.pdf`; `download.epsondevice.com/td/pdf/app/RX8130CE_en.pdf` | 2026-09-01 | **`ETM50E-10`, 2026-01-30**, 70 pp | §11-C1 — establishes mirror lag and its (small) content delta |
| S-3 | RX8130CE Application Manual, Japanese | Seiko Epson Corporation | primary | application manual | `download.epsondevice.com/td/pdf/app/RX8130CE_ja.pdf` | 2026-09-01 | **`ETM50J-10`**, 64 pp | §12 — reference-only; establishes that the English text is a translation |
| S-4 | RX8130CE product page | Seiko Epson Corporation | primary | vendor page | `www5.epsondevice.com/en/products/rtc/rx8130ce.html` → `www.epsondevice.com/crystal/en/products/rtc/rx8130ce.html` | 2026-09-01 | undated | §12 document enumeration; **negative result:** no Chinese-language manual is published |
| S-5 | PaperMono schematic, sheet 4 (`U16`) | M5Stack | primary | schematic PDF | `PaperMono_SCH_V0.6.2_20260522.pdf` (held in the device tree) | 2026-09-01 | **V0.6.2, 2026-05-22** | §2 pin table, §10 wiring |
| S-6 | `M5Unified` — `src/utility/rtc/RX8130_Class.{hpp,cpp}`, `src/utility/Power_Class.cpp` | M5Stack | primary | source | `github.com/m5stack/M5Unified`, pinned by the factory firmware at `2fe93c0c64f12f916e73a0605c86bf1241c06a6b` (patched) | 2026-09-01 | release 0.2.21 lineage, MIT | §8 API, §9 driver audit, §10.1 |
| S-7 | `M5PaperMono-UserDemo` — `main/hal/hal_board.cpp`, `main/hal/hal.h`, `main/app_sleep_wake.cpp`, `repos.json` | M5Stack | primary | source | `github.com/m5stack/M5PaperMono-UserDemo` @ `c1099107271d31a0678d661a896e2b04dbb331ea` | 2026-09-01 | 2026-08-10, MIT | §1 address/speed, §8 RAM use, §10 |
| S-8 | PaperMono product page — specification table, power-tree table | M5Stack | primary | vendor docs | `docs.m5stack.com/en/core/PaperMono` | 2026-09-01 | undated | §2.1 rail assignment, §10 |
| S-9 | PaperMono-Lite product page | M5Stack | primary | vendor docs | `docs.m5stack.com/en/core/PaperMono-Lite` | 2026-09-01 | undated | §10 — the RTC carries over unchanged |
| S-10 | `C153-PaperMono-UserDemo-v1.2` firmware image | M5Stack via M5Burner | primary | binary | SHA-256 `72c290bc2ffa216041b276660277369bd17ecef92315e367d98bb2c96c8428fa` | 2026-09-01 | v1.2, built 2026-08-06, IDF v5.5.1 | §10.1 — `PM1 shutdown, wake by RX8130 timer -> PM1 G0 falling edge` |
