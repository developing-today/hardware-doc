# Puya 128 Mbit SPI NOR flash — Xteink X3 / X4 (part number unresolved)

- **Category:** external SPI NOR flash holding the ESP32-C3's firmware.
- **Manufacturer:** **Puya Semiconductor (普冉半导体)** — read from the chip marking.
- **Research status:** ⚠ **Maker and density established; part number never read.**
- **Retrieved:** 2026-09-04

## What is established

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Puya** | **[CN-TD]** `sunwoods/Xteink-X3` BOM: *"PUYA 128Mbit Flash"* |
| Density | **128 Mbit = 16 MB** | **[EN-TD]** Imgur image 10 caption: *"128MBit (16MB) flash for firmware"*; **[CN-TD]** BOM |
| Role | External firmware flash for the ESP32-C3 | both |
| Interface | SPI NOR (implied by the SoC's boot path) | inference |
| **Confirmed capacity** | **16,777,216 bytes** | **[DUMP]** the X4 factory image is *exactly* this size |

Three independent lines of evidence agree on 16 MB: two teardown photographs and
the byte length of an actual flash dump.

## What is missing

**The part number.** Neither teardown transcribes a full marking. Puya's 16 MB
SPI NOR parts are in the `P25Q128*` family, but **no specific part is asserted
here** — that would be promoting a plausible candidate to a finding, which the
research method forbids.

Practical consequences of not knowing it:
- **Maximum SPI clock and supported read modes (QPI/QIO/DIO) are unknown.** ESP-IDF
  flash timing settings cannot be validated against the part.
- **Erase/write endurance and sector geometry are unknown.**
- **Whether the part supports the SFDP parameters the bootloader assumes** is
  unverified — relevant because Puya parts have a documented history of
  non-standard behaviour in some ESP-IDF versions.

## What would resolve it

A legible photograph of the chip's top marking. The archived teardown images
include chip close-ups at up to 5760 × 3240
([`devices/xteink/x3/media.md`](../../../../devices/xteink/x3/media.md), images
10 and 11: *"at an angle to better read the chip labels"*) — **these have not been
examined at full resolution.** This is the cheapest open identification in the
whole subject.

Failing that: `esptool.py flash_id` on a USB-unlocked unit returns the JEDEC
manufacturer and device ID, which maps directly to a part number.

```bash
# inferred, not executed — one command settles it
esptool.py --chip esp32c3 --port /dev/ttyUSB0 flash_id
```

---

## Used By

### [Xteink X4](../../../../devices/xteink/x4/README.md)

External firmware flash. Partition table parsed from the dump: `nvs` `0x9000` ·
`otadata` `0xE000` · `app0` `0x10000` (6400 KiB) · `app1` `0x650000` (6400 KiB) ·
**`spiffs` `0xC90000` (3456 KiB)** · `coredump` `0xFF0000`.

The unusually large SPIFFS is consistent with the stock firmware serving the
on-device web file manager (`http://bofi.xteink.cn/index.html`) out of flash.

→ [`devices/xteink/x4/factory-firmware.md`](../../../../devices/xteink/x4/factory-firmware.md)

### [Xteink X3](../../../../devices/xteink/x3/README.md)

Same part, same board family — this is the device both teardowns photographed.
The X3's own partition layout is **not established**; the X4's is assumed but
unverified.

→ [`devices/xteink/x3/factory-firmware.md`](../../../../devices/xteink/x3/factory-firmware.md)
