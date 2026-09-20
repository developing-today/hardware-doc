# Xteink X3 — compatibility and status

Snapshot **2026-09-04**.

## Working

Display (UC8253), ADC ladder buttons, microSD with its power rail, BQ27220 gauge,
QMI8658 IMU, RTC (whatever it is), Wi-Fi, BLE. Widely exercised — the X3 is the
second-most-targeted device in the ecosystem after the X4.

## Partial

| Item | State |
|---|---|
| **UC8279d panel batch** | Driver written **from the datasheet only**. No unit benched. Full/Half/Fast all run the same OTP waveform — likely a **full flash on every page turn**. No grayscale |
| **Controller fingerprint** | Works, but relies on an untested assumption about what the UC8253 answers to `0x70` |
| **Deep sleep** | Rail handling correct; **no current measurement exists** |
| **RTC** | Functions; **the part is not identified**, so accuracy and alarm/temperature capability are unknown |
| **NFC** | Hardware present; no software, no known purpose |

## Known failures with named causes

| Failure | Version / condition | Note |
|---|---|---|
| **OTA out-of-memory** | CrossPoint ≤1.4.0 via GitHub releases | Real, observed. Project stopped using GitHub releases *"as it causes out of memory issues on the x3"* |
| Blank screen after flashing | Newer UC8279d unit + firmware without that driver | Fixed in CrossPoint 1.5 |
| Soft brick | Locked unit + fork on a stale SDK | CrossPoint 1.5 release warning |
| **Rear glass cracking** | Physical | One owner report, unanswered follow-up about metal backing |

## Version-keyed

| Version | Status |
|---|---|
| CrossPoint **1.5** (2026-08-07) | **Supports the new X3 display variants.** Recommended minimum for a recently-purchased unit |
| CrossPoint **1.4.0** (2026-06-24) | X3 OTA problems; use web reflash or SD flash |
| CrossPoint **1.2.0** | Associated with a documented OTA brick (X4; assumed to apply) |
| Stock **V5.2.13** | Latest known stock, both CN and EN |
| Stock **V1.0.7** | Earliest published stock image |

## Hardware-revision keyed

**One known axis: the panel controller.** Units shipped from roughly **July 2026**
carry a **UC8279d** instead of a UC8253. The vendor gave the community advance
notice — the only instance found of Xteink pre-announcing a silent hardware change.

**There is no external marking.** A buyer cannot tell before powering on.
Practical rule: **buy recently → assume UC8279d → require CrossPoint ≥ 1.5 or an
equivalent.**

## Conflicting reports

The **RTC part** — three sources, three answers, all at address 0x68. See
[`gaps-and-conflicts.md`](gaps-and-conflicts.md). This is the only genuine
multi-party disagreement in the whole Xteink family, and it exists precisely
*because* the X3 is the only model with independent teardowns to disagree with.

## Lifecycle

**Current and in stock**, both colours, $69, as of 2026-09-04.
