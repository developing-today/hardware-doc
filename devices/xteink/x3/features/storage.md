# X3 — microSD storage

> SPI, shared with the display — **but with a power rail the X4 lacks.**
> 2026-09-04.

| Signal | GPIO |
|---|---:|
| SCLK | **8** (shared with EPD) |
| MOSI | **10** (shared with EPD) |
| MISO | **7** |
| CS | **12** |
| **powerEnable** | **13**, **active-HIGH** |

`separateSpi = false`, `spiHz = 0` → SD manager default. Driver: SdFat.

## The power rail is the X3's advantage

```
setup():     digitalWrite(13, HIGH)
deep sleep:  digitalWrite(13, LOW)
```

Confirmed by factory-firmware reverse engineering. The [X4](../../x4/features/storage.md)
has **no SD enable at all**, so its card stays powered through sleep. On the X3 you
can cut it — and if your firmware does not declare the rail, you lose that.

**Polarity:** active-HIGH here; **active-LOW** on both S3 devices. Do not port.

## Bus contention

Panel and card share SCLK 8 / MOSI 10, separated only by chip select. A large card
transfer stalls display refresh. This is structural on both C3 devices and is the
main architectural reason the S3 models moved to a dedicated SDMMC slot.

## Not established

Maximum card capacity, filesystem constraints, and whether the stock firmware
formats or requires a particular partition scheme. There is a Calibre plugin for
**stock**-firmware X3 cards ([`ElendilDrac01/xteink-x3-calibre-stock`](https://github.com/ElendilDrac01/xteink-x3-calibre-stock))
and one for CrossPoint-formatted cards
([`yemM/crosspoint-reader-sd-calibre-plugins`](https://github.com/yemM/crosspoint-reader-sd-calibre-plugins)),
which implies the two layouts differ — **not confirmed**.

## Status

`reported-working`.
