# Cardputer ADV — compatibility and status

> Snapshot **2026-09-04**. Keyed by hardware revision and software version.
> **Nothing in this table was tested on hardware by this session.** Status values are:
> `official` (vendor states it), `source` (read from code at a pinned commit),
> `reported` (firsthand community report, cited), `inferred`, `not-established`.

## 1. Vendor libraries

| Library | Version / commit | v1.0 | v1.1 | ADV | Status |
|---|---|---|---|---|---|
| `M5Cardputer` | **1.1.1**, `f1392858` (2026-07-21) | ✅ | ✅ | ✅ | `source` |
| `M5Cardputer` | < 1.1.1 | ✅ | ✅ | ❌ **keyboard silent** | `source` — ADV support landed `c331c7d`…`8ab9f43`, 2025-08-29…09-02 |
| `M5Cardputer` | < `eccba25` (2026-05-11) | ✅ | ✅ | ⚠ no fn layer → **no arrow keys** | `source` |
| `M5Unified` | `8530f537` (2026-08-27) | ✅ | ✅ | ✅ | `source` |
| `M5GFX` | `d91077b9` (2026-08-25) | ✅ | ✅ | ✅ | `source` |
| `M5Cardputer-UserDemo` | `main` `a34d7ebc` | ✅ | ✅ | ❌ | `source` |
| `M5Cardputer-UserDemo` | **`CardputerADV`** `b549eac0` (2026-06-08) | ❌ | ❌ | ✅ | `source` |

The single most common ADV problem is an old `M5Cardputer` library: `Keyboard_Class::begin()`
falls through to the base `KeyboardReader`, which does nothing, prints one `[error]` line, and
reports no keys. **Check your library version before anything else.**

## 2. ⚠ The autodetect hazard, both directions

M5GFX decides `board_M5CardputerADV` by driving G9/G8/G6/G5 as input-pulldown and testing
`(result & 0x0C) == 0x0C` — i.e. *"are G8 and G9 pulled up?"*. On the ADV they are, by R36/R37
(3.3 kΩ). On a v1.x they are 74HC138 address lines with no pull-up.

| Scenario | Outcome |
|---|---|
| Stock ADV | detected correctly |
| Stock v1.0/v1.1 | detected correctly |
| **v1.x with anything pulling G8 *and* G9 high** | **misdetected as ADV** → TCA8418 reader installed → keyboard dead. On a v1.x, G8/G9 are keyboard address lines, so this requires deliberate external wiring, but a probe clip or a mis-built harness will do it. |
| ADV with the internal I²C bus shorted low | misdetected as v1.x → GPIO-matrix reader → keyboard dead **and** the reader drives G8/G9/G11 as outputs into a live I²C bus |
| ADV in a case that stresses the FPC | display autodetect fails first (the panel-ID read on G37 gates everything) |

The second row is the dangerous one, because the fallback reader *drives* pins that are a bus.
`inferred` — not observed.

## 3. Community firmware

