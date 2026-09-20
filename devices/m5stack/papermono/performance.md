# Performance — M5Stack PaperMono

> Research snapshot **2026-09-01**.
>
> ## ⚠ Read this before anything else on this page
>
> **No performance measurement of this device exists.** Not from M5Stack, not from any
> independent party, and not from this research pass. There is **no** power figure for any of its
> five power states, **no** battery runtime, **no** boot time, **no** Wi-Fi or LoRa throughput or
> range, **no** microSD throughput, **no** NFC read latency and **no** thermal data.
>
> This page therefore contains **four kinds of number and no measurements**:
>
> | Kind | What it is | Where it appears |
> |---|---|---|
> | **Official claim** | The vendor states it; nobody has reproduced it | §2 |
> | **Component specification** | A component maker's datasheet figure, under *that maker's* conditions | §3 |
> | **Silicon claim** | A property of the ESP32-S3 die, not of this board | §4 |
> | **Absence** | Nothing exists. **The largest section on this page** | §5 |
>
> **There is no fifth column.** Nothing here is an independent measurement, a locally reproduced
> result or an estimate. Where a comparison cannot be supported it is marked **unresolved**
> rather than given invented precision.

## Contents

- [1. Why this page exists in this state](#1-why-this-page-exists-in-this-state)
- [2. The vendor's M5GFX refresh timings](#2-the-vendors-m5gfx-refresh-timings)
- [3. Component-level specifications](#3-component-level-specifications)
- [4. ESP32-S3 silicon claims — not device measurements](#4-esp32-s3-silicon-claims--not-device-measurements)
- [5. What does not exist](#5-what-does-not-exist)
- [6. The asymmetry inside M5Stack's own catalogue](#6-the-asymmetry-inside-m5stacks-own-catalogue)
- [7. What would actually settle these questions](#7-what-would-actually-settle-these-questions)
- [8. Reasoning that is available without measurement](#8-reasoning-that-is-available-without-measurement)

---

## 1. Why this page exists in this state

The PaperMono's defining engineering feature is a **five-state hardware power architecture**
implemented in a second microcontroller, with the RTC and IMU interrupts terminating on the power
manager so the application processor can be unpowered between events
([`power-architecture.md`](power-architecture.md)). It is marketed for "low-power IoT and embedded
applications".

**And no current figure for any of those five states has ever been published or measured.**

The power-state table in the vendor's own schematic says what is *powered* in each state. It
never says what it *costs*. That gap is tracked as
[G7](gaps-and-conflicts.md#g7--no-power-or-battery-life-figure-exists) and it is the single most
consequential unknown about this product: the one specification that would justify choosing it
over its own predecessor is the one nobody has.

Writing a plausible number here would be worse than writing none. So the deliverable of this page
is the **inventory of absence** in §5, plus the honest labelling of the few numbers that do exist.

## 2. The vendor's M5GFX refresh timings

These four numbers are the only performance figures M5Stack publishes for this board.

| Refresh mode | `epd_mode_t` | Vendor figure |
|---|---|---|
| Quality | `epd_quality = 1` | **4.71 s** |
| Text | `epd_text = 2` | **0.45 s** |
| Fast | `epd_fast = 3` | **0.34 s** |
| Fastest | `epd_fastest = 4` | **0.07 s** |

Source: the PaperMono product page (S01), under the heading *"M5GFX LUT Refresh Speed"*, with the
vendor's own caption: *"The following data is the laboratory test result of PaperMono under
different M5GFX refresh modes. The actual refresh time may vary depending on the display content
and operating environment, and is provided for reference only."*

**Evidence status: official claim, `not-tested`.** Now the four qualifications that must travel
with these numbers.

### 2.1 The configuration is unstated

The vendor gives no temperature, no supply voltage, no test pattern, no SPI clock, no library
version, no sample count and no variability. E-paper refresh time is strongly
content-dependent — the vendor says so itself — so "0.34 s" without a pattern is not a
reproducible figure. Compare the DKE panel manual, which at least states its own method: its
4-second maximum image update time is measured at 23 °C for a transition from a horizontal
2-scale pattern to a vertical 2-scale pattern, with the instrument named.

### 2.2 They may be for a LUT set that is no longer shipped

This is the qualification that matters most.

- **M5Stack states that the M5GFX waveforms for the PaperMono "are currently unstable"** and
  recommends the panel maker's OTP example instead, *for better panel life and refresh
  stability* (S01).
- **M5GFX `develop` has replaced the LUTs**, leaving 17 lines of the previous `lut_quality`
  commented out in-tree, and has added a new `_refresh_mode1_text()` code path (S47).
- **The factory firmware pins a M5GFX commit (`02107b82…`) older than either current branch.**

So the published timings correspond to some specific, unnamed build. **They should not be treated
as characteristic of any version you can check out today**, and they cannot be reproduced without
knowing which LUTs produced them.

### 2.3 The vendor-recommended path has no timings at all

M5Stack's own advice is to bypass M5GFX and drive the panel with the SSD1677's factory-programmed
OTP waveforms (`M5PaperMono-OTP-Demo`, S42). **No timing is published for that path anywhere.**
The four numbers above therefore describe the code path the vendor tells you not to use, and the
path it tells you to use is uncharacterised.

### 2.4 The same four numbers appear on the Lite's page, uncorrected

The PaperMono-Lite product page (S04) carries the identical four figures **with a caption that
still says "laboratory test results for PaperMono"**. They were copied, not separately measured.
Harmless — the two boards share a panel — but it establishes that these numbers are a single
measurement event, not a body of data.

### 2.5 What they are still good for

Read as an **order-of-magnitude guide to the shape of the trade-off**, they are useful and they
are corroborated in kind: a full-quality refresh is *seconds*, a partial refresh is *tenths of a
second*, and the ratio between them is roughly 15–70×. The DKE panel manual's independent
4-second maximum image update time sits in the same region as `epd_quality`'s 4.71 s, which is
weak but real cross-source agreement about the magnitude.

**One independent observation exists about refresh quality, and it is not a measurement.**
CNX-Software noted "epd_fastest – 0.07 s; **note: ghosting visible in demo**" — an observation of
M5Stack's own demo *video*, not of hardware. Consistent with the vendor's own precaution to
perform a full refresh after roughly ten partial refreshes.

## 3. Component-level specifications

These are **component-maker figures under that maker's own conditions**. They constrain what the
board can do; they are not statements about the board.

### 3.1 The DKE panel's optical figures

From the panel manual's optical table (**p. 5**, measured with an Eye-One Pro spectrophotometer):

| Symbol | Parameter | Conditions | Min | Typ | Max | Unit |
|---|---|---|---:|---:|---:|---|
| `KS` | Black state L* | | – | **24** | 30 | |
| `WS` | White state L* | | **58** | **62** | – | |
| `WS` | **White ghosting ΔL** | Full display mode | – | **1** | – | |
| `WS` | White ghosting ΔL | Partial display mode | – | **1** | – | |
| `WS` | White ghosting ΔL | Full-partial display mode | – | **1** | – | |
| `R` | **White reflectivity** | White | **26** | **30** | – | **%** |
| `CR` | **Contrast ratio** | **Indoor** | **5** | **7** | – | |
| `GN` | **`2Grey Level`** | – | – | – | – | |
| `Life` | | 23 ± 3 °C, 55 ± 10 %RH | | **5 years** | | |

`CR` is defined by the manual as surface reflectance with all white pixels divided by surface
reflectance with all black pixels.

**How to read these.** A contrast ratio of 5–7 with 26–30 % white reflectance is an **e-paper**
figure, not an LCD figure — roughly newsprint. It is specified **indoor**; a reflective display
generally improves in daylight, but that is not what this row states and no outdoor figure
exists. The ghosting ΔL of typically 1 is the manufacturer's claim under **its own waveform**,
which matters enormously — see the note below.

**The `GN — 2Grey Level` row is an unresolved conflict.** M5Stack markets 4-level greyscale and
its OTP demo implements a working four-grey mode; the manual's optical table says two, and the
manual's overview describes 1-bit black and white. Three readings are plausible and nothing in
evidence chooses between them. The least-risky assumption is that `GN` documents the *optically
characterised* levels rather than the achievable ones — under which four-grey works but **the
optical figures above do not apply to the intermediate levels**. Full analysis in the
[panel component record](../../../components/dke/depg0397bbs770f3/README.md) and
[C1](gaps-and-conflicts.md#c1--4-grey-levels-versus-2).

**The 5-year life figure is a storage/ambient statement, not a refresh-count endurance rating.**
The manual gives **no maximum refresh count anywhere** — which is exactly the number you would
want when choosing between refresh modes on a device the vendor warns can be permanently damaged
by continuous partial refresh.

### 3.2 The DKE panel's electrical figures

From the manual **p. 10, §6.2**, conditions `VSS = 0 V`, `VCI = 3.0 V`, `TOPR = 23 °C`:

| Parameter | Symbol | Conditions | Typ | Max | Unit |
|---|---|---|---:|---:|---|
| Typical operating current | `Iopr_VCI` | VCI = 3.0 V | – | **12** | mA |
| **Image update time** | – | 23 °C | – | **4** | **sec** |
| Typical peak current | `Iopr_VCI` | 2.3–3.6 V | **120** | – | mA |
| Deep-sleep mode current | `Idslp_VCI` | DC/DC off, no clock, no input load, RAM not retained | – | **1 … 5** | µA |

Operating temperature `TOPR` **0 to +50 °C**; storage `TSTG` −25 to +70 °C.

> ⚠ **The most consequential sentence in the panel's electrical section is note 3:** *"the listed
> electrical characteristics are only guaranteed under the controller & waveform provided by
> DKE"*. **M5GFX does not use that waveform** — it uploads its own LUTs from flash. So every
> figure in this table, including the 4-second update time, the 120 mA peak and the 12 mA
> operating current, is **untested for the M5GFX path**. The vendor's own recommendation to prefer
> the OTP demo follows directly from this sentence.

**Practical reading.** The 120 mA peak is the number that matters for battery and rail design: a
refresh is a current *event*, not a steady load, and it lands on the `EPD_3V3_L3B` rail alongside
whatever else is in the L3B group. The 1–5 µA deep-sleep figure is what makes an e-paper device
plausible at all in state L0/L1 — but it is the **panel's** contribution, and the board also
contains an always-on LDO, an M5PM1, an RTC and a charger. **The board-level idle current is not
the panel's deep-sleep current, and nobody has measured the difference.**

The panel's **0 to +50 °C operating range is the binding environmental constraint** on the whole
device: the SSD1677 die is rated −25 to +85 °C, so reasoning from the controller datasheet alone
over-estimates the envelope by 25 °C at one end and 35 °C at the other. Below 0 °C the ink is out
of specification and the OTP waveform bank does not extend there.

### 3.3 Other component figures that constrain the board

| Constraint | Figure | Source | Why it matters here |
|---|---|---|---|
| **SSD1677 maximum write clock** | **20 MHz** | SSD1677 datasheet §12.1 **and** DKE manual p. 16, independently | **M5GFX drives it at 40 MHz.** The vendor's own OTP demo uses 20 MHz. Unresolved, untested, and the most likely single cause worth investigating first for refresh instability — [C3](gaps-and-conflicts.md#c3--spi-clock-exceeds-the-panels-rated-maximum) |
| **AW9967 dimming input range** | **10–100 kHz** | AW9967 datasheet | **M5GFX programs the M5PM1 PWM at 5 kHz** — below the specified range, so dimming linearity and audible behaviour are not guaranteed. Software-fixable — [C5](gaps-and-conflicts.md#c5--frontlight-pwm-frequency-below-the-drivers-rated-range) |
| **Frontlight current** | schematic note claims `Iset = 15 mA` at `Rset = 11 R`; **fitted `R29` is 18 Ω**, giving roughly **11 mA** | schematic (S14) | The annotation is internally inconsistent with its own formula and appears stale. **Neither figure has been measured** — [C6](gaps-and-conflicts.md#c6--frontlight-current-annotation-contradicts-the-fitted-part) |
| **Charge current** | sheet 1 annotates `充电电流 0.5C` ≈ **575 mA** for the 1150 mAh cell | schematic (S14) | `inferred` from the annotation and the cell capacity. **The `ICHGSET` programming resistor was not resolved**, so this rests on the annotation alone |
| **Rail current limits** | `3V3_L2` DC-DC **600 mA**; the switched LDOs **400 mA** each | schematic (S14) | These are the headroom figures a designer needs. **What the board actually draws from them is unknown** |
| **Battery capacity** | **1150 mAh** | vendor specification | Against the PaperS3's 1800 mAh |

**None of these has been measured on a PaperMono.** They are datasheet and schematic readings.

## 4. ESP32-S3 silicon claims — not device measurements

These are properties of the die, and they are included so that nobody reasons from a device
absence to a silicon absence. **A silicon capability is not a device measurement**, and the method
requires the two to stay distinct.

| Property | Value | Note |
|---|---|---|
| Cores / clock | 2 × Xtensa LX7, **up to 240 MHz** | `CONFIG_ESP_DEFAULT_CPU_FREQ_MHZ_240=y` in the vendor's `sdkconfig.defaults`, so the shipped firmware does run at 240 MHz |
| Internal SRAM | 512 KB | |
| PSRAM | **8 MB octal, in package** | **Mandatory** on this board — M5GFX refuses to initialise the display without it |
| Flash | 16 MB external `XM25UH128DHIQT`, quad-capable | Header reports DIO; hardware supports QIO ([R2](gaps-and-conflicts.md#r2--qio-versus-dio-flash--resolved)) |
| Wi-Fi | **802.11 b/g/n, 2.4 GHz only** (Wi-Fi 4), 20/40 MHz channels | |
| Bluetooth | **Bluetooth 5 LE and Mesh. No Classic (BR/EDR) — a hardware absence** | No IDF version, Arduino core or library can add BR/EDR. See the [component record](../../../components/espressif/esp32-s3r8/README.md#radio-capabilities-and-the-classic-bluetooth-limitation) |
| Vector extensions | **PIE** 128-bit SIMD (TRM ch. 1) | Relevant to pixel-format conversion for the framebuffer. **Not known to be used by any code on this board** |

**Two warnings about using this table.**

*Do not translate silicon numbers into device numbers.* "240 MHz dual-core" says nothing about
this board's boot time, and "Wi-Fi 4" says nothing about its throughput through an FPC antenna
inside a plastic case beside an e-paper panel. Antenna performance is a board property and **no
antenna characterisation exists for this board at all**.

*One silicon-level caveat applies directly and is worth checking.* The in-package octal PSRAM is
subject to the ESP32-S3's documented **120 MHz octal-PSRAM temperature fragility** — see
[`guides/espressif/esp-idf-peripheral-capabilities.md`](../../../guides/espressif/esp-idf-peripheral-capabilities.md#43-esp32-s3--120-mhz-octal-psram-is-temperature-fragile).
Nothing in the vendor's `sdkconfig.defaults` selects 120 MHz PSRAM, so the shipped configuration
is not exposed to it; a build that raises the PSRAM clock would be. `inferred`, `not-tested`.

## 5. What does not exist

**This is the deliverable of this page.** Every row is an explicit gap, not an omission.

| Workload | What is missing | Vendor figure? | Independent figure? | Derived here? |
|---|---|---|---|---|
| **Power — state L0 (shipping)** | quiescent current | **none** | none | none |
| **Power — state L1 (standby)** | current with RTC + IMU alive | **none** | none | none |
| **Power — state L2 (deep sleep)** | current with the ESP32-S3 powered but asleep | **none** | none | none |
| **Power — L3A / L3B (active)** | current with panel / frontlight / SD / mic up | **none** | none | none |
| **Battery runtime** | hours or days in any duty cycle | **none** | none | none |
| **Frontlight power** | current at any brightness | **none** — and even the *design* current is contested (§3.3) | none | none |
| **Boot time** | cold boot to first pixel; wake-from-L1 to first pixel | **none** | none | none |
| **Wi-Fi** | throughput, range, RSSI, antenna pattern, TX current | **none** | none | none |
| **Bluetooth LE** | anything at all — **BLE is not even in the vendor's specification table** | **none** | none | none |
| **LoRa** | range, link budget, sensitivity, TX current, TCXO vs XTAL, `SX_ANT_SW` semantics | **none**; **no `Stamp-LoRa-1262` module datasheet exists anywhere** ([G5](gaps-and-conflicts.md#g5--no-stamp-lora-1262-module-datasheet-exists-anywhere-located)) | none | none |
| **NFC** | read range, read latency, which card types actually interoperate | **none** | none | none |
| **microSD** | read/write throughput, capacity or filesystem limits | **none** | none | none |
| **Microphone** | SNR, sensitivity, sample rates beyond the 16 kHz the demo uses | **none** — **no datasheet for `LMD4737T261-AC02` exists anywhere** ([G6](gaps-and-conflicts.md#g6--three-parts-have-no-obtainable-datasheet)) | none | none |
| **Touch** | latency, accuracy, report rate | **none** | none | none |
| **Display (OTP path)** | refresh timings for the path the vendor **recommends** | **none** (§2.3) | none | none |
| **Display endurance** | maximum refresh count before degradation | **none** — the panel manual omits it | none | none |
| **Thermal** | any temperature, anywhere, under any load | **none** — **no operating-temperature range is published for the product at all** | none | none |
| **PSRAM / memory bandwidth** | framebuffer fill rate, DMA contention | **none** | none | none |
| **Concurrent workloads** | e-paper refresh + microSD + Wi-Fi together | **none** | none | none |

**Every cell in the last three columns is empty**, and the vendor column is empty for every row.
That is twenty-odd workloads with zero data points.

The concurrency row deserves separate mention because it is the case most worth testing first,
and [`resources-and-conflicts.md` §10](resources-and-conflicts.md#10-realistic-simultaneous-use-scenarios)
already works out *why*: there is no pin conflict between an e-paper refresh, an SDMMC transfer
and Wi-Fi, so the pressure lands on **GDMA clients**, **PSRAM bandwidth**, and the **`3V3_L2`
600 mA rail and the battery** — a Wi-Fi TX burst on top of an SD write burst on top of a 120 mA
panel peak, with no published figure for any of the three. **Nobody has demonstrated this
combination.**

## 6. The asymmetry inside M5Stack's own catalogue

This is the most damning single fact on the page, and it is a measurement of the *documentation*,
not of the device.

| Product | Vendor-published power consumption | Vendor-published operating temperature |
|---|---|---|
| **M5PaperS3** (`C139`) | **Low-power mode: DC 4.2 V / 9.28 µA** (main power off, gyroscope in low-power mode)<br>**Standby: DC 4.2 V / 949.58 µA** (main power off, gyroscope on)<br>**Operating: DC 4.2 V / 154.02 mA** (main power on) | **0 ~ 40 °C** |
| **M5Paper Color** (`C151`) | **Standby: 92.53 µA**<br>**Full load: 211.97 mA** | not stated |
| **PaperMono** (`C153`) | **— nothing. The specification table has no power-consumption row at all** | **— nothing** |
| **PaperMono-Lite** (`C153-LITE`) | **— nothing** | **— nothing** |

Retrieved from `docs.m5stack.com` product pages, 2026-09-01. The PaperMono absence is a **verified
negative**: a full-text search of the retrieved 153 939-byte page finds zero occurrences of
"Power Consumption" and zero of "temperature" outside the sun-exposure precaution.

**M5Stack publishes two-decimal-place current figures for the two immediately adjacent products
in the same product line, and none whatsoever for the one whose headline feature is a five-state
power-management system.** No explanation for this is available and none should be invented — a
new product's characterisation may simply not be finished. But the consequence is concrete: the
PaperS3's numbers are the only power data that exists anywhere in this family, and they are for a
**different board with a different power architecture, a different RTC, no I/O expander and no
M5PM1**.

> **Do not use the PaperS3 figures as a proxy for the PaperMono.** They come from a board that
> has none of the PaperMono's five-state hardware, and the PaperMono adds an always-on LDO, an
> always-powered RTC, an M5PM1 and an M5IOE1 that the PaperS3 does not have. The direction of the
> difference is not even obvious: more always-on silicon could plausibly make the PaperMono's
> deepest state *worse*, while its ability to remove power from whole domains could make it much
> better. **Nothing in evidence says which.**

The PaperColor rows are worth a second glance for a different reason: at 92.53 µA standby it is
**an order of magnitude worse than the PaperS3's 9.28 µA low-power figure** — which shows that
these numbers vary by 10× across boards from the same vendor in the same line, and therefore that
extrapolating one to another is not a small approximation.

## 7. What would actually settle these questions

For whoever gets hardware. Ordered by value per unit of effort.

| # | Measurement | Method | Why first |
|---|---|---|---|
| 1 | **Current in each of L0, L1, L2, L3A, L3B** | Series shunt or a source-meter at the battery connector `J2`; hold each state through the M5PM1 API | It is the product's headline claim and it has **never been measured**. One afternoon closes the biggest gap in this record |
| 2 | **Refresh timing on the OTP path** at 20 MHz, against M5GFX at 40 MHz | Instrument `BUSY` (GPIO18) with a scope or a GPIO toggle; run the OTP demo and an M5GFX build | Tests [C3](gaps-and-conflicts.md#c3--spi-clock-exceeds-the-panels-rated-maximum) — the clock overrun — **and** produces the timings the recommended path lacks |
| 3 | **Ghosting after N partial refreshes**, with and without the vendor's 1-in-10 full refresh | Photograph a fixed pattern under fixed lighting at intervals | Tests the vendor's own precaution, and the one independent observation that exists (CNX's "ghosting visible in demo") |
| 4 | **Frontlight current at 0/64/128/255** | Shunt on `BL_15V_L3B` | Settles [C6](gaps-and-conflicts.md#c6--frontlight-current-annotation-contradicts-the-fitted-part) — 15 mA annotation against ~11 mA from the fitted `R29` — and characterises the squared gamma curve |
| 5 | **Battery runtime at a stated duty cycle** — e.g. wake on RTC every 15 min, refresh, sleep | Run to cut-off, log timestamps to microSD | The number every buyer actually wants. Meaningless without (1) |
| 6 | **Boot and wake latency** | GPIO toggle at first line of `app_main` and at refresh completion | Cheap; nobody has it |
| 7 | **Concurrent e-paper + microSD + Wi-Fi** | The scenario in [`resources-and-conflicts.md` §10](resources-and-conflicts.md#10-realistic-simultaneous-use-scenarios) | The most likely place a real application falls over |
| 8 | **LoRa range and TX current** at a stated SF/BW/power | Field test with a known counterpart | Also the only way to resolve whether the module has a TCXO |
| 9 | **NFC interoperability** across ISO14443A/B, FeliCa, ISO15693 cards | Read a set of known cards | The vendor claims four standards; **none has been demonstrated** |
| 10 | **Thermal under sustained Wi-Fi TX and refresh** | Thermocouple or IR, ambient stated | No thermal data of any kind exists, and the panel is only rated to +50 °C |

**Whoever does (1) should publish it.** It is the highest-value missing datum about this product
in the world, and it requires one board and a meter.

## 8. Reasoning that is available without measurement

Three things can be said honestly from architecture alone, provided they are labelled as such.

**The display costs nothing to hold.** An e-paper panel is bistable — it retains its image with
no power. So the useful mental model is that a refresh is a **current event** (120 mA peak per
the panel manual, under DKE's waveform) rather than a continuous load, and a static page costs
whatever the *rest* of the board costs. This is the reason the power architecture, not the
display, is the interesting engineering. **`inferred` from the panel's bistability; no board-level
figure exists.**

**The always-on set is small and is enumerable from the schematic.** In state L0 the powered
items are the charger, the protection circuitry, the `3V3_L0` LDO, the M5PM1, and — because the
vendor's own block diagram is wrong about this — the **RX8130CE RTC**, whose `VBAT`, `VIO`, `VDD`
and `VOUT` are all tied to `3V3_L0`
([R7](gaps-and-conflicts.md#r7--rtc-rail-the-vendor-block-diagram-is-wrong--resolved)). That is a
short list, and it is the list a measurement of (1) would be attributing current to. **What each
contributes is unknown.**

**Every optional rail defaults off.** Each switched LDO carries a 1 MΩ pulldown on its enable
(`R24`, `R26`, `R23`), so a cold power-up brings nothing up beyond L0. That is the correct
failure mode for a battery product, and it means the *floor* of the board's consumption is
architecturally low. It says nothing about the actual value.

**What cannot be reasoned to:** any number. Do not multiply a datasheet's typical current by a
duty cycle and present the result as a battery life. That is the exact failure the method's
"distinguish official claims, silicon limits, estimates and measurements" rule exists to prevent,
and it is why no estimate appears anywhere on this page.

## Related

- [`power-architecture.md`](power-architecture.md) — the five states, every rail and its enable, and what is *not* established
- [`features/epaper-display.md`](features/epaper-display.md) — the refresh modes and the OTP path
- [`features/power-and-sleep.md`](features/power-and-sleep.md) — how to reach each state from code
- [`resources-and-conflicts.md` §10](resources-and-conflicts.md#10-realistic-simultaneous-use-scenarios) — concurrent-use analysis, all untested
- [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) — why the battery-first verdict cannot be settled
- [`components/dke/depg0397bbs770f3`](../../../components/dke/depg0397bbs770f3/README.md) — the panel's full optical and electrical tables, with DKE's note 3
- [`components/espressif/esp32-s3r8`](../../../components/espressif/esp32-s3r8/README.md) — silicon capabilities and their limits
- [`gaps-and-conflicts.md` G7](gaps-and-conflicts.md#g7--no-power-or-battery-life-figure-exists) — the canonical gap entry
- [`sources.md`](sources.md) — S01, S04, S14, S20, S21, S47
