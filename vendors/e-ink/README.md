# E Ink — Documentation Sourcing Guide

Reusable knowledge for obtaining documentation about **E Ink Holdings** electrophoretic display panels.

> **TL;DR** — E Ink publishes **no public datasheets for AMEPD panels** and **no public part catalogue**. Panel specifications are distributed to integrators **under NDA**; E Ink says so on the face of its own documents (§5). `www.eink.com` is a **JavaScript SPA that returns the same 204 kB page for every path**, so a "HTTP 200" from it means nothing (§6, S2). The **one** place E Ink publishes real per-part numbers is its own kit store, **`shopkits.eink.com`** — but only for the ~91 evaluation modules it sells, which do **not** include the panels in this repository (§5.2, S5). In practice: **the board vendor's design files and driver source are the specification.**

---

## 1. Who they are

**E Ink Holdings Inc.** (元太科技工業股份有限公司, Yuen Tai Technology), Hsinchu, Taiwan. Listed on the Taipei Exchange. E Ink Holdings owns **E Ink Corporation**, the Cambridge, Massachusetts company spun out of the MIT Media Lab in 1997 that commercialised microencapsulated electrophoretic imaging film.

E Ink has an effective monopoly on commercial reflective electrophoretic displays. Every mainstream e-reader — Kindle, Kobo, reMarkable, Boox, PocketBook — uses their film, and so does essentially every electronic shelf label. There is no meaningful second source for the technology at production volume.

**They sell to device manufacturers**, and their commercial structure is built around long-term integration relationships, not catalogue sales. This shapes everything below.

---

## 2. Product structure — three things that are easy to confuse

| Layer | What it is | Who buys it |
|---|---|---|
| **FPL (Front Plane Laminate)** | The imaging film itself. Sold as a laminate to panel manufacturers, tracked by **FPL lot number** | Panel makers |
| **AMEPD panel** (e.g. `ED052TC4`) | The film bonded to a TFT backplane with row/column drivers and an FPC. **No controller, no memory** | Device manufacturers, under NDA |
| **Display module / kit** | A panel plus a controller board, sold through `shopkits.eink.com` with a user manual | Anyone with a business account |

**Brands** are film generations, not part numbers: **Carta** (current monochrome), Pearl (older monochrome), **Kaleido** (colour filter array over monochrome film), **Spectra** (multi-pigment colour, ESL), **Gallery** (multi-pigment colour, full-colour), **Prism**, **Mobius** (plastic backplane), **Aurora** (wide temperature), **Marquee**.

**A brand name tells you nothing about a part number.** E Ink never publishes which panel uses which film generation on its public site.

### 2.1 Part numbering

**[inference]** — E Ink publishes no numbering guide. From parts observed in the wild (`ED013TC1`, `ED052TC2`, `ED052TC4`, `ED060SC4`, `ED060KC1`, `ED060XC3`, `ED097OC4`):

```
ED  052  TC  4
│   │    │   └─ Variant within the size+family. Can change RESOLUTION, not just revision:
│   │    │      ED052TC2 = 960x540, ED052TC4 = 1280x720. Same size, same family code.
│   │    └───── Two-letter family / generation code. Meaning NOT established.
│   │           `TC` is seen on ED013TC1 (E Ink's own kit shop) and on ED052TC2/TC4.
│   └────────── Diagonal in hundredths of an inch: 013 = 1.27", 052 = 5.2", 060 = 6", 097 = 9.7"
└────────────── "E Ink Display"
```

⚠ **The trailing digit is not a revision.** `ED052TC2` and `ED052TC4` are the *same size* with **different resolutions and different connectors** — see the [ED052TC4 record §2](../../components/e-ink/ed052tc4/README.md). Never assume a higher trailing digit is a compatible newer version of a lower one.

---

## 3. Market position and why the documentation is closed

E Ink's customers are Amazon, Kobo, reMarkable, Onyx, and a long tail of ESL and signage integrators. Each receives, under NDA:

