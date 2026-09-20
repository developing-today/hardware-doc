# Performance — XIAO ESP32S3 Sense

> What is actually known about how fast, hot and hungry this board is.
> Snapshot **2026-08-24**.

## ⚠ Read this first

**No benchmark was executed in this research pass. No hardware was available.**

Every number below is one of:
- **vendor claim** — published by Seeed, method unstated;
- **silicon limit** — from a component datasheet, an upper bound the board will not reach;
- **owner report** — a single firsthand measurement with no stated instrument;
- **computed** — arithmetic from the above.

Nothing here is an independent, reproduced measurement. Treat the whole page as a **starting point for your own benchmarking**, not as a specification.

## 1. Compute

| Parameter | Value | Class |
|---|---|---|
| CPU | Dual-core Xtensa LX7 @ **240 MHz** | silicon |
| SRAM | 512 KB | silicon |
| PSRAM | **8 MB octal**, 80 MHz recommended | silicon |
| Flash | 8 MB QSPI, DIO 80 MHz (factory) / QIO available | primary |
| Vector ISA | ESP32-S3 PIE/SIMD — the reason it beats the original ESP32 at ML | silicon |

⚠ **Do not run octal PSRAM at 120 MHz.** It is temperature-fragile on the ESP32-S3 — see the [ESP-IDF peripheral guide](../../../guides/espressif/esp-idf-peripheral-capabilities.md#43-esp32-s3--120-mhz-octal-psram-is-temperature-fragile). Given this board's [thermal behaviour](#4-thermal), that is not theoretical.

## 2. Camera frame rates

**Sensor maxima — the board will not reach these.**

| Resolution | OV2640 | OV3660 | OV5640 |
|---|---|---|---|
| Full array | 15 fps | 15 fps | 15 fps |
| 1080p | — | 20 fps | 30 fps |
| 720p | — | 45 fps | 60 fps |
| VGA | 30 fps | 60 fps | 90 fps |
| QVGA | 60 fps | 120 fps | 120 fps |

Class: **silicon limit** (datasheets). Between the sensor and your application sit the DVP bus, PSRAM bandwidth, JPEG encoding and — usually — Wi-Fi. **No measured end-to-end frame rate was located from any source, vendor or community.**

If frame rate matters to your design, benchmark it first. This is the largest single evidence gap on this page.

## 3. Power

Vendor figures. Method, instrument and firmware unstated.

| Mode | Plain S3 | **Sense** |
|---|---|---|
| Modem-sleep | 27 mA | 31.6 mA @ 3.8 V |
| Light-sleep | 2 mA | 2.45 mA @ 3.8 V |
| **Deep-sleep** | **14 µA** | **33.51 µA @ 3.8 V** |
| Webcam avg | — | ~155 mA @ 3.8 V (~140 mA @ 5 V) |
| Webcam peak | — | ~366 mA @ 3.8 V (~347 mA @ 5 V) |
| Mic + SD write avg | — | 64.5 mA @ 3.8 V (54.58 mA @ 5 V) |
| Mic + SD write peak | — | 109.3 mA @ 3.8 V (86.7 mA @ 5 V) |

### The deep-sleep figures are not achievable once the camera is used — measured

Seeed publishes **three mutually contradictory values** (33.51 µA wiki, 3 mA wiki, 26.5 mA catalogue). Owner measurements on the Seeed forum show that **none of them is reachable after the camera has been initialised**, and explain why.

Measured deep-sleep current after taking a picture, same sketch and board, by sensor (`StuartsProjects`):

| Sensor | Plain deep sleep | **+ software standby register** |
|---|---:|---:|
| OV2640 | 22.3 mA | 22.3 mA (**standby does not work**) |
| **OV3660** | 37.8 mA | **1.45 mA** |
| OV5640 | 104 mA | — |

| Condition | Measured | Reporter |
|---|---:|---|
| Camera + SD fitted, **never initialised** | ~2.8 mA | `StuartsProjects` |
| **After a capture + SD write** | **~90 mA** | two reporters |
| ESPHome, camera *not* configured | ~140 µA | `JaBa` |
| ESPHome, camera configured | ~90 mA | `JaBa` |
| **Light sleep** (board + camera + SD) | ~4 mA | `StuartsProjects` |
| Light sleep, bare XIAO (no Sense board) | ~3 mA | `StuartsProjects` |
| **Best achieved**, OV3660 + standby | **<1 mA** | `jksemple` |

**The discrepancy against the wiki's 33.51 µA is three orders of magnitude.** Mechanism: the camera has no `PWDN` line and cannot be powered down, so it keeps drawing current through deep sleep once initialised. Seeed staff have said the wiki figures illustrate relative peripheral impact rather than promising an achievable number.

**The workaround** — writing an OV3660/OV5640 standby register before sleeping — recovers most of it:

```cpp
sensor_t *sensor = esp_camera_sensor_get();
sensor->set_reg(sensor, 0x3008, 0x40, 0x40);   // software standby
```

⚠ **Cancelling standby reportedly leaves the camera non-functional** until a power cycle. Usable for capture→sleep→reset cycles, not for resuming a live camera.

**Practical conclusion: for any battery project, use the OV3660.** It is the only one of the three sensors whose standby works, and it turns a 37.8 mA sleep into 1.45 mA.

Evidence: **firsthand measurement, multiple independent reporters, not reproduced here.** Full detail and quotes: [`community.md` §4A.2](community.md#4a2-deep-sleep-current--the-vendor-figures-are-unachievable-and-here-is-why).

## 4. Thermal

| Observation | Condition | Class |
|---|---|---|
| **~82 °C (180 °F)** | Streaming video, **open air, no heat sink** | **owner report**, single, no instrument stated |
| **53.5 °C** | With **dual heat sinks**, camera load | vendor claim |
| ~63.5 °C implied | Vendor states dual sinks are "🔻10 °C" better | vendor claim |

The two are not directly comparable — different sensors, cooling and workloads, and neither states a measurement point. But both point the same way: **this board runs hot under sustained camera use.**

Practical consequences:
- **Enclosing it requires thermal design.** Most wearable and camera projects enclose it.
- One owner recommends "heat sink and tiny fan if you're putting in a box".
- Heat is implicated in the [OV5640 noise problem](compatibility-and-status.md#41-ov5640-fixed-pattern-noise--reported-unresolved).
- The OV5640 draws **140 mA** vs the OV3660's 98 mA — a further reason to prefer the stock sensor.

Source: [`community.md` §4.2](community.md#42-a-hard-thermal-datum).

## 5. Storage

| Path | Interface | Measured? |
|---|---|---|
| microSD | **SPI 1-bit** (no SDIO — DAT1–3 not routed) | ❌ **nothing published by anyone** |
| SPIFFS | internal flash, 1,536 KB | ❌ |
| Flash read | DIO 80 MHz factory; QIO available | ❌ |

The 1-bit SPI wiring is a **primary-evidence** hard ceiling: no driver configuration can reach SDIO speeds. Sustained camera-to-SD recording is the demanding case; several projects do it, **none report numbers**.

## 6. Wireless

| Parameter | Value | Class |
|---|---|---|
| Wi-Fi | 802.11 b/g/n, 2.4 GHz only | silicon |
| BLE | 5.0 | silicon |
| Range | "100 m+ with U.FL antenna" | vendor claim, unqualified |
| Throughput | **unknown** | — |

The only benchmark located for this board is [`trzy/esp32s3-wifi-speed-test`](https://github.com/trzy/esp32s3-wifi-speed-test) (2 ★, unlicensed, 2023-12). **Not vendored** (no licence) and **not run**. If you need numbers, clone it.

Antenna is **detachable U.FL with no PCB fallback** — a detached antenna is a common cause of apparent poor performance. See [`features/wifi-and-bluetooth.md` §2](features/wifi-and-bluetooth.md#2-the-antenna-is-detachable-and-there-is-no-fallback).

## 7. Computed battery runtimes

Arithmetic from §3. **Not measured**; ignores self-discharge, ageing, temperature and converter efficiency.

| Cell | Deep sleep @ 34 µA | Mic+SD @ 64.5 mA | Webcam @ 155 mA |
|---|---|---|---|
| 250 mAh | ~10 months | ~3.9 h | ~1.6 h |
| 500 mAh | ~1.7 years | ~7.8 h | ~3.2 h |
| 1000 mAh | ~3.4 years | ~15.5 h | ~6.5 h |
| 2000 mAh | ~6.7 years | ~31 h | ~12.9 h |

The multi-year sleep figures are **not shelf-life predictions** — self-discharge and charger leakage bound real life long before. Read them as "sleep current is not your bottleneck". And note they assume the 33.51 µA figure is the correct one of the three.

## 8. What to benchmark first

If you have hardware, these are the highest-value unknowns, in order:

1. **Deep-sleep current** — settles a 790× vendor contradiction.
2. **End-to-end camera frame rate** at QVGA/VGA/UXGA, with and without Wi-Fi streaming.
3. **microSD sequential write throughput** — determines whether video-to-SD is viable.
4. **Junction/case temperature** under sustained streaming, with and without heat sinks.
5. **Wi-Fi throughput** — run `esp32s3-wifi-speed-test`.
6. **All four features concurrently** — camera + mic + SD + Wi-Fi, the untested integration case.

Record method, instrument, firmware version, sensor variant and ambient temperature — the existing figures are hard to use precisely because none of them do.

## 9. Related
- [`compatibility-and-status.md`](compatibility-and-status.md) · [`community.md`](community.md) · [`features/battery-and-power.md`](features/battery-and-power.md) · [`resources-and-conflicts.md`](resources-and-conflicts.md) · [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
