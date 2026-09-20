# Tracing nets from schematic PDFs

**Created:** 2026-09-07. **Status:** technique verified on 15 vendor schematics this session.
**Tooling verified:** poppler **26.06.0**, ImageMagick 7, on Linux via `nix-shell -p`.

A vendor schematic PDF is usually treated as a picture to be squinted at. For the large majority
of them that is wrong: they are **vector documents with a complete, coordinate-accurate text
layer**, and several EDA tools additionally emit *invisible* helper tokens that name every pin
and every net. Once you know that, a schematic becomes a database you can query, and a net list
can be recovered without opening a viewer.

This guide documents the method used to trace the LilyGO T-Display-S3, M5Stack Cardputer ADV,
DinMeter, Stamp-S3A and Cap-Bus sheets in this repository.

---

## 1. First, decide whether the file is traceable at all

Spend thirty seconds on this. It saves hours.

```bash
nix-shell -p poppler-utils --run 'pdfinfo   in.pdf'   # producer, page count, page size
nix-shell -p poppler-utils --run 'pdfimages -list in.pdf'   # embedded rasters
nix-shell -p poppler-utils --run 'pdftotext -layout in.pdf - | wc -w'
```

Read the three results together:

| Signature | Verdict |
|---|---|
| `Creator: Altium Designer` / `KiCad` / `OrCAD`, **0** rows from `pdfimages -list`, thousands of words | **Vector, fully traceable.** The best case, and by far the most common for hobbyist-market vendor schematics. |
| **1** full-page image the size of the page, `pdftotext` yields 0 words | **Raster scan. Not traceable by text.** Say so and stop. OCR is a different job with different error characteristics, and an OCR'd net name is not evidence. |
| 0 words but 0 images either | **Vector paths with no text**, i.e. the net labels were converted to outlined glyphs. Not traceable. Rare but real. |
| Healthy word count, but the words are all part values and no net names | Partly traceable: you can census designators and values, not connectivity. |

`pdfimages -list` printing only its two header lines means **zero** embedded images. That is a
positive signal, not a failure.

> **Do not reach for `pdfimages` to "extract the component drawings".** On 14 of the 15
> schematics traced for this guide it returned nothing at all, because there is nothing raster
> in them to return. The drawings are vector. To get a picture out, rasterise the page yourself
> with `pdftoppm` and crop (§7).

## 2. Why `-bbox-layout` beats `-layout`

`pdftotext -layout` tries to reconstruct one global column grid for the whole page. On a letter,
A3 or tabloid schematic sheet that is hopeless: a pin number at x=157 and a net label at x=110
belong together, but `-layout` has to reconcile them against every other object across 800
points of page width, and the result interleaves unrelated symbols. The word count looks
healthy and the output is unusable.

```bash
nix-shell -p poppler-utils --run 'pdftotext -bbox-layout in.pdf out.xhtml'
```

`-bbox-layout` abandons the grid and emits, for every word, its exact bounding box:

```xml
<word xMin="309.790967" yMin="533.008497" xMax="313.650077" yMax="543.319663">IBAT</word>
```

That is the whole trick. **A net label can be associated with the pin it sits beside only if you
know where both of them are**, and `-bbox-layout` is the only poppler mode that tells you.

Coordinates are PDF points (1/72 inch) with **y increasing downwards** — poppler normalises to a
top-left origin, which is the opposite of PDF user space. Get this backwards and every
above/below test inverts.

Note also: a *rotated* word has a small x-extent and a large y-extent. Comparing `xMax-xMin`
against `yMax-yMin` is a reliable rotation detector, and you will need it (§8).

## 3. The invisible token layer — the part nobody uses

Altium Designer's PDF export writes three families of helper tokens into the text layer. They
are invisible on screen (they are drawn in the same colour as the background, or clipped), but
`pdftotext` extracts them, and **each is placed at the exact schematic coordinate of the thing
it names**:

| Token | Meaning | Placed at |
|---|---|---|
| `CO<designator>` | component outline | the symbol's origin |
| `PI<designator><pin>` | pin instance | the pin's **electrical end point** |
| `NL<netname>` | net label | the label's anchor |

So `PIU7014` is U7 pin 14, `COR13` is R13's body, `NLG8` is the net label `G8`.

Two decoding rules that are not obvious and will silently corrupt a net list:

1. **The designator/pin split is ambiguous without context.** `PIU7014` could be `U7` pin `14`
   or `U701` pin `4`. Resolve it by first harvesting the real designator set from the
   `CO<designator>` tokens, then splitting `PI` tokens against that set, longest match wins.
   Altium zero-pads the pin number to two digits, so strip one leading `0` afterwards.
2. **`NL` tokens substitute `0` for every non-alphanumeric character.** `NLLCD0RS` is the net
   `LCD_RS`; `NLESP0EN` is `ESP_EN`; `NL05VIN` is `+5VIN`. If you read those literally you will
   invent nets that do not exist. Cross-check against the *visible* text at the same coordinate,
   which is unmangled.

