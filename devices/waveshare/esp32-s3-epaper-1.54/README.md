# Waveshare ESP32-S3-ePaper-1.54 — *stub*

> **SKUs 32298 / 32299 / 34211 / 34212.** Research snapshot **2026-09-01**.
> **Stub record**: surveyed, not researched in depth. All claims are vendor
> statements (`reported-working`) from the storefront and `docs.waveshare.com`.
> No artifacts retrieved, no hardware in hand.

Created during the [ESP32-S3-ePaper-3.97](../esp32-s3-epaper-3.97/README.md) pass.
**This board matters for one specific reason:** it is the Waveshare e-paper board
that actually has an **expansion header**, which the 3.97-inch flagship does not.

## Identity and variants

| SKU | Product | Note |
|---|---|---|
| **32298** | ESP32-S3-ePaper-1.54 | |
| **32299** | ESP32-S3-ePaper-1.54-EN | |
| **34211** | **ESP32-S3-Touch-ePaper-1.54** | touch variant |
| **34212** | ESP32-S3-Touch-ePaper-1.54-EN | touch variant |

| Field | Value |
|---|---|
| Price | **USD 15.99 – 22.99** (observed 2026-09-01, waveshare.com, US region) |
| Store | `https://www.waveshare.com/esp32-s3-epaper-1.54.htm` |
| Docs | `https://docs.waveshare.com/ESP32-S3-ePaper-1.54` — **HTTP 200** |

The `-EN` suffix marks a documentation/packaging variant, consistent with the
3.97-inch board where `-EN` is the **without-battery** SKU. **Not verified for this
product.**

## Key specifications

| Specification | Value |
|---|---|
| Module | **`ESP32-S3-PICO-1-N8R8`** — 8 MB flash, 8 MB PSRAM stacked |
| CPU | Xtensa LX7 dual-core, up to 240 MHz |
| SRAM / ROM | 512 KB / 384 KB |
| Wireless | 2.4 GHz Wi-Fi, Bluetooth 5 (LE), **onboard chip antenna** |
| Display | **1.54-inch e-paper, 200 × 200** |
| Audio | **ES8311** codec + microphone + MX1.25 speaker header + onboard speaker |
| RTC | **PCF85063** (back side) |
| Environment | **SHTC3** temperature and humidity |
| Storage | TF card slot, FAT32 |
| Power | MX1.25 2-pin Li-ion header |
| Buttons | PWR and BOOT side buttons |
| **Expansion** | **2 × 6-pin, 2.54 mm pitch female header** — *"Reserved … for external expansion"* |
| USB | Type-C, native ESP32-S3 USB |

Note the parts overlap almost exactly with the 3.97-inch board — same codec, same
RTC, same environmental sensor. Waveshare is clearly building one platform across
sizes, which is useful: findings transfer between them more readily than usual.

## Why this board is the honest answer to "e-paper development with expansion"

The [PaperMono record](../../m5stack/papermono/README.md) recommends "a Waveshare
ESP32 e-paper board" for e-paper development **with expansion**. The 3.97-inch board
— the one that actually competes with a PaperMono on display and price — turns out to
have **no expansion header at all**
([C-WS1](../esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws1--the-expansion-claim-is-backwards)).

**This one does.** The trade is severe and should be stated plainly:

| | ESP32-S3-ePaper-1.54 | ESP32-S3-ePaper-3.97 | M5Stack PaperMono |
|---|---|---|---|
| Panel | 1.54", **200 × 200** | 3.97", 800 × 480 | 3.97", 480 × 800 |
| Pixels | **40 000** | 384 000 | 384 000 |
| Expansion | **2 × 6 × 2.54 mm** | none | none |
| Price (2026-09-01) | USD 15.99–22.99 | USD 34.99–47.99 | USD 65.00 |

**You give up 90 % of the pixels to get the header.** For attaching a sensor and
learning e-paper that is often the right trade; for anything where the page is the
product it is not a PaperMono substitute at all.

The header's **pinout is not established** — the docs present it as an image only,
and no schematic was retrieved. That is the first thing a real record here needs.

## Why this is a stub

Not retrieved: schematic, demo code, images, header pinout, panel controller identity,
board dimensions, community projects. No artifact downloaded, nothing hashed.

## Sources

| ID | Title | Class | URL | Retrieved | Version |
|---|---|---|---|---|---|
| `E01` | ESP32-S3-ePaper-1.54 — store listing | primary | `https://www.waveshare.com/esp32-s3-epaper-1.54.htm` | 2026-09-01 | `unknown` |
| `E02` | ESP32-S3-ePaper-1.54 — documentation | primary | `https://docs.waveshare.com/ESP32-S3-ePaper-1.54` | 2026-09-01 | `unknown` (Docusaurus, undated) |


## Retained artifact

The storefront page this stub was written from is now held with the record:

| File | Bytes | SHA-256 | Retrieved |
|---|---:|---|---|
| [`artifacts/source-snapshots/storefront-esp32-s3-epaper-1.54-2026-09-01.html`](artifacts/source-snapshots/storefront-esp32-s3-epaper-1.54-2026-09-01.html) | 198,993 | `f31b3d44f384350554bf40a0e50d50446e929d11dce7e1e78d1764c5d2c265b6` | 2026-09-01 |

Filed **2026-09-20**; it had been sitting in `archive/devices/waveshare/shared-artifacts/epaper-esp32/research-scratch/survey/`
since capture, which is why the header above says no artifacts were retrieved. That
sentence is now out of date in this one respect — the page is here, and the rest of the
survey set is indexed in
[`vendors/waveshare/artifacts/epaper-storefront-survey-2026-09-01/`](../../../vendors/waveshare/artifacts/epaper-storefront-survey-2026-09-01/README.md).

It remains a **vendor marketing page** and establishes only that the product was listed
with these claims on that date. No hardware fact in this record gains authority from it.

## See also

- [ESP32-C6-ePaper-1.54](../esp32-c6-epaper-1.54/README.md) — same size, RISC-V, Wi-Fi 6, **plus a TCA9554 I/O expander**
- [ESP32-S3-ePaper-3.97](../esp32-s3-epaper-3.97/README.md) — researched in depth
- [M5Stack PaperMono comparisons](../../m5stack/papermono/comparisons-and-recommendations.md)
