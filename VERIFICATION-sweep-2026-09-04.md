# Verification — seven-session device sweep, 2026-09-04 → 2026-09-07

Umbrella report for the parallel research pass covering **Xteink**, **M5Stack DinMeter /
Cardputer / Cardputer radio expansions**, **LilyGO T-Display K230**, **LilyGO T-Display-S3 and
variants**, and the **Semtech LoRa generation lineage**.

Per-session reports carry the detail and are authoritative for their own subject:
[Xteink](VERIFICATION-xteink.md) ·
[M5Stack DinMeter](VERIFICATION-m5stack-dinmeter.md) ·
[M5Stack Cardputer](VERIFICATION-m5stack-cardputer.md) ·
[LilyGO T-Display K230](VERIFICATION-lilygo-t-display-k230.md).
The index merge and its parked corrections are in
[`research/passes/index-merge/README.md`](research/passes/index-merge/README.md).

---

## 1. The headline caveat

⚠ **No claim in this sweep was verified on physical hardware.** No board was purchased,
powered, flashed or probed. Every build, flash, pinout and behavioural claim is labelled
`reported-working`, `inferred` or `not-tested` in its own record; the count of
`executed-success` **on-device** claims across all seven sessions is **zero**, and each session
states this in its own words.

What *was* executed locally: HTTP retrieval, checksum and magic-byte validation, PDF text
extraction, repository cloning and log/tree inspection via the GitHub API, and the link and
deletion audits below.

## 2. Scope delivered

| | Count |
|---|---|
| Device records created | **38** across 3 new manufacturer trees (`xteink/` 6, `lilygo/` 16, `m5stack/` 16 — of which 2 pre-existed) |
| Authored Markdown files added (excl. `artifacts/`, excl. `scratch/`) | **469** |
| Component records in the library after the sweep | **201** |
| Vendor sourcing guides after the sweep | **37**, incl. new `canaan/`, `lilygo/`, `semtech/` |
| Cross-cutting guides added | **6** — [LoRa radio generations](guides/hardware/lora-radio-generations.md), [parallel 8080 LCD buses](guides/hardware/parallel-8080-lcd-buses.md), [RISC-V and vendor-SDK toolchains on NixOS](guides/nixos/riscv-and-vendor-sdk-toolchains.md), [adding LoRa/NFC/sidelight to e-ink firmware](guides/hardware/adding-lora-nfc-and-sidelight-to-eink-firmware.md), [SoC choice for battery e-ink devices](guides/hardware/soc-choice-for-battery-eink-devices.md), [handheld and e-ink device landscape](guides/markets/handheld-and-eink-device-landscape-2026-09.md) |
| Binary artifacts retained under `artifacts/` | **161** |

## 3. Machine-checked results

| Check | Method | Result |
|---|---|---|
| Relative-link integrity | Every inline Markdown link in every authored `.md` outside `artifacts/`, `archive/` and `scratch/`, fenced code blocks stripped, anchors ignored, percent-decoded | **10 387 links checked · 1 broken** |
| The one broken link | `devices/seeed-studio/xiao-esp32s3-sense/examples/selected/XIAO_Webcam/README.md → docs/xiao-esp32s3-sense.jpg?raw=true` | **Pre-existing and out of scope** — vendored upstream README, preserved as supplied. The root [`README.md`](README.md) already states bundled upstream Markdown is not claimed to be link-clean. Not introduced by this sweep and deliberately not "fixed", since editing it would diverge the vendored copy from upstream |
| Artifact type validation | Magic bytes compared against extension for every typed artifact added in the sweep (`%PDF`, `PK`, `\x89PNG`, `\xff\xd8\xff`, `RIFF`, `\x1f\x8b`) | **61 typed artifacts · 0 mismatches** — no HTML error page saved under a document extension |
| Device-record orphans | Every `devices/<vendor>/<board>/` directory grepped for an inbound link from [`devices/README.md`](devices/README.md) | **0 orphans.** One was found and fixed: `nicolai-electronics/tanmatsu`, orphaned since the 2026-08-24 pass — see §5 |
| Deletion audit on shared files | `git diff -- <file> \| grep -c '^-[^-]'` for all 25 shared files touched by the merge and cross-link passes | **0 deletions on every file** |
| Git state | `git rev-parse HEAD` before and after | **`4aa02e1030b3b0861e6fc34f23fa2113ec80d324`, unchanged.** 91 pre-existing staged paths from a concurrent session left intact; nothing added, committed, stashed or reset |

