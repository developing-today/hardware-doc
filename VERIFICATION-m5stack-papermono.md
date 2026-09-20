# Verification report — M5Stack PaperMono research pass

**Date:** 2026-09-01 · **Subject:** `devices/m5stack/papermono`,
`devices/m5stack/papermono-lite`, 21 component records, 2 vendor guides,
3 reusable tools.

**Headline caveat, stated once and plainly: there was no PaperMono hardware in
this pass.** No command was executed against a device, nothing was flashed,
nothing was measured. Every behavioural claim in the record is `inferred`,
`reported-working` (vendor-documented), or read from vendor source at a cited
`file:line`. Nothing is `executed-success` except operations on files.

## Result

| Check | Result |
|---|---|
| Authored Markdown | 60+ files, ~25,000 lines |
| Artifacts retained | 23 files, 55,405,315 bytes |
| Broken relative links in authored records | **0** |
| PDF/binary magic validation | **23/23 pass** (`%PDF-` / `0xE9`) |
| SHA-256 computed for retained artifacts | **23/23** |
| Acquisition manifest entries | 24 |
| `fetch.py --verify-only` | **pass**, 14 cached, 0 failed, exit 0 |
| Duplicate content among new artifacts | **none** |
| `tools/audit_archive.py` — losable artifacts | **0** |
| Filenames portable ASCII | yes |
| Failed downloads saved under misleading extensions | **none** — `fetch.py` refuses this structurally |

Bundled upstream Markdown was **excluded** from link checking, as the method
allows. A repo-wide check found 67 broken links, all inside vendored upstream
trees (`waveshare/.../source-snapshots/`, `seeed-studio/.../wiki-snapshot/`,
`nicolai-electronics/tanmatsu/artifacts/`) that predate this pass. **Zero broken
links exist in authored records anywhere in the repository.**

## What the evidence actually rests on

The most load-bearing source is the official schematic PDF. Because M5Stack's
`M5_Hardware` repository contains **no C153 entry** (verified at commit
`a240115c`, 2026-08-17), there is no published netlist, so the schematic is the
only primary machine-readable-ish evidence available.

It was mined by recovering Altium's invisible `CO`/`PI`/`NL` marker text from
the PDF and pairing it by coordinate — three reusable tools now in
[`tools/`](tools/): `altium_pdf_netlist.py`, `altium_pdf_pin_table.py`,
`altium_pdf_render_sheet.py`. This yielded a **230-designator census** and full
pin tables for the ESP32-S3, both custom chips, the flash and every connector.

**The method's limits were hit and are recorded.** Adjacency is not
connectivity: unlabelled wire-only nets are invisible to it, and on the dense
power sheet it produced readings that were wrong (it initially mis-attributed
the charger designator). Every pin assertion was therefore cross-checked either
by rendering the sheet at 200 dpi and reading it, or against a second
independent source — vendor firmware, the vendor product page, or the DKE panel
manual's own pinout, which matched the schematic's e-paper FPC position for
position. A parser bug that silently ate pin names (`GPIO0` parsed as a marker)
was found and fixed before any table was published.

## Claims examined and refuted during the pass

Recorded because a refuted hypothesis that is not written down gets
re-investigated:

1. **"The vendor's PaperMono page is wrong about `PYG3_BL_PWM`."** Refuted by
   schematic sheets 2 and 4. Both vendor pages are correct; they quote different
   layers of the drawing. See
   [`pin-naming-and-the-pyg-ambiguity.md`](devices/m5stack/papermono/pin-naming-and-the-pyg-ambiguity.md).
2. **"The NFC matching network is undocumented."** Refuted — the released NFC
   sheet `2/2` carries the complete front end. Sheet `1/2` is genuinely absent.
3. **"The RTC is on `3V3_L1`."** This is what M5Stack's own block diagram says.
   Refuted by reading sheet 4: `VBAT`/`VIO`/`VDD`/`VOUT` are all on `3V3_L0`.
   The vendor block diagram is wrong; the board is right.
4. **"The restock delay is an e-ink driver IC shortage."** The cited post and
   its full reply chain were retrieved; the reason does not appear in them.
   Hearsay.
5. **"PaperMono supersedes PaperS3."** Contradicted by the vendor's own
   specifications — fewer pixels, fewer grey levels, smaller battery, no
   expansion port.

Equally recorded: the vendor's product-page pin tables were checked exhaustively
and found **correct**, with two omissions and no errors. Confirming existing
documentation is a result.

## Conflicts left open

Ten unresolved conflicts and ten gaps are itemised in
[`gaps-and-conflicts.md`](devices/m5stack/papermono/gaps-and-conflicts.md). The
ones most worth someone's attention:

- **C1** panel manual says `2Grey Level`; M5Stack markets and ships 4-level grey
- **C3** M5GFX drives the panel at 40 MHz against a 20 MHz maximum stated
  independently by both Solomon Systech and DKE — the best candidate for the
  refresh instability M5Stack itself warns about
