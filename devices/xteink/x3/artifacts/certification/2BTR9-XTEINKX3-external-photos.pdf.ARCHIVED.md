# ARCHIVED: `2BTR9-XTEINKX3-external-photos.pdf`

> This file was **moved out of the repository**, not deleted.
> Archived **2026-09-11** by the round-2 index merge.

**Reason:** bulk FCC exhibit — external photos, 512,425 B (0.49 MiB). The round-2 artifact split keeps internal photographs and ID-label exhibits in the repository (they are the identification and teardown evidence) and archives the full test reports, RF-exposure annexes, users manuals and external-photo sets, which are bulky and repetitive.

## Identity

| Field | Value |
|---|---|
| Original repo path | `devices/xteink/x3/artifacts/certification/2BTR9-XTEINKX3-external-photos.pdf` |
| Archived to | `/home/user/repo-archive/hardware-doc/devices/xteink/x3/artifacts/certification/2BTR9-XTEINKX3-external-photos.pdf` |
| Type | file (PDF, magic-byte validated `%PDF`) |
| Size | 512,425 B (0.49 MiB) |
| SHA-256 | `eee16223c0806e6a529a9abe53421612103c4a4cc491f8ee442dfbf4a5aae3ce` |
| FCC ID | **`2BTR9-XTEINKX3`** |
| Exhibit type | **External Photos** |
| Exhibit title, as filed | External Photos |
| FCC document id | 8932225 |
| Upstream publication date | 2025-12-26 |
| Grant date | 2025-12-26 |
| Equipment class | XTEINK X3, 2402-2480 MHz, 2412-2462 MHz |
| Applicant | Shenzhen Xiaohu Xingtong Technology Co., Ltd. 🇨🇳 |
| Test firm | Shenzhen CTB Testing Technology Co., Ltd. |
| Retrieved | 2026-09-11 |
| Licence | **US Government public record.** FCC equipment-authorisation exhibits are published by a federal agency under 47 CFR §2.1033 and carry no copyright claim by the agency. |
| Redistribution status | **`allowed`** |
| Disposition | `archive`, placeholder in repository |

## How to get it back

Independent reacquisition URLs, most reliable first:

- <https://fccid.io/2BTR9-XTEINKX3/External-Photos/External-Photos-8932225.pdf>  
  fccid.io mirror — **200**, but only to a non-browser UA (`curl/8.5.0`, `WhatsApp/2.23.20.0`, `ChatGPT-User/1.0`, `ClaudeBot/1.0`). A Chrome UA gets a Cloudflare 403. The `.pdf` suffix is required.

- <https://apps.fcc.gov/eas/GetApplicationAttachment.html?id=8932225>  
  official FCC Equipment Authorization System attachment — the primary record. **403 to all five UAs tried from this host on 2026-09-11**; try from another network.

- <https://fcc.report/FCC-ID/2BTR9-XTEINKX3/8932225.pdf>  
  fcc.report mirror. **403 to all five UAs tried on 2026-09-11.**

- <https://fccid.io/2BTR9-XTEINKX3>  
  the filing's exhibit index — re-read the row to recover a changed document slug.

- <https://web.archive.org/web/2/https://fccid.io/2BTR9-XTEINKX3/External-Photos/External-Photos-8932225.pdf>  
  Wayback Machine, if every live route is dead.

Restore from the local archive, if you have one:

```bash
mv "/home/user/repo-archive/hardware-doc/devices/xteink/x3/artifacts/certification/2BTR9-XTEINKX3-external-photos.pdf" \
   "devices/xteink/x3/artifacts/certification/2BTR9-XTEINKX3-external-photos.pdf"
```

Or re-download and verify — note the User-Agent, which is not optional:

```bash
curl -fsSL -A "curl/8.5.0" "https://fccid.io/2BTR9-XTEINKX3/External-Photos/External-Photos-8932225.pdf" -o "2BTR9-XTEINKX3-external-photos.pdf"
echo "eee16223c0806e6a529a9abe53421612103c4a4cc491f8ee442dfbf4a5aae3ce  2BTR9-XTEINKX3-external-photos.pdf" | sha256sum -c -
```

The archive path above is a **convenience**. Everything needed to recover this file without the archive — hash, byte size, FCC ID, exhibit type, document id, publication date and 5 URLs — is in this file.
