# ARCHIVED: `2ASYE-T-QT-PRO-external-photos.pdf`

> This file was **moved out of the repository**, not deleted.
> Archived **2026-09-11** by the round-2 index merge.

**Reason:** bulk FCC exhibit — external photos, 199,661 B (0.19 MiB). The round-2 artifact split keeps internal photographs and ID-label exhibits in the repository (they are the identification and teardown evidence) and archives the full test reports, RF-exposure annexes, users manuals and external-photo sets, which are bulky and repetitive.

## Identity

| Field | Value |
|---|---|
| Original repo path | `devices/lilygo/t-qt/artifacts/certification/2ASYE-T-QT-PRO-external-photos.pdf` |
| Archived to | `/home/user/repo-archive/hardware-doc/devices/lilygo/t-qt/artifacts/certification/2ASYE-T-QT-PRO-external-photos.pdf` |
| Type | file (PDF, magic-byte validated `%PDF`) |
| Size | 199,661 B (0.19 MiB) |
| SHA-256 | `a6424be9d8f42f8afbe2a0e576af45417a8fad3d9dcac100e8387760bd711853` |
| FCC ID | **`2ASYE-T-QT-PRO`** |
| Exhibit type | **External Photos** |
| Exhibit title, as filed | External Photos |
| FCC document id | 6304969 |
| Upstream publication date | 2022-12-31 |
| Grant date | 2022-12-31 |
| Equipment class | T-QT Pro, 2402-2480 MHz, 2412-2472 MHz |
| Applicant | Shenzhen Xin Yuan Electronic Technology Co., Ltd. 🇨🇳 |
| Test firm | Shenzhen Accurate Technology Co., Ltd. |
| Retrieved | 2026-09-11 |
| Licence | **US Government public record.** FCC equipment-authorisation exhibits are published by a federal agency under 47 CFR §2.1033 and carry no copyright claim by the agency. |
| Redistribution status | **`allowed`** |
| Disposition | `archive`, placeholder in repository |

## How to get it back

Independent reacquisition URLs, most reliable first:

- <https://fccid.io/2ASYE-T-QT-PRO/External-Photos/External-Photos-6304969.pdf>  
  fccid.io mirror — **200**, but only to a non-browser UA (`curl/8.5.0`, `WhatsApp/2.23.20.0`, `ChatGPT-User/1.0`, `ClaudeBot/1.0`). A Chrome UA gets a Cloudflare 403. The `.pdf` suffix is required.

- <https://apps.fcc.gov/eas/GetApplicationAttachment.html?id=6304969>  
  official FCC Equipment Authorization System attachment — the primary record. **403 to all five UAs tried from this host on 2026-09-11**; try from another network.

- <https://fcc.report/FCC-ID/2ASYE-T-QT-PRO/6304969.pdf>  
  fcc.report mirror. **403 to all five UAs tried on 2026-09-11.**

- <https://fccid.io/2ASYE-T-QT-PRO>  
  the filing's exhibit index — re-read the row to recover a changed document slug.

- <https://web.archive.org/web/2/https://fccid.io/2ASYE-T-QT-PRO/External-Photos/External-Photos-6304969.pdf>  
  Wayback Machine, if every live route is dead.

Restore from the local archive, if you have one:

```bash
mv "/home/user/repo-archive/hardware-doc/devices/lilygo/t-qt/artifacts/certification/2ASYE-T-QT-PRO-external-photos.pdf" \
   "devices/lilygo/t-qt/artifacts/certification/2ASYE-T-QT-PRO-external-photos.pdf"
```

Or re-download and verify — note the User-Agent, which is not optional:

```bash
curl -fsSL -A "curl/8.5.0" "https://fccid.io/2ASYE-T-QT-PRO/External-Photos/External-Photos-6304969.pdf" -o "2ASYE-T-QT-PRO-external-photos.pdf"
echo "a6424be9d8f42f8afbe2a0e576af45417a8fad3d9dcac100e8387760bd711853  2ASYE-T-QT-PRO-external-photos.pdf" | sha256sum -c -
```

The archive path above is a **convenience**. Everything needed to recover this file without the archive — hash, byte size, FCC ID, exhibit type, document id, publication date and 5 URLs — is in this file.
