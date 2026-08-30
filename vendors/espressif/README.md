# Espressif Systems — documentation sourcing guide

Reusable, cross-device knowledge for obtaining official Espressif documentation for **any** Espressif chip, module or board. Written and verified 2026-08-21/2026-08-22 while researching the [ESP32-S3R8](../../components/espressif/esp32-s3r8/README.md) and [ESP32-U4WDH](../../components/espressif/esp32-u4wdh/README.md) on the [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md).

Every URL pattern and every claim about what does and does not resolve in this document was checked live with `curl` on the dates given. Where behaviour is stated as "404" or "redirects", that is an observed HTTP result, not an assumption.

---

## 1. The four hosts

Espressif documentation is spread across four hosts with different purposes and different lifecycles. Knowing which host owns a document class is most of the battle.

| Host | Owns | Stability |
|---|---|---|
| `www.espressif.com/sites/default/files/documentation/` | **Legacy** static PDF store: datasheets, technical reference manuals, module datasheets. | Path still works for datasheets/TRMs, but only as an HTTP redirect into `documentation.espressif.com`. Several document classes have been *removed* from it. |
| `documentation.espressif.com` | Current static-document platform and PCN/certification portal. Redirect target of the legacy path. | Serves real PDFs; also serves a **soft-404 SPA shell** for anything missing (see §5). |
| `docs.espressif.com/projects/<project>/` | **esp-docs** generated documentation: programming guides, errata, hardware design guidelines, framework docs. Versioned and often per-target. | The authoritative home of anything that is continuously updated. |
| `dl.espressif.com` | Binaries, toolchains, tool installers, prebuilt firmware, GitHub release mirrors — **and, contrary to what this table said before 2026-08-21, the primary store for development-board schematics, PCB layouts, dimension drawings, assembly drawings and mirrored third-party component datasheets.** See §2.4. | Mixed. The `/dl/`, `/schematics/` and `/AE/` prefixes behave differently and are not interchangeable. Returns a genuine HTTP 404 (a few hundred bytes of plain HTML) for missing files, which makes it *easier* to probe than `documentation.espressif.com`. |

Source code, issue trackers and in-repo Markdown/RST documentation live at `github.com/espressif/<project>`. When an esp-docs project publishes no PDF (see §4), the GitHub repository is the fallback primary source.

---

## 2. URL templates

### 2.1 Legacy static PDF store

```
https://www.espressif.com/sites/default/files/documentation/<doc>_<lang>.pdf
```

`<lang>` is `en` or `cn`. `<doc>` uses **underscores** for word separation but keeps the chip's own hyphens, e.g. `esp32-s3_technical_reference_manual`.

Verified working (2026-08-22), each returning `200 application/pdf` after a redirect to `documentation.espressif.com/<doc>_<lang>.pdf`:

| URL suffix | Bytes |
|---|---:|
| `esp32_datasheet_en.pdf` | 989 523 |
| `esp32-s3_datasheet_en.pdf` | 1 098 115 |
| `esp32-s3_datasheet_cn.pdf` | 1 635 642 |
| `esp32_technical_reference_manual_en.pdf` | 10 173 126 |
| `esp32-s3_technical_reference_manual_en.pdf` | 15 215 232 |
| `esp32-s3_technical_reference_manual_cn.pdf` | 15 429 955 |
| `esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.pdf` | 1 230 114 |
| `esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf` | 1 280 501 |
| `esp32-s3-wroom-2_datasheet_en.pdf` | 700 361 |
| `esp32-s3-mini-1_mini-1u_datasheet_en.pdf` | 1 338 916 |

So: **chip datasheets, chip TRMs and module datasheets are still served from the legacy path.** Nothing else reliably is.

### 2.2 esp-docs projects

Two shapes, depending on whether the project is target-aware.

Target-aware (chip-specific content):

```
https://docs.espressif.com/projects/<project>/en/<version>/<target>/<project>-en-<version>-<target>.pdf
```

Target-agnostic:

```
https://docs.espressif.com/projects/<project>/en/<version>/<project>-en-<version>.pdf
```

Three independent variables, and **all three must be right or you get a 404**:

- `<project>` — the esp-docs project slug (§3).
- `<version>` — the URL version segment: `latest`, `stable`, or a tag such as `v5.1.4`.
- the **filename version slug** — *not necessarily the same string as `<version>`*. This is the trap. For a tagged build the slug equals the tag (`v5.1.4`). For a `latest` build the slug is whatever branch the build came from, usually `master`, but sometimes literally `latest`. Verified divergence:

  | Project | URL version segment | Filename slug |
  |---|---|---|
  | `esp-chip-errata` | `latest` | `master` |
  | `esp-hardware-design-guidelines` | `latest` | `master` |
  | `esp-iot-solution` | `latest` | `master` |
  | `esp-adf` | `latest` | `master` |
  | `esp-matter` | `latest` | `master` |
  | `esp-at` | `latest` | **`latest`** |
  | `esp-idf` | `v5.1.4` | `v5.1.4` |

  There is no way to derive this. Resolve it empirically per §6.2.

