# Xteink X4 Classic — development

> ESP32-S3, 16 MB flash, 8 MB PSRAM. Retrieval **2026-09-04**.
> **Nothing executed against hardware — and, unlike the other models, nobody
> appears to own one outside China.**

## Toolchain

| Item | Value | Status |
|---|---|---|
| Framework | Arduino-ESP32 under PlatformIO | `reported-working` |
| Board | `esp32-s3-devkitc1-n16r8` | `reported-working` **[SDK]** |
| MCU | `board_build.mcu = esp32s3` | `reported-working` |
| Build flag | `-DFREEINK_DEVICE_X4CLASSIC=1` | `reported-working` |
| Also required | **`-DUSE_BLOCK_DEVICE_INTERFACE=1`** in the consumer build | `reported-working` |
| esptool chip | `esp32s3` | `inferred` |
| Stock firmware | `xteink_app` **v7.0.11** | **[DUMP]** |

```ini
[env:x4c]
extends = base
board = esp32-s3-devkitc1-n16r8  ; 16 MB flash + 8 MB PSRAM
board_build.mcu = esp32s3
build_flags =
  ${base.build_flags}
  -DBOARD_HAS_PSRAM
  ; SD is 1-bit SDMMC (FREEINK_SD_SDMMC auto-enables); SdFat needs its generic
  ; block-device interface for the FsVolume mount:
  -DUSE_BLOCK_DEVICE_INTERFACE=1
  -DFREEINK_DEVICE_X4CLASSIC=1
```
Verbatim from `platformio.sample.ini` at commit `2400379`.

**Auto-enabled:** `FREEINK_DRIVER_SSD1677`, `FREEINK_DRIVER_UC8179`,
`FREEINK_DRIVER_UC8279_X4`, `FREEINK_CAP_RTC`, `FREEINK_BATTERY_I2C_GAUGE`,
`FREEINK_SD_SDMMC`.
**Left off:** `FREEINK_CAP_TOUCH`, `FREEINK_CAP_FRONTLIGHT`.

## Build / flash / monitor

```bash
pio run -e x4c                 # inferred
pio run -e x4c -t upload       # inferred
pio device monitor -b 115200   # inferred
```

## Bricking risks — one is specific to this device and severe

| Risk | Note |
|---|---|
| **🔴 Restoring a full-flash image from another unit** | **X4C-specific and the worst risk in the family.** The panel controller is selected **only** from NVS `hw_calib/screenType`, which the factory writes once. There is **no MISO**, so there is no live probe to override a wrong value. A full-flash restore from a different unit overwrites `hw_calib` and can leave the device driving the wrong controller **with no way to detect it**. On every other Xteink, the boot probe silently corrects this. **Preserve NVS, or restore only your own image.** |
| Wrong display pins when porting from the X4 Pro | DC/RST/BUSY are permuted (14/10/18 vs 18/14/6). Symptom: resets and runs waveforms, never develops an image |
| Treating GPIO2/5/8/9 as rails or PWM | They are **buttons** here and rails/frontlight on the X4 Pro |
| Probing GPIO19/20 | Native USB D−/D+ |
| Holding GPIO0 at reset | Side-Left button **and** boot strap |
| Repurposing GPIO4 | Role unknown; the stock firmware configures it as an input for a reason nobody has identified |
| Stale fork on a locked unit | Family-wide; CrossPoint 1.5 warns about soft-bricking locked units |

## USB lock

**Not established for this model.** The X3, X4 and X4 Pro all ship USB-locked on
many units, and the same unlock paths (crosspointreader.com OTA unlock; SD-card
`update.bin` with Power+Up at boot; a vendor-sold developer-unlocked variant)
would be expected to apply. **No X4C owner report exists to confirm any of it.**
Treat the whole procedure as `inferred` on this device.

See [`../x4-pro/development.md`](../x4-pro/development.md#usb-lock) for what is
known family-wide.

## Debug access

Native S3 **USB-OTG** on GPIO19/20, USB-CDC. **USB-MSC capable per the SDK** —
which is more than the X4 Pro, where MSC exists in stock but has not been ported.
No exposed header, no test points documented, no teardown to look for pads.

## What you cannot do here

- **No touch.** Stock instantiates `NoTouchDriver`.
- **No frontlight.** Stock reports *"Frontlight hardware is disabled on this
  board"* — a nice example of the OEM firmware itself telling you the hardware is
  absent rather than merely unused.
- **No audio, LEDs, PMIC or GPIO expander.** Power management is direct-GPIO
  (the GPIO1 rail) plus the CW2017 gauge and BM8563 RTC.

## What you get that the X4 Pro does not

- **Six real navigation buttons**, interrupt-driven, no ADC ladder, no calibration.
- **A QMI8658 IMU** at 0x6B.
- **USB-MSC** in the SDK's capability list.

## Starting points

No X4C-specific firmware project was found in a ~200-repository census. The route
is the FreeInk SDK's `x4c` environment plus any CrossPoint/CrossInk consumer.
**Nobody has published an X4C build, an X4C bug report, or an X4C flashing guide.**
