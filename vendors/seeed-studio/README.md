# Seeed Studio — documentation sourcing guide

Reusable patterns for obtaining official Seeed material. Established **2026-08-24** during research on the [XIAO ESP32S3 Sense](../../devices/seeed-studio/xiao-esp32s3-sense/README.md); every technique below was live-verified on that date, with negative controls where noted.

## 1. The single most important finding: the wiki is a GitHub repo

**Do not scrape `wiki.seeedstudio.com`.** It is a Docusaurus SPA behind Cloudflare. A plain fetch of a wiki page returns ~150 KB of HTML containing **exactly one `href`** — a Cloudflare email-protection link. All documentation text and every download link are injected client-side.

*Negative control, 2026-08-24:* `curl -A '<Chrome UA>' https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/` → HTTP 200, 150,703 bytes, `1` link, zero `.pdf`/`.zip` URLs. A browser User-Agent does **not** help; the problem is rendering, not blocking.

The wiki source is public Markdown:

| Field | Value |
|---|---|
| Repository | `Seeed-Studio/wiki-documents` |
| **Branch** | **`docusaurus-version`** |
| Path template | `sites/<lang>/docs/<Category>/<Family>/<Product>/<Page>.md` |
| Languages | `en`, `zh-CN`, `ja`, `pt-BR` |
| Raw URL | `https://raw.githubusercontent.com/Seeed-Studio/wiki-documents/docusaurus-version/<path>` |

**Branch traps (verified 2026-08-24):**

| Branch | Tree API result |
|---|---|
| `main` | **HTTP 404 — does not exist** |
| `master` | HTTP 200, but only **1,366** entries and **zero** XIAO ESP32S3 matches — a different, near-empty tree |
| **`docusaurus-version`** | HTTP 200, **16,372** entries — the real content |

Enumerate everything for a product in one request:

```bash
curl -fsSL "https://api.github.com/repos/Seeed-Studio/wiki-documents/git/trees/docusaurus-version?recursive=1" \
| python3 -c "import json,sys;[print(t['path']) for t in json.load(sys.stdin)['tree'] if 'XIAO_ESP32S3' in t['path']]"
```

This returned **300 matching paths** (230 Markdown files after filtering) for the XIAO ESP32S3 family. Then fetch each with `raw.githubusercontent.com`, percent-encoding paths (many contain spaces, `&` and non-ASCII).

**Why this is worth the trouble:** the Markdown contains every `files.seeedstudio.com` artifact URL in plain text. Extracting URLs from the 230 files yielded **68 artifact links** (PDF/ZIP/DXF/XLSX/RAR/STEP) and **75 GitHub project links** — none of which are visible to a naive fetch of the rendered page.

## 2. Artifact hosting — `files.seeedstudio.com`

Static, no authentication, no User-Agent requirement. Observed path templates:

```
https://files.seeedstudio.com/wiki/<Product-Slug>/res/<file>          # older assets
https://files.seeedstudio.com/wiki/<Product-Slug>/new-res/<file>      # newer revisions
https://files.seeedstudio.com/wiki/<Product-Slug>/img/<file>          # images, some zips
https://files.seeedstudio.com/products/<SKU-or-family>/<file>         # product-scoped
https://files.seeedstudio.com/wiki/XIAO-KiCad-Library/<file>          # family-wide EDA libs
```

`res/` vs `new-res/` matters: when Seeed re-releases a design, the new file lands in `new-res/` and the old one **stays** in `res/`. Both remain live. Always check for a `new-res/` variant.

Filename conventions:

- `<InternalDocID>_<Product>_v<X.Y>_SCH_<YYMMDD>.pdf` — e.g. `202003753_XIAO ESP32S3 Sense_v1.5_SCH_260226.pdf`
- `<InternalDocID>_..._SCH&PCB_<YYMMDD>.zip` — the EDA source package
- Dates are **`YYMMDD`**
- **Double extensions occur** (`..._SCH_260226.pdf.pdf`) and are genuine

## 3. Known vendor data errors

Check for these on any Seeed product:

**Crossed document IDs.** For the XIAO ESP32S3, document `202003751` (advertised as the *non-Sense* v1.4 schematic) serves a file **byte-identical** to `202003753` (Sense v1.5). Both the PDF and the `SCH&PCB` ZIP are identical; unzipping the "v1.4" archive produces a directory named `..._Sense_v1.5_...`. The wiki's own Resources section links the wrong file. **Verify a schematic's title block matches the product you asked for.**

**Filename revision ≠ design revision.** The same package is published as "v1.5" while its title block, footprint library and revision-history sheet all say **v1.3**, and no v1.4/v1.5 entry exists in the revision history. Trust the **title block and revision-history sheet**, not the filename.

