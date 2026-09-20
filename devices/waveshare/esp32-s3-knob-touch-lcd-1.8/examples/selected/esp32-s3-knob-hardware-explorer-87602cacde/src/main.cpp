/*
 * Test App for Waveshare ESP32-Knob — Hardware Explorer v0.4
 * Target board: Waveshare ESP32-S3-Knob-Touch-LCD-1.8 (N16R8)
 *
 * Walks through every peripheral once at boot and reports the result on
 * USB-CDC serial: I²C scan, battery ADC, backlight, DRV2605 LRA haptics,
 * rotary encoder, CST816 touch, WiFi scan, PCM5100A audio DAC, PDM mic.
 *
 * v0.3:  Hardware Explorer (alle Peripherie verifiziert, inkl. Audio + Mic)
 * v0.4:  LVGL v9.5 + Arduino_GFX auf ST77916 QSPI 360x360 — "Hello Knob"
 *
 * Build settings live in platformio.ini.
 * Custom board JSON: boards/waveshare_knob_18.json
 *  - 16 MB flash QIO, 8 MB OPI PSRAM
 *  - USB_MODE=1, USB_CDC_ON_BOOT=1, BOARD_HAS_PSRAM
 *
 * Repo: https://github.com/SuperEugen/esp32-s3-knob-hardware-explorer
 * License: MIT
 */

#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <ESP_I2S.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2s_pdm.h"
#include "driver/gpio.h"
#include "display.h"

// ── Pin-Definitionen ───────────────────────────────────────────────────────
#define PIN_LCD_BL        47
#define PIN_TOUCH_SCL     12
#define PIN_TOUCH_SDA     11
#define TOUCH_ADDR        0x15
#define DRV2605_ADDR      0x5A
#define PIN_ENCODER_A      8
#define PIN_ENCODER_B      7
// GPIO0 = PCM5100A Enable — kein Encoder-Button!
#define PIN_BAT_ADC        1

// Audio PCM5100A (I2S Ausgang → 3.5mm Klinke)
#define PIN_PCM_ENABLE    0    // HIGH = DAC aktiv, LOW = Mute
#define PIN_I2S_BCLK     39
#define PIN_I2S_WS       40
#define PIN_I2S_DOUT     41

// PDM Mikrofon
#define PIN_PDM_CLK      45
#define PIN_PDM_DATA     46

#define I2S_SAMPLE_RATE  44100

// ── Forward-Deklarationen (PlatformIO/C++ vs Arduino IDE) ──────────────────
void hardware_explorer_task(void* param);
void printSystemInfo();
void i2cScan();
void testBattery();
void testDisplayBacklight();
void testVibration();
void testTouch();
void testEncoder();
void testWiFi();
void testAudio();
void testMicrophone();
void testLVGL();
bool initAudioDAC();
void drv_write(uint8_t reg, uint8_t val);

// ── I2S Handle (Low-Level PDM Mic) ────────────────────────────────────────
static i2s_chan_handle_t rx_chan = NULL;

// ── Arduino I2S (High-Level DAC) ──────────────────────────────────────────
I2SClass i2s;

// ── I2C Scan ───────────────────────────────────────────────────────────────
void i2cScan() {
  printf("\n[I2C] Scanning...\n");
  int found = 0;
  for (uint8_t addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      printf("[I2C]   0x%02X", addr);
      if (addr == TOUCH_ADDR)   printf(" <- CST816 Touch");
      if (addr == DRV2605_ADDR) printf(" <- DRV2605 Vibration");
      if (addr == 0x69)         printf(" <- IMU (MPU6050/ICM-20948?)");
      printf("\n");
      found++;
    }
  }
  printf("[I2C] %d device(s) found\n", found);
}

