# Cardputer ADV — Wi-Fi and BLE

> **Question:** *"How do I use the radio, and how good is the antenna?"*
> Radio is on the Stamp module, so this applies to the whole family with one real difference.
> Verified **2026-09-04**.

## Hardware

The ESP32-S3FN8's radio, matched by `L6 0 Ω / C19 4.3 nH / C20 (NC) / L1 2.7 nH / C2 2.2 pF /
C1 1.8 pF` into **ANT1** on the Stamp-S3A. Single 2.4 GHz chain: **Wi-Fi 802.11 b/g/n** and
**Bluetooth 5 LE**. No 5 GHz, no classic Bluetooth (the ESP32-S3 has no BR/EDR).

**The one generation difference:** M5Stack's own comparison table says the **antenna design was
optimised** on the Stamp-S3A — "Optimized antenna design for better reception" for v1.1 and
ADV versus "Standard antenna" for v1.0. The two Stamp schematics do show different matching
components, but a matching-network delta is not a quantified sensitivity improvement and
**no RF measurement is published**. Treat "better reception" as a vendor claim.

## Minimal procedure

Nothing Cardputer-specific — this is stock Arduino-ESP32 / ESP-IDF:

```cpp
#include <M5Cardputer.h>
#include <WiFi.h>
void setup() {
  auto cfg = M5.config(); M5Cardputer.begin(cfg, true);
  WiFi.mode(WIFI_STA);
  WiFi.begin("ssid", "pass");
  while (WiFi.status() != WL_CONNECTED) { delay(250); }
  M5Cardputer.Display.println(WiFi.localIP().toString());
}
void loop() {}
```

BLE: `NimBLE` is the practical choice on a no-PSRAM part, and it is what M5Stack's own factory
firmware uses — `sdkconfig.defaults` on the `CardputerADV` branch sets
`CONFIG_BT_NIMBLE_ENABLED=y`, `CONFIG_BT_NIMBLE_SM_LVL=2`,
`CONFIG_BT_NIMBLE_SVC_GAP_DEVICE_NAME="CardputerADV Keyboard"` and HID-tuned connection
parameters (12/48 interval, latency 8, 600 supervision timeout). The ADV factory firmware ships
as a **BLE HID keyboard**.

## The generic guide

Standard ESP32-S3 Wi-Fi and BLE procedures apply **unchanged**. There is no board-specific
provisioning, no external PA/LNA, no RF switch on the mainboard, and no coexistence hardware.

## What the community does with it

The radio is the reason most people buy this device. Catalogued in
[`../projects-and-community.md`](../projects-and-community.md):

* **Wi-Fi auditing** — Evil-M5Project (★2 570), Bruce (★6 642), ESP32Marauder (★12 212, has a
  `User_Setup_marauder_m5cardputer_adv.h`).
* **Wi-Fi CSI sensing** — `skizzophrenic/Cardputer-CSI-Human-Detector` (★207),
  `Zeloksa/Cardputer-ADV-CSI-Radar` (★100). Both 2026, both ADV. This is a genuinely unusual
  use of the part.
* **BLE tooling** — `MatthewKuKanich/ChimeraBLE` (★220), `Gitshaoxiang/M5Cardputer-BLE-HID-Keyboard`.
* **Streaming** — WebRadio ports, `geo-tp/M5Cardputer-Audio-Stream-Server`.
* **ESP-NOW** — the factory firmware pulls `espressif/esp-now@2.5.2` (see `dependencies.lock`).

## Resources and conflicts

| Resource | Note |
|---|---|
| RF | single chain; Wi-Fi and BLE coexist by time-sharing, as on any ESP32-S3 |
| **RAM** | **the binding constraint.** No PSRAM. A Wi-Fi stack plus TLS plus a framebuffer plus an audio decode buffer does not fit comfortably in 512 KB. |
| Power | 132.3 mA Wi-Fi / 154.6 mA BLE at 4.2 V (vendor) |
| **CAP LoRa** | a Cap LoRa-1262 adds a *second* radio at 868–923 MHz. No coexistence issue at those frequencies, but the SPI and current draw are shared. |

The RAM ceiling is not theoretical. The author of a Meshtastic client wrote (r/CardPuter,
2026-08-01): *"the ESP32-S3 here has no PSRAM, so a full Unicode font cannot live in RAM. It
ships as its own 2.16 MB flash partition … memory-mapped, so rendering Cyrillic, CJK or Greek
costs no heap at all."* That is a firsthand engineering account of working around the exact
constraint, and it is the single most instructive community post about this platform.

## Antenna modifications

`henriquesebastiao/external-cardputer-antenna` (★55) documents fitting an external antenna;
r/CardPuter has recurring "external antenna" mod posts. None of these are vendor-supported and
none carry measurements. Note that modifying the antenna invalidates whatever (unpublished)
certification the module carries.

## Evidence status

Antenna network: **official** — Stamp-S3A schematic. "Better reception": **vendor claim,
unquantified**. Radio capability: **silicon spec**. Everything about throughput, range or
sensitivity: **not tested, and no independent measurement found**.
