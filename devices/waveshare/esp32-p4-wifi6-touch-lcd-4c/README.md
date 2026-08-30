# Waveshare ESP32-P4-WIFI6-Touch-LCD-4C

> 4-inch 720 × 720 round capacitive-touch ESP32-P4 development board. **On sale as SKU 31522**,
> under the shared product listing. Research retrieved **2026-08-24**.

- **Manufacturer:** Waveshare
- **SoC:** [ESP32-P4NRW32](../../../components/espressif/esp32-p4/README.md)
- **Status:** **current, purchasable** — SKU **31522**, sold as a Version Option
- **Sibling:** [ESP32-P4-WIFI6-Touch-LCD-3.4C](../esp32-p4-wifi6-touch-lcd-3.4c/README.md) — same PCB, SKU 31523, 3.4 in / 800 × 800

## Availability — it is on sale

**The 4C is a normal, purchasable Waveshare product.** Both variants are sold under **one listing**
via a *Version Options* selector:

| SKU | Variant | Saleable |
|---|---|---|
| 31523 | 3.4C — 3.4in, 800 × 800 | yes |
| **31522** | **4C — 4in, 720 × 720** | **yes** |

Buy it at <https://www.waveshare.com/esp32-p4-wifi6-touch-lcd-3.4c.htm> and select
**"4inch Round Touch Display (720 × 720 pixels)"** under Version Options. The listing spans
**$64.99 – $74.99** across the two variants.

> Yes, the URL says `3.4c`. That is the shared listing for both. There is no separate 4C page, and
> its absence is not evidence of anything — an earlier pass of this research briefly concluded the
> 4C might not exist on exactly that mistaken basis. See
> [C2](../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c2--4c-availability--resolved-2026-08-24).

> **Unresolved:** which of $64.99 / $74.99 applies to the 4C. Per-option pricing is rendered
> client-side and was not extractable. Check at purchase.

Waveshare also ship first-class software support: a dedicated CI-built factory image
`ESP32-P4-WIFI6-Touch-LCD-4C-FactoryOnly-260821.bin`, a `sdkconfig.defaults.4c` build profile, and
a `BSP_LCD_TYPE_720_720_4_INCH` macro in the published BSP.

## Why it is still worth documenting

Waveshare ships **first-class software support for it**. The shared demo archive contains
`07_displaypanel_4inch`, a complete, working JD9365 initialisation and DSI timing set for the
720 × 720 panel, sitting beside the 3.4C's. Waveshare's Arduino board library exposes it as a
compile-time option:

```c
#define SCREEN_3INCH_4_DSI 1
#define SCREEN_4INCH_DSI   2
#ifndef CURRENT_SCREEN
#define CURRENT_SCREEN SCREEN_3INCH_4_DSI      // 3.4C is the default
#endif
```

So the 4C configuration is a supported, selectable target in the vendor's own code even though the
board is not in the store. That makes this record useful in two concrete ways: as a reference for
anyone who **has** one, and as a documented 720 × 720 JD9365 profile for anyone driving a similar
round DSI panel from a P4.

## Specifications

