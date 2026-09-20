# Xteink X4 — compatibility and status

Snapshot **2026-09-04**.

## Working

Display (both clock modes), ADC ladder buttons, power button, microSD over shared
SPI, battery ADC, USB-C flashing, Wi-Fi, BLE. This is the **most-exercised device
in the family** — ~200 repositories, most of which target it first.

## Partial / risky

| Item | State |
|---|---|
| **40 MHz panel overclock** | Works, is **2× datasheet**, and *"can glitch plane writes on marginal wiring"*. Per-unit validation required |
| **GPIO13 power latch** | Behaviour depends on an **unmarked board revision**. Firmware that omits the assert works on most units and is unusable on others |
| **Deep sleep** | The SD card **cannot be powered down** — there is no enable pin |
| **OTA** | Documented to fail with out-of-memory on this SoC class |

## Known failures with named cures

| Failure | Version | Cure |
|---|---|---|
| Stuck after OTA fails at `esp_ota_end()` | CrossPoint **1.2.0** | [`togotago/xteink-x4-escape`](https://github.com/togotago/xteink-x4-escape) |
| OTA update problems | CrossPoint **1.4.0** | *"reflash from the website if you're unlocked or SD flash if you're locked"* — [r/XTEINK `1uek163`](https://old.reddit.com/r/XTEINK/comments/1uek163/) |
| Soft-brick on locked units | Forks on a stale SDK | Pull the latest SDK — CrossPoint 1.5 release note |
| Blank display on a newer unit | Firmware without UC8179/UC8279 drivers | Use a firmware carrying the boot probe |

## Not implemented

USB-MSC (not documented for this device), grayscale (1 bpp only).

## Hardware-revision keyed

Two known axes of variation, **neither externally visible**:

1. **Power latch:** self-latching vs not (at least two revisions).
2. **Panel controller:** SSD1677 vs UC8179 vs UC8279.

**No revision marking scheme is known for either.** Compatibility statements
cannot be keyed to a revision, only to firmware behaviour that handles both.

## Lifecycle status

**Discontinued.** Delisted from the vendor store; all accessories sold out as of
2026-09-04. Firmware support remains **very active** — this is a case where
community support outlives vendor availability.
