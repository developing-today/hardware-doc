# Xteink X3 — performance

> **Nothing was measured — by this session, or by anyone.** Retrieved
> **2026-09-04**. This page mostly documents an absence, and one attempt that
> failed to produce results.

## Established figures

| Quantity | Value | Status |
|---|---:|---|
| Display SPI clock | **20 MHz** — UC8253 datasheet maximum (*"Clock rate up to 20 MHz"*, serial write timing `TSCYCW`); UC8279 rated the same | in-spec, developer-chosen |
| Prior fork clock (Witch Reader) | 16 MHz | ~25 % slower on plane writes |
| Battery capacity | **650 mAh** | teardown photograph caption, **single source** |
| Device mass | **55 g** | vendor announcement |
| Pixel density | **~257 PPI** | arithmetic: √(792²+528²) = 951.7 px ÷ 3.7″; vendor claims *"over 250 PPI"* |

**No plane-write timing exists for the X3.** The ~38 ms/~19 ms figures in this
tree are for the **X4's SSD1677 at 800×480**, a different controller and a
different panel. They are **not** transferable — the X3 has 21 % more pixels
(418,176 vs 384,000) and a different command family.

## The measurement that was attempted and abandoned

The X3 teardown was performed **expressly to instrument power**:

> "…so I can attach a **Nordic Power Profiler Kit II** to it to see if I can make
> any power optimizations to crosspoint firmware."
> — [r/xteinkereader `1uksv6s`](https://old.reddit.com/r/xteinkereader/comments/1uksv6s/), 2026-07-01

**No results were ever posted.** This is the closest anyone has come to measuring
any Xteink device, and it produced nothing. Recorded so the next person knows the
attempt was made and where it stopped.

## The one comparative observation that exists

Two X3 units, side by side, both on CrossInk 1.5.0, same settings, same screen
protector ([r/XTEINK `1vkuhbi`](https://old.reddit.com/r/XTEINK/comments/1vkuhbi/),
2026-08-10) · **firsthand comparative observation, no instrumentation**:

| Unit | Contrast | Speed |
|---|---|---|
| Official-site purchase | *"slightly **whiter** background and **clearer** text"* | *"Page turns and menus seem **slower**"* |
| Amazon.ca purchase, higher serial | *"slightly **darker** background and not as clear text"* | *"Page turns and menus seem **faster**"* |

**A real, visible contrast/speed trade-off between two units of the same model.**
The obvious hypothesis is the [UC8253 → UC8279d transition](features/display.md);
**which unit had which controller was never determined.** No numbers, no method,
n = 1 pair.

If the hypothesis is right, it would be the only user-visible evidence of that
silent hardware change — which is why it is recorded despite being subjective.

## What has never been measured

Runtime · active current · sleep current (**even though the X3, unlike the X4,
*can* power down its SD card**) · boot time · page-turn latency · full-refresh
time · Wi-Fi throughput or range · SD read/write rate · IMU ODR/noise · RTC drift
(**which would also settle the [DS1307-vs-DS3231 conflict](features/rtc.md)**).

## Known performance failure

**Out-of-memory during OTA**, observed on this device specifically:

> "I'd like to stop using github releases moving forward as **it causes out of
> memory issues on the x3**."
> — [r/XTEINK `1uek163`](https://old.reddit.com/r/XTEINK/comments/1uek163/), 2026-06-24

Root cause: the ESP32-C3 has **no PSRAM**. The S3 devices
([X4 Pro](../x4-pro/README.md), [X4 Classic](../x4-classic/README.md)) have 8 MB
and do not have this problem.

## Expected but unquantified: the UC8279d penalty

For units shipped from ~July 2026, the SDK states Full/Half/Fast currently run the
**same OTP waveform**, *"likely a full GC-style flash on every page turn"*, with
**no grayscale**. If accurate, page turns on a newer X3 are materially slower and
uglier than on an older one until waveform banks are tuned.

**This is a datasheet-derived expectation, not a measurement**, and it may be what
the two-unit comparison above was actually seeing — in which case the *faster*
unit would be the **older UC8253**. Unresolved.
