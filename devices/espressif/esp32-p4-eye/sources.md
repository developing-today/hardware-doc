# ESP32-P4-EYE (EOL) — source manifest

> Sources for the **end-of-life** original ESP32-P4 hand-held vision board.
> Originally retrieved **2026-08-21**; URLs re-verified **2026-08-28**.
> Local paths are relative to this device folder; a dash means link-only.
>
> ⚠ **The primary source URL for this record now returns HTTP 404.** The page moved; see
> [§4 Retrieval findings](#4-retrieval-findings) before citing it.

`Class` is one of **primary** / **authorized mirror** / **credible mirror** / **standard** / **community**.

This file supersedes and expands [§5 of `README.md`](README.md#5-sources); the `S1`–`S4` IDs used on
that page map onto `P4E-1`–`P4E-4` here.

---

## 1. Primary documentation

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| P4E-1 (=S1) | ESP32-P4-EYE User Guide | Espressif Systems | primary | manual | **current:** <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4-eye/user_guide.html> · **as cited 2026-08-21:** `…/esp32p4/eol/esp32-p4-eye/user_guide.html` | 2026-08-21; re-verified 2026-08-28 | esp-dev-kits `latest`; source commit `f6f80ab` at retrieval, **`df877cb` on 2026-08-28** | The top- and bottom-PCB component tables; the Related Documents list (schematic, PCB layout, camera datasheet, display datasheet, ST7789VW datasheet, OV2710 overview); the statement *"No previous versions available."* | ⚠ **The cited URL is now HTTP 404** (14,039 B soft-404 shell); the non-`eol/` path returns HTTP 200 / 41,557 B. **No Wayback capture of the old path exists.** ⚠ Also note *"No previous versions available"* refers to **user guides, not board revisions** — and P4E-4 proves at least two board versions exist | – |
| P4E-2 (=S2) | ESP32-P4X-EYE User Guide | Espressif Systems | primary | manual | <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4x-eye/user_guide.html> | 2026-08-21; HTTP 200 2026-08-28 | esp-dev-kits `latest` | **The substitution licence**: Espressif's statement that the successor differs from this board *only* in the fitted ESP32-P4 chip revision — the reason this EOL board's schematic and layout are used as evidence for the current board | ⚠ **"Described as a chip-revision change" ≠ "the circuits are identical."** Label the substitution wherever it is relied on. See [P4X-EYE §5](../esp32-p4x-eye/README.md#5-design-files--partial-and-a-substitution) | – |
| P4E-3 (=S3) | esp-dev-kits — EOL (End of Life) Boards, ESP32-P4 | Espressif Systems | primary | official page | <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/eol/eol-boards.html> | 2026-08-21; HTTP 200 2026-08-28 (15,478 B) | `latest`; source commit `df877cb` on 2026-08-28 | EOL status and the support statement — no updates, bug fixes or official support | Still live at its original URL; **this page did not move**. Its outbound links are how the P4E-1 migration was detected | – |

## 2. Primary design files

Espressif publishes a real schematic PDF and a real PCB layout PDF for this board on
`dl.espressif.com/AE/esp-dev-kits/` — which the successor does **not** have. Both re-probed
**2026-08-28**: HTTP 206, `application/pdf`.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| P4E-4a (=S4) | Schematics, main board **V2.3** | Espressif Systems | primary | schematic | <https://dl.espressif.com/AE/esp-dev-kits/SCH_ESP32-P4-EYE-MB_V2.3_20250416.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | **V2.3**, filename-dated **2025-04-16** | The board's circuitry — and, by the P4E-2 substitution, the closest available primary evidence for the current P4X-EYE, whose reference-design ZIP does not resolve | ⚠ **One revision newer than the layout (P4E-4b).** Espressif publishes **no changelog** between V2.2 and V2.3, so **do not assume the layout implements this schematic**. Renamed from the upstream filename to the repository's lowercase-hyphen convention. `%PDF` validated. 748,835 B, SHA-256 `8d3769796bb38dda8682d87e94764f2163eb6cd4f1be886b3da91a512a55bffa` | [`artifacts/esp32-p4-eye-mb-schematics-v2.3.pdf`](artifacts/esp32-p4-eye-mb-schematics-v2.3.pdf) |
| P4E-4b (=S4) | PCB layout, main board **V2.2** | Espressif Systems | primary | schematic | <https://dl.espressif.com/AE/esp-dev-kits/PCB_ESP32-P4-EYE-MB_V2.2_20250314.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | **V2.2**, filename-dated **2025-03-14** | Copper/placement view of the board | ⚠ **One revision older than the schematic.** The two published files describe **different board versions**; if a net matters, check both. `MB` = "main board", consistent with the split top/bottom PCB construction. Renamed on retrieval. `%PDF` validated. 1,371,064 B, SHA-256 `9ad4f2ec83442c843487ad2f7e5100cf91ca5ea4a9facfa1d4bba5d9ef9d4f7c` | [`artifacts/esp32-p4-eye-mb-pcb-layout-v2.2.pdf`](artifacts/esp32-p4-eye-mb-pcb-layout-v2.2.pdf) |

**Not published for this board:** BOM, Gerbers, dimensions, assembly drawing or EDA source. Unlike
the Function-EV family there are **no adapter-board reference designs either**, because there are no
adapter boards.

## 3. Shared and contextual sources

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| P4E-5 | Component documentation mirrored by Espressif — OV2710, HDF2710-47-MIPI, ST7789VW, ZJY154KC-IF17 | third-party manufacturers, via Espressif | authorized mirror | datasheet | `https://dl.espressif.com/AE/esp-dev-kits/{ov2710pbv1.1web,HDF2710-47-MIPI-V2.0,ST7789VW芯片手册,胶铁一体ZJY154KC-IF17}.pdf` | 2026-08-21; all four HTTP 206 `application/pdf` 2026-08-28 | as served | The **camera and display part identities**: an OV2710-based `HDF2710-47-MIPI` camera module, and a `ZJY154KC-IF17` 1.54-inch module driven by an **ST7789VW** | ⚠ **Third-party copyright, mirrored by Espressif with no stated licence** — redistribution status `unknown`; retained for internal engineering reference only. The last two upstream filenames are **Chinese and must be percent-encoded** in the request (`ST7789VW%E8%8A%AF%E7%89%87%E6%89%8B%E5%86%8C.pdf`, `%E8%83%B6%E9%93%81%E4%B8%80%E4%BD%93ZJY154KC-IF17.pdf`); both were renamed to portable ASCII on retrieval. Note the **third distinct path prefix** on this host: `/AE/esp-dev-kits/`, unrelated to `/dl/schematics/` and `/schematics/` | [`../shared-artifacts/`](../shared-artifacts/) — see [its manifest](../shared-artifacts/sources.md) |
| P4E-6 | esp-dev-kits documentation, ESP32-P4 target, PDF build | Espressif Systems | primary | manual | <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp-dev-kits-en-master-esp32p4.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | release `master`; title page **2026-08-23** | An offline copy of every P4 board user guide — **including this board's, whose HTML URL has since moved** (§4) | ⚠ **`master` build — a moving target.** **Archived out of the repository 2026-08-24**; 30,482,003 B, SHA-256 `04d75d2acda82c8f5136bfed4d1732e7e4bd095437e2ecacce271374d8f8538c`. Provenance and verified URLs: [`ARCHIVED-FRAMEWORK-GUIDES.md`](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) | archived → `archive/hardware-doc/devices/espressif/shared-artifacts/` |
| P4E-7 | Failed-download probe log | this repository | — (internal) | — | [`../../../component-download-failures.txt`](../../../component-download-failures.txt) | 2026-08-21 | — | The probes showing the successor's *"ESP32-P4X-EYE Reference Design (ZIP)"* link does not resolve for any filename variant — the reason this EOL record exists | Negative result, retained so the probes are not repeated | [`../../../component-download-failures.txt`](../../../component-download-failures.txt) |

---

## 4. Retrieval findings

### P4E-1's URL is now a 404 — the EOL guides moved

Probed **2026-08-28**:

| URL | Result |
|---|---|
| `…/esp32p4/eol/esp32-p4-eye/user_guide.html` *(as cited 2026-08-21)* | **HTTP 404**, 14,039 B soft-404 shell |
| `…/esp32p4/esp32-p4-eye/user_guide.html` *(current)* | **HTTP 200**, 41,557 B |
| `…/esp32p4/eol/esp32-p4-function-ev-board/user_guide.html` *(the sibling EOL board)* | **HTTP 404**, 14,039 B |
| `…/esp32p4/esp32-p4-function-ev-board/user_guide.html` *(current)* | **HTTP 200**, 49,519 B |
| `…/esp32p4/eol/eol-boards.html` *(the index)* | **HTTP 200** — **did not move** |

Espressif dropped the `eol/` path segment from the **board guides** while leaving the **EOL index
page** in place. The migration was found by fetching that index and reading its outbound links,
which now point at `../esp32-p4-eye/index.html` and `../esp32-p4-function-ev-board/index.html`.

Two aggravating factors:

1. **It is not a redirect.** The old path returns a 404 shell *with* HTTP status 404 — a link
   checker catches it, but a fetcher that ignores status codes silently stores 14 KB of navigation
   chrome. Same soft-404 shell family as the unresolvable P4X reference-design ZIPs (13,745 B at
   the 2026-08-21 pass, 14,039 B now).
2. **No Internet Archive capture of either old URL exists** — Wayback availability API on
   2026-08-28 returned `{"archived_snapshots": {}}` for both. Without P4E-6 the originally-cited
   content would be unrecoverable at that address.

The `esp-dev-kits` source commit also advanced from **`f6f80ab`** to **`df877cb`**, so the current
pages are not guaranteed to match what was mined. **No content was re-mined in this pass** — only
availability was re-checked, and nothing in [`README.md`](README.md) was changed on the strength of
the new URLs.

This is a reusable Espressif portal trap and belongs in the
[vendor sourcing guide](../../../vendors/espressif/README.md); it has **not** been added there in
this pass, which was scoped to device-level source manifests.

### `dl.espressif.com` is unaffected

Both design files (P4E-4) and all four mirrored component datasheets (P4E-5) returned HTTP 206 with
`application/pdf` on 2026-08-28, including the two percent-encoded Chinese filenames. The download
host has been markedly more stable than the documentation host.

---

## 5. Evidence notes and known gaps

**The version mismatch is the headline caveat.** P4E-4a is V2.3 (2025-04-16) and P4E-4b is V2.2
(2025-03-14). They are the only two design files published, they describe **different board
versions**, and there is no changelog. Any claim that reads a net off one and a placement off the
other is unsound.

**This board is documented as an evidence donor.** Its own status is EOL. The record exists because
Espressif publishes *its* schematic and layout and not the successor's — and because its Related
Documents list is **longer** than the successor's, which dropped the schematic and PCB in favour of
a broken ZIP link. That is a regression in published detail, not an improvement.

**No performance, pricing, availability, community or media research was done.** The record is
purely a documentation and design-file record.

**No component records were created from P4E-5.** The OV2710, ST7789VW, HDF2710-47 and ZJY154KC-IF17
identities are established but have no `components/` entries.

**Retrieval-date convention.** `2026-08-21` rows were mined then. `2026-08-28` marks **status
re-verification only** — HTTP code and content type. Content was not re-fetched, re-hashed or
re-compared.

---

## 6. Related records

- [ESP32-P4X-EYE](../esp32-p4x-eye/README.md) · [its sources](../esp32-p4x-eye/sources.md) — the successor these files are used as evidence for
- [ESP32-P4-Function-EV-Board (EOL)](../esp32-p4-function-ev-board/README.md) · [its sources](../esp32-p4-function-ev-board/sources.md) — affected by the same URL migration
- [Shared artifacts](../shared-artifacts/README.md) · [their sources](../shared-artifacts/sources.md)
- [ESP32-P4 component record](../../../components/espressif/esp32-p4/README.md)
- [Espressif vendor sourcing guide](../../../vendors/espressif/README.md)
