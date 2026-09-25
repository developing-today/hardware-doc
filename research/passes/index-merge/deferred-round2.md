# Deferred — round two, 2026-09-11

Content that is real, applicable and **deliberately not applied** by the round-two index merge.
Companion to round one's [`deferred.md`](deferred.md), which is unchanged.

Two reasons appear below: **a live session owns the file**, or **the work is outside this
task's target list**. Neither means the content is wrong.

---

## 1. ⛔ `devices/m5stack/papermono/**` — a live session owns it

`devices/m5stack/papermono/` and `VERIFICATION-m5stack-papermono.md` were modified **minutes
before** this pass started and kept changing throughout it (`gaps-and-conflicts.md` at 18:43,
`software/ecosystems/crosspoint-freeink/*` at 18:53). **Nothing under that tree was read-modified
or written.**

### 1.1 Eleven FCC exhibits, parked rather than filed

`2AN3WM5PAPERMONO` — **M5PaperMono**, M5Stack Technology Co.,Ltd, granted **2025-07-09**, test
firm Shenzhen Huak Testing Technology Co., Ltd. The exhibits are harvested and hashed, and would
have gone to `devices/m5stack/papermono/artifacts/certification/`:

| Exhibit | Type | Bytes | FCC doc id | Would go to |
|---|---|---:|---|---|
| `Antenna Specification` | Test Report | 2,362,575 | 9552975 | `2AN3WM5PAPERMONO-antenna-specification.pdf` |
| `External Photos` | External Photos | 358,814 | 9552995 | `2AN3WM5PAPERMONO-external-photos.pdf` |
| `Internal Photos` | Internal Photos | 1,368,012 | 9552996 | `2AN3WM5PAPERMONO-internal-photos.pdf` |
| `Label and Label Location` | ID Label/Location Info | 402,449 | 9553000 | `2AN3WM5PAPERMONO-label-and-label-location.pdf` |
| `RF Exposure Information` | RF Exposure Info | 100,267 | 9552998 | `2AN3WM5PAPERMONO-rf-exposure-information.pdf` |
| `SAR Calibration Certificates` | RF Exposure Info | 830,308 | 9552980 | `2AN3WM5PAPERMONO-sar-calibration-certificates.pdf` |
| `SAR EUT Test Position Photos` | RF Exposure Info | 1,248,669 | 9552979 | `2AN3WM5PAPERMONO-sar-eut-test-position-photos.pdf` |
| `SAR Return Loss & Impedance Measurement` | RF Exposure Info | 464,511 | 9552981 | `2AN3WM5PAPERMONO-sar-return-loss-impedance-measurement.pdf` |
| `SAR Scan Plots` | RF Exposure Info | 476,275 | 9552982 | `2AN3WM5PAPERMONO-sar-scan-plots.pdf` |
| `SAR Test Report` | RF Exposure Info | 1,718,829 | 9552983 | `2AN3WM5PAPERMONO-sar-test-report.pdf` |
| `User Manual` | Users Manual | 1,433,361 | 9553004 | `2AN3WM5PAPERMONO-user-manual.pdf` |

Total: 11 files, 10.27 MiB

They remain at `scratch/market-and-certification/fcc/2AN3WM5PAPERMONO/`, **unmoved and
unmodified**. Full metadata — URL, SHA-256, byte size, publication date — is in
[`plan.json`](plan.json), filtered on `"disposition": "park"`.

**To land them later**, when that tree is quiet:

```bash
python3 scratch/index-merge/plan-artifact-split.py          # re-plan; re-reads live state
# then remove '2AN3WM5PAPERMONO' from PARKED in plan-artifact-split.py
python3 scratch/index-merge/apply-artifact-plan.py --apply
python3 scratch/index-merge/write-cert-records.py --apply
```

Under the same split rule as everywhere else, **Internal Photos (1,368,012 B) and Label
(402,449 B) belong in the repository** and the other nine are archive-with-placeholder.

