# ESP32-P4-Function-EV-Board (EOL) — source manifest

> Sources for the **end-of-life** original ESP32-P4 multimedia evaluation board.
> Originally retrieved **2026-08-21**; URLs re-verified **2026-08-28**.
> Local paths are relative to this device folder; a dash means link-only.
>
> ⚠ **Two source URLs in this record moved between 2026-08-21 and 2026-08-28.** See
> [§4 Retrieval findings](#4-retrieval-findings) before citing the `eol/` paths anywhere.

`Class` is one of **primary** / **authorized mirror** / **credible mirror** / **standard** / **community**.

This file supersedes and expands [§6 of `README.md`](README.md#6-sources); the `S1`–`S4` IDs used
throughout that page map onto `P4F-1`–`P4F-4` here.

---

## 1. Primary documentation

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| P4F-1 (=S1) | ESP32-P4-Function-EV-Board User Guide | Espressif Systems | primary | manual | **current:** <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4-function-ev-board/user_guide.html> · **as cited 2026-08-21:** `…/esp32p4/eol/esp32-p4-function-ev-board/user_guide.html` | 2026-08-21; re-verified 2026-08-28 | esp-dev-kits `latest`; source commit `f6f80ab` at retrieval, **`df877cb` on 2026-08-28** | The **v1.4 → v1.52 revision history** (USB-UART → native USB Serial/JTAG; Full-speed OTG breakout added; **IO24/IO25 removed from the headers**); the complete component list; every design-file URL in P4F-4 | ⚠ **The cited URL is now HTTP 404** (14,039 B soft-404 shell). Content moved to the path without the `eol/` segment, which returns HTTP 200 / 49,519 B. **No Wayback capture of the old path exists.** Content behind the new URL was *not* re-mined on 2026-08-28 — only its availability was confirmed | – |
| P4F-2 (=S2) | ESP32-P4X-Function-EV-Board User Guide | Espressif Systems | primary | manual | <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4x-function-ev-board/user_guide.html> | 2026-08-21; HTTP 200 2026-08-28 | esp-dev-kits `latest` | **The substitution licence**: Espressif's statement that the successor differs from this board *only* in the fitted ESP32-P4 chip revision (v3.1 or later) — which is why this EOL board's design files are used as evidence for the current board | ⚠ **"Described as a chip-revision change" ≠ "schematics are identical."** Silkscreen, passives and errata-driven changes are unverified. Always label the substitution — see [P4X record §8](../esp32-p4x-function-ev-board/README.md#8-design-files-what-exists-and-an-important-substitution) | – |
| P4F-3 (=S3) | esp-dev-kits — EOL (End of Life) Boards, ESP32-P4 | Espressif Systems | primary | official page | <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/eol/eol-boards.html> | 2026-08-21; HTTP 200 2026-08-28 (15,478 B) | `latest`; source commit `df877cb` on 2026-08-28 | EOL status and the support statement quoted in [`README.md`](README.md): *"these boards … no longer receive updates, bug fixes, or official support"* | Still live at its original URL — **this page did not move**, unlike the guides it links to. Its own links now point at the non-`eol/` paths, which is how the migration in §4 was detected | – |

## 2. Primary design files

All published by Espressif from `dl.espressif.com/dl/schematics/`. All five re-probed
**2026-08-28**: HTTP 206 on a range request, correct `Content-Type`.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| P4F-4a (=S4) | Schematics, board v1.52 | Espressif Systems | primary | schematic | <https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-schematics_v1.52.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | **v1.52** | The board's circuitry — **and, by the P4F-2 substitution, the closest available primary evidence for the current P4X board**, whose own reference-design ZIP does not resolve | Validated by `%PDF` magic. 817,278 B, SHA-256 `7a1d12a37e21db20fe7db8092f4428b87465873feab65b3cd90bc6fe7dd6673b` | [`artifacts/esp32-p4-function-ev-board-schematics-v1.52.pdf`](artifacts/esp32-p4-function-ev-board-schematics-v1.52.pdf) |
| P4F-4b (=S4) | PCB layout | Espressif Systems | primary | schematic | <https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-pcb-layout.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | **unversioned filename** | Copper/placement view of the board | ⚠ **No version in the filename or URL.** Assumed to match v1.52; **that assumption is not verified**. `%PDF` validated. 1,808,476 B, SHA-256 `382426995df9dd4c5c26d4ef4fcbe575ef45425516ff6675039ede5b8c565a00` | [`artifacts/esp32-p4-function-ev-board-pcb-layout.pdf`](artifacts/esp32-p4-function-ev-board-pcb-layout.pdf) |
| P4F-4c (=S4) | Assembly drawing, v1.52 | Espressif Systems | primary | schematic | <https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-assembly_v1.52.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | **v1.52** | Component placement for assembly. **This board is the only one in the P4 family with a published main-board assembly drawing** — the C5 board, the other one with published main-board files, has none | `%PDF` validated. 131,618 B, SHA-256 `0d035b10b35f717a344f11d59059f228b42ba3a64fa4c751dc16f967d86bc816` | [`artifacts/esp32-p4-function-ev-board-assembly-v1.52.pdf`](artifacts/esp32-p4-function-ev-board-assembly-v1.52.pdf) |
| P4F-4d (=S4) | Dimensions drawing | Espressif Systems | primary | schematic | <https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-dimensions.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | **unversioned filename** | Mechanical outline and mounting geometry | Same unversioned caveat as P4F-4b. `%PDF` validated. 885,140 B, SHA-256 `f34799b848dc8b1638f1db473c69415512cad423c4e77be5fb03f534a334f57a` | [`artifacts/esp32-p4-function-ev-board-dimensions.pdf`](artifacts/esp32-p4-function-ev-board-dimensions.pdf) |
| P4F-4e (=S4) | Dimensions, CAD source (DXF) | Espressif Systems | primary | schematic | <https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-dimensions.dxf> | 2026-08-21; HTTP 206 `image/vnd.dxf` 2026-08-28 | **unversioned filename** | Machine-readable mechanical outline — the only editable CAD Espressif publishes for this board | Verified to be an ASCII AutoCAD DXF (begins with the standard `  0` / `SECTION` header, **not** HTML). Espressif suggests the free Autodesk Viewer. 3,879,854 B, SHA-256 `980ad74d4f7af35d403367acc735ac5f2a9bca726bd565bd4a21cda61250fe23` | [`artifacts/esp32-p4-function-ev-board-dimensions.dxf`](artifacts/esp32-p4-function-ev-board-dimensions.dxf) |

**Not published for this board:** BOM, Gerbers or EDA source. Espressif directs those to
`sales@espressif.com`. The *adapter* boards **do** have complete reference designs — see P4F-6.

## 3. Shared and contextual sources

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| P4F-5 | esp-dev-kits documentation, ESP32-P4 target, PDF build | Espressif Systems | primary | manual | <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp-dev-kits-en-master-esp32p4.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | release `master`; title page **2026-08-23** | An offline copy of every P4 board user guide in one file — **including the two EOL guides whose HTML URLs have since moved** (§4), which makes it the most robust surviving copy of P4F-1 | ⚠ **`master` build — a moving target**, not a versioned release; the URL will serve newer content over time. **Archived out of the repository 2026-08-24**; 30,482,003 B, SHA-256 `04d75d2acda82c8f5136bfed4d1732e7e4bd095437e2ecacce271374d8f8538c`. Full provenance and verified download URLs: [`ARCHIVED-FRAMEWORK-GUIDES.md`](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) | archived → `archive/hardware-doc/devices/espressif/shared-artifacts/` |
| P4F-6 | Shared artifact set for the Function-EV family | Espressif Systems and third-party vendors | primary / authorized mirror | datasheet, schematic | see [`../shared-artifacts/sources.md`](../shared-artifacts/sources.md) | 2026-08-21; all re-probed 2026-08-28 | per-file | FPC connector spec, panel and camera datasheets, display-driver datasheets, LCD/camera sub-board schematics and layouts, and the two **adapter-board reference designs with Gerbers, BOM and editable EDA source** | Stored once in [`../shared-artifacts/`](../shared-artifacts/) rather than duplicated into four board directories. Third-party datasheets are mirrored by Espressif with **no stated licence** — redistribution status `unknown` | [`../shared-artifacts/`](../shared-artifacts/) |
| P4F-7 | Failed-download probe log | this repository | — (internal) | — | [`../../../component-download-failures.txt`](../../../component-download-failures.txt) | 2026-08-21 | — | The recorded probes showing the **successor's** *"Reference Design (ZIP)"* link does not resolve for any filename variant — the reason this EOL record exists | Negative result. Retained so the probes are not repeated | [`../../../component-download-failures.txt`](../../../component-download-failures.txt) |

---

## 4. Retrieval findings

### The EOL user guides moved — the cited URL is now a 404

Probed **2026-08-28**:

| URL | Result |
|---|---|
| `…/esp32p4/eol/esp32-p4-function-ev-board/user_guide.html` *(as cited 2026-08-21)* | **HTTP 404**, 14,039 B soft-404 shell |
| `…/esp32p4/esp32-p4-function-ev-board/user_guide.html` *(current)* | **HTTP 200**, 49,519 B |
| `…/esp32p4/eol/esp32-p4-eye/user_guide.html` *(the sibling EOL board)* | **HTTP 404**, 14,039 B |
| `…/esp32p4/esp32-p4-eye/user_guide.html` *(current)* | **HTTP 200**, 41,557 B |
| `…/esp32p4/eol/eol-boards.html` *(the index)* | **HTTP 200** — **did not move** |

Espressif dropped the `eol/` path segment from the **board guides** while leaving the **EOL index
page** where it was. The migration was detected by fetching that index and reading its outbound
links, which now point at `../esp32-p4-eye/index.html` and
`../esp32-p4-function-ev-board/index.html`.

Two things make this worse than a routine redirect:

1. **It is not a redirect.** The old path returns a 404 shell with HTTP status 404, so a link
   checker catches it but a naive content fetcher that ignores status codes will silently capture
   14 KB of navigation chrome. This is the same soft-404 shell family (13,745 B at the 2026-08-21
   pass, 14,039 B now) already documented for the unresolvable P4X reference-design ZIPs.
2. **There is no Internet Archive capture of either old URL.** Queried via the Wayback availability
   API on 2026-08-28: `{"archived_snapshots": {}}` for both. If P4F-5 had not been retrieved, the
   content behind the originally-cited URL would now be unrecoverable at that address.

The `esp-dev-kits` documentation source commit also advanced from **`f6f80ab`** (2026-08-21) to
**`df877cb`** (2026-08-28), so the current pages are not guaranteed to match what was mined.
**No content was re-mined in this pass** — only availability was re-checked. Nothing in
[`README.md`](README.md) has been changed on the strength of the new URLs.

This is a reusable Espressif documentation-portal trap and belongs in the
[vendor sourcing guide](../../../vendors/espressif/README.md); it has **not** been added there in
this pass, which was scoped to device-level source manifests.

### Everything on `dl.espressif.com` still resolves

All five design files (P4F-4a–e) and every shared artifact (P4F-6) returned HTTP 206 with the
expected `Content-Type` on 2026-08-28. The download host has been markedly more stable than the
documentation host.

---

## 5. Evidence notes and known gaps

**This board is documented as an evidence donor.** Its own status is EOL; the reason the record is
maintained is that Espressif publishes *its* design files and not the successor's. Every use of
P4F-4 as evidence for the P4X board is a **substitution licensed by P4F-2's chip-revision
statement**, and must be labelled as such.

**Three of five design files are unversioned.** P4F-4b, P4F-4d and P4F-4e carry no revision in
filename or URL and are *assumed* to match v1.52. If a net or a dimension matters, check the
schematic and the layout against each other rather than trusting the pairing.

**IO24/IO25 are the silent-breakage trap.** P4F-1 is the only source establishing their removal in
v1.52. Any tutorial, example or forum post referencing them on a header predates v1.52 — and any
document describing a CP210x/CH34x driver for this board is a v1.4 document.

**No BOM, Gerbers or EDA source exist for the main board** from any source.

**Retrieval-date convention.** `2026-08-21` rows were mined then. `2026-08-28` marks **status
re-verification only**: HTTP code, content type and, for `dl.espressif.com`, that a range request
succeeds. Content was not re-fetched, re-hashed or re-compared.

---

## 6. Related records

- [ESP32-P4X-Function-EV-Board](../esp32-p4x-function-ev-board/README.md) · [its sources](../esp32-p4x-function-ev-board/sources.md) — the successor these files are used as evidence for
- [ESP32-P4X-C5-Function-EV-Board](../esp32-p4x-c5-function-ev-board/README.md) · [its sources](../esp32-p4x-c5-function-ev-board/sources.md)
- [ESP32-P4-EYE (EOL)](../esp32-p4-eye/README.md) · [its sources](../esp32-p4-eye/sources.md) — affected by the same URL migration
- [Shared artifacts](../shared-artifacts/README.md) · [their sources](../shared-artifacts/sources.md)
- [ESP32-P4 component record](../../../components/espressif/esp32-p4/README.md)
- [Espressif vendor sourcing guide](../../../vendors/espressif/README.md)
