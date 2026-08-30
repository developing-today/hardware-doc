# Resources and conflicts — XIAO ESP32S3 Sense

> Who owns which GPIO, bus, timer, DMA channel and rail — and what breaks when features run together.
> Snapshot **2026-08-24**. Limits are labelled **silicon** / **board** / **framework** / **observed**. Nothing here was measured on hardware.

## 1. GPIO budget

The ESP32-S3 has 45 GPIOs. On this board you get **11**.

| Disposition | Count | GPIOs |
|---|---:|---|
| User header | **11** | 1, 2, 3, 4, 5, 6, 7, 8, 9, 43, 44 |
| Consumed by the Sense daughterboard | 16 | 10–18, 21, 38, 39, 40, 41, 42, 47, 48 |
| Native USB | 2 | 19, 20 |
| SPI flash (dedicated pins) | — | `SPICLK/Q/D/HD/WP/CS0` |
| **No-connect — in-package PSRAM** | 5 | **33, 34, 35, 36, 37** (+ `SPICS1`) |
| No-connect — strapping | 2 | 45, 46 |

**Three of the eleven "free" pins are not really free** if you use the daughterboard: GPIO7/8/9 (`D8`/`D9`/`D10`) are the microSD SPI bus. Using them as GPIO while a card is mounted corrupts transfers.

So the honest free-pin count with the Sense board attached and the SD card in use is **eight**: GPIO1–6, 43, 44 — and two of those are the UART.

## 2. Bus ownership

| Bus | Pins | Owner | Shareable? |
|---|---|---|---|
| I²C (`Wire`) | GPIO5 SDA / GPIO6 SCL | user | ✅ — the only genuinely free bus. No on-board devices |
| **SCCB** (camera control) | GPIO40 SDA / GPIO39 SCL | `esp32-camera` | ❌ — separate from `Wire`; driver assumes exclusive ownership |
| SPI | GPIO7 SCK / GPIO8 MISO / GPIO9 MOSI | shared: microSD + user | ⚠ — shareable with **distinct CS pins**, but SD CS is GPIO21 |
| UART0 | GPIO43 TX / GPIO44 RX | user / console | ⚠ — console by default unless USB CDC is on |
| DVP (camera data) | GPIO10–18, 13, 38, 47, 48 | `esp32-camera` | ❌ |
| I²S PDM RX | GPIO42 CLK / GPIO41 DATA | microphone | ❌ |
| USB | GPIO19/20 | native USB | ❌ |
| QSPI flash | dedicated | ROM/bootloader | ❌ |

**Scanning `Wire` will never find the camera.** It is on GPIO39/40, not GPIO5/6.

## 3. Peripheral instance budget

| Resource | Total (silicon) | Used by the board | Left for you |
|---|---:|---|---|
| I²S | 2 (`I2S_NUM_0`, `I2S_NUM_1`) | **`I2S_NUM_0`** — PDM RX **only works on instance 0** | `I2S_NUM_1` — but it **cannot do PDM** |
| LEDC channels | 8 low-speed | 1 (camera `XCLK`, conventionally `LEDC_CHANNEL_0`) | 7 |
| LEDC timers | 4 | 1 (`LEDC_TIMER_0`) | 3 |
| GDMA channels | 5 in / 5 out | camera (1), I²S (1), SPI/SD (1), Wi-Fi | tight under full load |
| ADC1 channels | 10 | 0 | **9 exposed** (`A0`–`A5`, `A8`–`A10`) |
| ADC2 | — | 0 | **not exposed on this board** |
| RMT / PCNT / MCPWM / TWAI | full | 0 | all available — but pin-limited |

**The I²S constraint is a real design boundary.** ESP32-S3 PDM RX is `I2S_NUM_0`-only (**silicon** limit). If you want to record from the microphone *and* play audio over I²S, playback must use `I2S_NUM_1` on your own pins — and you have 8 free GPIOs to find 3 of them from.

**LEDC:** the camera takes channel 0 / timer 0 by convention. If you drive servos or LEDs with `ledcWrite`, start at channel 1 or you will disturb `XCLK` and get corrupted frames.

## 4. Memory

| Resource | Size | Notes |
|---|---|---|
| Internal SRAM | 512 KB | Shared with Wi-Fi/BLE stacks |
| **PSRAM** | **8 MB octal**, in-package | Camera framebuffers. Must be configured **OPI**, not QSPI |
| Flash | 8 MB external | Fully partitioned; **app slot 3,264 KB** |