⚠ **This is a knowing, temporary violation of the method's "nothing useful may exist in only one
place" rule.** The exhibits are currently in scratch with no placeholder. That is the lesser
harm against corrupting a live session's tree, but it **is** a debt and it should be paid.

### 1.2 The PaperMono certification record is now wrong, and was not corrected

`devices/m5stack/papermono/` states in at least seven places that **no certification of any kind
is published for this board** — `README.md:58`, `coverage.md:36,38`, `media.md:41,71,142`,
`sources.md:53,204`, `gaps-and-conflicts.md:325` (`G2`),
`features/wifi-and-bluetooth.md:87,113`, `features/lora.md:12,165`, `features/nfc.md:175`.

The narrow claim **survives**: `docs.m5stack.com/en/certification` really does return zero matches
for `PaperMono` and `C153`, and `sources.md:53` is careful to say so — *"It does not establish
that no certification exists — only that M5Stack publishes none. An FCC grantee-database search
was **not** attempted."* **That caveat was correct and is now resolved.**

**`2AN3WM5PAPERMONO` exists, granted 2025-07-09.** The same correction applies to two component
records that inherited the claim from PaperMono:

- `components/m5stack/stamp-lora-1262/README.md:143` (`G5` — *"No regulatory identifier of any kind"*)
- `components/semtech/sx1262/README.md:527,641` (`G14`) and `components/stmicroelectronics/st25r3916/README.md:435` (`C10`)

⚠ `components/m5stack/stamp-lora-1262/README.md` is **also** being edited by the live session —
see §4 — so it was left alone too. `components/semtech/sx1262/README.md` and
`components/stmicroelectronics/st25r3916/README.md` were quiet but are **PaperMono's claims in
PaperMono's words**; correcting them while the owning record stays stale would leave the tree
inconsistent in a *new* way. **Deferred as a set, to be applied together.**

**Note the shape of the error is the same one the Xteink pass made** and that this merge
corrected across 13 files: confusing *"the vendor publishes no identifier"* with *"no grant
exists"*. Worth checking for wherever it appears.

### 1.3 The richest untraced schematic in the repository

`PaperMono_SCH_V0.6.2_20260522.pdf` — 6 pages, 3,951 words, **144 `NL` net-label tokens**,
`Creator: Altium Designer`, only 2 embedded rasters. The net-tracing pass assessed it as **the
most traceable sheet held** and obtainable in under an hour by the method in
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md).
Nothing was extracted beyond the census entry. **Highest-value single item on this page.**

---

## 2. `ai-crawler-site-access-table.md` — live, and large

Last modified **18:47**, inside the 15-minute window, by the same session working `software/`.
[`archive/guides/research/artifacts/certification-and-market-2026-09-11/index-fragments.md`](../../../archive/guides/research/artifacts/certification-and-market-2026-09-11/index-fragments.md) §7 *(was `scratch/market-and-certification/…`; relocated 2026-09-20)*
carries a substantial paste-ready block that is **not applied**:

| Finding | Why it matters |
|---|---|
| **`fccid.io` serves an inverted Cloudflare block** — 403 to a Chrome UA, 200 to `curl/8.5.0`, `WhatsApp/2.23.20.0`, `ChatGPT-User/1.0`, `ClaudeBot/1.0`. Measured across 5 UAs × 4 paths; matrix at `scratch/market-and-certification/logs/ua-matrix.txt` | Directly contradicts `AGENTS.md`'s default escalation, which is to *reach for* a browser UA. Here that is the one that fails |
| ⚠ **The root `https://fccid.io/` returns 200 to every UA including Chrome** | A reachability probe against the root reports a **false success**. Probe a deep path |
| Exhibit URL form `https://fccid.io/<FCC-ID>/<Type-Slug>/<Doc-Slug>.pdf` — **the `.pdf` suffix is required**, else a 16 KB HTML viewer. 170 PDFs fetched 2026-09-11, 0 failures | |
| `fcc.report` — **403 to all five UAs.** Not a UA problem; no working path found | |
| `www.fcc.gov` / `apps.fcc.gov` — **403 to all five UAs** for `/oet/ea/fccid`, `/oetcf/eas/reports/GenericSearch.cfm`, `/eas/GetApplicationAttachment.html`. `opendata.fcc.gov/resource/kfc9-pnvf.json` → **404** | The *official* FCC search is unusable from this host. Use the mirror and **label it a mirror** |
| Marketplaces 2026-09-11: AliExpress 200 **with a bot-wall body**; eBay **403**; Amazon 200 **with no prices in the HTML**; Taobao/JD 200 **SPA shells** (34 KB / 2.7 KB) | **A 200 containing no prices is a failure**, and should be recorded as one |
| `wireless.miit.gov.cn`, `www.srrccn.org` — **connection failure (`000`)**. `miit.gov.cn`, `cnca.gov.cn` 200 but portals, not registers | |
| `https://www.tele.soumu.go.jp/giteki/SearchServlet?pageID=js01` → **200**, browser UA, no login. Form-driven, not queried | A real, reachable route nobody has used yet |

These are **exactly** the findings `AGENTS.md` rule 8 says to record. They are deferred only
because the file was live.

---

## 3. Outside this task's target list

| Item | Where it is | Why not applied |
|---|---|---|
| **`software/README.md`** entries | six round-one fragments + round two | The whole `software/` tree was **live throughout** this pass (last write 18:53). Still outstanding from round one |
| **`guides/markets/*`** — the X4 Classic at $79 replacing the X4, the X4 Light as an unannounced certified product, **and the grantee-enumeration technique as a generalisable method** | `archive/devices/xteink/shared-artifacts/research-scratch/index-fragments-round2.md` §6, `scratch/market-and-certification/index-fragments.md` §4 | `guides/markets/` was marked protected by three sessions in round one and is not in this task's target list |
| **`guides/markets/README.md`** pricing-coverage note — dated M5Stack and LilyGO store pricing now lives in each device's `market-and-pricing.md`; **marketplace/clone/used pricing remains unsampled** | `scratch/market-and-certification/index-fragments.md` §4 | as above |
| **`vendors/m5stack/README.md`** — the Cardputer pass's nine product ids and its §5.6/§5.7 traps | round one | carried over from round one's [`deferred.md`](deferred.md) §3, still unapplied |
| Four vendor guides unlinked from `vendors/README.md`: `dke`, `everest-semiconductor`, `omnivision`, `solder-party` | pre-dates both rounds | pre-existing defect, not this pass's to fix, but **it is still there** |

---

## 4. Files skipped on a liveness check

`find <file> -mmin -15` was run immediately before every edit. These were live and were **not
touched**:

| File | Last write | Note |
|---|---|---|
| `devices/m5stack/papermono/**` | 18:43 and continuing | task-forbidden regardless |
| `software/**` | **18:53** — during this pass | same session |
| `ai-crawler-site-access-table.md` | 18:47 | §2 above |
| `components/m5stack/stamp-lora-1262/README.md` | live session's own deletions | §1.2. ⚠ Exhibits *were* filed into `components/m5stack/stamp-lora-1262/artifacts/certification/` — **new files only**, no read-modify-write of the README |
| `components/unidentified/xteink-x3-x4/README.md`, `components/generic/kh3216-a35-chip-antenna/README.md`, `components/{belling/bl8075,cellwise/cw2017}/README.md` | 18:41–18:44 | indexed from `components/README.md`; **their own records were not edited** |
| `VERIFICATION-xteink-round2.md` | 18:50 | linked from the root `README.md`; **not edited** |

---

## 5. Two pre-existing defects found while verifying, reported not repaired