**Repackaged firmware with unchanged binaries.** `XIAO-ESP32S3-Sense-firmware-20240814.zip` contains binaries byte-identical to the earlier undated release; only the flashing wrapper changed. The application inside was built 2023-02-08. **Hash the binaries before assuming a dated release is newer.**

**Internal contradictions in spec tables.** Seeed published **three** mutually inconsistent low-power figures for one board (3 mA, 33.51 µA, 26.5 mA) across the wiki and the reference-design catalogue.

## 4. The reference-design catalogue is a project index, not a design guide

`https://files.seeedstudio.com/wiki/XIAO/XIAO-Reference-Design.pdf` (49.9 MB, 129 pages, published 2025-11-15) sounds like a hardware design guide. Pages 8–13 are family comparison tables; **pages 14–129 are a curated project showcase**, one project per page.

Two extraction traps:

1. **Project URLs are link annotations, not text.** They live in each page's `/Annots` array and are invisible to text extraction. 116 of 117 entries have one.
2. **InDesign kerning scatters spaces inside words** (`W e ar ables`, `X IA O ESP 3 2 - S 3`). Text extraction is unusable until re-joined. A workable approach: build a vocabulary from the pages that are *not* kerned, then greedily re-merge short token runs that reconstruct a known word.

Working extractor: [`../../devices/seeed-studio/xiao-esp32s3-sense/tools/extract_showcase.py`](../../tools/extract_showcase.py).

The comparison tables on pages 9–12 are the most compact cross-XIAO spec source that exists, and each cell links to the product page with an `?utm_source=Seeedblog` suffix.

## 5. EDA source formats by era

Seeed migrated EDA tools mid-life for the XIAO line:

| Era | Tool | Schematic format | Text extractable from PDF? |
|---|---|---|---|
| 2023 (v1.0–v1.2) | **EAGLE 9.6.2** (PDF via Qt 5.9.4) | `.sch` / `.brd` — **XML, parseable** | ❌ **No** — text is rendered as vector paths |
| 2025–2026 (v1.3+) | **KiCad 9** | `.kicad_sch` / `.kicad_pcb` — s-expressions | ✅ Yes |

**For KiCad packages, parse `.kicad_pcb` rather than `.kicad_sch` for connectivity.** KiCad schematics store no netlist — nets are implied by wire geometry — but the PCB file stores **resolved net names per pad**, which is ground truth. This is how the otherwise-undocumented board-to-board connector pinout was recovered. Tools: [`kicad_pcb_nets.py`](../../tools/kicad_pcb_nets.py), [`kicad_netlist.py`](../../tools/kicad_netlist.py).

For EAGLE-era boards, the PDF is useless but the `.sch` XML inside the `SCH&PCB` ZIP is fully parseable.

## 6. Licensing observations

- **Schematics and PCB design files are CC BY-SA 4.0**, indicated by a `Misc:LOGO_CC_BY-SA_4.0` footprint on every sheet. This is unusually permissive and makes derived documentation publishable with attribution.
- **Support downloads carry no stated terms** — firmware bundles, 3D models, DXF outlines, pinout spreadsheets.
- **Third-party datasheets rehosted by Seeed keep their original restrictions.** Seeed mirrors OmniVision OV3660/OV5640 datasheets that explicitly state *"Individuals and/or organizations are not allowed to re-distribute said information."* Rehosting by a vendor does not relicense them.
- Product-page and wiki prose is marketing copy; the wiki repo itself is open-source.

## 7. Per-product checklist

1. Enumerate wiki Markdown via the `docusaurus-version` tree API; grep for the product name and SKU.
2. Extract every `files.seeedstudio.com` URL from those Markdown files.
3. For each schematic, check for **both** `res/` and `new-res/` variants.
4. Download and **hash everything**; look for byte-identical files under different names.
5. Open each schematic PDF and confirm the **title block** names the product you expected.
6. If KiCad, parse `.kicad_pcb` for the authoritative netlist.
7. If EAGLE, parse the `.sch` XML — do not rely on the PDF.
8. Check the family reference-design catalogue for showcase projects and comparison tables.
9. Cross-check the Espressif/vendor board variant (`arduino-esp32 variants/<BOARD>/pins_arduino.h`) against the schematic.
10. Record contradictions rather than picking a value.

## 8. Products documented with this guide

- [XIAO ESP32S3 Sense](../../devices/seeed-studio/xiao-esp32s3-sense/README.md) — the pass that produced these findings

## 9. Change log

| Date | Change |
|---|---|
| 2026-08-24 | Guide created. Established the `docusaurus-version` branch requirement (with `main`/`master` negative controls), the `res/` vs `new-res/` split, the crossed-document-ID error, the filename-vs-title-block revision conflict, the EAGLE→KiCad migration and its extraction consequences, the `/Annots` link-extraction technique for the reference catalogue, and the CC BY-SA 4.0 status of design files. |