// ── Akku ADC ───────────────────────────────────────────────────────────────
void testBattery() {
  printf("\n[BAT] Battery ADC Test\n");
  int raw = analogRead(PIN_BAT_ADC);
  float voltage = ((float)raw * 3.3f / 4096.0f) * 2.0f;
  printf("[BAT] ADC raw=%d  Vbat=%.2fV\n", raw, voltage);
  if (voltage > 3.5f && voltage < 4.35f)
    printf("[BAT] OK Battery healthy\n");
  else
    printf("[BAT] ?? Spannung ausserhalb Bereich\n");
}

// ── Display Backlight ──────────────────────────────────────────────────────
void testDisplayBacklight() {
  printf("\n[DSP] Backlight blinkt 3x...\n");
  pinMode(PIN_LCD_BL, OUTPUT);
  for (int i = 0; i < 3; i++) {
    digitalWrite(PIN_LCD_BL, HIGH); vTaskDelay(pdMS_TO_TICKS(300));
    digitalWrite(PIN_LCD_BL, LOW);  vTaskDelay(pdMS_TO_TICKS(300));
  }
  digitalWrite(PIN_LCD_BL, HIGH);
  printf("[DSP] OK Backlight OK\n");
}

// ── Vibration DRV2605 ──────────────────────────────────────────────────────
void drv_write(uint8_t reg, uint8_t val) {
  Wire.beginTransmission(DRV2605_ADDR);
  Wire.write(reg); Wire.write(val);
  Wire.endTransmission();
}

void testVibration() {
  printf("\n[VIB] DRV2605 LRA Test\n");
  Wire.beginTransmission(DRV2605_ADDR);
  if (Wire.endTransmission() != 0) { printf("[VIB] nicht gefunden\n"); return; }
  drv_write(0x01, 0x00);
  drv_write(0x1D, 0xA8); // LRA Feedback
  drv_write(0x1A, 0x05); // Library 5 = LRA
  drv_write(0x04, 0x01); drv_write(0x05, 0x00); drv_write(0x0C, 0x01);
  printf("[VIB] Effect #1 Strong Click\n"); vTaskDelay(pdMS_TO_TICKS(600));
  drv_write(0x01, 0x05); drv_write(0x02, 0xFF);
  printf("[VIB] RTP volle Amplitude 1s\n"); vTaskDelay(pdMS_TO_TICKS(1000));
  drv_write(0x02, 0x00); drv_write(0x01, 0x00);
  printf("[VIB] OK\n");
}

// ── Touch CST816 ───────────────────────────────────────────────────────────
void testTouch() {
  printf("\n[TCH] Touch Test - 5 Sek antippen!\n");
  Wire.beginTransmission(TOUCH_ADDR);
  Wire.write(0x00); Wire.write(0x00);
  Wire.endTransmission();
  vTaskDelay(pdMS_TO_TICKS(50));
  uint32_t deadline = millis() + 5000;
  int count = 0;
  while (millis() < deadline) {
    uint8_t data[7] = {0};
    Wire.beginTransmission(TOUCH_ADDR);
    Wire.write(0x00);
    Wire.endTransmission(false);
    Wire.requestFrom((uint8_t)TOUCH_ADDR, (uint8_t)7);
    for (int i = 0; i < 7 && Wire.available(); i++) data[i] = Wire.read();
    if (data[2] > 0) {
      uint16_t x = ((uint16_t)(data[3] & 0x0F) << 8) | data[4];
      uint16_t y = ((uint16_t)(data[5] & 0x0F) << 8) | data[6];
      printf("[TCH] x=%d y=%d gesture=0x%02X\n", x, y, data[1]);
      count++;
    }
    vTaskDelay(pdMS_TO_TICKS(50));
  }
  printf("[TCH] %d events\n", count);
}

