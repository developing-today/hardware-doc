/*
 * ═══════════════════════════════════════════════════════════════
 *  Waveshare ESP32-S3-KNOB — SH8601 AMOLED + DRV2605 Haptics
 *
 *  DISPLAY:  SH8601 AMOLED 360×360 via QSPI @ 40MHz
 *  HAPTICS:  DRV2605 vibration driver via I2C (SDA=11, SCL=12)
 *
 *  4 Haptic Effects:
 *  ① Encoder Click    — Sharp Click (effect #6) on every step
 *  ② Inertia          — Buzz 60%/100% (#49/#47) when spinning fast
 *  ③ Braking          — Long Buzz (#118) on sudden stop
 *  ④ Heartbeat        — Double Click (#10) every 4s idle
 *
 *  NOTE: ESP-IDF LCD headers are in lcd_driver.c (pure C).
 *        This avoids the esp_lcd_io_i2c.h conflict with Wire.h.
 * ═══════════════════════════════════════════════════════════════
 */

// ── LCD driver (ESP-IDF wrapped in pure C — no conflicts!) ────
#include "lcd_driver.h"

// ── Haptic driver (Adafruit DRV2605 Arduino library) ─────────
#include <Adafruit_DRV2605.h>
#include <Wire.h>


Adafruit_DRV2605 drv;
bool drvOK = false;

// ─── Pin Definitions ──────────────────────────────────────────
#define LCD_BL 47
#define POWER_EN 5

#define DRV_SDA 11 // DRV2605 I2C — different from touch I2C!
#define DRV_SCL 12

#define ENC_A 9
#define ENC_B 10
#define ENC_SW 8

#define LCD_W 360
#define LCD_H 360

// ─── DRV2605 Effect IDs ───────────────────────────────────────
#define HAPTIC_CLICK 6        // Sharp Click 30%
#define HAPTIC_INERTIA_MED 49 // Buzz 60%
#define HAPTIC_INERTIA_MAX 47 // Buzz 100%
#define HAPTIC_BRAKE 118      // Long Buzz (programmatic stop)
#define HAPTIC_HEARTBEAT 10   // Double Click 100%

// ─── Line buffer for drawing ──────────────────────────────────
static uint16_t lineBuf[LCD_W];

// ─── Haptic helper (Adafruit uses go(), NOT run()) ────────────
void hapticPlay(uint8_t effectID) {
  if (!drvOK)
    return;
  drv.setWaveform(0, effectID);
  drv.setWaveform(1, 0); // terminate sequence
  drv.go();              // ← Adafruit API is go(), not run()
}

// ─── Startup greeting: Strong Click + Soft Bump ───────────────
void hapticGreeting() {
  if (!drvOK)
    return;
  drv.setWaveform(0, 1);
  drv.setWaveform(1, 0);
  drv.go();
  delay(200);
  drv.setWaveform(0, 7);
  drv.setWaveform(1, 0);
  drv.go();
}

// ─── RGB565 helper (byte-swapped for QSPI) ───────────────────
static inline uint16_t rgb565(uint8_t r, uint8_t g, uint8_t b) {
  uint16_t c =
      ((uint16_t)(r & 0xF8) << 8) | ((uint16_t)(g & 0xFC) << 3) | (b >> 3);
  return (c >> 8) | (c << 8);
}

// ─── Fill entire screen with one color ────────────────────────
void fillScreen(uint16_t color) {
  for (int x = 0; x < LCD_W; x++)
    lineBuf[x] = color;
  for (int y = 0; y < LCD_H; y++)
    lcd_draw_row(y, lineBuf, LCD_W);
}

// ─── Color bar test pattern ───────────────────────────────────
void drawColorBars() {
  uint16_t colors[8] = {rgb565(255, 0, 0),     rgb565(0, 255, 0),
                        rgb565(0, 0, 255),     rgb565(255, 255, 0),
                        rgb565(0, 255, 255),   rgb565(255, 0, 255),
                        rgb565(255, 255, 255), rgb565(0, 0, 0)};
  for (int x = 0; x < LCD_W; x++)
    lineBuf[x] = colors[x * 8 / LCD_W];
  for (int y = 0; y < LCD_H; y++)
    lcd_draw_row(y, lineBuf, LCD_W);
}

// ─── Cyan→green gradient ──────────────────────────────────────
void drawGradient() {
  for (int y = 0; y < LCD_H; y++) {
    uint8_t g = (uint8_t)(y * 255 / LCD_H);
    uint16_t c = rgb565(0, g, 255 - g);
    for (int x = 0; x < LCD_W; x++)
      lineBuf[x] = c;
    lcd_draw_row(y, lineBuf, LCD_W);
  }
}

// ─── Patterns ────────────────────────────────────────────────
#define NUM_PATTERNS 5
int currentPattern = 0;

void drawPattern(int p) {
  const char *names[] = {"FULL RED", "FULL GREEN", "FULL BLUE", "COLOR BARS",
                         "GRADIENT"};
  Serial.printf("-> Pattern %d: %s\n", p, names[p]);
  switch (p) {
  case 0:
    fillScreen(rgb565(255, 0, 0));
    break;
  case 1:
    fillScreen(rgb565(0, 255, 0));
    break;
  case 2:
    fillScreen(rgb565(0, 0, 255));
    break;
  case 3:
    drawColorBars();
    break;
  case 4:
    drawGradient();
    break;
  }
}

