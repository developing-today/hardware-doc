# Graphics and display libraries for e-paper

> The layer below a reader firmware: what draws pixels, what drives panels, and
> what the licence choice costs you.
>
> Snapshot **2026-09-04**. Repository facts `executed-success` (GitHub API).
> **Nothing was built, linked or benchmarked** — no hardware. Capability and
> suitability claims are `inferred`.

**Classification:** libraries — you link against these and call them. Contrast
[`frameworks/`](../frameworks/freeink-sdk/README.md), which call *you*.

## The landscape

| Library | ★ | Licence | HEAD | Last push | Layer |
|---|---|---|---|---|---|
| [`lvgl/lvgl`](https://github.com/lvgl/lvgl) | 24,586 | **MIT** | `a33757e2` | 2026-09-04 | Full widget UI toolkit |
| [`olikraus/u8g2`](https://github.com/olikraus/u8g2) | 6,664 | BSD-2 *(see below)* | `9a93ba2e` | 2026-08-23 | Monochrome drawing + fonts |
| [`adafruit/Adafruit-GFX-Library`](https://github.com/adafruit/Adafruit-GFX-Library) | 2,836 | BSD *(see below)* | `ac6d7c38` | 2026-04-09 | Minimal drawing primitives |
| [`vroland/epdiy`](https://github.com/vroland/epdiy) | 1,916 | **LGPL-3.0** | `42c16127` | 2026-08-23 | Parallel e-paper driver + board |
| [`waveshareteam/e-Paper`](https://github.com/waveshareteam/e-Paper) | 1,731 | **none** | `a794fbc3` | 2026-08-19 | Vendor panel demos |
| [`ZinggJM/GxEPD2`](https://github.com/ZinggJM/GxEPD2) | 1,480 | **GPL-3.0** | `de82887e` | 2026-04-19 | SPI e-paper panel driver |
| [`moononournation/Arduino_GFX`](https://github.com/moononournation/Arduino_GFX) | 1,137 | BSD *(see below)* | `b4c3cbe2` | 2026-08-30 | Fast colour display driver |
| [`s00500/ESPUI`](https://github.com/s00500/ESPUI) | 1,124 | MIT *(see below)* | `1eb5e2ff` | 2026-04-30 | Browser-served UI, not on-device |
| [`bitbank2/JPEGDEC`](https://github.com/bitbank2/JPEGDEC) | 625 | **Apache-2.0** | `86282979` | 2026-03-13 | JPEG decode for MCUs |
| [`bitbank2/bb_epaper`](https://github.com/bitbank2/bb_epaper) | 207 | **GPL-3.0** | `29afe89e` | 2026-09-03 | "All 24-pin eink panels" |

*"see below"* marks repositories GitHub reports as `NOASSERTION` — it cannot
classify the licence automatically. That is **not** the same as unlicensed; it
usually means a non-standard file or a licence header style Linguist doesn't
match. `waveshareteam/e-Paper` is the genuinely licence-less one.

## The finding that actually matters: e-paper libraries skew copyleft

Sort the table by what layer it occupies and a pattern appears:

| Layer | Typical licence |
|---|---|
| General graphics / UI (LVGL, Adafruit-GFX, u8g2, Arduino_GFX) | **permissive** — MIT / BSD |
| **E-paper panel drivers** (GxEPD2, bb_epaper, epdiy) | **copyleft** — GPL-3.0 / LGPL-3.0 |

**This is a real constraint on firmware architecture, not trivia.**
[CrossPoint Reader](../applications/crosspoint-reader/README.md) and the
[FreeInk SDK](../frameworks/freeink-sdk/README.md) are both **MIT**. Linking
GxEPD2 (GPL-3.0) or `bb_epaper` (GPL-3.0) into a distributed firmware binary
would place the combined work under the GPL. LGPL (epdiy) is more permissive but
its dynamic-linking relief is close to meaningless on a statically-linked MCU
image.

That plausibly explains an otherwise odd choice: **FreeInk ships its own SSD1677
and UC8253 drivers**, derived — per its `NOTICE` — from the MIT-licensed
`open-x4-epaper/community-sdk` with authorship credited to CidVonHighwind, rather
than adopting the far more popular GxEPD2. Writing panel drivers is real work
that a mature GPL library had already done.

**Marked `inferred`.** No maintainer has stated this motivation anywhere I found;
it is the reading the licences and the code lineage support. But if you are
choosing a driver for a permissively-licensed firmware, the constraint is real
regardless of whether it motivated FreeInk.

## What each is actually for

### LVGL — the heavyweight
A complete widget toolkit: objects, layouts, styles, animations, input devices,
theming. Genuinely excellent, genuinely large, and designed for **colour,
frequently-refreshed** panels.

On e-paper it is a poor fit by default and needs deliberate work: LVGL assumes
cheap partial redraws, e-paper does not. It supports 1-bit output and monochrome
themes, but its animation and invalidation model fights the medium. **Nothing in
the CrossPoint/FreeInk ecosystem uses it** — FreeInk wrote `FreeInkUI`, an
immediate-mode layer sized for e-paper, instead.

Use LVGL when you have a colour TFT and want widgets. On a 4-grey 800×480 e-paper
reader it is usually the wrong tool.

### GxEPD2 — the default Arduino e-paper driver
The most widely used SPI e-paper library, covering an enormous panel matrix. If
you are wiring a Waveshare or Good Display panel to an Arduino, this is what
tutorials assume.

**GPL-3.0**, which is the thing to notice before designing around it. Also last
pushed **2026-04-19** — the least recently touched library in this table, which
for a driver library tracking new panels is worth checking against your specific
panel.

### `bb_epaper` — the newer challenger
"A frustration-free library for working with all 24-pin eink panels", from
Larry Bank (`bitbank2`), who also wrote JPEGDEC. Actively pushed (2026-09-03),
smaller and more opinionated than GxEPD2. **GPL-3.0**, same constraint.

Relevant here: prior research recorded it as shipping **M5Stack PaperMono
support**, which makes it one of the few third-party libraries that names this
board.

### `u8g2` — monochrome done properly
The strongest option for **monochrome-only** work: a huge, well-curated font
collection, tight memory behaviour, and support for a very wide range of
displays including many e-paper panels. Permissively licensed (BSD-2-Clause).

If your device is 1-bit and text-heavy, u8g2's font handling is better than
anything else in this list.

### Adafruit-GFX — the lowest common denominator
Small, permissive, and the drawing API that half the Arduino ecosystem inherits.
It is a **drawing primitive layer**, not a driver — you pair it with a
device-specific backend. Its value is ubiquity and licence, not capability.

### `epdiy` — parallel-interface panels
For large, cheap **parallel-interface** e-paper (repurposed laptop and e-reader
panels), which SPI libraries cannot drive at all. Different problem space to
GxEPD2. **LGPL-3.0**.

### `waveshareteam/e-Paper` — vendor demos
Waveshare's own panel code. Broad panel coverage and **no licence file at all**,
which makes it all-rights-reserved by default and awkward to vendor. Treat it as
reference material for initialisation sequences rather than a dependency — which,
in practice, is how the ecosystem uses it.

### `JPEGDEC` — decode, not draw
Apache-2.0, MCU-optimised JPEG decode. Notable because
**`crosspoint-reader` forked it into its own org** — a small, permissively
licensed, single-purpose library is exactly the kind of dependency that survives
in constrained firmware.

### `ESPUI` — a different axis entirely
Serves a web UI from the ESP32 to a browser. **Nothing renders on the device.**
It solves the same problem upstream CrossPoint's JavaScript plugin system solves
— configuration and interaction via a phone — and is worth knowing about for that
reason, but it is not a display library. See
[plugin systems](../applications/crosspoint-reader/plugins/README.md).


## Licences resolved by reading the files (2026-09-04)

The table marks four repositories `NOASSERTION` — GitHub could not classify them.
That was listed as an open question. All four have now been **read directly**
(`executed-success`):

| Library | Actual licence | Evidence |
|---|---|---|
| `olikraus/u8g2` | **BSD-2-Clause** (new-BSD) | `LICENSE`: *"The U8g2lib code … is licensed under the terms of the new-bsd license (two-clause bsd license)"* |
| `adafruit/Adafruit-GFX-Library` | **BSD** | `license.txt`: *"Software License Agreement (BSD License), Copyright (c) 2012 Adafruit Industries"* |
| `moononournation/Arduino_GFX` | **BSD** | `license.txt` — byte-for-byte Adafruit's, **including Adafruit's own copyright line** |
| `s00500/ESPUI` | **MIT** | `LICENSE`: *"The MIT License (MIT), Copyright (c) 2017 Lukas Bachschwell"* |

None is unlicensed. `NOASSERTION` meant a non-standard filename or preamble, not
absence — as suspected, and now confirmed rather than assumed.

### ⚠ The u8g2 font trap

Reading the file surfaced something the licence label hides. `u8g2`'s `LICENSE`
says, immediately after declaring the code BSD-2:

> **Fonts are licensed under different conditions.**

And the file **contains GPL text** further down, because some bundled fonts carry
GPL terms while others are BSD, public-domain, or under bespoke foundry licences.

**So "u8g2 is BSD" is true of the code and false of the deliverable.** A firmware
that links u8g2 *and ships its fonts* may be taking on obligations — including
copyleft — that the repository's headline licence does not suggest. Anyone
shipping a permissively-licensed binary needs to check the specific fonts they
compile in, not the library.

This is exactly the shape of the copyleft problem described above, one layer
lower: the code is permissive, the **content** is not uniformly so. Worth noting
that the CrossPoint ecosystem keeps fonts in a **separate repository**
(`crosspoint-reader/crosspoint-fonts`, which itself carries **no licence file**)
and loads them from SD at runtime rather than compiling them in — which sidesteps
the linking question entirely, whether or not that was the motivation.

### `Arduino_GFX` carries Adafruit's copyright

Its `license.txt` is Adafruit's BSD text verbatim, retaining *"Copyright (c) 2012
Adafruit Industries"*. That is consistent with its API lineage — it descends from
Adafruit-GFX — but it means the file does not name `Arduino_GFX`'s own author.
Recorded as an observation; the practical effect is the same BSD terms either way.

## Choosing, for an e-paper reader

| If you need | Use | Watch out for |
|---|---|---|
| Widgets on a colour TFT | **LVGL** | Overkill and a poor invalidation fit on e-paper |
| Monochrome text and fonts | **u8g2** | Not a full UI toolkit |
| Drive an SPI e-paper panel, permissive licence not required | **GxEPD2** | **GPL-3.0**; least-recently-updated here |
| Same, actively maintained | **bb_epaper** | **GPL-3.0** |
| Large parallel e-paper | **epdiy** | **LGPL-3.0**; different hardware entirely |
| Panel init sequences as reference | `waveshareteam/e-Paper` | **No licence** — read, don't vendor |
| A permissively licensed reader firmware | **FreeInk SDK** | It is a *framework*, not a library — it takes over structure |

**The licence column is the one that constrains architecture.** Everything else
is a preference; GPL versus MIT is a decision about what you can ship.


## Sources

Repository metadata and HEAD commits for all eleven repositories, GitHub REST
API, authenticated, retrieved **2026-09-04**. SHAs are in the table and are the
identity to cite.

## Open questions

- **Nothing was built, linked, benchmarked or run.** No binary size, refresh
  timing, or RAM figure here is measured; there is no hardware.
- ~~The `NOASSERTION` licences were not resolved~~ — **closed 2026-09-04**: all
  four read at source (see above). Outstanding sub-question: **u8g2's per-font
  licences were not enumerated**, and at least some are not BSD.
- The claim that GxEPD2's GPL motivated FreeInk's own drivers is `inferred` from
  licences and lineage; **no maintainer statement was found**.
- Which e-paper panels each library actually supports was not enumerated.
- `bb_epaper`'s reported PaperMono support is carried over from earlier research
  and was **not verified** in this pass.

## See also

- [FreeInk SDK](../frameworks/freeink-sdk/README.md) — ships its own SSD1677/UC8253 drivers, and why that matters
- [`components/solomon-systech/ssd1677`](../../components/solomon-systech/ssd1677/README.md) — the controller most of this targets
- [`guides/hardware`](../../guides/hardware/README.md) — e-paper waveforms, bias rails, ghosting
- [PaperMono e-paper feature guide](../../devices/m5stack/papermono/features/epaper-display.md)
