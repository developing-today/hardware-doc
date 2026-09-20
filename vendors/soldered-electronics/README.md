# Soldered Electronics — vendor documentation guide

> Reusable knowledge for finding and validating Soldered (formerly **e-radionica**) documentation, hardware design data and source code.
> Established **2026-08-24** while researching the [Inkplate 5 / Gen 2](../../devices/soldered-electronics/inkplate-5/README.md) and [ZeroWriter Ink](../../devices/zerowriter/zerowriter-ink/README.md).

**Soldered Electronics (TAVU)** — Osijek, Croatia. Makers of the Inkplate e-paper series, Qwiic/easyC breakouts, and Dasduino boards. Rebranded from **e-radionica** around 2021–2022.

## Summary: go to GitHub first

Soldered's most reliable, most complete and most machine-readable documentation is **in their GitHub organisation**, not on their website. Product pages are marketing; the hardware repos contain the KiCad sources, BOM CSVs, schematic PDFs, gerbers, 3D models, interactive BOMs *and* the CE/UKCA compliance certificates.

| What you want | Where to get it |
|---|---|
| Schematics, BOM, gerbers, 3D, compliance | `github.com/SolderedElectronics/Soldered-<Product>-hardware-design` |
| Library source, examples, board defines | `github.com/SolderedElectronics/Inkplate-Arduino-library` |
| Authoritative pin/resolution constants | `src/boards/<BoardName>/pins.h` and `waveforms.h` in the Arduino library |
| Prose documentation | `soldered.com/documentation/inkplate` (**current**) |
| Tutorials | `learn.soldered.com` |
| Community support | `community.soldered.com` |
| Custom PCB service | `pcb.soldered.com` |

## URL templates

```
https://github.com/SolderedElectronics/Soldered-<Product>-hardware-design
https://github.com/SolderedElectronics/Soldered-Inkplate-5-hardware-design
https://github.com/SolderedElectronics/Soldered-Inkplate-5-Gen2-hardware-design
https://github.com/SolderedElectronics/Soldered-Inkplate-6-MOTION-hardware-design
https://github.com/SolderedElectronics/Soldered-Inkplate-4-TEMPERA-with-glass-panel-hardware-design
https://codeload.github.com/SolderedElectronics/<repo>/tar.gz/<commit>     # pinned snapshot
https://www.solde.red/<SKU>                                               # short link to a product page
```

### Naming is inconsistent — search, don't guess

Older repos use the **pre-rebrand** naming without the `Soldered-` prefix:

| Newer convention | Older convention |
|---|---|
| `Soldered-Inkplate-10-hardware-design` | `Inkplate-10-hardware` |
| `Soldered-Inkplate-6-hardware-design` | `Inkplate-6-hardware` |

**Both often exist for the same product** and are *not* the same content — the older repo may cover an earlier board revision. `Inkplate-6-hardware` (205★, last pushed 2021) and `Soldered-Inkplate-6-hardware-design` (5★) are different artifacts. Check both.

Also note the **Gen2** repos are named `...-Gen2-...` while the Arduino library calls the same board `Inkplate5V2` and the store calls it "Gen 2". Three names, one board.

Reliable enumeration:

```bash
curl -s -H 'Accept: application/vnd.github+json' \
  'https://api.github.com/orgs/SolderedElectronics/repos?per_page=100&page=1'
```

⚠ The org has **200+ repositories** — you must paginate. A single unpaginated call silently misses most Inkplate hardware repos. This caught me: page 1 returned no `Inkplate-5` repos at all; they only surfaced via `/search/repositories?q=inkplate+5+in:name`.

## Hardware repository layout

Every `*-hardware-design` repo follows the same structure, which makes them scriptable:

```
CAD/<VERSION>/           KiCad sources — hierarchical sheets, .kicad_pcb, PANEL/, Source 3D files/
OUTPUTS/<VERSION>/       <Product> BOM.csv
                         <Product> Schematics.pdf
                         <Product> iBOM.html          ← interactive BOM, very useful
                         <Product> ... gerber.zip
                         <Product> 3D.step
                         3d printable files/
OUTPUTS/Compliance/      CE.pdf, UKCA.pdf, Safety sheet EN.pdf, Safety sheet DE.pdf, Info.txt
LICENSE.md               TAPR Open Hardware License v1.0
README.md
```

Two things to know:

**The README is often an unedited template.** `Soldered-Inkplate-5-hardware-design/README.md` still contains the literal placeholders `--- Product name ---`, `------ product description ------` and a Wikipedia `Example_image.svg`. Do not conclude the repo is empty or wrong — the `CAD/` and `OUTPUTS/` folders are real and complete. Ignore the README; read the BOM.

**The BOM CSV delimiter varies.** Soldered's KiCad exports use **semicolons** (`Id;Designator;Package;Quantity;Designation;Supplier and ref;`), while ZeroWriter's fork of the same project exports **commas** with different columns (`Reference,Value,Datasheet,Footprint,Qty,DNP`). Sniff the delimiter; do not hardcode.

