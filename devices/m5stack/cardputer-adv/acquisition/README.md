# Cardputer ADV — acquisition

> Snapshot **2026-09-04**. Machine-readable: [`manifest.json`](manifest.json).
> Every artifact here is an **unauthenticated GET** or a **git clone at a pinned commit**.
> No login, no API key, no rate limit encountered — so no bespoke downloader was written; the
> commands below *are* the downloader, in execution order.

## Prerequisites

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
cd "$(git rev-parse --show-toplevel)"/devices/m5stack/cardputer-adv
mkdir -p artifacts/{schematic,mechanical,docs,source-snapshots}
```

A browser User-Agent is used throughout for consistency with the rest of this repository, but
**it was not required** — `docs.m5stack.com` and the two Aliyun OSS buckets served 200 to plain
`curl` as well.

## 1. Schematic and mechanical drawing

```bash
curl -fsSL -A "$UA" -o artifacts/schematic/Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf \
  "https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1178/Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf"
curl -fsSL -A "$UA" -o artifacts/mechanical/K132-Adv-cardputer-ADV.pdf \
  "https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1178/K132-Adv-cardputer-ADV.pdf"
```

Verify:

```bash
sha256sum -c <<'SUMS'
9553f5ee22b6e5f29a385388192e42c5ff76f16281b6f7ea9418f7b62a2d48b0  artifacts/schematic/Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf
6c937ca05e0894e54a3e47abb57e91de1b755dea032fd3f7438ea7a3e34550da  artifacts/mechanical/K132-Adv-cardputer-ADV.pdf
SUMS
```

Sizes: 878 155 B and 127 977 B. Both begin `%PDF-1.4`. **Validate by magic bytes, not by
extension** — this host has no `file`, so:

```bash
python3 -c "print(open('artifacts/schematic/Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf','rb').read(8))"
# b'%PDF-1.4'
```

## 2. Documentation snapshots

```bash
curl -fsSL -A "$UA" -o artifacts/docs/docs-en-core-Cardputer-Adv.html \
  "https://docs.m5stack.com/en/core/Cardputer-Adv"
curl -fsSL -A "$UA" -o artifacts/docs/docs-zh_CN-core-Cardputer-Adv.html \
  "https://docs.m5stack.com/zh_CN/core/Cardputer-Adv"
```

`f05bbb70ca0964ebcd465e866bf25302f24cd29ecada5099803c7786c3b54fec` (147 339 B) and
`4a285b0281f21864e394554161976786ac4846abfd7021f2422a3f4cced2ac61` (146 690 B).

⚠ **These hashes will drift** — the pages are live and M5Stack edits them. If yours differ,
that is a *finding* (compare the two and record what changed), not a failure. The retrieval date
is the identity that matters.

## 3. Source snapshots

```bash
git clone https://github.com/m5stack/M5Cardputer.git /tmp/M5Cardputer
git -C /tmp/M5Cardputer checkout f1392858b9994c3547120e602a57d3553d16ab01
rsync -a --exclude='.git' /tmp/M5Cardputer/ artifacts/source-snapshots/M5Cardputer-f1392858/

git clone -b CardputerADV https://github.com/m5stack/M5Cardputer-UserDemo.git /tmp/UserDemo
git -C /tmp/UserDemo checkout b549eac0a3c65bc108186c276b8fac0a214aaa4e
mkdir -p artifacts/source-snapshots/M5Cardputer-UserDemo-CardputerADV-b549eac0
cp /tmp/UserDemo/{partitions.csv,repos.json,sdkconfig.defaults,dependencies.lock} \
   artifacts/source-snapshots/M5Cardputer-UserDemo-CardputerADV-b549eac0/
cp /tmp/UserDemo/main/hal/hal_config.h \
   artifacts/source-snapshots/M5Cardputer-UserDemo-CardputerADV-b549eac0/
