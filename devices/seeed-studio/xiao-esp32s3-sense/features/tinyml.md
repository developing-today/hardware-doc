# TinyML / on-device inference — XIAO ESP32S3 Sense

> Running vision and audio models on the board itself. Three separate toolchains, one important performance trap.
> Snapshot **2026-08-24**. **No model was trained, built or benchmarked here** — this is a route map, not measured results.

## 1. Why this board is used for TinyML

| Property | Value | Why it matters |
|---|---|---|
| **8 MB octal PSRAM** | in-package | Model arena + camera framebuffers. The binding constraint on most ESP32 boards |
| **ESP32-S3 vector ISA** | PIE / SIMD | The S3's headline advantage over the original ESP32 for inference |
| Dual-core @ 240 MHz | Xtensa LX7 | Inference on one core, capture/networking on the other |
| **Integrated camera + mic** | on the daughterboard | No wiring needed to get a sensor stream |
| Price | $13.99 | Cheapest credible vision-ML platform |

The ESP32-S3 has **no NPU**. All inference runs on the CPU, accelerated by hand-written vector kernels (ESP-NN). Expect *hundreds of milliseconds* for image classification, not real-time video analytics.

## 2. Three toolchains — pick one

| | **Edge Impulse** | **SSCMA / SenseCraft** | **ESP-DL** |
|---|---|---|---|
| Vendor | Edge Impulse | **Seeed** | Espressif |
| Workflow | Web IDE → Arduino library | Roboflow/Colab → web flasher | C++ / ESP-IDF |
| Best for | Custom models, audio + vision | Vision, fastest path to a working demo | Maximum control |
| Model formats | its own pipeline | TFLite int8 via SenseCraft | TFLite, ONNX-ish |
| Output | `..._inferencing.zip` Arduino lib | flashed model + firmware | IDF component |
| Difficulty | Medium | **Lowest** | Highest |
| Wiki | [`EdgeImpulse.md`](../artifacts/wiki-snapshot/) | [`XIAO_ESP32S3_SSCMA.md`](../artifacts/wiki-snapshot/) | Espressif docs |

