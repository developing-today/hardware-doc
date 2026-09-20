# DinMeter — images and provenance

Machine-readable records: [`media/manifest.json`](media/manifest.json).
Applies to K134; the one v1.1-referenced asset is flagged in the manifest.

---

## What is retained

**Ten official product images**, all WebP, all retrieved 2026-09-04 from
`static-cdn.m5stack.com/resource/docs/products/core/M5DinMeter/`, all HTTP 200, all validated by
`RIFF`…`WEBP` magic bytes. Total ≈ 333 KB.

| Field | Value |
|---|---|
| Creator / rightsholder | **M5Stack Technology Co., Ltd** — corporate product photography; no individual photographer is credited |
| Source pages | <https://docs.m5stack.com/en/core/M5DinMeter> and <https://docs.m5stack.com/en/core/DinMeter_v1.1> |
| Retrieved | 2026-09-04 |
| Published/updated | **unknown** — the CDN returned no `Last-Modified` in the captured response |
| Licence | **unknown.** No licence statement on the page or in the files; the footer asserts `Copyright © M5Stack Technology Co., Ltd. All rights reserved.` |
| Redistribution status | `unknown` |
| Disposition | `repository`, **unstaged pending user review** |
| Modifications | **none** — bytes exactly as served. Nothing cropped, rotated, annotated or watermark-stripped |

Per-file SHA-256, byte size, caption and alt text are in the manifest.

## An honest caveat on the captions

The WebP files were validated by magic bytes and hashed, but **not visually rendered** in this
pass — no image decoder was invoked. So the manifest's captions are generic ("M5Stack DinMeter
product photograph") for nine of the ten, rather than describing what each specific frame shows.

That is deliberate. Writing "rear view showing the DC terminal" for a file nobody looked at would
be a fabricated observation dressed as provenance. The one detailed caption
(`img-1f3aa8b5…`) describes the composition stated by the page context, and is labelled in the
manifest as such.

**To improve this:** render each file and replace the captions. It is a five-minute job for
anyone with a browser and it would materially improve the record.

## ⚠ The real gap: no teardown, no PCB, no port close-up

Searched and **not found**, from any source:

| Wanted | Found |
|---|---|
| Bare-PCB photograph (front) | **none** |
| Bare-PCB photograph (back) | **none** |
| Teardown at any stage | **none** |
| Close-up of the encoder body's marking | **none** |
| Close-up of `LS1` (buzzer) marking | **none** |
| Rear port/label close-up at readable resolution | **none** |
| Photograph of the bundled pin sticker | **none** |
| Revision markings / silkscreen | **none** |

This is the **single most consequential media gap in the record**, because photographs would
settle four separate open questions at once:

1. The **rotary encoder's** manufacturer and part number
   ([`components/unidentified/m5stack-dinmeter/rotary-encoder`](../../../components/unidentified/m5stack-dinmeter/rotary-encoder/README.md))
2. The **buzzer `LS1`**'s part number
   ([`components/unidentified/m5stack-dinmeter/buzzer`](../../../components/unidentified/m5stack-dinmeter/buzzer/README.md))
3. The **PORT.A / PORT.B wire-colour conflict**, from the rear silkscreen or the pin sticker
   ([`gaps-and-conflicts.md`](gaps-and-conflicts.md) §1)
4. Whether the **v1.1 PCB really is the v1.0 PCB**, which the byte-identical published assets
   cannot establish ([`gaps-and-conflicts.md`](gaps-and-conflicts.md) §3)

## Related images held under components

Not duplicated here; filed by what they describe:

| Image | Where |
|---|---|
| Stamp-S3 official pin map (`S007_PinMap_01.jpg`, 631 459 B) | [`components/m5stack/stamp-s3/artifacts/`](../../../components/m5stack/stamp-s3/artifacts/S007_PinMap_01.jpg) |
| Stamp-S3A official pin map (`S007-V033_PinMap_01.jpg`, 693 286 B) | [`components/m5stack/stamp-s3a/artifacts/`](../../../components/m5stack/stamp-s3a/artifacts/S007-V033_PinMap_01.jpg) |

Both are **JPEG diagrams that were not OCR'd** in this pass. Reading the Stamp-S3A pin map is the
other thing that would settle the FPC-numbering question in
[`../dinmeter-v1.1/stamp-s3-to-s3a-delta.md`](../dinmeter-v1.1/stamp-s3-to-s3a-delta.md) §6.

## Image search that was not performed

- No reverse-image search for community teardowns.
- No video sources (a teardown video frame would count as evidence with proper attribution).
- No Chinese-language platforms, where M5Stack teardowns often appear first.

All declared exclusions — see [`research-log.md`](research-log.md) §9.
