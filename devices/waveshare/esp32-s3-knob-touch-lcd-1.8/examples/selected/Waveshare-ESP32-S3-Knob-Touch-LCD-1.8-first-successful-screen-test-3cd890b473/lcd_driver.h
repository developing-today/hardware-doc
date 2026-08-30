/*
 * lcd_driver.h
 * Pure C interface for SH8601 AMOLED display.
 * Keeps ESP-IDF headers isolated from Arduino C++ headers.
 */
#pragma once
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Initialize the SH8601 display over QSPI at 40 MHz */
void lcd_driver_init(void);

/* Draw a horizontal line of pixels (used for full-screen fills) */
void lcd_draw_row(int y, uint16_t *pixels, int width);

/* Draw an arbitrary bitmap region */
void lcd_draw_bitmap(int x1, int y1, int x2, int y2, uint16_t *data);

#ifdef __cplusplus
}
#endif
