# Camera — XIAO ESP32S3 Sense

> How to use the camera, which sensor you actually have, and the constraints nobody documents.
> Snapshot **2026-08-24**. Evidence: schematic netlist (primary), OmniVision datasheets (primary), Espressif `arduino-esp32` (primary), Seeed wiki (vendor prose). **No hardware testing** — nothing here is a firsthand measurement.

> A companion document, [`../camera-sensors.md`](../camera-sensors.md), covers the three sensors as *parts* in more depth (comparison tables, community-sourced figures flagged as such). This page covers using them *on this board*.

## 1. Which sensor do you have?

**This is the first thing to establish, and you cannot tell from the SKU.** Seeed has shipped three different sensors on the same product over its life:

| | **OV2640** | **OV3660** | **OV5640** |
|---|---|---|---|
| Status on the Sense | **Discontinued** — early units | **Current** default | Sold as a **paid upgrade** (with heat sink) |
| Active array | 1600 × 1200 (UXGA) | **2048 × 1536** (QXGA) | **2592 × 1944** (QSXGA) |
| Total array | 1632 × 1232 | — | — |
| Optical format | 1/4" | **1/5"** | 1/4" |
| Pixel size | 2.2 × 2.2 µm | **1.4 × 1.4 µm** | 1.4 × 1.4 µm |
| Technology | OmniPixel2 (FSI) | **OmniBSI** (backside-illuminated) | OmniBSI |
| Sensitivity | 0.6 V/lux-s | **670 mV/lux-s** | 600 mV/lux-s |
| S/N ratio | 40 dB | 34 dB | 36 dB |
| Dynamic range | 50 dB | **70 dB** @ 8× gain | 68 dB @ 8× gain |
| Active current | ~125–140 mW | **98 mA** | **140 mA** |
| Standby current | 600 µA | **20 µA** | 20 µA |
| Chief ray angle | 25° | 27.6° | 24° |
| Shutter | progressive | rolling | rolling / frame exposure |
| Input clock | — | 6–27 MHz | 6–27 MHz |
| Autofocus | no | no | **yes** (AFC + embedded VCM driver) |
| Interface | DVP | DVP | DVP **+ 2-lane MIPI** (MIPI unused here) |
| Package | 38-pin CSP2 | 51-pin CSP3 | 71-pin CSP3 |
| Datasheet version | v1.6, 2006-02-28 | v1.3, 2011-05 (*preliminary*) | v2.03, 2011-05 |

Max frame rates by resolution:

| Resolution | OV2640 | OV3660 | OV5640 |
|---|---|---|---|
| Full array | 15 fps (UXGA) | 15 fps (2048×1536) | 15 fps (2592×1944) |
| 1080p | — | 20 fps | **30 fps** |
| 720p | — | 45 fps | **60 fps** |
| XGA 1024×768 | — | 45 fps | — |
| VGA 640×480 | 30 fps (SVGA) | 60 fps | **90 fps** |
| QVGA 320×240 | 60 fps (CIF) | 120 fps | 120 fps |

These are **sensor** limits. You will not reach them on this board — the DVP bus, PSRAM bandwidth, JPEG encoding and Wi-Fi all sit between the sensor and your application. Treat the table as an upper bound, not a specification.

### Detecting the sensor at runtime

```c
#include "esp_camera.h"
sensor_t *s = esp_camera_sensor_get();
// s->id.PID:  0x26 = OV2640, 0x3660 = OV3660, 0x5640 = OV5640
ESP_LOGI(TAG, "sensor PID 0x%04x", s->id.PID);
```

The `esp32-camera` driver probes over SCCB and loads the right register set automatically, which is why the same factory binary works across all three ([`factory-firmware.md`](../factory-firmware.md) confirms all three driver strings are present in the shipped image). **Code that writes sensor registers directly is not portable between them** — the register maps differ substantially.

### Practical differences that matter

- **OV3660 is 1/5", the others 1/4".** Smaller optical format with the same lens mount means a **narrower field of view** and less light-gathering area. If you upgrade an OV2640 design to OV3660 the framing changes.
- **OV5640 draws 140 mA active** — comparable to the entire rest of the board under load. This is why Seeed sells it with a heat sink and quotes ~53.5 °C with dual sinks.
- **OV3660's datasheet is marked "PRELIMINARY SPECIFICATION"** and several figures (dark current) are "TBD". Treat its numbers as less firm than the OV5640's, which is a released PRODUCT SPECIFICATION.
- **Only the OV5640 has autofocus.** Seeed distributes an autofocus library ([`artifacts/originals/ov5640-autofocus-firmware.zip`](../artifacts/originals/ov5640-autofocus-firmware.zip), retained locally).

  ⚠ **The archive is misleadingly named.** It unpacks to a directory called **`OV5647_AF-main`** — but `OV5647` is a *different* OmniVision sensor (the Raspberry Pi Camera v1 part). The contents are genuinely for the **OV5640**: `library.properties` declares *"OV5640 Auto Focus for ESP32S3"* v1.0.0 by **Eric Nam**, and every source file is `ESP32_OV5640_AF.{h,cpp}` / `ESP32_OV5640_cfg.h`, with an `OV5640_HTTP` example. The upstream repository name simply contains a typo. **Do not discard the file thinking you downloaded the wrong sensor's library.**

  The AF routine is **not in the sensor's ROM** — a firmware blob must be uploaded to the OV5640's embedded microcontroller over SCCB at every power-up, which is what this library does.

