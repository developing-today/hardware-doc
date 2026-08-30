# Wiring / Notes

## Camera
On the **XIAO ESP32S3 Sense**, the camera sits on the Sense expansion board (OV2640 or OV3660 depending on the batch).

The `esp32_camera` pin mapping in the YAML is based on Seeed's reference example.

## Buttons
- **BOOT**: useful to force bootloader mode if needed
- **RESET**: reboots the device

## Antenna
The XIAO has a U.FL connector to improve Wi-Fi/BT range if you have the external antenna.
