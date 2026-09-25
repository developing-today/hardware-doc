# Corrections — adjudicated

Companion to [`corrections-requiring-review.md`](corrections-requiring-review.md).
Written **2026-09-11** by the certification/market pass.

> **Nothing here has been applied.** Several of these items touch files owned by other sessions,
> and one (`dcdc-u4`) is contested by a concurrent agent. Each entry gives a **verdict**, the
> **primary evidence** it rests on, and the **exact one-line patch** a maintainer would apply, so
> the whole set can be landed in one pass.

> ⚠ **Date.** The brief for this pass said 2026-09-07. Host clock and two independent servers'
> `date:` headers say **2026-09-11**. Retrieval dates below are 2026-09-11. Dates carried over
> from earlier passes are left as those passes recorded them.

## Concurrency notice — read before applying #1 and #6

A **sibling agent is tracing schematics in this repository right now**. Items **#1 (`dcdc-u4` /
JW5712)** and **#6 (TP4057 charge current)** both sit squarely in its path, and it may reach
these questions independently and with better evidence than a PNG crop and a datasheet table.

- If its conclusion **agrees** with the verdicts below, apply the patches.
- If it **disagrees**, do **not** pick between us on authority. The disagreement is itself the
  finding; record both, cite both, and say what would settle it. That is the house rule the
  2026-09-04 sweep followed and it is the right one.
- Files owned by that agent — `pinouts-and-buses.md`, `schematic-*.md` — were **not read,
  written or relied upon** by this pass.

---

## Summary

| # | Subject | Verdict | Strength |
|---|---|---|---|
| 1 | `dcdc-u4` is `JW5712` | ✅ **Correction upheld** — the part number is present and legible | **Primary**, independently re-verified |
| 2 | RadioLib licence | ✅ **Correction upheld** — RadioLib is **MIT** | **Primary**, `executed-success` |
| 3 | Semtech vendor guide reference | ✅ **Correction upheld** — the guide exists | **Primary**, filesystem |
| 4 | Two PaperMono X4 Pro claims | ✅ **Both upheld** — price confirmed; reflashability **partially** confirmed | Price **primary**; reflashability **not re-verified here** |
| 5 | `pcf85063a` stale link line | ✅ **Correction upheld** — the line is stale | **Primary**, filesystem |
| 6 | TP4057 charge current at 3.3 kΩ | ⚠ **~300 mA is right on the physics** — but the conflict is *not* fully resolved | **Primary datasheet**, but the board-level question is open |

---

## 1. `components/unidentified/m5stack-stamp-s3a/dcdc-u4/` — the part **is** `JW5712`

**Verdict: the correction is right. The DinMeter pass's claim is wrong.**

### Evidence — independently re-verified, not taken on trust

The corrections file cites a schematic render. This pass re-fetched it from scratch rather than
accepting the earlier reading.

| Step | Result |
|---|---|
| Re-fetch `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1150/Sch_StampS3_v0.3.3_page_01.png` | **HTTP 200**, 1 483 535 bytes, 2026-09-11 |
| SHA-256 | `1156e645de35fe68e6458e9131657c8f02045bbcd14f97ab190bb1486ee7a1c5` |
| Match against the hash in `corrections-requiring-review.md` §1 | ✅ **byte-identical** |
| Native resolution | 5848 × 4132 |
| Crop `1200×600+1000+3300`, upscaled 200% | **`JW5712` rendered in blue directly beneath the symbol body, plainly legible** |

The same crop also shows the pin names **`EN`, `VIN`, `GND`, `SW`, `VOS`, `VSEL1`, `VSEL2`,
`VSEL3`**, with `SW` → inductor → `VDD_3V3`, `VSEL1/2/3` tied to `VIN_5V`, `R16 100K/1%` on `EN`,
`C18 100nF/25V` on `VIN` and `C15 1nF/25V` on the output. That pin complement — **three `VSEL`
straps, a `VOS` remote sense, and no feedback divider** — is exactly what
[`components/joulwatt/jw5712`](../../../components/joulwatt/jw5712/README.md) documents, and it is
not a generic buck pinout. The identification is corroborated by function, not only by text.

