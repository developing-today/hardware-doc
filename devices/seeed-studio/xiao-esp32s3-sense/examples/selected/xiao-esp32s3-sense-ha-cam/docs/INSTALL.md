# Install (ESPHome Builder / Dashboard) — MiniCam ESP32 (XIAO ESP32S3 Sense)

This guide installs the **MiniCam ESP32** firmware on a **Seeed Studio XIAO ESP32S3 Sense** using **ESPHome Builder / Dashboard** (Home Assistant add-on).

## Prerequisites
- Home Assistant running
- ESPHome add-on installed and working
- Your `secrets.yaml` contains:
  - `wifi_ssid`
  - `wifi_password`
  - `api_encryption_key`
  - `ota_password`

## 1) Wire & power
- Plug the XIAO ESP32S3 Sense via **USB-C data cable**.
- Keep the Sense expansion (camera) firmly connected.

## 2) Create or open the device in ESPHome
- Open **ESPHome** in Home Assistant.
- Create a new device or select your existing one (e.g. `minicam-esp32`).

## 3) Paste the firmware YAML
Copy the content of `esphome/minicam-esp32.yaml` into the device configuration.

## 4) First flash (USB)
- Click **INSTALL**
- Choose **Plug into this computer** (USB/Serial)
- Select the detected serial port (e.g. `/dev/ttyACM3`)
- Wait for **Compile** → **Flash** to complete

> If it fails to connect, hold **BOOT** while plugging USB, then retry INSTALL.

## 5) Verify it works
From the ESPHome logs, note the IP address (example: `192.168.1.145`).

Test in a browser:
- Stream: `http://<IP>:8080`
- Snapshot: `http://<IP>:8081`

## 6) Home Assistant integration
Home Assistant should auto-discover the device via ESPHome:
- **Settings → Devices & Services → ESPHome**
- Add the discovered device.

## Update via OTA (later)
Once the device is on Wi‑Fi:
- In ESPHome, click **INSTALL**
- Choose **Wirelessly** (OTA)
