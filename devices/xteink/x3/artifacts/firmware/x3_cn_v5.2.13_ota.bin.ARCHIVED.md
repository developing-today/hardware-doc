# ARCHIVED: `x3_cn_v5.2.13_ota.bin`

> This file was **moved out of the repository**, not deleted.
> Archived **2026-09-23**.

**Reason:** Xteink X3 stock OTA firmware image (app partition only), CN default UI, version V5.2.13. Proprietary vendor firmware redistributed by a third party with no licence statement — redistribution status unknown, so it is not tracked in the repository. It is byte-reproducible: the Git-LFS oid published in the upstream pointer file IS this file's SHA-256, so a placeholder carries complete integrity. MOVED OUT OF SCRATCH 2026-09-20: the image was fetched on 2026-09-11 and parsed, but the acquisition record stated it was 'not retained' while the bytes in fact sat in archive/devices/xteink/shared-artifacts/research-scratch/x3-lfs/. Scratch is not storage. Mined before archiving — see the extraction document.

## Identity

| Field | Value |
|---|---|
| Original repo path | `devices/xteink/x3/artifacts/firmware/x3_cn_v5.2.13_ota.bin` |
| Archived to | `/home/user/repo-archive/hardware-doc/devices/xteink/x3/artifacts/firmware/x3_cn_v5.2.13_ota.bin` |
| Type | file |
| Size | 6,254,064 B (5.96 MiB) |
| SHA-256 | `0b2cbc4a6414aef4ad6e676b59fdefa3b529189758953765b26df02bac77bcb6` |
| Last modified (mtime) | 2026-09-11 23:42:36Z |
| Upstream repository | zocs/eink-quick-flasher |
| Commit | `79d2f5b8f1df08d2c8fb33146ac5f887790ddb9e` |
| Document version | `XTOS V5.2.13 (CN default UI)` |
| Retrieved | 2026-09-11 (via the GitHub LFS batch API); archived 2026-09-20 |
| License | none declared. Proprietary Xteink vendor firmware, mirrored by a third party. Redistribution status: unknown. |
| Path within upstream repo | `firmware/x3_cn_v5.2.13_ota.bin` |
| Difficulty to re-obtain | easy, BUT NOT BY PLAIN DOWNLOAD — this is a Git-LFS blob. See the warning below: every auto-generated URL in the next section returns a ~130-byte pointer file, not firmware. |
| Access notes | Git-LFS blob. Use the unauthenticated LFS batch API (recipe in zocs-x3-stock-images.NOT-FETCHED.md, status executed-success 2026-09-11). The signed S3 href expires in 3600 s. |

## How to get it back

Independent recovery URLs, most reliable first:

- raw file, pinned to commit (exact bytes):  
  <https://raw.githubusercontent.com/zocs/eink-quick-flasher/79d2f5b8f1df08d2c8fb33146ac5f887790ddb9e/firmware/x3_cn_v5.2.13_ota.bin>
- GitHub blob view, pinned to commit:  
  <https://github.com/zocs/eink-quick-flasher/blob/79d2f5b8f1df08d2c8fb33146ac5f887790ddb9e/firmware/x3_cn_v5.2.13_ota.bin>
- jsDelivr CDN mirror, pinned to commit:  
  <https://cdn.jsdelivr.net/gh/zocs/eink-quick-flasher@79d2f5b8f1df08d2c8fb33146ac5f887790ddb9e/firmware/x3_cn_v5.2.13_ota.bin>
- whole-repository tarball at that commit (**works for directories**):  
  <https://codeload.github.com/zocs/eink-quick-flasher/tar.gz/79d2f5b8f1df08d2c8fb33146ac5f887790ddb9e>
- current default branch (may have changed):  
  <https://github.com/zocs/eink-quick-flasher/raw/HEAD/firmware/x3_cn_v5.2.13_ota.bin>
- GitHub LFS batch API endpoint — POST the oid+size, get a 3600 s signed URL. THIS IS THE ONE THAT WORKS:  
  <https://github.com/zocs/eink-quick-flasher.git/info/lfs/objects/batch>
- raw path — redirects to media.githubusercontent.com for LFS paths; works in a browser, may return the pointer to a bare curl:  
  <https://github.com/zocs/eink-quick-flasher/raw/79d2f5b8f1df08d2c8fb33146ac5f887790ddb9e/firmware/x3_cn_v5.2.13_ota.bin>
- Wayback Machine capture of the mirroring repository:  
  <https://web.archive.org/web/2/https://github.com/zocs/eink-quick-flasher>

Fuller sourcing for this artifact is recorded in `devices/xteink/x3/artifacts/firmware/x3-stock-firmware-teardown.md`.

