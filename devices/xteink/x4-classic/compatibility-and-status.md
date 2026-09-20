# Xteink X4 Classic — compatibility and status

Snapshot **2026-09-04**.

## Status in one line

**A fully-specified board with no users.** The FreeInk SDK ships a complete,
confidence-annotated profile; nobody outside the SDK's authors has been observed
to own, flash, build for, or write about this device.

## Software support

| Project | X4C support | Evidence |
|---|---|---|
| **FreeInk SDK** | ✅ `BoardConfig::XTEINK_X4_CLASSIC`, `[env:x4c]`, all three panel drivers | source |
| CrossPoint Reader / CrossInk / forks | **inherits** whatever the SDK provides; **no X4C-specific work found** | ~200-repo census |
| Anything X4C-specific | **none exists** | same |

## Working — by reverse engineering, not by report

Display (all three controllers), seven interrupt-driven buttons, native SDMMC with
the GPIO6 power cycle, BM8563 RTC, CW2017 gauge, QMI8658 IMU, GPIO1 rail, USB.
All at **HIGH** confidence in the SDK's own annotation, none demonstrated publicly.

## Partial / pending

| Item | State |
|---|---|
| **GPIO4** | Configured as an input by stock, never read. **Role unknown** |
| **Charge-STAT polarity** | Carried from the X4 Pro, marked `PENDING` |
| **Panel orientation** | `NO_FLIP`, pending hardware |
| **Bezel insets** | Inherited from the X4 Pro, *"pending measurement"* |
| **USB lock** | Family-wide behaviour assumed; **no X4C report exists** |

## The one risk that is worse here than anywhere else

**Panel-controller selection cannot self-correct.** Every other Xteink probes the
display bus at boot and overrides a wrong NVS value. The X4C has no MISO, so
`hw_calib/screenType` is authoritative and unchecked. A full-flash restore from
another unit can leave the device permanently driving the wrong controller.

This turns a routine, safe operation elsewhere in the family into a
device-specific hazard. See [`factory-firmware.md`](factory-firmware.md).

## Hardware-revision keyed

Two axes, **neither externally visible and neither observed**:

1. **Panel controller** — SSD1677 / UC8179 / UC8279, recorded in NVS.
2. **Board revision** — the string `ESP32S3_X4R2_CLA` implies at least an `R2`.
   **No R1 has been seen**, and it is unknown whether one shipped.

## Conflicting reports

One, and it is about identification rather than behaviour: the community that
first spotted this device in a vendor video reported it as having a **frontlight**
([r/XTEINK `1ud0d9c`](https://old.reddit.com/r/XTEINK/comments/1ud0d9c/), 300 pts).
The firmware is unambiguous that it does not. **Firmware wins.** See
[`gaps-and-conflicts.md`](gaps-and-conflicts.md), which also records a later
hearsay claim that a *different* buttons-plus-frontlight model may exist.

## Lifecycle

**Unknown.** A vendor Shopify collection `x4-classic` exists and is **empty of
devices**. No launch announcement, no price, no listing, no discontinuation
notice. Either a China-only product, a provisioned-but-unlaunched international
SKU, or both.

---

## Round 2 — status as at 2026-09-11

**No line above was altered.**

| Item | Status | Revision / version | Evidence class |
|---|---|---|---|
| **Product exists and is buyable** | ✅ **working** | listed 2026-09-06, US$79 | vendor API |
| FreeInk SDK `[env:x4c]` | ✅ profile present | commit `9f4d3f9`, 2026-09-10 | source |
| FreeInk `displaySpiHz` | ⚠ **changed** 20 → **10 MHz** | commit `39606d5a`, 2026-09-09 | source |
| CrossPoint Reader on X4C | 🟡 **reported-working** | undated build, 2026-09-10 | community, firsthand (u/Diirge: *"CrossPoint sleep screen rendering got much better as of today on the x4c"*) |
| CrossInk on X4C | ❓ discussed, unverified | — | community ([r/XTEINK `1wctkd6`](https://old.reddit.com/r/XTEINK/comments/1wctkd6/)) |
| Draftling `xteink_x4_classic` | 🟡 **builds, never run on X4C** | commit `92ba7e5` | author's own statement |
| Stock firmware | ✅ ships and works | version **unknown** on X4C; v7.0.11 was the dump FreeInk analysed | inference |
| BM8563 RTC present | ✅ **corroborated** | — | owner: *"Has a clock"* |
| QMI8658 IMU present | ✅ **corroborated twice** | — | vendor ("Shake-to-Flip"); owner: *"Shake to turn page"* |
| BLE radio present | ✅ **corroborated** | — | **FCC RF-exposure exhibit**, BLE conducted peak −0.87 dBm |
| Wi-Fi 2.4 GHz b/g/n | ✅ | 2412–2462 MHz | **FCC grant** |
| Wi-Fi 5 GHz | ❌ **absent** | — | FCC grant covers 2.4 GHz only |
| Frontlight | ❌ **absent — settled** | — | vendor spec block `Front light: No`; firmware; two reviews |
| Touchscreen | ❌ absent | — | vendor spec block; firmware |
| USB-C | ❌ **absent** | — | vendor spec block `Ports: Pogo Pin` |
| USB-MSC | ❓ SDK-supported, **no socket on the enclosure** | — | inference from the spec block + FCC label photograph |
| Panel controller in retail units | ❓ **unknown** | `hw_calib/screenType` is factory-set per unit | — |
| Anything measured | ❌ **nothing** | — | see [`performance.md`](performance.md) |

### Regression risk introduced since the last snapshot

A firmware built from FreeInk **before** `39606d5a` clocks the panel at 20 MHz;
upstream now recommends 10 MHz for every Xteink board, and the commit message
names a display-buffer-tracking bug. Anyone carrying a pinned pre-`39606d5a`
build should read that commit before blaming the hardware for artefacts.
