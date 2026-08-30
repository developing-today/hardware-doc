# Command ledger — XIAO ESP32S3 Sense

Every consequential command from this research pass, with execution status. Snapshot **2026-08-24**.
Status vocabulary: `executed-success` · `executed-failed` · `reported-working` (vendor-documented, not run here) · `inferred` (derived, not run) · `not-tested`.

**No hardware was available.** Every flashing, monitoring or measurement command below is `reported-working` or `inferred` — never `executed-success`.

Environment for all executed commands: Linux, bash, Python 3.14, `uvx` for ad-hoc Python deps. Working directory `devices/seeed-studio/xiao-esp32s3-sense/` unless stated.

## Acquisition

| # | Command | Purpose | Status |
|---|---|---|---|
| 1 | `curl -sSL -A '<Chrome UA>' 'https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/'` | Fetch the wiki page | **`executed-failed`** (functionally) — HTTP 200, 150,703 B, but only **1 `href`**. JS shell; no artifact URLs. Negative control. |
| 2 | `curl -sSL 'https://api.github.com/repos/Seeed-Studio/wiki-documents/git/trees/main?recursive=1'` | Enumerate wiki source | **`executed-failed`** — HTTP 404, branch does not exist |
| 3 | `curl -sSL '.../git/trees/master?recursive=1'` | idem | `executed-success` but **0** XIAO matches in 1,366 entries |
| 4 | `curl -sSL '.../git/trees/docusaurus-version?recursive=1'` | idem | **`executed-success`** — 16,372 entries, 300 matches. **This is the correct branch.** |
| 5 | Parallel fetch of 230 `raw.githubusercontent.com/.../docusaurus-version/<path>` | Retrieve wiki Markdown | `executed-success` — 230/230, 6.7 MB |
| 6 | Parallel download of 42 `files.seeedstudio.com` artifacts | Retrieve schematics, datasheets, CAD, firmware | `executed-success` — 42/42, 127,061,501 B |
| 7 | `unzip -tq <each .zip>` | Archive integrity | `executed-success` — 24/24 OK |
| 8 | PDF magic-byte + ZIP-signature validation on all 42 | Reject HTML-served-as-PDF | `executed-success` — 0 suspect |

## Analysis

| # | Command | Purpose | Status |
|---|---|---|---|
| 9 | `python3 tools/kicad_pcb_nets.py '<...>.kicad_pcb' J3` | **Recover the undocumented 30-pin B2B pinout** from resolved PCB nets | **`executed-success`** — 34 pads mapped |
| 10 | `python3 tools/kicad_netlist.py '<...>.kicad_sch' --ref U1` | Geometric netlist reconstruction; confirmed GPIO33–37 + SPICS1 are no-connects | `executed-success` — 57 pins |
| 11 | `python3 tools/parse_kicad_sch.py '<...>.kicad_sch' --bom` | Full BOM | `executed-success` — 83 placed components |
| 12 | `python3 tools/esp_image_info.py <bin>...` | Parse ESP image headers, `esp_app_desc_t`, partition table | **`executed-success`** — recovered IDF v4.4.4, build `Feb 8 2023 18:07:54`, full flash map |
| 13 | `uvx --from pypdf python /tmp/px2.py <schematic>.pdf` | Schematic PDF text | `executed-success` for KiCad exports; **`executed-failed`** for EAGLE exports (vector text, no text layer) |
| 14 | `uvx --from pypdf python tools/extract_showcase.py xiao-reference-design.pdf out.json` | Extract 117 projects + `/Annots` hyperlinks | `executed-success` — 116/117 with URLs |
| 15 | `python3 tools/diff_vendored_lib.py --vendored <zip> --upstream-repo <o/r> --out <patch>` | Detect patched vs stale vendored libraries | `executed-success` — 1 identical, 2 stale-but-unmodified; found an **expired root CA** |
| 16 | `python3 tools/dedupe_pointer.py <keep> <dup> "<why>"` | Replace exact-duplicate files with pointer notes | `executed-success` — 4 duplicates, 3.07 MB reclaimed |
| 17 | `python3 tools/archive_artifact.py --repo-root . --manifest tools/archive-manifest.json` | Move bulky artifacts to `../repo-archive` with recovery placeholders | `executed-success` — 108.86 MB relocated, nothing deleted |

