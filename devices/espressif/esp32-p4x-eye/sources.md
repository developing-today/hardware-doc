# ESP32-P4X-EYE — source manifest

> Sources for the current, enclosed ESP32-P4 hand-held **vision** board.
> Originally retrieved **2026-08-21**; URLs re-verified **2026-08-28**.
> Local paths are relative to this device folder; a dash means link-only.
>
> ⚠ **This board has no board-specific local artifacts.** Espressif publishes no schematic or PCB
> layout that resolves for it. The design evidence in the record is a **documented substitution**
> from the EOL predecessor — see [§3](#3-substituted-evidence--the-eol-predecessor).

`Class` is one of **primary** / **authorized mirror** / **credible mirror** / **standard** / **community**.

This file supersedes and expands [§7 of `README.md`](README.md#7-sources); the `S1`–`S4` IDs used on
that page map onto `PXE-1`–`PXE-4` here.

---

## 1. Primary documentation

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| PXE-1 (=S1) | ESP32-P4X-EYE User Guide | Espressif Systems | primary | manual | <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4x-eye/user_guide.html> | 2026-08-21; HTTP 200 2026-08-28 | esp-dev-kits `latest`; source commit `f6f80ab` at retrieval, **`df877cb` on 2026-08-28** | **Almost the entire record**: the top- and bottom-PCB component tables (§2), the **ESP32-C6-MINI-1U** companion reached only via **bare test points**, 16 MB SPI flash, the 1.54-inch 240×240 SPI LCD, MicroSD in 4-line SDIO **or** SPI, the USB 2.0 HS **device-only** port and separate Debug port, the fill light, rotary encoder, digital microphone, battery connector and two-colour charge indicator, the chip-revision statement, the target-application positioning, and the **factory-demo feature list including face/pedestrian detection and YOLOv11-nano** | ⚠ **`latest` is an unstable path** and the source commit has already advanced, so this URL is not a pin. **Vendor claims, not measurements** — Espressif publishes **no fps, latency or accuracy figures** for the YOLOv11-nano demo, and **no battery-life figure** for the board. None are inferred in the record | – |
| PXE-2 (=S2) | ESP32-P4-EYE User Guide (predecessor) | Espressif Systems | primary | manual | **current:** <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4-eye/user_guide.html> · **as cited 2026-08-21:** `…/esp32p4/eol/esp32-p4-eye/user_guide.html` | 2026-08-21; re-verified 2026-08-28 | esp-dev-kits `latest` | The predecessor's design-file URLs (used in §3) and its *"No previous versions available"* statement | ⚠ **The cited URL is now HTTP 404** — the EOL guides moved. Full migration finding in [the predecessor's manifest §4](../esp32-p4-eye/sources.md#4-retrieval-findings). ⚠ Also note the predecessor's Related Documents list is **longer** than this board's: it publishes schematic and PCB where this board offers only a broken ZIP link | – |
| PXE-3 (=S3) | Espressif DevKits product catalogue | Espressif Systems | primary | store listing | <https://www.espressif.com/en/products/devkits> | 2026-08-21; HTTP 200 2026-08-28 (465,290 B) | as served, undated | The marketing blurb: *"ESP32-P4-based vision development board supporting MIPI-CSI camera and USB 2.0 High-Speed, integrating microphone and MicroSD slot"* | Undated marketing page with no version to pin. Adds nothing PXE-1 does not already state more precisely | – |

## 2. Component documentation mirrored by Espressif

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| PXE-4a (=S4) | OV2710 camera-sensor overview | OmniVision, via Espressif | authorized mirror | datasheet | <https://dl.espressif.com/AE/esp-dev-kits/ov2710pbv1.1web.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | v1.1 per filename | The camera sensor identity behind the "2 MP MIPI-CSI" specification | ⚠ Third-party copyright, mirrored with **no stated licence** — redistribution status `unknown`; retained for internal engineering reference only. A product *brief*, not a full datasheet. 159,720 B, SHA-256 `d34890622db7f06324242329e6b5193597c0088ffe9a2765194166ae3b201912` | [`../shared-artifacts/ov2710-camera-module-datasheet.pdf`](../shared-artifacts/ov2710-camera-module-datasheet.pdf) |
| PXE-4b (=S4) | HDF2710-47-MIPI camera-module specification | module vendor, via Espressif | authorized mirror | datasheet | <https://dl.espressif.com/AE/esp-dev-kits/HDF2710-47-MIPI-V2.0.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | **V2.0** per filename | The **camera module as fitted** — the assembly around the OV2710, including the manually adjustable focus | Same third-party / `unknown` licence position. 246,656 B, SHA-256 `050c43a50e45e77436dc99486098614f4ee04511c3586d702cab28b506868ecc` | [`../shared-artifacts/hdf2710-47-mipi-camera-module-spec.pdf`](../shared-artifacts/hdf2710-47-mipi-camera-module-spec.pdf) |
| PXE-4c (=S4) | ST7789VW LCD-controller datasheet | Sitronix, via Espressif | authorized mirror | datasheet | `https://dl.espressif.com/AE/esp-dev-kits/ST7789VW芯片手册.pdf` (percent-encoded: `ST7789VW%E8%8A%AF%E7%89%87%E6%89%8B%E5%86%8C.pdf`) | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | as served | The LCD controller driving the 1.54-inch 240×240 SPI panel | ⚠ **Upstream filename is Chinese and must be percent-encoded** in the request; renamed to portable ASCII on retrieval (`芯片手册` = "chip manual"). Third-party copyright, `unknown` redistribution. 3,135,599 B, SHA-256 `1f9e956057e3909c0714bdab9e682205e03cf52adefd5b4a01093fa3167d398b` | [`../../../components/sitronix/st7789vw/artifacts/st7789vw-datasheet.pdf`](../../../components/sitronix/st7789vw/artifacts/st7789vw-datasheet.pdf) |
| PXE-4d (=S4) | ZJY154KC-IF17 1.54-inch LCD module specification | module vendor, via Espressif | authorized mirror | datasheet | `https://dl.espressif.com/AE/esp-dev-kits/胶铁一体ZJY154KC-IF17.pdf` (percent-encoded: `%E8%83%B6%E9%93%81%E4%B8%80%E4%BD%93ZJY154KC-IF17.pdf`) | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | as served | The **display module as fitted**, around the ST7789VW | ⚠ Chinese upstream filename, percent-encoding required, renamed on retrieval (`胶铁一体` = "adhesive-and-metal integrated", describing the module's bonding construction). Third-party copyright, `unknown` redistribution. 1,290,995 B, SHA-256 `c323a0f082bea4a99431be5d54f2f3305d7489432e18c97d25aa23627bf3bfc5` | [`../shared-artifacts/zjy154kc-if17-lcd-module-spec.pdf`](../shared-artifacts/zjy154kc-if17-lcd-module-spec.pdf) |

All four sit under a **third distinct path prefix** on `dl.espressif.com` — `/AE/esp-dev-kits/` —
unrelated to `/dl/schematics/` and `/schematics/`. Espressif uses at least three unconnected URL
schemes on this one host; see [`../shared-artifacts/sources.md`](../shared-artifacts/sources.md).

## 3. Substituted evidence — the EOL predecessor

**Espressif publishes no direct schematic or PCB PDF for this board.** Its user guide offers only an
*"ESP32-P4X-EYE Reference Design (ZIP)"* link, and that link **does not resolve** for any filename
variant tried — every one returns the documentation platform's 13,745 B soft-404 shell. Probes are
recorded in [`component-download-failures.txt`](../../../component-download-failures.txt).

Because PXE-1 states the two boards differ **only in the fitted silicon revision**, the
predecessor's published files are used as the closest available primary evidence.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| PXE-5 | ESP32-P4-EYE main-board schematic **V2.3** and PCB layout **V2.2** | Espressif Systems | primary | schematic | <https://dl.espressif.com/AE/esp-dev-kits/SCH_ESP32-P4-EYE-MB_V2.3_20250416.pdf> · <https://dl.espressif.com/AE/esp-dev-kits/PCB_ESP32-P4-EYE-MB_V2.2_20250314.pdf> | 2026-08-21; both HTTP 206 `application/pdf` 2026-08-28 | **V2.3 / V2.2** — *different board versions* | The circuitry and layout used as this board's design evidence | ⚠ **A double caveat.** First, this is a **substitution**: "Espressif describes the difference as a chip-revision change" is not "identical schematic". Second, the two files are themselves **from different board revisions** with no published changelog — they do not describe the same artefact. Hashes and detail: [predecessor manifest §2](../esp32-p4-eye/sources.md#2-primary-design-files) | [`../esp32-p4-eye/artifacts/`](../esp32-p4-eye/artifacts/) |
| PXE-6 | Failed-download probe log | this repository | — (internal) | — | [`../../../component-download-failures.txt`](../../../component-download-failures.txt) | 2026-08-21 | — | That the reference-design ZIP is unrecoverable — a **negative result** retained so the probes are not repeated | Records the soft-404 shell size, the reliable signature of this failure mode | [`../../../component-download-failures.txt`](../../../component-download-failures.txt) |

## 4. Software and firmware references

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| PXE-7 | `espressif/esp-dev-kits` — `examples/esp32-p4-eye/examples/factory_demo` | Espressif Systems | primary | repository | <https://github.com/espressif/esp-dev-kits> | 2026-08-21; HTTP 200 2026-08-28 | commit `f6f80ab` at retrieval | The **single official example** for this board, and the concrete demonstration of the P4's AI capability: photo/timed capture, video recording, album preview, USB SD-card mounting, image-parameter configuration, and face / pedestrian / **YOLOv11-nano** detection | ⚠ Example directory named after the **pre-P4X** board. **Not cloned, built or run**; nothing retained locally. **No performance figures published or measured** — the demo's existence is established, its speed is not | – |
| PXE-8 | esp-dev-kits documentation, ESP32-P4 target, PDF build | Espressif Systems | primary | manual | <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp-dev-kits-en-master-esp32p4.pdf> | 2026-08-21; HTTP 206 `application/pdf` 2026-08-28 | release `master`; title page **2026-08-23** | An offline copy of every P4 board user guide, **including the EOL guides whose HTML URLs have since moved** | ⚠ **`master` build — a moving target.** **Archived out of the repository 2026-08-24**; 30,482,003 B, SHA-256 `04d75d2acda82c8f5136bfed4d1732e7e4bd095437e2ecacce271374d8f8538c`. Provenance: [`ARCHIVED-FRAMEWORK-GUIDES.md`](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) | archived → `archive/devices/espressif/shared-artifacts/` |

---

## 5. Retrieval findings

**One cited URL is dead: PXE-2.** The EOL user guides moved out of the `eol/` path segment between
2026-08-21 and 2026-08-28. The old path returns HTTP 404 with a 14,039 B soft-404 shell and has **no
Wayback capture**. Documented once in
[the predecessor's manifest §4](../esp32-p4-eye/sources.md#4-retrieval-findings).

**Everything else resolves.** PXE-1, PXE-3 and PXE-7 returned HTTP 200; PXE-4a–d, PXE-5 and PXE-8
returned HTTP 206 with `application/pdf`, **including both percent-encoded Chinese filenames**.

**The documentation host is the unstable one.** Every failure in this record — the unresolvable
reference-design ZIP, the soft-404 shells, the EOL migration — is on `docs.espressif.com`.
`dl.espressif.com` has served every artifact reliably across both passes.

**The source commit advanced** from `f6f80ab` to `df877cb`. **No content was re-mined in this pass.**

---

## 6. Evidence notes and known gaps

**This record is built almost entirely on PXE-1.** There is no second independent source for the
component tables, the test-point-only C6 access, the SD protocol options or the factory-demo feature
list, and none was sought.

**No board-specific artifact exists.** All design evidence is the §3 substitution, which carries two
stacked uncertainties — the chip-revision substitution *and* the predecessor's own V2.3/V2.2
schematic-vs-layout mismatch. Reproduce both labels, not just the conclusion.

**No performance figure of any kind exists.** YOLOv11-nano on-device is the most interesting claim
in the record and **no fps, latency or accuracy number is published by Espressif or measured here**.
Likewise no battery-life figure exists despite this being the only meaningfully portable P4 board.

**No BOM, Gerbers, dimensions, assembly drawing or EDA source** are published for either this board
or its predecessor, and there are **no adapter-board reference designs** for the EYE family because
there are no adapter boards.

**No component records were created** for the OV2710, ST7789VW, HDF2710-47 or ZJY154KC-IF17
identities established by PXE-4.

**No pricing, availability, community, media or example-validation research was done.**

**Retrieval-date convention.** `2026-08-21` rows were mined then. `2026-08-28` marks **status
re-verification only** — HTTP code and content type. Content was not re-fetched, re-hashed or
re-compared.

---

## 7. Related records

- [ESP32-P4-EYE (EOL)](../esp32-p4-eye/README.md) · [its sources](../esp32-p4-eye/sources.md) — **the source of this board's design evidence**
- [ESP32-P4X-Function-EV-Board](../esp32-p4x-function-ev-board/README.md) · [its sources](../esp32-p4x-function-ev-board/sources.md)
- [ESP32-P4X-C5-Function-EV-Board](../esp32-p4x-c5-function-ev-board/README.md) · [its sources](../esp32-p4x-c5-function-ev-board/sources.md)
- [Shared artifacts](../shared-artifacts/README.md) · [their sources](../shared-artifacts/sources.md)
- [ESP32-P4 component record](../../../components/espressif/esp32-p4/README.md)
- [Espressif vendor sourcing guide](../../../vendors/espressif/README.md)
