# Texas Instruments DRV2605 (non-L variant)

> **This part is NOT fitted on the ESP32-S3-Knob-Touch-LCD-1.8.**
> That board carries the **DRV2605L**. See
> [`../drv2605l/`](../drv2605l/) for the fitted part.

This record exists because Waveshare's documentation for the knob board links the **DRV2605**
(non-L) datasheet rather than the DRV2605L datasheet. These are two different documents for two
different parts. That is a documentation-sourcing quirk worth recording, **not** a specification
conflict — nothing here contradicts the DRV2605L record.

## Why keep it

Two distinct copies of the non-L datasheet were acquired from two independent paths, and neither
duplicates the DRV2605L datasheet. They differ in **both language and revision**:

| Local file | TI literature no. | Language | Date band | Bytes | SHA-256 (prefix) | Source path |
|---|---|---|---|---:|---|---|
| `drv2605-datasheet-slos825-2025-06-02.pdf` | **`ZHCSCW9E`** | **Chinese** | DEC 2012 – REVISED **APRIL 2018** | 2,478,601 | `bd754913` | Waveshare wiki mirror (`files.waveshare.com/wiki/common/Drv2605.pdf`) |
| `drv2605-datasheet-slos825c-2014-09-26.pdf` | `SLOS825C` | English | DEC 2012 – REVISED **SEPTEMBER 2014** | 2,557,610 | `c8248776` | Bundled in SensorLib 0.3.1 `datasheet/DRV2605.pdf` |

For comparison, the fitted part's datasheet in [`../drv2605l/`](../drv2605l/) is **`SLOS854D`**, a
completely different literature number for a different part.

> ⚠ **Two corrections to earlier analysis, and one filename that is now wrong.**
>
> 1. `drv2605-datasheet-slos825-2025-06-02.pdf` is **not** literature number `SLOS825`. Page 1
>    reads `ZHCSCW9E – DECEMBER 2012 – REVISED APRIL 2018` over a Chinese title block. `ZHCS…` is
>    TI's prefix for Chinese translations. **Its filename is therefore misleading on both counts:**
>    the literature number is wrong, and `2025-06-02` is a download/PDF-creation date, not the
>    document's revision date (April 2018). Renaming it to `drv2605-datasheet-zhcscw9e-zh.pdf` is
>    proposed but **not yet done** — flagged for decision rather than changed unilaterally, since
>    other documents reference the current path.
> 2. The Chinese copy is consequently **newer** than the English `SLOS825C` (April 2018 vs
>    September 2014), not older as previously implied. If you need the most current non-L content
>    held locally, that is the Chinese file.
>
> Verified 2026-08-24 by `sha256sum` and
> `nix-shell -p poppler-utils --run 'pdftotext -f 1 -l 1 <file> -'`.

**Which applies to the fitted part?** *Neither, strictly.* The knob board fits a **DRV2605L**;
both files here document the **non-L DRV2605**. They are kept to record what the vendor links and
to support cross-checking. For anything authoritative about the fitted part use
[`../drv2605l/artifacts/drv2605l-datasheet.pdf`](../drv2605l/artifacts/drv2605l-datasheet.pdf)
(`SLOS854D`).

Both copies are retained because they are individually small (~2.5 MiB), came from independent
sources, and differ in language and revision — the English `SLOS825C` is the harder one to
reacquire, since TI serves only the current revision from the `symlink` path.

### A byte-identical duplicate was removed

The Waveshare device record previously held its own copy of this document at
`devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/datasheets/Drv2605.pdf`. It was confirmed
**byte-identical** to `drv2605-datasheet-slos825-2025-06-02.pdf` (same SHA-256 `bd754913…`, same
2,478,601 bytes, `cmp` clean). The device-side copy was moved to `../hardware-doc-archive/` on
2026-08-24; the copy here is canonical. See the placeholder at
`devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/datasheets/README.md`.

## Part summary

The DRV2605 is TI's haptic driver with a licensed Immersion TouchSense effect library, driving
ERM and LRA actuators over I²C. The **DRV2605L** is the later, pin-compatible low-voltage variant
in a smaller package; it supersedes the DRV2605 for new designs. Do not assume register-level or
electrical equivalence between them without checking both datasheets — that is exactly the trap
Waveshare's mislinked document sets up.

## Reacquire

```bash
# Current revision from TI (literature number is stable; the revision letter is not)
curl -L -o drv2605.pdf https://www.ti.com/lit/ds/symlink/drv2605.pdf

# The Waveshare mirror that supplied the SLOS825 copy
curl -L -o Drv2605.pdf https://files.waveshare.com/wiki/common/Drv2605.pdf

# The SLOS825C copy is bundled in SensorLib 0.3.1
git clone https://github.com/lewisxhe/SensorLib.git
git -C SensorLib checkout v0.3.1
# -> SensorLib/datasheet/DRV2605.pdf
```

Product page: <https://www.ti.com/product/DRV2605>

> `ti.com/lit/ds/symlink/drv2605.pdf` always serves the **latest** revision, so a fresh download
> will not reproduce either hash above once TI publishes a new revision. Record the literature
> number and revision letter from page 1 after any download.

## Licensing

TI datasheets are distributed for design use. TI's terms permit use in support of TI products but
do not clearly grant redistribution. **Redistribution status: `unknown`.** Retained unstaged
pending review.

## Manufacturer

**Texas Instruments** — see the [Texas Instruments documentation-sourcing guide](../../../vendors/texas-instruments/README.md) for this vendor's document portals, URL patterns, part-numbering conventions, distribution channels and known gotchas.

## Used by

| Device | Role |
|---|---|
| *(none)* | No device in this repository is known to fit a DRV2605 (non-L). This record is reference material only. |

Related: [`../drv2605l/`](../drv2605l/) — the fitted variant, and the record that device
documentation should point at.
