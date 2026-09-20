# Espressif ESP32-S3FN8

> The ESP32-S3 variant with **8 MB flash in package and no PSRAM**.
> Record created **2026-09-04** from M5Stack Stamp module schematics and vendor board support.
> See also the family record [`espressif/esp32-s3r8`](../esp32-s3r8/README.md), which is the
> **8 MB PSRAM, no-flash** variant — the two suffixes are easy to confuse and mean opposite
> things.

## Reading the suffix

Espressif's ESP32-S3 part numbers encode in-package memory:

| Suffix | In-package flash | In-package PSRAM |
|---|---|---|
| *(none)* | — | — |
| **`FN8`** | **8 MB** | **none** |
| `FH4` | 4 MB | none |
| `R2` / `R8` / `R16V` | — | 2 / 8 / 16 MB |
| `R8V`, `FN8R2`… | combinations | |

**`FN8` = Flash 8, no PSRAM.** This is the single most consequential fact about every Cardputer:
the platform has **512 KB of SRAM and nothing else**, and no amount of external wiring changes
that, because the package has no PSRAM die and the Stamp module brings out no PSRAM-capable
pins for one.

## Key capabilities

| Property | Value |
|---|---|
| Cores | 2 × Xtensa LX7, up to **240 MHz** |
| SRAM | **512 KB** |
| ROM | 384 KB |
| In-package flash | **8 MB**, quad SPI |
| **PSRAM** | **none** |
| Radio | 2.4 GHz Wi-Fi 802.11 b/g/n; **Bluetooth 5 LE** (no BR/EDR) |
| USB | **native USB-OTG** + USB Serial/JTAG |
| Peripherals | 2 × I²S, 4 × SPI, 2 × I²C, RMT, LEDC, 2 × ADC, TWAI, SDMMC, LCD/camera interfaces |
| Crypto | AES, SHA, RSA, HMAC, digital signature, secure boot, flash encryption |
| GPIO | 45 usable on the bare die; **26 on the M5Stack Stamp-S3 footprint** |

## What "no PSRAM" costs, concretely

Measured against the Cardputer ADV's actual workload:

| Consumer | Bytes | % of 512 KB |
|---|---|---|
| 240 × 135 × 16 bpp framebuffer | 64 800 | 12.7 % |
| Double buffered | 129 600 | 25.3 % |
| Wi-Fi + LWIP | ~50 000–80 000 | 10–16 % |

Three independent pieces of downstream evidence:

* Meshtastic's Cardputer ADV variant compiles with **`-DOLEDDISPLAY_REDUCE_MEMORY`**.
* Bruce ships a **`-DLITE_VERSION=1`** flag "to save space".
* A community Meshtastic-client author (r/CardPuter, 2026-08-01) put a **2.16 MB GNU Unifont
  table in its own flash partition** and memory-mapped it, *"so rendering Cyrillic, CJK or Greek
  costs no heap at all"* — because *"the ESP32-S3 here has no PSRAM, so a full Unicode font
  cannot live in RAM."*

## Support pins seen on the M5Stack Stamp modules

From `Sch_StampS3_v0.2` and `Sch_StampS3_v0.3.3`:

| Function | Detail |
|---|---|
| Crystal | **X1, 40 MHz**, load caps 12 pF / 10 pF (v0.2) or 12 pF / 12 pF (v0.3.3) on `XTAL_P`/`XTAL_N` (pins 53/54) |
| `VDD_SPI` | pin 29, decoupled 100 nF + 1 µF — the in-package flash supply |
| `VDDA1`/`VDDA2` | pins 55/56 |
| `VDD3P3_RTC` | pin 20 · `VDD3P3_CPU` pin 46 |
| `CHIP_PU` | pin 4, from `ESP_EN` with an RC and a 10 kΩ pull-up |
| `LNA_IN` | pin 1 → π matching network → `ANT1` |
| `GND` | pin 57 and the exposed pad |
| `U0TXD`/`U0RXD` | brought to the module header with a **510 Ω 1 %** series resistor on TX |

## Used By

### M5Stack Stamp-S3 and Stamp-S3A modules

[`components/m5stack/stamp-s3`](../../m5stack/stamp-s3/README.md) ·
[`components/m5stack/stamp-s3a`](../../m5stack/stamp-s3a/README.md)
*(both created by a concurrent session; this record links rather than duplicates)*

Both modules carry the same `ESP32-S3FN8` die. What differs between them is entirely support
circuitry — the 3.3 V regulator, the load switch, and **which rail the WS2812 sits on**.

### M5Stack Cardputer v1.0, v1.1 and ADV

[`devices/m5stack/cardputer-v1.0`](../../../devices/m5stack/cardputer-v1.0/README.md) ·
[`devices/m5stack/cardputer-v1.1`](../../../devices/m5stack/cardputer-v1.1/README.md) ·
[`devices/m5stack/cardputer-adv`](../../../devices/m5stack/cardputer-adv/README.md)

All three use the same SoC through a Stamp module. Board-level GPIO allocation differs
substantially and is documented per device; the relevant SoC-level notes are:

* **G0** is the boot strap and the user button on every Cardputer.
* **G3** is a JTAG-source strap **and** the CAP header's `RESET` line on the ADV — worth knowing
  before attaching a board that drives it during reset.
* **G45/G46** are strap pins; the ADV drives G46 from the ES8311's `ASDOUT` (high-Z until the
  codec is enabled, so benign in practice).
* **G21** carries the WS2812 data on all three.
* **No SDMMC 4-bit mode** is used: the microSD is 1-bit SPI on all three, with `D1`/`D2` unwired.

### M5Stack CardputerZero

Does **not** use this part — it is a Raspberry Pi CM0 (BCM2837) device.
[`devices/m5stack/cardputer-zero`](../../../devices/m5stack/cardputer-zero/README.md)

## Substitutes and migration

| Part | Migration note |
|---|---|
| **`ESP32-S3R8`** / `R8V` | 8 MB PSRAM but **no in-package flash** — you must add an external flash chip. Not a drop-in. See [`esp32-s3r8`](../esp32-s3r8/README.md). |
| `ESP32-S3FN8R2` etc. | flash **and** PSRAM in package — the part a "Cardputer with PSRAM" would want |
| `ESP32-S3-WROOM-1-N8R8` | module form, flash + PSRAM; different footprint entirely from the Stamp-S3 |
| ESP32-S2 | no BLE, single core |
| ESP32-C6 | RISC-V, Wi-Fi 6 + 802.15.4, much less RAM |

## Gaps

* **No Espressif datasheet retained by this record.** M5Stack mirrors one at
  `m5stack-doc.oss-cn-shenzhen.aliyuncs.com/472/esp32-s3_datasheet_en.pdf` (linked from the
  Cardputer Mesh Kit page) — **not fetched in this pass**, and the PaperMono pass established
  that M5Stack's mirrors are frequently stale. Prefer Espressif's own copy and hash both.
* Pin-number-to-name mapping above is read from an M5Stack symbol, not from Espressif's datasheet.
* Errata: **not reviewed**.
