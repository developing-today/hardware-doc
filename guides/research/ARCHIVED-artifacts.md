# ARCHIVED: working evidence for research technique

> Moved out of `scratch/`, **not deleted**. Archived **2026-09-20**; every operation was `mv`.

Four sets of material that describe **how research was conducted and how it failed** — not any
board, chip or vendor. They back the two guides in this directory and the site-by-site findings in
[`ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md).

All are at `archive/guides/research/artifacts/`; directory index:
[`README.md`](../../archive/guides/research/artifacts/README.md).

| Set | Files | Bytes | Was at |
|---|---:|---:|---|
| `certification-and-market-2026-09-11/` | 48 | 1,316,850 | `scratch/market-and-certification/` |
| `tmp-sweeps-2026-08-26/` | 55 | 27,672,738 | `scratch/{_tmp-sweep-2026-08-26,workspace,misc}/` |
| `rescued-from-tmp-2026-09-20/` | 1 | 3,792 | `scratch/_rescued-from-tmp-2026-09-20/README.md` |
| `retrieval-specimens-2026-09-11/` | 2 | 1,052 | `scratch/_rescued-from-tmp-2026-09-20/misc/` |

---

## `certification-and-market-2026-09-11/` — ⚠ the exhibits are **not** there

This is the most-cited scratch subject in the repository: roughly **167 references** across ~30
device and component records name `scratch/market-and-certification/fcc/<FCC-ID>/<exhibit>.pdf` as
an artifact's local path.

**Those paths are historical.** A consolidation pass on 2026-09-20 removed all 163 exhibit PDFs
(194.2 MiB) and 71 extracted internal-photo PNGs (72.9 MiB), after proving by SHA-256 on every
file that each already existed under `devices/` or `components/`:

```
163 exhibit PDFs across 26 FCC-ID directories
  → in the repository        57
  → in the archive          106
  → in NEITHER                0        (0 bytes unrepresented)
```

The photographs were additionally regenerated — all 71, `pdfimages -png <ID>-internal-photos.pdf
int`, poppler 26.06.0 — and compared: **71 identical, 0 differing**. The five source PDFs are in
the **repository**, not merely archived, so they reproduce from a clean checkout with no archive
access.

**To resolve one of those citations:** look under the owning record's `artifacts/certification/`,
where either the PDF or its `*.ARCHIVED.md` placeholder sits.

What survives in the archive is the harvest *record*, and it is worth having:

| Path | Why |
|---|---|
| `fcc/<ID>/_filing.html` × 27 | Grant text, exhibit index and application metadata — including exhibits `harvest.py` never fetched |
| `fcc/filing-metadata.json` | ⚠ Holds the **correct** test-firm value for `2AN3WM5PAPERMONO` where a downstream record has it wrong |
| `fcc/harvest.py`, `harvest-*.json` | ⚠ `MAX_TEST_REPORTS = 1` — for PaperMono this picked an antenna datasheet and **skipped the four reports carrying the actual radio measurements**, including the LoRa duty cycle |
| `fcc/grantee-*.html`, `srch-*.html` | The grantee-code enumeration that surfaced the **X4 Light**, a device Xteink has never announced |
| `logs/ua-matrix.txt`, `logs/fcc-controls.txt` | See below |
| `xteink-certification-and-pricing.md` | Authored findings held outside `devices/xteink/` because a sibling agent owned that tree on 2026-09-11 |

### The single most reusable thing in it: the inverted Cloudflare block

[`finding-certification-records.md`](finding-certification-records.md) carries this, and it is
worth repeating because it inverts the standard fallback ladder:

```
UA                       fccid.io/2AN3W
Chrome/131 (browser UA)  403   ← Cloudflare "Complete the security check"
WhatsApp/2.23.20.0       200
ChatGPT-User/1.0         200
ClaudeBot/1.0            200
curl/8.5.0               200
```

**The honest `curl` UA works and the disguised browser UA does not.** `AGENTS.md`'s ladder assumes
the opposite direction, which is why the rule there is *"rotate UAs"*, not *"use a browser UA"*.

The same logs record that the **official** FCC endpoints are unusable from this host — 403 to
every UA at `apps.fcc.gov/oetcf/eas/…`, `www.fcc.gov/oet/ea/fccid` and the attachment endpoint;
404 at `opendata.fcc.gov/resource/kfc9-pnvf.json`; and `fcc.report` 403 to everything.

### One error corrected by this pass, worth not re-making

Grepping the **text layer** of FCC "ID Label" exhibits for `CE` / `IC:` / `CMIIT` reported
**26/26 absent**. ❌ **That is false. The labels are photographs.** The text layer contains only
the words "Label" and the FCC ID. Visual inspection of a single label found CE, FCC and WEEE marks
immediately.

---

## `tmp-sweeps-2026-08-26/` — three agents, one `/tmp`, three directories

55 files, digest `07f2419374dd20a25ce6d56647d1264caffa9e36aec0482e91be7cbbbd5c3a43`. Has its own
[README](../../archive/guides/research/artifacts/tmp-sweeps-2026-08-26/README.md), plus the four
READMEs written by the agents that made it.

It documents three things: the **triplication episode** that rule 1 of the scratch conventions
exists to prevent; the **extension/content mismatch specimens** (`ms.pdf`, `sib.pdf`, `p.bin` —
HTML LCSC pages served 200 under binary extensions; `ocr_*.png` holding JPEG data in two of three
copies); and **blocked or empty fetch bodies** from Gitee and LCSC.

⚠ **Keep the misleading names.** A specimen whose filename has been corrected no longer
demonstrates anything. `bq25306.txt` is a subtler case: two READMEs call it *"empty of readable
text — extraction likely failed"* and it is in fact **139 KB of correct datasheet text**. The
wrong claim is itself the specimen, and it is preserved in both places with the correction
recorded.

### 116 MB of those sweeps was never hardware material

`hermes_agent` 0.19.0 (a Python CLI, 974 files), two byte-identical copies of
`@earendil-works/pi-coding-agent` v0.84.3 (an npm package, 1,044 files each), a nixpkgs maintainer
diff, and a NixOS build log — swept indiscriminately out of `/tmp` along with the hardware files.
It is **not** in the archive and **not** deleted: it is in `repo-archive/scratch-foreign/`, grouped
by where it was found, with a README stating that it is unidentified third-party tooling of
unknown provenance. Forcing it into `devices/` or `components/` would have been worse than either
alternative.

---

## `rescued-from-tmp-2026-09-20/` and `retrieval-specimens-2026-09-11/`

The first holds the provenance note for the 2026-09-20 `/tmp` rescue — the only statement of
origin for 1,936 files — plus the table of where its nine groups went. The second holds two small
specimens: a **Zhihu bot-block body served with a 200 and containing no article**, and the
HTML→text extractor that pass used (whose two site-specific truncation markers identify it as
written for MobileRead threads).

---

## How to get it all back

```bash
mv "archive/guides/research/artifacts/<set>" "scratch/<original name>"
```

Individually:

| Piece | Route | Reliability |
|---|---|---|
| FCC exhibits | `https://fccid.io/<GRANTEE>/<PRODUCT>/<doc-id>.pdf` — ⚠ **use a non-browser UA** | good; they are US Government public records, redistribution allowed |
| Filing pages | `https://fccid.io/<FCC-ID>` | good |
| Shopify catalogues | see [`guides/markets/ARCHIVED-artifacts.md`](../markets/ARCHIVED-artifacts.md) | ⚠ returns *today's* catalogue |
| The failure specimens | ⚠ **not reacquirable** — they are what those hosts returned on those dates | — |
