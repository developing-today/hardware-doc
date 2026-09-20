# BM8563 — I²C real-time clock/calendar

- **Category:** low-power CMOS RTC/calendar with programmable clock output, alarm/timer
  interrupt and power-down detector; I²C, external 32.768 kHz crystal.
- **Manufacturer:** **unresolved.** The datasheet M5Stack mirrors carries no manufacturer name,
  logo or contact block on page 1. Filed under `generic/` rather than guessing a vendor.
- **Functional equivalent:** NXP **PCF8563** — same register map, same slave address, same
  feature set. See [`components/nxp/pcf8563/`](../../nxp/pcf8563/artifacts/pcf8563-datasheet-rev-11.pdf) in this repository
  for the fully-documented equivalent.
- **Retrieved:** 2026-09-04

The RTC of the M5Stack DinMeter, M5Dial, M5Capsule, M5StickC family and most other M5Stack
products. M5Unified exposes it as `RTC8563_Class`.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **BM8563** | datasheet cover; DinMeter schematic `U5` value text `RTC8563` |
| Datasheet | `BM8563_V1.1_cn.pdf` — **Chinese only**, v1.1 | retained artifact |
| Orderable variants | `BM8563ESA` (SOP8), `BM8563EMA` (MSOP8), `BM8563EHA` (TSSOP8), −40…+85 °C | datasheet ordering table |
| Supply | **1.5 – 5.5 V** | datasheet |
| Sleep current | typ. **0.25 µA** @ VDD 3.0 V, 25 °C | datasheet |
| I²C address | **write `0xA2`, read `0xA3`** → 7-bit **`0x51`** | datasheet |
| Max bus speed | 400 kbit/s | datasheet |
| Clock output | 32.768 kHz / 1024 Hz / 32 Hz / 1 Hz, programmable | datasheet |
| Interrupt | **open-drain** `INT` | datasheet |
| Oscillator caps | integrated | datasheet |
| Crystal | external 32.768 kHz | datasheet |

### ⚠ Document-metadata finding

Page 1 of `BM8563_V1.1_cn.pdf` carries the string **`MAX1937`** in the header area, immediately
after the title block and unrelated to anything else on the page. That is the signature of a
datasheet produced by editing another part's document — a Maxim MAX1937 template — and it is
worth knowing before trusting any electrical table in it that is not corroborated. The register
and address information *is* corroborated: it matches NXP's PCF8563 datasheet and M5Unified's
`RTC8563_Class` implementation.

**Language.** This document exists **only in Chinese** in every copy located. Per the
multi-language policy it is therefore the **primary source** and is retained in the repository
on its own merits, not archived as a translation. The English-language equivalent for the same
silicon behaviour is the [PCF8563 datasheet](../../nxp/pcf8563/artifacts/pcf8563-datasheet-rev-11.pdf).

## 2. Software

| Framework | API | Evidence |
|---|---|---|
| Arduino / M5Unified | `M5.Rtc` → `RTC8563_Class`; `isEnabled()`, `getDateTime()`, `setDateTime()`, `setAlarmIRQ()` | `M5Unified/src/utility/RTC8563_Class.*`; DinMeter's own `M5DinMeter.h:23` re-exports it as `DinMeter.Rtc` |
| Arduino (standalone) | `I2C_BM8563` — vendored in `m5stack/M5DinMeter-UserDemo` at `lib/I2C_BM8563/` | UserDemo snapshot |
| ESP-IDF | no built-in driver; `esp-board-manager` models only the I²C bus and notes *"BM8563 RTC (I2C 7-bit 0x51): no bmgr device type"* | `board_peripherals.yaml` |
| UiFlow2 / MicroPython | exposed as the board RTC | M5Stack docs |

## 3. Artifacts

| File | Size | SHA-256 | Version | Language | Licence | Redistribution | Disposition |
|---|---:|---|---|---|---|---|---|
| [`artifacts/BM8563_V1.1_cn.pdf`](artifacts/BM8563_V1.1_cn.pdf) | 590 599 | `a847c85a8d00121c1338c62797039fa1412d70588873313bd1759c80d4da44ed` | V1.1 | zh-CN (**only version that exists**) | unknown — no notice in the document | `unknown` | `repository` |

