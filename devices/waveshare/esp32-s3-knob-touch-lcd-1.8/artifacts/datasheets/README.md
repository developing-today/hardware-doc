# Waveshare-mirrored component datasheets — RELOCATED

> Retrieval date: **2026-08-22**. Revision analysis: **2026-08-23**.
> Verification + relocation: **2026-08-24**.

**This directory is now empty of PDFs.** Every file that was here has been moved — either into
the matching `components/<vendor>/<part>/artifacts/` record (when it was a genuinely distinct
document) or to `archive/` (when it was a byte-identical duplicate of a file
already held in `components/`).

Rationale: a component datasheet belongs in the component record, not in a device record. The
device record links to it. Keeping vendor-mirrored copies in a device subtree meant the same
document was discoverable by two different paths with no indication which was authoritative.

All hashes, sizes, and revision strings below were re-derived from the files themselves on
2026-08-24 — SHA-256 via `sha256sum`, revisions via
`nix-shell -p poppler-utils --run 'pdftotext -f 1 -l 2 <file> -'`. They are not copied from
earlier notes.

## Corrections to the previous analysis

The revision table that previously lived in this file was **wrong about the two TI documents**.
Both were recorded as older English revisions. They are in fact **Chinese-language translations**,
carrying TI `ZHCS…` literature numbers rather than `SLAS…`/`SLOS…`:

- `Pcm5100a.pdf` is **`ZHCSA60C`**, not `SLAS859`. Its revision date band
  (*MAY 2012 – REVISED MAY 2015*) is **identical** to the canonical English `SLAS859C`. It is the
  *same revision in Chinese*, not an older revision.
- `Drv2605.pdf` is **`ZHCSCW9E`**, not `SLOS825`. Revised **APRIL 2018** — which makes it
  *newer* than the English `SLOS825C` (revised September 2014) held alongside it, not older.

`Drv2605.pdf` was also recorded here as "the only non-duplicate promoted to `components/`". It is
in fact **byte-identical** to the copy already in `components/texas-instruments/drv2605/`, so two
identical files were being held. That is now resolved.

The four Espressif revision claims were checked and are **all correct as previously stated**.

## Where every file went

| Original filename | What it is | Revision | Bytes | SHA-256 | Disposition |
|---|---|---|---:|---|---|
| `Esp32-s3_datasheet_en.pdf` | ESP32-S3 Series Datasheet (EN) | **v1.6** | 1,186,331 | `b79310e52e90599920fb067c9365263a18943c2efc4b9788edffc2b2d6cdefa1` | **Moved** → [`esp32-s3-datasheet-v1.6-waveshare-mirror.pdf`](../../../../../components/espressif/esp32-s3r8/artifacts/esp32-s3-datasheet-v1.6-waveshare-mirror.pdf) |
| `Esp32_datasheet_en.pdf` | ESP32 Series Datasheet (EN) | **v4.9** | 991,747 | `608f5d36daa88db44da29cf3fe7e4651e0905301948fb22b0af889433bf1ce9b` | **Moved** → [`esp32-datasheet-v4.9-waveshare-mirror.pdf`](../../../../../components/espressif/esp32-u4wdh/artifacts/esp32-datasheet-v4.9-waveshare-mirror.pdf) |
| `Esp32-s3_technical_reference_manual_en.pdf` | ESP32-S3 TRM (EN) | **v1.2** | 14,540,185 | `47bb075de167d8165fc845f4729396080cf0fc92a9f0b793a2527dddae8a2ed9` | **Moved** → [`esp32-s3-technical-reference-manual-v1.2-waveshare-mirror.pdf`](../../../../../components/espressif/esp32-s3r8/artifacts/esp32-s3-technical-reference-manual-v1.2-waveshare-mirror.pdf) |
| `Esp32_technical_reference_manual_en.pdf` | ESP32 TRM (EN) | **v5.4** | 10,220,576 | `e897ef6a5b1aaecdfeb4412e98dcedff6ab6175489529fafc58aeca32153aeca` | **Moved** → [`esp32-technical-reference-manual-v5.4-waveshare-mirror.pdf`](../../../../../components/espressif/esp32-u4wdh/artifacts/esp32-technical-reference-manual-v5.4-waveshare-mirror.pdf) |
| `Pcm5100a.pdf` | PCM510xA DAC datasheet, **Chinese** | **`ZHCSA60C`** (rev. May 2015) | 1,453,455 | `9822f33dad999bca59a3e4607ae377fbf2723a9937c371559ebdfe926220ca67` | **Moved** → [`pcm5100a-datasheet-zhcsa60c-zh-waveshare-mirror.pdf`](../../../../../components/texas-instruments/pcm5100a/artifacts/pcm5100a-datasheet-zhcsa60c-zh-waveshare-mirror.pdf) |
| `Drv2605.pdf` | DRV2605 (**non-L**) haptic driver datasheet, **Chinese** | **`ZHCSCW9E`** (rev. Apr 2018) | 2,478,601 | `bd7549137c51d8b61e6161969f9c27c3dd89f235a27fbcea4b574f48f5eb6b30` | **Archived** — byte-identical duplicate of [`components/texas-instruments/drv2605/artifacts/drv2605-datasheet-slos825-2025-06-02.pdf`](../../../../../components/texas-instruments/drv2605/artifacts/drv2605-datasheet-slos825-2025-06-02.pdf) |
| `CST816D_datasheet_En_V1.3.pdf` | Hynitron CST816D touch controller datasheet (EN) | **V1.3** | 1,098,205 | `a0b14a06ef5d82050d1e98092e2249060438e8dd0dc56f96821259e9175c3409` | **Archived** — byte-identical duplicate of [`components/hynitron/cst816d/artifacts/cst816d-datasheet-v1.3.pdf`](../../../../../components/hynitron/cst816d/artifacts/cst816d-datasheet-v1.3.pdf) |

