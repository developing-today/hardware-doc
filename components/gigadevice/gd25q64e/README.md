# GigaDevice GD25Q64E

- **Part as fitted:** `GD25Q64ENIGR`
- **Category:** 64 Mbit (**8 MB**) serial NOR flash, SPI / dual / quad
- **Package:** USON-8, footprint `USON8-0.8-4X3MM` (4 × 3 mm)
- **Retrieved:** 2026-08-24
- **Evidence:** KiCad BOM and PCB netlist of the XIAO ESP32S3 Sense v1.5 package. **GigaDevice datasheet not obtained in this pass** — electrical limits below are not established here.

## Part number decode

| Field | Meaning |
|---|---|
| `GD25Q` | GigaDevice 25-series **quad** SPI NOR |
| `64` | **64 Mbit = 8 MB** |
| `E` | generation/revision |
| `N` | package code (USON-8) |
| `I` | industrial temperature grade |
| `G` | RoHS/green |
| `R` | tape-and-reel |

Standard JEDEC-compatible command set (`0x9F` RDID, `0x03`/`0x0B` read, `0x02` page program, `0x20`/`0xD8` erase, `0x06` WREN). Pinout as wired: `/CS`(1) `DO`(2) `/WP`(3) `GND`(4) `DIO`(5) `CLK`(6) `/HOLD`(7) `VCC`(8).

## Used by

### Seeed Studio XIAO ESP32S3 Sense

Reference designator **U5** — the sole program/data flash. Connected directly to the ESP32-S3R8's dedicated SPI flash pins:

| Flash pin | Signal | ESP32-S3 pin |
|---|---|---|
| 1 `/CS` | `SPICS0` | U1.32 |
| 2 `DO` | `SPIQ` | U1.34 |
| 3 `/WP` | `SPIWP` | U1.31 |
| 5 `DIO` | `SPID` | U1.35 |
| 6 `CLK` | `SPICLK` | U1.33 |
| 7 `/HOLD` | `SPIHD` | U1.30 |
| 8 `VCC` | `VDD_SPI` (U1.29, decoupled by C22) | — |

These are the SoC's dedicated flash pins — **not general-purpose GPIO**, and not available for user I/O. Together with the in-package octal PSRAM (which consumes GPIO33–37), this is why the usable GPIO set on this board is as small as it is.

