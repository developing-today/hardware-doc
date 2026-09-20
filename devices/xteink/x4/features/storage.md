# X4 — microSD storage

> SPI, **sharing the display bus**. No power enable. 2026-09-04.

| Signal | GPIO | Note |
|---|---:|---|
| SCLK | **8** | **shared with the EPD** |
| MOSI | **10** | **shared with the EPD** |
| MISO | **7** | SD-only |
| CS | **12** | |
| powerEnable | **none** | **The card cannot be powered down** |

`separateSpi = false`; `spiHz = 0` → SD manager default (40 MHz). Driver: SdFat.

## Consequences of sharing the bus

1. **Panel and card contend.** Only chip select separates them; a long card
   transfer stalls display refresh and vice versa.
2. **Clock rates differ.** The panel wants ≤20 MHz (or 40 MHz overclocked); the SD
   manager defaults to 40 MHz. The bus is reconfigured per transaction.
3. **No sleep power-down.** Unlike the [X3](../../x3/features/storage.md), which
   gates its card on GPIO13, the X4 has no SD enable. The card stays powered.

That last point is a real battery consideration and the X3's profile calls it out
explicitly for its own board: *"Without declaring it, `powerDownRailsForSleep()`
has no X3 SD enable to cut, so the card stays powered through sleep → battery
drain."* **On the X4 there is nothing to declare** — the drain is structural.

## Contrast with the S3 devices

The [X4 Pro](../../x4-pro/features/storage.md) and X4 Classic use **native SDMMC**
on dedicated pins with an active-low power enable. That is faster, independent of
the display, and sleeps properly. It is the single biggest architectural
improvement between the C3 and S3 generations.

## Status

`reported-working`. Max card capacity and filesystem limits: **not tested, not
reported anywhere found**.
