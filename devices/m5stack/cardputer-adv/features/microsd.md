# Cardputer ADV — microSD

> **Question:** *"How do I read and write the SD card, and why does it interfere with my radio?"*
> Applies to all Cardputer revisions (identical pins); the **conflict** section is ADV-specific.
> Verified **2026-09-04**.

## Hardware

Push-push microSD socket on the SPI peripheral bus, 1-bit SPI mode.

| Signal | GPIO | Source |
|---|---|---|
| `SCK` | **G40** | `M5Unified.cpp:211` `_pin_table_sd` |
| `MOSI` (CMD) | **G14** | same |
| `MISO` (D0) | **G39** | same |
| `CS` (D3) | **G12** | same |
| D1, D2 | not wired (`255`) | same |

Identical on v1.0, v1.1 and ADV — `_pin_table_sd` has one row each and they are the same
numbers. Component: [`generic/micro-sd-sdmmc`](../../../../components/generic/micro-sd-sdmmc/README.md).

## Minimal procedure

```cpp
#include <M5Cardputer.h>
#include <SD.h>
#include <SPI.h>

#define SD_CS 12
void setup() {
  auto cfg = M5.config(); M5Cardputer.begin(cfg, true);
  SPI.begin(40, 39, 14, SD_CS);           // SCK, MISO, MOSI, SS
  while (!SD.begin(SD_CS, SPI, 25000000)) { delay(500); }
  auto f = SD.open("/hello.txt", FILE_WRITE); f.println("hi"); f.close();
}
void loop() {}
```

The vendored example `M5Cardputer/examples/Basic/sdcard/sdcard.ino` (added `889cbd7`,
2024-01-19) does the same and is the vendor's reference.

## ⚠ The bus is shared with the CAP header

G40/G14/G39 also go to **CAP pins L4/L5/L6**. The CAP chip select is **G5**, the SD's is G12.
Nothing arbitrates them for you.

| Combination | Status | Notes |
|---|---|---|
| SD alone | **works** — vendor example | |
| SD + Cap LoRa-1262 | **reported working** — M5Stack's own factory firmware does both, Meshtastic does both | assert one CS at a time; run the bus at the SX1262's 16 MHz limit if you share a handle |
| SD + CAP + tight LoRa RX windows | **caution** | a 512 B SD block at 16 MHz is ~256 µs of bus occupancy plus card latency; receive windows opened late are missed packets |
| SD + display | **works** — different SPI host | |

Detail: [`cap-header.md`](cap-header.md) §"The SPI bus is shared", and
[`../resources-and-conflicts.md`](../resources-and-conflicts.md).

## Community notes

* *"What sd card does everybody use with their cardputer Adv?"* — r/CardPuter, 2026-08-09,
  ↑4/12 comments. There is no vendor-specified card class or maximum capacity, and no
  compatibility list. Treat card choice as untested.
* Several firmwares expect a specific SD layout: Evil-M5Project reads an `evil/` directory,
  Launcher boots `.bin` files from the card, Bruce keeps configuration there. If you swap
  firmware, expect to re-provision the card.
* `uagainshadow/Tons-of-LIVE-Public-CCTV-Cameras-for-the-Cardputer` is an SD content pack —
  a reminder that the card is a first-class part of the ecosystem, not just storage.

## Limits

| Limit | Class |
|---|---|
| 1-bit SPI only (D1/D2 unwired) — no 4-bit SDMMC | **board** |
| Shared bus with CAP | **board** |
| No card-detect line identified on the schematic | **board** |
| Maximum capacity / speed class | **unknown** — no vendor statement, not tested |

## Evidence status

Pin map: **official** (M5Unified pinned commit, three boards agree, and the docs PinMap
matches). Bus sharing: **official** (same nets on schematic sheet 4). Timing consequences:
**inferred**. No SD card was exercised by this session.