**Recommendation:** start with **SSCMA/SenseCraft** if you want a working object detector today (Seeed's own path, web-based flashing, no build environment). Use **Edge Impulse** when you need a custom dataset, audio models, or a portable Arduino library. Use **ESP-DL** only if you are already an ESP-IDF user and need to control memory placement.

## 3. ⚠ The ESP-NN trap — the single most important thing on this page

Edge Impulse's exported Arduino library ships a **generic C fallback** of the ESP-NN kernels, not the ESP32-S3 assembly-optimised versions. Seeed's own tutorial says so:

> "Before we use the downloaded library, we need to **enable the ESP NN Accelerator**. For that, you can download a preliminary version from the project GitHub, unzip it, and **replace the ESP NN folder** with it under `src/edge-impulse-sdk/porting/espressif/ESP-NN`, in your Arduino library folder."

If you skip this, your model still runs — **just several times slower**, with no error and no warning. This is the classic "my TinyML model is too slow on the S3" complaint, and it is a manual patch step buried in a tutorial.

Replacement ESP-NN: <https://github.com/Mjrovai/XIAO-ESP32S3-Sense/blob/main/ESP-NN.zip> (Marcelo Rovai). Note Seeed itself calls this "a preliminary version" — an unversioned ZIP in a third-party repo is a fragile dependency, so record the hash of whatever you use.

> Evidence: **vendor-documented**. The magnitude of the speed-up is **not quantified** by Seeed and was not measured here.

**Status: VERIFIED — the trap is real, and it is not obsolete.**

I checked this directly rather than leaving it as a maybe. Two archives, both retained locally:

| Archive | ESP32-S3 `.c` files | **ESP32-S3 `.S` assembly kernels** |
|---|---:|---:|
| Seeed's shipped Edge Impulse export ([`xiao-esp32s3-fruits-classify-inferencing.zip`](../artifacts/originals/xiao-esp32s3-fruits-classify-inferencing.zip)) | 3 | **0** |
| Mjrovai replacement ([`ESP-NN.zip`](../artifacts/tinyml/ESP-NN.zip)) | — | **19** |

The stock export **does** contain an `ESP-NN` directory with S3-aware C sources (`esp_nn_conv_esp32s3.c`, `esp_nn_depthwise_conv_s8_esp32s3.c`, `esp_nn_esp32s3.h`) — which is exactly why the omission is easy to miss. It looks like S3 support is present.

But it ships **zero hand-written assembly kernels**. The replacement contains **19**, covering the operations that dominate inference time:

```
esp_nn_conv_s8_mult8_1x1_esp32s3.S          esp_nn_fully_connected_s8_esp32s3.S
esp_nn_conv_s16_mult4_1x1_esp32s3.S         esp_nn_max_pool_s8_esp32s3.S
esp_nn_conv_s16_mult8_esp32s3.S             esp_nn_avg_pool_s8_esp32s3.S
esp_nn_depthwise_conv_s8_mult1_3x3_padded_* esp_nn_add_s8_esp32s3.S
esp_nn_depthwise_conv_s16_mult{1,4,8}_*     esp_nn_mul_s8_esp32s3.S
esp_nn_multiply_by_quantized_mult_*         esp_nn_relu_s8_esp32s3.S
```
(19 files: 8 convolution/depthwise, 2 pooling, 2 basic math, 1 fully-connected, 1 activation, 3 common/quantisation, plus variants.)

**Those assembly routines are what actually use the ESP32-S3's PIE/SIMD vector unit.** Without them you fall back to scalar C, and the S3's main advantage over an original ESP32 for ML evaporates — silently, with no warning and no error.

**So: if you export a model from Edge Impulse for this board, replace the ESP-NN folder.** The speed-up is not quantified by any source located, and was not measured here — but the mechanism is now confirmed from the files themselves, not inferred from a commented-out tutorial paragraph.

## 4. Build configuration

Non-negotiable, on top of the [standard camera settings](camera.md#4-why-esp_camera_init-fails):

| Setting | Value |
|---|---|
| **PSRAM** | **OPI PSRAM** — required |
| **Partition Scheme** | **Huge APP (3 MB, no OTA)** — model libraries are large |
| Board | `XIAO_ESP32S3` |
| Camera frame size | **`FRAMESIZE_QVGA`** (320 × 240) |
| `fb_location` | `CAMERA_FB_IN_PSRAM` |

From the Edge Impulse tutorial's own source:

```c
#define EI_CAMERA_RAW_FRAME_BUFFER_COLS  320
#define EI_CAMERA_RAW_FRAME_BUFFER_ROWS  240
#define EI_CAMERA_FRAME_BYTE_SIZE          3     // RGB888
.frame_size  = FRAMESIZE_QVGA,   // "Do not use sizes above QVGA when not JPEG"
.fb_location = CAMERA_FB_IN_PSRAM,
```

**That comment matters.** Above QVGA in a non-JPEG pixel format the DVP data rate outruns what the driver can absorb, so raw-RGB capture for inference is effectively capped at 320 × 240. Models wanting larger inputs must take JPEG frames and decode them — which costs more time than it saves.

A QVGA RGB888 buffer is `320 × 240 × 3` = **230,400 bytes**, `malloc`'d per inference in the reference code. That comes from PSRAM; on internal SRAM it would fail outright.

Typical model input is far smaller again (96 × 96 or 160 × 160), so the pipeline is: capture QVGA → crop/resize → quantise → infer.

## 5. Minimal inference loop (Edge Impulse, Arduino)

```cpp
#include <your-project_inferencing.h>     // exported EI library
#include "edge-impulse-sdk/dsp/image/image.hpp"
#define CAMERA_MODEL_XIAO_ESP32S3
#include "esp_camera.h"

uint8_t *snapshot_buf;

void loop() {
  snapshot_buf = (uint8_t*)malloc(
      EI_CAMERA_RAW_FRAME_BUFFER_COLS *
      EI_CAMERA_RAW_FRAME_BUFFER_ROWS *
      EI_CAMERA_FRAME_BYTE_SIZE);
  if (!snapshot_buf) { ei_printf("ERR: alloc failed\n"); return; }

  ei::signal_t signal;
  signal.total_length = EI_CLASSIFIER_INPUT_WIDTH * EI_CLASSIFIER_INPUT_HEIGHT;
  signal.get_data     = &ei_camera_get_data;

  if (!ei_camera_capture(EI_CLASSIFIER_INPUT_WIDTH,
                         EI_CLASSIFIER_INPUT_HEIGHT, snapshot_buf)) {
    free(snapshot_buf); return;
  }

  ei_impulse_result_t result = { 0 };
  run_classifier(&signal, &result, false);

  ei_printf("DSP: %d ms, Classification: %d ms, Anomaly: %d ms\n",
            result.timing.dsp, result.timing.classification,
            result.timing.anomaly);

#if EI_CLASSIFIER_OBJECT_DETECTION == 1
  for (auto &bb : result.bounding_boxes) {
    if (bb.value == 0) continue;
    ei_printf("  %s (%f) [x:%u y:%u w:%u h:%u]\n",
              bb.label, bb.value, bb.x, bb.y, bb.width, bb.height);
  }
#else
  for (size_t i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++)
    ei_printf("  %s: %.5f\n", ei_classifier_inferencing_categories[i],
              result.classification[i].value);
#endif

  free(snapshot_buf);          // ← every iteration, or you leak PSRAM
}
```

Two failure modes worth naming: **`malloc` without `free`** leaks 230 KB per frame and dies within seconds; and forgetting `esp_camera_fb_return()` inside the capture helper stalls after `fb_count` frames — see [`camera.md` §3](camera.md#3-minimal-working-capture-arduino).

`result.timing` is the free built-in benchmark. Report those numbers rather than guessing.

## 6. Audio models

The same Edge Impulse path handles keyword spotting from the PDM microphone. Wiki: `XIAO_ESP32S3_Keyword_Spotting.md` and `Edgeimpulse/Key_Word_Spotting.md`.

Standard recipe: 1-second windows at **16 kHz**, converted to **MFCC** features (13 × 49 × 1 is the documented shape), then a small CNN.

The microphone constraints apply unchanged — mono, 16-bit, `I2S_NUM_0` only. See [`microphone.md`](microphone.md).

**Audio + vision simultaneously** is not demonstrated by any example located, and would contend for both PSRAM bandwidth and DMA.

## 7. SSCMA / SenseCraft

Seeed's own stack. [`Seeed_Arduino_SSCMA`](../examples/selected/Seeed_Arduino_SSCMA/) v1.0.3 (MIT, depends on ArduinoJson) is vendored here, with examples for `inference`, `inference_i2c`, `inference_spi`, `inference_uart`, `camera_web_server`, `fan_tacking`, `mouse_hand`, `lock_screen`.

Workflow: label in **Roboflow** → train in **Google Colab** → deploy via the **SenseCraft Model Assistant** web tool → the device speaks a documented JSON protocol over serial/I²C/SPI.

The multiple transport examples are the interesting part: SSCMA is designed so the XIAO acts as a **vision co-processor** reporting results to a host MCU, not just a standalone device.

⚠ **Naming confusion:** much SSCMA documentation targets the **Grove Vision AI V2** (Himax WiseEye2), a *different* product with a dedicated NPU. Ensure any tutorial you follow specifies the XIAO ESP32S3 — performance expectations differ enormously between CPU inference and the Himax NPU.

## 8. Performance

**No inference benchmark was located from any source — vendor or community — and none was run here.**

What can be stated:
- The ESP32-S3 has **no NPU**; everything runs on CPU vector kernels.
- **ESP-NN must be manually replaced** (§3) or you lose most of the acceleration.
- Raw capture is capped at QVGA (§4).
- `result.timing.dsp` / `.classification` give you real numbers in three lines of code.

If you benchmark, record: model architecture and input size, quantisation (int8 vs float), whether ESP-NN was patched, CPU frequency, PSRAM mode/speed, and camera frame size. Existing community figures are unusable precisely because none state these.

See [`../performance.md`](../performance.md).

## 9. Worked examples

| Project | What it shows |
|---|---|
| [`on-device-vision-ai`](../examples/selected/on-device-vision-ai/) | Full pipeline — capture, train, quantise, deploy. Best write-up |
| [`Seeed_Arduino_SSCMA`](../examples/selected/Seeed_Arduino_SSCMA/) | Vendor library, 10 transport/application examples |
| `Mjrovai/XIAO-ESP32S3-Sense` | Largest teaching repo; **source of the ESP-NN replacement**. Metadata-only (93 MB) — see [`../examples/best.md`](../examples/best.md) |
| `mpous/xiao-esp32s3-camera-edgeimpulse` | Minimal Edge Impulse + camera |
| `SolomonGithu/tinyml_dog_bark_and_howl_classification` | Audio TinyML on this board |

## 10. Reality check

From [`../projects-and-community.md`](../projects-and-community.md): of 28 showcased XIAO ESP32-S3 projects, **7 are "AI vision" but almost all send images to a cloud LLM** (GPT-4o and similar). Genuine on-device inference is confined to a smaller TinyML cluster.

**Do not read "AI wearable powered by XIAO ESP32S3 Sense" as evidence the board runs the model.** For most headline projects — OpenGlass, WatchThis, the Pokédex — the board is a camera with Wi-Fi. That is a legitimate architecture, but it is a different engineering problem with different latency, privacy and connectivity properties.

On-device inference on this board is real but modest: small classifiers and detectors at QVGA, hundreds of milliseconds per frame

.

## 11. Related
- [`camera.md`](camera.md) — capture configuration this depends on
- [`microphone.md`](microphone.md) — audio input for keyword spotting
- [`../resources-and-conflicts.md`](../resources-and-conflicts.md) — PSRAM and DMA budgets
- [`../performance.md`](../performance.md) · [`../examples/best.md`](../examples/best.md)
