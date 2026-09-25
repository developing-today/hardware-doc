# Verification — M5Stack DinMeter (K134) and DinMeter v1.1 (K134-V11)

**Research pass date: 2026-09-04.** Records verified:
[`devices/m5stack/dinmeter`](devices/m5stack/dinmeter/README.md),
[`devices/m5stack/dinmeter-v1.1`](devices/m5stack/dinmeter-v1.1/README.md), and the 15 component
records they cite.

---

## 0. The headline, stated first

> **Zero claims in these records are hardware-tested. No DinMeter of either revision was
> available at any point.**

This is a documentary and source-code analysis: vendor documentation, three Altium-published
schematics parsed at the marker layer, four independent board-support source trees, and a broad
public-source sweep. It is thorough about what published artefacts can establish and it is worth
**nothing** as evidence of how a physical unit behaves. Every claim carries an evidence label and
every untested command says so.

| Claim category | Count |
|---|---:|
| Hardware-tested claims | **0** |
| Commands executed successfully (acquisition, extraction, analysis) | ~45 |
| Commands presented as untested (`not-tested`) | 14 |
| `reported-working` (vendor- or CI-published, not run here) | 9 |
| Examples built or run here | **0 of 22 catalogued** |
| Features with a hardware test status | **0 of 20** |

## 1. File and byte inventory — recomputed from disk

| Metric | Value |
|---|---:|
| Regular files across both device records + 15 component records | **124** |
| Symlinks (3 archived artifacts × 2 links each) | 6 |
| Markdown files authored | **69** |
| Bytes in repository (excluding symlink targets) | **13 396 847** (13.4 MB) |
| Bytes archived out of the repository | **21 625 485** (21.6 MB) |
| Downloads attempted | 28 |
| **Downloads failed** | **0** |
| HTML/error pages retained under a misleading extension | **0** |

Breakdown of the two device records:

| Record | Files | Notes |
|---|---:|---|
| `devices/m5stack/dinmeter` | 61 | full record: 34 authored `.md`, 10 images, 7 derived analyses, 5 source snapshots, 3 primary artifacts |
| `devices/m5stack/dinmeter-v1.1` | 34 | scoped revision record: 21 authored `.md` incl. `stamp-s3-to-s3a-delta.md`, 5 images, 2 deliberately-duplicated artifacts |

## 2. Binary validation by magic bytes

Every non-text artifact was validated by content, not by extension.

| Extension | Files | Detected type | Mismatches |
|---|---:|---|---:|
| `.pdf` | 10 | `%PDF-` | **0** |
| `.webp` | 10 | `RIFF`…`WEBP` | **0** |
| `.jpg` | 6 | `ff d8 ff` | **0** |
| `.tar.gz` | 2 | gzip | **0** |
| `.stl` / `.kicad_mod` | 5 | ASCII text (expected) | **0** |
| **Total** | **33** | | **0** |

### ⚠ One mismatch was found and corrected during acquisition

Four images fetched from `cdn.shopify.com` have canonical URLs ending **`.webp`** but returned
**JPEG** bytes (`ff d8 ff e1 … Exif`) — Shopify content-negotiates the format and ignores the
path extension. They were **renamed locally to `.jpg`** so the extension matches the content;
bytes are unmodified and the URLs are recorded exactly as served, each with a
`format_mismatch_note`. Recorded in
[`devices/m5stack/dinmeter-v1.1/media.md`](devices/m5stack/dinmeter-v1.1/media.md) and as a
durable vendor trap in [`vendors/m5stack/README.md`](vendors/m5stack/README.md) §11.8.

## 3. Link integrity

| Metric | Value |
|---|---:|
| Markdown files checked | **71** (69 authored + 2 additively edited shared files) |
| Relative links resolved | **563** |
| **Broken links** | **0** |

Four were broken on the first pass and were fixed: three pointed at
`components/nxp/pcf8563/README.md`, which does **not exist** (that component directory holds only
`artifacts/`), and one had an incorrect `../` depth. Absolute `http(s)://` links were not
fetched during verification.

**Archive paths are excluded from the "must resolve" requirement** per the repository convention —
the archive is machine-local. All three archived artifacts nonetheless resolve on this machine
and each satisfies the placeholder contract (§4).

## 4. Archived artifacts — the three-link chain

| Artifact | Bytes | SHA-256 (16) | Placeholder | Cited by owner | Cited by consuming device |
|---|---:|---|---|---|---|
| `devices/m5stack/dinmeter/artifacts/docs/docs-en-core-M5DinMeter.pdf` | 7 459 888 | `8b3db00abbc7e317` | ✔ | ✔ device README artifact layout | ✔ `sources.md` S-02 |
| `devices/m5stack/dinmeter-v1.1/artifacts/docs/docs-en-core-DinMeter_v1.1.pdf` | 11 261 000 | `617a9ea8039ed1fc` | ✔ | ✔ device README artifact layout | ✔ `sources.md` V-02 |
| `components/m5stack/stamp-s3/artifacts/Stamp-S3.step` | 2 904 597 | `7f29337cdac90c80` | ✔ | ✔ component README §5, §6 | ✔ **both** device records, via the component |

