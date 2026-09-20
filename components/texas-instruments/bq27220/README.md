# Texas Instruments BQ27220 — I²C battery fuel gauge

- **Category:** single-cell Li-ion gas gauge with Impedance Track™.
- **Manufacturer:** Texas Instruments.
- **Research status:** ⚠ Identified from **firmware source plus an independent
  teardown BOM**. No datasheet retrieved in this session.
- **Retrieved:** 2026-09-04

The battery gauge of the **Xteink X3**, and of the LilyGo T5-S3 boards the same
SDK supports.

## 1. What is established

| Property | Value | Evidence |
|---|---|---|
| I²C address | **0x55** | FreeInk board profile; `XteinkDetect` probe |
| Bus speed used on the X3 | 400 kHz | board profile |
| **State of charge** | command register **`0x2C`** | `XteinkDetect.cpp` (`BQ27220_SOC_REG`) |
| **Voltage** | command register **`0x08`** | `XteinkDetect.cpp` (`BQ27220_VOLT_REG`) |
| Access model | **TI command registers** | `GaugeType::Bq27220` |
| **Battery-profile upload** | **NOT required** — *"TI command registers, no profile upload"* | `BoardConfig.h:474-476` |
| Companion charger | optional; `chargerAddr = 0` on the X3 (**none on this bus**) | board profile |

## 2. Why this part is the family's best battery instrumentation

Three Xteink approaches, worst to best:

| Device | Method | Failure mode |
|---|---|---|
| [X4](../../../devices/xteink/x4/features/battery-and-power.md) | Bare **ADC** on GPIO0 with a ÷2 divider | Voltage-curve estimate only; no coulomb counting; cannot see charging |
| [X4 Pro](../../../devices/xteink/x4-pro/features/battery-and-power.md), X4 Classic | [CW2017](../../cellwise/cw2017/README.md) | **Reports 0 % until an 80-byte BATINFO profile is uploaded**; no current register |
| **X3** | **BQ27220** | **No profile upload needed.** Impedance Track™ coulomb counting |

The BQ27220 is the **least fragile of the three for a firmware author**: read
`0x2C`, get a number. That is worth knowing when choosing which Xteink to build a
project on.

## 3. Its second job: device identification

`XteinkDetect::detectXteinkVerdict()` scores the presence of three parts on the
C3 boards' secondary I²C bus (**SDA 20 / SCL 0**) to decide whether it is running
on an X3 or an X4:

| Address | Part | Probe |
|---|---|---|
| **0x55** | **BQ27220** | SoC reg `0x2C`, voltage reg `0x08` |
| 0x68 | [DS-series RTC](../../unidentified/xteink-x3-x4/rtc-ds-series/README.md) | seconds reg `0x00` |
| 0x6B | [QMI8658](../../qst/qmi8658a/README.md) | `WHO_AM_I` == `0x05` |

Finding them → **X3**. Finding nothing → **X4**. So a missing or mis-addressed
BQ27220 does not merely break the battery display — it can cause the firmware to
select the wrong board profile entirely.

## 4. Datasheet

**Not retrieved.** TI publishes `BQ27220` documentation openly at
`https://www.ti.com/product/BQ27220` (technical reference manual `SLUUBD2`);
retrieval status `not-attempted` this session. Recorded as an open acquisition —
this is one of the few chips in the Xteink subject with a **genuinely public,
authoritative vendor datasheet**, and it should be fetched and hashed.

## 5. Caveats

- The two register numbers above are the only ones the Xteink firmware uses. The
  BQ27220 has a much larger command set (`Control()`, `RemainingCapacity()`,
  `StateOfHealth()`, flags) that **no Xteink firmware touches** — including
  charge/discharge flags that would give charge state without a STAT GPIO.
- **The gauge's configured chemistry and design capacity were never audited.**
  The X3's cell is 650 mAh by teardown; whether the gauge is configured for that
  is unknown.
- Do not assume BQ27220 register semantics from the BQ27441 or BQ27441-G1 — they
  differ.

---

## Used By

### [Xteink X3](../../../devices/xteink/x3/README.md)

At **0x55** on the secondary I²C bus **SDA 20 / SCL 0 @ 400 kHz**, shared with the
[DS-series RTC](../../unidentified/xteink-x3-x4/rtc-ds-series/README.md) (0x68)
and the [QMI8658 IMU](../../qst/qmi8658a/README.md) (0x6B).
`chargerAddr = 0` — **no charger IC on this bus**, and unlike the S3 boards there
is also **no charge-STAT GPIO declared**, so how the stock firmware displays
charging state is **not established**.

Cell: **650 mAh**, connectorised, glued to the back cover (teardown). Charger:
a [TP4056-class part](../../unidentified/xteink-x3-x4/battery-charger-tp4056-class/README.md).

Corroborated independently by the Chinese teardown BOM: *"TI BQ27220 库仑计"*
(coulomb counter).

