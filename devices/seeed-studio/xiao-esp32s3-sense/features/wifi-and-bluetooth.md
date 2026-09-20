# Wi-Fi and Bluetooth — XIAO ESP32S3 Sense

> Snapshot **2026-08-24**. No RF measurements were taken.

## 1. Radio capability

| Capability | Supported | Notes |
|---|---|---|
| Wi-Fi 802.11 b/g/n, **2.4 GHz** | ✅ | STA, AP, AP+STA, ESP-NOW |
| **5 GHz Wi-Fi** | ❌ | No 5 GHz radio in the silicon |
| Wi-Fi 6 | ❌ | 802.11n only |
| **BLE 5.0** | ✅ | GAP/GATT, mesh, extended advertising |
| **Bluetooth Classic (BR/EDR)** | ❌ **not present in silicon** | See §4 |

## 2. The antenna is detachable and there is no fallback

`ANT1` is a **U.FL / IPEX-1 receptacle**. There is **no PCB trace antenna and no chip antenna**. The RF path runs from the SoC's `LNA_IN` through a match (`C18` 1 pF, `L2` 3.3 nH; `C17`/`L3` are unpopulated alternates) directly to the connector.

With no antenna fitted, the radio drives an open circuit. It will still associate a metre from an access point, then behave erratically at any real range. **"Wi-Fi keeps dropping" on this board is very often a detached antenna** — the U.FL connector is small and pops off easily, especially when a board is repeatedly removed from an enclosure.

Seeed claims "100 m+ remote communication when connected with U.FL antenna". Unverified here and highly environment-dependent.

## 3. Practical notes

- **Antenna orientation matters** in wearables — the most common application for this board buries it in a printed case against a body. No measurements located.
- **Wi-Fi + BLE coexistence works** but costs throughput. The factory firmware binary contains the string *"Error! Should enable WiFi modem sleep when both WiFi and Bluetooth are enabled!!!!!!"* — enable modem sleep when running both.
- **ADC1 is unaffected by Wi-Fi.** All nine exposed analog pins are ADC1, so the well-known "ADC2 stops working with Wi-Fi" ESP32 problem does not apply here — ADC2 is not exposed at all. See [`../pinouts-and-buses.md` §1](../pinouts-and-buses.md#1-the-14-pin-user-header-u9).
- **Streaming is the bottleneck, not capture.** Camera + Wi-Fi MJPEG is where this board runs out of headroom: PSRAM bandwidth, JPEG encoding and TX all contend.
- **The 3.3 V rail is shared.** Wi-Fi TX bursts sit alongside the camera's 98–140 mA on a 600 mA budget — see [`../resources-and-conflicts.md` §5](../resources-and-conflicts.md#5-power-budget).

## 4. No Bluetooth Classic — read this before designing audio

The ESP32-S3 has **BLE only**. There is **no A2DP, AVRCP, HFP, SPP or Classic HID**.

This matters because the Sense's headline feature is a microphone, and "Bluetooth microphone" or "Bluetooth audio wearable" is a natural project idea that **cannot be built on this silicon**. Options:

- Stream audio over **Wi-Fi** instead — what [`esp32-birdnet-mic`](../examples/selected/esp32-birdnet-mic/) does, via RTSP.
- Use **BLE Audio / LE Audio** — but host support is patchy and the ESP-IDF story is immature.
- Use different silicon. The original ESP32 (e.g. ESP32-U4WDH) has BR/EDR.

Details: [ESP32-S3R8 component record](../../../../components/espressif/esp32-s3r8/README.md#radio-capabilities-and-the-classic-bluetooth-limitation).

## 5. Throughput

**No measurement was made here, and Seeed publishes no figure.**

The only benchmark located for this exact board is [`trzy/esp32s3-wifi-speed-test`](https://github.com/trzy/esp32s3-wifi-speed-test) (2 ★, unlicensed, last touched 2023-12). It is **not vendored** because it carries no licence — clone it yourself if you need numbers. See [`../performance.md`](../performance.md).

## 6. Getting started

Standard `WiFi.h` / NimBLE usage applies — nothing about this board changes the API. The board-specific concerns are: **fit the antenna**, enable modem sleep if using both radios, and budget the 3.3 V rail for TX bursts alongside the camera.

Note the factory firmware's Wi-Fi credentials are **compiled in** and are Seeed's own, so the shipped demo cannot join your network — see [`../factory-firmware.md` §5](../factory-firmware.md#5-the-factory-demo-cannot-connect-to-your-network).

**BLE is a coverage gap in this research pass:** no vendored example uses it, and no community BLE project for this board was catalogued. See [`../coverage.md`](../coverage.md).

## 7. Related
- [`../pinouts-and-buses.md` §10](../pinouts-and-buses.md#10-antenna) · [`camera.md`](camera.md) · [`../resources-and-conflicts.md`](../resources-and-conflicts.md) · [`../performance.md`](../performance.md)
