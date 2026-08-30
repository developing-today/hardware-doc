# Non-English wiki translations — archived

The Seeed wiki publishes this product's documentation in five languages. **Only `en/` is
retained here**; the other four were moved to the archive on 2026-08-26.

| Language | Files | Bytes | Tree SHA-256 | Location |
|---|---:|---:|---|---|
| `en` | 46 | 1 150 845 | *(live in repo — changes as the corpus is edited)* | **in this repository** |
| `zh-CN` | 46 | 1 104 995 | `1fc9577fdfc1e5f99a0a15b097440f364637548f956f81a1ae94f31e6d1e88b7` | archived |
| `ja` | 46 | 1 297 817 | `3c1f6562b7e246269a0729b94833b1bab914c365f0e2bc16c1f4b7265f8c1259` | archived |
| `pt-BR` | 46 | 1 198 229 | `210420602b5462c23830ab745493c21b28dccff3964e691db90993a0ecf5b0f7` | archived |
| `es` | 46 | 1 205 702 | `9cff8fcdabb661ee49fb005c0955acee7b3099a28a9cc16b28157e506418bed1` | archived |

The tree hash covers file *contents and paths*, so it detects a missing or altered page. Reproduce it with:

```bash
find <lang> -type f -exec sha256sum {} \; | sort -k2 | sha256sum
```

**Archive path** (repo-relative, so it maps 1:1):

```
archive/hardware-doc/devices/seeed-studio/xiao-esp32s3-sense/artifacts/wiki-snapshot/sites/<lang>/
```

## Why only English was kept — the translations add nothing

This was **checked, not assumed**. Comparing all 46 paired `zh-CN`/`en` pages:

| Check | Result |
|---|---|
| Page count per language | **27 each** for `en`, `zh-CN`, `ja`, `pt-BR` — identical coverage |
| Section headings, Getting Started | **37 in both** |
| Numeric specs (mA / µA / MHz / MB / mAh / V) | **identical sets** — no value unique to either language |
| Code blocks per page | **identical counts** across all 46 pairs |
| GPIO numbers referenced | **no delta** on any pair |

The translations are faithful and derivative. They are ~25 % smaller in bytes purely
because Chinese and Japanese encode denser in UTF-8, not because content was cut.

**There is no need to read the Chinese, Japanese, Portuguese or Spanish wiki for this
product**, and no evidence of a non-English-first documentation track. Had a translation
carried material the English lacked, that would have been a finding and it would have
stayed in the repository.

## Reacquisition

All five languages come from the same source as the English corpus — the wiki is an
open-source Docusaurus site, **not** scraped from the rendered pages:

- **Repository:** `Seeed-Studio/wiki-documents`
- **Branch:** `docusaurus-version` (⚠ `main` 404s; `master` is a different, near-empty tree)
- **Path template:** `sites/<lang>/docs/Sensor/SeeedStudio_XIAO/SeeedStudio_XIAO_ESP32S3*/…`

```bash
# enumerate everything for this product, any language
curl -fsSL "https://api.github.com/repos/Seeed-Studio/wiki-documents/git/trees/docusaurus-version?recursive=1" \
| python3 -c "import json,sys;[print(t['path']) for t in json.load(sys.stdin)['tree'] if 'XIAO_ESP32S3' in t['path']]"

# fetch one file
curl -fsSL "https://raw.githubusercontent.com/Seeed-Studio/wiki-documents/docusaurus-version/<path>"
```

Retrieved **2026-08-24**. The tree API returned 16 372 entries; 300 matched this product.

> ⚠ These are `HEAD`-of-branch fetches, so they are **not revision-pinned**. Re-fetching
> will yield whatever the wiki says at that later date, which may differ. See
> [`../../sources.md`](../../../sources.md) row S8.

## Related

- [`../../gaps-and-conflicts.md`](../../../gaps-and-conflicts.md) — vendor contradictions found in the English corpus
- [`../../examples/search-log.md`](../../../examples/search-log.md) — the language comparison, in full
- [Seeed vendor guide](../../../../../../vendors/seeed-studio/README.md) — how to enumerate this wiki
