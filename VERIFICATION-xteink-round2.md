# Verification — Xteink family, round 2

> Research session **2026-09-11**. Scope: `devices/xteink/**`, the Xteink-specific
> component records, and one append to `ai-crawler-site-access-table.md`.
> Verifier: the authoring session (**self-audit**, as in round 1).
>
> Supplements [`VERIFICATION-xteink.md`](VERIFICATION-xteink.md) (2026-09-04),
> which is **not** modified by this pass.

## Headline

**The evidence position changed materially. The hardware-verification position
did not.**

Round 1's verdict named **source concentration** as this tree's principal
weakness: for the X4 Pro and X4 Classic, essentially every technical claim traced
to one repository at one commit, with no teardown, schematic or regulatory filing.

| Device | Custodians 2026-09-04 | Custodians 2026-09-11 |
|---|---:|---|
| X4 Pro | **1** | **4** — FreeInk · a physically dumped unit · an on-hardware-tested firmware · **FCC `2BTR9-X4PRO`** |
| X4 Classic | **1** | **3** — FreeInk · vendor listing + spec block · **FCC `2BTR9-X4C`**. Still **no board-level** second custodian |
| X3 | teardowns + BOM | **+ public FCC internal photographs** |
| X4 | teardown-free, one dump | **+ public FCC internal photographs** |

**Still zero claims in this tree have been verified on hardware by this
repository.** No Xteink device has been in anyone's hands here, in either pass.
Every "confirmed" means *confirmed by a cited third party*.

## 1. The primary question, answered

**"Is there a new model between the X4 and the X4 Pro?"** — **Yes: the X4
Classic, and it is the device already in this tree.** It launched
internationally on **2026-09-06 19:57:20 −0700** at **US$79**, SKUs
`X4Classic-gray` / `X4Classic-black`, read from the vendor's own
`products.json`.

**"X4 v2" is not a separate SKU.** The vendor's own product title is
`XTEINK X4 Classic (X4 V2) Pocket eReader`; four accessory titles carry the same
parenthetical; the product FAQ uses "X4 V2" in prose; and the vendor's Reddit
announcement of 2026-09-03 reads *"X4 Classic (X4 V2) is coming soon."*

**No other SKU exists between them.** `enum class Board` in the FreeInk SDK at
HEAD (`9f4d3f9`, 2026-09-10) still contains exactly five Xteink entries;
`"X4R1_CLA"` returns `total_count: 0` on GitHub code search; the vendor's
device-only `machine` collection contains exactly X3, X4 Classic and X4 Pro.

**A different new product was found**: **XTEINK X4 Light**, FCC ID `2BTR9-X4L`,
granted 2026-08-13, unannounced and unlisted → [`devices/xteink/x4-light/`](devices/xteink/x4-light/README.md).

## 2. Inventory

| Area | Files added | Files extended |
|---|---:|---:|
| `devices/xteink/x4-classic/` | **13** | 9 |
| `devices/xteink/x4-light/` | **2** (+3 PDFs) | — |
| `devices/xteink/x4-pro/` | 1 (+2 PDFs) | 4 |
| `devices/xteink/x3/` | 1 (+1 PDF) | 2 |
| `devices/xteink/x4/` | (+1 PDF) | 1 |
| `devices/xteink/README.md` | — | 1 |
| `components/` | **1 new record** (`generic/kh3216-a35-chip-antenna`) + 6 PDFs | 7 |
| `archive/devices/xteink/shared-artifacts/research-scratch/` | 4 authored + ~90 raw | 1 |
| repository root | **1** (this file) | 1 (`ai-crawler-site-access-table.md`) |

`devices/xteink/x4-classic/` went from **13 files to 26**: added
`research-log.md`, `commands.md`, `community.md`, `projects-and-community.md`,
`comparisons-and-recommendations.md`, `performance.md`,
`product-history-and-family.md`, `resources-and-conflicts.md`,
`examples/{catalog.json,search-log.md,best.md}`, `media/manifest.json`,
`artifacts/certification/README.md` — and 5 FCC exhibit PDFs.

## 3. Artifacts — validated by content, not extension

**18 files, 26,856,032 bytes.** Every one validated `%PDF` by reading the first
four bytes, and every PDF's own `Title` metadata checked against what it was
believed to be.

