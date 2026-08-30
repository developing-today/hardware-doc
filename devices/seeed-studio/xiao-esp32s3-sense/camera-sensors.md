# Camera sensors of the XIAO ESP32S3 Sense

> Three sensors are (or were) sold for the J3 daughterboard: **OV2640** (discontinued),
> **OV3660** (current default), **OV5640** (paid upgrade). Which one a given unit has
> cannot be determined from the SKU or packaging — read it back at runtime.
> Research pass **2026-08-24**, sources listed at the bottom; community-sourced numbers are flagged.

---

## TL;DR comparison

| | OV2640 | OV3660 ← *what new units ship with* | OV5640 |
|---|---|---|---|
| Status | **Discontinued** (pre-2025-06 units) | **Current** | Sold separately as upgrade |
| Array | 1600 × 1200 (**UXGA**, 2 MP) | 2048 × 1536 (**QXGA**, 3 MP) | 2592 × 1944 (**QSXGA/5MP**) |
| Optical format | 1/4″ | **1/5″** | 1/4″ |
| Pixel size | 2.2 µm (datasheet) | ≈2 µm (*computed from format*) | 1.4 µm (datasheet) |
| Max framesize in driver | `FRAMESIZE_UXGA` | `FRAMESIZE_QXGA` | `FRAMESIZE_QSXGA` |
| JPEG output | Yes (on-chip) | Yes (`support_jpeg = true`) | Yes (on-chip) |
| Typical fps | ~30 @ VGA, ~15 @ 720p ᶜ | ~60 @ VGA, **45 @ 720p**, 8 @ QXGA ᶜ | ~90 @ VGA, 30 @ 720p, 5 @ QSXGA ᶜ |
| Autofocus | No | No | **Optional AF variant** (sold by Seeed with AF) |
| Low light | Average | **Good** (newer fab generation) ᶜ | Average |
| Heat | Fine | Fine (lower power than OV2640) | Runs hot — ships with heatsinks |
| SCCB address | 0x30 | 0x3C | 0x3C |
| PID (`id.PID`) | **0x26** | **0x3660** | **0x5640** |

ᶜ community-measured figures ([espboards.dev comparison]), not vendor-datasheet numbers. Treat as indicative.

## Is the bigger number just more pixels?

No. What actually changes between these parts:

1. **Pixel size ≠ equal.** More megapixels on the same optical format means *smaller*
   pixels: the OV5640's 1.4 µm pixels collect less light per pixel than the 2.2 µm
   pixels of the OV2640. Resolution up, per-pixel sensitivity down. The OV3660 pairs
   its 3 MP with a smaller 1/5″ format but a newer process node, which is why the
   community consistently reports better real-world low-light behavior than the OV2640
   despite the nominally similar ~2 µm pixel.
2. **Frame rate falls off differently per part.** At 720p the OV3660 is the fastest of
   the three (~45 fps ᶜ); at full resolution all of them slow to single digits
   (OV3660 ~8 fps @ QXGA, OV5640 ~5 fps @ full 5 MP ᶜ).
3. **JPEG handling differs in cost.** All three can emit compressed data through
   `esp32-camera`, so streaming works without software compression either way — but
   quality/latency characteristics differ, and if you request raw RGB565 instead,
   PSRAM bandwidth becomes your bottleneck (driver README warns frame corruption under
   Wi-Fi load in raw modes).
4. **Register maps are incompatible.** Any code poking sensor registers directly
   (`sccb` reads/writes beyond the `sensor_t` abstraction) will not port across the
   three. Stick to the function pointers in `sensor_t`.
5. **Autofocus exists only on the OV5640 option** (voice-coil-motor variant). Fixed
   focus elsewhere; focus distance set by the lens holder.

## Which one do I actually have?

```c
#include "esp_camera.h"

// after esp_camera_init() succeeds:
sensor_t *s = esp_camera_sensor_get();
switch (s->id.PID) {
    case 0x26:   /* OV2640_PID */  printf("OV2640 (discontinued stock)\n"); break;
    case 0x3660: /* OV3660_PID */  printf("OV3660 (current stock)\n");     break;
    case 0x5640: /* OV5640_PID */  printf("OV5640 (upgrade)\n");           break;
    default:                       printf("unknown: 0x%x\n", s->id.PID);
}
```