// ── Encoder ────────────────────────────────────────────────────────────────
volatile int encoderPos = 0;
void IRAM_ATTR encoderISR() {
  encoderPos = encoderPos + (digitalRead(PIN_ENCODER_B) == HIGH ? 1 : -1);
}
void testEncoder() {
  printf("\n[ENC] Encoder Test - 5 Sek drehen!\n");
  encoderPos = 0;
  attachInterrupt(digitalPinToInterrupt(PIN_ENCODER_A), encoderISR, RISING);
  uint32_t deadline = millis() + 5000;
  int last = 0;
  while (millis() < deadline) {
    if (encoderPos != last) { printf("[ENC] %d\n", encoderPos); last = encoderPos; }
    vTaskDelay(pdMS_TO_TICKS(10));
  }
  detachInterrupt(digitalPinToInterrupt(PIN_ENCODER_A));
  printf("[ENC] Endposition: %d\n", encoderPos);
}

// ── WiFi ───────────────────────────────────────────────────────────────────
void testWiFi() {
  printf("\n[WiFi] Scanning...\n");
  WiFi.mode(WIFI_STA); WiFi.disconnect(); vTaskDelay(pdMS_TO_TICKS(100));
  int n = WiFi.scanNetworks();
  printf("[WiFi] %d Netzwerk(e)\n", n);
  for (int i = 0; i < min(n, 5); i++)
    printf("[WiFi]  %d: %-28s RSSI=%d\n", i+1, WiFi.SSID(i).c_str(), WiFi.RSSI(i));
  WiFi.scanDelete();
}

// ── Audio DAC (PCM5100A) ───────────────────────────────────────────────────
// Sinuston-Tabelle: 100 Samples einer vollen Periode, Amplitude 28000 (< 32767)
static const int16_t sine440[100] = {
     0,  1763,  3512,  5234,  6915,  8544, 10109, 11598, 13000, 14304,
 15500, 16580, 17533, 18352, 19029, 19557, 19930, 20144, 20196, 20086,
 19812, 19375, 18779, 18027, 17123, 16074, 14886, 13568, 12126, 10570,
  8908,  7150,  5306,  3386,  1402,  -591, -2584, -4566, -6526, -8453,
-10336,-12163,-13923,-15608,-17206,-18708,-20104,-21385,-22542,-23567,
-24452,-25190,-25777,-26208,-26479,-26589,-26537,-26325,-25954,-25427,
-24748,-23922,-22956,-21857,-20633,-19293,-17845,-16299,-14665,-12954,
-11174, -9338, -7455, -5537, -3595, -1640,   316,  2261,  4184,  6073,
  7916,  9703, 11422, 13063, 14616, 16071, 17419, 18651, 19759, 20735,
 21571, 22261, 22799, 23179, 23399, 23456, 23350, 23083, 22655, 22070
};

bool initAudioDAC() {
  // GPIO0 HIGH = PCM5100A enable
  gpio_config_t cfg = {};
  cfg.pin_bit_mask = (1ULL << PIN_PCM_ENABLE);
  cfg.mode = GPIO_MODE_OUTPUT;
  cfg.pull_up_en = GPIO_PULLUP_ENABLE;
  gpio_config(&cfg);
  gpio_set_level((gpio_num_t)PIN_PCM_ENABLE, 1);
  vTaskDelay(pdMS_TO_TICKS(20));

  // Arduino ESP_I2S High-Level API
  i2s.setPins(PIN_I2S_BCLK, PIN_I2S_WS, PIN_I2S_DOUT, -1); // bclk, ws, dout, din
  if (!i2s.begin(I2S_MODE_STD, I2S_SAMPLE_RATE, I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_STEREO)) {
    return false;
  }
  return true;
}

void testAudio() {
  printf("\n[AUD] PCM5100A Audio DAC Test\n");
  printf("[AUD] Kopfhoerer/Lautsprecher an 3.5mm anschliessen!\n");
  if (!initAudioDAC()) {
    printf("[AUD] FEHLER: I2S Init fehlgeschlagen\n");
    return;
  }
  printf("[AUD] I2S OK, spiele 440Hz Sinuston 3 Sek...\n");

  uint32_t deadline = millis() + 3000;
  int writes = 0;
  while (millis() < deadline) {
    for (int i = 0; i < 100; i++) {
      i2s.write(sine440[i]); // L
      i2s.write(sine440[i]); // R
    }
    writes++;
  }
  printf("[AUD] %d Durchlaeufe\n", writes);
  i2s.end();
  printf("[AUD] OK - Ton gehoert?\n");
}

