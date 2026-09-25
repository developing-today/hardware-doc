# Corrections requiring review

Written **2026-09-07** by the index-merge pass. **Nothing in this file has been applied as a
correction.** Each item would require *editing or deleting an existing line*, which the merge
pass was forbidden to do. Where possible a dated note was **added beneath** the incorrect line,
leaving the original visible; those cases are marked ✅ *note added in place*.

A maintainer needs to decide each one.

---

## 1. `components/unidentified/m5stack-stamp-s3a/dcdc-u4/` — the part **is** identified

| | |
|---|---|
| **Record making the claim** | `components/unidentified/m5stack-stamp-s3a/dcdc-u4/README.md`, created 2026-09-04 by the DinMeter pass |
| **Claim** | *"**Manufacturer / part number:** ⚠ **NOT ESTABLISHED.** The `Sch_StampS3_v0.3.3.pdf` symbol carries **no part-number text**."* |
| **Correction** | The part number **is** present: **`JW5712`** (JoulWatt), printed in the Altium *Comment* field directly beneath the symbol body |
| **Evidence** | Source render `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1150/Sch_StampS3_v0.3.3_page_01.png`, SHA-256 `1156e645de35fe68e6458e9131657c8f02045bbcd14f97ab190bb1486ee7a1c5`, re-fetched and hash-matched 2026-09-04. 1:1 crop of region `1000,3300–2200,3900` px shows `JW5712` in blue beneath the body. Text-layer occurrences: `JW5712` ×1 in `Sch_StampS3_v0.3.3`, ×0 in `Sch_M5StampS3_v0.2` |
| **Corroboration** | The unidentified record's own observations — `IOUT: 0~0.6A`, three `VSEL` straps, **no feedback divider**, `VOS` remote sense — match [`components/joulwatt/jw5712`](../../../components/joulwatt/jw5712/README.md) exactly. That record has existed since 2026-09-01 |
| **Probable cause** | The DinMeter pass parsed only the Altium **marker layer**. On these files the readable text lives inside a **Form XObject** that a marker-only parse never enters, and it fails *silently* |
| **Source** | `archive/devices/m5stack/shared-artifacts/cardputer/research-scratch/index-fragments.md` §0 |

**What the fragment asked for:** retire the `unidentified/` directory in favour of
`components/joulwatt/jw5712/`, leaving a redirect stub. A paste-ready stub is in the fragment.

**What was done instead:** ✅ *note added in place.* A provenance note was **appended** to
`components/joulwatt/jw5712/README.md` §4, and the `components/README.md` DinMeter table row for
`dcdc-u4` now carries a ⚠ pointing here. **The unidentified record itself was not touched.**

**Decision needed:** delete or stub `components/unidentified/m5stack-stamp-s3a/dcdc-u4/`.

> **In that session's favour**, and worth not losing: its identification of `MUN3CAD01-SC` as a
> **Murata µPOL power module** is *correct*, and it refutes the Cardputer session's own suspicion
> that the string was a mis-extraction.

---

## 2. `components/semtech/sx1262/README.md` §9 — RadioLib is **MIT**, not LGPL-3.0

| | |
|---|---|
| **Incorrect line** | *"⚠ **Licence mismatch, flagged not confirmed:** RadioLib is **LGPL-3.0** upstream while the M5Stack demo carrying it is MIT. Not verified in this pass."* |
| **Correction** | RadioLib is **MIT**. There is **no mismatch** |
| **Evidence** | `executed-success`, 2026-09-04. The licence file is **`license.txt`, lower case** — which is why a `LICENSE` fetch 404s, and is the likely origin of the LGPL-3.0 belief. Content is `MIT License / Copyright (c) 2018 Jan Gromeš`, **byte-identical at tags `7.2.1` and `7.7.1`**. `gh api repos/jgromes/RadioLib --jq .license.spdx_id` → `MIT` |
| **Source** | `scratch/lora-generations/index-fragments.md` §6.1 |

✅ *Note added in place* — a dated correction bullet sits immediately below the incorrect line;
the original is untouched and still visible.

**Decision needed:** replace the original bullet, or leave the original + correction pair.

