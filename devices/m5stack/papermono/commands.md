# PaperMono — command ledger

> ## No command in this ledger was run against physical hardware.
>
> **There is no PaperMono in this session and none could be bought — the product
> has been out of stock since nine minutes after launch.** Every command below
> operates on *documents, archives and binaries*: HTTP fetches, PDF parsing,
> `git` clones, hash checks and static binary inspection. The one section that
> describes touching a device — [Vendor build and flash procedure](#vendor-build-and-flash-procedure)
> — is transcribed from vendor documentation and is marked **`reported-working`**,
> which means *the vendor says so and nobody here has tried it*.
>
> Nothing in this file may be cited as evidence of device behaviour.

## Status vocabulary

| Status | Meaning |
|---|---|
| **`executed-success`** | Run in this session; the stated output was observed |
| **`executed-failed`** | Run; failed. Recorded because the failure is the finding |
| **`reported-working`** | Published by the vendor or a third party as working. **Not run here** |
| **`inferred`** | Reconstructed from observed artifacts; plausible but not itself executed as written |
| **`not-tested`** | Written down, never run, no external claim either |

## Environment

Every `executed-*` command below was run on this host on **2026-09-01**.

| | |
|---|---|
| OS / kernel | Linux 6.18.44 (NixOS) |
| Shell | GNU bash 5.3.15(1)-release, x86_64-pc-linux-gnu |
| `curl` | **8.21.0** (OpenSSL 3.6.3, zlib 1.3.2, brotli 1.2.0, zstd 1.5.7), release 2026-06-24 |
| `python3` | **3.14.7** (confirmed by the `cpython-314` bytecode cache left beside the tools) |
| `git` | **2.55.0** |
| `gh` | **2.97.0** (nixpkgs) |
| `sha256sum`, `od`, `stat` | GNU coreutils **9.11** |
| `pdftotext`, `pdftoppm`, `pdfinfo` | poppler **26.06.0**, supplied ephemerally by `nix-shell -p poppler-utils` — **not installed on the host** |

> **A version caveat worth stating.** The user-agent ladder used by the fetch
> helpers hardcodes the string `curl/8.5.0`. That is a *chosen identity*, not this
> host's real default, which is `curl/8.21.0`. Wherever this record says "plain
> curl worked", it means "a request identifying itself as `curl/8.5.0` worked".

## Paths

All working directories are given **as this repository sees them** — relative to
the `hardware-doc` repository root:

| Path here | What it is |
|---|---|
| `scratch/m5stack-papermono/` | the working tree for this pass (a symlink into `../repo-archive/scratch/hardware-doc/`) |
| `devices/m5stack/papermono/artifacts/` | the artifacts kept in this repository |
| `tools/` | the repo's parsers, including the three Altium tools below |

From the *consuming* repository the same paths are reachable as
`doc/hardware/scratch/…` and `doc/hardware/tools/…`.

---

## Contents

- [1. Artifact acquisition and content validation](#1-artifact-acquisition-and-content-validation)
- [2. PDF text, metadata and raster extraction](#2-pdf-text-metadata-and-raster-extraction)
- [3. Altium PDF tooling](#altium-pdf-tooling)
- [4. M5Burner firmware retrieval](#4-m5burner-firmware-retrieval)
- [5. Firmware image inspection](#5-firmware-image-inspection)
- [6. Source repository acquisition and verification](#6-source-repository-acquisition-and-verification)
- [7. Vendor build and flash procedure](#vendor-build-and-flash-procedure)
- [8. The vendor PlatformIO configuration, verbatim](#8-the-vendor-platformio-configuration-verbatim)

---

## 1. Artifact acquisition and content validation

### 1.1 Fetch a vendor document and record its provenance

| Field | Value |
|---|---|
| **Source / purpose** | Retrieve the PDFs and HTML pages listed in [`sources.md`](sources.md) and record status, decoded size, SHA-256 and retrieval time in a `.meta` sidecar beside each file |
| **Working directory** | `scratch/m5stack-papermono/docs/` |
| **Shell / OS** | bash 5.3.15 on Linux 6.18.44 |
| **Tool + version** | `curl` 8.21.0; `sha256sum`/`stat` coreutils 9.11 |
| **Prerequisites** | Network access. No credentials — every URL in this record is public |
| **Generated files** | `<outbase>.html`, `<outbase>.headers`, `<outbase>.meta` |
| **Status** | **`executed-success`** — 13 documentation pages, 9 store URLs and 5 M5Burner URLs; every one returned on the **first** request with the Chrome 131 UA, no fallback needed |
| **Date** | 2026-09-01 |

```bash
# _tools/fetch.sh <url> <outbase>
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
curl -sSL --compressed --max-time 90 \
  -A "$UA" \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -D "${out}.headers" \
  -o "${out}.html" \
  -w '%{http_code}|%{size_download}|%{content_type}|%{url_effective}' \
  "$url"
```

Full script: `scratch/m5stack-papermono/docs/_tools/fetch.sh`.

> **Record the decoded size, not `%{size_download}`.** With `--compressed`, curl's
> `size_download` is the **gzipped wire size**, which will not match the SHA-256
> you take over the file on disk. The helper records `bytes` from
> `stat -c%s` and keeps the wire figure separately as `wire_bytes`. Every byte
> count in [`sources.md`](sources.md) is the decoded on-disk size.

### 1.2 Validate a downloaded document by content, not by extension

| Field | Value |
|---|---|
| **Source / purpose** | Establish that a file claiming to be a PDF *is* a PDF, and that a firmware download is an ESP32 image rather than an HTML error page |
| **Working directory** | `scratch/m5stack-papermono/pdf/` (PDFs) · `…/docs/firmware/` (binaries) |
| **Shell / OS** | bash 5.3.15 on Linux |
| **Tool + version** | `od`, `head`, `sha256sum`, `stat` — coreutils 9.11 |
| **Prerequisites** | The file downloaded |
| **Expected output** | `%PDF` for a PDF; `e9` for an ESP32 image; no `<html`/`<?xml` in the first 512 bytes |
| **Status** | **`executed-success`** — all 11 PDFs began `%PDF`; both binaries began `0xE9`; **no download was rejected** |
| **Date** | 2026-09-01 |

```bash
# PDF magic — check the bytes, never the Content-Type
head -c 4 PaperMono_SCH_V0.6.2_20260522.pdf            # -> %PDF

# ESP32 image magic
od -An -tx1 -N1 C153-PaperMono-UserDemo-v1.2.bin       # -> e9

# no HTML/XML error page hiding behind a 200
head -c 512 C153-PaperMono-UserDemo-v1.2.bin | tr -d '\0' | grep -c -iE '<html|<\?xml|<!doctype'   # -> 0

# size and fingerprint
stat -c%s C153-PaperMono-UserDemo-v1.2.bin             # -> 2868208
sha256sum C153-PaperMono-UserDemo-v1.2.bin
# -> 72c290bc2ffa216041b276660277369bd17ecef92315e367d98bb2c96c8428fa
```

> **Why this is not paranoia.** `datasheet.lcsc.com` returns **HTTP 200 with
> `Content-Type: text/html`** for URLs that do serve a real PDF — status and
> content-type both lie, and only the leading `%PDF` tells the truth. The same
> discipline applied here caught nothing, which is itself the result worth
> recording: *zero rejections across 13 downloads.* The helper writes a rejected
> payload to `<name>.REJECTED.txt` rather than deleting it; no such file exists.

### 1.3 Hash every retained artifact

| Field | Value |
|---|---|
| **Source / purpose** | Produce the fingerprints quoted in [`sources.md`](sources.md) and in each component record |
| **Working directory** | `scratch/m5stack-papermono/pdf/` |
| **Tool + version** | coreutils 9.11 |
| **Status** | **`executed-success`** |
| **Date** | 2026-09-01 |

```bash
for f in *.pdf *.PDF; do
  printf '%s | %s bytes | ' "$f" "$(stat -c%s "$f")"
  sha256sum "$f" | cut -c1-64
done
```

Observed, in full:

```
C153_PaperMono_model_size.pdf              |    21346 | b833a3e52594a3175bc131006d41a3eb5662be5936d0b2f25030180033a6703b
DS_SX1261_2_V2-2-m5stack-mirror.pdf        |  4459535 | 6d783125dbef567954ce53095ad068d0950b2a8de52f95bb2cfde4146c4306c2
EPD_Module_User_Manual.pdf                 |  8666208 | 6b65f56d5d549a132e5c807eef329fb3e997feab04ac06e8a107f01591618130
esp32-s3_datasheet_en-m5stack-mirror.pdf   |  1083807 | b6db403d6d5db8d1b4db0c8390ff7e0a7db714b8388e986e1c64bff563f76b61
M5IOE1_IO_Expander_Datasheet_EN.pdf        |   398463 | 9204d99cb2e03395ffc905e05fbeddf7f9f25de5698a31a65fa439dee700d8d2
M5PM1_Datasheet_EN.pdf                     |   814731 | c6daffd0ab89d8de50c0a19f35f94321bc6c9511ad017dd242a3e765d88a96b6
PaperMono_SCH_V0.6.2_20260522.pdf          |  1462039 | b5abecac97cb043a6d1af7a673f2111d40d9254b0b5108635cb924d9b37ad6fa
RX8130CE_cn-Register-Datasheet-m5stack-…   |  2283323 | 7157dc5692e5e0d84203027b600858e57880ef7a38b9c7d7f8c661a93fc8f3f5
SSD1677-m5stack-mirror.pdf                 |  3602487 | daf8b726f822f6907529386b8af6fbea6ec5e8ecc7b7af361340be911d632544
ST25R3916_EN-m5stack-mirror.pdf            |  2241765 | 1170f4d74ff501917262ae42bf81c60c38c11d121e2ea2af6b1e845433befef1
BMI270-m5stack-mirror.PDF                  |  3830973 | 3ab915ed1d81d0eaa5ff1d1aed62b2b491260c9d59afbf79bb23fb477e015612
```

---

## 2. PDF text, metadata and raster extraction

Poppler is **not installed on this host**; every invocation is wrapped in
`nix-shell -p poppler-utils`, which is why the wrapper appears verbatim below
rather than being elided.

### 2.1 Document metadata and page counts

| Field | Value |
|---|---|
| **Source / purpose** | Establish each document's own revision, producer and date — the `Published/updated` column of [`sources.md`](sources.md) |
| **Working directory** | `scratch/m5stack-papermono/pdf/` |
| **Tool + version** | `pdfinfo`, poppler 26.06.0, via `nix-shell` |
| **Prerequisites** | Nix with a channel able to resolve `poppler-utils`; network on first use |
| **Status** | **`executed-success`** |
| **Date** | 2026-09-01 |

```bash
nix-shell -p poppler-utils --run "pdfinfo PaperMono_SCH_V0.6.2_20260522.pdf"
```

Observed (abridged) — and load-bearing, because it establishes the schematic's
export chain and sheet count:

```
Title:           New Output
Creator:         Altium Designer
Producer:        llPDFLib 3.x
CreationDate:    Mon Jun  8 19:00:00 2026 CDT
ModDate:         Mon Jul 27 22:00:05 2026 CDT
Pages:           6
```

Three metadata reads that became findings:

```bash
nix-shell -p poppler-utils --run "pdfinfo SSD1677-m5stack-mirror.pdf"
# Producer: PDFill: Free PDF Writer and Tools   CreationDate: 2019-01-09   Pages: 46
#   -> not a Solomon Systech export; and the document numbers itself n/47

nix-shell -p poppler-utils --run "pdfinfo EPD_Module_User_Manual.pdf"
# Producer: iLovePDF                            ModDate: 2026-08-21        Pages: 30
#   -> a re-processed copy; cover carries no revision at all

nix-shell -p poppler-utils --run "pdfinfo C153_PaperMono_model_size.pdf"
# Producer: Adobe PDF Library 18.0.4            CreationDate: 2026-08-20   Pages: 1
```

### 2.2 Layout-preserving text extraction

| Field | Value |
|---|---|
| **Source / purpose** | Read revision blocks, register tables and specification tables out of the datasheets and the schematic without opening a viewer |
| **Working directory** | `scratch/m5stack-papermono/` |
| **Tool + version** | `pdftotext`, poppler 26.06.0 |
| **Prerequisites** | The PDFs from §1 |
| **Generated files** | `pdf/sch-p{1..6}.txt`, `pdf/sch-all.txt` (557 153 B), `pdf/model-size.txt` |
| **Status** | **`executed-success`** |
| **Date** | 2026-09-01 |

```bash
# whole schematic, and one file per sheet
nix-shell -p poppler-utils --run "pdftotext -layout pdf/PaperMono_SCH_V0.6.2_20260522.pdf pdf/sch-all.txt"
for p in 1 2 3 4 5 6; do
  nix-shell -p poppler-utils --run \
    "pdftotext -f $p -l $p -layout pdf/PaperMono_SCH_V0.6.2_20260522.pdf pdf/sch-p$p.txt"
done

# mechanical drawing
nix-shell -p poppler-utils --run "pdftotext -layout pdf/C153_PaperMono_model_size.pdf pdf/model-size.txt"
```

**`-layout` is not optional here.** Without it, the schematic's title blocks and
the datasheets' revision tables lose their column association and become
unreadable; the same applies to the vendor HTML pages, whose specifications live
in `<table>` elements (the HTML-to-text helper preserves cells joined with ` | `
for exactly this reason).

Revision extraction, verbatim, for the rows in [`sources.md`](sources.md):

```bash
nix-shell -p poppler-utils --run \
  "pdftotext -f 1 -l 1 -layout BMI270-m5stack-mirror.PDF -"
# Document revision      1.3
# Document release date  Nov 2020
# Document number        BST-BMI270-DS000-05

nix-shell -p poppler-utils --run \
  "pdftotext -f 155 -l 160 -layout ST25R3916_EN-m5stack-mirror.pdf -" | grep -E 'DS12484 Rev'
# DS12484 Rev 8            -> revision history table dates rev 8 at 08-May-2023

nix-shell -p poppler-utils --run \
  "pdftotext -layout DS_SX1261_2_V2-2-m5stack-mirror.pdf -" | grep -m1 'Rev 2.2'
# Data Sheet  Rev 2.2  Semtech     (footer DS.SX1261-2.W.APP, Dec 2024)

nix-shell -p poppler-utils --run \
  "pdftotext -f 1 -l 1 -layout RX8130CE_cn-Register-Datasheet-m5stack-mirror.pdf -"
# ETM50E-09  -- and the body is English despite the _cn filename
```

> **A gotcha in the mechanical drawing.** `pdf/model-size.txt` comes back as
> `６２`, `１０１`, `４．８９` — the dimensions are typeset in **full-width CJK
> numerals**. The text is faithful; it is simply not comparable to ASCII digits
> without normalisation. Do not conclude the extraction failed.

### 2.3 Word bounding boxes — the input to the Altium tooling

| Field | Value |
|---|---|
| **Source / purpose** | Produce the per-page XML that the three schematic parsers consume. **Nothing in §3 works without this step** |
| **Working directory** | `scratch/m5stack-papermono/` |
| **Tool + version** | `pdftotext`, poppler 26.06.0 |
| **Generated files** | `pdf/bbox-p{1..6}.xml` (61 006 / 101 824 / 59 009 / 107 504 / 25 060 / 49 966 B) |
| **Status** | **`executed-success`** |
| **Date** | 2026-09-01 |

```bash
for p in 1 2 3 4 5 6; do
  nix-shell -p poppler-utils --run \
    "pdftotext -f $p -l $p -bbox pdf/PaperMono_SCH_V0.6.2_20260522.pdf pdf/bbox-p$p.xml"
done
```

### 2.4 Rasterising pages for human reading

| Field | Value |
|---|---|
| **Source / purpose** | Render sheets and manual pages as images so that extraction results could be **checked by eye** before being asserted. This is the verification step that makes §3 admissible |
| **Working directory** | `scratch/m5stack-papermono/` |
| **Tool + version** | `pdftoppm`, poppler 26.06.0 |
| **Generated files** | `sheets/sch-1.png`, `sheets/sch-2.png` (2339 × 1653 each) · `epd-pages/pg-01…pg-26.png` |
| **Status** | **`executed-success`** |
| **Date** | 2026-09-01 |

```bash
# schematic sheets 1-2 at 200 dpi -> 2339 x 1653 px for A4 landscape
nix-shell -p poppler-utils --run \
  "pdftoppm -f 1 -l 2 -r 200 -png pdf/PaperMono_SCH_V0.6.2_20260522.pdf sheets/sch"

# DKE panel manual, pages 1-10 at 130 dpi -> 1075 x 1521 px for A4 portrait
nix-shell -p poppler-utils --run \
  "pdftoppm -f 1 -l 10 -r 130 -png pdf/EPD_Module_User_Manual.pdf epd-pages/pg"

# the pinout and waveform pages again at 140 dpi, where 130 was not legible
nix-shell -p poppler-utils --run \
  "pdftoppm -f 15 -l 20 -r 140 -png pdf/EPD_Module_User_Manual.pdf epd-pages/pg"
```

Cropped renders of dense regions of sheet 2 (`sheets/p2-rails.png` 1498 × 1587,
`sheets/p2-chargeblock.png` 1511 × 1545) were produced the same way with
`pdftoppm`'s crop window:

```bash
nix-shell -p poppler-utils --run \
  "pdftoppm -f 2 -l 2 -r 200 -x <X> -y <Y> -W <W> -H <H> -png \
     pdf/PaperMono_SCH_V0.6.2_20260522.pdf sheets/p2-rails"
```

**Status for the crop specifically: `executed-success` in form, `inferred` in the
exact window.** The crop rectangles were chosen by eye, one region at a time, and
the individual `-x/-y/-W/-H` values were not recorded. The command shape is
reproducible; the precise framing of those two PNGs is not.

---

## Altium PDF tooling

Three parsers in [`tools/`](../../../tools/) recover structure from the published
schematic. They exist because of a **negative result**: `m5stack/M5_Hardware`
contains no C153 directory, so there is no `.kicad_pcb`, no `.SchDoc` and no
netlist — the PDF is the only schematic that exists.

**What they actually do.** Altium's PDF publisher emits *invisible* marker text at
schematic objects: `CO<designator>` at a component outline, `PI<designator><pin>`
at a pin instance, `NL<netname>` at a net label. Non-alphanumerics are replaced by
`0`, so the markers are lossy (`G0_BOOT_OUT` → `NLG00BOOT0OUT`) and serve only to
*locate* objects; the human-readable text beside them supplies the real name.

> ### Read this before trusting any output
>
> **These tools recover text adjacency, not electrical connectivity.** An
> unlabelled wire-only connection is invisible to them. Dense regions of sheet 2
> produced readings that had to be corrected against the rendered sheet (§2.4).
> **Every pin assertion in this record was cross-checked** either against a
> rendered sheet or against a second independent source — the vendor firmware,
> the vendor product page, or the DKE panel manual's own pinout. Where only the
> extraction supported a claim, the claim is marked `inferred`.

### Prerequisites common to all three

- `pdf/bbox-p{1..6}.xml` from §2.3, **in the current working directory**
- a `tools/` directory in the current working directory containing
  `altium_pdf_netlist.py` (the other two `sys.path.insert(0, 'tools')` and import
  from it)
- `python3` 3.14.7; **no third-party packages** — the parsers are pure standard
  library (`re`, `sys`, `math`, `json`, `html`)

> **Filename note, stated because it affects reproduction.** These were run from
> the scratch tree, where the same three files are named `altium_pdf_words.py`,
> `pin_table.py` and `render_sheet.py`. The copies now in [`tools/`](../../../tools/)
> are byte-identical apart from the renamed import
> (`altium_pdf_words` → `altium_pdf_netlist`) — verified by `diff`. The commands
> below are written against the **repository** names; the runs recorded as
> `executed-success` used the scratch names.

### 3.1 `altium_pdf_netlist.py` — marker classification and designator census

| Field | Value |
|---|---|
| **Source / purpose** | Parse the bbox XML into word records, split glued marker/text runs, and enumerate every reference designator in the document. Also the shared library for the other two tools |
| **Working directory** | `scratch/m5stack-papermono/` |
| **Tool + version** | `python3` 3.14.7 |
| **Expected output** | `total distinct designators: <n>` followed by a sorted JSON list |
| **Status** | **`executed-success`** |
| **Date** | 2026-09-01 |

```bash
python3 tools/altium_pdf_netlist.py
```

This is where the board-set finding came from: designators **restart per
document**, so the census contains three different `U1`s, two `X1`s and two
`ANT1`s. **A designator is meaningful only together with its sheet number** — the
PDF concatenates three separate Altium projects (main board, KEY/RGB sub-board,
NFC sub-board).

> **One regex detail is load-bearing.** The marker pattern uses a negative
> lookbehind, `(?<![A-Za-z])(CO|PI|NL)([A-Z0-9]+)`. Without it, `GPIO0` parses as
> `G` + a `PI` marker `O0`, and `SPI2_MOSI` as `S` + a `PI` marker `2` — which
> silently eats pin names on every MCU sheet. Altium emits each marker as its own
> text object, so a genuine marker is never preceded by a letter.

### 3.2 `altium_pdf_pin_table.py` — per-component pin/net table

| Field | Value |
|---|---|
| **Source / purpose** | For one component on one sheet, list every pin with the text inside the symbol body (the pin name) and the text outside it (the attached net). **This is the tool that produced the pin tables in [`pinouts-and-buses.md`](pinouts-and-buses.md) and resolved the `PYG` ambiguity** |
| **Working directory** | `scratch/m5stack-papermono/` |
| **Invocation** | `python3 tools/altium_pdf_pin_table.py <page> <designator> [row-band]` — the optional third argument is the vertical tolerance in points, default `3.5` |
| **Tool + version** | `python3` 3.14.7 |
| **Generated files** | `pins/p<page>-<designator>.txt` × 43 |
| **Status** | **`executed-success`** |
| **Date** | 2026-09-01 |

```bash
# the M5PM1 power-management coprocessor on sheet 2
python3 tools/altium_pdf_pin_table.py 2 U7 > pins/p2-U7.txt

# the M5IOE1 I/O expander on sheet 4 -- the other half of the PYG finding
python3 tools/altium_pdf_pin_table.py 4 U17 > pins/p4-U17.txt

# the ESP32-S3R8 on sheet 3
python3 tools/altium_pdf_pin_table.py 3 U12 > pins/p3-U12.txt

# the e-paper FPC connector on sheet 4, cross-checked against the DKE manual p.7
python3 tools/altium_pdf_pin_table.py 4 J5 > pins/p4-J5.txt

# everything that mattered, in one sweep
for spec in 2:U1 2:U2 2:U3 2:U4 2:U5 2:U6 2:U7 2:U8 2:U9 2:U10 2:U11 2:J1 2:J2 2:N2 \
            3:U12 3:U13 3:X1 3:FT1 3:ANT1 \
            4:U14 4:U15 4:U16 4:U17 4:U18 4:U19 4:U20 4:U21 4:J3 4:J4 4:J5 4:J6 4:BUZZER1 \
            5:LED1 5:S1 5:S2 5:S3 5:U1 \
            6:U1 6:U2 6:J1 6:X1 6:ANT1; do
  p="${spec%%:*}"; d="${spec##*:}"
  python3 tools/altium_pdf_pin_table.py "$p" "$d" > "pins/p${p}-${d}.txt"
done
```

Observed head of `pins/p2-U7.txt` — the rows that settled the naming question:

```
# U7 on sheet 2: 21 pin markers, x span 595..762
  pin |      x | inside symbol (pin name)            | outside (net / value)
--------------------------------------------------------------------------------
    3 |  595.0 | 3 G0_WAKEin(INT0/2)_IRQout_NEOPIXEL | PYG0_RTC_INT …
   12 |  595.0 | G4_WAKEin(INT3/4)_IRQout_PWM        | 12 PYG4_IMU_INT …
   13 |  595.0 | G3_WAKEin(INT3/4)_IRQout_PWM 唤醒源二选一 | 13 PYG3_BL_PWM …
   17 |  595.0 | G1_IRQout_ADC VCC                   | 17 G1_PY_IRQ …
   20 |  595.0 | G2_WAKEin(INT0/2)_IRQout_ADC 唤醒源二选一 | 20 PYG2_LoRa_EN …
```

On the M5PM1 the **symbol pin names** are `G<n>_…` and the **nets** are `PYG<n>_…`;
on the M5IOE1 (`p4-U17.txt`) it is the other way round. That inversion is the whole
of [`pin-naming-and-the-pyg-ambiguity.md`](pin-naming-and-the-pyg-ambiguity.md),
and it **refuted** an earlier conclusion in this same session that the vendor page
was defective.

Three empty results were also produced and are kept deliberately:
`pins/p2-U1.txt`, `p2-U2.txt`, `p2-U8.txt`, `p5-U1.txt`, `p6-U1.txt`,
`p6-U2.txt`, `p4-U18.txt`, `p4-U21.txt` are 32–33 bytes — the tool prints
`no pin markers for <D> on page <N>` and exits 0 rather than guessing.
**`executed-success` with an empty result is not `executed-failed`.**

### 3.3 `altium_pdf_render_sheet.py` — ordered text rendering of a sheet

| Field | Value |
|---|---|
| **Source / purpose** | Render a sheet as row-ordered text with the invisible markers stripped and re-attached inline as `[D.pin]` / `<D>`, so a whole sheet can be read — and a §3.2 result checked — without a PDF viewer |
| **Working directory** | `scratch/m5stack-papermono/` |
| **Invocation** | `python3 tools/altium_pdf_render_sheet.py <page> [row-tolerance]` — tolerance in points, default `3.0` |
| **Tool + version** | `python3` 3.14.7 |
| **Generated files** | `pdf/render-p{1..6}.txt` (6 256 / 8 340 / 5 176 / 8 421 / 2 196 / 4 147 B) |
| **Status** | **`executed-success`** |
| **Date** | 2026-09-01 |

```bash
for p in 1 2 3 4 5 6; do
  python3 tools/altium_pdf_render_sheet.py "$p" > "pdf/render-p$p.txt"
done

# a looser row tolerance for the dense power sheet
python3 tools/altium_pdf_render_sheet.py 2 4.0 | less
```

Observed head of `pdf/render-p2.txt`:

```
  31.6 | 1  2  3  4
  52.1 | TYPEC  PROTECTION  CHARG  ADC_DET
  62.6 | <U1>  <L1>  VBAT_L0
  69.9 | CC1  R1  [R10.1]  [R10.2]  NC/1%  [U10.2]  2  CC1  LX  [U10.11]  11  [L1.1]  [L1.2]
```

The `<U1>` and `[R10.1]` annotations are the tool's own — component outlines and
pin instances re-attached from the markers it stripped.

### 3.4 A fourth tool that exists in scratch but not in the repository

`scratch/m5stack-papermono/tools/altium_bom.py` builds a
designator → nearby-text report. It was **run** (`executed-success`) and used as a
cross-check on component values, but it was not promoted into
[`tools/`](../../../tools/) because adjacency to a component outline is a much
weaker signal than adjacency to a pin marker, and its output required more manual
correction than it saved. Recorded so nobody re-writes it.

---

## 4. M5Burner firmware retrieval

### 4.1 Recovering the API from the SPA bundle

| Field | Value |
|---|---|
| **Source / purpose** | The firmware pages are React shells with an empty `<div id="root">`. The download endpoint is not in the HTML |
| **Working directory** | `scratch/m5stack-papermono/docs/burner/` |
| **Tool + version** | `curl` 8.21.0, `grep` |
| **Status** | **`executed-success`** |
| **Date** | 2026-09-01 |

```bash
# 1. the page: 2735 bytes, no content
curl -sSL -A "$UA" 'https://burner.m5stack.com/firmware/2089640807996628993/' -o fw.html

# 2. follow the module graph: index -> http -> firmware
curl -sSL -A "$UA" 'https://burner.m5stack.com/assets/index-DpEo0Py5.js'    -o js-index.js
curl -sSL -A "$UA" 'https://burner.m5stack.com/assets/http-ChO34QIa.js'     -o js-http.js
curl -sSL -A "$UA" 'https://burner.m5stack.com/assets/firmware-C6nFrscE.js' -o js-firmware.js

grep -o 'var Kn = [^;]*' js-http.js
# var Kn = `${`/api`.replace(/\/$/,``)}/v1`
```

**The asset filenames are build-hashed and will change on the next deploy.** The
durable finding is the *shape*: the API base is `/api/v1`, and

```bash
curl -s -A "$UA" 'https://burner.m5stack.com/api/firmwares/2089640807996628993'
# {"msg":"请先登录"}    <- 401, auth-walled          [executed-failed, and that is the finding]

curl -s -A "$UA" 'https://burner.m5stack.com/api/v1/firmwares/2089640807996628993'
# 200, full JSON                                     [executed-success]
```

### 4.2 Public metadata

| Field | Value |
|---|---|
| **Source / purpose** | Establish firmware identity, source type, developer, version and `binFileName` — sources S33–S36 |
| **Working directory** | `scratch/m5stack-papermono/docs/burner/` |
| **Tool + version** | `curl` 8.21.0 |
| **Prerequisites** | None. **No authentication** |
| **Status** | **`executed-success`** |
| **Date** | 2026-09-01 |

```bash
for id in 2089640807996628993 2091144466157694978; do
  curl -sSL -A "$UA" "https://burner.m5stack.com/api/v1/firmwares/$id"          -o "api-$id-detail.json"
  curl -sSL -A "$UA" "https://burner.m5stack.com/api/v1/firmwares/$id/versions" -o "api-$id-versions.json"
done
```

Observed, and the reason [`README.md`](README.md) says the vendor's
"Factory Reset Firmware" link is mislabelled:

```json
"firmwareName": "PaperMono UserDemo",
"firmwareDescription": "PaperMono / PaperMono-Lite UserDemo",
"sourceType": "OFFICIAL"
```

— one image serves both SKUs, and it is a demo application, not a factory-reset
image.

### 4.3 Download, with content validation before naming

| Field | Value |
|---|---|
| **Source / purpose** | Retrieve the two firmware images (S38, S39) |
| **Working directory** | `scratch/m5stack-papermono/docs/firmware/` |
| **Tool + version** | `curl` 8.21.0, `od`/`sha256sum`/`stat` coreutils 9.11 |
| **Prerequisites** | The version ids from §4.2 |
| **Generated files** | `<name>.bin` and `<name>.bin.meta`; on failure `<name>.REJECTED.txt` |
| **Status** | **`executed-success`** — both images, `first_byte=0xe9`, **no rejections** |
| **Date** | 2026-09-01T05:05:22Z and 05:05:25Z |

```bash
# _tools/getfw.sh <firmwareId> <versionId> <outname>

# 1. the API 302s; capture the Location header rather than following it blind
api="https://burner.m5stack.com/api/v1/firmwares/${fid}/versions/${vid}/download"
loc=$(curl -sS -D - -o /dev/null -A "$UA" --max-time 30 "$api" \
      | tr -d '\r' | awk 'tolower($1)=="location:"{print $2}')

# 2. fetch to a temp file with NO extension
code=$(curl -sSL -A "$UA" --max-time 300 -o "$tmp" -w '%{http_code}|%{content_type}' "$loc")

# 3. validate by content, then and only then name it .bin
magic=$(od -An -tx1 -N1 "$tmp" | tr -d ' \n')      # must be e9
head -c 512 "$tmp" | grep -qiE '<html|<\?xml'      # must not match
[ "$(stat -c%s "$tmp")" -ge 4096 ] || exit 1
mv "$tmp" "${name}.bin"
```

Invoked as:

```bash
./_tools/getfw.sh 2089640807996628993 2089640808000823298 C153-PaperMono-UserDemo-v1.2
./_tools/getfw.sh 2091144466157694978 2091144466157694979 crosspoint-paper-mono-cjk-1.5.0-RC
```

Resulting `.meta`, verbatim:

```
api_url=https://burner.m5stack.com/api/v1/firmwares/2089640807996628993/versions/2089640808000823298/download
cdn_url=https://m5burner-cdn.m5stack.com/community/1/2089640807996628993/2089640808000823298/bin/2089640808000823299.bin
http_status=200
content_type=application/macbinary
bytes=2868208
sha256=72c290bc2ffa216041b276660277369bd17ecef92315e367d98bb2c96c8428fa
first_byte=0xe9
validation=ESP32-image(magic 0xE9)
retrieved_utc=2026-09-01T05:05:22Z
```

> **Note the CDN object name.** It is `2089640808000823299.bin` — the version id
> **plus one** — and bears no resemblance to the `binFileName` the API reports
> (`C153-PaperMono-ESP32S3R8-UserDemo-V1.2-yaozhenquan-8300e309-20260806_0x00.bin`).
> Naming the local file after the API's `binFileName` would have been reasonable
> and wrong; the local names are chosen and the mapping is recorded in the `.meta`.
> Also note `content_type: application/macbinary`, which is meaningless — one more
> reason to validate the bytes.

---

## 5. Firmware image inspection

| Field | Value |
|---|---|
| **Source / purpose** | Parse the ESP32 image header, the partition table at `0x8000` and `esp_app_desc_t` at `0x10020`; recover corroborating log strings |
| **Working directory** | `scratch/m5stack-papermono/docs/firmware/` |
| **Tool + version** | `python3` 3.14.7 (`_tools/espimg.py`, standard library only); `strings` (GNU binutils) |
| **Prerequisites** | The `.bin` files from §4.3. **`esptool` was not used and no serial port was opened** |
| **Generated files** | `esp-image-analysis.txt`, `*.strings.txt` |
| **Status** | **`executed-success`** — static analysis of a file on disk only |
| **Date** | 2026-09-01 |

```bash
python3 ../_tools/espimg.py C153-PaperMono-UserDemo-v1.2.bin       > esp-image-analysis.txt
python3 ../_tools/espimg.py crosspoint-paper-mono-cjk-1.5.0-RC.bin >> esp-image-analysis.txt

strings -n 6 C153-PaperMono-UserDemo-v1.2.bin > C153-PaperMono-UserDemo-v1.2.strings.txt
grep -E 'PaperMono|M5PM1|M5IOE1|BMI270|RX8130' C153-PaperMono-UserDemo-v1.2.strings.txt
```

Observed — and this is the **independent corroboration** of the pin map, because
it comes from the vendor's compiled artifact rather than the vendor's prose:

```
I (%lu) %s: [Autodetect] board_M5PaperMono
[I][%s] M5PM1 initialized at address 0x%02X (I2C: %lu Hz)
[I][%s] M5IOE1 initialized at address 0x%02X (I2C: %lu Hz)
I (%lu) %s: PM1 shutdown, wake by BMI270 INT1 -> PM1 G4 falling edge
I (%lu) %s: PM1 shutdown, wake by RX8130 timer  -> PM1 G0 falling edge
```

The last two confirm **M5PM1 G0 = RTC wake** and **M5PM1 G4 = IMU wake**, and that
these pins belong to the M5PM1 and not the expander. Note the firmware authors
write `PM1 G4`, not `PYG4` — the correct nomenclature, unlike the documentation.

`esp_app_desc_t` for the official image:

```
project_name  PaperMono-UserDemo
app_version   c78f6c5-dirty
build_date    Aug  6 2026  16:12:13
idf_version   v5.5.1
```

> **`-dirty` means this binary is not reproducible.** It was built from an
> uncommitted working tree, so no commit of `m5stack/M5PaperMono-UserDemo` will
> regenerate these bytes. That is why the image is retained in
> [`artifacts/firmware/`](artifacts/firmware/) rather than referenced by URL.

---

## 6. Source repository acquisition and verification

| Field | Value |
|---|---|
| **Source / purpose** | Acquire the vendor libraries and demos (S41–S47) and check two specific vendor claims |
| **Working directory** | `scratch/m5stack-papermono/repos/` |
| **Tool + version** | `git` 2.55.0; `gh` 2.97.0 for metadata |
| **Prerequisites** | `gh auth login` already done. **The token is never printed and appears nowhere in this repository** — reference it only as `$(gh auth token)` at point of use |
| **Status** | **`executed-success`** |
| **Date** | 2026-09-01 |

```bash
cd scratch/m5stack-papermono/repos

git clone https://github.com/m5stack/M5PaperMono-UserDemo.git
git clone https://github.com/m5stack/M5PaperMono-OTP-Demo.git
git clone https://github.com/m5stack/M5PM1.git
git clone https://github.com/m5stack/M5IOE1.git

# ~128 MB repo -- blobless, path search only
git clone --filter=blob:none --no-checkout https://github.com/m5stack/M5_Hardware.git

# both branches needed for the master/develop comparison
git clone https://github.com/m5stack/M5Unified.git && git -C M5Unified fetch origin develop:develop
git clone https://github.com/m5stack/M5GFX.git     && git -C M5GFX     fetch origin develop:develop

# metadata: default branch, HEAD, dates, licence, size
for r in M5PaperMono-UserDemo M5PaperMono-OTP-Demo M5PM1 M5IOE1 M5_Hardware M5Unified M5GFX; do
  gh api "repos/m5stack/$r" --jq '{name,default_branch,pushed_at,size,license:.license.spdx_id}'
done
```

Verification of the two headline findings:

```bash
# the negative: no C153 anywhere in the published hardware repo
git -C M5_Hardware ls-tree -r --name-only HEAD | grep -iE 'papermono|c153'
# -> no output, exit 1.  EXPECTED. This is the result, not a failure.

git -C M5_Hardware ls-tree -r --name-only HEAD | grep -oE 'C1[0-9]{2}' | sort -u | tail
# -> ... C149 C151 C152     (the SKU sequence stops one short of C153)

# the refutation: PaperMono support is on master AND in the release tags,
# so the vendor's "#develop" build requirement is stale
git -C M5GFX     grep -n 'board_M5PaperMono' master -- src/lgfx/boards.hpp
git -C M5Unified grep -q  'board_M5PaperMono' 0.2.21 -- src/ && echo "in tag 0.2.21"
git -C M5GFX     grep -q  'board_M5PaperMono' 0.2.28 -- src/ && echo "in tag 0.2.28"
```

**Nothing in these repositories was compiled, flashed or executed.** Every pin,
register and address taken from them is transcribed from source text at a cited
`file:line`.

> **Authenticate rather than rotate user agents.** `api.github.com` limits per
> identity: 60/h unauthenticated, **5 000/h** with a token. One recursive tree
> listing can exhaust 60 in a single call, and the resulting 403s carry
> `X-RateLimit-Remaining: 0` and look exactly like bot-blocking. Check that
> header before reaching for a UA.

---

## Vendor build and flash procedure

> ### `reported-working` — transcribed from vendor documentation, **not executed**
>
> No device exists in this session. Nothing below has been compiled, flashed,
> observed to boot, or observed to fail. It is reproduced so that the vendor's
> instructions can be compared against the vendor's own artifacts — which is how
> three of the conflicts in [`gaps-and-conflicts.md`](gaps-and-conflicts.md) were
> found.

| Field | Value |
|---|---|
| **Source** | [`docs.m5stack.com/en/arduino/papermono/program`](https://docs.m5stack.com/en/arduino/papermono/program) (S07) and the product page (S01) |
| **Working directory** | a PlatformIO or Arduino project directory — n/a here |
| **Shell / OS** | vendor does not state; Arduino IDE is cross-platform |
| **Tool + version** | Arduino IDE with the M5Stack board package; or PlatformIO with `platform = espressif32@6.12.0`. **The vendor states no Arduino IDE version and no board-package version anywhere** |
| **Prerequisites** | A PaperMono; a USB-C cable; the libraries below |
| **Expected output** | Sketch uploads; the example runs on the panel |
| **Status** | **`reported-working`** |
| **Date of transcription** | 2026-09-01 |

**1. Install the libraries.** The Arduino page names seven:

```
M5Unified   M5GFX   M5PM1   M5IOE1   M5UnitUnified   M5Unit-NFC   RadioLib
```

— "then install all prompted dependencies." **No versions are given for any of
them.** Note the conflict: `M5UnitUnified` is required here but absent from the
PlatformIO `lib_deps` on both product pages, while the product pages pin
`M5Unified` to `#develop`, which this page never mentions — and §6 above shows
that pin is unnecessary as of the snapshot date.

**2. Select the board.** *"Select the **M5PaperMono** board."* Independently
corroborated: the shipped binary contains `[Autodetect] board_M5PaperMono` (§5).

**3. Enter download mode.**

```
Press and hold the power button for about 2 seconds until the red LED flashes,
then release. The device is ready for firmware flashing.
```

That is the product page (S01) and the UiFlow2 page (S09), which agree. **The
Arduino page disagrees**, saying "the reset button on the side … until the side
LED starts blinking". The schematic shows three switches on the KEY/RGB sub-board
— `S1` (`PWR_BTN`), `S2` (`G2_KEY1`), `S3` (`G3_KEY2`) — and **no separate reset
button**, so the power-button reading is correct and the Arduino page is wrong.
`inferred`, `not-tested`.

**4. Upload.** The page says to open the **`BarGraph`** example and click Upload.
A bar-graph demo corresponds to none of the 14 advertised API sub-pages and reads
as boilerplate carried over from another product. Reproduced because it is what
the vendor says; flagged because it is probably not what you want.

**5. Power control**, from S01/S04:

```
Power on / reset : briefly press the power button once
Power off        : press the power button twice in succession
```

**Two `not-tested` hazards to know before you flash anything:**

- **Octal PSRAM is mandatory.** Without
  `board_build.arduino.memory_type = qio_opi`, M5GFX aborts display init with
  `"M5PaperMono need OPI-PSRAM enabled"` — a **blank screen on working hardware**
  with a single log line, which presents as dead hardware rather than as a build
  error.
- **Neither vendor project has an OTA partition.** The official image is a single
  15 360 K `factory` app. There is no field-update path as shipped.

---

## 8. The vendor PlatformIO configuration, verbatim

Reproduced exactly as published on the PaperMono product page (S01). **Status:
`reported-working`** — it is the only build configuration M5Stack publishes
anywhere, and it has not been built here.

```ini
[env:m5stack-papermono]
platform = espressif32@6.12.0
board = esp32-s3-devkitm-1
framework = arduino
board_build.partitions = default_16MB.csv
board_upload.flash_size = 16MB
board_upload.maximum_size = 16777216
board_build.arduino.memory_type = qio_opi
build_flags =
    -DESP32S3
    -DBOARD_HAS_PSRAM
    -mfix-esp32-psram-cache-issue
    -DCORE_DEBUG_LEVEL=0
    -DARDUINO_USB_CDC_ON_BOOT=1
    -DARDUINO_USB_MODE=1
lib_deps =
    M5Unified = https://github.com/m5stack/M5Unified#develop
    M5PM1 = https://github.com/m5stack/M5PM1
    M5IOE1 = https://github.com/m5stack/M5IOE1
    M5Unit-NFC=https://github.com/m5stack/M5Unit-NFC
    RadioLib = https://github.com/jgromes/RadioLib
```

The PaperMono-Lite page (S04) publishes the same block with two differences and
nothing else: the environment is `[env:m5stack-papermono-lite]`, and
`M5Unit-NFC` and `RadioLib` are absent from `lib_deps`.

Four observations about this block, all `inferred` from evidence elsewhere in
this record:

1. **`board = esp32-s3-devkitm-1`** — there is no PlatformIO board definition for
   the PaperMono; a generic devkit board is used and reconfigured by the flags.
2. **`board_build.arduino.memory_type = qio_opi`** selects QIO flash + OPI PSRAM.
   The **shipped factory binary's header reports flash mode `DIO`.** The hardware
   supports QIO — all four data lines are routed and the flash's `QE` bit is set
   at the factory — and `sdkconfig.defaults` in the vendor's own ESP-IDF project
   pins no flash mode, so the DIO header is an IDF default rather than a hardware
   limit. Documented build config and vendor artifact nonetheless disagree.
3. **`M5Unified#develop`** is stale — see §6.
4. **`M5UnitUnified` is missing**, though the Arduino page requires it.

For comparison, the vendor's actual ESP-IDF factory-firmware project (S41) does
**not** use PlatformIO at all: it is ESP-IDF **5.5.1** with arduino-esp32
**3.3.10** as a managed component, and it pins ten dependencies at exact commits
in `repos.json` — including `RadioLib` 7.2.1 at `b91c6af112e423dcb14529ade5827802a14e1015`,
`M5GFX` `develop` at `02107b828acb3eb782fccd747863638d64c876d7` and `M5Unified`
`develop` at `2fe93c0c64f12f916e73a0605c86bf1241c06a6b`. **That, not the
PlatformIO block, is what actually built the shipped image** — and even it will
not reproduce it, because the image is `-dirty`.

---

## Related

- [`sources.md`](sources.md) — every artifact these commands produced or consumed
- [`research-log.md`](research-log.md) — what was searched, and the retrieval gotchas
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — the conflicts these commands surfaced
- [`../../../tools/`](../../../tools/) — the parsers themselves
