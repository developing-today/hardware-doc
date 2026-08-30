# Feature coverage — XIAO ESP32S3 Sense

> Every advertised or fitted capability, mapped to hardware evidence, documentation and test status.
> Snapshot **2026-08-24**. **No hardware was available**, so no row reaches "hardware-tested".

Legend — evidence: **P** primary design data (netlist/datasheet) · **V** vendor documentation · **C** community report · **I** inferred.
Test status: `built` / `hw-tested` / `community-reported` / `not-tested`.

| Feature | Hardware | Guide | Official docs | Community example | Evidence | Test | Gaps |
|---|---|---|---|---|---|---|---|
| **Camera (DVP)** | [OV3660](../../../components/omnivision/ov3660/README.md) / [OV2640](../../../components/omnivision/ov2640/README.md) / [OV5640](../../../components/omnivision/ov5640/README.md) via [J3](../../../components/hirose/df40c-30dp-0.4v/README.md) | [`camera.md`](features/camera.md) | ✅ wiki + `camera_pins.h` | ✅ [vendor repo](examples/selected/SeeedStudio-XIAO-ESP32S3-Sense-camera/) | **P+V** | `not-tested` | Frame-rate limits unmeasured |
| **PDM microphone** | [MSM261D3526H1CPM](../../../components/memsensing/msm261d3526h1cpm/README.md) | [`microphone.md`](features/microphone.md) | ✅ wiki | ✅ [`esp32-birdnet-mic`](examples/selected/esp32-birdnet-mic/) | **P+V** | `not-tested` | Part **identified** from the daughterboard BOM; SNR/sensitivity still unknown |
| **microSD (SPI)** | slot on daughterboard | [`microsd.md`](features/microsd.md) | ✅ wiki | ✅ vendor repo | **P+V** | `not-tested` | **Throughput unmeasured**; CS pin contradicted in wiki |
| **Wi-Fi 2.4 GHz** | [ESP32-S3R8](../../../components/espressif/esp32-s3r8/README.md) + U.FL | [`wifi-and-bluetooth.md`](features/wifi-and-bluetooth.md) | ✅ | ✅ many | **P+V** | `not-tested` | **No throughput benchmark run** |
| **BLE 5.0** | ESP32-S3R8 | [`ble.md`](features/ble.md) | ✅ Espressif + Seeed | ⚠ **none selected** | **P+V** | `not-tested` | No vendored BLE example exists |
| **Bluetooth Classic** | — | documented as absent | ✅ | — | **P** | n/a | **Not present in silicon** |
| **USB CDC / flashing** | native USB | [`usb.md`](features/usb.md) | ✅ | ✅ | **P+V** | `not-tested` | — |
| **USB UVC (webcam)** | native USB | [`usb.md`](features/usb.md) | ❌ none | ✅ [`XIAO_Webcam`](examples/selected/XIAO_Webcam/) | **P+C** | `not-tested` | Undocumented by vendor |
| **USB HID / MSC** | native USB | [`usb.md`](features/usb.md#hid-and-msc-in-practice) | ❌ | ❌ | **I** | `not-tested` | Arduino TinyUSB API exists; no example located |
| **GPIO / PWM (LEDC)** | 11 pins | [`gpio-adc-and-pwm.md`](features/gpio-adc-and-pwm.md) | ✅ | ✅ | **P+V** | `not-tested` | — |
| **ADC (ADC1 ×9)** | GPIO1–9 | [`gpio-adc-and-pwm.md`](features/gpio-adc-and-pwm.md) | ✅ | ✅ | **P+V** | `not-tested` | Accuracy/linearity unmeasured |
| **I²C** | GPIO5/6, no devices fitted | [`gpio-adc-and-pwm.md`](features/gpio-adc-and-pwm.md) | ✅ | ✅ | **P** | `not-tested` | — |
| **UART0** | GPIO43/44 | [`gpio-adc-and-pwm.md`](features/gpio-adc-and-pwm.md) | ✅ | ✅ | **P** | `not-tested` | — |
| **SPI (user)** | GPIO7/8/9, shared with SD | [`microsd.md`](features/microsd.md) | ✅ | ✅ | **P+V** | `not-tested` | — |
| **Battery charging** | [SGM40567](../../../components/sgmicro/sgm40567/README.md) | [`battery-and-power.md`](features/battery-and-power.md) | ✅ | ✅ | **P+V** | `not-tested` | **Current disputed 100 vs 110 mA** |
| **Battery voltage sense** | **not fitted** | [`battery-and-power.md`](features/battery-and-power.md#4-you-cannot-read-the-battery-voltage) | ✅ (documented absent) | — | **P+V** | n/a | **Capability absent by design** |
| **Deep sleep** | ESP32-S3R8 | [`deep-sleep.md`](features/deep-sleep.md) | ⚠ **3 contradictory figures** | ✅ forum measurements | **V+C** | `community-measured` | **Vendor figures unachievable with camera; see [`performance.md`](performance.md)** |
| **PSRAM (8 MB octal)** | in-package | [`../resources-and-conflicts.md`](resources-and-conflicts.md#4-memory) | ✅ | ✅ | **P+V** | `not-tested` | Bandwidth unmeasured |
| **User LED** | GPIO21 (active-low) | [`gpio-adc-and-pwm.md`](features/gpio-adc-and-pwm.md) | ✅ | ✅ | **P+V** | `not-tested` | **Shared with SD CS** |
| **Charge LED** | `NCHG` | [`battery-and-power.md`](features/battery-and-power.md#3-charging) | ✅ | ✅ | **P+V** | `not-tested` | — |
| **BOOT / RESET buttons** | K2 / K1 | [`../development.md`](development.md#5-usb-serial-and-recovery) | ✅ | ✅ | **P+V** | `not-tested` | — |
| **On-device ML** | ESP32-S3 vector ISA | [`tinyml.md`](features/tinyml.md) | ✅ SSCMA | ✅ [SSCMA](examples/selected/Seeed_Arduino_SSCMA/), [vision-ai](examples/selected/on-device-vision-ai/) | **V+C** | `not-tested` | ESP-NN patch step; no benchmark exists |
| **JTAG debugging** | **conflicts with daughterboard** | [`../pinouts-and-buses.md`](pinouts-and-buses.md#72-the-camera-and-microphone-occupy-all-four-jtag-pins) | ❌ conflict undocumented | — | **P** | n/a | **Unavailable with sensors attached** |
| **OTA update** | `app0`/`app1` partitions | [`ota-and-storage.md`](features/ota-and-storage.md) | ⚠ generic | ✅ birdnet-mic | **P+C** | `not-tested` | 3,264 KB app ceiling |
| **SPIFFS / NVS** | flash partitions | [`ota-and-storage.md`](features/ota-and-storage.md#4-the-other-storage-options) | ✅ | ✅ | **P+V** | `not-tested` | Summary only |
| **ESP-NOW** | ESP32-S3R8 | [`esp-now.md`](features/esp-now.md) | ✅ Seeed tutorial | ❌ | **V** | `not-tested` | No community example |
| **LoRa (via Wio-SX1262)** | B2B — **conflicts with camera** | ⚠ noted in [`community.md`](community.md#3-the-use-case-the-vendor-catalogue-understates-lora-mesh) | ✅ (Plus only) | ✅ many (r/meshtastic) | **V+C** | `not-tested` | **Not usable with the Sense daughterboard** |

## Summary

- **28 capabilities tracked**, covered by **13 feature guides**. Every advertised or fitted capability now has a guide or an explicit documented-absence.
- **Zero rows are hardware-tested.** This remains the single largest limitation of the whole research pass.
- **Four capabilities have guides but no demonstrated example**: BLE, ESP-NOW, USB HID/MSC, and OTA (one community project only). Each guide says so explicitly rather than implying coverage.

That last point matters more than a filled-in table. BLE, ESP-NOW and USB HID/MSC are *documented* here from vendor tutorials and standard Espressif APIs, but nobody in the surveyed community has published a working example on this board. That absence is not a sampling artefact — it reflects what people actually build. This board is bought for cameras over Wi-Fi. If your application is a battery-powered BLE device, there is far less prior art than the board's popularity implies, and you should weigh the [XIAO nRF52840 Sense](comparisons-and-recommendations.md#5-versus-xiao-nrf52840-sense) instead.

## Related
- [`compatibility-and-status.md`](compatibility-and-status.md) · [`resources-and-conflicts.md`](resources-and-conflicts.md) · [`features/README.md`](features/README.md) · [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
