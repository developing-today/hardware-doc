# Compatibility and status — XIAO ESP32S3 Sense

> What is known to work, what is known to fail, and by which hardware/software version.
> Snapshot **2026-08-24**. **Nothing here was verified on hardware in this pass** — statuses come from vendor documentation, inspected source, and owner reports, each labelled.

Evidence: **official** (vendor states it) · **source** (read in working code) · **reported** (owner firsthand) · **inferred** · **absent** (no evidence found).

## 1. Hardware revisions

| Rev | Date | Change | Compatibility impact |
|---|---|---|---|
| v1.0 | 2023-01-04 | Initial | — |
| v1.1 | 2023-03-27 | — | — |
| **v1.2** | **2023-07-25** | **R5 0 Ω → L5 24 nH** in the crystal path | Only electrically meaningful revision. Boards **older than v1.2** have a plain link |
| **v1.3** | **2025-10-21** | Silkscreen removal (K1/K2/U3/U4), C30/C16 moved, shield hole clearance | **Cosmetic/mechanical only** |

Published as "v1.5"; the design is **v1.3**. See [`gaps-and-conflicts.md` §2](gaps-and-conflicts.md#2-the-schematics-own-revision-number-contradicts-its-filename).

**No documented incompatibility exists between revisions.** All firmware and all pin mappings apply to every revision.

## 2. Camera sensor variants

| Sensor | Era | Status | Compatibility |
|---|---|---|---|
| OV2640 | 2023 – ~2024 | **discontinued** | ✅ all wiki examples work |
| **OV3660** | current | **shipping** | ✅ all wiki examples work |
| OV5640 | upgrade SKU | sold separately | ✅ examples work; ⚠ see §4.1 |

`esp32-camera` auto-detects all three (**official** + **source** — all three driver strings are present in the factory binary). Code that pokes sensor registers directly is **not** portable between them.

**You cannot tell which sensor you have from the SKU.** Read `esp_camera_sensor_get()->id.PID` at runtime.

## 3. Software stack support

| Stack | Version | Board | Camera | Mic | SD | Status |
|---|---|:-:|:-:|:-:|:-:|---|
| Arduino-ESP32 | **2.0.7** | ✅ | ✅ | ✅ (`I2S.h`) | ✅ | **official** — the factory firmware's own toolchain |
| Arduino-ESP32 | **3.x** | ✅ | ✅ | ✅ (`ESP_I2S.h`) | ✅ | **official** — vendor ships 3.0.x camera examples |
| ESP-IDF | **≥ 5.0** | ✅ | ✅ | ✅ | ✅ | **source** — [`XIAO_Webcam`](examples/selected/XIAO_Webcam/) |
| PlatformIO | `espressif32`, board `seeed_xiao_esp32s3` | ✅ | ✅ | ✅ | ✅ | **source** — [Retro Camera](examples/selected/XIAO-ESP32S3-Sense_Retro_Camera/) |
| ESPHome | current | ✅ | ✅ | ✅ | ⚠ | **source** — [ha-cam](examples/selected/xiao-esp32s3-sense-ha-cam/), and a community YAML on r/Esphome |
| MicroPython | mainline | ✅ | ❌ | ⚠ | ✅ | **reported** — camera needs a custom build |
| CircuitPython | community | ✅ | ⚠ | ⚠ | ✅ | **reported** — not equivalent to Arduino |
| Zephyr | — | ✅ | ❌ | ❌ | ⚠ | **official** board only; sensors unsupported |
| NuttX | — | ✅ | ❌ | ❌ | ⚠ | **official** board only |
| MicroBlocks | — | ✅ | ❌ | ❌ | ❌ | **official** — GPIO level |
| Rust `esp-hal` | — | ⚠ | ❌ | ❌ | ⚠ | **reported** — one unlicensed crate |
| TinyGo | — | ⚠ | ❌ | ❌ | ❌ | **reported** — family examples only |

### The 2.x → 3.x break

**Confirmed incompatibility.** Arduino-ESP32 3.x (ESP-IDF 5.x) rewrote the I²S API and renamed `esp32-camera`'s `pin_sscb_*` to `pin_sccb_*`.

| Symptom | Cause | Fix |
|---|---|---|
| `I2S.h: No such file` | Sketch is 2.x, core is 3.x | Use `ESP_I2S.h`, `setPinsPdmRx(42,41)` |
| `'pin_sscb_sda' has no member` | idem | Rename to `pin_sccb_sda` |
| `ledcSetup` undefined | idem | Use `ledcAttach()` |

**Most community microphone code predates 3.x.** Anything last touched before mid-2024 is probably 2.x — including [`Xiao_Sense_CameraWebServer_Audio`](examples/best.md#3-xiao_sense_camerawebserver_audio) (2024-03).

## 4. Known-failing and problematic combinations

### 4.1 OV5640 fixed-pattern noise — **reported, unresolved**

Vertical lines in the same position frame-to-frame, worst in dark scenes. **Two independent owner reports**; the reporter explicitly notes the stock **OV3660 does not exhibit it**.

| Mitigation | Effect | Evidence |
|---|---|---|
| `XCLK` 20 MHz → **6 MHz** | "much less noticeable" | **reported**, one owner |
| 100 nF ceramics close to the camera | suggested | **inferred** |
| Heat sink / fan | suggested | **inferred** |

Status: **unresolved**. Source: [`community.md` §4.1](community.md#41-the-ov5640-upgrade-has-a-fixed-pattern-noise-problem).

### 4.2 Camera works cold, fails after soft reset — **architectural**

No `RESET`/`PWDN` line, so `esp_restart()` does not reset the sensor. **Only a full power cycle recovers it.** Evidence: **source** (`camera_pins.h` declares −1) + **primary** (netlist). Not fixable in software.

### 4.3 SD corruption when the user LED is driven — **primary evidence**

GPIO21 is both `LED_BUILTIN` and SD `CS`. **Never drive `LED_BUILTIN` while the card is mounted.** Confirmed from the netlist and vendor code. Notably **absent from community complaints**, which likely means people hit it and misattribute the cause.

### 4.4 JTAG unavailable with the daughterboard — **primary evidence**

Camera + mic occupy all four JTAG pins. Not fixable.

### 4.5 Thermal under sustained streaming — **reported**

One owner reports **~82 °C (180 °F) in open air** while streaming video. Seeed claims 53.5 °C **with dual heat sinks**. Not comparable methods, but consistent in direction.

### 4.6 Camera init failures — **official + source**

Overwhelmingly PSRAM/partition misconfiguration, not hardware. See [`features/camera.md` §4](features/camera.md#4-why-esp_camera_init-fails).

### 4.7 Serial port disappears — **expected behaviour**

Native USB, so the CDC device vanishes on crash/sleep/USB reconfiguration. Recovery: BOOT+RESET. **Official**.

## 5. Accessory compatibility

| Accessory | Sense | Plain S3 | Plus | Notes |
|---|:-:|:-:|:-:|---|
| Sense camera daughterboard | ✅ | ⚠ | ❌ | **Plus B2B is incompatible** (official) |
| **Wio-SX1262 LoRa** | ❌ | ✅ | ✅ | B2B occupied by the camera on the Sense |
| XIAO Expansion Board (OLED/RTC/buzzer) | ✅ | ✅ | ✅ | Uses the 14-pin header |
| Round Display for XIAO | ✅ | ✅ | ✅ | ⚠ **SD CS is `D2`, not 21** |
| Heat sink (single/dual) | ✅ | — | ⚠ | Dual sink **blocks the Plus BAT pin** |
| microSD > 32 GB | ⚠ | — | — | Needs FAT32 reformat; outside vendor support |

**You cannot have both a camera and LoRa on one XIAO.** This is the most consequential accessory incompatibility and it disappoints people regularly — see [`community.md` §3](community.md#3-the-use-case-the-vendor-catalogue-understates-lora-mesh).

## 6. Untested / unknown

| Item | Why it matters |
|---|---|
| All four features simultaneously (camera + mic + SD + Wi-Fi) | No verified example; DMA and the 600 mA rail are the risks |
| microSD throughput | No figure from anyone |
| Wi-Fi throughput | One unlicensed benchmark exists, unrun |
| Deep-sleep current | **Three contradictory vendor figures** |
| Camera frame rates achieved in practice | Sensor maxima are not board maxima |
| USB HID / MSC | Silicon supports it; nobody has demonstrated it here |
| Long-term B2B connector reliability | Repeated mating is the obvious wear point |

## 7. Related
- [`coverage.md`](coverage.md) · [`performance.md`](performance.md) · [`community.md`](community.md) · [`gaps-and-conflicts.md`](gaps-and-conflicts.md) · [`resources-and-conflicts.md`](resources-and-conflicts.md)
