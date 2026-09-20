# ESP32-P4X-C5-Function-EV-Board — source manifest

> Sources for the **dual-band Wi-Fi** member of the ESP32-P4 evaluation-board family, board
> version **2.0**. Originally retrieved **2026-08-21**; URLs re-verified **2026-08-28**.
> Local paths are relative to this device folder; a dash means link-only.
>
> ✅ **This is the only ESP32-P4 board whose main-board schematic, PCB layout and dimensions
> Espressif publishes as direct, resolving downloads.** Every other board in the family relies on a
> substitution from an EOL predecessor or on a reference-design ZIP that does not resolve.

`Class` is one of **primary** / **authorized mirror** / **credible mirror** / **standard** / **community**.

This file supersedes and expands [§8 of `README.md`](README.md#8-sources); the `S1`–`S4` IDs used on
that page map onto `C5-1`–`C5-4` here.

---

## 1. Primary documentation

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| C5-1 (=S1) | ESP32-P4X-C5-Function-EV-Board User Guide | Espressif Systems | primary | manual | <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4x-c5-function-ev-board/user_guide.html> | 2026-08-21; HTTP 200 2026-08-28 | esp-dev-kits `latest`; source commit `f6f80ab` at retrieval, **`df877cb` on 2026-08-28** | **Almost the entire record**: the feature list including the committed **16 MB flash + 32 MB PSRAM**, the ESP32-C5-MINI-1 dual-band radio, the clockwise board layout with its two ordering differences from the C6 board, the **new item 28 — an ESP-Prog/UART programming connector for the P4 itself**, *"no previous revisions"*, all four design-file URLs, the flash 80 MHz / no-auto-suspend limit, the LDO_VO3/VO4 sleep-power caveat, and the `R30`→`R29` `P4_WAKEUP_C5` strap footnote | ⚠ **`latest` is an unstable path** and the source commit has already advanced, so this URL is not a pin. **Vendor claims, not measurements.** ⚠ The **32 MB PSRAM** figure is notable precisely because it is *stated* here while the C6 board's guide says only "supports up to 32 MB" — treat the C6 board's as unconfirmed and this one as stated, **not** as a family-wide fact | – |
| C5-2 (=S2) | Espressif DevKits product catalogue | Espressif Systems | primary | store listing | <https://www.espressif.com/en/products/devkits> | 2026-08-21; HTTP 200 2026-08-28 (465,290 B) | as served, undated | Board lineup and marketing description | Undated marketing page with no version to pin. Adds nothing C5-1 does not state more precisely | – |
| C5-3 (=S3) | ESP-IDF `COMPATIBILITY.md` and chip-support matrix | Espressif Systems | primary | repository | <https://github.com/espressif/esp-idf/blob/master/COMPATIBILITY.md> | 2026-08-21; HTTP 200 2026-08-28 | `master` as served | That the **ESP32-C5 is supported only since ESP-IDF v5.5.2** — which, not the P4's v5.3 floor, is the practical toolchain minimum if you intend to build ESP-Hosted slave firmware for the C5 yourself | ⚠ **`master` is a moving target**, not a pinned commit or tag. The value read on 2026-08-21 may have changed; not re-read on 2026-08-28 | – |

## 2. Primary design files — the good case

Published directly from `dl.espressif.com/schematics/`. **Note the path is `/schematics/`, not
`/dl/schematics/`** — Espressif uses both on the same host and they are not redirects of each
other. All four re-probed **2026-08-28**: HTTP 206 with the expected content type.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| C5-4a (=S4) | Schematics, board **2.0** | Espressif Systems | primary | schematic | <https://dl.espressif.com/schematics/ESP32_P4X_C5_Function_EV_board-2.0-schematics.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | **board v2.0** | The board's circuitry. **The reference design you can actually read** if you are doing your own ESP32-P4 hardware — no substitution required | `%PDF` validated. 789,023 B, SHA-256 `ceff97cf20e86b30480f8410d285f411108b4402beb2f63c1a0559f5119b9bd9`. ⚠ The `-2.0-` in the filename is the board version: **if Espressif issues a 2.1 these URLs will not silently update** — re-check them | [`artifacts/esp32-p4x-c5-function-ev-board-2.0-schematics.pdf`](artifacts/esp32-p4x-c5-function-ev-board-2.0-schematics.pdf) |
| C5-4b (=S4) | PCB layout, board **2.0** | Espressif Systems | primary | schematic | <https://dl.espressif.com/schematics/ESP32_P4X_C5_Function_EV_board-2.0-pcb-layout.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | **board v2.0** | Copper/placement view | `%PDF` validated. 1,858,663 B, SHA-256 `99f52f5e42d09f31807ab3b434a62d494cc689303bdd6de4cd9d5f3ff5c06e16`. ✅ Unlike the [P4-EYE pair](../esp32-p4-eye/sources.md#2-primary-design-files), **schematic and layout here carry the same version** — there is no revision skew to work around | [`artifacts/esp32-p4x-c5-function-ev-board-2.0-pcb-layout.pdf`](artifacts/esp32-p4x-c5-function-ev-board-2.0-pcb-layout.pdf) |
| C5-4c (=S4) | Dimensions drawing, board **2.0** | Espressif Systems | primary | schematic | <https://dl.espressif.com/schematics/ESP32_P4X_C5_Function_EV_board-2.0-dimensions.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | **board v2.0** | Mechanical outline and mounting geometry | `%PDF` validated. 973,576 B, SHA-256 `e17701e88dcd413dbc9c8dbc6756dd1e80548f0bbd28cb1bd026a5abc73c6473` | [`artifacts/esp32-p4x-c5-function-ev-board-2.0-dimensions.pdf`](artifacts/esp32-p4x-c5-function-ev-board-2.0-dimensions.pdf) |
| C5-4d (=S4) | Dimensions, CAD source (DXF), board **2.0** | Espressif Systems | primary | schematic | <https://dl.espressif.com/schematics/ESP32_P4X_C5_Function_EV_board-2.0-dimensions.dxf> | 2026-08-21; HTTP 206 `image/vnd.dxf` 2026-08-28 | **board v2.0** | Machine-readable mechanical outline — the only editable CAD published for this board | AutoCAD drawing-exchange format; Espressif suggests the free Autodesk Viewer. 3,790,900 B, SHA-256 `66098f18545d861f3655a80ecdf8e789a112c60da59ea77e5dd0eb2eca028a29` | [`artifacts/esp32-p4x-c5-function-ev-board-2.0-dimensions.dxf`](artifacts/esp32-p4x-c5-function-ev-board-2.0-dimensions.dxf) |

**Not published for this board:** BOM, Gerbers, assembly drawing or EDA source. Espressif directs
those to `sales@espressif.com`. Note the [EOL P4-Function-EV board](../esp32-p4-function-ev-board/sources.md)
*does* have a published assembly drawing where this board does not — and it is **not an ancestor of
this design**, so its schematic is **not** a substitute for C5-4a.

## 3. Shared artifacts

Twelve files Espressif publishes once and links from several P4 board guides, stored once in
[`../shared-artifacts/`](../shared-artifacts/). All applicable to this board; full provenance,
hashes and licence position in [`../shared-artifacts/sources.md`](../shared-artifacts/sources.md).

| ID | Group | Class | Establishes | Scope/limitations |
|---|---|---|---|---|
| C5-5 | FPC connector spec (`1.0K-GT-15PB`), panel and camera datasheets, EK79007AD and EK73217BCGA display-driver datasheets | primary / authorized mirror | The MIPI-DSI/CSI connector (item 21, 1.0 mm pitch, 15-pin) and the optional display/camera parts | ⚠ Third-party copyright, mirrored by Espressif with **no stated licence** — redistribution status `unknown` |
| C5-6 | LCD and camera **sub-board** schematics and PCB layouts | primary | The adapter boards the optional LCD and camera attach through | ⚠ Still named `esp32-p4-function-ev-board-…` after the **EOL** board even though this board's guide links them. Also **re-prints, not different revisions** — see [`EXTRACTED-ADAPTER-BOARDS.md` §4](../shared-artifacts/EXTRACTED-ADAPTER-BOARDS.md) |
| C5-7 | LCD and camera **adapter-board reference designs** (ZIP, extracted) | primary | The **most complete design packages Espressif publishes anywhere in the P4 family** — OrCAD `.DSN` and Allegro `.brd` source, full Gerbers, drill, BOM, placement, Chinese-language fabrication notes. 74 members each, integrity-verified | ⚠ **LCD package version skew is real**: schematic V1.3 but *every* manufacturing output V1.2 — fabricating from those Gerbers builds V1.2 while reading a V1.3 schematic. ⚠ **Single-source risk**: no Internet Archive capture of either ZIP exists |
| C5-8 | esp-dev-kits documentation, ESP32-P4 target, PDF build | primary | An offline copy of every P4 board user guide | ⚠ **`master` build — a moving target.** **Archived out of the repository 2026-08-24**; 30,482,003 B, SHA-256 `04d75d2acda82c8f5136bfed4d1732e7e4bd095437e2ecacce271374d8f8538c`. Provenance: [`ARCHIVED-FRAMEWORK-GUIDES.md`](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) |

## 4. Software references

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| C5-9 | `espressif/esp-dev-kits` — `examples/esp32-p4-function-ev-board/examples/esp_brookesia_phone` | Espressif Systems | primary | repository | <https://github.com/espressif/esp-dev-kits> | 2026-08-21; HTTP 200 2026-08-28 | commit `f6f80ab` at retrieval | The example C5-1 points this board at | ⚠ **The example is written for the C6 board** and lives under the *pre-P4X* board's directory. **Expect the companion-radio configuration to need changing from C6 to C5.** Not cloned, built or run; nothing retained locally | – |
| C5-10 | ESP Launchpad configuration | Espressif Systems | primary | official page | <https://espressif.github.io/esp-launchpad/?flashConfigURL=https://espressif2022.github.io/ESP32-P4-Function-EV-Board/launchpad.toml> | 2026-08-21; HTTP 200 2026-08-28 | as served | A browser-based flashing route | ⚠ Published under the **pre-P4X board name** and served from a personal-looking GitHub Pages namespace. **Unversioned and mutable.** Same C6-vs-C5 applicability caveat as C5-9. Not exercised | – |

---

## 5. Retrieval findings

**Every source cited by this record still resolves.** C5-1, C5-2, C5-3, C5-9 and C5-10 returned
HTTP 200; all four design files (C5-4a–d) and every shared artifact returned HTTP 206 with the
expected content type. **This is the only board in the P4 family with no dead or migrated source.**

**The sibling records were not so lucky.** The two EOL board guides moved out of the `eol/` path
segment between the two passes and their originally-cited URLs now return HTTP 404 with no Wayback
capture — see [the EOL board's manifest §4](../esp32-p4-function-ev-board/sources.md#4-retrieval-findings).
This record cites neither, so it is unaffected.

**Three URL schemes on one host.** `dl.espressif.com` serves this board's files from
`/schematics/`, the EOL Function-EV board's from `/dl/schematics/`, and the EYE family's component
datasheets from `/AE/esp-dev-kits/`. All three are real; **none is a redirect of another**. Guessing
the wrong prefix produces a 404, not a redirect.

**The source commit advanced** from `f6f80ab` to `df877cb`, so pages behind `latest` are not
guaranteed to match what was mined. **No content was re-mined in this pass.**

---

## 6. Evidence notes and known gaps

**This record is built almost entirely on C5-1.** There is no second independent source for the
feature list, the board layout numbering or the strap footnote, and none was sought. C5-3 is the
only claim in the record backed by a source other than the user guide and the design files.

**The one thing this board is for is 5 GHz.** That capability is a property of the **ESP32-C5-MINI-1
companion module**, not of the ESP32-P4, which has no radio at all. C5-1 establishes the module is
fitted; **no throughput, range or coexistence measurement exists** from any source, and none is
inferred — including for the video-streaming workload the record argues the band matters for.

**The 32 MB PSRAM figure is stated for this board only.** It implies an `ESP32-P4NRW32X` part. Do
not propagate it to the C6 board, whose guide says only "supports up to 32 MB".

**No BOM, Gerbers, assembly drawing or EDA source for the main board** exist from any source. The
*adapter* boards are the exception (C5-7).

**The C5 toolchain floor is higher than the board's stated minimum.** C5-1 says ESP-IDF v5.3 for the
P4; C5-3 says v5.5.2 for the C5. Anyone rebuilding ESP-Hosted slave firmware needs the latter.

**No performance, pricing, availability, community, media or example-validation research was done.**
In particular, C5-1 explicitly warns the board's power architecture cannot demonstrate the chip's
low-power figures — **do not benchmark P4 sleep current on this board.**

**Retrieval-date convention.** `2026-08-21` rows were mined then. `2026-08-28` marks **status
re-verification only** — HTTP code and content type. Content was not re-fetched, re-hashed or
re-compared.

---

## 7. Related records

- [ESP32-P4X-Function-EV-Board](../esp32-p4x-function-ev-board/README.md) · [its sources](../esp32-p4x-function-ev-board/sources.md) — the 2.4 GHz sibling
- [ESP32-P4X-EYE](../esp32-p4x-eye/README.md) · [its sources](../esp32-p4x-eye/sources.md)
- [ESP32-P4-Function-EV-Board (EOL)](../esp32-p4-function-ev-board/README.md) · [its sources](../esp32-p4-function-ev-board/sources.md) — **not an ancestor of this design**
- [ESP32-P4-EYE (EOL)](../esp32-p4-eye/README.md) · [its sources](../esp32-p4-eye/sources.md)
- [Shared artifacts](../shared-artifacts/README.md) · [their sources](../shared-artifacts/sources.md)
- [ESP32-P4 component record](../../../components/espressif/esp32-p4/README.md)
- [Espressif vendor sourcing guide](../../../vendors/espressif/README.md)