**Application size ceiling is 3,264 KB** with the stock `8MB with spiffs` scheme. The factory `CameraWebServer.bin` is 2,941,584 B — **90 % of the slot**. Adding to it overflows. Switching to a no-OTA scheme frees the `app1` slot.

⚠ **Octal PSRAM at 120 MHz is temperature-fragile** on the ESP32-S3 — see the [ESP-IDF peripheral guide](../../../guides/espressif/esp-idf-peripheral-capabilities.md#43-esp32-s3--120-mhz-octal-psram-is-temperature-fragile). Use 80 MHz. Given this board's known thermal behaviour under camera load (~53.5 °C with heat sinks), this is not theoretical.

## 5. Power budget

| Rail | Limit | Consumers |
|---|---|---|
| `VCC_3V3` | **600 mA** (SGM6029) | SoC (peak ~350 mA with Wi-Fi TX), flash, camera (98–140 mA), microphone, microSD (~100 mA peak on write) |
| `VBUS` (5 V pin) | USB host | **0 V when running on battery** |
| Charge | ~110 mA | R10-programmed |

Adding up the worst case — Wi-Fi TX burst + OV5640 (140 mA) + SD write burst — the 600 mA rail is **not comfortably oversized**. Peripherals you add on the header share what remains. The vendor's own webcam figure (peak ~366 mA at 3.8 V) is consistent with meaningful headroom in normal operation but little margin for a hungry add-on.

## 6. Simultaneous-feature matrix

| Combination | Verdict | Mechanism |
|---|---|---|
| Camera + Wi-Fi | ✅ well trodden | The default use case. Bandwidth-bound, not pin-bound |
| Camera + microSD | ⚠ **works with care** | **SD `CS` = GPIO21 = user LED.** Never drive `LED_BUILTIN` while mounted |
| Camera + microphone | ⚠ **hard but done** | No pin conflict, but PSRAM/DMA/Wi-Fi contention. One good example exists |
| Camera + mic + SD + Wi-Fi | ⚠ **untested here** | All four together stress DMA and the 3V3 rail. No verified example located |
| Camera + JTAG | ❌ **impossible** | Camera owns `MTCK`/`MTDO` |
| Microphone + JTAG | ❌ **impossible** | Mic owns `MTDI`/`MTMS` |
| Microphone + I²S playback | ⚠ | PDM RX is `I2S_NUM_0`-only; playback must use `I2S_NUM_1` + 3 free GPIOs |
| SD + user SPI peripheral | ✅ | Share the bus, use a distinct CS on GPIO1–4 |
| Camera + deep sleep | ⚠ **badly compromised** | Camera cannot be powered down. Measured ~90 mA after a capture; ~1.45 mA with the OV3660 standby trick — **not** the ~34 µA the wiki implies |
| ADC + Wi-Fi | ✅ | All exposed ADC pins are **ADC1**. The usual ADC2/Wi-Fi conflict does not apply here |
| Wi-Fi + BLE | ⚠ | Coexistence works; the factory binary contains the string *"Should enable WiFi modem sleep when both WiFi and Bluetooth are enabled"* |

## 7. The two conflicts that actually bite

**GPIO21 is both `LED_BUILTIN` and the microSD chip-select.** Not a routing coincidence you can work around — the same net. Symptoms: mount succeeds once then never again; corrupted writes; SD activity visibly flickering the "status" LED. **Rule: in any sketch that touches the SD card, do not use `LED_BUILTIN`.** Use GPIO1–4 for an external indicator.

**The daughterboard consumes all four JTAG pins.** GPIO39/40 (camera SCCB) + GPIO41/42 (PDM mic) = `MTCK`/`MTDO`/`MTDI`/`MTMS`. Debug the board bare, or use `ESP_LOG` and the 64 KB `coredump` partition. This is a **board** limit that cannot be lifted in software.

A third, quieter one: **`pins_arduino.h` sets `SS = 44`** (GPIO44 = `D7`/`RX`), which has nothing to do with the SD card. Code relying on the default `SS` toggles the UART RX pin. Always pass CS explicitly.

## 8. Related
- [`pinouts-and-buses.md`](pinouts-and-buses.md) — the full pin map and conflict detail
- [`bom-and-board-construction.md`](bom-and-board-construction.md) — what is fitted
- [`features/camera.md`](features/camera.md) · [`development.md`](development.md) · [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
