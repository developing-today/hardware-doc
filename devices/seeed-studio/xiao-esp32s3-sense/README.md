# Seeed Studio XIAO ESP32S3 Sense

> **SKU 113991115** · product page [`XIAO-ESP32S3-Sense-p-5639`](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html)
> Design revision **v1.3** (published as "v1.5" — see [conflict #2](gaps-and-conflicts.md#2-the-schematics-own-revision-number-contradicts-its-filename))
> Status: **in production** · Research snapshot **2026-08-24**

A 21 × 17.8 mm ESP32-S3 board with a detachable camera/microphone/microSD daughterboard. Thumbnail-sized, Wi-Fi + BLE, 8 MB PSRAM, and the cheapest credible route to a networked camera you can put inside something.

---

## Common tasks / How do I…?

| Question | Answer |
|---|---|
| **Which pin is which?** | [`pinouts-and-buses.md`](pinouts-and-buses.md) — derived from the PCB netlist, not retyped from the wiki |
| **What is the daughterboard connector pinout?** | [`pinouts-and-buses.md` §2](pinouts-and-buses.md#2-the-j3-board-to-board-connector-sense-daughterboard-interface) — **not published by Seeed**; reconstructed here |
| **Why doesn't my new board do anything?** | [`factory-firmware.md` §5](factory-firmware.md#5-the-factory-demo-cannot-connect-to-your-network) — the factory demo has Seeed's own Wi-Fi credentials baked in |
| **Why does my SD card corrupt when I blink the LED?** | [`pinouts-and-buses.md` §7.1](pinouts-and-buses.md#71-the-user-led-and-the-sd-card-chip-select-are-the-same-pin) — they are the same pin (GPIO21) |
| **Why can't I use JTAG?** | [`pinouts-and-buses.md` §7.2](pinouts-and-buses.md#72-the-camera-and-microphone-occupy-all-four-jtag-pins) — the daughterboard owns all four JTAG pins |
| **My battery-powered board does nothing** | Probably `while(!Serial);` — [`features/deep-sleep.md` §7](features/deep-sleep.md#7-sleep-mechanics-on-this-board) |
| **Can I add the camera board to a plain XIAO ESP32S3?** | **No** — the B2B connector is not fitted ([FCC letter](regulatory-and-certification.md#4a-what-the-model-differences-exhibit-says--read-2026-08-24)) |
| **How do I read the battery voltage?** | You cannot, without adding hardware — [`pinouts-and-buses.md` §8.2](pinouts-and-buses.md#82-there-is-no-battery-voltage-sense--confirmed-by-the-vendor) |
| **Why won't `esp_camera_init()` work?** | Almost always PSRAM/partition settings — [`development.md`](development.md) |
| **Which camera do I actually have?** | Probably an **OV3660**, not the advertised OV2640 — read the PID at runtime; full comparison in [`camera-sensors.md`](camera-sensors.md), background in [conflict #5](gaps-and-conflicts.md#5-the-camera-sensor-fitted-has-changed-and-the-product-page-is-stale) |
| **Which example should I start from?** | [`examples/best.md`](examples/best.md) |
| **How do I restore the factory firmware?** | [`factory-firmware.md` §6](factory-firmware.md#6-restoring-the-factory-firmware) |
| **How do I run a model on it (TinyML)?** | [`features/tinyml.md`](features/tinyml.md) — and note most "AI" projects use the cloud |
| **What's actually on the camera board?** | [`sense-daughterboard.md`](sense-daughterboard.md) — full schematic analysis |
| **How do I fix the LED/SD-card clash?** | Move one 0 Ω resistor — [`sense-daughterboard.md` §5](sense-daughterboard.md#the-gpio3-vs-gpio21-contradiction-is-now-explained) |
| **Why is my deep-sleep current so high?** | The camera can't power down — [`features/deep-sleep.md`](features/deep-sleep.md) has the fix (~26x) |
| **How do I use the microphone?** | [`features/microphone.md`](features/microphone.md) — mono, 16-bit, `I2S_NUM_0` only |
| **How do I use the SD card?** | [`features/microsd.md`](features/microsd.md) — `SD.begin(21)`, FAT32, ≤32 GB |
| **How long will it run on a battery?** | [`features/battery-and-power.md`](features/battery-and-power.md) — and why the vendor figures disagree |
| **Can I use Bluetooth audio (A2DP)?** | **No** — [`features/ble.md` §1](features/ble.md#1--there-is-no-bluetooth-classic) |
| **How do I use BLE?** | [`features/ble.md`](features/ble.md) — and use NimBLE if the camera is also in the build |
| **How do I update firmware over the air?** | [`features/ota-and-storage.md`](features/ota-and-storage.md) — mind the 3,264 KB ceiling |
| **How do I talk to another XIAO without Wi-Fi?** | [`features/esp-now.md`](features/esp-now.md) |
| **Can I add LoRa?** | Not with the camera fitted — [`community.md` §3](community.md#3-the-use-case-the-vendor-catalogue-understates-lora-mesh) |
| **How do I mount it?** | No mounting holes — [`community.md` §4.3](community.md#43-there-are-no-mounting-holes) |
| **Is the OV5640 upgrade worth it?** | Usually not — [`market-and-pricing.md` §3](market-and-pricing.md#3-upgrading-to-the-ov5640) |
| **What should I buy instead?** | [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) |
| **What is unresolved / where is the vendor wrong?** | [`gaps-and-conflicts.md`](gaps-and-conflicts.md) |

---

## Identity and variants

| | |
|---|---|
| Manufacturer | Seeed Studio |
| Product | XIAO ESP32S3 Sense |
| SKU | 113991115 |
| SoC | **ESP32-S3R8** — dual-core Xtensa LX7 @ 240 MHz, 512 KB SRAM, **8 MB in-package octal PSRAM** |
| Flash | **GD25Q64ENIGR**, 8 MB (64 Mbit) QSPI |
| Board size | **17.78 × 21.14 mm** (measured from the KiCad `Edge.Cuts` layer) |
| PCB | **4 layers** (`F.Cu / In1.Cu / In2.Cu / B.Cu`) |
| Design licence | **CC BY-SA 4.0** (stated on every schematic sheet) |

### Family

| Variant | Distinguishing feature |
|---|---|
| **XIAO ESP32S3** | Bare board — no camera, no mic, no SD, no B2B connector |
| **XIAO ESP32S3 Sense** ← *this* | Adds the daughterboard: camera + PDM mic + microSD, via a 30-pin B2B connector |
| **XIAO ESP32S3 Plus** | 16 MB flash, 18 GPIO, 2× UART, 2× SPI, larger footprint. **B2B is compatible with the Wio-SX1262 LoRa board but *not* with the Sense camera board** |

Sensor options sold for the Sense daughterboard: **OV2640** (1600×1200, *discontinued*), **OV3660** (2048×1536, *current*), **OV5640** (2592×1944, sold as an upgrade with a heat sink).

---

## Architecture

```
        ┌──────────────── XIAO mainboard (17.8 × 21.1 mm, 4-layer) ────────────────┐
USB-C ──┤ UBF31-0171 ──22Ω── GPIO19/20 (native USB, no bridge IC)                  │
        │ SGM40567 charger ── VBAT ── bottom BAT± pads   R10=220K ⇒ ~110 mA charge │
        │ SGM6029 buck-boost ── VCC_3V3 (600 mA)                                   │
        │ ESP32-S3R8 ──QSPI── GD25Q64 8 MB flash                                   │
        │ U.FL ANT1 (no PCB antenna — external antenna required)                    │
        └───────────────────────────── J3 ─────────────────────────────────────────┘
                    Hirose DF40C-30DP-0.4V(51), 30 signals + 4 mechanical
        ┌───────────────────────── Sense daughterboard ────────────────────────────┐
        │ Camera (OV2640/3660/5640) — 8-bit DVP + SCCB, no PWDN, no RESET          │
        │ PDM microphone — GPIO42 CLK / GPIO41 DATA (mono)                          │
        │ microSD — SPI 1-bit, CS = GPIO21 (shared with the user LED)              │
        └──────────────────────────────────────────────────────────────────────────┘
```

Component records: [ESP32-S3R8](../../../components/espressif/esp32-s3r8/README.md) *(its ESP-IDF/IoT-Solution guides are [archived out of the repo](../../../components/espressif/esp32-s3r8/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md), ~77 MiB)* · [GD25Q64E](../../../components/gigadevice/gd25q64e/README.md) · [SGM40567](../../../components/sgmicro/sgm40567/README.md) · [SGM6029](../../../components/sgmicro/sgm6029/README.md) · [OV3660](../../../components/omnivision/ov3660/README.md) · [OV2640](../../../components/omnivision/ov2640/README.md) · [OV5640](../../../components/omnivision/ov5640/README.md) · [DF40C-30DP](../../../components/hirose/df40c-30dp-0.4v/README.md) · [MSM261D3526H1CPM](../../../components/memsensing/msm261d3526h1cpm/README.md)

Manufacturer guides: [Espressif](../../../vendors/espressif/README.md) · [OmniVision](../../../vendors/omnivision/README.md) — camera part-numbering, the DVP/MIPI split and how OmniVision documents (or does not document) its register sets · [Seeed Studio](../../../vendors/seeed-studio/README.md)

---

## What makes it distinctive

**The size-to-capability ratio is the whole product.** At 17.8 × 21.1 mm with a camera, a microphone, SD storage, Wi-Fi and BLE, there is essentially nothing else in this class. If your constraint is "must fit inside X", this board frequently wins by default.

**8 MB of PSRAM is unusually generous** for a board this small, and it is what makes the camera useful — QVGA/VGA framebuffers, or a couple of full-resolution JPEG buffers, live comfortably in PSRAM.

**Native USB.** No CH340/CP2102 bridge. That is why it can be a USB webcam ([`examples/best.md` §4](examples/best.md#4-xiao_webcam)) or a HID device, and why the serial port vanishes when firmware misbehaves.

**Open design data.** Seeed publishes KiCad sources under CC BY-SA 4.0. That is what made the netlist-derived documentation in this tree possible, and it is genuinely rare at this price.

## Shortcomings

Ordered by how much grief each causes in practice.

1. **The daughterboard consumes all four JTAG pins.** No hardware debugging with the Sense board attached. Non-negotiable, silicon-level.
2. **The user LED and SD chip-select are the same pin (GPIO21).** Silent data corruption if you treat the LED as a status indicator.
3. **No battery voltage sense.** Vendor-confirmed. Battery-powered designs need external hardware.
4. **The camera has no power-down or reset line.** You cannot recover a wedged sensor without a full power cycle, and you cannot power it down to save energy. Vendor figures claim ~34 µA deep sleep, but **owners measure ~90 mA once the camera has been used** — see [`features/deep-sleep.md`](features/deep-sleep.md).
5. **GPIO33–37 are gone**, consumed by in-package PSRAM. Using them corrupts memory rather than erroring.
6. **The antenna is a detachable U.FL part with no PCB fallback.** It falls off; Wi-Fi then behaves strangely rather than failing cleanly.
7. **It runs hot** under sustained camera use — Seeed sells heat sinks and quotes ~53.5 °C with dual sinks.
8. **The factory firmware is useless out of the box** (hardcoded credentials).
9. **Documentation quality is mixed.** The wiki is extensive but contains internal contradictions ([`gaps-and-conflicts.md`](gaps-and-conflicts.md)), and the B2B pinout is simply absent.

---

## Power

| Mode | Sense (3.8 V) |
|---|---|
| Modem-sleep | 31.6 mA |
| Light-sleep | 2.45 mA |
| **Deep-sleep** | **33.51 µA** |
| Webcam, average | ~155 mA |
| Webcam, peak | ~366 mA |
| Mic record + SD write, avg | 64.5 mA |

Vendor figures, **not measured here**; Seeed's own table also contains a contradictory 3 mA deep-sleep row ([conflict #4](gaps-and-conflicts.md#4-seeeds-own-spec-table-gives-two-different-deep-sleep-figures-for-the-sense)). Charging is ~100–110 mA ([conflict #3](gaps-and-conflicts.md#3-battery-charge-current-110-ma-schematic-vs-100-ma-wiki)), programmable via R10.

---

## When to use / when not to use

**Use it when** you need a camera or microphone in a very small space; you want PSRAM headroom for image work; you are doing TinyML vision; you want USB device-class flexibility; or you value having real schematics.

**Do not use it when** you need JTAG debugging alongside the sensors; you need battery telemetry without adding hardware; you need microsecond-clean deep sleep (the camera's idle draw dominates); you need Bluetooth Classic — the ESP32-S3 has **BLE only**, no A2DP/SPP/HFP (see the [ESP32-S3R8 record](../../../components/espressif/esp32-s3r8/README.md#radio-capabilities-and-the-classic-bluetooth-limitation)); or you need 5 GHz Wi-Fi.

**Consider instead:** the bare **XIAO ESP32S3** if you do not need the sensors (better sleep, JTAG free); the **XIAO ESP32S3 Plus** for more I/O and 16 MB flash; a **XIAO nRF52840 Sense** for low-power BLE with battery sensing; or a conventional **ESP32-S3-EYE / ESP32-CAM** class board where size is not the constraint and you want PWDN/reset control.

---

## Documentation map

| Document | Contents |
|---|---|
| [`pinouts-and-buses.md`](pinouts-and-buses.md) | GPIO map, J3 pinout, camera/mic/SD buses, conflicts, power tree |
| [`factory-firmware.md`](factory-firmware.md) | Shipped firmware analysis, flash map, restore procedure |
| [`gaps-and-conflicts.md`](gaps-and-conflicts.md) | Vendor errors, source disagreements, open questions |
| [`development.md`](development.md) | Arduino / ESP-IDF / PlatformIO / MicroPython / ESPHome setup |
| [`camera-sensors.md`](camera-sensors.md) | OV2640 / OV3660 / OV5640 compared as parts |
| [`features/camera.md`](features/camera.md) | Using the camera on this board |
| [`bom-and-board-construction.md`](bom-and-board-construction.md) | Full BOM, stackup, DNP parts, charge-current mod |
| [`resources-and-conflicts.md`](resources-and-conflicts.md) | GPIO/bus/timer/DMA/power budgets, simultaneous-use matrix |
| [`projects-and-community.md`](projects-and-community.md) | 117 projects mined from Seeed's catalogue |
| [`commands.md`](commands.md) | Command ledger with execution status |
| [`features/README.md`](features/README.md) | **All 7 feature guides** — camera, mic, SD, power, Wi-Fi/BLE, USB, GPIO |
| [`coverage.md`](coverage.md) | 28 capabilities → evidence, guide, test status |
| [`compatibility-and-status.md`](compatibility-and-status.md) | Works / fails, by revision and software version |
| [`performance.md`](performance.md) | Every known figure, with its evidence class |
| [`market-and-pricing.md`](market-and-pricing.md) | Dated prices, what the daughterboard costs |
| [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) | vs ESP32-CAM, S3-EYE, nRF52840 Sense, Plus |
| [`community.md`](community.md) | Direct community search — firsthand reports |
| [`media.md`](media.md) | Block diagram, official pinout images |
| [`sense-daughterboard.md`](sense-daughterboard.md) | **The sensor board's own schematic** — camera FPC, mic, SD, mod points |
| [`regulatory-and-certification.md`](regulatory-and-certification.md) | FCC filing, antenna performance, internal photos |
| [`examples/best.md`](examples/best.md) | Curated projects, with feature-coverage gaps |
| [`examples/catalog.json`](examples/catalog.json) | All 18 candidates, pinned commits, licences |
| [`examples/vendored-lib-deltas/`](examples/vendored-lib-deltas/README.md) | Dependency audit — includes an expired-root-CA finding |
| [`acquisition/manifest.json`](acquisition/manifest.json) | Every artifact: hash, size, licence, disposition |
| [`sources.md`](sources.md) | Source table with evidence classes |

## Artifact layout

```
artifacts/
├── schematics/      KiCad v1.5 (Sense), EAGLE v1.1/v1.2, expansion board, Plus
├── datasheets/      OV2640 / OV3660 / OV5640, ESP32-S3, XIAO reference design
├── cad/             DXF outlines, 3D models (STEP/STL)
├── kicad/           XIAO series symbols + footprints
├── pinouts/         official pinout spreadsheets
├── firmware/        factory bundles (2 releases, identical binaries)
├── extracted/       unpacked schematic + firmware archives
├── source-snapshots/ arduino-esp32 pins_arduino.h, camera_pins.h
└── wiki-snapshot/   230 markdown files — the complete official wiki source
```

Large binaries and media were moved to `archive/` and replaced with `*.ARCHIVED.md` placeholders carrying hashes and multiple recovery URLs. Exact-duplicate files were replaced with `*.DUPLICATE.md` pointers. Nothing was discarded.

## Provenance note

The pin, net and BOM data here is **derived from Seeed's published KiCad design files**, not transcribed from the wiki, and is cross-checked against Espressif's `arduino-esp32` board variant. Where the wiki and the design files disagree, both are recorded. No hardware was available in this pass — every electrical, thermal and timing figure is vendor-published or computed, never measured. See [`gaps-and-conflicts.md` §13](gaps-and-conflicts.md#13-what-this-research-pass-did-not-cover).
