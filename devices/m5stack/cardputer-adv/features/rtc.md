# Cardputer ADV — real-time clock

> **Question:** *"How do I keep wall-clock time across a power cycle?"*
> **Short answer: you cannot, in hardware. There is no RTC on any Cardputer.**
> Verified **2026-09-04**.

## The negative result, and how it was established

This is a *verified negative*, not a failed search:

1. **Designator census of every sheet** of `Sch_M5CardputerAdv_v1.0` (4 sheets, 155 distinct
   reference designators). The nine `U` designators are U1 TP4057, U2 SY7088, U3 CN809J,
   U4 SY8089, U5 NS4150B, U6 ES8311, U7 BMI270, U8 MSM381A3729H9BP, U9 TCA8418RTWR. **No RTC.**
2. **No crystal in the 32.768 kHz class** anywhere on the mainboard; the only crystal in the
   system is X1, 40 MHz, on the Stamp-S3A.
3. **No coin cell, no supercap, no `VBAT`/`VRTC` net.** J8 is the main battery connector.
4. **The ADV product page's specification table has no RTC row**, while
   `docs.m5stack.com/en/CardputerZero` **does** (`RX8130CE`) — so M5Stack lists an RTC when one
   is present.
5. **M5Unified has no RTC entry** for `board_M5CardputerADV`.

Positive control: the same census method on the **CardputerZero** page finds `RX8130CE @ 0x32`
listed in both the spec table and the HMI pin map. The method detects RTCs when they exist.

## What the ESP32-S3 gives you instead

| Mechanism | Survives | Accuracy | Notes |
|---|---|---|---|
| `esp_timer` / `gettimeofday` from RTC slow memory | **deep sleep only** | internal 150 kHz RC, ±5 % uncalibrated | dies on power-off and on the ADV's hard power switch |
| RTC slow memory + `RTC_DATA_ATTR` | deep sleep only | — | a few KB |
| SNTP over Wi-Fi | nothing, but re-acquires | network-grade | the normal answer; needs credentials and a network |
| GNSS time from a **Cap LoRa-1262** | nothing, but re-acquires | very good | ATGM336H over UART G13/G15; cold start 23 s, hot 1 s per the Mesh Kit spec |
| External RTC on Grove or CAP I²C | **yes** | part-dependent | see below |

## Adding an RTC

Both expansion routes work. Watch the address collisions.

| Route | Pins | Free addresses |
|---|---|---|
| **Grove / PORT.A** (external bus) | SCL G1, SDA G2 | entire space — nothing else is on it |
| **CAP header** (internal bus) | SCL G9, SDA G8, positions R4/R5 | avoid `0x18`, `0x34`, `0x69` |

Common parts and their fixed addresses: `BM8563`/`PCF8563` at `0x51`
([`generic/bm8563`](../../../../components/generic/bm8563/README.md)), `DS3231` at `0x68` —
**note `0x68` is one below the BMI270's `0x69`**, so a DS3231 on the *internal* bus is fine but
a DS3231 with its address strap altered is not. `RX8130CE` (what the Zero uses) is at `0x32`.

Prefer the **Grove** port: it is otherwise unused, it is 5 V-tolerant at the connector, and it
keeps your RTC off the bus the keyboard scanner needs for latency.

## Why this matters more than it sounds

Several of the platform's most popular applications assume a clock:

* **Meshtastic** timestamps messages. Without an RTC or GNSS, timestamps come from the mesh or
  from a phone, and a solo node boots with no idea of the time.
* Logging applications (`geo-tp/M5Cardputer-GPS-Logger`, CSI/radar projects) need monotonic
  *and* absolute time.
* Anything doing TOTP, certificate validation, or scheduled tasks needs wall-clock time.

The **Cardputer Mesh Kit's** GNSS is, in practice, the ADV's clock source — one more reason the
kit is more than the sum of its parts.

## Evidence status

Absence of an RTC: **verified negative** by full designator census plus a positive control.
Alternatives: **official** for ESP32-S3 mechanisms, **inferred** for the Grove/CAP recommendations.
Nothing here was hardware-tested.