The DinMeter pass's stated reason for finding no text — *"the symbol carries no part-number
text"* — is consistent with the diagnosis in the corrections file: a **marker-layer-only PDF
parse never enters the Form XObject where the text lives, and fails silently.** The rendered PNG
bypasses that entirely.

### FCC internal photos were checked and did **not** help

`2AN3WM5STAMPS3A` Internal Photos were downloaded (2026-09-11) and rendered at 2835 × 2126, then
cropped and upscaled 300%. **The DC-DC package marking is not legible** — a ~2 mm DFN at that
image scale carries no readable text. This is recorded as a **negative result**: photographic
confirmation of `U4` is *not* available from the FCC filing, and a future agent should not
re-attempt it expecting a different outcome.

So the evidence is: **one primary source (the vendor schematic), independently re-fetched and
hash-matched, plus functional corroboration.** No second independent source exists.

### Patch

`components/unidentified/m5stack-stamp-s3a/dcdc-u4/README.md`, the line reading
*"**Manufacturer / part number:** ⚠ **NOT ESTABLISHED.** …"* →

```markdown
**Manufacturer / part number:** **JoulWatt JW5712** — identified 2026-09-04, re-verified 2026-09-11. See [`components/joulwatt/jw5712`](../../../joulwatt/jw5712/README.md). This directory is retained as a redirect stub only.
```

Then retire the directory to a stub, per the ready-made text in `archive/devices/m5stack/shared-artifacts/cardputer/research-scratch/index-fragments.md` §0.

⚠ **`dcdc-u4` is contested by a concurrent agent.** Confirm with it before applying.

> Worth preserving from the DinMeter pass, as the corrections file already notes: its
> identification of `MUN3CAD01-SC` as a **Murata µPOL module** is **correct**.

---

## 2. `components/semtech/sx1262/README.md` §9 — RadioLib is **MIT**

**Verdict: the correction is right, and this one is not close.**

### Evidence — `executed-success`, 2026-09-11

```console
$ gh api repos/jgromes/RadioLib --jq '{spdx:.license.spdx_id,name:.license.name}'
{"key":"mit","name":"MIT License","spdx":"MIT"}

$ gh api repos/jgromes/RadioLib/contents --jq '.[]|select(.name|test("(?i)licen[cs]e"))'
license.txt  1068B  sha=201215f256b25b620461ad16e227ae2a5b32303f

$ gh api repos/jgromes/RadioLib/contents/license.txt --jq .content | base64 -d | head -3
MIT License

Copyright (c) 2018 Jan Gromeš
```

The file is **`license.txt`, lower case**, which is why a `LICENSE` fetch 404s — the likely
origin of the LGPL-3.0 belief, exactly as the LoRa-generations pass diagnosed. Two independent
confirmations: GitHub's own licence detection, and the file contents.

There is **no licence mismatch** with the MIT-licensed M5Stack demos.

### ⚠ The corrections file undercounts the blast radius

It says *"the same wrong claim appears in at least three more places"* and lists three. A
repo-wide grep on 2026-09-11 finds **11 un-annotated occurrences across 8 files** (excluding the
two lines at `sx1262/README.md:501–502`, which are the original + its in-place correction):

| File | Line | Form |
|---|---|---|
| `components/semtech/sx1262/README.md` | 751 | source-table row S-6, *"upstream licence LGPL-3.0 (**unverified**)"* |
| `components/m5stack/stamp-lora-1262/README.md` | 125 | *"RadioLib is **LGPL-3.0** upstream"* |
| `components/m5stack/stamp-lora-1262/README.md` | 291 | source-table row S-5, same wording |
| `devices/m5stack/papermono/features/lora.md` | 59 | *"RadioLib is LGPL-3.0 upstream"* |
| `devices/m5stack/papermono/development.md` | 166 | *"RadioLib's licence is not MIT … RadioLib is LGPL-3.0"* |
| `devices/m5stack/papermono/development.md` | 461 | *"RadioLib's LGPL-3.0 obligations were not analysed"* |
| `devices/m5stack/cardputer-adv/acquisition/README.md` | 157 | *"MIT repo that **pins LGPL-3.0 RadioLib**"* |
| `devices/m5stack/cardputer-adv/sources.md` | 40 | *"MIT ⚠ pins LGPL-3.0 RadioLib"* |
| `devices/m5stack/cardputer-adv/factory-firmware.md` | 15 | *"vendors/pins **RadioLib** which is **LGPL-3.0** upstream"* |
| `devices/m5stack/cardputer-adv/factory-firmware.md` | 77 | code-tree comment *"⚠ LGPL-3.0 upstream"* |
| `guides/lora/README.md` | 587 | *"Stamp record notes RadioLib as LGPL-3.0 upstream"* |

