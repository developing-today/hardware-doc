# microSD — XIAO ESP32S3 Sense

> Storage on the Sense daughterboard, the chip-select collision, and the undocumented solder-pad mod.
> Snapshot **2026-08-24**. No hardware testing.

## 1. What it is

A **push-push microSD slot** on the Sense daughterboard, wired for **SPI (1-bit) mode only**.

| Signal | GPIO | XIAO pin | J3 pad |
|---|---:|---|---:|
| `SCK` | **GPIO7** | `D8` | 3 |
| `MISO` (DAT0) | **GPIO8** | `D9` | 4 |
| `MOSI` (CMD) | **GPIO9** | `D10` | 5 |
| `CS` | **GPIO21** | — | 16 |

**It is not SDIO.** DAT1/DAT2/DAT3 are not routed across the board-to-board connector, so 4-bit mode is physically impossible regardless of driver configuration. Use `SD.h` (SPI), not `SD_MMC.h`.

## 2. Card requirements

| Requirement | Value |
|---|---|
| Capacity | **≤ 32 GB** (vendor-supported) |
| Filesystem | **FAT32** |
| Insertion | **gold contacts facing inward** |

Larger cards ship formatted exFAT, which the stock Arduino `SD` library will not mount. Reformatting a 64 GB card as FAT32 commonly works but is outside vendor support. Seeed recommends the SD Association's [SD Card Formatter](https://www.sdcard.org/downloads/formatter/), and notes that a **full** format (not quick) is needed for cards previously used for other purposes — e.g. a card that once held a Linux OS.

## 3. Minimal example

```cpp
#include "FS.h"
#include "SD.h"
#include "SPI.h"

#define SD_CS 21          // NOT the Arduino default SS

void setup() {
  Serial.begin(115200);

  if (!SD.begin(SD_CS)) {          // must pass CS explicitly
    Serial.println("Card Mount Failed");
    return;
  }
  uint8_t type = SD.cardType();
  if (type == CARD_NONE) { Serial.println("No SD card attached"); return; }

  Serial.printf("SD Card Size: %lluMB\n", SD.cardSize() / (1024 * 1024));

  File f = SD.open("/hello.txt", FILE_WRITE);
  if (f) { f.println("hello"); f.close(); }
}

void loop() {}
```

Stock `File > Examples > SD > SD_Test` **will not work unmodified** — it calls `SD.begin()` with no argument. Change it to `SD.begin(21)`.

> If you are using the **Round Display for XIAO** instead of the Sense board, the CS is **`D2`**, not 21.

## 4. The chip-select collision

**GPIO21 is simultaneously the microSD `CS` and `LED_BUILTIN`.**

`pins_arduino.h` declares `static const uint8_t LED_BUILTIN = 21;`; the PCB netlist shows `J3.16 → IO21/USER_LED`; and Seeed's own tutorial passes `21` to `SD.begin()`. They are the same net — not a routing coincidence.

Consequences:

- Driving the LED while the SD library holds the bus **asserts or de-asserts chip-select mid-transaction**. Expect failed mounts, corrupted writes, and `SD.begin()` working once and never again.
- Every SD transaction visibly flickers the user LED. That is not a fault.
- **Never use `LED_BUILTIN` as a status indicator in a sketch that touches the SD card.** Use an external LED on GPIO1–GPIO4, or treat the on-board LED purely as an SD activity light.

This is the highest-impact undocumented interaction on the board. Seeed documents the LED and the SD `CS` on different pages and never connects them.

## 5. The SPI bus is shared — and there is a solder-pad mod

Seeed states:

> "If you choose to use the microSD card function of the expansion board, you cannot also use the SPI function of the XIAO ESP32S3. You can turn on/off the microSD card function by connecting/cutting the pads of J3."
>
> - *To use the SPI pins / disable the SD card:* "Cut along the white thin line to disconnect the solder pad connection."
> - *To enable the SD card / disable the SPI pins:* "Solder the two solder pads together."
> - "By default, the microSD card function is enabled after the expansion board is installed."