- the **panel specification** (mechanical, optical, electrical, interface timing);
- a **waveform file** tuned to the FPL lot their panels came from;
- a **VCOM** value stored in the panel's on-FPC flash;
- an applications engineer.

None of that is public, and E Ink states the restriction explicitly on the documents themselves (§5).

**The consequence for anyone outside that relationship** is that a panel's optical, mechanical and timing characteristics are simply unavailable. What is available is whatever a board vendor chose to publish in *their* design files — which is why this repository's [ED052TC4 record](../../components/e-ink/ed052tc4/README.md) reconstructs the panel from three KiCad boards and a driver library rather than from a datasheet.

The posture is identical to [Hynitron](../hynitron/README.md) and Sitronix: sell to module houses, document to module houses.

---

## 4. What "no datasheet" concretely means

For a typical E Ink AMEPD you will **not** find:

| Missing | Consequence |
|---|---|
| Pixel pitch, active area, outline dimensions | Cannot design an enclosure without measuring |
| Contrast ratio, reflectance, viewing angle | Cannot compare panels or specify a product |
| Operating / storage temperature range | Cannot state an environmental rating |
| Interface timing (setup/hold, max `CL`, `CKV` widths) | Must copy a working driver's magic numbers |
| Waveform tables | Must use whatever the board vendor derived |
| Lifetime / update-count endurance | Cannot predict wear |
| FPC pinout and pin-1 orientation | Must reverse from a mainboard schematic |
| ESD, bend radius, handling limits | Must guess |

What you *can* usually establish from a board vendor's open design files: **the complete electrical interface and the connector pinout.** That is the practical substitute, and it is why open-hardware board vendors matter so much in this space.

---

## 5. Where E Ink information actually comes from

Ordered by likelihood of success.

| Rank | Source | Pattern | What you get |
|---|---|---|---|
| **1** | **The board vendor's open design files** | GitHub — e.g. `SolderedElectronics/Soldered-Inkplate-5-Gen2-hardware-design` (S6) | ✅ **Complete connector pinout, rails, signal names.** How this repository documented the `ED052TC4` |
| **2** | **The board vendor's driver source** | `SolderedElectronics/Inkplate-Arduino-library` (S7) | ✅ Resolution, waveform LUTs, drive-code encoding, timing constants, refresh sequences |
| **3** | **`shopkits.eink.com`** — E Ink's own kit store | `https://shopkits.eink.com/en/product/detail/<desc>(<PART>)` | ✅ **Real specifications** — §5.2. Only for the ~91 kit parts |
| 4 | **Leaked / mirrored E Ink specification PDFs** | Board vendors occasionally host them, e.g. `waveshare.com/w/upload/…` | ⚠ Genuine but NDA-marked. §5.1 |
| 5 | Community reverse-engineering | Essential Scrap's `ED060SC4` work, `vroland/epdiy`, Kindle/Kobo teardown communities | ⚠ Excellent for the 6" DES family; nothing specific to most parts |
| 6 | Panel databases (`panelook.com`) | Indexes E Ink part numbers with parameters | ❌ **Slider-CAPTCHA bot block** as of 2026-08-24 (S4) |
| **7** | **`www.eink.com`** | Any path | ❌ **Useless for part data.** §6 |

### 5.1 The one E Ink document this repository holds

| Document | Where it came from | Local path |
|---|---|---|
| **`800-1101 REV01` — "AF 16 Tone Grayscale 5-Bit Waveform Flash File Product Specification"**, E Ink Corporation, 2017-01-11, 5 pages | **`waveshare.com/w/upload/c/c4/E-paper-mode-declaration.pdf`** (S3) — a board vendor's wiki upload pool, not E Ink | [`components/e-ink/ed052tc4/artifacts/eink-af-16-tone-grayscale-5bit-waveform-flash-file-spec-800-1101-rev01.pdf`](../../components/e-ink/ed052tc4/artifacts/eink-af-16-tone-grayscale-5bit-waveform-flash-file-spec-800-1101-rev01.pdf) |