| Artifact | Bytes | SHA-256 (first 16) | Doc revision / date |
|---|---:|---|---|
| `2BTR9-XTEINKX3-internal-photos.pdf` | 869,708 | `b3affd56115e9c3e` | filed 2025-12-26, public 2026-06-24 |
| `2BTR9-XTEINKX4-internal-photos.pdf` | 770,254 | `fd1623a7c9df42ba` | filed 2026-01-05, public 2026-07-04 |
| `2BTR9-X4C-label.pdf` | 189,803 | `605b978782399a0f` | 2026-07-20 |
| `2BTR9-X4C-test-report.pdf` | 3,214,822 | `ce40d2300f5ac63c` | 2026-07-20, 51 pp |
| `2BTR9-X4C-antenna-report.pdf` | 1,548,468 | `720ce021f0d403a6` | spec V1.2 |
| `2BTR9-X4C-rf-exposure.pdf` | 144,966 | `7004f25d9c721f88` | 2026-07-20 |
| `2BTR9-X4C-confidentiality-request.pdf` | 121,559 | `6930195fcd9a7b0f` | 2026-07-20 |
| `2BTR9-X4L-external-photos.pdf` | 3,485,136 | `c6457651f19b4cac` | 2026-08-13, 9 images |
| `2BTR9-X4L-label.pdf` | 1,262,117 | `c5be3415bb656997` | 2026-08-13 |
| `2BTR9-X4L-test-report.pdf` | 1,547,812 | `cbe8fc7409534f49` | `BKC26074010GE-2` |
| `2BTR9-X4PRO-external-photos.pdf` | **5,317,690** | `2565de437321171c` | 2026-06-16, 7 images |
| `2BTR9-X4PRO-label.pdf` | 1,169,828 | `3d404d1cefbfc39f` | 2026-06-16 |
| `uc8253c-a-datasheet-rev0.6-…-elecrow-mirror.pdf` | 1,294,916 | `bee25538177b8cc6` | **`UC8253c_A` rev 0.6, 2020-10-13** |
| `uc8179c-c-datasheet-rev0.6-…-crystalfontz-mirror.pdf` | 1,202,516 | `bf1dcef76e0d02a5` | **`UC8179c_C` rev 0.6, 2019-11-26** |
| `esp32-c3-datasheet-en-v2.4.pdf` | 900,158 | `833fc000b4b3c3d3` | **Datasheet v2.4** |
| `bq27220-datasheet-sluscb7a-rev-a.pdf` | 570,379 | `9fffe0b632cd287c` | **`SLUSCB7A` Rev A** |
| `bq27220-technical-reference-manual-sluubd4-rev-a.pdf` | 2,768,446 | `44779f229423d649` | **`SLUUBD4` Rev A** |
| `gt911-programming-guide-rev00-…-crystalfontz-mirror.pdf` | 477,454 | `60c6c2284b482a7a` | **Rev.00, 2014-08-04** |

- **18 of 18 validated `%PDF`. 0 invalid.**
- **0 HTML error pages retained under a `.pdf` extension** — two were caught
  during retrieval and deleted (`uc8179-gooddisplay`, `uc8179-cf-517`).
- **2 valid PDFs retrieved that were the wrong document** and were caught by
  reading their `Title` metadata:
  - `crystalfontz.com/controllers/UltraChip/UC8179/478/` → **GOODiX GT911
    Programming Guide.** *Retained, refiled under `components/goodix/gt911/`,
    because it is the right document for a different component.*
  - `ti.com/lit/ug/sluubd2/sluubd2.pdf` → *"Using the TPS53317AEVM-726"*.
    **Discarded.** The correct literature number is `SLUUBD4`.

**Text-layer validation.** Every value transcribed from a PDF was cross-checked
against a heading visible in the rendered page — the IC version and datasheet
revision lines on the UltraChip covers, the `SLUSCB7A – MARCH 2016` stamp on the
TI datasheet, the `Datasheet Version 2.4` line on the ESP32-C3 cover, and the
`FCC ID: 2BTR9-X4C` header stamped on every page of the X4C exhibits. **No value
was taken from an unvalidated text layer.**

### One artifact fetched, verified and deliberately not retained