Each placeholder carries hash, byte size, media type, retrieval date, licence status,
redistribution status, disposition, reason for archiving, reproducibility, and **two or more
independent reacquisition URLs**. All three symlinks and their `.ARCHIVED.link` companions
resolve.

## 5. Bidirectional device ↔ component links

| Check | Result |
|---|---|
| Component records created or extended | **15** |
| With a `Used By` section | **15 / 15** |
| Naming DinMeter and/or DinMeter v1.1 and its role | **15 / 15** |
| Device READMEs linking every component they mention | ✔ verified — the key-specification table links all 14 functional parts |

Records: `m5stack/stamp-s3`, `m5stack/stamp-s3a`, `sitronix/st7789v2`, `sitronix/st7789p3`,
`generic/bm8563`, `generic/tp4057`, `microne/me3116am6g`, `silergy/sy7088`, `belling/bl8075`,
`murata/mun3cad01-sc`, `sgmicro/sgm2578`, `unidentified/m5stack-dinmeter/rotary-encoder`,
`unidentified/m5stack-dinmeter/buzzer`, `unidentified/m5stack-stamp-s3a/dcdc-u4`, and
`awinic/aw35122` (**additively extended**, not created).

Five are `unidentified` or schematic-only because no datasheet exists. **No part number was
guessed anywhere**, and no candidate from a comparison shortlist was promoted to a finding.

## 6. Manifests and structured data

| File | Valid JSON | Contents |
|---|---|---|
| `devices/m5stack/dinmeter/acquisition/manifest.json` | ✔ | 27 records — 20 downloaded, 7 derived, 1 archived, **0 failed** |
| `devices/m5stack/dinmeter-v1.1/acquisition/manifest.json` | ✔ | 9 records — 8 downloaded, 1 derived, 1 archived, **0 failed**, 2 flagged byte-identical to v1.0 |
| `devices/m5stack/dinmeter/media/manifest.json` | ✔ | 10 images, full provenance, 0 teardown/PCB |
| `devices/m5stack/dinmeter-v1.1/media/manifest.json` | ✔ | 5 images, **4 URL-extension mismatches recorded** |
| `devices/m5stack/dinmeter/examples/catalog.json` | ✔ | 22 examples — 8 official, 10 community, 2 rejected, 2 inaccessible, 7 selected, 3 vendored, **0 built** |

Every artifact record carries expected SHA-256, byte size, canonical URL, retrieval date,
licence, licence evidence, redistribution status, disposition and repository state.

## 7. Duplicate hashes — intentional, and quantified

| Pair | SHA-256 | Redundant bytes | Why kept |
|---|---|---:|---|
| v1.0 ↔ v1.1 schematic | `03ec3353…` | 433 658 | **The duplication is the finding.** Deduplicating would erase the evidence that M5Stack published one file under two URLs and two SKU names |
| `DinMeter.stl` ↔ `DinMeter_v1.1.stl` | `90f04d6a…` | 573 284 | same |
| `Stamp-S3.stl` ↔ `Stamp-S3A.stl` | `f72c1af2…` | 158 484 | same |
| **Total intentional redundancy** | | **1 165 426** (1.17 MB) | |

**One duplicate was deduplicated:** the ESP32-S3 datasheet fetched from
`m5stack-doc…/472/esp32-s3_datasheet_en.pdf` (SHA-256 `b6db403d…`) is byte-identical to
`components/espressif/esp32-s3r8/artifacts/esp32-s3-datasheet-v2.0-m5stack-mirror.pdf` already
held. **Not re-added**; the additional URL is recorded in the source table instead.

## 8. Source-table completeness

| Check | Result |
|---|---|
| Source rows | 37 (v1.0 record) + 16 (v1.1 record) = **53** |
| Rows with `Class` | 53 / 53 |
| Rows with a retrieval date | 53 / 53 |
| Rows with version/date **or an explicit `unknown`** | 53 / 53 |
| Rows stating what they establish | 53 / 53 |
| Rows stating scope/limitations | 53 / 53 |

## 9. Shared files — what was and was not touched

**Not edited** (as instructed): `README.md`, `devices/README.md`, `components/README.md`,
`vendors/README.md`, `artifact-manifest.md`, `software/README.md`, `guides/markets/*`,
`devices/m5stack/papermono*`. Proposed additions are staged as ready-to-paste Markdown in
[`archive/devices/m5stack/dinmeter/artifacts/research-scratch/index-fragments.md`](archive/devices/m5stack/dinmeter/artifacts/research-scratch/index-fragments.md).

**Two files additively edited**, each after confirming `find <file> -mmin -30` returned empty
immediately beforehand:

| File | Change | Existing content altered? |
|---|---|---|
| `vendors/m5stack/README.md` | **Appended** §11 (14 live-probed findings + change-log addendum) strictly after §10 | **No** |
| `components/awinic/aw35122/README.md` | **Inserted** one `###` subsection inside the existing `## 4. Used By` | **No** |