**Not every export carries them.** Of the 19 sheets bboxed for this guide, 9 had `NL` tokens and
10 had none — the same vendor, the same tool, different export settings. Where `NL` is absent
the visible net-label text is still there at the right coordinate, so the method still works;
you just lose the ability to distinguish a net label from an ordinary annotation by token class,
and must do it geometrically or by rendering a crop.

## 4. Binding a label to a pin — and calibrating the sign of `dy`

Altium anchors a net label at the lower-left of its text and floats it **just above** the wire
it names. In poppler's top-left coordinates that means the label's y is a few points **less**
than the wire's y.

This matters more than it sounds. Pins on a symbol are typically 7 pt apart and the label floats
~3.2–4.2 pt above its wire — so a label is *nearly equidistant* from the pin above it and the
pin below it. Picking the nearest one gives you a net list that is plausible and off by one row.

Worked example, Cardputer ADV sheet 3, the BMI270 at `U7`:

```
NLG8 at y=142.20     U7.1  (SDO) at y=138.37   -> dy = +3.83
                     U7.14 (SDX) at y=145.37   -> dy = -3.17
NLG9 at y=149.20     U7.14 (SDX) at y=145.37   -> dy = +3.83
                     U7.13 (SCX) at y=152.91   -> dy = -3.71
```

Both readings are self-consistent. "Labels sit above" gives SDX=G8, SCX=G9; "labels sit below"
gives SDO=G8, SDX=G9 and leaves SCX unlabelled.

**Do not resolve this by preference — find a known answer on the same sheet and calibrate.**
Here, pin 1 (`SDO`) turned out to carry a 3.3 kΩ resistor `R43` up to `+3.3V`, and the sheet
prints `7-bit Address 69H` beside the symbol. A BMI270's SDO pin selects the I²C address, so
SDO *must* be strapped, not driven by a GPIO. That settles it: labels sit **above**, and the
correct binding is SDX=G8 (SDA), SCX=G9 (SCL). Every other net on the sheet then followed.

A second, independent confirmation arrived two sheets later: the same board's TCA8418 keyboard
controller has SDA and SCL on the same `G8`/`G9` pair, which only works under the "above"
reading.

**Always find and state your calibration case.** A strapped address pin, a crystal, a
regulator's own output, a connector whose pinout is published elsewhere — anything whose answer
you already know.

For vertical wires the same rule rotates: the label sits just **left** of the wire, so `dx` is
slightly negative.

## 5. Multi-sheet documents and off-sheet connectors

Three practical rules.

**Bbox the whole document at once, not page by page.** `pdftotext -bbox-layout` emits one
`<page>` element per sheet in a single XHTML, and you need cross-sheet lookups constantly:
a net labelled on sheet 1 is consumed on sheet 3, and the `CO` designator set you use to split
`PI` tokens must be harvested from *all* pages or pins on a sheet whose symbol origin fell
elsewhere will fail to parse.

**Off-sheet connectivity is by name, not by geometry.** A net that appears exactly once in the
whole document is a red flag: either it is genuinely unterminated, or the other end is a *port*
or *power port* symbol whose text you have classified as something else. Count occurrences of
every net name across all pages as a sanity pass. On the Cap CC1101 sheets, `CC1101_RF_SW0`
appears on pages 1 and 3 — that is the off-sheet link, and it is the only evidence of it.

**Power ports are not net labels.** `GND`, `+3.3V`, `VBUS`, `+5VIN` are drawn as symbols with
the text *inline with* the wire (dy ≈ 0) rather than floating above it, and on many exports they
get no `NL` token at all. Treat them as a separate class with their own geometry, or you will
report dozens of pins as unconnected when they are simply grounded.

## 6. A worked example end to end — the LilyGO T-Display-S3 charger

The question: an owner tracing a physical board reported the charger position `U6` carried a
**5-lead TSOT-23**, while this repository's records said the schematic specified a **SOP-8
`TP4065`**. One of the two had to be wrong, and it mattered, because the published procedure for
changing the board's charge current derives from an 8-pin part's datasheet.

```bash
nix-shell -p poppler-utils --run '
  pdfinfo T_Display_S3.pdf
  pdfimages -list T_Display_S3.pdf
  pdftotext -bbox-layout T_Display_S3.pdf tds3.xhtml'
```

`pdfinfo` reports `Creator: Altium Designer`, 1 page, 792×612 pt. `pdfimages -list` prints its
header and nothing else — **zero raster, fully vector**. Traceable.

Locate the part string, then enumerate the pin tokens for its designator:

```bash
python3 trace.py grep bbox/tds3.xhtml 'TP40'     # -> TP4065 at x=273.09 y=484.09
python3 trace.py grep bbox/tds3.xhtml '^PIU6'
```

```
p1 x=  264.50 y=  483.48  PIU604
p1 x=  283.50 y=  496.46  PIU603
p1 x=  241.50 y=  499.46  PIU601
p1 x=  283.50 y=  503.46  PIU605
p1 x=  264.50 y=  518.48  PIU602
```

**Five pin tokens. There is no `PIU606`, `PIU607` or `PIU608`.** The symbol is a 5-pin device.
Reading the pin-function text at each coordinate gives 1 `CHRG`, 2 `GND`, 3 `BAT`, 4 `VCC`,
5 `PROG` — the LTC4054/TP4054 SOT-23-5 arrangement.

