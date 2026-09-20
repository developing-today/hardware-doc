# DKE — documentation sourcing guide

**DKE Holding Company Limited** (东方科脉 / Dongfang Kemai) — e-paper (electrophoretic)
display module manufacturer, China.

Established **2026-09-01** while researching the panel fitted to the
[M5Stack PaperMono](../../devices/m5stack/papermono/README.md). This is a **short guide**,
because DKE's documentation surface, as encountered, is small: one manual, obtained
indirectly, with one severe retrieval trap.

Product documented with this guide:
[**`DEPG0397BBS770F3`**](../../components/dke/depg0397bbs770f3/README.md).

## 1. ⚠ The panel manual comes from the *board* vendor, not from DKE

**No DKE-hosted copy of the `DEPG0397BBS770F3` manual was located, and no public DKE
document portal was found to search.**

The 30-page *EPD Module User Manual* — "Specification for 3.97 inch EPD" — was obtained
solely as an attachment on **M5Stack's** PaperMono product page, where it is linked under
the generic label **"3.97-inch Touchscreen"** in the *Datasheets* list. Verified
2026-09-01:

```
https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1267/EPD_Module_User_Manual.pdf
```

8,666,208 bytes ·
SHA-256 `6b65f56d5d549a132e5c807eef329fb3e997feab04ac06e8a107f01591618130`.

Note what the URL does **not** contain: the manufacturer's name, the part number, or
anything identifiable. `EPD_Module_User_Manual.pdf` under an M5Stack numeric product id.
**You cannot find this file by searching for the DKE part number.**

> **The general lesson, and it applies well beyond DKE:** for a display panel, the panel
> maker's documentation is very often distributed **through whoever put the panel on a
> board**, under a generic label, on the board vendor's CDN. **Look at the board vendor's
> asset list before concluding the panel manual does not exist.** Enumerate every asset
> URL on the product page — including the ones with unhelpful names — rather than
> searching for the part number.
>
> How to enumerate M5Stack's asset URLs, including the `zh_CN`-only ones:
> [`vendors/m5stack`](../m5stack/README.md).

### 1.1 Provenance caveats worth carrying

- The manual is **undated on its cover** and carries **no revision table**. The only
  internal date is on the embedded mechanical drawing: `REV. A0`, `FIRST ISSUE`,
  **2024-09-29**.
- Its PDF `Producer` is **`iLovePDF`** and its `ModDate` is **2026-08-21** — the same day
  the PaperMono store listing went live. There is **no `Author`, `Title` or `Creator`
  metadata at all**. The file was clearly re-processed before publication, and the
  original authoring tool is unrecoverable.
- Licence: DKE copyright, **no licence statement and no confidentiality footer**.
  Mirrored by M5Stack with no stated terms. Redistribution status `unknown`.
- ⚠ **Single-source.** Only one acquisition URL is known for this document. That is
  recorded deliberately rather than left as a silent gap, and it is why the bytes are
  retained in the repository rather than referenced.

> **Discrepancy noted 2026-09-01.** The component record's source table gives the upstream
> as `static-cdn.m5stack.com/resource/docs/products/core/PaperMono/…`. The URL actually
> present in the retrieved product page is the OSS bucket path above. `static-cdn.m5stack.com`
> is a real M5Stack host and does serve `/resource/docs/products/<category>/<Product>/…`
> assets, but **no reference to `EPD_Module_User_Manual.pdf` on that host was found in the
> captured pages.** Treat the OSS URL as the verified one and the `static-cdn` form as an
> unverified alternative worth trying if the OSS bucket goes away.

## 2. ⚠ The manual has no text layer — `pdftotext` returns nothing, silently

**This is the trap that matters, and it fails in the worst possible way: quietly.**

Every glyph in the PDF is a **vector outline**. There is no embedded text at all. So:

```bash
pdftotext depg0397bbs770f3-epd-module-user-manual.pdf -
# -> empty. Not garbage. Not an error. Nothing.
```

An empty result is easy to misread as "extraction failed, try another tool" or, worse, as
"this page is blank". Neither is true — the page is full of information that simply is not
text.

