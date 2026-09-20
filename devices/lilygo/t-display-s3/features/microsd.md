# T-Display-S3 — microSD

## There is no microSD slot on this board

The `pin_config.h` files define:

```c
/* External expansion */
#define PIN_SD_CMD    13
#define PIN_SD_CLK    11
#define PIN_SD_D0     12
```

and the comment `/* External expansion */` is doing a lot of work. LilyGO states it plainly:

> "SD card pins (SD CMD/CLK/D0) are only available on boards with the SD Shield add-on. The
> standard T-Display-S3 board does not have an onboard SD card slot."
> — `README.md` @ `ec889e789b3cf093412689a143f7f37b42b56af7`

The designator census of `schematic/T_Display_S3.pdf` confirms it: no card-socket designator
appears anywhere on the sheet.

## The T-Display TF Shield

| | |
|---|---|
| Product | **T-Display TF Shied** [sic], store handle `t-display-tf-shied` |
| SKUs | `H609` (pin header) **USD 2.51** · `H610` (female header) **USD 2.38**, both in stock 2026-09-07 |
| Interface | **1-bit SDMMC**: `CMD` GPIO13, `CLK` GPIO11, `D0` GPIO12 |
| Mechanical drawing | `dimensions/SD-Shield.DXF` in the board repo @ `ec889e7` |
| Vendor example | `examples/sd/` |
| Component record | [`generic/micro-sd-sdmmc`](../../../../components/generic/micro-sd-sdmmc/README.md) |

1-bit, not 4-bit. Expect a few MB/s, not tens.

```cpp
#include "SD_MMC.h"
SD_MMC.setPins(11 /*CLK*/, 13 /*CMD*/, 12 /*D0*/);
if (!SD_MMC.begin("/sdcard", true /* 1-bit mode */)) { /* … */ }
```

The `true` is mandatory — it selects 1-bit mode. Omitting it makes the driver look for D1–D3
that are not wired.

## If you do not fit the shield

GPIO11, 12 and 13 are **free** and are the most useful spare pins on the board, because they
are RTC-capable, ADC2-capable and physically adjacent on the header. Given how few pins remain
after the LCD bus and the PSRAM, that matters — see
[`gpio-and-expansion.md`](gpio-and-expansion.md).

## Alternative

An SPI microSD breakout on any three free pins works and avoids the shield. It is slower than
1-bit SDMMC but not dramatically so at these speeds, and it frees you from the shield's
mechanical footprint.
