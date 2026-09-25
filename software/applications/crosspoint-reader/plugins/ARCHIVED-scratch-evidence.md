# ARCHIVED: plugin evidence moved out of `scratch/`

> Moved, **not deleted**. Archived **2026-09-20**; every operation was `mv`.

Two sets of working material behind the records in this directory. Both were in `scratch/`; both
are now in the archive at this directory's own repo-relative path.

| Archived to | Files | Bytes | Tree digest | Was at |
|---|---:|---:|---|---|
| `archive/software/applications/crosspoint-reader/plugins/papermono-plugins-handoff-2026-09-11/` | 54 | 499,610 | `11a62e468f936302a9bea43e2940c6f9f9bd1b7e790d811fef13cea467e5cb41` | `scratch/papermono-plugins-handoff-2026-09-11/` |
| `archive/software/applications/crosspoint-reader/plugins/rescued-from-tmp-2026-09-20/` | 26 | 6,906,409 | — | `scratch/_rescued-from-tmp-2026-09-20/{crosspoint-plugins,misc}/` |

Directory-level index:
[`archive/software/applications/crosspoint-reader/plugins/README.md`](../../../../archive/software/applications/crosspoint-reader/plugins/README.md).
This is separate from `source-snapshots/`, which an earlier pass archived and which has its own
placeholder at [`source-snapshots.ARCHIVED.md`](source-snapshots.ARCHIVED.md).

## ⚠ The handoff package is merged — do not re-merge from it

`papermono-plugins-handoff-2026-09-11/` is eleven numbered analysis documents, a `HANDOFF.md`, a
`MERGED.md` and a `raw/` tree of plugin sources. Written 2026-09-11, closed 2026-09-13. Its
`MERGED.md` says:

> *"Several claims in these documents were checked against the raw source captured alongside them
> and did not hold."*

The corrected output is the records in **this** directory — `plugin-architecture.md`,
`firmware-plugin-internals.md`, `plugin-source-survey.md`, `sd-plugins-and-protected-content.md`,
`papermono-plugin-branch-notes.md`. **Re-merging from the numbered documents will re-import the
errors.** 29 of its 53 files are byte-identical to material already promoted; the analysis
documents were rewritten rather than copied, which is why the originals still matter — they are
the audit trail for what changed.

## What the rescued set adds

Primary vendor documents and plugin sources found loose in `/tmp` on 2026-09-20:

- **ByteBooks' own published documents** — the EULA, account-creation help, the error-code list
  and the transition FAQ.
- **The Libby, protected-content and plugin-store implementations** with their manifests —
  the sources behind [`libby-path.md`](libby-path.md) and
  [`sd-plugins-and-protected-content.md`](sd-plugins-and-protected-content.md).
- **`bytebooks-platform-transition/`** — Adobe's own FAQ *"Adobe eBook platform transition to
  Wipro Connected Services"* plus three MobileRead threads and the search that found them. This is
  the authoritative account of **why ByteBooks exists**, and it is **not mined into any record**.
  [`dtsbytebooks-review.md`](dtsbytebooks-review.md) exists but was not written from these
  captures.

Two traps in that set:

| File | Why it misleads |
|---|---|
| `adobe-eol.html` (446 B) | ⚠ An Akamai **"Access Denied"** body, not content. The successful fetch is the 139 KB `adobe-eol-ok.html` beside it. The filename does not warn you; the size does |
| `adobe-eol-ok.html` / `ad_try.html` | **Identical size (139,570 B)** — very likely two fetches of one page. Diff before treating them as independent evidence |
| `patch.py` | ⚠ **Not a plugin.** An M5Unit-NFC patch (PaperMono NFC-A emulation + field-detection fixes). The rest of that work is under [`components/stmicroelectronics/st25r3916/`](../../../../components/stmicroelectronics/st25r3916/README.md) |

⚠ Provenance for the rescued set is **unverified** — the sweep that recovered it did not produce
it. Full record:
[`archive/guides/research/artifacts/rescued-from-tmp-2026-09-20/`](../../../../archive/guides/research/artifacts/rescued-from-tmp-2026-09-20/README.md).

## How to get it back

| Route | Reliability |
|---|---|
| Local archive — `mv "archive/software/applications/crosspoint-reader/plugins/<dir>" .` | exact bytes |
| Plugin sources | the upstream plugin repositories enumerated in [`plugin-source-survey.md`](plugin-source-survey.md); `repos.txt` and `tree.json` in the rescued set list them with the GitHub API response they came from |
| ByteBooks documents | <https://bytebooks.com/> — publisher-hosted PDFs; ⚠ a vendor that has just taken over a platform is likely to revise them |
| Adobe transition FAQ | <https://helpx.adobe.com/enterprise/kb/eol-faq-adobe-digital-editions.html> — ⚠ returned **Access Denied** to the first attempt; the capture succeeded on a retry |
| MobileRead threads | <https://www.mobileread.com/forums/> — thread ids 373594, 373596, 374311 |
| Wayback | `https://web.archive.org/web/2/<any of the above>` |