- `<target>` — lowercase, no hyphen: `esp32`, `esp32s2`, `esp32s3`, `esp32c3`, `esp32c6`, `esp32h2`, `esp32p4`. Note this differs from the legacy-path spelling, which *does* use a hyphen (`esp32-s3_datasheet_en.pdf` vs `.../esp32s3/...`).

### 2.3 Other

```
https://documentation.espressif.com/en/<PCN-title>.html      # product change notices, HTML
https://github.com/espressif/<project>                        # source and in-repo docs
```

### 2.4 `dl.espressif.com` — development-board design files

**Added 2026-08-21 while researching the ESP32-P4 boards. This corrects §1, which previously asserted that `dl.espressif.com` served no documentation.** It serves a great deal, under **three unrelated path prefixes**, none of which redirects to the others. There is no directory listing on any of them; filenames must be harvested from the `esp-dev-kits` user guides.

| Prefix | Contains | Verified examples (2026-08-21) |
|---|---|---|
| `/dl/schematics/` | Main-board and sub-board schematics, PCB layouts, dimension PDFs and DXFs, assembly drawings, and mirrored **third-party** component datasheets (panels, cameras, display driver ICs, FPC connectors) | `esp32-p4-function-ev-board-schematics_v1.52.pdf` (817 278 B), `esp32-p4-function-ev-board-pcb-layout.pdf` (1 808 476 B), `esp32-p4-function-ev-board-dimensions.dxf` (3 879 854 B), `display_driver_chip_EK79007AD_datasheet.pdf` (3 723 767 B), `1.0K-GT-15PB_specification.pdf` (1 257 112 B) |
| `/schematics/` | Newer boards' design files, and **complete reference-design ZIPs** for adapter/sub-boards containing EDA source, Gerbers, BOM and assembly | `ESP32_P4X_C5_Function_EV_board-2.0-schematics.pdf` (789 023 B), `…-2.0-dimensions.dxf` (3 790 900 B), `LCDAdapterBoardReferenceDesign.zip` (1 276 237 B), `CameraAdapterBoardReferenceDesign.zip` (1 349 188 B) |
| `/AE/esp-dev-kits/` | Per-board manufacturer documents, frequently under **Chinese filenames** | `SCH_ESP32-P4-EYE-MB_V2.3_20250416.pdf` (748 835 B), `PCB_ESP32-P4-EYE-MB_V2.2_20250314.pdf` (1 371 064 B), `ST7789VW芯片手册.pdf` (3 135 599 B), `胶铁一体ZJY154KC-IF17.pdf` (1 290 995 B) |

Practical rules:

- **Filename conventions differ per prefix.** `/dl/schematics/` uses lowercase-hyphen with `_vX.YZ` version suffixes; `/schematics/` uses `Mixed_Underscore_Case` with `-M.N-` version infixes; `/AE/esp-dev-kits/` uses `SCH_`/`PCB_` prefixes with `_VX.Y_YYYYMMDD`. **Do not extrapolate a filename from one prefix to another** — every cross-prefix guess tried during the P4 pass returned 404.
- **Percent-encode Chinese filenames and do not translate them.** Same rule as for PCNs (§6.3).
- **Version numbers are baked into filenames.** When Espressif ships a new board revision the old URL keeps working and simply becomes stale. Re-derive URLs from the current user guide rather than reusing a recorded one.
- **Filenames outlive board names.** The sub-board PDFs named `esp32-p4-function-ev-board-*` are still linked from the *successor* `ESP32-P4X-*` user guides. A filename is not evidence of which board a document applies to.
- DXF files are ASCII AutoCAD drawing-exchange; validate them by their `  0`/`SECTION` header, **not** by `%PDF`.

### 2.5 `esp-dev-kits` — where board documentation actually lives

```
https://docs.espressif.com/projects/esp-dev-kits/en/<version>/<target>/                        # per-target board index
https://docs.espressif.com/projects/esp-dev-kits/en/<version>/<target>/<board-slug>/index.html
https://docs.espressif.com/projects/esp-dev-kits/en/<version>/<target>/<board-slug>/user_guide.html
https://docs.espressif.com/projects/esp-dev-kits/en/<version>/<target>/eol/eol-boards.html     # EOL index
https://docs.espressif.com/projects/esp-dev-kits/en/<version>/<target>/eol/<board-slug>/user_guide.html
https://docs.espressif.com/projects/esp-dev-kits/en/<version>/<target>/esp-dev-kits-en-master-<target>.pdf
```

