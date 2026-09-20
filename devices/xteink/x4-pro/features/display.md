# X4 Pro — display

> 800×480 monochrome e-ink, 4.26″, ~219 PPI. **Three possible controllers.**
> Evidence: hardware-confirmed via the FreeInk SDK. Last verified 2026-09-04.

## Capability summary

| Property | Value |
|---|---|
| Resolution | 800 × 480, native landscape scan |
| Depth | **1 bpp black/white.** No grayscale path on this board |
| Controller | **SSD1677** or **UC8179** or **UC8279**, batch-dependent |
| Bus | 4-wire SPI, write-only (no MISO on the normal path) |
| Clock | 20 MHz (FreeInk) · 5 MHz (OEM) |
| Orientation | `NO_FLIP` — pending hardware confirmation |
| Power | Controller's **internal booster** (`0x0C` soft-start). No PMIC, no charge pump |

## Hardware path

`ESP32-S3` → SCLK 12 / MOSI 11 / CS 13 / DC 18 / RST 14 / BUSY 6 → controller →
glass. GPIO1 must be HIGH for the panel rail.

Components: [`solomon-systech/ssd1677`](../../../../components/solomon-systech/ssd1677/README.md) ·
[`ultrachip/uc8179`](../../../../components/ultrachip/uc8179/README.md) ·
[`ultrachip/uc8279`](../../../../components/ultrachip/uc8279/README.md)

## The controller lottery — and how to survive it

**You cannot tell which controller a unit has without powering it on.** There is
no external marking. The SDK solves this at boot:

1. Bit-bang a half-duplex 4-wire SPI read on the display pins after a reset pulse.
2. Issue `VER (0x70)` — 5 bytes — and `FLG (0x71)` — 1 byte.
3. **The SSD-family does not answer these commands at all**, so a released SDA
   line floats to a uniform `0x00` or `0xFF` through the pull-up.
4. Match = `FLG` is neither `0x00` nor `0xFF`, has `BUSY_N` (bit0) set, **and**
   `VER` is non-uniform. → UltraChip.
5. Then `VER` byte 2 (`LUT_VER`) discriminates: `0x02`/`0x68`/`0x69` → **UC8279**;
   anything else → **UC8179**.

```c
// freeink-sdk XteinkDetect.cpp:113-119, commit 2400379
bool matchUc81xx(const uint8_t ver[5], uint8_t flg) {
  if (flg == 0x00 || flg == 0xFF) return false;
  if ((flg & 0x01) != 0x01) return false;
  return !verIsFloating(ver);
}
```

**A negative result worth keeping:** an earlier matcher required
`ver[1] != 0`. A shipping X4 Pro UC8179 was then observed returning
`VER = 00 00 01 FF FF` — `CHIP_VER` byte **`0x00`** — and was wrongly rejected.
The matcher deliberately **does not pin any specific `CHIP_VER` value** now.
Do not reintroduce that check.

NVS `hw_calib/screenType` also records the panel type, **but the SDK reads it for
diagnostics only** and never decides on it: a full-flash from another unit
overwrites it, so it can name the wrong panel. (The X4 **Classic** is the
exception — it has no MISO at all and NVS is its only source of truth.)

## Refresh modes

| Mode | Update-control byte (7.4.4) |
|---|---|
| Full | `0x22 = 0xF7` |
| Fast / partial (DU) | `0x22 = 0xFC` |

Both then issue master activation `0x20` and wait BUSY. Border is set
`0x3C = 0xC0` first.

**A visible whole-panel light-then-dark transition during FAST is the
electrophoretic waveform, not the frontlight.** The refresh routines never call
the LEDC path.

## Minimal procedure

Use the SDK; do not hand-roll. `-DFREEINK_DEVICE_X4PRO=1` links all three drivers
and `applyXteinkDisplayController()` selects at boot.

## Limits and pitfalls

| Limit | Kind | Note |
|---|---|---|
| 20 MHz SPI write | **silicon** | SSD1677 datasheet max for write mode |
| 40 MHz | **out of spec** | The `Ssd1677Driver` 0-default is 40 MHz; boards leaving `displaySpiHz = 0` run out of spec |
| ~38 ms/refresh plane write @20 MHz | **measured, on the X4** | Same controller; treat as indicative here |
| 1 bpp only | **board** | No grayscale banks tuned for this device |
| Bezel insets `{9,7,3,7}` | **board** | Without them, screens draw under the glass |

**Pitfall — the app0 pin map.** If you derive pins from a dump, confirm which
app slot `otadata` selects. app0 is a *different variant* and its map is wrong
here. See [`../factory-firmware.md`](../factory-firmware.md).

## Debugging

The probe logs `[XTDET] bus probe VER=… FLG=… -> UltraChip|default|inconclusive`
over serial, plus the MTP header (`RMTP 0xA2`) when the status line was driven —
`0xA5` at byte 0 means a UC part with a programmed MTP.

## Status

`hardware-confirmed` — *"the panel WORKS… it paints normally using the plain X4
OTP waveform, no custom LUT, no explicit voltages, no PMIC, no GPIO
power-enable."* **Open:** panel mount orientation.