`artifact-manifest.md:2035` already carries a ⚠ pointer and is correctly excluded.
`guides/hardware/adding-lora-nfc-and-sidelight-to-eink-firmware.md:256` already says **MIT** and
flags the discrepancy — it needs only the "unresolved" wording dropped.

**`devices/m5stack/papermono*` and `guides/lora/` were not touched by this pass.**

### Patch

Eleven one-line edits. The canonical replacement:

```markdown
RadioLib is **MIT** (`license.txt`, lower case — a `LICENSE` fetch 404s). Verified `executed-success` 2026-09-04, re-verified 2026-09-11: `gh api repos/jgromes/RadioLib --jq .license.spdx_id` → `MIT`. **No licence mismatch.**
```

⚠ **One genuinely open sub-question remains**, raised by
`guides/hardware/adding-lora-nfc-and-sidelight-to-eink-firmware.md:256`: the licence of the
**pinned 7.2.1 tree specifically** was checked by the LoRa-generations pass (byte-identical at
tags `7.2.1` and `7.7.1`) but the *vendored copy inside M5Stack's demo* was not separately
diffed. That is a smaller question and should not block these edits.

---

## 3. `components/semtech/sx1262/README.md` §11 / §13 — the Semtech guide exists

**Verdict: the correction is right. Trivially verifiable.**

### Evidence

```console
$ ls -la vendors/semtech/README.md
-rw-r--r-- 1 user users 33753 Sep  7 05:54 vendors/semtech/README.md
```

33 753 bytes, written 2026-09-07. §11 already carries an in-place note. **§13's *"no Semtech
guide exists yet"* is still wrong and still unannotated.**

### Patch

`components/semtech/sx1262/README.md` §13, the clause *"**no Semtech guide exists yet**; §11 is
what one would open with"* →

```markdown
see [`vendors/semtech/README.md`](../../../vendors/semtech/README.md), written 2026-09-07 using §11 as its starting point
```

The **G12** sub-question (2025-04-07 listing date vs Dec 2024 revision) stays `unresolved`, now
correctly understood as a *catalogue listing-date field*, not a document date. Leave it open.

---

## 4. `devices/m5stack/papermono/comparisons-and-recommendations.md` — two X4 Pro claims

**Verdict: claim 2 is confirmed with primary evidence. Claim 1 is upheld but on weaker
evidence than claim 2, and this pass did not independently re-verify it.**

### Claim 2 — *"the XTEINK X4 Pro … was never priced"*. **Wrong.**

Independently re-observed **2026-09-11** from `https://xteink.com/products.json?limit=250&page=1`:

| Variant | SKU | Price | Stock |
|---|---|---|---|
| Space Black | `X4Pro-Black` | **USD 99.00** | ✅ available |
| + Mist Sage Base | `X4PB+BW` | USD 115.00 | ❌ |
| + Space Black Base | — | USD 115.00 | ❌ |

`published_at` 2026-07-21. **Two independent observations a week apart — 2026-09-04 by the
Xteink pass, 2026-09-11 by this one — both USD 99.00.** The claim is false on both dates, and
is repeated in that record's `market-and-pricing.md` and `gaps-and-conflicts.md`.

Citation form: *USD 99.00, 1 unit, retrieved 2026-09-11,
`https://xteink.com/products/xteink-x4-pro-pocket-ereader`, ships from CN (origin not stated).*

### Claim 1 — *"a sealed consumer reader … You cannot put your own application on it."*

The correction asserts it is reflashable via OTA unlock, SD-card install, or a vendor
developer-unlocked variant, with four independent open-source firmwares targeting it.