Totals: **28,392,294 bytes** relocated into `components/`; **3,576,806 bytes** archived as
duplicates; 31,969,100 bytes accounted for in total.

Archived files are at
`archive/doc/hardware/devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/datasheets/`.
Nothing was deleted.

## Why the older Espressif revisions were kept rather than archived

Waveshare's firmware, demo code, and wiki instructions were written against *these* revisions.
When board behaviour disagrees with the current Espressif document, the revision Waveshare
shipped is often the one that explains it — register descriptions, default values, and errata
wording do change between revisions. They are now stored beside the current revision in the
component record, with the revision in the filename so the two can never be confused.

## Source URLs

Every file above came from Waveshare's shared wiki pool. All 7 URLs re-verified **2026-08-24**:

| Original file | Source URL | HTTP | `Content-Length` | Matches local size |
|---|---|---|---:|---|
| `Esp32-s3_datasheet_en.pdf` | <https://files.waveshare.com/wiki/common/Esp32-s3_datasheet_en.pdf> | `200` | 1,186,331 | yes |
| `Esp32_datasheet_en.pdf` | <https://files.waveshare.com/wiki/common/Esp32_datasheet_en.pdf> | `200` | 991,747 | yes |
| `Esp32-s3_technical_reference_manual_en.pdf` | <https://files.waveshare.com/wiki/common/Esp32-s3_technical_reference_manual_en.pdf> | `200` | 14,540,185 | yes |
| `Esp32_technical_reference_manual_en.pdf` | <https://files.waveshare.com/wiki/common/Esp32_technical_reference_manual_en.pdf> | `200` | 10,220,576 | yes |
| `Pcm5100a.pdf` | <https://files.waveshare.com/wiki/common/Pcm5100a.pdf> | `200` | 1,453,455 | yes |
| `Drv2605.pdf` | <https://files.waveshare.com/wiki/common/Drv2605.pdf> | `200` | 2,478,601 | yes |
| `CST816D_datasheet_En_V1.3.pdf` | <https://files.waveshare.com/wiki/common/CST816D_datasheet_En_V1.3.pdf> | `200` | 1,098,205 | yes |

These live in `/wiki/common/`, a pool shared across many Waveshare product wikis, so they are not
tied to this product page. Cross-referenced in [`../../sources.md`](../../sources.md) and
[`../../wiki-resource-links.md`](../../wiki-resource-links.md).

> **Reacquisition caveat:** Waveshare updates files in this pool **in place**. A future download
> from these URLs may return a *newer* revision under the same filename that will not match the
> hashes above. These specific older revisions may become unobtainable from Waveshare. That is
> the main argument for retaining them, and for submitting them to
> `https://web.archive.org/save/`.