The X3 CN OTA stock image, 6,254,064 B. Its SHA-256 **matched the Git-LFS oid
exactly**, its first byte is `0xE9`, and its ESP header reads **`chip_id = 5` =
ESP32-C3**. Not retained (proprietary, unknown licence); a **self-sufficient
placeholder** carrying all four images' hashes, sizes and a verified
no-`git-lfs` download recipe is at
`devices/xteink/x3/artifacts/firmware/zocs-x3-stock-images.NOT-FETCHED.md`.

## 4. Links

| Check | Result |
|---|---|
| Markdown files walked | **138** |
| Relative links resolved | **763** |
| **Broken** | **0** |

JSON: `examples/catalog.json` and `media/manifest.json` both parse.

## 5. Append-only compliance

**`devices/xteink/` is entirely untracked in git** (`??`), so
`git diff -- <file> | grep -c '^-[^-]'` returns 0 trivially and proves nothing.
A real check was therefore run against a pre-edit tar snapshot:

```
for f in <every pre-existing .md>:
    n = wc -l < baseline/$f
    diff <(head -n $n live/$f) baseline/$f
→ append-only violations: 0
```

`archive/devices/xteink/shared-artifacts/research-scratch/round2-baseline/` holds the tar and the pre-edit line counts, and
documents one caveat honestly: the tar was made *after* the first append to
`devices/xteink/x4-classic/README.md`, whose pre-edit state is fixed instead by
its captured line count (239) and the `---` rule at line 240.

For the one **tracked** file appended to:

```
$ git diff -- ai-crawler-site-access-table.md | grep -c '^-[^-]'
0
```

## 6. Git state

| Check | Result |
|---|---|
| `HEAD` | **`4aa02e1030b3b0861e6fc34f23fa2113ec80d324`** — unchanged |
| Staged paths | **91** — unchanged, and the sorted list hashes to the same `md5` as at session start |
| State-changing git commands run | **none** — only `status`, `diff`, `log`, `rev-parse`, `ls-files`, `check-ignore` |
| Protected files modified | **none** — `README.md`, `devices/README.md`, `components/README.md`, `vendors/README.md`, `artifact-manifest.md`, `software/README.md`, `guides/**`, `devices/m5stack/**`, `devices/lilygo/**`, `components/semtech/**` all untouched |

Proposed edits to those files are staged, unapplied, in
[`archive/devices/xteink/shared-artifacts/research-scratch/index-fragments-round2.md`](archive/devices/xteink/shared-artifacts/research-scratch/index-fragments-round2.md).

## 7. Claim-to-source spot checks

| Claim | Independent sources |
|---|---|
| X4 Classic launched 2026-09-06 at $79 | vendor `published_at` · vendor product page · 13 same-day community posts · a dated store review — **4** |
| "X4 V2" = X4 Classic | vendor announcement · product title · 4 accessory titles · product FAQ · third-party firmware header · FCC product code — **6** |
| X4 Classic has no frontlight | vendor spec block · vendor FAQ · FreeInk profile · 2 owner reviews — **4** |
| X4 Classic charges by pogo, not USB-C | vendor spec block · FCC label photograph · accessory renaming · owner review — **4** |
| X4 Classic has a QMI8658 IMU | FreeInk profile · **vendor "Shake-to-Flip"** · owner *"Shake to turn page"* — **3** |
| X4 Pro is an ESP32-S3 with 8 MB PSRAM | FreeInk · **`esptool chip-id` on a physical unit** · **eFuse `PSRAM_CAP=8M`** · boot log — **4** |
| X4 Pro I²C map (0x51, 0x5D, 0x63) | FreeInk · **live I²C trace on a physical unit** · Draftling — **3** |
| X4 Light exists | **FCC grant `2BTR9-X4L`** · test report EUT name · external photographs — **3, all one filing** |
| X3 is an ESP32-C3 | FreeInk · X4 dump chip-id · **X3 OTA image `chip_id = 5`** · teardown · BOM — **5** |
| X4 Classic panel density unchanged at 219 PPI | vendor spec block · 2 owners, one correcting the other — **3** |
| **`R2` in `ESP32S3_X4R2_CLA`** | **narrowed, not resolved** — three converging lines of evidence, no proof |

## 8. Conflicts recorded rather than resolved

