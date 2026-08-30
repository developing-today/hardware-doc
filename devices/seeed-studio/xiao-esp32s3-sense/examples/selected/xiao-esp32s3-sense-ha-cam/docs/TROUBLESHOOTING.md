# Troubleshooting (first basics)

## Camera doesn't start (ESP_FAIL)
1. Check that the Sense (camera) board is properly seated.
2. Confirm PSRAM is enabled (see `psram:` in the YAML).
3. Lower the resolution (e.g. `640x480`) to test.
4. Update ESPHome if needed (or try Arduino vs ESP-IDF framework).
5. Check the logs: `esphome logs ...`

## Device not discovered by HA
- Make sure HA and the device are on the same network.
- Check the `api:` section and that your firewall isn't blocking it.