Its first page carries the sentence that defines this vendor:

> *"This specification document is for use by **E Ink Corporation and their customers under non-disclosure agreements**. E Ink Corporation will be responsible for maintaining and controlling specification revisions."*

**It is worth reading in full even though it documents a different product**, because it is the only authoritative public description of:

- the **standard update-mode taxonomy** — INIT, DU, GC16, GL16, GLR16, GLD16, A2, DU4 — with E Ink's own ghosting ratings and typical update times at 25 °C;
- the recommended **A2 entry/exit sequences** that explain the periodic white flash on every e-reader;
- the **waveform-file header layout**, including the FPL-lot and VCOM-offset fields;
- the fact that waveforms are **per-lot** and **temperature-indexed**.

Analysis is in [ED052TC4 §8](../../components/e-ink/ed052tc4/README.md).

> ⚠ **Provenance and ethics.** This document was retrieved from a public URL on a board vendor's site. Given the NDA notice on its own first page, its public availability is presumably unintentional. It is retained here because it is the only primary E Ink source obtainable, and because its own front matter is the evidence for the central claim of this guide. Do not treat it as licensed material.

### 5.2 `shopkits.eink.com` — the exception that proves the rule

E Ink's kit store **does** publish real specifications, per part, with downloadable user manuals. Worked example, `ED013TC1` (S5):

| Item | Value |
|---|---|
| Size | 1.27 inch |
| Resolution | 128 (H) × 256 (V) |
| **Active area** | 14.46 × 28.93 mm |
| **Pixel pitch** | 0.113 × 0.113 mm |
| Outline | 18.7 × 39.8 × 0.96 mm |
| Weight | 1.55 ± 0.16 g |
| Grey levels | 2 |
| ppi | 225 |
| Backplane | Glass |

with a **`User Manual - 1.27'' ePaper Display (ED013TC1).pdf`** behind `shopkits.eink.com/en/download/<id>/…`. That is exactly the class of data missing for every non-kit panel.

**URL patterns (S5):**

```
https://shopkits.eink.com/en/product                        # catalogue, 91 items
https://shopkits.eink.com/en/product?cate=Black%26White     # 10 monochrome items
https://shopkits.eink.com/en/product?cate=DrivingBoard
https://shopkits.eink.com/en/product/detail/CompatibilityTable
https://shopkits.eink.com/en/product/detail/1.27''ePaperDisplay(ED013TC1)
https://shopkits.eink.com/en/download/<opaque-id>/<filename>.pdf
```

⚠ **Three limits.** (1) The catalogue is **evaluation kits only** — the black-and-white range as of 2026-08-24 is 1.27", 2.84", 2.9", 3.7", 4.3", 7", 13.3", 28", 31.2", 42". **There is no 5.2" part**, so the `ED052TC4` is not obtainable or documentable this way (S5). (2) Purchases require a business account: *"The products are not consumer products… Purchaser is purchasing the products for commercial use."* (3) Many kits require a specific E Ink driving board (`HULK`, `Mercury`) to be useful at all.

**Still, always check `shopkits` first for a new E Ink part number.** It is the only E Ink property that emits real numbers.

---

## 6. ⚠ `www.eink.com` returns HTTP 200 for everything

This is the single most important retrieval gotcha for this vendor, and it will silently corrupt any automated survey.

**[probe, 2026-08-24, S2]** — with a Chrome-131 User-Agent:

| URL | Result |
|---|---|
| `https://www.eink.com/` | 200, **204,139 bytes** |
| `https://www.eink.com/products` | 200, **204,139 bytes** |
| `https://www.eink.com/product/ED052TC4` | 200, **204,139 bytes** |
| `https://www.eink.com/brand.html` | 200, **204,139 bytes** |
| `https://www.eink.com/brand.html?type=carta` | 200, **204,139 bytes** |
| `https://www.eink.com/tech.html?type=electronicink` | 200, **204,139 bytes** |

