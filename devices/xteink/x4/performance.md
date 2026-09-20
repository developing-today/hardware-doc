# Xteink X4 — performance

> **Nothing was measured by this session.** The figures below are the only
> quantitative performance data that exists for any Xteink device, and all of it
> comes from one source. Retrieved **2026-09-04**.

## Display plane-write timing

| Configuration | Plane write | Spec status | Source |
|---|---:|---|---|
| **20 MHz** — FreeInk default | **~38 ms / refresh** | SSD1677 datasheet write maximum | **[SDK]** `BoardConfig.h:830–843` |
| **40 MHz** — `-DFREEINK_X4_OVERCLOCK_SPI` | **~19 ms** (saves ~17–20 ms) | **2× datasheet. Out of spec** | same |

Method, environment, sample count and instrumentation are **not stated** by the
source. Treat these as **developer-reported indicative figures**, not measurements
with error bars. They are recorded because they are the only numbers in the
subject and because the trade-off they describe is real and actionable.

The 40 MHz mode is what the **CrossPoint / Witch Reader** fork shipped. The SDK
made it opt-in and warns it *"can glitch plane writes on marginal wiring"* — a
glitched plane write is a visibly corrupt page, not a crash.

**A trap in the same code:** `Ssd1677Driver`'s internal default is **40 MHz**, so
any board profile leaving `displaySpiHz = 0` runs **out of spec silently**. The X4
profile sets it explicitly for exactly this reason.

## Button ADC — the only multi-unit data in the family

Raw 12-bit readings from **three physical devices** (**[SDK]** `InputManager.cpp:29–45`):

| | BACK | CONFIRM | LEFT | RIGHT |
|---|---:|---:|---:|---:|
| unit 1 | 3597 | 2760 | 1530 | 6 |
| unit 2 | 3470 | 2666 | 1480 | 6 |
| unit 3 | 3470 | 2655 | 1470 | 3 |
| **mean** | **3512** | **2694** | **1493** | **5** |
| spread | 3.6 % | 3.9 % | 4.0 % | — |

**n = 3.** Unit-to-unit spread is ~4 % at the top of the ladder — small, but the
SDK deliberately derives thresholds as **midpoints between adjacent means** rather
than fixed values because they are *"much more tolerant of different devices"*.

This is the only place in the Xteink subject where anyone sampled more than one
physical unit.

## What has never been measured

| Quantity | Status |
|---|---|
| **Battery capacity** | **Unknown.** The X3 is 650 mAh by teardown; the X4 is unmeasured |
| **Runtime** | No figure from any source |
| **Active current** | Never measured |
| **Sleep current** | Never measured — and the X4 **cannot power down its SD card**, so it is structurally worse than the X3 here |
| **Boot time** | Never measured |
| **Wi-Fi throughput / range** | Never measured |
| **SD read/write rate** | Never measured. The card **shares the display SPI bus**, so any figure would be workload-dependent |
| **Page-turn latency, end to end** | Never measured — the ~38/19 ms figures are *plane writes*, not full refreshes including waveform time |

## The measurement that was attempted and abandoned

The author of the [X3 teardown](../x3/media.md) stated their purpose plainly:

> "…so I can attach a **Nordic Power Profiler Kit II** to it to see if I can make
> any power optimizations to crosspoint firmware."
> — [r/xteinkereader `1uksv6s`](https://old.reddit.com/r/xteinkereader/comments/1uksv6s/), 2026-07-01

**No results were ever posted.** That is the closest anyone has come to
instrumenting this board family, and it produced nothing. Recorded so the next
person knows the attempt was made.

## Known performance failure

**Out-of-memory during OTA** on the C3 devices. CrossPoint abandoned GitHub
releases as an update channel because *"it causes out of memory issues on the x3"*
([r/XTEINK `1uek163`](https://old.reddit.com/r/XTEINK/comments/1uek163/), 2026-06-24).
The X4 shares the SoC and the **absence of PSRAM**, which is the root cause.

This is the clearest practical performance difference between the C3 and S3
generations: the [X4 Pro](../x4-pro/README.md) and X4 Classic have **8 MB PSRAM**
and support multi-buffer rendering and damage-window partial refresh; the X4
cannot.

## Honest summary

**Two indicative timing figures and one three-unit ADC sample.** Everything a
buyer or developer would actually want to know — battery life, sleep current,
refresh latency — is **unmeasured by anyone**.