- **C4** the M5IOE1's actual I²C address `0x4F` is absent from its own manual
- **C13** M5Unified `getVoltLow()` reads `VBLF`, not `VLF` — returns `false` on
  exactly the occasion it is used for
- **G7** no power or battery-life figure exists anywhere, vendor or independent

## Known incompleteness

Honest gaps in this pass, not oversights discovered later:

- **No imagery.** No product, teardown or PCB photograph is retained. Vendor
  imagery is not licensed for redistribution and no independent teardown existed
  at the snapshot date. Recorded rather than filled with unattributed images.
- **Closed since first writing.** `performance.md` and the `examples/`
  catalogue now exist. All 43 third-party repositories are pinned to a commit,
  which closes the recorded defect that citations could not be re-resolved.
  Still true: **no example was built, flashed or run**, and none can be until
  hardware exists.
- **Three datasheets are unobtainable** (`CN4040M000157A530001`,
  `LMD4737T261-AC02`, `RS-C1415MBAR`), recorded `lost` with search ledgers.
- ~~Third-party repository citations are unpinned~~ — **fixed 2026-09-01**:
  43 of 43 repositories resolved and pinned to a full commit SHA in
  `examples/catalog.json`. None were gone, private or archived.
- **`scratch/m5stack-papermono/` is uncommitted** at the time of writing: raw
  page captures, 200 dpi sheet renders, panel-manual page images, per-designator
  pin tables and the three subagent FINDINGS files. It belongs in the archive
  repository.

## Scope statement

This is a **reproducible broad-coverage snapshot dated 2026-09-01**, not a claim
that no other resource exists. Search cutoff 2026-09-01; 140 distinct queries
across 7 passes are logged in
[`research-log.md`](devices/m5stack/papermono/research-log.md). The stopping
criterion was met: two consecutive broad passes returned only vendor marketing
copy and duplicates. The product was eleven days old, out of stock since launch
day, and had attracted zero written independent reviews — so the ceiling here is
set by the world, not by the search.


## Second review pass — 2026-09-01

A review pass after the initial write-up found and fixed **four factual errors in
documents written during the first pass**, all discovered by reading the
schematic more carefully rather than by new retrieval:

| Was | Is | Where it was wrong |
|---|---|---|
| Battery "NTC-sensed" at `J2` | `J2` is 2-contact, power only. The `100K-RNTC` is **`R15` on the mainboard** at the IP2315's `NTC` pin | `README.md`, `pinouts-and-buses.md`, `power-architecture.md` |
| One CC pulldown (`R14`) | **Two** — `R4` on CC1 *and* `R14` on CC2 | `power-architecture.md` |
| USB-C receptacle is `U1` sheet 2 | Its designator is the bare string **`USB`** | `pinouts-and-buses.md` |
| `J6` has 16 pins | **12 contacts + 4 tabs** | `pinouts-and-buses.md` |

Two open questions closed: the IP2315 charge-programming resistor is **`R17` =
15 kΩ**, and the reported missing `N1` designator was a **parser artifact** —
`N`-series designators do not exist on this board, and the only genuine gaps are
`R46`, `R48`, `R55`–`R57`.

Seven new conflicts were recorded (C18–C24), including that this record's own
`README.md` recommends a Waveshare e-paper alternative the knowledge base cannot
support — all four Waveshare records here are LCD boards.

**The correction rate is the finding.** Four errors in the first pass's own
output, all in tables that looked authoritative, all caught only by re-reading
the primary artifact. The automated schematic extraction is a reading aid; where
this record's claims rest on it alone they are marked `inferred`, and that
marking should be taken seriously.


## Third review pass — 2026-09-01/02

### Closed
- **C24 (Waveshare recommendation unbacked)** — closed by writing
  [`devices/waveshare/esp32-s3-epaper-3.97`](devices/waveshare/esp32-s3-epaper-3.97/README.md),
  the knowledge base's first Waveshare **e-paper** board. Same SoC, same 8 MB/16 MB
  memory, same 3.97" 4-grey panel, **active area matching the PaperMono's DKE panel
  to 0.01 mm** — the two boards plausibly share a panel (`inferred`, not
  established: Waveshare names neither supplier nor controller).
- **Example survey** — `examples/{catalog.json,best.md,search-log.md}` written.
  **43 of 43 repositories resolved and pinned to full commit SHAs**; none gone or
  private. Ten selected, including one deliberate negative
  (`free-ink-on-paper-mono`: demonstrates FreeInk on this board, carries a
  relevant partial-refresh patch, and has **no LICENSE file** — all rights
  reserved, must not be copied).

### Added
- **Device-independent guides** at [`guides/nfc`](guides/nfc/README.md) and
  [`guides/lora`](guides/lora/README.md), filling the layer the method calls for
  between component records and device feature guides. Both bidirectionally
  linked to `papermono/features/{nfc,lora}.md` with explicit applicability
  statements ("applies with deltas", deltas enumerated).