Retrieved 2026-09-04 from
`https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/datasheet/core/BM8563_V1.1_cn.pdf`
(HTTP 200, `%PDF` validated, text layer parses, cover heading cross-checked). Linked from **both**
the DinMeter and DinMeter v1.1 documentation pages.

---

## Used By

### M5Stack DinMeter (K134) and DinMeter v1.1 (K134-V11)

Fitted as **`U5`**, 8-pin (`OSCI`, `OSCO`, `INT`, `VSS`, `SDA`, `SCL`, `CLKOUT`, `VDD`), on the
**internal** I²C bus — **SCL GPIO12, SDA GPIO11** — which is *separate* from the PORT.A Grove
bus (GPIO15/13). Crystal `Y2` = 32.768 kHz ±20 ppm 12.5 pF with `C28`/`C29` 6.0 pF. Supplied
from `+3.3V`; `VBAT_IN` reaches the RTC section through `D5` so timekeeping survives the power
latch opening.

Its open-drain `INT` is one of the two wake sources for the board's power latch (the other is
the encoder push-button on GPIO42) — an RTC alarm can power the whole device back up from a
latched-off state. On the schematic `INT` carries a 10 kΩ pull-up whose designator text reads
`R20` but which has no recoverable `CO` marker; see
[`devices/m5stack/dinmeter/pinouts-and-buses.md` §6](../../../devices/m5stack/dinmeter/pinouts-and-buses.md#6-reference-designator-census-and-three-that-do-not-resolve).

→ [`devices/m5stack/dinmeter/features/rtc-and-timekeeping.md`](../../../devices/m5stack/dinmeter/features/rtc-and-timekeeping.md)

### Xteink X4 Pro and X4 Classic — *added 2026-09-04*

Both S3-based Xteink e-readers carry a BM8563 at the standard **I²C 0x51**, on the
shared **SDA 39 / SCL 38 @ 400 kHz** bus, Arduino controller 0 (`Wire`).

The vendor's own stock firmware names the part explicitly: the class
`XTEink::BM8563Driver` appears in the X4 Pro flash dump, with driver init at IROM
`0x420a2834` adding device 0x51 and the bus object configured `{39, 38, 400000}`.
That is an unusually direct confirmation — most identifications of this part come
from an address plus a working driver, which cannot distinguish it from a PCF8563.

The FreeInk SDK models it as `RtcType::Pcf8563`, i.e. it drives the register-compatible
equivalent, and reports it **"confirmed found and initializing on hardware"**.

| | [X4 Pro](../../../devices/xteink/x4-pro/README.md) | [X4 Classic](../../../devices/xteink/x4-classic/README.md) |
|---|---|---|
| Address | 0x51 | 0x51 |
| Bus | SDA 39 / SCL 38 @ 400 kHz | SDA 39 / SCL 38 @ 400 kHz |
| Bus neighbours | [GT911](../../goodix/gt911/README.md) 0x5D, [CW2017](../../cellwise/cw2017/README.md) 0x63 | CW2017 0x63, [QMI8658](../../qst/qmi8658a/README.md) 0x6B |
| Backup power | **unknown** — no teardown exists for either device | same |
| `INT` used as a wake source | **not established** | **not established** |

**Family contrast worth recording:** the two ESP32-C3 Xteink devices answer
differently. The [X3](../../../devices/xteink/x3/README.md) uses an
[unidentified DS-series RTC at 0x68](../../unidentified/xteink-x3-x4/rtc-ds-series/README.md)
— a different part at a different address, whose exact identity is an
[open three-way conflict](../../../devices/xteink/x3/gaps-and-conflicts.md) — and
the [X4](../../../devices/xteink/x4/README.md) has **no RTC at all**. Four devices
from one vendor, three different answers.

→ [`devices/xteink/x4-pro/features/rtc.md`](../../../devices/xteink/x4-pro/features/rtc.md)
