# DinMeter v1.1 — feature coverage

The full 20-capability matrix, the "not present" list and the coverage summary are in
**[`../dinmeter/coverage.md`](../dinmeter/coverage.md)** and apply to v1.1 unchanged, because the
carrier's capability set is unchanged.

This page records the v1.1-specific coverage status.

---

## 1. Capabilities whose coverage differs

| Capability | v1.0 status | v1.1 status | Gap |
|---|---|---|---|
| **RGB LED** | works out of the box | **needs `GPIO38 = HIGH` — predicted, unverified** | ⚠ **No example exists anywhere**, official or community. The one feature that changed is the one feature nobody has demonstrated |
| **Display** | ST7789V2, datasheet retained | **ST7789P3, no datasheet exists** | Command-compatibility assumed, not verified |
| Wi-Fi / BLE *performance* | — | antenna match rebuilt; vendor claims better | **Unmeasured**; no figure published |
| Everything else (18 capabilities) | — | **identical** | as v1.0 |

## 2. Coverage summary

| Metric | v1.1 |
|---|---:|
| Advertised/fitted capabilities | 20 (same set as v1.0) |
| With a task-oriented feature guide | 20 / 20 (all in the v1.0 record, linked from [`features/README.md`](features/README.md)) |
| With official v1.1-specific documentation | **3** — the RGB-LED/GPIO38 note, Power On/Off, Download Mode |
| With an official example built for v1.1 | **0** — no v1.1-specific example exists |
| With a community example built for v1.1 | **0** — no project distinguishes the revisions |
| **Build-tested here** | **0** |
| **Hardware-tested here** | **0** |
| v1.1-specific gaps recorded | 8, in [`gaps-and-conflicts.md`](gaps-and-conflicts.md) |

## 3. Evidence coverage for the delta itself

This is where v1.1 coverage is actually strong, so it is worth stating what *is* established:

| Delta claim | Evidence | Status |
|---|---|---|
| Module changed Stamp-S3 → Stamp-S3A | vendor comparison table + both schematics | **established** |
| RGB LED moved to a switched rail gated by GPIO38 | vendor prose ×2 + net reading in both schematics | **established** |
| That this breaks stock M5Unified | grep of M5Unified master `8530f537…` | **inferred** (source read; not reproduced) |
| DC-DC replaced (`M2` → `U4` + external inductor) | designator diff + net/ball reading | **established** |
| DC-DC current rating 1 A → 0.6 A | datasheet (`M2`) vs sheet annotation (`U4`) | **established** |
| Antenna match rebuilt | designator diff + value reading | **established** (topology); values indicative |
| Antenna *performs* better | vendor claim only | **unverified** |
| No PSRAM on either | vendor spec + Launcher `build_unflags` | **established** |
| USB path unchanged | identical designators and nets on both sheets | **established** |
| Pin compatibility | identical 23-IO list + no new footprint + identical STL | **established**, with the 24/26 mm caveat |
| Price unchanged | shop JSON, both SKUs | **established** |
| Existing firmware runs unmodified | pin-by-pin comparison + board-enum grep | **established** except the LED |
| Display controller renamed | vendor page ×3 places | **established** |
| ST7789P3 ≡ ST7789V2 in behaviour | absence of contrary evidence | **inferred** |
| Carrier PCB physically unchanged | byte-identical published assets | **NOT established** — only the *documentation* is unchanged |

## 4. The gaps worth closing, in order

1. **Test the RGB LED on a v1.1 unit** (with and without the GPIO38 line). Converts the single
   most consequential inference in the record into a measurement. Ten minutes.
2. **Flash a v1.0-built binary onto a v1.1 unit.** Confirms the source-compatibility verdict.
3. **OCR or read `S007-V033_PinMap_01.jpg`.** Settles the rear-FPC numbering question.
4. **Photograph a v1.1 PCB.** The only way to test whether the carrier really is unchanged.
5. **RSSI comparison, v1.0 vs v1.1.** The only way to test the antenna claim.

→ [`../dinmeter/coverage.md`](../dinmeter/coverage.md) for the full matrix.
