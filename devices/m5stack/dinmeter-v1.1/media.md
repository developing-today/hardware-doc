# DinMeter v1.1 — images and provenance

Machine-readable records: [`media/manifest.json`](media/manifest.json).

**The family's product photography lives in the v1.0 record**
([`../dinmeter/media.md`](../dinmeter/media.md), 10 images) and is not duplicated here. This page
covers the five v1.1-specific images and one acquisition finding worth recording.

---

## What is retained

| # | File | Source | Format |
|---|---|---|---|
| 1 | `img-dff307df-….webp` | `static-cdn.m5stack.com` — the **only** image the v1.1 documentation page references that the v1.0 page does not | WebP |
| 2–5 | `shop-{1,4,6,9}_….jpg` | `cdn.shopify.com`, from the v1.1 shop listing | **JPEG** |

| Field | Value |
|---|---|
| Creator / rightsholder | **M5Stack Technology Co., Ltd** — corporate product photography, no individual credited |
| Retrieved | 2026-09-04, all HTTP 200 |
| Published/updated | **unknown** — no `Last-Modified` in the captured responses |
| Licence | **unknown.** No statement on either page; footer asserts `Copyright © M5Stack Technology Co., Ltd. All rights reserved.` |
| Redistribution status | `unknown` |
| Disposition | `repository`, **unstaged pending user review** |
| Modifications to bytes | **none** |

## ⚠ Acquisition finding: Shopify serves JPEG under `.webp` URLs

The four shop images have canonical URLs ending **`.webp`**:

```
https://cdn.shopify.com/s/files/1/0056/7689/2250/files/1_3a27efc4-…-dcf2d5d8f3f3.webp?v=1769738162
```

but the bytes returned begin `ff d8 ff e1 … Exif` — **JPEG**, not WebP. Shopify's CDN
content-negotiates the image format and ignores the extension in the path.

The magic-byte check caught it. The files were **renamed locally to `.jpg`** so the extension
matches the content; the bytes are unmodified and the canonical URL is recorded exactly as
served, with a `format_mismatch_note` on each manifest record.

This is precisely the failure the research method warns about — *never save a file under an
extension that misdescribes its content* — and it is worth knowing for any future M5Stack (or
Shopify) image acquisition: **validate by magic bytes, not by URL suffix.** Recorded in
[`../../../vendors/m5stack/README.md`](../../../vendors/m5stack/README.md) as a durable vendor
trap.

## Caveat on the captions

The files were validated by magic bytes and hashed but **not visually rendered** in this pass —
no image decoder was invoked. The manifest's captions are therefore generic ("Shop listing image
4") rather than describing what each frame shows. Writing "rear view showing the DC terminal" for
a file nobody looked at would be fabricated provenance.

Rendering them and replacing the captions is a five-minute job that would materially improve this
record.

## ⚠ The real gap: nothing distinguishes v1.1 visually

Searched and **not found**:

| Wanted | Found |
|---|---|
| A v1.1 PCB photograph | **none** |
| A v1.1 teardown at any stage | **none** |
| A **side-by-side v1.0 / v1.1 comparison** photograph | **none** |
| A photograph showing a Stamp-S3A soldered to a DinMeter carrier | **none** |
| A readable shot of the Stamp-S3A's `U4` marking | **none** |

That last one matters: a photograph of `U4`'s top marking is one of only two realistic ways to
identify the Stamp-S3A's regulator
([`components/unidentified/m5stack-stamp-s3a/dcdc-u4`](../../../components/unidentified/m5stack-stamp-s3a/dcdc-u4/README.md)),
and a v1.0/v1.1 board comparison is the **only** way to test whether the carrier really is
unchanged — the published assets being byte-identical proves only that the *documentation* is
([`gaps-and-conflicts.md`](gaps-and-conflicts.md) V2).

## Related images held elsewhere

| Image | Where | Note |
|---|---|---|
| Stamp-S3A official pin map (`S007-V033_PinMap_01.jpg`, 693 286 B) | [`components/m5stack/stamp-s3a/artifacts/`](../../../components/m5stack/stamp-s3a/artifacts/S007-V033_PinMap_01.jpg) | **Not OCR'd.** Reading it would settle the rear-FPC numbering question in [`stamp-s3-to-s3a-delta.md` §6b](stamp-s3-to-s3a-delta.md) |
| Stamp-S3 official pin map (`S007_PinMap_01.jpg`) | [`components/m5stack/stamp-s3/artifacts/`](../../../components/m5stack/stamp-s3/artifacts/S007_PinMap_01.jpg) | the comparison baseline |
| 10 × DinMeter product photography | [`../dinmeter/media/`](../dinmeter/media/) | applies to both revisions |
