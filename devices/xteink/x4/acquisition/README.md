# Xteink X4 — acquisition

## Clean-clone commands, in execution order

The one tracked artifact for this device is **archived**, so a clean clone sees a
placeholder plus a symlink. To reacquire it:

```bash
# 1. The 16 MB OEM full-flash dump. No auth needed.
mkdir -p devices/xteink/x4/artifacts/firmware
curl -fsSL "https://raw.githubusercontent.com/abhishek-nerella/XTEINK-OEM-BIN-/main/flash.bin" \
     -o devices/xteink/x4/artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin

# 2. Verify before trusting it.
sha256sum devices/xteink/x4/artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin
# expect: b9cf27cc254c737c901f81e7fcf0c48308e29bd979848ab0ac0bf6c6f5e8c245
stat -c%s devices/xteink/x4/artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin
# expect: 16777216
```

**Expected failure mode:** the upstream repository is a single person's
re-upload of proprietary vendor firmware with no licence and no mirror. If it
disappears, the fallbacks in the
[placeholder](../artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin.ARCHIVED.md)
are the only route, and one of them (`zocs/eink-quick-flasher`) offers a
**different, non-identical** artifact — OTA app images, not a full flash.

## Licensing and disposition

| Artifact | Licence | Redistribution | Disposition |
|---|---|---|---|
| `xteink-x4-oem-full-flash-16mb.bin` | **None declared.** Vendor firmware re-uploaded by a third party | **unknown, probably prohibited** | `local-cache` (archived), **unstaged pending user review** |

The upstream repository has **no LICENSE file** and a 55-byte README. This is
proprietary firmware; treat it as all-rights-reserved.

## Not downloaded, and why

| Artifact | Status | Reacquisition |
|---|---|---|
| `x4_en_v5.1.6_ota.bin`, `x4_cn_v5.2.13_ota.bin` | **Git LFS pointers** in `zocs/eink-quick-flasher`; the ~130-byte pointers were seen, the blobs were not fetched | **`manual`** — needs `git lfs` or the LFS batch API. **Cheap to close** |
| X4 SPIFFS contents (3.4 MB, `0xC90000`) | Present *inside* the archived dump but never extracted | **`automatic`** — extract from the held image |
| Vendor OTA feed response | `http://gotaserver.xteink.com/api/check-update` | **`manual`** — request format unknown; contacting a vendor server was out of scope |
| Delisted X4 product page + imagery | Wayback CDX **timed out** | **`blocked`** — retry with a longer timeout or `matchType=prefix` |
| Any X4 teardown photograph | **Does not exist** | **`lost`** |

## Verification

```bash
python3 tools/archive_artifact.py --repo-root . --manifest <manifest> --verify
python3 tools/audit_archive.py
```