## 4. Concurrency discipline

Seven research sessions plus two integration sessions ran in parallel against this repository
while a separate session worked on the PaperMono and `software/` trees.

- Every research session was **forbidden from editing shared indexes** and instead wrote
  ready-to-paste Markdown to `scratch/<subject>/index-fragments.md`. Those seven fragment files
  are retained as the audit trail.
- Every edit to a pre-existing file was **append-only** and preceded by a `find <file> -mmin -15`
  liveness check. One file (`vendors/lilygo/README.md`) was found live, deferred, and applied
  18 minutes later.
- Where a session found another session's record to be **wrong**, it did not overwrite it. It
  added a dated note beneath the original line, leaving the original visible, and filed the
  item in [`research/passes/index-merge/corrections-requiring-review.md`](research/passes/index-merge/corrections-requiring-review.md)
  for a human to adjudicate. **Six corrections are parked there and none has been applied.**

## 5. The one repository defect fixed in passing

`devices/nicolai-electronics/tanmatsu/` — a substantial record from the 2026-08-24 pass — had
**never been linked from [`devices/README.md`](devices/README.md)** and was unreachable by
navigation. A `## Nicolai Electronics` section was added on 2026-09-07, written only from the
record's own opening paragraphs. **The record itself was neither reviewed nor modified**, and it
remains the authority on its own contents.

## 6. What this sweep does not establish

- **No hardware.** See §1. In particular, no pinout, no flash command and no current-draw figure
  has been confirmed against a physical board.
- **No net-level schematic tracing** for the LilyGO family — `poppler` was unavailable, and the
  session names this as the largest cheap improvement available.
- **The Xteink X4 Pro record traces substantially to one commit.** No teardown, no firmware dump
  and no price-independent corroboration were obtained for the family's flagship.
- **`components/canaan/k230`** documents a SoC whose vendor SDK the sessions read but never
  built; the NixOS toolchain routes in
  [`guides/nixos/riscv-and-vendor-sdk-toolchains.md`](guides/nixos/riscv-and-vendor-sdk-toolchains.md)
  are `inferred`, all three of them.
- **Marketplace, clone and used-market price sampling** was not done for most devices. The
  landscape guide's own evidence boundary states this.
- **Certification and regulatory records** were checked only for Xteink (where the finding was
  that no external CE/FCC marking exists on the devices at all). No positive control was run, so
  the absence is weaker evidence than it looks.

---

*Compiled 2026-09-07. Method: [`.agents/skills/hardware-device-research/SKILL.md`](.agents/skills/hardware-device-research/SKILL.md).*

---
---

# Round two — 2026-09-11

**Nothing above this line has been edited.** Three further sessions ran on 2026-09-11 — Xteink
round two, schematic net-tracing, and certification / market — and their results were integrated
on the same date. Where round two refutes round one, a dated correction is added; the original
sentence stays visible. **A verification report that quietly rewrites itself is worthless.**

Per-session detail: [`VERIFICATION-xteink-round2.md`](VERIFICATION-xteink-round2.md) ·
[`archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/README.md`](archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/README.md) ·
[`archive/guides/research/artifacts/certification-and-market-2026-09-11/README.md`](archive/guides/research/artifacts/certification-and-market-2026-09-11/README.md).
The round-two merge, its deferrals and its corrections:
[`research/passes/index-merge/deferred-round2.md`](research/passes/index-merge/deferred-round2.md) ·
[`research/passes/index-merge/corrections-requiring-review.md`](research/passes/index-merge/corrections-requiring-review.md).

## R1. ⚠ §6 is wrong about Xteink certification — corrected, not rewritten

§6 records:

> **Certification and regulatory records** were checked only for Xteink (where the finding was
> that no external CE/FCC marking exists on the devices at all). No positive control was run, so
> the absence is weaker evidence than it looks.

**The self-doubt in that last sentence was justified. The finding is refuted.**