This is a **genuine, poorly-publicised hardware modification**: there are solder pads on the daughterboard that physically disconnect the card slot, freeing GPIO7/8/9 for your own SPI peripherals while keeping the camera and microphone.

Two cautions:
- It is **irreversible without soldering** — cutting a trace then re-bridging a 0.4 mm-pitch-era pad is fiddly.
- The pads are on the **daughterboard**, for which no schematic is published, so their exact behaviour is not verifiable from design data. Status: **`reported-working`** (vendor-documented), not verified here.

In practice you can often avoid the mod entirely: SPI is a **shared bus**. Add your peripheral on GPIO7/8/9 with its own chip-select on a free pin (GPIO1–4) and both devices coexist — that is what chip-select is for. The mod matters when you need the pins as plain GPIO, or when a peripheral misbehaves with a second device on the bus.

## 6. A vendor contradiction: is CS GPIO21 or GPIO3?

**Within the same wiki page**, `XIAO_ESP32S3_Sense_tf_and_filesystem.md`:

- The section *"Card slot circuit design for expansion boards"* tabulates **`GPIO3 → CS`**.
- The *"Program annotation"* section states the CS "is connected to **GPIO 21**", and **every code example uses 21**.

**GPIO21 is correct**, on the weight of evidence: all working code uses it, and the netlist routes `IO21/USER_LED` to J3 pad 16.

But the GPIO3 entry is not obviously a typo, because **GPIO3 genuinely does cross the connector** — J3 pad 2 (`D2/A2`) is routed to the daughterboard and is *unused by the stock Sense board*. A CS-select arrangement using GPIO3 is therefore physically possible, and might be what the solder pads in §5 actually switch. Unverified either way.

Recorded as an open question. If you are debugging a card that will not mount, trying `SD.begin(3)` costs nothing.

## 7. Performance expectations

**No throughput figure is published by Seeed, and none was measured here.** What can be said from the wiring:

- 1-bit SPI, so an order of magnitude below SDIO-capable boards.
- The bus is shared with anything else you put on SPI.
- Sustained camera-to-SD recording is the demanding case; several surveyed projects do it, none report numbers.

Treat "record video to SD" as achievable at modest resolution, not as a guaranteed capability at full sensor resolution. Benchmark before committing.

## 8. Alternatives on this board

| Storage | Size | Use when |
|---|---|---|
| **microSD** | ≤ 32 GB | Bulk data, recordings, images |
| **SPIFFS** | **1,536 KB** partition | Small config/web assets; survives reflash of the app |
| **NVS** | 20 KB | Key-value settings, Wi-Fi credentials |
| **PSRAM** | 8 MB | Volatile buffers only |

Flash partition layout: [`../factory-firmware.md` §4](../factory-firmware.md#4-flash-map).

## 9. Troubleshooting

| Symptom | Cause |
|---|---|
| `Card Mount Failed` | `SD.begin()` called without `21`; card not FAT32; card > 32 GB; card inserted upside-down |
| Mounts once, never again | **GPIO21 LED/CS collision** (§4) |
| Works alone, fails with another SPI device | Missing/duplicate chip-select |
| Card not detected at all | Daughterboard not fully seated; or SD pads cut (§5) |
| Corrupt files after power loss | No journalling in FAT32 — close files promptly |
| Previously-Linux card won't format | Use full format, not quick |

## 10. Related

- [`../pinouts-and-buses.md` §5](../pinouts-and-buses.md#5-microsd-card) · [`../resources-and-conflicts.md`](../resources-and-conflicts.md)
- [`microphone.md`](microphone.md) — WAV recording to card
- [`camera.md`](camera.md) — image capture to card
- [Hirose DF40C-30DP-0.4V](../../../../components/hirose/df40c-30dp-0.4v/README.md) — the connector the SPI bus crosses
