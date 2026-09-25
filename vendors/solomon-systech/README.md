# Solomon Systech — Documentation Sourcing Guide

Reusable knowledge for obtaining documentation for Solomon Systech display-controller ICs, and for
**not being fooled by what you get back.**

> **TL;DR — the one thing to take away.**
> **Mirror-sourced Solomon Systech PDFs arrive misnamed, and they arrive misnamed silently.**
> HTTP 200, valid `%PDF` magic, plausible file size, wrong part. **Identify every Solomon Systech
> PDF by the text on its first page before you file it, name it, or cite it.** Filenames lie,
> `Title` metadata lies, and on the most productive mirror the *URL itself* lies. §2.

Created **2026-09-20**, from a pass that filed five Solomon Systech datasheets — of which **two had
the wrong part number in the filename** and **one had the wrong part number in its own PDF
metadata**.

---

## 1. Who they are

Solomon Systech Limited (晶門半導體, Hong Kong; HKEX: 2878) is a fabless designer of display driver
and controller ICs. Its `SSD` family spans monochrome LCD, OLED/PLED, TFT, e-paper and — more
recently — display-plus-touch combination parts.

Two commercial facts drive everything in this guide:

1. **They sell gold-bump die on waffle pack, not packaged parts.** Every e-paper and OLED controller
   documented here ships as **COG (chip-on-glass)**: bare die, 250–300 µm thick, bonded to panel
   glass by a module house. You never buy one. You buy a panel module with one already bonded
   inside — which is why fitment on a finished board is almost always established from a *module*
   datasheet, a driver source file or a firmware probe rather than from a chip marking.
2. **Their customer is the module house, under NDA.** Solomon Systech therefore has no commercial
   reason to serve public register-level documentation, and largely does not. Everything in
   circulation is a courtesy copy hosted downstream: by a distributor, a module vendor, or a board
   vendor who needed it to write a driver.

This is the same structural situation as [Sitronix](../sitronix/README.md) §3 and
[UltraChip](../../components/ultrachip/uc8279/README.md), and it produces the same symptom: the
documents exist, but never where the part number says they should be.

---

## 2. ⚠ Retrieval finding — Solomon Systech PDFs arrive misnamed. Verify by first-page text.

**This section exists because it cost this repository nine days and two wrong filings.**

### 2.1 What happened

A research pass on 2026-09-11 fetched five Solomon Systech datasheets into scratch. On
**2026-09-20** their contents were checked against their filenames for the first time:

| Filename on disk | What the file **actually is** | Pages |
|---|---|---|
| **`ssd1680.pdf`** | ⚠ **SSD7317** — 128 × 96 OLED/PLED driver with integrated touch controller. *Not an e-paper part at all* | 87 |
| **`ssd1677.pdf`** | ⚠ **SSD1681** — 200 Source × 200 Gate EPD controller | 41 |
| `ssd1683.pdf` | SSD1683 ✅ — but its **PDF `Title` metadata says `SSD1780`** | 49 |
| `SSD1680_gh.pdf` | SSD1680 ✅ | 46 |
| **`ssd1677_real.pdf`** | SSD1677 ✅ | 46 |

**Two of five had the wrong part in the filename. A third had the wrong part in its own metadata.**

The `_real` suffix on the fifth file is the tell: the acquiring session *had already hit this*,
refetched the correct document, and saved it under a new name **without renaming the bad one**. The
wrong `ssd1677.pdf` then sat in scratch looking authoritative.

### 2.2 Why it happens — three independent mechanisms

**(a) The mirror's URL path is decorative.** Crystalfontz serves controller datasheets at
`https://www.crystalfontz.com/controllers/<Vendor>/<Part>/<id>/`, and **only the trailing numeric
`<id>` selects a document.** `<Vendor>` and `<Part>` are ignored. A request naming `SSD1680` with
the wrong id returns a different part's datasheet with **HTTP 200, `Content-Type: application/pdf`
and a valid `%PDF` header**. Nothing in the response indicates the mismatch.