```

Tree digest for the M5Cardputer snapshot. **Record the recipe with the digest** — and note the
trap this pass walked into:

```bash
cd artifacts/source-snapshots/M5Cardputer-f1392858
LC_ALL=C find . -type f | LC_ALL=C sort | xargs sha256sum | sha256sum
# b0f20d35d31d24514320a0263b51aeb33a01a50a4f68c7f341f172d3c2f232d7
```

33 files, **117 087 bytes**. **MIT**, with SPDX headers in every file.

> ⚠ **`sha256sum` embeds the path it was given.** The *same bytes* produce three different tree
> digests depending on where you stand:
>
> | Run from | Path argument | Digest |
> |---|---|---|
> | repository root | `devices/m5stack/cardputer-adv/artifacts/…` | `cd081a07…` |
> | the device directory | `artifacts/…` | `918c61c4…` |
> | **inside the snapshot** | `.` | **`b0f20d35…`** ← the recorded one |
>
> Only the third is portable. The skill's rule is "pin the locale when hashing trees"; the
> working directory needs pinning for exactly the same reason, and it bit harder here than the
> locale did.

Only the UserDemo's *build configuration* is retained, not the full tree — it is 5 files and
they are the load-bearing ones. Reconstruct the rest from the pinned commit above; then
`python fetch_repos.py` clones the five dependencies at
`M5GFX@0.2.15`, `M5Unified@0.2.10`, `mooncake@v2.2.0`, `mooncake_log@v1.3.0`,
`smooth_ui_toolkit@v2.4.0`.

## 4. Not acquired — and how to get each one

| Artifact | Status | Command |
|---|---|---|
| **EasyLoader** | not-downloaded | `curl -fsSLO "https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1178/Easy_Loader_for_Cardputer-Adv.exe"` — a Windows self-extractor; expect the image plus esptool inside |
| **Factory firmware binary** | **blocked** — no M5Burner id resolved | Find the id first: browse `burner.m5stack.com`, then `curl -fsSL "https://burner.m5stack.com/api/v1/firmwares/$ID"`. ⚠ `/api/…` returns 401; **`/api/v1/…` is public** |
| Schematic sheet renders (4 × ~5848×4132 PNG) | in scratch, not committed | `curl -fsSLO "…/1178/Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58_page_0{1,2,3,4}.png"` |
| Stamp-S3A schematic | belongs to the **component** | [`components/m5stack/stamp-s3a`](../../../../components/m5stack/stamp-s3a/README.md) |
| StampS3 v0.2 schematic | belongs to the component | `…/522/Sch_M5StampS3_v0.2.pdf` — 348 884 B, `6d92e1ae…` |
| Cardputer v1.0/v1.1 schematic | in the v1.1 record | `…/1127/Sch_M5Cardputer.pdf` — **byte-identical to `…/481/…`** |
| `M5_Hardware` structure files | not-downloaded | `git clone --filter=blob:none --no-checkout https://github.com/m5stack/M5_Hardware.git` then sparse-checkout `Products/K132-Adv_Cardputer-Adv/Structures` |
| Product imagery | reference-only | **do not commit** — unlicensed. See [`../media.md`](../media.md) |
| CardputerZero schematic + label ZIP | not-downloaded | `…/1243/C154-CardputerZERO_SCH_V0.6.1_20260702.pdf`, `…/1243/CardputerZero_Labels.zip` |

## 5. Dead URL — do not retry

```
https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/522/Sch_M5StampS3_v0.2_page_01.png
```

Returns **402 bytes that are not a PNG**. The `_page_NN.png` render convention is per-product,
not universal. Checked 2026-09-04. **Not saved under a `.png` name.**

## 6. Verify-only

```bash
cd "$(git rev-parse --show-toplevel)"/devices/m5stack/cardputer-adv
python3 - <<'PY'
import json,hashlib,os,sys
m=json.load(open('acquisition/manifest.json')); root=os.getcwd(); bad=0
for a in m['artifacts']:
    d=a.get('destination')
    if not d or a.get('repository_state')=='not-downloaded': continue
    p=os.path.join(root, d.split('devices/m5stack/cardputer-adv/',1)[-1])
    if d.endswith('/'):
        print('DIR ', 'ok' if os.path.isdir(p) else 'MISSING', d); bad+= not os.path.isdir(p); continue
    if not os.path.exists(p): print('MISSING', d); bad+=1; continue
    h=hashlib.sha256(open(p,'rb').read()).hexdigest()
    ok = h==a['sha256'] and os.path.getsize(p)==a['bytes']
    print('OK  ' if ok else 'FAIL', d); bad += not ok
sys.exit(1 if bad else 0)
PY
```

## 7. Licensing summary

| Group | Artifacts | Status | Action |
|---|---|---|---|
| **Permissive, clear** | `M5Cardputer` snapshot, UserDemo build config | **MIT**, SPDX headers present | safe to stage |
| **Conditional** | UserDemo *full tree* (not retained) | MIT repo that **pins LGPL-3.0 RadioLib** | resolve before vendoring the whole tree |
| **Unknown terms** | schematic PDF, mechanical PDF, documentation HTML | no notice anywhere; openly published on the product page | **retained but left untracked** pending a user decision — the same position this repository already takes on M5Stack schematics |
| **Not licensed for redistribution** | all product imagery | `vendors/m5stack` §8 | **reference-only**, zero bytes committed |
| **Large** | sheet renders (~2.5 MB total) | unlicensed technical images | kept in scratch (archive repo), regenerable from the URLs above |

**User decision needed:** whether to stage the three unknown-terms documents
(1.15 MB combined). Recommendation: **stage** — they are small, they are the primary evidence
for the entire record, and this repository already tracks M5Stack schematics for other products.