## Licensing

**All Soldered open-source hardware is under the TAPR Open Hardware License v1.0.** This is a real open-hardware licence that permits manufacture, modification and redistribution with reciprocal documentation obligations. It is why ZeroWriter could legally respin the Inkplate 5 Gen 2 and publish the result.

⚠ **GitHub reports these repos as `NOASSERTION`** because its licence detector does not recognise TAPR OHL. Do not take that as "unlicensed". The `LICENSE.md` in the repo root is an unambiguous grant. Several Soldered hardware repos show `NOASSERTION` or `None` in the API and are all TAPR OHL.

Software licences vary per repository and *are* correctly detected:

| Repo | Licence |
|---|---|
| `Inkplate-Arduino-library` | **LGPL-3.0** |
| `Inkplate-micropython` | MIT |
| `Inkplate-ESP-IDF-component` | GPL-3.0 |
| `Soldered-Inkplate-ESPHome` | GPL-3.0 |
| `Inkplate-LVGL-Library` | GPL-3.0 |

## Documentation migration: readthedocs → soldered.com

**`inkplate.readthedocs.io` is deprecated.** The `Inkplate-documentation` repository is still public and still contains the full `.rst` source, but **every page now begins with a JavaScript redirect**:

```rst
.. raw:: html

    <script>
        window.location.href = "https://soldered.com/documentation/inkplate";
    </script>
```

Consequences:

- **Fetching a readthedocs page with `curl` returns a redirect shim, not content.** The text is invisible to naive scraping.
- The **`.rst` source in the GitHub repo is still fully readable** and is the best machine-readable form of the prose documentation. `Inkplate-documentation/source/*.rst` — roughly 10,000 lines across `arduino.rst` (4,556), `micropython.rst` (2,404), `esp-idf.rst` (1,222), `peripheral-mode.rst` (633), `examples.rst`, `features.rst`, `gui-designer.rst`.
- The repo also has some **stale content**: `hardware-reference.rst` still says *"Inkplate 5 hardware repository is coming soon"*, although that repository has existed since 2024-10-20.

**Recommendation:** clone `Inkplate-documentation` and read `source/*.rst` directly. Ignore the rendered readthedocs site.

⚠ The repo is **~700 MB** because it commits the generated Sphinx `build/` output (535 MB) alongside 135 MB of documentation images. If you only want the text, fetch the tarball and keep `source/*.rst` — that is a few hundred kilobytes. See the archive placeholders under [`inkplate-5/artifacts/docs/`](../../devices/soldered-electronics/inkplate-5/artifacts/docs/).

## Traps encountered

| Trap | Detail |
|---|---|
| Product-page 404s | `soldered.com/product/...` slugs change. `.../soldered-inkplate-5-9-7-e-paper-board-copy/` returned **404 with a 561 KB HTML body** — validate on status code, not on response size |
| GitHub org pagination | 200+ repos; page 1 omits most Inkplate hardware repos |
| `NOASSERTION` licences | TAPR OHL is not machine-detected; read `LICENSE.md` |
| Template READMEs | Placeholder text in real, populated repos |
| Three names per board | "Inkplate 5 Gen 2" (store) = `Inkplate5V2` (library) = `Soldered-Inkplate-5-Gen2-hardware-design` (repo) |
| readthedocs JS redirect | Rendered docs unscrapeable; use the `.rst` source |
| Mixed CSV delimiters | Semicolon in Soldered exports, comma in forks |
| Old vs new brand | `e-radionicacom` is **not** a valid GitHub org today; use `SolderedElectronics` |

## The authoritative source for board constants

For any Inkplate, **the Arduino library is the ground truth** for resolution, pin mapping and peripheral addresses — more so than the store page:

```
Inkplate-Arduino-library/src/boards/<Board>/waveforms.h   → E_INK_WIDTH / E_INK_HEIGHT
Inkplate-Arduino-library/src/boards/<Board>/pins.h        → control-signal mapping, IO_INT_ADDR
Inkplate-Arduino-library/src/boards/<Board>/<Board>Driver.cpp → I2S pin assignment, refresh sequence
```

`src/boards/` is also the definitive list of supported boards: `Inkplate2`, `Inkplate5`, `Inkplate5V2`, `Inkplate6`, `Inkplate6COLOR`, `Inkplate6FLICK`, `Inkplate6PLUS`, `Inkplate10`, `Inkplate4TEMPERA`, `Inkplate13SPECTRA`.

**Inkplate 6 MOTION is a separate architecture** with its own library (`Inkplate_Motion_Arduino_Library`) and is not in that list.

## Related

- [Inkplate 5 / Gen 2](../../devices/soldered-electronics/inkplate-5/README.md)
- [Inkplate Peripheral Mode](../../devices/soldered-electronics/inkplate-5/features/peripheral-mode.md)
- [ZeroWriter Ink](../../devices/zerowriter/zerowriter-ink/README.md)
