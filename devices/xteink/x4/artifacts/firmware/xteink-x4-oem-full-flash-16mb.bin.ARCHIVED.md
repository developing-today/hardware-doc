# ARCHIVED: `xteink-x4-oem-full-flash-16mb.bin`

> This file was **moved out of the repository**, not deleted.
> Archived **2026-09-04**.

**Reason:** 16 MiB opaque factory flash image — large, binary, licence unknown, and re-fetchable from a public repository.

An identical copy was already present in the archive (content fingerprint `b9cf27cc254c737c…`, 1 file(s)), so this pass did not create a second copy.

## Identity

| Field | Value |
|---|---|
| Original repo path | `devices/xteink/x4/artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin` |
| Archived to | `/home/user/repo-archive/hardware-doc/devices/xteink/x4/artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin` |
| Type | file |
| Size | 16,777,216 B (16.00 MiB) |
| SHA-256 | `b9cf27cc254c737c901f81e7fcf0c48308e29bd979848ab0ac0bf6c6f5e8c245` |
| Last modified (mtime) | 2026-09-04 07:38:49Z |
| Upstream repository | abhishek-nerella/XTEINK-OEM-BIN- |
| Author / committer | abhishek-nerella (GitHub user; the origin of the dump itself — which unit, which stock version — is NOT documented upstream) |
| Retrieved | 2026-09-04 |
| License | None declared (no LICENSE file). Vendor firmware; treat as all-rights-reserved. |
| Path within upstream repo | `flash.bin` |
| Difficulty to re-obtain | Easy today — a single unauthenticated raw fetch. But it is a one-person re-upload of proprietary firmware with no provenance and no mirror, so it is exactly the kind of artifact that vanishes. |
| Access notes | No authentication needed. A GitHub token was used only to avoid API rate limits; raw.githubusercontent.com needs none. |

## How to get it back

Independent recovery URLs, most reliable first:

- current default branch (may have changed):  
  <https://github.com/abhishek-nerella/XTEINK-OEM-BIN-/raw/HEAD/flash.bin>
- original download URL:  
  <https://raw.githubusercontent.com/abhishek-nerella/XTEINK-OEM-BIN-/main/flash.bin>
- same blob via the github.com raw redirect (different host path):  
  <https://github.com/abhishek-nerella/XTEINK-OEM-BIN-/raw/main/flash.bin>
- repository web view — use to confirm the blob still exists and read its size:  
  <https://github.com/abhishek-nerella/XTEINK-OEM-BIN-/blob/main/flash.bin>
- NOT byte-identical — an independent stock-firmware set (Git LFS) carrying x4_en_v5.1.6_ota.bin and x4_cn_v5.2.13_ota.bin, which are ~6 MB OTA app-only images rather than a full flash. Use if this dump is lost and an app image will do.:  
  <https://github.com/zocs/eink-quick-flasher/tree/main/firmware>

Restore from the local archive:

```bash
mv "/home/user/repo-archive/hardware-doc/devices/xteink/x4/artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin" \
   "devices/xteink/x4/artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin"
```

Or re-download and verify:

```bash
curl -fsSL "https://github.com/abhishek-nerella/XTEINK-OEM-BIN-/raw/HEAD/flash.bin" -o "xteink-x4-oem-full-flash-16mb.bin"
echo "b9cf27cc254c737c901f81e7fcf0c48308e29bd979848ab0ac0bf6c6f5e8c245  xteink-x4-oem-full-flash-16mb.bin" | sha256sum -c -
```

If every URL above is dead, try the Wayback Machine:

    https://web.archive.org/web/2/https://github.com/abhishek-nerella/XTEINK-OEM-BIN-/raw/HEAD/flash.bin