*(Recorded as the lesser evil: had `pdftotext` returned plausible-looking **wrong** text,
that text would have had to be validated against a rendered page before use. Silence is at
least unambiguous once you know to expect it. **Validate any PDF extraction against a
render at least once**, whatever it returns.)*

### The working method: rasterise and read the images

```bash
# render one page (here, page 7) at 140 dpi
pdftoppm -r 140 -png -f 7 -l 7 \
  artifacts/depg0397bbs770f3-epd-module-user-manual.pdf pg
# -> pg-07.png, then read it as an image

# the whole document
pdftoppm -r 140 -png artifacts/depg0397bbs770f3-epd-module-user-manual.pdf pg
```

On a NixOS/devshell host without `poppler-utils` on the path:

```bash
nix-shell -p poppler-utils --run \
  'pdftoppm -r 140 -png -f 7 -l 7 artifacts/depg0397bbs770f3-epd-module-user-manual.pdf pg'
```

**140 dpi was sufficient** for this document's tables and its mechanical drawing.
Eighteen of the thirty pages were transcribed this way (1, 4–10, 15–19, 21–25); every
figure in the component record cites its manual page number so it can be re-checked by
rendering that one page.

### Detecting the condition before you waste time

```bash
pdffonts file.pdf      # no fonts listed -> no text layer
pdfinfo  file.pdf      # check Producer: a re-processor such as iLovePDF is a warning sign
```

A `Producer` of `iLovePDF`, `PDFill` or a similar web re-processor is a **standing warning
sign** that a document has been through a lossy round trip. M5Stack's mirrored **SSD1677**
PDF shows the same pattern from a different tool: 46 pages numbering themselves `n/47`,
Producer `PDFill`. See [`vendors/m5stack` §5.5](../m5stack/README.md).

## 3. Part-number pattern

Observed on one part, so treat as a **hypothesis with one confirming instance**, not a
decoder:

```
DEPG  0397   BB    S770   F3     [ HP-XM ]
 |     |     |      |      |         |
 |     |     |      |      |         └─ customer/option suffix, undocumented
 |     |     |      |      └─ revision / interface variant
 |     |     |      └─ internal variant code
 |     |     └─ variant code
 |     └─ diagonal size in hundredths of an inch: 0397 = 3.97"
 └─ DKE E-Paper Display family prefix
```

**`DEPG` + a four-digit size in hundredths of an inch is the reliable part** — the size
field is confirmed by the manual's own title ("Specification for 3.97 inch EPD"). The rest
is not decoded by any DKE document located, and **no part-number decoder for the `DEPG*`
family was found**.

> ⚠ **A suffix conflict is live and unresolved.** The manual cover and the mechanical
> drawing's title block both say **`DEPG0397BBS770F3`**. M5Stack's
> `M5PaperMono-OTP-Demo/README.md` calls the fitted panel
> **`DEPG0397BBS770F3HP-XM`**. The M5Stack string is a strict superset, so the likeliest
> reading is that `HP-XM` is a customisation suffix — `HP` possibly a waveform or OTP
> option, `XM` a customer code — and that DKE supplied a customer-specific OTP under a
> base-model manual. **That is a hypothesis, not a finding**: no DKE document in hand
> mentions any suffix.
>
> **Practical consequence:** when sourcing a DKE panel, the base part number may not
> describe the OTP waveform actually programmed into the unit you receive. For this panel
> the OTP waveform contents — how many of the 34 waveform slots are programmed, over what
> temperature span — are **unpublished**, and running outside the programmed range is a
> silent no-refresh failure.

## 4. Known data errors in DKE material

One, and it is provable:

> **The mechanical drawing's note 3 reads `800 gate × 480 source`, which is backwards.**
> 800 gate lines would exceed the bonded SSD1677 controller's **680 gate outputs**, and
> M5Stack's own firmware configures **480 gates** via `0x01 = {0xDF, 0x01, 0x02}`. The
> drawing note is wrong; the arithmetic is in the
> [component record](../../components/dke/depg0397bbs770f3/README.md).