// ─── Encoder ──────────────────────────────────────────────────
int encoderPos = 0;
int lastEncA = HIGH;
unsigned long lastEncTime = 0;
#define ENC_DEBOUNCE_MS 8

void updateEncoder() {
  if (millis() - lastEncTime < ENC_DEBOUNCE_MS)
    return;
  int a = digitalRead(ENC_A);
  if (a != lastEncA) {
    lastEncA = a;
    if (a == LOW) {
      encoderPos += (digitalRead(ENC_B) == HIGH) ? +1 : -1;
    }
    lastEncTime = millis();
  }
}

// ─── Haptic State ─────────────────────────────────────────────
#define SPEED_WINDOW_MS 100
#define INERTIA_THRESH_MED 6
#define INERTIA_THRESH_MAX 14
#define BRAKE_IDLE_MS 130
#define HEARTBEAT_PERIOD_MS 4000

struct {
  unsigned long windowStart = 0;
  int stepsInWindow = 0;
  int lastSpeed = 0;
  bool wasSpinning = false;
  bool brakeFired = false;
  unsigned long lastMoveTime = 0;
  unsigned long lastHeartbeat = 0;
} h;

// ─── Haptic update ────────────────────────────────────────────
void updateHaptics(int delta) {
  unsigned long now = millis();

  // Refresh speed window
  if (now - h.windowStart >= SPEED_WINDOW_MS) {
    h.lastSpeed = h.stepsInWindow;
    h.stepsInWindow = 0;
    h.windowStart = now;
  }

  if (delta != 0) {
    h.stepsInWindow += abs(delta);
    h.lastMoveTime = now;
    h.brakeFired = false;

    // ① Click or ② Inertia
    if (h.lastSpeed >= INERTIA_THRESH_MAX) {
      hapticPlay(HAPTIC_INERTIA_MAX);
      Serial.println("[HAP] INERTIA MAX");
      h.wasSpinning = true;
    } else if (h.lastSpeed >= INERTIA_THRESH_MED) {
      hapticPlay(HAPTIC_INERTIA_MED);
      Serial.println("[HAP] INERTIA MED");
      h.wasSpinning = true;
    } else {
      hapticPlay(HAPTIC_CLICK);
      Serial.println("[HAP] click");
    }
    h.lastHeartbeat = now;
  }

  // ③ Braking — once when stopping after spin
  if (h.wasSpinning && !h.brakeFired &&
      (now - h.lastMoveTime) >= BRAKE_IDLE_MS) {
    hapticPlay(HAPTIC_BRAKE);
    Serial.println("[HAP] BRAKE");
    h.wasSpinning = false;
    h.brakeFired = true;
    h.lastHeartbeat = now;
  }

  // ④ Heartbeat — idle pulse every 4 seconds
  if (!h.wasSpinning && (now - h.lastHeartbeat) >= HEARTBEAT_PERIOD_MS) {
    hapticPlay(HAPTIC_HEARTBEAT);
    Serial.println("[HAP] heartbeat 💓");
    h.lastHeartbeat = now;
  }
}

// ─── setup() ──────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n=== SH8601 AMOLED + DRV2605 Haptics ===");

  // 1. Board power
  pinMode(POWER_EN, OUTPUT);
  digitalWrite(POWER_EN, HIGH);
  delay(200);

  // 2. Backlight OFF during init
  pinMode(LCD_BL, OUTPUT);
  digitalWrite(LCD_BL, LOW);

  // 3. Encoder pins
  pinMode(ENC_A, INPUT_PULLUP);
  pinMode(ENC_B, INPUT_PULLUP);
  pinMode(ENC_SW, INPUT_PULLUP);
  lastEncA = digitalRead(ENC_A);

  // 4. DRV2605 — I2C on SDA=11, SCL=12
  Wire.begin(DRV_SDA, DRV_SCL);
  if (drv.begin()) {
    drv.selectLibrary(1);              // ERM library
    drv.setMode(DRV2605_MODE_INTTRIG); // triggered via go()
    drvOK = true;
    Serial.println("DRV2605 OK");
  } else {
    Serial.println("DRV2605 NOT FOUND — haptics disabled");
  }

  // 5. LCD (ESP-IDF init in lcd_driver.c — no header conflicts)
  lcd_driver_init();
  Serial.println("Display OK");

  // 6. First frame + backlight on
  drawPattern(currentPattern);
  delay(50);
  digitalWrite(LCD_BL, HIGH);

  // 7. Haptic greeting
  hapticGreeting();

  // 8. Init timers
  h.windowStart = millis();
  h.lastHeartbeat = millis();

  Serial.println("Ready! Encoder=cycle patterns | Serial 0-4=pattern");
}

// ─── loop() ───────────────────────────────────────────────────
void loop() {
  static int lastPos = 0;
  updateEncoder();

  int delta = encoderPos - lastPos;
  if (delta != 0) {
    currentPattern =
        ((currentPattern + delta) % NUM_PATTERNS + NUM_PATTERNS) % NUM_PATTERNS;
    lastPos = encoderPos;
    drawPattern(currentPattern);
  }

  updateHaptics(delta);

  if (Serial.available()) {
    char c = Serial.read();
    if (c >= '0' && c <= '4') {
      currentPattern = c - '0';
      drawPattern(currentPattern);
      hapticPlay(HAPTIC_CLICK);
    }
  }
}