Five things to know:

1. **It is target-aware and the bare path redirects to `esp32`.** `…/esp-dev-kits/en/latest/` silently becomes `…/en/latest/esp32/`. Ask for `esp32p4`, `esp32s3` etc. explicitly or you will enumerate the wrong board list.
2. **The per-target PDF build contains every board's user guide for that target, current *and* EOL, in one file.** For ESP32-P4 that is 30 482 003 B. This is by far the most efficient single artifact to retain for a board family.
3. **It uses the older server-rendered esp-docs theme**, so unlike `esp-dsp` you *can* enumerate boards and download links by scraping `href` attributes. This is the fastest reliable way to discover a family's boards:
   ```bash
   curl -sSL 'https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/' \
     | grep -oE 'href="[a-z0-9./-]+/index.html"' | sort -u
   ```
4. **EOL boards are not deleted, they are moved** under `<target>/eol/<board-slug>/`. A board vanishing from the target index does *not* mean its documentation is gone — and the EOL guide frequently retains design-file links that the successor's guide has dropped. **Always check the EOL index when a current board's design files are missing.**
5. **The authoritative list of board slugs, including ones not yet published,** is the repository's docs directory:
   ```bash
   curl -sSL 'https://api.github.com/repos/espressif/esp-dev-kits/contents/docs/en' \
     | grep -oE '"name": "[^"]+"'
   ```
   Every rendered user guide also carries an "Edit on GitHub" link containing the **exact source commit**, e.g. `github.com/espressif/esp-dev-kits/blob/f6f80ab/docs/en/<slug>/index.rst` — use that as your immutable revision identifier.

### 2.6 Board reference-design ZIPs — a known-broken link class

`esp-dev-kits` user guides for the current ESP32-P4 boards link a *"Reference Design (ZIP)"* at:

```
https://documentation.espressif.com/<Board-Name>-EN.zip
```

**As of 2026-08-21 none of these resolve.** They return the standard 13 745-byte soft-404 SPA shell (§5.1) with HTTP 200. Verified dead for `ESP32-P4X-Function-EV-Board-EN.zip`, `ESP32-P4X-EYE-EN.zip`, `ESP32-P4-Function-EV-Board-EN.zip`, `ESP32-P4-EYE-EN.zip` and `ESP32-P4X-C5-Function-EV-Board-EN.zip`, in `-EN`/`-CN`, upper/lowercase and `_EN` variants, on `documentation.espressif.com`, `documentation.espressif.com/en/`, the legacy `www.espressif.com` path and both `dl.espressif.com` schematic prefixes. Loading the URL in a real browser produces an empty body and issues no XHR, so it is not an SPA-gated download either.

Recovery strategy, in order:

1. **Check the EOL predecessor's user guide.** It very often publishes the individual schematic/PCB/dimension PDFs that the current guide replaced with the dead ZIP. This worked for both P4 board families.
2. Check whether the *sub-boards* have their own reference-design ZIPs under `dl.espressif.com/schematics/` — those do resolve, and are more complete (EDA source + Gerbers + BOM) than anything published for main boards.
3. Failing both, Espressif's own instruction applies: "For further design documentation for the board, please contact us at sales@espressif.com."

When you substitute a predecessor's schematic for a current board's, **say so explicitly in the record.** "Espressif describes the difference as a chip-revision change" is a weaker claim than "the schematics are identical", and conflating them is exactly the kind of silent error this guide exists to prevent.

---

## 3. Known esp-docs projects — verified status

Checked 2026-08-22. "PDF" means a PDF build was confirmed by downloading it and checking `%PDF` magic.

