# Product history and family — XIAO ESP32S3 Sense

> Where this board came from, what changed over its life, and where it sits in the XIAO line.
> Snapshot **2026-08-24**. Dates are from primary sources (schematic revision blocks, FCC filings, file timestamps) where possible.

## 1. Timeline

| Date | Event | Evidence |
|---|---|---|
| **2023-01-04** | Mainboard schematic **v1.0** — initial design | schematic revision block |
| 2023-03-24 | **Sense daughterboard v1.0** schematic dated | EAGLE file header |
| 2023-03-27 | Mainboard **v1.1** | revision block |
| **2023-04-14** | FCC module-approval letter | [FCC exhibit](regulatory-and-certification.md) |
| **2023-04-21** | **FCC application** `Z4T-XIAOESP32S3`, covering *both* the plain and Sense models | FCC grant record |
| 2023-02-08 | **Factory firmware built** (Arduino core 2.0.7, IDF v4.4.4) | `esp_app_desc_t` in the shipped binary |
| **2023-07-25** | Mainboard **v1.2** — R5 (0 Ω) replaced by **L5 24 nH** in the crystal path | revision block |
| ~2024 | **OV2640 discontinued**, replaced by **OV3660** — no SKU change | wiki statement |
| 2024-08-14 | Firmware bundle "20240814" published — **binaries unchanged from 2023** | hash comparison |
| **2025-10-21** | Mainboard **v1.3** — silkscreen removal (K1/K2/U3/U4), C30/C16 repositioned, shield hole clearance | revision block |
| 2025-11-15 | XIAO Reference Design catalogue published (129 pp) | PDF metadata |
| **2026-02-26** | Schematics re-released as "**v1.5**" — though the title block still says v1.3 | file dates |

**Only one electrically meaningful revision exists: v1.2**, which changed a 0 Ω link to a 24 nH inductor in the crystal path (a drive/EMC fix). Boards older than v1.2 differ there. v1.3 is cosmetic and mechanical.