// ── PDM Mikrofon ───────────────────────────────────────────────────────────
void testMicrophone() {
  printf("\n[MIC] PDM Mikrofon Test - 3 Sek sprechen!\n");

  i2s_chan_config_t rx_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_0, I2S_ROLE_MASTER);
  if (i2s_new_channel(&rx_cfg, NULL, &rx_chan) != ESP_OK) {
    printf("[MIC] FEHLER: Channel init\n"); return;
  }
  i2s_pdm_rx_config_t pdm_cfg = {
    .clk_cfg  = I2S_PDM_RX_CLK_DEFAULT_CONFIG(44100),
    .slot_cfg = I2S_PDM_RX_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_MONO),
    .gpio_cfg = {
      .clk = (gpio_num_t)PIN_PDM_CLK,
      .din = (gpio_num_t)PIN_PDM_DATA,
    },
  };
  if (i2s_channel_init_pdm_rx_mode(rx_chan, &pdm_cfg) != ESP_OK) {
    printf("[MIC] FEHLER: PDM mode init\n"); return;
  }
  if (i2s_channel_enable(rx_chan) != ESP_OK) {
    printf("[MIC] FEHLER: Channel enable\n"); return;
  }

  printf("[MIC] Lese 3 Sek Audio...\n");
  int16_t buf[256];
  int32_t maxVal = 0;
  int32_t sumSq = 0;
  int samples = 0;
  uint32_t deadline = millis() + 3000;

  while (millis() < deadline) {
    size_t read = 0;
    if (i2s_channel_read(rx_chan, buf, sizeof(buf), &read, 200) == ESP_OK) {
      int n = read / 2;
      for (int i = 0; i < n; i++) {
        int32_t v = abs(buf[i]);
        if (v > maxVal) maxVal = v;
        sumSq += (buf[i] / 256) * (buf[i] / 256); // skaliert um Overflow zu vermeiden
        samples++;
      }
    }
  }
  i2s_channel_disable(rx_chan);
  i2s_del_channel(rx_chan);
  rx_chan = NULL;

  float rms = (samples > 0) ? sqrtf((float)sumSq / samples) : 0;
  printf("[MIC] Peak: %ld  RMS: %.1f  Samples: %d\n", maxVal, rms, samples);
  if (maxVal > 500)
    printf("[MIC] OK Mikrofon reagiert auf Geraeusche!\n");
  else if (maxVal > 50)
    printf("[MIC] LEISE - Umgebungsrauschen erkannt, kein Ton?\n");
  else
    printf("[MIC] ?? Kaum Signal - Pin oder Init Problem?\n");
}

// ── LVGL Display Test (v0.4) ───────────────────────────────────────────────
void testLVGL() {
  printf("\n[LVG] LVGL Hello-World Test\n");
  if (!display_init()) {
    printf("[LVG] FEHLER: display_init() fehlgeschlagen\n");
    return;
  }

  // Optional: nacktes Arduino_GFX-Pattern fuer Display-Diagnose.
  // Auskommentiert lassen im normalen Betrieb. Bei Display-Problemen
  // einkommentieren — zeigt R/G/B/Streifen/Kreuz/Ecken-Text VOR LVGL.
  // display_test_pattern();

  // LVGL freigeben: erst hier darf loop() lv_timer_handler() rufen.
  display_enable_lvgl();

  // LVGL Hello-Welt
  printf("[LVG] Jetzt LVGL UI...\n");
  display_show_hello();
  printf("[LVG] UI laeuft, loop() haelt sie am Leben.\n");
  printf("[LVG] OK\n");
}

