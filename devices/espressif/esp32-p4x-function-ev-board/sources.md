# ESP32-P4X-Function-EV-Board — source manifest

> Sources for Espressif's current flagship ESP32-P4 multimedia evaluation board.
> Originally retrieved **2026-08-21**; URLs re-verified **2026-08-28**.
> Local paths are relative to this device folder; a dash means link-only.
>
> ⚠ **This board has no board-specific local artifacts.** Espressif publishes no schematic, PCB
> layout or reference design that resolves for it. Everything design-related in the record is a
> **documented substitution** from the EOL predecessor — see [§3](#3-substituted-evidence--the-eol-predecessor).

`Class` is one of **primary** / **authorized mirror** / **credible mirror** / **standard** / **community**.

This file supersedes and expands [§11 of `README.md`](README.md#11-sources); the `S1`–`S5` IDs used
throughout that page map onto `P4X-1`–`P4X-5` here.

---

## 1. Primary documentation

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| P4X-1 (=S1) | ESP32-P4X-Function-EV-Board User Guide | Espressif Systems | primary | manual | <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4x-function-ev-board/user_guide.html> | 2026-08-21; HTTP 200 2026-08-28 | esp-dev-kits `latest`; source commit `f6f80ab` at retrieval, **`df877cb` on 2026-08-28** | **Almost the entire record** — §1–§8 and §10 of [`README.md`](README.md): the chip-revision statement, the Secure Download warning (**errata ROM-770**), the full key-specification table, the clockwise board layout, the **40-pin J1 header pin map** with the `R61`/`R59`→`R199`/`R197` XTAL_32K and `R231`→`R100` `SD_PWRn` strap-swap footnotes, the LCD adapter jumper wiring, the ribbon-cable direction rule, the flash 80 MHz / no-auto-suspend limit, the LDO_VO3/VO4 sleep-power caveat, and the official example list | ⚠ **`latest` is an unstable path** and the source commit has already advanced since retrieval, so this URL is not a pin. **Vendor claims, not measurements** — Espressif publishes no fps, latency or power figures for this board, and explicitly warns its power architecture cannot demonstrate the chip's low-power specs | – |
| P4X-2 (=S2) | ESP32-P4-Function-EV-Board User Guide (predecessor) | Espressif Systems | primary | manual | **current:** <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4-function-ev-board/user_guide.html> · **as cited 2026-08-21:** `…/esp32p4/eol/esp32-p4-function-ev-board/user_guide.html` | 2026-08-21; re-verified 2026-08-28 | esp-dev-kits `latest` | The **v1.4 → v1.52 revision history** reproduced in [`README.md` §9](README.md#9-product-history) — the USB-UART → native USB Serial/JTAG change and the **removal of IO24/IO25 from the pin headers**; plus every design-file URL used in §3 | ⚠ **The cited URL is now HTTP 404** — the EOL guides moved. See [the predecessor's manifest §4](../esp32-p4-function-ev-board/sources.md#4-retrieval-findings) for the full migration finding | – |
| P4X-3 (=S3) | Espressif DevKits product catalogue | Espressif Systems | primary | store listing | <https://www.espressif.com/en/products/devkits> | 2026-08-21; HTTP 200 2026-08-28 (465,290 B) | as served, undated | The board lineup, the marketing description, and the **`ESP32-P4X-Function-EV-Board-L2` SKU string** | ⚠ **The `-L2` suffix is unresolved.** It appears **only** in this catalogue — no user guide, schematic or revision note in `esp-dev-kits` uses it, and this same page says the board has "Same functionality as ESP32-P4-Function-EV-Board". Most likely an accessory-bundle SKU (LCD and camera are optional extras). **Do not assume it is a distinct PCB.** Undated marketing page; no version to pin | – |
| P4X-4 (=S4) | esp-dev-kits — EOL (End of Life) Boards, ESP32-P4 | Espressif Systems | primary | official page | <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/eol/eol-boards.html> | 2026-08-21; HTTP 200 2026-08-28 (15,478 B) | `latest`; source commit `df877cb` on 2026-08-28 | The EOL status of the predecessor boards, which is what makes the §3 substitution necessary | Still live at its original URL — this page did not move | – |
| P4X-5 (=S5) | esp-dev-kits documentation, ESP32-P4 target, PDF build | Espressif Systems | primary | manual | <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp-dev-kits-en-master-esp32p4.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | release `master`; title page **2026-08-23** | An offline copy of every P4 board user guide, including the two EOL guides whose HTML URLs have since moved | ⚠ **`master` build — a moving target**, not a versioned release; the URL serves newer content over time. **Archived out of the repository 2026-08-24**; 30,482,003 B, SHA-256 `04d75d2acda82c8f5136bfed4d1732e7e4bd095437e2ecacce271374d8f8538c`. Provenance, Wayback capture and verified URLs: [`ARCHIVED-FRAMEWORK-GUIDES.md`](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) | archived → `archive/devices/espressif/shared-artifacts/` |

## 2. Software and tooling references

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| P4X-6 | `espressif/esp-dev-kits` repository | Espressif Systems | primary | repository | <https://github.com/espressif/esp-dev-kits> | 2026-08-21; HTTP 200 2026-08-28 | commit `f6f80ab` at retrieval | The official examples cited in [`README.md` §10](README.md#10-getting-started-examples-and-firmware) — `esp_brookesia_phone`, `lvgl_demo_v8`, `lvgl_demo_v9` — under `examples/esp32-p4-function-ev-board/`, **and** the documentation source behind P4X-1 | ⚠ The example directory is still named after the **pre-P4X** board. **Not cloned, built or run**; no example is retained locally and none was validated | – |
| P4X-7 | ESP Launchpad configuration for prebuilt images | Espressif Systems | primary | official page | <https://espressif.github.io/esp-launchpad/?flashConfigURL=https://espressif2022.github.io/ESP32-P4-Function-EV-Board/launchpad.toml> | 2026-08-21; HTTP 200 2026-08-28 | as served | A browser-based flashing route requiring no ESP-IDF install | ⚠ The config is still published under the **pre-P4X board name**, and the `.toml` is served from a personal-looking GitHub Pages namespace (`espressif2022`). **Unversioned and mutable** — nothing here pins which images it serves. Not exercised | – |

## 3. Substituted evidence — the EOL predecessor

**Espressif publishes no design files for this board.** Its user guide offers only an
*"ESP32-P4X-Function-EV-Board Reference Design (ZIP)"* link, and that link **does not resolve** for
any filename variant tried — every one returns the documentation platform's soft-404 shell
(13,745 B at the 2026-08-21 probes). Probes are recorded in
[`component-download-failures.txt`](../../../component-download-failures.txt).

Because P4X-1 states the two boards differ **only in the fitted silicon revision**, the
predecessor's published design set is used as the closest available primary evidence.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| P4X-8 | ESP32-P4-Function-EV-Board design files — schematic v1.52, PCB layout, assembly v1.52, dimensions PDF + DXF | Espressif Systems | primary | schematic | `https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-{schematics_v1.52,pcb-layout,assembly_v1.52,dimensions}.{pdf,dxf}` | 2026-08-21; all five HTTP 206 2026-08-28 | v1.52 where versioned; **three of five are unversioned** | The circuitry, layout, assembly and mechanical outline used as this board's design evidence | ⚠ **This is a substitution, not an equivalence.** "Espressif describes the difference as a chip-revision change" is **not** the claim "the schematics are identical" — silkscreen, passives and errata-driven changes are unverified. Label it wherever relied on. Per-file hashes and caveats: [predecessor manifest §2](../esp32-p4-function-ev-board/sources.md#2-primary-design-files) | [`../esp32-p4-function-ev-board/artifacts/`](../esp32-p4-function-ev-board/artifacts/) |
| P4X-9 | Failed-download probe log | this repository | — (internal) | — | [`../../../component-download-failures.txt`](../../../component-download-failures.txt) | 2026-08-21 | — | That the reference-design ZIP is unrecoverable — a **negative result**, retained so the probes are not repeated | Records the soft-404 shell size, which is the reliable signature of this failure mode on the Espressif docs host | [`../../../component-download-failures.txt`](../../../component-download-failures.txt) |

## 4. Shared artifacts

Twelve files that Espressif publishes once and links from several P4 board guides, stored once in
[`../shared-artifacts/`](../shared-artifacts/) rather than duplicated into four board directories.
All applicable to this board; full provenance, hashes and licence position in
[`../shared-artifacts/sources.md`](../shared-artifacts/sources.md).

| ID | Group | Class | Establishes | Scope/limitations |
|---|---|---|---|---|
| P4X-10 | FPC connector spec (`1.0K-GT-15PB`), panel and camera datasheets, EK79007AD and EK73217BCGA display-driver datasheets | primary / authorized mirror | The MIPI-DSI/CSI connector and the display/camera parts named in [`README.md` §3](README.md#3-key-specifications) | ⚠ Third-party copyright, mirrored by Espressif with **no stated licence** — redistribution status `unknown` |
| P4X-11 | LCD and camera **sub-board** schematics and PCB layouts | primary | The adapter boards the optional LCD and camera attach through | ⚠ Still named `esp32-p4-function-ev-board-…` after the **EOL** board even though this board's guide links them. Also **re-prints, not different revisions** — see [`EXTRACTED-ADAPTER-BOARDS.md` §4](../shared-artifacts/EXTRACTED-ADAPTER-BOARDS.md) |
| P4X-12 | LCD and camera **adapter-board reference designs** (ZIP) | primary | The **most complete design packages Espressif publishes anywhere in the P4 family** — OrCAD `.DSN` and Allegro `.brd` source, full Gerbers, drill, BOM, placement, fabrication notes | ⚠ **LCD package version skew is real**: schematic V1.3 but *every* manufacturing output V1.2 — fabricating from those Gerbers builds V1.2 while reading a V1.3 schematic. ⚠ **Single-source risk**: no Internet Archive capture of either ZIP exists |

---

## 5. Retrieval findings

**One cited URL is dead: P4X-2.** The EOL user guides moved out of the `eol/` path segment between
2026-08-21 and 2026-08-28; the old path returns HTTP 404 with a 14,039 B soft-404 shell and has **no
Wayback capture**. The full finding — including how the migration was detected and why the EOL index
page did *not* move — is documented once in
[the predecessor's manifest §4](../esp32-p4-function-ev-board/sources.md#4-retrieval-findings).

**Everything else resolves.** P4X-1, P4X-3, P4X-4, P4X-6 and P4X-7 returned HTTP 200; P4X-5 and all
of P4X-8 and P4X-10–12 returned HTTP 206 with the expected content types.

**The documentation host is the unstable one.** Every failure and every migration observed in this
record is on `docs.espressif.com`. `dl.espressif.com` has served every artifact reliably across both
passes — including files with percent-encoded Chinese names, and despite `Last-Modified` headers
that update without the content changing.

**The source commit advanced** from `f6f80ab` to `df877cb`, so pages behind `latest` are not
guaranteed to match what was mined. **No content was re-mined in this pass.**

---

## 6. Evidence notes and known gaps

**This record is built almost entirely on one document.** P4X-1 supplies §1–§8 and §10 of
[`README.md`](README.md). There is no second independent source for the J1 pin map, the strap-swap
resistor footnotes or the board layout numbering, and none was sought.

**No board-specific artifact exists.** Everything design-related is the §3 substitution. Anyone
relying on it must reproduce the label, not just the conclusion.

**No BOM, Gerbers or EDA source for the main board** exist from any source. Espressif directs those
to `sales@espressif.com`. The *adapter* boards are the exception (P4X-12).

**The `-L2` SKU is unresolved** and should stay that way until a second source appears.

**No performance figures exist.** Espressif publishes none for this board, none were measured, and
none are inferred. The record explicitly declines to benchmark P4 sleep current here because P4X-1
states the board's power architecture makes that meaningless.

**No pricing, availability, community, media or example-validation research was done.**

**Retrieval-date convention.** `2026-08-21` rows were mined then. `2026-08-28` marks **status
re-verification only** — HTTP code and content type. Content was not re-fetched, re-hashed or
re-compared.

---

## 7. Related records

- [ESP32-P4-Function-EV-Board (EOL)](../esp32-p4-function-ev-board/README.md) · [its sources](../esp32-p4-function-ev-board/sources.md) — **the source of this board's design evidence**
- [ESP32-P4X-C5-Function-EV-Board](../esp32-p4x-c5-function-ev-board/README.md) · [its sources](../esp32-p4x-c5-function-ev-board/sources.md) — the 5 GHz sibling, and the only P4 board with published main-board design files
- [ESP32-P4X-EYE](../esp32-p4x-eye/README.md) · [its sources](../esp32-p4x-eye/sources.md)
- [Shared artifacts](../shared-artifacts/README.md) · [their sources](../shared-artifacts/sources.md)
- [ESP32-P4 component record](../../../components/espressif/esp32-p4/README.md)
- [Espressif vendor sourcing guide](../../../vendors/espressif/README.md)