Notable failure worth preserving: **`pdftotext` is not installed** in this environment, and there is no system wordlist at `/usr/share/dict/words`. PDF work therefore uses `uvx --from pypdf python`, and the de-kerning vocabulary is built from the PDF's own clean pages rather than a dictionary.

## Flashing and recovery — NOT executed here

| # | Command | Status |
|---|---|---|
| 18 | `python esp32_flasher.py --project xiao_esp32_sense_factory` | **`reported-working`** — the vendor's shipped `.bat`, Windows-only |
| 19 | `esptool.py --chip esp32s3 --port /dev/ttyACM0 --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size 8MB 0x0 bootloader.bin 0x8000 partition-table.bin 0xe000 boot_app0.bin 0x10000 CameraWebServer.bin` | **`inferred`** — assembled from `esp32_flasher.py` lines 117–119 + `project_config.json`. Offsets and flags are the vendor's; the single-invocation form is derived. See [`factory-firmware.md` §6.2](factory-firmware.md#62-cross-platform-equivalent) |
| 20 | `esptool.py --chip esp32s3 --port /dev/ttyACM0 read_flash 0x10000 0x330000 app0.bin` then `python3 tools/esp_image_info.py app0.bin` | **`inferred`** — read-back identification. The *parser* half is `executed-success` against the distributed image |
| 21 | `esptool.py erase_flash` | `inferred` — clears `nvs`; standard recovery |
| 22 | `espcoredump.py info_corefile -c <coredump>` | `inferred` — the factory table has a 64 KB `coredump` partition at `0x7f0000` |
| 23 | Hold **BOOT**, plug USB, release **BOOT** | **`reported-working`** — vendor-documented ROM bootloader entry |
| 24 | Hold **BOOT**, tap **RESET**, release **BOOT** | **`reported-working`** — same, for a powered board |
| 25 | `idf.py set-target esp32s3 && idf.py build flash monitor` | `inferred` — standard IDF flow; see [`development.md` §3](development.md#3-esp-idf) for the required `sdkconfig` options |
| 26 | `idf.py add-dependency "espressif/esp32-camera^2.0.4"` | `inferred` |

> **Never treat #19–#26 as verified.** They are documented so the procedure is recoverable, not because they were confirmed.

## Reusable scripts

All under [`tools/`](tools/), all executed successfully in this pass:

| Script | Does |
|---|---|
| [`kicad_pcb_nets.py`](../../../tools/kicad_pcb_nets.py) | Authoritative netlist from `.kicad_pcb` (resolved net names per pad) |
| [`kicad_netlist.py`](../../../tools/kicad_netlist.py) | Geometric netlist reconstruction from `.kicad_sch` |
| [`parse_kicad_sch.py`](../../../tools/parse_kicad_sch.py) | BOM and net-label extraction |
| [`esp_image_info.py`](../../../tools/esp_image_info.py) | ESP-IDF image headers, app descriptor, partition tables |
| [`extract_showcase.py`](../../../tools/extract_showcase.py) | Seeed catalogue projects + hyperlinks, with InDesign de-kerning |
| [`diff_vendored_lib.py`](../../../tools/diff_vendored_lib.py) | Vendored-vs-upstream drift; exits 1 on difference (CI-usable) |
| [`archive_artifact.py`](../../../tools/archive_artifact.py) | Relocate bulky files, leave provenance placeholders |
| [`dedupe_pointer.py`](../../../tools/dedupe_pointer.py) | Replace exact duplicates with pointer notes |

No secrets were used; no environment variables required.

## Related
- [`development.md`](development.md) · [`factory-firmware.md`](factory-firmware.md) · [`acquisition/README.md`](acquisition/README.md)
