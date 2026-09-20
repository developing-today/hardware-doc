# How do I get the DinMeter onto the network?

**Applies to:** K134 (Stamp-S3) and K134-V11 (Stamp-S3A).
**Evidence status:** capability from silicon and vendor documentation; code
`reported-working` (vendor example). **Radio performance was not measured.**
**Last verified:** 2026-09-04.

---

## What the radio is

| Property | Value | Evidence |
|---|---|---|
| SoC | ESP32-S3FN8 | vendor spec row |
| Wi-Fi | **2.4 GHz 802.11 b/g/n only** — no 5 GHz, no Wi-Fi 6 | vendor spec row + ESP32-S3 datasheet |
| Bluetooth | **BLE 5 only.** The ESP32-S3 has **no Bluetooth Classic (BR/EDR)** — silicon-level, unfixable in software | ESP32-S3 datasheet |
| Antenna | on the **Stamp module**, "2.4 GHz 3D antenna", `ANT1` | Stamp product pages |
| Antenna part | Stamp-S3: `PROANT440`. **Stamp-S3A: no part text on the schematic** | schematics |
| External antenna connector | **none** | no connector designator on either sheet |

**No A2DP, no HFP, no SPP, no Bluetooth media keys.** If you wanted a Bluetooth *audio* knob,
this is the wrong device — see
[`../comparisons-and-recommendations.md`](../comparisons-and-recommendations.md) §2, where the
Waveshare knob solves it by soldering a second SoC onto the board.

BLE HID *is* possible and is what `tarmn3/m5dinmeter-ble-volume-knob` does.

## Arduino

Standard ESP32 Arduino; nothing DinMeter-specific:

```cpp
#include <WiFi.h>
#include <M5DinMeter.h>

void setup() {
    auto cfg = M5.config();
    DinMeter.begin(cfg, true);            // raises GPIO46 - do this first, always
    WiFi.begin("ssid", "password");
    while (WiFi.status() != WL_CONNECTED) { delay(500); }
    DinMeter.Display.print("Connected.");
}
```
Pattern taken from `M5DinMeter/examples/Basic/rtc/rtc.ino`, which is also the NTP example — see
[`rtc-and-timekeeping.md`](rtc-and-timekeeping.md).

M5Stack documents a dedicated tutorial at `docs.m5stack.com/en/arduino/m5dinmeter/wifi`
(HTTP 200, 2026-09-04).

**BLE:** `NimBLE-Arduino` or the ESP32 Arduino `BLEDevice` stack. Nothing board-specific.

## ESP-IDF

`esp_wifi` and `esp_nimble` as normal, target `esp32s3`. Espressif's `esp-board-manager`
DinMeter definition models **no radio at all** — because there is nothing board-specific to
model.

## The memory constraint that will actually bite you

**There is no PSRAM.** ESP32-S3FN8, on both revisions, confirmed three ways: no PSRAM row on
either product page; `FN8` has none in package; Bruce/Launcher explicitly does
`build_unflags = -DBOARD_HAS_PSRAM`.

So you are sharing the ESP32-S3's internal SRAM between:

| Consumer | Rough cost |
|---|---|
| Wi-Fi stack + lwIP | tens of KB, more with many sockets |
| TLS session (mbedTLS) | **~20–50 KB per connection**, dominated by the record buffers |
| BLE (NimBLE) | ~30–40 KB |
| A full 135 × 240 × 16 bpp framebuffer | **64 800 B** |

Running Wi-Fi + TLS + BLE + a full-screen sprite simultaneously is where a PSRAM-less S3 gets
uncomfortable. The mitigations are the usual ones: band buffers instead of a full framebuffer
(see [`display.md`](display.md)), `MBEDTLS_SSL_MAX_CONTENT_LEN` reduced from 16384, and not
running Wi-Fi and BLE concurrently unless you must.

**Not measured here.** No heap profiling was done. These are the standard ESP32-S3 constraints,
stated so you plan for them; the numbers are indicative.

## Coexistence

Wi-Fi and BLE share the single 2.4 GHz radio. ESP-IDF's coexistence arbiter handles it, at the
cost of throughput and latency on both. Nothing about the DinMeter changes this.

## Antenna and enclosure — the thing that is genuinely device-specific

The DinMeter is designed to be **installed inside a metal panel or cabinet**, with only its
53 × 30 mm face exposed through a 45 × 22.5 mm aperture. The antenna is on the Stamp module,
*behind* the panel.

That is a materially worse RF environment than a desktop puck, and it is the one place where
the Stamp-S3A's rebuilt antenna match might matter. M5Stack claims *"better signal reception"*
for the S3A with **no figure and no method**. Nothing here corroborates or refutes it.

**If you are deploying into a steel cabinet, budget for testing the link margin.** There is no
external antenna option, so the mitigations are placement, keeping the door open to RF, or an
external AP nearby. `inferred` — no RF measurement was performed.

## Resource cost and conflicts

GPIO: **none** — the radio is entirely on-die and the antenna is inside the module. There is no
pin conflict with the display, encoder, RTC, buzzer or Grove ports. The constraints are RAM,
power and RF environment, not pins.

**Power:** the vendor's "standby" figures (33.5 mA on Stamp-S3, 25.5 mA on Stamp-S3A) are the
number to plan around when the radio is up. Compare with 38.4 µA latched off. If you are running
on the bundled 250 mA·h cell, Wi-Fi-always-on is roughly a **10-hour** device; duty-cycled with
RTC wake it is a months-long device. That arithmetic is `inferred` from vendor figures, not
measured.

## Related

[`power-and-battery.md`](power-and-battery.md) · [`rtc-and-timekeeping.md`](rtc-and-timekeeping.md)
(RTC wake is how you make the battery last) ·
[`components/m5stack/stamp-s3a`](../../../../components/m5stack/stamp-s3a/README.md) §4 (the antenna change)
