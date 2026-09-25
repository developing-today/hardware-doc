# Xteink X3 — acquisition

## Clean-clone commands, in execution order

Both tracked artifact sets are **archived**, so a clean clone sees placeholders
plus symlinks. To reacquire:

```bash
# 1. English teardown, 13 images. The album page is a JS shell — enumerate first.
mkdir -p devices/xteink/x3/artifacts/teardown/imgur-2026-07-01
curl -fsSL "https://imgur.com/ajaxalbums/getimages/OA6CS2C/hit.json" -o /tmp/album.json
python3 - <<'PY'
import json, subprocess
for i, im in enumerate(json.load(open('/tmp/album.json'))['data']['images'], 1):
    url = f"https://i.imgur.com/{im['hash']}{im['ext']}"
    out = f"devices/xteink/x3/artifacts/teardown/imgur-2026-07-01/{i:02d}-{im['hash']}{im['ext']}"
    subprocess.run(['curl','-fsSL','-m','60',url,'-o',out], check=True)
PY

# 2. Chinese teardown + schematic sketch, 10 images + README.
mkdir -p devices/xteink/x3/artifacts/teardown/sunwoods-cn
for i in 01 02 03 04 05 06 07 08 09 10; do
  curl -fsSL "https://raw.githubusercontent.com/sunwoods/Xteink-X3/main/readme-img/$i.jpg" \
       -o "devices/xteink/x3/artifacts/teardown/sunwoods-cn/$i.jpg"
done
curl -fsSL "https://raw.githubusercontent.com/sunwoods/Xteink-X3/main/README.md" \
     -o devices/xteink/x3/artifacts/teardown/sunwoods-cn/README.upstream.md
```

**Expected failure mode for #1:** scraping `https://imgur.com/a/xteink-x3-teardown-OA6CS2C`
directly returns **2 of 13** images. The `ajaxalbums` endpoint is undocumented and
could disappear; if it does, the per-image SHA-256 list in the
[placeholder](../artifacts/teardown/imgur-2026-07-01.ARCHIVED.md) still identifies
every file, and the Reddit post remains as a pointer.

## Verify

Per-file SHA-256, byte size and captions are recorded in both placeholders and in
`manifest.json` inside the archived Imgur directory.

```bash
python3 tools/archive_artifact.py --repo-root . --manifest <manifest> --verify
python3 tools/audit_archive.py
```

## Licensing and disposition

| Artifact set | Licence | Redistribution | Disposition |
|---|---|---|---|
| Imgur teardown, 13 images, 18.61 MiB | **unknown** — a Reddit/Imgur user post, no terms stated | **unknown** | archived, **unstaged pending user review** |
| `sunwoods` teardown + schematic, 10 images, 4.80 MiB | **none declared** — no LICENSE in the repository | **unknown** | archived, **unstaged pending user review** |

Neither uploader stated terms. Both are firsthand photographs of a consumer device
by their authors.

## Not downloaded, and why

| Artifact | Status | Reacquisition |
|---|---|---|
| `x3_en_v1.0.7_full.bin`, `x3_en_v5.2.13_full.bin`, `x3_cn_v5.2.13_full.bin`, `x3_cn_v5.2.13_ota.bin` | **Git LFS pointers** (~130 B each) in [`zocs/eink-quick-flasher`](https://github.com/zocs/eink-quick-flasher/tree/main/firmware) | **`manual`** — needs `git lfs` or the LFS batch API. **The cheapest way to obtain the first X3 firmware image.** Licence: none declared; vendor firmware; redistribution **unknown** |
| `X3-FLASHER-GUIDE.md` / `-EN.md` | Present in the same repo, not fetched | **`automatic`** — plain raw fetch. The most detailed X3 flashing documentation that exists |
| An X3 flash dump | **Never obtained** | **`manual`** — dump a USB-unlocked unit |
| Vendor product imagery | Listing is **live**; URLs are in `vendors/xteink/artifacts/store-snapshots/2026-09-04/products-p1.json` under `products[].images[].src` | **`automatic`** — **capture before the X3 is delisted**, as happened to the X4 |
| Vendor OTA feed | `http://gotaserver.xteink.com/api/check-update` | **`manual`** — request format unknown |

## The most valuable work needs no network at all

Three open questions could be closed by **reading images already archived here**:

1. `sunwoods-cn/02.jpg` — the schematic sketch — would likely resolve the
   **GPIO0 / GPIO20 dual-assignment**.
2. `imgur-2026-07-01/13-Ay3rpJg.jpg` (5760×3240) would test the **"DS1307"**
   caption against the actual marking.
3. `imgur-2026-07-01/10-YgdHbR1.jpg` and `11-bgXQoVr.jpg` — captioned *"at an
   angle to better read the chip labels"* — would likely give the **Puya flash
   part number**.
