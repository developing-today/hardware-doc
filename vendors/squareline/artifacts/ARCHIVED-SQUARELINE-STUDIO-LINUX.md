# Archived artifact — SquareLine Studio Linux distribution

The SquareLine Studio Linux ZIP that this directory would otherwise hold has been kept **outside the repository**. It is 172 MiB of proprietary, all-rights-reserved binaries with no redistribution grant, so it is neither committed nor staged.

- **Archived:** 2026-08-30
- **Moved to:** `archive/vendors/squareline/artifacts/` (same relative path)
- **Kept out of the repository:** 180 438 276 bytes (~172.1 MiB)
- **Redistribution status:** **restricted** · **Disposition:** **local-cache**

Nothing was lost. Everything this repository needs from the archive was extracted into Markdown before it was set aside — see [What was extracted](#what-was-extracted-and-where-it-now-lives).

---

## 1. `SquareLine_Studio_Linux_v1_6_1.zip`

| Field | Value |
|---|---|
| **Original path** | `vendors/squareline/artifacts/SquareLine_Studio_Linux_v1_6_1.zip` |
| **What it is** | SquareLine Studio 1.6.1 for Linux x86-64 — proprietary drag-and-drop LVGL UI editor. Extract-and-run; **not an AppImage** |
| **Version** | **1.6.1** |
| **Byte size** | **180 438 276** |
| **SHA-256** | `28bcfbd475ad1670ec688117cbfeebbd6b0bedb52b16e64011d4c6eeca47ab5d` |
| **Members** | **1 711**, flat top level (no wrapper directory in this release) |
| **Build date evidence** | ZIP entry timestamp for `SquareLine_Studio.x86_64`: **2026-04-23 09:59:48** |
| **Publisher** | SquareLine Kft. |
| **Licence** | Proprietary, all rights reserved — **no licence file ships inside the archive** |
| **Why it is not in the repository** | Size combined with an explicit all-rights-reserved licence and no redistribution permission |

### Source repository

**None exists.** SquareLine Studio is proprietary, closed-source, distributed only as a signed
installer from the vendor. There is no upstream repository to pin, no commit, and no third-party
redistribution that would be lawful to rely on — so the two vendor URLs above are the whole of
the recovery story, and the SHA-256 is doing more work here than usual.

This is recorded explicitly because an absent repository line should read as *checked and
absent*, not as an omission someone might later "fix" with a plausible-looking link.

## Reacquisition

**Verified 2026-08-30.** This host returns **HTTP 206 for non-existent paths too**, so check `Content-Type`: `application/x-zip-compressed` means a real file, `text/html` is a soft 404.

| # | URL | Result |
|---|---|---|
| 1 | `https://static.squareline.io/downloads/SquareLine_Studio_Linux_v1_6_1.zip` | **206**, `application/x-zip-compressed` ✅ — direct, no login |
| 2 | `https://squareline.io/downloads` | **200** — JS shell; the current version's link is rendered client-side only |

```sh
curl -fL -o SquareLine_Studio_Linux_v1_6_1.zip \
  -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36' \
  https://static.squareline.io/downloads/SquareLine_Studio_Linux_v1_6_1.zip
echo '28bcfbd475ad1670ec688117cbfeebbd6b0bedb52b16e64011d4c6eeca47ab5d  SquareLine_Studio_Linux_v1_6_1.zip' | sha256sum -c -
```

**Reacquisition status:** `automatic`. Older releases follow the same pattern with underscores for dots (`v1_6_0`, `v1_5_4`, …); see the [vendor guide](../README.md#2-url-pattern).

> A copy also exists in the local Nix store at `/nix/store/zbag2bp9nrj7m8rv64vfrmfry1rzmh1b-SquareLine_Studio_Linux_v1_6_1.zip`, placed there by `nix-prefetch-url`. That path is **garbage-collectable** and must not be treated as preservation.

## What was extracted, and where it now lives

| New document | Captures |
|---|---|
| [`vendors/squareline/README.md`](../README.md) | Host map and the `download.squareline.io` NXDOMAIN negative result; the underscore URL pattern; the **HTTP 206 soft-404 trap** with three negative controls; the JS-shell downloads page; the complete ZIP layout; the four bundled LVGL trees; the exact executable set `setup.sh` chmods; licence and redistribution findings |
| [`guides/nixos/README.md`](../../../guides/nixos/README.md#5-squareline-studio) | How the tool is packaged declaratively on NixOS, including the defect this artifact inspection exposed — a packaging that chmods only `*.x86_64`/`*.so` silently loses font conversion and the LVGL preview servers |

## Related

- Vendor sourcing guide: [`vendors/squareline/README.md`](../README.md)
- NixOS packaging and the wider embedded toolchain: [`guides/nixos/README.md`](../../../guides/nixos/README.md)