// ── System-Info (Sanity-Check) ─────────────────────────────────────────────
void printSystemInfo() {
  printf("\n[SYS] Chip:       %s rev %d  (%d cores)\n",
         ESP.getChipModel(), ESP.getChipRevision(), ESP.getChipCores());
  printf("[SYS] CPU:        %lu MHz\n", (unsigned long)ESP.getCpuFreqMHz());
  printf("[SYS] Flash:      %lu MB @ %lu MHz  mode=0x%X\n",
         (unsigned long)(ESP.getFlashChipSize() / (1024 * 1024)),
         (unsigned long)(ESP.getFlashChipSpeed() / 1000000),
         (unsigned int)ESP.getFlashChipMode());
  printf("[SYS] PSRAM:      total=%lu KB  free=%lu KB",
         (unsigned long)(ESP.getPsramSize() / 1024),
         (unsigned long)(ESP.getFreePsram() / 1024));
  if (ESP.getPsramSize() == 0)
    printf("  ?? KEIN PSRAM aktiv!\n");
  else if (ESP.getPsramSize() >= 8 * 1024 * 1024)
    printf("  OK 8MB Octal\n");
  else
    printf("  ?? unerwartete Groesse\n");
  printf("[SYS] Heap:       total=%lu KB  free=%lu KB\n",
         (unsigned long)(ESP.getHeapSize() / 1024),
         (unsigned long)(ESP.getFreeHeap() / 1024));
  printf("[SYS] SDK:        %s\n", ESP.getSdkVersion());
}

// ── Haupt-Task ─────────────────────────────────────────────────────────────
void hardware_explorer_task(void* param) {
  vTaskDelay(pdMS_TO_TICKS(500));
  printf("\n===========================================\n");
  printf("  Test App for Waveshare ESP32-Knob - Hardware Explorer v0.3\n");
  printf("  Waveshare ESP32-S3 Knob Touch LCD 1.8\n");
  printf("===========================================\n");

  printSystemInfo();

  Wire.begin(PIN_TOUCH_SDA, PIN_TOUCH_SCL);
  pinMode(PIN_ENCODER_A, INPUT_PULLUP);
  pinMode(PIN_ENCODER_B, INPUT_PULLUP);
  analogReadResolution(12);

  i2cScan();
  testBattery();
  // testDisplayBacklight();   // disabled in v0.4 — LVGL uebernimmt Backlight (Pin 47)
  testVibration();
  testEncoder();   // 5 Sek drehen
  testTouch();     // 5 Sek antippen
  testWiFi();
  testAudio();     // Kopfhoerer rein! 3 Sek Ton
  testMicrophone(); // 3 Sek sprechen/klopfen
  testLVGL();      // v0.4 — Display + LVGL Hello-World

  printf("\n===========================================\n");
  printf("  DONE - alle Tests abgeschlossen\n");
  printf("===========================================\n");
  vTaskDelete(NULL);
}

void setup() {
  // Serial = USB-CDC (Hardware-CDC vom ESP32-S3) wenn USB_CDC_ON_BOOT=1
  Serial.begin(115200);
  delay(2000);  // USB-CDC braucht'n Moment bis Host-Seite verbindet

  // printf/puts auf Serial umleiten, damit unser bestehender printf-Code
  // ueber USB-CDC rauskommt statt auf UART0
  ets_install_putc1([](char c) { Serial.write((uint8_t)c); });

  xTaskCreate(hardware_explorer_task, "hw_explorer", 8192, NULL, 2, NULL);
}

void loop() {
  // LVGL weiter ticken lassen, damit das Hello-Bild stehen bleibt.
  // Falls display_init() fehlgeschlagen ist, schadet display_tick() nicht
  // (lv_timer_handler() ist tolerant gegenueber leerer Display-Liste).
  display_tick();
  vTaskDelay(pdMS_TO_TICKS(5));
}
