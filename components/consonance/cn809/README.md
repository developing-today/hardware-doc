# CN809 — voltage supervisor / reset generator

> Schematic value on the M5Stack Cardputer boards: **`CN809J`** (designator U3).
> Record created **2026-09-04**. The `CN809` family is a MicroPower voltage-detector /
> reset-generator commonly attributed to **Consonance Electronic** (上海如韵 / Consonance
> Electronic Inc.); the exact manufacturer of the fitted part is **not established** — see *Gaps*.

## Function

A three-terminal supply supervisor. It watches `VCC` and holds its `RESET` output asserted while
the supply is below a threshold, releasing it after a fixed delay once the supply is good. The
suffix letter selects the threshold voltage — that is what the `J` in `CN809J` encodes.

Its purpose on a battery device is to guarantee a clean reset on brown-out and on a battery that
sags under load, rather than letting the MCU run at an undefined voltage.

## Key capabilities

| Property | Value | Evidence |
|---|---|---|
| Package | 3-pin SOT-23-class | schematic symbol: `VCC` (3), `GND` (1), `RESET` (2) |
| Threshold | selected by the suffix; **`J` variant** | value string; **threshold voltage not established** |
| Reset output | push-pull or open-drain depending on the family member | **not established** |
| Reset timeout | fixed, typically ~140–240 ms in this family | **not established** |

## Pinout as drawn

| Pin | Name | Net on the Cardputer |
|---|---|---|
| 1 | `GND` | GND |
| 2 | `RESET` | via **R7 100 kΩ** to GND; also to the Q1 gate network |
| 3 | `VCC` | **`+5VIN`** |

Read from a rendered crop of Cardputer ADV schematic sheet 1.

## Used By

### M5Stack Cardputer ADV (K132-Adv) — [`devices/m5stack/cardputer-adv`](../../../devices/m5stack/cardputer-adv/README.md)

Designator **U3**, in the power-input block on sheet 1, immediately beside the **TP4057**
charger and the `VBAT_IN`/`VBAT_OUT` power-path FETs (Q1–Q3, `LP3218DT1G`).

It supervises the **`+5VIN`** rail — the USB input — and its `RESET` output participates in the
power-path gating rather than driving the SoC's `EN` pin directly. (The SoC's `CHIP_PU` is driven
from `ESP_EN` on the Stamp module, through its own RC and 10 kΩ pull-up.)

**Practical consequence for firmware:** none directly. The part is invisible to software. It
matters for two things a developer will meet:

* The device's behaviour when USB is connected or removed while running, and
* the interaction with M5Stack's repeated instruction that **the power switch must be ON to
  charge** — the charge path, the supervisor and the switch are all in the same block.

### M5Stack Cardputer v1.0 (K132) and v1.1 (K132-V11)

[`devices/m5stack/cardputer-v1.0`](../../../devices/m5stack/cardputer-v1.0/README.md) ·
[`devices/m5stack/cardputer-v1.1`](../../../devices/m5stack/cardputer-v1.1/README.md)

**Same part, same designator `U3`.** The value string `CN809J` appears on the v1.0/v1.1 shared
schematic (SHA-256 `6016c1fe…`) exactly as it does on the ADV — one of several parts confirming
that the ADV's power train is carried over unchanged from the earlier boards. The others are
`TP4057` (U1), `SY7088` (U2), `SY8089` (U4) and `LP3218DT1G` (Q1–Q3).

## Substitutes

| Part | Note |
|---|---|
| MAX809 / MAX810 | the parts the CN809 family is pin- and function-compatible with by design |
| APX809, SGM809, HT7XXX | common second sources; **check the threshold suffix**, which is not standardised across vendors |
| MCU internal brown-out detector | free, but does not gate the power path |

## Gaps

* **No datasheet retrieved.** The threshold voltage the `J` suffix selects, the reset timeout,
  the output structure (push-pull vs open-drain) and the supply range are all **unknown**.
* **Manufacturer not confirmed.** `CN809` is used by more than one vendor; the directory is named
  for the most commonly attributed one and this uncertainty is recorded rather than hidden.
* No board photograph, so the top marking has not been checked against the schematic value.
