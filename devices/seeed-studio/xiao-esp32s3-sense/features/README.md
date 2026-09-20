# Feature guides — XIAO ESP32S3 Sense

Task-oriented guides. Each answers "how do I use X on this board", with the pin cost, the conflicts, and the version traps.

| Guide | Covers | Headline gotcha |
|---|---|---|
| [`camera.md`](camera.md) | OV2640/3660/5640, DVP, capture, streaming | **No `PWDN`/`RESET`** — cannot reset or power down the sensor |
| [`microphone.md`](microphone.md) | PDM mic, I²S, WAV recording | **`I2S_NUM_0` only, mono, 16-bit only** |
| [`microsd.md`](microsd.md) | SPI card slot, FAT32, filesystems | **CS = GPIO21 = the user LED** |
| [`battery-and-power.md`](battery-and-power.md) | Charging, sleep, runtime, rails | **No battery voltage sense at all** |
| [`wifi-and-bluetooth.md`](wifi-and-bluetooth.md) | Wi-Fi, BLE overview, antenna | **No Bluetooth Classic** — no A2DP/HFP/SPP |
| [`ble.md`](ble.md) | BLE GATT, scanning, NimBLE vs Bluedroid | 250 B MTU — **don't stream images over BLE** |
| [`esp-now.md`](esp-now.md) | Router-free device-to-device messaging | **250-byte payload limit** |
| [`ota-and-storage.md`](ota-and-storage.md) | OTA updates, NVS, SPIFFS, coredump | **3,264 KB app ceiling** — factory image uses 90 % |
| [`usb.md`](usb.md) | Native USB, CDC, UVC, HID, recovery | The **serial port vanishing is normal** |
| [`gpio-adc-and-pwm.md`](gpio-adc-and-pwm.md) | Free pins, ADC, LEDC, I²C, strapping | **GPIO33–37 silently corrupt PSRAM** |
| [`deep-sleep.md`](deep-sleep.md) | Low power, sensor standby, battery bugs | **Vendor sleep figures are unachievable** with the camera |
| [`tinyml.md`](tinyml.md) | On-device inference: SSCMA, Edge Impulse, ESP-DL | **ESP-NN must be patched manually** or you lose the acceleration |

## Cross-cutting constraints

Three facts shape almost every design on this board:

1. **The daughterboard consumes all four JTAG pins** (camera GPIO39/40, mic GPIO41/42). No hardware debugging with sensors attached.
2. **You have ~4 genuinely free GPIOs** (1, 2, 3, 4) once the SD card is in use. Prefer I²C peripherals.
3. **The camera cannot be powered down.** Vendor deep-sleep figures (~34 µA) are **not achievable once the camera is initialised** — owners measure ~90 mA, or ~1.45 mA with the [standby workaround](deep-sleep.md#3-the-workaround--software-standby-via-a-sensor-register).

## Not yet written

Honest gaps — these capabilities exist but have no dedicated guide:


## Related
- [`../README.md`](../README.md) — device overview and the "How do I…?" index
- [`../resources-and-conflicts.md`](../resources-and-conflicts.md) — the simultaneous-use matrix
- [`../pinouts-and-buses.md`](../pinouts-and-buses.md) — the underlying wiring