- [`software/`](software/README.md) tree with a taxonomy (libraries / frameworks
  / applications / tooling / ecosystems) and its first record,
  [CrossPlay](software/applications/crossplay/README.md) — a CrossPoint Reader
  fork that **carries `papermono` build environments**, now cross-referenced from
  the PaperMono project population as Class P (support present in build config,
  **nobody has reported running it**).

### New vendor trap recorded
Waveshare's **MediaWiki `api.php` and `index.php` return a PHP fatal parse error
with HTTP 200**. This breaks the `action=parse&prop=wikitext` route that this
knowledge base's own Waveshare vendor guide recommends, and it fails in the worst
way — a success status with an error body. Rendered pretty URLs still work; the
storefront search is the working enumeration route. Dated and recorded in
[`vendors/waveshare`](vendors/waveshare/README.md).

### Ledger state
15 resolved (R), 25 open conflicts (C), 10 gaps (G). Record: 41 markdown files,
11,620 lines. `acquisition/fetch.py --verify-only` passes, 0 failed.
Link check: 457 authored markdown files, **0 broken links** — the six remaining
repository-wide are all inside vendored upstream trees and are excluded by the
method.

### Still open, and honestly so
- **No hardware.** Nothing in this record has been built, flashed or measured.
- **NFC and LoRa each rest on a single artifact** — the vendor's own demo. No
  independent implementation of either exists for this board, so an error there
  propagates here uncontradicted.
- **No imagery retained**; no power, battery-life or thermal figure exists from
  any source.
- **Chinese-language platforms (Gitee, Bilibili, CSDN) were never searched** —
  the largest known hole in the project survey, and the first place a later pass
  should look.

## Fourth review pass — 2026-09-04

### Carried-over technical followups, all three closed

| Followup | Outcome |
|---|---|
| **SX1262 G4** — are RadioLib's SX126x §15 errata workarounds applied at the *pinned* 7.2.1, not just master? | **Resolved: all four are.** `rxGain`/sensitivity ×4, `fixPaClamping` ×1 (+×3 in `SX1262.cpp`, **×0 in `SX1261.cpp`**, matching the datasheet's "SX1262 only" note), `fixImplicitTimeout` ×3, `fixInvertedIQ` ×2. Read from tag `7.2.1`, tag object `b91c6af1…` |
| **RadioLib licence** — "LGPL-3.0 upstream" vs MIT | **Resolved: MIT**, and has been since 2018. `license.txt` (1,068 B) and `library.json` both say MIT at 7.2.1. The LGPL claim is withdrawn |
| **ST25R3916 matching network** | **Recorded as an open observation.** The inferred `L1/L2`+`C6/C8` pairing gives a ≈11.7 MHz corner — *below* the 13.56 MHz carrier, the wrong side for an EMC low-pass. Pairing with the 220 pF group gives ≈20.6 MHz, which is conventional. Most likely the inference is wrong, not the board |

The RadioLib licence case is a lesson worth keeping: it survived two passes
because a probe for a file named `LICENSE` returned 404 — the file is
`license.txt`, lowercase. **A 404 on a guessed filename is not evidence of
absence.** The same mistake produced the Waveshare "no documentation" error
recorded in the third pass.

### Software tree — three records now written

`software/` gained a taxonomy (libraries / frameworks / applications / tooling /
ecosystems) and its first substantive records:

- [**CrossPoint Reader**](software/applications/crosspoint-reader/README.md) — ★7,538, 1,621 forks
- [**FreeInk SDK**](software/frameworks/freeink-sdk/README.md) — its submodule dependency
- [**CrossPlay**](software/applications/crossplay/README.md) — a fork, with patch-portability analysis

**Two findings bear directly on this device record:**

1. **Upstream CrossPoint ships `[env:papermono]`** (plus `-gh_release` and
   `-gh_release_rc`). PaperMono support is not fork-only — the 7,500-star upstream
   builds for this board.
2. **A CrossPoint plugin could not implement NFC or LoRa.** Per a carried-over
   analysis, the plugin system is browser JavaScript plus JSON manifests with no
   code running on the MCU and no peripheral access at all. Adding radios would
   require a fork or an upstream feature, not a plugin. Flagged for
   re-verification; the finding is `reported-working`, not confirmed in this pass.

### Also settled

`crosspoint-reader/.gitmodules` proves **CrossPoint consumes FreeInk SDK as a git
submodule** — the dependency direction question is closed. The chronology is the
counterintuitive part: **CrossPoint (2025-12-03) predates FreeInk (2026-06-03)**;
FreeInk is a re-architecture of the SDK CrossPoint already used, itself derived
from `open-x4-epaper/community-sdk` with SSD1677/UC8253 LUTs credited to
CidVonHighwind.

### State
Link check across my scope: **57 files, 0 broken.** `fetch.py --verify-only`
passes. Conflict ledger: C23 closed this session alongside the three above.
