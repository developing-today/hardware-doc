# DinMeter v1.1 — resources and conflicts

**The GPIO budget, peripheral budget, real conflicts, feature-combination analysis, power budget
and flash layout are identical to the v1.0's** — same carrier, same pin map, same peripherals.

→ **[`../dinmeter/resources-and-conflicts.md`](../dinmeter/resources-and-conflicts.md)**

---

## v1.1 deltas

### 1. One more internal pin has a job: GPIO38

| Pin | v1.0 | v1.1 |
|---|---|---|
| **GPIO38** (internal to the Stamp module) | Gates the module's rear LCD-FPC backlight rail only. **Unused** on the DinMeter carrier | Gates `BL_3V3`, which also supplies the module's **WS2812B-2020 RGB LED**. Must be high for the LED to light |

**No conflict.** GPIO38 is not one of the Stamp's 23 broken-out IOs, appears nowhere on the
DinMeter carrier schematic, and nothing else can want it. On this board it has exactly one job:
turning the status LED on.

Cost: one `pinMode` + one `digitalWrite` at boot. No timer, no channel, no bus.

### 2. Less 3.3 V headroom inside the module

| | Stamp-S3 | Stamp-S3A |
|---|---|---|
| Module regulator | `M2` MUN3CAD01-SC | `U4` unidentified 8-ball buck |
| Rated output | **1 A** | **0.6 A** |
| Inductor | integrated | external `L4` 2.2 µH |
| Output set by | `R6`/`R17` feedback divider | `VSEL1/2/3` pin straps |

**A 40 % reduction in the module's 3.3 V budget, disclosed nowhere by M5Stack** — not in either
specification table, not in the two-row comparison.

**Unlikely to matter on a DinMeter:** the carrier generates its own `+3.3V` from `U4`
BL8075CB5TR33 for the RTC, pull-ups and LCD FPC, and only draws the module's `3V3` pin lightly.
**It does matter** for anyone taking 3.3 V out of a bare Stamp-S3A to power external loads.

`inferred` from the `IOUT: 0~0.6A` annotation on the v0.3.3 sheet. See
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) V4.

### 3. Rear LCD FPC numbering — possibly reversed, irrelevant here

`J1`/`J3` on the module are numbered in opposite directions between v0.2 and v0.3.3 for the same
net order. **Unresolved** whether physical.

**Does not affect the DinMeter**, which uses its own `FPC1` on the carrier and never touches the
Stamp's rear header. Relevant only to bare-module users. See
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) V6.

### 4. Nothing else changed

| Resource | v1.1 |
|---|---|
| 23 broken-out GPIOs | **identical list** |
| Free user pins | **6** — GPIO1, 2, 13, 15 (Grove) + 43, 44 (UART0, unverified) |
| ⚠ Advertised-free-but-not | **GPIO14, GPIO39** — latch networks fitted on both revisions |
| SPI hosts / I²C / LEDC / PCNT / RMT / ADC | unchanged |
| LEDC timer conflict (backlight vs buzzer) | **unchanged — still the one conflict that will surprise you** |
| JTAG pins consumed by encoder + button | unchanged |
| Flash / partitions | unchanged; still nothing published by M5Stack |
| Power rails and limits | unchanged at board level |

→ [`../dinmeter/resources-and-conflicts.md`](../dinmeter/resources-and-conflicts.md) for the
complete tables.