PIDs from [`driver/include/sensor.h`](https://github.com/espressif/esp32-camera/blob/master/driver/include/sensor.h)
(`camera_pid_t`); addresses and `support_jpeg` flags from `driver/sensor.c`
(`camera_sensor_info_t`). The probe order in `camera_probe()` tries each supported
driver against the detected PID automatically, so `esp_camera_init()` needs no
per-sensor configuration on this board.

## Requesting resolutions above the fitted sensor's maximum

The driver clamps rather than fails: setting `FRAMESIZE_QXGA` on an OV2640 yields its
UXGA ceiling. A single code path written for QXGA works across all three sensors —
this is why Seeed could keep the wiki examples unchanged through the transition.

## Power (vendor-published, product page 2026-08-24)

Sense-specific operating figures from Seeed's spec table:

| Scenario | Type-C (5 V) | Battery (3.8 V) |
|---|---|---|
| Webcam web app — average | ~140 mA | ~155 mA |
| Webcam web app — peak (image capture) | ~347 mA | ~366 mA |
| Mic recording + SD write — average | 54.58 mA | 64.5 mA |
| Mic recording + SD write — peak | 86.7 mA | 109.3 mA |

Low-power modes (3.8 V supply): modem-sleep **44 mA**, light-sleep **5 mA**,
deep sleep **3 mA** ⚠ — that deep-sleep figure is almost certainly wrong (it equals
the modem/light-sleep scale, not sleep; the non-Sense XIAO ESP32S3 page states
**14 µA**). This is the third inconsistent deep-sleep number seen in Seeed materials —
see [gaps-and-conflicts.md §4](gaps-and-conflicts.md#4-seeeds-own-spec-table-gives-two-different-deep-sleep-figures-for-the-sense).
Plan around tens of µA and measure on hardware.

Note these figures predate the sensor change (measured against OV2640-era units);
the OV3660's lower power draw should make them slightly pessimistic, but no revised
numbers have been published.

## Swapping sensors

All three modules use the same ribbon connector to the J3 daughterboard carrier, and
the carrier's DVP wiring is identical — swapping modules is electrically trivial.
The mechanical catch is the OV5640 upgrade kit: taller module + required heatsinks.

## Resources

- [espressif/esp32-camera](https://github.com/espressif/esp32-camera) — the driver this
  board actually uses; per-sensor drivers live in `drivers/sensors/{ov2640,ov3660,ov5640}.c`,
  capability tables in `README.md`, PIDs/max-framesizes in `driver/{include/sensor.h,sensor.c}`
- [DeepWiki: esp32-camera sensor drivers](https://deepwiki.com/espressif/esp32-camera/3.2-camera-sensor-drivers) —
  generated cross-reference of driver capabilities incl. SCCB addresses
- [espboards.dev: ESP32 camera modules compared](https://www.espboards.dev/blog/esp32-camera-modules-compared/) —
  community fps/low-light measurements behind the ᶜ flags above
- Seeed wiki — XIAO ESP32S3 Series (OV2640-discontinuation statement) and
  *PCN XIAO ESP32-S3 Sense Series Camera Upgrade* PDF (2025-06-30 change record)
- OmniVision datasheets are NDA-gated; public register-level documentation effectively
  means reading the esp32-camera driver sources themselves. Linux-kernel ports
  (`drivers/media/i2c/ov5640.c`, `ov2640.c`) are a second usable register reference.

## Sourcing notes

Vendor-published: resolution/optical-format rows (esp32-camera README mirrors
OmniVision briefs), power table (Seeed product page, archived 2026-08-24).
Community: fps figures, low-light rankings. Computed: OV3660 pixel size from 1/5″
format. Not verified on physical hardware: everything here was gathered from documents;
no unit was probed during this research pass.
