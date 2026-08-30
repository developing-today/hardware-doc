# `sscom5.13.1.exe` — ARCHIVED, not deleted

This file is a placeholder standing in for a binary that was moved out of the repository.

| Field | Value |
|---|---|
| Original relative path | `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/tools/sscom5.13.1/sscom5.13.1.exe` |
| Archived to | `archive/hardware-doc/devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/tools/sscom5.13.1/sscom5.13.1.exe` |
| Archive date | **2026-08-24** |
| What it is | The **SSCOM V5.13.1 Windows serial terminal executable** — a 32-bit Windows GUI program. See [`README.md`](./README.md) for what SSCOM is and why it is here at all |
| SHA-256 | `51ea245a3d07436a86a4449b2791c1f37fa60e181dd128e8d7dd79cc1ad836ce` |
| Size | **451,072 bytes** (440.5 KiB) |
| Container it came from | `../Sscom5.13.1.zip` — **still present in this repository**, 420,199 bytes, SHA-256 `d85cce9c2494ec7de0163410f45d998c03ed181f01536979a3e0a0dd1256aa07` |
| Container file count | 3 members (2 regular files + 1 directory entry); 456,154 bytes extracted |
| Container extracted-tree digest | see [`README.md`](./README.md) |
| Version | **5.13.1** (distribution label, from the archive/filename). PE `VS_VERSION_INFO` reports `FileVersion 1.0.0.21`, `ProductVersion 1.0.0.0` — the author does not keep the resource version in step with the release name |
| Build date | **PE header timestamp `0x592960EC` = 2017-05-27 03:38:20 UTC.** ZIP member mtime is 2018-06-22 11:09 (repackaging date). Upstream `daxia.com` serves its `sscom.rar` with `Last-Modified: Fri, 26 May 2017 15:49:21 GMT` — **independently corroborating the 2017-05 build** |
| Architecture | `PE32 executable (GUI) Intel 80386, for MS Windows, 10 sections` — 32-bit x86 |
| Author / vendor | **Song Kaihua (宋凯华), "大虾" / daxia** — <http://www.daxia.com>. Repackaged and mirrored by Waveshare |
| License | **None stated.** Chinese freeware/shareware with an in-app registration solicitation. Redistribution status `unknown` |
| Upstream repo / git commit | **Not applicable** — no public VCS. (Historical note: a `sscom_source.zip` was published on `daxia.com` in 2006 for a much older version; it is *not* the source of this build. Internet Archive captures exist from 2006-12-15 and 2007-02-05 at `http://www.daxia.com/download/sscom_source.zip`) |
| Disposition | archived (`local-cache` outside the repository) |

## Why removal was OK

1. **It is a third-party Windows binary with no documentary value.** It is not part of this
   board's design, does not describe it, and contains nothing extractable — no schematic, no pin
   map, no datasheet, no configuration specific to this product. It is an off-the-shelf tool that
   Waveshare's wiki happens to link.
2. **It is fully regenerable from four independent sources**, one of which is a file that is
   still in this repository (`../Sscom5.13.1.zip`), so recovery needs no network at all.
3. **It is not needed to use this board.** Any serial terminal works. On Linux/macOS this
   `.exe` is unusable without Wine.
4. **It is a binary blob in a documentation tree.** Executables in a docs repository are a
   liability: unreviewable, unscannable in diffs, and — as noted in
   [`README.md`](./README.md) — this one ships with a hard-coded outbound network default.

The size saved is trivial (441 KiB). The reason to do it is hygiene, not bytes. **The ZIP was
deliberately kept** rather than archived instead: at 420 KB it is the byte-exact original, and
keeping it means the `.exe` is recoverable offline. Storing both the ZIP *and* its extracted
`.exe` was the only genuine redundancy, and that is what was removed.

## Reacquire

```bash
# Source 1 — from the ZIP still in this repository (no network required, byte-exact)
unzip -j ../Sscom5.13.1.zip 'sscom5.13.1/sscom5.13.1.exe' -d .

# Source 2 — Waveshare shared file pool (the path this repository originally used)
curl -L -O https://files.waveshare.com/wiki/common/Sscom5.13.1.zip
unzip -j Sscom5.13.1.zip 'sscom5.13.1/sscom5.13.1.exe' -d .

# Source 3 — Internet Archive capture of the Waveshare URL (2026-03-13; earlier captures at
#            20250822151448 and 20260102181659 share the same CDX content digest)
curl -L -o Sscom5.13.1.zip \
  "https://web.archive.org/web/20260313002151id_/https://files.waveshare.com/wiki/common/Sscom5.13.1.zip"

# Source 4 — the ORIGINAL AUTHOR's own distribution (upstream, not a mirror).
#            NOTE: this is a .rar, not the Waveshare .zip, so the *container* hash differs.
curl -L -O http://www.daxia.com/download/sscom.rar
unrar x sscom.rar        # or: 7z x sscom.rar

# Source 5 — Internet Archive captures of the author's URL, back to 2007
#   http://web.archive.org/web/20250624120136id_/http://www.daxia.com/download/sscom.rar
```

## Verify

```bash
sha256sum sscom5.13.1.exe
# expect 51ea245a3d07436a86a4449b2791c1f37fa60e181dd128e8d7dd79cc1ad836ce

# and the container, if you fetched source 2 or 3:
sha256sum Sscom5.13.1.zip
# expect d85cce9c2494ec7de0163410f45d998c03ed181f01536979a3e0a0dd1256aa07

# confirm the build identity independently of the hash:
python3 - <<'EOF'
import struct, datetime
d = open('sscom5.13.1.exe','rb').read()
pe = struct.unpack_from('<I', d, 0x3c)[0]
assert d[pe:pe+4] == b'PE\0\0'
ts = struct.unpack_from('<I', d, pe+8)[0]
print('machine 0x%04x' % struct.unpack_from('<H', d, pe+4)[0])   # expect 0x014c (i386)
print('link timestamp', datetime.datetime.fromtimestamp(ts, datetime.UTC))
# expect 2017-05-27 03:38:20+00:00
EOF
```

## URL probe results (2026-08-24)

| URL | HTTP | Content-Length | Last-Modified | Notes |
|---|---|---:|---|---|
| `https://files.waveshare.com/wiki/common/Sscom5.13.1.zip` | `200 OK` | 420199 — **matches local ZIP exactly** | `Mon, 28 Oct 2024 11:37:49 GMT` | Waveshare's `/wiki/common/` shared pool — linked from many product wikis, so not tied to this product's page |
| `http://www.daxia.com/download/sscom.rar` | `200 OK` | 417621 | `Fri, 26 May 2017 15:49:21 GMT` | **Upstream author.** Site front page advertises "SSCOM5.13". Different container (`.rar`), same program |
| `https://web.archive.org/cdx/…/Sscom5.13.1.zip` | `200 OK` | — | 5 captures: 2025-08-22, 2025-10-30, 2026-01-02, 2026-02-12, 2026-03-13 | All share CDX content digest `UYKG6LAWS4A3GST2QVFHHJGR7RPYMJGH` — the file has not changed across seven months of captures |
| `https://web.archive.org/cdx/…/daxia.com/download/sscom.rar` | `200 OK` | — | captures 2007-02-05 → 2025-08-15 | Content digest `NM23AQ6XAILHY22YEHG5XGQ6FESNMUXP` stable since at least 2022-01-12 |