> This trap was **already recorded** in
> [`ai-crawler-site-access-table.md` § `crystalfontz.com`](../../ai-crawler-site-access-table.md)
> before this pass — *"the URL lies… Check `pdfinfo`'s `Title` before filing anything from this
> host"* — from an occasion when `…/UltraChip/UC8179/478/` returned the **GOODiX GT911 Programming
> Guide**. The 2026-09-11 pass hit it again. **A documented trap is not a prevented trap.**
> Confirmed live 2026-09-20, `executed-success`.

**(b) `pdfinfo Title` is not sufficient either.** The advice above is good but incomplete for this
vendor. The SSD1683 datasheet's `Title` field reads **`SSD1780`** — a part number that appears
nowhere in its 49 pages. It is a stale Microsoft Word document property, `Author: ivanl`. A
2026-09-11 Crystalfontz document-id probe recorded in
[`components/ultrachip/uc8279`](../../components/ultrachip/uc8279/README.md) duly reported *"SSD1780"*
among the documents it found — **there is no such part; it is the SSD1683.** Corrected here with
evidence and date, per the conflict protocol; the UC8279 record's own conclusion is unaffected.

Other `Title` fields observed on this vendor's files in this repository:
`SSD1681_0.13 Holitech` (a *panel maker's* name, not Solomon Systech's), `SSD1680`, `SSD1780`, and
— on both SSD1677 copies — **no `Title` at all**.

**(c) The part numbers are four digits apart and easy to transpose.** `SSD1677` / `SSD1680` /
`SSD1681` / `SSD1683` / `SSD1673` are five *different* EPD controllers with five *different* LUT
formats. `SSD1780` does not exist. `SSD7317` is not even an e-paper part. There is no visual cue in
the number to tell you which is which.

### 2.3 The rule

**Verify by first-page text. Always. It costs one command:**

```bash
nix shell nixpkgs#poppler-utils --command pdftotext -layout -f 1 -l 2 IN.pdf - | head -30
```

The cover of a genuine Solomon Systech datasheet is unambiguous and machine-checkable:

```
SOLOMON SYSTECH
SEMICONDUCTOR TECHNICAL DATA

                    SSD1681                 ← the part number, on its own line

              Product Preview               ← or "Advance Information"
   200 Source x 200 Gate Red/Black/White
Active Matrix EPD Display Driver with Controller

SSD1681   Rev 0.13   P 1/41   Jun 2019   Copyright © 2019 Solomon Systech Limited
```

**Then cross-check the footer.** Every page carries `<PART>  Rev <x.y>  P <n>/<total>  <Mon> <Year>`.
That single line gives you part, revision, date **and** a page-integrity check for free:

```bash
# Confirms PDF page index == printed footer page for every page.
# A mismatch means a page was dropped upstream.
nix shell nixpkgs#poppler-utils --command pdftotext -layout IN.pdf - \
  | python3 -c "
import sys,re
for i,p in enumerate(sys.stdin.read().split('\f')):
    m=re.search(r'(SSD\w+)\s+Rev ([\d.]+)\s+P (\d+)/(\d+)',p)
    if m and i+1!=int(m.group(3)): print('MISMATCH pdf page',i+1,'-> footer',m.group(3))
"
```

