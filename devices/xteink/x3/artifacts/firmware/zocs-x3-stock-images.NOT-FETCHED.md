# Xteink X3 stock firmware images — acquisition record

**Status: `not-downloaded` into this repository.** This file is a
**self-sufficient placeholder**: everything needed to obtain and verify all four
images is here, and **none of it requires `git lfs`, a clone, or access to any
archive.** Written 2026-09-11.

## Why this file exists

The 2026-09-04 sweep recorded these four images as *"Git LFS blobs that were not
fetched"* and the verification report listed them as an open gap, noting the
`.bin` entries in the upstream Git tree are **~130-byte LFS pointer files**, so a
naive `curl` of the raw URL yields a text stub rather than firmware.

This pass **resolved the acquisition method and verified it end-to-end**, but did
not vendor the bytes: three of the four are 16 MiB each, they are proprietary
vendor firmware with no licence, and the repository already archives the
comparable X4 dump rather than tracking it.

## The four images

Upstream: [`zocs/eink-quick-flasher`](https://github.com/zocs/eink-quick-flasher),
commit **`79d2f5b8f1df08d2c8fb33146ac5f887790ddb9e`** (HEAD at 2026-09-11),
directory `firmware/`.

| File | Version | Lang | Type | **Bytes** | **SHA-256 (= the Git-LFS oid)** |
|---|---|---|---|---:|---|
| `x3_en_v1.0.7_full.bin` | **V1.0.7** | EN | full 16 MB flash | **16,777,216** | `f631402cceff2a3e39252ca1fc71afee8274b3060afe7f81d2e5dd45413c8b22` |
| `x3_en_v5.2.13_full.bin` | **V5.2.13** | EN | full 16 MB flash | **16,777,216** | `37efcb7db2422b6c7b86b23b2e82b0fb4453ebde350014e7f8e8ad3f06ca2dac` |
| `x3_cn_v5.2.13_full.bin` | **V5.2.13** | CN | full 16 MB flash | **16,777,216** | `edfe1e5eb0083b860f82281aa25391a3fdea2a598a1fb618408808a18a6ca9aa` |
| `x3_cn_v5.2.13_ota.bin` | **V5.2.13** | CN | OTA, app only | **6,254,064** | `0b2cbc4a6414aef4ad6e676b59fdefa3b529189758953765b26df02bac77bcb6` |

**The Git-LFS `oid` *is* the SHA-256 of the file content.** Those hashes are read
from the pointer files and are therefore usable as integrity checks without ever
touching LFS.

Two further LFS blobs sit alongside them and are **not** stock firmware:
`firmware/crosspoint-x3-alpha/{bootloader,firmware,partitions}.bin`.

## Reacquisition — `automatic`, verified working 2026-09-11

**No `git lfs` required.** GitHub's LFS batch API answers unauthenticated:

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

- **Status: `executed-success`**, 2026-09-11. The OTA image was fetched
  (HTTP 200, 6,254,064 bytes) and its SHA-256 **matched the oid exactly**.
- The signed S3 `href` expires in **3600 s**; re-run the batch call, do not cache
  the URL.
- To get a pointer for any other file:
  `gh api "repos/zocs/eink-quick-flasher/contents/firmware/<name>?ref=79d2f5b8f1df08d2c8fb33146ac5f887790ddb9e" --jq .content | base64 -d`
- Fallback, if the batch API ever refuses: `git lfs` after a normal clone, or
  `https://github.com/zocs/eink-quick-flasher/raw/79d2f5b/firmware/<name>`
  (which redirects to `media.githubusercontent.com` for LFS paths).

## What the fetched image establishes

The OTA image was fetched and parsed but **not retained**. Its ESP image header
and `esp_app_desc_t` read:

| Field | Value |
|---|---|
| Magic | `0xE9` — a valid ESP application image |
| **`chip_id`** | **5 = ESP32-C3** |
| Segments | 6 |
| Entry point | `0x40381E52` |
| `project_name` | **`arduino-lib-builder`** |
| Version string in the descriptor | `esp-idf: v4.4.7 38eeba213a` |
| `idf_ver` | **`v4.4.7-dirty`** |
| Build time/date in descriptor | `12:29:20`, `Mar  5 2024` — the **Arduino core prebuilt** date, not the app's |
| Strings present | `5.2.13`, `xteink`, `xteink_ble` |

**Two findings:**

1. **`chip_id = 5` independently confirms the X3 is an ESP32-C3**, from a
   machine-readable field in a vendor image — a second mechanism, alongside the
   FreeInk profile, the Chinese BOM and the X4's own dump.
2. **The X3 stock firmware is built on the same Arduino / ESP-IDF v4.4.7 base as
   the X4's**, which this repository already established by parsing the X4 dump.
   That is direct support for the existing conclusion that **one codebase serves
   both C3 models** — the same reason the version number `V5.2.13` appears on
   both devices.

**`xteink_ble` is a string in an X3 image.** The X3's BLE capability has not been
characterised anywhere in this tree; this is the first evidence that the stock
firmware carries a BLE component.

## Licensing and disposition

| Field | Value |
|---|---|
| Redistribution status | **`unknown`** — proprietary vendor firmware redistributed by a third party with no licence statement |
| Disposition | **`reference-only`** |
| Repository state | `not-downloaded` |
| Reacquisition | **`automatic`** — the recipe above, verified 2026-09-11 |
| Total if fetched | **56,585,712 bytes** across four files |

## Cited from

[`../../factory-firmware.md`](../../factory-firmware.md) ·
[`../../gaps-and-conflicts.md`](../../gaps-and-conflicts.md) ·
[`../../commands.md`](../../commands.md) ·
[`../../sources.md`](../../sources.md) (source **X310**).
