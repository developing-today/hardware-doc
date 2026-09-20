# CellWise CW2017 — I²C battery fuel gauge

- **Category:** single-cell Li-ion state-of-charge gauge, I²C.
- **Manufacturer:** Shenzhen CellWise Microelectronics (深圳市赛微微电子).
- **Research status:** ⚠ Identified from **firmware reverse engineering plus a
  live I²C register dump**. No datasheet retrieved.
- **Retrieved:** 2026-09-04

The battery gauge of the **Xteink X4 Pro** and **X4 Classic**.

## 1. What is established

| Property | Value | Evidence |
|---|---|---|
| I²C address | **0x63** (the part's default) | live bus scan + board profile |
| Bus speed used | 400 kHz | board profile |
| **State of charge** | register **`0x04`** | `BatteryMonitor`, from OEM RE |
| **Cell voltage** | registers **`0x02`/`0x03`**, 14-bit, **`mV = (raw·5 + 8) >> 4`** | same |
| **Battery profile (BATINFO)** | **80 bytes**, registers **`0x10`–`0x5F`** | same |
| **Reports 0 % until the profile is loaded** | yes | same |
| **Current register** | **NONE** | same |
| Charge-state observability | **not observable from the gauge** | same |
| SDK type | `GaugeType::Cw2017` | `BoardConfig.h` |

## 2. How it was identified — a nice piece of evidence

The address alone was ambiguous. The identification came from an **I²C register
dump of the live bus**: registers `0x10`–`0x3F` showed *"the classic BATINFO
battery-model curve"*, and 0x63 is the CW2017's default address.

That mattered because an earlier hypothesis held that **0x63 was a display
power-management IC** and that the X4 Pro's panel had dead rails needing an
external supply. That narrative sent the bring-up down a long false path. Reading
the register contents rather than guessing from the address killed it.

**Reusable lesson:** an I²C address is a weak identifier. A register dump that
shows a recognisable data *shape* is a strong one.

## 3. The BATINFO profile — the active defect risk

**A CW2017 with no resident profile reports 0 % forever.** It does not error; it
just reads flat.

`BatteryMonitor` therefore:
1. verifies the resident profile at `0x10`–`0x5F`;
2. **re-uploads the OEM 80-byte table** (recovered from the stock firmware's
   `Cw2017PowerHal` class via Ghidra) if it is missing;
3. then reads SoC from `0x04`.

Any firmware that talks to this gauge without doing step 2 will show a
permanently empty battery on a healthy device. **This is the highest-consequence
software fact about the X4 Pro's power path.**

## 4. Charging state must come from elsewhere

The CW2017 has **no current register**, and on both Xteink boards there is **no
charger IC on the gauge's I²C bus**. So the gauge cannot tell you whether the
device is charging.

Both boards solve it the same way: a **charger `STAT` line on GPIO21**, configured
input / no-pull and read **active-HIGH** (raw level = charging). `BatteryMonitor`
falls back to this pin when the gauge reports charging as unobservable.

## 5. Datasheet

**Not retrieved.** No public CellWise portal was reached this session. The
register semantics above come from firmware RE and are consistent with published
CW2015/CW2017 driver code in the wild, but **have not been checked against a
vendor document**. Treat the voltage formula in particular as
`reported-working`, not `datasheet-confirmed`.

## 6. Caveats and unsafe assumptions

- **Do not assume a fresh or replaced cell keeps the profile valid.** The BATINFO
  table models a *specific* cell chemistry and capacity. Neither Xteink board's
  battery capacity is documented, so the table cannot be audited.
- Do not assume the CW2015 register map applies unchanged.
- **Do not read charge state from this part.** Use the STAT GPIO.

---

## Used By

### [Xteink X4 Pro](../../../devices/xteink/x4-pro/README.md)

At **0x63** on the shared I²C bus **SDA 39 / SCL 38 @ 400 kHz**, alongside the
[GT911 touch controller](../../goodix/gt911/README.md) (0x5D) and the
[BM8563 RTC](../../generic/bm8563/README.md) (0x51), all on Arduino controller 0
(`Wire`). Charge STAT on **GPIO21**, active-HIGH — recovered from
`Cw2017PowerHal` vtable slot 3 → IROM `0x4214f67c`, pin `0x15` set in board init
`0x4214eeb0`. Battery capacity is **unknown**.

→ [`devices/xteink/x4-pro/features/battery-and-power.md`](../../../devices/xteink/x4-pro/features/battery-and-power.md)
→ [`devices/xteink/x4-pro/pinouts-and-buses.md`](../../../devices/xteink/x4-pro/pinouts-and-buses.md)

### [Xteink X4 Classic](../../../devices/xteink/x4-classic/README.md)

Identical: **0x63** on **SDA 39 / SCL 38 @ 400 kHz**, sharing the bus with the
BM8563 RTC (0x51) and a [QMI8658 IMU](../../qst/qmi8658a/README.md) (0x6B).
Charge STAT again **GPIO21** active-HIGH, though the SDK marks the **polarity as
`PENDING`** on this board.

→ [`devices/xteink/x4-classic/README.md`](../../../devices/xteink/x4-classic/README.md)

## See also

The other two Xteink battery approaches, for contrast:
[`../../texas-instruments/bq27220/README.md`](../../texas-instruments/bq27220/README.md)
(X3 — a real impedance-track gauge, **no profile upload needed**) and the
[X4](../../../devices/xteink/x4/features/battery-and-power.md) (a bare ADC).

---

## Datasheet — **not obtained**, 2026-09-11

The record above states *"No datasheet retrieved."* That is still true, and this
section records what was tried so it is not repeated.

| Source tried | Result |
|---|---|
| `http://www.cellwise-semi.com/` (CN) | **200** — site is live and reachable |
| `http://en.cellwise-semi.com/` | **200** |
| `…/products/index?ptype=voltameter&voltage=电压型` (voltage-type gauges) | 200, **no `CW2017` on the page** |
| `…/Home/Index/products` (full product index) | 200 — parts listed are **CW1011, CW2015, CW2215, CW3301, CW6004, CW6301, CW6305, CW6307, CW6308, CW6602, CW6603**. **No CW2017** |
| `https://www.cellwise-semi.com/uploads/CW2017.pdf`, `/upload/CW2017.pdf` | connection failure / not found |
| **LCSC** `wmsc.lcsc.com/ftps/wm/search/global?keyword=CW2017` | **403 on every UA tried** (Chrome, WhatsApp, ClaudeBot) |
| GitHub code search `filename:CW2017 extension:pdf` | **`total_count: 0`** |
| DuckDuckGo HTML endpoint | **HTTP 202 bot-check**, no results |

### The finding, not just the failure

**CW2017 is not in CellWise's own public catalogue.** Its closest listed
siblings are **CW2015** and **CW2215**, both voltage-type single-cell gauges.
Three readings are possible and the evidence does not choose between them:

1. the part is a customer-specific or China-only variant never catalogued;
2. it is superseded and the page was removed;
3. it is catalogued only in a region or behind a login not reachable from here.

**This is a real unavailability, not a lazy search.** The part is confirmed
present and working on hardware — a third party read it on the live I²C bus of a
physical X4 Pro at `0x63` on 2026-09-06
([`kycube/x4pro-emu` `docs/hardware.md`](https://github.com/kycube/x4pro-emu/blob/bf4b86ae0471012d4d07c0bb3042f3f561c9c302/docs/hardware.md)) —
but its datasheet is not public.

### What the working behaviour already establishes, without a datasheet

From FreeInk's driver plus the live-bus observation, and now independently
restated by a second firmware project:

| Register | Meaning |
|---|---|
| `0x04` | State of charge (%) |
| `0x02` / `0x03` | VCELL, 14-bit; **mV = (raw × 5 + 8) >> 4** |
| `0x10`–`0x5F` | **80-byte BATINFO profile.** Until it is written, SoC reads 0 % |

That mV conversion and the 80-byte profile window are the two facts a datasheet
would normally supply, and both are now corroborated by two independent code
bases and one live-bus reading. **The remaining unknowns are the alert/threshold
registers, the sleep behaviour, and what the correct BATINFO curve is for the
actual cell** — and none of those can be answered from code.

### What would settle it

1. **Chinese-language search**: `CW2017 规格书`, `CW2017 数据手册`,
   `赛微微电 CW2017` (CellWise = 深圳市赛微微电子). Not attempted this pass.
2. **LCSC HTML storefront** `https://www.lcsc.com/search?q=CW2017` with UA
   `WhatsApp/2.23.20.0` — the JSON API 403s but the HTML page returned 200 and
   was not mined.
3. **A CW2015 datasheet as a proxy.** CW2015 *is* catalogued. Its register map is
   likely close, and the differences would themselves be informative — but
   **a proxy must never be recorded as this part's datasheet.**
4. Ask the FreeInk authors, who wrote a working driver and presumably had
   something to write it from.

**Used by:** [Xteink X4 Pro](../../../devices/xteink/x4-pro/README.md) ·
[Xteink X4 Classic](../../../devices/xteink/x4-classic/README.md).
