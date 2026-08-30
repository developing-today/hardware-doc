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
│   └── the repository root  ─────────┐ symlink, created by scripts/hardware-doc-init.sh
├── hardware-doc/         ←────┘ THIS REPO
└── hardware-doc-archive/        bulk artifacts moved out of here (separate repo, usually unpublished)
```

It is **not a submodule and not vendored** into the consuming repo: at ~440 MB it would
make every clone of that repo roughly 6.5× larger. Consumers clone it on demand.

```bash
git clone https://github.com/developing-today/hardware-doc.git
```

### Resolving the sibling archive

`../hardware-doc-archive` is a sibling of the **real repository root** — not of your working
directory, and not `~`. Under a git worktree resolve it via the *common* dir:

```bash
ARCHIVE="$(dirname "$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")")/hardware-doc-archive"
```

`--git-common-dir` rather than `--show-toplevel`: inside a linked worktree the toplevel is the
worktree, whose parent is the wrong directory. The archive holds bulky derived artifacts moved
out of this repo; every one leaves a `*.ARCHIVED.md` placeholder here carrying size, SHA-256,
upstream commit/author/licence and multiple recovery URLs, so **the archive is optional** —
its absence costs you convenience, not information.

`hardware-doc-archive` is **itself a git repository**, but it is normally **unpublished or
private** — at multiple gigabytes it is impractical to host alongside this one. Treat it as a
local companion: if you have it, placeholders resolve to real bytes; if you do not, they
resolve to recovery URLs.

See [`AGENTS.md`](AGENTS.md) for working conventions and
[`.agents/skills/hardware-device-research/SKILL.md`](.agents/skills/hardware-device-research/SKILL.md)
for the research method.

- [Devices](devices/README.md)
- [Components and interfaces](components/README.md)
- [Vendor documentation-sourcing guides](vendors/README.md)
- [Cross-cutting guides](guides/README.md) — [Espressif](guides/espressif/README.md) · [hardware subsystems](guides/hardware/README.md) · [markets and sourcing](guides/markets/README.md) · [reverse engineering](guides/reverse-engineering/netlists-from-vendor-eda-files.md) · [research technique](guides/research/finding-projects-that-use-a-board.md) · [NixOS host](guides/nixos/README.md)
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

## Quick entry points

- **How do I build firmware from this machine?** — [NixOS as an embedded development host](guides/nixos/README.md)

- **Which Espressif chip should this be?** — [ecosystem and product lines](guides/espressif/ecosystem-and-product-lines.md)
- **Which of these boards should I use?** — [device comparison matrix](guides/markets/device-comparison-matrix.md) — all fourteen documented devices side by side
- **How many PCNT units / DMA channels / UARTs does this chip have?** — [SoC peripheral reference](guides/espressif/soc-peripheral-reference.md)
- **How do I drive this display?** — [display interfaces](guides/hardware/display-interfaces.md) · e-paper specifically — [e-paper displays](guides/hardware/e-paper-displays.md)
- **Where should I buy this, and will the docs survive?** — [vendor and marketplace comparison](guides/markets/vendor-comparison.md)
- **Is this board a clone, and what differs?** — [clones, siblings and variants](guides/markets/clones-and-variants.md)
- **How do I recover a pinout the vendor never published?** — [netlists from vendor EDA files](guides/reverse-engineering/netlists-from-vendor-eda-files.md)
- **Espressif ESP32-P4** — [chip](components/espressif/esp32-p4/README.md) · [board index](devices/README.md#espressif--official-esp32-p4-development-boards) · [shared board artifacts](devices/espressif/shared-artifacts/README.md)
- **Espressif ESP32-S3** — [ESP32-S3R8](components/espressif/esp32-s3r8/README.md), including the [Bluetooth Classic limitation](components/espressif/esp32-s3r8/README.md#radio-capabilities-and-the-classic-bluetooth-limitation)
- **How to obtain any Espressif document** — [vendor guide](vendors/espressif/README.md)
- **Espressif framework knowledge** — [ESP-IDF peripheral capabilities](guides/espressif/esp-idf-peripheral-capabilities.md) · [ESP-ADF audio pipelines](guides/espressif/esp-adf-audio-pipelines.md) · [ESP-IoT-Solution components](guides/espressif/esp-iot-solution-components.md)

## Verification reports

- [Seeed XIAO ESP32S3 Sense](VERIFICATION-xiao-esp32s3-sense.md) — 2026-08-24: 1,092 files, 42 artifacts validated, 0 broken links, 0 hardware-tested claims.
