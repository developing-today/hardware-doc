# Verification — Xteink device family

> Research session **2026-09-04**. Scope: `devices/xteink/**` plus the component
> records created or extended for it. Verifier: the authoring session (self-audit).

## Headline

**Zero claims in this tree were verified on hardware by this session.** No Xteink
device was available. Every hardware statement is either reverse-engineering
evidence produced by a third party (the FreeInk SDK), a teardown photograph, a
parsed firmware image, a vendor API response, or a labelled community report.

That is stated first because it is the most important limitation of the whole
body of work.

## 1. Inventory

| Area | Files |
|---|---:|
| `devices/xteink/` | **112** |
| `components/ultrachip/` (index + uc8253, uc8179, uc8279) | 4 |
| `components/cellwise/` (index + cw2017) | 2 |
| `components/espressif/esp32-c3/` | 1 |
| `components/texas-instruments/bq27220/` | 1 |
| `components/unidentified/xteink-x3-x4/` (index + 4 parts) | 5 |
| **Total authored** | **125** |

Per device: `x4-pro` 33 · `x3` 29 · `x4` 28 · `x4-classic` 13 · `s4` 7 ·
`nano` 1 · family index 1.

Byte total for `devices/xteink/`: **536,576 B** of authored Markdown/JSON
(excludes symlinks into the archive).

## 2. Artifacts — validated by content, not extension

| Artifact | Bytes | Magic | SHA-256 | Result |
|---|---:|---|---|---|
| `xteink-x4-oem-full-flash-16mb.bin` | 16,777,216 | first byte `0xE9` = ESP image | `b9cf27cc254c737c901f81e7fcf0c48308e29bd979848ab0ac0bf6c6f5e8c245` | **valid** |
| X3 teardown, Imgur set | 19,513,196 | 13 files, all `FF D8 FF` | per-file, in placeholder + `manifest.json` | **valid** |
| X3 teardown, `sunwoods` set | 5,034,272 | 10 files, all `FF D8 FF` | per-file, in placeholder | **valid** |

- **23 of 23 JPEGs** validated by magic bytes. **0 invalid.**
- **0 files** found to be HTML saved under a `.bin` / `.jpg` / `.pdf` extension.
- The flash image's chip-id field independently reads **5 = ESP32-C3**,
  corroborating the SoC family from a second, machine-readable direction.

### Archive integrity

```
python3 tools/archive_artifact.py --repo-root . --manifest … --verify
  → verified 3, missing 0, drifted 0
```

Three-link chain confirmed for all three archived artifacts: placeholder at the
former path ✅ · symlink resolving through this repo's own `archive/` link ✅ ·
cited from the owning device record ✅.

`tools/audit_archive.py` flags the Imgur set as **"[no repo]"** — correct and
expected: it is an Imgur album, not a repository. Its placeholder carries **two
independent hosts** (`imgur.com` and `old.reddit.com`), satisfying the two-source
rule.

## 3. Links

| Check | Result |
|---|---|
| Markdown files checked | 123 |
| Relative links resolved | **650** |
| **Broken** | **0** |

Two broken links were found and fixed during verification
(`x4-pro/acquisition/README.md` → `../gaps-and-conflicts.md`;
`x4-pro/features/buttons.md` → a non-existent `x3/features/buttons.md`).

**One pre-existing broken link was found and deliberately not fixed:**
`components/generic/bm8563/README.md` links twice to
`../../nxp/pcf8563/README.md`, which does not exist — `components/nxp/pcf8563/`
contains only an `artifacts/` directory. That file belongs to a concurrent
session; the breakage predates this work and repairing another session's prose was
out of scope. **Reported, not repaired** — see
`scratch/xteink/index-fragments.md`.

## 4. JSON

All 6 machine-readable manifests parse: five `acquisition/manifest.json` and one
`examples/catalog.json`.

## 5. Evidence-label census

Occurrences of each status label across the tree:

| Label | Count |
|---|---:|
| `hardware-confirmed` (**by a cited third party**, never by this session) | 39 |
| `reported-working` | 52 |
| `inferred` | 38 |
| `executed-success` (**research commands only** — fetches, parses, hashes) | 27 |
| `not-attempted` | 19 |
| `PENDING` (carried from the source's own annotation) | 13 |
| `not-tested` | 6 |
| `executed-failed` (preserved with diagnosis) | 3 |

**Claims hardware-tested by this session: 0.** Every `executed-success` refers to
a network fetch, a file parse, a hash or an archive operation — none touched an
Xteink device.

## 6. Claim-to-source spot checks

| Claim | Independent sources |
|---|---|
| X3/X4 SoC is ESP32-C3 | FreeInk profile · **flash-image chip-id 5** · English teardown caption · Chinese BOM — **4** |
| 16 MB flash | FreeInk · **exact image length** · both teardowns — **4** |
| X3 ~257 PPI | vendor *"250+ PPI"* · **arithmetic from 792×528 / 3.7″** — **2, one derivable** |
| X4 ~219 PPI | owner-measured *"220 ppi"* · **arithmetic from 800×480 / 4.26″** — **2** |
| QMI8658 @ 0x6B | `BoardConfig.h` · `XteinkDetect.cpp` · Chinese BOM — **3** |
| BQ27220 @ 0x55 | `BoardConfig.h` · `XteinkDetect.cpp` · Chinese BOM — **3** |
| X4 delisted | vendor API absence · **all 4 accessory SKUs sold out** · owner statement — **3** |
| X3 NFC tag is a writable passive tag | CrossInk maintainer statement · 3 firsthand owner reports · Chinese BOM — **5** |
| **X3 RTC part** | **3 sources, 3 different answers — recorded as unresolved, not resolved by preference** |

## 7. Conflicts recorded rather than resolved

| # | Conflict | Where |
|---|---|---|
| 1 | X3 RTC: `DS3231` (firmware) vs `DS1307` (teardown caption) vs `DS-series` (Chinese BOM) | `x3/gaps-and-conflicts.md` |
| 2 | X3 GPIO0 and GPIO20 each assigned **two** roles in the same SDK commit | `x3/gaps-and-conflicts.md` |
| 3 | X4 Pro touch `flipY`: the SDK header says "confirmed", its own doc says "pending" — **twice** | `x4-pro/gaps-and-conflicts.md` |
| 4 | X4 Pro firmware version: app descriptor `7.4.4` vs package metadata `V7.4.5` | `x4-pro/factory-firmware.md` |
| 5 | X4 dimensions: 74 g / 5.9 mm (2025) vs 80 g / ~7 mm (2026) | `x4/gaps-and-conflicts.md` |
| 6 | S4 price: ¥339 ≈ US$47 vs an AliExpress *"~$99"* | `s4/gaps-and-conflicts.md` |
| 7 | S4 owner reports *"running crosspoint"* — impossible on Android | `s4/gaps-and-conflicts.md` |
| 8 | X4 Classic reported with a frontlight by the community; firmware says none | `x4-classic/gaps-and-conflicts.md` |
| 9 | X3 community price $79 vs vendor API $69 | `x3/gaps-and-conflicts.md` |

## 8. Refuted hypotheses, preserved with their evidence

| Hypothesis | Refuted by |
|---|---|
| I²C `0x63` on the X4 Pro is a display PMIC with dead rails | A register dump showing the CW2017's BATINFO curve |
| The X4 Pro uses an ADC button ladder | A pull-up edge test; the ladder matcher is vestigial firmware |
| X4 Pro GPIO7 is a display enable | It reads `INPUT_PULLUP` — it is the Right button |
| An "X5" exists | 8 mentions, all speculation; one author self-corrected to "X4" |
| "X4 Mini" is a SKU | 6 uses, all colloquial; a video so titled names *"the XTEINK X4"* in its body |
| The X4 "runs Linux" | The dump is an Arduino/ESP-IDF 4.4.7 image on an MMU-less RISC-V core |
| A UC8179 always reports `CHIP_VER != 0` | A shipping X4 Pro returned `VER = 00 00 01 FF FF` |

## 9. Confirmed-correct existing documentation

- `software/applications/crossplay/README.md` correctly identified the X4 Pro as
  ESP32-S3 with 480×800 touch and a frontlight, and correctly identified the
  C3-image-onto-S3 OTA hazard. **Verified against the board profile; no
  correction needed.**
- **One prior statement is superseded:** the PaperMono record described the X4 Pro
  as a device on which *"You cannot put your own application on it."* That is
  incorrect — see `x4-pro/comparisons-and-recommendations.md`. The correction is
  recorded in the Xteink tree and, because `devices/m5stack/**` is owned by
  another session, is **proposed** in `scratch/xteink/index-fragments.md` rather
  than edited in place.

## 10. Shared files

**No shared or protected file was modified.** Confirmed by path-scoped
`git status` and by mtime: `README.md`, `devices/README.md`,
`components/README.md`, `vendors/README.md`, `artifact-manifest.md`,
`software/README.md`, `guides/markets/*` and `devices/m5stack/**` carry **no
modification from this session**. Proposed additions to them are staged as
ready-to-paste Markdown in `scratch/xteink/index-fragments.md`.

Five **existing** component records were **appended to** (Used By sections only,
no existing text altered), each after confirming `find <file> -mmin -30` was
empty: `solomon-systech/ssd1677`, `goodix/gt911`, `qst/qmi8658a`,
`espressif/esp32-s3r8`, `generic/bm8563`.

## 11. Known gaps in this verification

- **No example was built or statically validated.** No toolchain was installed.
- **Component datasheets were not retrieved** for the UC8253/UC8179/UC8279,
  CW2017, BQ27220 or ESP32-C3. Each record marks its datasheet
  `not-attempted` and gives the URL where known.
- **Bundled upstream Markdown was not link-checked** — none is vendored.
- Chinese marketplaces, Xiaohongshu, Bilibili and regulatory databases were
  **declared exclusions**, not exhausted searches.
- This is a **self-audit**. No independent verifier reviewed the work.

## 12. Verdict

The tree is internally consistent, fully cross-linked, artifact-validated and
honest about its evidence class. Its principal weakness is **source
concentration**: for the X4 Pro and X4 Classic, essentially every technical claim
traces to one repository at one commit
(`Free-Ink/freeink-sdk` @ `24003795381a6c23630a26472ae3b06550333e71`), with no
teardown, schematic or regulatory filing to corroborate it. That is stated in each
of those records rather than papered over.

---

# ⚠ Round-two correction, 2026-09-11 — the regulatory findings are refuted

**Nothing above this line has been edited.** A verification report that quietly rewrites itself
is worthless; the original text stands and this section supersedes the parts named below.

Round two of this sweep ran on **2026-09-11**. Full report:
[`VERIFICATION-xteink-round2.md`](VERIFICATION-xteink-round2.md). Certification detail, with
controls: `devices/xteink/<record>/certification-and-compliance.md`.

## C1 — "regulatory databases were declared exclusions" (§11)

> *"Chinese marketplaces, Xiaohongshu, Bilibili and regulatory databases were **declared
> exclusions**, not exhausted searches."*

Accurately stated at the time, and the exclusion has now been lifted. The US FCC database **was**
searched on 2026-09-11, with positive and negative controls. Result below.

## C2 — "no … regulatory filing to corroborate it" (§12)

> *"…with no teardown, schematic or regulatory filing to corroborate it."*

**Refuted on two of three counts.**

**Xteink is an FCC grantee.** Applicant **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**,
grantee code **`2BTR9`**, registered 2025-12-21, holding **five granted Original Equipment
authorisations** — one for every ESP32-based device in this tree, plus one for a device this
repository did not know existed:

| FCC ID | Granted | Device | Record |
|---|---|---|---|
| `2BTR9-X4L` | **2026-08-13** | XTEINK X4 Light | [`x4-light`](devices/xteink/x4-light/README.md) — **new, found by grantee enumeration** |
| `2BTR9-X4C` | 2026-07-20 | XTEINK X4 Classic | [`x4-classic`](devices/xteink/x4-classic/README.md) |
| `2BTR9-X4PRO` | 2026-06-16 | XTEINK X4 Pro | [`x4-pro`](devices/xteink/x4-pro/README.md) |
| `2BTR9-XTEINKX4` | 2026-01-05 | XTEINK X4 | [`x4`](devices/xteink/x4/README.md) |
| `2BTR9-XTEINKX3` | 2025-12-26 | XTEINK X3 | [`x3`](devices/xteink/x3/README.md) |

- **Regulatory filing: exists.** Five of them.
- **Teardown: exists.** The `2BTR9-XTEINKX4` filing's **Internal Photos** were never withheld.
  They are the **first public teardown of the Xteink X4** and are now held at
  [`devices/xteink/x4/artifacts/certification/`](devices/xteink/x4/artifacts/certification/README.md).
  The X3's are public too. The X4 Pro's unlock **2026-12-12**.
- **Schematic: still absent, permanently.** All five filings hold Schematics, Block Diagram and
  Operational Description under **long-term** confidentiality. **The FCC is not a route to an
  Xteink schematic**, and never will be.

So §12's source-concentration verdict is **half repaired**: the X4 Pro still traces
substantially to one commit, but it now has an independent regulatory record and a dated
teardown release.

## C3 — the underlying error, stated plainly

The 2026-09-04 pass confused **"no mark visible in a product photograph"** with **"no grant
exists"**. Only the first was ever tested.

- ✅ **Survives:** no FCC ID was legible on the exteriors photographed.
- ❌ **Refuted:** any reading that these devices are uncertified or unauthorised for the US.

47 CFR §2.935 permits an **e-label** in software instead of a printed mark — ordinary for a
device with a screen. **Likely, and not verified.**

**Why it was missed, and the transferable lesson:** the 2026-09-04 pass searched by *product
name*. Xteink's grants are filed under model codes (`XTEINKX3`, `X4PRO`, `X4C`) that a product
search does not reach. **Enumerating the vendor's FCC grantee code returns its complete
certified product list, including devices it has never announced** — which is how the X4 Light
was found. That technique generalises to every vendor in this repository and is written up in
[`guides/research/finding-certification-records.md`](guides/research/finding-certification-records.md).

## C4 — what is *not* corrected

The controls that make these findings meaningful, and the limits that remain:

| ID probed | HTTP | Role |
|---|---|---|
| `2BTR9-XTEINKX4` · `2AC7Z-ESPS3WROOM1` · `2AN3WM5CARDPUTER` | **200** | positive |
| `2AN3WM5CARDPUTERZERO` · `2ASYE-T-DISPLAY-K230` · `2ZZZZNOSUCHGRANTEE` | **404** | negative, invented |

- **Still zero hardware claims.** §5's "Claims hardware-tested by this session: 0" is unchanged
  and remains true of round two.
- **CE, UKCA, SRRC, CCC, MIC and ISED are still not established.** CE has no database to search;
  the Chinese registers failed to connect; the Japanese one was reachable but not queried.
  **Those are not negative results.**
- **`fccid.io` is a mirror, not the FCC.** `apps.fcc.gov` returned 403 to all five user agents
  tried, so no confirmation against the primary host was obtained.
- **No FCC grant exists for the [S4](devices/xteink/s4/README.md) or the
  [Nano](devices/xteink/nano/README.md)** — an absence against a *complete* grantee enumeration
  with passing controls, which is the strongest form this evidence takes.

Every correction above is listed in
[`scratch/index-merge/corrections-requiring-review.md`](scratch/index-merge/corrections-requiring-review.md).
