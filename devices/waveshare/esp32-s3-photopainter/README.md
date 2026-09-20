# Waveshare ESP32-S3-PhotoPainter — *stub*

> **SKUs 32408 / 32753.** Research snapshot **2026-09-01**. **Stub record**:
> surveyed, not researched in depth. All claims are vendor statements
> (`reported-working`) from the storefront. No artifacts retrieved, no hardware in
> hand.

Created during the [ESP32-S3-ePaper-3.97](../esp32-s3-epaper-3.97/README.md) pass.
Recorded because the PhotoPainter was named as a candidate to research, and the
survey's finding about it is worth keeping: **it is a finished appliance, not a
development board**, and so it is not a PaperMono alternative.

## Identity

| Field | Value |
|---|---|
| Name | ESP32-S3-PhotoPainter |
| SKUs | **32408**, **32753** |
| Price | **USD 82.99 – 83.99** (observed 2026-09-01, waveshare.com, US region) |
| Store | `https://www.waveshare.com/esp32-s3-photopainter.htm` |
| Docs | `https://docs.waveshare.com/ESP32-S3-PhotoPainter` — **404**; not on the new platform at the snapshot date |

## What it is

A **7.3-inch full-colour e-paper photo frame in a solid wood surround**, marketed on
"ultra-long standby", 800 × 480 resolution, with an optional battery.

| Specification | Value |
|---|---|
| SoC | ESP32-S3 |
| Panel | **7.3-inch E Ink Spectra 6 (E6)**, full colour |
| Resolution | 800 × 480 |
| Enclosure | Solid wood photo frame |
| Battery | Optional |

**800 × 480 at 7.3 inches is the same pixel count as the 3.97-inch board** — the same
frame spread over nearly twice the diagonal. It is a viewing-distance product.

## The PhotoPainter family is not one product

The survey turned up **four** distinct listings under this name, only one of which is
ESP32-based. Recorded because the name alone is ambiguous and conflating them would
be an error:

| Slug | SKUs | Price (2026-09-01) | Processor |
|---|---|---|---|
| `esp32-s3-photopainter` | 32408, 32753 | USD 82.99–83.99 | **ESP32-S3** |
| `photopainter` | 24708, 24709 | USD 88.99–90.99 | **Raspberry Pi RP2040** — *not ESP32* |
| `photopainter-b` | 30068, 30315 | USD 92.99–93.99 | **not established** |
| `rpi-zero-photopainter-acce` | — | — | Raspberry Pi Zero accessory |

The `photopainter` original uses **7.3-inch ACeP 7-colour**; `photopainter-b` and the
ESP32-S3 version use **Spectra 6 (E6)**. So the family spans two display generations
*and* at least two processor architectures under one brand.

**`photopainter-b`'s processor was not determined** and is recorded as `unknown`
rather than assumed from the naming.

## Why it was not chosen as the PaperMono comparison

It fails the test on the two things that matter:

1. **It is not a development board.** It is a framed consumer object. There is no
   expansion, and the product is the picture on the wall.
2. **Colour e-paper is a different technology with different constraints.** Spectra 6
   refresh times are measured in tens of seconds, not the 0.3–3.5 s of the monochrome
   3.97-inch panel. Comparing it to a PaperMono on refresh, power or interactivity
   would be comparing unlike things — the sort of false equivalence the
   [PaperMono comparison page](../../m5stack/papermono/comparisons-and-recommendations.md)
   is careful to avoid.

The board that *does* serve the comparison is the
[ESP32-S3-ePaper-3.97](../esp32-s3-epaper-3.97/README.md).

## Why this is a stub

Nothing beyond the storefront was retrieved. No schematic, no demo code, no images,
no panel identification, no `photopainter-b` processor, no refresh figures, no
standby-current evidence for the "ultra-long standby" claim.

## Sources

| ID | Title | Class | URL | Retrieved | Version |
|---|---|---|---|---|---|
| `P01` | ESP32-S3-PhotoPainter — store listing | primary | `https://www.waveshare.com/esp32-s3-photopainter.htm` | 2026-09-01 | `unknown` |
| `P02` | PhotoPainter — store listing | primary | `https://www.waveshare.com/photopainter.htm` | 2026-09-01 | `unknown` |
| `P03` | PhotoPainter (B) — store listing | primary | `https://www.waveshare.com/photopainter-b.htm` | 2026-09-01 | `unknown` |
| `P04` | `docs.waveshare.com/ESP32-S3-PhotoPainter` → **404** | primary | — | 2026-09-01 | negative result |

## See also

- [ESP32-S3-ePaper-3.97](../esp32-s3-epaper-3.97/README.md) — researched in depth
- [The sibling survey](../esp32-s3-epaper-3.97/README.md#sibling-products)