⚠ **The same wrong claim appears in at least three more places** and was **not** annotated,
because they lie outside this task's target list:

- `components/m5stack/stamp-lora-1262/README.md` §4
- `devices/m5stack/papermono/features/lora.md` §2
- `artifact-manifest.md` — the `M5Cardputer-UserDemo-CardputerADV-b549eac0` row says
  *"repo pins LGPL-3.0 RadioLib"*. ✅ A ⚠ pointer to this file **was** added there, since that
  row is new in this pass.

---

## 3. `components/semtech/sx1262/README.md` §11 / G12 — a Semtech vendor guide now exists

| | |
|---|---|
| **Now-stale line** | *"No vendor sourcing guide exists in this repository for Semtech — see the vendor guides index"* (and, in §13, *"**no Semtech guide exists yet**; §11 is what one would open with"*) |
| **Correction** | [`vendors/semtech/README.md`](../../../vendors/semtech/README.md) was written 2026-09-04, using §11 as its starting point |
| **On G12** | The guide's recovered document catalogue confirms Semtech's current listing is `SX1261/SX1262 Datasheet` — the same document held here at Rev 2.2. The "2025-04-07 listing date vs Dec 2024 revision" question is **still `unresolved`**, but is now known to be a *listing-date* field in a catalogue rather than a document date |
| **Source** | `scratch/lora-generations/index-fragments.md` §6.2 |

✅ *Note added in place* below the §11 opening sentence. **The §13 "no Semtech guide exists yet"
line was not annotated** — it is in a different section and a second inline note would clutter
the record. It still needs updating.

---

## 4. `devices/m5stack/papermono/comparisons-and-recommendations.md` — two X4 Pro claims

| | |
|---|---|
| **Incorrect claim 1** | The X4 Pro is *"a **sealed consumer reader** with locked-down firmware… **You cannot put your own application on it.**"* |
| **Correction 1** | **It is reflashable.** Many units ship USB-locked, but the lock is defeated by an OTA unlock, by SD-card install, or by buying the vendor's developer-unlocked variant. **At least four independent open-source firmwares target it.** The real difference from a PaperMono is not programmability — it is the absence of a published schematic, headers and USB-C |
| **Incorrect claim 2** | *"the XTEINK X4 Pro — the comparison the community actually makes — was never priced."* Repeated in that record's `market-and-pricing.md` and `gaps-and-conflicts.md` |
| **Correction 2** | **$99.00**, observed 2026-09-04 from `xteink.com`'s Shopify `/products.json` |
| **Source** | `archive/devices/xteink/shared-artifacts/research-scratch/index-fragments.md` §6, which contains ready-to-paste replacement text |

❌ **No note added.** `devices/m5stack/papermono*` is outside this task's target list and is owned
by another pass. **Nothing was written to that tree.**

---

## 5. `components/generic/bm8563/README.md` — reported broken link, now self-healed

| | |
|---|---|
| **Report** | The Xteink pass (2026-09-04) found **two links to `../../nxp/pcf8563/README.md`** at roughly lines 8 and 45. At that time `components/nxp/pcf8563/` held only `artifacts/`, so both links were broken. **The breakage pre-dated that session** |
| **Status 2026-09-07** | ⚠ **The links now resolve.** `components/nxp/pcf8563/README.md` was created on 2026-09-07 by the LilyGO T-Display-S3 pass, which describes it as a *"record created to fill a gap — the artifact existed with no README"* |
| **Residual issue** | `components/nxp/pcf85063a/README.md` still flags that directory as *"Artifacts-only directory; no record page yet"* — **that line is now wrong** |
| **Source** | `archive/devices/xteink/shared-artifacts/research-scratch/index-fragments.md` §7 |

❌ **Not fixed, per instruction.** The Xteink fragment offered two options; **option B (write the
missing record) has effectively happened by accident**, which is the better-signposted outcome it
recommended. ✅ The situation is recorded in `components/README.md` under *"One pre-existing
defect, reported not repaired"*.

**Decision needed:** update the stale sentence in `components/nxp/pcf85063a/README.md`.

---

## 6. ⚠ New conflict found *during* this merge — TP4057 charge current