The same check on two further LilyGO sheets (`T-DISPLAY-S3-AMOLED.pdf` `U5`,
`T-Display-S3-AMOLED-Touch.pdf` `U6`) returns five pins and the same five function names. Three
independent sheets agree.

Verdict: **the schematic never said SOP-8.** The owner's physical observation and the schematic
agree, and the repository's record of the schematic was wrong. That is a finding you can reach
in about four minutes, and could not reach at all without `-bbox-layout`.

Finally, render a crop as the durable artifact (§7) so the next reader does not have to trust
the transcription.

## 7. Getting pictures out of a vector schematic

`pdfimages` cannot help — there is no raster to extract. Rasterise the page and crop:

```bash
# 300 dpi => 1 PDF point = 300/72 = 4.1667 px
nix-shell -p poppler-utils --run 'pdftoppm -f 3 -l 3 -r 300 -png in.pdf /tmp/page'
nix-shell -p imagemagick   --run 'magick /tmp/page-3.png -crop WxH+X+Y +repage \
                                    -bordercolor white -border 12 out.png'
```

Convert a bbox coordinate to a crop offset by multiplying by `dpi/72`. Because you already know
the coordinates of the symbol you care about, the crop is exact rather than hunted for.

Rendering is also the **tie-breaker of last resort** when the text layer is ambiguous, and it
earned its place twice in this session:

- On the Cardputer ADV, two net labels extracted as the strings `GI` and `GO`. Both `G0` and
  `G1` exist elsewhere on the same sheet and extract correctly, so this was not a font-mapping
  fault. A 300 dpi crop showed the module symbol's own pin names beside them — `G1` and `G2`,
  in an unmistakable digit glyph. The net *names* really are the letters `GI`/`GO`: a vendor
  typo. The electrical answer (Grove SCL = GPIO1, SDA = GPIO2) was only obtainable by looking.
- On the Cap-Bus connector, two red labels sit on each wire. Only the render shows that **both**
  are net labels — a functional alias and a host-GPIO alias on the same net — rather than one
  label plus one annotation.

## 8. Failure modes actually hit

**Poppler merges independent rotated text objects that share an x-column.** On the T-Display-S3
sheet, poppler emitted a single `<line>` reading `R13 IBAT (mA) = 580`. No such string exists.
It is a vertical resistor designator `R13` and a separate rotated note `IBAT (mA) = 580`, drawn
in the same narrow x-band and glued together by poppler's line grouping. Detect this by checking
the inter-word gaps — genuine spaces within a rotated line are uniform (~1.2 pt here), and the
merge point often is too, so gap analysis alone is *not* sufficient. Render the crop.

**Greedy designator/pin splitting.** Covered in §3. `PIU7014` parsed naively as `U701` pin `4`
produced a plausible-looking but entirely fictional symbol.

**Symmetric proximity tolerance.** Covered in §4. A `±5 pt` window around a pin catches the
label belonging to the neighbouring pin. Rank by the sign of the offset, not by distance.

**`-layout` word counts as a proxy for tracing effort.** A sheet can yield 1 120 words of
perfectly extracted text and still be unreadable as `-layout` output. Judge traceability from
`pdfimages -list` and the producer string, not from word count.

**Absence of a label is not proof of no connection** — but absence of *anything* is close to it.
On the Cardputer ADV, BMI270 `INT1` (pin 4) and `INT2` (pin 9) have no net label. The stronger
statement available is that a row query across the *entire* sheet at those two y coordinates
returns **only** U7's own pin tokens: no other component pin, no label, no power port lies at
that height anywhere on the page. Combined with the same being true of the unused OIS pins on
the same symbol, that supports "not routed". State the query you ran, not just the conclusion.

## 9. Recommended order of work

1. `pdfinfo` + `pdfimages -list` + word count → traceable or not. **Record the negative result
   if not; it stops the next agent repeating the attempt.**
2. `pdftotext -bbox-layout` the whole document.
3. Harvest `CO` designators; build the designator set.
4. Split `PI` tokens against it; you now have every pin's coordinate.
5. Harvest `NL` tokens and visible label text.
6. **Find a calibration case with a known answer and fix the sign of `dy`.**
7. Bind labels to pins; classify power ports separately.
8. Census net names across all pages; investigate every net that appears exactly once.
9. Render crops for anything ambiguous, and for anything you want a future reader to be able to
   check without re-running any of this.

## 10. Limits

This recovers **labelled connectivity**. It does not recover wire geometry, so two pins joined by
an unlabelled wire are only detectable by exact row/column alignment, and a wire with a bend is
invisible. For full connectivity you need the source EDA files, a netlist export, or Gerbers —
none of which these vendors publish. Where a claim rests on alignment rather than on a label,
say so.

---

### See also

- [`scratch/schematic-tracing/`](../../scratch/schematic-tracing/README.md) — the tools
  (`trace.py`, `render.py`, `netlist.py`) and the per-file traceability census.
