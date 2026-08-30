# Bluetooth LE — XIAO ESP32S3 Sense

> BLE on this board, and the one thing it categorically cannot do.
> Snapshot **2026-08-24**. No hardware testing. Vendor source: `XIAO_ESP32S3_Bluetooth_Usage.md` in the [wiki snapshot](../artifacts/wiki-snapshot/).

## 1. ⚠ There is no Bluetooth Classic

**The ESP32-S3 is BLE-only.** No BR/EDR, therefore **no A2DP, AVRCP, HFP, HSP, SPP or Classic HID**.

This bites hardest on exactly this board, because the Sense has a microphone and "Bluetooth audio wearable" is the obvious project idea. It cannot be built here:

| You want | On this board |
|---|---|
| Stream audio to Bluetooth headphones (A2DP) | ❌ **impossible** |
| Act as a Bluetooth headset / mic (HFP/HSP) | ❌ **impossible** |
| Serial-over-Bluetooth to a phone (SPP) | ❌ impossible — use **BLE NUS** instead |
| Classic Bluetooth keyboard/mouse | ❌ — BLE HID works instead |
| BLE GATT sensor / beacon / config link | ✅ |
| BLE Mesh | ✅ |

If you need Classic, use original-ESP32 silicon (e.g. the [ESP32-U4WDH](../../../../components/espressif/esp32-u4wdh/README.md) documented in this repo). Otherwise stream audio [over Wi-Fi](wifi-and-bluetooth.md#5-throughput), as [`esp32-birdnet-mic`](../examples/selected/esp32-birdnet-mic/) does with RTSP.

Seeed's own wiki says the board "supports Bluetooth 5, BLE, and Mesh networking" — accurate, but easy to misread as including Classic. See the [ESP32-S3R8 record](../../../../components/espressif/esp32-s3r8/README.md#radio-capabilities-and-the-classic-bluetooth-limitation).

## 2. Two stacks: Bluedroid vs NimBLE

| | **Bluedroid** (`BLEDevice.h`) | **NimBLE** (`NimBLEDevice.h`) |
|---|---|---|
| Ships with Arduino-ESP32 | ✅ built in | ❌ install `NimBLE-Arduino` |
| Flash footprint | Large | **~⅓ the size** |
| RAM | Higher | Lower |
| API | What Seeed's tutorials use | Similar but not identical |

**On this board, footprint matters.** The app partition is **3,264 KB** and a camera application already consumes most of it ([`../factory-firmware.md` §4](../factory-firmware.md#4-flash-map)). If you are combining BLE with the camera, **use NimBLE** — Bluedroid plus `esp32-camera` plus Wi-Fi is a realistic way to overflow the partition.

## 3. Scanning (vendor example)

```cpp
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

int scanTime = 5;              // seconds
BLEScan *pBLEScan;

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks {
  void onResult(BLEAdvertisedDevice d) {
    Serial.printf("Advertised: %s \n", d.toString().c_str());
  }
};

void setup() {
  Serial.begin(115200);
  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);   // faster results, more power
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99);
}

void loop() {
  BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
  Serial.printf("Devices found: %d\n", foundDevices.getCount());
  pBLEScan->clearResults();        // free the results buffer
  delay(2000);
}
```

### ⚠ Arduino-ESP32 3.x API break

Seeed's wiki flags this explicitly. On core **3.x**, `start()` returns a **pointer**:

```cpp
// 2.x
BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
// 3.x
BLEScanResults *foundDevices = pBLEScan->start(scanTime, false);
```

Same 2.x→3.x hazard as the [I²S microphone API](microphone.md#4-minimal-example--arduino-2x-legacy) and the [camera `pin_sccb_*` rename](../development.md#the-2x--3x-break). Check your core version first.

**`clearResults()` is not optional** — scan results accumulate in RAM, and a long-running scanner without it will exhaust the heap.

## 4. GATT server

The standard pattern: a **server** advertises and holds data; a **client** scans, connects and reads or subscribes. Data lives in **characteristics** grouped into **services**, each identified by a UUID.

Characteristic properties map onto the four ATT operations — **read, write, notify, indicate**. Notify sends without a response; indicate requires acknowledgement.

```cpp
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

void setup() {
  BLEDevice::init("XIAO_ESP32S3");
  BLEServer *pServer = BLEDevice::createServer();
  BLEService *pService = pServer->createService(SERVICE_UUID);

  BLECharacteristic *pChar = pService->createCharacteristic(
      CHARACTERISTIC_UUID,
      BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY);
  pChar->addDescriptor(new BLE2902());     // required for notify
  pChar->setValue("Hello");

  pService->start();
  BLEDevice::getAdvertising()->addServiceUUID(SERVICE_UUID);
  BLEDevice::startAdvertising();
}
```

`BLE2902` (the Client Characteristic Configuration Descriptor) is **required for notifications** — omitting it is a common reason a client connects but never receives updates.

> ⚠ The service UUID in Seeed's wiki is printed as `4fafc201-1fb5-459e-8n-c5c9c331914b` — **`8n` is not valid hex**. It is a transcription error in the wiki. The correct upstream value is `...-459e-8fcc-...`.

## 5. Resource cost and coexistence

| Resource | BLE |
|---|---|
| GPIO | **none** — shares the antenna |
| Flash | Bluedroid large; NimBLE ~⅓ |
| RAM | significant; contends with camera framebuffers |
| Antenna | shared with Wi-Fi |

**Wi-Fi + BLE coexistence works but costs throughput.** The factory firmware binary contains the string *"Error! Should enable WiFi modem sleep when both WiFi and Bluetooth are enabled!!!!!!"* — enable modem sleep when running both.

**BLE + camera is realistic** (no pin conflict, and BLE uses no GPIO), but watch flash and RAM. `ebowwa/esp32s3-cam-firmware` in the [catalog](../examples/catalog.json) does camera + BLE, though it is unlicensed and was not vendored.

**BLE needs the antenna fitted.** Same U.FL caveat as Wi-Fi — [there is no PCB fallback antenna](wifi-and-bluetooth.md#2-the-antenna-is-detachable-and-there-is-no-fallback).

## 6. Power

BLE advertising is far cheaper than Wi-Fi, which makes "BLE sensor that sleeps between advertisements" attractive on paper. **On a Sense board it is undermined by the camera**, which cannot be powered down and dominates sleep current — see [`deep-sleep.md`](deep-sleep.md).

If your product is a battery-powered BLE sensor with no camera, the [XIAO nRF52840 Sense](../comparisons-and-recommendations.md#5-versus-xiao-nrf52840-sense) is the better board: ~5 µA sleep, an IMU, and battery voltage sensing this board lacks.

## 7. Coverage gap — be aware

**No BLE example was located for this board** in the 18-project survey, and none is vendored. The community builds Wi-Fi cameras with it, not BLE devices.

That means: the API above is standard ESP32 BLE (which is well documented by Espressif and works the same everywhere), but **board-specific BLE pitfalls — range with the U.FL antenna in an enclosure, coexistence behaviour under camera load, real power figures — are undocumented by anyone**, including this research pass.

If you are choosing this board *for* BLE, you are on less-trodden ground than its popularity suggests.

## 8. Related
- [`wifi-and-bluetooth.md`](wifi-and-bluetooth.md) — radio overview, antenna, coexistence
- [`deep-sleep.md`](deep-sleep.md) — why BLE low-power designs struggle here
- [ESP32-S3R8](../../../../components/espressif/esp32-s3r8/README.md) — the Classic Bluetooth limitation at source
- [`../coverage.md`](../coverage.md) · [`../comparisons-and-recommendations.md`](../comparisons-and-recommendations.md)