The "v1.4"/"v1.5" designations are **document release numbers, not board revisions** — no such entry exists in the revision history. See [`gaps-and-conflicts.md` §2](gaps-and-conflicts.md#2-the-schematics-own-revision-number-contradicts-its-filename).

## 2. The sensor substitution

The most consequential product change happened **silently**:

| Era | Sensor | Resolution |
|---|---|---|
| Launch (2023) | **OV2640** | 1600 × 1200 |
| Current | **OV3660** | 2048 × 1536 |
| Optional upgrade | OV5640 | 2592 × 1944 |

**The SKU did not change.** The product page still headlines the OV2640; the wiki states it is discontinued. A unit bought today most likely has an OV3660.

This is a supply-chain substitution of the kind you should expect to recur — **write code that detects the sensor at runtime** (`esp_camera_sensor_get()->id.PID`) rather than assuming one. Details: [`camera-sensors.md`](camera-sensors.md), [`gaps-and-conflicts.md` §5](gaps-and-conflicts.md#5-the-camera-sensor-fitted-has-changed-and-the-product-page-is-stale).

It also has a **power consequence** discovered late in this research: the OV2640 **cannot** be put into software standby, while the OV3660 can (37.8 mA → 1.45 mA deep sleep). Early boards are therefore materially worse for battery projects than current ones. See [`performance.md`](performance.md#3-power).

## 3. The XIAO family

All share a **17.8 × 21.1 mm** footprint and the same 14-pin castellated pinout — the line's central design idea is that boards are swappable.

| Board | SKU | Silicon | Price | Radio |
|---|---|---|---:|---|
| XIAO SAMD21 | 102010328 | Microchip SAMD21 | — | none |
| XIAO RP2040 | 102010428 | RP2040 | — | none |
| XIAO RP2350 | 102010550 | RP2350 | — | none |
| XIAO nRF52840 | 102010448 | nRF52840 | — | BLE |
| XIAO nRF52840 Sense | 102010469 | nRF52840 + IMU + mic | $12.99 | BLE |
| XIAO ESP32C3 | 113991054 | ESP32-C3 | $4.99 | Wi-Fi 4 + BLE |
| XIAO ESP32C6 | 113991254 | ESP32-C6 | $5.20 | Wi-Fi 6, BLE, Zigbee, Thread |
| **XIAO ESP32S3** | 113991114 | ESP32-S3R8 | $7.49 | Wi-Fi 4 + BLE |
| **XIAO ESP32S3 Sense** | **113991115** | + camera, mic, SD | **$13.99** | Wi-Fi 4 + BLE |
| XIAO ESP32S3 Plus | 102010671 | 16 MB flash, 18 GPIO | $7.90 | Wi-Fi 4 + BLE |
| XIAO RA4M1 | 102010551 | Renesas RA4M1 | — | none |
| XIAO MG24 / Sense | 102010590 / 102010610 | Silicon Labs EFR32MG24 | — | BLE 5.3, Matter |
| XIAO nRF54L15 / Sense | 101991421 / 101991422 | Nordic nRF54L15 | — | BLE 6.0, Matter |

Source: XIAO Reference Design catalogue pp. 9–12 and dated store observations ([`market-and-pricing.md`](market-and-pricing.md)).

### What "Sense" means

A **"Sense" suffix denotes added sensors**, and the added sensors differ by board:

- **ESP32S3 Sense** → camera + PDM microphone + microSD, on a **detachable** daughterboard
- **nRF52840 Sense** → 6-axis IMU + microphone, **on-board**
- **MG24 Sense** / **nRF54L15 Sense** → 6-axis IMU + microphone

Only the ESP32S3 Sense has a camera, and only it uses a detachable sensor board.

## 4. Ecosystem and accessories

| Accessory | Works with the Sense? |
|---|---|
| OV5640 camera upgrade + heat sink | ✅ replaces the sensor on the FPC |
| Aluminium heat sinks (single/dual) | ✅ recommended under camera load |
| XIAO Expansion Board (OLED/RTC/buzzer/SD) | ✅ via the 14-pin header |
| Round Display for XIAO | ✅ but SD `CS` becomes `D2` |
| **Wio-SX1262 LoRa** | ❌ **B2B occupied by the camera board** |
| XIAO ESP32S3 Plus base boards | ❌ different mechanical footprint |

The LoRa incompatibility matters more than it looks — [LoRa mesh is the second-largest use case](community.md#3-the-use-case-the-vendor-catalogue-understates-lora-mesh) for XIAO ESP32S3 boards generally, and Sense owners cannot participate without a second board.

## 5. Design culture

Two things distinguish Seeed's approach here, both unusual at this price:

**Design files are CC BY-SA 4.0.** Full KiCad sources for the mainboard and EAGLE sources for the daughterboard. That is what made this research tree's netlist-derived documentation possible, and it is why [the board-to-board pinout](pinouts-and-buses.md#2-the-j3-board-to-board-connector-sense-daughterboard-interface) could be recovered at all.

**The board is sold as a module, not just a dev board.** Castellated edges, all components on one side, [modular FCC approval](regulatory-and-certification.md), and published KiCad footprints — the intent is that you solder it into your own product. This is also why [there are no mounting holes](community.md#43-there-are-no-mounting-holes), which surprises people expecting a dev board.

Against that: the documentation contains [multiple unresolved contradictions](gaps-and-conflicts.md), a [schematic net-name error Seeed has acknowledged but not yet fixed](community.md#4a1-a-vendor-confirmed-schematic-error), and [power figures that owners cannot reproduce](performance.md#3-power). The hardware is more carefully designed than the documentation describing it.

## 6. Related
- [`README.md`](README.md) · [`market-and-pricing.md`](market-and-pricing.md) · [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md)
- [`bom-and-board-construction.md`](bom-and-board-construction.md) — revision detail
- [`regulatory-and-certification.md`](regulatory-and-certification.md) — certification timeline
