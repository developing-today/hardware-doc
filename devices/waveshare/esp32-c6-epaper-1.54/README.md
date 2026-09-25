# Waveshare ESP32-C6-ePaper-1.54 — *stub*

> **SKUs 34393 / 34394.** Research snapshot **2026-09-01**. **Stub record**:
> surveyed, not researched in depth. All claims are vendor statements
> (`reported-working`) from the storefront and `docs.waveshare.com`. No artifacts
> retrieved, no hardware in hand.

Created during the [ESP32-S3-ePaper-3.97](../esp32-s3-epaper-3.97/README.md) pass.
Recorded because it is the **only** e-paper board in this survey that is neither
Xtensa nor Wi-Fi-4-only, and because it carries a documented **I/O expander** — which
bears directly on an unresolved question about the 3.97-inch board's schematic.

## Identity

| SKU | Product |
|---|---|
| **34393** | ESP32-C6-ePaper-1.54 |
| **34394** | ESP32-C6-ePaper-1.54-EN |

| Field | Value |
|---|---|
| Price | **USD 16.99 – 17.99** (observed 2026-09-01, waveshare.com, US region) |
| Store | `https://www.waveshare.com/esp32-c6-epaper-1.54.htm` |
| Docs | `https://docs.waveshare.com/ESP32-C6-ePaper-1.54` — **HTTP 200** |

## Key specifications

| Specification | Value |
|---|---|
| SoC | **ESP32-C6** — RISC-V **single-core**, up to 160 MHz |
| Wireless | **Wi-Fi 6**, Bluetooth 5, **IEEE 802.15.4 (Zigbee 3.0 / Thread)** |
| Memory | 512 KB HP SRAM, 16 KB LP SRAM, 320 KB ROM, **16 MB flash stacked** |
| Display | 1.54-inch e-paper, **200 × 200** |
| Audio | **ES8311** codec + microphone + amplifier + MX1.25 speaker header |
| RTC | **PCF85063** (back side) |
| Environment | **SHTC3** |
| **I/O expander** | **TCA9554** — 8-bit programmable GPIO expander over I²C (back side) |
| Storage | TF card slot, FAT32 |
| Power | MX1.25 2-pin Li-ion header |
| **Expansion** | **2 × 6-pin, 2.54 mm pitch female header** |
| USB | Type-C, native ESP32-C6 USB |

## What makes it distinct

**Radios.** It is the only board in this survey with **802.15.4** — so Zigbee and
Thread/Matter are available, and Wi-Fi 6 with them. For a battery-first e-paper
sensor node joining a Thread mesh, that is a genuinely different proposition from
everything else here, including the PaperMono (whose long-range story is LoRa, not
mesh).

**No PSRAM.** The specification lists 512 KB HP SRAM and 16 MB flash with **no
PSRAM** — unlike the S3 boards. At 200 × 200 × 1 bit a full framebuffer is only 5 KB,
so this is unlikely to bite for display work, but it rules the board out for anything
that wanted a large buffer.

**Single-core RISC-V**, so ports of Xtensa-specific code are not automatic.

## Relevance to the 3.97-inch record

The [ESP32-S3-ePaper-3.97 schematic](../esp32-s3-epaper-3.97/pinouts-and-buses.md)
heads its GPIO allocation column **"IO Expander"** while containing **no I/O expander
part**. This board *does* fit a **TCA9554** and Waveshare documents it explicitly.

That makes **template reuse across the family the most probable explanation** for the
stray heading on the 3.97 — but it is an explanation, not evidence. Tracked as
[C-WS4](../esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws4--io-expander-column-heading-with-no-io-expander-part),
and deliberately **not** used to invent a TCA9554 on the 3.97-inch board.

## Why this is a stub

Not retrieved: schematic, demo code, images, header pinout, panel controller identity,
board dimensions. No artifact downloaded, nothing hashed. No `components/ti/tca9554`
record was created — **this pass never saw that part in design data**, only in vendor
prose about a board it did not research.

## Sources

| ID | Title | Class | URL | Retrieved | Version |
|---|---|---|---|---|---|
| `C01` | ESP32-C6-ePaper-1.54 — store listing | primary | `https://www.waveshare.com/esp32-c6-epaper-1.54.htm` | 2026-09-01 | `unknown` |
| `C02` | ESP32-C6-ePaper-1.54 — documentation | primary | `https://docs.waveshare.com/ESP32-C6-ePaper-1.54` | 2026-09-01 | `unknown` (Docusaurus, undated) |


## Retained artifact

The storefront page this stub was written from is now held with the record:

| File | Bytes | SHA-256 | Retrieved |
|---|---:|---|---|
| [`artifacts/source-snapshots/storefront-esp32-c6-epaper-1.54-2026-09-01.html`](artifacts/source-snapshots/storefront-esp32-c6-epaper-1.54-2026-09-01.html) | 197,275 | `b84c6c6a02aa036ebee749ba8e7e9d699bccdf8619ab3506efc0aca20d487c50` | 2026-09-01 |

Filed **2026-09-20**; it had been sitting in `archive/devices/waveshare/shared-artifacts/epaper-esp32/research-scratch/survey/`
since capture, which is why the header above says no artifacts were retrieved. That
sentence is now out of date in this one respect — the page is here, and the rest of the
survey set is indexed in
[`vendors/waveshare/artifacts/epaper-storefront-survey-2026-09-01/`](../../../vendors/waveshare/artifacts/epaper-storefront-survey-2026-09-01/README.md).

It remains a **vendor marketing page** and establishes only that the product was listed
with these claims on that date. No hardware fact in this record gains authority from it.

## See also

- [ESP32-S3-ePaper-1.54](../esp32-s3-epaper-1.54/README.md) — same size and form, Xtensa, no I/O expander
- [ESP32-S3-ePaper-3.97](../esp32-s3-epaper-3.97/README.md) — researched in depth
- [ESP32-C6-WROOM-1](../../../components/espressif/esp32-c6-wroom-1/README.md) — the C6 module record already in this knowledge base (**this board's exact packaging is not established**)
