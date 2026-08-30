# Espressif guides

Cross-cutting notes about Espressif's silicon lineup and its **framework documentation** (ESP-IDF, ESP-ADF, ESP-IoT-Solution, esp-dev-kits), as opposed to the per-chip and per-board records under [`components/`](../../components/README.md) and [`devices/`](../../devices/README.md).

## Silicon

| Page | What it captures |
|---|---|
| [**Ecosystem and product lines**](ecosystem-and-product-lines.md) | **The family map.** ESP8266 → ESP32 → S2/S3 → C2/C3/C5/C6/C61 → H2/H21/H4 → P4: which have Classic Bluetooth vs BLE-only vs 802.15.4 vs **no radio at all**, Xtensa vs RISC-V, when each is the right choice, bare chip vs module vs devkit, the ordering-nomenclature decode (`U4WDH`, `R8`, `N16`, the `P4X` trap), and the **companion-radio pattern** (P4 + C6/C5) contrasted with the S3 + U4WDH retrofit. Links to the deep records rather than duplicating them |

## Frameworks and SDKs

These pages exist because the source PDFs were large (~219 MB total), fully regenerable from stable Espressif URLs, and **not scarce** — so they were archived out of the repository after the durable knowledge in them was extracted here. Every fact below cites its source document, version and page.

| Page | What it captures |
|---|---|
| [ESP-IDF peripheral capabilities](esp-idf-peripheral-capabilities.md) | Cross-target **ESP32 vs ESP32-S3 vs ESP32-P4** comparison — peripheral instance counts, LEDC/SDMMC/I2S/USB divergences, PSRAM and flash configuration constraints, and the API entry point for each peripheral. Includes the important negative result that the IDF guide renders `SOC_*` counts **symbolically**, so the retained TRMs stay authoritative for RMT/PCNT/MCPWM/timer counts. |
| [ESP-ADF audio pipelines](esp-adf-audio-pipelines.md) | The ESP-ADF Element→Pipeline architecture, the Bluetooth Classic (HFP/A2DP/AVRCP) service API, codec/`audio_hal` integration, and the **audio memory budget** — the numbers that constrain the Classic-BT audio path on the ESP32-U4WDH. |
| [ESP-IoT-Solution components](esp-iot-solution-components.md) | The **LCD driver-interface selection table**, touch-controller support, the **Knob** software-PCNT component and its accuracy limits, and the USB controller taxonomy — the component drivers behind the knob board and the P4 display boards. |

## Archive records

The PDFs these pages were distilled from, with SHA-256, page counts and verified download URLs:

- [ESP32-U4WDH artifacts](../../components/espressif/esp32-u4wdh/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) — ESP-IDF v5.1.4 & v5.2.5 (`esp32`), ESP-ADF
- [ESP32-S3R8 artifacts](../../components/espressif/esp32-s3r8/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) — ESP-IDF v5.1.4 & v5.2.5 (`esp32s3`), ESP-IoT-Solution
- [ESP32-P4 artifacts](../../components/espressif/esp32-p4/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) — ESP-IDF v5.3.2 (`esp32p4`)
- [ESP32-P4 board shared artifacts](../../devices/espressif/shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) — esp-dev-kits (`esp32p4`)

## Related

- [How to obtain any Espressif document](../../vendors/espressif/README.md) — the sourcing procedure, including where Espressif does and does not publish PDF builds
- [Guides index](../README.md) · [Markets and sourcing](../markets/README.md)
- Chip records: [ESP32-P4](../../components/espressif/esp32-p4/README.md) · [ESP32-S3R8](../../components/espressif/esp32-s3r8/README.md) · [ESP32-U4WDH](../../components/espressif/esp32-u4wdh/README.md)
