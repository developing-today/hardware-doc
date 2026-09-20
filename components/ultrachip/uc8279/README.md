# UltraChip UC8279 (and UC8279d, UC8279C) — e-paper display controller

- **Category:** electrophoretic display driver / timing controller.
- **Manufacturer:** UltraChip Inc.
- **Research status:** ⚠ Driver written **from a datasheet the FreeInk authors
  hold**, not retrieved here. **Never validated on X3 hardware.**
- **Retrieved:** 2026-09-04

Three closely-related variants appear in this knowledge base:

| Variant | Where | `LUT_VER` | NVS `screenType` |
|---|---|---|---|
| **UC8279** (800×480) | Xteink X4 / X4 Pro / X4 Classic, newer batches | `0x02`, `0x68` | 2 or 0x0C |
| **UC8279** reserved | — | `0x69` | — |
| **UC8279d** ("d_B" silicon) | **Xteink X3**, production from ~July 2026 | — | — |
| **UC8279C** | EEGO A4 768×552 (`Uc8279cA4Driver`) | — | — |

## 1. What is established

| Property | Value | Evidence |
|---|---|---|
| Mode used | `PSR KW/R = 1` — 1 bpp, `DTM1` = OLD, `DTM2` = NEW, differential refresh | `Uc8279Driver` |
| Command set | Near-identical to the UC8253: `PSR`/`PON`/`POF`, `DTM1 0x10`, `DSP 0x11`, `DRF 0x12`, `DTM2 0x13`, `CDI 0x50`, `TRES 0x61`, `DSLP 0x07`+`0xA5` | driver source |
| **LUT format** | **Group-based: 7-byte groups, 7 groups per LUT in KW mode** — **NOT** the UC8253's 43-byte format | `docs/xteink-x3-uc8279-support.md` |
| Serial write clock | **20 MHz** — *"Clock rate up to 20 MHz"* | datasheet, cited |
| Readable IDs | `VER 0x70` (reserved `0x00`, `CHIP_VER` default `0x03`, 24-bit `LUT_VER`), `FLG 0x71`, `RMTP 0xA2` | `XteinkDetect.cpp` |
| **OTP waveforms** | **4K MTP carrying 12 temperature-range LUT sets**, each with its own frame rate and rail voltages | `docs/xteink-x3-uc8279-support.md` |
| **`TS_AUTO`** | **Re-senses temperature before every booster enable** — PWR/PLL/VDCS stay at silicon defaults and every refresh is temperature-compensated *by the controller* | same |
| `CDI` default | SDK drives the border white each refresh (`0x97`); the **datasheet default is `0xD7`**, which floats it | same |
| Datasheet held by SDK authors | **UC8279d_B rev 0.1, dated December 2025** | same |

## 2. Features present in silicon but not wired up

Documented by the FreeInk authors as available and unused:

| Command | Capability | Why it might matter |
|---|---|---|
| **`AUTO (0x17)`** | `PON → DRF → POF (→ DSLP)` as a **single command** | Removes host round-trips on sleepy, ESL-style periodic updates — a real power win for always-on dashboards |
| **`PBC (0x44)`** | Panel-break check via the CHKGI/CHKGO wire loop | Only if the module bonds the loop out |
| **`CRC (0x72)`** | MTP integrity check over `0x000–0xFFF` | Field diagnosis of a corrupted waveform store |
| **`TSC (0x40)`** | On-chip temperature readback | Free ambient temperature for a consumer that wants it |

## 3. What does **not** work yet, and why

**On the Xteink X3, this driver has never run on a physical device.** Quoted:

> "Everything below is written from the UC8279d_B 0.1 datasheet (Dec 2025) and is
> **Pending hardware validation — no UC8279 X3 unit has been on the bench yet.**"

Consequences, all still open:

- **Full / Half / Fast all run the same OTP waveform**, so a page turn is likely a
  full GC-style flash. Fast modes need custom register banks (`REG = 1`,
  commands `0x20`–`0x24`).
- **The X3's six tuned UC8253 banks cannot be ported** — different LUT format
  (see §1). This is a rewrite, not a copy, despite the near-identical command set.
- **No grayscale** (`supportsStripGrayscale()` false). The X3 reader's 4-level
  anti-aliasing path needs UC8279-format gray banks tuned on hardware.
- `TRES` is programmed 792×528 on the X3, but the UC8253 init programs
  **VRES = 600** (the OEM scans the full gate count). If the image is offset or
  compressed, the SDK suggests trying `0x02 0x58`.