Also worth flagging as an internal inconsistency rather than an error: the manual's
overview describes the panel as *"capable to display image at **1-bit white and black**"*
and its optical specification table reads **`GN — 2Grey Level`**, while M5Stack markets
**4-level greyscale** and the vendor OTP demo implements a working four-grey mode.
**Unresolved.** Three readings are possible — a stale manual template, a panel binned for
mono with usable grey, or a marketing overstatement — and nothing in evidence chooses
between them.

## 5. Document-class checklist

For a DKE panel, expect **only the first line to be obtainable**:

| Class | Where to look | `DEPG0397BBS770F3` result |
|---|---|---|
| **Module user manual / specification** | **the board vendor's asset list**, under a generic label | ✅ 30 pp., via M5Stack `1267/EPD_Module_User_Manual.pdf` |
| Mechanical drawing | usually **embedded in the manual** | ✅ embedded, `REV A0`, 2024-09-29 |
| Controller datasheet | the **controller maker**, not DKE | ✅ [SSD1677](../../components/solomon-systech/ssd1677/README.md), via an M5Stack mirror |
| **OTP waveform contents** | — | ❌ **unpublished** |
| Errata / revision history | — | ❌ **no revision table at all** |
| Application notes, design guidelines | — | ❌ none located |
| Product change notices | — | ❌ none located |
| Reliability / qualification report | — | ⚠ reliability conditions are **inside the manual** |
| Public document portal | — | ❌ **none found** |
| Distributor datasheets | — | ❌ none located |

## 6. Per-part procedure

1. **Do not start with DKE.** Start with the board or module vendor that fitted the panel.
2. **Enumerate every asset URL on the board vendor's product page**, including generically
   named files. The panel manual will not be named after the part.
3. Run `pdffonts`. **No fonts means no text layer** — go straight to `pdftoppm`.
4. Render at **140 dpi PNG** and read the pages as images. Cite manual page numbers so
   every figure can be re-checked.
5. **Cross-check the panel manual against the bonded controller's datasheet.** That is how
   the reversed gate/source note was caught — the panel document contradicted the
   controller's output count.
6. **Cross-check against the board vendor's firmware.** Register writes such as
   `0x01 = {0xDF,0x01,0x02}` (480 gates) settle geometry questions the drawings get wrong.
7. Record the part-number suffix exactly as each source states it. They will disagree.
8. Since a DKE-hosted copy is unlikely to exist, **retain the bytes** rather than the URL,
   and record the single-source status explicitly.

## 7. Rights and licensing observations

- DKE copyright notice on every page footer; the mechanical drawing carries the Chinese
  mark **东方科脉**.
- **No licence statement and no confidentiality footer** on the manual — which is unusual
  and, in practice, permissive by omission rather than by grant. Redistribution status
  `unknown`.
- Mirrored by M5Stack with no stated terms of its own. **A board vendor rehosting a panel
  maker's manual does not relicense it.**

## 8. Products documented with this guide

- [**DKE `DEPG0397BBS770F3`**](../../components/dke/depg0397bbs770f3/README.md) — the
  3.97" panel of the [M5Stack PaperMono](../../devices/m5stack/papermono/README.md); the
  pass that produced these findings
- Related device guide: [`features/epaper-display.md`](../../devices/m5stack/papermono/features/epaper-display.md)
- Related vendor guide: [`vendors/m5stack`](../m5stack/README.md) — how to enumerate the
  asset list this manual was hiding in

## 9. Change log

| Date | Change |
|---|---|
| 2026-09-01 | Guide created during the M5Stack PaperMono pass. Established: DKE panel manuals are distributed **through the board vendor**, under generic labels, with no public DKE portal located; the `DEPG<size><variant>` part-number pattern and the unresolved `HP-XM` suffix; and the critical retrieval trap that **the manual PDF has no text layer at all** (vector-outlined glyphs), so `pdftotext` silently returns nothing and pages must be rendered with `pdftoppm -r 140 -png` and read as images. Recorded the provably reversed `800 gate × 480 source` drawing note and the unresolved 1-bit/2-grey/4-grey contradiction. |