Not from any fragment. Surfaced by placing two sessions' text in the same record.

| Source | Designator | `R_PROG` | Stated charge current |
|---|---|---|---|
| DinMeter pass, `components/generic/tp4057/README.md` § Used By | `U2`, `R13` | **3.3 kΩ** | **100 mA**, *"M5Stack specifies"* |
| Cardputer pass, same file, appended by this merge | `U1`, `R5` | **3.3 kΩ** | **≈300 mA**, *inferred* from `I = 1000 × V_PROG / R_PROG`, explicitly **not measured** |

Same part, same programme resistance, **3× disagreement**. At least one is wrong, or the two
boards differ in a way neither record captures.

✅ *Note added in place* — a ⚠ paragraph in that record points at this entry. **Neither figure
was altered.** The Cardputer figure is self-declared as an order-of-magnitude inference; the
DinMeter figure is attributed to the vendor. That asymmetry suggests the vendor figure is the
one to trust, but **it has not been checked** and the datasheet was not consulted by either pass.

---

## 7. Housekeeping observed, not acted on

- **Eight vendor guides exist but are absent from `vendors/README.md`.** This pass added the four
  in scope — `canaan`, `lilygo`, `semtech`, `m5stack`. Still unlinked, and pre-dating these seven
  passes: **`dke`, `everest-semiconductor`, `omnivision`, `solder-party`**.
- **`vendors/README.md` has three orphan table rows after its `## Related` section** (lines
  ~122–124: Seeed Studio, Soldered Electronics, Zerowriter), in a column format that matches no
  table in the file. Pre-existing; **not touched**, as repairing it means moving existing lines.
- **No `VERIFICATION-*.md` exists for the LilyGO T-Display-S3 pass or the LoRa-generations pass.**
  The other five passes each produced one and all five are now linked from the root `README.md`.
  If the T-Display-S3 session writes one, it needs adding to that list.

---
---

# Round two — 2026-09-11

Appended by the round-two index merge. **Nothing above this line was altered.** Items 1–7 remain
as written on 2026-09-07; item 1 is now **adjudicated** — see §R0.

Unlike round one, most items below **were applied**, as dated notes appended beneath the stale
line. The original sentence is visible in every case. Items still needing a human decision are
marked ⚠ **OPEN**.

---

## R0. Item 1 (`dcdc-u4`) is adjudicated — the part is `JW5712`

✅ **Closed.** Two round-two sessions confirmed it independently: the certification/market pass
re-fetched and hash-matched the schematic PNG
([`corrections-adjudicated.md`](corrections-adjudicated.md) §1), and the schematic net-tracing
pass read `JW5712` out of the sheet text directly. The `⚠` on the `components/README.md` row is
**unchanged**; a new round-two section in that file records the adjudication beneath it.

**Still not done, and still a maintainer's call:** whether to retire
`components/unidentified/m5stack-stamp-s3a/dcdc-u4/` in favour of a redirect stub. The tracing
pass argues **no** — other records link to it, and it is the stable landing place for a search on
the unknown string. This merge followed that advice and marked it *resolved, retained for
linkage*.

---

## R1. ⭐ The Xteink certification finding is **refuted** — 13 records + 2 reports corrected

**The single largest correction of this sweep.**

| | |
|---|---|
| **Claim** | Records across `devices/xteink/` and `VERIFICATION-xteink.md` stated that **no FCC/CE filing exists** for any Xteink device, and `VERIFICATION-sweep-2026-09-04.md` §6 generalised it to *"no external CE/FCC marking exists on the devices at all"* |
| **Status** | ❌ **Refuted** |
| **Correction** | Xteink — **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**, grantee code **`2BTR9`**, registered 2025-12-21 — holds **five granted Original Equipment authorisations**: `2BTR9-XTEINKX3` (2025-12-26), `2BTR9-XTEINKX4` (2026-01-05), `2BTR9-X4PRO` (2026-06-16), `2BTR9-X4C` (2026-07-20), `2BTR9-X4L` (2026-08-13) |
| **Evidence** | `https://fccid.io/2BTR9` and the five filing pages, retrieved 2026-09-11, **with controls**: positives `2BTR9-XTEINKX4`, `2AC7Z-ESPS3WROOM1`, `2AN3WM5CARDPUTER` → **200**; negatives `2AN3WM5CARDPUTERZERO`, `2ASYE-T-DISPLAY-K230`, `2ZZZZNOSUCHGRANTEE` → **404**. Raw run `scratch/market-and-certification/logs/fcc-controls.txt` |
| **Root cause** | The original pass confused **"no mark visible in a product photograph"** with **"no grant exists"**. Only the first was ever tested. It also searched by *product name*; Xteink files under model codes (`XTEINKX3`, `X4PRO`, `X4C`) that a name search does not reach |
| **What survives** | ✅ *"No FCC ID was legible on the exteriors photographed."* Not re-tested, and plausibly still true — 47 CFR §2.935 permits a software **e-label** instead of a printed mark. **That explanation was not verified.** |

