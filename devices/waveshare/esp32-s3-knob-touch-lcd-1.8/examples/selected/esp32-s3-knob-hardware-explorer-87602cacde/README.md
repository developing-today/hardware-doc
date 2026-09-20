# ESP32-S3 Knob Hardware Explorer

A PlatformIO test sketch and hardware reference for the
**Waveshare ESP32-S3-Knob-Touch-LCD-1.8** board.

This project verifies and documents every piece of peripheral hardware on
the board — pin assignments, I²C addresses, register quirks, USB-C oddities.
Use it as a starting point for your own projects on this board, or just as
a known-good reference when something doesn't work.

## What this is

`Test App for Waveshare ESP32-Knob` — a single-file Arduino-style sketch
that runs through every peripheral once at boot and prints the result over
USB-CDC serial. No fancy framework, no LVGL yet — just plain hardware
verification.

## Hardware

| Component   | Spec                                          |
|-------------|-----------------------------------------------|
| MCU         | ESP32-S3-WROOM-2 (N16R8, 240 MHz, 16MB/8MB)   |
| Display     | 1.8" round, 360×360, capacitive touch (CST816)|
| Encoder     | Rotary knob (GPIO 7/8)                        |
| Audio       | PCM5100A DAC → 3.5mm jack                     |
| Microphone  | PDM on GPIO 45/46                             |
| Haptics     | DRV2605 LRA (I²C 0x5A)                        |
| Battery     | 800 mAh LiPo (3.7V)                           |

## Verified pin map

| Function              | Pin / Address       | Notes                              |
|-----------------------|---------------------|------------------------------------|
| I²C SDA               | GPIO 11             |                                    |
| I²C SCL               | GPIO 12             |                                    |
| Touch CST816          | I²C 0x15            | reg 0x00, 12-bit coordinates       |
| Vibration DRV2605     | I²C 0x5A            | **LRA motor!** Library 5, reg 0x1D=0xA8 |
| Display backlight     | GPIO 47             |                                    |
| Encoder A             | GPIO 8              |                                    |
| Encoder B             | GPIO 7              | encoder has no push button         |
| Battery ADC           | GPIO 1              | factor ×2, full ≈ 4.3V             |
| PCM5100A enable       | GPIO 0              | (not an encoder button!)           |
| I²S BCLK / WS / DOUT  | GPIO 39 / 40 / 41   | audio DAC → 3.5mm jack             |
| PDM mic CLK / DATA    | GPIO 45 / 46        |                                    |
| Display QSPI          | CS=14, PCLK=13, D0–3=15–18, RST=21 |                       |

## Build / Flash

PlatformIO project — either via VS Code extension or CLI:

```bash
pio run                 # build
pio run -t upload       # flash
pio device monitor      # serial monitor
```

See `platformio.ini` for the full configuration. Custom board JSON for the
N16R8 PSRAM variant lives under `boards/`.

## Stumbling blocks (so you don't hit them too)

### 1. Arduino-ESP32 3.x → use the pioarduino fork

PlatformIO Stable only ships Arduino-ESP32 2.0.17, which is too old for
`ESP_I2S.h` and the new I²S-PDM API. Use the community
[pioarduino fork](https://github.com/pioarduino/platform-espressif32) instead
— it's the de-facto standard in 2025/2026.

### 2. Custom board JSON for N16R8 PSRAM

`board = esp32-s3-devkitc-1` defaults to N8 *without* PSRAM. The settings in
`platformio.ini` are overruled by the board JSON, so you need a custom one.
See `boards/waveshare_knob_18.json` — key fields: `psram_type: opi`,
`memory_type: qio_opi`, `BOARD_HAS_PSRAM`.

### 3. ⚠️ USB-C plug orientation matters

The board has *one* USB-C port, but behind it sits a **CH334 USB hub** with
two devices:

| Device                    | What                          | macOS port            |
|---------------------------|-------------------------------|-----------------------|
| CH343 UART bridge         | companion chip (ESP32-U4WDH)  | `/dev/cu.usbserial-*` |
| Native ESP32-S3 USB-OTG   | our target MCU                | `/dev/cu.usbmodem*`   |

**Which one is active depends on the plug orientation.**

- Wrong way → only `usbserial-*` shows up, esptool says
  *"This chip is ESP32, not ESP32-S3"* (it's talking to the companion chip
  via UART bridge!)
- Right way → `usbmodem` appears, everything works

**Rule of thumb: on a `wrong chip` error, flip the plug first — don't
touch your config.**

### 4. `printf` vs `Serial.printf` with USB-CDC

With `USB_CDC_ON_BOOT=1`, `Serial` becomes USB-CDC, but plain `printf()`
does *not* — it's the ESP-IDF C library and still writes to UART0. Symptom:
serial monitor connects, says "Connected!", then silence.

One-line fix in `setup()`:

```cpp
ets_install_putc1([](char c) { Serial.write((uint8_t)c); });
```

That reroutes every `printf` byte to USB-CDC.

## Sources & related projects

- Waveshare wiki: <https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8>
- [muness/roon-knob](https://github.com/muness/roon-knob) — HiFi controller, dual-chip architecture explained, AVRCP
- [KrX3D/WaveShare-Knob-Esp32S3](https://github.com/KrX3D/WaveShare-Knob-Esp32S3) — ESPHome config
- [nkinnan/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8...](https://github.com/nkinnan/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8_and_Guition-K5-Knob-Series-JC3636K518) — full ESPHome config
- [Tasmota discussion #23737](https://github.com/arendst/Tasmota/discussions/23737) — ST77916 display init, CST816 touch
- [pioarduino versions list](https://github.com/sivar2311/platform-espressif32-versions)

## Tested

| Test                   | Result                                          |
|------------------------|-------------------------------------------------|
| I²C scan               | finds CST816 (0x15) + DRV2605 (0x5A) ✅          |
| Battery ADC            | reads ~4.3V healthy ✅                           |
| Backlight (GPIO 47)    | blinks 3× ✅                                     |
| DRV2605 LRA            | strong-click + 1s full amplitude ✅              |
| Encoder (GPIO 7+8)     | reacts to rotation ✅                            |
| Touch CST816           | reacts to taps ✅                                |
| WiFi scan              | lists nearby networks ✅                         |
| PCM5100A audio DAC     | plays 440 Hz sine via I²S ✅                     |
| PDM microphone         | reads peak / RMS samples ✅                      |

## License

MIT — see [LICENSE](LICENSE).

## Author

Ingo Hoffmann · [@SuperEugen](https://github.com/SuperEugen) · Berlin
