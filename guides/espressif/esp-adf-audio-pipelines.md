# ESP-ADF audio pipelines, Bluetooth audio and the audio memory budget

- **Purpose:** the architectural and budgetary facts from the ESP-ADF Programming Guide that bear on the **Classic Bluetooth audio path on the [ESP32-U4WDH](../../components/espressif/esp32-u4wdh/README.md)**, extracted before the 25.7 MB PDF was archived.
- **Extracted:** 2026-08-24

## Source

| Key | Document | Build | Pages | Regenerate from |
|---|---|---|---|---|
| **ADF** | *Espressif Audio Development Framework Guide*, Release `latest` (master) | dated **Jul 31, 2026**; PDF `CreationDate` 2026-07-30, server `Last-Modified` 2026-07-31 | 495 | `https://docs.espressif.com/projects/esp-adf/en/latest/esp-adf-en-master.pdf` |

Archive record, SHA-256 and URL verification: [`components/espressif/esp32-u4wdh/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md`](../../components/espressif/esp32-u4wdh/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md).

> **Moving-target caveat.** This is a `master`/`latest` build, not a versioned release. The URL above always serves the *current* master build; it will not reproduce this exact file indefinitely. At the time of archiving it served a byte-identical file (25 732 191 bytes). Page numbers below are for **this** build.

---

## 1. Which chips ESP-ADF actually targets

> "For easier start with ESP-ADF, Espressif designed **ESP32, ESP32-S2, and ESP32-S3** based development boards…"
> — ADF § 1.1 *Development Board Overview*

> "The ESP chips (including **ESP32, ESP32-S2, ESP32-S3**) have all the above features or are able to support them…"
> — ADF § 3.1.1 *Project Options*, p. 330

**There is no ESP32-P4 support in ESP-ADF**, and no P4 board in its Development Boards chapter. The board list is: ESP32-LyraT V4.3/V4.2/V4, ESP32-LyraT-Mini V1.2, ESP32-LyraTD-MSC V2.2, ESP32-Korvo-DU1906, ESP32-S2-Kaluga-1, ESP32-S3-Korvo-2 V3.0/V3.1, ESP32-S3-Korvo-2-LCD V1.0, ESP32-C3-Lyra V2.0 (§ 3.3, pp. 334–435).