**Byte-identical.** It is a client-rendered SPA that serves one shell document for every route and fills it in with JavaScript. Consequences:

- **A 200 is not evidence that a page exists.** `eink.com/product/ED052TC4` "works" and tells you nothing.
- **A text scrape of the whole site finds no part numbers at all.** A regex for `ED\d{3}[A-Z]{2}\d` over the products page returns **zero matches**. E Ink genuinely does not publish a part catalogue on its corporate site.
- Compare sizes, not status codes, when probing this host.

Also: **`www.e-ink.com` (with the hyphen) does not respond** — connection timeout, no HTTP status, both with and without a browser UA (S2). The live domain is `eink.com`.

---

## 7. Distribution

| Channel | Availability |
|---|---|
| Mouser / Digi-Key | ❌ **None.** E Ink panels are not distributor parts |
| **`shopkits.eink.com`** | ⚠ Evaluation kits only, business accounts only, ~91 SKUs |
| **Good Display / Dalian Good Display** | ✅ The main reseller route for small E Ink modules, with usable public specs. Their `GDE`/`GDEW`/`GDEY` part numbers are **their** modules built on E Ink film, not E Ink part numbers |
| **Waveshare** | ✅ Modules built on Good Display panels, with wikis and drivers. Often the most accessible entry point |
| AliExpress / Taobao | ⚠ Pulls and grey-market panels. Unwarranted, undocumented, frequently mismatched to their claimed waveform |
| **Bonded into a finished board** | ✅ How the panels in this repository arrived |

**You cannot meaningfully "buy an `ED052TC4`."** You buy an [Inkplate 5 Gen 2](../../devices/soldered-electronics/inkplate-5-gen2/README.md) or a [ZeroWriter Ink](../../devices/zerowriter/zerowriter-ink/README.md) and inherit one.

---

## 8. Gotchas

- **Every path on `www.eink.com` returns the same 200.** §6. The most dangerous one, because it looks like success.
- **`www.e-ink.com` is dead; `www.eink.com` is live.** §6.
- **`panelook.com` is CAPTCHA-blocked.** §5, S4. It is the database that would answer most questions.
- **Trailing digits are not revisions.** `ED052TC2` ≠ an older `ED052TC4`. §2.1.
- **Brand names are film generations, not part identifiers.** Nothing public maps a part number to Carta / Pearl / Kaleido.
- **A waveform is panel-lot-specific.** *"Each AF waveform is specifically adjusted for a particular display module lot"* (S3). There is no such thing as a generic waveform, and a waveform from a different lot will produce subtly wrong greys.
- **VCOM is panel-specific and lives in the panel's own flash** — which board designers routinely leave unrouted, at which point it is unrecoverable. See [ED052TC4 §5.3](../../components/e-ink/ed052tc4/README.md).
- **Parallel AMEPD panels have no controller.** If you are expecting an SSD1680-style command set, you have the wrong mental model. [ED052TC4 §4](../../components/e-ink/ed052tc4/README.md).
- **Any "E Ink datasheet" you find for a non-kit panel is either a leak or a fabrication.** Check for an E Ink header and a document number (`800-nnnn`) before believing a number in it.
- **Good Display part numbers are not E Ink part numbers.** A `GDEW042T2` is a Good Display module; the E Ink panel inside it has its own designation that Good Display may not disclose.

---

## 9. Parts and devices we document

| Record | Type | Used by |
|---|---|---|
| [**ED052TC4 / ED052TC2**](../../components/e-ink/ed052tc4/README.md) | 5.2" parallel AMEPD panel, 1280 × 720 / 960 × 540, 8 grey levels | [Inkplate 5](../../devices/soldered-electronics/inkplate-5/README.md) · [Inkplate 5 Gen 2](../../devices/soldered-electronics/inkplate-5-gen2/README.md) · [ZeroWriter Ink](../../devices/zerowriter/zerowriter-ink/README.md) |

