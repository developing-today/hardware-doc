# Microphone (PDM) — XIAO ESP32S3 Sense

> The board's second headline feature, and the one with the most version-sensitive code.
> Snapshot **2026-08-24**. No hardware testing — code below is from vendor documentation and inspected projects.

## 1. What it is

A **mono PDM (pulse-density modulation) MEMS microphone** on the detachable Sense daughterboard.

| Property | Value | Evidence |
|---|---|---|
| Interface | **PDM**, 1-bit serial | schematic net names `PDM_CLK` / `PDM_DATA` |
| Clock | **GPIO42** (`MTMS`) → J3 pad 27 | PCB netlist |
| Data | **GPIO41** (`MTDI`) → J3 pad 26 | PCB netlist |
| Channels | **Mono** — one data line | netlist: no second data net crosses J3 |
| Test points | TP2 = CLK, TP3 = DATA | netlist |
| Part number | **MEMSensing `MSM261D3526H1CPM`** | [component record](../../../../components/memsensing/msm261d3526h1cpm/README.md) — from the daughterboard EAGLE BOM |

It is **not** I²S-standard (no `WS`/`LRCLK`) and **not** analogue. The ESP32-S3's I²S peripheral has a dedicated PDM-RX mode with a hardware decimation filter that turns the 1-bit stream into PCM.

