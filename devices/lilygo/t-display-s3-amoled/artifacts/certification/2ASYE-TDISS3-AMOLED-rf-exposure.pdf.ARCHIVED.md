# ARCHIVED: `2ASYE-TDISS3-AMOLED-rf-exposure.pdf`

> This file was **moved out of the repository**, not deleted.
> Archived **2026-09-11** by the round-2 index merge.

**Reason:** bulk FCC exhibit — rf exposure info, 152,844 B (0.15 MiB). The round-2 artifact split keeps internal photographs and ID-label exhibits in the repository (they are the identification and teardown evidence) and archives the full test reports, RF-exposure annexes, users manuals and external-photo sets, which are bulky and repetitive.

## Identity

| Field | Value |
|---|---|
| Original repo path | `devices/lilygo/t-display-s3-amoled/artifacts/certification/2ASYE-TDISS3-AMOLED-rf-exposure.pdf` |
| Archived to | `/home/user/repo-archive/hardware-doc/devices/lilygo/t-display-s3-amoled/artifacts/certification/2ASYE-TDISS3-AMOLED-rf-exposure.pdf` |
| Type | file (PDF, magic-byte validated `%PDF`) |
| Size | 152,844 B (0.15 MiB) |
| SHA-256 | `8c40576dcdf810a5a88a9277110802fd85e8b6e7549d75471efec77d9ebd7623` |
| FCC ID | **`2ASYE-TDISS3-AMOLED`** |
| Exhibit type | **RF Exposure Info** |
| Exhibit title, as filed | RF Exposure |
| FCC document id | 8123279 |
| Upstream publication date | 2025-03-17 |
| Grant date | 2025-03-17 |
| Equipment class | T-Display-S3-AMOLED, 2402-2480 MHz, 2412-2472 MHz |
| Applicant | Shenzhen Xin Yuan Electronic Technology Co., Ltd. 🇨🇳 |
| Test firm | Bay Area Compliance Laboratories Corp (Shenzhen) |
| Retrieved | 2026-09-11 |
| Licence | **US Government public record.** FCC equipment-authorisation exhibits are published by a federal agency under 47 CFR §2.1033 and carry no copyright claim by the agency. |
| Redistribution status | **`allowed`** |
| Disposition | `archive`, placeholder in repository |

## How to get it back

Independent reacquisition URLs, most reliable first:

- <https://fccid.io/2ASYE-TDISS3-AMOLED/RF-Exposure-Info/RF-Exposure-8123279.pdf>  
  fccid.io mirror — **200**, but only to a non-browser UA (`curl/8.5.0`, `WhatsApp/2.23.20.0`, `ChatGPT-User/1.0`, `ClaudeBot/1.0`). A Chrome UA gets a Cloudflare 403. The `.pdf` suffix is required.

- <https://apps.fcc.gov/eas/GetApplicationAttachment.html?id=8123279>  
  official FCC Equipment Authorization System attachment — the primary record. **403 to all five UAs tried from this host on 2026-09-11**; try from another network.

- <https://fcc.report/FCC-ID/2ASYE-TDISS3-AMOLED/8123279.pdf>  
  fcc.report mirror. **403 to all five UAs tried on 2026-09-11.**

- <https://fccid.io/2ASYE-TDISS3-AMOLED>  
  the filing's exhibit index — re-read the row to recover a changed document slug.

- <https://web.archive.org/web/2/https://fccid.io/2ASYE-TDISS3-AMOLED/RF-Exposure-Info/RF-Exposure-8123279.pdf>  
  Wayback Machine, if every live route is dead.

Restore from the local archive, if you have one:

```bash
mv "/home/user/repo-archive/hardware-doc/devices/lilygo/t-display-s3-amoled/artifacts/certification/2ASYE-TDISS3-AMOLED-rf-exposure.pdf" \
   "devices/lilygo/t-display-s3-amoled/artifacts/certification/2ASYE-TDISS3-AMOLED-rf-exposure.pdf"
```

Or re-download and verify — note the User-Agent, which is not optional:

```bash
curl -fsSL -A "curl/8.5.0" "https://fccid.io/2ASYE-TDISS3-AMOLED/RF-Exposure-Info/RF-Exposure-8123279.pdf" -o "2ASYE-TDISS3-AMOLED-rf-exposure.pdf"
echo "8c40576dcdf810a5a88a9277110802fd85e8b6e7549d75471efec77d9ebd7623  2ASYE-TDISS3-AMOLED-rf-exposure.pdf" | sha256sum -c -
```

The archive path above is a **convenience**. Everything needed to recover this file without the archive — hash, byte size, FCC ID, exhibit type, document id, publication date and 5 URLs — is in this file.