## Reacquisition — 2+ independent URLs per document

### ESP32-S3 Datasheet (v1.6 mirrored; upstream serves latest)
1. <https://files.waveshare.com/wiki/common/Esp32-s3_datasheet_en.pdf> (this mirror)
2. <https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf> (vendor, latest rev)
3. <https://web.archive.org/web/2018/https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf> (archived revs)

### ESP32 Datasheet (v4.9 mirrored)
1. <https://files.waveshare.com/wiki/common/Esp32_datasheet_en.pdf>
2. <https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf>
3. <https://web.archive.org/web/2020/https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf>

### ESP32-S3 Technical Reference Manual (v1.2 mirrored)
1. <https://files.waveshare.com/wiki/common/Esp32-s3_technical_reference_manual_en.pdf>
2. <https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf>
3. <https://web.archive.org/web/2022/https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf>

### ESP32 Technical Reference Manual (v5.4 mirrored)
1. <https://files.waveshare.com/wiki/common/Esp32_technical_reference_manual_en.pdf>
2. <https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf>
3. <https://web.archive.org/web/2021/https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf>

### PCM510xA Datasheet (`ZHCSA60C`, Chinese)
1. <https://files.waveshare.com/wiki/common/Pcm5100a.pdf>
2. <https://www.ti.com/lit/ds/zhcsa60c/zhcsa60c.pdf> (TI, Chinese, revision-pinned)
3. <https://www.ti.com/lit/ds/symlink/pcm5100a.pdf> (TI, English, latest rev)

### DRV2605 Datasheet (`ZHCSCW9E`, Chinese, non-L part)
1. <https://files.waveshare.com/wiki/common/Drv2605.pdf>
2. <https://www.ti.com/lit/ds/zhcscw9e/zhcscw9e.pdf> (TI, Chinese, revision-pinned)
3. <https://www.ti.com/lit/ds/symlink/drv2605.pdf> (TI, English, latest rev)

### CST816D Datasheet (V1.3)
1. <https://files.waveshare.com/wiki/common/CST816D_datasheet_En_V1.3.pdf>
2. <https://www.hynitron.com/> (vendor; datasheets are behind the product/contact flow)
3. <https://github.com/lewisxhe/SensorLib> — `datasheet/` directory carries touch-controller PDFs

> TI's `lit/ds/symlink/<part>.pdf` form always serves the **latest** revision; the
> `lit/ds/<litno>/<litno>.pdf` form is revision-pinned and is the one to use to reproduce a hash.

## The DRV2605 vs DRV2605L finding

Waveshare links the **DRV2605** datasheet, but the knob board fits a **DRV2605L** — a different
part with a different TI literature number (`SLOS854D`). Both records are kept:

- [`components/texas-instruments/drv2605/`](../../../../../components/texas-instruments/drv2605/) — the non-L document Waveshare links
- [`components/texas-instruments/drv2605l/`](../../../../../components/texas-instruments/drv2605l/) — **the fitted part**

This is a documentation-sourcing error on the vendor's part, not a specification conflict. Do not
assume register-level or electrical equivalence between the two parts.

## Errata and change notices

Errata are **not** mirrored by Waveshare and are held only in the component records:

- `components/espressif/esp32-s3r8/artifacts/esp32-s3-errata.pdf`
- `components/espressif/esp32-u4wdh/artifacts/esp32-errata.pdf`
- `components/espressif/esp32-u4wdh/artifacts/esp32-chip-revision-v3-0-user-guide.pdf`
- `components/espressif/esp32-u4wdh/artifacts/pcn-2021-021-esp32-u4wdh-dual-core.pdf`
- `components/espressif/esp32-u4wdh/artifacts/pcn20220901-esp32-chip-revision-upgrade.pdf`
- `components/espressif/esp32-u4wdh/artifacts/ar2022-003-esp32-v3-aes-fault-injection-advisory.pdf`
- `components/espressif/esp32-u4wdh/artifacts/ar2022-005-chip-revision-numbering-scheme.pdf`

Always read the errata alongside whichever datasheet revision you are working from.

## Licensing

Espressif and TI datasheets are distributed for design use; neither clearly grants
redistribution. **Redistribution status: `unknown`** for all files listed here. Retained unstaged
pending review.