✅ **Applied as dated notes, originals untouched, in 13 records:**

`devices/xteink/x4-pro/{README.md, media.md, research-log.md, compatibility-and-status.md, acquisition/README.md, features/wifi-and-bluetooth.md}` ·
`devices/xteink/x4/{media.md, gaps-and-conflicts.md, community.md, features/wifi-and-bluetooth.md}` ·
`devices/xteink/x3/gaps-and-conflicts.md` · `devices/xteink/x4-classic/media.md` ·
`devices/xteink/s4/gaps-and-conflicts.md`

✅ **Applied as dated correction sections in 2 reports:** `VERIFICATION-xteink.md` (§C1–C4) and
`VERIFICATION-sweep-2026-09-04.md` (round-two section). **Neither original sentence was edited.**

✅ **Five new `certification-and-compliance.md` records** — `x3`, `x4`, `x4-pro`, `x4-classic`,
`x4-light` — each reproducing the full control set rather than referencing it.

⚠ **OPEN — two consequences a maintainer should weigh:**

1. `devices/xteink/x4-pro/gaps-and-conflicts.md` and `x4-classic/gaps-and-conflicts.md` already
   carried round-two "resolved" rows for this, written by the Xteink pass. There are now **two**
   corrections of the same claim in those files. Harmless, but redundant.
2. The **same error shape** almost certainly exists for M5Stack PaperMono — see
   [`deferred-round2.md`](deferred-round2.md) §1.2. **Not corrected: live session.**

---

## R2. The X4 Classic launched and the X4 was withdrawn — `devices/README.md` was wrong on both

| | |
|---|---|
| **Claim** | The Xteink family table in `devices/README.md` prices the **X4** and marks the **X4 Classic** *"not listed"* |
| **Status** | ❌ Both wrong as of 2026-09-06 |
| **Correction** | X4 Classic, marketed **"XTEINK X4 Classic (X4 V2)"**, listed **2026-09-06** at **USD 79** (95 with base). It **replaced** the X4, whose product record **and all four dedicated accessories** have been removed from the catalogue |
| **Evidence** | `https://xteink.com/products.json?limit=250&page=1`, 25 products enumerated, retrieved 2026-09-11 by **two independent sessions** returning identical figures. Corroborated by the FCC succession `2BTR9-XTEINKX4` (2026-01-05) → `2BTR9-X4C` (2026-07-20) |

✅ **Applied** as a dated `### Round-two corrections` subsection beneath the stale table in
`devices/README.md`, plus appends to `devices/xteink/x4/market-and-pricing.md` and
`devices/xteink/x4-pro/market-and-pricing.md`. **The stale rows are unedited.**

⚠ **OPEN:** `guides/markets/device-comparison-matrix.md` and
`guides/markets/handheld-and-eink-device-landscape-2026-09.md` almost certainly carry the same
stale X4 price and X4-Classic-not-listed claim. **Not checked and not corrected** — `guides/markets/`
is outside this task's target list and was marked protected by three round-one sessions.

---

## R3. ✅ Closed — the X4 Pro **was** priced (round one, item 4, claim 2)

Round one parked a conflict: `devices/m5stack/papermono/comparisons-and-recommendations.md` says
*"the XTEINK X4 Pro … was never priced"*, against a vendor-API observation of **USD 99.00** on
2026-09-04.