This is not theoretical. Run on the SSD1677 it reports a mismatch from page 2 onward, which proved
that **printed page 2 — the revision-history page — is missing from every known copy of that
datasheet**. See [SSD1677 §7-C8](../../components/solomon-systech/ssd1677/README.md#7-caveats-errata-and-conflicts).
Run on the SSD1680, SSD1681 and SSD1683 it reports clean, 46/46, 41/41 and 49/49.

### 2.4 And check whether it is one document at all

**`ssd7317-…-crystalfontz-mirror.pdf` is 87 pages containing four separate documents** at three
different revisions: a 37-page datasheet (Rev 1.3, Oct 2020), a 13-page **SPI Software Porting User
Guide** (Rev 1.0, Apr 2019), a 13-page **I²C Software Porting User Guide** (Rev 1.1, Aug 2019) and a
24-page appendix set. Nothing in the filename, the metadata or the first page says so.

The footer census above finds this automatically: the pagination **restarts** at `P 1/13` on page 38
and again on page 51, and becomes `P n/24` on page 64. **If total-page-count changes mid-file, you
have a bundle**, and the extra documents may be the only copies in circulation — the two SSD7317
porting guides are not indexed anywhere else this pass could find, and they contain the *only*
description of the part's mandatory firmware-download protocol.

### 2.5 Watch for OCR'd scans

**`SSD7317` Rev 1.3 is a scan with an OCR text layer, and the OCR is wrong in ways that look
right.** `VDD` extracts as `Yoo`, `VCI` as `Ver`, `I²C` as `PC` or `re`, `16-Oct-19` as `16-0ct-19`,
and the part number itself as `S8D7317`, `SSD731 7` and `lss07317`. Twenty-four appendix pages are
non-recoverable mojibake.

**Tell:** genuine Solomon Systech exports carry a `Creator`/`Producer` pair such as
`PDFCreator` + `GPL Ghostscript`, or `Microsoft® Word` + `PDFill`. **A file with no `Creator` and no
`Producer` at all is a scan-and-recombine.** Cross-check any value you transcribe from one against a
second occurrence in the document, and read dense numeric tables from rendered page images.

---

## 3. Where documents actually come from

Ordered by how likely you are to succeed.

| Rank | Source | Pattern | Notes |
|---|---|---|---|
| 1 | **Crystalfontz controller library** | `https://www.crystalfontz.com/controllers/<Vendor>/<Part>/<id>/` | ✅ **Best single source for this vendor.** 33 Solomon Systech documents. ⚠ **Only `<id>` matters** (§2.2a). Plain `curl`, no UA games needed — verified 2026-09-20 |
| 2 | **Board-vendor product-page attachments** | e.g. `static-cdn.m5stack.com/resource/docs/products/…` | ✅ How the [SSD1677](../../components/solomon-systech/ssd1677/README.md) was obtained, and **the only known source for it** |
| 3 | **Panel/module-maker copies** | Varies | The module house that bonded the die sometimes ships the controller datasheet alongside its module spec. The SSD1681 copy here passed through **Holitech** — visible only in its `Title` metadata |
| 4 | **GitHub repositories** | Driver projects vendoring the datasheet they worked from | How the SSD1680 copy here appears to have been obtained (`_gh` suffix; **URL not recorded** — record your URLs) |
| 5 | **Driver source as documentation** | GxEPD2, Waveshare/Good Display demos, vendor BSPs | For this family, working init sequences are often more reliable than the datasheet's own flow — see §5 |
| 6 | **Solomon Systech itself** | `solomon-systech.com` | Product *listings* and brief selection tables. **Register-level datasheets: behind a registration wall.** Not obtained by this pass |

### 3.1 Enumerating everything Crystalfontz has — the useful recipe

The controller index embeds a **JSON catalogue** in the page source. Do not scrape the rendered
accordion; parse the JSON. Verified `executed-success`, 2026-09-20:

```bash
curl -sS https://www.crystalfontz.com/controllers/ -o cf.html      # 200, ~105 KB, plain UA
python3 - <<'EOF'
import re
h = open('cf.html', encoding='utf8', errors='replace').read()
for m in re.finditer(r'\{"id":(\d+),"name":"(SSD[^"]*)","version":"([^"]*)"', h):
    print(m.group(1), m.group(2), m.group(3))
EOF
```

Each entry carries `id`, `name`, `version` and a `summary` that is the datasheet's own subtitle —
**so you can confirm the part, the revision and the resolution before downloading anything.** Then
fetch by id; the `<Vendor>`/`<Part>` segments can be anything.

### 3.2 Solomon Systech document ids — live-verified 2026-09-20

Complete catalogue section, 33 entries (`executed-success`):

| id | Part | Ver | | id | Part | Ver | | id | Part | Ver |
|---:|---|---|---|---:|---|---|---|---:|---|---|
| 335 | SSD1289 | 1.1 | | 434 | SSD1327 | 1.8 | | 346 | SSD1801 | 1.1 |
| 336 | SSD1298 | 1.1 | | 381 | SSD1331 | 1.2 | | 347 | SSD1803 | 0.2 |
| 337 | SSD1303 | 1.7 | | 380 | SSD1332 | 2.3 | | 411 | SSD1805 | 1.4 |
| 338 | SSD1305 | 2.1 | | 345 | SSD1339 | 1.1 | | 348 | SSD1815 | 1.5 |
| 339 | SSD1306 | 1.1 | | 448 | SSD1351 | 1.5 | | 349 | SSD1815B | 1.6 |
| 443 | SSD1306B | 1.1 | | 490 | SSD1362 | 1.0 | | 350 | SSD1851 | 1.2 |
| 340 | SSD1307 | 1.4 | | **410** | **SSD1673** | **0.21** | | 351 | SSD1963 | 1.6 |
| 341 | SSD1308 | 1.0 | | **497** | **SSD1680** | **0.14** | | 352 | SSD2119 | 1.4 |
| 342 | SSD1309 | 1.1 | | **500** | **SSD1681** | **0.13** | | **469** | **SSD7317** | **0.11** |
| 450 | SSD1320 | 1.0 | | **514** | **SSD1683** | **1.0** | | **498** | **SSD7317** | **1.3** |
| 427 | SSD1322 | 1.2 | | 343 | SSD1325 | 2.3 | | | | |

**Four facts worth carrying forward:**

- ⚠ **There is no `SSD1677` entry.** Confirmed by full enumeration, not by a failed search. The most
  productive mirror for this vendor **does not have** the controller that is actually fitted on
  hardware in this repository. Fetching "SSD1677" from this host **cannot** succeed, and will return
  something else with a 200.
- ⚠ **There is no `SSD1780` entry** — that string is the SSD1683's stale `Title` metadata (§2.2b).
- **`SSD7317` appears twice**, at two revisions (id 469 = v0.11, id 498 = v1.3). Where a part has
  multiple ids, **take the highest version, not the lowest id.**
- **`SSD1673` (id 410, v0.21)** is a fifth EPD controller in this family — 150 × 250 — **not held
  here**. Recorded as a known, unfetched document.

### 3.3 Crystalfontz serves re-optimised derivatives

Two of the copies retained in this repository are **larger** than Crystalfontz's and have earlier
`ModDate`s. Compared byte-for-byte and text-for-text, 2026-09-20:

| Part | Copy retained here | Crystalfontz copy | Verdict |
|---|---|---|---|
| **SSD1680** | 2 759 375 B, `b28ec2b4…`, ModDate 2020-05-06, `Optimized: no` | 857 636 B, `c6d3090b…`, ModDate 2021-05-10, `Optimized: yes` | **Same document.** Identical `CreationDate`, `Creator`, `Producer`, 46 pages; whitespace-normalised text **byte-identical** |
| **SSD1683** | 3 931 534 B, `77c188ba…`, ModDate 2021-04-20, `Optimized: no` | 1 877 699 B, `f40921ac…`, ModDate 2025-07-21, `Optimized: yes` | **Same document.** Same test, same result |

**So a hash mismatch against a Crystalfontz copy does not mean you have a different revision.** Check
`CreationDate` + `Creator` + `Producer` + page count first, then compare normalised text. If those
match, you are looking at Crystalfontz's optimisation pass, not a vendor re-issue. **Record the other
hash in the component record** so the next agent recognises the file instead of re-deriving the
comparison.

---

## 4. Part numbering

```
SSD 16 8 1
│   │  │ └─ variant / size index within the generation
│   │  └─── generation
│   └────── family class
└────────── Solomon Systech prefix
```

Conventions that hold across the parts documented here — **[inference]**, no Solomon Systech
numbering document is public:

| Prefix | Class | Examples |
|---|---|---|
| `SSD12xx` / `SSD13xx` | **OLED/PLED** segment/common drivers | `SSD1306`, `SSD1309`, `SSD1327`, `SSD1351`, `SSD1362` |
| `SSD16xx` | **Active-matrix EPD** (e-paper) drivers with controller | `SSD1673`, `SSD1677`, `SSD1680`, `SSD1681`, `SSD1683` |
| `SSD18xx` | Monochrome **LCD** segment/common drivers | `SSD1801`, `SSD1815`, `SSD1851` |
| `SSD19xx` / `SSD2xxx` | **TFT** LCD controllers | `SSD1963`, `SSD2119`, `SSD1289` |
| `SSD73xx` | **Display + integrated touch** combination parts | `SSD7317` |

⚠ **Within `SSD16xx`, the number does not order by size or capability.** `SSD1677` is 960 × 680;
`SSD1680` is 176 × 296; `SSD1681` is 200 × 200; `SSD1683` is 400 × 300. **`SSD1677` is the largest
and has the lowest number.** Do not infer geometry, generation or feature set from the digits.

**Die suffixes:** `Z` = gold bump die, **bump face up**; `Z8` = gold bump die, **bump face down**.
Both ship on waffle pack. The suffix is a bonding-orientation choice made by the module house, not a
functional variant.

---

## 5. ⚠ "SSD16xx" is not one command set

The single most expensive assumption you can make about this vendor. Established from the four
primary documents now held:

| | [SSD1677](../../components/solomon-systech/ssd1677/README.md) | [SSD1680](../../components/solomon-systech/ssd1680/README.md) | [SSD1681](../../components/solomon-systech/ssd1681/README.md) | [SSD1683](../../components/solomon-systech/ssd1683/README.md) |
|---|---:|---:|---:|---:|
| Max geometry | 960 × 680 | 176 × 296 | 200 × 200 | 400 × 300 |
| **`0x32` LUT write** | **105 B** | **153 B** | **153 B** | **227 B** |
| Waveform setting total | 112 B | 159 B | 159 B | 233 B |
| Waveform phases | **40** (4 × 10 groups) | **48** (4 × 12) | **48** (4 × 12) | **32** (4 × 8) |
| Frame-rate control | per group | **per group (`FR[0..11]`)** | per group | **one global `FR` byte** |
| **RAM X addressing** | ⚠ **pixels** (POR `XEA=0x3BF`) | **bytes** (POR `0x15`) | **bytes** (POR `0x15` ⚠ *wrong*) | **bytes** (POR `0x31`) |
| **Temperature value** | 12-bit | **12-bit** (1/16 °C) | **12-bit** | ⚠ **8-bit** (1 °C) |
| TR entry size | 3 B | 3 B | 3 B | **2 B** |
| OTP WS / TR slots | **34 / 34** | **36 / 36** | **36 / 36** | **24 / 24** |
| `0x0C` soft-start | ⚠ **5 bytes, no bit table published** | 4 bytes, **fully decoded** | 4 bytes, decoded | 4 bytes, decoded |
| `0x21` byte `B` | — | `B[7]` source output mode | ⚠ **named, undefined** | `B[4]` cascade enable |
| Cascade mode | no | **yes** (352 × 296) | **no** (pins vestigial) | **yes** (800 × 300) |
| Deep-sleep modes | ⚠ **1 documented** (`11`) | **2** (`01`, `11`) | **2** | **2** |

**Consequences that bite:**

- **A LUT is not portable.** Three different byte counts, three different internal layouts.
- **A windowing routine is not portable.** The SSD1677 counts RAM X in pixels; the rest count bytes.
- **A temperature routine is not portable to/from the SSD1683.** 8-bit versus 12-bit, 1 °C versus
  1/16 °C.
- **A power budget is not portable.** SSD1683 deep sleep is ~3× the SSD1680's.
- **Only `0x0C` is genuinely common** — and it is the one command the SSD1677 does *not* document,
  which is precisely why the siblings were worth acquiring. See
  [`devices/m5stack/papermono/gaps-and-conflicts.md`](../../devices/m5stack/papermono/gaps-and-conflicts.md).

### 5.1 Documentation-quality traps that recur across this vendor

Observed on at least two parts each, so treat them as vendor-level rather than per-document:

- **Datasheets are derived by editing a sibling's, and values get left behind.** The SSD1681's RAM
  window defaults are the SSD1680's (176 × 296 on a 200 × 200 part). The SSD1683's 8-bit temperature
  rules still refer to *"MSByte bit D11"*. The SSD7317 says its 12-page GDDRAM is *"divided into
  eight pages"* — the SSD130x number. **Sanity-check every POR value against the part's own
  geometry.**
- **Everything is "Advance Information" or "Product Preview", and stays that way for years.**
  SSD1677 Rev 1.0 is from 2018 and is still the only revision; SSD1680 Rev 0.14 and SSD1681 Rev 0.13
  are from 2019; SSD1683 Rev 1.0 from 2021. **There is no "final" datasheet to wait for.**
- **`0x22` Display Update Control 2 values are a bit-field whose bits are never defined.** Twelve
  composite values are tabulated on every EPD part. **Copy a tabulated value; never compose one.**
- **Commands routinely defer to application notes that are not public** — initial code setting, CRC
  calculation, OTP programming sequences, and on the SSD1683 a waveform *password*. **OTP
  programming is not achievable from any public Solomon Systech document.**
- **Feature lists under-report the command table.** The SSD1681 omits six capabilities its own
  register map implements. **Census the command table; do not trust page 5.**
- **A `TBD` is not an omission, it is the spec.** Fourteen of sixteen SSD1681 SPI timing parameters
  and all three of its current maxima are literally `TBD`.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| Mouser / Digi-Key | ❌ Essentially none |
| LCSC | ⚠ Occasional COG die listings; not the general case |
| **Panel module houses** | ✅ **The real channel.** DKE, Good Display, Holitech, Waveshare and others bond the die and sell you glass |
| AliExpress / Taobao | ✅ As finished e-paper or OLED modules, effectively never as loose die |

**Practical consequence, identical to [Sitronix](../sitronix/README.md) §6:** you do not choose a
Solomon Systech part, you choose a panel — and the controller inside can change between production
runs of the same module part number. This repository has the worked example: the
[Xteink X4 family](../xteink/README.md) ships with an **SSD1677 *or* an UltraChip
[UC8179](../../components/ultrachip/uc8179/README.md)/[UC8279](../../components/ultrachip/uc8279/README.md)**
on identical wiring, with **no external marking** to tell them apart.

### 6.1 The family's most useful identification trait

**UC81xx parts answer `VER (0x70)` and `FLG (0x71)` register reads. Solomon Systech `SSD16xx` parts
do not** — a released data line floats to a uniform `0x00`/`0xFF` on an SSD part and returns a
driven, structured pattern on a UC81xx. That asymmetry is what makes runtime controller detection
possible on boards shipping more than one variant. See
[`components/ultrachip/uc8179`](../../components/ultrachip/uc8179/README.md) and
[SSD1677 §10](../../components/solomon-systech/ssd1677/README.md#10-used-by).

⚠ Note the corollary for *documentation* work: **you cannot ask an SSD16xx what it is.** Identity
comes from the module datasheet, the driver source, or the schematic — never from the chip.

---

## 7. Licensing and redistribution

Consistent across all six Solomon Systech artifacts now held:

- Covers carry a plain `Copyright © <year> Solomon Systech Limited`.
- **None carries a per-page confidentiality footer**, unlike [Goodix](../goodix/README.md)'s GT911
  guide (*"strictly prohibited without written consent"*) or UltraChip's *"for TFT module use only"*
  stamp. **No redistribution term has been observed on any Solomon Systech document in this
  repository.**
- The only per-page stamp seen is **Crystalfontz's own** *"Downloaded from
  www.crystalfontz.com/controllers"* — a **mirror watermark added by the distributor**, not a
  restriction by the rights-holder.

All six are therefore recorded as redistribution status **`unknown`** (nothing stated), disposition
**`repository`**. This is the common and unproblematic case.

---

## 8. Per-part checklist

When adding a new Solomon Systech part, in order:

1. **Enumerate the Crystalfontz JSON catalogue first** (§3.1). It tells you whether the document
   exists, at what revision, and under which id — **before** you download anything. If the part is
   absent (as `SSD1677` is), stop and look at board-vendor product pages instead.
2. **Fetch by id.** Ignore the `<Vendor>`/`<Part>` segments; they do nothing.
3. **Identify by first-page text**, never by filename or `Title` (§2.3).
4. **Run the footer census** (§2.3). It gives you part, revision, date, page integrity and
   bundle detection in one pass.
5. **Check `Creator`/`Producer`.** Absent ⇒ scan ⇒ the text layer is OCR ⇒ corroborate every value
   (§2.5).
6. **Hash it, and compare against the Crystalfontz copy** if you obtained it elsewhere. A mismatch is
   usually re-optimisation, not a new revision (§3.3) — but **prove it** before keeping only one.
7. **Sanity-check POR values against the part's own geometry** before transcribing them (§5.1).
8. **Census the command table**; do not trust the feature list (§5.1).
9. **Record the acquisition URL.** Two of the six files here have `unknown` provenance purely because
   nobody wrote it down.

---

## 9. Parts and records

| Record | Type | Status |
|---|---|---|
| [**SSD1677**](../../components/solomon-systech/ssd1677/README.md) | 960 × 680 EPD driver + controller | ✅ **Fitted on hardware** — [M5Stack PaperMono](../../devices/m5stack/papermono/README.md) and [Lite](../../devices/m5stack/papermono-lite/README.md), [Waveshare ESP32-S3-ePaper-3.97](../../devices/waveshare/esp32-s3-epaper-3.97/README.md), [Xteink X4 / X4 Pro / X4 Classic](../../devices/README.md). **Two copies held**; ⚠ absent from Crystalfontz |
| [**SSD1680**](../../components/solomon-systech/ssd1680/README.md) | 176 × 296 EPD driver + controller | Reference-only. **The family's decodable reference command set** |
| [**SSD1681**](../../components/solomon-systech/ssd1681/README.md) | 200 × 200 EPD driver + controller | Reference-only. ⚠ Datasheet carries inherited SSD1680 values |
| [**SSD1683**](../../components/solomon-systech/ssd1683/README.md) | 400 × 300 EPD driver + controller | Reference-only. ⚠ `Title` metadata says `SSD1780` |
| [**SSD7317**](../../components/solomon-systech/ssd7317/README.md) | ⚠ **128 × 96 OLED + in-cell touch** | Reference-only, **acquired by mistake**. 4-document bundle; OCR'd scan |
| `SSD1673` — 150 × 250 EPD | — | **Known, not held.** Crystalfontz id 410, v0.21 |
| `SSD7317` v0.11 | — | **Known, not held.** Crystalfontz id 469 |

**No device in this repository is manufactured by Solomon Systech.** The company makes silicon that
arrives inside other people's panels.

---

## 10. Sources

| ID | Title | Class | URL / path | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | Crystalfontz controller catalogue | credible mirror | `https://www.crystalfontz.com/controllers/` | **2026-09-20** | §3.1–§3.2 — the embedded JSON catalogue, all 33 Solomon Systech ids, and the **absence of SSD1677 and SSD1780**. HTTP 200, plain UA, 104 682 B |
| S2 | Crystalfontz document fetches, ids 497 / 500 / 514 / 498 | credible mirror | `https://www.crystalfontz.com/controllers/Solomon%20Systech/<Part>/<id>/` | **2026-09-20** | §3.3 — all four HTTP 200 `application/pdf`; ids 500 and 498 **byte-identical** to files held; 497 and 514 are re-optimised derivatives |
| S3 | `ai-crawler-site-access-table.md` § `crystalfontz.com` | this repository | [`../../ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md) | 2026-09-20 | §2.2a — the decorative-path trap, recorded 2026-09-11 and re-confirmed here |
| S4 | SSD1677 / SSD1680 / SSD1681 / SSD1683 / SSD7317 datasheets | primary / credible mirror | the five component records in §9 | 2026-09-01, 2026-09-11, **2026-09-20** | §2, §4, §5, §5.1, §7 — every cross-part comparison |
| S5 | `components/ultrachip/uc8279` — Crystalfontz id probe | this repository | [`../../components/ultrachip/uc8279/README.md`](../../components/ultrachip/uc8279/README.md) | 2026-09-20 | §2.2b — the *"SSD1780"* probe result, **now corrected**: id 514 is catalogued as SSD1683 v1.0 |
| S6 | Sitronix sourcing guide | this repository | [`../sitronix/README.md`](../sitronix/README.md) | 2026-09-20 | §1, §6 — the identical module-house commercial structure, named for comparison |

> **Evidence boundary.** S1 and S2 are **live fetches performed 2026-09-20**, `executed-success`:
> they establish what Crystalfontz served on that date, with hashes. They do **not** establish that
> Solomon Systech publishes nothing elsewhere — `solomon-systech.com` was **not probed in this
> pass**, and the claim that its register-level datasheets sit behind a registration wall is
> **inherited from the [SSD1677 record](../../components/solomon-systech/ssd1677/README.md) §12
> (2026-09-01)** and is `not-tested` here. §4 (numbering) is explicitly **[inference]**. §5's
> comparison table is transcribed from four primary datasheets whose text layers were each
> page-by-page validated; the SSD7317's was **not** (§2.5), and no SSD7317 value appears in §5.

---

## Related

- [Vendor guide index](../README.md)
- [SSD1677](../../components/solomon-systech/ssd1677/README.md) · [SSD1680](../../components/solomon-systech/ssd1680/README.md) · [SSD1681](../../components/solomon-systech/ssd1681/README.md) · [SSD1683](../../components/solomon-systech/ssd1683/README.md) · [SSD7317](../../components/solomon-systech/ssd7317/README.md)
- [DKE](../dke/README.md) — the module house that bonds SSD1677 die into the PaperMono panel
- [E Ink Holdings](../e-ink/README.md) — ⚠ *"If you are expecting an SSD1680-style command set, you have the wrong mental model"*: E Ink's parallel AMEPD panels have **no controller at all**
- [Sitronix](../sitronix/README.md) — same commercial structure, same documentation problem
- [Waveshare](../waveshare/README.md) — a board vendor that mirrors controller datasheets, often stale
- [`guides/hardware/e-paper-displays.md`](../../guides/hardware/e-paper-displays.md) — integrated-controller modules versus raw parallel panels
- [`components/ultrachip/uc8179`](../../components/ultrachip/uc8179/README.md) · [`uc8279`](../../components/ultrachip/uc8279/README.md) — the competing family, and the `VER`/`FLG` detection asymmetry
