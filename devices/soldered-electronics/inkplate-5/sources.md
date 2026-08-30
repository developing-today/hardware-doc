# Inkplate 5 — source manifest

> Every source cited by this device record, with class, medium, retrieval date and local artifact path.
> Sources marked **2026-08-24** were retrieved during the original research pass; **2026-08-28** marks a
> URL re-verification pass in which the HTTP status was checked but content was not re-mined.
>
> Local paths are relative to this device folder. A dash means link-only (nothing retained locally).
> This manifest covers **both generations** where the evidence is shared; Gen-2-specific rows are in
> [`../inkplate-5-gen2/sources.md`](../inkplate-5-gen2/sources.md).

`Class` is one of **primary** / **authorized mirror** / **credible mirror** / **standard** / **community**.

---

## 1. Primary design data — Soldered Electronics hardware repository

The single most important source in this record. Everything in the BOM table, the component
identification and the licensing position derives from it, not from any product page.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| IP5-1 | `SolderedElectronics/Soldered-Inkplate-5-hardware-design` | Soldered Electronics (TAVU) | primary | repository | <https://github.com/SolderedElectronics/Soldered-Inkplate-5-hardware-design> | 2026-08-24 (HTTP 200 re-checked 2026-08-28) | commit `80c0d0fe`, 2024-10-20 | The complete V1.2.0 open-hardware design package — KiCad sources, BOM, schematic PDF, gerbers, 3D STEP, compliance certificates | Snapshot is a **plain copy, not a git clone** — no `.git`, so the commit is recorded here rather than being independently verifiable from the tree | [`artifacts/hardware/soldered-inkplate-5-hardware-design/`](artifacts/hardware/soldered-inkplate-5-hardware-design/) |
| IP5-2 | `Soldered Inkplate 5 BOM.csv` (V1.2.0) | Soldered Electronics | primary | repository | in IP5-1, `OUTPUTS/V1.2.0/` | 2026-08-24 | V1.2.0 | **Every row of the [BOM table](README.md#complete-bill-of-materials-inkplate-5-v120)** — designators, part numbers, functions; and the ED052TC2-vs-ED052TC4 panel difference when diffed against the Gen 2 BOM | Semicolon-delimited KiCad export (`Id;Designator;Package;Quantity;Designation;Supplier and ref;`). Lists the module only as `ESP32-WROVER` — **no B/E variant, no flash size** (see [gaps §5](gaps-and-conflicts.md)) | `artifacts/hardware/soldered-inkplate-5-hardware-design/OUTPUTS/V1.2.0/Soldered Inkplate 5 BOM.csv` (3,442 B) |
| IP5-3 | `Soldered Inkplate 5 Schematics.pdf` | Soldered Electronics | primary | schematic | in IP5-1, `OUTPUTS/V1.2.0/` | 2026-08-24 | V1.2.0 | Rendered schematic for all five hierarchical sheets | **Not netlist-parsed in this pass** — see [gaps §8](gaps-and-conflicts.md#8-not-covered-in-this-pass). Component identity came from IP5-2, not from tracing this PDF | `artifacts/hardware/soldered-inkplate-5-hardware-design/OUTPUTS/V1.2.0/Soldered Inkplate 5 Schematics.pdf` (1,021,221 B) |
| IP5-4 | KiCad hierarchical schematic sources | Soldered Electronics | primary | repository | in IP5-1, `CAD/V1.2.0/` | 2026-08-24 | V1.2.0 | Editable design source: `MCU`, `POWER`, `E-paper`, `CTRL & COMS`, `SD & RTC` sheets plus the root sheet | Six `.kicad_sch` files, 767 KB total. Machine-readable but **not parsed for connectivity in this pass** | `artifacts/hardware/soldered-inkplate-5-hardware-design/CAD/V1.2.0/*.kicad_sch` |
| IP5-5 | `Soldered Inkplate 5.kicad_pcb` and `PANEL/…_panel.kicad_pcb` | Soldered Electronics | primary | repository | in IP5-1, `CAD/V1.2.0/` | 2026-08-24 | V1.2.0 | Board layout and the production panel. The **ESP32-WROVER pad-to-net map** used to verify the Gen 2 and the ZeroWriter respin are pin-identical | The panel file (17.7 MB) is a manufacturing aid, not new design information | `artifacts/hardware/soldered-inkplate-5-hardware-design/CAD/V1.2.0/` (4,365,432 B + 17,657,358 B) |
| IP5-6 | `Soldered Inkplate 5 iBOM.html` | Soldered Electronics (InteractiveHtmlBom) | primary | repository | in IP5-1, `OUTPUTS/V1.2.0/` | 2026-08-24 | V1.2.0 | Interactive placement/BOM cross-reference — the fastest way to locate a designator physically | **Generated output**, derived from IP5-2 + IP5-5. Not independent evidence | `artifacts/hardware/soldered-inkplate-5-hardware-design/OUTPUTS/V1.2.0/Soldered Inkplate 5 iBOM.html` (791,871 B) |
| IP5-7 | Gerber set, `…267_2x162_47 4 gerber.zip` | Soldered Electronics | primary | repository | in IP5-1, `OUTPUTS/V1.2.0/` | 2026-08-24 | V1.2.0 | Fabrication-ready copper/mask/silk/drill data; board outline 267.2 × 162.47 mm implied by the filename | Not opened or verified in this pass | `artifacts/hardware/soldered-inkplate-5-hardware-design/OUTPUTS/V1.2.0/Soldered Inkplate 5 267_2x162_47 4 gerber.zip` (2,489,705 B) |
| IP5-8 | `Soldered Inkplate 5 3D.step`, case STEP/F3Z/STL | Soldered Electronics | primary | repository | in IP5-1, `CAD/V1.2.0/Source 3D files/` and `OUTPUTS/V1.2.0/3d printable files/` | 2026-08-24 | V1.2.0 | Mechanical envelope of the assembled board and the printable enclosure | The `.f3z` is a Fusion 360 archive — **proprietary format**, needs Fusion to open. STEP and STL are open | `artifacts/hardware/soldered-inkplate-5-hardware-design/` (28.4 MB + 10.9 MB + 4.97 MB + 15.0 MB) |
| IP5-9 | CE / UKCA declarations and multilingual safety sheets | Soldered Electronics | primary | regulatory record | in IP5-1, `OUTPUTS/Compliance/` | 2026-08-24 | undated in-repo | That Soldered ship conformity declarations **inside the public hardware repository** — unusual for an open-hardware vendor | **Retained but not read** ([gaps §8](gaps-and-conflicts.md#8-not-covered-in-this-pass)). No claim in this record depends on their content | `artifacts/hardware/soldered-inkplate-5-hardware-design/OUTPUTS/Compliance/` (5 files, 144,610 B) |
| IP5-10 | `LICENSE.md` — TAPR Open Hardware License v1.0 | TAPR, applied by Soldered Electronics | standard | manual | in IP5-1, repo root | 2026-08-24 | TAPR OHL v1.0 | The **actual licence grant** for the hardware design. This is why ZeroWriter could legally respin the Gen 2 | GitHub's licence detector reports `NOASSERTION` because it cannot machine-identify TAPR OHL — the file, not the API field, is authoritative | `artifacts/hardware/soldered-inkplate-5-hardware-design/LICENSE.md` (13,919 B) |
| IP5-11 | Upstream repository `README.md` | Soldered Electronics | primary | repository | in IP5-1, repo root | 2026-08-24 | commit `80c0d0fe` | — (recorded as a **negative** result) | ⚠ **Unedited template.** Still contains the literal placeholders `--- Product name ---`, `------ product description ------` and a Wikipedia `Example_image.svg`. Carries **no product information**; do not cite it. Noted in the [vendor guide](../../../vendors/soldered-electronics/README.md) | `artifacts/hardware/soldered-inkplate-5-hardware-design/README.md` (2,736 B) |

## 2. Primary software source — Inkplate Arduino library

The authoritative source for resolutions, pin assignments, the I2S1 display architecture, the
supported-board list and the peripheral-mode protocol. Where this library and Soldered's prose
documentation disagree, **this library wins** — it is what actually runs on the board.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| IP5-12 | `SolderedElectronics/Inkplate-Arduino-library` | Soldered Electronics | primary | repository | <https://github.com/SolderedElectronics/Inkplate-Arduino-library> | 2026-08-24 (HTTP 200 re-checked 2026-08-28) | commit `1751cbe5`, 2026-08-20; **LGPL-3.0** | The whole software section of [`README.md`](README.md#software); 306★ at retrieval | Plain copy, not a git clone. 725 files / 40.2 MiB, of which 33.2 MiB is `examples/` image assets | [`artifacts/source-snapshots/Inkplate-Arduino-library/`](artifacts/source-snapshots/Inkplate-Arduino-library/) |
| IP5-13 | `src/boards/Inkplate5/waveforms.h` and `src/boards/Inkplate5V2/waveforms.h` | Soldered Electronics | primary | repository | in IP5-12 | 2026-08-24 | commit `1751cbe5` | **The resolution figures**: `E_INK_WIDTH/HEIGHT` = 960×540 (`Inkplate5`) and 1280×720 (`Inkplate5V2`) | Compile-time constants — the strongest available evidence, since no E Ink panel datasheet exists ([gaps §6](gaps-and-conflicts.md)) | [`artifacts/source-snapshots/Inkplate-Arduino-library/src/boards/Inkplate5V2/waveforms.h`](artifacts/source-snapshots/Inkplate-Arduino-library/src/boards/Inkplate5V2/waveforms.h) |
| IP5-14 | `src/boards/Inkplate5V2/Inkplate5V2Driver.cpp` | Soldered Electronics | primary | repository | in IP5-12 | 2026-08-24 | commit `1751cbe5` | **The I2S1-parallel-DMA display architecture** and the `setI2S1pin()` D0–D7 → GPIO 4/5/18/19/23/25/26/27 mapping quoted in [`README.md`](README.md#how-the-e-paper-interface-actually-works) | Source-code evidence of what the driver *does*; it is not a vendor statement of what the *hardware* is. Corroborated by IP5-2/IP5-5 | [`artifacts/source-snapshots/Inkplate-Arduino-library/src/boards/Inkplate5V2/Inkplate5V2Driver.cpp`](artifacts/source-snapshots/Inkplate-Arduino-library/src/boards/Inkplate5V2/Inkplate5V2Driver.cpp) |
| IP5-15 | `src/boards/Inkplate5V2/pins.h` | Soldered Electronics | primary | repository | in IP5-12 | 2026-08-24 | commit `1751cbe5` | Expander-pin assignments (`OE`, `GMOD`, `SPV`, `WAKEUP`, `PWRUP`, `VCOM`, `SD_PMOS_PIN`) behind the PCAL6416A at 0x20 | Board-target-specific; do not generalise across Inkplate models | [`artifacts/source-snapshots/Inkplate-Arduino-library/src/boards/Inkplate5V2/pins.h`](artifacts/source-snapshots/Inkplate-Arduino-library/src/boards/Inkplate5V2/pins.h) |
| IP5-16 | `src/boards/` directory listing | Soldered Electronics | primary | repository | in IP5-12 | 2026-08-24 | commit `1751cbe5` | **The authoritative supported-board list** used for [the family table](README.md#the-inkplate-family): Inkplate 2, 5, 5V2, 6, 6COLOR, 6FLICK, 6PLUS, 10, 13SPECTRA, 4TEMPERA | Lists what *this library* supports. **Inkplate 6 MOTION is absent** — it has a separate library and a different architecture | `artifacts/source-snapshots/Inkplate-Arduino-library/src/boards/` |
| IP5-17 | `examples/Inkplate5V2/Diagnostics/Peripheral_Mode/` and `examples/Inkplate5/Diagnostics/Inkplate5_Peripheral_Mode/` | Soldered Electronics | primary | repository | in IP5-12 | 2026-08-24 | commit `1751cbe5` | **The shipped `TS;…` peripheral protocol (60 commands, variable-width coordinates)** — which resolved [gaps §2](gaps-and-conflicts.md#2-peripheral-mode--the-documentation-describes-an-obsolete-protocol--resolved) and contradicts IP5-24 | The exact `payloadSize` accounting was **not verified**; no tested client example is offered | `artifacts/source-snapshots/Inkplate-Arduino-library/examples/Inkplate5V2/Diagnostics/Peripheral_Mode/` |
| IP5-18 | Inkplate 5 / 5V2 example sketches (101 `.ino`) | Soldered Electronics | primary | repository | in IP5-12 | 2026-08-24 | commit `1751cbe5` | Available example coverage per board | **Retained but not reviewed** ([gaps §8](gaps-and-conflicts.md#8-not-covered-in-this-pass)). 33.2 MiB of the tree is their bundled BMP/JPG/`.h` image assets | `artifacts/source-snapshots/Inkplate-Arduino-library/examples/Inkplate5{,V2}/` |
| IP5-19 | Bundled third-party licences | various, via Soldered Electronics | primary | repository | in IP5-12, `licenses/` and `LICENSE` | 2026-08-24 | commit `1751cbe5` | That the archive is **mixed-licence**: LGPL-3.0 for the library itself, with separately-licensed bundled dependencies and Adafruit-GFX-derived fonts | Not individually audited. Treat per-file, not per-archive | `artifacts/source-snapshots/Inkplate-Arduino-library/licenses/`, `.../LICENSE` |
| IP5-20 | `SolderedElectronics/Inkplate-micropython` | Soldered Electronics | primary | repository | <https://github.com/SolderedElectronics/Inkplate-micropython> | 2026-08-24 (HTTP 200 re-checked 2026-08-28) | commit `4a2b2926`, 2026-08-10; **MIT** | The MicroPython driver path; 91★ at retrieval | Plain copy. 313 files / 10.0 MiB, including 3.9 MiB of **prebuilt `.bin` firmware for other Inkplate models** — not for the Inkplate 5 | [`artifacts/source-snapshots/Inkplate-micropython/`](artifacts/source-snapshots/Inkplate-micropython/) |

## 3. Primary prose documentation — Inkplate documentation repository and web

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| IP5-21 | `SolderedElectronics/Inkplate-documentation` | Soldered Electronics | primary | repository | <https://github.com/SolderedElectronics/Inkplate-documentation> | 2026-08-24 (HTTP 200 re-checked 2026-08-28) | commit `1b3d3329`, 2025-08-25 | The reStructuredText source behind `soldered.com/documentation/inkplate` — **the form of the docs worth citing**, since the rendered sites are unstable | ~10,000 lines; **surveyed, not fully mined** ([gaps §8](gaps-and-conflicts.md#8-not-covered-in-this-pass)). `arduino.rst` alone is 4,556 lines | [`artifacts/docs/Inkplate-documentation/`](artifacts/docs/Inkplate-documentation/) |
| IP5-22 | `source/features.rst`, lines 57–84 | Soldered Electronics | primary | manual | in IP5-21 | 2026-08-24 | commit `1b3d3329` | **The whole [family comparison table](README.md#family-comparison)** — screen sizes, resolutions, greyscale, refresh timings. Source of the 1.02 s / 0.12 s (Inkplate 5) and 1.13 s / 0.26 s (Gen 2) figures | **Vendor-published figures, not independently measured.** No test method, sample count or temperature is stated; e-paper waveform duration is temperature-dependent | [`artifacts/docs/Inkplate-documentation/source/features.rst`](artifacts/docs/Inkplate-documentation/source/features.rst) |
| IP5-23 | `source/hardware-reference.rst` | Soldered Electronics | primary | manual | in IP5-21 | 2026-08-24 | commit `1b3d3329` | — (recorded as a **conflict**) | ⚠ **Stale.** Still says the *"Inkplate 5 hardware repository is coming soon"* although IP5-1 has existed since 2024-10-20. See [gaps §3](gaps-and-conflicts.md#3-hardware-referencerst-is-stale) | [`artifacts/docs/Inkplate-documentation/source/hardware-reference.rst`](artifacts/docs/Inkplate-documentation/source/hardware-reference.rst) |
| IP5-24 | `source/peripheral-mode.rst` | Soldered Electronics | primary | manual | in IP5-21 | 2026-08-24 | commit `1b3d3329` | — (recorded as a **conflict**) | ⚠ **Describes an obsolete protocol.** The documented `#<op>(<args>)*` framing with 3-digit zero-padded coordinates is **not** what the current library implements (IP5-17). Do not build a client from this page | [`artifacts/docs/Inkplate-documentation/source/peripheral-mode.rst`](artifacts/docs/Inkplate-documentation/source/peripheral-mode.rst) |
| IP5-25 | Inkplate documentation site (current) | Soldered Electronics | primary | official page | <https://soldered.com/documentation/inkplate> | 2026-08-28 (HTTP 200) | live page | The current canonical home of the prose documentation | Rendered from IP5-21. **Prefer the `.rst` source** — the rendered site has already migrated hosts once | – |
| IP5-26 | Inkplate documentation on readthedocs | Soldered Electronics | primary | official page | <https://inkplate.readthedocs.io> | 2026-08-24; re-checked 2026-08-28 (HTTP 200) | deprecated | — (recorded as a **trap**) | ⚠ **Deprecated.** Returns HTTP 200 but serves only a **JavaScript redirect** to IP5-25, so naive fetchers capture an empty shell. Search engines still surface these URLs and the `.rst` source still cross-links them. See [gaps §4](gaps-and-conflicts.md#4-readthedocs-is-deprecated-but-still-indexed) | – |
| IP5-27 | Soldered Learn (tutorials) | Soldered Electronics | primary | official page | <https://learn.soldered.com> | 2026-08-28 | — | — | ❌ **DEAD — host does not resolve.** No DNS record for `learn.soldered.com` as of 2026-08-28 (checked with `getent hosts`; all three UA fallbacks returned connection failure, not an HTTP status). Still cited by the [vendor guide](../../../vendors/soldered-electronics/README.md) and by [`README.md`](README.md#related). **No claim in this record depends on it** | – |
| IP5-28 | Soldered community forum | Soldered Electronics | community | forum | <https://community.soldered.com> | 2026-08-28 (HTTP 200) | live | Vendor-hosted support channel | **Not searched or mined** in any pass. Listed for completeness | – |
| IP5-29 | Soldered store | Soldered Electronics | primary | store listing | <https://soldered.com> | 2026-08-28 (HTTP 200) | live | Product existence and the "Gen 2" marketing name | ⚠ **No per-product URL is recorded** because none was captured in the research pass, and the vendor's short-link form `https://www.solde.red/<SKU>` requires an SKU that was never obtained. **No pricing or availability research was done** ([gaps §8](gaps-and-conflicts.md#8-not-covered-in-this-pass)) | – |

## 4. Other official Soldered software (link-only)

Named in [`README.md` § Software](README.md#software). All re-checked **2026-08-28**, all HTTP 200.
None were cloned, inspected or tested — their licence fields are as reported by the repository record
at the time of the 2026-08-24 pass.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| IP5-30 | `Inkplate-ESP-IDF-component` | Soldered Electronics | primary | repository | <https://github.com/SolderedElectronics/Inkplate-ESP-IDF-component> | 2026-08-28 (HTTP 200) | GPL-3.0 | An ESP-IDF path exists alongside Arduino | Not inspected; no version pinned | – |
| IP5-31 | `Soldered-Inkplate-ESPHome` | Soldered Electronics | primary | repository | <https://github.com/SolderedElectronics/Soldered-Inkplate-ESPHome> | 2026-08-28 (HTTP 200) | GPL-3.0 | ESPHome external component | ⚠ Documented as covering **SPI Inkplates** — the Inkplate 5 is a **parallel** panel, so applicability is **unverified** | – |
| IP5-32 | `Inkplate-LVGL-Library` | Soldered Electronics | primary | repository | <https://github.com/SolderedElectronics/Inkplate-LVGL-Library> | 2026-08-28 (HTTP 200) | GPL-3.0 | LVGL integration exists | Not inspected; board coverage unverified | – |
| IP5-33 | `Inkplate-GUI-Designer` | Soldered Electronics | primary | repository | <https://github.com/SolderedElectronics/Inkplate-GUI-Designer> | 2026-08-28 (HTTP 200) | not recorded | Web UI designer tool | Not inspected | – |
| IP5-34 | `Inkplate-image-converter` | Soldered Electronics | primary | repository | <https://github.com/SolderedElectronics/Inkplate-image-converter> | 2026-08-28 (HTTP 200) | not recorded | Web image-conversion tool | Not inspected | – |
| IP5-35 | `Inkplate-Peripheral-Mode-Raspberry-Pi-Example` | Soldered Electronics | primary | repository | <https://github.com/SolderedElectronics/Inkplate-Peripheral-Mode-Raspberry-Pi-Example> | 2026-08-24; HTTP 200 2026-08-28 | not recorded | An official host-side peripheral-mode client exists | ⚠ **Protocol generation unverified.** Given IP5-24 vs IP5-17, this example may implement the **obsolete** protocol. Cited in [`features/peripheral-mode.md`](features/peripheral-mode.md) but not run | – |
| IP5-36 | `Inkplate-Peripheral-Mode-STM32-Example` | Soldered Electronics | primary | repository | <https://github.com/SolderedElectronics/Inkplate-Peripheral-Mode-STM32-Example> | 2026-08-24; HTTP 200 2026-08-28 | not recorded | As above, for STM32 hosts | Same caveat as IP5-35 | – |

## 5. Third-party / community projects (link-only)

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| IP5-37 | `turgu1/EPub-InkPlate` | Guy Turcotte (turgu1) | community | repository | <https://github.com/turgu1/EPub-InkPlate> | 2026-08-24; HTTP 200 2026-08-28 | 307★ at retrieval | **Demonstrated project** — a complete EPub reader, the highest-starred Inkplate application. The strongest evidence that the platform is viable for text-heavy devices | Star count is a popularity signal, **not** a correctness or maintenance signal. Not built, run or tested here; Inkplate 5 support unverified | – |
| IP5-38 | `turgu1/ESP-IDF-InkPlate` | Guy Turcotte (turgu1) | community | repository | <https://github.com/turgu1/ESP-IDF-InkPlate> | 2026-08-24; HTTP 200 2026-08-28 | not recorded | A community ESP-IDF port exists | Not inspected. Independent of the official IP5-30 | – |
| IP5-39 | `martinberlin/inkplate-platformio` | Martin Fasani (martinberlin) | community | repository | <https://github.com/martinberlin/inkplate-platformio> | 2026-08-24; HTTP 200 2026-08-28 | not recorded | A PlatformIO path exists | Not inspected | – |

## 6. Cross-referenced records in this repository

Not external sources — internal records that carry evidence this device record relies on.

| Record | What it supplies |
|---|---|
| [`../inkplate-5-gen2/sources.md`](../inkplate-5-gen2/sources.md) | The Gen 2 hardware repository (commit `7450a321`) and its BOM — the other half of the two-generation comparison |
| [`../../zerowriter/zerowriter-ink/sources.md`](../../zerowriter/zerowriter-ink/sources.md) | ZeroWriter's KiCad respin of the Gen 2, which is where the pin-map-identity finding was verified |
| [`../../../vendors/soldered-electronics/README.md`](../../../vendors/soldered-electronics/README.md) | Reusable URL templates, the GitHub-pagination trap, the BOM-delimiter trap, and the readthedocs → soldered.com migration |

---

## 7. Evidence notes and known gaps

**The design files carry this record, not the marketing.** Every component identity, the panel
difference between the two generations, and the licensing position come from IP5-1/IP5-2 and
IP5-12. No Soldered product page was mined, and no pricing or availability research was done.

**Two vendor documents actively contradict the shipping product.** IP5-23 claims a hardware
repository that has existed for nearly two years does not exist yet, and IP5-24 documents a
peripheral protocol the current firmware does not speak. Both are recorded in
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) rather than silently resolved.

**No E Ink panel datasheet exists in this record.** E Ink does not publish panel datasheets
openly, so *every* `ED052TC2` / `ED052TC4` specification here is derived from Soldered's design
files and library source — see [gaps §6](gaps-and-conflicts.md#6-no-e-ink-panel-datasheet) and the
[`ED052TC4` component record](../../../components/e-ink/ed052tc4/README.md). There is **no
component record for the `ED052TC2`** at all.

**Refresh timings are vendor claims (IP5-22).** They are the only figures available, they are
recorded as such, and an earlier architectural inference that contradicted them was
[explicitly retracted](gaps-and-conflicts.md#7-refresh-timings--resolved-and-my-inference-was-wrong).

**One dead host.** IP5-27 (`learn.soldered.com`) no longer resolves in DNS. It is referenced by
the vendor guide and by this record's *Related* line; nothing substantive depends on it.

**Retrieval-date convention.** Rows reading `2026-08-24` were mined then. Rows reading
`2026-08-28 (HTTP 200)` had only their **status re-verified** on that date — the content behind
them was not re-fetched or re-compared, so a silent upstream change since 2026-08-24 would not
have been detected.