- `software/applications/crosspoint-reader/plugins/source-snapshots.ARCHIVED.md` — a placeholder
  with **no SHA-256, no byte size and no original path**. It has 4 URLs, so it is not useless,
  but it does not meet the method's self-sufficiency contract. **In the live tree — not touched.**
- `devices/seeed-studio/xiao-esp32s3-sense/artifacts/wiki-snapshot/sites/TRANSLATIONS.ARCHIVED.md`
  — carries a hash and a size but never states the **original path** of what was archived.
- Three files named `*.png` in
  `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/examples/selected/…/images/` are **JPEGs**
  (`ff d8 ff db`). Tracked, committed in `cbfbff3`, vendored from a community example. Real
  images, wrong extension — **not** an HTML error page saved as a document, which is the failure
  mode the magic-byte check exists to catch. Renaming them would be a delete-plus-add in a
  vendored tree, so they are reported instead.

---

# Discharged — 2026-09-20

*Appended, not rewritten. Everything above is preserved as it was written on
2026-09-11.*

## §1.1 and §1.2 — paid in full

`devices/m5stack/papermono/**` was quiet on 2026-09-20 and the parked work has
been done.

**The eleven exhibits are filed.** Under the same split rule §1.1 anticipated:

| Disposition | Files | Bytes | Where |
|---|---:|---:|---|
| Retained in repository | 2 | 1,770,461 | `devices/m5stack/papermono/artifacts/certification/` — Internal Photos + Label |
| Archived with placeholders | 9 | 8,993,609 | `archive/devices/m5stack/papermono/artifacts/certification/` |

Every SHA-256 in §1.1's table was re-verified **after** the move and matches the
2026-09-11 harvest. Directory index with hashes, URLs and FCC document ids:
`devices/m5stack/papermono/artifacts/certification/README.md`.

**The "nothing useful may exist in only one place" debt flagged in §1.1 is
cleared.** Each of the nine archived exhibits now has a self-sufficient
placeholder carrying hash, byte size, FCC document id, publication date and five
reacquisition URLs.

**The exhibits were mined before they were archived**, which §1.1 did not ask
for but the method requires: `devices/m5stack/papermono/certification.md`.

**§1.2's corrections are applied**, across eleven device files and six component
records. `G2` is closed in `gaps-and-conflicts.md` with the original wording
preserved and the refutation stated. The three component claims §1.2 named —
`stamp-lora-1262` G5, `sx1262` G14, `st25r3916` C10 — are struck through and
corrected in place.

## ⚠ Two facts in §1.1 and §1.2 above are wrong

Recorded rather than silently edited, because a future reader may have copied
them.

| Field | §1.1 / §1.2 says | Actual | Evidence |
|---|---|---|---|
| Grant date | **2025-07-09** | **2026-08-12** | both grant certificates, `_filing.html`; SAR report is dated 2026-07-25 and the sample was received 2026-07-14, so a 2025 grant is chronologically impossible |
| Test firm | **Shenzhen Huak Testing Technology Co., Ltd.** | **Shenzhen Accurate Technology Co., Ltd.** (A2LA 4297.01) | SAR report pp. 1, 7; filing index |

Both look like values carried over from a neighbouring filing during the
round-2 harvest. **Worth checking whether the same two fields are wrong in any
of the 32 `certification-and-compliance.md` files that pass generated** — this
was not checked.

## §1.3 — not done

The schematic net-tracing pass on `PaperMono_SCH_V0.6.2_20260522.pdf` was **not**
attempted. Still the highest-value single item on this page.

Note that it is now **less** urgent than it was: M5Stack's FCC label exhibit
turned out to be its full architecture diagram, and it independently reproduces
**30 of 31 GPIO assignments** already in `pinouts-and-buses.md`. Net tracing
would still add the passive network, designators and the sheets the label omits —
and it would settle **C26**, the one row where the label and the schematic
disagree.