Restore from the local archive:

```bash
mv "/home/user/repo-archive/hardware-doc/devices/xteink/x3/artifacts/firmware/x3_cn_v5.2.13_ota.bin" \
   "devices/xteink/x3/artifacts/firmware/x3_cn_v5.2.13_ota.bin"
```

Or re-download and verify:

```bash
curl -fsSL "https://raw.githubusercontent.com/zocs/eink-quick-flasher/79d2f5b8f1df08d2c8fb33146ac5f887790ddb9e/firmware/x3_cn_v5.2.13_ota.bin" -o "x3_cn_v5.2.13_ota.bin"
echo "0b2cbc4a6414aef4ad6e676b59fdefa3b529189758953765b26df02bac77bcb6  x3_cn_v5.2.13_ota.bin" | sha256sum -c -
```

If every URL above is dead, try the Wayback Machine:

    https://web.archive.org/web/2/https://raw.githubusercontent.com/zocs/eink-quick-flasher/79d2f5b8f1df08d2c8fb33146ac5f887790ddb9e/firmware/x3_cn_v5.2.13_ota.bin


---

## ⚠ Read this before using any URL above

**This is a Git-LFS blob.** The `raw.githubusercontent.com`, `cdn.jsdelivr.net`, `blob/` and
repository-tarball URLs generated above all return a **~130-byte pointer file** that looks like
this, not 6.25 MB of firmware:

```
version https://git-lfs.github.com/spec/v1
oid sha256:0b2cbc4a6414aef4ad6e676b59fdefa3b529189758953765b26df02bac77bcb6
size 6254064
```

A naive `curl` will "succeed", write a text stub with a `.bin` extension, and fail silently.
**Always check the size and hash.**

### The recipe that works — `executed-success`, 2026-09-11 and re-verified 2026-09-20

No `git lfs`, no clone, no authentication:

```bash
OID=0b2cbc4a6414aef4ad6e676b59fdefa3b529189758953765b26df02bac77bcb6
SIZE=6254064

curl -s -X POST \
  "https://github.com/zocs/eink-quick-flasher.git/info/lfs/objects/batch" \
  -H "Accept: application/vnd.git-lfs+json" \
  -H "Content-Type: application/vnd.git-lfs+json" \
  -d "{\"operation\":\"download\",\"transfers\":[\"basic\"],
       \"objects\":[{\"oid\":\"$OID\",\"size\":$SIZE}]}" -o batch.json

URL=$(python3 -c "import json;print(json.load(open('batch.json'))['objects'][0]['actions']['download']['href'])")
curl -sL "$URL" -o x3_cn_v5.2.13_ota.bin
sha256sum x3_cn_v5.2.13_ota.bin     # must equal $OID
```

**The Git-LFS `oid` *is* the SHA-256 of the content**, so the pointer alone is a complete
integrity record — which is why this artifact can be archived without loss. The signed S3 `href`
expires in **3600 s**; re-run the batch call rather than caching the URL. A captured batch
response from the 2026-09-11 fetch is preserved at
`archive/devices/xteink/shared-artifacts/research-scratch/x3-lfs/batch.json` (its signed URL is long expired; kept as evidence the
endpoint answers unauthenticated).

## What was mined out of it before archiving

Full write-up: [`x3-stock-firmware-teardown.md`](x3-stock-firmware-teardown.md).

Headline facts, all `executed-success` from parsing these bytes on 2026-09-20:

| | |
|---|---|
| Vendor OS name | **`XTOS V5.2.13`** |
| Chip | `chip_id = 5` → **ESP32-C3**; backend device string **`ESP32C3_X3`** |
| Build toolchain | **PlatformIO on Windows**, `framework-arduinoespressif32`, ESP-IDF **v4.4.7** |
| BLE stack | **NimBLE-Arduino 2.3.6** |
| Filesystem | **LittleFS**, mounted at `/littlefs` — *not* SPIFFS |
| Backends | `api-prod.xteink.cn`, `bofi.xteink.cn`, hardcoded `8.130.157.48:5000` |
| On-device HTTP API | ~30 endpoints, full list in the teardown |

## Provenance correction

The sibling acquisition record
[`zocs-x3-stock-images.NOT-FETCHED.md`](zocs-x3-stock-images.NOT-FETCHED.md) previously stated
this image was *"fetched and parsed but **not retained**"* and recorded its disposition as
`reference-only` / `not-downloaded`. **That was wrong from 2026-09-11 onward** — the bytes had
been retained, in `archive/devices/xteink/shared-artifacts/research-scratch/x3-lfs/`. This pass moved them to the archive and corrected
that record. The other three images in that table genuinely were never fetched and remain
`reference-only`.
