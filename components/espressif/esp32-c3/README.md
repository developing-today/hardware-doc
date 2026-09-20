# Espressif ESP32-C3 — RISC-V Wi-Fi + BLE SoC

- **Category:** 32-bit RISC-V microcontroller with 2.4 GHz Wi-Fi and Bluetooth LE 5.
- **Manufacturer:** Espressif Systems.
- **Research status:** ⚠ **Family-level identification only.** See §1 — the exact
  package/variant on the Xteink boards has **never been read**.
- **Retrieved:** 2026-09-04

The application processor of the **Xteink X3** and **Xteink X4**.

## 1. Identification status — read this before citing a part number

**No exact part number is asserted anywhere in this repository for the Xteink
boards.** What exists:

| Evidence | Says |
|---|---|
| [Imgur X3 teardown](../../../devices/xteink/x3/media.md), image 10 | *"ESP32-C3 main CPU"* — a photograph caption |
| [`sunwoods/Xteink-X3`](https://github.com/sunwoods/Xteink-X3) BOM | `ESP32-C3` |
| **X4 factory flash dump**, bootloader header | **chip-id field = 5**, which is the ESP32-C3 |
| FreeInk SDK | targets `esp32c3` |

Chip-id 5 is a **hard, machine-readable confirmation of the family** and is the
strongest of the four. But **the family is all it confirms.**

**Why the variant is not inferable.** Both teardowns show a **separate Puya
128 Mbit flash chip**, so the SoC is one of the variants *without* embedded flash
(e.g. a bare `ESP32-C3` QFN32) rather than an `ESP32-C3FH4`/`FN4` or a
`ESP32-C3-MINI-1` module. **That is an inference from a photograph, not a
reading**, and this record does not promote it. A legible top-marking photograph
would settle it in seconds.

Per the research method's rule: *"Do not assign a guessed part number."*

## 2. What the family gives you

| Property | Value |
|---|---|
| Core | Single **RISC-V RV32IMC**, up to 160 MHz |
| SRAM | 400 KB |
| **PSRAM** | **None on these boards.** This is the defining constraint |
| Radios | Wi-Fi 2.4 GHz b/g/n; **Bluetooth LE 5** |
| **Bluetooth Classic** | **Not present.** The C3 has no BR/EDR radio |
| USB | **USB Serial/JTAG** peripheral — flashing and debug over the native port, no bridge IC |
| ADC | ADC1 channels on GPIO0–GPIO4 |

**The absence of PSRAM is the single most consequential fact** for anyone writing
firmware for the X3 or X4. It is why CrossPoint abandoned GitHub-release OTA —
*"it causes out of memory issues on the x3"* — and why the S3-based
[X4 Pro](../../../devices/xteink/x4-pro/README.md) and
[X4 Classic](../../../devices/xteink/x4-classic/README.md), with 8 MB PSRAM, can
do multi-buffer rendering and damage-window partial refresh that the C3 cannot.

## 3. How the Xteink boards use ADC1

Both C3 devices put **four functions on the four ADC1-capable pins**:

| GPIO | ADC1 channel | Xteink role |
|---:|---|---|
| 0 | CH0 | Battery voltage sense (÷2 divider) — **X4**; contested on the X3 |
| 1 | CH1 | **Button ladder group 1** — Back / Confirm / Left / Right |
| 2 | CH2 | **Button ladder group 2** — Up / Down |
| 3 | CH3 | Power button (digital, not ADC) |

`analogSetAttenuation(ADC_11db)`. Six buttons on two pins — see
[`devices/xteink/x4/features/buttons.md`](../../../devices/xteink/x4/features/buttons.md)
for the three-device calibration data.

## 4. Datasheet

**Not retrieved in this session.** Espressif publishes openly at
`https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf`
plus a technical reference manual. Retrieval status `not-attempted`; recorded as
an open acquisition.

**Note the repository's own precedent:** three agents once fetched three ESP32-S3
datasheets from three portals and got **three different SHA-256 values and three
different sizes**. If this is fetched later, hash it and name the source in the
filename.

## 5. Caveats and unsafe assumptions

- **Do not assume the ESP32-S3 pin conventions.** On the C3, GPIO20 and GPIO0 are
  ordinary pins the Xteink boards use for I²C; on the **S3** those are USB D+ and
  a boot strap. This is exactly why `XteinkDetect` compiles its C3 I²C fingerprint
  to a no-op unless a C3 profile is in the build — running it on an S3 would poke
  USB D+ and a strap pin at boot.
- **No Bluetooth Classic.** Any project expecting A2DP or SPP is on the wrong SoC.
- The exact variant is unknown, so **flash-embedded-vs-external assumptions are
  unsafe** for anyone recompiling bootloaders.

---

## Used By

### [Xteink X4](../../../devices/xteink/x4/README.md)

Sole processor. 16 MB external
[Puya SPI NOR flash](../../unidentified/xteink-x3-x4/spi-nor-flash-128mbit-puya/README.md),
no PSRAM. Drives one shared SPI bus (SCLK 8 / MOSI 10) for **both** the
[e-paper controller](../../solomon-systech/ssd1677/README.md) and the microSD
card; a two-pin ADC button ladder; and a battery MOSFET latch on GPIO13.
**No I²C peripherals at all** — that absence is what the SDK's runtime probe uses
to tell an X4 from an X3.

Stock firmware is an **Arduino-framework build on ESP-IDF v4.4.7**, confirmed from
the dump's `esp_app_desc_t`.

→ [`devices/xteink/x4/pinouts-and-buses.md`](../../../devices/xteink/x4/pinouts-and-buses.md)
→ [`devices/xteink/x4/factory-firmware.md`](../../../devices/xteink/x4/factory-firmware.md)

### [Xteink X3](../../../devices/xteink/x3/README.md)

Same board family, same flash. Adds a secondary **I²C bus on SDA 20 / SCL 0**
carrying a [BQ27220 gauge](../../texas-instruments/bq27220/README.md) (0x55),
a [DS-series RTC](../../unidentified/xteink-x3-x4/rtc-ds-series/README.md) (0x68)
and a [QMI8658 IMU](../../qst/qmi8658a/README.md) (0x6B). Same two-pin ADC ladder.
GPIO13 becomes the **SD power rail** rather than a battery latch.

**Note two unresolved dual-assignments** on this device: GPIO0 (`batteryAdc` vs
I²C SCL) and GPIO20 (`usbDetect` vs I²C SDA). See
[`devices/xteink/x3/gaps-and-conflicts.md`](../../../devices/xteink/x3/gaps-and-conflicts.md).

→ [`devices/xteink/x3/pinouts-and-buses.md`](../../../devices/xteink/x3/pinouts-and-buses.md)

## See also

[`../esp32-s3r8/README.md`](../esp32-s3r8/README.md) — the SoC of the X4 Pro and
X4 Classic, and the reason those devices can do things these cannot.

---

## Datasheet — retrieved 2026-09-11

The record above gave the URL with retrieval status `not-attempted`. **Fetched,
validated and retained.**

| Field | Value |
|---|---|
| Local path | [`artifacts/esp32-c3-datasheet-en-v2.4.pdf`](artifacts/esp32-c3-datasheet-en-v2.4.pdf) |
| **SHA-256** | `833fc000b4b3c3d39c496fcbd597fed5806956503ce7390b19cc8ae82f19f968` |
| **Bytes** | **900,158** |
| Pages | **76**, A4 |
| Source URL | <https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf> |
| Source class | **primary** — Espressif's own host |
| Retrieved | **2026-09-11**, HTTP 200, magic bytes `%PDF` |
| **Document version** | **Datasheet Version 2.4** (read from the cover) |
| PDF `CreationDate` | **2026-05-06 04:52:40** |
| Producer | `xdvipdfmx (20240407)` |
| Covers | `ESP32-C3`, `ESP32-C3FN4` (**End of life**), `ESP32-C3FH4` |
| Redistribution status | `unknown` — Espressif datasheets carry no explicit redistribution grant |
| Disposition | `repository`, **unstaged** |

**Text-layer validated** against the rendered cover: *"ESP32-C3 Series /
Datasheet Version 2.4 / Ultra-Low-Power SoC with RISC-V Single-Core CPU /
2.4 GHz Wi-Fi (802.11b/g/n) and Bluetooth® 5 (LE) / QFN32 (5×5 mm) package"*.

**Note the variant coverage.** This document covers the bare `ESP32-C3` and the
in-package-flash `ESP32-C3FN4`/`FH4`. The Xteink X3 and X4 use an **external**
16 MB SPI flash, so the in-package-flash variants are **not** what is fitted.
Neither device's exact Espressif part number or module has been read off a board
by this repository — the FCC internal photographs of both are now retained
(see the device records) and have **not** been read at marking level.

**Used by:** [Xteink X3](../../../devices/xteink/x3/README.md) ·
[Xteink X4](../../../devices/xteink/x4/README.md).
