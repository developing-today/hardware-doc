# T-Display K230 — images and provenance

Machine-readable provenance for every retained image: [`media/manifest.json`](media/manifest.json)
(14 records, each with SHA-256, byte size, direct URL, source page, retrieval date, licence
status and modification history).

**All 14 images are vendor material.** Neither lilygo.cc nor wiki.lilygo.cc carries a licence
statement, so every record is `redistribution_status: unknown` and every file is held
**unstaged** pending review.

## What was obtained

| Image | Shows | Source |
|---|---|---|
| `LILYGO-T-DISPLAY-K230_11.jpg` | Bare board, angled, AMOLED lit — the primary listing photo | Shopify CDN |
| `LILYGO-T-DISPLAY-K230_9.jpg` · `_1.jpg` | Bare board, alternate marketing views | Shopify CDN |
| `LILYGO-T-DISPLAY-K230-KIT_12.jpg` | **Kit — main unit docked to the keyboard base.** The single most useful image for identifying the product | Shopify CDN |
| `LILYGO-T-DISPLAY-K230-KIT_9/6/10.jpg` | Kit, alternate views | Shopify CDN |
| `t-display-k230-specifications.jpg` | **Annotated specification card** — LilyGO's own callout graphic | wiki |
| `t-display-k230-40pin.jpg` | **40-pin header pinout diagram** | wiki |
| `t-display-k230-keyboard-extension.jpg` | **Keyboard extension board diagram** | wiki |
| `t-display-k230-cn.jpg` | Chinese-market annotated feature graphic | wiki |
| `t-display-k230-1/2/3.jpg` | Wiki product images | wiki |

The three annotated graphics — specification card, 40-pin diagram, keyboard extension diagram —
are the highest-value items. They are the only published visual documentation of the header and
the keyboard base, and they exist **only on the wiki**, not in the shop listing or the GitHub
repository.

## What was not found — negative results

Searched on 2026-09-04 and **not located**:

| Missing | Consequence |
|---|---|
| **Any PCB photograph**, front or back | The PMIC, speaker amplifier, microphone and the claimed ESP32-S3 cannot be resolved. Directly blocks [`GC-2`](gaps-and-conflicts.md), [`GC-4`](gaps-and-conflicts.md), [`GC-9`](gaps-and-conflicts.md) and every entry in the [unidentified-parts record](../../../components/unidentified/t-display-k230/README.md). |
| **Any teardown**, at any stage | Same. |
| **Any third-party review photograph** | No independent visual evidence exists at all. |
| **A schematic** | The wiki's `#schematic` heading has no content ([`GC-5`](gaps-and-conflicts.md)). |
| **A dimension drawing** | The `#dimension-diagram` heading on the bare-board page has no content. The Cased Version page references `t-display-k230-cased-dimensions.jpg`, which was **not fetched** in this pass — see below. |
| **Cased Version images** | Six are referenced by the Cased Version wiki page: `-cased-angle`, `-cased-front-back`, `-cased-dimensions`, `-cased-features`, `-cased-details`, `-cased-pinmap`. Base URL `https://wiki.lilygo.cc/products/t-display-series/t-display-k230/cased-version/image/<name>.jpg`. **Enumerated, not retrieved** — reacquisition is `automatic`. |

Images embedded in the GitHub repositories were also **not** copied into this record, because
they are reachable at pinned commits and are large: `images/top.png` (227 921 B),
`image/bottom.png` (938 091 B), `image/left.png` (481 816 B), `image/pins_annotated.png`
(699 111 B), `image/dfu_reset_guide.gif` / `_en.gif` (~1 MB each), `images/swd.png`
(3 113 181 B), `images/nRF-ConnectProgrammer.mp4` (2 089 939 B). All are recoverable from
`https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF52840/raw/4646a728580739d487126f47a521e9b8032b3c2c/<path>`
and the nRF9151 equivalent at `ed4ecbe3…`. **`image/pins_annotated.png` is the most valuable of
these** — an annotated pin photograph of the nRF52840 base board.

## Rights

No watermark was removed, no image was cropped, rotated, annotated or recompressed. Every file
is byte-identical to what the server returned, and its SHA-256 in the manifest proves it.
An image-search result is not provenance; every record here names the page the image was
published on.