This matters for this knowledge base: **ADF is stored under the ESP32-U4WDH record, not the ESP32-S3R8 record, because the A2DP elements require BR/EDR and only the original ESP32 has it.** See [ESP32-S3R8 § Classic Bluetooth limitation](../../components/espressif/esp32-s3r8/README.md#radio-capabilities-and-the-classic-bluetooth-limitation).

---

## 2. The architecture: Element → Pipeline → Ringbuffer

### 2.1 Audio Element

> "The basic building block for the application programmer developing with ADF is the **`audio_element`** object. **Every decoder, encoder, filter, input stream, or output stream is in fact an Audio Element.** … The general functionality of an Element is to take some data on input, process it, and output to the next. **Each Element is run as a separate task.**"
> — ADF § 2.1.1 *Audio Element*, p. 16

Elements expose **seven callbacks**, declared in `audio_element_cfg_t`:

`open` · `seek` · `process` · `close` · `destroy` · `read` · `write`

> "Particular Elements typically use a subset of all available callbacks. For instance the MP3 Decoder is using **open, process, close and destroy**."
> — same page

Header: `components/audio_pipeline/include/audio_element.h`. Element types are enumerated by `audio_element_type_t` in `audio_common.h`.

### 2.2 Audio Pipeline

> "Dynamic combination of a group of linked Elements is done using the Audio Pipeline. You do not deal with the individual elements but with just one audio pipeline. **Every element is connected by a ringbuffer.** The Audio Pipeline also takes care of forwarding messages from the element tasks to an application."
> — ADF § 2.1.2 *Audio Pipeline*, p. 37

Header: `components/audio_pipeline/include/audio_pipeline.h`. Lifecycle API: `audio_pipeline_init()` / `_link()` / `_unlink()` / `_run()` / `_pause()` / `_resume()` / `_stop()` / `_wait_for_stop()` / `_wait_for_stop_with_ticks()` / `_terminate()` / `_terminate_with_ticks()` / `_reset_ringbuffer()` / `_reset_elements()` / `_deinit()`. Event plumbing: `audio_pipeline_set_listener()`, `_remove_listener()`, `_get_event_iface()`.

**Design consequence:** every element costs a FreeRTOS task *and* a ringbuffer. A three-element pipeline is three tasks plus two ringbuffers. This is the dominant term in the memory budget in § 5.

### 2.3 The canonical pipelines

| Example | Element graph |
|---|---|
| `get-started/play_mp3_control` | MP3 decoder → I2S stream |
| `player/pipeline_http_mp3` | HTTP reader stream → MP3 decoder → I2S writer stream |
| **Bluetooth A2DP sink** | `bluetooth_service` → `a2dp_stream` → decoder → `i2s_stream_writer` |

---

## 3. Bluetooth audio — the U4WDH path

### 3.1 Profiles provided

> "The Bluetooth service is dedicated to interface with Bluetooth devices and provides support for the following protocols:
> - **HFP (Hands-Free Profile)**: remotely controlling the mobile phone by the Hands-Free device and the voice connection…
> - **A2DP (Advanced Audio Distribution Profile)**: implementing streaming of multimedia audio using a Bluetooth…
> - **AVRCP (Audio Video Remote Control Profile)**: used together with A2DP for remote control of devices…"
> — ADF § 2.6.1 *Bluetooth Service*, p. 149

All three are **BR/EDR** profiles. This is precisely the set the ESP32-S3 cannot provide and the reason the knob board carries a second MCU.

### 3.2 API entry points

Headers:
- `components/bluetooth_service/include/bluetooth_service.h`
- `components/bluetooth_service/include/a2dp_stream.h` (p. 153)
- `components/bluetooth_service/include/hfp_stream.h` (p. 153)

| Function | Behaviour |
|---|---|
| `bluetooth_service_start(bluetooth_service_cfg_t *config)` | "Initialize and start the Bluetooth service. **This function can only be called for one time**" |
| `bluetooth_service_create_stream()` | "Create Bluetooth stream, it is valid when Bluetooth service has started." Returns an `audio_element_handle_t` — i.e. Bluetooth appears in the pipeline as an ordinary Element |
| `bluetooth_service_create_periph()` | Returns an `esp_periph_handle_t` for the peripheral/event side |
| `bluetooth_service_destroy()` | Tear-down |

**AVRCP passthrough commands** are exposed as peripheral calls (pp. 149–150), each documented as "Send the AVRC passthrough command (X) to the Bluetooth device":

`periph_bluetooth_play` · `_pause` · `_stop` · `_next` · `_prev` · `_rewind` · `_fast_forward` · `_discover` · `_cancel_discover` · `_connect`

`periph_bluetooth_discover()` documents `ESP_ERR_INVALID_STATE: if bluetooth stack is not yet enabled`.

This is the API surface behind the knob board's "AVRCP knob" behaviour: a rotary/press gesture maps onto `periph_bluetooth_next` / `_prev` / `_play`.

### 3.3 Media source and URI conventions

- `MEDIA_SRC_TYPE_MUSIC_A2DP` — enumerator in the media-source type list (p. 56)
- HFP streams are addressed by URI, e.g. `"hfp://8000:1@bt/hfp/stream.pcm"` (p. 59) — note **8 kHz, 1 channel**, i.e. narrowband voice, as opposed to A2DP's stereo music path

---

## 4. Codec / DAC integration

### 4.1 The `audio_hal` abstraction

> "…to e.g. initialize the audio board, `audio_hal_init()`, control the volume, `audio_hal_get_volume()` and `audio_hal_set_volume()`."
> — ADF § 2.9 *Abstraction Layer*, p. 243

Header: `components/audio_hal/include/audio_hal.h`.

| Function | Notes |
|---|---|
| `audio_hal_init(audio_hal_codec_config_t *conf, audio_hal_func_t *func)` | "**If selected codec has already been installed, it'll return the `audio_hal` handle.**" `func` is "Structure containing functions used to operate audio the codec chip" — i.e. codec drivers are vtables |
| `audio_hal_ctrl_codec(handle, mode, ctrl)` | Start/stop a given `audio_hal_codec_mode_t` |
| `audio_hal_deinit()`, `audio_hal_set_volume()`, `audio_hal_get_volume()` | |

### 4.2 Codec chips with in-tree drivers

Counted by occurrence across the guide: **ES8388** (dominant, on the LyraT boards), **ES8374**, **ES8311**, **ES8389**, **ES8156**, **ES7210**, **ES7243**, **ES7148**, **ZL38063**, **TAS5805M**.

> **Relevant gap:** the **PCM5100A** DAC fitted on the Waveshare knob board has **no ESP-ADF `audio_hal` driver**. That is expected — the PCM5100A is a hardware-configured I²S DAC with no control bus, so there is nothing for an `audio_hal` vtable to do; you drive it with a plain `i2s_stream_writer` and control volume in software or upstream. See [PCM5100A component record](../../components/texas-instruments/pcm5100a/README.md) and [ESP32-U4WDH § 9 shared-resource arbitration](../../components/espressif/esp32-u4wdh/README.md#9-shared-resource-arbitration-the-pcm5100a-dac).

### 4.3 Minimum vs typical project topologies

> "- **Minimum** — having minimum additional components, assuming using on board I2S, or PDM interface as well as **DAC**, if no high quality audio on the output is required.
> - **Typical** — with an **external codec chip and a power amplifier**, for high quality output audio and multiple input / output options."
> — ADF § 3.1.1 *Project Options*, p. 330

---

## 5. The audio memory budget — the most useful table in the document

> "The spare internal Data-RAM is about **290 kB** with 'hello_world' example. For audio system this may be insufficient, and therefore the ESP32 incorporates the ability to use up to **4 MB** of external SPI RAM (i.e. PSRAM)…"
> — ADF § 3.2.1 *Memory*, p. 332

> ⚠ "**Bluetooth and Wi-Fi can not coexist without PSRAM** because it will not leave enough memory for an audio application."
> — ADF § 3.2.1, p. 332

### 5.1 Component memory-usage table

Reproduced from ADF § 3.2.1 *Memory Usage by Component Overview*, p. 333. Baseline: "The initial spare internal RAM is 290 kB."

| Component | Internal RAM required, **PSRAM not used** | Internal RAM required, **with PSRAM** |
|---|---|---|
| Wi-Fi | 50 kB+ | 50 kB+ |
| **Bluetooth** | **140 kB** (50 kB if only BLE needed) | **95 kB** (50 kB if only BLE needed) |
| Flash Card | 12 kB+ | 12 kB+ |
| I2S | Configurable, 8 kB for reference | Configurable, 8 kB for reference |
| RingBuffer | Configurable, 30 kB for reference | **0 kB — all moved into PSRAM** |

**Reading this for the U4WDH:** Classic Bluetooth alone costs **140 kB of 290 kB** without PSRAM. Add I2S (8 kB) and ringbuffers (30 kB) and an A2DP-sink pipeline occupies roughly 178 kB of the 290 kB budget before any application code. The U4WDH has **no PSRAM** (it is a 4 MB-embedded-flash part, `U4WDH` = 4 MB flash, no PSRAM), so the "PSRAM not used" column is the operative one and the RingBuffer 30 kB cannot be offloaded. This is a concrete argument that the U4WDH's role on the knob board is necessarily *narrow* — a BT-audio-and-AVRCP appliance, not a general application processor.

### 5.2 Internal-RAM optimisation rules

From ADF § 3.2.1 *Optimization of Internal RAM and Use of PSRAM*, p. 333:

- If PSRAM is in use, set all Wi-Fi **static** buffers to minimum; if PSRAM is *not* used, select **dynamic** buffers instead.
- If PSRAM **and** BT are used, set `CONFIG_BT_ALLOCATION_FROM_SPIRAM_FIRST` and `CONFIG_BT_BLE_DYNAMIC_ENV_MEMORY` to *yes* — "to allocate more of **40 kB** memory to PSRAM".
- If PSRAM **and** Wi-Fi are used, set `CONFIG_WIFI_LWIP_ALLOCATION_FROM_SPIRAM_FIRST` to *yes*.
- Set `CONFIG_WL_SECTOR_SIZE` to **512** (wear levelling). Note: "The smaller the size of sector be, the slower the Write / Read speed will be… **only 512 and 4096 are supported.**"
- Allocate explicitly rather than relying on `malloc()`:
  ```c
  char *buf = heap_caps_malloc(1024 * 10, MALLOC_CAP_SPIRAM   | MALLOC_CAP_8BIT); // PSRAM
  char *buf = heap_caps_malloc(512,       MALLOC_CAP_INTERNAL | MALLOC_CAP_8BIT); // internal
  ```
- ⚠ "**The task stack will always be allocated at internal RAM.**" `xTaskCreateStatic()` can place a stack in PSRAM, but:

> "**Don't use ROM code in `xTaskCreateStatic` task.** … you also need to consider other pieces of code that call ROM functions, as well as the code that is not recompiled against the `CONFIG_SPIRAM_CACHE_WORKAROUND` patch, **like the Wi-Fi and Bluetooth libraries**. In general, we advise using this only in threads that do not call any IDF libraries (including libc), doing only calculations and using FreeRTOS primitives to talk to other threads."
> — ADF § 3.2.1, p. 333

Also: `CONFIG_SPIRAM_CACHE_WORKAROUND` "should be kept enabled" (p. 332) — it is on by default.

### 5.3 Recommended system settings

ADF § 3.2.2 *System Settings*, p. 334 — "recommended to achieve a high Wi-Fi performance in an audio project":

| Setting | Value |
|---|---|
| Flash SPI mode | **QIO** |
| Flash SPI speed | **80 MHz** |
| CPU frequency | **240 MHz** |
| LWIP → TCP → Default receive window size | **5 × Maximum Segment Size** |
| If external antenna | change `PHY_RF_CAL_PARTIAL` to `PHY_RF_CAL_FULL` in `esp-idf/components/esp32/phy_init.c` |

---

## 6. Stream and codec element inventory

Useful when deciding whether ADF already has an element rather than writing one. All under `components/audio_stream/include/` unless noted.

| Stream element | Header | ADF § |
|---|---|---|
| Algorithm (AEC/AGC/NS front-end) | `algorithm_stream.h` | 2.2.1 |
| FatFs | `fatfs_stream.h` | 2.2.2 |
| HTTP | `http_stream.h` | 2.2.3 |
| **I2S** | `i2s_stream.h` | 2.2.4 |
| PWM | `pwm_stream.h` | 2.2.5 |
| Raw | `raw_stream.h` | 2.2.6 |
| SPIFFS | `spiffs_stream.h` | 2.2.7 |
| TCP client | `tcp_client_stream.h` | 2.2.8 |
| Tone | `tone_stream.h` | 2.2.9 |
| Flash-embedding | `embed_flash_stream.h` | 2.2.10 |
| TTS | `tts_stream.h` | 2.2.11 |
| **A2DP** | `bluetooth_service/include/a2dp_stream.h` | 2.6.1 |
| **HFP** | `bluetooth_service/include/hfp_stream.h` | 2.6.1 |

Each has a `*_CFG_DEFAULT()` macro. `i2s_stream.h` additionally provides `I2S_STREAM_CFG_DEFAULT_WITH_PARA(port, rate, bits, stream_type)` and `I2S_STREAM_CFG_DEFAULT_WITH_TYLE_AND_CH(port, rate, bits, stream_type, channel)` (*sic* — the typo is Espressif's).

**Codec elements** (ADF § 2.4, pp. 119–134): AAC decoder · AMR decoder **and encoder** · FLAC decoder · MP3 decoder · OGG decoder · OPUS decoder · WAV decoder **and encoder**. Note only AMR and WAV have encoders in-tree.

**Other subsystems:** Playlist (§ 2.3), Audio Processing — including downmix (§ 2.5), Services (§ 2.6, including the **Input Key Service** which "provides GPIO input interrupts and **ADC key** functions in the form of events", p. 154), Speech Recognition (§ 2.7), Peripherals (§ 2.8).

---

## 7. Related records

- [ESP32-U4WDH component record](../../components/espressif/esp32-u4wdh/README.md) — the chip this framework targets on the knob board
- [ESP32-S3R8 component record](../../components/espressif/esp32-s3r8/README.md) — why it *cannot* run the A2DP path
- [PCM5100A DAC](../../components/texas-instruments/pcm5100a/README.md)
- [ESP-IDF peripheral capabilities](esp-idf-peripheral-capabilities.md) — I2S and PSRAM constraints referenced above
- [Espressif vendor documentation-sourcing guide](../../vendors/espressif/README.md)