**Xteink is an FCC grantee.** Applicant **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**,
grantee code **`2BTR9`**, registered 2025-12-21, holding **five granted Original Equipment
authorisations** — one for every ESP32-based device in the tree:

| FCC ID | Granted | Device |
|---|---|---|
| `2BTR9-X4L` | **2026-08-13** | XTEINK X4 Light — **never announced** |
| `2BTR9-X4C` | 2026-07-20 | XTEINK X4 Classic |
| `2BTR9-X4PRO` | 2026-06-16 | XTEINK X4 Pro |
| `2BTR9-XTEINKX4` | 2026-01-05 | XTEINK X4 |
| `2BTR9-XTEINKX3` | 2025-12-26 | XTEINK X3 |

**The error was a category error**, and it is worth naming precisely: the pass confused *"no mark
visible in a product photograph"* with *"no grant exists"*. Only the first was ever tested.

- ✅ **Survives:** no FCC ID was legible on the exteriors photographed. Not re-tested.
- ❌ **Refuted:** any reading that these devices are uncertified or unauthorised for the US.

47 CFR §2.935 permits a software **e-label** instead of a printed mark — ordinary for a device
with a screen. **Likely, and not verified.**

**This time the controls were run.** Positives `2BTR9-XTEINKX4`, `2AC7Z-ESPS3WROOM1`,
`2AN3WM5CARDPUTER` → **200**. Negatives `2AN3WM5CARDPUTERZERO`, `2ASYE-T-DISPLAY-K230`,
`2ZZZZNOSUCHGRANTEE` → **404**. The grantee was **enumerated in full** (`2BTR9` → exactly five
IDs), so the absence of an S4 or Nano grant is an absence against a complete listing.

**Transferable lesson:** round one searched by *product name*. Xteink files under model codes a
name search never reaches. **Enumerate the vendor's FCC grantee code** and you get its complete
certified product list, including unannounced devices. Written up in
[`guides/research/finding-certification-records.md`](guides/research/finding-certification-records.md).

Corrections are appended beneath the stale claim in **13 Xteink records** and in
[`VERIFICATION-xteink.md`](VERIFICATION-xteink.md) §C1–C4. Five new
`certification-and-compliance.md` records carry the full evidence.

## R2. The X4 Classic launched; the X4 was withdrawn

**X4 Classic**, marketed **"XTEINK X4 Classic (X4 V2)"**, listed **2026-09-06** at **USD 79**
(95 with base). It **replaced the X4**, whose product record **and all four dedicated
accessories** are now gone from the catalogue — on 2026-09-04 the accessories were still listed
but sold out, which was an end-of-life *signature*; a week later it is a completed withdrawal.

Two independent sessions enumerated `xteink.com/products.json` on 2026-09-11 (25 products) and
returned identical figures. The FCC succession corroborates the replacement. The stale rows in
[`devices/README.md`](devices/README.md) are **unedited**, with a dated correction beneath them.

## R3. A sixth Xteink device, found by enumeration rather than by name

[**X4 Light**](devices/xteink/x4-light/README.md) — FCC **`2BTR9-X4L`**, granted **2026-08-13**.
Never announced, listed, priced or reviewed. No `x4-light` collection handle exists, so unlike the
X4 Classic there is **no pre-launch signal** in the storefront either.

⚠ Its SoC, panel, feature set and price are **all unknown**. *"Light"* is a marketing word the
filing does not define. Internal photographs unlock **2027-02-09**; external photographs are
already public and held in the record.

This directly qualifies round one's *"Models that do not exist"* finding. That finding was correct
about `X4 Plus / Air / Pro Max` and remains correct. It was **not** correct that the family was
closed — and it could not have known, because it had no grantee code to enumerate.

## R4. Schematic net-tracing — 291 PDFs assessed

Every `artifacts/**/*.pdf` in the repository — **291 files** — was assessed for traceability.
Per-file verdicts: [`guides/reverse-engineering/schematic-pdf-traceability-census.md`](guides/reverse-engineering/schematic-pdf-traceability-census.md).

