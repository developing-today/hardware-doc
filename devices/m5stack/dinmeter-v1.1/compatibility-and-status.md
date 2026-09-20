# DinMeter v1.1 — compatibility and status

Shared rows (library versions, third-party firmware, peripherals, known-bad combinations) are in
**[`../dinmeter/compatibility-and-status.md`](../dinmeter/compatibility-and-status.md)** and apply
unchanged. This page is the v1.1 delta.

**No v1.1 hardware was available.** Nothing below is a firsthand test.

---

## 1. Does v1.0 firmware run on v1.1?

**Yes, unmodified, with exactly one exception.**

| Subsystem | v1.1 status | Basis |
|---|---|---|
| Boot / download mode | **works** | identical vendor instruction on both Stamp pages |
| Toolchain / target (`esp32s3`, 8 MB, no PSRAM) | **works** | vendor spec, both revisions |
| M5Unified board detection | **works** — enumerates as `board_M5DinMeter` | no v1.1 or S3A enum exists at master `8530f537…` |
| Display | **works** | identical pins, resolution, GRAM gap, `INVON`, driver path |
| Rotary encoder | **works** | identical pins |
| Encoder button / WAKE | **works** | identical |
| Buzzer | **works** | identical |
| RTC (BM8563, 0x51) | **works** | identical |
| Power hold (GPIO46) | **works** | identical |
| Battery ADC | **works** | identical |
| PORT.A / PORT.B | **works** | identical |
| Wi-Fi / BLE API | **works** | same SoC, same stack |
| Wi-Fi / BLE *performance* | **unknown** | antenna match rebuilt; vendor claims better, publishes no figure |
| **RGB LED** | **fails (predicted)** | needs `GPIO38 = HIGH`; no framework does it |

## 2. The one incompatibility, in full

| Field | Value |
|---|---|
| Symptom | RGB LED does not light. No error, no warning, no compile failure |
| Affects | K134-V11 only |
| Cause | Stamp-S3A moved the WS2812B-2020's supply from the always-on `VDD_3V3` to the switched `BL_3V3`, gated by an AW35122FDR whose enable is GPIO38. The AW35122's `EN` has an internal ~7.1 MΩ pull-down, so the rail defaults off |
| Why no framework saves you | M5Unified master `8530f5377d782e4a25a6c482de2e71c3f75ca8eb` (2026-09-04): `board_M5DinMeter → GPIO_NUM_21` at `src/M5Unified.cpp:246`; **no GPIO38 enable step for any board**; no `board_M5StampS3A`; no v1.1 board enum |
| Workaround | `pinMode(38, OUTPUT); digitalWrite(38, HIGH); delay(1);` before driving GPIO21 |
| Portable? | Yes — GPIO38 is unconnected on the v1.0 carrier, so the same code is safe on both |
| **Evidence status** | **`inferred`** — vendor documentation + schematic + source read. **Not reproduced on hardware** |
| Reported upstream? | **No.** No M5Unified issue or PR addressing it was found on 2026-09-04 |

## 3. Framework support, v1.1-specific

| Framework | Status | Note |
|---|---|---|
| `M5DinMeter` 1.0.0 + M5Unified 0.2.21 | works, except the LED | no v1.1 release exists; the library is unchanged since 2024-03-07 |
| `espressif/esp-board-manager` @ `2beb9b22…` | expected to work; **untested on v1.1** | its `board_info.yaml` says `version: 1.0.0` and it was written against the v1.0 page. Every pin it models is unchanged, so nothing in it is *wrong* for v1.1 — it simply does not know about GPIO38 |
| UiFlow2 / `uiflow-micropython` | expected to work | the DinMeter target is not versioned by board revision |
| `bmorcelli/Launcher` | expected to work | `m5stack-dinmeter` target makes no revision distinction |

**No framework anywhere distinguishes v1.0 from v1.1.** That is convenient for compatibility and
is precisely why the LED change is a silent failure.

## 4. Module-level status (Stamp-S3A)

| Item | Status | Note |
|---|---|---|
| ESP32-S3FN8, 8 MB, no PSRAM | unchanged | |
| 23 broken-out GPIOs | unchanged, same list | |
| USB-C native | unchanged | same `J2`, same `R1`/`R2` 5.1 kΩ CC |
| 3.3 V rail current | **reduced: 1 A → 0.6 A** | undisclosed by the vendor; see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) V4 |
| Rear LCD FPC numbering | **possibly reversed** | unresolved; irrelevant to the DinMeter |
| Module footprint | believed unchanged | no Stamp-S3A footprint published; STLs byte-identical; but the spec table says 26 mm vs 24 mm |
| Sleep current | much improved (vendor figures) | 310.89 → 6.84 µA on `VIN_5V` |

## 5. What is untested — which is everything

| Category | Status |
|---|---|
| Any v1.1 hardware in hand | **none** |
| The RGB-LED/GPIO38 prediction | **not verified** ← highest-value test |
| Any firmware built or flashed | **none** |
| Any electrical or RF measurement | **none** |
| Antenna improvement claim | **not tested** |
| Teardown / chip-marking confirmation | **none** |
| Whether the v1.1 PCB really is the v1.0 PCB | **not verified** |

## 6. If you have a v1.1 unit — three tests, ten minutes

1. **`pinMode(38,OUTPUT); digitalWrite(38,HIGH);` then drive GPIO21.** Does the LED light? Does
   it light *without* the GPIO38 line? Two runs settle the record's biggest open question.
2. **Flash a binary built for v1.0 unmodified.** Confirms or refutes the source-compatibility
   verdict in [`stamp-s3-to-s3a-delta.md` §8](stamp-s3-to-s3a-delta.md#8-does-existing-dinmeter-firmware-run-unmodified).
3. **Measure the Grove 5 V rail** on `J3` pin 3 — 5.00 V or ≈ 5.38 V? Settles a conflict that
   applies to both revisions.

Results belong here and in [`../dinmeter/compatibility-and-status.md`](../dinmeter/compatibility-and-status.md).