> **Licensing note.** The OV3660 and OV5640 datasheets carry an explicit restriction: *"Individuals and/or organizations are not allowed to re-distribute said information."* They are retained in this tree for research use, but their redistribution status is **`restricted`/`unknown`** and they are flagged for review in [`acquisition/manifest.json`](../acquisition/manifest.json). The specification tables above are factual data extracted from them, not a reproduction of the documents.

## 2. Pin wiring

Full detail in [`pinouts-and-buses.md` §3](../pinouts-and-buses.md#3-camera-bus-dvp-8-bit-parallel). Summary, triple-confirmed against the PCB netlist and `camera_pins.h`:

| Signal | GPIO | | Signal | GPIO |
|---|---:|---|---|---:|
| `XCLK` | 10 | | `D0`(Y2) | 15 |
| `PCLK` | 13 | | `D1`(Y3) | 17 |
| `VSYNC` | 38 | | `D2`(Y4) | 18 |
| `HREF` | 47 | | `D3`(Y5) | 16 |
| `SIOD` (SDA) | 40 | | `D4`(Y6) | 14 |
| `SIOC` (SCL) | 39 | | `D5`(Y7) | 12 |
| **`PWDN`** | **−1** | | `D6`(Y8) | 11 |
| **`RESET`** | **−1** | | `D7`(Y9) | 48 |

In Arduino, define `CAMERA_MODEL_XIAO_ESP32S3` before including `camera_pins.h` and all of this is handled.

## 3. Minimal working capture (Arduino)

```cpp
#define CAMERA_MODEL_XIAO_ESP32S3
#include "esp_camera.h"
#include "camera_pins.h"

void setup() {
  Serial.begin(115200);

  camera_config_t c = {};
  c.ledc_channel = LEDC_CHANNEL_0;      // XCLK is generated by LEDC
  c.ledc_timer   = LEDC_TIMER_0;
  c.pin_d0=Y2_GPIO_NUM;  c.pin_d1=Y3_GPIO_NUM;
  c.pin_d2=Y4_GPIO_NUM;  c.pin_d3=Y5_GPIO_NUM;
  c.pin_d4=Y6_GPIO_NUM;  c.pin_d5=Y7_GPIO_NUM;
  c.pin_d6=Y8_GPIO_NUM;  c.pin_d7=Y9_GPIO_NUM;
  c.pin_xclk=XCLK_GPIO_NUM;   c.pin_pclk=PCLK_GPIO_NUM;
  c.pin_vsync=VSYNC_GPIO_NUM; c.pin_href=HREF_GPIO_NUM;
  c.pin_sccb_sda=SIOD_GPIO_NUM; c.pin_sccb_scl=SIOC_GPIO_NUM;
  c.pin_pwdn=PWDN_GPIO_NUM;   c.pin_reset=RESET_GPIO_NUM;   // both -1
  c.xclk_freq_hz = 20000000;
  c.pixel_format = PIXFORMAT_JPEG;
  c.frame_size   = FRAMESIZE_UXGA;
  c.jpeg_quality = 12;                  // 0..63, LOWER is better quality
  c.fb_count     = 2;                   // needs PSRAM
  c.fb_location  = CAMERA_FB_IN_PSRAM;
  c.grab_mode    = CAMERA_GRAB_WHEN_EMPTY;

  if (esp_camera_init(&c) != ESP_OK) { Serial.println("init failed"); return; }
}

void loop() {
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) return;
  Serial.printf("%ux%u  %u bytes\n", fb->width, fb->height, fb->len);
  esp_camera_fb_return(fb);            // ALWAYS return the buffer
  delay(1000);
}
```

**`esp_camera_fb_return()` is not optional.** With `fb_count = 2` you have exactly two buffers; forgetting to return one stalls after the second frame, and forgetting entirely stalls after the first. This is the most common "the camera works once" bug.

## 4. Why `esp_camera_init()` fails

In rough order of frequency. Almost all of these are configuration, not hardware.

| Symptom | Cause | Fix |
|---|---|---|
| `0x105 ESP_ERR_NOT_FOUND`, or init fails at `FRAMESIZE_UXGA` | **PSRAM not enabled.** Framebuffers do not fit in 512 KB SRAM | Arduino: *Tools → PSRAM → **OPI PSRAM***. ESP-IDF: `CONFIG_SPIRAM=y`, octal mode, 80 MHz |
| Sketch does not fit / upload fails | Wrong partition scheme | Arduino: *Partition Scheme → **8MB with spiffs (3MB APP…)*** |
| `0x20004 ESP_ERR_NOT_SUPPORTED`, SCCB probe fails | Daughterboard not seated | Press until it clicks. See §7 |
| Works cold, fails after soft reset | **No `RESET` line** — sensor keeps stale state | Power-cycle. Architectural; see [`pinouts-and-buses.md` §3.1](../pinouts-and-buses.md#31-there-is-no-camera-power-down-or-reset-line--and-that-has-consequences) |
| Compiles on one machine, not another | Arduino core 2.x vs 3.x API break | Use the matching tree from [`SeeedStudio-XIAO-ESP32S3-Sense-camera`](../examples/selected/SeeedStudio-XIAO-ESP32S3-Sense-camera/) |
| Green/pink/torn frames | `xclk_freq_hz` too high, or FPC not seated | Try 10 MHz; reseat the ribbon |
| Random crashes once camera runs | Code touching **GPIO33–37** | Those pins are in-package PSRAM. See [`pinouts-and-buses.md` §7.5](../pinouts-and-buses.md#75-gpio33gpio37-do-not-exist-for-you) |

## 5. Resource cost

- **`XCLK` consumes an LEDC channel and timer** (`LEDC_CHANNEL_0` / `LEDC_TIMER_0` by convention). If you also drive servos or LEDs with `ledcWrite`, avoid channel 0/timer 0.
- **Framebuffers live in PSRAM.** A UXGA JPEG buffer is allocated generously; `fb_count = 2` at UXGA is a meaningful fraction of the 8 MB. Reduce `frame_size` or `fb_count` before blaming PSRAM size.
- **The camera occupies GPIO39 + GPIO40**, which are two of the four JTAG pins — see [`pinouts-and-buses.md` §7.2](../pinouts-and-buses.md#72-the-camera-and-microphone-occupy-all-four-jtag-pins). **You cannot hardware-debug while the camera is attached.**
- **DMA and PSRAM bandwidth contend with Wi-Fi.** Streaming MJPEG over Wi-Fi at high resolution is where this board runs out of headroom, not at capture.

## 6. Using the camera with other features

| Combination | Status | Notes |
|---|---|---|
| Camera + Wi-Fi (MJPEG stream) | **Well trodden** | The default use case; see [`examples/best.md`](../examples/best.md) |
| Camera + microSD | **Works** | ⚠ SD `CS` = GPIO21 = the user LED. Never drive `LED_BUILTIN` while the card is mounted |
| Camera + microphone | **Works, but hard** | Only one project demonstrates it well; see [`examples/best.md` §3](../examples/best.md#3-xiao_sense_camerawebserver_audio) |
| Camera + USB UVC | **Works** | [`XIAO_Webcam`](../examples/selected/XIAO_Webcam/) — no Wi-Fi needed |
| Camera + JTAG debug | **Impossible** | Pin conflict, not a software limitation |
| Camera + deep sleep | **Compromised** | Cannot power the sensor down; Sense sleeps at ~34 µA vs 14 µA bare |

## 7. Handling the daughterboard

Seeed's own removal instructions, which are worth repeating because the connector is fragile:

> Apply gentle pressure from the **side** of the board pair and slide the expansion board off the B2B connector. Work along one edge first, then release the rest of the connector gradually.
>
> **Never pull the expansion board straight up or straight down**, and do not twist or rock the two boards like opening a book — prying vertically can bend pins, crack the connector housing, or break the B2B socket on the XIAO itself.

The connector is a Hirose `DF40C-30DP-0.4V(51)` on 0.4 mm pitch. A broken B2B socket on the mainboard is not practically repairable by hand.

**Thermal:** Seeed quotes **53.5 °C with dual heat sinks**, about 10 °C lower than without, under camera load. If you enclose the board — as most wearable projects do — plan for this. Note their caveat that the dual-heat-sink case is **not compatible with using the BAT pin on the XIAO ESP32S3 Plus**.

## 8. Related

- [`pinouts-and-buses.md`](../pinouts-and-buses.md) — complete wiring, conflicts, J3 pinout
- [`development.md`](../development.md) — toolchain and PSRAM/partition setup
- [`examples/best.md`](../examples/best.md) — working camera projects
- [`gaps-and-conflicts.md` §5](../gaps-and-conflicts.md#5-the-camera-sensor-fitted-has-changed-and-the-product-page-is-stale) — the sensor-substitution conflict
- Local datasheets: [`ov2640`](../../../../components/omnivision/ov2640/artifacts/ov2640-datasheet-v2.2.pdf) · [`ov3660`](../../../../components/omnivision/ov3660/artifacts/ov3660-datasheet.pdf) · [`ov5640`](../../../../components/omnivision/ov5640/artifacts/ov5640-datasheet-v2.03.pdf) · module specs for [OV3660](../../../../components/omnivision/ov3660/artifacts/ov3660-camera-module-spec.pdf) and [OV5640](../../../../components/omnivision/ov5640/artifacts/ov5640-camera-module-spec.pdf)
