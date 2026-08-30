# lyngdorf-secondary-sleep

Minimal ESP-IDF firmware for the **secondary ESP32** on the [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm) board.

The board has two MCUs: the ESP32-S3 (which runs the [main lyngdorf-knob firmware](https://github.com/svwhisper/lyngdorf-knob)) and a secondary **ESP32-U4WDH** that ships running Waveshare's stock Bluetooth/WiFi audio firmware. The secondary chip is permanently powered from `3V3` and has no GPIO-controllable enable from the S3 — when left running stock firmware it draws **~50 mA continuously**, dominating idle battery current.

This project is a ~10-line app whose `app_main` calls `esp_deep_sleep_start()` with no wake sources configured. After flashing, the secondary draws ~10 µA and stays that way until power-cycled (which puts it back here, since deep sleep is the only thing the firmware does).

## Flash procedure

The board's single USB-C port routes to both MCUs depending on cable orientation. To talk to the secondary:

```bash
git clone https://github.com/svwhisper/lyngdorf-secondary-sleep.git
cd lyngdorf-secondary-sleep
idf.py set-target esp32 build

# Flip the USB-C cable 180° from its normal S3 orientation
ls /dev/cu.usbserial-*   # confirm — should show one entry

idf.py -p /dev/cu.usbserial-* flash

# Flip the cable back to its original orientation for normal S3 use
```

If your flash attempt reports `This chip is ESP32, not ESP32-S3`, you've got the cable in the right orientation for this project (it's expecting the S3, but is talking to the secondary). Use `--chip esp32` (which `idf.py` does automatically here since `set-target esp32` is in effect).

## Reverting

To restore Waveshare's stock audio firmware on the secondary, flip the cable back to the secondary orientation and flash whatever stock binary Waveshare distributes. Not bundled here.

## License

MIT.
