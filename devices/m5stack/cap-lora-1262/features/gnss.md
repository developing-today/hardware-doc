# GNSS — Cap LoRa-1262 (U214)

> **How do I get a position fix?** Open `Serial1` at **115200 8N1** with **RX = G15,
> TX = G13**, and parse NMEA. That is the whole interface. Everything difficult about this
> subsystem comes from the two pins being documented backwards in one place — §6.

Snapshot 2026-09-04 · schematic **V1.1** · nothing tested on hardware.

## 1. Hardware path

```
J1 ceramic patch (ANT1818-04, 18x18x4 mm)
   │ L1 6.8 nH
   ▼
U1 MAX2659 LNA  (VCC +3.3V, SHDN tied, C6 100nF / C7 33nF)
   │ C5 470 pF
   ▼  pin 11 ANT
M2 ATGM336H-6N  ── AT6668 chipset inside ── VBAT ◀── BT1 backup cell
   │ pin 2 TXD ──▶ Cap-Bus 1 ──▶ host G15   (host RX)
   │ pin 3 RXD ◀── Cap-Bus 2 ◀── host G13   (host TX)
   │ VCC  ◀── FB2/FB3 120 Ω/MB ◀── VDD_3V3
   └ SDA/SCL (16/17), 1PPS (4), NRST (9), ON/OFF (5): NOT ROUTED to the host
```

| Element | Part | Record |
|---|---|---|
| GNSS module | **ATGM336H-6N**, schematic comment `GP-02` | [`components/zhongkewei/atgm336h-6n`](../../../../components/zhongkewei/atgm336h-6n/README.md) |
| GNSS chipset | **AT6668** | [`components/zhongkewei/at6668`](../../../../components/zhongkewei/at6668/README.md) |
| LNA | **MAX2659** | [`components/analog-devices/max2659`](../../../../components/analog-devices/max2659/README.md) |
| Patch antenna | `ANT1818-04` (18 × 18 × 4 mm) | [`components/generic/gnss-ceramic-patch-antenna`](../../../../components/generic/gnss-ceramic-patch-antenna/README.md) |

**The LNA is the notable design choice.** Most ATGM336H breakouts hang a passive patch
straight off `ANT`. This board puts a **MAX2659 (≈ +20 dB gain, sub-1 dB NF)** in front of
it, powered from `VCC_RF` through a ferrite. That is what buys the −162 dBm tracking figure
in the specification table, and it means the GNSS front end draws current even when the
receiver is idle — `SHDN` is tied, so the host cannot switch the LNA off.

## 2. Capability, as published

| Item | Value |
|---|---|
| Constellations | GPS · QZSS · BDS (BD2 + BD3) · GALILEO · GLONASS |
| Bands | BDS **B1I + B1C** · GPS/QZSS/SBAS **L1** · GALILEO **E1** · GLONASS **R1** |
| Channels | 50 |
| Accuracy | **< 1.5 m CEP50** |
| Update rate | up to **10 Hz** |
| Sensitivity | tracking **−162 dBm** · acquisition −160 dBm · cold start −148 dBm |
| TTFF | cold **23 s** · hot **1 s** |
| Protocol | **NMEA 0183 4.1** on the wire; **CASIC binary** for configuration |
| UART | **115200 bps, 8N1** |

> ⚠ **115200, not 9600.** The ATGM336H's own factory default in most other products is
> 9600 bps. M5Stack ships this Cap configured at 115200 and both the vendor example and
> Meshtastic's `GPS_BAUDRATE` assume it. If you autobaud, include 9600 in the sweep anyway —
> nothing in the documentation says the setting is stored in the module's flash rather than
> applied by firmware.

Multi-band (B1I+B1C, E1, L1, R1) does **not** mean dual-frequency: these are all the same
~1.56–1.61 GHz L1 neighbourhood, which is why one 18 mm patch and one LNA suffice. Do not
read "multi-frequency" here as L1+L5 RTK-grade capability.

## 3. Software

| Stack | Class / API | Notes |
|---|---|---|
| **M5Stack Arduino** | `MultipleSatellite` from **`github.com/m5stack/TinyGPSPlus`** | ⚠ *"needs to be downloaded from the GitHub version adapted for M5Stack devices … Do not download it from the Arduino Library Manager"* **[DOC]**. Repo head `254a10041ac38d17d98dab24c0ae4d2a8d19a677`, 2025-01-02, **no LICENSE file present** (upstream TinyGPSPlus is LGPL-2.1) |
| **Meshtastic** | built-in GPS subsystem, `HAS_GPS 1` | `GPS_RX_PIN 15`, `GPS_TX_PIN 13`, `GPS_BAUDRATE 115200` |
| **UiFlow2** | `uiflow-micropython.readthedocs.io/en/latest/cap/lora1262.html` | vendor |
| Any NMEA parser | — | The device emits standard NMEA 0183 4.1; nothing M5Stack-specific is needed just to read a fix |

Vendor example skeleton (**[DOC]**, `executed-success` on the read, `not-tested`):

```cpp
#include "MultipleSatellite.h"
static const int RXPin = 15, TXPin = 13;      // host RX = G15, host TX = G13
static const uint32_t GPSBaud = 115200;
MultipleSatellite gps(Serial1, GPSBaud, SERIAL_8N1, RXPin, TXPin);

satellite_mode_t currentMode = SATELLITE_MODE_GLONASS;   // vendor default

void setup() {
    gps.begin();
    gps.setSystemBootMode(BOOT_FACTORY_START);
    String version = gps.getGNSSVersion();
    gps.setSatelliteMode(currentMode);
}
void loop() {
    gps.updateGPS();
    if (gps.location.isUpdated()) { gps.location.lat(); gps.location.lng(); }
    gps.satellites.value();  gps.date.month(); gps.time.hour();
}
```

