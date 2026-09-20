# X4 Pro — microSD storage

> Native SDMMC, 1-bit. **Not SPI** — an SPI card path can never work on this
> board. Evidence: hardware-confirmed. Last verified 2026-09-04.

## Capability summary

| Signal | GPIO |
|---|---:|
| CLK | **41** |
| CMD | **42** |
| DAT0 | **40** |
| power enable | **5** — **ACTIVE-LOW** |

Slot 1, 1-bit, internal pull-ups, 40 MHz. DAT1/2/3 unused.
Driver: `esp_driver_sdmmc` via `SdmmcBlockDevice`.
Component: [`generic/micro-sd-sdmmc`](../../../../components/generic/micro-sd-sdmmc/)

## Build requirement

`FREEINK_SD_SDMMC` auto-enables with `-DFREEINK_DEVICE_X4PRO=1`, **but the
consumer build must also define `USE_BLOCK_DEVICE_INTERFACE=1`** — SdFat needs its
generic block-device interface for the `FsVolume` mount. The `x4pro` env defines
it; a hand-rolled env that omits it compiles and then fails to mount.

## The mount sequence — both steps are required

From the OEM `mountSD`, reproduced in `SdmmcBlockDevice::begin`:

1. **Power-cycle GPIO5 and retry the WHOLE mount.** Before each attempt, pulse
   GPIO5 HIGH (80 ms) → LOW (120 ms), then run `sdmmc_card_init` **and a real
   sector-0 read**.
   *Why:* retrying only `card_init` leaves SdFat's first, un-retried block read to
   hit a still-marginal data path and fail with
   `sdmmc_read_sectors_dma … 0x107`. Validating a real read before publishing the
   card means the retry actually covers block I/O.
2. **Leave GPIO5 LOW.** Driving it HIGH after init — an earlier misreading of the
   OEM — breaks **every** subsequent read with `0x107`. It must stay in the state
   the validated read succeeded under.

## DMA buffering

Reads and writes bounce through a `MALLOC_CAP_DMA` buffer, because SdFat's caches
may live in **PSRAM** or be unaligned. This is a real constraint on an 8 MB-PSRAM
board and is easy to get wrong.

## Sleep

The enable is active-LOW, so the sleep path drives GPIO5 **HIGH** to cut the card.
`powerActiveHigh = false` makes `powerDownRailsForSleep()` do this by polarity.

## Pitfalls

| Symptom | Cause |
|---|---|
| Card silent to CMD0 | You are trying SPI mode. Use SDMMC |
| Every read fails `0x107` | GPIO5 held HIGH |
| First read after mount fails | Retrying `card_init` only, not the full mount |
| Mounts but data corrupt | Missing the DMA bounce buffer |

## Status

`hardware-confirmed` — *"CONFIRMED WORKING on hardware."*