Related non-E-Ink records for the same display subsystem:
[TPS65186 PMIC](../../components/texas-instruments/tps65186/README.md) ·
[PCAL6416A I/O expander](../../components/nxp/pcal6416a/README.md).

**No device in this repository is manufactured by E Ink.**

---

## 10. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | E Ink corporate site | primary | https://www.eink.com/ | 2026-08-24 | HTTP 200, 204,139 B. Brand list (Marquee, Spectra, Gallery, Kaleido, Prism, Carta, Mobius, Aurora); application taxonomy; **no part numbers anywhere** |
| S2 | **Negative probe** — `eink.com` path invariance and `e-ink.com` | probe | `eink.com/`, `/products`, `/product/ED052TC4`, `/brand.html`, `/brand.html?type=carta`, `/tech.html?type=electronicink`; and `https://www.e-ink.com/` | 2026-08-24 | **All six `eink.com` URLs return 200 with byte-identical 204,139-byte bodies.** Regex for `ED\d{3}[A-Z]{2}\d` over the products page: **0 matches**. `www.e-ink.com` **times out with no HTTP status** |
| S3 | **E Ink Corporation `800-1101 Rev01`** — AF waveform flash file product specification | **primary (E Ink), redistributed** | https://www.waveshare.com/w/upload/c/c4/E-paper-mode-declaration.pdf | 2026-08-24 | The NDA notice (§5.1); update-mode taxonomy and times; waveform-file header; per-lot and per-temperature waveform model. `%PDF-1.5`, 5 pages, 362,418 B |
| S4 | **Negative probe** — Panelook | probe | https://www.panelook.com/ (model search `ED052TC`, and a direct parameter URL) | 2026-08-24 | **Slider-CAPTCHA challenge page** on both, with and without a Chrome-131 UA |
| S5 | **E Ink kit store** | primary | https://shopkits.eink.com/en/product · `…/product?cate=Black%26White` · `…/product/detail/1.27''ePaperDisplay(ED013TC1)` · `…/product/detail/CompatibilityTable` | 2026-08-24 | 91 SKUs; **10 monochrome items, none 5.2"**; full `ED013TC1` specification table (§5.2); the download URL pattern; the business-account-only condition; part numbers `ED013TC1`, `ED060KC1` |
| S6 | Soldered Inkplate 5 / Gen2 hardware design (TAPR OHL) | primary | https://github.com/SolderedElectronics/Soldered-Inkplate-5-hardware-design · `…-Gen2-hardware-design` | 2026-08-24 | The route in §5 rank 1 — complete panel connector pinouts | local snapshots |
| S7 | Inkplate Arduino library | primary | https://github.com/SolderedElectronics/Inkplate-Arduino-library | 2026-08-24 | The route in §5 rank 2 — resolutions, waveform LUTs, drive encoding, timings. **v11.1.4** | local snapshot |

> **Evidence boundary.** S1, S2, S4 and S5 are **HTTP probes performed 2026-08-24**. The claim that E Ink publishes no AMEPD datasheets is a **negative result from this search plus E Ink's own NDA notice (S3)** — it is not proof that no public copy exists anywhere. §2.1's part-number decode is explicitly **[inference]**: the `052` → 5.2" and `013` → 1.27" mappings are confirmed by S5 and by product listings, but the meaning of the two-letter family code is **not established**. No claim in this guide about a *specific* panel's optical or mechanical properties is made, because none can be sourced.

---

## Related

- [Vendor guide index](../README.md)
- [ED052TC4 / ED052TC2 component record](../../components/e-ink/ed052tc4/README.md) — the worked example of documenting a panel with no datasheet
- [Hynitron](../hynitron/README.md) — the same "sell to module houses, document to module houses" posture
- [Soldered Electronics](../soldered-electronics/README.md) — the open-hardware board vendor whose design files substitute for the missing panel datasheet
- [Waveshare](../waveshare/README.md) — the mirror that served the one E Ink document we hold
- [Repository crawler / site-access table](../../ai-crawler-site-access-table.md)
