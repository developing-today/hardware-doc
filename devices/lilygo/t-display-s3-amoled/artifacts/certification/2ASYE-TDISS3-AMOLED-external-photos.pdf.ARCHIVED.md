# ARCHIVED: `2ASYE-TDISS3-AMOLED-external-photos.pdf`

> This file was **moved out of the repository**, not deleted.
> Archived **2026-09-11** by the round-2 index merge.

**Reason:** bulk FCC exhibit — external photos, 1,797,931 B (1.71 MiB). The round-2 artifact split keeps internal photographs and ID-label exhibits in the repository (they are the identification and teardown evidence) and archives the full test reports, RF-exposure annexes, users manuals and external-photo sets, which are bulky and repetitive.

## Identity

| Field | Value |
|---|---|
| Original repo path | `devices/lilygo/t-display-s3-amoled/artifacts/certification/2ASYE-TDISS3-AMOLED-external-photos.pdf` |
| Archived to | `/home/user/repo-archive/hardware-doc/devices/lilygo/t-display-s3-amoled/artifacts/certification/2ASYE-TDISS3-AMOLED-external-photos.pdf` |
| Type | file (PDF, magic-byte validated `%PDF`) |
| Size | 1,797,931 B (1.71 MiB) |
| SHA-256 | `28026191703ef5d57ec29a752dbee1d896c3dd6dbc180a201e8d2c39c9eb7930` |
| FCC ID | **`2ASYE-TDISS3-AMOLED`** |
| Exhibit type | **External Photos** |
| Exhibit title, as filed | External Photos |
| FCC document id | 8123268 |
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

- <https://fccid.io/2ASYE-TDISS3-AMOLED/External-Photos/External-Photos-8123268.pdf>  
  fccid.io mirror — **200**, but only to a non-browser UA (`curl/8.5.0`, `WhatsApp/2.23.20.0`, `ChatGPT-User/1.0`, `ClaudeBot/1.0`). A Chrome UA gets a Cloudflare 403. The `.pdf` suffix is required.

- <https://apps.fcc.gov/eas/GetApplicationAttachment.html?id=8123268>  
  official FCC Equipment Authorization System attachment — the primary record. **403 to all five UAs tried from this host on 2026-09-11**; try from another network.

- <https://fcc.report/FCC-ID/2ASYE-TDISS3-AMOLED/8123268.pdf>  
  fcc.report mirror. **403 to all five UAs tried on 2026-09-11.**

- <https://fccid.io/2ASYE-TDISS3-AMOLED>  
  the filing's exhibit index — re-read the row to recover a changed document slug.

- <https://web.archive.org/web/2/https://fccid.io/2ASYE-TDISS3-AMOLED/External-Photos/External-Photos-8123268.pdf>  
  Wayback Machine, if every live route is dead.

Restore from the local archive, if you have one:

```bash
mv "/home/user/repo-archive/hardware-doc/devices/lilygo/t-display-s3-amoled/artifacts/certification/2ASYE-TDISS3-AMOLED-external-photos.pdf" \
   "devices/lilygo/t-display-s3-amoled/artifacts/certification/2ASYE-TDISS3-AMOLED-external-photos.pdf"
```

Or re-download and verify — note the User-Agent, which is not optional:

```bash
curl -fsSL -A "curl/8.5.0" "https://fccid.io/2ASYE-TDISS3-AMOLED/External-Photos/External-Photos-8123268.pdf" -o "2ASYE-TDISS3-AMOLED-external-photos.pdf"
echo "28026191703ef5d57ec29a752dbee1d896c3dd6dbc180a201e8d2c39c9eb7930  2ASYE-TDISS3-AMOLED-external-photos.pdf" | sha256sum -c -
```

The archive path above is a **convenience**. Everything needed to recover this file without the archive — hash, byte size, FCC ID, exhibit type, document id, publication date and 5 URLs — is in this file.
