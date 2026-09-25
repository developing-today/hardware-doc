# Xteink X4 Pro — compatibility and status

Keyed by firmware/SDK version where known. Snapshot **2026-09-04**.

## Working — hardware-confirmed by the FreeInk maintainers

At SDK commit `2400379` (2026-09-01), *"All peripherals are up"*:

| Subsystem | Detail |
|---|---|
| Display | Paints with the plain X4 OTP waveform; no custom LUT, no PMIC |
| Buttons | GPIO 0 / 7 / 3, digital active-low |
| Frontlight | GPIO8 cool + GPIO9 warm, 25 kHz / 10-bit |
| RTC | BM8563 @0x51 found and initialising |
| SDMMC | 1-bit, mounts reliably with the GPIO5 power-cycle retry |
| GT911 touch | Including the capacitive Home key |
| CW2017 | Battery percentage, after BATINFO upload |

## Partial

| Item | State |
|---|---|
| **Panel orientation** | Ships `NO_FLIP`; mount transform pending hardware |
| **Touch axis flip** | SDK header and SDK docs disagree — see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) |
| **Deep-sleep power** | Rails driven off by polarity, but *"worth a power-draw check"* — never measured |
| **BLE page-turners** | Work, but a fork exists specifically for *"validated reconnect support"*, implying default reconnect is unreliable |

## Not working / not implemented

| Item | State |
|---|---|
| **USB-MSC** ("USB Transfer") | Present in stock, **not ported** to the FreeInk SDK |
| **`usbDetect` / VBUS sense** | Not identified. Stock uses the GPIO21 charge state instead |
| **`batteryAdc`** | Not isolated |
| **Grayscale** | 1 bpp only on this board |

## Version-specific reports

| Version | Report |
|---|---|
| CrossPoint **1.5** (2026-08-07) | Supports the new X3 display variants. Warns *"Other forks will need to pull the latest SDK to avoid soft bricking locked units"* |
| CrossPoint **1.4.0** (2026-06-24) | X3 users hit OTA problems; project moved off GitHub releases due to X3 out-of-memory. Not X4 Pro-specific but the same OTA path |
| Stock **7.4.4** (2026-08-27, IDF 6.0.1) | Uses the X4-compatible `0xFC` fast sequence |
| Stock, **earlier image** | Used `0xC7` for fast — **a firmware that hard-codes one will misbehave on the other** |

## Hardware-revision keyed

**There is no published PCB revision scheme for the X4 Pro.** The only known
hardware variation is the **panel controller** (SSD1677 / UC8179 / UC8279), which
is invisible externally and is resolved at boot.

Consequence: **compatibility claims cannot be keyed to a revision.** A firmware
either carries all three drivers and the boot probe, or it is a lottery.

## Conflicting reports

None found between independent parties — because there is only **one** party
producing board-level facts for this device (the FreeInk SDK). The conflicts that
exist are **internal to that source**.

That is itself a status finding: **this device's hardware documentation has no
independent corroboration.** No teardown, no schematic, no regulatory filing.

---

## ⚠ Correction, 2026-09-11 — Xteink FCC grants exist

The line(s) below, still present above and deliberately unedited, are **refuted**:

> *line 62:* independent corroboration.** No teardown, no schematic, no regulatory filing.
>

**Xteink is an FCC grantee.** Applicant **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**, grantee code **`2BTR9`**, registered 2025-12-21, holding **five granted Original Equipment authorisations**:

| FCC ID | Granted | Device |
|---|---|---|
| `2BTR9-X4L` | 2026-08-13 | XTEINK X4 Light |
| `2BTR9-X4C` | 2026-07-20 | XTEINK X4 Classic |
| `2BTR9-X4PRO` | 2026-06-16 | XTEINK X4 Pro |
| `2BTR9-XTEINKX4` | 2026-01-05 | XTEINK X4 |
| `2BTR9-XTEINKX3` | 2025-12-26 | XTEINK X3 |

The original finding confused **"no mark visible in a product photograph"** with **"no grant exists"**. Those are different claims, and only the first was tested.

- ✅ **Survives:** no FCC ID was legible on the exteriors photographed. Not re-tested.
- ❌ **Refuted:** any reading that these devices are uncertified or unauthorised for the US.

47 CFR §2.935 permits an **e-label** in software instead of a printed mark, which is ordinary for a device with a screen. **That is a likely explanation and it was not verified.**

The absence was never re-searched in 2026-09-04 because **no FCC ID was known and the grantee code had not been found**. Enumerating the grantee — not searching the product name — is what resolved it. Method: [`guides/research/finding-certification-records.md`](../../../guides/research/finding-certification-records.md).

Full record, with controls: [`certification-and-compliance.md`](certification-and-compliance.md).

Listed in [`research/passes/index-merge/corrections-requiring-review.md`](../../../research/passes/index-merge/corrections-requiring-review.md).