| Firmware | Version at snapshot | v1.0 | v1.1 | ADV | Basis | Notes |
|---|---|---|---|---|---|---|
| **Bruce** | `1d555e0d` 2026-08-28 | ✅ | ✅ | ✅ | `source` | one build target, runtime TCA8418 probe. Polled keyboard (100 ms) — less responsive. Inherits the ES8311 reg-`0x01` divergence. |
| **Launcher** (a.k.a. M5Launcher) | `3b91484e` 2026-09-04 | ✅ | ✅ | ✅ | `source` + vendor doc | `CardputerADV.md`; I²C polling only |
| **Meshtastic** upstream | `be2f68b5` 2026-09-03 | ❌ | ❌ | ✅ | `source` | `m5stack-cardputer-adv` variant only |
| **Plai** | ★175, 2026-08-24 | ❌ | ❌ | ✅ | `reported` | *"works great … automatically detected the lora cap"* (u/Big-Bunch2804, 2026-08-05). **Regression 2026-08-29: arrow keys stopped working on ADV; configuration not persisted across firmware switches.** |
| **MeshCore ports** ×3 | 2026-09 | ❌ | ❌ | ✅ | descriptions | `MultiMote/…` self-describes as "still in development" |
| **ESP32Marauder** | `91724fd8` 2026-08-24 | ✅ | ✅ | ✅ | `source` | separate `User_Setup_marauder_m5cardputer_adv.h` |
| **Evil-M5Project** | 2026-08-20 | ✅ | ✅ | ❓ | `not-established` | description lists Cardputer/AtomS3/Fire/Core2, **not** ADV |
| **NEMO** | `0b8c5c73` 2026-07-15 | ✅ | ✅ | ❓ | `inferred` | no ADV config; builds against `M5Cardputer`, so ≥1.1.1 *should* autodetect. Unverified. |
| **MicroHydra** | 2026-08-21 | ✅ | ✅ | ❓ | `not-established` | |
| **Picoware** | 2026-09-03 | ❓ | ❓ | ✅ | description | names "Cardputer ADV" |
| **d4rkmen/M5Apps** | 2026-08-28 | ✅ | ✅ | ✅ | description | *"v1.0, v1.1 and ADV"* |
| **UiFlow2** | live service | ✅ | ✅ | ✅ | `official` | separate doc paths per model |

## 4. Peripherals

| Peripheral | ADV | Basis |
|---|---|---|
| **Cap LoRa-1262** (U214) | ✅ | official; factory firmware `CardputerADV` branch has `main/hal/cap_lora868/`; Meshtastic variant |
| **Cap CC1101 & NFC** (U219) | ✅ | official — released 2026-08-28 "For Cardputer-Adv" |
| Community CAP TFT boards | ✅ reported | `Prokuon/CardputerADV_Cap_TFT-2.8`, ↑989 on r/CardPuter |
| Any Grove I²C unit | ✅ inferred | standard M5 Grove; bus is otherwise empty |
| **Cap boards on v1.0/v1.1** | ❌ | no connector, and no free pins to build one |
| **Cardputer Accessory Kit v1.1** (M5StampS3A + display, $9.95) | ⚠ | sold as a v1.1 spare. It is a *Stamp-S3A + display*, i.e. the parts the ADV also uses, but it is **not** an ADV upgrade path — the mainboard is what differs. |

## 5. Known failures and open reports

| Symptom | Revision | Cause / status |
|---|---|---|
| Keyboard reports nothing | ADV | `M5Cardputer` < 1.1.1, or autodetect failed. Check the boot log. |
| No arrow keys | ADV | library older than `eccba25` (2026-05-11), or third-party firmware that never implemented the fn layer |
| Arrow keys stopped working after an update | ADV | **firsthand regression report**, Plai, 2026-08-29 |
| RGB LED dim/dead when the backlight is dimmed | v1.1 and ADV | **by design** — shared `BL_3V3` rail. Vendor documents it for v1.1 only. |
| Speaker silent after using the microphone | ADV | **driver defect** — the mic disable sequence powers the shared codec down. [`features/audio.md`](features/audio.md) §6.2 |
| Device will not charge | all | power switch must be **ON** to charge (vendor states this on all three pages) |
| Black screen on power-on | ADV | **unresolved** — r/M5Stack 2026-08-22, two low-information replies. Single report. |
| Configuration lost when switching firmware | ADV | reported for Plai; NVS layouts differ between firmwares. Expect to re-provision. |
| Cannot source replacement screws/buttons | ADV | reported 2026-08-05; M5Stack sells a mixed M3 pack, buttons are commonly 3D-printed |

## 6. Combination testing

Covered in [`resources-and-conflicts.md`](resources-and-conflicts.md) §6. The combinations that
**fail** rather than merely being tight:

* microphone→speaker without an explicit re-enable (driver defect),
* backlight PWM + RGB LED (shared rail),
* IMU motion-wake from deep sleep (no interrupt line established),
* wall-clock time across a power cycle (no RTC).

## 7. What "untested" means here

This session had **no Cardputer hardware**. Every ✅ above means "the code, the schematic or the
vendor says so", and every `reported` means "a named person on a dated public post says so".
None of it means "I saw it work".