**No state-changing git command was run at any point.** `git status` was read-only.

## 10. Evidence discipline — specific checks

| Check | Result |
|---|---|
| PDF text layer validated before transcription | ✔ page-frame zone letters `A`–`D`, numbers `1`–`4`, and seven known part strings verified at expected coordinates; 84 of 85 marker-derived designators match visible text |
| A legible-but-wrong extraction was caught and discarded | ✔ Altium draws its marker layer **twice**; the first parse produced `PPIIJJ110011` for `PIJ10101`. Output discarded, glyph dedup added, failure preserved in `commands.md` §4 |
| Absence proven by enumeration, not by searching for the expected | ✔ complete `CO`/`PI`/`NL` census; `COS1`/`COR20`/`COY1` etc. searched in both single **and** double-struck forms — zero hits |
| Extraction incompleteness disclosed | ✔ ~20 of ~260 `PI` markers unrecovered, stated with the cause; no published table rests on a missing marker |
| Document metadata read | ✔ the BM8563 datasheet carries a stray `MAX1937` header string — a derived document — recorded in its component record |
| Candidates never promoted to findings | ✔ five parts left `unidentified`; the repo's existing Alps encoder record explicitly **not** claimed for this device |
| Refuted/negative results recorded | ✔ ESPHome/Tasmota/Meshtastic/Bruce-upstream all **0 hits**, recorded; 8 confirmed-already-correct claims listed in `gaps-and-conflicts.md` §10 |
| Conflicts recorded rather than resolved by preference | ✔ **9** open conflicts across the two records |
| Blocked sources reported honestly | ✔ `community.m5stack.com` 401 — and **no UA rotation attempted**, since it is authentication, not bot-blocking |

## 11. Open conflicts carried forward

| # | Conflict | Where |
|---|---|---|
| 1 | PORT.A/B wire colours — vendor PinMap vs schematic + M5Unified | `dinmeter/gaps-and-conflicts.md` §1 |
| 2 | `S1`, `R20`, `Y1` — designator text with no marker layer | §2 |
| 3 | v1.1 assets are byte-identical v1.0 assets | §3, v1.1 V2 |
| 4 | ST7789P3 — named 3×, documented nowhere | §4, v1.1 V3 |
| 5 | Stamp-S3A 24 mm vs 26 mm | §5, v1.1 V5 |
| 6 | Grove rail: 5.00 V spec vs ≈5.38 V from the schematic's own formula | §6 |
| 7 | Stamp-S3A DC-DC: page says MUN3CAD01-SC, schematic says otherwise | v1.1 V4 |
| 8 | Backlight PWM: 200 Hz (M5Stack's firmware) vs 5 kHz (Espressif) | `compatibility-and-status.md` §6 |
| 9 | Rear FPC pin numbering reversed between Stamp revisions | v1.1 V6 |

## 12. The one prediction that most needs testing

**DinMeter v1.1's RGB LED almost certainly will not light with stock M5Unified.** The Stamp-S3A
moves the WS2812B-2020 onto a switched rail gated by GPIO38, and M5Unified at master
`8530f5377d782e4a25a6c482de2e71c3f75ca8eb` has no GPIO38 enable step for any board.

**Status: `inferred`** — vendor documentation + schematic net reading + source grep. **Not
reproduced on hardware.** Two lines of code on a real v1.1 unit would settle it:

```cpp
pinMode(38, OUTPUT); digitalWrite(38, HIGH); delay(1);   // then drive GPIO21
```

## 13. Verification verdict

| Property | Status |
|---|---|
| Inventory recomputed from disk | ✔ |
| SHA-256 computed for every retained artifact | ✔ |
| Binary types validated by magic bytes | ✔ 33/33, **0 mismatches** |
| Failed downloads retained under misleading extensions | ✔ none |
| Authored relative links resolve | ✔ 563/563 |
| Archived artifacts satisfy the placeholder contract | ✔ 3/3, ≥2 reacquisition URLs each |
| Three-link chain intact for archived artifacts | ✔ 3/3 |
| Bidirectional device ↔ component links | ✔ 15/15 |
| Manifests valid and complete | ✔ 5/5 |
| Duplicate bytes quantified and justified | ✔ 1.17 MB intentional; 1 cross-repo duplicate avoided |
| Source rows complete | ✔ 53/53 |
| Shared index files untouched | ✔ |
| State-changing git commands | ✔ **none run** |
| **Hardware-tested claims** | **0 — stated plainly throughout** |

**Verdict: the records are internally consistent, fully cross-linked, honestly labelled, and
verifiable from a clean clone.** Their limitation is singular and stated on every page: no
hardware was in hand, so nothing here is a measurement.

---

*Report generated 2026-09-04 as part of the DinMeter research pass. Bulk archive:
`archive/devices/m5stack/dinmeter{,-v1.1}/` and `archive/components/m5stack/stamp-s3/`.
Working store and proposed index additions:
[`archive/devices/m5stack/dinmeter/artifacts/`](archive/devices/m5stack/dinmeter/artifacts/research-scratch/README.md).*