→ [`devices/xteink/x3/features/battery-and-power.md`](../../../devices/xteink/x3/features/battery-and-power.md)
→ [`devices/xteink/x3/pinouts-and-buses.md`](../../../devices/xteink/x3/pinouts-and-buses.md)

### LilyGo T5-S3 (not documented in this repository)

The same SDK pairs a BQ27220 with a BQ25896 charger at 0x6B on that board.
Recorded only to show the SDK's `chargerAddr` field has a real user.

### LilyGO T-Display K230 Kit — [`devices/lilygo/t-display-k230`](../../../devices/lilygo/t-display-k230/README.md) · *added 2026-09-07*

On the **nRF9151 keyboard base board**. I²C4: `SDA` ← `GPIO47`, `SCL` ← `GPIO46`, 7-bit address
**`0x55`**. Shares the bus with a [BQ25896](../bq25896/README.md) charger at `0x6B`, a
[TCA8418](../tca8418/README.md) at `0x34`, an [XL9555](../../xlsemi/xl9555/README.md) at a probed
address in `0x20`–`0x27`, and an [AHT20](../../asair/aht20/README.md) at `0x38`.

Cell is a **21700** in the keyboard-base compartment; the 5 V boost that powers the main unit from
it is enabled by the **nRF52840's `P0.04`**, not by the K230.

Low-battery shutdown is a **userspace policy** (`ui_hardware.c`), not a hardware cut-off: a
millivolt threshold against the gauge reading, with a confirm count and a recovery log line,
gated on BQ25896 USB-present. Defaults were tuned post-release in BSP v0.2.2 and v0.2.3.

*Source: `scratch/lilygo-k230/index-fragments.md` §F3.*

---

## Datasheet and technical reference manual — retrieved 2026-09-11

The record above stated *"No datasheet retrieved in this session"* and that the
authoritative vendor datasheet *"should be fetched and hashed"*. **Both the
datasheet and the technical reference manual have now been fetched, validated
and retained.**

| | Datasheet | Technical Reference Manual |
|---|---|---|
| Local path | [`artifacts/bq27220-datasheet-sluscb7a-rev-a.pdf`](artifacts/bq27220-datasheet-sluscb7a-rev-a.pdf) | [`artifacts/bq27220-technical-reference-manual-sluubd4-rev-a.pdf`](artifacts/bq27220-technical-reference-manual-sluubd4-rev-a.pdf) |
| **SHA-256** | `9fffe0b632cd287c9210aa1d2e71af1816b31764c11f1b62425de3a4a7cfe5f4` | `44779f229423d649e410439d1d1a3a65026d5919cdd43112ee3a3d8d9811ead9` |
| **Bytes** | **570,379** | **2,768,446** |
| Pages | 24 | — |
| TI literature number | **`SLUSCB7A`** | **`SLUUBD4`** |
| **Revision** | **Rev. A** — *SLUSCB7A – MARCH 2016 – REVISED APRIL 2016* | **Rev. A** |
| PDF title | `bq27220 Single-Cell CEDV Fuel Gauge datasheet (Rev. A)` | `BQ27220 Technical Reference Manual (Rev. A)` |
| PDF `CreationDate` | 2025-11-11 (TI re-renders on request) | — |
| Source URL | <https://www.ti.com/lit/ds/symlink/bq27220.pdf> | <https://www.ti.com/lit/ug/sluubd4/sluubd4.pdf> |
| Source class | **primary** | **primary** |
| Redistribution status | `unknown` — TI literature carries no explicit redistribution grant | same |
| Disposition | `repository`, **unstaged** | `repository`, **unstaged** |

**Text-layer validated** for both against their rendered page-1 headings
(*"bq27220 Single-Cell CEDV Fuel Gauge"*, `SLUSCB7A – MARCH 2016 – REVISED APRIL
2016`; and *"BQ27220 Technical Reference Manual"*).

### A failed guess, preserved

`https://www.ti.com/lit/ug/sluubd2/sluubd2.pdf` was tried first and returned a
**valid 1,277,976-byte PDF** titled ***"Using the TPS53317AEVM-726"*** — an
evaluation-module user's guide for an entirely unrelated part. TI's `sluubdN`
literature numbers are **not** sequential within a product family, and a
successful HTTP 200 plus a `%PDF` magic number proves nothing about *which*
document you got. The file was discarded. **Read the PDF title before filing
anything from `ti.com/lit`.** The correct number is `SLUUBD4`.

### Why the TRM matters more than the datasheet here

The X3's gauge is described in this repository as *"needing no profile upload"*,
in contrast to the X4 Pro's and X4 Classic's CW2017, which reports 0 % until an
80-byte BATINFO table is written. The **CEDV** configuration model, the
`Data Memory` layout and the gauging-parameter defaults that make that true are
in the **TRM**, not the datasheet. It is now available for the next session to
audit the FreeInk `BatteryMonitor` code against.

**Used by:** [Xteink X3](../../../devices/xteink/x3/README.md).
