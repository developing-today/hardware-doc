# Waveshare e-Paper ESP32 Driver Board — *stub*

> **SKU 15823.** Research snapshot **2026-09-01**. **Stub record**: surveyed, not
> researched in depth. Every claim is a vendor statement (`reported-working`) read
> from the storefront and legacy wiki. No artifacts retrieved, no hardware in hand.

Created during the [ESP32-S3-ePaper-3.97](../esp32-s3-epaper-3.97/README.md) pass so
that the Waveshare ESP32 e-paper population is known rather than re-derived. **It is
here because it is genuinely relevant, not for completeness** — of Waveshare's seven
ESP32 e-paper products, this is the one that best fits the phrase "a Waveshare ESP32
e-paper *driver* board", and it is the oldest and most widely deployed of them.

## Identity

| Field | Value |
|---|---|
| Name | e-Paper ESP32 Driver Board |
| SKU | **15823** |
| Price | **USD 14.99** (observed 2026-09-01, waveshare.com, US region, single unit) |
| Store | `https://www.waveshare.com/e-paper-esp32-driver-board.htm` |
| Wiki | `https://www.waveshare.com/wiki/E-Paper_ESP32_Driver_Board` — **legacy wiki, HTTP 200** |
| `docs.waveshare.com` | **404** — this product is not on the new platform |

## What it is

**Not a board with a screen on it.** It is a small ESP32 carrier with a 24-pin FPC
connector, sold to drive Waveshare's **raw e-paper panels**, which you buy separately.
Ships with the driver board, an adapter board and an FFC extension cable.

| Specification | Value |
|---|---|
| SoC | **ESP32** (original — not S3, not C6) |
| Flash | 4 MB |
| SRAM / ROM | 520 KB / 448 KB |
| Wi-Fi | 802.11 b/g/n |
| Bluetooth | **4.2, BR/EDR *and* BLE** |
| Panel interface | 3-wire or **4-wire SPI (default)** |
| Operating voltage | 5 V; the 5 V pin accepts **3.6–5.5 V**, so a Li-ion cell works |
| Operating current | 50–150 mA |
| Dimensions | **29.46 × 48.25 mm** |

### The panel pin map is fixed

The wiki states plainly: *"the above is the board fixed connection, with no
additional operation by the user."*

| Panel pin | ESP32 GPIO |
|---|---|
| `DIN` (MOSI) | **P14** |
| `SCLK` | **P13** |
| `CS` | **P15** |
| `DC` | **P27** |
| `RST` | **P26** |
| `BUSY` | **P25** |

That fixed mapping is the board's whole proposition and also its limit: **the only
expansion interface is the panel connector.** There is no general-purpose GPIO header
documented — so, like its bigger sibling, it does not satisfy "e-paper development
board *with expansion*" in the sense that phrase is normally meant. See
[C-WS1](../esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws1--the-expansion-claim-is-backwards).

## Panel compatibility — the actual reason to buy it

The wiki publishes a demo-per-panel table covering **23 panel models**, which is by
far the widest e-paper compatibility of anything in this survey:

1.54" · 1.54" (B) · 2.13" · 2.13" (B) · 2.13" (D) · 2.66" · 2.66" (B) · 2.7" ·
2.7" (B) · 2.9" · 2.9" (B) · 3.7" · 4.01" (F) · 4.2" · 4.2" (B) · 4.26" · 5.65" (F) ·
5.83" · 5.83" (B) · 7.5" · 7.5" (B) · 13.3" (B) · 13.3" (K)

Each maps to a named demo (`epd1in54_V2-demo`, `epd7in5_V2-demo`, …). The wiki warns
that each demo targets the **latest** revision of its panel and that older panels need
the version label on the back checked.

**Note the 3.97-inch panel is absent from that list** — the panel used on the
[ESP32-S3-ePaper-3.97](../esp32-s3-epaper-3.97/README.md) is not among the models this
driver board documents support for.

## Revision history

The wiki records two hardware changes, which matter because they change the driver you
need on the host PC:

| Date | Change |
|---|---|
| **2024-12-30** | USB connector replaced with **Type-C**. "The hardware is basically compatible" |
| **2022-07-28** | Serial chip changed **CP2102 → CH343**. *"Please pay attention to the driver selection"* |

So a unit bought before July 2022 needs CP2102 drivers and a later one needs CH343.
That is the single most likely cause of "the board does not appear as a serial port"
on this product.

## Software

- Arduino-based; the wiki presents it as usable "just like any other Arduino board".
- Ships an **Android app** that pushes images over **Bluetooth EDR** — which is why
  the original ESP32 rather than an S3 is the right choice here: the S3 has no
  Bluetooth Classic. (This knowledge base documents that constraint at length under
  [ESP32-S3R8](../../../components/espressif/esp32-s3r8/README.md).)
- Ships an **HTML host-side page** that pushes images over Wi-Fi.
- Supports **Floyd–Steinberg dithering** and common image formats (BMP, JPEG, GIF, PNG).
- Factory e-paper driver is described as open source.

Stated applications: supermarket electronic price tags, electronic name cards, serial
information display boards.

## Why this is a stub and what would make it a record

Not retrieved: schematic, demo archive, factory firmware, images, pricing history,
community projects, or any component identification beyond the SoC. **No artifact was
downloaded**, so there is nothing to hash.

The highest-value next step would be the demo archive and the schematic, both of which
the legacy wiki's Resources section links.

## Sources

| ID | Title | Class | URL | Retrieved | Version |
|---|---|---|---|---|---|
| `D01` | e-Paper ESP32 Driver Board — store listing | primary | `https://www.waveshare.com/e-paper-esp32-driver-board.htm` | 2026-09-01 | `unknown` |
| `D02` | `E-Paper_ESP32_Driver_Board` wiki | primary | `https://www.waveshare.com/wiki/E-Paper_ESP32_Driver_Board` | 2026-09-01 | revisions dated 20220728, 20241230 |

## See also

- [ESP32-S3-ePaper-3.97](../esp32-s3-epaper-3.97/README.md) — the integrated-panel board researched in depth
- [The sibling survey](../esp32-s3-epaper-3.97/README.md#sibling-products)
- [Waveshare documentation-sourcing guide](../../../vendors/waveshare/README.md)
