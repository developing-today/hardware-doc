# Media and visual identification — M5Stack PaperMono

> Snapshot **2026-09-01**. Machine-readable index: [`media/manifest.json`](media/manifest.json).
>
> ## ⚠ **Zero images are retained. That is the finding, and it is deliberate.**
>
> **No product photograph, no teardown, no PCB view and no revision-marking image is held in this
> record**, for two reasons that are different in kind and must not be conflated:
>
> 1. **The only imagery that exists is vendor product photography**, and it is **not licensed for
>    redistribution** — M5Stack states no licence for it anywhere.
> 2. **No independent teardown, PCB photograph or component close-up existed at the snapshot
>    date.** Nobody has opened one in public. That is a **verified absence** (§3), not a failed
>    search.
>
> The visual evidence this record *does* hold is the **vendor schematic** and the **mechanical
> drawing** (§4). Both are primary design documents, both are retained, and between them they
> establish the board's construction and its outline — but neither tells you what the product
> looks like or how to identify one in hand.

## Contents

- [1. What was sought](#1-what-was-sought)
- [2. Where it was looked for](#2-where-it-was-looked-for)
- [3. Why nothing is retained](#3-why-nothing-is-retained)
- [4. The visual evidence that is held](#4-the-visual-evidence-that-is-held)
- [5. Derived renders that exist but are not media](#5-derived-renders-that-exist-but-are-not-media)
- [6. What a future pass should capture](#6-what-a-future-pass-should-capture)
- [7. Rules for whoever fills this in](#7-rules-for-whoever-fills-this-in)
- [8. What can be said about the product's appearance without a photograph](#8-what-can-be-said-about-the-products-appearance-without-a-photograph)

---

## 1. What was sought

The method's visual-identification list, and the status of each class for this device:

| # | Image class | Status | Why it matters here |
|---|---|---|---|
| 1 | **Front** — the product as sold | **exists, vendor-only, not retained** | Basic identification |
| 2 | **Back** | **not located** | Where a revision marking or regulatory label would be — and **no certification identifier is published for this board at all** (S11), so a photograph of the back is currently the *only* possible route to one |
| 3 | **Ports and labels** | **not located** | USB-C position, the side RGB indicator, the three switches |
| 4 | **Enclosure open** | **not located** | The board is described as three PCBs plus three flexible assemblies; nothing shows how they sit |
| 5 | **Teardown stages** | **none exists** | Verified absence at the snapshot date |
| 6 | **PCB front** | **none exists** | Would confirm fitted parts against the schematic, including the `Stamp-LoRa-1262-mini` module |
| 7 | **PCB back** | **none exists** | — |
| 8 | **Revision markings** | **none exists** | **Only one hardware revision (V0.6.2) is in evidence, and it comes from a schematic filename.** There is no way to tell one board from another in hand |
| 9 | **Component close-ups** | **none exists** | **Three parts have no obtainable datasheet** — the `CN4040M000157A530001` crystal, the `LMD4737T261-AC02` microphone and the `RS-C1415MBAR` RGB LED ([G6](gaps-and-conflicts.md#g6--three-parts-have-no-obtainable-datasheet)). A sharp photograph of a top marking is the most likely route to identifying any of them |
| 10 | **Representative use** | **exists, vendor and one video, not retained** | — |

**Rows 5–9 are the ones that would change what this record knows.** Rows 1, 3 and 10 are
marketing; rows 6–9 are evidence.

## 2. Where it was looked for

Imagery was not searched for as a separate exercise; it was **sought as part of the two broad
coverage passes** logged in [`research-log.md`](research-log.md) and catalogued in
[`community.md`](community.md). What that covered, and what it returned:

| Venue | Imagery outcome |
|---|---|
| **`docs.m5stack.com`** (13 pages, EN/zh_CN/ja) | Vendor product photography and PinMap diagrams present. **Not retained** — no licence stated (§3) |
| **`shop.m5stack.com`** product pages and blog | Vendor product photography. Same |
| **M5Burner API** | Both firmware records carry a `coverUrl` on `m5burner-cdn.m5stack.com`. **Not retrieved** — they are vendor/community catalogue artwork, and their licence is likewise unstated |
| **Hackaday, Hackster, Tom's Hardware, Adafruit blog** | **No article at all**, therefore no photography. Hackaday's search API returns `[]`; Hackster's search is a JS shell with no working path |
| **YouTube** | **Two videos**: the vendor's launch clip and one hands-on (Volos Projects, 2026-08-29). **No frames were extracted** — a video frame is a derivative of a copyrighted work and its provenance would be no clearer than the source |
| **X / Twitter** | **Four photographs** of a PaperMono-Lite in @henry19840301's 2026-08-21 purchase post — the **only known independent photography of the product**. Individual, unlicensed, and of an unboxing rather than of the hardware's construction |
| **r/M5Stack, Hacker News** | No teardown, no PCB photograph, no revision marking |
| **GitHub — five third-party projects** | `MingRZou/PaperMono-Launcher` carries **one photograph** captioned "PaperMono-Launcher on real hardware" — a running screen, not a hardware view. `EggUncle/PaperMonoCalendar` is explicit that its previews are **software-generated, not device photographs** (「非设备实拍」) |
| **`community.m5stack.com`** | **Auth-walled** (HTTP 401). The vendor forum is the likeliest home for owner photographs and **could not be searched** |
| **Regulatory databases** | **Not searched.** M5Stack publishes no certification identifier (S11), and an FCC grantee-database search **was not attempted** — see §6 |

**Two of those rows are the leads.** The vendor forum is inaccessible rather than empty, and the
FCC database was never tried. Both could yield internal photographs.

## 3. Why nothing is retained

| Reason | Applies to | Detail |
|---|---|---|
| **Licence unknown, redistribution not permitted** | All vendor product photography, PinMap diagrams, store imagery, M5Burner cover art | M5Stack states no licence for its imagery on any page retrieved. Under the method's own labels that is `redistribution: unknown` — and **`unknown` is not permission.** The method is explicit that licensing is metadata rather than a gate *on acquisition*; it is nonetheless a gate on **redistribution**, and committing a vendor's product photography into a published repository is redistribution |
| **Individual's copyright** | @henry19840301's four purchase photographs | One person's photographs posted to a social account. Cited as evidence in [`community.md`](community.md); not copied |
| **Derivative of a copyrighted video** | Frames from either YouTube video | Extracting frames would produce an image whose provenance is a video the record has no rights to |
| **Does not exist** | **Teardown, PCB front/back, enclosure-open, revision markings, component close-ups** | **A verified absence at 2026-09-01**, consistent with a product that has been purchasable for approximately nine minutes ([`market-and-pricing.md` §7](market-and-pricing.md#7-availability-history)). You cannot tear down hardware nobody can buy |

**The distinction between the first three rows and the last matters.** The first three are
*rights* problems — the images exist and a future pass with permission, or a fair-use judgement
the user makes, could retain them. The last is an *evidence* problem, and no amount of permission
fixes it. **Only new hardware in someone's hands fixes it.**

**No watermark was removed from anything, no image was altered, and no image-search result is
presented as provenance** — because no image was taken at all.

## 4. The visual evidence that is held

Two documents, both primary, both in the repository:

| Artifact | Path | Bytes | SHA-256 | What it shows visually |
|---|---|---|---|---|
| **Schematic V0.6.2** | [`artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf`](artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf) | 1 462 039 | `b5abecac97cb043a6d1af7a673f2111d40d9254b0b5108635cb924d9b37ad6fa` | **6 sheets, Altium export.** Sheet 1 is a block diagram with the power-state matrix; sheets 2–4 the main board; sheet 5 the KEY/RGB/PDM sub-board; sheet 6 the NFC sub-board (numbered **2/2** — sheet 1 of that document is absent). This is what establishes that **the product is three PCBs plus three flexible assemblies** |
| **Mechanical drawing** | [`artifacts/mechanical/C153_PaperMono_model_size.pdf`](artifacts/mechanical/C153_PaperMono_model_size.pdf) | 21 346 | `b833a3e52594a3175bc131006d41a3eb5662be5936d0b2f25030180033a6703b` | **1 page.** Outline dimensions, corner radii and port positions — the closest thing to a picture of the object that this record holds |

Both are M5Stack-published, licence **unknown**, disposition **repository**, retrieved
**2026-09-01**. Provenance in [`acquisition/manifest.json`](acquisition/manifest.json) and
[`sources.md`](sources.md) (S14, S15).

> **A retrieval quirk in the mechanical drawing, recorded because it will bite the next reader.**
> Its dimensions are typeset in **full-width CJK numerals**, so text extraction yields `６２`
> rather than `62`. Human-legible, not machine-comparable without normalisation. This is a mild
> instance of exactly the failure mode the method warns about — trusting a PDF text layer you
> have not validated.

## 5. Derived renders that exist but are not media

Rendering the retained PDFs produced page images during this pass. **They are working files, not
media, and they are deliberately not promoted into `media/`:**

| Working set | Location | What it is |
|---|---|---|
| Schematic sheet renders and crops | `scratch/m5stack-papermono/sheets/` (~4.0 MB) | 200 dpi renders of sheets 1, 2 and 4, plus crops of the charge block, the rails, the RTC and the EPD boost circuit. These were how the [RTC rail error](gaps-and-conflicts.md#r7--rtc-rail-the-vendor-block-diagram-is-wrong--resolved) was found — the text extraction was ambiguous and the sheet had to be *looked at* |
| Panel-manual page renders | `scratch/m5stack-papermono/epd-pages/` (~3.7 MB) | 22 page images of the DKE panel manual, which belongs to the [panel component](../../../components/dke/depg0397bbs770f3/README.md), not to this device |

**Why they are not retained.** They are **derived and exactly reproducible** from artifacts the
repository already holds, by a documented command
([`commands.md` §2.4](commands.md#24-rasterising-pages-for-human-reading)). Storing ~7.7 MB of
regenerable raster alongside the 1.5 MB source it was generated from is the case
[`SIZE-AUDIT.md`](../../../SIZE-AUDIT.md) exists to prevent. **Nothing is lost by their absence**
— which is precisely what cannot be said of the missing photographs in §3.

## 6. What a future pass should capture

Ordered by how much each would change what this record knows. This is a work list, not a wish
list.

### 6.1 With hardware in hand

| # | Shot | What it would settle |
|---|---|---|
| 1 | **PCB front and back, sharp, whole-board, with a scale reference** | Confirms the fitted BOM against the schematic — including whether the `Stamp-LoRa-1262-mini` module and the `ST25R3916-AQWT` are the parts drawn. **The schematic was recovered from invisible Altium marker text by spatial adjacency**, which yields *text adjacency, not electrical connectivity*; a photograph is an independent check on every part it shows |
| 2 | **Macro close-ups of three top markings**: the 40 MHz crystal (`X1`), the PDM microphone, the RGB LED | The **only realistic route** to identifying `CN4040M000157A530001`, `LMD4737T261-AC02` and `RS-C1415MBAR`, whose only web occurrences anywhere are M5Stack's own pages ([G6](gaps-and-conflicts.md#g6--three-parts-have-no-obtainable-datasheet)) |
| 3 | **The NFC sub-board, both faces** | **NFC schematic sheet 1 of 2 is not published** ([G1](gaps-and-conflicts.md#g1--nfc-schematic-sheet-1-of-2-is-not-published)). A photograph is the only available substitute for the missing sheet, and would show the antenna construction the released sheet describes in a note (4 turns, 25 × 25 mm, 0.25 mm trace, 0.3 mm gap, 17 µm copper) |
| 4 | **The `Stamp-LoRa-1262-mini` module, close** | **No module datasheet exists anywhere.** A photograph could settle **TCXO versus XTAL** by showing whether a TCXO can is fitted — one of the record's named unknowns ([G5](gaps-and-conflicts.md#g5--no-stamp-lora-1262-module-datasheet-exists-anywhere-located)) |
| 5 | **The back of the enclosure, and any label** | The only possible source of a regulatory identifier, since M5Stack publishes none ([G2](gaps-and-conflicts.md#g2--no-certification-identifiers-exist-on-the-vendor-site)) |
| 6 | **Enclosure-open, showing the three-board arrangement and the three FPCs** | The record asserts the construction from title blocks and connector lists. Nothing has verified it |
| 7 | **Any silkscreen revision marking** | There is currently **no way to distinguish hardware revisions in hand** |
| 8 | **Panel photographs at 1, 2 and 4 grey levels, fixed lighting, with a grey step wedge** | Would bear directly on [C1](gaps-and-conflicts.md#c1--4-grey-levels-versus-2) — the vendor markets 4 grey levels and the panel manual's optical table says 2 |
| 9 | **Ghosting series**: a fixed pattern after 1, 5, 10, 20, 50 partial refreshes, with and without the vendor's 1-in-10 full refresh | The only independent observation that exists about this display is CNX-Software's "ghosting visible in demo" — of a *video*. See [`performance.md` §7](performance.md#7-what-would-actually-settle-these-questions) |
| 10 | **Frontlight on and off, same scene, same exposure** | Nothing shows what the frontlight actually does |

### 6.2 Without hardware

| # | Action | Why it is worth trying |
|---|---|---|
| 11 | **Search the FCC (and CE / TELEC) grantee databases** for M5Stack filings covering C153 | **Never attempted in this pass.** FCC filings routinely include **internal photographs, external photographs and label-location exhibits** — which would supply items 1, 5 and 7 above **with clear public-record provenance**. This is the single highest-value untaken imagery lead, and it needs no hardware |
| 12 | **Re-check `community.m5stack.com` with an account** | Auth-walled at HTTP 401; the vendor forum is the likeliest first home for owner photographs |
| 13 | **Re-run the search after the restock** | Every "none exists" on this page is a consequence of supply |
| 14 | **Retrieve the Lite's schematic** `PaperMono-Lite_PRJ_V0.6.2_20260522.pdf` (S16) | Not fetched. `PRJ`-named with **4 sheets** against the full model's 6 — it may render differently and show different views |
| 15 | **Ask M5Stack for permission to redistribute product imagery** | Turns a rights problem into a solved one for items 1, 3 and 10 |

## 7. Rules for whoever fills this in

So that a later pass does not have to re-derive the policy:

1. **Record provenance at acquisition time, not afterwards.** Every retained image needs
   creator/rightsholder where known, **source page** *and* **direct URL**, publication date,
   retrieval date, applicable device revision, licence and the evidence for it, redistribution
   status, modification history, local path, **caption** and **alt text**. The manifest schema in
   [`media/manifest.json`](media/manifest.json) has a field for each; fill them or write
   `unknown`, never omit them.
2. **Captions explain what the image demonstrates**, plus any crop, annotation, rotation or
   processing. "Front of the device" is not a caption; "front face showing the USB-C port on the
   lower edge and the side RGB indicator" is.
3. **Never remove a watermark**, and **never present an image-search result as provenance** —
   the page an image was *found* on is not necessarily its source.
4. **A vendor image with no stated licence is `unknown`, and `unknown` is not permission.**
   Record the URL and the metadata; retain the bytes only on an explicit decision, and record who
   made it.
5. **Prefer images that establish something over images that look good.** A blurry photograph of
   a legible top marking is worth more to this record than a studio product shot.
6. **Hash everything**, and note whether the file is byte-identical to something already held
   elsewhere in the repository — the `shared-assets/` pool exists for that.

## 8. What can be said about the product's appearance without a photograph

For identification purposes, from the mechanical drawing, the schematic and the vendor
specification table — **all `not-tested`, none observed**:

- **A closed handheld slab**, **62.0 × 101.0 × 8.0 mm**, **74.7 g** (Lite: 72.4 g), grey case
  (Lite: **white**).
- The **3.97-inch e-paper panel occupies most of the front face**; 480 × 800 portrait,
  approximately 235 DPI.
- **A USB-C port** (`U1`, `TYPEC-302-BRP16SC08`).
- **Three switches on one sub-board**: `S1` `PWR_BTN`, `S2` `G2_KEY1` (Button A), `S3` `G3_KEY2`
  (Button B). **There is no reset button** — the vendor's own Arduino page is wrong about this
  ([R4](gaps-and-conflicts.md#r4--download-mode-control--resolved-on-the-balance-of-evidence)).
- **A side RGB indicator** — three LED dies, of which **only green and blue can be dimmed**; red
  is driven by the M5PM1's `LED_EN_PP`, which has no PWM mode.
- **No expansion connector of any kind** — no Grove, no M-Bus. Visually, there is nothing on the
  edges but the USB-C port and the buttons.
- Package: 113.2 × 69.6 × 21.0 mm, gross 91.3 g.

**One dimensional conflict is on record.** CNX-Software published 101 × 61 × 7.95 mm against the
vendor's 62.0 × 101.0 × 8.0 mm. Neither was measured; this record uses the vendor's figures
throughout.

## Related

- [`media/manifest.json`](media/manifest.json) — the schema, empty, with the reason recorded in it
- [`README.md`](README.md) — the device overview, which carries the same "images: an explicit gap" note
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — G1, G2, G5, G6 and C1, each of which a photograph would help settle
- [`community.md`](community.md) — where the photographs that do exist were found, and who owns them
- [`commands.md` §2.4](commands.md#24-rasterising-pages-for-human-reading) — how to regenerate the derived renders in §5
- [`acquisition/manifest.json`](acquisition/manifest.json) — provenance for the two retained documents
- [`sources.md`](sources.md) — S11, S14, S15, S16, S72, S80–S82, S85, S87, S91, S92