**The enabling finding: Altium exports embed invisible `CO` / `PI` / `NL` marker tokens at item
coordinates** — component outlines, pins and net labels — so a net list is recoverable from the
PDF text layer alone, with poppler and no EDA sources. That is what made the traces below
possible. Method: [`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md).

**Five boards fully traced**, each gaining a `schematic-netlist.md`: LilyGO T-Display-S3 (shared),
M5Stack Cardputer ADV (4 sheets), DinMeter, Cap LoRa-1262 and Cap CC1101. Two also gained a
`driver-vs-document-audit.md` — the vendor driver read against the schematic and the datasheet.
**8 schematic crops** were added across five `media/` directories, each with a **separate sibling
manifest**, because `media/manifest.json` is not append-safe as JSON.

Two traps worth more than the traces:

- ⚠ **KiCad and EAGLE exports frequently outline schematic text to vector paths.** `pdftotext`
  then yields **zero words** and the file is permanently untraceable. **For ZeroWriter Ink and the
  Seeed XIAO ESP32S3 a usable second export of the same design sits in the same directory** — the
  `Eeschema` copies. Without that check both designs look undocumented and are not.
- ⚠ **Non-Altium exports carry no `CO`/`PI`/`NL` tokens**, so every binding must be geometric.
  That applies to the Espressif ESP32-P4 board schematics.

⚠ **The richest untraced sheet in the repository is the M5Stack PaperMono's** —
`PaperMono_SCH_V0.6.2`, 6 pages, **144 `NL` tokens**, fully traceable, obtainable in about an
hour. It was **not traced**, because that record was owned by a live session throughout both
rounds.

## R5. Unidentified parts — three resolved or advanced, none deleted

| Record | Outcome |
|---|---|
| `unidentified/m5stack-stamp-s3a/dcdc-u4` | ✅ **Resolved — `JW5712`.** Confirmed independently by two round-two sessions. Retained for linkage, not retired |
| `unidentified/lilygo-t-display-s3-family/axpm65611` | ⚠ **Function established** — AMOLED bipolar display-bias supply, 12-pin — **identity still unknown**. No real record is possible without a manufacturer |
| `unidentified/m5stack-dinmeter/rotary-encoder` | Topology established: 5-terminal, A/COM/B + switch. Identity unknown |
| `unidentified/m5stack-dinmeter/buzzer` | Topology established: magnetic, AC-coupled drive. Identity unknown |

`JW5712` is now known to be fitted on **three** M5Stack boards. ⚠ Its only datasheet is a **raster
scan** — 0 extractable words — so it cannot be text-searched.

**No `unidentified/*` record was deleted, and none should be.** Other records link to them and
they are the stable landing place for a search on the unknown string.

## R6. Artifacts — 174 FCC exhibits, decided

Round one left **174 exhibit PDFs from 26 filings** in `scratch/`, outside the repository **with
no placeholders**, which the method forbids for anything useful. Round two applied the rules.

| | Files | Size |
|---|---:|---:|
| **Retained in the repository** — internal photographs and ID-label exhibits, ≤ 4 MiB each | **59** | **57.80 MiB** (60.61 MB) |
| **Archived**, each with a self-sufficient placeholder at its former repo path | **106** | **130.59 MiB** (136.93 MB) |
| **Parked** — PaperMono, live session | 11 | 10.27 MiB |
| Not copied — byte-identical to bytes already present | 5 | — |

Internal photographs were prioritised because for several of these boards they are the **only
public internal imagery that exists**, and `2BTR9-XTEINKX4`'s are the **first public teardown of
the Xteink X4**. Licensing is stated plainly: FCC exhibits are **US Government public records**,
redistribution **`allowed`** — correcting the `unknown` recorded earlier.

⚠ **The "281 MB" figure for that corpus is the whole scratch subject directory.** The PDFs are
**195.48 MiB / 204.97 MB**; the rest is text extractions, filing HTML and logs.

## R7. Machine-checked results — re-run, not copied

Every figure below was measured on **2026-09-11** by
[`research/passes/index-merge/verify-round2.py`](research/passes/index-merge/verify-round2.py). Round one's
numbers are **not** reused.

| Check | Round one (2026-09-07) | **Round two (2026-09-11)** |
|---|---|---|
| Relative links checked / broken | 10 387 / **1** | **10 970 / 1** |
| Typed artifacts / magic-byte mismatches | 61 / **0** | **1 219 / 3** |
| Device records / orphans | 38 created / **0** | **60 / 0** |
| Component records | 201 | **194** *(counted at `components/<mfr>/<part>/README.md`; round one's figure used a different rule)* |
| Vendor guides | 37 | **38** — new [`vendors/xteink/`](vendors/xteink/README.md) |
| Authored `.md` (excl. `artifacts/`, `archive/`, `scratch/`) | 469 *added* | **958** *total* |
| Binary artifacts under `artifacts/` | 161 *added* | **2 380** *total* |
| Archive placeholders / incomplete | not measured | **155 / 2** |
| `certification-and-compliance.md` records | 0 | **32** |
| `schematic-netlist.md` records | 0 | **5** |
| Deletions on any file edited by the merge | **0** | **0** |
| `HEAD` | `4aa02e10…` | **`4aa02e10…`, unchanged** — 91 staged paths intact |

**The three new deltas are scope, not regression.** Round one validated only the artifacts *it
added* and counted only the links it could reach; round two checked the whole tree.

- **The one broken link is the same one round one reported** — the vendored upstream
  `XIAO_Webcam/README.md → docs/…jpg?raw=true`, preserved as supplied and deliberately not
  fixed, for the reason round one gave. **The round-two merge introduced no broken link**: an
  intermediate check caught one forward reference of its own (to `deferred-round2.md`, written
  later in the pass) and it was resolved before completion.
- **All 3 magic-byte mismatches are pre-existing and benign**: three files named `*.png` in
  `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/examples/selected/…/images/` are **JPEGs**
  (`ff d8 ff db`), tracked since commit `cbfbff3`, vendored from a community example. They are
  real images with the wrong extension — **not** an HTML error page saved as a document, which is
  the failure this check exists to catch. Renaming them would be a delete-plus-add in a vendored
  tree, so they are **reported, not repaired**.
- **2 archive placeholders are incomplete**, both pre-existing:
  `software/applications/crosspoint-reader/plugins/source-snapshots.ARCHIVED.md` (no hash, no
  size, no original path — **in the live `software/` tree, not touched**) and
  `devices/seeed-studio/…/TRANSLATIONS.ARCHIVED.md` (hash and size present, original path never
  stated). **All 106 placeholders written by this pass are complete.**

## R8. What round two still does not establish

- **Still zero hardware claims.** §1's headline caveat is unchanged and applies to round two in
  full. No board was purchased, powered, flashed or probed.
- **CE, UKCA, SRRC, CCC, MIC and ISED remain unestablished for every device.** CE has no database
  to search; the Chinese registers failed to connect (`000`); the Japanese register was reachable
  (200) but form-driven and **not queried**; ISED returned 503. ⚠ **Those are method failures, not
  absence findings**, and must not be read as "not approved".
- **The `ID Label` exhibits were downloaded but never visually inspected for secondary marks.**
  Whether a CE mark appears on Xteink artwork is open, and cheap to close.
- **Schematics are permanently withheld on all 26 filings examined.** The FCC is not a route to a
  schematic for any of these vendors.
- **Marketplace, clone and used-market pricing is still unsampled.** AliExpress, eBay, Amazon,
  Taobao and JD were all bot-walled or JS-shelled on 2026-09-11. ⚠ **A 200 response containing no
  prices is a failure, not a data point** — §6's marketplace gap is **unchanged**.
- **`fccid.io` is a mirror, not the FCC.** `apps.fcc.gov` returned 403 to all five user agents
  tried, so none of the above was confirmed against the primary host.
- **PaperMono was untouched in both rounds.** Its certification claims are now known to be stale
  (`2AN3WM5PAPERMONO` exists, granted 2025-07-09), its richest-in-repository schematic is
  untraced, and 11 of its FCC exhibits sit in scratch with no placeholder. All parked in
  [`deferred-round2.md`](research/passes/index-merge/deferred-round2.md) §1.
- **§6's remaining bullets stand**: no net-level tracing was attempted for most of the LilyGO
  family, and `components/canaan/k230`'s toolchain routes are still all `inferred`.

---

*Round two compiled 2026-09-11. Method: [`.agents/skills/hardware-device-research/SKILL.md`](.agents/skills/hardware-device-research/SKILL.md).*