| Project | Target-aware | PDF build? | Verified PDF URL / notes |
|---|---|---|---|
| `esp-idf` | yes | **yes, up to v5.3.2 only** | `…/esp-idf/en/v5.1.4/esp32s3/esp-idf-en-v5.1.4-esp32s3.pdf`. See §4. |
| `esp-dev-kits` | yes | yes | `…/esp-dev-kits/en/latest/esp32p4/esp-dev-kits-en-master-esp32p4.pdf` (30 482 003 B). Server-rendered theme, so scrapable. **The home of every official development-board user guide.** See §2.5. |
| `esp-chip-errata` | yes | yes | `…/esp-chip-errata/en/latest/esp32s3/esp-chip-errata-en-master-esp32s3.pdf` |
| `esp-hardware-design-guidelines` | yes | yes | `…/esp-hardware-design-guidelines/en/latest/esp32/esp-hardware-design-guidelines-en-master-esp32.pdf` |
| `esp-iot-solution` | no | yes | `…/esp-iot-solution/en/latest/esp-iot-solution-en-master.pdf` (26 148 298 B) |
| `esp-adf` | no | yes | `…/esp-adf/en/latest/esp-adf-en-master.pdf` (25 732 191 B) |
| `esp-matter` | yes | yes | `…/esp-matter/en/latest/esp32/esp-matter-en-master-esp32.pdf` (1 524 159 B) |
| `esp-at` | yes | yes | `…/esp-at/en/latest/esp32/esp-at-en-latest-esp32.pdf` (9 436 168 B) — note `latest`, not `master` |
| `esp-dsp` | yes | **no** | HTML site exists at `…/esp-dsp/en/latest/esp32/`; all PDF name permutations 404. Use GitHub. |
| `esptool` | yes | **no** | HTML only at `…/esptool/en/latest/esp32/`. |
| `arduino-esp32` | no | **no** | HTML only at `…/arduino-esp32/en/latest/`. |
| `esp-rainmaker` | yes | **no** | HTML only at `…/esp-rainmaker/en/latest/esp32/`. Slug is `esp-rainmaker`, **not** `rainmaker` — `/projects/rainmaker/` 404s. |
| `esp-box` | — | **no** | `/projects/esp-box/en/latest/` returns 404. Documentation lives in the GitHub repo. |
| `esp-protocols` | — | **no** | `/projects/esp-protocols/en/latest/` returns 404; per-component docs are published under separate slugs. |
| `esp-serial-flasher` | — | **no** | `/projects/esp-serial-flasher/en/latest/` returns 404. GitHub only. |
| `esp-insights` | — | **no** | `/projects/esp-insights/en/latest/` returns 404. GitHub only. |

**Rule of thumb:** an esp-docs project having a browsable HTML site does *not* imply a PDF build. PDF generation is opted into per project.

---

## 4. IMPORTANT FINDING — documents that migrated off the legacy path

This is the single most valuable thing in this guide, because it silently breaks the obvious URL pattern.

**Errata and hardware design guidelines are no longer published as legacy static PDFs.** They were migrated into versioned esp-docs projects. The legacy URLs you will find cited in older application notes, forum posts and third-party board documentation do not 404 in a way that is easy to notice — they **HTTP-redirect to an HTML index page**:

```
https://www.espressif.com/sites/default/files/documentation/esp32_errata_en.pdf
  -> 200 text/html, 15900 B
  -> https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/index.html

https://www.espressif.com/sites/default/files/documentation/esp32-s3_hardware_design_guidelines_en.pdf
  -> 200 text/html, 15510 B
  -> https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/index.html
```

A naive `curl -o esp32_errata_en.pdf` therefore **succeeds with HTTP 200 and writes an HTML page into a `.pdf` file.** Nothing warns you. This is precisely why every download must be magic-byte validated (§5.3).

### How to detect it

The redirect is the tell. Ask for the effective URL:

```bash
curl -sSLI -o /dev/null -w '%{http_code} %{content_type} %{url_effective}\n' \
  https://www.espressif.com/sites/default/files/documentation/esp32_errata_en.pdf
```

Three distinguishable outcomes:

| `url_effective` ends in | Meaning | Recovery |
|---|---|---|
| `documentation.espressif.com/<same-name>.pdf`, `content_type: application/pdf` | Document still lives on the legacy path. | Nothing to do. |
| `docs.espressif.com/projects/<project>/…/index.html` | **Migrated to esp-docs.** The redirect target *names the project and target for you*. | Build the esp-docs PDF URL from that path (below). |
| `documentation.espressif.com/404`, `content_type: text/html`, exactly **13 745 bytes** | Soft 404 — no such document anywhere on the static platform. | Search esp-docs and GitHub; the document may not exist at all. |

### How to recover

The redirect hands you `<project>` and `<target>` directly. Rewrite `index.html` into the PDF build name and resolve the filename slug per §6.2:

```
docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/index.html
                            └── project ──┘        └tgt┘
->  docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/esp-chip-errata-en-master-esp32.pdf
```

### The same class of breakage inside esp-docs: dropped PDF builds

ESP-IDF **stopped producing PDF builds after v5.3.2**. Verified 2026-08-22 and re-verified with a wider probe on 2026-08-21 for the `esp32p4` target:

| Version | PDF (esp32 target) | PDF (esp32p4 target) |
|---|---|---|
| v4.4.8 | yes, 34 872 788 B | n/a — no P4 target before v5.3 |
| v5.0.9 | yes, 32 028 087 B | n/a |
| v5.1.4 | yes, 37 852 819 B | n/a |
| v5.1.6 | yes, 32 937 951 B | n/a |
| v5.2.5 | yes, 30 789 611 B | yes, 11 767 843 B |
| v5.3 | **yes** | **yes**, 13 297 191 B |
| v5.3.1 | — (not probed) | **yes** |
| v5.3.2 | — (not probed) | **yes**, 13 656 675 B |
| v5.3.3 | **no — 404** | **no — 404** |
| v5.4, v5.4.1, v5.4.2 | **no — 404** | **no — 404** |
| v5.5, v5.5.1 | **no — 404** | **no — 404** |

> **Correction, 2026-08-21.** An earlier edition of this guide stated the cutoff was "after the v5.2 series", based on a probe that jumped from v5.2.5 straight to v5.3.3. That was wrong: **v5.3, v5.3.1 and v5.3.2 all publish PDFs.** The real boundary is between **v5.3.2 and v5.3.3**. Probe consecutive patch releases, not just minor versions — the 2026-08-22 record in [`component-download-failures.txt`](../../component-download-failures.txt) understated the newest available manual by three releases. Its "v5.2.5 is the newest PDF that exists" line stands corrected here.

Interestingly, a `v5.2.5` PDF exists for the `esp32p4` target even though Espressif's own chip-support matrix says P4 support began in v5.3. Treat pre-v5.3 P4 documentation as preview material and do not rely on it.

So if you need an offline ESP-IDF manual for a project pinned to v5.4 or newer, **the closest available PDF is v5.3.2**, and you must note the version skew explicitly rather than pretending the PDF matches. For an exact match on v5.3.3+ you must build the docs yourself from `github.com/espressif/esp-idf/tree/<tag>/docs` or archive the HTML.

