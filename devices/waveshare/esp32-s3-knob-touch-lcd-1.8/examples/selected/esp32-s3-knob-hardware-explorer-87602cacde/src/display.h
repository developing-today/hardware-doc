/*
 * display.h — Display- und LVGL-Initialisierung
 * Waveshare ESP32-S3 Knob Touch LCD 1.8 (ST77916, 360x360, QSPI)
 */
#pragma once

#include <Arduino.h>

/**
 * @brief Display + LVGL initialisieren.
 *
 * - Setzt QSPI Bus + ST77916 Panel via Arduino_GFX auf
 * - Aktiviert LCD-Backlight
 * - Initialisiert LVGL v9 mit Strip-Buffer (ein Streifen 360x40 in PSRAM)
 * - Registriert flush_cb und tick_cb
 *
 * @return true wenn alles geklappt hat, false bei Fehler
 */
bool display_init();

/**
 * @brief LVGL-Timer-Handler aufrufen — muss regelmaessig laufen!
 *
 * Aufrufen alle ~5-10 ms aus loop() oder einer Task.
 */
void display_tick();

/**
 * @brief Mini-UI bauen: Label "Hello LVGL!" zentriert mit Smiley.
 *
 * Nur fuer den ersten v0.4-Test. Spaeter kommt hier richtige UI hin.
 */
void display_show_hello();

/**
 * @brief Reines Arduino_GFX Test-Pattern (ohne LVGL!).
 *
 * Zeigt nacheinander Vollflaechen-Farben + Streifen + Text.
 * Dient zur Diagnose: wenn das nicht klappt, liegt's am Display-Treiber,
 * nicht am LVGL-Glue.
 *
 * MUSS NACH display_init() aufgerufen werden.
 */
void display_test_pattern();

/**
 * @brief LVGL-Tick aktivieren (erst NACH allen Tests).
 * Vorher meidet display_tick() die LVGL-Aufrufe, damit kein Race
 * mit display_test_pattern() entsteht.
 */
void display_enable_lvgl();
