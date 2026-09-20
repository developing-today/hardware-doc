# RTC — M5Stack PaperMono

> **How do I keep time, and how do I schedule a wake-up?**
> Hardware revision **V0.6.2** · snapshot **2026-09-01** · nothing tested on hardware.

**This guide is short.** Keeping time is ordinary; the PaperMono-specific fact is that
the RTC's alarm interrupt goes to the **power manager**, so a scheduled wake works with
the ESP32-S3 completely unpowered.

## 1. Capability summary and the hardware path

A Seiko Epson RTC on the shared system I²C bus, powered from the **L1** rail.

```
RX8130CE (I2C 0x32)
   ├─ SDA/SCL ──▶ system I²C bus (GPIO47/48), 400 kHz
   ├─ nIRQ ─────▶ PYG0_RTC_INT ──▶ M5PM1 pin 3 (G0)     <- NOT the ESP32-S3
   └─ VDD   ◀─── 3V3_L1, enabled by M5PM1 LDO3V3_EN_PP
```

| Element | Part | Record |
|---|---|---|
| RTC | Seiko Epson **RX8130CE**, `0x32` | [`components/seiko-epson/rx8130ce/`](../../../../components/seiko-epson/rx8130ce/) — **record is written**: the datasheet artifact is held, the write-up is not yet done |
| Interrupt destination | **M5PM1 `G0`** | [`components/m5stack/m5pm1`](../../../../components/m5stack/m5pm1/README.md) · [`power-and-sleep.md`](power-and-sleep.md) |

## 2. ⚠ The alarm interrupt lands on the power manager

As with the [IMU](imu.md), there is **no path from the RTC to any ESP32-S3 GPIO**.
Configuring an ESP32 wake source for an RTC alarm will never fire.

The shipped factory binary confirms both destination and polarity:

```
PM1 shutdown, wake by RX8130 timer  -> PM1 G0 falling edge
```

M5Unified sets the board up accordingly (`Power_Class.cpp:528` onward):
`_rtcIntPin = GPIO_NUM_1` — note that is the **M5PM1's IRQ output to the host**, not the
RTC line — with `setGPIOIRQMaskBits(0x1E)` to *enable GPIO0's interrupt and disable the
other four*, `G0` configured as a plain input, and `G1` configured as a push-pull IRQ
output toward the ESP32-S3.

So the chain when the host is awake is:
**RX8130CE `nIRQ` → M5PM1 `G0` → M5PM1 `G1` → ESP32-S3 GPIO1.**
When the host is asleep in L1, the chain stops at the M5PM1 and the M5PM1 powers the host
back up.

## 3. Prerequisites

| Item | Value |
|---|---|
| M5Unified | 0.2.21 — `M5.Rtc`, backed by `RX8130_Class` at **400 kHz** (`RTC_Class.cpp:60`) |
| M5PM1 | 1.0.7, for wake configuration |

The factory firmware just aliases it: `m5::RTC_Class& rtc = M5.Rtc;` (`hal.h:70`).

## 4. Resources consumed

| Resource | Value |
|---|---|
| I²C address | **`0x32`** on the shared bus at **400 kHz** (`RX8130_I2C_FREQ_HZ = 400000`) |
| M5PM1 pin | `G0`, input, wake-enabled, falling edge |
| ESP32-S3 GPIO | **none** directly; GPIO1 carries the M5PM1's IRQ when the host is awake |
| Rail | `3V3_L1` — alive in state **L1** and above |
| RTC RAM | The factory firmware uses **4 bytes from `0x20`** (`RX8130_RAM_BASE = 0x20`, `RX8130_RAM_SIZE = 4`) |

Two other retention stores exist and are unused on this board: the M5PM1's **32 bytes**
at `0xA0`–`0xBF`, and the M5IOE1's **32 bytes** at `0x70`–`0x8F`. Both survive states in
which the ESP32-S3 is unpowered, which makes them useful for cross-sleep state — nothing
in vendor firmware touches them.

## 5. Minimal procedure (`inferred`)

```cpp
#include <M5Unified.h>

void setup() {
  M5.begin(M5.config());

  auto dt = M5.Rtc.getDateTime();          // as used at app_clock.cpp:563, :1123
  // ... set it:
  // m5::rtc_datetime_t t{{2026,9,1,2},{12,0,0}};
  // M5.Rtc.setDateTime(&t);               // app_clock.cpp:1043
}
```

`M5Unified`'s `RX8130_Class` exposes `getDateTime`, `setDateTime`,
`setTimerIRQ(uint32_t msec)`, `setAlarmIRQ(date, time)`, `getIRQstatus()`, `clearIRQ()`,
`disableIRQ()` and **`getVoltLow()`** (`RX8130_Class.cpp:37`, `:94`, `:119`, `:212`,
`:272`, `:280`, `:287`, `:295`).

`getVoltLow()` is the one worth wiring into a first-boot path: it tells you the RTC lost
its supply and the time is not trustworthy.

## 6. Scheduled wake — two routes

### 6.1 The M5PM1's own timer (simpler)

The M5PM1 has an independent 31-bit second timer and does not need the RTC at all:

```cpp
pm1.timerSet(600, M5PM1_TIM_ACTION_POWERON);   // wake in 10 minutes
pm1.shutdown();
```

Actions: `STOP`, `FLAG`, `REBOOT`, `POWERON`, `POWEROFF`. Registers `0x38`–`0x3B` counter,
`0x3C` config, `0x3D` reload key (`0xA5`). This is the vendor's own published sketch —
see [`power-and-sleep.md` §6.1](power-and-sleep.md#61-timed-power-off--power-on-reported-working--vendors-own-sketch).

### 6.2 The RX8130CE alarm (calendar-accurate)

Use the RTC when you need a wall-clock alarm — "07:30 every weekday" — rather than an
elapsed interval:

```cpp
M5.Rtc.setAlarmIRQ(&date, &time);
pm1.gpioSetWakeEnable(M5PM1_GPIO_NUM_0, true);
pm1.gpioSetWakeEdge  (M5PM1_GPIO_NUM_0, M5PM1_GPIO_WAKE_FALLING);
pm1.setLdoEnable(true);
pm1.ldoSetPowerHold(true);       // keep L1 (and therefore the RTC) alive
pm1.shutdown();
```

`inferred` — this composes the vendor's IMU-wake pattern with `G0` instead of `G4`. The
factory firmware **disables** both wake sources at startup
(`clearPm1WakeIrqState()`, `hal_board.cpp:42–43`), so it does not itself demonstrate the
RTC-wake path end to end. The shipped binary's log string shows the path exists.

### Decision table

| Need | Use |
|---|---|
| "Wake me in N seconds" | **M5PM1 timer** (§6.1) — no RTC involvement, vendor-demonstrated |
| "Wake me at 07:30" | **RX8130CE alarm** (§6.2) |
| "Reboot if I hang" | M5PM1 **watchdog** — `wdtSet(sec)` / `wdtFeed()`, registers `0x0A`/`0x0B` |
| Periodic host-side tick while awake | `setTimerIRQ(msec)` on the RTC, routed via M5PM1 `G1` → GPIO1 |

## 7. Limits

| Class | Limit |
|---|---|
| **Board** | `nIRQ` goes only to the M5PM1 (§2) |
| **Board** | The RTC is on `3V3_L1`. **In state L0 (shipping) the RTC is not powered** — there is no separate coin cell or supercap in evidence. Time is lost on a full L0 transition |
| **Documentation** | The only RTC datasheet mirrored by M5Stack is **Chinese-language** (`RX8130CE_cn-Register-Datasheet.pdf`) |
| **Framework** | M5Unified drives it at 400 kHz |
| **Observed** | Nothing. No drift, accuracy or long-term timekeeping report exists |

> The L0 consequence is worth restating: the vendor's state table puts only the charger,
> protection and `3V3_L0` in L0, with L1 (RTC + IMU) above it. So the deepest state costs
> you the clock. If your product must keep time indefinitely, **do not go to L0** —
> `ldoSetPowerHold(true)` keeps L1 up.

## 8. Conflicts

| Combination | Verdict | Mechanism |
|---|---|---|
| RTC + [IMU](imu.md) wake | ✅ | Different M5PM1 GPIOs (`G0` / `G4`); both can be enabled |
| RTC + [touch](touch.md) wake | ⚠ | RTC wakes from L1, touch only from L2 |
| RTC + other I²C devices | ✅ | Distinct addresses; 400 kHz |
| RTC + state L0 | ❌ | RTC unpowered (§7) |
| RTC + [charger](battery-and-charging.md) bus access | ⚠ | The usual shared-bus hazard |

## 9. Debugging

| Symptom | Cause |
|---|---|
| Alarm never wakes the board | Configured on an ESP32-S3 pin instead of M5PM1 `G0` (§2) |
| Time resets on every power cycle | You reached **L0**; the RTC rail is L1 (§7) |
| `getVoltLow()` true | RTC supply was lost — treat the time as invalid |
| Wake fires but the RTC is dead afterwards | `ldoSetPowerHold(true)` not set |
| Interrupt latched forever | `clearIRQ()` after handling |

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**; the RX8130CE is fitted on both C153 and C153-LITE |
| Framework range | M5Unified 0.2.21 · M5PM1 1.0.7 |
| Evidence | Wiring: **schematic**. Wake destination and polarity: **shipped binary + firmware**. `M5.Rtc` API: **read from `RX8130_Class`**. §6.2 sketch: **`inferred`** — no vendor code demonstrates RTC wake end to end |
| Confidence | High on the interrupt path; medium on the alarm-wake sketch; **none on accuracy** |
| Last verified | **2026-09-01** |

## Related

- [`power-and-sleep.md`](power-and-sleep.md) · [`imu.md`](imu.md) · [`../power-architecture.md#wake-sources-and-how-they-reach-the-m5pm1`](../power-architecture.md#wake-sources-and-how-they-reach-the-m5pm1)
- [`components/seiko-epson/rx8130ce/`](../../../../components/seiko-epson/rx8130ce/) (stub) · [`components/m5stack/m5pm1`](../../../../components/m5stack/m5pm1/README.md)