**A second independent observation on 2026-09-11 returned USD 99.00 again** — same endpoint, one
week apart, identical. The PaperMono claim is **wrong on both dates**.

⚠ **OPEN — not applied.** `devices/m5stack/papermono/` is owned by a live session. The
confirmation is recorded in `devices/xteink/x4-pro/market-and-pricing.md` and parked in
[`deferred-round2.md`](deferred-round2.md) §1.

---

## R4. FCC exhibit redistribution was recorded `unknown`; it is `allowed`

| | |
|---|---|
| **Claim** | `devices/xteink/{x4-pro,x4-light,x4-classic}/artifacts/certification/README.md` record *Redistribution status: **`unknown`*** |
| **Correction** | **`allowed`.** FCC equipment-authorisation exhibits are **US Government public records**, published under 47 CFR §2.1033. The agency asserts no copyright |
| **Scope** | every FCC exhibit in the repository — 59 retained, 106 archived |

✅ **Applied** as a dated *Correction* section appended to each of the three files. The original
tables are unedited. ⚠ Confidentiality **embargoes** are unaffected: withheld exhibits were never
published, so there is nothing to redistribute until their release dates.

---

## R5. ⚠ **OPEN** — `goodix/gt911` programming guide forbids redistribution on its own face

`components/goodix/gt911/artifacts/gt911-programming-guide-rev00-2014-08-04-crystalfontz-mirror.pdf`
(477,454 B, `60c6c228…`) states on page 1: *"GOODIX CONFIDENTIAL … Reproduction and/or
distribution … is strictly prohibited without written consent of GOODIX."*

Redistribution status **`prohibited` as written**. Currently **in the repository, unstaged**.
**A maintainer must choose:** keep unstaged · archive with a placeholder · keep only the metadata
block and delete the bytes. **This merge changed nothing** and flagged it in
`components/README.md` and `artifact-manifest.md` §6.

Same shape, lower severity — **UC8253** and **UC8179** datasheets are marked *"for TFT module use
only"*, a **use restriction of unclear scope, not a licence**. Both unstaged. ⚠ **OPEN.**

---

## R6. ⚠ **OPEN** — `nanjing-top-power/tp4065` package may be wrong

The net-tracing pass found the schematic symbol is **5-pin**, not SOP-8. If
`components/nanjing-top-power/tp4065/README.md` states or implies SOP-8 it needs a dated
correction. **Not checked and not applied** — outside every round-two session's scope, and
outside this merge's target list. Reported by
[`archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/index-fragments.md`](../../../archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/index-fragments.md) §2. *(Was `scratch/schematic-tracing/…`; relocated 2026-09-20.)*

Note this is a **different part** from the TP4057 charge-current conflict in item 6 above, which
remains open.

---

## R7. ⚠ **OPEN** — two component records exist only as certification evidence

`components/espressif/esp32-s3-wroom-1/` and `esp32-s3-wroom-1u/` now contain
`artifacts/certification/` and `acquisition/manifest.json` but **no component `README.md`**. They
were created so the two positive-control filings would not sit outside the repository without a
placeholder trail.

The module is fitted on **several documented boards**, so a real record is worth writing.
**A maintainer should decide:** write the records, or fold the evidence into
`components/espressif/esp32-s3r8/`. A note saying exactly this is appended inside each
directory's README.

---

## R8. Counts in `VERIFICATION-sweep-2026-09-04.md` §2 and §3 are superseded, not wrong

Round one reported 10,387 links / 1 broken and 61 typed artifacts / 0 mismatches. Re-run on
2026-09-11: **10,940 links / 2 broken** and **1,219 typed artifacts / 3 mismatches**.

The deltas are **scope, not regression** — round one validated only artifacts *it added*, and the
link count grew with the tree. Both new findings are pre-existing:

- the extra broken link is the same vendored upstream README round one already excluded;
- the 3 mismatches are **JPEGs named `.png`** in a vendored Waveshare example, tracked since
  commit `cbfbff3`.

✅ **Applied** as a round-two section in that report. §2 and §3 are **unedited**.
