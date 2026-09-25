# Hardware research

Standalone repository: **[`developing-today/hardware-doc`](https://github.com/developing-today/hardware-doc)**.

Device and component research, decomposed to primary evidence — netlists parsed from vendor
EDA files, firmware images unpacked, datasheets mined — with every claim carrying its source
and evidence status.

## How this repo is used

It is normally checked out **beside** the repo that consumes it and symlinked into place:

```
<repo-parent>/
├── code/                        consuming repo (config, infra, …)
│   └── doc/hardware  ───────────┐ symlink, created by scripts/hardware-doc-init.sh
├── hardware-doc/         ←──────┘ THIS REPO
└── repo-archive/        bulk artifacts moved out of here (separate repo, usually unpublished)
```

It is **not a submodule and not vendored** into the consuming repo: at ~440 MB it would
make every clone of that repo roughly 6.5× larger. Consumers clone it on demand.

```bash
git clone https://github.com/developing-today/hardware-doc.git
./scripts/init.sh        # only needed if the archive is not already a sibling
```

`scripts/init.sh` points `archive/` and `scratch/` at the sibling artifact archive. A fresh
clone usually needs nothing — the symlinks are committed relative, so they already resolve when
`repo-archive/` sits beside this repo. Run it when the archive is elsewhere, newly added, or
this repo is a linked worktree. It never clones and never deletes.

### Resolving the sibling archive

`../repo-archive` is a sibling of the **real repository root** — not of your working
directory, and not `~`. Under a git worktree resolve it via the *common* dir:

```bash
ARCHIVE="$(dirname "$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")")/repo-archive"
```

`--git-common-dir` rather than `--show-toplevel`: inside a linked worktree the toplevel is the
worktree, whose parent is the wrong directory. The archive holds bulky derived artifacts moved
out of this repo; every one leaves a `*.ARCHIVED.md` placeholder here carrying size, SHA-256,
upstream commit/author/licence and multiple recovery URLs, so **the archive is optional** —
its absence costs you convenience, not information.

`repo-archive` is **itself a git repository**, but it is normally **unpublished or
private** — at multiple gigabytes it is impractical to host alongside this one. Treat it as a
local companion: if you have it, placeholders resolve to real bytes; if you do not, they
resolve to recovery URLs.

### The `archive/` symlink

When the archive is present locally it is reachable at **`./archive/`** — a tracked symlink
to `../repo-archive`. That gives `*.ARCHIVED.md` placeholders a stable in-repo path
to point at.

Both tracked symlinks in this project (`archive` here, `doc/hardware` in a consuming repo)
are committed **relative**, and `hardware-doc-init.sh` swaps in an **absolute** path only
where the relative form cannot resolve — then marks the path `--skip-worktree`, because
`.gitignore` has no effect on tracked files. See
[`AGENTS.md` § Symlinks and `--skip-worktree`](AGENTS.md#symlinks-and---skip-worktree) for
the caveat that matters: while the flag is set, git will not update that path.

See [`AGENTS.md`](AGENTS.md) for working conventions and
[`.agents/skills/hardware-device-research/SKILL.md`](.agents/skills/hardware-device-research/SKILL.md)
for the research method.

- [Devices](devices/README.md)
- [Components and interfaces](components/README.md)
- [Vendor documentation-sourcing guides](vendors/README.md)
- [Cross-cutting guides](guides/README.md) — [Espressif](guides/espressif/README.md) · [hardware subsystems](guides/hardware/README.md) · [NFC](guides/nfc/README.md) · [LoRa](guides/lora/README.md) · [markets and sourcing](guides/markets/README.md) · [reverse engineering](guides/reverse-engineering/netlists-from-vendor-eda-files.md) · [research technique](guides/research/finding-projects-that-use-a-board.md) · [NixOS host](guides/nixos/README.md)
- [Artifact manifest](artifact-manifest.md)
- [Inventory](inventory.txt)
- [Verification report](verification.json)
- [Component download failures](component-download-failures.txt)

All research in this initial set was retrieved 2026-08-21. Downloaded files are checksummed from local bytes; see each device/component record for provenance and caveats. Relative-link validation covers authored Markdown outside `artifacts/`; bundled upstream Markdown is preserved as supplied and is not claimed to be link-clean.

- [Size audit](SIZE-AUDIT.md) — where the 442 MB is, what is reproducible, what must stay

## Research passes

| Pass | Date | Scope |
|---|---|---|
| Waveshare ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 → 2026-08-23 | One device, decomposed into ~22 component records; Espressif and Waveshare vendor guides created |
| Framework-guide extraction and archival | 2026-08-24 | Distilled ESP-IDF (×5 target builds), ESP-ADF, ESP-IoT-Solution and esp-dev-kits PDFs into [`guides/espressif/`](guides/espressif/README.md), then archived the ~219 MB of regenerable framework PDFs out of the repository. Chip datasheets, TRMs, errata, hardware-design guidelines and board design files were **all retained**. Per-directory archive records with SHA-256 and verified download URLs: [u4wdh](components/espressif/esp32-u4wdh/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) · [s3r8](components/espressif/esp32-s3r8/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) · [p4](components/espressif/esp32-p4/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) · [P4 boards](devices/espressif/shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) |
| **Espressif ESP32-P4 and its official development boards** | **2026-08-21** | [ESP32-P4 component record](components/espressif/esp32-p4/README.md) plus **five** board records under [devices/espressif/](devices/espressif/). Established the real P4 board lineup (no Korvo board exists on P4); corrected three claims in the [Espressif vendor guide](vendors/espressif/README.md#8-change-log-for-this-guide) |
| **Cross-link completion, vendor guides and market docs** | **2026-08-24** | **17 new [vendor sourcing guides](vendors/README.md)** (10 for manufacturers whose parts we document, 7 anticipatory), each with product lines, part-numbering conventions, distribution channels, URL patterns verified by live probe **with negative controls**, and an explicit evidence boundary. Added manufacturer back-links to every manufacturer-specific component record. New [markets and sourcing](guides/markets/README.md) guides and the [Espressif ecosystem map](guides/espressif/ecosystem-and-product-lines.md). **Corrected a WCH finding**: the `downloads/<PART>DS1_PDF.html` URLs return an identical 4,305-byte SPA shell for every path, existing or not |
| **Host toolchain: NixOS embedded development** | **2026-08-30** | New [`guides/nixos/`](guides/nixos/README.md) covering ESP-IDF on NixOS (5.5.2 and 6.0.1 side by side, and why installing the package alone yields no `idf.py`), package availability in the locked nixpkgs with dated absences, and why LVGL/sensor libraries are project dependencies. New [SquareLine vendor guide](vendors/squareline/README.md) — the Linux build is **a ZIP, not an AppImage**, and the CDN **returns HTTP 206 for non-existent paths**. The 172 MiB proprietary editor ZIP is archived out of the repository with a [reacquisition record](vendors/squareline/artifacts/ARCHIVED-SQUARELINE-STUDIO-LINUX.md). ⚠ **Nothing in this pass was built or rebuilt** |
| **Seven-session sweep: Xteink, M5Stack DinMeter / Cardputer / LoRa expansions, LilyGO K230 and T-Display-S3, LoRa generations** | **2026-09-04 → 2026-09-07** | ~40 device records and ~90 component records across seven parallel sessions, indexed here on 2026-09-07. New device families: [Xteink](devices/README.md#xteink-阅星瞳--星瞳-star-pupil) pocket e-readers (6), [LilyGO](devices/README.md#lilygo-shenzhen-xin-yuan-electronic-technology-also-trades-as-ttgo) (16, including the repository's **first RISC-V device**, the K230), and the expanded [M5Stack](devices/README.md#m5stack) family — DinMeter ×2, five Cardputers and eight Cardputer radio expansions. Three new vendor guides ([Canaan](vendors/canaan/README.md), [LilyGO](vendors/lilygo/README.md), [Semtech](vendors/semtech/README.md)) and three cross-cutting guides ([LoRa radio generations](guides/hardware/lora-radio-generations.md), [parallel 8080 LCD buses](guides/hardware/parallel-8080-lcd-buses.md), [RISC-V and vendor-SDK toolchains on NixOS](guides/nixos/riscv-and-vendor-sdk-toolchains.md)). ⚠ **Nothing in this pass was verified on physical hardware**, and each session was forbidden from editing shared indexes — the merge, its deferrals and its parked corrections are recorded in [`research/passes/index-merge/README.md`](research/passes/index-merge/README.md) |
| **Round two: Xteink re-survey, schematic net-tracing, certification and market** | **2026-09-11** | Three parallel sessions, integrated the same day. ⭐ **Overturned the sweep's Xteink certification finding**: Xteink holds **five FCC Original Equipment grants** under grantee code `2BTR9`, and enumerating that code surfaced a **sixth device the vendor has never announced** — the [X4 Light](devices/xteink/x4-light/README.md). Dated the **X4 Classic launch** (2026-09-06, USD 79) and the **X4's withdrawal**. **291 schematic PDFs assessed** and five boards net-traced from PDF alone — Altium exports embed `CO`/`PI`/`NL` tokens at item coordinates, which is what made it possible ([guide](guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md)). **32 device records gained a `certification-and-compliance.md`**, each carrying its positive and negative controls. **174 FCC exhibits split**: 59 retained in-repo (57.8 MiB — internal photographs, including the **first public teardown of the Xteink X4**), 106 archived with self-sufficient placeholders (130.6 MiB); FCC exhibits are **US Government public records, redistribution `allowed`**. New guides: [finding certification records](guides/research/finding-certification-records.md), [tracing nets from schematic PDFs](guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md); new [Xteink vendor guide](vendors/xteink/README.md). ⚠ **Still nothing verified on physical hardware.** ⚠ `devices/m5stack/papermono/**` was owned by a live session throughout and was **not touched** — its deferrals are in [`research/passes/index-merge/deferred-round2.md`](research/passes/index-merge/deferred-round2.md) |

| **Preprint repositories and the wider literature** | **2026-09-01 → 2026-09-11** | All 78 entries on Wikipedia's [List of preprint repositories][wpl] **plus what that list omits**, in [`research/preprint-repositories/`](research/preprint-repositories/README.md) — 40 records, ~23,000 lines. Deep records for the servers carrying hardware/software/systems work ([arXiv](research/preprint-repositories/arxiv.md), [Cryptology ePrint](research/preprint-repositories/cryptology-eprint-archive.md), [HAL](research/preprint-repositories/hal.md), [Zenodo](research/preprint-repositories/zenodo.md), [TechRxiv](research/preprint-repositories/techrxiv.md), [ECSarXiv](research/preprint-repositories/ecsarxiv.md)); grouped records for the rest. **160 landmark papers and theses individually verified** by fetching each identifier and machine-checking its title — [collected by field](research/preprint-repositories/landmark-papers.md). ⭐ **Corrected six Wikipedia claims by measurement** (OSF Preprints `>1,000,000` → **200,519** hosted; ScienceOpen → **~3,584**; [Synthical hosts nothing at all](research/preprint-repositories/synthical.md)). Extended beyond preprints to the [lawful full-text ladder](research/preprint-repositories/open-access-full-text-sources.md) (**USENIX has been paywall-free since 2008** — the real home of the systems literature), [government and university technical reports](research/preprint-repositories/government-and-institutional-technical-reports.md) (**the RISC-V ISA specs are six Berkeley EECS reports**, verified), the [computing servers Wikipedia omits](research/preprint-repositories/additional-preprint-servers.md) (**ECCC**, **OpenReview**), [theses and dissertations](research/preprint-repositories/theses-and-dissertations.md) (**the global ETD discovery layer collapsed in 2025–26**; EThOS is metadata-only since the British Library cyberattack), [dead-site recovery](research/preprint-repositories/recovering-dead-technical-sites.md) (**the DEC SRC/WRL/CRL series survives only as a 2007 bitsavers mirror**), and [bulk libraries and their copyright status](research/preprint-repositories/bulk-libraries-and-shadow-archives.md). ⚠ **No artifacts retained; no shadow-library service probed and no mirror domains recorded anywhere** |

[wpl]: https://en.wikipedia.org/wiki/List_of_preprint_repositories

## Quick entry points

- **How do I build firmware from this machine?** — [NixOS as an embedded development host](guides/nixos/README.md)
- **Where is the paper for this, and can I trust it?** — [preprint repositories](research/preprint-repositories/README.md) · [landmark papers by field](research/preprint-repositories/landmark-papers.md) · [reliability and durability](research/preprint-repositories/reliability-and-durability.md)
- **I have a citation and want the PDF, legally** — [open-access full-text ladder](research/preprint-repositories/open-access-full-text-sources.md)
- **A vendor doc portal or datasheet host has died** — [recovering dead technical sites](research/preprint-repositories/recovering-dead-technical-sites.md)

- **Which Espressif chip should this be?** — [ecosystem and product lines](guides/espressif/ecosystem-and-product-lines.md)
- **Which of these boards should I use?** — [device comparison matrix](guides/markets/device-comparison-matrix.md) — all fourteen documented devices side by side
- **How many PCNT units / DMA channels / UARTs does this chip have?** — [SoC peripheral reference](guides/espressif/soc-peripheral-reference.md)
- **How do I drive this display?** — [display interfaces](guides/hardware/display-interfaces.md) · e-paper specifically — [e-paper displays](guides/hardware/e-paper-displays.md)
- **How do I bring up an NFC reader, and why does it read nothing?** — [NFC guide](guides/nfc/README.md) — standards, antenna matching, and symptom-to-cause debugging
- **What do SF, BW and CR actually cost me?** — [LoRa guide](guides/lora/README.md) — airtime, battery and duty-cycle arithmetic, LoRa vs LoRaWAN vs Meshtastic, and honest range estimation
- **Where should I buy this, and will the docs survive?** — [vendor and marketplace comparison](guides/markets/vendor-comparison.md)
- **Is this board a clone, and what differs?** — [clones, siblings and variants](guides/markets/clones-and-variants.md)
- **How do I recover a pinout the vendor never published?** — [netlists from vendor EDA files](guides/reverse-engineering/netlists-from-vendor-eda-files.md)
- **Espressif ESP32-P4** — [chip](components/espressif/esp32-p4/README.md) · [board index](devices/README.md#espressif--official-esp32-p4-development-boards) · [shared board artifacts](devices/espressif/shared-artifacts/README.md)
- **Espressif ESP32-S3** — [ESP32-S3R8](components/espressif/esp32-s3r8/README.md), including the [Bluetooth Classic limitation](components/espressif/esp32-s3r8/README.md#radio-capabilities-and-the-classic-bluetooth-limitation)
- **How to obtain any Espressif document** — [vendor guide](vendors/espressif/README.md)
- **Espressif framework knowledge** — [ESP-IDF peripheral capabilities](guides/espressif/esp-idf-peripheral-capabilities.md) · [ESP-ADF audio pipelines](guides/espressif/esp-adf-audio-pipelines.md) · [ESP-IoT-Solution components](guides/espressif/esp-iot-solution-components.md)
- **Which LoRa chip is this, and what breaks if I swap it?** — [LoRa radio generations](guides/hardware/lora-radio-generations.md) — the four generations of Semtech silicon, and the migration cost. ⚠ The **LLCC68 is pin-compatible with the SX1262 and 19 dB worse**; the **SX1268 cannot reach 868/915 MHz** at all
- **My display is black and the library says it initialised** — [parallel Intel-8080 LCD buses on ESP32](guides/hardware/parallel-8080-lcd-buses.md) — why the display-library choice matters more than the board, and a debugging checklist
- **How do I build for a RISC-V board with a vendor SDK?** — [RISC-V and vendor-SDK toolchains on NixOS](guides/nixos/riscv-and-vendor-sdk-toolchains.md) — why `pkgsCross.riscv64-*` is not a substitute for XuanTie GCC
- **I want a cheap pocket e-reader I can reflash** — [Xteink family](devices/README.md#xteink-阅星瞳--星瞳-star-pupil) — six products, four ESP32-based. ⚠ **The X4 Pro is not an enhanced X4**; firmware for one will not run on the other
- **Which LilyGO T-Display-S3 is this actually?** — [LilyGO family index](devices/README.md#lilygo-shenzhen-xin-yuan-electronic-technology-also-trades-as-ttgo) — one *name* covering eleven boards, eight display controllers and four chargers. Sourcing: [LilyGO vendor guide](vendors/lilygo/README.md)
- **How do I add LoRa, sub-GHz or NFC to a Cardputer?** — [M5Stack Cardputer expansions](devices/README.md#cardputer-expansions--lora-sub-ghz-and-nfc--added-2026-09-04) — and note that only the **ADV + Cap LoRa-1262** combination has an upstream Meshtastic variant
- **How do I obtain a Semtech, Canaan or LilyGO document?** — [Semtech](vendors/semtech/README.md) · [Canaan](vendors/canaan/README.md) · [LilyGO](vendors/lilygo/README.md) vendor guides
- **Is this thing certified, and how would I even check?** — [finding certification records](guides/research/finding-certification-records.md) — FCC grantee-code enumeration, which regulatory databases are actually reachable, and **the positive/negative controls that make an absence finding mean anything**. ⚠ `fccid.io` serves **403 to a Chrome UA and 200 to `curl`** — the honest user agent is the one that works
- **The vendor published a schematic PDF and nothing else** — [tracing nets from schematic PDFs](guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md) — Altium exports embed invisible `CO`/`PI`/`NL` tokens at item coordinates, which is what makes a net list recoverable with poppler alone. ⚠ **KiCad and EAGLE exports often outline their text to vector paths** and are then untraceable — but a usable second export often sits in the same directory
- **What has this vendor certified that it never announced?** — [Xteink vendor guide](vendors/xteink/README.md) — the worked example: enumerating grantee code `2BTR9` surfaced the [X4 Light](devices/xteink/x4-light/README.md), a device with no announcement, no listing and no price

## Verification reports

- [Preprint and scholarly-literature repositories](research/preprint-repositories/VERIFICATION.md) — 2026-09-11 re-probe of a 2026-09-01 → 07 pass: 40 records, 78/78 list coverage, 160 identifiers verified, 0 broken links. **Five findings corrected** (Berkeley EECS restored at a new path; Anubis answers HTTP 200 not 403; CERN CDS and ETH no longer walled; OpenReview's API block was transient; CogPrints' recovery route degraded) and **one dating error flagged**.
- [Seeed XIAO ESP32S3 Sense](VERIFICATION-xiao-esp32s3-sense.md) — 2026-08-24: 1,092 files, 42 artifacts validated, 0 broken links, 0 hardware-tested claims.
- [M5Stack PaperMono](VERIFICATION-m5stack-papermono.md) — 2026-09-01: 50 authored files (~14,700 lines), 23 artifacts validated, 0 broken links, 0 hardware-tested claims; 5 hypotheses refuted, 10 conflicts left open.
- [**Seven-session device sweep**](VERIFICATION-sweep-2026-09-04.md) — 2026-09-04 → 2026-09-07: the umbrella report for the whole pass. 469 authored files, **10 387 relative links checked / 1 broken** (pre-existing, in a vendored upstream README), 61 artifacts magic-byte validated / 0 mismatches, 0 device-record orphans, 0 deletions on any shared file, `HEAD` unchanged. ⚠ **Zero on-device claims.**
- [Xteink device family](VERIFICATION-xteink.md) — 2026-09-04: Xteink X3, X4, X4 Pro, X4 Classic, S4 and Nano.
- [M5Stack DinMeter](VERIFICATION-m5stack-dinmeter.md) — 2026-09-04: DinMeter (K134) and DinMeter v1.1 (K134-V11).
- [M5Stack Cardputer family](VERIFICATION-m5stack-cardputer.md) — 2026-09-04: 48 authored files, 331/331 links, 6/6 artifact hashes, 0 protected files touched.
- [LilyGO T-Display K230](VERIFICATION-lilygo-t-display-k230.md) — 2026-09-04: T-Display K230 and K230 Kit, the repository's first RISC-V device.
- [**Xteink family, round two**](VERIFICATION-xteink-round2.md) — 2026-09-11: the **X4 Classic launch** at USD 79 and the X4's withdrawal, the **undocumented X4 Light** found by FCC grantee enumeration, and three new custodians for the X4 Pro.
- [Certification, market and adjudication pass](archive/guides/research/artifacts/certification-and-market-2026-09-11/README.md) — 2026-09-11: closes two of the [2026-09-04 sweep](VERIFICATION-sweep-2026-09-04.md) §6 gaps and **overturns its Xteink certification finding**. 26 FCC filings, 174 exhibits, with positive and negative controls.
- [Schematic net-tracing pass](archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/README.md) — 2026-09-11: **291 schematic PDFs assessed**, five boards fully traced from PDF alone; per-file verdicts in [`traceability-census.md`](guides/reverse-engineering/schematic-pdf-traceability-census.md).
- [**Scratch relocation**](SCRATCH-RELOCATION-2026-09-20.md) — 2026-09-20: `scratch/` emptied. Every subject moved by `mv` to the archive tier at its owning record's repo-relative path, verified by file count and tree digest, with a `README.md` written at each destination. Two authored pass reports were **promoted into this repository** ([`research/passes/`](research/passes/README.md)) because 33 records cite them. **116 MB turned out not to be hardware material at all** — swept indiscriminately out of `/tmp` by earlier passes — and is preserved, unfiled and clearly labelled, in `repo-archive/scratch-foreign/`. ⚠ Use the relocation table to resolve any `scratch/…` path you meet in an older record.
