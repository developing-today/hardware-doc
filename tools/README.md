# `tools/` — extraction and housekeeping scripts

Small, dependency-free Python that turns downloaded artifacts into facts. Everything here uses
**only the standard library** on purpose: several of these were written on hosts with no
`pdftotext`, no `pip`, and no `file(1)`.

Run them from the repository root unless a script says otherwise.

## Housekeeping — the archive

| Script | What it does |
|---|---|
| [`archive_artifact.py`](archive_artifact.py) | **The only supported way to move an artifact into `archive/`.** Moves a file or directory to its repo-relative path under the archive, verifies content by fingerprint after the move, refuses to clobber an existing entry with different bytes, writes a standalone `*.ARCHIVED.md` placeholder with hash/size/provenance/recovery URLs, and leaves a stand-in symlink. `--dry-run` and `--verify` modes |
| [`audit_archive.py`](audit_archive.py) | Sweeps the tree for archived artifacts whose placeholder, target or hash has drifted |
| [`link_archived.py`](link_archived.py) | Repairs / creates the stand-in symlinks into `archive/` |
| [`dedupe_shared_assets.py`](dedupe_shared_assets.py), [`dedupe_pointer.py`](dedupe_pointer.py) | Find byte-identical duplicates across the tree and route them through `shared-assets/` |

> ⚠ `archive_artifact.py` **will not protect you from archiving a directory that already has an
> archived child.** Its collision guard compares the *same* path, and a nested earlier entry is
> not the same path — it is silently replaced, orphaning the child's placeholder. This has
> happened. **Check for `*.ARCHIVED.md` beneath a directory before archiving the directory.**
> Worked example: [`devices/zerowriter/zerowriter-ink/source-snapshot-provenance.md`](../devices/zerowriter/zerowriter-ink/source-snapshot-provenance.md).

## EDA and schematic extraction

| Script | Input | Output |
|---|---|---|
| [`kicad_netlist.py`](kicad_netlist.py), [`kicad_pcb_nets.py`](kicad_pcb_nets.py), [`parse_kicad_sch.py`](parse_kicad_sch.py) | KiCad `.kicad_sch` / `.kicad_pcb` | nets, pin tables, footprint census |
| [`eagle_netlist.py`](eagle_netlist.py) | EAGLE `.sch` | nets |
| [`altium_pdf_netlist.py`](altium_pdf_netlist.py), [`altium_pdf_pin_table.py`](altium_pdf_pin_table.py), [`altium_pdf_trace.py`](altium_pdf_trace.py), [`altium_pdf_bind_nets.py`](altium_pdf_bind_nets.py), [`altium_pdf_reflow.py`](altium_pdf_reflow.py), [`altium_pdf_render_sheet.py`](altium_pdf_render_sheet.py) | Altium-exported schematic PDFs | designators, pins, nets, rendered sheets |

## PDF text extraction *(promoted from `archive/devices/lilygo/t-display-s3-shared/artifacts/` 2026-09-20)*

Written because that session's host had **no `pdftotext`, `pdftoppm`, `qpdf`, `mutool`, and no
`pip` to install `pypdf`**. They remain useful anywhere those are unavailable, and
`pdfcid.py` handles a case `pdftotext` gets silently wrong.

| Script | Use it when |
|---|---|
| [`pdftext.py`](pdftext.py) | General case. FlateDecode content streams, `Tj`/`TJ`/`'`/`"` operators, one line per text-showing op with page and approximate `x,y` from `Tm`/`Td` |
| [`pdfall.py`](pdfall.py) | The text is **missing** from `pdftext.py`'s output. Walks *all* streams including **Form XObjects** and groups on `BT…ET`. Altium puts the sheet body in a Form XObject, so reading `/Contents` alone returns pin markers and **zero labels** |
| [`pdfcid.py`](pdfcid.py) | The PDF uses **Type0 / Identity-H** fonts. Decodes via the `/ToUnicode` CMap |

> ⚠ **Validate extracted text against a rendered page or a known heading before transcribing any
> value.** `pdfcid.py` run on `CO5300_V0.01.pdf` returned `FOD300 … FHHPONE TecOnology` — a
> uniform `+0x1D` code-point offset producing output that is **human-legible and wrong**. The
> correct reading is *CO5300 … CHIPONE Technology*. This is the most dangerous PDF failure mode
> because nothing looks broken.

## Firmware images

| Script | Use it when |
|---|---|
| [`esp_image_info.py`](esp_image_info.py) | You have a **bare ESP application image** — magic `0xE9` at offset 0, `esp_app_desc_t` at `0x20` — or a standalone partition table. Prints chip ID, flash mode/size/frequency, entry point, project name, IDF version, build date, ELF SHA-256 |
| [`appdesc.py`](appdesc.py) *(promoted 2026-09-20)* | You have a **merged / full-flash image**. `esp_image_info.py` looks only at `0x20` and finds nothing, because in a merged image the bootloader is at `0x0`, the **partition table at `0x8000`** and the **app at `0x10000`**. `appdesc.py` scans the whole file for the `0xABCD5432` descriptor magic — finding *every* app slot, so it reports `app0` and `app1` separately — and decodes the partition table at `0x8000` |

**Use both.** They answer different questions and neither supersedes the other.

## Type checking and acquisition

| Script | What it does |
|---|---|
| [`magic.py`](magic.py) *(promoted 2026-09-20)* | Magic-byte type check + SHA-256 + size for a list of files. Recognises PDF, ZIP, PNG, JPEG, 7z, XZ, gzip, **STEP (`ISO-10303-21`)**, DWG, ASCII STL, HTML and XML. **A `file(1)` substitute for hosts that lack it** — and the routine guard against the classic failure of saving an HTML error page under a `.pdf` or `.bin` extension |
| [`diff_vendored_lib.py`](diff_vendored_lib.py) | Compare a vendored dependency against upstream and emit the delta as a patch |
| [`extract_showcase.py`](extract_showcase.py) | Pull structured data out of vendor showcase pages |

## Conventions

- **Standard library only.** No script here may require `pip install`.
- **Print, don't write.** Extraction scripts write to stdout; the caller decides where output goes.
- **Never trust an extension.** Run `magic.py` on anything downloaded before filing it.
- **Label the evidence.** Output of these scripts is `executed-success` for *what the bytes say*;
  it is not evidence of hardware behaviour.