| # | Conflict | Where |
|---|---|---|
| R2-C1 | The X4C product page lists two **different** supported-format sets, in the spec block and the FAQ | `x4-classic/gaps-and-conflicts.md` |
| R2-C2 | Vendor says "4.3 inch"; everything else says 4.26″ | same |
| R2-C3 | The FAQ refers to an *"E-ink secondary screen on the back"* that does not exist | same |
| R2-C4 | Two reviewers report better contrast; density is provably unchanged; mechanism unknown | same |
| R2-C5 | US$79 store price vs €89 reported by an EU buyer the same week — not normalised | same |
| **R2-C6/P1** | **X4 Pro touch orientation**: FreeInk says "confirmed by corner-tap"; Draftling says the same values put touches **180° out** and corrected them **on hardware**; the emulator repeats FreeInk | `x4-pro/gaps-and-conflicts.md` |
| R2-P-ver | **Four** stock-firmware version numbers for one X4 Pro: 7.2.4 (hardware-read), 7.4.4, V7.4.5, 7.5.4 | `x4-pro/factory-firmware.md` |

## 9. Refuted, narrowed and confirmed

| Hypothesis | Outcome |
|---|---|
| "A new SKU sits between the X4 and the X4 Pro" | **True, and it is the X4 Classic** — already in this tree, now launched |
| "X4 v2 is a separate future product" | **Refuted.** It is the vendor's own alias for the X4 Classic |
| "X4 Plus / Air / Lite / X4S / X4 Max" | **No evidence for Plus, Air, S or Max.** "Light" **exists** — as `2BTR9-X4L`, a *sixth* device, not a name for the X4 Classic |
| "`R2` implies an undocumented X4C revision 1" | **Narrowed.** The tags are a shared-codebase enum; `"X4R1_CLA"` returns 0 hits; there is no earlier X4C grant; vendor and owners both call the plain X4 "V1" |
| "The X4 Classic has a frontlight" (community, June–September) | **Refuted by the vendor's own spec block.** Round 1's firmware-based claim was right |
| "Shopify collection handles are the tightest available product list" | **Superseded.** The **FCC grantee code** is tighter, and it found a device the handles did not |

## 10. Known gaps in this verification

- **Self-audit.** No independent verifier.
- **Nothing built, nothing measured, no hardware.** `examples/catalog.json`
  contains zero locally-built entries.
- **31 retained board photographs were not read.** One image of 31 was opened.
  Four unidentified parts and the X3 RTC three-way conflict are waiting on them.
- **Three datasheets remain genuinely unobtainable**: UC8279 (12 sources tried),
  CW2017 (**absent from CellWise's own catalogue**), BL8075 (vendor site dead).
- **Chinese marketplaces were not searched.** The X4 Classic's Chinese launch
  date and price are unknown, and no figure in this tree claims otherwise.
- **The X4 Classic has no `features/` guides.** Its `features/` directory holds
  only a `README.md`. Called out in `coverage.md` rather than quietly left.
- **`web.archive.org` CDX was not retried**; the withdrawn X4 pages are still
  unrecovered.

## 11. User decisions still needed

Listed in full in
[`archive/devices/xteink/shared-artifacts/research-scratch/index-fragments-round2.md`](archive/devices/xteink/shared-artifacts/research-scratch/index-fragments-round2.md) §5.

1. **`gt911-programming-guide-*.pdf`** declares itself *"GOODIX CONFIDENTIAL …
   distribution … strictly prohibited"*. Keep unstaged, archive with a
   placeholder, or delete the bytes?
2. **UC8253 / UC8179 datasheets** are marked *"for TFT module use only"*.
3. **`2BTR9-X4PRO-external-photos.pdf`, 5.3 MB** — largest file added.
4. **12 FCC exhibits, 17.9 MB**, all redistribution status `unknown`.
5. **X3 stock images, 56.6 MB** — currently `reference-only` with a verified
   recipe.

**Nothing was staged or committed by this session.**

## 12. Verdict

The primary question is answered from the vendor's own API and a federal
regulatory record, with the date, price and SKUs read from machine-readable
fields rather than prose. The X4 Classic record is now the depth of the X3
record. The X4 Pro's single-source weakness is substantially repaired — though
its **panel pinout specifically** is still single-source, and that is stated in
the record rather than glossed.

The tree's honest limitation is unchanged and worth repeating: **nothing here has
been verified on hardware by this repository, and the three most decisive
documents in the whole subject — the internal photographs of the X4 Pro, the X4
Classic and the X4 Light — are embargoed until 2026-12-12, 2027-01-16 and
2027-02-09 respectively.** Those dates are recorded in each record so the next
session can simply re-check.
