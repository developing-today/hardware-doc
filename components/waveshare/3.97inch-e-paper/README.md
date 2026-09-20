# Waveshare 3.97inch e-Paper (raw panel module)

- **Category:** 3.97-inch active-matrix electrophoretic (AM EPD) display module — 800 × 480, bi-stable, pure-reflective, SPI
- **Driver IC:** **[Solomon Systech SSD1677](../../solomon-systech/ssd1677/README.md)**, bonded on (COG)
- **Vendor part number:** **not published.** Waveshare sells and documents this panel only as "3.97inch e-Paper"; no supplier or module part number appears on the storefront, in the docs, in the manual, or in the schematic's text layer
- **Document status:** manual **Rev 1.0, 2025-04-24** — revision history reads "New creation", so this is the first published revision
- **Research status:** manual retained in [`artifacts/`](artifacts/). **Its text layer is offset-encoded and must be decoded before use** — see [below](#the-manual-has-a-hostile-text-layer)
- **Retrieved:** 2026-09-01. **Nothing verified on hardware.**

Filed under `components/waveshare/` rather than under a board because **it is a panel,
not a board** — it is sold both as a standalone raw panel (`3.97inch e-Paper HAT+`
product family, from whose file directory the manual is served) and fitted to the
[ESP32-S3-ePaper-3.97](../../../devices/waveshare/esp32-s3-epaper-3.97/README.md).

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[MAN]** | `artifacts/3.97inch-e-paper-manual-v1.0-2025-04-24.pdf`, decoded text layer, cited by section number where the document gives one | `executed-success` for the decode and transcription; `not-tested` for the values themselves |
| **[SCH]** | The host board's schematic, `devices/waveshare/esp32-s3-epaper-3.97/artifacts/schematic/` | `executed-success` for the extraction |
| **[SRC]** | Waveshare driver source at a cited `file:line` | `executed-success` for the read |
| **[STORE]** | Waveshare storefront/docs prose | `reported-working` — vendor claim |

## Specifications

| Property | Value | Evidence |
|---|---|---|
| Screen size | 3.97 inch | **[MAN]** |
| Resolution | **800 × 480** | **[MAN]**, **[SRC]** `EPD_3in97.h:35–36` |
| **Active area** | **86.40 × 51.84 mm** | **[MAN]** |
| Outline | 56.24 (H) × 96.62 (V) × 0.92 (D) mm | **[MAN]** |
| Pixel pitch | 0.108 × 0.108 mm | **[MAN]** §4-4 |
| **DPI** | **235** | **[MAN]** |
| Weight | 10.44 ± 0.5 g | **[MAN]** |
| Colours | Black / white | **[STORE]** |
| Greyscale | **4 levels** | **[STORE]**; the driver exposes `Init_4GRAY` / `Display_4Gray` **[SRC]** |
| Viewing angle | > 170° | **[STORE]** |
| Interface | 3-wire (9-bit) or 4-wire (8-bit) SPI, selected by `BS1` | **[MAN]** §6.4 |
| Core logic voltage | 1.7 / **1.8** / 1.9 V | **[MAN]** |
| Operating temperature | **0 to +50 °C** | **[MAN]** |
| Storage temperature | −25 to +70 °C | **[MAN]** |
| Optimal storage humidity | 55 ± 10 % RH | **[MAN]** |

### Timing and power

| Parameter | Value | Conditions | Evidence |
|---|---|---|---|
| 4-grey update | **3 s** | 23 °C | **[MAN]** |
| Partial update | **0.3 s** | 23 °C | **[MAN]** |
| Typical power | **36 mW** | V = 3.0 V | **[MAN]** |
| Deep-sleep power | **0.003 mW** | V = 3.0 V | **[MAN]** |
| Peak current | **120 mA** | — | **[MAN]** |

The manual states these were measured with a **Tektronix TCP0030A** current probe
under a defined pattern transition — unusually specific for a panel document, and
worth preserving because it makes the figures comparable to nothing else that does
not state the same.

> **These are panel figures, not board figures.** The host board's storefront quotes
> different, slower numbers (full 3.5 s, fast 2.8 s, partial 0.6 s). That is expected
> — a board number includes the host's SPI transfer — but neither set is a
> measurement you can rely on. See
> [C-WS6](../../../devices/waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws6--refresh-times-disagree-between-module-and-panel-documents).

## What the panel provides on its own

From the manual's own description **[MAN]**:

> The display is capable to display image at 1-bit white and black full display
> capabilities. The 3.97 inch active area contains 800 × 480 pixels. The module is a
> TFT-array driving electrophoresis display, with integrated circuits including gate
> driver, source driver, MCU interface, timing controller, oscillator, DC-DC, SRAM,
> LUT, and VCOM.

Note **"1-bit white and black"** in the module's own overview, against the marketed
**4 greyscale**. This is the same tension the
[DKE DEPG0397BBS770F3 record](../../dke/depg0397bbs770f3/README.md) documents for the
PaperMono's panel, where the manual's optical table says 2 grey levels and the vendor
markets 4. **The pattern recurs across 3.97" panels from different vendors** — read
it as "4-grey is achievable with the right waveform, 1-bit is what the module
guarantees", and treat 4-grey quality as something to verify per unit.

Because the SSD1677 integrates the **DC-DC, oscillator, SRAM, LUT and VCOM**
generation, a host board needs no EPD boost converter — it supplies logic power and
the SPI lines, and the panel's `GDR`/`RESE` pins plus an inductor close the boost
loop. The host board's FPC connector `J2` carries `VGH`, `VGL`, `VSH1`, `VSH2`,
`VSL`, `VCOM`, `VPP`, `GDR` and `RESE`, consistent with that topology **[SCH]**.

## Pin interface

The manual's pin table names, among others:

| Pin | Role | Evidence |
|---|---|---|
| `VDDIO` (15) | Power supply for interface logic pins; should be tied to `VCI` | **[MAN]** |
| `VDDP` (16) | Power supply for the chip | **[MAN]** |
| `VDD` (18) | Core logic, regulated internally from `VCI`; needs a capacitor | **[MAN]** |
| `BSI` (8) | **Bus interface selection**: H = 3-wire 9-bit SPI, L = 4-wire 8-bit SPI | **[MAN]** §5-5 |
| `RESE` (3) | Current-sense input for the boost control loop | **[MAN]** |

The SSD1677 additionally offers an **I²C master interface to read an external
temperature sensor** **[MAN]** — relevant because e-paper waveforms are strongly
temperature-dependent, and a panel that can read its own ambient temperature can
select its LUT without host involvement. Whether the host board wires this is
**not established**.

## The manual has a hostile text layer

**Do not `grep` this PDF and believe the result.** The document embeds two subset
fonts whose code points are uniformly displaced from the real characters:

| Font | Offset | Raw | Decoded |
|---|---|---|---|
| A | **+26** | `OTINK 6GVKX` | `inch e-Paper` |
| B | **+29** | `LQFKH 3DSHU` | `inch e-Paper` |

Naive extraction yields text that is **human-legible but wrong** — the most dangerous
PDF failure mode, because it does not look like a failure. The method's rule applies
literally here: *validate the text layer against a known heading before transcribing
any value.*

The decoder used, and the validation against the cover heading `3.97inch e-Paper`, is
[`tools/deshift.py`](../../../devices/waveshare/esp32-s3-epaper-3.97/tools/deshift.py)
with the procedure in
[`commands.md` §6](../../../devices/waveshare/esp32-s3-epaper-3.97/commands.md).
**Only after the heading validated was `Driver IC: SSD1677` — or any number above —
transcribed.**

## Is this the same panel as the M5Stack PaperMono's?

| Property | This panel | [DKE `DEPG0397BBS770F3`](../../dke/depg0397bbs770f3/README.md) |
|---|---|---|
| **Active area** | **86.40 × 51.84 mm** | **51.84 × 86.40 mm** |
| **DPI** | **235** | **235** |
| **Driver IC** | **SSD1677** | **SSD1677** |
| Resolution | 800 × 480 | 480 × 800 |
| Greyscale marketed / manual | 4 / "1-bit" | 4 / 2 |
| Part number | **not published** | `DEPG0397BBS770F3` |

Active area matches **to 0.01 mm** transposed; DPI is identical; the controller is
identical. **This is `inferred` and deliberately not asserted.** It is equally
consistent with one panel sold to two board vendors, two panels built to a common
ESL-market reference, or coincidence in a size where the controller dictates the
geometry.

What would settle it: a photograph of the FPC marking on either board, or Waveshare
publishing a part number. Tracked as
[C-WS8](../../../devices/waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws8--is-this-the-same-panel-as-the-papermonos).

### One place the two documents actively disagree

This manual states **"Resolution: 800 gate × 480 source"** **[MAN]** §4-3. The DKE
record derives the **opposite** — 800 *source* × 480 *gate* — from SSD1677 register
values (`0x44` sets `XEA = 799`; the frame is 48 000 bytes = 800 × 480 / 8), which is
stronger evidence than a specification line.

Unresolved. Practical impact is low because drivers address the framebuffer, but it
matters if you write your own controller init. See
[C-WS7](../../../devices/waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws7--gate-versus-source-orientation).

## Software

The reference driver is Waveshare's own `EPD_3in97.cpp/.h`
([repo](https://github.com/waveshareteam/ESP32-S3-ePaper-3.97) @ `9b12d40`), which
exposes:

| Function group | Members |
|---|---|
| Init | `Init`, `Init_Fast`, `Init_Partial`, `Init_4GRAY` |
| Display | `Display`, `Display_Base`, `Display_Fast`, `Display_Fast_Base`, `Display_Partial`, `Display_4Gray`, `WritePicture_4Gray` |
| Windowed | `V2_Display_Window`, `V2_Display_Window_Base` |
| Clear | `Clear`, `Clear_Black` |

The `_Base` variants write the previous-image buffer, which is what makes correct
partial refresh possible on an SSD1677 — the controller diffs old against new. The
presence of `V2_` names suggests lineage from Waveshare's generic e-paper driver
family rather than code written for this panel.

Generic SSD1677 behaviour, register map and the **DC-balance hazard** are documented
once, in the [SSD1677 record](../../solomon-systech/ssd1677/README.md) — not repeated
here.

## Artifacts

| File | Bytes | SHA-256 | Source | Retrieved |
|---|---|---|---|---|
| [`artifacts/3.97inch-e-paper-manual-v1.0-2025-04-24.pdf`](artifacts/3.97inch-e-paper-manual-v1.0-2025-04-24.pdf) | 2 774 287 | `4f756734dbfa7485c57e7ab7124f59f0afb00ca2600cda24a2285f02e4ab05cf` | `https://files.waveshare.com/wiki/3.97inch_e-Paper_HAT%2B/3.97inch_e-Paper.pdf` | 2026-09-01 |

Validated as a real PDF by magic bytes (`%PDF-`), not by HTTP status.
**Licence `unknown`** — the document states no terms. Disposition: `repository`.

## Used by

### [Waveshare ESP32-S3-ePaper-3.97](../../../devices/waveshare/esp32-s3-epaper-3.97/README.md)

Fitted as the integrated display, on FPC connector `J2`. Driven over **4-wire SPI**
from the ESP32-S3: `EPD_SCK` GPIO11, `EPD_DIN` GPIO12, `EPD_CS` GPIO10, `EPD_DC`
GPIO9, `EPD_RST` GPIO46, `EPD_BUSY` GPIO3 — corroborated by both the schematic and
`DEV_Config.h`. Panel supply comes from an
[AXP2101](../../x-powers/axp2101/README.md) rail (`EPD_VCC_AXP`); there is **no
GPIO-controlled panel power pin** (`EPD_PWR_PIN -1`), so power gating is a PMIC
operation. Full map in
[pinouts-and-buses.md](../../../devices/waveshare/esp32-s3-epaper-3.97/pinouts-and-buses.md).

### Sold standalone

As a raw panel in the `3.97inch e-Paper HAT+` family — the manual is served from that
product's file directory. Those products were **not researched** in this pass; only
the panel document was taken.

## See also

- [SSD1677 controller](../../solomon-systech/ssd1677/README.md)
- [DKE DEPG0397BBS770F3](../../dke/depg0397bbs770f3/README.md) — the comparable panel on the PaperMono
- [Waveshare documentation-sourcing guide](../../../vendors/waveshare/README.md)
- [All components](../../README.md)
