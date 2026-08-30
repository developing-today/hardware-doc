# ESP-NOW — XIAO ESP32S3 Sense

> Router-free, low-latency device-to-device messaging. Cheap on this board because it costs no pins.
> Snapshot **2026-08-24**. No hardware testing. Vendor source: `Application/XIAO_ESP32S3_ESPNOW.md` in the [wiki snapshot](../artifacts/wiki-snapshot/).

## 1. What it is

ESP-NOW is Espressif's **connectionless link-layer protocol**. Devices address each other by **MAC address** — no access point, no IP stack, no pairing handshake, no association delay.

Seeed's summary of why it exists:

> "ESP-NOW is a wireless communication protocol based on the **data link layer**, which simplifies the five-layer OSI upper-layer protocol into one layer without the need to add packet headers and unpack layer by layer. It greatly alleviates the lag and delay caused by packet loss during network congestion and has a **higher response speed**."

Supported topologies: **one-to-one, one-to-many, many-to-one and many-to-many**.

| Versus | ESP-NOW advantage |
|---|---|
| **Wi-Fi** | Lower power, lower latency, longer range, no router needed |
| **BLE** | No pairing process, lower power, higher throughput |

**When *not* to use it:** ESP-NOW suits fast, reliable, low-power point-to-point links. Complex networks, many devices, or anything needing IP (cloud, MQTT, web) still want Wi-Fi.

## 2. Why it fits this board particularly well

Two board-specific reasons ESP-NOW deserves consideration here:

**It costs zero GPIO.** With [only ~4 free pins](gpio-adc-and-pwm.md#1-the-eleven-pins-you-get) once the daughterboard and SD card are in use, a radio protocol that needs no pins is valuable.

**It avoids Wi-Fi association entirely.** A duty-cycled Sense node that wakes, captures and transmits pays no DHCP/association cost — significant when [the camera already dominates your power budget](deep-sleep.md).

The obvious application: **a camera node that wakes, takes a picture, and hands it to a nearby gateway** without either device being on a network. Note the payload limit in §5 makes image transfer a chunked affair.

## 3. Minimal sender

Adapted from Seeed's example (which targets an S3 sender talking to C3/C6 receivers):

```cpp
#include <Arduino.h>
#include "WiFi.h"
#include "esp_now.h"

// Receiver MAC — you MUST read this off your own device, not copy it
static uint8_t peerMac[6] = {0x64, 0xe8, 0x33, 0x89, 0x80, 0xb8};
esp_now_peer_info_t peerInfo;

void onSent(const uint8_t *mac, esp_now_send_status_t status) {
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivered" : "Failed");
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);            // required, even with no AP
  Serial.println(WiFi.macAddress());   // ← read your own MAC here

  if (esp_now_init() != ESP_OK) { Serial.println("ESP-NOW init failed"); return; }
  esp_now_register_send_cb(onSent);

  memcpy(peerInfo.peer_addr, peerMac, 6);
  peerInfo.channel = 0;           // 0 = use current Wi-Fi channel
  peerInfo.encrypt = false;
  if (esp_now_add_peer(&peerInfo) != ESP_OK) { Serial.println("add peer failed"); return; }
}

void loop() {
  const char *msg = "hello";
  esp_now_send(peerMac, (uint8_t *)msg, strlen(msg));
  delay(2000);
}
```

Receiver side registers `esp_now_register_recv_cb()` and reads the payload in the callback.

> ⚠ Seeed's example includes the comment *"You need input your XIAO ESP32 Series MAC, **Cannot copy directly!!!!**"* — the MAC addresses in the tutorial are those of the author's boards. Print `WiFi.macAddress()` on each of your own devices first. Using the tutorial's values is the single most common ESP-NOW mistake.

## 4. Channel and coexistence rules

These cause most ESP-NOW failures and are not board-specific, but they are worth stating:

- **`WiFi.mode(WIFI_STA)` is mandatory** even though no AP is involved — ESP-NOW runs on the Wi-Fi MAC.
- **All peers must be on the same Wi-Fi channel.** Setting `peerInfo.channel = 0` means "whatever channel this device is currently on".
- **If one device is connected to an AP, its channel is fixed by that AP** — the other peers must match it. A node joined to a 2.4 GHz network on channel 6 cannot talk to a peer sitting on channel 1.
- **Do not call `WiFi.disconnect()`** after `esp_now_init()`; it can drop the channel configuration.
- ESP-NOW **coexists with Wi-Fi and BLE**, sharing the same radio, with the usual throughput cost.

## 5. Limits

| Limit | Value |
|---|---|
| **Max payload** | **250 bytes** per packet |
| Encrypted peers | 6 (ESP32-S3, with encryption enabled) |
| Total peers | 20 |
| Channel | must match across peers |
| Delivery | callback reports success/failure; **no automatic retry** |

**250 bytes is the number to design around.** A QVGA JPEG from this board is tens of kilobytes — that is hundreds of packets, needing your own chunking, sequencing and reassembly. ESP-NOW has no fragmentation layer.

**For image transfer, Wi-Fi is the right tool.** Use ESP-NOW for telemetry, triggers, commands, and "wake the gateway, then switch to Wi-Fi" handoffs.

## 6. Security

`peerInfo.encrypt = false` in the example above means **packets are sent in the clear**. ESP-NOW supports encryption with a PMK/LMK, at the cost of being limited to 6 encrypted peers. If your device controls anything, enable it.

## 7. Coverage status

**No ESP-NOW example was located for this board** in the 18-project survey, and none is vendored. The code above is from Seeed's tutorial plus standard Espressif API usage, and was **not compiled or tested here**.

The protocol is Espressif's and behaves identically across ESP32 boards, so there is no board-specific reason to expect trouble — but no board-specific range, throughput or power figures exist either.

Seeed's tutorial itself is cross-device (XIAO ESP32S3 ↔ C3 ↔ C6), which is a useful signal: ESP-NOW works across the XIAO family, so a cheap [ESP32C3 at $4.99](../market-and-pricing.md) makes a sensible receiver for a Sense camera node.

## 8. Related
- [`wifi-and-bluetooth.md`](wifi-and-bluetooth.md) — radio, antenna, coexistence
- [`ble.md`](ble.md) — the other pin-free radio option
- [`deep-sleep.md`](deep-sleep.md) — why avoiding association matters here
- [`gpio-adc-and-pwm.md`](gpio-adc-and-pwm.md) — the pin scarcity that makes ESP-NOW attractive
