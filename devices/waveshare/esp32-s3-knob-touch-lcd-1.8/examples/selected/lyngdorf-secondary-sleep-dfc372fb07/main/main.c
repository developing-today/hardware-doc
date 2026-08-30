// Minimal "sleep forever" firmware for the ESP32-U4WDH secondary MCU on the
// Waveshare ESP32-S3-Knob-Touch-LCD-1.8 board. Goal: drop the secondary into
// the lowest power state possible so it stops contributing ~50 mA to board
// idle current.
//
// No wake sources are configured, so the chip stays in deep sleep until
// power is removed (or the cable is flipped and a different image flashed).

#include "esp_sleep.h"
#include "esp_log.h"

void app_main(void) {
    ESP_LOGI("sleep", "secondary entering deep sleep (no wake source)");
    esp_sleep_disable_wakeup_source(ESP_SLEEP_WAKEUP_ALL);
    esp_deep_sleep_start();
}
