# ARCHIVED: `lr2021-datasheet-v1.1-mouser-mirror.pdf`

> This file was **moved out of the repository**, not deleted.
> Archived **2026-09-07**.

**Reason:** Superseded datasheet revision (Rev 1.1, DS.LR2021, 2025-10-14, 236 pp) retained per the keep-both-revisions rule because it differs from Rev 2.1 in substance, not only formatting. 5.16 MB alongside the 5.81 MB Rev 2.1 copy is more weight than one chip warrants in-repo; Rev 2.1 is the current document and stays.

## Identity

| Field | Value |
|---|---|
| Original repo path | `components/semtech/lr2021/artifacts/lr2021-datasheet-v1.1-mouser-mirror.pdf` |
| Archived to | `archive/components/semtech/lr2021/artifacts/lr2021-datasheet-v1.1-mouser-mirror.pdf` (the path after `archive/` is the path it had here) |
| Type | file |
| Size | 5,158,757 B (4.92 MiB) |
| SHA-256 | `926b88cbfb6434e3954569b3f0d96e47c3ca2952245ebc1d01f65ab52d382ff7` |
| Last modified (mtime) | 2026-09-07 10:31:43Z |
| Author / committer | Semtech Corporation (PDF /Author 'julie') |
| Commit date | 2025-10-13 (PDF CreationDate D:20251013170105Z) |
| License | unknown - (c) Semtech Corporation, marked 'Proprietary & Confidential' on every page |
| Document identity | **`DS.LR2021`, Final Datasheet Rev. 1.1, dated `10/14/25`, 236 pages.** PDF `/Title` `LR2021_V1_1_datasheet.pdf`, `/Creator` FrameMaker 17.0.4, `/Producer` Adobe PDF Library 17.0 |
| Type validated | Yes — magic bytes `%PDF-1.6`, 236 pages parsed with `pypdf` |

## How to get it back

**Three independent routes, best first.** None of them is Semtech's own site: Semtech's
canonical link for this document is a Salesforce content-distribution shell that no
non-browser client has been able to get bytes out of (see
[`vendors/semtech/README.md` §4](../../../../vendors/semtech/README.md)).

| # | Source | URL | Verified |
|---|---|---|---|
| 1 | **Mouser Electronics mirror** — where this copy came from | `https://www.mouser.com/pdfDocs/61979758LR2021_V1_1_datasheet.pdf` | 2026-09-04, HTTP 200, `application/pdf`, 5 158 757 B. ⚠ **Requires a non-default User-Agent** — see below |
| 2 | **Wayback Machine** capture of the Mouser URL | `https://web.archive.org/web/2026/https://www.mouser.com/pdfDocs/61979758LR2021_V1_1_datasheet.pdf` | submitted to `web.archive.org/save/` 2026-09-04 because Mouser is bot-hostile and a single-host recovery path is one outage from useless |
| 3 | **Semtech product page** (canonical, but gated) | `https://www.semtech.com/products/wireless-rf/lora-plus/lr2021` → *Documents* → *Datasheet*. ⚠ Now serves **v2.2**, not v1.1 — Semtech does not publish superseded revisions. **This route cannot return this file.** Recorded so nobody wastes an hour on it | 2026-09-04 |

⚠ **Mouser blocks the ordinary browser User-Agent for this path and serves the WhatsApp
link-preview agent.** This is the reverse of the usual pattern and it is not a typo:

```bash
# 403 + a 13 895-byte "Access Denied / captcha" HTML page, saved with a .pdf name if you are careless
curl -sSL -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
     -o out.pdf 'https://www.mouser.com/pdfDocs/61979758LR2021_V1_1_datasheet.pdf'

# 200 application/pdf, 5 158 757 B  <- this one
curl -sSL -A 'WhatsApp/2.23.20.0' \
     -o out.pdf 'https://www.mouser.com/pdfDocs/61979758LR2021_V1_1_datasheet.pdf'
sha256sum out.pdf   # 926b88cbfb6434e3954569b3f0d96e47c3ca2952245ebc1d01f65ab52d382ff7
```

The `61979758` prefix is Mouser's own opaque document id. It is **not derivable** from the
part number — it was recovered from a search-engine index. Guessed filenames
(`LR2021_datasheet.pdf`, `DS_LR2021_V1.0.pdf`) return HTTP **403** with a 1 140-byte body,
`executed-failed` 2026-09-04.

Restore from the local archive if you have it:

```bash
mv "$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")/../repo-archive/hardware-doc/components/semtech/lr2021/artifacts/lr2021-datasheet-v1.1-mouser-mirror.pdf" \
   components/semtech/lr2021/artifacts/lr2021-datasheet-v1.1-mouser-mirror.pdf
```

## Why this revision was kept rather than discarded

Rev 1.1 and Rev 2.1 are **not the same document with a new date**, and the differences are
the kind that silently invalidate a design:

- Rev 1.1 is titled **`LR2021 Datasheet`** and covers **one part**. Rev 2.1 is
  **`LR2021/LR2022/LR2012 Datasheet`** (`DS.LR20xx`) and covers three, with per-part
  feature exclusions. A "the datasheet says…" claim sourced from Rev 1.1 has no
  LR2022/LR2012 column to be wrong about; the same claim in Rev 2.1 might.
- **A published sensitivity figure moved.** Rev 1.1 front page: FLRC sub-GHz
  **−101.5 dBm @ 1.95 Mbps**. Rev 2.1 front page: **−100.5 dBm @ 1.95 Mbps**. 1 dB worse,
  no erratum, no callout in the revision history beyond a general "Added 0.5dB to all
  sensitivity numbers in Table 3-13 and Table 3-18".
- Rev 2.1's own revision history lists further substantive edits — FLRC bandwidth values in
  three tables, a new `SetLoraTxSync` command, a new §11.1.3 "(G)FSK Limitations", a new
  §22.3 "Firmware Patch RAM (PRAM)", changed `IDDSL1` sleep current, changed 434/490 MHz
  transmit numbers, and changed Z-Wave typical sensitivities.

So: **Rev 2.1 is authoritative; Rev 1.1 is the record of what Semtech said first**, and is
the only way to tell whether a 2025-vintage board or driver was designed against numbers
that no longer hold.

## Documented in

The full provenance table, both revisions side by side, is in the component record:
[`components/semtech/lr2021/README.md` §14](../README.md#14-local-artifacts).