Identical to the [3.4C](../esp32-p4-wifi6-touch-lcd-3.4c/README.md#key-specifications) in every
respect except the display. The wiki feature lists for the two boards are word-for-word the same
apart from the display sentence. Rather than duplicate the table, see the
[shared platform record](../esp32-p4-wifi6-touch-lcd-xc-shared/README.md#board-architecture).

### What is actually different

| Parameter | 4C | 3.4C |
|---|---|---|
| Panel diagonal | **4.0 in** | 3.4 in |
| Active area | **720 × 720** | 800 × 800 |
| Pixel density | **~255 ppi** (derived) | ~333 ppi (derived) |
| JD9365 init reg `0x40` | **`0x04`** | `0x00` |
| Controller, lanes, lane rate, porches | JD9365, 2 lane, 1500 Mbps, pw20/bp20/fp40 · pw4/bp12/fp24 | **identical** |

Pixel densities are **derived arithmetic**, not vendor figures: 720 ÷ (4.0 in) and 800 ÷ (3.4 in)
along the diameter. They are included because they capture the real trade-off the user asked
about — the 4C is the *larger, coarser* panel. Content designed pixel-exact for one will not
transfer to the other.

Everything else — porches, lane rate, reset and backlight GPIOs, I²C, I²S, amplifier enable — is
byte-identical between the two variants' code. Full analysis:
[shared record](../esp32-p4-wifi6-touch-lcd-xc-shared/README.md#what-is-genuinely-shared-vs-per-variant).

## Pin map

Identical to the 3.4C. See the
[verified pin map](../esp32-p4-wifi6-touch-lcd-xc-shared/README.md#verified-pin-map), including
the **unresolved microSD pins** warning.

## Getting the display up

Use `artifacts/demo/ESP-IDF/07_displaypanel_4inch/` from the
[shared record](../esp32-p4-wifi6-touch-lcd-xc-shared/README.md) — **07**, not 06. For Arduino,
define `CURRENT_SCREEN SCREEN_4INCH_DSI` before including Waveshare's `displays_config.h`;
the library defaults to the 3.4C and will otherwise configure 800 × 800 on a 720 × 720 panel.

```c
#define CURRENT_SCREEN SCREEN_4INCH_DSI
#include "displays_config.h"
```

That default is a genuine trap for 4C owners: a stock build silently targets the wrong resolution.

## Common tasks / How do I...?

All feature guides are shared with the 3.4C, since the hardware is otherwise identical:

| Task | Guide |
|---|---|
| Drive the round display | [`features/display.md`](./features/display.md) |
| Read touch input | [3.4C `features/touch.md`](../esp32-p4-wifi6-touch-lcd-3.4c/features/touch.md) |
| Wi-Fi 6 / Bluetooth | [3.4C `features/wifi-and-bluetooth.md`](../esp32-p4-wifi6-touch-lcd-3.4c/features/wifi-and-bluetooth.md) |
| Audio | [3.4C `features/audio.md`](../esp32-p4-wifi6-touch-lcd-3.4c/features/audio.md) |
| Camera | [3.4C `features/camera.md`](../esp32-p4-wifi6-touch-lcd-3.4c/features/camera.md) |
| microSD | [3.4C `features/storage.md`](../esp32-p4-wifi6-touch-lcd-3.4c/features/storage.md) |
| Build and flash | [3.4C `development.md`](../esp32-p4-wifi6-touch-lcd-3.4c/development.md) |

Only [`features/display.md`](./features/display.md) is maintained separately here, because the
display is the only hardware difference.

## Shortcomings and constraints

Inherits every constraint of the [3.4C](../esp32-p4-wifi6-touch-lcd-3.4c/README.md#shortcomings-and-constraints), plus:

- **Not purchasable** through Waveshare's store as of 2026-08-24.
- **Community is smaller than the 3.4C's, but real.** Confirmed 4C projects:
  [`fabkury/p3a`](https://github.com/fabkury/p3a) (89★, Apache-2.0, actively maintained) and
  [`Alex-developer/ADSB-Radar`](https://github.com/Alex-developer/ADSB-Radar) (MIT), both selecting
  `CONFIG_BSP_LCD_TYPE_720_720_4_INCH=y`. An earlier pass wrongly recorded zero — it was searching
  product names, which nobody uses.
- **Lower pixel density** than the 3.4C on a physically larger panel.
- Vendor Arduino library **defaults to the 3.4C**, so 4C builds need an explicit override.

## Evidence status

Vendor documentation, vendor source code and the live store listing, retrieved 2026-08-24.
**No hardware and no photograph of a real unit here.** But commercial availability is confirmed
from the listing's own SKU data, and **at least two independent projects build for this exact
variant** — so units are in people's hands. Display parameters are well-evidenced from Waveshare's
shipped code.

## Related

- [ESP32-P4-WIFI6-Touch-LCD-3.4C](../esp32-p4-wifi6-touch-lcd-3.4c/README.md) — buy this one
- [Shared XC platform](../esp32-p4-wifi6-touch-lcd-xc-shared/README.md)
- [Waveshare vendor guide](../../../vendors/waveshare/README.md)
