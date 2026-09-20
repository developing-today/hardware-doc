# Best examples for the XIAO ESP32S3 Sense

> Which projects to actually start from, what each one teaches, and where each one will bite you.
> Surveyed **2026-08-24**. 18 candidates evaluated, 9 vendored into [`selected/`](selected/), the rest recorded as metadata-only in [`catalog.json`](catalog.json).

Selection bias is declared up front: I preferred projects that **exercise the awkward parts of this board** — the camera/microphone JTAG-pin collision, the SD/LED chip-select collision, PSRAM framebuffer pressure, and the Arduino 2.x→3.x API break — over projects that merely blink an LED. A project with 3 stars that shows you how to run the camera as a USB webcam is more useful here than a 300-star project that re-hosts the vendor example.

None of these were built or flashed in this pass — no hardware was available. Assessments come from reading the source and auditing dependencies. Treat build status as **`not-tested`** throughout.

---

## Start here, by goal

| If you want to… | Use | Why |
|---|---|---|
| Get a picture out of the board at all | [`SeeedStudio-XIAO-ESP32S3-Sense-camera`](#1-seeedstudio-xiao-esp32s3-sense-camera) | Vendor-engineer maintained, and the **only** source with separate Arduino 2.x and 3.x variants |
| Camera **and** microphone at the same time | [`Xiao_Sense_CameraWebServer_Audio`](#3-xiao_sense_camerawebserver_audio) | The one project that solves the hard resource-sharing problem |
| A USB webcam (no Wi-Fi) | [`XIAO_Webcam`](#4-xiao_webcam) | Uses native USB UVC — a capability almost nobody exploits |
| Serious continuous audio capture | [`esp32-birdnet-mic`](#2-esp32-birdnet-mic) | Production-grade PDM→RTSP, actively maintained, multi-target |
| Home Assistant integration | [`xiao-esp32s3-sense-ha-cam`](#5-xiao-esp32s3-sense-ha-cam) | Tiny, ESPHome-native, deliberately minimal |
| On-device vision ML | [`Seeed_Arduino_SSCMA`](#6-seeed_arduino_sscma) / [`on-device-vision-ai`](#7-on-device-vision-ai) | Vendor ML stack, and a full documented pipeline |
| A complete product-shaped build | [`XIAO-ESP32S3-Sense_Retro_Camera`](#8-xiao-esp32s3-sense_retro_camera) | Camera + TFT + SD + enclosure, pinned dependencies |
| MicroPython | [`Seeed-Studio-XIAO-ESP32S3-GPIOViewer`](#9-gpio-viewer-micropython) | Rare working MicroPython project for this board |
| To learn the whole board | `Mjrovai/XIAO-ESP32S3-Sense` (metadata-only) | Best *teaching* resource; see note on why it is not vendored |

---

## 1. `SeeedStudio-XIAO-ESP32S3-Sense-camera`

**[limengdu/SeeedStudio-XIAO-ESP32S3-Sense-camera](https://github.com/limengdu/SeeedStudio-XIAO-ESP32S3-Sense-camera)** · 331★ · **MIT** · commit `bb67cd0a` (2026-06-17) · author *Citric Li* (Seeed) · **vendored**, 3.5 MB

The reference implementation, maintained by a Seeed engineer. Contains `take_photos`, `record_video`, `round_display_take_picture`, and — the reason it matters — **`CameraWebServer_for_esp-arduino_2.0.x` and `CameraWebServer_for_esp-arduino_3.0.x` as separate trees**.

**Why that split is the single most useful thing in this repository:** Arduino-ESP32 3.x moved to ESP-IDF 5.x, which rewrote the I²S driver and changed `esp32-camera` initialisation. Most XIAO camera code on the internet was written against 2.0.x and **fails to compile** on a current core. This repo is the only place that gives you both, side by side, so you can see exactly what changed.

- **Start here if** you are new to the board.
- **Pitfall:** the sketches assume PSRAM is enabled and the "8MB with spiffs" partition scheme. Get those wrong in the IDE and `esp_camera_init()` returns `0x105` (`ESP_ERR_NOT_FOUND`) with no useful message. See [`development.md`](../development.md).
- **Covers:** camera, SD, Wi-Fi, JPEG capture, MJPEG streaming.

## 2. `esp32-birdnet-mic`

**[Sukecz/esp32-birdnet-mic](https://github.com/Sukecz/esp32-birdnet-mic)** · 166★ · **MIT** · commit `8552b12a` (2026-08-01) · **vendored**, source only (8 MB)

A PDM-microphone → **RTSP** streamer feeding BirdNET-Go/BirdNET-Pi. The most professionally engineered audio project for this board: OTA updates, a web configuration UI, a browser flasher, and builds for ESP32-S3 / C3 / C5 / C6.

**What it teaches that nothing else does:** how to run the PDM microphone *continuously* without dropouts while the Wi-Fi stack is active. That is a genuinely hard problem on this part — I²S PDM RX, DMA buffer sizing, and Wi-Fi's own DMA appetite all contend, and this codebase has evidently been tuned against real failures.

- **Actively maintained** — releases through v1.22, dated weeks before this snapshot. The best signal of ongoing viability in the whole catalogue.
- **Note:** the prebuilt firmware images (68 MB) and screenshots were archived out; see [`selected/esp32-birdnet-mic/web-flasher.ARCHIVED.md`](selected/esp32-birdnet-mic/web-flasher.ARCHIVED.md). **All source is retained.**
- **Covers:** PDM microphone, I²S DMA, Wi-Fi, RTSP, OTA, web UI, multi-target builds.

## 3. `Xiao_Sense_CameraWebServer_Audio`

**[fabio-garavini/Xiao_Sense_CameraWebServer_Audio](https://github.com/fabio-garavini/Xiao_Sense_CameraWebServer_Audio)** · 34★ · **no licence** · commit `47bb9edc` (2024-03-25) · **metadata-only**

Streams **video and audio simultaneously** from the Sense.

This is the example that addresses the board's defining constraint. The camera occupies the DVP bus and two JTAG pins; the microphone occupies the other two JTAG pins and I2S_NUM_0; both want PSRAM bandwidth and both want to push data over Wi-Fi. Getting them to coexist is the question people actually ask about this board, and this is the most direct answer.

- **⚠ Not vendored: the repository has no licence file.** Absent a licence, redistribution is not permitted, so only the URL and commit are recorded. Fetch it yourself:
  ```bash
  git clone https://github.com/fabio-garavini/Xiao_Sense_CameraWebServer_Audio
  git -C Xiao_Sense_CameraWebServer_Audio checkout 47bb9edc
  ```
- **⚠ Stale:** last touched 2024-03-25, so it predates Arduino-ESP32 3.x. Expect I²S API breakage on a current core; cross-reference the 3.0.x tree from example 1.
- **Covers:** camera + microphone concurrency, HTTP streaming.

## 4. `XIAO_Webcam`

**[KamranAghlami/XIAO_Webcam](https://github.com/KamranAghlami/XIAO_Webcam)** · 3★ · **MIT** · commit `aed81505` (2025-12-30) · **vendored**, 3 MB

An **ESP-IDF** project that makes the board enumerate as a **standard USB UVC webcam**. Plug it into a PC and it appears in any video application — no Wi-Fi, no app, no streaming protocol.

Low star count, high value. This exploits the ESP32-S3's native USB peripheral, which on this board is wired straight to the USB-C connector with no bridge chip ([`pinouts-and-buses.md` §6](../pinouts-and-buses.md#6-usb-boot-and-reset)). Almost every other project treats USB purely as a serial/flashing port and ignores that the silicon can be a USB *device* of arbitrary class.

- **Also the cleanest pure ESP-IDF example** in the catalogue — useful if you want the component-manager workflow rather than Arduino.
- **⚠ Weak dependency pinning:** `main/idf_component.yml` requests `esp32-camera: "=*"` and `espressif/usb_device_uvc: "=*"` — any version. Pin these yourself before relying on a reproducible build.
- **Covers:** USB UVC device class, ESP-IDF component manager, camera.

## 5. `xiao-esp32s3-sense-ha-cam`

**[jmleclercq/xiao-esp32s3-sense-ha-cam](https://github.com/jmleclercq/xiao-esp32s3-sense-ha-cam)** · 4★ · **MIT** · commit `00a269f6` (2026-08-07) · **vendored**, 52 KB

A deliberately **minimal and reproducible** ESPHome configuration for Home Assistant. 52 KB total — essentially a YAML file and a README.

Included precisely *because* it is small. ESPHome hides the entire pin-assignment problem behind a board definition, so this is the shortest path from unboxing to a working camera entity. It is also the best demonstration that for many use cases you should not be writing C at all.

- Very recent (2026-08-07), so it reflects current ESPHome.
- **Covers:** ESPHome, camera, Home Assistant integration.

## 6. `Seeed_Arduino_SSCMA`

**[Seeed-Studio/Seeed_Arduino_SSCMA](https://github.com/Seeed-Studio/Seeed_Arduino_SSCMA)** · 46★ · **MIT** · commit `65a1b206` (2025-06-06) · **vendored**, 5 MB

Seeed's official **SSCMA** (Seeed SenseCraft Model Assistant) Arduino library — the supported route to running vision models, and the bridge to the SenseCraft AI web tooling.

- Vendor-maintained, so it tracks the SenseCraft model zoo.
- **Note:** README illustration GIFs (5 MB) were archived out; source and examples retained.
- **Covers:** on-device inference, camera, model deployment, SenseCraft AI.

## 7. `on-device-vision-ai`

**[webmcu-ai/on-device-vision-ai](https://github.com/webmcu-ai/on-device-vision-ai)** · 14★ · **MIT** · commit `8a8d92ef` (2026-04-28) · **vendored**, source retained

A complete documented ML pipeline for the "XIAO ML kit" — capture, train, deploy, run. Author *Jeremy Ellis*, a long-standing TinyML educator.

Value is in the **write-up**, not just the code: it covers the parts people get stuck on (dataset capture on-device, quantisation, deployment) rather than just shipping a finished model.

- **Note:** the 7.5 MB compiled PDF and 7 MB of LaTeX/photos were archived out — see the `.ARCHIVED.md` placeholders, which include recovery URLs.
- **Covers:** TinyML end-to-end, camera, OLED, model quantisation.

## 8. `XIAO-ESP32S3-Sense_Retro_Camera`

**[barkinsarikartal/XIAO-ESP32S3-Sense_Retro_Camera](https://github.com/barkinsarikartal/XIAO-ESP32S3-Sense_Retro_Camera)** · 19★ · **MIT** · commit `442a6971` (2026-06-15) · **vendored**, source retained

A finished physical product: camera + 2.0" TFT + SD storage + 3D-printed body, built with PlatformIO.

Notable for being the **best-pinned project in the catalogue** — `platformio.ini` pins `ESPAsyncWebServer @ ^3.6.0` and `AsyncTCP @ ^3.3.2`, and correctly sets `-DBOARD_HAS_PSRAM`. It is also a good worked example of the **SD-CS/user-LED collision**: any project doing camera→SD→display has to deal with GPIO21 doing double duty.

- **Note:** 10 MB of STL meshes archived out; placeholder retains recovery URLs.
- **Covers:** camera, SPI TFT (LovyanGFX), microSD, PSRAM, enclosure design.

## 9. GPIO Viewer (MicroPython)

**[TuzaaBap/Seeed-Studio-XIAO-ESP32S3-GPIOViewer](https://github.com/TuzaaBap/Seeed-Studio-XIAO-ESP32S3-GPIOViewer)** · 23★ · **MIT** · commit `ddd1c1cc` (2025-11-03) · **vendored**, 656 KB

Real-time web view of GPIO state, in **MicroPython**.

Included because MicroPython support on this board is genuinely patchy — the camera in particular is not supported by mainline MicroPython — and working examples are scarce. This one is a useful diagnostic tool in its own right when you are debugging pin conflicts.

- **Covers:** MicroPython, GPIO, web UI.

---

## Deliberately not vendored

| Project | Stars | Reason |
|---|---:|---|
| `Mjrovai/XIAO-ESP32S3-Sense` | 322 | **93 MB** — dominated by Jupyter notebooks, datasets and model binaries. Apache-2.0, so redistribution would be fine; excluded purely on size. It is the **best learning resource for the board** and worth cloning yourself: `git clone https://github.com/Mjrovai/XIAO-ESP32S3-Sense && git -C XIAO-ESP32S3-Sense checkout 770dfef0` |
| `Seeed-Studio/edgelab-example-esp32` | 35 | 29 MB, Apache-2.0. Superseded by SSCMA (example 6) for most purposes |
| `Xiao_Sense_CameraWebServer_Audio` | 34 | **No licence** — see example 3 |
| `Xiao-Sense_Assist_ESPHome` | 15 | **No licence.** ESPHome voice-assistant configs; overlaps example 5 |
| `limengdu/XIAO-ESP32S3Sense-Speech2ChatGPT` | 47 | **No licence**, 11 MB. Mic + SD + Wi-Fi + UI integration — technically interesting, legally unclear |
| `2b-t/esp32s3-microros` | 10 | **No licence.** micro-ROS camera streaming; niche but a genuinely distinct approach |
| `trzy/esp32s3-wifi-speed-test` | 2 | **No licence.** Tiny but valuable — it is the only Wi-Fi throughput benchmark found for this board. Fetch it if you need real numbers |
| `wrsturgeon/xiao-esp32s3-sense` | 3 | **No licence.** Rust (`esp-hal`) support crate — the only Rust option located |
| `Mi-Bee-Studio/seeed-esp32s3-cam` | 6 | `NOASSERTION` licence — GitHub could not identify the terms |

**Pattern worth noting:** the majority of the most technically interesting XIAO ESP32S3 Sense projects **carry no licence at all**. That is normal for hobby embedded code but it means a research tree like this one can preserve only their URLs and commit hashes, not their bytes. All are recorded with pinned commits in [`catalog.json`](catalog.json) so they remain retrievable as long as the repositories exist.

---

## Feature coverage across the selected set

| Feature | Covered by | Gap? |
|---|---|---|
| Camera — still capture | 1, 4, 7, 8 | — |
| Camera — MJPEG stream | 1, 5, 8 | — |
| Camera — USB UVC | 4 | — |
| PDM microphone | 2 | Only one vendored project; audio is under-covered |
| **Camera + mic together** | 3 *(metadata-only)* | **Gap — no vendored example** |
| microSD | 1, 8 | — |
| Wi-Fi / HTTP | 1, 2, 5, 8 | — |
| **BLE** | — | **Gap — no selected example uses BLE** |
| USB device classes | 4 | — |
| On-device ML | 6, 7 | — |
| Display (SPI TFT) | 8 | — |
| ESPHome | 5 | — |
| MicroPython | 9 | — |
| ESP-IDF (native) | 4 | — |
| **Battery / power management** | — | **Gap — consistent with there being no battery ADC** |
| **Deep sleep** | — | **Gap** |

Three real gaps: **BLE**, **power management/deep sleep**, and a **vendored** camera+microphone example. The BLE and power gaps are not accidents of my sampling — they reflect what the community actually builds with this board, which is overwhelmingly Wi-Fi cameras. If your application is a battery-powered BLE sensor, there is much less prior art than the board's popularity suggests.

---

## Related

- [`catalog.json`](catalog.json) — all 18 candidates with commit hashes, licences and disposition
- [`search-log.md`](search-log.md) — queries run and result depth
- [`vendored-lib-deltas/README.md`](vendored-lib-deltas/README.md) — dependency audit, including an expired-CA finding
- [`../development.md`](../development.md) — toolchain setup these examples assume
- [`../pinouts-and-buses.md`](../pinouts-and-buses.md) — the pin conflicts these examples work around