**Flash map.** The 8 MB is partitioned by the factory firmware as: `nvs` 20 KB @ 0x9000 · `otadata` 8 KB @ 0xE000 · `app0` 3,264 KB @ 0x10000 · `app1` 3,264 KB @ 0x340000 · `spiffs` 1,536 KB @ 0x670000 · `coredump` 64 KB @ 0x7F0000 — exactly 8.00 MB, fully allocated. Details and the practical 3,264 KB application-size ceiling: [../../devices/seeed-studio/xiao-esp32s3-sense/factory-firmware.md](../../../devices/seeed-studio/xiao-esp32s3-sense/factory-firmware.md#4-flash-map).

**Mode note.** The vendor's factory images are built for **DIO** at 80 MHz, while the Arduino IDE default for this board is **QIO**. Both work on this part; QIO is faster. See [../../devices/seeed-studio/xiao-esp32s3-sense/development.md](../../../devices/seeed-studio/xiao-esp32s3-sense/development.md).

> **Do not confuse the R8 suffix with flash.** The ESP32-S3**R8** designation refers to **8 MB of in-package PSRAM**, not flash. The 8 MB of flash is this separate external device.


---

## What differs from the Winbond W25Q128JV

This repository holds a deep record for the **[Winbond W25Q128JV family](../../winbond/w25q128jv/README.md)** (16 MB, fitted on the Tanmatsu and the Waveshare Knob board). The GD25Q64E is the same *class* of device — JEDEC-compatible SPI NOR with dual and quad modes — so rather than restate the shared command set, this section records only the deltas. **For erase/program timing, the SFDP mechanism, the full command table, write-protection schemes and the DIO-versus-QIO discussion, read the Winbond record; it applies with the substitutions below.**

| | **GD25Q64E** | **W25Q128JV** |
|---|---|---|
| Manufacturer | GigaDevice | Winbond |
| Density | **64 Mbit = 8 MB** | 128 Mbit = 16 MB |
| Package as fitted | **USON-8, 4 × 3 mm** (`GD25Q64ENIGR`) | SOIC-8 208 mil (`W25Q128JVS`) / WSON-8 (`W25Q128JVPIQ`) |
| JEDEC `RDID` (`0x9F`) manufacturer byte | **`0xC8`** (GigaDevice) | **`0xEF`** (Winbond) |
| Board | Seeed XIAO ESP32S3 Sense, `U5` | Tanmatsu `U9`; Waveshare Knob `U3` |
| Datasheet in this repo | ❌ **not obtained** — see below | ✅ Rev F, retained |

### The three things that actually differ in practice

**1. The JEDEC ID.** `RDID` (`0x9F`) returns a 3-byte manufacturer/memory-type/capacity triple. The manufacturer byte is **`0xC8` for GigaDevice** and `0xEF` for Winbond. Bootloaders and flash-detection code that whitelist manufacturer IDs — and some do — will not recognise a GigaDevice part unless `0xC8` is in the table. The capacity byte encodes 64 Mbit rather than 128 Mbit, so any code that assumes a size instead of reading it will address past the end. `esptool` and the ESP-IDF bootloader read the ID properly and handle both.

**2. The QE (Quad Enable) bit, and where it lives.** This is the classic cross-vendor portability trap for SPI NOR. Quad I/O modes require a **Quad Enable** bit to be set in a status register, and **vendors disagree about which register, which bit position, and what the factory default is**. Getting it wrong yields a part that works in single/dual mode and fails — often intermittently, often only under load — in quad mode.

> ⚠ **This record cannot state the GD25Q64E's QE bit location or factory default**, because the GigaDevice datasheet was not obtained (below). Do **not** assume it matches Winbond's. Determine it from the datasheet, or from SFDP, before enabling QIO.

The practical mitigations, in order of preference: read **SFDP** (JEDEC JESD216), which encodes the QE mechanism in a vendor-neutral way and is what modern bootloaders use; or read back the status registers and verify the bit took; or simply **use DIO**, which needs no QE bit at all.

**3. It is 8 MB, not 16 MB.** The XIAO's factory partition table allocates all 8.00 MB exactly (see the flash map above), leaving a practical **3,264 KB application ceiling** with OTA enabled. The Winbond parts on the other boards have twice the room.

### ⚠ The datasheet was not obtained, and this is what that costs

Thirteen URLs were tried across three sessions; all failed. Full log in [`component-download-failures.txt`](../../../component-download-failures.txt). Two failures are worth repeating because they are traps rather than plain 404s:

- **`gigadevice.com.cn` 404 pages are ~139 KB of HTML** (the `.com` ones are 86 bytes). A size-based sanity check would pass them.
- The `wmsc.lcsc.com/.../v2/...` recipe that genuinely works for other parts returned, for a **guessed** GD25Q64E filename, **a valid 1,062,428-byte PDF that is an NPN bias-resistor transistor datasheet** (MMUN2211 series). Archived to `../hardware-doc-archive/.../WRONG-PART-mmun22xx-transistor-lcsc-C2919772.pdf`. **LCSC serves *something* for any plausible filename; the filename must be read off the real product page, and the extracted text must be grepped for the part number before the file is trusted.**

**Consequently unverified here:** the QE bit location and default, the exact JEDEC device/capacity bytes, erase and program timings, supply and current limits, endurance and retention, and the SFDP contents.

**Recommended next step:** fetch the LCSC product-detail page for the correct C-number, extract the exact PDF filename from the markup, then apply the `/v2/` path with a Chrome User-Agent and an `lcsc.com` referer.

---

## Manufacturer

**GigaDevice Semiconductor (Beijing) Inc.** — no vendor sourcing guide exists in this repository yet. What was learned this session: the `gigadevice.com` `/Public/Uploads/uploadfile/files/<date>/<PART>Datasheet<rev>.pdf` pattern that appears in search results **404s for every date and revision tried**, on both the `.com` and `.com.cn` hosts, and the `.com.cn` 404 body is large enough to fool a size check.

## Related
- [ESP32-S3R8](../../espressif/esp32-s3r8/README.md)