Also beware `v5.4` vs `v5.4.0`: the former is a real docs version that exists (its 404 page is the site's own 13 818-byte shell), the latter is not a docs version at all (a different, 7 805-byte 404). Do not infer version existence from 404 size alone — but differing 404 bodies are a useful hint that you are querying two different layers.

---

## 5. Gotchas

### 5.1 SPA shells and soft 404s

`documentation.espressif.com` returns **HTTP 200** with an HTML application shell for missing documents. Fingerprint observed consistently on 2026-08-22: `200 text/html`, exactly **13 745 bytes**, final URL `https://documentation.espressif.com/404`. Treat that byte count as a strong soft-404 signal for this host, but do not rely on it alone — it will change when the site is rebuilt. The reliable test is always the magic bytes.

Some esp-docs landing pages are also JS-rendered: `docs.espressif.com/projects/esp-dsp/en/latest/esp32/` returns a 7 682-byte shell containing no document links at all. **You cannot enumerate a project's PDFs by scraping its landing page** unless the project uses the older server-rendered theme (which `esp-iot-solution`, `esp-adf`, `esp-matter` and `esp-at` do — for those, grepping `href="…\.pdf"` works and is the fastest way to learn the filename slug).

### 5.2 Redirects and aliases

- Always use `curl -L`. The legacy path is redirect-only.
- `…/en/latest/` on a target-aware project **redirects to a default target**, e.g. `/projects/esp-dsp/en/latest/` → `/projects/esp-dsp/en/latest/esp32/`. If you scrape the redirected page you are looking at ESP32 content while believing you asked for something generic.
- `latest` and `stable` are moving aliases. `latest` tracks `master` and can change daily; its PDF has no cover version number at all. **Pin an explicit version tag whenever one exists.** When you must use `latest` (errata and hardware design guidelines have no tagged releases), pin the artifact by SHA-256 and retrieval date instead, and say so in the record.
- Documents move between versions. A section present in v5.1 may be relocated or deleted by v5.3; cite the version you actually read.

### 5.3 Always validate

Never trust HTTP 200. Validate every downloaded file:

```bash
[ "$(head -c 4 file.pdf)" = "%PDF" ] || { echo "NOT A PDF"; exit 1; }
```

Then sanity-check: size plausible for the document class (chip datasheet ~1 MB, TRM 10–16 MB, programming guide 25–40 MB; anything under ~50 KB is almost certainly an error page), and a `%%EOF` trailer present:

```bash
tail -c 32 file.pdf | strings | grep -q EOF
```

Saving an HTML error page under a `.pdf` filename is the failure mode this whole section exists to prevent. If a document cannot be obtained as a real PDF, record the attempt in [`component-download-failures.txt`](../../component-download-failures.txt) rather than storing a fake.

### 5.4 Language variants

Chinese editions exist for most legacy documents (`_cn.pdf`) and are sometimes **newer** than the English edition. If a datasheet fact looks stale, checking the `_cn` revision date is a legitimate cross-check. Do not store both unless the divergence matters.

Separately, and unrelated to *editions*: some documents on `dl.espressif.com` have **Chinese filenames** even though their content is relevant to English users. Percent-encode and fetch them verbatim; do not translate the filename. See §2.4 and §6.3.

### 5.5 Obfuscated PDF text layers, and how to read a datasheet anyway

Several Espressif PDFs ship deliberately unreadable text layers, and there is more than one scheme (PCNs use a uniform +29 code-point offset; the ESP32 and ESP32-P4 datasheets use non-uniform glyph-subset maps that no offset recovers). The historic fix recorded here was "fetch `documentation.espressif.com/<slug>.html` instead, which serves clean extractable text."

**That fix stopped working when the platform became a Vue SPA.** As of 2026-08-21, `https://documentation.espressif.com/<slug>.html` returns a ~200 KB HTML shell whose `<title>` is correct but whose body contains **zero document text**; the content is fetched client-side. Plain `curl` yields nothing usable, and the API base (`/api`) does not expose a guessable document endpoint.

What does work is rendering the page in a real browser and reading `document.body.innerText`:

```javascript
// via any CDP/Playwright/Puppeteer-style driver
await navigate("https://documentation.espressif.com/esp32-p4_datasheet_en.html");
await sleep(15000);                       // the viewer is slow; 6 s is not enough
await evaluate("() => document.body.innerText.length");        // e.g. 196767
await evaluate("() => document.body.innerText.slice(0,40000)"); // page in chunks
```

Two limits to be aware of:

- **The viewer lazy-loads.** A cold render gives you the table of contents, cover, product overview and the first few pages of body text — not the whole document. For the ESP32-P4 datasheet that was enough for the nomenclature, part numbers, package, memory sizes and Features list, but **not** for the pin tables, electrical characteristics or packaging sections. Those require scripted scrolling, or reading the PDF in a viewer.
- **Extract in slices.** Returning 200 KB through a tool boundary in one call is fragile; 40 000-character slices worked reliably.

If you only need a handful of facts, this is much cheaper than fighting the PDF. If you need pin tables, open the PDF in a real viewer and accept that you cannot grep it.

Corollary for record-keeping: **do not cite a version number you could not actually read.** When a document's cover version is unreadable, pin the artifact by SHA-256 and retrieval date and say the version is untranscribed. The ESP32-P4 TRM in this tree is recorded that way.

---

## 6. How to search

### 6.1 Enumeration checklist for a given chip

Work this list top to bottom for every Espressif part. Each row states where the document actually lives today.

| # | Document class | Where | Notes |
|---|---|---|---|
| 1 | Chip datasheet | legacy path, `<chip>_datasheet_en.pdf` | Always exists. |
| 2 | Technical reference manual | legacy path, `<chip>_technical_reference_manual_en.pdf` | Not published for every part (low-end parts may have datasheet only). Chip-specific instruction-set extensions live **inside** the TRM, not as separate documents — e.g. ESP32-S3 PIE/SIMD is TRM Chapter 1. |
| 3 | **Errata / ECO list** | `esp-chip-errata` esp-docs project | **Migrated — legacy URL redirects to HTML.** §4. Mandatory reading; contains the chip-revision identification procedure. |
| 4 | **Hardware design guidelines** | `esp-hardware-design-guidelines` esp-docs project | **Migrated — legacy URL redirects to HTML.** §4. Supersedes the old per-chip "hardware design guidelines" PDFs. |
| 5 | ESP-IDF programming guide, per target | `esp-idf` esp-docs project | PDF only up to v5.2.x. Pin the version your firmware uses. |
| 6 | ESP-IDF release notes | `github.com/espressif/esp-idf/releases/tag/<tag>` | Not on the docs site. |
| 7 | Module datasheets | legacy path | Only relevant if the board carries a **module**. A bare-die/SiP design (e.g. ESP32-S3R8 soldered directly) does **not** use a WROOM/MINI datasheet; citing one would be wrong. |
| 8 | Product change notices (PCN) | `documentation.espressif.com` | §6.3. Often HTML-only. |
| 9 | Certification documents | `documentation.espressif.com` certification section | FCC/CE/SRRC. Module-level, not chip-level. |
| 10 | Application notes | mixed | Increasingly folded into esp-docs guides rather than standalone PDFs. |
| 11 | Framework/library docs | esp-docs projects, §3 | `esp-adf` audio, `esp-iot-solution` board/peripheral components, `esp-dsp` SIMD kernels (no PDF), `esp-matter`, `esp-at`. |

A part is "exhaustively researched" when every row is either downloaded or recorded as a justified absence.

**Row 7 in practice:** probe the module datasheet slugs even when you expect none, and record the negative. For ESP32-P4, `esp32-p4-mini-1`, `esp32-p4-wroom-1`, `esp32-p4-module` and `esp32-p4-mini-1_mini-1u` all soft-404, and the modules product page lists no P4 part — which is itself a significant engineering finding (there is no pre-certified path; every design integrates the bare QFN die).

### 6.1a Enumeration checklist for an official development board

Chip and board documentation live in different places and have different failure modes. Work this list for any Espressif dev kit.

| # | Document class | Where | Notes |
|---|---|---|---|
| 1 | Board lineup for a chip family | `esp-dev-kits` per-target index, §2.5 | Scrape `href="…/index.html"`. **Also read `<target>/eol/eol-boards.html`** — retired boards keep their guides and often keep design files the successor dropped. |
| 2 | Authoritative slug list, incl. unreleased | GitHub contents API on `esp-dev-kits/docs/en` | §2.5 |
| 3 | User guide (HTML) | `…/<target>/<slug>/user_guide.html` | Server-rendered; scrape it for every download URL. This is the **only** reliable index of a board's design files. |
| 4 | User guide (PDF) | `…/<target>/esp-dev-kits-en-master-<target>.pdf` | One file covers every board for that target. |
| 5 | Schematic, PCB layout, dimensions (PDF + DXF), assembly | `dl.espressif.com`, §2.4 | Published for some boards and not others. Not guessable — take URLs from row 3. |
| 6 | Reference-design ZIP (EDA source + Gerber + BOM) | `documentation.espressif.com/<Board>-EN.zip` for main boards (**currently broken**, §2.6); `dl.espressif.com/schematics/…ReferenceDesign.zip` for adapter/sub-boards (**works**) | The sub-board ZIPs are the most complete design packages Espressif publishes. |
| 7 | Third-party component datasheets (panel, camera, driver IC, connector) | `dl.espressif.com`, mirrored | Copyright is the original vendor's; redistribution status unknown. |
| 8 | Board examples and factory demos | `github.com/espressif/esp-dev-kits/tree/<commit>/examples/<board>` | The commit is in the user guide's "Edit on GitHub" link. **Example directories are frequently still named after the EOL predecessor.** |
| 9 | Browser-flashable prebuilt images | ESP Launchpad, `espressif.github.io/esp-launchpad/?flashConfigURL=…` | Also often still keyed to the predecessor board name. |
| 10 | Chip errata for the fitted silicon revision | `esp-chip-errata`, §6.1 row 3 | Board user guides call out revision-specific errata in boxed warnings — read those first. |

**Two traps specific to board research.** First, a board's *name* may change without its design changing: Espressif renamed the P4 boards to `ESP32-P4X-…` purely to signal a newer fitted chip revision, and `ESP32-P4X` is not a chip. Second, **filenames and example paths outlive board names**, so a `esp32-p4-function-ev-board-*.pdf` linked from an `ESP32-P4X-*` guide is correct and not a mistake.

### 6.2 Resolving an unknown filename slug

Two techniques, in order of cost:

**(a) Scrape the landing page** — works for server-rendered esp-docs themes:

```bash
curl -sSL https://docs.espressif.com/projects/esp-adf/en/latest/ \
  | grep -oE 'href="[^"]*\.pdf"' | sort -u
# href="./esp-adf-en-master.pdf"
```

**(b) Brute-force the small slug space** — three candidates cover everything observed:

```bash
proj=esp-dsp; ver=latest; tgt=esp32
for slug in master latest "$ver"; do
  for u in "https://docs.espressif.com/projects/$proj/en/$ver/$tgt/$proj-en-$slug-$tgt.pdf" \
           "https://docs.espressif.com/projects/$proj/en/$ver/$proj-en-$slug.pdf"; do
    code=$(curl -sSL -o /tmp/p -w '%{http_code}' "$u")
    [ "$(head -c 4 /tmp/p)" = "%PDF" ] && echo "HIT $u ($code)"
  done
done
```

If nothing hits, the project genuinely has no PDF build; fall back to GitHub.

**(c) Reusable validating download** used for every artifact in this tree:

```bash
dl() { # dl <url> <dest>
  curl -sSL --max-time 300 -o "$2.part" "$1" || return 1
  if [ "$(head -c 4 "$2.part")" != "%PDF" ]; then
    echo "FAIL not-a-pdf: $1"; rm -f "$2.part"; return 1
  fi
  mv "$2.part" "$2"
  echo "OK $(sha256sum "$2" | cut -d' ' -f1) $(stat -c%s "$2") $2"
}
```

The `.part` staging matters: it guarantees a bad response never lands at the final filename.

### 6.3 Finding PCNs (product change notices)

PCNs record silicon and packaging changes that alter a part's behaviour, and they are frequently the **only** source for a fact that contradicts the datasheet. They are not indexed in the esp-docs projects.

- They live on `documentation.espressif.com` under human-readable, often **Chinese-titled, percent-encoded** filenames, even for English-relevant content.
- **Many are HTML-only, with no PDF rendition.** Worked example: **PCN-2021-021, "Upgrade ESP32-U4WDH to a Dual-Core Processor Product"** (document v1.3, issued 2021-09-02, effective 2021-12-02) — it records that ESP32-U4WDH was originally a *single-core* ECO V3 part capped at 160 MHz before that change. It is served at:

  ```
  https://documentation.espressif.com/en/PCN-2021-021%20ESP32-U4WDH%20%E5%8D%87%E7%BA%A7%E4%B8%BA%E5%8F%8C%E6%A0%B8%E5%A4%84%E7%90%86%E5%99%A8%E4%BA%A7%E5%93%81.html
  ```

  Every plausible PDF rendition returns the 13 745-byte soft-404 shell. **Do not save the HTML under a `.pdf` name.** Record it as a failure with the working HTML URL, and summarise the substantive finding in the component record.
- To obtain a signed PDF PCN, request it from Espressif sales/support, who distribute PCNs as PDF to notified customers.
- Practical search: query the documentation platform's full-text search for the part number plus "PCN", and search `PCN-<year>-<nnn>` directly. Espressif's own search index also covers *inside* PDFs, which is how we confirmed that the ESP32-S3 PIE specification is TRM Chapter 1 and not a standalone document.

### 6.4 When nothing resolves

1. Check the Wayback availability API — `https://archive.org/wayback/available?url=<url>` — and the CDX index for all archived PDFs under the legacy path. A document that was *never* archived and does not resolve today very likely never existed under that name.
2. Search the esp-docs full-text index; the content may exist as a *chapter* of a larger document rather than a document of its own. This is common: instruction-set extensions, chip-revision identification and power-consumption tables are all chapters, not standalone PDFs.
3. Check `github.com/espressif/<project>` for in-repo `docs/`.
4. Record the dead end, with every URL tried and its status, in [`component-download-failures.txt`](../../component-download-failures.txt). A well-recorded negative result is a real research output and prevents the next person repeating the search.

---

## 7. Parts and boards documented using this guide

| Part | Record |
|---|---|
| ESP32-S3R8 | [components/espressif/esp32-s3r8/README.md](../../components/espressif/esp32-s3r8/README.md) |
| ESP32-U4WDH | [components/espressif/esp32-u4wdh/README.md](../../components/espressif/esp32-u4wdh/README.md) |
| ESP32-P4 | [components/espressif/esp32-p4/README.md](../../components/espressif/esp32-p4/README.md) |

| Official board | Record |
|---|---|
| ESP32-P4X-Function-EV-Board | [devices/espressif/esp32-p4x-function-ev-board/README.md](../../devices/espressif/esp32-p4x-function-ev-board/README.md) |
| ESP32-P4X-C5-Function-EV-Board | [devices/espressif/esp32-p4x-c5-function-ev-board/README.md](../../devices/espressif/esp32-p4x-c5-function-ev-board/README.md) |
| ESP32-P4X-EYE | [devices/espressif/esp32-p4x-eye/README.md](../../devices/espressif/esp32-p4x-eye/README.md) |
| ESP32-P4-Function-EV-Board (EOL) | [devices/espressif/esp32-p4-function-ev-board/README.md](../../devices/espressif/esp32-p4-function-ev-board/README.md) |
| ESP32-P4-EYE (EOL) | [devices/espressif/esp32-p4-eye/README.md](../../devices/espressif/esp32-p4-eye/README.md) |

## 8. Change log for this guide

| Date | Change |
|---|---|
| 2026-08-21/22 | Created during ESP32-S3R8 / ESP32-U4WDH research. |
| **2026-08-21** | **§1 corrected** — `dl.espressif.com` *is* a documentation host for board design files. **§2.4 added** (its three path prefixes). **§2.5 added** (`esp-dev-kits` structure, EOL layout, GitHub slug enumeration). **§2.6 added** (broken board reference-design ZIP class). **§3 corrected** — ESP-IDF PDF cutoff is v5.3.2, not v5.2.x; `esp-dev-kits` added to the project table. **§4 corrected** with the consecutive-patch probe evidence. **§5.5 added** — `documentation.espressif.com` HTML renditions are now SPA-only and need a browser render. **§6.1a added** — board-level enumeration checklist. Findings from the ESP32-P4 research pass. |

See also the [vendor guide index](../README.md) and the [hardware research root](../../README.md).
