# How do I keep time on the DinMeter and wake it on a schedule?

**Applies to:** K134 and K134-V11 (identical).
**Evidence status:** wiring `executed-success` (schematic + M5Unified + esp-board-manager all
agree); code `reported-working` (vendor example). **Last verified:** 2026-09-04.

---

## Hardware path

```
BM8563 (U5, SOP8)  ──I²C──►  ESP32-S3   SCL GPIO12 / SDA GPIO11   [INTERNAL bus, address 0x51]
   Y2 32.768 kHz ±20 ppm 12.5 pF, C28/C29 6.0 pF
   VDD ← +3.3V (from U4 BL8075, fed from VBAT_IN → survives the power latch opening)
   INT (open drain) ──► power-latch wake path
```

Component: [`components/generic/bm8563`](../../../../components/generic/bm8563/README.md)
(functionally an NXP [PCF8563](../../../../components/nxp/pcf8563/artifacts/pcf8563-datasheet-rev-11.pdf)).

**The RTC is not on PORT.A.** Internal bus GPIO11/12; PORT.A is GPIO13/15. A Grove I²C unit
cannot collide with it — even one that happens to answer at 0x51.

## Arduino

```cpp
#include <M5DinMeter.h>
void setup() {
    DinMeter.begin();
    if (!DinMeter.Rtc.isEnabled()) { /* RTC not found */ }

    // direct set:  { {YYYY, MM, DD}, {hh, mm, ss} }
    DinMeter.Rtc.setDateTime({{2026, 9, 4}, {12, 34, 56}});
}
void loop() {
    auto dt = DinMeter.Rtc.getDateTime();
    Serial.printf("%04d/%02d/%02d %02d:%02d:%02d\n",
        dt.date.year, dt.date.month, dt.date.date,
        dt.time.hours, dt.time.minutes, dt.time.seconds);
    delay(500);
}
```
`DinMeter.Rtc` is a reference to `M5.Rtc`, an `RTC8563_Class` (`M5DinMeter.h:23`).
`reported-working` — the full NTP-synchronising version is
`M5DinMeter/examples/Basic/rtc/rtc.ino`, which is worth reading for its handling of the
`esp_sntp.h` / `sntp.h` header split across IDF versions.

**Keep the RTC in UTC.** The vendor example says so explicitly: *"It is recommended to set UTC
for the RTC and ESP32 internal clocks."* Do timezone conversion with `configTzTime` +
`localtime()`, not by storing local time in the RTC.

### NTP sync, condensed from the vendor example

```cpp
WiFi.begin(SSID, PASS);  while (WiFi.status() != WL_CONNECTED) delay(500);
configTzTime("UTC-8", "0.pool.ntp.org", "1.pool.ntp.org", "2.pool.ntp.org");
while (sntp_get_sync_status() != SNTP_SYNC_STATUS_COMPLETED) delay(1000);
time_t t = time(nullptr) + 1;
while (t > time(nullptr)) ;          // land on a second boundary
DinMeter.Rtc.setDateTime(gmtime(&t));
```

## Alarms and waking the board

This is the interesting part. The BM8563's open-drain `INT` is wired into the **power-latch wake
path**, so an alarm can bring the device back from a fully latched-off state — not from a sleep
mode, from *off*.

```cpp
DinMeter.Power.timerSleep(60);                     // wake in 60 s
DinMeter.Power.timerSleep(rtc_time_t{7, 30, 0});   // wake at 07:30
DinMeter.Power.timerSleep(rtc_date_t{...}, rtc_time_t{...});
```
`reported-working` (`examples/Basic/wakeup/wakeup.ino`). Internally these programme the BM8563
alarm/timer and then release GPIO46.

Lower-level: `M5.Rtc.setAlarmIRQ(...)` and `M5.Rtc.clearIRQ()` in `RTC8563_Class`.

## ESP-IDF

**There is no ESP-IDF driver for the BM8563**, and Espressif's board definition says so:

> *"Not modeled: BM8563 RTC (I2C 7-bit 0x51): no bmgr device type; the `i2c_master` above is its
> bus"*

You get the bus (port 0, SDA 11, SCL 12) and write the register access yourself, or port
`I2C_BM8563` — which M5Stack vendors into its own factory-firmware project at
`M5DinMeter-UserDemo/lib/I2C_BM8563/` (retained in
[`../artifacts/source-snapshots/`](../artifacts/source-snapshots/)). The register map is the
PCF8563's.

## BM8563 essentials

| Property | Value |
|---|---|
| Address | write `0xA2` / read `0xA3` → **7-bit `0x51`** |
| Bus speed | ≤ 400 kbit/s |
| Supply | 1.5 – 5.5 V (here 3.3 V) |
| Sleep current | typ. 0.25 µA @ 3.0 V |
| `INT` | **open drain** — needs a pull-up (the schematic shows a 10 kΩ at the `R20` position) |
| `CLKOUT` | programmable 32.768 kHz / 1024 / 32 / 1 Hz — **not wired on this board** |
| Century flag | present; the driver handles it |

⚠ The datasheet M5Stack mirrors carries a stray `MAX1937` string in its header — a sign it was
derived by editing another part's document. The address and register information is corroborated
by the PCF8563 datasheet and by M5Unified's implementation, so it is trustworthy; other
electrical tables in it are worth double-checking.

## Resource cost and conflicts

GPIO 11, 12; one I²C port; no timers, no interrupts by default (the `INT` line goes to the power
circuit, not to a GPIO you can poll). **No conflicts.** The RTC coexists with the display, the
encoder, Wi-Fi and both Grove ports.

## Pitfalls

| Symptom | Cause |
|---|---|
| `isEnabled()` false | Wrong bus — you used `Ex_I2C` (GPIO13/15) instead of `In_I2C` (GPIO11/12) |
| Time resets on power loss | The `+3.3V` rail comes from `VBAT_IN`; with **no battery fitted** and no USB/DC, the RTC has no supply |
| Alarm never fires | Alarm flag not cleared from the previous event; call `clearIRQ()` |
| Time drifts | Crystal is ±20 ppm ≈ ±1.7 s/day worst case. Re-sync from NTP |
| Local time stored in RTC then wrong after DST | Store UTC |

## Unresolved

- Whether the board loads the BM8563's `CLKOUT` — it appears unconnected but was not fully
  traced.
- The exact `R20` pull-up on `INT` has designator text but no recoverable schematic marker; see
  [`../pinouts-and-buses.md` §6](../pinouts-and-buses.md#6-reference-designator-census-and-three-that-do-not-resolve).
