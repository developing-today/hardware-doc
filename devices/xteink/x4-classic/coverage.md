# Xteink X4 Classic — feature coverage

Snapshot **2026-09-04**. "Evidence" here means the FreeInk SDK's Ghidra analysis
of a stock dump, unless stated. **Nothing was tested by this session, and no
third party has ever reported using this device.**

| Feature | Hardware | Official docs | Community evidence | Guide | Confidence | Gaps |
|---|---|---|---|---|---|---|
| Display 800×480 | SSD1677 / UC8179 / UC8279 | none | **none** | [`pinouts`](pinouts-and-buses.md) | **HIGH** (RE) | Panel module part; orientation |
| **Controller selection** | **NVS `hw_calib/screenType` only** | none | none | [`factory-firmware`](factory-firmware.md) | **HIGH** | **No live probe possible — no MISO** |
| Buttons ×7, interrupt-driven | GPIO 0/2/3/5/7/8/9 | none | none | [`pinouts`](pinouts-and-buses.md) | **HIGH**, map corrected on hardware | — |
| **GPIO4** | plain input, no ISR | none | none | — | **PENDING** | **Role entirely unknown** |
| microSD, native SDMMC 1-bit | 41/42/40 + EN **6** active-LOW | none | none | [`pinouts`](pinouts-and-buses.md) | **HIGH** | Max card size |
| RTC BM8563 | 0x51 | none | none | [`pinouts`](pinouts-and-buses.md) | **HIGH** | Backup power source |
| Fuel gauge CW2017 | 0x63 | none | none | [`pinouts`](pinouts-and-buses.md) | **HIGH** | **Battery capacity unknown**; needs BATINFO upload |
| **IMU QMI8658** | 0x6B, `WHO_AM_I` 0x05, no INT | none | none | [`pinouts`](pinouts-and-buses.md) | **HIGH** (`CTRL1/2/3/7` init RE-confirmed) | No wake-on-motion; no perf data |
| Charge STAT | GPIO21 | none | none | [`pinouts`](pinouts-and-buses.md) | **med** | **Polarity PENDING** |
| USB / USB-MSC | D− 19 / D+ 20 | none | none | [`development`](development.md) | **HIGH** per SDK | Never demonstrated |
| Wi-Fi + BLE | ESP32-S3 | none | none | — | stated by SDK | Never demonstrated |
| Power rail | GPIO1 HIGH at boot | none | none | [`pinouts`](pinouts-and-buses.md) | **HIGH** | — |
| **Charging connector** | — | none | none | — | **UNKNOWN** | **USB-C or pogo? Not established** |
| **Touch** | **absent** | — | — | — | **HIGH** | — |
| **Frontlight** | **absent** | — | — | — | **HIGH** — stock says *"Frontlight hardware is disabled on this board"* | — |

## Not fitted

Touch, frontlight, audio codec, buzzer, LEDs, PMIC, GPIO expander. Power
management is direct-GPIO plus the gauge and RTC.

## Combination scenarios

**None assessed** — there is no hardware, no owner and no build report. The
concerns inherited from the [X4 Pro](../x4-pro/coverage.md) apply structurally
(display refresh + SDMMC both DMA-heavy; three devices on one `Wire` controller;
Wi-Fi and BLE sharing one radio), but nothing device-specific can be said.

## Score

**11 of 15** capabilities have HIGH-confidence reverse-engineering evidence.
**0 of 15** have any community corroboration.
**0 of 15** were verified by this session.
**2** are explicitly PENDING in the source itself (GPIO4, STAT polarity).
**1** first-order buyer question is entirely unanswered (**the charging connector**).

---

## Round 2 coverage delta — 2026-09-11

**No line above was altered.**

| Capability | Hardware evidence | Vendor claim | Guide | Example | Tested on X4C? |
|---|---|---|---|---|---|
| Display 800×480 | SDK + Draftling | ✅ "4.3 inch / 219 PPI" | [`pinouts-and-buses.md`](pinouts-and-buses.md) | E01, E02, E03 | **no** |
| Buttons ×7 + GPIO4 | SDK + Draftling | — | [`resources-and-conflicts.md`](resources-and-conflicts.md) | E01, E02 | **no** |
| microSD (SDMMC 1-bit) | SDK + Draftling | ✅ "16 GB bundled, to 256 GB" | [`resources-and-conflicts.md`](resources-and-conflicts.md) | E01, E02, E03 | **no** |
| RTC BM8563 @0x51 | SDK | — | — | E01 | **owner-corroborated** ("Has a clock") |
| Gauge CW2017 @0x63 | SDK + Draftling | ✅ "920 mAh" | — | E01, E02 | **no** |
| **IMU QMI8658 @0x6B** | SDK | ✅ **"Shake-to-Flip"** | — | **none** | **owner-corroborated** ("Shake to turn page") |
| Wi-Fi 2.4 GHz | SDK | ✅ | — | — | **FCC-certified** |
| **BLE** | SDK | ✅ | — | E02 (keyboard, other board) | **FCC-measured** (−0.87 dBm) |
| Charging, pogo | SDK (`STAT` GPIO21) | ✅ "Ports: Pogo Pin" | — | — | **no** |
| Deep sleep / EXT1 on GPIO3 | SDK + Draftling | — | [`resources-and-conflicts.md`](resources-and-conflicts.md) §6 | E01, E02 | **no** |
| USB-MSC | SDK | ✗ not mentioned | — | none | **no socket** |
| Magnetic phone attachment | — | ✅ "built-in magnetic ring… different position from the first-generation X4" | — | — | owner-corroborated |
| Frontlight | **absent** | ✅ explicitly "No" | — | — | n/a |
| Touch | **absent** | ✅ explicitly "No" | — | — | n/a |

### Explicit coverage gaps

1. **The IMU has no feature guide and no example**, despite being the vendor's
   headline differentiator. This is the largest single hole in the record.
2. **No `features/` guide exists for any capability of this device.** The
   directory holds only a `README.md`. The X4 Pro and X3 have full sets; the X4
   Classic does not, and round 2 did not close that — it is called out here
   rather than quietly left.
3. **Zero capabilities have been exercised on X4 Classic hardware by anyone whose
   work is public**, with the single exception of CrossPoint's sleep-screen
   rendering, reported in one Reddit comment.