`setSystemBootMode()`, `setSatelliteMode()` and `getGNSSVersion()` are **CASIC binary
commands**, not NMEA — that is what the *CASIC Multi-mode Satellite Navigation Receiver
Protocol Specification* documents. It is archived; see
[`components/zhongkewei/at6668/artifacts/`](../../../../components/zhongkewei/at6668/artifacts/).

## 4. What the host cannot do

Because pins 4, 5, 9, 16 and 17 of `M2` are not routed to the Cap-Bus
([`../pinouts-and-buses.md` §4](../pinouts-and-buses.md)):

| Missing | Consequence |
|---|---|
| `1PPS` | **No pulse-per-second.** Rules out disciplined-clock / precise-timing uses |
| `NRST` | No hardware reset. A wedged receiver can only be recovered over UART (or by cutting the Cap's 5 V at the host) |
| `ON/OFF` | No hardware power/standby toggle. Power saving must be a CASIC software command |
| `SDA`/`SCL` | The module's I²C port is unavailable; UART is the only channel |
| LNA `SHDN` | The MAX2659 cannot be shut down; its quiescent current is always paid |

## 5. Power

Vendor figures, conditions unstated **[DOC]**:

- U214 page: **"Power Consumption (Power On): 33.1 mA"**
- U201 (predecessor) page, state-resolved and far more useful: GPS on / LoRa standby
  **29.24 mA**; **GPS sleep / LoRa standby 3.16 mA**; GPS on / LoRa TX max **155.03 mA**.

The 3.16 mA figure is the interesting one: putting the GNSS to sleep is worth roughly
26 mA at 5 V on the predecessor board, i.e. it dominates idle draw. Those numbers are for
U201 and must not be copied into a U214 table — but the *shape* of the tradeoff carries.

## 6. ⚠ "No satellites, ever" — the RX/TX documentation trap

This is the most-reported problem with the Cap, and it is a documentation defect, not a
hardware defect.

The Cardputer Mesh Kit page labels EXT pin 12 (`G13`) `UART_RX` and pin 14 (`G15`)
`UART_TX`. Anyone wiring from that page puts the host's receiver on **G13** and gets
silence. The correct assignment — confirmed by the schematic, the Cap's own pin-map
graphic, M5Stack's Arduino example and Meshtastic's `variant.h` — is **host RX = G15,
host TX = G13**. Full evidence table in
[`../pinouts-and-buses.md` §1.1](../pinouts-and-buses.md).

Firsthand report, [r/CardPuter 2026-08-28](https://old.reddit.com/r/CardPuter/comments/1w0gv7y/)
("Adv & LoRa cap doesn't find gps", 15 comments): the owner tried several firmwares
outdoors with no satellites *seen at all*, concluded the GNSS was dead on arrival, then
edited the post — *"it seems I got this working eventually at least in meshtastic by
setting manually the gpio rx and tx pins. See 30 satellites now."* **[COM]**

Second, distinct cause in the same thread: several owners traced GNSS breakage to
**M5Launcher 2.8.0** leaving stale state, fixed by reflashing an earlier launcher;
u/bmorcelli (the launcher's author) replied *"I have it fixed on Launcher Beta 2.9"*
(2026-09-02). **[COM]** So "GPS doesn't work" has at least two unrelated common causes and
neither is the receiver.

Third, a *non*-bug that looks like one: Meshtastic **degrades position precision by
default**. u/Cricrimor, [r/CardPuter 2026-01-18](https://old.reddit.com/r/CardPuter/comments/1qf0z9v/):
*"By default, precision of location is degraded in meshtastic. You can set this in
parameters > Channels."* The reporting owner had a fix *2 miles off* under Meshtastic while
M5Stack's own demo was *"spot on"*, and resolved it by changing the channel precision
setting. **[COM]**

| Symptom | Likely cause |
|---|---|
| Zero satellites *seen*, indoors and out, any firmware | RX/TX pins swapped — §6 |
| Worked, then stopped after a launcher update | Stale launcher state — reflash |
| Fix obtained but position is ~1–3 km off | Meshtastic channel position-precision setting |
| Long TTFF every time | Backup cell `BT1` not holding, or the receiver is cold-starting because the almanac was cleared |
| Works outdoors only | Normal. A 18 mm patch behind a plastic Cap is not an indoor antenna |

## 7. Unresolved

- **`ANT1818-04`** is read from a schematic comment only; no antenna datasheet was located
  and the manufacturer is not identified.
- **`GP-02`**, the `M2` symbol comment, is unexplained. The specification table says
  `ATGM336H-6N@AT6668`; `GP-02` may be an M5Stack internal library name or a second-source
  designation. Not resolved.
- Whether 115200 bps is stored in the module or applied by firmware each boot.
- No independent measurement of TTFF, accuracy or sensitivity for this board.

## Applicability

| Field | Value |
|---|---|
| Hardware | Cap **U214**, schematic V1.1, on Cardputer-Adv |
| Software | `m5stack/TinyGPSPlus` @ `254a1004…` · Meshtastic ≥ 2.7.20 |
| Evidence | Pinout: schematic + three corroborating sources. Capability: **vendor claim only**. Failure modes: **firsthand community reports**, dated and cited |
| Confidence | High on wiring; vendor-claim-only on performance |
| Last verified | 2026-09-04 |
