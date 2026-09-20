/* Local build-experiment shim: AVR/ESP pgmspace API on a native host.
   NOT upstream. Provides the handful of symbols PNGdec/JPEGDEC expect. */
#pragma once
#include <string.h>
#include <stdint.h>
#ifndef PROGMEM
#define PROGMEM
#endif
static inline void *memcpy_P(void *d, const void *s, size_t n) { return memcpy(d, s, n); }
#ifndef pgm_read_byte
static inline uint8_t pgm_read_byte(const void *p) { return *(const uint8_t *)p; }
#endif
