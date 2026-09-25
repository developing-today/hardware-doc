# ARCHIVED: NFC research evidence for this part

> Moved out of `scratch/`, **not deleted**. Archived **2026-09-20**; every operation was `mv`.

Two corpora gathered on **2026-09-11** while researching NFC on the M5Stack PaperMono and the
M5Unit-NFC. Almost nothing in them is about either product — they are about **this chip**: its
register definitions, ST's own RFAL driver, the community forks that patched it, and the issue
threads where its behaviour was worked out. A chip's driver corpus is a component artifact even
when a device task fetched it.

## Identity

| Field | Value |
|---|---|
| Archived to | `archive/components/stmicroelectronics/st25r3916/artifacts/` |
| Was at | `scratch/_rescued-from-tmp-2026-09-20/{nfc-and-epaper-research/nfcres,github-issues}/` |
| `nfc-source-survey-2026-09-11/` | **65 files, 128,655,077 B**, digest `ad52daa9d11b4bfc1aa3a93bf75a9753425395d6c450a365769d0473f0331582` |
| `nfc-issue-survey-2026-09-11/` | **41 files, 2,060,706 B**, digest `7a3154c13c946c5a5b9088144c886a7ffd3203fba2f7eacb4671ce47fe50c6b0` |
| Gathered | 2026-09-11 |
| Rescued from `/tmp` | 2026-09-20 — ⚠ **provenance unverified**, see below |

Full contents table: [`archive/components/stmicroelectronics/st25r3916/artifacts/README.md`](../../../archive/components/stmicroelectronics/st25r3916/artifacts/README.md).

## What is in it, in one paragraph

**The implementations worth reading side by side:** ST's reference RFAL driver
(`st_rfal_rfst25r3916.c`, 235 KB; `st_com.{c,h}`, 113 KB; `st_rfal_duino.cpp`, 183 KB), M5's unit
driver and its register-definition header (`src_unit_unit_ST25R3916.{hpp,cpp}`,
`src_unit_ST25R3916_definition.hpp`, 114 KB together), an NFC-F/FeliCa emulation layer, and
**five takes on NFC-A card emulation** — one original plus four community forks. **The census:**
14 GitHub code-search responses (~120 MB) covering every public project naming this part, plus
full repository metadata, five issues, a PR, and Japanese-language write-ups from Qiita.

## ⚠ What has *not* been done

**The vendor driver has never been audited against the datasheet.** That audit — decoding every
constant and register write against the register map, checking power-up ordering and delays,
finding the fault and status registers the driver never reads — is the highest-yield activity
available for a part like this, and this corpus was gathered to make it possible. As of
2026-09-20 it has not been started. The presence of `st_rfal_rfst25r3916.c` beside
`src_unit_unit_ST25R3916.cpp` is an invitation, not a finding.

Three further cautions:

- **This is a 2026-09-11 snapshot of a ranked, non-deterministic search.** A project absent from
  those JSON files was not necessarily absent from GitHub.
- **The four "forks" may not be independent.** `fork_marekbujko.cpp`, `fork_roro3828.cpp` and
  `fork_Sped0n.cpp` are all **17,132 bytes** — the same size as the two upstream files beside
  them. Diff before treating any two as separate implementations.
- **`group3/` contains search-engine and chatbot output** (`m5n6o7-bing.*`, `m5n6o7-chatgpt.*`),
  not primary sources. The filenames say so; treat them accordingly.

## Provenance caveat

These files were recovered from `/tmp` by a sweep that stated plainly it did not produce them and
could not verify authorship or completeness, and the subject README written alongside them said
the grouping was unverified. **Treat everything as unattributed 2026-09-11 working material.**
Full rescue record:
[`archive/guides/research/artifacts/rescued-from-tmp-2026-09-20/`](../../../archive/guides/research/artifacts/rescued-from-tmp-2026-09-20/README.md).

## How to get it back

| Route | Reliability |
|---|---|
| Local archive — `mv "archive/components/stmicroelectronics/st25r3916/artifacts/<dir>" .` | exact bytes |
| ST's RFAL and X-CUBE-NFC6 — <https://www.st.com/en/embedded-software/x-cube-nfc6.html> | the driver sources, current version |
| `stm32duino/ST25R3916` — <https://github.com/stm32duino/ST25R3916> | the Arduino wrapper |
| `m5stack/M5Unit-NFC` and `m5stack/M5UnitUnified` | the unit driver and its issue history |
| Re-running the GitHub code searches | ⚠ **will not reproduce this set** — results are ranked and drift |

The searches are the part that does not come back, which is why 120 MB of JSON was kept.