**This pass did not re-verify that**, and says so rather than laundering another session's
finding into a fresh-looking confirmation. What this pass *can* add, as corroborating
circumstance:

- Xteink holds **FCC `2BTR9-X4PRO`**, granted 2026-06-16 — the product is a real, certified,
  currently-sold device, not a one-off.
- The **X4 internal photos** show a bare ESP32-class QFN with an etched PCB antenna, a microSD
  socket and a USB receptacle — a **conventionally reflashable architecture**. That is
  consistent with the correction and inconsistent with "sealed", though it is the X4, not the
  X4 Pro, and it is architecture rather than a demonstrated flash.
- **The X4 Pro's own internal photos unlock on 2026-12-12** and will settle the hardware half.

**Recommend applying claim 2 now; hold claim 1 until someone re-verifies the four firmwares.**

### Patch

In `devices/m5stack/papermono/comparisons-and-recommendations.md`, replace the *"was never
priced"* clause with:

```markdown
the XTEINK X4 Pro — the comparison the community actually makes — is **USD 99.00** (retrieved 2026-09-04 and again 2026-09-11, `https://xteink.com/products/xteink-x4-pro-pocket-ereader`, ships from CN)
```

Ready-to-paste replacement text for claim 1 is in `archive/devices/xteink/shared-artifacts/research-scratch/index-fragments.md` §6.

❌ **`devices/m5stack/papermono*` is owned by another pass. Nothing was written there.**

---

## 5. `components/nxp/pcf85063a/README.md` — the stale "no record page yet" line

**Verdict: the correction is right. The line is stale.**

### Evidence

```console
$ ls -la components/nxp/pcf8563/README.md
-rw-r--r-- 1 user users 3204 Sep  7 06:17 components/nxp/pcf8563/README.md
```

The record was created 2026-09-07 by the LilyGO T-Display-S3 pass. The line at
`components/nxp/pcf85063a/README.md:767` still reads *"Artifacts-only directory; no record page
yet"*. The two links in `components/generic/bm8563/README.md` that the Xteink pass reported
broken now resolve — the breakage self-healed, as the corrections file records.

This is the **lowest-risk item in the set**: one stale clause, no contested ownership, no
concurrent agent.

### Patch

`components/nxp/pcf85063a/README.md` line 767 →

```markdown
- [nxp/pcf8563](../pcf8563/README.md) — same I²C address, different register map. §12.1. Record page created 2026-09-07; [datasheet](../pcf8563/artifacts/pcf8563-datasheet-rev-11.pdf)
```

---

## 6. ⚠ TP4057 charge current at `R_PROG` = 3.3 kΩ — 100 mA vs ~300 mA

**Verdict: ~300 mA is correct for the part at 3.3 kΩ. The 100 mA figure is the datasheet's
10 kΩ row. But the *board-level* question is not closed, and I am not closing it.**

### The primary evidence neither pass consulted

Both records reason about the TP4057 without opening the datasheet — the corrections file says
so explicitly: *"the datasheet was not consulted by either pass."* **It was sitting in the
repository the whole time**, at
`components/generic/tp4057/artifacts/tp4057-datasheet-cn-m5stack-mirror.pdf` (628 588 bytes,
Chinese, M5Stack mirror).

Extracted 2026-09-11 with `pdftotext -layout` (poppler 26.06.0), `executed-success`.
From the electrical characteristics table:

| Parameter | Condition | Min | Typ | Max | Unit |
|---|---|---|---|---|---|
| `IBAT` 充电电流 | 恒流模式, **RPROG = 10 kΩ** | 93 | **100** | 107 | mA |
| `IBAT` 充电电流 | 恒流模式, **RPROG = 2 kΩ** | 465 | **500** | 535 | mA |
| `VPROG` PROG 引脚电压 | 恒流模式, RPROG = 10 kΩ | 0.93 | **1.0** | 1.07 | V |

The part is titled **「500mA线性锂离子电池充电器」** — a 500 mA linear Li-ion charger — and the
datasheet states the charge current is set by an external resistor between `PROG` and `GND`.

Both table rows satisfy `I_CHG = 1000 × V_PROG / R_PROG` with `V_PROG` = 1.0 V:

- 10 kΩ → 1000 × 1.0 / 10 000 = 0.100 A ✅ matches the 100 mA row
- 2 kΩ → 1000 × 1.0 / 2 000 = 0.500 A ✅ matches the 500 mA row

**Therefore at 3.3 kΩ: 1000 × 1.0 / 3 300 = 0.303 A ≈ 303 mA.**

### What that settles, and what it does not

✅ **Settled:** the **formula the Cardputer pass used is the datasheet's own**, and its ~300 mA
figure is right for a 3.3 kΩ programme resistor. 303 mA is comfortably inside the part's 500 mA
capability, so the answer is not clipped.

✅ **Settled:** **100 mA is exactly the datasheet's `RPROG = 10 kΩ` row.** The coincidence is too
clean to be chance. Somebody — M5Stack's documentation, or the DinMeter pass reading it — took
the datasheet's example row as if it were this board's result.

❌ **Not settled: which resistor is actually fitted on each board.** There are two live
possibilities and this pass cannot choose between them:

| | If R is genuinely 3.3 kΩ on both boards | If the DinMeter fits 10 kΩ and the record's "3.3 kΩ" is wrong |
|---|---|---|
| DinMeter | 100 mA figure is **wrong**, ~300 mA is right | 100 mA figure is **right**, the resistor value in the record is wrong |
| Cardputer | ~300 mA right either way | ~300 mA right |

Note the records also disagree on **designators** — DinMeter says `U2`/`R13`, Cardputer says
`U1`/`R5` — which is itself consistent with these being two different schematics rather than one
transcription error. The corrections file's instinct that "the two boards differ in a way
neither record captures" is live and I cannot exclude it.

> ⏭ **This is the sibling schematic-tracing agent's question.** Reading the actual value of
> `R13` on the DinMeter schematic and `R5` on the Cardputer schematic settles it in one look.
> **If that agent's reading conflicts with the analysis above, do not pick — record both.** My
> evidence is a datasheet table and arithmetic; it says what the *part* does at a given
> resistance. It says nothing about what resistance is *fitted*, and on that question a
> schematic beats me outright.

### Patch

**Do not edit either figure yet.** Instead append to `components/generic/tp4057/README.md` the
one line that is safe regardless of how the resistor question lands:

```markdown
**Datasheet, `executed-success` 2026-09-11** (`artifacts/tp4057-datasheet-cn-m5stack-mirror.pdf`, `pdftotext -layout`): the part is a **500 mA** charger; the electrical table gives **100 mA typ at RPROG = 10 kΩ** and **500 mA typ at RPROG = 2 kΩ**, with `VPROG` = 1.0 V — confirming `I = 1000 × V_PROG / R_PROG`. **At 3.3 kΩ this part sources ≈303 mA.** The 100 mA figure recorded above is precisely the datasheet's 10 kΩ row. ⚠ **Which resistor is actually fitted on each board is not established here** — see [`research/passes/index-merge/corrections-adjudicated.md`](corrections-adjudicated.md) §6.
```

Once the resistor values are confirmed from schematics, **then** correct whichever figure loses.

---

## Item 7 of the original file — housekeeping

Not adjudicated; it is a to-do list, not a disagreement. Re-verified 2026-09-11 that
`vendors/semtech/README.md` exists (33 753 B). The four still-unlinked vendor guides
(`dke`, `everest-semiconductor`, `omnivision`, `solder-party`) and the three orphan
`vendors/README.md` table rows were **not touched** — `vendors/README.md` is on this pass's
do-not-edit list.

One addition to that list, found by this pass: **`VERIFICATION-sweep-2026-09-04.md` §6's
certification bullet is now known to be wrong**, not merely weak. See
[`archive/guides/research/artifacts/certification-and-market-2026-09-11/xteink-certification-and-pricing.md`](../../../archive/guides/research/artifacts/certification-and-market-2026-09-11/xteink-certification-and-pricing.md) §1. *(Was `scratch/market-and-certification/…`; relocated 2026-09-20.)*
That file is on the do-not-edit list too, so it is flagged here rather than annotated in place.