The only project observed working this problem is
[`anki630/crossmosa-freeink-sdk`](https://github.com/anki630/crossmosa-freeink-sdk)
— *"UC8279 waveform tuning"*.

## 4. Datasheet

**Not retrieved.** The SDK authors cite **UC8279d_B 0.1 (December 2025)**; no
public URL was located. Recorded as an open acquisition — this is the single most
valuable missing document in the Xteink subject, because it is the only thing
standing between the X3's newer panel and working fast waveforms.

---

## Used By

### [Xteink X3](../../../devices/xteink/x3/README.md) — production from ~July 2026 (as **UC8279d**)

Same board, same 792×528 glass, same pinout as the UC8253 units; **only the
controller changes**. Profile `BoardConfig::XTEINK_X3_UC8279`. Selected at boot
by `detectX3DisplayController()`, which bit-bangs a half-duplex read on
SCLK 8 / SDA 10 / CS 21 / DC 4 / RST 5 / BUSY 6 and requires **two passes agreeing
byte-for-byte**.

The vendor gave the community advance notice of this switch — the only
pre-announced silent hardware change found in the family. Owners report a
**user-visible difference**: one X3 has *"slightly whiter background and clearer
text… page turns and menus seem slower"*, the other *"slightly darker background
and not as clear text… page turns and menus seem faster"*
([r/XTEINK `1vkuhbi`](https://old.reddit.com/r/XTEINK/comments/1vkuhbi/), 2026-08-10,
firsthand side-by-side comparison — **which unit is which controller is not
established**).

→ [`devices/xteink/x3/features/display.md`](../../../devices/xteink/x3/features/display.md)

### [Xteink X4 Pro](../../../devices/xteink/x4-pro/README.md) / [X4](../../../devices/xteink/x4/README.md) — newer batches (800×480)

Alternative to SSD1677/UC8179 on identical wiring. Distinguished from the UC8179
by `LUT_VER` ∈ {`0x02`, `0x68`, `0x69`}.

### [Xteink X4 Classic](../../../devices/xteink/x4-classic/README.md) — batch-dependent

Selected from NVS `hw_calib/screenType` = **2** or **0x0C**; **the bus cannot be
probed** on that board.

### EEGO A4 (as **UC8279C**, 768×552)

Not documented in this repository; recorded because the same SDK carries
`Uc8279cA4Driver` and it establishes the variant exists.

## See also

[`../uc8253/README.md`](../uc8253/README.md) — the part it replaces on the X3 ·
[`../uc8179/README.md`](../uc8179/README.md) — its 800×480 sibling ·
[`../README.md`](../README.md)

---

## Datasheet — **not obtained**, 2026-09-11. What was tried, and what would work.

The record above notes that the FreeInk authors hold **UC8279d_B rev 0.1, dated
December 2025** and wrote their driver from it. **That document was not located
publicly by this pass, and neither was any other UC8279 datasheet.**

### Attempts, all failed

| Source tried | Result |
|---|---|
| `crystalfontz.com/controllers/UltraChip/` | **Carries only UC8151 and UC8179.** The full controller index contains no other `UC82xx` |
| Crystalfontz document-id probe, ids 512–523 via the working trailing-number path | Returned FocalTech, D-FT3267, SSD1780, ST7567S/A, CH13620 and Hynitron CST816D — **no UC8279** |
| `buydisplay.com/download/ic/UC8279.pdf` | **403** |
| `good-display.com` product path, `v4.cecdn.yun300.cn` CDN | **403** / HTML |
| `e-paper-display.com`, `e-paper-display.cn` | **404** |
| `waveshare.com` / `waveshare.net` / `files.waveshare.com` wiki upload paths | 403 / 404 / HTML |
| GitHub code search `filename:UC8279 extension:pdf` | **`total_count: 0`** |
| **LCSC** `wmsc.lcsc.com/ftps/wm/search/global` | **403 on every UA tried** (Chrome, WhatsApp, ClaudeBot). `www.lcsc.com/search` HTML returns 200 but was not mined further |
| DuckDuckGo HTML endpoint | **HTTP 202 bot-check page**, no results, on four queries |
| `alldatasheet.com` | **403** |

### Honest status

**UltraChip publishes nothing.** There is no customer portal, no product page and
no public datasheet index. Every UltraChip document in circulation — including
the two now held in this repository for the [UC8253](../uc8253/README.md) and
[UC8179](../uc8179/README.md) — is a **PDF exported by a named UltraChip employee
with a consumer tool, stamped *"for TFT module use only"*, that leaked through a
module vendor or a distributor.** UC8279 is a 2025-era part; it has not leaked
yet, or not to a host reachable from here.

**This is a genuine unavailability, not a failed search.** Record it as such and
do not re-run the same twelve attempts.

### What would actually work, in order of likely success

1. **A Chinese module vendor's download page.** DKE, Good Display / 大连佳显,
   微雪 (Waveshare CN), 中景园, and Elecrow all publish controller PDFs beside the
   panels that use them — **Elecrow is where this repository's UC8253 came from**.
   Search in Chinese: `UC8279 规格书`, `UC8279 数据手册`, `UC8279d`.
2. **LCSC via the HTML storefront** (`https://www.lcsc.com/search?q=UC8279`) with
   UA `WhatsApp/2.23.20.0`, which returns 200 where the JSON API returns 403.
   LCSC serves datasheets from `datasheet.lcsc.com/lcsc/<id>.pdf`.
3. **Ask the FreeInk authors.** They hold `UC8279d_B 0.1 (Dec 2025)` and cite it
   openly in `Uc8279X4Driver.cpp`. A GitHub issue is the cheapest route to the
   exact document the drivers were written against.
4. **The EEGO Reader A4**, which the FreeInk SDK now supports, uses a
   **UC8279C** — a different sub-revision — and its vendor may publish more.

### Why it matters more than usual here

The UC8279 is the controller actually fitted to at least one shipping X4 Pro
(`hw_calib/screenType = 2`, `VER = 00 0F 68 00 00`, LUT_VER `0x68`), and the
FreeInk driver's own comments record that **the family datasheet's 6-byte LUT
groups do not fit the tables this part uses** — a 7-byte reading is required, and
the tail byte's role is unknown. That is precisely the kind of question only the
correct revision of the datasheet answers.

**Used by:** [Xteink X3](../../../devices/xteink/x3/README.md) (UC8279d) ·
[X4](../../../devices/xteink/x4/README.md) ·
[X4 Pro](../../../devices/xteink/x4-pro/README.md) ·
[X4 Classic](../../../devices/xteink/x4-classic/README.md).
