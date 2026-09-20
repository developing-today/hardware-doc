# Example search log

Queries run, depth reached, and what was excluded. Snapshot **2026-08-24**.

## Services and queries

| Service | Query | Sort / depth | Results | Useful |
|---|---|---|---|---|
| GitHub code search API | `xiao_esp32s3 repo:Seeed-Studio/wiki-documents` | — | HTTP 401 (auth required) | ✗ — replaced by the tree API |
| GitHub git-trees API | `Seeed-Studio/wiki-documents` tree `docusaurus-version?recursive=1` | full tree, 16,372 entries | **300 paths** matching `xiao_esp32s3` | ✓ **230 Markdown files retrieved** |
| GitHub git-trees API | same, branch `main` | — | **HTTP 404** | negative control |
| GitHub git-trees API | same, branch `master` | 1,366 entries | **0** matches | negative control |
| GitHub repo search | `xiao+esp32s3+sense`, stars desc | 30 of **142** | 30 inspected | ✓ 15 catalogued |
| GitHub repo search | `xiao+esp32s3+camera`, stars desc | 30 of **70** | 30 inspected | ✓ overlap + 5 new |
| GitHub repo search | `xiao+esp32s3`, stars desc | 30 of **413** | 30 inspected | ✓ 4 new |
| GitHub repo search | `seeed+xiao+esp32s3+sense+microphone`, stars desc | 4 of 4 | all | ✓ 0 new |
| GitHub releases API | `Sukecz/esp32-birdnet-mic/releases` | 5 most recent | v1.10–v1.22 | ✓ second recovery path for archived firmware |
| Wiki Markdown corpus | URL extraction across all 230 files | full | **68 artifact URLs**, **75 GitHub links** | ✓ primary artifact source |
| Seeed reference-design PDF | `/Annots` link extraction, 129 pages | full | **117 project entries, 116 with URLs** | ✓ see [`../projects-and-community.md`](../projects-and-community.md) |
| Seeed product page | `XIAO-ESP32S3-Sense-p-5639.html` | 1 page | 1.0 MB HTML | ✓ identity only |
| `wiki.seeedstudio.com` rendered page | `xiao_esp32s3_getting_started` | 1 page | 150 KB HTML, **1 link** | ✗ JS shell — negative control |

## Depth and stopping criterion

Repository search was taken to **30 results per query, sorted by stars**, across four query families. The fourth query returned no new repositories, and the third returned only four — two consecutive passes yielding mostly duplicates, which is the stopping criterion used.

**Total candidate pool:** 18 repositories carried into [`catalog.json`](catalog.json), 9 vendored.

## Known exclusions

- **Not searched:** GitLab, Codeberg, Bitbucket, Gitee. Gitee in particular is likely to hold Chinese-language XIAO projects not on GitHub, and is a real gap given Seeed is a Shenzhen company.
- **Not searched exhaustively:** Hackster.io, Hackaday.io, Instructables and YouTube were reached only *via* Seeed's showcase catalogue, not searched directly. The catalogue is a vendor-curated subset.
- **Forums:** the Seeed forum was not systematically mined. `github.com/Seeed-Studio/wiki-documents/discussions/69` appeared 210 times across the wiki corpus as the standard feedback link but was not read.
- **Languages:** the wiki translations were **compared and found equivalent** (see below). Chinese *community* platforms (Bilibili, Zhihu) remain unsearched.
- **Regulatory:** FCC filings **were** subsequently mined — see [`regulatory-and-certification.md`](../regulatory-and-certification.md). They did *not* resolve the microphone (the daughterboard schematic did). CE/EU technical files were not pursued.

This is a **reproducible broad-coverage snapshot**, not proof that no other resource exists.


## Non-English sources — checked, and they add nothing

A common assumption is that a Shenzhen vendor's Chinese documentation contains detail the English lacks. **Checked directly on 2026-08-24 — for this product it does not.**

The wiki snapshot holds **46 paired zh-CN/en pages**. Comparing them:

| Check | Result |
|---|---|
| Page count per language | **27 each** for `en`, `zh-CN`, `ja`, `pt-BR` — identical coverage |
| Section headers, Getting Started | **37 in both** |
| Numeric specs (mA/µA/MHz/MB/mAh/V) | **Identical sets** — zero values unique to either language |
| Code blocks per page | **Identical counts** on all 46 pairs |
| GPIO numbers mentioned | **No delta** on any pair |

The zh-CN pages are consistently ~25 % smaller in bytes, which is Chinese being denser, not content being cut.

**Conclusion: the translations are faithful and derivative.** There is no need to read the Chinese, Japanese or Portuguese wiki for this product, and no evidence of a Chinese-first documentation track.

Other Chinese-language channels attempted:

| Source | Result |
|---|---|
| **Gitee** (`/api/v5/search/repositories`) | HTTP 200 but **zero results** for "XIAO ESP32S3" |
| **Gitee** (`/explore?search=`) | **HTTP 405** — method not allowed to scripted clients |
| Bilibili, Zhihu | **Not attempted** — no reliable unauthenticated API |

So the Chinese-language gap is now **partially closed**: the official documentation is confirmed equivalent, but Chinese *community* platforms (Bilibili video, Zhihu posts) remain unsearched and may hold project material.

## Related
- [`catalog.json`](catalog.json) · [`best.md`](best.md) · [`../acquisition/README.md`](../acquisition/README.md)