Commonly cited online as an **MSM261D3526H1CPM**, but this could not be confirmed from any primary source — Seeed publishes no daughterboard schematic or BOM. See [`gaps-and-conflicts.md` §7](../gaps-and-conflicts.md#7-microphone-part-number-not-established--resolved-2026-08-24).

## 2. Hard constraints

These are **silicon** limits confirmed by Seeed's own documentation, not style preferences:

> "It should be noted that for the current ESP32-S3 chip, we can only use `PDM_MONO_MODE` and the sampling bit width can only be **16 bit**. Only the sampling rate can be modified, but after testing, the sampling rate at **16 kHz** is relatively stable."
> — `XIAO_ESP32S3_Sense_mic.md`

| Constraint | Detail |
|---|---|
| Mode | **`PDM_MONO_MODE` only** — no stereo, no standard I²S RX |
| Bit width | **16-bit only** |
| Sample rate | Adjustable; **16 kHz is the vendor-tested stable value** |
| I²S instance | **`I2S_NUM_0` only** — the ESP32-S3's PDM RX is not available on `I2S_NUM_1` |

**Consequence for audio projects:** if you also want I²S *playback* (a speaker, a DAC), it must use `I2S_NUM_1` on your own GPIOs — and you have only ~8 free pins. Plan the pin budget before committing.

**Consequence for copied code:** sketches that set a channel mask, request stereo, or ask for 24/32-bit will fail or return silence. Much ESP32 I²S microphone code found online targets external I²S mics (INMP441 etc.), which are a *different interface* and will not work here.

## 3. Minimal example — Arduino 3.x (current)

Uses `ESP_I2S.h`. This is the API on Arduino-ESP32 **3.x / ESP-IDF 5.x**.

```cpp
#include <ESP_I2S.h>
I2SClass I2S;

void setup() {
  Serial.begin(115200);
  while (!Serial) ;

  I2S.setPinsPdmRx(42, 41);          // CLK = 42, DATA = 41

  if (!I2S.begin(I2S_MODE_PDM_RX, 16000,
                 I2S_DATA_BIT_WIDTH_16BIT,
                 I2S_SLOT_MODE_MONO)) {
    Serial.println("Failed to initialize I2S!");
    while (1) ;
  }
}

void loop() {
  int sample = I2S.read();
  if (sample && sample != -1 && sample != 1) Serial.println(sample);
}
```

## 4. Minimal example — Arduino 2.x (legacy)

Uses `I2S.h`. **This will not compile on Arduino-ESP32 3.x.**

```cpp
#include <I2S.h>

void setup() {
  Serial.begin(115200);
  while (!Serial) ;

  // setAllPins(bclk, ws/clk, dataIn, dataOut, chanSel)
  I2S.setAllPins(-1, 42, 41, -1, -1);

  if (!I2S.begin(PDM_MONO_MODE, 16000, 16)) {
    Serial.println("Failed to initialize I2S!");
    while (1) ;
  }
}

void loop() {
  int sample = I2S.read();
  if (sample && sample != -1 && sample != 1) Serial.println(sample);
}
```

Note the odd `setAllPins(-1, 42, 41, -1, -1)` signature: in PDM mode the second parameter carries the **PDM clock** and the third the **PDM data**, with the remaining I²S signals unused. This is why the argument order looks wrong compared to standard I²S examples.

### Which API am I on?

| You have | Use |
|---|---|
| `#include <ESP_I2S.h>` compiles | Arduino-ESP32 **3.x** — use §3 |
| `#include <I2S.h>` compiles, `ESP_I2S.h` does not | Arduino-ESP32 **2.x** — use §4 |

**Most community microphone code for this board predates 3.x.** The vendor's factory firmware was itself built with core 2.0.7. If a promising project was last touched before mid-2024, assume it is 2.x.

## 5. Recording to microSD (WAV)

The standard vendor recipe writes a 44-byte WAV header then streams samples. Key parameters from `XIAO_ESP32S3_Sense_mic.md`:

```cpp
#define SAMPLE_RATE      16000U
#define SAMPLE_BITS      16
#define WAV_HEADER_SIZE  44
#define RECORD_TIME      20        // seconds
```

Buffer size is `RECORD_TIME * SAMPLE_RATE * SAMPLE_BITS / 8` — for 20 s at 16 kHz/16-bit that is **640,000 bytes**, which must be allocated in **PSRAM**, not internal SRAM.

**⚠ The SD card and the user LED share GPIO21.** Any `digitalWrite(LED_BUILTIN, …)` during recording asserts the card's chip-select mid-transaction. Do not use the built-in LED as a "recording" indicator — this is the single most likely way to corrupt a recording. See [`microsd.md` §4](microsd.md#4-the-chip-select-collision).

Format the card **FAT32**, ≤ 32 GB.

## 6. Resource cost and conflicts

| Resource | Cost |
|---|---|
| GPIO | 41, 42 (both cross J3) |
| I²S | **`I2S_NUM_0` consumed entirely** |
| DMA | one GDMA channel |
| PSRAM | recording buffers |
| **JTAG** | **GPIO41/42 = `MTDI`/`MTMS`** |

**The microphone permanently costs you half the JTAG port.** Combined with the camera's use of `MTCK`/`MTDO`, the daughterboard consumes all four. Hardware debugging is impossible with the sensor board fitted — see [`../pinouts-and-buses.md` §7.2](../pinouts-and-buses.md#72-the-camera-and-microphone-occupy-all-four-jtag-pins).

| Combination | Status |
|---|---|
| Mic + microSD | ✅ vendor-documented (WAV recorder) — mind the GPIO21 collision |
| Mic + Wi-Fi streaming | ✅ demonstrated by [`esp32-birdnet-mic`](../examples/selected/esp32-birdnet-mic/) |
| Mic + camera | ⚠ works but hard — see [`../examples/best.md` §3](../examples/best.md#3-xiao_sense_camerawebserver_audio) |
| Mic + I²S playback | ⚠ playback must use `I2S_NUM_1` + 3 free GPIOs |
| Mic + JTAG | ❌ impossible |
| Mic + Bluetooth audio (A2DP) | ❌ **impossible** — ESP32-S3 has **BLE only**, no Bluetooth Classic |

That last row catches people out repeatedly: a "Bluetooth microphone" using A2DP/HFP cannot be built on this silicon. See the [ESP32-S3R8 record](../../../../components/espressif/esp32-s3r8/README.md#radio-capabilities-and-the-classic-bluetooth-limitation).

## 7. Troubleshooting

| Symptom | Likely cause |
|---|---|
| `Failed to initialize I2S!` | Wrong API for your core version (§4 vs §3), or `I2S_NUM_1` requested |
| Compiles, returns all zeros / silence | Stereo or non-16-bit requested; or daughterboard not seated |
| Constant `-1` / `1` values | Normal idle artefacts — the vendor examples filter them explicitly |
| Works, then drops out under Wi-Fi | DMA/buffer starvation. Study [`esp32-birdnet-mic`](../examples/selected/esp32-birdnet-mic/), which solves this |
| Recording is noise | Sample rate too high — return to 16 kHz |
| SD writes corrupt during recording | **GPIO21 LED/CS collision** |

## 8. Best reference implementation

[`esp32-birdnet-mic`](../examples/selected/esp32-birdnet-mic/) (MIT, 166★, actively maintained through 2026-08) — continuous PDM capture streamed as **RTSP** while Wi-Fi is active, with OTA and a web UI. It is the only surveyed project that demonstrably solves sustained capture under network load, which is the hard part.

For learning, the vendor's own `XIAO_ESP32S3_Sense_mic.md` (in [`../artifacts/wiki-snapshot/`](../artifacts/wiki-snapshot/)) is the clearest minimal path.

## 9. Related

- [MSM261D3526H1CPM component record](../../../../components/memsensing/msm261d3526h1cpm/README.md)
- [`microsd.md`](microsd.md) — for recording targets
- [`../pinouts-and-buses.md` §4](../pinouts-and-buses.md#4-microphone-pdm) · [`../resources-and-conflicts.md`](../resources-and-conflicts.md) · [`../development.md`](../development.md#the-2x--3x-break)
