# Performance — Xteink X4 Classic

> **Nothing in this document was measured by this repository.** No Xteink X4
> Classic has been in anyone's hands here. Snapshot **2026-09-11**.

This file exists so that the absence is explicit and so that the few numbers that
*do* exist are separated by evidence class rather than blended into a ranking.

## 1. What is actually known

| Quantity | Value | Class | Source |
|---|---|---|---|
| CPU | ESP32-S3 dual Xtensa LX7, 240 MHz | **silicon spec** | [`espressif/esp32-s3r8`](../../../components/espressif/esp32-s3r8/README.md) |
| PSRAM | 8 MB octal | silicon spec | same |
| Display SPI clock, FreeInk | **10 MHz** since commit `39606d5a` (2026-09-09); was 20 MHz | **source** | [`BoardConfig.h`](https://github.com/Free-Ink/freeink-sdk/blob/9f4d3f9ca675e64cc9d616081f39a33cdefce57e/libs/hardware/BoardConfig/include/BoardConfig.h) |
| Display SPI clock, OEM | **5 MHz** on the X4 Pro's OEM driver (`SPISettings 0x4C4B40`); **10 MHz** observed on a physical X4 Pro's stock app (`SPI2 CLOCK 0x70c7`) | **third-party measurement, X4 Pro, not X4C** | [`kycube/x4pro-emu` `docs/hardware.md`](https://github.com/kycube/x4pro-emu/blob/bf4b86ae0471012d4d07c0bb3042f3f561c9c302/docs/hardware.md) |
| Frame size | 48,000 B per plane (800×480×1 bpp) | **arithmetic** | — |
| Plane transfer time at 10 MHz | **≈38 ms** for 48,000 B; 48 ms for a 60,000 B transfer | **third-party measurement on X4 Pro** | same |
| Battery capacity | **920 mAh** | **vendor claim** | store spec block, 2026-09-11 |
| Mass | **68 g** | vendor claim | same |
| Thickness | **4.9 mm** | vendor claim | same |

The 38 ms figure is the **SPI transfer** alone. It is not a refresh time: the
UC8279/SSD1677 waveform dominates, and for the X4 Pro the FreeInk documentation
quotes ~1800 ms full / ~500 ms fast **without a device measurement**. Those
numbers are inherited, not verified, and they are for the Pro.

## 2. What is claimed but not measured

Every one of these is a subjective firsthand impression from a launch-week
reviewer, most of them using a vendor-supplied pre-release unit. **None has a
method, a sample count or a unit.**

| Claim | Who | Why it is not a measurement |
|---|---|---|
| *"Super fast"*, *"everything feels fast and responsive"* | u/Which_Heart_983, vendor-hosted review | no baseline, no timing |
| *"much more faster and intuitive than the X3"* | u/Comprehensive_Oil426 | different SoC **and** different firmware version; confounded |
| *"Stock firmware feels very snappy… prefer the reading speed on stock vs Crosspoint"* | u/ajcabrera | firmware comparison, no timings |
| *"a few extra days from 100 % to 0 %"* vs the X4 | u/ajcabrera | uncontrolled duty cycle; the X4's capacity is unpublished, so even the ratio is unknown |
| *"Super long battery life"* | u/Which_Heart_983 | — |
| *"higher contrast display"* / *"letters are darker"* | u/Which_Heart_983, u/Comprehensive_Oil426 | **plausible and unresolved.** Could be a panel-controller batch difference, a waveform change, or observer bias. No photometry |

**One community claim was actively corrected inside its own thread.** Asked
whether the pixel density improved, u/scamper_ replied *"It does not, it's still
219"*, and the most careful reviewer (u/ajcabrera) independently wrote *"Both use
the same 219 PPI screen I believe"*. **The X4C panel density is unchanged from
the X4.** Treat any "better screen" report as a contrast claim, not a resolution
claim.

## 3. What is not known at all

- **No deep-sleep current** for this board, or for any ESP32-C3/ESP32-S3 device in
  this repository. This gap was already recorded in the family's
  [SoC-choice guide](../../../guides/hardware/soc-choice-for-battery-eink-devices.md)
  and is unchanged.
- **No refresh-time measurement** on an X4 Classic in any mode.
- **No Wi-Fi throughput or range figure.** The FCC grant gives a **conducted**
  peak of 8.13 dBm class behaviour for the sibling X4L and a 2.30 dBi antenna for
  the X4C, which bounds EIRP but says nothing about usable throughput.
- **No boot time, no page-turn latency, no SD read rate.**
- **No thermal data.** Not expected to matter; not verified.

## 4. What it would take

| Measurement | Method | Cost |
|---|---|---|
| Page-turn latency | High-speed video or a photodiode on the panel, 20 repetitions, report median and p95 | one device |
| Deep-sleep current | Inline µA meter on the cell, device in shipped state, 10-minute average | one device, opened |
| Refresh time per mode | `micros()` around `EpdBus` `DRF` → `BUSY` release, per controller variant | one device, reflashed |
| Contrast vs X4 | Same text, same font, same room, calibrated camera or reflectance meter, both devices | two devices |
| Battery endurance | Fixed page-turn interval, fixed Wi-Fi state, to cut-off, 3 runs | two devices, weeks |

Until then this file should be read as: **the X4 Classic's performance is
unmeasured, and the things people say about it are impressions.**
